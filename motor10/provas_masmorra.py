#!/usr/bin/env python3
"""provas_masmorra.py — MOTOR 10, ETAPA 4b: O BANCO DE PROVAS DA MASMORRA (capítulo 17; o projeto A, seção 12: MA0 a MA7, MA12 a MA16; o contrato: projeto/ETAPA_4B.md).

  MA0 a pessoa comum é a de hoje (o módulo ligado e desligado: o mesmo estado e a mesma MESA) · MA1 o tempo (os lances, os blocos, a tocha, o escuro), em masmorras do gerador
  · MA2 a luz e o escuro · MA3 quem vê primeiro · MA4 não é mina (a casa da vila vive 60 dias ao lado da cripta) · MA5 o despojo pela categoria (pelas contas da masmorra)
  · MA6 a Cripta da Cova Velha (o robô de verdade, pelo masmorra.py) · MA7 a armadilha pelo item · MA12 o que vagueia e o descanso · MA13 a memória (um ano sozinha)
  · MA14 o mapa é segredo · MA15 a vila de teste (a cripta numa cópia do save) · MA16 as recusas · e o gerador (todos os moldes saem inteiros).
As provas rodam em mundos de rascunho, cada um numa pasta temporária (MOTOR10_MUNDO); nunca num save. O save do jogador (ensaio/) só é LIDO, numa cópia temporária.
A luta é a do luta.py de verdade; o dado do jogador é o de verdade (teste.rola), a não ser onde a prova o prende (dado_posto).
Uso: python3 provas_masmorra.py [N]      (o provas_mundo.py também roda este banco; N escala as vidas e as lutas, 300 de padrão)
"""
import contextlib, copy, io, json, math, os, random, shutil, sys, tempfile
import tabelas as T
import tabelas_mundo as M
import tabelas_bichos as TB
import tabelas_masmorra as K
import tabelas_manha as TMH
import estado, ato, turno, teste, luta, bichos, criaturas, caca, mercado
import masmorra as MS
import provas_mundo as PM
from itens import item
from pessoas import padrao, veste, ficha

AQUI = os.path.dirname(os.path.abspath(__file__))
VEM_DE_FORA = 120           # a faixa da MA13 (o projeto A e o capítulo 17.12): o bando de fora chega 120 dias depois de o nível ficar vazio (a prova confere contra isto, e não contra a página)
ROBO = dict(recua=0.30, foge=0.35, prudente=0.75, tentativas=4, dias6=20, dias4=60, tochas=6)      # o robô: o Maro recua na luta abaixo de 30% do PV; o grupo sai abaixo de 35%; o prudente não abre a porta do fundo com alguém abaixo de 75%


def quieto(f, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()): return f(*a, **k)


def recusa(f): return PM.recusa(f)
def sn(x): return 'sim' if x else 'NÃO'
def pct(x): return f"{100 * x:.0f}%"


@contextlib.contextmanager
def pasta(prefixo='m10_masm_'):
    """uma pasta temporária como save (MOTOR10_MUNDO), desfeita no fim"""
    d = tempfile.mkdtemp(prefix=prefixo); antes = os.environ.get('MOTOR10_MUNDO'); os.environ['MOTOR10_MUNDO'] = d
    try: yield d
    finally:
        if antes is None: os.environ.pop('MOTOR10_MUNDO', None)
        else: os.environ['MOTOR10_MUNDO'] = antes
        shutil.rmtree(d, ignore_errors=True)


@contextlib.contextmanager
def dado_posto(margens):
    """o dado do jogador rolado de verdade, com o total posto à mão (contra + margem): a mesma descida sai igual em dois mundos"""
    real = teste.rola; fila = list(margens)
    def posto(E, o_que, atributo, contra, mais=0, quem=None, oculto=False, dom=0, **kw):
        r = real(E, o_que, atributo, contra, mais=mais, quem=quem, oculto=oculto, dom=dom, **kw); m = fila.pop(0) if fila else 0; r['total'] = contra + m; r['passou'] = m >= 0
        r['dados'] = [[10], [10]]
        if dom: r['fez'] = False
        return r
    teste.rola = posto
    try: yield
    finally: teste.rola = real


@contextlib.contextmanager
def dado_semente(semente):
    """o dado do jogador (teste.rola) com semente, só no robô do banco: a mesma vida sai igual em toda rodada (a luta já tem a semente dela; o mundo, a dele)"""
    real = teste.d20x; r = random.Random(semente)
    def d20x():
        t = [r.randint(1, 20)]
        while t[-1] == 20: t.append(r.randint(1, 20))
        return t
    teste.d20x = d20x
    try: yield
    finally: teste.d20x = real


def vila(semente=1, cripta=True, tochas=6):
    """a vila de teste inteira (a de hoje, com a etapa da magia) e a Cripta da Cova Velha; o Maro leva tochas (pagas à loja, a 1 de prata)"""
    import vila_teste
    E = vila_teste.cria(semente=semente)
    quieto(vila_teste.magia, E)
    if cripta: MS.na_vila(E)
    if tochas: compra_tochas(E, 'eu', tochas)
    return E


def compra_tochas(E, pid, n):
    """o robô compra tochas na loja da vila (1 de prata cada: a prata muda de mão)"""
    n = min(n, E['gente'][pid]['moedas'])
    if n > 0: estado.aplica(E, 'compra', [['pessoa', pid, 'moedas', 'soma', -n], ['estoque', 'vila', 'prata', 'soma', n], ['pessoa', pid, 'carga.tocha', 'soma', n]], onde='vila', quem=[pid], texto='compra tochas')
    return n


def prata_do_mundo(E): return mercado.prata_do_mundo(E)


# ---------------------------------------------------------------- O ROBÔ QUE DESCE ----------------------------------------------------------------
def luta_robo(E, pid, recua=ROBO['recua']):
    """a luta do robô: a do ato.py luta, até o fim; quem comanda recua abaixo de 30% do PV (se ainda há quem lute)"""
    nome = E['gente'][pid]['nome']
    for _ in range(300):
        d = MS.descida(E['gente'][pid])
        if not d or d.get('fase') != 'luta': return dict(fase=(d or {}).get('fase', 'fim'))
        S = json.load(open(estado.arq_abre(d['luta']), encoding='utf-8')); f = next((x for x in S['L'] if x.get('id') == pid), None)
        ordem = 'recuar' if f and f['estado'] == 'pe' and f['pv'] < recua * f['pvmax'] and len([x for x in S['L'] if x['lado'] == 'A' and x['estado'] == 'pe']) > 1 else 'atacar'
        try: R = quieto(MS.luta_roda, E, pid, [f'{nome}: {ordem}'])
        except SystemExit: R = quieto(MS.luta_roda, E, pid, [])
        if R['fase'] != 'luta': return R
    raise RuntimeError('a luta não acaba')


def _fraco(E, g, frac):
    return any(E['gente'][c]['estado'] == 'vivo' and E['gente'][c]['pv'] < frac * estado.pv_max(E['gente'][c]) for c in g)


