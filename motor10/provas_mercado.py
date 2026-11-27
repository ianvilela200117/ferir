#!/usr/bin/env python3
"""provas_mercado.py — MOTOR 10: O BANCO DE PROVAS DO MERCADO (etapa 2: o preço que sai do estoque, a prata contada, as peças da loja, a virada do dia).

As metas são as do contrato (projeto/ETAPA2.md, seção 6). As provas rodam em mundos de rascunho (a vila de prova do provas_mundo, com um mercado aberto
pelo `mercado.funda`: 400 de povo, o estoque no alvo, a prateleira, 2.000 de prata no lugar); nunca num save.
TODA prova confere que a soma da prata do mundo (gente mais lugares) fecha e que o estado segue inteiro (`estado.valida`).
O mercado não rola dado: o acaso dele é o do mundo (`estado.sorte`), e o das provas sai de uma semente fixa. Mesma semente, mesmas provas.
A exceção é a meta FORJAR PARA A LOJA NÃO É MINA (a segunda volta): o ROBÔ FERREIRO DE LOJA vive na vila de TESTE (`vila_teste.py comeco=ferreiro`), compra a matéria na loja,
forja o que mais rende e vende à loja. Aí o dado da forja é o de verdade, e a medida muda um pouco de uma rodada para outra. A faixa dela foi dada de fora, na segunda volta, e não se mexe nela para a prova passar: a prova diz o que mediu.

Uso: python3 provas_mercado.py [N]      N = o tamanho das amostras (padrão 300): N idas e voltas ao acaso em cada mão de comércio. Os 200 negócios do contrato são sempre 200.
     (o `python3 provas_mundo.py` também roda este banco)
"""
import contextlib, copy, io, json, math, random, sys
import tabelas as T
import tabelas_mundo as M
import tabelas_mercado as C
import tabelas_oficio as O_
import estado, ato, mercado, oficio, turno
import provas_mundo as PM
from itens import item

FAIXA_ANO = (0.6, 2.2)      # o contrato: a comida, num ano de viradas numa vila de 400 pessoas, fica entre estas duas vezes a base
PERDE = 0.20                # o contrato: comprar e vender de volta no mesmo lugar perde isto ou mais
SOBRA = (0, 2)              # o contrato: o que sobra ao diarista num dia comum, em prata
# a meta FORJAR PARA A LOJA NÃO É MINA (a faixa foi dada de fora, na segunda volta; não se mexe nela para a prova passar):
MINA_DIAS = (5, 30)         # as duas janelas: os 5 primeiros dias, e daí ao Dia 30
MINA_COMECO = (6, 12)       # nos 5 primeiros dias, o que a forja rende ao ferreiro de começo, em prata por dia: em média no máximo 6 (uma diária e meia), e no pior caso no máximo 12
MINA_DEPOIS = 4             # do Dia 6 ao 30, em média no máximo 4 por dia (uma diária)
MINA_SEMENTES = 30          # em pelo menos tantas vilas de teste, de sementes diferentes


# ---------- montar um mundo de rascunho ----------
def vila(semente=1, pop=400, prata=30, caixa=None):
    """a vila de prova do provas_mundo, à meia-noite do Dia 1, com um mercado aberto: `pop` de povo, o estoque no alvo, a prateleira, e 5 de prata por pessoa no lugar"""
    E = PM.vila(semente, prata); E['relogio']['bloco'] = 0; E['turno']['aberto']['bloco'] = 0
    mercado.funda(E, 'vila', pop, prata=round(pop * C.PRATA_CABECA) if caixa is None else caixa)
    return E


def mais_um_lugar(E, pop=1500):
    """a mão do gerador: uma cidade com mercado, e a Bera morando lá (gente e lugar não têm verbo de nascer no gravador)"""
    E['lugares']['cidade'] = dict(nome='a Cidade de Prova', em='na Cidade de Prova', tipo='cidade', cama=True, estoque={})
    E['gente']['bera'] = dict(copy.deepcopy(E['gente']['eu']), nome='Bera', jogador=False, lugar='cidade', carga={})
    mercado.funda(E, 'cidade', pop)
    return E


def da(E, pid='eu', prata=0, **carga):
    """o gerador põe bens (e prata) na mão de alguém, por um evento "gera": dali em diante a conta tem de fechar"""
    ef = [['pessoa', pid, 'carga.' + k.replace('_', ':'), 'soma', n] for k, n in carga.items()] + ([['pessoa', pid, 'moedas', 'soma', prata]] if prata else [])
    estado.aplica(E, 'gera', ef, texto='os bens de prova')


def recusa(f):
    """roda f e devolve o texto da recusa (ou None se passou)"""
    try:
        with contextlib.redirect_stdout(io.StringIO()): f()
    except SystemExit as e: return str(e) or 'recusado'
    return None


def retrato(E): return json.dumps({k: E[k] for k in estado.ARQS}, sort_keys=True, ensure_ascii=False)
def prata(E): return mercado.prata_do_mundo(E)
def inteiro(E): return not estado.valida(E)


def bens_do_mundo(E):
    """todo bem que existe, somado: nas cargas e nos estoques (menos a prata, que tem a conta dela)"""
    tot = {}
    for d in [p.get('carga', {}) for p in E['gente'].values()] + [l['estoque'] for l in E['lugares'].values()]:
        for k, n in d.items():
            if k != 'prata' and n: tot[k] = tot.get(k, 0) + n
    return tot


def na_faixa(E):
    """nenhum preço de nenhum lugar com mercado fora de 0,4 a 3 bases?"""
    return all(C.FATOR_MIN - 1e-9 <= mercado.fator(E, lid, b) <= C.FATOR_MAX + 1e-9 for lid in E['lugares'] if mercado.tem_mercado(E, lid) for b in C.bens())


def um_dia(E):
    """um dia de diarista (o dia de rotina do provas_mundo: dorme na cama, come na taverna, trabalha dois blocos); o registro de rascunho não fica na memória"""
    PM.dia_de_rotina(E); E['_novos'].clear()


def um_ano(semente=1, pop=400):
    """um ano de viradas (364 dias) na vila, com um diarista vivendo nela. Devolve a série do fator de preço da comida e da lenha no começo de cada dia, e as contas."""
    E = vila(semente, pop); p0 = prata(E); eu0 = E['gente']['eu']['moedas']; S = {1: (mercado.fator(E, 'vila', 'comida'), mercado.fator(E, 'vila', 'lenha'))}; faixa = True; taverna = []
    for _ in range(M.ANO):
        um_dia(E); S[E['relogio']['dia']] = (mercado.fator(E, 'vila', 'comida'), mercado.fator(E, 'vila', 'lenha')); faixa = faixa and na_faixa(E); taverna.append(mercado.refeicao(E, 'vila'))
    return dict(E=E, serie=S, prata=prata(E) == p0, inteiro=inteiro(E), faixa=faixa, bolso=(eu0, E['gente']['eu']['moedas']), retrato=retrato(E), taverna=taverna)


# ---------- as provas do contrato ----------
def _ida_e_volta(n):
    """1. comprar sobe o preço e vender desce; comprar e vender de volta no mesmo lugar sempre perde (20% ou mais)"""
    bens = C.bens(); r = random.Random(11); piores = {}; subiu = desceu = voltou = compras = vendas = sem_volta = no_teto = no_chao = 0; fecha = True
    for mao_ in (0, 8):                                                    # um Leigo em comércio (a loja paga 60%) e um Lendário (80%)
        E = vila(prata=200000); pior = 1.0
        if mao_: estado.aplica(E, 'gera', [['pessoa', 'eu', 'maestria.comércio', 'poe', mao_]], texto='a mão de prova')
        for i in range(n):
            bem = r.choice(bens); tem = E['lugares']['vila']['estoque'].get(bem, 0); a = mercado.preco(E, 'vila', bem); teto = C.base(bem) * C.FATOR_MAX; chao = C.base(bem) * C.FATOR_MIN
            if i % 2 == 0 and tem >= 1:                                     # compra e vende de volta
                p0 = prata(E); q = r.randint(1, max(1, int(tem * r.choice((0.01, 0.1, 0.5, 1))))); c = mercado.comprar(E, 'eu', bem, q); b = mercado.preco(E, 'vila', bem); compras += 1; subiu += b > a; no_teto += b == a == teto
                if mercado.paga(E, 'eu', bem, q) < 1:                       # tão pouco que a volta não vale uma moeda (a loja recusa): perde tudo; o gerador desfaz, para a prova seguir
                    sem_volta += 1; perda = 1.0; estado.aplica(E, 'mestre', [['pessoa', 'eu', 'carga.' + bem, 'soma', -q], ['estoque', 'vila', bem, 'soma', q]], texto='o bem de prova volta')
                else: v = mercado.vender(E, 'eu', bem, q); perda = 1 - v['prata'] / c['prata']
            else:                                                           # vende (o gerador dá o bem) e compra de volta
                q = r.randint(2, max(2, int(mercado.alvo(E, 'vila', bem) * r.choice((0.05, 0.3, 1, 3))))); da(E, **{bem.replace(':', '_'): q}); p0 = prata(E); k = mercado.cabe(E, 'eu', bem)
                if k < q: estado.aplica(E, 'mestre', [['pessoa', 'eu', 'carga.' + bem, 'soma', k - q]], texto='o que a loja não tem prata para pagar sai de cena'); q = k      # a loja só compra o que a prata dela paga
                if q < 1 or mercado.paga(E, 'eu', bem, q) < 1:
                    if q: estado.aplica(E, 'mestre', [['pessoa', 'eu', 'carga.' + bem, 'soma', -q]], texto='o bem de prova sai de cena')
                    continue
                v = mercado.vender(E, 'eu', bem, q); b = mercado.preco(E, 'vila', bem); c = mercado.comprar(E, 'eu', bem, q); vendas += 1; desceu += b < a; no_chao += b == a == chao; perda = 1 - v['prata'] / c['prata']
                estado.aplica(E, 'mestre', [['pessoa', 'eu', 'carga.' + bem, 'soma', -q]], texto='o bem de prova sai de cena')
            voltou += mercado.preco(E, 'vila', bem) == a; pior = min(pior, perda); fecha = fecha and prata(E) == p0
        piores[mao_] = pior; fecha = fecha and inteiro(E)
    feitas = compras + vendas; X = vila(prata=500); c = mercado.comprar(X, 'eu', 'comida', 100); v = mercado.vender(X, 'eu', 'comida', 100)
    exemplo = f"100 de comida custam {c['prata']} e voltam por {v['prata']} ({pc(1 - v['prata'] / c['prata'])} de perda)"
    return ('IDA E VOLTA: comprar sobe o preço e vender desce; comprar e vender de volta no mesmo lugar sempre perde 20% ou mais',
            f"{feitas} idas e voltas ao acaso (todos os bens, de 1 unidade ao estoque inteiro; metade com mão de Leigo, metade de Lendário): a compra subiu o preço em {subiu} de {compras} (nas outras {no_teto} ele já estava no teto), a venda desceu em {desceu} de {vendas} (nas outras {no_chao} já estava no chão), "
            f"e desfeito o negócio o preço voltou ao que era em {voltou} de {feitas}; a menor perda: {pc(piores[0], 1)} com mão de Leigo (a loja paga 60%), {pc(piores[8], 1)} com mão de Lendário (80%); "
            f"em {sem_volta} a volta não valia uma moeda (perda inteira); exemplo, numa vila no Dia 1: {exemplo}; a prata {'fecha' if fecha else 'NÃO FECHA'}",
            feitas >= n and subiu and desceu and subiu + no_teto == compras and desceu + no_chao == vendas and voltou == feitas and min(piores.values()) >= PERDE and 1 - v['prata'] / c['prata'] >= PERDE and fecha)


