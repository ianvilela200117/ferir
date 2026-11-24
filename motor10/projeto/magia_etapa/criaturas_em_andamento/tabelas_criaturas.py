"""tabelas_criaturas.py — RASCUNHO da parte J (versão do projeto final): os números das criaturas novas.

É a página que o construtor levaria para o motor (tabelas_criaturas.py, irmã do tabelas_bichos.py). Aqui ela ENXERTA na memória as tabelas do
tabelas_bichos (traços, armas do corpo, espécies), sem tocar em arquivo nenhum do motor10.
Os GANCHOS (Conjuração, Firmeza, Mana, guarda) seguem a conta da magia de projeto/magia_etapa/conta/PROJETO.md, parte B.
"""
import os
import tabelas as T
import tabelas_bichos as TB

# ---------- os traços novos (entram na lista fechada; cada um tem a sua prova, J6) ----------
OSSOS = 0.5                             # o corte e a ponta valem isto em quem é só osso (o impacto vale inteiro)
PEDE_PRATA = int(os.environ.get('J_IMATERIAL', 1))      # o aço comum conta tantas categorias abaixo em quem "pede prata" e em quem é imaterial
DRENO = 0.5                             # a fração do que o golpe tirou que volta em PV para quem drena
def ardente(cat): return T.devolve_max(cat)      # o que leva quem golpeia de perto o corpo que arde (o teto do "devolve" da categoria)
ATIRA_PADRAO = dict(nome='espinho', dado='1d6', golpe='ponta', alcance=6, folego=1)
MAU_OLHADO = dict(acerto=-2, defesa=-2) # o mau-olhado da conta da magia (B.5), enquanto a luta dura
BRADO = dict(acerto=2, coragem=4, rodadas=3)     # o "benzido" da conta (B.5), com prazo: é grito, não bênção
# ---------- os GANCHOS da conta da magia (B.1 a B.5): as mesmas fórmulas, para o monstro que lança ----------
MANA_VOLTA = 1
GUARDA_ARMADURA = 0.6                   # sem amuleto, a armadura do tronco (e o couro do bicho) guarda contra a magia esta fração do valor
FIRMEZA_BASE = 22; CALEJO = 4
CONCENTRA = 28; CONCENTRA_FERIDA = 4
def mana_max(afin, vont, maestria): return (afin + vont) // 10 + maestria
def conj(maestria, atributo, foco): return maestria + (atributo // 10) / 2 + T.BON[foco]
def firmeza(vont, maestria, amuleto=None, armadura=None, inteiro=False):
    return FIRMEZA_BASE + (vont // 10) / 2 + maestria / 2 + (T.BON[amuleto] if amuleto is not None else (T.BON[armadura] / (1 if inteiro else 2)) if armadura is not None else 0)

_n = TB._n
TRACOS_NOVOS = {
    'sem vida':   'não sangra, o veneno não pega e não testa a coragem; não cansa (o fôlego não gasta), mas não faz a ação a mais; a zero de PV está desfeito (não fica caído)',
    'ossos':      f'o golpe de corte e o de ponta valem {OSSOS:.0%}; o de impacto vale inteiro',
    'pede prata': f'arma que não é de prata, benta nem encantada conta {PEDE_PRATA} categoria(s) abaixo; o feitiço conta inteiro',
    'imaterial':  'pede prata, e não tem corpo: atravessa a linha, não é derrubado nem agarrado, e não leva golpe livre; o toque não se apara e não olha o material da armadura',
    'dreno':      f'recupera em PV {DRENO:.0%} do que o golpe do corpo tira',
    'ardente':    'quem golpeia de perto (a 1 casa) leva o fogo de volta (4 por degrau da categoria); a ferida que o corpo abre queima por cinco rodadas, como a que sangra',
    'atira':      'tem um tiro do corpo (espinho, pedra): atira em quem está a 2 casas ou mais; com inimigo ao alcance do corpo, bate de perto',
    'noturno':    'o escuro não tira nada do golpe nem do tiro',
    # os três da conta da magia (B.8): aqui só o nome e a frase; quem os roda é o magia.py
    'resiste':    'o corpo guarda contra a magia inteiro, e a Firmeza leva o bônus inteiro do corpo',
    'lança':      'sabe um feitiço da lista, com Mana e Conjuração pelo instinto e pela categoria do corpo',
    'amaldiçoa':  'a ferida que abre põe uma maldição da categoria do corpo, no passo 1',
}
TB.TRACOS.update(TRACOS_NOVOS)

# ---------- o corpo: as armas que faltam ----------
TB.ARMAS_CORPO.update({
    'toque': dict(dado='1d6',  golpe='toque',   folego=1),      # o toque de quem não tem corpo: não se apara e não olha o material
    'chama': dict(dado='1d8',  golpe='fogo',    folego=1),      # o corpo que arde: olha a categoria da armadura, não o material
    'punho': dict(dado='1d8',  golpe='impacto', folego=1),      # o punho de barro, de pedra, de ferro
})
T.MATRIZ['fogo'] = dict(couro=1.0, malha=1.0, placa=1.0)
CRUS = ('toque',)                                               # os golpes que não se aparam e não olham o material

_esp = TB._esp
def _mais(e, **mais): e['mais'] = mais; return e

# ---------- as criaturas novas de CORPO (a ficha é a do capítulo 6) ----------
# atributos: (Força, Agilidade, Vigor, Vontade, Percepção, Afinidade)
CORPOS = {
    # --- os mortos que andam ---
    'corpo-seco': _esp('corpo-seco', 'o', 0, 'E', 8, 0, (70, 30, 80, 10, 30, 10), ['garra'], 'pelo', 'médio', ['sem vida', 'agarra', 'noturno'], 0, (2, 5),
                       {'osso:0': 1}, ['ruína', 'brejo', 'caverna'], 'é lento e não sente: não foge, não sangra, e quem ele agarra não recua'),
    'carniçal':   _esp('carniçal', 'o', 1, 'D', 22, 2, (65, 75, 50, 30, 65, 15), ['garra', 'presa'], 'pelo', 'médio', ['sem vida', 'veneno', 'matilha', 'noturno'], 0, (2, 4),
                       {'osso:1': 1, 'glândula:1': 1}, ['ruína', 'caverna'], 'come os mortos e caça em roda; a unha deixa a podridão, que segue trabalhando'),
    'múmia':      _esp('múmia', 'a', 2, 'C', 50, 4, (95, 40, 100, 80, 50, 50), ['punho'], 'pelo', 'médio', ['sem vida', 'agarra', 'apavora', 'amaldiçoa'], 0, (1, 1),
                       {'pano': 3, 'osso:2': 1}, ['ruína'], 'guarda o que foi enterrado com ela; quem ela fere leva a maldição da cova para casa'),
    # --- os seres de magia ---
    'fogo-fátuo': _mais(_esp('fogo-fátuo', 'o', 1, 'D', 18, 2, (20, 85, 30, 50, 70, 70), ['toque'], 'pelo', 'pequeno', ['voa', 'imaterial', 'lança'], -2, (1, 3),
                             {}, ['brejo', 'ruína'], 'a luz que chama para o fundo do brejo; de longe lança a seta, e o aço comum mal a toca'),
                        artes=[dict(nome='seta', tipo='ataque', dado='1d8', alcance=8, mana=2)]),
    'alma':       _esp('alma penada', 'a', 1, 'D', 20, 2, (30, 70, 40, 60, 60, 60), ['toque'], 'pelo', 'médio', ['sem vida', 'imaterial', 'apavora'], 0, (1, 2),
                       {}, ['ruína', 'brejo'], 'o aço comum passa por ela quase sem ferir: pede prata, bênção ou encanto'),
    'espectro':   _esp('espectro', 'o', 2, 'C', 55, 6, (40, 85, 85, 80, 70, 80), ['toque'], 'pelo', 'médio', ['sem vida', 'imaterial', 'dreno', 'amaldiçoa'], 0, (1, 1),
                       {}, ['ruína'], 'bebe a vida de quem toca, e o aço comum mal o fere; sem prata, bênção ou encanto, só resta sair'),
    'barro':      _esp('golem de barro', 'o', 1, 'D', 30, 2, (100, 30, 100, 10, 30, 10), ['punho'], 'escama', 'médio', ['sem vida', 'resiste'], 0, (1, 2),
                       {'metal:0': 2}, ['ruína', 'caverna'], 'guarda o que lhe mandaram guardar e não sai do posto; não cansa e não recua'),
    'gárgula':    _esp('gárgula', 'a', 2, 'C', 40, 2, (80, 65, 70, 40, 70, 30), ['garra', 'chifre'], 'carapaça', 'médio', ['voa', 'bote'], 2, (1, 2),
                       {'osso:2': 1, 'metal:1': 2}, ['ruína', 'serra'], 'parece pedra até cair em cima de quem passa; no ar a espada mal a toca, e a casca pede maça'),
    'fogo':       _esp('elemental do fogo', 'o', 2, 'C', 60, 6, (100, 85, 100, 50, 60, 70), ['chama'], 'pelo', 'médio', ['sem vida', 'ardente'], 0, (1, 2),
                       {'carvão': 6}, ['caverna', 'ruína', 'serra'], 'quem bate de perto se queima: pede lança, arco, ou água'),
    'pedra':      _esp('elemental da pedra', 'o', 3, 'B', 90, 4, (130, 30, 120, 60, 40, 60), ['punho'], 'carapaça', 'grande', ['sem vida', 'couraça', 'investida'], 0, (1, 1),
                       {'metal:2': 3}, ['caverna', 'serra'], 'rola como pedra solta e não tem fresta: pede malho, e arma Épica'),
    'ferro':      _esp('golem de ferro', 'o', 3, 'B', 100, 4, (150, 30, 130, 10, 40, 10), ['punho'], 'carapaça', 'grande', ['sem vida', 'couraça', 'agarra', 'resiste'], 0, (1, 1),
                       {'metal:2': 6}, ['ruína'], 'não tem fresta, não cansa, e a magia escorre nele; quem ele segura não sai'),
    # --- as feras mágicas que faltam ---
    'harpia':     _esp('harpia', 'a', 1, 'D', 22, 2, (50, 85, 40, 40, 75, 25), ['garra'], 'pelo', 'médio', ['voa'], -2, (2, 4),
                       {'comida': 1, 'couro:1': 1, 'osso:1': 1}, ['serra', 'ruína'], 'vêm de cima, em bando, e somem para o alto; no ar a espada mal as toca'),
    'lobisomem':  _esp('lobisomem', 'o', 2, 'C', 55, 6, (100, 90, 90, 50, 85, 30), ['garra', 'presa'], 'pelo', 'médio', ['regenera', 'pede prata', 'amaldiçoa'], 4, (1, 1),
                       {'couro:2': 2, 'osso:2': 1}, ['floresta', 'campo'], 'a carne fecha, e o aço comum fere pouco: sem prata, quase ninguém o mata; a mordida deixa a maldição da lua'),
    'mantícora':  _mais(_esp('mantícora', 'a', 2, 'C', 50, 4, (95, 70, 85, 50, 80, 30), ['garra', 'presa'], 'pelo', 'grande', ['atira', 'veneno'], 2, (1, 1),
                             {'comida': 6, 'couro:2': 3, 'osso:2': 2, 'glândula:2': 1}, ['serra', 'campo', 'ruína'], 'atira os espinhos da cauda enquanto você chega, e os espinhos têm veneno'),
                        tiro=dict(nome='espinho', dado='1d6', golpe='ponta', alcance=6, folego=1)),
    'quimera':    _esp('quimera', 'a', 3, 'B', 95, 6, (120, 70, 130, 60, 75, 40), ['garra', 'presa', 'chifre'], 'escama', 'grande', ['sopro', 'investida'], 4, (1, 1),
                       {'comida': 8, 'couro:2': 4, 'osso:2': 3}, ['serra', 'ruína'], 'três cabeças: uma sopra fogo, uma morde, uma dá a cabeçada de quem vem correndo'),
    'boitatá':    _esp('boitatá', 'o', 3, 'B', 95, 4, (100, 80, 100, 70, 80, 60), ['presa', 'cauda'], 'escama', 'grande', ['ardente', 'sopro', 'apavora'], 2, (1, 1),
                       {'couro:2': 5, 'carvão': 8}, ['campo', 'brejo', 'floresta'], 'a cobra de fogo guarda o campo: quem não queima o mato ela costuma deixar passar'),
    'mapinguari': _esp('mapinguari', 'o', 3, 'B', 100, 6, (140, 40, 130, 60, 60, 20), ['garra', 'bocarra'], 'pelo', 'grande', ['couraça', 'agarra', 'apavora'], 4, (1, 1),
                       {'comida': 10, 'couro:2': 6, 'osso:2': 4}, ['floresta'], 'o couro não tem fresta e o fedor tira a coragem; a boca fica na barriga, e é para lá que ele puxa'),
    # --- um chefe de corpo (os outros chefes são gente ou povo: chefes.py) ---
    'vampiro':    _esp('senhor vampiro', 'o', 3, 'B', 100, 6, (120, 90, 100, 90, 80, 70), ['garra', 'presa'], 'pelo', 'médio', ['dreno', 'regenera', 'apavora', 'noturno', 'pede prata'], 0, (1, 1),
                       {}, ['ruína'], 'bebe a vida, a carne fecha, e o aço comum fere pouco; de dia, sem a noite, é outro', chefe=True),
}
TB.ESPECIES.update(CORPOS)

# ---------- OS POVOS: gente com corpo de monstro. A ficha é a de gente (pessoas.ficha): veste arma, armadura e escudo de verdade ----------
# base: os atributos de nascença · pts: como os pontos do nível se repartem · couro: a pele que vale como armadura onde a peça não cobre
_pts = dict(Força=.30, Agilidade=.20, Vigor=.25, Vontade=.10, Percepção=.10, Afinidade=.05)
POVOS = {
    'goblin':    dict(artigo='o', tamanho='pequeno', tracos=['noturno'], coragem=-4, base=dict(Força=45, Agilidade=70, Vigor=45, Vontade=35, Percepção=60, Afinidade=30),
                      pts=dict(Força=.15, Agilidade=.35, Vigor=.20, Vontade=.05, Percepção=.20, Afinidade=.05)),
    'orc':       dict(artigo='o', tamanho='médio', tracos=['noturno'], coragem=2, base=dict(Força=85, Agilidade=55, Vigor=75, Vontade=50, Percepção=45, Afinidade=25), pts=_pts),
    'ogro':      dict(artigo='o', tamanho='grande', tracos=[], coragem=2, base=dict(Força=110, Agilidade=40, Vigor=90, Vontade=40, Percepção=40, Afinidade=20), pts=_pts),
    'lagarto':   dict(artigo='o', tamanho='médio', tracos=[], coragem=0, couro='escama', base=dict(Força=70, Agilidade=65, Vigor=70, Vontade=45, Percepção=60, Afinidade=30), pts=_pts),
    'minotauro': dict(artigo='o', tamanho='grande', tracos=['investida'], coragem=6, couro='pelo', base=dict(Força=110, Agilidade=55, Vigor=85, Vontade=50, Percepção=60, Afinidade=20), pts=_pts),
    'gigante':   dict(artigo='o', tamanho='enorme', tracos=[], coragem=4, couro='pelo', base=dict(Força=150, Agilidade=35, Vigor=110, Vontade=60, Percepção=50, Afinidade=20), pts=_pts),
    'esqueleto': dict(artigo='o', tamanho='médio', tracos=['sem vida', 'ossos', 'noturno'], coragem=0, base=dict(Força=60, Agilidade=55, Vigor=50, Vontade=10, Percepção=40, Afinidade=10), pts=_pts),
    'cova':      dict(artigo='o', tamanho='médio', tracos=['sem vida', 'noturno'], coragem=0, base=dict(Força=80, Agilidade=55, Vigor=70, Vontade=80, Percepção=50, Afinidade=20), pts=_pts),
}
# a linha de cada criatura de povo: o povo, o nível, a mão (a maestria), a categoria do conjunto (é ela que dá o grau), e o que veste e empunha
# arma, arma2: (família, degraus acima do conjunto) · armadura: (material, com elmo?) ou None · escudo: True/False
def _tropa(nome, povo, cat, grau, nivel, mao, arma, armadura=None, escudo=False, arma2=None, bando=(1, 1), despojo=None, habitat=(), sabe='', lider=False):
    return dict(nome=nome, povo=povo, cat=cat, grau=grau, nivel=nivel, maestria=mao, arma=arma, arma2=arma2, armadura=armadura, escudo=escudo, bando=bando, despojo=dict(despojo or {}),
                habitat=list(habitat), sabe=sabe, lider=lider, chefe=False)
TROPA = {
    'goblin':          _tropa('goblin', 'goblin', 0, 'F', 8, 0, ('adaga', 0), ('couro', False), False, bando=(2, 4), despojo={'metal:0': 1, 'couro:0': 1}, habitat=['caverna', 'ruína', 'floresta'],
                              sabe='pequeno, covarde e nunca sozinho: dois cabem onde cabe um homem. É o que sai da toca para roubar e espiar'),
    'goblin lanceiro': _tropa('goblin lanceiro', 'goblin', 0, 'F', 8, 0, ('lança', 0), ('couro', False), True, bando=(2, 6), despojo={'metal:0': 1, 'couro:0': 1}, habitat=['caverna', 'ruína', 'floresta'],
                              sabe='a linha da toca: a lança alcança antes da espada, e bate por cima do ombro do da frente; a lança pesa na mão dele'),
    'goblin arqueiro': _tropa('goblin arqueiro', 'goblin', 0, 'F', 8, 0, ('arco', 0), ('couro', False), False, arma2=('adaga', 0), bando=(2, 4), despojo={'madeira:0': 1, 'couro:0': 1}, habitat=['caverna', 'ruína', 'floresta'],
                              sabe='atira de trás da linha e corre de quem chega'),
    'orc':             _tropa('orc', 'orc', 1, 'D', 25, 2, ('machado', 0), ('malha', True), True, bando=(3, 5), despojo={'metal:1': 1, 'couro:1': 1}, habitat=['serra', 'caverna', 'ruína', 'campo'],
                              sabe='é um soldado: escudo, malha e machado. Vale o que veste, e não corre à toa'),
    'orc bruto':       _tropa('orc bruto', 'orc', 1, 'D', 30, 2, ('malho', 0), ('malha', True), False, bando=(1, 2), despojo={'metal:1': 2, 'couro:1': 1}, habitat=['serra', 'caverna', 'ruína', 'campo'],
                              sabe='o malho de duas mãos amassa a placa; sem escudo, apanha mais'),
    'lagarto':         _tropa('homem-lagarto', 'lagarto', 1, 'D', 25, 2, ('lança', 0), None, True, bando=(2, 4), despojo={'couro:1': 2, 'osso:1': 1}, habitat=['brejo'],
                              sabe='a escama é a armadura dele e a água não o atrapalha; de lança, segura um vau'),
    'ogro':            _tropa('ogro', 'ogro', 2, 'C', 50, 4, ('malho', 0), ('couro', False), False, bando=(1, 2), despojo={'comida': 4, 'couro:2': 2, 'osso:2': 2}, habitat=['serra', 'caverna', 'brejo'],
                              sabe='o tronco que ele empunha alcança antes da espada; de braço aberto, larga-o, e aí é só um corpo grande'),
    'minotauro':       _tropa('minotauro', 'minotauro', 2, 'C', 50, 4, ('montante', 0), None, False, bando=(1, 1), despojo={'couro:2': 3, 'osso:2': 2}, habitat=['ruína', 'caverna'],
                              sabe='vem correndo de cabeça baixa: quem o espera num corredor sem espaço para a carga luta com um homem grande, e só'),
    'gigante':         _tropa('gigante', 'gigante', 3, 'B', 100, 4, ('malho', 0), ('couro', False), False, bando=(1, 2), despojo={'comida': 12, 'couro:2': 8, 'osso:2': 6}, habitat=['serra'],
                              sabe='oito batem nele de uma vez; o tronco que ele empunha pega a três casas, antes de qualquer lança'),
    'esqueleto':       _tropa('esqueleto', 'esqueleto', 0, 'E', 10, 0, ('espada', 0), None, True, bando=(3, 6), despojo={'osso:0': 1, 'metal:0': 1}, habitat=['ruína', 'caverna'],
                              sabe='a ponta e o fio passam entre os ossos: pede maça. Não foge, não cansa, não sangra'),
    'cova':            _tropa('cavaleiro da cova', 'cova', 3, 'B', 90, 6, ('montante', 0), ('placa', True), False, bando=(1, 2), despojo={'metal:2': 3, 'osso:2': 1}, habitat=['ruína'],
                              sabe='um mestre de armas que não cansa, dentro de placa velha; guarda quem o ergueu'),
}
TOSCA_DUR = 1.0                         # a peça da tropa é o atalho de gente miúda que a luta já tem: vale a categoria e não existe no Livro (1.0: a mesma durabilidade de uma peça nova)
REF = {0: 10, 1: 30, 2: 50, 3: 90, 4: 120, 5: 150}      # o nível do homem do degrau, por categoria (o do banco: provas.py)
