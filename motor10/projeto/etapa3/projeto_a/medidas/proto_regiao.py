#!/usr/bin/env python3
"""proto_regiao.py — PROTÓTIPO DE MEDIDA (projeto A, etapa 3): a região que nasce em volta da vila de teste, e o dia da região (o povo em número, o carreto,
a prata que se repõe, a freguesia, a forja do povo, a caça do povo, a comida que estraga, o bicho que sai do ermo, a fome, a migração, o bando).
NÃO É MOTOR: é o rascunho com que o PROJETO.md mede os números. Tudo entra pelo gravador (o proto_aplica, que aceita o verbo 'rota' e o arquivo 'rotas').
Os números moram em TAB (o que seria o tabelas_regiao.py).
"""
import copy, math, random, sys
import estado, mercado, caca, bichos, masmorra, itens
import tabelas as T, tabelas_mundo as M, tabelas_mercado as C, tabelas_caca as K, tabelas_bichos as TB
import proto_aplica

# ======================= A PÁGINA (o que seria o tabelas_regiao.py) =======================
TAB = dict(
    # os povoados: quantos de cada tipo, o povo, a forja (oficina, e o alcance do fogo e da bigorna), a mesa de runas, a botica, o santuário, e as partes do povo
    # (a fração que é guarda, caçador e carreteiro: o resto produz o que o perfil diz)
    TIPOS={'capital': dict(n=1, pop=4000, oficina=3, alcance=3, runas=2, botica=2, santuario=2, guarda=0.03, cacador=0.0, prat='cidade'),
           'cidade':  dict(n=2, pop=1500, oficina=2, alcance=2, runas=1, botica=1, santuario=1, guarda=0.02, cacador=0.005, prat='cidade'),
           'vila':    dict(n=5, pop=400, oficina=1, alcance=1, runas=None, botica=1, santuario=None, guarda=0.01, cacador=0.01, prat='vila'),
           'aldeia':  dict(n=8, pop=120, oficina=0, alcance=0, runas=None, botica=None, santuario=None, guarda=0.0, cacador=0.03, prat=None)},
    # o perfil: quanto o lugar produz de cada bem, vezes o que o povo dele come (1: o que come; a cidade compra comida, a aldeia vende)
    PERFIL={'capital': {'comida': 0.75, 'lenha': 0.7, 'madeira:0': 0.6, 'pano': 1.5, 'ferramenta': 1.6, 'remédio': 1.2, 'metal:0': 0.7, 'couro:0': 0.9, 'sal': 0.8},
            'cidade':  {'comida': 0.9, 'lenha': 0.9, 'pano': 1.3, 'ferramenta': 1.3, 'sal': 1.4, 'metal:0': 0.9},
            'vila':    {'comida': 1.25, 'lenha': 1.2, 'madeira:0': 1.3, 'couro:0': 1.3, 'pano': 0.8, 'ferramenta': 0.8, 'sal': 0.7},
            'aldeia':  {'comida': 1.4, 'pano': 0.6, 'ferramenta': 0.5, 'sal': 0.6, 'remédio': 0.7}},
    ESPECIALIDADE={'capital': ['ferramenta', 'pano', 'remédio'], 'cidade': ['ferramenta', 'pano', 'sal'], 'vila': ['comida', 'couro:0', 'madeira:0'], 'aldeia': ['comida', 'metal:0', 'madeira:0', 'erva:0']},
    PERFIL_ERMO={'floresta': {'madeira:0': 2.0, 'lenha': 1.6, 'couro:0': 1.4, 'madeira:1': 1.5},
                 'serra': {'metal:0': 3.0, 'metal:1': 2.0, 'carvão': 1.5, 'comida': 0.85},
                 'caverna': {'metal:0': 2.5, 'metal:1': 2.0, 'comida': 0.85},
                 'brejo': {'erva:0': 2.0, 'erva:1': 1.5, 'remédio': 1.4},
                 'campo': {'comida': 1.25, 'couro:0': 1.6, 'osso:0': 1.4},
                 'ruína': {}},
    BOLSA_CABECA=5,             # a bolsa do povo: tanta prata por pessoa, quando a região nasce (nasce num evento gera, como a prata da 4b)
    FORA=dict(pop=20000, caixa=100000),       # o mundo de fora: um mercado grande e equilibrado no fim da estrada real e do rio, com as mesmas estações
    # O CARRETO DO POVO (quem leva os bens de um lugar ao outro): por rota, por bem, por dia
    FLUXO=0.02,                 # a parte da diferença de preço que o carreto fecha por dia (vezes o menor dos dois alvos)
    FRETE=0.012,                # o frete do povo: tanto de prata por unidade de peso por bloco de rota
    MARGEM=0.05,                # o carreteiro só leva quando a diferença passa do frete e disto (do preço de origem)
    PISO=0.5,                   # ninguém vende abaixo de tanto do alvo (o celeiro não se esvazia para fora)
    CAPACIDADE={'estrada': 1500, 'caminho': 500, 'trilha': 150, 'fora': 200},     # o peso que o carreto do povo leva por dia, numa rota (vezes 1 menos o perigo do carreto)
    PESO={'comida': 1, 'lenha': 2, 'carvão': 1, 'sal': 1, 'pano': 1, 'remédio': 0.2, 'ferramenta': 2, 'metal': 2, 'couro': 1, 'osso': 0.5, 'madeira': 2, 'erva': 0.2, 'tocha': 0.5},
    # A PRATA DO LUGAR QUE SE REPÕE: o caixa (a loja, quem paga o serviço) e a bolsa do povo se acertam devagar
    RELAXA=0.02,                # por dia, a bolsa paga ao caixa (ou o caixa à bolsa) esta fração da diferença do caixa para o alvo dele (5 de prata por pessoa)
    # A FREGUESIA: o povo compra da prateleira (por pessoa, por dia, por categoria); paga o que a loja pede, da bolsa ao caixa; a peça sai do mundo (gasta no uso)
    FREGUES={0: 0.0002, 1: 0.00002},
    # A FORJA DO POVO: os ferreiros do lugar refazem a prateleira até o alvo (por dia: esta chance vezes o que falta, com a matéria do estoque)
    FORJA_POVO={0: 0.0003, 1: 0.00003},      # os ferreiros do povo fazem, por pessoa e por dia, tantas peças de cada categoria, até a prateleira voltar ao alvo (com a matéria do estoque)
    # A CAÇA DO POVO: cada caçador tira tantos bichos por dia do ermo de borda vizinho (as presas: corça, javali, ratazana); o despojo entra no estoque
    CACA_POVO=0.05, PRESAS=('corça', 'javali', 'ratazana'),
    ESTRAGA=0.02,
    SAFRA_REGIAO=(0.8, 1.15), SAFRA_LUGAR=(0.85, 1.15), SAFRA_NA_VILA=True,      # a colheita do ano: a da região inteira, vezes a de cada lugar (a média é um pouco abaixo de 1: o ano bom e o ruim)               # a comida da carga perde isto por dia (o celeiro do lugar, não)
    # O BICHO QUE SAI DO ERMO (por semana): o predador com fome (a presa rareou) ou no inverno desce ao povoado vizinho e come gado; a guarda mata alguns
    PREDADORES={'lobo': dict(gado=6, mata=0.05), 'urso': dict(gado=10, mata=0.1), 'pantera': dict(gado=8, mata=0.15)},
    SAI=0.03, GUARDA_MATA_MAX=0.5,                   # chance por semana, por cabeça × ousadia × (fome do bicho + inverno)
    INVERNO=0.5,
    # A FOME E A MIGRAÇÃO (por semana)
    FOME_DIAS=3,                # o lugar com menos de tantos dias de comida passa fome
    FOME_MORRE=0.005, FOME_SAI=0.02, BANDO_PARTE=0.2,      # por semana de fome: morrem, saem; dos que saem, tantos vão para o bando
    TERRA=0.5,                  # A TERRA NÃO SAI COM QUEM SAI: quando o povo muda, a colheita muda pela raiz da razão (o resto da produção, pela razão inteira: é braço)
    POBRE=0.5, POBRE_SAI=0.01, CHEGA_MAX=0.02,     # a prata por cabeça abaixo de tanto da média da região: saem tantos por semana; um lugar recebe até tanto do povo dele por semana
    # O BANDO (salteadores contados num ermo): a patrulha mata, a fome engrossa
    BANDO_INICIAL=(4, 8), PATRULHA_MATA=0.004, BANDO_CHEGA=0.05, BANDO_TETO=8,      # a patrulha mata 1 por semana com a chance de 0,4% por guarda dos povoados vizinhos (até 50%); chega 1 com 15% (mais 20% se um vizinho é pobre)
    IMPOSTO=0.03,
    PRATA_CABECA_ALVO=10,       # a prata de um povoado (caixa e bolsa) que o fluxo da prata tem por certa: 10 por pessoa (5 no caixa, 5 na bolsa)
    MOEDA=(0.4, 0.5, 1.6),      # o preço do carreto vezes (a prata do lugar ÷ a que ele tem por certa) elevado a isto, entre estes dois               # O IMPOSTO DO SENHOR: no começo de cada estação, cada povoado paga tanto da bolsa do povo ao caixa da capital (a capital vive disso e paga a guarda)
    FATOR_ESTRADA={'estrada': 0.3, 'caminho': 0.6, 'trilha': 1.0, 'fora': 0.3}, BANDO_CADA=150, PATRULHA_GUARDA=0.01, PATRULHA_MAX=0.8,
)

