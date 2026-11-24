"""tabelas_magia.py — MOTOR 10, ETAPA DA MAGIA: OS NÚMEROS DA MAGIA NA LUTA (a frente da luta; a regra mora no magia.py e no luta.py).

A base comum (os nomes, as tradições, os graus e o custo dos feitiços; o foco, a guarda, a Firmeza, a Mana, a cura) mora no tabelas.py e não se redefine aqui.
Aqui moram os números de LUTA: o alcance, contra o quê, o dado e o que cada feitiço põe; o tempo de lançar; a concentração; os estados com prazo; a poção
bebida na luta; o encanto de peça; os nove traços novos; as fases do chefe; e a regra curta de quem o jogador não comanda (magia.escolhe).

A CONTA (a do aço, linha por linha):
  Conjuração = mão da tradição + dom nela + bônus do atributo dela ÷ 2 + bônus do foco (sem foco: Comum, −4; foco de outra tradição: uma categoria abaixo)
  o que voa (seta, lança de fogo, raio...) vai contra a Defesa inteira, como um tiro; a área (bola de fogo), contra a Defesa sem escudo e sem arma;
  o que prende, assusta ou amaldiçoa, contra a Firmeza (mais o calejo)
  dano = dado × K × valor do foco ÷ guarda × força do feitiço (1 + 0,03 por ponto de bônus do atributo da tradição); o crítico dobra os dados e corta a guarda pela metade
"""
import tabelas as T

K = 4.0                     # o tamanho do feitiço entre iguais: o mesmo K do aço (tabelas.K_DANO)
CALEJO = 4                  # cada controle que pega soma isto na Firmeza do alvo até o fim da luta (ninguém fica preso a luta inteira)
MANA_LUTA = 1               # a Mana que volta no começo de cada turno de quem lança (decisão do jogador: devagar)
SUSTENTA = 1                # o que custa, por rodada, manter um feitiço de campo (a luz, a névoa)
CONCENTRA = 28              # quem canaliza um feitiço longo e leva dano: 2d20 + bônus de Vontade + mão da tradição contra isto, ou perde o feitiço e a Mana
CONCENTRA_FERIDA = 4        # ... e isto a mais se o golpe abriu ferida
FORCADO = -4                # abaixo da mão que o grau pede, o lance é FORÇADO: isto por grau de mão que falta (a mão é conselho, não tranca, como na forja)
SEM_MANA_PV = 0.05          # lançar NO OSSO (sem Mana): cada ponto que falta custa esta fração do PV máximo, e o lance é forçado
SEM_FOCO = -4               # sem foco: lança-se com as mãos, como foco Comum com isto
FOCO_OUTRA = 1              # foco de outra tradição rende esta quantidade de categorias abaixo (abaixo do Comum: sem foco)
FALTA = 5                   # cada tantos pontos que faltam do atributo que o foco pede: −1 na Conjuração (requisito por atributo, nunca por nível)
MAO = {0: 0, 1: 2, 2: 4, 3: 6, 4: 8}            # a mão que cada grau pede: truque (quem o sabe), Iniciante, Treinado, Mestre, Lendário
ACOES = {0: 1, 1: 1, 2: 2, 3: 2, 4: 2}          # as ações que o lance gasta no turno em que começa (2: o turno inteiro, não anda)
LONGO = {3: 1, 4: 2}        # o feitiço LONGO só sai no começo do turno seguinte (grau 3) ou do outro (grau 4); até lá, quem canaliza testa a concentração se apanhar
AREA_ALVOS = 4              # a área pega até tantos na casa, amigo ou inimigo
MANA_AVISO = 1 / 3          # a luta para quando a Mana de quem o jogador comanda cai abaixo desta fração do máximo