def _duzentos(n):
    """2. a soma da prata (gente mais lugares) é a mesma antes e depois de 200 negócios ao acaso"""
    E = mais_um_lugar(vila(prata=600)); da(E, 'eu', comida=60, lenha=40, couro_0=30, osso_0=12, metal_1=4, couro_2=2, erva_1=3); da(E, 'bera', prata=1500, comida=30, pano=8, metal_0=20, madeira_1=5, osso_2=1)
    for pid in ('eu', 'bera'): estado.aplica(E, 'gera', [['item', 'nasce', item('arma', c, familia='lança', dono=pid)] for c in (0, 1, 2)] + [['item', 'nasce', item('armadura', 1, material='malha', dono=pid)]], texto='as peças de prova')
    estado.aplica(E, 'mestre', [['item', 'i0001', 'dur', 'soma', -6]], texto='uma peça gasta')
    r = random.Random(2); p0 = prata(E); b0 = bens_do_mundo(E); i0 = len(E['itens']['itens']); feitos = dict(compra=0, venda=0, cesta=0, compra_peca=0, venda_peca=0); recusados = 0; giro = 0; certinho = True; bens = C.bens(); voltas = 0
    while sum(feitos.values()) < 200 and voltas < 5000:
        voltas += 1; pid = r.choice(('eu', 'bera')); p = E['gente'][pid]; lid = p['lugar']; x = r.random(); antes = retrato(E) if voltas % 10 == 0 else None
        if x < 0.35:
            bem = r.choice(bens); tem = E['lugares'][lid]['estoque'].get(bem, 0); q = r.randint(1, max(1, int(tem * r.choice((0.02, 0.1, 0.4, 1.5))))); tipo = 'compra'; f = lambda: mercado.comprar(E, pid, bem, q)
        elif x < 0.62:
            carga = p.get('carga', {}); bem = r.choice(list(carga) or bens); q = r.randint(1, max(1, int(carga.get(bem, 0) * r.choice((0.3, 1, 1, 1.5))))); tipo = 'venda'; f = lambda: mercado.vender(E, pid, bem, q)
        elif x < 0.70: tipo = 'cesta'; f = lambda: mercado.vender_cesta(E, pid)
        elif x < 0.85:
            iid = r.choice([i for i, it in E['itens']['itens'].items() if not it.get('dono')] or ['i0001']); tipo = 'compra_peca'; f = lambda: mercado.comprar_peca(E, pid, iid)
        else:
            iid = r.choice(list(E['itens']['itens'])); tipo = 'venda_peca'; f = lambda: mercado.vender_peca(E, pid, iid)
        m0 = p['moedas']; rec = recusa(f)
        if rec:
            recusados += 1
            if antes is not None and antes != retrato(E): certinho = False  # negócio recusado não muda nada
        else: feitos[tipo] += 1; giro += abs(E['gente'][pid]['moedas'] - m0)
        certinho = certinho and na_faixa(E) and prata(E) == p0         # depois de cada negócio: todo preço na faixa, e a prata do mundo igual
    certo = sum(feitos.values()) == 200 and prata(E) == p0 and bens_do_mundo(E) == b0 and len(E['itens']['itens']) == i0 and inteiro(E) and certinho and all(feitos.values()) and recusados > 0
    depois = prata(E); b1 = bens_do_mundo(E); c0 = {l: E['lugares'][l]['estoque']['comida'] for l in ('vila', 'cidade')}; ev0 = E['relogio']['eventos']
    for _ in range(3): ato.passa(E, 'bera', M.BLOCOS_DIA, 'esperar', para=False)                           # três dias passam (a Bera espera): a virada roda nos dois lugares
    viradas = [e for e in E['_novos'] if e['id'] > ev0 and e['tipo'] in ('producao', 'consumo')]; andou = all(E['lugares'][l]['estoque']['comida'] != c0[l] for l in c0)
    certo = certo and prata(E) == p0 and inteiro(E) and andou and len(viradas) == 12 and {e['onde'] for e in viradas} == {'vila', 'cidade'} and na_faixa(E)
    return ('A PRATA FECHA: a soma da prata do mundo (gente mais lugares) é a mesma antes e depois de 200 negócios ao acaso',
            f"dois lugares e duas pessoas: {feitos['compra']} compras e {feitos['venda']} vendas de bem, {feitos['cesta']} vendas de cesta, {feitos['compra_peca']} compras e {feitos['venda_peca']} vendas de peça ({_m(giro)} de prata mudaram de mão), e {recusados} pedidos recusados no caminho; "
            f"a prata do mundo: {_m(p0)} antes, {_m(depois)} depois, e igual depois de cada negócio; os bens somados (carga mais estoque) {'iguais' if b0 == b1 else 'DIFERENTES'}; "
            f"três viradas depois (produção e consumo nos dois lugares: {len(viradas)} eventos), a prata segue em {_m(prata(E))}; "
            f"peças no Livro de Itens: {i0} e {len(E['itens']['itens'])}; estado {'inteiro' if inteiro(E) else 'QUEBRADO'}", certo)


def _faixa_e_caixa(n):
    """3. o preço nunca sai da faixa de 0,4 a 3 bases; a loja sem prata recusa a compra"""
    E = vila(prata=50); fora = 0; conta = 0; teto = chao = 0; bens = C.bens()
    for bem in bens:
        a = mercado.alvo(E, 'vila', bem); b = C.base(bem)
        for s in (0, 0.5, 1, 2, a / 100, a / 9.01, a / 9, a / 4, a, 2 * a, a * 6.25, a * 6.26, a * 100, 1e12):
            f = mercado.fator_de(a, s); conta += 1; fora += not C.FATOR_MIN <= f <= C.FATOR_MAX
        tem = E['lugares']['vila']['estoque'].get(bem, 0)
        if tem: estado.aplica(E, 'mestre', [['estoque', 'vila', bem, 'soma', -tem]], texto='o estoque de prova acaba')
        teto += abs(mercado.preco(E, 'vila', bem) - C.FATOR_MAX * b) < 1e-9
        estado.aplica(E, 'mestre', [['estoque', 'vila', bem, 'soma', int(a * 50) + 50]], texto='o estoque de prova transborda'); chao += abs(mercado.preco(E, 'vila', bem) - C.FATOR_MIN * b) < 1e-9
    E = vila(prata=50); da(E, lenha=200); p0 = prata(E); cx = mercado.caixa(E, 'vila')
    estado.aplica(E, 'mestre', [['estoque', 'vila', 'prata', 'soma', -cx], ['pessoa', 'eu', 'moedas', 'soma', cx]], texto='a loja fica sem prata'); antes = retrato(E)
    r1 = recusa(lambda: mercado.vender(E, 'eu', 'lenha', 20)); r2 = recusa(lambda: mercado.vender_peca(E, 'eu', 'i0001')); igual = antes == retrato(E)
    estado.aplica(E, 'mestre', [['estoque', 'vila', 'prata', 'soma', 7], ['pessoa', 'eu', 'moedas', 'soma', -7]], texto='a loja junta 7 de prata'); k = mercado.cabe(E, 'eu', 'lenha')
    r3 = recusa(lambda: mercado.vender(E, 'eu', 'lenha', k + 1)); v = mercado.vender(E, 'eu', 'lenha', k); r4 = recusa(lambda: mercado.vender_peca(E, 'eu', 'i0001'))
    certo = fora == 0 and teto == chao == len(bens) and r1 and r2 and igual and r3 and r4 and 0 < v['prata'] <= 7 and prata(E) == p0 and inteiro(E) and mercado.caixa(E, 'vila') == 7 - v['prata']
    return ('A FAIXA E O CAIXA: o preço nunca sai de 0,4 a 3 bases; a loja sem prata recusa a compra',
            f"{len(bens)} bens em {conta} estoques, de zero a um trilhão: {fora} fora da faixa; com o estoque a zero, {teto} de {len(bens)} no teto (× {vz(C.FATOR_MAX)}); transbordando, {chao} de {len(bens)} no chão (× {vz(C.FATOR_MIN)}); "
            f"a loja com 0 de prata: vender 20 de lenha {'recusado' if r1 else 'ACEITO'}, vender uma peça {'recusado' if r2 else 'ACEITO'}, estado {'intacto' if igual else 'MUDOU'}; "
            f"com 7 de prata ela compra até {k} de lenha (paga {v['prata']}) e recusa {k + 1}; a prata fecha", certo)


