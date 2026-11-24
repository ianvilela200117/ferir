#!/usr/bin/env python3
"""provas_manha.py, MOTOR 10: O BANCO DE PROVAS DO LADINO (etapa 4b, capítulo 18; o contrato: projeto/ETAPA_4B.md; as metas: projeto/etapa4b/projeto_a/PROJETO.md, seção 12).

As metas do projeto A que são do ladino (MA8 a MA11), com a faixa dada de fora (não se mexe nela para a prova passar: a prova diz o que mediu), e as que guardam o resto da
frente: o dado do ladino (o dom escondido, o povo, a ferramenta que gasta), a gazua na forja e na loja, a armadura miúda na forja, a tocha na loja, o Quim e a loja da vila
(na cópia do save do jogador, nunca nele), as recusas, a MESA de quem não tem nada de novo, e o furto que fica escrito.
  MA8  A GAZUA PELO ITEM: a conta exata (e a tabela do projeto A, a de abrir, achar e arrombar) e 6.000 tentativas com o dado de verdade (manha.testa).
  MA9  A GAZUA E A TOCHA NA LOJA NÃO SÃO MINA: o robô ferreiro de loja do provas_mercado, com a gazua na lista e na prateleira (30 vilas); a tocha e a gazua compradas e
       vendidas de volta perdem; a chave não se vende.
  MA10 O LADINO APRENDE FAZENDO: os robôs de treino (40 blocos o Iniciante; o Jeitoso 27; o Prodígio 20); o Mestre e o Lendário pedem o feito; o bloco da masmorra dá 1;
       o treino em casa pede gazua; o Negado para em Iniciante.
  MA11 O GOLPE PELAS COSTAS (E1 a): o ladino Treinado surpreende o gêmeo; e o de arma uma acima (4.000 lutas, semente fixa).
As provas rodam em mundos de rascunho (a vila de prova do provas_mundo, a vila de teste do vila_teste.py); o save do jogador (ensaio/) só é LIDO, numa cópia temporária.
Uso: python3 provas_manha.py [N]      (N: o tamanho das amostras, 300 de padrão; o provas_mundo.py também roda este banco)
"""
import contextlib, io, json, os, shutil, sys, tempfile
import tabelas as T
import tabelas_mundo as M
import tabelas_manha as TM
import tabelas_mercado as C
import tabelas_oficio as O
import estado, ato, teste, talento, luta, oficio, mercado, manha, turno
import provas_mundo as PM
import provas_mercado as PMC
from itens import item
from pessoas import padrao, veste

AQUI = os.path.dirname(os.path.abspath(__file__))


def quieto(f, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()): return f(*a, **k)


def recusa(f): return PM.recusa(f)
def gera(E, ef, texto='prova'): return estado.aplica(E, 'gera', ef, texto=texto)
def mestre(E, ef, texto='prova'): return estado.aplica(E, 'mestre', ef, texto=texto)
def retrato(E): return json.dumps({k: E[k] for k in estado.ARQS}, sort_keys=True, ensure_ascii=False)
def sn(x): return 'sim' if x else 'NÃO'
def pc(x, casas=0): return f'{100 * x:.{casas}f}%'.replace('.', ',')
def vz(x, casas=2): return f'{x:.{casas}f}'.replace('.', ',').replace('-', '−')


@contextlib.contextmanager
def dado_posto(margens):
    """o dado do jogador rolado de verdade, com o total posto à mão (contra + margem): para conferir o que sai quando passa e quando falha"""
    real = teste.rola; fila = list(margens)
    def posto(E, o_que, atributo, contra, mais=0, quem=None, oculto=False, dom=0, **kw):
        r = real(E, o_que, atributo, contra, mais=mais, quem=quem, oculto=oculto, dom=dom, **kw); m = fila.pop(0); r['total'] = contra + m; r['passou'] = m >= 0
        if dom: r['fez'] = r['total'] >= contra and r['total'] - dom < contra
        return r
    teste.rola = posto
    try: yield
    finally: teste.rola = real


def nasce(E, pid, nome, atributos=None, **mais):
    at = dict(Força=60, Agilidade=60, Vigor=60, Vontade=50, Percepção=50, Afinidade=40); at.update(atributos or {})
    gera(E, [['pessoa', 'nasce', pid, dict(nome=nome, nivel=10, atributos=at, lugar='vila', **mais)]], f'{nome} nasce')


def da_gazua(E, pid, cat=0):
    """uma gazua nova na mão de alguém (o gerador): devolve o id"""
    gera(E, [['item', 'nasce', item('gazua', cat, dono=pid)]], 'a gazua de prova'); return f"i{E['itens']['seq']:04d}"


def empunha(E, pid, familia, cat=0):
    gera(E, [['item', 'nasce', item('arma', cat, familia=familia, dono=pid)]], 'a arma de prova'); iid = f"i{E['itens']['seq']:04d}"
    gera(E, [['item', iid, 'uso', 'poe', 'arma']], 'empunha'); return iid


# ---------------------------------------------------------------- MA8: A GAZUA PELO ITEM ----------------------------------------------------------------
# a tabela do projeto A (seção 4.3, a conta exata): (quem, o atributo, a mão, as chances em %, da mesma categoria da ferramenta para cima; ou da Comum para cima, no achar)
TAB_GAZUA = [('o Maro (Agilidade 60, Leigo)', 60, 0, [66, 32, 12, 5]), ('a Rute (Agilidade 82, Leiga)', 82, 0, [74, 40, 15, 5]),
             ('o ladino Iniciante (Agilidade 70)', 70, 2, [77, 44, 18, 6]), ('o ladino Treinado (Agilidade 80)', 80, 4, [86, 57, 26, 9]),
             ('o ladino Mestre (Agilidade 90)', 90, 6, [93, 70, 36, 13]), ('o ladino Lendário (Agilidade 100)', 100, 8, [98, 81, 48, 20])]
