#!/usr/bin/env python3
"""festas.py — G36, AS FESTAS DO CALENDÁRIO (Livro Nove 15; MOTOR 9.1, Dia 438, pedido do jogador).

Uma festa por lua, das fés e das terras do Livro (01_mundo, seções 5 e 6). Toda festa tem EFEITO e PREÇO (Lei 2). O tick diário chama
"festas.py dia N": no dia da festa o script põe os modificadores nos pilares (reino.py mod, com prazo: vencem sozinhos), cobra do cofre o
que é da casa pagar (a Intendente paga pelo livro; o que tem dado sai pelo selo) e imprime o que fica À MÃO. Nada se aplica duas vezes.

Uso:
  python3 festas.py ver              o calendário das festas
  python3 festas.py proximas [N]     as N próximas, com o dia da campanha
  python3 festas.py dia DIA          o tick chama sozinho
"""
import subprocess, sys
from nucleo import carrega, grava, anota, dia_atual, calendario, P, LUAS

ARQ = 'festas.json'
# (lua, dia da lua, nome, de quem, efeito em texto, preço em texto, ações)
# ações: ('mod', cidades|'todas', pilar, valor, dias) · ('cofre', valor) · ('cofre_d6x20',) · ('rep', quem, valor) · ('obras', dias) · ('mao', texto)
FESTAS = [
 (1, 1, 'a Noite das Brasas', 'a Mão Queimada (Telosus e Ireviel)', 'as forjas ficam acesas a noite inteira: Ordem +1 em Ireviel por 7 dias; a obra de forja do rei nesta noite tem +2',
  'a fé pede o carvão da noite: 100', [('mod', ['Ireviel'], 'Ordem', 1, 7), ('cofre', -100), ('mao', 'NOITE DAS BRASAS: a obra de forja desta noite tem +2 (obra_valor.py mais=2)')]),
 (2, 15, 'a Caça do Lobo', 'o Céu Aberto e as aldeias do Vale do Leve', 'a missão da cidade da Guilda dos Aventureiros (G1) desta semana tem +2',
  'a caçada mexe a mata: com 1 natural na missão da cidade, um bicho Raro do bestiário desce perto de Ireviel', [('mao', 'CAÇA DO LOBO: a missão da cidade (G1) desta semana com +2; com 1 natural, um bicho Raro desce perto de Ireviel (gerar)')]),
 (3, 1, 'o Dia da Cinza', 'a Vigília (Zieth e Marasar), em memória da Febre', 'os vigilantes visitam os doentes: Saúde +1 no Porto de Marasar e em Levis por 7 dias',
  'a forja grande não acende neste dia (a série da semana sai um dia depois)', [('mod', ['o Porto de Marasar', 'Levis'], 'Saúde', 1, 7), ('mao', 'DIA DA CINZA: a forja grande não acende hoje')]),
 (4, 15, 'a Cheia do Rio', 'o Templo do Rio (Levis e o rio)', 'as barcas voltam: Comércio +1 em Levis e em Ireviel por 7 dias',
  'a oferenda aos mortos da água: 1d6 × 20 (sem ela, o Templo do Rio −5)', [('mod', ['Levis', 'Ireviel'], 'Comércio', 1, 7), ('cofre_d6x20', 'a oferenda da Cheia do Rio aos mortos da água')]),
 (5, 1, 'o Plantio', 'o Sono Verde e todo o campo', 'a semente vai à terra: Comida +1 em toda cidade por 7 dias',
  'neste dia não se corta árvore viva: o carvão da semana custa +50', [('mod', 'todas', 'Comida', 1, 7), ('cofre', -50)]),
 (6, 10, 'a Bênção das Barcas', 'os Filhos do Livro e as Velas (o rio e a costa)', 'Comércio +1 no Porto de Marasar e em Farenta por 7 dias',
  'a moeda das Velas a cada barqueiro do reino: 50', [('mod', ['o Porto de Marasar', 'Farenta'], 'Comércio', 1, 7), ('cofre', -50)]),
 (7, 1, 'a Feira do Sal', 'o Delta e as salinas', 'Dinheiro +1 em Ireviel por 7 dias; o estoque da cidade (G5) desta semana rola com +2',
  'a portagem do Delta dobra na semana: 100', [('mod', ['Ireviel'], 'Dinheiro', 1, 7), ('cofre', -100), ('mao', 'FEIRA DO SAL: o d20 do estoque da cidade (G5) desta semana com +2')]),
 (8, 1, 'o Concurso dos Mestres', 'Steunn (os mestres do bronze)', 'o rei pode mandar uma obra: Poder de Ofício contra os mestres (aberto.py oposto, melhor de três); vencendo, reputação +10 com Steunn e fama da casa +1',
  'a obra enviada fica em Steunn como prêmio da cidade, vença ou não', [('mao', 'CONCURSO DOS MESTRES de Steunn: o rei manda uma obra? (a obra fica lá; vencendo: reputacao.py muda Steunn +10 e guildas.py fama casa +1)')]),
 (9, 15, 'o Jejum da Areia', 'a Chama sob a Areia (os Eloulane de Yaelane)', 'os Eloulane não vendem nem deixam passar vaduar por 7 dias: as caravanas de Yaelane param',
  'quem quer vaduar nesta semana só acha o das minas de Levis e do Clã, mais caro', [('mao', 'JEJUM DA AREIA: 7 dias sem vaduar de Yaelane no mercado (o preço do vaduar sobe: mercado.py choque, se a casa comprar)')]),
 (10, 1, 'a Colheita', 'todo o reino', 'Comida +1 em toda cidade por 7 dias',
  'os braços vão ao campo: as obras do reino em andamento ficam 3 dias mais longas', [('mod', 'todas', 'Comida', 1, 7), ('obras', 3)]),
 (11, 1, 'os Jogos das Cidades', 'uma cidade grande (Livro Nove 13)', 'sete dias de trégua; quatro provas (o Duelo, a Forja, as Barcas, o Canto); vencer uma prova: título e reputação',
  'os inimigos também vêm à praça', [('mao', 'OS JOGOS DAS CIDADES (Livro Nove 13): qual cidade chama (o dado do evento de mundo) ou o rei paga 2.000 para chamar em Ireviel')]),
 (12, 1, 'a Noite das Velas', 'as Velas e o Templo do Rio (a costa e o rio)', 'cada casa acende uma vela pelos mortos do ano: Ordem +1 em toda cidade por 7 dias',
  'velas e esmolas: 1d6 × 20', [('mod', 'todas', 'Ordem', 1, 7), ('cofre_d6x20', 'as velas e as esmolas da Noite das Velas')]),
]


