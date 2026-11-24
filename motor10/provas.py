#!/usr/bin/env python3
"""provas.py — MOTOR 10: O BANCO DE PROVAS. As metas de equilíbrio, escritas e medidas.

Toda mudança no tabelas.py ou no luta.py roda isto. Meta que falha: a mudança não entra (ou a meta muda, com a palavra do jogador).
As metas dizem em números o que o jogador pediu:
  "a arma decide muito quem vence" · "uma arma dá chance de um nível 50 vencer um nível 500" · "sem restrição de nível para usar a peça".
Cinco blocos: O EQUILÍBRIO (quem vence) · A DURAÇÃO (quanto dura) · AS ARMAS ENTRE SI (nenhuma escolha é a única certa)
· OS MÓDULOS (cada coisa que interfere, interfere mesmo, e para o lado certo) · OS BICHOS (as oito metas da etapa 2: o corpo é a arma
e a armadura, o bando, o chefe, o tamanho, os traços, a moral, a duração; e o que o corpo do bicho tem de ser).

E um sexto, A MAGIA NA LUTA (etapa da magia, capítulo 11): o duelo e a lei "o item decide" com o foco e o amuleto, a Mana, o grupo, as tradições, o feitiço longo
sob flecha, o retrochoque, o controle, a multidão, os bichos, os nove traços novos, a poção e o veneno de lâmina, a peça encantada, as fases do chefe, a ordem, e a luta que volta ao estado.

Uso: python3 provas.py [N] [magia]        N = lutas por meta (padrão 600) · magia: só o bloco da magia
"""
import sys
import luta
import tabelas as T
from itens import item
from pessoas import ficha, padrao, veste, defesa

C = dict(comum=0, incomum=1, raro=2, epico=3, unico=4, lendario=5, mitico=6, primordial=7)
R = C['raro']


def um(nivel, arma, arm, esc=None, familia='espada', material='malha', nome=None, elmo=None, **kw):
    """um lado com um combatente: nível, categoria da arma, categoria da armadura (e do escudo; sem dizer, igual à armadura)"""
    e = arm if esc is None else esc
    return lambda: [veste(padrao(nome or f'n{nivel}-{arma}{arm}', nivel, **kw), arma=(familia, arma), armadura=(material, arm), escudo=e, elmo=elmo)]


def varios(k, nivel, arma, arm, pre='s', familia='espada', **kw):
    return lambda: [veste(padrao(f'{pre}{i + 1}', nivel, **kw), arma=(familia, arma), armadura=('malha', arm), escudo=arm) for i in range(k)]


def gente(nome, nivel, arma, armadura=None, escudo=None, arma2=None, elmo=None, molde='guerreiro', **kw):
    """um lado com um combatente vestido peça por peça"""
    return lambda: [veste(padrao(nome, nivel, molde=molde, **kw), arma=arma, armadura=armadura, escudo=escudo, arma2=arma2, elmo=elmo)]


# (o que se mede · lado A · lado B · faixa de vitória de A em % · opções)
METAS = [
    ('SIMETRIA: iguais em tudo (nível 50, Raro)',                      um(50, R, R, nome='a'), um(50, R, R, nome='b'), (44, 56), {}),
    ('A ARMA: mesmo nível, só a ARMA uma categoria acima',             um(50, R + 1, R), um(50, R, R), (85, 100), {}),
    ('O CONJUNTO: mesmo nível, tudo uma categoria acima',              um(50, R + 1, R + 1), um(50, R, R), (92, 100), {}),
    ('O NÍVEL AJUDA DEVAGAR: mesma arma, 75 contra 50',                um(75, R, R), um(50, R, R), (50, 68), {}),
    ('O NÍVEL CONTA: mesma arma, 150 contra 50',                       um(150, R, R), um(50, R, R), (80, 100), {}),
    ('O NÍVEL SEM A MAESTRIA: 150 contra 50, os dois Mestres',         um(150, R, R, maestria=6), um(50, R, R, maestria=6), (60, 92), {}),
    ('UMA categoria na arma vence 100 níveis (50 × 150)',              um(50, R + 1, R), um(150, R, R), (55, 85), {}),
    ('A CHANCE PEQUENA: uma arma UMA acima, nível 50 × nível 500',     um(50, R + 1, R), um(500, R, R), (2, 20), {}),
    ('DUAS categorias na arma vencem 150 níveis (50 × 200)',           um(50, R + 2, R), um(200, R, R), (85, 100), {}),
    ('A ARMA DECIDE: uma arma DUAS acima, nível 50 × nível 500',       um(50, R + 2, R), um(500, R, R), (45, 75), {}),
    ('... e não é sorte do nível 50: o mesmo com o nível 40',          um(40, R + 2, R), um(500, R, R), (25, 75), {}),
    ('... e com o nível 60',                                           um(60, R + 2, R), um(500, R, R), (45, 80), {}),
    ('uma arma TRÊS acima, nível 50 × nível 500',                      um(50, R + 3, R), um(500, R, R), (80, 100), {}),
    ('A ARMADURA DECIDE MENOS: só a armadura DUAS acima, 50 × 500',    um(50, R, R + 2, esc=R), um(500, R, R), (1, 45), {}),
    ('... mas conta: só a armadura UMA acima, no mesmo nível',         um(50, R, R + 1, esc=R), um(50, R, R), (75, 97), {}),
    ('... e só a armadura DUAS acima vence 100 níveis (50 × 150)',     um(50, R, R + 2, esc=R), um(150, R, R), (75, 100), {}),
    ('O CONJUNTO duas acima (com Vontade para sustentar), 50 × 500',   um(50, R + 2, R + 2, atributos={'Vontade': 80}), um(500, R, R), (95, 100), {}),
    ('A FANTASIA: um nível 50 de conjunto Lendário × dez de nível 275 de Raro', um(50, C['lendario'], C['lendario'], moral='firme'), varios(10, 275, R, R), (85, 100), dict(n=200)),
    ('A GUILDA: um nível 90 de conjunto Mítico × dez de nível 275 de Raro', um(90, C['mitico'], C['mitico'], moral='firme'), varios(10, 275, R, R), (90, 100), dict(n=120)),
    ('SÓ A ARMA NÃO BASTA contra dez: o mesmo, com armadura Rara',     um(90, C['mitico'], R, moral='firme'), varios(10, 275, R, R), (0, 40), dict(n=120)),
    ('O NÚMERO CONTA: uma categoria não garante contra dez (nível 120 de Lendário × dez de nível 60 de Único)', um(120, C['lendario'], C['lendario'], moral='firme'), varios(10, 60, C['unico'], C['unico']), (15, 60), dict(n=300)),
    ('... e na mesma categoria os dez vencem sempre',                  um(120, C['unico'], C['unico'], moral='firme'), varios(10, 60, C['unico'], C['unico']), (0, 5), dict(n=120)),
    ('... mas DUAS categorias no conjunto vencem os dez',              um(120, C['mitico'], C['mitico'], moral='firme', atributos={'Vontade': 80}), varios(10, 60, C['unico'], C['unico']), (90, 100), dict(n=120)),
    ('SOLDADOS COMUNS não derrubam o Lendário: um nível 120 × dez de nível 15', um(120, C['lendario'], C['lendario'], moral='firme'), varios(10, 15, 0, 0), (97, 100), dict(n=120)),
]
# (o que se mede · lado A · lado B · faixa da MEDIANA de rodadas)
DURACAO = [
    ('duelo entre iguais (nível 50, Raro)',            um(50, R, R, nome='a'), um(50, R, R, nome='b'), (4, 9)),
    ('duelo entre iguais (nível 150, Lendário)',       um(150, 5, 5, nome='a'), um(150, 5, 5, nome='b'), (4, 9)),
    ('cinco contra cinco (nível 40, Incomum)',         varios(5, 40, 1, 1, pre='a'), varios(5, 40, 1, 1, pre='b'), (4, 12)),
    ('a luta em que o aço não passa não se arrasta: só a armadura DUAS acima, 50 × 500', um(50, R, R + 2, esc=R), um(500, R, R), (4, 30)),
]

# AS ARMAS ENTRE SI: toda arma de guerra, com cada armadura, todas Raras, nível 60, uma contra todas as outras
UMA_MAO = ['espada', 'maça', 'machado', 'martelo', 'lança']
DUAS_MAOS = ['montante', 'alabarda', 'malho']


def armas(n):
    """cada montagem luta contra todas as outras. Devolve [(montagem, % médio de vitória)]."""
    mont = [(f, m) for f in UMA_MAO + DUAS_MAOS for m in T.MATERIAIS]
    faz = lambda f, m, nome: gente(nome, 60, (f, R), (m, R), R if f in UMA_MAO else None)
    soma = {x: 0 for x in mont}
    for i, a in enumerate(mont):
        for b in mont[i + 1:]:
            v, _ = luta.duelos(faz(*a, 'um'), faz(*b, 'outro'), n=n, inicio='perto')
            soma[a] += v; soma[b] += 100 - v
    return [(f"{f}{' e escudo' if f in UMA_MAO else ''}, {m}", round(s / (len(mont) - 1))) for (f, m), s in soma.items()]


