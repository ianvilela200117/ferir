"""tabelas_criaturas.py — MOTOR 10, ETAPA DA MAGIA: TODOS os números das CRIATURAS num lugar só (os povos que vestem peças de verdade, os mortos que andam,
os seres de magia, as feras que faltam, os chefes mágicos e os covis).

A regra mora no criaturas.py; os números da luta de magia, no tabelas_magia.py (a frente da luta); os bichos de antes, no tabelas_bichos.py.
DUAS TRANCAS da etapa 2 (o provas.py as confere): as criaturas NÃO entram no tabelas_bichos.ESPECIES, e os traços novos NÃO entram no tabelas_bichos.TRACOS.
As criaturas moram em ESPECIES (aqui); os nomes dos traços novos, em tabelas.TRACOS_NOVOS; a frase de cada um, em TRACOS (aqui).
Mudar uma criatura é mudar esta página e rodar `python3 provas_criaturas.py` (ou `provas_mundo.py`, que o chama).

O POVO (goblin, orc, ogro...) é GENTE: a ficha de gente (pessoas.ficha), com arma, armadura e escudo de verdade, e o corpo do povo por cima (o tamanho, os traços,
a coragem e a pele). A peça do povo é GASTA E MALFEITA: na luta vale a categoria dela; morto o dono, não presta para vender como peça: é sucata (o despojo).
A CRIATURA DE CORPO (o morto que anda, o ser de magia, a fera) é um bicho: o corpo é a arma e a armadura, com categoria (bichos.py), e pode trazer traços novos.
"""
import tabelas as T
import tabelas_bichos as TB
import tabelas_magia as TM

# ---------- AS FRASES DOS TRAÇOS NOVOS (a lista é tabelas.TRACOS_NOVOS; a luta os roda com os números do tabelas_magia.py) ----------
# vão à mesa dentro da ameaça de qualquer criatura: não dizem "dele", "nele"
TRACOS = {
    'resiste':   f'o corpo guarda contra a magia inteiro (não só {T.GUARDA_ARMADURA:.0%}), e a Firmeza leva o bônus inteiro do corpo'.replace('.', ','),
    'imaterial': f'não tem carne: arma sem encanto e sem bênção conta {TM.IMATERIAL} categoria abaixo (o golpe vale um terço); o feitiço e a peça encantada contam inteiros; não vai ao chão nem é agarrado',
    'amaldiçoa': 'a ferida que abre põe uma maldição da categoria do corpo, no passo 1: ela anda dia a dia até alguém a quebrar',
    'lança':     'sabe feitiços (a lista vem logo abaixo), com a Mana e a Conjuração do instinto e da categoria do corpo; o corpo é o foco',
    'sem vida':  'não sangra, o veneno não pega e não foge; não cansa, mas não faz a ação a mais; a zero de PV se desfaz',
    'ossos':     f'o golpe de corte e o de ponta valem {TM.OSSOS:.0%}; o de impacto, inteiro: pede maça ou martelo',
    'dreno':     f'recupera em PV {TM.DRENO:.0%} do que o golpe do corpo tira',
    'ardente':   f'quem golpeia de perto leva o fogo de volta ({TM.ardente_fogo(0)} por categoria do corpo, a contar do Comum); a ferida que o corpo abre queima {TM.ARDENTE_RODADAS} rodadas, como a que sangra',
    'noturno':   'o escuro não tira nada do golpe nem do tiro',
}
def frase(t):
    """a frase de um traço, velho (tabelas_bichos.TRACOS) ou novo (TRACOS daqui)"""
    return TB.TRACOS.get(t) or TRACOS[t]

