"""mede_j.py — as medidas do projeto final da parte J (lutas de ENSAIO no luta_j.py: dado de mentira, com semente; nada é guardado).
Uso: python3 mede_j.py [bandos] [chefes] [tracos] [vila] [N]"""
import sys, random
from mede import *
import chefes as C
from itens import item

args = [a for a in sys.argv[1:] if not a.isdigit()] or ['bandos', 'chefes', 'tracos', 'vila']
N = next((int(a) for a in sys.argv[1:] if a.isdigit()), 400)

def misto(cat, prata=False, pre='m'):
    """o grupo de quatro que não é só espada: dois de espada e escudo, um de maça e escudo, uma arqueira atrás (todos do degrau)"""
    def faz():
        lvl = TC.REF[cat]; at = {'Vontade': 80} if cat >= 3 else None
        L = [veste(padrao(f'{pre}{i + 1}', lvl, atributos=at), arma=('espada', cat), armadura=('malha', cat), escudo=cat) for i in range(2)]
        L.append(veste(padrao(f'{pre}3', lvl, atributos=at), arma=('maça', cat), armadura=('malha', cat), escudo=cat))
        L.append(veste(padrao(f'{pre}4', lvl, molde='arqueiro', atributos=at, linha='trás'), arma=('arco', cat), arma2=('adaga', cat), armadura=('couro', cat)))
        if prata:
            for p in L: p['equip']['arma']['efeitos'].append(dict(chave='prata'))
        return L
    return faz


def sem_traco(que, traco, n=None, **mais):
    """o bando sem um traço (para a prova de cada traço, com ele e sem ele)"""
    def faz():
        if que in TC.TROPA:
            L = CR.faz_bando(que, n=n, **mais)
            for p in L: p['povo']['tracos'] = [t for t in p['povo']['tracos'] if t != traco]
            return L
        e = TB.ESPECIES[que]; return CR.faz_bando(que, n=n, tracos=[t for t in e['tracos'] if t != traco], **mais)
    return faz

# ---------- a vila de teste (as fichas do vila_teste.py) ----------
def maro(elmo=False):
    p = dict(nome='Maro', nivel=5, atributos=dict(Força=70, Agilidade=60, Vigor=70, Vontade=50, Percepção=50, Afinidade=40), maestria={'espada': 2}, equip={}, controla=True)
    return veste(p, arma=('espada', 0), armadura=('malha', 0), escudo=0, elmo=None if elmo else False)
def tome(): return veste(padrao('Tomé', 30, molde='guerreiro', maestria={'lança': 4, 'espada': 2}), arma=('lança', 1), armadura=('malha', 0), escudo=0)
def rute(): return veste(padrao('Rute', 22, molde='arqueiro', maestria={'arco': 4, 'adaga': 2}, linha='trás'), arma=('arco', 1), arma2=('adaga', 0), armadura=('couro', 0), elmo=False)
def bento(): return veste(padrao('Bento', 28, molde='guerreiro', maestria={'martelo': 2}), arma=('martelo', 0), armadura=('couro', 0), elmo=False)
def ivo(): return veste(padrao('Ivo', 14, molde='guerreiro', maestria={'machado': 2}), arma=('machado', 0))

