#!/usr/bin/env python3
"""provas_caca.py — MOTOR 10: O BANCO DE PROVAS DA CAÇA E DA COLETA (etapa 2: o ermo contado, o rastro, a ameaça lida antes, a luta do ato.py, o despojo, a virada).

As metas são as do contrato (projeto/ETAPA2.md, seção 7). As provas rodam em mundos de rascunho, cada um numa pasta temporária (MOTOR10_MUNDO); nunca num save.
O dado é o de verdade (teste.rola no rastro, na fuga e na coleta; o do luta.py na luta): por isso as medidas mudam um pouco de uma rodada para outra,
e as metas de frequência são medidas em muitas vidas.

O ROBÔ CAÇADOR vive de verdade: dorme na cama e paga, come e paga, vende o despojo na loja da vila (a 60% do preço do dia) e sai para o ermo quando o corpo deixa.
  O PRUDENTE (nível 10, gente gerada, de arco, espada de reserva, couro e capuz Comuns) procura corça, lê a ameaça e só ataca a presa de grau F com o terreno
    a favor: uma corça com o cerco, ou até duas com o alto e o cerco. O resto ele deixa; do bicho que o viu, ele foge (da presa que não investe, só sai de perto).
    Ferido, repousa enquanto tem prata; sem prata, sai por um bloco só.
  O AFOITO é o mesmo homem: procura o que aparecer, ataca tudo o que aparece (bando, grau maior, o que o viu primeiro), todo dia, ferido ou não.
A LUTA de todo robô é a do `ato.py luta` (ato.luta_nova e ato.luta_roda, com a ordem "atacar" a cada parada), em arquivo, como na mesa.

Uso: python3 provas_caca.py [N]      N = o tamanho das amostras (padrão 300): N ÷ 10 vidas de 30 dias de cada robô (no mínimo 20)
     (o `python3 provas_mundo.py` também roda este banco)
"""
import contextlib, copy, io, json, math, os, shutil, sys, tempfile
import tabelas as T
import tabelas_mundo as M
import tabelas_bichos as TB
import tabelas_caca as K
import tabelas_mercado as C
import estado, ato, corpo, teste, turno, bichos, caca, mercado, oficio
import provas_mundo as PM
from itens import item
from pessoas import padrao

# ---------- o contrato (as faixas não se mexem) ----------
DIARIA = M.SALARIO['diarista'] * 2      # a diária do diarista: dois blocos de trabalho
RENDE = (1.5, 4.0)          # o caçador tira por dia, ao preço de base, de 1,5 a 4 vezes a diária
FERE = (0.02, 0.12)         # e sai ferido ou morto em 2 a 12% das saídas
AFOITO = 0.70               # o afoito morre em 30 dias em 70% ou mais das sementes
DIAS = 30
CACADOS = 60                # caçar 60 de uma espécie...
VOLTA = (30, 120)           # ... e ela leva de 30 a 120 dias para voltar a...
NOVE = 0.9                  # ... nove décimos do teto
ROBO = dict(nivel=10, cat=0, kit='arco', alvo='corça', reserva=6, cansado=7, ordem='atacar agressiva', pv=0.8, repousa=True, cerco_um=False, conserta=4)       # o caçador de começo (cansado: com este cansaço ele não luta, e volta)
VETERANO = dict(nivel=60, cat=2, kit='espada', mao=4)                   # quem caça os 60 (de espada, malha e escudo Raros, Treinado em caça)


# ---------- montar um mundo de rascunho ----------
@contextlib.contextmanager
def rascunho():
    """uma pasta temporária como save (MOTOR10_MUNDO), desfeita no fim"""
    d = tempfile.mkdtemp(prefix='m10_caca_'); antes = os.environ.get('MOTOR10_MUNDO'); os.environ['MOTOR10_MUNDO'] = d
    try: yield d
    finally:
        if antes is None: os.environ.pop('MOTOR10_MUNDO', None)
        else: os.environ['MOTOR10_MUNDO'] = antes
        shutil.rmtree(d, ignore_errors=True)


def cacador(E, pid='eu', nivel=10, cat=0, kit='arco', mao=0, nome=None, atributos=None):
    """a mão do gerador (gente, atributo e maestria não têm verbo de nascer no gravador): faz da pessoa um caçador deste nível, gente gerada (arqueiro ou
    guerreiro), com o conjunto desta categoria: de arco, espada de reserva, couro e capuz; ou de espada, escudo, malha e elmo. As peças nascem por evento."""
    if pid not in E['gente']: E['gente'][pid] = dict(copy.deepcopy(E['gente']['eu']), jogador=False, nome=nome or pid, carga={}, marca={}, treino={}, moedas=0)
    p = E['gente'][pid]; g = padrao(p['nome'], nivel, molde='arqueiro' if kit == 'arco' else 'guerreiro', atributos=atributos); m = T.maestria_tipica(nivel)
    p.update(nivel=nivel, atributos=g['atributos'], maestria={'arco': m, 'espada': m, 'montante': m, 'caça': mao}, feridas=[], corpo=dict(fome=0, sono=0, cansaco=0)); p['pv'] = estado.pv_max(p)
    velhas = [['item', i, 'some'] for i, it in E['itens']['itens'].items() if it.get('dono') == pid]; s0 = E['itens']['seq']; n = p['nome']
    if kit == 'arco': pecas = [(item('arma', cat, f'Arco de {n}', familia='arco', dono=pid), 'arma'), (item('arma', cat, f'Espada de {n}', familia='espada', dono=pid), 'arma2'),
                               (item('armadura', cat, f'Gibão de {n}', material='couro', dono=pid), 'veste'), (item('armadura', cat, f'Capuz de {n}', material='couro', cobre=['cabeça'], dono=pid), 'veste')]
    elif kit == 'montante': pecas = [(item('arma', cat, f'Montante de {n}', familia='montante', dono=pid), 'arma'), (item('armadura', cat, f'Cota de {n}', material='malha', dono=pid), 'veste'),
                                     (item('armadura', cat, f'Elmo de {n}', material='malha', cobre=['cabeça'], dono=pid), 'veste')]
    else: pecas = [(item('arma', cat, f'Espada de {n}', familia='espada', dono=pid), 'arma'), (item('escudo', cat, f'Escudo de {n}', dono=pid), 'escudo'),
                   (item('armadura', cat, f'Cota de {n}', material='malha', dono=pid), 'veste'), (item('armadura', cat, f'Elmo de {n}', material='malha', cobre=['cabeça'], dono=pid), 'veste')]
    estado.aplica(E, 'gera', velhas + [['item', 'nasce', it] for it, _ in pecas], texto=f'o conjunto de {n}')
    estado.aplica(E, 'gera', [['item', f'i{s0 + k + 1:04d}', 'uso', 'poe', uso] for k, (_, uso) in enumerate(pecas)], texto=f'{n} se veste')
    return p


def mundo(semente=1, habitat='floresta', perigo=1, pop=400, prata=30, fauna=None, materia=None, **quem):
    """a vila de prova (com mercado, se pop), à meia-noite do Dia 1, um ermo vizinho povoado pela tabela (ou com a fauna e a matéria dadas), e o caçador"""
    E = PM.vila(semente, prata); E['relogio']['bloco'] = 0; E['turno']['aberto']['bloco'] = 0
    if pop: mercado.funda(E, 'vila', pop); estado.aplica(E, 'gera', [['lugar', 'vila', 'oficina', 'poe', 1]], onde='vila', texto='a forja da vila de prova')
    E['lugares']['mata'] = dict(nome='a Mata de Prova', em='na Mata de Prova', tipo='ermo', estoque={})         # a mão do gerador: lugar não tem verbo de nascer
    caca.povoa(E, 'mata', habitat, perigo, vizinho='vila')
    ef = ([['lugar', 'mata', 'teto', 'poe', dict(fauna)], ['lugar', 'mata', 'bichos', 'poe', dict(fauna)]] if fauna is not None else []) + \
         ([['lugar', 'mata', 'coleta_teto', 'poe', dict(materia)], ['lugar', 'mata', 'coleta', 'poe', dict(materia)]] if materia is not None else [])
    if ef: estado.aplica(E, 'gera', ef, onde='mata', texto='o ermo de prova')
    cacador(E, 'eu', **dict(dict(nivel=ROBO['nivel'], cat=ROBO['cat'], kit=ROBO['kit']), **quem))
    return E


def poe(E, **bichos_):
    """o gerador põe a contagem de uma espécie no ermo de prova (por evento)"""
    estado.aplica(E, 'gera', [['lugar', 'mata', f'bichos.{e}', 'poe', q] for e, q in bichos_.items()], onde='mata', texto='a contagem de prova')


def dias_sem_ninguem(E, n=1):
    """o mundo vira n dias sem ninguém em cena: o relógio anda um dia e cada módulo roda a sua virada (o mesmo caminho do ato.passa)"""
    for _ in range(n):
        estado.aplica(E, 'tempo', [['relogio', M.BLOCOS_DIA]], texto='um dia sem ninguém'); ato._mundo_vira(E); E['_novos'].clear()


def recusa(f):
    try:
        with contextlib.redirect_stdout(io.StringIO()): f()
    except SystemExit as e: return str(e) or 'recusado'
    return None


def retrato(E): return json.dumps({k: E[k] for k in estado.ARQS}, sort_keys=True, ensure_ascii=False)
def prata(E): return mercado.prata_do_mundo(E)
def quieto(f, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()): return f(*a, **k)
def base(bens): return sum(q * (C.base(b) or 0) for b, q in bens.items())       # o valor de um despojo ao preço de base do mercado
def pc(x, casas=0): return f'{100 * x:.{casas}f}%'.replace('.', ',')
def vz(x, casas=2): return f'{x:.{casas}f}'.replace('.', ',')
def eventos(d):
    arq = os.path.join(d, 'eventos.jsonl')
    return [json.loads(x) for x in open(arq, encoding='utf-8').read().splitlines()] if os.path.exists(arq) else []


