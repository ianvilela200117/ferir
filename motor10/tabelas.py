"""tabelas.py — MOTOR 10: TODOS os números da luta e dos itens num lugar só.

Nenhum outro script do Motor 10 traz número de regra. Mudar o jogo é mudar esta página e rodar `provas.py`:
se uma meta do banco de provas quebra, a mudança não entra.
(Os números dos BICHOS moram na página deles, o tabelas_bichos.py: o corpo do bicho usa a mesma escala de categoria daqui.)

A ESCALA (a regra de ouro do Motor 10, "o item decide"):
  cada categoria vale o TRIPLO da de baixo, na arma E na armadura, e o que conta é a DIFERENÇA entre as duas.
    dano = dado × K_DANO × valor da arma ÷ proteção da parte atingida, vezes a força de quem bate
    mesma categoria ......... o golpe passa inteiro (× 1)
    arma UMA acima .......... × 3            armadura UMA acima ....... um terço
    arma DUAS acima ......... × 9            armadura DUAS acima ...... um nono
    arma TRÊS acima ......... × 27           armadura TRÊS acima ...... quase nada (só o crítico arranha)
  Por isso um duelo entre iguais dura o mesmo em qualquer degrau, e quem está mal armado não fere quem está bem vestido.
"""

CATS = ['Comum', 'Incomum', 'Raro', 'Épico', 'Único', 'Lendário', 'Mítico', 'Primordial']
ATRIBUTOS = ['Força', 'Agilidade', 'Vigor', 'Vontade', 'Percepção', 'Afinidade']

# ---------- a categoria ----------
MULT = [1, 3, 9, 27, 81, 243, 729, 2187]       # o valor da arma: o triplo a cada categoria
RD = [1, 3, 9, 27, 81, 243, 729, 2187]         # a proteção da armadura de MALHA: DIVIDE o golpe (couro e placa: MATERIAIS)
NU = 1 / 3                                     # a proteção de uma parte sem armadura (um degrau abaixo do Comum)
K_DANO = 4.0                                   # o tamanho do golpe entre iguais (afina a duração da luta)
BON = [0, 4, 8, 12, 16, 20, 24, 28]            # acerto da arma; e Defesa, do escudo ou da arma que apara
DUR = [10, 20, 30, 40, 50, 60, 80, 100]        # durabilidade de uma peça nova
NUCLEO_DUR = 1                                 # o núcleo (item do Livro, tipo 'nucleo': o que a obra Épica ou maior pede) não gasta: 1 de 1

# ---------- as armas ----------
# dado · golpe (corte, ponta, impacto) · alcance em casas (1 casa ≈ 3 m) · mãos · peso · apara (Defesa a mais) · à distância?
FAMILIAS = {
    'punho':    dict(dado='1d4',  golpe='impacto', alcance=1,  maos=1, peso='leve'),
    'adaga':    dict(dado='1d4',  golpe='ponta',   alcance=1,  maos=1, peso='leve', atributo='Agilidade'),
    'espada':   dict(dado='1d8',  golpe='corte',   alcance=1,  maos=1, peso='media', apara=2),
    'maça':     dict(dado='1d8',  golpe='impacto', alcance=1,  maos=1, peso='media'),
    'machado':  dict(dado='1d10', golpe='corte',   alcance=1,  maos=1, peso='pesada'),
    'martelo':  dict(dado='1d10', golpe='impacto', alcance=1,  maos=1, peso='pesada'),
    'lança':    dict(dado='1d8',  golpe='ponta',   alcance=2,  maos=1, peso='media'),
    'montante': dict(dado='1d12', golpe='corte',   alcance=1,  maos=2, peso='pesada', apara=2),
    'alabarda': dict(dado='1d12', golpe='corte',   alcance=2,  maos=2, peso='pesada'),
    'malho':    dict(dado='1d12', golpe='impacto', alcance=1,  maos=2, peso='pesada'),
    'arco':     dict(dado='1d8',  golpe='ponta',   alcance=12, maos=2, peso='media', distancia=True, atributo='Agilidade'),
    'besta':    dict(dado='1d10', golpe='ponta',   alcance=12, maos=2, peso='media', distancia=True, recarga=1),
}
DUAS_MAOS = 1.25            # a arma de duas mãos de corpo a corpo multiplica o valor por isto (arco e besta, não)
HASTE_COLADO = -2           # arma de alcance 2 contra quem está colado: a haste atrapalha
BESTA_FORCA = 1.2           # a besta não usa o braço: a força do golpe dela é fixa
ESCUDO_BASE = 4             # o escudo dá isto na Defesa, mais o bônus da categoria dele (a arma que apara dá só o bônus da dela)
QUEBRADA = -4               # arma quebrada: um pedaço de ferro Comum, com isto no acerto