TAB_ACHAR = [('o Maro (Percepção 50)', 50, 0, [77, 53, 29, 13, 6]), ('o ladino Iniciante (Percepção 60)', 60, 2, [86, 66, 40, 20, 9]),
             ('o ladino Treinado (Percepção 60)', 60, 4, [91, 74, 48, 26, 12]), ('o ladino Mestre (Percepção 70)', 70, 6, [96, 84, 62, 36, 18])]
TAB_ARROMBAR = [('o Maro e o Tomé (Força 70 a 79)', 70, [70, 36, 36, 13, 13]), ('um bruto de Força 100', 100, [81, 48, 48, 20, 20])]      # Comum com maça Comum, Comum no ombro, Incomum com maça, Incomum no ombro, Rara com maça
MA8_FAIXA = dict(mesma=(0.55, 0.75), uma=(0.20, 0.40), duas=(0, 0.15), mestre_duas=(0, 0.40))      # a faixa da meta (projeto A, seção 12): não se mexe
MA8_TENTATIVAS = 6000       # as tentativas com o dado de verdade, repartidas pelas quatro linhas da meta
MA8_FOLGA = 0.05            # o que se viu nas tentativas fica a até tantos pontos da conta exata (o dado de verdade: mais de 3 desvios de folga)


def _conta_do_projeto(n):
    """a conta do manha.chance (a do jogo) bate com a tabela do projeto A, linha por linha (abrir, achar e arrombar)"""
    E = PM.vila(); ruins = []; k = 0
    for nome, ag, mao, quer in TAB_GAZUA:
        k += 1; pid = f'g{k}'; nasce(E, pid, nome, dict(Agilidade=ag), maestria={'manha': mao} if mao else {}); da_gazua(E, pid, 0)
        tem = [round(100 * manha.chance(E, pid, 'gazua', cat=c, vista=False)[0]) for c in range(4)]
        if any(abs(a - b) > 1 for a, b in zip(tem, quer)): ruins.append(f'abrir, {nome}: {tem} (o projeto: {quer})')
    for nome, pe, mao, quer in TAB_ACHAR:
        k += 1; pid = f'a{k}'; nasce(E, pid, nome, {'Percepção': pe}, maestria={'manha': mao} if mao else {})
        tem = [round(100 * manha.chance(E, pid, 'achar', cat=c, vista=False)[0]) for c in range(5)]
        if any(abs(a - b) > 1 for a, b in zip(tem, quer)): ruins.append(f'achar, {nome}: {tem} (o projeto: {quer})')
    for nome, fo, quer in TAB_ARROMBAR:
        k += 1; pid = f'b{k}'; nasce(E, pid, nome, dict(Força=fo)); k += 1; sem = f'b{k}'; nasce(E, sem, nome, dict(Força=fo)); empunha(E, pid, 'maça', 0)
        tem = [round(100 * manha.chance(E, q, 'arrombar', cat=c, vista=False)[0]) for q, c in ((pid, 0), (sem, 0), (pid, 1), (sem, 1), (pid, 2))]
        if any(abs(a - b) > 1 for a, b in zip(tem, quer)): ruins.append(f'arrombar, {nome}: {tem} (o projeto: {quer})')
    linhas = len(TAB_GAZUA) + len(TAB_ACHAR) + len(TAB_ARROMBAR)
    return ('MA8 A CONTA DO LADINO: o manha.chance (a conta exata do 2d20 que rola de novo no 20) bate, a um ponto, com a tabela do projeto A (abrir com a gazua, achar e arrombar, de quem é Leigo ao Lendário)',
            f'{linhas} linhas conferidas, todas iguais' if not ruins else 'DIFERENTE: ' + ' · '.join(ruins), not ruins)