NOMES_A = ['Vale', 'Ponte', 'Porto', 'Alto', 'Campo', 'Fonte', 'Lagoa', 'Moinho', 'Ribeira', 'Monte', 'Passo', 'Sobral', 'Carvalhal', 'Azenha', 'Freixo', 'Juncal', 'Silveira', 'Toural', 'Barreiro', 'Outeiro']
NOMES_B = ['Fundo', 'de Cima', 'Velho', 'Novo', 'do Salgueiro', 'das Garças', 'do Lobo', 'Negro', 'da Cruz', 'das Pedras', 'do Sal', 'Claro', 'Branco', 'do Moinho', 'Grande', 'da Lebre', 'das Cabras', 'do Freixo']


# ======================= o verbo 'rota' e o arquivo 'rotas' (o que o alicerce poria no estado.py) =======================
def _rota_um(E, ef):
    R = E.setdefault('rotas', {})
    if len(ef) == 4 and ef[1] == 'nasce':
        rid, r = ef[2], copy.deepcopy(ef[3])
        if rid in R or not isinstance(r, dict) or r.get('a') not in E['lugares'] or r.get('b') not in E['lugares']: return f'rota torta: {ef}'
        if not (isinstance(r.get('blocos'), int) and 1 <= r['blocos'] <= 6) or r.get('tipo') not in TAB['CAPACIDADE']: return f'rota torta (blocos 1 a 6, tipo): {ef}'
        R[rid] = r; return None
    if len(ef) != 5 or ef[1] not in R: return f'não há a rota {ef[1:2]}'
    _, rid, campo, op, val = ef; r = R[rid]
    if op == 'poe': r[campo] = copy.deepcopy(val); return None
    if op == 'soma':
        q = r.get(campo, 0) + val
        if q < 0: return f'a rota {rid} só tem {r.get(campo, 0)} de {campo}'
        r[campo] = q; return None
    return f'rota: op {op}'


def instala():
    C.PRATELEIRA.setdefault('capital', C.PRATELEIRA['cidade']); C.PRATELEIRA_MAGIA.setdefault('capital', C.PRATELEIRA_MAGIA['cidade'])     # a capital tem a prateleira da cidade
    C.PRATELEIRA_LADINO.setdefault('capital', C.PRATELEIRA_LADINO['cidade'])
    proto_aplica.EXTRA[:] = ['rotas']; proto_aplica.EXTRA_VERBOS['rota'] = 'rotas'; proto_aplica.UM_EXTRA['rota'] = _rota_um
    for t in ('regiao', 'viagem', 'frete'):
        if t not in M.EVENTOS: M.EVENTOS.append(t)
    M.MUNDO_SOZINHO = tuple(M.MUNDO_SOZINHO) + ('regiao',)
    proto_aplica.instala()


