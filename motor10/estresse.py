#!/usr/bin/env python3
"""estresse.py — MOTOR 10: O TESTE DE ESTRESSE DA LUTA. Milhares de lutas montadas ao acaso, com ordens ao acaso, conferindo o que nunca pode acontecer.

Cada luta: de 1 a 6 contra de 1 a 8, todas as armas e categorias, corredores, alto, cobertura, tempo, surpresa, guardas, líderes,
peças com efeito, peças já gastas, ordens ao acaso a cada parada, e o estado indo ao arquivo e voltando.
Em metade das lutas entram BICHOS misturados (bichos.py): bandos inteiros, bichos soltos no meio da gente, bichos do lado da casa, e
bichos fora do comum (outro tamanho, outra categoria, outro couro, outras armas do corpo, traços ao acaso, com ou sem moral de chefe).
Toda luta com bicho guarda o registro, e no fim se conta em quantas cada traço foi visto acontecer (o bote, o veneno, o sopro, a fuga...).
Confere a cada parada: ninguém de pé com PV zero nem acima do máximo · quem o jogador comanda não foge nem se rende pelo dado · o corredor
nunca tem mais do que cabe (cada um toma o seu tanto; o bicho grande demais fica sozinho na casa) nem os dois lados na mesma casa · a
durabilidade não sai da faixa · todo caído tem destino no fim · o corpo do bicho não gasta, não tem registro nem dono · bicho não se rende
nem larga a arma · o chefe e o encurralado não fogem · ninguém se rende a um lado só de bichos.

Depois, A MAGIA (a etapa da magia), com um acaso à parte (as lutas de cima seguem as mesmas): um terço de N lutas com quem lança das quatro tradições, gente
com poção, elixir, amuleto, encanto e veneno na lâmina, povo que lança, bichos com os traços novos (e o que lança), chefes com fases, o ermo do "chamar",
e as ordens de lançar, beber e usar ao acaso (a ordem torta é recusada, e conta). Confere também: a Mana entre zero e o máximo · os prazos dos estados
positivos · o calejo de zero para cima · a cura do dia nunca acima de metade do PV · a carga nunca negativa · quem não tem vida nunca fica caído, não foge
nem se rende · o morto erguido é outro lutador, sem registro no mundo, e o morto segue morto · o campo é de quem está na luta · o que volta ao estado
(poção gasta, elixir, maldição posta) tem a forma do contrato.

Uso: python3 estresse.py [N] [gente]      N = quantas lutas (padrão 3000) · gente: só gente, sem bichos (as mesmas lutas de antes dos bichos)
"""
import sys, json, random, collections
import luta, tabelas as T
import tabelas_bichos as TB
import tabelas_magia as TM
import tabelas_mundo as TMU
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


MARCAS = {'matilha': 'a matilha derruba', 'bote': '(bote)', 'investida': '(investida)', 'veneno': 'o veneno entra em', 'agarra': ' AGARRA ', 'voa': '(no ar)', 'regenera': ' regenera (', 'apavora': '(o pavor:',
          'couraça': '(a couraça não abre)', 'sopro': ' SOPRA', 'foge': ' FOGE (', 'encurralado': 'ENCURRALAD', 'apertado': 'luta sem espaço', 'veneno depois da luta': 'para o veneno depois da luta'}
# por que a luta parou, em palavras inteiras (a frase da parada traz nomes e números: aqui ela vira o motivo)
MOTIVOS = [('a luta vai começar', 'a luta vai começar'), ('rodadas sem novidade', 'três rodadas sem novidade'), ('morreu', 'alguém morreu'), ('caiu', 'alguém caiu'), ('fugiu', 'alguém fugiu'),
           ('se rendeu', 'alguém se rendeu'), ('saiu da luta', 'alguém saiu da luta'), ('abaixo de 50% do PV', 'o comandado abaixo de metade do PV'), ('abaixo de 25% do PV', 'o comandado abaixo de um quarto do PV'),
           ('levou uma ferida', 'o comandado levou uma ferida'), ('está sem fôlego', 'o comandado ficou sem fôlego'), ('fraquejou', 'o comandado fraquejou'), ('é só apanhar', 'o comandado segura onde só apanha'),
           ('quebrou', 'uma peça quebrou'), ('não está mais de pé', 'o alvo da ordem não está mais de pé'), ('agarrou', 'um bicho agarrou o comandado'), ('recuperou o fôlego', 'a ordem de tomar fôlego acabou')]
