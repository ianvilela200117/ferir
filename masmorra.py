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
MOTOR 9.1 (438, G37, pedido do jogador: "um atlas de masmorras do mundo"):
  python3 masmorra.py atlas [tudo]                               os lugares caídos que a casa conhece (do mundo_vivo.json), o que se sabe e o estado
  python3 masmorra.py degrau NOME                                o DEGRAU do lugar, no dado, na 1ª vez que a casa entra ou manda olhos (o precedente
                                                                 de Zythir, ZC36): guarda núcleo, prisioneiro ou peça antiga: d6 1-2 Épico · 3-4 Único ·
                                                                 5 Lendário · 6 Mítico · guarda material, receita ou segredo: d6 1-2 Raro · 3-4 Épico · 5 Único · 6 Lendário
  python3 masmorra.py gera NOME ? ["o que guarda"]               "?" no lugar da categoria: usa o degrau já rolado (ou rola agora)
  python3 masmorra.py estado NOME "o que a casa fez lá"         o estado do lugar no atlas
  python3 masmorra.py extra NOME "onde" "o que é (guarda ...)" "notícia"   um lugar que não está no mundo_vivo.json
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


ATLAS = 'masmorras/atlas.json'


def atlas_dados():
    from nucleo import carrega
    S = carrega(ATLAS, {})
    for k in ('degrau', 'estado', 'extras'): S.setdefault(k, [] if k == 'extras' else {})
    return S


def lugares():
    """os lugares que GUARDAM algo (o gerador de lugar: "guarda um núcleo / uma receita / um prisioneiro...") no mundo_vivo.json e os que o Mestre acrescentou"""
    import re
    from nucleo import carrega
    V = carrega('mundo_vivo.json', {}); out = []
    for l in V.get('lugares', []) + V.get('lugares_novos', []):
        oq = str(l.get('o_que', ''))
        if l.get('o_que_era') or re.search(r'\bguarda (um|uma|o|a|material|UM|UMA)\b', oq) or re.search(r'(ca[íi]d[ao]|afundad[ao]) (por|em)\b', oq): out.append(l)
    return out + atlas_dados()['extras']


def limpa(t):
    import re
    t = re.sub(r'\(OCULTO\)[^·;]*', '', str(t)); t = re.sub(r'\(OCULTO[^)]*\)', '', t)
    return re.sub(r'\s+', ' ', t).strip(' ;·')


def guarda_de(l):
    return limpa(l.get('guarda') or l.get('o_que', ''))


def degrau(nome):
    from nucleo import grava, sem_acento
    S = atlas_dados()
    if nome in S['degrau']: return S['degrau'][nome]
    L = next((l for l in lugares() if sem_acento(nome) in sem_acento(l['nome'])), None)
    g = sem_acento(guarda_de(L) if L else '')
    alto = any(x in g for x in ('nucleo', 'prisioneiro', 'peca antiga'))
    import selo
    Z = selo.load()
    tab = '1-2: Épico | 3-4: Único | 5: Lendário | 6: Mítico' if alto else '1-2: Raro | 3-4: Épico | 5: Único | 6: Lendário'
    sid = selo.declara(Z, '-', f'DE QUE DEGRAU É {nome.upper()} (G37; guarda: {guarda_de(L) if L else "?"})', 'd6', tab, selo.opcoes(['oculto']), quieto=True)
    r = selo.rola(Z, sid, quieto=True)['rolagens'][-1]['res']
    S['degrau'][nome] = r; os.makedirs(P('masmorras'), exist_ok=True); grava(ATLAS, S)
    return r


def atlas(tudo):
    S = atlas_dados()
    print('O ATLAS DAS MASMORRAS (G37) · os lugares caídos que a casa conhece')
    for l in lugares():
        if str(l.get('noticia', '')).startswith('não chega') and not tudo: continue
        mapa = os.path.exists(arq(l['nome'])); vistas = 0; n = 0; cat = S['degrau'].get(l['nome'])
        if mapa:
            M = json.load(open(arq(l['nome']), encoding='utf-8')); n = len(M['salas']); vistas = sum(1 for x in M['salas'] if x['vista']); cat = cat or M.get('cat')
        quando = l.get('noticia') or l.get('dia') or ''
        if l.get('o_que_era'):
            txt = f"era {limpa(l['o_que_era'])}; caiu por {limpa(l['por_que_caiu'])}; guarda {limpa(l['guarda'])}; mora {limpa(l['habita'])}; entrar: {limpa(l['entrar'])}"
        else: txt = limpa(l.get('o_que', ''))
        print(f"  {l['nome']}" + (f" ({limpa(l.get('onde', ''))})" if l.get('onde') else '') + f": {txt}" + (f" · notícia: {quando}" if quando else '')
              + (f" · DEGRAU {cat}" if cat else ' · degrau: no dado, na 1ª entrada') + (f" · MAPA: {vistas} de {n} salas vistas" if mapa else '')
              + (f" · ESTADO: {S['estado'][l['nome']]}" if S['estado'].get(l['nome']) else ''))


def estado(nome, txt):
    from nucleo import grava, anota, dia_atual
    S = atlas_dados(); S['estado'][nome] = f'{txt} ({dia_atual()})'; grava(ATLAS, S); anota(f'- ATLAS (G37): {nome}: {txt}'); print('anotado.')


def extra(nome, onde, o_que, noticia):
    from nucleo import grava
    S = atlas_dados(); S['extras'] = [x for x in S['extras'] if x['nome'] != nome] + [{'nome': nome, 'onde': onde, 'o_que': o_que, 'noticia': noticia}]; grava(ATLAS, S); print('anotado.')


def main():
    a = sys.argv[1:]
    if a and a[0] == 'atlas': atlas('tudo' in a); return
    if len(a) >= 3 and a[0] == 'estado': estado(a[1], a[2]); return
    if len(a) >= 5 and a[0] == 'extra': extra(a[1], a[2], a[3], a[4]); return
    if len(a) >= 2 and a[0] == 'degrau': print(f'{a[1]}: {degrau(a[1])}'); return
    if len(a) >= 3 and a[0] == 'gera' and a[2] == '?': a[2] = degrau(a[1])
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
