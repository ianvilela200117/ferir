#!/usr/bin/env python3
"""alquimia.py — MOTOR 10: A ALQUIMIA E O BEBER (etapa da magia, capítulo 12). Os números moram no tabelas_magia_mundo.py; o preço das poções, no tabelas_mercado.py.

  A LEVA é uma obra no molde da forja (oficio.py): a matéria da receita entra quando ela abre, 3^k blocos PESADOS de bancada numa BOTICA (o campo `botica` do lugar,
    0 a 4), e no fim UM teste: 2d20 + maestria de alquimia + Afinidade ÷ 10 + a botica + o preparo (receita, ajudante, fogo, vidraria: +2 cada; com o dom, até +8),
    contra 28 + 6 por categoria. Rende 2 doses do Comum ao Raro (bens, na carga: "cura:0") e 6 elixires do Épico para cima (itens do Livro, contados no mundo; a leva
    pede matéria Rara e um NÚCLEO da categoria). Falhar por 1 a 4: sai uma categoria abaixo (a Comum sai aguada: 1 dose). Por 5 ou mais: a matéria some, e o núcleo também.
  AS NOVE RECEITAS: cura, antídoto, veneno de lâmina (peçonha), Mana, guarda, fúria, vigília, quebra-maldição (água benta e osso) e o remédio (3 de erva Comum).
  BEBER (fora da luta; na luta é a ordem `beber`): Vigor ÷ 30 doses por dia (no mínimo 1); cada uma além disso pede Vigor contra 24 + 4 por dose a mais (falhou: a poção não faz
    nada e a pessoa enjoa). A CURA segue a lei ao contrário: 1d8 × 6 × 3^(categoria da poção − categoria da ferida mais funda), e por dia, feitiço e poção somados, nunca
    mais que metade do PV máximo. A Mana devolve 4 por degrau; a guarda vale amuleto da categoria por 1 bloco; a vigília tira sono e cansaço (uma por dia); o quebra-maldição
    quebra a maldição de categoria menor, faz recuar 2 passos a da mesma e segura 1 dia a maior. O antídoto e a fúria só servem na luta.
  O VENENO DE LÂMINA passa-se na arma (corte ou ponta): a primeira ferida que ela abrir na luta envenena; seca em um dia; 1 dose = 1 golpe. É crime nas vilas.

Uso (o personagem do jogador, ou quem=ID):
  python3 alquimia.py ver                                  a botica daqui, a sua mão, as poções que leva, o que bebeu e o que curou hoje
  python3 alquimia.py pede POCAO CATEGORIA                 o que a leva pede (matéria, núcleo, blocos) e a chance, sem abrir nada
  python3 alquimia.py fazer POCAO CATEGORIA [blocos=N] [nucleo=ID]     abre a leva (a matéria entra) e trabalha N blocos (sem N: até fechar)
  python3 alquimia.py continua [OBRA] [blocos=N]           mais blocos na leva aberta · python3 alquimia.py larga OBRA
  python3 alquimia.py beber POCAO:CAT|ELIXIR [alvo=ID] [maldicao=MID]     bebe (ou dá de beber a quem está junto); o quebra-maldição escolhe a maldição
  python3 alquimia.py lamina [ARMA] [cat=K]                passa uma dose de veneno de lâmina na arma (a que está na mão, se não disser)
  python3 alquimia.py jornal N                             N blocos a serviço da botica do lugar (o salário da sua mão, até a jornada)
  python3 alquimia.py botica NIVEL|nada "como foi"         o Mestre registra a botica do lugar onde a pessoa está (0 a 4)
POCAO: cura antídoto veneno mana guarda fúria vigília quebra-maldição remédio · CATEGORIA: Comum Incomum Raro Épico Único Lendário
"""
import secrets, sys
import tabelas as T
import tabelas_mundo as M
import tabelas_oficio as O
import tabelas_magia_mundo as W
import estado, ato, teste, talento, oficio
from itens import item, cat_i

FEM = oficio.FEM
RECEITAS = tuple(W.RECEITAS) + ('remédio',)
tantos = estado.tantos


