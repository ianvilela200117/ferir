#!/usr/bin/env python3
"""provas.py — MOTOR 10: O BANCO DE PROVAS. As metas de equilíbrio, escritas e medidas.

Toda mudança no tabelas.py ou no luta.py roda isto. Meta que falha: a mudança não entra (ou a meta muda, com a palavra do jogador).
As metas dizem em números o que o jogador pediu:
  "a arma decide muito quem vence" · "uma arma dá chance de um nível 50 vencer um nível 500" · "sem restrição de nível para usar a peça".
Cinco blocos: O EQUILÍBRIO (quem vence) · A DURAÇÃO (quanto dura) · AS ARMAS ENTRE SI (nenhuma escolha é a única certa)
· OS MÓDULOS (cada coisa que interfere, interfere mesmo, e para o lado certo) · OS BICHOS (as oito metas da etapa 2: o corpo é a arma
e a armadura, o bando, o chefe, o tamanho, os traços, a moral, a duração; e o que o corpo do bicho tem de ser).

Uso: python3 provas.py [N]        N = lutas por meta (padrão 600)
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
    saiu = 0; k = max(60, n // 5)
    for _ in range(k):
        S = luta.nova(gente('o rei', 40, ('espada', 1), ('couro', 1), controla=True, linha='trás')() + varios(2, 60, 2, 2, pre='guarda ', moral='firme')(), varios(4, 40, 1, 1, pre='b')(), inicio='perto', lugar=dict(largura=2), quieto=True)
        luta.corre(S, interativo=True); luta.ordem(S, 'o rei: recuar defensiva')
        while luta.corre(S, interativo=True) == 'parada' and S['L'][2]['estado'] == 'pe': pass
        saiu += next(f for f in S['L'] if f['nome'] == 'o rei')['estado'] == 'saiu'
    saiu = round(100 * saiu / k); out.append(('A RETIRADA: com dois guardas segurando o corredor, quem recebe ordem de recuar sai da luta', f'em {saiu}% das lutas', saiu >= 80))
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
    ok('B+ A AMEAÇA: a frase que o caçador lê antes da luta diz o grau, a categoria, o tamanho, o corpo e os traços de cada espécie, e faz a conta da regra de ouro com o que ele veste',
       f"{len(TB.ESPECIES) - len(falta)} de {len(TB.ESPECIES)} espécies; o lobo contra quem veste Comum: {'diz um terço e o triplo' if 'um terço' in a and 'o triplo' in a else 'NÃO DIZ'}", not falta and 'um terço' in a and 'o triplo' in a and 'são 4' in a)
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
    return out


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 600
    luta.semente(10); ok = 0; tot = 0
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
    print(f'\n{ok} de {tot} metas passam.')
    return ok == tot


if __name__ == '__main__':
    sys.exit(0 if main() else 1)
