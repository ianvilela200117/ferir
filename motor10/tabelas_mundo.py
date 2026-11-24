"""tabelas_mundo.py — MOTOR 10: TODOS os números do mundo num lugar só (o tempo, o corpo, viver, treinar).

Os números da luta e dos itens moram no tabelas.py. Mudar o mundo é mudar esta página e rodar `provas_mundo.py`.
"""

# ---------- o tempo ----------
BLOCO_HORAS = 4
BLOCOS = ['madrugada', 'alvorada', 'manhã', 'tarde', 'entardecer', 'noite']    # 6 blocos de 4 horas; o dia começa à meia-noite
BLOCOS_DIA = len(BLOCOS)
ESCUROS = (0, 5)            # blocos sem luz: a luta ao ar livre ganha "escuro"
SEMANA = 7
ESTACAO = 91
ANO = 364
ESTACOES = ['primavera', 'verão', 'outono', 'inverno']
COLHEITA = [0.5, 1, 2.5, 0]

# ---------- o corpo (três medidores de 0 a 10) ----------
MEDIDORES = ['fome', 'sono', 'cansaco']
MED_MAX = 10
FOME_A_CADA = 2             # a fome sobe 1 a cada tantos blocos
REFEICAO = -3               # uma refeição tira isto da fome
SONO_ACORDADO = 1           # por bloco acordado
SONO_CAMA = -3              # por bloco dormido numa cama
SONO_CHAO = -2              # por bloco dormido no chão
ESFORCO = dict(pesado=2, leve=1, nada=0, descanso=-1)     # o cansaço que um bloco de cada tipo dá
CANSACO_CAMA = -3           # o cansaço que um bloco dormido tira (no chão: SONO_CHAO)
# a pena do corpo: vale a PIOR das três (não somam), em todo teste, no acerto e na Defesa
PENAS = dict(fome=[(7, -4), (4, -2)], sono=[(8, -4), (6, -2)], cansaco=[(9, -2)])
LIMIARES = dict(fome=(4, 7), sono=(6, 8), cansaco=(9,))   # ao cruzar um destes, a ação longa PARA
CANSACO_FOLEGO = 3          # cada tantos pontos de cansaço tiram 1 do fôlego máximo
FOLEGO_MIN = 2
FOME_PV = 0.05              # com fome 7 ou mais na virada do dia: perde esta fração do PV máximo
SONO_CAI = (8, 28)          # com sono 8 ou mais, por bloco acordado: Vontade contra isto, ou dorme ali mesmo (no chão, até o sono baixar do primeiro limiar)
CURA_BLOCO = 0.05           # PV que um bloco dormido devolve (fração do máximo), sem fome 4 ou mais
CURA_DIA = 2                # ... em no máximo tantos blocos por dia (10% por noite dormida)
FERIDA_DIAS = (7, 21)       # dias de repouso para a ferida sarar (ferida, grave)
PESADOS_SEM_REPOUSO = 2     # dia com tantos blocos pesados não conta para sarar (nem o dia em que a pessoa lutou, nem o dia em que passou um bloco ou mais numa saída ao ermo)
LUTA_CANSA = 2              # uma luta cansa isto

# ---------- o descanso em casa (quem NÃO é o personagem cuida de si quando não está em cena; o personagem nunca descansa de graça) ----------
CASA_ZERA = 3               # passados tantos blocos ou mais do último bloco em cena (o bloco em que o corpo foi mexido pela última vez): a fome, o sono e o cansaço voltam a zero (comeu e dormiu por conta própria); com menos, nada muda.
                            # Quem volta no bloco da noite e é chamado às 8h passou 3: são dois blocos inteiros em casa
CASA_NOITE = 6              # a cada tantos blocos inteiros passados (um dia): uma noite dormida de cura (CURA_BLOCO × CURA_DIA do PV máximo) e um dia de repouso nas feridas
INTEIRO_PV = 0.9            # ao abrir uma saída, a mesa diz o estado de quem vai junto se ele não está inteiro: PV abaixo desta fração do máximo, ferida aberta, ou o corpo cobrando

# ---------- viver (em prata) ----------
REFEICAO_PRECO = 1
CAMA_PRECO = 2              # por noite (paga-se ao deitar numa pousada)
CAMA_VALE = 6               # a cama paga vale tantos blocos (um dia inteiro), a contar do bloco em que se pagou, no lugar onde se pagou: dormir de novo nesse prazo não cobra
SALARIO = dict(diarista=2, aprendiz=3, oficial=6, mestre=10)      # por bloco trabalhado
JORNADA = 2                 # a jornada: o lugar paga a cada pessoa no máximo tantos blocos de serviço por dia (trabalhar e o jornal da oficina contam juntos)
ESFORCO_OFICIO = dict(diarista='pesado', aprendiz='pesado', oficial='leve', mestre='leve')

# ---------- o vocabulário comum dos bens (etapa 2: o mercado, o ofício e a caça falam a mesma língua) ----------
# a matéria de ofício tem categoria; a chave dela, na carga e no estoque, é "nome:categoria" ("metal:0", "couro:2", "osso:1")
MATERIAS = ['metal', 'couro', 'osso', 'madeira', 'erva']
def materia(nome, cat): return f'{nome}:{cat}'
def le_materia(chave):
    n, _, c = chave.partition(':')
    return (n, int(c)) if c.isdigit() else (chave, None)
