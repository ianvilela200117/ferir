"""m6_cena.py: as lutas da cena jogada (seção 8), com semente fixa: o grupo no corredor dos nichos e na câmara do guardião"""
import sys
from med_comum import *
sys.path.insert(0, '.')

def quim():
    p = padrao('Quim', 14, molde='arqueiro', maestria={'adaga': 2}); veste(p, arma=('adaga', 0), armadura=('couro', 0), elmo=False)
    return p
def guardiao():
    g = CR.criatura('cavaleiro-da-cova', nome='o guardião da cripta', cat=0, nivel=25, maestria=4); g.update(lider=True, chefe=True)
    g['fases'] = [dict(abaixo=0.5, diz='bate o pé: os ossos da sala se levantam', ergue=2, brado=True)]
    return g
sem = int(sys.argv[1]) if len(sys.argv) > 1 else 4
luta.semente(sem)
A = [cheio('tome'), cheio('eu', controla=True), dict(quim(), linha='trás'), cheio('rute', linha='trás')]
S = luta.nova(A, CR.bando('corpo-seco', n=2), inicio='perto', lugar=dict(largura=1), tempo=[]); luta.corre(S)
print('\n'.join(S['log'][:60])); print(luta.resultado_diz(S))
print('---')
for f in S['L']: print(f['nome'], f['estado'], f['pv'], '/', f['pvmax'])
pv = {f['nome']: f['pv'] for f in S['L'] if f['lado'] == 'A'}
A2 = [cheio('tome'), cheio('eu', controla=True), dict(quim(), linha='trás'), cheio('rute', linha='trás')]
for a in A2:
    if a['nome'] in pv: a['pv'] = max(1, pv[a['nome']])
luta.semente(sem + 100)
S2 = luta.nova(A2, [guardiao()] + CR.bando('esqueleto', n=2), inicio='perto', lugar=dict(largura=2), tempo=[]); luta.corre(S2)
print('=== GUARDIÃO ==='); print('\n'.join(S2['log'][:120])); print(luta.resultado_diz(S2))
for f in S2['L']: print(f['nome'], f['estado'], f['pv'], '/', f['pvmax'])

