#!/usr/bin/env python3
"""m2_gravador.py — MEDIDA (projeto A, etapa 3): o gravador por toque (proto_aplica) dá O MESMO MUNDO que o de hoje, e quanto mais depressa.

Roda de dentro de motor10/:  PYTHONDONTWRITEBYTECODE=1 python3 projeto/etapa3/projeto_a/medidas/m2_gravador.py [dias=40]
Tudo em memória (nada é gravado em pasta nenhuma).
  1. A vila de teste com a magia e a 4b, o personagem esperando e comendo (o mundo vira sozinho), N dias: com o gravador de hoje e com o por toque.
  2. O robô ferreiro de loja do provas_mercado (forja, compra, vende, jornal, cama), 30 dias, três sementes: com os dois gravadores.
Confere: o estado final e o registro de eventos saem iguais, número por número.
"""
import copy, json, os, sys, time
sys.path.insert(0, os.getcwd()); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import estado, ato, vila_teste, proto_aplica
op = dict(x.split('=', 1) for x in sys.argv[1:] if '=' in x); dias = int(op.get('dias', 40))


def vila():
    E = vila_teste.cria('ferreiro', semente=3, talentos=True, inclinacao='forja', inclinacao2='encanto')
    vila_teste.magia(E); vila_teste.fantasia(E); E['_novos'] = []
    return E


def espera(E, dias):
    eu = estado.eu(E); evs = []
    for _ in range(dias * 6):
        if E['gente'][eu]['corpo']['fome'] >= 3:
            try: ato.comer(E, eu)
            except SystemExit: pass
        ato.passa(E, eu, 1, 'esperar', texto='espera', para=False)
        evs += E['_novos']; E['_novos'] = []
    return evs


def retrato(E): return json.dumps({k: E[k] for k in estado.ARQS}, sort_keys=True, ensure_ascii=False)


base = vila()
R = {}
for nome, inst in (('hoje', proto_aplica.desinstala), ('por toque', proto_aplica.instala)):
    inst(); E = copy.deepcopy(base); t = time.perf_counter(); evs = espera(E, dias); dt = time.perf_counter() - t
    R[nome] = (retrato(E), json.dumps(evs, sort_keys=True, ensure_ascii=False), dt, len(evs))
proto_aplica.desinstala()
print(f"1. A VILA DE TESTE (magia e 4b), {dias} dias com o personagem esperando: {R['hoje'][3]} eventos")
for k, (_, _, dt, n) in R.items(): print(f"   gravador {k}: {dt:.2f} s ({1000 * dt / dias:.1f} ms por dia; {1000 * dt / max(1, n):.2f} ms por evento)")
print(f"   o estado final é o mesmo: {R['hoje'][0] == R['por toque'][0]} · o registro de eventos é o mesmo: {R['hoje'][1] == R['por toque'][1]}")

import provas_mercado
print('\n2. O ROBÔ FERREIRO DE LOJA (provas_mercado), 30 dias, categorias Comum e Incomum')
for sem in (1, 2, 3):
    out = {}
    for nome, inst in (('hoje', proto_aplica.desinstala), ('por toque', proto_aplica.instala)):
        inst(); t = time.perf_counter(); V = provas_mercado.ferreiro_de_loja(sem, (0, 1)); out[nome] = (json.dumps(V, sort_keys=True), time.perf_counter() - t)
    proto_aplica.desinstala()
    print(f"   semente {sem}: hoje {out['hoje'][1]:.2f} s · por toque {out['por toque'][1]:.2f} s · o resultado é o mesmo: {out['hoje'][0] == out['por toque'][0]}")
