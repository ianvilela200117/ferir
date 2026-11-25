"""tabelas_regiao.py — MOTOR 10, ETAPA FINAL: TODOS os números da região (os lugares, as estradas, a gente com nome, os rivais, o raro contado, a história,
as frentes, a notícia, a caixa, as missões, o querer, a viagem e a criação do personagem). O contrato: projeto/ETAPA_FINAL.md.

Mudar a região é mudar esta página e rodar `provas_regiao.py` e `provas_ano.py` (o `provas_mundo.py` roda os dois). Os números são METAS até o banco medir.
"""

# ---------- A REGIÃO: os lugares de povo ----------
# tipo: (quantos, povo (faixa), oficina, cama, botica, runas, santuário, resistência às frentes, guarda (soldados em número), distância do centro (faixa, em léguas))
LUGARES = {
    'capital': (1, (3800, 4200), 3, True, 2, 2, 3, 6, 40, (0, 0)),
    'cidade':  (2, (1400, 1600), 2, True, 1, 1, 2, 5, 20, (4, 6)),
    'vila':    (5, (350, 450),   1, True, 0, None, 1, 3, 6, (3, 8)),
    'aldeia':  (5, (100, 140),   0, False, None, None, None, 2, 2, (6, 11)),
    'posto':   (3, (100, 140),   1, True, None, None, None, 4, 8, (8, 12)),
}
ESTRADAS = 24               # as estradas da região (o grafo é conexo: a árvore mais curta e as mais curtas que faltam)
LEGUA_BLOCOS = 1.4          # uma estrada leva tantas léguas por bloco (arredondado, de 1 a 6 blocos)
BANDO_INICIO = (0, 4)       # os salteadores em cada estrada no Dia 1 (mais nas longas e nas que passam por ermo)
POVOS_LUGAR = {             # a gente de outros povos, pela fração (a soma até 1): o resto é humano
    'capital': {'anão': 0.05, 'elfo': 0.03, 'pequenino': 0.04, 'gnomo': 0.02, 'meio-orc': 0.03},
    'cidade':  {'anão': 0.04, 'elfo': 0.02, 'pequenino': 0.04, 'gnomo': 0.02, 'meio-orc': 0.03},
    'vila':    {'pequenino': 0.06, 'anão': 0.02, 'meio-orc': 0.02},
    'aldeia':  {'pequenino': 0.10},
    'posto':   {'anão': 0.25, 'meio-orc': 0.05, 'gnomo': 0.03},
}

# ---------- os ermos (habitat, perigo) e as masmorras ----------
ERMOS = [('floresta', 1), ('floresta', 2), ('serra', 3), ('brejo', 2), ('campo', 1), ('caverna', 2)]
ERMO_LONGE = (1, 2)         # os blocos do lugar de povo até o ermo vizinho
ERMO_VIZINHOS = (1, 3)      # quantos lugares de povo dão para cada ermo
# (molde, categoria do primeiro nível, níveis, perto de: 'ermo' ou 'lugar')
MASMORRAS = [('cripta', 0, 1, 'lugar'), ('cripta', 1, 2, 'lugar'), ('mina', 1, 2, 'ermo'), ('ruína', 1, 3, 'ermo'), ('ruína', 2, 3, 'ermo'),
             ('toca', 0, 2, 'ermo'), ('toca', 1, 2, 'ermo'), ('covil', 5, 1, 'ermo')]
CALAMIDADE = dict(tipo='serra', idade='ancião', dorme=(400, 700))      # o covil da calamidade: o dragão ancião dorme (os dias até acordar sozinho); a peça Mítica no tesouro dele
DRAGAO_JOVEM = dict(tipo='serra', idade='jovem', tesouro=(300, 600))   # o dragão jovem que ataca: mora no ermo da serra e cobra de uma vila (a frente de ameaça)
COVIS = [('goblin', 'floresta', 10), ('orc', 'serra', 6)]               # os covis de criatura nos ermos (espécie, habitat, cabeças)

