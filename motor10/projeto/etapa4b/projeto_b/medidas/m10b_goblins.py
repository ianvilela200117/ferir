"""m10b: a luta da cena jogada, no save de hoje: a patrulha goblin (de faca, vê no escuro: noturno) na Mata do Corvo, DE NOITE.
Maro e Durva (a anã de passagem, proposta: vê no escuro emulado) contra Maro e Tomé (humano)."""
import sys, random
sys.path.insert(0, '/tmp/claude-0/-home-user-ferir/2caa978a-1aa4-5b05-88b7-11bcda935cb0/scratchpad/masmorras/projeto_b/medidas')
from m10_cena import maro, durva, tome, TRACOS_DE
import luta, criaturas
N = int(sys.argv[1]) if len(sys.argv) > 1 else 1500
for n in (3, 4):
    for rot, casa in (('Maro e Durva (vê no escuro)', lambda: [maro(), durva(True)]), ('Maro e Durva, sem o traço', lambda: [maro(), durva(False)]), ('Maro e Tomé (humano)', lambda: [maro(), tome()])):
        for tempo in ([], ['escuro']):
            luta.semente(9); v = mm = 0
            for i in range(N):
                S = luta.nova(casa(), criaturas.bando('goblin', random.Random(i), n=n), quieto=True, inicio='perto', tempo=tempo); luta.corre(S)
                v += S['fim'] == 'A'; mm += any(f['estado'] == 'morto' and f['nome'] == 'Maro' for f in S['L'])
            print(f"  {n} goblins · {rot:<30} {'de noite' if tempo else 'de dia  '}: a casa vence {100 * v / N:5.1f}% · Maro morre {100 * mm / N:4.1f}%")
