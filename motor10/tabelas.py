"""tabelas.py — MOTOR 10: TODOS os números da luta e dos itens num lugar só.

Nenhum outro script do Motor 10 traz número de regra. Mudar o jogo é mudar esta página e rodar `provas.py`:
se uma meta do banco de provas quebra, a mudança não entra.

A ESCALA (a regra de ouro do Motor 10, "o item decide"):
  cada categoria vale 2,5 vezes a de baixo, na arma E na armadura, e o que conta é a DIFERENÇA entre as duas.
    dano = dado × K_DANO × valor da arma ÷ proteção da parte atingida, vezes a força de quem bate
    mesma categoria ......... o golpe passa inteiro (× 1)
    arma UMA acima .......... × 2,5          armadura UMA acima ....... × 0,4
    arma DUAS acima ......... × 6            armadura DUAS acima ...... × 0,16
    arma TRÊS acima ......... × 15           armadura TRÊS acima ...... quase nada (só o crítico arranha)
  Por isso um duelo entre iguais dura o mesmo em qualquer degrau, e quem está mal armado não fere quem está bem vestido.
"""

CATS = ['Comum', 'Incomum', 'Raro', 'Épico', 'Único', 'Lendário', 'Mítico', 'Primordial']
ATRIBUTOS = ['Força', 'Agilidade', 'Vigor', 'Vontade', 'Percepção', 'Afinidade']

# ---------- a categoria ----------
MULT = [1, 2.5, 6, 15, 40, 100, 250, 600]      # o valor da arma
RD = [1, 2.5, 6, 15, 40, 100, 250, 600]        # a proteção da armadura de MALHA: DIVIDE o golpe (couro e placa: MATERIAIS)
NU = 0.4                                       # a proteção de uma parte sem armadura (um degrau abaixo do Comum)
K_DANO = 4.5                                   # o tamanho do golpe entre iguais (afina a duração da luta)
BON = [0, 3, 6, 9, 12, 15, 18, 21]             # acerto (arma) e Defesa (escudo; ou metade, ao aparar com a arma)
DUR = [10, 20, 30, 40, 50, 60, 80, 100]        # durabilidade de uma peça nova

# ---------- as armas ----------
# dado · golpe (corte, ponta, impacto) · alcance em casas (1 casa ≈ 3 m) · mãos · peso · à distância?
FAMILIAS = {
    'punho':    dict(dado='1d4',  golpe='impacto', alcance=1,  maos=1, peso='leve'),
    'adaga':    dict(dado='1d4',  golpe='ponta',   alcance=1,  maos=1, peso='leve'),
    'espada':   dict(dado='1d8',  golpe='corte',   alcance=1,  maos=1, peso='media'),
    'maça':     dict(dado='1d8',  golpe='impacto', alcance=1,  maos=1, peso='media'),
    'machado':  dict(dado='1d10', golpe='corte',   alcance=1,  maos=1, peso='pesada'),
    'martelo':  dict(dado='1d10', golpe='impacto', alcance=1,  maos=1, peso='pesada'),
    'lança':    dict(dado='1d8',  golpe='ponta',   alcance=2,  maos=1, peso='media'),
    'montante': dict(dado='1d12', golpe='corte',   alcance=1,  maos=2, peso='pesada'),
    'alabarda': dict(dado='1d12', golpe='corte',   alcance=2,  maos=2, peso='pesada'),
    'malho':    dict(dado='1d12', golpe='impacto', alcance=1,  maos=2, peso='pesada'),
    'arco':     dict(dado='1d8',  golpe='ponta',   alcance=12, maos=2, peso='media', distancia=True, atributo='Agilidade'),
    'besta':    dict(dado='1d10', golpe='ponta',   alcance=12, maos=2, peso='media', distancia=True, atributo='Força', recarga=1),
}
DUAS_MAOS = 1.25            # a arma de duas mãos multiplica o dado por isto

# ---------- as armaduras ----------
# fator da RD · o que pede de Força · fôlego a mais por rodada em que a pessoa age
MATERIAIS = {
    'couro': dict(rd=0.5, pede=40, folego=0),
    'malha': dict(rd=1.0, pede=60, folego=0),
    'placa': dict(rd=1.5, pede=80, folego=1),
}
# o golpe contra o material: a RD da peça vezes isto
MATRIZ = {
    'corte':   dict(couro=0.85, malha=1.25, placa=1.5),  # o fio abre o couro e escorrega no metal
    'ponta':   dict(couro=1.0, malha=0.85, placa=1.15),  # a ponta abre o elo da malha
    'impacto': dict(couro=1.15, malha=1.0, placa=0.7),   # o malho amassa a placa
}
PARTES = ['cabeça', 'tronco', 'braços', 'pernas']
# onde o golpe cai (d10)
ONDE = {1: 'cabeça', 2: 'braços', 3: 'braços', 4: 'tronco', 5: 'tronco', 6: 'tronco', 7: 'tronco', 8: 'pernas', 9: 'pernas', 10: 'pernas'}

