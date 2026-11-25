#!/usr/bin/env python3
"""provas_3.py — MOTOR 10: O BANCO DE PROVAS DO ALICERCE DA ETAPA 3 (a região que responde; o contrato: projeto/ETAPA_3.md).

O que o alicerce (onda 1) entregou, conferido aqui:
  O GRAVADOR POR TOQUE (o mesmo estado e o mesmo registro, byte a byte, que o gravador inteiro de antes: numa cópia do ensaio/, 30 dias de rotina e uma descida à cripta;
  numa vila nova com a magia e a 4b, 60 dias com caça, forja, alquimia e masmorra; e um ano da vila de teste, mais depressa) · A PRATA QUE NÃO NASCE (a conta em cada evento)
  · OS ARQUIVOS NOVOS (o padrão vazio; o save de antes abre igual e não ganha arquivo) · O REGISTRO POR ESTAÇÃO · OS VERBOS E AS RECUSAS · OS CAMPOS E OS INVARIANTES
  · QUEM VIAJA E QUEM ESTÁ PRESO ESTÃO FORA · OS GANCHOS (negocia, companhia) · OS ESQUELETOS NEUTROS (o mundo de hoje sai igual) · A CONTA RÁPIDA · A FIXTURA
  · A MESA (o orçamento, o SÓ O MESTRE de quem está em cena, a caixa que vira pergunta, a viagem aberta que o fecha guarda) · O SAVE DO JOGADOR (numa cópia, com turno.py abre).
As provas rodam em mundos de rascunho, nunca num save. O save do jogador (ensaio/) só é LIDO, numa cópia temporária.
Uso: python3 provas_3.py [N]      (N não muda nada aqui: o banco é de contas fixas)
"""
import contextlib, copy, io, json, os, random, shutil, sys, tempfile, time
import tabelas_mundo as M
import estado, ato, turno, teste, luta, mercado, oficio, alquimia, caca, masmorra, vila_teste, talento
import regiao, viagem, gente, noticias, caixa, missoes, rapida, fixtura3
import provas_mundo as PM
import provas_masmorra as PMS
import provas_caca as PC
from itens import item

AQUI = os.path.dirname(os.path.abspath(__file__))
NOVOS = ('regiao', 'viagem', 'gente', 'missoes', 'caixa', 'noticias')


def quieto(f, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()): return f(*a, **k)


def recusa(f): return PM.recusa(f)
def gera(E, ef, texto='prova'): return estado.aplica(E, 'gera', ef, texto=texto)
def sn(x): return 'sim' if x else 'NÃO'
def tenta(f, *a, **k):
    try: return quieto(f, *a, **k)
    except SystemExit: return None


def retrato(E): return json.dumps({k: E[k] for k in estado.ARQS if k in E}, sort_keys=True, ensure_ascii=False)


@contextlib.contextmanager
def gravador(modo):
    """roda com o gravador dito ('toque': o de agora; 'inteiro': o de antes, a cópia inteira)"""
    antes = os.environ.get('MOTOR10_GRAVADOR')
    if modo == 'inteiro': os.environ['MOTOR10_GRAVADOR'] = 'inteiro'
    else: os.environ.pop('MOTOR10_GRAVADOR', None)
    try: yield
    finally:
        os.environ.pop('MOTOR10_GRAVADOR', None)
        if antes is not None: os.environ['MOTOR10_GRAVADOR'] = antes


@contextlib.contextmanager
def pasta(copia_de=None):
    """um save de rascunho (MOTOR10_MUNDO), vazio ou cópia de outro, desfeito no fim"""
    d = tempfile.mkdtemp(prefix='m10_3_'); alvo = os.path.join(d, 'save'); antes = os.environ.get('MOTOR10_MUNDO')
    if copia_de: shutil.copytree(copia_de, alvo)
    else: os.makedirs(alvo)
    os.environ['MOTOR10_MUNDO'] = alvo
    try: yield alvo
    finally:
        os.environ.pop('MOTOR10_MUNDO', None)
        if antes is not None: os.environ['MOTOR10_MUNDO'] = antes
        shutil.rmtree(d, ignore_errors=True)


@contextlib.contextmanager
def dados(semente):
    """o dado do jogador e o da luta repetíveis (os dois gravadores têm de ver os mesmos dados)"""
    luta.semente(semente)
    with PMS.dado_semente(semente + 1): yield


# ---------------------------------------------------------------- os robôs das provas de igualdade ----------------------------------------------------------------
def rotina(E, pid='eu'):
    """um dia de quem vive na vila: dorme até a alvorada, come, trabalha a jornada, come, e espera a meia-noite (as recusas fazem parte do caminho)"""
    b = E['relogio']['bloco']
    if b < 2: tenta(ato.dormir, E, pid, 2 - b, para=False)
    tenta(ato.comer, E, pid)
    if E['relogio']['bloco'] == 2: tenta(ato.trabalhar, E, pid, 2)
    tenta(ato.comer, E, pid)
    r = (M.BLOCOS_DIA - E['relogio']['bloco']) % M.BLOCOS_DIA or M.BLOCOS_DIA
    if E['gente'][pid]['estado'] == 'vivo' and not estado.luta_aberta(E): ato.passa(E, pid, r, 'esperar', texto='espera', para=False)


def _ensaio_30(modo):
    """uma cópia do ensaio/: 30 dias de rotina do Maro e uma descida à cripta (sozinho, com tochas). Devolve (o retrato, o registro, os segundos)"""
    with gravador(modo), pasta(os.path.join(AQUI, 'ensaio')), dados(41):
        E = estado.carrega(); pid = estado.eu(E); t = time.perf_counter(); d0 = E['relogio']['dia']
        while E['relogio']['dia'] < d0 + 30 and E['gente'][pid]['estado'] == 'vivo' and not estado.luta_aberta(E): rotina(E, pid)
        if E['gente'][pid]['estado'] == 'vivo' and not estado.luta_aberta(E):
            tenta(PMS.compra_tochas, E, pid, 2)
            tenta(PMS.desce, E, pid, [], [pid], prudente=True)
            tenta(PMS.vende, E, pid)
        dt = time.perf_counter() - t
        return retrato(E), json.dumps(estado.eventos(E), sort_keys=True, ensure_ascii=False), dt