# OS ESTADOS (lista fechada: só o que a luta sabe rodar). O prazo de "preso", "cego", "guardado", "nó" e "guarda" conta em turnos de quem o tem; o de "seiva",
# "fúria" e o "benzido" do brado, em rodadas; o "benzido" da bênção e o "mau-olhado" duram até o fim da luta.
ESTADOS = dict(
    cego=dict(golpe=-4, tiro=-8),               # o escuro só para ele: no golpe; no tiro e no feitiço que voa
    guardado=dict(defesa=4),                    # o escudo do mago
    benzido=dict(acerto=2, coragem=2),          # a bênção do clérigo (e o brado do chefe). O projeto dizia +4 na coragem: benzer os quatro antes da luta rendia 15 pontos, acima da meta (5 a 14)
    olhado=dict(acerto=-4, defesa=-4, conj=-4), # o mau-olhado da bruxa (as penas de magia não somam: de mau-olhado, veneno e maldição vale a pior). O projeto dizia −2, mas mediu a bruxa
                                                # com um cajado que valia inteiro; com o talismã (o foco dela) e −2, a bruxa no grupo dava 38 a 40% (meta M13: 42 a 58); com −3, 42 a 43%; com −4, 49% (e sozinha 14%, M14: 5 a 20)
    seiva=0.05,                                 # com seiva: esta fração do PV máximo volta por rodada (é o "regenera" dos bichos, menor)
    furia=dict(acerto=2, defesa=-2, rodadas=5), # a poção de fúria: só alcança quem empunha arma até a categoria da poção
    enjoo=-2,                                   # bebeu além do que o corpo aguenta e falhou o Vigor: isto em tudo até o fim da luta
)
PRAZO_SEM_FIM = 99          # o prazo de quem fica assim "até o fim da luta"

# OS FEITIÇOS NA LUTA (as chaves do tabelas.FEITICOS). tipo: dano (vai contra a Defesa, como um tiro) · area (Defesa sem escudo e sem arma, amigo ou inimigo) ·
# poe (contra a Firmeza: põe um estado) · medo (contra a Firmeza: o alvo testa a coragem) · escudo · bencao · guarda · cura · amparo · seiva · campo · chamar · rito (fora da luta)
# alc: o alcance em casas (0: a casa de quem lança; 1: o toque, colado ou na mesma casa)
FEITICOS = {
    'luz':              dict(tipo='campo', alc=0, tira='escuro'),
    'seta':             dict(tipo='dano', alc=8, dado='1d8'),
    'prender':          dict(tipo='poe', alc=6, poe='preso', dur=2),
    'escudo':           dict(tipo='escudo', alc=4, dur=4),
    'lança-de-fogo':    dict(tipo='dano', alc=8, dado='2d8', queima=True),          # a ferida que abrir queima (como a que sangra, 5 rodadas)
    'bola-de-fogo':     dict(tipo='area', alc=8, dado='1d8'),
    'raio':             dict(tipo='dano', alc=8, dado='2d10', atordoa=1),          # se abrir ferida, atordoa 1 ação
    'cura':             dict(tipo='cura', alc=1, dado='1d8'),
    'bênção':           dict(tipo='bencao', alc=4),
    'amparo':           dict(tipo='amparo', alc=1),                                 # estanca o sangue; tira veneno até a categoria do foco; firma quem caiu
    'castigo':          dict(tipo='dano', alc=6, dado='2d8', dado_outro='1d4'),    # 2d8 em quem é maldito; nos outros, 1d4 (a fé não fere de longe quem não é maldito)
    'guarda':           dict(tipo='guarda', alc=0, dur=4),                          # até 4 na casa de quem lança: contam como tendo amuleto da categoria do foco
    'quebrar-maldição': dict(tipo='rito'),
    'raízes':           dict(tipo='poe', alc=6, poe='preso', dur=2),
    'espinho':          dict(tipo='dano', alc=6, dado='1d6', veneno=(0.25, 3)),    # e envenena: um quarto do golpe por 3 rodadas (e o −2 no acerto do veneno)
    'névoa':            dict(tipo='campo', alc=0, poe_campo=('neblina', 'lama')),  # quem lança escolhe: neblina (a primeira) ou lama
    'afugentar':        dict(tipo='medo', alc=6, so_bicho=True),                    # o bicho testa a coragem (o chefe, de moral firme, não)
    'seiva':            dict(tipo='seiva', alc=1, dur=5),
    'chamar':           dict(tipo='chamar', alc=0),                                 # só no ermo: um bicho da contagem do ermo, até a categoria do foco, vem lutar ao lado
    'mau-olhado':       dict(tipo='poe', alc=6, poe='olhado', dur=PRAZO_SEM_FIM),
    'medo':             dict(tipo='medo', alc=6),
    'sangria':          dict(tipo='dano', alc=4, dado='1d6', rouba=0.5),           # e quem lança recupera metade do que tirou (não é cura: é troca)
    'ler':              dict(tipo='rito'),
    'nó':               dict(tipo='poe', alc=6, poe='no', dur=4),                   # a Mana do alvo não volta, e cada feitiço dele custa 1 a mais
    'praga':            dict(tipo='rito'),
}
MEDO = 26                   # o teste de coragem de quem o medo (ou o afugentar) pegou
NO_CUSTO = 1                # com o nó, cada feitiço custa isto a mais

