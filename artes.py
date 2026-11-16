#!/usr/bin/env python3
"""artes.py — G30, AURA ALTA E ARTES DE ARMA (Livro Nove 3; MOTOR 9.1, Dia 438): as técnicas de cada guerreiro, declaradas e na ficha.

  QUANTAS (o precedente do 438, o Moreth e o Eiagrir): a maestria de Luta escrita na ficha; sem ela, para quem vive da arma, pela faixa de
  nível: até 49 Treinado · 50-149 Mestre · 150+ Lendário. Técnicas = Treinado 1 · Mestre 2 · Lendário 3, +1 a cada 50 níveis.
  Círculo máximo: Treinado 2º · Mestre 4º · Lendário 6º.
  QUAIS: as Artes da ARMA dele (2º, 4º, 6º, até o círculo que ele alcança) e o resto em TÉCNICAS DE AURA do grimório (1º e 2º). A arma sai
  da ficha ou da classe; sem nada escrito, sai no d7 (selo). As auras saem no d10 (selo; a repetida vale a seguinte livre da lista).
  NA FICHA (G9): a Arte que fere = (o dado da arma como 1d6) + 2d6 × círculo, com METADE do multiplicador da arma (o foco da categoria:
  Comum ×1 · Incomum ×1,25 · Raro ×1,5 · Épico ×2 · Único ×3 · Lendário ×5 · Mítico ×10 · Primordial ×20; mínimo ×1); 1x por cena cada;
  a chave "arte" faz o luta.py rodar o EFEITO. Luta Lendário: o REMATE (encadear três, 1x por dia) ganha nome na primeira cena.
  Quem é DA CASA vai à mesa (público); os grandes do mundo vão OCULTOS (Lei 7: a mesma regra, no envelope antes da primeira luta).

Uso:
  python3 artes.py ver [NOME]
  python3 artes.py da NOME arma=lanca|espada|maca|machado|arco|escudo|punho|? [arma2=...] [cat=Lendário] [essencia=Terra] [maestria=Mestre] [nivel=N] [oculto] [peca="LANÇA DO BREN"]
  python3 artes.py ficha NOME              (re)escreve as Artes dele na ficha de combate (fichas_combate.json)
"""
import json, sys
from nucleo import carrega, grava, anota, dia_atual, sem_acento

ARQ = 'artes.json'
ARMAS = {'espada': ['fio_duplo', 'corte_corrido', 'corte_do_horizonte'], 'lanca': ['ponta_que_espera', 'chuva_de_pontas', 'lanca_que_nao_dobra'],
         'maca': ['quebra_guarda', 'tremor_de_ferro', 'bigorna'], 'machado': ['rachar', 'roda_de_lamina', 'derrubar_o_tronco'],
         'arco': ['tiro_duplo', 'flecha_que_prega', 'flecha_que_nao_cai'], 'escudo': ['empurrar_a_parede', 'guarda_de_dois', 'muralha_de_um_homem'],
         'punho': ['mao_aberta', 'passo_que_some', 'golpe_no_sopro']}
NOME_ARMA = {'espada': 'Espada', 'lanca': 'Lança', 'maca': 'Maça e martelo', 'machado': 'Machado', 'arco': 'Arco e besta', 'escudo': 'Escudo', 'punho': 'Punho e corpo'}
ARTE_TXT = {'fio_duplo': 'FIO DUPLO', 'corte_corrido': 'CORTE CORRIDO', 'corte_do_horizonte': 'CORTE DO HORIZONTE', 'ponta_que_espera': 'PONTA QUE ESPERA',
            'chuva_de_pontas': 'CHUVA DE PONTAS', 'lanca_que_nao_dobra': 'LANÇA QUE NÃO DOBRA', 'quebra_guarda': 'QUEBRA-GUARDA', 'tremor_de_ferro': 'TREMOR DE FERRO',
            'bigorna': 'BIGORNA', 'rachar': 'RACHAR', 'roda_de_lamina': 'RODA DE LÂMINA', 'derrubar_o_tronco': 'DERRUBAR O TRONCO', 'tiro_duplo': 'TIRO DUPLO',
            'flecha_que_prega': 'FLECHA QUE PREGA', 'flecha_que_nao_cai': 'FLECHA QUE NÃO CAI', 'empurrar_a_parede': 'EMPURRAR A PAREDE', 'guarda_de_dois': 'GUARDA DE DOIS',
            'muralha_de_um_homem': 'MURALHA DE UM HOMEM', 'mao_aberta': 'MÃO ABERTA', 'passo_que_some': 'PASSO QUE SOME', 'golpe_no_sopro': 'GOLPE NO SOPRO'}
