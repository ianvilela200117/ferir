#!/usr/bin/env python3
"""torre_acesa_404.py — O SINO DA TORRE MAIOR (madrugada do 404). REAL: um combate, dados verdadeiros, todo dado impresso.
Regras T2 do envelope 2n (declaradas antes). Uso: python3 sims/torre_acesa_404.py dormindo|acordado
"""
import secrets, sys
d = lambda n: secrets.randbelow(n) + 1
def nd(q, f):
    r = [d(f) for _ in range(q)]; return sum(r), r
def ex1():
    ch = [d(20)]
    while ch[-1] == 20: ch.append(d(20))
    return ch
def j2():
    a, b = ex1(), ex1(); return sum(a) + sum(b), [a, b]

modo = sys.argv[1] if len(sys.argv) > 1 else 'dormindo'
PVMAX = 420; pv = 324; DF = 44; RD = 4
ferido = {'Moreth': 0, 'Bjarkunn': 0, 'Draron': 0, 'Mamiltia': 0, 'Ferir': 0}
HER = {'Moreth': dict(pv=600, df=50, rd=8), 'Bjarkunn': dict(pv=180, df=28, rd=4), 'Draron': dict(pv=150, df=26, rd=4)}
vento = False; fim = None; rodada = 0
print(f'O SINO · o ZESRETH {pv}/{PVMAX} · Defesa {DF} · RD {RD} · modo: {modo}')

def golpe_moreth(crit_auto=False, primeiro=False):
    global pv
    if crit_auto:
        s, r = nd(2, 10); br = s * 3 + 15 + 46; rd = RD // 2
        fogo = nd(1, 6)[0] if primeiro else 0
        liq = max(br - rd, 0) + fogo; pv -= liq; ferido['Moreth'] += liq
        print(f'  MORETH (dorme: crítico) {r}×3+15+46={br} − RD {rd}' + (f' + fogo 1d6 [{fogo}]' if fogo else '') + f' = {liq} → {pv}')
        return
    if vento:
        print('  MORETH: o aço passa pelo vento (Corpo de Vento): nada'); return
    t, ch = j2(); nat = (ch[0][0], ch[1][0])
    crit = (nat[0] == 20 and nat[1] >= 11) or (nat[1] == 20 and nat[0] >= 11)
    if (nat[0] == 1 and nat[1] <= 10) or (nat[1] == 1 and nat[0] <= 10) or (t + 44 < DF + 14 and not crit):
        print(f'  MORETH {ch}+44={t+44} vs {DF+14}: erra'); return
    q = 2 if crit else 1; s, r = nd(q, 10); br = s * 3 + 15 + 46; rd = RD // 2 if crit else RD
    liq = max(br - rd, 0); pv -= liq; ferido['Moreth'] += liq
    print(f'  MORETH {ch}+44={t+44} vs {DF+14}: ACERTA{" CRÍTICO" if crit else ""} {r}×3+61={br} − RD {rd} = {liq} → {pv}')