# ---------- as armaduras ----------
# fator da proteção · o que pede de Força · fôlego a mais por rodada em que a pessoa age · Defesa · iniciativa
# (a Defesa e a iniciativa são as da peça que cobre o tronco: o couro deixa esquivar, a placa prende)
MATERIAIS = {
    'couro': dict(rd=0.7, pede=40, folego=0, defesa=3, ini=2),
    'malha': dict(rd=1.0, pede=60, folego=0, defesa=0, ini=0),
    'placa': dict(rd=1.4, pede=80, folego=1, defesa=-2, ini=-2),
}
SEM_ARMADURA = dict(defesa=3, ini=2)            # quem não veste nada no tronco se mexe como quem veste couro
# o golpe contra o material: a proteção da peça vezes isto
MATRIZ = {
    'corte':   dict(couro=0.85, malha=1.1, placa=1.3),   # o fio abre o couro e escorrega no metal
    'ponta':   dict(couro=1.0, malha=0.85, placa=1.15),  # a ponta abre o elo da malha
    'impacto': dict(couro=1.15, malha=1.0, placa=0.7),   # o malho amassa a placa
}
PARTES = ['cabeça', 'tronco', 'braços', 'pernas']
ONDE = {1: 'cabeça', 2: 'braços', 3: 'braços', 4: 'tronco', 5: 'tronco', 6: 'tronco', 7: 'tronco', 8: 'pernas', 9: 'pernas', 10: 'pernas'}   # onde o golpe cai (d10)

# ---------- o requisito (por ATRIBUTO, nunca por nível) ----------
PEDE_PESO = {'leve': 40, 'media': 60, 'pesada': 80}     # o que a arma pede de Força (ou do "atributo" da família)
AJUSTE_PESO = 20            # os efeitos "leve" e "pesa" tiram ou põem isto no que a peça pede
FALTA_ACERTO = 5            # cada 5 pontos que faltam: −1 no acerto (arma) ou na Defesa (armadura e escudo)
FALTA_FOLEGO = 10           # cada 10 pontos que faltam: +1 de fôlego por golpe (arma) ou por rodada (armadura)
SOB_MEDIDA = 10             # sob medida: o requisito cai 10 por grau do ferreiro, só para o dono
SOB_MEDIDA_GRAUS = (1, 4)   # os graus que existem
SOB_MEDIDA_PROT = 1.1       # a armadura sob medida protege isto vezes, no dono
NAO_E_DELE = 1              # peça sob medida na mão de outro rende esta quantidade de categorias abaixo
SINTONIA = 20               # peças Épicas ou melhores que a pessoa sustenta: Vontade ÷ isto (no mínimo 1)
SINTONIA_DESDE = 3          # o índice da categoria Épico
SINTONIA_ABAIXO = 1         # a peça que passa do limite rende esta quantidade de categorias abaixo, e os efeitos dela dormem
def devolve_max(cat): return 4 * (cat + 1)      # o teto do efeito "devolve" pela categoria da peça

