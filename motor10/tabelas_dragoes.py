"""tabelas_dragoes.py — MOTOR 10, ETAPA 4b: TODOS os números dos dragões (capítulo 20; o contrato: projeto/ETAPA_4B.md, seções 2, 9 e 12).

Três tipos, pelo lugar onde vivem (o dragão da serra, o verme do brejo, o dragão das grutas), cinco idades (do filhote, grau D, ao ancião, grau S). Tudo roda com os traços
que a luta já tem, mais a fase `foge` (o dragão que voa, ferido fora do covil, vai embora pelo ar: E3 a).
O NÚCLEO DO MOTOR LÊ DAQUI: TIPOS e IDADES (o gravador confere o registro `dragao` de um lugar), `chave(tipo, idade)` e ESPECIES (estado.especie, bichos.especie, o atalho
do cenário {"bicho": CHAVE}). ESPECIES são as 15 chaves (3 tipos e 5 idades), cada uma um registro na forma do tabelas_bichos.ESPECIES, mais `fases` e `dragao`.
Mudar um dragão é mudar esta página e rodar `python3 provas_dragoes.py` (as metas DR1 a DR9 e MI1 a MI6).
"""
import tabelas_bichos as _TB

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
    'filhote': dict(dorme=(10, 20), come=0, prata=(0, 0), mata=(0, 0), tributo=0),      # o filhote não ataca vila: caça no ermo e volta a dormir
    'jovem':  dict(dorme=(20, 40), come=30, prata=(5, 20), mata=(0, 1), tributo=0),
    'adulto': dict(dorme=(30, 60), come=60, prata=(20, 60), mata=(0, 3), tributo=0.03),
    'velho':  dict(dorme=(90, 180), come=120, prata=(50, 150), mata=(1, 5), tributo=0.05),
    'ancião': dict(dorme=(300, 400), come=200, prata=(100, 300), mata=(2, 8), tributo=0.08),
}
VIGILIA = dict(base=20, leve=2, sobe=2)      # contra 20 + Percepção ÷ 10 + 2, e +2 a cada punhado tirado no mesmo sono (o teste do ladrão: manha.testa 'escondido')
CONTA = dict(filhote=(0, 2), jovem=(1, 3), adulto=(1, 2), velho=(0, 1), ancião=(0, 1))   # numa região de 16 lugares (para o gerador da etapa 7)

# ---------- o covil do gerador (masmorra.gera, molde covil): o nome do dragão que mora lá (um nome é de um dragão só) ----------
NOMES = ['o Brasido', 'o Fuligem', 'o Ronco', 'o Lodo', 'o Garrudo', 'o Rachado', 'o Cinzento', 'o Torto', 'o Urro', 'o Musgo', 'o Pedrês', 'o Sem-Sono']

# ---------- a vila de teste (E4 a): o dragão jovem longe, em Vau Seco, que só se conta (dragoes.na_vila) ----------
VILA_TESTE = dict(
    aldeia=dict(id='vau', nome='Vau Seco', em='em Vau Seco', tipo='aldeia', pop=120),       # a aldeia que ele ataca: com mercado (a prata de tabela: 5 por cabeça), longe de Pedra Rasa
    covil=dict(id='serra_fria', nome='a Serra Fria', em='na Serra Fria', habitat='serra', perigo=3, longe=6),       # o ermo do covil: vizinho de Vau Seco, não de Pedra Rasa
    dragao=dict(nome='o Tição', tipo='serra', idade='jovem', anos=60, tesouro=300, dorme=20, ult_ataque=6),      # dorme mais 20 dias; o último ataque foi há 6 dias
    pecas=[('arma', 'espada', 2, 'a Lâmina de Vau Seco', 'a espada do último que enfrentou o Tição: ficou no covil com o dono'),
           ('escudo', None, 1, 'o escudo do caçador de Vau Seco', 'o escudo de um caçador de Vau Seco que subiu a serra e não voltou')],
)

