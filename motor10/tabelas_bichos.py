"""tabelas_bichos.py — MOTOR 10: TODOS os números dos bichos num lugar só (o tamanho, o corpo, os traços, a moral, as espécies).

Um bicho é uma ficha de luta como qualquer outra, e a regra de ouro vale igual: o corpo dele é a ARMA (dente, presa, garra,
ferrão, casco, chifre, cauda, bocarra) e a ARMADURA (pelo, escama, carapaça), com CATEGORIA. O que conta é a diferença entre a arma de quem
bate e a armadura de quem apanha. Os números da luta e dos itens moram no tabelas.py; aqui só o que é do bicho.
Mudar um bicho é mudar esta página e rodar `python3 provas.py` (o bloco OS BICHOS).

O CORPO NÃO É PEÇA: não está no Livro de Itens, não tem dono, não quebra, não ocupa sintonia. O despojo sai da tabela.
"""
import tabelas as T

# ---------- o grau (o que o caçador lê) casa com a categoria do corpo ----------
# F é o Comum que foge ou que só incomoda; E, o Comum que fere; daí para cima, um grau por categoria.
# O grau fala de UM bicho contra um homem do mesmo degrau (o conjunto da categoria do bicho); o bando pesa mais, e a ameaça avisa.
GRAUS = ['F', 'E', 'D', 'C', 'B', 'A', 'S']
GRAU_DA_CAT = {0: ('F', 'E'), 1: ('D',), 2: ('C',), 3: ('B',), 4: ('A',), 5: ('S',)}
GRAU_DIZ = dict(F='presa: sozinha quase nunca derruba um homem armado, mas o golpe de sorte abre ferida', E='perigo de morte para quem está sozinho com peças Comuns',
                D='perigo de morte para um homem armado, mesmo com peças Incomuns', C='mata um veterano', B='pede um grupo', A='pede um grupo de mestres', S='calamidade')
# O BANDO PESA MAIS QUE O GRAU DE UM SÓ: para quem está sozinho, N juntos valem tantos graus acima (medido na régua do capítulo 6: duas corças derrubam o caçador
# de começo uma vez em quatro; seis ratazanas vencem-no em seis de dez; quatro lobos vencem o homem de conjunto Incomum em oito de dez)
BANDO_GRAU = [(4, 2), (2, 1)]      # com 4 ou mais, dois graus acima; com 2 ou 3, um grau acima
def grau_do_bando(grau, n):
    sobe = next((s for q, s in BANDO_GRAU if n >= q), 0)
    return GRAUS[min(len(GRAUS) - 1, GRAUS.index(grau) + sobe)]

# ---------- o tamanho ----------
# pv: vezes o PV · alcance: casas que o corpo alcança · cerco: quantos batem nele de perto na mesma rodada, e quantos mais de haste
# ocupa: quantas vagas ele toma de um corredor (gente toma 1) · defesa: o pequeno é difícil de acertar; o enorme, fácil
TAMANHOS = {
    'pequeno': dict(pv=0.6, alcance=1, cerco=(2, 1), ocupa=0.5, defesa=2),
    'médio':   dict(pv=1.0, alcance=1, cerco=(4, 2), ocupa=1,   defesa=0),
    'grande':  dict(pv=1.5, alcance=2, cerco=(6, 3), ocupa=2,   defesa=-2),
    'enorme':  dict(pv=2.5, alcance=3, cerco=(8, 4), ocupa=3,   defesa=-4),
}
APERTADO = -2               # bicho maior que o corredor luta apertado: isto no acerto e na Defesa por vaga que falta

# ---------- o corpo: a arma ----------
# dado · golpe (corte, ponta, impacto: entra na matriz do golpe contra o material, como qualquer arma) · fôlego por golpe
# o valor e o bônus de acerto saem da CATEGORIA do corpo (tabelas.MULT e tabelas.BON); o alcance, do tamanho
ARMAS_CORPO = {
    'dente':   dict(dado='1d4',  golpe='ponta',   folego=1),     # a dentada do bicho miúdo; o dente fino da cobra
    'presa':   dict(dado='1d6',  golpe='ponta',   folego=1),     # a mordida do lobo, a presa do javali, o bico
    'garra':   dict(dado='1d8',  golpe='corte',   folego=1),
    'ferrão':  dict(dado='1d6',  golpe='ponta',   folego=1),
    'casco':   dict(dado='1d4',  golpe='impacto', folego=1),     # o coice
    'chifre':  dict(dado='1d10', golpe='ponta',   folego=2),
    'cauda':   dict(dado='1d10', golpe='impacto', folego=2),
    'bocarra': dict(dado='1d12', golpe='ponta',   folego=2),     # a boca do bicho enorme
}
# ---------- o corpo: a armadura ----------
# cada couro vale como um material de armadura (a proteção, a Defesa, a iniciativa e a linha da matriz do golpe são as dele),
# sem pedir Força e sem custar fôlego. Cobre o corpo todo, a cabeça também.
COUROS = {'pelo': 'couro', 'escama': 'malha', 'carapaça': 'placa'}

