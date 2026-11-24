"""tabelas_povos.py — MOTOR 10, ETAPA 4b: TODOS os números dos povos do personagem (capítulo 19; o contrato: projeto/ETAPA_4B.md, seções 8 e 12).

Seis povos: o humano (a medida de todos), o anão, o elfo, o meio-orc, o pequenino e o gnomo. Cada um mexe nos seis atributos COM A SOMA IGUAL (soma zero), tem de
nenhum a dois traços da lista fechada (tabelas.TRACOS_POVO), uma coragem, um CORPO (gente ou miúdo: a armadura é feita para o corpo), uma TENDÊNCIA nos talentos (um caminho
a favor, um contra), a vida longa, e um bônus de +2 num teste do ladino (o teto de +2 por teste).
O NÚCLEO DO MOTOR LÊ ESTA PÁGINA DIRETO (o gravador, o lutador, o talento, a luta): os campos de POVOS (mods, tracos, coragem, corpo, a_favor, contra, vida, frase) e os
números ESCURO e VENENO. Mudar um povo é mudar esta página e rodar `provas_povos.py` (o `provas_mundo.py` também o roda): a lei é que nenhum povo pese mais que o Grande Dom.

COMO OS NÚMEROS FORAM AFINADOS (a frente P, com a luta de verdade: provas_povos.py, PO1 a PO3). O rascunho do projeto B tinha sido medido com o traço emulado. Construído,
o banco achou três coisas, e os números abaixo são o acerto delas:
  - o atributo pesa aos degraus de 10 (o golpe, a Defesa, a iniciativa); só o Vigor pesa ponto a ponto (o PV). O Vigor é a alavanca: +5 vale uns 3 a 4 pontos no duelo;
  - com o Vigor +5, o anão e o meio-orc passavam rente aos 60% no escuro (59,2 e 58,8): o anão ficou com +2, o meio-orc com 0 (a força dele é a Força);
  - com o Vigor −5, o gnomo caía a 39% no nível 5 (abaixo dos 40): ficou com 0; o elfo, com −3; o pequenino, com +3 (o nível 5 dele estava rente, a 42%);
  - no tiro, a metade do escuro dava ao arqueiro que vê no escuro de 63 a 67% contra o arqueiro humano, de noite (passa do Grande Dom, 59,8%): no tiro e no feitiço que
    voa, o escuro pesa inteiro (ESCURO_TIRO). De perto vale a metade, como o juízo decidiu (ESCURO).
"""