# ---------- OS POVOS: o corpo de quem veste peças ----------
# base: os atributos de nascença · pts: como os pontos do nível se repartem · couro: a pele que vale como armadura onde a peça não cobre (None: a pele de gente)
_PTS = dict(Força=.30, Agilidade=.20, Vigor=.25, Vontade=.10, Percepção=.10, Afinidade=.05)
POVOS = {
    'goblin':        dict(tamanho='pequeno', tracos=['noturno'], coragem=-4, couro=None,
                          base=dict(Força=45, Agilidade=60, Vigor=30, Vontade=35, Percepção=60, Afinidade=30), pts=dict(Força=.15, Agilidade=.35, Vigor=.20, Vontade=.05, Percepção=.20, Afinidade=.05)),      # miúdo, frágil e desajeitado: vale pelo número
    'orc':           dict(tamanho='médio', tracos=['noturno'], coragem=2, couro=None, base=dict(Força=85, Agilidade=50, Vigor=75, Vontade=45, Percepção=45, Afinidade=25), pts=_PTS),
    'ogro':          dict(tamanho='grande', tracos=[], coragem=2, couro='pelo', base=dict(Força=110, Agilidade=40, Vigor=90, Vontade=40, Percepção=40, Afinidade=20), pts=_PTS),
    'homem-lagarto': dict(tamanho='médio', tracos=[], coragem=0, couro='escama', base=dict(Força=70, Agilidade=65, Vigor=70, Vontade=45, Percepção=60, Afinidade=30), pts=_PTS),
    'gigante':       dict(tamanho='enorme', tracos=[], coragem=4, couro='pelo', base=dict(Força=150, Agilidade=35, Vigor=110, Vontade=60, Percepção=50, Afinidade=20), pts=_PTS),
    'esqueleto':     dict(tamanho='médio', tracos=['sem vida', 'ossos', 'noturno'], coragem=0, couro=None, base=dict(Força=60, Agilidade=55, Vigor=50, Vontade=10, Percepção=40, Afinidade=10), pts=_PTS),
    'cova':          dict(tamanho='médio', tracos=['sem vida', 'noturno'], coragem=0, couro=None, base=dict(Força=80, Agilidade=55, Vigor=70, Vontade=80, Percepção=50, Afinidade=20), pts=_PTS),
}

# ---------- OS POSTOS: o que cada um do povo veste e empunha ----------
# arma, arma2: (família, degraus acima da categoria do bando) · armadura: (material, com elmo?) ou None · escudo · linha: 'trás' (atira de trás da linha) · mais: o que muda na pessoa
def _posto(nome, arma, armadura=None, escudo=False, arma2=None, linha=None, **mais):
    return dict(nome=nome, arma=arma, arma2=arma2, armadura=armadura, escudo=escudo, linha=linha, mais=mais)

# ---------- AS ESPÉCIES (o que se conta no ermo: lugar.bichos e lugar.teto; o gravador lê os nomes) ----------
# Os campos são os do tabelas_bichos (nome, artigo, cat, grau, nivel, instinto, atributos, armas, couro, tamanho, tracos, coragem, moral, bando, despojo, nucleo, chefe, alfa,
# habitat, sabe), mais: plural · fera (só a fera atende ao "chamar" do druida) · feiticos (de quem tem o traço "lança") · fases · armas_diz (o que a mesa lê do corpo, quando
# a arma do corpo da tabela dos bichos não tem o nome certo: o golem bate com o punho, que a luta roda como a cauda, 1d10 de impacto. O tabelas_bichos.ARMAS_CORPO não ganha
# arma nova: o estresse.py sorteia dela, e a linha dele tem de seguir igual à da base).
# O POVO tem ainda: povo (o corpo, em POVOS) · postos (o que cada um veste) · bando_postos (como o bando se reparte) · lider (o posto de quem manda: caído ele, o bando testa a coragem)
def _corpo(nome, artigo, cat, grau, nivel, instinto, atributos, armas, couro, tamanho, tracos, coragem, bando, despojo, habitat, sabe, plural=None, fera=False, chefe=False, alfa=False, **mais):
    """uma criatura de CORPO (a ficha de bicho: bichos.bicho). atributos: (Força, Agilidade, Vigor, Vontade, Percepção, Afinidade)"""
    e = TB._esp(nome, artigo, cat, grau, nivel, instinto, atributos, armas, couro, tamanho, tracos, coragem, bando, despojo, habitat, sabe, chefe=chefe, alfa=alfa)
    e.update(plural=plural or nome + 's', fera=fera, feiticos=list(mais.pop('feiticos', [])), fases=list(mais.pop('fases', [])), **mais)
    return e


