#!/usr/bin/env python3
"""provas_regiao.py — MOTOR 10: O BANCO DA ETAPA FINAL, AS PEÇAS (o contrato: projeto/ETAPA_FINAL.md). O banco do ano é o provas_ano.py.

RG1 O GRAVADOR NOVO: o verbo mundo (as seções, a forma, a história só no gerador), os campos novos da pessoa (a memória que guarda 12, os laços, o herdeiro, o jogador
    só na herança), a estrada, o morto que não recebe; o save sem mundo.json abre e segue sem ele.
RG2 O ENSAIO QUE COPIA SÓ O QUE MUDA: os mesmos eventos ao acaso, com a cópia inteira e com a cópia econômica, dão o mesmo mundo; o que o evento não toca é o mesmo objeto.
RG3 O MUNDO GERADO (três sementes): inteiro; os 16 lugares de povo, as 24 estradas (o grafo é conexo), os 6 ermos, as 8 masmorras com origem; uns 150 nomeados e 40 rivais
    em 6 guildas; o raro contado (12 Épicas, 4 Únicas, 3 Lendárias, 1 Mítica); 13 frentes; mesma semente, mesmo mundo; nasce em menos de 5 segundos.
RG4 A HISTÓRIA (a meta 5b): a cadeia de donos de toda peça Única ou maior, sem buraco; a origem de toda masmorra; ninguém vivo mais velho que o povo deixa; toda casa viva com gente viva.
RG5 A VIAGEM: chega no tempo da estrada; o pedágio vai para o bando; a luta na estrada tira o morto da conta e reparte a bolsa; viagem e saída não andam juntas.
RG6 A NOTÍCIA: anda uma estrada por dia; do quarto salto é boato; a janela chega a todo lugar no mesmo dia; a velha some.
RG7 A CAIXA: o oitavo pedido força o mais velho; o prazo vencido vale o padrão, com custo; a resposta faz a opção; o turno não fecha com pedido vencendo sem pergunta.
RG8 A MISSÃO: a paga é da bolsa de quem pede; tomar só no quadro; a entrega sai da carga e paga; a missão contra a frente tira um passo; a vencida e a falhada.
RG9 A GENTE: a opinião e os porquês; o querer da semana muda número; o ferreiro sem metal escreve na caixa de quem está ali.
RG10 AS FRENTES: o passo faz o efeito e manda o sinal; o sexto é o desfecho (a janela); a missão no passo zero a barra; o dono morto, barrada; investigar abre um campo.
RG11 O DIRETOR NEUTRO: 60 dias de mundo com o diretor chamado todo dia e sem ele dão o mesmo mundo.
RG12 A CONTA RÁPIDA (a meta 8): erra menos de 8 pontos contra o luta.py em casos novos.
RG13 A CRIAÇÃO: cada povo nasce inteiro num berço do mundo (a soma dos atributos, os laços dos dois lados, a memória da família, a prata que sai da casa, a armadura miúda),
    a segunda inclinação só no humano, e o segundo personagem vivo é recusado.
RG14 O HERDEIRO: só um parente, aprendiz ou jurado; morto o personagem, o herdeiro assume (a cadeira do jogador, as peças do morto, a casa, a memória pela metade).
RG15 O TURNO DO MUNDO NOVO: a MESA da criação; a MESA do personagem com as estradas, o quadro e o ranking; o RETOMAR do primeiro turno sem o ruído do gerador; o save antigo sem nada disto.
Uso: python3 provas_regiao.py [N]      (o provas_mundo.py também roda este banco)
"""
import contextlib, copy, io, json, os, random, shutil, sys, tempfile, time
import tabelas as T
import tabelas_mundo as M
import tabelas_regiao as R
import tabelas_povos as TP
import estado

AQUI = os.path.dirname(os.path.abspath(__file__))
def sn(x): return 'sim' if x else 'NÃO'
def recusa(f):
    try:
        with contextlib.redirect_stdout(io.StringIO()): f()
    except SystemExit as e: return str(e) or 'recusado'
    return None
def quieto(f, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()): return f(*a, **k)
def retrato(E): return json.dumps({k: E[k] for k in estado.ARQS}, sort_keys=True, ensure_ascii=False)
_MUNDOS = {}
def mundo(s=1):
    import gera
    if s not in _MUNDOS: _MUNDOS[s] = gera.mundo(s)[0]
    return copy.deepcopy(_MUNDOS[s])


def com_personagem(E, povo='humano', berco=2, nome='Prova'):
    import cria
    quieto(cria.nasce, E, povo, berco, 'fio', nome)
    return E


