"""m5b: a fúria do dragão da serra: (i) desce ao chão em fúria (perde 'voa', ganha 'ardente'), (ii) a fúria a 30%."""
import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-ferir/2caa978a-1aa4-5b05-88b7-11bcda935cb0/scratchpad/masmorras/projeto_b/medidas')
from dragoes_ensaio import *
N = int(sys.argv[1]) if len(sys.argv) > 1 else 300
IDADES['velho']['tracos'] = ['sopro', 'apavora', 'couraça', 'resiste']
IDADES['ancião']['tracos'] = ['sopro', 'apavora', 'couraça', 'resiste']
OPC = {'(i) desce ao chão em fúria a 50%': [dict(abaixo=0.5, perde=['voa'], ganha=['ardente'], diz='desce ao chão em fúria')],
       '(ii) a fúria a 30%': [dict(abaixo=0.3, ganha=['ardente'], diz='a fúria')],
       '(iii) desce ao chão em fúria a 30%': [dict(abaixo=0.3, perde=['voa'], ganha=['ardente'], diz='desce ao chão em fúria')]}
for idade in ('jovem', 'adulto', 'velho', 'ancião'):
    c = IDADES[idade]['cat']; n = REF[c]; V = {'Vontade': 80} if c >= 3 else {}
    for rot, fs in OPC.items():
        for k in (4, 6):
            r = grupo_contra(grupo(k, n, c, c, atributos=V), lambda fs=fs: [dragao('serra', idade, fases=fs)], n=N, inicio='perto')
            print(f"{idade:<7} {rot:<36} {k} do degrau: vence {r['vence']:5.1f}% · mortos {r['mortos']:.2f} · alguém morre {r['alguem_morre']:5.1f}%")
