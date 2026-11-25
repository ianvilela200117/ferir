#!/usr/bin/env python3
"""historia.py — MOTOR 10, ETAPA FINAL: A HISTÓRIA DO MUNDO, de 400 a 1.000 anos, gerada ano a ano antes de o personagem nascer.

Uma FUNÇÃO PURA da semente e do mapa (os lugares, os ermos e as masmorras que o gera.py já nomeou): mesma semente, mesma história. Não grava nada:
o gera.py põe o que sai daqui no mundo (mundo.casas, mundo.reinos, mundo.cronica, a origem das masmorras, a história das peças altas).

O que sai: os REINOS (o de hoje e os que caíram) · as CASAS NOBRES, com a linhagem (quem mandou, de quando a quando, como morreu) e as que caíram ·
as GUERRAS (quem contra quem, quem venceu, o lugar saqueado que virou ruína) · as PESTES e as FOMES · as LENDAS mortas (o feito, onde morreram, a peça que deixaram)
e as três LENDAS VIVAS · as PEÇAS ALTAS (Épicas, Únicas, Lendárias e a Mítica: quem forjou, de mão em mão, ano a ano, até quem tem hoje) · a ORIGEM de cada masmorra
· a CRÔNICA (tudo isso em linhas, por ano: o Mestre lê inteira; a gente do mundo conta pedaços).

  python3 historia.py SEMENTE          mostra a história de um mapa de exemplo (só olha)
"""
import random, sys
import tabelas_regiao as R
import nomes as NM

TIPOS_ALTOS = [('arma', 'espada'), ('arma', 'machado'), ('arma', 'lança'), ('arma', 'arco'), ('arma', 'montante'), ('arma', 'maça'), ('arma', 'martelo'),
               ('armadura', 'malha'), ('armadura', 'placa'), ('escudo', None), ('foco', 'cajado'), ('amuleto', None)]
NOME_PECA = {'espada': ['a Lâmina', 'a Espada', 'o Gume'], 'machado': ['o Machado', 'a Acha'], 'lança': ['a Lança', 'a Haste'], 'arco': ['o Arco'],
             'montante': ['o Montante', 'a Grande Lâmina'], 'maça': ['a Maça', 'o Malho'], 'martelo': ['o Martelo'], 'malha': ['a Cota', 'a Malha'],
             'placa': ['a Couraça', 'o Arnês'], None: ['o Escudo', 'o Broquel'], 'cajado': ['o Cajado', 'o Bordão'], 'amuleto': ['o Amuleto', 'o Selo']}
DE_PECA = ['da Aurora', 'do Juramento', 'da Última Noite', 'do Rei Velho', 'da Serra', 'do Lobo', 'das Cinzas', 'da Viúva', 'do Inverno', 'da Ponte', 'do Eclipse',
           'da Coroa Partida', 'dos Sete', 'da Maré', 'do Corvo', 'do Sangue Antigo', 'da Promessa', 'do Primeiro Fogo', 'da Vigília', 'do Exílio', 'da Fome', 'do Silêncio']
FEITOS = ['matou o {fera} que assolava {lugar}', 'segurou sozinho a ponte de {lugar} contra um bando inteiro', 'desceu à {ruina} e voltou com o que ninguém trouxe',
          'fechou a fenda de onde saíam os mortos, perto de {lugar}', 'levou o povo de {lugar} pela serra no inverno da fome', 'venceu o torneio do rei três anos seguidos',
          'quebrou o cerco de {lugar}', 'expulsou os orcs da serra até o último', 'achou o veio de ferro que fez a riqueza de {lugar}', 'curou a peste em {lugar} com o que sabia do mato']
FERAS = ['dragão da serra', 'verme do brejo', 'grifo', 'basilisco', 'senhor da guerra orc', 'necromante', 'lobisomem', 'gigante', 'hidra']
MORTES = ['na guerra', 'de velho, na cama', 'de peste', 'num duelo', 'afogado na travessia', 'de uma flecha na estrada', 'de febre', 'à traição, por um parente',
          'num desabamento', 'caçando na serra']
