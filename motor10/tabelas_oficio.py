"""tabelas_oficio.py — MOTOR 10: TODOS os números do ofício (forjar, consertar, ajustar) num lugar só.

Os números do mundo moram no tabelas_mundo.py; os da luta e dos itens, no tabelas.py. Mudar o ofício é mudar esta página
e rodar `provas_oficio.py` (ou `provas_mundo.py`, que o chama).
"""
import math
import tabelas as T
import tabelas_mundo as M

# ---------- a obra (forjar) ----------
FORJA_ATE = 5               # forja-se até o Lendário (o índice da categoria); acima disso, ninguém forja ainda
def blocos(cat): return 3 ** cat                # blocos PESADOS de bancada: Comum 1, Incomum 3, Raro 9, Épico 27, Único 81, Lendário 243
TESTE_BASE = 28             # o teste final: 2d20 + maestria do ofício + Afinidade ÷ 10 + oficina + preparo, contra isto...
TESTE_CAT = 6               # ... mais isto por categoria
def contra(cat): return TESTE_BASE + TESTE_CAT * cat
POR_POUCO = 5               # falhar por MENOS disto: a peça sai uma categoria abaixo. Por isto ou mais: a matéria some (o núcleo também)
TOSCA = 0.5                 # abaixo do Comum não há categoria: o Comum que falha por pouco sai TOSCO (nasce com esta fração da durabilidade)

# ---------- a oficina do lugar (lugar.oficina, de 0 a 4; lugar sem o campo não tem oficina) ----------
OFICINAS = ['bancada', 'forja de vila', 'forja de cidade', 'grande forja', 'forja mestra']      # o nível soma no teste (0 a 4)
OFICINA_CONSERTA = 1        # o ferreiro do lugar conserta (pago) até a categoria nível + isto: a forja de vila, até o Raro

# ---------- o preparo (cada um vale +2; até +8) ----------
# cada preparo é uma marca com ALCANCE: o índice da categoria mais alta a que ele serve (0 Comum ... 5 Lendário). Só soma na obra que ele alcança.
# os dois da pessoa moram em pessoa.marca; os dois do lugar, em lugar.preparo
PREPAROS = dict(receita=('pessoa', 'prep_receita'), ajudante=('pessoa', 'prep_ajudante'), fogo=('lugar', 'fogo'), bigorna=('lugar', 'bigorna'))
PREPARO_CADA = 2
PREPARO_MAX = 8

# ---------- a maestria do ofício (forja, couro): sobe por blocos de bancada, como a das armas ----------
OFICIO_BLOCOS = {2: 50, 4: 150, 6: 375, 8: 1000}        # blocos de bancada (forjar, consertar, ajustar, jornal) para cada grau
FEITO_OBRA = {6: 3, 8: 4}   # de Mestre para cima, além dos blocos, um FEITO: uma obra nascida desta categoria ou melhor (Mestre: Épico; Lendário: Único)
MAO_DA_OBRA = [0, 0, 2, 4, 6, 8]    # a mão que a obra pede, por categoria (Comum e Incomum: Leigo; Raro: Iniciante; Épico: Treinado; Único: Mestre; Lendário: Lendário)
                                    # para FORJAR é conselho, não tranca (abaixo dela a conta quase não fecha); para CONSERTAR sozinho, é o que se pede

# ---------- a matéria de cada peça (na categoria da obra; do Épico para cima, matéria Rara mais um núcleo da categoria) ----------
MATERIA_ARMA = M.MATERIA_ARMA                   # adaga 1 de metal ... montante 5 (tabelas_mundo: o mercado tira o preço da arma da mesma tabela); as mãos ("punho") não se forjam
MATERIA_ARMADURA = dict(couro=('couro', 1), malha=('metal', 1), placa=('metal', 2))     # a matéria, e quanto por ponto de corpo coberto
PARTE_PESO = M.PARTE_PESO                                                               # cabeça 1, tronco 2, braços 1, pernas 1 (tabelas_mundo: o mercado usa o mesmo peso no preço)
MATERIA_ESCUDO = M.MATERIA_ESCUDO                                                       # 2 de madeira e 1 de metal (tabelas_mundo)
OFICIO_COURO = ('couro',)   # as armaduras deste material são do ofício "couro"; todo o resto é da "forja"
PECAS_ENCANTO = ('foco', 'amuleto')     # (etapa da magia) o foco e o amuleto se fazem no ofício do ENCANTO, na mesa de runas, com os blocos, o teste e a falha da forja
PECAS_LADINO = ('gazua',)   # (etapa 4b) a GAZUA se forja na oficina, como a adaga: 1 de metal da categoria (tabelas_mundo.MATERIA_GAZUA), os blocos, o teste e a falha da forja;
                            # do Épico para cima, matéria Rara e um núcleo (a lei da forja). Conserta-se na bancada como as outras peças. A chave não se forja