# ---------- a receita ----------
def nome_pocao(pocao, cat):
    if pocao == 'remédio': return 'remédio'
    return estado.nome_bem(M.materia(pocao, cat)) if cat <= M.POCAO_ATE else f"elixir de {M.POCOES[pocao].replace('poção de ', '')} {T.CATS[cat]}"


def materia_leva(pocao, cat):
    """{chave: quanto} que a leva gasta: a receita na categoria da leva (do Épico para cima, matéria Rara); a água benta, sem categoria"""
    if pocao == 'remédio': return dict(W.REMEDIO)
    c = O.cat_materia(cat)
    return {(k if k in M.BENS else M.materia(k, c)): n for k, n in W.RECEITAS[pocao].items()}


def confere(pocao, cat):
    """a receita e a categoria, conferidas ANTES de qualquer coisa mudar; devolve o índice da categoria"""
    if pocao not in RECEITAS: sys.exit(f'não há receita de "{pocao}" (as que há: {", ".join(RECEITAS)})')
    c = cat_i(cat)
    if c > W.ALQUIMIA_ATE: sys.exit(f'ninguém faz poção acima do {T.CATS[W.ALQUIMIA_ATE]} (veio {T.CATS[c]})')
    if pocao == 'remédio' and c: sys.exit('o remédio é um só (não tem categoria): faça-o Comum')
    if pocao == 'veneno' and c > W.VENENO_ATE: sys.exit(f'o veneno de lâmina não passa do {T.CATS[W.VENENO_ATE]}: é o que há de peçonha')
    return c


def _mat(d): return ', '.join(f'{n} de {estado.nome_bem(k)}' for k, n in d.items())


# ---------- pedir e fazer ----------
def pede(E, pid, pocao, cat):
    """o que a leva pede e a conta de hoje, sem abrir nada"""
    c = confere(pocao, cat); p = oficio._vivo(E, pid); mat = materia_leva(pocao, c); carga = p.get('carga', {}); v = oficio.banca(E, p['lugar'], 'alquimia')
    rende = '1 remédio' if pocao == 'remédio' else tantos(W.DOSES, 'dose') if c <= M.POCAO_ATE else tantos(W.ELIXIRES, 'elixir', 'elixires')
    L = [f"leva de {nome_pocao(pocao, c)} · {tantos(O.blocos(c), 'bloco pesado', 'blocos pesados')} de botica · rende {rende}",
         'Matéria: ' + ', '.join(f"{n} de {estado.nome_bem(k)} (você tem {carga.get(k, 0)})" for k, n in mat.items()) + (f' · e um núcleo {T.CATS[c]}' if O.pede_nucleo(c) else '')]
    if v is None: L.append(f"{E['lugares'][p['lugar']]['nome']} não tem botica: a leva não abre.")
    else: L.append('O teste final, hoje e aqui: ' + oficio.diz_conta(oficio.conta(E, pid, c, 'alquimia'), pouco='sai uma abaixo' if c else 'sai aguada', banca='botica'))
    return '\n'.join(L)