def rg1():
    E = estado.novo(3); r = []
    estado.aplica(E, 'gera', [['lugar', 'nasce', 'a', dict(nome='Alfa', tipo='vila', cama=True)], ['lugar', 'nasce', 'b', dict(nome='Beta', tipo='aldeia')], ['lugar', 'nasce', 'm', dict(nome='o Mato', tipo='ermo')]])
    estado.aplica(E, 'gera', [['lugar', 'nasce', 'e', dict(nome='a estrada de Alfa a Beta', tipo='estrada', ponta=['a', 'b'], longe=2, perigo=1, bando=0)], ['mundo', 'casas', 'c1', 'poe', dict(nome='os Prova', tipo='comum', sede='a', viva=True)]])
    at = {k: 50 for k in T.ATRIBUTOS}
    estado.aplica(E, 'gera', [['pessoa', 'nasce', 'x', dict(nome='Xis', nivel=3, atributos=at, lugar='a', casa='c1')], ['pessoa', 'nasce', 'y', dict(nome='Ipsilon', nivel=3, atributos=at, lugar='a', moedas=10)]])
    recusas = [recusa(lambda: estado.aplica(E, 'mestre', [['mundo', 'nada', 'x', 'poe', {}]])), recusa(lambda: estado.aplica(E, 'querer', [['mundo', 'casas', 'c2', 'poe', dict(nome='os Outros')]])),
               recusa(lambda: estado.aplica(E, 'caixa', [['mundo', 'caixa', 'cx1', 'poe', dict(pede='algo', prazo=3, opcoes=dict(a='sim'), padrao='a')]])),
               recusa(lambda: estado.aplica(E, 'mestre', [['pessoa', 'x', 'lacos.zz', 'poe', 'irmão']])), recusa(lambda: estado.aplica(E, 'mestre', [['pessoa', 'x', 'jogador', 'poe', True]])),
               recusa(lambda: estado.aplica(E, 'mestre', [['pessoa', 'x', 'herdeiro', 'poe', 'y']])), recusa(lambda: estado.aplica(E, 'mestre', [['lugar', 'm', 'vizinhos', 'poe', ['e']]]) if estado.valida(E) == [] and False else (_ for _ in ()).throw(SystemExit('x'))),
               recusa(lambda: estado.aplica(E, 'querer', [['pessoa', 'x', 'papel', 'poe', 'ferreiro']]))]
    for i in range(15): estado.aplica(E, 'querer', [['pessoa', 'x', 'memoria', 'junta', dict(dia=1, de='y', o_que=f'fato {i}', peso=(i % 11) - 5)]])
    mem = E['gente']['x']['memoria']; doze = len(mem) == M.MEMORIA_MAX and min(abs(m['peso']) for m in mem) >= 1
    estado.aplica(E, 'mestre', [['pessoa', 'y', 'estado', 'poe', 'morto']], texto='prova')
    morto = recusa(lambda: estado.aplica(E, 'mestre', [['pessoa', 'y', 'moedas', 'soma', 5]])) is not None
    estado.aplica(E, 'mestre', [['estoque', 'a', 'prata', 'soma', 3]], texto='prova')
    ok_mundo = E['mundo']['casas']['c1']['nome'] == 'os Prova'
    d = tempfile.mkdtemp(); os.environ['MOTOR10_MUNDO'] = d; F = estado.novo(1); F['lugares']['v'] = dict(nome='V', tipo='vila', estoque={}); estado.grava(F); sem_arq = not os.path.exists(os.path.join(d, 'mundo.json'))
    G = estado.carrega(); abre = G['mundo'] == {}; shutil.rmtree(d); os.environ.pop('MOTOR10_MUNDO', None)
    passa = all(recusas) and doze and morto and ok_mundo and sem_arq and abre and estado.valida(E) == []
    return ('RG1 O GRAVADOR NOVO', f"{sum(1 for x in recusas if x)} de {len(recusas)} efeitos tortos recusados; a memória guarda {len(mem)} (sai o de menor peso: {sn(doze)}); o morto não recebe prata: {sn(morto)}; "
            f"o save sem mundo.json grava sem ele: {sn(sem_arq)}, e abre com o mundo vazio: {sn(abre)}; estado inteiro: {sn(estado.valida(E) == [])}", passa)


def rg2(n=400):
    E0 = mundo(1); r = random.Random(5); lids = [k for k, l in E0['lugares'].items() if l.get('tipo') in M.POVOADOS]; pids = [k for k, p in E0['gente'].items() if p['estado'] == 'vivo']
    iids = list(E0['itens']['itens'])
    evs = []
    for i in range(n):
        x = r.random()
        if x < 0.3: l = r.choice(lids); evs.append([['estoque', l, 'comida', 'soma', r.randint(1, 5)]])
        elif x < 0.55: p = r.choice(pids); evs.append([['pessoa', p, 'fama', 'soma', 1], ['pessoa', p, 'memoria', 'junta', dict(dia=1, de=r.choice(pids), o_que='x', peso=1)]])
        elif x < 0.7: evs.append([['item', r.choice(iids), 'historia', 'junta', 'prova']])
        elif x < 0.8: evs.append([['mundo', 'seq', 'prova', 'soma', 1], ['mundo', 'cronica', 'junta', dict(ano=1, texto='prova')]] if False else [['mundo', 'seq', 'prova', 'soma', 1]])
        elif x < 0.9: evs.append([['relogio', 1]])
        else: p = r.choice(pids); evs.append([['pessoa', p, 'lacos.' + r.choice([q for q in pids if q != p]), 'poe', 'amigo']])
    A = copy.deepcopy(E0); B = copy.deepcopy(E0); orig = estado._ensaio
    for ef in evs: estado.aplica(A, 'mestre', ef, texto='prova')
    estado._ensaio = lambda E, efeitos: {k: copy.deepcopy(E[k]) for k in estado.ARQS}
    try:
        for ef in evs: estado.aplica(B, 'mestre', ef, texto='prova')
    finally: estado._ensaio = orig
    igual = retrato(A) == retrato(B)
    antes = A['gente']; l0 = lids[0]; estado.aplica(A, 'mestre', [['estoque', l0, 'comida', 'soma', 1]], texto='prova')
    mesmo = all(A['gente'][k] is antes[k] for k in antes) and A['lugares'][lids[1]] is not None
    return ('RG2 O ENSAIO QUE COPIA SÓ O QUE MUDA', f"{n} eventos ao acaso, com a cópia econômica e com a inteira: o mesmo mundo: {sn(igual)}; o que o evento não toca segue o mesmo objeto: {sn(mesmo)}", igual and mesmo)