TALHES = (None, 'miúdo')    # (etapa 4b) a armadura se forja para um corpo: de gente (sem talhe) ou miúda (o pequenino e o gnomo: `forjar armadura ... talhe=miúdo`); a matéria é a mesma

# ---------- A LEI DO VALOR (decisão do jogador, Dia 30 do mundo novo: a regra da forja do Ferir, obra_valor.py, com os números do Motor 10) ----------
# Na FORJA e no COURO a categoria da peça NÃO SE ESCOLHE: escolhe-se a peça e o que entra nela (a matéria da categoria dita; do Épico para cima, a matéria Rara e um
# núcleo da categoria), rola-se 2d20 explosivos e soma-se TUDO: a mão, a matéria, o núcleo, o martelo de forja, a tenaz, a oficina, o preparo. A peça sai na MAIOR
# categoria cuja CD o total alcança, até o TETO; abaixo da CD do Comum, a matéria se perde. O encanto (o foco e o amuleto), a alquimia, a gravação e o ajuste seguem
# com a categoria escolhida e o teste de passar (7.3 a 7.6). OS NÚMEROS ABAIXO SÃO OS DA ESPECIFICAÇÃO MEDIDA (projeto/etapa_efeitos/LEI_DO_VALOR.md).
VALOR_OFICIOS = ('forja', 'couro')
VALOR_CD = [20, 34, 48, 62, 76, 92]          # Comum, Incomum, Raro, Épico, Único, Lendário (PROVISÓRIO até a especificação)
VALOR_MATERIA = [0, 4, 8]                    # a matéria: Comum, Incomum, Rara
VALOR_NUCLEO = {3: 4, 4: 8, 5: 12}           # o núcleo (do Épico para cima; a matéria é a Rara)
VALOR_MARTELO = [1, 2, 3, 5, 7, 10]          # o martelo de forja, pela categoria dele
VALOR_TENAZ = [1, 1, 2, 3, 4, 5]             # a tenaz
VALOR_AFINADA = 1                            # a ferramenta de obra-prima (afinada) soma mais isto
TETO_ACIMA = 1                               # sem núcleo, a peça sobe no máximo tanto acima da matéria, e nunca acima do Raro; com núcleo, até a categoria dele
def teto(cat): return cat if cat > M.MATERIA_ATE else min(cat + TETO_ACIMA, M.MATERIA_ATE)
def cat_do_total(total, teto_):
    """a maior categoria cuja CD o total alcança, até o teto; None: abaixo da CD do Comum (a matéria se perde)"""
    k = None
    for c in range(min(teto_, len(VALOR_CD) - 1) + 1):
        if total >= VALOR_CD[c]: k = c
    return k
# OS DADOS (rolados na mesma conta, uma vez): cada 20 que abre dá +1 efeito; os dois dados em 20 são OBRA-PRIMA (1d6: 1 a 3, a peça sobe uma categoria se o teto
# deixa, senão +1 efeito; 4 a 6, +1 efeito); um dado em 1 é COMPLICAÇÃO (1d6: 1, a peça se perde; 2 e 3, cai uma categoria; 4 a 6, nasce com um quarto a menos de
# durabilidade); os dois dados em 1, a peça se perde. O QUASE: o total ficou a VALOR_QUASE ou menos da CD seguinte, e o teto deixava subir: +1 efeito.
VALOR_QUASE = 3
VALOR_COMPLICA_DUR = 0.75

