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

A PARTE 2, FASE 1a (projeto/etapa_efeitos/DESENHO.md, seções 5 e 10): as metas B2 (a categoria não muda: o motor novo contra a regra de antes, copiada aqui) e FJ1 a FJ10
(a faixa pela conta exata e as tabelas de 5.6; o dado de verdade; a monotonia; o teto; o teto de efeitos e o cheio; a escolha; as ferramentas; a loja com o poupa-ferro;
o dom escondido pela faixa; a mesa). Só elas: `python3 provas_oficio.py faixa [N]`.
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
            if (oficio.valor_ferramentas(E, 'eu')[2] or -1) < alvo:                         # a Lei do Valor: o martelo e a tenaz da categoria que ele mira, entregues como a matéria e o núcleo
                estado.aplica(E, 'gera', [['item', 'nasce', item('ferramenta', alvo, forma=f_, dono='eu')] for f_ in ('martelo', 'tenaz')], onde='vila', texto='as ferramentas do robô'); V['ferramentas'] = V.get('ferramentas', 0) + 2
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
        deu += (f". COM QUE ISTO VALE: na {O.OFICINAS[ROBO['nivel']]} (+{ROBO['nivel']}), com os quatro preparos (+{O.PREPARO_MAX}) desde o Dia 1, e com matéria" + (' e núcleo novos' if O.pede_nucleo(cat) else ' nova') + f" a cada obra, e com o martelo de forja e a tenaz da categoria (a Lei do Valor): {tent / n:.1f} {o_que} por vida (a pior vida: {pior})"
                + (f". COM UM NÚCLEO SÓ, a peça nasce em {sum(prim) / len(prim):.0%} das vidas; nas outras, o núcleo se gastou ou se perdeu" if prim and O.pede_nucleo(cat) else ''))
        fechos[cat] = f
        if cat in PELA_OBRA:    # a Lendária julga DUAS coisas: a primeira TENTATIVA (o dia em que a primeira obra fecha), e a peça RARA DE PROPÓSITO (nasce em pelo menos uma vida e em menos da metade)
            lo, hi = RARA_DE_PROPOSITO; rara = lo <= len(tem) < n * hi
            deu = (f"a primeira obra {oficio.FEM[cat]} fecha no Dia {f}" if f is not None else f"a primeira obra {oficio.FEM[cat]} NÃO FECHA na metade das {n} vidas até o Dia {ate}")
            deu += f"; a peça nasceu em {len(tem)} de {n} vidas até o Dia {ate}" + (f", entre o Dia {min(tem)} e o {max(tem)}" if tem else '') + (f" (a faixa: de {lo} a menos de {n * hi:g})" if rara else f" (FORA DA FAIXA: de {lo} a menos de {n * hi:g})")
            if prim: deu += f"; acerta de primeira em {sum(prim) / len(prim):.0%} das vidas ({tent / n:.1f} obras por vida)"
            deu += (f". COM QUE ISTO VALE: na {O.OFICINAS[ROBO['nivel']]} (+{ROBO['nivel']}), com os quatro preparos (+{O.PREPARO_MAX}) desde o Dia 1, e com matéria e núcleo novos a cada obra, e com o martelo de forja e a tenaz da categoria (a Lei do Valor): {tent / n:.1f} {o_que} por vida (a pior vida: {pior})"
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
        estado.aplica(E, 'mestre', [['obra', oid, 'blocos', 'poe', O.blocos(3)]], texto='os blocos da prova')
        if i % 10 == 0:                                                                     # a Lei do Valor: com núcleo, só os dois 1 perdem a obra; numa obra em dez, eles são postos
            real = teste.rola
            def dois_um(E_, o_que, atributo, contra, mais=0, quem=None, oculto=False, dom=0, rotulo=None):
                r = real(E_, o_que, atributo, contra, mais=mais, quem=quem, oculto=oculto, dom=dom); r['dados'] = [[1], [1]]; r['total'] = 2 + r['bonus'] + r['pena'] + mais + dom; r['passou'] = r['total'] >= contra; return r
            teste.rola = dois_um
            try: F = oficio.remata(E, oid)
            finally: teste.rola = real
        else: F = oficio.remata(E, oid)
        vistos[F['fim']] += 1
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
    Rs = lambda tot, a, b, te, fc: oficio._resolve(tot, a, b, te, fc)[0][1]                                                                  # os dados especiais, com as faces postas (sem 1d6)
    ok['dois_1'] = Rs(CD[2] + 5, 1, 1, 2, -1)['cat'] is None and Rs(CD[2] + 5, 1, 1, 2, 2)['cat'] is None and Rs(CD[2] + 5, 1, 1, 2, 3)['cat'] == 0 and Rs(CD[2] + 5, 1, 1, 2, 3)['tosca']
    ok['um_1'] = Rs(CD[2] + 1, 1, 9, 2, -1)['cat'] == 1 and Rs(CD[1] + 1, 9, 1, 2, -1)['cat'] == 0 and Rs(CD[0] + 1, 1, 9, 2, -1)['cat'] == 0 and Rs(CD[0] + 1, 1, 9, 2, -1)['tosca'] and Rs(CD[0] - 1, 1, 9, 2, -1)['cat'] is None
    ok['dois_20'] = Rs(CD[1] + 1, 20, 20, 2, -1)['cat'] == 2 and Rs(CD[1] + 1, 20, 20, 2, -1)['sobe'] and Rs(CD[2] + 1, 20, 20, 2, -1)['cat'] == 2 and Rs(CD[2] + 1, 20, 20, 2, -1)['mais_efeito'] == 1
    ok['quase'] = Rs(CD[2] - 1, 5, 9, 2, 4)['quase'] and not Rs(CD[2] - 1, 5, 9, 2, 3)['quase'] and not Rs(CD[2] - 1 - O.QUASE_JANELA, 5, 9, 2, 4)['quase'] and not Rs(CD[1] + 30, 5, 9, 1, 4)['quase']
    ok['poder'] = Rs(CD[0] - 3, 5, 9, 2, 2)['cat'] == 0 and Rs(CD[0] - 6, 5, 9, 2, 2)['cat'] is None and Rs(CD[0] - 30, 5, 9, 2, 3)['cat'] == 0 and Rs(CD[0] - 30, 5, 9, 2, -1)['cat'] is None
    ok['como'] = all(Rs(t_, a_, b_, 2, -1)['como'] for t_, a_, b_ in ((CD[0] - 9, 1, 1), (CD[0] - 9, 5, 9), (CD[1] + 1, 1, 9), (CD[1] + 1, 20, 20)))
    ok['porta'] = O.teto(0, 2) == 0 and O.teto(1, 2) == 1 and O.teto(0, 4) == 1 and O.teto(1, 4) == 2 and O.teto(2, 8) == 2 and O.teto(3, 2) == 3 and O.teto(3, 8, 5) == 4 and O.teto(5, 8, 5) == 5 and O.teto(2, 8, 5) == 2
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
    estado.aplica(E, 'gera', [['item', 'nasce', item('ferramenta', 3, forma=f_, dono='eu')] for f_ in ('martelo', 'tenaz')], onde='vila', texto='o martelo e a tenaz Épicos da prova')     # a Lei do Valor: sem ferramenta, a Épica sai uma vez em quinze
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
    pm = oficio.molde('ferramenta', 1, oficio='martelo'); pt = oficio.molde('ferramenta', 1, oficio='tenaz'); pj = oficio.molde('ferramenta', 1, oficio='forja'); pj0 = oficio.molde('ferramenta', 0, oficio='forja')
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
    # (a parte 2, fase 1a) SÓ A FERRAMENTA ESCOLHE AGORA: a arma e a armadura guardam os efeitos por escolher, e a mesa diz que o catálogo de luta chega na próxima fase
    F, arma = obra(2, 0); aid = F['item']; estado.aplica(E, 'mestre', [['item', aid, 'efeitos_livres', 'poe', 2]], texto='os efeitos de prova')
    r_arma = recusa(lambda: oficio.efeito(E, 'eu', aid, 'critico_19')) or ''; a = L()[aid]
    ok['efeito_arma'] = 'o catálogo de luta chega na próxima fase' in r_arma and not a.get('efeitos') and a.get('efeitos_livres') == 2
    arm = oficio.molde('armadura', 2, material='malha'); F, armadura = obra(2, 0, arm); vid = F['item']; estado.aplica(E, 'mestre', [['item', vid, 'efeitos_livres', 'poe', 1]], texto='os efeitos de prova')
    ok['efeito_armadura'] = 'o catálogo de luta chega na próxima fase' in (recusa(lambda: oficio.efeito(E, 'eu', vid, 'devolve')) or '') and not L()[vid].get('efeitos')
    F, tz = obra(1, 0, pt); tid = F['item']; estado.aplica(E, 'mestre', [['item', tid, 'efeitos_livres', 'poe', 2]], texto='os efeitos de prova')
    r_pesa = recusa(lambda: oficio.efeito(E, 'eu', tid, 'pesa')); r_forte = recusa(lambda: oficio.efeito(E, 'eu', tid, 'lastro'))
    oficio.efeito(E, 'eu', tid, 'prumo'); r_dup = recusa(lambda: oficio.efeito(E, 'eu', tid, 'prumo'))
    oficio.efeito(E, 'eu', tid, 'afinada'); r_fim = recusa(lambda: oficio.efeito(E, 'eu', tid, 'fagulha'))
    t_ = L()[tid]; ok['efeito_ferramenta'] = bool(r_pesa and r_forte and r_dup and r_fim) and [e['chave'] for e in t_['efeitos']] == ['prumo', 'afinada'] and 'efeitos_livres' not in t_
    F, outra = obra(0, 0, pj0); oid2 = F['item']; estado.aplica(E, 'mestre', [['item', oid2, 'efeitos_livres', 'poe', 1], ['item', oid2, 'dono', 'poe', 'zeca']], texto='a peça muda de dono')
    ok['efeito_dono'] = bool(recusa(lambda: oficio.efeito(E, 'eu', oid2, 'afinada')))
    ok['estado'] = not estado.valida(E) and oficio.prata_do_mundo(E) == p0
    falhas = [k for k, v in ok.items() if not v]
    return [('O MARTELO DE FORJA, A TENAZ E OS EFEITOS (a Lei do Valor; o dado posto à mão; na fase 1a, só a ferramenta escolhe: a arma e a armadura guardam os efeitos)',
             f"{sum(ok.values())} de {len(ok)} conferências certas" + (f"; falham: {', '.join(falhas)}" if falhas else '') + f" · (martelo, tenaz, categoria) sem / jogo Comum / martelo Raro / couro na forja / no couro / de outro / quebrado / afinado = {(sem, com_jogo, com_martelo, couro_na_forja, couro_no_couro, de_outro, quebrado, afinado)}",
             not falhas)]


# ---------- A PARTE 2, FASE 1a: A FAIXA DA FORJA E AS FERRAMENTAS (o contrato: projeto/etapa_efeitos/DESENHO.md, seções 5 e 10; as metas B2 e FJ1 a FJ10) ----------
# As contas exatas saem do oficio.dist_efeitos (o mesmo dado do dist_valor, agrupado); as medidas com o dado de verdade, do remate de verdade. O dado posto à mão só onde se diz.
REF = (('Ferord, matéria Comum', 23, 1, 1, 0), ('Ferord, a tenaz (matéria Incomum)', 38, 2, 1, 1), ('um Mestre, matéria Rara', 65, 2, 2, 2), ('o Mestre, núcleo Épico', 80, 3, 2, 3),
       ('o melhor possível, núcleo Lendário', 127, 5, 5, 5))         # (quem, a soma, o teto, a maior ferramenta, a categoria da obra): os cinco ferreiros do contrato (5.6, 5.8)
INICIANTE = ('um Iniciante, matéria Comum (a porta)', 8, 0, -1, 0)
ABAIXO = (('o Mestre, matéria Comum', 35, 1, 2, 0, 3), ('o melhor, matéria Comum', 52, 1, 5, 0, 4), ('o melhor, matéria Rara sem núcleo', 82, 2, 5, 2, 4))     # (..., o índice em REF da obra da mão dele)
# AS CONTAS DE 5.6 COMO O CONTRATO AS PUBLICOU (% por obra; cheios por 100 obras), para conferir célula por célula (a folga: o arredondamento da tabela e o corte do dado)
TABELA_56 = {(23, 1, 1): {0: (84.6, (26.0, 34.2, 24.4, 0, 0, 0), 19.1), 1: (15.1, (7.0, 3.1, 2.9, 1.4, 0.4, 0.2), 0)},
             (38, 2, 1): {0: (32.2, (2.0, 6.9, 23.4, 0, 0, 0), 23.8), 1: (63.0, (35.5, 19.1, 4.5, 1.7, 2.1, 0), 0.9), 2: (4.5, (0, 2.9, 0.9, 0.2, 0.3, 0.2), 0)}}
OUTROS_56 = ((8, 0, -1, 0.28, 23, 'das peças'), (65, 2, 2, 1.24, 62, 'por obra'), (80, 3, 2, 1.47, 70, 'por obra'), (127, 5, 5, 1.60, 70, 'por obra'), (82, 2, 5, 1.84, 96, 'por obra'), (52, 1, 5, 1.54, 86, 'por obra'))
FOLGA_56 = 0.1              # pontos de % (a tabela arredonda a 0,1; o dado do motor corta a cadeia de 20 em 4 voltas, o do rascunho em 8)
# AS DUAS RÉGUAS DA PERGUNTA 1 (DESENHO 12): a FJ1 confere a que está em vigor no tabelas_oficio.REGUA_FAIXA. As faixas gerais da FJ1 (de 55 a 75% com efeito, de 0,8 a 1,7 por obra,
# a colada de 8 a 25%) e as tabelas de 5.6 são da régua (a). Da (b) o contrato só dá a tenaz de Ferord (12, pergunta 1 (b)): a Incomum em 63% (sem efeito 51,2 · 1 efeito 7,4 ·
# 2 efeitos 2,3 · 3 ou 4 efeitos 2,1), a Comum em 32% com 1 ou 2 efeitos em 83% delas, a Rara em 4,5% sempre com efeito, 0,7 efeito por obra. O que não depende da régua
# (abaixo da mão no máximo 1,2 vez, a colada do Iniciante 0, a Lendária do melhor em 25,4%) vale nas duas.
REGUA_A = ((2, 4), (5, 3), (8, 2), (16, 1))
REGUA_B = ((1, 4), (3, 3), (5, 2), (10, 1))
TENAZ_B = dict(inc=63.0, inc_ef=(51.2, 7.4, 2.3, 2.1), comum=32.2, comum_12=0.83, rara=4.5, por_obra=0.7)      # (% por obra; o 2,1 junta os 3 e os 4; a Comum: a fração delas com 1 ou 2)


def _cat_hoje(total, a0, b0, teto, fc):
    """A REGRA DE ANTES DA FASE 1a, copiada aqui como estava no oficio._resolve (só a categoria): é a régua da meta B2. Não se mexe nela."""
    k = O.cat_do_total(total, teto); cat = k
    if a0 == 1 and b0 == 1: return 0 if fc >= O.NADA_SE_PERDE else None
    if a0 == 1 or b0 == 1:
        if k is not None and k > 0: cat = k - 1
    elif a0 == 20 and b0 == 20 and k is not None and k < teto: cat = k + 1
    if cat is None and (fc >= O.NADA_SE_PERDE or (fc >= 2 and total >= O.VALOR_CD[0] - O.VALOR_SEGURA)): cat = 0
    return cat


def _dist_hoje(soma, teto, fc=-1):
    """o oficio.dist_valor de antes da fase 1a, copiado aqui (os mesmos laços, o mesmo dado)"""
    res = {}
    for a0 in range(1, 21):
        da = {a0: 1.0} if a0 < 20 else {20 + x: q for x, q in oficio._UM.items()}
        for b0 in range(1, 21):
            db = {b0: 1.0} if b0 < 20 else {20 + x: q for x, q in oficio._UM.items()}
            for va, pa in da.items():
                for vb, pb in db.items():
                    c = _cat_hoje(va + vb + soma, a0, b0, teto, fc); res[c] = res.get(c, 0) + pa * pb / 400
    return res


def _marg(d):
    m = {}
    for k, q in d.items(): m[k[0]] = m.get(k[0], 0) + q
    return m


def _dif(a, b): return max(abs(a.get(c, 0) - b.get(c, 0)) for c in set(a) | set(b))


def _b2(n):
    """B2 A CATEGORIA NÃO MUDA: a chance de cada categoria do motor novo (o dist_valor e o dist_efeitos) contra a regra de antes, soma de −10 a 200 (de 3 em 3), teto 0 a 5,
    sem ferramenta e com cada uma (2.982 casos); e com os efeitos de ferramenta ligados (o prumo de 1 a 5, o lastro, a fagulha, a têmpera, o molde). A afinada é a de antes (+1)."""
    pior = 0.0; casos = 0
    for soma in range(-10, 201, 3):
        for teto in range(6):
            for fc in (-1, 0, 1, 2, 3, 4, 5):
                h = _dist_hoje(soma, teto, fc); pior = max(pior, _dif(oficio.dist_valor(soma, teto, fc), h), _dif(_marg(oficio.dist_efeitos(soma, teto, fc)), h)); casos += 1
    pior2 = 0.0; casos2 = 0
    ligados = [dict(prumo=p) for p in range(1, 6)] + [dict(lastro=True), dict(fagulha=True)] + [dict(tempera=t) for t in (1, 2, 3)] + [dict(prumo=5, lastro=True, fagulha=True, tempera=3, molde_cat=0)]
    for soma in range(-10, 201, 15):
        for teto in range(6):
            h = {fc: _dist_hoje(soma, teto, fc) for fc in (2, 4, 5)}
            for i, kw in enumerate(ligados):
                fc = (2, 4, 5)[i % 3]; pior2 = max(pior2, _dif(_marg(oficio.dist_efeitos(soma, teto, fc, **kw)), h[fc])); casos2 += 1
    return [('B2 A CATEGORIA NÃO MUDA: a chance de cada categoria pelo motor novo (o dist_valor e a conta dos efeitos) contra a regra de antes, soma de −10 a 200, teto 0 a 5, sem ferramenta e com cada uma, e com os efeitos de ferramenta ligados (prumo, lastro, fagulha, têmpera, molde): diferença até 1e−12, sem exceção',
             f"{casos} casos: a maior diferença {pior:.1e}; com os efeitos de ferramenta ligados, mais {casos2} casos: {pior2:.1e}", pior <= 1e-12 and pior2 <= 1e-12)]


def _resumo(s, t, fc, **kw): return oficio.resumo_efeitos(oficio.dist_efeitos(s, t, fc, detalhe=True, **kw))


def _fj1(n):
    """FJ1 A FAIXA, PELA CONTA EXATA: os cinco ferreiros na obra da mão, o Iniciante, e o Mestre e o melhor abaixo da mão; e as tabelas de 5.6, célula por célula (pela régua em
    vigor: a (a) com as faixas e as tabelas do contrato; a (b) com a tenaz que o contrato dá para ela)"""
    if tuple(O.REGUA_FAIXA) == REGUA_B: return _fj1_b(n)
    if tuple(O.REGUA_FAIXA) != REGUA_A: return [('FJ1 A FAIXA', f'a régua em vigor ({O.REGUA_FAIXA}) não é nem a (a) nem a (b) do contrato: o banco não tem a referência dela', False)]
    out = []; R = {nome: _resumo(s, t, fc) for nome, s, t, fc, oc in REF + (INICIANTE,)}
    mao = [R[x[0]] for x in REF]; ini = R[INICIANTE[0]]; ten = R[REF[1][0]]
    inc34 = sum(q for e, q in ten['cat'][1]['ef'].items() if e in (3, 4))
    ok = (all(0.55 <= r['com'] <= 0.75 and 0.8 <= r['efeitos'] <= 1.7 and 0.08 <= r['colada'] <= 0.25 for r in mao) and 0.10 <= ini['com'] <= 0.30 and ini['colada'] == 0 and 0.02 <= inc34 <= 0.06)
    txt = ' · '.join(f"{x[0]} (2d20+{x[1]}): {R[x[0]]['efeitos']:.2f} efeito por obra, obra com efeito {R[x[0]]['com']:.1%}, colada {R[x[0]]['colada']:.1%}" for x in REF + (INICIANTE,))
    out.append(('FJ1 A FAIXA, PELA CONTA EXATA: na obra da mão, Treinado ou melhor, a obra com efeito de 55 a 75% e de 0,8 a 1,7 efeito por obra; o Iniciante, de 10 a 30%; a colada de 8 a 25% (a do Iniciante, 0); na tenaz de Ferord, a Incomum de 3 ou 4 efeitos de 2 a 6%',
                txt + f"; na tenaz de Ferord, a Incomum de 3 ou 4 efeitos em {inc34:.1%} das obras", ok))
    razoes = []
    for nome, s, t, fc, oc, i in ABAIXO:
        r = _resumo(s, t, fc); razoes.append((nome, s, r['efeitos'], r['efeitos'] / R[REF[i][0]]['efeitos'], REF[i][0]))
    out.append(('FJ1 ABAIXO DA MÃO NÃO É MINA: o Mestre e o melhor com matéria abaixo da mão tiram no máximo 1,2 vez os efeitos por obra da obra da mão deles (medido de 0,76 a 1,15 vez)',
                ' · '.join(f"{nome} (2d20+{s}): {ef:.2f} por obra, {rz:.2f} vez a de {mao_}" for nome, s, ef, rz, mao_ in razoes), all(rz <= 1.2 for *_, rz, _m in razoes)))
    pior = 0.0; ruins = []                                                 # as tabelas de 5.6, célula por célula
    for (s, t, fc), tab in TABELA_56.items():
        r = _resumo(s, t, fc)
        for k, (ch, efs, cheios) in tab.items():
            c = r['cat'].get(k, dict(chance=0, ef={}, cheios=0)); mine = [c['ef'].get(e, 0) * 100 for e in range(5)] + [sum(q for e, q in c['ef'].items() if e >= 5) * 100]
            for nome_, a, b in [('chance', c['chance'] * 100, ch), ('cheios', c['cheios'] * 100, cheios)] + [(f'{e} ef', mine[e], efs[e]) for e in range(6)]:
                d = abs(a - b); pior = max(pior, d)
                if d > FOLGA_56 + 1e-9: ruins.append(f"2d20+{s} {oficio.FEM[k]} {nome_}: {a:.2f} (o contrato diz {b})")
    for s, t, fc, efo, com, como in OUTROS_56:
        r = _resumo(s, t, fc); c = r['com_peca'] if como == 'das peças' else r['com']
        if abs(r['efeitos'] - efo) > 0.006: ruins.append(f"2d20+{s}: {r['efeitos']:.3f} efeito por obra (o contrato diz {efo})")
        if abs(c * 100 - com) > 0.6: ruins.append(f"2d20+{s}: {c:.1%} com efeito {como} (o contrato diz {com}%)")
    lend = _resumo(127, 5, 5)['cat'][5]['chance']
    if abs(lend - 0.254) > 0.0006: ruins.append(f'a Lendária do melhor: {lend:.2%} (o contrato diz 25,4%)')
    out.append(('FJ1 AS CONTAS EXATAS DE 5.6 BATEM: as duas tabelas de Ferord (matéria Comum e a tenaz), célula por célula, e os outros perfis (efeitos por obra, obra com efeito, a Lendária do melhor em 25,4%)',
                f"{sum(len(tab) * 8 for tab in TABELA_56.values()) + 2 * len(OUTROS_56) + 1} conferências; a maior diferença numa célula {pior:.2f} ponto (folga {FOLGA_56})" + (f"; FORA: {'; '.join(ruins[:4])}" if ruins else ''), not ruins))
    return out


def _fj1_b(n):
    """FJ1 COM A RÉGUA (b) (a pergunta 1 (b) do contrato): a tenaz de Ferord pelos números que o contrato dá para a (b), e o que não depende da régua (abaixo da mão, o Iniciante,
    a Lendária do melhor). As faixas gerais de 10 (FJ1) e as tabelas de 5.6 são da régua (a): com a (b), o Mestre as recalibra."""
    out = []; ten = _resumo(38, 2, 1); ruins = []
    inc = ten['cat'].get(1, dict(chance=0, ef={})); com_ = ten['cat'].get(0, dict(chance=0, ef={})); rar = ten['cat'].get(2, dict(chance=0, ef={}))
    meus = [inc['ef'].get(0, 0) * 100, inc['ef'].get(1, 0) * 100, inc['ef'].get(2, 0) * 100, (inc['ef'].get(3, 0) + inc['ef'].get(4, 0)) * 100]
    for nome_, a, b, folga in ([('Incomum', inc['chance'] * 100, TENAZ_B['inc'], FOLGA_56), ('Comum', com_['chance'] * 100, TENAZ_B['comum'], FOLGA_56), ('Rara', rar['chance'] * 100, TENAZ_B['rara'], FOLGA_56)]
                               + [(f'Incomum {r}', meus[i], TENAZ_B['inc_ef'][i], FOLGA_56) for i, r in enumerate(('sem efeito', '1 efeito', '2 efeitos', '3 ou 4 efeitos'))]
                               + [('a Comum com 1 ou 2 efeitos (fração)', (com_['ef'].get(1, 0) + com_['ef'].get(2, 0)) / com_['chance'] * 100 if com_['chance'] else 0, TENAZ_B['comum_12'] * 100, 0.6),
                                  ('a Rara sem efeito', rar['ef'].get(0, 0) * 100, 0, FOLGA_56), ('efeito por obra (×100)', ten['efeitos'] * 100, TENAZ_B['por_obra'] * 100, 5.0)]):
        if abs(a - b) > folga + 1e-9: ruins.append(f"{nome_}: {a:.2f} (o contrato diz {b})")
    out.append(('FJ1 A FAIXA, PELA CONTA EXATA, COM A RÉGUA (b): a tenaz de Ferord pelos números que o contrato dá para a (b) (a Incomum em 63%: sem efeito 51,2 · 1 efeito 7,4 · 2 efeitos 2,3 · 3 ou 4 efeitos 2,1; a Comum com 1 ou 2 efeitos em 83% delas; a Rara sempre com efeito; 0,7 efeito por obra). As faixas gerais da FJ1 e as tabelas de 5.6 são da (a): com a (b), o Mestre as recalibra',
                f"a tenaz: {ten['efeitos']:.2f} efeito por obra, obra com efeito {ten['com']:.1%}; Incomum {inc['chance']:.1%} ({', '.join(f'{x:.1f}' for x in meus)})" + (f"; FORA: {'; '.join(ruins)}" if ruins else ''), not ruins))
    R = {x[0]: _resumo(x[1], x[2], x[3]) for x in REF}; ini = _resumo(*INICIANTE[1:4]); razoes = []
    for nome, s, t, fc, oc, i in ABAIXO:
        r = _resumo(s, t, fc); razoes.append((nome, s, r['efeitos'], r['efeitos'] / R[REF[i][0]]['efeitos'], REF[i][0]))
    lend = _resumo(127, 5, 5)['cat'][5]['chance']
    out.append(('FJ1 ABAIXO DA MÃO NÃO É MINA (e o que não depende da régua): o Mestre e o melhor com matéria abaixo da mão tiram no máximo 1,2 vez os efeitos por obra da obra da mão deles; a colada do Iniciante é 0; a Lendária do melhor segue em 25,4%',
                ' · '.join(f"{nome} (2d20+{s}): {ef:.2f} por obra, {rz:.2f} vez a de {mao_}" for nome, s, ef, rz, mao_ in razoes) + f"; a colada do Iniciante {ini['colada']:.1%}; a Lendária do melhor {lend:.1%}",
                all(rz <= 1.2 for *_, rz, _m in razoes) and ini['colada'] == 0 and abs(lend - 0.254) <= 0.0006))
    return out


def ferord(semente=1, prata=300):
    """FERORD HOJE (o contrato, 5.6): Treinado na forja, Afinidade 75, forja de vila, preparo +6 até o Incomum (a receita, o fogo e a bigorna), o martelo de forja Incomum e o jogo
    Comum afinado: 2d20 + 23 na matéria Comum, 2d20 + 38 na Incomum"""
    E = oficina_de_prova(semente, nivel=1, afinidade=75, mao=4, prata=prata, fogo=1, bigorna=1, receita=1)
    estado.aplica(E, 'gera', [['item', 'nasce', item('ferramenta', 1, forma='martelo', dono='eu')], ['item', 'nasce', item('ferramenta', 0, oficio='forja', dono='eu', efeitos=[{'chave': 'afinada'}])]], onde='vila', texto='as ferramentas de Ferord')
    return E


@contextlib.contextmanager
def com_dados(a, b):
    """SÓ NA PROVA: o dado de verdade é rolado e anotado, mas as faces são postas à mão (as listas da cadeia de cada d20: [20, 6] é um 20 que rolou de novo e deu 6)"""
    real = teste.rola
    def rola(E_, o_que, atributo, contra, mais=0, quem=None, oculto=False, dom=0, rotulo=None):
        r = real(E_, o_que, atributo, contra, mais=mais, quem=quem, oculto=oculto, dom=dom); r['dados'] = [list(a), list(b)]
        r['total'] = sum(a) + sum(b) + r['bonus'] + r['pena'] + mais + dom; r['passou'] = r['total'] >= contra
        if dom: r['fez'] = r['total'] >= contra and r['total'] - dom < contra
        return r
    teste.rola = rola
    try: yield
    finally: teste.rola = real


def obra_de(E, peca, a=None, b=None, quem='eu', molde=None):
    """a obra inteira, sem viver os dias: a matéria entregue, a obra aberta (molde=, se houver), os blocos postos, e o remate (com as faces postas, se a e b vêm)"""
    ef = [['pessoa', quem, 'carga.' + k, 'soma', q] for k, q in oficio.materia_da_obra(E, quem, peca).items()]
    estado.aplica(E, 'gera', ef, onde=E['gente'][quem]['lugar'], texto='a matéria de prova')
    R = oficio.forjar(E, quem, peca, blocos=0, molde=molde)
    estado.aplica(E, 'mestre', [['obra', R['obra'], 'blocos', 'poe', O.blocos(peca['cat'])]], texto='os blocos da prova')
    if a is None: return oficio.remata(E, R['obra'])
    with com_dados(a, b): return oficio.remata(E, R['obra'])


def tira(E, iid): estado.aplica(E, 'mestre', [['item', iid, 'some']], texto='a peça sai da prova')
def tenaz(cat=1): return oficio.molde('ferramenta', cat, oficio='tenaz')
def _com_efeito(it): return bool(it and ((it.get('efeitos_livres') or 0) + len(it.get('efeitos') or [])))


def _fj2(n):
    """FJ2 O DADO DE VERDADE: 400 obras da tenaz de Ferord com o teste.rola, obra por obra (a peça nova sai da prova a cada obra, para não mudar a soma)"""
    E = ferord(prata=100); esperado = oficio.efeitos_de(oficio.valor(E, 'eu', 1))['com']; m = max(400, n); vistos = 0; cats = {}
    for i in range(m):
        F = obra_de(E, tenaz()); it = E['itens']['itens'].get(F['item']) if F['item'] else None; vistos += _com_efeito(it); cats[F.get('sai')] = cats.get(F.get('sai'), 0) + 1
        if F['item']: tira(E, F['item'])
        E['_novos'].clear(); E['turno']['dados'].clear()
    saiu = ', '.join(('perde' if k is None else oficio.FEM[k]) + f' {v}' for k, v in sorted(cats.items(), key=lambda kv: -1 if kv[0] is None else kv[0]))
    return [('FJ2 O DADO DE VERDADE: a fração das obras da tenaz de Ferord que saem com efeito, em 400 obras com o teste.rola, bate com a conta exata (a da régua em vigor; com a (a), 62,3%) a 4 desvios',
             f"medido {vistos / m:.1%} em {m} obras ({saiu}); a conta exata {esperado:.1%}; o estado {'inteiro' if not estado.valida(E) else 'QUEBRADO'}",
             bate(vistos / m, esperado, m) and not estado.valida(E))]


def _ef_faixa(t, teto, fc, **kw):
    x = oficio._resolve(t, 10, 10, teto, fc, kw.get('prumo', 0), kw.get('lastro', False))[0][1]
    return x, oficio.conta_efeitos(x)


def _fj3(n):
    """FJ3 A MONOTONIA: todo total de toda faixa e teto, com e sem prumo e lastro (e a ferramenta Única): dentro da mesma categoria, mais soma nunca dá menos efeitos"""
    ruins = 0; casos = 0
    for teto in range(6):
        for k in range(teto + 1):
            for kw in (dict(), dict(prumo=1), dict(prumo=3), dict(prumo=5), dict(lastro=True), dict(prumo=2, lastro=True)):
                for fc in (-1, 4):
                    ant = -1; top = O.cd_de_cima(k) if k < teto else O.cd_de_cima(k) + 60
                    for t in range(O.VALOR_CD[k], top):
                        x, c = _ef_faixa(t, teto, fc, **kw); casos += 1
                        if x['cat'] != k: continue
                        if c['efeitos'] < ant: ruins += 1
                        ant = c['efeitos']
    return [('FJ3 A MONOTONIA: em todo total de toda faixa e teto, com e sem prumo e lastro (e com a ferramenta Única), mais soma nunca dá menos efeitos: zero inversões',
             f"{casos} totais: {ruins} inversões", ruins == 0 and casos >= 11000)]


def _fj4(n):
    """FJ4 O TETO: todo total na categoria do teto, em cada teto, com e sem prumo; o quase (a ferramenta Única) no teto"""
    passa2 = 0; acima = 0; acima_ruim = 0; quase_teto = 0; casos = 0
    for teto in range(6):
        for prumo in range(6):
            for t in range(O.VALOR_CD[teto], O.cd_de_cima(teto) + 80):
                for fc in (-1, 4, 5):
                    x = oficio._resolve(t, 10, 10, teto, fc, prumo)[0][1]; casos += 1
                    if x['k'] != teto: continue
                    passa2 += x['faixa'] > O.TETO_FAIXA
                    if t >= O.cd_de_cima(teto): acima += 1; acima_ruim += x['faixa'] != O.TETO_FAIXA
                    quase_teto += x['quase']
    return [('FJ4 O TETO: na categoria do teto a faixa nunca passa de 2, e o total acima da CD trancada dá sempre 2; o quase nunca age na categoria do teto',
             f"{casos} totais nos seis tetos (prumo 0 a 5, sem ferramenta, a Única e a Lendária): a faixa passou de 2 em {passa2}; acima da CD trancada, {acima} totais, {acima_ruim} fora do 2; o quase no teto: {quase_teto}",
             passa2 == 0 and acima > 0 and acima_ruim == 0 and quase_teto == 0)]


def _fj5(n):
    """FJ5 O TETO DE EFEITOS E O CHEIO: a conta (toda saída possível) e as peças nascidas e escolhidas"""
    ruins = []; casos = 0
    for teto in range(6):                                                  # (a) a conta, em toda saída: os totais, as faces (normal, um 1, dois 20, dois 1), os 20, as fagulhas, a têmpera, o molde
        for t in range(-10, 230, 2):
            for faces in ((9, 9), (1, 9), (20, 20), (1, 1)):
                x = oficio._resolve(t, faces[0], faces[1], teto, 5)[0][1]
                for n20 in range(4):
                    for n19 in range(3):
                        for tp in range(4):
                            for molde, mnum in ((False, False), (True, False), (True, True)):       # o molde de número leva o primeiro cheio (o cheio cabe nele: 5.4, passo 7)
                                c = oficio.conta_efeitos(x, n20, n19, True, tp, molde, mnum); casos += 1
                                if x['cat'] is None: continue
                                fora = c['teto'] - O.efeitos_max(x['cat'])
                                if c['efeitos'] > c['teto'] or fora != x['mais_efeito'] + c['molde'] or fora > 2 or c['cheios'] > c['livres'] + (1 if c['molde'] and mnum else 0) or c['cheios'] > c['sobra'] + tp: ruins.append((teto, t, faces, n20, n19, tp, molde, mnum))
    E = ferord(prata=100); nascidas = []
    for a, b, peca in (([9], [18], tenaz()), ([20, 6], [14], tenaz()), ([20, 4], [19], tenaz()), ([1], [18], tenaz()), ([20, 20, 5], [20, 3], tenaz()), ([5], [3], tenaz()),
                       ([20, 6], [14], oficio.molde('arma', 1, familia='espada')), ([17], [16], oficio.molde('ferramenta', 0, oficio='forja'))):
        F = obra_de(E, peca, a, b)
        if F['item']: nascidas.append(F['item'])
    L = lambda: E['itens']['itens']
    for i in nascidas:                                                     # (b) as peças nascidas, antes e depois de escolher (auto, na ferramenta)
        if oficio.escolhe_agora(L()[i]) and L()[i].get('efeitos_livres'): oficio.efeito(E, 'eu', i, 'auto')
    M = _ferreiro(nivel=4, afinidade=100, mao=8, prep=5, ferramentas=())    # o molde e a obra-prima no teto: o melhor, com o martelo Lendário de molde e a tenaz Única de prumo
    estado.aplica(M, 'gera', [['item', 'nasce', item('ferramenta', 5, forma='martelo', dono='eu', efeitos=[{'chave': 'molde'}, {'chave': 'tempera'}])],
                              ['item', 'nasce', item('ferramenta', 4, forma='tenaz', dono='eu', efeitos=[{'chave': 'prumo'}])]], onde='vila', texto='as ferramentas Lendárias de prova')
    F1 = obra_de(M, tenaz(1), [20, 20, 2], [20, 1], molde='prumo')          # o molde de prumo numa tenaz que sai Rara (o teto), com a obra-prima no teto: 2 fora do teto
    F2 = obra_de(M, tenaz(1), [1], [1], molde='prumo')                     # os dois 1: a ferramenta Épica ou maior segura (Comum, tosca, sem efeito): o molde se perde
    pecas = [L()[i] for i in nascidas] + [M['itens']['itens'][F['item']] for F in (F1, F2) if F['item']]
    for it in pecas:
        n_ = len(it.get('efeitos') or []) + (it.get('efeitos_livres') or 0); fora = it.get('teto_efeitos', O.efeitos_max(it['cat'])) - O.efeitos_max(it['cat'])
        if n_ > it.get('teto_efeitos', O.efeitos_max(it['cat'])) or fora > 2 or (it.get('cheios_livres') or 0) > (it.get('efeitos_livres') or 0): ruins.append(it['nome'])
        for e in it.get('efeitos') or []:
            if e.get('cheio') and not O.de_numero(e['chave']): ruins.append(f"{it['nome']}: cheio em {e['chave']}")
    m1 = M['itens']['itens'][F1['item']]; m2 = M['itens']['itens'][F2['item']] if F2['item'] else None
    molde_ok = (m1['cat'] == 2 and m1.get('teto_efeitos') == O.efeitos_max(2) + 2 and {'chave': 'prumo', 'cheio': True} in m1['efeitos'] and O.valor_ferramenta('prumo', 2, True) == O.valor_ferramenta('prumo', 3)
                and m2 is not None and not m2.get('efeitos') and not m2.get('efeitos_livres'))
    estado.aplica(E, 'gera', [['item', 'nasce', item('ferramenta', 1, forma='tenaz', dono='eu', efeitos_livres=4, cheios_livres=1, teto_efeitos=4)],        # a tenaz no fio que ainda tem os seus por escolher
                              ['item', 'nasce', item('ferramenta', 1, forma='tenaz', dono='eu', efeitos_livres=1, teto_efeitos=4)]], onde='vila', texto='duas tenazes com efeitos por escolher')   # e uma sem cheio
    il = f"i{E['itens']['seq'] - 1:04d}"; ic = f"i{E['itens']['seq']:04d}"
    estado.aplica(M, 'gera', [['item', 'nasce', item('ferramenta', 5, forma='tenaz', dono='eu', efeitos=[{'chave': 'molde'}])]], onde='vila', texto='a tenaz Lendária de molde'); im = f"i{M['itens']['seq']:04d}"
    junta = [recusa(lambda: estado.aplica(E, 'mestre', [['item', nascidas[1], 'efeito', 'junta', {'chave': 'sinete'}]], texto='a mais')),                   # passa do teto (a tenaz cheia)
             recusa(lambda: estado.aplica(E, 'mestre', [['item', nascidas[0], 'efeito', 'junta', {'chave': 'lastro'}]], texto='a porta')),                  # forte na Incomum
             recusa(lambda: estado.aplica(E, 'mestre', [['item', nascidas[0], 'efeito', 'junta', {'chave': 'fagulha', 'cheio': True}]], texto='o cheio')),  # cheio sem número
             recusa(lambda: estado.aplica(E, 'mestre', [['item', il, 'efeito', 'junta', {'chave': 'sinete'}]], texto='a mais, com os por escolher')),       # o teto conta os por escolher (o evento inteiro)
             recusa(lambda: estado.aplica(E, 'mestre', [['item', ic, 'efeito', 'junta', {'chave': 'prumo', 'cheio': True}]], texto='o cheio do nada')),     # cheio sem cheio por escolher
             recusa(lambda: estado.aplica(M, 'mestre', [['item', im, 'efeito', 'junta', {'chave': 'degrau'}]], texto='dois apelões'))]                       # um apelão de regra por peça
    escolha_ok = estado.aplica(E, 'forjar', [['item', il, 'efeito', 'junta', {'chave': 'prumo', 'cheio': True}], ['item', il, 'cheios_livres', 'poe', 0], ['item', il, 'efeitos_livres', 'soma', -1]], texto='a escolha (junta, cheio, por escolher) passa') is not None
    ok = not ruins and molde_ok and all(junta) and escolha_ok and not estado.valida(E) and not estado.valida(M)
    return [('FJ5 O TETO DE EFEITOS E O CHEIO: nenhuma peça passa do teto_efeitos; o cheio só em efeito de número, com o número da categoria de cima; fora do teto, só a obra-prima e um molde',
             f"{casos} saídas da conta e {len(pecas)} peças nascidas e escolhidas: {len(ruins)} fora da regra; o molde de prumo na Rara com a obra-prima no teto: teto {m1.get('teto_efeitos')} (o da Rara, {O.efeitos_max(2)}, mais 2), "
             f"o prumo cheio vale {O.valor_ferramenta('prumo', 2, True)} (o da Épica); os dois 1 com a ferramenta que segura: a peça sai sem efeito e o molde se perde: {'sim' if m2 is not None and not m2.get('efeitos') else 'NÃO'}; "
             f"o gravador recusa o efeito acima do teto (e o que passaria dele contando os por escolher), a porta errada, o cheio sem número, o cheio sem cheio por escolher e o segundo apelão de regra: {sum(bool(x) for x in junta)} de {len(junta)}; "
             f"a escolha (o efeito, o cheio e o por escolher no mesmo evento) passa: {'sim' if escolha_ok else 'NÃO'}", ok)]


def _fj6(n):
    """FJ6 A ESCOLHA: o comando, a loja e o sozinho"""
    ok = {}; E = ferord(prata=100); L = lambda: E['itens']['itens']
    F = obra_de(E, tenaz(), [20, 7], [14]); i = F['item']                  # a tenaz no fio (79: falta 1, 4 da faixa nas duas réguas, e o 20): 4 efeitos por escolher e 1 cheio
    ev0 = E['relogio']['eventos']
    ok['porta'] = bool(recusa(lambda: oficio.efeito(E, 'eu', i, 'lastro'))) and bool(recusa(lambda: oficio.efeito(E, 'eu', i, 'molde')))
    ok['pesa'] = bool(recusa(lambda: oficio.efeito(E, 'eu', i, 'pesa')))
    oficio.efeito(E, 'eu', i, 'prumo', cheio=True); um = E['relogio']['eventos'] - ev0
    ok['repete'] = bool(recusa(lambda: oficio.efeito(E, 'eu', i, 'prumo')))
    at = dict(E['gente']['eu']['atributos']); estado.aplica(E, 'gera', [['pessoa', 'nasce', 'zeca', dict(nome='Zeca', nivel=1, atributos=at, lugar='vila')]], onde='vila', texto='outro ferreiro')
    ok['dono'] = bool(recusa(lambda: oficio.efeito(E, 'zeca', i, 'afinada')))
    ev1 = E['relogio']['eventos']; oficio.efeito(E, 'eu', i, 'afinada'); oficio.efeito(E, 'eu', i, 'fagulha'); dois = 1 + E['relogio']['eventos'] - ev1
    hist = [h for h in L()[i]['historia'] if 'deu à peça o efeito' in h]
    ok['evento'] = um == 1 and dois == 3 and len(hist) == 3 and L()[i]['efeitos'][0] == {'chave': 'prumo', 'cheio': True}
    F2 = obra_de(E, oficio.molde('arma', 1, familia='espada'), [20, 7], [14]); ok['arma'] = 'o catálogo de luta chega na próxima fase' in (recusa(lambda: oficio.efeito(E, 'eu', F2['item'], 'prumo')) or '')
    # a loja escolhe ao comprar (a receita do lugar: o jeito da loja, pela semente) e o mundo escolhe sozinho (o ferreiro que não é o jogador, pelo jeito dele): mesma semente, mesma escolha
    def lote(sem):
        W = ferord(sem, prata=100); i1 = obra_de(W, tenaz(), [20, 7], [14])['item']; estado.aplica(W, 'mestre', [['item', i1, 'dono', 'poe', None], ['item', i1, 'onde', 'poe', 'vila']], texto='a peça vai à loja')
        jl, fl = oficio.escolhe_sozinho(W, i1, quem='vila')
        at_ = dict(W['gente']['eu']['atributos']); estado.aplica(W, 'gera', [['pessoa', 'nasce', 'bento', dict(nome='Bento', nivel=1, atributos=at_, lugar='vila', maestria={'forja': 4})]], onde='vila', texto='o ferreiro do mundo')
        estado.aplica(W, 'gera', [['item', 'nasce', item('ferramenta', 1, forma='martelo', dono='bento')], ['item', 'nasce', item('ferramenta', 0, oficio='forja', dono='bento', efeitos=[{'chave': 'afinada'}])], ['pessoa', 'bento', 'marca.prep_receita', 'poe', 1]], onde='vila', texto='as ferramentas dele')
        Fb = obra_de(W, tenaz(), [20, 7], [14], quem='bento'); ib = Fb['item']
        return (jl, [e['chave'] for e in W['itens']['itens'][i1]['efeitos']], oficio.jeito(W, 'bento'), [e['chave'] for e in W['itens']['itens'][ib]['efeitos']], W['itens']['itens'][ib].get('efeitos_livres', 0), estado.valida(W), Fb['texto'])
    A = lote(7); B = lote(7)
    ok['semente'] = A[:5] == B[:5] and len(A[1]) == 4 and len(A[3]) == 4 and A[4] == 0 and not A[5] and 'escolhe pelo jeito' in A[6]
    jeitos = {oficio.jeito(E, f'ferreiro{k}') for k in range(40)}; ok['jeitos'] = jeitos == set(O.JEITOS)
    # O CHEIO NÃO SE PERDE CALADO (num mundo novo, para a soma não mudar): o prumo escolhido sem `cheio`, quando o cheio não teria outro lugar, leva o cheio; a escolha que jogaria o
    # cheio fora é recusada (com `perde`, entra, e a peça diz que ele se perdeu); a receita que o jogaria fora para e pergunta
    W2 = ferord(prata=100); L2 = lambda: W2['itens']['itens']
    ic = obra_de(W2, tenaz(), [20, 7], [14])['item']; r1 = oficio.efeito(W2, 'eu', ic, 'prumo')
    sozinho = L2()[ic]['efeitos'] == [{'chave': 'prumo', 'cheio': True}] and 'o cheio foi junto' in r1 and not L2()[ic].get('cheios_livres'); tira(W2, ic)
    idd = obra_de(W2, tenaz(), [20, 7], [14])['item']
    for k in ('afinada', 'fagulha', 'sinete'): oficio.efeito(W2, 'eu', idd, k)
    rec = recusa(lambda: oficio.efeito(W2, 'eu', idd, 'recobro')) or ''; r2 = oficio.efeito(W2, 'eu', idd, 'recobro', perde=True)
    perde_ok = 'perde' in rec and 'se perde' in r2 and 'se perde' in L2()[idd]['historia'][-1] and not L2()[idd].get('cheios_livres') and not L2()[idd].get('efeitos_livres'); tira(W2, idd)
    oficio.receita(W2, 'eu', 'tenaz', 'afinada,fagulha,sinete,recobro,prumo'); Fr = obra_de(W2, tenaz(), [20, 7], [14]); ir = Fr['item']
    para = 'a receita para antes de recobro' in Fr['texto'] and L2()[ir].get('efeitos_livres') == 1 and L2()[ir].get('cheios_livres') == 1
    oficio.receita(W2, 'eu', 'tenaz', 'nada'); tira(W2, ir)
    ok['cheio'] = sozinho and perde_ok and para and not estado.valida(W2)
    ok['estado'] = not estado.valida(E)
    falhas = [k for k, v in ok.items() if not v]
    return [('FJ6 A ESCOLHA: a porta pela força; sem repetir; só o dono; cada escolha um evento; a arma da 1a não escolhe; a loja e o ferreiro do mundo escolhem sozinhos pelo jeito, e a mesma semente dá a mesma escolha; 40 ferreiros mostram os 4 jeitos; o cheio não se perde calado (o prumo o leva sozinho, a escolha que o jogaria fora pede `perde`, a receita para e pergunta)',
             f"{sum(ok.values())} de {len(ok)} conferências" + (f" (falham: {', '.join(falhas)})" if falhas else '') + f"; a loja (o jeito {A[0]}): {', '.join(A[1])}; o ferreiro do mundo (o jeito {A[2]}): {', '.join(A[3])}; os jeitos de 40 ferreiros: {', '.join(sorted(jeitos))}",
             not falhas)]


def _feitio(d): r = oficio.resumo_efeitos(d); return r['feitio']


def _fj7(n):
    """FJ7 AS FERRAMENTAS: a régua de feitio de cada efeito em cada categoria que ele abre (a média dos cinco ferreiros) e o que cada um faz; o mesmo efeito em duas; o prumo de várias fontes"""
    base = {x[0]: _feitio(oficio.dist_efeitos(x[1], x[2], x[3])) for x in REF}; linhas = []; ok_regua = True
    def ganho(kw=None, soma_mais=0, molde=False):
        g = [_feitio(oficio.dist_efeitos(s + soma_mais, t, fc, molde_cat=oc if molde else None, **(kw or {}))) - base[nome] for nome, s, t, fc, oc in REF]
        return sum(g) / len(g)
    medidas = [('afinada', 0, dict(), 1, False), ('fagulha', 0, dict(fagulha=True), 0, False)] + [('prumo', c, dict(prumo=O.valor_ferramenta('prumo', c)), 0, False) for c in range(1, 6)] \
              + [('lastro', 3, dict(lastro=True), 0, False)] + [('tempera', c, dict(tempera=O.valor_ferramenta('tempera', c)), 0, False) for c in range(3, 6)] + [('molde', 5, dict(), 0, True)]
    for k, cat, kw, mais, molde in medidas:
        g = ganho(kw, mais, molde); teto = O.FORCA_FEITIO[O.forca_da_cat(cat)]; ok_regua = ok_regua and g <= teto + 1e-9 and g >= 0
        linhas.append(f"{k} {oficio.FEM[cat]}{' ' + str(kw.get('prumo', kw.get('tempera', ''))) if kw.get('prumo') or kw.get('tempera') else ''} {g:+.2f} (teto {teto:.2f})")
    ok = {'regua': ok_regua}
    # o que cada um faz, no remate e nos atos (o dado posto à mão)
    E = _ferreiro(nivel=1, afinidade=50, mao=4, prep=None, ferramentas=()); L = lambda: E['itens']['itens']
    estado.aplica(E, 'gera', [['item', 'nasce', item('ferramenta', 2, forma='tenaz', dono='eu', efeitos=[{'chave': 'recobro'}, {'chave': 'poupa_ferro'}, {'chave': 'sinete'}, {'chave': 'remendo'}])],
                              ['item', 'nasce', item('ferramenta', 1, forma='martelo', dono='eu', efeitos=[{'chave': 'mao_de_medida'}])], ['pessoa', 'eu', 'moedas', 'soma', 500]], onde='vila', texto='as ferramentas de prova')
    esp = oficio.molde('arma', 0, familia='espada'); arco = oficio.molde('arma', 0, familia='arco')
    ok['poupa_ferro'] = (oficio.materia_da_obra(E, 'eu', esp) == {M.materia('metal', 0): 2} and oficio.materia_da_obra(E, 'eu', tenaz(0)) == oficio.materia_de(tenaz(0))
                         and oficio.materia_da_obra(E, 'eu', arco) == oficio.materia_de(arco))          # o arco (3 de madeira): o poupa-ferro poupa o ferro, não a madeira
    c0 = dict(E['gente']['eu'].get('carga') or {}); F = obra_de(E, oficio.molde('arma', 0, familia='machado'), [1], [1])          # machado: 2 de metal e 1 de madeira; os dois 1: perde
    volta = {k: v - c0.get(k, 0) for k, v in (E['gente']['eu'].get('carga') or {}).items() if v != c0.get(k, 0)}
    mt, md = M.materia('metal', 1), M.materia('madeira', 1)                 # a metade, para cima no total, a começar pela principal: a tenaz (1 e 1) devolve 1; o martelo de forja (2 e 1), 1 e 1; a espada (3), 2
    ok['recobro'] = (F['sai'] is None and volta == {M.materia('metal', 0): 1, M.materia('madeira', 0): 1} and 'o recobro devolve' in F['texto']
                     and oficio.recobro({mt: 1, md: 1}) == {mt: 1} and oficio.recobro({mt: 2, md: 1}) == {mt: 1, md: 1} and oficio.recobro({mt: 3}) == {mt: 2} and oficio.recobro({mt: 8}) == {mt: 4})
    F = obra_de(E, esp, [12], [11]); it = L()[F['item']]; ok['sinete'] = it.get('sinete') == 'eu' and 'Sinete: eu' in __import__('itens').janela(it)
    em_uso = [k for k, x in L().items() if x.get('dono') == 'eu' and x.get('uso') == 'arma']                 # o sinete na notícia de um feito: a arma em uso leva o nome de quem a forjou
    estado.aplica(E, 'mestre', [['item', k, 'uso', 'poe', None] for k in em_uso] + [['item', F['item'], 'uso', 'poe', 'arma']], texto='a espada do sinete em uso')
    ok['sinete'] = ok['sinete'] and f"que leva o sinete de {E['gente']['eu']['nome']}" in __import__('noticias').sinete(E, 'eu')
    estado.aplica(E, 'mestre', [['item', F['item'], 'dur', 'soma', -8]], texto='a peça gasta'); t0 = estado.agora(E); R = oficio.consertar(E, 'eu', F['item']); repousa(E)
    ok['remendo'] = R['feitos'] == 1 and R['pontos'] == 8 and oficio.conserto_bloco(E, 'eu') == O.REMENDO_BLOCO
    ok['mao_de_medida'] = oficio.ajuste_blocos(E, 'eu', 3) == 2 and oficio.ajuste_blocos(E, 'eu', 4) == 3
    R = oficio.ajustar(E, 'eu', F['item']); ok['mao_de_medida'] = ok['mao_de_medida'] and R['rolagem']['mais'] == oficio.conta(E, 'eu', 0, contra=O.ajuste_contra(0))['mais'] + O.MEDIDA_TESTE
    # o mesmo efeito em duas não soma (vale o maior); o prumo soma até 5; o jogo nos dois lugares vale uma vez
    G = _ferreiro(nivel=1, afinidade=50, mao=4)
    def fx_com(*fs):
        for i_ in [k for k, x in G['itens']['itens'].items() if x['tipo'] == 'ferramenta']: tira(G, i_)
        estado.aplica(G, 'gera', [['item', 'nasce', item('ferramenta', c, dono='eu', **({'forma': f} if f != 'jogo' else {'oficio': 'forja'}), efeitos=e)] for f, c, e in fs], onde='vila', texto='ferramentas'); return oficio.efeitos_em_uso(G, 'eu')
    a = fx_com(('martelo', 3, [{'chave': 'tempera'}, {'chave': 'lastro'}]), ('tenaz', 4, [{'chave': 'tempera'}, {'chave': 'lastro'}]))
    b = fx_com(('martelo', 5, [{'chave': 'prumo'}]), ('tenaz', 4, [{'chave': 'prumo'}]))
    c = fx_com(('jogo', 1, [{'chave': 'prumo', 'cheio': True}]),)
    d = fx_com(('martelo', 1, [{'chave': 'prumo'}]), ('tenaz', 2, [{'chave': 'prumo'}]))
    ok['mesmo'] = a['tempera'] == 2 and a.get('lastro') is True and b['prumo'] == O.PRUMO_MAX and c['prumo'] == 2 and d['prumo'] == 3
    ok['estado'] = not estado.valida(E) and not estado.valida(G)
    falhas = [k for k, v in ok.items() if not v]
    return [('FJ7 AS FERRAMENTAS: cada efeito, no número da categoria da ferramenta, dentro do teto da força dela (0,15 · 0,30 · 0,60 · 1,20 pontos de feitio por obra, a média dos cinco ferreiros); o recobro, o poupa-ferro, o remendo, a mão de medida e o sinete fazem o que dizem; o mesmo efeito em duas não soma; o prumo para em 5',
             f"a régua: {' · '.join(linhas)}; {sum(ok.values())} de {len(ok)} conferências" + (f" (falham: {', '.join(falhas)})" if falhas else '') + f"; (têmpera em duas: {a['tempera']}; prumo Lendário + Único: {b['prumo']}; o jogo de prumo cheio nos dois lugares: {c['prumo']}; prumo 1 + 2: {d['prumo']})",
             not falhas)]


def _fj8(n):
    """FJ8 A LOJA: o ferreiro de loja do provas_mercado com uma tenaz Incomum de poupa-ferro (a meta FORJAR PARA A LOJA NÃO É MINA, as faixas de hoje)"""
    import provas_mercado as PMe
    sementes = max(PMe.MINA_SEMENTES, n // 10); media = lambda X: sum(X) / len(X); tz = item('ferramenta', 1, forma='tenaz', efeitos=[{'chave': 'poupa_ferro'}])
    R = {nome: [PMe.ferreiro_de_loja(s, cats, ferramenta=tz) for s in range(1, sementes + 1)] for nome, cats in (('só peças Comuns', (0,)), ('Comuns e Incomuns', (0, 1)))}
    m5 = {k: media([V['rende'][0] for V in vs]) for k, vs in R.items()}; p5 = {k: max(V['rende'][0] for V in vs) for k, vs in R.items()}; m30 = {k: media([V['rende'][1] for V in vs]) for k, vs in R.items()}
    todas = [V for vs in R.values() for V in vs]; fecha = all(V['prata'] and V['inteiro'] and V['vivo'] for V in todas)
    certo = max(m5.values()) <= PMe.MINA_COMECO[0] and max(p5.values()) <= PMe.MINA_COMECO[1] and max(m30.values()) <= PMe.MINA_DEPOIS and fecha
    return [(f"FJ8 A LOJA: FORJAR PARA A LOJA NÃO É MINA com uma tenaz Incomum de poupa-ferro (o mesmo ferreiro de loja da meta do provas_mercado, que segue lá sem a tenaz): nos {PMe.MINA_DIAS[0]} primeiros dias, em média no máximo {PMe.MINA_COMECO[0]} de prata por dia e no pior caso {PMe.MINA_COMECO[1]}; depois, em média no máximo {PMe.MINA_DEPOIS}",
             f"{sementes} vilas de teste por escada. " + ' · '.join(f"{k}: {m5[k]:.2f} por dia nos {PMe.MINA_DIAS[0]} primeiros dias (o pior {p5[k]:.2f}), {m30[k]:.2f} depois ({media([V['pecas'][0] + V['pecas'][1] for V in R[k]]):.1f} peças vendidas)" for k in R)
             + f"; a prata {'fecha' if all(V['prata'] for V in todas) else 'NÃO FECHA'}; estado {'inteiro' if all(V['inteiro'] for V in todas) else 'QUEBRADO'}", certo)]


def _fj9(n):
    """FJ9 O DOM ESCONDIDO: a conta (o dom de +1 e de +2 muda a categoria, ou só o número de efeitos) e o remate que o mostra pela faixa"""
    medidas = {}
    for dom in (1, 2):                                                     # Ferord, matéria Comum: 2d20 + 23, o dom dentro
        cat = ef = ch = 0.0
        for (uns, v2, n19, n20, td), p in oficio._dados():
            a0, b0 = oficio._FACE[(uns, v2)]
            x1 = oficio._resolve(td + 23, a0, b0, 1, 1)[0][1]; x0 = oficio._resolve(td + 23 - dom, a0, b0, 1, 1)[0][1]
            c1, c0 = oficio.conta_efeitos(x1, n20), oficio.conta_efeitos(x0, n20)
            if x1['cat'] != x0['cat']: cat += p
            elif c1['efeitos'] != c0['efeitos']: ef += p
            elif c1['cheios'] != c0['cheios']: ch += p                     # (o conserto) e o dom que muda só o cheio também se mostra
        medidas[dom] = (cat, ef, ch)
    conta_ok = abs(medidas[1][0] - 0.020) < 0.0006 and abs(medidas[1][1] - 0.082) < 0.0006 and abs(medidas[2][0] - 0.038) < 0.0006 and abs(medidas[2][1] - 0.164) < 0.0006
    E = ferord(prata=100); estado.aplica(E, 'mestre', [['pessoa', 'eu', 'dom', 'poe', {'forja': 1}]], texto='um dom escondido, para a prova')
    c = oficio.valor(E, 'eu', 0); vis = c['soma']                          # a mesa vê 23; o dado leva +1 escondido
    F = obra_de(E, oficio.molde('arma', 0, familia='espada'), [12], [11])  # 12 + 11 + 23 + 1 = 47: falta 8, 2 efeitos; sem o dom, 46: falta 9, 1 efeito
    it = E['itens']['itens'][F['item']]; r = F['rolagem']
    viu = (E['gente']['eu'].get('marca') or {}).get('dom_visto') is not None and r.get('fez') == 'efeitos' and 'saía com menos efeitos' in F['texto'] and it.get('efeitos_livres') == 2 and c['oculto'] == 1 and vis == 23
    E3 = ferord(prata=100); estado.aplica(E3, 'mestre', [['pessoa', 'eu', 'dom', 'poe', {'forja': 1}]], texto='um dom escondido, para a prova')
    F3 = obra_de(E3, oficio.molde('arma', 1, familia='espada'), [20, 6], [13])     # 39 + 38 + 1 = 78: no fio, 4 + 1 do 20 = 5: 4 efeitos e 1 cheio; sem o dom, 77: 3 + 1 = 4, sem cheio
    i3 = E3['itens']['itens'][F3['item']]
    viu_cheio = F3['rolagem'].get('fez') == 'cheio' and 'saía com menos cheios' in F3['texto'] and i3.get('efeitos_livres') == 4 and i3.get('cheios_livres') == 1 and (E3['gente']['eu'].get('marca') or {}).get('dom_visto') is not None
    return [('FJ9 O DOM ESCONDIDO se mostra pela categoria ou pela faixa: um Treinado com Dom +1 e com Grande Dom (Ferord, matéria Comum) (medido: 2,0% + 8,2%; 3,8% + 16,4%); e o remate em que só o número de efeitos muda o mostra ("sem o dom, saía com menos efeitos"), e o que só muda o cheio também ("saía com menos cheios")',
             f"Dom +1: muda a categoria em {medidas[1][0]:.1%} das obras e só os efeitos em {medidas[1][1]:.1%} (e só o cheio em mais {medidas[1][2]:.1%}); Grande Dom: {medidas[2][0]:.1%} e {medidas[2][1]:.1%} (e só o cheio em mais {medidas[2][2]:.1%}); "
             f"o remate de prova: {'mostrou' if viu else 'NÃO MOSTROU'} (a mesa via 2d20 + {vis}; a peça saiu com {it.get('efeitos_livres')} efeitos por escolher); o remate em que só o cheio muda: {'mostrou' if viu_cheio else 'NÃO MOSTROU'}",
             conta_ok and viu and viu_cheio)]


def _fj10(n):
    """FJ10 A MESA: o pede (a régua de cada faixa até o teto), o remate ("faltaram N: X da faixa, Y dos 20"), a janela (o cheio), a receita (escolhe sem perguntar e a mesa relata), a arma da 1a"""
    import itens as IT
    ok = {}; E = ferord(prata=100); L = lambda: E['itens']['itens']
    pd = oficio.pede(E, 'eu', tenaz())
    ok['pede'] = all(x in pd for x in ('a RÉGUA DA FAIXA', 'Comum 22–38: 0', '53–54: 4', 'Incomum 55–63: 0', '64–71: 1', '78–79: 4', 'Rara (o teto desta obra: a régua para em 2)', '97 em diante: 2', 'efeito por obra', 'peça colada'))
    F = obra_de(E, tenaz(), [9], [18]); ok['remate'] = 'faltaram 15 para a Rara (80): o terço do meio, 1 da faixa, 0 dos 20' in F['texto']; tira(E, F['item'])     # (a peça nova sai: senão ela vira a tenaz em uso e muda a soma)
    F2 = obra_de(E, tenaz(), [20, 6], [14]); ok['remate_fio'] = 'faltaram 2 para a Rara (80): no fio, 4 da faixa, 1 dos 20 = 5: 4 efeitos por escolher (o teto da Incomum: 4), e 1 cheio' in F2['texto']
    oficio.efeito(E, 'eu', F2['item'], 'prumo', cheio=True); jan = IT.janela(L()[F2['item']]); ok['janela'] = 'cheio: o número da categoria de cima' in jan and 'conta 2 a menos' in jan and 'Efeitos por escolher: 3' in jan
    pecas = ' · '.join(ato.diz_pecas(E, 'eu')); ok['pecas'] = 'prumo 2 (cheio)' in pecas
    tira(E, F2['item'])
    oficio.receita(E, 'eu', 'tenaz', 'prumo,afinada,fagulha'); F3 = obra_de(E, tenaz(), [20, 6], [14]); t3 = L()[F3['item']]
    ok['receita'] = 'Pela sua receita: prumo' in F3['texto'] and [e['chave'] for e in t3['efeitos']] == ['prumo', 'afinada', 'fagulha'] and t3['efeitos'][0].get('cheio') and t3.get('efeitos_livres') == 1
    tira(E, F3['item'])
    F4 = obra_de(E, oficio.molde('arma', 1, familia='espada'), [20, 6], [14]); a4 = L()[F4['item']]; dz = 'efeitos por escolher: 4 (o catálogo de luta chega na próxima fase)'
    ok['arma'] = (dz.capitalize() in F4['texto'] and dz in ' · '.join(ato.diz_pecas(E, 'eu')) and dz.capitalize() in IT.janela(a4)
                  and dz in (recusa(lambda: oficio.efeito(E, 'eu', F4['item'], 'prumo')) or '') and a4.get('efeitos_livres') == 4 and a4.get('cheios_livres') == 1)
    # (o conserto) a ferramenta Comum não diz que ganhou o cheio que se perde; o pede da ferramenta conta só o cheio que ela guarda
    F5 = obra_de(E, oficio.molde('ferramenta', 0, oficio='forja'), [12], [18]); c5 = L()[F5['item']]      # 53: a Comum no fio, 4 da faixa: 2 efeitos, e a sobra de 2 cheios se perde
    ok['comum_perde'] = 'a sobra de 2 cheios se perde: não há efeito de número onde cair numa ferramenta Comum' in F5['texto'] and 'e 2 cheios (' not in F5['texto'] and not c5.get('cheios_livres') and c5.get('efeitos_livres') == 2
    tira(E, F5['item']); ok['pede_cheio'] = 'cheio guardado por obra' in pd and '1,03 efeito por obra' in pd
    ok['estado'] = not estado.valida(E)
    falhas = [k for k, v in ok.items() if not v]
    return [('FJ10 A MESA: o pede mostra a régua de cada faixa até o teto; o remate diz "faltaram N: X da faixa, Y dos 20"; a janela mostra o cheio; a receita escolhe sem perguntar e a mesa relata; a arma e a armadura forjadas na 1a mostram "efeitos por escolher: N (o catálogo de luta chega na próxima fase)"; a ferramenta Comum diz a sobra que se perde, e o pede da ferramenta conta o cheio que ela guarda',
             f"{sum(ok.values())} de {len(ok)} conferências" + (f" (falham: {', '.join(falhas)})" if falhas else ''), not falhas)]


def provas_faixa(n=300):
    """as metas da fase 1a (B2, FJ1 a FJ10), cada uma no seu mundo de rascunho"""
    out = []
    for nome, f in (('B2', _b2), ('FJ1', _fj1), ('FJ2', _fj2), ('FJ3', _fj3), ('FJ4', _fj4), ('FJ5', _fj5), ('FJ6', _fj6), ('FJ7', _fj7), ('FJ8', _fj8), ('FJ9', _fj9), ('FJ10', _fj10)):
        try: out.extend(f(n))
        except (SystemExit, Exception) as e:
            import traceback; out.append((f'{nome} (a fase 1a)', f'A PROVA QUEBROU: {type(e).__name__}: {e} · {traceback.format_exc().splitlines()[-3].strip()}', False))
    return out


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
    roda('A FAIXA DA FORJA (a parte 2, fase 1a)', lambda: provas_faixa(n))
    return out


def main():
    a = sys.argv[1:]
    if a and a[0] == 'faixa':                               # só as metas da fase 1a
        n = int(a[1]) if len(a) > 1 and a[1].isdigit() else 300; res = provas_faixa(n)
        for nome, deu, passa in res: print(f"  {'passa' if passa else 'FALHA'}  {nome}: {deu}")
        print(f'\n{sum(p for _, _, p in res)} de {len(res)} provas passam.'); return all(p for _, _, p in res)
    if a and not a[0].isdigit(): print(__doc__); return True
    n = int(a[0]) if a else 300
    print('BANCO DE PROVAS DO OFÍCIO · etapa 2: forjar, consertar, ajustar · a parte 2, fase 1a: a faixa da forja e as ferramentas (B2, FJ1 a FJ10)\n')
    res = provas(n)
    for nome, deu, passa in res: print(f"  {'passa' if passa else 'FALHA'}  {nome}: {deu}")
    print(f'\n{sum(p for _, _, p in res)} de {len(res)} provas passam.')
    return all(p for _, _, p in res)


if __name__ == '__main__':
    sys.exit(0 if main() else 1)