# ======================= o gerador =======================
def _dist(a, b): return math.hypot(a[0] - b[0], a[1] - b[1])


def prata_do_mundo(E): return mercado.prata_do_mundo(E) + sum(int(l.get('bolsa') or 0) for l in E['lugares'].values())


def gera(E, semente=1):
    """a região em volta da vila de teste: devolve o resumo. Pede a vila de teste com a magia e a 4b (Pedra Rasa, a Mata do Corvo, a Cova Velha, a cripta, Vau Seco, a Serra Fria)."""
    L = E['lugares']
    for k in ('vila', 'mata', 'cova', 'cripta', 'vau', 'serra_fria'):
        if k not in L: sys.exit(f'falta {k}: a região nasce em volta da vila de teste com a magia e a 4b')
    E.setdefault('rotas', {})
    r = random.Random(f'regiao|{semente}')
    # 1. AS POSIÇÕES (o que já existe é âncora: Pedra Rasa a oeste, Vau Seco a leste, longe)
    pos = {'vila': (25, 55), 'vau': (85, 25), 'mata': (17, 66), 'cova': (30, 64), 'serra_fria': (93, 14), 'fora': (110, 60)}
    tipos = {'vila': 'vila', 'vau': 'aldeia'}; nomes_usados = {l.get('nome') for l in L.values()}
    def livre(x0, x1, y0, y1, longe=14):
        for _ in range(400):
            p = (r.uniform(x0, x1), r.uniform(y0, y1))
            if all(_dist(p, q) >= longe for q in pos.values()): return p
        return p
    def nome():
        while True:
            n = f'{r.choice(NOMES_A)} {r.choice(NOMES_B)}'
            if n not in nomes_usados: nomes_usados.add(n); return n
    novos = [('capital', livre(50, 65, 40, 60, 20))]
    pos['capital'] = novos[0][1]
    for t, nn in (('cidade', 2), ('vila', 4), ('aldeia', 7)):
        for i in range(nn):
            if t == 'cidade': p = livre(70, 95, 45, 75, 20) if i == 0 else livre(35, 60, 10, 30, 20)       # a cidade do rio (a leste, perto de fora) e a cidade do norte
            else: p = livre(5, 100, 5, 95, 12 if t == 'vila' else 10)
            k = f'{t}_{i + 1}'; pos[k] = p; novos.append((t, p)); tipos[k] = t
    tipos['capital'] = 'capital'
    # os ermos novos (as faixas): a Mata Funda (o interior, atrás da Mata do Corvo), o Pé da Serra (a borda da serra), o Brejo, a Charneca, as Grutas
    ERMOS = [('mata_funda', 'a Mata Funda', 'floresta', 2, (8, 78)), ('pe_serra', 'o Pé da Serra', 'serra', 1, (80, 15)), ('brejo', 'o Brejo das Garças', 'brejo', 2, (55, 85)),
             ('charneca', 'a Charneca', 'campo', 1, (45, 30)), ('grutas', 'as Grutas do Alto', 'caverna', 2, (88, 48)), ('borda_brejo', 'a borda do brejo', 'brejo', 1, (62, 72))]
    for k, _, _, _, p in ERMOS: pos[k] = p
    ef = []
    povs = [k for k, t in tipos.items() if k not in L]
    for k in povs:
        t = tipos[k]; nm = 'a capital' if False else nome()
        ef.append(['lugar', 'nasce', k, dict(nome=nm, em='em ' + nm, tipo=t, sobre=f'{t}')])
    for k, nm, hab, per, _ in ERMOS: ef.append(['lugar', 'nasce', k, dict(nome=nm, em=('na ' if nm.startswith('a ') else 'no ' if nm.startswith('o ') else 'nas ') + nm.split(' ', 1)[1], tipo='ermo')])
    ef.append(['lugar', 'nasce', 'fora', dict(nome='o mundo de fora', em='fora da região', tipo='fora', sobre='o fim da estrada real e do rio: daqui não se viaja para lá (etapa futura)')])
    estado.aplica(E, 'gera', ef, texto='a região nasce em volta da vila de teste')
    # 2. AS ROTAS: cada povoado aos 2 ou 3 mais perto; a árvore que liga todos; e as mais curtas até 22; e 2 para fora
    P = [k for k, t in tipos.items()]
    pares = sorted(((round(_dist(pos[a], pos[b]), 2), a, b) for i, a in enumerate(P) for b in P[i + 1:]))
    pai = {k: k for k in P}
    def raiz(x):
        while pai[x] != x: x = pai[x]
        return x
    esc = []
    for d, a, b in pares:
        if raiz(a) != raiz(b): pai[raiz(a)] = raiz(b); esc.append((d, a, b))
    grau = lambda k: sum(1 for _, x, y in esc if k in (x, y))
    for hub, quer in (('capital', 4),) + tuple((k, 3) for k, t in tipos.items() if t == 'cidade'):       # a capital é o nó das estradas; a cidade também
        for d, a, b in pares:
            if grau(hub) >= quer: break
            if hub in (a, b) and (d, a, b) not in esc and d < 45: esc.append((d, a, b))
    for d, a, b in pares:
        if len(esc) >= 22: break
        if (d, a, b) in esc: continue
        if grau(a) >= 4 or grau(b) >= 4: continue
        esc.append((d, a, b))
    ORDEM = dict(capital=3, cidade=2, vila=1, aldeia=0)
    def tipo_rota(a, b):
        x, y = sorted((ORDEM[tipos[a]], ORDEM[tipos[b]]))
        return 'estrada' if x >= 1 and y >= 2 else 'caminho' if y >= 1 else 'trilha'
    ermos_todos = ['mata', 'cova', 'serra_fria'] + [k for k, *_ in ERMOS]
    ef = []
    for i, (d, a, b) in enumerate(esc[:22]):
        mid = ((pos[a][0] + pos[b][0]) / 2, (pos[a][1] + pos[b][1]) / 2)
        er = min((e for e in ermos_todos if e != 'serra_fria'), key=lambda e: _dist(pos[e], mid)); de_ = _dist(pos[er], mid)
        ef.append(['rota', 'nasce', f'r{i + 1:02d}', dict(a=a, b=b, blocos=max(1, min(6, round(d / 7))), tipo=tipo_rota(a, b), ermo=er if de_ < 30 else None, expoe=1.0 if de_ < 12 else 0.3)])
    rio = min((k for k, t in tipos.items() if t == 'cidade'), key=lambda k: _dist(pos[k], pos['fora']))
    ef.append(['rota', 'nasce', 'r23', dict(a='capital', b='fora', blocos=6, tipo='fora', ermo=None, nome='a estrada real')])
    ef.append(['rota', 'nasce', 'r24', dict(a=rio, b='fora', blocos=5, tipo='fora', ermo=None, nome='o rio')])
    # 3. OS ERMOS NOVOS: povoados pela tabela da caça (o povoa é o do caca.py: aqui os efeitos à mão, iguais); o vizinho é o povoado mais perto (e os outros a até 18)
    for k, nm, hab, per, p in ERMOS:
        fa = K.fauna(hab, per); ma = K.materia(hab, per)
        ef += [['lugar', k, 'habitat', 'poe', hab], ['lugar', k, 'perigo', 'poe', per], ['lugar', k, 'teto', 'poe', dict(fa)], ['lugar', k, 'bichos', 'poe', dict(fa)],
               ['lugar', k, 'coleta_teto', 'poe', dict(ma)], ['lugar', k, 'coleta', 'poe', dict(ma)], ['lugar', k, 'longe', 'poe', 1 if per == 1 else 3]]
    estado.aplica(E, 'gera', ef, texto='as rotas e os ermos novos')
    viz = {}
    for e in [k for k, *_ in ERMOS]:
        perto = sorted(povs + ['vila', 'vau'], key=lambda q: _dist(pos[q], pos[e]))
        for q in perto[:3]:
            if _dist(pos[q], pos[e]) < 22 or q == perto[0]: viz.setdefault(q, []).append(e); viz.setdefault(e, []).append(q)
    viz.setdefault('vila', []).append('mata_funda'); viz.setdefault('mata_funda', []).append('vila')
    ef = []
    for k, vs in viz.items():
        atual = list(E['lugares'][k].get('vizinhos') or []); novo = atual + [v for v in vs if v not in atual]
        if novo != atual: ef.append(['lugar', k, 'vizinhos', 'poe', novo])
    estado.aplica(E, 'gera', ef, texto='os ermos ganham vizinhos')
    # 4. OS MERCADOS (o funda de sempre) e o perfil de cada povoado (o que produz a mais e a menos), as oficinas, as runas, a botica e o santuário, a bolsa do povo
    for k in povs:
        t = tipos[k]; T_ = TAB['TIPOS'][t]
        mercado.funda(E, k, T_['pop'], prateleira_=bool(T_['prat']), como='a região nasce')
    mercado.funda(E, 'fora', TAB['FORA']['pop'], prata=TAB['FORA']['caixa'], prateleira_=False, como='o mundo de fora')
    ef = []
    for k in povs:
        t = tipos[k]; T_ = TAB['TIPOS'][t]; l = E['lugares'][k]; mult = dict(TAB['PERFIL'][t])
        habs = {E['lugares'][v].get('habitat') for v in viz.get(k, [])}
        for h in habs:
            for b, x in TAB['PERFIL_ERMO'].get(h, {}).items(): mult[b] = mult.get(b, 1) * x
        prod = {}
        for b, q in (l.get('produz') or {}).items():
            n, c = M.le_materia(b); chave = b if b in mult else (f'{n}:0' if c and f'{n}:0' in mult and n in ('metal', 'madeira', 'couro') else None)
            prod[b] = q * mult.get(b, mult.get(chave, 1) if chave and c else 1)
        # O BALANÇO: o lugar novo vende o que faz a mais pelo que compra a menos (ao preço de base); a especialidade dele fecha a conta
        esp = [b for b in TAB['ESPECIALIDADE'][t] if b in prod] or ['comida']
        bal = sum((prod[b] - T_['pop'] * C.consumo(b)) * C.base(b) for b in prod)
        val_esp = sum(prod[b] * C.base(b) for b in esp)
        x = max(0.3, 1 - bal / val_esp) if val_esp else 1
        for b in esp: prod[b] *= x
        for b, q in prod.items():
            if abs(q - (l.get('produz') or {}).get(b, 0)) > 1e-6: ef.append(['lugar', k, 'produz.' + b, 'poe', round(q, 4)])
        if T_['oficina'] is not None:
            ef += [['lugar', k, 'oficina', 'poe', T_['oficina']], ['lugar', k, 'preparo', 'poe', dict(fogo=T_['alcance'], bigorna=T_['alcance'])]]
        for campo in ('runas', 'botica', 'santuario'):
            if T_[campo] is not None: ef.append(['lugar', k, campo, 'poe', T_[campo]])
        ef.append(['lugar', k, 'bolsa', 'poe', T_['pop'] * TAB['BOLSA_CABECA']])
    ef.append(['lugar', 'vila', 'bolsa', 'poe', 400 * TAB['BOLSA_CABECA']]); ef.append(['lugar', 'vau', 'bolsa', 'poe', 120 * TAB['BOLSA_CABECA']])
    estado.aplica(E, 'gera', ef, texto='o perfil, as oficinas e a bolsa do povo')
    # a forja mestra fica longe: na aldeia mais perto do Pé da Serra (a aldeia dos ferreiros da serra)
    mestra = min((k for k in povs if tipos[k] == 'aldeia'), key=lambda k: _dist(pos[k], pos['pe_serra']))
    estado.aplica(E, 'gera', [['lugar', mestra, 'oficina', 'poe', 4], ['lugar', mestra, 'preparo', 'poe', dict(fogo=4, bigorna=4)], ['lugar', mestra, 'sobre', 'poe', 'a aldeia dos ferreiros da serra: a forja mestra']], texto='a forja mestra')
    for k in povs:
        if TAB['TIPOS'][tipos[k]]['botica'] is not None or TAB['TIPOS'][tipos[k]]['santuario'] is not None: mercado.funda_magia(E, k, como='a região nasce')
    # 5. AS MASMORRAS NOVAS (7): perto dos ermos, a categoria sobe com a distância de Pedra Rasa
    MM = [('mina', 'pe_serra', 1), ('mina', 'grutas', 2), ('ruína', 'charneca', 1), ('ruína', 'brejo', 3), ('toca', 'borda_brejo', 0), ('toca', 'mata_funda', 1), ('cripta', 'cova', 1)]
    nm_m = ['a Mina Velha', 'a Mina Funda', 'as Ruínas da Charneca', 'a Torre Afogada', 'a Toca do Brejo', 'a Toca da Mata Funda', 'o Ossário do Monte']
    for (molde, perto, cat), nm in zip(MM, nm_m):
        efm = masmorra.gera(E, molde, nm, perto, cat=cat, longe=1, niveis={0: 1, 1: 2, 2: 2, 3: 1}[cat])
        estado.aplica(E, 'gera', efm, onde=perto, texto=f'{nm}, uma masmorra ({molde})')
    # 6. OS BANDOS (salteadores contados num ermo): dois, nos ermos mais longe de Pedra Rasa que alguma rota cruza
    cruzados = sorted({rt['ermo'] for rt in E['rotas'].values() if rt.get('ermo') and rt['ermo'] not in ('mata', 'cova')}, key=lambda e: -_dist(pos[e], pos['vila']))
    ef = [['lugar', e, 'bando', 'poe', r.randint(*TAB['BANDO_INICIAL'])] for e in cruzados[:2]]
    if ef: estado.aplica(E, 'gera', ef, texto='os bandos de salteadores')
    E['_pos'] = pos; E['_tipos'] = tipos
    return dict(povoados=len(tipos), ermos=len(ermos_todos), rotas=len(E['rotas']), masmorras=sum(1 for l in E['lugares'].values() if l.get('tipo') == 'masmorra'), mestra=mestra)


