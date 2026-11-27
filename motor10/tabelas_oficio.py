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
VALOR_CD = [22, 55, 80, 105, 130, 155]       # Comum, Incomum, Raro, Épico, Único, Lendário: "a Comum pede 22, a Incomum 55, e daí mais 25 por categoria"
VALOR_MATERIA = [0, 15, 30]                  # a matéria: Comum, Incomum, Rara ("a obra vale 15 por categoria")
VALOR_NUCLEO = {3: 15, 4: 30, 5: 45}         # o núcleo, somado à matéria Rara que a obra leva: a obra inteira vale 45, 60, 75
VALOR_MARTELO = [1, 3, 5, 7, 9, 11]          # o martelo de forja, pela categoria dele (1 + 2 por categoria)
VALOR_TENAZ = [1, 3, 5, 7, 9, 11]            # a tenaz: a mesma tabela
VALOR_AFINADA = 1                            # a ferramenta de obra-prima (afinada) soma mais isto, uma vez só por obra
TETO_ACIMA = 1                               # sem núcleo, a peça sobe no máximo tanto acima da matéria, e nunca acima do Raro; com núcleo, até a categoria dele
PORTA_DEGRAU = 4                             # A PORTA DO DEGRAU: subir acima da matéria pede mão de Treinado (maestria 4); Leigo e Iniciante param na categoria da matéria
def teto(cat, maestria=None, ferramenta_cat=None):
    """o teto da obra: com núcleo, a categoria dele (e uma acima, com ferramenta Lendária); sem núcleo, a matéria + 1 (nunca acima do Raro), e a matéria só, sem a mão de Treinado"""
    if cat > M.MATERIA_ATE: return min(cat + (1 if (ferramenta_cat or -1) >= ACIMA_DO_FERRO else 0), FORJA_ATE)
    if maestria is not None and maestria < PORTA_DEGRAU: return cat
    return min(cat + TETO_ACIMA, M.MATERIA_ATE)
def cat_do_total(total, teto_):
    """a maior categoria cuja CD o total alcança, até o teto; None: abaixo da CD do Comum (a matéria se perde)"""
    k = None
    for c in range(min(teto_, len(VALOR_CD) - 1) + 1):
        if total >= VALOR_CD[c]: k = c
    return k
# OS DADOS (as faces de partida dos dois d20; sem 1d6): cada 20 da cadeia dá +1 efeito por escolher (somado aos da FAIXA, abaixo), até o teto de efeitos da categoria;
# OS DOIS ABRINDO EM 20 são a OBRA-PRIMA: a peça sobe uma categoria se o teto deixa, e a faixa fica (a do total); no teto, +1 efeito, que pode passar do teto de efeitos;
# UM ABRINDO EM 1: a peça sai uma categoria abaixo do que o total deu (a Comum, tosca), e a faixa fica (o 1 tira a categoria, não os efeitos); OS DOIS ABRINDO EM 1:
# a matéria e o núcleo se perdem, qualquer que seja o total. A peça salva pela ferramenta (a Rara e a Épica, abaixo) sai sem efeito.
# OS PODERES DAS FERRAMENTAS (a maior das duas; os de cima trazem os de baixo): Rara, a matéria não se perde se o total ficou a VALOR_SEGURA ou menos abaixo da CD do Comum
# (sai Comum, tosca; não vale contra os dois 1); Épica, a matéria nunca se perde, nem nos dois 1; Única, o QUASE (+1 efeito quando faltou QUASE_JANELA ou menos para a CD
# de cima e ela podia ser alcançada, isto é, abaixo do teto; com ou sem dado especial); Lendária, ACIMA DO FERRO (na obra com núcleo, o teto sobe uma categoria).
VALOR_SEGURA = 5
QUASE_JANELA = 6

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
POR_POUCO_RARA = 8          # (a regra da categoria escolhida, que segue no encanto) Rara ou melhor: a matéria só some se a obra falhar por isto ou mais
NADA_SE_PERDE = 3           # Épica ou melhor: a matéria nunca some; a obra que falha feio sai uma categoria abaixo (o Comum, tosco)
OBRA_PRIMA_FACIL = 4        # Única ou melhor: os degraus da obra-prima descem OBRA_PRIMA_DESCE
ACIMA_DO_FERRO = 5          # Lendária: a peça que passa por ACIMA_MARGEM ou mais nasce uma categoria acima (até o Lendário; sem núcleo a mais)
ACIMA_MARGEM = 25
# A OBRA-PRIMA: a peça que PASSA no teste por OBRA_PRIMA[i] ou mais ganha i+1 efeitos, até o teto da categoria dela; quem forjou escolhe cada um
# (`oficio.py efeito ITEM CHAVE`), entre os efeitos que a luta roda e que valem naquele tipo de peça (itens.EFEITOS; o "pesa" não se escolhe).
OBRA_PRIMA = (10, 20, 30)
OBRA_PRIMA_DESCE = 5
EFEITOS_MAX = (2, 4, 4, 5, 5, 6, 6, 7)    # (a parte 2, fase 1a) O TETO DE EFEITOS: a Comum leva 2; a Incomum e a Rara, 4; e daí +1 a cada duas categorias (antes: 1, 1, 2, 2, 3...)
def efeitos_max(cat): return EFEITOS_MAX[max(0, min(cat, len(EFEITOS_MAX) - 1))]
def efeitos_da_obra(margem, cat, facil=False):
    """(o encanto, que segue no teste de passar) quantos efeitos a obra-prima dá: os degraus que a margem alcançou (10, 20, 30), até o teto de efeitos da categoria"""
    if margem < 0: return 0
    d = OBRA_PRIMA_DESCE if facil else 0; return min(efeitos_max(cat), sum(1 for x in OBRA_PRIMA if margem >= x - d))

