"""tabelas_manha.py — MOTOR 10, ETAPA 4b: TODOS os números do ladino (capítulo 18; o contrato: projeto/ETAPA_4B.md, seção 12).

A MANHA é o 17º caminho, o ofício do ladino: andar escondido, escutar, achar e desarmar armadilha, abrir fechadura. Sobe pela escada das armas (40, 160, 500, 1.500 blocos,
vezes o talento), com feito de Mestre para cima. Todo teste do ladino é 2d20 + o atributo ÷ 10 + a mão de manha (+ o dom escondido, + o +2 do povo) contra um número.
A GAZUA É A ARMA, A FECHADURA É A ARMADURA: conta a diferença de categoria (o item decide).
Esqueleto do alicerce (onda 1): os números são o rascunho do projeto A (projeto/etapa4b/projeto_a/PROJETO.md, anexo), a conferir pela frente L (provas_manha.py).
"""

# ---------- os testes (a lista fechada; os nomes que as outras frentes usam): o atributo, e se a mão de manha soma ----------
TESTES = {'escondido': ('Agilidade', True), 'escutar': ('Percepção', True), 'achar': ('Percepção', True), 'gazua': ('Agilidade', True), 'desarmar': ('Agilidade', True),
          'arrombar': ('Força', False), 'atencao': ('Percepção', True)}

# ---------- as contas (o número contra o qual se rola) ----------
ACHAR = (20, 6)             # 2d20 + Percepção ÷ 10 + manha, contra 20 + 6 por categoria do que está escondido (a armadilha, a passagem, o fundo falso)
GAZUA = (24, 8)             # 2d20 + Agilidade ÷ 10 + manha, contra 24 + 8 × (a categoria da fechadura ou da armadilha − a da gazua)
SEM_GAZUA = -1              # sem gazua (o grampo, a ponta da faca), ela conta um degrau abaixo do Comum
FALHA = 5                   # falhar por isto ou mais: a armadilha dispara em quem desarmava; a gazua (ou a arma de arrombar) perde 1
ARROMBAR = (24, 8)          # 2d20 + Força ÷ 10, contra 24 + 8 × (a categoria da porta − a da arma de impacto em uso); o ombro conta −1. A mão de manha não soma
ARROMBAR_ARMAS = ('maça', 'martelo', 'malho')       # as armas de impacto que arrombam
ESCUTAR = dict(madeira=22, ferro=26, pedra=26, mortos=6)     # escutar à porta: contra isto pelo material; os mortos não respiram (+6)
ESCONDIDO_ARMADURA = dict(couro=0, malha=-3, placa=-6)       # a armadura do tronco no andar escondido; sem armadura, 0
ESCONDIDO_LUZ = -6          # quem anda com luz, contra quem está no escuro
FEITO = {6: 2, 8: 3}        # Mestre: abrir ou desarmar uma Rara de verdade (não no treino); Lendário: uma Épica
TREINO_BLOCO = 1            # na masmorra, no máximo tantos blocos de treino de manha por bloco que fecha
FURTO = dict(contra=20, guarda=4, leva='1d6', pena=3, preso_dias=3)     # o furto: fica escrito, entra na etapa 3 (com a gente que lembra e a vila com justiça)