# A POÇÃO NA LUTA (beber é 1 ação; dar de beber a um aliado colado, também). Quantas por dia e o enjoo: tabelas.doses_dia e tabelas.ENJOO.
POCAO_CURA = '1d8'          # a cura da poção: este dado × 6 × 3^(categoria da poção − categoria da ferida mais funda) (tabelas.cura), com o teto do dia
POCAO_MANA = 4              # a poção de Mana devolve isto por degrau: 4, 8, 12, 16
NAO_SE_BEBE = {'veneno': 'o veneno de lâmina se passa na arma, fora da luta', 'vigília': 'a vigília tira sono e cansaço: bebe-se fora da luta',
               'quebra-maldição': 'a quebra-maldição age no relógio da maldição: bebe-se fora da luta'}
VENENO_LAMINA = dict(fracao=0.25, rodadas=3, acima=1 / 3)      # a dose na lâmina: a primeira vez que a arma tira sangue, a vítima perde por rodada esta fração do golpe,
                                                               # por tantas rodadas (e o −2 do veneno de sempre); numa lâmina de categoria maior que a dose, um terço disso por degrau

# A PEÇA ENCANTADA: solta o feitiço gravado uma vez por luta, sem Mana, com as ações do feitiço; vale como foco um degrau abaixo da peça
ENCANTO = dict(abaixo=1, por_grau=2)                           # Conjuração = 2 por grau de quem gravou + bônus de Afinidade do dono ÷ 2 + o bônus desse foco

# OS TRAÇOS NOVOS (a lista fechada: tabelas.TRACOS_NOVOS; a frase de cada um mora na página das criaturas)
OSSOS = 0.5                 # o golpe de corte e o de ponta valem isto contra quem é só osso (o de impacto, inteiro)
DRENO = 0.5                 # quem drena recupera em PV esta fração do que o golpe do corpo tira
IMATERIAL = 1               # a arma sem encanto e sem bênção conta tantas categorias abaixo contra o imaterial
ARDENTE_RODADAS = T.SANGRA_RODADAS[1]     # a ferida que o corpo ardente abre queima tantas rodadas, como a que sangra; quem o golpeia de perto leva o fogo de volta (tabelas.devolve_max)
MALDICAO_BICHO = dict(nome='a marca de {quem}', tipo='míngua', condicao=dict(tipo='matar'))   # o molde da maldição que o traço "amaldiçoa" põe, se o lutador não trouxer o dele ("maldicao")

# AS FASES DO CHEFE
BRADO = 3                   # o brado: os do lado dele ficam benzidos por tantas rodadas
ERGUE_PV = 0.5              # o morto erguido levanta com esta fração do PV máximo, como "sem vida", do lado de quem o ergueu

# A REGRA CURTA DE QUEM O JOGADOR NÃO COMANDA (magia.escolhe)
ROBO = dict(bebe=0.5,       # bebe a poção de cura abaixo desta fração do PV
            cura=0.5,       # cura o aliado abaixo desta fração do PV
            seiva=0.75,     # dá seiva abaixo desta
            calejo=2,       # não tenta controlar quem já foi controlado tantas vezes
            antidoto=0.10)  # bebe o antídoto quando o veneno que falta correr tira esta fração do PV

# GENTE GERADA QUE LANÇA (os moldes das provas e do mundo; como os do tabelas.MOLDES: os atributos de nascença e como os pontos do nível se repartem)
MOLDES = {
    'mago':    (dict(Força=45, Agilidade=55, Vigor=55, Vontade=65, Percepção=55, Afinidade=70), dict(Força=.05, Agilidade=.10, Vigor=.15, Vontade=.25, Percepção=.15, Afinidade=.30)),
    'clérigo': (dict(Força=60, Agilidade=50, Vigor=65, Vontade=70, Percepção=50, Afinidade=50), dict(Força=.15, Agilidade=.10, Vigor=.20, Vontade=.30, Percepção=.10, Afinidade=.15)),
    'druida':  (dict(Força=50, Agilidade=55, Vigor=60, Vontade=55, Percepção=70, Afinidade=50), dict(Força=.10, Agilidade=.15, Vigor=.15, Vontade=.15, Percepção=.30, Afinidade=.15)),
    'bruxa':   (dict(Força=45, Agilidade=55, Vigor=55, Vontade=65, Percepção=55, Afinidade=70), dict(Força=.05, Agilidade=.10, Vigor=.15, Vontade=.25, Percepção=.15, Afinidade=.30)),
}