AURAS = ['Pele de Pedra', 'Raiz de Pedra menor', 'Passo de Vento', 'Sangue Quente', 'Fôlego de Ferro', 'Mão de Pedra', 'Instante', 'Calma', 'Luz no Escudo', 'Nó de Chamada']
FOCO = {'Comum': 1, 'Incomum': 1.25, 'Raro': 1.5, 'Épico': 2, 'Único': 3, 'Lendário': 5, 'Mítico': 10, 'Primordial': 20}
BASE = {'Treinado': (1, 2), 'Mestre': (2, 4), 'Lendário': (3, 6)}


def titulo(t):
    return ' '.join(w if w in ('que', 'de', 'do', 'um', 'a', 'o') else w[:1].upper() + w[1:] for w in t.lower().split())


def opt(a, k, padrao=None):
    return next((x[len(k) + 1:] for x in a if x.startswith(k + '=')), padrao)


def maestria_de(nome, nivel):
    cl = sem_acento(str(carrega('npcs.json', {}).get(nome, {}).get('classe', '')))
    for g in ('lendario', 'mestre', 'treinado'):
        if f'luta {g}' in cl: return {'lendario': 'Lendário', 'mestre': 'Mestre', 'treinado': 'Treinado'}[g], 'escrita na ficha'
    return ('Lendário' if nivel >= 150 else 'Mestre' if nivel >= 50 else 'Treinado'), 'pela faixa de nível (precedente do 438)'


def circ(k): return [2, 4, 6][[x for x in ARMAS.values() if k in x][0].index(k)]


def para_ficha(e, ficha):
    """as entradas de "magias" da ficha de combate: uma por Arte que fere (as Reações entram para o script armar)"""
    usadas = set()
    for m in ficha.get('magias', []):
        if m.get('arte'): continue
        r = m.get('rodada'); usadas |= set(r if isinstance(r, list) else [r])
    out = []; livre = (x for x in range(1, 60) if x not in usadas)
    for k in sorted(e['artes'], key=lambda k: -circ(k)):
        c = circ(k); nome = f"{ARTE_TXT[k]} (Arte de {NOME_ARMA[e['arma_de'][k]].split()[0].lower()}, {c}º; G30: metade do multiplicador da arma, ×{e['mult']:g}; 1x por cena)"
        it = {'nome': nome, 'arte': k, 'dano': f'{1 + 2 * c}d6', 'mult': e['mult'], 'cd': 30, 'essencia': e.get('essencia') or ''}
        it['rodada'] = [1] if k in ('ponta_que_espera', 'guarda_de_dois') else [next(livre)]
        if k in ('ponta_que_espera', 'chuva_de_pontas', 'flecha_que_prega', 'tiro_duplo', 'flecha_que_nao_cai'): pass
        out.append(it)
    return out


def escreve_ficha(nome, e):
    R = carrega('fichas_combate.json', {'fichas': {}})
    if nome not in R['fichas']: return False
    f = R['fichas'][nome]
    f['magias'] = [m for m in f.get('magias', []) if not m.get('arte') and not str(m.get('nome', '')).split(' (')[0] in ARTE_TXT.values()] + para_ficha(e, f)
    txt = f"ARTES DE ARMA (G30, 438): {', '.join(NOME_ARMA[a] + ': ' + ', '.join(titulo(ARTE_TXT[k]) for k in e['artes'] if e['arma_de'][k] == a) for a in e['armas'])}" + (f"; auras: {', '.join(e['auras'])}" if e['auras'] else '')
    p = str(f.get('pecas', ''))
    p = p.split(' · ARTES DE ARMA (G30')[0] if ' · ARTES DE ARMA (G30' in p else ('' if p.startswith('ARTES DE ARMA (G30') else p)
    f['pecas'] = (p + ' · ' if p else '') + txt
    grava('fichas_combate.json', R); return True