def _o_ano(A):
    """4. um ano de viradas numa vila de 400 pessoas: a comida fica entre 0,6 e 2,2 bases, mais cara na entressafra (do fim do inverno ao fim da primavera) e mais barata depois da colheita.
    (O que se mede: a faixa do ano; o fim do inverno pelo menos 10% acima da base e 40% acima do pós-colheita; o pós-colheita pelo menos 10% abaixo da base; o piso do ano no pós-colheita.)"""
    S = {d: v[0] for d, v in A['serie'].items()}; lo = min(S, key=S.get); hi = max(S, key=S.get); E = A['E']; est = M.ESTACAO
    marcos = [('o Dia 1', 1), ('o fim da primavera', est + 1), ('o fim do verão', 2 * est + 1), ('depois da colheita (o fim do outono)', 3 * est + 1), ('o fim do inverno', 4 * est + 1)]
    colheita = S[3 * est + 1]; inverno = S[4 * est + 1]; acima = sum(1 for v in S.values() if v > inverno)
    certo = (FAIXA_ANO[0] <= S[lo] and S[hi] <= FAIXA_ANO[1] and inverno >= 1.10 and colheita <= 0.90 and inverno >= 1.4 * colheita and abs(lo - (3 * est + 1)) <= 3
             and A['prata'] and A['inteiro'] and A['faixa'] and E['relogio']['dia'] == M.ANO + 1)
    return ('O ANO: 364 viradas numa vila de 400 pessoas; a comida fica entre 0,6 e 2,2 bases, mais cara na entressafra (do fim do inverno ao fim da primavera) e mais barata depois da colheita',
            f"a comida andou de × {vz(S[lo])} (Dia {lo}) a × {vz(S[hi])} (Dia {hi}); " + ' · '.join(f"{nome}: × {vz(S[d])}" for nome, d in marcos)
            + f"; a entressafra começa no fim do inverno ({pc(inverno / colheita - 1)} acima do pós-colheita e {pc(inverno - 1)} acima da base) e tem o pico no fim da primavera (Dia {hi}): {acima} dias do ano são mais caros que o fim do inverno, "
            f"porque a colheita da primavera é meia (tabelas_mundo.COLHEITA); o celeiro: {_m(round(E['lugares']['vila']['estoque']['comida']))} de comida no fim (começou com {_m(round(C.celeiro_dias(1) * 400))}); a prata fecha; estado {'inteiro' if A['inteiro'] else 'QUEBRADO'}", certo)