def modulos(n):
    """cada módulo da luta tem de mexer no resultado para o lado certo. Devolve [(o que se mede, o que deu, passou?)]."""
    out = []; v = lambda a, b, **kw: luta.duelos(a, b, n=n, **kw)[0]
    # 1 distância e alcance
    lan = lambda: [veste(padrao(f'lança {i}', 50), arma=('lança', R), armadura=('couro', R)) for i in (1, 2, 3)]
    esp = lambda: [veste(padrao(f'espada {i}', 50), arma=('espada', R), armadura=('couro', R)) for i in (1, 2, 3)]
    x = v(lan, esp, inicio='perto', lugar=dict(largura=1)); y = v(lan, esp, inicio='perto')
    out.append(('1 ALCANCE: três lanças contra três espadas (sem escudo), num corredor de um e em campo aberto', f'{x}% e {y}%', x >= 60 and x - y >= 5))
    arq = gente('arqueira', 50, ('arco', R), ('couro', R), arma2=('adaga', R), molde='arqueiro'); inf = gente('infante', 50, ('espada', R), ('malha', R), R)
    lo, co = v(arq, inf, inicio='longe'), v(arq, inf, inicio='colado')
    out.append(('1 DISTÂNCIA: a arqueira começa longe ou começa colada', f'{lo}% contra {co}%', lo - co >= 15))
    # 3 o tempo
    nb, lm = v(arq, inf, inicio='longe', tempo=['neblina']), v(arq, inf, inicio='longe', tempo=['lama'])
    out.append(('3 O TEMPO: a mesma arqueira, de longe: na neblina, com tempo limpo, na lama', f'{nb}%, {lo}%, {lm}%', lo - nb >= 8 and lm - lo >= 8))
    # 2 o lugar
    so = gente('sozinho', 150, ('espada', R + 1), ('malha', R), R, moral='firme'); quatro = varios(4, 50, R, R, pre='t')
    ab, cr = v(so, quatro, inicio='perto'), v(so, quatro, inicio='perto', lugar=dict(largura=1))
    out.append(('2 O LUGAR: um contra quatro, em campo aberto ou num corredor de um', f'{ab}% contra {cr}%', cr - ab >= 10))
    # 5 golpe contra armadura
    placa = gente('de placa', 60, ('espada', R), ('placa', R), R)
    ma, mo = v(gente('malho', 60, ('malho', R), ('malha', R)), placa), v(gente('montante', 60, ('montante', R), ('malha', R)), placa)
    out.append(('5 GOLPE CONTRA ARMADURA: o malho e o montante contra a placa', f'{ma}% contra {mo}%', ma - mo >= 10))
    # 4 fôlego e requisito
    fraco = ficha(veste(padrao('fraco', 50, atributos={'Força': 60}), arma=('espada', R), armadura=('placa', R)))
    forte = ficha(veste(padrao('forte', 50, atributos={'Força': 85}), arma=('espada', R), armadura=('placa', R)))
    out.append(('4 REQUISITO: a placa em quem não tem Força para ela', f"Defesa {defesa(fraco):g} contra {defesa(forte):g}; fôlego por rodada {fraco['fol_rodada']} contra {forte['fol_rodada']}",
                defesa(fraco) < defesa(forte) and fraco['fol_rodada'] > forte['fol_rodada']))
    novato = padrao('novato', 20); pede_placa = T.MATERIAIS['placa']['pede']
    out.append(('4 REQUISITO: a gente gerada de nível baixo não tem Força para a placa nem para a arma pesada', f"nível 20: Força {novato['atributos']['Força']} (a placa pede {pede_placa})", novato['atributos']['Força'] < pede_placa))
    S = luta.nova(um(50, R, R, nome='exausto')(), um(50, R, R, nome='inteiro')(), inicio='colado', quieto=False); ex = S['L'][0]; ex['fol'] = 0; S['r'] = 1; S['log'] = []
    luta._turno(S, ex); golpes = sum('exausto golpeia' in x for x in S['log'])
    out.append(('4 FÔLEGO: quem começa o turno sem fôlego faz uma ação só', f'{golpes} golpe(s) no turno', golpes <= 1 and ('toma fôlego' in ' '.join(S['log']) or golpes == 1)))
    # sob medida e sintonia
    sob = lambda dono: item('arma', 5, 'a espada do Aldric', familia='montante', sob=dict(dono=dono, grau=3))
    dele = ficha(veste(padrao('Aldric', 30, atributos={'Força': 60}), arma=sob('Aldric'))); de_outro = ficha(veste(padrao('Bera', 30, atributos={'Força': 60}), arma=sob('Aldric')))
    out.append(('SOB MEDIDA: a mesma peça na mão do dono e na mão de outro', f"acerto +{dele['arma']['acerto']:g} e × {dele['arma']['mult']:g} contra +{de_outro['arma']['acerto']:g} e × {de_outro['arma']['mult']:g}",
                dele['arma']['mult'] > de_outro['arma']['mult'] and dele['arma']['acerto'] > de_outro['arma']['acerto']))
    muitas = veste(padrao('carregado', 50, atributos={'Vontade': 25}), arma=item('arma', 4, familia='espada', efeitos=[dict(chave='sangra')]), armadura=('malha', 3), escudo=item('escudo', 3, efeitos=[dict(chave='firme')]))
    f = ficha(muitas); out.append(('SINTONIA: quatro peças despertas em quem só sustenta uma', f"dormem: {', '.join(f['dormem']) or 'nenhuma'}",
                                   len(f['dormem']) == 3 and f['arma']['efeitos'] == {'sangra': True} and not any(s['efeitos'] for s in f['fontes'])))
    tres = varios(3, 100, R, R, pre='t')
    com, semv = v(um(50, R + 1, R + 1, moral='firme', atributos={'Vontade': 80}), tres), v(um(50, R + 1, R + 1, moral='firme'), tres)
    out.append(('SINTONIA NA LUTA: o conjunto Épico contra três de nível 100 de Raro, com Vontade para as quatro peças e sem', f'{com}% contra {semv}%', com - semv >= 20))
    # 6 parte do corpo
    sem = v(gente('sem elmo', 50, ('espada', R), ('malha', R), R, elmo=False), gente('de elmo', 50, ('espada', R), ('malha', R), R))
    out.append(('6 PARTE DO CORPO: o mesmo guerreiro sem o elmo, contra o de elmo', f'{sem}%', sem <= 40))
    # 7 durabilidade e o impasse
    q = 0; imp = 0; k = max(30, n // 6)
    for _ in range(k):
        S = luta.nova(gente('mestre de ferro ruim', 300, ('espada', 0), ('malha', R), R)(), gente('bem vestido', 50, ('espada', R), ('malha', 4), 4, moral='firme')(), inicio='colado', quieto=True); luta.corre(S)
        q += 'espada Comum' in luta.resultado(S)['quebradas']
        S = luta.nova(gente('mal armado', 50, ('espada', 0), ('malha', 3), 3)(), gente('bem vestido', 50, ('espada', 0), ('malha', 3), 3)(), inicio='colado', quieto=True); luta.corre(S)
        imp += S['fim'] == 'impasse'
    q = round(100 * q / k); imp = round(100 * imp / k)
    out.append(('7 DURABILIDADE: o mestre de nível 300 com espada Comum quebra a espada na armadura Única', f'em {q}% das lutas', q >= 50))
    out.append(('O IMPASSE: quando ninguém fere ninguém, os lados se separam (a luta não vai a 60 rodadas)', f'em {imp}% dessas lutas', imp >= 80))
    # 8 moral
    m = 0; k = max(60, n // 3)
    for _ in range(k):
        S = luta.nova(um(120, 4, 4, moral='firme')(), varios(6, 30, 1, 1, pre='b')(), inicio='colado', quieto=True); luta.corre(S); r = luta.resultado(S)
        m += bool(r['fugiram'] or r['presos'])
    m = round(100 * m / k); out.append(('8 MORAL: seis contra um muito mais forte: alguém foge ou se rende', f'em {m}% das lutas', m >= 30))
    foge = 0
    for _ in range(k):
        S = luta.nova(um(30, 1, 1, nome='o jogador', controla=True)() + varios(3, 30, 1, 1, pre='amigo ')(), um(120, 4, 4, nome='o terror', moral='firme')(), inicio='colado', quieto=True); luta.corre(S)
        foge += S['L'][0]['estado'] in ('fugiu', 'rendido')
    out.append(('8 MORAL: quem o jogador comanda nunca foge nem se rende pelo dado', f'{foge} vez(es) em {k} lutas perdidas', foge == 0))
    # 9 grupo contra grupo: o cerco e o contorno
    S = luta.nova(um(200, 5, 5, nome='o cercado', moral='firme')(), varios(10, 50, R, R, pre='c')(), inicio='colado', quieto=True); mx = 0
    for _ in range(4):
        luta.rodada(S); mx = max(mx, len(S['L'][0]['golpeado']))
    out.append(('9 O CERCO: dez contra um em campo aberto, quantos batem nele numa rodada', f'{mx} (o teto é {T.CERCO} de perto e {T.CERCO_HASTE} de haste)', 3 <= mx <= T.CERCO))
    passou = 0; k = max(30, n // 10)
    for _ in range(k):
        S = luta.nova(um(200, 0, 5, nome='a linha', moral='firme')() + gente('a de trás', 50, ('arco', R), ('couro', R), linha='trás', moral='firme', molde='arqueiro')(), varios(7, 50, R, R, pre='c', moral='firme')(), inicio='colado', quieto=False)
        for _ in range(3):
            if not S['fim']: luta.rodada(S)
        passou += any('golpeia a de trás' in x for x in S['log'])
    passou = round(100 * passou / k); out.append(('9 O CONTORNO: sete contra uma linha de um: os que sobram passam e chegam em quem está atrás', f'em {passou}% das lutas, em três rodadas', passou >= 70))
    # 10 a luta para e pergunta
    S = luta.nova(gente('o rei', 40, ('lança', 3), ('couro', 2), controla=True)(), varios(2, 40, 1, 1, pre='b')(), inicio='colado', quieto=True)
    p1 = luta.corre(S, interativo=True); luta.ordem(S, 'o rei: recuar'); x0 = S['L'][0]['x']; luta.rodada(S)
    out.append(('10 PARA E PERGUNTA: a luta para antes da 1ª rodada, e a ordem de recuar é cumprida', f"{p1}; o rei foi da casa {x0} para a {S['L'][0]['x']}", p1 == 'parada' and S['L'][0]['x'] < x0))
    meio = 0; k = max(60, n // 5)
    for _ in range(k):
        S = luta.nova(gente('o rei', 40, ('espada', 1), ('couro', 1), controla=True)() + varios(2, 40, 1, 1, pre='amigo ')(), varios(4, 40, 2, 1, pre='b')(), inicio='colado', quieto=True)
        luta.corre(S, interativo=True)
        while luta.corre(S, interativo=True) == 'parada':
            if S['fila']: meio += 1; break
    meio = round(100 * meio / k); out.append(('10 PARA E PERGUNTA: a parada vem no MEIO da rodada, antes dos turnos que faltam', f'em {meio}% das lutas houve parada com turnos por vir', meio >= 50))
    D0 = luta.D; luta.semente(35); gasto = avisou = 0; k = 60       # dados à parte: as outras provas rolam os mesmos de antes
    for _ in range(k):
        S = luta.nova(gente('o rei', 40, ('espada', 1), ('couro', 1), controla=True)(), varios(2, 40, 1, 1, pre='b')(), inicio='longe', quieto=False)
        luta.corre(S, interativo=True); luta.ordem(S, 'o rei: folego'); viu = False
        while luta.corre(S, interativo=True) == 'parada': viu = viu or any('recuperou o fôlego' in x for x in S['paradas'])
        gasto += sum('o rei se resguarda (o fôlego já está cheio' in x for x in S['log']); avisou += viu
    luta.D = D0
    out.append(('10 A ORDEM DE FÔLEGO ACABA quando o fôlego enche: a luta para e pergunta, e ninguém segue tomando fôlego de fôlego cheio enquanto o inimigo chega',
                f'{k} lutas com a ordem dada de fôlego cheio e o inimigo longe: {gasto} ações gastas tomando fôlego à toa; a luta parou e avisou em {avisou}', gasto == 0 and avisou == k))
    D0 = luta.D; luta.semente(36); k = 120; pegou = torto = 0      # dados à parte, como na prova de cima
    for _ in range(k):
        S = luta.nova(gente('o guarda', 30, ('lança', 1), ('malha', 0), escudo=0)(), [x for i in (1, 2) for x in gente(f'bandido {i}', 7, ('adaga', 0))()], inicio='perto', quieto=False)
        luta.corre(S); L = S['log']
        for i, linha in enumerate(L):
            if '(o alcance bate primeiro)' not in linha: continue
            quem = next((f['nome'] for f in S['L'] if f['lado'] == 'B' and f"golpeia {f['nome']} (o alcance" in linha), None); pegou += 1
            depois = next((x for x in L[i + 1:] if not x.startswith('    ')), '')        # a primeira linha depois do golpe e do que ele causou (as linhas dele vêm mais recuadas)
            torto += bool(quem) and (depois.startswith(f'  {quem} avança') or not (i > 0 and L[i - 1].startswith(f'  {quem} avança')))
    luta.D = D0
    out.append(('O REGISTRO NA ORDEM: quem avança para dentro de uma arma mais longa aparece dando o passo ANTES do golpe que o pega; ninguém avança, no registro, depois de cair ou de morrer',
                f'{k} lutas de um lanceiro contra dois de adaga: {pegou} golpes de "o alcance bate primeiro"; em {torto} a linha do passo veio depois do golpe', pegou >= 20 and torto == 0))
    saiu = 0; k = max(60, n // 5)
    for _ in range(k):
        S = luta.nova(gente('o rei', 40, ('espada', 1), ('couro', 1), controla=True, linha='trás')() + varios(2, 60, 2, 2, pre='guarda ', moral='firme')(), varios(4, 40, 1, 1, pre='b')(), inicio='perto', lugar=dict(largura=2), quieto=True)
        luta.corre(S, interativo=True); luta.ordem(S, 'o rei: recuar defensiva')
        while luta.corre(S, interativo=True) == 'parada' and S['L'][2]['estado'] == 'pe': pass
        saiu += next(f for f in S['L'] if f['nome'] == 'o rei')['estado'] == 'saiu'
    saiu = round(100 * saiu / k); out.append(('A RETIRADA: com dois guardas segurando o corredor, quem recebe ordem de recuar sai da luta', f'em {saiu}% das lutas', saiu >= 80))
    D0 = luta.D; luta.semente(52); k = 150; torto = venceu = ficou = 0      # dados à parte, para as outras medidas não mudarem
    casa = lambda: gente('Maro', 5, ('espada', 0), ('malha', 0), escudo=0, controla=True)() + gente('Rute', 22, ('arco', 1), ('couro', 0), molde='arqueiro', controla=True)()
    for _ in range(k):
        S = luta.nova(casa(), gente('o ladrão', 1, ('adaga', 0), molde='comum')(), inicio='perto', quieto=False)
        luta.corre(S, interativo=True); luta.ordem(S, 'Maro: recuar'); luta.ordem(S, 'Rute: atacar')
        while luta.corre(S, interativo=True) == 'parada': pass
        L = S['log'] if 'Maro SAI DA LUTA' in ''.join(S['log']) else []; sai = next((i for i, x in enumerate(L) if 'Maro SAI DA LUTA' in x), None)       # o registro da última corrida (onde a luta acabou)
        caiu = next((i for i, x in enumerate(L) if 'o ladrão' in x and any(y in x for y in ('MORRE', 'CAI', 'sangra até cair'))), None)
        torto += sai is not None and caiu is not None and caiu < sai                                                                                      # saiu DEPOIS de o último inimigo cair
        venceu += S['fim'] == 'A'; ficou += S['fim'] == 'A' and luta.por_nome(S, 'Maro')['estado'] == 'pe'
    S = luta.nova(casa(), gente('o ladrão', 1, ('adaga', 0), molde='comum')(), inicio='colado', quieto=True); S['comecou'] = True; S['r'] = 1; luta.ordem(S, 'Maro: recuar')
    S['L'][2].update(estado='morto', pv=0); luta._fecha_rodada(S); mao = (luta.por_nome(S, 'Maro')['estado'], S['fim'])       # posto à mão: o último inimigo cai com quem recuava a 1 casa
    luta.D = D0
    out.append(('A RETIRADA SÓ EXISTE COM INIMIGO DE PÉ: quem tem ordem de recuar na rodada em que o último inimigo cai NÃO sai da luta: a luta acabou, e ele ficou com o campo como os outros',
                f'{k} lutas de dois contra um ladrão, com "Maro: recuar": a casa venceu {venceu}, e Maro acabou de pé no campo em {ficou}; saiu da luta depois de o último inimigo cair: {torto} vez(es); '
                f'posto à mão (o inimigo morto, Maro a 1 casa, com ordem de recuar): Maro fica "{mao[0]}" e o campo é de "{mao[1]}"', torto == 0 and mao == ('pe', 'A') and venceu >= k // 2 and ficou >= venceu // 2))
    try: luta.nova(um(50, R, R, nome='gêmeo')(), um(50, R, R, nome='gêmeo')(), tempo=['granizo'], quieto=True); erro = 'aceitou'
    except SystemExit as e: erro = 'recusou' if 'nome repetido' in str(e) and 'granizo' in str(e) else 'recusou pela metade'
    out.append(('O CENÁRIO É CONFERIDO antes de qualquer dado (nome repetido, tempo que não existe)', erro, erro == 'recusou'))
    return out


def bichos(n):
    """OS BICHOS: as oito metas do contrato da etapa 2 (projeto/ETAPA2.md, seção 4), de B1 a B8, e o que o corpo do bicho tem de ser (B+).
    As lutas começam "perto" (3 casas), como um encontro no ermo. O homem do degrau é o do banco: gente gerada, de espada, malha e escudo.
    Devolve [(o que se mede, o que deu, passou?)]."""
    import contextlib, io, json, random
    import bichos as B
    import tabelas_bichos as TB
    out = []; ok = lambda nome, deu, passa: out.append((nome, deu, bool(passa)))
    bi = lambda esp, q=None, **mais: (lambda: B.bando(esp, n=q, **mais) if q else [B.bicho(esp, **mais)])
    v = lambda a, b, **kw: luta.duelos(a, b, **{**dict(n=n, inicio='perto'), **kw})
    ref = {0: 10, 1: 30, 2: 50, 3: 90, 4: 120, 5: 150}                    # o nível do homem do degrau, por categoria
    # B1 e B8: o mesmo degrau
    x, rod = v(um(50, R, R), bi('pantera'))
    ok('B1 O MESMO DEGRAU: um nível 50, tudo Raro, contra a pantera (Rara, média, sozinha): 40 a 60%', f'{x}%', 40 <= x <= 60)
    # B2: uma categoria na arma
    mais = v(um(50, R + 1, R), bi('pantera'))[0]; perde = 0
    for _ in range(n):
        S = luta.nova(um(50, R - 1, R)(), bi('pantera')(), inicio='perto', quieto=True); luta.corre(S); perde += S['fim'] == 'B'
    perde = round(100 * perde / n)
    ok('B2 A ARMA DECIDE CONTRA O BICHO: o mesmo homem com a arma uma categoria acima vence em 80% ou mais; com a arma uma abaixo, perde em 80% ou mais', f'vence {mais}%; perde {perde}%', mais >= 80 and perde >= 80)
    # B3: o bando
    ab, co = v(um(30, 1, 1), bi('lobo', 4))[0], v(um(30, 1, 1), bi('lobo', 4), lugar=dict(largura=1))[0]
    ok('B3 O BANDO: quatro lobos Incomuns contra um nível 30 de conjunto Incomum: 10 a 35% em campo aberto, e 20 pontos a mais num corredor de um', f'{ab}% e {co}%', 10 <= ab <= 35 and co - ab >= 20)
    # B4: o chefe
    ra, ep = v(varios(4, 60, R, R), bi('serpe'))[0], v(varios(4, 60, R + 1, R + 1), bi('serpe'))[0]; ev = v(varios(4, 60, R + 1, R + 1, atributos={'Vontade': 80}), bi('serpe'), n=max(100, n // 3))[0]
    ok('B4 O CHEFE: a serpe (Épica, enorme) contra quatro de nível 60 de conjunto Raro (5 a 30%) e de conjunto Épico (55 a 90%)',
       f'{ra}% e {ep}% (gente gerada: a Vontade 56 sustenta duas peças Épicas, a arma e o escudo, e a armadura dorme; com Vontade 80, o conjunto inteiro desperto: {ev}%)', 5 <= ra <= 30 and 55 <= ep <= 90)
    # B5: o tamanho
    tams = list(TB.TAMANHOS); med = {}
    for t in tams:
        f = ficha(B.bicho('urso', tamanho=t, tracos=[], cat=R)); S = luta.nova(bi('urso', nome='o alvo', tamanho=t, tracos=[], cat=5, moral='firme')(), varios(14, 50, R, R, pre='c', moral='firme')(), inicio='colado', quieto=True); mx = 0
        for _ in range(2): luta.rodada(S); mx = max(mx, len(S['L'][0]['golpeado']))
        S = luta.nova(um(50, R, R)(), [B.bicho('urso', nome=f'bicho {i}', tamanho=t, tracos=[]) for i in range(4)], lugar=dict(largura=2), quieto=True); cabem = sum(1 for g in S['L'][1:] if g['x'] == S['L'][1]['x'])
        tent = acert = 0
        for _ in range(max(150, n // 2)):
            S = luta.nova(um(50, R, R, nome='o homem', moral='firme')(), bi('urso', nome='o alvo', tamanho=t, tracos=[], cat=R, moral='firme')(), inicio='colado'); luta.corre(S, maximo=6)
            gol = [l for l in S['log'] if l.startswith('  o homem golpeia o alvo')]; tent += len(gol); acert += sum(1 for l in gol if 'erra' not in l and 'aparado' not in l)
        med[t] = dict(pv=f['pvmax'], alc=f['arma']['alcance'], defesa=defesa(f), cerco=mx, cabem=cabem, acerta=round(100 * acert / max(1, tent)))
    cresce = lambda k, estrito=True: all((med[a][k] < med[b][k]) if estrito else (med[a][k] <= med[b][k]) for a, b in zip(tams, tams[1:]))
    lst = lambda k, suf='': ', '.join(f'{med[t][k]:g}{suf}' for t in tams)
    ok('B5 O TAMANHO (o mesmo bicho pequeno, médio, grande e enorme): o maior tem mais PV, alcança mais longe, apanha de mais gente, toma mais do corredor e é mais fácil de acertar',
       f"PV {lst('pv')} · alcança {lst('alc')} casa(s) · batem nele na rodada {lst('cerco')} · cabem {lst('cabem')} na frente de um corredor de dois · Defesa {lst('defesa')} · o homem acerta {lst('acerta', '%')} dos golpes",
       cresce('pv') and cresce('alc', False) and med['enorme']['alc'] > med['pequeno']['alc'] and cresce('cerco') and [med[t]['cerco'] for t in tams] == [TB.TAMANHOS[t]['cerco'][0] for t in tams]
       and all(med[a]['cabem'] >= med[b]['cabem'] for a, b in zip(tams, tams[1:])) and med['pequeno']['cabem'] > med['médio']['cabem'] > med['grande']['cabem'] and cresce('acerta') and med['enorme']['acerta'] - med['pequeno']['acerta'] >= 15)
    # B6: cada traço, com e sem (a vitória de quem enfrenta o bicho tem de cair 8 pontos ou mais com o traço)
    casos = [('matilha', 'quatro lobos contra um nível 30 de conjunto Incomum', um(30, 1, 1), 'lobo', 4, {}),
             ('bote', 'a pantera contra um nível 50 de conjunto Raro', um(50, R, R), 'pantera', None, {}),
             ('investida', 'o javali, vindo de longe, contra um nível 10 de conjunto Comum', um(10, 0, 0), 'javali', None, dict(inicio='longe')),
             ('veneno', 'a surucucu contra um nível 30 de conjunto Incomum', um(30, 1, 1), 'surucucu', None, {}),
             ('agarra', 'o urso contra um nível 30 de conjunto Incomum', um(30, 1, 1), 'urso', None, {}),
             ('voa', 'o grifo contra um nível 50 de conjunto Raro, de espada', um(50, R, R), 'grifo', None, {}),
             ('regenera', 'o trasgo contra um nível 50 de conjunto Raro', um(50, R, R), 'trasgo', None, {}),
             ('apavora', 'a hidra contra quatro de nível 120 de conjunto Único', varios(4, 120, 4, 4), 'hidra', None, {}),
             ('couraça', 'o basilisco (Épico) contra quatro de nível 60 de conjunto Raro', varios(4, 60, R, R), 'basilisco', None, {}),
             ('sopro', 'a serpe contra quatro de nível 60 de conjunto Épico', varios(4, 60, R + 1, R + 1), 'serpe', None, {})]
    assert [c[0] for c in casos] == list(TB.TRACOS), 'cada traço da lista fechada tem a sua prova'
    for t, nome, quem, esp, q, kw in casos:
        com = v(quem, bi(esp, q), **kw)[0]; sem = v(quem, bi(esp, q, tracos=[x for x in TB.ESPECIES[esp]['tracos'] if x != t]), **kw)[0]
        extra = f"; de lança, {v(um(50, R, R, familia='lança'), bi('grifo'), n=max(100, n // 3))[0]}%" if t == 'voa' else ''
        ok(f'B6 O TRAÇO {t.upper()}: {nome}, com o traço e sem ele (8 pontos ou mais)', f'vence {com}% com, {sem}% sem: {sem - com:+d}{extra}', sem - com >= 8)
    # B7: a moral do bicho
    comuns = [k for k, e in TB.ESPECIES.items() if not e['chefe']]; k = max(60, n // 4); tot_v = tot_f = 0; por = {}; rend = 0
    def fugas(a, b, k, **kw):
        nv = nf = nr = 0
        for _ in range(k):
            S = luta.nova(a(), b(), quieto=True, **{**dict(inicio='perto'), **kw}); luta.corre(S); nr += any(f['estado'] == 'rendido' for f in S['L'])
            if S['fim'] == 'A': nv += 1; nf += any(f['estado'] == 'fugiu' for f in S['L'] if f['lado'] == 'B')
        return nv, nf, nr
    for esp in comuns:
        c = TB.ESPECIES[esp]['cat']; nv, nf, nr = fugas(um(ref[c], c, c, **(dict(atributos={'Vontade': 80}) if c >= 3 else {})), bi(esp), k); tot_v += nv; tot_f += nf; rend += nr; por[esp] = round(100 * nf / max(1, nv))
    _, enc, _ = fugas(um(50, R, R), bi('pantera'), k, lugar=dict(sem_saida='B')); _, chf, _ = fugas(varios(4, 90, 3, 3, atributos={'Vontade': 80}), bi('serpe'), k)
    geral = round(100 * tot_f / max(1, tot_v)); menos_foge = min(por, key=por.get)
    ok('B7 A MORAL: o bicho comum ferido foge em 30% ou mais das lutas que perde (cada espécie que não é chefe, sozinha, contra o homem do degrau dela); o encurralado e o chefe não fogem; ninguém se rende',
       f"foge em {geral}% das {tot_v} lutas perdidas (a que mais foge: {max(por, key=por.get)}, {max(por.values())}%; a que menos: {menos_foge}, {por[menos_foge]}%) · a pantera sem saída fugiu {enc} vez(es) · a serpe fugiu {chf} vez(es) · rendições: {rend}",
       geral >= 30 and enc == 0 and chf == 0 and rend == 0)
    # B8: a duração
    sos = [e for e, d in TB.ESPECIES.items() if d['bando'] == (1, 1) and not d['chefe'] and e != 'pantera']        # os outros bichos que andam sozinhos, cada um contra o homem do degrau dele
    dur = {e: luta.duelos(um(ref[TB.ESPECIES[e]['cat']], TB.ESPECIES[e]['cat'], TB.ESPECIES[e]['cat'], **(dict(atributos={'Vontade': 80}) if TB.ESPECIES[e]['cat'] >= 3 else {})), bi(e), n=max(200, n // 3), inicio='perto')[1] for e in sos}
    ok('B8 A DURAÇÃO: a luta de um contra um bicho do mesmo degrau, mediana de 3 a 9 rodadas (a de B1, e a de cada bicho que anda sozinho contra o homem do degrau dele)',
       f"a pantera {rod} rodadas; " + ', '.join(f'{e} {r}' for e, r in dur.items()), 3 <= rod <= 9 and all(3 <= r <= 9 for r in dur.values()))
    # B+: o corpo não é peça
    gasta = quebrou = dorme = 0; k = max(30, n // 10)
    for _ in range(k):
        S = luta.nova(gente('o caçador', 150, ('espada', R), ('malha', R + 2), R + 2, moral='firme', atributos={'Vontade': 90})(), bi('basilisco', moral='firme')(), inicio='colado', quieto=True); luta.corre(S)
        corpos = [it for it in S['itens'].values() if it.get('tipo') == 'corpo']; quebrou += any(it['dur'] != [1, 1] or it.get('id') or it.get('dono') for it in corpos) or bool(luta.resultado(S)['quebradas'] and any('corpo' in q for q in luta.resultado(S)['quebradas']))
        gasta += any(it['dur'][0] < it['dur'][1] - 1 for it in S['itens'].values() if it.get('tipo') == 'arma')
    f = ficha(B.bicho('dragão', atributos={'Vontade': 10})); dorme = len(f['dormem'])
    ok('B+ O CORPO NÃO É PEÇA: não quebra, não tem dono nem registro no Livro, e não ocupa sintonia (mas gasta o aço de quem bate nele com arma pior)',
       f"em {k} lutas longas contra o basilisco (Épico), o corpo se gastou ou ganhou dono em {quebrou}; a espada Rara do caçador se gastou na luta em {round(100 * gasta / k)}%; o dragão (corpo Lendário) com Vontade 10: {dorme} peça(s) dormindo",
       quebrou == 0 and dorme == 0 and gasta >= k * 0.5)
    # B+: a ameaça
    falta = [e for e, d in TB.ESPECIES.items() if not all(x in B.ameaca(e) for x in (f"grau {d['grau']}", T.CATS[d['cat']], d['tamanho'][:-1], d['couro'], TB.GRAU_DIZ[d['grau']])) or any(TB.TRACOS[t] not in B.ameaca(e) for t in d['tracos'])
             or ('não foge' in B.ameaca(e)) != d['chefe']]
    a = B.ameaca('lobo', n=4, arma='Comum', armadura='Comum')
    em_bando = [e for e, d in TB.ESPECIES.items() if d['bando'][1] > 1]; avisa = [e for e in em_bando if 'EM BANDO, o grau' in B.ameaca(e) and 'o bando vale grau' in B.ameaca(e) and 'EM BANDO' not in B.ameaca(e, n=1)]
    sozinhas = [e for e, d in TB.ESPECIES.items() if d['bando'][1] == 1 and 'EM BANDO' not in B.ameaca(e)]; rato = B.ameaca('ratazana')
    sobe = f"valem grau {TB.grau_do_bando('F', 2)}" in B.ameaca('corça', n=2) and f"valem grau {TB.grau_do_bando('D', 4)}" in a and TB.grau_do_bando('F', 2) == 'E' and TB.grau_do_bando('D', 4) == 'B' and TB.grau_do_bando('S', 9) == 'S'
    ok('B+ A AMEAÇA: a frase que o caçador lê antes da luta diz o grau, a categoria, o tamanho, o corpo e os traços de cada espécie, e faz a conta da regra de ouro com o que ele veste; '
       'da que anda em bando, diz que o grau é o de um só e quanto vale o bando (um grau acima com 2 ou 3, dois com 4 ou mais), o cerco e o corredor; do bicho pequeno, que o traço dele não derruba gente',
       f"{len(TB.ESPECIES) - len(falta)} de {len(TB.ESPECIES)} espécies; o lobo contra quem veste Comum: {'diz um terço e o triplo' if 'um terço' in a and 'o triplo' in a else 'NÃO DIZ'}; "
       f"o aviso do bando em {len(avisa)} de {len(em_bando)} espécies de bando (e em nenhuma das {len(sozinhas)} que andam sós); duas corças valem grau {TB.grau_do_bando('F', 2)} e quatro lobos, grau {TB.grau_do_bando('D', 4)}: {'dito' if sobe else 'NÃO DITO'}; a ratazana: {'diz que não derruba gente' if 'não derruba nem agarra gente' in rato else 'NÃO DIZ'}",
       not falta and sobe and 'um terço' in a and 'o triplo' in a and 'são 4' in a and len(avisa) == len(em_bando) and len(sozinhas) + len(em_bando) == len(TB.ESPECIES) and 'não derruba nem agarra gente' in rato and 'não derruba nem agarra gente' not in B.ameaca('lobo'))
    # B+: o despojo e o núcleo
    ruim = []; r1 = B.despojo('serpe', random.Random(3)); r2 = B.despojo('serpe', random.Random(3))
    for e, d in TB.ESPECIES.items():
        for i in range(20):
            bens, nuc = B.despojo(e, random.Random(i))
            if set(bens) != set(d['despojo']) or any(not 1 <= bens[b] <= d['despojo'][b] for b in bens) or bool(nuc) != d['chefe']: ruim.append(e)
            if nuc and not (nuc['tipo'] == 'nucleo' and nuc['cat'] == d['cat'] and nuc['de'] == e and nuc['dur'] == [1, 1] and nuc['dono'] is None): ruim.append(e)
            if any(M_cat is not None and M_cat > 2 for M_cat in [int(b.split(':')[1]) if ':' in b else None for b in bens]): ruim.append(e)
    ok('B+ O DESPOJO: sai da tabela (de metade ao inteiro de cada bem, matéria até o Raro), a mesma sorte dá o mesmo despojo, e só o chefe dá núcleo, da categoria dele',
       f"{len(TB.ESPECIES) - len(set(ruim))} de {len(TB.ESPECIES)} espécies certas; chefes: {', '.join(e for e, d in TB.ESPECIES.items() if d['chefe'])}", not ruim and r1 == r2)
    # B+: o bicho entra pelo cenário (o do luta.py e o do ato.py), vai ao arquivo e volta
    from pessoas import padrao as _padrao, veste as _veste
    def pelo_cenario(d):                                    # o que o ato.luta_nova faz com cada pessoa do cenário que não tem "id"
        d = json.loads(json.dumps(d)); vs = d.pop('veste', {})
        return _veste(_padrao(d.pop('nome'), d.pop('nivel'), molde=d.pop('molde', 'guerreiro'), maestria=d.pop('maestria', None), atributos=d.pop('atributos', None), **d))
    certo = 0; esps = list(TB.ESPECIES)
    for e in esps:
        direto = ficha(B.bicho(e)); volta = ficha(pelo_cenario(B.bicho(e))); atalho = ficha(pelo_cenario(dict(nome=direto['nome'], nivel=0, bicho=e)))
        S = luta.nova(um(50, R, R)(), [pelo_cenario(x) for x in B.bando(e, random.Random(1))], quieto=True); luta.rodada(S); S = json.loads(json.dumps(S)); luta.corre(S)
        certo += json.dumps(direto, sort_keys=True) == json.dumps(volta, sort_keys=True) == json.dumps(atalho, sort_keys=True) and S['fim'] in ('A', 'B', 'ninguém', 'impasse', 'empate')
    try:
        with contextlib.redirect_stdout(io.StringIO()): ficha(B.bicho('lobo', tracos=['invisível'])); rec = 'aceitou'
    except SystemExit: rec = 'recusou'
    ok('B+ O CENÁRIO: o bicho que o bichos.bicho devolve passa pelo cenário da luta (o do ato.py também), pelo atalho {"bicho": espécie}, vai ao arquivo e volta; traço fora da lista é recusado',
       f'{certo} de {len(esps)} espécies com a mesma ficha pelos três caminhos e a luta inteira depois de ir ao arquivo; o traço inventado: {rec}', certo == len(esps) and rec == 'recusou')
    # B+: o agarrado fica onde está, e só se agarra quem está colado
    viol = pegou = 0; k = max(60, n // 5); caiu = ('CAI', 'MORRE', 'FOGE', 'sangra até cair', 'cai pelo veneno', 'morre no chão')
    for _ in range(k):
        S = luta.nova(varios(2, 30, 1, 1, pre='homem ')(), bi('urso', moral='firme')(), inicio='perto', lugar=dict(largura=1)); luta.corre(S); presos = set()
        for l in S['log']:
            if ' AGARRA ' in l: presos.add(l.split(' AGARRA ')[1].strip()); pegou += 1
            elif ' solta ' in l: presos.discard(l.split(' solta ')[1].strip())
            elif any(x in l for x in caiu): presos = set() if 'o urso' in l else {x for x in presos if x not in l}
            else: viol += any(l.startswith(f'  {x} avança') or l.startswith(f'  {x} recua') or l.endswith(f'troca de lugar com {x}') for x in presos)
    de_lanca = 0
    for _ in range(k):
        S = luta.nova(um(30, 1, 1, familia='lança')(), bi('urso')(), inicio='perto'); luta.corre(S); de_lanca += any(' AGARRA ' in l for l in S['log'])
    ok('B+ O AGARRADO: fica onde está (não anda, não recua, e quem vem atrás não troca de lugar com ele), e só é agarrado quem está colado: o lanceiro, que bate a duas casas, o urso não abraça',
       f'dois de espada contra o urso num corredor de um, em {k} lutas: {pegou} abraços, e o agarrado saiu do lugar {viol} vez(es); um de lança contra o urso: agarrado em {de_lanca} de {k} lutas', pegou >= k // 2 and viol == 0 and de_lanca == 0)
    # B+: quem ficou com o campo não testa a coragem (não há de quem fugir nem a quem se render)
    S = luta.nova(varios(2, 30, 1, 1, pre='vencedor ')(), bi('lobo')(), lugar=dict(sem_saida='A'), quieto=True); S['L'][2]['estado'] = 'morto'; S['L'][0]['pv'] = 1; mudou = 0; k = 200
    for i in range(k): S['r'] = i + 1; luta._moral(S, S['L'][0], 'metade_caiu' if i % 2 else 'golpe_terrivel'); S['L'][0]['testou'] = []; mudou += S['L'][0]['estado'] != 'pe' or S['L'][0]['abalado']
    S = luta.nova(varios(2, 30, 1, 1, pre='acuado ')(), bi('lobo')(), lugar=dict(sem_saida='A'), quieto=True); S['L'][0]['pv'] = 1; com = 0
    for i in range(k): S['r'] = i + 1; luta._moral(S, S['L'][0], 'golpe_terrivel'); com += S['L'][0]['estado'] != 'pe' or S['L'][0]['abalado']; S['L'][0]['abalado'] = False
    ok('B+ QUEM FICOU COM O CAMPO não testa a coragem: sem inimigo de pé, ninguém foge nem se rende (o mesmo homem, por um fio e sem saída, com o lobo morto e com o lobo de pé)',
       f'com o lobo morto, fraquejou em {mudou} de {k} sustos; com o lobo de pé, em {com} (e a um bicho não se rendeu: {"certo" if S["L"][0]["estado"] == "pe" else "RENDEU-SE"})', mudou == 0 and com >= k // 10 and S['L'][0]['estado'] == 'pe')
    # B+: quem foi posto no chão, ou ficou com a perna presa, não foge (a caça perdia a carcaça de um bicho que a mesa dizia caído)
    k = max(200, n); fug = 0; mal = 0; parou = 0; enc = 0
    for i in range(k):
        luta.semente(9000 + i); S = luta.nova(varios(1, 10, 0, 0)(), B.bando('corça', n=2), inicio='colado', surpresa='B'); luta.corre(S)
        for f in S['L']:
            if f['lado'] != 'B': continue
            fug += f['estado'] == 'fugiu'; mal += f['estado'] == 'fugiu' and bool(f['chao'] or f['preso']); enc += bool(f.get('encurralado'))
        parou += sum('NÃO SAI' in l for l in S['log'])
    luta.D = luta.Dados()
    ok('B+ QUEM NÃO ANDA NÃO FOGE: o bicho que vai ao chão ou fica com a perna presa não sai da luta (nem o que levou, de costas, o golpe que o derrubou); com a perna presa, luta como encurralado',
       f'{k} lutas do caçador de começo contra duas corças surpreendidas: {fug} corças fugiram, {mal} delas no chão ou com a perna presa; o golpe pelas costas segurou {parou}; ficaram encurraladas {enc}', fug > k // 4 and mal == 0 and parou >= 1)
    # B+: as espécies (o que o contrato pede da lista, e a API fixa que a caça usa)
    import tabelas_mundo as M
    API = ('nome', 'cat', 'grau', 'tamanho', 'bando', 'despojo', 'nucleo', 'habitat'); mal = []; ES = TB.ESPECIES
    for e, d in ES.items():
        if any(k not in d for k in API + ('nivel', 'instinto', 'atributos', 'armas', 'couro', 'tracos', 'moral', 'coragem', 'chefe')): mal.append(e); continue
        lo, hi = d['bando']; mat = [M.le_materia(b) for b in d['despojo'] if ':' in b]
        if not (d['grau'] in TB.GRAU_DA_CAT[d['cat']] and d['tamanho'] in TB.TAMANHOS and d['couro'] in TB.COUROS and d['armas'] and all(x in TB.ARMAS_CORPO for x in d['armas']) and all(t in TB.TRACOS for t in d['tracos'])
                and set(d['atributos']) == set(T.ATRIBUTOS) and d['instinto'] in T.MAESTRIAS and 1 <= lo <= hi and d['habitat'] and d['nucleo'] == d['chefe'] and (d['moral'] == 'firme') == d['chefe']
                and d['despojo'] and all(isinstance(q, int) and q >= 1 for q in d['despojo'].values()) and all(b in M.BENS for b in d['despojo'] if ':' not in b)
                and all(nome in M.MATERIAS and c == min(d['cat'], M.MATERIA_ATE) for nome, c in mat)): mal.append(e)
    cats = {d['cat'] for d in ES.values()}; graus = {d['grau'] for d in ES.values()}; chefes = {d['cat'] for d in ES.values() if d['chefe']}; usados = {t for d in ES.values() for t in d['tracos']}
    de_bando = sum(d['bando'][1] > 1 for d in ES.values()); sos_ = sum(d['bando'][1] == 1 and not d['chefe'] for d in ES.values())
    ok('B+ AS ESPÉCIES: de 12 a 16, do Comum ao Lendário, com o grau de F a S casado com a categoria; há bicho de bando, bicho sozinho e chefe (um núcleo para cada categoria, do Épico ao Lendário); '
       'os traços são uma lista fechada de 8 a 12, todos em uso; cada espécie tem a ficha inteira, e o despojo fala a língua comum dos bens (matéria da categoria dela, até o Raro)',
       f"{len(ES)} espécies, {len(ES) - len(mal)} com a ficha inteira; categorias: {', '.join(T.CATS[c] for c in sorted(cats))}; graus: {', '.join(g for g in TB.GRAUS if g in graus)}; "
       f"{de_bando} de bando, {sos_} que andam sós, {sum(d['chefe'] for d in ES.values())} chefes ({', '.join(T.CATS[c] for c in sorted(chefes))}); {len(TB.TRACOS)} traços, {len(usados)} em uso",
       not mal and 12 <= len(ES) <= 16 and cats == set(range(6)) and graus == set(TB.GRAUS) and de_bando and sos_ and {3, 4, 5} <= chefes and 8 <= len(TB.TRACOS) <= 12 and usados == set(TB.TRACOS))
    # B+: o bicho na luta DO MUNDO (ato.py luta), numa pasta de rascunho: a luta volta ao estado por um evento, e o bicho e o corpo dele não entram no mundo; as linhas para a MESA
    import os, shutil, tempfile
    import estado, ato, provas_mundo
    pasta = tempfile.mkdtemp(prefix='m10_bichos_'); antes = os.environ.get('MOTOR10_MUNDO'); os.environ['MOTOR10_MUNDO'] = pasta
    try:
        E = provas_mundo.vila(); E['lugares']['mata'] = dict(nome='a Mata de Prova', em='na Mata de Prova', tipo='ermo', estoque={}); conta = {e: 5 for e in ES}
        estado.aplica(E, 'gera', [['lugar', 'vila', 'vizinhos', 'poe', ['mata']], ['lugar', 'vila', 'bichos.ratazana', 'poe', 37]] + [['lugar', 'mata', f'bichos.{e}', 'poe', q] for e, q in conta.items()], texto='os bichos de prova')
        estado.grava(E); linhas = B.mesa(E); txt = '\n'.join(linhas); comuns_ = [d['nome'] for d in ES.values() if not d['chefe']]
        mesa_ok = len(linhas) == 2 and all(x in linhas[1] for x in comuns_) and txt.count('ratazana (') == 1 and not any(d['nome'] in txt for d in ES.values() if d['chefe']) and '37' not in txt and len(txt.encode()) <= 2000
        arq_c, arq_l = os.path.join(pasta, 'cen.json'), os.path.join(pasta, 'luta.json'); livro = sorted(E['itens']['itens']); gente_ = sorted(E['gente'])
        json.dump(dict(inicio='perto', A=[dict(id='eu', controla=True)], B=[dict(nome='a corça de prova', nivel=0, bicho='corça'), B.bicho('ratazana', nome='a ratazana de prova')]), open(arq_c, 'w', encoding='utf-8'), ensure_ascii=False)
        with contextlib.redirect_stdout(io.StringIO()):
            ato.luta_nova(E, arq_c, arq_l)
            for _ in range(80):
                E = estado.carrega(); S = json.load(open(arq_l, encoding='utf-8'))
                if S['fim']: break
                ato.luta_roda(E, arq_l, ['Aldric: atacar'] if S['L'][0]['estado'] == 'pe' else []); estado.grava(E)
        E = estado.carrega(); S = json.load(open(arq_l, encoding='utf-8')); f = S['L'][0]; p = E['gente']['eu']; bs = [x for x in S['L'] if x.get('bicho')]; corpos = [it for it in S['itens'].values() if it.get('tipo') == 'corpo']
        nl = sum(json.loads(x)['tipo'] == 'luta' for x in open(os.path.join(pasta, 'eventos.jsonl'), encoding='utf-8').read().splitlines())
        certo = (bool(S['fim']) and not estado.valida(E) and sorted(E['gente']) == gente_ and sorted(E['itens']['itens']) == livro and nl == 1 and len(bs) == 2 and not any(x.get('id') for x in bs)
                 and len(corpos) == 2 and all(it['dur'] == [1, 1] and not it.get('id') and not it.get('dono') for it in corpos) and E['turno']['lutas'][0]['fim'] == S['fim'] and E['lugares']['mata']['bichos'] == conta
                 and (p['estado'] == 'morto') == (f['estado'] == 'morto') and (p['estado'] == 'morto' or p['pv'] == max(1, f['pv'])) and len(p['feridas']) == len(f['feridas']))
        ok('B+ NO MUNDO: o personagem do mundo contra dois bichos pelo ato.py luta (o atalho e a pessoa do bichos.bicho): a luta volta ao estado por um evento só; o bicho não vira gente, o corpo não entra no Livro, '
           'e a contagem do ermo não muda sozinha (tirar o bicho da contagem é da caça); as linhas dos bichos para a MESA são curtas, sem a contagem e sem os chefes',
           f"a luta acabou ({S['fim']}, {S['r']} rodadas); o Aldric: {p['estado']}, PV {p['pv']}, {len(p['feridas'])} ferida(s); eventos de luta: {nl}; gente e Livro: {'os mesmos' if sorted(E['gente']) == gente_ and sorted(E['itens']['itens']) == livro else 'MUDARAM'}; "
           f"estado {'inteiro' if not estado.valida(E) else 'QUEBRADO'}; MESA: {len(comuns_)} espécies de dois lugares, cada uma dita uma vez, em {len(txt.encode())} bytes", certo and mesa_ok)
    finally:
        os.environ.pop('MOTOR10_MUNDO', None)
        if antes is not None: os.environ['MOTOR10_MUNDO'] = antes
        shutil.rmtree(pasta, ignore_errors=True)
    return out


# ---------- A MAGIA NA LUTA (etapa da magia, capítulo 11): os construtores de quem lança e as metas ----------
def mago(nome, nivel=50, foco=2, arm=None, amuleto='igual', m=None, sabe=('seta', 'prender', 'escudo', 'lança-de-fogo'), molde='mago', trad='arcano', forma='cajado', mao=2, **kw):
    """o lançador gerado: cajado (o foco de duas mãos, que é também a arma), couro, e o amuleto da categoria da armadura; a mão da tradição é a do nível"""
    arm = foco if arm is None else arm
    return veste(padrao(nome, nivel, molde=molde, maestria={'maça': mao, trad: T.maestria_tipica(nivel) if m is None else m}, feiticos=list(sabe), tradicao=trad, **kw),
                 armadura=('couro', arm), foco=(forma, foco), amuleto=arm if amuleto == 'igual' else amuleto)


def clerigo(nome, nivel=50, c=2, amuleto='igual', sabe=('cura',), m=None, **kw):
    """o clérigo na linha: maça, escudo e malha (a mão na arma um grau abaixo da da fé), o símbolo na mão do escudo"""
    mt = T.maestria_tipica(nivel)
    return veste(padrao(nome, nivel, molde='clérigo', maestria={'maça': max(0, mt - 2), 'fé': mt if m is None else m}, feiticos=list(sabe), tradicao='fé', **kw),
                 arma=('maça', c), armadura=('malha', c), escudo=c, foco=('símbolo', c), amuleto=c if amuleto == 'igual' else amuleto)


def druida(nome='o druida', nivel=50, foco=2, m=None, **kw): return mago(nome, nivel, foco, molde='druida', trad='verde', sabe=('raízes', 'espinho'), m=m, **kw)


def bruxa(nome='a bruxa', nivel=50, c=2, m=None, **kw):
    """a bruxa: o talismã na mão, uma adaga na outra, couro e amuleto"""
    return veste(padrao(nome, nivel, molde='bruxa', maestria={'adaga': 2, 'pacto': T.maestria_tipica(nivel) if m is None else m}, feiticos=['mau-olhado', 'sangria'], tradicao='pacto', **kw),
                 arma=('adaga', c), armadura=('couro', c), foco=('talismã', c), amuleto=c)


def gm(nome, nivel=50, arma=R, arm=R, esc=None, amuleto=None, familia='espada', **kw):
    """o guerreiro do banco (espada, malha e escudo), com ou sem amuleto"""
    return veste(padrao(nome, nivel, **kw), arma=(familia, arma), armadura=('malha', arm), escudo=arm if esc is None else esc, amuleto=amuleto)


def arqueira(nome, nivel=50, c=R, am=None): return veste(padrao(nome, nivel, molde='arqueiro'), arma=('arco', c), arma2=('adaga', c), armadura=('couro', c), amuleto=am)


def magia_luta(n):
    """A MAGIA NA LUTA: a seção G do projeto (conta/PROJETO.md), na parte da luta, e as metas da ordem de serviço. Nível 50, tudo Raro, quando não diz outra coisa;
    o guerreiro de espada, malha e escudo; o mago de cajado, couro e amuleto, que sabe seta, prender, escudo e lança de fogo. Devolve [(o que se mede, o que deu, passou?)]."""
    import itertools, json, statistics
    import magia as MG
    import tabelas_magia as TM
    import bichos as B
    from itens import item
    luta.semente(2026)                                      # a semente da magia: o bloco se repete igual rodando sozinho (provas.py N magia)
    out = []; ok = lambda nome, deu, passa: out.append((nome, deu, bool(passa)))
    n1 = max(1200, 2 * n)                                   # as faixas da magia são estreitas: o dobro de lutas (a luta de magia é curta)
    v = lambda a, b, **kw: luta.duelos(a, b, **{**dict(n=n1, inicio='perto'), **kw})[0]
    um_ = lambda f, **kw: (lambda: [f(**kw)] if callable(f) else [f])
    M = lambda **kw: (lambda: [mago('a maga', **kw)]); W = lambda **kw: (lambda: [gm('o guerreiro', **kw)])
    def conta(a, b, **kw):
        C = {}
        for _ in range(kw.pop('vezes', n)):
            S = luta.nova(a(), b(), quieto=True, **kw); luta.corre(S)
            for k, x in (S.get('conta') or {}).items(): C[k] = C.get(k, 0) + x
        return C
    # M1 a M7: o duelo, e a lei "o item decide"
    x = v(M(), lambda: [mago('o mago')])
    ok('M1 MAGO CONTRA MAGO (iguais, perto): de 44 a 56%', f'{x}%', 44 <= x <= 56)
    c = [v(M(), W(amuleto=R), inicio=i) for i in ('longe', 'perto', 'colado')]; s = [v(M(), W(), inicio=i) for i in ('longe', 'perto', 'colado')]
    ok('M2 MAGO CONTRA O GUERREIRO COM AMULETO: de longe 28 a 45%, de perto 12 a 28%, colado 4 a 16% (o mago é um arqueiro que gasta Mana)', f'{c[0]}%, {c[1]}% e {c[2]}%', 28 <= c[0] <= 45 and 12 <= c[1] <= 28 and 4 <= c[2] <= 16)
    ok('M3 SEM AMULETO A MAGIA PESA: contra o guerreiro sem amuleto (a armadura guarda 0,6) o mago ganha de 15 a 35 pontos, de longe e de perto (custa como lutar sem elmo)',
       f'de longe {s[0]}% (+{s[0] - c[0]}), de perto {s[1]}% (+{s[1] - c[1]}), colado {s[2]}% (+{s[2] - c[2]})', 15 <= s[0] - c[0] <= 35 and 15 <= s[1] - c[1] <= 35)
    a, b = v(M(foco=R + 1, arm=R), W(amuleto=R), inicio='longe'), v(M(foco=R + 1, arm=R), W(amuleto=R))
    ok('M4 O FOCO DECIDE: o foco uma categoria acima contra o guerreiro igual com amuleto: de longe 85 a 100%, de perto 65 a 90%', f'{a}% e {b}%', 85 <= a <= 100 and 65 <= b <= 90)
    a, b = v(M(), W(amuleto=R + 1), inicio='longe'), v(M(), W(arma=R + 1, arm=R + 1, amuleto=R + 1, atributos={'Vontade': 100}), inicio='longe')
    ok('M5 O AMULETO É A ARMADURA DA MAGIA: contra o amuleto uma acima, de 2 a 18%; contra o conjunto uma acima (com Vontade para sustentar as cinco peças), de 0 a 8%', f'{a}% e {b}%', 2 <= a <= 18 and 0 <= b <= 8)
    a, b = v(M(foco=R + 2, arm=R), W(nivel=500, amuleto=R), inicio='longe'), v(M(foco=R + 2, arm=R), W(nivel=500, amuleto=R))
    ok('M6 A CHANCE DO PEQUENO: o nível 50 de foco duas acima contra o nível 500 com amuleto: de longe 65 a 92%, de perto 15 a 40%', f'{a}% e {b}%', 65 <= a <= 92 and 15 <= b <= 40)
    a = v(M(foco=R + 1, arm=R), W(nivel=500, amuleto=R), inicio='longe')
    ok('M7 ... e com o foco uma acima, de longe: de 5 a 30%', f'{a}%', 5 <= a <= 30)
    # M8: o tamanho de cada feitiço num igual com amuleto (a conta exata do dado, sem o crítico)
    def tam(lanc, alvo, k, dado=None):
        S = luta.nova([lanc], [alvo], quieto=True); f, e = S['L']; _, cc, vz, _, fm = MG.conj(S, f, k); g, _ = MG.guarda(S, e)
        q, fc = map(int, (dado or TM.FEITICOS[k]['dado']).split('d')); ds = sorted(int(sum(t) * TM.K * T.MULT[cc] * vz / g * fm) for t in itertools.product(range(1, fc + 1), repeat=q))
        return statistics.median(ds) / e['pvmax'], max(ds), e['pvmax']
    lin = []; pior = 0; mata = []
    for k, lanc in (('seta', mago('a')), ('lança-de-fogo', mago('a')), ('raio', mago('a')), ('bola-de-fogo', mago('a')), ('espinho', druida()), ('sangria', bruxa()), ('castigo', clerigo('c', sabe=('castigo',)))):
        for alvo in (gm('g', amuleto=R), json.loads(json.dumps(lanc)) | {'nome': 'o gêmeo'}):
            md, mx, pv = tam(json.loads(json.dumps(lanc)), alvo, k)
            if alvo['nome'] == 'g': lin.append(f"{T.nome_feitico(k)} {md:.0%}"); pior = max(pior, md if k != 'seta' else 0)
            if mx >= pv: mata.append(f"{T.nome_feitico(k)} em {alvo['nome']} ({mx} de {pv})")
    sm = tam(mago('a'), gm('g', amuleto=R), 'seta')[0]
    ok('M8 NENHUM FEITIÇO MATA DE PV CHEIO SEM CRÍTICO ENTRE IGUAIS (no guerreiro com amuleto e no gêmeo de quem lança); na mediana, nenhum tira mais de 45% do PV do guerreiro, e a seta até 20%',
       'na mediana: ' + ', '.join(lin) + ('; nenhum mata de PV cheio' if not mata else '; MATA: ' + ', '.join(mata)), not mata and pior <= 0.45 and sm <= 0.20)
    # M9: a Mana (só de seta, contra um alvo que não morre)
    def seca(volta):
        antes = TM.MANA_LUTA; TM.MANA_LUTA = volta; sec = []; tiros = []
        try:
            for _ in range(max(100, n // 3)):
                S = luta.nova([mago('m', sabe=('seta',))], [gm('o saco', nivel=500, arma=0, arm=4, amuleto=4)], inicio=30, quieto=True); f, g = S['L']; g['preso'] = True; r0 = None
                for r in range(1, 21):
                    luta.rodada(S); g['x'] = f['x'] + 6
                    if r0 is None and f['mana'] < 2: r0 = r
                sec.append(r0 or 21); tiros.append((S.get('conta') or {}).get('seta_lances', 0))
        finally: TM.MANA_LUTA = antes
        return statistics.median(sec), statistics.mean(tiros)
    (r1, t1), (r0, t0) = seca(1), seca(0)
    ok('M9 A MANA É O FÔLEGO DA MAGIA: só de seta, sem parar, seca entre a rodada 6 e a 10; a volta de 1 por turno rende de 25 a 50% de setas a mais na luta (até 20 rodadas; a luta acaba no impasse quando o alvo não sente)',
       f'seca na rodada {r1:g} (sem a volta, na {r0:g}); {t1:.1f} setas contra {t0:.1f} ({t1 / t0 - 1:+.0%})', 6 <= r1 <= 10 and 0.25 <= t1 / t0 - 1 <= 0.50)
    # M10 a M13: o grupo (nível 40, tudo Incomum, todos com amuleto; cinco contra cinco, perto)
    G = lambda pre, k, am=1, **kw: [gm(f'{pre}{i}', nivel=40, arma=1, arm=1, amuleto=am, **kw) for i in range(1, k + 1)]
    M1 = lambda sabe: mago('o mago', nivel=40, foco=1, linha='trás', sabe=sabe, m=4)
    base = v(lambda: G('a', 5), lambda: G('b', 5)); sem = v(lambda: G('a', 4) + [M1(('seta', 'lança-de-fogo', 'prender'))], lambda: G('b', 5), n=2 * n1)
    com = v(lambda: G('a', 4) + [M1(('seta', 'bola-de-fogo'))], lambda: G('b', 5)); nu = v(lambda: G('a', 4) + [M1(('seta', 'bola-de-fogo'))], lambda: G('b', 5, am=None))
    ok('M10 O MAGO NO GRUPO, no lugar de um guerreiro: sem área 40 a 55%; com a bola de fogo contra cinco com amuleto 52 a 70%; contra cinco sem amuleto 75 a 92%',
       f'cinco contra cinco: {base}%; sem área {sem}%; com área {com}%; com área contra os sem amuleto {nu}%', 40 <= sem <= 55 and 52 <= com <= 70 and 75 <= nu <= 92)
    x = v(lambda: G('a', 4) + [M1(('seta', 'bola-de-fogo', 'prender'))], lambda: G('b', 5), lugar=dict(largura=2))
    ok('M11 ... e no corredor de dois (seta, bola de fogo, prender): de 50 a 68%', f'{x}%', 50 <= x <= 68)
    cl = lambda **kw: clerigo('o clérigo', nivel=40, c=1, **kw); mx_c = (lambda p: T.mana_max(p['atributos']['Afinidade'], p['atributos']['Vontade'], 4))(cl())
    a, b = v(lambda: G('a', 4) + [cl()], lambda: G('b', 5), n=2 * n1), v(lambda: G('a', 4) + [cl()], lambda: G('b', 5), lugar=dict(largura=2))
    bz = v(lambda: G('a', 4, benzido=True) + [cl(mana=mx_c - 8)], lambda: G('b', 5), n=2 * n1)
    ok('M12 O CLÉRIGO NA LINHA (maça, escudo, malha; cura), no lugar de um guerreiro: em campo 42 a 58%, no corredor 48 a 64%; benzendo os quatro antes da luta (8 de Mana a menos), de 5 a 14 pontos a mais',
       f'{a}%, {b}%; benzidos {bz}% ({bz - a:+d})', 42 <= a <= 58 and 48 <= b <= 64 and 5 <= bz - a <= 14)
    a, b = v(lambda: G('a', 4) + [druida(nivel=40, foco=1, m=4, linha='trás')], lambda: G('b', 5)), v(lambda: G('a', 4) + [bruxa(nivel=40, c=1, m=4, linha='trás')], lambda: G('b', 5))
    ok('M13 O DRUIDA (cajado; raízes, espinho), atrás, no lugar de um guerreiro: de 45 a 62%', f'{a}% (cinco contra cinco: {base}%)', 45 <= a <= 62)
    ok('M13 A BRUXA (talismã e adaga; mau-olhado, sangria), atrás, no lugar de um guerreiro: de 42 a 58% (o projeto a mediu com um cajado que valia inteiro; o cajado não é foco do pacto)',
       f'{b}% (cinco contra cinco: {base}%)', 42 <= b <= 58)
    x = v(lambda: [bruxa()], W(amuleto=R), inicio='longe')
    ok('M14 A BRUXA SOZINHA contra o guerreiro com amuleto, de longe: de 5 a 20% (péssima sozinha)', f'{x}%', 5 <= x <= 20)
    # M15 e M16: o feitiço longo sob flecha (perde-se pela concentração que falha e pelo corte: no chão ou atordoado, sem teste)
    nn = max(6000, 10 * n)                                  # o efeito do guarda é pequeno (uns 4 pontos): a amostra tem de ser grande
    def longo(a, b, vezes=nn):
        C = conta(a, b, vezes=vezes, inicio='longe'); return (C.get('conc_falhas', 0) + C.get('conc_cortes', 0)) / max(1, C.get('longos', 0)), C.get('conc_falhas', 0) / max(1, C.get('conc_testes', 0))
    rm = lambda **kw: mago('a maga', sabe=('raio',), m=6, **kw)
    (p1, f1), (p2, f2), (p3, _) = longo(lambda: [rm()], lambda: [arqueira('q1', am=R)]), longo(lambda: [rm()], lambda: [arqueira('q1', am=R), arqueira('q2', am=R)], 2 * nn), \
        longo(lambda: [rm(linha='trás'), gm('o guarda', guarda='a maga', moral='firme')], lambda: [arqueira('q1', am=R), arqueira('q2', am=R)], 2 * nn)
    ok('M15 O FEITIÇO LONGO SOB FLECHA (o raio: sai no começo do turno seguinte; quem canaliza e apanha testa a concentração): sob uma arqueira se perdem de 15 a 35%, sob duas de 25 a 50%',
       f'{p1:.0%} e {p2:.0%} (cada teste de concentração falha {f1:.0%} e {f2:.0%})', 0.15 <= p1 <= 0.35 and 0.25 <= p2 <= 0.50)
    ok('M16 ... e um guarda de escudo na frente de quem canaliza tira 3 pontos ou mais', f'{p3:.0%} contra {p2:.0%} ({100 * (p3 - p2):+.1f} pontos)', p2 - p3 >= 0.03)
    # M17 e M21: o dado do lance (a conta exata e o dado de verdade)
    q = 20000; r_c = sum(MG.jogada(0)['falha'] for _ in range(q)) / q; r_f = sum(MG.jogada(0, True)['falha'] for _ in range(q)) / q
    ok('M17 O RETROCHOQUE: no lance comum (dois 1) de 0,1 a 0,5% dos lances; no forçado (basta um 1) de 8 a 12%', f'{r_c:.2%} e {r_f:.2%} em {q} lances de cada', 0.001 <= r_c <= 0.005 and 0.08 <= r_f <= 0.12)
    S = luta.nova([mago('m', m=6)], [gm('g', amuleto=R)], quieto=True); f, e = S['L']; cj = MG.conj(S, f, 'prender')[0]; fz = MG.firmeza(S, e); e['calejo'] = 2; fz2 = MG.firmeza(S, e)
    pg = lambda alvo: sum(1 for _ in range(2000) if (lambda j: j['total'] >= alvo or j['crit'])(MG.jogada(cj))) / 2000
    ok('M21 O CONTROLE: o mago Mestre de foco Raro pega (prender) no guerreiro igual com amuleto de 55 a 75% das vezes; calejado duas vezes (+8 na Firmeza), de 25 a 40%',
       f'Conjuração {cj:+g} contra a Firmeza {fz:g}: a conta dá {luta.chance(fz - cj):.0%}, o dado {pg(fz):.0%}; calejado ({fz2:g}): {luta.chance(fz2 - cj):.0%} e {pg(fz2):.0%}',
       0.55 <= luta.chance(fz - cj) <= 0.75 and 0.25 <= luta.chance(fz2 - cj) <= 0.40 and abs(pg(fz) - luta.chance(fz - cj)) < 0.05)
    # M18 e M19: a multidão e os bichos
    k8, k12 = [v(lambda: [mago('a maga', sabe=('seta', 'bola-de-fogo', 'escudo', 'prender'))], lambda: [gm(f's{i}', nivel=20, arma=0, arm=0) for i in range(k)], inicio='longe', n=max(120, n // 4)) for k in (8, 12)]
    ok('M18 A MULTIDÃO: um mago Raro (seta, bola de fogo, prender, escudo) contra 8 e contra 12 soldados Comuns de nível 20, sem amuleto, de longe: de 55 a 85% e de 35 a 70% (morre cercado)', f'{k8}% e {k12}%', 55 <= k8 <= 85 and 35 <= k12 <= 70)
    a, b, t = v(M(), lambda: [B.bicho('pantera')], inicio='longe'), v(M(), lambda: [B.bicho('pantera')]), v(M(), lambda: [B.bicho('trasgo')], inicio='longe')
    ok('M19 O MAGO NÃO É CAÇADOR: contra a pantera, de longe 35 a 60% e de perto 0 a 12% (o bote o mata); contra o trasgo, de longe, 30 a 55%', f'{a}%, {b}% e {t}%', 35 <= a <= 60 and 0 <= b <= 12 and 30 <= t <= 55)
    # M20: os nove traços novos, cada um com ele e sem ele
    n2 = max(1000, 2 * n); par = lambda a1, b1, a2, b2, **kw: (luta.duelos(a1, b1, **{**dict(n=n2), **kw})[0], luta.duelos(a2, b2, **{**dict(n=n2), **kw})[0])
    pan = lambda *tr, **kw: (lambda: [B.bicho('pantera', tracos=['bote'] + list(tr), **kw)])
    tr = {}
    tr['resiste'] = par(M(), pan('resiste'), M(), pan(), inicio='longe')
    tr['imaterial'] = par(W(), pan('imaterial'), W(), pan(), inicio='perto')
    tr['lança'] = par(W(), pan('lança', feiticos=['seta']), W(), pan(), inicio='longe')
    tr['sem vida'] = par(W(nivel=30, arma=1, arm=1), lambda: B.bando('lobo', n=4, tracos=['matilha', 'sem vida']), W(nivel=30, arma=1, arm=1), lambda: B.bando('lobo', n=4), inicio='perto')
    tr['ossos'] = par(W(), pan('ossos'), W(), pan(), inicio='perto')
    tr['dreno'] = par(lambda: [gm(f'g{i}') for i in range(6)], lambda: [B.bicho('serpe', tracos=['sopro', 'veneno', 'dreno'])], lambda: [gm(f'g{i}') for i in range(6)], lambda: [B.bicho('serpe')], inicio='perto', n=max(400, n))
    tr['ardente'] = par(W(), pan('ardente'), W(), pan(), inicio='perto')
    tr['noturno'] = par(W(), pan('noturno'), W(), pan(), inicio='perto', tempo=['escuro'])
    mal = sum(1 for _ in range(n2) if (lambda S: (luta.corre(S), S['L'][0].get('maldicoes_postas'))[1])(luta.nova(W()(), pan('amaldiçoa')(), inicio='perto', quieto=True)))
    tr['amaldiçoa'] = (round(100 * mal / n2), 0)
    ok('M20 OS NOVE TRAÇOS NOVOS, cada um com ele e sem ele: 8 pontos ou mais (resiste: o mago contra a pantera, de longe; imaterial, ossos, ardente, noturno no escuro: o guerreiro de espada contra a pantera; '
       'lança: a pantera que lança seta, de longe; sem vida: quatro lobos que não fogem contra o nível 30; dreno: a serpe contra seis guerreiros (o sopro é golpe do corpo: drena de cada um que pega); amaldiçoa: em quantas lutas o guerreiro sai com a maldição)',
       ' · '.join(f"{k} {a:g}% contra {b:g}%" for k, (a, b) in tr.items()), all(abs(a - b) >= 8 for a, b in tr.values()))
    # P1 a P4: a poção e o veneno de lâmina (o duelo de gêmeos com amuleto; quem leva bebe abaixo de metade do PV)
    n3 = max(1200, 2 * n); g = lambda **kw: (lambda: [gm('a', amuleto=R, **kw)]); w2 = lambda **kw: (lambda: [gm('b', amuleto=R, **kw)])
    p = [luta.duelos(g(carga={f'cura:{R}': k}), w2(), n=n3)[0] for k in (1, 2, 3)]
    ok('P1 A POÇÃO AJUDA E NÃO DECIDE: uma poção de cura da categoria da luta, 52 a 62%; duas, 55 a 68%; a terceira não soma mais de 3 pontos (o corpo aguenta Vigor ÷ 30 por dia: quem não comanda o jogador não bebe além disso)',
       f'{p[0]}%, {p[1]}% e {p[2]}%', 52 <= p[0] <= 62 and 55 <= p[1] <= 68 and p[2] - p[1] <= 3)
    a, b = luta.duelos(g(carga={f'cura:{R - 1}': 2}), w2(), n=max(3000, 5 * n))[0], luta.duelos(g(elixires=[dict(id='e1', pocao='cura', cat=R + 1, nome='elixir de cura Épico')]), w2(), n=n3)[0]
    ok('P2 A CURA SEGUE A LEI AO CONTRÁRIO: duas poções uma categoria abaixo da ferida, 47 a 53%; um elixir uma acima, 55 a 68%', f'{a}% e {b}%', 47 <= a <= 53 and 55 <= b <= 68)
    ven = lambda: item('arma', R, familia='espada', veneno=dict(cat=R, ate=10 ** 9))
    gv = lambda **kw: (lambda: [veste(padrao('a', 50, **kw), arma=ven(), armadura=('malha', R), escudo=R, amuleto=R)])
    a = luta.duelos(gv(), w2(), n=n3)[0]
    ok('P3 O VENENO DE LÂMINA: uma dose da categoria (a primeira vez que a arma tira sangue: um quarto do golpe por 3 rodadas e −2 no acerto), de 52 a 62%', f'{a}%', 52 <= a <= 62)
    a, b = luta.duelos(gv(carga={f'cura:{R}': 2}), w2(), n=n3)[0], luta.duelos(g(carga={f'cura:{R}': 2}), w2(arma=R + 1), n=n3)[0]
    ok('P4 O FRASCO NÃO VENCE A PEÇA: veneno e duas poções, até 75%; duas poções contra o gêmeo com a arma uma acima, até 12%', f'{a}% e {b}%', a <= 75 and b <= 12)
    # P9: o limite do corpo e o teto da cura (prova posta à mão)
    enj = 0; teto_ok = True; falhou_beber = 0
    for _ in range(200):
        S = luta.nova([gm('a', amuleto=R, carga={f'cura:{R}': 4})], [gm('b')], quieto=True); f = S['L'][0]; f['pv'] = 20; f['funda'] = 0; lim = T.doses_dia(f['atributos']['Vigor'])
        for i in range(4): MG.bebe(S, f, f'cura:{R}')
        MG.cura(S, f, '1d8', 5); enj += bool(MG.ve(f, 'enjoo')); teto_ok &= f['curado'] <= int(f['pvmax'] * T.CURA_TETO) and f['doses'] == 4 and not f['carga']
    ok('P9 O LIMITE DO CORPO E O TETO DA CURA: além de Vigor ÷ 30 poções no dia, cada uma pede Vigor (falhou: não faz nada, e enjoa); poção e feitiço somados nunca devolvem mais que metade do PV no dia',
       f'o guerreiro aguenta {lim} por dia; bebendo 4, enjoou em {enj} de 200; o teto {"sempre segurou" if teto_ok else "PASSOU"}', 0 < enj < 200 and teto_ok)
    # E1 a E3: a peça encantada (um degrau abaixo, uma vez por luta, ocupa sintonia)
    enc = lambda k, c=R, grau=2: item('arma', c, familia='espada', encantos=[dict(feitico=k, grau=grau, feito_por=None, dia=1, gasto=None)])
    ge = lambda k, c=R, arm=R, **kw: (lambda: [veste(padrao('a', 50, **kw), arma=enc(k, c), armadura=('malha', arm), escudo=arm, amuleto=arm)])
    a, b = luta.duelos(ge('seta'), w2(), n=n3)[0], luta.duelos(ge('seta'), w2(), n=n3, inicio='longe')[0]
    ok('E1 O ENCANTO NÃO DECIDE NUM IGUAL: a espada Rara com seta gravada contra o gêmeo, de perto e de longe: de 46 a 56%', f'{a}% e {b}%', 46 <= a <= 56 and 46 <= b <= 56)
    s8 = lambda: [gm(f's{i}', nivel=30, arma=1, arm=1, amuleto=1) for i in range(8)]
    a, b = luta.duelos(lambda: [gm('a', amuleto=R, moral='firme')], s8, n=2 * n3, inicio='longe')[0], luta.duelos(ge('bola-de-fogo', moral='firme'), s8, n=2 * n3, inicio='longe')[0]
    ok('E2 ... MAS AJUDA CONTRA A MULTIDÃO DE BAIXO: a bola de fogo gravada, uma vez, contra oito de uma categoria abaixo: de 5 a 15 pontos a mais', f'{a}% e {b}% ({b - a:+d})', 5 <= b - a <= 15)
    pecas = lambda vont: ficha(veste(padrao('x', 50, atributos={'Vontade': vont}), arma=enc('prender'), armadura=('malha', 3), escudo=3))
    dorme, acorda = pecas(25), pecas(80)
    ver = ficha(veste(padrao('y', 50, atributos={'Vontade': 25}), arma=enc('prender', 0), armadura=('malha', 0), escudo=item('escudo', 0, encantos=[dict(feitico='escudo', grau=1, feito_por=None, dia=1, gasto=None)])))
    S = luta.nova([veste(padrao('z', 50, atributos={'Vontade': 65}, controla=True), arma=enc('prender'), armadura=('malha', R), escudo=R)], [gm('w')], inicio='perto', quieto=True); f = S['L'][0]
    f['_restam'] = 2; a1 = MG.decide(S, f, MG.ordem(S, f, 'usar', []), False); MG.faz(S, f, a1); uso = not f['encantos'][0]['carregado']
    try: MG.ordem(S, f, 'usar', []); de_novo = 'aceitou'
    except SystemExit: de_novo = 'recusou'
    ok('E3 A PEÇA ENCANTADA OCUPA SINTONIA E SAI UMA VEZ POR LUTA: com Vontade 25 (uma peça desperta) a espada encantada, atrás do escudo e da armadura Épicos, dorme e não solta; com Vontade 80, solta; '
       'duas peças Comuns encantadas, com Vontade 25: uma dorme; o encanto solto não sai de novo na mesma luta',
       f"Vontade 25: a espada {'dorme' if dorme['encantos'][0]['dorme'] else 'NÃO DORME'}; 80: {'desperta' if not acorda['encantos'][0]['dorme'] else 'DORME'}; das Comuns encantadas, {'uma dorme' if len(ver['dormem']) == 1 else 'NENHUMA DORME'}; "
       f"o encanto {'saiu' if uso else 'NÃO SAIU'}, e pedir de novo {de_novo}", dorme['encantos'][0]['dorme'] and not acorda['encantos'][0]['dorme'] and len(ver['dormem']) == 1 and uso and de_novo == 'recusou')
    # AS FASES DO CHEFE, A ORDEM DE QUEM O JOGADOR COMANDA, A LUTA SEM MAGIA, E A LUTA QUE VOLTA AO ESTADO
    fs = [dict(abaixo=0.75, diz='urra, e o pelo pega fogo', ganha=['ardente'], brado=True, ergue=2, feiticos=['seta'], mana=6)]; viu = dict(fase=0, para=0, erg=0, sem_id=True, morto=True, ard=True)
    for _ in range(40):
        S = luta.nova([gm(f'g{i}') for i in range(3)], [B.bicho('urso', nome='o urso velho', fases=fs, lider=True, moral='firme', cat=R)] + B.bando('lobo', n=3), inicio='perto', quieto=True)
        while luta.corre(S, interativo=True) == 'parada':
            viu['para'] += any('mudou' in x for x in S['paradas']); S = json.loads(json.dumps(S))
        viu['para'] += any('mudou' in x for x in S['paradas'])          # (a fase da última rodada, a que acabou a luta)
        u = luta.por_nome(S, 'o urso velho'); C = S.get('conta') or {}; viu['fase'] += C.get('fases', 0); viu['erg'] += C.get('erguidos', 0)
        if u.get('fase'): viu['ard'] &= 'ardente' in u['tracos'] and 'seta' in u['feiticos']
        for x in S['L']:
            if 'morto que anda' in x['nome']: viu['sem_id'] &= not x.get('id') and 'sem vida' in x['tracos'] and x['lado'] == 'B'; viu['morto'] &= luta.por_nome(S, x['nome'].split(', morto')[0])['estado'] == 'morto'
    ok('AS FASES DO CHEFE: ao cruzar o limiar do PV, o chefe muda uma vez (ganha o traço, aprende o feitiço, recobra a Mana, dá o brado e ergue os mortos como "sem vida" do lado dele), e a luta para e pergunta; o morto erguido é outro lutador, sem registro no mundo, e o morto segue morto',
       f"em 40 lutas: {viu['fase']} fases, {viu['para']} paradas, {viu['erg']} mortos erguidos; o chefe {'mudou como diz' if viu['ard'] else 'NÃO MUDOU'}; os erguidos {'sem id e sem vida' if viu['sem_id'] else 'ERRADOS'}, o morto {'segue morto' if viu['morto'] else 'VOLTOU'}",
       0 < viu['fase'] <= 40 and viu['para'] == viu['fase'] and viu['erg'] > 0 and viu['ard'] and viu['sem_id'] and viu['morto'])
    heroi = lambda: veste(padrao('Lia', 120, molde='mago', maestria={'espada': 4, 'arcano': 6}, feiticos=['seta', 'escudo', 'bola-de-fogo', 'luz'], tradicao='arcano', carga={'cura:2': 2}, controla=True),
                          arma=enc('prender'), armadura=('malha', 3), foco=('varinha', R), amuleto=R)
    S = luta.nova([heroi()], [gm('o bandido', amuleto=R), gm('o outro')], inicio='longe', tempo=['escuro'], quieto=True); luta.corre(S, interativo=True); recusas = 0
    for ruim in ('Lia: lancar raio', 'Lia: lancar seta em Lia', 'Lia: beber veneno', 'Lia: beber antídoto', 'Lia: lancar seta casa 3', 'Lia: lancar escudo em o bandido', 'Lia: usar escudo', 'Lia: lancar nada'):
        try: luta.ordem(S, ruim)
        except SystemExit: recusas += 1
    luta.ordem(S, 'Lia: lancar luz'); luta.corre(S, interativo=True); luz = 'escuro' not in S['tempo'] and 'luz' in (S.get('campo') or {}); volta = 'Lia' not in S['ordens']
    luta.ordem(S, 'Lia: lancar seta em o bandido sempre'); f = S['L'][0]; m0 = f['mana']; luta.corre(S, interativo=True); f = S['L'][0]; sempre = S['ordens'].get('Lia', {}).get('sempre') or f['estado'] != 'pe' or f['mana'] < 2
    ok('A ORDEM DE QUEM O JOGADOR COMANDA (lancar, beber, usar) é conferida antes de qualquer dado; a de uma vez volta à ordem de antes; a de "sempre" segue até a Mana acabar ou o alvo cair; quem o jogador comanda não lança sozinho',
       f"{recusas} de 8 ordens tortas recusadas; a luz {'tirou o escuro' if luz else 'NÃO TIROU'} e a ordem {'voltou' if volta else 'FICOU'}; a seta de sempre {'seguiu' if sempre else 'PAROU'} (Mana {m0} → {f['mana']})", recusas == 8 and luz and volta and sempre)
    S = luta.nova([gm('a')], [gm('b')], quieto=True); luta.corre(S)
    ok('A PESSOA COMUM É A DE HOJE: a luta em que ninguém traz magia não liga a magia (nenhum campo de magia no lutador; os 80 do banco seguem iguais, e com semente fixa a luta é a mesma de antes)',
       'a luta de gêmeos sem nada: ' + ('sem magia' if not S.get('magia') and not any('est' in f or 'canaliza' in f for f in S['L']) else 'LIGOU A MAGIA'), not S.get('magia') and not any('est' in f or 'canaliza' in f for f in S['L']))
    ok(*_no_mundo())
    return out


def _no_mundo():
    """a luta de magia do mundo (ato.py luta, numa pasta de rascunho): a maga do mundo chega ferida (40% do PV) e lança e bebe sozinha (o jogador não a comanda nesta prova),
    contra um salteador fraco; a luta volta ao estado por um evento: a Mana que sobrou, a poção bebida, o desgaste do foco; o estado fica inteiro. Três lutas, com os dados
    delas (semente 1 a 3, à parte das outras provas): em toda luta em que a maga vive a volta é conferida inteira, e ela tem de viver e beber em pelo menos uma."""
    import contextlib, io, json, os, shutil, tempfile
    import estado, ato, provas_mundo
    from itens import item
    antes = os.environ.get('MOTOR10_MUNDO'); D0 = luta.D; vidas = []
    try:
        for sem in (1, 2, 3):
            pasta = tempfile.mkdtemp(prefix='m10_magia_'); os.environ['MOTOR10_MUNDO'] = pasta; luta.semente(sem)
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    E = provas_mundo.vila(); estado.aplica(E, 'gera', [['item', 'nasce', item('foco', R, forma='cajado', dono='eu')], ['item', 'nasce', item('amuleto', R, dono='eu')], ['pessoa', 'eu', 'carga.cura:2', 'soma', 2]], texto='a maga se arma')
                    novos = sorted(i for i, it in E['itens']['itens'].items() if it.get('dono') == 'eu' and it['tipo'] in ('foco', 'amuleto'))
                    estado.aplica(E, 'estudar', [['pessoa', 'eu', 'maestria.arcano', 'poe', 6], ['pessoa', 'eu', 'feitico', 'aprende', 'seta'], ['pessoa', 'eu', 'feitico', 'aprende', 'lança-de-fogo'], ['pessoa', 'eu', 'tradicao', 'poe', 'arcano']], texto='a maga estuda')
                    estado.aplica(E, 'gera', [['item', i, 'uso', 'poe', 'foco' if E['itens']['itens'][i]['tipo'] == 'foco' else 'pescoco'] for i in novos], texto='a maga se veste')
                    p = E['gente']['eu']; estado.aplica(E, 'mestre', [['pessoa', 'eu', 'pv', 'soma', int(estado.pv_max(p) * 0.4) - p['pv']]], texto='a maga chega ferida')
                    estado.grava(E); p = E['gente']['eu']; mana0 = estado.mana(p); dur0 = {i: E['itens']['itens'][i]['dur'][0] for i in novos}
                    arq_c, arq_l = os.path.join(pasta, 'cen.json'), os.path.join(pasta, 'luta.json')
                    json.dump(dict(inicio='longe', A=[dict(id='eu')], B=[dict(nome='o salteador', nivel=10, veste=dict(arma=['espada', 'Comum'], armadura=['couro', 'Comum']))]), open(arq_c, 'w', encoding='utf-8'), ensure_ascii=False)
                    ato.luta_nova(E, arq_c, arq_l)
                    for _ in range(60):
                        E = estado.carrega(); S = json.load(open(arq_l, encoding='utf-8'))
                        if S['fim']: break
                        ato.luta_roda(E, arq_l, []); estado.grava(E)
                E = estado.carrega(); S = json.load(open(arq_l, encoding='utf-8')); f = S['L'][0]; p = E['gente']['eu']
                nl = sum(json.loads(x)['tipo'] == 'luta' for x in open(os.path.join(pasta, 'eventos.jsonl'), encoding='utf-8').read().splitlines())
                bebeu = (f.get('gastou') or {}).get('cura:2', 0); foco = [i for i in novos if E['itens']['itens'][i]['tipo'] == 'foco'][0]; vivo = p['estado'] == 'vivo'
                volta = (estado.mana(p) == max(0, min(estado.mana_max(p), f['mana'])) < mana0 and p.get('carga', {}).get('cura:2', 0) == 2 - bebeu and E['itens']['itens'][foco]['dur'][0] == dur0[foco] - 1) if vivo else None
                vidas.append(dict(fim=S['fim'], r=S['r'], vivo=vivo, bebeu=bebeu, mana=(mana0, estado.mana(p)), foco=(dur0[foco], E['itens']['itens'][foco]['dur'][0]), nl=nl, magia=bool(S.get('magia')),
                                  volta=volta, erro=estado.valida(E)))
            finally: shutil.rmtree(pasta, ignore_errors=True)
    finally:
        luta.D = D0; os.environ.pop('MOTOR10_MUNDO', None)
        if antes is not None: os.environ['MOTOR10_MUNDO'] = antes
    certo = (all(v['fim'] and v['nl'] == 1 and v['magia'] and not v['erro'] and (v['volta'] or not v['vivo']) for v in vidas) and any(v['vivo'] and v['bebeu'] >= 1 and v['volta'] for v in vidas))
    diz = '; '.join(f"luta {k + 1}: acabou ({v['fim']}, {v['r']} rodadas), a maga {'viva' if v['vivo'] else 'MORTA'}, Mana {v['mana'][0]} → {v['mana'][1]}, bebeu {v['bebeu']} poção(ões), o foco {v['foco'][0]} → {v['foco'][1]}"
                    + (f", a volta {'confere' if v['volta'] else 'NÃO CONFERE'}" if v['vivo'] else '') + f", {v['nl']} evento de luta, estado {'inteiro' if not v['erro'] else 'QUEBRADO: ' + v['erro'][0]}" for k, v in enumerate(vidas))
    return ('A LUTA DE MAGIA VOLTA AO ESTADO (ato.py luta, no mundo de prova): a maga do mundo, ferida, lança e bebe sozinha, e a luta volta por um evento só: a Mana que sobrou, a poção bebida, o foco que gastou; o estado fica inteiro; '
            'a volta é conferida em toda luta em que ela vive, e ela vive e bebe em pelo menos uma', diz, certo)


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 600
    luta.semente(10); ok = 0; tot = 0
    if sys.argv[2:3] == ['magia']:                          # só o bloco da magia (ele tem a semente dele: dá o mesmo que no banco inteiro)
        print(f'BANCO DE PROVAS DO MOTOR 10 · só A MAGIA NA LUTA · {n} lutas por meta\n')
        for nome, deu, passa in magia_luta(n):
            ok += passa; tot += 1
            print(f"  {'passa' if passa else 'FALHA'}  {nome}: {deu}")
        print(f'\n{ok} de {tot} metas passam.')
        return ok == tot
    print(f'BANCO DE PROVAS DO MOTOR 10 · {n} lutas por meta\n')
    print(f"{'O EQUILÍBRIO (vitória do primeiro)':<104}{'faixa':>10}{'medido':>9}")
    for nome, a, b, (lo, hi), kw in METAS:
        v, r = luta.duelos(a, b, n=kw.get('n', n), inicio='colado'); passa = lo <= v <= hi; ok += passa; tot += 1
        print(f"{nome:<104}{f'{lo}-{hi}%':>10}{f'{v}%':>8}  {'passa' if passa else 'FALHA'}  ({r} rodadas)")
    print(f"\n{'A DURAÇÃO (mediana de rodadas)':<104}{'faixa':>10}{'medido':>9}")
    for nome, a, b, (lo, hi) in DURACAO:
        v, r = luta.duelos(a, b, n=max(200, n // 3), inicio='colado'); passa = lo <= r <= hi; ok += passa; tot += 1
        print(f"{nome:<104}{f'{lo}-{hi} r':>10}{f'{r} r':>8}  {'passa' if passa else 'FALHA'}")
    print('\nAS ARMAS ENTRE SI (cada montagem Rara de nível 60 contra todas as outras; a meta: nenhuma abaixo de 35% nem acima de 65%)')
    tab = sorted(armas(max(40, n // 10)), key=lambda x: -x[1]); passa = all(35 <= p <= 65 for _, p in tab); ok += passa; tot += 1
    for i in range(0, len(tab), 4): print('  ' + ' · '.join(f'{nome} {p}%' for nome, p in tab[i:i + 4]))
    print(f"  {'passa' if passa else 'FALHA'}  a melhor {tab[0][1]}%, a pior {tab[-1][1]}%")
    print('\nOS MÓDULOS (cada coisa que interfere, interfere para o lado certo)')
    for nome, deu, passa in modulos(max(300, n // 2)):
        ok += passa; tot += 1
        print(f"  {'passa' if passa else 'FALHA'}  {nome}: {deu}")
    print('\nOS BICHOS (as oito metas da etapa 2, de B1 a B8, e o que o corpo do bicho tem de ser)')
    for nome, deu, passa in bichos(n):
        ok += passa; tot += 1
        print(f"  {'passa' if passa else 'FALHA'}  {nome}: {deu}")
    print('\nA MAGIA NA LUTA (a etapa da magia, capítulo 11: o projeto conta, seção G, na parte da luta; os nove traços novos; as fases do chefe; a ordem; a luta que volta ao estado)')
    for nome, deu, passa in magia_luta(n):
        ok += passa; tot += 1
        print(f"  {'passa' if passa else 'FALHA'}  {nome}: {deu}")
    print(f'\n{ok} de {tot} metas passam.')
    return ok == tot


if __name__ == '__main__':
    sys.exit(0 if main() else 1)