def motivo(p): return next((nome for marca, nome in MOTIVOS if marca in p), 'outro motivo: ' + p)
FINS = dict(A='a casa ficou com o campo', B='o outro lado ficou com o campo', impasse='impasse', empate='empate', ninguém='ninguém ficou de pé')
fins = collections.Counter(); rod = []; paradas = collections.Counter(); erros = 0; com_bicho = 0; visto = collections.Counter()
N = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 3000
for i in range(N):
    luta.semente(i); A, B, kw = cena(i)
    try:
        tem_bicho = any(p.get('bicho') for p in A + B); com_bicho += tem_bicho
        S = luta.nova(A, B, quieto=(i % 5 != 0 and not tem_bicho), **kw); larg = S['lugar'].get('largura'); passos = 0        # toda luta com bicho guarda o registro: é nele que se vê o traço acontecer
        so_bichos = {lado: all(f.get('bicho') for f in S['L'] if f['lado'] == lado) for lado in 'AB'}
        if tem_bicho: visto['apertado'] += any(MARCAS['apertado'] in a for a in S['avisos'])
        st = luta.corre(S, interativo=True)
        while st == 'parada':
            passos += 1
            assert passos < 400, 'paradas demais'
            for p in S['paradas']: paradas[motivo(p)] += 1
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
                assert not (f['estado'] == 'fugiu' and (f['chao'] or f['preso'])), f"{f['nome']} fugiu no chão ou com a perna presa"
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
print(f"{N} lutas · erros {erros} · como acabaram: {', '.join(f'{FINS.get(k, k)} {v}' for k, v in fins.most_common())} · rodadas: a do meio {rod[len(rod)//2]}, nove em dez até {rod[int(len(rod)*.9)]}, a mais longa {rod[-1]}")
print('por que a luta parou e perguntou (as mais comuns):', ', '.join(f'{k} {v}' for k, v in paradas.most_common(14)))
if COM_BICHOS:
    print(f'lutas com bicho: {com_bicho} · em quantas cada traço esteve em campo:', ', '.join(f"{t} {visto['com o traço ' + t]}" for t in TB.TRACOS))
    print('em quantas lutas com bicho se viu acontecer (pelo registro):', ', '.join(f'{k} {visto[k]}' for k in MARCAS if MARCAS[k]))
    nunca = [k for k in MARCAS if MARCAS[k] and not visto[k]]
    if nunca: print('NÃO SE VIU ACONTECER nestas lutas (rode mais, ou veja a prova do traço no provas.py):', ', '.join(nunca))


# ---------- A MAGIA: as lutas de magia, com um acaso à parte ----------
RM = random.Random(1110)
TRADS = list(T.TRADICOES)
POR_TRAD = {t: [k for k, v in T.FEITICOS.items() if v['de'] in (t, 'todas') and TM.FEITICOS[k]['tipo'] != 'rito'] for t in TRADS}
FORMA = {'arcano': ['varinha', 'cajado'], 'fé': ['símbolo'], 'verde': ['cajado'], 'pacto': ['talismã']}
POCAO = ['cura', 'mana', 'antídoto', 'guarda', 'fúria']


def _magica(kw):
    """a carga, os elixires e o benzido ao acaso"""
    if RM.random() < .4: kw['carga'] = {f'{RM.choice(POCAO)}:{RM.randint(0, 2)}': RM.randint(1, 3) for _ in range(RM.randint(1, 2))}
    if RM.random() < .15: kw['elixires'] = [dict(id=f"elixir {RM.randint(1, 99)}", pocao=RM.choice(['cura', 'mana', 'guarda']), cat=RM.randint(3, 5), nome='elixir')]
    if RM.random() < .1: kw['benzido'] = True
    return kw


def _arma_m():
    mais = {}
    if RM.random() < .25: mais['encantos'] = [dict(feitico=RM.choice(['seta', 'prender', 'escudo', 'bola-de-fogo', 'cura', 'luz', 'raio', 'mau-olhado']), grau=RM.randint(1, 4), feito_por=None, dia=1, gasto=None)]
    if RM.random() < .15: mais['veneno'] = dict(cat=RM.randint(0, 2), ate=10 ** 9)
    if RM.random() < .1: mais['benta'] = 10 ** 9
    return item('arma', RM.randint(0, 5), familia=RM.choice(['adaga', 'espada', 'maça', 'lança', 'machado', 'arco']), **mais)