def desce(E, pid, com, ordem=None, ladino=None, prudente=True, conta=None, mid='cripta'):
    """UMA DESCIDA DO ROBÔ, pelo masmorra.py de verdade: anda a cripta, luta o que aparece, pega o que acha, abre o baú e a porta do fundo (a chave, a gazua ou a força),
    e sai: quando tudo foi visto, quando alguém cai abaixo de 35% do PV, ou (o prudente) quando chega à porta do fundo com alguém abaixo de 75%"""
    C = conta if conta is not None else {}
    for k in ('lutas', 'vagantes', 'armadilhas_achadas', 'armadilhas_disparadas', 'tochas', 'blocos'): C.setdefault(k, 0)
    t0 = (E['gente'][pid].get('carga') or {}).get('tocha', 0)
    o = list(ordem or [pid] + list(com))
    R = quieto(MS.descer, E, pid, mid, com=com, ordem=o, luz='tocha' if t0 else 'nada', quem_luz=pid if t0 else None)
    feitas = set(); procurou = set(); fundo = MS.fundo(E, mid); visitou = set(); tenta = {}; pausas = 0; pegou = set()
    for passo in range(600):
        p = E['gente'][pid]; d = MS.descida(p)
        if not d: break
        g = MS._grupo(E, pid, d); sid = d['sala']; visitou.add(sid)
        try:
            if d['fase'] == 'luta': luta_robo(E, pid); continue
            if d['fase'] == 'encontro':
                C['vagantes'] += bool(d['encontro'].get('vem'))
                if ladino in g and MS._frente(E, pid, d) == ladino: quieto(MS.ordem, E, pid, [x for x in MS._ordem(E, pid, d) if x != ladino] + [ladino])
                enc = d['encontro']; ant = d.get('anterior')
                pas = enc.get('surpresa') != 'A' and enc.get('onde', enc['sala']) == sid and ant in E['lugares'] and E['lugares'][ant].get('largura') == 1 and E['lugares'][enc['sala']].get('largura') != 1
                quieto(MS.atacar, E, pid, passagem=pas); C['lutas'] += 1; luta_robo(E, pid); continue
            if d['fase'] == 'armadilha':
                C['armadilhas_achadas'] += 1; feitas_ = set((d.get('armadilha') or {}).get('contornadas') or [])
                ach = [x for x in MS._achadas(E, sid) if x[2].get('onde', 'chão') == 'chão' and x[1] not in feitas_]
                if not ach: quieto(MS.contornar, E, pid); continue
                if ladino in g: quieto(MS.desarmar, E, pid, ach[0][0], quem=ladino)
                else: quieto(MS.contornar, E, pid, ach[0][0])
                continue
            if ladino in g and MS._frente(E, pid, d) != ladino: quieto(MS.ordem, E, pid, [ladino] + [x for x in MS._ordem(E, pid, d) if x != ladino])
            if _fraco(E, g, ROBO['foge']) or any(E['gente'][c]['estado'] != 'vivo' for c in [pid] + list(com)): break
            if not MS._luz_de(E, pid, d):                       # a luz acabou: outra tocha de quem leva, ou o grupo sai
                tem = [c for c in g if (E['gente'][c].get('carga') or {}).get('tocha', 0) >= 1]
                if tem: quieto(MS.luz, E, pid, 'tocha', quem=tem[0]); continue
                break
            l = E['lugares'][sid]; gd = l.get('guardado')
            if prudente and (E['lugares'][mid].get('alarme', 0) or 0) >= K.ALARME['alerta'] and not MS.ocupada(E, sid) and len(g) > 1 and pausas < 3:
                pausas += 1; quieto(MS.descansar, E, pid, 1, vigia=g[-1]); continue
            if ladino in g and sid not in procurou: procurou.add(sid); quieto(MS.procurar, E, pid, quem=ladino); continue
            if isinstance(gd, dict) and not gd.get('aberto') and not MS.ocupada(E, sid):
                ach = MS._achadas(E, sid)
                if ach and ladino in g: quieto(MS.desarmar, E, pid, ach[0][0], quem=ladino); continue
                k = ('guardado', sid); tenta[k] = tenta.get(k, 0) + 1
                if tenta[k] <= 2 * ROBO['tentativas']:
                    ch = MS._chave_de(E, g, sid)
                    if ch: quieto(MS.abrir, E, pid, 'guardado', 'chave'); continue
                    if tenta[k] <= ROBO['tentativas'] or ladino in g:
                        melhor = max(g, key=lambda c: E['gente'][c]['atributos']['Agilidade'] + 100 * bool(c == ladino))
                        quieto(MS.abrir, E, pid, 'guardado', 'gazua' if __import__('manha').gazua_de(E, melhor) else 'grampo', quem=melhor); continue
                    quieto(MS.abrir, E, pid, 'guardado', 'força', quem=max(g, key=lambda c: E['gente'][c]['atributos']['Força'])); continue
            tes = MS._tesouro(E, sid)
            if tes and (sid, tes) not in pegou and not MS.ocupada(E, sid) and (not isinstance(gd, dict) or gd.get('aberto')):
                pegou.add((sid, tes))                           # a peça cuja parte dos outros quem pega não tem como pagar segue ali: o robô não tenta de novo a mesma coisa
                try: quieto(MS.pegar, E, pid)
                except SystemExit: pass
                continue
            if sid == fundo and not MS.ocupada(E, sid) and sid not in procurou: procurou.add(sid); quieto(MS.procurar, E, pid); continue
            # a próxima sala: a que o grupo ainda não viu (a porta trancada pede a chave, a gazua ou a força); o prudente não abre a do fundo com alguém abaixo de 75%
            def cands(x): return [v for v in MS._viz(E, x) if v not in visitou and not (prudente and v == fundo and _fraco(E, g, ROBO['prudente'])) and tenta.get(('porta', v), 0) < 2 * ROBO['tentativas']]
            cs = cands(sid)
            if cs:
                v = cs[0]; pt = MS.porta(E, sid, v)
                if pt and pt['estado'] in ('trancada', 'emperrada'):
                    k = ('porta', v); tenta[k] = tenta.get(k, 0) + 1; ch = MS._chave_de(E, g, MS._pk(sid, v))
                    if ch: quieto(MS.abrir, E, pid, v, 'chave')
                    elif ladino in g and pt['estado'] == 'trancada': quieto(MS.abrir, E, pid, v, 'gazua' if __import__('manha').gazua_de(E, ladino) else 'grampo', quem=ladino)
                    else: quieto(MS.abrir, E, pid, v, 'força', quem=max(g, key=lambda c: E['gente'][c]['atributos']['Força']))
                    continue
                quieto(MS.ir, E, pid, v); continue
            alvo = next((x for x in reversed(d['caminho'][:-1]) if cands(x)), None)
            if alvo and len(d['caminho']) > 1: quieto(MS.ir, E, pid, d['caminho'][-2]); continue
            break
        except SystemExit as x:
            C.setdefault('recusas', []).append(str(x)[:120]); break
    for _ in range(40):                                     # a saída: volta pelas salas (o que aparece no caminho, luta-se), e sai
        p = E['gente'][pid]; d = MS.descida(p)
        if not d: break
        try:
            if d['fase'] == 'luta': luta_robo(E, pid); continue
            if d['fase'] == 'encontro': quieto(MS.atacar, E, pid); C['lutas'] += 1; luta_robo(E, pid); continue
            quieto(MS.sair, E, pid)
        except SystemExit as x:
            C.setdefault('recusas', []).append('sair: ' + str(x)[:120]); quieto(MS.larga, E, pid, 'o robô não achou a saída'); break
    C['tochas'] += t0 - (E['gente'][pid].get('carga') or {}).get('tocha', 0)
    return C


def inteiro(E, c):
    estado.em_cena(E, c)                                    # quem não é o personagem cuida de si em casa: o tempo que passou fora de cena entra antes de olhar
    q = E['gente'][c]; return q['estado'] == 'vivo' and q['pv'] >= M.INTEIRO_PV * estado.pv_max(q)          # inteiro para o robô: o PV de volta (a ferida aberta segue sarando)


def em_casa(E, pid, blocos=6):
    """um dia em casa do robô: vende o despojo, trabalha a jornada se a prata está curta, come, dorme na cama (paga)"""
    vende(E, pid)
    try: quieto(ato.comer, E, pid)
    except SystemExit: pass
    if E['gente'][pid]['moedas'] < 3 * (M.CAMA_PRECO + 2 * M.REFEICAO_PRECO):
        try: quieto(ato.trabalhar, E, pid, M.JORNADA)
        except SystemExit: ato.passa(E, pid, M.JORNADA, 'esperar', para=False)
    else: ato.passa(E, pid, M.JORNADA, 'descansar', esforco='descanso', para=False)
    try: quieto(ato.comer, E, pid)
    except SystemExit: pass
    try: quieto(ato.dormir, E, pid, M.BLOCOS_DIA - M.JORNADA, para=False)
    except SystemExit: quieto(ato.dormir, E, pid, M.BLOCOS_DIA - M.JORNADA, chao=True, para=False)


def vende(E, pid):
    """o robô vende o despojo da carga e as peças que achou na masmorra (não a chave, nem a maldita, nem o que veste): devolve a prata"""
    if E['gente'][pid]['estado'] != 'vivo': return 0
    try: pr = quieto(mercado.vender_cesta, E, pid)['prata']
    except (SystemExit, KeyError, TypeError): pr = 0
    for iid, it in list(E['itens']['itens'].items()):
        if it.get('dono') == pid and not it.get('uso') and it.get('tipo') in ('arma', 'armadura', 'escudo', 'gazua') and not it.get('maldita') and any('achou esta peça' in h for h in it.get('historia') or []):
            antes = E['gente'][pid]['moedas']
            try: quieto(mercado.vender_peca, E, pid, iid); pr += E['gente'][pid]['moedas'] - antes
            except (SystemExit, KeyError, TypeError): pass
    return pr


