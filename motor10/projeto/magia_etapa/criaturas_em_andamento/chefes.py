"""chefes.py — RASCUNHO da parte J (versão do projeto final): os chefes mágicos e os bandos. Cada função devolve o lado B pronto para a luta.
Os feitiços são os da lista da conta da magia (B.7), com os números de lá; cada chefe tem, além deles, UMA arte de assinatura que não está na lista."""
import random
from itens import item
import tabelas as T
import bichos
import criaturas as CR
from pessoas import padrao, veste

# ---------- os feitiços da lista (conta da magia, B.7), na forma que o rascunho da luta roda ----------
def FT(qual, **mais):
    d = dict(
        seta=dict(nome='seta', tipo='ataque', dado='1d8', alcance=8, mana=2),
        lanca=dict(nome='lança de fogo', tipo='ataque', dado='2d8', alcance=8, mana=4, acoes=2, deixa='queima'),
        bola=dict(nome='bola de fogo', tipo='ataque', area=True, casa=4, dado='1d8', alcance=8, mana=6, acoes=2, quando='dois'),
        raio=dict(nome='raio', tipo='ataque', dado='2d10', alcance=8, mana=6, prepara=True, deixa='atordoa'),
        prender=dict(nome='prender', tipo='prende', alcance=6, rodadas=2, mana=3, recarga=1),
        espinho=dict(nome='espinho', tipo='ataque', dado='1d6', alcance=6, mana=2, deixa='veneno', fracao=0.25, rodadas_v=3),
        mau_olhado=dict(nome='mau-olhado', tipo='maldiz', alcance=6, mana=2, recarga=1),
        medo=dict(nome='medo', tipo='grito', um=True, contra='F', cd=26, alcance=6, mana=3, recarga=2),
        sangria=dict(nome='sangria', tipo='ataque', dado='1d6', alcance=4, mana=2, deixa='dreno'),
    )[qual]
    d.update(mais); return d


def goblins(lanceiros=4, arqueiros=2, capataz=True, espada=None, facas=0):
    """um bando de goblins dito à mão: os de faca (os que saem da toca), a linha de lança e escudo, os arqueiros atrás; o primeiro é o capataz (caído ele, o bando testa a coragem).
    espada: a categoria da espada do capataz (a peça do Livro que o covil guarda: Incomum no covil de começo)"""
    def faz():
        L = [CR.povo('goblin', nome=f'goblin {i + 1}') for i in range(facas)] + [CR.povo('goblin lanceiro', nome=f'goblin lanceiro {i + 1}') for i in range(lanceiros)] + \
            [CR.povo('goblin arqueiro', nome=f'goblin arqueiro {i + 1}', linha='trás') for i in range(arqueiros)]
        if capataz and L:
            if espada is not None: L[0] = CR.povo('goblin lanceiro', nome='o capataz goblin', nivel=16, maestria=2, arma=item('arma', espada, familia='espada'))
            L[0]['nome'] = 'o capataz goblin'; L[0]['lider'] = True
        return L
    return faz


def patrulha(n=3, arco=0):
    """a patrulha: os goblins de faca que andam na mata (arco: quantos deles são de arco)"""
    return goblins(0, arco, capataz=False, facas=n - arco)


def covil(n=9, capataz=True, espada=None, xama=False, artes=True, toca=0):
    """QUEM ESTÁ NA TOCA, pela contagem: o xamã e 2 guardas de lança (se há xamã), o capataz (com a espada do covil, se ainda a tem); do resto, um quarto de arco, um quarto de lança, e os de faca"""
    def faz():
        L = []; r = n
        if xama and r >= 3: L += [o_xama(artes, toca)] + [CR.povo('goblin lanceiro', nome=f'guarda do xamã {i + 1}', nivel=14, maestria=2, guarda='o xamã', linha='trás') for i in range(2)]; r -= 3
        if capataz and r >= 1:
            cap = CR.povo('goblin lanceiro', nome='o capataz goblin', nivel=16, maestria=2, **(dict(arma=item('arma', espada, familia='espada')) if espada is not None else {}))
            if not L: cap['lider'] = True
            L.append(cap); r -= 1
        arq = r // 4; lan = r // 4
        return L + [CR.povo('goblin', nome=f'goblin {i + 1}') for i in range(r - arq - lan)] + [CR.povo('goblin lanceiro', nome=f'goblin lanceiro {i + 1}') for i in range(lan)] + \
               [CR.povo('goblin arqueiro', nome=f'goblin arqueiro {i + 1}', linha='trás') for i in range(arq)]
    return faz


