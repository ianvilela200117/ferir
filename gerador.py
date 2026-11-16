#!/usr/bin/env python3
"""Motor de Mundo v5. Geradores do mundo (Partes XIV, XVI e XXIII). Dados verdadeiros (secrets).
Uso:
  python3 gerador.py material [CATEGORIA|-] [N] [essencia=X] [origem=metal|pedra|planta|monstro|essencia]
  python3 gerador.py monstro  [CATEGORIA|-] [N] [essencia=X] [habitat=X]
  python3 gerador.py npc      [N]                  NPC vivo: desejo, ambição, medo, segredo, linha vermelha, dilema, traços
  python3 gerador.py missao   [GRAU|-] [N]         missão no formato de Satisfy (graus F a SSS)
  python3 gerador.py culto    [N]
  python3 gerador.py vilao    [N]
  python3 gerador.py lugar    [N]
  python3 gerador.py novidade [N]                  o que entra de novo nesta sessão (Regra da Novidade, XXI.6)
  python3 gerador.py essencias                     lista as 24 Essências
CATEGORIA: Comum Incomum Raro Epico Unico Lendario Mitico Primordial (sem acento). "-" sorteia.
Tudo o que for gerado e entrar em jogo é registrado no estado (Cânone, XXI.6). Nada gerado contradiz o que já existe."""
import secrets, sys
 
def d(n): return secrets.randbelow(n) + 1
def esc(lst): return lst[secrets.randbelow(len(lst))]
def esc_n(lst, n):
    pool = list(lst); out = []
    for _ in range(min(n, len(pool))):
        x = esc(pool); pool.remove(x); out.append(x)
    return out
 
CATS = ['Comum', 'Incomum', 'Raro', 'Epico', 'Unico', 'Lendario', 'Mitico', 'Primordial']
NOME_CAT = dict(zip(CATS, ['Comum', 'Incomum', 'Raro', 'Épico', 'Único', 'Lendário', 'Mítico', 'Primordial']))
# magnitude por categoria: bônus fixo {b} e dado {d}
MAG = {'Comum': (0, '—'), 'Incomum': (1, '1d4'), 'Raro': (2, '1d6'), 'Epico': (3, '2d6'), 'Unico': (5, '3d6'),
       'Lendario': (8, '5d6'), 'Mitico': (12, '10d6'), 'Primordial': (20, '20d6')}
PRECO = {'Comum': '10-15/kg', 'Incomum': '40-60/kg', 'Raro': '150-250/kg', 'Epico': '600-1.000/kg', 'Unico': '2.500-4.000/kg',
         'Lendario': '10.000+/kg, só em leilão', 'Mitico': 'sem mercado', 'Primordial': 'sem mercado'}
 
