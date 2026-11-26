#!/usr/bin/env python3
"""provas_oficio.py — MOTOR 10: O BANCO DE PROVAS DO OFÍCIO (etapa 2: forjar, consertar, ajustar).

As metas são as do contrato (projeto/ETAPA2.md, seção 5). As provas rodam em mundos de rascunho (a vila de prova do provas_mundo, com uma oficina);
nunca num save. O dado é o de verdade (teste.rola): por isso as medidas de chance trazem também a conta exata, e a escada é medida em muitas vidas.

O ROBÔ FERREIRO vive de verdade: dorme na cama e paga, come e paga, trabalha na bancada enquanto o corpo deixa (3,5 blocos por dia), vive do jornal
da oficina, e tem a matéria e o núcleo de cada obra na mão. Ele segue o caminho comum: um degrau de cada vez, e só abre a obra de um degrau quando
tem a mão que a obra pede (tabelas_oficio.MAO_DA_OBRA). Repete o degrau até a peça nascer, com matéria e núcleo novos a cada obra.
A MEDIDA DA ESCADA é o dia em que metade das vidas já tinha a peça (quem nunca a teve conta como nunca). A linha diz também quando a primeira obra fecha.
A LENDÁRIA É DIFERENTE, por decisão do jogador, e a prova dela julga DUAS coisas: (i) o dia em que a primeira OBRA fecha (a primeira tentativa: dias 300 a 450);
(ii) a peça é RARA DE PROPÓSITO: nasce até o Dia 450 em pelo menos uma vida e em menos da metade delas (RARA_DE_PROPOSITO). É isto que é só dela:
se a chance subir e a Lendária passar a nascer na metade das vidas, ou se deixar de nascer, a prova falha.
Uma linha à parte ("o ritmo da bancada") confere a outra leitura da meta: o dia em que a primeira obra de cada categoria fecha, acerte ou não.

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
RARA_DE_PROPOSITO = (1, 0.5)        # ... e a peça Lendária é rara de propósito: até o Dia 450 nasce em pelo menos tantas vidas (1) e em MENOS desta fração delas (a metade). Medido: de 3 a 12 de 30
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
            r = R['rolagem']; alvo = R['cat'] if R.get('cat') is not None else next(c for c in range(O.FORJA_ATE + 1) if O.contra(c) == r['contra']); V['pena'] += r['pena'] != 0
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
        if cat in PELA_OBRA:    # a Lendária julga DUAS coisas: a primeira TENTATIVA (o dia em que a primeira obra fecha), e a peça RARA DE PROPÓSITO (nasce em pelo menos uma vida e em menos da metade)
            lo, hi = RARA_DE_PROPOSITO; rara = lo <= len(tem) < n * hi
            deu = (f"a primeira obra {oficio.FEM[cat]} fecha no Dia {f}" if f is not None else f"a primeira obra {oficio.FEM[cat]} NÃO FECHA na metade das {n} vidas até o Dia {ate}")
            deu += f"; a peça nasceu em {len(tem)} de {n} vidas até o Dia {ate}" + (f", entre o Dia {min(tem)} e o {max(tem)}" if tem else '') + (f" (a faixa: de {lo} a menos de {n * hi:g})" if rara else f" (FORA DA FAIXA: de {lo} a menos de {n * hi:g})")
            if prim: deu += f"; acerta de primeira em {sum(prim) / len(prim):.0%} das vidas ({tent / n:.1f} obras por vida)"
            deu += (f". COM QUE ISTO VALE: na {O.OFICINAS[ROBO['nivel']]} (+{ROBO['nivel']}), com os quatro preparos (+{O.PREPARO_MAX}) desde o Dia 1, e com matéria e núcleo novos a cada obra: {tent / n:.1f} {o_que} por vida (a pior vida: {pior})"
                    + (f". COM UM NÚCLEO SÓ, a peça nasce em {sum(prim) / len(prim):.0%} das vidas; nas outras, o núcleo se gastou ou se perdeu" if prim else ''))
            out.append((f"A ESCADA, {oficio.FEM[cat].upper()}: a primeira OBRA {oficio.FEM[cat]} do robô ferreiro FECHA entre os dias {a} e {b} (a primeira tentativa), E a peça é rara de propósito: até o Dia {ate} nasce em pelo menos {lo} e em menos da metade das vidas (na melhor oficina, com o preparo todo e com núcleo novo a cada obra)",
                        deu, f is not None and a <= f <= b and rara))
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
                 and (not nasceu or ((nasceu[0]['cat'] == 3 if F['fim'] == 'acertou' else nasceu[0]['cat'] < 3) and nasceu[0]['dia'] == E['relogio']['dia'] and nasceu[0]['dono'] == 'eu' and nasceu[0]['historia'])))
        if not certo: erros.append((i, F['fim']))
    return ('A CONTA FECHA: a matéria de uma obra falhada some do mundo, e o núcleo perdido sai do Livro de Itens',
            f"{sum(vistos.values())} obras Épicas: {vistos['perdeu']} perdidas (a matéria e o núcleo somem, nada nasce), {vistos['abaixo']} abaixo (nasce peça menor, o núcleo se gasta), {vistos['acertou']} Épicas; contas erradas: {len(erros)}; a prata não mexe",
            not erros and vistos['perdeu'] > 0)


def _margens(n):
    """(a Lei do Valor) cada total dá a categoria que o livro diz (o dado posto à mão só aqui): a maior CD alcançada, até o teto; abaixo da CD do Comum, perde;
    o núcleo se gasta em qualquer saída; os dados especiais (as faces postas no _resolve) e o poder das ferramentas"""
    al = 5; E = oficina_de_prova(nivel=2, afinidade=50, mao=4, prata=300, fogo=al, bigorna=al, receita=al, ajudante=al); L = lambda: E['itens']['itens']; ok = {}; p0 = oficio.prata_do_mundo(E); CD = O.VALOR_CD
    def obra(cat, total):
        oid, nid = obra_pronta(E, cat)
        with dado_posto([total - CD[min(cat, len(CD) - 1)]]): F = oficio.remata(E, oid)
        return F, L().get(F['item']) if F['item'] else None, nid
    for total, quer in ((CD[2], 2), (CD[2] + 40, 2), (CD[2] - 1, 1), (CD[1], 1), (CD[1] - 1, 0), (CD[0], 0), (CD[0] - 1, None)):        # a matéria Rara: o teto é o Raro
        F, it, _ = obra(2, total); ok[f'rara_{total}'] = (it['cat'] if it else None) == quer and (not it or it['dur'] == [T.DUR[it['cat']], T.DUR[it['cat']]])
    for total, quer in ((CD[1], 1), (CD[2] + 10, 1), (CD[0], 0), (CD[0] - 1, None)):                                                    # a matéria Comum: o teto é o Incomum
        F, it, _ = obra(0, total); ok[f'comum_{total}'] = (it['cat'] if it else None) == quer
    F, it, nid = obra(4, CD[4]); ok['unica'] = it['cat'] == 4 and nid not in L()
    F, it, nid = obra(4, CD[3]); ok['unica_abaixo'] = it['cat'] == 3 and nid not in L() and E['gente']['eu'].get('marca', {}).get('feito_forja', 0) >= 6      # nasce Épica: vale como feito de Mestre
    F, it, nid = obra(3, CD[0] - 1); ok['epica_perdida'] = it is None and nid not in L()                                                 # a Épica perdida: o núcleo sai do Livro
    sem_nome = oficio.molde('arma', 2, familia='arco'); entrega(E, sem_nome); R = oficio.forjar(E, 'eu', sem_nome, blocos=0); estado.aplica(E, 'mestre', [['obra', R['obra'], 'blocos', 'poe', O.blocos(2)]], texto='os blocos da prova')
    with dado_posto([CD[1] - CD[2]]): F = oficio.remata(E, R['obra'])
    caiu = L()[F['item']]['nome']; ok['nome'] = sem_nome['nome'] == 'arco Raro' and caiu == 'arco Incomum'
    Rs = oficio._resolve                                                                                                                # os dados especiais, com as faces postas
    d11 = Rs(CD[2] + 5, 1, 1, 2, -1); ok['dois_1'] = len(d11) == 1 and d11[0][1]['cat'] is None
    u1 = {x['d6']: x for _, x in Rs(CD[1] + 1, 1, 9, 2, -1)}; ok['um_1'] = u1[1]['cat'] is None and u1[2]['cat'] == 0 and u1[3]['cat'] == 0 and u1[4]['cat'] == 1 and u1[4]['gasta'] and u1[6]['gasta']
    d20 = {x['d6']: x for _, x in Rs(CD[1] + 1, 20, 20, 2, -1)}; ok['dois_20'] = d20[1]['cat'] == 2 and d20[1]['sobe'] and d20[5]['cat'] == 1 and d20[5]['mais_efeito'] == 1
    d20t = {x['d6']: x for _, x in Rs(CD[2] + 1, 20, 20, 2, -1)}; ok['dois_20_no_teto'] = d20t[1]['cat'] == 2 and d20t[1]['mais_efeito'] == 1
    ok['quase'] = Rs(CD[2] - 1, 5, 9, 2, -1)[0][1]['quase'] and not Rs(CD[2] - 1 - O.VALOR_QUASE, 5, 9, 2, -1)[0][1]['quase'] and not Rs(CD[1] + 30, 5, 9, 1, -1)[0][1]['quase']
    ok['poder'] = Rs(CD[0] - 3, 5, 9, 2, 2)[0][1]['cat'] == 0 and Rs(CD[0] - 6, 5, 9, 2, 2)[0][1]['cat'] is None and Rs(CD[0] - 30, 1, 1, 2, 3)[0][1]['cat'] == 0
    ok['soma_1'] = all(abs(sum(oficio.dist_valor(s_, t_).values()) - 1) < 1e-9 for s_, t_ in ((0, 1), (20, 2), (60, 5)))
    falhas = [k for k, v in ok.items() if not v]
    return ('AS MARGENS DA LEI DO VALOR (o dado posto à mão, só nesta prova): a peça sai na maior CD alcançada, até o teto (sem núcleo, uma acima da matéria e nunca acima do Raro); abaixo da CD do Comum, perde; o núcleo se gasta; os dados especiais; o poder das ferramentas',
            f"{sum(ok.values())} de {len(ok)} saídas certas" + (f"; falham: {', '.join(falhas)}" if falhas else ''), not falhas and not estado.valida(E) and oficio.prata_do_mundo(E) == p0)


def _ferreiro(nivel, afinidade, mao, prep=None, ferramentas=(), semente=1):
    """um ferreiro de prova para as metas da Lei do Valor: a oficina, a mão, o preparo (o alcance de todos os quatro; None: nenhum) e as ferramentas [(forma, cat, afinada)]"""
    al = prep; E = oficina_de_prova(semente, nivel=nivel, afinidade=afinidade, mao=mao, fogo=al, bigorna=al, receita=al, ajudante=al)
    ef = [['item', 'nasce', item('ferramenta', cat, oficio='forja', forma=forma, dono='eu', efeitos=[{'chave': 'afinada'}] if af else [])] for forma, cat, af in ferramentas]
    if ef: estado.aplica(E, 'gera', ef, onde='vila', texto='as ferramentas de prova')
    return E


METAS_VALOR = [       # (o nome, o ferreiro, a categoria da obra, as faixas: {categoria ou 'perde': (de, até)})
    ('T1 FERORD HOJE, matéria Comum (Treinado, Afinidade 70, forja de vila, preparo +6 até o Incomum, jogo de forja Comum afinado)', dict(nivel=1, afinidade=70, mao=4, prep=None, ferramentas=(('jogo', 0, True),), so=dict(receita=1, fogo=1, bigorna=1)), 0, {0: (0.80, 1), 1: (0, 0.20), 'perde': (0, 0.05)}),
    ('T1 FERORD HOJE, matéria Incomum', dict(nivel=1, afinidade=70, mao=4, prep=None, ferramentas=(('jogo', 0, True),), so=dict(receita=1, fogo=1, bigorna=1)), 1, {1: (0.50, 0.70), 2: (0, 0.05), 'perde': (0, 0.05)}),
    ('T2 UM INICIANTE (Iniciante, Afinidade 50, forja de vila, sem preparo, sem ferramenta), matéria Comum', dict(nivel=1, afinidade=50, mao=2), 0, {0: (0.70, 0.85), 'perde': (0.10, 0.25), 1: (0, 0.05)}),
    ('T3 UM MESTRE (Mestre, Afinidade 80, grande forja, preparo +8, martelo e tenaz Raros), matéria Rara', dict(nivel=3, afinidade=80, mao=6, prep=5, ferramentas=(('martelo', 2, False), ('tenaz', 2, False))), 2, {2: (0.60, 0.80)}),
    ('T3 O MESMO MESTRE, com um núcleo Épico', dict(nivel=3, afinidade=80, mao=6, prep=5, ferramentas=(('martelo', 2, False), ('tenaz', 2, False))), 3, {3: (0.30, 0.50)}),
    ('T4 O MELHOR POSSÍVEL (Lendário, Afinidade 100, forja mestra, preparo +8, martelo e tenaz Lendários), matéria Rara e núcleo Lendário', dict(nivel=4, afinidade=100, mao=8, prep=5, ferramentas=(('martelo', 5, False), ('tenaz', 5, False))), 5, {5: (0.15, 0.30)}),
]


def _monta(f, semente=1):
    f = dict(f); so = f.pop('so', None); E = _ferreiro(semente=semente, **f)
    if so: estado.aplica(E, 'gera', [['lugar', 'vila', 'preparo.' + k, 'poe', v] for k, v in so.items() if k in ('fogo', 'bigorna')] + [['pessoa', 'eu', 'marca.prep_' + k, 'poe', v] for k, v in so.items() if k in ('receita', 'ajudante')], onde='vila', texto='o preparo de prova')
    return E


def _valor_metas(n):
    """as metas da Lei do Valor (decisão do jogador, Dia 30: com poucos buffs a peça sai Comum; com muitos, Rara e Épica; a Lendária segue difícil), pela conta exata;
    e uma delas medida com o dado de verdade, obra por obra, para conferir que a conta exata é a que o remate faz"""
    out = []
    for nome, f, cat, faixas in METAS_VALOR:
        E = _monta(f); c = oficio.valor(E, 'eu', cat); ch = c['chances']; viu = {}; passa = True
        for k, (a, b) in faixas.items():
            x = ch.get(None if k == 'perde' else k, 0); viu[k] = x; passa = passa and a - 1e-9 <= x <= b + 1e-9
        tab = ' · '.join(f"{T.CATS[k] if k is not None else 'perde'} {v:.1%}" for k, v in sorted(ch.items(), key=lambda kv: -1 if kv[0] is None else kv[0]) if v >= 0.0005)
        meta = ' · '.join(f"{T.CATS[k] if k != 'perde' else 'perde'} de {a:.0%} a {b:.0%}" for k, (a, b) in faixas.items())
        out.append((f"A LEI DO VALOR, {nome}: {meta}", f"{oficio.diz_valor(c).split(' · a peça sai')[0]} → {tab}", passa))
    E = _monta(METAS_VALOR[1][1]); c = oficio.valor(E, 'eu', 1); esperado = c['chances'].get(1, 0); m = max(200, n); vistos = 0          # T1 com matéria Incomum, obra por obra
    for i in range(m):
        Ei = _monta(METAS_VALOR[1][1], semente=i + 1); oid, _ = obra_pronta(Ei, 1); F = oficio.remata(Ei, oid); vistos += F.get('sai') == 1
    out.append(('A LEI DO VALOR, O DADO DE VERDADE: a fração de peças Incomuns nas obras de Ferord com matéria Incomum bate com a conta exata (4 desvios)', f"medido {vistos / m:.1%} em {m} obras; a conta exata {esperado:.1%}", bate(vistos / m, esperado, m)))
    teto_ok = O.teto(0) == 1 and O.teto(1) == 2 and O.teto(2) == 2 and all(O.teto(k) == k for k in range(3, O.FORJA_ATE + 1))
    out.append(('T5 A ECONOMIA: sem núcleo a peça sobe no máximo uma categoria acima da matéria e nunca acima do Raro (a Rara não nasce de matéria Comum); com núcleo, até a categoria dele',
                f"o teto: matéria Comum → {T.CATS[O.teto(0)]}, Incomum → {T.CATS[O.teto(1)]}, Rara → {T.CATS[O.teto(2)]}; núcleo Épico → {T.CATS[O.teto(3)]}, Único → {T.CATS[O.teto(4)]}, Lendário → {T.CATS[O.teto(5)]}", teto_ok))
    return out


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


def _ferramentas(n):
    """(a Lei do Valor) O MARTELO DE FORJA E A TENAZ: cada lugar pega a melhor peça que a pessoa tem (o jogo serve nos dois), pela tabela da categoria; a de outro ofício,
    a quebrada e a de outra pessoa não valem; a afinada soma uma vez; a forja de cada uma (matéria, nome, forma); os efeitos que os dados dão; e o comando de escolher o efeito"""
    ok = {}; al = 5; VM, VT, VA = O.VALOR_MARTELO, O.VALOR_TENAZ, O.VALOR_AFINADA
    E = oficina_de_prova(nivel=2, afinidade=50, mao=4, prata=300, fogo=al, bigorna=al, receita=al, ajudante=al); L = lambda: E['itens']['itens']; p0 = oficio.prata_do_mundo(E)
    def nasce(it): estado.aplica(E, 'gera', [['item', 'nasce', it]], onde='vila', texto='a peça de prova'); return f"i{E['itens']['seq']:04d}"
    def obra(cat, margem, peca=None):
        peca = peca or espada(cat); nid = entrega(E, peca); R = oficio.forjar(E, 'eu', peca, blocos=0, nucleo=nid)
        estado.aplica(E, 'mestre', [['obra', R['obra'], 'blocos', 'poe', O.blocos(peca['cat'])]], texto='os blocos da prova')
        with dado_posto([margem]): F = oficio.remata(E, R['obra'])
        return F, L().get(F['item']) if F['item'] else None
    vf = lambda: oficio.valor_ferramentas(E, 'eu')
    sem = vf()
    ij = nasce(item('ferramenta', 0, oficio='forja', dono='eu')); com_jogo = vf()
    im = nasce(item('ferramenta', 2, forma='martelo', dono='eu')); com_martelo = vf()
    ic = nasce(item('ferramenta', 4, oficio='couro', dono='eu')); couro_na_forja = vf(); couro_no_couro = oficio.valor_ferramentas(E, 'eu', 'couro')
    at = dict(E['gente']['eu']['atributos']); estado.aplica(E, 'gera', [['pessoa', 'nasce', 'zeca', dict(nome='Zeca', nivel=1, atributos=at, lugar='vila')]], onde='vila', texto='outro ferreiro')
    nasce(item('ferramenta', 5, forma='tenaz', dono='zeca')); de_outro = vf()
    estado.aplica(E, 'mestre', [['item', im, 'dur', 'soma', -100]], texto='o martelo quebra'); quebrado = vf()
    estado.aplica(E, 'mestre', [['item', im, 'dur', 'soma', 100], ['item', im, 'efeito', 'junta', {'chave': 'afinada'}]], texto='o martelo conserta e afina'); afinado = vf()
    ok['lugares'] = (sem, com_jogo, com_martelo, couro_na_forja, couro_no_couro, de_outro, quebrado, afinado) == ((0, 0, None), (VM[0], VT[0], 0), (VM[2], VT[0], 2), (VM[2], VT[0], 2), (VM[4], VT[4], 4), (VM[2], VT[0], 2), (VM[0], VT[0], 0), (VM[2] + VA, VT[0], 2))
    c = oficio.valor(E, 'eu', 1); ok['soma'] = c['mais'] == c['maestria'] + c['oficina'] + c['preparo'] + c['materia'] + c['nucleo'] + c['martelo'] + c['tenaz'] and c['martelo'] == VM[2] + VA and f"martelo de forja {VM[2] + VA}" in oficio.diz_valor(c)
    aj = oficio.conta(E, 'eu', 1, contra=O.ajuste_contra(1)); ok['ajuste'] = aj['ferramenta'] == VM[2] + VA + VT[0]                       # o ajuste (teste de passar) também soma as ferramentas
    for k in (ij, im, ic): estado.aplica(E, 'mestre', [['item', k, 'some']], texto='tira a ferramenta da prova')
    pm = oficio.molde('ferramenta', 1, oficio='martelo'); pt = oficio.molde('ferramenta', 1, oficio='tenaz'); pj = oficio.molde('ferramenta', 1, oficio='forja')
    ok['materia'] = (oficio.materia_de(pm), oficio.materia_de(pt), oficio.materia_de(pj)) == ({M.materia('metal', 1): 2, M.materia('madeira', 1): 1}, {M.materia('metal', 1): 1, M.materia('madeira', 1): 1}, {M.materia('metal', 1): 3, M.materia('madeira', 1): 2})
    F, it = obra(1, 0, pm); ok['forja_martelo'] = it['tipo'] == 'ferramenta' and it['forma'] == 'martelo' and it['nome'] == 'martelo de forja Incomum' and it['cat'] == 1
    F, it2 = obra(1, 0, pt); ok['forja_tenaz'] = it2['forma'] == 'tenaz' and it2['nome'] == 'tenaz Incomum'
    for x in (it, it2): estado.aplica(E, 'mestre', [['item', x['id'], 'some']], texto='tira')
    ok['recusa_forma'] = bool(recusa(lambda: oficio.molde('ferramenta', 1, oficio='alquimia')))
    real = teste.rola                                                                                                                   # os efeitos que os dados dão: um 20 que abre, e o quase
    def faces(a, b):
        def rola(E_, o_que, atributo, contra, mais=0, quem=None, oculto=False, dom=0, rotulo=None):
            r = real(E_, o_que, atributo, contra, mais=mais, quem=quem, oculto=oculto, dom=dom); r['dados'] = [a, b]; r['total'] = sum(a) + sum(b) + r['bonus'] + r['pena'] + mais + dom; r['passou'] = r['total'] >= contra; return r
        return rola
    try:
        teste.rola = faces([20, 9], [12]); pv = espada(2); nv = entrega(E, pv); Rv = oficio.forjar(E, 'eu', pv, blocos=0, nucleo=nv)
        estado.aplica(E, 'mestre', [['obra', Rv['obra'], 'blocos', 'poe', O.blocos(2)]], texto='os blocos da prova'); Fv = oficio.remata(E, Rv['obra']); itv = L().get(Fv['item']) if Fv['item'] else None
        vinte = itv.get('efeitos_livres', 0) if itv else None
    finally: teste.rola = real
    ok['vinte'] = vinte is not None and vinte >= 1
    F, arma = obra(2, 0); aid = F['item']; estado.aplica(E, 'mestre', [['item', aid, 'efeitos_livres', 'poe', 2]], texto='a obra-prima de prova')
    r_pesa = recusa(lambda: oficio.efeito(E, 'eu', aid, 'pesa')); r_nao = recusa(lambda: oficio.efeito(E, 'eu', aid, 'firme'))
    oficio.efeito(E, 'eu', aid, 'critico_19'); r_dup = recusa(lambda: oficio.efeito(E, 'eu', aid, 'critico_19'))
    oficio.efeito(E, 'eu', aid, 'sangra'); r_fim = recusa(lambda: oficio.efeito(E, 'eu', aid, 'derruba'))
    a = L()[aid]; ok['efeito_arma'] = bool(r_pesa and r_nao and r_dup and r_fim) and [e['chave'] for e in a['efeitos']] == ['critico_19', 'sangra'] and 'efeitos_livres' not in a
    arm = oficio.molde('armadura', 2, material='malha'); F, armadura = obra(2, 0, arm); vid = F['item']; estado.aplica(E, 'mestre', [['item', vid, 'efeitos_livres', 'poe', 1]], texto='a obra-prima de prova')
    r_dev = recusa(lambda: oficio.efeito(E, 'eu', vid, 'devolve', valor=T.devolve_max(2) + 1)); oficio.efeito(E, 'eu', vid, 'devolve')
    ok['efeito_devolve'] = bool(r_dev) and L()[vid]['efeitos'] == [{'chave': 'devolve', 'valor': T.devolve_max(2)}]
    F, outra = obra(0, 0); oid2 = F['item']; estado.aplica(E, 'mestre', [['item', oid2, 'efeitos_livres', 'poe', 1], ['item', oid2, 'dono', 'poe', 'zeca']], texto='a peça muda de dono')
    ok['efeito_dono'] = bool(recusa(lambda: oficio.efeito(E, 'eu', oid2, 'leve')))
    ok['estado'] = not estado.valida(E) and oficio.prata_do_mundo(E) == p0
    falhas = [k for k, v in ok.items() if not v]
    return [('O MARTELO DE FORJA, A TENAZ E OS EFEITOS (a Lei do Valor; o dado posto à mão)',
             f"{sum(ok.values())} de {len(ok)} conferências certas" + (f"; falham: {', '.join(falhas)}" if falhas else '') + f" · (martelo, tenaz, categoria) sem / jogo Comum / martelo Raro / couro na forja / no couro / de outro / quebrado / afinado = {(sem, com_jogo, com_martelo, couro_na_forja, couro_no_couro, de_outro, quebrado, afinado)}",
             not falhas)]


def provas(n=300):
    out = []; m = max(400, 2 * n)
    def roda(nome, f):
        try: out.extend(f())
        except (SystemExit, Exception) as e: out.append((nome or 'PROVA DO OFÍCIO', f'A PROVA QUEBROU: {type(e).__name__}: {e}', False))
    cheias = max(20, n // 10); curtas = max(20, n // 15)
    roda('A ESCADA E O ROBÔ FERREIRO', lambda: escada([vida(s + 1) for s in range(cheias)] + [vida(cheias + s + 1, dias=ROBO['curta'], ate=4) for s in range(curtas)]))
    roda('AS METAS DA LEI DO VALOR', lambda: _valor_metas(n))
    for nome, f in (('A CONTA FECHA', lambda: [_conta_fecha(n)]), ('AS MARGENS', lambda: [_margens(n)]), ('A OBRA ABERTA', lambda: [_obra_aberta(n)]),
                    ('O CONSERTO', lambda: [_conserto(n)]), ('SOB MEDIDA', lambda: [_sob_medida(n)]), ('A MAESTRIA', lambda: [_maestria(n)]), ('AS RECUSAS', lambda: [_recusas(n)])):
        roda(nome, f)
    for nome, f in (('AS FERRAMENTAS E A OBRA-PRIMA', lambda: _ferramentas(n)),):
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
