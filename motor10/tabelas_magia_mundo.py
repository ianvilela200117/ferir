"""tabelas_magia_mundo.py — MOTOR 10: TODOS os números do MUNDO DA MAGIA num lugar só (etapa da magia, capítulos 12 a 14).

Estudar um feitiço e seguir uma tradição; a Mana fora da luta; o voto, o laço e a dívida; lançar fora da luta e os ritos; tratar ferida; a alquimia (a leva, as nove
receitas, beber); o encanto (gravar, o foco e o amuleto); a maldição (o relógio de 6 passos, quebrar). Os números da luta moram no tabelas_magia.py (a frente da luta);
a base comum (a Conjuração, a Firmeza, a guarda, a Mana máxima, a cura, os 24 feitiços e o truque), no tabelas.py; o vocabulário do estado, no tabelas_mundo.py;
o preço dos bens novos, no tabelas_mercado.py. Mudar o mundo da magia é mudar esta página e rodar `provas_magia.py` (ou `provas_mundo.py`, que o chama).
"""
import tabelas as T
import tabelas_mundo as M

# ---------- estudar um feitiço (conta B.7) ----------
ESTUDO = [3, 6, 18, 54, 162]        # blocos LEVES de estudo por grau do feitiço (0 é o truque), vezes o talento na tradição dele. Contam como treino da tradição
ESTUDO_ESFORCO = 'leve'
TRUQUE_TRADICAO = 'arcano'          # o truque (luz, de todas as tradições) estudado por quem não segue tradição nenhuma conta como treino desta
# AS FONTES: quem saiba o feitiço e queira ensinar (cobra o salário do grau de ofício dele por bloco, tabelas_mundo.SALARIO, e só ensina dentro da jornada dele:
# 2 blocos pagos por dia), um ESCRITO que o ensine (item do Livro de Itens), um SANTUÁRIO (os feitiços da fé, a quem tem voto) ou o ERMO DO LAÇO (os do verde, a quem tem laço)

# ---------- a Mana fora da luta (conta B.3 e B.6) ----------
MANA_DORME = 0.25                   # por bloco dormido: esta fração da Mana máxima (arredonda para o mais perto, no mínimo 1)
MANA_DESCANSO = 0.125               # por bloco de descanso
MANA_ACORDADO = dict(leve=1, nada=1, pesado=0)      # por bloco acordado, em pontos: o leve e o parado devolvem 1; o pesado, nada
MANA_ERMO = 2.0                     # o druida (verde) no ermo: a volta em dobro...
MANA_MUROS = 0.5                    # ... e entre muros, a metade
MUROS = ('cidade', 'masmorra')      # os tipos de lugar que são "entre muros"
PACTO_SOZINHA = 0.5                 # a bruxa (pacto): a Mana volta sozinha só até esta fração da máxima; o resto paga-se (rito "paga")...
PACTO_PV = 0.02                     # ... esta fração do PV máximo por ponto de Mana...
PACTO_DIVIDA = 4                    # ... ou 1 de dívida a cada tantos pontos
PRECE_FORA = 0.5                    # o clérigo (fé): a Mana só volta com a PRECE (1 bloco por dia): no santuário enche; fora dele, esta fração da máxima
CASA_SONO = 2                       # O DESCANSO EM CASA de quem não é o personagem (corpo.casa; tabelas_mundo.CASA_NOITE): cada dia inteiro em casa vale tantos blocos dormidos
CASA_ESFORCO = 'nada'               # ... e o resto do dia acordado, neste esforço (a regra de cada bloco, acima); o clérigo reza a prece do dia em casa (no santuário enche; longe, metade)

# ---------- as tradições: o voto, o laço, o pacto (conta B.6) ----------
VOTO_LAMINA = ('corte', 'ponta')    # o voto da lâmina: não põe em uso arma destes golpes (pôr é quebrar)
VOTO_POBREZA = 50                   # o voto da pobreza: na virada, a prata acima disto vai para o caixa do santuário do voto
FARTURA = [(0.10, -4), (0.40, -2)]  # o laço do druida: a fartura do ermo (contagem ÷ teto) abaixo disto tira isto da Conjuração (a luta lê: magia_mundo.pena_laco)
PACTO_ABRE = 1                      # o pacto nasce devendo isto
PACTO_BLOCOS = (0, 5)               # o pacto só se faz no escuro (madrugada ou noite)
DIVIDA_GRAU = {2: 1, 3: 2, 4: 3}    # a dívida que um feitiço de pacto soma ao ser lançado, pelo grau
DIVIDA_PRAGA = 1                    # a praga soma a categoria dela mais isto
DIVIDA_PV = 0.05                    # pagar a dívida em PV (rito de 1 bloco): 1 ponto a cada tantos do PV máximo...
DIVIDA_MATERIA = 4                  # ... ou queimando tantas unidades de osso ou de erva (da categoria do foco) por ponto
DIVIDA_LIMITE = 10                  # a dívida acima de Vontade ÷ isto vira maldição na própria bruxa (a "Conta": quebra quando a dívida zera)