# ESSÊNCIA: (na arma, na armadura, no ofício, defeito, oposta)
ESS = {
 'Fogo':     ('o golpe queima: +{d} de fogo', 'RD {b} contra fogo e frio', '+{b} em Processo na têmpera', 'aquece na mão; molhado, racha', 'Gelo'),
 'Gelo':     ('o golpe congela: o alvo perde {b} de Defesa por 1 rodada', 'RD {b} contra fogo', 'tempera sem empenar: +{b} em Técnica', 'quebradiço no calor', 'Fogo'),
 'Vento':    ('alcance +{b} m; o golpe empurra {b} m', '+{b} de Defesa contra projéteis', 'a peça sai {b10}% mais leve', 'leve demais: −1 no dano de esmagamento', 'Terra'),
 'Terra':    ('o golpe derruba (Vigor contra CD {cd})', 'RD +{b}', '+{b} em Matéria', 'pesa o dobro', 'Vento'),
 'Agua':     ('o golpe atravessa escudos: ignora {b} de Defesa', 'RD {b} contra fogo e veneno', '+{b} no Acaso (a água perdoa)', 'enferruja fora do óleo', 'Raio'),
 'Raio':     ('+{d} de raio, que salta para um segundo alvo', 'quem golpeia o portador leva {b2}', '+{b} em Processo (forja rápida)', 'atrai tempestade', 'Agua'),
 'Vida':     ('cada golpe que fere cura o portador em {b2}', 'cura {d} PV por hora; Sangrando para sozinho', 'peças e poções de cura: +{b} em Técnica', 'atrai mosca e verme; apodrece se ficar sem uso', 'Podridao'),
 'Podridao': ('a ferida infecciona (Vigor contra CD {cd})', 'RD {b} contra doença e veneno', 'dissolve impurezas: +{b} em Matéria', 'cheiro de morte; animais fogem', 'Vida'),
 'Sangue':   ('+{d} contra quem já sangra', '+{b} nos testes de morte do portador', 'laço de sangue: nas mãos do dono, +{b} em um teste por dia', 'pede sangue: 1 PV por dia', 'Luz'),
 'Sombra':   ('no escuro: +{b} no ataque e o alvo não vê de onde vem', '+{b} em Furtividade e na Defesa no escuro', 'a peça não brilha nem faz som', 'enfraquece ao sol: −{b} de dia', 'Luz'),
 'Luz':      ('cega por 1 rodada com 18 a 20', 'revela invisíveis num raio de {b10} m', '+{b} em Técnica (a luz mostra o defeito)', 'denuncia o portador no escuro', 'Sombra'),
 'Som':      ('o grito do metal atordoa (Vontade contra CD {cd})', 'ouve passos a {b10} m', 'afina a peça: +{b} em Processo', 'canta quando se move', 'Silencio'),
 'Silencio': ('o golpe não faz som: +{b} contra quem não viu o portador', 'imune a magia de voz até o {c}º círculo', 'oficina sem barulho: o turno rende 1 hora a mais', 'o portador ouve mal', 'Som'),
 'Mente':    ('o alvo hesita: −{b} na próxima ação', '+{b} contra medo e encanto', '+{b} em Técnica (a mão lembra cada golpe)', 'sussurra à noite', 'Fome'),
 'Tempo':    ('uma vez por luta, um ataque a mais', 'uma vez por dia, desfaz um golpe recebido', 'a peça fica pronta {b10}% mais rápido', 'envelhece o portador 1 dia por uso', 'Sorte'),
 'Peso':     ('dano +{b2}, mas −1 no ataque', 'não pode ser derrubado nem empurrado', '+{b} em Matéria', 'afunda na água, quebra pontes', 'Vento'),
 'Sal':      ('fere mortos e espíritos com dano dobrado', 'nada morto atravessa o portador', 'conserva: a peça nunca enferruja nem apodrece', 'seca a pele do portador', 'Agua'),
 'Forca':    ('+{b5} em Força enquanto empunha', '+{b5} em Vigor enquanto veste', '+{b} em Técnica pesada', 'cansa: −1 por hora de uso contínuo', 'Fome'),
 'Veneno':   ('envenena: {d} por rodada até passar em Vigor contra CD {cd}', 'imune a venenos até a categoria da peça', '+{b} em alquimia (destila)', 'mata a planta onde encosta', 'Vida'),
 'Sorte':    ('o 19 natural também é crítico', '+{b} num teste por dia, à escolha', '+{b} no Acaso', 'a sorte cobra: +1 de Revés por semana', 'Tempo'),
 'Elo':      ('o golpe corta laços mágicos e encantamentos (Romper contra CD da magia)', 'sente aliados com Laço 3 ou mais', '+{b} em Infusão e Encantamento', 'prende o dono: perder a peça dói (Vontade contra 20 ou Atordoado 1 dia)', 'Fome'),
 'Metal':    ('quebra armas de categoria igual ou menor com 20 natural', 'RD +{b} contra lâminas', '+{b} em Matéria e Processo', 'pesado e frio', 'Podridao'),
 'Fome':     ('rouba {b2} PV a cada golpe que fere', 'devora uma magia que o toca, uma vez por dia', 'devora impurezas: +{b} em Matéria, mas gasta o dobro de carvão', 'tem fome: precisa ser alimentado de sangue ou magia toda semana', 'Vida'),
 'Espinho':  ('o golpe prende como raiz (Força contra CD {cd})', 'quem agarra o portador sangra {b2}', 'cresce: a peça se conserta 1 de durabilidade por dia', 'floresce na primavera e pesa', 'Fogo'),
}
SLOTS = {'ofensa': 0, 'defesa': 1, 'oficio': 2}
 
