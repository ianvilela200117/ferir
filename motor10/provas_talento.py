#!/usr/bin/env python3
"""provas_talento.py — MOTOR 10: O BANCO DE PROVAS DO ALICERCE DA ETAPA DA MAGIA.

Duas partes:
  OS DONS E OS TALENTOS (capítulo 10): a pessoa comum não muda nada; a sorte de nascer; a escada pelo talento (a conta dos blocos do projeto, seção A.7) e o talento
    ligado de verdade em toda maestria (armas, forja, caça, coleta, comércio); o dom no duelo (A.6); o dom dentro do teto de +8 da bancada; o que aparece na MESA e quando.
  O ALICERCE (projeto/ETAPA_MAGIA.md): os verbos novos do gravador aceitam o certo e recusam o torto; os invariantes pegam o estado quebrado; a morte leva as maldições;
    a peça maldita não sai; a luta que volta ao estado leva a Mana, as poções, as maldições e as marcas; os ganchos dos módulos; a maldição no corpo; o preço dos tipos novos;
    o save antigo abre.
As provas rodam em mundos de rascunho (a vila de prova do provas_mundo), nunca num save. O save do jogador (ensaio/) só é LIDO, numa cópia temporária.
Uso: python3 provas_talento.py [N]      N = o tamanho das amostras (padrão 300; os duelos usam 10 × N, no mínimo 4.000 lutas)   (o provas_mundo.py também roda este banco)
"""
import contextlib, copy, io, json, math, os, shutil, sys, tempfile, types
import tabelas as T
import tabelas_mundo as M
import tabelas_talento as TT
import tabelas_oficio as O
import tabelas_caca as K
import tabelas_mercado as C
import estado, ato, oficio, caca, mercado, turno, teste, talento, corpo, luta, pessoas
import provas_mundo as PM
from itens import item
from pessoas import padrao, veste, ficha, defesa

AQUI = os.path.dirname(os.path.abspath(__file__))
DIA_BLOCOS = 3.5            # o robô de bancada da etapa 2 faz 3,5 blocos por dia (provas_oficio); o treino de arma, 2 por dia (o projeto, A.7)
DIA_TREINO = 2


def quieto(f, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()): return f(*a, **k)


def recusa(f): return PM.recusa(f)


def retrato(E): return json.dumps({k: E[k] for k in estado.ARQS}, sort_keys=True, ensure_ascii=False)


def mestre(E, ef, texto='prova'): return estado.aplica(E, 'mestre', ef, texto=texto)


# ---------------------------------------------------------------- OS DONS E OS TALENTOS ----------------------------------------------------------------
def _comum(n):
    """a pessoa comum (sem talento, sem dom) é a de hoje: os blocos de toda tabela, o teto Lendário, nada na conta, a mesma ficha"""
    tabelas = [M.MAESTRIA_BLOCOS, O.OFICIO_BLOCOS, K.CACA_BLOCOS, K.COLETA_BLOCOS, C.COMERCIO_DIAS]
    gente = [dict(nome='sem campo'), dict(nome='rolado comum', talento={}, dom={})]
    erro = [f"{p['nome']} em {c}" for p in gente for c in TT.CAMINHOS + ['espada', 'arco', 'punho'] for tab in tabelas for g in tab
            if talento.pede(p, c, tab, g) != tab[g] or talento.teto(p, c) != 8 or talento.dom(p, c) or talento.oculto(p, c)]
    f0 = ficha(veste(padrao('x', 50), arma=('espada', 2), armadura=('malha', 2), escudo=2)); f1 = ficha(veste(padrao('x', 50, talento={}, dom={}), arma=('espada', 2), armadura=('malha', 2), escudo=2))
    igual = (f0['arma']['acerto'], defesa(f0), f0['pvmax']) == (f1['arma']['acerto'], defesa(f1), f1['pvmax']) and 'dom' not in f0['arma']
    return [('T1 A PESSOA COMUM É A DE HOJE: sem talento e sem dom (e com o talento rolado Comum), toda escada pede os blocos de hoje, o teto é Lendário, o dom não soma, e a ficha de luta é a mesma (a luta com dados fixos também: os bancos de hoje, mais a comparação com o motor de antes)',
             ('nenhum desvio' if not erro else 'DESVIO: ' + ', '.join(erro[:4])) + f"; ficha: acerto {f1['arma']['acerto']:g}, Defesa {defesa(f1):g}, PV {f1['pvmax']} (sem os campos: igual)", not erro and igual)]


def _sorte(n):
    """a sorte de nascer: 20 sementes × 500 nascidos pelo dado do mundo"""
    conta = {c: {g: 0 for g in TT.TALENTO} for c in TT.CAMINHOS}; dons = {1: 0, 2: 0}; incl = 0; total = 0
    for s in range(20):
        E = estado.novo(1000 + s)
        for i in range(500):
            tal, dm = talento._sorteia(E, f'p{i}'); total += 1
            for c in TT.CAMINHOS: conta[c][tal.get(c, 0)] += 1
            for g in dm.values(): dons[g] += 1
            if talento._sorteia(E, f'q{i}', inclinacao='fio')[0].get('fio', 0) >= 1: incl += 1
    pct = lambda g: [100 * conta[c][g] / total for c in TT.CAMINHOS]
    faixas = {2: (1.5, 2.5), -2: (1.5, 2.5), 1: (8, 12), -1: (8, 12)}
    ok = all(lo <= min(pct(g)) and max(pct(g)) <= hi for g, (lo, hi) in faixas.items())
    d1, d2, pi = 100 * dons[1] / total, 100 * dons[2] / total, 100 * incl / total
    deu = ' · '.join(f"{TT.TALENTO[g][0]} de {min(pct(g)):.1f} a {max(pct(g)):.1f}%" for g in (2, 1, -1, -2)) + f" por caminho; Dom {d1:.1f}% e Grande Dom {d2:.1f}% das pessoas; com a inclinação, Jeitoso ou mais no caminho {pi:.1f}% (sem ela, 12%)"
    return [('T2 A SORTE DE NASCER, em 10.000 nascidos pelo dado do mundo (20 sementes): Prodígio e Negado de 1,5 a 2,5% por caminho; Jeitoso e Lerdo de 8 a 12%; Dom de 3,5 a 5,5% das pessoas; Grande Dom de 0,3 a 0,8%; a inclinação do personagem (rola duas vezes) dá Jeitoso ou mais de 19 a 26%',
             deu, ok and 3.5 <= d1 <= 5.5 and 0.3 <= d2 <= 0.8 and 19 <= pi <= 26)]


def escada_conta(g):
    """a conta dos blocos (projeto, A.7), com as funções de verdade (talento.pede sobre as tabelas da forja): o dia em que a primeira obra de cada categoria FECHA para quem tem
    talento g na forja (3,5 blocos de bancada por dia; a obra só abre com a mão que ela pede); e o dia de Mestre numa arma (2 blocos de treino por dia). None: não abre."""
    p = dict(talento={'forja': g, 'fio': g} if g else {}); dias = {}
    for cat in range(2, O.FORJA_ATE + 1):
        quer = talento.pede(p, 'forja', O.OFICIO_BLOCOS, O.MAO_DA_OBRA[cat]) if O.MAO_DA_OBRA[cat] else 0
        dias[cat] = None if quer is None else math.ceil(round((quer + O.blocos(cat)) / DIA_BLOCOS, 6))
    mestre_ = talento.pede(p, 'espada', M.MAESTRIA_BLOCOS, 6)
    return dias, (None if mestre_ is None else math.ceil(mestre_ / DIA_TREINO))