def _o_diarista(A):
    """5. com os preços de um dia comum, o diarista vive (o salário de um dia paga a cama e a comida, com sobra de 0 a 2 de prata)"""
    S = sorted(v[0] for v in A['serie'].values()); mediano = S[len(S) // 2]; pico = S[-1]; salario = 2 * M.SALARIO['diarista']; cama = M.CAMA_PRECO; a0, a1 = A['bolso']
    def comida(fator_):                                                     # o que custa a comida de um dia com a comida a este fator: (comprada para a semana, comprada no dia)
        E = vila(); a = mercado.alvo(E, 'vila', 'comida'); quer = round(a / fator_ ** 2); tem = E['lugares']['vila']['estoque']['comida']
        estado.aplica(E, 'mestre', [['estoque', 'vila', 'comida', 'soma', quer - tem]], texto='o celeiro de prova')
        return mercado.custa(E, 'vila', 'comida', M.SEMANA) / M.SEMANA, mercado.custa(E, 'vila', 'comida', 1)
    casos = [('no alvo (× 1,00)', 1.0), (f'no dia mediano do ano (× {vz(mediano)})', mediano)]; linhas = []; certo = True
    for nome, f in casos:
        sem, dia = comida(f); linhas.append(f"{nome}: a comida da semana sai a {vz(sem)} por dia e sobram {vz(salario - cama - sem)}; comprada no dia, {dia} e sobram {salario - cama - dia}")
        certo = certo and SOBRA[0] <= salario - cama - sem <= SOBRA[1] and SOBRA[0] <= salario - cama - dia <= SOBRA[1]
    sem, dia = comida(pico)
    return ('O DIARISTA VIVE: com os preços de um dia comum, o salário de um dia paga a cama e a comida, com sobra de 0 a 2 de prata',
            f"salário {salario} (2 blocos), cama {cama}; " + '; '.join(linhas) + f". NO PICO da entressafra (× {vz(pico)}) " + ('não fecha' if salario - cama - sem < 0 else 'ainda fecha') + f": a semana sai a {vz(sem)} por dia e sobram {vz(salario - cama - sem)}. "
            f"O diarista que viveu o ano da prova 4 comeu na taverna (a refeição do ato.py, a {M.REFEICAO_PRECO} de prata fixa) e foi de {a0} a {a1} de prata: {vz((a1 - a0) / M.ANO)} por dia. "
            f"Se a taverna seguisse o celeiro (mercado.refeicao: o preço do dia em prata inteira), a refeição custaria " + ', '.join(f"{k} de prata em {A['taverna'].count(k)} dias" for k in sorted(set(A['taverna'])))
            + f", e o ano dele renderia {salario * M.ANO - cama * M.ANO - sum(A['taverna'])}",
            certo and (a1 - a0) / M.ANO == salario - cama - M.REFEICAO_PRECO and A['prata'] and A['inteiro'])


def _gasta_e_quebrada(n):
    """6. peça gasta vale menos que nova; peça quebrada vale sucata"""
    tabela = C.preco_peca(2); conserto = round(tabela * M.CONSERTO_PONTO * 15); vale = {}; pagou = {}; certo = True
    for nome, gasto, sob in (('nova', 0, None), ('gasta', 15, None), ('quebrada', 30, None), ('sob', 0, dict(dono='Bera', grau=2))):       # cada uma numa vila sua: a loja não tem outra igual
        E = vila(prata=50); L = lambda: E['itens']['itens']
        estado.aplica(E, 'gera', [['item', 'nasce', item('arma', 2, f'Espada Rara {nome}', familia='espada', dono='eu', sob=sob)]], texto='a peça de prova'); iid = f"i{E['itens']['seq']:04d}"
        if gasto: estado.aplica(E, 'mestre', [['item', iid, 'dur', 'soma', -gasto]], texto='o desgaste de prova')
        p0 = prata(E); vale[nome] = mercado.preco_peca(L()[iid]); pagou[nome] = mercado.vender_peca(E, 'eu', iid)['prata']
        certo = certo and iid in mercado.prateleira(E, 'vila') and L()[iid]['dono'] is None and L()[iid]['onde'] == 'vila' and mercado.preco_peca(L()[iid]) == vale[nome] and prata(E) == p0 and inteiro(E)
    certo = (certo and vale['nova'] == tabela == 1080 and vale['gasta'] == tabela - conserto == 756 and vale['quebrada'] == round(tabela * C.SUCATA) == 108 and vale['sob'] == C.preco_peca(1) == 180
             and pagou == {k: math.floor(round(C.PAGA_PECA * v, 6)) for k, v in vale.items()}        # a loja paga a parte dela nas PEÇAS (tabelas_mercado.PAGA_PECA) sobre o valor de cada uma
             and pagou == dict(nova=432, gasta=302, quebrada=43, sob=72))                             # A DECISÃO DO JOGADOR, ESCRITA: a loja paga 40% pelas peças a um Leigo. Com outro número na tabela, esta linha falha
    return ('A PEÇA GASTA E A QUEBRADA: peça gasta vale menos que nova; peça quebrada vale sucata; pelas peças a loja paga 40% a um Leigo (432, 302, 43 e 72 pela espada Rara)',
            f"uma espada Rara: nova (30/30) vale {_m(vale['nova'])}; gasta (15/30), {vale['gasta']} (o preço menos os {conserto} do conserto que ela pede); quebrada (0/30), {vale['quebrada']} (a sucata: {pc(C.SUCATA)}); "
            f"sob medida para outro, {vale['sob']} (uma categoria abaixo); a loja pagou a um Leigo {pagou['nova']}, {pagou['gasta']}, {pagou['quebrada']} e {pagou['sob']}, e cada uma foi para a prateleira pelo valor dela; a prata fecha", certo)


# ---------- as provas que o contrato não lista, mas o módulo deve ----------
def _pelo_que_cobre(n):
    """a armadura vale pelo que cobre (o preço de tabela é o da que cobre tronco, braços e pernas), e a loja farta conta por material, não por recorte"""
    E = vila(prata=50); pecas = [('o corpo inteiro (tronco, braços e pernas)', None), ('só o tronco', ['tronco']), ('o elmo', ['cabeça']), ('só os braços', ['braços']), ('o corpo e a cabeça', ['cabeça', 'tronco', 'braços', 'pernas'])]
    estado.aplica(E, 'gera', [['item', 'nasce', item('armadura', 1, material='placa', cobre=c, dono='eu')] for _, c in pecas] + [['item', 'nasce', item('armadura', 1, material='placa', cobre=['pernas'], dono='eu')]], texto='as placas de prova')
    ids = [i for i, it in E['itens']['itens'].items() if it.get('dono') == 'eu' and it.get('material') == 'placa']; L = E['itens']['itens']; vale = [mercado.preco_peca(L[i]) for i in ids[:5]]; p0 = prata(E)
    conserto = [O_.conserto_pago(1, 10, M.peso_da_peca('armadura', c)) for _, c in pecas]; pagou = [mercado.vender_peca(E, 'eu', i)['prata'] for i in ids]      # a loja não tinha placa nenhuma: as seis são "iguais" entre si
    cheio = [math.floor(round(C.PAGA_PECA * v * C.FARTA ** (k + k), 6)) for k, v in enumerate(vale + [mercado.preco_peca(L[ids[5]])])]       # a k-ésima acha k placas iguais e k peças Incomuns acima do alvo da loja
    return ('A ARMADURA VALE PELO QUE COBRE: o preço de tabela é o da armadura de tronco, braços e pernas; a que cobre menos vale a proporção (o elmo, um quarto), no preço e no conserto; e a loja farta conta por material, não por recorte',
            'placa Incomum (tabela 180): ' + '; '.join(f'{nome}, {v}' for (nome, _), v in zip(pecas, vale)) + f"; consertar 10 pontos de cada: {', '.join(map(str, conserto))} de prata; "
            f"vendidas uma atrás da outra, a loja pagou {', '.join(map(str, pagou))} (cada recorte conta como mais uma placa igual, e como mais uma peça Incomum acima do alvo da loja: 20% a menos por cada uma das duas contas); a prata fecha",
            vale == [180, 90, 45, 45, 225] and conserto == [36, 18, 9, 9, 45] and pagou == cheio and pagou[0] == math.floor(round(C.PAGA_PECA * 180, 6)) and pagou[1] < C.PAGA_PECA * 90 and prata(E) == p0 and inteiro(E))


def _pela_materia(n):
    """a arma vale pela matéria que leva, como a armadura vale pelo que cobre: o preço de tabela é o da espada (3 unidades de matéria); cada arma vale a proporção das unidades
    de matéria dela (a mesma tabela que o ofício gasta na obra); o escudo, a das dele. Vale no que a loja pede, no que ela paga e no conserto pago."""
    base = sum(O_.MATERIA_ARMA[M.PECA_DE_TABELA].values()); pede = {0: {}, 1: {}}; certo = True; pontos = 5; paga_ = {}; conserto = {}
    for cat in pede:
        for fam in list(O_.MATERIA_ARMA) + ['escudo']:      # cada peça numa vila sua, com uma forja de vila: a prateleira no alvo, e a loja com as iguais que o gerador pôs
            E = vila(prata=500); arma = fam != 'escudo'; peca = oficio.molde('arma' if arma else 'escudo', cat, familia=fam if arma else None); un = sum(oficio.materia_de(peca).values()); quer = C.preco_peca(cat) * un / base
            estado.aplica(E, 'gera', [['lugar', 'vila', 'oficina', 'poe', 1], ['item', 'nasce', item(peca['tipo'], cat, familia=peca.get('familia'), dono='eu')]], texto='a peça e a forja de prova'); iid = f"i{E['itens']['seq']:04d}"
            it = lambda: E['itens']['itens'][iid]; k = mercado.iguais(E, 'vila', it()); pede[cat][fam] = mercado.preco_peca(it()); pg = mercado.paga_peca(E, 'eu', it())
            estado.aplica(E, 'mestre', [['item', iid, 'dur', 'soma', -pontos]], texto='o desgaste de prova'); p0 = prata(E); eu0 = E['gente']['eu']['moedas']; oficio.consertar(E, 'eu', iid, pago=True); custo = eu0 - E['gente']['eu']['moedas']
            if fam in ('adaga', M.PECA_DE_TABELA, 'montante'): paga_[fam, cat] = pg; conserto[fam, cat] = custo
            certo = (certo and pede[cat][fam] == math.ceil(round(quer, 6)) and pg == math.floor(round(C.PAGA_PECA * quer * C.FARTA ** k, 6)) and custo == max(1, math.ceil(round(quer * M.CONSERTO_PONTO * pontos, 6)))
                     and it()['dur'][0] == it()['dur'][1] and prata(E) == p0 and inteiro(E))
    t0, t1 = C.preco_peca(0), C.preco_peca(1)
    certo = (certo and pede[0][M.PECA_DE_TABELA] == t0 == 30 and pede[1][M.PECA_DE_TABELA] == t1 == 180 and pede[0]['adaga'] * 3 == t0 and pede[1]['adaga'] * 3 == t1 and pede[0]['montante'] * 3 == 5 * t0
             and pede[0]['escudo'] == t0 and len(set(pede[0].values())) >= 4)
    return ('A ARMA VALE PELA MATÉRIA QUE LEVA: o preço de tabela é o da espada (3 unidades de matéria); cada arma vale a proporção das unidades de matéria dela, e o escudo, a das dele; no que a loja pede, no que paga e no conserto pago',
            'Comuns (a loja pede): ' + ', '.join(f'{f} {v}' for f, v in pede[0].items()) + '; Incomuns: ' + ', '.join(f'{f} {v}' for f, v in pede[1].items())
            + f"; a um Leigo, a loja que já tem uma igual paga {paga_['adaga', 0]} pela adaga Comum e {paga_[M.PECA_DE_TABELA, 0]} pela espada, e a que não tem nenhuma paga {paga_['montante', 0]} pelo montante; consertar {pontos} pontos, pago: "
            f"{conserto['adaga', 1]} de prata na adaga Incomum, {conserto[M.PECA_DE_TABELA, 1]} na espada, {conserto['montante', 1]} no montante; a prata fecha", certo)


def _pecas_do_livro(n):
    """as peças da loja são itens do Livro de Itens com "onde" no lugar e sem dono; comprar e vender mudam o dono e o "onde" por evento"""
    E = mais_um_lugar(vila(prata=400)); L = lambda: E['itens']['itens']; p0 = prata(E); loja = mercado.prateleira(E, 'vila'); todas = all(it['onde'] == 'vila' and it['dono'] is None and it['id'] in L() for it in loja.values())
    iid = next(i for i, it in loja.items() if it.get('familia') == 'espada' and it['cat'] == 1); cx = mercado.caixa(E, 'vila'); eu = E['gente']['eu']['moedas']
    c = mercado.comprar_peca(E, 'eu', iid); it = L()[iid]; comprou = it['dono'] == 'eu' and it['onde'] is None and iid not in mercado.prateleira(E, 'vila') and c['prata'] == C.preco_peca(1) == 180 and mercado.caixa(E, 'vila') == cx + 180 and E['gente']['eu']['moedas'] == eu - 180
    estado.aplica(E, 'mestre', [['item', 'i0001', 'uso', 'poe', None], ['item', iid, 'uso', 'poe', 'arma']], texto='o Aldric empunha a peça comprada')
    em_uso = recusa(lambda: mercado.vender_peca(E, 'eu', iid)); quieto_ = ato.tirar(E, 'eu', iid)                 # a peça em uso não se vende: guarda-se antes
    v = mercado.vender_peca(E, 'eu', iid); it = L()[iid]; vendeu = bool(em_uso) and it['dono'] is None and it['onde'] == 'vila' and it['uso'] is None and iid in mercado.prateleira(E, 'vila') and v['prata'] == math.floor(round(C.PAGA_PECA * 180, 6)) and len(it['historia']) == 2 and inteiro(E)
    estado.aplica(E, 'gera', [['item', 'nasce', item('arma', 0, 'Adaga caída de prova', familia='adaga', onde='vila', solto=True)], ['item', 'nasce', item('arma', 4, 'Lança Única de prova', familia='lança', dono='eu')], ['item', 'nasce', item('arma', 4, 'Maça Única largada', familia='maça', onde='vila')],
                              ['item', 'nasce', dict(tipo='nucleo', cat=3, nome='Núcleo Épico de prova', dur=[1, 1], dono='eu', onde=None, de='bicho de prova', historia=[])]], texto='o que a loja não negocia')
    caida, unica, largada, nucleo = (f"i{E['itens']['seq'] - 3 + k:04d}" for k in range(4)); fora_da_loja = caida not in mercado.prateleira(E, 'vila'); outra = next(iter(mercado.prateleira(E, 'cidade'))); da_bera = 'i0002'; estado.aplica(E, 'mestre', [['item', da_bera, 'dono', 'poe', 'bera']], texto='o gibão passa para a Bera'); antes = retrato(E)
    casos = [('vender uma peça Única', lambda: mercado.vender_peca(E, 'eu', unica)), ('vender um núcleo', lambda: mercado.vender_peca(E, 'eu', nucleo)), ('vender a peça de outro', lambda: mercado.vender_peca(E, 'eu', da_bera)),
             ('comprar uma peça Única largada no lugar', lambda: mercado.comprar_peca(E, 'eu', largada)), ('comprar uma peça caída no chão (solta: não é da loja)', lambda: mercado.comprar_peca(E, 'eu', caida)), ('comprar a peça da prateleira de outro lugar', lambda: mercado.comprar_peca(E, 'eu', outra)),
             ('comprar uma peça que tem dono', lambda: mercado.comprar_peca(E, 'eu', da_bera)), ('comprar o que não está no Livro', lambda: mercado.comprar_peca(E, 'eu', 'i9999'))]
    rec = [nome for nome, f in casos if recusa(f)]; igual = antes == retrato(E)
    return ('AS PEÇAS DA LOJA são itens do Livro de Itens com "onde" no lugar e sem dono; a compra e a venda mudam o dono e o "onde", por evento',
            f"{len(loja)} peças na prateleira da vila, todas no Livro, sem dono e com onde = vila; comprar a espada Incomum: 180 de prata para o lugar, dono = eu, onde = nada; vendê-la empunhada: {'recusado' if em_uso else 'ACEITO'}; guardada: {v['prata']} ({pc(1 - v['prata'] / c['prata'])} de perda), "
            f"sai da mão, volta à prateleira, e a história dela guarda as duas linhas; {len(rec)} de {len(casos)} pedidos errados recusados" + ('' if len(rec) == len(casos) else f" (passaram: {', '.join(x for x, _ in casos if x not in rec)})")
            + f"; a peça caída no chão não entra na prateleira: {'sim' if fora_da_loja else 'NÃO'}; estado {'intacto' if igual else 'MUDOU'}; a prata fecha", todas and comprou and vendeu and fora_da_loja and len(rec) == len(casos) and igual and prata(E) == p0 and 1 - v['prata'] / c['prata'] >= PERDE)


def _loja_farta(n):
    """a loja paga menos pela peça que já tem na prateleira, e menos por toda peça de uma categoria de que a prateleira já passou do alvo: forjar para a loja sem parar não é mina"""
    E = vila(prata=50); n_ad = 14; L = lambda: E['itens']['itens']; alvo = mercado.alvo_pecas(E, 'vila'); nasce = lambda q, **k: ['item', 'nasce', item(*q, dono='eu', **k)]
    na_loja = lambda X, cat: sum(1 for it in mercado.prateleira(X, 'vila').values() if it['cat'] == cat); no_alvo = all(na_loja(E, c) == q for c, q in alvo.items()) and bool(alvo)
    estado.aplica(E, 'gera', [nasce(('arma', 0), familia='adaga') for _ in range(n_ad)] + [nasce(('arma', 0), familia='malho'), nasce(('arma', 1), familia='arco'), nasce(('arma', 1), familia='machado')], texto='as peças de prova')
    meu = lambda fam, cat=0: [i for i, it in L().items() if it.get('dono') == 'eu' and it.get('familia') == fam and it['cat'] == cat]; ids = meu('adaga'); malho = meu('malho')[0]; arco = meu('arco', 1)[0]; machado = meu('machado', 1)[0]
    p0 = prata(E); ja = mercado.iguais(E, 'vila', L()[ids[0]]); metal = mercado.custa(E, 'vila', 'metal:0', 1); pagou = []; rec = 0; v_ad = mercado.valor(L()[ids[0]]); v_malho = mercado.valor(L()[malho])
    for i in ids:
        r = recusa(lambda: pagou.append(mercado.vender_peca(E, 'eu', i)['prata'])); rec += bool(r)
    cheio = math.floor(round(C.PAGA_PECA * v_ad, 6)); espera = [math.floor(round(C.PAGA_PECA * v_ad * C.FARTA ** ((ja + k) + k), 6)) for k in range(n_ad)]; espera = [x for x in espera if x >= 1]     # a k-ésima acha ja + k iguais, e k peças Comuns acima do alvo
    vendidas = len(pagou); outro = mercado.vender_peca(E, 'eu', malho)['prata']; outro_cheio = math.floor(round(C.PAGA_PECA * v_malho, 6)); outro_espera = math.floor(round(C.PAGA_PECA * v_malho * C.FARTA ** vendidas, 6))
    inc = [mercado.vender_peca(E, 'eu', arco)['prata'], mercado.vender_peca(E, 'eu', machado)['prata']]; inc_cheio = math.floor(round(C.PAGA_PECA * C.preco_peca(1), 6))     # a outra categoria tem o alvo dela: a primeira peça Incomum sai inteira; a segunda acha uma acima do alvo
    pede = {mercado.preco_peca(it) for it in mercado.prateleira(E, 'vila').values() if it.get('familia') == 'adaga'}
    compensa = sum(1 for x in pagou if x > metal)
    # quem compra da prateleira abre espaço de novo: o que a loja pagaria por uma alabarda, antes e depois de o personagem comprar de volta uma adaga
    estado.aplica(E, 'gera', [nasce(('arma', 0), familia='alabarda'), ['pessoa', 'eu', 'moedas', 'soma', 50]], texto='mais uma peça de prova, e prata para comprar'); p1 = prata(E); alab = meu('alabarda')[0]
    antes = mercado.paga_peca(E, 'eu', L()[alab]); sobra0 = mercado.sobra(E, 'vila', L()[alab]); mercado.comprar_peca(E, 'eu', ids[0]); depois = mercado.paga_peca(E, 'eu', L()[alab]); sobra1 = mercado.sobra(E, 'vila', L()[alab])
    torto = [recusa(lambda ef=ef: estado.aplica(E, 'mestre', [ef], texto='o alvo torto')) for ef in (['lugar', 'vila', 'alvo_pecas.0', 'poe', -1], ['lugar', 'vila', 'alvo_pecas', 'poe', {'9': 2}], ['lugar', 'vila', 'alvo_pecas.0', 'soma', -99])]
    certo = (no_alvo and alvo == {0: 11, 1: 4} and all(torto) and pagou == espera and rec == n_ad - len(espera) > 0 and all(a >= b for a, b in zip(pagou, pagou[1:])) and pagou[0] < cheio and outro == outro_espera < outro_cheio
             and inc == [inc_cheio, math.floor(round(inc_cheio * C.FARTA, 6))] and compensa <= 6 and sum(pagou) < 0.3 * n_ad * cheio and pede == {math.ceil(round(v_ad, 6))}
             and sobra1 == sobra0 - 1 and depois > antes and prata(E) == p1 and p1 == p0 + 50 and inteiro(E))
    return ('A LOJA FARTA: a loja paga 20% a menos por cada peça igual que já tem na prateleira, e também 20% a menos por cada peça da mesma categoria que a prateleira tem acima do alvo do lugar (o que o gerador pôs nela ao abrir a loja); o que ela pede não muda; quem compra da prateleira abre espaço de novo',
            f"a vila nasce com a prateleira no alvo ({alvo.get(0, 0)} peças Comuns e {alvo.get(1, 0)} Incomuns, guardado no lugar por evento). {n_ad} adagas Comuns novas (cada uma vale {vz(v_ad, 0)}) vendidas uma a uma, numa loja que já tinha {ja}: "
            f"a loja paga {', '.join(map(str, pagou))} e recusa as outras {rec} (não valem uma moeda); ao todo {sum(pagou)} de prata (sem a regra seriam {n_ad * cheio}); {compensa} delas pagam mais que o metal de uma adaga ({metal} de prata); "
            f"um malho, que a loja não tinha, já não sai pelos {outro_cheio} inteiros: sai por {outro} (há {vendidas} peças Comuns acima do alvo); a outra categoria tem o alvo dela: um arco Incomum sai pelos {inc[0]} inteiros, e um machado Incomum, logo depois, por {inc[1]}; "
            f"na prateleira cada adaga segue a {vz(v_ad, 0)}; comprada de volta uma adaga, a loja passa de {antes} a {depois} pela mesma alabarda (uma peça a menos acima do alvo); o alvo torto (negativo, ou de categoria que não existe) é recusado pelo gravador: {sum(bool(x) for x in torto)} de {len(torto)}; a prata fecha", certo)


# ---------- o robô ferreiro de loja (a meta FORJAR PARA A LOJA NÃO É MINA) ----------
def _pecas_de_forja(cats, gazua=False):
    """tudo o que se forja, nestas categorias: as onze armas, o escudo, e cada armadura inteira e o elmo dela (com `gazua`, a gazua também: etapa 4b, a meta MA9 do provas_manha)"""
    for cat in cats:
        if gazua: yield oficio.molde('gazua', cat)
        for fam in O_.MATERIA_ARMA: yield oficio.molde('arma', cat, familia=fam)
        yield oficio.molde('escudo', cat)
        for mat in O_.MATERIA_ARMADURA:
            for cobre in (None, ['cabeça']): yield oficio.molde('armadura', cat, material=mat, cobre=cobre)


def _paga_se(E, peca, cat, tosca=False):
    """o que a loja pagaria HOJE por esta peça, se ela nascesse nesta categoria (ou Comum e tosca)"""
    it = item(peca['tipo'], cat, familia=peca.get('familia'), material=peca.get('material'), cobre=peca.get('cobre'), dono='eu')
    if tosca: it['dur'][0] = max(1, int(it['dur'][1] * O_.TOSCA))
    return mercado.paga_peca(E, 'eu', it)


def _escolhe(E, cats, gazua=False):
    """a peça que MAIS RENDE hoje, por bloco de bancada, a quem compra a matéria na loja e vende a peça à loja: o que a loja pagaria por ela (pesado pela chance
    de acertar e de sair uma abaixo), menos a matéria que falta comprar, menos o que a matéria que ele já tem valeria vendida. Devolve (a peça, a matéria a comprar),
    ou None se nenhuma paga a matéria (ou se o bolso não dá para a matéria e mais um dia de cama e comida)."""
    p = E['gente']['eu']; lid = p['lugar']; carga = p.get('carga', {}); est = E['lugares'][lid]['estoque']; melhor = None; reserva = M.CAMA_PRECO + M.REFEICAO_PRECO
    for peca in _pecas_de_forja(cats, gazua):
        cat = peca['cat']; mat = oficio.materia_da_obra(E, 'eu', peca); falta = {k: q - carga.get(k, 0) for k, q in mat.items() if carga.get(k, 0) < q}      # (fase 1a) com o poupa-ferro, a matéria que a obra gasta
        if any(est.get(k, 0) < q for k, q in falta.items()): continue
        custo = sum(mercado.custa(E, lid, k, q) for k, q in falta.items())
        if p['moedas'] < custo + reserva: continue
        meu = sum(mercado.parte(p) * mercado.lote(E, lid, k, min(q, carga.get(k, 0)), compra=False) for k, q in mat.items() if carga.get(k, 0) > 0)
        of = oficio.oficio_de(peca)
        if of in O_.VALOR_OFICIOS:                                  # a Lei do Valor: a soma decide a categoria; rende o que a loja pagaria por cada uma, pesado pela chance dela
            ch = oficio.valor(E, 'eu', cat, of)['chances']; rende = sum(q * _paga_se(E, peca, k) for k, q in ch.items() if k is not None)
        else:
            c = oficio.conta(E, 'eu', cat, of)
            rende = c['acerta'] * _paga_se(E, peca, cat) + c['pouco'] * (_paga_se(E, peca, cat - 1) if cat else _paga_se(E, peca, 0, tosca=True))
        lucro = (rende - custo - meu) / O_.blocos(cat)
        if lucro > 0 and (melhor is None or lucro > melhor[0]): melhor = (lucro, peca, falta)
    return melhor and melhor[1:]


def ferreiro_de_loja(semente, cats, gazua=False, ferramenta=None):
    """uma vida do FERREIRO DE LOJA: o ferreiro de começo da vila de TESTE (`vila_teste.py comeco=ferreiro`), do Dia 1 ao Dia 30. Vive de verdade (come e paga, dorme na cama
    e paga) e é GANANCIOSO: em todo bloco de bancada que o corpo deixa, compra na loja a matéria da peça que mais rende hoje (`_escolhe`), forja e vende a peça à loja na hora.
    Quando nenhuma peça paga a matéria, serve o jornal da oficina (é disso que come). Devolve, por janela (os 5 primeiros dias; daí ao Dia 30): o que a loja pagou pelas peças,
    o que ele gastou em matéria, o jornal, as peças vendidas, as obras fechadas, e o bolso.
    Com `gazua` (etapa 4b, a meta MA9 do provas_manha): a loja abre a parte da masmorra (a tocha e a gazua na prateleira) e o robô põe a gazua na lista do que forja.
    Com `ferramenta` (a parte 2, fase 1a: a meta FJ8 do provas_oficio): o robô começa com esta ferramenta na mão (a tenaz de poupa-ferro)."""
    import vila_teste
    E = vila_teste.cria('ferreiro', semente=semente); lid = E['gente']['eu']['lugar']
    if gazua: mercado.funda_masmorra(E, lid)
    if ferramenta: estado.aplica(E, 'gera', [['item', 'nasce', dict(ferramenta, dono='eu')]], onde=lid, texto='a ferramenta do ferreiro de loja')
    p0 = prata(E); t0 = estado.agora(E)
    corte = t0 + MINA_DIAS[0] * M.BLOCOS_DIA; fim = t0 + MINA_DIAS[1] * M.BLOCOS_DIA; parado = [None]
    V = dict(vendas=[0, 0], materia=[0, 0], jornal=[0, 0], pecas=[0, 0], obras=[0, 0], bolso=[E['gente']['eu']['moedas']], na_mao=0)
    w = lambda: 0 if estado.agora(E) < corte else 1          # a janela em que o relógio está
    def bancada():
        R = None
        if oficio.obras_de(E, 'eu'): R = oficio.continua(E, 'eu', blocos=1)
        elif parado[0] != E['relogio']['dia']:
            melhor = _escolhe(E, cats, gazua)
            if melhor:
                for k, q in melhor[1].items(): V['materia'][w()] += mercado.comprar(E, 'eu', k, q)['prata']
                R = oficio.forjar(E, 'eu', melhor[0], blocos=1)
            else: parado[0] = E['relogio']['dia']             # nenhuma peça paga a matéria hoje: não pergunta de novo antes de o dia virar
        if R is None: V['jornal'][w()] += oficio.jornal(E, 'eu', 1)['ganhou']; return
        if not R.get('fim'): return
        V['obras'][w()] += 1
        if R['item']:
            pg = mercado.paga_peca(E, 'eu', E['itens']['itens'][R['item']])
            if 1 <= pg <= mercado.caixa(E, lid): V['vendas'][w()] += mercado.vender_peca(E, 'eu', R['item'])['prata']; V['pecas'][w()] += 1
    while estado.agora(E) < fim and E['gente']['eu']['estado'] == 'vivo':
        b = E['relogio']['bloco']; p = E['gente']['eu']; c = p['corpo']
        if len(V['bolso']) == 1 and estado.agora(E) >= corte: V['bolso'].append(p['moedas'])
        if (c['fome'] >= 3 or (b in (0, 1, 5) and c['fome'] >= 2)) and p['moedas'] >= M.REFEICAO_PRECO and E['lugares'][lid]['estoque'].get('comida', 0) > 0:
            ato.comer(E, 'eu'); p = E['gente']['eu']; c = p['corpo']
        aguenta = c['cansaco'] + M.ESFORCO['pesado'] < M.LIMIARES['cansaco'][0] and c['sono'] + M.SONO_ACORDADO < M.LIMIARES['sono'][0]
        if b in (0, 1) or (b == 5 and not aguenta):                                         # dorme a madrugada e a alvorada; deita na noite quando o corpo não dá mais um bloco
            ato.dormir(E, 'eu', (2 - b) if b < 2 else 3, chao=not ato.cama_paga(E, 'eu') and p['moedas'] < M.CAMA_PRECO, para=False)
        elif aguenta: bancada()
        else: ato.descansar(E, 'eu', 1)
        E['_novos'].clear()                                                                  # a vida de rascunho não vai para arquivo: não guarda o registro na memória
    eu = E['gente']['eu']; V['bolso'] += [eu['moedas']] * (3 - len(V['bolso'])); V['vivo'] = eu['estado'] == 'vivo'; V['prata'] = prata(E) == p0; V['inteiro'] = inteiro(E)
    V['na_mao'] = sum(1 for it in E['itens']['itens'].values() if it.get('dono') == 'eu' and it.get('feito_por') == 'eu')      # as peças que ele forjou e a loja não quis
    V['rende'] = [(V['vendas'][i] - V['materia'][i]) / d for i, d in enumerate((MINA_DIAS[0], MINA_DIAS[1] - MINA_DIAS[0]))]   # o que a forja rende por dia, em cada janela
    V['no_bolso'] = [(V['bolso'][i + 1] - V['bolso'][i]) / d for i, d in enumerate((MINA_DIAS[0], MINA_DIAS[1] - MINA_DIAS[0]))]
    return V


def _forjar_nao_e_mina(n):
    """FORJAR PARA A LOJA NÃO É MINA: o ferreiro de começo da vila de teste, comprando matéria na loja, forjando o que mais rende e vendendo à loja. Mede-se o que a FORJA
    rende (o que a loja pagou pelas peças, menos a matéria comprada), em prata por dia. O robô tenta as duas escadas (só peças Comuns; Comuns e Incomuns) e julga-se a que rende mais."""
    sementes = max(MINA_SEMENTES, n // 10); media = lambda L: sum(L) / len(L)
    R = {nome: [ferreiro_de_loja(s, cats) for s in range(1, sementes + 1)] for nome, cats in (('só peças Comuns', (0,)), ('Comuns e Incomuns', (0, 1)))}
    m5 = {k: media([V['rende'][0] for V in vs]) for k, vs in R.items()}; p5 = {k: max(V['rende'][0] for V in vs) for k, vs in R.items()}; m30 = {k: media([V['rende'][1] for V in vs]) for k, vs in R.items()}
    todas = [V for vs in R.values() for V in vs]; fecha = all(V['prata'] and V['inteiro'] and V['vivo'] for V in todas)
    def diz(k):
        vs = R[k]; d5, d25 = MINA_DIAS[0], MINA_DIAS[1] - MINA_DIAS[0]
        return (f"{k}: nos {d5} primeiros dias a forja rende {vz(m5[k])} de prata por dia (o pior caso: {vz(p5[k])}; o melhor: {vz(min(V['rende'][0] for V in vs))}), com {vz(media([V['pecas'][0] for V in vs]), 1)} peças vendidas "
                f"em {vz(media([V['obras'][0] for V in vs]), 1)} obras; do Dia {d5 + 1} ao {MINA_DIAS[1]}, {vz(m30[k])} por dia ({vz(media([V['pecas'][1] for V in vs]), 1)} peças vendidas em {d25} dias); "
                f"no bolso, com a cama, a comida e o jornal de quando nenhuma peça paga a matéria: {mais(media([V['no_bolso'][0] for V in vs]))} e {mais(media([V['no_bolso'][1] for V in vs]))} por dia "
                f"(o jornal deu {vz(media([V['jornal'][0] for V in vs]) / d5)} e {vz(media([V['jornal'][1] for V in vs]) / d25)} por dia; sem ele, o bolso dos {d5} primeiros dias ficaria em {mais(media([V['no_bolso'][0] - V['jornal'][0] / d5 for V in vs]))})")
    certo = sementes >= MINA_SEMENTES and max(m5.values()) <= MINA_COMECO[0] and max(p5.values()) <= MINA_COMECO[1] and max(m30.values()) <= MINA_DEPOIS and fecha
    return (f"FORJAR PARA A LOJA NÃO É MINA: o ferreiro de começo da vila de TESTE, comprando matéria na loja, forjando o que mais rende e vendendo à loja, ganha com a forja (o que a loja paga pelas peças, menos a matéria) "
            f"em média no máximo {MINA_COMECO[0]} de prata por dia nos {MINA_DIAS[0]} primeiros dias (no pior caso, no máximo {MINA_COMECO[1]}), e em média no máximo {MINA_DEPOIS} por dia do Dia {MINA_DIAS[0] + 1} ao {MINA_DIAS[1]}; "
            f"vale para peças Comuns e Incomuns (julga-se a escada que rende mais)",
            f"{sementes} vilas de teste por escada. " + '. '.join(diz(k) for k in R) + f". Julgado (a escada que rende mais): {vz(max(m5.values()))} em média e {vz(max(p5.values()))} no pior caso nos {MINA_DIAS[0]} primeiros dias "
            f"({sum(V['rende'][0] > MINA_COMECO[1] for V in todas)} das {len(todas)} vidas passam de {MINA_COMECO[1]}); {vz(max(m30.values()))} em média depois; a prata {'fecha' if all(V['prata'] for V in todas) else 'NÃO FECHA'}; estado {'inteiro' if all(V['inteiro'] for V in todas) else 'QUEBRADO'}"
            + ('' if all(V['vivo'] for V in todas) else f"; MORRERAM {sum(not V['vivo'] for V in todas)}"), certo)


def _anda_sozinho(A):
    """a virada: o preço anda sozinho (o que foi comprado a mais volta; a lenha encarece no inverno), e a prata não mexe"""
    E = vila(prata=3000); p0 = prata(E); tem = E['lugares']['vila']['estoque']['lenha']; c = mercado.comprar(E, 'eu', 'lenha', tem // 2); f0 = mercado.fator(E, 'vila', 'lenha'); F = {}
    for d in range(1, 91):
        um_dia(E)
        if d in (30, 60, 90): F[d] = mercado.fator(E, 'vila', 'lenha')
    G = vila(prata=50); da(G, couro_0=120); mercado.vender(G, 'eu', 'couro:0', 120); g0 = mercado.fator(G, 'vila', 'couro:0'); g1 = prata(G)
    for d in range(90): um_dia(G)
    g90 = mercado.fator(G, 'vila', 'couro:0'); S = {d: v[1] for d, v in A['serie'].items()}; est = M.ESTACAO; verao = S[2 * est + 1]; inverno = S[4 * est + 1]
    um = vila(); n0 = um['relogio']['eventos']; PM.dia_de_rotina(um); tipos = [e['tipo'] for e in um['_novos'] if e['id'] > n0]; sem_prata = all(not any(x[0] == 'estoque' and x[2] == 'prata' for x in e['efeitos']) for e in um['_novos'] if e['tipo'] in ('producao', 'consumo'))
    certo = (abs(f0 - 2 ** 0.5) < 0.01 and F[30] < f0 - 0.2 and F[90] <= 1.10 and F[30] > F[60] > F[90] and g0 < 0.72 and g0 < g90 < 1 and inverno >= 1.2 and verao <= 0.95
             and prata(E) == p0 and prata(G) == g1 and inteiro(E) and inteiro(G) and tipos.count('producao') == 1 and tipos.count('consumo') == 1 and sem_prata)
    return ('O PREÇO ANDA SOZINHO: o lugar produz mais do que falta e menos do que sobra; a lenha encarece no inverno; a virada não mexe na prata',
            f"comprada a metade da lenha da vila ({_m(c['n'])} por {_m(c['prata'])}), o preço vai a × {vz(f0)}; sem mais negócio: × {vz(F[30])} em 30 dias, × {vz(F[60])} em 60, × {vz(F[90])} em 90; "
            f"vendido couro até dobrar o estoque, o preço cai a × {vz(g0)} e está em × {vz(g90)} 90 dias depois (o que sobra escoa devagar); a lenha no ano da prova 4: × {vz(verao)} no fim do verão, × {vz(inverno)} no fim do inverno; "
            f"cada virada são um evento de produção e um de consumo por lugar, sem efeito na prata; a prata fecha", certo)


def _celeiro(A):
    """o ciclo do ano se repete igual; e o lugar que colhe um décimo a menos (ou a mais) do que come não desanda: acha outro ciclo, mais caro (ou mais barato)"""
    def anos(safra, n=3):
        E = vila(); p0 = prata(E); out = []
        if safra != 1: estado.aplica(E, 'mestre', [['lugar', 'vila', 'produz.comida', 'poe', 400 * safra]], texto='a safra de prova')
        for _ in range(n):
            fs = []
            for _ in range(M.ANO): um_dia(E); fs.append(mercado.fator(E, 'vila', 'comida'))
            out.append((min(fs), max(fs)))
        return out, prata(E) == p0 and inteiro(E)
    igual, ok1 = anos(1); menos, ok2 = anos(0.9); mais, ok3 = anos(1.1); perto = lambda a, b, tol: abs(a[0] - b[0]) <= tol and abs(a[1] - b[1]) <= tol
    diz = lambda r: ' · '.join(f"ano {i + 1}: × {vz(a)} a × {vz(b)}" for i, (a, b) in enumerate(r))
    certo = (perto(igual[0], igual[2], 0.02) and perto(menos[1], menos[2], 0.05) and perto(mais[1], mais[2], 0.05) and menos[2][1] > igual[2][1] + 0.1 and mais[2][1] < igual[2][1] - 0.1
             and menos[2][1] < C.FATOR_MAX and mais[2][0] > C.FATOR_MIN and FAIXA_ANO[0] <= igual[2][0] and igual[2][1] <= FAIXA_ANO[1] and ok1 and ok2 and ok3)
    return ('O CELEIRO SE ACERTA SOZINHO: o ciclo do ano se repete; o lugar que colhe 10% a menos (ou a mais) do que come acha outro ciclo, mais caro (ou mais barato), sem desandar',
            f"três anos seguidos, com um diarista comendo na vila. Safra igual ao consumo: {diz(igual)}. Safra 10% menor: {diz(menos)}. Safra 10% maior: {diz(mais)}. A prata fecha nos três", certo)


def _comercio(n):
    """a maestria de comércio: a loja paga de 60 a 80% conforme a mão de quem vende; a mão sobe por dias de negócio, e de Mestre para cima pede um feito"""
    partes = [C.parte(m) for m in (0, 2, 4, 6, 8)]; E = vila(prata=3000); p0 = prata(E); t = lambda: E['gente']['eu'].get('treino', {}).get('comércio', 0)
    mercado.comprar(E, 'eu', 'lenha', 5); miudo = t(); mercado.comprar(E, 'eu', 'lenha', 20); mercado.comprar(E, 'eu', 'lenha', 20); um = t()         # negócio miúdo não conta; dois no mesmo dia contam um
    for _ in range(C.COMERCIO_DIAS[2] - 2): um_dia(E); mercado.comprar(E, 'eu', 'lenha', 20)
    antes = mercado.mao(E['gente']['eu']); um_dia(E); R = mercado.comprar(E, 'eu', 'lenha', 20); depois = mercado.mao(E['gente']['eu']); pct = mercado.parte(E['gente']['eu'])
    estado.aplica(E, 'mestre', [['pessoa', 'eu', 'treino.comércio', 'soma', C.COMERCIO_DIAS[6]]], texto='anos de balcão, para a prova'); falta = mercado.sobe(E, 'eu'); treinado = mercado.mao(E['gente']['eu'])
    estado.aplica(E, 'gera', [['item', 'nasce', item('arma', 2, 'Espada Rara da vitrine', familia='espada', onde='vila')]], texto='uma peça cara na prateleira'); iid = f"i{E['itens']['seq']:04d}"
    mercado.comprar_peca(E, 'eu', iid); mestre = mercado.mao(E['gente']['eu']); feito = E['gente']['eu'].get('marca', {}).get('feito_comércio')
    L, Ld = (vila(prata=50) for _ in range(2)); estado.aplica(Ld, 'gera', [['pessoa', 'eu', 'maestria.comércio', 'poe', 8]], texto='a mão de prova')
    for X in (L, Ld): da(X, lenha=100)
    q0 = prata(L), prata(Ld); leigo = mercado.vender(L, 'eu', 'lenha', 100)['prata']; lend = mercado.vender(Ld, 'eu', 'lenha', 100)['prata']; fecha = q0 == (prata(L), prata(Ld)) and inteiro(L) and inteiro(Ld)
    partes_peca = [C.parte_peca(m) for m in (0, 2, 4, 6, 8)]; espada = {}                             # NAS PEÇAS a mão soma os mesmos 5 pontos por grau, de 40 a 60%: a mesma espada Rara, por um Leigo e por um Lendário em comércio
    for nome, mao_ in (('leigo', 0), ('lendario', 8)):
        X = vila(prata=50)
        if mao_: estado.aplica(X, 'gera', [['pessoa', 'eu', 'maestria.comércio', 'poe', mao_]], texto='a mão de prova')
        estado.aplica(X, 'gera', [['item', 'nasce', item('arma', 2, 'Espada Rara de prova', familia='espada', dono='eu')]], texto='a peça de prova'); x0 = prata(X)
        espada[nome] = mercado.vender_peca(X, 'eu', f"i{X['itens']['seq']:04d}")['prata']; fecha = fecha and prata(X) == x0 and inteiro(X)
    nas_pecas = all(abs(a - b) < 1e-9 for a, b in zip(partes_peca, [0.40, 0.45, 0.50, 0.55, 0.60])) and len(partes_peca) == 5 and espada == dict(leigo=432, lendario=648)
    certo = (nas_pecas and partes == [0.60, 0.65, 0.70, 0.75, 0.80] and (miudo, um) == (0, 1) and (antes, depois) == (0, 2) and 'MAESTRIA' in R['texto'] and abs(pct - 0.65) < 1e-9 and treinado == 4 and 'falta o feito' in falta
             and mestre == 6 and feito == 6 and leigo < lend and abs(lend / leigo - 80 / 60) < 0.03 and prata(E) == p0 and inteiro(E) and fecha)
    return ('A MÃO DE COMÉRCIO: pelos bens a loja paga 60% a um Leigo e 5 pontos a mais por grau, até 80%; pelas PEÇAS, 40% e os mesmos 5 pontos por grau, até 60%; a mão sobe por dias de negócio, e de Mestre para cima pede um negócio grande',
            f"pelos bens a loja paga {', '.join(pc(x) for x in partes)} (Leigo a Lendário): 100 de lenha rendem {leigo} a um Leigo e {lend} a um Lendário; pelas peças paga {', '.join(pc(x) for x in partes_peca)}: "
            f"a mesma espada Rara (vale {_m(C.preco_peca(2))}) rende {espada['leigo']} a um Leigo e {espada['lendario']} a um Lendário em comércio; negócio de menos de {C.NEGOCIO_MIN} de prata não conta, dois no mesmo dia contam um; "
            f"com {C.COMERCIO_DIAS[2] - 1} dias de negócio: {T.MAESTRIAS[antes]}; com {C.COMERCIO_DIAS[2]}: {T.MAESTRIAS[depois]}; com {C.COMERCIO_DIAS[2] + C.COMERCIO_DIAS[6]} dias e nenhum negócio grande: {T.MAESTRIAS[treinado]} (falta o feito); "
            f"depois de comprar uma peça de {_m(C.preco_peca(2))}: {T.MAESTRIAS[mestre]}; a prata fecha", certo)


def _recusas(n):
    """o que não pode ser negociado é recusado sem mudar nada; lugar sem povo não tem mercado; sem argumento, o script só diz o uso"""
    E = vila(prata=20); da(E, lenha=5, sal=1); antes = retrato(E); p0 = prata(E)
    casos = [('comprar sem a prata', lambda: mercado.comprar(E, 'eu', 'ferramenta', 5)), ('comprar mais do que o lugar tem', lambda: mercado.comprar(E, 'eu', 'remédio', 61)), ('comprar o que a loja não negocia', lambda: mercado.comprar(E, 'eu', 'ouro', 1)),
             ('comprar matéria Épica (metal:3)', lambda: mercado.comprar(E, 'eu', 'metal:3', 1)), ('comprar a prata', lambda: mercado.comprar(E, 'eu', 'prata', 5)), ('comprar zero', lambda: mercado.comprar(E, 'eu', 'comida', 0)),
             ('comprar meia unidade', lambda: mercado.comprar(E, 'eu', 'comida', '0.5')), ('comprar um número negativo', lambda: mercado.comprar(E, 'eu', 'comida', -3)), ('vender o que não carrega', lambda: mercado.vender(E, 'eu', 'pano', 1)),
             ('vender mais do que carrega', lambda: mercado.vender(E, 'eu', 'lenha', 6)), ('vender o que não vale uma moeda (1 de lenha)', lambda: mercado.vender(E, 'eu', 'lenha', 1)), ('vender tudo de um bem que não carrega', lambda: mercado.vender(E, 'eu', 'carvão', 'tudo')),
             ('comprar uma peça sem a prata', lambda: mercado.comprar_peca(E, 'eu', next(i for i, it in mercado.prateleira(E, 'vila').items() if it['cat'] == 1))), ('negociar em nome de quem não existe', lambda: mercado.comprar(E, 'fantasma', 'comida', 1))]
    rec = [nome for nome, f in casos if recusa(f)]; igual = antes == retrato(E) and prata(E) == p0
    S = PM.vila(prata=50); da(S, lenha=30); antes_s = retrato(S); ev0 = S['relogio']['eventos']; s0 = prata(S)                          # a vila da etapa 1: sem `pop`, não tem mercado
    sem = [recusa(lambda: mercado.comprar(S, 'eu', 'comida', 1)), recusa(lambda: mercado.vender(S, 'eu', 'lenha', 30)), recusa(lambda: mercado.vender_peca(S, 'eu', 'i0001'))]
    mercado.virada(S); parado = all(sem) and antes_s == retrato(S) and S['relogio']['eventos'] == ev0 and 'não há mercado' in '\n'.join(mercado.mesa(S)); r2 = recusa(lambda: mercado.funda(E, 'vila', 100))
    estado.aplica(E, 'mestre', [['pessoa', 'eu', 'pv', 'soma', -9999], ['pessoa', 'eu', 'estado', 'poe', 'morto'], ['item', 'i0001', 'uso', 'poe', None], ['item', 'i0002', 'uso', 'poe', None]], texto='o Aldric morre, para a prova'); morto = recusa(lambda: mercado.vender(E, 'eu', 'lenha', 5))
    with contextlib.redirect_stdout(io.StringIO()) as tela: mercado.main([])
    uso = tela.getvalue().startswith('mercado.py') and 'Uso' in tela.getvalue()
    meias = [recusa(lambda a=a: mercado.main(a)) or '' for a in (['comprar'], ['funda'], ['funda', 'abc'], ['funda', '-5'], ['preco'])]      # o comando pela metade, ou com o número torto: UMA frase que diz o que falta
    uso2 = all(m and len(m.splitlines()) == 1 and 'Uso' not in m for m in meias)
    return ('AS RECUSAS: o que não pode ser negociado é recusado e nada muda pela metade; lugar sem povo não tem mercado; sem argumento, o script só diz o uso; com o comando pela metade, uma frase diz o que falta',
            f"{len(rec)} de {len(casos)} recusados" + ('' if len(rec) == len(casos) else f" (passaram: {', '.join(x for x, _ in casos if x not in rec)})") + f"; estado {'intacto' if igual else 'MUDOU'}; "
            f"na vila da etapa 1 (sem `pop`): comprar, vender e vender peça recusados, e a virada não gera evento nenhum: {'sim' if parado else 'NÃO'}; abrir mercado onde já há: {'recusado' if r2 else 'ACEITO'}; morto não negocia: {'recusado' if morto else 'ACEITO'}; "
            f"sem argumento: {'só o uso' if uso else 'FEZ OUTRA COISA'}; cinco comandos pela metade ou com número torto: {'uma frase cada' if uso2 else 'NÃO'} («{meias[2][:44]}...»); a prata fecha", len(rec) == len(casos) and igual and parado and r2 and morto and uso and uso2 and prata(E) == p0 and prata(S) == s0)


def _a_mesa(n):
    """mesa(E) mostra os preços do lugar onde o personagem está"""
    E = mais_um_lugar(vila(prata=80)); da(E, couro_0=6, osso_1=2); p0 = prata(E)
    estado.aplica(E, 'mestre', [['estoque', 'cidade', 'comida', 'soma', -E['lugares']['cidade']['estoque']['comida'] // 2]], texto='a cidade come a metade do celeiro')
    def linha(txt, bem): return next((l for l in txt.splitlines() if l.startswith(f'| {bem} |')), '')
    def confere(lid):
        txt = '\n'.join(mercado.mesa(E)); l = E['lugares'][lid]; outro = E['lugares']['cidade' if lid == 'vila' else 'vila']; lc = linha(txt, 'comida')
        return (txt.startswith('## O mercado') and l['nome'] in txt and outro['nome'] not in txt and mercado._m(l['estoque']['comida']) in lc and mercado._n(mercado.preco(E, lid, 'comida')) in lc
                and f"10 por {mercado.custa(E, lid, 'comida', 10)}" in lc and f"{mercado.paga(E, 'eu', 'comida', 10)} por 10" in lc and all(i in txt for i in mercado.prateleira(E, lid))
                and not any(i in txt for i in mercado.prateleira(E, 'cidade' if lid == 'vila' else 'vila')) and '| couro Comum |' in txt and '| osso Incomum |' in txt and 'i0001' in txt), txt, lc
    v_ok, v_txt, v_l = confere('vila'); estado.aplica(E, 'mestre', [['pessoa', 'eu', 'lugar', 'poe', 'cidade']], texto='o Aldric muda de lugar, para a prova'); c_ok, c_txt, c_l = confere('cidade')
    inteira = turno.mesa(E); tam = len(c_txt.encode()); tudo = len(inteira.encode())
    return ('A MESA: mesa(E) mostra os preços do lugar onde o personagem está (o estoque, o preço do dia, o que custa comprar, o que a loja paga, a prateleira, o que ele carrega)',
            f"na vila, a linha da comida: «{v_l}»; na cidade (com meio celeiro): «{c_l}»; cada mesa traz só o lugar dela, a prateleira dele e a carga do personagem; "
            f"a parte do mercado: {tam} bytes; a MESA.md inteira, com ela: {tudo} bytes (o teto da etapa 1 são 8.000); a mesa só lê: a prata fecha", v_ok and c_ok and v_l != c_l and c_txt in inteira and tudo <= 8000 and inteiro(E) and prata(E) == p0)


def _mesmo_mundo(A):
    """mesma semente, mesmo mercado; semente diferente, não (o acaso do mercado é só o do mundo)"""
    fecha = []
    def roda(sem, pop):
        E = vila(sem, pop); p0 = prata(E); mercado.comprar(E, 'eu', 'lenha', 10)
        for _ in range(40): um_dia(E)
        fecha.append(prata(E) == p0 and inteiro(E)); return retrato(E)
    igual = roda(7, 137) == roda(7, 137); outro = roda(7, 137) != roda(8, 137); B = um_ano(1, 400)
    return ('O MESMO MUNDO: mesma semente e mesmos atos dão o mesmo mercado; semente diferente, não',
            f"40 dias numa vila de 137 pessoas (onde o consumo do dia tem parte quebrada, e a sobra vira acaso do mundo): mesma semente {'igual' if igual else 'DIFERENTE'}, outra semente {'diferente' if outro else 'IGUAL'}; "
            f"o ano inteiro da prova 4, rodado de novo: {'idêntico' if B['retrato'] == A['retrato'] else 'DIFERENTE'}; a prata fecha em todos", igual and outro and B['retrato'] == A['retrato'] and all(fecha) and B['prata'])


def _m(x): return mercado._m(x)
def vz(x, casas=2): return mercado._n(x, casas).replace('-', '−')              # 1,17 (e −0,35)
def mais(x, casas=2): return ('+' if x > 0 else '') + mercado._n(x, casas).replace('-', '−')      # +1,17 e −0,35
def pc(x, casas=0): return f'{100 * x:.{casas}f}%'.replace('.', ',')        # 36,4%


def provas(n=300):
    out = []; A = {}
    def roda(nome, f):
        try: out.append(f())
        except (SystemExit, Exception) as e: out.append((nome, f'A PROVA QUEBROU: {type(e).__name__}: {e}', False))
    try: A = um_ano()
    except (SystemExit, Exception) as e: out.append(('O ANO (a medição)', f'A PROVA QUEBROU: {type(e).__name__}: {e}', False))
    for nome, f in (('IDA E VOLTA', lambda: _ida_e_volta(n)), ('A PRATA FECHA', lambda: _duzentos(n)), ('A FAIXA E O CAIXA', lambda: _faixa_e_caixa(n)), ('O ANO', lambda: _o_ano(A)), ('O DIARISTA VIVE', lambda: _o_diarista(A)),
                    ('A PEÇA GASTA E A QUEBRADA', lambda: _gasta_e_quebrada(n)), ('AS PEÇAS DA LOJA', lambda: _pecas_do_livro(n)), ('A ARMADURA VALE PELO QUE COBRE', lambda: _pelo_que_cobre(n)), ('A ARMA VALE PELA MATÉRIA QUE LEVA', lambda: _pela_materia(n)), ('A LOJA FARTA', lambda: _loja_farta(n)), ('FORJAR PARA A LOJA NÃO É MINA', lambda: _forjar_nao_e_mina(n)), ('O PREÇO ANDA SOZINHO', lambda: _anda_sozinho(A)), ('O CELEIRO SE ACERTA SOZINHO', lambda: _celeiro(A)), ('A MÃO DE COMÉRCIO', lambda: _comercio(n)),
                    ('AS RECUSAS', lambda: _recusas(n)), ('A MESA', lambda: _a_mesa(n)), ('O MESMO MUNDO', lambda: _mesmo_mundo(A))):
        roda(nome, f)
    return out


def main():
    a = sys.argv[1:]
    if a and not a[0].isdigit(): print(__doc__); return True
    n = int(a[0]) if a else 300
    print('BANCO DE PROVAS DO MERCADO · etapa 2: o preço, a prata contada, as peças da loja, a virada\n')
    res = provas(n)
    for nome, deu, passa in res: print(f"  {'passa' if passa else 'FALHA'}  {nome}: {deu}")
    print(f'\n{sum(p for _, _, p in res)} de {len(res)} provas passam.')
    return all(p for _, _, p in res)


if __name__ == '__main__':
    sys.exit(0 if main() else 1)