def _povo(nome, artigo, povo, cat, grau, nivel, maestria, postos, bando_postos, bando, despojo, habitat, sabe, plural=None, lider=None, chefe=False, toca_postos=None):
    """uma espécie de POVO (a ficha de gente: criaturas.criatura). postos: {posto: _posto(...)}; bando_postos: [(posto, fração)] o bando que anda no ermo (o primeiro leva o que sobra);
    toca_postos: como se reparte quem fica na toca (sem dizer, o mesmo do bando)"""
    P = POVOS[povo]
    at = {k: P['base'][k] + int(nivel * P['pts'][k]) for k in T.ATRIBUTOS}
    armas = list(dict.fromkeys(p['arma'][0] for p in postos.values()))
    return dict(nome=nome, artigo=artigo, plural=plural or nome + 's', cat=cat, grau=grau, nivel=nivel, instinto=maestria, atributos=at, armas=armas, couro=P['couro'],
                tamanho=P['tamanho'], tracos=list(P['tracos']), coragem=P['coragem'], moral='testa', bando=tuple(bando), despojo=dict(despojo), nucleo=False, chefe=chefe,
                alfa=bool(lider), habitat=list(habitat), sabe=sabe, fera=False, feiticos=[], fases=[], povo=povo, postos=postos, bando_postos=list(bando_postos), lider=lider,
                toca_postos=list(toca_postos or bando_postos))