def vila(nome, faz_a, faz_b, n=None, **kw):
    n = n or N; L.semente(7); random.seed(7); r = dict(vence=0, perde=0, m1=0, c1=0, f1=0, alguem=0, campo=0, fugiu=0, rendeu=0); rs = []; nb = 0
    for _ in range(n):
        S = L.nova(faz_a(), faz_b(), quieto=True, **{**dict(inicio='perto'), **kw}); L.corre(S); h = S['L'][0]; As = [f for f in S['L'] if f['lado'] == 'A']; Bs = [f for f in S['L'] if f['lado'] == 'B']; nb = len(Bs)
        r['vence'] += S['fim'] == 'A'; r['perde'] += S['fim'] == 'B'; rs.append(S['r'])
        r['m1'] += h['estado'] == 'morto'; r['c1'] += h['estado'] in ('morto', 'caido'); r['f1'] += h['estado'] in ('morto', 'caido') or len(h['feridas']) > h['feridas_antes']
        r['alguem'] += any(f['estado'] == 'morto' for f in As)
        r['campo'] += sum(f['estado'] in ('morto', 'caido') for f in Bs) if S['fim'] == 'A' else sum(f['estado'] == 'morto' for f in Bs)
        r['fugiu'] += sum(f['estado'] == 'fugiu' for f in Bs); r['rendeu'] += sum(f['estado'] == 'rendido' for f in Bs)
    rs.sort(); p = lambda k: f"{100 * r[k] / n:3.0f}%"
    print(f"{nome:<86} vence {p('vence')} · Maro: morto {p('m1')}, caído ou morto {p('c1')}, ferido {p('f1')} · alguém da casa morto {p('alguem')} · do bando ({nb}): no campo {r['campo'] / n:.1f}, fogem {r['fugiu'] / n:.1f}, rendem-se {r['rendeu'] / n:.1f} · {rs[len(rs) // 2]} rodadas")
    return r

if 'bandos' in args:
    print(f'== OS BANDOS contra o homem do degrau deles ({N} lutas por linha) ==')
    print('GOBLINS (Comuns, grau F). A patrulha: os de faca. O covil: o capataz de peças comuns, um quarto de arco, um quarto de lança e escudo, o resto de faca')
    for k in (2, 3, 4):
        print(diz(f'1 homem Comum (nível 10) × a patrulha de {k}', mede(homens(1, 0), C.patrulha(k), N)))
    print(diz('   × a patrulha de 4, num corredor de um', mede(homens(1, 0), C.patrulha(4), N, lugar=dict(largura=1))))
    print(diz('   × a patrulha de 4, eles surpreendidos', mede(homens(1, 0), C.patrulha(4), N, surpresa='B')))
    print(diz('   × a patrulha de 3 e 1 de arco', mede(homens(1, 0), C.patrulha(4, 1), N)))
    print(diz('   × o covil de 6', mede(homens(1, 0), C.covil(6), N)))
    print(diz('1 homem de conjunto INCOMUM (nível 30) × o covil de 6', mede(homens(1, 1), C.covil(6), N)))
    print(diz('   o mesmo × o covil de 12', mede(homens(1, 1), C.covil(12), N)))
    for k in (6, 9, 12, 16):
        print(diz(f'4 homens Comuns × o covil de {k}', mede(homens(4, 0), C.covil(k), N)))
    print(diz('   4 homens Comuns × o covil de 12, num corredor de dois', mede(homens(4, 0), C.covil(12), N, lugar=dict(largura=2))))
    print(diz('   4 homens Comuns × o covil de 12, no ESCURO (o goblin é noturno)', mede(homens(4, 0), C.covil(12), N, tempo=['escuro'])))
    print(diz('   4 homens Comuns × o covil de 12, eles surpreendidos', mede(homens(4, 0), C.covil(12), N, surpresa='B')))
    print(diz('4 homens INCOMUNS × o covil de 16', mede(homens(4, 1), C.covil(16), N)))
    print('ORCS (Incomuns, grau D): soldados de machado, malha, elmo e escudo; o primeiro é o capitão')
    for k in (2, 3, 5):
        print(diz(f'1 homem Incomum (nível 30) × {k} orcs', mede(homens(1, 1), C.orcs(k), N)))
    print(diz('   1 homem Incomum × 3 orcs, num corredor de um', mede(homens(1, 1), C.orcs(3), N, lugar=dict(largura=1))))
    print(diz('1 homem de conjunto RARO (nível 50) × 3 orcs', mede(homens(1, 2), C.orcs(3), N)))
    print(diz('   o mesmo × 5 orcs', mede(homens(1, 2), C.orcs(5), N)))
    for k, b in ((4, 0), (5, 0), (4, 2)):
        print(diz(f'4 homens Incomuns × {k} orcs e {b} brutos', mede(homens(4, 1), C.orcs(k, b), N)))
    print(diz('4 homens Comuns (nível 10) × 4 orcs', mede(homens(4, 0), C.orcs(4), N)))
    print(diz('4 homens RAROS × 5 orcs e 2 brutos', mede(homens(4, 2), C.orcs(5, 2), N)))
    print(diz('4 homens RAROS × 10 orcs e 2 brutos', mede(homens(4, 2), C.orcs(10, 2), N)))
    print()