# ---------- a gente com nome ----------
GENTE = {   # quem tem nome em cada tipo de lugar: (papel, quantos)
    'capital': [('senhor', 1), ('capitão', 1), ('guarda', 3), ('ferreiro', 2), ('coureiro', 1), ('mercador', 3), ('taverneiro', 2), ('curandeiro', 1),
                ('sacerdote', 1), ('mago', 1), ('ladino', 1), ('escriba', 1), ('bardo', 1), ('mestre de guilda', 1)],
    'cidade':  [('senhor', 1), ('capitão', 1), ('guarda', 2), ('ferreiro', 1), ('coureiro', 1), ('mercador', 2), ('taverneiro', 1), ('curandeiro', 1),
                ('sacerdote', 1), ('mago', 1), ('ladino', 1)],
    'vila':    [('ferreiro', 1), ('taverneiro', 1), ('guarda', 1), ('caçador', 1), ('curandeiro', 1), ('mercador', 1), ('ancião', 1)],
    'aldeia':  [('ancião', 1), ('caçador', 1), ('lavrador', 1)],
    'posto':   [('capitão', 1), ('guarda', 1), ('mineiro', 1), ('mercador', 1)],
}
FAMILIA = dict(conjuge=0.20, filho=0.14, irmao=0.07)       # a chance de cada nomeado adulto ter um cônjuge, um filho e um irmão com nome no mesmo lugar
# papel: (nível, molde, grau de ofício, maestria, prata, peças [(tipo, qual, categoria (faixa), cobre, uso)], magia)
PAPEL = {
    'senhor':     ((25, 60), 'guerreiro', 'mestre', {'espada': 4}, (300, 800), [('arma', 'espada', (1, 2), None, 'arma'), ('armadura', 'malha', (1, 2), None, 'veste'), ('escudo', None, (1, 1), None, 'escudo')], None),
    'capitão':    ((30, 70), 'guerreiro', 'oficial', {'espada': 4, 'lança': 4}, (60, 150), [('arma', 'espada', (1, 2), None, 'arma'), ('armadura', 'malha', (1, 1), None, 'veste'), ('armadura', 'malha', (0, 1), ['cabeça'], 'veste'), ('escudo', None, (1, 1), None, 'escudo')], None),
    'guarda':     ((10, 35), 'guerreiro', 'oficial', {'lança': 2}, (15, 50), [('arma', 'lança', (0, 1), None, 'arma'), ('armadura', 'malha', (0, 0), None, 'veste'), ('armadura', 'malha', (0, 0), ['cabeça'], 'veste'), ('escudo', None, (0, 0), None, 'escudo')], None),
    'ferreiro':   ((15, 40), 'guerreiro', 'oficial', {'forja': 4, 'martelo': 2}, (40, 120), [('arma', 'martelo', (0, 1), None, 'arma'), ('armadura', 'couro', (0, 0), None, 'veste')], None),
    'coureiro':   ((10, 30), 'comum', 'oficial', {'couro': 4}, (30, 80), [('arma', 'adaga', (0, 0), None, 'arma'), ('armadura', 'couro', (1, 1), None, 'veste')], None),
    'mercador':   ((8, 25), 'comum', 'oficial', {'comércio': 4}, (100, 400), [], None),
    'taverneiro': ((8, 20), 'comum', 'oficial', {'comércio': 2, 'adaga': 2}, (50, 150), [('arma', 'adaga', (0, 0), None, 'arma')], None),
    'curandeiro': ((10, 30), 'comum', 'aprendiz', {'cura': 2, 'coleta': 2}, (20, 60), [('arma', 'adaga', (0, 0), None, 'arma')], None),
    'sacerdote':  ((20, 45), 'clérigo', 'oficial', {'fé': 4, 'maça': 2}, (20, 80), [('foco', 'símbolo', (0, 1), None, 'foco'), ('arma', 'maça', (0, 0), None, 'arma'), ('armadura', 'couro', (0, 0), None, 'veste')],
                   dict(tradicao='fé', feiticos=['luz', 'cura', 'bênção', 'amparo'])),
    'mago':       ((25, 60), 'mago', 'mestre', {'arcano': 4}, (60, 200), [('foco', 'cajado', (1, 1), None, 'foco'), ('amuleto', None, (0, 1), None, 'pescoco'), ('armadura', 'couro', (0, 0), None, 'veste')],
                   dict(tradicao='arcano', feiticos=['luz', 'seta', 'escudo', 'prender', 'lança-de-fogo'])),
    'bruxa':      ((20, 45), 'bruxa', 'oficial', {'pacto': 4, 'adaga': 2}, (20, 60), [('foco', 'talismã', (0, 0), None, 'foco'), ('arma', 'adaga', (0, 0), None, 'arma')],
                   dict(tradicao='pacto', feiticos=['luz', 'mau-olhado', 'medo', 'sangria', 'ler', 'nó'])),
    'druida':     ((20, 45), 'druida', 'oficial', {'verde': 4}, (10, 40), [('foco', 'cajado', (0, 0), None, 'foco'), ('armadura', 'couro', (0, 0), None, 'veste')],
                   dict(tradicao='verde', feiticos=['raízes', 'espinho', 'névoa', 'afugentar', 'seiva'])),
    'ladino':     ((10, 35), 'arqueiro', 'oficial', {'manha': 4, 'adaga': 2}, (30, 100), [('arma', 'adaga', (0, 1), None, 'arma'), ('armadura', 'couro', (0, 0), None, 'veste'), ('gazua', None, (0, 1), None, None)], None),
    'escriba':    ((5, 20), 'comum', 'oficial', {}, (30, 80), [], None),
    'bardo':      ((8, 25), 'comum', 'oficial', {'comércio': 2, 'adaga': 2}, (20, 60), [('arma', 'adaga', (0, 0), None, 'arma')], None),
    'mestre de guilda': ((40, 80), 'guerreiro', 'mestre', {'espada': 6}, (200, 500), [('arma', 'espada', (2, 2), None, 'arma'), ('armadura', 'malha', (2, 2), None, 'veste'), ('escudo', None, (1, 1), None, 'escudo')], None),
    'caçador':    ((12, 30), 'arqueiro', 'aprendiz', {'arco': 4, 'caça': 4}, (15, 40), [('arma', 'arco', (0, 1), None, 'arma'), ('arma', 'adaga', (0, 0), None, 'arma2'), ('armadura', 'couro', (0, 0), None, 'veste')], None),
    'lenhador':   ((8, 20), 'guerreiro', 'diarista', {'machado': 2, 'coleta': 2}, (5, 20), [('arma', 'machado', (0, 0), None, 'arma')], None),
    'mineiro':    ((8, 25), 'guerreiro', 'diarista', {'martelo': 2, 'coleta': 2}, (10, 30), [('arma', 'martelo', (0, 0), None, 'arma')], None),
    'lavrador':   ((5, 15), 'comum', 'diarista', {}, (5, 20), [], None),
    'pescador':   ((5, 15), 'comum', 'diarista', {'lança': 2}, (5, 20), [('arma', 'lança', (0, 0), None, 'arma')], None),
    'ancião':     ((10, 30), 'comum', 'oficial', {}, (20, 60), [], None),
    'aprendiz':   ((3, 8), 'comum', 'aprendiz', {}, (2, 10), [], None),
    'criança':    ((1, 3), 'comum', 'diarista', {}, (0, 2), [], None),
    'nobre':      ((8, 30), 'guerreiro', 'oficial', {'espada': 2}, (60, 200), [('arma', 'espada', (0, 1), None, 'arma'), ('armadura', 'couro', (0, 1), None, 'veste')], None),
}
SOBRE = {   # o que a mesa diz de cada papel ({lugar}: o nome do lugar)
    'senhor': 'o senhor de {lugar}; manda na terra e na guarda', 'capitão': 'o capitão da guarda de {lugar}', 'guarda': 'da guarda de {lugar}',
    'ferreiro': 'o ferreiro; conserta e vende o que forja', 'coureiro': 'o coureiro; curte o couro e faz armadura dele', 'mercador': 'mercador; compra e vende, e leva carga pela estrada',
    'taverneiro': 'da taverna; sabe de tudo o que se conta', 'curandeiro': 'cura ferida e colhe erva', 'sacerdote': 'do santuário; cura e benze',
    'mago': 'o mago; ensina o arcano a quem paga', 'bruxa': 'a bruxa da borda; lê a sorte e vende o que não se vende na loja', 'druida': 'o druida do ermo; fala com o mato',
    'ladino': 'vive de manha; abre o que está fechado', 'escriba': 'o escriba; lê, escreve e guarda a história da terra', 'bardo': 'canta o que se passou, e o que se inventa',
    'mestre de guilda': 'o mestre da casa das guildas; paga missão e conhece todo aventureiro', 'caçador': 'caça no ermo e vende o couro', 'lenhador': 'tira madeira do mato',
    'mineiro': 'tira o metal da pedra', 'lavrador': 'lavra a terra', 'pescador': 'pesca no rio', 'ancião': 'o mais velho do lugar; sabe das histórias antigas',
    'aprendiz': 'aprende o ofício da casa', 'criança': 'criança da casa', 'aventureiro': 'aventureiro', 'nobre': 'da casa dos {casa}; herdeiro do nome',
}
ALDEIA_OFICIO = {'floresta': 'lenhador', 'serra': 'mineiro', 'brejo': 'pescador', 'campo': 'lavrador', 'caverna': 'mineiro'}      # o lavrador da aldeia vira o ofício do ermo vizinho