# ---------- lançar fora da luta e os ritos ----------
RITO_BLOCOS = 1                     # todo rito (prece, ler, quebrar, praga, benzer, pagar a dívida, fazer o voto ou o laço) leva tantos blocos LEVES
SEM_FOCO = -4                       # a Conjuração de quem lança sem foco: Comum, com isto
FOCO_OUTRO = 1                      # o foco de outra tradição rende tantas categorias abaixo
LER_FE = 4                          # quem lê (a maldição, o dom, a peça): quem sabe o feitiço "ler", ou quem é da fé com mão de Treinado para cima
BENCAO_DURA = 1                     # a bênção dada antes da luta vale tantos blocos a contar do seguinte (a luta que abre dentro deles leva o benzido)
SEIVA = 2                           # a seiva fora da luta: a cura da noite vale isto vezes (a noite seguinte)
AGUA_BENTA = dict(erva=1, mana=2)   # o clérigo benze 1 de erva Comum com 2 de Mana num santuário: rende 1 de água benta (rito)
AGUA_BENTA_RENDE = 3                # ... por rito, até tantas (cada uma pede a sua erva e a sua Mana)
BENZER_ARMA = 2                     # benzer uma arma (rito, num santuário): esta Mana; vale tabelas_mundo.BENTA_DURA (7 dias)

# ---------- tratar a ferida (o ofício "cura") ----------
TRATAR = 1                          # um tratamento (1 bloco leve e 1 remédio; um por paciente por dia) soma tantos dias de repouso a todas as feridas dele
TRATAR_DOM = 0.5                    # ... e o dom da cura soma isto por grau
TRATAR_MAO = (2, 4)                 # a mão de cura que tratar pede: Iniciante na ferida; Treinado se há ferida grave

# ---------- a alquimia: a leva, no molde da forja (conta C.1 e C.3) ----------
BOTICAS = ['panela', 'botica de vila', 'botica de cidade', 'laboratório', 'grande laboratório']      # o nível soma no teste (0 a 4)
ALQUIMIA_ATE = 5                    # faz-se poção até o Lendário
RECEITAS = {                        # as unidades de matéria da leva, na categoria dela (do Épico para cima: matéria Rara, mais um NÚCLEO da categoria).
    'cura':            {'erva': 4},     # A RECEITA LEVA 8 DE PREÇO DE BASE NA COMUM (vezes 6 por categoria): dois terços do que valem as 2 doses (12); a quebra-maldição, 14. Comprada na loja e vendida à loja,
    'antídoto':        {'erva': 3, 'osso': 2},      # a leva não paga a matéria (a loja paga 60% a 80%); é o que impede a mina (provas_magia, MG8 e MG9)
    'veneno':          {'peçonha': 4},              # o veneno de lâmina: 1 dose = 1 golpe; só até o Raro (é o que há de peçonha)
    'mana':            {'erva': 4},
    'guarda':          {'osso': 2, 'erva': 3},
    'fúria':           {'erva': 3, 'osso': 2},
    'vigília':         {'erva': 4},
    'quebra-maldição': {'água benta': 2, 'erva': 3, 'osso': 2},    # mais a água benta (bem sem categoria: a mesma em toda leva): é a mais cara
}
REMEDIO = {'erva:0': 3}             # a nona receita: o remédio (o bem que já existe) sai de 3 de erva Comum, numa leva Comum, e rende 1
VENENO_ATE = M.POCAO_ATE            # o veneno de lâmina não passa do Raro (a peçonha vai até o Raro)
DOSES = 2                           # a leva do Comum ao Raro rende tantas doses (bem, na carga: "cura:0")
ELIXIRES = 6                        # a leva do Épico para cima rende tantos elixires (itens do Livro, contados no mundo)
AGUADA = 1                          # a leva Comum que falha por pouco sai aguada: rende tantas doses (a das outras categorias sai uma categoria abaixo)
PREPAROS_ALQUIMIA = dict(receita=('pessoa', 'prep_alquimia'), ajudante=('pessoa', 'prep_ajudante'), fogo=('lugar', 'fogo'), vidraria=('lugar', 'vidraria'))     # +2 cada um, até +8 (o dom dentro)
POVO_POCOES = ('cura', 'antídoto', 'vigília')       # as poções que a botica de um lugar faz para o povo (o mercado as produz até a categoria da botica)...
SANTUARIO_POCOES = ('quebra-maldição',)             # ... e esta, só onde há também santuário (a água benta)
BOTICA_FAZ = {0: -1, 1: 0, 2: 1, 3: 2, 4: 2}        # a botica do lugar faz para o povo poções até esta categoria (a panela, nenhuma; a de vila, só a Comum)