def _mista_60(modo):
    """uma vila nova (o ferreiro, com a magia e a 4b, mais forte que o de começo), 60 dias: de três em três, forja uma adaga e vende, faz uma leva de poção de cura e vende,
    desce à cripta (com a gente forte da vila); nos últimos seis dias, caça na Mata do Corvo; nos outros blocos, a rotina. Devolve (o retrato, o registro, os segundos)"""
    with gravador(modo), pasta(), dados(43):
        E = vila_teste.cria('ferreiro', semente=5, talentos=True, inclinacao='forja', inclinacao2='encanto'); quieto(vila_teste.magia, E); quieto(vila_teste.fantasia, E)
        arma = next((it.get('familia') for it in E['itens']['itens'].values() if it.get('dono') == 'eu' and it.get('uso') == 'arma'), None)
        gera(E, [['pessoa', 'eu', 'maestria.alquimia', 'poe', 2], ['pessoa', 'eu', 'moedas', 'soma', 200], ['pessoa', 'eu', 'nivel', 'soma', 8], ['pessoa', 'eu', 'pv', 'soma', 999]]
             + ([['pessoa', 'eu', 'maestria.' + arma, 'poe', 4]] if arma else []), 'o ferreiro de prova sabe a alquimia, luta e tem prata')
        pid = 'eu'; V = PC.caderno(); t = time.perf_counter(); d0 = E['relogio']['dia']; ultimo = None
        while E['relogio']['dia'] < d0 + 60 and E['gente'][pid]['estado'] == 'vivo' and not estado.luta_aberta(E):
            if estado.agora(E) == ultimo:                   # o dia não andou (tudo recusou): o tempo passa um bloco, como quem espera
                if estado.fora(E, pid): break
                ato.passa(E, pid, 1, 'esperar', texto='espera', para=False)
            ultimo = estado.agora(E); k = 0 if E['relogio']['dia'] - d0 >= 54 else 1 + (E['relogio']['dia'] - d0) % 3; b = E['relogio']['bloco']
            if b < 2: tenta(ato.dormir, E, pid, 2 - b, para=False); tenta(ato.comer, E, pid); continue
            if b == 2:
                if k == 0: tenta(PC.uma_saida, E, pid, V, PC.prudente, alvo='corça', blocos=2, ermo='mata')
                elif k == 1:
                    if tenta(mercado.comprar, E, pid, 'metal:0', 1):
                        R = tenta(oficio.forjar, E, pid, oficio.molde('arma', 0, 'Adaga de prova', familia='adaga'))
                        if R and R.get('item'): tenta(mercado.vender_peca, E, pid, R['item'])
                elif k == 2:
                    for bem, q in alquimia.materia_leva('cura', 0).items(): tenta(mercado.comprar, E, pid, bem, q)
                    tenta(alquimia.fazer, E, pid, 'cura', 0); tenta(mercado.vender, E, pid, 'cura:0', 'tudo')
                else:
                    com = [c for c in ('durva', 'brasco', 'ilvena', 'tome', 'rute') if E['gente'].get(c, {}).get('estado') == 'vivo' and E['gente'][c]['lugar'] == E['gente'][pid]['lugar']]
                    tenta(PMS.compra_tochas, E, pid, 3); tenta(PMS.desce, E, pid, com, [c for c in com if c in ('durva', 'brasco', 'tome')] + [pid] + [c for c in com if c not in ('durva', 'brasco', 'tome')], prudente=True)
                    tenta(PMS.vende, E, pid)
            if E['gente'][pid]['estado'] == 'vivo' and not estado.luta_aberta(E): rotina(E, pid)
        dt = time.perf_counter() - t
        return retrato(E), json.dumps(estado.eventos(E), sort_keys=True, ensure_ascii=False), dt


def _ano(modo, dias=364):
    """um ano da vila de teste (o ferreiro, com a magia e a 4b), o personagem na rotina: (o retrato, o registro, os segundos, os eventos)"""
    with gravador(modo):
        E = vila_teste.cria('ferreiro', semente=3, talentos=True, inclinacao='forja', inclinacao2='encanto'); quieto(vila_teste.magia, E); quieto(vila_teste.fantasia, E); E['_novos'] = []
        evs = []; t = time.perf_counter(); d0 = E['relogio']['dia']
        while E['relogio']['dia'] < d0 + dias and E['gente']['eu']['estado'] == 'vivo': rotina(E, 'eu'); evs += E['_novos']; E['_novos'] = []
        dt = time.perf_counter() - t
        return retrato(E), json.dumps(evs, sort_keys=True, ensure_ascii=False), dt, len(evs)


def _igual(n):
    out = []
    if os.path.exists(os.path.join(AQUI, 'ensaio', 'relogio.json')):
        a, b = _ensaio_30('toque'), _ensaio_30('inteiro'); desceu = any(e['tipo'] == 'masmorra' for e in json.loads(a[1]))
        out.append(('G1 O GRAVADOR POR TOQUE DÁ O MESMO MUNDO (uma cópia do ensaio/: 30 dias de rotina do Maro e uma descida à cripta, com os dois gravadores e os mesmos dados)',
                    f"o estado igual, byte a byte: {sn(a[0] == b[0])}; o registro igual: {sn(a[1] == b[1])} ({len(json.loads(a[1]))} eventos; desceu à cripta: {sn(desceu)}); por toque {a[2]:.2f} s, inteiro {b[2]:.2f} s",
                    a[0] == b[0] and a[1] == b[1] and desceu))
    a, b = _mista_60('toque'), _mista_60('inteiro'); evs = json.loads(a[1]); tipos = {e['tipo'] for e in evs}
    feito = {'cacar', 'forjar', 'alquimia', 'masmorra'} <= tipos
    out.append(('G2 O GRAVADOR POR TOQUE DÁ O MESMO MUNDO (uma vila nova com a magia e a 4b: 60 dias com caça, forja, alquimia e masmorra)',
                f"o estado igual, byte a byte: {sn(a[0] == b[0])}; o registro igual: {sn(a[1] == b[1])} ({len(evs)} eventos; houve caça, forja, alquimia e masmorra: {sn(feito)}); "
                f"por toque {a[2]:.2f} s, inteiro {b[2]:.2f} s", a[0] == b[0] and a[1] == b[1] and feito))
    a, b = _ano('toque'), _ano('inteiro')
    out.append(('G3 UM ANO DA VILA DE TESTE (a magia e a 4b, o personagem na rotina): o mesmo mundo, e mais depressa (a meta da ordem: menos tempo que o gravador de hoje)',
                f"o estado igual: {sn(a[0] == b[0])}; o registro igual: {sn(a[1] == b[1])} ({a[3]} eventos); por toque {a[2]:.2f} s ({1000 * a[2] / 364:.1f} ms por dia), "
                f"inteiro {b[2]:.2f} s ({1000 * b[2] / 364:.1f} ms por dia)", a[0] == b[0] and a[1] == b[1] and a[2] < b[2]))
    return out