# ---------- os traços (lista FECHADA: só entra o que a luta roda, e cada um tem a sua prova no provas.py) ----------
MATILHA = 1                 # quantos outros da matilha têm de já ter batido no alvo nesta rodada para o golpe que fere derrubar
MATILHA_CORAGEM = 4         # o que o bicho de matilha soma na coragem enquanto houver outro da matilha de pé
BOTE = dict(ini=20, acerto=8, dados=3, atordoa=1)   # a iniciativa a mais na primeira rodada; o acerto do primeiro golpe; quantas vezes os dados; ações que perde quem o bote derruba
INVESTIDA = dict(casas=2, acerto=8, dados=3)        # quanto tem de correr desde o último golpe; o acerto da carga; quantas vezes os dados
VENENO = dict(fracao=0.5, rodadas=4, acerto=-2)     # a fração do golpe que a vítima perde por rodada; por quantas rodadas; a pena de quem está envenenado
AGARRADO = dict(acerto=-4, defesa=-4)               # a pena de quem está agarrado: não tem espaço para a arma, e está tão exposto quanto quem está no chão
VOA = -6                    # arma de alcance 1 contra o bicho no ar
REGENERA = 0.15             # a fração do PV máximo que volta a cada turno do bicho
PAVOR = 28                  # o teste de coragem de quem começa a luta contra o que apavora
SOPRO = dict(dado='1d8', alcance=4, recarga=2, folego=3, forca=1.2)     # o sopro não se apara; a força dele é fixa, como a da besta
# o bote, a investida e a matilha não derrubam quem é maior que o bicho; o que agarra não agarra quem é maior que ele, nem quem não está colado nele (um de cada vez)
PEDE_TAMANHO = ('matilha', 'bote', 'investida', 'agarra')      # os traços que derrubam ou agarram: no bicho pequeno não pegam gente (a ameaça avisa)
_n = lambda x: f'{x:+d}'.replace('-', '−')
# as frases dos traços vão à mesa dentro da ameaça de qualquer espécie ("a pantera", "o urso"): não dizem "dele", "nele", "contra ele"
TRACOS = {
    'matilha':   f'o golpe que fere um alvo em que outro da matilha já bateu nesta rodada o derruba; com outro da matilha de pé, {_n(MATILHA_CORAGEM)} na coragem',
    'bote':      f"na primeira rodada age antes de todos; o primeiro golpe tem {_n(BOTE['acerto'])} e rola os dados {BOTE['dados']} vezes; quem esse golpe ferir vai ao chão e perde {BOTE['atordoa']} ação",
    'investida': f"se correu {INVESTIDA['casas']} casas ou mais desde o último golpe, o golpe tem {_n(INVESTIDA['acerto'])}, rola os dados {INVESTIDA['dados']} vezes e derruba quem ferir",
    'veneno':    f"o golpe que fere envenena: por {VENENO['rodadas']} rodadas a vítima perde por rodada {VENENO['fracao']:.0%} do golpe e tem {_n(VENENO['acerto'])} no acerto; não acumula: vale a pior mordida, e o prazo recomeça",
    'agarra':    f"o golpe que fere quem está colado no bicho agarra: o agarrado não anda, não recua, não troca de lugar e tem {_n(AGARRADO['acerto'])} no acerto e {_n(AGARRADO['defesa'])} na Defesa, até o bicho passar um turno sem feri-lo",
    'voa':       f'arma de alcance 1 tem {_n(VOA)} contra quem voa; a linha não segura quem voa; não leva golpe livre ao se afastar; num corredor, ou no chão, não voa',
    'regenera':  f'no começo de cada turno, recupera {REGENERA:.0%} do PV máximo',
    'apavora':   f'quando a luta começa, quem não é de ferro testa a coragem contra {PAVOR}',
    'couraça':   'não tem fresta: ninguém mira a fresta, e o crítico não corta a proteção pela metade',
    'sopro':     f"a cada {SOPRO['recarga']} rodadas sopra em todos os inimigos a até {SOPRO['alcance']} casas: um ataque em cada um, com a categoria do corpo, que não se apara; o tempo e a cobertura valem como num tiro",
}