# ---------- os rivais: aventureiros nativos ----------
RIVAIS = [  # (quantos, nível (faixa), categoria da arma (faixa), categoria da armadura (faixa), o que se diz)
    (15, (5, 12), (0, 1), (0, 1), 'novato'),
    (14, (15, 40), (1, 2), (1, 2), 'oficial'),
    (8, (50, 100), (2, 2), (1, 2), 'veterano'),     # do Épico para cima, só as peças da história (o raro é contado)
    (3, (120, 200), (2, 2), (2, 2), 'Lenda'),
]
ARQUETIPOS = [  # (molde, maestria, arma (família), escudo, armadura (material), magia)
    ('guerreiro', 'espada', 'espada', True, 'malha', None), ('guerreiro', 'machado', 'machado', True, 'malha', None), ('guerreiro', 'montante', 'montante', False, 'malha', None),
    ('guerreiro', 'lança', 'lança', True, 'malha', None), ('arqueiro', 'arco', 'arco', False, 'couro', None), ('arqueiro', 'adaga', 'adaga', False, 'couro', None),
    ('mago', 'arcano', None, False, 'couro', dict(tradicao='arcano', feiticos=['luz', 'seta', 'escudo', 'lança-de-fogo', 'prender'])),
    ('clérigo', 'fé', 'maça', True, 'malha', dict(tradicao='fé', feiticos=['luz', 'cura', 'bênção', 'castigo', 'amparo'])),
]
GUILDAS = 6                 # as guildas: cada uma com 4 a 6 aventureiros; o resto anda sozinho
GUILDA_TAMANHO = (4, 6)
GUILDA_NOMES = (['a Companhia', 'a Irmandade', 'a Ordem', 'a Mesa', 'a Liga', 'o Bando', 'os Juramentados', 'a Guarda'],
                ['do Lobo Cinzento', 'da Lâmina Partida', 'do Corvo Branco', 'da Lanterna', 'do Escudo Velho', 'das Sete Pedras', 'da Estrada', 'do Sino Rachado',
                 'da Raposa', 'do Carvalho Negro', 'da Brasa', 'do Último Passo'])

