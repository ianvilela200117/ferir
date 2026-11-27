#!/usr/bin/env python3
"""provas_povos.py — MOTOR 10: O BANCO DE PROVAS DOS POVOS (etapa 4b, capítulo 19; as metas: projeto/etapa4b/projeto_b/PROJETO.md, seção 9; o contrato: projeto/ETAPA_4B.md).

A PESSOA COMUM SEGUE IGUAL (CO1 a CO4): o módulo dos povos não toca quem é humano (a MESA, o lutador, a ficha); as cinco lutas de semente fixa saem iguais com a gente
feita pelo caminho dos povos; o humano que nasce pelo povos.nasce tem os mesmos atributos, talentos e dons da vila de teste de hoje; o save do jogador (numa cópia) abre,
o Maro é humano, e a gente de outros povos só se acrescenta (recusa duas vezes).
OS POVOS (PO1 a PO8): a lei (nenhum povo vence o humano de peças iguais acima de 60%, nem abaixo de 40%, em condição nenhuma; contra a arma uma acima, até 15%; o anão
contra o veneno, até o Grande Dom mais 2); a soma dos atributos; a tendência nos talentos; o corpo e a armadura; a coragem contra o pavor; a idade.
As lutas são as do luta.py de verdade, com semente fixa (o mesmo número de lutas dá o mesmo resultado). O número de lutas por linha escala com N (4 × N, no mínimo 400;
a meta pede 4.000: `python3 provas_povos.py 1000`).
Os mundos são de rascunho, na memória (numa pasta temporária); o save do jogador (ensaio/) só é LIDO, numa cópia.
Uso: python3 provas_povos.py [N]      (o provas_mundo.py também roda este banco)
"""
import contextlib, copy, io, os, shutil, sys, tempfile
import tabelas as T
import tabelas_povos as TP
import tabelas_talento as TT
import estado, ato, turno, teste, talento, luta, bichos, oficio, povos
import provas_mundo as PM
from itens import item
from pessoas import veste, ficha, linha, padrao

AQUI = os.path.dirname(os.path.abspath(__file__))
R = 2                       # a categoria Rara: a régua do nível 50
OUTROS = [k for k in TP.POVOS if k != TP.HUMANO]


def lutas(n): return max(400, 4 * n)
def quieto(f, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()): return f(*a, **k)
def recusa(f): return PM.recusa(f)
def gera(E, ef, texto='prova'): return estado.aplica(E, 'gera', ef, texto=texto)
def sn(x): return 'sim' if x else 'NÃO'
def pct(x): return f"{x:.1f}".replace('.', ',')
def pct2(x): return f"{x:.2f}".replace('.', ',')


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


def nasce(E, pid, nome, povo=None, nivel=10, **mais):
    """alguém nasce na vila de prova pelo caminho dos povos (os atributos de um guerreiro mais os do povo, a idade de adulto do povo)"""
    r = dict(nome=nome, nivel=nivel, atributos=dict(Força=60, Agilidade=60, Vigor=60, Vontade=50, Percepção=50, Afinidade=40), lugar='vila', **mais)
    if povo: r = povos.nasce(E, pid, r, povo)
    gera(E, [['pessoa', 'nasce', pid, r]], f'{nome} nasce')


# ---------------------------------------------------------------- A PESSOA COMUM SEGUE IGUAL ----------------------------------------------------------------
def _sem_povos(f):
    """roda f com o módulo dos povos desligado (os outros ganchos seguem)"""
    velho = estado._MODS
    try:
        estado._MODS = [m for m in estado.modulos() if m.__name__ != 'povos']; return f()
    finally: estado._MODS = velho


def _co1(n):
    import vila_teste
    R_ = {}
    E = PM.vila(); R_['a MESA da vila de prova sai igual com e sem o módulo dos povos'] = turno.mesa(E) == _sem_povos(lambda: turno.mesa(E))
    V = vila_teste.cria(talentos=True); R_['a MESA da vila de teste sai igual com e sem o módulo dos povos'] = turno.mesa(V) == _sem_povos(lambda: turno.mesa(V))
    limpos = all('tracos' not in estado.lutador(V, k) and 'coragem' not in estado.lutador(V, k) for k in V['gente'])
    R_['ninguém da vila de teste vai à luta com traço ou coragem de povo'] = limpos
    a = estado.lutador(E, 'eu'); gera(E, [['pessoa', 'eu', 'povo', 'poe', 'humano']]); b = estado.lutador(E, 'eu')
    R_['quem é humano por escrito luta igual a quem não tem o campo'] = a == b and linha(ficha(a)) == linha(ficha(b))
    ruim = [k for k, v in R_.items() if not v]
    return [('CO1 A PESSOA COMUM NÃO MUDA (no banco: o módulo dos povos não toca quem é humano; os três bancos de hoje, provas.py 600, provas_mundo.py e estresse.py 1500, rodam à parte)',
             ' · '.join(R_) if not ruim else 'ERRADO: ' + ' · '.join(ruim), not ruim)]