# ---------- o requisito (por ATRIBUTO, nunca por nível) ----------
PEDE_PESO = {'leve': 40, 'media': 60, 'pesada': 80}     # Força (ou o "atributo" da família) que a arma pede
FALTA_ACERTO = 5            # cada 5 pontos que faltam: −1 no acerto (arma) ou na Defesa (armadura e escudo)
FALTA_FOLEGO = 10           # cada 10 pontos que faltam: +1 de fôlego por golpe (arma) ou por rodada (armadura)
SOB_MEDIDA = 10             # sob medida: o requisito cai 10 por grau do ferreiro (graus 1 a 4), só para o dono
NAO_E_DELE = 1              # peça sob medida na mão de outro rende esta quantidade de categorias abaixo
SINTONIA = 20               # peças Épicas ou melhores com efeito desperto que a pessoa sustenta: Vontade ÷ isto (mínimo 1)
SINTONIA_DESDE = 3          # índice da categoria Épico

# ---------- a pessoa ----------
DEF_BASE = 24               # Defesa = isto + Agilidade ÷ 20 + maestria ÷ 2 + escudo (ou metade do bônus da arma)
def acerto_base(maestria, forca, agil): return maestria + (forca // 10 + agil // 10) / 4
def defesa_base(maestria, agil): return DEF_BASE + (agil // 10) / 2 + maestria / 2
def pv_max(vigor, nivel): return vigor * 2 + nivel // 2
def folego_max(vigor): return 6 + vigor // 10
def forca_mult(atributo): return 1 + (atributo // 10) * 0.04      # a força empurra o que o aço abriu
def acoes(maestria): return 2 + (1 if maestria >= 6 else 0) + (1 if maestria >= 8 else 0)
def reacoes(maestria): return 1 + (1 if maestria >= 8 else 0)
MAESTRIAS = {0: 'Leigo', 2: 'Iniciante', 4: 'Treinado', 6: 'Mestre', 8: 'Lendário'}

# ---------- a luta ----------
CRIT_OUTRO = 11             # crítico: um dado deu 20 e o outro deu isto ou mais
FERIDA = 0.25               # golpe que tira esta fração do PV máximo (ou um crítico que fere) abre uma FERIDA
FERIDA_GRAVE = 0.50         # e esta, uma ferida GRAVE (e é um "golpe terrível" para a moral de quem vê)
SANGRA = 0.03               # sangrando: perde esta fração do PV máximo por rodada
SEM_FOLEGO = 4              # sem fôlego: −isto no acerto e na Defesa, e uma ação só
PASSO = 2                   # casas por ação de andar
INICIO = {'longe': 8, 'perto': 3, 'colado': 1}   # a distância entre as duas frentes quando a luta começa
SEGURA = 2                  # em campo aberto, cada um de pé segura este tanto de inimigos; o resto passa
POSTURAS = {'firme': (0, 0, 0), 'agressiva': (2, -2, 0), 'defensiva': (-2, 2, 1)}   # acerto, Defesa, fôlego a mais por rodada
ENTRE = -2                  # golpe ou tiro com alguém de pé no caminho
# o tempo e o lugar: (acerto corpo a corpo, acerto à distância)
TEMPO = {
    'escuro':  dict(acerto=-4, tiro=-8),
    'chuva':   dict(tiro=-4),
    'vento':   dict(tiro=-2),
    'neblina': dict(tiro=-4, sem_tiro_longe=True),
    'lama':    dict(passo=1),
    'calor':   dict(folego_armadura=1),
    'água':    dict(passo=1, defesa=-2, folego=1),
}
ALTO = dict(acerto=1, tiro=2)       # quem está no alto
COBERTURA = -4                      # tiro contra quem tem cobertura

# a moral: 2d20 + Vontade ÷ 10 + o que ajuda, contra a CD do susto
MORAL = dict(lider_caiu=29, metade_caiu=26, golpe_terrivel=24, ferido_grave=26)
MORAL_LIDER = 2             # com o líder de pé
MORAL_MAIS = 2              # o lado dele tem mais gente de pé
MORAL_MENOS = -4            # o outro lado tem o dobro
MORTE_CD = 12               # caído: d20 contra isto por rodada; 3 falhas morre, 3 sucessos estável