# ---------- os povos ----------
# mods: o que soma em cada atributo (a soma é zero) · tracos: a lista fechada (tabelas.TRACOS_POVO) · coragem: soma no teste de coragem · corpo: 'gente' ou 'miúdo'
# a_favor / contra: o caminho da tendência (tabelas_talento.TENDENCIA: melhor de dois / pior de dois) · vida: (adulto aos, velho aos, o máximo) · frase: o que o jogador lê
POVOS = {
    'humano':    dict(mods={}, tracos=[], coragem=0, corpo='gente', a_favor=None, contra=None, vida=(16, 60, 90),
                      frase='a medida de todos: nada a mais, nada a menos'),
    'anão':      dict(mods=dict(Vigor=2, Vontade=5, Agilidade=-5, Percepção=-2), tracos=['vê no escuro', 'resiste a veneno'], coragem=0, corpo='gente',
                      a_favor='forja', contra='verde', vida=(30, 200, 300),
                      frase='duro, teimoso e de vista curta; vê na penumbra das minas, e o veneno o pega pela metade'),
    'elfo':      dict(mods=dict(Agilidade=10, Percepção=8, Afinidade=5, Vigor=-3, Força=-10, Vontade=-10), tracos=['vê no escuro'], coragem=0, corpo='gente',
                      a_favor='tiro', contra='peso', vida=(80, 500, 800),
                      frase='leve e de olho longo, frágil de corpo e de pouca paciência; vê na penumbra'),
    'meio-orc':  dict(mods=dict(Força=5, Afinidade=-5), tracos=['vê no escuro'], coragem=0, corpo='gente',
                      a_favor='peso', contra='encanto', vida=(14, 50, 75),
                      frase='forte e de sangue quente; vê na penumbra, como o pai orc'),
    'pequenino': dict(mods=dict(Força=-15, Agilidade=5, Percepção=2, Vigor=3, Vontade=5), tracos=[], coragem=4, corpo='miúdo',
                      a_favor='manha', contra='haste', vida=(25, 80, 130),
                      frase='miúdo, rijo e sem medo: o pavor pega pouco nele, e anda sem ser ouvido'),
    'gnomo':     dict(mods=dict(Afinidade=10, Percepção=5, Força=-10, Vontade=-5), tracos=['vê no escuro'], coragem=0, corpo='miúdo',
                      a_favor='encanto', contra='peso', vida=(35, 250, 400),
                      frase='miúdo, curioso e de mão fina; vê na penumbra, e o mecanismo não tem segredo para ele'),
}
HUMANO = 'humano'           # quem não tem o campo `povo` é humano (o save antigo, a gente de hoje)
CORPOS = ('gente', 'miúdo')
PLURAL = {'humano': 'humanos', 'anão': 'anões', 'elfo': 'elfos', 'meio-orc': 'meio-orcs', 'pequenino': 'pequeninos', 'gnomo': 'gnomos'}      # "do povo dos anões" (a mesa não sabe se é ele ou ela)
FORMAS = {'humano': ('humano', 'humana'), 'anão': ('anão', 'anã'), 'elfo': ('elfo', 'elfa'), 'meio-orc': ('meio-orc',), 'pequenino': ('pequenino', 'pequenina'), 'gnomo': ('gnomo', 'gnoma')}      # como o povo se diz no começo do "sobre"

# ---------- os traços do povo (a frase; os nomes moram no tabelas.TRACOS_POVO) ----------
TRACOS = {'vê no escuro': 'de perto, o escuro pesa só a metade, −2 no golpe e não −4; no tiro e no feitiço que voa, pesa inteiro; fora da luta, anda, procura, abre e desarma sem luz',
          'resiste a veneno': 'o veneno tira a metade por rodada'}
ESCURO = 0.5                # a fração do escuro (tabelas.TEMPO['escuro']) que ainda pesa no golpe de quem vê no escuro: a metade (o juízo da etapa)
ESCURO_TIRO = 1.0           # a fração do escuro que pesa no TIRO e no feitiço que voa de quem vê no escuro: inteiro (medido: com a metade, o arqueiro que vê no escuro vence
                            # o humano de 63 a 67% de noite). O luta.py e o magia.py passam a ler este número no lugar do ESCURO quando o golpe é de longe (pedido ao integrador)
VENENO = 0.5                # a fração do veneno (o que entra por rodada) que pesa em quem resiste a veneno

# ---------- o +2 do povo nos testes do ladino (os testes: tabelas_manha.TESTES; achar_pedra: o achar em lugar de pedra, a cripta, a mina, a ruína) ----------
MANHA = {'pequenino': {'escondido': 2}, 'elfo': {'achar': 2}, 'anão': {'achar_pedra': 2}, 'gnomo': {'gazua': 2, 'desarmar': 2}, 'meio-orc': {'arrombar': 2}}
MANHA_TETO = 2              # o povo não soma mais que isto num teste (um grau de maestria, o mesmo do Grande Dom)
MANHA_DIZ = {'escondido': 'andar escondido', 'escutar': 'escutar', 'achar': 'achar a armadilha e a passagem escondida', 'achar_pedra': 'achar a armadilha e a passagem na pedra (cripta, mina, ruína)',
             'gazua': 'abrir fechadura', 'desarmar': 'desarmar armadilha', 'arrombar': 'arrombar', 'atencao': 'vigiar'}

