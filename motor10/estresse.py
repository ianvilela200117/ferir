#!/usr/bin/env python3
"""estresse.py — MOTOR 10: O TESTE DE ESTRESSE DA LUTA. Milhares de lutas montadas ao acaso, com ordens ao acaso, conferindo o que nunca pode acontecer.

Cada luta: de 1 a 6 contra de 1 a 8, todas as armas e categorias, corredores, alto, cobertura, tempo, surpresa, guardas, líderes,
peças com efeito, peças já gastas, ordens ao acaso a cada parada, e o estado indo ao arquivo e voltando.
Confere a cada parada: ninguém de pé com PV zero · quem o jogador comanda não foge nem se rende pelo dado · o corredor nunca tem
mais gente que a largura nem os dois lados na mesma casa · a durabilidade não sai da faixa · todo caído tem destino no fim.

Uso: python3 estresse.py [N]      N = quantas lutas (padrão 3000)
"""
import sys, json, random, collections
import luta, tabelas as T
from pessoas import padrao, veste
from itens import item

R = random.Random(2026)
FAM = [f for f in T.FAMILIAS if f != 'punho']
MAT = list(T.MATERIAIS)
ACOES = ['atacar', 'segurar', 'avancar', 'recuar', 'folego']


def pessoa(nome, lado):
    niv = R.choice([1, 5, 12, 20, 35, 50, 80, 150, 300, 500]); fam = R.choice(FAM); cat = R.randint(0, 7)
    kw = {}
    if R.random() < .3: kw['linha'] = 'trás'
    if R.random() < .2: kw['moral'] = 'firme'
    p = padrao(nome, niv, molde=R.choice(list(T.MOLDES)), **kw)
    ef = []
    if R.random() < .3: ef.append(dict(chave=R.choice(['sangra', 'critico_19', 'derruba', 'leve', 'pesa', 'nao_quebra'])))
    arma = item('arma', cat, familia=fam, efeitos=ef)
    arma2 = (R.choice(['adaga', 'espada', 'maça']), R.randint(0, 5)) if R.random() < .4 else None
    arm = None; elmo = None; esc = None
    if R.random() < .85:
        c = R.randint(0, 7); efa = []
        if R.random() < .2: efa.append(dict(chave='devolve', valor=R.randint(1, T.devolve_max(c))))
        if R.random() < .2: efa.append(dict(chave='firme'))
        arm = item('armadura', c, material=R.choice(MAT), efeitos=efa)
        if R.random() < .7: elmo = (R.choice(MAT), R.randint(0, 7))
    if T.FAMILIAS[fam]['maos'] == 1 and R.random() < .6: esc = R.randint(0, 7)
    if R.random() < .15: arma['dur'][0] = R.randint(0, 2)
    return veste(p, arma=arma, arma2=arma2, armadura=arm, elmo=elmo, escudo=esc)


def cena(i):
    na, nb = R.randint(1, 6), R.randint(1, 8)
    A = [pessoa(f'a{k}', 'A') for k in range(na)]; B = [pessoa(f'b{k}', 'B') for k in range(nb)]
    A[0]['controla'] = True
    if na > 1 and R.random() < .5: A[1]['guarda'] = 'a0'; A[1]['papel'] = 'guarda'
    if R.random() < .5: B[0]['lider'] = True
    if na > 2 and R.random() < .5: A[2]['lider'] = True
    lugar = {}
    if R.random() < .4: lugar['largura'] = R.randint(1, 3)
    for k in ('alto', 'cobertura', 'sem_saida'):
        if R.random() < .2: lugar[k] = R.choice('AB')
    tempo = R.sample(list(T.TEMPO), R.randint(0, 2))
    return A, B, dict(inicio=R.choice(['longe', 'perto', 'colado', 5, 12]), lugar=lugar, tempo=tempo, surpresa=R.choice([None, None, 'A', 'B']))


fins = collections.Counter(); rod = []; paradas = collections.Counter(); erros = 0
N = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
for i in range(N):
    luta.semente(i); A, B, kw = cena(i)
    try:
        S = luta.nova(A, B, quieto=(i % 5 != 0), **kw); larg = S['lugar'].get('largura'); passos = 0
        st = luta.corre(S, interativo=True)
        while st == 'parada':
            passos += 1
            assert passos < 400, 'paradas demais'
            for p in S['paradas']: paradas[p.split(' ')[-1] if 'rodadas' in p else ' '.join(w for w in p.split() if not any(c.isdigit() for c in w))[-28:]] += 1
            if R.random() < .7:
                meus = [f['nome'] for f in luta.de_pe(S, 'A')]; deles = [f['nome'] for f in luta.de_pe(S, 'B')]
                if meus:
                    quem = R.choice(meus); ac = R.choice(ACOES + ['guardar'])
                    txt = f'{quem}: {ac}'
                    if ac == 'atacar' and deles and R.random() < .6: txt += ' ' + R.choice(deles)
                    if ac == 'guardar':
                        outros = [m for m in meus if m != quem]
                        txt = f'{quem}: guardar {R.choice(outros)}' if outros else f'{quem}: atacar'
                    if R.random() < .5: txt += ' ' + R.choice(list(T.POSTURAS))
                    luta.ordem(S, txt)
                if R.random() < .3: luta.ordem(S, 'grupo: ' + R.choice(['atacar', 'segurar', 'recuar']))
            if R.random() < .3: S = json.loads(json.dumps(S))          # o estado vai ao arquivo e volta
            st = luta.corre(S, interativo=True)
            # o que tem de valer sempre
            for f in S['L']:
                assert f['estado'] in ('pe', 'caido', 'morto', 'fugiu', 'rendido', 'saiu'), f['estado']
                assert f['fol'] <= f['folmax'], 'fôlego acima do máximo'
                if f['estado'] == 'pe': assert f['pv'] > 0, f"{f['nome']} de pé com PV {f['pv']}"
                if f.get('controla'): assert f['estado'] not in ('fugiu', 'rendido'), 'o comandado fugiu ou se rendeu pelo dado'
            for it in S['itens'].values(): assert 0 <= it['dur'][0] <= it['dur'][1], 'durabilidade fora'
            if larg:
                for lado in 'AB':
                    c = collections.Counter(f['x'] for f in luta.de_pe(S, lado))
                    assert max(c.values() or [0]) <= larg, f'casa com mais gente que a largura: {c}'
                xa = {f['x'] for f in luta.de_pe(S, 'A')}; xb = {f['x'] for f in luta.de_pe(S, 'B')}
                assert not (xa & xb), 'os dois lados na mesma casa de um corredor'
        assert S['fim'] in ('A', 'B', 'ninguém', 'impasse', 'empate'), S['fim']
        r = luta.resultado(S); fins[S['fim']] += 1; rod.append(S['r'])
        assert not any(f['estado'] == 'caido' and not f.get('estavel') for f in S['L']), 'caído sem destino no fim'
    except SystemExit as e:
        erros += 1; print(f'#{i} RECUSA: {str(e)[:200]}')
    except Exception as e:
        erros += 1; import traceback; print(f'#{i} ERRO: {type(e).__name__}: {e}'); traceback.print_exc(limit=3)
        if erros > 12: break
rod.sort()
print(f'{N} lutas · erros {erros} · fins {dict(fins)} · rodadas: mediana {rod[len(rod)//2]}, p90 {rod[int(len(rod)*.9)]}, máx {rod[-1]}')
print('paradas mais comuns:', paradas.most_common(14))
sys.exit(1 if erros else 0)