# ---------- o raro contado (no Dia 1, no mundo inteiro; com quem: as Lendas, os veteranos, as casas nobres, o tesouro das masmorras) ----------
RARO = {2: 60, 3: 12, 4: 4, 5: 3, 6: 1}     # categoria: quantas peças (Rara, Épica, Única, Lendária, Mítica)

# ---------- a história (o gerador roda ano a ano, de 400 a 1.000 anos) ----------
HISTORIA = dict(anos=(400, 1000), nobres=(6, 9), reinos_mortos=(1, 3), geracao=(22, 34), guerras_seculo=(1, 3), pestes_seculo=(0, 2), fomes_seculo=(1, 3),
                lendas=(8, 14), antes=(40, 400), cai_casa=0.35)

# ---------- a virada da região (regiao.py): o povo em número, a fome, a migração, o bando, o comércio entre lugares ----------
FOME_DIAS = 8               # o celeiro abaixo de tantos dias de comida: o povo começa a sair (e nasce a frente da fome)
FOME_MORRE = 0.01           # sem comida nenhuma no celeiro: esta fração do povo morre por dia (e outro tanto sai)
MIGRA = 0.005               # com o celeiro baixo: esta fração do povo vai por dia para o vizinho mais farto
BANDO_FOME = 0.15           # com o celeiro baixo: a chance, por dia e por estrada do lugar, de um faminto virar salteador
BANDO_TETO = 12             # nenhuma estrada passa de tantos salteadores
COMERCIO = dict(bens=('comida', 'lenha', 'sal', 'pano', 'ferramenta', 'metal:0', 'couro:0'), razao=1.35, lote=0.04, teto=0.15)
                            # o comércio entre lugares (os mercadores, em número): por estrada aberta e por dia, se o preço do outro lado passa de `razao` vezes o daqui,
                            # leva até `lote` do estoque daqui (e não mais que `teto` do alvo de lá); a prata vai do lugar que compra para o que vende, no preço do meio
GUARDA_PATRULHA = 0.02      # por soldado da guarda (em número), por dia: a chance de a patrulha tirar um salteador da estrada vizinha

# ---------- a notícia (noticias.py) ----------
BOATO_SALTO = 4             # do quarto salto em diante, a notícia é boato ("dizem que...")
NOTICIA_DURA = 90           # a notícia some do mundo tantos dias depois de nascer
MESA_NOTICIAS = 6           # quantas notícias chegadas a MESA mostra (as mais novas)

# ---------- a gente: a memória, a opinião, o querer da semana (gente.py) ----------
OPINIAO_DIZ = [(-6, 'odeia você'), (-3, 'não gosta de você'), (-1, 'desconfia de você'), (0, 'não tem nada contra você'), (3, 'gosta de você'), (6, 'confia em você'), (99, 'faria tudo por você')]
QUERER = {  # papel: [(querer, peso)] — cada querer muda número (gente.py faz o efeito)
    'ferreiro': [('forja', 3), ('pede_materia', 2)], 'coureiro': [('curte', 3)], 'caçador': [('caca', 3), ('recompensa', 1)], 'lenhador': [('tira', 1)],
    'mineiro': [('tira', 1)], 'pescador': [('tira', 1)], 'lavrador': [('tira', 1)], 'mercador': [('lucra', 2), ('escolta', 1)], 'taverneiro': [('serve', 1)],
    'guarda': [('patrulha', 1)], 'capitão': [('patrulha', 2), ('contra_frente', 1)], 'senhor': [('contra_frente', 2), ('imposto', 1), ('limpar', 1)],
    'curandeiro': [('colhe', 1)], 'sacerdote': [('colhe', 1)], 'mago': [('estuda', 1)], 'bruxa': [('estuda', 1)], 'druida': [('estuda', 1)],
    'ladino': [('furta', 2), ('estuda', 1)], 'ancião': [('conta', 1)], 'escriba': [('conta', 1)], 'bardo': [('conta', 1)], 'aprendiz': [('treina', 1)],
    'nobre': [('corte', 1)], 'mestre de guilda': [('limpar', 1), ('contra_frente', 1)],
}
FURTO = (0.25, 0.15)        # o ladino: a chance de furtar alguém do lugar na semana; a chance de a guarda pegar (e ele perde o que furtou)
IMPOSTO = 0.01              # o senhor cobra esta fração da prata do lugar por semana (vai para a bolsa dele)

