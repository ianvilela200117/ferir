"""m4_descida.py: RASCUNHO do robô que desce a cripta de teste (a Cripta da Cova Velha) com o Maro de hoje e os companheiros da vila.
A luta é a do luta.py de verdade (o PV e as feridas passam de uma luta para a outra); o resto (a armadilha, a fechadura, o escondido, a luz, o que vagueia, o lance)
é a PROPOSTA do projeto A, escrita aqui à mão (ainda não há masmorra.py). Mede: quantas vidas limpam a cripta, em quantos dias, quantos morrem, as tochas, o que se leva.
Uso: python3 m4_descida.py [VIDAS] [quem]     quem: grupo (Maro, Tomé, Rute) · ladino (com o Quim na frente) · quatro (com Anselmo) · sozinho"""
import sys, random, copy
from med_comum import *
from pessoas import ficha

VIDAS = int(sys.argv[1]) if len(sys.argv) > 1 else 200
QUEM = sys.argv[2] if len(sys.argv) > 2 else 'grupo'
CAUTELA = 'cauto' in sys.argv[3:]
CORREDOR = 'corredor' in sys.argv[3:]
TOME = 'tome' in sys.argv[3:]
PRUDENTE = 'prudente' in sys.argv[3:]
SEMFASE = 'semfase' in sys.argv[3:]
ESPADA = 'espada' in sys.argv[3:]
GNV = int(next((x[3:] for x in sys.argv[3:] if x.startswith('nv=')), 25)); GMA = int(next((x[3:] for x in sys.argv[3:] if x.startswith('ma=')), 4)); GLAC = int(next((x[4:] for x in sys.argv[3:] if x.startswith('lac=')), 2))
ONDE_LUTA = ['?']
R = random.Random(5)
def d20x():
    t = [R.randint(1, 20)]
    while t[-1] == 20: t.append(R.randint(1, 20))
    return t
def d2(): return sum(d20x()) + sum(d20x())
def rola(dado, vezes=1): n, f = map(int, dado.split('d')); return sum(R.randint(1, f) for _ in range(n * vezes))

# ---------- a proposta (os números do tabelas_masmorra.py) ----------
LANCES_BLOCO = 12               # 1 lance = 20 minutos; 12 lances fecham um bloco (o ato.passa anda 1 bloco)
CUSTO = dict(anda=1, escondido=2, procurar=2, tenta=1, pegar=1, luta=1, contorna=1, volta=1)
VAGA = (0.17, 0.10)             # o que vagueia: a chance por bloco dentro (17%), mais 10% por ponto de alarme
ACHAR = (20, 6); PASSAGEM = -6; GAZUA = (24, 8); ESQUIVA = (20, 6)
ARMADILHAS = {'dardo': dict(dado='1d6', golpe='ponta', acerto=6), 'runa': dict(dado='1d8', golpe='magia', acerto=6)}

# ---------- a cripta de teste (a proposta da vila de teste) ----------
def cripta():
    return dict(
        r2=dict(larg=1, bichos=('corpo-seco', 2), estado='à toa', armadilha=dict(tipo='dardo', cat=0, onde='chão')),
        r3=dict(larg=None, bichos=('esqueleto', 3), estado='à toa', prata=10),
        r4=dict(larg=2, bichos=('ratazana', 4), estado='dormindo', bau=dict(fechadura=0, armadilha=dict(tipo='dardo', cat=0), prata=25, itens=['maça Comum', 'poção de cura Comum', 'a chave de ferro'])),
        r5=dict(larg=1, porta=dict(fechadura=1, chave='a chave de ferro', porta=1), armadilha=dict(tipo='runa', cat=0, onde='chão')),
        r6=dict(larg=2, chefe=True, bichos=('esqueleto', GLAC), estado='à toa', bau=dict(fechadura=0, armadilha=None, prata=30, itens=['o escudo do guardião (Incomum)']), segredo=1),
        r7=dict(larg=1, prata=15, itens=['a gazua Incomum']),
        vagantes=[('corpo-seco', 1), ('ratazana', 3)], alarme=0)
ROTA = ['r2', 'r3', 'r4', 'r5', 'r6']

def guardiao():
    g = CR.criatura('cavaleiro-da-cova', nome='o guardião da cripta', cat=0, nivel=GNV, maestria=GMA, **(dict(arma=('espada', 0), escudo=True) if ESPADA else {})); g.update(lider=True, chefe=True)
    if not SEMFASE: g['fases'] = [dict(abaixo=0.5, diz='bate o pé: os ossos da sala se levantam', ergue=2, brado=True)]
    return g

