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

E um sétimo, A PARTE 2, FASE 1b (projeto/etapa_efeitos/DESENHO.md, seção 10): B0 (a luta de sempre, contra o motor de antes), EF1 a EF8 (a régua dos números e das regras,
a peça magra de cima, a pilha, o atordoar que não trava, o calejo, a escada do medo, os freios do apelão) e B3 (o item decide).

Uso: python3 provas.py [N] [magia]        N = lutas por meta (padrão 600) · magia: só o bloco da magia
     python3 provas.py [N] efeitos         só o bloco da fase 1b (N lutas por linha; padrão 2.000, o modo de sempre do contrato) · efeitos tabela: a tabela por nível
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


# ---------- A PARTE 2, FASE 1b: A BASE DA LUTA E OS EFEITOS DE ITEM (o bloco EF e as metas B0, B1, B3; projeto/etapa_efeitos/DESENHO.md, seção 10) ----------
# O padrão é o do banco: o duelo de iguais do nível 50 (mão de Mestre), tudo Raro, começando perto; cada efeito medido no duelo ESPELHADO (metade das lutas com ele no lado A,
# metade no B: a vantagem de lado some) e com OS MESMOS DADOS em cada coluna do mesmo efeito (a semente dele: o número igual dá a vitória igual). O número da categoria entra
# na peça pelo gancho das provas (p['fx_prova']: tabelas_efeitos.valor, o mesmo que a peça daria): entre iguais o golpe tira o mesmo em qualquer categoria. Os cenários
# desiguais (a Perfura contra a armadura uma acima; a Robusta contra o Aturdir e a Coragem contra o Medo da mesma categoria; o um contra dez) medem a vitória com e sem o efeito,
# com os mesmos dados. Uso: python3 provas.py [N] efeitos (só este bloco; N lutas por linha, 2.000 de padrão) · python3 provas.py [N] efeitos tabela (a tabela por nível)
import tabelas_efeitos as TE
B0_REF = 'dbb6c3e'          # o commit do motor de antes da fase 1b (a fase 1a): a meta B0 roda as mesmas lutas nele e no de agora, com a escada do medo desligada


def _vence(faz_a, faz_b, n, seed, **kw):
    """a fração de vitórias de A em n lutas (o empate vale meia), com os dados da semente (à parte dos outros blocos)"""
    D0 = luta.D; luta.semente(seed); v = 0.0
    try:
        for _ in range(n):
            S = luta.nova(faz_a(), faz_b(), quieto=True, **{**dict(inicio='perto'), **kw}); luta.corre(S)
            v += 1 if S['fim'] == 'A' else 0 if S['fim'] == 'B' else 0.5
    finally: luta.D = D0
    return v / max(1, n)