if 'chefes' in args:
    print(f'== OS CHEFES com os lacaios contra um grupo de quatro ({N} lutas por linha). "arte": por luta, as que foram anunciadas, as cortadas, e a fase mais funda vista ==')
    def ch(nome, a, b, **kw):
        m = mede(a, b, N, **kw); print(diz(nome, m) + f" · artes {m['artes']:.1f} (longas {m['anunciadas']:.2f}, cortadas {m['cortadas']:.2f}; contra a Firmeza {m['tentou']:.1f}, pegam {m['pegou']:.1f}) · fase {m['fases']:.2f}")
        return m
    print('O XAMÃ GOBLIN (pacto de Iniciante, talismã e amuleto Incomuns; 2 guardas de lança; a tropa é Comum). Abaixo de metade do PV ele FOGE, e o bando testa a coragem')
    ch('   4 homens Comuns × o covil de 9 com o xamã', homens(4, 0), C.xama(9))
    ch('   4 homens Comuns × o covil de 9 SEM xamã', homens(4, 0), C.covil(9))
    ch('   4 homens Comuns × o covil de 9 com o xamã sem as artes', homens(4, 0), C.xama(9, artes=False))
    ch('   o grupo misto Comum (dois de espada, um de maça, uma arqueira) × o covil de 9 com o xamã', misto(0), C.xama(9))
    ch('   4 homens Incomuns (o degrau do xamã) × o covil de 9 com o xamã', homens(4, 1), C.xama(9))
    print('O COVIL CHEIO (16 cabeças: o xamã, 2 guardas, o capataz de espada Incomum, 3 de arco, 3 de lança, 6 de faca)')
    ch('   4 homens Comuns', homens(4, 0), C.xama(16, capataz=1))
    ch('   6 homens Comuns', homens(6, 0), C.xama(16, capataz=1))
    ch('   4 homens Incomuns', homens(4, 1), C.xama(16, capataz=1))
    ch('   o grupo misto Incomum', misto(1), C.xama(16, capataz=1))
    ch('   4 homens Incomuns × o covil de 16 sem xamã (capataz de espada Incomum)', homens(4, 1), C.covil(16, espada=1))
    ch('   4 homens Raros', homens(4, 2), C.xama(16, capataz=1))
    print('O SENHOR DA GUERRA ORC (machado Raro e escudo Raro do Livro; a tropa é Incomum). O ITEM DECIDE:')
    orc1 = lambda cat: (lambda: [CR.povo('orc', nome='o orc', arma=item('arma', cat, familia='machado'))])
    ch('   1 homem Incomum × 1 orc comum (machado Incomum)', homens(1, 1), orc1(1))
    ch('   1 homem Incomum × o MESMO orc com um machado Raro na mão', homens(1, 1), orc1(2))
    ch('   4 homens Incomuns × o capitão comum e 3 orcs', homens(4, 1), C.orcs(4))
    ch('   4 homens Incomuns × o senhor com um machado INCOMUM e 3 orcs', homens(4, 1), C.senhor(3, 0, 0, arma=1))
    ch('   4 homens Incomuns × o senhor com o machado RARO e 3 orcs', homens(4, 1), C.senhor(3, 0, 0))
    print('   A GUARDA DO SENHOR (ele, 6 orcs, 2 brutos, 2 goblins de arco = 11) e O ACAMPAMENTO DE GUERRA (ele, 8 orcs, 3 brutos, 3 de arco = 15)')
    ch('   1 homem Incomum × o senhor SOZINHO, com o machado Raro', homens(1, 1), C.senhor(sozinho=True))
    ch('   1 homem Incomum × o mesmo orc com um machado INCOMUM', homens(1, 1), C.senhor(sozinho=True, arma=1))
    ch('   1 homem Raro × o senhor sozinho, com o machado Raro', homens(1, 2), C.senhor(sozinho=True))
    ch('   4 homens Incomuns (o degrau da tropa) × a guarda', homens(4, 1), C.senhor(6, 2, 2))
    ch('   8 homens Incomuns × a guarda', homens(8, 1), C.senhor(6, 2, 2))
    ch('   4 homens Raros (o degrau do senhor) × a guarda', homens(4, 2), C.senhor(6, 2, 2))
    ch('   4 homens Raros × o acampamento de guerra', homens(4, 2), C.senhor(8, 3, 3))
    ch('   o grupo misto Raro × o acampamento de guerra', misto(2), C.senhor(8, 3, 3))
    ch('   4 homens Raros × o acampamento, com um capitão comum no lugar do senhor', homens(4, 2), C.orcs(9, 3, 3))
    print('A BRUXA DO BREJO (talismã Raro; 1 trasgo, 3 fogos-fátuos Raros, 4 afogados Incomuns)')
    ch('   4 homens Raros (o degrau dela)', homens(4, 2), C.bruxa())
    ch('   4 homens Raros × a bruxa sem as artes', homens(4, 2), C.bruxa(artes=False))
    ch('   o grupo misto Raro', misto(2), C.bruxa())
    ch('   4 homens Incomuns', homens(4, 1), C.bruxa())
    ch('   4 homens Épicos', homens(4, 3), C.bruxa())
    ch('   4 homens Raros × a bruxa SÓ com o trasgo (os outros mortos antes, um a um)', homens(4, 2), C.bruxa(1, 0, 0))
    print('O NECROMANTE (foco Épico; 2 cavaleiros da cova Épicos de guarda; 8 esqueletos de conjunto Raro)')
    ch('   4 homens Raros (o degrau da tropa)', homens(4, 2), C.necromante(8, 2))
    ch('   4 homens Raros de MAÇA', homens(4, 2, familia='maça'), C.necromante(8, 2))
    ch('   o grupo misto Raro', misto(2), C.necromante(8, 2))
    ch('   4 homens Épicos (o degrau dele)', homens(4, 3), C.necromante(8, 2))
    ch('   4 homens Épicos × o mesmo, sem as artes', homens(4, 3), C.necromante(8, 2, artes=False))
    ch('   o grupo misto Épico', misto(3), C.necromante(8, 2))
    ch('   4 homens Lendários... não: 4 homens ÚNICOS', homens(4, 4), C.necromante(8, 2))
    ch('   4 homens Raros de maça × o necromante SEM cavaleiro, com 6 esqueletos Raros', homens(4, 2, familia='maça'), C.necromante(6, 0))
    print('O SENHOR VAMPIRO (corpo Épico; 3 carniçais, 3 lobos). De noite o campo é escuro, e ele e os carniçais são noturnos')
    NOITE = dict(tempo=['escuro'])
    ch('   4 homens Épicos, de noite', homens(4, 3), C.vampiro(), **NOITE)
    ch('   4 homens Épicos × o vampiro sem as artes, de noite', homens(4, 3), C.vampiro(artes=False), **NOITE)
    ch('   4 homens Épicos, de noite, com LUZ (sem o escuro)', homens(4, 3), C.vampiro())
    ch('   4 homens Épicos com arma de PRATA, de noite', homens(4, 3, prata=True), C.vampiro(), **NOITE)
    ch('   4 homens Épicos, DE DIA (não regenera nem drena)', homens(4, 3), C.vampiro(dia=True))
    ch('   4 homens Épicos com prata, de dia', homens(4, 3, prata=True), C.vampiro(dia=True))
    ch('   4 homens Raros com prata, de dia', homens(4, 2, prata=True), C.vampiro(dia=True))
    ch('   4 homens Únicos, de noite', homens(4, 4), C.vampiro(), **NOITE)
    print('O REI MORTO (espada Única; 2 cavaleiros da cova Épicos de guarda; 4 guardas mortos de conjunto Épico)')
    ch('   4 homens Épicos (o degrau da guarda)', homens(4, 3), C.rei_morto())
    ch('   4 homens Únicos (o degrau dele)', homens(4, 4), C.rei_morto())
    ch('   o grupo misto Único', misto(4), C.rei_morto())
    ch('   4 homens Únicos × o rei sem as artes', homens(4, 4), C.rei_morto(artes=False))
    ch('   4 homens Lendários', homens(4, 5), C.rei_morto())
    print('O DRAGÃO VELHO (o dragão de hoje com roteiro)')
    ch('   4 homens Lendários × o dragão de HOJE (sem roteiro)', homens(4, 5), C.dragao_velho(artes=False))
    ch('   4 homens Lendários × o dragão velho', homens(4, 5), C.dragao_velho())
    ch('   o grupo misto Lendário × o dragão velho', misto(5), C.dragao_velho())
    ch('   6 homens Lendários × o dragão velho', homens(6, 5), C.dragao_velho())
    ch('   4 homens Únicos × o dragão velho', homens(4, 4), C.dragao_velho())
    print()