def rg3():
    import gera, regiao
    L = []; ok = True; t0 = time.time(); E1, _ = gera.mundo(1); dt = time.time() - t0; E1b, _ = gera.mundo(1); igual = retrato(E1) == retrato(E1b)
    for s in (1, 2, 3):
        E = mundo(s); Ls = E['lugares']; pov = [k for k, l in Ls.items() if l.get('tipo') in M.POVOADOS]
        tipos = {t: sum(1 for k in pov if Ls[k]['tipo'] == t) for t in R.LUGARES}; est = [k for k, l in Ls.items() if l.get('tipo') == 'estrada']
        conexo = len(regiao.saltos(E, pov[0], so_abertas=False)) == len(pov); ermos = [k for k, l in Ls.items() if l.get('tipo') == 'ermo' and l.get('habitat')]
        ms = [k for k, l in Ls.items() if l.get('tipo') == 'masmorra']; origem = all(Ls[k].get('origem') for k in ms)
        nom = [k for k, p in E['gente'].items() if not p.get('rival')]; riv = [k for k, p in E['gente'].items() if p.get('rival')]
        cats = {}; [cats.__setitem__(it['cat'], cats.get(it['cat'], 0) + 1) for it in E['itens']['itens'].values() if it['tipo'] != 'nucleo']
        fr = E['mundo'].get('frentes') or {}
        c = (estado.valida(E) == [] and tipos == {t: v[0] for t, v in R.LUGARES.items()} and len(est) == R.ESTRADAS and conexo and len(ermos) >= 6 and len(ms) == 8 and origem
             and 130 <= len(nom) <= 185 and len(riv) == 40 and len(E['mundo'].get('guildas') or {}) == 6 and cats.get(3) == 12 and cats.get(4) == 4 and cats.get(5) == 3 and cats.get(6) == 1
             and 45 <= cats.get(2, 0) <= 90 and len(fr) == 13)
        ok = ok and c
        L.append(f"semente {s}: {len(pov)} lugares, {len(est)} estradas (conexo: {sn(conexo)}), {len(ermos)} ermos, {len(ms)} masmorras (com origem: {sn(origem)}), {len(nom)} nomeados e {len(riv)} rivais, "
                 f"o raro {', '.join(f'{T.CATS[k]} {v}' for k, v in sorted(cats.items()) if k >= 2)}, {len(fr)} frentes; inteiro: {sn(estado.valida(E) == [])}")
    return ('RG3 O MUNDO GERADO', ' · '.join(L) + f" · mesma semente, mesmo mundo: {sn(igual)}; nasce em {dt:.1f} s", ok and igual and dt < 5)


def rg4():
    import re
    L = []; ok = True
    for s in (1, 2, 3):
        E = mundo(s); bur = 0; altas = 0
        for it in E['itens']['itens'].values():
            if it['cat'] < 4 or it['tipo'] == 'nucleo': continue
            altas += 1; anos = [int(m.group(1)) for h in it.get('historia') or [] if (m := re.match(r'Ano (\d+):', h))]
            if anos != sorted(anos) or len(anos) < 2: bur += 1; continue
            hs = it['historia']
            for i in range(len(hs) - 1):
                a0 = int(re.match(r'Ano (\d+):', hs[i]).group(1)); a1 = int(re.match(r'Ano (\d+):', hs[i + 1]).group(1))
                if a1 - a0 > 60 and not any(w in hs[i] for w in ('perdeu-se', 'ficou com o corpo', 'jaz', 'tesouro')): bur += 1; break
        velhos = [p['nome'] for p in E['gente'].values() if p['estado'] == 'vivo' and isinstance(p.get('idade'), int) and p['idade'] > TP.POVOS[estado.povo(p)]['vida'][2]]
        casas = E['mundo'].get('casas') or {}; sem = [c['nome'] for k, c in casas.items() if c.get('viva') and not any(p.get('casa') == k and p['estado'] == 'vivo' for p in E['gente'].values())]
        ms = [k for k, l in E['lugares'].items() if l.get('tipo') == 'masmorra' and not l.get('origem')]
        c = bur == 0 and not velhos and not sem and not ms and altas >= 8; ok = ok and c
        L.append(f"semente {s}: {altas} peças Únicas ou maiores, {bur} com buraco na cadeia; {len(velhos)} vivos velhos demais; {len(sem)} casas vivas sem gente; {len(ms)} masmorras sem origem")
    return ('RG4 A HISTÓRIA (a meta 5b)', ' · '.join(L), ok)


