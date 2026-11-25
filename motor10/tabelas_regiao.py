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
FOME_DIAS = 10              # o celeiro abaixo de tantos dias de comida: o povo começa a sair (e nasce a frente da fome)
FOME_MORRE = 0.01           # sem comida nenhuma no celeiro: esta fração do povo morre por dia (e outro tanto sai)
MIGRA = 0.005               # com o celeiro baixo: esta fração do povo vai por dia para o vizinho mais farto
BANDO_FOME = 0.15           # com o celeiro baixo: a chance, por dia e por estrada do lugar, de um faminto virar salteador
BANDO_TETO = 12             # nenhuma estrada passa de tantos salteadores
COMERCIO = dict(bens=('comida', 'lenha', 'sal', 'pano', 'ferramenta', 'metal:0', 'couro:0'), razao=1.35, lote=0.04, teto=0.15)
                            # o comércio entre lugares (os mercadores, em número): por estrada aberta e por dia, se o preço do outro lado passa de `razao` vezes o daqui,
                            # leva até `lote` do estoque daqui (e não mais que `teto` do alvo de lá); a prata vai do lugar que compra para o que vende, no preço do meio
GUARDA_PATRULHA = 0.02      # por soldado da guarda (em número), por dia: a chance de a patrulha tirar um salteador da estrada vizinha
