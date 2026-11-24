"""m3_chefe.py: o chefe do fundo da cripta de teste (candidatos), contra o grupo do Maro de hoje (cópia do ensaio): Maro, Tomé e Rute; e com Anselmo ou Lúcia.
E o golpe pelas costas (a proposta de luta do ladino), medido contra o gêmeo e contra a arma uma acima."""
import sys
from med_comum import *
import luta as LU, tabelas_bichos as TB

N = int(sys.argv[1]) if len(sys.argv) > 1 else 400
L = []
def m(nome, fa, fb, **kw):
    R = duelos(fa, fb, N, **kw); L.append(diz(nome, R)); print(L[-1], flush=True); return R

def guardiao(cat=1, nivel=30, maestria=4, fases=True, ergue=2, montante=True):
    g = CR.criatura('cavaleiro-da-cova', nome='o guardião da cripta', cat=cat, nivel=nivel, maestria=maestria)
    g.update(lider=True, chefe=True)
    if fases: g['fases'] = [dict(abaixo=0.5, diz='bate o pé no chão de pedra: os ossos da sala se levantam', ergue=ergue, brado=True)]
    return g

def com_lacaios(n_esq=2, **k):
    return lambda i: [guardiao(**k)] + CR.bando('esqueleto', n=n_esq)

maro = lambda: cheio('eu', controla=True)
G3 = lambda: [maro(), cheio('tome'), cheio('rute', linha='trás')]
G4a = lambda: [maro(), cheio('tome'), cheio('rute', linha='trás'), cheio('anselmo', linha='trás')]
G4l = lambda: [maro(), cheio('tome'), cheio('lucia'), cheio('rute', linha='trás')]

print('== O GUARDIÃO DA CRIPTA (cavaleiro da cova Incomum: montante e placa Incomuns, nível 30, Treinado; abaixo de metade do PV ergue 2 mortos e dá o brado) ==')
m('grupo de 3 contra o guardião e 2 esqueletos, sala de 2, com luz', G3, com_lacaios(2), inicio='perto', lugar=dict(largura=2))
m('grupo de 3 contra o guardião e 2 esqueletos, sala aberta, com luz', G3, com_lacaios(2), inicio='perto')
m('grupo de 3 contra o guardião sozinho (sem fases), sala aberta', G3, lambda i: [guardiao(fases=False)], inicio='perto')
m('grupo de 4 (com Anselmo) contra o guardião e 2 esqueletos, sala aberta', G4a, com_lacaios(2), inicio='perto')
m('grupo de 4 (com Lúcia) contra o guardião e 2 esqueletos, sala aberta', G4l, com_lacaios(2), inicio='perto')
m('grupo de 3 contra o guardião (nível 20, Iniciante) e 2 esqueletos, sala aberta', G3, com_lacaios(2, nivel=20, maestria=2), inicio='perto')
m('grupo de 3 contra o guardião (nível 20, Iniciante) e 2 esqueletos, NO ESCURO', G3, com_lacaios(2, nivel=20, maestria=2), inicio='perto', tempo=['escuro'])
for nv, ms in ((20, 2), (25, 4), (30, 4)):
    m(f'grupo de 3 contra o guardião COMUM (nível {nv}, maestria {ms}) e 2 esqueletos, sala aberta', G3, com_lacaios(2, cat=0, nivel=nv, maestria=ms), inicio='perto')
    m(f'grupo de 3 contra o guardião COMUM (nível {nv}, maestria {ms}) e 2 esqueletos, sala de 2', G3, com_lacaios(2, cat=0, nivel=nv, maestria=ms), inicio='perto', lugar=dict(largura=2))
    m(f'grupo de 3 contra o guardião COMUM (nível {nv}, maestria {ms}) e 2 esqueletos, NO ESCURO', G3, com_lacaios(2, cat=0, nivel=nv, maestria=ms), inicio='perto', tempo=['escuro'])
    m(f'grupo de 4 (com Anselmo) contra o guardião COMUM (nível {nv}, maestria {ms}) e 2 esqueletos, sala aberta', G4a, com_lacaios(2, cat=0, nivel=nv, maestria=ms), inicio='perto')
    m(f'Maro e Tomé contra o guardião COMUM (nível {nv}, maestria {ms}) e 2 esqueletos, sala aberta', lambda: [maro(), cheio('tome')], com_lacaios(2, cat=0, nivel=nv, maestria=ms), inicio='perto')
m('Maro sozinho contra o guardião COMUM (nível 25, Treinado), sem lacaios', lambda: [maro()], lambda i: [guardiao(cat=0, nivel=25, maestria=4, fases=False)], inicio='perto')
m('Maro sozinho contra o guardião (nível 20, Iniciante), sem lacaios', lambda: [maro()], lambda i: [guardiao(nivel=20, maestria=2, fases=False)], inicio='perto')

# ---------- o golpe pelas costas (a proposta): o primeiro golpe de quem tem manha de Treinado contra quem foi surpreendido rola os dados 3 vezes, com +4 ----------
_orig = LU._golpe_especial
COSTAS = {}
def _pelas_costas(S, a, w, livre):
    r = _orig(S, a, w, livre)
    if r: return r
    c = COSTAS.get(a['nome'])
    if c and not w['distancia'] and not livre and 'costas' not in a['usou'] and S['r'] == 1 and S.get('surpresa') and S['surpresa'] != a['lado']:
        a['usou'].append('costas'); return dict(nome='pelas costas', acerto=c[0], dados=c[1])
    return None

def ladino(nome, cat=2, costas=None, nivel=50, familia='espada'):
    p = veste(padrao(nome, nivel, molde='arqueiro'), arma=(familia, cat), armadura=('couro', cat), escudo=None if familia != 'espada' else None)
    return p

def gemeo(nome, cat=2, nivel=50):
    return veste(padrao(nome, nivel), arma=('espada', cat), armadura=('malha', cat), escudo=cat)

print('\n== O GOLPE PELAS COSTAS (nível 50, o ladino de espada e couro; o outro de espada, malha e escudo; o outro lado foi surpreendido) ==')
for costas in (None, (4, 2), (4, 3), (8, 3)):
    LU._golpe_especial = _pelas_costas; COSTAS.clear()
    if costas: COSTAS['Ladino'] = costas
    tag = 'sem o golpe' if not costas else f'+{costas[0]} e os dados {costas[1]} vezes'
    m(f'ladino Raro surpreende o gêmeo Raro ({tag})', lambda: [ladino('Ladino', 2, costas)], lambda i: [gemeo('Outro', 2)], inicio='colado', surpresa='B')
    m(f'ladino Raro surpreende o outro de arma Épica ({tag})', lambda: [ladino('Ladino', 2, costas)], lambda i: [veste(padrao('Outro', 50), arma=('espada', 3), armadura=('malha', 2), escudo=2)], inicio='colado', surpresa='B')
    m(f'ladino Raro surpreende o outro de conjunto Épico ({tag})', lambda: [ladino('Ladino', 2, costas)], lambda i: [gemeo('Outro', 3)], inicio='colado', surpresa='B')
    m(f'ladino Raro, de adaga, surpreende o gêmeo Raro ({tag})', lambda: [ladino('Ladino', 2, costas, familia='adaga')], lambda i: [gemeo('Outro', 2)], inicio='colado', surpresa='B')
LU._golpe_especial = _orig
m('sem surpresa nenhuma: ladino Raro contra o gêmeo Raro', lambda: [ladino('Ladino', 2)], lambda i: [gemeo('Outro', 2)], inicio='colado')
open('m3_saida.txt', 'w').write('\n'.join(L) + '\n')
