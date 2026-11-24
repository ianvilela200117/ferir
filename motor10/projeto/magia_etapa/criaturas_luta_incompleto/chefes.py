"""chefes.py — RASCUNHO da parte J: os chefes mágicos e os bandos. Cada função devolve o lado B pronto para a luta."""
import random
from itens import item
import tabelas as T
import bichos
import criaturas as CR
from pessoas import padrao, veste


def goblins(lanceiros=4, arqueiros=2, capataz=True):
    """o bando de goblins: a linha de lança e escudo, os arqueiros atrás; o primeiro é o capataz (caído ele, o bando testa a coragem)"""
    def faz():
        L = [CR.povo('goblin', nome=f'goblin {i + 1}') for i in range(lanceiros)] + [CR.povo('goblin arqueiro', nome=f'goblin arqueiro {i + 1}', linha='trás') for i in range(arqueiros)]
        if capataz and L: L[0]['nome'] = 'o capataz goblin'; L[0]['lider'] = True
        return L
    return faz


def orcs(n=4, brutos=0, arqueiros=0, capitao=True):
    def faz():
        L = [CR.povo('orc', nome=f'orc {i + 1}') for i in range(n)] + [CR.povo('orc bruto', nome=f'orc bruto {i + 1}') for i in range(brutos)] + [CR.povo('goblin arqueiro', nome=f'goblin arqueiro {i + 1}', linha='trás') for i in range(arqueiros)]
        if capitao and L: L[0]['nome'] = 'o capitão orc'; L[0]['lider'] = True
        return L
    return faz


def xama(guardas=2, lanceiros=4, arqueiros=2, artes=True):
    """O XAMÃ GOBLIN (Incomum, grau D): frágil, atrás da linha, com dois guardas que põem o corpo na frente"""
    def faz():
        x = CR.povo('goblin', nome='o xamã', cat=1, nivel=22, maestria=2, lider=True, linha='trás', moral='firme', chefe=True, foco=1, atributos=dict(Vontade=70, Afinidade=75),
                    arma=CR._tosca(item('arma', 1, 'cajado de osso', familia='adaga')), escudo=None)
        x['equip']['escudo'] = None
        if artes:
            x['artes'] = [dict(nome='fúria da toca', tipo='brado', quando='comeco', usos=1, mana=4),
                          dict(nome='os da toca', tipo='invoca', que='goblin', n=3, quando='sempre', alcance=99, usos=1, fase=1, mana=4, atras=1),
                          dict(nome='praga', tipo='maldiz', alcance=6, recarga=2, mana=3),
                          dict(nome='faísca verde', tipo='ataque', dado='1d8', alcance=6, recarga=0, mana=2, deixa='queima')]
            x['fases'] = [dict(abaixo=0.5, diz='grita pelos da toca')]
        return [x] + [CR.povo('goblin', nome=f'guarda do xamã {i + 1}', nivel=14, maestria=2, guarda='o xamã', linha='trás') for i in range(guardas)] + \
               [CR.povo('goblin', nome=f'goblin {i + 1}') for i in range(lanceiros)] + [CR.povo('goblin arqueiro', nome=f'goblin arqueiro {i + 1}', linha='trás') for i in range(arqueiros)]
    return faz


def senhor(orcs_=4, brutos=2, arqueiros=2, arma=2, artes=True, sozinho=False):
    """O SENHOR DA GUERRA ORC (grau C): um orc mestre de armas com um machado RARO do Livro de Itens, no meio de orcs de conjunto Incomum"""
    def faz():
        machado = item('arma', arma, 'o Racha-Escudo', familia='machado', efeitos=[dict(chave='sangra')])
        s = CR.povo('orc', nome='o senhor da guerra', nivel=60, maestria=6, lider=True, moral='firme', chefe=True, arma=machado, escudo=item('escudo', 2), atributos=dict(Vontade=70))
        if artes:
            s['artes'] = [dict(nome='brado de guerra', tipo='brado', quando='comeco', usos=1), dict(nome='urro', tipo='grito', cd=26, alcance=4, usos=1, fase=1)]
            s['fases'] = [dict(abaixo=0.5, diz='entra em fúria', acerto=4, defesa=-2, brado=True)]
        if sozinho: return [s]
        return [s] + [CR.povo('orc', nome=f'orc {i + 1}') for i in range(orcs_)] + [CR.povo('orc bruto', nome=f'orc bruto {i + 1}') for i in range(brutos)] + \
               [CR.povo('goblin arqueiro', nome=f'goblin arqueiro {i + 1}', linha='trás') for i in range(arqueiros)]
    return faz


