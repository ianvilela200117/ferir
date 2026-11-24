"""m1: quanto vale cada atributo, o tamanho e o escuro, no duelo de nível 50 com peças Raras (a régua do Grande Dom: 54 a 64%, medido 61%)."""
import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-ferir/2caa978a-1aa4-5b05-88b7-11bcda935cb0/scratchpad/masmorras/projeto_b/medidas')
from base_b import *

N = int(sys.argv[1]) if len(sys.argv) > 1 else 4000
H = lambda: [homem('humano', 50)]
linhas = [
    ('o gêmeo (igual em tudo)', lambda: [homem('x', 50)], {}),
    ('o Grande Dom no fio (+2)', lambda: [homem('x', 50, dom={'fio': 2})], {}),
    ('o Dom no fio (+1)', lambda: [homem('x', 50, dom={'fio': 1})], {}),
    ('Força +10', lambda: [homem('x', 50, mods={'Força': 10})], {}),
    ('Agilidade +10', lambda: [homem('x', 50, mods={'Agilidade': 10})], {}),
    ('Vigor +10', lambda: [homem('x', 50, mods={'Vigor': 10})], {}),
    ('Vigor +5', lambda: [homem('x', 50, mods={'Vigor': 5})], {}),
    ('Vontade +10', lambda: [homem('x', 50, mods={'Vontade': 10})], {}),
    ('Percepção +10', lambda: [homem('x', 50, mods={'Percepção': 10})], {}),
    ('Vigor −10', lambda: [homem('x', 50, mods={'Vigor': -10})], {}),
    ('Força −10', lambda: [homem('x', 50, mods={'Força': -10})], {}),
    ('Agilidade −10', lambda: [homem('x', 50, mods={'Agilidade': -10})], {}),
    ('o tamanho pequeno (PV × 0,6, Defesa +2, 2 batem nele)', lambda: [homem('x', 50, povo=dict(tamanho='pequeno', tracos=[], coragem=0, couro=None, cat=0))], {}),
    ('no escuro: noturno (o escuro não tira nada)', lambda: [homem('x', 50, tracos=['noturno'])], dict(tempo=['escuro'])),
    ('no escuro: os dois sem nada', lambda: [homem('x', 50)], dict(tempo=['escuro'])),
]
print(f'DUELO, nível 50, espada, malha e escudo Raros, contra o humano igual ({N} lutas por linha; começa perto)')
for nome, fa, kw in linhas:
    v, r, ma, mb = duelo(fa, H, n=N, inicio='perto', **kw)
    print(f'  {nome:<58} vence {v:5.1f}%  · rodadas {r} · morre {ma:.2f} · mata {mb:.2f}')