ESPECIES = {
    # ===== OS POVOS (gente com corpo de monstro: veste arma, armadura e escudo de verdade) =====
    'goblin': _povo('goblin', 'o', 'goblin', 0, 'F', 8, 0,
                    dict(faca=_posto('goblin', ('adaga', 0), ('couro', False)),
                         lanceiro=_posto('goblin lanceiro', ('lança', 0), ('couro', False), True),
                         arqueiro=_posto('goblin arqueiro', ('arco', 0), ('couro', False), arma2=('adaga', 0), linha='trás'),
                         capataz=_posto('o capataz goblin', ('lança', 0), ('couro', True), True, linha='trás', nivel=14, maestria=2),
                         guarda=_posto('goblin da guarda', ('lança', 0), ('couro', True), True, nivel=14, maestria=2)),
                    [('faca', 1.0)], (2, 4), {'metal:0': 1, 'couro:0': 1}, ['caverna', 'ruína', 'floresta'],
                    'pequeno, covarde e nunca sozinho: dois cabem onde cabe um homem. Mora em toca, rouba de noite e vê no escuro; caído o capataz, o bando racha', lider='capataz',
                    toca_postos=[('faca', 0.5), ('lanceiro', 0.25), ('arqueiro', 0.25)]),
    'orc':    _povo('orc', 'o', 'orc', 1, 'D', 15, 0,
                    dict(soldado=_posto('orc', ('machado', 0), ('couro', False), True),
                         bruto=_posto('orc bruto', ('malho', 0), ('couro', False)),
                         capitao=_posto('o capitão orc', ('machado', 0), ('malha', True), True, nivel=25, maestria=4)),
                    [('soldado', 0.75), ('bruto', 0.25)], (2, 4), {'metal:1': 1, 'couro:1': 1}, ['serra', 'caverna', 'ruína', 'campo'],
                    'forte e mal treinado: vale pelo que veste e pelo número. Vê no escuro, e o malho do bruto amassa a placa', lider='capitao'),
    'ogro':   _povo('ogro', 'o', 'ogro', 2, 'C', 45, 4, dict(ogro=_posto('ogro', ('malho', 0), ('couro', False))), [('ogro', 1.0)], (1, 2),
                    {'comida': 4, 'couro:2': 2, 'osso:2': 2}, ['serra', 'caverna', 'brejo'],
                    'o tronco que ele empunha alcança antes da espada; o couro grosso cobre o que a peça não cobre'),
    'homem-lagarto': _povo('homem-lagarto', 'o', 'homem-lagarto', 1, 'D', 20, 2, dict(lanceiro=_posto('homem-lagarto', ('lança', 0), None, True)), [('lanceiro', 1.0)], (2, 3),
                           {'couro:1': 2, 'osso:1': 1}, ['brejo'], 'a escama é a armadura dele, e a água não o atrapalha; de lança e escudo, segura um vau', plural='homens-lagarto'),
    'gigante': _povo('gigante', 'o', 'gigante', 3, 'B', 100, 6, dict(gigante=_posto('gigante', ('malho', 0), ('couro', False))), [('gigante', 1.0)], (1, 1),
                     {'comida': 12, 'couro:2': 8, 'osso:2': 6}, ['serra'], 'oito batem nele de uma vez, mas o tronco que ele empunha pega a três casas, antes de qualquer lança'),
    # ===== OS MORTOS QUE ANDAM =====
    'esqueleto': _povo('esqueleto', 'o', 'esqueleto', 0, 'E', 10, 2, dict(soldado=_posto('esqueleto', ('espada', 0), None, True)), [('soldado', 1.0)], (2, 4),
                       {'osso:0': 1, 'metal:0': 1}, ['ruína', 'caverna'], 'a ponta e o fio passam entre os ossos: pede maça. Não foge, não cansa, não sangra'),
    'cavaleiro-da-cova': _povo('cavaleiro da cova', 'o', 'cova', 3, 'B', 90, 6, dict(cavaleiro=_posto('cavaleiro da cova', ('montante', 0), ('placa', True))), [('cavaleiro', 1.0)], (1, 1),
                               {'metal:2': 3, 'osso:2': 1}, ['ruína'], 'um mestre de armas que não cansa, dentro de placa velha; guarda quem o ergueu', plural='cavaleiros da cova'),
    'corpo-seco': _corpo('corpo-seco', 'o', 0, 'E', 8, 0, (70, 30, 80, 10, 30, 10), ['garra'], 'pelo', 'médio', ['sem vida', 'agarra', 'noturno'], 0, (1, 3),
                         {'osso:0': 1}, ['ruína', 'brejo', 'caverna'], 'é lento e não sente: não foge, não sangra, e quem ele agarra não recua', plural='corpos-secos'),
    'carniçal':   _corpo('carniçal', 'o', 1, 'D', 22, 2, (65, 75, 50, 30, 65, 15), ['garra', 'presa'], 'pelo', 'médio', ['sem vida', 'veneno', 'matilha', 'noturno'], 0, (2, 4),
                         {'osso:1': 1, 'peçonha:1': 1}, ['ruína', 'caverna'], 'come os mortos e caça em roda; a unha deixa a podridão, que segue trabalhando', plural='carniçais'),
    'múmia':      _corpo('múmia', 'a', 2, 'C', 50, 4, (95, 40, 100, 80, 50, 50), ['garra'], 'pelo', 'médio', ['sem vida', 'agarra', 'apavora', 'amaldiçoa'], 0, (1, 1),
                         {'pano': 3, 'osso:2': 1}, ['ruína'], 'guarda o que foi enterrado com ela; quem ela fere leva a maldição da cova para casa',
                         maldicao=dict(nome='a maldição da cova', tipo='míngua', condicao=dict(tipo='devolver', o_que='o que se tirou da cova'))),
    # ===== OS SERES DE MAGIA =====
    'fogo-fátuo': _corpo('fogo-fátuo', 'o', 1, 'D', 18, 2, (20, 85, 30, 50, 70, 70), ['ferrão'], 'pelo', 'pequeno', ['voa', 'imaterial', 'lança'], -2, (1, 3),
                         {}, ['brejo', 'ruína'], 'a luz que chama para o fundo do brejo; de longe lança a seta, e o aço comum mal a toca', plural='fogos-fátuos', feiticos=['seta']),
    'alma-penada': _corpo('alma penada', 'a', 1, 'D', 20, 2, (30, 70, 40, 60, 60, 60), ['garra'], 'pelo', 'médio', ['sem vida', 'imaterial', 'apavora'], 0, (1, 2),
                          {}, ['ruína', 'brejo'], 'o aço comum passa por ela quase sem ferir: pede bênção, encanto ou feitiço', plural='almas penadas'),
    'espectro':   _corpo('espectro', 'o', 2, 'C', 55, 6, (40, 85, 85, 80, 70, 80), ['garra'], 'pelo', 'médio', ['sem vida', 'imaterial', 'dreno', 'amaldiçoa'], 0, (1, 1),
                         {}, ['ruína'], 'bebe a vida de quem toca, e o aço comum mal o fere; sem bênção, encanto ou feitiço, o certo é sair',
                         maldicao=dict(nome='o frio do espectro', tipo='insônia', condicao=dict(tipo='matar', especie='espectro'))),
    'golem-de-barro': _corpo('golem de barro', 'o', 1, 'D', 30, 2, (100, 30, 100, 10, 30, 10), ['cauda'], 'escama', 'médio', ['sem vida', 'resiste'], 0, (1, 2),
                             {'metal:0': 2}, ['ruína', 'caverna'], 'guarda o que lhe mandaram guardar e não sai do posto; não cansa, não recua, e a magia escorre nele', plural='golens de barro',
                             armas_diz='punho de barro'),
    'gárgula':    _corpo('gárgula', 'a', 2, 'C', 40, 2, (80, 65, 70, 40, 70, 30), ['garra', 'chifre'], 'carapaça', 'médio', ['voa', 'bote'], 2, (1, 2),
                         {'osso:2': 1, 'metal:1': 2}, ['ruína', 'serra'], 'parece pedra até cair em cima de quem passa; no ar a espada mal a toca, e a casca pede maça'),
    'elemental-do-fogo': _corpo('elemental do fogo', 'o', 2, 'C', 60, 6, (100, 85, 100, 50, 60, 70), ['garra'], 'pelo', 'médio', ['sem vida', 'ardente', 'resiste'], 0, (1, 1),
                                {'carvão': 6}, ['caverna', 'ruína', 'serra'], 'quem bate de perto se queima: pede lança, arco, ou feitiço', plural='elementais do fogo'),
    # ===== AS FERAS QUE FALTAM =====
    'harpia':     _corpo('harpia', 'a', 1, 'D', 22, 2, (50, 85, 40, 40, 75, 25), ['garra'], 'pelo', 'médio', ['voa'], -2, (2, 4),
                         {'comida': 1, 'couro:1': 1, 'osso:1': 1}, ['serra', 'ruína'], 'vêm de cima, em bando, e somem para o alto; no ar a espada mal as toca', fera=True),
    'lobisomem':  _corpo('lobisomem', 'o', 2, 'C', 55, 6, (100, 90, 90, 50, 85, 30), ['garra', 'presa'], 'pelo', 'médio', ['regenera', 'amaldiçoa', 'noturno'], 4, (1, 1),
                         {'couro:2': 2, 'osso:2': 1}, ['floresta', 'campo'], 'a carne fecha, vê no escuro, e a mordida deixa a maldição da lua: quem é mordido não dorme e definha',
                         fera=True, maldicao=dict(nome='a maldição da lua', tipo='insônia', condicao=dict(tipo='matar', especie='lobisomem'))),
    # ===== OS CHEFES DE CORPO (os outros chefes são gente ou povo: CHEFES, abaixo) =====
    'vampiro':    _corpo('senhor vampiro', 'o', 3, 'B', 100, 6, (120, 90, 100, 90, 80, 70), ['garra', 'presa'], 'pelo', 'médio', ['dreno', 'regenera', 'apavora', 'noturno', 'lança'], 0, (1, 1),
                         {}, ['ruína'], 'bebe a vida, a carne fecha, e o olhar dele gela a coragem; de dia, sem a noite, é menos', plural='senhores vampiros', chefe=True,
                         feiticos=['medo', 'sangria'], fases=[dict(abaixo=0.3, diz='a sede o toma: cada ferida que ele abre amaldiçoa', ganha=['amaldiçoa'], mana=4)],
                         maldicao=dict(nome='a sede', tipo='míngua', condicao=dict(tipo='matar', especie='vampiro'))),
}
FERA_TB = True              # as feras do tabelas_bichos (as 14 de antes) atendem ao "chamar" do druida; das criaturas, só as marcadas "fera"

