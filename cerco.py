#!/usr/bin/env python3
"""cerco.py — CERCO DE LONGE contra uma fera ou uma muralha, jogado de verdade (MOTOR 6.3). Uma cena por dia. Dados verdadeiros.
Cada cerco é um arquivo em cercos/NOME.json com a ficha do alvo, os atiradores e quem está a bordo. Nasceu do cerco da Elaeva (Dia 382).
Uso: python3 cerco.py NOME dia DIA [sal] | visao [N] [sal] | entra QUEM | sai QUEM | ver     (446: 'sal' = os tiros do dia com o SAL da fraqueza escondida: o dano dobra; 'fase' no json: a segunda fase aos 50%)        ·        python3 cerco.py lista
Cerco novo: copie cercos/elaeva.json, troque "alvo" (nome, pv, pvm, df = Defesa + 14, rd), "atiradores" (nome: [tiros por dia, dados d6, multiplicador, ataque]),
"a_bordo", "lugar" (a cidade cujo tempo vale), "capitao" ([nome, bônus]) e zere "dias" e "fim". As regras de cada dia são as mesmas:
As regras são as da régua (sims/elaeva_barcos.py, Dia 361), com a MAGIA DISPUTADA do Dia 379, declaradas aqui ANTES do primeiro dado:
 A FERA: Elaeva, Mítica 376 · PV 37.600 · Defesa 134 (+14 = 148) · casca (RD) 50 · fraca a Fogo (já contado no multiplicador de quem atira fogo).
 CADA DIA, nesta ordem:
  1. ELA DECIDE: abaixo de 25% do PV, d6 1-4 vai embora · abaixo de 50%, d6 1-2 vai embora.
  2. ONDE ELA ESTÁ: d6 1-2 longe da costa hoje (ninguém atira).
  3. O TEMPO em Farenta (clima.json): tempestade = barco não sai, ninguém atira · neblina = −4 no ataque de todos.
  4. O PERIGO DO DIA, d20: 1-2 (1-3 com vento forte) A ÂNCORA GARRA e a galé deriva para a costa: a Isolda testa 2d20+21 contra 30;
     se falhar, a galé entra nos 18 m e o ESPINHEIRO pega o convés (40d6 em cada um a bordo; 2d20 + Agilidade÷10 contra 44 leva metade) e 1d6 remadores caem ·
     19-20 A FERA SE EXPÕE (o cerne aparece): todos os tiros do dia com +10 no ataque · o resto: nada.
  5. OS TIROS: cada atirador joga 2d20 + ataque contra 148. Em cheio: dano inteiro · resiste: metade · 20 que morde (o outro dado 11+): dados dobrados ·
     dois 1: o feitiço se desfaz. Depois tira a casca (50).
     Mamiltia 2 × 8d6 × 20 (ataque 134) · Eiagrir 2 × 16d6 × 5 (36) · Ferir 7 × 8d6 × 5 (34) · Moreth, quando chegar, 2 × 16d6 × 10 (44).
Uso: python3 sims/cerco_elaeva.py dia DIA   |   visao [N]   (a Visão do Tempo: o que UM dia pode dar, sem valor de jogo)   |   entra NOME   |   sai NOME   |   ver
"""
import sys, os, json, secrets, random
from nucleo import carrega, grava, anota
ARQ = None; TODOS = {}; AGI = {}; DF, RD = 148, 50; CAP = ['a Isolda', 21]; ALVO = 'a fera'
SIM = False
def d(n): return random.randint(1, n) if SIM else secrets.randbelow(n) + 1
def ex():
    t = 0
    while True:
        r = d(20); t += r
        if r != 20: return t
def load():
    global TODOS, AGI, DF, RD, CAP, ALVO
    S = carrega(ARQ)
    if not S: sys.exit(f'não achei {ARQ}. (python3 cerco.py lista)')
    TODOS = {k: tuple(v) for k, v in S['atiradores'].items()}; AGI = S.get('agi', {}); DF, RD = S['alvo']['df'], S['alvo']['rd']; CAP = S.get('capitao', CAP); ALVO = S['alvo']['nome']
    return S