# ======================= o fluxo da prata (o preço vezes a prata que o lugar tem, sobre a que tem por certa) =======================
def moeda(E, lid, caixa=None):
    """A PRATA QUE FALTA BARATEIA: o lugar com menos prata que a dele vende mais barato, e o que tem mais, mais caro. O lugar sem bolsa (o save antigo, a vila de teste
    sem a região) conta só o caixa contra 5 por pessoa: no começo, 1"""
    l = E['lugares'][lid]; pop = mercado.povo(E, lid)
    if not pop or not TAB['MOEDA'][0]: return 1.0
    cx = l['estoque'].get('prata', 0) if caixa is None else caixa
    if lid == 'fora': alvo_, tem = TAB['FORA']['caixa'], cx
    elif l.get('bolsa') is None: alvo_, tem = C.PRATA_CABECA * pop, cx
    else: alvo_, tem = TAB['PRATA_CABECA_ALVO'] * pop, cx + int(l.get('bolsa') or 0)
    return max(TAB['MOEDA'][1], min(TAB['MOEDA'][2], (max(1, tem) / max(1, alvo_)) ** TAB['MOEDA'][0]))


def moeda_na_loja():
    """(a proposta) o fluxo da prata vale também na loja: o lote e o preço do dia saem vezes a moeda do lugar"""
    if getattr(mercado, '_moeda', False): return
    lote0, preco0 = mercado.lote, mercado.preco
    mercado.lote = lambda E, lid, bem, n, compra=True: lote0(E, lid, bem, n, compra) * moeda(E, lid)
    mercado.preco = lambda E, lid, bem: (lambda v: None if v is None else v * moeda(E, lid))(preco0(E, lid, bem))
    mercado._moeda = True