def _gente(nome, nivel, mao, cat, at, arma='adaga', **mais):
    p = veste(padrao(nome, nivel, molde='comum', maestria=mao, atributos=at, **mais), arma=CR._tosca(item('arma', cat, familia=arma)), armadura=CR._tosca(item('armadura', cat, material='couro')))
    return p


def bruxa(trasgo=1, diabretes=2, secos=3, artes=True):
    """A BRUXA DO BREJO (Rara, grau C): amaldiçoa, prende no lodo, solta a peste; abaixo de 40% larga a pele de velha"""
    def faz():
        b = _gente('a bruxa do brejo', 55, 4, 2, dict(Vontade=95, Afinidade=95, Vigor=70, Agilidade=70), lider=True, linha='trás', moral='firme', chefe=True, foco=2)
        if artes:
            b['artes'] = [dict(nome='guincho', tipo='grito', cd=28, alcance=6, usos=1, fase=1),
                          dict(nome='lodo que prende', tipo='prende', area=True, alcance=6, rodadas=2, recarga=3, mana=4, quando='dois'),
                          dict(nome='nuvem de peste', tipo='ataque', area=True, dado='1d6', alcance=4, deixa='veneno', recarga=3, mana=5, quando='dois'),
                          dict(nome='mau-olhado', tipo='maldiz', alcance=8, recarga=1, mana=3),
                          dict(nome='seta de espinho', tipo='ataque', dado='1d8', alcance=8, recarga=0, mana=2)]
            b['fases'] = [dict(abaixo=0.4, diz='larga a pele de velha', ganha=['regenera'], acerto=4, cura=0.2)]
        return [b] + [bichos.bicho('trasgo', nome=f'o trasgo da bruxa {i + 1}', moral='firme') for i in range(trasgo)] + [bichos.bicho('diabrete', nome=f'diabrete {i + 1}') for i in range(diabretes)] + \
               [bichos.bicho('corpo-seco', nome=f'afogado {i + 1}', cat=1) for i in range(secos)]
    return faz


def necromante(esqueletos=6, cavaleiros=1, artes=True):
    """O NECROMANTE (Épico, grau B): frágil, atrás dos mortos. Ergue quem cai, dos dois lados. Morto ele, os mortos se desfazem."""
    def faz():
        n = _gente('o necromante', 85, 4, 3, dict(Vontade=100, Afinidade=100, Vigor=70), lider=True, linha='trás', moral='firme', chefe=True, foco=3, desfaz='todos')
        if artes:
            n['artes'] = [dict(nome='pavor', tipo='grito', cd=28, alcance=5, usos=1),
                          dict(nome='beber um dos seus', tipo='bebe', pv=0.3, recarga=2, fase=1, quando='ferido', mana=2),
                          dict(nome='o chamado dos mortos', tipo='levanta', prepara=True, quando='caidos', pelo_menos=2, recarga=3, mana=8, que='esqueleto', alcance=99),
                          dict(nome='seta de sombra', tipo='ataque', dado='1d10', alcance=8, recarga=0, mana=2, deixa='dreno')]
            n['fases'] = [dict(abaixo=0.5, diz='bebe a força dos próprios mortos')]
        return [n] + [CR.povo('cova', nome=f'cavaleiro da cova {i + 1}', guarda='o necromante', linha='trás') for i in range(cavaleiros)] + \
               [CR.povo('esqueleto', nome=f'esqueleto {i + 1}', cat=2, nivel=50, maestria=4) for i in range(esqueletos)]
    return faz


