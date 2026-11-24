"""tabelas_masmorra.py — MOTOR 10, ETAPA 4b: TODOS os números das masmorras (capítulo 17; o contrato: projeto/ETAPA_4B.md, seções 2 e 12).

A masmorra é um lugar (tipo "masmorra"), e cada sala é um lugar pequeno (tipo "sala") ligado às outras por passagens. Lá dentro o tempo anda em LANCES de 20 minutos;
doze lances fecham um bloco, e só então o relógio anda, pelo ato.passa. A luz é a tocha (um bem, arde um bloco) ou o feitiço luz. A armadilha bate como uma arma da categoria
dela (a conta do aço). A sala limpa fica limpa; o tesouro levado não volta.
Os NOMES (os moldes, as armadilhas, os estados da porta) são o vocabulário do tabelas_mundo, que o gravador confere: as chaves daqui são as mesmas.
Os números dos testes do ladino (achar, a gazua, desarmar, arrombar, escutar, andar escondido) moram no tabelas_manha (a frente do ladino): a masmorra os lê de lá.
Mudar um número é mudar esta página e rodar `python3 provas_masmorra.py` (o provas_mundo.py também o roda).
"""

# ---------- o tempo ----------
LANCE_MINUTOS = 20
LANCES_BLOCO = 12           # doze lances fecham um bloco: só então o ato.passa anda
CUSTO = dict(ir=1, escondido=2, escuro=2, carrega=2, escutar=1, procurar=2, tenta=1, contornar=1, disparar=1, pegar=1, luta=1, voltar=1, fosso=1, esperar=1)
#                                 (escuro: a ida no escuro, sem quem veja nele, custa o dobro; o fosso: tirar quem caiu custa um lance)
ESFORCO_BLOCO = 'leve'      # o bloco lá dentro: o da procura de caça
ESFORCO_IDA = 'leve'        # a ida e a volta (o caminho até a boca da masmorra)

# ---------- a luz e o escuro ----------
TOCHA = dict(bem='tocha', base=1, blocos=1)     # arde um bloco; gasta-se uma da carga de quem leva a luz quando o bloco fecha
LUZ_MANA_BLOCO = 4          # o feitiço luz, fora da luta, por bloco (gasta-se quando o bloco fecha; acende com isto na Mana)
LUZ_FEITICO = 'luz'         # o feitiço que alumia (tabelas_magia)

# ---------- quem vê primeiro ----------
ATENTO = {-1: -6, 0: 0, 1: 4}       # dormindo, à toa, alerta: na Percepção de quem vigia (o morto não dorme)
ESCONDIDO = 20              # o grupo anda escondido contra 20 + Percepção ÷ 10 do melhor vigia + ATENTO
ATENCAO = 20                # quem vai na frente: Percepção + manha contra 20 + Agilidade ÷ 10 dos que emboscam
EMBOSCA = ('gárgula', 'aranha')     # quem arma emboscada (testa-se a atenção mesmo à toa)
INICIO = dict(viu='perto', aberta='longe', porta='colado', notou='perto', vem='perto', surpreso='perto')
ESCUTA = (3, 'poucos', 'muitos')    # escutar diz "de poucos" até tantos, "de muitos" acima (nunca o número)

# ---------- o alarme e o que vagueia ----------
ALARME = dict(luta=1, arrombar=1, fosso=1, pedra=1, runa=1, alarme=2, acalma=1, alerta=2, vem=4)      # o teto é tabelas_mundo.ALARME_MAX
ALARME_DIZ = {0: 'quieta', 1: 'quieta, com um eco ou outro', 2: 'com barulho: quem mora lá está alerta', 3: 'com barulho: quem mora lá está alerta',
              4: 'acordada: o barulho chama quem está perto', 5: 'acordada: o barulho chama quem está perto'}
VAGA = (1 / 6, 0.10)        # o que vagueia: por bloco lá dentro, mais isto por ponto de alarme

# ---------- as armadilhas (as chaves: tabelas_mundo.ARMADILHAS) ----------
ARMADILHAS = {
    'dardo':  dict(dado='1d6',  golpe='ponta',   pega='um',      escapa='acerto',    barulho=0, diz='um furo na parede: um dardo'),
    'lâmina': dict(dado='1d10', golpe='corte',   pega='um',      escapa='acerto',    barulho=0, diz='uma fresta no chão e na parede: uma lâmina que varre'),
    'fosso':  dict(dado='2d6',  golpe='impacto', pega='um',      escapa='Agilidade', parte='pernas', estacas_desde=1, barulho=1, diz='a laje cede: um fosso'),
    'pedra':  dict(dado='2d8',  golpe='impacto', pega='um',      escapa='Agilidade', cabeca=0.3, barulho=1, diz='uma pedra presa no teto'),
    'gás':    dict(dado='1d6',  golpe='guarda',  pega='todos',   escapa='Vigor',     metade=True, barulho=0, diz='bicos de barro nas frestas: gás'),
    'runa':   dict(dado='1d8',  golpe='guarda',  pega='um',      escapa='Firmeza',   amaldicoa_desde=1, barulho=1, diz='uma runa riscada na laje'),
    'alarme': dict(dado=None,   pega='ninguém',  barulho=2, diz='um fio de sinos'),
}
ARMADILHA_ACERTO = 6        # 2d20 + isto + o bônus da categoria, contra a Defesa sem escudo (ou a Firmeza, a runa)
ESQUIVA = (20, 6)           # Agilidade ou Vigor contra 20 + 6 por categoria
PASSAGEM = -6               # achar de passagem: quem vai na frente, de graça, 6 mais difícil
RUNA_MALDICAO = dict(nome='a marca da runa', tipo='marca')      # a runa da Incomum para cima amaldiçoa (passo 1, da categoria dela; quebra longe da sala, 7 dias)