def monta(sem, prata_eu=2000):
    """(a medida) carrega a cópia do ensaio (MOTOR10_MUNDO), põe a região pela semente e liga o dia da região; devolve E"""
    E = estado.carrega(); E['rotas'] = {}; E['relogio']['semente'] = 1000 + sem; MEDE.pop('safra', None)
    if prata_eu: estado.aplica(E, 'mestre', [['pessoa', 'eu', 'moedas', 'soma', prata_eu]], quem=['eu'], texto='(medida) a bolsa do personagem')
    gera(E, sem)
    class _Mod: pass
    REG = _Mod(); REG.__name__ = 'proto_regiao'; REG.virada = virada
    estado.modulos(); estado._MODS[:] = [m for m in estado._MODS if getattr(m, '__name__', '') != 'proto_regiao'] + [REG]
    return E


# ======================= o dia da região =======================
MEDE = dict(razoes=[], carreto=0)      # (só a medida) as razões de preço de loja entre vizinhos antes do carreto; a prata que o carreto moveu
def _peso(b): n, _ = M.le_materia(b); return TAB['PESO'].get(n, TAB['PESO'].get(b, 1))
BENS = [b for b in C.bens() if M.le_materia(b)[1] in (None, 0, 1)]
def guardas(E, lid): l = E['lugares'][lid]; return int((l.get('pop') or 0) * TAB['TIPOS'].get(l.get('tipo'), {}).get('guarda', 0))