def rg5():
    d = tempfile.mkdtemp(); velho = os.environ.get('MOTOR10_MUNDO'); os.environ['MOTOR10_MUNDO'] = d       # a luta grava o mundo: numa pasta de rascunho, nunca na do jogo
    try: return _rg5()
    finally:
        shutil.rmtree(d)
        if velho is None: os.environ.pop('MOTOR10_MUNDO', None)
        else: os.environ['MOTOR10_MUNDO'] = velho


def _rg5():
    import viagem, regiao
    E = com_personagem(mundo(2)); eu = 'eu'; lid = E['gente'][eu]['lugar']; e, o = regiao.estradas(E, lid)[0]; longe = E['lugares'][e]['longe']
    estado.aplica(E, 'mestre', [['lugar', e, 'bando', 'poe', 0], ['lugar', e, 'passa', 'poe', None]], texto='prova'); t0 = estado.agora(E)
    quieto(viagem.ir, E, eu, o); chegou = E['gente'][eu]['lugar'] == o and estado.agora(E) - t0 == longe and not estado.fora(E, eu) and e in E['gente'][eu]['marca'].get('andou', [])
    base = dict(R.VIAGEM['base']); R.VIAGEM['base'] = {1: 1.0, 2: 1.0, 3: 1.0}; bicho = R.VIAGEM['bicho']; R.VIAGEM['bicho'] = 0.0
    try:
        estado.aplica(E, 'mestre', [['lugar', e, 'bando', 'poe', 3], ['estoque', e, 'prata', 'soma', 30], ['pessoa', eu, 'moedas', 'soma', 40]], texto='prova')
        quieto(viagem.ir, E, eu, lid); v = E['gente'][eu]['marca']['viagem']; enc = v.get('fase') == 'encontro'
        prata0 = E['lugares'][e]['estoque'].get('prata', 0); m0 = E['gente'][eu]['moedas']; taxa = v['encontro']['taxa']
        R.VIAGEM['base'] = {1: 0.0, 2: 0.0, 3: 0.0}
        quieto(viagem.pagar, E, eu)
        for _ in range(6):                                  # o corpo pode parar a viagem no meio (o sono, a fome): segue até chegar
            if not estado.fora(E, eu): break
            quieto(viagem.segue, E, eu)
        pagou = E['lugares'][e]['estoque']['prata'] == prata0 + taxa and E['gente'][eu]['moedas'] == m0 - taxa and E['gente'][eu]['lugar'] == lid and not estado.fora(E, eu)
        junto = recusa(lambda: estado.aplica(E, 'mestre', [['pessoa', eu, 'marca.viagem', 'poe', dict(estrada=e, sai=lid, para=o, feitos=0, longe=longe, com=[], fase='anda')], ['pessoa', eu, 'marca.caca', 'poe', dict(ermo=lid, fase='procura', restam=1, casa=lid, com=[])]]))
        R.VIAGEM['base'] = {1: 1.0, 2: 1.0, 3: 1.0}; quieto(viagem.ir, E, eu, o); b0 = E['lugares'][e]['bando']
        quieto(viagem.atacar, E, eu)
        for _ in range(15):
            if (E['gente'][eu]['marca'].get('viagem') or {}).get('fase') != 'luta': break
            quieto(viagem.luta, E, eu, ['Prova: atacar'])
        tirou = E['lugares'][e]['bando'] <= b0 and estado.valida(E) == []
    finally: R.VIAGEM['base'] = base; R.VIAGEM['bicho'] = bicho
    return ('RG5 A VIAGEM', f"a estrada de {longe} blocos: chegou no tempo dela, com a estrada marcada: {sn(chegou)}; o encontro: {sn(enc)}; o pedágio ({taxa}) foi para o bando e a viagem seguiu: {sn(pagou)}; "
            f"viagem e saída juntas: recusado: {sn(junto)}; a luta na estrada tirou o morto da conta, e o estado ficou inteiro: {sn(tirou)}", chegou and enc and pagou and bool(junto) and tirou)