# ---------- a caixa (caixa.py) ----------
CAIXA_PRAZO = (3, 10)       # os dias de prazo de um pedido
CAIXA_CUSTO = 2             # o padrão (calar) custa isto na opinião de quem pediu

# ---------- as missões (missoes.py) ----------
QUADRO = {'capital': 6, 'cidade': 4, 'vila': 2, 'aldeia': 1, 'posto': 1}        # quantas missões abertas cada quadro aguenta
MISSAO_PRAZO = (7, 28)      # os dias de prazo de uma missão
MISSAO_PAGA = {'caça': (8, 4), 'entrega': (10, 3), 'limpar': (120, 3), 'matar': (200, 3), 'escolta': (15, 2), 'investigar': (40, 2)}   # (base, vezes por categoria do alvo)
MISSAO_FAMA = {'caça': 1, 'entrega': 1, 'limpar': 5, 'matar': 8, 'escolta': 1, 'investigar': 3}      # a fama de quem cumpre
MISSAO_FALHA = (-1, -2)     # quem toma e não cumpre: a fama, e a opinião de quem pediu

# ---------- a viagem (viagem.py) ----------
VIAGEM = dict(base={1: 0.02, 2: 0.05, 3: 0.09}, por_bando=0.012, noite=1.5, bicho=0.35, grupo=(2, 5),
              nivel={1: (3, 8), 2: (6, 15), 3: (12, 30)}, taxa_cabeca=4, taxa_salteador=1, fuga=20)
              # a chance de encontro por bloco na estrada: pela base do perigo, mais por salteador nela, vezes isto de noite; a fração dos encontros que é bicho do ermo
              # que a estrada passa; quantos salteadores atacam; o nível deles pelo perigo; o pedágio (por cabeça de quem viaja, mais por salteador); a fuga (Agilidade contra isto)