def magia(nome, q, mult, at, auto=False):
    global pv
    s, r = nd(q, 6); dm = int(s * mult)
    if auto: liq = max(dm - RD, 0); txt = 'em cheio (dorme)'
    else:
        t, ch = j2()
        if ch[0][0] == 1 and ch[1][0] == 1: print(f'  {nome}: {ch} dois 1: nada'); return
        if t + at >= 58: liq = max(dm - RD, 0); txt = f'{ch}+{at}={t+at} vs 58 em cheio'
        else: liq = max(dm // 2 - RD, 0); txt = f'{ch}+{at}={t+at} vs 58 pela metade'
    pv -= liq; ferido[nome] = ferido.get(nome, 0) + liq
    print(f'  {nome}: {q}d6 {r}={s} ×{mult} = {dm}, {txt} −RD → {liq} → {pv}')

def raio():
    alvo = max(('Moreth', 'Bjarkunn', 'Draron'), key=lambda k: ferido[k])
    if ferido[alvo] == 0: alvo = 'Moreth'
    h = HER[alvo]; t, ch = j2(); s, r = nd(20, 6); dm = s * 2
    cheio = t + 38 >= h['df'] + 14
    liq = max((dm if cheio else dm // 2) - h['rd'], 0)
    macico = liq > h['pv'] / 2
    print(f'  ZESRETH: RAIO em {alvo}: {ch}+38={t+38} vs {h["df"]+14} ' + ('EM CHEIO' if cheio else 'pela metade') + f' · 20d6={s}×2={dm} − RD {h["rd"]} = {liq}' + (' · DANO MACIÇO: MORRE' if macico else f' (de {h["pv"]})'))
    return alvo, liq, macico

def fuga():
    global pv, fim
    print('  FOGE: Corpo de Vento, e salta do sino para o escuro')
    t, ch = j2(); s, r = nd(8, 6); dm = s * 20; liq = max(dm - RD, 0)
    print(f'  MAMILTIA: {ch}+134={t+134} vs 58 em cheio · 8d6 {r}={s}×20 = {dm} − RD = {liq} → {pv - liq}')
    pv -= liq; ferido['Mamiltia'] += liq
    if pv <= 0: fim = 'MORTO NO AR (a Mamiltia)'; return
    t, ch = j2(); s, r = nd(16, 6); dm = s * 5
    liq = max((dm if t + 34 >= 58 else dm // 2) - RD, 0); pv -= liq; ferido['Ferir'] += liq
    print(f'  FERIR: {ch}+34={t+34} vs 58 · 16d6={s}×5={dm} → {liq} → {pv}')
    fim = 'MORTO NO AR (o rei)' if pv <= 0 else f'FUGIU PELO AR, ferido ({pv}/{PVMAX})'

if modo == 'dormindo':
    rodada = 1; print('— RODADA 1 (ele dorme: ninguém erra, todo golpe é crítico)')
    for i in range(4):
        golpe_moreth(crit_auto=True, primeiro=(i == 0))
        if pv <= 0: break
    if pv > 0: magia('Bjarkunn', 12, 1.5, 14, auto=True)
    if pv > 0: magia('Draron', 6, 3, 16, auto=True)
    if pv <= 0: fim = 'MORTO DORMINDO, no sino'
mortos = []
while fim is None and rodada < 6:
    rodada += 1; print(f'— RODADA {rodada} (ele está acordado: {pv}/{PVMAX})')
    iz, cz = j2(); im, cm = j2()
    ele_primeiro = iz + 21 > im + 23
    print(f'  iniciativa: Zesreth {cz}+21={iz+21} × Moreth {cm}+23={im+23} → ' + ('ELE PRIMEIRO' if ele_primeiro else 'A CASA PRIMEIRO'))
    def turno_dele():
        global vento
        if pv < PVMAX * 0.25:
            f = d(6); print(f'  abaixo de 25%: d6 [{f}] ' + ('FOGE' if f <= 4 else 'fica e luta'))
            if f <= 4: fuga(); return True
        if not vento and rodada >= 3:
            vento = True; print('  ZESRETH: CORPO DE VENTO (só magia o fere)'); return False
        a, l, m = raio()
        if m: mortos.append(a); HER.pop(a, None); ferido[a] = -1
        return False
    def turno_casa():
        if vento:
            if pv > 0: magia('Moreth (Lança do Sol)', 16, 10, 44)
        else:
            for i in range(4):
                if pv <= 0: return
                golpe_moreth()
        if pv > 0 and 'Bjarkunn' in HER: magia('Bjarkunn', 12, 1.5, 14)
        if pv > 0 and 'Draron' in HER: magia('Draron', 6, 3, 16)
    if ele_primeiro:
        if turno_dele(): break
        turno_casa()
    else:
        turno_casa()
        if pv > 0 and turno_dele(): break
    if pv <= 0 and fim is None: fim = f'MORTO no sino, na rodada {rodada}'
print(f'FIM: {fim} · quem o feriu: ' + ' · '.join(f'{k} {v}' for k, v in ferido.items() if v > 0) + (f' · MORTOS DA CASA: {", ".join(mortos)}' if mortos else ''))
