"""m5: a proposta final do dragão, medida: cada idade e cada tipo em casa (com a fúria), o que a categoria da peça faz, o corredor (o covil na masmorra) e o dragão dormindo (surpreendido)."""
import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-ferir/2caa978a-1aa4-5b05-88b7-11bcda935cb0/scratchpad/masmorras/projeto_b/medidas')
from dragoes_ensaio import *
import magia

N = int(sys.argv[1]) if len(sys.argv) > 1 else 300
parte = sys.argv[2] if len(sys.argv) > 2 else 'tudo'
# a proposta: os traços da idade (o velho e o ancião resistem à magia) e a fúria de cada tipo
IDADES['velho']['tracos'] = ['sopro', 'apavora', 'couraça', 'resiste']
IDADES['ancião']['tracos'] = ['sopro', 'apavora', 'couraça', 'resiste']
FURIA = {'serra': dict(abaixo=0.5, diz='a fúria: o fogo sobe pela garganta', ganha=['ardente']),
         'brejo': dict(abaixo=0.5, diz='a fúria: enrosca na lama', ganha=['agarra']),
         'grutas': dict(abaixo=0.5, diz='a fúria: bebe o sangue de quem prende', ganha=['dreno'])}
CASA = {'serra': {}, 'brejo': dict(tempo=['água']), 'grutas': dict(tempo=['escuro'])}


def D(tipo, idade, **mais):
    fs = [FURIA[tipo]] if idade != 'filhote' else None
    return lambda: [dragao(tipo, idade, fases=fs, **mais)]


def linha_(rot, r): print(f"  {rot:<60} vence {r['vence']:5.1f}% · mortos {r['mortos']:.2f} · alguém morre {r['alguem_morre']:5.1f}% · rodadas {r['rodadas']}")


if parte in ('tudo', 'idades'):
    for idade in IDADES:
        c = IDADES[idade]['cat']; n = REF[c]; V = {'Vontade': 80} if c >= 3 else {}
        f = ficha(dragao('serra', idade))
        print(f"\n{idade.upper()} (grau {TB.GRAUS[c + 1]}, {T.CATS[c]}, {IDADES[idade]['tamanho']}, nível {IDADES[idade]['nivel']}, PV {f['pvmax']}); o degrau: nível {n}, {T.CATS[c]}" + (', Vontade 80' if V else ''))
        for tipo in TIPOS:
            linha_(f'{tipo}, em casa: um homem do degrau', grupo_contra(grupo(1, n, c, c, atributos=V), D(tipo, idade), n=N, inicio='perto', **CASA[tipo]))
            linha_(f'{tipo}, em casa: 4 do degrau', grupo_contra(grupo(4, n, c, c, atributos=V), D(tipo, idade), n=N, inicio='perto', **CASA[tipo]))
            if c >= 2: linha_(f'{tipo}, em casa: 6 do degrau', grupo_contra(grupo(6, n, c, c, atributos=V), D(tipo, idade), n=N, inicio='perto', **CASA[tipo]))

if parte in ('tudo', 'jovem'):
    print('\nO JOVEM DA SERRA (com a fúria) contra o grupo de nível 50: o que a categoria da peça faz')
    J = D('serra', 'jovem')
    for rot, g in (('4, tudo Raro', grupo(4, 50, R, R)), ('4 misto (2 espadas, lança, arco atrás), tudo Raro', grupo(4, 50, R, R, misto=True)),
                   ('5, tudo Raro', grupo(5, 50, R, R)), ('6, tudo Raro', grupo(6, 50, R, R)),
                   ('4 com a ARMA Épica (o resto Raro)', lambda: [homem(f'h{i}', 50, arma=R + 1) for i in range(4)]),
                   ('4 com a armadura e o escudo Épicos (a arma Rara)', lambda: [homem(f'h{i}', 50, arm=R + 1) for i in range(4)]),
                   ('4, tudo Épico (Vontade 80)', grupo(4, 50, R + 1, R + 1, atributos={'Vontade': 80})),
                   ('4, tudo Incomum', grupo(4, 50, R - 1, R - 1)),
                   ('4 de nível 150, tudo Raro (o nível sem a peça)', grupo(4, 150, R, R))):
        linha_(rot, grupo_contra(g, J, n=N, inicio='perto'))
    print('\nO COVIL NA MASMORRA: o mesmo jovem (grande: toma 2 vagas) e o adulto (enorme: toma 3) num corredor; e dormindo (surpreendido: perde o primeiro turno)')
    linha_('jovem, 4 de nível 50 Raros, corredor de largura 2', grupo_contra(grupo(4, 50, R, R), J, n=N, inicio='perto', lugar=dict(largura=2)))
    linha_('jovem, 4 de nível 50 Raros, corredor de largura 1 (ele luta apertado)', grupo_contra(grupo(4, 50, R, R), J, n=N, inicio='perto', lugar=dict(largura=1)))
    linha_('jovem, 4 de nível 50 Raros, ele dormindo (surpreendido)', grupo_contra(grupo(4, 50, R, R), J, n=N, inicio='perto', surpresa='B'))
    linha_('jovem, 4 de nível 50 Raros, começa longe', grupo_contra(grupo(4, 50, R, R), J, n=N, inicio='longe'))
    A = D('serra', 'adulto'); g = grupo(4, 90, 3, 3, atributos={'Vontade': 80})
    linha_('adulto, 4 de nível 90 Épicos, campo aberto', grupo_contra(g, A, n=N, inicio='perto'))
    linha_('adulto, 4 de nível 90 Épicos, corredor de largura 2 (apertado)', grupo_contra(g, A, n=N, inicio='perto', lugar=dict(largura=2)))
    linha_('adulto, 4 de nível 90 Épicos, ele dormindo', grupo_contra(g, A, n=N, inicio='perto', surpresa='B'))
