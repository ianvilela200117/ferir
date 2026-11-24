"""m3: as idades do dragão contra o grupo do degrau, e o jovem contra o grupo de nível 50 de peças Raras (a pergunta do pedido)."""
import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-ferir/2caa978a-1aa4-5b05-88b7-11bcda935cb0/scratchpad/masmorras/projeto_b/medidas')
from dragoes_ensaio import *

N = int(sys.argv[1]) if len(sys.argv) > 1 else 300
tipo = sys.argv[2] if len(sys.argv) > 2 else 'serra'
print(f'(do Épico para cima, o grupo tem Vontade 80: sustenta o conjunto inteiro, 2.9) O DRAGÃO DA {tipo.upper()} ({N} lutas por linha; começa perto; o grupo de espada, malha e escudo; "misto": 2 espadas, 1 lança, 1 arco atrás)')
for idade, i in IDADES.items():
    f = ficha(dragao(tipo, idade))
    print(f"\n{idade}: grau {TB.GRAUS[min(6, i['cat'] + 1)]}, {T.CATS[i['cat']]}, {i['tamanho']}, nível {i['nivel']}, PV {f['pvmax']}, acerto {f['arma']['acerto']:+g}, Defesa {defesa(f):g}, fôlego {f['folmax']}, traços {', '.join(f['tracos'])}")
    c = i['cat']; n = REF[c]; V = {'Vontade': 80} if c >= 3 else {}
    D = lambda idade=idade: [dragao(tipo, idade)]
    um = grupo(1, n, c, c, atributos=V)
    r1 = grupo_contra(um, D, n=N, inicio='perto')
    print(f"  um homem do degrau (nível {n}, {T.CATS[c]}): vence {r1['vence']}% · morre {r1['mortos']:.2f}")
    for k in (4, 6):
        r = grupo_contra(grupo(k, n, c, c, atributos=V), D, n=N, inicio='perto')
        print(f"  {k} do degrau: vence {r['vence']}% · mortos por luta {r['mortos']:.2f} · alguém morre em {r['alguem_morre']}% · rodadas {r['rodadas']}")
    r = grupo_contra(grupo(4, n, c + 1, c + 1, atributos={'Vontade': 80}), D, n=N, inicio='perto')
    print(f"  4 do degrau com o conjunto uma acima ({T.CATS[c + 1]}): vence {r['vence']}% · mortos {r['mortos']:.2f} · alguém morre {r['alguem_morre']}%")
    if c >= 1:
        r = grupo_contra(grupo(4, n, c - 1, c - 1, atributos=V), D, n=N, inicio='perto')
        print(f"  4 do degrau com o conjunto uma abaixo ({T.CATS[c - 1]}): vence {r['vence']}% · mortos {r['mortos']:.2f} · alguém morre {r['alguem_morre']}%")
