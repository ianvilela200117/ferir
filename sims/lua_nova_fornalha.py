#!/usr/bin/env python3
"""lua_nova_fornalha.py — A VISÃO sobre a FORNALHA à meia-noite do 400 (regras M2-M4 do envelope 2n). N futuros, sem valor de jogo.
Uso: python3 sims/lua_nova_fornalha.py [N]
"""
import random, sys
N = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
def d(n): return random.randint(1, n)
def ex1():
    t = r = d(20)
    while r == 20: r = d(20); t += r
    return t
def ex2(): return ex1() + ex1()
def nd(q, f): return sum(d(f) for _ in range(q))
def lanca(at, q, f, mult, rd=4):
    a, b = d(20), d(20)
    if a == 1 and b == 1: return 0, 'nada'
    t = a + b + at
    dm = nd(q, f) * mult
    if t >= 58: return max(int(dm) - rd, 0), 'cheio'
    return max(int(dm) // 2 - rd, 0), 'metade'
def fogo(mod):
    r = d(20)
    if r == 1: return 'telhado'
    t = r + mod
    return 'entra' if t <= 5 else 'fora' if t <= 12 else 'contido'
def futuro(rei_patio=False, magos=True, visao=True, portao=False, rei_fogo=False):
    R = dict(rapto=None, herkald='salvo', zes='vivo', draron=False, bjarkunn=False, isolda=False, veio=True)
    pv = 420; vivos_magos = 2
    if portao:
        q = d(6)
        if q >= 5: R['veio'] = False; R['zes'] = 'voltou'; R['fogo'] = fogo(2 + 2 + 4 + (3 if rei_fogo else 0) - 7); return R
        if q >= 3: R['veio'] = False; R['zes'] = 'telhado'; R['fogo'] = fogo(2 + 2 + 4 + (3 if rei_fogo else 0) - 7 - 3); return R
        dm, _ = lanca(134, 8, 6, 20); pv -= dm
        if pv <= 0: R['zes'] = 'morto'
        elif pv < 105 and d(6) <= 4: R['zes'] = 'fugiu'
        else:
            dm, _ = lanca(134, 8, 6, 20); pv -= dm; R['zes'] = 'morto' if pv <= 0 else 'fugiu'
        R['fogo'] = fogo(2 + 2 + 4 + (3 if rei_fogo else 0) - 7); return R
    ini_z = ex2() + 21; atrap = 0; dano = {}
    cast = []
    if magos: cast += [('bjarkunn', 14, 12, 6, 1.5, 7), ('draron', 16, 6, 6, 3, 5)]
    if rei_patio: cast += [('rei', 34, 16, 6, 5, 14)]
    for nome, at, q, f, mult, niv in cast:
        dm, como = lanca(at, q, f, mult); pv -= dm; dano[nome] = dm
        if ex2() + niv > ini_z and dm > 0: atrap += 5 if como == 'cheio' else 2
    alvo = max(dano, key=dano.get) if dano and max(dano.values()) > 0 else 'isolda'
    a = ex2() + 38; raio = nd(20, 6) * 2
    PVM = {'bjarkunn': (180, 28, 4), 'draron': (150, 26, 4), 'rei': (376, 45, 10), 'isolda': (300, 40, 8)}[alvo]
    if a < PVM[1] + 14: raio //= 2
    raio = max(raio - PVM[2], 0)
    if alvo in ('bjarkunn', 'draron'):
        if raio > PVM[0] / 2: R[alvo] = True; vivos_magos -= 1
    elif alvo == 'isolda': R['isolda'] = raio
    z = ex2() + 38 + 21 - atrap; i = ex2() + 34 + 11 + (2 if visao else 0) + 2 + 2 + (2 if rei_patio else 0); m = z - i
    if pv <= 0: R['zes'] = 'morto'; R['rapto'] = 'falha'
    elif m >= 10: R['rapto'] = 'limpo'; R['herkald'] = 'levado'; R['zes'] = 'sumiu'
    elif m >= 0:
        R['rapto'] = 'devagar'
        if d(6) <= 2:
            dm, _ = lanca(134, 8, 6, 20); pv -= dm
            if nd(8, 6) * 10 > 110: R['herkald'] = 'morto'
        dm, _ = lanca(34, 16, 6, 5); pv -= dm
        if pv <= 0: R['zes'] = 'morto'; R['herkald'] = R['herkald'] if R['herkald'] == 'morto' else 'salvo (cai ferido)'
        else:
            R['zes'] = 'sumiu'
            if R['herkald'] != 'morto': R['herkald'] = 'levado'
    else:
        R['rapto'] = 'falha'
        dm, _ = lanca(134, 8, 6, 20); pv -= dm
        if pv <= 0: R['zes'] = 'morto'
        elif pv < 105 and d(6) <= 4: R['zes'] = 'fugiu'
        else:
            dm, _ = lanca(134, 8, 6, 20); pv -= dm; R['zes'] = 'morto' if pv <= 0 else 'fugiu'
    sopra = -2 if R['zes'] in ('sumiu',) and False else 0
    R['fogo'] = fogo(2 + vivos_magos * (1 if magos else 1) + 4 + (3 if rei_fogo else 0) - 7 + sopra)
    return R
def regua(rot, **k):
    from collections import Counter
    C = Counter(); F = Counter(); Z = Counter(); mm = 0; iso = 0
    for _ in range(N):
        r = futuro(**k); C[r['herkald']] += 1; F[r['fogo']] += 1; Z[r['zes']] += 1; mm += r['draron'] or r['bjarkunn']; iso += 1 if r['isolda'] else 0
    p = lambda x: f'{100 * x / N:.0f}%'
    print(f'{rot}')
    print('   o Herkald: ' + ' · '.join(f'{k} {p(v)}' for k, v in C.most_common()))
    print('   o Zesreth: ' + ' · '.join(f'{k} {p(v)}' for k, v in Z.most_common()))
    print(f'   um mago da hoste morto pelo Raio: {p(mm)} · o Raio na Isolda: {p(iso)}')
    print('   o fogo na hora: ' + ' · '.join(f'{k} {p(F[k])}' for k in ('contido', 'fora', 'entra', 'telhado')))
print(f'A VISÃO DO GORJAL E A DO REI · a Fornalha, meia-noite do 400 · {N} futuros (sem valor de jogo)')
regua('COMO ESTÁ (a Isolda segura o Herkald; o Bjarkunn e o Draron no pátio; a Mamiltia e o rei chegam na 2ª rodada):')
regua('COMO ESTÁ, mas os dois magos da hoste FORA do pátio (não lançam nele):', magos=False)
regua('O REI NO PÁTIO desde o começo (e depois no fogo):', rei_patio=True, rei_fogo=True)
regua('O HERKALD E A TILDE NO PORTÃO, ao lado da Mamiltia (o rei no cais):', portao=True)
regua('O HERKALD E A TILDE NO PORTÃO, ao lado da Mamiltia, e o rei no fogo:', portao=True, rei_fogo=True)
