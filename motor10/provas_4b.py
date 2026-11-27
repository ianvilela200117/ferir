#!/usr/bin/env python3
"""provas_4b.py — MOTOR 10: O BANCO DE PROVAS DO ALICERCE DA ETAPA 4b (as masmorras e o mundo de fantasia; o contrato: projeto/ETAPA_4B.md).

O que o alicerce (onda 1) entregou, conferido aqui:
  O VOCABULÁRIO (as páginas: os 17 caminhos, os eventos, os módulos, a tocha, a gazua e a chave, os traços do povo fora das listas de hoje) · A PESSOA COMUM É A DE HOJE
  (as cinco lutas de semente fixa iguais às do motor de antes; o sorteio dos 16 caminhos e do dom igual ao de hoje) · O POVO NA PESSOA (os verbos, as recusas, o lutador)
  · A LUTA DE QUEM TEM O TRAÇO (vê no escuro, resiste a veneno, a coragem, o golpe pelas costas, a fase "foge") · O DESPOJO PELA CATEGORIA DE QUEM MORREU (MA5, na caça
  também) · O 17º CAMINHO E A SEGUNDA INCLINAÇÃO · A MASMORRA E A DESCIDA NO GRAVADOR (os campos, os invariantes, o segredo, a morte lá dentro) · A ARMADURA TEM CORPO
  · OS MÓDULOS NOVOS (o esqueleto neutro: a MESA de hoje sai igual) · O SAVE DO JOGADOR (numa cópia: abre, rola a manha de quem já nasceu e joga um dia).
As provas rodam em mundos de rascunho (a vila de prova do provas_mundo), nunca num save. O save do jogador (ensaio/) só é LIDO, numa cópia temporária.
Uso: python3 provas_4b.py [N]      (o provas_mundo.py também roda este banco)
"""
import contextlib, copy, io, json, os, random, shutil, sys, tempfile
import tabelas as T
import tabelas_mundo as M
import tabelas_talento as TT
import tabelas_bichos as TB
import tabelas_povos as TP
import tabelas_manha as TMH
import tabelas_masmorra as TMS
import tabelas_criaturas as TC
import estado, ato, turno, teste, talento, luta, bichos, criaturas, caca, oficio
import masmorra, manha, povos, dragoes
import provas_mundo as PM
from itens import item
from pessoas import padrao, veste, ficha, linha

AQUI = os.path.dirname(os.path.abspath(__file__))


def quieto(f, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()): return f(*a, **k)


def recusa(f): return PM.recusa(f)
def gera(E, ef, texto='prova'): return estado.aplica(E, 'gera', ef, texto=texto)
def sn(x): return 'sim' if x else 'NÃO'


@contextlib.contextmanager
def dado_posto(margens):
    """o dado do jogador rolado de verdade, com o total posto à mão (contra + margem): para conferir o que sai quando passa e quando falha"""
    real = teste.rola; fila = list(margens)
    def posto(E, o_que, atributo, contra, mais=0, quem=None, oculto=False, dom=0, **kw):
        r = real(E, o_que, atributo, contra, mais=mais, quem=quem, oculto=oculto, dom=dom, **kw); m = fila.pop(0); r['total'] = contra + m; r['passou'] = m >= 0
        if dom: r['fez'] = r['total'] >= contra and r['total'] - dom < contra
        return r
    teste.rola = posto
    try: yield
    finally: teste.rola = real


def nasce(E, pid, nome, **mais):
    at = dict(Força=60, Agilidade=60, Vigor=60, Vontade=50, Percepção=50, Afinidade=40)
    gera(E, [['pessoa', 'nasce', pid, dict(nome=nome, nivel=10, atributos=at, lugar='vila', **mais)]], f'{nome} nasce')


# ---------------------------------------------------------------- O VOCABULÁRIO ----------------------------------------------------------------
def _vocabulario(n):
    hum = TP.POVOS['humano']
    certo = dict(
        caminhos=len(TT.CAMINHOS) == 17 and TT.NOVOS == ['manha'] and len(TT.ANTIGOS) == 16 and 'manha' in M.OFICIOS and TT.DOM_NOME.get('manha') == 'a mão leve',
        eventos=all(e in M.EVENTOS for e in ('masmorra', 'masmorra_vida', 'dragão')) and all(e in M.MUNDO_SOZINHO for e in ('masmorra_vida', 'dragão')) and 'masmorra' not in M.MUNDO_SOZINHO,
        modulos=all(m in M.MODULOS for m in ('masmorra', 'manha', 'povos', 'dragoes')),
        bens='tocha' in M.BENS and estado.bem_conhecido('tocha') and abs(M.peso_da_peca('gazua') * M.PECA_BASE - 10) < 1e-9 and M.peso_da_peca('chave') == 0,
        itens={'gazua', 'chave'} <= set(estado.TIPOS_ITEM),
        tracos=not set(T.TRACOS_POVO) & set(TB.TRACOS) and not set(T.TRACOS_POVO) & set(T.TRACOS_NOVOS) and 8 <= len(TB.TRACOS) <= 12 and 12 <= len(TB.ESPECIES) <= 16,
        povos=hum['mods'] == {} and hum['tracos'] == [] and hum['coragem'] == 0 and hum['corpo'] == 'gente' and hum['a_favor'] is None and hum['contra'] is None
            and all(sum(r['mods'].values()) == 0 and set(r['tracos']) <= set(T.TRACOS_POVO) and r['corpo'] in TP.CORPOS for r in TP.POVOS.values()),
        paginas=set(TMS.ARMADILHAS) == set(M.ARMADILHAS) and set(TMS.MOLDES) == set(M.MOLDES) and set(TMH.TESTES) == {'escondido', 'escutar', 'achar', 'gazua', 'desarmar', 'arrombar', 'atencao'},
        costas=T.COSTAS == dict(desde=4, acerto=4, dados=3) and TB.NUCLEO_DESDE == 3)
    ruim = [k for k, v in certo.items() if not v]
    return [('B1 O VOCABULÁRIO COMUM (as páginas): 17 caminhos com a manha; os eventos masmorra, masmorra_vida e dragão; os quatro módulos; a tocha; a gazua (10 de prata) e a chave (sem preço); '
             'os traços do povo fora das listas de hoje (o tabelas_bichos segue com 8 a 12 traços e 12 a 16 espécies); o humano neutro e a soma zero; as chaves das páginas da masmorra e do ladino; o golpe pelas costas e o núcleo do Épico',
             'tudo certo' if not ruim else 'ERRADO: ' + ', '.join(ruim), not ruim)]