# ---------- beber fora da luta (conta C.3) ----------
MANA_POCAO = 4                      # a poção de Mana devolve isto por degrau (Comum 4, Incomum 8, Raro 12, Épico 16)
VIGILIA = dict(sono=-3, cansaco=-2)  # a poção de vigília tira isto; uma por dia
GUARDA_DURA = 1                     # a poção de guarda: por tantos blocos, conta como amuleto da categoria dela (contra a maldição e o lugar maldito; a luta lê marca.guarda)
ENJOO_DURA = 1                      # quem passa das doses do dia e falha o Vigor enjoa: −2 em tudo por tantos blocos (marca.enjoo; o corpo lê)
QUEBRA_RECUA = 2                    # a poção quebra-maldição da categoria da maldição faz o relógio recuar tantos passos (nunca abaixo do 1)
SO_NA_LUTA = ('antídoto', 'fúria')  # fora da luta não fazem nada (não há veneno a tirar; a fúria é de 5 rodadas): beber é recusado

# ---------- o encanto (conta E) ----------
RUNAS = ['pedra riscada', 'mesa de runas', 'oficina de runas', 'grande oficina', 'oficina mestra']      # a bancada do encanto (lugar.runas, 0 a 4): o nível soma no teste
def blocos_gravar(cat): return max(1, 3 ** cat // 3)    # gravar leva um terço dos blocos da forja: Comum e Incomum 1, Raro 3, Épico 9, Único 27, Lendário 81
ESSENCIA = dict(osso=4, erva=2)     # a essência de gravar, até o Raro, na categoria da peça; do Épico para cima, um NÚCLEO da categoria
ESTRAGO = 5                         # gravar que falha por 5 ou mais: a essência some e a peça perde isto de durabilidade...
MALDITA_FALHA = 10                  # ... e falhar por isto ou mais deixa a peça MALDITA (é de onde vêm as peças malditas do mundo)
PREPAROS_ENCANTO = dict(receita=('pessoa', 'prep_encanto'), ajudante=('pessoa', 'prep_ajudante'), tinta=('lugar', 'tinta'), pedra=('lugar', 'pedra'))
# o foco e o amuleto se fazem no ofício do encanto, na mesa de runas, com os blocos, o teste e a falha da forja (a matéria: tabelas_mundo.MATERIA_FOCO e MATERIA_AMULETO)

# ---------- a maldição (conta D.3 e D.4; o tipo, a condição e o saber: mundo 5) ----------
def forca(cat): return 2 + 4 * cat  # a força da maldição: na virada de cada dia, 2d20 + a força contra a Firmeza do amaldiçoado; venceu, anda um passo
FIM_PV = 0.10                       # no passo 5 (o fim à vista), cada virada tira esta fração do PV máximo
QUEBRAR = (28, 2)                   # o rito do clérigo (quebrar-maldição, 1 bloco, uma tentativa por dia): 2d20 + Conjuração contra 28 + a força + 2 por passo além do primeiro
QUEBRAR_MARCA = 5                   # o rito que falha por tanto ou mais: o clérigo leva a marca (a mesma maldição, no passo 1)
SAIR_DIAS = 7                       # a maldição do lugar quebra quando a pessoa passa tantos dias sem pôr o pé nele
SINAIS = {                          # o que a pessoa sente quando desconfia (do passo 2, ou quando alguém lhe disse que algo a tocou): sem tipo, sem categoria, sem prazo
    'míngua':  'acorda mais fraco do que deitou, e isto não é doença',
    'chaga':   'a pele arde onde nada a feriu, e a ferida custa a fechar',
    'azar':    'tudo sai torto, até o que sempre saiu direito',
    'insônia': 'não descansa nem dormindo',
    'marca':   'os outros desviam os olhos, e os bichos olham demais',
}
NOMES = {'míngua': 'a Míngua', 'chaga': 'a Chaga', 'azar': 'o Azar', 'insônia': 'a Vigília Negra', 'marca': 'a Marca'}       # o nome da maldição que nasce sem nome (do encanto que falhou, do voto, da dívida)
def preco_quebrar(cat): return 10 * M.PECA_VEZES ** cat      # o serviço do clérigo que quebra: um terço do preço de tabela da categoria (10, 60, 360, 2.160)

# ---------- os serviços de pessoa a pessoa (evento "servico": a prata só muda de mão) ----------
SERVICO = dict(ler=10, cura=3, bencao=5, tratar=2, agua=4, benzer=5, praga=10)      # o que cobra quem presta, por vez (ler: o rito; cura: o lance; bênção: por pessoa;
                                                                                     # tratar: mais o remédio; água benta: cada uma; benzer a arma; a praga, mais a dívida dela)