# ---------- AS FERRAMENTAS DO OFÍCIO e A OBRA-PRIMA (a etapa dos efeitos, parte 1) ----------
# A FERRAMENTA é uma peça do Livro de Itens (tipo "ferramenta"), de um ofício: o JOGO DE FORJA (o martelo de forja e a tenaz) serve à forja; o JOGO DE COURO (a faca e a
# sovela), ao couro. Forja-se na oficina, como a adaga: a matéria, os blocos (3^k), o teste e a falha da forja; do Épico para cima, matéria Rara e um núcleo.
# Quem tem a ferramenta (dono, inteira) soma o BÔNUS dela no teste do ofício (forjar e ajustar), FORA do teto do preparo; vale a melhor que a pessoa tiver.
PECAS_FERRAMENTA = ('ferramenta',)
FERRAMENTA_OFICIOS = ('forja', 'couro')
# A LEI DO VALOR separa o MARTELO DE FORJA e a TENAZ (cada um soma: VALOR_MARTELO, VALOR_TENAZ); o JOGO (o par de uma vez) vale pelos dois. A chave da matéria: a forma
# (martelo, tenaz) ou o ofício do jogo (forja, couro).
MATERIA_FERRAMENTA = dict(martelo={'metal': 2, 'madeira': 1}, tenaz={'metal': 1, 'madeira': 1}, forja={'metal': 3, 'madeira': 2}, couro={'metal': 1, 'couro': 1})
NOME_FERRAMENTA = dict(martelo='martelo de forja', tenaz='tenaz', forja='jogo de forja', couro='jogo de couro')
FERRAMENTA_FORMAS = ('martelo', 'tenaz', 'jogo')        # o jogo de forja e o de couro (da parte 1) valem pelo martelo e pela tenaz juntos
def chave_ferramenta(forma, oficio): return forma if forma in ('martelo', 'tenaz') else oficio
def bonus_ferramenta(t, k):
    """o bônus de uma ferramenta de categoria t numa obra de categoria k: 1 + t (Comum +1 ... Lendária +6) na obra da categoria dela ou abaixo; na obra uma acima, +1; acima disso, nada"""
    return 1 + t if t >= k else 1 if t == k - 1 else 0
# OS PODERES DA FERRAMENTA, pela categoria dela (os de cima trazem os de baixo):
POR_POUCO_RARA = 8          # Rara ou melhor: a matéria só some se a obra falhar por isto ou mais (sem ela, POR_POUCO)
NADA_SE_PERDE = 3           # Épica ou melhor: a matéria nunca some; a obra que falha feio sai uma categoria abaixo (o Comum, tosco)
OBRA_PRIMA_FACIL = 4        # Única ou melhor: os degraus da obra-prima descem OBRA_PRIMA_DESCE
ACIMA_DO_FERRO = 5          # Lendária: a peça que passa por ACIMA_MARGEM ou mais nasce uma categoria acima (até o Lendário; sem núcleo a mais)
ACIMA_MARGEM = 25
# A OBRA-PRIMA: a peça que PASSA no teste por OBRA_PRIMA[i] ou mais ganha i+1 efeitos, até o teto da categoria dela; quem forjou escolhe cada um
# (`oficio.py efeito ITEM CHAVE`), entre os efeitos que a luta roda e que valem naquele tipo de peça (itens.EFEITOS; o "pesa" não se escolhe).
OBRA_PRIMA = (10, 20, 30)
OBRA_PRIMA_DESCE = 5
EFEITOS_MAX = (1, 1, 2, 2, 3, 3, 3, 3)    # Comum e Incomum 1; Raro e Épico 2; do Único para cima 3
def efeitos_da_obra(margem, cat, facil=False):
    """quantos efeitos a obra-prima dá: os degraus que a margem alcançou, até o teto da categoria"""
    if margem < 0: return 0
    d = OBRA_PRIMA_DESCE if facil else 0; return min(EFEITOS_MAX[min(cat, len(EFEITOS_MAX) - 1)], sum(1 for x in OBRA_PRIMA if margem >= x - d))
# A BANCADA DE CADA OFÍCIO (etapa da magia): o campo do lugar que é a bancada dele (0 a 4; o lugar sem o campo não a tem), e o tipo de evento do trabalho nela
BANCA = dict(forja='oficina', couro='oficina', encanto='runas', alquimia='botica', fé='santuario')
EVENTO_OFICIO = dict(encanto='encantar', alquimia='alquimia', fé='rito')        # o evento do bloco de bancada (a forja e o couro: o tipo da obra, forjar ou ajustar)