def perigo_rota(E, rt):
    """(a chance de encontro de bicho por bloco, a de bando por bloco) da rota, da contagem do ermo que ela cruza e do bando dele, menos a patrulha"""
    er = E['lugares'].get(rt.get('ermo')) if rt.get('ermo') else None
    if not er: return 0.0, 0.0
    a = min(K.ACASO_MAX, sum(q * K.indole(e)[0] for e, q in (er.get('bichos') or {}).items() if q >= 1 and not (estado.especie(e) or {}).get('chefe')) / K.ACASO_CADA) * TAB['FATOR_ESTRADA'][rt['tipo']] * rt.get('expoe', 1.0)
    pat = min(TAB['PATRULHA_MAX'], (guardas(E, rt['a']) + guardas(E, rt['b'])) * TAB['PATRULHA_GUARDA'] / rt['blocos']) if rt['a'] in E['lugares'] and rt['b'] in E['lugares'] else 0
    return a, (er.get('bando') or 0) / TAB['BANDO_CADA'] * (1 - pat) * rt.get('expoe', 1.0)


def virada(E):
    """o dia da região: UM evento ('regiao') com tudo o que o povo fez no dia; e, uma vez por semana, um segundo (o bicho que sai, a fome, a migração, o bando)"""
    dia = E['relogio']['dia']; ef = []; Ls = E['lugares']; rs = estado.sorte(E, 'regiao|dia')
    est = {lid: dict(l['estoque']) for lid, l in Ls.items() if mercado.tem_mercado(E, lid)}
    bolsa = {lid: int(l.get('bolsa') or 0) for lid, l in Ls.items()}
    mo = {lid: moeda(E, lid, est[lid].get('prata', 0)) for lid in est}
    fome_ = {lid: est[lid].get('comida', 0) < 2 * TAB['FOME_DIAS'] * max(1, mercado.povo(E, lid)) for lid in est}
    def preco(lid, b):
        a = mercado.alvo(E, lid, b); s = est[lid].get(b, 0)
        m = 1 if (b == 'comida' and fome_[lid] and mo[lid] < 1) else mo[lid]          # NA FOME O PÃO NÃO BARATEIA: o lugar com fome paga a comida pelo preço da falta, tenha a prata que tiver
        return C.base(b) * mercado.fator_de(a, s) * (m if TAB['MOEDA'][0] else 1)
    def mexe(lid, b, q): est[lid][b] = est[lid].get(b, 0) + q; ef.append(['estoque', lid, b, 'soma', q])
    # 0. A SAFRA DO ANO: no começo do ano, cada povoado tira a colheita dele (a região inteira, e um pouco de cada lugar); o mercado colheu hoje pela tabela: aqui entra a diferença
    if (dia - 1) % M.ANO == 0 or 'safra' not in MEDE:
        rr = estado.sorte(E, f'regiao|safra|{(dia - 1) // M.ANO}'); reg = rr.uniform(*TAB['SAFRA_REGIAO'])
        MEDE['safra'] = {lid: round(reg * rr.uniform(*TAB['SAFRA_LUGAR']), 3) for lid in sorted(est) if lid != 'fora'}
    ontem = max(1, dia - 1); e_ = ((ontem - 1) % M.ANO) // M.ESTACAO
    for lid, sf in MEDE['safra'].items():
        q = (Ls[lid].get('produz') or {}).get('comida', 0)
        if lid == 'vila' and not TAB['SAFRA_NA_VILA']: continue
        x = q * max(C.RESPOSTA[0], min(C.RESPOSTA[1], mercado.fator(E, lid, 'comida'))) * M.COLHEITA[e_] * (sf - 1)
        n = int(x) if x >= 0 else -min(int(-x), int(est[lid].get('comida', 0)))
        if n: mexe(lid, 'comida', n)
    # 1. O CARRETO DO POVO: em cada rota, nos dois sentidos, o bem vai de onde é barato para onde é caro, se a diferença paga o frete
    for rid, rt in sorted(E.get('rotas', {}).items()):
        A, B = rt['a'], rt['b']
        if A not in est or B not in est: continue
        pa_, pb_ = perigo_rota(E, rt); cap = TAB['CAPACIDADE'][rt['tipo']] * (1 - min(0.9, 4 * pb_)); usado = 0
        for b in BENS:
            for de, para in ((A, B), (B, A)):
                po, pd = preco(de, b), preco(para, b); f = TAB['FRETE'] * _peso(b) * rt['blocos']
                rz = (C.base(b) * mercado.fator_de(mercado.alvo(E, para, b), est[para].get(b, 0))) / max(1e-9, C.base(b) * mercado.fator_de(mercado.alvo(E, de, b), est[de].get(b, 0)))
                MEDE['razoes'].append(rz) if rz > 1 else None
                gap = pd - po - f - TAB['MARGEM'] * po
                if gap <= 0: continue
                q = TAB['FLUXO'] * min(mercado.alvo(E, de, b), mercado.alvo(E, para, b)) * gap / pd
                q = min(q, est[de].get(b, 0) - TAB['PISO'] * mercado.alvo(E, de, b), (cap - usado) / _peso(b), est[para].get('prata', 0) / ((po + pd) / 2))
                q = mercado._inteiro(E, q, f'regiao|carreto|{rid}|{de}|{b}') if q > 0 else 0       # a parte quebrada é a chance de mais uma (o mercado pequeno também é servido)
                if q < 1: continue
                v = int(q * (po + pd) / 2)
                if v < 1: continue
                mexe(de, b, -q); mexe(para, b, q); mexe(para, 'prata', -v); mexe(de, 'prata', v); usado += q * _peso(b); MEDE['carreto'] += v
    # 2. O CAIXA E A BOLSA se acertam; 3. A FREGUESIA compra da prateleira; 4. A FORJA DO POVO refaz a prateleira; 5. A CAÇA DO POVO
    for lid in sorted(est):
        l = Ls[lid]
        if lid == 'fora': continue
        pop = mercado.povo(E, lid); alvo_c = TAB['BOLSA_CABECA'] * pop; cx = est[lid].get('prata', 0)
        d = int(TAB['RELAXA'] * (alvo_c - cx))
        d = min(d, bolsa[lid]) if d > 0 else -min(-d, cx)
        if d: mexe(lid, 'prata', d); bolsa[lid] -= d; ef.append(['lugar', lid, 'bolsa', 'soma', -d])
        prat = mercado.prateleira(E, lid); quer = mercado.alvo_pecas(E, lid)
        for cat, taxa in TAB['FREGUES'].items():
            n = mercado._inteiro(E, pop * taxa, f'regiao|{lid}|fregues|{cat}')
            pecas = sorted(i for i, it in prat.items() if it['cat'] == cat and it['tipo'] in ('arma', 'armadura', 'escudo'))
            for _ in range(n):
                if not pecas: break
                iid = pecas.pop(rs.randrange(len(pecas))); v = mercado.preco_peca(prat[iid])
                if bolsa[lid] < v: break
                ef += [['item', iid, 'some'], ['lugar', lid, 'bolsa', 'soma', -v]]; mexe(lid, 'prata', v); bolsa[lid] -= v; del prat[iid]
        if l.get('oficina') is not None and quer:
            alc = min(1, (l.get('preparo') or {}).get('fogo', 0) if isinstance(l.get('preparo'), dict) else 0)
            import oficio
            for cat in range(alc + 1):
                tem = sum(1 for it in prat.values() if it['cat'] == cat); falta = int(quer.get(cat, 0)) - tem
                if falta <= 0: continue
                n = min(falta, mercado._inteiro(E, pop * TAB['FORJA_POVO'][cat], f'regiao|{lid}|forja|{cat}'))
                base_ = [x for x in C.prateleira_de(l.get('tipo')) if x[2] == cat]
                for _ in range(n):
                    if not base_: break
                    tipo, qual, c, cobre = rs.choice(base_)
                    it = itens.item(tipo, c, familia=qual if tipo == 'arma' else None, material=qual if tipo == 'armadura' else None, cobre=cobre, onde=lid)
                    mat = oficio.materia_de(dict(it, cat=c))
                    if any(est[lid].get(k, 0) < q for k, q in mat.items()): continue
                    for k, q in mat.items(): mexe(lid, k, -q)
                    ef.append(['item', 'nasce', it])
        nc = int(pop * TAB['TIPOS'].get(l.get('tipo'), {}).get('cacador', 0))
        if nc:
            for er in [v for v in (l.get('vizinhos') or []) if Ls.get(v, {}).get('perigo') == 1 and caca.tem_caca(E, v)]:
                B = {e: q for e, q in caca.bichos_de(E, er).items() if e in TAB['PRESAS'] and q >= 2}
                n = mercado._inteiro(E, nc * TAB['CACA_POVO'], f'regiao|{lid}|caca|{er}')
                for _ in range(n):
                    if not B: break
                    e = rs.choices(sorted(B), weights=[B[x] for x in sorted(B)])[0]; B[e] -= 1
                    if B[e] < 2: del B[e]
                    ef.append(['lugar', er, f'bichos.{e}', 'soma', -1])
                    for bem, q in bichos.despojo(e, rs)[0].items(): mexe(lid, bem, q)
                break
    # 6. A COMIDA QUE ESTRAGA na carga de quem a leva
    for pid, p in E['gente'].items():
        q = (p.get('carga') or {}).get('comida', 0)
        if p.get('estado') == 'vivo' and q >= 1:
            n = min(q, mercado._inteiro(E, q * TAB['ESTRAGA'], f'regiao|{pid}|estraga'))
            if n: ef.append(['pessoa', pid, 'carga.comida', 'soma', -n])
    ef = _junta(ef)
    if ef: estado.aplica(E, 'regiao', ef, texto=f'o dia da região ({dia})')
    if dia % M.SEMANA == 0: semana(E)
    if dia % M.ESTACAO == 1 and dia > 1: imposto(E)