# ---------- A FAIXA DA FORJA (a parte 2, fase 1a; o contrato: projeto/etapa_efeitos/DESENHO.md, seção 5) ----------
# Na forja e no couro (a Lei do Valor), a CATEGORIA sai como sempre (a maior CD que o total alcança, até o teto). Os EFEITOS saem de quanto FALTOU para a CD de cima:
# quanto mais perto dela, sem passar, mais efeitos. Passou, é a categoria de cima. NADA DISTO MEXE NO TOTAL: a chance de cada categoria é a de antes, linha por linha.
REGUA_FAIXA = ((2, 4), (5, 3), (8, 2), (16, 1))     # (a) a proporcional (a recomendação; pergunta 1 do contrato): faltou 1 ou 2 → 4 efeitos; 3 a 5 → 3; 6 a 8 → 2; 9 a 16 → 1; 17 ou mais → 0
# REGUA_FAIXA = ((1, 4), (3, 3), (5, 2), (10, 1))   # (b) ao pé da letra dos números do exemplo do jogador: faltou 1 → 4; 2 ou 3 → 3; 4 ou 5 → 2; 6 a 10 → 1; 11 ou mais → 0
                                                    #     (se o jogador escolher (b), troque a linha de cima por esta: o resto do motor e do banco segue igual)
TETO_FAIXA = 2              # NA CATEGORIA DO TETO (a de cima está trancada: a matéria, a porta do degrau, o núcleo, a Lendária) a régua para em 2, e passar da CD trancada dá 2
VALOR_CD_ACIMA = 180        # a CD de cima da Lendária (a da Mítica, pelo passo de 25: ninguém forja Mítica): fecha a faixa da Lendária, que vive sempre no teto
FAIXA_NOME = ('o terço de baixo', 'o terço do meio', 'o terço de cima', 'colada', 'no fio')       # o nome à mesa de cada degrau da régua (0 a 4 efeitos da faixa)
PRUMO_MAX = 5               # o prumo soma de todas as fontes (ferramentas; depois habilidades, dons e classe), até isto
def cd_de_cima(k): return VALOR_CD[k + 1] if k + 1 < len(VALOR_CD) else VALOR_CD_ACIMA
def da_regua(falta):
    """quantos efeitos dá a régua para o que faltou à CD de cima (falta ≤ 0, que só existe no teto ou com o prumo, conta como colada no fio)"""
    for ate, n in REGUA_FAIXA:
        if falta <= ate: return n
    return 0
def faixa(total, k, teto_, prumo=0, lastro=False):
    """os efeitos da FAIXA de uma obra cujo total deu a categoria k (antes dos dados especiais), com este teto: a régua pelo que faltou à CD de cima (o prumo conta N a menos);
    na categoria do teto, no máximo TETO_FAIXA (e TETO_FAIXA se o total passou da CD trancada); o LASTRO faz o 0 virar 1. Devolve (efeitos da faixa, o que faltou)."""
    if k is None: return 0, None
    falta = cd_de_cima(k) - total
    if k >= teto_: n = TETO_FAIXA if falta <= 0 else min(TETO_FAIXA, da_regua(falta - prumo))
    else: n = da_regua(falta - prumo)
    return (max(n, 1) if lastro else n), falta