def roda(script, *args):
    r = subprocess.run([sys.executable, P(script)] + [str(x) for x in args], capture_output=True, text=True)
    out = (r.stdout + r.stderr).strip()
    if out: print('    ' + out.replace('\n', '\n    '))
    return out


def dia_da(ano, lua, dl):
    return 190 + (ano - 1013) * 365 + (lua - 1) * 30 + (dl - 1)


def proximas(dia, n):
    cal = calendario(dia); out = []
    for ano in (cal['ano'], cal['ano'] + 1):
        for f in FESTAS:
            dd = dia_da(ano, f[0], f[1])
            if dd >= dia: out.append((dd, f))
    return sorted(out, key=lambda x: x[0])[:n]


def main():
    a = sys.argv[1:]
    if not a or a[0] == 'ver':
        if not a: print(__doc__)
        print('AS FESTAS DO CALENDÁRIO (G36)')
        for f in FESTAS: print(f"  {f[1]} da Lua {LUAS[f[0] - 1]}: {f[2].upper()} ({f[3]}) · {f[4]} · PREÇO: {f[5]}")
        print('  os Dias Mudos (5, no fim do ano): não se acende forja grande, não se faz magia de 4º círculo para cima e não se casa (Livro, o calendário)')
        return
    if a[0] == 'proximas':
        n = int(a[1]) if len(a) > 1 else 4
        for dd, f in proximas(dia_atual(), n): print(f"  Dia {dd} ({calendario(dd)['txt']}): {f[2].upper()} · {f[4]} · PREÇO: {f[5]}")
        return
    if a[0] == 'dia' and len(a) > 1:
        dia = int(a[1]); cal = calendario(dia); S = carrega(ARQ, {'feitas': []})
        if cal.get('mudo'): return
        f = next((x for x in FESTAS if x[0] == cal['lua'] and x[1] == cal['dia_lua']), None)
        prox = proximas(dia + 1, 1)
        if not f:
            if prox and prox[0][0] - dia <= 3: print(f"  FESTA CHEGANDO: {prox[0][1][2]} no Dia {prox[0][0]} ({prox[0][1][3]})")
            return
        chave = f"{cal['ano']}-{f[0]}-{f[1]}"
        if chave in S['feitas']: print(f'  FESTA (já aplicada): {f[2]}'); return
        print(f"  ★ FESTA DE HOJE (G36): {f[2].upper()} ({f[3]}) · {f[4]} · PREÇO: {f[5]}")
        cids = [c['nome'] for c in carrega('reino.json')['cidades']]
        for ac in f[6]:
            if ac[0] == 'mod':
                for c in (cids if ac[1] == 'todas' else ac[1]): roda('reino.py', 'mod', c, ac[2], ac[3], f"FESTA: {f[2]} (até o {dia + ac[4] - 1})")
            elif ac[0] == 'cofre': roda('ficha.py', 'cofre', ac[1], f"FESTA: {f[2]} (G36)")
            elif ac[0] == 'cofre_d6x20':
                import selo
                Z = selo.load(); sid = selo.declara(Z, '-', f'{ac[1].upper()} (G36): 1d6 × 20', 'd6', '1: 20 | 2: 40 | 3: 60 | 4: 80 | 5: 100 | 6: 120', selo.opcoes([]), quieto=True)
                v = selo.rola(Z, sid, quieto=True)['rolagens'][-1]['total'] * 20; print(f'    {ac[1]}: d6 → {v}'); roda('ficha.py', 'cofre', -v, f"FESTA: {f[2]} (G36)")
            elif ac[0] == 'rep': roda('reputacao.py', 'muda', ac[1], ac[2], f"FESTA: {f[2]}")
            elif ac[0] == 'obras':
                R = carrega('reino.json'); n = 0
                for c in R['cidades']:
                    for o in c.get('obras', []): o['pronta'] = o['pronta'] + ac[1]; n += 1
                grava('reino.json', R); print(f'    {n} obra(s) do reino em andamento: +{ac[1]} dias (os braços foram ao campo)')
            elif ac[0] == 'mao': print('    À MÃO · ' + ac[1])
        S['feitas'].append(chave); grava(ARQ, S)
        anota(f"- FESTA (G36) [Dia {dia}]: {f[2]} ({f[3]}) · {f[4]} · PREÇO: {f[5]}")
        return
    print(__doc__)


if __name__ == '__main__':
    main()
