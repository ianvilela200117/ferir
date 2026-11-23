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
SONO_CAI = (8, 28)          # com sono 8 ou mais, por bloco acordado: Vontade contra isto, ou dorme ali mesmo
CURA_BLOCO = 0.05           # PV que um bloco dormido devolve (fração do máximo), sem fome 4 ou mais
CURA_DIA = 2                # ... em no máximo tantos blocos por dia (10% por noite dormida)
FERIDA_DIAS = (7, 21)       # dias de repouso para a ferida sarar (ferida, grave)
PESADOS_SEM_REPOUSO = 2     # dia com tantos blocos pesados não conta para sarar
LUTA_CANSA = 2              # uma luta cansa isto

# ---------- viver (em prata) ----------
REFEICAO_PRECO = 1
CAMA_PRECO = 2              # por noite (paga-se ao deitar numa pousada)
SALARIO = dict(diarista=2, aprendiz=3, oficial=6, mestre=10)      # por bloco trabalhado (a jornada são 2 blocos)
ESFORCO_OFICIO = dict(diarista='pesado', aprendiz='pesado', oficial='leve', mestre='leve')

# ---------- treinar ----------
MAESTRIA_BLOCOS = {2: 40, 4: 160, 6: 500, 8: 1500}       # blocos de treino ou de luta com a arma para cada grau
MAESTRIA_FEITO = 6          # deste grau para cima, além dos blocos, pede um FEITO com a arma (o mundo registra)

# ---------- os eventos (o que pode acontecer; evento fora desta lista é recusado) ----------
EVENTOS = ['tempo', 'virada', 'comer', 'dormir', 'trabalhar', 'treinar', 'descansar', 'esperar', 'luta', 'compra', 'venda', 'cura', 'mestre', 'gera']
ESTADOS = ['vivo', 'morto']
