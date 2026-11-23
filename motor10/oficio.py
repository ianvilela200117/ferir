#!/usr/bin/env python3
"""oficio.py — MOTOR 10: O OFÍCIO. Forjar é uma obra de vários dias, com matéria contada, que pode falhar e custa caro.
Consertar é o pão do ferreiro. Ajustar faz a peça servir a um dono. Tudo por evento; os números moram no tabelas_oficio.py.

  FORJAR uma peça de categoria k: a matéria (até o Raro, matéria da categoria; do Épico para cima, um NÚCLEO da categoria mais matéria Rara),
    3^k blocos PESADOS de bancada numa oficina, e no fim UM teste: 2d20 + maestria do ofício + Afinidade ÷ 10 + a oficina (0 a 4)
    + o preparo (até +8), contra 28 + 6 × k. Sem requisito de nível, e sem tranca de maestria: quem tem a matéria pode tentar.
  A OBRA FICA ABERTA entre um dia e outro: a matéria entra quando ela abre, os blocos somam, o ato para quando o corpo pede, o teste só sai quando os blocos fecham.
  FALHAR CUSTA: por menos de 5, a peça sai uma categoria abaixo (o Comum sai tosco); por 5 ou mais, a matéria some, e o núcleo sai do Livro de Itens.
  O PREPARO tem alcance: receita e ajudante (da pessoa), fogo e bigorna (do lugar), +2 cada um, só na obra da categoria que ele alcança.
  A MAESTRIA do ofício (forja; couro, para a armadura de couro) sobe por blocos de bancada; de Mestre para cima pede um feito (uma obra nascida).
  CONSERTAR: você na bancada (tempo e um pouco de matéria; pede a mão da categoria), ou pago à oficina do lugar (2% do preço por ponto).
  AJUSTAR (sob medida): grava o dono na peça; o grau (1 a 4) sai da mão de quem ajusta; custa blocos e um teste.

Uso (o personagem do jogador, ou quem=ID):
  python3 oficio.py ver                                   a oficina daqui, a sua mão, o preparo, as obras abertas, a matéria que você carrega
  python3 oficio.py pede arma FAMILIA CATEGORIA           o que a obra pede (matéria, núcleo, blocos) e a sua conta no teste, sem abrir nada
  python3 oficio.py pede armadura MATERIAL CATEGORIA [cobre=cabeça]   ·   python3 oficio.py pede escudo CATEGORIA
  python3 oficio.py forjar arma FAMILIA CATEGORIA ["Nome"] [blocos=N] [nucleo=ID]    abre a obra (a matéria entra) e trabalha N blocos
  python3 oficio.py forjar armadura MATERIAL CATEGORIA ["Nome"] [cobre=tronco,braços,pernas] [blocos=N] [nucleo=ID]    (elmo: cobre=cabeça)
  python3 oficio.py forjar escudo CATEGORIA ["Nome"] [blocos=N] [nucleo=ID]
  python3 oficio.py continua [OBRA] [blocos=N]            mais N blocos na obra aberta (sem N: até fechar, ou até o corpo parar)
  python3 oficio.py larga OBRA                            abandona a obra (a matéria que já foi ao fogo se perde; o núcleo fica)
  python3 oficio.py consertar ITEM [pontos=N] [pago]      devolve durabilidade: você na bancada, ou `pago` à oficina do lugar
  python3 oficio.py ajustar ITEM [para=ID] [blocos=N]     sob medida para alguém que está aqui (sem para: para você)
  python3 oficio.py jornal N [oficio=forja|couro]         N blocos de bancada a serviço da oficina do lugar (ela paga o seu salário por bloco)
  python3 oficio.py preparo receita|ajudante|fogo|bigorna CATEGORIA|nada "como foi ganho"     o Mestre registra um preparo ganho no mundo
  python3 oficio.py oficina NIVEL|nada "como foi"         o Mestre registra a oficina do lugar onde a pessoa está (0 a 4; nada: o lugar fica sem)
FAMILIA: adaga espada maça machado martelo lança montante alabarda malho arco besta · MATERIAL: couro malha placa
CATEGORIA: Comum Incomum Raro Épico Único Lendário
"""
import math, sys
import tabelas as T
import tabelas_mundo as M
import tabelas_oficio as O
import estado, ato, corpo, teste
from itens import item, cat_i

PECAS = ('arma', 'armadura', 'escudo')
FEM = ['Comum', 'Incomum', 'Rara', 'Épica', 'Única', 'Lendária', 'Mítica', 'Primordial']       # a categoria, quando o nome que vem antes é feminino (a peça, a obra)


# ---------- o dado, contado (para dizer a chance antes de abrir a obra) ----------
def _somas():
    """a distribuição de 2d20 em que cada 20 rola de novo e soma (como o teste.py rola)"""
    um = {}
    for k in range(5):
        for x in range(1, 20): um[20 * k + x] = 0.05 ** (k + 1)
    dois = {}
    for a, pa in um.items():
        for b, pb in um.items(): dois[a + b] = dois.get(a + b, 0) + pa * pb
    return dois
_SOMAS = _somas()


def chance_de(precisa):
    """a chance de 2d20 (com o 20 que rola de novo) dar `precisa` ou mais"""
    return min(1.0, sum(p for s, p in _SOMAS.items() if s >= precisa))


def chances(soma, contra):
    """(acerta, sai uma abaixo, perde tudo) para quem soma `soma` ao 2d20 contra `contra`"""
    acerta = chance_de(contra - soma); pouco = chance_de(contra - soma - (O.POR_POUCO - 1)) - acerta
    return acerta, pouco, max(0.0, 1 - acerta - pouco)


# ---------- ler: a oficina, a mão, o preparo, a conta ----------
def _vivo(E, pid):
    p = E['gente'].get(pid) or sys.exit(f'não há a pessoa "{pid}"')
    if p['estado'] != 'vivo': sys.exit(f"{p['nome']} não está vivo")
    return p


def oficina(E, lid):
    """o nível da oficina do lugar (0 a 4), ou None se o lugar não tem oficina"""
    v = E['lugares'][lid].get('oficina')
    if v is None or v is False or not isinstance(v, (int, float)): return None
    return max(0, min(len(O.OFICINAS) - 1, int(v)))