# ---------- as frentes (frentes.py) ----------
# Os moldes: (tipo, nome, meta, os 6 passos (o sinal que a notícia leva), os efeitos de cada passo, a missão contra ela, quando é barrada).
# Os efeitos são VERBOS DE FRENTE (frentes.py os faz em efeitos do gravador): ('estoque', bem, fração) · ('prata', fração) (do lugar para o dono) · ('povo', fração)
# · ('rota', 'fecha'|'abre') (a estrada do lugar mais perto do ermo) · ('bando', n) · ('bichos', n) (no ermo da frente) · ('produz', bem, fator) · ('morre', papel)
# · ('missao',) (quem manda põe a missão contra ela) · ('fama', n) (o dono) · ('acorda',) (o dragão da calamidade) · ('casa',) (a casa da frente toma o lugar)
FRENTES = {
    'bando':    ('ameaça', 'o bando {dono} na estrada', 'tomar a estrada e cobrar de quem passa',
                 ['mais salteadores aparecem na estrada', 'um mercador é roubado e morto na estrada', 'a estrada fecha: ninguém passa sem pagar', 'o bando assalta um lugar e leva a prata', 'o bando mata um da guarda', 'o lugar se esvazia: quem pode, vai embora'],
                 [[('bando', 3)], [('estoque', 'pano', -0.2), ('bando', 1)], [('rota', 'fecha')], [('prata', -0.15), ('povo', -0.03)], [('morre', 'guarda'), ('missao',)], [('povo', -0.4)]], 'matar', 'dono'),
    'horda':    ('ameaça', 'a horda {dono}', 'crescer até tomar a terra',
                 ['o bando da toca cresce', 'roubam o celeiro de noite', 'um caçador não volta do mato', 'a horda ataca de dia', 'a estrada fecha: a horda está nela', 'o lugar cai: a horda o toma'],
                 [[('bichos', 3)], [('estoque', 'comida', -0.1)], [('morre', 'caçador'), ('missao',)], [('povo', -0.05), ('prata', -0.1)], [('rota', 'fecha'), ('bichos', 2)], [('povo', -0.6)]], 'limpar', 'covil'),
    'mortos':   ('ameaça', 'os mortos {dono}', 'erguer os mortos da terra',
                 ['os mortos da masmorra se mexem', 'o cemitério amanhece revolvido', 'um morto anda de noite no lugar', 'quem sai de noite não volta', 'os mortos fecham a estrada', 'o lugar é abandonado aos mortos'],
                 [[('vagantes', 2)], [('povo', -0.01)], [('morre', 'lavrador'), ('missao',)], [('povo', -0.04)], [('rota', 'fecha')], [('povo', -0.6)]], 'limpar', 'chefe'),
    'dragão':   ('ameaça', 'o dragão {dono}', 'fazer o lugar pagar tributo até não sobrar nada',
                 ['o dragão é visto sobre o lugar', 'o dragão queima um campo', 'o dragão leva o gado e a prata', 'ninguém passa pela estrada da serra', 'o dragão queima a casa do senhor', 'o lugar arde: quem sobra, foge'],
                 [[('fama', 2)], [('estoque', 'comida', -0.2)], [('prata', -0.2), ('missao',)], [('rota', 'fecha')], [('morre', 'ancião')], [('povo', -0.7)]], 'matar', 'dragao'),
    'trono':    ('ambição', 'a ambição {dono}', 'tomar a coroa',
                 ['a casa junta aliados', 'a casa junta prata', 'um senhor rival morre de repente', 'a casa arma gente', 'a guarda do rei é emboscada', 'a casa toma o lugar do rei'],
                 [[('fama', 3)], [('prata', -0.05)], [('morre', 'nobre'), ('missao',)], [('fama', 3)], [('morre', 'guarda')], [('casa',)]], 'investigar', 'dono'),
    'cartel':   ('ambição', 'o cartel {dono}', 'ter todo o metal da região na mão',
                 ['o mercador compra todo o metal que acha', 'o metal some das lojas', 'o ferreiro fecha a forja por falta', 'o mercador compra a mina', 'o preço do metal triplica', 'o metal da região é dele'],
                 [[('estoque', 'metal:0', -0.25)], [('estoque', 'metal:0', -0.3), ('missao',)], [('estoque', 'metal:0', -0.3)], [('produz', 'metal:0', 0.7)], [('estoque', 'metal:0', -0.5)], [('produz', 'metal:0', 0.5)]], 'investigar', 'dono'),
    'culto':    ('ambição', 'o culto {dono}', 'abrir a porta para o que mora embaixo',
                 ['gente some de noite', 'o culto compra a casa velha', 'um nobre entra no culto', 'mais gente some', 'o culto prepara o sacrifício', 'o sacrifício: o lugar fica maldito'],
                 [[('povo', -0.01)], [('prata', -0.05), ('missao',)], [('fama', 2)], [('povo', -0.02), ('morre', 'aprendiz')], [('morre', 'sacerdote')], [('povo', -0.1)]], 'investigar', 'dono'),
    'guilda':   ('ambição', 'a corrida {dono}', 'ser a primeira a limpar a masmorra funda',
                 ['a guilda junta gente', 'a guilda compra tochas e cordas', 'a guilda desce o primeiro nível', 'a guilda perde um dos seus lá embaixo', 'a guilda chega ao fundo', 'a guilda limpa a masmorra e leva o tesouro'],
                 [[('fama', 2)], [('fama', 1)], [('fama', 2)], [('fama', -1)], [('fama', 3)], [('fama', 8)]], None, 'limpa'),
    'seca':     ('falta', 'a seca {dono}', 'secar a colheita',
                 ['o rio baixa', 'a colheita sai pequena', 'o celeiro baixa', 'o gado morre de sede', 'a semente acaba', 'a fome'],
                 [[('produz', 'comida', 0.9)], [('produz', 'comida', 0.85)], [('estoque', 'comida', -0.15), ('missao',)], [('estoque', 'comida', -0.15)], [('produz', 'comida', 0.8)], [('estoque', 'comida', -0.5)]], 'entrega', 'entregue'),
    'mina':     ('falta', 'a mina {dono} se perde', 'a água tomar a mina',
                 ['a água sobe no fundo da mina', 'o veio de baixo fica debaixo d\'água', 'os mineiros param', 'o metal some do posto', 'a galeria desaba', 'a mina está perdida'],
                 [[('produz', 'metal:0', 0.9)], [('produz', 'metal:0', 0.8), ('missao',)], [('produz', 'metal:0', 0.8)], [('estoque', 'metal:0', -0.4)], [('morre', 'mineiro')], [('produz', 'metal:0', 0.3)]], 'entrega', 'entregue'),
    'sumiços':  ('mistério', 'os sumiços {dono}', 'levar a gente do lugar, um a um',
                 ['alguém some na borda do mato', 'acham um corpo sem sangue', 'mais um some, de dentro de casa', 'o povo não sai mais de noite', 'some um da guarda', 'o lugar se esvazia de medo'],
                 [[('povo', -0.01)], [('morre', 'lavrador'), ('missao',)], [('povo', -0.02)], [('estoque', 'comida', -0.1)], [('morre', 'guarda')], [('povo', -0.4)]], 'investigar', 'dono'),
    'luzes':    ('mistério', 'as luzes {dono}', 'acordar o que está selado',
                 ['luzes nas ruínas de noite', 'os bichos fogem do mato', 'um caçador volta louco', 'a terra treme de noite', 'as luzes chegam ao lugar', 'o selo quebra: algo sai'],
                 [[('fama', 1)], [('bichos', -3)], [('morre', 'caçador'), ('missao',)], [('estoque', 'comida', -0.05)], [('povo', -0.03)], [('vagantes', 4), ('povo', -0.1)]], 'investigar', 'limpa'),
    'calamidade': ('calamidade', '{dono}, o que dorme', 'acordar',
                 ['a serra treme de noite', 'os bichos da serra fogem para o vale', 'cai cinza nos campos', 'o dragão jovem foge da serra', 'a fumaça sai da boca do covil', 'o dragão ancião acorda'],
                 [[('bichos', -4)], [('bichos', -6)], [('estoque', 'comida', -0.05)], [('fama', 3)], [('povo', -0.05)], [('acorda',)]], None, 'nunca'),
    'praga':    ('falta', 'a praga do gado {dono}', 'matar o gado da terra',
                 ['uma vaca amanhece morta', 'o gado adoece no pasto', 'o couro some da feira', 'a carne falta na mesa', 'a praga chega aos bois de arado', 'o pasto fica vazio'],
                 [[('estoque', 'couro:0', -0.2)], [('produz', 'couro:0', 0.8), ('missao',)], [('estoque', 'couro:0', -0.3)], [('estoque', 'comida', -0.05)], [('produz', 'comida', 0.95)], [('produz', 'couro:0', 0.5)]], 'entrega', 'entregue'),
    'sal':      ('falta', 'a falta de sal {dono}', 'acabar com o sal da terra',
                 ['o sal some da feira', 'a carne apodrece sem sal', 'o mercador de sal não vem mais', 'o povo briga pelo que sobra', 'a carne do inverno se perde', 'o lugar fica sem sal'],
                 [[('estoque', 'sal', -0.3)], [('estoque', 'comida', -0.03), ('missao',)], [('produz', 'sal', 0.7)], [('estoque', 'sal', -0.4)], [('estoque', 'comida', -0.05)], [('produz', 'sal', 0.5)]], 'entrega', 'entregue'),
    'fome':     ('falta', 'a fome {dono}', 'esvaziar o celeiro',
                 ['o celeiro está no fim', 'o povo come a semente', 'a primeira morte de fome', 'o povo foge pela estrada', 'os famintos viram salteadores', 'o lugar se esvazia'],
                 [[('missao',)], [('produz', 'comida', 0.9)], [('povo', -0.02)], [('povo', -0.05)], [('bando', 3)], [('povo', -0.3)]], 'entrega', 'farto'),
    'nêmesis':  ('nêmesis', '{dono}, o matador', 'acabar com o sangue de quem matou',
                 ['o matador veste o que tirou do morto', 'o matador fica sabendo do herdeiro', 'o matador procura o herdeiro', 'o matador fere um parente', 'o matador cerca a casa', 'o matador encontra o herdeiro'],
                 [[('fama', 2)], [('fama', 1)], [('fama', 1)], [('fama', 2)], [('fama', 1)], [('fama', 3)]], 'matar', 'dono'),
}
FRENTES_DIA1 = ['bando', 'horda', 'mortos', 'dragão', 'trono', 'cartel', 'culto', 'guilda', 'falta', 'falta', 'sumiços', 'luzes', 'calamidade']
FALTAS_DIA1 = ['seca', 'mina', 'praga', 'sal']      # as duas faltas do Dia 1 saem destas, pelo acaso do mundo (a seca não está em todo mundo)
FRENTE_ROLA = dict(dado=(2, 10), contra=17, comeco=3, forca=(2, 5), resiste_guarda=20, calamidade_cada=28, ambicao=2)     # por semana: 2d10 + força contra 17 (3 a menos nos dois primeiros passos: a frente aparece depressa) + a resistência do lugar (+1 a cada 20 da guarda); a ambição, +2 de força (mora em lugar forte); a calamidade rola a cada 28 dias
INVESTIGA = dict(contra=22, cat=2, campos=('passo', 'dono', 'meta', 'onde'))      # investigar: 2d20 + Percepção ÷ 10 + manha contra 22 + 2 por categoria da frente; abre um campo por vez