def _co2(n):
    """as cinco lutas de semente fixa (dados/semente_fixa_sem_magia.txt), com cada pessoa feita pelo caminho dos povos (povos.gerado, humano)"""
    from pessoas import defesa
    g = lambda nome, nivel, molde='guerreiro': povos.gerado(nome, nivel, TP.HUMANO, molde=molde)
    casos = [
        ('iguais', lambda: [veste(g('a', 50), arma=('espada', R), armadura=('malha', R), escudo=R)], lambda: [veste(g('b', 50), arma=('espada', R), armadura=('malha', R), escudo=R)], 'perto'),
        ('arco', lambda: [veste(g('arq', 50, 'arqueiro'), arma=('arco', R), armadura=('couro', R), arma2=('adaga', R))], lambda: [veste(g('inf', 50), arma=('espada', R), armadura=('malha', R), escudo=R)], 'longe'),
        ('lobos', lambda: [veste(g('h', 30), arma=('espada', 1), armadura=('malha', 1), escudo=1)], lambda: bichos.bando('lobo', n=4), 'perto'),
        ('cinco', lambda: [veste(g(f'a{i}', 40), arma=('lança', 1), armadura=('malha', 1)) for i in range(5)], lambda: [veste(g(f'b{i}', 40), arma=('machado', 1), armadura=('couro', 1), escudo=1) for i in range(5)], 'perto'),
        ('serpe', lambda: [veste(g(f'h{i}', 60), arma=('espada', R), armadura=('malha', R), escudo=R) for i in range(4)], lambda: [bichos.bicho('serpe')], 'perto')]
    L = []; escada = luta.ESCADA; luta.ESCADA = False       # (a parte 2, fase 1b) a escada do medo é a mudança de propósito da fase, medida no EF7: o contrato (DESENHO, B0) quer a luta de
    try:                                                  # antes "dado por dado, salvo a escada do medo"; com ela ligada, o cinco contra cinco e a serpe mudam (quem fraquejou fica acuado)
      for nome, a, b, ini in casos:
        luta.semente(777); v = []
        for _ in range(150):
            S = luta.nova(a(), b(), inicio=ini, quieto=True); luta.corre(S); v.append((S['fim'], S['r'], sum(f['pv'] for f in S['L'])))
        L.append(f"{nome} {sum(1 for x in v if x[0] == 'A')} {sum(x[1] for x in v)} {sum(x[2] for x in v)}")
    finally: luta.ESCADA = escada
    f = ficha(veste(g('x', 50), arma=('espada', R), armadura=('malha', R), escudo=R)); L.append(f"ficha {f['arma']['acerto']} {defesa(f)} {f['pvmax']} {f['folmax']}")
    ref = [x for x in open(os.path.join(AQUI, 'dados', 'semente_fixa_sem_magia.txt'), encoding='utf-8').read().split('\n') if x.strip()]
    igual = L == ref
    return [('CO2 A LUTA SEM POVO: as cinco lutas de semente fixa, com cada pessoa feita pelo caminho dos povos (humano), saem iguais às de hoje, número por número (dados/semente_fixa_sem_magia.txt; com a escada do medo desligada, como no B0 da fase 1b)',
             'iguais' if igual else 'DIFERENTES: ' + ' · '.join(L), igual)]


def _registros_da_vila():
    """os registros da gente da vila de teste, como o vila_teste.cria os monta (antes do talento)"""
    import vila_teste as VT
    out = [(pid, dict(nome=nm, nivel=nv, atributos=padrao(nm, nv, molde=mo)['atributos'], lugar='vila', grau_oficio=gr, maestria=dict(ma), treino=VT.treino_da_mao(ma), moedas=pr, sobre=so), None)
           for pid, nm, so, nv, mo, gr, ma, pr, _ in VT.GENTE]
    for k, c in VT.COMECOS.items():
        out.append(('eu', dict(nome=VT.NOMES[k], nivel=VT.NIVEL, atributos=dict(c['atributos']), lugar='vila', grau_oficio=c['grau_oficio'], maestria=dict(c['maestria']), treino=dict(c['treino']),
                               marca=dict(c['marca']), carga=dict(c['carga']), moedas=VT.PRATA, jogador=True, sobre=c['sobre']), 'fio'))
    return out