def imposto(E):
    """o imposto do senhor, no começo da estação: a bolsa de cada povoado paga ao caixa da capital"""
    Ls = E['lugares']; cap = next((k for k, l in Ls.items() if l.get('tipo') == 'capital'), None); ef = []; tot = 0
    if not cap: return
    for k, l in sorted(Ls.items()):
        if k in (cap, 'fora') or not mercado.tem_mercado(E, k): continue
        v = int((l.get('bolsa') or 0) * TAB['IMPOSTO'])
        if v > 0: ef += [['lugar', k, 'bolsa', 'soma', -v], ['estoque', cap, 'prata', 'soma', v]]; tot += v
    if ef: estado.aplica(E, 'regiao', _junta(ef), texto=f'o imposto da estação: {tot} de prata para {Ls[cap]["nome"]}')


def _junta(ef):
    """soma os efeitos de estoque e de bolsa iguais (o mesmo lugar, o mesmo bem): o registro guarda o que mudou no dia, não cada carroça"""
    soma = {}; resto = []
    for x in ef:
        if x[0] == 'estoque' or (x[0] == 'lugar' and x[2] == 'bolsa' and x[3] == 'soma') or (x[0] == 'lugar' and x[2].startswith('bichos.') and x[3] == 'soma'):
            k = (x[0], x[1], x[2]); soma[k] = soma.get(k, 0) + x[4]
        else: resto.append(x)
    return [[k[0], k[1], k[2], 'soma', v] for k, v in soma.items() if v] + resto