def um_dia(S, tempo, quieto=False):
    L = []; frac = S['pv'] / S['pvm']; dano = {}
    if frac < 0.25:
        r = d(6); L.append(f"ELA DECIDE (abaixo de 25%): d6 [{r}] → " + ('VAI EMBORA' if r <= 4 else 'fica'))
        if r <= 4: S['fim'] = 'foi embora'; return L, dano
    elif frac < 0.50:
        r = d(6); L.append(f"ELA DECIDE (abaixo de 50%): d6 [{r}] → " + ('VAI EMBORA' if r <= 2 else 'fica'))
        if r <= 2: S['fim'] = 'foi embora'; return L, dano
    r = d(6)
    if r <= 2: L.append(f'ONDE ELA ESTÁ: d6 [{r}] → longe da costa hoje; ninguém atira'); return L, dano
    L.append(f'ONDE ELA ESTÁ: d6 [{r}] → na praia, ao alcance')
    ceu, vento = tempo
    if ceu == 'tempestade': L.append('O TEMPO: tempestade → a galé não sai do abrigo; ninguém atira'); return L, dano
    mod = -4 if ceu == 'neblina' else 0
    p = d(20); lim = 3 if vento in ('vento forte',) else 2
    if p <= lim:
        t = ex() + ex() + CAP[1]
        if t >= 30: L.append(f'O PERIGO: d20 [{p}] A ÂNCORA GARRA · {CAP[0]} 2d20+{CAP[1]} = {t} contra 30 → SEGURA a galé nos 30 m')
        else:
            L.append(f'O PERIGO: d20 [{p}] A ÂNCORA GARRA · {CAP[0]} 2d20+{CAP[1]} = {t} contra 30 → FALHA: a galé entra nos 18 m e o ESPINHEIRO varre o convés')
            for n in S['a_bordo'] + [CAP[0].replace('a ', '').replace('o ', '')]:
                dm = sum(d(6) for _ in range(40)); sv = ex() + ex() + AGI.get(n, 6)
                if sv >= 44: dm //= 2
                S['feridos'][n] = S['feridos'].get(n, 0) + dm; L.append(f'   {n}: Agilidade {sv} contra 44 → −{dm} PV')
            L.append(f'   remadores caídos: 1d6 [{d(6)}]')
    elif p >= 19: mod += 10; L.append(f'O PERIGO: d20 [{p}] A FERA SE EXPÕE: o cerne aparece (+10 no ataque de todos hoje)')
    else: L.append(f'O PERIGO: d20 [{p}] → nada')
    for n in S['a_bordo']:
        vezes, q, mult, at = TODOS[n]; tot = 0; det = []
        for _ in range(vezes):
            a, b = d(20), d(20); xa, xb = a, b
            while a == 20: a = d(20); xa += a
            while b == 20: b = d(20); xb += b
            a0, b0 = (20 if xa >= 20 else xa), (20 if xb >= 20 else xb)
            t = xa + xb + at + mod
            crit = (a0 == 20 and b0 >= 11) or (b0 == 20 and a0 >= 11)
            if xa == 1 and xb == 1: liq = 0; como = 'desfaz'
            else:
                dm = int(sum(d(6) for _ in range(q * (2 if crit else 1))) * mult)
                if crit: como = 'MORDE'
                elif t >= DF: como = 'em cheio'
                else: dm //= 2; como = 'resiste'
                liq = max(dm - RD, 0)
                if S.get('sal_hoje') and liq > 0: liq *= 2; como += ' +SAL ×2'   # 446 (MOTOR 9b): a fraqueza escondida: o sal na ponta e no piche dobra o dano (e corta a regeneração)
            tot += liq; det.append(f'{t} {como} {liq}')
        dano[n] = tot; S['pv'] -= tot
        L.append(f'{n}: ' + ' · '.join(det) + f' → {tot}')
        if S['pv'] <= 0: S['pv'] = 0; S['fim'] = 'MORTA'; L.append(f'{ALVO.upper()} CAI'); break
        fs = S.get('fase')   # 446 (G33): a SEGUNDA FASE aos 50% vale também no cerco
        if fs and not fs.get('feita') and S['pv'] < S['pvm'] * 0.5:
            fs['feita'] = True; L.append(f"SEGUNDA FASE ({fs.get('nome', '')}): " + fs.get('efeito_cerco', 'o Mestre aplica o que a fase diz'))
            for k, v in fs.get('atiradores', {}).items(): TODOS[k] = tuple(v); S['atiradores'][k] = v
    return L, dano