def _co3(n):
    import vila_teste as VT
    dif = []; extra = set(); tot = 0
    for s in (1, 7):
        E = estado.novo(s); V = VT.cria(semente=s, talentos=True)
        for pid, r, inc in _registros_da_vila():
            a = talento.nasce(E, pid, r, inc); b = talento.nasce(E, pid, povos.nasce(E, pid, r, TP.HUMANO), inc); tot += 1
            if a['atributos'] != b['atributos'] or a.get('talento') != b.get('talento') or a.get('dom') != b.get('dom'): dif.append(f"{r['nome']} (semente {s})")
            extra |= set(b) - set(a)
            if inc is None:
                v = V['gente'][pid]
                if v['atributos'] != b['atributos'] or v.get('talento') != b.get('talento') or (v.get('dom') or None) != (b.get('dom') or None): dif.append(f"{r['nome']} contra a vila de hoje (semente {s})")
    ok = not dif and extra <= {'povo', 'idade'}
    return [('CO3 O HUMANO QUE NASCE: pelo caminho dos povos (povos.nasce humano, depois talento.nasce), a gente da vila de teste e o personagem de cada começo nascem com os mesmos atributos, talentos e dons da vila de hoje, caminho por caminho; '
             'o registro só ganha o povo e a idade',
             f"{tot} nascimentos conferidos em duas sementes: " + ('todos iguais' if not dif else 'DIFERENTES: ' + ', '.join(dif[:6])) + f"; campos a mais: {', '.join(sorted(extra)) or 'nenhum'}", ok)]


def _co4(n):
    src = os.path.join(AQUI, 'ensaio')
    if not os.path.exists(os.path.join(src, 'relogio.json')): return [('CO4 O SAVE DO JOGADOR', 'não há save em ensaio/ para conferir', True)]
    d = tempfile.mkdtemp(prefix='m10_povos_save_'); antes = os.environ.get('MOTOR10_MUNDO')
    try:
        shutil.copytree(src, os.path.join(d, 'save')); os.environ['MOTOR10_MUNDO'] = os.path.join(d, 'save')
        E = estado.carrega(); P0 = estado.valida(E); pid = estado.eu(E); eu = E['gente'][pid]
        humano = povos.de(eu) == TP.HUMANO and 'povo' not in eu and not povos.voce(E)
        if estado.luta_aberta(E):
            return [('CO4 O SAVE DO JOGADOR (numa cópia)', f"abre: {sn(not P0)}; {eu['nome']} é humano: {sn(humano)}; a luta está aberta no save: a gente de outros povos espera ela fechar (o na_vila recusa)", not P0 and humano)]
        ja = E['lugares'].get('vila', {}).get('povos') is not None
        if ja:
            t = recusa(lambda: povos.na_vila(E)) or ''
            return [('CO4 O SAVE DO JOGADOR (numa cópia): abre, o Maro é humano, a gente de outros povos já entrou e não entra duas vezes',
                     f"abre: {sn(not P0)}; {eu['nome']} é humano: {sn(humano)}; recusa a segunda vez: {sn('duas vezes' in t)}", not P0 and humano and 'duas vezes' in t)]
        g0, i0, l0 = copy.deepcopy(E['gente']), copy.deepcopy(E['itens']['itens']), copy.deepcopy(E['lugares'])
        L = quieto(povos.na_vila, E)
        igual_g = all(E['gente'][k] == v for k, v in g0.items()); igual_i = all(E['itens']['itens'][k] == v for k, v in i0.items())
        igual_l = all({c: x for c, x in E['lugares'][k].items() if not (k == 'vila' and c == 'povos')} == v for k, v in l0.items())
        novos_g = sorted(set(E['gente']) - set(g0)); novos_i = len(set(E['itens']['itens']) - set(i0)); novos_l = sorted(set(E['lugares']) - set(l0))
        P1 = estado.valida(E); t = recusa(lambda: povos.na_vila(E)) or ''; mesa = turno.mesa(E)
        na_vila_ = eu['lugar'] == 'vila' and not estado.fora(E, pid)          # a MESA só mostra quem está aqui se o personagem está na vila
        mostra = any(f"{nm} ({s.split(',')[0]}" in mesa for _, nm, _, _, s, *_ in TP.VILA['gente']) if na_vila_ else True
        ok = not P0 and humano and igual_g and igual_i and igual_l and novos_g == sorted(x[0] for x in TP.VILA['gente']) and not novos_l and not P1 and 'duas vezes' in t and mostra
        return [('CO4 O SAVE DO JOGADOR (o ensaio/, numa cópia: nada é escrito nele): abre, o Maro é humano e o estado está inteiro; a gente de outros povos só se acrescenta (o que existia sai igual, campo por campo) '
                 'e recusa entrar duas vezes; a MESA mostra quem chegou',
                 f"abre inteiro: {sn(not P0)}; {eu['nome']} é humano: {sn(humano)}; o que existia sai igual (gente {sn(igual_g)}, peças {sn(igual_i)}, lugares {sn(igual_l)}); "
                 f"chegaram {len(novos_g)} pessoas e {novos_i} peças, nenhum lugar novo; depois: {'inteiro' if not P1 else 'QUEBRADO: ' + P1[0]}; recusa a segunda vez: {sn('duas vezes' in t)}; {len(L)} linhas contadas",
                 ok)]
    finally:
        os.environ.pop('MOTOR10_MUNDO', None)
        if antes is not None: os.environ['MOTOR10_MUNDO'] = antes
        shutil.rmtree(d, ignore_errors=True)