# ---------------------------------------------------------------- a prata ----------------------------------------------------------------
def _prata(n):
    R = {}; E = fixtura3.cria(3); p0 = estado.prata_do_mundo(E)
    R['a prata do mundo soma a bolsa do povo (a da fixtura: Pedra Rasa e os povoados novos)'] = p0 == mercado.prata_do_mundo(E) + sum(l.get('bolsa', 0) for l in E['lugares'].values())
    r = recusa(lambda: estado.aplica(E, 'trabalhar', [['pessoa', 'eu', 'moedas', 'soma', 5]], texto='prata do nada'))
    R['o evento que faz prata nascer fora do gera e do mestre é recusado, com a conta'] = bool(r) and 'nascer' in r and '5 de prata' in r and estado.prata_do_mundo(E) == p0
    r = recusa(lambda: estado.aplica(E, 'regiao', [['lugar', 'vila', 'bolsa', 'soma', -7]], texto='a bolsa que some'))
    R['e o que faz sumir (a bolsa do povo)'] = bool(r) and 'sumir' in r
    R['a prata que muda de mão passa (o caixa paga à bolsa no mesmo evento)'] = bool(estado.aplica(E, 'regiao', [['lugar', 'vila', 'bolsa', 'soma', -7], ['estoque', 'vila', 'prata', 'soma', 7]], texto='o povo paga a loja')) and estado.prata_do_mundo(E) == p0
    R['o Mestre e o gerador podem pôr prata'] = bool(estado.aplica(E, 'mestre', [['pessoa', 'eu', 'moedas', 'soma', 3]], texto='achou')) and estado.prata_do_mundo(E) == p0 + 3
    mid = estado.proximo_id(E, 'missoes')
    reg = dict(de='odilia', onde='cerro', tipo='caçar', grau='E', alvo=dict(especie='lobo', n=1), paga=25, caucao=5, prazo=E['relogio']['dia'] + 14, guarda=25)
    r = recusa(lambda: estado.aplica(E, 'missao', [['missao', 'abre', reg]], texto='a paga do nada'))
    R['a missão que guarda a paga sem tirá-la de ninguém é recusada'] = bool(r) and 'nascer' in r
    p1 = estado.prata_do_mundo(E); estado.aplica(E, 'missao', [['missao', 'abre', reg], ['pessoa', 'odilia', 'moedas', 'soma', -25]], texto='a alcaide guarda a paga')
    R['a guarda conta na prata do mundo (sai da bolsa de quem pede)'] = E['missoes']['itens'][mid]['guarda'] == 25 and estado.prata_do_mundo(E) == p1
    estado.aplica(E, 'missao', [['missao', mid, 'guarda', 'soma', -25], ['pessoa', 'tome', 'moedas', 'soma', 25], ['missao', mid, 'quem', 'poe', 'tome'], ['missao', mid, 'fecha', 'cumprida']], texto='Tomé cumpre')
    R['cumprida, a paga vai a quem cumpriu, e a missão fechada não guarda prata'] = E['missoes']['itens'][mid]['estado'] == 'cumprida' and estado.prata_do_mundo(E) == p1 and not estado.valida(E)
    morre = estado.aplica(E, 'virada', [['pessoa', 'belmiro', 'estado', 'poe', 'morto']], texto='o mercador morre')
    R['a morte leva a prata do morto ao estoque do lugar: a soma não muda'] = bool(morre) and estado.prata_do_mundo(E) == p1 and E['gente']['belmiro']['moedas'] == 0
    ruim = [k for k, v in R.items() if not v]
    return [('P1 A PRATA NÃO NASCE NEM SOME (a conta em cada evento: as moedas, o caixa, a bolsa do povo e a guarda das missões; fora do gera e do mestre, recusa)',
             ' · '.join(R) if not ruim else 'ERRADO: ' + ' · '.join(ruim), not ruim)]


# ---------------------------------------------------------------- os arquivos, o save de antes, o registro por estação ----------------------------------------------------------------
def _arquivos(n):
    R = {}
    with pasta() as d:
        E = PM.vila(); estado.grava(E)
        R['o save sem a etapa 3 não ganha arquivo novo ao gravar'] = not any(os.path.exists(os.path.join(d, k + '.json')) for k in estado.PADRAO)
        E2 = estado.carrega(); R['e abre com o padrão vazio'] = all(E2[k] == estado.PADRAO[k] for k in estado.PADRAO) and not estado.valida(E2)
        gera(E2, [['lugar', 'nasce', 'outra', dict(nome='a Outra Vila', tipo='aldeia')], ['rota', 'nasce', 'r1', dict(a='vila', b='outra', blocos=2, tipo='caminho')]]); estado.grava(E2)
        R['a rota grava o rotas.json (e só ele)'] = os.path.exists(os.path.join(d, 'rotas.json')) and not os.path.exists(os.path.join(d, 'caixa.json')) and estado.carrega()['rotas']['r1']['blocos'] == 2
        ids = []
        for k in range(M.ESTACAO + 5):                      # um dia por evento, gravando todo dia: a estação vira no Dia 92
            ev = estado.aplica(E2, 'tempo', [['relogio', M.BLOCOS_DIA]], texto=f'o dia {k}'); ids.append(ev['id']); estado.grava(E2)
        arq = os.path.join(d, estado.arq_estacao(1, 0)); evs = estado.eventos()
        aberta = [json.loads(x) for x in open(os.path.join(d, 'eventos.jsonl'), encoding='utf-8')]
        R['a estação que acabou vai comprimida para eventos/1_primavera.jsonl.gz'] = os.path.exists(arq) and all(estado._estacao_do_dia(e['dia']) == (1, 1) for e in aberta)
        R['e o histórico inteiro se lê pelo estado.eventos, em ordem, sem buraco'] = [e['id'] for e in evs] == list(range(1, evs[-1]['id'] + 1)) and evs[-1]['id'] == ids[-1]
        R['estado.eventos(desde=N) só lê o que vem depois de N'] = [e['id'] for e in estado.eventos(desde=ids[-3])] == ids[-2:]
    ruim = [k for k, v in R.items() if not v]
    return [('A1 OS ARQUIVOS DA ETAPA 3 (rotas, noticias, caixa, missoes: o padrão vazio; o save de antes abre igual e não ganha arquivo) E O REGISTRO POR ESTAÇÃO',
             ' · '.join(R) if not ruim else 'ERRADO: ' + ' · '.join(ruim), not ruim)]


