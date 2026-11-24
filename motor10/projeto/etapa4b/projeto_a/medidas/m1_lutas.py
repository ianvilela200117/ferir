"""m1_lutas.py: as lutas da cripta de teste contra o Maro de hoje (cópia do ensaio) e os companheiros da vila.
O que se mede: o corredor de um contra a sala aberta, a luz contra o escuro, a surpresa dos dois lados, o grupo, o chefe do fundo."""
import sys
from med_comum import *

N = int(sys.argv[1]) if len(sys.argv) > 1 else 600
maro = lambda: gente('eu', controla=True)
maro_cheio = lambda: cheio('eu', controla=True)
esq = lambda n: (lambda i: CR.bando('esqueleto', n=n))
seco = lambda n: (lambda i: CR.bando('corpo-seco', n=n))
rato = lambda n: (lambda i: bichos.bando('ratazana', n=n))
L = []
def m(nome, fa, fb, **kw):
    R = duelos(fa, fb, N, **kw); L.append(diz(nome, R)); print(L[-1], flush=True); return R

print('== MARO SOZINHO (PV cheio; espada, escudo, malha e elmo Comuns) ==')
for n in (1, 2, 3):
    m(f'{n} esqueleto(s), sala aberta, com luz, perto', lambda: [maro_cheio()], esq(n), inicio='perto')
    m(f'{n} esqueleto(s), corredor de 1, com luz, perto', lambda: [maro_cheio()], esq(n), inicio='perto', lugar=dict(largura=1))
    m(f'{n} esqueleto(s), sala aberta, NO ESCURO, perto', lambda: [maro_cheio()], esq(n), inicio='perto', tempo=['escuro'])
for n in (1, 2, 3):
    m(f'{n} corpo(s)-seco(s), sala aberta, com luz', lambda: [maro_cheio()], seco(n), inicio='perto')
    m(f'{n} corpo(s)-seco(s), corredor de 1, com luz', lambda: [maro_cheio()], seco(n), inicio='perto', lugar=dict(largura=1))
for n in (3, 6):
    m(f'{n} ratazanas, sala aberta, com luz', lambda: [maro_cheio()], rato(n), inicio='perto')
print('== A SURPRESA (3 esqueletos, sala aberta, com luz) ==')
m('Maro surpreende (os esqueletos perdem o 1º turno)', lambda: [maro_cheio()], esq(3), inicio='perto', surpresa='B')
m('Maro é surpreendido (perde o 1º turno), colado', lambda: [maro_cheio()], esq(3), inicio='colado', surpresa='A')
print('== O GRUPO: Maro, Tomé e Rute (PV cheio) ==')
grupo = lambda: [maro_cheio(), cheio('tome'), cheio('rute', linha='trás')]
grupo4 = lambda: [maro_cheio(), cheio('tome'), cheio('rute', linha='trás'), cheio('anselmo', linha='trás')]
for n in (4, 6):
    m(f'grupo de 3 contra {n} esqueletos, corredor de 1, com luz', grupo, esq(n), inicio='perto', lugar=dict(largura=1))
    m(f'grupo de 3 contra {n} esqueletos, sala aberta, com luz', grupo, esq(n), inicio='perto')
    m(f'grupo de 3 contra {n} esqueletos, sala aberta, NO ESCURO', grupo, esq(n), inicio='perto', tempo=['escuro'])
m('grupo de 4 (com Anselmo) contra 6 esqueletos, sala aberta, com luz', grupo4, esq(6), inicio='perto')
open('m1_saida.txt', 'w').write('\n'.join(L) + '\n')
