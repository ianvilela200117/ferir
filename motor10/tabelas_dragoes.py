"""tabelas_dragoes.py — MOTOR 10, ETAPA 4b: TODOS os números dos dragões (capítulo 20; o contrato: projeto/ETAPA_4B.md, seções 2, 9 e 12).

Três tipos, pelo lugar onde vivem (o dragão da serra, o verme do brejo, o dragão das grutas), cinco idades (do filhote, grau D, ao ancião, grau S). Tudo roda com os traços
que a luta já tem, mais a fase `foge` (o dragão que voa, ferido fora do covil, vai embora pelo ar: E3 a).
O NÚCLEO DO MOTOR LÊ DAQUI: TIPOS e IDADES (o gravador confere o registro `dragao` de um lugar), `chave(tipo, idade)` e ESPECIES (estado.especie, bichos.especie, o atalho
do cenário {"bicho": CHAVE}). ESPECIES é feita pela frente D (as 15 chaves, cada uma um registro na forma do tabelas_bichos.ESPECIES, mais `fases` e `dragao`).
Esqueleto do alicerce (onda 1): os números são o rascunho do projeto B (projeto/etapa4b/projeto_b/PROJETO.md, anexo); ESPECIES vazia: nenhum dragão ainda.
"""

# ---------- as idades: cat · tamanho · nível · instinto · (Força, Agilidade, Vigor, Vontade, Percepção, Afinidade) · armas · traços · anos · chefe ----------
IDADES = {
    'filhote': dict(cat=1, tamanho='médio',  nivel=30,  instinto=2, at=(70, 80, 70, 50, 70, 40),    armas=['garra', 'presa'],            tracos=['sopro'],                                  anos=(0, 30),      chefe=False),
    'jovem':   dict(cat=2, tamanho='grande', nivel=80,  instinto=6, at=(120, 70, 150, 60, 75, 45),  armas=['garra', 'bocarra', 'cauda'], tracos=['sopro', 'apavora'],                       anos=(30, 150),    chefe=True),
    'adulto':  dict(cat=3, tamanho='enorme', nivel=110, instinto=6, at=(140, 70, 150, 80, 85, 50),  armas=['garra', 'bocarra', 'cauda'], tracos=['sopro', 'apavora', 'couraça'],            anos=(150, 500),   chefe=True),
    'velho':   dict(cat=4, tamanho='enorme', nivel=160, instinto=6, at=(160, 70, 200, 90, 90, 55),  armas=['garra', 'bocarra', 'cauda'], tracos=['sopro', 'apavora', 'couraça', 'resiste'], anos=(500, 1000),  chefe=True),
    'ancião':  dict(cat=5, tamanho='enorme', nivel=220, instinto=8, at=(180, 70, 240, 100, 90, 60), armas=['garra', 'bocarra', 'cauda'], tracos=['sopro', 'apavora', 'couraça', 'resiste'], anos=(1000, None), chefe=True),
}

# ---------- os tipos (pelo lugar; nada de cor) ----------
TIPOS = {
    'serra':  dict(nome='o dragão da serra', prefixo='dragão-da-serra', habitat=['serra', 'ruína'], mais=['voa'], sopro='o fogo', casa={},
                   fase=dict(abaixo=0.3, foge=True, perde=['voa'], ganha=['ardente'], diz='desce ao chão em fúria')),
    'brejo':  dict(nome='o verme do brejo', prefixo='verme-do-brejo', habitat=['brejo'], mais=['veneno'], sopro='o bafo podre', casa=dict(tempo=['água']),
                   fase=dict(abaixo=0.5, ganha=['agarra'], diz='enrosca na lama'), peconha=True),
    'grutas': dict(nome='o dragão das grutas', prefixo='dragão-das-grutas', habitat=['caverna', 'ruína'], mais=['noturno', 'agarra'], sopro='a brasa e a fumaça', casa=dict(tempo=['escuro']),
                   fase=dict(abaixo=0.5, ganha=['dreno'], diz='bebe o sangue de quem prende')),
}
def chave(tipo, idade):
    """a chave da espécie de um dragão (a do tabelas_dragoes.ESPECIES e do atalho do cenário): 'dragão-da-serra-jovem', 'verme-do-brejo-filhote', 'dragão-das-grutas-ancião'"""
    return f"{TIPOS[tipo]['prefixo']}-{idade}"

# ---------- o corpo, o núcleo e o tesouro ----------
DESPOJO = {'filhote': {'comida': 4, 'couro:1': 3, 'osso:1': 2}, 'jovem': {'comida': 10, 'couro:2': 5, 'osso:2': 4},
           'adulto': {'couro:2': 8, 'osso:2': 6}, 'velho': {'couro:2': 10, 'osso:2': 8}, 'ancião': {'couro:2': 12, 'osso:2': 10}}
PECONHA = {'filhote': {'peçonha:1': 1}, 'outros': {'peçonha:2': 2}}           # só o verme do brejo
NUCLEO_DESDE = 3            # o núcleo (o coração) só do Épico para cima (o adulto): a escada da forja não pede núcleo abaixo disso
SARA_DORMINDO = 0.10        # o dragão ferido sara isto do PV por dia de sono
TESOURO = {'jovem': (0.01, (2, 3), 2), 'adulto': (0.03, (3, 5), 3), 'velho': (0.06, (4, 6), 4), 'ancião': (0.10, (5, 8), 5)}   # a prata (fração da prata do mundo), as peças, a melhor categoria
TESOURO_MUNDO = 0.25        # todos os covis juntos (meta MI6, não invariante)

# ---------- a vida do dragão (evento "dragão", todo dia) ----------
VIDA = {    # dorme: dias de sono depois de comer · come: gado de um ataque · prata e mata: (de, até) · tributo: fração da prata da vila por estação
    'jovem':  dict(dorme=(20, 40), come=30, prata=(5, 20), mata=(0, 1), tributo=0),
    'adulto': dict(dorme=(30, 60), come=60, prata=(20, 60), mata=(0, 3), tributo=0.03),
    'velho':  dict(dorme=(90, 180), come=120, prata=(50, 150), mata=(1, 5), tributo=0.05),
    'ancião': dict(dorme=(300, 400), come=200, prata=(100, 300), mata=(2, 8), tributo=0.08),
}
VIGILIA = dict(base=20, leve=2, sobe=2)      # contra 20 + Percepção ÷ 10 + 2, e +2 a cada punhado tirado no mesmo sono (o teste do ladrão: manha.testa 'escondido')
CONTA = dict(filhote=(0, 2), jovem=(1, 3), adulto=(1, 2), velho=(0, 1), ancião=(0, 1))   # numa região de 16 lugares (para o gerador da etapa 7)

# ---------- as espécies (as 15 chaves de chave(tipo, idade)): a frente D as monta ----------
ESPECIES = {}