# ---------------------------------------------------------------- os verbos, os campos, as recusas ----------------------------------------------------------------
def _verbos(n):
    R = {}; E = fixtura3.cria(3); estado.aplica(E, 'tempo', [['relogio', 30 * M.BLOCOS_DIA]], texto='um mês'); dia = E['relogio']['dia']
    q = lambda tipo, ef: recusa(lambda: estado.aplica(E, tipo, ef, texto='prova'))
    R['a rota só nasce no gera'] = bool(q('regiao', [['rota', 'nasce', 'rx', dict(a='vila', b='ribanceira', blocos=3, tipo='caminho')]]))
    R['não repete as duas pontas, nem passa de 6 blocos, nem cruza o que não é ermo'] = bool(q('gera', [['rota', 'nasce', 'rx', dict(a='telhal', b='vila', blocos=2, tipo='estrada')]])) \
        and bool(q('gera', [['rota', 'nasce', 'rx', dict(a='vila', b='ribanceira', blocos=7, tipo='caminho')]])) and bool(q('gera', [['rota', 'nasce', 'rx', dict(a='vila', b='ribanceira', blocos=3, tipo='caminho', ermo='telhal')]]))
    estado.aplica(E, 'regiao', [['rota', 'r_vila_cerro', 'falta.comida', 'soma', 12], ['rota', 'r_vila_cerro', 'aberta', 'poe', False]], texto='o carreto deixou comida; o bando fecha a rota')
    R['a falta e o aberta mudam no dia da região; o resto só com o Mestre'] = E['rotas']['r_vila_cerro']['falta'] == {'comida': 12} and not E['rotas']['r_vila_cerro']['aberta'] \
        and bool(q('regiao', [['rota', 'r_vila_cerro', 'blocos', 'poe', 1]])) and regiao.vizinhos(E, 'vila') == [('telhal', 'r_vila_telhal', 3)]
    R['o papel só no gera ou no mestre, e da tabela'] = bool(q('gente', [['pessoa', 'ivo', 'papel', 'poe', 'guarda']])) and bool(q('gera', [['pessoa', 'ivo', 'papel', 'poe', 'rei']]))
    fato = lambda k, peso, t='entregou': [dia - k, t, peso, 'eu', 'viu', f'fato {k}']
    estado.aplica(E, 'gente', [['pessoa', 'bento', 'memoria', 'junta', fato(k, 1 + k % 5)] for k in range(12)], texto='Bento lembra de doze coisas')
    leve = [f for f in E['gente']['bento']['memoria'] if abs(estado.peso_hoje(f, E['relogio']['dia'])) == min(abs(estado.peso_hoje(x, E['relogio']['dia'])) for x in E['gente']['bento']['memoria'])]
    estado.aplica(E, 'gente', [['pessoa', 'bento', 'memoria', 'junta', fato(0, 8, 'salvou')]], texto='o décimo terceiro')
    m = E['gente']['bento']['memoria']
    R['a memória cabe 12: o 13º esquece o mais leve de hoje (o mais velho, no empate), no próprio verbo'] = len(m) == 12 and min(leve, key=lambda f: f[0]) not in m and all(f in m for f in leve if f != min(leve, key=lambda f: f[0])) and m[-1][1] == 'salvou'
    R['o fato esfria pela tabela (o leve perde 1 a cada 28 dias; o de 8, nunca)'] = estado.peso_hoje([1, 'pagou', 3, 'eu', 'viu', ''], 1 + 56) == 1 and estado.peso_hoje([1, 'salvou', 8, 'eu', 'viu', ''], 999) == 8 \
        and estado.peso_hoje([1, 'roubou', -6, 'eu', 'viu', ''], 1 + 112) == -4
    R['o fato torto é recusado (o tipo, o peso, de quem)'] = bool(q('gente', [['pessoa', 'bento', 'memoria', 'junta', [dia, 'xingou', 1, 'eu', 'viu', '']]])) \
        and bool(q('gente', [['pessoa', 'bento', 'memoria', 'junta', [dia, 'deu', 11, 'eu', 'viu', '']]])) and bool(q('gente', [['pessoa', 'bento', 'memoria', 'junta', [dia, 'deu', 1, 'ninguem', 'viu', '']]]))
    estado.aplica(E, 'gente', [['pessoa', 'bento', 'memoria', 'retribui', m[-1][:2]], ['pessoa', 'bento', 'memoria', 'esquece', 0]], texto='Bento agradece, e esquece o primeiro')
    R['retribui guarda o fato agradecido; esquece tira um'] = E['gente']['bento']['marca']['retribui'] == [m[-1][:2]] and len(E['gente']['bento']['memoria']) == 11
    estado.aplica(E, 'gente', [['lacos', 'bento', 'dalva', 'soma', 4], ['lacos', 'bento', 'tome', 'poe', -3], ['lacos', 'bento', 'dalva', 'soma', 20], ['pessoa', 'bento', 'querer', 'poe', dict(t='encomendar', desde=dia)]], texto='laços')
    R['o laço (o de gente: "lacos") vai de −10 a 10, na ficha de quem sente; o querer da lista'] = E['gente']['bento']['lacos'] == {'dalva': 10, 'tome': -3} and 'lacos' not in E['gente']['dalva'] \
        and bool(q('gente', [['lacos', 'bento', 'bento', 'soma', 1]])) and bool(q('gente', [['pessoa', 'bento', 'querer', 'poe', dict(t='voar')]])) and E['gente']['bento']['querer']['t'] == 'encomendar'
    seis = [k for k in E['gente'] if k not in ('bento', 'dalva', 'tome')][:4]
    estado.aplica(E, 'gente', [['lacos', 'bento', k, 'poe', 1] for k in seis], texto='mais laços')
    R['cabem 6 laços; zero tira o laço'] = len(E['gente']['bento']['lacos']) == 6 and bool(q('gente', [['lacos', 'bento', 'odilia', 'poe', 2]])) \
        and bool(estado.aplica(E, 'gente', [['lacos', 'bento', 'tome', 'soma', 3]], texto='fazem as pazes')) and 'tome' not in E['gente']['bento']['lacos']
    estado.aplica(E, 'noticia', [['fama', 'eu', 'vila', 'oficio', 'soma', 30], ['fama', 'eu', 'vila', 'crime', 'soma', 150]], texto='a fama')
    R['a fama: de 0 a 100, por lugar e eixo, esfria 1 a cada 28 dias na leitura'] = estado.fama_hoje(E['gente']['eu'], 'vila', 'crime', dia) == 100 and estado.fama_hoje(E['gente']['eu'], 'vila', 'oficio', dia + 56) == 28 \
        and bool(q('noticia', [['fama', 'eu', 'vila', 'beleza', 'soma', 1]])) and gente.fama(E, 'eu', 'vila', 'oficio') == 30
    nid = estado.proximo_id(E, 'noticias')
    estado.aplica(E, 'noticia', [['noticia', 'nasce', dict(tipo='feito', texto='o ferreiro fez a espada', onde='vila', sobre='eu', alcance=2, peso=2)]], texto='a notícia nasce')
    R['a notícia nasce onde o fato foi, e não anda mais depressa que uma rota por dia'] = E['noticias']['ativas'][nid]['em'] == {'vila': [dia, 0]} and bool(q('noticia', [['noticia', nid, 'chega', 'telhal', 1]])) \
        and bool(q('noticia', [['noticia', nid, 'chega', 'telhal', 3]]))
    estado.aplica(E, 'tempo', [['relogio', M.BLOCOS_DIA]], texto='um dia')
    estado.aplica(E, 'noticia', [['noticia', nid, 'chega', 'telhal', 1]], texto='a notícia chega')
    R['no dia seguinte chega ao vizinho (o noticias.chegou já lê)'] = [x['id'] for x in noticias.chegou(E, 'telhal')] == [nid] and noticias.chegou(E, 'cerro') == []
    agora = estado.agora(E); mot = dict(tipo='item', id=next(k for k, it in E['itens']['itens'].items() if it.get('dono') == 'tome'))
    pedido = lambda **x: dict(dict(de='tome', molde='conserto', pede='consertar a lança', prazo=agora + 12, opcoes=dict(a='aceitar', b='recusar'), padrao='b', custo='ele leva a outro', motivo=mot), **x)
    R['a caixa só escreve com motivo no estado, de quem vive, com o padrão entre as opções e o prazo adiante'] = bool(q('caixa', [['caixa', 'abre', pedido(motivo=dict(tipo='item', id='i9999'))]])) \
        and bool(q('caixa', [['caixa', 'abre', pedido(padrao='c')]])) and bool(q('caixa', [['caixa', 'abre', pedido(prazo=agora)]]))
    estado.aplica(E, 'caixa', [['caixa', 'abre', pedido()] for _ in range(M.CAIXA_MAX)], texto='sete pedidos')
    cid = sorted(E['caixa']['abertos'])[0]
    R['cabem 7: o oitavo é recusado (força-se o mais velho antes, no mesmo evento)'] = bool(q('caixa', [['caixa', 'abre', pedido()]])) \
        and bool(estado.aplica(E, 'caixa', [['caixa', cid, 'fecha', 'forcado'], ['caixa', 'abre', pedido()]], texto='o oitavo força o primeiro')) and len(caixa.abertos(E)) == 7
    estado.aplica(E, 'gera', [['pessoa', 'eu', 'mora', 'poe', 'vila'], ['pessoa', 'eu', 'mapa', 'poe', dict(lugares=['vila'], rotas=['r_vila_telhal'])], ['pessoa', 'eu', 'mapa', 'junta', dict(lugares=['telhal'])],
                      ['pessoa', 'eu', 'marca.preco', 'poe', 0.8], ['lugar', 'telhal', 'safra', 'poe', 1.1], ['lugar', 'charco', 'bando', 'poe', 6], ['lugar', 'cerro', 'vigia', 'poe', [dia]]])
    R['mora, o mapa (poe e junta), o fator de preço, a colheita, o bando, a vigia: com faixa'] = E['gente']['eu']['mapa'] == dict(lugares=['vila', 'telhal'], rotas=['r_vila_telhal']) and estado.mora(E['gente']['eu']) == 'vila' \
        and bool(q('gera', [['pessoa', 'eu', 'marca.preco', 'poe', 3]])) and bool(q('gera', [['lugar', 'telhal', 'safra', 'poe', 2]])) and bool(q('gera', [['lugar', 'charco', 'bando', 'poe', 51]])) \
        and bool(q('gera', [['lugar', 'vila', 'bolsa', 'poe', -1]])) and bool(q('gera', [['lugar', 'vila', 'tipo', 'poe', 'castelo']])) and bool(q('gera', [['pessoa', 'eu', 'mapa', 'poe', dict(lugares=['nada'])]]))
    gera(E, [['item', 'nasce', dict(tipo='animal', qual='mula', cat=0, nome='a mula de prova', dur=[1, 1], leva=80, come=2, dono='eu')], ['item', 'nasce', dict(tipo='carro', cat=0, nome='a carroça de prova', dur=[1, 1], leva=300, so_estrada=True, onde='vila')]])
    R['o animal e o carro entram no Livro de Itens; o animal sem "qual" da lista, não'] = sum(1 for it in E['itens']['itens'].values() if it['tipo'] in ('animal', 'carro')) == 2 \
        and bool(q('gera', [['item', 'nasce', dict(tipo='animal', qual='dragão', cat=0, nome='x', dur=[1, 1], leva=80, dono='eu')]]))
    R['o estado fica inteiro'] = not estado.valida(E)
    ruim = [k for k, v in R.items() if not v]
    return [('V1 OS VERBOS DA ETAPA 3 E AS RECUSAS (rota; papel, memória, querer, laços, fama; notícia; caixa; missão; mora, mapa, as marcas; os campos do lugar; o animal e o carro)',
             ' · '.join(R) if not ruim else 'ERRADO: ' + ' · '.join(ruim), not ruim)]