def quim():
    """o ladino da vila (proposta): nível 14, manha de Iniciante, adaga, couro, gazua Comum"""
    p = padrao('Quim', 14, molde='arqueiro', maestria={'adaga': 2}); veste(p, arma=('adaga', 0), armadura=('couro', 0), elmo=False)
    p['pv'] = T.pv_max(p['atributos']['Vigor'], 14); p['feridas'] = []; p['manha'] = 2; p['gazua'] = 0
    return p

def grupo():
    if QUEM == 'sozinho': G = [cheio('eu', controla=True)]
    else:
        G = [cheio('eu', controla=True), cheio('tome'), cheio('rute', linha='trás')]
        if QUEM == 'quatro': G.append(cheio('anselmo', linha='trás'))
        if QUEM == 'ladino': G.insert(0, quim())
    for g in G: g.setdefault('manha', 0); g.setdefault('gazua', None); g['cansaco'] = 0
    return G

def bonus(g, at): return g['atributos'][at] // 10
def armadura(g):
    tr = [a for a in (g['equip'].get('armaduras') or []) if 'tronco' in (a.get('cobre') or ['tronco', 'braços', 'pernas'])]
    return {'couro': 0, 'malha': -3, 'placa': -6}.get(tr[0]['material'] if tr else 'couro', 0)

def dispara(g, arm, cat):
    """a armadilha dispara em g: o golpe pela conta do aço (ou da magia, a runa). Devolve o dano."""
    F = ficha(g); a = ARMADILHAS[arm]
    d1, d2_ = d20x(), d20x(); tot = sum(d1) + sum(d2_) + a['acerto'] + T.BON[cat]; crit = max(d1[0], d2_[0]) == 20 and min(d1[0], d2_[0]) >= 11
    if (d1[0], d2_[0]) == (1, 1) or (tot < F['def_fixa'] and not crit): return 0
    if a['golpe'] == 'magia':
        tr = [x for x in F['partes'].values() if x.get('cat') is not None]; guarda = T.guarda(None, F['partes']['tronco']['cat'] if 'tronco' in F['partes'] else None)
        return int(rola(a['dado'], 2 if crit else 1) * T.K_DANO * T.MULT[cat] / (guarda / (2 if crit else 1)))
    parte = T.ONDE[R.randint(1, 10)]; pc = F['partes'].get(parte)
    prot = (pc['rd'] * T.MATRIZ[a['golpe']][pc['material']] / (2 if crit else 1)) if pc else T.NU
    return int(rola(a['dado'], 2 if crit else 1) * T.K_DANO * T.MULT[cat] / prot)

def fere(G, g, dano, conta):
    g['pv'] -= dano
    pvmax = ficha(g)['pvmax']
    if dano >= pvmax * T.FERIDA_GRAVE: g['feridas'].append(['tronco', True])
    elif dano >= pvmax * T.FERIDA: g['feridas'].append(['tronco', False])
    if g['pv'] <= 0:
        if dano > pvmax * T.FERIDA_GRAVE: conta['mortos'].append(g['nome']); G.remove(g)
        else: g['pv'] = 1; conta['caiu'] += 1

def luta_com(G, B, larg, tempo, surpresa, conta, inicio='perto'):
    """a luta de verdade: o PV e as feridas voltam ao grupo; quem morre sai"""
    A = [copy.deepcopy(g) for g in G]
    if QUEM == 'ladino': A = [a for a in A if a['nome'] != 'Quim'] + [dict(a, linha='trás') for a in A if a['nome'] == 'Quim']
    if TOME: A = [a for a in A if a['nome'] == 'Tomé'] + [a for a in A if a['nome'] != 'Tomé']
    for a, g in zip(A, G): a['pena'] = -2 if g['cansaco'] >= 9 else 0; a['fol_menos'] = g['cansaco'] // 3
    S = luta.nova(A, B, quieto=True, inicio=inicio, lugar=dict(largura=larg) if larg else {}, tempo=tempo, surpresa=surpresa)
    if CAUTELA:
        luta.corre(S, interativo=True); k = 0
        while not S['fim'] and k < 200:
            k += 1; eu = next((f for f in S['L'] if f['nome'] == 'Maro' and f['estado'] == 'pe'), None)
            if eu and eu['pv'] < 0.30 * eu['pvmax'] and luta.inimigos(S, eu): quieto(luta.ordem, S, 'Maro: recuar')
            elif eu: quieto(luta.ordem, S, 'Maro: atacar')
            if luta.corre(S, interativo=True) == 'fim': break
    else: luta.corre(S)
    for f in S['L']:
        if f['lado'] == 'A' and f['estado'] == 'morto': conta.setdefault('onde', {}); conta['onde'][ONDE_LUTA[0]] = conta['onde'].get(ONDE_LUTA[0], 0) + 1
    conta['lutas'] += 1; vivos = []
    for g in G:
        f = next(x for x in S['L'] if x['nome'] == g['nome'])
        if f['estado'] == 'morto': conta['mortos'].append(g['nome']); continue
        g['pv'] = max(1, f['pv']); g['feridas'] = [list(x) for x in f['feridas']]; g['cansaco'] += 2; vivos.append(g)
        if f['estado'] == 'caido': conta['caiu'] += 1
        if f['estado'] == 'saiu': g['saiu'] = True
    G[:] = vivos
    return S['fim'] == 'A'