# ---------------------------------------------------------------- A PESSOA COMUM É A DE HOJE ----------------------------------------------------------------
def _velho(E, pid, inc):
    """o sorteio do talento e do dom como era antes da etapa 4b (16 caminhos)"""
    tal = {}
    for c in TT.ANTIGOS:
        r = estado.sorte(E, f'talento|{pid}|{c}'); d = r.randint(1, 100)
        if c == inc: d = max([d] + [r.randint(1, 100) for _ in range(TT.INCLINACAO - 1)])
        g = next(g for ate, g in TT.TALENTO_D100 if d <= ate)
        if g: tal[c] = g
    r = estado.sorte(E, f'dom|{pid}'); d = r.randint(1, 1000); gd = next((g for ate, g in TT.DOM_D1000 if d <= ate), 0)
    return tal, ({r.choices(TT.ANTIGOS, weights=[TT.DOM_PESO if tal.get(c, 0) >= 1 else 1 for c in TT.ANTIGOS])[0]: gd} if gd else {})


def _comum(n):
    """as cinco lutas de semente fixa (dados/semente_fixa_sem_magia.txt); o sorteio dos 16 caminhos e do dom; o lutador e a ficha do humano"""
    R = 2
    casos = [
        ('iguais', lambda: [veste(padrao('a', 50), arma=('espada', R), armadura=('malha', R), escudo=R)], lambda: [veste(padrao('b', 50), arma=('espada', R), armadura=('malha', R), escudo=R)], 'perto'),
        ('arco', lambda: [veste(padrao('arq', 50, molde='arqueiro'), arma=('arco', R), armadura=('couro', R), arma2=('adaga', R))], lambda: [veste(padrao('inf', 50), arma=('espada', R), armadura=('malha', R), escudo=R)], 'longe'),
        ('lobos', lambda: [veste(padrao('h', 30), arma=('espada', 1), armadura=('malha', 1), escudo=1)], lambda: bichos.bando('lobo', n=4), 'perto'),
        ('cinco', lambda: [veste(padrao(f'a{i}', 40), arma=('lança', 1), armadura=('malha', 1)) for i in range(5)], lambda: [veste(padrao(f'b{i}', 40), arma=('machado', 1), armadura=('couro', 1), escudo=1) for i in range(5)], 'perto'),
        ('serpe', lambda: [veste(padrao(f'h{i}', 60), arma=('espada', R), armadura=('malha', R), escudo=R) for i in range(4)], lambda: [bichos.bicho('serpe')], 'perto')]
    L = []; escada = luta.ESCADA; luta.ESCADA = False       # (a parte 2, fase 1b) a escada do medo é a mudança de propósito da fase, medida no EF7: o contrato (DESENHO, B0) quer a luta de
    try:                                                  # antes "dado por dado, salvo a escada do medo"; com ela ligada, o cinco contra cinco e a serpe mudam (quem fraquejou fica acuado)
      for nome, a, b, ini in casos:
        luta.semente(777); v = []
        for _ in range(150):
            S = luta.nova(a(), b(), inicio=ini, quieto=True); luta.corre(S); v.append((S['fim'], S['r'], sum(f['pv'] for f in S['L'])))
        L.append(f"{nome} {sum(1 for x in v if x[0] == 'A')} {sum(x[1] for x in v)} {sum(x[2] for x in v)}")
    finally: luta.ESCADA = escada
    f = ficha(veste(padrao('x', 50), arma=('espada', R), armadura=('malha', R), escudo=R)); L.append(f"ficha {f['arma']['acerto']} {defesa(f)} {f['pvmax']} {f['folmax']}")
    ref = open(os.path.join(AQUI, 'dados', 'semente_fixa_sem_magia.txt'), encoding='utf-8').read().split('\n')
    lutas_iguais = L == [x for x in ref if x.strip()]
    dif = 0; movidos = 0; total = 0
    for s in (1, 1001, 7):
        E = estado.novo(s)
        for i in range(max(100, n)):
            for inc in (None, 'fio'):
                tal, dm = talento._sorteia(E, f'p{i}', inclinacao=inc); vt, vd = _velho(E, f'p{i}', inc); total += 1
                if {k: g for k, g in tal.items() if k != 'manha'} != vt or (dm != vd and 'manha' not in dm): dif += 1
                movidos += dm != vd
    E = PM.vila(); d = estado.lutador(E, 'eu'); sem = 'tracos' not in d and 'coragem' not in d
    lf = linha(ficha(d)); limpa = not any(t in lf for t in T.TRACOS_POVO) and 'coragem' not in lf and 'manha' not in lf
    return [('B2 A PESSOA COMUM É A DE HOJE: as cinco lutas de semente fixa saem iguais às do motor de antes, número por número (dados/semente_fixa_sem_magia.txt; com a escada do medo desligada, como no B0 da fase 1b); o sorteio dos 16 caminhos de antes e do dom é o mesmo '
             '(o dom só muda quando a segunda sorte o passa à manha); o humano vai à luta sem traço nem coragem, e a ficha dele é a de hoje',
             f"lutas: {'iguais' if lutas_iguais else 'DIFERENTES: ' + ' · '.join(L)}; sorteio de {total} nascidos: {dif} diferentes nos 16 caminhos ou no dom ({movidos} com o dom passado à manha); humano: sem traço {sn(sem)}, ficha limpa {sn(limpa)}",
             lutas_iguais and dif == 0 and sem and limpa)]


def defesa(f):
    from pessoas import defesa as d
    return d(f)