ORIGEM = {
 'metal':    ['veio profundo', 'veio raso', 'ferro de pântano', 'pepita de rio', 'metal caído do céu', 'escória de uma forja antiga'],
 'pedra':    ['cristal de geodo', 'pedra de vulcão', 'mármore de fundo de lago', 'pedra que cresce em caverna', 'vidro de raio'],
 'planta':   ['madeira de árvore antiga', 'resina', 'raiz de pântano', 'flor de altitude', 'fungo de caverna', 'casca de árvore morta-viva'],
 'monstro':  ['couro', 'osso', 'escama', 'sangue', 'glândula', 'pena', 'chifre'],
 'essencia': ['névoa colhida', 'água de fonte', 'cinza de incêndio antigo', 'luz presa em vidro', 'orvalho de campo de batalha'],
}
SIL1 = ['kre', 'var', 'thu', 'mor', 'sel', 'dra', 'ul', 'vey', 'ha', 'gor', 'ith', 'bra', 'nes', 'quo', 'fen', 'or', 'zai', 'lum', 'kas', 'ery']
SIL2 = ['kos', 'nar', 'eth', 'vil', 'ra', 'dun', 'mir', 'ssa', 'gal', 'ron', 'ine', 'tor', 'ula', 'ek', 'ast', 'ium', 'ade', 'ol']
def nome(): return (esc(SIL1) + esc(SIL2)).capitalize()
 
def efeito(e, cat, slot):
    b, dd = MAG[cat]
    return ESS[e][SLOTS[slot]].format(b=b, b2=b * 2, b5=b * 5, b10=b * 10, cd=10 + 2 * b, d=dd, c=max(1, min(9, CATS.index(cat) + 1)))
 
def material(cat=None, essencia=None, origem=None):
    cat = cat or esc(CATS[1:7])
    origem = origem or esc(list(ORIGEM))
    i = CATS.index(cat)
    e1 = essencia or esc(list(ESS))
    ess = [e1]
    if i >= 3 and d(6) >= 4:
        ess.append(esc([x for x in ESS if x not in (e1, ESS[e1][4])]))
    dureza, maleab, cond = d(6) + i, d(6), d(6) + i
    out = {
        'nome': nome(), 'categoria': NOME_CAT[cat], 'origem': f'{origem} ({esc(ORIGEM[origem])})',
        'essência': ' + '.join(ess), 'oposta': ESS[e1][4],
        'propriedades': f'dureza {dureza} · maleabilidade {maleab} · condutividade mágica {cond}',
        'na forja': f'Matéria {(dureza - 5) // 2:+d} · Processo {(maleab - 3) // 2:+d} · aceita infusão até o {min(9, cond)}º círculo',
        'efeitos': {}, 'defeito': ESS[e1][3], 'preço': PRECO[cat],
        'ocorrência': f'reserva {esc(["pequena", "média", "grande"])} (rolar ao achar o veio ou o ninho)',
    }
    if cat != 'Comum':
        for s in SLOTS:
            out['efeitos'][f'na {"arma" if s == "ofensa" else "armadura" if s == "defesa" else "ferramenta"}'] = efeito(e1, cat, s)
        if len(ess) > 1:
            s = esc(list(SLOTS))
            out['efeitos'][f'secundário ({ess[1]}, só {s})'] = efeito(ess[1], cat, s)
    return out
 
CORPO = ['besta', 'réptil', 'ave', 'inseto', 'aquático', 'morto-vivo', 'elemental', 'constructo', 'aberração', 'gigante', 'planta', 'espírito']
TAMANHO = ['homem', 'cavalo', 'casa', 'torre', 'colina', 'montanha']
COMPORT = ['territorial: ataca quem entra', 'migrante: segue estações e rebanhos', 'caçador: escolhe a presa e a segue por dias',
           'dorminhoco: acorda com barulho, sangue ou magia', 'colmeia: obedece a uma rainha', 'inteligente: negocia, guarda rancor, tem plano',
           'necrófago: segue batalhas e pestes', 'guardião: protege um lugar ou uma coisa', 'faminto: desce às aldeias no inverno',
           'servo: alguém (culto, mago, Lendário) o controla']