def main():
    global SIM, ARQ
    a = sys.argv[1:]
    if not a or a[0] == 'lista':
        import glob
        for f in sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cercos', '*.json'))):
            T = json.load(open(f, encoding='utf-8')); print(f"{os.path.basename(f)[:-5]}: {T['alvo']['nome']} {T['pv']}/{T['pvm']} · {len(T['dias'])} dias · fim: {T['fim']}")
        return
    ARQ = f'cercos/{a[0]}.json'; a = a[1:]
    S = load()
    if not a or a[0] == 'ver':
        print(f"{ALVO} {S['pv']}/{S['pvm']} ({100 * S['pv'] / S['pvm']:.0f}%) · a bordo: {', '.join(S['a_bordo'])} · dias de cerco: {len(S['dias'])} · fim: {S['fim']} · feridos: {S['feridos']}")
        for x in S['dias'][-5:]: print(f"   Dia {x['dia']}: {x['antes']} → {x['depois']} · " + ' · '.join(f'{k} {v}' for k, v in x['dano'].items()))
        return
    if a[0] in ('entra', 'sai'):
        if a[1] not in TODOS: sys.exit(f'{a[1]} não tem tiro neste cerco. Atiradores: {", ".join(TODOS)}')
        if a[0] == 'entra' and a[1] not in S['a_bordo']: S['a_bordo'].append(a[1])
        if a[0] == 'sai' and a[1] in S['a_bordo']: S['a_bordo'].remove(a[1])
        grava(ARQ, S); print('a bordo:', ', '.join(S['a_bordo'])); return
    lugar = S.get('lugar', 'Ireviel')
    C = next((v for k, v in carrega('clima.json', {}).get('hoje', {}).items() if lugar.lower() in k.lower()), {'ceu': 'limpo', 'vento': 'brisa'})
    tempo = (C['ceu'], C['vento'])
    if a[0] == 'visao':
        SIM = True; n = int(a[1]) if len(a) > 1 else 3000; tot = []; longe = 0; garra = 0; feridos = 0; some = 0
        for _ in range(n):
            T = json.loads(json.dumps(S)); T['sal_hoje'] = 'sal' in a; L, dn = um_dia(T, tempo)
            tot.append(S['pv'] - T['pv']); longe += any('longe da costa' in l for l in L); garra += any('GARRA' in l for l in L); feridos += any('FALHA' in l for l in L); some += T['fim'] == 'foi embora'
        tot.sort()
        print(f"A VISÃO DO TEMPO (uma hora à frente, {n} futuros; tempo: {tempo[0]}, {tempo[1]}): vai embora hoje em {100 * some / n:.0f}% · fica longe em {100 * longe / n:.0f}% · quando vem, perde de {tot[int(.45 * n)]} a {tot[int(.95 * n)]} PV (o mais comum: {tot[int(.7 * n)]}) de {S['pv']} · a âncora garra em {100 * garra / n:.0f}% e o perigo alcança o convés em {100 * feridos / n:.1f}%"); return
    if a[0] == 'dia':
        dia = int(a[1])
        if S['fim']: print('o cerco já acabou:', S['fim']); return
        if any(x['dia'] == dia for x in S['dias']): print('este dia de cerco já foi rolado.'); return
        if not S['dias']: anota(f"- DECLARADO (CERCO) [Dia {dia}] O CERCO de {ALVO}: regras em cerco.py (o alvo decide · onde está · o tempo · o perigo d20 · os tiros com magia disputada contra {DF}, casca {RD}). PV {S['pvm']}.")
        S['sal_hoje'] = 'sal' in a
        antes = S['pv']; L, dn = um_dia(S, tempo)
        S['dias'].append({'dia': dia, 'antes': antes, 'depois': S['pv'], 'dano': dn, **({'sal': True} if S.pop('sal_hoje', False) else {})})
        grava(ARQ, S)
        print(f"CERCO, Dia {dia} ({lugar}: {tempo[0]}, {tempo[1]}) · {ALVO} {antes}/{S['pvm']}")
        for l in L: print('  ' + l)
        print(f"  → {ALVO} {S['pv']}/{S['pvm']} ({100 * S['pv'] / S['pvm']:.0f}%) · perdeu {antes - S['pv']} hoje" + (f" · FIM: {S['fim']}" if S['fim'] else ''))
        anota(f"- ROLADO (CERCO {dia}) " + ' ‖ '.join(L) + f" ‖ {ALVO} {S['pv']}/{S['pvm']}")
if __name__ == '__main__':
    main()