def orcs(n=4, brutos=0, arqueiros=0, capitao=True):
    def faz():
        L = [CR.povo('orc', nome=f'orc {i + 1}') for i in range(n)] + [CR.povo('orc bruto', nome=f'orc bruto {i + 1}') for i in range(brutos)] + [CR.povo('goblin arqueiro', nome=f'goblin arqueiro {i + 1}', linha='trás') for i in range(arqueiros)]
        if capitao and L: L[0]['nome'] = 'o capitão orc'; L[0]['lider'] = True
        return L
    return faz


def o_xama(artes=True, toca=3, foge=True, **mais):
    """O XAMÃ GOBLIN sozinho (a pessoa): pacto de Iniciante, talismã Incomum, frágil"""
    x = CR.povo('goblin', nome='o xamã', cat=1, nivel=22, maestria=2, lider=True, linha='trás', moral='firme', chefe=True, foco=1, amuleto=1, atributos=dict(Vontade=70, Afinidade=75),
                arma=item('arma', 1, 'faca de osso', familia='adaga'), **mais)
    x['equip']['escudo'] = None
    if artes:
        x['artes'] = [dict(nome='uivo da toca', tipo='brado', quando='comeco', usos=1),
                      FT('medo'), FT('mau_olhado'), FT('sangria')]
        if foge: x['fases'] = [dict(abaixo=0.5, diz='larga o bando e corre para o fundo da toca', foge=True)]
    return x


def xama(n=9, capataz=None, artes=True, toca=0):
    """O XAMÃ GOBLIN (Incomum, grau D) e o covil de n cabeças: atrás da linha, com dois guardas que põem o corpo na frente. capataz: a categoria da espada dele (None: capataz de peças comuns)"""
    return covil(n, True, capataz, True, artes, toca)


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
    return veste(padrao(nome, nivel, molde='comum', maestria=mao, atributos=at, **mais), arma=item('arma', cat, familia=arma), armadura=item('armadura', cat, material='couro'))


def bruxa(trasgo=1, fatuos=3, secos=4, artes=True):
    """A BRUXA DO BREJO (Rara, grau C): pacto de Treinada, talismã Raro. Amaldiçoa, assusta, bebe a vida, prende no lodo; abaixo de 40% larga a pele de velha"""
    def faz():
        b = _gente('a bruxa do brejo', 55, 4, 2, dict(Vontade=95, Afinidade=95, Vigor=70, Agilidade=70), lider=True, linha='trás', moral='firme', chefe=True, foco=2, amuleto=2)
        if artes:
            b['artes'] = [dict(nome='guincho', tipo='grito', cd=28, alcance=6, usos=1, fase=1),
                          dict(nome='lodo que prende', tipo='prende', area=True, alcance=6, rodadas=2, recarga=3, mana=5, acoes=2, quando='dois'),
                          FT('mau_olhado'), FT('medo'), FT('sangria', alcance=6)]
            b['fases'] = [dict(abaixo=0.4, diz='larga a pele de velha', ganha=['regenera'], acerto=4, cura=0.2)]
        return [b] + [bichos.bicho('trasgo', nome=f'o trasgo da bruxa {i + 1}', moral='firme') for i in range(trasgo)] + [bichos.bicho('fogo-fátuo', nome=f'fogo-fátuo {i + 1}', cat=2) for i in range(fatuos)] + \
               [bichos.bicho('corpo-seco', nome=f'afogado {i + 1}', cat=1) for i in range(secos)]
    return faz


def necromante(esqueletos=6, cavaleiros=1, artes=True, cat_esq=2):
    """O NECROMANTE (Épico, grau B): frágil, atrás dos mortos. Ergue quem cai, dos dois lados. Morto ele, os mortos se desfazem."""
    def faz():
        n = _gente('o necromante', 85, 6, 3, dict(Vontade=100, Afinidade=100, Vigor=70), lider=True, linha='trás', moral='firme', chefe=True, foco=3, amuleto=3, desfaz='todos')
        if artes:
            n['artes'] = [dict(nome='pavor', tipo='grito', cd=28, alcance=5, usos=1),
                          dict(nome='beber um dos seus', tipo='bebe', pv=0.3, recarga=2, fase=1, quando='ferido', mana=2),
                          dict(nome='o chamado dos mortos', tipo='levanta', prepara=True, quando='caidos', pelo_menos=2, recarga=3, mana=6, que='esqueleto', alcance=99),
                          FT('mau_olhado'), FT('sangria', nome='seta de sombra', alcance=8)]
            n['fases'] = [dict(abaixo=0.5, diz='bebe a força dos próprios mortos')]
        return [n] + [CR.povo('cova', nome=f'cavaleiro da cova {i + 1}', guarda='o necromante', linha='trás') for i in range(cavaleiros)] + \
               [CR.povo('esqueleto', nome=f'esqueleto {i + 1}', cat=cat_esq, nivel=50, maestria=4) for i in range(esqueletos)]
    return faz