# AS FORÇAS DO EFEITO e a PORTA de cada uma: a categoria que abre a força (fraco na Comum, normal na Incomum, forte na Épica, apelão na Lendária). Só cabe na peça o efeito
# cuja porta a categoria FINAL dela abre. A mesma régua mede tudo: no duelo, 5 · 10 · 20 · 40 pontos de vitória; na ferramenta, em PONTOS DE FEITIO POR OBRA (efeitos + metade dos cheios).
FORCAS = ('fraco', 'normal', 'forte', 'apelão')
FORCA_PORTA = dict(fraco=0, normal=1, forte=3, apelão=5)
FORCA_FEITIO = dict(fraco=0.15, normal=0.30, forte=0.60, apelão=1.20)      # o teto da régua das ferramentas, em pontos de feitio por obra (o passo ×2 da régua do duelo)
def forca_da_cat(cat):
    """a força mais alta que a categoria abre (a porta)"""
    return [f for f in FORCAS if FORCA_PORTA[f] <= max(0, cat)][-1]
def cabe_forca(forca, cat, emprestado=False):
    """a força cabe na peça desta categoria? (com o DEGRAU EMPRESTADO, uma força acima da que a categoria abre)"""
    i = FORCAS.index(forca_da_cat(cat)) + (1 if emprestado else 0)
    return FORCAS.index(forca) <= min(i, len(FORCAS) - 1)

# OS DOZE EFEITOS DE FERRAMENTA (5.8). O martelo de forja, a tenaz e o jogo nascem pela mesma lei, com faixa e efeitos; quem forja escolhe (o `oficio.py efeito`).
# Valem os efeitos das ferramentas EM USO (a melhor no lugar do martelo e a melhor no lugar da tenaz: a de maior categoria; no empate, a de mais efeitos, depois a afinada;
# o jogo que é o melhor nos dois lugares vale uma vez). O MESMO EFEITO EM DUAS NÃO SOMA (vale o maior), menos o PRUMO, que soma até PRUMO_MAX.
# NENHUM mexe no total (a chance da categoria), menos a afinada, que é a de hoje (+1).
# chave: (força, porta, números por categoria da ferramenta (Comum ... Primordial) ou None, o que faz, o que vale (medido: pontos de feitio por obra, ou o que ele poupa))
# O NÚMERO NUNCA SE GUARDA NA PEÇA: sai da categoria dela (valor_ferramenta). O CHEIO leva o número da categoria de cima (o prumo cheio de uma tenaz Incomum é 2).
# O POUPA-FERRO poupa o FERRO: a matéria principal da peça, quando é o metal (a espada, a maça, o martelo, a placa...); o arco e a armadura de couro não (o banco: com ele poupando
# também a madeira, o arco Incomum barato fazia da loja uma mina na sorte, 15 de prata por dia, acima dos 12 da meta FJ8; poupando só o metal, 5,8 no pior caso).
# Só o prumo e a têmpera têm número que cresce: são os efeitos de NÚMERO da ferramenta (só eles levam cheio). Os números da Comum e da Incomum na têmpera, e o da Comum
# no prumo, só servem ao degrau emprestado (a força de cima, "com o número da categoria da peça").
FERRAMENTA_EFEITOS = {
    'afinada':       ('fraco', 0, None, '+1 no total do ofício, uma vez por obra (a única que mexe no total; não cresce)', '+0,02 efeito; +2,8 pontos na chance da Incomum da tenaz'),
    'fagulha':       ('fraco', 0, None, 'o dado que abre em 19 dá +1 efeito, como o 20 (não rola de novo)', '+0,09'),
    'recobro':       ('fraco', 0, None, 'a obra perdida devolve metade da matéria, para baixo (o núcleo se perde como sempre)', 'matéria'),
    'remendo':       ('fraco', 0, None, 'o conserto na bancada devolve 8 pontos por bloco, não 5', 'tempo'),
    'mao_de_medida': ('fraco', 0, None, 'o ajuste sob medida leva metade dos blocos e soma +2 no teste', 'tempo'),
    'sinete':        ('fraco', 0, None, 'a peça nasce com o sinete de quem a forjou: a janela diz', 'assinatura'),
    'prumo':         ('normal', 1, (1, 1, 2, 3, 4, 5, 5, 5), 'o que falta para a CD de cima conta {valor} a menos, só para os efeitos (no teto, até 2)', '+0,14 · +0,27 · +0,41 · +0,54 · +0,68 (Incomum a Lendária)'),
    'poupa_ferro':   ('normal', 1, None, 'a obra gasta 1 de metal a menos, se o metal é a matéria principal da peça e ela leva 3 ou mais dele (o ferro: a madeira e o couro não)', 'um terço da espada'),
    'lastro':        ('forte', 3, None, 'a peça que alcança uma categoria nasce com pelo menos 1 efeito da faixa', '+0,36'),
    'tempera':       ('forte', 3, (1, 1, 1, 1, 2, 3, 3, 3), 'na peça que ela forja, até {valor} efeito(s) de número nasce(m) cheio(s) (o número da categoria de cima)', '+0,32 · +0,46 · +0,54 (Épica a Lendária)'),
    'molde':         ('apelão', 5, None, 'ao abrir a obra, diz-se um efeito (molde=CHAVE): se a peça sai na categoria da obra ou acima, nasce com ele, fora do teto; se sai abaixo, o molde se perde', '+0,60'),
    'degrau':        ('apelão', 5, None, 'um efeito da peça que ela forja pode ser da força de cima, com o número da categoria da peça (o degrau emprestado; só em peça de até 4 efeitos)', 'dentro da régua da força de cima'),
}
REMENDO_BLOCO = 8           # o conserto por bloco com o remendo (hoje, sem ele: CONSERTO_BLOCO, 5)
MEDIDA_TESTE = 2            # a mão de medida: +2 no teste do ajuste (e metade dos blocos, para cima)
DEGRAU_ATE = 4              # o degrau emprestado só em peça de até tantos efeitos (a porta adiantada: 4.5 do contrato)
APELIDOS_EFEITO = {'têmpera': 'tempera', 'mão_de_medida': 'mao_de_medida', 'medida': 'mao_de_medida', 'poupa-ferro': 'poupa_ferro', 'poupaferro': 'poupa_ferro',
                   'molde_de_mestre': 'molde', 'degrau_emprestado': 'degrau', 'brasa': 'fagulha', 'mão_de_reparo': 'remendo'}