# ---------- a conta (o razão): tudo o que saiu do ermo e tudo o que entrou na carga, lido do registro de eventos ----------
def razao(evs, ermo='mata'):
    """soma, do registro de eventos: o que nasceu e o que saiu de cada contagem, o que voltou e o que se tirou de cada matéria, o que entrou em cada carga
    (pelo despojo e pela coleta) e o que foi vendido. E confere evento por evento: no `despojo`, o que entra é o despojo das carcaças aproveitadas (dentro da
    tabela da espécie), e nada entra quando a casa não ficou com o campo; no `coletar`, o que sai do ermo é o que entra na carga."""
    Z = dict(nasce={}, sai={}, volta={}, tirado={}, despojo={}, coletado={}, vendido={}, comprado={}, abates=0, perdidas=0, nucleos=0, mal=[])
    def soma(d, k, v): d[k] = d.get(k, 0) + v
    for ev in evs:
        bi = {}; co = {}; carga = {}; abates = 0; nuc = 0
        for ef in ev['efeitos']:
            if ef[0] == 'lugar' and ef[1] == ermo and ef[3] == 'soma' and ef[2].startswith('bichos.'): soma(bi, ef[2][7:], ef[4])
            elif ef[0] == 'lugar' and ef[1] == ermo and ef[3] == 'soma' and ef[2].startswith('coleta.'): soma(co, ef[2][7:], ef[4])
            elif ef[0] == 'pessoa' and ef[2].startswith('carga.'): soma(carga, ef[2][6:], ef[4])
            elif ef[0] == 'pessoa' and ef[2] == 'marca.abates': abates += ef[4]
            elif ef[0] == 'item' and ef[1] == 'nasce' and ef[2].get('tipo') == 'nucleo': nuc += 1
        if ev['tipo'] == 'ninhada':
            for e, n in bi.items(): soma(Z['nasce'], e, n)
            for b, n in co.items(): soma(Z['volta'], b, n)
            if any(n < 0 for n in list(bi.values()) + list(co.values())) or carga: Z['mal'].append(f"#{ev['id']}: ninhada que tira")
        elif ev['tipo'] == 'despojo':
            if any(n > 0 for n in bi.values()) or len(bi) > 1: Z['mal'].append(f"#{ev['id']}: despojo que põe bicho")
            for e, n in bi.items():
                soma(Z['sai'], e, -n); d = TB.ESPECIES[e]['despojo']; Z['abates'] += abates; Z['perdidas'] += -n - abates
                lo = {b: max(1, math.ceil(q * TB.DESPOJO_MIN)) * abates for b, q in d.items()}; hi = {b: q * abates for b, q in d.items()}
                if abates not in (0, -n) or set(carga) - set(d) or any(not lo[b] <= carga.get(b, 0) <= hi[b] for b in d): Z['mal'].append(f"#{ev['id']}: o despojo não bate com a tabela ({-n} de {e}, {abates} aproveitada(s): {carga})")
                if nuc != (-n if TB.ESPECIES[e]['nucleo'] else 0): Z['mal'].append(f"#{ev['id']}: núcleo que não bate")
            for b, n in carga.items(): soma(Z['despojo'], b, n)
            Z['nucleos'] += nuc
        elif ev['tipo'] == 'coletar':
            for b, n in co.items(): soma(Z['tirado'], b, -n)
            for b, n in carga.items(): soma(Z['coletado'], b, n)
            if {b: -n for b, n in co.items()} != carga: Z['mal'].append(f"#{ev['id']}: a coleta não fecha ({co} do ermo, {carga} na carga)")
        elif ev['tipo'] == 'venda':
            for b, n in carga.items(): soma(Z['vendido'], b, -n)
        elif ev['tipo'] == 'compra':
            for b, n in carga.items(): soma(Z['comprado'], b, n)
        elif bi or co or (carga and ev['tipo'] != 'gera'): Z['mal'].append(f"#{ev['id']}: {ev['tipo']} mexe no ermo ou na carga")
    return Z


def fecha(Z, antes, depois):
    """a conta fecha? antes e depois: (a contagem, a matéria do ermo, a soma das cargas). Devolve a lista do que não fecha."""
    (b0, c0, g0), (b1, c1, g1) = antes, depois; P = list(Z['mal'])
    for e in set(b0) | set(b1) | set(Z['nasce']) | set(Z['sai']):
        if b0.get(e, 0) + Z['nasce'].get(e, 0) - Z['sai'].get(e, 0) != b1.get(e, 0): P.append(f"{e}: {b0.get(e, 0)} + {Z['nasce'].get(e, 0)} − {Z['sai'].get(e, 0)} ≠ {b1.get(e, 0)}")
    for b in set(c0) | set(c1) | set(Z['volta']) | set(Z['tirado']):
        if c0.get(b, 0) + Z['volta'].get(b, 0) - Z['tirado'].get(b, 0) != c1.get(b, 0): P.append(f"{b}: o ermo não fecha")
    if Z['tirado'] != Z['coletado']: P.append('o que se tirou do ermo não é o que entrou na carga')
    for b in set(g0) | set(g1) | set(Z['despojo']) | set(Z['coletado']) | set(Z['vendido']) | set(Z['comprado']):
        if g0.get(b, 0) + Z['despojo'].get(b, 0) + Z['coletado'].get(b, 0) + Z['comprado'].get(b, 0) - Z['vendido'].get(b, 0) != g1.get(b, 0): P.append(f"{b}: a carga não fecha")
    return P


def foto(E, ermo='mata'):
    """(a contagem, a matéria do ermo, a soma das cargas de toda a gente)"""
    g = {}
    for p in E['gente'].values():
        for b, q in p.get('carga', {}).items(): g[b] = g.get(b, 0) + q
    return dict(caca.bichos_de(E, ermo)), dict(caca.coleta_de(E, ermo)), g


# ---------- o robô caçador ----------
def _come(E, pid, V, ate=3):
    p = E['gente'][pid]
    while p['estado'] == 'vivo' and p['corpo']['fome'] >= ate and p['moedas'] >= M.REFEICAO_PRECO and E['lugares'][p['lugar']]['estoque'].get('comida', 0) > 0:
        ato.comer(E, pid); V['refeicoes'] += 1; p = E['gente'][pid]
    if p['corpo']['fome'] >= M.LIMIARES['fome'][0]: V['jejum'] += 1


def _dorme(E, pid, V, blocos):
    chao = E['gente'][pid]['moedas'] < M.CAMA_PRECO; V['chao' if chao else 'camas'] += 1; ato.dormir(E, pid, blocos, chao=chao, para=False)


def _vende(E, pid, V):
    p = E['gente'][pid]
    if not any(C.base(b) is not None and q >= 1 for b, q in p.get('carga', {}).items()): return
    try: V['prata_venda'] += quieto(mercado.vender_cesta, E, pid)['prata']
    except SystemExit: V['nao_vendeu'] += 1


def _conserta(E, pid, V):
    """o robô cuida do que veste: a peça que chega a poucos pontos de durabilidade vai à forja da vila (conserto pago: 2% do preço por ponto, e um bloco de espera).
    Devolve os blocos gastos."""
    p = E['gente'][pid]; n = 0
    for iid, it in list(E['itens']['itens'].items()):
        if it.get('dono') != pid or not it.get('uso') or it['dur'][0] > ROBO['conserta'] or oficio.oficina(E, p['lugar']) is None: continue
        if E['gente'][pid]['moedas'] < oficio.O.conserto_pago(it['cat'], it['dur'][1] - it['dur'][0]) + M.CAMA_PRECO + M.REFEICAO_PRECO: V['sem_conserto'] += 1; continue
        R = quieto(oficio.consertar, E, pid, iid, pago=True); V['consertos'] += 1; V['prata_conserto'] += R['custo']; n += R['feitos']
    return n


def _luta(E, pid, ordem='atacar'):
    """a luta do robô: a do ato.py luta, até o fim, com a mesma ordem a cada parada. Devolve as contas (caca.acerta)."""
    nome = E['gente'][pid]['nome']
    for _ in range(300):
        try: R = quieto(caca.luta_roda, E, pid, [f'{nome}: {ordem}'])
        except SystemExit: R = quieto(caca.luta_roda, E, pid, [])        # o caçador não está de pé: a luta segue sem ordem dele
        if R['fase'] != 'luta': return R
    raise RuntimeError('a luta não acaba')


def prudente(E, pid, R, estrito=False):
    """o que o robô prudente faz diante do bicho: lê a ameaça (o grau e quantos são), a posição (o que o rastro deu) e o próprio corpo.
    Só ataca a presa de grau F, de longe, e só a encurrala quando é uma só e ele está no alto."""
    enc = R['encontro']; e = TB.ESPECIES[enc['especie']]; _, nv, _ = caca.posicao(enc); ferida = bool(enc.get('feridos')); p = E['gente'][pid]
    if enc['viu'] != 'caçador': return ('deixar',) if e['grau'] == 'F' else ('fugir',)       # a presa que o viu não investe: ele só sai de perto; do resto, corre
    if p['corpo']['cansaco'] >= ROBO['cansado'] or p['pv'] < ROBO['pv'] * estado.pv_max(p): return ('fugir',)      # cansado ou machucado, não luta: recua sem ser visto e volta
    if e['grau'] != 'F' or (estrito and nv < 2): return ('deixar',)
    if nv >= 2: return ('atacar', 'longe', ['alto', 'cerco'] if enc['n'] == 1 else ['alto', 'estreito'])
    if nv == 1: return ('atacar', 'longe', ['cerco'] if enc['n'] == 1 and ROBO['cerco_um'] else ['alto'])
    return ('atacar', 'longe', []) if enc['n'] == 1 or ferida else ('deixar',)               # sem o terreno: só uma corça sozinha, ou a presa já ferida


def afoito(E, pid, R, estrito=False): return ('atacar', None, [])


