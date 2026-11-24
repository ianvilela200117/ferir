"""m2: cada povo contra o humano de peças iguais (a lei: nunca mais que o Grande Dom, cerca de 60%; e perde para a arma uma acima como o Grande Dom perde, até 15%)."""
import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-ferir/2caa978a-1aa4-5b05-88b7-11bcda935cb0/scratchpad/masmorras/projeto_b/medidas')
from povos_ensaio import *

N = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
so = sys.argv[2].split(',') if len(sys.argv) > 2 else list(POVOS)
H = lambda: [de_povo('humano', 'o rival', 50)]
H1 = lambda: [de_povo('humano', 'o rival', 50, arma=R + 1)]
Hc = lambda: [de_povo('humano', 'o rival', 5, arma=0, arm=0)]
print(f'nível 50, espada, malha e escudo Raros ({N} lutas por linha, começa perto). A régua: o Grande Dom vence o gêmeo 59,8%; com a arma do gêmeo uma acima, até 15%.')
for pv in so:
    P = lambda pv=pv: [de_povo(pv, pv, 50)]
    Pc = lambda pv=pv: [de_povo(pv, pv, 5, arma=0, arm=0)]
    a = duelo(P, H, n=N, inicio='perto')[0]
    b = duelo(P, H, n=N, inicio='perto', tempo=['escuro'])[0]
    c = duelo(P, H1, n=N, inicio='perto')[0]
    d = duelo(Pc, Hc, n=N, inicio='perto')[0]
    print(f'  {pv:<10} contra o humano: {a:5.1f}% · no escuro {b:5.1f}% · contra a arma uma acima {c:5.1f}% · no nível 5, tudo Comum {d:5.1f}%')
