"""m11: A PROPOSTA FINAL DO DRAGÃO, medida de uma vez (para as tabelas do PROJETO.md).
Os traços da idade; a fase de cada tipo (a serra: abaixo de 30%, no covil desce em fúria (perde 'voa', ganha 'ardente'), fora dele foge pelo ar; o brejo: abaixo de 50% enrosca
(ganha 'agarra'); as grutas: abaixo de 50% bebe o sangue (ganha 'dreno')). Em casa: o covil é "sem saída" para o dragão; o brejo luta na água; as grutas no escuro.
A fase "foge" não existe no motor: aqui é emulada por embrulho do magia.fase (o que a construção faria)."""
import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-ferir/2caa978a-1aa4-5b05-88b7-11bcda935cb0/scratchpad/masmorras/projeto_b/medidas')
from dragoes_ensaio import *
import magia

N = int(sys.argv[1]) if len(sys.argv) > 1 else 600
parte = sys.argv[2] if len(sys.argv) > 2 else 'tudo'
IDADES['velho']['tracos'] = ['sopro', 'apavora', 'couraça', 'resiste']
IDADES['ancião']['tracos'] = ['sopro', 'apavora', 'couraça', 'resiste']
FASE = {'serra': [dict(abaixo=0.3, diz='desce ao chão em fúria', perde=['voa'], ganha=['ardente'], foge=True)],
        'brejo': [dict(abaixo=0.5, diz='enrosca na lama', ganha=['agarra'])],
        'grutas': [dict(abaixo=0.5, diz='bebe o sangue de quem prende', ganha=['dreno'])]}
COVIL = {'serra': dict(lugar=dict(sem_saida='B')), 'brejo': dict(lugar=dict(sem_saida='B'), tempo=['água']), 'grutas': dict(lugar=dict(sem_saida='B'), tempo=['escuro'])}
_fase = magia.fase; CONTA = {'fugiu': 0}


def _fase_b(S, e):
    """a fase com "foge": se o dragão voa, não está num corredor e não está no covil (sem saída), foge pelo ar em vez de mudar"""
    i0 = e.get('fase', 0)
    for i, fs in enumerate(e.get('fases') or [], 1):
        if i <= i0 or e['estado'] != 'pe' or e['pv'] > e['pvmax'] * fs.get('abaixo', 0): continue
        if fs.get('foge') and luta.tem(e, 'voa') and not S['lugar'].get('largura') and S['lugar'].get('sem_saida') != e['lado']:
            e['fase'] = i; e['estado'] = 'fugiu'; CONTA['fugiu'] += 1; luta.diz(S, f"  ◆ {e['nome']} FOGE pelo ar, ferido"); luta._fim(S); return
    _fase(S, e)


magia.fase = _fase_b
D = lambda tipo, idade: (lambda: [dragao(tipo, idade, fases=FASE[tipo] if idade != 'filhote' else None)])


def lin(rot, r, extra=''): print(f"  {rot:<64} vence {r['vence']:5.1f}% · mortos por luta {r['mortos']:.2f} · alguém morre {r['alguem_morre']:5.1f}% · rodadas {r['rodadas']}{extra}")


if parte in ('tudo', 'idades'):
    print(f'AS IDADES E OS TIPOS, EM CASA ({N} lutas por linha; do Épico para cima o grupo tem Vontade 80)')
    for idade in IDADES:
        c = IDADES[idade]['cat']; n = REF[c]; V = {'Vontade': 80} if c >= 3 else {}
        f = ficha(dragao('serra', idade))
        print(f"\n{idade.upper()}: grau {TB.GRAUS[c + 1]}, {T.CATS[c]}, {IDADES[idade]['tamanho']}, nível {IDADES[idade]['nivel']}, PV {f['pvmax']}, acerto {f['arma']['acerto']:+g}, Defesa {defesa(f):g}; o degrau: nível {n}, {T.CATS[c]}")
        for tipo in TIPOS:
            kw = COVIL[tipo]
            if idade == 'filhote': lin(f'{tipo}: um homem do degrau', grupo_contra(grupo(1, n, c, c), D(tipo, idade), n=N, inicio='perto', **kw)); continue
            lin(f'{tipo}: 4 do degrau', grupo_contra(grupo(4, n, c, c, atributos=V), D(tipo, idade), n=N, inicio='perto', **kw))
            lin(f'{tipo}: 6 do degrau', grupo_contra(grupo(6, n, c, c, atributos=V), D(tipo, idade), n=N, inicio='perto', **kw))
            lin(f'{tipo}: 4 do degrau, o conjunto uma acima', grupo_contra(grupo(4, n, c + 1, c + 1, atributos={'Vontade': 80}), D(tipo, idade), n=N // 2, inicio='perto', **kw))
            lin(f'{tipo}: 4 do degrau, o conjunto uma abaixo', grupo_contra(grupo(4, n, c - 1, c - 1, atributos=V), D(tipo, idade), n=N // 2, inicio='perto', **kw))
            lin(f'{tipo}: um homem do degrau', grupo_contra(grupo(1, n, c, c, atributos=V), D(tipo, idade), n=N // 2, inicio='perto', **kw))

if parte in ('tudo', 'jovem'):
    print(f'\nO JOVEM DA SERRA CONTRA O GRUPO DE NÍVEL 50 ({N} lutas por linha)')
    J = D('serra', 'jovem'); cov = COVIL['serra']
    for rot, g, kw in (('no covil: 4, tudo Raro', grupo(4, 50, R, R), cov), ('no covil: 4 misto (2 espadas, lança, arco atrás)', grupo(4, 50, R, R, misto=True), cov),
                       ('no covil: 5, tudo Raro', grupo(5, 50, R, R), cov), ('no covil: 6, tudo Raro', grupo(6, 50, R, R), cov),
                       ('no covil: 4 com a ARMA Épica (o resto Raro)', lambda: [homem(f'h{i}', 50, arma=R + 1) for i in range(4)], cov),
                       ('no covil: 4 com a armadura e o escudo Épicos', lambda: [homem(f'h{i}', 50, arm=R + 1) for i in range(4)], cov),
                       ('no covil: 4, tudo Épico (Vontade 80)', grupo(4, 50, R + 1, R + 1, atributos={'Vontade': 80}), cov),
                       ('no covil: 4, tudo Incomum', grupo(4, 50, R - 1, R - 1), cov),
                       ('no covil, ele dormindo (surpreendido): 4, tudo Raro', grupo(4, 50, R, R), dict(cov, surpresa='B')),
                       ('no covil, num corredor de largura 2: 4, tudo Raro', grupo(4, 50, R, R), dict(lugar=dict(sem_saida='B', largura=2))),
                       ('fora do covil (campo aberto; ele foge ferido): 4, tudo Raro', grupo(4, 50, R, R), {})):
        CONTA['fugiu'] = 0; nn = N
        r = grupo_contra(g, J, n=nn, inicio='perto', **kw)
        lin(rot, r, f" · ele fugiu em {round(100 * CONTA['fugiu'] / nn)}%" if CONTA['fugiu'] else '')