# ---------------------------------------------------------------- O POVO NA PESSOA ----------------------------------------------------------------
def _pessoa(n):
    E = PM.vila(); R = {}
    R['povo em gera'] = not recusa(lambda: gera(E, [['pessoa', 'eu', 'povo', 'poe', 'anão'], ['pessoa', 'eu', 'idade', 'poe', 40]]))
    R['povo fora de gera e mestre: recusado'] = bool(recusa(lambda: estado.aplica(E, 'treinar', [['pessoa', 'eu', 'povo', 'poe', 'elfo']], texto='x')))
    R['povo que não há: recusado'] = bool(recusa(lambda: gera(E, [['pessoa', 'eu', 'povo', 'poe', 'drow']])))
    R['idade acima do povo: recusada'] = bool(recusa(lambda: gera(E, [['pessoa', 'eu', 'idade', 'poe', 301]])))
    R['segunda inclinação no anão: recusada'] = bool(recusa(lambda: gera(E, [['pessoa', 'eu', 'inclinacao2', 'poe', 'manha']])))
    d = estado.lutador(E, 'eu'); R['o anão vai à luta com os traços'] = d.get('tracos') == ['vê no escuro', 'resiste a veneno'] and 'coragem' not in d
    R['a ficha do anão diz os traços'] = 'vê no escuro' in linha(ficha(d))
    R['volta a humano'] = not recusa(lambda: gera(E, [['pessoa', 'eu', 'povo', 'poe', None], ['pessoa', 'eu', 'inclinacao', 'poe', 'fio'], ['pessoa', 'eu', 'inclinacao2', 'poe', 'manha']])) and 'povo' not in E['gente']['eu']
    R['a mesma inclinação duas vezes: recusada'] = bool(recusa(lambda: gera(E, [['pessoa', 'eu', 'inclinacao2', 'poe', 'fio']])))
    R['segunda inclinação fora do personagem: recusada'] = bool(recusa(lambda: nasce(E, 'x', 'Xis', inclinacao2='manha')))
    nasce(E, 'pipa', 'Pipa', povo='pequenino', idade=30); d = estado.lutador(E, 'pipa')
    R['a pequenina nasce com o povo e a coragem'] = E['gente']['pipa'].get('povo') == 'pequenino' and d.get('coragem') == 4 and 'tracos' not in d and 'coragem +4' in linha(ficha(d))
    q = copy.deepcopy(E); q['gente']['pipa']['idade'] = 200; q['gente']['eu']['povo'] = 'drow'; P = estado.valida(q)
    R['o valida pega a idade e o povo tortos'] = any('não vive 200 anos' in x for x in P) and any('povo' in x for x in P)
    R['o estado está inteiro'] = not estado.valida(E)
    ruim = [k for k, v in R.items() if not v]
    return [('B3 O POVO NA PESSOA: o povo e a idade só em gera ou mestre, da tabela e até a vida do povo; a segunda inclinação só no personagem humano, noutro caminho; o lutador leva os traços e a coragem do povo (o nome, não); a ficha os diz; o valida pega o torto',
             'tudo certo' if not ruim else 'ERRADO: ' + ', '.join(ruim), not ruim)]


# ---------------------------------------------------------------- A LUTA DE QUEM TEM O TRAÇO ----------------------------------------------------------------
def _bonus(S, a, e, w):
    vistos = []; real = luta.jogada
    def j(b, crit19=False): vistos.append(b); return dict(total=-99, falha=False, crit=False)
    luta.jogada = j
    try: luta.golpe(S, a, e, w)
    finally: luta.jogada = real
    return vistos[0]


