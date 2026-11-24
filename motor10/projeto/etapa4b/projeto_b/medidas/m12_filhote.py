"""m12: o filhote como bicho comum (moral "testa": ferido, pode fugir; coragem 0) contra um homem do degrau (nível 30, Incomum), cada tipo em casa."""
import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-ferir/2caa978a-1aa4-5b05-88b7-11bcda935cb0/scratchpad/masmorras/projeto_b/medidas')
from dragoes_ensaio import *
N = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
CASA = {'serra': {}, 'brejo': dict(tempo=['água']), 'grutas': dict(tempo=['escuro'])}
for tipo in TIPOS:
    for moral in ('firme', 'testa'):
        luta.semente(3); v = fug = m = 0
        for _ in range(N):
            S = luta.nova(grupo(1, 30, 1, 1)(), [dragao(tipo, 'filhote', moral=moral, coragem=0)], quieto=True, inicio='perto', **CASA[tipo]); luta.corre(S)
            v += S['fim'] == 'A'; fug += any(f['estado'] == 'fugiu' for f in S['L'] if f['lado'] == 'B'); m += S['L'][0]['estado'] == 'morto'
        print(f'  filhote {tipo:<7} moral {moral:<6}: o homem vence {100 * v / N:5.1f}% (o filhote fugiu em {100 * fug / N:4.1f}%) · o homem morre {100 * m / N:4.1f}%')