# ---------------------------------------------------------------- A LEI: CADA POVO CONTRA O HUMANO ----------------------------------------------------------------
def _gente(povo, nome, nivel=50, arma=R, arm=R, familia='espada', material='malha', molde='guerreiro', dom=None):
    """um combatente gerado daquele povo, vestido com peças iguais às do rival (o escudo, se a arma é de uma mão e não é de tiro)"""
    p = povos.gerado(nome, nivel, povo, molde=molde)
    if dom: p['dom'] = dict(dom)
    e = arm if T.FAMILIAS[familia]['maos'] == 1 and familia not in ('arco', 'besta') else None
    return veste(p, arma=(familia, arma), armadura=(material, arm), escudo=e)


def duelo(fa, fb, n, semente=7, **kw):
    """a vitória do lado A, em % (o empate vale meio)"""
    luta.semente(semente); va = 0
    for _ in range(n):
        S = luta.nova(fa(), fb(), quieto=True, **kw); luta.corre(S)
        va += 1 if S['fim'] == 'A' else 0 if S['fim'] == 'B' else 0.5
    return 100 * va / n


ESPADA, ADAGA, ARCO = dict(), dict(familia='adaga', material='couro'), dict(familia='arco', material='couro', molde='arqueiro')
LINHAS = [('espada', ESPADA, 'perto', None, 50), ('espada no escuro', ESPADA, 'perto', ['escuro'], 50), ('espada no nível 5', dict(arma=0, arm=0), 'perto', None, 5),
          ('espada no nível 5, no escuro', dict(arma=0, arm=0), 'perto', ['escuro'], 5), ('adaga', ADAGA, 'perto', None, 50), ('adaga no escuro', ADAGA, 'perto', ['escuro'], 50),
          ('arco, de longe', ARCO, 'longe', None, 50), ('arco, de longe, no escuro', ARCO, 'longe', ['escuro'], 50)]
_LEI = {}


def _lei(n):
    """as linhas da lei, medidas uma vez por N (PO1 e PO2 leem daqui)"""
    if n in _LEI: return _LEI[n]
    N = lutas(n); res = {}
    for pv in OUTROS:
        for nome, kw, ini, tempo, nv in LINHAS:
            kw2 = dict(kw, nivel=nv)
            res[(pv, nome)] = duelo(lambda: [_gente(pv, pv, **kw2)], lambda: [_gente(TP.HUMANO, 'o rival', **kw2)], N, inicio=ini, tempo=tempo)
        res[(pv, 'acima')] = duelo(lambda: [_gente(pv, pv)], lambda: [_gente(TP.HUMANO, 'o rival', arma=R + 1)], N, inicio='perto')
    res['dom'] = duelo(lambda: [_gente(TP.HUMANO, 'o do dom', dom={'fio': 2})], lambda: [_gente(TP.HUMANO, 'o gêmeo')], N, inicio='perto')
    _LEI[n] = (N, res); return _LEI[n]


def _tiro_ligado():
    """o luta.py já lê o ESCURO_TIRO (o tiro no escuro de quem vê no escuro)? Até o integrador ligar, o tiro usa a metade do escuro"""
    try: return 'ESCURO_TIRO' in open(os.path.join(AQUI, 'luta.py'), encoding='utf-8').read()
    except OSError: return False


def _po1(n):
    N, res = _lei(n); out = []
    for titulo, linhas in (('PO1a CADA POVO CONTRA O HUMANO DE PEÇAS IGUAIS: espada, adaga e arco de dia; espada e adaga no escuro; nível 5 e 50 (a lei: de 40 a 60% em toda linha; o Grande Dom contra o gêmeo, medido na mesma rodada)',
                            [x[0] for x in LINHAS if x[0] != 'arco, de longe, no escuro']),
                           ('PO1b O ARCO NO ESCURO: o arqueiro que vê no escuro contra o arqueiro humano, de noite (de 40 a 60%; no tiro o escuro pesa inteiro: tabelas_povos.ESCURO_TIRO)', ['arco, de longe, no escuro'])):
        fora = [f"{pv} {nome} {pct(res[(pv, nome)])}%" for pv in OUTROS for nome in linhas if not 40 <= res[(pv, nome)] <= 60]
        faixa = ' · '.join(f"{pv} de {pct(min(res[(pv, x)] for x in linhas))} a {pct(max(res[(pv, x)] for x in linhas))}%" if len(linhas) > 1 else f"{pv} {pct(res[(pv, linhas[0])])}%" for pv in OUTROS)
        deu = f"{faixa} · o Grande Dom contra o gêmeo: {pct(res['dom'])}% ({N} lutas por linha)"
        if fora: deu += ' · FORA DA FAIXA: ' + ', '.join(fora)
        if fora and titulo.startswith('PO1b') and not _tiro_ligado(): deu += ' · o luta.py ainda dá ao tiro a metade do escuro: falta ligar o ESCURO_TIRO (pedido ao integrador)'
        out.append((titulo, deu, not fora))
    return out