def fazer(E, pid, pocao, cat, blocos=None, nucleo=None):
    """abre a leva (a matéria sai da carga e entra nela) e trabalha `blocos` blocos (None: até fechar, ou até o corpo parar; 0: só abre)"""
    c = confere(pocao, cat); p = oficio._vivo(E, pid); lid = p['lugar']
    if oficio.banca(E, lid, 'alquimia') is None: sys.exit(f"{E['lugares'][lid]['nome']} não tem botica: a leva não abre")
    mat = materia_leva(pocao, c); carga = p.get('carga', {}); falta = {k: n - carga.get(k, 0) for k, n in mat.items() if carga.get(k, 0) < n}
    if falta: sys.exit(f"falta matéria para a leva de {nome_pocao(pocao, c)}: {_mat(falta)} (a leva pede {_mat(mat)})")
    nid = oficio._nucleo(E, pid, c, nucleo) if O.pede_nucleo(c) else None
    if nucleo and not nid: sys.exit(f'uma leva {FEM[c]} não leva núcleo (só do {T.CATS[M.MATERIA_ATE + 1]} para cima)')
    nome = f"a leva de {nome_pocao(pocao, c)}"
    reg = dict(quem=pid, lugar=lid, tipo='leva', oficio='alquimia', pocao=pocao, cat=c, blocos=0, pede=O.blocos(c), materia=mat, nucleo=nid, nome=nome)
    ef = [['pessoa', pid, 'carga.' + k, 'soma', -n] for k, n in mat.items()] + [['obra', 'abre', reg]]
    if nid: ef.append(['item', nid, 'historia', 'junta', f"Dia {E['relogio']['dia']}: entrou n{nome[1:]}"])
    estado.aplica(E, 'alquimia', ef, onde=lid, quem=[pid], texto=f"{p['nome']} abre {nome}; entram {_mat(mat)}" + (f" e {E['itens']['itens'][nid]['nome']}" if nid else ''))
    oid = f"o{E['itens']['oseq']:04d}"
    R = oficio.continua(E, pid, oid, blocos)
    R['texto'] = f"Obra {oid} aberta: {nome}. Entraram {_mat(mat)}" + (f" e o núcleo {nid}" if nid else '') + '.\n' + R['texto']
    return R


def remata(E, o):
    """os blocos da leva fecharam: sai o teste final (dado de verdade, uma vez) e a obra fecha (oficio.remata chama isto)"""
    oid = o['id']; pid = o['quem']; p = E['gente'][pid]; c = o['cat']; pocao = o['pocao']; lid = o['lugar']; nid = o.get('nucleo'); L = E['itens']['itens']; dia = E['relogio']['dia']
    if nid and nid not in L: sys.exit(f'o núcleo da leva {oid} não está mais no Livro de Itens: a leva não fecha (largue-a com `larga`)')
    k = oficio.conta(E, pid, c, 'alquimia', lid); nuc = L[nid]['nome'] if nid else None
    r = teste.rola(E, o.get('nome', 'a leva'), 'Afinidade', k['contra'], mais=k['mais'], quem=pid, **({'dom': k['oculto']} if k['oculto'] else {}))
    margem = r['total'] - r['contra']; oficio._faixa_do_dom(r, k, margem)
    sai = c if margem >= 0 else c - 1 if margem > -O.POR_POUCO else None
    fim = 'acertou' if margem >= 0 else 'abaixo' if sai is not None else 'perdeu'
    ef = []; nascem = []
    if sai is not None:
        if pocao == 'remédio': ef.append(['pessoa', pid, 'carga.remédio', 'soma', 1]); rende = '1 remédio'
        elif sai < 0: ef.append(['pessoa', pid, 'carga.' + M.materia(pocao, 0), 'soma', W.AGUADA]); rende = f"{tantos(W.AGUADA, 'dose')} de {nome_pocao(pocao, 0)} (aguada)"
        else:
            n = W.DOSES if c <= M.POCAO_ATE else W.ELIXIRES
            if sai <= M.POCAO_ATE: ef.append(['pessoa', pid, 'carga.' + M.materia(pocao, sai), 'soma', n]); rende = f"{tantos(n, 'dose')} de {nome_pocao(pocao, sai)}"
            else:
                for _ in range(n):
                    x = item('elixir', sai, pocao=pocao, dono=pid, feito_por=pid, dia=dia); x['historia'].append(f"Dia {dia}: {p['nome']} fez {estado.em(E, lid)}" + (f', com {nuc}' if nuc else ''))
                    ef.append(['item', 'nasce', x]); nascem.append(x)
                rende = f"{tantos(n, 'elixir', 'elixires')} de {M.POCOES[pocao].replace('poção de ', '')} {T.CATS[sai]}"
        for grau, quer in sorted(O.FEITO_OBRA.items()):                     # o feito: uma leva nascida da categoria certa (ou melhor)
            if sai >= quer and p.get('marca', {}).get('feito_alquimia', 0) < grau: ef.append(['pessoa', pid, 'marca.feito_alquimia', 'poe', grau])
    if nid: ef.append(['item', nid, 'some'])
    ef.append(['obra', oid, 'fecha'])
    if talento.decidiu(r): ef += talento.mostra(E, pid)
    conta_txt = f"{teste.total_visto(r)} contra {r['contra']}"
    if fim == 'acertou': txt = f"{p['nome']} acerta {o.get('nome', 'a leva')} ({conta_txt}): {rende}"
    elif fim == 'abaixo': txt = f"{p['nome']} erra por pouco {o.get('nome', 'a leva')} ({conta_txt}): sai {rende}" + (f'; {nuc} se gasta nela' if nuc else '')
    else: txt = f"{o.get('nome', 'a leva')[0].upper() + o.get('nome', 'a leva')[1:]} se perde ({conta_txt}): some a matéria ({_mat(o['materia'])})" + (f' e some {nuc}' if nuc else '')
    estado.aplica(E, 'alquimia', ef, onde=lid, quem=[pid], texto=txt)
    ids = [f"i{E['itens']['seq'] - len(nascem) + i + 1:04d}" for i in range(len(nascem))]
    out = teste.diz(E, r) + f"\n  (o +{k['mais']}: maestria {k['maestria']}, botica {k['oficina']}, preparo {k['preparo']})\n" + txt + (f". Entraram no Livro de Itens: {', '.join(ids)}" if ids else '') + oficio._diz_dom(E, pid, r) + oficio.sobe(E, pid, 'alquimia')
    return dict(obra=oid, fim=fim, item=ids[0] if ids else None, itens=ids, rolagem=r, texto=out)