def descida(C, G, tochas, conta):
    """uma descida: anda a rota até o chefe cair, ou alguém cair ou ficar abaixo de 35% do PV (aí volta pelas salas limpas). Devolve as tochas que sobraram."""
    lances = [0]; blocos = [0]; luz = [tochas > 0]
    def passa(n, escondido=False):
        lances[0] += n
        while lances[0] >= LANCES_BLOCO:
            lances[0] -= LANCES_BLOCO; blocos[0] += 1
            nonlocal_tochas[0] = max(0, nonlocal_tochas[0] - 1) if luz[0] else nonlocal_tochas[0]
            luz[0] = nonlocal_tochas[0] > 0
            for g in G: g['cansaco'] += 1
            if C['vagantes'] and R.random() < VAGA[0] + VAGA[1] * C['alarme']:
                esp, n_ = C['vagantes'].pop(0); conta['vagantes'] += 1
                ONDE_LUTA[0] = 'vagante'; luta_com(G, CR.bando(esp, n=n_) if esp != 'ratazana' else bichos.bando(esp, n=n_), 1, [] if luz[0] else ['escuro'], None, conta)
    nonlocal_tochas = [tochas]
    def ruim(): return not G or G[0]['nome'] != (G[0]['nome']) or any(g['pv'] < 0.35 * ficha(g)['pvmax'] for g in G) or conta['mortos']
    def frente(): return G[0]
    def tempo(): return [] if luz[0] else ['escuro']
    def sala(k):
        if not G: return False
        s = C[k]; conta['salas'].add(k)
        # a armadilha do chão: quem vai na frente olha onde pisa (de passagem: 6 mais difícil); o ladino procura (2 lances)
        a = s.get('armadilha')
        if a and not a.get('feita'):
            f = frente()
            if f['manha'] >= 2: passa(CUSTO['procurar']); achou = d2() + bonus(f, 'Percepção') + f['manha'] >= ACHAR[0] + ACHAR[1] * a['cat']
            else: achou = d2() + bonus(f, 'Percepção') + PASSAGEM >= ACHAR[0] + ACHAR[1] * a['cat']
            if achou and luz[0]: passa(CUSTO['contorna']); conta['achou'] += 1
            else: conta['disparou'] += 1; fere(G, f, dispara(f, a['tipo'], a['cat']), conta)
            a['feita'] = True
            if not G or ruim(): return False
        # a porta trancada: a chave, a gazua, ou a força
        pt = s.get('porta')
        if pt and not pt.get('aberta'):
            if pt.get('chave') in conta['itens']: pt['aberta'] = True
            else:
                for _ in range(6):
                    passa(CUSTO['tenta']); f = max(G, key=lambda g: (g['gazua'] is not None, bonus(g, 'Agilidade') + g['manha']))
                    if f['gazua'] is not None and d2() + bonus(f, 'Agilidade') + f['manha'] >= GAZUA[0] + GAZUA[1] * (pt['fechadura'] - f['gazua']): pt['aberta'] = True; break
                    if f['gazua'] is None:
                        fo = max(G, key=lambda g: bonus(g, 'Força')); C['alarme'] += 1
                        if d2() + bonus(fo, 'Força') >= GAZUA[0] + GAZUA[1] * (pt['porta'] + 1): pt['aberta'] = True; break
                if not pt.get('aberta'): return False
        # quem mora na sala
        if s.get('bichos') and not s.get('limpa'):
            esp, n = s['bichos']
            B = ([guardiao()] if s.get('chefe') else []) + (CR.bando(esp, n=n) if esp != 'ratazana' else bichos.bando(esp, n=n))
            alerta = C['alarme'] >= 2 and s['estado'] != 'dormindo'
            # o grupo não anda escondido (o robô): os de lá notam; se estão alertas, a frente testa a atenção (Percepção contra 20 + Agilidade ÷ 10 deles): falhou, o grupo é surpreendido
            surpresa = None
            if alerta and d2() + bonus(frente(), 'Percepção') + frente()['manha'] < 20 + 6: surpresa = 'A'
            if s['estado'] == 'dormindo' and luz[0] and d2() + min(bonus(g, 'Agilidade') + g['manha'] + armadura(g) for g in G) - 6 >= 20 + 5 - 6: surpresa = 'B'
            passa(CUSTO['luta']); C['alarme'] += 1; ONDE_LUTA[0] = k
            larg = 1 if (CORREDOR and k == 'r3') else s['larg']
            if not luta_com(G, B, larg, tempo(), surpresa, conta): return False
            s['limpa'] = True
            if s.get('chefe'): conta['chefe'] = True
            if ruim(): return 'volta'
        # o baú: a armadilha da fechadura e a fechadura (o ladino procura e desarma; o grupo sem gazua força o baú, e a armadilha dispara)
        b = s.get('bau')
        if b and not b.get('aberto'):
            a = b.get('armadilha'); f = max(G, key=lambda g: (g['gazua'] is not None, g['manha']))
            if a and f['manha'] >= 2 and f['gazua'] is not None:
                passa(CUSTO['procurar'])
                if d2() + bonus(f, 'Percepção') + f['manha'] >= ACHAR[0] + ACHAR[1] * a['cat']:
                    conta['achou'] += 1
                    while True:
                        passa(CUSTO['tenta']); r = d2() + bonus(f, 'Agilidade') + f['manha'] - (GAZUA[0] + GAZUA[1] * (a['cat'] - f['gazua']))
                        if r >= 0: a = None; break
                        if r <= -5: conta['disparou'] += 1; fere(G, f, dispara(f, a['tipo'], a['cat']), conta); a = None; break
            for _ in range(8):
                passa(CUSTO['tenta'])
                if a: conta['disparou'] += 1; fere(G, f, dispara(f, a['tipo'], a['cat']), conta); a = None
                if not G or f not in G: return 'volta'
                if f['gazua'] is not None: ok = d2() + bonus(f, 'Agilidade') + f['manha'] >= GAZUA[0] + GAZUA[1] * (b['fechadura'] - f['gazua'])
                else: fo = max(G, key=lambda g: bonus(g, 'Força')); C['alarme'] += 1; ok = d2() + bonus(fo, 'Força') >= GAZUA[0] + GAZUA[1] * (b['fechadura'] + 1)
                if ok: b['aberto'] = True; break
            if b.get('aberto'): passa(CUSTO['pegar']); conta['prata'] += b['prata']; conta['itens'] += b['itens']
        if s.get('prata') and not s.get('pego') and k != 'r7': passa(CUSTO['pegar']); s['pego'] = True; conta['prata'] += s['prata']
        if s.get('segredo') and not C.get('r7_achado'):
            f = max(G, key=lambda g: bonus(g, 'Percepção') + g['manha']); passa(CUSTO['procurar'])
            if luz[0] and d2() + bonus(f, 'Percepção') + f['manha'] >= ACHAR[0] + ACHAR[1] * s['segredo']:
                C['r7_achado'] = True; passa(CUSTO['anda'] + CUSTO['pegar']); conta['prata'] += C['r7']['prata']; conta['itens'] += C['r7']['itens']; conta['segredo'] = True
            C['segredo_tentou'] = True
        return True
    for k in ROTA:
        if PRUDENTE and k == 'r6' and not C['r6'].get('limpa') and any(g['pv'] < 0.75 * ficha(g)['pvmax'] for g in G): conta['recuou_chefe'] = conta.get('recuou_chefe', 0) + 1; break
        if C[k].get('limpa') and not C[k].get('porta') and not C[k].get('bau'): passa(CUSTO['anda']); continue
        passa(CUSTO['anda'])
        r = sala(k)
        if r is not True or not G: break
    volta = len(conta['salas']); passa(volta * CUSTO['volta'])
    if lances[0]: blocos[0] += 1; nonlocal_tochas[0] = max(0, nonlocal_tochas[0] - (1 if luz[0] else 0))     # sair arredonda o bloco que está aberto
    conta['blocos'] += blocos[0] + 2                                                                               # mais a ida e a volta até a Cova Velha (1 bloco cada)
    return nonlocal_tochas[0]