def rg6():
    import noticias, regiao
    E = mundo(1); pov = regiao.povoados(E); o = pov[0]; d = regiao.saltos(E, o); dia0 = E['relogio']['dia']
    noticias.da(E, o, 'uma notícia de prova', 1); nid = max(E['mundo']['noticias']); noticias.da(E, o, 'a janela de prova', 3, janela=True); jid = max(E['mundo']['noticias'])
    toda = len(E['mundo']['noticias'][jid]['chegou']) == len(pov)
    certos = True; boato = False
    for k in range(1, 6):
        regiao.anda(E, 1); ch = E['mundo']['noticias'][nid]['chegou']
        certos = certos and all(ch.get(x, [0, 99])[1] == d[x] for x, s in d.items() if s <= k) and all(x not in ch for x, s in d.items() if s > k)
        boato = boato or any(s >= R.BOATO_SALTO and noticias.diz(E, E['mundo']['noticias'][nid], s).startswith('dizem que') for _, s in ch.values())
    longe4 = any(s >= R.BOATO_SALTO for s in d.values())
    regiao.anda(E, R.NOTICIA_DURA - 3); sumiu = nid not in (E['mundo'].get('noticias') or {})
    return ('RG6 A NOTÍCIA', f"anda uma estrada por dia, de lugar em lugar: {sn(certos)}; do quarto salto é boato: {sn(boato or not longe4)}; a janela chegou aos {len(pov)} lugares no mesmo dia: {sn(toda)}; a velha some: {sn(sumiu)}",
            certos and (boato or not longe4) and toda and sumiu)


def rg7():
    import caixa, gente, turno
    E = com_personagem(mundo(1)); eu = 'eu'; q = next(k for k, p in E['gente'].items() if p['lugar'] == E['gente'][eu]['lugar'] and k != eu and p['estado'] == 'vivo'); hoje = E['relogio']['dia']
    ids = [caixa.nova(E, q, f'coisa {i}', hoje + 2 + i, dict(a='sim', b='não'), dict(a=gente.lembra(E, q, eu, 'ajudou', 2), b=gente.lembra(E, q, eu, 'calou', -2)), 'b') for i in range(8)]
    ab = caixa.abertos(E); forcou = len(ab) == M.CAIXA_MAX and E['mundo']['caixa'][ids[0]]['fim'] == 'b'
    caixa.responde(E, ids[1], 'a'); resp = E['mundo']['caixa'][ids[1]]['fim'] == 'a' and gente.opiniao(E, q, eu)[0] == 0
    xa = caixa.nova(E, q, 'coisa de amanhã', hoje + 1, dict(a='sim', b='não'), dict(a=[], b=gente.lembra(E, q, eu, 'calou', -2)), 'b')
    rec = caixa.recusa_fecha(E); recusa_ok = any(xa in x for x in rec)
    caixa.pergunta(E, xa); ligada = not any(xa in x for x in caixa.recusa_fecha(E))
    import regiao
    E['gente'][eu]['jogador'] = True
    venceu_antes = sum(1 for x in E['mundo']['caixa'].values() if x['fim'] == 'b')
    for _ in range(4): caixa.virada(dict(E, relogio=dict(E['relogio'], dia=E['relogio']['dia'] + 20))) if False else None
    E['relogio']['dia'] += 20; caixa.virada(E); vencidos = sum(1 for x in E['mundo']['caixa'].values() if x['fim'] == 'b')
    custo = gente.opiniao(E, q, eu)[0] < 0
    return ('RG7 A CAIXA', f"o oitavo pedido forçou o mais velho (vale o padrão): {sn(forcou)}; a resposta fez a opção (e a memória): {sn(resp)}; o turno recusa fechar com o pedido vencendo sem pergunta: {sn(recusa_ok)}, "
            f"e fecha com a pergunta ligada: {sn(ligada)}; vencido o prazo, vale o padrão ({vencidos - venceu_antes} pedidos), com custo na opinião: {sn(custo)}", forcou and resp and recusa_ok and ligada and custo and vencidos > venceu_antes)


def rg8():
    import missoes, frentes, gente
    E = com_personagem(mundo(1)); eu = 'eu'; lid = E['gente'][eu]['lugar']; q = next(k for k, p in E['gente'].items() if p['lugar'] == lid and k != eu and p['estado'] == 'vivo' and p['moedas'] >= 20)
    bolsa = E['gente'][q]['moedas']; mid = missoes.posta(E, q, lid, 'entrega', 'couro:0', n=2, paga=999); m = E['mundo']['missoes'][mid]; teto = m['paga'] <= int(bolsa * 0.6)
    outro = next(k for k in E['lugares'] if E['lugares'][k].get('tipo') in M.POVOADOS and k != lid)
    fora = recusa(lambda: missoes.toma(E, eu, next(iter(missoes.abertas(E, outro)), 'm9999')))
    missoes.toma(E, eu, mid); estado.aplica(E, 'mestre', [['pessoa', eu, 'carga.couro:0', 'soma', 2]], texto='prova'); m0 = E['gente'][eu]['moedas']
    quieto(missoes.entrega, E, eu, mid); pagou = E['gente'][eu]['moedas'] == m0 + m['paga'] and not (E['gente'][eu].get('carga') or {}).get('couro:0') and gente.opiniao(E, q, eu)[0] >= 3
    fid = next(iter(frentes.ativas(E))); f = E['mundo']['frentes'][fid]; estado.aplica(E, 'mestre', [['mundo', 'frentes', fid, 'passo', 'poe', 3]], texto='prova')
    m2 = missoes.posta(E, q, lid, 'entrega', 'lenha', n=1, paga=5, frente=fid); missoes.toma(E, eu, m2); estado.aplica(E, 'mestre', [['pessoa', eu, 'carga.lenha', 'soma', 1]], texto='prova')
    quieto(missoes.entrega, E, eu, m2); recuou = E['mundo']['frentes'][fid]['passo'] == 2
    m3 = missoes.posta(E, q, lid, 'entrega', 'sal', n=1, paga=5); missoes.toma(E, eu, m3); fama0 = E['gente'][eu].get('fama', 0)
    E['relogio']['dia'] = E['mundo']['missoes'][m3]['prazo'] + 1; missoes.virada(E); falhou = E['mundo']['missoes'][m3]['estado'] == 'falhou' and E['gente'][eu].get('fama', 0) < fama0
    return ('RG8 A MISSÃO', f"a paga cabe na bolsa de quem pede (até 60%): {sn(teto)}; tomar fora do quadro: recusado: {sn(fora)}; a entrega saiu da carga, pagou e fez memória: {sn(pagou)}; "
            f"a missão contra a frente tirou um passo: {sn(recuou)}; a tomada vencida falhou, com a fama: {sn(falhou)}", teto and bool(fora) and pagou and recuou and falhou)


