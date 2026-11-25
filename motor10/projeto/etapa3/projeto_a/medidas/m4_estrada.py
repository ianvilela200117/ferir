#!/usr/bin/env python3
"""m4_estrada.py — MEDIDA (projeto A, etapa 3): o perigo da estrada contra o Maro de nível 5 (e o ferreiro do Dia 1), pelas lutas de verdade do luta.py.

Roda de dentro de motor10/:  PYTHONDONTWRITEBYTECODE=1 python3 projeto/etapa3/projeto_a/medidas/m4_estrada.py COPIA_DO_ENSAIO [lutas=400]
COPIA_DO_ENSAIO: uma CÓPIA do ensaio/ no rascunho (só é lida: o Maro, a Rute e o Tomé de hoje, com o que vestem).
1. As lutas do encontro: o que aparece na estrada (o bando dos bichos da Mata do Corvo; a patrulha goblin; os salteadores do povo), começando PERTO e sem surpresa
   (é o bicho que viu o viajante), e pegando-o desprevenido (COLADO e surpreendido: quem fugiu e foi alcançado, ou quem dormia no mato sem vigia).
   O Maro sozinho; o Maro com Tomé e Rute; o ferreiro do Dia 1 (a vila nova de ferreiro, nível 5, martelo e couro Comuns).
2. A conta da viagem: com a chance de encontro por bloco (a regra proposta no PROJETO.md, seção 3), quanto o Maro morre por viagem de N blocos, em cada tipo de rota.
"""
import json, os, random, sys
sys.path.insert(0, os.getcwd())
a = sys.argv[1:]
if not a: print(__doc__); sys.exit()
os.environ['MOTOR10_MUNDO'] = os.path.abspath(a[0]); op = dict(x.split('=', 1) for x in a[1:] if '=' in x); N = int(op.get('lutas', 400))
import estado, luta, bichos, criaturas, vila_teste, copy
from pessoas import padrao, veste
import tabelas_caca as K

E = estado.carrega()
MARO = estado.lutador(E, 'eu'); TOME = estado.lutador(E, 'tome'); RUTE = estado.lutador(E, 'rute')
for f in (MARO, TOME, RUTE): f['pv'] = estado.pv_max(E['gente'][f['id']]); f['feridas'] = []; f['pena'] = 0; f['fol_menos'] = 0      # inteiros, descansados
V = vila_teste.cria('ferreiro', semente=1); ALDO = estado.lutador(V, 'eu'); ALDO['pv'] = estado.pv_max(V['gente']['eu'])


def salteadores(r, n=None, nivel=None):
    """o bando de salteadores (gente do povo que foi para o mato): de 2 a 5, nível 6 a 12, adaga ou lança ou espada Comum, couro Comum (sem elmo: é gente pobre)"""
    n = n or r.randint(2, 5); out = []
    for i in range(n):
        nv = nivel or r.randint(6, 12); arma = r.choice([('adaga', 0), ('lança', 0), ('espada', 0), ('machado', 0)])
        p = veste(padrao(f'salteador {i + 1}', nv), arma=arma, armadura=('couro', 0), elmo=False)
        if i == 0: p['nome'] = 'o chefe do bando'; p['lider'] = True
        out.append(p)
    return out


ENCONTROS = [
    ('lobo', lambda r: bichos.bando('lobo', r)), ('javali', lambda r: bichos.bando('javali', r)), ('urso', lambda r: bichos.bando('urso', r)),
    ('goblins', lambda r: criaturas.bando('goblin', r)), ('salteadores (2 a 5)', lambda r: salteadores(r)), ('salteadores (3)', lambda r: salteadores(r, 3)),
    ('pantera', lambda r: bichos.bando('pantera', r)),
]
CASAS = [('Maro', lambda: [copy.deepcopy(MARO)]), ('Maro, Tomé e Rute', lambda: [copy.deepcopy(MARO), copy.deepcopy(TOME), copy.deepcopy(RUTE)]), ('o ferreiro do Dia 1', lambda: [copy.deepcopy(ALDO)])]


def mede(casa, enc, inicio, surpresa):
    r = random.Random(7); luta.semente(11); g = luta.D; R = dict(vence=0, morre=0, perde=0)
    try:
        for i in range(N):
            S = luta.nova(casa(), enc(random.Random(i)), inicio=inicio, surpresa=surpresa, quieto=True); luta.corre(S); h = S['L'][0]
            R['vence'] += S['fim'] == 'A'; R['perde'] += S['fim'] != 'A'; R['morre'] += h['estado'] == 'morto'
    finally: luta.D = g
    return {k: 100 * v / N for k, v in R.items()}


