"""m5_surpresa.py: o que vale ver primeiro no grupo (a surpresa dos dois lados), e o que vale a luz e o corredor, na cripta de teste (cópia do ensaio)."""
import sys
from med_comum import *
N = int(sys.argv[1]) if len(sys.argv) > 1 else 500
L = []
def m(nome, fa, fb, **kw):
    R = duelos(fa, fb, N, **kw); L.append(diz(nome, R)); print(L[-1], flush=True); return R
G3 = lambda: [cheio('tome'), cheio('eu', controla=True), cheio('rute', linha='trás')]
esq = lambda n: (lambda i: CR.bando('esqueleto', n=n))
gob = lambda n: (lambda i: CR.bando('goblin', n=n, toca=True))
for nome, f in (('6 esqueletos', esq(6)), ('8 goblins (a toca: faca, lança e arco)', gob(8))):
    for sp, txt in ((None, 'ninguém surpreso'), ('B', 'o grupo surpreende (viu primeiro)'), ('A', 'o grupo é surpreendido')):
        m(f'grupo de 3 (Tomé na frente) contra {nome}, sala aberta, com luz: {txt}', G3, f, inicio='perto', surpresa=sp)
    m(f'grupo de 3 (Tomé na frente) contra {nome}, sala aberta, NO ESCURO, ninguém surpreso', G3, f, inicio='perto', tempo=['escuro'])
    m(f'grupo de 3 (Tomé na frente) contra {nome}, corredor de 1, com luz, ninguém surpreso', G3, f, inicio='perto', lugar=dict(largura=1))
open('m5_saida.txt', 'w').write('\n'.join(L) + '\n')