def _po2(n):
    N, res = _lei(n); mx = max(res[(pv, 'acima')] for pv in OUTROS)
    return [('PO2 CADA POVO CONTRA O HUMANO COM A ARMA UMA ACIMA (a categoria decide: até 15%)', ' · '.join(f"{pv} {pct(res[(pv, 'acima')])}%" for pv in OUTROS) + f" ({N} lutas por linha)", mx <= 15)]


def _po3(n):
    N = lutas(n); r = {}
    for nome, f in (('humano', lambda: [_gente(TP.HUMANO, 'o humano')]), ('anão', lambda: [_gente('anão', 'o anão')]), ('o Grande Dom', lambda: [_gente(TP.HUMANO, 'o do dom', dom={'fio': 2})])):
        r[nome] = duelo(f, lambda: [bichos.bicho('aranha')], N, inicio='perto')
    ok = r['anão'] <= r['o Grande Dom'] + 2
    return [('PO3 O VENENO: o anão (resiste a veneno) contra a aranha-de-toca, nível 50, espada, malha e escudo Raros (até o Grande Dom contra a aranha mais 2 pontos)',
             ' · '.join(f"{k} {pct(v)}%" for k, v in r.items()) + f" ({N} lutas por linha)", ok)]


# ---------------------------------------------------------------- A SOMA, A TENDÊNCIA, O CORPO, A CORAGEM, A IDADE ----------------------------------------------------------------
def _po4(n):
    import vila_teste as VT, tabelas_magia as TM
    E = estado.novo(1); ruins = []; conta = 0; baixo = 99
    zero = [k for k, r in TP.POVOS.items() if sum((r.get('mods') or {}).values()) != 0]
    bases = [(f'começo {k}', dict(c['atributos'])) for k, c in VT.COMECOS.items()]
    bases += [(f'molde {m} nível {nv}', padrao('x', nv, molde=m)['atributos']) for m in list(T.MOLDES) + list(TM.MOLDES) for nv in (1, 5, 50, 150)]
    for pv in TP.POVOS:
        for nome, at in bases:
            r = povos.nasce(E, 'x', dict(nome='x', atributos=at), pv); conta += 1; baixo = min(baixo, min(r['atributos'].values()))
            if sum(r['atributos'].values()) != sum(at.values()): ruins.append(f'{pv} ({nome})')
    W = PM.vila(); igual = []
    for pv in TP.POVOS:
        pid = 'p_' + pv.replace('-', '_'); r = dict(nome=pid, nivel=50, atributos=padrao(pid, 50)['atributos'], lugar='vila')
        gera(W, [['pessoa', 'nasce', pid, povos.nasce(W, pid, r, pv)]]); d = estado.lutador(W, pid); g = povos.gerado(pid, 50, pv)
        igual.append(d['atributos'] == g['atributos'] and d.get('tracos') == g.get('tracos') and d.get('coragem') == g.get('coragem'))
    gente = [k for k, g in TP.GENTE.items() if any(pv not in TP.POVOS or not 0 <= q <= 1 for pv, q in g.items()) or sum(g.values()) > 1 + 1e-9]
    gente += ['a vila de teste'] if sum(TP.VILA['povos'].values()) > 1 + 1e-9 or any(pv not in TP.POVOS for pv in TP.VILA['povos']) else []
    ok = not zero and not ruins and baixo >= 1 and all(igual) and not gente
    return [('PO4 A SOMA DOS ATRIBUTOS: a do humano, sempre (todos os povos, todos os começos e moldes, do nível 1 ao 150); o lutador de quem nasceu com o povo leva os mesmos números da pessoa gerada daquele povo',
             f"{conta} nascimentos: " + ('a soma igual em todos' if not ruins else 'A SOMA MUDA: ' + ', '.join(ruins[:5])) + (f"; o povo que não soma zero: {', '.join(zero)}" if zero else '')
             + f"; o menor atributo: {baixo}; o lutador igual à pessoa gerada: {sn(all(igual))}; a gente de cada lugar (a página) soma até 1: " + (sn(True) if not gente else 'NÃO: ' + ', '.join(gente)), ok)]