BENS = ['comida', 'lenha', 'carvão', 'sal', 'pano', 'remédio', 'ferramenta']     # os bens sem categoria ("prata" é o dinheiro do lugar, no estoque dele)
MATERIA_ATE = 2             # a matéria comum vai até o Raro; do Épico para cima a obra pede um NÚCLEO (item do Livro de Itens, tipo 'nucleo', contado no mundo)
PECA_BASE = 30              # o preço de tabela de uma peça Comum nova, em prata: o da espada, do escudo e da armadura que cobre tronco, braços e pernas (as outras: peso_da_peca)
PECA_VEZES = 6              # ... vezes isto a cada categoria
PECA_LOJA_ATE = 3           # a loja vende até o Épico; daí para cima, só leilão, encomenda ou despojo
CONSERTO_PONTO = 0.02       # consertar na oficina de outro: esta fração do preço da peça por ponto de durabilidade
PARTE_PESO = dict(cabeça=1, tronco=2, braços=1, pernas=1)      # quanto pesa cada parte do corpo numa armadura: na matéria que ela leva (o ofício) e no preço (o mercado)
CORPO_PESO = 4              # a armadura de tabela cobre tronco, braços e pernas: 4 pontos. O preço de tabela é o dela; a que cobre menos vale a proporção (o elmo: um quarto)
# a matéria de cada arma e do escudo, em unidades (na categoria da obra; do Épico para cima, matéria Rara mais um núcleo). O ofício gasta isto na obra (tabelas_oficio),
# e o mercado tira daqui o preço: A ARMA VALE PELA MATÉRIA QUE LEVA, como a armadura vale pelo que cobre
MATERIA_ARMA = {
    'adaga':    dict(metal=1),
    'espada':   dict(metal=3),
    'maça':     dict(metal=3),
    'machado':  dict(metal=2, madeira=1),
    'martelo':  dict(metal=3, madeira=1),
    'lança':    dict(metal=1, madeira=2),
    'montante': dict(metal=5),
    'alabarda': dict(metal=3, madeira=2),
    'malho':    dict(metal=4, madeira=1),
    'arco':     dict(madeira=3),
    'besta':    dict(madeira=3, metal=1),
}                                               # as mãos ("punho") não se forjam
MATERIA_ESCUDO = dict(madeira=2, metal=1)
PECA_DE_TABELA = 'espada'   # o preço de tabela (PECA_BASE, vezes PECA_VEZES por categoria) é o desta arma: as outras valem a proporção das unidades de matéria que levam
def peso_da_peca(tipo, cobre=None, familia=None):
    """a fração do preço de tabela que uma peça vale pelo tamanho. A armadura, pelo que cobre: os pontos de corpo ÷ CORPO_PESO (o elmo: um quarto).
    A arma e o escudo, pela matéria que levam: as unidades de matéria ÷ as da espada (a adaga: um terço; o montante: cinco terços; o escudo: 1).
    A arma que a tabela não conhece vale o preço de tabela."""
    if tipo == 'armadura': return sum(PARTE_PESO.get(x, 0) for x in (cobre or ['tronco', 'braços', 'pernas'])) / CORPO_PESO
    mat = MATERIA_ESCUDO if tipo == 'escudo' else MATERIA_ARMA.get(familia) if tipo == 'arma' else None
    return sum(mat.values()) / sum(MATERIA_ARMA[PECA_DE_TABELA].values()) if mat else 1.0
def peso_do_item(it): return peso_da_peca(it.get('tipo'), it.get('cobre'), it.get('familia'))       # o mesmo, lido de um item do Livro de Itens
OFICINA_MAX = 4             # a oficina de um lugar vai de 0 (bancada) a isto (forja mestra)
PERIGO_MAX = 3              # o perigo de um ermo vai de 1 (a borda) a isto (o coração)

# ---------- treinar ----------
MAESTRIA_BLOCOS = {2: 40, 4: 160, 6: 500, 8: 1500}       # blocos de treino ou de luta com a arma para cada grau (o ofício que ainda não tem tabela própria, como a cura, segue esta)
MAESTRIA_FEITO = 6          # deste grau para cima, além dos blocos, pede um FEITO com a arma (o mundo registra)

# ---------- os eventos (o que pode acontecer; evento fora desta lista é recusado) ----------
EVENTOS = ['tempo', 'virada', 'comer', 'dormir', 'trabalhar', 'treinar', 'descansar', 'esperar', 'vestir', 'luta', 'compra', 'venda', 'cura', 'mestre', 'gera',
           'forjar', 'consertar', 'ajustar', 'cacar', 'coletar', 'despojo', 'producao', 'consumo', 'ninhada', 'casa']
NASCE = ('gera', 'mestre')  # só nestes eventos nasce lugar, nasce gente e nasce prata
NA_LUTA = ('luta', 'mestre')        # com uma luta aberta no mundo, só estes eventos entram: a luta que volta ao estado e a mão do Mestre (e a nota da saída de caça que diz que está naquela luta)
ROTINA = ('comer', 'dormir', 'descansar', 'esperar')      # o que se repete todo dia: no RETOMAR, os eventos destes tipos viram UMA linha por dia
MUNDO_SOZINHO = ('virada', 'producao', 'consumo', 'ninhada', 'casa')     # o mundo andando sozinho (o dia que vira, o lugar que produz e consome, o ermo que se refaz, quem descansou em casa): não é fato do turno, a não ser que alguém morra
RETOMAR_FATOS = 40          # o teto de linhas de fatos no RETOMAR.md; passando disso, a primeira linha diz quantos ficaram de fora e como lê-los
OFICIOS = ['forja', 'couro', 'caça', 'coleta', 'comércio', 'cura']      # os ofícios que têm maestria e treino, como as armas (maestria.forja, treino.caça)
MODULOS = ['mercado', 'oficio', 'caca']     # os módulos do mundo: cada um pode ter virada(E) (roda quando o dia vira), mesa(E) (linhas para a MESA.md), so_mestre(E) (linhas para o SÓ O MESTRE da MESA) e retomar(E) (linhas para o RETOMAR.md)
ESTADOS = ['vivo', 'morto']
