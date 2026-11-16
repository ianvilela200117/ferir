#!/usr/bin/env python3
"""masmorra.py — G14, AS MASMORRAS POR SALAS (Dia 433, pedido do jogador).

Um lugar fechado (Ithium, Alnesar, Quoium, Eryssa, Iroule...) vira um mapa de 5 a 9 SALAS, geradas no dado na
primeira vez que alguém da casa entra (ou antes, se a casa mandar olhos). A última sala é O CORAÇÃO: o que o lugar
guarda, com o guardião dele. Cada sala, d20:
  1-4   VAZIA: um rastro (pegada, osso, inscrição gasta) que diz algo do lugar
  5-8   PERIGO: um bicho ou guarda (um degrau abaixo da categoria do lugar; o Mestre monta a luta pela G9)
  9-11  ARMADILHA: notar contra CD 15 + o degrau do lugar × 2; falha: o dano do degrau e uma CONDIÇÃO (G16)
  12-14 SEGREDO: porta escondida, passagem, inscrição (saber.py) que abre um atalho ou explica o lugar
  15-17 TESOURO (G17, pelo degrau do lugar)
  18-19 O QUE HABITA o lugar (os mortos, o culto, o bando): encontro; pode ser conversa
  20    SURPRESA (gerador novidade)
Caminho: cada sala leva à seguinte; com 6 no d6 há um DESVIO (a sala liga também a uma mais adiante).
O mapa fica em masmorras/NOME.json; o dado é anotado no envelope como OCULTO (a casa só vê a sala em que entrou).

Uso:
  python3 masmorra.py gera NOME CAT ["o que guarda"] [salas=N]   CAT: Comum Incomum Raro Epico Unico Lendario Mitico
  python3 masmorra.py ver NOME [tudo]                            o que a casa já viu (com "tudo": o mapa inteiro, só o Mestre)
  python3 masmorra.py entra NOME SALA                            marca a sala como vista
"""
import json, os, sys
from nucleo import d, anota, dia_atual, P

DEGRAU = {'comum': 0, 'incomum': 1, 'raro': 2, 'epico': 3, 'unico': 4, 'lendario': 5, 'mitico': 6, 'primordial': 7}
NOMECAT = ['Comum', 'Incomum', 'Raro', 'Épico', 'Único', 'Lendário', 'Mítico', 'Primordial']
DANO = ['1d6', '2d6', '3d6', '4d6', '6d6', '8d6', '12d6', '20d6']


def tipo(r, g):
    if r <= 4: return 'VAZIA (um rastro)'
    if r <= 8: return f'PERIGO: um bicho ou guarda {NOMECAT[max(g - 1, 0)]}'
    if r <= 11: return f'ARMADILHA: notar CD {15 + g * 2}; falha: {DANO[g]} e uma condição (G16)'
    if r <= 14: return 'SEGREDO (porta, passagem ou inscrição)'
    if r <= 17: return f'TESOURO (G17, degrau {NOMECAT[g]})'
    if r <= 19: return 'O QUE HABITA o lugar (encontro; pode ser conversa)'
    return 'SURPRESA (gerador novidade)'


def arq(nome):
    os.makedirs(P('masmorras'), exist_ok=True)
    return P('masmorras', nome.lower().replace(' ', '_') + '.json')


def gera(nome, cat, guarda, n):
    g = DEGRAU[cat.lower().replace('é', 'e').replace('ú', 'u').replace('í', 'i')]
    if os.path.exists(arq(nome)):
        sys.exit(f'{nome} já tem mapa (masmorra.py ver {nome} tudo). Não se gera duas vezes.')
    n = n or (4 + d(5))
    salas = []
    for i in range(1, n):
        r = d(20); desvio = d(6) == 6 and i < n - 1
        salas.append({'n': i, 'dado': r, 'o_que': tipo(r, g), 'leva_a': [i + 1] + ([min(n, i + 1 + d(2))] if desvio else []), 'vista': False})
    salas.append({'n': n, 'dado': None, 'o_que': f'O CORAÇÃO: {guarda or "o que o lugar guarda"}, com o guardião ({NOMECAT[g]})', 'leva_a': [], 'vista': False})
    M = {'nome': nome, 'cat': NOMECAT[g], 'guarda': guarda, 'gerada': dia_atual(), 'salas': salas}
    json.dump(M, open(arq(nome), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    linhas = ' · '.join(f"{s['n']}{'[' + str(s['dado']) + ']' if s['dado'] else ''} {s['o_que']}" + (f" (→ {','.join(map(str, s['leva_a']))})" if len(s['leva_a']) > 1 else '') for s in salas)
    anota(f"- (OCULTO) MASMORRA {nome} ({NOMECAT[g]}; G14), {n} salas, d20 por sala: {linhas}")
    print(f'MASMORRA {nome}: {n} salas geradas (o mapa no envelope, oculto; masmorras/{os.path.basename(arq(nome))})')


def ver(nome, tudo):
    M = json.load(open(arq(nome), encoding='utf-8'))
    print(f"MASMORRA {M['nome']} ({M['cat']}) · {len(M['salas'])} salas")
    for s in M['salas']:
        if tudo or s['vista']:
            print(f"  sala {s['n']}: {s['o_que']} → leva a {s['leva_a'] or 'nada (o fim)'}" + ('' if s['vista'] else ' (não vista)'))
        else:
            print(f"  sala {s['n']}: ?")


def entra(nome, n):
    M = json.load(open(arq(nome), encoding='utf-8'))
    s = M['salas'][int(n) - 1]; s['vista'] = True
    json.dump(M, open(arq(nome), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    anota(f"- MASMORRA {nome}: a casa entrou na sala {n}: {s['o_que']}")
    print(f"sala {n}: {s['o_que']} → leva a {s['leva_a'] or 'nada (o fim)'}")


def main():
    a = sys.argv[1:]
    if len(a) >= 3 and a[0] == 'gera':
        n = int(next((x[6:] for x in a if x.startswith('salas=')), 0))
        rest = [x for x in a[3:] if not x.startswith('salas=')]
        gera(a[1], a[2], rest[0] if rest else '', n); return
    if len(a) >= 2 and a[0] == 'ver':
        ver(a[1], 'tudo' in a); return
    if len(a) >= 3 and a[0] == 'entra':
        entra(a[1], a[2]); return
    print(__doc__)


if __name__ == '__main__':
    main()
