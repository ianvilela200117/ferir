#!/usr/bin/env python3
"""coleta.py — G35, OS OFÍCIOS DE COLETA COM GRAU (Livro Nove 14; MOTOR 9.1, Dia 438, pedido do jogador).

Sobre o Motor XI.7 (Coleta: teste contra a CD do lugar; reserva FINITA, rolada antes de começar) e V.3 (a escala de maestria).
  CINCO OFÍCIOS: minerar (minério, pedra, cristal) · ervar (erva, resina, raiz, fungo) · esfolar (o despojo do bicho morto) ·
                 pescar (peixe, pérola, coral, o sal das salinas) · lenhar (madeira, casca)
  O GRAU (a maestria de cada ofício): Leigo +0 · Iniciante +2 · Treinado +4 · Mestre +6 · Lendário +8. Ele também diz o que a mão
     alcança: Leigo e Iniciante até Incomum · Treinado até Raro · Mestre até Épico · Lendário até Único (acima disso, só núcleo e caçada).
  SOBE PELA PRÁTICA (V.3): Iniciante 3 dias · Treinado 7 dias e um teste CD 20 · Mestre 14 dias, CD 25 e um feito · Lendário 30 dias,
     CD 35, uma Prova e um mestre ou uma fonte. Cada dia de coleta de verdade conta 1 dia (o script avisa quando chega a hora do teste).
  O DIA DE COLETA: 2d20 + atributo ÷ 10 + o grau + a ferramenta (+1 a +6) contra a CD da categoria +10 (os dois dados):
     Comum 15 · Incomum 20 · Raro 25 · Épico 30 · Único 35. Pela margem (como o aberto.py):
       falha feia (10 ou mais abaixo): ACIDENTE: d6 1-3 ferido (1d6 × (degrau + 1) de PV) · 4-6 o barulho atrai um bicho da região
       falha: nada · sucesso: 1 UNIDADE · ganho (+10): 2 · extraordinário (+20): 3 e um ACHADO (0,1 kg um degrau acima, se a reserva tiver)
     A UNIDADE: Comum 5 kg · Incomum 2 kg · Raro 1 kg · Épico 0,5 kg · Único 0,1 kg. Sai da RESERVA do lugar (finita).
  A RESERVA (Motor XI.7: rolada antes): pequena d6 unidades · média 2d6 · grande 4d6 (a ocorrência que o gerador dá ao material).
  ESFOLAR: depois de cada bicho Raro ou acima morto, o melhor esfolador rola contra a CD da categoria do bicho:
       falha feia: um tipo de despojo se estraga (perde a metade) · falha ou sucesso: o despojo como saiu · ganho: +1 unidade de um tipo ·
       extraordinário: +1 unidade de cada tipo.
  PREÇO (Lei 2): um dia por teste; a ferramenta (a forja do rei faz: Comum +1 ... Mítica +6); o acidente; e a reserva acaba.

Uso:
  python3 coleta.py ver
  python3 coleta.py grau NOME OFICIO GRAU ["motivo"]       acerta o grau (leitura da ficha; GRAU: Leigo Iniciante Treinado Mestre Lendário)
  python3 coleta.py reserva "LUGAR" MATERIAL CATEGORIA [tamanho=pequena|media|grande]     abre um veio/mata/cardume (rola o tamanho no selo)
  python3 coleta.py vai NOME OFICIO "LUGAR" [dias=N] [ferramenta=N] [atributo=N] [mais=N] [para=casa]
  python3 coleta.py esfola NOME CATEGORIA_DO_BICHO "o bicho" [ferramenta=N] [atributo=N]
"""
import sys
from nucleo import carrega, grava, anota, dia_atual, sem_acento

ARQ = 'coleta.json'
OFICIOS = ['minerar', 'ervar', 'esfolar', 'pescar', 'lenhar']
GRAUS = ['Leigo', 'Iniciante', 'Treinado', 'Mestre', 'Lendário']
BONUS = {'Leigo': 0, 'Iniciante': 2, 'Treinado': 4, 'Mestre': 6, 'Lendário': 8}
ALCANCE = {'Leigo': 1, 'Iniciante': 1, 'Treinado': 2, 'Mestre': 3, 'Lendário': 4}   # o degrau mais alto que a mão tira
CATS = ['Comum', 'Incomum', 'Raro', 'Épico', 'Único']
CD = {'Comum': 15, 'Incomum': 20, 'Raro': 25, 'Épico': 30, 'Único': 35}
UNID = {'Comum': 5, 'Incomum': 2, 'Raro': 1, 'Épico': 0.5, 'Único': 0.1}
SOBE = {'Iniciante': (3, None), 'Treinado': (7, 20), 'Mestre': (14, 25), 'Lendário': (30, 35)}


def opt(a, k, padrao=None):
    return next((x[len(k) + 1:] for x in a if x.startswith(k + '=')), padrao)


def cat_de(t):
    k = next((c for c in CATS if sem_acento(c) == sem_acento(t)), None)
    if not k: sys.exit(f'categoria de coleta: {", ".join(CATS)} (acima de Único, só núcleo e caçada)')
    return k