# ---------- a idade de quem nasce agora (o personagem): a de adulto do povo mais um dado ----------
IDADE_DADO = 10             # o personagem nasce com a idade de adulto do povo mais 1d10 anos (o dado do mundo: idade|PESSOA)

# ---------- a gente do mundo (proposta para o gerador da região, etapa 7: aqui é chute) ----------
# {lugar: {povo: fração}}; a loja de cada lugar põe na prateleira as armaduras dos corpos da gente dele, na proporção
GENTE = {
    'capital':          {'humano': 0.80, 'anão': 0.06, 'elfo': 0.03, 'meio-orc': 0.04, 'pequenino': 0.05, 'gnomo': 0.02},
    'cidade':           {'humano': 0.85, 'anão': 0.05, 'elfo': 0.02, 'meio-orc': 0.03, 'pequenino': 0.04, 'gnomo': 0.01},
    'cidade da serra':  {'humano': 0.25, 'anão': 0.65, 'meio-orc': 0.02, 'pequenino': 0.03, 'gnomo': 0.05},
    'vila da floresta': {'humano': 0.30, 'elfo': 0.65, 'pequenino': 0.05},
    'vila':             {'humano': 0.80, 'anão': 0.02, 'elfo': 0.01, 'meio-orc': 0.02, 'pequenino': 0.14, 'gnomo': 0.01},
    'fronteira orc':    {'humano': 0.70, 'anão': 0.03, 'meio-orc': 0.25, 'pequenino': 0.02},
    'tocas da colina':  {'humano': 0.20, 'anão': 0.10, 'pequenino': 0.10, 'gnomo': 0.60},
    'rivais':           {'humano': 0.70, 'anão': 0.10, 'elfo': 0.08, 'meio-orc': 0.06, 'pequenino': 0.04, 'gnomo': 0.02},
}

# ---------- a vila de teste (povos.na_vila: acrescenta, só por eventos "gera") ----------
# a gente de Pedra Rasa · a gente de outros povos: (id, nome, povo, idade, sobre, nível, molde, grau de ofício, maestria, prata, as peças: (tipo, família ou material, categoria, cobre, uso))
# · a prateleira: as armaduras miúdas Comuns (tipo, material, categoria, cobre)
VILA = dict(
    povos={'humano': 0.88, 'pequenino': 0.08, 'anão': 0.02, 'meio-orc': 0.02},
    gente=[
        ('durva', 'Durva', 'anão', 112, 'anã, ferreira de passagem; forja e conserta, e vai junto se a chamam', 34, 'guerreiro', 'oficial', {'forja': 4, 'martelo': 4}, 40,
         [('arma', 'martelo', 1, None, 'arma'), ('armadura', 'couro', 1, None, 'veste')]),
        ('brasco', 'Brasco', 'meio-orc', 31, 'meio-orc, guarda de caravana de passagem; viu o que o dragão deixou em Vau Seco', 26, 'guerreiro', 'diarista', {'malho': 4}, 30,
         [('arma', 'malho', 0, None, 'arma'), ('armadura', 'malha', 0, None, 'veste')]),
        ('ilvena', 'Ilvena', 'elfo', 240, 'elfa, caçadora de passagem; segue rastro de noite', 38, 'arqueiro', 'aprendiz', {'arco': 4, 'caça': 4, 'adaga': 2}, 25,
         [('arma', 'arco', 1, None, 'arma'), ('arma', 'adaga', 0, None, 'arma2'), ('armadura', 'couro', 1, None, 'veste')]),
        ('nena', 'Nena Ramalho', 'pequenino', 44, 'pequenina, faz o pão da pousada; mora na vila', 9, 'comum', 'aprendiz', {'coleta': 2}, 12, []),
    ],
    loja=[('armadura', 'couro', 0, None), ('armadura', 'malha', 0, None), ('armadura', 'malha', 0, ['cabeça'])],
)