def lancador(nome):
    t = RM.choice(TRADS); niv = RM.choice([5, 12, 20, 35, 50, 80, 150])
    kw = _magica(dict(feiticos=RM.sample(POR_TRAD[t], RM.randint(1, min(4, len(POR_TRAD[t])))), tradicao=t))
    if RM.random() < .3: kw['mana'] = RM.randint(0, 12)
    if RM.random() < .25: kw['linha'] = 'trás'
    if RM.random() < .2: kw['tracos'] = RM.sample(list(T.TRACOS_NOVOS), 1)
    p = padrao(nome, niv, molde=RM.choice(list(TM.MOLDES)), maestria={t: RM.choice([0, 2, 4, 6, 8]), 'maça': RM.choice([0, 2, 4]), 'espada': RM.choice([0, 2, 4])}, **kw)
    foco = (RM.choice(FORMA[t] if RM.random() < .8 else list(T.FOCOS)), RM.randint(0, 5)) if RM.random() < .85 else None
    arma = _arma_m() if RM.random() < .5 else None
    return veste(p, arma=arma, armadura=(RM.choice(MAT), RM.randint(0, 5)) if RM.random() < .8 else None, escudo=RM.randint(0, 4) if RM.random() < .3 else None,
                 foco=foco, amuleto=RM.randint(0, 5) if RM.random() < .6 else None)


def armado(nome):
    """gente sem feitiço, com o que a magia vende: amuleto, poção, elixir, encanto, veneno na lâmina"""
    p = padrao(nome, RM.choice([5, 20, 50, 80, 150, 300]), molde=RM.choice(list(T.MOLDES)), **_magica({}))
    return veste(p, arma=_arma_m(), armadura=(RM.choice(MAT), RM.randint(0, 6)) if RM.random() < .85 else None, escudo=RM.randint(0, 5) if RM.random() < .4 else None, amuleto=RM.randint(0, 5) if RM.random() < .6 else None)


def povo(nome):
    t = RM.choice(TRADS); kw = dict(feiticos=RM.sample(POR_TRAD[t], RM.randint(1, 2)), tradicao=t) if RM.random() < .4 else {}
    p = padrao(nome, RM.choice([5, 10, 20, 40]), maestria=RM.choice([0, 2, 4]), povo=dict(especie='povo de prova', tamanho=RM.choice(list(TB.TAMANHOS)), couro=RM.choice(list(TB.COUROS)),
               cat=RM.randint(0, 2), coragem=RM.randint(-3, 2), tracos=RM.sample(['noturno', 'sem vida', 'resiste', 'ossos', 'ardente'], RM.randint(0, 2))), **kw)
    return veste(p, arma=(RM.choice(['lança', 'maça', 'espada', 'adaga']), RM.randint(0, 3)), armadura=('couro', RM.randint(0, 3)) if RM.random() < .6 else None, escudo=RM.randint(0, 2) if RM.random() < .4 else None,
                 foco=('talismã', RM.randint(0, 2)) if kw else None)


def bicho_m(nome):
    esp = RM.choice(ESP); e = TB.ESPECIES[esp]; tr = list(e['tracos']) + RM.sample([t for t in T.TRACOS_NOVOS if t not in e['tracos']], RM.randint(1, 3)); mais = {}
    if 'lança' in tr: mais['feiticos'] = RM.sample(['seta', 'prender', 'mau-olhado', 'espinho', 'medo', 'sangria', 'raio'], RM.randint(1, 2))
    if RM.random() < .3: mais['maldicao'] = dict(nome='o toque de {quem}', tipo=RM.choice(TMU.MALDICAO_TIPOS), condicao=dict(tipo=RM.choice(TMU.MALDICAO_CONDICOES)))
    return bichos.bicho(esp, nome=nome, tracos=tr, **mais)


def fases():
    return [dict(abaixo=RM.choice([0.3, 0.5, 0.7]), diz='muda', ganha=RM.sample(list(T.TRACOS_NOVOS), RM.randint(0, 2)), brado=RM.random() < .5, ergue=RM.randint(0, 3),
                 feiticos=RM.sample(['seta', 'raio', 'medo', 'mau-olhado', 'bola-de-fogo'], RM.randint(0, 2)), mana=RM.randint(0, 8)) for _ in range(RM.randint(1, 2))]


