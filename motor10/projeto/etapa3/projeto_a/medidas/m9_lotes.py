# m9_lotes.py: o melhor lote do atravessador em cada povoado, a cada 10 dias, por 100 dias (sem a viagem): quantos dão lucro antes da estrada
# roda de dentro de motor10/: PYTHONDONTWRITEBYTECODE=1 python3 projeto/etapa3/projeto_a/medidas/m9_lotes.py COPIA_DO_ENSAIO
import os, sys, json, math
sys.path.insert(0, os.getcwd()); sys.path.insert(0, 'projeto/etapa3/projeto_a/medidas')
os.environ['MOTOR10_MUNDO'] = sys.argv[1]
import estado, ato, mercado
import proto_regiao as R, tabelas_mercado as C
R.instala(); R.moeda_na_loja()
E = R.monta(1, prata_eu=500)
# anda 100 dias, e a cada 10 olha o melhor lote de cada povoado (como se o robô estivesse ali), sem a viagem
melhores = []
for d in range(100):
    for _ in range(6):
        if E['gente']['eu']['corpo']['fome'] >= 3:
            try: ato.comer(E, 'eu')
            except SystemExit: pass
        ato.passa(E, 'eu', 1, 'esperar', para=False)
    E['_novos'] = []
    if d % 10 == 9:
        for aqui in [k for k in E['lugares'] if mercado.tem_mercado(E, k) and k != 'fora']:
            for rid, rt in E['rotas'].items():
                if aqui not in (rt['a'], rt['b']): continue
                dest = rt['b'] if rt['a'] == aqui else rt['a']
                if dest == 'fora': continue
                for b in R.BENS:
                    tem = int(E['lugares'][aqui]['estoque'].get(b, 0)); n = min(tem, int(115 / R._peso(b)))
                    for k in (1, max(1, n // 4), n):
                        if k < 1: continue
                        c = mercado.custa(E, aqui, b, k); v = mercado.paga(E, 'eu', b, k, lid=dest)
                        melhores.append((v - c, d, aqui, dest, b, k, c, v, round(mercado.preco(E, dest, b) / mercado.preco(E, aqui, b), 2)))
melhores.sort(reverse=True)
for x in melhores[:15]: print(x)
print('quantos lotes dão lucro antes da viagem:', sum(1 for x in melhores if x[0] > 0), 'de', len(melhores))
from collections import Counter
print('os bens dos 200 melhores:', Counter(x[4] for x in melhores[:200]).most_common(8))