# ---------- os rivais (rivais.py) ----------
RIVAL = dict(ousadia={'novato': 0.25, 'oficial': 0.33, 'veterano': 0.5, 'Lenda': 0.6},     # a chance mínima de vencer que cada um aceita para ir
             morre=0.7, morre_junto=0.6,      # (quem vai junto morre menos que quem vai na frente)
                        # quem perde a luta da conta rápida: a chance de morrer (cada um do grupo), vezes o quanto a luta era ruim
             fere=0.6,                # ... e a de sair ferido (descansa uma semana)
             longe={'novato': 2, 'oficial': 3, 'veterano': 4, 'Lenda': 6},       # até quantas estradas da casa o rival vai atrás de missão, masmorra ou chefe
             olho=0.15,               # a base da chance de o rival expor a frente que investiga (mais a Percepção e a manha)
             dias_masmorra=(2, 2),    # os dias de uma descida: tantos, mais tantos por nível
             forja_ferreiro=6,        # a maestria de forja do ferreiro que faz a peça do núcleo (o melhor da capital)
             forja_chance={4: 0.4, 6: 0.6, 8: 0.75}, forja_sinal=0.4,       # (o ferreiro começa a obra com 40% do preço na mão; o resto, quando entrega)
                  # a chance de a peça Épica do núcleo sair inteira, pela maestria do ferreiro (cada categoria acima, vezes 0,75)
             forja_paga=0.08,         # a fração do valor da peça que o ferreiro cobra (o Épico: uns 520 de prata); os dias da obra: 3 elevado à categoria (o Épico, 27; o Único, 81)
             chefe_fama=150,          # só vai atrás do chefe do ermo quem já tem esta fama
             caca_morre={'novato': 0.008, 'oficial': 0.005, 'veterano': 0.003, 'Lenda': 0.001},      # por semana de caça para viver, a chance de morrer nela
             caca_rende=(8, 30),      # o que uma semana de caça rende a um rival (em bens vendidos na casa dele)
             novos=0.5,               # a cada estação, entram tantos novatos quantos esta fração dos que faltam para 40
             torneio_dia=150, torneio_premio=200, leilao_cada=91, leilao_dia=45)