# ---------- beber fora da luta ----------
def _a_beber(E, pid, coisa):
    """o que se bebe: ('bem', chave, nome, categoria) da carga, ou ('elixir', id, poção, categoria) do Livro. "cura" sem categoria vale se só há uma na carga."""
    p = E['gente'][pid]; L = E['itens']['itens']
    if coisa in L:
        it = L[coisa]
        if it.get('tipo') != 'elixir' or it.get('dono') != pid: sys.exit(f"{it['nome']} ({coisa}) não é um elixir de {p['nome']}")
        return 'elixir', coisa, it['pocao'], it['cat']
    n, c = M.le_materia(coisa)
    if c is None:
        tem = sorted(k for k, q in (p.get('carga') or {}).items() if q > 0 and M.le_materia(k)[0] == coisa and estado.e_pocao(k))
        if len(tem) != 1: sys.exit(f'diga a categoria da poção ({coisa}:0, {coisa}:1, {coisa}:2)' + (f": {p['nome']} leva {', '.join(estado.nome_bem(k) for k in tem)}" if tem else f": {p['nome']} não leva {coisa}"))
        coisa = tem[0]; n, c = M.le_materia(coisa)
    if n not in M.POCOES or c > M.POCAO_ATE: sys.exit(f'"{coisa}" não é poção (as poções: {", ".join(M.POCOES)}; do Épico para cima é elixir: o id dele)')
    if (p.get('carga') or {}).get(coisa, 0) < 1: sys.exit(f"{p['nome']} não leva {estado.nome_bem(coisa)}")
    return 'bem', coisa, n, c


def _junto(E, pid, alvo):
    """quem bebe: a própria pessoa, ou quem está com ela (no mesmo lugar, ou na mesma saída), vivo"""
    if alvo in (None, pid): return pid
    q = E['gente'].get(alvo) or sys.exit(f'não há a pessoa "{alvo}"')
    if q['estado'] != 'vivo': sys.exit(f"{q['nome']} não bebe: {estado.morte_diz(E, q)}")
    if estado.onde(E, alvo) != estado.onde(E, pid): sys.exit(f"{q['nome']} não está com {E['gente'][pid]['nome']}: não há a quem dar de beber")
    estado.em_cena(E, alvo); return alvo


def d(lados): return secrets.randbelow(lados) + 1      # o dado de quem está em cena (a cura da poção e do feitiço): rolado uma vez, e dito