def of_de(t):
    k = next((o for o in OFICIOS if o.startswith(sem_acento(t)[:4])), None)
    if not k: sys.exit(f'ofício: {", ".join(OFICIOS)}')
    return k


def grau_de(S, nome, of):
    return S['graus'].get(nome, {}).get(of, {}).get('grau', 'Leigo')


def teste(Z, titulo, bonus, cd, oculto=False):
    """2d20 + bônus contra a CD + 10, lido pela margem (falha feia, falha, sucesso, ganho, extraordinário)"""
    import selo
    a = cd + 10
    tab = f'1-{a - 10}: FALHA FEIA | {a - 9}-{a - 1}: falha | {a}-{a + 9}: SUCESSO | {a + 10}-{a + 19}: GANHO | {a + 20}+: EXTRAORDINÁRIO'
    sid = selo.declara(Z, '-', titulo, f'2d20+{bonus}', tab, selo.opcoes(['oculto'] if oculto else []), quieto=True)
    r = selo.rola(Z, sid, quieto=True)['rolagens'][-1]
    return r['total'], r['res'], r['txt']


def pratica(S, nome, of, dias=1):
    g = S['graus'].setdefault(nome, {}).setdefault(of, {'grau': 'Leigo', 'dias': 0})
    g['dias'] = g.get('dias', 0) + dias
    i = GRAUS.index(g['grau'])
    if i + 1 < len(GRAUS):
        prox = GRAUS[i + 1]; dn, cd = SOBE[prox]
        if g['dias'] >= dn:
            if cd is None: g['grau'] = prox; return f'★ {nome} sobe a {prox} em {of} ({g["dias"]} dias de prática)'
            return f'⚑ {nome} tem os dias para {prox} em {of}: falta o teste (aberto.py 2d20+N cd={cd})' + (' e um feito na área' if prox == 'Mestre' else ' e uma Prova e um mestre ou fonte' if prox == 'Lendário' else '') + f' → coleta.py grau {nome} {of} {prox}'
    return ''