def _po5(n):
    nasc = 20000; E = estado.novo(3); linhas = []; ok = True
    for pv in OUTROS:
        fav, con = TP.POVOS[pv]['a_favor'], TP.POVOS[pv]['contra']
        a = sum(talento._um(E, f'p{i}', fav, povo=pv) >= 1 for i in range(nasc)) / nasc * 100
        c = sum(talento._um(E, f'p{i}', con, povo=pv) <= -1 for i in range(nasc)) / nasc * 100
        ok = ok and 20 <= a <= 25 and 20 <= c <= 25; linhas.append(f"{pv}: {fav} Jeitoso ou melhor {pct(a)}%, {con} Lerdo ou pior {pct(c)}%")
    h = sum(talento._um(E, f'p{i}', 'forja') >= 1 for i in range(nasc)) / nasc * 100
    dif = 0
    for i in range(2000):
        base, _ = talento._sorteia(E, f'q{i}')
        if talento._sorteia(E, f'q{i}', povo=TP.HUMANO)[0] != base: dif += 1
        for pv in OUTROS:
            t, _ = talento._sorteia(E, f'q{i}', povo=pv); fora = {TP.POVOS[pv]['a_favor'], TP.POVOS[pv]['contra']}
            if {k: g for k, g in t.items() if k not in fora} != {k: g for k, g in base.items() if k not in fora}: dif += 1
    ok = ok and 10.5 <= h <= 13.5 and dif == 0
    return [('PO5 A TENDÊNCIA: no caminho a favor, Jeitoso ou melhor de 20 a 25%; no contra, Lerdo ou pior de 20 a 25%; os outros caminhos e o humano saem como hoje, caminho por caminho',
             f"{nasc} nascimentos por povo: " + ' · '.join(linhas) + f" · o humano na forja: {pct(h)}% (hoje, 12%) · 2.000 nascidos conferidos nos outros caminhos: {dif} diferentes", ok)]


def _po6(n):
    E = PM.vila(); E['lugares']['vila']['oficina'] = 1; R_ = {}
    for pid, nome, pv in (('pipa', 'Pipa', 'pequenino'), ('gil', 'Gil', 'gnomo'), ('duro', 'Duro', 'anão')): nasce(E, pid, nome, pv)
    nasce(E, 'bento', 'Bento', maestria={'forja': 4})
    s0 = E['itens']['seq']
    gera(E, [['item', 'nasce', item('armadura', 0, material='malha', dono='pipa')], ['item', 'nasce', item('armadura', 0, material='couro', talhe='miúdo', dono='pipa')],
             ['item', 'nasce', item('armadura', 0, material='malha', talhe='miúdo', dono='eu')], ['item', 'nasce', item('armadura', 0, material='couro', talhe='miúdo', dono='gil')],
             ['item', 'nasce', item('armadura', 0, material='malha', dono='duro')], ['item', 'nasce', item('arma', 0, familia='espada', dono='pipa')], ['item', 'nasce', item('escudo', 0, dono='pipa')]])
    gente_pipa, miuda_pipa, miuda_eu, miuda_gil, gente_duro, espada_pipa, escudo_pipa = (f'i{s0 + k:04d}' for k in range(1, 8))
    t = recusa(lambda: ato.vestir(E, 'pipa', gente_pipa)) or ''
    R_['a armadura de gente na pequenina: recusada, com a frase'] = 'não serve no corpo de Pipa' in t and 'oficio.py ajustar' in t
    R_['a miúda no humano: recusada'] = bool(recusa(lambda: ato.vestir(E, 'eu', miuda_eu)))
    R_['a miúda na pequenina e no gnomo, a de gente no anão: servem'] = not any(recusa(lambda i=i, p=p: ato.vestir(E, p, i)) for p, i in (('pipa', miuda_pipa), ('gil', miuda_gil), ('duro', gente_duro)))
    R_['a arma e o escudo não têm corpo'] = not recusa(lambda: ato.vestir(E, 'pipa', espada_pipa)) and not recusa(lambda: ato.vestir(E, 'pipa', escudo_pipa))
    it = lambda i: E['itens']['itens'][i]          # o gravador troca o registro a cada evento: lê-se sempre de novo
    R_['o povos.serve e o pode_vestir dizem o mesmo que o gravador'] = all(povos.serve(it(i), E['gente'][p]) == estado.serve(it(i), E['gente'][p]) and (povos.pode_vestir(E, p, i) == '') == estado.serve(it(i), E['gente'][p])
                                                                           for p in ('pipa', 'gil', 'duro', 'eu') for i in (gente_pipa, miuda_pipa, miuda_eu, gente_duro, espada_pipa))
    with dado_posto([5]): quieto(oficio.ajustar, E, 'bento', gente_pipa, para='pipa')
    R_['ajustada pelo ferreiro, a de gente serve na pequenina'] = it(gente_pipa).get('talhe') == 'miúdo' and not recusa(lambda: gera(E, [['item', miuda_pipa, 'uso', 'poe', None], ['item', gente_pipa, 'uso', 'poe', 'veste']]))
    with dado_posto([5]): quieto(oficio.ajustar, E, 'bento', miuda_eu, para='eu')
    R_['e a miúda, ajustada, serve no humano'] = it(miuda_eu).get('talhe') is None and not recusa(lambda: gera(E, [['item', 'i0002', 'uso', 'poe', None], ['item', miuda_eu, 'uso', 'poe', 'veste']]))
    R_['o talhe do começo segue o corpo do povo'] = all((povos.talhe(pv) == 'miúdo') == (TP.POVOS[pv]['corpo'] == 'miúdo') for pv in TP.POVOS)
    R_['o estado está inteiro'] = not estado.valida(E)
    ruim = [k for k, v in R_.items() if not v]
    return [('PO6 O CORPO: a armadura de outro corpo é recusada ao vestir, com a frase do ferreiro; ajustada, serve; a arma e o escudo não têm corpo',
             ' · '.join(R_) if not ruim else 'ERRADO: ' + ' · '.join(ruim), not ruim)]