def cena_m():
    faz = lambda nome: RM.choice([lancador, lancador, armado, povo, bicho_m, pessoa_m])(nome)
    A = [faz(f'a{k}') for k in range(RM.randint(1, 5))]; B = [faz(f'b{k}') for k in range(RM.randint(1, 6))]
    A[0]['controla'] = True
    if RM.random() < .5: B[0]['fases'] = fases(); B[0]['lider'] = True; B[0]['moral'] = 'firme'
    if len(A) > 1 and RM.random() < .4: A[1]['guarda'] = 'a0'; A[1]['papel'] = 'guarda'
    lugar = {}
    if RM.random() < .4: lugar['largura'] = RM.randint(1, 3)
    for k in ('alto', 'cobertura', 'sem_saida'):
        if RM.random() < .15: lugar[k] = RM.choice('AB')
    kw = dict(inicio=RM.choice(['longe', 'perto', 'colado', 5, 12]), lugar=lugar, tempo=RM.sample(list(T.TEMPO), RM.randint(0, 2)), surpresa=RM.choice([None, None, 'A', 'B']))
    if RM.random() < .3: kw['ermo'] = RM.sample(ESP, RM.randint(1, 4))
    return A, B, kw


def pessoa_m(nome):
    """a gente de sempre (sem nada de magia) no meio da luta de magia"""
    niv = RM.choice([1, 12, 35, 80, 300]); p = padrao(nome, niv, molde=RM.choice(list(T.MOLDES)))
    return veste(p, arma=(RM.choice(FAM), RM.randint(0, 7)), armadura=(RM.choice(MAT), RM.randint(0, 7)) if RM.random() < .8 else None)


def ordem_m(S):
    """uma ordem ao acaso para quem o jogador comanda: as de sempre, e as de lançar, beber e usar (das que ele pode, e às vezes uma torta)"""
    meus = luta.de_pe(S, 'A'); deles = luta.de_pe(S, 'B')
    if not meus: return None
    f = RM.choice(meus); nm = f['nome']; r = RM.random()
    if r < .35 and f.get('feiticos'):
        k = RM.choice(f['feiticos'] + ['raio']); t = TM.FEITICOS[k]['tipo']; txt = f'{nm}: lancar {k}'
        if t == 'area' and RM.random() < .7: txt += f' casa {RM.choice(deles)["x"] if deles else 0}'
        elif t in ('dano', 'poe', 'medo') and deles and RM.random() < .7: txt += f' em {RM.choice(deles)["nome"]}'
        elif t in ('cura', 'escudo', 'bencao', 'seiva', 'amparo') and RM.random() < .5: txt += f' em {RM.choice(meus)["nome"]}'
        if k == 'névoa' and RM.random() < .5: txt += ' lama'
        if RM.random() < .3: txt += ' sempre'
        if RM.random() < .2: txt += ' osso'
        return txt
    if r < .5 and (f.get('carga') or f.get('elixires')):
        b = RM.choice([x.partition(':')[0] for x in f.get('carga') or {}] + [x['pocao'] for x in f.get('elixires') or []] + ['veneno'])
        return f'{nm}: beber {b}' + (f' em {RM.choice(meus)["nome"]}' if RM.random() < .2 else '')
    if r < .6 and f.get('encantos'): return f'{nm}: usar' + (f' em {RM.choice(deles)["nome"]}' if deles and RM.random() < .5 else '')
    ac = RM.choice(ACOES); txt = f'{nm}: {ac}'
    if ac == 'atacar' and deles and RM.random() < .6: txt += ' ' + RM.choice(deles)['nome']
    return txt