def main():
    a = sys.argv[1:]; S = carrega(ARQ, {'nota': 'G35: os graus de coleta e as reservas abertas (coleta.py).', 'graus': {}, 'reservas': {}}); dia = dia_atual()
    if not a or a[0] == 'ver':
        if not a: print(__doc__)
        print('OS OFÍCIOS DE COLETA (G35)')
        for n, gs in sorted(S['graus'].items()): print(f'  {n}: ' + ' · '.join(f"{o} {g['grau']} ({g.get('dias', 0)} dias)" for o, g in gs.items()))
        for l, r in S['reservas'].items(): print(f"  RESERVA {l}: {r['material']} ({r['cat']}) · {r['resta']} de {r['total']} unidades ({UNID[r['cat']]:g} kg cada)")
        if not S['graus'] and not S['reservas']: print('  ninguém tem grau anotado ainda.')
        return
    c = a[0]
    if c == 'grau' and len(a) >= 4:
        of = of_de(a[2]); g = next((x for x in GRAUS if sem_acento(x) == sem_acento(a[3])), None) or sys.exit(f'grau: {", ".join(GRAUS)}')
        e = S['graus'].setdefault(a[1], {}).setdefault(of, {'grau': 'Leigo', 'dias': 0}); antes = e['grau']; e['grau'] = g
        e['dias'] = max(e.get('dias', 0), SOBE.get(g, (0, 0))[0]); grava(ARQ, S)
        mot = a[4] if len(a) > 4 else ''; anota(f"- COLETA (G35) [Dia {dia}]: {a[1]} em {of}: {antes} → {g}" + (f' ({mot})' if mot else '')); print(f'{a[1]} · {of}: {antes} → {g}'); return
    import selo
    Z = selo.load()
    if c == 'reserva' and len(a) >= 4:
        lugar, mat, cat = a[1], a[2], cat_de(a[3]); tam = sem_acento(opt(a, 'tamanho', 'media'))
        dado = {'pequena': 'd6', 'media': '2d6', 'grande': '4d6'}.get(tam) or sys.exit('tamanho: pequena, media, grande')
        lo, hi = {'d6': (1, 6), '2d6': (2, 12), '4d6': (4, 24)}[dado]
        sid = selo.declara(Z, '-', f'A RESERVA de {mat} ({cat}) em {lugar} ({tam}; G35: rolada antes de começar)', dado, f'{lo}-{hi}: tantas unidades ({UNID[cat]:g} kg cada)', selo.opcoes([]), quieto=True)
        n = selo.rola(Z, sid, quieto=True)['rolagens'][-1]['total']
        S['reservas'][lugar] = {'material': mat, 'cat': cat, 'total': n, 'resta': n, 'desde': dia}; grava(ARQ, S)
        anota(f"- COLETA (G35) [Dia {dia}]: a reserva de {mat} ({cat}) em {lugar}: {n} unidades ({n * UNID[cat]:g} kg)"); print(f'RESERVA {lugar}: {mat} ({cat}) · {n} unidades ({n * UNID[cat]:g} kg)'); return
    if c == 'vai' and len(a) >= 4:
        nome, of, lugar = a[1], of_de(a[2]), a[3]
        r = S['reservas'].get(lugar) or sys.exit(f'não há reserva aberta em "{lugar}" (coleta.py reserva "{lugar}" MATERIAL CATEGORIA)')
        g = grau_de(S, nome, of)
        if CATS.index(r['cat']) > ALCANCE[g]: sys.exit(f'{nome} é {g} em {of}: a mão dele não tira {r["cat"]} (alcance: até {CATS[ALCANCE[g]]}). Nada foi rolado.')
        dias = int(opt(a, 'dias', 1)); fe = int(opt(a, 'ferramenta', 0)); at = int(opt(a, 'atributo', 0)); mais = int(opt(a, 'mais', 0))
        bonus = at + BONUS[g] + fe + mais; tot_u = 0; ach = 0; lin = []
        for k in range(dias):
            if r['resta'] <= 0: lin.append(f'dia {k + 1}: a reserva ACABOU'); break
            t, res, txt = teste(Z, f'COLETA (G35): {nome} {of} em {lugar}, dia {k + 1} ({r["material"]}, {r["cat"]}; {g} +{BONUS[g]}, ferramenta +{fe}, atributo +{at})', bonus, CD[r['cat']])
            u = {'SUCESSO': 1, 'GANHO': 2, 'EXTRAORDINÁRIO': 3}.get(res, 0); u = min(u, r['resta']); r['resta'] -= u; tot_u += u
            if res == 'EXTRAORDINÁRIO': ach += 1
            nota = ''
            if res == 'FALHA FEIA':
                sid = selo.declara(Z, '-', f'O ACIDENTE da coleta de {nome} em {lugar}', 'd6', f'1-3: ferido: 1d6 × {CATS.index(r["cat"]) + 1} de PV | 4-6: o barulho atrai um bicho da região (encontro)', selo.opcoes([]), quieto=True)
                x = selo.rola(Z, sid, quieto=True)['rolagens'][-1]['total']
                if x <= 3:
                    sid = selo.declara(Z, '-', f'O FERIMENTO de {nome} na coleta', 'd6', '1-6: tanto × ' + str(CATS.index(r['cat']) + 1), selo.opcoes([]), quieto=True)
                    pv = selo.rola(Z, sid, quieto=True)['rolagens'][-1]['total'] * (CATS.index(r['cat']) + 1); nota = f' · ACIDENTE: {nome} perde {pv} PV'
                else: nota = ' · ACIDENTE: o barulho atrai um BICHO DA REGIÃO (encontro: o Mestre monta pela G9)'
            p = pratica(S, nome, of)
            lin.append(f'dia {k + 1}: {txt}' + (f' → {u} unidade(s)' if u else '') + nota + (f' · {p}' if p else ''))
        kg = round(tot_u * UNID[r['cat']], 2); grava(ARQ, S)
        if kg and opt(a, 'para') == 'casa':
            import subprocess, os
            subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ficha.py'), 'mat', r['material'], f'+{kg}', f'coleta de {nome} em {lugar} (G35)'])
        out = f"COLETA (G35) [Dia {dia}]: {nome} ({of} {g}) em {lugar}, {dias} dia(s): {tot_u} unidade(s) de {r['material']} = {kg:g} kg" + (f' · {ach} ACHADO(S): 0,1 kg um degrau acima (o Mestre diz qual material, pelo Livro)' if ach else '') + f" · a reserva: {r['resta']} de {r['total']}"
        anota('- ' + out + ' · ' + ' ‖ '.join(lin)); print(out)
        for l in lin: print('   ' + l)
        return
    if c == 'esfola' and len(a) >= 4:
        nome, cat, bicho = a[1], a[2], a[3]
        cat = next((x for x in CATS + ['Lendário', 'Mítico', 'Primordial'] if sem_acento(x) == sem_acento(cat)), None) or sys.exit('categoria do bicho')
        cd = CD.get(cat, 35 + 5 * (['Lendário', 'Mítico', 'Primordial'].index(cat) + 1) if cat not in CD else 0)
        g = grau_de(S, nome, 'esfolar'); fe = int(opt(a, 'ferramenta', 0)); at = int(opt(a, 'atributo', 0))
        t, res, txt = teste(Z, f'ESFOLAR (G35): {nome} no {bicho} ({cat}; {g} +{BONUS[g]})', at + BONUS[g] + fe, cd)
        efe = {'FALHA FEIA': 'um TIPO de despojo se estraga: perde a metade (o Mestre diz qual, pelo dado)', 'falha': 'o despojo como saiu', 'SUCESSO': 'o despojo como saiu',
               'GANHO': '+1 unidade de UM tipo de despojo', 'EXTRAORDINÁRIO': '+1 unidade de CADA tipo de despojo'}[res]
        p = pratica(S, nome, 'esfolar'); grava(ARQ, S)
        out = f"ESFOLAR (G35) [Dia {dia}]: {nome} no {bicho}: {txt} → {efe}" + (f' · {p}' if p else ''); anota('- ' + out); print(out); return
    print(__doc__)


if __name__ == '__main__':
    main()