def main():
    a = sys.argv[1:]; S = carrega(ARQ, {})
    if not a or a[0] == 'ver':
        if not a: print(__doc__)
        for k, e in sorted(S.items(), key=lambda kv: -kv[1]['nivel']):
            if len(a) > 1 and sem_acento(a[1]) not in sem_acento(k): continue
            print(f"  {k} ({e['nivel']}, Luta {e['maestria']}: {e["n"]} técnica{"s" if e["n"] > 1 else ""} até o {e["circulo"]}º){' [OCULTO]' if e.get('oculto') else ''}: "
                  + ' · '.join(f"{NOME_ARMA[w]}: " + ', '.join(titulo(ARTE_TXT[x]) for x in e['artes'] if e['arma_de'][x] == w) for w in e['armas'])
                  + (f" · auras: {', '.join(e['auras'])}" if e['auras'] else '') + f" · ×{e['mult']:g}" + (' · REMATE: a nomear' if e['maestria'] == 'Lendário' else ''))
        return
    if a[0] == 'ficha' and len(a) > 1:
        e = S.get(a[1]) or sys.exit('sem Artes no livro.'); print('ficha acertada.' if escreve_ficha(a[1], e) else 'não tem ficha de combate.'); return
    if a[0] != 'da' or len(a) < 3: sys.exit(__doc__)
    nome = a[1]; N = carrega('npcs.json', {}); V = carrega('mundo_vivo.json', {})
    nv = opt(a, 'nivel')
    if nv: nv = int(nv)
    elif nome in N: nv = N[nome]['nivel']
    else:
        achou = [l['nivel'] for l in V.get('lendarios', []) if l['nome'].split(',')[0] == nome] + [p['nivel'] for g in V.get('guildas', []) for p in [g['chefe']] + g.get('membros', []) if p['nome'] == nome] + [v['nivel'] for v in V.get('viloes', []) if v['nome'] == nome]
        nv = achou[0] if achou else sys.exit(f'{nome}: não achei o nível (nivel=N).')
    m = opt(a, 'maestria'); mq = (m, 'dita pelo Mestre') if m else maestria_de(nome, nv)
    base, cmax = BASE[mq[0]]; n = base + nv // 50
    oc = 'oculto' in a
    import selo
    Z = selo.load(); armas = []
    for chave in ('arma', 'arma2'):
        w = opt(a, chave)
        if not w: continue
        w = sem_acento(w).replace('ç', 'c')
        if w == '?':
            sid = selo.declara(Z, '-', f'A ARMA DE {nome.upper()} (G30; nada escrito na ficha nem na classe)', 'd7', ' | '.join(f'{i + 1}: {NOME_ARMA[x]}' for i, x in enumerate(ARMAS)), selo.opcoes(['oculto'] if oc else []), quieto=True)
            w = list(ARMAS)[selo.rola(Z, sid, quieto=True)['rolagens'][-1]['total'] - 1]
        if w not in ARMAS: sys.exit(f'arma que não conheço: {w} ({", ".join(ARMAS)})')
        armas.append(w)
    if not armas: sys.exit('arma=... (ou arma=? para o dado)')
    artes, arma_de = [], {}
    for w in armas:
        for k in ARMAS[w]:
            if circ(k) <= cmax and len(artes) < n: artes.append(k); arma_de[k] = w
    auras = []
    resto = n - len(artes)
    if resto > 0:
        k = min(resto, len(AURAS))
        sid = selo.declara(Z, '-', f'AS TÉCNICAS DE AURA DE {nome.upper()} (G30; {k} delas; a repetida vale a seguinte livre da lista)', 'd10', ' | '.join(f'{i + 1}: {x}' for i, x in enumerate(AURAS)),
                           selo.opcoes((['oculto'] if oc else []) + ([f'x={k}'] if k > 1 else [])), quieto=True)
        for r in selo.rola(Z, sid, quieto=True)['rolagens']:
            i = r['total'] - 1
            while AURAS[i] in auras: i = (i + 1) % len(AURAS)
            auras.append(AURAS[i])
    cat = opt(a, 'cat'); F = carrega('fichas_combate.json', {'fichas': {}})['fichas'].get(nome, {})
    mult = max(1, FOCO[cat] / 2) if cat else max(1, F.get('mult', 2) / 2)
    e = {'nivel': nv, 'maestria': mq[0], 'maestria_de': mq[1], 'n': n, 'circulo': cmax, 'armas': armas, 'artes': artes, 'arma_de': arma_de, 'auras': auras,
         'mult': mult, 'mult_de': (f'metade do foco {cat}' if cat else 'metade do multiplicador da ficha (a categoria da arma não está escrita)'), 'essencia': opt(a, 'essencia', ''),
         'peca': opt(a, 'peca', ''), 'oculto': oc, 'dia': dia_atual()}
    if mq[0] == 'Lendário': e['remate'] = 'a nomear na primeira cena (Livro Nove 3.4: encadeia três, 1x por dia)'
    S[nome] = e; grava(ARQ, S); naf = escreve_ficha(nome, e)
    lin = (f"{nome} ({nv}; Luta {mq[0]}, {mq[1]}: {n} técnica{"s" if n > 1 else ""} até o {cmax}º){' (OCULTO)' if oc else ''}: "
           + ' · '.join(f"{NOME_ARMA[w]}{' (' + e['peca'] + ')' if e['peca'] and w == armas[0] else ''}: " + ', '.join(f'{ARTE_TXT[x]} ({circ(x)}º)' for x in artes if arma_de[x] == w) for w in armas)
           + (f" · auras: {', '.join(auras)}" if auras else '') + f" · na ficha ×{mult:g} ({e['mult_de']})" + (' · o REMATE a nomear' if mq[0] == 'Lendário' else '') + (' · ficha de combate acertada' if naf else ''))
    anota(f"- G30, AS ARTES DE ARMA [Dia {dia_atual()}]: " + lin); print(lin)


if __name__ == '__main__':
    main()