COMO_PASSA = ['herdou', 'tomou em guerra', 'comprou', 'achou', 'ganhou do senhor', 'roubou', 'recebeu como dote', 'tirou do corpo']


def _ano(a): return f'Ano {a}'


def gera(semente, mapa):
    """a história inteira (um dicionário). mapa: {regiao, lugares: [{tag, nome, tipo}], ermos: [{tag, nome, habitat}], masmorras: [{tag, nome, molde, cat}]}"""
    r = random.Random(f'historia|{semente}'); N = NM.Nomes(r, usados=[x['nome'] for x in mapa['lugares']])
    H = R.HISTORIA; anos = r.randint(*H['anos']); ano0 = anos + r.randint(*H['antes']); inicio = ano0 - anos
    lug = mapa['lugares']; cap = next(x for x in lug if x['tipo'] == 'capital'); cid_ = [x for x in lug if x['tipo'] == 'cidade']
    vilas = [x for x in lug if x['tipo'] == 'vila']; peq = [x for x in lug if x['tipo'] in ('aldeia', 'posto')]
    ms = mapa['masmorras']; er = mapa['ermos']
    C = []                                                  # a crônica: (ano, texto, onde, tags)
    def cron(a, t, onde=None, *tags): C.append(dict(ano=a, texto=t, onde=onde, tags=list(tags)))
    # ---- as casas nobres (a do rei e as vassalas), com a linhagem ----
    nn = r.randint(*H['nobres']); casas = {}
    sedes = [cap] + cid_ + r.sample(vilas, min(len(vilas), max(0, nn - 1 - len(cid_))))
    for i in range(nn):
        nome = N.casa(True); cid = 'c_' + NM._sem_acento(nome).replace(' ', '_')
        sede = sedes[i]['tag'] if i < len(sedes) else r.choice(lug)['tag']
        casas[cid] = dict(nome=f'os {nome}', tipo='nobre', fundada=r.randint(inicio, inicio + anos // 3), sede=sede, viva=True, caiu=None, ramo=[], lema=None)
    def chefe_novo(cid, ano, como='herdou'):
        c = casas[cid]; pov = 'humano'
        x = dict(nome=N.gente(pov), nasce=ano - r.randint(18, 40), assume=ano, morre=None, como=None, veio=como); c['ramo'].append(x); return x
    for cid, c in casas.items():
        chefe_novo(cid, c['fundada'], 'fundou'); cron(c['fundada'], f"{c['ramo'][0]['nome']} funda a casa dos {c['nome'][3:]} em {_nm(lug, c['sede'])}.", c['sede'], 'casa', cid)
    # ---- os reinos ----
    reinos = []; nr = r.randint(*H['reinos_mortos'])
    marcos = sorted(r.sample(range(inicio + 30, ano0 - 120), nr))
    a0 = inicio
    for k in range(nr + 1):
        fim = marcos[k] if k < nr else None
        nome = f"o Reino de {N.lugar()}" if k < nr else f"o Reino de {mapa['regiao']}"
        reinos.append(dict(nome=nome, fundado=a0, caiu=fim, casa=None))
        cron(a0, f"Nasce {nome}.", cap['tag'], 'reino')
        if fim: cron(fim, f"Cai {nome}: a coroa se parte, as casas se matam pelo que sobra.", cap['tag'], 'reino', 'queda')
        a0 = (fim or ano0) + 1
    rei = next(k for k, c in casas.items() if c['sede'] == cap['tag']); reinos[-1]['casa'] = rei; reinos[-1]['fundado'] = max(reinos[-1]['fundado'], casas[rei]['fundada'])
    # ---- as lendas mortas (cada uma com a peça que deixou) e as peças altas ----
    itens = []; lendas = []
    def peca(cat, ano, por, onde_forja):
        tipo, qual = r.choice(TIPOS_ALTOS); nome = f"{r.choice(NOME_PECA[qual if qual else (tipo if tipo == 'amuleto' else None)])} {r.choice(DE_PECA)}"
        while any(i['nome'] == nome for i in itens): nome = f"{r.choice(NOME_PECA[qual if qual else (tipo if tipo == 'amuleto' else None)])} {r.choice(DE_PECA)}"
        it = dict(cat=cat, tipo=tipo, qual=qual, nome=nome, ano=ano, por=por, donos=[dict(ano=ano, quem=por, como='forjou')], hoje=None, onde=onde_forja, ate=ano + r.randint(*MAO))
        itens.append(it); return it
    nl = r.randint(*H['lendas']); anos_l = sorted(r.sample(range(inicio + 20, ano0 - 60), nl))
    for a in anos_l:
        pov = r.choices(['humano', 'anão', 'elfo', 'meio-orc', 'pequenino', 'gnomo'], [60, 14, 10, 6, 6, 4])[0]
        nome = N.gente(pov); ondef = r.choice(lug); feito = r.choice(FEITOS).format(fera=r.choice(FERAS), lugar=ondef['nome'], ruina=r.choice(ms)['nome'])
        morre = a + r.randint(10, 50); onde_m = r.choice(ms + lug)
        L = dict(nome=nome, povo=pov, ano=a, morre=morre, feito=feito, onde=ondef['tag'], morreu=onde_m['tag'], peca=None)
        lendas.append(L); cron(a, f"{nome}{_dos(pov)} {feito}.", ondef['tag'], 'lenda')
        cat = r.choices([3, 4, 5], [6, 3, 1])[0]
        if sum(1 for i in itens if i['cat'] == cat) < R.RARO[cat]:
            it = peca(cat, a + r.randint(0, 8), nome, ondef['tag']); L['peca'] = it['nome']
            cron(it['ano'], f"{nome} faz forjar {it['nome']} ({_cat_diz(cat)}).", ondef['tag'], 'peça')
        cron(morre, f"{nome} morre {NM.em(onde_m['nome'])}" + (f"; {L['peca']} fica com o corpo." if L['peca'] and onde_m in ms else '.'), onde_m['tag'], 'lenda', 'morte')
        if L['peca']:                                       # a peça segue com a lenda até a morte dela (o ano a ano faz a perda, na hora certa)
            it = next(i for i in itens if i['nome'] == L['peca']); it['ate'] = morre
            if onde_m in ms: it['fim_lenda'] = (morre, onde_m['tag'], nome)
    # o resto das peças altas que a conta pede (forjadas por mestres de cada século)
    for cat in (3, 4, 5, 6):
        while sum(1 for i in itens if i['cat'] == cat) < R.RARO[cat]:
            a = r.randint(inicio, ano0 - 80 if cat < 6 else inicio + anos // 4)
            por = 'os anões da serra' if cat == 6 else f"o mestre {N.gente(r.choice(['humano', 'anão', 'anão', 'gnomo']))}"
            it = peca(cat, a, por, r.choice(lug)['tag']); cron(a, f"{por[0].upper() + por[1:]} {'forjam' if cat == 6 else 'forja'} {it['nome']} ({_cat_diz(cat)}).", it['onde'], 'peça')
    # ---- o ano a ano: as casas vivem e morrem, as guerras, as pestes, as fomes, as peças mudam de mão ----
    guerras = []; pestes = []; fomes = []; ruinas = {}
    prob_g = r.uniform(*H['guerras_seculo']) / 100; prob_p = r.uniform(*H['pestes_seculo']) / 100; prob_f = r.uniform(*H['fomes_seculo']) / 100
    for a in range(inicio, ano0 + 1):
        vivas = [k for k, c in casas.items() if c['viva'] and c['fundada'] <= a]
        for cid in vivas:                                  # o chefe envelhece e morre; quem herda assume; a casa sem herdeiro cai
            c = casas[cid]; x = c['ramo'][-1]
            if a - x['nasce'] > r.randint(45, 85) and a > x['assume']:
                x['morre'] = a; x['como'] = r.choice(MORTES[1:])
                if cid != rei and r.random() < H['cai_casa'] / 6 and len(vivas) > 4:
                    c['viva'] = False; c['caiu'] = a; cron(a, f"Morre {x['nome']}, o último dos {c['nome'][3:]}: a casa acaba, e as terras passam a outros.", c['sede'], 'casa', 'queda', cid)
                else: y = chefe_novo(cid, a); cron(a, f"Morre {x['nome']} ({x['como']}); {y['nome']} assume a casa dos {c['nome'][3:]}.", c['sede'], 'casa', cid)
        if r.random() < prob_g and len(vivas) >= 2:        # A GUERRA: duas casas, um lugar saqueado (às vezes vira ruína), peças tomadas
            a1, a2 = r.sample(vivas, 2); dura = r.randint(1, 7); ven = r.choice([a1, a2]); per = a2 if ven == a1 else a1
            alvo = r.choice(lug + er); g = dict(ano=a, fim=a + dura, lados=[a1, a2], venceu=ven, perdeu=per, onde=alvo['tag'])
            nome_g = f"guerra {r.choice(['dos Dois Rios', 'das Cinzas', 'do Trigo', 'da Coroa', 'dos Irmãos', 'da Ponte', 'do Inverno Longo', 'das Torres', 'do Sal', 'dos Cem Dias'])}"
            if any(x['nome'] == nome_g for x in guerras): nome_g += f" de {a}"
            g['nome'] = nome_g; guerras.append(g)
            cron(a, f"Começa a {nome_g}: os {casas[a1]['nome'][3:]} contra os {casas[a2]['nome'][3:]}; {_cap(alvo['nome'])} é saquead{'a' if _fem(alvo['nome']) else 'o'}.", alvo['tag'], 'guerra')
            cron(a + dura, f"Acaba a {nome_g}: vencem os {casas[ven]['nome'][3:]}.", alvo['tag'], 'guerra')
            if per != rei and r.random() < 0.3 and sum(1 for k in casas if casas[k]['viva']) > 4:
                casas[per]['viva'] = False; casas[per]['caiu'] = a + dura; cron(a + dura, f"Os {casas[per]['nome'][3:]} não se levantam mais: a casa cai com a guerra.", casas[per]['sede'], 'casa', 'queda', per)
            for it in itens:                                # a peça de quem perdeu pode mudar de mão
                if it['ano'] < a and not it.get('perdida') and it['donos'][-1].get('casa') == per and r.random() < 0.5:
                    q = casas[ven]['ramo'][-1]['nome']; it['donos'].append(dict(ano=a + dura, quem=q, casa=ven, como='tomou em guerra')); it['ate'] = a + dura + r.randint(*MAO)
        if r.random() < prob_p:
            onde = r.choice(lug); pestes.append(dict(ano=a, onde=onde['tag'])); cron(a, f"A peste chega a {onde['nome']}: morre um em cada três.", onde['tag'], 'peste')
        if r.random() < prob_f:
            onde = r.choice(vilas + peq); fomes.append(dict(ano=a, onde=onde['tag'])); cron(a, f"O inverno da fome em {onde['nome']}: o povo come a semente.", onde['tag'], 'fome')
        for it in itens:                                    # A PEÇA PASSA DE MÃO quando acaba o tempo de quem a tem (morre, vende, perde): sem buraco na cadeia
            if it['ano'] >= a: continue
            if it.get('perdida'):                           # a perdida numa masmorra jaz lá; às vezes alguém a acha
                if r.random() < ACHA:
                    quem = N.gente(r.choice(['humano', 'humano', 'anão', 'elfo'])); onde_nm = _nm(lug + ms, it['onde'])
                    it['donos'].append(dict(ano=a, quem=quem, como=f"achou {NM.em(onde_nm)}")); it.pop('perdida'); it['ate'] = a + r.randint(*MAO)
                    cron(a, f"{quem} acha {it['nome']} {NM.em(onde_nm)}.", it['onde'], 'peça')
                continue
            if a < it['ate']: continue
            fl = it.pop('fim_lenda', None)
            if fl:                                          # a lenda morreu numa masmorra: a peça ficou com o corpo
                it['donos'].append(dict(ano=a, quem=None, como=f"ficou com o corpo de {fl[2]} {NM.em(_nm(ms, fl[1]))}")); it['onde'] = fl[1]; it['perdida'] = True; continue
            if r.random() < PERDE:                          # perde-se numa masmorra (quem a tinha morreu lá dentro)
                m = r.choice(ms); it['donos'].append(dict(ano=a, quem=None, como=f"perdeu-se {NM.em(m['nome'])}, com quem a levava")); it['onde'] = m['tag']; it['perdida'] = True; continue
            cs = [k for k in vivas if k in casas]; cid = r.choice(cs) if cs and r.random() < 0.6 else None
            quem = casas[cid]['ramo'][-1]['nome'] if cid else N.gente(r.choice(['humano', 'humano', 'anão', 'elfo']))
            it['donos'].append(dict(ano=a, quem=quem, casa=cid, como=r.choices(COMO_PASSA, PESO_PASSA)[0])); it['ate'] = a + r.randint(*MAO)
    # ---- as três Lendas vivas (os rivais do topo: o gera.py faz a ficha) ----
    vivas_l = []
    for k in range(3):
        pov = r.choices(['humano', 'anão', 'elfo', 'meio-orc'], [60, 18, 14, 8])[0]; nome = N.gente(pov)
        nasce = ano0 - r.randint(40 if pov in ('humano', 'meio-orc') else 90, 60 if pov in ('humano', 'meio-orc') else 260)
        feito = r.choice(FEITOS).format(fera=r.choice(FERAS), lugar=r.choice(lug)['nome'], ruina=r.choice(ms)['nome'])
        vivas_l.append(dict(nome=nome, povo=pov, idade=ano0 - nasce, feito=feito)); cron(ano0 - r.randint(3, 25), f"{nome}{_dos(pov)} {feito}: todo o reino sabe o nome.", None, 'lenda', 'viva')
    # ---- quem tem hoje cada peça alta (o gera.py põe a última mão: o nome de quem é hoje) ----
    lend = [i for i in itens if i['cat'] == 5]; unic = [i for i in itens if i['cat'] == 4]; epic = [i for i in itens if i['cat'] == 3]; mit = [i for i in itens if i['cat'] == 6]
    vass = [k for k, c in casas.items() if c['viva'] and k != rei]
    for k, it in enumerate(lend): it['hoje'] = f'lenda:{k}'
    dest_u = ['lenda:0', 'lenda:1', f'casa:{rei}', 'masmorra']; dest_e = ['veterano'] * 4 + ['lenda:2', 'lenda:0'] + [f'casa:{x}' for x in vass[:2]] + ['masmorra'] * 3 + ['dragao']
    for lista, dest in ((unic, dest_u), (epic, dest_e)):
        for k, it in enumerate(lista):                     # a perdida numa masmorra fica lá; a outra vai a quem a conta pede
            it['hoje'] = f"masmorra:{it['onde']}" if it.get('perdida') and any(m['tag'] == it['onde'] for m in ms) else dest[k % len(dest)]
            if it['hoje'] == 'masmorra': it['hoje'] = 'masmorra:' + r.choice([m['tag'] for m in ms if m['molde'] in ('ruína', 'cripta', 'mina')] or [ms[0]['tag']])
    for it in mit: it['hoje'] = 'calamidade'
    for it in itens: it.pop('perdida', None); it.pop('ate', None); it.pop('fim_lenda', None)
    # ---- a origem de cada masmorra (o que a história diz dela) ----
    for m in ms:
        a = r.randint(inicio + 10, ano0 - 30)
        txt = {'cripta': f"a cripta onde os {r.choice(list(casas.values()))['nome'][3:]} enterravam os seus, selada no {_ano(a).lower()} depois da peste",
               'mina': f"a mina que dava ferro a {r.choice(lug)['nome']}, abandonada no {_ano(a).lower()} quando o fundo desabou e o que morava embaixo subiu",
               'ruína': f"o que sobrou de {N.lugar()}, saqueada no {_ano(a).lower()} na {r.choice(guerras)['nome'] if guerras else 'guerra das casas'}, e nunca mais erguida",
               'toca': f"a velha atalaia que os bichos tomaram no {_ano(a).lower()}, quando a guarda deixou de subir",
               'covil': f"a caverna onde o dragão desceu no {_ano(inicio + 5).lower()}, sobre o ouro {_de(reinos[0]['nome'])}, e dorme desde então"}[m['molde']]
        ruinas[m['tag']] = txt; cron(a if m['molde'] != 'covil' else inicio + 5, txt[0].upper() + txt[1:] + '.', m['tag'], 'ruína')
    C.sort(key=lambda x: x['ano'])
    return dict(semente=semente, ano0=ano0, anos=anos, inicio=inicio, reinos=reinos, casas=casas, rei=rei, guerras=guerras, pestes=pestes, fomes=fomes,
                lendas=lendas, vivas=vivas_l, itens=itens, ruinas=ruinas, cronica=C)


MAO = (6, 45)               # os anos que uma mão segura uma peça alta antes de ela passar (a vida de quem a tem)
PERDE = 0.06                # a chance de, ao passar, a peça se perder numa masmorra (com quem a levava)
ACHA = 0.02                 # por ano, a chance de alguém achar a peça perdida
PESO_PASSA = [40, 10, 14, 6, 6, 10, 4, 10]     # herdou, tomou em guerra, comprou, achou, ganhou do senhor, roubou, recebeu como dote, tirou do corpo
PLURAL = {'anão': 'anões', 'elfo': 'elfos', 'meio-orc': 'meio-orcs', 'pequenino': 'pequeninos', 'gnomo': 'gnomos'}
def _dos(p): return f", dos {PLURAL[p]}," if p in PLURAL else ''
def _cap(x): return x[:1].upper() + x[1:]
def _fem(nome): return nome.split()[0] in ('a', 'as') or (nome.split()[0] not in ('o', 'os') and nome.split()[0].endswith('a'))
def _de(n):
    art, _, resto = n.partition(' ')
    return {'a': 'da ', 'o': 'do ', 'as': 'das ', 'os': 'dos '}[art] + resto if art in ('a', 'o', 'as', 'os') and resto else 'de ' + n
def _nm(lug, tag): return next((x['nome'] for x in lug if x['tag'] == tag), tag)
def _povo_diz(p): return {'humano': 'humano', 'anão': 'anão', 'elfo': 'elfo', 'meio-orc': 'meio-orc', 'pequenino': 'pequenino', 'gnomo': 'gnomo'}[p]
def _cat_diz(c): return ['Comum', 'Incomum', 'Rara', 'Épica', 'Única', 'Lendária', 'Mítica', 'Primordial'][c]


def exemplo(semente=1):
    """um mapa de exemplo (para olhar a história sem gerar o mundo)"""
    r = random.Random(semente); N = NM.Nomes(r)
    lug = [dict(tag=f'L{i}', nome=N.lugar(), tipo=t) for i, t in enumerate(['capital', 'cidade', 'cidade'] + ['vila'] * 5 + ['aldeia'] * 5 + ['posto'] * 3)]
    er = [dict(tag=f'E{i}', nome=N.ermo(h), habitat=h) for i, (h, p) in enumerate(R.ERMOS)]
    ms = [dict(tag=f'M{i}', nome=f'{m}', molde=m, cat=c) for i, (m, c, n, pe) in enumerate(R.MASMORRAS)]
    return dict(regiao=N.lugar(), lugares=lug, ermos=er, masmorras=ms)


if __name__ == '__main__':
    a = sys.argv[1:]
    if len(a) != 1 or not a[0].isdigit(): print(__doc__); sys.exit()
    H = gera(int(a[0]), exemplo(int(a[0])))
    print(f"{H['anos']} anos de história, do ano {H['inicio']} ao {H['ano0']} (o Dia 1). {len(H['casas'])} casas nobres ({sum(not c['viva'] for c in H['casas'].values())} caíram), "
          f"{len(H['reinos'])} reinos, {len(H['guerras'])} guerras, {len(H['pestes'])} pestes, {len(H['lendas'])} lendas mortas, {len(H['itens'])} peças altas.")
    for c in H['cronica']: print(f"  {c['ano']}: {c['texto']}")
    print('\nAS PEÇAS ALTAS:')
    for it in H['itens']: print(f"  {it['nome']} ({_cat_diz(it['cat'])}): " + ' → '.join(f"{d['ano']} {d['quem'] or '—'} ({d['como']})" for d in it['donos']) + f" · hoje: {it['hoje']}")