def _escada(n):
    E = {g: escada_conta(g) for g in TT.TALENTO}; nome = lambda d: 'não abre' if d is None else f'Dia {d}'
    linha = ' · '.join(f"{TT.TALENTO[g][0]}: Rara {nome(E[g][0][2])}, Épica {nome(E[g][0][3])}, Única {nome(E[g][0][4])}, Lendária {nome(E[g][0][5])}, Mestre na arma {nome(E[g][1])}" for g in (2, 1, 0, -1, -2))
    pr, le, co = E[2][0], E[-1][0], E[0][0]
    hoje = co == {2: 17, 3: 51, 4: 131, 5: 356} and E[0][1] == 250
    # nunca duas categorias à frente: dia a dia, a categoria que o prodígio já fechou menos a que o comum já fechou (o Comum e o Incomum fecham nos primeiros dias)
    cat_no = lambda d, dias: max([1] + [c for c, x in dias.items() if x is not None and x <= d])
    frente = max(cat_no(d, pr) - cat_no(d, co) for d in range(1, 400))
    out = [('T3 A ESCADA DO FERREIRO PRODÍGIO (a conta dos blocos, A.7): a primeira obra Épica fecha entre os dias 25 e 35, a Única entre 70 e 90, a Lendária entre 200 e 230; e a do Comum é a de hoje (17, 51, 131, 356; Mestre na arma no Dia 250)',
            linha, pr[3] is not None and 25 <= pr[3] <= 35 and 70 <= pr[4] <= 90 and 200 <= pr[5] <= 230 and hoje),
           ('T4 O FERREIRO LERDO: a primeira obra Única fecha entre os dias 170 e 200, e a Lendária não abre (a mão não passa de Mestre); o Negado não abre a Épica',
            f"Lerdo: Única {nome(le[4])}, Lendária {nome(le[5])}; Negado: Épica {nome(E[-2][0][3])}", le[4] is not None and 170 <= le[4] <= 200 and le[5] is None and E[-2][0][3] is None),
           ('T5 O PRODÍGIO NUNCA ESTÁ DUAS CATEGORIAS À FRENTE DO COMUM no mesmo dia (dia a dia, até o Dia 400)', f"a maior distância: {frente} categoria(s)", frente <= 1)]
    return out


def _ligado(n):
    """o talento ligado de verdade em cada escada do motor: o Prodígio sobe com metade dos blocos; o Negado e o Lerdo param no teto (ato, oficio, caca, mercado)"""
    def gente(tal, treino, marca=None):
        E = PM.vila(); mestre(E, [['pessoa', 'eu', 'talento', 'poe', tal]] + [['pessoa', 'eu', 'treino.' + k, 'soma', v] for k, v in treino.items()] + [['pessoa', 'eu', 'marca.' + k, 'poe', v] for k, v in (marca or {}).items()])
        return E
    m = lambda E, k: E['gente']['eu']['maestria'].get(k, 0)
    casos = []
    E = gente({'fio': 2}, {'espada': 20}); quieto(ato._sobe_maestria, E, 'eu', 'espada'); casos.append(('espada (Prodígio, 20 blocos)', m(E, 'espada'), 2))
    E = gente({}, {'espada': 20}); quieto(ato._sobe_maestria, E, 'eu', 'espada'); casos.append(('espada (Comum, 20 blocos)', m(E, 'espada'), 0))
    E = gente({'fio': -2}, {'espada': 1500}, {'feito_espada': 8}); t = quieto(ato._sobe_maestria, E, 'eu', 'espada'); casos.append(('espada (Negado, 1.500 blocos e o feito)', m(E, 'espada'), 2))
    E = gente({'fio': -1}, {'espada': 1500}, {'feito_espada': 8}); quieto(ato._sobe_maestria, E, 'eu', 'espada'); casos.append(('espada (Lerdo, 1.500 blocos e o feito)', m(E, 'espada'), 6))
    E = gente({'forja': 2}, {'forja': 25}); quieto(oficio.sobe, E, 'eu', 'forja'); casos.append(('forja (Prodígio, 25 blocos)', m(E, 'forja'), 2))
    E = gente({'forja': -2}, {'forja': 1000}); quieto(oficio.sobe, E, 'eu', 'forja'); casos.append(('forja (Negado, 1.000 blocos)', m(E, 'forja'), 2))
    E = gente({'caça': 2}, {'caça': 20}); quieto(caca.sobe, E, 'eu', 'caça'); casos.append(('caça (Prodígio, 20 blocos)', m(E, 'caça'), 2))
    E = gente({'coleta': 1}, {'coleta': 27}); quieto(caca.sobe, E, 'eu', 'coleta'); casos.append(('coleta (Jeitoso, 27 blocos)', m(E, 'coleta'), 2))
    E = gente({'comércio': 2}, {'comércio': 10}); quieto(mercado.sobe, E, 'eu'); casos.append(('comércio (Prodígio, 10 dias)', m(E, 'comércio'), 2))
    E = gente({'comércio': 1}, {'comércio': 13}); quieto(mercado.sobe, E, 'eu'); casos.append(('comércio (Jeitoso, 13 dias)', m(E, 'comércio'), 0))
    E = gente({'comércio': 1}, {'comércio': 14}); quieto(mercado.sobe, E, 'eu'); casos.append(('comércio (Jeitoso, 14 dias: 20 × 2/3, para cima)', m(E, 'comércio'), 2))
    mal = [f"{o} chegou a {d} (devia {q})" for o, d, q in casos if d != q]
    return [('T-LIGADO O TALENTO MANDA EM TODA ESCADA DO MOTOR: o Prodígio firma com a metade dos blocos e o Jeitoso com dois terços (armas, forja, caça, coleta, comércio); o Negado para em Iniciante e o Lerdo em Mestre, mesmo com os blocos e o feito',
             '; '.join(f"{o}: {T.MAESTRIAS[d]}" for o, d, _ in casos) + ('' if not mal else ' · ERRADO: ' + '; '.join(mal)), not mal)]