def rei_morto(cavaleiros=2, esqueletos=4, artes=True):
    """O REI MORTO (Único, grau A): espera no trono enquanto a guarda luta; ergue a guarda caída; a espada dele é peça do Livro"""
    def faz():
        espada = item('arma', 4, 'a Espada do Rei Sem Nome', familia='espada', efeitos=[dict(chave='sangra'), dict(chave='critico_19')])
        r = CR.povo('cova', nome='o rei morto', cat=4, nivel=130, maestria=8, lider=True, linha='trás', moral='firme', chefe=True, foco=4, amuleto=4, fica=3, arma=espada, escudo=item('escudo', 3), atributos=dict(Vontade=100, Afinidade=80, Vigor=130))
        if artes:
            r['artes'] = [dict(nome='olhar da cova', tipo='grito', cd=30, alcance=6, usos=1),
                          dict(nome='erguer a guarda', tipo='levanta', so_seus=True, prepara=True, quando='caidos', pelo_menos=2, recarga=4, mana=6, pv=0.5, alcance=99),
                          dict(nome='ordem do rei', tipo='brado', quando='meus', recarga=4, alcance=99)]
            r['fases'] = [dict(abaixo=0.6, diz='levanta-se do trono', acerto=2), dict(abaixo=0.25, diz='a coroa arde', acerto=2, cura=0.15, brado=True)]
        return [r] + [CR.povo('cova', nome=f'cavaleiro da cova {i + 1}', guarda='o rei morto', linha='trás') for i in range(cavaleiros)] + \
               [CR.povo('esqueleto', nome=f'guarda morto {i + 1}', cat=3, nivel=90, maestria=6) for i in range(esqueletos)]
    return faz


def dragao_velho(artes=True, sem=()):
    """O DRAGÃO VELHO (Lendário, grau S): o dragão de hoje com roteiro. No chão; aos 60% levanta voo e chama a chuva de fogo; aos 30% a asa cede e ele desce em fúria."""
    def faz():
        if not artes: return [bichos.bicho('dragão')]
        d = bichos.bicho('dragão', nome='o dragão velho', tracos=['sopro', 'couraça', 'apavora', 'resiste'], chefe=True, foco=5,
                         artes=[dict(nome='palavra de pavor', tipo='grito', cd=30, alcance=8, usos=1, fase=1),
                                dict(nome='chuva de fogo', tipo='ataque', area=True, dado='1d10', alcance=8, prepara=True, recarga=3, mana=6, deixa='queima', fase=1, ate_fase=1)
                                ],
                         fases=[dict(abaixo=0.6, diz='levanta voo', ganha=['voa']), dict(abaixo=0.3, diz='a asa cede: desce em fúria', perde=['voa'], acerto=4, sopro_recarga=1)])
        d['artes'] = [x for x in d['artes'] if x['nome'] not in sem]
        if 'furia' in sem: d['fases'][1] = dict(abaixo=0.3, diz='a asa cede: desce', perde=['voa'])
        return [d]
    return faz


def vampiro(carnicais=3, lobos=3, artes=True, dia=False, veu=False, livre=True):
    """O SENHOR VAMPIRO (Épico, grau B): bebe a vida, a carne fecha, o aço comum fere pouco; prende com o olhar. dia=True: à luz do dia, não regenera nem drena"""
    def faz():
        tr = ['apavora', 'pede prata'] if dia else ['dreno', 'regenera', 'apavora', 'noturno', 'pede prata']
        v = bichos.bicho('vampiro', nome='o senhor vampiro', lider=True, chefe=True, tracos=tr, foco=3, **(dict(
            artes=[dict(nome='véu de sombra', tipo='escuro', rodadas=3, quando='comeco', usos=1, mana=4)] * (0 if dia or not veu else 1) + [dict(nome='o olhar', tipo='atordoa', alcance=6, perde=2, recarga=2, mana=4, quando='livre' if livre else 'sempre')],
            fases=[] if dia else [dict(abaixo=0.3, diz='a sede o toma', acerto=4, defesa=-2)]) if artes else {}))
        return [v] + [bichos.bicho('carniçal', nome=f'carniçal {i + 1}') for i in range(carnicais)] + [bichos.bicho('lobo', nome=f'lobo {i + 1}') for i in range(lobos)]
    return faz