# ---------- a moral do bicho ----------
# o bicho não se rende nem fica abalado: luta ou foge. Testa 2d20 + Vontade ÷ 10 + a coragem da espécie (e o que vale para todos:
# +2 com o alfa de pé, +2 se o bando é maior, −4 se o outro lado tem o dobro) contra o susto. Falhou, foge.
MORAL = dict(ferido=26)     # o susto que só o bicho tem: levou uma FERIDA. Os outros são os de toda a gente (tabelas.MORAL): abaixo de um quarto do PV, o golpe terrível num do bando, metade do bando caída, o alfa caído
ENCURRALADO = 2             # sem saída o bicho não foge: luta até o fim, com isto no acerto
# o chefe não testa (moral "firme")

# ---------- dizer ----------
PARTES_BICHO = dict(braços='patas da frente', pernas='patas de trás')      # o que a mesa lê quando o golpe cai nos "braços" ou nas "pernas" de um bicho (a regra é a mesma: tabelas.ONDE)
import re as _re
_CONTRAI = {('em', 'a'): 'na', ('em', 'o'): 'no', ('em', 'as'): 'nas', ('em', 'os'): 'nos', ('de', 'a'): 'da', ('de', 'o'): 'do', ('de', 'as'): 'das', ('de', 'os'): 'dos',
            ('por', 'a'): 'pela', ('por', 'o'): 'pelo', ('por', 'as'): 'pelas', ('por', 'os'): 'pelos'}
_CONTRAI_RE = _re.compile(r'\b([Ee]m|[Dd]e|[Pp]or) (as|os|a|o) (?=[a-zà-ú])')
def contrai(txt):
    """o nome do bicho sozinho leva o artigo ("a corça", "o javali"): "em a corça" vira "na corça", "de o javali" vira "do javali", "por o lobo" vira "pelo lobo"."""
    def f(m):
        c = _CONTRAI[(m.group(1).lower(), m.group(2).lower())]
        return (c.capitalize() if m.group(1)[0].isupper() else c) + ' '
    return _CONTRAI_RE.sub(f, txt)

# ---------- o despojo ----------
DESPOJO_MIN = 0.5           # a luta estraga: de cada bem sai desta fração (arredondada para cima) até o inteiro da tabela


def _esp(nome, artigo, cat, grau, nivel, instinto, atributos, armas, couro, tamanho, tracos, coragem, bando, despojo, habitat, sabe, chefe=False, alfa=False):
    """uma espécie. atributos: (Força, Agilidade, Vigor, Vontade, Percepção, Afinidade)"""
    return dict(nome=nome, artigo=artigo, cat=cat, grau=grau, nivel=nivel, instinto=instinto, atributos=dict(zip(T.ATRIBUTOS, atributos)), armas=list(armas), couro=couro,
                tamanho=tamanho, tracos=list(tracos), coragem=coragem, moral='firme' if chefe else 'testa', bando=tuple(bando), despojo=dict(despojo), nucleo=bool(chefe),
                chefe=bool(chefe), alfa=bool(alfa), habitat=list(habitat), sabe=sabe)