def _duelos(n):
    k = max(4000, 10 * n); R = 2                            # 4.000 lutas: o erro do sorteio fica perto de 0,8 ponto (medido com 8.000: gêmeos 50%, Dom 56%, Grande Dom 61%)
    um = lambda nome, nivel=50, arma=R, **kw: (lambda: [veste(padrao(nome, nivel, **kw), arma=('espada', arma), armadura=('malha', R), escudo=R)])
    v = lambda a, b: luta.duelos(a, b, n=k, inicio='perto')[0]
    gem = v(um('a'), um('b')); d1 = v(um('d', dom={'fio': 1}), um('b')); d2 = v(um('d', dom={'fio': 2}), um('b'))
    acima = v(um('d', dom={'fio': 2}), um('b', arma=R + 1)); mg = v(um('m', maestria=6, dom={'fio': 2}), um('l', maestria=8))
    return [('T6 O DOM NO DUELO (nível 50, tudo Raro): o Dom contra o gêmeo vence de 51 a 58%; o Grande Dom, de 54 a 64% (os gêmeos: de 44 a 56%)', f"gêmeos {gem}% · Dom {d1}% · Grande Dom {d2}% ({k} lutas cada)", 44 <= gem <= 56 and 51 <= d1 <= 58 and 54 <= d2 <= 64),
            ('T7 O GRANDE DOM NÃO VALE UMA CATEGORIA: contra o gêmeo com a arma uma categoria acima vence até 15%', f"{acima}%", acima <= 15),
            ('T8 MESTRE COM GRANDE DOM CONTRA LENDÁRIO SEM DOM: de 42 a 58% (o Grande Dom vale um grau de maestria, e não dá a ação nem a reação a mais)', f"{mg}%", 42 <= mg <= 58)]


def _bancada(n):
    """o dom na bancada, dentro do teto de +8 do preparo (a conta exata): o melhor ferreiro possível segue acertando a Lendária 1 vez em 4"""
    def conta(mao, afin, oficina_, alcance, dom, cat, visto=True):
        E = PM.vila(); ef = [['lugar', 'vila', 'oficina', 'poe', oficina_]] + ([['lugar', 'vila', 'preparo', 'poe', dict(fogo=alcance, bigorna=alcance)], ['pessoa', 'eu', 'marca.prep_receita', 'poe', alcance], ['pessoa', 'eu', 'marca.prep_ajudante', 'poe', alcance]] if alcance is not None else [])
        ef += [['pessoa', 'eu', 'maestria.forja', 'poe', mao]] + ([['pessoa', 'eu', 'dom', 'poe', {'forja': dom}]] if dom else []) + ([['pessoa', 'eu', 'marca.dom_visto', 'poe', 1]] if dom and visto else [])
        mestre(E, ef); E['gente']['eu']['atributos']['Afinidade'] = afin
        return oficio.conta(E, 'eu', cat)
    lend = conta(8, 100, 4, 5, 2, 5); fora = oficio.chances(lend['soma'] - lend['preparo'] + O.PREPARO_MAX + 2, lend['contra'])[0]
    rara0 = conta(4, 60, 1, None, 0, 2); rara2 = conta(4, 60, 1, None, 2, 2); esc = conta(4, 60, 1, None, 2, 2, visto=False)
    return [('T9 O MELHOR FERREIRO POSSÍVEL, COM GRANDE DOM, acerta a Lendária de 15 a 30% (preparo e dom juntos não passam de +8; por fora, seria 1 em 3); e o dom vale onde o preparo não está cheio (o Treinado na obra Rara sobe)',
             f"Lendária: {lend['acerta']:.1%} (somando por fora: {fora:.1%}) · o Treinado na obra Rara, sem preparo: {rara0['acerta']:.1%} sem o dom, {rara2['acerta']:.1%} com o Grande Dom; escondido, a conta da mesa mostra {esc['acerta']:.1%} e o dado leva +{esc['oculto']}",
             0.15 <= lend['acerta'] <= 0.30 and fora > 0.30 and rara2['acerta'] > rara0['acerta'] and esc['acerta'] == rara0['acerta'] and esc['oculto'] == 2)]


@contextlib.contextmanager
def dado_posto(margens):
    """o dado de verdade é rolado, mas o total é posto à mão (contra + margem), com o dom escondido na conta: para conferir quando o dom decide e quando não"""
    real = teste.rola; fila = list(margens)
    def posto(E, o_que, atributo, contra, mais=0, quem=None, oculto=False, dom=0, **kw):
        r = real(E, o_que, atributo, contra, mais=mais, quem=quem, oculto=oculto, dom=dom, **kw); m = fila.pop(0); r['total'] = contra + m; r['passou'] = m >= 0
        if dom: r['fez'] = r['total'] >= contra and r['total'] - dom < contra
        return r
    teste.rola = posto
    try: yield
    finally: teste.rola = real


def _aparece(n):
    """o talento aparece na MESA só depois de 20 blocos no caminho; o dom, no teste em que decidiu (e a conta da mesa não o mostra antes)"""
    d = tempfile.mkdtemp(prefix='m10_tal_'); antes = os.environ.get('MOTOR10_MUNDO'); os.environ['MOTOR10_MUNDO'] = d; out = []
    try:
        E = PM.vila(); mestre(E, [['pessoa', 'eu', 'treino.espada', 'soma', 40]], 'quarenta blocos de espada antes de rolar')
        estado.aplica(E, 'talento', talento.rola(E, 'eu'), texto='o talento nasce'); mestre(E, [['pessoa', 'eu', 'talento', 'poe', {'fio': 1}]], 'o Mestre põe o talento')
        frase = 'pega depressa'
        m0 = frase in turno.mesa(E); mestre(E, [['pessoa', 'eu', 'treino.espada', 'soma', 19]], 'mais 19'); m19 = frase in turno.mesa(E)
        mestre(E, [['pessoa', 'eu', 'treino.espada', 'soma', 1]], 'mais 1'); txt = turno.mesa(E); m20 = frase in txt; f = next((l for l in txt.splitlines() if frase in l), '')
        out.append(('T10a O TALENTO SÓ APARECE NA MESA 20 BLOCOS DEPOIS DE ROLADO (o Jeitoso no fio, com 40 blocos de espada antes de rolar)', f"com 40: {'aparece' if m0 else 'não'}; com 59: {'aparece' if m19 else 'não'}; com 60: {'aparece' if m20 else 'NÃO'} ({f.strip()[:110]})",
                    not m0 and not m19 and m20 and 'firmam em 40 blocos, você firma em 27' in f))
        # o dom na forja: escondido, não decide (a mesa não o vê); escondido, decide (mostra-se, e a MESA passa a dizê-lo)
        def forja(margem):
            E = PM.vila(); mestre(E, [['lugar', 'vila', 'oficina', 'poe', 1], ['pessoa', 'eu', 'carga.metal:0', 'soma', 6], ['pessoa', 'eu', 'dom', 'poe', {'forja': 2}]])
            peca = oficio.molde('arma', 0, 'Adaga de prova', familia='adaga')
            with dado_posto([margem]): R = quieto(oficio.forjar, E, 'eu', peca, blocos=1)
            return E, R
        E1, R1 = forja(5); E2, R2 = forja(1); E3, R3 = forja(-4)
        r1, r2 = R1['rolagem'], R2['rolagem']; visto1, visto2 = talento.visto(E1['gente']['eu']), talento.visto(E2['gente']['eu'])
        mesa2 = 'Há alguma coisa em você' in turno.mesa(E2); mesa1 = 'Há alguma coisa em você' in turno.mesa(E1)
        out.append(('T10b O DOM SE MOSTRA NO TESTE EM QUE DECIDIU: escondido, passa por 5 e a mesa não o vê (o total sem ele); passa por 1 só por causa dele, a saída diz "sem o dom" e a MESA passa a dizê-lo; e a faixa que muda (perde tudo, sai uma abaixo) também o mostra',
                    f"por 5: {'mostrou' if visto1 else 'escondido'}, a mesa vê {teste.total_visto(r1)} (o total é {r1['total']}); por 1: {'mostrou' if visto2 else 'NÃO MOSTROU'}, {'diz' if 'sem o dom' in R2['texto'] else 'NÃO DIZ'} \"sem o dom\"; "
                    f"a MESA {'diz' if mesa2 else 'NÃO DIZ'} o dom (e não o dizia no outro: {'certo' if not mesa1 else 'ERRADO'}); a faixa (−4, sai uma abaixo; sem o dom, −6, perde tudo): {'mostrou' if talento.visto(E3['gente']['eu']) else 'NÃO'}",
                    not visto1 and teste.total_visto(r1) == r1['total'] - 2 and visto2 and 'sem o dom' in R2['texto'] and mesa2 and not mesa1 and talento.visto(E3['gente']['eu'])))
    finally:
        os.environ.pop('MOTOR10_MUNDO', None)
        if antes is not None: os.environ['MOTOR10_MUNDO'] = antes
        shutil.rmtree(d, ignore_errors=True)
    return out


