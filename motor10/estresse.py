#!/usr/bin/env python3
"""estresse.py — MOTOR 10: O TESTE DE ESTRESSE DA LUTA. Milhares de lutas montadas ao acaso, com ordens ao acaso, conferindo o que nunca pode acontecer.

Cada luta: de 1 a 6 contra de 1 a 8, todas as armas e categorias, corredores, alto, cobertura, tempo, surpresa, guardas, líderes,
peças com efeito, peças já gastas, ordens ao acaso a cada parada, e o estado indo ao arquivo e voltando.
Em metade das lutas entram BICHOS misturados (bichos.py): bandos inteiros, bichos soltos no meio da gente, bichos do lado da casa, e
bichos fora do comum (outro tamanho, outra categoria, outro couro, outras armas do corpo, traços ao acaso, com ou sem moral de chefe).
Confere a cada parada: ninguém de pé com PV zero nem acima do máximo · quem o jogador comanda não foge nem se rende pelo dado · o corredor
nunca tem mais do que cabe (cada um toma o seu tanto; o bicho grande demais fica sozinho na casa) nem os dois lados na mesma casa · a
durabilidade não sai da faixa · todo caído tem destino no fim · o corpo do bicho não gasta, não tem registro nem dono · bicho não se rende
nem larga a arma · o chefe e o encurralado não fogem · ninguém se rende a um lado só de bichos.

Uso: python3 estresse.py [N] [gente]      N = quantas lutas (padrão 3000) · gente: só gente, sem bichos (as mesmas lutas de antes dos bichos)
"""
import sys, json, random, collections
import luta, tabelas as T
import tabelas_bichos as TB
import bichos
from pessoas import padrao, veste
from itens import item

R = random.Random(2026)
RB = random.Random(407)             # o acaso dos bichos é à parte: com "gente", as lutas são as mesmas de sempre
COM_BICHOS = 'gente' not in sys.argv[2:]
ESP = list(TB.ESPECIES)
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


def bicho(nome):
    """um bicho ao acaso: quase sempre o da tabela; às vezes fora do comum (outro tamanho, categoria, couro, armas do corpo, traços, moral)"""
    mais = {}
    if RB.random() < .3: mais['tamanho'] = RB.choice(list(TB.TAMANHOS))
    if RB.random() < .3: mais['tracos'] = RB.sample(list(TB.TRACOS), RB.randint(0, 4))
    if RB.random() < .2: mais['cat'] = RB.randint(0, 7)
    if RB.random() < .15: mais['armas'] = RB.sample(list(TB.ARMAS_CORPO), RB.randint(1, 3))
    if RB.random() < .15: mais['couro'] = RB.choice(list(TB.COUROS))
    if RB.random() < .2: mais['moral'] = RB.choice(['testa', 'firme'])
    if RB.random() < .2: mais['linha'] = 'trás'
    if RB.random() < .1: mais['pv'] = RB.randint(1, 40)
    return bichos.bicho(RB.choice(ESP), nome=nome, **mais)


def cena(i):
    na, nb = R.randint(1, 6), R.randint(1, 8); modo = RB.choice(['bando', 'mistura', 'mistura', 'tudo']) if COM_BICHOS and RB.random() < .5 else None
    A = [pessoa(f'a{k}', 'A') if k == 0 or modo is None or RB.random() > .12 else bicho(f'a{k}') for k in range(na)]
    if modo == 'bando':                                     # um bando inteiro de uma espécie, como a caça vai montar (os nomes do bando são dele)
        B = bichos.bando(RB.choice(ESP), RB)
    else: B = [pessoa(f'b{k}', 'B') if modo is None or (modo == 'mistura' and RB.random() < .5) else bicho(f'b{k}') for k in range(nb)]
    na, nb = len(A), len(B)
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


MARCAS = {'matilha': 'a matilha o derruba', 'bote': '(bote)', 'investida': '(investida)', 'veneno': 'está envenenado', 'agarra': ' AGARRA ', 'voa': None, 'regenera': ' regenera (', 'apavora': '(pavor:',
          'couraça': None, 'sopro': ' SOPRA', 'foge': ' FOGE (', 'encurralado': 'ENCURRALADO', 'apertado': 'luta apertado', 'veneno depois da luta': 'para o veneno depois da luta'}
