"""mede_cacador_j.py — o caçador do banco (provas_caca: o mesmo robô, a mesma vida) numa mata que tem um covil: quanto cai a caça dele e quanto sobe o risco.
É a PARTE 3 do mede_covil.py dos projetistas anteriores, com outras ousadias (o goblin entra na contagem do ermo por procuração: dente e pelo Comuns, patrulha de 2 a 4)."""
import sys, random, statistics
sys.path.insert(0, '/tmp/claude-0/-home-user-ferir/2caa978a-1aa4-5b05-88b7-11bcda935cb0/scratchpad/magia/criaturas_mundo')
import mede_covil as MC
from mede_covil import *
def parte3(configs, vidas=80, dias=30):
    import provas_caca as PC
    TB.ESPECIES['goblin'] = TB._esp('goblin', 'o', 0, 'F', 8, 0, (46, 72, 46, 35, 61, 30), ['dente'], 'pelo', 'pequeno', [], -4, (2, 4), {'metal:0': 1, 'couro:0': 1}, ['floresta'], 'procuração de rascunho')
    cont = dict(enc=0)
    print(f'O CAÇADOR DO BANCO (nível 10, arco, conjunto Comum; o robô PRUDENTE do provas_caca), {vidas} vidas de {dias} dias na borda da floresta, com um covil de N goblins na mata')
    for ous, inv, n in configs:
        K.INDOLE['goblin'] = (ous, inv); Vs = []
        for s in range(1, vidas + 1):
            V = PC.caderno(); r = random.Random(900 + s)
            with PC.rascunho():
                fauna = dict(K.fauna('floresta', 1))
                if n: fauna['goblin'] = n
                E = PC.mundo(s, fauna=fauna); estado.grava(E); S = {}; dia0 = E['relogio']['dia']; cv = MC.covil_novo(cabecas=n); ac = caca.acaso(E, 'mata')
                while E['relogio']['dia'] <= dias and E['gente']['eu']['estado'] == 'vivo':
                    PC.um_passo(E, 'eu', V, PC.prudente, 'corça', S)
                    while dia0 < E['relogio']['dia']:
                        dia0 += 1
                        if n and not estado.luta_aberta(E): cv['cabecas'] = caca.bichos_de(E, 'mata').get('goblin', 0); MC.comer_so(E, cv, r)
                V['vivo'] = E['gente']['eu']['estado'] == 'vivo'; V['dias'] = dias if V['vivo'] else min(dias, E['relogio']['dia']); V['corca'] = caca.bichos_de(E, 'mata').get('corça', 0); V['gob'] = V['por_especie'].get('goblin', 0); V['ac'] = ac
            Vs.append(V)
        diarias = sum(v['valor'] for v in Vs) / sum(v['dias'] for v in Vs) / 4; sa = sum(v['saidas'] for v in Vs); fe = sum(v['feridas'] for v in Vs)
        print(f"  covil de {n:>2} (ousadia {ous:g}, investe {inv:.0%}; acaso de {100 * Vs[0]['ac']:.1f}% por bloco): {diarias:.2f} diárias por dia · ferido ou morto em {100 * fe / sa:.1f}% das saídas · morrem {sum(not v['vivo'] for v in Vs)} de {len(Vs)} ({100 * sum(not v['vivo'] for v in Vs) / len(Vs):.0f}%) · "
              f"lutas com goblins: {sum(v['gob'] for v in Vs)} · a corça no Dia {dias}: {statistics.mean(v['corca'] for v in Vs):.0f} de 80", flush=True)
if __name__ == '__main__':
    parte3(((0, 0.6, 0), (2.0, 0.6, 9), (2.0, 0.6, 16), (3.0, 0.6, 9)))