def _luta(n):
    R = {}
    def duelo(tr, arma='espada', tempo=('escuro',), ini='colado'):
        a = veste(padrao('a', 50, tracos=list(tr)), arma=(arma, 2), armadura=('couro', 2)); b = veste(padrao('b', 50), arma=('espada', 2), armadura=('malha', 2))
        S = luta.nova([a], [b], inicio=ini, tempo=list(tempo), quieto=True); A, B = S['L']
        return _bonus(S, A, B, A['arma'])
    g = duelo(['vê no escuro']) - duelo([]); t = duelo(['vê no escuro'], 'arco', ini='longe') - duelo([], 'arco', ini='longe'); c = duelo(['vê no escuro'], tempo=()) - duelo([], tempo=())
    t0 = -T.TEMPO['escuro']['tiro'] * (1 - TP.ESCURO_TIRO)      # o tiro de quem vê no escuro: a fração ESCURO_TIRO do escuro pesa (hoje 1,0: inteiro, nada a menos)
    R[f'vê no escuro: +{g:g} no golpe e +{t:g} no tiro, no escuro (a página dá +{t0:g}); +{c:g} no claro'] = g == 2 and t == t0 and c == 0
    aranha = bichos.bicho('aranha'); vn = {}
    for tr in ([], ['resiste a veneno']):
        S = luta.nova([aranha], [veste(padrao('h', 30, tracos=tr), arma=('espada', 1))], inicio='colado', quieto=True); A, B = S['L']
        luta._depois_do_golpe(S, A, B, A['armas_corpo'][0], 40, None, False); vn[bool(tr)] = (B['veneno'] or [0])[0]
    R[f'resiste a veneno: {vn[True]} por rodada em vez de {vn[False]}'] = vn[False] == max(1, int(40 * TB.VENENO['fracao'])) and vn[True] == max(1, int(40 * TB.VENENO['fracao'] * TP.VENENO))
    S = luta.nova([veste(padrao('p', 30, coragem=4), arma=('espada', 1))], [veste(padrao('q', 30), arma=('espada', 1))], quieto=True)
    R['a coragem do povo vai à ficha da luta'] = S['L'][0].get('coragem') == 4 and not S['L'][1].get('coragem')
    def costas(m, surpresa='B', r=1):
        lad = veste(padrao('lad', 50, maestria={'espada': 4, 'manha': m}), arma=('espada', 2), armadura=('couro', 2))
        S = luta.nova([lad], [veste(padrao('alvo', 50), arma=('espada', 2), armadura=('malha', 2))], inicio='colado', surpresa=surpresa, quieto=True); S['r'] = r; A = S['L'][0]
        e1 = luta._golpe_especial(S, A, A['arma'], ''); e2 = luta._golpe_especial(S, A, A['arma'], ''); return e1, e2
    e1, e2 = costas(4)
    R['o golpe pelas costas: +4 e os dados 3 vezes, uma vez só'] = bool(e1) and e1['nome'] == 'pelas costas' and e1['acerto'] == 4 and e1['dados'] == 3 and e2 is None
    R['sem ele: a manha de Iniciante, sem surpresa, na segunda rodada, ou quando o surpreendido é ele'] = costas(2)[0] is None and costas(4, None)[0] is None and costas(4, 'B', 2)[0] is None and costas(4, 'A')[0] is None
    def lutas(manha_):
        luta.semente(31); v = []
        for _ in range(40):
            S = luta.nova([veste(padrao('l', 50, maestria={'espada': 4, 'manha': manha_}), arma=('espada', 2), armadura=('couro', 2))], [veste(padrao('o', 50), arma=('espada', 2), armadura=('malha', 2), escudo=2)], inicio='colado', quieto=True)
            luta.corre(S); v.append((S['fim'], S['r'], [f['pv'] for f in S['L']]))
        return v
    R['a manha sem surpresa luta igual a quem não a tem, dado por dado'] = lutas(4) == lutas(0)
    fz = [dict(abaixo=0.95, foge=True, perde=['voa'], ganha=['ardente'], diz='desce ao chão em fúria')]
    def grifos(lugar):
        luta.semente(12); fim = []
        for _ in range(12):
            g = bichos.bicho('grifo', fases=copy.deepcopy(fz), lider=True, moral='firme')        # o chefe não foge pelo susto: só a fase o tira da luta
            S = luta.nova([veste(padrao(f'h{i}', 60), arma=('lança', 2), armadura=('malha', 2)) for i in range(3)], [g], inicio='perto', lugar=lugar, quieto=True); luta.corre(S)
            G = S['L'][-1]; fim.append((G['estado'], 'voa' in G['tracos'], 'ardente' in G['tracos']))
        return fim
    fora, covil, corredor = grifos({}), grifos({'sem_saida': 'B'}), grifos({'largura': 1})
    R[f"a fase foge: fora do covil foge pelo ar ({sum(x[0] == 'fugiu' for x in fora)} de {len(fora)}); no covil nunca ({sum(x[0] == 'fugiu' for x in covil)}), e a fúria vale"] = \
        all(x[0] == 'fugiu' for x in fora) and not any(x[0] == 'fugiu' for x in covil) and all(not x[1] and x[2] for x in covil if x[0] != 'fugiu')
    R[f"num corredor não voa, e não foge ({sum(x[0] == 'fugiu' for x in corredor)})"] = not any(x[0] == 'fugiu' for x in corredor)
    ruim = [k for k, v in R.items() if not v]
    return [('B4 A LUTA DE QUEM TEM O TRAÇO, A MANHA OU A FASE: vê no escuro (a metade do escuro), resiste a veneno (a metade), a coragem do povo na ficha, o golpe pelas costas (E1 a), a fase "foge" do que voa (E3 a); quem não tem, luta igual',
             ' · '.join(k for k in R) if not ruim else 'ERRADO: ' + ' · '.join(ruim), not ruim)]


# ---------------------------------------------------------------- O DESPOJO PELA CATEGORIA (MA5) ----------------------------------------------------------------
def _despojo(n):
    R = {}; torto = []
    for esp, e in list(TB.ESPECIES.items()) + list(TC.ESPECIES.items()):
        for s in range(4):
            a = bichos.despojo(esp, random.Random(s)); b = bichos.despojo(esp, random.Random(s), cat=None); c = bichos.despojo(esp, random.Random(s), cat=e['cat'])
            if not (a[0] == b[0] == c[0] and (a[1] or {}).get('cat') == (b[1] or {}).get('cat') == (c[1] or {}).get('cat')): torto.append(esp)
    R[f'na categoria da espécie, a tabela de hoje com os mesmos dados ({len(TB.ESPECIES) + len(TC.ESPECIES)} espécies)'] = not torto
    k = lambda esp, cat: set(bichos.despojo(esp, random.Random(1), cat=cat)[0])
    R['o cavaleiro da cova feito Comum: metal e osso Comuns'] = k('cavaleiro-da-cova', 0) == {'metal:0', 'osso:0'}
    R['o esqueleto feito Raro: sucata Rara'] = k('esqueleto', 2) == {'osso:2', 'metal:2'}
    R['a gárgula feita Comum, o golem feito Raro (a matéria de outra categoria anda junto)'] = k('gárgula', 0) == {'osso:0', 'metal:0'} and k('golem-de-barro', 2) == {'metal:1'}
    R['a mesma quantidade'] = sum(bichos.despojo('cavaleiro-da-cova', random.Random(1), cat=0)[0].values()) == sum(bichos.despojo('cavaleiro-da-cova', random.Random(1))[0].values())
    s2, s4 = bichos.despojo('serpe', random.Random(3), cat=2)[1], bichos.despojo('serpe', random.Random(3), cat=4)[1]
    R['o núcleo só do Épico para cima, na categoria de quem morreu'] = s2 is None and s4 is not None and s4['cat'] == 4
    E = PM.vila(); d = tempfile.mkdtemp(prefix='m10_4b_caca_'); antes = os.environ.get('MOTOR10_MUNDO')
    try:
        os.environ['MOTOR10_MUNDO'] = d
        gera(E, [['lugar', 'nasce', 'mato', dict(nome='o Mato de Prova', tipo='ermo', vizinhos=['vila'], longe=1, perigo=1, bichos={'goblin': 3}, teto={'goblin': 5})], ['lugar', 'vila', 'vizinhos', 'poe', ['mato']]])
        S = luta.nova([estado.lutador(E, 'eu')], bichos.bando('goblin', n=1, cat=2), inicio='perto', quieto=True); S['L'][1]['estado'] = 'morto'; S['fim'] = 'A'
        arq = os.path.join(d, 'luta_goblin.json'); luta.salva(S, arq)
        s = dict(ermo='mato', casa='vila', quer='caça', alvo=None, restam=2, com=[], dia=1, fase='luta', encontro=dict(especie='goblin', n=1), luta=estado.arq_guarda(arq), lutas=0, parou=None, sangue=None)
        gera(E, [['pessoa', 'eu', 'marca.caca', 'poe', s]]); Rr = quieto(caca.acerta, E, 'eu')
        R[f"na caça, o goblin Raro morto rende {', '.join(sorted(Rr['bens']))}"] = set(Rr['bens']) == {'metal:2', 'couro:2'}
    finally:
        os.environ.pop('MOTOR10_MUNDO', None)
        if antes is not None: os.environ['MOTOR10_MUNDO'] = antes
        shutil.rmtree(d, ignore_errors=True)
    ruim = [k for k, v in R.items() if not v]
    return [('B5 O DESPOJO PELA CATEGORIA DE QUEM MORREU (MA5; o defeito achado pelo projeto A, consertado em toda parte): a matéria na categoria do morto (até a Rara), a mesma quantidade, o núcleo só do Épico para cima; na categoria da espécie, a tabela de hoje; a caça passa a categoria de cada morto',
             ' · '.join(R) if not ruim else 'ERRADO: ' + ' · '.join(ruim) + (f" (tortos: {', '.join(sorted(set(torto))[:5])})" if torto else ''), not ruim)]