def _gazua_pelo_item(n):
    """MA8: o leigo de Agilidade 60 (a da mesma categoria, uma acima, duas acima) e o Mestre (duas acima): a conta exata, e 6.000 tentativas com o dado de verdade"""
    E = PM.vila(); da_gazua(E, 'eu', 0)
    nasce(E, 'mestre', 'o ladino Mestre', dict(Agilidade=90), maestria={'manha': 6}); da_gazua(E, 'mestre', 0)
    linhas = [('mesma', 'eu', 0), ('uma', 'eu', 1), ('duas', 'eu', 2), ('mestre_duas', 'mestre', 2)]
    cada = max(200, round(MA8_TENTATIVAS * n / 300) // len(linhas)); R = {}
    for k, pid, cat in linhas:
        exata = manha.chance(E, pid, 'gazua', cat=cat, vista=False)[0]; passa = 0
        for _ in range(cada):
            r = manha.testa(E, pid, 'gazua', cat=cat, oculto=True); passa += r['passou']; E['turno']['dados'].clear()
        R[k] = (exata, passa / cada)
    na = all(MA8_FAIXA[k][0] <= R[k][0] <= MA8_FAIXA[k][1] for k in R); perto = all(abs(R[k][0] - R[k][1]) <= MA8_FOLGA for k in R)
    diz = lambda k, nome: f"{nome}: {pc(R[k][0])} na conta, {pc(R[k][1], 1)} no dado (a faixa: {pc(MA8_FAIXA[k][0])} a {pc(MA8_FAIXA[k][1])})"
    return ('MA8 A GAZUA PELO ITEM: o leigo de Agilidade 60 abre a fechadura da categoria da gazua de 55 a 75% das vezes, a uma acima de 20 a 40%, a duas acima até 15%; '
            'o Mestre, duas acima, menos de 40% (a conta exata, e as tentativas com o dado de verdade a até 5 pontos dela)',
            f"{cada * len(linhas)} tentativas pelo manha.testa. " + ' · '.join(diz(k, nm) for k, nm in (('mesma', 'o leigo, a mesma'), ('uma', 'uma acima'), ('duas', 'duas acima'), ('mestre_duas', 'o Mestre, duas acima'))),
            na and perto)


# ---------------------------------------------------------------- O DADO DO LADINO ----------------------------------------------------------------
def _dado(n):
    """o testa: a mão e o povo na conta; o dom escondido entra no dado e só se mostra quando decide; o desgaste da ferramenta; a gazua quebrada não conta; o mais barulhento"""
    import povos
    E = PM.vila(); R = {}
    nasce(E, 'lad', 'Lia', dict(Agilidade=70, Percepção=60), maestria={'manha': 4}, dom={'manha': 2}); g = da_gazua(E, 'lad', 0)
    p = E['gente']['lad']
    with dado_posto([0, 5, -5, -4]):
        r0 = manha.testa(E, 'lad', 'gazua', cat=0); r5 = manha.testa(E, 'lad', 'gazua', cat=0); rf = manha.testa(E, 'lad', 'desarmar', cat=0); r4 = manha.testa(E, 'lad', 'gazua', cat=0)
    R['a mão e o povo vão à conta que a mesa vê (o dom escondido, não)'] = r0['mais'] == manha.grau(p) + povos.manha(p, 'gazua') and r0.get('dom') == 2
    R['o dom que decide se mostra (o efeito vai ao evento de quem chamou); o que não decide, não'] = r0['efeitos'] == [['pessoa', 'lad', 'marca.dom_visto', 'poe', E['relogio']['dia']]] and r5['efeitos'] == []
    R['falhar por 5 ou mais entorta a gazua (gasta); por 4, não; passar, não'] = manha.gasta(rf) == [['item', g, 'dur', 'soma', -1]] and rf['falhou_feio'] and manha.gasta(r4) == [] and manha.gasta(r5) == []
    m = empunha(E, 'lad', 'maça', 0)
    with dado_posto([-6]): ra = manha.testa(E, 'lad', 'arrombar', cat=0)
    R['arrombar: a Força e a maça em uso, sem a mão nem o dom; falhar feio gasta a maça'] = ra['atributo'] == 'Força' and ra['mais'] == povos.manha(p, 'arrombar') and not ra.get('dom') and ra['ferramenta'] == m and manha.gasta(ra) == [['item', m, 'dur', 'soma', -1]]
    mestre(E, [['item', g, 'dur', 'soma', -10]], 'a gazua quebra')
    R['a gazua quebrada não conta: sem gazua, um degrau abaixo do Comum'] = manha.gazua_de(E, 'lad') is None and manha.contra(E, 'lad', 'gazua', 0) == (TM.GAZUA[0] + TM.GAZUA[1] * (0 - TM.SEM_GAZUA), None)
    R['escutar: o número de quem chama (a madeira 22, o ferro 26, mais 6 se são mortos)'] = manha.contra_escutar() == 22 and manha.contra_escutar('ferro') == 26 and manha.contra_escutar('madeira', mortos=True) == 28 and manha.contra(E, 'lad', 'escutar', 0) is None
    nasce(E, 'gui', 'Gui', dict(Agilidade=70)); gera(E, [['item', 'nasce', item('armadura', 0, material='malha', dono='gui')]]); gera(E, [['item', f"i{E['itens']['seq']:04d}", 'uso', 'poe', 'veste']])
    q, mais = manha.mais_barulhento(E, ['eu', 'gui']); q2, mais2 = manha.mais_barulhento(E, ['eu', 'gui'], luz=True)
    R['o grupo anda no passo do mais barulhento: a malha tira 3, a luz mais 6'] = q == 'gui' and mais == TM.ESCONDIDO_ARMADURA['malha'] and q2 == 'gui' and mais2 == TM.ESCONDIDO_ARMADURA['malha'] + TM.ESCONDIDO_LUZ
    R['o dado do jogador fica escrito no turno'] = len(E['turno']['dados']) == 5
    import tabelas_povos as TP
    nasce(E, 'gno', 'Gil', dict(Agilidade=70), povo='gnomo'); da_gazua(E, 'gno', 0); real = povos.manha
    with dado_posto([0]): rg = manha.testa(E, 'gno', 'gazua', cat=0)
    povos.manha = lambda p, t, pedra=False: TP.MANHA_TETO + 3
    try:
        with dado_posto([0]): rx = manha.testa(E, 'gno', 'gazua', cat=0)
    finally: povos.manha = real
    R[f"o povo soma no teste do ladino (o gnomo na gazua: +{rg['mais']}), e nunca passa do teto (+{TP.MANHA_TETO})"] = rg['mais'] == min(TP.MANHA_TETO, real(E['gente']['gno'], 'gazua')) and rx['mais'] == TP.MANHA_TETO
    R['o estado segue inteiro'] = not estado.valida(E)
    ruim = [k for k, v in R.items() if not v]
    return ('O DADO DO LADINO (manha.testa): a mão e o +2 do povo na conta; o dom escondido entra no dado e só se mostra quando decide; falhar por 5 ou mais gasta a ferramenta; '
            'a gazua quebrada não conta; o grupo anda no passo do mais barulhento', ' · '.join(R) if not ruim else 'ERRADO: ' + ' · '.join(ruim), not ruim)


# ---------------------------------------------------------------- MA9: A LOJA NÃO É MINA ----------------------------------------------------------------
def _loja_nao_e_mina(n):
    """MA9: o robô ferreiro de loja (provas_mercado) com a gazua na lista e na prateleira, nas mesmas janelas e faixas da meta do mercado de hoje"""
    sementes = max(PMC.MINA_SEMENTES, n // 10); media = lambda L: sum(L) / len(L)
    R = {nome: [PMC.ferreiro_de_loja(s, cats, gazua=True) for s in range(1, sementes + 1)] for nome, cats in (('só peças Comuns', (0,)), ('Comuns e Incomuns', (0, 1)))}
    m5 = {k: media([V['rende'][0] for V in vs]) for k, vs in R.items()}; p5 = {k: max(V['rende'][0] for V in vs) for k, vs in R.items()}; m30 = {k: media([V['rende'][1] for V in vs]) for k, vs in R.items()}
    todas = [V for vs in R.values() for V in vs]; fecha = all(V['prata'] and V['inteiro'] and V['vivo'] for V in todas)
    certo = sementes >= PMC.MINA_SEMENTES and max(m5.values()) <= PMC.MINA_COMECO[0] and max(p5.values()) <= PMC.MINA_COMECO[1] and max(m30.values()) <= PMC.MINA_DEPOIS and fecha
    return ('MA9 A GAZUA NA LOJA NÃO É MINA: o robô ferreiro de loja, com a gazua na lista do que forja e na prateleira, ganha com a forja em média no máximo '
            f'{PMC.MINA_COMECO[0]} de prata por dia nos {PMC.MINA_DIAS[0]} primeiros dias (no pior caso, {PMC.MINA_COMECO[1]}), e no máximo {PMC.MINA_DEPOIS} por dia até o Dia {PMC.MINA_DIAS[1]} (a meta do mercado de hoje)',
            f"{sementes} vilas de teste por escada. " + ' · '.join(f"{k}: {vz(m5[k])} por dia nos {PMC.MINA_DIAS[0]} primeiros (o pior: {vz(p5[k])}), {vz(m30[k])} depois" for k in R)
            + f"; a prata {'fecha' if all(V['prata'] for V in todas) else 'NÃO FECHA'}; estado {'inteiro' if all(V['inteiro'] for V in todas) else 'QUEBRADO'}" + ('' if all(V['vivo'] for V in todas) else f"; MORRERAM {sum(not V['vivo'] for V in todas)}"),
            certo)


def _tocha_e_gazua(n):
    """a tocha (bem) e a gazua (peça) na loja: comprar e vender de volta perde; a virada as gasta e repõe; a chave não se vende; o "vender tudo" não leva a tocha; a prata fecha"""
    E = PMC.vila(prata=200); lid = 'vila'; p0 = mercado.prata_do_mundo(E); R = {}
    txt = mercado.funda_masmorra(E, lid); l = E['lugares'][lid]
    R['a loja abre a tocha no alvo, com a produção no consumo, e uma gazua na prateleira (que entra no alvo da categoria)'] = \
        l['estoque'].get('tocha') == round(C.alvo_dias('tocha') * 400 * C.consumo('tocha')) and l['produz'].get('tocha') == round(400 * C.consumo('tocha'), 4) \
        and sum(1 for it in mercado.prateleira(E, lid).values() if it['tipo'] == 'gazua') == 1 and mercado.alvo_pecas(E, lid).get(0) == C.alvo_pecas('vila')[0] + 1
    c = mercado.comprar(E, 'eu', 'tocha', 20)['prata']; v = mercado.vender(E, 'eu', 'tocha', 20)['prata']
    R[f'comprar 20 tochas ({c}) e vender de volta ({v}) perde {pc(1 - v / c)}'] = v <= (1 - PMC.PERDE) * c
    gz = next(i for i, it in mercado.prateleira(E, lid).items() if it['tipo'] == 'gazua')
    cg = mercado.comprar_peca(E, 'eu', gz)['prata']; vg = mercado.vender_peca(E, 'eu', gz)['prata']
    R[f'a gazua Comum custa {cg} (a da adaga) e a loja a paga {vg} (40%)'] = cg == 10 and vg == 4
    gera(E, [['item', 'nasce', item('chave', 0, 'a chave de prova', abre='vila', dono='eu')]]); ch = f"i{E['itens']['seq']:04d}"
    R['a loja não compra a chave'] = 'chave' in (recusa(lambda: mercado.vender_peca(E, 'eu', ch)) or '')
    mestre(E, [['item', ch, 'some']], 'a chave de prova some')             # (a chave de prova não abre nada que exista: sai do Livro antes de conferir o estado)
    gera(E, [['pessoa', 'eu', 'carga.tocha', 'soma', 3], ['pessoa', 'eu', 'carga.lenha', 'soma', 10]])
    quieto(mercado.vender_cesta, E, 'eu')
    R['o "vender tudo" leva a lenha e deixa a tocha (é de usar)'] = E['gente']['eu']['carga'].get('tocha') == 3 and not E['gente']['eu']['carga'].get('lenha')
    for _ in range(60): quieto(PM.dia_de_rotina, E, trabalha=False)
    f = mercado.fator(E, lid, 'tocha')
    R[f'em 60 dias de virada a tocha fica perto da base (× {vz(f)})'] = PMC.FAIXA_ANO[0] <= f <= PMC.FAIXA_ANO[1]
    gera(E, [['pessoa', 'eu', 'moedas', 'soma', 0]])
    R['a prata fecha (só a do gerador nasceu)'] = mercado.prata_do_mundo(E) == p0
    R['recusa abrir duas vezes, e o lugar sem mercado'] = 'já tem' in (recusa(lambda: mercado.funda_masmorra(E, lid)) or '') and bool(recusa(lambda: mercado.funda_masmorra(PM.vila(), 'vila')))
    R['o estado segue inteiro'] = not estado.valida(E)
    ruim = [k for k, v in R.items() if not v]
    return ('MA9 A TOCHA E A GAZUA NA LOJA: a tocha é bem como os outros (o povo a gasta; o preço sai do estoque), a gazua é peça (vale a da adaga, a loja paga 40%); comprar e vender de volta perde; '
            'a chave não se vende; a prata fecha', ' · '.join(R) if not ruim else 'ERRADO: ' + ' · '.join(ruim), not ruim)


# ---------------------------------------------------------------- A FORJA DA GAZUA E DA ARMADURA MIÚDA ----------------------------------------------------------------
def _forja(n):
    import vila_teste
    E = vila_teste.cria('ferreiro', semente=2); R = {}
    gera(E, [['pessoa', 'eu', 'carga.metal:0', 'soma', 6], ['pessoa', 'eu', 'moedas', 'soma', 100]])
    mats = [oficio.materia_de(oficio.molde('gazua', c)) for c in range(4)]
    R['a gazua pede 1 de metal da categoria (do Épico para cima, metal Raro e um núcleo), e os blocos da forja (1, 3, 9, 27)'] = \
        mats == [{'metal:0': 1}, {'metal:1': 1}, {'metal:2': 1}, {'metal:2': 1}] and [O.blocos(c) for c in range(4)] == [1, 3, 9, 27] and O.pede_nucleo(3) and not O.pede_nucleo(2) \
        and oficio.oficio_de(dict(tipo='gazua')) == 'forja'
    with dado_posto([2]): F = oficio.forjar(E, 'eu', oficio.molde('gazua', 'Comum'))
    gz = F['item']; it = E['itens']['itens'].get(gz) or {}
    R['forjada, a gazua nasce na mão de quem forjou, com a durabilidade da categoria'] = it.get('tipo') == 'gazua' and it.get('dono') == 'eu' and it.get('feito_por') == 'eu' and it['dur'] == [10, 10]
    mestre(E, [['item', gz, 'dur', 'soma', -4]], 'a gazua entorta')
    quieto(oficio.consertar, E, 'eu', gz)
    R['conserta-se na bancada (com metal), como as outras peças'] = E['itens']['itens'][gz]['dur'] == [10, 10]
    R['não se ajusta (não é peça de vestir)'] = 'ajuste' in (recusa(lambda: oficio.ajustar(E, 'eu', gz)) or '')
    with dado_posto([2]): F2 = oficio.forjar(E, 'eu', oficio.molde('armadura', 'Comum', material='malha', cobre=['cabeça'], talhe='miúdo'))
    el = E['itens']['itens'].get(F2['item']) or {}
    R['a armadura forjada para o corpo miúdo nasce miúda (talhe), com a mesma matéria'] = el.get('talhe') == 'miúdo' and 'miúdo' in el.get('nome', '') and oficio.materia_de(oficio.molde('armadura', 0, material='malha', cobre=['cabeça'], talhe='miúdo')) == oficio.materia_de(oficio.molde('armadura', 0, material='malha', cobre=['cabeça']))
    R['a arma e a gazua não têm talhe'] = bool(recusa(lambda: oficio.molde('arma', 0, familia='adaga', talhe='miúdo'))) and bool(recusa(lambda: oficio.molde('gazua', 0, talhe='miúdo')))
    R['a gazua forjada vale na loja o que vale a da prateleira'] = mercado.preco_peca(E['itens']['itens'][gz]) == 10
    R['o estado segue inteiro'] = not estado.valida(E)
    ruim = [k for k, v in R.items() if not v]
    return ('A FORJA DA GAZUA E DA ARMADURA MIÚDA (oficio.py): a gazua se forja como a adaga (1 de metal da categoria, os blocos, o teste e a falha da forja) e se conserta; '
            'a armadura se forja para o corpo miúdo com talhe=miúdo', ' · '.join(R) if not ruim else 'ERRADO: ' + ' · '.join(ruim), not ruim)


# ---------------------------------------------------------------- MA10: O LADINO APRENDE FAZENDO ----------------------------------------------------------------
def _aprende_em_casa(g):
    """o robô de treino: a vila de prova, uma gazua, o talento posto à mão; dorme, come, treina a manha 2 blocos por dia em casa. Devolve os blocos com que chegou a Iniciante"""
    E = PM.vila(); da_gazua(E, 'eu', 0); gera(E, [['pessoa', 'eu', 'moedas', 'soma', 200]])
    if g: mestre(E, [['pessoa', 'eu', 'talento', 'poe', {'manha': g}]], 'o talento de prova')
    for _ in range(40):
        ato.dormir(E, 'eu', 2, para=False); ato.comer(E, 'eu')
        for _ in range(2):
            quieto(manha.treinar, E, 'eu', 1)
            if manha.grau(E['gente']['eu']) >= 2: return manha.blocos_de(E['gente']['eu']), not estado.valida(E)
        ato.passa(E, 'eu', 2, 'esperar', para=False)
    return None, not estado.valida(E)


def _aprende(n):
    R = {}
    bl = {g: _aprende_em_casa(g) for g in (0, 1, 2)}
    R[f"em casa, com a gazua: o Iniciante aos {bl[0][0]} blocos; o Jeitoso aos {bl[1][0]}; o Prodígio aos {bl[2][0]}"] = [bl[g][0] for g in (0, 1, 2)] == [40, 27, 20] and all(bl[g][1] for g in bl)
    E = PM.vila()
    mestre(E, [['pessoa', 'eu', 'maestria.manha', 'poe', 4], ['pessoa', 'eu', 'treino.manha', 'poe', 499]])
    ef = manha.treino(E, 'eu', TM.TREINO_BLOCO); mestre(E, ef); diz = manha.sobe(E, 'eu')
    R['o bloco da masmorra dá 1 de treino; com os blocos do Mestre, sem o feito, a mão não sobe'] = ef == [['pessoa', 'eu', 'treino.manha', 'soma', 1]] and manha.grau(E['gente']['eu']) == 4 and 'falta o feito' in diz
    e1 = manha.feito(E, 'eu', 1); mestre(E, e1); e2 = manha.feito(E, 'eu', 2); mestre(E, e2)
    R['abrir uma Incomum não é o feito do Mestre; a Rara é, e a mão sobe no mesmo evento'] = e1 == [['pessoa', 'eu', 'marca.feito_manha', 'poe', 1]] and e2 == [['pessoa', 'eu', 'marca.feito_manha', 'poe', 2], ['pessoa', 'eu', 'maestria.manha', 'poe', 6]] and manha.grau(E['gente']['eu']) == 6
    mestre(E, [['pessoa', 'eu', 'treino.manha', 'poe', 1500]]); d2 = manha.sobe(E, 'eu'); e3 = manha.feito(E, 'eu', 3)
    R['o Lendário pede a Épica'] = 'falta o feito' in d2 and e3 == [['pessoa', 'eu', 'marca.feito_manha', 'poe', 3], ['pessoa', 'eu', 'maestria.manha', 'poe', 8]] and manha.feito(E, 'eu', 1) == []
    E = PM.vila(); mestre(E, [['pessoa', 'eu', 'treino.manha', 'poe', 39]]); ef = manha.treino(E, 'eu', 1)
    R['o bloco que fecha os 40 blocos já traz a mão (Iniciante)'] = ef == [['pessoa', 'eu', 'treino.manha', 'soma', 1], ['pessoa', 'eu', 'maestria.manha', 'poe', 2]]
    E = PM.vila(); mestre(E, [['pessoa', 'eu', 'talento', 'poe', {'manha': -2}], ['pessoa', 'eu', 'maestria.manha', 'poe', 2], ['pessoa', 'eu', 'treino.manha', 'poe', 1499]])
    ef = manha.treino(E, 'eu', 1); mestre(E, ef); d3 = manha.sobe(E, 'eu')
    R['o Negado para em Iniciante'] = ef == [['pessoa', 'eu', 'treino.manha', 'soma', 1]] and 'para em Iniciante' in d3
    E = PM.vila(); a0 = retrato(E); t0 = estado.agora(E); rz = recusa(lambda: manha.treinar(E, 'eu', 2))
    R['o treino em casa pede gazua (recusa antes de gastar o tempo)'] = 'gazua' in (rz or '') and retrato(E) == a0 and estado.agora(E) == t0
    g = da_gazua(E, 'eu', 0); mestre(E, [['item', g, 'dur', 'soma', -10]]); a1 = retrato(E)
    R['a gazua quebrada não serve ao treino'] = 'gazua' in (recusa(lambda: manha.treinar(E, 'eu', 1)) or '') and retrato(E) == a1
    ruim = [k for k, v in R.items() if not v]
    return ('MA10 O LADINO APRENDE FAZENDO: 40 blocos fazem o Iniciante (o Jeitoso 27, o Prodígio 20); o Mestre pede o feito (abrir ou desarmar uma Rara de verdade) e o Lendário a Épica; '
            'o bloco da masmorra dá 1 de treino; o treino em casa pede gazua; o talento põe o teto', ' · '.join(R) if not ruim else 'ERRADO: ' + ' · '.join(ruim), not ruim)


# ---------------------------------------------------------------- MA11: O GOLPE PELAS COSTAS ----------------------------------------------------------------
MA11_FAIXA = dict(soma=(5, 15), acima=0.80)     # a faixa da meta (projeto A, seção 12): +5 a +15 pontos contra o gêmeo; a arma uma acima vence 80% ou mais
MA11_LUTAS = 4000           # as lutas da meta, repartidas pelas três linhas


def _ladino(manha_):
    return veste(padrao('Ladino', 50, molde='arqueiro', maestria={'espada': T.maestria_tipica(50), 'manha': manha_}), arma=('espada', 2), armadura=('couro', 2))


def _outro(cat_arma=2):
    return veste(padrao('Outro', 50), arma=('espada', cat_arma), armadura=('malha', 2), escudo=2)


def _duelos(fa, fb, n, semente=7, surpresa='B'):
    luta.semente(semente); a = b = 0
    for _ in range(n):
        S = luta.nova([fa()], [fb()], inicio='colado', surpresa=surpresa, quieto=True); luta.corre(S); a += S['fim'] == 'A'; b += S['fim'] == 'B'
    return a / n, b / n


def _costas(n):
    cada = max(400, -(-round(MA11_LUTAS * n / 300) // 3))
    com = _duelos(lambda: _ladino(4), _outro, cada); sem = _duelos(lambda: _ladino(0), _outro, cada); acima = _duelos(lambda: _ladino(4), lambda: _outro(3), cada)
    soma = 100 * (com[0] - sem[0])
    return ('MA11 O GOLPE PELAS COSTAS (E1 a): o ladino Treinado (nível 50, espada e couro Raros) que surpreende o gêmeo (espada, malha e escudo Raros) ganha de 5 a 15 pontos com o golpe; '
            'e quem tem a arma uma acima vence 80% ou mais mesmo pego pelas costas (semente fixa)',
            f"{3 * cada} lutas. Surpreendendo o gêmeo: {pc(com[0], 1)} com a manha de Treinado, {pc(sem[0], 1)} sem ela ({'+' if soma >= 0 else ''}{vz(soma, 1)} pontos); "
            f"contra a espada Épica, o outro vence {pc(acima[1], 1)}",
            MA11_FAIXA['soma'][0] <= soma <= MA11_FAIXA['soma'][1] and acima[1] >= MA11_FAIXA['acima'])


# ---------------------------------------------------------------- O QUIM E A LOJA DA VILA (na_vila) ----------------------------------------------------------------
def _quim_em(E):
    """roda o manha.na_vila no mundo e confere: só eventos do gerador, a prata nova (a do Quim), o Quim com o talento rolado, a loja, a recusa da segunda vez"""
    R = {}; p0 = mercado.prata_do_mundo(E); n0 = E['relogio']['eventos']; t0 = estado.agora(E); antes = {k: dict(v) for k, v in E['gente'].items() if k != 'quim'}
    L = quieto(manha.na_vila, E)
    k = E['relogio']['eventos'] - n0; novos = E['_novos'][-k:] if k > 0 else []
    q = E['gente'].get('quim') or {}; g = manha.gazua_de(E, 'quim'); l = E['lugares']['vila']
    R['o Quim nasce: nível 14, manha de Iniciante (40 blocos), a adaga e o couro em uso, uma gazua Comum'] = q.get('nivel') == 14 and manha.grau(q) == 2 and manha.blocos_de(q) == 40 and bool(g) and g['cat'] == 0 \
        and {it.get('uso') for it in E['itens']['itens'].values() if it.get('dono') == 'quim'} == {'arma', 'veste', None}
    R['nasce com o talento e o dom rolados (os 17 caminhos: nada lhe falta)'] = talento.rolado(q) and talento.falta(q) == []
    R[f"a prata nova é a do Quim ({mercado.prata_do_mundo(E) - p0})"] = mercado.prata_do_mundo(E) - p0 == TM.QUIM['moedas']
    R['a loja ganha a tocha e a gazua'] = l['estoque'].get('tocha', 0) > 0 and bool(l.get('feira_masmorra')) and any(it['tipo'] == 'gazua' for it in mercado.prateleira(E, 'vila').values())
    R['só eventos do gerador, sem o relógio andar; ninguém de antes muda'] = k > 0 and len(novos) == k and all(e['tipo'] == 'gera' for e in novos) and estado.agora(E) == t0 and all(E['gente'][x] == v for x, v in antes.items())
    a1 = retrato(E); rz = recusa(lambda: manha.na_vila(E))
    R['a segunda vez recusa, antes de mudar qualquer coisa'] = bool(rz) and retrato(E) == a1
    R['o estado segue inteiro'] = not estado.valida(E)
    return R, L


def _quim_ja(E):
    """o save que já tem a etapa (o `vila_teste.py fantasia` rodou nele): o Quim está, a loja tem a descida, e a segunda vez recusa sem mudar nada"""
    R = {}; q = E['gente'].get('quim') or {}; l = E['lugares']['vila']
    R['o Quim já está no save (o fantasia rodou nele), com os 17 caminhos rolados'] = bool(q) and talento.rolado(q) and talento.falta(q) == []
    R['a loja já tem a descida (a tocha e a gazua)'] = bool(l.get('feira_masmorra')) and 'tocha' in l['estoque']
    a1 = retrato(E); rz = recusa(lambda: manha.na_vila(E))
    R['a segunda vez recusa, antes de mudar qualquer coisa'] = bool(rz) and retrato(E) == a1
    R['o estado segue inteiro'] = not estado.valida(E)
    return R


def _na_vila(n):
    import vila_teste
    E = vila_teste.cria('guerreiro', semente=4, talentos=True); R, L = _quim_em(E)
    src = os.path.join(AQUI, 'ensaio'); R2 = {}
    if os.path.exists(os.path.join(src, 'relogio.json')):
        d = tempfile.mkdtemp(prefix='m10_manha_save_'); antes = os.environ.get('MOTOR10_MUNDO')
        try:
            shutil.copytree(src, os.path.join(d, 'save')); os.environ['MOTOR10_MUNDO'] = os.path.join(d, 'save')
            E2 = estado.carrega(); R2 = _quim_ja(E2) if 'quim' in E2['gente'] else _quim_em(E2)[0]
        finally:
            os.environ.pop('MOTOR10_MUNDO', None)
            if antes is not None: os.environ['MOTOR10_MUNDO'] = antes
            shutil.rmtree(d, ignore_errors=True)
    ruim = [f'(a vila nova) {k}' for k, v in R.items() if not v] + [f'(a cópia do save) {k}' for k, v in R2.items() if not v]
    return ('O QUIM E A LOJA DA VILA (manha.na_vila, para o `vila_teste.py fantasia`): o ladino da vila nasce, a loja ganha a tocha e a gazua, só por eventos do gerador; '
            'recusa a segunda vez; na vila nova e numa cópia do save do jogador (nada é escrito nele)',
            (' · '.join(R) + (f" · e o mesmo na cópia do save ({len(R2)} conferências)" if R2 else ' · (não há save em ensaio/ para conferir)') + f". A mesa: {L[0][:90]}...") if not ruim else 'ERRADO: ' + ' · '.join(ruim),
            not ruim)


# ---------------------------------------------------------------- A MESA, AS RECUSAS E O FURTO ----------------------------------------------------------------
def _mesa(n):
    import vila_teste
    R = {}
    E = PM.vila()
    R['quem não tem manha nem gazua não ganha linha no "Você" nem no SÓ O MESTRE'] = manha.voce(E) == [] and manha.so_mestre(E) == []
    E = vila_teste.cria('guerreiro', semente=1); txt = turno.mesa(E)
    R['a vila de hoje (sem a etapa) não fala de tocha nem de gazua; a loja de sempre não vende tocha'] = 'tocha' not in txt and 'gazua' not in txt.lower() and 'tocha' not in C.bens() and not E['lugares']['vila']['estoque'].get('tocha')
    da_gazua(E, 'eu', 0); v = manha.voce(E)
    R['com uma gazua, o "Você" diz a mão do ladino e a chance de abrir, achar e arrombar (sem o dom que a pessoa não viu)'] = bool(v) and 'manha' in v[0] and any('chance' in x for x in v)
    ruim = [k for k, v in R.items() if not v]
    return ('A MESA: a de quem não tem nada de novo sai igual; com a gazua ou a manha, o "Você" mostra a mão do ladino e a conta antes de tentar',
            ' · '.join(R) if not ruim else 'ERRADO: ' + ' · '.join(ruim), not ruim)


def _recusas(n):
    E = PM.vila(); da_gazua(E, 'eu', 0); R = {}
    casos = [('treinar zero blocos', lambda: manha.treinar(E, 'eu', 0)), ('treinar com número torto', lambda: manha.treinar(E, 'eu', 'dois')),
             ('o teste que não existe', lambda: manha.testa(E, 'eu', 'voar', cat=0)), ('o teste sem número nem categoria', lambda: manha.testa(E, 'eu', 'gazua')),
             ('o escutar sem o número de quem chama', lambda: manha.testa(E, 'eu', 'escutar', cat=0)), ('a pessoa que não existe', lambda: manha.testa(E, 'ninguem', 'achar', cat=0)),
             ('o furto (etapa 3)', lambda: manha.main(['furtar', 'lino'])), ('a vila sem mercado (o Quim e a loja)', lambda: manha.na_vila(E)),
             ('o grupo vazio no andar escondido', lambda: manha.mais_barulhento(E, []))]
    for nome, f in casos:
        a = retrato(E); rz = recusa(f); R[nome] = bool(rz) and retrato(E) == a
    ruim = [k for k, v in R.items() if not v]
    return ('AS RECUSAS: o que não pode não acontece, com a frase, antes de mudar qualquer coisa (o treino sem número, o teste torto, o furto, a vila sem loja, o grupo vazio)',
            f"{len(R)} recusas, todas com a frase e sem mudar nada" if not ruim else 'NÃO RECUSOU (ou mudou algo): ' + ' · '.join(ruim), not ruim)


def _furto(n):
    rz = recusa(lambda: manha.main(['furtar', 'dalva'])) or ''
    ok = not TM.FURTO_LIGADO and 'etapa 3' in rz and set(TM.FURTO) == {'contra', 'guarda', 'leva', 'pena', 'preso_dias'}
    return ('O FURTO FICA ESCRITO E DESLIGADO (o juízo: entra na etapa 3, com a gente que lembra e a vila com justiça): os números estão na página, e o comando recusa com a frase',
            f"desligado: {sn(not TM.FURTO_LIGADO)}; a frase: {rz[:110]}...", ok)


def provas(n=300):
    out = []
    for f in (_conta_do_projeto, _gazua_pelo_item, _dado, _loja_nao_e_mina, _tocha_e_gazua, _forja, _aprende, _costas, _na_vila, _mesa, _recusas, _furto):
        try: out.append(f(n))
        except (Exception, SystemExit) as x:
            import traceback; out.append((f'{f.__name__}: a prova quebrou', f'{type(x).__name__}: {x} · ' + ' | '.join(traceback.format_exc().splitlines()[-4:-1]).strip(), False))
    return out


def main():
    a = sys.argv[1:]
    if a and not a[0].isdigit(): print(__doc__); return True
    n = int(a[0]) if a else 300
    print('BANCO DE PROVAS DO LADINO · etapa 4b: a manha, a gazua, a tocha, o Quim\n')
    res = provas(n)
    for nome, deu, passa in res: print(f"  {'passa' if passa else 'FALHA'}  {nome}: {deu}")
    print(f'\n{sum(p for _, _, p in res)} de {len(res)} provas passam.')
    return all(p for _, _, p in res)


if __name__ == '__main__':
    import signal; hasattr(signal, 'SIGPIPE') and signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    sys.exit(0 if main() else 1)