def rg9():
    import gente, regiao, caixa
    E = com_personagem(mundo(1)); eu = 'eu'; q = next(k for k in E['gente'] if k != eu and not E['gente'][k].get('rival'))
    estado.aplica(E, 'mestre', gente.lembra(E, q, eu, 'me salvou', 4) + gente.lembra(E, q, eu, 'me deve', -1), texto='prova'); v, pq = gente.opiniao(E, q, eu)
    op = v == 3 and pq[0] == 'me salvou'
    n0 = E['relogio']['eventos']; E2 = copy.deepcopy(E); E2['gente'][eu]['estado'] = 'morto' if False else E2['gente'][eu]['estado']
    lid = E['gente'][eu]['lugar']; ferr = next((k for k, p in E['gente'].items() if p.get('papel') == 'ferreiro' and p['lugar'] == lid), None)
    if not ferr:
        ferr = next(k for k, p in E['gente'].items() if p.get('papel') == 'ferreiro'); estado.aplica(E, 'mestre', [['pessoa', eu, 'lugar', 'poe', E['gente'][ferr]['lugar']]], texto='prova'); lid = E['gente'][eu]['lugar']
    est = E['lugares'][lid]['estoque'].get('metal:0', 0); estado.aplica(E, 'mestre', [['estoque', lid, 'metal:0', 'soma', -est]], texto='prova') if est else None
    gente._q_pede_materia(E, ferr, E['gente'][ferr], random.Random(1)); pediu = any(x['de'] == ferr for _, x in caixa.abertos(E))
    E3 = mundo(1); E3['gente'] = {k: p for k, p in E3['gente'].items()}; dia = E3['relogio']['dia']
    estado.aplica(E3, 'tempo', [['relogio', M.BLOCOS_DIA * 7 - E3['relogio']['bloco']]], texto='uma semana'); m0 = E3['relogio']['eventos']; gente.virada(E3)
    qs = [e for e in E3['_novos'] if e['id'] > m0 and e['tipo'] == 'querer']; numero = qs and all(e['efeitos'] for e in qs)
    return ('RG9 A GENTE', f"a opinião ({v:+d}) e o porquê de maior peso: {sn(op)}; no primeiro dia da semana, {len(qs)} quereres, cada um com efeito: {sn(numero)}; o ferreiro sem metal escreveu na caixa do personagem que estava ali: {sn(pediu)}",
            op and bool(numero) and pediu)