def vida():
    C = cripta(); G = grupo(); tochas = 6; dias = 0; conta = dict(lutas=0, mortos=[], caiu=0, prata=0, itens=[], salas=set(), achou=0, disparou=0, vagantes=0, chefe=False, segredo=False, blocos=0, descidas=0, tochas=0)
    pvmax = {g['nome']: ficha(g)['pvmax'] for g in G}
    while dias < 20 and not conta['chefe'] and 'Maro' not in conta['mortos']:
        dias += 1
        if all(g['pv'] >= 0.9 * pvmax[g['nome']] and not g['feridas'] for g in G):
            conta['descidas'] += 1; t0 = tochas; tochas = descida(C, G, tochas, conta); conta['tochas'] += t0 - tochas
            if tochas < 2: tochas += 4                                                                              # compra mais tochas (1 de prata cada)
        for g in G:                                                                                                 # a noite em casa: um décimo do PV; a ferida sara em 7 dias (aqui: um sétimo por dia)
            g['pv'] = min(pvmax[g['nome']], g['pv'] + pvmax[g['nome']] // 10); g['cansaco'] = 0
            if g['feridas'] and R.random() < 1 / 7: g['feridas'].pop()
    conta['dias'] = dias
    return conta

L = []
def p(x): L.append(x); print(x, flush=True)
luta.semente(3)
V = [vida() for _ in range(VIDAS)]
limpou = [v for v in V if v['chefe']]; morreu_maro = sum('Maro' in v['mortos'] for v in V); morreu_alguem = sum(bool(v['mortos']) for v in V)
p(f"== A CRIPTA DA COVA VELHA, {QUEM} {' '.join(sys.argv[3:])} ({VIDAS} vidas de até 20 dias; desce quando todos estão inteiros) ==")
p(f"limpa a cripta (o guardião cai) em {len(limpou) / VIDAS:.0%} das vidas" + (f", no dia {sorted(v['dias'] for v in limpou)[len(limpou) // 2]} (mediana), em {sum(v['descidas'] for v in limpou) / len(limpou):.1f} descidas" if limpou else ''))
p(f"Maro morre em {morreu_maro / VIDAS:.0%} das vidas; morre alguém do grupo em {morreu_alguem / VIDAS:.0%} ({sum(len(v['mortos']) for v in V)} mortos)")
ond = {}
for v in V:
    for k2, q in (v.get('onde') or {}).items(): ond[k2] = ond.get(k2, 0) + q
p('onde morrem (nas lutas): ' + ', '.join(f'{k2} {q}' for k2, q in sorted(ond.items())) + f" · quem morre: " + ', '.join(f"{n} {sum(x == n for v in V for x in v['mortos'])}" for n in sorted({x for v in V for x in v['mortos']})))
p(f"por vida: {sum(v['lutas'] for v in V) / VIDAS:.1f} lutas, {sum(v['vagantes'] for v in V) / VIDAS:.2f} com o que vagueia, armadilhas achadas {sum(v['achou'] for v in V) / VIDAS:.2f} e disparadas {sum(v['disparou'] for v in V) / VIDAS:.2f}, "
  f"{sum(v['blocos'] for v in V) / VIDAS:.1f} blocos de descida (com a ida e a volta), {sum(v['tochas'] for v in V) / VIDAS:.1f} tochas")
p(f"voltou antes do chefe para descansar: {sum(v.get('recuou_chefe', 0) for v in V) / VIDAS:.2f} vezes por vida")
if limpou: p(f"quem limpa leva: {sum(v['prata'] for v in limpou) / len(limpou):.0f} de prata em média (de {min(v['prata'] for v in limpou)} a {max(v['prata'] for v in limpou)}); acha o nicho escondido em {sum(v['segredo'] for v in limpou) / len(limpou):.0%}")
open(f'm4_saida_{QUEM}' + ('_cauto' if CAUTELA else '') + ('_corredor' if CORREDOR else '') + ('_tome' if TOME else '') + ('_prudente' if PRUDENTE else '') + ('_semfase' if SEMFASE else '') + ('_espada' if ESPADA else '') + f'_g{GNV}_{GMA}_{GLAC}' + '.txt', 'w').write('\n'.join(L) + '\n')
