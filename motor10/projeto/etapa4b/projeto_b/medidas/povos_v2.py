"""povos_v2.py: os povos da segunda volta (a soma dos atributos é zero), com a coragem do povo emulada por embrulho do luta.nova (só para medir)."""
import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-ferir/2caa978a-1aa4-5b05-88b7-11bcda935cb0/scratchpad/masmorras/projeto_b/medidas')
import povos_ensaio as PE
from povos_ensaio import *

PE.POVOS.clear()
PE.POVOS.update({
    'humano':    dict(mods={}, tracos=[], coragem=0),
    'anão':      dict(mods={'Vigor': 5, 'Vontade': 5, 'Agilidade': -5, 'Percepção': -5}, tracos=['vê no escuro', 'resiste a veneno'], coragem=0),
    'elfo':      dict(mods={'Agilidade': 10, 'Percepção': 10, 'Afinidade': 5, 'Vigor': -5, 'Força': -10, 'Vontade': -10}, tracos=['vê no escuro'], coragem=0),
    'meio-orc':  dict(mods={'Força': 10, 'Vigor': 5, 'Afinidade': -10, 'Vontade': -5}, tracos=['vê no escuro'], coragem=0),
    'pequenino': dict(mods={'Força': -15, 'Agilidade': 5, 'Percepção': 5, 'Vontade': 5}, tracos=[], coragem=4),
    'gnomo':     dict(mods={'Afinidade': 10, 'Percepção': 5, 'Força': -10, 'Vigor': -5}, tracos=['vê no escuro'], coragem=0),
})
for k, d in PE.POVOS.items(): assert sum(d['mods'].values()) == 0, k
COR = {}
_nova = luta.nova


def _nova_cor(*a, **kw):
    S = _nova(*a, **kw)
    for f in S['L']:
        if f['nome'] in COR: f['coragem'] = COR[f['nome']]
    return S


luta.nova = _nova_cor


def de_povo2(povo, nome, nivel, **kw):
    p = de_povo(povo, nome, nivel, **kw); COR[nome] = PE.POVOS[povo]['coragem']
    return p
