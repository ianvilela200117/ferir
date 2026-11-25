#!/usr/bin/env python3
"""m1_custo_dia.py — MEDIDA (projeto A, etapa 3): quanto custa em tempo um dia de mundo HOJE (a vila de teste com a magia e a 4b), e de onde vem o custo.

Roda de dentro de motor10/:  PYTHONDONTWRITEBYTECODE=1 python3 projeto/etapa3/projeto_a/medidas/m1_custo_dia.py RASCUNHO [dias=60]
RASCUNHO: uma pasta de rascunho FORA do repositório; a vila nasce em RASCUNHO/m1_vila (apagada antes, se existir).
Nada é gravado fora do rascunho: o mundo anda em memória (o estado.grava não é chamado depois de nascer).
"""
import os, shutil, sys, time, cProfile, pstats, io
sys.path.insert(0, os.getcwd())
a = sys.argv[1:]
if not a: print(__doc__); sys.exit()
raiz = os.path.abspath(a[0]); op = dict(x.split('=', 1) for x in a[1:] if '=' in x); dias = int(op.get('dias', 60))
if raiz.startswith(os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))):
    sys.exit('o rascunho tem de ficar fora do repositório')
pasta = os.path.join(raiz, 'm1_vila'); shutil.rmtree(pasta, ignore_errors=True)
import vila_teste, estado, ato
vila_teste.main([pasta, 'comeco=ferreiro', 'inclinacao=forja', 'inclinacao2=encanto'])
vila_teste.main(['magia', pasta]); vila_teste.main(['fantasia', pasta])
os.environ['MOTOR10_MUNDO'] = pasta
E = estado.carrega()
import json
tam = {k: len(json.dumps(E[k], ensure_ascii=False)) for k in estado.ARQS}
print('\nTAMANHO DO ESTADO (bytes, json compacto):', tam, 'total', sum(tam.values()))
# o personagem espera, dia após dia (o mundo vira sozinho): sem comer morre de fome, então come da loja uma vez por dia
eu = estado.eu(E)
t0 = time.perf_counter(); n_ev0 = E['relogio']['eventos']
pr = cProfile.Profile(); pr.enable()
for d in range(dias):
    for _ in range(6):
        if E['gente'][eu]['corpo']['fome'] >= 3:
            try: ato.comer(E, eu)
            except SystemExit: pass
        ato.passa(E, eu, 1, 'esperar', texto='espera', para=False)
pr.disable()
dt = time.perf_counter() - t0
print(f'\n{dias} dias em {dt:.2f} s: {1000 * dt / dias:.1f} ms por dia; {E["relogio"]["eventos"] - n_ev0} eventos ({(E["relogio"]["eventos"] - n_ev0) / dias:.1f} por dia)')
print(f'um ano (364 dias) neste passo: {364 * dt / dias:.1f} s')
s = io.StringIO(); pstats.Stats(pr, stream=s).sort_stats('cumulative').print_stats(18); print(s.getvalue()[:4000])
