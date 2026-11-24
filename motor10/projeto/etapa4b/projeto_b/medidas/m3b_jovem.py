"""m3b: variantes do dragão jovem contra o grupo de nível 50 de peças Raras (a pergunta do pedido): quantos vencem, quantos morrem, o que a categoria da peça faz."""
import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-ferir/2caa978a-1aa4-5b05-88b7-11bcda935cb0/scratchpad/masmorras/projeto_b/medidas')
from dragoes_ensaio import *
N = int(sys.argv[1]) if len(sys.argv) > 1 else 600
VAR = {
    'v2 (nível 70, Vigor 110, Treinado)': dict(),
    'v3 (Vigor 130)': dict(at=(110, 70, 130, 60, 75, 45)),
    'v4 (Vigor 130, Mestre)': dict(at=(110, 70, 130, 60, 75, 45), instinto=6),
    'v5 (Vigor 150, Mestre, nível 80)': dict(at=(120, 70, 150, 60, 75, 45), instinto=6, nivel=80),
}
base = dict(IDADES['jovem'])
for nome, mud in VAR.items():
    IDADES['jovem'] = dict(base, **mud)
    f = ficha(dragao('serra', 'jovem'))
    print(f"{nome}: PV {f['pvmax']}, acerto {f['arma']['acerto']:+g}, Defesa {defesa(f):g}")
    D = lambda: [dragao('serra', 'jovem')]
    for rot, g in (('4 de nível 50, tudo Raro', grupo(4, 50, R, R)), ('4 misto (2 espadas, lança, arco)', grupo(4, 50, R, R, misto=True)),
                   ('5 de nível 50, tudo Raro', grupo(5, 50, R, R)), ('4 com a ARMA Épica (o resto Raro)', lambda: [homem(f'h{i}', 50, arma=R + 1) for i in range(4)]),
                   ('4 com a armadura Épica (a arma Rara)', lambda: [homem(f'h{i}', 50, arm=R + 1, esc=R) for i in range(4)])):
        r = grupo_contra(g, D, n=N, inicio='perto')
        print(f"   {rot:<38} vence {r['vence']:5.1f}% · mortos por luta {r['mortos']:.2f} · alguém morre em {r['alguem_morre']:5.1f}% · rodadas {r['rodadas']}")
