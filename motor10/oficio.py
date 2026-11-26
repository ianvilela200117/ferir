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
  A BANCADA SERVE A TODO OFÍCIO (etapa da magia): a forja e o couro na oficina; o ENCANTO na mesa de runas (o foco e o amuleto se forjam ali, com a mão de encanto,
    e a gravação de um feitiço numa peça é obra dele: encanto.py); a ALQUIMIA na botica (a leva: alquimia.py); o jornal também no santuário (fé). A obra é uma só:
    abre com a matéria, soma blocos, e o teste sai quando os blocos fecham; quem remata a leva e a gravação é o módulo dela.

Uso (o personagem do jogador, ou quem=ID):
  python3 oficio.py ver                                   a oficina daqui, a sua mão, o preparo, as obras abertas, a matéria que você carrega
  python3 oficio.py pede arma FAMILIA CATEGORIA           o que a obra pede (matéria, núcleo, blocos) e a sua conta no teste, sem abrir nada
  python3 oficio.py pede armadura MATERIAL CATEGORIA [cobre=cabeça]   ·   python3 oficio.py pede escudo CATEGORIA
  python3 oficio.py forjar arma FAMILIA CATEGORIA ["Nome"] [blocos=N] [nucleo=ID]    abre a obra (a matéria entra) e trabalha N blocos
  python3 oficio.py forjar armadura MATERIAL CATEGORIA ["Nome"] [cobre=tronco,braços,pernas] [blocos=N] [nucleo=ID]    (elmo: cobre=cabeça)
  python3 oficio.py forjar escudo CATEGORIA ["Nome"] [blocos=N] [nucleo=ID]
  python3 oficio.py forjar foco FORMA CATEGORIA ["Nome"] · forjar amuleto CATEGORIA ["Nome"]    (etapa da magia) no ofício do encanto, na mesa de runas (o mesmo que encanto.py fazer)
  python3 oficio.py forjar gazua CATEGORIA ["Nome"] [blocos=N]       (etapa 4b) a ferramenta do ladino, como a adaga: 1 de metal da categoria
  python3 oficio.py forjar armadura MATERIAL CATEGORIA ... talhe=miúdo     (etapa 4b) a armadura do corpo miúdo (o pequenino, o gnomo): a mesma matéria, o mesmo teste
                                                          (ou para=ID: a armadura sai no corpo dessa pessoa, miúda ou de gente)
  python3 oficio.py continua [OBRA] [blocos=N]            mais N blocos na obra aberta (sem N: até fechar, ou até o corpo parar)
  python3 oficio.py larga OBRA                            abandona a obra (a matéria que já foi ao fogo se perde; o núcleo fica)
  python3 oficio.py consertar ITEM [pontos=N] [pago]      devolve durabilidade: você na bancada, ou `pago` à oficina do lugar
  python3 oficio.py ajustar ITEM [para=ID] [blocos=N]     sob medida para alguém que está aqui (sem para: para você)
  python3 oficio.py jornal N [oficio=forja|couro|alquimia|encanto|fé]    N blocos de bancada a serviço do lugar (a oficina, a botica, a mesa de runas ou o santuário;
                                                          ele paga o seu salário por bloco, até a jornada:
                                                          2 blocos pagos por dia, contados junto com o `ato.py trabalhar`; depois disso a bancada é sua, sem paga)
  python3 oficio.py pede ferramenta forja|couro CATEGORIA · forjar ferramenta forja|couro CATEGORIA ["Nome"]     (a etapa dos efeitos) a FERRAMENTA do ofício: o jogo de forja
                                                          (2 de metal e 1 de madeira) ou o de couro (1 de metal e 1 de couro); quem a tem soma no teste do ofício, fora do teto
                                                          do preparo: Comum +1 ... Lendária +6 na obra da categoria dela ou abaixo, +1 na de uma acima; e os poderes (REGRAS 7.14)
  python3 oficio.py efeito ITEM CHAVE [valor=N]           a OBRA-PRIMA (a peça que passa por 10, 20, 30 ganha 1, 2, 3 efeitos, até o teto da categoria): escolhe um efeito dela
  python3 oficio.py preparo receita|ajudante|fogo|bigorna CATEGORIA|nada "como foi ganho" [oficio=alquimia|encanto]     o Mestre registra um preparo ganho no mundo
                                                          (a alquimia: receita, ajudante, fogo, vidraria; o encanto: receita, ajudante, tinta, pedra)
  python3 oficio.py oficina NIVEL|nada "como foi"         o Mestre registra a oficina do lugar onde a pessoa está (0 a 4; nada: o lugar fica sem)