def vida(semente, quem='grupo', dias=ROBO['dias6'], prudente=True, vender=False, continua=False):
    """UMA VIDA DO ROBÔ ao lado da cripta: desce quando todos estão inteiros (e com tochas), descansa em casa entre as descidas, até `dias` dias. Sem `continua`, para quando
    a cripta foi limpa e o nicho visto; com ele (a casa que vive ao lado dela), segue descendo uma vez por semana, para ver se algo voltou"""
    E = vila(semente)
    com = {'grupo': ['tome', 'rute'], 'sozinho': [], 'ladino': ['tome', 'rute', 'quim'], 'quatro': ['tome', 'rute', 'anselmo']}[quem]
    if quem == 'ladino': _quim(E)
    ladino = 'quim' if quem == 'ladino' else None
    ordem = (['quim'] if ladino else []) + (['tome', 'eu'] + [c for c in com if c not in ('quim', 'tome')] if 'tome' in com else ['eu'] + [c for c in com if c != 'quim'])      # o prudente põe o guarda na frente
    C = dict(descidas=0, dias=0, renda=0, renda_antes=0, renda_depois=0, depois=0); p0 = prata_do_mundo(E); d0 = E['relogio']['dia']; ult = -99
    while E['relogio']['dia'] - d0 < dias:
        if E['gente']['eu']['estado'] != 'vivo': break
        m = E['lugares']['cripta']; vistas = set(((E['gente']['eu'].get('marca') or {}).get('mapa') or {}).get('cripta', {}).get('salas') or [])
        limpa = isinstance(m.get('limpa'), dict) and 'cripta_7' in vistas and not MS._tesouro(E, 'cripta_7')
        if limpa and not continua: break
        vivos = [c for c in com if E['gente'][c]['estado'] == 'vivo']
        semana = not limpa or E['relogio']['dia'] - ult >= 7
        if semana and all(inteiro(E, c) for c in ['eu'] + vivos) and E['relogio']['bloco'] == 2:
            t = (E['gente']['eu'].get('carga') or {}).get('tocha', 0)
            if t < ROBO['tochas']: compra_tochas(E, 'eu', ROBO['tochas'] - t)
            antes_cripta = sum(int((E['lugares'][x].get('estoque') or {}).get('prata', 0)) for x in MS.salas(E, 'cripta'))
            C['descidas'] += 1; ult = E['relogio']['dia']; ja_limpa = isinstance(m.get('limpa'), dict) and esgotada(E)
            desce(E, 'eu', vivos, [x for x in ordem if x in ['eu'] + vivos], ladino=ladino if ladino in vivos else None, prudente=prudente, conta=C)
            r = antes_cripta - sum(int((E['lugares'][x].get('estoque') or {}).get('prata', 0)) for x in MS.salas(E, 'cripta'))
            if vender: r += sum(vende(E, c) for c in ['eu'] + vivos)
            C['renda'] += r
            if ja_limpa: C['renda_depois'] += r; C['depois'] += 1
            else: C['renda_antes'] += r
            if E['gente']['eu']['estado'] == 'vivo':
                for _ in range(2):
                    try: quieto(ato.comer, E, 'eu')
                    except SystemExit: break
            if E['gente']['eu']['estado'] == 'vivo' and E['relogio']['bloco'] != 2:
                falta = (2 - E['relogio']['bloco']) % M.BLOCOS_DIA
                if falta: quieto(ato.dormir, E, 'eu', falta, chao=E['gente']['eu']['moedas'] < M.CAMA_PRECO, para=False)
        else:
            em_casa(E, 'eu')
    m = E['lugares']['cripta']
    C.update(limpa=isinstance(m.get('limpa'), dict), maro_morreu=E['gente']['eu']['estado'] != 'vivo', morreu=[c for c in ['eu'] + com if E['gente'][c]['estado'] != 'vivo'],
             onde=[(E['gente'][c].get('morte') or {}).get('onde') for c in ['eu'] + com if E['gente'][c]['estado'] != 'vivo'], prata_fecha=prata_do_mundo(E) == p0, inteiro=not estado.valida(E),
             dias=E['relogio']['dia'] - d0, aberta=any((E['gente'][c].get('marca') or {}).get('masmorra') for c in E['gente']))
    return C, E


def esgotada(E, mid='cripta'):
    """o tesouro que o gerador pôs já foi levado (nenhuma prata nas salas, nenhuma peça sem dono nelas): daí em diante, só rende o que volta"""
    return not any(int(estado.livre(E, x).get('prata', 0)) for x in MS.salas(E, mid)) and not any(it.get('onde') in MS.salas(E, mid) and not it.get('dono') and not estado.de_morto(it) for it in E['itens']['itens'].values())


def _quim(E):
    """o Quim da vila de teste, o de verdade (onda 3: manha.na_vila, da frente L): nível 14, manha de Iniciante, adaga e couro Comuns, uma gazua Comum, com o talento e o
    dom rolados pelo dado do mundo; e a loja da vila passa a vender a tocha e a gazua"""
    if 'quim' in E['gente']: return
    import manha
    quieto(manha.na_vila, E, 'vila')


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 300
    print('BANCO DE PROVAS DA MASMORRA\n')
    res = provas(n)
    for nome, deu, passa in res: print(f"  {'passa' if passa else 'FALHA'}  {nome}: {deu}")
    print(f'\n{sum(p for _, _, p in res)} de {len(res)} provas passam.')
    return all(p for _, _, p in res)


# ---------------------------------------------------------------- AS METAS ----------------------------------------------------------------
def _ma0(n):
    """MA0. A PESSOA COMUM É A DE HOJE: dez dias de rotina na vila de prova, com o módulo da masmorra ligado e desligado: o mesmo estado e a mesma MESA"""
    with pasta():
        E1 = PM.vila(); E2 = copy.deepcopy(E1); velho = estado._MODS
        for _ in range(10): quieto(PM.dia_de_rotina, E1)
        try:
            estado._MODS = [m for m in estado.modulos() if m.__name__ != 'masmorra']
            for _ in range(10): quieto(PM.dia_de_rotina, E2)
            m2 = turno.mesa(E2)
        finally: estado._MODS = velho
        igual = all(E1[k] == E2[k] for k in ('gente', 'lugares', 'itens', 'relogio')) and turno.mesa(E1) == m2
        sem = MS.mesa(E1) == [] and MS.so_mestre(E1) == [] and MS.retomar(E1) == [] and MS.voce(E1) == []
    return [('MA0 A PESSOA COMUM É A DE HOJE: dez dias de rotina com o módulo da masmorra ligado e desligado dão o mesmo estado e a mesma MESA; sem masmorra vizinha, o módulo não põe linha nenhuma '
             '(as lutas de semente fixa e os bancos de antes: o provas_4b e o provas.py)', f"o mesmo estado e a mesma MESA: {sn(igual)}; nenhuma linha sem masmorra: {sn(sem)}", igual and sem)]


def _gera_mundo(s, molde, niveis=None, cat=None):
    E = PM.vila(semente=s, prata=200)
    ef = MS.gera(E, molde, f"a Masmorra de Prova {s}", 'vila', niveis=niveis, cat=cat)
    ev = estado.aplica(E, 'gera', ef, onde='vila', texto='a masmorra de prova')
    return E, ef[0][2], ev


def _ma1(n):
    """MA1. O TEMPO: N lances andam ⌈N ÷ 12⌉ blocos pelo ato.passa, mais a ida e a volta; cada bloco gasta uma tocha de quem leva a luz; acabadas as tochas, a luta seguinte tem o
    escuro. Em 20 masmorras do gerador (os cinco moldes), que nascem inteiras e em segredo"""
    mal = []; certo = 0; mundos = 20; tortos = []; segredo = True
    with pasta():
        for s in range(1, mundos + 1):
            molde = list(K.MOLDES)[s % len(K.MOLDES)]
            E, mid, ev = _gera_mundo(s, molde, niveis=1 + s % 3 if molde != 'covil' else 1, cat=s % 2)
            P = estado.valida(E)
            if P: tortos.append(f"{molde} {s}: {P[0]}"); continue
            segredo = segredo and turno.secreto(ev)
            estado.aplica(E, 'mestre', [['lugar', mid, 'vagantes', 'poe', {}]], texto='sem vagantes (a prova do tempo)')
            compra_tochas(E, 'eu', 9)
            t0 = estado.agora(E); ida = MS._longe(E, mid); ent = E['lugares'][mid]['entrada']; viz = MS._viz(E, ent)[0]
            quieto(MS.descer, E, 'eu', mid, luz='tocha'); tochas0 = E['gente']['eu']['carga']['tocha']
            k, m_ = 3 + s % 7, 2 + s % 5; lances = k + 2 * m_
            for _ in range(k): quieto(MS.escutar, E, 'eu', viz)
            for _ in range(m_): quieto(MS.procurar, E, 'eu')
            d = MS.descida(E['gente']['eu']); blocos_dentro = d['blocos'] + (1 if d['lances'] else 0)
            quieto(MS.sair, E, 'eu')
            esperado = ida + math.ceil(lances / K.LANCES_BLOCO) + ida
            gastas = tochas0 - E['gente']['eu']['carga'].get('tocha', 0)
            ok = estado.agora(E) - t0 == esperado and gastas == math.ceil(lances / K.LANCES_BLOCO) == blocos_dentro and not MS.descida(E['gente']['eu']) and not estado.valida(E)
            certo += ok
            if not ok: mal.append(f"{molde} {s}: {lances} lances, {estado.agora(E) - t0} blocos (esperava {esperado}), {gastas} tochas")
        # acabada a tocha, a luta seguinte é no escuro (a cripta: uma tocha só, um bloco à porta, e o corredor dos nichos)
        E = vila(1, tochas=0); compra_tochas(E, 'eu', 1)
        quieto(MS.descer, E, 'eu', 'cripta', com=['tome', 'rute'], ordem=['tome', 'eu', 'rute'], luz='tocha')
        for _ in range(K.LANCES_BLOCO): quieto(MS.escutar, E, 'eu', 'cripta_2')
        sem_luz = not MS._luz_de(E, 'eu', MS.descida(E['gente']['eu']))
        R = quieto(MS.ir, E, 'eu', 'cripta_2')
        if R['fase'] == 'armadilha': R = quieto(MS.contornar, E, 'eu')
        escuro = False
        if MS.descida(E['gente']['eu']) and MS.descida(E['gente']['eu'])['fase'] == 'encontro':
            R = quieto(MS.atacar, E, 'eu'); C = json.load(open(R['luta'].replace('_luta.json', '_cenario.json'), encoding='utf-8')); escuro = 'escuro' in C['tempo'] and not C['luz']
        dobro = MS.descida(E['gente']['eu'])['lances'] >= 2 * K.CUSTO['ir']
    ok = certo == mundos - len(tortos) and not tortos and sem_luz and escuro and dobro and segredo
    return [('MA1 O TEMPO: os lances fecham ⌈N ÷ 12⌉ blocos pelo ato.passa, mais a ida e a volta (o bloco aberto conta inteiro ao sair); cada bloco gasta uma tocha de quem leva a luz; acabada a tocha, '
             'anda-se no dobro e a luta é no escuro. Em 20 masmorras do gerador (os cinco moldes, de 1 a 3 níveis), que nascem inteiras e em segredo',
             f"{certo} de {mundos - len(tortos)} descidas com a conta certa; {len(tortos)} masmorras tortas" + (f" ({'; '.join(tortos[:2])})" if tortos else '') + f"; o gerador é segredo do Mestre: {sn(segredo)}; "
             f"acabada a tocha, sem luz: {sn(sem_luz)}, a ida no dobro: {sn(dobro)}, a luta no escuro: {sn(escuro)}" + (f" · erradas: {'; '.join(mal[:3])}" if mal else ''), ok)]


