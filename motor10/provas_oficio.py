#!/usr/bin/env python3
"""provas_oficio.py — MOTOR 10: O BANCO DE PROVAS DO OFÍCIO (etapa 2: forjar, consertar, ajustar).

As metas são as do contrato (projeto/ETAPA2.md, seção 5). As provas rodam em mundos de rascunho (a vila de prova do provas_mundo, com uma oficina);
nunca num save. O dado é o de verdade (teste.rola): por isso as medidas de chance trazem também a conta exata, e a escada é medida em muitas vidas.

O ROBÔ FERREIRO vive de verdade: dorme na cama e paga, come e paga, trabalha na bancada enquanto o corpo deixa (3,5 blocos por dia), vive do jornal
da oficina, e tem a matéria e o núcleo de cada obra na mão. Ele segue o caminho comum: um degrau de cada vez, e só abre a obra de um degrau quando
tem a mão que a obra pede (tabelas_oficio.MAO_DA_OBRA). Repete o degrau até a peça nascer, com matéria e núcleo novos a cada obra.
A MEDIDA DA ESCADA é o dia em que metade das vidas já tinha a peça (quem nunca a teve conta como nunca). A linha diz também quando a primeira obra fecha.
A LENDÁRIA É DIFERENTE, por decisão do jogador: julga-se o dia em que a primeira OBRA fecha (a primeira tentativa); a peça nascer é raro de propósito;
e uma linha à parte ("o ritmo da bancada") confere a outra leitura da meta: o dia em que a primeira obra de cada categoria fecha, acerte ou não.

Uso: python3 provas_oficio.py [N]      N = o tamanho das amostras (padrão 300): N ÷ 10 vidas inteiras do robô e N ÷ 15 curtas (no mínimo 20 de cada), 2 × N obras por medida de chance
     (o `python3 provas_mundo.py` também roda este banco)
"""
import contextlib, copy, io, json, math, os, shutil, sys, tempfile
import tabelas as T
import tabelas_mundo as M
import tabelas_oficio as O
import estado, ato, oficio, teste
import provas_mundo as PM
from itens import item
from pessoas import ficha

JANELAS = {2: (15, 30), 3: (45, 80), 4: (130, 200), 5: (300, 450)}      # o contrato: o dia em que a primeira peça de cada categoria sai
PELA_OBRA = (5,)            # DECISÃO DO JOGADOR (MUDANCAS.md, etapa 2, terceira volta): a Lendária é difícil de propósito. A chance não sobe; a meta dela é o dia em que a
                            # primeira OBRA Lendária FECHA (a primeira tentativa), acerte ou não. Nas outras categorias a meta segue sendo o dia em que a peça NASCE.
ROBO = dict(nivel=4, afinidade=60, alcance=5, dias=450, curta=240)       # o robô: a melhor oficina, o preparo todo, Afinidade de bom aprendiz, mão de Leigo
                                                                         # (a vida curta para na primeira Única, ou no dia `curta`: só engrossa a amostra das três primeiras metas)
MELHOR = dict(nivel=4, afinidade=100, alcance=5, mao=8)                  # o melhor ferreiro possível: Lendário, oficina 4, preparo 8 (e Afinidade 100)
VILA = dict(nivel=1, afinidade=50, mao=2, fogo=1, bigorna=1, receita=0, ajudante=0)     # um Iniciante em oficina de vila: o fogo e a bigorna da vila servem até o Incomum; a receita e o ajudante dele, ao Comum


# ---------- montar um mundo de rascunho ----------
def oficina_de_prova(semente=1, nivel=1, afinidade=50, mao=0, prata=30, fogo=None, bigorna=None, receita=None, ajudante=None, carga=None):
    """a vila de prova, com uma oficina. Atributo e grau de ofício não têm verbo no gravador: quem os dá é a mão do gerador, aqui."""
    E = PM.vila(semente, prata); eu = E['gente']['eu']; eu['atributos']['Afinidade'] = afinidade; eu['grau_oficio'] = 'aprendiz'
    ef = [['lugar', 'vila', 'oficina', 'poe', nivel]] if nivel is not None else []
    ef += [['lugar', 'vila', 'preparo.' + k, 'poe', v] for k, v in (('fogo', fogo), ('bigorna', bigorna)) if v is not None]
    ef += [['pessoa', 'eu', 'marca.prep_' + k, 'poe', v] for k, v in (('receita', receita), ('ajudante', ajudante)) if v is not None]
    if mao: ef.append(['pessoa', 'eu', 'maestria.forja', 'poe', mao])
    ef += [['pessoa', 'eu', 'carga.' + k, 'soma', n] for k, n in (carga or {}).items()]
    if ef: estado.aplica(E, 'gera', ef, onde='vila', texto='a oficina de prova')
    return E


def entrega(E, peca):
    """a matéria e o núcleo de uma obra, na mão de quem forja (por evento "gera"). Devolve o id do núcleo, ou None."""
    ef = [['pessoa', 'eu', 'carga.' + k, 'soma', n] for k, n in oficio.materia_de(peca).items()]
    nuc = O.pede_nucleo(peca['cat'])
    if nuc: ef.append(['item', 'nasce', dict(tipo='nucleo', cat=peca['cat'], nome=f"Núcleo {T.CATS[peca['cat']]} de prova", dur=[1, 1], dono='eu', onde=None, de='bicho de prova', historia=[])])
    estado.aplica(E, 'gera', ef, onde='vila', texto='a matéria de prova')
    return f"i{E['itens']['seq']:04d}" if nuc else None


def espada(cat, nome=None): return oficio.molde('arma', cat, nome or f'Espada {T.CATS[cat]} de prova', familia='espada')


