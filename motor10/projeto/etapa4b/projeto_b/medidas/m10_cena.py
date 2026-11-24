"""m10: a luta da cena jogada. Maro (o guerreiro de nível 5 da vila de teste) e um companheiro contra três esqueletos da Cova Velha, DE NOITE (escuro).
O companheiro: Durva, a anã ferreira de passagem (proposta), com e sem o 'vê no escuro'; ou Tomé, o guarda (humano), como a vila de teste o tem."""
import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-ferir/2caa978a-1aa4-5b05-88b7-11bcda935cb0/scratchpad/masmorras/projeto_b/medidas')
from povos_v2 import *
import criaturas
import vila_teste as V

N = int(sys.argv[1]) if len(sys.argv) > 1 else 1000


def maro():
    c = V.COMECOS['guerreiro']
    return veste(dict(nome='Maro', nivel=V.NIVEL, atributos=dict(c['atributos']), maestria=dict(c['maestria']), equip={}), arma=('espada', 0), armadura=('malha', 0), escudo=0, elmo=False)


def durva(ve=True):
    p = padrao('Durva', 34, molde='guerreiro', maestria={'martelo': 4})
    for k, v in PE.POVOS['anão']['mods'].items(): p['atributos'][k] += v
    veste(p, arma=('martelo', 1), armadura=('couro', 1), elmo=False)
    TRACOS_DE['Durva'] = list(PE.POVOS['anão']['tracos']) if ve else []
    return p


def tome():
    p = padrao('Tomé', 30, molde='guerreiro', maestria={'lança': 4})
    return veste(p, arma=('lança', 1), armadura=('malha', 0), escudo=0)


if __name__ == "__main__":
    esq = lambda: [criaturas.criatura('esqueleto', nome=f'esqueleto {i + 1}') for i in range(3)]
    for rot, casa in (('Maro sozinho', lambda: [maro()]), ('Maro e Durva (vê no escuro)', lambda: [maro(), durva(True)]),
                      ('Maro e Durva, sem o traço (o mesmo corpo de anã)', lambda: [maro(), durva(False)]), ('Maro e Tomé (humano)', lambda: [maro(), tome()])):
        for tempo in ([], ['escuro']):
            luta.semente(5); v = mm = 0
            for _ in range(N):
                S = luta.nova(casa(), esq(), quieto=True, inicio='perto', tempo=tempo); luta.corre(S)
                v += S['fim'] == 'A'; mm += any(f['estado'] == 'morto' and f['nome'] == 'Maro' for f in S['L'])
            print(f"  {rot:<50} {'de noite' if tempo else 'de dia  '}: a casa vence {100 * v / N:5.1f}% · Maro morre {100 * mm / N:4.1f}%")