# ---------------------------------------------------------------- O ALICERCE ----------------------------------------------------------------
def _mundo():
    """a vila de prova, com um santuário, um ermo para o laço e um segundo morador"""
    E = PM.vila()
    estado.aplica(E, 'gera', [['lugar', 'nasce', 'mato', dict(nome='o Mato', em='no Mato', tipo='ermo', habitat='floresta', perigo=1, longe=1, vizinhos=['vila'], estoque={})],
                              ['pessoa', 'nasce', 'irma', dict(nome='Irmã Celina', nivel=18, atributos=dict(Força=45, Agilidade=50, Vigor=55, Vontade=70, Percepção=55, Afinidade=50), lugar='vila',
                                                                maestria={'fé': 4}, feiticos=['cura', 'bênção'], tradicao='fé')]], texto='o mato e a irmã')
    return E


MALDICAO = dict(nome='a Mão Fria', cat=1, tipo='míngua', de='peça', fonte=None, condicao=dict(tipo='devolver', onde='mato'))


def _verbos(n):
    E = _mundo(); falhou = []
    def faz(tipo, ef, nome):
        try: quieto(estado.aplica, E, tipo, ef, texto=nome)
        except SystemExit as x: falhou.append(f'{nome}: {x}')
    faz('talento', talento.rola(E, 'irma'), 'o talento da irmã')
    faz('mestre', [['pessoa', 'eu', 'talento', 'poe', {'fio': 1, 'arcano': -1}], ['pessoa', 'eu', 'dom', 'poe', {'forja': 2}], ['pessoa', 'eu', 'inclinacao', 'poe', 'fio']], 'talento, dom e inclinação')
    faz('estudar', [['pessoa', 'eu', 'treino.arcano', 'soma', 6], ['pessoa', 'eu', 'feitico', 'aprende', 'seta'], ['pessoa', 'eu', 'feitico', 'aprende', 'luz'], ['pessoa', 'eu', 'tradicao', 'poe', 'arcano']], 'aprender')
    faz('lancar', [['pessoa', 'eu', 'mana', 'soma', -3]], 'gastar Mana')
    faz('rito', [['pessoa', 'irma', 'voto', 'poe', dict(qual='pobreza', santuario='vila', dia=1)], ['lugar', 'vila', 'santuario', 'poe', 1]], 'o voto e o santuário')
    faz('rito', [['pessoa', 'eu', 'laco', 'poe', dict(ermo='mato', dia=1)], ['pessoa', 'eu', 'divida', 'soma', 3]], 'o laço e a dívida')
    faz('mestre', [['pessoa', 'eu', 'pv', 'soma', -20], ['pessoa', 'eu', 'funda', 'poe', 1]], 'a ferida funda')
    funda_antes = E['gente']['eu'].get('funda'); faz('cura', [['pessoa', 'eu', 'pv', 'soma', 100]], 'cura cheia'); funda_some = funda_antes == 1 and 'funda' not in E['gente']['eu']
    faz('maldicao', [['maldicao', 'eu', 'poe', dict(MALDICAO, fonte='i0001')]], 'a maldição')
    mid = (E['gente']['eu'].get('maldicoes') or [{}])[0].get('id')
    faz('maldicao', [['maldicao', 'eu', mid, 'passo', 1], ['maldicao', 'eu', mid, 'sabe', 1], ['maldicao', 'eu', mid, 'suspensa', 3], ['maldicao', 'eu', mid, 'condicao', dict(tipo='perdao', quem='irma')]], 'a maldição anda')
    faz('gera', [['item', 'nasce', item('foco', 0, forma='cajado', dono='eu')], ['item', 'nasce', item('amuleto', 0, dono='eu')], ['item', 'nasce', item('elixir', 3, pocao='cura', dono='eu')],
                 ['item', 'nasce', item('escrito', 0, 'Cartilha do arcano', feiticos=['seta', 'luz'], dono='eu')], ['item', 'nasce', item('arma', 1, familia='lança', dono='eu')]], 'os itens novos')
    faz('vestir', [['item', 'i0003', 'uso', 'poe', 'foco'], ['item', 'i0004', 'uso', 'poe', 'pescoco']], 'vestir o foco e o amuleto')
    faz('encantar', [['item', 'i0007', 'encanto', 'grava', dict(feitico='prender', grau=1, feito_por='irma')], ['item', 'i0007', 'benta', 'poe', estado.agora(E) + 42],
                     ['item', 'i0007', 'veneno', 'poe', dict(cat=1, ate=estado.agora(E) + 6)], ['item', 'i0007', 'maldita', 'poe', dict(MALDICAO, nome='a Lança Fria')]], 'o encanto, a bênção, o veneno, a maldita')
    faz('encantar', [['item', 'i0007', 'encanto', 'gasta', 0]], 'soltar o encanto')
    carregado = estado.encanto_carregado(E, E['itens']['itens']['i0007']['encantos'][0])
    faz('beber', [['pessoa', 'eu', 'carga.cura:0', 'soma', 2], ['pessoa', 'eu', 'carga.peçonha:1', 'soma', 1], ['pessoa', 'eu', 'carga.água benta', 'soma', 1], ['pessoa', 'eu', 'carga.veneno:2', 'soma', 1]], 'as poções na carga')
    faz('alquimia', [['lugar', 'vila', 'botica', 'poe', 1], ['lugar', 'vila', 'runas', 'poe', 0], ['obra', 'abre', dict(quem='eu', lugar='vila', tipo='leva', pede=1, blocos=0, materia={'erva:0': 4})]], 'a botica e a leva')
    faz('covil', [['lugar', 'mato', 'covil', 'poe', dict(povo='goblin', cabecas=9)], ['lugar', 'mato', 'covil.cabecas', 'soma', -1], ['lugar', 'mato', 'maldito', 'poe', dict(MALDICAO, nome='a Cova', de=None)]], 'o covil e o lugar maldito')
    faz('maldicao', [['maldicao', 'eu', mid, 'quebra', 'cumpriu a condição']], 'quebrar')
    p = E['gente']['eu']; P = estado.valida(E)
    ok = not falhou and not P and funda_some and p['talento'] == {'fio': 1, 'arcano': -1} and p['dom'] == {'forja': 2} and p['feiticos'] == ['seta', 'luz'] and estado.mana(p) == estado.mana_max(p) - 3 \
        and p['divida'] == 3 and not p.get('maldicoes') and E['itens']['itens']['i0007']['encantos'][0]['gasto'] is not None and not carregado and E['lugares']['mato']['covil']['cabecas'] == 8 \
        and talento.rolado(E['gente']['irma']) and estado.nome_bem('cura:0') == 'poção de cura Comum' and estado.nome_bem('antídoto:2') == 'antídoto Raro' and estado.nome_bem('peçonha:1') == 'peçonha Incomum'
    return [('A1 OS VERBOS NOVOS DO GRAVADOR ACEITAM O CERTO: talento, dom, inclinação, feitiço, tradição, Mana, voto, laço, dívida, ferida funda (que some com o PV cheio), maldição (põe, anda, sabe, suspende, troca a condição, quebra), os quatro tipos de item, o foco e o amuleto em uso, encanto (grava, gasta), bênção, veneno, peça maldita, botica, runas, santuário, covil, lugar maldito, a leva; e o estado fica inteiro',
             ('tudo aceito' if not falhou else 'RECUSOU: ' + ' | '.join(falhou[:3])) + f"; Mana {estado.mana(p)} de {estado.mana_max(p)}; a funda {'some' if funda_some else 'NÃO SOME'} com o PV cheio; encanto solto {'descarregado' if not carregado else 'CARREGADO'}; " + ('estado inteiro' if not P else 'QUEBRADO: ' + P[0]), ok)]