fins = collections.Counter(); rod = []; paradas = collections.Counter(); erros = 0; com_bicho = 0; visto = collections.Counter()
N = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 3000
for i in range(N):
    luta.semente(i); A, B, kw = cena(i)
    try:
        S = luta.nova(A, B, quieto=(i % 5 != 0), **kw); larg = S['lugar'].get('largura'); passos = 0
        tem_bicho = any(f.get('bicho') for f in S['L']); com_bicho += tem_bicho
        so_bichos = {lado: all(f.get('bicho') for f in S['L'] if f['lado'] == lado) for lado in 'AB'}
        if tem_bicho: visto['apertado'] += any('apertado' in a for a in S['avisos'])
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
                assert f['pv'] <= f['pvmax'], f"{f['nome']} com PV acima do máximo"
                if f.get('controla'): assert f['estado'] not in ('fugiu', 'rendido'), 'o comandado fugiu ou se rendeu pelo dado'
                if f.get('bicho'):
                    assert f['estado'] != 'rendido', f"{f['nome']} é bicho e se rendeu"
                    assert not f['sem_arma'], f"{f['nome']} é bicho e largou a arma"
                    if f.get('moral') == 'firme': assert f['estado'] != 'fugiu', f"{f['nome']} tem moral de chefe e fugiu"
                    if S['lugar'].get('sem_saida') == f['lado']: assert f['estado'] != 'fugiu', f"{f['nome']} estava encurralado e fugiu"
                if so_bichos[luta.outro(f['lado'])]: assert f['estado'] != 'rendido', f"{f['nome']} se rendeu a um lado só de bichos"
                if f.get('agarrado'): assert luta.por_nome(S, f['agarrado']), 'agarrado por quem não está na luta'
            for it in S['itens'].values():
                assert 0 <= it['dur'][0] <= it['dur'][1], 'durabilidade fora'
                if it.get('tipo') == 'corpo': assert it['dur'] == [1, 1] and not it.get('id') and not it.get('dono'), 'o corpo do bicho gastou, ou ganhou registro ou dono'
            if larg:
                for lado in 'AB':
                    c = collections.Counter(); q = collections.Counter()
                    for f in luta.de_pe(S, lado): c[f['x']] += f.get('ocupa', 1); q[f['x']] += 1
                    assert all(c[x] <= larg or q[x] == 1 for x in c), f'casa com mais do que cabe na largura {larg}: {dict(c)}'
                xa = {f['x'] for f in luta.de_pe(S, 'A')}; xb = {f['x'] for f in luta.de_pe(S, 'B')}
                assert not (xa & xb), 'os dois lados na mesma casa de um corredor'
        assert S['fim'] in ('A', 'B', 'ninguém', 'impasse', 'empate'), S['fim']
        r = luta.resultado(S); fins[S['fim']] += 1; rod.append(S['r'])
        assert not any(f['estado'] == 'caido' and not f.get('estavel') for f in S['L']), 'caído sem destino no fim'
        assert not any('corpo' in q for q in r['quebradas']), 'o corpo do bicho apareceu entre as peças quebradas'
        if tem_bicho:
            for t in set(x for f in S['L'] for x in f.get('tracos', [])): visto['com o traço ' + t] += 1
            txt = '\n'.join(S['log'])
            for k, marca in MARCAS.items():
                if marca and marca in txt: visto[k] += 1
    except SystemExit as e:
        erros += 1; print(f'#{i} RECUSA: {str(e)[:200]}')
    except Exception as e:
        erros += 1; import traceback; print(f'#{i} ERRO: {type(e).__name__}: {e}'); traceback.print_exc(limit=3)
        if erros > 12: break
rod.sort()
print(f'{N} lutas · erros {erros} · fins {dict(fins)} · rodadas: mediana {rod[len(rod)//2]}, p90 {rod[int(len(rod)*.9)]}, máx {rod[-1]}')
print('paradas mais comuns:', paradas.most_common(14))
if COM_BICHOS:
    print(f'lutas com bicho: {com_bicho} · em quantas cada traço esteve em campo:', ', '.join(f"{t} {visto['com o traço ' + t]}" for t in TB.TRACOS))
    print('o que se viu acontecer nas lutas com registro (uma em cada cinco):', ', '.join(f'{k} {visto[k]}' for k in MARCAS if MARCAS[k]))
sys.exit(1 if erros else 0)
