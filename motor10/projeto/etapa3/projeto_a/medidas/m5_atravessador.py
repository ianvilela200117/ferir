#!/usr/bin/env python3
"""m5_atravessador.py — MEDIDA (projeto A, etapa 3): quanto rende o ATRAVESSADOR (comprar onde é barato, levar, vender onde é caro) e o FRETE (levar o que o povo não leva),
na região do protótipo, com o mercado de verdade (o custa, o paga, a loja que paga 60% ao Leigo, a mão de comércio que sobe por dias de negócio).

Roda de dentro de motor10/:  PYTHONDONTWRITEBYTECODE=1 python3 projeto/etapa3/projeto_a/medidas/m5_atravessador.py COPIA_DO_ENSAIO [dias=120] [sementes=1,2,3] [moeda=1]
O robô é o personagem (o Maro da cópia, com a bolsa que se diz), GANANCIOSO: em cada povoado olha cada rota que sai dali e cada bem, e compra o lote (até o que ele leva:
Força ÷ 2 de peso, mais 80 com a mula) que mais rende, pela conta de hoje: o que a loja do destino paga, menos o que custa aqui, menos a viagem (a comida, a cama, a mula, a comida que estraga).
Viaja (o tempo anda pelo ato.passa), vende, e de novo. Sem lote que pague, anda para o vizinho maior (ou espera um dia). O PERIGO da estrada não mata o robô aqui: a conta dele sai
à parte, pela chance de encontro de cada rota (a regra do PROJETO) e pelas lutas do m4 (o Maro sozinho, ficando para lutar): a chance de estar vivo no fim.
"""
import json, math, os, sys
sys.path.insert(0, os.getcwd()); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
a = sys.argv[1:]
if not a: print(__doc__); sys.exit()
os.environ['MOTOR10_MUNDO'] = os.path.abspath(a[0]); op = dict(x.split('=', 1) for x in a[1:] if '=' in x)
DIAS = int(op.get('dias', 120)); SEMS = [int(x) for x in op.get('sementes', '1,2,3').split(',')]
import estado, ato, mercado
import tabelas_mundo as M, tabelas_mercado as C, tabelas_caca as K
import proto_regiao as R
R.instala()
if op.get('moeda', '1') == '1': R.moeda_na_loja()
TAB4 = json.load(open(os.path.join(os.path.dirname(os.environ['MOTOR10_MUNDO']), 'm4_tab.json')))
MORRE = {e: TAB4[f'Maro|{n}'][0]['morre'] / 100 for e, n in (('lobo', 'lobo'), ('javali', 'javali'), ('urso', 'urso'), ('pantera', 'pantera'), ('goblin', 'goblins'))}
MORRE_BANDO = TAB4['Maro|salteadores (2 a 5)'][0]['morre'] / 100
MULA = dict(preco=60, leva=80, come=2)


def morte_bloco(E, rt):
    """a chance de o Maro sozinho morrer num bloco desta rota: o encontro de bicho (pesado pela contagem × ousadia, vezes o investe), e o do bando"""
    a_b, a_n = R.perigo_rota(E, rt); er = E['lugares'].get(rt.get('ermo')) or {}
    w = {e: q * K.indole(e)[0] for e, q in (er.get('bichos') or {}).items() if q >= 1 and e in MORRE}; tot = sum(q * K.indole(e)[0] for e, q in (er.get('bichos') or {}).items() if q >= 1 and not (estado.especie(e) or {}).get('chefe')) or 1
    return a_b * sum(w[e] / tot * K.indole(e)[1] * MORRE[e] for e in w) + a_n * MORRE_BANDO


def leva(p): return p['atributos']['Força'] / 2 + MULA['leva']
def peso_carga(p): return sum(R._peso(b) * q for b, q in (p.get('carga') or {}).items())