def rg10():
    import frentes, regiao
    E = mundo(1); fid = next(k for k, f in frentes.ativas(E).items() if f['molde'] == 'seca'); f = E['mundo']['frentes'][fid]
    p0 = (E['lugares'][f['onde']].get('produz') or {}).get('comida'); frentes.passo(E, fid); efeito = (E['lugares'][f['onde']]['produz'] or {}).get('comida') < p0
    sinal = any('frente' in (n.get('tags') or []) and fid in (n.get('tags') or []) for n in E['mundo']['noticias'].values())
    for _ in range(5): frentes.passo(E, fid)
    fim = E['mundo']['frentes'][fid]['fim'] == 'desfecho' and any(f['nome'][:10].lower() in j['texto'].lower() for j in E['mundo'].get('janela', []))
    g = next(k for k, f in frentes.ativas(E).items() if f['molde'] == 'cartel'); frentes.passo(E, g); frentes.recua(E, g, 'prova'); no_zero = E['mundo']['frentes'][g]['passo'] == 0 and not E['mundo']['frentes'][g].get('fim')
    frentes.recua(E, g, 'prova'); barrada = no_zero and E['mundo']['frentes'][g]['fim'] == 'barrada'
    b = next(k for k, f in frentes.ativas(E).items() if f['molde'] == 'bando'); estado.aplica(E, 'mestre', [['pessoa', E['mundo']['frentes'][b]['dono'], 'estado', 'poe', 'morto']], texto='prova')
    frentes.virada(E); dono = E['mundo']['frentes'][b]['fim'] == 'barrada'
    import cria
    E2 = com_personagem(mundo(1)); h = next(k for k, f in frentes.ativas(E2).items() if f['molde'] == 'luzes'); frentes.passo(E2, h)
    lid = E2['mundo']['frentes'][h]['onde']; estado.aplica(E2, 'mestre', [['pessoa', 'eu', 'lugar', 'poe', lid], ['pessoa', 'eu', 'atributos.Percepção', 'poe', 99]] if False else [['pessoa', 'eu', 'lugar', 'poe', lid]], texto='prova')
    for _ in range(6):
        try: quieto(frentes.investigar, E2, 'eu', h)
        except SystemExit: break
    abriu = len(frentes.sabe(E2, 'eu', h)) >= 1
    return ('RG10 AS FRENTES', f"o passo faz o efeito (a seca tira da colheita): {sn(efeito)}, e manda o sinal pela notícia: {sn(sinal)}; o sexto é o desfecho, com a janela: {sn(fim)}; "
            f"a missão tira um passo, e no zero a barra: {sn(barrada)}; o dono morto, barrada: {sn(dono)}; investigar abriu campo: {sn(abriu)} ({', '.join(frentes.sabe(E2, 'eu', h))})", efeito and sinal and fim and barrada and dono and abriu)


def rg11(dias=60):
    import regiao, diretor
    A = com_personagem(mundo(2)); B = copy.deepcopy(A)
    estado.aplica(A, 'mestre', [['pessoa', 'eu', 'estado', 'poe', 'morto']], texto='prova'); estado.aplica(B, 'mestre', [['pessoa', 'eu', 'estado', 'poe', 'morto']], texto='prova')
    A['gente']['eu']['estado'] = 'vivo'; A['gente']['eu']['pv'] = 1; B['gente']['eu']['estado'] = 'vivo'; B['gente']['eu']['pv'] = 1      # o personagem de prova, de pé, só para o diretor ter de quem falar; o mundo anda sozinho
    def anda(E, chama):
        for _ in range(dias):
            falta = M.BLOCOS_DIA - E['relogio']['bloco']; estado.aplica(E, 'tempo', [['relogio', falta]], texto='o dia vira')
            import ato; ato._mundo_vira(E)
            if chama: diretor.so_mestre(E); diretor.pauta(E)
    anda(A, True); anda(B, False)
    igual = retrato(A) == retrato(B)
    return ('RG11 O DIRETOR NEUTRO', f"{dias} dias de mundo, com o diretor chamado todo dia e sem ele: o mesmo mundo: {sn(igual)}", igual)


def rg12(n=120):
    import conta
    e, p90 = conta.confere(n, k=80)
    return ('RG12 A CONTA RÁPIDA (a meta 8)', f"erro médio contra o luta.py em {n} casos novos (80 lutas cada): {e * 100:.1f} pontos (90% até {p90 * 100:.1f}); a meta: menos de 8", e < 0.08)


def rg13():
    import cria, mercado
    ok = True; L = []
    for i, povo in enumerate(TP.POVOS):
        E = mundo(3); p0 = mercado.prata_do_mundo(E); berco = i % 6; b = cria.bercos(E)[berco]
        quieto(cria.nasce, E, povo, berco, 'fio', 'Prova', 'forja' if povo == 'humano' else None)
        p = E['gente']['eu']; soma = sum(p['atributos'].values()); at0 = sum(R.BERCOS[b['molde']][3].values())
        lacos = all(E['gente'][k].get('lacos', {}).get('eu') for k in p.get('lacos', {})); mem = any(m.get('de') == 'eu' for m in E['gente'][b['chefe']].get('memoria') or [])
        miudo = TP.POVOS[povo]['corpo'] != 'miúdo' or all(it.get('talhe') == 'miúdo' for it in E['itens']['itens'].values() if it.get('dono') == 'eu' and it['tipo'] == 'armadura')
        c = estado.valida(E) == [] and soma == at0 and lacos and mem and miudo and mercado.prata_do_mundo(E) == p0
        ok = ok and c; L.append(f"{povo}/{b['molde']}: {sn(c)}")
    E = mundo(3); dois = recusa(lambda: cria.nasce(E, 'anão', 0, 'fio', 'X', 'forja'))
    quieto(cria.nasce, E, 'humano', 0, 'fio', 'Prova'); vivo2 = recusa(lambda: cria.nasce(E, 'humano', 1, 'fio', 'Outro'))
    return ('RG13 A CRIAÇÃO', ' · '.join(L) + f" · a segunda inclinação no anão: recusada: {sn(dois)}; um segundo personagem com o primeiro vivo: recusado: {sn(vivo2)}", ok and bool(dois) and bool(vivo2))