# ---------- OS CHEFES MÁGICOS (gente ou povo, com feitiços, fases e lacaios) ----------
# quem é (povo e posto, ou gente de um molde), o nível, a mão, a categoria do que veste, os feitiços, a tradição, o foco e o amuleto, as fases, e os lacaios
# lacaios: [(espécie, posto ou None, quantos, o que muda)]; guarda: quantos dos primeiros lacaios põem o corpo na frente do chefe
CHEFES = {
    'xamã goblin': dict(nome='o xamã goblin', povo='goblin', posto='faca', cat=1, grau='D', nivel=22, maestria=2, atributos=dict(Vontade=70, Afinidade=75),
                        tradicao='pacto', feiticos=['mau-olhado', 'medo', 'sangria'], foco=('talismã', 1), amuleto=1, arma=('adaga', 1), escudo=False, linha='trás', moral='testa',
                        fases=[dict(abaixo=0.5, diz='uiva, e a toca inteira uiva com ele', brado=True, mana=3)],
                        lacaios=[('goblin', 'guarda', 2, {}), ('goblin', 'capataz', 1, {}), ('goblin', 'faca', 4, {}), ('goblin', 'lanceiro', 2, {}), ('goblin', 'arqueiro', 2, {})], guarda=2,
                        sabe='o xamã da toca: amaldiçoa de longe, gela a coragem e bebe o sangue de quem fere; dois de lança põem o corpo na frente dele, e ele foge quando a coisa aperta'),
    'senhor da guerra': dict(nome='o senhor da guerra orc', povo='orc', posto='capitao', cat=2, grau='C', nivel=60, maestria=6, atributos=dict(Vontade=70),
                             arma=('machado', 0), escudo=True, armadura=('malha', True), moral='firme',
                             encanto=dict(feitico='medo', grau=2), fases=[dict(abaixo=0.5, diz='entra em fúria e urra: os orcs urram com ele', brado=True)],
                             lacaios=[('orc', 'soldado', 2, dict(cat=2, nome='orc da guarda')), ('orc', 'soldado', 4, {}), ('orc', 'bruto', 2, {})], guarda=0,
                             sabe='um orc mestre de armas com um machado Raro que ruge quando ele quer (o encanto do medo, uma vez por luta); ferido, urra, e os orcs dele ganham coragem'),
    'necromante': dict(nome='o necromante', molde='bruxa', cat=3, grau='B', nivel=85, maestria={'pacto': 6, 'adaga': 2}, atributos=dict(Vontade=100, Afinidade=100, Vigor=70),
                       tradicao='pacto', feiticos=['sangria', 'nó', 'medo'], foco=('talismã', 3), amuleto=3, arma=('adaga', 3), armadura=('couro', False), linha='trás', moral='firme',      # sem o mau-olhado: com o mau-olhado de −4 (o da bruxa, M13) ele vencia 76% (meta C5: 30 a 70)
                       fases=[dict(abaixo=0.7, diz='ergue os mortos do chão', ergue=3, mana=6), dict(abaixo=0.35, diz='chama de novo os que caíram', ergue=3, mana=6)],
                       lacaios=[('cavaleiro-da-cova', None, 1, {}), ('esqueleto', None, 6, dict(cat=2, nivel=50, maestria=4))], guarda=1,
                       sabe='frágil, atrás dos mortos; ergue quem cai, dos dois lados, e bebe a vida de longe. Morto ele, os mortos não se erguem mais'),
    'bruxa do brejo': dict(nome='a bruxa do brejo', molde='bruxa', cat=2, grau='C', nivel=55, maestria={'pacto': 4, 'adaga': 2}, atributos=dict(Vontade=95, Afinidade=95, Vigor=70, Agilidade=70),
                           tradicao='pacto', feiticos=['mau-olhado', 'medo', 'sangria', 'nó'], foco=('talismã', 2), amuleto=2, arma=('adaga', 2), armadura=('couro', False), linha='trás', moral='firme',
                           fases=[dict(abaixo=0.4, diz='larga a pele de velha: a faca dela passa a amaldiçoar', ganha=['amaldiçoa'], mana=6)],
                           lacaios=[('trasgo', None, 1, {}), ('fogo-fátuo', None, 3, dict(cat=2)), ('corpo-seco', None, 2, dict(cat=2, nome='afogado'))], guarda=0,      # dois afogados (eram três): com o mau-olhado de −4 ela vencia 71% (meta C5: 30 a 70); com dois, 54%
                           sabe='amaldiçoa, gela a coragem, bebe o sangue e ata a magia de quem lança; o trasgo dela não cai depressa, e os afogados não sentem dor',
                           maldicao=dict(nome='a praga do brejo', tipo='chaga', condicao=dict(tipo='perdao'))),
    'vampiro': dict(especie='vampiro', linha='trás', lacaios=[('carniçal', None, 3, {}), ('lobo', None, 3, {})], guarda=0,
                    sabe='bebe a vida, a carne fecha, o olhar gela a coragem; os carniçais e os lobos vêm primeiro'),
    # etapa 4b (a masmorra): o chefe do fundo da cripta. É o cavaleiro da cova na categoria da cripta (Comum), de montante e placa velha, nível 25, mão de Treinado.
    # Medido (projeto A, m3): contra Maro, Tomé e Rute de PV cheio, perde 98% das lutas numa sala aberta e mata alguém da casa em 8%; sozinho com o Maro, o Maro morre em 64%
    'guardião da cripta': dict(nome='o guardião da cripta', povo='cavaleiro-da-cova', posto='cavaleiro', cat=0, grau='E', nivel=25, maestria=4, arma=('montante', 0), escudo=False,
                               fases=[dict(abaixo=0.5, diz='bate o pé no chão de pedra: os ossos da sala se levantam', ergue=2, brado=True)],
                               lacaios=[('esqueleto', None, 2, {})], guarda=0,
                               sabe='um cavaleiro morto, de montante e placa velha, que guarda a cripta e não cansa; ferido, bate o pé, e os ossos da sala se levantam com ele'),
}