def beber(E, pid, coisa, alvo=None, mid=None):
    """bebe (ou dá de beber a quem está junto) uma poção da carga ou um elixir, fora da luta. Recusa, antes de gastar, o que fora da luta não faz nada."""
    p = E['gente'].get(pid) or sys.exit(f'não há a pessoa "{pid}"')
    if p['estado'] != 'vivo': sys.exit(f"{p['nome']} não age: {estado.morte_diz(E, p)}")
    estado.sem_luta(E); estado.em_cena(E, pid)
    if coisa == 'remédio' or M.le_materia(coisa)[0] == 'remédio': sys.exit('o remédio não se bebe: serve a quem trata a ferida (`magia_mundo.py tratar PACIENTE`)')
    tipo, chave, pocao, cat = _a_beber(E, pid, coisa); q = _junto(E, pid, alvo); b = E['gente'][q]; dia = E['relogio']['dia']
    nome = nome_pocao(pocao, cat) if tipo == 'bem' else E['itens']['itens'][chave]['nome']
    if pocao in W.SO_NA_LUTA: sys.exit(f"{nome}: fora da luta não faz nada (" + ('não há veneno a tirar' if pocao == 'antídoto' else 'a fúria é de cinco rodadas') + '). Na luta: a ordem `beber`.')
    if pocao == 'veneno': sys.exit('o veneno de lâmina não se bebe: passa-se na arma (`alquimia.py lamina`)')
    if pocao == 'vigília' and (b.get('marca') or {}).get('vigilia_dia') == dia: sys.exit(f"{b['nome']} já bebeu vigília hoje: a segunda não faz nada")
    if pocao == 'cura' and b['pv'] >= estado.pv_max(b): sys.exit(f"{b['nome']} está com o PV cheio ({b['pv']}/{estado.pv_max(b)}): {nome} não faria nada (nada se gasta)")
    mal = None
    if pocao == 'quebra-maldição':
        ms = [m for m in b.get('maldicoes') or [] if isinstance(m, dict)]
        if not ms: sys.exit(f"{b['nome']} não tem maldição andando: o quebra-maldição não faz nada")
        mal = next((m for m in ms if m['id'] == mid), None) if mid else max(ms, key=lambda m: (m['passo'], m['cat']))
        if mal is None: sys.exit(f"{b['nome']} não tem a maldição \"{mid}\"")
    gasta = [['pessoa', pid, 'carga.' + chave, 'soma', -1]] if tipo == 'bem' else [['item', chave, 'some']]
    n = estado.hoje(E, b, 'doses'); limite = T.doses_dia(b['atributos']['Vigor']); ef = list(gasta) + [['pessoa', q, 'marca.doses', 'poe', dict(dia=dia, n=n + 1)]]
    linhas = []; quem_bebe = f"{b['nome']} bebe" if q == pid else f"{p['nome']} dá a {b['nome']}"
    if n >= limite:                                          # passou das doses do dia: o corpo pode recusar
        r = teste.rola(E, f"aguentar mais uma poção ({n + 1}ª do dia)", 'Vigor', T.ENJOO[0] + T.ENJOO[1] * (n - limite + 1), quem=q)
        linhas.append(teste.diz(E, r))
        if not r['passou']:
            ef.append(['pessoa', q, 'marca.enjoo', 'poe', dict(ate=estado.agora(E) + W.ENJOO_DURA)])
            estado.aplica(E, 'beber', ef, onde=estado.onde(E, pid), quem=list(dict.fromkeys([pid, q])), texto=f"{quem_bebe} {nome}, e o corpo a põe para fora")
            return dict(fim='enjoou', texto='\n'.join(linhas + [f"{b['nome']} já bebeu {tantos(n, 'poção', 'poções')} hoje (o corpo aguenta {limite}): a poção não faz nada, e {b['nome']} enjoa ({W.ENJOO_DURA} bloco de −2 em tudo)."]))
    if pocao == 'cura':
        dado = d(8); bruto = int(T.cura(dado, cat, b.get('funda'))); teto = max(0, int(estado.pv_max(b) * T.CURA_TETO) - estado.hoje(E, b, 'curado')); falta = estado.pv_max(b) - b['pv']
        cura = max(0, min(bruto, teto, falta))
        if cura: ef += [['pessoa', q, 'pv', 'soma', cura], ['pessoa', q, 'marca.curado', 'poe', dict(dia=dia, n=estado.hoje(E, b, 'curado') + cura)]]
        fd = b.get('funda') or 0; lei = '' if fd == cat else f" (a ferida mais funda é {T.CATS[fd]}: a poção {FEM[cat] if cat <= M.POCAO_ATE else T.CATS[cat]} vale {'o triplo' if cat - fd == 1 else 'um terço' if cat - fd == -1 else f'3^{cat - fd}'.replace('-', '−')})"
        por_que = '' if cura == bruto else ' (o teto da cura de hoje: metade do PV máximo por dia, feitiço e poção somados)' if cura == teto else ' (o PV encheu)'
        linhas.append(f"{quem_bebe} {nome}: 1d8 = {dado}, × 6 × 3^(poção − ferida){lei} = {bruto}; cura {cura}{por_que}. PV {b['pv'] + cura}/{estado.pv_max(b)}")
    elif pocao == 'mana':
        import magia_mundo
        mais = W.MANA_POCAO * (cat + 1); m0, mx = magia_mundo.mana_vista(b); ef.append(['pessoa', q, 'mana', 'soma', mais])
        linhas.append(f"{quem_bebe} {nome}: Mana {m0} → {min(mx, m0 + mais)} de {mx}" + (' (já estava cheia)' if m0 >= mx else ''))
    elif pocao == 'guarda':
        ef.append(['pessoa', q, 'marca.guarda', 'poe', dict(cat=cat, ate=estado.agora(E) + W.GUARDA_DURA)])
        linhas.append(f"{quem_bebe} {nome}: por {tantos(W.GUARDA_DURA, 'bloco')}, conta como amuleto {T.CATS[cat]} (contra a maldição, o lugar maldito e a magia na luta)")
    elif pocao == 'vigília':
        ef += [['pessoa', q, 'sono', 'soma', W.VIGILIA['sono']], ['pessoa', q, 'cansaco', 'soma', W.VIGILIA['cansaco']], ['pessoa', q, 'marca.vigilia_dia', 'poe', dia]]
        linhas.append(f"{quem_bebe} {nome}: sono {W.VIGILIA['sono']}, cansaço {W.VIGILIA['cansaco']}".replace('-', '−'))
    elif pocao == 'quebra-maldição':
        import maldicao
        ef += maldicao.pela_pocao(E, q, mal, cat)
        linhas.append(f"{quem_bebe} {nome}: " + maldicao.diz_pocao(mal, cat, b))
    estado.aplica(E, 'beber', ef, onde=estado.onde(E, pid), quem=list(dict.fromkeys([pid, q])), texto=f"{quem_bebe} {nome}")
    return dict(fim='bebeu', texto='\n'.join(linhas))