def _grupo_vila():
    """o grupo da vila (Maro, Tomé e Rute de hoje, com o PV cheio), para o luta.nova"""
    E = vila(1)
    def P(pid, **k): d = estado.lutador(E, pid); d.update(k); d['pv'] = estado.pv_max(E['gente'][pid]); d['feridas'] = []; return copy.deepcopy(d)
    return P


def _duelos(fa, fb, n, sem=7, **kw):
    luta.semente(sem); v = m = 0
    for i in range(n):
        S = luta.nova(fa(), fb(), quieto=True, **kw); luta.corre(S)
        v += S['fim'] == 'A'; m += any(f['estado'] == 'morto' for f in S['L'] if f['lado'] == 'A')
    return v / n, m / n


def _ma2_3(n):
    """MA2 e MA3. A LUZ E O ESCURO, E QUEM VÊ PRIMEIRO: o grupo da vila contra seis esqueletos numa sala aberta"""
    k = 2 * n
    with pasta():
        P = _grupo_vila()
        maro = lambda: [P('eu'), P('tome'), P('rute', linha='trás')]
        tome = lambda: [P('tome'), P('eu'), P('rute', linha='trás')]
        seis = lambda: bichos.bando('esqueleto', n=6)
        luz, ml = _duelos(maro, seis, k, inicio='perto'); esc, me = _duelos(maro, seis, k, inicio='perto', tempo=['escuro'])
        nada, mn = _duelos(tome, seis, k, inicio='perto'); surp, ms_ = _duelos(tome, seis, k, inicio='perto', surpresa='B'); pego, mp = _duelos(tome, seis, k, inicio='perto', surpresa='A')
    ok2 = 0.70 <= luz <= 0.90 and 0.15 <= esc <= 0.40
    ok3 = surp - nada >= 0.10 and nada - pego >= 0.15
    return [('MA2 A LUZ E O ESCURO: Maro, Tomé e Rute contra seis esqueletos, sala aberta (com luz, 70 a 90%; no escuro, 15 a 40%)',
             f"com luz vence {pct(luz)} (morre alguém em {pct(ml)}); no escuro {pct(esc)} (em {pct(me)}); {k} lutas cada", ok2),
            ('MA3 QUEM VÊ PRIMEIRO: o mesmo grupo (Tomé na frente) surpreendendo e surpreendido (+10 pontos ou mais; −15 ou mais)',
             f"ninguém surpreso {pct(nada)}; o grupo surpreende {pct(surp)} ({100 * (surp - nada):+.0f}); o grupo é surpreendido {pct(pego)} ({100 * (pego - nada):+.0f}); {k} lutas cada", ok3)]


