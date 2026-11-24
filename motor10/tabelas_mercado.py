"""tabelas_mercado.py — MOTOR 10: TODOS os números do mercado num lugar só (o preço, o povo que come, o lugar que produz, as peças da loja).

Os números do mundo moram no tabelas_mundo.py (a estação, a colheita, o preço de tabela das peças, o salário); os da luta e dos itens, no tabelas.py.
Mudar o mercado é mudar esta página e rodar `provas_mercado.py` (ou `provas_mundo.py`, que o chama).
"""
import tabelas as T
import tabelas_mundo as M

# ---------- o preço de um bem ----------
# preço do dia = base × √(alvo ÷ estoque), entre FATOR_MIN e FATOR_MAX vezes a base. O alvo são tantos dias de consumo do lugar.
FATOR_MIN = 0.4
FATOR_MAX = 3.0
COMPRA = 1.10               # comprar custa isto vezes o preço
PAGA = 0.60                 # a loja paga esta fração do preço a quem é Leigo em comércio...
PAGA_GRAU = 0.05            # ... e isto a mais por grau de maestria de comércio de quem vende (Iniciante 65% ... Lendário 80%)
# a prata é inteira: a compra arredonda para cima, a venda para baixo (a loja arredonda a favor dela). Venda que não chega a 1 de prata é recusada.

# o preço de base, em prata, de uma unidade (a comida é a refeição: uma unidade alimenta uma pessoa por um dia)
BASE = {'comida': M.REFEICAO_PRECO, 'lenha': 1, 'carvão': 2, 'sal': 3, 'pano': 5, 'remédio': 8, 'ferramenta': 12}
BASE_MATERIA = dict(metal=3, couro=2, osso=1, madeira=2, erva=2)       # a matéria Comum...
MATERIA_VEZES = M.PECA_VEZES                                            # ... vezes isto a cada categoria (como as peças): metal Comum 3, Incomum 18, Raro 108


def base(bem):
    """o preço de base de um bem ou de uma matéria ("metal:1"), ou None se a loja não sabe o que é"""
    if bem in BASE: return BASE[bem]
    nome, cat = M.le_materia(bem)
    if cat is None or nome not in BASE_MATERIA or cat > M.MATERIA_ATE: return None
    return BASE_MATERIA[nome] * MATERIA_VEZES ** cat


def bens():
    """todos os bens que a loja negocia, na ordem da mesa: os sete bens, depois a matéria por categoria"""
    return list(BASE) + [M.materia(n, c) for c in range(M.MATERIA_ATE + 1) for n in BASE_MATERIA]


def parte(maestria): return min(PAGA + PAGA_GRAU * 4, PAGA + PAGA_GRAU * max(0, maestria) / 2)     # a fração do preço que a loja paga a quem tem esta maestria de comércio (0 a 8)


# ---------- o povo que consome (por cabeça, por dia) ----------
CONSUMO = {'comida': 1.0, 'lenha': 0.25, 'carvão': 0.02, 'sal': 0.02, 'pano': 0.01, 'remédio': 0.005, 'ferramenta': 0.005}
CONSUMO_MATERIA = dict(metal=0.01, couro=0.01, osso=0.005, madeira=0.02, erva=0.01)       # a matéria Comum (o ferreiro, o coureiro e o curandeiro do povo)...
CONSUMO_CAT = 6                                                                           # ... dividida por isto a cada categoria
CONSUMO_ESTACAO = {'lenha': [1, 0.75, 1, 1.5]}  # o consumo que muda com a estação (primavera, verão, outono, inverno): no inverno queima-se metade a mais de lenha


def consumo(bem):
    """o que UMA pessoa gasta deste bem por dia (0 se o povo não o gasta)"""
    if bem in CONSUMO: return CONSUMO[bem]
    nome, cat = M.le_materia(bem)
    if cat is None or nome not in CONSUMO_MATERIA or cat > M.MATERIA_ATE: return 0
    return CONSUMO_MATERIA[nome] / CONSUMO_CAT ** cat


ALVO_DIAS = 30              # o alvo do estoque: tantos dias de consumo do lugar...
ALVO_DIAS_BEM = {'comida': 60}      # ... menos a comida, que se colhe uma vez por ano: o celeiro tem de atravessar o inverno e a entressafra
ALVO_MIN = 1                # o alvo nunca é menor que isto (lugar pequeno, matéria rara)
def alvo_dias(bem): return ALVO_DIAS_BEM.get(bem, ALVO_DIAS)

# ---------- o lugar que produz ----------
# lugar.produz = {bem: quanto por dia}. TODA produção acompanha o preço; a COLHEITA, além disso, segue a estação (tabelas_mundo.COLHEITA: × 0,5 · 1 · 2,5 · 0).
RESPOSTA = (0.5, 2.0)       # a produção do dia é a de tabela vezes o fator do preço, entre estes dois (falta: o povo dobra o serviço; sobra: corta pela metade)
SAFRA = ('comida',)         # os bens que são colheita: a produção do dia é, além disso, vezes a estação
CELEIRO_DIAS = 47           # os dias de comida que um lugar equilibrado tem no celeiro no fim do inverno: o ponto em que o ciclo do ano se repete igual
                            # (é com isto que o gerador abre um mercado no Dia 1; mudou o alvo, a resposta ou a colheita, este número se mede de novo)
PRODUZ_ATE = 1              # o povo de um lugar tira matéria até o Incomum; a Rara vem do ermo e da masmorra, pela mão de quem foi buscar
PRATA_CABECA = 5            # a prata de um lugar quando o gerador abre o mercado: isto por pessoa (aldeia de 120: 600; vila de 400: 2.000; cidade de 1.500: 7.500)