def semana(E):
    """a semana: o bicho que sai do ermo, a fome e a migração, o bando"""
    Ls = E['lugares']; ef = []; rs = estado.sorte(E, 'regiao|semana'); txt = []
    inverno = estado.estacao(E) == 'inverno'
    # o bicho que sai: o predador com fome (a presa rareou), ou no inverno, desce ao povoado vizinho
    for er, l in sorted(Ls.items()):
        if l.get('tipo') != 'ermo' or not caca.tem_caca(E, er): continue
        B = caca.bichos_de(E, er); T_ = caca.teto_de(E, er)
        presa = sum(B.get(e, 0) for e in TAB['PRESAS']); teto_p = sum(T_.get(e, 0) for e in TAB['PRESAS'])
        fome = (max(0.0, 1 - presa / teto_p) if teto_p else 0.0) + (TAB['INVERNO'] if inverno else 0)        # onde a presa não é contada (a serra), o bicho só desce no inverno
        povs = [v for v in (l.get('vizinhos') or []) if mercado.tem_mercado(E, v)]
        if not povs: continue
        for e, P in TAB['PREDADORES'].items():
            n = B.get(e, 0)
            if n < 1 or rs.random() >= min(0.9, n * K.indole(e)[0] * fome * TAB['SAI']): continue
            v = rs.choice(povs); gado = min(int(Ls[v]['estoque'].get('comida', 0)), P['gado'] * max(1, n // 3))
            if gado: ef.append(['estoque', v, 'comida', 'soma', -gado])
            if rs.random() < P['mata'] and Ls[v].get('pop', 0) > 1: ef.append(['lugar', v, 'pop', 'soma', -1])
            mortos = 1 if rs.random() < min(TAB['GUARDA_MATA_MAX'], 0.1 + guardas(E, v) * 0.005) else 0
            if mortos: ef.append(['lugar', er, f'bichos.{e}', 'soma', -mortos])
            txt.append(f"{TB.ESPECIES[e]['nome']} desce de {l['nome']} a {Ls[v]['nome']}: leva {gado} de gado" + (f', a guarda mata {mortos}' if mortos else ''))
    # a fome e a migração: sai quem passa fome, e quem é pobre (a prata por cabeça abaixo da metade da média da região); vai para o vizinho por rota que está melhor, até 2% do povo dele por semana
    povs = [k for k in sorted(Ls) if mercado.tem_mercado(E, k) and k != 'fora']
    pc = {k: ((Ls[k]['estoque'].get('prata', 0) + int(Ls[k].get('bolsa') or 0)) / max(1, Ls[k]['pop'])) for k in povs}; media = sum(pc.values()) / max(1, len(pc))
    chegou = {}
    for lid in povs:
        l = Ls[lid]; pop = mercado.povo(E, lid)
        dias = l['estoque'].get('comida', 0) / pop; bolsa = int(l.get('bolsa') or 0); sai = 0; morre = 0
        if dias < TAB['FOME_DIAS']:
            morre = mercado._inteiro(E, pop * TAB['FOME_MORRE'], f'regiao|{lid}|morre'); sai = mercado._inteiro(E, pop * TAB['FOME_SAI'], f'regiao|{lid}|sai'); txt.append(f"{l['nome']} passa fome")
        elif pc[lid] < TAB['POBRE'] * media: sai = mercado._inteiro(E, pop * TAB['POBRE_SAI'], f'regiao|{lid}|pobre')
        if not (sai or morre): continue
        vizs = [rt['b'] if rt['a'] == lid else rt['a'] for rt in E['rotas'].values() if lid in (rt['a'], rt['b'])]
        vizs = [v for v in vizs if v in pc and pc[v] > pc[lid] and Ls[v]['estoque'].get('comida', 0) / Ls[v]['pop'] >= TAB['FOME_DIAS']]
        if not vizs and not morre: continue
        dest = max(vizs, key=lambda v: pc[v]) if vizs else None
        if dest: sai = min(sai, max(0, int(Ls[dest]['pop'] * TAB['CHEGA_MAX']) - chegou.get(dest, 0)))
        else: sai = 0
        bando = int(sai * TAB['BANDO_PARTE']) if dias < TAB['FOME_DIAS'] else 0; vai = sai - bando; leva = int(bolsa * sai / pop)
        if not (sai or morre): continue
        ef.append(['lugar', lid, 'pop', 'soma', -(sai + morre)])
        for b, q in (l.get('produz') or {}).items(): ef.append(['lugar', lid, 'produz.' + b, 'poe', round(q * ((pop - sai - morre) / pop) ** (TAB['TERRA'] if b in C.SAFRA else 1), 4)])
        if leva and dest: ef += [['lugar', lid, 'bolsa', 'soma', -leva], ['lugar', dest, 'bolsa', 'soma', leva]]
        if vai and dest:
            pd = mercado.povo(E, dest) + chegou.get(dest, 0); chegou[dest] = chegou.get(dest, 0) + vai; ef.append(['lugar', dest, 'pop', 'soma', vai])
            for b, q in (Ls[dest].get('produz') or {}).items(): ef.append(['lugar', dest, 'produz.' + b, 'poe', round(q * ((pd + vai) / mercado.povo(E, dest)) ** (TAB['TERRA'] if b in C.SAFRA else 1), 4)])
        if bando:
            er = next((v for v in (l.get('vizinhos') or []) if Ls.get(v, {}).get('tipo') == 'ermo'), None)
            if er: ef.append(['lugar', er, 'bando', 'poe', int(Ls[er].get('bando') or 0) + bando])
        if sai or morre: txt.append((f"{sai} deixam {l['nome']} por {Ls[dest]['nome']}" if sai else '') + (f' ({bando} vão para o mato)' if bando else '') + (f'; {morre} morrem de fome' if morre else ''))
    # o bando: a patrulha dos povoados vizinhos mata, e chega gente (da fome e da pobreza dos povoados vizinhos, e de fora): o bando não some de vez
    for er, l in sorted(Ls.items()):
        if l.get('bando') is None: continue
        n = int(l.get('bando') or 0); vz = [v for v in (l.get('vizinhos') or []) if mercado.tem_mercado(E, v)]
        g = sum(guardas(E, v) for v in vz); k = 1 if n > 0 and rs.random() < min(0.5, g * TAB['PATRULHA_MATA']) else 0
        pobre = any(pc.get(v, media) < TAB['POBRE'] * media for v in vz)
        chega = 1 if n < TAB['BANDO_TETO'] and rs.random() < TAB['BANDO_CHEGA'] + (0.2 if pobre else 0) else 0
        if k or chega:
            ef.append(['lugar', er, 'bando', 'poe', max(0, n - k + chega)])
            if k: txt.append(f"a patrulha mata {k} do bando {estado.de(E, er)}")
    if ef: estado.aplica(E, 'regiao', _junta(ef), texto='a semana da região: ' + ('; '.join(txt) or 'nada'))