def obra_pronta(E, cat):
    """abre uma obra de espada desta categoria, com a matéria entregue, e põe os blocos no fim (sem viver os dias): falta só o teste"""
    peca = espada(cat); nid = entrega(E, peca); R = oficio.forjar(E, 'eu', peca, blocos=0, nucleo=nid)
    estado.aplica(E, 'mestre', [['obra', R['obra'], 'blocos', 'poe', O.blocos(cat)]], texto='os blocos da prova')
    return R['obra'], nid


def mede(n, cat, **cenario):
    """n obras desta categoria, cada uma num mundo novo, com o dado de verdade: (fração que acerta, a conta exata)"""
    acertos = 0; exata = None
    for i in range(n):
        al = cenario.get('alcance'); E = oficina_de_prova(i + 1, nivel=cenario['nivel'], afinidade=cenario['afinidade'], mao=cenario.get('mao', 0), fogo=cenario.get('fogo', al), bigorna=cenario.get('bigorna', al),
                                                          receita=cenario.get('receita', al), ajudante=cenario.get('ajudante', al))
        oid, _ = obra_pronta(E, cat)
        if exata is None: exata = oficio.conta(E, 'eu', cat)
        acertos += oficio.remata(E, oid)['fim'] == 'acertou'
    return acertos / n, exata


def bate(medido, exata, n):
    """a medida com o dado de verdade concorda com a conta exata? (4 desvios e meio ponto de folga)"""
    return abs(medido - exata) <= 4 * math.sqrt(max(exata * (1 - exata), 0.01) / n) + 0.005


def recusa(f):
    try:
        with contextlib.redirect_stdout(io.StringIO()): f()
    except SystemExit as e: return str(e) or 'recusado'
    return None


def retrato(E): return json.dumps({k: E[k] for k in estado.ARQS}, sort_keys=True, ensure_ascii=False)


@contextlib.contextmanager
def dado_posto(margens):
    """SÓ PARA A PROVA DAS MARGENS: o dado de verdade é rolado e anotado, mas o total é posto à mão (o número contra, mais a margem), para conferir cada saída"""
    real = teste.rola; fila = list(margens)
    def posto(E, o_que, atributo, contra, mais=0, quem=None, oculto=False):
        r = real(E, o_que, atributo, contra, mais=mais, quem=quem, oculto=oculto); m = fila.pop(0); r['total'] = contra + m; r['passou'] = m >= 0; r['posto_a_mao'] = True
        return r
    teste.rola = posto
    try: yield
    finally: teste.rola = real


def repousa(E):
    """dorme três blocos na cama e come, para a prova seguir com o corpo inteiro"""
    ato.dormir(E, 'eu', 3, para=False)
    while E['gente']['eu']['corpo']['fome'] >= 2: ato.comer(E, 'eu')


# ---------- o robô ferreiro ----------
def vida(semente, dias=None, ate=O.FORJA_ATE):
    """uma vida do robô ferreiro, do Dia 1 até `dias` (ou até nascer a peça da categoria `ate`). Devolve o que houve: o dia em que cada categoria nasceu, o dia em que a primeira obra de cada uma fechou, e as contas."""
    dias = dias or ROBO['dias']; al = ROBO['alcance']
    E = oficina_de_prova(semente, nivel=ROBO['nivel'], afinidade=ROBO['afinidade'], fogo=al, bigorna=al, receita=al, ajudante=al)
    prata0 = oficio.prata_do_mundo(E); V = dict(nasce={}, fecha={}, tentou={}, de_primeira={}, bancada=0, parou=0, pena=0, camas=0, refeicoes=0, chao=0, jejum=0)
    def bancada():
        p = E['gente']['eu']; aberta = oficio.obras_de(E, 'eu'); alvo = next((c for c in range(O.FORJA_ATE + 1) if c not in V['nasce']), None)
        if p['moedas'] < 6: R = oficio.jornal(E, 'eu', 1)                                    # o bolso acabou: a obra espera, o jornal paga a cama
        elif aberta: R = oficio.continua(E, 'eu', blocos=1)
        elif alvo is not None and oficio.mao(p) >= O.MAO_DA_OBRA[alvo] and p['moedas'] >= O.blocos(alvo) + 6:      # tem a mão que a obra pede, e prata para viver até o fim dela
            peca = espada(alvo, f'Espada {T.CATS[alvo]} do robô'); nid = entrega(E, peca); V['tentou'][alvo] = V['tentou'].get(alvo, 0) + 1
            R = oficio.forjar(E, 'eu', peca, blocos=1, nucleo=nid)
        else: R = oficio.jornal(E, 'eu', 1)
        V['bancada'] += R['feitos']; V['parou'] += bool(R['parou'])
        if R.get('fim'):
            r = R['rolagem']; alvo = next(c for c in range(O.FORJA_ATE + 1) if O.contra(c) == r['contra']); V['pena'] += r['pena'] != 0
            primeira = alvo not in V['fecha']; V['fecha'].setdefault(alvo, r['dia'])
            if primeira: V['de_primeira'][alvo] = R['fim'] == 'acertou'
            if R['item']: V['nasce'].setdefault(E['itens']['itens'][R['item']]['cat'], r['dia'])
    while E['relogio']['dia'] <= dias and E['gente']['eu']['estado'] == 'vivo' and ate not in V['nasce']:
        b = E['relogio']['bloco']; p = E['gente']['eu']; c = p['corpo']
        if c['fome'] >= 3 or (b in (0, 1, 5) and c['fome'] >= 2):                           # come uma vez por dia, mais ou menos
            if p['moedas'] >= M.REFEICAO_PRECO and E['lugares']['vila']['estoque'].get('comida', 0) > 0: ato.comer(E, 'eu'); V['refeicoes'] += 1; p = E['gente']['eu']; c = p['corpo']
            else: V['jejum'] += 1
        aguenta = c['cansaco'] + M.ESFORCO['pesado'] < M.LIMIARES['cansaco'][0] and c['sono'] + M.SONO_ACORDADO < M.LIMIARES['sono'][0]
        if b in (0, 1) or (b == 5 and not aguenta):                                         # dorme a madrugada e a alvorada; deita na noite quando o corpo não dá mais um bloco
            chao = not ato.cama_paga(E, 'eu') and p['moedas'] < M.CAMA_PRECO; V['chao'] += chao; tinha = p['moedas']       # a cama é por noite: paga uma vez, vale o dia inteiro
            ato.dormir(E, 'eu', (2 - b) if b < 2 else 3, chao=chao, para=False); V['camas'] += (tinha - E['gente']['eu']['moedas']) // M.CAMA_PRECO
        elif aguenta: bancada()
        else: ato.descansar(E, 'eu', 1)
        E['_novos'].clear()                                                                  # a vida de rascunho não vai para arquivo: não guarda o registro na memória
    V['dia'] = E['relogio']['dia']; V['cheia'] = ate == O.FORJA_ATE; V['prata'] = oficio.prata_do_mundo(E) == prata0; V['quebrado'] = estado.valida(E); V['mao'] = oficio.mao(E['gente']['eu']); V['vivo'] = E['gente']['eu']['estado'] == 'vivo'
    solta = sum(oficio.materia_do_mundo(E).values()) - sum(sum(o.get('materia', {}).values()) for o in E['itens'].get('obras', {}).values())
    V['materia'] = solta == 0                                                                # o que foi entregue entrou em obra: nada sobra solto, nada nasce do nada
    V['nucleos'] = sum(1 for it in E['itens']['itens'].values() if it['tipo'] == 'nucleo') == sum(1 for o in E['itens'].get('obras', {}).values() if o.get('nucleo'))
    return V


