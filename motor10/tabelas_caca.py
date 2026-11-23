"""tabelas_caca.py — MOTOR 10: TODOS os números da caça e da coleta num lugar só (a saída, o rastro, a posição, o acaso, a fuga, a cria, a coleta, a fauna dos ermos).

Os números dos bichos moram no tabelas_bichos.py (a espécie, o bando, o despojo); os do mundo, no tabelas_mundo.py; os da luta, no tabelas.py.
Mudar a caça é mudar esta página e rodar `provas_caca.py` (ou `provas_mundo.py`, que o chama).

O ERMO é um lugar sem povo, vizinho de um lugar com gente: `bichos` e `teto` (espécie: quantos há, e quantos cabem), `coleta` e `coleta_teto`
(matéria com categoria, "metal:0": quanto há, e quanto cabe). O que se tira, sai. O que nasce, nasce devagar.
"""
import tabelas as T
import tabelas_mundo as M
import tabelas_bichos as TB

# ---------- a saída: ir ao ermo vizinho, procurar, e voltar (um ato só; a pessoa segue morando no lugar dela) ----------
IDA = 1                     # blocos de ida até o ermo vizinho (o ermo pode dizer outro número no campo `longe`); a volta custa o mesmo
ARRASTA = 1                 # quem perdeu a luta e não morreu volta arrastando-se: isto a mais de blocos na volta
PROCURA = 2                 # os blocos de procura (ou de coleta) de uma saída, se ninguém disser outro número
PROCURA_MAX = 6             # uma saída não passa disto: é ir e voltar, não é morar no mato
ESFORCO = dict(ida='leve', volta='leve', procura='pesado', coleta='pesado')      # o que cada bloco pesa no corpo (tabelas_mundo.ESFORCO)

# ---------- o rastro ----------
# rastrear: 2d20 + Percepção ÷ 10 + maestria de caça (+ a pena do corpo), UMA vez por bloco de procura, contra a FARTURA do ermo:
RASTRO_BASE = 22            # o número contra, com a espécie no teto...
RASTRO_ARISCO = [0, 2, 4, 6, 8, 10]      # ... mais isto pela categoria do bicho (o bicho raro é arisco)...
RASTRO_CHEFE = 4            # ... mais isto se é chefe...
RASTRO_FALTA = 12           # ... mais isto vezes o que falta da espécie (1 − contagem ÷ teto): na metade do teto, +6; quase sumida, +12
RASTRO_ESCURO = -4          # procurar de noite ou de madrugada (bloco sem luz)
# sem alvo ("o que aparecer") o número é o de base mais a falta do ermo inteiro; o que aparece é sorteado pela contagem de cada espécie
def arisco(especie):
    e = TB.ESPECIES.get(especie)
    if not e: return 0
    return RASTRO_ARISCO[min(e['cat'], len(RASTRO_ARISCO) - 1)] + (RASTRO_CHEFE if e['chefe'] else 0)

# ---------- a posição: o que a margem do rastro dá a quem viu primeiro ----------
# passou no rastro: o caçador VIU PRIMEIRO. Se atacar, o bicho é surpreendido (perde o primeiro turno) e a luta começa longe ou perto, à escolha.
POSICAO_CADA = 5            # cada tantos pontos de margem dão UMA vantagem de terreno, à escolha...
POSICAO_MAX = 2             # ... até tantas
VANTAGENS = dict(alto=('alto', 'A'), cerco=('sem_saida', 'B'))      # a vantagem → a chave do lugar da luta e o lado (o caçador no alto; o bicho sem saída)
COLADO = 5                  # com esta margem ou mais, a luta pode começar colada (chegou ao alcance do braço sem ser visto)
INICIOS_RASTRO = ('longe', 'perto')      # os começos de quem viu primeiro (mais 'colado', com a margem acima)
INICIO_ACASO = 'perto'      # o que apareceu sem ser procurado está perto, e viu o caçador: ninguém é surpreendido, e não há vantagem de terreno
INICIO_ALCANCADO = 'colado' # quem fugiu e foi alcançado luta colado, e SURPREENDIDO (foi pego de costas)

# ---------- o acaso: aparece o que não se procurava ----------
# no bloco em que o rastro falhou (e em todo bloco de coleta), o mundo rola: a chance é a soma, sobre as espécies do ermo, de contagem × ousadia, dividida por isto
ACASO_CADA = 400
ACASO_MAX = 0.5             # nunca mais que isto por bloco
# a ÍNDOLE de cada espécie: (ousadia: o quanto ela vem ao encontro de gente · investe: a chance de atacar quem não a atacou)
INDOLE = {
    'corça': (0.1, 0.0), 'ratazana': (0.4, 0.3), 'javali': (0.4, 0.35), 'lobo': (1.0, 0.7), 'surucucu': (0.5, 0.5), 'urso': (0.6, 0.5),
    'pantera': (1.0, 0.9), 'aranha': (0.6, 0.8), 'grifo': (0.8, 0.6), 'trasgo': (1.0, 0.9), 'basilisco': (0.6, 0.7), 'serpe': (1.0, 0.9), 'hidra': (0.6, 0.9), 'dragão': (1.0, 0.8),
}
INDOLE_PADRAO = (0.6, 0.5)  # a espécie que esta página ainda não conhece
def indole(especie): return INDOLE.get(especie, INDOLE_PADRAO)
INVESTE_FUGA = 0.2          # quem corre chama o bicho: isto a mais na chance de ele vir atrás (até 1)

# ---------- fugir ----------
# 2d20 + Agilidade ÷ 10 (+ a pena do corpo) contra isto mais a Agilidade ÷ 10 do bicho. Só se testa contra o bicho que VIU o caçador (o acaso).
FUGA_BASE = 20