def lamina(E, pid, arma=None, cat=None):
    """passa uma dose de veneno de lâmina na arma (corte ou ponta): a primeira ferida que ela abrir na luta envenena; seca em um dia. Crime nas vilas."""
    p = E['gente'].get(pid) or sys.exit(f'não há a pessoa "{pid}"')
    if p['estado'] != 'vivo': sys.exit(f"{p['nome']} não age: {estado.morte_diz(E, p)}")
    estado.sem_luta(E); estado.em_cena(E, pid); L = E['itens']['itens']
    iid = arma or (estado.pecas(E, pid)['arma'] or {}).get('id') or sys.exit(f"{p['nome']} não tem arma na mão: diga qual (`alquimia.py lamina ITEM`)")
    it = L.get(iid) or sys.exit(f'não há o item "{iid}" no Livro de Itens')
    if it.get('dono') != pid or it.get('tipo') != 'arma': sys.exit(f"{it['nome']} não é uma arma de {p['nome']}")
    if T.FAMILIAS[it['familia']]['golpe'] not in ('corte', 'ponta'): sys.exit(f"{it['nome']} não tem fio nem ponta: o veneno não fica nela")
    doses = sorted((M.le_materia(k)[1], k) for k, q in (p.get('carga') or {}).items() if q > 0 and M.le_materia(k)[0] == 'veneno' and estado.e_pocao(k))
    if cat is not None: doses = [x for x in doses if x[0] == cat_i(cat)]
    if not doses: sys.exit(f"{p['nome']} não leva veneno de lâmina" + (f" {FEM[cat_i(cat)]}" if cat is not None else ''))
    c, chave = doses[-1]; ate = estado.agora(E) + M.VENENO_DURA
    crime = ' É crime aqui: quem vir, conta ao guarda.' if E['lugares'][estado.onde(E, pid)].get('pop') else ''
    estado.aplica(E, 'beber', [['pessoa', pid, 'carga.' + chave, 'soma', -1], ['item', iid, 'veneno', 'poe', dict(cat=c, ate=ate)]], onde=estado.onde(E, pid), quem=[pid],
                  texto=f"{p['nome']} passa veneno na lâmina de {it['nome']}")
    fraco = f" A dose é {FEM[c]} e a arma {FEM[it['cat']]}: rende um terço por degrau." if it['cat'] > c else ''
    return f"{p['nome']} passa uma dose de {estado.nome_bem(chave)} em {it['nome']}: a primeira ferida que a arma abrir na luta envenena (um golpe). Seca em um dia.{fraco}{crime}"