def _invariantes(n):
    R = {}; E0 = fixtura3.cria(3)
    def quebra(f):
        E = copy.deepcopy(E0); f(E); return estado.valida(E)
    R['a rota que liga a um lugar que não existe'] = any('rota' in x for x in quebra(lambda E: E['rotas']['r_vila_cerro'].update(b='nada')))
    R['duas rotas com as mesmas pontas'] = any('já há uma rota' in x for x in quebra(lambda E: E['rotas'].update(r2=dict(E['rotas']['r_vila_cerro']))))
    R['a memória com 13'] = any('memória' in x for x in quebra(lambda E: E['gente']['bento'].update(memoria=[[1, 'deu', 1, 'eu', 'viu', '']] * 13)))
    R['o laço com quem não há'] = any('laço' in x for x in quebra(lambda E: E['gente']['bento'].update(lacos={'ninguem': 3})))
    R['a fama acima de 100'] = any('fama' in x for x in quebra(lambda E: E['gente']['eu'].update(fama={'vila': {'feito': [120, 1]}})))
    R['o mundo de fora com gente'] = any('mundo de fora' in x for x in quebra(lambda E: (E['lugares'].update(fora=dict(nome='o Mundo de Fora', tipo='fronteira', estoque={})), E['gente']['ivo'].update(lugar='fora'))))
    R['a missão fechada que ainda guarda prata'] = any('guarda' in x for x in quebra(lambda E: E['missoes']['itens'].update(ms0001=dict(id='ms0001', de='odilia', onde='cerro', tipo='levar', grau='F', paga=10, caucao=2, prazo=9, quem=None, estado='vencida', guarda=10))))
    R['o pedido da caixa de quem morreu'] = any('caixa' in x for x in quebra(lambda E: (E['caixa']['abertos'].update(c0001=dict(id='c0001', de='odilia', para='eu', pede='x', prazo=99, aberto=1, opcoes=dict(a='s', b='n'), padrao='b', motivo=dict(tipo='lugar', id='cerro'))), E['gente']['odilia'].update(estado='morto', pv=0, moedas=0))))
    v = dict(rota='r_vila_cerro', origem='vila', destino='cerro', feito=1, blocos=2, com=['tome'], fase='estrada')
    R['a viagem e a saída abertas juntas'] = any('ao mesmo tempo' in x for x in quebra(lambda E: E['gente']['eu']['marca'].update(viagem=v, caca=dict(ermo='mata', casa='vila', fase='procura', restam=1, com=[]))))
    R['quem foi junto numa viagem que não existe'] = any('viagem que não existe' in x for x in quebra(lambda E: E['gente']['tome']['marca'].update(viagem=dict(de='eu'))))
    R['a viagem por uma rota que não liga as pontas'] = any('pontas' in x for x in quebra(lambda E: E['gente']['eu']['marca'].update(viagem=dict(v, destino='telhal'))))
    R['a fixtura inteira passa'] = estado.valida(E0) == []
    ruim = [k for k, v in R.items() if not v]
    return [('V2 OS INVARIANTES DA ETAPA 3 (o estado.valida acusa, e o fecha recusa): ' + ' · '.join(R.keys()), 'acusa todos' if not ruim else 'NÃO ACUSA: ' + ' · '.join(ruim), not ruim)]