HABITAT = ['pântano', 'montanha', 'floresta antiga', 'lago gelado', 'deserto de sal', 'cavernas', 'ruínas', 'rio', 'costa', 'planície', 'tundra', 'vulcão']
TRACOS = ['couraça (RD +categoria × 3)', 'regenera (cura nível ÷ 2 PV por rodada, menos contra a Essência oposta)', 'voa', 'veneno no golpe',
          'olhar paralisante (Vontade contra CD 10 + nível ÷ 10)', 'muitas cabeças ou membros (+1 ataque por rodada)', 'camuflagem (desvantagem para achá-lo)',
          'grito que causa medo (Vontade ou Amedrontado)', 'sopro em cone de 9 m (Essência)', 'escava ou nada', 'sentido sísmico (nunca é surpreendido)',
          'imune a armas duas categorias abaixo da categoria dele', 'carrega doença', 'invoca crias (1d6 por luta)', 'reflete magia com 18 a 20',
          'devora metal (com 1 natural de quem o fere, a arma perde 1 categoria)', 'muda de forma', 'fala e mente']
NIVEL = {'Comum': (1, 10), 'Incomum': (10, 30), 'Raro': (30, 70), 'Epico': (70, 160), 'Unico': (110, 200),
         'Lendario': (150, 300), 'Mitico': (250, 400), 'Primordial': (350, 500)}
PVMULT = {'Comum': 5, 'Incomum': 6, 'Raro': 8, 'Epico': 15, 'Unico': 20, 'Lendario': 25, 'Mitico': 100, 'Primordial': 300}
MULT = {'Comum': 1, 'Incomum': 1.5, 'Raro': 2.5, 'Epico': 5, 'Unico': 10, 'Lendario': 25, 'Mitico': 100, 'Primordial': 500}
BONUS = {'Comum': 2, 'Incomum': 4, 'Raro': 6, 'Epico': 10, 'Unico': 15, 'Lendario': 20, 'Mitico': 30, 'Primordial': 50}
RD = {'Comum': 0, 'Incomum': 1, 'Raro': 3, 'Epico': 6, 'Unico': 12, 'Lendario': 25, 'Mitico': 50, 'Primordial': 100}
NTRACOS = {'Comum': 0, 'Incomum': 1, 'Raro': 1, 'Epico': 2, 'Unico': 3, 'Lendario': 4, 'Mitico': 5, 'Primordial': 6}
PARTES = {'couro ou escama': 'defesa', 'osso ou presa': 'ofensa', 'chifre ou garra': 'ofensa', 'sangue ou ícor': 'oficio',
          'glândula': 'oficio', 'olho': 'defesa', 'pena ou pelo': 'defesa'}
QTD = {'homem': 1, 'cavalo': 2, 'casa': 5, 'torre': 15, 'colina': 50, 'montanha': 200}
DADO = {'homem': '1d8', 'cavalo': '1d10', 'casa': '1d12', 'torre': '2d10', 'colina': '3d10', 'montanha': '4d12'}
 