FAMILIA: adaga espada maça machado martelo lança montante alabarda malho arco besta · MATERIAL: couro malha placa · e a gazua (sem família): forjar gazua CATEGORIA
CATEGORIA: Comum Incomum Raro Épico Único Lendário
"""
import math, sys
import tabelas as T
import tabelas_mundo as M
import tabelas_oficio as O
import estado, ato, corpo, teste, talento
from itens import item, cat_i, rotulo, tem as item_tem, EFEITOS, ESCOLHE_NAO

PECAS = ('arma', 'armadura', 'escudo')
FORJA = PECAS + O.PECAS_ENCANTO + O.PECAS_LADINO + O.PECAS_FERRAMENTA      # o que se forja (o foco e o amuleto, no ofício do encanto; a gazua e a ferramenta, na oficina)
SEM_FAMILIA = ('escudo', 'amuleto', 'gazua')                # o que se forja sem família, forma nem material: só a categoria
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
def _vivo(E, pid): return estado.presente(E, pid, 'trabalhar na bancada')        # vivo e no lugar onde mora: quem saiu para o ermo não forja nem conserta


def oficina(E, lid):
    """o nível da oficina do lugar (0 a 4), ou None se o lugar não tem oficina"""
    v = E['lugares'][lid].get('oficina')
    if v is None or v is False or not isinstance(v, (int, float)): return None
    return max(0, min(len(O.OFICINAS) - 1, int(v)))


def nome_oficina(v): return f'{O.OFICINAS[v]} (+{v})'


def banca(E, lid, oficio='forja'):
    """o nível da bancada do ofício no lugar (0 a 4): a oficina (forja, couro), a mesa de runas (encanto), a botica (alquimia), o santuário (fé); None se o lugar não a tem"""
    if O.BANCA.get(oficio, 'oficina') == 'oficina': return oficina(E, lid)
    v = E['lugares'][lid].get(O.BANCA[oficio])
    return None if not isinstance(v, int) or isinstance(v, bool) else max(0, min(M.BANCADA_MAX, v))


def nomes_banca(oficio):
    import tabelas_magia_mundo as W
    return dict(encanto=W.RUNAS, alquimia=W.BOTICAS, fé=['altar', 'capela', 'santuário', 'templo', 'grande templo']).get(oficio, O.OFICINAS)
def nome_banca(oficio, v): return f'{nomes_banca(oficio)[v]} (+{v})'
def evento_de(oficio, tipo='forjar'): return O.EVENTO_OFICIO.get(oficio, tipo if tipo in ('forjar', 'ajustar') else 'forjar')        # o tipo de evento do trabalho na bancada deste ofício
def _sem_banca(E, lid, oficio):
    nome = dict(encanto='mesa de runas', alquimia='botica', fé='santuário').get(oficio, 'oficina')
    return f"{E['lugares'][lid]['nome']} não tem {nome}"
def _fam(x): return x.get('forma') if x.get('tipo') == 'foco' else O.chave_ferramenta(x.get('forma') or 'jogo', x.get('oficio')) if x.get('tipo') == 'ferramenta' else x.get('familia')        # o foco leva a forma, e a ferramenta a forma ou o ofício do jogo, onde a arma leva a família
def mao(p, oficio='forja'): m = p.get('maestria'); return m.get(oficio, 0) if isinstance(m, dict) else 0             # a maestria no ofício (0 a 8)
def bancada(p, oficio='forja'): t = p.get('treino'); return t.get(oficio, 0) if isinstance(t, dict) else 0         # os blocos de bancada já feitos


def tabela_preparos(oficio='forja'):
    """os quatro preparos do ofício: a forja e o couro (receita, ajudante, fogo, bigorna); a alquimia (receita, ajudante, fogo, vidraria); o encanto (receita, ajudante, tinta, pedra)"""
    import tabelas_magia_mundo as W
    return dict(alquimia=W.PREPAROS_ALQUIMIA, encanto=W.PREPAROS_ENCANTO).get(oficio, O.PREPAROS)


def preparos(E, pid, lid=None, oficio='forja'):
    """{os quatro preparos do ofício: o índice da categoria que ele alcança, ou None se não há}"""
    p = E['gente'][pid]; l = E['lugares'][lid or p['lugar']]; out = {}; do_lugar = l.get('preparo') if isinstance(l.get('preparo'), dict) else {}
    for nome, (de, chave) in tabela_preparos(oficio).items():
        v = p.get('marca', {}).get(chave) if de == 'pessoa' else do_lugar.get(chave)
        out[nome] = int(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else None
    return out


def preparo(E, pid, cat, lid=None, oficio='forja'):
    """o preparo que vale numa obra de categoria `cat`: +2 por preparo que a alcança, até +8"""
    return min(O.PREPARO_MAX, O.PREPARO_CADA * sum(1 for v in preparos(E, pid, lid, oficio).values() if v is not None and v >= cat))


def ferramentas(E, pid, oficio='forja'):
    """(a Lei do Valor) as ferramentas deste ofício que a pessoa tem, inteiras: a melhor no lugar do MARTELO DE FORJA e a melhor no lugar da TENAZ (o jogo, da parte 1,
    serve nos dois lugares). Devolve {martelo: (id, item) | None, tenaz: (id, item) | None}"""
    out = dict(martelo=None, tenaz=None)
    if oficio not in O.FERRAMENTA_OFICIOS: return out
    boas = [(k, it) for k, it in E['itens']['itens'].items() if it.get('tipo') == 'ferramenta' and it.get('oficio') == oficio and it.get('dono') == pid and it['dur'][0] > 0]
    chave = lambda x: (x[1]['cat'], bool(item_tem(x[1], 'afinada')), x[0])
    for lugar in ('martelo', 'tenaz'):
        cabem = [x for x in boas if (x[1].get('forma') or 'jogo') in (lugar, 'jogo')]
        if cabem: out[lugar] = max(cabem, key=chave)
    return out


def valor_ferramentas(E, pid, oficio='forja'):
    """o que as ferramentas somam (a Lei do Valor): o martelo de forja e a tenaz, cada um pela categoria dele, e a afinada (obra-prima) mais VALOR_AFINADA uma vez.
    Devolve (martelo, tenaz, a maior categoria entre as duas ou None)"""
    f = ferramentas(E, pid, oficio); vm = vt = 0; cats = []
    if f['martelo']: it = f['martelo'][1]; vm = O.VALOR_MARTELO[min(it['cat'], len(O.VALOR_MARTELO) - 1)]; cats.append(it['cat'])
    if f['tenaz']: it = f['tenaz'][1]; vt = O.VALOR_TENAZ[min(it['cat'], len(O.VALOR_TENAZ) - 1)]; cats.append(it['cat'])
    if any(x and item_tem(x[1], 'afinada') for x in f.values()): vm += O.VALOR_AFINADA
    return vm, vt, (max(cats) if cats else None)


def conta(E, pid, cat, oficio='forja', lid=None, contra=None):
    """a conta do teste desta pessoa, hoje, numa obra desta categoria: o que soma, contra quanto, e as três chances"""
    p = E['gente'][pid]; lid = lid or p['lugar']; v = banca(E, lid, oficio) or 0; prep = preparo(E, pid, cat, lid, oficio)
    # O DOM da bancada (etapa da magia) é um preparo que nasce com a pessoa: preparo e dom juntos não passam de +8. O dom que a pessoa ainda não viu não entra na conta
    # que vai à mesa: vai escondido no dado (c['oculto'], o dom= do teste.rola)
    c = dict(maestria=mao(p, oficio), afinidade=p['atributos']['Afinidade'] // 10, oficina=v, preparo=min(O.PREPARO_MAX, prep + talento.dom_visto(p, oficio)), pena=corpo.pena(p, estado.agora(E)), contra=O.contra(cat) if contra is None else contra)
    c['oculto'] = min(O.PREPARO_MAX, prep + talento.dom(p, oficio)) - c['preparo']
    vm, vt, fc = valor_ferramentas(E, pid, oficio); c['ferramenta'] = vm + vt; c['ferramenta_cat'] = fc       # o martelo de forja e a tenaz somam também no teste de passar (o ajuste)
    c['mais'] = c['maestria'] + c['oficina'] + c['preparo'] + c['ferramenta']      # o que entra como "mais" no teste.rola (a Afinidade e a pena, ele mesmo soma)
    c['soma'] = c['mais'] + c['afinidade'] + c['pena']
    c['acerta'], c['pouco'], c['perde'] = chances(c['soma'], c['contra'])
    return c


# ---------- A LEI DO VALOR (a forja e o couro: a soma decide a categoria) ----------
def _um_d20x(prof=4):
    """a distribuição de UM d20 que rola de novo no 20 e soma (cortada em `prof` voltas: o resto da massa fica no último 20)"""
    d = {}
    def rec(acc, p, k):
        for x in range(1, 21):
            q = p / 20
            if x == 20 and k < prof: rec(acc + 20, q, k + 1)
            else: d[acc + x] = d.get(acc + x, 0) + q
    rec(0, 1.0, 0); return d
_UM = _um_d20x()


def _resolve(total, a0, b0, teto, fc):
    """o que sai de uma obra pela Lei do Valor, dado o total e as duas faces de partida (a0, b0): uma lista de (chance, saída), em que a saída é
    {cat: a categoria ou None (perde), tosca, d6: a face do 1d6 que decide (ou None), como: o que houve}. fc: a maior categoria das ferramentas (ou -1).
    Os dados: os dois em 1, perde; um em 1, complicação (1d6: 1 perde, 2-3 cai uma, 4-6 a peça nasce gasta); os dois em 20, OBRA-PRIMA (1d6: 1-3 sobe uma se o teto deixa,
    senão +1 efeito; 4-6, +1 efeito). O poder das ferramentas: a Rara segura a matéria até 5 abaixo da CD do Comum (sai Comum, tosca); a Épica nunca a perde."""
    k = O.cat_do_total(total, teto); quase_janela = O.VALOR_QUASE * (2 if fc >= O.OBRA_PRIMA_FACIL else 1)
    def seguro(x, como):
        """o poder das ferramentas sobre a matéria perdida"""
        if x['cat'] is not None: return x
        if fc >= O.NADA_SE_PERDE or (fc >= 2 and 'dados' not in como and total >= O.VALOR_CD[0] - 5): return dict(x, cat=0, tosca=True, como=como + '; a ferramenta segura a matéria: sai Comum, tosca')
        return x
    base = dict(cat=k, tosca=False, d6=None, gasta=False, sobe=False, mais_efeito=0,
                quase=k is not None and k < teto and k + 1 < len(O.VALOR_CD) and total >= O.VALOR_CD[k + 1] - quase_janela)
    if a0 == 1 and b0 == 1: return [(1.0, seguro(dict(base, cat=None, quase=False), 'os dois dados em 1 (dados): a peça se perde'))]
    if a0 == 1 or b0 == 1:
        L = []
        for f in range(1, 7):
            if f == 1: x = seguro(dict(base, cat=None, quase=False, d6=f), 'complicação, 1d6 = 1 (dados): a peça se perde')
            elif f <= 3: x = seguro(dict(base, cat=None if k is None else (k - 1 if k > 0 else 0), tosca=k == 0, d6=f), f'complicação, 1d6 = {f}: cai uma categoria')
            else: x = dict(base, d6=f, gasta=k is not None, como=f'complicação, 1d6 = {f}: a peça nasce gasta')
            x.setdefault('como', ''); L.append((1 / 6, x))
        return L
    if a0 == 20 and b0 == 20 and k is not None:
        L = []
        for f in range(1, 7):
            if f <= 3 and k < teto: x = dict(base, cat=k + 1, sobe=True, d6=f, como=f'OBRA-PRIMA, 1d6 = {f}: a peça sobe uma categoria')
            else: x = dict(base, d6=f, mais_efeito=1, como=f'OBRA-PRIMA, 1d6 = {f}: +1 efeito')
            L.append((1 / 6, x))
        return L
    return [(1.0, seguro(dict(base, como=''), ''))]


def dist_valor(soma, teto, fc=-1):
    """a chance de cada categoria (e de perder: None) pela Lei do Valor, para quem soma `soma` ao 2d20 explosivo, com o teto e os dados especiais"""
    res = {}
    for a0 in range(1, 21):
        da = {a0: 1.0} if a0 < 20 else {20 + x: q for x, q in _UM.items()}
        for b0 in range(1, 21):
            db = {b0: 1.0} if b0 < 20 else {20 + x: q for x, q in _UM.items()}
            for va, pa in da.items():
                for vb, pb in db.items():
                    p = pa * pb / 400
                    for q, x in _resolve(va + vb + soma, a0, b0, teto, fc): res[x['cat']] = res.get(x['cat'], 0) + p * q
    return res


def valor(E, pid, cat, oficio='forja', lid=None):
    """a conta da LEI DO VALOR desta pessoa, hoje, numa obra cuja matéria (ou núcleo) é da categoria `cat`: o que soma, o teto, e a chance de cada categoria"""
    p = E['gente'][pid]; lid = lid or p['lugar']; v = banca(E, lid, oficio) or 0; prep = preparo(E, pid, cat, lid, oficio); vm, vt, fc = valor_ferramentas(E, pid, oficio)
    c = dict(maestria=mao(p, oficio), afinidade=p['atributos']['Afinidade'] // 10, oficina=v, preparo=min(O.PREPARO_MAX, prep + talento.dom_visto(p, oficio)),
             materia=O.VALOR_MATERIA[min(cat, M.MATERIA_ATE)], nucleo=O.VALOR_NUCLEO.get(cat, 0), martelo=vm, tenaz=vt, ferramenta_cat=fc,
             pena=corpo.pena(p, estado.agora(E)), teto=O.teto(cat), cat=cat, contra=O.VALOR_CD[min(cat, len(O.VALOR_CD) - 1)])
    c['oculto'] = min(O.PREPARO_MAX, prep + talento.dom(p, oficio)) - c['preparo']
    c['mais'] = c['maestria'] + c['oficina'] + c['preparo'] + c['materia'] + c['nucleo'] + c['martelo'] + c['tenaz']
    c['soma'] = c['mais'] + c['afinidade'] + c['pena']; c['ferramenta'] = vm + vt
    c['chances'] = dist_valor(c['soma'], c['teto'], -1 if fc is None else fc)
    return c


def diz_valor(c):
    """a conta da Lei do Valor em uma linha, e a chance de cada categoria"""
    partes = (f"maestria {c['maestria']} + Afinidade {c['afinidade']} + matéria {c['materia']}" + (f" + núcleo {c['nucleo']}" if c['nucleo'] else '')
              + (f" + martelo de forja {c['martelo']}" if c['martelo'] else '') + (f" + tenaz {c['tenaz']}" if c['tenaz'] else '') + f" + oficina {c['oficina']} + preparo {c['preparo']}"
              + (f" − {-c['pena']} do corpo" if c['pena'] else ''))
    ch = c['chances']; cats = [k for k in range(c['teto'] + 1) if ch.get(k, 0) >= 0.0005]
    tab = ' · '.join(f"{T.CATS[k]} {ch.get(k, 0):.0%}" for k in cats) + f" · perde {ch.get(None, 0):.0%}"
    cds = ' · '.join(f"{T.CATS[k]} {O.VALOR_CD[k]}" for k in range(min(c['teto'], len(O.VALOR_CD) - 1) + 1))
    return f"2d20 + {c['soma']} ({partes}) · a peça sai na maior categoria que o total alcança ({cds}; o teto desta obra: {T.CATS[c['teto']]}): {tab}"


def diz_conta(c, pouco='sai uma abaixo', perde='perde tudo', banca='oficina'):
    partes = f"maestria {c['maestria']} + Afinidade {c['afinidade']} + {banca} {c['oficina']} + preparo {c['preparo']}" + (f" + ferramenta {c['ferramenta']}" if c.get('ferramenta') else '') + (f" − {-c['pena']} do corpo" if c['pena'] else '')
    return f"2d20 + {c['soma']} ({partes}) contra {c['contra']}: acerta {c['acerta']:.0%} · {pouco} {c['pouco']:.0%} · {perde} {c['perde']:.0%}"


def _em(E, lid): l = E['lugares'][lid]; return l.get('em', 'em ' + l['nome'])
def _peca(x): return rotulo(x)                                                 # "Adaga da Cira (Comum)"; "espada Rara" (o nome que já diz a categoria não a repete)
tantos = estado.tantos
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
def molde(tipo, cat, nome=None, familia=None, material=None, cobre=None, forma=None, talhe=None, oficio=None):
    """o que se vai forjar, conferido ANTES de qualquer coisa mudar: {tipo, cat, nome, familia | material e cobre (e o talhe da armadura miúda) | forma (o foco)}"""
    if tipo not in FORJA: sys.exit(f'não se forja "{tipo}" (forja-se: {", ".join(FORJA)})')
    c = cat_i(cat)
    if c > O.FORJA_ATE: sys.exit(f'ninguém forja acima do {T.CATS[O.FORJA_ATE]} (veio {T.CATS[c]})')
    if tipo == 'arma' and familia not in O.MATERIA_ARMA: sys.exit(f'não se forja a arma "{familia}" (forja-se: {", ".join(O.MATERIA_ARMA)})')
    if tipo == 'foco' and forma not in M.MATERIA_FOCO: sys.exit(f'não se faz o foco "{forma}" (faz-se: {", ".join(M.MATERIA_FOCO)})')
    if talhe not in O.TALHES + ('gente',): sys.exit(f'talhe desconhecido: "{talhe}" (a armadura é de gente, ou miúda: talhe=miúdo)')
    if talhe == 'miúdo' and tipo != 'armadura': sys.exit('só a armadura se forja para o corpo miúdo (a arma, o escudo e a gazua servem em todo corpo)')
    if tipo == 'ferramenta':                                # (a etapa dos efeitos, parte 1) a ferramenta do ofício: o jogo de forja ou o jogo de couro
        if oficio in ('martelo', 'tenaz'): forma, of = oficio, 'forja'
        elif oficio in O.FERRAMENTA_OFICIOS: forma, of = 'jogo', oficio
        else: sys.exit(f'a ferramenta: forjar ferramenta martelo|tenaz CATEGORIA (o martelo de forja, a tenaz) ou ferramenta forja|couro CATEGORIA (o jogo, os dois de uma vez) (veio "{oficio}")')
        it = item('ferramenta', c, nome, oficio=of, forma=forma); return dict(tipo='ferramenta', cat=c, nome=it['nome'], oficio=of, forma=forma)
    it = item(tipo, c, nome, **({'forma': forma} if tipo == 'foco' else {} if tipo in ('amuleto', 'gazua') else dict(familia=familia, material=material, cobre=cobre, talhe=None if talhe == 'gente' else talhe)))        # confere o material e as partes, e dá o nome padrão
    d = dict(tipo=tipo, cat=c, nome=it['nome'])
    if tipo == 'foco': d['forma'] = forma
    if tipo == 'arma': d['familia'] = familia
    if tipo == 'armadura':
        d['material'] = material; d['cobre'] = it['cobre']
        if it.get('talhe'): d['talhe'] = it['talhe']            # a armadura miúda (etapa 4b): a peça nasce com o talhe
    return d


def _materia_conserto(it):
    """a chave da matéria que o conserto desta peça gasta, ou None se a tabela não sabe de que ela é feita"""
    try: return O.materia_conserto(it['tipo'], it['cat'], _fam(it), it.get('material'), it.get('cobre'))
    except KeyError: return None
def oficio_de(x): return O.oficio_da(x['tipo'], x.get('material'))
def materia_de(x, cat=None): return O.materia(x['tipo'], x['cat'] if cat is None else cat, _fam(x), x.get('material'), x.get('cobre'))


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
    p = _vivo(E, pid); cat = peca['cat']; of = oficio_de(peca); v = banca(E, p['lugar'], of); mat = materia_de(peca); carga = p.get('carga', {})
    L = [f"{_peca(peca)} · ofício: {of} · {tantos(O.blocos(cat), 'bloco pesado', 'blocos pesados')} de bancada",
         'Matéria: ' + ', '.join(f"{n} de {_mat(k)} (você tem {carga.get(k, 0)})" for k, n in mat.items())
         + (f' · e um núcleo {T.CATS[cat]}' if O.pede_nucleo(cat) else '')]
    if v is None: L.append(_sem_banca(E, p['lugar'], of) + ': a obra não abre.')
    elif of in O.VALOR_OFICIOS: L.append('A soma, hoje e aqui (a Lei do Valor): ' + diz_valor(valor(E, pid, cat, of)))
    else: L.append('O teste final, hoje e aqui: ' + diz_conta(conta(E, pid, cat, of), pouco='sai uma abaixo' if cat else 'sai tosca', banca='runas' if of == 'encanto' else 'oficina'))
    if mao(p, of) < O.MAO_DA_OBRA[cat]:
        L.append(f"AVISO: a obra {FEM[cat]} pede mão de {T.MAESTRIAS[O.MAO_DA_OBRA[cat]]}; a sua é de {T.MAESTRIAS[mao(p, of)]}. Pode tentar; o que entra na obra não volta.")
    return '\n'.join(L)


# ---------- a maestria ----------
def sobe(E, pid, oficio='forja'):
    """a maestria do ofício sobe quando os blocos de bancada chegam; de Mestre para cima, só com o FEITO (marca.feito_OFICIO)"""
    p = E['gente'][pid]; tem = mao(p, oficio); bl = bancada(p, oficio); txt = ''
    for grau in sorted(O.OFICIO_BLOCOS):
        quer = talento.pede(p, oficio, O.OFICIO_BLOCOS, grau)             # os blocos vezes o talento (etapa da magia), até o teto dele
        if grau <= tem: continue
        if quer is None:
            if bl >= O.OFICIO_BLOCOS[grau]: txt = f" (a mão não sobe mais em {oficio}: o talento para em {T.MAESTRIAS[talento.teto(p, oficio)]})"
            break
        if bl < quer: continue
        if grau in O.FEITO_OBRA and p.get('marca', {}).get(f'feito_{oficio}', 0) < grau:
            txt = f" (tem os blocos para {T.MAESTRIAS[grau]} em {oficio}; falta o feito: uma obra {FEM[O.FEITO_OBRA[grau]]}, ou melhor, nascida da sua mão)"; break
        estado.aplica(E, 'treinar', [['pessoa', pid, 'maestria.' + oficio, 'poe', grau]], onde=p['lugar'], quem=[pid], texto=f"{p['nome']} chega a {T.MAESTRIAS[grau]} em {oficio}")
        p = E['gente'][pid]; tem = grau; txt = f'. MAESTRIA: {T.MAESTRIAS[grau]} em {oficio}'
    return txt


# ---------- forjar ----------
def forjar(E, pid, peca, blocos=None, nucleo=None):
    """abre a obra (a matéria sai da carga e entra nela) e trabalha `blocos` blocos (None: até fechar, ou até o corpo parar; 0: só abre)"""
    p = _vivo(E, pid); lid = p['lugar']; cat = peca['cat']; of = oficio_de(peca)
    if banca(E, lid, of) is None: sys.exit(_sem_banca(E, lid, of) + ': a obra não abre')
    mat = materia_de(peca); carga = p.get('carga', {}); falta = {k: n - carga.get(k, 0) for k, n in mat.items() if carga.get(k, 0) < n}
    if falta: sys.exit(f"falta matéria para {_peca(peca)}: {_lista(falta)} (a obra pede {_lista(mat)})")
    nid = _nucleo(E, pid, cat, nucleo) if O.pede_nucleo(cat) else None
    if nucleo and not nid: sys.exit(f'uma obra {FEM[cat]} não leva núcleo (só do {T.CATS[M.MATERIA_ATE + 1]} para cima)')
    reg = dict(quem=pid, lugar=lid, tipo='forjar', oficio=of, peca=dict(peca), cat=cat, blocos=0, pede=O.blocos(cat), materia=mat, nucleo=nid)
    ef = [['pessoa', pid, 'carga.' + k, 'soma', -n] for k, n in mat.items()] + [['obra', 'abre', reg]]
    if nid: ef.append(['item', nid, 'historia', 'junta', f"Dia {E['relogio']['dia']}: entrou na obra de {peca['nome']}"])
    estado.aplica(E, evento_de(of), ef, onde=lid, quem=[pid], texto=f"{p['nome']} abre a obra: {_peca(peca)}; entram {_lista(mat)}" + (f" e {E['itens']['itens'][nid]['nome']}" if nid else ''))
    oid = f"o{E['itens']['oseq']:04d}"
    R = continua(E, pid, oid, blocos)
    R['texto'] = f"Obra {oid} aberta: {_peca(peca)}. Entraram {_lista(mat)}" + (f" e o núcleo {nid}" if nid else '') + '.\n' + R['texto']
    return R


def _obra(E, pid, oid=None):
    minhas = obras_de(E, pid)
    if oid:
        if oid not in minhas: sys.exit(f'não há a obra "{oid}" aberta em nome de {E["gente"][pid]["nome"]}' + (f' (abertas: {", ".join(minhas)})' if minhas else ''))
        return minhas[oid]
    if len(minhas) == 1: return next(iter(minhas.values()))
    sys.exit('não há obra aberta.' if not minhas else f'há mais de uma obra aberta: diga qual ({", ".join(minhas)})')


def _nome_obra(E, o):
    if o['tipo'] == 'forjar': return _peca(o['peca'])
    if o['tipo'] in ('leva', 'gravar'): return o.get('nome') or o['tipo']                   # a leva e a gravação guardam o nome delas ao abrir
    it = E['itens']['itens'].get(o['item']); return f"o ajuste de {it['nome'] if it else o['item']}"


def continua(E, pid, oid=None, blocos=None):
    """trabalha na obra aberta. Para quando os blocos fecham (e aí sai o teste), quando acabam os blocos pedidos, ou quando o corpo cruza um limiar."""
    p = _vivo(E, pid); o = _obra(E, pid, oid); oid = o['id']; of = o['oficio']
    if p['lugar'] != o['lugar']: sys.exit(f"a obra {oid} está {_em(E, o['lugar'])}: é lá que se trabalha nela")
    if banca(E, o['lugar'], of) is None: sys.exit(_sem_banca(E, o['lugar'], of) + f": a obra {oid} não anda")
    if o.get('nucleo') and E['itens']['itens'].get(o['nucleo'], {}).get('dono') != pid: sys.exit(f"o núcleo da obra {oid} não está mais na mão de quem forja: a obra não anda (largue-a com `larga`)")
    if o['tipo'] in ('ajustar', 'gravar') and _ajuste_solto(E, o): sys.exit(f"{_ajuste_solto(E, o)}: a obra {oid} não anda (largue-a com `larga`)")       # a gravação, como o ajuste, trabalha na peça de alguém que está ali
    falta = max(0, o['pede'] - o['blocos']); n = falta if blocos is None else max(0, min(int(blocos), falta)); nome = _nome_obra(E, o)
    feitos, pq = ato.passa(E, pid, n, evento_de(of, o['tipo']), esforco='pesado', texto=f"{p['nome']} trabalha na obra: {nome}",
                           mais=lambda i: [['obra', oid, 'blocos', 'soma', 1], ['pessoa', pid, 'treino.' + of, 'soma', 1]])
    o = E['itens']['obras'][oid]; p = E['gente'][pid]
    R = dict(obra=oid, feitos=feitos, parou=pq, fim=None, item=None, rolagem=None)
    R['texto'] = f"{p['nome']} trabalha {tantos(feitos, 'bloco')} na obra {oid}, {nome}: {o['blocos']} de {o['pede']}" + (sobe(E, pid, of) if feitos else '') + (f'. PAROU: {pq}' if pq else '')
    if o['blocos'] >= o['pede'] and E['gente'][pid]['estado'] == 'vivo':
        F = remata(E, oid); R.update(fim=F['fim'], item=F['item'], rolagem=F['rolagem'], cat=o['cat'], sai=F.get('sai')); R['texto'] += '\n' + F['texto']
    return R


def remata(E, oid):
    """os blocos fecharam: sai o teste final (dado de verdade, uma vez) e a obra fecha"""
    o = E['itens'].get('obras', {}).get(oid) or sys.exit(f'não há a obra "{oid}"')
    if o['blocos'] < o['pede']: sys.exit(f"a obra {oid} tem {o['blocos']} de {o['pede']} blocos: o teste só sai quando os blocos fecham")
    _vivo(E, o['quem'])
    if o['tipo'] == 'leva': import alquimia; return alquimia.remata(E, o)          # a leva da alquimia e a gravação do encanto: quem remata é o módulo delas
    if o['tipo'] == 'gravar': import encanto; return encanto.remata(E, o)
    return _remata_forja(E, o) if o['tipo'] == 'forjar' else _remata_ajuste(E, o)


def _remata_valor(E, o):
    """(a LEI DO VALOR) os blocos fecharam: sai o teste (2d20 explosivos, uma vez, e o 1d6 dos dados especiais quando eles pedem), e a soma decide a categoria da peça"""
    import secrets
    oid = o['id']; pid = o['quem']; p = E['gente'][pid]; cat = o['cat']; peca = o['peca']; lid = o['lugar']; of = o['oficio']; nid = o.get('nucleo'); L = E['itens']['itens']
    if nid and nid not in L: sys.exit(f'o núcleo da obra {oid} não está mais no Livro de Itens: a obra não fecha (largue-a com `larga`)')
    c = valor(E, pid, cat, of, lid); nuc = L[nid]['nome'] if nid else None; dia = E['relogio']['dia']; fam = _fam(peca); fc = -1 if c['ferramenta_cat'] is None else c['ferramenta_cat']
    r = teste.rola(E, f"forjar {_peca(peca)}", 'Afinidade', c['contra'], mais=c['mais'], quem=pid, **({'dom': c['oculto']} if c['oculto'] else {}))
    a0, b0 = r['dados'][0][0], r['dados'][1][0]
    if r.get('posto_a_mao'): a0 = b0 = 10                    # o dado posto à mão (só na prova): sem dado especial
    saidas = _resolve(r['total'], a0, b0, c['teto'], fc); d6 = None
    if len(saidas) > 1: d6 = secrets.randbelow(6) + 1; x = next(x for _, x in saidas if x['d6'] == d6)
    else: x = saidas[0][1]
    sai = x['cat']; ef = []; it = None
    n20 = 0 if r.get('posto_a_mao') else sum(1 for d in r['dados'] for f in d if f == 20)
    efeitos = n20 + x['mais_efeito'] + (1 if x['quase'] else 0)
    fim = 'perdeu' if sai is None else 'acertou' if sai >= cat else 'abaixo'
    if sai is not None:
        padrao = molde(peca['tipo'], cat, familia=peca.get('familia'), material=peca.get('material'), cobre=peca.get('cobre'), forma=peca.get('forma') if peca['tipo'] == 'foco' else None, talhe=peca.get('talhe'), oficio=(peca.get('forma') if peca.get('forma') in ('martelo', 'tenaz') else peca.get('oficio')) if peca['tipo'] == 'ferramenta' else None)['nome']
        nome = None if sai != cat and peca['nome'] == padrao else peca['nome']           # a peça sem nome próprio ganha o nome da categoria em que nasceu
        forma = {'oficio': peca.get('oficio'), 'forma': peca.get('forma') or 'jogo'} if peca['tipo'] == 'ferramenta' else {} if peca['tipo'] in ('amuleto', 'gazua') else dict(familia=peca.get('familia'), material=peca.get('material'), cobre=peca.get('cobre'), **({'talhe': peca['talhe']} if peca.get('talhe') else {}))
        it = item(peca['tipo'], sai, nome, dono=pid, feito_por=pid, dia=dia, **forma)
        como = f"Dia {dia}: {p['nome']} forjou {_em(E, lid)}" + (f', com {nuc}' if nuc else '') + f" (a soma: {teste.total_visto(r)}; a obra era de matéria {FEM[min(cat, M.MATERIA_ATE)]}" + (f" e núcleo {T.CATS[cat]}" if cat > M.MATERIA_ATE else '') + ')'
        if x['tosca']: it['dur'][0] = max(1, int(it['dur'][1] * O.TOSCA)); como += '; a peça saiu tosca'
        elif x['gasta']: it['dur'][0] = max(1, int(it['dur'][1] * O.VALOR_COMPLICA_DUR)); como += '; a peça nasceu gasta'
        livres = min(O.EFEITOS_MAX[min(sai, len(O.EFEITOS_MAX) - 1)], efeitos)
        if livres: it['efeitos_livres'] = livres; como += f'; {livres} efeito{"s" if livres > 1 else ""} por escolher'
        if x['como']: como += f"; {x['como']}"
        if nid and L[nid].get('de'): it['nucleo_de'] = L[nid]['de']
        it['historia'].append(como); ef.append(['item', 'nasce', it])
        for grau, quer in sorted(O.FEITO_OBRA.items()):                     # o feito: uma obra nascida da categoria certa (ou melhor)
            if it['cat'] >= quer and p.get('marca', {}).get(f'feito_{of}', 0) < grau: ef.append(['pessoa', pid, f'marca.feito_{of}', 'poe', grau])
    if nid: ef.append(['item', nid, 'some'])
    ef.append(['obra', oid, 'fecha'])
    if talento.decidiu(r): ef += talento.mostra(E, pid)
    conta_txt = f"soma {teste.total_visto(r)}"
    if sai is None: txt = f"a obra de {_peca(peca)} se perde ({conta_txt}" + (f"; {x['como']}" if x['como'] else f", abaixo da CD do Comum, {O.VALOR_CD[0]}") + f"): some a matéria ({_lista(o['materia'])})" + (f' e some {nuc}' if nuc else '')
    else:
        txt = f"{p['nome']} forja {peca['nome'] if nome else _peca(it)}: {conta_txt}, a peça sai {FEM[sai]}" + (' (tosca)' if x['tosca'] else ' (gasta)' if x['gasta'] else '')
        txt += (f"; {x['como']}" if x['como'] else '') + (f"; {it['efeitos_livres']} efeito{'s' if it['efeitos_livres'] > 1 else ''} por escolher" if it.get('efeitos_livres') else '')
        if x['quase']: txt += f"; QUASE: a soma ficou a {O.VALOR_CD[sai + 1] - r['total']} da CD {FEM[sai + 1]}"
        if n20: txt += f"; {n20} dado{'s' if n20 > 1 else ''} em 20"
    estado.aplica(E, evento_de(of), ef, onde=lid, quem=[pid], texto=txt)
    iid = f"i{E['itens']['seq']:04d}" if it else None
    out = (teste.diz(E, r) + f"\n  (o +{c['mais']}: maestria {c['maestria']}, matéria {c['materia']}" + (f", núcleo {c['nucleo']}" if c['nucleo'] else '') + (f", martelo de forja {c['martelo']}" if c['martelo'] else '')
           + (f", tenaz {c['tenaz']}" if c['tenaz'] else '') + f", oficina {c['oficina']}, preparo {c['preparo']}) · as CDs: " + ' · '.join(f"{T.CATS[k]} {O.VALOR_CD[k]}" for k in range(min(c['teto'], len(O.VALOR_CD) - 1) + 1))
           + f" (o teto: {T.CATS[c['teto']]})" + (f" · o 1d6 dos dados: {d6}" if d6 else '') + '\n' + txt + (f'. Entrou no Livro de Itens: {iid}' if iid else '') + _diz_dom(E, pid, r) + sobe(E, pid, of))
    return dict(obra=oid, fim=fim, item=iid, rolagem=r, texto=out, sai=sai, cat=cat)


def _remata_forja(E, o):
    if o.get('oficio') in O.VALOR_OFICIOS: return _remata_valor(E, o)       # a forja e o couro: a Lei do Valor (o encanto segue com a categoria escolhida)
    oid = o['id']; pid = o['quem']; p = E['gente'][pid]; cat = o['cat']; peca = o['peca']; lid = o['lugar']; of = o['oficio']; nid = o.get('nucleo'); L = E['itens']['itens']
    if nid and nid not in L: sys.exit(f'o núcleo da obra {oid} não está mais no Livro de Itens: a obra não fecha (largue-a com `larga`)')
    c = conta(E, pid, cat, of, lid); nuc = L[nid]['nome'] if nid else None; dia = E['relogio']['dia']; fam = _fam(peca)
    r = teste.rola(E, f"forjar {_peca(peca)}", 'Afinidade', c['contra'], mais=c['mais'], quem=pid, **({'dom': c['oculto']} if c['oculto'] else {}))
    margem = r['total'] - r['contra']; fc = c.get('ferramenta_cat'); fc = -1 if fc is None else fc        # o poder da ferramenta que a pessoa tem (a categoria dela)
    por_pouco = O.POR_POUCO_RARA if fc >= 2 else O.POR_POUCO
    sai = cat if margem >= 0 else cat - 1 if (margem > -por_pouco or fc >= O.NADA_SE_PERDE) else None; ef = []; it = None
    acima = margem >= O.ACIMA_MARGEM and fc >= O.ACIMA_DO_FERRO and cat < O.FORJA_ATE      # a ferramenta Lendária: a peça que passa muito nasce uma categoria acima
    if acima: sai = cat + 1
    _faixa_do_dom(r, c, margem)
    fim = 'acertou' if margem >= 0 else 'abaixo' if sai is not None else 'perdeu'
    if sai is not None:
        padrao = molde(peca['tipo'], cat, familia=peca.get('familia'), material=peca.get('material'), cobre=peca.get('cobre'), forma=peca.get('forma') if peca['tipo'] == 'foco' else None, talhe=peca.get('talhe'), oficio=(peca.get('forma') if peca.get('forma') in ('martelo', 'tenaz') else peca.get('oficio')) if peca['tipo'] == 'ferramenta' else None)['nome']       # o nome que a obra ganha quando não se dá nome: diz a categoria DA OBRA
        nome = None if max(0, sai) != cat and peca['nome'] == padrao else peca['nome']      # a peça sem nome próprio que sai uma categoria abaixo ganha o nome da categoria em que saiu ("arco Incomum", e não "arco Raro")
        forma = {'forma': fam} if peca['tipo'] == 'foco' else {'oficio': peca.get('oficio'), 'forma': peca.get('forma') or 'jogo'} if peca['tipo'] == 'ferramenta' else {} if peca['tipo'] in ('amuleto', 'gazua') else dict(familia=peca.get('familia'), material=peca.get('material'), cobre=peca.get('cobre'), **({'talhe': peca['talhe']} if peca.get('talhe') else {}))
        it = item(peca['tipo'], max(0, sai), nome, dono=pid, feito_por=pid, dia=dia, **forma)
        como = f"Dia {dia}: {p['nome']} forjou {_em(E, lid)}" + (f', com {nuc}' if nuc else '')
        if sai < 0: it['dur'][0] = max(1, int(it['dur'][1] * O.TOSCA)); como += '; a peça saiu tosca'
        elif sai < cat: como += f'; a obra era {FEM[cat]} e a peça saiu {FEM[sai]}'
        elif acima: como += f'; a obra era {FEM[cat]} e a ferramenta Lendária a fez nascer {FEM[sai]}'
        livres = O.efeitos_da_obra(margem, it['cat'], facil=fc >= O.OBRA_PRIMA_FACIL) if margem >= 0 else 0
        if livres: it['efeitos_livres'] = livres; como += f'; OBRA-PRIMA: passou por {margem}, {livres} efeito{"s" if livres > 1 else ""} por escolher'
        if nid and L[nid].get('de'): it['nucleo_de'] = L[nid]['de']
        it['historia'].append(como); ef.append(['item', 'nasce', it])
        for grau, quer in sorted(O.FEITO_OBRA.items()):                     # o feito: uma obra nascida da categoria certa (ou melhor)
            if it['cat'] >= quer and p.get('marca', {}).get(f'feito_{of}', 0) < grau: ef.append(['pessoa', pid, f'marca.feito_{of}', 'poe', grau])
    if nid: ef.append(['item', nid, 'some'])
    ef.append(['obra', oid, 'fecha'])
    if talento.decidiu(r): ef += talento.mostra(E, pid)                    # o dom escondido fez a diferença: a pessoa vê que tem
    conta_txt = f"{teste.total_visto(r)} contra {r['contra']}"
    if fim == 'acertou': txt = f"{p['nome']} forja {_peca(peca)}: {conta_txt}" + (f"; a ferramenta Lendária a fez nascer {FEM[sai]}" if acima else '') + (f"; OBRA-PRIMA: {it['efeitos_livres']} efeito{'s' if it['efeitos_livres'] > 1 else ''} por escolher" if it and it.get('efeitos_livres') else '')
    elif fim == 'abaixo': txt = f"{p['nome']} erra por pouco ({conta_txt}): {peca['nome']} sai " + (f'{FEM[sai]}, uma categoria abaixo' if sai >= 0 else 'Comum e tosca') + (f'; {nuc} se gasta nela' if nuc else '')
    else: txt = f"a obra de {_peca(peca)} se perde ({conta_txt}): some a matéria ({_lista(o['materia'])})" + (f' e some {nuc}' if nuc else '')
    estado.aplica(E, evento_de(of), ef, onde=lid, quem=[pid], texto=txt)
    iid = f"i{E['itens']['seq']:04d}" if it else None
    out = teste.diz(E, r) + f"\n  (o +{c['mais']}: maestria {c['maestria']}, {'runas' if of == 'encanto' else 'oficina'} {c['oficina']}, preparo {c['preparo']}" + (f", ferramenta {c['ferramenta']}" if c.get('ferramenta') else '') + ")\n" + txt + (f'. Entrou no Livro de Itens: {iid}' if iid else '') + _diz_dom(E, pid, r) + sobe(E, pid, of)
    return dict(obra=oid, fim=fim, item=iid, rolagem=r, texto=out)


def _faixa_do_dom(r, c, margem):
    """o teste da bancada tem três faixas (acerta, sai uma abaixo, perde tudo): o dom escondido FEZ a diferença se mudou a faixa (r['fez'], que o teste.diz e o talento.decidiu leem)"""
    if not c.get('oculto'): return
    faixa = lambda m: 0 if m >= 0 else 1 if m > -O.POR_POUCO else 2
    sem = margem - c['oculto']
    r['fez'] = (True if margem >= 0 else 'faixa') if faixa(sem) != faixa(margem) else False


def _diz_poder(fc):
    """o poder das ferramentas pela maior categoria delas, em palavras (a Lei do Valor)"""
    P = []
    if fc >= 2: P.append('a matéria só se perde 5 abaixo da CD do Comum (a peça sai Comum, tosca)' if fc < O.NADA_SE_PERDE else 'a matéria nunca se perde (a peça sai, no pior, Comum e tosca)')
    if fc >= O.OBRA_PRIMA_FACIL: P.append(f'o QUASE vale a {2 * O.VALOR_QUASE} da CD seguinte')
    return (' · poder: ' + '; '.join(P)) if P else ''


def _diz_dom(E, pid, r):
    return f" Foi o dom que fez a diferença: há alguma coisa nas mãos de {E['gente'][pid]['nome']}." if talento.decidiu(r) else ''


def larga(E, pid, oid):
    """abandona a obra. A matéria que já foi ao fogo se perde (com zero blocos, volta à carga); o núcleo fica com o dono: só o teste o gasta."""
    p = _vivo(E, pid); o = _obra(E, pid, oid); ef = [['obra', o['id'], 'fecha']]; leva_materia = o['tipo'] in ('forjar', 'leva', 'gravar'); volta = leva_materia and o['blocos'] == 0
    if volta: ef += [['pessoa', pid, 'carga.' + k, 'soma', n] for k, n in o['materia'].items()]
    txt = f"{p['nome']} larga a obra: {_nome_obra(E, o)}" + ('' if not leva_materia else f" (a matéria volta: {_lista(o['materia'])})" if volta else f" (a matéria se perde: {_lista(o['materia'])})")
    estado.aplica(E, evento_de(o.get('oficio', 'forja'), o['tipo']), ef, onde=p['lugar'], quem=[pid], texto=txt)
    return dict(obra=o['id'], fim='largada', item=None, rolagem=None, texto=txt + '.')


# ---------- consertar ----------
def consertar(E, pid, iid, pontos=None, pago=False):
    """devolve durabilidade a uma peça da pessoa: ela mesma na bancada (blocos pesados e um pouco de matéria), ou paga à oficina do lugar (2% do preço por ponto)"""
    p = _vivo(E, pid); lid = p['lugar']; l = E['lugares'][lid]; it = E['itens']['itens'].get(iid) or sys.exit(f'não há o item "{iid}" no Livro de Itens')
    if it['tipo'] not in FORJA: sys.exit(f"{it['nome']} não é peça que se conserte")
    if it.get('dono') != pid: sys.exit(f"{it['nome']} não é de {p['nome']}")
    of = oficio_de(it); v = banca(E, lid, of); nb = nomes_banca(of)
    if v is None: sys.exit(_sem_banca(E, lid, of) + ': não se conserta aqui')
    gasto = it['dur'][1] - it['dur'][0]
    if gasto <= 0: sys.exit(f"{it['nome']} não precisa de conserto ({it['dur'][0]}/{it['dur'][1]})")
    q = gasto if pontos is None else min(int(pontos), gasto)
    if q < 1: sys.exit('diga quantos pontos consertar (1 ou mais)')
    cat = it['cat']; sobra = f" Pediu {pontos}; a peça só tinha {tantos(gasto, 'ponto gasto', 'pontos gastos')}." if pontos is not None and int(pontos) > gasto else ''
    if pago:
        if cat > v + O.OFICINA_CONSERTA: sys.exit(f"a {nb[v]} {estado.de(E, lid)} só conserta até o {T.CATS[min(v + O.OFICINA_CONSERTA, len(T.CATS) - 1)]}; {it['nome']} é {T.CATS[cat]}")
        custo = O.conserto_pago(cat, q, M.peso_do_item(it))
        if p['moedas'] < custo: sys.exit(f"consertar {tantos(q, 'ponto')} de {_peca(it)} custa {custo} de prata; {p['nome']} tem {p['moedas']}")
        estado.aplica(E, 'consertar', [['pessoa', pid, 'moedas', 'soma', -custo], ['estoque', lid, 'prata', 'soma', custo], ['item', iid, 'dur', 'soma', q]], onde=lid, quem=[pid],
                      texto=f"{p['nome']} paga {custo} de prata à {nb[v]} pelo conserto de {it['nome']} ({tantos(q, 'ponto')})")
        n, pq = ato.passa(E, pid, math.ceil(q / O.PAGO_BLOCO), 'consertar', esforco='nada', texto=f"{p['nome']} espera o conserto", para=False)
        it = E['itens']['itens'][iid]
        return dict(pontos=q, custo=custo, feitos=n, parou=pq, texto=f"A {nb[v]} conserta {it['nome']}: {tantos(q, 'ponto')} por {custo} de prata, em {tantos(n, 'bloco')}. Durabilidade {it['dur'][0]}/{it['dur'][1]}.{sobra}")
    pede_mao = O.MAO_DA_OBRA[cat] if cat < len(O.MAO_DA_OBRA) else None
    if pede_mao is None or mao(p, of) < pede_mao:
        sys.exit(f"consertar uma peça {FEM[cat]} pede mão de {T.MAESTRIAS[pede_mao] if pede_mao is not None else 'quem ainda não existe'} em {of}; a de {p['nome']} é de {T.MAESTRIAS[mao(p, of)]}. Pago à oficina: {O.conserto_pago(cat, q, M.peso_do_item(it))} de prata.")
    chave = _materia_conserto(it) or sys.exit(f"{it['nome']} não é peça que a bancada saiba consertar"); unidades = math.ceil(q / O.CONSERTO_MATERIA)
    if p.get('carga', {}).get(chave, 0) < unidades: sys.exit(f"consertar {tantos(q, 'ponto')} de {it['nome']} gasta {unidades} de {_mat(chave)}; {p['nome']} carrega {p.get('carga', {}).get(chave, 0)}")
    def mais(i):
        antes = i * O.CONSERTO_BLOCO; agora = min(O.CONSERTO_BLOCO, q - antes); un = math.ceil((antes + agora) / O.CONSERTO_MATERIA) - math.ceil(antes / O.CONSERTO_MATERIA)
        return [['item', iid, 'dur', 'soma', agora], ['pessoa', pid, 'treino.' + of, 'soma', 1]] + ([['pessoa', pid, 'carga.' + chave, 'soma', -un]] if un else [])
    antes = it['dur'][0]; tinha = p.get('carga', {}).get(chave, 0)
    n, pq = ato.passa(E, pid, math.ceil(q / O.CONSERTO_BLOCO), 'consertar', esforco='pesado', mais=mais, texto=f"{p['nome']} conserta {it['nome']}")
    it = E['itens']['itens'][iid]; p = E['gente'][pid]; feito = it['dur'][0] - antes
    return dict(pontos=feito, custo=0, feitos=n, parou=pq, texto=f"{p['nome']} conserta {it['nome']}: {tantos(feito, 'ponto')} em {tantos(n, 'bloco')}, com {tinha - p.get('carga', {}).get(chave, 0)} de {_mat(chave)}. Durabilidade {it['dur'][0]}/{it['dur'][1]}"
                + sobe(E, pid, of) + (f'. PAROU: {pq}' if pq else '.') + sobra)


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
    if it.get('dono') not in (pid, alvo): sys.exit(f"{it['nome']} não é de {p['nome']}" + (f" nem de {a['nome']}" if alvo != pid else ''))
    of = oficio_de(it)
    if O.ajuste_grau(mao(p, of)) < T.SOB_MEDIDA_GRAUS[0]: sys.exit(f"ajustar pede pelo menos mão de {T.MAESTRIAS[2]} em {of}; a de {p['nome']} é de {T.MAESTRIAS[mao(p, of)]}")
    if any(o['tipo'] == 'ajustar' and o['item'] == iid for o in E['itens'].get('obras', {}).values()): sys.exit(f"{it['nome']} já está num ajuste aberto")
    reg = dict(quem=pid, lugar=lid, tipo='ajustar', oficio=of, item=iid, para=alvo, cat=it['cat'], blocos=0, pede=O.ajuste_blocos(it['cat']))
    estado.aplica(E, 'ajustar', [['obra', 'abre', reg]], onde=lid, quem=[pid, alvo] if alvo != pid else [pid], texto=f"{p['nome']} abre o ajuste de {it['nome']} para {a['nome']}")
    oid = f"o{E['itens']['oseq']:04d}"
    R = continua(E, pid, oid, blocos); R['texto'] = f"Ajuste {oid} aberto: {_peca(it)} para {a['nome']}.\n" + R['texto']
    return R


def _remata_ajuste(E, o):
    oid = o['id']; pid = o['quem']; p = E['gente'][pid]; lid = o['lugar']; of = o['oficio']
    solto = _ajuste_solto(E, o)
    if solto:
        estado.aplica(E, 'ajustar', [['obra', oid, 'fecha']], onde=lid, quem=[pid], texto=f"o ajuste {oid} se desfaz: {solto}")
        return dict(obra=oid, fim='desfeito', item=o['item'], rolagem=None, texto=f"O ajuste {oid} se desfaz: {solto}.")
    it = E['itens']['itens'][o['item']]; a = E['gente'][o['para']]; cat = it['cat']; grau = O.ajuste_grau(mao(p, of)); c = conta(E, pid, cat, of, lid, contra=O.ajuste_contra(cat))
    r = teste.rola(E, f"ajustar {it['nome']} para {a['nome']}", 'Afinidade', c['contra'], mais=c['mais'], quem=pid, **({'dom': c['oculto']} if c['oculto'] else {}))
    margem = r['total'] - r['contra']; ef = [['obra', oid, 'fecha']]; _faixa_do_dom(r, c, margem); conta_txt = f"{teste.total_visto(r)} contra {r['contra']}"
    if talento.decidiu(r): ef += talento.mostra(E, pid)
    if margem >= 0 and grau >= T.SOB_MEDIDA_GRAUS[0]:
        fim = 'acertou'; txt = f"{p['nome']} ajusta {it['nome']} para {a['nome']}, grau {grau} ({conta_txt})"
        ef += [['item', o['item'], 'sob_medida', 'poe', dict(dono=a['nome'], grau=grau, id=o['para'])], ['item', o['item'], 'historia', 'junta', f"Dia {E['relogio']['dia']}: {p['nome']} ajustou para {a['nome']} (grau {grau})"]]
        corpo = estado.corpo_de(a)                          # O AJUSTE RECORTA A PEÇA (etapa 4b): a armadura passa a servir no corpo de quem a pede (tirada de uso antes, se preciso)
        if it['tipo'] == 'armadura' and (it.get('talhe') or 'gente') != corpo:
            if it.get('uso'): ef.append(['item', o['item'], 'uso', 'poe', None])
            ef.append(['item', o['item'], 'talhe', 'poe', None if corpo == 'gente' else corpo]); txt += f" (recortada para o corpo {'miúdo' if corpo == 'miúdo' else 'de gente'})"
    elif margem > -O.POR_POUCO: fim = 'falhou'; txt = f"o ajuste de {it['nome']} não assenta ({conta_txt}): fica como estava"
    else:
        fim = 'estragou'; txt = f"o ajuste de {it['nome']} sai errado ({conta_txt}): a peça perde {O.AJUSTE_ESTRAGO} de durabilidade"
        ef.append(['item', o['item'], 'dur', 'soma', -O.AJUSTE_ESTRAGO])
    estado.aplica(E, 'ajustar', ef, onde=lid, quem=[pid], texto=txt)
    return dict(obra=oid, fim=fim, item=o['item'], rolagem=r, texto=teste.diz(E, r) + f"\n  (o +{c['mais']}: maestria {c['maestria']}, oficina {c['oficina']}, preparo {c['preparo']})\n" + txt + '.' + _diz_dom(E, pid, r))


# ---------- o jornal: a bancada a serviço da oficina do lugar ----------
def jornal(E, pid, blocos, oficio='forja'):
    """N blocos de bancada no serviço miúdo da oficina (a ferramenta do povo): o lugar paga o salário do grau de ofício da pessoa, e os blocos contam como bancada.
    A paga segue a JORNADA (tabelas_mundo: 2 blocos pagos por dia, junto com o `ato.py trabalhar`); passado isso, ou sem prata na oficina, o bloco é só bancada."""
    p = _vivo(E, pid); lid = p['lugar']
    if oficio not in O.BANCA: sys.exit(f'o jornal é de {", ".join(O.BANCA)} (veio "{oficio}")')
    if banca(E, lid, oficio) is None: sys.exit(_sem_banca(E, lid, oficio) + ': não há onde servir')
    grau = O.jornal_grau(mao(p, oficio), p.get('grau_oficio', 'diarista')); paga = M.SALARIO[grau]; tinha = p['moedas']
    def mais(i):
        ef = [['pessoa', pid, 'treino.' + oficio, 'soma', 1]]
        if ato.jornada(E, pid) < M.JORNADA and E['lugares'][lid]['estoque'].get('prata', 0) >= paga: ef += ato.paga_bloco(E, pid, lid, paga)      # depois da jornada, e sem prata, a oficina não paga
        return ef
    onde_serve = dict(encanto='na mesa de runas', alquimia='na botica', fé='no santuário').get(oficio, 'na bancada da oficina')
    n, pq = ato.passa(E, pid, int(blocos), 'trabalhar', esforco=O.JORNAL_ESFORCO if oficio in ('forja', 'couro') else 'leve', mais=mais, texto=f"{p['nome']} serve {onde_serve} ({grau})")
    ganhou = E['gente'][pid]['moedas'] - tinha
    sobe_txt = sobe(E, pid, oficio) if oficio in ('forja', 'couro', 'alquimia', 'encanto') else __import__('magia_mundo').sobe(E, pid, oficio)       # a fé sobe pela tabela das armas (magia_mundo)
    return dict(feitos=n, parou=pq, ganhou=ganhou, texto=f"{p['nome']} serve {tantos(n, 'bloco')} {onde_serve} e recebe {ganhou} de prata" + ('' if ganhou == n * paga else f' (o lugar paga {M.JORNADA} blocos por dia a cada um, e só enquanto tem prata; o resto é serviço sem paga)')
                + sobe_txt + (f'. PAROU: {pq}' if pq else '.'))


# ---------- a obra-prima: escolher o efeito (a etapa dos efeitos, parte 1) ----------
def efeitos_que_cabem(it):
    """os efeitos que a obra-prima pode dar nesta peça: os que valem no tipo dela, menos o "pesa" e os que ela já tem"""
    tem_ja = {e.get('chave') for e in it.get('efeitos') or []}
    return [k for k, (_, tipos) in EFEITOS.items() if it['tipo'] in tipos and k not in ESCOLHE_NAO and k not in tem_ja]


def efeito(E, pid, iid, chave, valor=None):
    """quem tem a peça de obra-prima escolhe um efeito para ela (um dos efeitos por escolher)"""
    import tabelas as TB
    p = E['gente'][pid]; it = E['itens']['itens'].get(iid) or sys.exit(f'não há o item "{iid}" no Livro de Itens')
    if it.get('dono') != pid: sys.exit(f"{it['nome']} não é de {p['nome']}")
    if not it.get('efeitos_livres'): sys.exit(f"{it['nome']} não tem efeito por escolher (só a obra-prima dá: a peça que passa no teste por {O.OBRA_PRIMA[0]} ou mais)")
    cabem = efeitos_que_cabem(it)
    if chave not in cabem: sys.exit(f'"{chave}" não cabe em {it["nome"]}. Cabem: ' + ' · '.join(f"{k} ({EFEITOS[k][0].format(valor='N')})" for k in cabem))
    reg = {'chave': chave}
    if chave == 'devolve':
        mx = TB.devolve_max(it['cat']); v = mx if valor is None else valor
        if not (isinstance(v, int) and 1 <= v <= mx): sys.exit(f'"devolve" numa peça {T.CATS[it["cat"]]} vai de 1 a {mx} (sem valor=, o teto)')
        reg['valor'] = v
    frase = EFEITOS[chave][0].format(valor=reg.get('valor', ''))
    estado.aplica(E, 'forjar', [['item', iid, 'efeito', 'junta', reg], ['item', iid, 'efeitos_livres', 'soma', -1],
                                ['item', iid, 'historia', 'junta', f"Dia {E['relogio']['dia']}: {p['nome']} deu à peça de obra-prima o efeito: {frase}"]],
                  onde=p['lugar'], quem=[pid], texto=f"{p['nome']} escolhe o efeito de {it['nome']}: {frase}")
    resta = E['itens']['itens'][iid].get('efeitos_livres') or 0
    return f"{it['nome']} ganha o efeito: {frase}." + (f" Ainda há {resta} por escolher." if resta else '')


# ---------- o preparo ganho no mundo (o Mestre registra) ----------
def ganha_preparo(E, qual, cat, pid=None, lid=None, como='', oficio='forja'):
    """registra um preparo do ofício: os da pessoa (receita, ajudante) vão para ela; os do lugar (fogo e bigorna; a vidraria da botica; a tinta e a pedra das runas), para o lugar
    onde ela está. `cat`: a categoria que ele alcança (None: perde-se)"""
    tab = tabela_preparos(oficio)
    if qual not in tab: sys.exit(f'preparo desconhecido no ofício {oficio}: "{qual}" (os que existem: {", ".join(tab)})')
    c = None if cat is None else cat_i(cat); de, chave = tab[qual]; alcance = 'nada' if c is None else f'até o {T.CATS[c]}'
    if de == 'pessoa':
        p = _vivo(E, pid); txt = f"{p['nome']} ganha o preparo: {qual} ({alcance})" + (f': {como}' if como else '')
        if not estado.aplica(E, 'mestre', [['pessoa', pid, 'marca.' + chave, 'poe', c]], onde=p['lugar'], quem=[pid], texto=txt): return f"{p['nome']} já tinha esse preparo: nada mudou."
    else:
        lid = lid or _vivo(E, pid)['lugar']; l = E['lugares'].get(lid) or sys.exit(f'não há o lugar "{lid}"')
        txt = f"{l['nome']} ganha o preparo: {qual} ({alcance})" + (f': {como}' if como else '')
        if not estado.aplica(E, 'mestre', [['lugar', lid, 'preparo.' + chave, 'poe', c]], onde=lid, texto=txt): return f"{l['nome']} já tinha esse preparo: nada mudou."
    return txt + '.'


def poe_oficina(E, lid, nivel, como=''):
    """o Mestre registra a oficina de um lugar (0 a 4), ou tira (None)"""
    l = E['lugares'].get(lid) or sys.exit(f'não há o lugar "{lid}"')
    if nivel is not None and not 0 <= nivel < len(O.OFICINAS): sys.exit(f'a oficina vai de 0 ({O.OFICINAS[0]}) a {len(O.OFICINAS) - 1} ({O.OFICINAS[-1]}); veio {nivel}')
    txt = f"{l['nome']} " + ('fica sem oficina' if nivel is None else f'tem agora uma {nome_oficina(nivel)}') + (f': {como}' if como else '')
    if not estado.aplica(E, 'mestre', [['lugar', lid, 'oficina', 'poe', nivel]], onde=lid, texto=txt): return f"{l['nome']} já estava assim: nada mudou."
    return txt + '.'


# ---------- a virada do dia ----------
def virada(E):
    """o dia virou: a obra sem dono vivo se desfaz. (A regra da morte, no estado.py, já desfaz as obras de quem morre, na hora: a matéria que estava nelas se perde,
    e o núcleo cai solto com o resto do que era dele. Isto aqui é só a rede: a obra que ficou órfã por outro caminho.)"""
    for oid, o in list(E['itens'].get('obras', {}).items()):
        q = E['gente'].get(o.get('quem'))
        if q and q['estado'] == 'vivo': continue
        estado.aplica(E, evento_de(o.get('oficio', 'forja'), o.get('tipo')), [['obra', oid, 'fecha']], onde=o.get('lugar'), quem=[o['quem']] if q else [],
                      texto=f"a obra {oid} se desfaz: {q['nome'] if q else 'quem a fazia'} morreu")


# ---------- a mesa ----------
def _diz_preparos(E, pid): return ' · '.join(f"{k}: {'não há' if v is None else 'até o ' + T.CATS[min(v, len(T.CATS) - 1)]}" for k, v in preparos(E, pid).items())


def ver(E, pid):
    """as linhas da oficina para esta pessoa: o lugar, a mão, o preparo, as obras, a matéria, o que dá para fazer e o que custa"""
    p = E['gente'][pid]; l = E['lugares'][p['lugar']]; v = oficina(E, p['lugar']); L = []; itens = E['itens']['itens']
    if estado.fora(E, pid): return [f"**{p['nome']} está fora, {_em(E, estado.fora(E, pid))}:** lá não há bancada."]
    L.append(f"**{l['nome']}:** " + ('não há oficina (não se forja, não se conserta, não se ajusta aqui).' if v is None else f"{nome_oficina(v)} · conserta, pago, até o {T.CATS[min(v + O.OFICINA_CONSERTA, len(T.CATS) - 1)]}"))
    maos = []
    for of in ('forja', 'couro'):
        if not (mao(p, of) or bancada(p, of)) and of != 'forja': continue
        prox = next((f'{T.MAESTRIAS[g]} aos {q}' + (f' e uma obra {FEM[O.FEITO_OBRA[g]]}' if g in O.FEITO_OBRA else '') for g, q in sorted(O.OFICIO_BLOCOS.items()) if g > mao(p, of)), 'o topo')
        maos.append(f"{of} {T.MAESTRIAS[mao(p, of)]} ({tantos(bancada(p, of), 'bloco')} de bancada; {prox})")
    L.append('Mão: ' + ' · '.join(maos)); L.append('Preparo (+2 cada, na obra que ele alcança): ' + _diz_preparos(E, pid))
    f = ferramentas(E, pid, 'forja'); vm, vt, fc = valor_ferramentas(E, pid, 'forja')
    lugar = lambda k, nome: (f"{f[k][0]} {_peca(f[k][1])}" + (' (o jogo: martelo e tenaz)' if (f[k][1].get('forma') or 'jogo') == 'jogo' else '') if f[k] else f"nenhum{'a' if k == 'tenaz' else ''} ({nome})")
    L.append(f"Ferramentas (somam na Lei do Valor): martelo de forja: {lugar('martelo', 'forjar ferramenta martelo CATEGORIA')}, +{vm} · tenaz: {lugar('tenaz', 'forjar ferramenta tenaz CATEGORIA')}, +{vt}" + (_diz_poder(fc) if fc is not None else ''))
    for oid, o in obras_de(E, pid).items():
        L.append(f"Obra aberta {oid}: {_nome_obra(E, o)}, {o['blocos']} de {o['pede']} blocos, {_em(E, o['lugar'])} (`oficio.py continua {oid}`)")
    mat = {k: n for k, n in p.get('carga', {}).items() if M.le_materia(k)[1] is not None}; nuc = [f"{i} {it['nome']} ({T.CATS[it['cat']]})" for i, it in itens.items() if it['tipo'] == 'nucleo' and it.get('dono') == pid]
    if mat or nuc: L.append('Matéria na carga: ' + (_lista(mat) if mat else 'nenhuma') + (' · núcleos: ' + ', '.join(nuc) if nuc else ''))
    if v is None: return L
    L += ['', '**Na bancada** (bloco pesado; `oficio.py pede ...` diz a matéria e a chance antes de abrir):',
          '- forjar (a LEI DO VALOR: a soma decide a categoria): escolhe-se a peça e a matéria que entra; os blocos vêm da matéria (' + ', '.join(f'{T.CATS[c]} {O.blocos(c)}' for c in range(M.MATERIA_ATE + 1))
          + f'); do {T.CATS[M.MATERIA_ATE + 1]} para cima, a matéria Rara e um núcleo (' + ', '.join(f'{T.CATS[c]} {O.blocos(c)}' for c in range(M.MATERIA_ATE + 1, O.FORJA_ATE + 1)) + ' blocos). '
          + 'A peça sai na maior categoria cuja CD a soma alcança (' + ' · '.join(f'{T.CATS[c]} {O.VALOR_CD[c]}' for c in range(len(O.VALOR_CD))) + f'), até o teto (sem núcleo, uma acima da matéria e nunca acima do {T.CATS[M.MATERIA_ATE]}); abaixo da CD do Comum, a matéria se perde. `oficio.py pede ...` diz a chance de cada categoria.']
    gastas = [(i, it) for i, it in itens.items() if it.get('dono') == pid and it['tipo'] in PECAS + O.PECAS_LADINO and it['dur'][0] < it['dur'][1]]
    for i, it in gastas[:4]:
        q = it['dur'][1] - it['dur'][0]; of = oficio_de(it); chave = _materia_conserto(it); pode = chave and it['cat'] < len(O.MAO_DA_OBRA) and mao(p, of) >= O.MAO_DA_OBRA[it['cat']]
        eu_txt = f"você, {tantos(math.ceil(q / O.CONSERTO_BLOCO), 'bloco')} e {math.ceil(q / O.CONSERTO_MATERIA)} de {_mat(chave)}" if pode else 'você não tem a mão'
        pago = f"pago, {O.conserto_pago(it['cat'], q, M.peso_do_item(it))} de prata e {tantos(math.ceil(q / O.PAGO_BLOCO), 'bloco')} de espera" if it['cat'] <= v + O.OFICINA_CONSERTA else 'esta oficina não conserta'
        L.append(f"- consertar {it['nome']} ({i}, {it['dur'][0]}/{it['dur'][1]}): {eu_txt}; {pago}")
    if len(gastas) > 4: L.append(f"- ... e mais {tantos(len(gastas) - 4, 'peça gasta', 'peças gastas')}")
    L.append(f"- o conserto pago (`oficio.py consertar ITEM pago`): {100 * M.CONSERTO_PONTO:g}% do preço da peça por ponto, em prata inteira (arredonda para cima: um ponto de uma espada Comum custa {O.conserto_pago(0, 1)} de prata), "
             f"e um bloco de espera por peça (a cada {O.PAGO_BLOCO} pontos ou parte): mandar consertar quatro peças leva quatro blocos")
    g = O.ajuste_grau(mao(p))
    L.append('- ajustar (sob medida): ' + (f'grau {g}; de {O.ajuste_blocos(0)} (Comum) a {O.ajuste_blocos(O.FORJA_ATE)} blocos ({T.CATS[O.FORJA_ATE]}) e um teste contra {O.AJUSTE_BASE} + {O.TESTE_CAT} por categoria' if g else f'pede mão de {T.MAESTRIAS[2]}'))
    L.append(f"- jornal: {M.SALARIO[O.jornal_grau(mao(p), p.get('grau_oficio', 'diarista'))]} de prata por bloco de bancada a serviço da oficina (paga-se pelo que a mão vale: {O.jornal_grau(mao(p), p.get('grau_oficio', 'diarista'))}), até a jornada ({M.JORNADA} blocos pagos por dia; hoje: {ato.jornada(E, pid)}) (`oficio.py jornal N`)")
    return L


def mesa(E):
    """as linhas do ofício para a MESA.md"""
    pid = estado.eu(E)
    if not pid: return []
    if estado.fora(E, pid): return []                        # quem está no ermo não tem bancada à frente: a MESA não a mostra
    return ['## A oficina'] + ver(E, pid)


# ---------- a linha de comando ----------
def main(a=None):
    a = sys.argv[1:] if a is None else list(a)
    if not a: print(__doc__); return
    op = dict(x.split('=', 1) for x in a if '=' in x); pos = [x for x in a if '=' not in x]
    cmds = ('ver', 'pede', 'forjar', 'continua', 'larga', 'consertar', 'ajustar', 'jornal', 'preparo', 'oficina', 'efeito')
    if not pos or pos[0] not in cmds: print(__doc__); return
    if pos[0] == 'jornal' and (len(pos) < 2 or not pos[1].isdigit() or int(pos[1]) < 1):       # uma frase por erro, em vez do uso inteiro
        sys.exit("diga quantos blocos de jornal, em número inteiro (1 ou mais): `python3 oficio.py jornal 2`" + (f' (veio "{pos[1]}")' if len(pos) > 1 else '') + '. Um bloco são 4 horas.')
    E = estado.carrega(); pid = op.get('quem') or estado.eu(E)
    if pid not in E['gente']: sys.exit(f'não há a pessoa "{pid}"')
    inteiro = lambda k: int(op[k]) if op.get(k, '').isdigit() else sys.exit(f'{k}= pede um número inteiro, de zero para cima (veio "{op[k]}")') if k in op else None
    def peca(i):
        tipo = pos[i] if len(pos) > i else sys.exit('diga o que forjar: arma FAMILIA CATEGORIA, armadura MATERIAL CATEGORIA, escudo CATEGORIA ou gazua CATEGORIA. Veja o uso: python3 oficio.py')
        if tipo in SEM_FAMILIA: fam = None; resto = pos[i + 1:]
        else: fam = pos[i + 1] if len(pos) > i + 1 else None; resto = pos[i + 2:]
        if tipo in FORJA and not resto: sys.exit('falta a categoria da peça. Veja o uso: python3 oficio.py')
        resto = resto or [0]
        return molde(tipo, resto[0], resto[1] if len(resto) > 1 else None, familia=fam if tipo == 'arma' else None, material=fam if tipo == 'armadura' else None,
                     cobre=op['cobre'].split(',') if op.get('cobre') else None, forma=fam if tipo == 'foco' else None, talhe=talhe_de(tipo), oficio=fam if tipo == 'ferramenta' else None)
    def talhe_de(tipo):
        """o talhe da armadura que se forja: o dito (talhe=miúdo), ou o do corpo de quem vai vesti-la (para=ID; etapa 4b)"""
        if 'para' not in op or tipo != 'armadura': return op.get('talhe')
        q = E['gente'].get(op['para']) or sys.exit(f'não há a pessoa "{op["para"]}" (para= diz para quem é a armadura)')
        c = estado.corpo_de(q); return None if c == 'gente' else c
    falta = lambda o_que, exemplo: sys.exit(f'{o_que}: `python3 oficio.py {exemplo}`')
    if pos[0] == 'ver': print('\n'.join(ver(E, pid))); return
    if pos[0] == 'pede': print(pede(E, pid, peca(1))); return
    if pos[0] == 'forjar': out = forjar(E, pid, peca(1), blocos=inteiro('blocos'), nucleo=op.get('nucleo'))['texto']
    elif pos[0] == 'continua': out = continua(E, pid, pos[1] if len(pos) > 1 else None, blocos=inteiro('blocos'))['texto']
    elif pos[0] == 'larga': out = larga(E, pid, pos[1] if len(pos) > 1 else falta('diga qual obra largar (o id dela: `oficio.py ver` mostra)', 'larga o0001'))['texto']
    elif pos[0] == 'consertar': out = consertar(E, pid, pos[1] if len(pos) > 1 else falta('diga qual peça consertar (o id dela)', 'consertar i0007 pago'), pontos=inteiro('pontos'), pago='pago' in pos[2:])['texto']
    elif pos[0] == 'ajustar': out = ajustar(E, pid, pos[1] if len(pos) > 1 else falta('diga qual peça ajustar (o id dela)', 'ajustar i0007'), para=op.get('para'), blocos=inteiro('blocos'))['texto']
    elif pos[0] == 'jornal': out = jornal(E, pid, int(pos[1]), oficio=op.get('oficio', 'forja'))['texto']
    elif pos[0] == 'efeito':
        if len(pos) < 3: falta('diga a peça e o efeito da obra-prima', 'efeito i0007 critico_19')
        out = efeito(E, pid, pos[1], pos[2], valor=inteiro('valor'))
    elif pos[0] == 'preparo':
        if len(pos) < 3: falta('diga qual preparo (receita, ajudante, fogo ou bigorna) e até que categoria ele serve (ou "nada")', 'preparo fogo Raro "como foi ganho"')
        out = ganha_preparo(E, pos[1], None if pos[2] == 'nada' else pos[2], pid=pid, como=pos[3] if len(pos) > 3 else '', oficio=op.get('oficio', 'forja'))
    else:                                                   # oficina
        if len(pos) < 2 or not (pos[1] == 'nada' or pos[1].isdigit()): falta(f'diga o nível da oficina, de 0 ({O.OFICINAS[0]}) a {len(O.OFICINAS) - 1} ({O.OFICINAS[-1]}), ou "nada"', 'oficina 1 "como foi"')
        out = poe_oficina(E, E['gente'][pid]['lugar'], None if pos[1] == 'nada' else int(pos[1]), como=pos[2] if len(pos) > 2 else '')
    estado.grava(E)                                         # grava ANTES de falar: a saída cortada não perde o que o dado rolou
    print(out)
    print(ato.ultima_linha(E, pid))


if __name__ == '__main__':
    import signal; hasattr(signal, 'SIGPIPE') and signal.signal(signal.SIGPIPE, signal.SIG_DFL)      # a saída cortada (`| head`) acaba o comando calada, sem erro de programa: tudo já foi gravado antes de falar
    main()