def _fora(n):
    R = {}; E = fixtura3.cria(3)
    v = dict(rota='r_vila_cerro', origem='vila', destino='cerro', feito=1, blocos=2, com=['tome'], fase='estrada', dia=E['relogio']['dia'])
    r = recusa(lambda: estado.aplica(E, 'viagem', [['pessoa', 'eu', 'marca.viagem', 'poe', dict(v, rota='r_nada')]], texto='x'))
    R['a viagem por rota que não existe é recusada'] = bool(r)
    estado.aplica(E, 'viagem', [['pessoa', 'eu', 'marca.viagem', 'poe', v], ['pessoa', 'tome', 'marca.viagem', 'poe', dict(de='eu')]], texto='o Maro e o Tomé saem para Cerro Manso')
    R['quem viaja está fora: no ermo que a rota cruza'] = estado.fora(E, 'eu') == 'charco' and estado.fora(E, 'tome') == 'charco' and estado.quem_viaja(E, 'tome') == 'eu'
    r1 = recusa(lambda: ato.trabalhar(E, 'eu', 1)); r2 = recusa(lambda: mercado.comprar(E, 'tome', 'comida', 1))
    R['o presente recusa o ato da vila a quem viaja (e a quem vai junto)'] = bool(r1) and 'estrada' in r1 and bool(r2) and 'estrada' in r2
    R['a saída ao ermo não abre com a viagem aberta'] = bool(recusa(lambda: estado.aplica(E, 'cacar', [['pessoa', 'eu', 'marca.caca', 'poe', dict(ermo='mata', casa='vila', fase='procura', restam=1, com=[])]], texto='x')))
    gera(E, [['pessoa', 'tome', 'carga.comida', 'soma', 2]]); pr = estado.prata_do_mundo(E)
    estado.aplica(E, 'mestre', [['pessoa', 'tome', 'estado', 'poe', 'morto']], texto='o Tomé morre na estrada')
    R['quem morre na estrada fica no ermo da rota, com a carga; e sai da viagem'] = E['gente']['tome']['morte']['onde'] == 'charco' and E['lugares']['charco']['estoque'].get('comida', 0) >= 2 \
        and 'viagem' not in E['gente']['tome']['marca'] and estado.prata_do_mundo(E) == pr
    sem = dict(v, rota='r_telhal_ribanceira', origem='telhal', destino='ribanceira', feito=3, blocos=4, com=[])
    estado.aplica(E, 'mestre', [['pessoa', 'eu', 'marca.viagem', 'poe', sem]], texto='outra estrada')
    R['a rota de campo aberto: a ponta mais perto'] = estado.fora(E, 'eu') == 'ribanceira'
    estado.aplica(E, 'mestre', [['pessoa', 'eu', 'marca.viagem', 'poe', None]], texto='chegou')
    ate = estado.agora(E) + 3
    estado.aplica(E, 'furto', [['pessoa', 'eu', 'marca.preso', 'poe', dict(ate=ate)]], texto='o Maro vai preso')
    r = recusa(lambda: ato.trabalhar(E, 'eu', 1))
    R['o preso está no lugar dele e não age, até o bloco da marca'] = estado.fora(E, 'eu') is None and bool(r) and 'preso' in r
    estado.aplica(E, 'tempo', [['relogio', 3]], texto='passam três blocos')
    R['passado o prazo, age de novo'] = estado.preso(E, 'eu') is None and recusa(lambda: quieto(ato.esperar, E, 'eu', 1)) is None
    ruim = [k for k, v in R.items() if not v]
    return [('F1 QUEM VIAJA E QUEM ESTÁ PRESO ESTÃO FORA (o presente recusa o ato da vila; a morte na estrada; uma saída, uma descida e uma viagem nunca juntas)',
             ' · '.join(R) if not ruim else 'ERRADO: ' + ' · '.join(ruim), not ruim)]


# ---------------------------------------------------------------- os ganchos e os esqueletos ----------------------------------------------------------------
class _Recusa:
    """um módulo de prova que recusa negociar com o personagem e cobra 6 de prata de quem vai junto (o que a frente B1 vai fazer)"""
    __name__ = 'prova_gancho'
    @staticmethod
    def negocia(E, quem, com_quem): return 'Dalva não serve a quem a roubou' if quem == 'eu' else ''
    @staticmethod
    def companhia(E, quem, com, perigo, dias, paga=0):
        pede = 6 * len(com)
        if paga < pede: return f"pedem {pede} de prata para ir junto (paga={pede})", []
        return '', [['pessoa', quem, 'moedas', 'soma', -pede]] + [['pessoa', c, 'moedas', 'soma', 6] for c in com]


@contextlib.contextmanager
def _com_modulo(m):
    velho = estado.modulos(); estado._MODS = velho + [m]
    try: yield
    finally: estado._MODS = velho


def _ganchos(n):
    R = {}
    with pasta():
        E = PM.vila(); E['lugares']['mata'] = dict(nome='a Mata de Prova', em='na Mata de Prova', tipo='ermo', estoque={}); quieto(caca.povoa, E, 'mata', 'floresta', 1, vizinho='vila')
        quieto(mercado.funda, E, 'vila', 400)
        gera(E, [['pessoa', 'nasce', 'rute', dict(nome='Rute', nivel=5, atributos=dict(Força=55, Agilidade=60, Vigor=55, Vontade=50, Percepção=55, Afinidade=40), lugar='vila', moedas=10)]])
        E['relogio']['bloco'] = 2; base = retrato(E)
        with _com_modulo(_Recusa):
            gera(E, [['pessoa', 'eu', 'fome', 'soma', 5]]); base = retrato(E)
            r1 = recusa(lambda: mercado.comprar(E, 'eu', 'comida', 1)); r2 = recusa(lambda: ato.comer(E, 'eu'))
            R['o gancho negocia recusa a loja e a refeição antes de cobrar, com a frase de quem não serve'] = r1 == r2 == 'Dalva não serve a quem a roubou' and retrato(E) == base
            r3 = recusa(lambda: caca.sair(E, 'eu', 'mata', alvo='corça', blocos=1, com=['rute']))
            R['o gancho companhia recusa a saída sem a paga, e diz o preço'] = bool(r3) and 'paga=6' in r3 and retrato(E) == base
            pr = estado.prata_do_mundo(E); m0 = E['gente']['rute']['moedas']
            quieto(caca.sair, E, 'eu', 'mata', alvo='corça', blocos=1, com=['rute'], paga=6)
            R['com a paga, sai, e a prata vai a quem vai junto no evento que abre (a soma não muda)'] = E['gente']['rute']['moedas'] == m0 + 6 and estado.prata_do_mundo(E) == pr \
                and any(any(x[2:3] == ['marca.caca'] for x in e['efeitos']) and ['pessoa', 'rute', 'moedas', 'soma', 6] in e['efeitos'] for e in E['_novos'])
        tenta(caca.volta, E, 'eu')
    sem = recusa(lambda: estado.negocia(PM.vila(), 'eu', 'vila')); emc = estado.companhia(PM.vila(), 'eu', ['x'], {}, 1)
    R['sem módulo que cobre, toda loja negocia e quem é chamado vai sem paga (a regra de hoje)'] = estado.negocia(PM.vila(), 'eu', 'vila') == '' and emc == ('', [])
    ruim = [k for k, v in R.items() if not v]
    return [('K1 OS GANCHOS (negocia no mercado e na refeição; companhia na caça, na descida e na viagem): uma chamada, sem regra; o esqueleto não muda nada',
             ' · '.join(R) if not ruim else 'ERRADO: ' + ' · '.join(ruim), not ruim)]