# ---------- os moldes (as chaves: tabelas_mundo.MOLDES) ----------
MOLDES = {   # salas por nível · níveis · quem mora · armadilhas · o chefe do fundo (pela categoria) · a fração de corredor · o bando de fora (o nível vazio)
    'cripta': dict(salas=(4, 8),  niveis=(1, 2), mora=['esqueleto', 'corpo-seco', 'carniçal', 'alma-penada', 'múmia', 'espectro'], ninho=['ratazana'],
                   armadilhas=['dardo', 'lâmina', 'runa', 'gás'], chefe={0: 'guardião da cripta', 1: 'guardião da cripta', 3: 'necromante'}, corredor=0.5, fora=['goblin']),
    'mina':   dict(salas=(6, 12), niveis=(1, 3), mora=['aranha', 'trasgo', 'golem-de-barro'], ninho=['ratazana'], covil=['goblin', 'orc'],
                   armadilhas=['fosso', 'pedra', 'alarme'], chefe={1: 'xamã goblin', 2: 'senhor da guerra'}, corredor=0.6, minerio=True, fora=['goblin', 'orc']),
    'ruína':  dict(salas=(8, 16), niveis=(1, 3), mora=['esqueleto', 'gárgula', 'golem-de-barro', 'fogo-fátuo', 'harpia'], armadilhas='todas',
                   chefe={2: 'bruxa do brejo', 3: 'necromante'}, corredor=0.3, fora=['goblin', 'orc']),
    'toca':   dict(salas=(5, 10), niveis=(1, 2), covil=['goblin', 'orc', 'homem-lagarto', 'ogro'], armadilhas=['fosso', 'alarme'],
                   chefe={1: 'xamã goblin', 2: 'senhor da guerra'}, corredor=0.4, fora=['goblin', 'orc']),
    'covil':  dict(salas=(3, 6),  niveis=(1, 1), mora=[], armadilhas=[], chefe={3: 'serpe', 4: 'hidra'}, corredor=0.5, fora=[]),     # o dragão: tabelas_dragoes (frente D)
}
NOMES_SALA = {   # o gerador dá às salas os nomes do molde: a boca, o corredor, as salas, a do fundo, a escondida, a escada
    'cripta': dict(boca='a escada', corredor='o corredor dos nichos', salas=['o ossário', 'a capela', 'a sala das urnas', 'a galeria dos túmulos', 'a sala dos jazigos', 'a câmara das oferendas', 'a cripta pequena'],
                   fundo='a câmara do túmulo', segredo='o nicho escondido', escada='os degraus'),
    'mina':   dict(boca='a boca da mina', corredor='a galeria', salas=['o salão da veia', 'o poço velho', 'o depósito', 'a sala das vagonetas', 'a câmara alagada', 'o desmoronado', 'a forja velha'],
                   fundo='o salão fundo', segredo='o veio escondido', escada='o poço da escada'),
    'ruína':  dict(boca='o pórtico', corredor='o corredor', salas=['o salão', 'a biblioteca caída', 'o pátio de dentro', 'a capela velha', 'a cozinha', 'o quartel', 'a galeria das estátuas'],
                   fundo='a sala do senhor', segredo='o cofre escondido', escada='a escada de caracol'),
    'toca':   dict(boca='a entrada da toca', corredor='o túnel', salas=['o covil', 'a despensa', 'o salão do fogo', 'o canto dos ossos', 'a sala dos presos', 'o poço'],
                   fundo='o trono de pedra', segredo='o buraco escondido', escada='a rampa'),
    'covil':  dict(boca='a boca da caverna', corredor='a galeria', salas=['a gruta', 'a gruta dos ossos', 'o lago escuro'], fundo='a câmara do tesouro', segredo='a fenda escondida', escada='a descida'),
}
LARGURA = (1, 2, None)      # o corredor (1), a sala estreita (2) e a aberta (nada): o corredor sai pela fração do molde; o resto, meio a meio
MORA = 0.6                  # o gerador: a chance de uma sala (fora a boca e a escondida) ter quem more nela
NINHO = 0.3                 # e a de uma sala do molde com ninho ser um ninho (o bicho que cria, com teto)
LADO = (1, 3)               # as salas de lado (becos com tesouro ou armadilha), por nível
PORTA = dict(chance=0.4, fechada=0.5, trancada=0.3, emperrada=0.2, ferro=0.3)     # a porta de cada passagem do caminho; a do fundo é sempre de ferro e trancada
ARMADILHA_CADA = 3          # uma armadilha a cada tantas salas do nível (no chão do corredor, na porta, no guardado)
GUARDA_CHEFE = 2            # a guarda do chefe do fundo: tantos de quem mora no molde, na sala dele
SEGREDO_CADA = 3            # uma sala escondida a cada tantos níveis (o primeiro sempre)
TESOURO = dict(prata=(20, 4), salas=(2, 4), pecas_cada=3, acima=('escondida', 'chefe'), maldita=1 / 6, pocoes=(1, 2), guardado=0.5)      # a prata por sala de tesouro: 20 × 4 por categoria
GUARDADOS = ('o baú', 'o sarcófago', 'o nicho', 'a arca', 'o cofre')
MEMORIA = dict(ergue=10, vem_de_fora=120)       # o chefe vivo ergue um morto a cada tantos dias; o nível vazio espera tantos dias por um bando de fora