def confere_m(S):
    """o que tem de valer sempre numa luta de magia (além do de sempre)"""
    nomes = {f['nome'] for f in S['L']}
    for f in S['L']:
        assert f['estado'] in ('pe', 'caido', 'morto', 'fugiu', 'rendido', 'saiu'), f['estado']
        if f['estado'] == 'pe': assert f['pv'] > 0, f"{f['nome']} de pé com PV {f['pv']}"
        assert f['pv'] <= f['pvmax'], f"{f['nome']} com PV acima do máximo"
        assert f['fol'] <= f['folmax'], 'fôlego acima do máximo'
        if f.get('controla'): assert f['estado'] not in ('fugiu', 'rendido'), 'o comandado fugiu ou se rendeu pelo dado'
        if f.get('feiticos') and f.get('mana_max'): assert 0 <= f['mana'] <= f['mana_max'], f"{f['nome']}: Mana {f['mana']} de {f['mana_max']}"
        for k, x in (f.get('est') or {}).items():
            assert (x is True) or (isinstance(x, int) and x >= 0) or (isinstance(x, list) and x[1] > 0 if k in ('guarda',) else isinstance(x, list) and x[0] > 0), f"{f['nome']}: estado {k} torto ({x})"
        assert f.get('calejo', 0) >= 0, 'calejo negativo'
        assert f.get('curado', 0) <= int(f['pvmax'] * T.CURA_TETO), f"{f['nome']} curado acima do teto ({f['curado']} de {f['pvmax']})"
        assert all(q > 0 for q in (f.get('carga') or {}).values()), f"{f['nome']}: carga zerada ou negativa {f.get('carga')}"
        if 'sem vida' in (f.get('tracos') or []): assert f['estado'] not in ('caido', 'fugiu', 'rendido'), f"{f['nome']} não tem vida e ficou {f['estado']}"
        if 'morto que anda' in f['nome']:
            assert not f.get('id') and 'sem vida' in f['tracos'], 'o morto erguido tem registro, ou tem vida'
            o = luta.por_nome(S, f['nome'].split(', morto que anda')[0]); assert o and o['estado'] == 'morto', 'o morto que se ergueu voltou à vida'
        for m in f.get('maldicoes_postas') or []:
            assert m['passo'] == 1 and m['de'] in TMU.MALDICAO_ORIGENS and m['tipo'] in TMU.MALDICAO_TIPOS and m['condicao']['tipo'] in TMU.MALDICAO_CONDICOES and 0 <= m['cat'] <= 7 and 'id' not in m, f'maldição posta torta: {m}'
        for b, q in (f.get('gastou') or {}).items(): assert isinstance(q, int) and q > 0 and ':' in b, f'poção gasta torta: {b} {q}'
        if f.get('canaliza'): assert f['estado'] in ('pe', 'fugiu', 'rendido', 'saiu'), f"{f['nome']} canaliza caído"
    for v in (S.get('campo') or {}).values(): assert v['quem'] in nomes, 'o campo é de quem não está na luta'
    for it in S['itens'].values(): assert 0 <= it['dur'][0] <= it['dur'][1], 'durabilidade fora'


NM = max(1, N // 3); mfins = collections.Counter(); merros = 0; mc = collections.Counter(); recusas = 0
for i in range(NM):
    luta.semente(100000 + i); A, B, kw = cena_m()
    try:
        S = luta.nova(A, B, quieto=(i % 4 != 0), **kw); assert S.get('magia') or not any(p.get('feiticos') for p in A + B), 'a luta com feitiço não ligou a magia'
        st = luta.corre(S, interativo=True); passos = 0
        while st == 'parada':
            passos += 1
            assert passos < 400, 'paradas demais'
            if RM.random() < .7:
                txt = ordem_m(S)
                if txt:
                    try: luta.ordem(S, txt)
                    except SystemExit: recusas += 1
                if RM.random() < .2: luta.ordem(S, 'grupo: ' + RM.choice(['atacar', 'segurar', 'recuar']))
            if RM.random() < .3: S = json.loads(json.dumps(S))
            st = luta.corre(S, interativo=True)
            confere_m(S)
        confere_m(S)
        assert not any(f['estado'] == 'caido' and not f.get('estavel') for f in S['L']), 'caído sem destino no fim'
        mfins[S['fim']] += 1
        for k, x in (S.get('conta') or {}).items(): mc[k] += x
        mc['com magia'] += bool(S.get('magia'))
    except SystemExit as e:
        merros += 1; print(f'magia #{i} RECUSA: {str(e)[:200]}')
    except Exception as e:
        merros += 1; import traceback; print(f'magia #{i} ERRO: {type(e).__name__}: {e}'); traceback.print_exc(limit=4)
        if merros > 12: break
print(f"lutas de magia: {NM} · erros {merros} · como acabaram: {', '.join(f'{FINS.get(k, k)} {v}' for k, v in mfins.most_common())} · ordens tortas recusadas: {recusas}")
print('o que a magia fez nelas:', ', '.join(f'{k} {mc[k]}' for k in ('lances', 'retrochoque', 'longos', 'conc_perdidos', 'pocoes', 'doses_lamina', 'maldicoes', 'fases', 'erguidos', 'bencaos', 'cura_lances')))
sys.exit(1 if erros or merros else 0)