RANKING_PECA = 5           # no ranking, cada categoria da melhor arma e da melhor armadura em uso vale isto (mais a fama)

# ---------- a criação do personagem (cria.py) ----------
NIVEL_PERSONAGEM = 5        # o nível de quem começa (o da vila de teste, onde a luta foi afinada)
# os berços: (o papel da família, onde ela mora, o que se diz, os atributos (soma 340), a mão, o grau, as peças [(tipo, qual, cat, cobre, uso)], a prata, a carga, o laço com o chefe da família, a magia)
BERCOS = {
    'forja':    ('ferreiro', ('vila', 'posto', 'aldeia'), 'cresceu na forja da família; tem a mão de Iniciante no martelo e na forja',
                 dict(Força=65, Agilidade=50, Vigor=65, Vontade=50, Percepção=45, Afinidade=65), {'forja': 2, 'martelo': 2}, 'aprendiz',
                 [('arma', 'martelo', 0, None, 'arma'), ('armadura', 'couro', 0, None, 'veste')], 30, {'metal:0': 4, 'madeira:0': 2}, 'pai', None),
    'caça':     ('caçador', ('aldeia', 'vila'), 'cresceu no mato com a família de caçadores; tem a mão de Iniciante no rastro e no arco',
                 dict(Força=55, Agilidade=70, Vigor=60, Vontade=45, Percepção=70, Afinidade=40), {'caça': 2, 'arco': 2}, 'diarista',
                 [('arma', 'arco', 0, None, 'arma'), ('arma', 'adaga', 0, None, 'arma2'), ('armadura', 'couro', 0, None, 'veste')], 20, {'comida': 3}, 'pai', None),
    'guarda':   ('guarda', ('cidade', 'capital', 'vila'), 'cresceu na casa da guarda; tem a mão de Iniciante na espada',
                 dict(Força=70, Agilidade=60, Vigor=70, Vontade=50, Percepção=50, Afinidade=40), {'espada': 2}, 'diarista',
                 [('arma', 'espada', 0, None, 'arma'), ('escudo', None, 0, None, 'escudo'), ('armadura', 'malha', 0, None, 'veste')], 30, {}, 'pai', None),
    'mercador': ('mercador', ('capital', 'cidade'), 'cresceu atrás do balcão da casa de comércio; tem a mão de Iniciante no comércio e na adaga',
                 dict(Força=50, Agilidade=55, Vigor=55, Vontade=60, Percepção=60, Afinidade=60), {'comércio': 2, 'adaga': 2}, 'diarista',
                 [('arma', 'adaga', 0, None, 'arma'), ('armadura', 'couro', 0, None, 'veste')], 120, {'pano': 4}, 'pai', None),
    'templo':   ('sacerdote', ('cidade', 'capital', 'vila'), 'deixado no santuário quando criança, e criado lá; tem a mão de Iniciante na cura e na maça, e sabe a luz',
                 dict(Força=50, Agilidade=55, Vigor=55, Vontade=70, Percepção=55, Afinidade=55), {'cura': 2, 'maça': 2}, 'diarista',
                 [('arma', 'maça', 0, None, 'arma'), ('armadura', 'couro', 0, None, 'veste')], 10, {'erva:0': 3}, 'mestre', dict(feiticos=['luz'])),
    'nobre':    ('senhor', ('cidade', 'vila'), 'da casa nobre que manda no lugar; tem a mão de Iniciante na espada, a espada da família e inimigos que nunca viu',
                 dict(Força=65, Agilidade=60, Vigor=65, Vontade=55, Percepção=50, Afinidade=45), {'espada': 2}, 'diarista',
                 [('arma', 'espada', 1, None, 'arma'), ('escudo', None, 0, None, 'escudo'), ('armadura', 'malha', 0, None, 'veste')], 80, {}, 'pai', None),
}