if 'tracos' in args:
    print(f'== CADA TRAÇO NOVO, com ele e sem ele ({N} lutas por linha): a vitória de quem enfrenta a criatura tem de cair 8 pontos ou mais com o traço ==')
    def par(t, nome, quem, que, n=None, **kw):
        com = mede(quem, cri(que, n), N, **kw)['vence']; sem = mede(quem, sem_traco(que, t, n), N, **kw)['vence']
        print(f"  {t.upper():<11} {nome:<74} vence {com:>3}% com, {sem:>3}% sem: {sem - com:+d}")
    par('sem vida', 'três corpos-secos contra dois homens Comuns', homens(2, 0), 'corpo-seco', 3)
    par('ossos', 'o esqueleto contra um homem Comum de espada', homens(1, 0), 'esqueleto', 1)
    par('ossos', 'seis esqueletos contra quatro homens Comuns de espada', homens(4, 0), 'esqueleto', 6)
    par('imaterial', 'a alma penada contra um homem Incomum', homens(1, 1), 'alma', 1)
    par('imaterial', 'o espectro contra um homem Raro', homens(1, 2), 'espectro', 1)
    par('pede prata', 'o lobisomem contra um homem Raro', homens(1, 2), 'lobisomem', 1)
    par('dreno', 'o espectro contra um homem Raro com arma de prata', homens(1, 2, prata=True), 'espectro', 1)
    par('ardente', 'o elemental do fogo contra um homem Raro', homens(1, 2), 'fogo', 1)
    par('atira', 'a mantícora contra um homem Raro, começando longe', homens(1, 2), 'mantícora', 1, inicio='longe')
    def semn(l, a):
        def faz():
            B = C.goblins(l, a)()
            for p in B: p['povo']['tracos'] = []
            return B
        return faz
    for nome, quem, l, q in (('nove goblins de lança e três de arco contra quatro homens Comuns, no escuro', homens(4, 0), 9, 3), ('dois de lança e dois de arco contra um homem Comum, no escuro', homens(1, 0), 2, 2)):
        com = mede(quem, C.goblins(l, q), N, tempo=['escuro'])['vence']; sem = mede(quem, semn(l, q), N, tempo=['escuro'])['vence']
        print(f"  {'NOTURNO':<11} {nome:<74} vence {com:>3}% com, {sem:>3}% sem: {sem - com:+d}")
    print()