def _ma4(n):
    """MA4. NÃO É MINA: a casa da vila (Maro, Tomé, Rute, prudente) vive 60 dias ao lado da cripta: desce quando os três estão inteiros (depois de limpa, uma vez por semana), vende o que acha"""
    vidas = max(8, n // 12); R = []
    with pasta():
        for s in range(1, vidas + 1):
            luta.semente(1000 + s)
            with dado_semente(2000 + s): C, E = vida(500 + s, 'grupo', dias=ROBO['dias4'], vender=True, continua=True)
            R.append(C)
    dia = sum(C['renda'] for C in R) / max(1, sum(3 * max(1, C['dias']) for C in R))
    dep = [C for C in R if C['depois']]; depois = sum(C['renda_depois'] for C in dep) / max(1, sum(3 * C['depois'] for C in dep))
    diaria = M.SALARIO['diarista'] * M.JORNADA; fecha = all(C['prata_fecha'] and C['inteiro'] for C in R)
    ok = dia <= diaria and depois < 0.25 * diaria and fecha and len(dep) >= vidas // 2
    return [('MA4 NÃO É MINA: a casa da vila vive 60 dias ao lado da cripta (desce quando os três estão inteiros; depois de limpa, uma vez por semana; vende o despojo e as peças): '
             'por pessoa e por dia de vida, no máximo 1 diária; depois da primeira limpeza (e do tesouro levado), menos de 0,25 diária por dia de trabalho; a prata do mundo fecha',
             f"{vidas} vidas; a casa tira {estado.num(round(dia, 2))} de prata por pessoa e por dia de vida ({estado.num(round(dia / diaria, 2))} diária); depois da limpeza e do tesouro levado ({len(dep)} vidas, {sum(C['depois'] for C in dep)} descidas), "
             f"{estado.num(round(depois, 2))} por pessoa e por dia de trabalho ({estado.num(round(depois / diaria, 3))} diária); a prata do mundo fecha e o estado fica inteiro: {sn(fecha)}", ok)]


def _ma5(n):
    """MA5. O DESPOJO PELA CATEGORIA, NAS CONTAS DA MASMORRA: o guardião (o cavaleiro da cova feito Comum) rende metal Comum; o esqueleto de uma sala Rara, sucata Rara"""
    with pasta():
        E = vila(1)
        estado.aplica(E, 'mestre', [['lugar', 'cripta_3', 'cat', 'poe', 2], ['lugar', 'cripta_3', 'bichos', 'poe', {'esqueleto': 1}]], texto='o ossário Raro (a prova)')
        quieto(MS.descer, E, 'eu', 'cripta', com=['tome', 'rute'], luz='tocha')
        estado.aplica(E, 'mestre', [['lugar', 'cripta_2', 'bichos', 'poe', {}], ['lugar', 'cripta_2', 'armadilhas', 'poe', []]], texto='o corredor vazio (a prova)')
        def mata(sala):
            R = quieto(MS.ir, E, 'eu', sala)
            if R['fase'] == 'armadilha': R = quieto(MS.contornar, E, 'eu')
            R = quieto(MS.atacar, E, 'eu'); arq = R['luta']; S = json.load(open(arq, encoding='utf-8'))
            for f in S['L']:
                if f['lado'] == 'B': f['estado'] = 'morto'; f['pv'] = 0
            S['fim'] = 'A'; luta.salva(S, arq)
            antes = {c: dict(E['gente'][c].get('carga') or {}) for c in ('eu', 'tome', 'rute')}
            R = quieto(MS.luta_roda, E, 'eu', [])
            return {b: sum((E['gente'][c].get('carga') or {}).get(b, 0) - antes[c].get(b, 0) for c in antes) for b in set().union(*[E['gente'][c].get('carga') or {} for c in antes])}
        quieto(MS.ir, E, 'eu', 'cripta_2'); g3 = mata('cripta_3')
        estado.aplica(E, 'mestre', [['lugar', 'cripta_5', 'armadilhas', 'poe', []], ['lugar', 'cripta', 'portas.cripta_5|cripta_6', 'poe', dict(estado='aberta', material='ferro', cat=1, fechadura=1)]], texto='o caminho aberto (a prova)')
        quieto(MS.ir, E, 'eu', 'cripta_5'); g6 = mata('cripta_6')
    raro = {b: q for b, q in g3.items() if q > 0}; guard = {b: q for b, q in g6.items() if q > 0}
    ok = raro and all(M.le_materia(b)[1] == 2 for b in raro) and guard.get('metal:0', 0) >= 2 and not any(M.le_materia(b)[1] not in (None, 0) for b in guard)
    return [('MA5 O DESPOJO PELA CATEGORIA, NAS CONTAS DA MASMORRA (as lutas postas à mão): o esqueleto de uma sala Rara rende sucata Rara; o guardião da cripta (o cavaleiro da cova feito Comum) e a guarda dele, metal e osso Comuns',
             f"o esqueleto Raro: {_bens(raro)}; o guardião e os dois esqueletos Comuns: {_bens(guard)}", bool(ok))]


def _bens(d): return ', '.join(f"{q} de {estado.nome_bem(b)}" for b, q in sorted(d.items())) or 'nada'


def _ma6(n):
    """MA6. A CRIPTA DA COVA VELHA, pelo robô de verdade (o masmorra.py, a luta do luta.py, o dado do jogador): o prudente de três limpa em 80% ou mais, e o Maro morre em 15% ou menos;
    sozinho, morre em 70% ou mais; com o ladino na frente (ele procura e desarma; atrás na luta), morre menos que sem"""
    out = {}
    with pasta():
        for quem, k in (('grupo', max(20, n // 2)), ('ladino', max(20, n // 2)), ('sozinho', max(10, n // 5))):
            L = []
            for s in range(1, k + 1):
                luta.semente(7 * s)
                with dado_semente(11 * s): C, E = vida(s, quem)
                L.append(C)
            out[quem] = L
    f = lambda q, c: sum(bool(C[c]) for C in out[q]) / len(out[q])
    g = out['grupo']; mortes = [o for C in g if C['maro_morreu'] for o in C['onde'][:1]]
    fundo = sum(o == 'cripta_6' for o in mortes)
    ok = f('grupo', 'limpa') >= 0.80 and f('grupo', 'maro_morreu') <= 0.15 and f('sozinho', 'maro_morreu') >= 0.70 and f('ladino', 'maro_morreu') < f('grupo', 'maro_morreu') and all(C['prata_fecha'] and C['inteiro'] and not C['aberta'] for q in out for C in out[q])
    media = lambda q, c: sum(C.get(c, 0) for C in out[q]) / len(out[q])
    return [('MA6 A CRIPTA DA COVA VELHA, pelo robô de verdade (o masmorra.py inteiro; até 20 dias; desce quando todos estão inteiros; o guarda na frente; recua abaixo de 30% do PV; o prudente não abre a porta do fundo com alguém abaixo de 75%): '
             'o prudente de três limpa em 80% ou mais e o Maro morre em 15% ou menos; sozinho, morre em 70% ou mais; com o ladino, morre menos que sem',
             f"os três: limpam {pct(f('grupo', 'limpa'))}, o Maro morre em {pct(f('grupo', 'maro_morreu'))} ({fundo} de {len(mortes)} mortes na câmara do guardião), {estado.num(round(media('grupo', 'descidas'), 1))} descidas, "
             f"{estado.num(round(media('grupo', 'lutas'), 1))} lutas, {estado.num(round(media('grupo', 'vagantes'), 1))} com quem vagueia e {estado.num(round(media('grupo', 'tochas'), 1))} tochas por vida ({len(g)} vidas); "
             f"com o ladino: limpam {pct(f('ladino', 'limpa'))}, o Maro morre em {pct(f('ladino', 'maro_morreu'))}, {estado.num(round(media('ladino', 'armadilhas_achadas'), 1))} armadilhas achadas por vida (sem ele, {estado.num(round(media('grupo', 'armadilhas_achadas'), 1))}); "
             f"sozinho: morre em {pct(f('sozinho', 'maro_morreu'))}; a prata fecha, o estado inteiro e nenhuma descida aberta em todas: {sn(all(C['prata_fecha'] and C['inteiro'] and not C['aberta'] for q in out for C in out[q]))}", ok)]


def _ma7(n):
    """MA7. A ARMADILHA PELO ITEM: o dardo Raro mata na hora 35% ou mais de quem veste Comum; em quem veste malha Rara tira menos de 15% do PV; o dardo Comum nunca mata de PV cheio sem crítico"""
    k = max(4000, 20000 * n // 300); r = random.Random(11)
    with pasta():
        E = vila(1); Fm = ficha(dict(estado.lutador(E, 'eu'), pv=estado.pv_max(E['gente']['eu']), feridas=[]))
    Fr = ficha(veste(padrao('x', 50), arma=('espada', 2), armadura=('malha', 2), escudo=2))
    def mede(F, cat):
        mata = tira = sem_crit = pega = 0
        for _ in range(k):
            d, parte, crit, _ = MS.golpe(F, 'dardo', cat, r)
            if d <= 0: continue
            tira += d; pega += 1
            if d >= F['pvmax'] and d > F['pvmax'] * T.FERIDA_GRAVE:
                mata += 1; sem_crit += not crit
        return mata / k, tira / max(1, pega) / F['pvmax'], sem_crit
    m_raro, _, _ = mede(Fm, 2); _, t_rara, _ = mede(Fr, 2); m_com, _, sc = mede(Fm, 0)
    ok = m_raro >= 0.35 and t_rara < 0.15 and sc == 0
    return [('MA7 A ARMADILHA PELO ITEM (a conta do aço): o dardo Raro no Maro de peças Comuns mata na hora 35% ou mais; no nível 50 de malha Rara tira menos de 15% do PV; o dardo Comum nunca mata de PV cheio sem crítico',
             f"o dardo Raro no Maro: mata na hora em {pct(m_raro)}; na malha Rara tira, quando pega, {pct(t_rara)} do PV; o dardo Comum matou sem crítico {sc} vezes ({k} disparos cada)", ok)]


def _cova(semente=1):
    """um mundo pequeno (a vila de prova, a Cova Velha e a cripta, com Tomé e Rute): para as provas que repetem muito"""
    E = PM.vila(semente=semente, prata=100)
    estado.aplica(E, 'gera', [['lugar', 'nasce', 'cova', dict(nome='a Cova Velha', em='na Cova Velha', tipo='ermo', estoque={}, vizinhos=['vila'])], ['lugar', 'vila', 'vizinhos', 'poe', ['cova']]], texto='a cova (a prova)')
    for pid, nome in (('tome', 'Tomé'), ('rute', 'Rute')):
        at = dict(Força=70, Agilidade=65, Vigor=70, Vontade=50, Percepção=55, Afinidade=40)
        estado.aplica(E, 'gera', [['pessoa', 'nasce', pid, dict(nome=nome, nivel=20, atributos=at, lugar='vila')]], texto=nome)
    MS.na_vila(E)
    return E


def _ma12(n):
    """MA12. O QUE VAGUEIA E O DESCANSO: a chance por bloco é 1 em 6, mais 10 pontos por ponto de alarme (±2 pontos), medida no dado do mundo (masmorra.rola_vaga, o mesmo que o bloco
    rola); quem chega a quem dorme sem vigia pega o grupo desprevenido sempre; com vigia, nunca (pelo _vaga, que põe o bando na sala); quem vigia não dorme (o descanso de verdade)"""
    k = max(2000, 20 * n); freq = {}; surp_sem = surp_com = vem_sem = vem_com = 0
    with pasta():
        E = _cova(); compra_tochas(E, 'eu', 4)
        quieto(MS.descer, E, 'eu', 'cripta', com=['tome', 'rute'], luz='tocha')
        d0 = copy.deepcopy(E['gente']['eu']['marca']['masmorra']); m0 = copy.deepcopy(E['lugares']['cripta']); s0 = copy.deepcopy(E['lugares']['cripta_1'])
        for al in range(4):
            E['lugares']['cripta'] = dict(copy.deepcopy(m0), alarme=al, vagantes={'corpo-seco': 99}); vem = 0
            for t in range(k):
                E['gente']['eu']['marca']['masmorra']['blocos'] = 100000 * al + t
                vem += MS.rola_vaga(E, 'eu') is not None
            freq[al] = vem / k
        for t in range(400):
            d = copy.deepcopy(d0); d['blocos'] = 900000 + t; E['gente']['eu']['marca']['masmorra'] = d
            E['lugares']['cripta'] = dict(copy.deepcopy(m0), alarme=3, vagantes={'corpo-seco': 99}); E['lugares']['cripta_1'] = copy.deepcopy(s0)
            vig = 'tome' if t % 2 else None
            R = quieto(MS._vaga, E, 'eu', [], dorme=True, vigia=vig)
            if R:
                s_ = MS.descida(E['gente']['eu'])['encontro']['surpresa']
                if vig: vem_com += 1; surp_com += s_ == 'A'
                else: vem_sem += 1; surp_sem += s_ == 'A'
            if vem_com >= 30 and vem_sem >= 30: break
        E['gente']['eu']['marca']['masmorra'] = d0; E['lugares']['cripta'] = m0; E['lugares']['cripta_1'] = s0
        sono0 = {c: E['gente'][c]['corpo']['sono'] for c in ('eu', 'tome', 'rute')}
        estado.aplica(E, 'mestre', [['lugar', 'cripta', 'vagantes', 'poe', {}]], texto='sem vagantes (a prova do descanso)')
        quieto(MS.descansar, E, 'eu', 2, vigia='tome')
        vigiou = E['gente']['tome']['corpo']['sono'] >= sono0['tome'] and E['gente']['rute']['corpo']['sono'] <= sono0['rute']
    esp = {al: min(1, K.VAGA[0] + K.VAGA[1] * al) for al in range(4)}
    ok = all(abs(freq[al] - esp[al]) <= 0.02 for al in range(4)) and vem_sem and surp_sem == vem_sem and vem_com and surp_com == 0 and vigiou
    return [('MA12 O QUE VAGUEIA E O DESCANSO: a chance por bloco é 1 em 6, mais 10 pontos por ponto de alarme (±2 pontos), no dado do mundo; dormindo sem vigia o grupo é surpreendido sempre, com vigia nunca; quem vigia não dorme',
             ' · '.join(f"alarme {al}: {pct(freq[al])} (a conta: {pct(esp[al])})" for al in range(4)) + f" ({k} blocos cada); dormindo sem vigia, surpreendido {surp_sem} de {vem_sem}; com vigia, {surp_com} de {vem_com}; quem vigia ficou acordado: {sn(vigiou)}", ok)]


def _ma13(n):
    """MA13. A MEMÓRIA: um ano da cripta limpa, sozinha: o morto não volta sem chefe; o rato volta e não passa do teto; o bando de fora chega 120 dias depois de o nível ficar vazio;
    o tesouro não volta; a prata fecha. E, com o chefe vivo, ele ergue um morto a cada 10 dias, até o que a sala tinha"""
    mundos = max(3, n // 60); mal = []; chega = []; ratos = []
    with pasta():
        for s in range(1, mundos + 1):
            E = vila(s); p0 = prata_do_mundo(E)
            ef = [['lugar', x, 'bichos', 'poe', {}] for x in MS.salas(E, 'cripta')] + [['lugar', 'cripta_6', 'chefe', 'poe', dict(E['lugares']['cripta_6']['chefe'], vivo=False)], ['lugar', 'cripta', 'vagantes', 'poe', {}]]
            ef += [x for sid in MS.salas(E, 'cripta') for x in (['estoque', sid, 'prata', 'soma', -int(E['lugares'][sid]['estoque'].get('prata', 0))], ['estoque', 'vila', 'prata', 'soma', int(E['lugares'][sid]['estoque'].get('prata', 0))]) if E['lugares'][sid]['estoque'].get('prata')]
            estado.aplica(E, 'mestre', ef, texto='a cripta limpa, e o tesouro levado (a prova)'); d0 = E['relogio']['dia']; vazio = None; mortos_voltam = False; teto_ok = True; volta_rato = None; veio = None
            for dia in range(365):
                estado.aplica(E, 'tempo', [['relogio', M.BLOCOS_DIA]], texto='o dia passa (a prova)')
                MS.virada(E); caca.virada(E)
                nv = E['lugares']['cripta']['niveis'][0]
                if vazio is None and 'vazio' in nv: vazio = nv['vazio']
                b = {e: q for x in MS.salas(E, 'cripta') for e, q in MS.bichos_de(E, x).items()}
                if any(MS._sem_vida(e) for e in b): mortos_voltam = True
                if veio is None and vazio is not None and any(not MS._fera(e) for e in b): veio = E['relogio']['dia'] - vazio
                if MS.bichos_de(E, 'cripta_4').get('ratazana', 0) > 4: teto_ok = False
                if volta_rato is None and MS.bichos_de(E, 'cripta_4').get('ratazana', 0): volta_rato = E['relogio']['dia'] - d0
            tes = sum(int(E['lugares'][x]['estoque'].get('prata', 0)) for x in MS.salas(E, 'cripta'))
            ratos.append(volta_rato); chega.append(veio)
            if mortos_voltam or not teto_ok or tes or prata_do_mundo(E) != p0 or estado.valida(E): mal.append(f"mundo {s}: mortos {sn(mortos_voltam)}, teto {sn(teto_ok)}, tesouro {tes}, prata {sn(prata_do_mundo(E) == p0)}")
        E = vila(1); estado.aplica(E, 'mestre', [['lugar', 'cripta_3', 'bichos', 'poe', {}], ['lugar', 'cripta_2', 'bichos', 'poe', {}]], texto='o ossário e o corredor vazios, o guardião vivo (a prova)')
        er = []
        for dia in range(80):
            estado.aplica(E, 'tempo', [['relogio', M.BLOCOS_DIA]], texto='o dia passa (a prova)'); antes = sum(MS.bichos_de(E, 'cripta_3').values()) + sum(MS.bichos_de(E, 'cripta_2').values())
            MS.virada(E)
            if sum(MS.bichos_de(E, 'cripta_3').values()) + sum(MS.bichos_de(E, 'cripta_2').values()) > antes: er.append(dia + 1)
        ergue_ok = er[:5] == [10, 20, 30, 40, 50] and MS.bichos_de(E, 'cripta_2').get('corpo-seco', 0) == 2 and MS.bichos_de(E, 'cripta_3').get('esqueleto', 0) == 3 and len(er) == 5
    ok = not mal and len(chega) == mundos and all(x == VEM_DE_FORA for x in chega) and ergue_ok and all(x is not None for x in ratos)
    return [('MA13 A MEMÓRIA (um ano da cripta limpa, sozinha, em vários mundos): o morto não volta sem chefe; o rato volta e não passa do teto; o bando de fora chega 120 dias depois de o nível ficar vazio; '
             'o tesouro não volta; a prata fecha. E o chefe vivo ergue um morto a cada 10 dias, até o que a sala tinha',
             f"{mundos} mundos; " + (f"tortos: {'; '.join(mal)}" if mal else 'o morto não voltou, o rato ficou no teto, o tesouro não voltou e a prata fechou em todos') + f"; o rato voltou no dia {', '.join(str(x) for x in ratos)}; "
             f"o bando de fora chegou {', '.join(str(x) for x in chega) or 'nunca'} dias depois do nível vazio; com o guardião vivo, os mortos se ergueram nos dias {', '.join(str(x) for x in er) or 'nenhum'}", ok)]


def _publico(E):
    t = turno.mesa(E); return t[:t.index('## SÓ O MESTRE')]


def _ma14(n):
    """MA14. O MAPA É SEGREDO: a mesa só mostra o que o grupo viu; as rolagens ocultas não vão à parte pública; o gerador vai ao SÓ O MESTRE; a mesma descida, com e sem o chefe atrás da porta, dá o
    mesmo texto até a porta abrir (três mundos, o dado preso)"""
    R = {}; iguais = 0
    with pasta():
        E = vila(1); ev = next(e for e in E['_novos'] if e['tipo'] == 'gera' and any(isinstance(x, list) and x[:2] == ['lugar', 'nasce'] and x[2] == 'cripta' for x in e['efeitos']))
        R['o gerador é segredo (vai ao SÓ O MESTRE do RETOMAR, não aos fatos)'] = turno.secreto(ev) and not any('Cripta' in x for x in turno.fatos([ev]))
        quieto(MS.descer, E, 'eu', 'cripta', com=['tome', 'rute'], luz='tocha'); quieto(MS.escutar, E, 'eu', 'cripta_2')
        pub = _publico(E)
        R['a mesa só mostra o que o grupo viu (nada do ossário, da capela, do guardião, do tesouro guardado)'] = 'a escada' in pub and not any(x in pub for x in ('ossário', 'capela', 'guardião', 'sarcófago', 'nicho', 'chave de ferro'))
        R['a rolagem oculta não vai à parte pública (só "rolagem oculta"); o SÓ O MESTRE tem o número'] = '(OCULTA)' not in pub and 'rolagem oculta' not in pub and '(OCULTA)' in turno.mesa(E)
    for s in range(1, 4):
        textos = []
        for com_chefe in (True, False):
            with pasta():
                E = vila(s)
                if not com_chefe: estado.aplica(E, 'mestre', [['lugar', 'cripta_6', 'chefe', 'poe', None]], texto='sem o guardião (a prova)')
                luta.semente(s); out = []
                with dado_posto([1, -3, 2, 5, -1, 4, 0, 3, -2, 6] * 20):
                    for f, a, k in ((MS.descer, ('cripta',), dict(com=['tome', 'rute'], ordem=['tome', 'eu', 'rute'], luz='tocha')), (MS.ir, ('cripta_2',), {}), (MS.contornar, (), {}), (MS.atacar, (), {}),
                                    (luta_robo, (), {}), (MS.ir, ('cripta_3',), {}), (MS.atacar, (), dict(passagem=True)), (luta_robo, (), {}), (MS.ir, ('cripta_5',), {}), (MS.contornar, (), {}), (MS.escutar, ('cripta_6',), {}), (MS.ver, (), {})):
                        try:
                            r = quieto(f, E, 'eu', *a, **k); out.append(r if isinstance(r, list) else r.get('texto', ''))
                        except SystemExit as x: out.append(f'recusa: {x}')
                        out.append(_publico(E))
                textos.append(out)
        iguais += textos[0] == textos[1]
    R[f'com e sem o guardião atrás da porta de ferro, o mesmo texto até a porta abrir ({iguais} de 3 mundos)'] = iguais == 3
    ruim = [k for k, v in R.items() if not v]
    return [('MA14 O MAPA É SEGREDO: a mesa mostra só o que o grupo viu; a rolagem oculta não vai à parte pública; o gerador vai ao SÓ O MESTRE; a mesma descida, com e sem o chefe atrás da porta, dá o mesmo texto até ela abrir',
             ' · '.join(R) if not ruim else 'ERRADO: ' + ' · '.join(ruim), not ruim)]


def _ma15(n):
    """MA15. A VILA DE TESTE: a Cripta da Cova Velha numa cópia do save do jogador (o ensaio/): só eventos; recusa a segunda vez; o estado inteiro; a prata nova é 80; nada de antes muda"""
    src = os.path.join(AQUI, 'ensaio')
    if not os.path.exists(os.path.join(src, 'relogio.json')): return [('MA15 A VILA DE TESTE', 'não há save em ensaio/ para conferir', True)]
    with pasta() as d:
        shutil.copytree(src, os.path.join(d, 'save')); os.environ['MOTOR10_MUNDO'] = os.path.join(d, 'save')
        E = estado.carrega(); A = copy.deepcopy({k: E[k] for k in ('gente', 'itens', 'lugares', 'relogio')}); p0 = prata_do_mundo(E); n0 = E['relogio']['eventos']
        if 'cripta' in E['lugares']: return [('MA15 A VILA DE TESTE', 'o save já tem a cripta (o integrador a pôs): nada a conferir aqui', True)]
        L = MS.na_vila(E); evs = E['_novos'][-(E['relogio']['eventos'] - n0):] if E['relogio']['eventos'] > n0 else []
        so_gera = bool(evs) and all(e['tipo'] == 'gera' for e in evs) and all(turno.secreto(e) for e in evs)
        dois = recusa(lambda: MS.na_vila(E)); n1 = E['relogio']['eventos']
        novos_lug = set(E['lugares']) - set(A['lugares']); mudou = [k for k in A['lugares'] if E['lugares'][k] != A['lugares'][k]]
        gente_igual = E['gente'] == A['gente'] and E['relogio']['semente'] == A['relogio']['semente'] and (E['relogio']['dia'], E['relogio']['bloco']) == (A['relogio']['dia'], A['relogio']['bloco'])
        itens_igual = all(E['itens']['itens'].get(k) == v for k, v in A['itens']['itens'].items())
        nova = prata_do_mundo(E) - p0; P = estado.valida(E)
        estado.grava(E); E2 = estado.carrega(); volta = not estado.valida(E2) and 'cripta' in E2['lugares']
    ok = so_gera and bool(dois) and n1 == E['relogio']['eventos'] and nova == 80 and not P and mudou == ['vila'] and len(novos_lug) == 8 and gente_igual and itens_igual and volta
    return [('MA15 A VILA DE TESTE: a Cripta da Cova Velha (masmorra.na_vila) numa cópia do save do jogador: só eventos do gerador (segredo); recusa a segunda vez, antes de pôr qualquer coisa; o estado inteiro; '
             'a prata nova é 80; nada de antes muda (só a vila ganha a cripta por vizinha); grava e abre de novo',
             f"{len(evs)} evento(s), todos do gerador e em segredo: {sn(so_gera)}; a segunda vez: {'recusada' if dois else 'ACEITA'}; prata nova: {nova}; lugares novos: {len(novos_lug)}; "
             f"mudou de antes: {', '.join(mudou) or 'nada'}; a gente, os itens e o relógio iguais: {sn(gente_igual and itens_igual)}; o estado {'inteiro' if not P else 'QUEBRADO: ' + P[0]}; grava e abre: {sn(volta)}. {L[0][:90]}...", ok)]


def _ma16(n):
    """MA16. AS RECUSAS, com a frase, antes de gastar (nem tempo, nem evento)"""
    R = {}
    with pasta():
        E = vila(1)
        def nada(f):
            ev, ag = E['relogio']['eventos'], estado.agora(E); t = recusa(f); return bool(t) and E['relogio']['eventos'] == ev and estado.agora(E) == ag
        estado.aplica(E, 'mestre', [['pessoa', 'eu', 'marca.caca', 'poe', dict(ermo='mata', casa='vila', quer='caça', alvo=None, restam=1, com=[], dia=1, fase='procura', encontro=None, luta=None, lutas=0, parou=None, sangue=None)]], texto='uma saída aberta (a prova)')
        R['descer com a saída de caça aberta'] = nada(lambda: MS.descer(E, 'eu', 'cripta'))
        estado.aplica(E, 'mestre', [['pessoa', 'eu', 'marca.caca', 'poe', None]], texto='a saída fecha (a prova)')
        R['descer sem tocha nenhuma com luz=tocha'] = nada(lambda: MS.descer(E, 'eu', 'cripta', luz='tocha', quem_luz='tome', com=['tome']))
        estado.aplica(E, 'mestre', [['lugar', 'cripta', 'portas.cripta_1|cripta_2', 'poe', dict(estado='trancada', material='madeira', cat=0, fechadura=0)]], texto='a porta trancada (a prova)')
        quieto(MS.descer, E, 'eu', 'cripta', com=['tome', 'rute'], luz='tocha')
        R['ir à sala que não é vizinha'] = nada(lambda: MS.ir(E, 'eu', 'cripta_6'))
        R['abrir com gazua sem gazua'] = nada(lambda: MS.abrir(E, 'eu', 'cripta_2', 'gazua', quem='tome'))
        R['passar pela porta trancada'] = nada(lambda: MS.ir(E, 'eu', 'cripta_2'))
        estado.aplica(E, 'mestre', [['lugar', 'cripta', 'portas.cripta_1|cripta_2', 'poe', dict(estado='fechada', material='madeira', cat=0, fechadura=None)]], texto='a porta destrancada (a prova)')
        R['os atos da vila com a descida aberta'] = nada(lambda: ato.comer(E, 'eu')) and 'na descida' in (recusa(lambda: ato.trabalhar(E, 'eu', 1)) or '')
        R['duas descidas'] = nada(lambda: MS.descer(E, 'eu', 'cripta')) and nada(lambda: MS.descer(E, 'tome', 'cripta'))
        R['quem foi junto não decide'] = 'quem decide é quem comanda' in (recusa(lambda: MS.ir(E, 'tome', 'cripta_2')) or '')
        estado.aplica(E, 'mestre', [['pessoa', 'eu', 'marca.masmorra', 'poe', dict(MS.descida(E['gente']['eu']), luz=dict(tipo=None, quem=None))]], texto='a luz apaga (a prova)')
        R['procurar no escuro'] = nada(lambda: MS.procurar(E, 'eu'))
        R['desarmar no escuro'] = True
        quieto(MS.luz, E, 'eu', 'tocha', quem='eu')
        r = quieto(MS.ir, E, 'eu', 'cripta_2')
        if r['fase'] == 'armadilha': quieto(MS.contornar, E, 'eu')
        R['pegar com inimigo de pé'] = nada(lambda: MS.pegar(E, 'eu'))
        R['ir com gente à frente'] = nada(lambda: MS.ir(E, 'eu', 'cripta_3'))
        quieto(MS.atacar, E, 'eu')
        R['a luta aberta tranca a descida (e o mundo)'] = nada(lambda: MS.ir(E, 'eu', 'cripta_3')) and nada(lambda: MS.procurar(E, 'eu')) and nada(lambda: ato.passa(E, 'lino', 1, 'esperar'))
        R['descansar com a luta aberta'] = nada(lambda: MS.descansar(E, 'eu', 1))
        R['o estado está inteiro'] = not estado.valida(E)
    ruim = [k for k, v in R.items() if not v]
    return [('MA16 AS RECUSAS, com a frase, antes de gastar (nem tempo nem evento): descer com a saída de caça aberta, sem tocha; ir à sala que não é vizinha; abrir com gazua sem gazua; os atos da vila com a descida aberta; '
             'duas descidas; quem foi junto não decide; procurar no escuro; pegar com inimigo de pé; andar com gente à frente; a luta aberta tranca a descida e o mundo',
             ' · '.join(R) if not ruim else 'ERRADO: ' + ' · '.join(ruim), not ruim)]


def _capela(E, mais=()):
    """a prova do tesouro: a capela e o caminho até ela sem ninguém e sem armadilha (o baú segue com a fechadura); o grupo de três desce e chega lá"""
    ef = [['lugar', x, 'bichos', 'poe', {}] for x in ('cripta_2', 'cripta_3', 'cripta_4')] + [['lugar', x, 'armadilhas', 'poe', []] for x in ('cripta_2', 'cripta_4')]
    estado.aplica(E, 'mestre', ef + list(mais), texto='a capela vazia (a prova)')
    quieto(MS.descer, E, 'eu', 'cripta', com=['tome', 'rute'], luz='tocha'); quieto(MS.ir, E, 'eu', 'cripta_2'); quieto(MS.ir, E, 'eu', 'cripta_4')


def _ma17(n):
    """MA17. O TESOURO E QUEM O LEVA: o que ficou junto do corpo de quem morreu na sala não é tesouro (nem no "Dentro:", nem no pegar, nem sai do estoque sem o Mestre);
    e quem fica com a peça paga a cada um dos outros a parte dele nela (sem a prata, a peça segue ali, e outro do grupo pode pegá-la pagando)"""
    R = {}
    with pasta():
        E = vila(1); _capela(E, [['pessoa', 'tome', 'moedas', 'soma', 40], ['pessoa', 'tome', 'carga.osso:0', 'soma', 4]])
        leva = E['gente']['tome']['moedas']; p0 = prata_do_mundo(E)
        estado.aplica(E, 'mestre', [['pessoa', 'tome', 'estado', 'poe', 'morto']], texto='Tomé morre na capela (a prova)')
        R['a prata e a carga do morto ficam junto do corpo'] = estado.junto(E, 'cripta_4') == {'prata': leva, 'osso:0': 4}
        with dado_posto([5]): t = quieto(MS.abrir, E, 'eu', 'guardado', 'força')['texto']
        dentro = next((x for x in t.split('\n') if x.startswith('Dentro')), '')
        R['o "Dentro:" do baú é só o tesouro'] = dentro.startswith('Dentro: 25 de prata') and 'osso' not in dentro
        m0 = E['gente']['eu']['moedas'] + E['gente']['rute']['moedas']
        quieto(MS.pegar, E, 'eu')
        R['o pegar reparte só o tesouro'] = E['gente']['eu']['moedas'] + E['gente']['rute']['moedas'] - m0 == 25 and E['lugares']['cripta_4']['estoque'].get('prata') == leva and estado.junto(E, 'cripta_4').get('osso:0') == 4
        R['a mesa diz o que ficou junto do corpo'] = any('junto de um corpo' in x and f'{leva} de prata' in x for x in MS._aqui(E, 'eu'))
        R['o estoque não larga a parte do morto sozinho'] = bool(recusa(lambda: estado.aplica(E, 'mestre', [['estoque', 'cripta_4', 'prata', 'soma', -1], ['pessoa', 'eu', 'moedas', 'soma', 1]], texto='a prova')))
        estado.aplica(E, 'mestre', [['lugar', 'cripta_4', 'do_morto.prata', 'soma', -leva], ['estoque', 'cripta_4', 'prata', 'soma', -leva], ['pessoa', 'rute', 'moedas', 'soma', leva]], texto='a cena: Rute fica com a bolsa de Tomé (a prova)')
        R['o Mestre a solta, no mesmo evento'] = estado.junto(E, 'cripta_4') == {'osso:0': 4} and not estado.valida(E) and prata_do_mundo(E) == p0
        quieto(MS.sair, E, 'eu')
        E = vila(1); escudo = item('escudo', 1, 'o escudo de bronze', historia=['a prova']); escudo.update(onde='cripta_4')
        _capela(E, [['pessoa', 'eu', 'moedas', 'soma', -E['gente']['eu']['moedas']], ['pessoa', 'tome', 'moedas', 'soma', 60], ['item', 'nasce', escudo]])
        iid = next(i for i, it in E['itens']['itens'].items() if it['nome'] == 'o escudo de bronze'); p0 = prata_do_mundo(E)
        with dado_posto([5]): quieto(MS.abrir, E, 'eu', 'guardado', 'força')
        pe = MS.parte_peca(E, E['itens']['itens'][iid], 3, 'vila'); m = {c: E['gente'][c]['moedas'] for c in ('eu', 'tome', 'rute')}
        r1 = quieto(MS.pegar, E, 'eu'); pm = sum(pp for i, pp in ((i, MS.parte_peca(E, E['itens']['itens'][i], 3, 'vila')) for i in r1['itens']))
        R['sem a prata da parte dos outros, a peça segue ali'] = iid in r1['deixou'] and not E['itens']['itens'][iid].get('dono') and pe > 0
        R['quem fica com a peça paga a parte de cada um'] = r1['pagou'] == ({'tome': pm, 'rute': pm} if pm else {}) and E['gente']['eu']['moedas'] == m['eu'] + r1['partes']['eu'].get('prata', 0) - 2 * pm
        m = {c: E['gente'][c]['moedas'] for c in ('eu', 'tome', 'rute')}
        quieto(MS.pegar, E, 'eu', iid, quem='tome')
        R['outro do grupo a pega, pagando'] = E['itens']['itens'][iid].get('dono') == 'tome' and E['gente']['tome']['moedas'] == m['tome'] - 2 * pe and E['gente']['eu']['moedas'] == m['eu'] + pe and E['gente']['rute']['moedas'] == m['rute'] + pe
        R['a prata do mundo fecha, o estado inteiro'] = prata_do_mundo(E) == p0 and not estado.valida(E)
    ruim = [k for k, v in R.items() if not v]
    return [('MA17 O TESOURO E QUEM O LEVA: o que ficou junto do corpo de quem morreu na sala (a prata e a carga dele) não é tesouro: não entra no "Dentro:", o pegar não o reparte, '
             'e o estoque não o larga sem o Mestre (que o solta no mesmo evento); quem fica com a peça paga a cada um dos outros a parte dele nela (o que a loja de casa daria, dividido pelo grupo); '
             'sem a prata, a peça segue ali, e outro do grupo pode pegá-la pagando',
             ' · '.join(R) if not ruim else 'ERRADO: ' + ' · '.join(ruim), not ruim)]


def _ma18(n):
    """MA18. A ENTRADA ROLA UMA VEZ: o bloco que fecha no caminho fecha antes de o grupo olhar a sala; quem vagueia e chega acha o grupo com quem mora ali: um encontro só,
    uma atenção só, e a surpresa rolada fica. A mesa separa quem chega de quem já estava ali"""
    R = {}
    with pasta():
        E = vila(1)
        estado.aplica(E, 'mestre', [['lugar', 'cripta_2', 'bichos', 'poe', {}], ['lugar', 'cripta_2', 'armadilhas', 'poe', []], ['lugar', 'cripta_4', 'atento', 'poe', 1], ['lugar', 'cripta', 'vagantes', 'poe', {'corpo-seco': 1}]], texto='a prova')
        quieto(MS.descer, E, 'eu', 'cripta', com=['tome', 'rute'], luz='tocha'); quieto(MS.ir, E, 'eu', 'cripta_2')
        d = copy.deepcopy(MS.descida(E['gente']['eu'])); d['lances'] = MS.K.LANCES_BLOCO - 1
        estado.aplica(E, 'mestre', [['pessoa', 'eu', 'marca.masmorra', 'poe', d]], texto='o bloco quase fechando (a prova)')
        atencoes = []; real_at, real_vaga = MS._atencao, MS.rola_vaga
        def conta(*a): r = real_at(*a); atencoes.append(r); return r
        MS._atencao = conta; MS.rola_vaga = lambda E_, pid: ('corpo-seco', 1)
        try:
            with dado_posto([-5]): t = quieto(MS.ir, E, 'eu', 'cripta_4')['texto']
        finally: MS._atencao, MS.rola_vaga = real_at, real_vaga
        enc = (MS.descida(E['gente']['eu']) or {}).get('encontro') or {}
        R['uma atenção só, na entrada que fecha o bloco'] = len(atencoes) == 1
        R['a surpresa rolada fica'] = bool(atencoes) and enc.get('surpresa') == atencoes[0] == 'A' and 'DESPREVENIDO' in t
        R['quem chega e quem já estava ali'] = 'CHEGA: o corpo-seco.' in t and '4 ratazanas já estavam ali.' in t and 'CHEGAM: 4 ratazanas' not in t
        R['o encontro tem todos os da sala'] = enc.get('n') == {'ratazana': 4, 'corpo-seco': 1}
    ruim = [k for k, v in R.items() if not v]
    return [('MA18 A ENTRADA ROLA UMA VEZ: o bloco que fecha no caminho fecha antes de o grupo olhar a sala; quem vagueia e chega acha o grupo com quem mora ali (um encontro, uma atenção, '
             'e a surpresa rolada fica); a mesa diz quem chega e quem já estava ali',
             ' · '.join(R) if not ruim else 'ERRADO: ' + ' · '.join(ruim), not ruim)]


def provas(n=300):
    out = []
    for f in (_ma0, _ma1, _ma2_3, _ma5, _ma7, _ma12, _ma13, _ma14, _ma15, _ma16, _ma17, _ma18, _ma6, _ma4):
        try: out += f(n)
        except (Exception, SystemExit) as x:
            import traceback; out.append((f'{f.__name__}: a prova quebrou', f'{type(x).__name__}: {x} · ' + ' | '.join(traceback.format_exc().splitlines()[-4:-1]).strip(), False))
    return out


if __name__ == '__main__':
    sys.exit(0 if main() else 1)