# ---------- a virada: os bichos criam devagar ----------
# por dia, de cada espécie nascem contagem × CRIA × (1 − contagem ÷ teto): muito devagar com poucos, devagar perto do teto, e nunca acima dele
CRIA = [0.05, 0.03, 0.012]  # por categoria (Comum, Incomum, Raro; daí para cima vale a última)
CRIA_MIN = 2                # com menos disto a espécie não cria: fica à espera de que venha de fora
VEM_DE_FORA = [20, 45, 120] # ... e de fora vem um casal, em média, a cada tantos dias (por categoria): espécie caçada até o fim some por muito tempo
CHEFE_NASCE = {3: 180, 4: 364, 5: 0}     # o chefe não cria: nasce outro, em média, a cada tantos dias enquanto a contagem está abaixo do teto (0: não nasce de novo)
def cria(cat): return CRIA[min(cat, len(CRIA) - 1)]
def vem_de_fora(cat): return VEM_DE_FORA[min(cat, len(VEM_DE_FORA) - 1)]

# ---------- a coleta (minério, madeira, erva): matéria com categoria, tirada do `coleta` do ermo ----------
# um teste por bloco: 2d20 + atributo ÷ 10 + maestria de coleta, contra COLETA_BASE + COLETA_CAT × categoria + COLETA_FALTA × (1 − quanto há ÷ teto)
COLETA = {                  # atributo do teste · quanto rende o bloco que passa · a fração do teto que volta por dia · o nome do que se tira
    'metal':   dict(atributo='Força',     rende=1, volta=0.004, nome='minério'),
    'madeira': dict(atributo='Força',     rende=2, volta=0.02,  nome='madeira'),
    'erva':    dict(atributo='Percepção', rende=1, volta=0.04,  nome='erva'),
}
COLETA_BASE = 20
COLETA_CAT = 4
COLETA_FALTA = 8
COLETA_MARGEM = 5           # passar por tantos pontos rende 1 a mais (e mais 1 a cada tantos)
COLETA_POUCO = 5            # falhar por menos disto ainda rende 1; por isto ou mais, nada

# ---------- a maestria (maestria.caça, maestria.coleta): sobe por blocos, como a das armas ----------
CACA_BLOCOS = {2: 40, 4: 160, 6: 500, 8: 1500}       # blocos de procura
FEITO_CACA = {6: 2, 8: 3}   # de Mestre para cima, além dos blocos, um FEITO: ficar com a carcaça de um bicho desta categoria ou maior (Mestre: Raro; Lendário: Épico)
COLETA_BLOCOS = {2: 40, 4: 160, 6: 500, 8: 1500}     # blocos de coleta
FEITO_COLETA = {6: 2}       # Mestre: ter tirado matéria Rara com a própria mão

# ---------- a fartura, em palavras (o que o povo sabe; a contagem é do Mestre) ----------
FARTURA = [(0.75, 'há fartura'), (0.4, 'há, mas rareou'), (0.1, 'é raro ver'), (0.0, 'quase sumiu')]
def fartura_diz(tem, teto):
    if tem <= 0: return 'sumiu'
    f = tem / teto if teto else 1
    return next(txt for lim, txt in FARTURA if f >= lim)

# ---------- a fauna e a matéria de um ermo novo (o gerador e o Mestre povoam por aqui: caca.py povoa) ----------
PERIGOS = ['borda', 'interior', 'coração']      # o perigo do ermo (1 a 3): a borda é o ermo de começo, ao lado da vila
# espécie: (o perigo a partir do qual ela vive no ermo, o teto dela ali). Só entra a espécie que vive no habitat do ermo (tabelas_bichos: habitat).
TETO = {
    'corça': (1, 80), 'ratazana': (1, 90), 'javali': (1, 40), 'lobo': (1, 12), 'surucucu': (1, 8), 'urso': (1, 3),
    'pantera': (2, 2), 'aranha': (2, 6), 'grifo': (2, 2), 'trasgo': (2, 2), 'basilisco': (3, 1), 'serpe': (3, 1), 'hidra': (3, 1), 'dragão': (3, 1),
}
# habitat: {matéria: (o perigo a partir do qual há, o teto)}
COLETA_TETO = {
    'floresta': {'madeira:0': (1, 200), 'erva:0': (1, 60), 'madeira:1': (1, 20), 'erva:1': (1, 10), 'madeira:2': (2, 4), 'erva:2': (2, 3)},
    'campo':    {'erva:0': (1, 80), 'madeira:0': (1, 40), 'erva:1': (1, 8)},
    'brejo':    {'erva:0': (1, 90), 'erva:1': (1, 20), 'madeira:0': (1, 60), 'erva:2': (2, 5)},
    'serra':    {'metal:0': (1, 150), 'metal:1': (1, 20), 'madeira:0': (1, 60), 'metal:2': (2, 5)},
    'caverna':  {'metal:0': (1, 100), 'metal:1': (1, 30), 'metal:2': (2, 6)},
    'ruína':    {'metal:0': (1, 40), 'metal:1': (1, 10), 'erva:0': (1, 30), 'metal:2': (3, 4)},
}
HABITATS = list(COLETA_TETO)


def fauna(habitat, perigo=1):
    """{espécie: teto} de um ermo novo deste habitat e deste perigo"""
    return {esp: teto for esp, (desde, teto) in TETO.items() if esp in TB.ESPECIES and habitat in TB.ESPECIES[esp]['habitat'] and desde <= perigo}


def materia(habitat, perigo=1):
    """{matéria: teto} de um ermo novo deste habitat e deste perigo"""
    return {bem: teto for bem, (desde, teto) in COLETA_TETO.get(habitat, {}).items() if desde <= perigo}