# ---------- o covil, a fuga, o roubo e o boato ----------
SARA_MIN = 1                # o dragão que fugiu ferido volta ao covil e dorme os dias de sarar (de SARA_DORMINDO em SARA_DORMINDO do PV), pelo menos isto
PUNHADO = 6                 # o punhado do ladrão: a sexta parte da prata que havia no covil quando o dragão adormeceu (sem prata, uma peça guardada)
BOATO = 60                  # a pousada conta o último ataque por tantos dias; depois, só que o dragão mora lá
FERIU_MAX = 6               # o dragão lembra de quem o feriu (E3 a): os últimos tantos nomes

# ---------- as espécies (as 15 chaves de chave(tipo, idade)) ----------
# o nome que vai à mesa: "o filhote de dragão da serra", "o verme jovem do brejo", "o dragão ancião das grutas" (o artigo é "o" em todos)
NOME = {'serra': ('dragão', 'da serra'), 'brejo': ('verme', 'do brejo'), 'grutas': ('dragão', 'das grutas')}
SABE = {
    'serra':  'voa e sopra fogo; ferido, no covil desce ao chão em fúria (quem o golpeia de perto se queima), e fora dele foge pelo ar e volta ao covil para sarar',
    'brejo':  'não tem asas; o golpe envenena; luta melhor na água; ferido, enrosca na lama e prende quem está colado',
    'grutas': 'não tem asas; o escuro não lhe tira nada; prende quem está colado; ferido, bebe o sangue de quem prende',
}
SABE_FILHOTE = 'um filhote ainda: testa a coragem como qualquer bicho, e foge ferido'
SABE_CHEFE = 'o dragão grande não foge pelo susto: só ferido, e só o que voa, fora do covil'
CORAGEM = 0                 # o dragão não soma nada na coragem (o filhote testa como bicho; do jovem para cima a moral é firme)
PAVOR = dict(jovem=_TB.PAVOR + 1)       # O PAVOR DO DRAGÃO JOVEM (a parte 2, fase 1b): quem começa a luta contra ele testa a coragem contra isto, 1 acima do pavor dos outros
                            # (tabelas_bichos.PAVOR, que segue valendo do adulto ao ancião). A escada do medo (DESENHO 3.6) segura no ACUADO quem antes quebrava, e o grupo de 4 do
                            # degrau passou a vencer o jovem da serra em 76-77% (a meta DR2: 50 a 75; sem a escada, 72-73%); com o pavor 1 acima, 71-72% (1.000 lutas, três sementes).
                            # Com 2 acima, 68-69%, mas o pequenino do PO7 (provas_povos) fugia 6,1% (a meta: até 6); nas quatro idades, o velho do brejo caía a 24,8% (a meta: 25 a 50).
                            # O Mestre confirma (DESENHO 12.3; a outra saída é a faixa do jovem até 80, que pede a palavra do jogador)


def _especie(tipo, idade):
    i = IDADES[idade]; t = TIPOS[tipo]; n, de = NOME[tipo]
    nome = f'filhote de {n} {de}' if idade == 'filhote' else f'{n} {idade} {de}'
    tr = list(dict.fromkeys(i['tracos'] + t['mais']))
    desp = dict(DESPOJO[idade])
    if t.get('peconha'): desp.update(PECONHA['filhote' if idade == 'filhote' else 'outros'])
    sabe = f"{SABE[tipo]}; " + (SABE_FILHOTE if not i['chefe'] else SABE_CHEFE)
    e = _TB._esp(nome, 'o', i['cat'], _TB.GRAU_DA_CAT[i['cat']][0], i['nivel'], i['instinto'], i['at'], i['armas'], 'escama', i['tamanho'], tr, CORAGEM, (1, 1),
                 desp, t['habitat'], sabe, chefe=i['chefe'])
    e['nucleo'] = i['cat'] >= NUCLEO_DESDE                  # o coração do dragão: só do adulto (Épico) para cima
    e['fases'] = [dict(t['fase'], foge_diz='foge pelo ar, ferido') if t['fase'].get('foge') else dict(t['fase'])] if i['chefe'] else []
    e['dragao'] = dict(tipo=tipo, idade=idade, **({'pavor': PAVOR[idade]} if 'apavora' in tr and idade in PAVOR else {}))
    return e


ESPECIES = {chave(t, i): _especie(t, i) for t in TIPOS for i in IDADES}