# ---------- o lugar ----------
def poe_botica(E, lid, nivel, como=''):
    """o Mestre (ou o gerador) registra a botica de um lugar (0 a 4), ou tira (None)"""
    l = E['lugares'].get(lid) or sys.exit(f'não há o lugar "{lid}"')
    if nivel is not None and not 0 <= nivel < len(W.BOTICAS): sys.exit(f'a botica vai de 0 ({W.BOTICAS[0]}) a {len(W.BOTICAS) - 1} ({W.BOTICAS[-1]}); veio {nivel}')
    txt = f"{l['nome']} " + ('fica sem botica' if nivel is None else f'tem agora uma {oficio.nome_banca("alquimia", nivel)}') + (f': {como}' if como else '')
    if not estado.aplica(E, 'mestre', [['lugar', lid, 'botica', 'poe', nivel]], onde=lid, texto=txt): return f"{l['nome']} já estava assim: nada mudou."
    return txt + '.'


# ---------- a mesa ----------
def ver(E, pid):
    p = E['gente'][pid]; f = estado.fora(E, pid); lid = p['lugar']; v = oficio.banca(E, lid, 'alquimia'); dia = E['relogio']['dia']; L = []
    pocoes = [f"{q:g} de {estado.nome_bem(k)}" for k, q in (p.get('carga') or {}).items() if q and estado.e_pocao(k)]
    elix = [f"{i} {it['nome']}" for i, it in E['itens']['itens'].items() if it.get('dono') == pid and it.get('tipo') == 'elixir']
    mao = oficio.mao(p, 'alquimia')
    if not f and v is not None: L.append(f"**{E['lugares'][lid]['nome']}:** {oficio.nome_banca('alquimia', v)} · a leva Comum: 1 bloco pesado, 4 de matéria, rende 2 doses (`alquimia.py pede cura Comum`)")
    if mao or oficio.bancada(p, 'alquimia'): L.append(f"Mão de alquimia: {T.MAESTRIAS[mao]} ({tantos(oficio.bancada(p, 'alquimia'), 'bloco')} de botica)")
    for oid, o in oficio.obras_de(E, pid).items():
        if o['tipo'] == 'leva': L.append(f"Leva aberta {oid}: {o.get('nome')}, {o['blocos']} de {o['pede']} blocos, {estado.em(E, o['lugar'])} (`alquimia.py continua {oid}`)")
    if pocoes or elix: L.append('Poções: ' + ', '.join(pocoes + elix))
    n = estado.hoje(E, p, 'doses'); cur = estado.hoje(E, p, 'curado'); lim = T.doses_dia(p['atributos']['Vigor'])
    if pocoes or elix or n or cur: L.append(f"Hoje: {tantos(n, 'poção bebida', 'poções bebidas')} de {lim} sem enjoar · cura recebida {cur} de {int(estado.pv_max(p) * T.CURA_TETO)} (o teto do dia)"
                                            + (f" · a ferida mais funda é {T.CATS[p['funda']]}: a poção de baixo vale um terço" if p.get('funda') else ''))
    m = (p.get('marca') or {})
    if isinstance(m.get('guarda'), dict) and m['guarda'].get('ate', 0) > estado.agora(E): L.append(f"A poção de guarda vale amuleto {T.CATS[m['guarda']['cat']]} até o bloco seguinte.")
    if isinstance(m.get('enjoo'), dict) and m['enjoo'].get('ate', 0) > estado.agora(E): L.append('ENJOADO: −2 em tudo até o bloco seguinte.')
    if f and L: L.insert(0, f"**{p['nome']} está fora, {estado.em(E, f)}:** lá não há botica; bebe-se o que se leva.")
    return L