def chave_efeito(k):
    """a chave do efeito como o jogador a escreve (com acento, espaço ou hífen): a do catálogo"""
    k = str(k).strip().lower().replace(' ', '_'); return APELIDOS_EFEITO.get(k, APELIDOS_EFEITO.get(k.replace('-', '_'), k.replace('-', '_')))
def de_numero(chave): return chave in FERRAMENTA_EFEITOS and FERRAMENTA_EFEITOS[chave][2] is not None       # o efeito de ferramenta que tem número que cresce (leva cheio)
def valor_ferramenta(chave, cat, cheio=False):
    """o número de um efeito de ferramenta numa peça desta categoria (cheio: o da categoria de cima); None se o efeito não tem número"""
    n = FERRAMENTA_EFEITOS.get(chave, (None, None, None))[2]
    return None if n is None else n[max(0, min(cat + (1 if cheio else 0), len(n) - 1))]
# A RECEITA DO JEITO (o mundo escolhe sozinho: 5.7). O ferreiro do mundo tem um jeito, que sai da semente e do id dele (não muda com o dia); a receita põe primeiro os
# efeitos de NÚMERO (para o cheio ter onde cair), depois os do jeito, e o resto na ordem da semente. Na ferramenta (a fase 1a), o jeito se lê assim:
JEITOS = ('gume', 'guarda', 'fôlego', 'tranco')
JEITO_DIZ = dict(gume='do gume (dano, crítico, sangue)', guarda='da guarda (defesa, firmeza, aparar)', fôlego='do fôlego (leveza, não quebrar, fôlego)', tranco='do tranco (derrubar, atordoar, medo)')
JEITO_FERRAMENTA = dict(gume=('fagulha', 'molde', 'degrau', 'afinada'),             # o do gume quer mais efeito e mais forte
                        guarda=('lastro', 'recobro', 'afinada', 'remendo'),         # o da guarda não quer perder: o efeito garantido, a matéria de volta, o +1
                        fôlego=('poupa_ferro', 'mao_de_medida', 'remendo', 'recobro'),      # o do fôlego poupa: a matéria, o tempo
                        tranco=('afinada', 'fagulha', 'sinete', 'lastro'))          # o do tranco quer a peça certa e o nome nela
RECEITA_AUTO = dict(ferramenta='guarda')    # `oficio.py efeito ITEM auto` sem receita do jogador: a da guarda (a do gume é a da arma, quando o catálogo de luta chegar)
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