def oficio_da(tipo, material=None): return 'encanto' if tipo in PECAS_ENCANTO else 'couro' if tipo == 'armadura' and material in OFICIO_COURO else 'forja'
def cat_materia(cat): return min(cat, M.MATERIA_ATE)        # a categoria da matéria que a obra gasta
def pede_nucleo(cat): return cat > M.MATERIA_ATE


def materia(tipo, cat, familia=None, material=None, cobre=None):
    """{chave "nome:categoria": quanto} que a peça gasta"""
    if tipo == 'arma': base = MATERIA_ARMA[familia]
    elif tipo == 'foco': base = M.MATERIA_FOCO[familia]             # o foco: a forma vem no lugar da família (varinha, cajado, símbolo, talismã)
    elif tipo == 'amuleto': base = M.MATERIA_AMULETO
    elif tipo == 'gazua': base = M.MATERIA_GAZUA                   # a gazua (etapa 4b): 1 de metal, como a adaga
    elif tipo == 'ferramenta': base = MATERIA_FERRAMENTA[familia]   # a ferramenta: o ofício dela vem no lugar da família (forja, couro)
    elif tipo == 'armadura':
        nome, por = MATERIA_ARMADURA[material]; base = {nome: por * sum(PARTE_PESO[x] for x in (cobre or ['tronco', 'braços', 'pernas']))}
    else: base = MATERIA_ESCUDO
    return {M.materia(k, cat_materia(cat)): n for k, n in base.items()}


def materia_conserto(tipo, cat, familia=None, material=None, cobre=None):
    """a chave da matéria principal da peça (a que mais entra nela): é dela que o conserto gasta"""
    m = materia(tipo, cat, familia, material, cobre); return max(m, key=lambda k: m[k])


# ---------- consertar ----------
CONSERTO_BLOCO = 5          # pontos de durabilidade que um bloco de bancada devolve (feito por você)
CONSERTO_MATERIA = 10       # cada tantos pontos (ou parte) gastam 1 de matéria principal da peça
PAGO_BLOCO = 10             # pago à oficina: um bloco de espera a cada tantos pontos (ou parte)
def preco(cat): return M.PECA_BASE * M.PECA_VEZES ** cat                # o preço de tabela da peça nova (30 a Comum, vezes 6 por categoria): o da espada
def conserto_pago(cat, pontos, peso=1.0): return max(1, math.ceil(round(preco(cat) * peso * M.CONSERTO_PONTO * pontos, 6)))     # 2% do preço da peça por ponto, em prata inteira (o preço segue o tamanho dela: a armadura, o que cobre; a arma, a matéria que leva: tabelas_mundo.peso_da_peca)

# ---------- ajustar (sob medida) ----------
AJUSTE_BASE = 22            # o teste do ajuste: a mesma soma da forja, contra isto mais 6 por categoria da peça
def ajuste_contra(cat): return AJUSTE_BASE + TESTE_CAT * cat
def ajuste_blocos(cat): return cat + 1          # blocos de bancada: Comum 1 ... Lendário 6
def ajuste_grau(maestria): return max(0, min(T.SOB_MEDIDA_GRAUS[1], maestria // 2))     # o grau do sob medida sai da mão de quem ajusta: Iniciante 1 ... Lendário 4
AJUSTE_ESTRAGO = 5          # ajuste que falha por 5 ou mais gasta isto da durabilidade da peça

# ---------- o jornal (trabalhar na oficina do lugar) ----------
JORNAL_ESFORCO = 'pesado'   # bloco de bancada é sempre pesado
JORNAL_GRAU = {2: 'aprendiz', 4: 'oficial', 6: 'mestre'}        # quem serve na bancada ganha pelo que a mão vale (tabelas_mundo.SALARIO): de Iniciante, o salário de aprendiz;
                                                                # de Treinado, o de oficial; de Mestre para cima, o de mestre. Nunca menos que o grau de ofício que a pessoa já tem.
def jornal_grau(maestria, grau='diarista'):
    """o grau de ofício pelo qual a oficina paga o jornal a quem tem esta maestria no ofício e este grau de ofício: o que pagar mais"""
    da_mao = next((g for m, g in sorted(JORNAL_GRAU.items(), reverse=True) if maestria >= m), grau)
    return max((grau if grau in M.SALARIO else 'diarista', da_mao), key=lambda g: M.SALARIO[g])