def rg14():
    import cria, gente
    E = com_personagem(mundo(1)); eu = 'eu'; pai = next(k for k, t in E['gente'][eu]['lacos'].items())
    estranho = next(k for k, p in E['gente'].items() if k not in E['gente'][eu]['lacos'] and k != eu and p['estado'] == 'vivo')
    nao = recusa(lambda: cria.herdeiro(E, estranho)); quieto(cria.herdeiro, E, pai)
    q = next(k for k in E['gente'] if k not in (eu, pai) and not E['gente'][k].get('rival') and E['gente'][k]['estado'] == 'vivo')
    estado.aplica(E, 'mestre', gente.lembra(E, q, eu, 'me salvou a vida', 5), texto='prova'); n_pecas = sum(1 for it in E['itens']['itens'].values() if it.get('dono') == eu)
    estado.aplica(E, 'mestre', [['pessoa', eu, 'estado', 'poe', 'morto']], texto='a prova da morte')
    quieto(cria.herda, E); assumiu = E['gente'][pai].get('jogador') and not E['gente'][eu].get('jogador') and estado.eu(E) == pai
    pecas = sum(1 for it in E['itens']['itens'].values() if it.get('dono') == pai and any('Prova' in h or True for h in it.get('historia') or [])) >= n_pecas
    mem = gente.opiniao(E, q, pai)[0] >= 2
    return ('RG14 O HERDEIRO', f"o estranho como herdeiro: recusado: {sn(nao)}; morto o personagem, o herdeiro assume a cadeira do jogador: {sn(assumiu)}, com as peças do morto: {sn(pecas)}, e a memória pela metade: {sn(mem)}; "
            f"estado inteiro: {sn(estado.valida(E) == [])}", bool(nao) and assumiu and pecas and mem and estado.valida(E) == [])


def rg15():
    import gera, cria, turno, ato
    d = tempfile.mkdtemp(); os.environ['MOTOR10_MUNDO'] = os.path.join(d, 'm')
    try:
        quieto(gera.main, [os.path.join(d, 'm'), 'semente=4']); E = estado.carrega(); quieto(cria.perguntas, E); txt = turno.mesa(E)
        criacao = 'OS BERÇOS' in txt and 'Que povo?' in txt and 'cria.py nasce' in txt
        quieto(turno.responde, E, '1a.2a.3e'); quieto(cria.nasce, E, 'humano', 0, 'forja', 'Prova'); quieto(turno.pergunta, E, 'a?', ['a=x', 'b=y']); quieto(turno.pergunta, E, 'b?', ['a=x', 'b=y'])
        txt2 = turno.mesa(E); mesa_ok = 'Estradas daqui' in txt2 and 'ranking' in txt2
        quieto(ato.passa, E, 'eu', 1, 'esperar'); quieto(turno.fecha, E, 'prova'); ret = open(os.path.join(estado.pasta(), 'RETOMAR.md'), encoding='utf-8').read()
        limpo = 'no quadro de' not in ret and 'nasce a frente' not in ret
    finally: shutil.rmtree(d); os.environ.pop('MOTOR10_MUNDO', None)
    src = os.path.join(AQUI, 'ensaio'); antigo = True
    if os.path.exists(os.path.join(src, 'relogio.json')):
        d2 = tempfile.mkdtemp(); shutil.copytree(src, os.path.join(d2, 'e')); os.environ['MOTOR10_MUNDO'] = os.path.join(d2, 'e')
        try:
            G = estado.carrega(); t = turno.mesa(G); antigo = 'Estradas daqui' not in t and G['mundo'] == {} and estado.valida(G) == []
            estado.grava(G); antigo = antigo and not os.path.exists(os.path.join(d2, 'e', 'mundo.json'))
        finally: shutil.rmtree(d2); os.environ.pop('MOTOR10_MUNDO', None)
    return ('RG15 O TURNO DO MUNDO NOVO', f"a MESA da criação (os berços, as perguntas, como nascer): {sn(criacao)}; a MESA do personagem (as estradas, o ranking): {sn(mesa_ok)}; o RETOMAR do primeiro turno sem o ruído do gerador: {sn(limpo)}; "
            f"o save antigo (ensaio/, numa cópia) abre sem nada disto e grava sem o mundo.json: {sn(antigo)}", criacao and mesa_ok and limpo and antigo)


def provas(n=300):
    out = []
    for f in (rg1, rg2, rg3, rg4, rg5, rg6, rg7, rg8, rg9, rg10, rg11, rg12, rg13, rg14, rg15):
        try: out.append(f())
        except SystemExit as e: out.append((f.__name__.upper(), f'QUEBROU: {e}', False))
        except Exception as e:
            import traceback; out.append((f.__name__.upper(), f'QUEBROU: {type(e).__name__}: {e} · {traceback.format_exc().splitlines()[-3].strip()}', False))
    return out


if __name__ == '__main__':
    res = provas(int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 300)
    for nm, deu, passa in res: print(f"  {'passa' if passa else 'FALHA'}  {nm}: {deu}")
    print(f"\n{sum(p for _, _, p in res)} de {len(res)} provas passam.")
    sys.exit(0 if all(p for _, _, p in res) else 1)