if 'vila' in args:
    print(f'== A VILA DE TESTE ({N} lutas por linha): Maro (nível 5, espada, escudo e malha Comuns, sem elmo), Tomé (30, lança Incomum), Rute (22, arco Incomum), Bento (28, martelo), Ivo (14, machado) ==')
    print('A PATRULHA (os goblins de faca que andam na mata; "arco": um deles de arco)')
    for n_, a in ((1, 0), (2, 0), (3, 0), (3, 1), (4, 0)):
        vila(f'Maro só × a patrulha de {n_}' + (f' (um de arco)' if a else '') + ', sem surpresa', lambda: [maro()], C.patrulha(n_, a))
    for n_, a in ((2, 0), (3, 0), (3, 1), (4, 0)):
        vila(f'Maro só × a patrulha de {n_}' + (f' (um de arco)' if a else '') + ', eles surpreendidos (ele viu primeiro)', lambda: [maro()], C.patrulha(n_, a), surpresa='B')
    vila('Maro só × a patrulha de 4, surpreendidos, numa passagem de um', lambda: [maro()], C.patrulha(4), surpresa='B', lugar=dict(largura=1))
    vila('Maro COM ELMO × a patrulha de 3, surpreendidos', lambda: [maro(True)], C.patrulha(3), surpresa='B')
    vila('Maro só × a patrulha de 3, de NOITE (o escuro), sem surpresa', lambda: [maro()], C.patrulha(3), tempo=['escuro'])
    vila('Maro e Rute × a patrulha de 4 (um de arco), de longe, eles surpreendidos', lambda: [maro(), rute()], C.patrulha(4, 1), surpresa='B', inicio='longe')
    vila('Maro e Rute × a patrulha de 4 (um de arco), sem surpresa, de perto', lambda: [maro(), rute()], C.patrulha(4, 1))
    vila('Maro e Tomé × a patrulha de 4 (um de arco), sem surpresa, de perto', lambda: [maro(), tome()], C.patrulha(4, 1))
    print('A TOCA (o covil de começo, 9 cabeças: o capataz de espada Incomum, 2 de arco, 2 de lança, 4 de faca)')
    toca = lambda: C.covil(9, espada=1)
    vila('Maro só, de dia, sem surpresa', lambda: [maro()], toca())
    vila('Maro e Rute, de madrugada (eles surpreendidos)', lambda: [maro(), rute()], toca(), surpresa='B')
    vila('Maro, Tomé e Rute, de dia, sem surpresa', lambda: [maro(), tome(), rute()], toca())
    vila('Maro, Tomé e Rute, de madrugada (eles surpreendidos)', lambda: [maro(), tome(), rute()], toca(), surpresa='B')
    vila('Maro, Tomé e Rute, na boca da toca (corredor de dois), sem surpresa', lambda: [maro(), tome(), rute()], toca(), lugar=dict(largura=2))
    vila('Maro, Tomé e Rute, de NOITE, sem surpresa (o escuro é deles)', lambda: [maro(), tome(), rute()], toca(), tempo=['escuro'])
    vila('Maro, Tomé, Rute e Bento, de madrugada', lambda: [maro(), tome(), rute(), bento()], toca(), surpresa='B')
    vila('Maro, Tomé e Rute × a toca de 6 (depois de duas patrulhas mortas), de madrugada', lambda: [maro(), tome(), rute()], C.covil(6, espada=1), surpresa='B')
    vila('Maro, Tomé e Rute × a toca crescida (13 cabeças), de madrugada', lambda: [maro(), tome(), rute()], C.covil(13, espada=1), surpresa='B')
    print('A TOCA COM O XAMÃ (o covil que ninguém incomodou, 16 cabeças: o xamã, 2 guardas, o capataz, 3 de arco, 3 de lança, 6 de faca)')
    cheio = lambda: C.xama(16, capataz=1)
    vila('Maro, Tomé e Rute, de madrugada', lambda: [maro(), tome(), rute()], cheio(), surpresa='B')
    vila('Maro, Tomé, Rute, Bento e Ivo, de madrugada', lambda: [maro(), tome(), rute(), bento(), ivo()], cheio(), surpresa='B')
    vila('Maro, Tomé, Rute, Bento e Ivo, de dia, sem surpresa', lambda: [maro(), tome(), rute(), bento(), ivo()], cheio())
    vila('Maro, Tomé e Rute × o covil de 12 com o xamã, de madrugada', lambda: [maro(), tome(), rute()], C.xama(12, capataz=1), surpresa='B')
    vila('o xamã e os 2 guardas, pegos fora da toca × Maro e Rute, de longe, surpreendidos', lambda: [maro(), rute()], C.xama(3), surpresa='B', inicio='longe')
    print('A COVA VELHA (os mortos não fogem; corredor; escuro, a não ser com tocha)')
    esq = lambda k, g=False: (lambda: ([CR.povo('esqueleto', nome='o guardião da cova', cat=1, nivel=20, maestria=2, lider=True)] if g else []) + CR.faz_bando('esqueleto', n=k))
    for k in (1, 2, 3):
        vila(f'Maro só × {k} esqueleto(s), corredor de um, com tocha', lambda: [maro()], esq(k), lugar=dict(largura=1))
    vila('Maro só × 2 esqueletos, corredor de um, no escuro', lambda: [maro()], esq(2), lugar=dict(largura=1), tempo=['escuro'])
    vila('Maro com uma MAÇA Comum × 3 esqueletos, corredor de um, com tocha', lambda: [veste(dict(maro(), maestria={'maça': 0}), arma=('maça', 0), armadura=('malha', 0), escudo=0, elmo=False)], esq(3), lugar=dict(largura=1))
    vila('Maro e Bento (martelo) × 4 esqueletos, corredor de dois, com tocha', lambda: [maro(), bento()], esq(4), lugar=dict(largura=2))
    vila('Maro, Tomé e Rute × 4 esqueletos, corredor de dois, com tocha', lambda: [maro(), tome(), rute()], esq(4), lugar=dict(largura=2))
    vila('Maro, Tomé e Bento × 6 esqueletos, corredor de dois, com tocha', lambda: [maro(), tome(), bento()], esq(6), lugar=dict(largura=2))
    vila('Maro, Tomé e Bento × o guardião (conjunto Incomum) e 5 esqueletos, corredor de dois, com tocha', lambda: [maro(), tome(), bento()], esq(5, True), lugar=dict(largura=2))
    vila('Maro, Tomé, Rute e Bento × o guardião e 5 esqueletos, corredor de dois, com tocha', lambda: [maro(), tome(), rute(), bento()], esq(5, True), lugar=dict(largura=2))
    vila('Maro só × 2 corpos-secos, campo aberto, de dia', lambda: [maro()], cri('corpo-seco', 2))
    print('OUTROS (para comparar)')
    vila('Maro só × 1 orc', lambda: [maro()], C.orcs(1, capitao=False))
    vila('Maro, Tomé e Rute × 2 orcs', lambda: [maro(), tome(), rute()], C.orcs(2, capitao=False))
    vila('Maro, Tomé e Rute × 3 orcs', lambda: [maro(), tome(), rute()], C.orcs(3))
    vila('Maro só × 1 alma penada', lambda: [maro()], cri('alma', 1))
    vila('Maro só × 1 fogo-fátuo', lambda: [maro()], cri('fogo-fátuo', 1))
    vila('Maro só × 2 harpias', lambda: [maro()], cri('harpia', 2))