def mesa(E):
    pid = estado.eu(E)
    if not pid or E['gente'][pid]['estado'] != 'vivo': return []
    L = ver(E, pid)
    return ['## A botica e as poções'] + L if L else []


# ---------- a linha de comando ----------
def main(a=None):
    a = sys.argv[1:] if a is None else list(a)
    op = dict(x.split('=', 1) for x in a if '=' in x); pos = [x for x in a if '=' not in x]
    cmds = ('ver', 'pede', 'fazer', 'continua', 'larga', 'beber', 'lamina', 'jornal', 'botica')
    if not pos or pos[0] not in cmds: print(__doc__); return
    falta = lambda o_que, exemplo: sys.exit(f'{o_que}: `python3 alquimia.py {exemplo}`')
    if pos[0] in ('pede', 'fazer') and len(pos) < 3: falta('diga a poção e a categoria', f'{pos[0]} cura Comum')
    if pos[0] == 'beber' and len(pos) < 2: falta('diga o que beber (a poção com a categoria, ou o id do elixir)', 'beber cura:0')
    if pos[0] == 'jornal' and (len(pos) < 2 or not pos[1].isdigit() or int(pos[1]) < 1): falta('diga quantos blocos, em número inteiro (1 ou mais)', 'jornal 2')
    E = estado.carrega(); pid = op.get('quem') or estado.eu(E)
    if pid not in E['gente']: sys.exit(f'não há a pessoa "{pid}"')
    num = lambda k: int(op[k]) if op.get(k, '').isdigit() else sys.exit(f'{k}= pede um número inteiro (veio "{op[k]}")') if k in op else None
    if pos[0] == 'ver': print('\n'.join(ver(E, pid)) or 'nada de botica nem de poção aqui.'); return
    if pos[0] == 'pede': print(pede(E, pid, pos[1], pos[2])); return
    if pos[0] == 'fazer': out = fazer(E, pid, pos[1], pos[2], blocos=num('blocos'), nucleo=op.get('nucleo'))['texto']
    elif pos[0] == 'continua': out = oficio.continua(E, pid, pos[1] if len(pos) > 1 else None, blocos=num('blocos'))['texto']
    elif pos[0] == 'larga': out = oficio.larga(E, pid, pos[1] if len(pos) > 1 else falta('diga qual leva largar', 'larga o0001'))['texto']
    elif pos[0] == 'beber': out = beber(E, pid, pos[1], alvo=op.get('alvo'), mid=op.get('maldicao'))['texto']
    elif pos[0] == 'lamina': out = lamina(E, pid, pos[1] if len(pos) > 1 else None, cat=op.get('cat'))
    elif pos[0] == 'jornal': out = oficio.jornal(E, pid, int(pos[1]), oficio='alquimia')['texto']
    else:
        if len(pos) < 2 or not (pos[1] == 'nada' or pos[1].isdigit()): falta(f'diga o nível da botica, de 0 ({W.BOTICAS[0]}) a {len(W.BOTICAS) - 1} ({W.BOTICAS[-1]}), ou "nada"', 'botica 1 "como foi"')
        out = poe_botica(E, E['gente'][pid]['lugar'], None if pos[1] == 'nada' else int(pos[1]), como=pos[2] if len(pos) > 2 else '')
    estado.grava(E)                                         # grava ANTES de falar
    print(out)
    print(ato.ultima_linha(E, pid))


if __name__ == '__main__':
    import signal; hasattr(signal, 'SIGPIPE') and signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    main()
