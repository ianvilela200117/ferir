"""tabelas_manha.py, MOTOR 10, ETAPA 4b: TODOS os números do ladino (capítulo 18; o contrato: projeto/ETAPA_4B.md, seção 12).

A MANHA é o 17º caminho, o ofício do ladino: andar escondido, escutar, achar e desarmar armadilha, abrir fechadura. Sobe pela escada das armas (40, 160, 500, 1.500 blocos,
vezes o talento), com feito de Mestre para cima. Todo teste do ladino é 2d20 + o atributo ÷ 10 + a mão de manha (+ o dom escondido, + o +2 do povo) contra um número.
A GAZUA É A ARMA, A FECHADURA É A ARMADURA: conta a diferença de categoria (o item decide).
Mudar o ladino é mudar esta página e rodar `provas_manha.py` (ou `provas_mundo.py`, que o chama). O preço da gazua e da tocha, e o que o povo gasta de tocha, moram no
tabelas_mercado.py; a forja da gazua, no tabelas_oficio.py.
"""

# ---------- os testes (a lista fechada; os nomes que as outras frentes usam): o atributo, e se a mão de manha soma ----------
TESTES = {'escondido': ('Agilidade', True), 'escutar': ('Percepção', True), 'achar': ('Percepção', True), 'gazua': ('Agilidade', True), 'desarmar': ('Agilidade', True),
          'arrombar': ('Força', False), 'atencao': ('Percepção', True)}
NOMES = {'escondido': 'andar escondido', 'escutar': 'escutar', 'achar': 'achar', 'gazua': 'abrir a fechadura', 'desarmar': 'desarmar a armadilha',
         'arrombar': 'arrombar', 'atencao': 'notar a emboscada'}        # como cada teste se diz à mesa

# ---------- as contas (o número contra o qual se rola) ----------
ACHAR = (20, 6)             # 2d20 + Percepção ÷ 10 + manha, contra 20 + 6 por categoria do que está escondido (a armadilha, a passagem, o fundo falso)
GAZUA = (24, 8)             # 2d20 + Agilidade ÷ 10 + manha, contra 24 + 8 × (a categoria da fechadura ou da armadilha − a da gazua)
SEM_GAZUA = -1              # sem gazua (o grampo, a ponta da faca), ela conta um degrau abaixo do Comum
FALHA = 5                   # falhar por isto ou mais: a armadilha dispara em quem desarmava; a gazua (ou a arma de arrombar) perde 1 de durabilidade
ARROMBAR = (24, 8)          # 2d20 + Força ÷ 10, contra 24 + 8 × (a categoria da porta − a da arma de impacto em uso). A mão de manha não soma
ARROMBAR_ARMAS = ('maça', 'martelo', 'malho')       # as armas de impacto que arrombam
OMBRO = -1                  # arrombar sem arma de impacto em uso: o ombro conta um degrau abaixo do Comum
ESCUTAR = dict(madeira=22, ferro=26, pedra=26, mortos=6)     # escutar à porta: contra isto pelo material; os mortos não respiram (+6)
ESCONDIDO_ARMADURA = dict(couro=0, malha=-3, placa=-6)       # a armadura do tronco no andar escondido; sem armadura, 0
ESCONDIDO_LUZ = -6          # quem anda com luz, contra quem está no escuro

# ---------- a mão: o feito e o treino ----------
FEITO = {6: 2, 8: 3}        # Mestre: abrir ou desarmar uma Rara de verdade (não no treino); Lendário: uma Épica (a categoria mais alta fica em marca.feito_manha)
TREINO_BLOCO = 1            # na masmorra, no máximo tantos blocos de treino de manha por bloco que fecha (em que a pessoa andou escondida, escutou, procurou, abriu ou desarmou)
TREINO_ESFORCO = 'pesado'   # o treino em casa (`manha.py treinar N`, com uma gazua: a fechadura velha, o passo macio no pátio) é bloco pesado, como o treino de arma
TREINO_PEDE_GAZUA = True    # sem gazua não há fechadura para treinar: o treino em casa pede uma
CHANCE_CATS = (0, 1, 2)     # a mesa do ladino mostra a chance contra estas categorias (Comum, Incomum, Rara)

# ---------- o furto (fica escrito; entra na etapa 3, com a gente que lembra e a vila com justiça) ----------
FURTO = dict(contra=20, guarda=4, leva='1d6', pena=3, preso_dias=3)     # 2d20 + Agilidade ÷ 10 + manha contra 20 + Percepção ÷ 10 da vítima (+4 se guarda ou mercador);
                            # passou: 1d6 × (1 + metade do grau de manha) de prata; falhou por 5 ou mais: crime (devolve e paga o triplo, ou 3 dias preso)
FURTO_LIGADO = False        # desligado nesta etapa: o `manha.py furtar` recusa com a frase (o ladino de começo tiraria uns 34 de prata por dia da bolsa da vila: é mina)

# ---------- a vila de teste (manha.na_vila): o Quim, o ladino da vila ----------
QUIM = dict(id='quim', nome='Quim', sobre='o sobrinho do Lino; abre trinco, anda calado e acha o que os outros não veem', nivel=14, molde='arqueiro',
            grau_oficio='diarista', maestria={'manha': 2, 'adaga': 2}, moedas=10,
            pecas=[('arma', 'adaga', 0, 'arma'), ('armadura', 'couro', 0, 'veste'), ('gazua', None, 0, None)])
            # nível 14, a manha de Iniciante (os 40 blocos que explicam a mão), adaga e couro Comuns, uma gazua Comum, 10 de prata; nasce com o talento e o dom rolados