TAB = {}
print(f'1. AS LUTAS DA ESTRADA ({N} lutas por linha; em % das lutas: vence a casa · o primeiro da casa morre)')
for cn, casa in CASAS:
    for en, enc in ENCONTROS:
        p = mede(casa, enc, 'perto', None); c = mede(casa, enc, 'colado', 'A')
        TAB[(cn, en)] = (p, c)
        print(f"  {cn:22} contra {en:20}: viu-o e veio (perto): vence {p['vence']:5.1f} · morre {p['morre']:5.1f}   |   pego desprevenido (colado, surpreso): vence {c['vence']:5.1f} · morre {c['morre']:5.1f}")

# 2. a conta da viagem: o encontro por bloco sai da contagem do ermo que a rota cruza (o acaso da caça vezes o fator da estrada) e do bando
OUSADIA = {e: K.indole(e)[0] for e in ('corça', 'javali', 'lobo', 'urso', 'pantera', 'serpe', 'goblin')}
INVESTE = {e: K.indole(e)[1] for e in ('corça', 'javali', 'lobo', 'urso', 'pantera', 'serpe', 'goblin')}
MATA = dict(corça=80, javali=40, lobo=12, urso=3, pantera=1, goblin=6)          # a Mata do Corvo de hoje (a serpe fica fora: é chefe, não anda na estrada)
FATOR = dict(estrada=0.3, caminho=0.6, trilha=1.0)
BANDO_CADA = 150            # o bando de salteadores: homens × 1 ÷ isto por bloco (o bando de 6: 4% por bloco), vezes (1 − a patrulha)
NOME = dict(javali='javali', lobo='lobo', urso='urso', pantera='pantera', goblin='goblins')


def viagem(blocos, tipo, ermo, bando=0, patrulha=0.0, casa='Maro', politica='luta'):
    """a chance de morrer numa viagem de `blocos` blocos: cada bloco, P(encontro); o que aparece pesa pela contagem × ousadia; quem não investe vai embora (o viajante deixa);
    quem investe vira luta, começando perto (o bicho viu primeiro). O salteador sempre ataca (ou cobra pedágio: a conta não o põe). Política 'luta': fica e luta."""
    a_bicho = min(K.ACASO_MAX, sum(q * OUSADIA[e] for e, q in ermo.items()) / K.ACASO_CADA) * FATOR[tipo]
    a_bando = bando / BANDO_CADA * (1 - patrulha)
    peso = {e: q * OUSADIA[e] for e, q in ermo.items()}; tot = sum(peso.values()) or 1
    morre_enc = 0.0
    for e, w in peso.items():
        if e == 'corça': continue
        p = TAB[(casa, NOME[e])][0]['morre'] / 100; morre_enc += (w / tot) * INVESTE[e] * p
    m_bicho = a_bicho * morre_enc; m_bando = a_bando * TAB[(casa, 'salteadores (2 a 5)')][0]['morre'] / 100
    por_bloco = m_bicho + m_bando
    return 1 - (1 - por_bloco) ** blocos, a_bicho, a_bando


print('\n2. A CONTA DA VIAGEM (o encontro por bloco pela regra proposta; a luta pelas linhas de cima; o viajante fica e luta; o caminho de dia)')
casos = [('a estrada da vila (4 blocos), cruzando a Mata do Corvo cheia', 4, 'estrada', MATA, 0, 0.5),
         ('o caminho da aldeia (4 blocos), pela Mata cheia', 4, 'caminho', MATA, 0, 0.0),
         ('a trilha (6 blocos), pela Mata cheia', 6, 'trilha', MATA, 0, 0.0),
         ('a trilha (6 blocos), pela Mata cheia, com um bando de 6 salteadores', 6, 'trilha', MATA, 6, 0.0),
         ('o caminho (4 blocos), campo sem bicho, bando de 8, patrulha fraca', 4, 'caminho', {}, 8, 0.2),
         ('a trilha da serra (6 blocos): lobo 12, urso 3, pantera 2', 6, 'trilha', dict(lobo=12, urso=3, pantera=2), 0, 0.0)]
for nome, bl, tipo, erm, bd, pt in casos:
    for cn in ('Maro', 'Maro, Tomé e Rute', 'o ferreiro do Dia 1'):
        m, ab, an = viagem(bl, tipo, erm, bd, pt, casa=cn)
        print(f"  {nome:72} · {cn:20}: encontro de bicho {100 * ab:.2f}% por bloco, de bando {100 * an:.2f}% · MORRE em {100 * m:.2f}% das viagens")
json.dump({f'{k[0]}|{k[1]}': v for k, v in TAB.items()}, open(os.path.join(os.path.dirname(os.environ['MOTOR10_MUNDO']), 'm4_tab.json'), 'w'), ensure_ascii=False)
