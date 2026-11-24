"""m4: as fases do dragão (o que a luta já roda: ganhar traço, aprender feitiço, recobrar Mana) e a fase que falta ("foge": emulada aqui por embrulho do magia.fase).
Mede o jovem e o adulto contra o grupo do degrau, cada tipo na casa dele: a serra ao ar livre, o brejo na água, as grutas no escuro."""
import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-ferir/2caa978a-1aa4-5b05-88b7-11bcda935cb0/scratchpad/masmorras/projeto_b/medidas')
from dragoes_ensaio import *
import magia

N = int(sys.argv[1]) if len(sys.argv) > 1 else 400
_fase = magia.fase
FUGIU = {'n': 0}


def _fase_foge(S, e):
    antes = e.get('fase', 0); _fase(S, e); i = e.get('fase', 0)
    if i > antes and e['fases'][i - 1].get('foge') and luta.tem(e, 'voa') and not S['lugar'].get('largura') and S['lugar'].get('sem_saida') != e['lado'] and e['estado'] == 'pe':
        e['estado'] = 'fugiu'; FUGIU['n'] += 1; luta.diz(S, f"    {e['nome']} FOGE pelo ar, ferido"); luta._fim(S)


magia.fase = _fase_foge
FURIA = {'serra': dict(abaixo=0.5, diz='a fúria: o fogo sobe pela garganta', ganha=['ardente']),
         'brejo': dict(abaixo=0.5, diz='a fúria: afunda na lama e a carne fecha', ganha=['regenera']),
         'grutas': dict(abaixo=0.5, diz='a fúria: enrosca e não solta', ganha=['dreno'])}
CASA = {'serra': {}, 'brejo': dict(tempo=['água']), 'grutas': dict(tempo=['escuro'])}

for idade in ('jovem', 'adulto'):
    c = IDADES[idade]['cat']; n = REF[c]; V = {'Vontade': 80} if c >= 3 else {}
    g4 = grupo(4, n, c, c, atributos=V)
    print(f'\n{idade.upper()} contra 4 do degrau (nível {n}, {T.CATS[c]}), {N} lutas por linha, começa perto')
    for tipo in ('serra', 'brejo', 'grutas'):
        for rot, fases, kw in (('sem fase, ao ar livre e com luz', None, {}), ('sem fase, em casa', None, CASA[tipo]),
                               ('com a fúria a 50%, em casa', [FURIA[tipo]], CASA[tipo]),
                               ('fúria a 50% e foge a 25% (fora do covil)', [FURIA[tipo], dict(abaixo=0.25, diz='foge', foge=True)], CASA[tipo])):
            FUGIU['n'] = 0
            r = grupo_contra(g4, lambda: [dragao(tipo, idade, fases=fases)], n=N, inicio='perto', **kw)
            print(f"  {tipo:<7} {rot:<42} vence {r['vence']:5.1f}% · mortos {r['mortos']:.2f} · alguém morre {r['alguem_morre']:5.1f}% · rodadas {r['rodadas']}" + (f" · fugiu em {round(100 * FUGIU['n'] / N)}%" if FUGIU['n'] else ''))