# ---------- as espécies ----------
# instinto: a maestria do bicho (0, 2, 4, 6 ou 8: vale como a maestria da pessoa, no acerto, na Defesa e nas ações a mais)
# coragem: o que a espécie soma no teste de moral · bando: (de quantos, a quantos) andam juntos · alfa: o primeiro do bando é o líder
# despojo: o que o bicho inteiro rende (a matéria tem categoria: "couro:1"; a comum vai até o Raro; o bicho de veneno dá PEÇONHA, da categoria dele até a Rara) · chefe: não foge e dá NÚCLEO da categoria dele
ESPECIES = {
    'corça':     _esp('corça', 'a', 0, 'F', 4, 0, (45, 70, 45, 30, 70, 20), ['casco'], 'pelo', 'médio', [], -6, (1, 2),
                      {'comida': 6, 'couro:0': 2, 'osso:0': 1}, ['floresta', 'campo'], 'foge ao primeiro sangue, mas até lá escoiceia'),
    'ratazana':  _esp('ratazana', 'a', 0, 'F', 3, 0, (35, 70, 35, 30, 55, 20), ['dente'], 'pelo', 'pequeno', ['matilha'], -2, (3, 6),
                      {'comida': 1, 'couro:0': 1}, ['brejo', 'ruína', 'caverna'], 'sozinha não é nada; em bando perdem o medo, e cabem duas onde cabe um homem'),
    'javali':    _esp('javali', 'o', 0, 'E', 10, 0, (70, 50, 100, 50, 45, 20), ['presa'], 'pelo', 'médio', ['investida'], 4, (1, 1),
                      {'comida': 6, 'couro:0': 2, 'osso:0': 2}, ['floresta', 'brejo'], 'vem de longe em linha reta e derruba; colado, sem espaço para correr, é só um porco bravo'),
    'lobo':      _esp('lobo', 'o', 1, 'D', 20, 2, (60, 75, 40, 40, 70, 20), ['presa'], 'pelo', 'médio', ['matilha'], 0, (3, 5),
                      {'comida': 3, 'couro:1': 2, 'osso:1': 1}, ['floresta', 'serra', 'campo'], 'caça em roda; num corredor só um morde de cada vez; caído o alfa, o bando racha', alfa=True),
    'surucucu':  _esp('surucucu', 'a', 1, 'D', 25, 2, (60, 90, 60, 40, 70, 20), ['dente'], 'escama', 'médio', ['bote', 'veneno'], 2, (1, 1),
                      {'comida': 2, 'couro:1': 2, 'osso:1': 1, 'peçonha:1': 1}, ['brejo', 'floresta', 'ruína'], 'o primeiro bote é o pior; o veneno segue trabalhando depois da mordida'),
    'urso':      _esp('urso', 'o', 1, 'D', 35, 4, (100, 50, 80, 50, 50, 20), ['garra', 'presa'], 'pelo', 'grande', ['agarra'], 2, (1, 1),
                      {'comida': 10, 'couro:1': 4, 'osso:1': 2}, ['floresta', 'serra', 'caverna'], 'quem ele abraça não recua; a pata alcança antes da espada, e só a lança o segura fora do abraço'),
    'pantera':   _esp('pantera', 'a', 2, 'C', 50, 6, (100, 95, 100, 50, 80, 20), ['garra', 'presa'], 'pelo', 'médio', ['bote'], 4, (1, 1),
                      {'comida': 4, 'couro:2': 2, 'osso:2': 1}, ['floresta', 'serra'], 'escolhe a hora: o primeiro golpe é dela, e derruba'),
    'aranha':    _esp('aranha-de-toca', 'a', 2, 'C', 45, 2, (50, 80, 40, 40, 60, 20), ['ferrão'], 'carapaça', 'médio', ['veneno'], 2, (2, 3),
                      {'couro:2': 1, 'osso:2': 1, 'peçonha:2': 1}, ['caverna', 'ruína', 'floresta'], 'a casca pede maça ou martelo; o veneno segue trabalhando depois da mordida'),
    'grifo':     _esp('grifo', 'o', 2, 'C', 55, 6, (95, 85, 85, 55, 90, 20), ['garra', 'presa'], 'pelo', 'grande', ['voa'], 2, (1, 2),
                      {'comida': 6, 'couro:2': 2, 'osso:2': 2}, ['serra'], 'no ar a espada mal o toca: pede lança, arco, ou um teto baixo'),
    'trasgo':    _esp('trasgo', 'o', 2, 'C', 55, 2, (80, 45, 105, 50, 40, 20), ['garra'], 'pelo', 'grande', ['regenera'], 2, (1, 1),
                      {'couro:2': 3, 'osso:2': 3}, ['brejo', 'caverna', 'ruína'], 'a carne dele fecha: ou cai depressa, ou não cai'),
    'basilisco': _esp('basilisco', 'o', 3, 'B', 90, 6, (100, 65, 100, 60, 60, 30), ['presa', 'cauda'], 'escama', 'grande', ['couraça', 'veneno'], 4, (1, 1),
                      {'couro:2': 5, 'osso:2': 4, 'peçonha:2': 2}, ['ruína', 'caverna', 'brejo'], 'não tem fresta: arma abaixo do Épico não o fere de verdade'),
    'serpe':     _esp('serpe', 'a', 3, 'B', 100, 4, (85, 60, 75, 70, 70, 30), ['bocarra', 'cauda'], 'escama', 'enorme', ['sopro', 'veneno'], 0, (1, 1),
                      {'comida': 12, 'couro:2': 6, 'osso:2': 5, 'peçonha:2': 2}, ['serra', 'ruína'], 'o sopro pega o grupo inteiro, e a cauda envenena; quatro de aço Raro raramente voltam', chefe=True),
    'hidra':     _esp('hidra', 'a', 4, 'A', 150, 6, (120, 55, 110, 80, 70, 40), ['bocarra'], 'escama', 'enorme', ['regenera', 'veneno', 'apavora'], 0, (1, 1),
                      {'couro:2': 8, 'osso:2': 6, 'peçonha:2': 3}, ['brejo', 'ruína'], 'o que não morre depressa volta inteiro', chefe=True),
    'dragão':    _esp('dragão', 'o', 5, 'S', 220, 8, (180, 70, 240, 100, 90, 60), ['garra', 'bocarra', 'cauda'], 'escama', 'enorme', ['voa', 'sopro', 'couraça', 'apavora'], 0, (1, 1),
                      {'couro:2': 12, 'osso:2': 10}, ['serra', 'ruína'], 'voa, sopra, não tem fresta. Só aço Lendário o fere de verdade', chefe=True),
}