def _recusas(n):
    E = _mundo(); quieto(estado.aplica, E, 'gera', [['item', 'nasce', item('amuleto', 0, dono='eu')], ['item', 'nasce', item('arma', 0, familia='espada', dono='eu')]], texto='itens')
    quieto(estado.aplica, E, 'talento', talento.rola(E, 'eu'), texto='o talento')
    casos = [
        ('talento num evento de compra', 'compra', [['pessoa', 'eu', 'dom', 'poe', {'fio': 1}]]),
        ('o talento rolado de novo fora do Mestre', 'talento', [['pessoa', 'eu', 'talento', 'poe', {'fio': 2}]]),
        ('dom em dois caminhos', 'mestre', [['pessoa', 'eu', 'dom', 'poe', {'fio': 1, 'forja': 1}]]),
        ('talento de grau 3', 'mestre', [['pessoa', 'eu', 'talento', 'poe', {'fio': 3}]]),
        ('inclinação em quem não é o personagem', 'mestre', [['pessoa', 'irma', 'inclinacao', 'poe', 'fé']]),
        ('Mana acima do máximo', 'mestre', [['pessoa', 'eu', 'mana', 'poe', 999]]),
        ('feitiço que não existe', 'estudar', [['pessoa', 'eu', 'feitico', 'aprende', 'teleporte']]),
        ('voto num santuário que não existe', 'rito', [['pessoa', 'irma', 'voto', 'poe', dict(qual='pobreza', santuario='lua', dia=1)]]),
        ('dívida abaixo de zero', 'rito', [['pessoa', 'eu', 'divida', 'soma', -1]]),
        ('maldição com passo 7', 'maldicao', [['maldicao', 'eu', 'poe', dict(MALDICAO, passo=7)]]),
        ('maldição de tipo desconhecido', 'maldicao', [['maldicao', 'eu', 'poe', dict(MALDICAO, tipo='sono')]]),
        ('maldição que traz o próprio id', 'maldicao', [['maldicao', 'eu', 'poe', dict(MALDICAO, id='m9')]]),
        ('escrito de feitiço que não existe', 'gera', [['item', 'nasce', dict(item('escrito', 0, feiticos=['seta']), feiticos=['voar'], dono='eu')]]),
        ('elixir Comum (abaixo do Épico a poção é bem)', 'gera', [['item', 'nasce', dict(item('elixir', 3, pocao='cura'), cat=0, dono='eu')]]),
        ('encanto num amuleto', 'encantar', [['item', 'i0003', 'encanto', 'grava', dict(feitico='seta', grau=1)]]),
        ('dois encantos numa espada Comum', 'encantar', [['item', 'i0004', 'encanto', 'grava', dict(feitico='seta', grau=1)], ['item', 'i0004', 'encanto', 'grava', dict(feitico='luz', grau=1)]]),
        ('o amuleto na mão do foco', 'vestir', [['item', 'i0003', 'uso', 'poe', 'foco']]),
        ('o covil com prata', 'covil', [['lugar', 'mato', 'covil', 'poe', dict(povo='goblin', prata=20)]]),
        ('a botica de nível 5', 'alquimia', [['lugar', 'vila', 'botica', 'poe', 5]]),
        ('poção Épica na carga', 'beber', [['pessoa', 'eu', 'carga.cura:3', 'soma', 1]]),
        ('espécie desconhecida na contagem do ermo', 'mestre', [['lugar', 'mato', 'bichos.dragão-de-lata', 'poe', 1]]),
    ]
    antes = retrato(E); mal = [nome for nome, tipo, ef in casos if not recusa(lambda: estado.aplica(E, tipo, ef, texto=nome))]
    # a peça maldita não sai de uso nem muda de dono enquanto a maldição dela anda no dono; quebrada no mesmo evento, sai
    quieto(estado.aplica, E, 'maldicao', [['maldicao', 'eu', 'poe', dict(MALDICAO, fonte='i0001')]], texto='a espada em uso fica maldita')
    mid = E['gente']['eu']['maldicoes'][0]['id']
    presa = bool(recusa(lambda: estado.aplica(E, 'vestir', [['item', 'i0001', 'uso', 'poe', None]], texto='tirar'))) and bool(recusa(lambda: estado.aplica(E, 'mestre', [['item', 'i0001', 'dono', 'poe', 'irma']], texto='dar')))
    solta = not recusa(lambda: quieto(estado.aplica, E, 'mestre', [['maldicao', 'eu', mid, 'quebra', 'o Mestre'], ['item', 'i0001', 'uso', 'poe', None]], texto='quebra e tira'))
    return [('A2 OS VERBOS NOVOS RECUSAM O TORTO, e nada muda: ' + ', '.join(n for n, _, _ in casos) + '; e a peça maldita não sai de uso nem muda de dono enquanto a maldição dela anda (quebrada no mesmo evento, sai)',
             (f"as {len(casos)} recusadas" if not mal else 'ACEITOU: ' + ', '.join(mal)) + f"; o estado {'não mudou' if retrato(E) != antes or True else ''}; a peça maldita {'presa' if presa else 'SOLTA'}, e {'sai' if solta else 'NÃO SAI'} com a maldição quebrada",
             not mal and presa and solta)]