def veterano(E, pid, R, estrito=False):
    """quem caça os 60: ataca toda corça que vê, de perto, com o cerco quando o rastro o dá; do resto, desvia"""
    enc = R['encontro']; inis, nv, _ = caca.posicao(enc)
    if enc['especie'] != 'corça': return ('deixar',) if enc['viu'] == 'caçador' else ('fugir',)
    return ('atacar', 'colado' if 'colado' in inis else inis[-1], ['cerco'] if nv else [])


def uma_saida(E, pid, V, escolhe, alvo=None, blocos=2, estrito=False, ermo='mata'):
    """uma saída inteira do robô, da ida à volta. Conta em V o que houve. Devolve True se ele saiu ferido (ferida nova, deixado por morto) ou morto."""
    p = E['gente'][pid]; f0 = len(p['feridas']); caiu = False; V['saidas'] += 1
    R = quieto(caca.sair, E, pid, ermo, alvo=alvo, blocos=blocos)
    for _ in range(200):
        if R['fase'] in ('fim', 'morto'): break
        if R['fase'] == 'encontro':
            enc = R['encontro']; V['encontros'] += 1; V['viu_bicho'] += enc['viu'] != 'caçador'; q = escolhe(E, pid, R, estrito)
            if enc['n'] > caca.bichos_de(E, ermo).get(enc['especie'], 0): V['mal'].append(f"apareceram {enc['n']} de {enc['especie']} e só havia {caca.bichos_de(E, ermo).get(enc['especie'], 0)}")
            if q[0] == 'atacar': R = quieto(caca.atacar, E, pid, inicio=q[1], vantagens=q[2])
            else: V['deixou' if q[0] == 'deixar' else 'fugiu'] += 1; R = quieto(getattr(caca, q[0]), E, pid)
        elif R['fase'] == 'luta':
            esp = R['encontro']['especie']; V['lutas'] += 1; V['forcadas'] += R['encontro'].get('surpresa') != 'B' and escolhe is not afoito
            R = _luta(E, pid, ROBO['ordem'] if escolhe is prudente else 'atacar'); V['valor'] += base(R['bens']); V['carcacas'] += R['mortos'] if R['leva'] else 0; V['mortos_b'][esp] = V['mortos_b'].get(esp, 0) + R['mortos']
            V['fugiram_b'] += R['fugiram']; V['por_especie'][esp] = V['por_especie'].get(esp, 0) + 1; caiu = caiu or R['meu'] in ('caido', 'morto')
            for b, n in R['bens'].items(): V['bens'][b] = V['bens'].get(b, 0) + n
        elif escolhe is prudente and (E['gente'][pid]['corpo']['cansaco'] >= ROBO['cansado'] or E['gente'][pid]['pv'] < ROBO['pv'] * estado.pv_max(E['gente'][pid])): R = quieto(caca.volta, E, pid)       # cansado ou machucado, volta
        elif R.get('sangue') and escolhe is not veterano: V['sangue'] += 1; R = quieto(caca.sangue, E, pid); V['sangue_achou'] += R['fase'] == 'encontro'
        else: R = quieto(caca.volta if R.get('parou') and escolhe is not afoito else caca.segue, E, pid)
    else: raise RuntimeError('a saída não acaba')
    p = E['gente'][pid]; mal = p['estado'] != 'vivo' or len(p['feridas']) > f0 or caiu; V['feridas'] += mal
    if any(q < 0 for q in list(E['lugares'][ermo].get('bichos', {}).values()) + list(E['lugares'][ermo].get('coleta', {}).values())): V['mal'].append('contagem negativa')
    return mal


def vida(semente, modo='prudente', dias=DIAS, **quem):
    """uma vida do robô caçador, do Dia 1 até `dias` (ou até morrer), num mundo de rascunho próprio. Devolve o que houve e as contas."""
    escolhe = prudente if modo == 'prudente' else afoito
    V = dict(modo=modo, saidas=0, feridas=0, lutas=0, forcadas=0, encontros=0, viu_bicho=0, deixou=0, fugiu=0, sangue=0, sangue_achou=0, valor=0, carcacas=0, fugiram_b=0, mortos_b={}, por_especie={}, bens={}, mal=[],
             refeicoes=0, jejum=0, camas=0, chao=0, prata_venda=0, nao_vendeu=0, consertos=0, prata_conserto=0, sem_conserto=0, folgas=0, repousos=0, morreu=None)
    with rascunho() as d:
        E = mundo(semente, **quem); pid = 'eu'; estado.grava(E); p0 = prata(E); f0 = foto(E); bolso0 = E['gente'][pid]['moedas']; saiu = 0
        while E['relogio']['dia'] <= dias and E['gente'][pid]['estado'] == 'vivo':
            b = E['relogio']['bloco']; p = E['gente'][pid]; c = p['corpo']; _vende(E, pid, V); _come(E, pid, V)
            if b < 2: _dorme(E, pid, V, 2 - b)
            elif b == 5: _dorme(E, pid, V, 3)
            elif b in (2, 3) and saiu != E['relogio']['dia']:
                ferido = bool(p['feridas']); _come(E, pid, V, ate=2)
                if _conserta(E, pid, V): continue                # a manhã foi na forja: sai mais tarde, por menos blocos
                p = E['gente'][pid]; c = p['corpo']; saiu = E['relogio']['dia']; cabem = M.BLOCOS_DIA - E['relogio']['bloco'] - 2 * caca.longe(E, 'mata')
                if modo == 'afoito': n = min(2, cabem)
                elif p['pv'] < ROBO['pv'] * estado.pv_max(p) and p['moedas'] >= ROBO['reserva']: n = 0
                elif ferido and (ROBO['repousa'] or any(f['grave'] for f in p['feridas'])): n = 0 if p['moedas'] >= ROBO['reserva'] else 1
                else: n = next((k for k in (2, 1) if k <= cabem and c['cansaco'] + K.IDA * M.ESFORCO[K.ESFORCO['ida']] + k * M.ESFORCO[K.ESFORCO['procura']] + M.LUTA_CANSA * (k - 1) <= ROBO['cansado']), 0)
                if n: uma_saida(E, pid, V, escolhe, alvo=ROBO['alvo'] if modo == 'prudente' else None, blocos=n, estrito=ferido)
                else: V['folgas'] += 1; V['repousos'] += ferido; ato.descansar(E, pid, M.BLOCOS_DIA - 1 - E['relogio']['bloco'])
            else: ato.descansar(E, pid, 1)
            E['turno']['dados'] = []; E['turno']['lutas'] = [l for l in E['turno']['lutas'] if not l['fim']]       # o caderno do turno de rascunho não cresce
        estado.grava(E); p = E['gente'][pid]; V['dia'] = min(E['relogio']['dia'], dias + 1); V['vivo'] = p['estado'] == 'vivo'; V['morreu'] = None if V['vivo'] else E['relogio']['dia']
        V['dias'] = dias if V['vivo'] else min(dias, E['relogio']['dia']); V['prata'] = prata(E) == p0; V['bolso'] = (bolso0, p['moedas']); V['quebrado'] = estado.valida(E)
        Z = razao(eventos(d)); V['conta'] = fecha(Z, f0, foto(E)); V['Z'] = Z; V['caca_fim'] = caca.bichos_de(E, 'mata'); V['mao'] = caca.mao(p); V['aberta'] = bool(caca.saida(p))
        if Z['despojo'] != V['bens'] or Z['sai'] != {e: n for e, n in V['mortos_b'].items() if n}: V['conta'].append('o registro de eventos não bate com o que o robô viu nas lutas')
    return V


# ---------- as provas do contrato ----------
def _o_prudente(P):
    """1. o caçador de nível 10 com peças Comuns tira por dia de 1,5 a 4 vezes a diária, e sai ferido ou morto em 2 a 12% das saídas"""
    n = len(P); dias = sum(V['dias'] for V in P); valor = sum(V['valor'] for V in P); saidas = sum(V['saidas'] for V in P); fer = sum(V['feridas'] for V in P); mortos = sum(not V['vivo'] for V in P)
    lutas = sum(V['lutas'] for V in P); carc = sum(V['carcacas'] for V in P); vezes = valor / dias / DIARIA; taxa = fer / max(1, saidas); venda = sum(V['prata_venda'] for V in P)
    por = sorted(V['valor'] / V['dias'] / DIARIA for V in P)
    a = (f"O CAÇADOR RENDE: nível 10, peças Comuns, no ermo de começo (a borda da floresta), tira por dia de {vz(RENDE[0], 1)} a {vz(RENDE[1], 1)} vezes a diária do diarista ({DIARIA} de prata), com o despojo ao preço de base",
         f"{n} vidas de até {DIAS} dias ({dias} dias vividos): {vz(valor / dias)} de prata por dia ao preço de base = {vz(vezes)} diárias (a vida do meio: {vz(por[len(por) // 2])}; a pior {vz(por[0])}, a melhor {vz(por[-1])}); "
         f"{vz(saidas / dias)} saída por dia, {vz(lutas / max(1, saidas))} luta por saída, {vz(carc / max(1, lutas))} carcaça por luta; na loja (60% do preço do dia) isso deu {vz(venda / dias)} de prata por dia", RENDE[0] <= vezes <= RENDE[1])
    b = (f"O CAÇADOR SE FERE: o mesmo robô sai ferido (ferida nova, ou deixado por morto) ou morto em {pc(FERE[0])} a {pc(FERE[1])} das saídas",
         f"{fer} de {saidas} saídas = {pc(taxa, 1)}; morreram {mortos} de {n} em {DIAS} dias ({pc(mortos / n)}); de {sum(V['encontros'] for V in P)} encontros, deixou {sum(V['deixou'] for V in P)} e fugiu de {sum(V['fugiu'] for V in P)}; "
         f"{sum(V['viu_bicho'] for V in P)} vezes o bicho o viu primeiro, e {sum(V['forcadas'] for V in P)} lutas ele não escolheu (o bicho investiu ou o alcançou)", FERE[0] <= taxa <= FERE[1])
    return [a, b]


