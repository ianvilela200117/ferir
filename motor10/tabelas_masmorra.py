"""tabelas_masmorra.py — MOTOR 10, ETAPA 4b: TODOS os números das masmorras (capítulo 17; o contrato: projeto/ETAPA_4B.md, seções 2 e 12).

A masmorra é um lugar (tipo "masmorra"), e cada sala é um lugar pequeno (tipo "sala") ligado às outras por passagens. Lá dentro o tempo anda em LANCES de 20 minutos;
doze lances fecham um bloco, e só então o relógio anda, pelo ato.passa. A luz é a tocha (um bem, arde um bloco) ou o feitiço luz. A armadilha bate como uma arma da categoria
dela (a conta do aço). A sala limpa fica limpa; o tesouro levado não volta.
Os NOMES (os moldes, as armadilhas, os estados da porta) são o vocabulário do tabelas_mundo, que o gravador confere: as chaves daqui são as mesmas.
Esqueleto do alicerce (onda 1): os números são o rascunho do projeto A (projeto/etapa4b/projeto_a/PROJETO.md, anexo), a conferir pela frente M (provas_masmorra.py).
"""

# ---------- o tempo ----------
LANCE_MINUTOS = 20
LANCES_BLOCO = 12           # doze lances fecham um bloco: só então o ato.passa anda
CUSTO = dict(ir=1, escondido=2, escuro=2, carrega=2, escutar=1, procurar=2, tenta=1, contornar=1, disparar=1, pegar=1, luta=1, voltar=1, fosso=1)
ESFORCO_BLOCO = 'leve'      # o bloco lá dentro: o da procura de caça

# ---------- a luz e o escuro ----------
TOCHA = dict(bem='tocha', base=1, blocos=1)     # arde um bloco; gasta-se uma da carga de quem leva a luz quando o bloco fecha
LUZ_MANA_BLOCO = 4          # o feitiço luz, fora da luta, por bloco

# ---------- quem vê primeiro ----------
ATENTO = {-1: -6, 0: 0, 1: 4}       # dormindo, à toa, alerta: na Percepção de quem vigia (o morto não dorme)
ESCONDIDO = 20              # o grupo anda escondido contra 20 + Percepção ÷ 10 do melhor vigia + ATENTO
ATENCAO = 20                # quem vai na frente: Percepção + manha contra 20 + Agilidade ÷ 10 dos que emboscam

# ---------- o alarme e o que vagueia ----------
ALARME = dict(luta=1, arrombar=1, fosso=1, pedra=1, runa=1, alarme=2, acalma=1, alerta=2, vem=4)      # o teto é tabelas_mundo.ALARME_MAX
VAGA = (1 / 6, 0.10)        # o que vagueia: por bloco lá dentro, mais isto por ponto de alarme

# ---------- as armadilhas (as chaves: tabelas_mundo.ARMADILHAS) ----------
ARMADILHAS = {
    'dardo':  dict(dado='1d6',  golpe='ponta',   pega='um',      escapa='acerto',    barulho=0),
    'lâmina': dict(dado='1d10', golpe='corte',   pega='um',      escapa='acerto',    barulho=0),
    'fosso':  dict(dado='2d6',  golpe='impacto', pega='um',      escapa='Agilidade', parte='pernas', estacas_desde=1, barulho=1),
    'pedra':  dict(dado='2d8',  golpe='impacto', pega='um',      escapa='Agilidade', cabeca=0.3, barulho=1),
    'gás':    dict(dado='1d6',  golpe='guarda',  pega='todos',   escapa='Vigor',     metade=True, barulho=0),
    'runa':   dict(dado='1d8',  golpe='guarda',  pega='um',      escapa='Firmeza',   amaldicoa_desde=1, barulho=1),
    'alarme': dict(dado=None,   pega='ninguém',  barulho=2),
}
ARMADILHA_ACERTO = 6        # 2d20 + isto + o bônus da categoria, contra a Defesa sem escudo (ou a Firmeza, a runa)
ESQUIVA = (20, 6)           # Agilidade ou Vigor contra 20 + 6 por categoria
PASSAGEM = -6               # achar de passagem: quem vai na frente, de graça, 6 mais difícil
ESCUTAR_FERRO = 4           # a porta de ferro ou de pedra: escutar é 4 mais difícil

# ---------- os moldes (as chaves: tabelas_mundo.MOLDES) ----------
MOLDES = {   # salas por nível · níveis · quem mora · armadilhas · o chefe do fundo (pela categoria) · a fração de corredor
    'cripta': dict(salas=(4, 8),  niveis=(1, 2), mora=['esqueleto', 'corpo-seco', 'carniçal', 'alma-penada', 'múmia', 'espectro'], ninho=['ratazana'],
                   armadilhas=['dardo', 'lâmina', 'runa', 'gás'], chefe={0: 'guardião da cripta', 1: 'guardião da cripta', 3: 'necromante'}, corredor=0.5),
    'mina':   dict(salas=(6, 12), niveis=(1, 3), mora=['aranha', 'trasgo', 'golem-de-barro'], ninho=['ratazana'], covil=['goblin', 'orc'],
                   armadilhas=['fosso', 'pedra', 'alarme'], chefe={1: 'xamã goblin', 2: 'senhor da guerra'}, corredor=0.6, minerio=True),
    'ruína':  dict(salas=(8, 16), niveis=(1, 3), mora=['esqueleto', 'gárgula', 'golem-de-barro', 'fogo-fátuo', 'harpia'], armadilhas='todas',
                   chefe={2: 'bruxa do brejo', 3: 'necromante'}, corredor=0.3),
    'toca':   dict(salas=(5, 10), niveis=(1, 2), covil=['goblin', 'orc', 'homem-lagarto', 'ogro'], armadilhas=['fosso', 'alarme'],
                   chefe={1: 'xamã goblin', 2: 'senhor da guerra'}, corredor=0.4),
    'covil':  dict(salas=(3, 6),  niveis=(1, 1), mora=[], armadilhas=[], chefe={3: 'serpe', 4: 'hidra'}, corredor=0.5),     # o dragão: tabelas_dragoes (frente D)
}
SEGREDO_CADA = 3            # uma sala escondida a cada tantos níveis
TESOURO = dict(prata=(20, 4), salas=(2, 4), pecas_cada=3, acima=('escondida', 'chefe'), maldita=1 / 6, pocoes=(1, 2))      # a prata por sala de tesouro: 20 × 4 por categoria
MEMORIA = dict(ergue=10, vem_de_fora=120)       # o chefe vivo ergue um morto a cada tantos dias; o nível vazio espera tantos dias por um bando de fora