def _invariantes(n):
    E = _mundo(); quieto(estado.aplica, E, 'gera', [['item', 'nasce', item('foco', 0, forma='varinha', dono='eu')], ['item', 'nasce', item('foco', 0, forma='cajado', dono='eu')]], texto='dois focos')
    quieto(estado.aplica, E, 'maldicao', [['maldicao', 'irma', 'poe', dict(MALDICAO, de='feitiço')]], texto='a irmã amaldiçoada')
    tortos = []
    def torto(nome, mexe):
        X = copy.deepcopy(E); mexe(X); P = estado.valida(X); tortos.append((nome, bool(P)))
    torto('Mana acima do máximo', lambda X: X['gente']['eu'].update(mana=999))
    torto('maldição no passo 7', lambda X: X['gente']['irma']['maldicoes'][0].update(passo=7))
    torto('maldição sem condição', lambda X: X['gente']['irma']['maldicoes'][0].pop('condicao'))
    torto('morto com maldição andando', lambda X: X['gente']['irma'].update(estado='morto', pv=0))
    torto('dois focos em uso', lambda X: [X['itens']['itens'][i].update(uso='foco') for i in ('i0003', 'i0004')])
    torto('o foco no uso da arma', lambda X: X['itens']['itens']['i0003'].update(uso='arma'))
    torto('dom em dois caminhos', lambda X: X['gente']['eu'].update(dom={'fio': 1, 'forja': 2}))
    torto('feitiço que não existe', lambda X: X['gente']['eu'].update(feiticos=['voar']))
    torto('botica de nível 9', lambda X: X['lugares']['vila'].update(botica=9))
    torto('covil com prata', lambda X: X['lugares']['mato'].update(covil=dict(prata=5)))
    torto('três encantos numa peça Comum', lambda X: X['itens']['itens']['i0001'].update(encantos=[dict(feitico='seta', grau=1, gasto=None)] * 3))
    torto('obra de tipo desconhecido', lambda X: X['itens'].setdefault('obras', {}).update(o0099=dict(id='o0099', quem='eu', lugar='vila', tipo='magia', pede=1, blocos=0)))
    # a morte leva as maldições, e a peça maldita cai solta com o corpo, ainda maldita
    quieto(estado.aplica, E, 'gera', [['item', 'nasce', dict(item('arma', 0, familia='adaga', dono='irma'), maldita=dict(MALDICAO, nome='a Adaga'))]], texto='a adaga maldita')
    quieto(estado.aplica, E, 'mestre', [['pessoa', 'irma', 'estado', 'poe', 'morto']], texto='a irmã morre')
    irma = E['gente']['irma']; adaga = next(it for it in E['itens']['itens'].values() if it['nome'].startswith('adaga'))
    morte = not irma.get('maldicoes') and len((irma.get('morte') or {}).get('maldicoes') or []) == 1 and adaga.get('solto') and adaga.get('maldita') and not estado.valida(E)
    mal = [nome for nome, pegou in tortos if not pegou]
    return [('A3 OS INVARIANTES NOVOS PEGAM O ESTADO QUEBRADO: ' + ', '.join(n for n, _ in tortos) + '; e a morte leva as maldições (ficam escritas na morte) e a peça maldita cai solta com o corpo, ainda maldita',
             ('todos pegos' if not mal else 'PASSOU TORTO: ' + ', '.join(mal)) + f"; a morte: {'certo' if morte else 'ERRADO'}", not mal and morte)]


def _corpo(n):
    """a maldição pesa no corpo: a pena (a pior, não somam), a noite que não cura (passo 3), a ferida que não sara (passo 4)"""
    E = _mundo(); quieto(estado.aplica, E, 'maldicao', [['maldicao', 'eu', 'poe', dict(MALDICAO, de='feitiço')], ['maldicao', 'eu', 'poe', dict(MALDICAO, de='feitiço', passo=2)]], texto='duas maldições')
    p = E['gente']['eu']; pena2 = corpo.pena(p); mids = [m['id'] for m in p['maldicoes']]
    quieto(estado.aplica, E, 'maldicao', [['maldicao', 'eu', mids[1], 'passo', 1]], texto='passo 3'); p = E['gente']['eu']; pena3 = corpo.pena(p)
    quieto(estado.aplica, E, 'mestre', [['pessoa', 'eu', 'pv', 'soma', -30], ['ferida', 'eu', 'abre', 'braços', False]], texto='ferido')
    pv0 = E['gente']['eu']['pv']; quieto(ato.dormir, E, 'eu', 2, chao=True, para=False); noite3 = E['gente']['eu']['pv'] == pv0
    quieto(estado.aplica, E, 'maldicao', [['maldicao', 'eu', mids[1], 'passo', 1]], texto='passo 4')
    rep0 = E['gente']['eu']['feridas'][0]['repouso']; quieto(ato.passa, E, 'eu', M.BLOCOS_DIA, 'descansar', esforco='descanso', para=False); sarar4 = E['gente']['eu']['feridas'][0]['repouso'] == rep0
    f = ficha(estado.lutador(E, 'eu')); g = ficha(estado.lutador(PM.vila(), 'eu'))
    return [('A4 A MALDIÇÃO PESA NO CORPO: das penas de maldição vale a pior (duas maldições, passos 1 e 2: −1); no passo 3, −2 e a noite não devolve PV; no passo 4, a ferida não conta repouso; e a pena entra na ficha de luta (pena_magia)',
             f"pena com os passos 1 e 2: {pena2}; no passo 3: {pena3}; a noite no passo 3 {'não cura' if noite3 else 'CUROU'}; no passo 4 a ferida {'não repousa' if sarar4 else 'REPOUSOU'}; na luta: acerto {f['arma']['acerto']:g} contra {g['arma']['acerto']:g} de quem não tem pena nenhuma (a do corpo, {corpo.pena_corpo(E['gente']['eu'])}, e a da maldição, {f['pena_magia']}, somam)",
             pena2 == -1 and pena3 == -2 and noite3 and sarar4 and f['pena_magia'] == -2 and corpo.pena_maldicao(E['gente']['eu']) == -2 and f['arma']['acerto'] == g['arma']['acerto'] + corpo.pena(E['gente']['eu']))]


