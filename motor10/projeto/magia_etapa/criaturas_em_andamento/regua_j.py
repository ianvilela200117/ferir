"""regua_j.py — onde cai cada criatura nova na régua dos graus. Uso: python3 regua_j.py [N] [só estas...]"""
import sys
from mede import *
n = int(sys.argv[1]) if len(sys.argv) > 1 else 300; so = sys.argv[2:]
def linha(que):
    e = TC.TROPA.get(que) or TB.ESPECIES[que]; c = e['cat']; lo, hi = e['bando']; tr = (TC.POVOS[e['povo']]['tracos'] if que in TC.TROPA else e['tracos']); gate = 'imaterial' in tr or 'pede prata' in tr
    print(diz(f"{e['nome']} (grau {e['grau']}, {T.CATS[c]}): 1 homem × 1", mede(homens(1, c), cri(que, 1), n)))
    if 'ossos' in tr: print(diz(f"   1 homem de MAÇA × 1", mede(homens(1, c, familia='maça'), cri(que, 1), n)))
    if gate: print(diz(f"   1 homem com arma de PRATA × 1", mede(homens(1, c, prata=True), cri(que, 1), n)))
    if gate: print(diz(f"   1 homem com a arma uma categoria ACIMA × 1", mede(homens(1, c, arma=c + 1), cri(que, 1), n)))
    if hi > 1: print(diz(f"   1 homem × {hi}", mede(homens(1, c), cri(que, hi), n)))
    if c >= 3 or hi > 1: print(diz(f"   4 homens × {hi}", mede(homens(4, c), cri(que, hi), n)))
    if gate and (c >= 3 or hi > 1): print(diz(f"   4 homens com arma de PRATA × {hi}", mede(homens(4, c, prata=True), cri(que, hi), n)))
    if c >= 3: print(diz(f"   4 homens de conjunto uma categoria ABAIXO × {hi}", mede(homens(4, c - 1), cri(que, hi), n)))
print(f'A RÉGUA DAS CRIATURAS NOVAS ({n} lutas por linha; o homem do degrau é o do banco: espada, malha e escudo da categoria, nível {TC.REF}; o aço comum conta {TC.PEDE_PRATA} categoria(s) abaixo em quem pede prata)')
for que in list(TC.TROPA) + list(TC.CORPOS):
    if que == 'vampiro': continue
    if not so or que in so: linha(que)