def _p_2d20(k):
    """a chance de dois d20 que explodem somarem k ou menos (até 20 o 20 não entra: quem tira 20 passa de 20)"""
    return sum(1 for a in range(1, 20) for b in range(1, 20) if a + b <= k) / 400


def _po7(n):
    import tabelas_bichos as TB
    cd = TB.PAVOR; foge_ate = cd - T.MORAL_QUEBRA
    conta = {}
    for pv in ('pequenino', TP.HUMANO):
        f = ficha(veste(povos.gerado('x', 50, pv), arma=('espada', R), armadura=('malha', R), escudo=R)); bon = f['vontade_b'] + f.get('coragem', 0) + T.MORAL_MAIS
        foge = _p_2d20(foge_ate - bon) * 100; fraq = (_p_2d20(cd - 1 - bon) - _p_2d20(foge_ate - bon)) * 100; conta[pv] = (foge, fraq)
    try:
        rival = (lambda: [__import__('dragoes').dragao('serra', 'jovem')]); quem = 'o dragão jovem da serra'
        d0 = rival()[0]
        if 'apavora' not in ((d0.get('bicho') or {}).get('tracos') or d0.get('tracos') or []): raise SystemExit('o jovem não apavora')      # o lutador do dragão leva os traços no bicho
    except SystemExit: rival = (lambda: [bichos.bicho('dragão')]); quem = 'o dragão do capítulo 6 (o jovem que apavora ainda não existe: frente D)'
    vezes = 2000; fugiu = abalou = 0; luta.semente(11)
    grupo = lambda: [veste(povos.gerado('Pipa', 50, 'pequenino'), arma=('espada', R), armadura=('malha', R), escudo=R)] + [veste(povos.gerado(f'h{i}', 50), arma=('espada', R), armadura=('malha', R), escudo=R) for i in range(3)]
    for _ in range(vezes):
        S = luta.nova(grupo(), rival(), inicio='perto'); luta._abre_rodada(S)          # só o começo da luta: o teste do pavor (lido no registro da luta: o que vem depois é outro susto)
        fugiu += any(x.strip().startswith(('Pipa FOGE (o pavor', 'Pipa SE RENDE (o pavor')) for x in S['log']); abalou += any(x.strip().startswith('Pipa FRAQUEJA (o pavor') for x in S['log'])
    medido = 100 * fugiu / vezes
    ok = conta['pequenino'][0] <= 6 and medido <= 6
    return [('PO7 A CORAGEM CONTRA O PAVOR: o pequenino de nível 50 (coragem +4), num grupo de quatro contra o que apavora, foge até 6% (a conta exata e 2.000 começos de luta)',
             f"a conta: o pequenino foge {pct2(conta['pequenino'][0])}% e fraqueja {pct2(conta['pequenino'][1])}%; o humano foge {pct2(conta[TP.HUMANO][0])}% e fraqueja {pct2(conta[TP.HUMANO][1])}% · "
             f"medido contra {quem}: o pequenino foge {pct(medido)}% e fraqueja {pct(100 * abalou / vezes)}%", ok)]