def monstro(cat=None, essencia=None, habitat=None):
    cat = cat or esc(CATS[1:7]); i = CATS.index(cat)
    lo, hi = NIVEL[cat]; nv = lo + secrets.randbelow(hi - lo + 1)
    e = essencia or esc(list(ESS))
    tam = esc(TAMANHO[i // 2: i // 2 + 3])
    b, dd = MAG[cat]
    drops = []
    for p in sorted(set(esc(list(PARTES)) for _ in range(2 + i // 2))):
        m = material(cat=cat, essencia=e, origem='monstro')
        slot = PARTES[p]
        drops.append(f'{p} ×{QTD[tam] * d(4)}: «{m["nome"].lower()}» ({NOME_CAT[cat]}, {m["essência"]}), serve para '
                     f'{"armadura" if slot == "defesa" else "arma" if slot == "ofensa" else "ofício e poção"}: {efeito(e, cat, slot)}')
    if i >= 3:
        drops.append(f'CORAÇÃO: núcleo {NOME_CAT[cat]} de {e}, serve de NÚCLEO para Mítico' + (' e Primordial' if i >= 5 else ''))
    ataque = nv // 4 + BONUS[cat]
    return {
        'nome': nome(), 'categoria': NOME_CAT[cat], 'nível': nv, 'corpo': esc(CORPO), 'tamanho': tam, 'essência': e,
        'números': f'PV {nv * PVMULT[cat]} · Defesa {10 + nv // 4 + BONUS[cat]} · RD {RD[cat]} · ataque +{ataque} · '
                   f'{1 + nv // 100} ataque(s) por rodada · dano {DADO[tam]} × {MULT[cat]:g} · XP {nv * 10} (×5 chefe, ×10 Lendário ou acima)',
        'traços': esc_n(TRACOS, NTRACOS[cat]),
        'poder assinatura': f'{efeito(e, cat, "ofensa")}, em área de {3 * (i + 1)} m, uma vez a cada 3 rodadas',
        'fraqueza': f'a Essência {ESS[e][4]}: dano dobrado e corta a regeneração · e mais uma, a descobrir: {esc(["fogo comum", "luz do sol", "um som", "sal", "o próprio nome", "ferro frio", "água corrente", "a cria"])}',
        'comportamento': esc(COMPORT), 'habitat': habitat or esc(HABITAT),
        'sinal (Lei 15)': esc(['rastro de gado morto', 'cheiro de enxofre', 'silêncio dos pássaros', 'árvores marcadas', 'poços secos',
                               'gente que some à noite', 'tremores', 'névoa da cor da Essência']),
        'drops': drops,
    }
 
# ---------- NPC vivo ----------
DESEJO = ['uma casa própria', 'um título', 'vingar um morto', 'pagar uma dívida antiga', 'ser reconhecido no ofício', 'proteger um filho',
          'sair da cidade', 'casar com quem ama', 'enriquecer', 'ser perdoado', 'aprender um segredo', 'voltar para casa', 'mandar em alguém',
          'curar alguém', 'nunca mais passar fome', 'deixar uma obra']
AMBICAO = ['abrir o próprio negócio', 'tomar o lugar do chefe', 'conquistar terra', 'fundar uma escola', 'virar Lendário', 'casar acima da sua classe',
           'formar uma companhia', 'descobrir uma receita perdida', 'ganhar a guerra do seu povo', 'comprar a liberdade da família',
           'entrar numa facção que o recusou', 'derrubar quem humilhou a família']
MEDO = ['a pobreza', 'ser esquecido', 'a morte de um filho', 'a prisão', 'o fogo', 'a humilhação pública', 'a magia', 'voltar a ser escravo',
        'a velhice', 'perder a mão do ofício', 'a solidão', 'o próprio passado']
SEGREDO = ['deve a alguém perigoso', 'já matou e ninguém sabe', 'é filho de quem não deveria', 'trabalha para outra facção',
           'tem uma doença escondida', 'roubou o que tem', 'ama alguém proibido', 'sabe de um crime de alguém importante',
           'tem um filho em outra cidade', 'traiu um amigo uma vez', 'não sabe ler', 'fez um pacto']
LINHA = ['nunca machuca uma criança', 'nunca trai a família', 'nunca volta atrás numa palavra dada', 'nunca se ajoelha',
         'nunca trabalha para a facção X', 'nunca deixa um ferido para trás', 'nunca entrega um amigo à lei', 'nunca vende o ofício barato']
DILEMA = ['a ambição dele exige trair alguém que ele ama', 'o desejo dele e o do parceiro não cabem juntos',
          'cumprir a palavra vai custar a casa dele', 'a facção que o paga quer algo que fere a sua linha vermelha',
          'salvar um filho custa a vida de um estranho', 'a verdade sobre o segredo dele destruiria quem confia nele']
TRACOS_NPC = ['COVARDE', 'AVARENTO', 'ORGULHOSO', 'TEIMOSO', 'LEAL', 'CURIOSO', 'CRUEL', 'RELIGIOSO', 'AMBICIOSO', 'HONESTO', 'VINGATIVO', 'GENEROSO']
def npc():
    return {'nome': nome(), 'desejo': esc(DESEJO), 'ambição (relógio de 4)': esc(AMBICAO), 'medo': esc(MEDO), 'segredo': esc(SEGREDO),
            'linha vermelha': esc(LINHA), 'dilema que vai chegar': esc(DILEMA), 'traços': ' e '.join(esc_n(TRACOS_NPC, 2))}
 
# ---------- Missão (formato de Satisfy) ----------
GRAUS = ['F', 'E', 'D', 'C', 'B', 'A', 'S', 'SS', 'SSS']
XP_G = [50, 150, 400, 1000, 2500, 6000, 15000, 40000, 100000]
OURO_G = [10, 30, 100, 300, 1000, 3000, 10000, 30000, 'terra, título ou peça única']
TIPO = ['Normal', 'Normal', 'Encadeada (1 de 1d4+1)', 'Oculta', 'De Classe', 'De Facção', 'De Mundo', 'Emergência (prazo em horas)', 'Lendária']
OBJ = ['escoltar alguém até um lugar', 'caçar uma criatura', 'recuperar um objeto roubado', 'forjar ou entregar uma encomenda difícil',
       'descobrir quem fez algo', 'convencer alguém poderoso', 'defender um lugar por um tempo', 'achar um material raro',
       'libertar alguém preso', 'levar uma mensagem que outros querem', 'curar uma praga', 'pagar ou cobrar uma dívida']
COMPL = ['quem pediu mente sobre algo', 'outra facção quer o contrário', 'o prazo é menor do que parece', 'o alvo tem um motivo bom',
         'um rival também aceitou', 'a recompensa não existe mais', 'tem um monstro no caminho', 'um aliado vai ser posto em risco']
EXTRA = ['item da categoria do grau', 'receita (fragmento ou esboço)', 'um Favor com nome', '+1 de Reputação com uma facção',
         '1 ponto de Trilha', 'um título', 'informação do Envelope', 'material da categoria do grau']
PENAL = ['quem pediu morre ou se perde', 'Reputação −1 a −2 com quem pediu', 'a região piora um passo', 'uma facção ganha um segmento',
         'perde um item ou o adiantamento em dobro', 'o rival ganha o feito e a Fama']
def missao(grau=None):
    g = GRAUS.index(grau) if grau in GRAUS else secrets.randbelow(7)
    oculto = d(6) >= 4
    return {
        '[MISSÃO]': nome() + ' (o Mestre dá o nome pela ficção)', 'dificuldade': GRAUS[g] + '  (pela razão Ameaça ÷ régua, Parte XVI.6)',
        'tipo': esc(TIPO), 'objetivo': esc(OBJ), 'complicação escondida (Envelope)': esc(COMPL),
        'prazo': f'{d(6) + g} dias', 'recompensa': f'{XP_G[g]} XP · {OURO_G[g]} de ouro · ' + ('??? (revelada ao concluir)' if oculto else esc(EXTRA)),
        'penalidade se falhar': esc(PENAL), 'quem oferece': 'um NPC ou um sinal no mundo, nunca do nada (XVI.6)',
    }
 
# ---------- Culto, vilão, lugar ----------
def culto():
    return {'nome': 'Culto ' + esc(['da', 'do']) + ' ' + nome(), 'adora': esc(['um monstro Mítico adormecido', 'um deus morto', 'a praga', 'um Lendário morto',
            'uma Essência (' + esc(list(ESS)) + ')', 'o fim do mundo', 'um rei antigo', 'a fome']),
            'promete': esc(['cura', 'riqueza', 'vingança', 'vida eterna', 'terra', 'o fim das dívidas', 'poder sobre os mortos']),
            'sinal': esc(['tatuagem na palma', 'fita de cor', 'olhos pintados', 'dente arrancado', 'cheiro de incenso', 'moeda furada']),
            'células': f'{d(4) + 1} cidades', 'líder': f'nível {50 + d(20) * 10}, classe Rara a Lendária', 'rito': esc(['sacrifício', 'jejum', 'veneno', 'febre', 'sangue', 'silêncio', 'roubo de crianças', 'queima de livros']),
            'plano (relógio de 6)': esc(['acordar o que adoram', 'envenenar uma feira', 'tomar uma cidade por dentro', 'matar um herdeiro', 'abrir um selo', 'espalhar uma praga']),
            'fraqueza': esc(['a fé é mentira e o líder sabe', 'brigam pela sucessão', 'dependem de um material', 'um membro quer sair', 'o patrono cobra caro'])}
 
def vilao():
    v = npc(); v.update({
        'nível': 80 + d(30) * 10, 'obra sinistra (relógio de 8)': esc(['conquistar uma região', 'acabar com uma raça ou fé', 'forjar uma arma Mítica proibida',
            'virar imortal', 'comprar o reino', 'trazer de volta um morto amado', 'quebrar um pacto antigo', 'vingar o povo dele']),
        'por que é humano': esc(['perdeu tudo para quem hoje é herói', 'acredita salvar mais gente do que mata', 'ama alguém e faz por ela',
            'foi traído pelo reino', 'tem medo de morrer', 'quer que o pai finalmente o veja']),
        'equipamento': f'{d(3)} peça(s) Lendária(s) ou Mítica(s) (o mundo também tem Míticos)', 'método': esc(['veneno', 'dinheiro', 'exército', 'magia', 'chantagem', 'monstros', 'fé', 'lei']),
        'o que o faria parar': esc(['receber o que quer de outro jeito', 'perder quem ama', 'ser desmascarado em público', 'nada'])})
    return v
 
def lugar():
    return {'nome': nome(), 'o que era': esc(['mina', 'templo', 'forte', 'oficina de mestre morto', 'cidade afundada', 'torre de mago', 'cemitério de reis', 'mercado']),
            'por que caiu': esc(['praga', 'guerra', 'monstro', 'maldição', 'dívida', 'terremoto', 'traição']),
            'o que guarda': esc(['material Raro a Lendário', 'uma receita', 'uma peça antiga', 'um núcleo', 'um prisioneiro', 'um segredo de facção']),
            'o que habita': esc(['monstro (gerar)', 'bandidos', 'mortos', 'um eremita', 'um culto', 'nada, e é isso que assusta']),
            'custo de entrar': esc(['uma luta', 'uma chave', 'uma senha', 'um teste de Vigor por hora', 'um preço a alguém', 'um sacrifício'])}
 
NOVIDADE = ['um material novo aparece à venda ou em boato (gerar material)', 'um monstro novo é avistado (gerar monstro)',
            'um NPC novo, com ambição, entra na vida de alguém próximo (gerar npc)', 'uma missão nova bate à porta (gerar missão)',
            'um lugar novo é descoberto (gerar lugar)', 'um culto mostra o sinal (gerar culto, ou avançar um existente)',
            'uma facção nova nasce de um conflito antigo', 'uma técnica, receita ou feitiço novo circula',
            'um NPC antigo volta mudado (subiu, caiu, casou, perdeu alguém)', 'uma promessa antiga cobra (de quem prometeu ou a quem)',
            'uma consequência antiga chega (de algo feito há mais de 30 dias)', 'um preço ou uma lei muda e alguém sofre com isso']
 
def show(x, ind=0):
    for k, v in x.items():
        if isinstance(v, dict):
            print(' ' * ind + f'{k}:'); show(v, ind + 2)
        elif isinstance(v, list):
            print(' ' * ind + f'{k}:')
            for i in v: print(' ' * (ind + 2) + '· ' + str(i))
        else:
            print(' ' * ind + f'{k}: {v}')
 
def main():
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    tipo = a[0]
    kv = {x.split('=')[0]: x.split('=')[1] for x in a if '=' in x}
    pos = [x for x in a[1:] if '=' not in x]
    if tipo == 'essencias':
        f = dict(b='B', b2='2B', b5='5B', b10='10B', cd='10+2B', d='D', c='C')
        print('B e D pela categoria: Incomum 1/1d4 · Raro 2/1d6 · Épico 3/2d6 · Único 5/3d6 · Lendário 8/5d6 · Mítico 12/10d6 · Primordial 20/20d6 · C = círculo')
        for k, v in ESS.items(): print(f'{k}: arma {v[0].format(**f)} · armadura {v[1].format(**f)} · ofício {v[2].format(**f)} · defeito {v[3]} · oposta {v[4]}')
        return
    if tipo == 'novidade':
        n = int(pos[0]) if pos else 1
        for _ in range(n):
            r = d(12); print(f'1d12 [{r}] {NOVIDADE[r - 1]}')
        return
    if tipo in ('material', 'monstro', 'missao'):
        arg = pos[0] if pos and pos[0] != '-' else None
        n = int(pos[1]) if len(pos) > 1 else 1
    else:
        arg = None; n = int(pos[0]) if pos else 1
    for _ in range(n):
        if tipo == 'material': show(material(arg, kv.get('essencia'), kv.get('origem')))
        elif tipo == 'monstro': show(monstro(arg, kv.get('essencia'), kv.get('habitat')))
        elif tipo == 'missao': show(missao(arg))
        elif tipo == 'npc': show(npc())
        elif tipo == 'culto': show(culto())
        elif tipo == 'vilao': show(vilao())
        elif tipo == 'lugar': show(lugar())
        else: sys.exit(__doc__)
        print('—' * 40)
 
if __name__ == '__main__':
    main()
