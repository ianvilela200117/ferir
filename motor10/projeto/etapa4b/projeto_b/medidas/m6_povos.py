"""m6: a segunda volta dos povos: o duelo de espada (claro, escuro, arma uma acima, nível 5), a arma de cada povo (o arco do elfo, a adaga do pequenino), o veneno (a aranha-de-toca)."""
import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-ferir/2caa978a-1aa4-5b05-88b7-11bcda935cb0/scratchpad/masmorras/projeto_b/medidas')
from povos_v2 import *
N = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
so = sys.argv[2].split(',') if len(sys.argv) > 2 else [k for k in PE.POVOS if k != 'humano']
H = lambda **kw: (lambda: [de_povo2('humano', 'o rival', 50, **kw)])
print(f'nível 50, Raro ({N} lutas por linha). A régua: o Grande Dom vence o gêmeo 59,8% (4.000 lutas); contra a arma uma acima, até 15%.')
for pv in so:
    P = lambda **kw: (lambda: [de_povo2(pv, pv, 50, **kw)])
    a = duelo(P(), H(), n=N, inicio='perto')[0]
    b = duelo(P(), H(), n=N, inicio='perto', tempo=['escuro'])[0]
    c = duelo(P(), H(arma=R + 1), n=N, inicio='perto')[0]
    d = duelo(lambda: [de_povo2(pv, pv, 5, arma=0, arm=0)], lambda: [de_povo2('humano', 'o rival', 5, arma=0, arm=0)], n=N, inicio='perto')[0]
    e = duelo(lambda: [de_povo2(pv, pv, 50, familia='arco', material='couro', molde='arqueiro')], lambda: [de_povo2('humano', 'o rival', 50, familia='arco', material='couro', molde='arqueiro')], n=N, inicio='longe')[0]
    f = duelo(lambda: [de_povo2(pv, pv, 50, familia='adaga', material='couro')], lambda: [de_povo2('humano', 'o rival', 50, familia='adaga', material='couro')], n=N, inicio='perto')[0]
    print(f'  {pv:<10} espada: {a:5.1f}% · no escuro {b:5.1f}% · contra a arma uma acima {c:5.1f}% · nível 5 Comum {d:5.1f}% · arco contra arco, de longe {e:5.1f}% · adaga e couro {f:5.1f}%')
# o veneno: cada um sozinho contra a aranha-de-toca (C, Raro, veneno), e a régua do Grande Dom
print('\nCONTRA A ARANHA-DE-TOCA (Rara, veneno), um homem de nível 50, espada, malha e escudo Raros:')
for pv in ['humano'] + so:
    r = duelo(lambda: [de_povo2(pv, pv, 50)], lambda: [bichos.bicho('aranha')], n=N, inicio='perto')[0]
    print(f'  {pv:<10} vence {r:5.1f}%')
r = duelo(lambda: [homem('gd', 50, dom={'fio': 2})], lambda: [bichos.bicho('aranha')], n=N, inicio='perto')[0]
print(f'  o humano com o Grande Dom no fio: {r:5.1f}%')