def melhor(E):
    p = E['gente']['eu']; aqui = p['lugar']; best = None
    for rid, rt in E['rotas'].items():
        if aqui not in (rt['a'], rt['b']): continue
        dest = rt['b'] if rt['a'] == aqui else rt['a']
        if dest == 'fora' or not mercado.tem_mercado(E, dest): continue
        dias = rt['blocos'] / 4; custo_v = math.ceil(dias) * (M.CAMA_PRECO + M.REFEICAO_PRECO + MULA['come'])
        for b in R.BENS:
            tem = E['lugares'][aqui]['estoque'].get(b, 0); cap = int((leva(p) - peso_carga(p)) / R._peso(b))
            for n in sorted({max(1, cap // 8), max(1, cap // 4), max(1, cap // 2), cap}):
                n = min(n, int(tem))
                if n < 1: continue
                c = mercado.custa(E, aqui, b, n)
                if c > p['moedas'] - 10: continue
                estraga = (1 - (1 - R.TAB['ESTRAGA']) ** math.ceil(dias)) if b == 'comida' else 0
                v = mercado.paga(E, 'eu', b, int(n * (1 - estraga)), lid=dest)
                lucro = v - c - custo_v
                if best is None or lucro > best[0]: best = (lucro, rid, dest, b, n, c, v)
    return best


def come_dorme(E):
    p = E['gente']['eu']
    if p['corpo']['fome'] >= 3:
        try: ato.comer(E, 'eu')
        except SystemExit:
            try: ato.comer(E, 'eu', da_carga=True)
            except SystemExit: pass
    p = E['gente']['eu']
    if p['corpo']['sono'] >= 5 or E['relogio']['bloco'] in (0, 5):
        try: ato.dormir(E, 'eu', 2, para=False)
        except SystemExit: ato.dormir(E, 'eu', 2, chao=True, para=False)


def vida(sem):
    E = R.monta(sem, prata_eu=0)
    p = E['gente']['eu']; quer = 200 - p['moedas']
    estado.aplica(E, 'mestre', [['pessoa', 'eu', 'moedas', 'soma', quer + MULA['preco']]], quem=['eu'], texto='(medida) o atravessador começa com 200 de prata e uma mula')
    estado.aplica(E, 'mestre', [['pessoa', 'eu', 'moedas', 'soma', -MULA['preco']], ['estoque', 'vila', 'prata', 'soma', MULA['preco']]], quem=['eu'], texto='(medida) compra a mula')
    p0 = E['gente']['eu']['moedas']; fim = estado.agora(E) + DIAS * M.BLOCOS_DIA; vivo = 1.0; viagens = 0; lucros = []; parado = 0; blocos_estrada = 0
    while estado.agora(E) < fim and E['gente']['eu']['estado'] == 'vivo':
        come_dorme(E)
        # vende o que leva, se aqui paga mais do que custou
        for b, q in list((E['gente']['eu'].get('carga') or {}).items()):
            if b == 'comida' and q <= 4: continue
            if q >= 1 and mercado.paga(E, 'eu', b, int(q)) >= 1:
                try: mercado.vender(E, 'eu', b, int(q) - (4 if b == 'comida' else 0))
                except SystemExit: pass
        x = melhor(E)
        if x and x[0] > 0:
            lucro, rid, dest, b, n, c, v = x; rt = E['rotas'][rid]
            r = mercado.comprar(E, 'eu', b, n)
            vivo *= (1 - morte_bloco(E, rt)) ** rt['blocos']; blocos_estrada += rt['blocos']
            ato.passa(E, 'eu', rt['blocos'], 'viagem', esforco='leve', para=False, mais=lambda i: [])
            estado.aplica(E, 'viagem', [['pessoa', 'eu', 'lugar', 'poe', dest]], quem=['eu'], texto=f'chega a {E["lugares"][dest]["nome"]}')
            q = E['gente']['eu'].get('carga', {}).get(b, 0); pg = 0
            if q >= 1:
                try: pg = mercado.vender(E, 'eu', b, int(q))['prata']
                except SystemExit: pass
            lucros.append(pg - r['prata']); viagens += 1
        else:
            parado += 1; aqui = E['gente']['eu']['lugar']
            vz = [(E['lugares'][rt['b'] if rt['a'] == aqui else rt['a']].get('pop', 0), rid) for rid, rt in E['rotas'].items() if aqui in (rt['a'], rt['b']) and 'fora' not in (rt['a'], rt['b'])]
            if parado % 3 == 0 and vz:                     # sem lote que pague, anda para o vizinho (o maior, ou outro), e olha lá
                _, rid = sorted(vz)[-1 - (parado // 3) % len(vz)]; rt = E['rotas'][rid]; dest = rt['b'] if rt['a'] == aqui else rt['a']
                vivo *= (1 - morte_bloco(E, rt)) ** rt['blocos']; blocos_estrada += rt['blocos']
                ato.passa(E, 'eu', rt['blocos'], 'viagem', esforco='leve', para=False)
                estado.aplica(E, 'viagem', [['pessoa', 'eu', 'lugar', 'poe', dest]], quem=['eu'], texto=f'chega a {E["lugares"][dest]["nome"]}')
            else: ato.passa(E, 'eu', 2, 'esperar', para=False)
        # a mula come
        if E['relogio']['bloco'] == 2 and E['gente']['eu']['moedas'] >= MULA['come']:
            estado.aplica(E, 'mestre', [['pessoa', 'eu', 'moedas', 'soma', -MULA['come']], ['estoque', E['gente']['eu']['lugar'], 'prata', 'soma', MULA['come']]], quem=['eu'], texto='a mula come')
        E['_novos'] = []
    eu = E['gente']['eu']; ganho = eu['moedas'] - p0 + sum(mercado.paga(E, 'eu', b, int(q)) for b, q in (eu.get('carga') or {}).items() if q >= 1)
    return dict(ganho=ganho, por_dia=ganho / DIAS, viagens=viagens, parado=parado, vivo=vivo, mao=T_M[(eu.get('maestria') or {}).get('comércio', 0)], lucros=lucros, blocos=blocos_estrada,
                prata=R.prata_do_mundo(E))


import tabelas as T
T_M = T.MAESTRIAS
for sem in SEMS:
    V = vida(sem); L = sorted(V['lucros'])
    print(f"semente {sem}: em {DIAS} dias o atravessador (200 de prata e uma mula; come, dorme na cama, a mula come) ficou com {V['ganho']:+d} de prata ({V['por_dia']:+.2f} por dia), "
          f"{V['viagens']} viagens ({V['blocos']} blocos de estrada), {V['parado']} vezes sem lote que pague · a mão de comércio chegou a {V['mao']} · "
          f"o lucro da viagem: mediana {L[len(L) // 2] if L else 0}, o melhor {L[-1] if L else 0}, o pior {L[0] if L else 0} · o Maro sozinho estaria vivo no fim em {100 * V['vivo']:.0f}% das vidas")