CONTRATO = {regiao: ('gera', 'virada', 'vizinhos', 'distancia', 'caminho', 'rota_entre', 'rotas_de', 'guardas', 'perigo', 'mesa', 'so_mestre'),
            viagem: ('ir', 'blocos_ate', 'anda_npc', 'carga', 'virada', 'mesa', 'retomar', 'so_mestre', 'recusa_fecha'),
            gente: ('povoa', 'povoa_regiao', 'ponto', 'opiniao', 'lembra', 'tom', 'fama', 'teto', 'vai_junto', 'companhia', 'negocia', 'virada', 'mesa', 'so_mestre'),
            noticias: ('nasce', 'chegou', 'virada', 'mesa', 'so_mestre'), caixa: ('abertos', 'abre', 'responde', 'virada', 'mesa', 'so_mestre'),
            missoes: ('quadro', 'abre', 'pega', 'cumpre', 'entrega', 'fecha', 'virada', 'mesa', 'so_mestre'), rapida: ('teto', 'grau', 'letra', 'linha', 'missao', 'encontro')}


def _esqueletos(n):
    R = {}
    faltam = [f'{m.__name__}.{f}' for m, fs in CONTRATO.items() for f in fs if not callable(getattr(m, f, None))]
    R['as funções do contrato existem' + (f" (faltam: {', '.join(faltam)})" if faltam else '')] = not faltam
    R['os eventos, o mundo sozinho e os módulos novos na página'] = all(t in M.EVENTOS for t in ('viagem', 'regiao', 'frete', 'mercado', 'gente', 'noticia', 'caixa', 'missao', 'encomenda', 'furto', 'companhia')) \
        and all(t in M.MUNDO_SOZINHO for t in ('regiao', 'mercado', 'gente', 'noticia')) and all(m in M.MODULOS for m in NOVOS) and M.MODULOS.index('regiao') == 1 and M.MODULOS[-1] == 'noticias'
    def mundo(ligados):
        velho = estado._MODS
        try:
            estado._MODS = [m for m in estado.modulos() if ligados or m.__name__ not in NOVOS]
            with dados(7):
                E = vila_teste.cria('ferreiro', semente=4); quieto(vila_teste.magia, E); quieto(vila_teste.fantasia, E); m0 = turno.mesa(E)
                for _ in range(20): rotina(E, 'eu')
                return retrato(E), json.dumps(E['_novos'], sort_keys=True, ensure_ascii=False), m0, turno.mesa(E)
        finally: estado._MODS = velho
    a, b = mundo(True), mundo(False)
    R['a vila de teste de hoje, 20 dias, com e sem os seis módulos novos: o mesmo estado, o mesmo registro, a mesma MESA'] = a == b
    E = fixtura3.cria(3)
    R['o esqueleto é neutro: nada se gera, ninguém anda, a opinião é zero, a viagem recusa "ainda não"'] = regiao.gera(E, 1) == [] and viagem.anda_npc(E, 'eu', 'telhal') == [] and gente.opiniao(E, 'bento')[0] == 0 \
        and 'ainda não' in (recusa(lambda: viagem.ir(E, 'eu', 'telhal')) or '') and gente.vai_junto(E, 'eu', 'tome', {}, 1)['vai'] and caixa.abertos(E) == [] and missoes.quadro(E, 'cerro') == []
    R['a distância e os blocos até um lugar já saem do mapa'] = regiao.distancia(E, 'cerro', 'ribanceira') == 9 and viagem.blocos_ate(E, 'vila', 'telhal') == 3 and regiao.caminho(E, 'cerro', 'ribanceira')[1] == ['cerro', 'vila', 'telhal', 'ribanceira']
    ruim = [k for k, v in R.items() if not v]
    return [('K2 OS ESQUELETOS NEUTROS (regiao, viagem, gente, noticias, caixa, missoes) E OS EVENTOS NOVOS: o mundo de hoje sai igual com eles ligados',
             ' · '.join(R) if not ruim else 'ERRADO: ' + ' · '.join(ruim), not ruim)]


def _rapida(n):
    R = {}; E = fixtura3.cria(3)
    tetos = {E['gente'][k]['nome']: rapida.letra(rapida.teto(E, k)) for k in ('eu', 'tome', 'rute', 'ivo', 'durva') if k in E['gente']}
    diz = ', '.join(f'{k} {v}' for k, v in tetos.items())
    R[f"o teto da gente da vila de teste ({diz})"] = all(v in M.GRAUS for v in tetos.values())
    R['a tabela é uma só, com as quatro linhas (de −2 a 1) e os números dos dois projetos'] = sorted(M.RAPIDA) == [-2, -1, 0, 1] and M.RAPIDA[0]['cumpre'] == 0.65 and M.RAPIDA[1]['cumpre'] == 0.9
    a = rapida.missao(E, 'tome', 'D', 'm1'); b = rapida.missao(E, 'tome', 'D', 'm1'); c = [rapida.missao(E, 'tome', 'F', f'x{k}')['cumpre'] for k in range(400)]
    R['o dado é o do mundo (mesma chave, mesma conta); quem tem teto acima do grau cumpre quase sempre'] = a == b and sum(c) / len(c) > 0.8
    m = [rapida.encontro(E, 'ivo', 'C', f'e{k}')['morre'] for k in range(400)]; mc = [rapida.encontro(E, 'ivo', 'C', f'e{k}', com=1)['morre'] for k in range(400)]
    R['o encontro acima do teto mata, e a companhia tira a metade'] = sum(m) / 400 > 0.5 and sum(mc) < sum(m)
    ruim = [k for k, v in R.items() if not v]
    return [('K3 A CONTA RÁPIDA PROVISÓRIA (rapida.py: o teto, a missão do nomeado, o encontro na estrada; a etapa 5 a troca)', ' · '.join(R) if not ruim else 'ERRADO: ' + ' · '.join(ruim), not ruim)]


def _fixtura(n):
    R = {}; E = fixtura3.cria(3); p0 = estado.prata_do_mundo(E)
    novos = [k for k in ('telhal', 'ribanceira', 'cerro', 'charco') if k in E['lugares']]
    R['3 povoados novos, 1 ermo novo, 3 rotas, 6 pessoas de papel'] = len(novos) == 4 and len(E['rotas']) == 3 and sum(1 for p in E['gente'].values() if p.get('papel')) == 6 \
        and [E['lugares'][k]['tipo'] for k in novos] == ['cidade', 'vila', 'aldeia', 'ermo']
    R['tudo por eventos do gerador; o estado inteiro'] = not estado.valida(E)
    R['a bolsa do povo: 5 por pessoa'] = E['lugares']['telhal']['bolsa'] == 7500 and E['lugares']['cerro']['bolsa'] == 600
    R['recusa rodar duas vezes'] = bool(recusa(lambda: fixtura3.poe(E)))
    for _ in range(10): rotina(E, 'eu')
    R['dez dias de rotina: a prata fecha, o estado segue inteiro'] = estado.prata_do_mundo(E) == p0 and not estado.valida(E)
    ruim = [k for k, v in R.items() if not v]
    return [('X1 A FIXTURA (fixtura3.py: a região pequena para as frentes testarem antes do gerador de A1)', ' · '.join(R) if not ruim else 'ERRADO: ' + ' · '.join(ruim), not ruim)]