def _vila_nova(povo, semente=1):
    """a vila nova com o personagem de outro povo, como o vila_teste.py PASTA povo= fará: povos.nasce, depois talento.nasce; as peças do começo no talhe do povo"""
    E = estado.novo(semente)
    E['lugares']['vila'] = dict(nome='a Vila de Prova', em='na Vila de Prova', tipo='vila', cama=True, estoque=dict(comida=2000, prata=2000))
    r = dict(nome='Pipa', nivel=5, atributos=dict(Força=70, Agilidade=60, Vigor=70, Vontade=50, Percepção=50, Afinidade=40), lugar='vila', grau_oficio='diarista',
             maestria={'espada': 2}, treino={'espada': 40}, moedas=30, jogador=True)
    r = talento.nasce(E, 'eu', povos.nasce(E, 'eu', r, povo), 'fio')
    estado.aplica(E, 'gera', [['pessoa', 'nasce', 'eu', r]], texto='o personagem nasce')
    tl = povos.talhe(povo); s0 = E['itens']['seq']
    estado.aplica(E, 'gera', [['item', 'nasce', item('arma', 0, 'Espada de Pipa', familia='espada', dono='eu')], ['item', 'nasce', item('armadura', 0, 'Malha de Pipa', material='malha', dono='eu', **({'talhe': tl} if tl else {}))]], texto='as peças')
    estado.aplica(E, 'gera', [['item', f'i{s0 + 1:04d}', 'uso', 'poe', 'arma'], ['item', f'i{s0 + 2:04d}', 'uso', 'poe', 'veste']], texto='veste')
    return E


def _po8(n):
    R_ = {}; E = estado.novo(5); fora = []
    for pv, r in TP.POVOS.items():
        a, _, mx = r['vida']
        for i in range(200):
            x = povos.nasce(E, f'p{i}', dict(nome='x', atributos=dict(padrao('x', 5)['atributos'])), pv)['idade']
            if not a < x <= a + TP.IDADE_DADO or x > mx: fora.append(f'{pv} {x}')
    R_['quem nasce agora tem a idade de adulto do povo mais um d10'] = not fora
    W = PM.vila(); nasce(W, 'nena', 'Nena', 'pequenino')
    R_['o gravador recusa a idade acima do povo'] = bool(recusa(lambda: gera(W, [['pessoa', 'nena', 'idade', 'poe', TP.POVOS['pequenino']['vida'][2] + 1]])))
    q = copy.deepcopy(W); q['gente']['nena']['idade'] = TP.POVOS['pequenino']['vida'][2] + 1
    R_['o valida acusa quem vive mais que o povo'] = any('não vive' in x for x in estado.valida(q))
    import vila_teste as VT
    V = VT.cria(talentos=True); quieto(povos.na_vila, V)
    R_['a gente de outros povos da vila de teste tem idade de vivo'] = all(V['gente'][k]['idade'] <= TP.POVOS[V['gente'][k]['povo']]['vida'][2] for k, *_ in TP.VILA['gente']) and not estado.valida(V)
    ok_novo = []
    for pv in TP.POVOS:
        N_ = _vila_nova(pv); eu = N_['gente']['eu']; a = TP.POVOS[pv]['vida'][0]; m = turno.mesa(N_)
        ok_novo.append(eu.get('povo') == pv and a < eu['idade'] <= a + TP.IDADE_DADO and not estado.valida(N_) and f"Do povo dos {TP.PLURAL[pv]}, {eu['idade']} anos" in m
                       and (N_['itens']['itens']['i0002'].get('talhe') == povos.talhe(pv)))
    R_['a vila nova com o personagem de cada povo: o povo, a idade, as peças do corpo dele, a linha do Você'] = all(ok_novo)
    ruim = [k for k, v in R_.items() if not v]
    return [('PO8 A IDADE: ninguém vivo passa do máximo do povo; a vila nova dá ao personagem a idade de adulto do povo (mais um d10)',
             ' · '.join(R_) if not ruim else 'ERRADO: ' + ' · '.join(ruim) + (f" ({', '.join(fora[:4])})" if fora else ''), not ruim)]


# ---------------------------------------------------------------- o banco ----------------------------------------------------------------
METAS = (_co1, _co2, _co3, _co4, _po1, _po2, _po3, _po4, _po5, _po6, _po7, _po8)


def provas(n=300):
    """as metas dos povos: a lista de (nome, o que deu, passa). Roda num MOTOR10_MUNDO temporário (nada se grava em mundo nenhum)"""
    d = tempfile.mkdtemp(prefix='m10_povos_'); antes = os.environ.get('MOTOR10_MUNDO'); os.environ['MOTOR10_MUNDO'] = d; res = []
    try:
        for f in METAS:
            try: res += f(n)
            except SystemExit as x: res.append((f.__name__.strip('_').upper(), f'RECUSADO NO MEIO: {x}', False))
    finally:
        os.environ.pop('MOTOR10_MUNDO', None)
        if antes is not None: os.environ['MOTOR10_MUNDO'] = antes
        shutil.rmtree(d, ignore_errors=True)
    return res


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    print(f'BANCO DE PROVAS DOS POVOS (etapa 4b; {lutas(n)} lutas por linha)\n')
    res = provas(n)
    for nome, deu, passa in res: print(f"  {'passa' if passa else 'FALHA'}  {nome}: {deu}")
    print(f'\n{sum(p for _, _, p in res)} de {len(res)} provas passam.')
    return all(p for _, _, p in res)


if __name__ == '__main__':
    sys.exit(0 if main() else 1)