def celeiro_dias(dia):
    """os dias de comida no celeiro de um lugar equilibrado (a produção de tabela igual ao consumo) no começo deste dia do mundo: o ciclo do ano, andado desde o fim do inverno"""
    d = CELEIRO_DIAS; a = alvo_dias('comida')
    for t in range(1, (dia - 1) % M.ANO + 1):
        f = FATOR_MAX if d <= 0 else max(FATOR_MIN, min(FATOR_MAX, (a / d) ** 0.5))
        d = max(0, d + M.COLHEITA[(t - 1) // M.ESTACAO] * max(RESPOSTA[0], min(RESPOSTA[1], f)) - 1)
    return d


# ---------- as peças da loja (itens do Livro de Itens com "onde" no lugar e sem dono) ----------
def preco_peca(cat): return M.PECA_BASE * M.PECA_VEZES ** cat      # o preço de tabela da peça nova: 30 a Comum, vezes 6 por categoria (é o da espada: tabelas_mundo.PECA_DE_TABELA)
SUCATA = 0.10               # a peça quebrada (durabilidade 0) vale esta fração do preço de tabela; e nenhuma peça vale menos que isto
# a peça gasta vale o preço de tabela menos o conserto que ela pede (tabelas_mundo.CONSERTO_PONTO: 2% do preço por ponto gasto)
# a peça sob medida vale como uma categoria abaixo (tabelas.NAO_E_DELE): na mão de outro é isso que ela rende
# a armadura vale pelo que cobre (tabelas_mundo.PARTE_PESO): o preço de tabela é o da que cobre tronco, braços e pernas; o elmo vale um quarto; a manga, um quarto
# a arma vale pela matéria que leva (tabelas_mundo.MATERIA_ARMA): o preço de tabela é o da espada (3 unidades); a adaga (1) vale um terço; o montante (5), cinco terços; o escudo (3), o de tabela
# a loja negocia peças até o Épico (tabelas_mundo.PECA_LOJA_ATE); núcleo não se negocia em loja
FARTA = 0.8                 # A LOJA FARTA: a loja paga isto vezes por cada peça IGUAL (mesmo tipo, mesma família ou material, mesma categoria; o recorte não conta) que já tem na prateleira,
                            # E TAMBÉM isto vezes por cada peça DA MESMA CATEGORIA que a prateleira tem ACIMA DO ALVO do lugar (lugar.alvo_pecas: o que o gerador pôs na prateleira
                            # ao abrir a loja, por categoria; categoria sem alvo: zero). Com uma igual, 80% do que pagaria; com cinco, um terço (1 desliga a regra).
                            # O que ela PEDE pela peça não muda. Quem compra da prateleira abre espaço de novo.


def valor_peca(cat, dur, dur_max, sob_medida=False, peso=1.0):
    """o valor de uma peça (antes de arredondar): o preço da categoria vezes o tamanho dela (tabelas_mundo.peso_da_peca: a armadura vale pelo que cobre;
    a arma e o escudo, pela matéria que levam), menos o conserto que ela pede; quebrada, a sucata"""
    p = preco_peca(cat) * peso / (M.PECA_VEZES ** T.NAO_E_DELE if sob_medida else 1)
    if dur <= 0: return p * SUCATA
    return p * max(SUCATA, 1 - M.CONSERTO_PONTO * (dur_max - dur))


# a prateleira com que o gerador abre a loja, por tipo de lugar: (tipo, família ou material, categoria, cobre)
_COMUNS = [('arma', 'adaga', 0, None), ('arma', 'espada', 0, None), ('arma', 'maça', 0, None), ('arma', 'machado', 0, None), ('arma', 'lança', 0, None), ('arma', 'arco', 0, None),
           ('armadura', 'couro', 0, None), ('armadura', 'couro', 0, ['cabeça']), ('armadura', 'malha', 0, None), ('armadura', 'malha', 0, ['cabeça']), ('escudo', None, 0, None)]
_INCOMUNS = [('arma', 'espada', 1, None), ('arma', 'lança', 1, None), ('armadura', 'couro', 1, None), ('escudo', None, 1, None)]
# (o que o gerador põe aqui, por categoria, é também o ALVO de peças do lugar: a vila, 11 Comuns e 4 Incomuns; a cidade, 11 e 9)
PRATELEIRA = dict(vila=_COMUNS + _INCOMUNS,
                  cidade=_COMUNS + _INCOMUNS + [('arma', 'machado', 1, None), ('arma', 'arco', 1, None), ('arma', 'montante', 1, None), ('armadura', 'malha', 1, None), ('armadura', 'malha', 1, ['cabeça'])])
def prateleira_de(tipo): return PRATELEIRA.get(tipo, PRATELEIRA['vila'])        # a prateleira com que nasce a loja de um lugar deste tipo
def alvo_pecas(tipo):
    """{categoria: quantas peças} a loja de um lugar deste tipo quer ter na prateleira: o que o gerador põe nela ao abrir a loja"""
    quer = {}
    for _, _, cat, _ in prateleira_de(tipo): quer[cat] = quer.get(cat, 0) + 1
    return quer

# ---------- a maestria de comércio (maestria.comércio): sobe por DIAS DE NEGÓCIO ----------
NEGOCIO_MIN = 10            # um negócio (compra ou venda) deste tanto de prata ou mais faz do dia um dia de negócio (conta um por dia)
COMERCIO_DIAS = {2: 20, 4: 80, 6: 250, 8: 750}      # dias de negócio para cada grau
FEITO_NEGOCIO = {6: 1000, 8: 10000}                 # de Mestre para cima, além dos dias, um FEITO: um negócio só deste tanto de prata ou mais