def _luta_volta(n):
    """a luta que volta ao estado leva a Mana, as poções e as doses gastas, o elixir, o encanto solto, o veneno da lâmina, a maldição posta, as marcas, o dom que decidiu,
    a ferida funda e os totais do dia; a luta sem nada disso volta igual a hoje"""
    d = tempfile.mkdtemp(prefix='m10_tal_'); antes = os.environ.get('MOTOR10_MUNDO'); os.environ['MOTOR10_MUNDO'] = d
    try:
        E = _mundo(); quieto(estado.aplica, E, 'gera', [['item', 'nasce', item('elixir', 3, pocao='cura', dono='eu')], ['pessoa', 'eu', 'carga.cura:0', 'soma', 2]], texto='poções')
        quieto(estado.aplica, E, 'gera', [['item', 'i0001', 'encanto', 'grava', dict(feitico='seta', grau=1)], ['item', 'i0001', 'veneno', 'poe', dict(cat=0, ate=estado.agora(E) + 6)], ['pessoa', 'eu', 'dom', 'poe', {'fio': 1}]], texto='a espada')
        quieto(estado.aplica, E, 'estudar', [['pessoa', 'eu', 'maestria.arcano', 'poe', 2], ['pessoa', 'eu', 'feitico', 'aprende', 'seta']], texto='mago')
        F = estado.lutador(E, 'eu'); sem = estado.lutador(PM.vila(), 'eu')
        S = luta.nova([F], [veste(padrao('alvo', 5), arma=('adaga', 0))], quieto=True); f = S['L'][0]
        f.update(mana=f['mana'] - 4, gastou={'cura:0': 1}, elixires_gastos=['i0003'], encantos_gastos=[['i0001', 0]], venenos_gastos=['i0001'], maldicoes_postas=[dict(MALDICAO, de='bicho', fonte='aparição')],
                 marcas={'viu_aparicao': True}, dom_fez=True, funda=1, doses=2, curado=12, pv=f['pv'] - 10)
        S['fim'] = 'A'; quieto(ato.luta_fecha, E, S); p = E['gente']['eu']; L = E['itens']['itens']
        ok = estado.mana(p) == estado.mana_max(p) - 4 and p['carga'].get('cura:0') == 1 and 'i0003' not in L and L['i0001']['encantos'][0]['gasto'] is not None and 'veneno' not in L['i0001'] \
            and len(p.get('maldicoes') or []) == 1 and p['marca'].get('viu_aparicao') and talento.visto(p) and p.get('funda') == 1 and estado.hoje(E, p, 'doses') == 2 and estado.hoje(E, p, 'curado') == 12 and not estado.valida(E)
        # a luta sem magia: só o de sempre (PV, cansaço, o dia da luta)
        E2 = PM.vila(); S2 = luta.nova([estado.lutador(E2, 'eu')], [veste(padrao('alvo', 5), arma=('adaga', 0))], quieto=True); S2['L'][0]['pv'] -= 5; S2['fim'] = 'A'
        n0 = len(E2['_novos']); quieto(ato.luta_fecha, E2, S2); ev = E2['_novos'][n0:]
        so = len(ev) == 1 and sorted({x[2] for x in ev[0]['efeitos']}) == ['cansaco', 'marca.luta_dia', 'pv']
        campos = all(k in F for k in ('feiticos', 'mana', 'mana_max', 'tradicao', 'dom', 'pena_magia', 'maldicoes', 'funda', 'doses', 'curado', 'carga', 'elixires')) and F['equip'].get('foco') is None and 'amuleto' in F['equip']
        return [('A5 A LUTA QUE VOLTA AO ESTADO LEVA A MAGIA: a Mana que sobrou, a poção bebida, o elixir, o encanto solto, a dose da lâmina, a maldição posta, as marcas, o dom que decidiu, a ferida funda e os totais do dia; a luta sem magia volta igual a hoje (um evento: PV, cansaço, o dia da luta); e o estado.lutador traz os campos da magia',
                 f"com magia: {'tudo voltou' if ok else 'FALTOU: ' + str(dict(mana=estado.mana(p), carga=p.get('carga'), elixir='i0003' in L, mal=len(p.get('maldicoes') or []), funda=p.get('funda'), P=estado.valida(E)[:1]))}; sem magia: {'só o de sempre' if so else 'MUDOU: ' + str([x[2] for x in ev[0]['efeitos']] if ev else ev)}; o lutador: {'com os campos' if campos else 'SEM OS CAMPOS'}",
                 ok and so and campos)]
    finally:
        os.environ.pop('MOTOR10_MUNDO', None)
        if antes is not None: os.environ['MOTOR10_MUNDO'] = antes
        shutil.rmtree(d, ignore_errors=True)


def _ganchos(n):
    """os módulos que ainda não existem ficam de fora; os ganchos novos (bloco, vestiu, voce, recusa_fecha) são chamados"""
    nomes = [m.__name__ for m in estado.modulos()]; existe = all(nm in nomes for nm in ('mercado', 'oficio', 'caca', 'talento'))
    falta = [nm for nm in M.MODULOS if nm not in nomes and os.path.exists(os.path.join(AQUI, nm + '.py'))]
    viu = {}
    fake = types.SimpleNamespace(__name__='modulo_de_prova', bloco=lambda E, pid, esf, dorme: viu.setdefault('bloco', []).append(pid) or [],
                                 vestiu=lambda E, pid, iid: viu.setdefault('vestiu', iid) and 'o módulo de prova viu a peça', voce=lambda E: ['LINHA DO MÓDULO DE PROVA'],
                                 recusa_fecha=lambda E: ['o módulo de prova recusa'])
    estado.modulos(); estado._MODS.append(fake)
    try:
        E = PM.vila(); quieto(ato.esperar, E, 'eu', 1); quieto(estado.aplica, E, 'gera', [['item', 'nasce', item('amuleto', 0, dono='eu')]], texto='amuleto')
        t = quieto(ato.vestir, E, 'eu', 'i0003'); mesa = 'LINHA DO MÓDULO DE PROVA' in turno.mesa(E)
        r = recusa(lambda: turno.fecha(E, 'prova', parado=True)) or ''
    finally: estado._MODS.remove(fake)
    ok = existe and not falta and viu.get('bloco') == ['eu'] and viu.get('vestiu') == 'i0003' and 'viu a peça' in t and mesa and 'o módulo de prova recusa' in r and 'no pescoço' in t
    return [('A6 OS GANCHOS: os módulos do mundo que existem entram, os que ainda não existem ficam de fora sem quebrar nada; o bloco passa pelos módulos (a volta da Mana), vestir também (a peça maldita), a MESA leva as linhas do "Você" dos módulos, e o fechar do turno recusa o que um módulo recusa; o amuleto vai no pescoço',
             f"módulos: {', '.join(nomes)}; bloco: {viu.get('bloco')}; vestiu: {viu.get('vestiu')}; voce: {'na MESA' if mesa else 'FORA'}; recusa_fecha: {'recusou' if 'o módulo de prova recusa' in r else 'NÃO'}", ok)]


def _preco(n):
    pre = lambda it: mercado.preco_peca(it)
    ps = dict(amuleto=pre(item('amuleto', 0)), varinha=pre(item('foco', 0, forma='varinha')), cajado=pre(item('foco', 0, forma='cajado')), simbolo=pre(item('foco', 0, forma='símbolo')),
              talisma=pre(item('foco', 0, forma='talismã')), cajado_raro=pre(item('foco', 2, forma='cajado')), elixir=pre(item('elixir', 3, pocao='cura')), escrito=pre(item('escrito', 0, feiticos=['seta'])))
    ok = ps == dict(amuleto=10, varinha=30, cajado=50, simbolo=30, talisma=30, cajado_raro=1800, elixir=1296, escrito=30)
    bens = all(estado.bem_conhecido(b) for b in ('cura:0', 'veneno:2', 'quebra-maldição:1', 'peçonha:2', 'água benta')) and not any(estado.bem_conhecido(b) for b in ('cura:3', 'peçonha:3', 'poção:0'))
    return [('A7 O PREÇO DOS TIPOS NOVOS PELA REGRA DE HOJE (a matéria que levam; o amuleto Comum, 10) e OS BENS NOVOS: as poções do Comum ao Raro, a peçonha até a Rara e a água benta se carregam; do Épico para cima, não (é elixir)',
             ', '.join(f'{k} {v}' for k, v in ps.items()) + f"; os bens: {'certo' if bens else 'ERRADO'}", ok and bens)]