# ---------- a pessoa ----------
DEF_BASE = 22               # Defesa = isto + Agilidade ÷ 20 + maestria ÷ 2 + o da armadura + o escudo, ou o aparo da arma
def acerto_base(maestria, forca, agil): return maestria + (forca // 10 + agil // 10) / 4
def defesa_base(maestria, agil): return DEF_BASE + (agil // 10) / 2 + maestria / 2
def pv_max(vigor, nivel): return vigor * 2 + nivel // 4
def folego_max(vigor): return 6 + vigor // 10
FOLEGO_MIN = 2              # o cansaço do corpo não baixa o fôlego máximo além disto
def forca_mult(atributo): return 1 + (atributo // 10) * 0.03      # a força empurra o que o aço abriu
MAESTRIAS = {0: 'Leigo', 2: 'Iniciante', 4: 'Treinado', 6: 'Mestre', 8: 'Lendário'}
ACOES = 2                   # as ações de todo mundo, por rodada
def esforcos(maestria):
    """as ações A MAIS que a pessoa pode fazer na rodada, cada uma com o multiplicador do custo de fôlego"""
    return [1, 2] if maestria >= 8 else [1] if maestria >= 6 else [2]
def reacoes(maestria): return 1 + (1 if maestria >= 8 else 0)

# gente GERADA (o mundo, os testes): os atributos de nascença e como os pontos do nível (1 por nível) se repartem
MOLDES = {
    'guerreiro': (dict(Força=70, Agilidade=60, Vigor=70, Vontade=50, Percepção=50, Afinidade=40), dict(Força=.30, Agilidade=.20, Vigor=.25, Vontade=.10, Percepção=.10, Afinidade=.05)),
    'arqueiro':  (dict(Força=55, Agilidade=75, Vigor=60, Vontade=50, Percepção=65, Afinidade=40), dict(Força=.15, Agilidade=.35, Vigor=.20, Vontade=.10, Percepção=.15, Afinidade=.05)),
    'comum':     (dict(Força=50, Agilidade=50, Vigor=50, Vontade=45, Percepção=45, Afinidade=40), dict(Força=.20, Agilidade=.20, Vigor=.20, Vontade=.15, Percepção=.15, Afinidade=.10)),
}
def maestria_tipica(nivel):
    """a maestria que um combatente GERADO costuma ter naquele nível. Quem joga ganha maestria por treino e feito, não por nível."""
    return 0 if nivel < 10 else 2 if nivel < 25 else 4 if nivel < 50 else 6 if nivel < 150 else 8

# ---------- a luta ----------
CRIT_OUTRO = 11             # crítico: um dado deu 20 e o outro deu isto ou mais
INICIO = {'longe': 8, 'perto': 3, 'colado': 1}   # a distância entre as duas frentes quando a luta começa
PASSO = 2                   # casas por ação de andar
CERCO = 4                   # em campo aberto, quantos batem corpo a corpo no mesmo alvo na mesma rodada
CERCO_HASTE = 2             # e quantos mais, com arma de alcance 2, por cima do ombro dos outros
SEGURA = 2                  # cada um de pé na frente segura este tanto de inimigos; quem sobra contorna
FLANCO = 3                  # cada um que já bateu no alvo nesta rodada tira isto da Defesa dele para o próximo
FLANCO_MAX = 3              # ... até este tanto de vezes
MIRA_ACERTO = -8            # MIRAR A FRESTA: isto no acerto...
MIRA_PROT = 3               # ... e a armadura melhor que a arma protege isto vezes menos (conta uma categoria abaixo)
ENTRE = -2                  # golpe ou tiro com alguém de pé no caminho
TIRO_FUGINDO = -4           # atirar no mesmo turno em que recuou de alguém colado
POSTURAS = {'firme': (0, 0, 0), 'agressiva': (2, -2, 0), 'defensiva': (-2, 2, 1)}   # acerto, Defesa, fôlego a mais por rodada
SEM_FOLEGO = 4              # sem fôlego: −isto no acerto e na Defesa, e uma ação só
TOMA_FOLEGO = ('1d4', 1)    # tomar fôlego devolve o dado mais isto
RESGUARDO = 2               # quem toma fôlego ou espera: +isto na Defesa até o próximo turno
CHAO = -4                   # no chão: isto na Defesa
PRESO = -2                  # perna gravemente ferida: isto na Defesa, e não anda
ABALADO = -2                # abalado: isto no acerto
# a ferida
FERIDA = 0.25               # golpe que tira esta fração do PV máximo abre uma FERIDA
FERIDA_GRAVE = 0.50         # e esta, uma ferida GRAVE (e é um "golpe terrível" para a moral de quem vê)
FERIDA_MIN = 0.05           # o crítico só abre ferida se tirar pelo menos isto do PV máximo
FERIDAS = dict(cabeça=(1, 2), braços=(-2, -4), tronco=(3, 6))   # ações perdidas · acerto · fôlego perdido (ferida, grave)
SANGRA = 0.20               # quem sangra perde por rodada esta fração do golpe que abriu a ferida
SANGRA_RODADAS = (3, 5)     # por quantas rodadas (ferida, grave)
MORTE_CD = 12               # caído: d20 contra isto por rodada; 3 falhas morre, 3 sucessos estável
IMPASSE = 8                 # rodadas seguidas sem ninguém ferir ninguém de verdade: os lados se separam
IMPASSE_MIN = 0.02          # "de verdade": o PV tirado na rodada, somadas as frações do PV máximo de cada um, chega a isto
MAX_RODADAS = 60
RETIRADA = 8                # quem tem ordem de recuar e acaba a rodada a esta distância (em casas) de todo inimigo de pé saiu da luta
# o tempo e o lugar
TEMPO = {
    'escuro':  dict(acerto=-4, tiro=-8),
    'chuva':   dict(tiro=-4),
    'vento':   dict(tiro=-2),
    'neblina': dict(tiro=-4, sem_tiro_longe=3),
    'lama':    dict(passo=1),
    'calor':   dict(folego_armadura=1),
    'água':    dict(passo=1, defesa=-2, folego=1),
}
ALTO = dict(acerto=1, tiro=2)       # quem está no alto
COBERTURA = -4                      # tiro contra quem tem cobertura
# a moral: 2d20 + Vontade ÷ 10 + o que ajuda, contra o susto
MORAL = dict(lider_caiu=29, metade_caiu=26, golpe_terrivel=24, ferido_grave=26)
MORAL_LIDER = 2             # com o líder de pé
MORAL_MAIS = 2              # o lado dele tem mais gente de pé
MORAL_MENOS = -4            # o outro lado tem o dobro
MORAL_QUEBRA = 10           # falhar por isto ou mais: quebra de uma vez

# ---------- a magia: A BASE COMUM (etapa da magia; as duas frentes leem daqui, e a frente da luta afina os SEUS números no tabelas_magia.py) ----------
# A magia usa a conta do aço, linha por linha: o foco é a arma de quem lança, o amuleto é a armadura contra a magia, e só a diferença de categoria conta.
TRADICOES = {'arcano': 'Afinidade', 'fé': 'Vontade', 'verde': 'Percepção', 'pacto': 'Afinidade'}     # as quatro tradições e o atributo da Conjuração de cada uma
FOCOS = {   # a forma do foco: mãos · vezes o valor da categoria (o cajado, como toda arma de duas mãos) · o que pede (por atributo, nunca por nível) · de que tradições é
    'varinha': dict(maos=1, vezes=1.0, pede=('Afinidade', 40), de=('arcano',)),
    'cajado':  dict(maos=2, vezes=DUAS_MAOS, pede=('Afinidade', 60), de=('arcano', 'verde'), apara=True, dado='1d6', golpe='impacto'),     # o cajado apara (o bônus da categoria) e bate como arma leve
    'símbolo': dict(maos=1, vezes=1.0, pede=('Vontade', 60), de=('fé',)),
    'talismã': dict(maos=1, vezes=1.0, pede=('Vontade', 40), de=('pacto',)),
}
GUARDA_ARMADURA = 0.6       # sem amuleto, a armadura do tronco (e o couro do bicho) guarda contra a magia esta fração do valor dela (decisão do jogador, M1 a)
GUARDA_NU = NU              # sem amuleto e sem armadura no tronco: um terço
def guarda(amuleto_cat=None, tronco_cat=None):
    """a guarda contra a magia: o valor do amuleto, ou 0,6 do valor da armadura do tronco, o que for maior; sem um nem outro, um terço. O material e a parte do corpo não contam."""
    g = [MULT[amuleto_cat]] if amuleto_cat is not None else []
    if tronco_cat is not None: g.append(RD[tronco_cat] * GUARDA_ARMADURA)
    return max(g) if g else GUARDA_NU
FIRMEZA_BASE = 22           # a Firmeza é a Defesa da cabeça: a mesma forma da Defesa do corpo
def conjuracao(maestria, atributo, foco_cat, dom=0):
    """o acerto de quem lança: a maestria da tradição, o dom nela, metade do bônus do atributo da tradição e o bônus do foco"""
    return maestria + dom + (atributo // 10) / 2 + BON[foco_cat]
def firmeza(vontade, maestria_maior, amuleto_cat=None, tronco_cat=None, dom=0):
    """contra o que prende, assusta ou amaldiçoa: 22, metade do bônus de Vontade, metade da maior maestria da pessoa, metade do dom de tradição, e o melhor entre o bônus
    do amuleto e metade do bônus da armadura do tronco (como na guarda: o amuleto fraco não tira o que a armadura boa já dava). O calejo da luta soma por cima (é da frente da luta)."""
    b = [BON[amuleto_cat]] if amuleto_cat is not None else []
    if tronco_cat is not None: b.append(BON[tronco_cat] / 2)
    return FIRMEZA_BASE + (vontade // 10) / 2 + maestria_maior / 2 + dom / 2 + (max(b) if b else 0)
def mana_max(afinidade, vontade, maestria, dom=0): return (afinidade + vontade) // 10 + maestria + dom      # o fôlego da magia: (Afinidade + Vontade) ÷ 10, a maestria da tradição e o dom nela
CURA_K = 6                  # a lei ao contrário: a cura devolve dado × 6 × 3 elevado a (categoria da cura − categoria da ferida mais funda)
def cura(dado, cat_cura, cat_funda): return dado * CURA_K * 3 ** (cat_cura - (cat_funda or 0))
CURA_TETO = 0.5             # por pessoa e por dia, feitiço e poção somados não devolvem mais que esta fração do PV máximo
def doses_dia(vigor): return max(1, vigor // 30)        # quantas poções se bebem por dia sem enjoar
ENJOO = (24, 4)             # cada poção além disso: Vigor contra 24 + 4 por poção a mais; falhou, a poção não faz nada e a pessoa enjoa
# OS FEITIÇOS (os 24 e o truque): o nome, a tradição, o grau (0 é o truque), a Mana que custa e se se lança fora da luta. Estes nomes, tradições, graus e custos não mudam
# na onda 2 (o mundo aprende e gasta por eles); os números de luta (alcance, contra o quê, dano, o que põe) moram no tabelas_magia.FEITICOS, com as mesmas chaves.
FEITICOS = {
    'luz':              dict(de='todas',  grau=0, mana=1, fora=True),     # tira o escuro do campo; 1 de Mana por rodada a mais
    'seta':             dict(de='arcano', grau=1, mana=2, fora=False),
    'prender':          dict(de='arcano', grau=1, mana=3, fora=False),
    'escudo':           dict(de='arcano', grau=1, mana=2, fora=False),
    'lança-de-fogo':    dict(de='arcano', grau=2, mana=4, fora=False),
    'bola-de-fogo':     dict(de='arcano', grau=2, mana=6, fora=False),
    'raio':             dict(de='arcano', grau=3, mana=6, fora=False),
    'cura':             dict(de='fé',     grau=1, mana=3, fora=True, dado='1d8'),
    'bênção':           dict(de='fé',     grau=1, mana=2, fora=True),     # fora da luta: dada antes dela
    'amparo':           dict(de='fé',     grau=1, mana=2, fora=True),
    'castigo':          dict(de='fé',     grau=2, mana=4, fora=False),
    'guarda':           dict(de='fé',     grau=2, mana=6, fora=False),
    'quebrar-maldição': dict(de='fé',     grau=3, mana=6, fora=True),     # rito de 1 bloco, fora da luta
    'raízes':           dict(de='verde',  grau=1, mana=3, fora=False),
    'espinho':          dict(de='verde',  grau=1, mana=2, fora=False),
    'névoa':            dict(de='verde',  grau=1, mana=2, fora=False),    # névoa ou lamaçal: quem lança escolhe neblina ou lama; 1 de Mana por rodada a mais
    'afugentar':        dict(de='verde',  grau=1, mana=3, fora=False),
    'seiva':            dict(de='verde',  grau=2, mana=4, fora=True),     # fora da luta: dobra a cura da noite
    'chamar':           dict(de='verde',  grau=3, mana=6, fora=False),
    'mau-olhado':       dict(de='pacto',  grau=1, mana=2, fora=False),
    'medo':             dict(de='pacto',  grau=1, mana=3, fora=False),
    'sangria':          dict(de='pacto',  grau=1, mana=2, fora=False),
    'ler':              dict(de='pacto',  grau=1, mana=2, fora=True),     # rito de 1 bloco: lê uma maldição, um dom ou uma peça
    'nó':               dict(de='pacto',  grau=2, mana=4, fora=False),
    'praga':            dict(de='pacto',  grau=3, mana=6, fora=True),     # rito de 1 bloco, com um laço: põe uma maldição (e soma dívida)
}
def nome_feitico(k): return k if k == 'mau-olhado' else k.replace('-', ' ')      # o nome à mesa: "lança de fogo", "quebrar maldição", "mau-olhado"
# OS TRAÇOS NOVOS (a lista fechada que a luta roda nesta etapa). NÃO entram no tabelas_bichos.TRACOS (a meta da etapa 2 sobre a lista dos bichos fica como está):
# a frase de cada um mora na página das criaturas (tabelas_criaturas.TRACOS); os números, na página da magia na luta (tabelas_magia)
TRACOS_NOVOS = ('resiste', 'imaterial', 'amaldiçoa', 'lança', 'sem vida', 'ossos', 'dreno', 'ardente', 'noturno')

# ---------- a etapa 4b (as masmorras e o mundo de fantasia; o contrato: projeto/ETAPA_4B.md) ----------
# O GOLPE PELAS COSTAS (E1 a): quem tem a manha de Treinado (4) ou mais dá, na primeira rodada, contra o lado surpreendido, o primeiro golpe de corpo a corpo da luta
# com +4 no acerto e os dados rolados 3 vezes (vale uns 11 pontos, como o Grande Dom; a arma uma acima segue vencendo). Não derruba.
COSTAS = dict(desde=4, acerto=4, dados=3)
# OS TRAÇOS DO POVO (a lista fechada nova, da etapa 4b): NÃO entram no tabelas_bichos.TRACOS nem no TRACOS_NOVOS (não ligam a luta de magia).
# A frase de cada um mora no tabelas_povos.TRACOS; os números (a fração do escuro e do veneno que ainda pesa), no tabelas_povos (ESCURO, VENENO)
TRACOS_POVO = ('vê no escuro', 'resiste a veneno')