# ---------- O BANDO NO ERMO (a patrulha) e A TOCA (o covil inteiro) ----------
# quem está na toca: o chefe (se o covil tem), a guarda dele, o líder do povo, e o resto pelo bando_postos da espécie
# ---------- O COVIL: a toca de um povo, contada ao lado da fauna (as cabeças SÃO a contagem da espécie no ermo: lugar.bichos.ESPECIE) ----------
# O registro do covil mora no lugar (lugar.covil): {"especie", "nome", "teto", "lider" (o líder de pé?), "chefe" (o chefe que mora ali, ou None), "fome", "ult_roubo",
#   "sem_lider" (dias sem líder), "cheio" (dias seguidos com a toca cheia), "fora" (dias até chegar um bando de fora, com a toca vazia), "desde"}
# O TESOURO da toca é o estoque do ermo (a prata e a comida que o bando juntou), contado como toda prata: o covil não guarda prata.
COVIS = {
    'goblin': dict(nome='a toca dos goblins', come=0.3, presa={'corça': 6, 'javali': 6, 'ratazana': 1}, cria=0.025, teto=16, rouba_cada=7, rouba_chance=20, rouba_comida=2,
                   rouba_prata=0.25, prata_dado=6, definha=9, lider_dias=7, chefe='xamã goblin', chefe_desde=12, chefe_dias=30, vem_de_fora=120, novo_bando=6, cabecas=9, tesouro=20),
    'orc':    dict(nome='o acampamento orc', come=0.6, presa={'corça': 6, 'javali': 6}, cria=0.015, teto=12, rouba_cada=10, rouba_chance=12, rouba_comida=3,
                   rouba_prata=0.4, prata_dado=12, definha=9, lider_dias=10, chefe='senhor da guerra', chefe_desde=10, chefe_dias=60, vem_de_fora=240, novo_bando=4, cabecas=6, tesouro=60),
}
# os mortos não comem, não roubam e não criam: a toca deles (a cova) só guarda; o chefe que ergue (o necromante) ergue um a cada tantos dias, até o teto
COVA_ERGUE = 10
RASTRO_TOCA = 2             # achar a toca é isto mais difícil que achar o rastro de base (a toca se esconde; o bando, não)
TOCA_ESCURA = True          # dentro da toca é escuro (quem luta lá dentro, sem luz, tem o escuro de sempre; o povo noturno, não)
# a toca vista de fora: o que o caçador conta da boca dela, antes de entrar (o número exato é do Mestre)
TOCA_CONTA = [(4, 'poucos'), (8, 'um bando'), (12, 'muitos'), (99, 'uma toca cheia')]