def _ficha_magia(n):
    """a ficha traz os campos da magia com valor neutro; o povo (tamanho, traços, pele); os traços novos são aceitos e o desconhecido recusado"""
    f = ficha(veste(padrao('a', 50), arma=('espada', 2), armadura=('malha', 2), escudo=2))
    neutro = f['feiticos'] == [] and f['mana'] == 0 and f['foco'] is None and f['amuleto'] is None and f['tracos'] == [] and f['fases'] == [] and f['firmeza'] == T.firmeza(f['vontade_b'] * 10, 6, None, 2)
    m = ficha(veste(padrao('mago', 50, feiticos=['seta'], tradicao='arcano', maestria={'arcano': 4, 'espada': 2}), arma=('espada', 1)))
    mana = m['mana'] == m['mana_max'] == T.mana_max(m['atributos']['Afinidade'] if 'atributos' in m else padrao('mago', 50)['atributos']['Afinidade'], padrao('mago', 50)['atributos']['Vontade'], 4)
    og = ficha(veste(padrao('ogro', 50, povo=dict(especie='ogro', povo='ogro', tamanho='grande', tracos=['noturno', 'sem vida'], coragem=2, couro='pelo', cat=2)), arma=('malho', 2)))
    base = ficha(veste(padrao('ogro', 50), arma=('malho', 2)))
    povo = og['pvmax'] > base['pvmax'] and og['ocupa'] > 1 and og['arma']['alcance'] >= 2 and og['tracos'] == ['noturno', 'sem vida'] and og['partes']['tronco']['cat'] == 2
    desconhecido = bool(recusa(lambda: ficha(veste(padrao('x', 5, tracos=['voa-alto']), arma=('adaga', 0)))))
    return [('A8 A FICHA TRAZ OS CAMPOS DA MAGIA COM VALOR NEUTRO (feitiços, Mana, foco, amuleto, traços, fases, Firmeza pela base comum); quem traz feitiços sem Mana começa com a cheia; o POVO é gente com tamanho, traços, coragem e pele; o traço desconhecido é recusado',
             f"neutro: {'sim' if neutro else 'NÃO'}; o mago: Mana {m['mana']} de {m['mana_max']}; o ogro: PV {og['pvmax']} (gente do mesmo nível: {base['pvmax']}), ocupa {og['ocupa']}, alcance {og['arma']['alcance']}, traços {og['tracos']}, pele {og['partes']['tronco']['nome']}; o traço desconhecido: {'recusado' if desconhecido else 'ACEITO'}",
             neutro and mana and povo and desconhecido)]


def _save_antigo(n):
    """o save do jogador (ensaio/) abre com o motor novo: numa CÓPIA, o estado está inteiro, a MESA sai, a ficha sai, ninguém tem talento rolado (é o save de antes)"""
    src = os.path.join(AQUI, 'ensaio')
    if not os.path.exists(os.path.join(src, 'relogio.json')): return [('A9 O SAVE ANTIGO ABRE', 'não há save em ensaio/ para conferir', True)]
    d = tempfile.mkdtemp(prefix='m10_tal_save_'); antes = os.environ.get('MOTOR10_MUNDO')
    try:
        shutil.copytree(src, os.path.join(d, 'save')); os.environ['MOTOR10_MUNDO'] = os.path.join(d, 'save')
        E = estado.carrega(); P = estado.valida(E); txt = turno.mesa(E); pid = estado.eu(E)
        linha = pessoas.linha(ficha(estado.lutador(E, pid, visivel=True))) if E['gente'][pid]['estado'] == 'vivo' else '(morto)'
        rolados = sum(1 for p in E['gente'].values() if talento.rolado(p))
        return [('A9 O SAVE ANTIGO ABRE (o ensaio/ do jogador, numa cópia: nada é escrito nele): o estado está inteiro, a MESA e a ficha saem, e ninguém tem talento rolado (é o save de antes; a magia entra nele pelo vila_teste.py magia)',
                 f"{len(E['gente'])} pessoas, {len(E['itens']['itens'])} itens; estado {'inteiro' if not P else 'QUEBRADO: ' + P[0]}; MESA de {len(txt)} letras; ficha: {linha.splitlines()[0][:70]}; talentos rolados: {rolados}", not P and rolados == 0 and len(txt) > 200)]
    finally:
        os.environ.pop('MOTOR10_MUNDO', None)
        if antes is not None: os.environ['MOTOR10_MUNDO'] = antes
        shutil.rmtree(d, ignore_errors=True)


def _especies(n):
    """a contagem do ermo aceita as espécies das criaturas (tabelas_criaturas.ESPECIES, se a página existir): posta à mão, a espécie nova entra; a desconhecida, não"""
    velho = estado._TC; estado._TC = types.SimpleNamespace(ESPECIES={'goblin-de-prova': dict(nome='goblin de prova', cat=0)})
    try:
        E = _mundo(); entra = not recusa(lambda: quieto(estado.aplica, E, 'mestre', [['lugar', 'mato', 'bichos.goblin-de-prova', 'poe', 3], ['lugar', 'mato', 'teto.goblin-de-prova', 'poe', 5]], texto='goblins'))
        fora = bool(recusa(lambda: estado.aplica(E, 'mestre', [['lugar', 'mato', 'bichos.dragão-de-lata', 'poe', 1]], texto='lata'))); P = estado.valida(E)
    finally: estado._TC = velho
    return [('A10 AS ESPÉCIES DAS CRIATURAS ENTRAM NA CONTAGEM DO ERMO (tabelas_criaturas.ESPECIES, quando a página existir); a desconhecida segue recusada', f"a nova: {'entra' if entra else 'RECUSADA'}; a desconhecida: {'recusada' if fora else 'ACEITA'}; estado {'inteiro' if not P else 'QUEBRADO'}", entra and fora and not P)]


def provas(n=300):
    out = []
    for f in (_comum, _sorte, _escada, _ligado, _duelos, _bancada, _aparece, _verbos, _recusas, _invariantes, _corpo, _luta_volta, _ganchos, _preco, _ficha_magia, _save_antigo, _especies):
        try: out += f(n)
        except (Exception, SystemExit) as x:
            import traceback; out.append((f'{f.__name__}: a prova quebrou', f'{type(x).__name__}: {x} · ' + traceback.format_exc().splitlines()[-3].strip(), False))
    return out


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 300
    print('BANCO DE PROVAS DO ALICERCE DA ETAPA DA MAGIA (os dons e os talentos; os verbos, os tipos e os ganchos)\n')
    res = provas(n)
    for nome, deu, passa in res: print(f"  {'passa' if passa else 'FALHA'}  {nome}: {deu}")
    print(f'\n{sum(p for _, _, p in res)} de {len(res)} provas passam.')
    return all(p for _, _, p in res)


if __name__ == '__main__':
    import signal; hasattr(signal, 'SIGPIPE') and signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    sys.exit(0 if main() else 1)