# ---------------------------------------------------------------- O 17º CAMINHO E A SEGUNDA INCLINAÇÃO ----------------------------------------------------------------
def _talento(n):
    R = {}
    R['falta: a gente de antes, a manha; a nova e a não rolada, nada'] = talento.falta(dict(talento={'fio': 1})) == ['manha'] and talento.falta(dict(talento={}, marca={'talento_novos': ['manha']})) == [] and talento.falta(dict()) == []
    E = PM.vila(); gera(E, [['pessoa', 'eu', 'talento', 'poe', {'haste': 1}], ['pessoa', 'eu', 'dom', 'poe', {'haste': 1}], ['pessoa', 'eu', 'inclinacao', 'poe', 'fio']])
    R['o caminho velho trocado fora do Mestre: recusado'] = bool(recusa(lambda: gera(E, [['pessoa', 'eu', 'talento', 'poe', {'haste': 2}]])))
    R['a segunda inclinação noutro caminho que não o rolado agora: recusada'] = bool(recusa(lambda: talento.rola_caminho(E, 'eu', 'manha', inclinacao2='tiro')))
    ef = talento.rola_caminho(E, 'eu', 'manha', inclinacao2='manha'); ev = gera(E, ef, 'a manha de quem já nasceu'); p = E['gente']['eu']
    R['rola só a manha: o resto e o dom ficam'] = {k: g for k, g in p['talento'].items() if k != 'manha'} == {'haste': 1} and p['dom'] == {'haste': 1} and p['marca'].get('talento_novos') == ['manha'] and p.get('inclinacao2') == 'manha'
    R['é segredo do Mestre'] = turno.secreto(ev)
    R['não rola duas vezes'] = bool(recusa(lambda: talento.rola_caminho(E, 'eu', 'manha')))
    nasce(E, 'np', 'Nico'); gera(E, [['pessoa', 'np', 'talento', 'poe', {}]])
    R['a segunda inclinação de quem não é o personagem: recusada'] = bool(recusa(lambda: talento.rola_caminho(E, 'np', 'manha', inclinacao2='manha')))
    def pct(povo=None, inc=None, inc2=None, c='manha', alto=True):
        k = 0; N = 20 * max(100, n)
        for s in range(20):
            E = estado.novo(500 + s)
            for i in range(N // 20):
                g = talento._um(E, f'p{i}', c, inc, inc2, povo); k += (g >= 1) if alto else (g <= -1)
        return 100 * k / N
    h, i2, pf, pc, pfi, ac = pct(), pct(inc2='manha'), pct('pequenino'), pct('pequenino', c='haste', alto=False), pct('pequenino', inc='manha'), pct('anão', inc='verde', c='verde')
    R[f'o humano, Jeitoso ou mais na manha em {h:.1f}% (8 a 16)'] = 8 <= h <= 16
    R[f'com a segunda inclinação, {i2:.1f}% (19 a 26)'] = 19 <= i2 <= 26
    R[f'o pequenino a favor da manha, {pf:.1f}%; contra a haste, Lerdo ou pior em {pc:.1f}% (19 a 26)'] = 19 <= pf <= 26 and 19 <= pc <= 26
    R[f'a inclinação no caminho a favor, {pfi:.1f}% (melhor de três: 27 a 37); no contra, {ac:.1f}% (anulam-se: 8 a 16)'] = 27 <= pfi <= 37 and 8 <= ac <= 16
    ruim = [k for k, v in R.items() if not v]
    return [('B6 O 17º CAMINHO E A SEGUNDA INCLINAÇÃO: quem já nasceu rola só a manha (talento.rola_caminho), num evento gera, sem mexer nos 16 nem no dom; a segunda inclinação do personagem humano só no caminho rolado agora (E2 b); a tendência do povo e as inclinações no dado',
             ' · '.join(R) if not ruim else 'ERRADO: ' + ' · '.join(ruim), not ruim)]


# ---------------------------------------------------------------- A MASMORRA E A DESCIDA NO GRAVADOR ----------------------------------------------------------------
def _cripta(E):
    ef = [['lugar', 'nasce', 'cripta', dict(nome='a Cripta de Prova', tipo='masmorra', molde='cripta', niveis=[dict(n=1, cat=0, salas=['c1', 'c2'])], entrada='c1', portas={}, alarme=0, vagantes={'corpo-seco': 1}, longe=1, vizinhos=['vila'])],
          ['lugar', 'nasce', 'c1', dict(nome='a escada', tipo='sala', masmorra='cripta', nivel=1, largura=1)],
          ['lugar', 'nasce', 'c2', dict(nome='o ossário', tipo='sala', masmorra='cripta', nivel=1, bichos={'esqueleto': 3}, estoque={'prata': 10}, guardado=dict(nome='a tigela das oferendas', fechadura=0, aberto=False),
                                        armadilhas=[dict(tipo='dardo', cat=0, onde='porta:c1'), dict(tipo='gás', cat=0, onde='guardado')], segredos=[], chefe=dict(qual='necromante', vivo=True), atento=-1, cat=0)],
          ['lugar', 'c1', 'vizinhos', 'poe', ['c2']], ['lugar', 'c2', 'vizinhos', 'poe', ['c1']],
          ['lugar', 'cripta', 'portas.c1|c2', 'poe', dict(estado='fechada', material='madeira', cat=0, fechadura=None)], ['lugar', 'vila', 'vizinhos', 'poe', ['cripta']],
          ['item', 'nasce', item('chave', 0, 'a chave de prova', abre='c1|c2', onde='c2')]]
    return gera(E, ef, 'a cripta de prova')


def _masmorra(n):
    R = {}; E = PM.vila(); ev = _cripta(E)
    R['a masmorra nasce, o estado inteiro'] = not estado.valida(E)
    R['o evento que a cria é segredo do Mestre'] = turno.secreto(ev)
    R['a caça não a lista como ermo'] = caca.ermos(E, 'vila') == []
    def quebra(f):
        q = copy.deepcopy(E); f(q); return estado.valida(q)
    R['a sala vizinha da vila: pego'] = any('sala por vizinha' in x for x in quebra(lambda q: q['lugares']['vila'].update(vizinhos=['cripta', 'c1'])))
    R['a passagem de um lado só: pega'] = any('dois lados' in x for x in quebra(lambda q: q['lugares']['c2'].update(vizinhos=[])))
    R['a masmorra com bichos: pega'] = any('bichos ou coleta' in x for x in quebra(lambda q: q['lugares']['cripta'].update(bichos={'esqueleto': 1})))
    R['a chave que não abre nada: pega'] = any('abre o que não existe' in x for x in quebra(lambda q: next(it for it in q['itens']['itens'].values() if it['tipo'] == 'chave').update(abre='c1|c9')))
    R['a sala fora do nível: pega'] = bool(quebra(lambda q: q['lugares']['c2'].update(nivel=2)))
    rec = {'armadilha torta': ['lugar', 'c2', 'armadilhas', 'poe', [dict(tipo='serra', cat=0)]], 'alarme 9': ['lugar', 'cripta', 'alarme', 'poe', 9],
           'chefe que não é chefe': ['lugar', 'c2', 'chefe', 'poe', dict(qual='lobo', vivo=True)], 'porta fora de ordem': ['lugar', 'cripta', 'portas.c2|c1', 'poe', dict(estado='fechada')],
           'atento 2': ['lugar', 'c2', 'atento', 'poe', 2], 'o dragão com prata': ['lugar', 'c2', 'dragao', 'poe', dict(nome='o Tição', tipo='serra', idade='jovem', prata=5)],
           'o dragão de cor': ['lugar', 'c2', 'dragao', 'poe', dict(nome='o Tição', tipo='azul', idade='jovem')], 'a gente que passa de 1': ['lugar', 'vila', 'povos', 'poe', {'humano': 0.9, 'pequenino': 0.2}]}
    rr = [k for k, ef in rec.items() if not recusa(lambda: gera(E, [ef]))]
    R['os campos tortos são recusados' + (f" (passaram: {', '.join(rr)})" if rr else '')] = not rr
    R['o dragão e a gente na forma certa entram'] = not recusa(lambda: gera(E, [['lugar', 'c2', 'dragao', 'poe', dict(nome='o Tição', tipo='serra', idade='jovem', dorme_ate=20, punhados=0, vila='vila')], ['lugar', 'vila', 'povos', 'poe', {'humano': 0.9, 'pequenino': 0.1}]]))
    R['o mesmo dragão em dois lugares: pego'] = any('dois lugares' in x for x in quebra(lambda q: q['lugares']['c1'].update(dragao=dict(q['lugares']['c2']['dragao']))))
    gera(E, [['lugar', 'c2', 'dragao', 'poe', None]])
    nasce(E, 'tome', 'Tomé'); nasce(E, 'rute', 'Rute'); gera(E, [['item', 'nasce', item('gazua', 0, dono='tome')]])
    desc = dict(masmorra='cripta', sala='c1', com=['tome', 'rute'], ordem=['eu', 'tome', 'rute'], lances=0, luz=dict(tipo='tocha', quem='eu'), fase='anda', luta=None, caminho=['c1'])
    R['a descida torta é recusada'] = bool(recusa(lambda: gera(E, [['pessoa', 'eu', 'marca.masmorra', 'poe', dict(desc, sala='vila')]])))
    gera(E, [['pessoa', 'eu', 'marca.masmorra', 'poe', desc], ['pessoa', 'tome', 'marca.masmorra', 'poe', dict(de='eu')], ['pessoa', 'rute', 'marca.masmorra', 'poe', dict(de='eu')]])
    R['quem desce está fora, na sala do grupo'] = estado.fora(E, 'eu') == estado.fora(E, 'tome') == estado.onde(E, 'rute') == 'c1' and estado.quem_desce(E, 'tome') == 'eu' and estado.descida(E, 'rute')['sala'] == 'c1'
    R['os atos da vila recusados, com a frase da descida'] = 'na descida' in (recusa(lambda: estado.presente(E, 'eu')) or '') and 'na descida' in '\n'.join(turno._aqui(E))
    R['uma saída de caça com a descida aberta: recusada'] = bool(recusa(lambda: gera(E, [['pessoa', 'eu', 'marca.caca', 'poe', dict(ermo='vila')]])))
    E['turno']['lutas'].append(dict(arq='lutas/l_prova.json', fim=None))
    nota = not recusa(lambda: estado.aplica(E, 'masmorra', [['pessoa', 'eu', 'marca.masmorra', 'poe', dict(desc, fase='luta', luta='lutas/l_prova.json')]], texto='a luta abre'))
    R['a luta da descida: a nota entra, e a tranca diz o comando da masmorra'] = nota and 'masmorra.py luta' in (estado.luta_diz(E) or '')
    E['turno']['lutas'][-1]['fim'] = 'A'; gera(E, [['pessoa', 'eu', 'marca.masmorra', 'poe', desc]])
    gera(E, [['pessoa', 'tome', 'estado', 'poe', 'morto']]); g = next(it for it in E['itens']['itens'].values() if it['tipo'] == 'gazua')
    R['quem ia junto morre: sai da descida, e o que levava fica na sala'] = 'masmorra' not in (E['gente']['tome'].get('marca') or {}) and g.get('onde') == 'c1' and g.get('solto')
    gera(E, [['pessoa', 'eu', 'estado', 'poe', 'morto']]); P = estado.valida(E)
    R['quem comanda morre: solta quem ia junto, e a descida dele fica para as contas'] = 'masmorra' not in (E['gente']['rute'].get('marca') or {}) and 'masmorra' in E['gente']['eu']['marca'] and any('morreu com a descida aberta' in x for x in P)
    ruim = [k for k, v in R.items() if not v]
    return [('B7 A MASMORRA E A DESCIDA NO GRAVADOR (uma cripta de prova posta à mão): os campos novos na forma, os invariantes (nenhuma sala vizinha de vila; a passagem dos dois lados; a chave que abre o que existe), o segredo, '
             'a descida (fora, a tranca da luta, uma saída e uma descida não andam juntas), a morte lá dentro; o dragão e a gente do lugar',
             ' · '.join(R) if not ruim else 'ERRADO: ' + ' · '.join(ruim), not ruim)]


# ---------------------------------------------------------------- A ARMADURA TEM CORPO ----------------------------------------------------------------
def _corpo(n):
    R = {}; E = PM.vila(); E['lugares']['vila']['oficina'] = 1
    nasce(E, 'pipa', 'Pipa', povo='pequenino'); nasce(E, 'bento', 'Bento', maestria={'forja': 4})
    gera(E, [['item', 'nasce', item('armadura', 0, material='malha', dono='pipa')], ['item', 'nasce', item('armadura', 0, material='couro', talhe='miúdo', dono='pipa')], ['item', 'nasce', item('armadura', 0, material='couro', talhe='miúdo', dono='eu')]])
    gente, miuda, miuda_eu = 'i0003', 'i0004', 'i0005'
    R['a de gente na pequenina: recusada'] = bool(recusa(lambda: gera(E, [['item', gente, 'uso', 'poe', 'veste']])))
    R['a miúda na pequenina: serve'] = not recusa(lambda: gera(E, [['item', miuda, 'uso', 'poe', 'veste']]))
    t = recusa(lambda: ato.vestir(E, 'eu', miuda_eu)) or ''
    R['a miúda no humano: o ato a recusa com a frase'] = 'não serve no corpo de Aldric' in t and 'oficio.py ajustar' in t
    R['recortar a peça em uso: recusado'] = bool(recusa(lambda: gera(E, [['item', 'i0002', 'talhe', 'poe', 'miúdo']])))
    R['o talhe fora da armadura: recusado'] = bool(recusa(lambda: gera(E, [['item', 'i0001', 'talhe', 'poe', 'miúdo']])))
    with dado_posto([5]): quieto(oficio.ajustar, E, 'bento', gente, para='pipa')
    R['o ajuste recorta a peça para o corpo de quem a pede'] = E['itens']['itens'][gente].get('talhe') == 'miúdo' and not recusa(lambda: gera(E, [['item', miuda, 'uso', 'poe', None], ['item', gente, 'uso', 'poe', 'veste']]))
    R['o estado está inteiro'] = not estado.valida(E)
    ruim = [k for k, v in R.items() if not v]
    return [('B8 A ARMADURA TEM CORPO (a de gente, a miúda): a que não serve não entra em uso (o gravador e o ato.vestir, com a frase); o ajuste do ferreiro a recorta para quem a pede; a arma e o escudo não têm corpo',
             ' · '.join(R) if not ruim else 'ERRADO: ' + ' · '.join(ruim), not ruim)]


# ---------------------------------------------------------------- OS MÓDULOS NOVOS ----------------------------------------------------------------
FUNCOES = {masmorra: ('de', 'salas', 'gera', 'poe', 'na_vila', 'voce', 'mesa', 'so_mestre', 'retomar', 'recusa_fecha'),
           manha: ('grau', 'gazua_de', 'contra', 'testa', 'mais_barulhento', 'treino', 'feito', 'na_vila', 'voce', 'so_mestre'),
           povos: ('de', 'tracos', 'traços', 've_no_escuro', 'coragem', 'corpo', 'serve', 'manha', 'frase', 'nasce', 'pode_vestir', 'voce', 'mesa', 'so_mestre', 'na_vila'),
           dragoes: ('especie', 'dragao', 'de', 'monta', 'acordado', 'vigilia', 'punhado', 'acorda', 'depois_da_luta', 'poe', 'ameaca', 'mesa', 'so_mestre', 'na_vila')}


def _modulos(n):
    R = {}
    faltam = [f'{m.__name__}.{f}' for m, fs in FUNCOES.items() for f in fs if not callable(getattr(m, f, None))]
    R['as funções do contrato existem' + (f" (faltam: {', '.join(faltam)})" if faltam else '')] = not faltam
    E = PM.vila(); a = turno.mesa(E); velho = estado._MODS
    try:
        estado._MODS = [m for m in estado.modulos() if m.__name__ not in ('masmorra', 'manha', 'povos', 'dragoes')]; b = turno.mesa(E)
    finally: estado._MODS = velho
    R['a MESA de hoje sai igual com os quatro módulos ligados'] = a == b
    gera(E, [['item', 'nasce', item('gazua', 0, dono='eu')]])
    with dado_posto([0, -5]): r1 = manha.testa(E, 'eu', 'gazua', cat=1); r2 = manha.testa(E, 'eu', 'escondido', contra=25, mais=-3, oculto=True)
    R['o dado do ladino: a gazua contra a fechadura uma acima (24 + 8), o escondido com o número de quem vigia'] = r1['contra'] == 32 and r1['ferramenta'] == 'i0003' and r1['passou'] and r2['contra'] == 25 and r2['falhou_feio'] and r2['oculto'] \
        and all(k in r1 for k in ('teste', 'margem', 'falhou_feio', 'ferramenta', 'efeitos'))
    R['sem gazua, um degrau abaixo do Comum'] = manha.contra(E, 'bento' if 'bento' in E['gente'] else 'eu', 'gazua', 0)[0] == 24 + 8 * (0 - TMH.SEM_GAZUA) if 'bento' in E['gente'] else True
    R['o povo no teste do ladino, com o teto'] = povos.manha(dict(povo='gnomo'), 'gazua') == 2 and povos.manha(dict(povo='anão'), 'achar', pedra=True) == 2 and povos.manha(dict(povo='anão'), 'achar') == 0 and povos.manha({}, 'escondido') == 0
    R['nenhum dragão, nenhuma masmorra no esqueleto'] = dragoes.monta(E, 'vila') is None and masmorra.de(E, 'vila') is None
    ruim = [k for k, v in R.items() if not v]
    return [('B9 OS MÓDULOS NOVOS (o esqueleto: masmorra, manha, povos, dragoes): as funções do contrato existem e são neutras; a MESA de hoje sai igual; o dado do ladino já faz a conta do projeto A, com o povo',
             ' · '.join(R) if not ruim else 'ERRADO: ' + ' · '.join(ruim), not ruim)]


# ---------------------------------------------------------------- O SAVE DO JOGADOR ----------------------------------------------------------------
def _recusa_rolar(E, k):
    """rolar de novo o caminho que a pessoa já tem recusa (sys.exit), sem efeito nenhum"""
    try: talento.rola_caminho(E, k, 'manha')
    except SystemExit: return True
    return False


def _save(n):
    src = os.path.join(AQUI, 'ensaio')
    if not os.path.exists(os.path.join(src, 'relogio.json')): return [('B10 O SAVE DO JOGADOR', 'não há save em ensaio/ para conferir', True)]
    d = tempfile.mkdtemp(prefix='m10_4b_save_'); antes = os.environ.get('MOTOR10_MUNDO')
    try:
        shutil.copytree(src, os.path.join(d, 'save')); os.environ['MOTOR10_MUNDO'] = os.path.join(d, 'save')
        E = estado.carrega(); P0 = estado.valida(E); txt = turno.mesa(E); pid = estado.eu(E); dl = estado.lutador(E, pid)
        rolados = [k for k, p in E['gente'].items() if p.get('estado') == 'vivo' and talento.rolado(p)]
        ja = bool(rolados) and all(talento.falta(E['gente'][k]) == [] for k in rolados)      # o save já tem a etapa (o `vila_teste.py fantasia` rodou nele)
        falta_m = ja or all(talento.falta(E['gente'][k]) == ['manha'] for k in rolados)
        antes_tal = {k: (dict(E['gente'][k]['talento']), dict(E['gente'][k].get('dom') or {})) for k in rolados}
        ef = []
        if ja:                          # a manha já rolada: rolar de novo recusa, para cada um, sem mudar nada
            igual = all(_recusa_rolar(E, k) for k in rolados) and all((dict(E['gente'][k]['talento']), dict(E['gente'][k].get('dom') or {})) == antes_tal[k] for k in rolados)
        else:
            for k in rolados: ef += talento.rola_caminho(E, k, 'manha', inclinacao2='manha' if k == pid and E['gente'][k].get('inclinacao') != 'manha' else None)
            if ef: gera(E, ef, 'a manha de quem já nasceu')
            igual = all({c: g for c, g in E['gente'][k]['talento'].items() if c != 'manha'} == antes_tal[k][0] and (E['gente'][k].get('dom') or {}) == antes_tal[k][1] for k in rolados)
        quieto(PM.dia_de_rotina, E); P1 = estado.valida(E)
        return [('B10 O SAVE DO JOGADOR ABRE (o ensaio/, numa cópia: nada é escrito nele): o estado inteiro, a MESA sai, o Maro vai à luta sem traço; a manha de quem já nasceu rola num evento só, sem mexer nos 16 caminhos nem no dom; e joga um dia',
                 f"{len(E['gente'])} pessoas; estado {'inteiro' if not P0 else 'QUEBRADO: ' + P0[0]}; MESA de {len(txt)} letras; sem traço: {sn('tracos' not in dl)}; {len(rolados)} já rolados, "
                 + (f"o save já tem a manha de todos (o fantasia rodou nele), e rolar de novo recusa: {sn(igual)}; " if ja else f"faltava a manha a todos: {sn(falta_m)}; ")
                 + f"o resto igual: {sn(igual)}; a segunda inclinação do personagem: {E['gente'][pid].get('inclinacao2')}; depois de um dia: {'inteiro' if not P1 else 'QUEBRADO: ' + P1[0]}",
                 not P0 and len(txt) > 200 and 'tracos' not in dl and falta_m and igual and not P1)]
    finally:
        os.environ.pop('MOTOR10_MUNDO', None)
        if antes is not None: os.environ['MOTOR10_MUNDO'] = antes
        shutil.rmtree(d, ignore_errors=True)


def provas(n=300):
    out = []
    for f in (_vocabulario, _comum, _pessoa, _luta, _despojo, _talento, _masmorra, _corpo, _modulos, _save):
        try: out += f(n)
        except (Exception, SystemExit) as x:
            import traceback; out.append((f'{f.__name__}: a prova quebrou', f'{type(x).__name__}: {x} · ' + ' | '.join(traceback.format_exc().splitlines()[-4:-1]).strip(), False))
    return out


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 300
    print('BANCO DE PROVAS DO ALICERCE DA ETAPA 4b (as masmorras e o mundo de fantasia: o vocabulário comum)\n')
    res = provas(n)
    for nome, deu, passa in res: print(f"  {'passa' if passa else 'FALHA'}  {nome}: {deu}")
    print(f'\n{sum(p for _, _, p in res)} de {len(res)} provas passam.')
    return all(p for _, _, p in res)


if __name__ == '__main__':
    import signal; hasattr(signal, 'SIGPIPE') and signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    sys.exit(0 if main() else 1)