def _pontos(faz_com, faz_sem, n, seed, **kw):
    """os pontos de vitória do efeito no duelo espelhado: a vitória de quem tem, − 50"""
    a = _vence(faz_com, faz_sem, n // 2, seed, **kw); b = _vence(faz_sem, faz_com, n - n // 2, seed + 7919, **kw)
    return 100 * (a + (1 - b)) / 2 - 50


def _delta(faz_com, faz_sem, faz_contra, n, seed, **kw):
    """os pontos que o efeito dá num cenário desigual: a vitória com ele − sem ele, contra o mesmo lado e com os mesmos dados"""
    return 100 * (_vence(faz_com, faz_contra, n, seed, **kw) - _vence(faz_sem, faz_contra, n, seed, **kw))


def _g(nome, fx=None, nivel=50, arma=R, arm=R, esc='igual', familia='espada', vont=None, atributos=None, **kw):
    """o guerreiro do banco (espada, malha com elmo e escudo), com os números de efeito postos (fx: {'arma': {...}, 'armadura': {...}, 'escudo': {...}, 'amuleto': {...}})"""
    at = dict(atributos or {}); at.update({'Vontade': vont} if vont else {})
    p = padrao(nome, nivel, atributos=at or None, **({'fx_prova': fx} if fx else {}), **kw)
    return veste(p, arma=(familia, arma), armadura=('malha', arm), escudo=(arm if esc == 'igual' else esc) if T.FAMILIAS[familia]['maos'] == 1 else None)


def _onde(k):
    """em que peça o banco põe o número do efeito (o Temível, na armadura)"""
    pc = TE.EFEITOS[k]['pecas']; return 'arma' if 'arma' in pc else 'armadura' if 'armadura' in pc else pc[0]


def _ef1_linha(k, n, seed, nivel=50, so=None):
    """os pontos de um efeito de número nas 8 categorias, no cenário dele (None: a categoria não tem o efeito; so: só estas categorias)"""
    cena = TE.EFEITOS[k].get('cena'); out = []
    for c in range(len(T.CATS)):
        v = TE.valor(k, c)
        if so is not None and c not in so: out.append(None); continue
        if v is None: out.append(None); continue
        if k == 'cacadora': v = (v, 'gente')
        fx = {_onde(k): {k: v}}; mt = T.maestria_tipica(nivel)
        if cena == 'magia':
            out.append(_pontos(lambda: [mago('a maga', nivel, fx_prova=fx)], lambda: [mago('o mago', nivel)], n, seed)); continue
        if cena == 'acima':                                 # a Perfura: contra a armadura uma categoria acima da arma
            contra = lambda: [_g('o encouraçado', nivel=nivel, arm=R + 1, esc=R, vont=100)]
            out.append(_delta(lambda: [_g('com', fx, nivel)], lambda: [_g('sem', None, nivel)], contra, n, seed)); continue
        if cena == 'carga':                                 # a Robusta: contra a carga 6 (o Aturdir Épico: a medida do contrato, "a Rara corta a carga 6"), a mesma em toda coluna. Contra o
            contra = lambda: [_g('o atordoador', {'arma': {'aturdir': TE.ATURDIR[3]}}, nivel)]       # Aturdir da mesma categoria a linha descia de verdade (a Mítica contra a carga 12 pega em 2 golpes; a Lendária contra a 10, em 3)
            out.append(_delta(lambda: [_g('com', fx, nivel)], lambda: [_g('sem', None, nivel)], contra, n, seed)); continue
        if cena == 'medo':                                  # a Coragem: contra o Medo da mesma categoria (a Comum, contra o da Incomum)
            contra = lambda: [_g('o temido', {'arma': {'medo': TE.MEDO[max(c, 1)]}}, nivel)]
            out.append(_delta(lambda: [_g('com', fx, nivel)], lambda: [_g('sem', None, nivel)], contra, n, seed)); continue
        out.append(_pontos(lambda: [_g('com', fx, nivel)], lambda: [_g('sem', None, nivel)], n, seed))
    return out


def _f(x): return '—' if x is None else f'{x:+.1f}'.replace('.', ',')


def ef1(n):
    """EF1 A RÉGUA DOS NÚMEROS: cada efeito de número nas 8 categorias, no cenário dele: nunca acima do teto da faixa da categoria (o cheio, que é o número da de cima, nunca acima
    do teto da de cima: é a coluna seguinte); cada coluna não menor que a da esquerda; com a folga de 1 ponto"""
    out = []; linhas = {}
    for i, k in enumerate([k for k in TE.EFEITOS if TE.de_numero(k)]):
        pts = _ef1_linha(k, n, 3000 + 17 * i); linhas[k] = pts
        cs = [c for c in range(len(pts)) if pts[c] is not None]
        duvidas = lambda: {c for c in cs if pts[c] > TE.teto_da_cat(c) + TE.FOLGA} | {x for a, b in zip(cs, cs[1:]) if pts[b] < pts[a] - TE.FOLGA for x in (a, b)}
        longo = ''; feitas = set()
        while duvidas() - feitas:                           # O MODO LONGO (seção 10: 20.000 lutas por linha): a coluna que passa do teto, ou o par que desce, se remede com 10 vezes as lutas;
            novas = duvidas() - feitas                      # e de novo, se a coluna remedida faz descer o par com a vizinha (cada coluna, uma vez)
            re_ = _ef1_linha(k, 10 * n, 3000 + 17 * i, so=novas)
            for c in novas: pts[c] = re_[c]
            feitas |= novas
        if feitas: longo = f" (remedidas no modo longo, {10 * n} lutas: {', '.join(T.CATS[c] for c in sorted(feitas))})"
        acima = [T.CATS[c] for c in cs if pts[c] > TE.teto_da_cat(c) + TE.FOLGA]
        desce = [f"{T.CATS[a]}→{T.CATS[b]}" for a, b in zip(cs, cs[1:]) if pts[b] < pts[a] - TE.FOLGA]
        out.append((f"EF1 {TE.EFEITOS[k]['nome'].upper()} ({TE.EFEITOS[k].get('cena') or 'duelo'}): nunca acima do teto da faixa (Comum 5 · Incomum e Rara 10 · Épica e Única 20 · da Lendária para cima 40), "
                    f"e cada coluna não menor que a da esquerda (folga {TE.FOLGA})",
                    ' · '.join(f"{T.CATS[c][:3]} {_f(pts[c])}" for c in range(len(pts))) + longo + (f"; ACIMA DO TETO: {', '.join(acima)}" if acima else '') + (f"; DESCE: {', '.join(desce)}" if desce else ''),
                    not acima and not desce))
    return out, linhas


def ef2(n):
    """EF2 A RÉGUA DAS REGRAS: cada efeito de regra que tem cenário, medido nele, do piso ao teto da força dele (com a folga), seja ele medido (m), de conta (c) ou de desenho (d)
    no contrato. A força de cada um é a que o banco mede, nos dois sentidos (tabelas_efeitos; o DESENHO 12.3 registra as que mudaram de porta). O Imortal compra a vida, não a
    vitória (a régua não o julga: 4.3). Os de desenho sem cenário (Leve, Pesa, Não Quebra, Fio Manso) não têm vitória a medir. Fora da faixa, a linha se remede no modo longo
    (10 vezes as lutas) antes de reprovar."""
    out = []; dez = varios(10, 60, C['unico'], C['unico'])
    um_ = lambda fx, **kw: (lambda: [veste(padrao('o um', 120, moral='firme', **({'fx_prova': fx} if fx else {})), arma=('espada', C['lendario']), armadura=('malha', C['lendario']), escudo=C['lendario'])])
    cenas = {
        'derruba': lambda k, q: _pontos(lambda: [_g('com', {'arma': {k: True}})], lambda: [_g('sem')], q, 4101),
        'arrancada': lambda k, q: _pontos(lambda: [_g('com', {'arma': {k: True}})], lambda: [_g('sem')], q, 4102),
        'expoe': lambda k, q: _pontos(lambda: [_g('com', {'arma': {k: True}})], lambda: [_g('sem')], q, 4103),
        'ponta_certa': lambda k, q: _pontos(lambda: [_g('com', {'arma': {k: True}})], lambda: [_g('sem')], q, 4104),
        'desforra': lambda k, q: _pontos(lambda: [_g('com', {'arma': {k: True}})], lambda: [_g('sem')], q, 4105),
        'escancara': lambda k, q: _pontos(lambda: [_g('com', {'arma': {k: True}})], lambda: [_g('sem')], q, 4106),
        'amolece': lambda k, q: _pontos(lambda: [_g('com', {'arma': {k: True}})], lambda: [_g('sem')], q, 4107),
        'folego': lambda k, q: _pontos(lambda: [_g('com', {'arma': {k: True}}, familia='martelo')], lambda: [_g('sem', familia='martelo')], q, 4108),
        'brasa': lambda k, q: _pontos(lambda: [_g('com', {'arma': {k: True}})], lambda: [_g('sem')], q, 4109),
        'golpe_do_fim': lambda k, q: _pontos(lambda: [_g('com', {'arma': {k: True}})], lambda: [_g('sem')], q, 4110),
        # os de grupo: o um contra dez do banco, com as 2.000 lutas por linha do contrato (seção 10)
        'ceifadora': lambda k, q: _delta(um_({'arma': {k: True}}), um_(None), dez, q, 4111),
        'varredura': lambda k, q: _delta(um_({'arma': {k: True}}), um_(None), dez, q, 4112),
        'tempestade': lambda k, q: _delta(um_({'arma': {k: True}}), um_(None), dez, q, 4113),
        'imortal': lambda k, q: _pontos(lambda: [_g('com', {'armadura': {k: True}})], lambda: [_g('sem')], q, 4114),
        'aparadora': lambda k, q: _pontos(lambda: [_g('com', {'escudo': {k: True}})], lambda: [_g('sem')], q, 4115),
        'luz': lambda k, q: _pontos(lambda: [_g('com', {'arma': {k: True}})], lambda: [_g('sem')], q, 4116, tempo=['escuro']),
        'firme': lambda k, q: _delta(lambda: [_g('com', {'armadura': {k: True}})], lambda: [_g('sem')], lambda: [_g('o que derruba', {'arma': {'derruba': True}})], q, 4117),
        # o Atar no "mago contra mago" do contrato: o clérigo de maça (quem lança e bate) contra o mago; o guerreiro contra a maga deu +0,3, e o mago de varinha e espada, +0,0
        'atar': lambda k, q: _delta(lambda: [clerigo('com', fx_prova={'arma': {k: True}})], lambda: [clerigo('sem')], lambda: [mago('o mago')], q, 4118),
        'refletora': lambda k, q: _delta(lambda: [_g('com', {'escudo': {k: True}}, amuleto=R)], lambda: [_g('sem', amuleto=R)], lambda: [mago('a maga')], q, 4119, inicio='longe'),
        'dominio': lambda k, q: _pontos(lambda: [mago('com', fx_prova={'foco': {k: True}})], lambda: [mago('sem')], q, 4120),
        'guardia': lambda k, q: _delta(lambda: [_g('g1', {'escudo': {k: True}}, guarda='g2', moral='firme'), _g('g2'), _g('g3')], lambda: [_g('g1', guarda='g2', moral='firme'), _g('g2'), _g('g3')],
                                       lambda: [_g('b1'), _g('b2'), _g('b3')], q, 4121),
        'escudo_que_conta': lambda k, q: _delta(lambda: [_g('g1', {'escudo': {k: True}}), _g('g2'), _g('g3')], lambda: [_g('g1'), _g('g2'), _g('g3')],
                                                lambda: [_g('b1', {'arma': {'medo': 20}}), _g('b2', {'arma': {'medo': 20}}), _g('b3', {'arma': {'medo': 20}})], q, 4122),
    }
    for k, x in TE.EFEITOS.items():
        if x['tipo'] != 'regra': continue
        f = x['forca']; m = x['medida']; mede = cenas.get(k)
        if not mede: out.append((f"EF2 {x['nome'].upper()} ({f}; {m})", 'sem vitória a medir (o contrato o marca de desenho, sem cenário: a regra faz o que diz, e a peça o mostra)', True)); continue
        dentro = lambda v: TE.PISO_PONTOS[f] - TE.FOLGA <= v <= TE.FORCA_PONTOS[f] + TE.FOLGA
        pts = mede(k, n); longo = ''
        if k != 'imortal' and not dentro(pts): pts = mede(k, 10 * n); longo = f' (remedido no modo longo, {10 * n} lutas)'
        ok_ = k == 'imortal' or dentro(pts)
        out.append((f"EF2 {x['nome'].upper()} ({f}: {TE.PISO_PONTOS[f]} a {TE.FORCA_PONTOS[f]}; o contrato: {m})",
                    f"{_f(pts)}{longo}" + (' (a régua não julga: compra a vida)' if k == 'imortal' else '' if ok_ else (' ABAIXO DO PISO' if pts < TE.PISO_PONTOS[f] else ' ACIMA DO TETO')), ok_))
    return out


def _arma_fx(cat, efs, fam='espada'):
    """a arma de verdade, com os efeitos (os cheios marcados): o número sai do catálogo, como no jogo"""
    return item('arma', cat, familia=fam, efeitos=[dict(chave=k, **({'cheio': True} if ch else {}), **({'contra': 'gente'} if k == 'cacadora' else {})) for k, ch in efs], **({'teto_efeitos': len(efs)} if len(efs) > 4 else {}))


def ef3(n):
    """EF3 A PEÇA MAGRA DE CIMA: a arma uma acima, sem efeito, contra a de baixo com efeitos cheios (mesma gente); o degrau emprestado em peça de 6 é recusado; os quatro pares; o conjunto"""
    out = []; nn = max(n, 2000)
    def contra(cat_alta, cat_baixa, efs, piso=None, **kw):  # "a arma uma acima": a armadura e o escudo dos dois são da categoria de baixo (a arma de cima vale ×3, como entre a Épica e a Rara)
        alta = lambda: [veste(padrao('a de cima', 50, atributos={'Vontade': 100}), arma=('espada', cat_alta), armadura=('malha', cat_baixa), escudo=cat_baixa)]
        baixa = lambda: [veste(padrao('a de baixo', 50, atributos={'Vontade': 100}), arma=_arma_fx(cat_baixa, efs), armadura=('malha', cat_baixa), escudo=cat_baixa)]
        mede = lambda q: 100 * (_vence(alta, baixa, q // 2, 5101, **kw) + 1 - _vence(baixa, alta, q - q // 2, 5102, **kw)) / 2
        v = mede(nn)
        if piso is not None and v < piso and v >= piso - 3: v = mede(10 * nn); longos.append(v)      # na borda (até 3 pontos abaixo): o modo longo (10 vezes as lutas) decide
        return v
    longos = []
    quatro = [('gume', 1), ('certeira', 1), ('critico', 1), ('vampira', 1)]
    l1 = contra(R + 1, R, quatro, 75 - TE.FOLGA); l2 = contra(R + 1, R, [('gume', 1), ('certeira', 1), ('critico', 1), ('medo', 1)], 75 - TE.FOLGA)
    emp = lambda: item('arma', R, familia='espada', degrau=True, efeitos=[dict(chave='gume', cheio=True), dict(chave='critico', cheio=True), dict(chave='escancara', emprestado=True)])      # (Dia 46, o Mestre: o degrau só em peça de até 3; a de 4 dava 73,95%)
    a3 = lambda: [veste(padrao('a de cima', 50, atributos={'Vontade': 100}), arma=('espada', R + 1), armadura=('malha', R), escudo=R)]           # (a peça nova a cada luta: a mesma peça
    b3 = lambda: [veste(padrao('a de baixo', 50, atributos={'Vontade': 100}), arma=emp(), armadura=('malha', R), escudo=R)]                      # gastava de uma luta para outra e quebrava)
    m3 = lambda q: 100 * (_vence(a3, b3, q // 2, 5103) + 1 - _vence(b3, a3, q - q // 2, 5104)) / 2
    l3 = m3(nn)
    if 75 - TE.FOLGA - 3 <= l3 < 75 - TE.FOLGA: l3 = m3(10 * nn); longos.append(l3)                     # na borda (o contrato: 74,7%, "na borda"): o modo longo decide
    pc_ = lambda v, meta: (f"{v:.2f}%" if abs(v - meta) < 0.15 else f"{v:.1f}%").replace('.', ',')      # perto da meta, duas casas: o arredondamento não esconde a borda
    out.append(('EF3 A ÉPICA MAGRA contra a Rara de 4 cheios (Gume +30%, Certeira +3, Crítico 19/11, Vampira 50%; ou o Medo 20 no lugar da Vampira; ou 2 cheios, Gume e Crítico, e a Escancara do degrau emprestado, a peça de 3): 75% ou mais (folga 1)',
                f"{pc_(l1, 75 - TE.FOLGA)}, {pc_(l2, 75 - TE.FOLGA)} e {pc_(l3, 75 - TE.FOLGA)}" + (f" ({len(longos)} no modo longo, {10 * nn} lutas)" if longos else ''), min(l1, l2, l3) >= 75 - TE.FOLGA))
    seis = [('gume', 1), ('certeira', 1), ('critico', 1), ('vampira', 1), ('medo', 1), ('aturdir', 1)]
    l4 = contra(R + 1, R, seis, 60 - TE.FOLGA)
    va = lambda: [_g('a de cima', arma=R + 1, vont=100)]; vb = lambda: [_g('a de baixo', {'arma': {'gume': 0.40, 'certeira': 3, 'critico': (19, 11), 'vampira': 0.5, 'medo': 20, 'aturdir': 6}}, vont=100)]
    vidro = 100 * (_vence(va, vb, nn // 2, 5105) + 1 - _vence(vb, va, nn - nn // 2, 5106)) / 2       # espelhada, como as outras linhas (o gume de +40% do vidro, posto pelo gancho)
    out.append(('EF3 O TETO INTEIRO: a Épica magra contra a Rara de 6 cheios, os mais fortes (Gume, Certeira, Crítico, Vampira 50%, Medo 20, Aturdir 6); e a mesma com o Gume de +40% do vidro (os números da fase 5): 60% ou mais',
                f"{pc_(l4, 60 - TE.FOLGA)} e {pc_(vidro, 60 - TE.FOLGA)}", min(l4, vidro) >= 60 - TE.FOLGA))
    try: item('arma', R, familia='espada', degrau=True, teto_efeitos=6, efeitos=[dict(chave=k, cheio=True) for k in ('gume', 'certeira', 'critico', 'vampira', 'medo')] + [dict(chave='escancara', emprestado=True)]); r1 = 'aceitou'
    except SystemExit as e: r1 = 'recusou' if 'até 3 efeitos' in str(e) else 'recusou por outro motivo: ' + str(e)[:80]
    out.append(('EF3 O DEGRAU EMPRESTADO EM PEÇA DE 6 é recusado (com 6, a Épica magra venceu só 58,5%, e com 4, 73,95%: o degrau só em peça de até 3)', r1, r1 == 'recusou'))
    # OS QUATRO PARES: "a X cheia" é a peça com o teto de efeitos da categoria, todos cheios, na ordem de 4.4 (Gume, Certeira, Crítico, Vampira; o quinto, o Medo); a Incomum de 4,
    # os dois primeiros cheios. (Com os cinco mais fortes, o Aturdir no lugar da Vampira, o par de cima mede-se à parte: a linha seguinte.)
    can = ['gume', 'certeira', 'critico', 'vampira', 'medo']
    pares = [('a Rara magra × a Incomum de 4 com 2 cheios', R, 1, [(k, i < 2) for i, k in enumerate(can[:4])]),
             ('a Épica × a Rara cheia (4)', 3, R, [(k, 1) for k in can[:4]]),
             ('a Única × a Épica cheia (5)', 4, 3, [(k, 1) for k in can[:5]]),
             ('a Lendária × a Única cheia (5)', 5, 4, [(k, 1) for k in can[:5]])]
    n0 = len(longos); vs = [(nm, contra(a, b, efs, 60 - TE.FOLGA)) for nm, a, b, efs in pares]
    out.append(('EF3 OS QUATRO PARES (a de cima magra contra a de baixo cheia, mesma gente; "cheia": o teto de efeitos da categoria, todos cheios, na ordem de 4.4): 60% ou mais em cada',
                ' · '.join(f"{nm}: {v:.1f}%".replace('.', ',') for nm, v in vs) + (f" ({len(longos) - n0} remedido(s) no modo longo, {10 * nn} lutas)" if len(longos) > n0 else ''), all(v >= 60 - TE.FOLGA for _, v in vs)))
    forte = contra(5, 4, [(k, 1) for k in ('gume', 'certeira', 'critico', 'medo', 'aturdir')])
    out.append(('EF3 (à parte, sem meta: o contrato não o pede) o par de cima com os cinco mais fortes (Gume, Certeira, Crítico, Medo e Aturdir cheios: os números da Lendária numa Única)', f"a Lendária magra vence {forte:.1f}%".replace('.', ','), True))
    # O CONJUNTO: o conjunto uma acima (arma, armadura e escudo), sem efeito, contra o de baixo com a peça destas linhas (a arma de 4 cheios): a leitura que fecha com a meta (85%);
    # o conjunto de baixo com TUDO cheio é o B3 (o topo do sistema contra o conjunto uma acima: 60%)
    cj = _conjunto(nn, R + 1, so_arma=True)
    out.append(('EF3 O CONJUNTO: o conjunto uma acima, sem efeito, contra o de baixo com a arma de 4 cheios (Gume, Certeira, Crítico, Vampira): 85% ou mais', f"{cj:.1f}%".replace('.', ','), cj >= 85 - TE.FOLGA))
    return out


def _conjunto(nn, alta, seed=5201, so_arma=False):
    """a vitória do conjunto de cima (arma, armadura e escudo da categoria alta, sem efeito) contra o conjunto Raro com tudo cheio (a arma de 4 cheios; a armadura: Couraça, Devolve,
    Regenera e Robusta; o escudo: Guarda e Temível), espelhada"""
    def baixo(nome):
        p = padrao(nome, 50, atributos={'Vontade': 100})
        if so_arma: return veste(p, arma=_arma_fx(R, [('gume', 1), ('certeira', 1), ('critico', 1), ('vampira', 1)]), armadura=('malha', R), escudo=R)
        return veste(p, arma=_arma_fx(R, [('gume', 1), ('certeira', 1), ('critico', 1), ('medo', 1)]),
                     armadura=item('armadura', R, material='malha', efeitos=[dict(chave=k, cheio=True) for k in ('couraca', 'devolve', 'regenera', 'robusta')]),
                     escudo=item('escudo', R, efeitos=[dict(chave=k, cheio=True) for k in ('guarda', 'temivel')]))
    cima = lambda: [veste(padrao('o de cima', 50, atributos={'Vontade': 100}), arma=('espada', alta), armadura=('malha', alta), escudo=alta)]
    a = _vence(cima, lambda: [baixo('o de baixo')], nn // 2, seed); b = _vence(lambda: [baixo('o de baixo')], cima, nn - nn // 2, seed + 1)
    return 100 * (a + 1 - b) / 2


def ef4(n):
    """EF4 A PILHA: golpes sorteados com as piores combinações que cabem (o Golpe do Fim, o Gume e a Caçadora Primordiais cheios, o Crítico 17/7, a Perfura, o alvo exposto,
    quem bate amolecido, a Couraça): o golpe dividido pelo mesmo golpe pela regra de hoje, com os mesmos dados, nunca acima de ×7; os dados nunca mais de 4 vezes; a couraça
    até 75%; os números fixos até +8 e a resistência até +16; o crítico nunca melhor que 17/7. (O fecho, o trunfo e o Rito são da fase 2: o dado somado ainda não existe.)"""
    import random
    rr = random.Random(41); golpes = max(10000, 5 * n); pior = 0.0; vezes = 0; cou = 0.0; crit = 0.0; mortos = 0; cortou = 0
    D0 = luta.D; luta.semente(4401)
    try:
        while golpes > 0:
            efa = {k: v for k, v in (('golpe_do_fim', True), ('gume', 1.0), ('cacadora', (1.0, 'gente')), ('critico', (17, 7)), ('perfura', 0.35), ('critico_19', True)) if rr.random() < .7}
            efv = {k: v for k, v in (('couraca', 0.5),) if rr.random() < .5}
            a = _g('a', {'arma': efa}, arma=rr.randint(0, 7), vont=100); e = _g('e', {'armadura': efv} if efv else None, arm=rr.randint(0, 7), esc=rr.randint(0, 7), vont=100)
            S = luta.nova([a], [e], inicio='colado', quieto=True); S['r'] = 1; S['mede'] = []; fa, fe = S['L']
            for _ in range(50):
                fe['pv'] = fe['pvmax'] = 10 ** 9; fe['estado'] = 'pe'; fe['feridas'] = []; fe['exposto'] = S['r'] + 2 if rr.random() < .5 else 0; fa['amolecido'] = S['r'] + 1 if rr.random() < .2 else 0
                fe['golpeado'] = []; luta.golpe(S, fa, fe, fa['arma'], extra=True); golpes -= 1
            for m in S['mede']:
                if m['hoje'] > 0: pior = max(pior, m['final'] / m['hoje'])
                cortou += m['final'] < m['novo']; vezes = max(vezes, m['vezes']); cou = max(cou, m['couraca']); crit = max(crit, TE.chance_critico(m['faixa']))
    finally: luta.D = D0
    fixos = _fixos_teto()
    ok_ = pior <= TE.TETO_PILHA + 1e-9 and vezes <= TE.DADOS_MAX and cou <= TE.COURACA_TETO + 1e-9 and crit <= TE.chance_critico(TE.CRITICO_MELHOR) + 1e-9 and fixos[0]
    return [('EF4 A PILHA: o golpe nunca passa de 7 vezes o golpe de hoje (com os mesmos dados), os dados nunca rolam mais de 4 vezes, a couraça até 75%, os fixos até +8 e a resistência até +16, o crítico nunca melhor que 17/7',
             f"{max(10000, 5 * n)} golpes: o pior ×{pior:.2f} do golpe de hoje (o teto cortou {cortou} golpes); os dados no máximo {vezes} vezes; a couraça no máximo {100 * cou:.0f}%; "
             f"o crítico no máximo {100 * crit:.0f}% (17/7: {100 * TE.chance_critico(TE.CRITICO_MELHOR):.0f}%); {fixos[1]}".replace('.', ','), ok_)]


def _fixos_teto():
    """os números fixos com tudo empilhado: a Certeira Primordial e a Desforra; a Guarda Primordial; a Coragem Primordial, a Robusta Primordial e o Escudo que Conta; a Robusta"""
    S = luta.nova([_g('a', {'arma': {'certeira': 8, 'desforra': True}, 'escudo': {'guarda': 8}, 'amuleto': {'coragem': 8}, 'armadura': {'robusta': (16, 5)}}, vont=100)], [_g('b')], quieto=True)
    a, b = S['L']; a['desforra'][b['nome']] = 99; a['coragem_escudo'] = 2
    ac, df, cg, rs = luta._fixo(S, a, 'acerto', a['arma'], b), luta._fixo(S, a, 'defesa'), luta._fixo(S, a, 'coragem'), luta._fixo(S, a, 'resistencia')
    return ac <= TE.FIXO_TETO and df <= TE.FIXO_TETO and cg <= TE.FIXO_TETO and rs <= TE.RESIST_TETO, f"os fixos empilhados: acerto +{ac}, Defesa +{df}, coragem +{cg}, resistência +{rs}"


def ef5(n):
    """EF5 O ATORDOAR NÃO TRAVA: a carga Primordial (15) contra Vigor 50; o chefe; o 3 contra 3; e com a ferida grave na cabeça (a arma uma acima abre a grave): em cada janela de
    3 turnos seguidos, o alvo age em 2 ou mais. E as medidas que o contrato remede: a coluna do Aturdir (no EF1) e o 3 contra 3 com a carga 4 e 6."""
    out = []; nn = max(n, 2000)
    def janelas(faz_a, faz_b, k):
        D0 = luta.D; luta.semente(5501 + k); mal = jan = perd = turnos = 0
        try:
            for _ in range(nn):
                S = luta.nova(faz_a(), faz_b(), quieto=True, inicio='perto'); S['mede_turnos'] = {}; luta.corre(S)
                for nome, h in S['mede_turnos'].items():
                    if luta.por_nome(S, nome)['lado'] != 'B': continue
                    turnos += len(h); perd += sum(h)
                    for i in range(len(h) - 2): jan += 1; mal += sum(h[i:i + 3]) >= 2
        finally: luta.D = D0
        return mal, jan, perd / max(1, turnos)
    at15 = {'arma': {'aturdir': 15}}
    cenas = [('a carga 15 contra Vigor 50', lambda: [_g('o atordoador', at15)], lambda: [_g('o alvo', atributos={'Vigor': 50})]),
             ('o chefe (líder, de moral firme)', lambda: [_g('o atordoador', at15)], lambda: [_g('o chefe', lider=True, moral='firme')]),
             ('o 3 contra 3', lambda: [_g(f'a{i}', at15) for i in range(3)], lambda: [_g(f'b{i}') for i in range(3)]),
             ('com a ferida grave na cabeça (a arma uma acima)', lambda: [_g('o atordoador', at15, arma=R + 1, vont=100)], lambda: [_g('o alvo', atributos={'Vigor': 50})])]
    res = [(nm,) + janelas(a, b, i) for i, (nm, a, b) in enumerate(cenas)]
    out.append(('EF5 O ATORDOAR NÃO TRAVA: em cada janela de 3 turnos seguidos o alvo age em 2 ou mais (nenhuma janela com 2 perdidos), na carga Primordial contra Vigor 50, no chefe, no 3 contra 3 e com a ferida grave na cabeça',
                ' · '.join(f"{nm}: {mal} de {jan} janelas com 2 perdidos, {100 * pt:.0f}% dos turnos perdidos" for nm, mal, jan, pt in res).replace('.', ','), all(r[1] == 0 for r in res)))
    t4 = _delta(lambda: [_g(f'a{i}', {'arma': {'aturdir': 4}}) for i in range(3)], lambda: [_g(f'a{i}') for i in range(3)], lambda: [_g(f'b{i}') for i in range(3)], max(600, n // 2), 5601)
    t6 = _delta(lambda: [_g(f'a{i}', {'arma': {'aturdir': 6}}) for i in range(3)], lambda: [_g(f'a{i}') for i in range(3)], lambda: [_g(f'b{i}') for i in range(3)], max(600, n // 2), 5601)
    out.append(('EF5 O 3 CONTRA 3, REMEDIDO (o contrato mediu a carga 4 e 6: +18,0 e +21,8; a régua do grupo: o aberto vale para os três que batem)', f"carga 4: {_f(t4)} · carga 6: {_f(t6)}", True))
    return out


def ef6(n):
    """EF6 O CALEJO: os golpes até o 1º e até o 2º atordoar (a carga 4 da Rara contra a resistência 10, 14, 18...): o 2º pede 1,4 vez os do 1º, ou mais. A meta se lê com os golpes
    que tiram PV entre um atordoar e o outro, os da cabeça firme incluídos (o tempo que o 2º atordoar custa: os dois freios juntos); a conta só do calejo (os golpes que enchem a
    barra) vai à mesa ao lado, com a resistência que ele sobe (+40% e +80% de carga). Com a carga 4 ela é 3 e 4 golpes, ×1,33: o "40% mais golpes" de 3.5 vale na carga, e o
    golpe é inteiro (DESENHO 12.3). E O CALEJO POR FAMÍLIA NA FIRMEZA (3.5): o controle de arma que pega dá +4 na Firmeza contra o feitiço da mesma família (pernas: prender e
    raízes; mana: o nó), não contra o de outra, e com o calejo de hoje vale o maior (a M21 igual)."""
    D0 = luta.D; luta.semente(5701); t1 = []; t2 = []; b1 = []; b2 = []; k = max(5 * n, 10000)
    try:
        for _ in range(k):
            S = luta.nova([_g('o atordoador', {'arma': {'aturdir': 4}})], [_g('o alvo')], quieto=True, inicio='colado'); S['mede_carga'] = {}; luta.corre(S)
            h = S['mede_carga'].get('o alvo') or []
            if len(h) >= 3: t1.append(h[0][0]); t2.append(h[1][0]); b1.append(h[0][1]); b2.append(h[1][1])
    finally: luta.D = D0
    md = lambda x: sum(x) / max(1, len(x)); m1, m2, c1, c2 = md(t1), md(t2), md(b1), md(b2)
    S = luta.nova([_g('a')], [_g('o alvo')], quieto=True); e = S['L'][1]; rs = []
    for c in (0, 1, 2): e['calejo_f']['cabeca'] = c; rs.append(luta.resistencia(S, e, 'cabeca'))
    calejo = rs[1] >= 1.4 * rs[0] - 1e-9 and rs[2] >= 1.8 * rs[0] - 1e-9
    out = [('EF6 O CALEJO: o 2º atordoar pede 1,4 vez os golpes do 1º, ou mais (a carga 4 da Rara contra a resistência 10, 14, 18...; os golpes que tiram PV entre um e outro, com a cabeça firme); e o calejo sobe a resistência 40% e 80%',
            f"{len(t1)} lutas de {k} com dois atordoares: {m1:.1f} golpes até o 1º, {m2:.1f} até o 2º (×{m2 / max(1e-9, m1):.2f}); só os que enchem a barra (o calejo sozinho): {c1:.1f} e {c2:.1f} (×{c2 / max(1e-9, c1):.2f}: "
            f"a carga 4 é inteira); a resistência {rs[0]:g}, {rs[1]:g}, {rs[2]:g}".replace('.', ','), m2 >= 1.4 * m1 and calejo)]
    import magia
    S = luta.nova([mago('m1')], [mago('m2')], quieto=True); e = S['L'][1]; fz = lambda k_: magia.firmeza(S, e, k_)
    b = {k_: fz(k_) for k_ in ('prender', 'raízes', 'nó')}
    e['calejo_f']['pernas'] = 1; pe = {k_: fz(k_) - b[k_] for k_ in b}
    e['calejo_f']['pernas'] = 0; e['calejo_f']['mana'] = 1; ma = {k_: fz(k_) - b[k_] for k_ in b}
    e['calejo_f']['mana'] = 0; e['calejo_f']['pernas'] = 1; e['calejo'] = 1; os_dois = fz('prender') - b['prender']
    certo = pe == {'prender': 4, 'raízes': 4, 'nó': 0} and ma == {'prender': 0, 'raízes': 0, 'nó': 4} and os_dois == 4
    out.append(('EF6 O CALEJO POR FAMÍLIA NA FIRMEZA (3.5): o calejo de pernas dá +4 contra o prender e as raízes e nada contra o nó; o de mana, +4 contra o nó; com o calejo de hoje, vale o maior (não somam: a M21 igual)',
                f"pernas: {pe} · mana: {ma} · o de hoje e o de pernas juntos: +{os_dois:g}".replace('.', ','), certo))
    return out


def ef7(n):
    """EF7 A ESCADA DO MEDO: o módulo 8 (30% ou mais); quem o jogador comanda contra o Medo de peça (0 fugas, 0 rendições, a luta para uma vez só por ele); a Coragem da mesma
    categoria corta metade ou mais do Medo; o pior acúmulo de uma build Rara contra Vontade 50 (no máximo 60% de quebra em 4 rodadas)"""
    out = []; k8 = max(3000, n); m = 0
    D0 = luta.D; luta.semente(5801)
    try:
        for _ in range(k8):
            S = luta.nova(um(120, 4, 4, moral='firme')(), varios(6, 30, 1, 1, pre='b')(), inicio='colado', quieto=True); luta.corre(S); r = luta.resultado(S)
            m += bool(r['fugiram'] or r['presos'])
    finally: luta.D = D0
    out.append(('EF7 O MÓDULO 8 COM A ESCADA (seis contra um muito mais forte: alguém foge ou se rende): 30% ou mais (o contrato mediu 39%; antes da escada, 52%)', f'{100 * m / k8:.0f}% de {k8} lutas', m / k8 >= 0.30))
    foge = paradas = mais_de_uma = 0; kc = max(600, n // 2)
    D0 = luta.D; luta.semente(5802)
    try:
        for _ in range(kc):
            S = luta.nova([_g('o jogador', controla=True)], [_g('o temido', {'arma': {'medo': 29}})], inicio='colado', quieto=True)
            vistas = 0
            while luta.corre(S, interativo=True) == 'parada':
                vistas += sum(1 for p in S['paradas'] if 'fraquejou (o medo das peças)' in p)
            vistas += sum(1 for p in S['paradas'] if 'fraquejou (o medo das peças)' in p)
            foge += S['L'][0]['estado'] in ('fugiu', 'rendido'); paradas += vistas; mais_de_uma += vistas > 1
    finally: luta.D = D0
    out.append(('EF7 QUEM O JOGADOR COMANDA contra o Medo Primordial (29) de peça: nunca foge nem se rende, e a luta para uma vez só por esse medo (já abalado, ele não testa mais as fontes novas)',
                f'{kc} lutas: {foge} fugas ou rendições; {paradas} paradas pelo medo das peças, mais de uma na mesma luta em {mais_de_uma}', foge == 0 and mais_de_uma == 0))
    cortes = []
    for c in (R, 4, 5, 7):
        md = TE.MEDO[c]; cg = TE.CORAGEM[c]; temido = lambda: [_g('o temido', {'arma': {'medo': md}})]
        sem = _delta(temido, lambda: [_g('o temido')], lambda: [_g('o alvo')], max(n, 2000), 5810 + c)
        com = _delta(temido, lambda: [_g('o temido')], lambda: [_g('o alvo', {'amuleto': {'coragem': cg}})], max(n, 2000), 5810 + c)
        cortes.append((c, sem, com))
    ok_c = all(com <= sem / 2 + TE.FOLGA for _, sem, com in cortes)
    out.append(('EF7 A CORAGEM CORTA O MEDO: a Coragem da mesma categoria corta metade ou mais dos pontos do Medo (o contrato: +4 corta o Medo 22 de +15,0 para +5,1)',
                ' · '.join(f"{T.CATS[c]}: o Medo {TE.MEDO[c]} dá {_f(sem)}, contra a Coragem +{TE.CORAGEM[c]}, {_f(com)}" for c, sem, com in cortes), ok_c))
    quebra = 0; kq = max(n, 2000)
    D0 = luta.D; luta.semente(5820)
    try:
        for _ in range(kq):
            S = luta.nova([veste(padrao('a build Rara', 50, fx_prova={'arma': {'medo': TE.MEDO[3]}, 'armadura': {'temivel': TE.TEMIVEL[R]}}), arma=('espada', R), armadura=('malha', R), escudo=R)],
                          [_g('o alvo', vont=50)], inicio='colado', quieto=True)
            for _ in range(4):
                if not S['fim']: luta.rodada(S)
            quebra += S['L'][1]['estado'] in ('fugiu', 'rendido')
    finally: luta.D = D0
    out.append(('EF7 O PIOR ACÚMULO DE UMA BUILD RARA contra Vontade 50 (o Temível 24 na 1ª rodada e o Medo 20 cheio; o Brado e a ameaça dos trunfos são da fase 2): no máximo 60% de quebra em 4 rodadas (o contrato, com o Brado e os trunfos: 34%)',
                f'{100 * quebra / kq:.0f}% de {kq} lutas', quebra / kq <= 0.60))
    return out


def ef8(n):
    """EF8 OS FREIOS DO APELÃO: duas peças de apelão (só a melhor acorda); a sintonia (o apelão vale 2 lugares); o Imortal com outra fonte de salvamento (um salvamento de 1 PV por
    dia, venha de onde vier, e no outro dia de novo: no mundo de prova, pela luta que volta ao estado)"""
    out = []
    duas = ficha(veste(padrao('as duas', 50, atributos={'Vontade': 100}), arma=item('arma', 5, familia='espada', efeitos=[dict(chave='golpe_do_fim')]),
                       armadura=item('armadura', 5, material='malha', efeitos=[dict(chave='imortal')]), escudo=3))
    acorda = duas['arma']['efeitos'].get('golpe_do_fim') and not any(src['efeitos'].get('imortal') for src in duas['fontes']) and duas.get('apelao_dorme') == ['armadura de malha Lendária']
    sint = ficha(veste(padrao('Vontade 50', 50, atributos={'Vontade': 50}), arma=item('arma', 5, familia='espada', efeitos=[dict(chave='golpe_do_fim')]), armadura=('malha', 3), escudo=3))
    sem_ap = ficha(veste(padrao('Vontade 50', 50, atributos={'Vontade': 50}), arma=item('arma', 5, familia='espada'), armadura=('malha', 3), escudo=3))
    # Vontade 60 (3 lugares): o Golpe do Fim acorda (2 lugares) e a armadura de Imortal e Couraça ocupa 1, acordada, com a Couraça e o Imortal dormindo: a mesma peça vale igual com 60 e com 100
    v60 = ficha(veste(padrao('Vontade 60', 50, atributos={'Vontade': 60}), arma=item('arma', 5, familia='espada', efeitos=[dict(chave='golpe_do_fim')]),
                      armadura=item('armadura', 5, material='malha', efeitos=[dict(chave='imortal'), dict(chave='couraca')]), escudo=2))
    arm60 = [src['efeitos'] for src in v60['fontes'] if src['item']['tipo'] == 'armadura']
    ok60 = not v60['dormem'] and arm60 == [{'couraca': TE.COURACA[5]}] and v60['arma']['efeitos'].get('golpe_do_fim') and v60.get('apelao_dorme') == ['armadura de malha Lendária']
    out.append(('EF8 OS FREIOS DO APELÃO: duas peças de apelão de regra, só a melhor acorda (o Imortal da armadura dorme, o resto dela vale); o apelão acordado ocupa 2 lugares na sintonia (Vontade 50: a peça e mais nenhuma Épica), e a peça cujo apelão dorme, 1 (Vontade 60: as duas Lendárias acordadas, o Imortal dormindo)',
                f"Vontade 100: acorda {'o Golpe do Fim' if acorda else 'ERRADO'}, dorme o apelão de {duas.get('apelao_dorme')}; Vontade 50 com o apelão: dormem {sint['dormem']}; sem o apelão: dormem {sem_ap['dormem']}; "
                f"Vontade 60: dormem {v60['dormem'] or 'nenhuma'}, a armadura vale {arm60}".replace('.', ','),
                bool(acorda) and len(sint['dormem']) == 3 and len(sem_ap['dormem']) == 2 and bool(ok60)))
    out.append(_imortal_no_mundo())
    return out


def _imortal_no_mundo():
    """o Imortal no mundo de prova: o personagem com a armadura e o amuleto de Imortal (dois apelões de regra: um acorda), por um fio, contra quem o derruba. A 1ª luta o salva
    (com 1 PV; o uso gasto volta ao estado no evento da luta: ['item', id, 'efeito', 'gasta', 'imortal']); no mesmo dia, a ficha da luta já não traz Imortal nenhum (o salvamento
    é um por dia, venha de onde vier: estado.lutador, salvo_dia); no dia seguinte, traz de novo, e a luta o salva de novo. (O fim de cada luta, depois do salvamento, é posto à mão.)"""
    import contextlib, io, json, os, shutil, tempfile
    import estado, ato, provas_mundo
    antes = os.environ.get('MOTOR10_MUNDO'); D0 = luta.D; pasta = tempfile.mkdtemp(prefix='m10_imortal_'); os.environ['MOTOR10_MUNDO'] = pasta; vistos = []
    def uma(E, k):
        p = E['gente']['eu']; estado.aplica(E, 'mestre', [['pessoa', 'eu', 'pv', 'soma', 3 - p['pv']]], texto='por um fio'); estado.grava(E)
        arq_c, arq_l = os.path.join(pasta, f'cen{k}.json'), os.path.join(pasta, f'luta{k}.json'); luta.semente(70 + k)
        json.dump(dict(inicio='colado', A=[dict(id='eu')], B=[dict(nome='o algoz', nivel=200, moral='firme', veste=dict(arma=['malho', 'Único'], armadura=['malha', 'Único']))]), open(arq_c, 'w', encoding='utf-8'), ensure_ascii=False)
        ato.luta_nova(E, arq_c, arq_l)
        for _ in range(40):
            E = estado.carrega(); S = json.load(open(arq_l, encoding='utf-8'))
            if S['fim'] or S['L'][0]['fx_usos'].get('imortal'): break
            ato.luta_roda(E, arq_l, []); estado.grava(E)
        E = estado.carrega(); S = json.load(open(arq_l, encoding='utf-8')); f = S['L'][0]; salvou = bool(f['fx_usos'].get('imortal'))
        if not S['fim']:                                    # posto à mão: depois do salvamento, o algoz cai e a luta volta ao estado
            S['L'][1]['estado'] = 'morto'; S['fim'] = 'A'; json.dump(S, open(arq_l, 'w', encoding='utf-8'), ensure_ascii=False); ato.luta_fecha(E, S, arq_l); estado.grava(E)
        return estado.carrega(), salvou, f['pv']
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            E = provas_mundo.vila()
            estado.aplica(E, 'gera', [['item', 'nasce', item('armadura', 5, material='malha', efeitos=[dict(chave='imortal')], dono='eu')], ['item', 'nasce', item('amuleto', 5, efeitos=[dict(chave='imortal')], dono='eu')]], texto='o Imortal de prova')
            novos = sorted(i for i, it in E['itens']['itens'].items() if it.get('dono') == 'eu' and any(e.get('chave') == 'imortal' for e in it.get('efeitos') or []))
            estado.aplica(E, 'gera', [['item', i, 'uso', 'poe', 'veste' if E['itens']['itens'][i]['tipo'] == 'armadura' else 'pescoco'] for i in novos], texto='veste'); estado.grava(E)
            E, s1, pv1 = uma(E, 1); gasto = [x.get('gasto') for i in novos for x in E['itens']['itens'][i]['efeitos'] if x.get('gasto')]
            F2 = ficha(estado.lutador(E, 'eu')); mesmo_dia = any(src['efeitos'].get('imortal') for src in F2['fontes'])
            estado.aplica(E, 'mestre', [['relogio', 6 * 4]], texto='um dia passa'); estado.grava(E)
            F3 = ficha(estado.lutador(E, 'eu')); outro_dia = any(src['efeitos'].get('imortal') for src in F3['fontes'])
            E, s3, pv3 = uma(E, 3); erro = estado.valida(E)
    finally:
        luta.D = D0; os.environ.pop('MOTOR10_MUNDO', None)
        if antes is not None: os.environ['MOTOR10_MUNDO'] = antes
        shutil.rmtree(pasta, ignore_errors=True)
    certo = s1 and len(gasto) == 1 and not mesmo_dia and outro_dia and s3 and not erro
    return ('EF8 O IMORTAL UMA VEZ POR DIA, venha de onde vier (a armadura e o amuleto de Imortal; no mundo de prova, pela luta que volta ao estado): salva na 1ª luta, não volta no mesmo dia, e no dia seguinte salva de novo',
            f"1ª luta: {'o Imortal o segurou de pé com 1 PV' if s1 else 'NÃO SALVOU'}, e o uso gasto voltou ao estado ({len(gasto)} peça marcada); no mesmo dia, a ficha {'ainda traz o Imortal (ERRADO)' if mesmo_dia else 'não traz Imortal nenhum'}; "
            f"no dia seguinte, {'traz de novo' if outro_dia else 'NÃO TRAZ'}, e a luta {'salva de novo' if s3 else 'NÃO SALVA'}; o estado {'inteiro' if not erro else 'QUEBRADO: ' + erro[0]}", certo)


def b0(n):
    """B0 A LUTA DE SEMPRE: as lutas de hoje, sem nada novo (gente, bichos e magia, ao acaso, com semente fixa), no motor de antes da fase 1b (o commit B0_REF, tirado do git numa
    pasta de rascunho) e no de agora, com a escada do medo desligada (ela é a única mudança que toca toda luta, e se mede em EF7): iguais, dado por dado"""
    import json, os, shutil, subprocess, tempfile
    aqui = os.path.dirname(os.path.abspath(__file__)); k = max(200, n // 3); tmp = tempfile.mkdtemp(prefix='m10_b0_')
    try:
        raiz = subprocess.run(['git', 'rev-parse', '--show-toplevel'], cwd=aqui, capture_output=True, text=True).stdout.strip()
        arq = subprocess.run(['git', 'archive', B0_REF, 'motor10'], cwd=raiz, capture_output=True)
        if arq.returncode or not raiz: return [('B0 A LUTA DE SEMPRE', f'sem o motor de antes no git ({B0_REF}): não conferido', False)]
        subprocess.run(['tar', '-x', '-C', tmp], input=arq.stdout, check=True)
        script = os.path.join(tmp, 'b0_lutas.py'); open(script, 'w', encoding='utf-8').write(_B0_SCRIPT)
        res = {}
        for nome, pasta in (('antes', os.path.join(tmp, 'motor10')), ('agora', aqui)):
            sai = os.path.join(tmp, f'{nome}.json')
            r = subprocess.run([sys.executable, script, pasta, str(k), sai], capture_output=True, text=True)
            if r.returncode: return [('B0 A LUTA DE SEMPRE', f'o motor {nome} quebrou: {r.stderr[-300:]}', False)]
            res[nome] = json.load(open(sai, encoding='utf-8'))
        dif = [a['i'] for a, b in zip(res['antes'], res['agora']) if a['h'] != b['h']]
    finally: shutil.rmtree(tmp, ignore_errors=True)
    return [(f'B0 A LUTA DE SEMPRE: {k} lutas ao acaso sem nada novo (gente, bichos e magia), no motor de antes ({B0_REF}) e no de agora, com a escada do medo desligada: iguais, dado por dado (o resto do banco confere que as metas de hoje passam com a escada ligada)',
             f'{k - len(dif)} de {k} lutas iguais, linha por linha' + (f'; DIFERENTES: {dif[:10]}' if dif else ''), not dif)]


_B0_SCRIPT = r"""
import sys, os, json, random, hashlib
os.chdir(sys.argv[1]); sys.path.insert(0, sys.argv[1])
N = int(sys.argv[2]); saida = sys.argv[3]
import luta, tabelas as T, tabelas_bichos as TB, tabelas_magia as TM, bichos
from pessoas import padrao, veste
from itens import item
if hasattr(luta, 'ESCADA'): luta.ESCADA = False
R = random.Random(77)
FAM = [f for f in T.FAMILIAS if f != 'punho']; MAT = list(T.MATERIAIS); ESP = list(TB.ESPECIES); TRADS = list(T.TRADICOES)
POR_TRAD = {t: [k for k, v in T.FEITICOS.items() if v['de'] in (t, 'todas') and TM.FEITICOS[k]['tipo'] != 'rito'] for t in TRADS}
FORMA = {'arcano': ['varinha', 'cajado'], 'fé': ['símbolo'], 'verde': ['cajado'], 'pacto': ['talismã']}
def pessoa(nome):
    niv = R.choice([1, 5, 12, 20, 35, 50, 80, 150, 300]); fam = R.choice(FAM); cat = R.randint(0, 7); kw = {}
    if R.random() < .3: kw['linha'] = 'trás'
    if R.random() < .2: kw['moral'] = 'firme'
    ef = [dict(chave=R.choice(['leve', 'nao_quebra']))] if R.random() < .2 else []
    p = padrao(nome, niv, molde=R.choice(list(T.MOLDES)), **kw)
    arma = item('arma', cat, familia=fam, efeitos=ef); arm = None; elmo = None; esc = None
    if R.random() < .85:
        c = R.randint(0, 7); efa = [dict(chave='firme')] if R.random() < .2 else []
        arm = item('armadura', c, material=R.choice(MAT), efeitos=efa)
        if R.random() < .7: elmo = (R.choice(MAT), R.randint(0, 7))
    if T.FAMILIAS[fam]['maos'] == 1 and R.random() < .6: esc = R.randint(0, 7)
    if R.random() < .15: arma['dur'][0] = R.randint(0, 2)
    return veste(p, arma=arma, arma2=(R.choice(['adaga', 'espada', 'maça']), R.randint(0, 5)) if R.random() < .4 else None, armadura=arm, elmo=elmo, escudo=esc)
def bicho(nome):
    mais = {}
    if R.random() < .3: mais['tamanho'] = R.choice(list(TB.TAMANHOS))
    if R.random() < .3: mais['tracos'] = R.sample(list(TB.TRACOS), R.randint(0, 4))
    if R.random() < .2: mais['cat'] = R.randint(0, 7)
    return bichos.bicho(R.choice(ESP), nome=nome, **mais)
def lancador(nome):
    t = R.choice(TRADS); niv = R.choice([12, 35, 50, 80])
    p = padrao(nome, niv, molde=R.choice(list(TM.MOLDES)), maestria={t: R.choice([2, 4, 6]), 'maça': 2, 'espada': 2}, feiticos=R.sample(POR_TRAD[t], R.randint(1, min(3, len(POR_TRAD[t])))), tradicao=t,
               **({'carga': {'cura:1': 2}} if R.random() < .4 else {}))
    return veste(p, arma=(R.choice(['espada', 'maça']), R.randint(0, 4)) if R.random() < .5 else None, armadura=(R.choice(MAT), R.randint(0, 4)), foco=(R.choice(FORMA[t]), R.randint(0, 4)), amuleto=R.randint(0, 4) if R.random() < .6 else None)
def cena(i):
    tipo = i % 3
    faz = pessoa if tipo == 0 else (lambda n: R.choice([pessoa, bicho])(n)) if tipo == 1 else (lambda n: R.choice([pessoa, lancador, lancador])(n))
    A = [faz(f'a{k}') for k in range(R.randint(1, 4))]; B = [faz(f'b{k}') for k in range(R.randint(1, 5))]
    if R.random() < .5: B[0]['lider'] = True
    lugar = {}
    if R.random() < .3: lugar['largura'] = R.randint(1, 3)
    return A, B, dict(inicio=R.choice(['longe', 'perto', 'colado']), lugar=lugar, tempo=R.sample(list(T.TEMPO), R.randint(0, 1)), surpresa=R.choice([None, None, 'A', 'B']))
out = []
for i in range(N):
    luta.semente(5000 + i); A, B, kw = cena(i)
    S = luta.nova(A, B, quieto=False, **kw); luta.corre(S)
    txt = '\n'.join(S['log']) + f"\nFIM {S['fim']} {S['r']}"
    out.append(dict(i=i, h=hashlib.sha1(txt.encode()).hexdigest()))
json.dump(out, open(saida, 'w'), ensure_ascii=False)
"""


def b3(n):
    """B3 O ITEM DECIDE (na fase 1b, o sistema é o dos efeitos de item): o topo (o conjunto Raro com tudo cheio, os mais fortes) contra o conjunto uma acima sem nada (60% ou
    mais) e contra o conjunto DUAS acima (85% ou mais)"""
    nn = max(n, 2000); um_ = _conjunto(nn, R + 1, 5301); dois = _conjunto(nn, R + 2, 5302)
    return [('B3 O ITEM DECIDE: o topo dos efeitos de item (o conjunto Raro com tudo cheio) contra o conjunto uma acima sem nada (60% ou mais) e contra o DUAS acima (85% ou mais)',
             f"uma acima vence {um_:.1f}% · duas acima, {dois:.1f}%".replace('.', ','), um_ >= 60 - TE.FOLGA and dois >= 85 - TE.FOLGA)]


def efeitos(n):
    """o bloco EF da fase 1b (DESENHO 10): B0, EF1 a EF8, B3 (o B1 é o provas_ano, que o provas_mundo roda)"""
    out = []
    for nome, f in (('B0', b0), ('EF1', lambda n_: ef1(n_)[0]), ('EF2', ef2), ('EF3', ef3), ('EF4', ef4), ('EF5', ef5), ('EF6', ef6), ('EF7', ef7), ('EF8', ef8), ('B3', b3)):
        try: out.extend(f(n))
        except (SystemExit, Exception) as e:
            import traceback; out.append((f'{nome} (a fase 1b)', f'A PROVA QUEBROU: {type(e).__name__}: {e} · {traceback.format_exc().splitlines()[-3].strip()}', False))
    return out


def _alisa(v):
    """a linha medida, ALISADA para a mesa: a regressão isotônica (juntar os vizinhos que descem, pela média, até a linha não descer de uma categoria para a de cima: o efeito
    só cresce com a categoria) e sem negativo (o efeito não tira vitória de quem o tem: o negativo é o ruído de poucas lutas por célula, perto de ±2,5 pontos com 600)"""
    xs = [(i, x) for i, x in enumerate(v) if x is not None]; blocos = []
    for i, x in xs:
        blocos.append([x, 1, [i]])
        while len(blocos) > 1 and blocos[-2][0] / blocos[-2][1] > blocos[-1][0] / blocos[-1][1]:
            b = blocos.pop(); blocos[-1][0] += b[0]; blocos[-1][1] += b[1]; blocos[-1][2] += b[2]
    out = [None] * len(v)
    for soma, q, ids in blocos:
        for i in ids: out[i] = round(max(0.0, soma / q), 1)
    return tuple(out)


def tabela_pontos(n):
    """A TABELA DO BANCO POR NÍVEL (4.2: "no seu nível, perto de +X pontos de vitória"): cada efeito de número nas 8 categorias, nos níveis 10, 20, 50 e 150 (o duelo de iguais
    de cada nível, a mão típica dele, tudo Raro; no cenário do EF1), alisada (_alisa). Devolve o dicionário que vai no tabelas_efeitos.PONTOS"""
    tab = {}
    for i, k in enumerate([k for k in TE.EFEITOS if TE.de_numero(k)]):
        cru = {nv: _ef1_linha(k, n, 3000 + 17 * i, nivel=nv) for nv in TE.NIVEIS_PONTOS}
        tab[k] = {nv: _alisa(cru[nv]) for nv in TE.NIVEIS_PONTOS}
        print(f'  {k} (medido): ' + ' | '.join(f"{nv}: {tuple(None if x is None else round(x, 1) for x in cru[nv])}" for nv in TE.NIVEIS_PONTOS), flush=True)
        print(f'  {k} (alisado): ' + ' | '.join(f"{nv}: {tab[k][nv]}" for nv in TE.NIVEIS_PONTOS), flush=True)
    return tab


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 600
    luta.semente(10); ok = 0; tot = 0
    if 'efeitos' in sys.argv[1:]:                           # (a parte 2, fase 1b) só o bloco EF (2.000 lutas por linha de padrão); `efeitos tabela`: a tabela por nível do tabelas_efeitos.PONTOS
        n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 2000
        if 'tabela' in sys.argv[1:]:
            print(f'A TABELA POR NÍVEL (tabelas_efeitos.PONTOS) · {n} lutas por célula\n'); tab = tabela_pontos(n); print('\nPONTOS = ' + repr(tab)); return True
        print(f'BANCO DE PROVAS DO MOTOR 10 · só A FASE 1b (a base da luta e os efeitos de item: B0, EF1 a EF8, B3) · {n} lutas por linha\n')
        for nome, deu, passa in efeitos(n):
            ok += passa; tot += 1
            print(f"  {'passa' if passa else 'FALHA'}  {nome}: {deu}", flush=True)
        print(f'\n{ok} de {tot} metas passam.')
        return ok == tot
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
    ne = max(n, 2000)                                       # o contrato (seção 10) mede as metas da fase 1b com 2.000 lutas por linha (o modo longo, 20.000), mesmo no banco de 600
    print(f'\nA PARTE 2, FASE 1b (a base da luta e os efeitos de item; DESENHO 10: B0, EF1 a EF8, B3; {ne} lutas por linha, como no contrato; só elas: `provas.py 2000 efeitos`)')
    for nome, deu, passa in efeitos(ne):
        ok += passa; tot += 1
        print(f"  {'passa' if passa else 'FALHA'}  {nome}: {deu}", flush=True)
    print(f'\n{ok} de {tot} metas passam.')
    return ok == tot


if __name__ == '__main__':
    sys.exit(0 if main() else 1)