def nome_oficina(v): return f'{O.OFICINAS[v]} (+{v})'
def mao(p, oficio='forja'): m = p.get('maestria'); return m.get(oficio, 0) if isinstance(m, dict) else 0             # a maestria no ofício (0 a 8)
def bancada(p, oficio='forja'): t = p.get('treino'); return t.get(oficio, 0) if isinstance(t, dict) else 0         # os blocos de bancada já feitos


def preparos(E, pid, lid=None):
    """{receita, ajudante, fogo, bigorna: o índice da categoria que ele alcança, ou None se não há}"""
    p = E['gente'][pid]; l = E['lugares'][lid or p['lugar']]; out = {}; do_lugar = l.get('preparo') if isinstance(l.get('preparo'), dict) else {}
    for nome, (de, chave) in O.PREPAROS.items():
        v = p.get('marca', {}).get(chave) if de == 'pessoa' else do_lugar.get(chave)
        out[nome] = int(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else None
    return out


def preparo(E, pid, cat, lid=None):
    """o preparo que vale numa obra de categoria `cat`: +2 por preparo que a alcança, até +8"""
    return min(O.PREPARO_MAX, O.PREPARO_CADA * sum(1 for v in preparos(E, pid, lid).values() if v is not None and v >= cat))


def conta(E, pid, cat, oficio='forja', lid=None, contra=None):
    """a conta do teste desta pessoa, hoje, numa obra desta categoria: o que soma, contra quanto, e as três chances"""
    p = E['gente'][pid]; lid = lid or p['lugar']; v = oficina(E, lid) or 0
    c = dict(maestria=mao(p, oficio), afinidade=p['atributos']['Afinidade'] // 10, oficina=v, preparo=preparo(E, pid, cat, lid), pena=corpo.pena(p), contra=O.contra(cat) if contra is None else contra)
    c['mais'] = c['maestria'] + c['oficina'] + c['preparo']                 # o que entra como "mais" no teste.rola (a Afinidade e a pena, ele mesmo soma)
    c['soma'] = c['mais'] + c['afinidade'] + c['pena']
    c['acerta'], c['pouco'], c['perde'] = chances(c['soma'], c['contra'])
    return c


def diz_conta(c, pouco='sai uma abaixo', perde='perde tudo'):
    partes = f"maestria {c['maestria']} + Afinidade {c['afinidade']} + oficina {c['oficina']} + preparo {c['preparo']}" + (f" {c['pena']} do corpo" if c['pena'] else '')
    return f"2d20 + {c['soma']} ({partes}) contra {c['contra']}: acerta {c['acerta']:.0%} · {pouco} {c['pouco']:.0%} · {perde} {c['perde']:.0%}"


def _em(E, lid): l = E['lugares'][lid]; return l.get('em', 'em ' + l['nome'])
def obras_de(E, pid): return {k: o for k, o in E['itens'].get('obras', {}).items() if o.get('quem') == pid}
def _mat(chave): n, c = M.le_materia(chave); return f"{n} {(FEM if n.endswith('a') else T.CATS)[c]}" if c is not None else chave        # "metal Raro", "madeira Rara"
def _lista(d): return ', '.join(f'{n} de {_mat(k)}' for k, n in d.items())


def materia_do_mundo(E):
    """toda a matéria com categoria que existe: nas cargas, nos estoques e dentro das obras abertas (para as provas: a conta tem de fechar)"""
    tot = {}
    def junta(d):
        for k, n in (d or {}).items():
            if M.le_materia(k)[1] is not None: tot[k] = tot.get(k, 0) + n
    for p in E['gente'].values(): junta(p.get('carga'))
    for l in E['lugares'].values(): junta(l.get('estoque'))
    for o in E['itens'].get('obras', {}).values(): junta(o.get('materia'))
    return tot


def prata_do_mundo(E): return sum(p['moedas'] for p in E['gente'].values()) + sum(l['estoque'].get('prata', 0) for l in E['lugares'].values())


# ---------- a peça que se quer ----------
def molde(tipo, cat, nome=None, familia=None, material=None, cobre=None):
    """o que se vai forjar, conferido ANTES de qualquer coisa mudar: {tipo, cat, nome, familia | material e cobre}"""
    if tipo not in PECAS: sys.exit(f'não se forja "{tipo}" (forja-se: {", ".join(PECAS)})')
    c = cat_i(cat)
    if c > O.FORJA_ATE: sys.exit(f'ninguém forja acima do {T.CATS[O.FORJA_ATE]} (veio {T.CATS[c]})')
    if tipo == 'arma' and familia not in O.MATERIA_ARMA: sys.exit(f'não se forja a arma "{familia}" (forja-se: {", ".join(O.MATERIA_ARMA)})')
    it = item(tipo, c, nome, familia=familia, material=material, cobre=cobre)        # confere o material e as partes, e dá o nome padrão
    d = dict(tipo=tipo, cat=c, nome=it['nome'])
    if tipo == 'arma': d['familia'] = familia
    if tipo == 'armadura': d['material'] = material; d['cobre'] = it['cobre']
    return d


def _materia_conserto(it):
    """a chave da matéria que o conserto desta peça gasta, ou None se a tabela não sabe de que ela é feita"""
    try: return O.materia_conserto(it['tipo'], it['cat'], it.get('familia'), it.get('material'), it.get('cobre'))
    except KeyError: return None
def oficio_de(x): return O.oficio_da(x['tipo'], x.get('material'))
def materia_de(x, cat=None): return O.materia(x['tipo'], x['cat'] if cat is None else cat, x.get('familia'), x.get('material'), x.get('cobre'))


def _nucleo(E, pid, cat, nid=None):
    """o núcleo que entra na obra: da categoria da obra, na mão de quem forja, e fora de outra obra aberta"""
    ocupados = {o.get('nucleo') for o in E['itens'].get('obras', {}).values()}; L = E['itens']['itens']
    if nid:
        it = L.get(nid) or sys.exit(f'não há o item "{nid}" no Livro de Itens')
        if it['tipo'] != 'nucleo': sys.exit(f"{it['nome']} ({nid}) não é um núcleo")
        if it['cat'] != cat: sys.exit(f"{it['nome']} é um núcleo {T.CATS[it['cat']]}: a obra {FEM[cat]} pede um núcleo {T.CATS[cat]}")
        if it.get('dono') != pid: sys.exit(f"{it['nome']} não está na mão de quem forja")
        if nid in ocupados: sys.exit(f"{it['nome']} já está dentro de outra obra aberta")
        return nid
    for iid, it in L.items():
        if it['tipo'] == 'nucleo' and it['cat'] == cat and it.get('dono') == pid and iid not in ocupados: return iid
    sys.exit(f'uma obra {FEM[cat]} pede um núcleo {T.CATS[cat]} na mão de quem forja (item do Livro de Itens, tipo "nucleo"). Não há nenhum livre.')


def pede(E, pid, peca):
    """o que a obra pede e a conta de hoje, sem abrir nada"""
    p = _vivo(E, pid); cat = peca['cat']; of = oficio_de(peca); v = oficina(E, p['lugar']); mat = materia_de(peca); carga = p.get('carga', {})
    L = [f"{peca['nome']} ({T.CATS[cat]}) · ofício: {of} · {O.blocos(cat)} bloco(s) pesado(s) de bancada",
         'Matéria: ' + ', '.join(f"{n} de {_mat(k)} (você tem {carga.get(k, 0)})" for k, n in mat.items())
         + (f' · e um núcleo {T.CATS[cat]}' if O.pede_nucleo(cat) else '')]
    if v is None: L.append('Aqui não há oficina: a obra não abre.')
    else: L.append('O teste final, hoje e aqui: ' + diz_conta(conta(E, pid, cat, of), pouco='sai uma abaixo' if cat else 'sai tosca'))
    if mao(p, of) < O.MAO_DA_OBRA[cat]:
        L.append(f"AVISO: a obra {FEM[cat]} pede mão de {T.MAESTRIAS[O.MAO_DA_OBRA[cat]]}; a sua é de {T.MAESTRIAS[mao(p, of)]}. Pode tentar; o que entra na obra não volta.")
    return '\n'.join(L)


# ---------- a maestria ----------
def sobe(E, pid, oficio='forja'):
    """a maestria do ofício sobe quando os blocos de bancada chegam; de Mestre para cima, só com o FEITO (marca.feito_OFICIO)"""
    p = E['gente'][pid]; tem = mao(p, oficio); bl = bancada(p, oficio); txt = ''
    for grau, quer in sorted(O.OFICIO_BLOCOS.items()):
        if grau <= tem or bl < quer: continue
        if grau in O.FEITO_OBRA and p.get('marca', {}).get(f'feito_{oficio}', 0) < grau:
            txt = f" (tem os blocos para {T.MAESTRIAS[grau]} em {oficio}; falta o feito: uma obra {FEM[O.FEITO_OBRA[grau]]}, ou melhor, nascida da sua mão)"; break
        estado.aplica(E, 'treinar', [['pessoa', pid, 'maestria.' + oficio, 'poe', grau]], onde=p['lugar'], quem=[pid], texto=f"{p['nome']} chega a {T.MAESTRIAS[grau]} em {oficio}")
        p = E['gente'][pid]; tem = grau; txt = f'. MAESTRIA: {T.MAESTRIAS[grau]} em {oficio}'
    return txt


# ---------- forjar ----------
def forjar(E, pid, peca, blocos=None, nucleo=None):
    """abre a obra (a matéria sai da carga e entra nela) e trabalha `blocos` blocos (None: até fechar, ou até o corpo parar; 0: só abre)"""
    p = _vivo(E, pid); lid = p['lugar']; cat = peca['cat']; of = oficio_de(peca)
    if oficina(E, lid) is None: sys.exit(f"{E['lugares'][lid]['nome']} não tem oficina: a obra não abre")
    mat = materia_de(peca); carga = p.get('carga', {}); falta = {k: n - carga.get(k, 0) for k, n in mat.items() if carga.get(k, 0) < n}
    if falta: sys.exit(f"falta matéria para {peca['nome']} ({T.CATS[cat]}): {_lista(falta)} (a obra pede {_lista(mat)})")
    nid = _nucleo(E, pid, cat, nucleo) if O.pede_nucleo(cat) else None
    if nucleo and not nid: sys.exit(f'uma obra {FEM[cat]} não leva núcleo (só do {T.CATS[M.MATERIA_ATE + 1]} para cima)')
    reg = dict(quem=pid, lugar=lid, tipo='forjar', oficio=of, peca=dict(peca), cat=cat, blocos=0, pede=O.blocos(cat), materia=mat, nucleo=nid)
    ef = [['pessoa', pid, 'carga.' + k, 'soma', -n] for k, n in mat.items()] + [['obra', 'abre', reg]]
    if nid: ef.append(['item', nid, 'historia', 'junta', f"Dia {E['relogio']['dia']}: entrou na obra de {peca['nome']}"])
    estado.aplica(E, 'forjar', ef, onde=lid, quem=[pid], texto=f"{p['nome']} abre a obra: {peca['nome']} ({T.CATS[cat]}); entram {_lista(mat)}" + (f" e {E['itens']['itens'][nid]['nome']}" if nid else ''))
    oid = f"o{E['itens']['oseq']:04d}"
    R = continua(E, pid, oid, blocos)
    R['texto'] = f"Obra {oid} aberta: {peca['nome']} ({T.CATS[cat]}). Entraram {_lista(mat)}" + (f" e o núcleo {nid}" if nid else '') + '.\n' + R['texto']
    return R


def _obra(E, pid, oid=None):
    minhas = obras_de(E, pid)
    if oid:
        if oid not in minhas: sys.exit(f'não há a obra "{oid}" aberta em nome de {E["gente"][pid]["nome"]}' + (f' (abertas: {", ".join(minhas)})' if minhas else ''))
        return minhas[oid]
    if len(minhas) == 1: return next(iter(minhas.values()))
    sys.exit('não há obra aberta.' if not minhas else f'há mais de uma obra aberta: diga qual ({", ".join(minhas)})')


def _nome_obra(E, o):
    if o['tipo'] == 'forjar': return f"{o['peca']['nome']} ({T.CATS[o['cat']]})"
    it = E['itens']['itens'].get(o['item']); return f"o ajuste de {it['nome'] if it else o['item']}"


def continua(E, pid, oid=None, blocos=None):
    """trabalha na obra aberta. Para quando os blocos fecham (e aí sai o teste), quando acabam os blocos pedidos, ou quando o corpo cruza um limiar."""
    p = _vivo(E, pid); o = _obra(E, pid, oid); oid = o['id']; of = o['oficio']
    if p['lugar'] != o['lugar']: sys.exit(f"a obra {oid} está {_em(E, o['lugar'])}: é lá que se trabalha nela")
    if oficina(E, o['lugar']) is None: sys.exit(f"{E['lugares'][o['lugar']]['nome']} não tem mais oficina: a obra {oid} não anda")
    if o.get('nucleo') and E['itens']['itens'].get(o['nucleo'], {}).get('dono') != pid: sys.exit(f"o núcleo da obra {oid} não está mais na mão de quem forja: a obra não anda (largue-a com `larga`)")
    if o['tipo'] == 'ajustar' and _ajuste_solto(E, o): sys.exit(f"{_ajuste_solto(E, o)}: a obra {oid} não anda (largue-a com `larga`)")
    falta = max(0, o['pede'] - o['blocos']); n = falta if blocos is None else max(0, min(int(blocos), falta)); nome = _nome_obra(E, o)
    feitos, pq = ato.passa(E, pid, n, o['tipo'], esforco='pesado', texto=f"{p['nome']} trabalha na obra: {nome}",
                           mais=lambda i: [['obra', oid, 'blocos', 'soma', 1], ['pessoa', pid, 'treino.' + of, 'soma', 1]])
    o = E['itens']['obras'][oid]; p = E['gente'][pid]
    R = dict(obra=oid, feitos=feitos, parou=pq, fim=None, item=None, rolagem=None)
    R['texto'] = f"{p['nome']} trabalha {feitos} bloco(s) na obra {oid}, {nome}: {o['blocos']} de {o['pede']}" + (sobe(E, pid, of) if feitos else '') + (f'. PAROU: {pq}' if pq else '')
    if o['blocos'] >= o['pede'] and E['gente'][pid]['estado'] == 'vivo':
        F = remata(E, oid); R.update(fim=F['fim'], item=F['item'], rolagem=F['rolagem']); R['texto'] += '\n' + F['texto']
    return R


def remata(E, oid):
    """os blocos fecharam: sai o teste final (dado de verdade, uma vez) e a obra fecha"""
    o = E['itens'].get('obras', {}).get(oid) or sys.exit(f'não há a obra "{oid}"')
    if o['blocos'] < o['pede']: sys.exit(f"a obra {oid} tem {o['blocos']} de {o['pede']} blocos: o teste só sai quando os blocos fecham")
    _vivo(E, o['quem'])
    return _remata_forja(E, o) if o['tipo'] == 'forjar' else _remata_ajuste(E, o)


def _remata_forja(E, o):
    oid = o['id']; pid = o['quem']; p = E['gente'][pid]; cat = o['cat']; peca = o['peca']; lid = o['lugar']; of = o['oficio']; nid = o.get('nucleo'); L = E['itens']['itens']
    if nid and nid not in L: sys.exit(f'o núcleo da obra {oid} não está mais no Livro de Itens: a obra não fecha (largue-a com `larga`)')
    c = conta(E, pid, cat, of, lid); nuc = L[nid]['nome'] if nid else None; dia = E['relogio']['dia']
    r = teste.rola(E, f"forjar {peca['nome']} ({T.CATS[cat]})", 'Afinidade', c['contra'], mais=c['mais'], quem=pid)
    margem = r['total'] - r['contra']; sai = cat if margem >= 0 else cat - 1 if margem > -O.POR_POUCO else None; ef = []; it = None
    fim = 'acertou' if margem >= 0 else 'abaixo' if sai is not None else 'perdeu'
    if sai is not None:
        it = item(peca['tipo'], max(0, sai), peca['nome'], familia=peca.get('familia'), material=peca.get('material'), cobre=peca.get('cobre'), dono=pid, feito_por=pid, dia=dia)
        como = f"Dia {dia}: forjada por {p['nome']} {_em(E, lid)}" + (f', com {nuc}' if nuc else '')
        if sai < 0: it['dur'][0] = max(1, int(it['dur'][1] * O.TOSCA)); como += '; saiu tosca'
        elif sai < cat: como += f'; era para ser {FEM[cat]} e saiu {FEM[sai]}'
        if nid and L[nid].get('de'): it['nucleo_de'] = L[nid]['de']
        it['historia'].append(como); ef.append(['item', 'nasce', it])
        for grau, quer in sorted(O.FEITO_OBRA.items()):                     # o feito: uma obra nascida da categoria certa (ou melhor)
            if it['cat'] >= quer and p.get('marca', {}).get(f'feito_{of}', 0) < grau: ef.append(['pessoa', pid, f'marca.feito_{of}', 'poe', grau])
    if nid: ef.append(['item', nid, 'some'])
    ef.append(['obra', oid, 'fecha'])
    conta_txt = f"{r['total']} contra {r['contra']}"
    if fim == 'acertou': txt = f"{p['nome']} forja {peca['nome']} ({T.CATS[cat]}): {conta_txt}"
    elif fim == 'abaixo': txt = f"{p['nome']} erra por pouco ({conta_txt}): {peca['nome']} sai " + (f'{FEM[sai]}, uma categoria abaixo' if sai >= 0 else 'Comum e tosca') + (f'; {nuc} se gasta nela' if nuc else '')
    else: txt = f"a obra de {peca['nome']} ({T.CATS[cat]}) se perde ({conta_txt}): some a matéria ({_lista(o['materia'])})" + (f' e some {nuc}' if nuc else '')
    estado.aplica(E, 'forjar', ef, onde=lid, quem=[pid], texto=txt)
    iid = f"i{E['itens']['seq']:04d}" if it else None
    out = teste.diz(E, r) + f"\n  (o +{c['mais']}: maestria {c['maestria']}, oficina {c['oficina']}, preparo {c['preparo']})\n" + txt + (f'. Entrou no Livro de Itens: {iid}' if iid else '') + sobe(E, pid, of)
    return dict(obra=oid, fim=fim, item=iid, rolagem=r, texto=out)


def larga(E, pid, oid):
    """abandona a obra. A matéria que já foi ao fogo se perde (com zero blocos, volta à carga); o núcleo fica com o dono: só o teste o gasta."""
    p = _vivo(E, pid); o = _obra(E, pid, oid); ef = [['obra', o['id'], 'fecha']]; volta = o['tipo'] == 'forjar' and o['blocos'] == 0
    if volta: ef += [['pessoa', pid, 'carga.' + k, 'soma', n] for k, n in o['materia'].items()]
    txt = f"{p['nome']} larga a obra: {_nome_obra(E, o)}" + ('' if o['tipo'] != 'forjar' else f" (a matéria volta: {_lista(o['materia'])})" if volta else f" (a matéria se perde: {_lista(o['materia'])})")
    estado.aplica(E, o['tipo'], ef, onde=p['lugar'], quem=[pid], texto=txt)
    return dict(obra=o['id'], fim='largada', item=None, rolagem=None, texto=txt + '.')


# ---------- consertar ----------
def consertar(E, pid, iid, pontos=None, pago=False):
    """devolve durabilidade a uma peça da pessoa: ela mesma na bancada (blocos pesados e um pouco de matéria), ou paga à oficina do lugar (2% do preço por ponto)"""
    p = _vivo(E, pid); lid = p['lugar']; l = E['lugares'][lid]; it = E['itens']['itens'].get(iid) or sys.exit(f'não há o item "{iid}" no Livro de Itens')
    if it['tipo'] not in PECAS: sys.exit(f"{it['nome']} não é peça que se conserte")
    if it.get('dono') != pid: sys.exit(f"{it['nome']} não é de {p['nome']}")
    v = oficina(E, lid)
    if v is None: sys.exit(f"{l['nome']} não tem oficina: não se conserta aqui")
    gasto = it['dur'][1] - it['dur'][0]
    if gasto <= 0: sys.exit(f"{it['nome']} está inteira ({it['dur'][0]}/{it['dur'][1]})")
    q = gasto if pontos is None else min(int(pontos), gasto)
    if q < 1: sys.exit('diga quantos pontos consertar (1 ou mais)')
    cat = it['cat']
    if pago:
        if cat > v + O.OFICINA_CONSERTA: sys.exit(f"a {O.OFICINAS[v]} de {l['nome']} só conserta até o {T.CATS[min(v + O.OFICINA_CONSERTA, len(T.CATS) - 1)]}; {it['nome']} é {T.CATS[cat]}")
        custo = O.conserto_pago(cat, q)
        if p['moedas'] < custo: sys.exit(f"consertar {q} ponto(s) de {it['nome']} ({T.CATS[cat]}) custa {custo} de prata; {p['nome']} tem {p['moedas']}")
        estado.aplica(E, 'consertar', [['pessoa', pid, 'moedas', 'soma', -custo], ['estoque', lid, 'prata', 'soma', custo], ['item', iid, 'dur', 'soma', q]], onde=lid, quem=[pid],
                      texto=f"{p['nome']} paga {custo} de prata à {O.OFICINAS[v]} pelo conserto de {it['nome']} ({q} ponto(s))")
        n, pq = ato.passa(E, pid, math.ceil(q / O.PAGO_BLOCO), 'consertar', esforco='nada', texto=f"{p['nome']} espera o conserto", para=False)
        it = E['itens']['itens'][iid]
        return dict(pontos=q, custo=custo, feitos=n, parou=pq, texto=f"A {O.OFICINAS[v]} conserta {it['nome']}: {q} ponto(s) por {custo} de prata, em {n} bloco(s). Durabilidade {it['dur'][0]}/{it['dur'][1]}.")
    of = oficio_de(it); pede_mao = O.MAO_DA_OBRA[cat] if cat < len(O.MAO_DA_OBRA) else None
    if pede_mao is None or mao(p, of) < pede_mao:
        sys.exit(f"consertar uma peça {FEM[cat]} pede mão de {T.MAESTRIAS[pede_mao] if pede_mao is not None else 'quem ainda não existe'} em {of}; a de {p['nome']} é de {T.MAESTRIAS[mao(p, of)]}. Pago à oficina: {O.conserto_pago(cat, q)} de prata.")
    chave = _materia_conserto(it) or sys.exit(f"{it['nome']} não é peça que a bancada saiba consertar"); unidades = math.ceil(q / O.CONSERTO_MATERIA)
    if p.get('carga', {}).get(chave, 0) < unidades: sys.exit(f"consertar {q} ponto(s) de {it['nome']} gasta {unidades} de {_mat(chave)}; {p['nome']} carrega {p.get('carga', {}).get(chave, 0)}")
    def mais(i):
        antes = i * O.CONSERTO_BLOCO; agora = min(O.CONSERTO_BLOCO, q - antes); un = math.ceil((antes + agora) / O.CONSERTO_MATERIA) - math.ceil(antes / O.CONSERTO_MATERIA)
        return [['item', iid, 'dur', 'soma', agora], ['pessoa', pid, 'treino.' + of, 'soma', 1]] + ([['pessoa', pid, 'carga.' + chave, 'soma', -un]] if un else [])
    antes = it['dur'][0]; tinha = p.get('carga', {}).get(chave, 0)
    n, pq = ato.passa(E, pid, math.ceil(q / O.CONSERTO_BLOCO), 'consertar', esforco='pesado', mais=mais, texto=f"{p['nome']} conserta {it['nome']}")
    it = E['itens']['itens'][iid]; p = E['gente'][pid]; feito = it['dur'][0] - antes
    return dict(pontos=feito, custo=0, feitos=n, parou=pq, texto=f"{p['nome']} conserta {it['nome']}: {feito} ponto(s) em {n} bloco(s), com {tinha - p.get('carga', {}).get(chave, 0)} de {_mat(chave)}. Durabilidade {it['dur'][0]}/{it['dur'][1]}"
                + sobe(E, pid, of) + (f'. PAROU: {pq}' if pq else '.'))


# ---------- ajustar (sob medida) ----------
def _ajuste_solto(E, o):
    """por que o ajuste não pode seguir (ou None): a peça saiu do Livro ou mudou de mão, ou o dono dela foi embora"""
    it = E['itens']['itens'].get(o['item']); a = E['gente'].get(o['para'])
    if not it: return 'a peça não está mais no Livro de Itens'
    if it.get('dono') not in (o['quem'], o['para']): return f"{it['nome']} mudou de mão"
    if not a or a['estado'] != 'vivo' or a['lugar'] != o['lugar']: return 'quem ia receber a peça não está mais aqui'
    return None


def ajustar(E, pid, iid, para=None, blocos=None):
    """sob medida: abre o ajuste de uma peça para alguém que está aqui (sem `para`: para quem ajusta) e trabalha nele; no fim, um teste"""
    p = _vivo(E, pid); lid = p['lugar']; alvo = para or pid; a = _vivo(E, alvo); it = E['itens']['itens'].get(iid) or sys.exit(f'não há o item "{iid}" no Livro de Itens')
    if it['tipo'] not in PECAS: sys.exit(f"{it['nome']} não é peça que se ajuste")
    if oficina(E, lid) is None: sys.exit(f"{E['lugares'][lid]['nome']} não tem oficina: não se ajusta aqui")
    if a['lugar'] != lid: sys.exit(f"{a['nome']} não está aqui: o ajuste pede o corpo de quem vai usar a peça")
    if it.get('dono') not in (pid, alvo): sys.exit(f"{it['nome']} não é de {p['nome']} nem de {a['nome']}")
    of = oficio_de(it)
    if O.ajuste_grau(mao(p, of)) < T.SOB_MEDIDA_GRAUS[0]: sys.exit(f"ajustar pede pelo menos mão de {T.MAESTRIAS[2]} em {of}; a de {p['nome']} é de {T.MAESTRIAS[mao(p, of)]}")
    if any(o['tipo'] == 'ajustar' and o['item'] == iid for o in E['itens'].get('obras', {}).values()): sys.exit(f"{it['nome']} já está num ajuste aberto")
    reg = dict(quem=pid, lugar=lid, tipo='ajustar', oficio=of, item=iid, para=alvo, cat=it['cat'], blocos=0, pede=O.ajuste_blocos(it['cat']))
    estado.aplica(E, 'ajustar', [['obra', 'abre', reg]], onde=lid, quem=[pid, alvo] if alvo != pid else [pid], texto=f"{p['nome']} abre o ajuste de {it['nome']} para {a['nome']}")
    oid = f"o{E['itens']['oseq']:04d}"
    R = continua(E, pid, oid, blocos); R['texto'] = f"Ajuste {oid} aberto: {it['nome']} ({T.CATS[it['cat']]}) para {a['nome']}.\n" + R['texto']
    return R


def _remata_ajuste(E, o):
    oid = o['id']; pid = o['quem']; p = E['gente'][pid]; lid = o['lugar']; of = o['oficio']
    solto = _ajuste_solto(E, o)
    if solto:
        estado.aplica(E, 'ajustar', [['obra', oid, 'fecha']], onde=lid, quem=[pid], texto=f"o ajuste {oid} se desfaz: {solto}")
        return dict(obra=oid, fim='desfeito', item=o['item'], rolagem=None, texto=f"O ajuste {oid} se desfaz: {solto}.")
    it = E['itens']['itens'][o['item']]; a = E['gente'][o['para']]; cat = it['cat']; grau = O.ajuste_grau(mao(p, of)); c = conta(E, pid, cat, of, lid, contra=O.ajuste_contra(cat))
    r = teste.rola(E, f"ajustar {it['nome']} para {a['nome']}", 'Afinidade', c['contra'], mais=c['mais'], quem=pid)
    margem = r['total'] - r['contra']; ef = [['obra', oid, 'fecha']]; conta_txt = f"{r['total']} contra {r['contra']}"
    if margem >= 0 and grau >= T.SOB_MEDIDA_GRAUS[0]:
        fim = 'acertou'; txt = f"{p['nome']} ajusta {it['nome']} para {a['nome']}, grau {grau} ({conta_txt})"
        ef += [['item', o['item'], 'sob_medida', 'poe', dict(dono=a['nome'], grau=grau, id=o['para'])], ['item', o['item'], 'historia', 'junta', f"Dia {E['relogio']['dia']}: ajustada por {p['nome']} para {a['nome']} (grau {grau})"]]
    elif margem > -O.POR_POUCO: fim = 'falhou'; txt = f"o ajuste de {it['nome']} não assenta ({conta_txt}): fica como estava"
    else:
        fim = 'estragou'; txt = f"o ajuste de {it['nome']} sai errado ({conta_txt}): a peça perde {O.AJUSTE_ESTRAGO} de durabilidade"
        ef.append(['item', o['item'], 'dur', 'soma', -O.AJUSTE_ESTRAGO])
    estado.aplica(E, 'ajustar', ef, onde=lid, quem=[pid], texto=txt)
    return dict(obra=oid, fim=fim, item=o['item'], rolagem=r, texto=teste.diz(E, r) + f"\n  (o +{c['mais']}: maestria {c['maestria']}, oficina {c['oficina']}, preparo {c['preparo']})\n" + txt + '.')


# ---------- o jornal: a bancada a serviço da oficina do lugar ----------
def jornal(E, pid, blocos, oficio='forja'):
    """N blocos de bancada no serviço miúdo da oficina (a ferramenta do povo): o lugar paga o salário do grau de ofício da pessoa, e os blocos contam como bancada"""
    p = _vivo(E, pid); lid = p['lugar']
    if oficio not in ('forja', 'couro'): sys.exit(f'o jornal é de forja ou de couro (veio "{oficio}")')
    if oficina(E, lid) is None: sys.exit(f"{E['lugares'][lid]['nome']} não tem oficina: não há bancada onde servir")
    grau = p.get('grau_oficio', 'diarista'); paga = M.SALARIO.get(grau, M.SALARIO['diarista']); tinha = p['moedas']
    def mais(i):
        ef = [['pessoa', pid, 'treino.' + oficio, 'soma', 1]]
        if E['lugares'][lid]['estoque'].get('prata', 0) >= paga: ef += [['estoque', lid, 'prata', 'soma', -paga], ['pessoa', pid, 'moedas', 'soma', paga]]      # oficina sem prata não paga
        return ef
    n, pq = ato.passa(E, pid, int(blocos), 'trabalhar', esforco=O.JORNAL_ESFORCO, mais=mais, texto=f"{p['nome']} serve na bancada da oficina ({grau})")
    ganhou = E['gente'][pid]['moedas'] - tinha
    return dict(feitos=n, parou=pq, ganhou=ganhou, texto=f"{p['nome']} serve {n} bloco(s) na bancada e recebe {ganhou} de prata" + ('' if ganhou == n * paga else ' (a oficina ficou sem prata para pagar)')
                + sobe(E, pid, oficio) + (f'. PAROU: {pq}' if pq else '.'))


# ---------- o preparo ganho no mundo (o Mestre registra) ----------
def ganha_preparo(E, qual, cat, pid=None, lid=None, como=''):
    """registra um preparo: receita e ajudante vão para a pessoa; fogo e bigorna, para o lugar onde ela está. `cat`: a categoria que ele alcança (None: perde-se)"""
    if qual not in O.PREPAROS: sys.exit(f'preparo desconhecido: "{qual}" (os que existem: {", ".join(O.PREPAROS)})')
    c = None if cat is None else cat_i(cat); de, chave = O.PREPAROS[qual]; alcance = 'nada' if c is None else f'até o {T.CATS[c]}'
    if de == 'pessoa':
        p = _vivo(E, pid); txt = f"{p['nome']} ganha o preparo: {qual} ({alcance})" + (f': {como}' if como else '')
        estado.aplica(E, 'mestre', [['pessoa', pid, 'marca.' + chave, 'poe', c]], onde=p['lugar'], quem=[pid], texto=txt)
    else:
        lid = lid or _vivo(E, pid)['lugar']; l = E['lugares'].get(lid) or sys.exit(f'não há o lugar "{lid}"')
        txt = f"{l['nome']} ganha o preparo: {qual} ({alcance})" + (f': {como}' if como else '')
        estado.aplica(E, 'mestre', [['lugar', lid, 'preparo.' + chave, 'poe', c]], onde=lid, texto=txt)
    return txt + '.'


def poe_oficina(E, lid, nivel, como=''):
    """o Mestre registra a oficina de um lugar (0 a 4), ou tira (None)"""
    l = E['lugares'].get(lid) or sys.exit(f'não há o lugar "{lid}"')
    if nivel is not None and not 0 <= nivel < len(O.OFICINAS): sys.exit(f'a oficina vai de 0 ({O.OFICINAS[0]}) a {len(O.OFICINAS) - 1} ({O.OFICINAS[-1]}); veio {nivel}')
    txt = f"{l['nome']} " + ('fica sem oficina' if nivel is None else f'tem agora uma {nome_oficina(nivel)}') + (f': {como}' if como else '')
    estado.aplica(E, 'mestre', [['lugar', lid, 'oficina', 'poe', nivel]], onde=lid, texto=txt)
    return txt + '.'


# ---------- a virada do dia ----------
def virada(E):
    """o dia virou: a obra de quem morreu se desfaz (a matéria que estava nela some com ela; o núcleo segue no Livro de Itens, como estava)"""
    for oid, o in list(E['itens'].get('obras', {}).items()):
        q = E['gente'].get(o.get('quem'))
        if q and q['estado'] == 'vivo': continue
        estado.aplica(E, 'ajustar' if o.get('tipo') == 'ajustar' else 'forjar', [['obra', oid, 'fecha']], onde=o.get('lugar'), quem=[o['quem']] if q else [],
                      texto=f"a obra {oid} se desfaz: {q['nome'] if q else 'quem a fazia'} morreu")


# ---------- a mesa ----------
def _diz_preparos(E, pid): return ' · '.join(f"{k}: {'não há' if v is None else 'até o ' + T.CATS[min(v, len(T.CATS) - 1)]}" for k, v in preparos(E, pid).items())


def ver(E, pid):
    """as linhas da oficina para esta pessoa: o lugar, a mão, o preparo, as obras, a matéria, o que dá para fazer e o que custa"""
    p = E['gente'][pid]; l = E['lugares'][p['lugar']]; v = oficina(E, p['lugar']); L = []; itens = E['itens']['itens']
    L.append(f"**{l['nome']}:** " + ('não há oficina (não se forja, não se conserta, não se ajusta aqui).' if v is None else f"{nome_oficina(v)} · conserta, pago, até o {T.CATS[min(v + O.OFICINA_CONSERTA, len(T.CATS) - 1)]}"))
    maos = []
    for of in ('forja', 'couro'):
        if not (mao(p, of) or bancada(p, of)) and of != 'forja': continue
        prox = next((f'{T.MAESTRIAS[g]} aos {q}' + (f' e uma obra {FEM[O.FEITO_OBRA[g]]}' if g in O.FEITO_OBRA else '') for g, q in sorted(O.OFICIO_BLOCOS.items()) if g > mao(p, of)), 'o topo')
        maos.append(f"{of} {T.MAESTRIAS[mao(p, of)]} ({bancada(p, of)} blocos de bancada; {prox})")
    L.append('Mão: ' + ' · '.join(maos)); L.append('Preparo (+2 cada, na obra que ele alcança): ' + _diz_preparos(E, pid))
    for oid, o in obras_de(E, pid).items():
        L.append(f"Obra aberta {oid}: {_nome_obra(E, o)}, {o['blocos']} de {o['pede']} blocos, {_em(E, o['lugar'])} (`oficio.py continua {oid}`)")
    mat = {k: n for k, n in p.get('carga', {}).items() if M.le_materia(k)[1] is not None}; nuc = [f"{i} {it['nome']} ({T.CATS[it['cat']]})" for i, it in itens.items() if it['tipo'] == 'nucleo' and it.get('dono') == pid]
    if mat or nuc: L.append('Matéria na carga: ' + (_lista(mat) if mat else 'nenhuma') + (' · núcleos: ' + ', '.join(nuc) if nuc else ''))
    if v is None: return L
    L += ['', '**Na bancada** (bloco pesado; `oficio.py pede ...` diz a matéria e a chance antes de abrir):',
          '- forjar: ' + ', '.join(f'{T.CATS[c]} {O.blocos(c)}' for c in range(O.FORJA_ATE + 1)) + f' blocos; do {T.CATS[M.MATERIA_ATE + 1]} para cima pede núcleo. Falhar por {O.POR_POUCO} ou mais: a matéria some.']
    gastas = [(i, it) for i, it in itens.items() if it.get('dono') == pid and it['tipo'] in PECAS and it['dur'][0] < it['dur'][1]]
    for i, it in gastas[:4]:
        q = it['dur'][1] - it['dur'][0]; of = oficio_de(it); chave = _materia_conserto(it); pode = chave and it['cat'] < len(O.MAO_DA_OBRA) and mao(p, of) >= O.MAO_DA_OBRA[it['cat']]
        eu_txt = f"você, {math.ceil(q / O.CONSERTO_BLOCO)} bloco(s) e {math.ceil(q / O.CONSERTO_MATERIA)} de {_mat(chave)}" if pode else 'você não tem a mão'
        pago = f"pago, {O.conserto_pago(it['cat'], q)} de prata" if it['cat'] <= v + O.OFICINA_CONSERTA else 'esta oficina não conserta'
        L.append(f"- consertar {it['nome']} ({i}, {it['dur'][0]}/{it['dur'][1]}): {eu_txt}; {pago}")
    if len(gastas) > 4: L.append(f'- ... e mais {len(gastas) - 4} peça(s) gasta(s)')
    g = O.ajuste_grau(mao(p))
    L.append('- ajustar (sob medida): ' + (f'grau {g}; de {O.ajuste_blocos(0)} (Comum) a {O.ajuste_blocos(O.FORJA_ATE)} blocos ({T.CATS[O.FORJA_ATE]}) e um teste contra {O.AJUSTE_BASE} + {O.TESTE_CAT} por categoria' if g else f'pede mão de {T.MAESTRIAS[2]}'))
    L.append(f"- jornal: {M.SALARIO.get(p.get('grau_oficio', 'diarista'), M.SALARIO['diarista'])} de prata por bloco de bancada a serviço da oficina (`oficio.py jornal N`)")
    return L


def mesa(E):
    """as linhas do ofício para a MESA.md"""
    pid = estado.eu(E)
    if not pid: return []
    return ['## A oficina'] + ver(E, pid)


# ---------- a linha de comando ----------
def main(a=None):
    a = sys.argv[1:] if a is None else list(a)
    if not a: print(__doc__); return
    op = dict(x.split('=', 1) for x in a if '=' in x); pos = [x for x in a if '=' not in x]
    cmds = ('ver', 'pede', 'forjar', 'continua', 'larga', 'consertar', 'ajustar', 'jornal', 'preparo', 'oficina')
    if pos[0] not in cmds: print(__doc__); return
    E = estado.carrega(); pid = op.get('quem') or estado.eu(E)
    if pid not in E['gente']: sys.exit(f'não há a pessoa "{pid}"')
    inteiro = lambda k: int(op[k]) if op.get(k, '').isdigit() else sys.exit(f'{k}= pede um número (veio "{op[k]}")') if k in op else None
    def peca(i):
        tipo = pos[i] if len(pos) > i else sys.exit('diga o que forjar: arma FAMILIA CATEGORIA, armadura MATERIAL CATEGORIA ou escudo CATEGORIA. Veja o uso: python3 oficio.py')
        if tipo == 'escudo': fam = None; resto = pos[i + 1:]
        else: fam = pos[i + 1] if len(pos) > i + 1 else None; resto = pos[i + 2:]
        if tipo in PECAS and not resto: sys.exit('falta a categoria da peça. Veja o uso: python3 oficio.py')
        resto = resto or [0]
        return molde(tipo, resto[0], resto[1] if len(resto) > 1 else None, familia=fam if tipo == 'arma' else None, material=fam if tipo == 'armadura' else None,
                     cobre=op['cobre'].split(',') if op.get('cobre') else None)
    grava = True
    if pos[0] == 'ver': print('\n'.join(ver(E, pid))); return
    if pos[0] == 'pede': print(pede(E, pid, peca(1))); return
    if pos[0] == 'forjar': print(forjar(E, pid, peca(1), blocos=inteiro('blocos'), nucleo=op.get('nucleo'))['texto'])
    elif pos[0] == 'continua': print(continua(E, pid, pos[1] if len(pos) > 1 else None, blocos=inteiro('blocos'))['texto'])
    elif pos[0] == 'larga' and len(pos) > 1: print(larga(E, pid, pos[1])['texto'])
    elif pos[0] == 'consertar' and len(pos) > 1: print(consertar(E, pid, pos[1], pontos=inteiro('pontos'), pago='pago' in pos[2:])['texto'])
    elif pos[0] == 'ajustar' and len(pos) > 1: print(ajustar(E, pid, pos[1], para=op.get('para'), blocos=inteiro('blocos'))['texto'])
    elif pos[0] == 'jornal' and len(pos) > 1 and pos[1].isdigit() and int(pos[1]) >= 1: print(jornal(E, pid, int(pos[1]), oficio=op.get('oficio', 'forja'))['texto'])
    elif pos[0] == 'preparo' and len(pos) > 2: print(ganha_preparo(E, pos[1], None if pos[2] == 'nada' else pos[2], pid=pid, como=pos[3] if len(pos) > 3 else ''))
    elif pos[0] == 'oficina' and len(pos) > 1 and (pos[1] == 'nada' or pos[1].isdigit()):
        print(poe_oficina(E, E['gente'][pid]['lugar'], None if pos[1] == 'nada' else int(pos[1]), como=pos[2] if len(pos) > 2 else ''))
    else: print(__doc__); grava = False
    if grava:
        estado.grava(E); p = E['gente'][pid]
        print(f"{estado.quando(E)} · PV {p['pv']}/{estado.pv_max(p)} · {corpo.diz(p)} · {p['moedas']} de prata")


if __name__ == '__main__':
    main()
