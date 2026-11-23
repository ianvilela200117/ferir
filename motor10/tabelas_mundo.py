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
PESADOS_SEM_REPOUSO = 2     # dia com tantos blocos pesados não conta para sarar
LUTA_CANSA = 2              # uma luta cansa isto

# ---------- viver (em prata) ----------
REFEICAO_PRECO = 1
CAMA_PRECO = 2              # por noite (paga-se ao deitar numa pousada)
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
PECA_BASE = 30              # o preço de uma peça Comum nova, em prata
PECA_VEZES = 6              # ... vezes isto a cada categoria
PECA_LOJA_ATE = 3           # a loja vende até o Épico; daí para cima, só leilão, encomenda ou despojo
CONSERTO_PONTO = 0.02       # consertar na oficina de outro: esta fração do preço da peça por ponto de durabilidade
PARTE_PESO = dict(cabeça=1, tronco=2, braços=1, pernas=1)      # quanto pesa cada parte do corpo numa armadura: na matéria que ela leva (o ofício) e no preço (o mercado)
CORPO_PESO = 4              # a armadura de tabela cobre tronco, braços e pernas: 4 pontos. O preço de tabela é o dela; a que cobre menos vale a proporção (o elmo: um quarto)
def peso_da_peca(tipo, cobre=None):
    """a fração do preço de tabela que uma peça vale pelo tamanho: arma e escudo, 1; a armadura, os pontos de corpo que cobre ÷ CORPO_PESO (o elmo: um quarto)"""
    if tipo != 'armadura': return 1.0
    return sum(PARTE_PESO.get(x, 0) for x in (cobre or ['tronco', 'braços', 'pernas'])) / CORPO_PESO
OFICINA_MAX = 4             # a oficina de um lugar vai de 0 (bancada) a isto (forja mestra)
PERIGO_MAX = 3              # o perigo de um ermo vai de 1 (a borda) a isto (o coração)

# ---------- treinar ----------
MAESTRIA_BLOCOS = {2: 40, 4: 160, 6: 500, 8: 1500}       # blocos de treino ou de luta com a arma para cada grau
MAESTRIA_FEITO = 6          # deste grau para cima, além dos blocos, pede um FEITO com a arma (o mundo registra)

# ---------- os eventos (o que pode acontecer; evento fora desta lista é recusado) ----------
EVENTOS = ['tempo', 'virada', 'comer', 'dormir', 'trabalhar', 'treinar', 'descansar', 'esperar', 'vestir', 'luta', 'compra', 'venda', 'cura', 'mestre', 'gera',
           'forjar', 'consertar', 'ajustar', 'cacar', 'coletar', 'despojo', 'producao', 'consumo', 'ninhada']
NASCE = ('gera', 'mestre')  # só nestes eventos nasce lugar, nasce gente e nasce prata
OFICIOS = ['forja', 'couro', 'caça', 'coleta', 'comércio', 'cura']      # os ofícios que têm maestria e treino, como as armas (maestria.forja, treino.caça)
MODULOS = ['mercado', 'oficio', 'caca']     # os módulos do mundo: cada um pode ter virada(E) (roda quando o dia vira) e mesa(E) (linhas para a MESA.md)
ESTADOS = ['vivo', 'morto']