def rei_morto(cavaleiros=2, esqueletos=4, artes=True):
    """O REI MORTO (Único, grau A): espera no trono enquanto a guarda luta; ergue a guarda caída; a espada dele é peça do Livro"""
    def faz():
        espada = item('arma', 4, 'a Espada do Rei Sem Nome', familia='espada', efeitos=[dict(chave='sangra'), dict(chave='critico_19')])
        r = CR.povo('cova', nome='o rei morto', cat=4, nivel=130, maestria=8, lider=True, linha='trás', moral='firme', chefe=True, foco=4, fica=3, arma=espada, escudo=item('escudo', 3), atributos=dict(Vontade=100, Afinidade=80, Vigor=130))
        if artes:
            r['artes'] = [dict(nome='olhar da cova', tipo='grito', cd=30, alcance=6, usos=1),
                          dict(nome='erguer a guarda', tipo='levanta', so_seus=True, prepara=True, quando='caidos', pelo_menos=2, recarga=4, mana=8, pv=0.5, alcance=99),
                          dict(nome='ordem do rei', tipo='brado', quando='meus', recarga=4, mana=3, alcance=99)]
            r['fases'] = [dict(abaixo=0.6, diz='levanta-se do trono', acerto=2), dict(abaixo=0.25, diz='a coroa arde', acerto=2, cura=0.15, brado=True)]
        return [r] + [CR.povo('cova', nome=f'cavaleiro da cova {i + 1}', guarda='o rei morto', linha='trás') for i in range(cavaleiros)] + \
               [CR.povo('esqueleto', nome=f'guarda morto {i + 1}', cat=3, nivel=90, maestria=6) for i in range(esqueletos)]
    return faz


def dragao_velho(artes=True):
    """O DRAGÃO VELHO (Lendário, grau S): o dragão de hoje com roteiro. No chão; aos 60% levanta voo e chama a chuva de fogo; aos 30% a asa cede e ele desce em fúria."""
    def faz():
        if not artes: return [bichos.bicho('dragão')]
        d = bichos.bicho('dragão', nome='o dragão velho', tracos=['sopro', 'couraça', 'apavora'], chefe=True,
                         artes=[dict(nome='palavra de pavor', tipo='grito', cd=30, alcance=8, usos=1, fase=1),
                                dict(nome='chuva de fogo', tipo='ataque', area=True, dado='1d10', alcance=8, prepara=True, recarga=3, mana=6, deixa='queima', fase=1, ate_fase=1),
                                dict(nome='bater de asas', tipo='ataque', area=True, dado='1d6', alcance=2, deixa='chao', recarga=2, mana=2, quando='dois')],
                         fases=[dict(abaixo=0.6, diz='levanta voo', ganha=['voa']), dict(abaixo=0.3, diz='a asa cede: desce em fúria', perde=['voa'], acerto=4, sopro_recarga=1)])
        return [d]
    return faz


def vampiro(carnicais=3, lobos=3, artes=True):
    """O SENHOR VAMPIRO (Épico, grau B): bebe a vida, a carne fecha, o aço comum fere pouco; prende com o olhar"""
    def faz():
        v = bichos.bicho('vampiro', nome='o senhor vampiro', lider=True, chefe=True, **(dict(
            artes=[dict(nome='o olhar', tipo='prende', alcance=6, rodadas=2, recarga=2, mana=4), dict(nome='véu de sombra', tipo='escuro', rodadas=3, quando='comeco', usos=1, mana=4)],
            fases=[dict(abaixo=0.25, diz='desfaz-se em névoa', ganha=['incorpóreo'], perde=['regenera'])]) if artes else {}))
        return [v] + [bichos.bicho('carniçal', nome=f'carniçal {i + 1}') for i in range(carnicais)] + [bichos.bicho('lobo', nome=f'lobo {i + 1}') for i in range(lobos)]
    return faz
