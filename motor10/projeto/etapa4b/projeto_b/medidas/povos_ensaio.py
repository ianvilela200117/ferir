"""povos_ensaio.py: os povos candidatos, montados sobre o motor de hoje SEM mexer nele (o que falta na luta é emulado aqui, por embrulho, só para medir):
  'vê no escuro' (o escuro tira a METADE: −2 no golpe, −4 no tiro) · 'resiste a veneno' (o veneno do corpo tira a metade por rodada).
A soma dos seis atributos de cada povo é zero."""
import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-ferir/2caa978a-1aa4-5b05-88b7-11bcda935cb0/scratchpad/masmorras/projeto_b/medidas')
from base_b import *

POVOS = {
    'humano':    dict(mods={}, tracos=[]),
    'anão':      dict(mods={'Vigor': 10, 'Vontade': 5, 'Agilidade': -5, 'Percepção': -5, 'Afinidade': -5}, tracos=['vê no escuro', 'resiste a veneno']),
    'elfo':      dict(mods={'Agilidade': 10, 'Percepção': 10, 'Afinidade': 5, 'Vigor': -10, 'Força': -5, 'Vontade': -10}, tracos=[]),
    'meio-orc':  dict(mods={'Força': 10, 'Vigor': 5, 'Afinidade': -10, 'Vontade': -5}, tracos=['vê no escuro']),
    'pequenino': dict(mods={'Força': -15, 'Vigor': -5, 'Agilidade': 10, 'Percepção': 5, 'Vontade': 5}, tracos=['resiste a veneno']),
    'gnomo':     dict(mods={'Afinidade': 10, 'Percepção': 5, 'Vontade': 5, 'Força': -10, 'Vigor': -5, 'Agilidade': -5}, tracos=['vê no escuro']),
}
for k, d in POVOS.items(): assert sum(d['mods'].values()) == 0, k

# --- o que a luta ainda não roda, emulado por embrulho do golpe (só para medir) ---
_golpe = luta.golpe
TRACOS_DE = {}          # nome do lutador -> traços do povo


def _golpe_povo(S, a, e, w, livre=''):
    ta, te = TRACOS_DE.get(a['nome'], ()), TRACOS_DE.get(e['nome'], ())
    guarda_t, guarda_v = dict(T.TEMPO['escuro']), dict(TB.VENENO)
    try:
        if 'vê no escuro' in ta and 'escuro' in S['tempo']: T.TEMPO['escuro'] = dict(acerto=-2, tiro=-4)
        if 'resiste a veneno' in te: TB.VENENO['fracao'] = guarda_v['fracao'] / 2
        return _golpe(S, a, e, w, livre)
    finally:
        T.TEMPO['escuro'] = guarda_t; TB.VENENO.clear(); TB.VENENO.update(guarda_v)


luta.golpe = _golpe_povo


def de_povo(povo, nome, nivel, **kw):
    d = POVOS[povo]; p = homem(nome, nivel, mods=d['mods'], **kw); TRACOS_DE[nome] = list(d['tracos'])
    return p