# ---------------------------------------------------------------- a MESA ----------------------------------------------------------------
def _mesa(n):
    R = {}
    with pasta():
        E = fixtura3.cria(3); estado.grava(E); txt = turno.mesa(E); o = turno.orcamento(txt)
        R['o orçamento mede cada parte (KB de 1.000 letras) e o total'] = abs(sum(kb for k, kb, _ in o if k != 'total') - len(txt.encode('utf-8')) / 1000) < 1e-6 and o[-1][0] == 'total'
        R['e o turno avisa a parte que passa do teto (o mercado de hoje passa)'] = any('mercado' in x for x in turno.avisos(txt)) and turno.avisos('## Você\nx\n') == []
        mestre = txt.split('## SÓ O MESTRE')[1]
        R['o SÓ O MESTRE só fala de quem está em cena: sem ato no turno, só do personagem'] = 'talento e dom de Bento' not in mestre and 'talento e dom de' in mestre and estado.na_cena(E) == ['eu']
        quieto(ato.trabalhar, E, 'bento', 1); m2 = turno.mesa(E).split('## SÓ O MESTRE')[1]
        R['quem esteve num ato do turno, no mesmo lugar, entra'] = 'talento e dom de Bento' in m2 and 'bento' in estado.na_cena(E)
        dia = E['relogio']['dia']; mot = dict(tipo='lugar', id='vila')
        gera(E, [['caixa', 'abre', dict(de='dalva', molde='loja', pede='uma espada Comum para a loja, por 18', prazo=estado.agora(E) + 4, opcoes=dict(a='aceitar', b='recusar'), padrao='b', custo='o mercador pede a outro', motivo=mot)]])
        cid = caixa.abertos(E)[0]['id']; t1 = turno.mesa(E)
        R['o pedido que vence em um dia aparece entre as perguntas, e vira pergunta sozinho ao fechar'] = f'{cid}:' in t1.split('## Perguntas abertas')[1].split('## SÓ O MESTRE')[0]
        quieto(turno.pergunta, E, 'O que fazer de tarde?', ['a=trabalhar', 'b=descansar'])
        quieto(ato.esperar, E, 'eu', 1)
        r = recusa(lambda: turno.fecha(E, 'um turno de prova'))
        R['o fecha põe o pedido nas perguntas (com o id, ligado a caixa.py responde) e fecha'] = r is None and any(q.get('caixa') == cid for q in E['turno']['perguntas'])
        n = next(q['n'] for q in E['turno']['perguntas'] if q.get('caixa') == cid)
        txt2 = quieto(turno.responde, E, f'{n}a'); quieto(ato.esperar, E, 'eu', 1); quieto(turno.pergunta, E, 'E à noite?', ['a=dormir', 'b=beber'])
        r = recusa(lambda: turno.fecha(E, 'outro turno'))
        R['respondido e não cumprido, o fecha recusa (cumpra com caixa.py responde)'] = bool(r) and f'caixa.py responde {cid} a' in r
        estado.aplica(E, 'caixa', [['caixa', cid, 'fecha', 'feito']], texto='o pedido foi aceito')
        R['cumprido, fecha'] = recusa(lambda: turno.fecha(E, 'outro turno')) is None
        v = dict(rota='r_vila_cerro', origem='vila', destino='cerro', feito=1, blocos=2, com=[], fase='estrada', dia=dia)
        estado.aplica(E, 'viagem', [['pessoa', 'eu', 'marca.viagem', 'poe', v]], texto='o Maro sai para Cerro Manso'); t3 = turno.mesa(E)
        R['com a viagem aberta, o "Aqui" diz a estrada, e saem o mercado e a oficina'] = 'está na estrada' in t3 and '## O mercado' not in t3 and '## A oficina' not in t3
        quieto(turno.pergunta, E, 'Seguir?', ['a=seguir', 'b=voltar']); quieto(turno.pergunta, E, 'Acampar?', ['a=sim', 'b=não'])
        estado.aplica(E, 'viagem', [['relogio', 1]], texto='um bloco de estrada')
        r = recusa(lambda: turno.fecha(E, 'na estrada')); E2 = estado.carrega(); ret = open(os.path.join(estado.pasta(), 'RETOMAR.md'), encoding='utf-8').read()
        R['o fecha guarda a viagem aberta (fica na pessoa) e o RETOMAR diz que ela está aberta'] = r is None and (E2['gente']['eu']['marca'] or {}).get('viagem', {}).get('rota') == 'r_vila_cerro' and 'a viagem está aberta' in ret
    ruim = [k for k, v in R.items() if not v]
    return [('M1 A MESA (o orçamento do juízo, medido e avisado; o SÓ O MESTRE de quem está em cena; a caixa que vira pergunta; a viagem aberta que o fecha guarda)',
             ' · '.join(R) if not ruim else 'ERRADO: ' + ' · '.join(ruim), not ruim)]


def _save(n):
    src = os.path.join(AQUI, 'ensaio')
    if not os.path.exists(os.path.join(src, 'relogio.json')): return [('S1 O SAVE DO JOGADOR', 'não há save em ensaio/ para conferir', True)]
    R = {}
    with pasta(src) as d:
        antes = sorted(os.listdir(d)); E = estado.carrega()
        R['abre com o padrão vazio nos quatro arquivos novos, e o estado inteiro'] = all(E[k] == estado.PADRAO[k] for k in estado.PADRAO) and not estado.valida(E)
        txt = quieto(turno.abre, E); mestre = txt.split('## SÓ O MESTRE')[1]
        so = [x for x in mestre.split('\n') if x.startswith('- talento e dom de ')]
        R[f'o turno.py abre sai ({len(txt.encode("utf-8")) / 1000:.1f} KB); o SÓ O MESTRE só com quem está em cena ({len(so)} linha de talento; o resto no talento.py mestre)'] = len(txt) > 200 and len(so) <= len(estado.na_cena(E))
        rotina(E, estado.eu(E)); estado.grava(E)
        R['um dia de rotina, gravado: nenhum arquivo novo, o estado inteiro'] = sorted(os.listdir(d)) == antes and not estado.valida(estado.carrega())
    ruim = [k for k, v in R.items() if not v]
    return [('S1 O SAVE DO JOGADOR ABRE (uma cópia do ensaio/: nada é escrito nele): os arquivos novos com o padrão, o turno.py abre, um dia de rotina',
             ' · '.join(R) if not ruim else 'ERRADO: ' + ' · '.join(ruim), not ruim)]


def provas(n=300):
    out = []
    for f in (_igual, _prata, _arquivos, _verbos, _invariantes, _fora, _ganchos, _esqueletos, _rapida, _fixtura, _mesa, _save):
        try: out += f(n)
        except (Exception, SystemExit) as x:
            import traceback; out.append((f'{f.__name__}: a prova quebrou', f'{type(x).__name__}: {x} · ' + ' | '.join(traceback.format_exc().splitlines()[-4:-1]).strip(), False))
    return out


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 300
    print('BANCO DE PROVAS DO ALICERCE DA ETAPA 3 (a região que responde: o gravador por toque, a prata, os arquivos, os verbos, os ganchos, os esqueletos, a MESA)\n')
    res = provas(n)
    for nome, deu, passa in res: print(f"  {'passa' if passa else 'FALHA'}  {nome}: {deu}")
    print(f'\n{sum(p for _, _, p in res)} de {len(res)} provas passam.')
    return all(p for _, _, p in res)


if __name__ == '__main__':
    import signal; hasattr(signal, 'SIGPIPE') and signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    sys.exit(0 if main() else 1)