def _meio(dias_ou_nada):
    """o dia em que metade das vidas já tinha a peça (quem nunca teve conta como nunca): a mediana de verdade, ou None se a metade não teve"""
    v = sorted(d if d is not None else math.inf for d in dias_ou_nada); m = v[(len(v) + 1) // 2 - 1]
    return None if m == math.inf else m


def escada(vidas):
    """as quatro metas da escada, uma linha por categoria, mais a linha das contas da vida do robô"""
    out = []; todas = vidas; fechos = {}
    for cat, (a, b) in JANELAS.items():
        vidas = [V for V in todas if V['cheia'] or cat < O.FORJA_ATE]; n = len(vidas); ate = ROBO['dias'] if cat == O.FORJA_ATE else ROBO['curta']
        nasce = [V['nasce'].get(cat) for V in vidas]; tem = [d for d in nasce if d is not None]; fecha = [V['fecha'].get(cat) for V in vidas]; m = _meio(nasce); f = _meio(fecha)
        prim = [V['de_primeira'][cat] for V in vidas if cat in V['de_primeira']]; tent = sum(V['tentou'].get(cat, 0) for V in vidas)
        deu = (f"nasce no Dia {m} (o dia em que metade das {n} vidas já a tinha)" if m is not None else f"NÃO NASCE na metade das {n} vidas até o Dia {ate}")
        deu += f"; nasceu em {len(tem)} de {n}" + (f", entre o Dia {min(tem)} e o {max(tem)}" if tem else '')
        deu += f"; a primeira obra {oficio.FEM[cat]} fecha no Dia {f}" if f is not None else f"; a primeira obra {oficio.FEM[cat]} não chega a fechar na metade das vidas"
        pior = max((V['tentou'].get(cat, 0) for V in vidas), default=0); o_que = 'núcleos' if O.pede_nucleo(cat) else 'levas de matéria'
        if prim: deu += f", e acerta de primeira em {sum(prim) / len(prim):.0%} das vidas ({tent / n:.1f} obras por vida)"
        deu += (f". COM QUE ISTO VALE: na {O.OFICINAS[ROBO['nivel']]} (+{ROBO['nivel']}), com os quatro preparos (+{O.PREPARO_MAX}) desde o Dia 1, e com matéria" + (' e núcleo novos' if O.pede_nucleo(cat) else ' nova') + f" a cada obra: {tent / n:.1f} {o_que} por vida (a pior vida: {pior})"
                + (f". COM UM NÚCLEO SÓ, a peça nasce em {sum(prim) / len(prim):.0%} das vidas; nas outras, o núcleo se gastou ou se perdeu" if prim and O.pede_nucleo(cat) else ''))
        fechos[cat] = f
        if cat in PELA_OBRA:    # a Lendária: julga-se a primeira TENTATIVA (o dia em que a primeira obra fecha); a peça nascer é raro de propósito, e a linha diz em quantas vidas nasceu
            out.append((f"A ESCADA, {oficio.FEM[cat].upper()}: a primeira OBRA {oficio.FEM[cat]} do robô ferreiro FECHA entre os dias {a} e {b} (a primeira tentativa; a peça nascer é difícil de propósito, e a linha diz em quantas vidas nasceu; na melhor oficina, com o preparo todo e com núcleo novo a cada obra)",
                        (f"a primeira obra {oficio.FEM[cat]} fecha no Dia {f}" if f is not None else f"a primeira obra {oficio.FEM[cat]} NÃO FECHA na metade das {n} vidas até o Dia {ate}") + '. A PEÇA: ' + deu, f is not None and a <= f <= b))
        else: out.append((f"A ESCADA, {oficio.FEM[cat].upper()}: a primeira peça {oficio.FEM[cat]} do robô ferreiro sai entre os dias {a} e {b} (na melhor oficina, com o preparo todo e com núcleo novo a cada obra: a linha diz o que isso gasta)", deu, m is not None and a <= m <= b))
    out.append(('O RITMO DA BANCADA (a outra leitura da meta da escada: o dia em que a primeira OBRA de cada categoria fecha, acerte ou não), nas mesmas janelas',
                ' · '.join(f"{oficio.FEM[c]}: Dia {fechos[c]} ({a} a {b})" if fechos[c] is not None else f"{oficio.FEM[c]}: não fecha na metade das vidas ({a} a {b})" for c, (a, b) in JANELAS.items()),
                all(fechos[c] is not None and a <= fechos[c] <= b for c, (a, b) in JANELAS.items())))
    vidas = todas; n = len(vidas); ritmo = sum(V['bancada'] for V in vidas) / max(1, sum(V['dia'] - 1 for V in vidas)); certo = all(V['prata'] and V['materia'] and V['nucleos'] and not V['quebrado'] and V['vivo'] for V in vidas)
    mal = sum(V['parou'] + V['pena'] + V['chao'] + V['jejum'] for V in vidas)
    dias = max(1, sum(V['dia'] - 1 for V in vidas))
    deu = (f"{n} vidas ({sum(V['cheia'] for V in vidas)} de até {ROBO['dias']} dias): {ritmo:.2f} blocos de bancada por dia; o jornal pago pelo que a mão vale (aprendiz, oficial, mestre), até {M.JORNADA} blocos por dia; {sum(V['camas'] for V in vidas) / dias:.2f} noite de cama e {sum(V['refeicoes'] for V in vidas) / dias:.2f} refeição pagas por dia; "
           f"noites no chão, jejuns, paradas do corpo e testes com pena: {mal}; a prata do mundo {'fecha' if all(V['prata'] for V in vidas) else 'NÃO FECHA'}; "
           f"a matéria e os núcleos entregues {'entraram todos em obra' if all(V['materia'] and V['nucleos'] for V in vidas) else 'NÃO FECHAM'}; estado {'inteiro' if not any(V['quebrado'] for V in vidas) else 'QUEBRADO'}")
    out.append(('O ROBÔ VIVE DE VERDADE: come, dorme, paga a cama, vive do jornal; a prata e a matéria fecham', deu, certo and mal == 0 and 3 <= ritmo <= 3.6))
    return out


# ---------- as provas ----------
def _melhor(n):
    med, c = mede(n, 5, **MELHOR); robo = oficio.chances(8 + ROBO['nivel'] + O.PREPARO_MAX + ROBO['afinidade'] // 10, O.contra(5))[0]
    return ('O MELHOR FERREIRO POSSÍVEL (Lendário, oficina 4, preparo 8, Afinidade 100) acerta a Lendária entre 15 e 30% das vezes',
            f"conta exata {c['acerta']:.1%} ({oficio.diz_conta(c)}); medido {med:.1%} em {n} obras; por pouco (sai Única) {c['pouco']:.1%}; com Afinidade {ROBO['afinidade']}, {robo:.1%}", 0.15 <= c['acerta'] <= 0.30 and bate(med, c['acerta'], n))


def _iniciante(n):
    com, cc = mede(n, 0, **VILA); rar, cr = mede(n, 2, **VILA); nu = oficio.chances(VILA['mao'] + VILA['nivel'] + VILA['afinidade'] // 10, O.contra(0))[0]
    return ('UM INICIANTE EM OFICINA DE VILA acerta a Comum em 85% ou mais, e a Rara em menos de 25% (a Comum, medida com os quatro preparos do Comum; a linha diz também a conta sem preparo nenhum)',
            f"Comum, com o preparo do Comum inteiro (+8): conta exata {cc['acerta']:.1%}, medido {com:.1%} em {n} obras (sem preparo nenhum: {nu:.1%}); Rara, onde aquele preparo não alcança: conta exata {cr['acerta']:.1%}, medido {rar:.1%}",
            cc['acerta'] >= 0.85 and cr['acerta'] < 0.25 and bate(com, cc['acerta'], n) and bate(rar, cr['acerta'], n))


def _conta_fecha(n):
    """obras Épicas de um Treinado mal preparado (quase todas falham): em cada uma, a matéria e o núcleo têm de fechar"""
    vistos = dict(acertou=0, abaixo=0, perdeu=0); erros = []
    for i in range(max(40, n // 5)):
        E = oficina_de_prova(i + 1, nivel=2, afinidade=50, mao=4, receita=3); peca = espada(3); nid = entrega(E, peca); receita = oficio.materia_de(peca)
        m0 = sum(oficio.materia_do_mundo(E).values()); p0 = oficio.prata_do_mundo(E); i0 = len(E['itens']['itens']); c0 = dict(E['gente']['eu']['carga'])
        R = oficio.forjar(E, 'eu', peca, blocos=0, nucleo=nid); oid = R['obra']
        aberta = sum(oficio.materia_do_mundo(E).values()) == m0 and all(E['gente']['eu'].get('carga', {}).get(k, 0) == c0[k] - q for k, q in receita.items()) and E['itens']['obras'][oid]['materia'] == receita
        estado.aplica(E, 'mestre', [['obra', oid, 'blocos', 'poe', O.blocos(3)]], texto='os blocos da prova'); F = oficio.remata(E, oid); vistos[F['fim']] += 1
        nasceu = [x for x in E['itens']['itens'].values() if x.get('feito_por') == 'eu']
        certo = (aberta and oid not in E['itens']['obras'] and sum(oficio.materia_do_mundo(E).values()) == m0 - sum(receita.values()) and nid not in E['itens']['itens'] and oficio.prata_do_mundo(E) == p0
                 and len(nasceu) == (0 if F['fim'] == 'perdeu' else 1) and len(E['itens']['itens']) == i0 - 1 + len(nasceu) and not estado.valida(E)
                 and (not nasceu or (nasceu[0]['cat'] == (3 if F['fim'] == 'acertou' else 2) and nasceu[0]['dia'] == E['relogio']['dia'] and nasceu[0]['dono'] == 'eu' and nasceu[0]['historia'])))
        if not certo: erros.append((i, F['fim']))
    return ('A CONTA FECHA: a matéria de uma obra falhada some do mundo, e o núcleo perdido sai do Livro de Itens',
            f"{sum(vistos.values())} obras Épicas: {vistos['perdeu']} perdidas (a matéria e o núcleo somem, nada nasce), {vistos['abaixo']} por pouco (nasce Rara, o núcleo se gasta), {vistos['acertou']} certas; contas erradas: {len(erros)}; a prata não mexe",
            not erros and vistos['perdeu'] > 0)


def _margens(n):
    """cada margem do teste dá a saída que o livro diz (o dado é posto à mão só aqui)"""
    al = 5; E = oficina_de_prova(nivel=2, afinidade=50, mao=4, prata=300, fogo=al, bigorna=al, receita=al, ajudante=al); L = lambda: E['itens']['itens']; ok = []; p0 = oficio.prata_do_mundo(E)
    def obra(cat, margem):
        oid, nid = obra_pronta(E, cat)
        with dado_posto([margem]): F = oficio.remata(E, oid)
        return F, L().get(F['item']) if F['item'] else None, nid
    for m, fim, cat in ((0, 'acertou', 2), (7, 'acertou', 2), (-1, 'abaixo', 1), (-4, 'abaixo', 1), (-5, 'perdeu', None), (-20, 'perdeu', None)):       # uma obra Rara
        F, it, _ = obra(2, m); ok.append(F['fim'] == fim and (it['cat'] if it else None) == cat and (not it or it['dur'] == [T.DUR[cat], T.DUR[cat]]))
    F, it, _ = obra(0, -1); ok.append(F['fim'] == 'abaixo' and it['cat'] == 0 and it['dur'] == [int(T.DUR[0] * O.TOSCA), T.DUR[0]]); tosca = it and it['dur']       # o Comum por pouco: tosco
    F, it, _ = obra(0, -5); ok.append(F['fim'] == 'perdeu' and it is None)
    F, it, nid = obra(4, -4); feito = E['gente']['eu'].get('marca', {}).get('feito_forja')                                                                # a Única por pouco: nasce Épica, o núcleo se gasta, e vale como feito de Mestre
    ok.append(F['fim'] == 'abaixo' and it['cat'] == 3 and nid not in L() and feito == 6 and it.get('nucleo_de') == 'bicho de prova' and it['feito_por'] == 'eu')
    F, it, nid = obra(3, -5); ok.append(F['fim'] == 'perdeu' and it is None and nid not in L())                                                           # a Épica perdida: o núcleo sai do Livro
    sem_nome = oficio.molde('arma', 2, familia='arco'); entrega(E, sem_nome); R = oficio.forjar(E, 'eu', sem_nome, blocos=0); estado.aplica(E, 'mestre', [['obra', R['obra'], 'blocos', 'poe', O.blocos(2)]], texto='os blocos da prova')
    with dado_posto([-1]): F = oficio.remata(E, R['obra'])                                                                                                # a obra sem nome próprio que sai uma abaixo: a peça ganha o nome da categoria em que saiu
    caiu = L()[F['item']]['nome']; ok.append(sem_nome['nome'] == 'arco Raro' and caiu == 'arco Incomum' and L()[F['item']]['cat'] == 1)
    estado.aplica(E, 'gera', [['item', 'nasce', item('arma', 2, 'Espada Rara de prova', familia='espada', dono='eu')]], texto='a peça de prova'); iid = f"i{E['itens']['seq']:04d}"; aj = []
    for m, fim in ((-1, 'falhou'), (-5, 'estragou'), (0, 'acertou')):                                                                                     # o ajuste
        repousa(E); d0 = L()[iid]['dur'][0]
        with dado_posto([m]): R = oficio.ajustar(E, 'eu', iid)
        it = L()[iid]; aj.append(R['fim']); ok.append(R['fim'] == fim and bool(it.get('sob_medida')) == (m >= 0) and it['dur'][0] == d0 - (O.AJUSTE_ESTRAGO if fim == 'estragou' else 0))
    return ('AS MARGENS (o dado posto à mão, só nesta prova): passar dá a peça; falhar por 1 a 4, uma categoria abaixo (o Comum, tosco); por 5 ou mais, nada, e o núcleo sai do Livro',
            f"{sum(ok)} de {len(ok)} saídas certas: a Rara com margem 0, +7, −1, −4, −5, −20; o Comum por −1 sai tosco ({tosca}); a Única por −4 nasce Épica, gasta o núcleo e vale como feito de Mestre; "
            f"a Épica por −5 leva o núcleo; a obra sem nome próprio (\"{sem_nome['nome']}\") que sai uma abaixo nasce \"{caiu}\"; o ajuste por −1, −5 e 0: {', '.join(aj)}", all(ok) and not estado.valida(E) and oficio.prata_do_mundo(E) == p0)


def _obra_aberta(n):
    d = tempfile.mkdtemp(prefix='m10_oficio_'); antes = os.environ.get('MOTOR10_MUNDO'); os.environ['MOTOR10_MUNDO'] = d
    try:
        estado.grava(oficina_de_prova(nivel=2, afinidade=50, mao=2, prata=200, carga={'metal:2': 3}))
        E = estado.carrega(); p0 = oficio.prata_do_mundo(E); R = oficio.forjar(E, 'eu', espada(2)); oid = R['obra']; estado.grava(E); o1 = copy.deepcopy(E['itens']['obras'].get(oid)); parou = (R['feitos'], R['parou'])
        E = estado.carrega(); o2 = E['itens']['obras'].get(oid); voltas = 0; sem_materia = E['gente']['eu'].get('carga', {}).get('metal:2', 0) == 0
        while not R['fim'] and voltas < 6:
            repousa(E); R = oficio.continua(E, 'eu'); estado.grava(E); E = estado.carrega(); voltas += 1
        evs = [json.loads(x) for x in open(os.path.join(d, 'eventos.jsonl'), encoding='utf-8').read().splitlines()]; blocos = sum(1 for e in evs if any(x[0] == 'obra' and x[2:4] == ['blocos', 'soma'] for x in e['efeitos']))
        certo = (parou[1] and 0 < parou[0] < O.blocos(2) and o1 == o2 and o1['blocos'] == parou[0] and sem_materia and R['fim'] in ('acertou', 'abaixo', 'perdeu') and oid not in E['itens']['obras']
                 and blocos == O.blocos(2) == E['gente']['eu']['treino']['forja'] and len(E['turno']['dados']) == 1 and E['relogio']['dia'] > 1 and not estado.valida(E) and oficio.prata_do_mundo(E) == p0)
        return ('A OBRA ABERTA: a obra de vários dias sobrevive a gravar e abrir o estado; o ato para quando o corpo cruza um limiar; o teste só sai no último bloco',
                f"a obra Rara parou no bloco {parou[0]} de {O.blocos(2)} ({parou[1]}); gravada e aberta de novo, {'igual' if o1 == o2 else 'DIFERENTE'}; fechou no Dia {E['relogio']['dia']} com {blocos} blocos e {len(E['turno']['dados'])} teste ({R['fim']})", certo)
    finally:
        os.environ.pop('MOTOR10_MUNDO', None)
        if antes is not None: os.environ['MOTOR10_MUNDO'] = antes
        shutil.rmtree(d, ignore_errors=True)


def _conserto(n):
    E = oficina_de_prova(nivel=1, afinidade=50, mao=2, prata=500, carga={'metal:2': 2})
    estado.aplica(E, 'gera', [['item', 'nasce', item('arma', 2, 'Espada Rara de prova', familia='espada', dono='eu')]], texto='a peça de prova'); iid = f"i{E['itens']['seq']:04d}"
    estado.aplica(E, 'mestre', [['item', iid, 'dur', 'soma', -20]], texto='a peça gasta'); tabela = round(O.preco(2) * M.CONSERTO_PONTO * 10)
    eu0 = E['gente']['eu']['moedas']; vila0 = E['lugares']['vila']['estoque']['prata']; total0 = oficio.prata_do_mundo(E); t0 = estado.agora(E)
    R = oficio.consertar(E, 'eu', iid, pontos=10, pago=True); it = E['itens']['itens'][iid]
    pago = (R['custo'] == tabela == 216 and E['gente']['eu']['moedas'] == eu0 - tabela and E['lugares']['vila']['estoque']['prata'] == vila0 + tabela and oficio.prata_do_mundo(E) == total0 and it['dur'] == [20, 30] and estado.agora(E) - t0 == 1)
    t1 = estado.agora(E); R2 = oficio.consertar(E, 'eu', iid, pontos=10); it = E['itens']['itens'][iid]; p = E['gente']['eu']
    meu = it['dur'] == [30, 30] and estado.agora(E) - t1 == 2 and p.get('carga', {}).get('metal:2', 0) == 1 and p['moedas'] == eu0 - tabela and p['treino']['forja'] == 2 and not estado.valida(E)
    return ('O CONSERTO: 10 pontos de uma peça Rara custam o que a tabela diz (2% de 1.080 por ponto), e a prata vai para a oficina; feito por você, custa tempo e matéria',
            f"pago: {R['custo']} de prata (a tabela diz {tabela}), o dono {eu0} → {eu0 - R['custo']}, a oficina {vila0} → {E['lugares']['vila']['estoque']['prata']}, em {R['feitos']} bloco; "
            f"na sua bancada: {R2['pontos']} pontos em {R2['feitos']} blocos, com 1 de metal Raro e nenhuma prata", pago and meu)


def _sob_medida(n):
    al = 5; E = oficina_de_prova(nivel=2, afinidade=50, mao=4, prata=300, fogo=al, bigorna=al, receita=al, ajudante=al)
    E['gente']['outro'] = dict(copy.deepcopy(E['gente']['eu']), nome='Bera', jogador=False)                 # a mão do gerador: mais uma pessoa na vila
    estado.aplica(E, 'gera', [['item', 'nasce', item('arma', 2, 'Espada Rara de prova', familia='espada', dono='eu')], ['item', 'i0001', 'uso', 'poe', None]], texto='a peça de prova'); iid = f"i{E['itens']['seq']:04d}"
    estado.aplica(E, 'gera', [['item', iid, 'uso', 'poe', 'arma']], texto='o Aldric empunha a peça'); antes = ficha(estado.lutador(E, 'eu'))['arma']; fins = []; t0 = estado.agora(E); p0 = oficio.prata_do_mundo(E)
    for _ in range(40):
        t0 = estado.agora(E); R = oficio.ajustar(E, 'eu', iid); fins.append(R['fim']); gasto = estado.agora(E) - t0
        if R['fim'] == 'acertou': break
        repousa(E)
    it = E['itens']['itens'][iid]; sm = it.get('sob_medida') or {}; dono = ficha(estado.lutador(E, 'eu'))['arma']
    estado.aplica(E, 'mestre', [['item', iid, 'dono', 'poe', 'outro'], ['item', iid, 'uso', 'poe', 'arma']], texto='a peça passa para outra mão'); outro = ficha(estado.lutador(E, 'outro'))['arma']
    certo = (fins[-1] == 'acertou' and sm.get('dono') == 'Aldric' and sm.get('grau') == O.ajuste_grau(4) == 2 and gasto == O.ajuste_blocos(2) and dono['cat'] == 2 and dono['acerto'] == antes['acerto'] + 1
             and outro['cat'] == 1 and outro['mult'] * 3 == dono['mult'] and not estado.valida(E) and oficio.prata_do_mundo(E) == p0)
    return ('SOB MEDIDA: a peça ajustada rende no dono e rende uma categoria abaixo na mão de outro (pessoas.ficha)',
            f"ajuste de um Treinado numa espada Rara: {len(fins)} tentativa(s) de {O.ajuste_blocos(2)} blocos ({', '.join(fins)}); grau {sm.get('grau')}, gravada para {sm.get('dono')}; "
            f"no dono: {T.CATS[dono['cat']]}, acerto {antes['acerto']:g} → {dono['acerto']:g}, × {dono['mult']:g}; na mão de outro: {T.CATS[outro['cat']]}, acerto {outro['acerto']:g}, × {outro['mult']:g}", certo)


def _maestria(n):
    al = 5; E = oficina_de_prova(nivel=4, afinidade=60, prata=100, fogo=al, bigorna=al, receita=al, ajudante=al); I, Tr, Me, Le = (O.OFICIO_BLOCOS[g] for g in (2, 4, 6, 8)); p0 = oficio.prata_do_mundo(E)
    estado.aplica(E, 'mestre', [['pessoa', 'eu', 'treino.forja', 'soma', I - 2]], texto='dias de bancada, para a prova'); oficio.jornal(E, 'eu', 1); a = oficio.mao(E['gente']['eu']); oficio.jornal(E, 'eu', 1); b = oficio.mao(E['gente']['eu'])
    estado.aplica(E, 'mestre', [['pessoa', 'eu', 'treino.forja', 'soma', Le]], texto='anos de bancada, para a prova'); falta = oficio.sobe(E, 'eu'); c = oficio.mao(E['gente']['eu']); obras = 0
    while oficio.mao(E['gente']['eu']) < 6 and obras < 60:                                  # o feito de Mestre: uma Épica nascida da própria mão
        oid, _ = obra_pronta(E, 3); oficio.remata(E, oid); obras += 1
    d = oficio.mao(E['gente']['eu']); feito = E['gente']['eu'].get('marca', {}).get('feito_forja'); obras2 = 0
    while oficio.mao(E['gente']['eu']) < 8 and obras2 < 80:                                 # o de Lendário: uma Única
        oid, _ = obra_pronta(E, 4); oficio.remata(E, oid); obras2 += 1
    e = oficio.mao(E['gente']['eu'])
    return ('A MAESTRIA DE FORJA sobe por blocos de bancada; de Mestre para cima, os blocos não bastam: pede uma obra nascida (Mestre: Épica; Lendário: Única)',
            f"com {I - 1} blocos: {T.MAESTRIAS[a]}; com {I}: {T.MAESTRIAS[b]}; com {I + Le} e nenhuma obra: {T.MAESTRIAS[c]}{falta.split(';')[0] + ')' if falta else ''}; depois da primeira Épica nascida ({obras} obra(s)): {T.MAESTRIAS[d]}; "
            f"depois da primeira Única ({obras2} obra(s)): {T.MAESTRIAS[e]}", (a, b, c, d, e) == (0, 2, 4, 6, 8) and feito == 6 and 'falta o feito' in falta and not estado.valida(E) and oficio.prata_do_mundo(E) == p0)


def _recusas(n):
    E = oficina_de_prova(nivel=1, afinidade=50, prata=5, carga={'metal:0': 3, 'metal:2': 3})
    estado.aplica(E, 'gera', [['item', 'nasce', dict(tipo='nucleo', cat=4, nome='Núcleo Único de prova', dur=[1, 1], dono='eu', onde=None, de='bicho de prova', historia=[])],
                              ['item', 'nasce', item('arma', 2, 'Espada Rara de prova', familia='espada', dono='eu')], ['item', 'i0001', 'dur', 'soma', -5]], texto='as peças de prova')
    S = PM.vila(); estado.aplica(S, 'gera', [['pessoa', 'eu', 'carga.metal:0', 'soma', 3]], texto='matéria sem oficina')        # uma vila sem oficina
    casos = [('forjar onde não há oficina', lambda: oficio.forjar(S, 'eu', espada(0))), ('forjar sem a matéria', lambda: oficio.forjar(E, 'eu', espada(1))),
             ('forjar uma Épica sem núcleo', lambda: oficio.forjar(E, 'eu', espada(3))), ('forjar uma Épica com um núcleo Único', lambda: oficio.forjar(E, 'eu', espada(3), nucleo='i0003')),
             ('forjar acima do Lendário', lambda: oficio.forjar(E, 'eu', oficio.molde('arma', 6, 'Espada Mítica', familia='espada'))), ('forjar as mãos', lambda: oficio.molde('arma', 0, 'Punho', familia='punho')),
             ('pôr núcleo numa obra Comum', lambda: oficio.forjar(E, 'eu', espada(0), nucleo='i0003')), ('consertar, pago, sem a prata', lambda: oficio.consertar(E, 'eu', 'i0004', pontos=10, pago=True)),
             ('consertar uma peça inteira', lambda: oficio.consertar(E, 'eu', 'i0002')), ('consertar uma Rara sem a mão (Leigo)', lambda: oficio.consertar(E, 'eu', 'i0004', pontos=5)),
             ('consertar um núcleo', lambda: oficio.consertar(E, 'eu', 'i0003')), ('ajustar sem a mão (Leigo)', lambda: oficio.ajustar(E, 'eu', 'i0001')),
             ('continuar uma obra que não existe', lambda: oficio.continua(E, 'eu')), ('servir na bancada onde não há oficina', lambda: oficio.jornal(S, 'eu', 1))]
    estado.aplica(E, 'mestre', [['item', 'i0004', 'dur', 'soma', -10]], texto='a peça gasta'); antes = retrato(E), retrato(S)
    rec = [nome for nome, f in casos if recusa(f)]; igual = antes == (retrato(E), retrato(S))
    R = oficio.forjar(E, 'eu', espada(0), blocos=0); cedo = recusa(lambda: oficio.remata(E, R['obra'])); oficio.larga(E, 'eu', R['obra']); voltou = E['gente']['eu']['carga'].get('metal:0') == 3 and not E['itens']['obras']
    estado.aplica(E, 'gera', [['pessoa', 'eu', 'moedas', 'soma', 50]], texto='prata para a prova'); peca = espada(4); nid = entrega(E, peca); m0 = sum(oficio.materia_do_mundo(E).values())
    R = oficio.forjar(E, 'eu', peca, blocos=2, nucleo=nid); oficio.larga(E, 'eu', R['obra'])                                    # largar uma obra que já foi ao fogo: a matéria se perde, o núcleo fica
    largou = sum(oficio.materia_do_mundo(E).values()) == m0 - 3 and E['itens']['itens'].get(nid, {}).get('dono') == 'eu' and not E['itens']['obras'] and E['gente']['eu']['treino']['forja'] == 2
    repousa(E); estado.aplica(E, 'mestre', [['estoque', 'vila', 'prata', 'soma', -E['lugares']['vila']['estoque']['prata']], ['pessoa', 'eu', 'moedas', 'soma', E['lugares']['vila']['estoque']['prata']]], texto='a oficina fica sem prata')
    total = oficio.prata_do_mundo(E); J = oficio.jornal(E, 'eu', 1); sem_paga = J['feitos'] == 1 and J['ganhou'] == 0 and E['gente']['eu']['treino']['forja'] == 3 and oficio.prata_do_mundo(E) == total
    M2 = oficina_de_prova(nivel=1, carga={'metal:0': 3}); estado.aplica(M2, 'gera', [['item', 'i0001', 'uso', 'poe', None], ['item', 'i0002', 'uso', 'poe', None]], texto='o Aldric tira as peças')
    oficio.forjar(M2, 'eu', espada(0), blocos=0); estado.aplica(M2, 'mestre', [['pessoa', 'eu', 'pv', 'soma', -9999], ['pessoa', 'eu', 'estado', 'poe', 'morto']], texto='o ferreiro morre, para a prova')
    L2 = M2['itens']['itens']; caiu = all(it.get('dono') is None and it.get('onde') == 'vila' and it.get('solto') for it in L2.values())
    desfez = not estado.valida(M2) and not M2['itens']['obras'] and caiu and not M2['gente']['eu'].get('carga') and M2['gente']['eu']['moedas'] == 0       # a regra da morte: a obra se desfaz NA HORA, e o que era dele cai solto onde morreu
    with contextlib.redirect_stdout(io.StringIO()) as tela: oficio.main([])
    uso = tela.getvalue().startswith('oficio.py') and 'Uso' in tela.getvalue()
    tortas = [recusa(lambda a=a: oficio.main(a)) or '' for a in (['jornal', '0'], ['jornal', 'x'], ['jornal'])]              # o número torto: UMA frase que diz o que falta, e não o uso inteiro
    uso = uso and all(t.startswith('diga quantos blocos de jornal') and len(t.splitlines()) == 1 for t in tortas)
    return ('AS RECUSAS: o que não pode abrir não abre, e nada muda pela metade; sem argumento, o script só diz o uso; o jornal com número torto ganha uma frase',
            f"{len(rec)} de {len(casos)} recusados" + ('' if len(rec) == len(casos) else f" (passaram: {', '.join(x for x, _ in casos if x not in rec)})") + f"; estado {'intacto' if igual else 'MUDOU'}; "
            f"teste antes de os blocos fecharem: {'recusado' if cedo else 'ACEITO'}; obra largada com zero blocos devolve a matéria: {'sim' if voltou else 'NÃO'}; largada com dois blocos, perde a matéria e fica com o núcleo: {'sim' if largou else 'NÃO'}; "
            f"oficina sem prata não paga o jornal, e o bloco conta: {'sim' if sem_paga else 'NÃO'}; a obra de quem morreu se desfaz na hora da morte, e o que era dele cai solto onde morreu (o estado segue inteiro): {'sim' if desfez else 'NÃO'}; sem argumento, só o uso, e `jornal 0`, `jornal x` e `jornal` com uma frase cada: {'sim' if uso else 'NÃO'}",
            len(rec) == len(casos) and igual and cedo and voltou and largou and sem_paga and desfez and uso and not estado.valida(E))


def provas(n=300):
    out = []; m = max(400, 2 * n)
    def roda(nome, f):
        try: out.extend(f())
        except (SystemExit, Exception) as e: out.append((nome or 'PROVA DO OFÍCIO', f'A PROVA QUEBROU: {type(e).__name__}: {e}', False))
    cheias = max(20, n // 10); curtas = max(20, n // 15)
    roda('A ESCADA E O ROBÔ FERREIRO', lambda: escada([vida(s + 1) for s in range(cheias)] + [vida(cheias + s + 1, dias=ROBO['curta'], ate=4) for s in range(curtas)]))
    for nome, f in (('O MELHOR FERREIRO', lambda: [_melhor(m)]), ('O INICIANTE NA VILA', lambda: [_iniciante(m)]), ('A CONTA FECHA', lambda: [_conta_fecha(n)]), ('AS MARGENS', lambda: [_margens(n)]), ('A OBRA ABERTA', lambda: [_obra_aberta(n)]),
                    ('O CONSERTO', lambda: [_conserto(n)]), ('SOB MEDIDA', lambda: [_sob_medida(n)]), ('A MAESTRIA', lambda: [_maestria(n)]), ('AS RECUSAS', lambda: [_recusas(n)])):
        roda(nome, f)
    return out


def main():
    a = sys.argv[1:]
    if a and not a[0].isdigit(): print(__doc__); return True
    n = int(a[0]) if a else 300
    print('BANCO DE PROVAS DO OFÍCIO · etapa 2: forjar, consertar, ajustar\n')
    res = provas(n)
    for nome, deu, passa in res: print(f"  {'passa' if passa else 'FALHA'}  {nome}: {deu}")
    print(f'\n{sum(p for _, _, p in res)} de {len(res)} provas passam.')
    return all(p for _, _, p in res)


if __name__ == '__main__':
    sys.exit(0 if main() else 1)