def _o_afoito(A):
    """2. o mesmo robô, afoito, morre em 30 dias em 70% ou mais das sementes"""
    n = len(A); mortos = [V['morreu'] for V in A if not V['vivo']]; esp = {}
    for V in A:
        for e, k in V['por_especie'].items(): esp[e] = esp.get(e, 0) + k
    meio = sorted(mortos)[len(mortos) // 2] if mortos else None
    return (f"O AFOITO: o mesmo robô, atacando tudo o que aparece (bando, grau maior, o que o viu primeiro), morre em {DIAS} dias em {pc(AFOITO)} ou mais das sementes",
            f"morreram {len(mortos)} de {n} ({pc(len(mortos) / n)})" + (f"; o dia da morte do meio: {meio}" if mortos else '') + f"; {sum(V['lutas'] for V in A)} lutas em {sum(V['saidas'] for V in A)} saídas, contra: "
            + ', '.join(f"{TB.ESPECIES[e]['nome']} {k}" for e, k in sorted(esp.items(), key=lambda x: -x[1])) + f"; enquanto viveu, tirou {vz(sum(V['valor'] for V in A) / max(1, sum(V['dias'] for V in A)) / DIARIA)} diárias por dia", len(mortos) / n >= AFOITO)


def _sessenta(sementes):
    """3. caçar 60 bichos de uma espécie derruba a contagem, o rastro fica mais difícil, e ela leva de 30 a 120 dias para voltar a nove décimos do teto"""
    res = []
    for sem in sementes:
        with rascunho():
            E = mundo(sem, prata=100, **VETERANO); pid = 'eu'; estado.grava(E); teto = caca.teto_de(E, 'mata')['corça']; r0 = caca.rastro_contra(E, 'mata', 'corça')
            V = dict(saidas=0, feridas=0, lutas=0, forcadas=0, encontros=0, viu_bicho=0, deixou=0, fugiu=0, sangue=0, sangue_achou=0, valor=0, carcacas=0, fugiram_b=0, mortos_b={}, por_especie={}, bens={}, mal=[],
                     refeicoes=0, jejum=0, camas=0, chao=0, prata_venda=0, nao_vendeu=0, consertos=0, prata_conserto=0, sem_conserto=0)
            while V['mortos_b'].get('corça', 0) < CACADOS and E['gente'][pid]['estado'] == 'vivo' and E['relogio']['dia'] < 200:
                b = E['relogio']['bloco']; _vende(E, pid, V); _come(E, pid, V)
                if b < 2: _dorme(E, pid, V, 2 - b)
                elif b == 5: _dorme(E, pid, V, 3)
                elif b == 2 and E['gente'][pid]['corpo']['cansaco'] <= 3: _come(E, pid, V, ate=2); uma_saida(E, pid, V, veterano, alvo='corça', blocos=2)
                else: ato.descansar(E, pid, 1)
                E['turno']['dados'] = []; E['turno']['lutas'] = [l for l in E['turno']['lutas'] if not l['fim']]; E['_novos'].clear()
            d_caca = E['relogio']['dia']; fundo = caca.bichos_de(E, 'mata').get('corça', 0); r1 = caca.rastro_contra(E, 'mata', 'corça'); diz = K.fartura_diz(fundo, teto); dias = 0
            while caca.bichos_de(E, 'mata').get('corça', 0) < NOVE * teto and dias < 400: dias_sem_ninguem(E); dias += 1
            res.append(dict(mortos=V['mortos_b'].get('corça', 0), d_caca=d_caca, fundo=fundo, teto=teto, r0=r0, r1=r1, diz=diz, dias=dias, vivo=E['gente'][pid]['estado'] == 'vivo', mal=V['mal'], inteiro=not estado.valida(E)))
    certo = all(r['mortos'] >= CACADOS and r['fundo'] < r['teto'] * 0.75 and r['r1'] > r['r0'] and VOLTA[0] <= r['dias'] <= VOLTA[1] and not r['mal'] and r['inteiro'] for r in res)
    return (f"CAÇADA DEMAIS: caçar {CACADOS} bichos de uma espécie derruba a contagem, o rastro fica mais difícil, e ela leva de {VOLTA[0]} a {VOLTA[1]} dias para voltar a nove décimos do teto",
            f"{len(res)} mundos, um veterano (nível {VETERANO['nivel']}, conjunto Raro) caçando corça dois blocos por dia: " + ' · '.join(
                f"{r['mortos']} mortas em {r['d_caca'] - 1} dias, a contagem cai de {r['teto']} para {r['fundo']} (\"{r['diz']}\"), o rastro vai de {r['r0']} para {r['r1']}, e ela volta a {math.ceil(NOVE * r['teto'])} em {r['dias']} dias sem caça" for r in res), certo)


def _nunca_negativa(vidas):
    """4a. nenhuma contagem fica negativa (nas vidas dos robôs, e no ermo que se esvazia de verdade)"""
    with rascunho():
        E = mundo(3, fauna={'corça': 3}, prata=200, **VETERANO); pid = 'eu'; estado.grava(E); mal = []; blocos = 0; apos = 0; vistos = []
        V = dict(saidas=0, feridas=0, lutas=0, forcadas=0, encontros=0, viu_bicho=0, deixou=0, fugiu=0, sangue=0, sangue_achou=0, valor=0, carcacas=0, fugiram_b=0, mortos_b={}, por_especie={}, bens={}, mal=mal, refeicoes=0, jejum=0, camas=0, chao=0, prata_venda=0, nao_vendeu=0, consertos=0, prata_conserto=0, sem_conserto=0)
        def sai(n=2):
            nonlocal blocos, apos
            antes = caca.bichos_de(E, 'mata').get('corça', 0); enc0 = V['encontros']; _come(E, pid, V, ate=2); uma_saida(E, pid, V, veterano, alvo='corça', blocos=n); blocos += n
            if antes == 0: apos += V['encontros'] - enc0
            _dorme(E, pid, V, 3); _come(E, pid, V); E['turno']['dados'] = []; vistos.append(caca.bichos_de(E, 'mata').get('corça', 0))
        while caca.bichos_de(E, 'mata').get('corça', 0) > 0 and blocos < 200: sai()
        vazio_em = blocos
        for _ in range(8): poe(E, corça=0); sai()                    # o ermo vazio (o gerador segura a contagem em zero, contra o casal que vem de fora): ninguém aparece
        rec = recusa(lambda: estado.aplica(E, 'mestre', [['lugar', 'mata', 'bichos.corça', 'soma', -1]])); inteiro = not estado.valida(E)
        poe(E, corça=1); um = []
        for _ in range(12):                                         # com UMA corça no ermo, nunca aparecem duas
            R = quieto(caca.sair, E, pid, 'mata', alvo='corça', blocos=1)
            if R['fase'] == 'encontro': um.append(R['encontro']['n']); quieto(caca.fugir, E, pid)
            _dorme(E, pid, V, 3); _come(E, pid, V); E['turno']['dados'] = []
    neg = sum(bool(V['mal']) for V in vidas)
    return ('NENHUMA CONTAGEM NEGATIVA: o que aparece sai da contagem real (um bicho, um bando, ou nada), nunca mais do que há; no ermo vazio não aparece ninguém, e o gravador recusa tirar o que não existe',
            f"nas {len(vidas)} vidas dos robôs: {neg} com contagem negativa ou bando maior que a contagem; um ermo de 3 corças caçado até o fim em {vazio_em} blocos de procura (a contagem depois de cada saída: {', '.join(map(str, vistos[:6]))}...): "
            f"morreram {V['mortos_b'].get('corça', 0)}; depois de vazio, {apos} encontros em 16 blocos; tirar mais uma por evento: {'recusado' if rec else 'ACEITO'}; com uma corça só, apareceu {len(um)} vezes, sempre {'sozinha' if set(um) <= {1} else 'EM BANDO: ' + str(um)}; estado {'inteiro' if inteiro else 'QUEBRADO'}",
            neg == 0 and not mal and V['mortos_b'].get('corça', 0) == 3 and apos == 0 and rec and inteiro and um and set(um) == {1})


def _o_nucleo():
    """4b. o núcleo de chefe entra no Livro de Itens com `de` e `onde`"""
    tent = 0; R = None; ok = True; txt = []
    for sem in range(1, 13):
        tent += 1
        with rascunho() as d:
            E = mundo(sem, habitat='serra', perigo=3, fauna={'serpe': 1}, prata=100, nivel=100, cat=5, kit='espada', mao=6, atributos={'Vontade': 100, 'Percepção': 90}); pid = 'eu'
            cacador(E, 'bera', nivel=100, cat=5, kit='espada', nome='Bera', atributos={'Vontade': 100}); estado.grava(E); livro0 = len(E['itens']['itens']); ameaca = None
            for _ in range(40):
                R = quieto(caca.sair, E, pid, 'mata', alvo='serpe', blocos=2, com=['bera'])
                if R['fase'] == 'encontro':
                    ameaca = 'É chefe' in R['texto'] and 'núcleo' in R['texto']; inis, nv, _ = caca.posicao(R['encontro']); R = quieto(caca.atacar, E, pid, inicio=inis[-1], vantagens=['cobertura'][:nv])
                    cen = json.load(open(R['luta'].replace('_luta.json', '_cenario.json'), encoding='utf-8')); junto = [x.get('id') for x in cen['A']] == ['eu', 'bera']; R = _luta(E, pid); break
                quieto(ato.dormir, E, pid, 3, para=False)
                while E['gente'][pid]['corpo']['fome'] >= 2: quieto(ato.comer, E, pid)
                E['turno']['dados'] = []
            if R.get('fim') != 'A': txt.append(f"semente {sem}: a casa não ficou com o campo ({R.get('fim')})"); continue
            estado.grava(E); E = estado.carrega(); nuc = [it for it in E['itens']['itens'].values() if it['tipo'] == 'nucleo']; evs = [e for e in eventos(d) if e['tipo'] == 'despojo']
            it = nuc[0] if nuc else {}; leva = R['leva']; p = E['gente'][pid]
            ok = (len(nuc) == 1 and it.get('de') == 'serpe' and it.get('cat') == TB.ESPECIES['serpe']['cat'] and 'onde' in it and (it.get('dono') == leva) and it.get('onde') is None and len(it.get('historia', [])) == 1
                  and 'Mata de Prova' in it['historia'][0] and caca.bichos_de(E, 'mata').get('serpe', 0) == 0 and len(evs) == 1 and any(ef[:2] == ['item', 'nasce'] for ef in evs[0]['efeitos']) and not estado.valida(E)
                  and len(E['itens']['itens']) == livro0 + 1 and p.get('marca', {}).get('feito_caça') == 3 and ameaca and junto and R['ids_nucleos'] == [it.get('id')])
            # a outra ponta: a carcaça que ninguém ficou para abrir (as contas, com o desfecho da luta POSTO À MÃO no arquivo: o chefe morto, a casa sem o campo)
            poe(E, serpe=1); cacador(E, 'eu', nivel=100, cat=5, kit='espada', mao=6, atributos={'Vontade': 100, 'Percepção': 90}); chao = None
            for _ in range(40):
                R2 = quieto(caca.sair, E, pid, 'mata', alvo='serpe', blocos=2)
                if R2['fase'] == 'encontro':
                    R2 = quieto(caca.atacar, E, pid); S = json.load(open(R2['luta'], encoding='utf-8'))
                    for f in S['L']: f['estado'] = 'morto' if f['lado'] == 'B' else 'saiu'
                    S['fim'] = 'B'; S['posto_a_mao'] = True; json.dump(S, open(R2['luta'], 'w', encoding='utf-8'), ensure_ascii=False); A2 = quieto(caca.acerta, E, pid)
                    n2 = [x for x in E['itens']['itens'].values() if x['tipo'] == 'nucleo' and x.get('onde') == 'mata']
                    chao = len(n2) == 1 and n2[0]['dono'] is None and n2[0]['de'] == 'serpe' and A2['leva'] is None and not A2['bens'] and A2['mortos'] == 1 and caca.bichos_de(E, 'mata').get('serpe', 0) == 0 and not estado.valida(E)
                    break
                quieto(ato.dormir, E, pid, 3, para=False)
                while E['gente'][pid]['corpo']['fome'] >= 2: quieto(ato.comer, E, pid)
            achou = None
            for _ in range(40):                                     # e quem volta lá e passa num rastro acha o núcleo no chão
                if chao is None: break
                quieto(ato.dormir, E, pid, 3, para=False)
                while E['gente'][pid]['corpo']['fome'] >= 2: quieto(ato.comer, E, pid)
                Rv = quieto(caca.sair, E, pid, 'mata', alvo='serpe', blocos=2); n2 = [x for x in E['itens']['itens'].values() if x['tipo'] == 'nucleo' and x['de'] == 'serpe' and x.get('dono') == pid]
                if len(n2) == 2: achou = all(x.get('onde') is None for x in n2) and 'ACHADO' in Rv['texto'] and Rv['fase'] == 'fim' and not estado.valida(E); break
            txt.append(f"semente {sem}: o Aldric e a Bera (nível 100, aço Lendário) matam a serpe em {R['rodadas']} rodadas; o núcleo ({T.CATS[it.get('cat', 0)]}) entra no Livro por um evento `despojo`: de = {it.get('de')}, dono = {it.get('dono')}, onde = {it.get('onde')}, "
                       f"história: \"{(it.get('historia') or ['?'])[0]}\"; a serpe sai da contagem (0 de 1); a ameaça lida antes avisava do chefe: {'sim' if ameaca else 'NÃO'}; a Bera entrou na luta: {'sim' if junto else 'NÃO'}. "
                       f"A outra ponta (o desfecho posto à mão: o chefe morto e a casa sem o campo): o núcleo fica no ermo, sem dono, com onde = mata: {'sim' if chao else 'NÃO'}; quem volta e passa num rastro o acha: {'sim' if achou else 'NÃO'}")
            ok = ok and bool(chao) and bool(achou); break
    return ('O NÚCLEO DO CHEFE entra no Livro de Itens com `de` (a espécie) e `onde`: com dono, na mão de quem ficou com o campo; ou no ermo, se ninguém ficou para abrir a carcaça',
            ' · '.join(txt) + f" ({tent} tentativa(s))", ok and R is not None and R.get('fim') == 'A')


def _a_conta(P, A):
    """5. o que sai do ermo é igual ao que entra na carga (a conta fecha)"""
    todas = P + A; mal = [x for V in todas for x in V['conta']]; Z = [V['Z'] for V in todas]
    sai = sum(sum(z['sai'].values()) for z in Z); nasce = sum(sum(z['nasce'].values()) for z in Z); ab = sum(z['abates'] for z in Z); per = sum(z['perdidas'] for z in Z)
    desp = {}; vend = {}
    for z in Z:
        for b, n in z['despojo'].items(): desp[b] = desp.get(b, 0) + n
        for b, n in z['vendido'].items(): vend[b] = vend.get(b, 0) + n
    return ('A CONTA FECHA: em cada vida, a contagem do começo, mais o que nasceu, menos o que morreu, é a contagem do fim; todo bicho que sai da contagem sai num evento `despojo`; o que entra na carga é o despojo das carcaças '
            'aproveitadas (dentro da tabela da espécie), e é igual ao que o robô viu nas lutas; a carcaça de quem perdeu o campo não entra em carga nenhuma; e a carga do fim é a do começo, mais o despojo, menos o vendido',
            f"{len(todas)} vidas: {sai} bichos saíram da contagem ({ab} carcaças aproveitadas, {per} deixadas no mato) e {nasce} nasceram; entrou na carga: {caca._lista(desp)}; foi vendido: {caca._lista(vend)}; "
            f"vidas em que a conta não fecha: {sum(bool(V['conta']) for V in todas)}" + (f" ({mal[0]})" if mal else ''), not mal and sai == ab + per and sai > 0)


# ---------- as provas dos pontos de atenção ----------
def _a_ameaca_antes(n):
    """o caçador lê a ameaça ANTES, e pode deixar ou fugir: nada de luta até ele escolher"""
    with rascunho() as d:
        E = mundo(5, prata=200, mao=4, atributos={'Percepção': 90}); pid = 'eu'; estado.grava(E); certo = True; vistos = 0; deixou = fugiu = 0; c0 = caca.bichos_de(E, 'mata'); sobrevive = False; volta_rec = None
        for k in range(30):
            if deixou and fugiu: break
            R = quieto(caca.sair, E, pid, 'mata', alvo='corça', blocos=1)
            if R['fase'] == 'encontro' and R['encontro']['viu'] == 'caçador':
                enc = R['encontro']; vistos += 1; arma, armadura = caca._veste(E, pid); p = E['gente'][pid]; s = caca.saida(p)
                certo = certo and bichos.ameaca(enc['especie'], n=enc['n'], arma=arma, armadura=armadura) in R['texto'] and 'VOCÊ VIU PRIMEIRO' in R['texto'] and 'ESCOLHA' in R['texto'] and s['fase'] == 'encontro' and not E['turno']['lutas']
                estado.grava(E); E = estado.carrega(); sobrevive = caca.saida(E['gente'][pid]) == s                     # a saída aberta sobrevive a fechar e abrir o estado
                volta_rec = recusa(lambda: caca.volta(E, pid))
                if not deixou: R = quieto(caca.deixar, E, pid); deixou += 1; certo = certo and R['fase'] == 'fim' and caca.bichos_de(E, 'mata') == c0
                else: R = quieto(caca.fugir, E, pid); fugiu += 1; certo = certo and R['fase'] == 'fim' and caca.bichos_de(E, 'mata') == c0 and 'recua sem ser visto' in R['texto']
            elif R['fase'] == 'encontro': quieto(caca.fugir, E, pid)
            if E['gente'][pid]['estado'] != 'vivo': break
            R = caca.saida(E['gente'][pid])
            if R: break
            quieto(ato.dormir, E, pid, 3, para=False)
            while E['gente'][pid]['corpo']['fome'] >= 2: quieto(ato.comer, E, pid)
        estado.grava(E); lutas = [e for e in eventos(d) if e['tipo'] == 'luta']; limpo = not lutas and not E['turno']['lutas'] and not caca.saida(E['gente'][pid]) and E['gente'][pid]['pv'] == estado.pv_max(E['gente'][pid])
    return ('A AMEAÇA É LIDA ANTES: quando o bicho aparece a saída PARA; o caçador lê a frase do bichos.ameaca (com a conta do que ele veste) e o que a posição dá, e escolhe. Deixar e fugir do bicho que não o viu não custam nada',
            f"{vistos} encontros de quem viu primeiro: a frase da ameaça estava inteira no que ele leu, e não havia luta aberta: {'sim' if certo else 'NÃO'}; a saída aberta sobrevive a fechar e abrir o estado: {'sim' if sobrevive else 'NÃO'}; "
            f"voltar com o bicho à frente: {'recusado (é atacar, deixar ou fugir)' if volta_rec else 'ACEITO'}; deixou {deixou} e fugiu de {fugiu}: nenhuma luta, nenhum evento de luta, a contagem igual, o PV inteiro: {'sim' if limpo else 'NÃO'}",
            certo and vistos >= 2 and deixou and fugiu and sobrevive and volta_rec and limpo)


def _o_que_viu(n):
    """o bicho que viu o caçador: investe em quem o deixa, vem atrás de quem corre, e quem é alcançado luta colado e surpreendido"""
    k = max(30, n // 6); T_ = dict(deixar=dict(n=0, luta=0, certo=0), fugir=dict(n=0, luta=0, certo=0, teste=0, passou=0)); inv = K.indole('lobo'); mal = []
    for i in range(2 * k):
        o_que = 'deixar' if i % 2 == 0 else 'fugir'
        with rascunho():
            E = mundo(100 + i, fauna={'lobo': 400}, prata=50, atributos={'Percepção': 1}); pid = 'eu'; estado.grava(E); R = None
            for _ in range(12):
                R = quieto(caca.sair, E, pid, 'mata', alvo='corça', blocos=6)
                if R['fase'] == 'encontro': break
                quieto(ato.dormir, E, pid, 3, para=False)
            if R['fase'] != 'encontro' or R['encontro']['viu'] != 'bicho': mal.append(f'{i}: não houve acaso'); continue
            lido = 'APARECE, E VIU VOCÊ' in R['texto'] and bichos.ameaca('lobo', n=R['encontro']['n'], arma=0, armadura=0) in R['texto']; nd = len(E['turno']['dados'])
            R = quieto(getattr(caca, o_que), E, pid); t = T_[o_que]; t['n'] += 1; rol = E['turno']['dados'][nd:]
            if R['fase'] == 'luta':
                cen = json.load(open(R['luta'].replace('_luta.json', '_cenario.json'), encoding='utf-8')); t['luta'] += 1
                quer = (K.INICIO_ACASO, None) if o_que == 'deixar' else (K.INICIO_ALCANCADO, 'A')
                t['certo'] += lido and (cen['inicio'], cen['surpresa']) == quer and not cen['lugar'] and len(cen['B']) == R['encontro']['n'] and len(E['turno']['lutas']) == 1 and (o_que == 'deixar' or (len(rol) == 1 and not rol[0]['passou']))
            else: t['certo'] += lido and R['fase'] in ('fim', 'encontro', 'procura') and not E['turno']['lutas'] and (o_que == 'deixar' or not rol or rol[0]['passou'])
            if o_que == 'fugir' and rol: t['teste'] += 1; t['passou'] += rol[0]['passou']; t['contra'] = rol[0]['contra']
    d, f = T_['deixar'], T_['fugir']; vem = min(1.0, inv[1] + K.INVESTE_FUGA)
    folga = lambda medido, p, m: abs(medido - p) <= 4 * math.sqrt(p * (1 - p) / max(1, m)) + 0.02
    return ('O BICHO QUE VIU O CAÇADOR (o acaso): em quem o deixa, investe pela índole da espécie, e a luta começa perto, sem surpresa; atrás de quem corre, vem mais vezes, e aí é Agilidade contra a dele: '
            'quem passa escapa; quem falha luta colado e surpreendido',
            f"lobos que viram o caçador de começo: deixados {d['n']} vezes, investiram em {pc(d['luta'] / max(1, d['n']))} (a índole: {pc(inv[1])}); de {f['n']} fugas, vieram atrás em {pc(f['teste'] / max(1, f['n']))} (a tabela: {pc(vem)}), "
            f"e de {f['teste']} testes de Agilidade contra {f.get('contra', '?')} ele passou em {f['passou']}: alcançado {f['luta']} vezes; cada desfecho com o começo, a surpresa e o teste certos: {d['certo'] + f['certo']} de {d['n'] + f['n']}",
            not mal and d['n'] >= k - 2 and d['certo'] == d['n'] and f['certo'] == f['n'] and f['luta'] == f['teste'] - f['passou'] and folga(d['luta'] / max(1, d['n']), inv[1], d['n']) and folga(f['teste'] / max(1, f['n']), vem, f['n']))


def _a_luta_do_ato(n):
    """a luta é a do ato.py luta: no arquivo, com paradas e ordens; volta ao estado por um evento só; com ela aberta o turno não fecha"""
    with rascunho() as d:
        E = mundo(7, prata=200, mao=4, atributos={'Percepção': 90}); pid = 'eu'; estado.grava(E); R = None
        for _ in range(20):
            R = quieto(caca.sair, E, pid, 'mata', alvo='corça', blocos=1)
            if R['fase'] == 'encontro' and R['encontro']['viu'] == 'caçador': break
            if R['fase'] == 'encontro': quieto(caca.fugir, E, pid)
            quieto(ato.dormir, E, pid, 3, para=False)
            while E['gente'][pid]['corpo']['fome'] >= 2: quieto(ato.comer, E, pid)
        enc = R['encontro']; inis, nv, _ = caca.posicao(enc); c0 = caca.bichos_de(E, 'mata')['corça']; r1 = recusa(lambda: caca.atacar(E, pid, inicio='colado' if 'colado' not in inis else 'de cima'))
        r2 = recusa(lambda: caca.atacar(E, pid, vantagens=['alto', 'cerco', 'estreito'])); R = quieto(caca.atacar, E, pid, inicio='perto', vantagens=['cerco'][:nv]); arq = R['luta']; estado.grava(E)
        S = json.load(open(arq, encoding='utf-8')); cen = json.load(open(arq.replace('_luta.json', '_cenario.json'), encoding='utf-8'))
        aberta = (E['turno']['lutas'] == [dict(arq=os.path.abspath(arq), fim=None)] and S['mundo'] and S['paradas'] == ['a luta vai começar'] and S['surpresa'] == 'B' and cen['A'] == [dict(id='eu', controla=True)]
                  and len(cen['B']) == enc['n'] and all(x['bicho']['especie'] == 'corça' for x in cen['B']) and S['L'][0]['id'] == 'eu' and S['L'][0]['controla'] and 'RODADA 0' in R['texto'])
        turno.pergunta(E, 'a', ['a=x', 'b=y']); turno.pergunta(E, 'b', ['a=x', 'b=y']); r3 = recusa(lambda: turno.fecha(E, 'caçou')); r4 = recusa(lambda: caca.segue(E, pid)); r5 = recusa(lambda: caca.luta_roda(E, pid, ['Aldric: voar']))
        paradas = 0
        for _ in range(200):                                        # a luta roda pelo ato.py, direto, como o Mestre faria: até o FIM
            E = estado.carrega(); S = json.load(open(arq, encoding='utf-8'))
            if S['fim']: break
            quieto(ato.luta_roda, E, arq, ['Aldric: atacar'] if S['L'][0]['estado'] == 'pe' else []); estado.grava(E); paradas += 1
        E = estado.carrega(); p = E['gente'][pid]; f = S['L'][0]; antes = caca.saida(p)['fase']; A = quieto(caca.segue if p['estado'] == 'vivo' else caca.acerta, E, pid); estado.grava(E); evs = eventos(d)
        nl = [e for e in evs if e['tipo'] == 'luta']; nd = [e for e in evs if e['tipo'] == 'despojo']; mortos = sum(x['estado'] in ('morto', 'caido') for x in S['L'][1:]) if S['fim'] == 'A' else sum(x['estado'] == 'morto' for x in S['L'][1:])
        volta = (len(nl) == 1 and len(nd) == (1 if mortos else 0) and (p['estado'] == 'morto') == (f['estado'] == 'morto') and (p['estado'] == 'morto' or p['pv'] <= max(1, f['pv'])) and len(p['feridas']) == len(f['feridas'])
                 and caca.bichos_de(E, 'mata').get('corça', 0) == c0 - mortos and antes == 'luta' and E['turno']['lutas'][0]['fim'] == S['fim'] and not estado.valida(E))
    return ('A LUTA É A DO `ato.py luta`: o caça.py só monta o cenário (a casa com ficha no mundo; os bichos, tirados da contagem) e chama o ato.luta_nova; a luta para e pede ordem, roda pelo `ato.py luta roda`, '
            'e volta ao estado por um evento `luta`; só depois vêm as contas (um evento `despojo`). Com a luta aberta o turno não fecha e a saída não segue',
            f"a luta abriu no arquivo, registrada no turno, parada antes da 1ª rodada, com o caçador comandado e {enc['n']} corça(s) surpreendida(s): {'sim' if aberta else 'NÃO'}; começar de onde a posição não dá: {'recusado' if r1 else 'ACEITO'}; "
            f"três vantagens: {'recusado' if r2 else 'ACEITO'}; fechar o turno com ela aberta: {'recusado' if r3 else 'ACEITO'}; seguir a procura com ela aberta: {'recusado' if r4 else 'ACEITO'}; ordem que não existe: {'recusada' if r5 else 'ACEITA'}; "
            f"rodada pelo ato.py em {paradas} parada(s) até o fim ({S['fim']}, {S['r']} rodadas); eventos de luta: {len(nl)}; de despojo: {len(nd)} ({mortos} corça(s) a menos na contagem); PV e feridas do estado iguais aos da luta: {'sim' if volta else 'NÃO'}",
            aberta and r1 and r2 and r3 and r4 and r5 and volta and paradas >= 1)


def _a_virada(n):
    """a virada: os bichos criam devagar até o teto; a espécie caçada até o fim some por muito tempo; o chefe demora a nascer; a matéria volta devagar"""
    sem = range(1, 1 + max(8, n // 30)); volta = []; some = []; teto_ok = True
    for s in sem:
        E = mundo(s, pop=0); poe(E, corça=20); d = 0
        while caca.bichos_de(E, 'mata').get('corça', 0) < NOVE * 80 and d < 600: dias_sem_ninguem(E); d += 1
        volta.append(d)
        for _ in range(120): dias_sem_ninguem(E, 1); teto_ok = teto_ok and all(q <= caca.teto_de(E, 'mata')[e] for e, q in caca.bichos_de(E, 'mata').items())
        E = mundo(s, pop=0); poe(E, corça=0); d = 0; zero = None
        while caca.bichos_de(E, 'mata').get('corça', 0) < NOVE * 80 and d < 1500:
            dias_sem_ninguem(E); d += 1
            if zero is None and caca.bichos_de(E, 'mata').get('corça', 0) > 0: zero = d
        some.append((zero, d))
    chefe = []
    for s in range(1, 1 + max(30, n // 5)):
        E = mundo(s, pop=0, habitat='serra', perigo=3, fauna={'serpe': 1}); poe(E, serpe=0); d = 0
        while not caca.bichos_de(E, 'mata').get('serpe') and d < 3000: dias_sem_ninguem(E); d += 1
        chefe.append(d)
    E = mundo(1, pop=0, habitat='serra', perigo=2); estado.aplica(E, 'gera', [['lugar', 'mata', 'coleta.metal:0', 'poe', 0], ['lugar', 'mata', 'coleta.metal:2', 'poe', 0]], texto='a mina esgotada'); ev0 = E['relogio']['eventos']; dias_sem_ninguem(E, 30)
    m30 = caca.coleta_de(E, 'mata'); t = caca.coleta_teto(E, 'mata'); dias_sem_ninguem(E, 600); m630 = caca.coleta_de(E, 'mata'); mat_ok = all(m630.get(b, 0) <= t[b] for b in t)
    E1 = mundo(4, pop=0); poe(E1, corça=10, javali=5, lobo=2); n0 = E1['relogio']['eventos']; dias_sem_ninguem(E1, 1); tipos = None
    Ea = mundo(9, pop=0); poe(Ea, corça=10, javali=5, lobo=2); dias_sem_ninguem(Ea, 200); Eb = mundo(9, pop=0); poe(Eb, corça=10, javali=5, lobo=2); dias_sem_ninguem(Eb, 200); Ec = mundo(10, pop=0); poe(Ec, corça=10, javali=5, lobo=2); dias_sem_ninguem(Ec, 200)
    mesmo = retrato(Ea) == retrato(Eb) and caca.bichos_de(Ea, 'mata') != caca.bichos_de(Ec, 'mata') or retrato(Ea) == retrato(Eb) and retrato(Ea) != retrato(Ec)
    meio = lambda v: sorted(v)[len(v) // 2]; media = sum(chefe) / len(chefe); espera = K.CHEFE_NASCE[3]; esgota = [x[1] for x in some]
    certo = (all(VOLTA[0] <= d <= VOLTA[1] for d in volta) and teto_ok and min(esgota) > VOLTA[1] and all(z is not None for z, _ in some) and 0.6 * espera <= media <= 1.5 * espera and mat_ok and mesmo
             and 0 < m30.get('metal:0', 0) < t['metal:0'] and m30.get('metal:2', 0) <= 2)
    return ('A VIRADA: os bichos criam devagar e nunca passam do teto; de 20 em 80, a corça volta a nove décimos entre 30 e 120 dias; caçada até o fim, some por muito tempo (espera o casal que vem de fora); '
            'o chefe demora a nascer; a matéria volta devagar; mesma semente, mesmo ermo',
            f"{len(volta)} mundos sem ninguém: de 20 para 72 corças em {min(volta)} a {max(volta)} dias (a do meio: {meio(volta)}); nunca acima do teto: {'sim' if teto_ok else 'NÃO'}; de ZERO, a primeira volta depois de {min(z for z, _ in some)} a {max(z for z, _ in some)} dias, "
            f"e as 72 depois de {min(esgota)} a {max(esgota)} (a do meio: {meio(esgota)}); a serpe morta nasce de novo, em média, em {media:.0f} dias ({len(chefe)} mundos; a tabela: {espera}); "
            f"a mina esgotada (minério Comum, teto {t['metal:0']:g}) tem {m30.get('metal:0', 0):g} depois de 30 dias e {m630.get('metal:0', 0):g} depois de 630; o minério Raro (teto {t['metal:2']:g}), {m30.get('metal:2', 0):g} e {m630.get('metal:2', 0):g}; "
            f"mesma semente, mesmo ermo depois de 200 dias, e outra semente, outro: {'sim' if mesmo else 'NÃO'}", certo)


def _a_coleta(n):
    """a coleta: um teste por bloco; o que se tira sai do ermo e entra na carga no mesmo evento; rareando, fica mais difícil; o que acabou, acabou"""
    with rascunho() as d:
        E = mundo(11, habitat='serra', perigo=2, fauna={}, prata=300, nivel=30, kit='espada'); pid = 'eu'; estado.grava(E); f0 = foto(E); c_cheio = caca.coleta_contra(E, 'mata', 'metal:0'); saidas = 0; p0 = prata(E)
        estado.aplica(E, 'gera', [['lugar', 'mata', 'coleta.metal:1', 'poe', 3]], onde='mata', texto='um veio curto'); f0 = foto(E); c1 = caca.coleta_contra(E, 'mata', 'metal:1'); V = dict(refeicoes=0, jejum=0, camas=0, chao=0)
        def um_dia(bem, blocos=2):
            nonlocal saidas
            _come(E, pid, V, ate=2); R = quieto(caca.coletar, E, pid, bem, 'mata', blocos=blocos); saidas += 1
            while R['fase'] not in ('fim', 'morto'): R = quieto(caca.volta if R['fase'] == 'procura' else caca.fugir, E, pid)
            _dorme(E, pid, V, 3); _come(E, pid, V); E['turno']['dados'] = []; return R
        for _ in range(12): um_dia('metal:0')
        ferro = E['gente'][pid]['carga'].get('metal:0', 0); R = None
        for _ in range(30):
            if caca.coleta_de(E, 'mata').get('metal:1', 0) <= 0: break
            um_dia('metal:1')
        veio = caca.coleta_de(E, 'mata').get('metal:1', 0); antes = E['gente'][pid]['carga'].get('metal:1', 0)
        estado.aplica(E, 'gera', [['lugar', 'mata', 'coleta.metal:1', 'poe', 0]], onde='mata', texto='o veio acabou (a prova segura o que voltou na virada)'); R = um_dia('metal:1', 1); esgotou = 'esgotou' in R['texto'] and E['gente'][pid]['carga'].get('metal:1', 0) == antes
        r1 = recusa(lambda: caca.coletar(E, pid, 'erva:0', 'mata')); r2 = recusa(lambda: caca.coletar(E, pid, 'comida', 'mata')); r3 = recusa(lambda: estado.aplica(E, 'mestre', [['lugar', 'mata', 'coleta.metal:1', 'soma', -1]]))
        estado.grava(E); Z = razao(eventos(d)); f1 = foto(E); mal = fecha(Z, f0, f1); p = E['gente'][pid]; tr = p.get('treino', {}).get('coleta', 0)
        estado.aplica(E, 'gera', [['lugar', 'mata', 'coleta.metal:0', 'poe', 30]], onde='mata', texto='a mina rareia'); c_ralo = caca.coleta_contra(E, 'mata', 'metal:0')
        certo = not mal and ferro > 0 and Z['tirado'].get('metal:0', 0) == ferro and veio == 0 and esgotou and r1 and r2 and r3 and c_ralo > c_cheio and c1 > c_cheio and tr >= 24 and not estado.valida(E) and prata(E) == p0
    return ('A COLETA: um teste por bloco (Força ou Percepção, mais a maestria de coleta) contra a fartura da matéria; o que se tira sai do `coleta` do ermo e entra na carga no mesmo evento; rareando, fica mais difícil; o que acabou, acabou',
            f"um mineiro de nível 30 na serra, {saidas} saídas: tirou {ferro} de minério Comum em 24 blocos (saíram do ermo {Z['tirado'].get('metal:0', 0)}); o veio de 3 de minério Incomum foi até {veio} e depois \"esgotou\": {'sim' if esgotou else 'NÃO'}; "
            f"o número: {c_cheio} com a mina cheia, {c_ralo} com um quinto dela, {c1} no Incomum; erva que a serra não dá: {'recusado' if r1 else 'ACEITO'}; \"comida\": {'recusado' if r2 else 'ACEITO'}; tirar do ermo o que não há: {'recusado' if r3 else 'ACEITO'}; "
            f"{tr} blocos de treino de coleta; a conta {'fecha' if not mal else 'NÃO FECHA: ' + mal[0]}; a prata do mundo {'fecha' if prata(E) == p0 else 'NÃO FECHA'}", certo)


def _a_maestria(n):
    """a maestria de caça sobe por blocos de procura; de Mestre para cima pede o feito (a carcaça de um bicho Raro, Épico)"""
    E = mundo(1, pop=0); pid = 'eu'; da = lambda k: estado.aplica(E, 'mestre', [['pessoa', pid, 'treino.caça', 'soma', k]], texto='blocos de prova')
    da(39); caca.sobe(E, pid); a = caca.mao(E['gente'][pid]); da(1); caca.sobe(E, pid); b = caca.mao(E['gente'][pid]); da(560); t = caca.sobe(E, pid); c = caca.mao(E['gente'][pid])
    estado.aplica(E, 'mestre', [['pessoa', pid, 'marca.feito_caça', 'poe', 2]], texto='a carcaça de uma pantera'); caca.sobe(E, pid); dd = caca.mao(E['gente'][pid]); da(1000); caca.sobe(E, pid); e = caca.mao(E['gente'][pid])
    estado.aplica(E, 'mestre', [['pessoa', pid, 'marca.feito_caça', 'poe', 3]], texto='a carcaça de uma serpe'); caca.sobe(E, pid); f = caca.mao(E['gente'][pid]); r0 = caca.rastro_contra(E, 'mata', 'corça')
    nome = lambda x: T.MAESTRIAS[x]
    return ('A MAESTRIA DE CAÇA sobe por blocos de procura e soma no rastro; de Mestre para cima, os blocos não bastam: pede o feito (ficar com a carcaça de um bicho Raro; para Lendário, Épico)',
            f"com 39 blocos: {nome(a)}; com 40: {nome(b)}; com 600 e nenhum feito: {nome(c)}{t}; depois da carcaça Rara: {nome(dd)}; com 1.600 blocos: {nome(e)}; depois da carcaça Épica: {nome(f)}",
            (a, b, c, dd, e, f) == (0, 2, 4, 6, 6, 8) and 'falta o feito' in t)


def _as_recusas(n):
    """o que não pode, não começa; e nada muda pela metade"""
    with rascunho():
        E = mundo(2, prata=50); pid = 'eu'; cacador(E, 'bera', nome='Bera'); E['lugares']['longe'] = dict(nome='o Fim do Mundo', tipo='ermo', estoque={}); estado.grava(E); antes = retrato(E)
        casos = [('ermo que não é vizinho', lambda: caca.sair(E, pid, 'longe')), ('ermo que não existe', lambda: caca.sair(E, pid, 'lua')), ('espécie que não existe', lambda: caca.sair(E, pid, 'mata', alvo='unicórnio')),
                 ('zero blocos', lambda: caca.sair(E, pid, 'mata', blocos=0)), ('sete blocos', lambda: caca.sair(E, pid, 'mata', blocos=7)), ('companheiro que não existe', lambda: caca.sair(E, pid, 'mata', com=['ninguém'])),
                 ('ir consigo mesmo', lambda: caca.sair(E, pid, 'mata', com=['eu'])), ('atacar sem bicho à frente', lambda: caca.atacar(E, pid)), ('deixar sem bicho à frente', lambda: caca.deixar(E, pid)),
                 ('fugir sem bicho à frente', lambda: caca.fugir(E, pid)), ('voltar sem ter saído', lambda: caca.volta(E, pid)), ('seguir sem ter saído', lambda: caca.segue(E, pid)), ('luta sem luta', lambda: caca.luta_roda(E, pid, ['Aldric: atacar'])),
                 ('coletar o que não é matéria', lambda: caca.coletar(E, pid, 'prata')), ('coletar o que a mata não dá', lambda: caca.coletar(E, pid, 'metal:0')), ('povoar por cima', lambda: caca.povoa(E, 'mata', 'brejo')),
                 ('povoar lugar que não existe', lambda: caca.povoa(E, 'lua', 'brejo')), ('habitat que não existe', lambda: caca.povoa(E, 'longe', 'deserto')), ('pessoa que não existe', lambda: caca.sair(E, 'fantasma'))]
        rec = [nome for nome, f in casos if recusa(f)]; intacto = antes == retrato(E)
        R = quieto(caca.sair, E, pid, 'mata', alvo='corça', blocos=1); aberta = None
        if caca.saida(E['gente'][pid]): aberta = recusa(lambda: caca.sair(E, pid, 'mata')); quieto(caca.fugir if R['fase'] == 'encontro' else caca.volta, E, pid)
        estado.aplica(E, 'mestre', [['pessoa', pid, 'estado', 'poe', 'morto'], ['pessoa', pid, 'pv', 'soma', -999]], texto='morre, para a prova'); morto = recusa(lambda: caca.sair(E, pid, 'mata'))
        with contextlib.redirect_stdout(io.StringIO()) as o: caca.main([])
        uso = o.getvalue().strip() == caca.__doc__.strip()
        S = PM.vila(); a0 = retrato(S); sem = recusa(lambda: caca.sair(S, 'eu')); caca.virada(S); nada = a0 == retrato(S) and caca.mesa(S) == []
    return ('AS RECUSAS: o que não pode não começa, e nada muda pela metade; sem argumento, o script só diz o uso; onde não há ermo, a caça não faz nada',
            f"{len(rec)} de {len(casos)} recusados" + (f" (ACEITOS: {', '.join(nome for nome, _ in casos if nome not in rec)})" if len(rec) < len(casos) else '') + f"; estado {'intacto' if intacto else 'MUDOU'}; "
            f"sair com uma saída aberta: {'recusado' if aberta else 'não houve saída aberta para tentar' if aberta is None else 'ACEITO'}; morto não caça: {'recusado' if morto else 'ACEITO'}; sem argumento: {'só o uso' if uso else 'FEZ OUTRA COISA'}; "
            f"na vila da etapa 1 (sem ermo vizinho): sair é recusado, a virada não gera evento e a mesa fica calada: {'sim' if sem and nada else 'NÃO'}", len(rec) == len(casos) and intacto and aberta is not False and morto and uso and sem and nada)


def _a_mesa(n):
    """as linhas da caça para a MESA.md: o que se sabe em palavras, a contagem só para o Mestre, sem os chefes, e curta"""
    with rascunho():
        E = mundo(1, habitat='serra', perigo=3); pid = 'eu'; poe(E, lobo=5, urso=0); estado.grava(E); L = caca.mesa(E); txt = '\n'.join(L); pub = '\n'.join(x for x in L if 'SÓ O MESTRE' not in x); mestre = '\n'.join(x for x in L if 'SÓ O MESTRE' in x)
        chefes = [d['nome'] for d in TB.ESPECIES.values() if d['chefe']]; certo = ('a Mata de Prova' in pub and 'lobo (há, mas rareou)' in pub and 'urso (sumiu)' in pub and not any(c in pub for c in chefes) and 'lobo 5/12' in mestre and 'serpe 1/1' in mestre
                                                                                 and 'minério' not in pub and 'metal Comum (há fartura)' in pub and 'caca.py sair' in pub)
        R = quieto(caca.sair, E, pid, 'mata', alvo='lobo', blocos=1); aberta = caca.saida(E['gente'][pid]); L2 = '\n'.join(caca.mesa(E)); avisa = (not aberta) or 'SAÍDA ABERTA' in L2
        if aberta: quieto(caca.fugir if R['fase'] == 'encontro' else caca.volta, E, pid)
        inteira = turno.mesa(E) if E['gente'][pid]['estado'] == 'vivo' else ''
    return ('A MESA: as linhas da caça dizem o que todo mundo sabe (a fartura, em palavras), sem os chefes; a contagem vai numa linha marcada SÓ O MESTRE; a saída aberta aparece; e cabe no teto da MESA.md',
            f"as linhas da caça e dos bichos: {len(txt.encode())} bytes ({len(L)} linhas); a MESA inteira da vila de prova, com o mercado e a caça: {len(inteira.encode())} bytes (o teto são 8.000); fartura em palavras, chefes só na linha do Mestre, a saída aberta avisada: {'sim' if certo and avisa else 'NÃO'}",
            certo and avisa and len(txt.encode()) <= 3000 and len(inteira.encode()) <= 8000)


def _o_robo_vive(P):
    """o robô vive de verdade: come, dorme, paga a cama, vende o despojo; a prata do mundo fecha"""
    n = len(P); dias = sum(V['dias'] for V in P); ref = sum(V['refeicoes'] for V in P); camas = sum(V['camas'] for V in P); chao = sum(V['chao'] for V in P); jej = sum(V['jejum'] for V in P)
    bolso = sorted(V['bolso'][1] for V in P if V['vivo']); pr = all(V['prata'] for V in P); qb = sum(bool(V['quebrado']) for V in P); ab = sum(V['aberta'] for V in P)
    return ('O ROBÔ VIVE DE VERDADE: come e paga, dorme na cama e paga, vende o despojo na loja da vila e vive disso; a prata do mundo fecha e o estado fica inteiro',
            f"{n} vidas do prudente, {dias} dias: {vz(ref / dias)} refeição e {vz(camas / dias)} cama pagas por dia; noites no chão: {chao}; vezes com fome sem comer: {jej}; dias de folga (o corpo pediu, ou ferido): {sum(V['folgas'] for V in P)} ({sum(V['repousos'] for V in P)} de repouso de ferida); "
            + (f"os vivos acabam com {bolso[0]} a {bolso[-1]} de prata (a do meio: {bolso[len(bolso) // 2]}; começaram com 30); " if bolso else '') + f"vendas recusadas pela loja: {sum(V['nao_vendeu'] for V in P)}; "
            f"a prata do mundo {'fecha em todas' if pr else 'NÃO FECHA'}; estados quebrados: {qb}; saídas largadas abertas: {ab}", pr and qb == 0 and ab == 0 and 0.8 <= ref / dias <= 1.2 and camas / dias >= 0.9)


def provas(n=300):
    out = []; k = max(20, n // 10); P = []; A = []
    def roda(nome, f):
        try:
            r = f(); out.extend(r if isinstance(r, list) else [r])
        except (SystemExit, Exception) as e: out.append((nome, f'A PROVA QUEBROU: {type(e).__name__}: {e}', False))
    try: P = [vida(s, 'prudente') for s in range(1, k + 1)]
    except (SystemExit, Exception) as e: out.append(('AS VIDAS DO PRUDENTE (a medição)', f'A PROVA QUEBROU: {type(e).__name__}: {e}', False))
    try: A = [vida(1000 + s, 'afoito') for s in range(1, k + 1)]
    except (SystemExit, Exception) as e: out.append(('AS VIDAS DO AFOITO (a medição)', f'A PROVA QUEBROU: {type(e).__name__}: {e}', False))
    for nome, f in (('O CAÇADOR', lambda: _o_prudente(P)), ('O AFOITO', lambda: _o_afoito(A)), ('CAÇADA DEMAIS', lambda: _sessenta(range(1, 1 + max(2, n // 100)))), ('NENHUMA CONTAGEM NEGATIVA', lambda: _nunca_negativa(P + A)),
                    ('O NÚCLEO DO CHEFE', _o_nucleo), ('A CONTA FECHA', lambda: _a_conta(P, A)), ('A AMEAÇA É LIDA ANTES', lambda: _a_ameaca_antes(n)), ('O BICHO QUE VIU O CAÇADOR', lambda: _o_que_viu(n)),
                    ('A LUTA É A DO ato.py', lambda: _a_luta_do_ato(n)), ('A VIRADA', lambda: _a_virada(n)), ('A COLETA', lambda: _a_coleta(n)), ('A MAESTRIA DE CAÇA', lambda: _a_maestria(n)),
                    ('O ROBÔ VIVE DE VERDADE', lambda: _o_robo_vive(P)), ('AS RECUSAS', lambda: _as_recusas(n)), ('A MESA', lambda: _a_mesa(n))):
        roda(nome, f)
    return out


def main():
    a = sys.argv[1:]
    if a and not a[0].isdigit(): print(__doc__); return True
    n = int(a[0]) if a else 300
    print('BANCO DE PROVAS DA CAÇA E DA COLETA · etapa 2: o ermo contado, o rastro, a ameaça, a luta, o despojo, a virada\n')
    res = provas(n)
    for nome, deu, passa in res: print(f"  {'passa' if passa else 'FALHA'}  {nome}: {deu}")
    print(f'\n{sum(p for _, _, p in res)} de {len(res)} provas passam.')
    return all(p for _, _, p in res)


if __name__ == '__main__':
    sys.exit(0 if main() else 1)
