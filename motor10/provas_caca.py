#!/usr/bin/env python3
"""provas_caca.py — MOTOR 10: O BANCO DE PROVAS DA CAÇA E DA COLETA (etapa 2: o ermo contado, o rastro, a ameaça lida antes, a luta do ato.py, o despojo, a virada).

As metas são as do contrato (projeto/ETAPA2.md, seção 7). As provas rodam em mundos de rascunho, cada um numa pasta temporária (MOTOR10_MUNDO); nunca num save.
O dado é o de verdade (teste.rola no rastro, na fuga e na coleta; o do luta.py na luta): por isso as medidas mudam um pouco de uma rodada para outra,
e as metas de frequência são medidas em muitas vidas.

O ROBÔ CAÇADOR vive de verdade numa vila com mercado e forja: dorme na cama e paga, come e paga, vende o despojo na loja (a 60% do preço do dia), manda consertar
o que veste (o conserto pago da forja) e sai para o ermo quando o corpo deixa: a ida de manhã, até dois blocos de procura, a volta à noite.
  O CAÇADOR (nível 10, gente gerada; arco, espada de reserva, cota e elmo de malha, tudo Comum) procura corça. Lê a ameaça e só ataca a presa de grau F que ele viu
    primeiro, de longe, com o terreno que o rastro deu: com duas vantagens, o alto e o cerco (uma corça ou duas); com uma, o cerco se a corça está só, o alto se
    são duas; sem nenhuma, só a corça sozinha. Ele ENCURRALA sempre que pode: é assim que a carcaça fica, e é daí que vem o perigo. Segue o sangue da presa que
    fugiu ferida. O resto ele deixa; do bicho que o viu, foge (da presa, só sai de perto). Cansado ou machucado, recua e volta. Ferido, repousa até sarar
    (sem prata, pega um bloco de diária por dia). A ordem na luta é a simples: "atacar".
  O AFOITO é o mesmo homem: procura o que aparecer e ataca tudo o que aparece (bando, grau maior, o que o viu primeiro), todo dia, ferido ou não.
  O CAUTELOSO (para comparar; não é meta) é o mesmo homem sem encurralar o par, nem a corça que ele não vê do alto.
A LUTA de todo robô é a do `ato.py luta` (ato.luta_nova e ato.luta_roda, em arquivo, com a ordem dada a cada parada), como na mesa.

Uso: python3 provas_caca.py [N]      N = o tamanho das amostras (padrão 300): N ÷ 4 vidas de 30 dias do caçador e do afoito (no mínimo 40), e metade disso do cauteloso
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
# ---------- os robôs ----------
ROBO = dict(nivel=10, cat=0, kit='arco', alvo='corça', ordem='atacar',
            reserva=6,      # ferido ou machucado, repousa; com menos prata do que isto, pega um bloco de diária por dia
            cansado=7,      # com este cansaço ele não luta: recua e volta
            pv=0.8,         # abaixo desta fração do PV ele não luta nem sai
            conserta=4)     # a peça que chega a esta durabilidade vai à forja
VETERANO = dict(nivel=30, cat=1, kit='espada', mao=4)       # quem caça os 60: de espada, escudo e malha Incomuns, Treinado em caça


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
    """a mão do gerador (gente, atributo e maestria não têm verbo de nascer no gravador): faz da pessoa um caçador deste nível, gente gerada, com o conjunto desta
    categoria: de arco (arqueiro: arco, espada de reserva, cota e elmo de malha) ou de espada (guerreiro: espada, escudo, cota e elmo de malha). As peças nascem por evento."""
    if pid not in E['gente']: E['gente'][pid] = dict(copy.deepcopy(E['gente']['eu']), jogador=False, nome=nome or pid, carga={}, marca={}, treino={}, moedas=50)
    p = E['gente'][pid]; g = padrao(p['nome'], nivel, molde='arqueiro' if kit == 'arco' else 'guerreiro', atributos=atributos); m = T.maestria_tipica(nivel); n = p['nome']
    p.update(nivel=nivel, atributos=g['atributos'], maestria={'arco': m, 'espada': m, 'caça': mao}, feridas=[], corpo=dict(fome=0, sono=0, cansaco=0)); p['pv'] = estado.pv_max(p)
    velhas = [['item', i, 'some'] for i, it in E['itens']['itens'].items() if it.get('dono') == pid]; s0 = E['itens']['seq']
    pecas = [(item('arma', cat, f'Arco de {n}', familia='arco', dono=pid), 'arma'), (item('arma', cat, f'Espada de {n}', familia='espada', dono=pid), 'arma2')] if kit == 'arco' else \
            [(item('arma', cat, f'Espada de {n}', familia='espada', dono=pid), 'arma'), (item('escudo', cat, f'Escudo de {n}', dono=pid), 'escudo')]
    pecas += [(item('armadura', cat, f'Cota de {n}', material='malha', dono=pid), 'veste'), (item('armadura', cat, f'Elmo de {n}', material='malha', cobre=['cabeça'], dono=pid), 'veste')]
    estado.aplica(E, 'gera', velhas + [['item', 'nasce', it] for it, _ in pecas], texto=f'o conjunto de {n}')
    estado.aplica(E, 'gera', [['item', f'i{s0 + k + 1:04d}', 'uso', 'poe', uso] for k, (_, uso) in enumerate(pecas)], texto=f'{n} se veste')
    return p


def mundo(semente=1, habitat='floresta', perigo=1, pop=400, prata=30, fauna=None, materia=None, **quem):
    """a vila de prova (com mercado e forja de vila, se pop), à meia-noite do Dia 1, um ermo vizinho povoado pela tabela (ou com a fauna e a matéria dadas), e o caçador"""
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


def quieto(f, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()): return f(*a, **k)


def retrato(E): return json.dumps({k: E[k] for k in estado.ARQS}, sort_keys=True, ensure_ascii=False)
def prata(E): return mercado.prata_do_mundo(E)
def base(bens): return sum(q * (C.base(b) or 0) for b, q in bens.items())       # o valor de um despojo ao preço de base do mercado
def pc(x, casas=0): return f'{100 * x:.{casas}f}%'.replace('.', ',')
def vz(x, casas=2): return f'{x:.{casas}f}'.replace('.', ',')
def sn(x): return 'sim' if x else 'NÃO'
def cenario(R): return json.load(open(R['luta'].replace('_luta.json', '_cenario.json'), encoding='utf-8'))
def eventos(d):
    arq = os.path.join(d, 'eventos.jsonl')
    return [json.loads(x) for x in open(arq, encoding='utf-8').read().splitlines()] if os.path.exists(arq) else []


def encerra(E, pid, R=None):
    """fecha a saída aberta sem lutar: do bicho à frente, foge; parada, volta. (Se a fuga acabar em luta, a saída fica aberta: quem chama decide.)"""
    for _ in range(4):
        s = caca.saida(E['gente'][pid])
        if not s or E['gente'][pid]['estado'] != 'vivo' or s['fase'] == 'luta': break
        R = quieto(caca.fugir if s['fase'] == 'encontro' else caca.volta, E, pid)
    return R


def noite(E, pid):
    """dorme três blocos na cama e come, para a prova seguir com o corpo inteiro (o caderno do turno de rascunho não cresce)"""
    quieto(ato.dormir, E, pid, 3, para=False)
    while E['gente'][pid]['estado'] == 'vivo' and E['gente'][pid]['corpo']['fome'] >= 2 and E['gente'][pid]['moedas'] >= M.REFEICAO_PRECO: quieto(ato.comer, E, pid)
    E['turno']['dados'] = []


def ate_encontrar(E, pid, quer=lambda R: True, alvo='corça', blocos=1, vezes=40, **mais):
    """sai para caçar (uma saída por dia, dormindo e comendo entre elas) até dar com um encontro que sirva; os que não servem, larga. Devolve o encontro, ou None."""
    for _ in range(vezes):
        R = quieto(caca.sair, E, pid, 'mata', alvo=alvo, blocos=blocos, **mais)
        if R['fase'] == 'encontro' and quer(R): return R
        encerra(E, pid, R)
        if caca.saida(E['gente'][pid]) or E['gente'][pid]['estado'] != 'vivo': return None
        noite(E, pid)
    return None


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
            if carga and not bi: Z['mal'].append(f"#{ev['id']}: despojo sem bicho")
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
    """(a contagem, a matéria do ermo, a soma das cargas de toda a gente, mais o que ficou no chão do ermo com quem morreu ali: a regra da morte põe a carga do morto no estoque do lugar)"""
    g = {}
    for p in E['gente'].values():
        for b, q in p.get('carga', {}).items(): g[b] = g.get(b, 0) + q
    for b, q in E['lugares'][ermo].get('estoque', {}).items():
        if b != 'prata' and q: g[b] = g.get(b, 0) + q
    return dict(caca.bichos_de(E, ermo)), dict(caca.coleta_de(E, ermo)), g


# ---------- o robô caçador ----------
def caderno():
    """o que o robô anota da própria vida"""
    return dict(saidas=0, feridas=0, lutas=0, forcadas=0, encontros=0, viu_bicho=0, deixou=0, recuou=0, fugiu=0, sangue=0, sangue_achou=0, valor=0, carcacas=0, fugiram_b=0, mortos_b={}, por_especie={}, bens={}, mal=[],
                refeicoes=0, jejum=0, camas=0, chao=0, prata_venda=0, nao_vendeu=0, consertos=0, prata_conserto=0, sem_conserto=0, folgas=0, repousos=0, jornais=0, morreu=None)


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
    """o robô cuida do que veste: a peça que chega a poucos pontos de durabilidade vai à forja da vila (o conserto pago do oficio.py: 2% do preço por ponto,
    e a espera). Devolve os blocos gastos."""
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


def _fraco(E, pid):
    p = E['gente'][pid]; return p['corpo']['cansaco'] >= ROBO['cansado'] or p['pv'] < ROBO['pv'] * estado.pv_max(p)      # cansado ou machucado: não luta


def prudente(E, pid, R, encurrala=True):
    """o que o caçador faz diante do bicho: lê a ameaça (o grau e quantos são), a posição (o que o rastro deu) e o próprio corpo. Só ataca a presa de grau F que ele
    viu primeiro, e de longe. Com o cerco à mão, encurrala (é assim que a carcaça fica). encurrala=False é o CAUTELOSO: só encurrala a corça sozinha, e do alto."""
    enc = R['encontro']; e = TB.ESPECIES[enc['especie']]; _, nv, _ = caca.posicao(enc); ferida = bool(enc.get('feridos')); um = enc['n'] == 1
    if enc['viu'] != 'caçador': return ('deixar',) if e['grau'] == 'F' else ('fugir',)       # a presa que o viu não investe: ele só sai de perto; do resto, corre
    if _fraco(E, pid): return ('recuar',)                                                   # recua sem ser visto e volta
    if e['grau'] != 'F': return ('deixar',)
    if nv >= 2: return ('atacar', 'longe', ['alto', 'cerco'] if um or encurrala else ['alto', 'estreito'])
    if nv == 1: return ('atacar', 'longe', ['cerco'] if um and encurrala else ['alto'])
    return ('atacar', 'longe', []) if um or ferida else ('deixar',)                          # sem o terreno: só uma corça sozinha, ou a presa já ferida


def cauteloso(E, pid, R): return prudente(E, pid, R, encurrala=False)
CUIDAM = (prudente, cauteloso)      # os robôs que olham o próprio corpo antes de lutar


def afoito(E, pid, R): return ('atacar', None, [])


def veterano(E, pid, R):
    """quem caça os 60: ataca toda corça que vê, de perto, com o cerco quando o rastro o dá, e segue o sangue da que foge; do resto, desvia. Só para por ferida grave."""
    enc = R['encontro']; inis, nv, _ = caca.posicao(enc)
    if enc['especie'] != 'corça': return ('deixar',) if enc['viu'] == 'caçador' else ('fugir',)
    return ('atacar', 'colado' if 'colado' in inis else inis[-1], ['cerco'] if nv else [])


def uma_saida(E, pid, V, escolhe, alvo=None, blocos=2, ermo='mata'):
    """uma saída inteira do robô, da ida à volta. Anota em V o que houve. Devolve True se ele saiu ferido (ferida nova, ou deixado por morto) ou morto."""
    p = E['gente'][pid]; f0 = len(p['feridas']); caiu = False; V['saidas'] += 1; ordem = ROBO['ordem'] if escolhe in CUIDAM else 'atacar'
    R = quieto(caca.sair, E, pid, ermo, alvo=alvo, blocos=blocos)
    for _ in range(200):
        if R['fase'] in ('fim', 'morto'): break
        if R['fase'] == 'encontro':
            enc = R['encontro']; V['encontros'] += 1; V['viu_bicho'] += enc['viu'] != 'caçador'; q = escolhe(E, pid, R)
            if enc['n'] > caca.bichos_de(E, ermo).get(enc['especie'], 0): V['mal'].append(f"apareceram {enc['n']} de {enc['especie']} e só havia {caca.bichos_de(E, ermo).get(enc['especie'], 0)}")
            if q[0] == 'atacar': R = quieto(caca.atacar, E, pid, inicio=q[1], vantagens=q[2])
            else: V[dict(deixar='deixou', recuar='recuou', fugir='fugiu')[q[0]]] += 1; R = quieto(caca.deixar if q[0] == 'deixar' else caca.fugir, E, pid)
        elif R['fase'] == 'luta':
            esp = R['encontro']['especie']; V['lutas'] += 1; V['forcadas'] += R['encontro'].get('surpresa') != 'B' and escolhe is not afoito
            R = _luta(E, pid, ordem); V['valor'] += base(R['bens']); V['carcacas'] += R['mortos'] if R['leva'] else 0; V['mortos_b'][esp] = V['mortos_b'].get(esp, 0) + R['mortos']
            V['fugiram_b'] += R['fugiram']; V['por_especie'][esp] = V['por_especie'].get(esp, 0) + 1; caiu = caiu or R['meu'] in ('caido', 'morto')
            for b, n in R['bens'].items(): V['bens'][b] = V['bens'].get(b, 0) + n
        elif escolhe in CUIDAM and _fraco(E, pid): R = quieto(caca.volta, E, pid)                    # cansado ou machucado, volta
        elif R.get('sangue'): V['sangue'] += 1; R = quieto(caca.sangue, E, pid); V['sangue_achou'] += R['fase'] == 'encontro'
        else: R = quieto(caca.volta if R.get('parou') and escolhe is not afoito else caca.segue, E, pid)
    else: raise RuntimeError('a saída não acaba')
    p = E['gente'][pid]; mal = p['estado'] != 'vivo' or len(p['feridas']) > f0 or caiu; V['feridas'] += mal
    if any(q < 0 for q in list(E['lugares'][ermo].get('bichos', {}).values()) + list(E['lugares'][ermo].get('coleta', {}).values())): V['mal'].append('contagem negativa')
    return mal


def um_passo(E, pid, V, escolhe, alvo, S):
    """um passo da vida do robô, conforme a hora: vende o que traz, come, e dorme (da noite à alvorada), ou manda consertar o que veste, ou sai para caçar
    (de manhã, uma vez por dia, pelos blocos que o corpo e o dia deixam), ou descansa. S guarda o dia da última saída."""
    b = E['relogio']['bloco']; _vende(E, pid, V); _come(E, pid, V)
    if b < 2: _dorme(E, pid, V, 2 - b)
    elif b == 5: _dorme(E, pid, V, 3)
    elif b in (2, 3) and S.get('dia') != E['relogio']['dia']:
        _come(E, pid, V, ate=2)
        if _conserta(E, pid, V): return                             # a manhã foi na forja: sai mais tarde, por menos blocos
        p = E['gente'][pid]; c = p['corpo']; S['dia'] = E['relogio']['dia']; ferido = bool(p['feridas']); cabem = M.BLOCOS_DIA - E['relogio']['bloco'] - 2 * caca.longe(E, 'mata')
        custo = lambda k: caca.longe(E, 'mata') * M.ESFORCO[K.ESFORCO['ida']] + k * M.ESFORCO[K.ESFORCO['procura']] + M.LUTA_CANSA * (k - 1)        # o cansaço com que ele chega ao último bloco
        if escolhe is afoito: n = min(2, cabem)
        elif (ferido and (escolhe is not veterano or any(f['grave'] for f in p['feridas']))) or p['pv'] < ROBO['pv'] * estado.pv_max(p): n = 0        # ferido ou machucado, não caça (o veterano só para por ferida grave)
        else: n = next((k for k in (2, 1) if k <= cabem and c['cansaco'] + custo(k) <= ROBO['cansado']), 0)
        if n: uma_saida(E, pid, V, escolhe, alvo=alvo, blocos=n)
        else:
            V['folgas'] += 1; V['repousos'] += ferido
            if p['moedas'] < ROBO['reserva'] and p['corpo']['cansaco'] + M.ESFORCO['pesado'] < M.LIMIARES['cansaco'][0]: ato.trabalhar(E, pid, 1); V['jornais'] += 1      # sem prata, pega um bloco de diária (um bloco pesado não tira o repouso do dia)
            ato.descansar(E, pid, M.BLOCOS_DIA - 1 - E['relogio']['bloco'])
    else: ato.descansar(E, pid, 1)
    E['turno']['dados'] = []; E['turno']['lutas'] = [l for l in E['turno']['lutas'] if not l['fim']]       # o caderno do turno de rascunho não cresce


def vida(semente, modo='prudente', dias=DIAS, **quem):
    """uma vida do robô caçador, do Dia 1 até `dias` (ou até morrer), num mundo de rascunho próprio. Devolve o que houve e as contas."""
    escolhe = dict(prudente=prudente, cauteloso=cauteloso, afoito=afoito)[modo]; V = caderno(); V['modo'] = modo
    with rascunho() as d:
        E = mundo(semente, **quem); pid = 'eu'; estado.grava(E); p0 = prata(E); f0 = foto(E); bolso0 = E['gente'][pid]['moedas']; S = {}
        while E['relogio']['dia'] <= dias and E['gente'][pid]['estado'] == 'vivo': um_passo(E, pid, V, escolhe, None if modo == 'afoito' else ROBO['alvo'], S)
        estado.grava(E); p = E['gente'][pid]; V['vivo'] = p['estado'] == 'vivo'; V['morreu'] = None if V['vivo'] else E['relogio']['dia']
        V['dias'] = dias if V['vivo'] else min(dias, E['relogio']['dia']); V['prata'] = prata(E) == p0; V['bolso'] = (bolso0, p['moedas']); V['quebrado'] = estado.valida(E)
        Z = razao(eventos(d)); V['conta'] = fecha(Z, f0, foto(E)); V['Z'] = Z; V['caca_fim'] = caca.bichos_de(E, 'mata'); V['mao'] = caca.mao(p); V['aberta'] = bool(caca.saida(p))
        V['de_fome'] = any(e['tipo'] == 'virada' and any(ef[:3] == ['pessoa', pid, 'estado'] for ef in e['efeitos']) for e in eventos(d))                   # morreu de fome em casa (não no ermo)
        V['no_chao'] = sum(1 for it in E['itens']['itens'].values() if it.get('onde') == 'mata'); V['vestido'] = sum(1 for it in E['itens']['itens'].values() if it.get('dono') == pid and it.get('uso'))
        if Z['despojo'] != V['bens'] or Z['sai'] != {e: n for e, n in V['mortos_b'].items() if n}: V['conta'].append('o registro de eventos não bate com o que o robô viu nas lutas')
    return V


# ---------- as provas do contrato ----------
def _o_cacador(P, Cc=()):
    """1. o caçador de nível 10 com peças Comuns tira por dia de 1,5 a 4 vezes a diária, e sai ferido ou morto em 2 a 12% das saídas"""
    n = len(P); dias = sum(V['dias'] for V in P); valor = sum(V['valor'] for V in P); saidas = sum(V['saidas'] for V in P); fer = sum(V['feridas'] for V in P); mortos = sum(not V['vivo'] for V in P)
    lutas = sum(V['lutas'] for V in P); carc = sum(V['carcacas'] for V in P); vezes = valor / dias / DIARIA; taxa = fer / max(1, saidas); venda = sum(V['prata_venda'] for V in P)
    por = sorted(V['valor'] / V['dias'] / DIARIA for V in P); soma = lambda k: sum(V[k] for V in P); vivos = [V for V in P if V['vivo']]
    bolso = sum(V['bolso'][1] - V['bolso'][0] for V in vivos) / max(1, sum(V['dias'] for V in vivos))
    a = (f"O CAÇADOR RENDE: nível 10, peças Comuns (arco, espada de reserva, cota e elmo de malha), no ermo de começo (a borda da floresta), tira por dia de {vz(RENDE[0], 1)} a {vz(RENDE[1], 1)} vezes a diária do diarista ({DIARIA} de prata: {M.JORNADA} blocos pagos), com o despojo ao preço de base",
         f"{n} vidas de até {DIAS} dias ({dias} dias vividos): {vz(valor / dias)} de prata por dia ao preço de base = {vz(vezes)} diárias (a vida do meio: {vz(por[len(por) // 2])}; a pior {vz(por[0])}, a melhor {vz(por[-1])}); "
         f"{vz(saidas / dias)} saída por dia, {vz(lutas / max(1, saidas))} luta por saída, {vz(carc / max(1, lutas))} carcaça por luta; seguiu o sangue {soma('sangue')} vezes e achou a presa em {soma('sangue_achou')}; "
         f"na loja (60% do preço do dia) isso deu {vz(venda / dias)} de prata por dia, e o conserto do que ele veste levou {vz(soma('prata_conserto') / dias)}. "
         f"NO BOLSO (a meta não mede isto; é o que o jogador sente): depois da cama, da comida e do conserto, os {len(vivos)} que chegaram vivos ficaram com {'+' if bolso >= 0 else '−'}{vz(abs(bolso))} de prata por dia (o diarista da jornada fica com +1,00)",
         RENDE[0] <= vezes <= RENDE[1])
    b = (f"O CAÇADOR SE FERE: o mesmo robô (que encurrala a presa sempre que o rastro lhe dá o cerco) sai ferido (ferida nova, ou deixado por morto) ou morto em {pc(FERE[0])} a {pc(FERE[1])} das saídas",
         f"{fer} de {saidas} saídas = {pc(taxa, 1)}; morreram {mortos} de {n} em {DIAS} dias ({pc(mortos / n)}); de {soma('encontros')} encontros, deixou {soma('deixou')}, recuou de {soma('recuou')} por estar cansado ou machucado, e fugiu de {soma('fugiu')}; "
         f"{soma('viu_bicho')} vezes o bicho o viu primeiro, e {soma('forcadas')} lutas ele não escolheu (o bicho investiu ou o alcançou)" + _compara(Cc), FERE[0] <= taxa <= FERE[1])
    return [a, b]


def _compara(Cc):
    """para comparar (não é meta): o CAUTELOSO, o mesmo robô sem encurralar o par nem a corça que ele não vê do alto"""
    if not Cc: return ''
    dias = sum(V['dias'] for V in Cc); sa = sum(V['saidas'] for V in Cc)
    return (f". PARA COMPARAR (não é meta), o cauteloso, que só encurrala a corça sozinha e do alto, em {len(Cc)} vidas: {vz(sum(V['valor'] for V in Cc) / dias / DIARIA)} diárias por dia, "
            f"ferido ou morto em {pc(sum(V['feridas'] for V in Cc) / max(1, sa), 1)} das saídas, e morreram {sum(not V['vivo'] for V in Cc)} de {len(Cc)}")


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
    res = []; quer = len(list(sementes)); caidos = 0
    for sem in range(1, 4 * quer + 1):
        if len(res) >= quer: break
        with rascunho():
            E = mundo(sem, prata=100, **VETERANO); pid = 'eu'; estado.grava(E); teto = caca.teto_de(E, 'mata')['corça']; r0 = caca.rastro_contra(E, 'mata', 'corça'); V = caderno(); S = {}
            while V['mortos_b'].get('corça', 0) < CACADOS and E['gente'][pid]['estado'] == 'vivo' and E['relogio']['dia'] < 200: um_passo(E, pid, V, veterano, 'corça', S); E['_novos'].clear()
            if V['mortos_b'].get('corça', 0) < CACADOS: caidos += 1; continue        # o veterano morreu (ou parou) antes das 60: o ermo mata. A medida segue noutro mundo
            d_caca = E['relogio']['dia']; fundo = caca.bichos_de(E, 'mata').get('corça', 0); r1 = caca.rastro_contra(E, 'mata', 'corça'); diz = K.fartura_diz(fundo, teto); dele = 0; dias = 0
            while caca.bichos_de(E, 'mata').get('corça', 0) < NOVE * teto and dele < 400: dias_sem_ninguem(E); dele += 1        # de onde o veterano a deixou (depende da pressa dele: a espécie cria enquanto ele caça)
            poe(E, corça=teto - CACADOS)                                                                                        # a medida da meta: do fundo que ela descreve, o teto menos os 60 caçados
            while caca.bichos_de(E, 'mata').get('corça', 0) < NOVE * teto and dias < 400: dias_sem_ninguem(E); dias += 1
            res.append(dict(mortos=V['mortos_b'].get('corça', 0), d_caca=d_caca, fundo=fundo, teto=teto, r0=r0, r1=r1, diz=diz, dias=dias, dele=dele, vivo=E['gente'][pid]['estado'] == 'vivo', mal=V['mal'], inteiro=not estado.valida(E)))
    certo = len(res) == quer and all(r['mortos'] >= CACADOS and r['fundo'] < r['teto'] * 0.75 and r['r1'] > r['r0'] and VOLTA[0] <= r['dias'] <= VOLTA[1] and not r['mal'] and r['inteiro'] for r in res)
    return (f"CAÇADA DEMAIS: caçar {CACADOS} bichos de uma espécie derruba a contagem, o rastro fica mais difícil, e ela leva de {VOLTA[0]} a {VOLTA[1]} dias para voltar a nove décimos do teto (a volta é medida do fundo que a meta descreve: o teto menos os {CACADOS})",
            f"{len(res)} mundos, um veterano (nível {VETERANO['nivel']}, conjunto {T.CATS[VETERANO['cat']]}) vivendo de caçar corça: " + ' · '.join(
                f"{r['mortos']} mortas em {r['d_caca'] - 1} dias, a contagem cai de {r['teto']} para {r['fundo']} (\"{r['diz']}\"; a espécie cria enquanto ele caça), o rastro vai de {r['r0']} para {r['r1']}; de onde ele a deixou, volta a {math.ceil(NOVE * r['teto'])} em {r['dele']} dias sem caça; "
                f"do fundo da meta ({r['teto'] - CACADOS} de {r['teto']}), em {r['dias']} dias" for r in res)
            + (f" (outros {caidos} veteranos morreram antes de fechar as {CACADOS}: a medida seguiu noutro mundo)" if caidos else ''), certo)


def _nunca_negativa(vidas):
    """4a. nenhuma contagem fica negativa (nas vidas dos robôs, e no ermo que se esvazia de verdade)"""
    with rascunho():
        E = mundo(3, fauna={'corça': 5}, prata=300, **VETERANO); pid = 'eu'; estado.grava(E); V = caderno(); blocos = 0; apos = 0; vistos = [5]
        def sai(n=1):
            nonlocal blocos, apos
            antes = caca.bichos_de(E, 'mata').get('corça', 0); enc0 = V['encontros']; uma_saida(E, pid, V, veterano, alvo='corça', blocos=n); blocos += n
            if antes == 0: apos += V['encontros'] - enc0
            noite(E, pid); vistos.append(caca.bichos_de(E, 'mata').get('corça', 0))
        while caca.bichos_de(E, 'mata').get('corça', 0) > 0 and blocos < 200: sai()
        vazio_em = blocos; caminho = list(vistos)
        for _ in range(8): poe(E, corça=0); sai(2)                   # o ermo vazio (o gerador segura a contagem em zero, contra o casal que vem de fora): ninguém aparece
        rec = recusa(lambda: estado.aplica(E, 'mestre', [['lugar', 'mata', 'bichos.corça', 'soma', -1]])); inteiro = not estado.valida(E)
        poe(E, corça=1); um = []
        for _ in range(12):                                         # com UMA corça no ermo, nunca aparecem duas
            poe(E, corça=1); R = quieto(caca.sair, E, pid, 'mata', alvo='corça', blocos=1)
            if R['fase'] == 'encontro': um.append(R['encontro']['n'])
            encerra(E, pid, R); noite(E, pid)
    neg = sum(bool(V_['mal']) for V_ in vidas)
    return ('NENHUMA CONTAGEM NEGATIVA: o que aparece sai da contagem real (um bicho, um bando, ou nada), nunca mais do que há; no ermo vazio não aparece ninguém, e o gravador recusa tirar o que não existe',
            f"nas {len(vidas)} vidas dos robôs: {neg} com contagem negativa ou bando maior que a contagem; um ermo de 5 corças caçado até o fim em {vazio_em} blocos de procura (a contagem, saída a saída: {', '.join(map(str, caminho))}): "
            f"morreram {V['mortos_b'].get('corça', 0)}; depois de vazio, {apos} encontros em 16 blocos; tirar mais uma por evento: {'recusado' if rec else 'ACEITO'}; com uma corça só, apareceu {len(um)} vezes, sempre {'sozinha' if set(um) <= {1} else 'EM BANDO: ' + str(um)}; estado {'inteiro' if inteiro else 'QUEBRADO'}",
            neg == 0 and not V['mal'] and V['mortos_b'].get('corça', 0) == 5 and apos == 0 and rec and inteiro and um and set(um) == {1})


def _o_nucleo():
    """4b. o núcleo de chefe entra no Livro de Itens com `de` e `onde`"""
    txt = []; ok = False; forte = dict(nivel=100, cat=5, kit='espada', mao=6, atributos={'Vontade': 100, 'Percepção': 90})
    for sem in range(1, 9):
        with rascunho() as d:
            E = mundo(sem, habitat='serra', perigo=3, fauna={'serpe': 1}, prata=300, **forte); pid = 'eu'; cacador(E, 'bera', nome='Bera', **forte); estado.grava(E); livro0 = len(E['itens']['itens'])
            R = ate_encontrar(E, pid, alvo='serpe', blocos=2, com=['bera'])
            if not R: txt.append(f'semente {sem}: a serpe não apareceu'); continue
            ameaca = 'É chefe' in R['texto'] and 'núcleo' in R['texto']; inis, nv, _ = caca.posicao(R['encontro']); R = quieto(caca.atacar, E, pid, inicio=inis[-1], vantagens=['cobertura'][:nv])
            junto = [x.get('id') for x in cenario(R)['A']] == ['eu', 'bera']; R = _luta(E, pid)
            if R['fim'] != 'A': txt.append(f"semente {sem}: a casa não ficou com o campo ({R['fim']})"); continue
            estado.grava(E); E = estado.carrega(); nuc = [it for it in E['itens']['itens'].values() if it['tipo'] == 'nucleo']; evs = [e for e in eventos(d) if e['tipo'] == 'despojo']
            it = nuc[0] if nuc else {}; p = E['gente'][pid]
            ok = (len(nuc) == 1 and it.get('de') == 'serpe' and it.get('cat') == TB.ESPECIES['serpe']['cat'] and 'onde' in it and it.get('dono') == R['leva'] == pid and it.get('onde') is None and len(it.get('historia', [])) == 1
                  and 'Mata de Prova' in it['historia'][0] and caca.bichos_de(E, 'mata').get('serpe', 0) == 0 and len(evs) == 1 and any(ef[:2] == ['item', 'nasce'] for ef in evs[0]['efeitos']) and not estado.valida(E)
                  and len(E['itens']['itens']) == livro0 + 1 and p.get('marca', {}).get('feito_caça') == 3 and ameaca and junto and R['ids_nucleos'] == [it.get('id')] and not razao(eventos(d))['mal'])
            # a outra ponta: a carcaça que ninguém ficou para abrir. As contas, com o desfecho da luta POSTO À MÃO no arquivo (o chefe morto, a casa fora do campo): só para conferir este ramo
            encerra(E, pid); noite(E, pid); poe(E, serpe=1); chao = achou = False; R2 = ate_encontrar(E, pid, alvo='serpe', blocos=2)
            if R2:
                R2 = quieto(caca.atacar, E, pid); S = json.load(open(R2['luta'], encoding='utf-8'))
                for f in S['L']: f['estado'] = 'morto' if f['lado'] == 'B' else 'saiu'
                S['fim'] = 'B'; S['posto_a_mao'] = True; json.dump(S, open(R2['luta'], 'w', encoding='utf-8'), ensure_ascii=False); A2 = quieto(caca.acerta, E, pid)
                n2 = [x for x in E['itens']['itens'].values() if x['tipo'] == 'nucleo' and x.get('onde') == 'mata']
                chao = len(n2) == 1 and n2[0]['dono'] is None and n2[0]['de'] == 'serpe' and A2['leva'] is None and not A2['bens'] and A2['mortos'] == 1 and caca.bichos_de(E, 'mata').get('serpe', 0) == 0 and not estado.valida(E) and A2['fase'] == 'fim'
                for _ in range(40):                                 # e quem volta lá e passa num rastro acha o núcleo no chão
                    noite(E, pid); Rv = quieto(caca.sair, E, pid, 'mata', alvo='serpe', blocos=2); encerra(E, pid, Rv)
                    meus = [x for x in E['itens']['itens'].values() if x['tipo'] == 'nucleo' and x['de'] == 'serpe' and x.get('dono') == pid]
                    if len(meus) == 2: achou = all(x.get('onde') is None for x in meus) and 'ACHADO' in Rv['texto'] and not estado.valida(E); break
            txt.append(f"semente {sem}: o Aldric e a Bera (nível 100, aço Lendário) matam a serpe em {R['rodadas']} rodada(s); o núcleo ({T.CATS[it.get('cat', 0)]}) entra no Livro por um evento `despojo`: de = {it.get('de')}, dono = {it.get('dono')}, onde = {it.get('onde')}, "
                       f"história: \"{(it.get('historia') or ['?'])[0]}\"; a serpe sai da contagem (0 de 1); a ameaça lida antes avisava do chefe e do núcleo: {sn(ameaca)}; a Bera entrou na luta ao lado dele: {sn(junto)}. "
                       f"A outra ponta (o desfecho posto à mão: o chefe morto, a casa fora do campo): o núcleo nasce no ermo, sem dono, com onde = mata: {sn(chao)}; quem volta e passa num rastro o acha: {sn(achou)}")
            ok = ok and chao and achou; break
    return ('O NÚCLEO DO CHEFE entra no Livro de Itens com `de` (a espécie) e `onde`: com dono, na mão de quem ficou com o campo (e aí `onde` fica vazio: peça com dono não está largada); ou no ermo, sem dono, se ninguém ficou para abrir a carcaça',
            ' · '.join(txt), ok)


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
        E = mundo(5, prata=300, mao=4, atributos={'Percepção': 90}); pid = 'eu'; estado.grava(E); certo = True; vistos = 0; c0 = caca.bichos_de(E, 'mata'); sobrevive = volta_rec = None; feitos = []
        for o_que in ('deixar', 'fugir'):
            R = ate_encontrar(E, pid, quer=lambda R: R['encontro']['viu'] == 'caçador')
            if not R: break
            enc = R['encontro']; vistos += 1; arma, armadura = caca._veste(E, pid); s = caca.saida(E['gente'][pid])
            certo = certo and bichos.ameaca(enc['especie'], n=enc['n'], arma=arma, armadura=armadura) in R['texto'] and 'VOCÊ VIU PRIMEIRO' in R['texto'] and 'ESCOLHA' in R['texto'] and s['fase'] == 'encontro' and not E['turno']['lutas']
            estado.grava(E); E = estado.carrega(); sobrevive = caca.saida(E['gente'][pid]) == s                     # a saída aberta sobrevive a fechar e abrir o estado
            volta_rec = recusa(lambda: caca.volta(E, pid)); R = quieto(getattr(caca, o_que), E, pid); feitos.append(o_que)
            certo = certo and R['fase'] == 'fim' and caca.bichos_de(E, 'mata') == c0 and (o_que == 'deixar' or 'recua sem ser visto' in R['texto']); noite(E, pid)
        estado.grava(E); lutas = [e for e in eventos(d) if e['tipo'] == 'luta']; p = E['gente'][pid]; limpo = not lutas and not E['turno']['lutas'] and not caca.saida(p) and p['pv'] == estado.pv_max(p)
    return ('A AMEAÇA É LIDA ANTES: quando o bicho aparece a saída PARA; o caçador lê a frase do bichos.ameaca (com a conta do que ele veste) e o que a posição dá, e escolhe. Deixar e fugir do bicho que não o viu não custam nada',
            f"{vistos} encontros de quem viu primeiro: a frase da ameaça estava inteira no que ele leu, e não havia luta aberta: {sn(certo)}; a saída aberta sobrevive a fechar e abrir o estado: {sn(sobrevive)}; "
            f"voltar com o bicho à frente: {'recusado (é atacar, deixar ou fugir)' if volta_rec else 'ACEITO'}; deixou uma vez e fugiu outra: nenhuma luta, nenhum evento de luta, a contagem igual, o PV inteiro: {sn(limpo)}",
            certo and feitos == ['deixar', 'fugir'] and sobrevive and bool(volta_rec) and limpo)


def _o_que_viu(n):
    """o bicho que viu o caçador: investe em quem o deixa, vem atrás de quem corre, e quem é alcançado luta colado e surpreendido"""
    k = max(30, n // 6); T_ = dict(deixar=dict(n=0, luta=0, certo=0), fugir=dict(n=0, luta=0, certo=0, teste=0, passou=0)); inv = K.indole('lobo'); mal = 0
    for i in range(2 * k):
        o_que = 'deixar' if i % 2 == 0 else 'fugir'
        with rascunho():
            E = mundo(100 + i, fauna={'lobo': 2000}, prata=50, atributos={'Percepção': 1}); pid = 'eu'; estado.grava(E)      # um ermo coalhado de lobos e um caçador que não vê rastro: o acaso vem logo
            R = ate_encontrar(E, pid, quer=lambda R: R['encontro']['viu'] == 'bicho', blocos=6, vezes=12)
            if not R: mal += 1; continue
            lido = 'APARECE, E VIU VOCÊ' in R['texto'] and bichos.ameaca('lobo', n=R['encontro']['n'], arma=0, armadura=0) in R['texto']; nd = len(E['turno']['dados']); quantos = R['encontro']['n']
            R = quieto(getattr(caca, o_que), E, pid); t = T_[o_que]; t['n'] += 1; rol = E['turno']['dados'][nd:]; s = caca.saida(E['gente'][pid])
            if s and s['fase'] == 'luta':
                cen = json.load(open(caca._arq(s).replace('_luta.json', '_cenario.json'), encoding='utf-8')); t['luta'] += 1; quer = (K.INICIO_ACASO, None) if o_que == 'deixar' else (K.INICIO_ALCANCADO, 'A')
                t['certo'] += lido and (cen['inicio'], cen['surpresa']) == quer and not cen['lugar'] and len(cen['B']) == quantos and len(E['turno']['lutas']) == 1 and (o_que == 'deixar' or (len(rol) == 1 and not rol[0]['passou']))
            else: t['certo'] += lido and not E['turno']['lutas'] and (not s if o_que == 'fugir' else True) and (o_que == 'deixar' or not rol or rol[0]['passou'])
            if o_que == 'fugir' and rol and rol[0]['atributo'] == 'Agilidade': t['teste'] += 1; t['passou'] += rol[0]['passou']; t['contra'] = rol[0]['contra']
    d, f = T_['deixar'], T_['fugir']; vem = min(1.0, inv[1] + K.INVESTE_FUGA)
    folga = lambda medido, p, m: abs(medido - p) <= 4 * math.sqrt(p * (1 - p) / max(1, m)) + 0.02
    return ('O BICHO QUE VIU O CAÇADOR (o acaso): em quem o deixa, investe pela índole da espécie, e a luta começa perto, sem surpresa; atrás de quem corre, vem mais vezes, e aí é Agilidade contra a dele: '
            'quem passa escapa; quem falha luta colado e surpreendido',
            f"lobos que viram o caçador de começo: deixados {d['n']} vezes, investiram em {pc(d['luta'] / max(1, d['n']))} (a índole: {pc(inv[1])}); de {f['n']} fugas, vieram atrás em {pc(f['teste'] / max(1, f['n']))} (a tabela: {pc(vem)}), "
            f"e de {f['teste']} testes de Agilidade contra {f.get('contra', '?')} ele passou em {f['passou']}: alcançado {f['luta']} vezes; cada desfecho com o começo, a surpresa e o teste certos: {d['certo'] + f['certo']} de {d['n'] + f['n']}",
            mal <= 2 and d['n'] >= k - 2 and d['certo'] == d['n'] and f['certo'] == f['n'] and f['luta'] == f['teste'] - f['passou'] and folga(d['luta'] / max(1, d['n']), inv[1], d['n']) and folga(f['teste'] / max(1, f['n']), vem, f['n']))


def _a_luta_do_ato(n):
    """a luta é a do ato.py luta: no arquivo, com paradas e ordens; volta ao estado por um evento só; com ela aberta o turno não fecha"""
    with rascunho() as d:
        E = mundo(7, prata=300, mao=4, atributos={'Percepção': 90}); pid = 'eu'; estado.grava(E); R = ate_encontrar(E, pid, quer=lambda R: R['encontro']['viu'] == 'caçador')
        enc = R['encontro']; inis, nv, _ = caca.posicao(enc); c0 = caca.bichos_de(E, 'mata')['corça']; r1 = recusa(lambda: caca.atacar(E, pid, inicio='de cima'))
        r2 = recusa(lambda: caca.atacar(E, pid, vantagens=['alto', 'cerco', 'estreito'])); R = quieto(caca.atacar, E, pid, inicio='perto', vantagens=['cerco'][:nv]); arq = R['luta']; estado.grava(E)
        S = json.load(open(arq, encoding='utf-8')); cen = cenario(R)
        aberta = (E['turno']['lutas'] == [dict(arq=estado.arq_guarda(arq), fim=None)] and not os.path.isabs(estado.arq_guarda(arq)) and S['mundo'] and S['paradas'] == ['a luta vai começar'] and S['surpresa'] == 'B' and cen['A'] == [dict(id='eu', controla=True)]
                  and len(cen['B']) == enc['n'] and all(x['bicho']['especie'] == 'corça' for x in cen['B']) and S['L'][0]['id'] == 'eu' and S['L'][0]['controla'] and 'RODADA 0' in R['texto'])
        turno.pergunta(E, 'a', ['a=x', 'b=y']); turno.pergunta(E, 'b', ['a=x', 'b=y']); r3 = recusa(lambda: turno.fecha(E, 'caçou')); r4 = recusa(lambda: caca.segue(E, pid)); r5 = recusa(lambda: caca.luta_roda(E, pid, ['Aldric: voar']))
        paradas = 0
        for _ in range(200):                                        # a luta roda pelo ato.py, direto, como o Mestre faria: até o FIM
            E = estado.carrega(); S = json.load(open(arq, encoding='utf-8'))
            if S['fim']: break
            quieto(ato.luta_roda, E, arq, ['Aldric: atacar'] if S['L'][0]['estado'] == 'pe' else []); estado.grava(E); paradas += 1
        E = estado.carrega(); p = E['gente'][pid]; f = S['L'][0]; antes = caca.saida(p)['fase']; quieto(caca.volta if p['estado'] == 'vivo' else caca.acerta, E, pid); estado.grava(E); evs = eventos(d); p = E['gente'][pid]
        nl = [e for e in evs if e['tipo'] == 'luta']; nd = [e for e in evs if e['tipo'] == 'despojo']; mortos = sum(x['estado'] in ('morto', 'caido') for x in S['L'][1:]) if S['fim'] == 'A' else sum(x['estado'] == 'morto' for x in S['L'][1:])
        volta = (len(nl) == 1 and len(nd) == (1 if mortos else 0) and (p['estado'] == 'morto') == (f['estado'] == 'morto') and (p['estado'] == 'morto' or p['pv'] <= max(1, f['pv'])) and len(p['feridas']) == len(f['feridas'])
                 and caca.bichos_de(E, 'mata').get('corça', 0) == c0 - mortos and antes == 'luta' and E['turno']['lutas'][0]['fim'] == S['fim'] and not estado.valida(E) and not caca.saida(p))
    return ('A LUTA É A DO `ato.py luta`: o caca.py só monta o cenário (a casa com ficha no mundo; os bichos, tirados da contagem) e chama o ato.luta_nova; a luta para e pede ordem, roda pelo `ato.py luta roda`, '
            'e volta ao estado por um evento `luta`; só depois vêm as contas (um evento `despojo`). Com a luta aberta o turno não fecha e a saída não segue',
            f"a luta abriu no arquivo, registrada no turno, parada antes da 1ª rodada, com o caçador comandado e {enc['n']} corça(s) surpreendida(s): {sn(aberta)}; começar de onde a posição não dá: {'recusado' if r1 else 'ACEITO'}; "
            f"três vantagens: {'recusado' if r2 else 'ACEITO'}; fechar o turno com ela aberta: {'recusado' if r3 else 'ACEITO'}; seguir a procura com ela aberta: {'recusado' if r4 else 'ACEITO'}; ordem que não existe: {'recusada' if r5 else 'ACEITA'}; "
            f"rodada pelo ato.py em {paradas} parada(s) até o fim ({S['fim']}, {S['r']} rodadas); eventos de luta: {len(nl)}; de despojo: {len(nd)} ({mortos} corça(s) a menos na contagem); PV e feridas do estado iguais aos da luta: {sn(volta)}",
            aberta and bool(r1 and r2 and r3 and r4 and r5) and volta and paradas >= 1)


def _a_presa_ferida(n):
    """a presa que fugiu ferida deixa sangue: quem a segue na hora acha o mesmo bicho, com o PV e as feridas com que fugiu, sem gastar bloco"""
    seguidos = achados = iguais = sem_tempo = numero = 0; esfria = larga = None; mesma_conta = True
    for sem in range(1, 40):
        if seguidos >= max(8, n // 30) and esfria is not None and larga is not None: break
        with rascunho():
            E = mundo(200 + sem, prata=300, mao=2); pid = 'eu'; estado.grava(E)
            for _ in range(12):
                R = ate_encontrar(E, pid, quer=lambda R: R['encontro']['viu'] == 'caçador' and R['encontro']['n'] == 1, blocos=2, vezes=6)
                if not R: break
                c0 = caca.bichos_de(E, 'mata')['corça']; R = quieto(caca.atacar, E, pid, inicio='longe', vantagens=['alto'][:caca.posicao(R['encontro'])[1]]); R = _luta(E, pid); vez = 0
                while R['fase'] == 'procura' and R.get('sangue'):
                    s = caca.saida(E['gente'][pid]); sg = s['sangue']; mesma_conta = mesma_conta and caca.bichos_de(E, 'mata')['corça'] == c0        # o que fugiu segue na contagem
                    if larga is None and vez == 0 and seguidos >= 2:                                                                              # uma vez, em vez de seguir o sangue, segue a procura: a presa fica largada
                        R = quieto(caca.segue, E, pid); s2 = caca.saida(E['gente'][pid]); larga = not (s2 or {}).get('sangue') and bool(recusa(lambda: caca.sangue(E, pid))) if s2 and s2['fase'] != 'luta' else not (s2 or {}).get('sangue'); break
                    t0 = estado.agora(E); contra = caca.sangue_contra(E, 'mata', sg); quer = caca.rastro_contra(E, 'mata', 'corça') - K.SANGUE + K.SANGUE_ESFRIA * vez
                    R = quieto(caca.sangue, E, pid); seguidos += 1; numero += contra == quer == E['turno']['dados'][-1]['contra']; sem_tempo += estado.agora(E) == t0
                    if vez == 1: esfria = contra == caca.rastro_contra(E, 'mata', 'corça') - K.SANGUE + K.SANGUE_ESFRIA
                    if R['fase'] != 'encontro': break
                    achados += 1; R = quieto(caca.atacar, E, pid, inicio='longe', vantagens=['alto'][:caca.posicao(R['encontro'])[1]]); S = json.load(open(R['luta'], encoding='utf-8')); b = [f for f in S['L'] if f['lado'] == 'B']
                    iguais += len(b) == len(sg['feridos']) and all(f['pv'] == fd['pv'] and f['feridas'][:f['feridas_antes']] == fd['feridas'] and f['pv'] < f['pvmax'] for f, fd in zip(b, sg['feridos']))
                    R = _luta(E, pid); vez += 1; c0 = caca.bichos_de(E, 'mata')['corça'] if R['fase'] == 'procura' else c0
                encerra(E, pid, R)
                if E['gente'][pid]['estado'] != 'vivo' or caca.saida(E['gente'][pid]): break
                noite(E, pid)
    return ('A PRESA FERIDA: o bicho que foge com ferida aberta deixa sangue; quem ficou com o campo pode segui-lo na hora, sem gastar bloco, com o rastro mais fácil; quem passa acha o MESMO bicho, com o PV e as feridas '
            'com que fugiu; cada nova perseguição no mesmo bloco é mais difícil; quem segue a procura larga a presa; e o que fugiu segue na contagem',
            f"{seguidos} rastros de sangue seguidos: o número era o do rastro menos {K.SANGUE} (mais {K.SANGUE_ESFRIA} por perseguição já feita) em {numero}; o relógio não andou em {sem_tempo}; a presa foi achada em {achados}, e em {iguais} entrou na luta com o PV e as feridas "
            f"com que tinha fugido; a segunda perseguição no mesmo bloco pediu {K.SANGUE_ESFRIA} a mais: {'sim' if esfria else 'não aconteceu' if esfria is None else 'NÃO'}; quem seguiu a procura perdeu o sangue: {'sim' if larga else 'não aconteceu' if larga is None else 'NÃO'}; "
            f"a corça que fugiu seguiu na contagem: {sn(mesma_conta)}",
            seguidos >= 5 and numero == seguidos and sem_tempo == seguidos and achados >= 3 and iguais == achados and esfria is not False and larga is not False and mesma_conta)


def _quem_morre(n):
    """quem morre no ermo fica lá com TUDO o que era dele (a regra da morte, do estado.py): as peças vestidas e as guardadas e o núcleo caem soltos ali, a carga e a prata
    ficam no chão; quem passa num rastro ali acha tudo. Nada sai do mundo sem evento."""
    for sem in range(1, 12):
        with rascunho():
            E = mundo(300 + sem, fauna={'lobo': 12}, prata=250); pid = 'eu'; cacador(E, 'bera', nome='Bera', nivel=100, cat=5, kit='espada', mao=6, atributos={'Vontade': 100, 'Percepção': 90})
            estado.aplica(E, 'gera', [['item', 'nasce', item('arma', 2, 'Lança guardada de prova', familia='lança', dono=pid)], ['item', 'nasce', item('nucleo', 3, 'Núcleo de prova', de='serpe', dono=pid)],
                                      ['pessoa', pid, 'carga.couro:2', 'soma', 4], ['pessoa', pid, 'carga.comida', 'soma', 6]], texto='o que o caçador leva, para a prova'); estado.grava(E)
            dele = sorted(i for i, it in E['itens']['itens'].items() if it.get('dono') == pid); vestia = [i for i in dele if E['itens']['itens'][i].get('uso')]; V = caderno(); p0 = prata(E)
            for _ in range(20):
                if E['gente'][pid]['estado'] != 'vivo': break
                levava = (E['gente'][pid]['moedas'], dict(E['gente'][pid].get('carga', {})))
                uma_saida(E, pid, V, afoito, alvo='lobo', blocos=2)
                if E['gente'][pid]['estado'] == 'vivo': noite(E, pid)
            if E['gente'][pid]['estado'] == 'vivo': continue
            L = E['itens']['itens']; m = E['gente'][pid]; chao = E['lugares']['mata']['estoque']
            ficou = all(L[i].get('dono') is None and L[i].get('onde') == 'mata' and L[i].get('solto') and not L[i].get('uso') and 'ficou com o corpo' in L[i]['historia'][-1] for i in dele)
            nada = m['moedas'] == 0 and not m.get('carga') and m.get('morte', {}).get('onde') == 'mata' and chao.get('prata', 0) == levava[0] and all(chao.get(b, 0) >= q for b, q in levava[1].items())
            inteiro = not estado.valida(E); fechada = not caca.saida(E['gente'][pid]); poe(E, lobo=0); achou = False; em = None; b0 = E['gente']['bera']['moedas']
            for k in range(20):                                     # a Bera vai lá (os lobos saíram): passando num rastro, acha o que ficou com o corpo
                R = quieto(caca.sair, E, 'bera', 'mata', alvo='lobo', blocos=1); encerra(E, 'bera', R)
                if all(L2.get('dono') == 'bera' for L2 in (E['itens']['itens'][i] for i in dele)):
                    achou = ('ACHADO junto de um corpo' in R['texto'] and 'ACHADO no chão' in R['texto'] and not estado.valida(E) and not any(E['lugares']['mata']['estoque'].values())
                             and E['gente']['bera'].get('carga', {}).get('couro:2', 0) == 4 and E['gente']['bera']['moedas'] >= b0 + levava[0] - 2 * (k + 1) * (M.CAMA_PRECO + 4 * M.REFEICAO_PRECO)); em = k + 1; break
                noite(E, 'bera'); poe(E, lobo=0)
            return ('QUEM MORRE NO ERMO fica lá com tudo o que era dele: as peças (as vestidas, as guardadas e o núcleo) seguem no Livro de Itens, sem dono, SOLTAS, com `onde` no ermo; a carga e a prata ficam no chão (o estoque do ermo); o morto não fica com nada; quem passa num rastro ali acha tudo',
                    f"o caçador de começo atacou os lobos e morreu na saída {V['saidas']}; as {len(dele)} peças dele ({len(vestia)} vestidas, uma lança guardada e um núcleo) ficaram no ermo, soltas, com a história escrita: {sn(ficou)}; "
                    f"a carga e os {levava[0]} de prata ficaram no chão, e o morto sem nada: {sn(nada)}; a saída dele fechou: {sn(fechada)}; estado {'inteiro' if inteiro else 'QUEBRADO'}; "
                    f"a Bera achou as peças, a carga e a prata na saída {em}: {sn(achou)}; a prata do mundo fecha: {sn(prata(E) == p0)}", ficou and nada and inteiro and fechada and achou and prata(E) == p0)
    return ('QUEM MORRE NO ERMO fica lá com tudo o que era dele', 'em 11 mundos o caçador de começo não morreu atacando lobos: a prova não chegou a medir', False)


def _a_virada(n):
    """a virada: os bichos criam devagar até o teto; a espécie caçada até o fim some por muito tempo; o chefe demora a nascer; a matéria volta devagar"""
    volta = []; some = []; teto_ok = True
    for s in range(1, 1 + max(8, n // 30)):
        E = mundo(s, pop=0); poe(E, corça=20); d = 0
        while caca.bichos_de(E, 'mata').get('corça', 0) < NOVE * 80 and d < 600: dias_sem_ninguem(E); d += 1
        volta.append(d)
        for _ in range(120): dias_sem_ninguem(E, 1); teto_ok = teto_ok and all(q <= caca.teto_de(E, 'mata')[e] for e, q in caca.bichos_de(E, 'mata').items())
        E = mundo(s, pop=0); poe(E, corça=0); d = 0; zero = None
        while caca.bichos_de(E, 'mata').get('corça', 0) < NOVE * 80 and d < 3000:
            dias_sem_ninguem(E); d += 1
            if zero is None and caca.bichos_de(E, 'mata').get('corça', 0) > 0: zero = d
        some.append((zero, d))
    chefe = []
    for s in range(1, 1 + max(30, n // 5)):
        E = mundo(s, pop=0, habitat='serra', perigo=3, fauna={'serpe': 1}); poe(E, serpe=0); d = 0
        while not caca.bichos_de(E, 'mata').get('serpe') and d < 3000: dias_sem_ninguem(E); d += 1
        chefe.append(d)
    E = mundo(1, pop=0, habitat='serra', perigo=2); estado.aplica(E, 'gera', [['lugar', 'mata', 'coleta.metal:0', 'poe', 0], ['lugar', 'mata', 'coleta.metal:2', 'poe', 0]], texto='a mina esgotada'); dias_sem_ninguem(E, 30)
    m30 = caca.coleta_de(E, 'mata'); t = caca.coleta_teto(E, 'mata'); dias_sem_ninguem(E, 600); m630 = caca.coleta_de(E, 'mata'); mat_ok = all(m630.get(b, 0) <= t[b] for b in t)
    def roda(sem):
        E = mundo(sem, pop=0); poe(E, corça=10, javali=5, lobo=2); dias_sem_ninguem(E, 200); return retrato(E)
    mesmo = roda(9) == roda(9) and roda(9) != roda(10)
    meio = lambda v: sorted(v)[len(v) // 2]; media = sum(chefe) / len(chefe); espera = K.CHEFE_NASCE[3]; esgota = [x[1] for x in some]; zeros = [x[0] for x in some if x[0] is not None]
    certo = (all(VOLTA[0] <= d <= VOLTA[1] for d in volta) and teto_ok and len(zeros) == len(some) and meio(esgota) > VOLTA[1] and min(esgota) > max(volta) and 0.6 * espera <= media <= 1.5 * espera and mat_ok and mesmo
             and 0 < m30.get('metal:0', 0) < t['metal:0'] and m30.get('metal:2', 0) <= 2)
    return ('A VIRADA: os bichos criam devagar e nunca passam do teto; de 20 em 80, a corça volta a nove décimos entre 30 e 120 dias; caçada até o fim, some por muito tempo (espera o casal que vem de fora); '
            'o chefe demora a nascer; a matéria volta devagar; mesma semente, mesmo ermo',
            f"{len(volta)} mundos sem ninguém: de 20 para 72 corças em {min(volta)} a {max(volta)} dias (a do meio: {meio(volta)}); nunca acima do teto: {sn(teto_ok)}; de ZERO, a primeira corça volta depois de {min(zeros)} a {max(zeros)} dias, "
            f"e as 72 depois de {min(esgota)} a {max(esgota)} (a do meio: {meio(esgota)}); a serpe morta nasce de novo, em média, em {media:.0f} dias ({len(chefe)} mundos; a tabela: {espera}); "
            f"a mina esgotada (minério Comum, teto {t['metal:0']:g}) tem {m30.get('metal:0', 0):g} depois de 30 dias e {m630.get('metal:0', 0):g} depois de 630; o minério Raro (teto {t['metal:2']:g}), {m30.get('metal:2', 0):g} e {m630.get('metal:2', 0):g}; "
            f"mesma semente, mesmo ermo depois de 200 dias, e outra semente, outro: {sn(mesmo)}", certo)


def _a_coleta(n):
    """a coleta: um teste por bloco; o que se tira sai do ermo e entra na carga no mesmo evento; rareando, fica mais difícil; o que acabou, acabou"""
    with rascunho() as d:
        E = mundo(11, habitat='serra', perigo=2, fauna={}, prata=300, nivel=30, kit='espada'); pid = 'eu'; estado.grava(E); c_cheio = caca.coleta_contra(E, 'mata', 'metal:0'); saidas = 0; p0 = prata(E)
        estado.aplica(E, 'gera', [['lugar', 'mata', 'coleta.metal:1', 'poe', 3]], onde='mata', texto='um veio curto'); f0 = foto(E); c1 = caca.coleta_contra(E, 'mata', 'metal:1')
        def um_dia(bem, blocos=2):
            nonlocal saidas
            R = quieto(caca.coletar, E, pid, bem, 'mata', blocos=blocos); saidas += 1; R = encerra(E, pid, R); noite(E, pid); return R
        for _ in range(12): um_dia('metal:0')
        ferro = E['gente'][pid]['carga'].get('metal:0', 0)
        for _ in range(30):
            if caca.coleta_de(E, 'mata').get('metal:1', 0) <= 0: break
            um_dia('metal:1')
        veio = caca.coleta_de(E, 'mata').get('metal:1', 0); antes = E['gente'][pid]['carga'].get('metal:1', 0)
        estado.aplica(E, 'gera', [['lugar', 'mata', 'coleta.metal:1', 'poe', 0]], onde='mata', texto='o veio acabou (a prova segura o que voltou na virada)'); R = um_dia('metal:1', 1); esgotou = 'esgotou' in R['texto'] and E['gente'][pid]['carga'].get('metal:1', 0) == antes
        r1 = recusa(lambda: caca.coletar(E, pid, 'erva:0', 'mata')); r2 = recusa(lambda: caca.coletar(E, pid, 'comida', 'mata')); r3 = recusa(lambda: estado.aplica(E, 'mestre', [['lugar', 'mata', 'coleta.metal:1', 'soma', -1]]))
        estado.grava(E); Z = razao(eventos(d)); f1 = foto(E); p = E['gente'][pid]; tr = p.get('treino', {}).get('coleta', 0); fecha_prata = prata(E) == p0
        mal = [x for x in fecha(Z, f0, f1) if 'metal:1: o ermo' not in x]                                          # (o veio que a prova zerou à mão não entra na conta do ermo)
        estado.aplica(E, 'gera', [['lugar', 'mata', 'coleta.metal:0', 'poe', 30]], onde='mata', texto='a mina rareia'); c_ralo = caca.coleta_contra(E, 'mata', 'metal:0')
        certo = not mal and ferro > 0 and Z['tirado'].get('metal:0', 0) == ferro and veio == 0 and esgotou and r1 and r2 and r3 and c_ralo > c_cheio and c1 > c_cheio and tr >= 24 and not estado.valida(E) and fecha_prata
    return ('A COLETA: um teste por bloco (Força ou Percepção, mais a maestria de coleta) contra a fartura da matéria; o que se tira sai do `coleta` do ermo e entra na carga no mesmo evento; rareando, fica mais difícil; o que acabou, acabou',
            f"um mineiro de nível 30 na serra, {saidas} saídas: tirou {ferro} de minério Comum em 24 blocos (saíram do ermo {Z['tirado'].get('metal:0', 0)}); o veio de 3 de minério Incomum foi até {veio} e depois \"esgotou\": {sn(esgotou)}; "
            f"o número: {c_cheio} com a mina cheia, {c_ralo} com um quinto dela, {c1} no veio Incomum; erva que a serra não dá: {'recusado' if r1 else 'ACEITO'}; \"comida\": {'recusado' if r2 else 'ACEITO'}; tirar do ermo o que não há: {'recusado' if r3 else 'ACEITO'}; "
            f"{tr} blocos de treino de coleta; a conta {'fecha' if not mal else 'NÃO FECHA: ' + mal[0]}; a prata do mundo {'fecha' if fecha_prata else 'NÃO FECHA'}", bool(certo))


def _a_maestria(n):
    """a maestria de caça sobe por blocos de procura; de Mestre para cima pede o feito (a carcaça de um bicho Raro, Épico)"""
    E = mundo(1, pop=0); pid = 'eu'; da = lambda k: estado.aplica(E, 'mestre', [['pessoa', pid, 'treino.caça', 'soma', k]], texto='blocos de prova'); mao = lambda: caca.mao(E['gente'][pid])
    da(K.CACA_BLOCOS[2] - 1); caca.sobe(E, pid); a = mao(); da(1); caca.sobe(E, pid); b = mao(); da(560); t = caca.sobe(E, pid); c = mao()
    estado.aplica(E, 'mestre', [['pessoa', pid, 'marca.feito_caça', 'poe', 2]], texto='a carcaça de uma pantera'); caca.sobe(E, pid); dd = mao(); da(1000); caca.sobe(E, pid); e = mao()
    estado.aplica(E, 'mestre', [['pessoa', pid, 'marca.feito_caça', 'poe', 3]], texto='a carcaça de uma serpe'); caca.sobe(E, pid); f = mao(); nome = lambda x: T.MAESTRIAS[x]
    return ('A MAESTRIA DE CAÇA sobe por blocos de procura e soma no rastro; de Mestre para cima, os blocos não bastam: pede o feito (ficar com a carcaça de um bicho Raro; para Lendário, Épico)',
            f"com {K.CACA_BLOCOS[2] - 1} blocos: {nome(a)}; com {K.CACA_BLOCOS[2]}: {nome(b)}; com 600 e nenhum feito: {nome(c)}{t}; depois da carcaça Rara: {nome(dd)}; com 1.600 blocos: {nome(e)}; depois da carcaça Épica: {nome(f)}",
            (a, b, c, dd, e, f) == (0, 2, 4, 6, 6, 8) and 'falta o feito' in t)


def _o_robo_vive(P):
    """o robô vive de verdade: come, dorme, paga a cama, vende o despojo, conserta o que veste; a prata do mundo fecha"""
    n = len(P); dias = sum(V['dias'] for V in P); soma = lambda k: sum(V[k] for V in P); ref = soma('refeicoes'); camas = soma('camas')
    bolso = sorted(V['bolso'][1] for V in P if V['vivo']); pr = all(V['prata'] for V in P); qb = sum(bool(V['quebrado']) for V in P); ab = soma('aberta'); mortos = [V for V in P if not V['vivo']]
    corpo_ok = all(V['no_chao'] >= 1 and V['vestido'] == 0 for V in mortos if not V['de_fome']) and all(V['no_chao'] == 0 for V in P if V['vivo']); fome = sum(V['de_fome'] for V in P)
    return ('O ROBÔ VIVE DE VERDADE: come e paga, dorme na cama e paga, vende o despojo na loja da vila, manda consertar o que veste, e vive disso; a prata do mundo fecha e o estado fica inteiro (o morto fica no ermo, com tudo o que era dele)',
            f"{n} vidas do caçador, {dias} dias: {vz(ref / dias)} refeição e {vz(camas / dias)} cama pagas por dia; {soma('consertos')} consertos pagos ({soma('prata_conserto')} de prata; {soma('sem_conserto')} vezes sem prata para o conserto); noites no chão: {soma('chao')}; "
            f"vezes com fome sem comer: {soma('jejum')}; mortos de fome: {fome}; dias de folga: {soma('folgas')} ({soma('repousos')} de repouso de ferida; em {soma('jornais')} pegou um bloco de diária, por falta de prata); " + (f"os vivos acabam com {bolso[0]} a {bolso[-1]} de prata (a do meio: {bolso[len(bolso) // 2]}; começaram com 30); " if bolso else '')
            + f"vendas recusadas pela loja: {soma('nao_vendeu')}; a prata do mundo {'fecha em todas' if pr else 'NÃO FECHA'}; estados quebrados: {qb}; saídas largadas abertas: {ab}; os {len(mortos)} mortos ficaram no ermo, sem nada vestido e com as peças soltas no chão: {sn(corpo_ok)}",
            pr and qb == 0 and fome == 0 and ab == 0 and corpo_ok and 0.8 <= ref / dias <= 1.2 and camas / dias >= 0.85)


def _as_recusas(n):
    """o que não pode, não começa; e nada muda pela metade"""
    with rascunho():
        E = mundo(2, prata=50); pid = 'eu'; cacador(E, 'bera', nome='Bera'); E['lugares']['longe'] = dict(nome='o Fim do Mundo', tipo='ermo', estoque={}); estado.grava(E); antes = retrato(E)
        casos = [('ermo que não é vizinho', lambda: caca.sair(E, pid, 'longe')), ('ermo que não existe', lambda: caca.sair(E, pid, 'lua')), ('espécie que não existe', lambda: caca.sair(E, pid, 'mata', alvo='unicórnio')),
                 ('zero blocos', lambda: caca.sair(E, pid, 'mata', blocos=0)), ('sete blocos', lambda: caca.sair(E, pid, 'mata', blocos=7)), ('companheiro que não existe', lambda: caca.sair(E, pid, 'mata', com=['ninguém'])),
                 ('ir consigo mesmo', lambda: caca.sair(E, pid, 'mata', com=['eu'])), ('atacar sem bicho à frente', lambda: caca.atacar(E, pid)), ('deixar sem bicho à frente', lambda: caca.deixar(E, pid)),
                 ('fugir sem bicho à frente', lambda: caca.fugir(E, pid)), ('voltar sem ter saído', lambda: caca.volta(E, pid)), ('seguir sem ter saído', lambda: caca.segue(E, pid)), ('seguir sangue que não há', lambda: caca.sangue(E, pid)),
                 ('luta sem luta', lambda: caca.luta_roda(E, pid, ['Aldric: atacar'])), ('coletar o que não é matéria', lambda: caca.coletar(E, pid, 'prata')), ('coletar o que a mata não dá', lambda: caca.coletar(E, pid, 'metal:0')),
                 ('povoar por cima', lambda: caca.povoa(E, 'mata', 'brejo')), ('povoar lugar que não existe', lambda: caca.povoa(E, 'lua', 'brejo')), ('habitat que não existe', lambda: caca.povoa(E, 'longe', 'deserto')),
                 ('pessoa que não existe', lambda: caca.sair(E, 'fantasma'))]
        rec = [nome for nome, f in casos if recusa(f)]; intacto = antes == retrato(E)
        R = ate_encontrar(E, pid, quer=lambda R: R['encontro']['viu'] == 'caçador'); aberta = None
        if R: aberta = bool(recusa(lambda: caca.sair(E, pid, 'mata'))) and bool(recusa(lambda: caca.coletar(E, pid, 'madeira:0'))); encerra(E, pid, R)
        estado.aplica(E, 'mestre', [['pessoa', pid, 'estado', 'poe', 'morto'], ['pessoa', pid, 'pv', 'soma', -999]], texto='morre, para a prova'); morto = recusa(lambda: caca.sair(E, pid, 'mata'))
        with contextlib.redirect_stdout(io.StringIO()) as o: caca.main([])
        uso = o.getvalue().strip() == caca.__doc__.strip()
        S = PM.vila(); a0 = retrato(S); sem = recusa(lambda: caca.sair(S, 'eu')); caca.virada(S); nada = a0 == retrato(S) and caca.mesa(S) == []
    return ('AS RECUSAS: o que não pode não começa, e nada muda pela metade; sem argumento, o script só diz o uso; onde não há ermo, a caça não faz nada',
            f"{len(rec)} de {len(casos)} recusados" + (f" (ACEITOS: {', '.join(nome for nome, _ in casos if nome not in rec)})" if len(rec) < len(casos) else '') + f"; estado {'intacto' if intacto else 'MUDOU'}; "
            f"sair com uma saída aberta: {'recusado' if aberta else 'não houve saída aberta para tentar' if aberta is None else 'ACEITO'}; morto não caça: {'recusado' if morto else 'ACEITO'}; sem argumento: {'só o uso' if uso else 'FEZ OUTRA COISA'}; "
            f"na vila da etapa 1 (sem ermo vizinho): sair é recusado, a virada não gera evento e a mesa fica calada: {sn(sem and nada)}", len(rec) == len(casos) and intacto and aberta is not False and bool(morto) and uso and bool(sem) and nada)


def _a_mesa(n):
    """as linhas da caça para a MESA.md: o que se sabe em palavras, a contagem só para o Mestre, sem os chefes, e curta"""
    with rascunho():
        E = mundo(1, habitat='serra', perigo=3); pid = 'eu'; poe(E, lobo=5, urso=0); estado.grava(E); L = caca.mesa(E); txt = '\n'.join(L); pub = '\n'.join(x for x in L if 'SÓ O MESTRE' not in x); mestre = '\n'.join(x for x in L if 'SÓ O MESTRE' in x)
        chefes = [d['nome'] for d in TB.ESPECIES.values() if d['chefe']]
        certo = ('a Mata de Prova' in pub and 'lobo (há, mas rareou)' in pub and 'urso (sumiu)' in pub and not any(c in pub for c in chefes) and 'lobo 5/12' in mestre and 'serpe 1/1' in mestre and 'metal Comum (há fartura)' in pub and 'caca.py sair' in pub)
        R = quieto(caca.sair, E, pid, 'mata', alvo='lobo', blocos=1); aberta = caca.saida(E['gente'][pid]); avisa = (not aberta) or 'SAÍDA ABERTA' in '\n'.join(caca.mesa(E)); encerra(E, pid, R)
        s = caca.saida(E['gente'][pid])
        if s and s['fase'] == 'luta': avisa = avisa and 'EM LUTA' in '\n'.join(caca.mesa(E))
        E2 = mundo(1); estado.grava(E2); inteira = turno.mesa(E2); da_caca = len('\n'.join(caca.mesa(E2)).encode())
    return ('A MESA: as linhas da caça dizem o que todo mundo sabe (a fartura, em palavras), sem os chefes; a contagem vai numa linha marcada SÓ O MESTRE; a saída aberta aparece; e cabe no teto da MESA.md',
            f"as linhas da caça e dos bichos na serra de prova: {len(txt.encode())} bytes ({len(L)} linhas); na vila de prova com mercado, forja e a mata ao lado, a MESA inteira tem {len(inteira.encode())} bytes (o teto são 8.000), {da_caca} da caça; "
            f"fartura em palavras, chefes só na linha do Mestre, a saída aberta avisada: {sn(certo and avisa)}", certo and avisa and len(txt.encode()) <= 3000 and len(inteira.encode()) <= 8000)


# ---------- as provas da integração (o que os revisores acharam, e foi consertado) ----------
def _ate_a_luta(E, pid, alvo, com=(), vezes=30):
    """sai até dar com o bicho, e ataca. Devolve True se a luta abriu."""
    for _ in range(vezes):
        quieto(caca.sair, E, pid, 'mata', alvo=alvo, blocos=6, com=com)
        for _ in range(20):
            s = caca.saida(E['gente'][pid])
            if not s or E['gente'][pid]['estado'] != 'vivo': break
            if s['fase'] == 'encontro': quieto(caca.atacar if s['encontro']['especie'] == alvo else caca.fugir, E, pid)
            elif s['fase'] == 'luta': return True
            else: quieto(caca.volta, E, pid)
        if E['gente'][pid]['estado'] != 'vivo' or any(E['gente'][c]['estado'] != 'vivo' for c in com): return False
        for q in [pid] + list(com): noite(E, q)
    return False


def _luta_pelo_ato(E, pid):
    """roda a luta aberta da saída até o fim PELO `ato.py luta roda` (o caminho que o capítulo deixa aberto): as contas da caça ficam por fazer"""
    nome = E['gente'][pid]['nome']; arq = caca._arq(caca.saida(E['gente'][pid]))
    for _ in range(400):
        S = json.load(open(arq, encoding='utf-8'))
        if S['fim']: return S
        try: quieto(ato.luta_roda, E, arq, [f'{nome}: atacar'])
        except SystemExit: quieto(ato.luta_roda, E, arq, [])
    raise RuntimeError('a luta não acaba')


def _as_contas_do_morto(n):
    """a luta acabada pelo `ato.py luta roda`, com quem comandava MORTO: o comando seguinte da caça (`volta` ou `luta`) faz as mesmas contas (o chefe sai da contagem, o núcleo nasce)"""
    for sem in range(1, 120):
        with rascunho():
            E = mundo(sem, prata=100, habitat='serra', perigo=3, fauna={'serpe': 1}); cacador(E, 'bera', nivel=200, cat=5, kit='espada', nome='Bera', atributos={'Vontade': 120}); estado.grava(E)
            if not _ate_a_luta(E, 'eu', 'serpe', com=['bera']): continue
            S = _luta_pelo_ato(E, 'eu'); serpe = next(f for f in S['L'] if f['lado'] == 'B')
            if E['gente']['eu']['estado'] != 'morto' or S['fim'] != 'A' or serpe['estado'] not in ('morto', 'caido'): continue
            antes = estado.valida(E); E2 = {k: copy.deepcopy(v) for k, v in E.items()}; lido = {}
            quieto(caca.volta, E, 'eu'); quieto(caca.luta_roda, E2, 'eu', [])
            for nome, W in (('volta', E), ('luta', E2)):
                nuc = [it for it in W['itens']['itens'].values() if it['tipo'] == 'nucleo']
                lido[nome] = dict(serpes=caca.bichos_de(W, 'mata').get('serpe', 0), nucleo=bool(nuc) and nuc[0].get('dono') == 'bera' and nuc[0].get('de') == 'serpe', carga=dict(W['gente']['bera'].get('carga', {})),
                                  fechada=not caca.saida(W['gente']['eu']) and not caca.vai_com(W['gente']['bera']), inteiro=not estado.valida(W))
            igual = retrato(dict(E, turno={})) == retrato(dict(E2, turno={})); v = lido['volta']
            certo = igual and v['serpes'] == 0 and v['nucleo'] and v['carga'].get('couro:2', 0) >= 3 and v['fechada'] and v['inteiro'] and any('saída aberta' in x for x in antes)
            return ('AS CONTAS DO LÍDER MORTO: a luta de caça acabada pelo `ato.py luta roda`, com quem comandava morto, fecha com as MESMAS contas pelo `caca.py volta` e pelo `caca.py luta` (o chefe sai da contagem, o núcleo entra no Livro, o despojo vai para quem ficou com o campo)',
                    f"semente {sem}: o caçador de começo morreu, a companheira matou a serpe ({S['r']} rodadas); antes das contas, o estado acusa o morto com a saída aberta: {sn(any('saída aberta' in x for x in antes))}; "
                    f"pelo `volta`: serpes {v['serpes']}, núcleo Épico com a companheira: {sn(v['nucleo'])}, na carga dela {caca._lista(v['carga'])}, a saída fechada e a companheira solta: {sn(v['fechada'])}, estado {'inteiro' if v['inteiro'] else 'QUEBRADO'}; "
                    f"pelo `luta`: o mesmo mundo, peça por peça: {sn(igual)}", certo)
    return ('AS CONTAS DO LÍDER MORTO', 'em 119 mundos o caso não saiu (o líder morto e a serpe morta pela companheira): a prova não chegou a medir', False)


def _fora_e_fora(n):
    """com a saída aberta, a pessoa está no ermo: os atos da vila são recusados (para quem comanda e para quem foi junto); o corpo de quem vai junto passa os mesmos blocos;
    o que o bicho que viu o caçador vai fazer fica decidido quando ele aparece (passar o relógio não rola de novo); o sangue esfria se o relógio anda"""
    with rascunho():
        E = mundo(11, fauna={'lobo': 2000}, prata=60, atributos={'Percepção': 1}); cacador(E, 'bera', nome='Bera'); cacador(E, 'caio', nome='Caio'); estado.aplica(E, 'gera', [['pessoa', 'eu', 'carga.comida', 'soma', 2]], texto='a merenda'); estado.grava(E)
        R = ate_encontrar(E, 'eu', quer=lambda R: R['encontro']['viu'] == 'bicho', alvo='lobo', blocos=6, vezes=12, com=['bera']); enc = (caca.saida(E['gente']['eu']) or {}).get('encontro') or {}
        if not R or enc.get('viu') != 'bicho': return ('FORA É FORA', 'o encontro de prova não saiu (um lobo que viu o caçador): a prova não chegou a medir', False)
        E['turno']['dados'] = []
        antes = retrato(E); casos = []
        for q in ('eu', 'bera'):
            casos += [(f'{q}: dormir na pousada', lambda q=q: ato.dormir(E, q, 2)), (f'{q}: trabalhar', lambda q=q: ato.trabalhar(E, q, 1)), (f'{q}: comer na taverna', lambda q=q: ato.comer(E, q) if q == 'bera' else ato.esperar(E, q, 1)),
                      (f'{q}: treinar', lambda q=q: ato.treinar(E, q, 1, 'espada')), (f'{q}: vender na loja', lambda q=q: mercado.vender_cesta(E, q)), (f'{q}: comprar', lambda q=q: mercado.comprar(E, q, 'comida', 1)),
                      (f'{q}: servir na forja', lambda q=q: oficio.jornal(E, q, 1)), (f'{q}: mandar consertar', lambda q=q: oficio.consertar(E, q, next(i for i, it in E['itens']['itens'].items() if it.get('dono') == q), pago=True))]
        casos += [('a companheira abre saída própria', lambda: caca.sair(E, 'bera', 'mata')), ('outro caçador leva a mesma companheira', lambda: caca.sair(E, 'caio', 'mata', com=['bera'])), ('a companheira decide a saída do outro', lambda: caca.volta(E, 'bera'))]
        rec = [nome for nome, f in casos if recusa(f)]; igual = antes == retrato(E)
        come = recusa(lambda: ato.comer(E, 'eu')) is None and E['gente']['eu']['carga'].get('comida') == 1                       # no ermo, só da própria carga (e sem pagar)
        guardado = isinstance(enc.get('investe'), bool) and isinstance(enc.get('persegue'), bool)
        E2 = {k: copy.deepcopy(v) for k, v in E.items()}; quieto(ato.esperar, E2, 'caio', 2)                                    # o relógio do mundo anda (outro age na vila): o que o lobo vai fazer não muda
        A = quieto(caca.deixar, E, 'eu'); B = quieto(caca.deixar, E2, 'eu'); mesmo = (A['fase'] == 'luta') == (B['fase'] == 'luta') == bool(enc['investe'])
    with rascunho():
        E = mundo(12, fauna={'corça': 80}, prata=60); cacador(E, 'bera', nome='Bera'); estado.grava(E); c0 = dict(E['gente']['bera']['corpo'])
        R = quieto(caca.sair, E, 'eu', 'mata', alvo='corça', blocos=2, com=['bera']); marcada = caca.vai_com(E['gente']['bera']) == 'eu' and estado.fora(E, 'bera') == 'mata'; encerra(E, 'eu', R)
        e, b = E['gente']['eu']['corpo'], E['gente']['bera']['corpo']; junto = b['sono'] == e['sono'] > c0['sono'] and b['cansaco'] == e['cansaco'] and not caca.vai_com(E['gente']['bera']) and not estado.fora(E, 'bera') and not estado.valida(E)
    with rascunho():                                                                                                             # o sangue é agora ou nunca
        E = mundo(13, fauna={'corça': 80}, prata=60); cacador(E, 'caio', nome='Caio'); estado.grava(E); s = None
        quieto(caca.sair, E, 'eu', 'mata', alvo='corça', blocos=6); s = dict(caca.saida(E['gente']['eu']), fase='procura', encontro=None, sangue=dict(especie='corça', feridos=[dict(pv=20, feridas=[['pernas', False]])], vezes=0, escuro=False, quando=estado.agora(E)))
        estado.aplica(E, 'mestre', [['pessoa', 'eu', 'marca.caca', 'poe', s]], texto='uma corça fugiu ferida (posta à mão, para a prova)'); quieto(ato.esperar, E, 'caio', 1); nd = len(E['turno']['dados'])
        R = quieto(caca.sangue, E, 'eu'); esfriou = 'esfriou' in R['texto'] and len(E['turno']['dados']) == nd and not caca.saida(E['gente']['eu']).get('sangue')
    return ('FORA É FORA: com a saída aberta, quem comanda e quem foi junto estão no ermo, e os atos da vila são recusados sem mudar nada; o corpo de quem vai junto passa os mesmos blocos; '
            'o que o bicho que viu o caçador fará fica decidido quando ele aparece; o sangue esfria se o relógio anda',
            f"com dois lobos à frente: {len(rec)} de {len(casos)} atos da vila e da saída alheia recusados" + ('' if len(rec) == len(casos) else f" (passaram: {', '.join(x for x, _ in casos if x not in rec)})") + f"; estado {'intacto' if igual else 'MUDOU'}; "
            f"comer da própria carga, sem pagar: {sn(come)}; o investir e o perseguir guardados no encontro: {sn(guardado)}; com o relógio do mundo dois blocos adiante, o lobo faz o mesmo: {sn(mesmo)}; "
            f"a companheira marcada na saída e solta na volta, com o mesmo sono e o mesmo cansaço de quem comandava: {sn(marcada and junto)}; o sangue seguido depois de o relógio andar: {'esfriou, sem rolar dado' if esfriou else 'FOI ACEITO'}",
            len(rec) == len(casos) and igual and come and guardado and mesmo and marcada and junto and esfriou)


def _a_loja_nao_e_achado(n):
    """num lugar que tem loja E bichos, quem passa num rastro só acha o que está SOLTO (o que alguém largou): a prateleira é da loja"""
    with rascunho():
        E = mundo(21, fauna={'corça': 80}, prata=30, mao=8, atributos={'Percepção': 150}); mercado.funda(E, 'mata', 120)                    # um posto com loja no meio do campo de caça
        estado.aplica(E, 'gera', [['item', 'nasce', item('arma', 0, 'Adaga largada de prova', familia='adaga', onde='mata', solto=True)]], texto='alguém largou uma adaga no mato'); estado.grava(E)
        largada = f"i{E['itens']['seq']:04d}"; loja0 = len(mercado.prateleira(E, 'mata')); meus0 = sum(1 for it in E['itens']['itens'].values() if it.get('dono') == 'eu'); p0 = prata(E); rastros = 0
        for _ in range(6):
            R = quieto(caca.sair, E, 'eu', 'mata', alvo='corça', blocos=2); rastros += R['texto'].count('PASSA'); encerra(E, 'eu', R); noite(E, 'eu')
        loja1 = len(mercado.prateleira(E, 'mata')); meus1 = sum(1 for it in E['itens']['itens'].values() if it.get('dono') == 'eu'); achou = E['itens']['itens'][largada].get('dono') == 'eu'
        conta = quieto(caca.conta, E, 'mata'); no_chao = sum('no chão' in x for x in conta)
    return ('A LOJA NÃO É ACHADO: num lugar com loja e com bichos, quem passa num rastro só acha o que está SOLTO (o que alguém largou ali); a prateleira é da loja',
            f"um posto de 120 pessoas com mercado no campo de caça: {rastros} rastros achados em 6 saídas; a prateleira: {loja0} peças antes, {loja1} depois; as peças do caçador: {meus0} → {meus1} (a adaga largada: {'achada' if achou else 'NÃO ACHADA'}); "
            f"a contagem do Mestre lista {no_chao} coisa(s) no chão; a prata do mundo fecha: {sn(prata(E) == p0)}; estado {'inteiro' if not estado.valida(E) else 'QUEBRADO'}",
            rastros >= 1 and loja0 == loja1 >= 10 and meus1 == meus0 + 1 and achou and no_chao == 0 and prata(E) == p0 and not estado.valida(E))


def _a_pasta_muda(n):
    """o save guarda o caminho da luta RELATIVO à pasta dele: a pasta muda de lugar no meio da luta e a caçada segue; se o arquivo se perde, a recusa é uma frase, e o Mestre larga a saída"""
    d2 = tempfile.mkdtemp(prefix='m10_caca_muda_'); antes = os.environ.get('MOTOR10_MUNDO')
    try:
        with rascunho() as d:
            E = mundo(31, fauna={'corça': 80}, prata=60, mao=8, atributos={'Percepção': 150}); estado.grava(E)
            if not _ate_a_luta(E, 'eu', 'corça'): return ('A PASTA DO SAVE MUDA DE LUGAR', 'a luta de prova não abriu: a prova não chegou a medir', False)
            estado.grava(E); s = caca.saida(E['gente']['eu']); relativo = not os.path.isabs(s['luta']) and not os.path.isabs(E['turno']['lutas'][-1]['arq'])
            shutil.rmtree(d2); shutil.copytree(d, d2)
        os.environ['MOTOR10_MUNDO'] = d2; E = estado.carrega(); R = None
        for _ in range(200):
            R = quieto(caca.luta_roda, E, 'eu', ['Aldric: atacar'] if E['gente']['eu']['estado'] == 'vivo' else [])
            if R['fase'] != 'luta': break
        seguiu = R['fase'] != 'luta' and all(l['fim'] for l in E['turno']['lutas']) and not estado.valida(E)
        E = mundo(32, fauna={'corça': 80}, prata=60, mao=8, atributos={'Percepção': 150}); shutil.rmtree(d2); os.makedirs(d2); estado.grava(E)
        if not _ate_a_luta(E, 'eu', 'corça'): return ('A PASTA DO SAVE MUDA DE LUGAR', 'a segunda luta de prova não abriu: a prova não chegou a medir', False)
        estado.grava(E); os.remove(caca._arq(caca.saida(E['gente']['eu'])))
        frases = [recusa(lambda: caca.luta_roda(E, 'eu', [])), recusa(lambda: caca.volta(E, 'eu')), recusa(lambda: caca.segue(E, 'eu')), recusa(lambda: ato.luta_roda(E, caca._arq(caca.saida(E['gente']['eu'])), []))]
        turno.pergunta(E, 'a?', ['a=1', 'b=2']); turno.pergunta(E, 'b?', ['a=1', 'b=2']); preso = recusa(lambda: turno.fecha(E, 'tentando fechar'))
        quieto(caca.larga, E, 'eu', 'o arquivo da luta se perdeu'); solto = not caca.saida(E['gente']['eu']) and all(l['fim'] for l in E['turno']['lutas']) and not estado.valida(E)
        fechou = recusa(lambda: turno.fecha(E, 'a saída foi largada')) is None
    finally:
        if antes is None: os.environ.pop('MOTOR10_MUNDO', None)
        else: os.environ['MOTOR10_MUNDO'] = antes
        shutil.rmtree(d2, ignore_errors=True)
    return ('A PASTA DO SAVE MUDA DE LUGAR: o caminho da luta fica guardado relativo à pasta do save; movida a pasta no meio da luta, a caçada segue e fecha; se o arquivo se perde, a recusa é uma frase, e o Mestre larga a saída',
            f"caminho relativo na saída e no caderno do turno: {sn(relativo)}; a pasta copiada para outro lugar: a luta seguiu até o fim e voltou ao estado: {sn(seguiu)}; com o arquivo apagado: {sum(bool(x) for x in frases)} de {len(frases)} comandos recusados com frase "
            f"(sem erro de programa), o turno não fecha: {sn(bool(preso))}; `caca.py larga`: a saída e a luta soltas, o estado inteiro: {sn(solto)}; e o turno fecha: {sn(fechou)}",
            relativo and seguiu and all(frases) and bool(preso) and solto and fechou)


def provas(n=300):
    out = []; k = max(40, n // 4); P = []; A = []
    def roda(nome, f):
        try:
            r = f(); out.extend(r if isinstance(r, list) else [r])
        except (SystemExit, Exception) as e: out.append((nome, f'A PROVA QUEBROU: {type(e).__name__}: {e}', False))
    try: P = [vida(s, 'prudente') for s in range(1, k + 1)]
    except (SystemExit, Exception) as e: out.append(('AS VIDAS DO CAÇADOR (a medição)', f'A PROVA QUEBROU: {type(e).__name__}: {e}', False))
    try: A = [vida(1000 + s, 'afoito') for s in range(1, k + 1)]
    except (SystemExit, Exception) as e: out.append(('AS VIDAS DO AFOITO (a medição)', f'A PROVA QUEBROU: {type(e).__name__}: {e}', False))
    try: Cc = [vida(2000 + s, 'cauteloso') for s in range(1, k // 2 + 1)]
    except (SystemExit, Exception) as e: Cc = []; out.append(('AS VIDAS DO CAUTELOSO (a medição)', f'A PROVA QUEBROU: {type(e).__name__}: {e}', False))
    for nome, f in (('O CAÇADOR', lambda: _o_cacador(P, Cc)), ('O AFOITO', lambda: _o_afoito(A)), ('CAÇADA DEMAIS', lambda: _sessenta(range(1, 1 + max(3, n // 100)))), ('NENHUMA CONTAGEM NEGATIVA', lambda: _nunca_negativa(P + A)),
                    ('O NÚCLEO DO CHEFE', _o_nucleo), ('A CONTA FECHA', lambda: _a_conta(P, A)), ('A AMEAÇA É LIDA ANTES', lambda: _a_ameaca_antes(n)), ('O BICHO QUE VIU O CAÇADOR', lambda: _o_que_viu(n)),
                    ('A LUTA É A DO ato.py', lambda: _a_luta_do_ato(n)), ('A PRESA FERIDA', lambda: _a_presa_ferida(n)), ('QUEM MORRE NO ERMO', lambda: _quem_morre(n)), ('A VIRADA', lambda: _a_virada(n)),
                    ('A COLETA', lambda: _a_coleta(n)), ('A MAESTRIA DE CAÇA', lambda: _a_maestria(n)), ('O ROBÔ VIVE DE VERDADE', lambda: _o_robo_vive(P)), ('AS RECUSAS', lambda: _as_recusas(n)), ('A MESA', lambda: _a_mesa(n)),
                    ('AS CONTAS DO LÍDER MORTO', lambda: _as_contas_do_morto(n)), ('FORA É FORA', lambda: _fora_e_fora(n)), ('A LOJA NÃO É ACHADO', lambda: _a_loja_nao_e_achado(n)), ('A PASTA DO SAVE MUDA DE LUGAR', lambda: _a_pasta_muda(n))):
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