# ---------- O DESPOJO ----------
# a peça do povo é gasta e malfeita: morto o dono, é sucata (a matéria do despojo da espécie: o ferro da lâmina, o couro da armadura). O despojo segue a regra do
# tabelas_bichos (de metade ao inteiro de cada bem). A prata é a que o bando juntou (o estoque do ermo): quem fica com o campo NA TOCA leva o tesouro inteiro.
PECONHA_ATE = 2             # a peçonha do bicho de veneno vai até a Rara (é matéria: tabelas_mundo.MATERIAS)
RENDIDO_SAI = True          # quem se rende a quem fica com o campo sai da contagem (vai preso ou é rematado: a casa decide a cena), e o despojo dele é o de um morto

# ---------- a caça: a índole (a ousadia e a chance de investir) e o teto de cada criatura num ermo ----------
INDOLE = {'goblin': (0.8, 0.5), 'orc': (1.0, 0.8), 'ogro': (0.8, 0.8), 'homem-lagarto': (0.6, 0.5), 'gigante': (0.6, 0.6), 'esqueleto': (0.6, 1.0), 'cavaleiro-da-cova': (0.4, 1.0),
          'corpo-seco': (0.5, 1.0), 'carniçal': (1.0, 0.9), 'múmia': (0.3, 1.0), 'fogo-fátuo': (0.8, 0.6), 'alma-penada': (0.6, 0.8), 'espectro': (0.6, 1.0), 'golem-de-barro': (0.2, 1.0),
          'gárgula': (0.6, 0.8), 'elemental-do-fogo': (0.4, 0.8), 'harpia': (1.0, 0.7), 'lobisomem': (1.0, 0.9), 'vampiro': (0.6, 0.9)}

# ---------- a régua (as provas): o homem do degrau, por categoria (o mesmo do provas.py) ----------
REF = {0: 10, 1: 30, 2: 50, 3: 90, 4: 120, 5: 150}
