"""m13: o corredor e o dragão, na proposta final (m11): o jovem e o adulto da serra, no covil (sem saída), na câmara aberta e num corredor de largura 2 e de 1."""
import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-ferir/2caa978a-1aa4-5b05-88b7-11bcda935cb0/scratchpad/masmorras/projeto_b/medidas')
import m11_final as F
from dragoes_ensaio import grupo, R
N = int(sys.argv[1]) if len(sys.argv) > 1 else 600
for idade, g in (('jovem', grupo(4, 50, R, R)), ('adulto', grupo(4, 90, 3, 3, atributos={'Vontade': 80}))):
    for rot, lugar in (('câmara aberta', dict(sem_saida='B')), ('corredor de largura 2', dict(sem_saida='B', largura=2)), ('corredor de largura 1', dict(sem_saida='B', largura=1))):
        r = F.grupo_contra(g, F.D('serra', idade), n=N, inicio='perto', lugar=lugar)
        F.lin(f'{idade}, 4 do degrau, {rot}', r)
