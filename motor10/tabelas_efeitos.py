"""tabelas_efeitos.py — MOTOR 10, A PARTE 2, FASE 1b: O CATÁLOGO DOS EFEITOS DE LUTA E A BASE DA LUTA (o contrato: projeto/etapa_efeitos/DESENHO.md, seções 3 e 4).

Nenhum número de efeito de luta mora fora desta página. Os de ferramenta (fase 1a) moram no tabelas_oficio.FERRAMENTA_EFEITOS; os da luta de antes, no tabelas.py.

A RÉGUA DE FAIXAS (3.1): a categoria da peça diz a força mais alta que cabe nela: Comum fraco (até 5 pontos de vitória), Incomum e Rara normal (até 10),
Épica e Única forte (até 20), Lendária, Mítica e Primordial apelão (até 40). "+6,2" quer dizer que quem tem o efeito vence 56,2% do duelo de iguais (nível 50, mão de
Mestre, tudo Raro, começando perto).
  O efeito de NÚMERO tem um valor por categoria (o número NUNCA se guarda na peça: valor() o tira da categoria que ela rende agora); o CHEIO leva o da categoria de cima
  (a Primordial cheia fica na Primordial). O efeito de REGRA tem força fixa e só entra da porta dela para cima.
A PILHA (3.2): dano = o de hoje × (1 + PEÇAS) × (1 + TÉCNICA) × (1 + DOM) × ESTADOS × (1 − COURAÇA), para baixo uma vez; o golpe inteiro nunca passa de 7 vezes o
mesmo golpe pela regra de hoje, com os mesmos dados (o TETO DA PILHA); os dados da arma rolam o MAIOR entre o crítico (2), o fecho e o Golpe do Fim (4), nunca mais de 4.
OS NÚMEROS FIXOS (P3): acerto, Defesa, Firmeza, Conjuração, coragem e fala somam até +8 cada, de tudo o que é novo; a resistência à carga, até +16.
A CARGA (3.4), O CALEJO POR FAMÍLIA (3.5) e A ESCADA DO MEDO (3.6): os números abaixo.
"""
import tabelas as T

CATS = T.CATS
FEM = ('Comum', 'Incomum', 'Rara', 'Épica', 'Única', 'Lendária', 'Mítica', 'Primordial')       # a categoria depois de "peça" (a frase da mesa concorda: "a peça Rara")
FORCAS = ('fraco', 'normal', 'forte', 'apelão')
FORCA_PORTA = dict(fraco=0, normal=1, forte=3, apelão=5)        # a categoria que abre a força (a mesma régua da forja: tabelas_oficio.FORCA_PORTA)
FORCA_PONTOS = dict(fraco=5, normal=10, forte=20, apelão=40)    # o teto da força em pontos de vitória (o duelo de iguais)
PISO_PONTOS = dict(fraco=0, normal=5, forte=10, apelão=20)      # o piso da força (EF2: o efeito de regra fica do piso ao teto da força dele)
FOLGA = 1                                                       # a folga do banco nas bordas da faixa (seção 10)
def forca_da_cat(cat):
    """a força mais alta que a categoria abre (a porta)"""
    return [f for f in FORCAS if FORCA_PORTA[f] <= max(0, cat)][-1]
def teto_da_cat(cat): return FORCA_PONTOS[forca_da_cat(cat)]    # o teto, em pontos de vitória, de um efeito de número nesta categoria
def cabe_forca(forca, cat, emprestado=False):
    """a força cabe na peça desta categoria? (com o DEGRAU EMPRESTADO, uma força acima da que a categoria abre)"""
    i = FORCAS.index(forca_da_cat(cat)) + (1 if emprestado else 0)
    return FORCAS.index(forca) <= min(i, len(FORCAS) - 1)

# ---------- OS EFEITOS DE NÚMERO (21): os 8 valores, da Comum à Primordial (4.2) ----------
GUME = (0.10, 0.15, 0.20, 0.30, 0.40, 0.50, 0.75, 1.00)        # o +15% é o Gume da Incomum; o +50%, o da Lendária (e o cheio da Única)
CERTEIRA = (1, 2, 2, 3, 4, 5, 6, 8)
CRITICO = ((20, 9), (20, 7), (20, 6), (19, 11), (19, 9), (18, 9), (17, 9), (17, 7))       # a face alta / o mínimo do outro dado (o de antes: 20/11; o critico_19, 19/11, é o da Épica)
VAMPIRA = (0.15, 0.25, 0.35, 0.50, 0.60, 0.75, 0.90, 1.00)
# a Sangria: a Comum faz a ferida sangrar 5 rodadas (o `sangra` de antes); da Incomum para cima, cada golpe que fere abre um filete (a fração do golpe por rodada, as rodadas);
# da Épica para cima os filetes dela somam (até o teto de filetes); da Lendária para cima, atar não os estanca (o amparo, sim)
SANGRIA = ('ferida', (0.20, 2, False, False), (0.20, 3, False, False), (0.20, 3, True, False), (0.25, 4, True, False), (0.25, 5, True, True), (1 / 3, 5, True, True), (1 / 3, 6, True, True))
ATURDIR = (None, 3, 4, 6, 8, 10, 12, 15)                        # carga de cabeça por golpe que tira PV (a Comum não tem)
MEDO = (None, 17, 18, 20, 22, 24, 26, 29)                       # quem ela fere testa a coragem contra isto (a Comum não tem)
SEGUNDO_GOLPE = (1, 2, 2, 3, 4, 5, 6, 8)                        # vezes por luta em que o golpe que acerta dá outro, de graça
PERFURA = (0.9, 0.8, 0.67, 0.6, 0.55, 0.45, 0.4, 0.35)          # contra armadura de categoria maior que a arma, a proteção conta isto (nunca abaixo de um terço: P5)
COURACA = (0.05, 0.10, 0.12, 0.20, 0.25, 0.33, 0.40, 0.50)      # dano de golpe recebido a menos (em curva com as outras couraças; teto 75%)
DEVOLVE = (0.10, 0.15, 0.20, 0.30, 0.40, 0.50, 0.65, 0.80)      # parte do dano levado que volta em quem golpeia de perto (decisão 2: o devolve vira %)
REGENERA = (0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08)     # do PV máximo por rodada (no teto da cura do dia)
TEMIVEL = (20, 22, 24, 26, 29, 31, 33, 35)                      # quem começa a luta contra o dono testa a coragem contra isto
ROBUSTA = ((3, 1), (4, 2), (6, 2), (8, 3), (10, 3), (12, 4), (14, 4), (16, 5))       # resistência à carga (metade na coragem) e fôlego máximo a mais (com o antigo Fole)
GUARDA = (1, 2, 2, 3, 4, 5, 6, 8)                               # Defesa
FIRMEZA = (1, 2, 2, 3, 4, 5, 6, 8)                              # Firmeza
CORAGEM = (2, 3, 4, 5, 6, 7, 8, 8)                              # coragem (para em +8: P3)
CONTRA = ('bicho', 'morto', 'povo', 'gente', 'dragão')          # os tipos da Caçadora (escolhidos na forja)

# ---------- O CATÁLOGO ----------
# chave: tipo ('numero' ou 'regra'), pecas (os tipos de peça em que vale), valores (só o de número) ou forca (só o de regra), nome (à mesa), faz (a frase; {v}: o número),
# e, quando há: familias (as armas em que vale), golpes (o golpe da arma), perto (não vale no arco nem na besta), pesada (só arma pesada), grupo (da pilha), familia (da carga),
# medida (os pontos de vitória do contrato: (m) medido, (c) conta, (d) desenho), cena (onde o banco o mede, EF1 e EF2), usos (por luta 'luta', por dia 'dia').
PECAS_LUTA = ('arma', 'armadura', 'escudo', 'foco', 'amuleto')
TODAS = PECAS_LUTA
EFEITOS = {
    # os de número: arma
    'gume':          dict(tipo='numero', pecas=('arma',), valores=GUME, nome='Gume', faz='dano a mais: +{v}', grupo='pecas', medida='3,6 → 30,7 (m)'),
    'certeira':      dict(tipo='numero', pecas=('arma',), valores=CERTEIRA, nome='Certeira', faz='acerto: +{v}', fixo='acerto', medida='4,0 → 23'),
    'critico':       dict(tipo='numero', pecas=('arma',), valores=CRITICO, nome='Crítico', faz='o crítico é {v} (a face alta / o mínimo do outro dado)', medida='3,0 → 33,8'),
    'cacadora':      dict(tipo='numero', pecas=('arma',), valores=GUME, nome='Caçadora', faz='dano a mais contra {contra}: +{v} (soma com o Gume)', grupo='pecas', contra=True, medida='o Gume, só contra o tipo'),
    'vampira':       dict(tipo='numero', pecas=('arma',), valores=VAMPIRA, nome='Vampira', faz='cura {v} do dano que faz (no teto da cura do dia)', medida='3,4 → 16'),
    'sangria':       dict(tipo='numero', pecas=('arma',), valores=SANGRIA, nome='Sangria', faz='{v}', medida='1,1 → 28'),
    'aturdir':       dict(tipo='numero', pecas=('arma',), valores=ATURDIR, nome='Aturdir', faz='carga de cabeça {v} por golpe que fere (cheia, atordoa: perde o turno e fica aberto)', familia='cabeca', medida='7,5 → 17,0 (m)'),
    'medo':          dict(tipo='numero', pecas=('arma',), valores=MEDO, nome='Medo', faz='quem ela fere testa a coragem contra {v} (uma vez por rodada, junto das outras fontes)', medida='4,8 → 32,0'),
    'segundo_golpe': dict(tipo='numero', pecas=('arma',), valores=SEGUNDO_GOLPE, nome='Segundo Golpe', faz='{v} vez(es) por luta, o golpe que acerta dá outro, de graça', usos='luta', medida='3,8 → 22'),
    'perfura':       dict(tipo='numero', pecas=('arma',), valores=PERFURA, nome='Perfura', faz='contra armadura de categoria maior, a proteção conta ×{v} (nunca abaixo de um terço)', medida='2 → 38', cena='acima'),
    # os de número: armadura, escudo, amuleto, foco
    'couraca':       dict(tipo='numero', pecas=('armadura',), valores=COURACA, nome='Couraça', faz='dano de golpe recebido a menos: {v}', grupo='couraca', medida='3 → 31'),
    'devolve':       dict(tipo='numero', pecas=('armadura',), valores=DEVOLVE, nome='Devolve', faz='{v} do dano levado volta em quem golpeia o dono de perto', medida='3,0 → 30'),
    'regenera':      dict(tipo='numero', pecas=('armadura',), valores=REGENERA, nome='Regenera', faz='{v} do PV máximo volta por rodada (no teto da cura do dia)', medida='1,5 → 14,7'),
    'temivel':       dict(tipo='numero', pecas=('armadura', 'escudo'), valores=TEMIVEL, nome='Temível', faz='quem começa a luta contra o dono testa a coragem contra {v}', medida='2,7 → 24'),
    'robusta':       dict(tipo='numero', pecas=('armadura',), valores=ROBUSTA, nome='Robusta', faz='{v}', fixo='resistencia', medida='a Rara corta a carga 6 de +11,2 para +10,0 (m)', cena='carga'),
    'guarda':        dict(tipo='numero', pecas=('escudo',), valores=GUARDA, nome='Guarda', faz='Defesa: +{v}', fixo='defesa', medida='3,8 → 19'),
    'firmeza':       dict(tipo='numero', pecas=('amuleto',), valores=FIRMEZA, nome='Firmeza', faz='Firmeza: +{v}', fixo='firmeza', medida='+4: 7,0 (m)', cena='magia'),
    'coragem':       dict(tipo='numero', pecas=('amuleto',), valores=CORAGEM, nome='Coragem', faz='coragem: +{v}', fixo='coragem', medida='+4 corta o Medo 22 de +15,0 para +5,1 (m)', cena='medo'),
    'guarda_magica': dict(tipo='numero', pecas=('amuleto',), valores=COURACA, nome='Guarda Mágica', faz='dano de feitiço recebido a menos: {v}', grupo='couraca', medida='15%: 6,2 (m)', cena='magia'),
    'chama':         dict(tipo='numero', pecas=('foco',), valores=GUME, nome='Chama', faz='dano de feitiço a mais: +{v}', grupo='pecas', medida='+15%: 4,6; +30%: 7,2 (m)', cena='magia'),
    'foco_certeiro': dict(tipo='numero', pecas=('foco',), valores=CERTEIRA, nome='Foco Certeiro', faz='Conjuração: +{v}', fixo='conjuracao', medida='+2: 7,4 (m)', cena='magia'),
    # os de regra (26; a Sede, o vidro e o poder de lenda ficam para a fase 5). A FORÇA DE CADA UM É A QUE O BANCO MEDE (EF2: do piso ao teto da força, com a folga), nos dois
    # sentidos: a Luz e a Aparadora subiram (forte, normal); a Desforra, o Atar, o Escudo que Conta e a Guardiã desceram ao fraco, e o Domínio ao forte (o DESENHO 12.3 o registra;
    # o Mestre confirma ou manda voltar, e a volta é afinar a regra: os números medidos estão lá)
    'leve':          dict(tipo='regra', forca='fraco', pecas=('arma', 'armadura', 'escudo', 'foco'), nome='Leve', faz='pede 20 a menos de atributo', medida='(d)'),
    'pesa':          dict(tipo='regra', forca='fraco', pecas=('arma', 'armadura', 'escudo', 'foco'), nome='Pesa', faz='pede 20 a mais de atributo (é defeito: não se escolhe)', medida='(d)', defeito=True),
    'nao_quebra':    dict(tipo='regra', forca='fraco', pecas=TODAS, nome='Não Quebra', faz='não perde durabilidade', medida='(d)'),
    'derruba':       dict(tipo='regra', forca='fraco', pecas=('arma',), nome='Derruba', faz='uma vez por luta, o golpe que fere derruba (e dá o calejo de pernas)', usos='luta', familia='pernas', medida='+3,2 (m)'),
    'firme':         dict(tipo='regra', forca='fraco', pecas=('armadura', 'escudo'), nome='Firme', faz='o dono não é derrubado', medida='(d)'),
    'luz':           dict(tipo='regra', forca='forte', pecas=TODAS, nome='Luz', faz='a peça clareia: o escuro não pesa no golpe do dono (no tiro, metade)',
                          medida='(d); o banco: +12,1 no escuro (é tirar o −4 do escuro: vale uma Certeira +4), e por isso forte, da Épica (o contrato a punha no fraco; a porta pelo banco: DESENHO 12.3)'),
    'fio_manso':     dict(tipo='regra', forca='fraco', pecas=('arma',), nome='Fio Manso', faz='o golpe que mataria quem está abaixo de 1/4 do PV o deixa caído, vivo (para fazer preso)', medida='(d)'),
    'arrancada':     dict(tipo='regra', forca='fraco', pecas=('arma', 'armadura'), nome='Arrancada', faz='uma ação a mais na primeira rodada', medida='+2,7 (m)'),
    'aparadora':     dict(tipo='regra', forca='normal', pecas=('escudo', 'arma'), familias=('espada', 'montante'), nome='Aparadora', faz='quem tem o golpe aparado pelo dono perde 1 de fôlego',
                          medida='(d); o banco: +9,8 no duelo de escudo (o golpe aparado é comum, e o fôlego acaba), e por isso normal, da Incomum (o contrato a punha no fraco; a porta pelo banco: DESENHO 12.3)'),
    'expoe':         dict(tipo='regra', forca='normal', pecas=('arma',), nome='Expõe', faz='o golpe que fere deixa o alvo exposto (+50% de dano) até o fim da rodada', medida='+7,1 (m)'),
    'ponta_certa':   dict(tipo='regra', forca='normal', pecas=('arma',), nome='Ponta Certa', faz='uma vez por luta, o golpe que errou por 5 ou menos acerta', usos='luta', medida='+5,1 (m)'),
    'desforra':      dict(tipo='regra', forca='fraco', pecas=('arma',), nome='Desforra', faz='ferido por alguém, +2 no acerto contra ele até o fim do turno seguinte', fixo='acerto',
                          medida='+5 (c); o banco: +3,4, e por isso fraco, da Comum (o contrato a punha no normal; a porta pelo banco: DESENHO 12.3)'),
    'escancara':     dict(tipo='regra', forca='forte', pecas=('arma',), nome='Escancara', faz='o golpe que fere deixa o alvo exposto (+50% de dano) até o fim da rodada seguinte', medida='+15,5 (m)'),
    'amolece':       dict(tipo='regra', forca='forte', pecas=('arma',), nome='Amolece', faz='o golpe que fere deixa o alvo amolecido (−25% de dano) até o fim da rodada seguinte', medida='+11,5 (m)'),
    'folego':        dict(tipo='regra', forca='forte', pecas=('arma',), pesada=True, nome='Fôlego', faz='o golpe da arma pesada custa 1 de fôlego a menos', medida='+13,3 (m, martelo)', cena='martelo'),
    'ceifadora':     dict(tipo='regra', forca='forte', pecas=('arma',), nome='Ceifadora', faz='quem derruba um inimigo golpeia de graça outro que alcança', medida='+15,8 no um contra dez (m)', cena='dez'),
    'varredura':     dict(tipo='regra', forca='forte', pecas=('arma',), golpes=('corte', 'impacto'), perto=True, nome='Varredura', faz='cada golpe que acerta pega também um outro inimigo colado, com metade do dano (rola o acerto dele)', medida='+14,6 no um contra dez; +11,0 no 3 contra 3 (m)', cena='dez'),
    'brasa':         dict(tipo='regra', forca='forte', pecas=('arma',), nome='Brasa', faz='cada golpe que fere abre um filete de fogo (1/5 do golpe por 3 rodadas; os de fogo somam); queima também quem não tem vida; a água e o amparo apagam', medida='+14,5 (m)'),
    'atar':          dict(tipo='regra', forca='fraco', pecas=('arma',), nome='Atar', faz='carga de mana 4 por golpe que fere (só em quem tem Mana): cheia, o alvo fica atado (o nó) 2 turnos', familia='mana', cena='magia',
                          medida='(d; o mago contra mago); o banco: +3,2 (o clérigo de maça contra o mago: o nó de hoje pesa pouco numa luta), e por isso fraco, da Comum (o contrato o punha no forte; a porta pelo banco: DESENHO 12.3)'),
    'refletora':     dict(tipo='regra', forca='forte', pecas=('escudo',), nome='Refletora', faz='uma vez por luta, o feitiço contra o dono volta em quem lançou (rola de novo, contra a defesa dele)', usos='luta', medida='(d)', cena='magia'),
    'escudo_que_conta': dict(tipo='regra', forca='fraco', pecas=('escudo',), nome='Escudo que Conta', faz='uma vez por luta (1 ação, a ordem `animar`), os aliados a 2 casas descem um degrau do medo e ganham +2 na coragem', usos='luta',
                          medida='(d; 3 contra 3); o banco: −0,5 no 3 contra 3 de Medo 20 (2.000 lutas), e por isso fraco, da Comum (o contrato o punha no forte; a porta pelo banco: DESENHO 12.3)'),
    'guardia':       dict(tipo='regra', forca='fraco', pecas=('escudo',), nome='Guardiã', faz='guardar um aliado colado não gasta a reação, uma vez por rodada',
                          medida='(d; 3 contra 3); o banco: +2,3 no 3 contra 3 (2.000 lutas; +2,6 sem o limite por rodada), e por isso fraco, da Comum (o contrato a punha no forte; a porta pelo banco: DESENHO 12.3)'),
    'golpe_do_fim':  dict(tipo='regra', forca='apelão', pecas=('arma',), nome='Golpe do Fim', faz='o crítico é 17/11 e rola os dados 4 vezes, não 2', medida='+35,2 (m)'),
    'tempestade':    dict(tipo='regra', forca='apelão', pecas=('arma',), golpes=('corte', 'impacto'), perto=True, nome='Tempestade', faz='cada golpe que acerta pega também um outro inimigo colado, com o dano inteiro', medida='+20,6 no um contra dez (m)', cena='dez'),
    'imortal':       dict(tipo='regra', forca='apelão', pecas=('armadura', 'amuleto'), nome='Imortal', faz='uma vez por dia, o dono fica com 1 PV em vez de cair (o salvamento de 1 PV é um só por dia, venha de onde vier)', usos='dia', medida='+5,6 (m): compra a vida, não a vitória'),
    'dominio':       dict(tipo='regra', forca='forte', pecas=('foco',), nome='Domínio', faz='uma vez por luta, um feitiço que o dono sabe sai sem Mana, sem ser longo, com os dados rolados duas vezes', usos='luta', cena='magia',
                          medida='(c); o banco: +11,3 no mago contra o mago (com 2 usos, +16,6; com 3, +17,6: não chega ao apelão), e por isso forte, da Épica (o contrato o punha no apelão; a porta pelo banco: DESENHO 12.3)'),
}
# OS DE ANTES (a transição, 3.7 e 9.2): nenhuma peça nova os ganha (a resposta 2a). O critico_19 fica para sempre na peça que já o tem (o Martelo Incomum de Ferord). O `sangra`
# é a Sangria Comum (3.7.3: a ferida sangra 5 rodadas): na peça Comum a entrada da 1b o converte na chave `sangria`, igual; acima da Comum ele FICA (a chave `sangria` ali daria
# a Sangria da categoria, mais forte que o de antes). O `devolve N` (fixo) vira o Devolve (o % da categoria) na entrada.
LEGADO = {
    'critico_19': dict(pecas=('arma',), nome='o 19 também é crítico', faz='o crítico é 19/11 (o de antes: o que nasceu, nasceu)', critico=(19, 11)),
    'sangra':     dict(pecas=('arma',), nome='sangra (a Sangria Comum de antes)', faz='a ferida que ela abre sangra 5 rodadas (o de antes: a Sangria Comum, que fica na peça que já o tem)', vira='sangria'),
}
def devolve_fixo_max(cat): return 4 * (cat + 1)      # (a transição) o teto do `devolve N` de antes: a validação o aceita até a entrada da 1b, e a entrada o converte em %
APELIDOS = {'gume': 'gume', 'crítico': 'critico', 'caçadora': 'cacadora', 'segundo golpe': 'segundo_golpe', 'segundo': 'segundo_golpe', 'couraça': 'couraca', 'temível': 'temivel',
            'guarda mágica': 'guarda_magica', 'guarda_mágica': 'guarda_magica', 'foco certeiro': 'foco_certeiro', 'não quebra': 'nao_quebra', 'não_quebra': 'nao_quebra',
            'fio manso': 'fio_manso', 'expõe': 'expoe', 'ponta certa': 'ponta_certa', 'fôlego': 'folego', 'escudo que conta': 'escudo_que_conta', 'guardiã': 'guardia',
            'golpe do fim': 'golpe_do_fim', 'domínio': 'dominio'}
def chave(k):
    """a chave do efeito como o jogador a escreve (com acento, espaço ou hífen): a do catálogo (ou a mesma, se não é de luta)"""
    k = str(k).strip().lower(); k2 = k.replace('-', ' ').replace('_', ' ')
    return APELIDOS.get(k, APELIDOS.get(k2, k2.replace(' ', '_')))
def de_luta(k): return k in EFEITOS
def de_numero(k): return k in EFEITOS and EFEITOS[k]['tipo'] == 'numero'
def apelao_de_regra(k): return k in EFEITOS and EFEITOS[k]['tipo'] == 'regra' and EFEITOS[k]['forca'] == 'apelão'      # a peça leva um só; ocupa 2 lugares na sintonia
def porta(k):
    """a categoria em que o efeito começa a caber: o de regra, a da força dele; o de número, a primeira em que ele tem valor (o Aturdir e o Medo, a Incomum)"""
    e = EFEITOS[k]
    if e['tipo'] == 'regra': return FORCA_PORTA[e['forca']]
    return next(i for i, v in enumerate(e['valores']) if v is not None)
def forca(k, cat):
    """a força do efeito nesta categoria: a do de regra é fixa; a do de número é a que a categoria abre"""
    e = EFEITOS[k]; return e['forca'] if e['tipo'] == 'regra' else forca_da_cat(cat)
def escolhe_nao(k): return bool(EFEITOS.get(k, {}).get('defeito')) or k in LEGADO      # o defeito (o Pesa) e os de antes não se escolhem
def valor(k, cat, cheio=False):
    """O NÚMERO do efeito na peça que rende esta categoria (cheio: o da categoria de cima; a Primordial cheia fica na Primordial). O de regra: True. None: o efeito não tem
    número nesta categoria (o Aturdir e o Medo na Comum). É a única fonte do número: a peça nunca o guarda."""
    e = EFEITOS.get(k)
    if e is None: return LEGADO[k].get('critico', True) if k in LEGADO else None
    if e['tipo'] == 'regra': return True
    return e['valores'][max(0, min(cat + (1 if cheio else 0), len(CATS) - 1))]
def cabe(k, tipo, cat, familia=None, emprestado=False):
    """o efeito cabe nesta peça? (o tipo, a arma certa, a porta pela força; com o degrau emprestado, a força de cima, com o número da categoria da peça). Devolve None ou a frase do porquê."""
    e = EFEITOS.get(k)
    if e is None: return f'"{k}" não é efeito de luta'
    if tipo not in e['pecas']: return f'{e["nome"]} não vale em {tipo} (vale em: {", ".join(e["pecas"])})'
    if tipo == 'arma' and familia in T.FAMILIAS:
        fa = T.FAMILIAS[familia]
        if e.get('familias') and familia not in e['familias']: return f'{e["nome"]} só vale na arma: {", ".join(e["familias"])}'
        if e.get('pesada') and fa['peso'] != 'pesada': return f'{e["nome"]} só vale na arma pesada (machado, martelo, montante, alabarda, malho)'
        if e.get('golpes') and fa['golpe'] not in e['golpes']: return f'{e["nome"]} só vale na arma de {" ou ".join(e["golpes"])}'
        if e.get('perto') and fa.get('distancia'): return f'{e["nome"]} é de perto: não vale no arco nem na besta'
    if e['tipo'] == 'numero':
        if valor(k, cat) is None: return f'{e["nome"]} não tem número numa peça {FEM[cat]} (começa na {FEM[porta(k)]})'
        return None
    if not cabe_forca(e['forca'], cat, emprestado):
        return f'{e["nome"]} é {e["forca"]}: a porta da peça {FEM[cat]} não abre essa força' + (' (nem com o degrau emprestado)' if emprestado else ' (fraco na Comum, normal na Incomum, forte na Épica, apelão na Lendária)')
    return None
def frase(k, cat, cheio=False, contra=None):
    """o efeito em palavras, com o número da categoria (o cheio: o da de cima)"""
    if k in LEGADO: return LEGADO[k]['faz']
    e = EFEITOS[k]; v = valor(k, cat, cheio)
    return e['nome'] + ': ' + e['faz'].format(v=diz_valor(k, v), contra=contra or 'o tipo escolhido')
def diz_valor(k, v):
    """o número à mesa: "+15%", "+2", "19/11", "carga 6", "1/5 do golpe por 3 rodadas" """
    if v is None: return '—'
    if k == 'critico': return f'{v[0]}/{v[1]}'
    if k == 'sangria':
        if v == 'ferida': return 'a ferida que ela abre sangra 5 rodadas'
        fr = '1/3' if abs(v[0] - 1 / 3) < 1e-9 else '1/4' if v[0] == 0.25 else '1/5'
        return f'cada golpe que fere abre um filete de {fr} do golpe por {v[1]} rodadas' + ('; os filetes dela somam' if v[2] else '') + ('; atar não os estanca' if v[3] else '')
    if k == 'robusta': return f'resistência à carga +{v[0]} (metade na coragem) e fôlego máximo +{v[1]}'
    if k == 'perfura': return f'{v:g}'.replace('.', ',')
    if isinstance(v, float): return f'{round(100 * v):d}%'
    return f'{v}'
def ordem_valor(k, v):
    """um número que cresce com o valor (para o maior entre duas fontes: P5)"""
    if v is True or v is None: return 0
    if k == 'critico' or (isinstance(v, tuple) and len(v) == 2 and k in ('critico', 'critico_19')): return chance_critico(v)
    if k == 'sangria': return 0 if v == 'ferida' else v[0] * v[1] + (1 if v[2] else 0) + (1 if v[3] else 0)
    if k == 'robusta': return v[0]
    if k == 'perfura': return -v                                    # a Perfura menor corta mais
    return v

# ---------- A PILHA (3.2) ----------
PILHA = dict(pecas=1.00, tecnica=0.40, dom=0.60)                # o teto de cada grupo que soma (PEÇAS: Gume, Caçadora, a Chama; TÉCNICA e DOM: fases 2 e 3)
EXPOSTO = 1.5               # o exposto leva +50% no dano de golpe e de feitiço
AMOLECIDO = 0.75            # o amolecido faz −25% de dano
COURACA_TETO = 0.75         # a couraça (em curva: 1 − (1 − a) × (1 − b)) nunca passa disto; ninguém é imune por efeito
TETO_PILHA = 7              # O TETO DA PILHA: o golpe com tudo o que é novo nunca tira mais que isto vezes o mesmo golpe pela regra de hoje, com os mesmos dados
DADOS_MAX = 4               # os dados da arma rolam o MAIOR entre o crítico (2), o fecho e o Golpe do Fim (4): nunca mais de 4 vezes
GOLPE_DO_FIM = dict(critico=(17, 11), dados=4)
CRITICO_MELHOR = (17, 7)    # P6: o crítico vale a melhor faixa entre as fontes, nunca melhor que isto
FIXO_TETO = 8               # P3: acerto, Defesa, Firmeza, Conjuração, coragem e fala: até +8 cada, de tudo o que é novo
RESIST_TETO = 16            # P3: a resistência à carga, até +16
PERFURA_PISO = 1 / 3        # P5: a Perfura (e a mira na fresta, e o Golpe de Quebra da fase 2: vale o maior) nunca deixa a proteção abaixo de um terço da que a armadura dá
def chance_critico(faixa):
    """a chance de crítico de uma faixa (a face alta, o mínimo do outro dado), nos dois d20 que abrem o golpe"""
    a, m = faixa; dentro = 21 - m; sem = max(0, a - m)
    return (dentro * dentro - sem * sem) / 400
def melhor_critico(*faixas):
    """P6: a melhor faixa entre as fontes (pela chance), nunca melhor que 17/7"""
    f = max((x for x in faixas if x), key=chance_critico)
    return (max(f[0], CRITICO_MELHOR[0]), max(f[1], CRITICO_MELHOR[1]))
def curva(*xs):
    """P4: chance e resistência em curva, com o teto da couraça"""
    r = 1.0
    for x in xs: r *= (1 - max(0.0, x))
    return min(COURACA_TETO, 1 - r)

# ---------- OS ESTADOS (3.3) ----------
PRAZO_MAX = 3               # P9: o prazo do estado soma até isto (em rodadas, contando a de agora); a potência é fixa
EXPOE_RODADAS = 1           # o Expõe: até o fim da rodada
ESCANCARA_RODADAS = 2       # a Escancara: até o fim da rodada seguinte
AMOLECE_RODADAS = 2         # o Amolece: até o fim da rodada seguinte
FILETES_MAX = 3             # cada fonte de sangue é um filete; até 3 (o quarto toma o lugar do mais fraco)
BRASA = (0.20, 3)           # o filete de fogo da Brasa: a fração do golpe por rodada, as rodadas (os de fogo somam; queima também quem não tem vida)
ATAR_SOZINHO = 0.05         # quem o jogador não comanda ata a si quando os filetes de efeito tiram isto do PV por rodada e não há inimigo colado
ATADO_TURNOS = 2            # o Atar: o alvo fica atado (o nó de hoje) tantos turnos
DESFORRA = 2                # a Desforra: o acerto a mais contra quem feriu o dono
PONTA_CERTA = 5             # a Ponta Certa: o golpe que errou por isto ou menos acerta (uma vez por luta)
FIO_MANSO = 0.25            # o Fio Manso: abaixo desta fração do PV, o golpe que mataria deixa caído e vivo
ESCUDO_CONTA = dict(casas=2, coragem=2)     # o Escudo que Conta: os aliados a tantas casas descem um degrau do medo e ganham isto na coragem
LUZ = (1.0, 0.5)            # a Luz: a parte do escuro que ela tira do golpe do dono (no golpe, no tiro)
APARADORA_RODADA = None     # a Aparadora: None, a cada golpe aparado; 'rodada', uma vez por rodada; 'luta', uma vez por luta (o fôlego que o golpe aparado tira)
GUARDIA_RODADA = 1          # a Guardiã: quantas guardas por rodada sem gastar a reação
DOMINIO_USOS = 1            # o Domínio: vezes por luta

# ---------- A CARGA (3.4) e O CALEJO POR FAMÍLIA (3.5) ----------
FAMILIAS = ('cabeca', 'pernas', 'mana')     # as barras de carga (o ânimo tem a escada no lugar da barra)
CALEJOS = FAMILIAS + ('animo',)
FAMILIA_DIZ = dict(cabeca='cabeça', pernas='pernas', mana='mana', animo='ânimo')
FEITICO_FAMILIA = {'prender': 'pernas', 'raízes': 'pernas', 'nó': 'mana'}  # a família de cada feitiço de controle (o medo e o afugentar seguem como hoje; o mau-olhado não tem família)
ESTADO_FAMILIA = {'preso': 'pernas', 'no': 'mana'}
RESIST_BASE = 6             # RESISTÊNCIA = 6 + bônus de Vigor ÷ 2 + 4 por calejo da família (+4 de saída no chefe e no bicho grande; a Robusta soma, até +16)
RESIST_CALEJO = 4
RESIST_CHEFE = 4
CALEJO_FIRMEZA = 4          # o controle de arma que pega dá +4 na Firmeza contra o feitiço da mesma família (com o calejo de hoje, vale o maior)
ATAR_CARGA = 4              # o Atar: carga de mana por golpe
FIRME_TURNOS = 2            # A CABEÇA FIRME: do atordoar até o fim do segundo turno em que o alvo volta a agir, nada soma carga de cabeça e nada lhe tira o turno pela cabeça
JANELA_TURNOS = 3           # ninguém perde mais de 1 turno em cada 3 seguidos
ABERTO = -4                 # o atordoado pela carga fica aberto (−4 na Defesa) até o fim da rodada seguinte (as penas novas de Defesa no alvo não somam: vale a pior)
def resistencia(vigor, calejos=0, chefe=False, robusta=0):
    return RESIST_BASE + (vigor // 10) / 2 + RESIST_CALEJO * calejos + (RESIST_CHEFE if chefe else 0) + min(RESIST_TETO, robusta)

# ---------- A ESCADA DO MEDO (3.6) ----------
ACUADO = -4                 # o acuado: −4 no acerto (no lugar do −2 do abalado); não avança contra quem o assustou (só segura, guarda, toma fôlego ou recua)
QUEBRA_ABALADO = 5          # o abalado que falha por isto ou mais quebra (por menos, fica acuado); o acuado que falha quebra; o firme que falha por 10 ou mais quebra (tabelas.MORAL_QUEBRA)
ACUADO_DESCE = 2            # o acuado desce a abalado depois de tantas rodadas sem susto novo
MEDO_MAIS = 1               # as fontes novas testam juntas: um teste por alvo por rodada, contra a maior CD, +1 por fonte a mais...
MEDO_MAIS_MAX = 2           # ... até +2
CALEJO_ANIMO = 4            # cada degrau que uma fonte nova faz pegar dá +4 na coragem contra as fontes novas, até o fim da luta

# ---------- QUEM ESCOLHE (5.7): o mundo escolhe sozinho pelo PAPEL do dono, se ele tem papel de luta; senão, pelo JEITO do ferreiro ----------
PAPEL_LUTA = {'guarda': 'guarda', 'capitão': 'guerreiro', 'senhor': 'guerreiro', 'nobre': 'guerreiro', 'aventureiro': 'guerreiro', 'caçador': 'caçador', 'mago': 'lança', 'sacerdote': 'lança'}
RECEITA_PAPEL = dict(guerreiro=('gume', 'critico', 'certeira'), guarda=('couraca', 'guarda', 'devolve'), caçador=('cacadora', 'gume', 'sangria'), lança=('chama', 'foco_certeiro'))
CONTRA_PAPEL = dict(caçador='bicho')        # a Caçadora que o mundo escolhe pelo papel: o caçador, contra o bicho (sem papel, o mundo não escolhe a Caçadora: ela pede um tipo)
JEITO_LUTA = dict(gume=('gume', 'critico', 'sangria', 'certeira', 'vampira', 'chama', 'expoe', 'escancara'),            # o do gume: dano, crítico, sangue
                  guarda=('guarda', 'couraca', 'firmeza', 'aparadora', 'devolve', 'guarda_magica', 'firme', 'robusta'),   # o da guarda: defesa, firmeza, aparar
                  fôlego=('leve', 'nao_quebra', 'folego', 'arrancada', 'regenera', 'foco_certeiro'),                   # o do fôlego: leveza, não quebrar, fôlego
                  tranco=('derruba', 'aturdir', 'medo', 'temivel', 'amolece', 'coragem'))                             # o do tranco: derrubar, atordoar, medo
RECEITA_AUTO = 'gume'       # `oficio.py efeito ITEM auto` na peça de luta, sem receita do jogador: a do gume na arma, a da guarda no resto (5.7)

# ---------- O QUE CADA EFEITO VALE NO NÍVEL DO DONO (4.2: "no seu nível, perto de +X pontos de vitória") ----------
# Medido pelo banco (`python3 provas.py 2000 efeitos tabela`), no duelo de iguais de cada nível (mão típica do nível, tudo Raro, perto), com o número de cada categoria posto na
# peça; o mago contra mago para os de foco e amuleto; a Perfura contra a armadura uma acima; a Robusta contra a carga 6; a Coragem contra o Medo da mesma categoria (o cenário do EF1).
# Alisada: a linha não desce de uma categoria para a de cima (a regressão isotônica) e não tem negativo: o ruído de 2.000 lutas por célula é perto de ±1,5 pontos.
# Os níveis que não estão na tabela leem o mais perto. (A tabela é medida: muda quando a regra muda, e o banco a refaz.)
NIVEIS_PONTOS = (10, 20, 50, 150)
PONTOS = {                  # {chave: {nível: (8 valores, da Comum à Primordial)}}: o banco (`provas.py 2000 efeitos tabela`, 2.000 lutas por célula), ALISADO (provas._alisa)
    'gume': {10: (5.6, 8.4, 8.5, 12.9, 16.3, 19.4, 23.8, 26.8), 20: (4.2, 7.3, 8.7, 13.9, 18.8, 20.3, 23.5, 27.0), 50: (4.9, 5.8, 7.5, 13.7, 18.0, 20.5, 26.8, 31.2), 150: (5.7, 7.7, 10.6, 14.3, 15.0, 21.0, 29.1, 33.4)},
    'certeira': {10: (1.2, 5.9, 5.9, 9.9, 13.9, 15.1, 18.1, 22.3), 20: (2.9, 5.8, 5.8, 9.5, 10.8, 16.6, 18.7, 22.5), 50: (3.2, 7.8, 7.8, 10.8, 13.5, 18.2, 20.4, 24.2), 150: (5.3, 6.3, 6.3, 11.6, 14.9, 16.9, 20.1, 23.8)},
    'critico': {10: (2.9, 6.8, 6.8, 12.3, 16.6, 24.0, 28.2, 32.8), 20: (1.9, 6.5, 6.5, 11.3, 15.9, 26.0, 29.4, 31.5), 50: (3.9, 5.0, 5.0, 14.1, 16.5, 22.8, 29.2, 34.3), 150: (5.7, 8.4, 8.4, 13.3, 18.9, 27.5, 33.3, 35.9)},
    'cacadora': {10: (7.1, 7.9, 7.9, 13.1, 16.5, 22.3, 24.4, 26.4), 20: (4.0, 8.0, 10.2, 15.3, 16.3, 20.2, 24.4, 28.8), 50: (4.6, 7.5, 8.2, 14.1, 18.2, 21.0, 26.4, 32.3), 150: (5.2, 8.1, 12.5, 14.3, 17.5, 21.0, 29.7, 35.0)},
    'vampira': {10: (1.8, 5.0, 7.5, 9.3, 9.3, 9.9, 10.3, 10.3), 20: (1.8, 2.6, 5.0, 8.5, 10.7, 11.5, 11.6, 11.6), 50: (3.2, 4.8, 6.0, 11.2, 11.2, 11.2, 11.7, 13.7), 150: (5.5, 8.9, 10.2, 15.9, 18.3, 19.9, 19.9, 19.9)},
    'sangria': {10: (1.6, 7.2, 7.2, 10.7, 13.8, 15.4, 19.2, 19.2), 20: (1.0, 7.0, 7.6, 10.2, 14.6, 18.3, 18.5, 19.5), 50: (1.7, 6.8, 6.8, 13.1, 13.3, 14.1, 18.2, 18.2), 150: (4.8, 10.4, 10.4, 15.3, 18.2, 18.7, 24.5, 25.0)},
    'aturdir': {10: (None, 2.3, 4.0, 5.6, 6.2, 9.5, 9.5, 9.5), 20: (None, 2.1, 4.2, 5.6, 8.1, 8.1, 8.1, 9.7), 50: (None, 6.5, 7.4, 10.1, 11.4, 16.0, 16.0, 18.2), 150: (None, 6.6, 8.0, 11.5, 11.5, 12.2, 13.4, 16.9)},
    'medo': {10: (None, 2.0, 2.8, 4.6, 9.1, 13.4, 16.9, 23.6), 20: (None, 1.8, 2.8, 8.0, 10.2, 14.5, 15.5, 23.0), 50: (None, 3.4, 3.4, 6.3, 9.2, 15.6, 19.6, 28.6), 150: (None, 1.8, 4.9, 5.4, 12.3, 17.5, 21.8, 28.5)},
    'segundo_golpe': {10: (3.0, 7.1, 7.1, 7.3, 10.6, 12.3, 12.3, 12.3), 20: (4.1, 7.2, 7.2, 8.9, 9.8, 12.1, 12.7, 13.0), 50: (2.0, 6.1, 6.1, 10.2, 13.3, 15.8, 17.5, 17.5), 150: (4.5, 5.8, 5.8, 8.6, 13.5, 16.0, 19.5, 20.2)},
    'perfura': {10: (1.6, 3.4, 6.7, 9.6, 13.8, 21.2, 28.8, 32.8), 20: (1.3, 3.9, 5.2, 9.5, 11.3, 20.6, 24.6, 31.1), 50: (1.6, 3.4, 5.6, 11.1, 13.5, 23.2, 30.1, 35.4), 150: (0.0, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 1.4)},
    'couraca': {10: (0.5, 6.0, 6.0, 9.5, 13.7, 19.7, 23.3, 31.8), 20: (3.4, 5.4, 6.0, 12.1, 14.7, 21.4, 26.2, 32.7), 50: (2.9, 5.0, 6.2, 12.1, 15.0, 19.5, 27.2, 34.7), 150: (2.4, 5.0, 8.4, 15.0, 17.5, 24.4, 31.0, 39.2)},
    'devolve': {10: (2.5, 3.4, 4.9, 10.0, 13.0, 17.2, 25.8, 33.3), 20: (3.0, 3.6, 6.9, 9.9, 14.8, 18.5, 24.3, 32.7), 50: (4.9, 7.8, 9.5, 13.3, 16.1, 22.5, 30.6, 36.3), 150: (2.5, 6.6, 7.6, 15.4, 21.2, 25.4, 33.9, 41.5)},
    'regenera': {10: (0.0, 2.3, 5.9, 7.8, 10.9, 10.9, 10.9, 10.9), 20: (1.9, 4.8, 6.1, 8.4, 10.2, 10.5, 10.7, 11.0), 50: (2.1, 5.4, 6.9, 8.5, 10.8, 12.1, 12.9, 13.7), 150: (2.2, 8.9, 13.5, 14.7, 16.6, 18.7, 20.2, 20.2)},
    'temivel': {10: (3.1, 3.9, 5.8, 9.6, 11.5, 15.8, 19.6, 24.2), 20: (4.0, 4.2, 8.5, 8.5, 14.0, 15.9, 18.8, 23.0), 50: (5.5, 5.5, 8.5, 10.7, 13.5, 17.5, 22.0, 24.2), 150: (1.2, 3.6, 5.0, 6.9, 11.3, 13.6, 19.8, 22.8)},
    'robusta': {10: (2.9, 2.9, 2.9, 4.7, 7.2, 7.2, 7.2, 9.2), 20: (5.1, 7.1, 7.1, 7.6, 8.4, 12.2, 12.6, 13.8), 50: (1.2, 2.6, 4.0, 4.0, 6.3, 6.3, 6.3, 8.7), 150: (4.4, 5.6, 6.7, 10.0, 11.7, 11.7, 12.1, 14.9)},
    'guarda': {10: (3.0, 5.2, 5.2, 7.6, 9.2, 11.8, 16.4, 16.6), 20: (2.9, 6.7, 6.7, 8.2, 10.2, 13.7, 14.8, 15.0), 50: (4.0, 6.6, 6.6, 8.1, 11.5, 14.3, 16.9, 21.0), 150: (3.2, 8.4, 8.4, 11.3, 17.3, 18.9, 20.7, 25.5)},
    'firmeza': {10: (0.1, 1.6, 1.6, 1.6, 2.7, 4.4, 4.8, 5.4), 20: (0.3, 2.5, 2.5, 2.8, 5.0, 5.0, 5.3, 6.2), 50: (2.6, 4.6, 4.6, 5.0, 7.6, 10.2, 13.3, 17.5), 150: (3.2, 3.2, 3.2, 5.2, 8.1, 10.5, 15.6, 21.0)},
    'coragem': {10: (1.6, 2.7, 3.9, 3.9, 7.5, 8.5, 13.9, 18.7), 20: (0.2, 0.3, 3.0, 5.3, 9.2, 12.7, 14.0, 17.4), 50: (1.3, 2.4, 5.2, 5.4, 11.2, 14.2, 16.7, 21.1), 150: (1.0, 1.8, 3.7, 10.5, 11.1, 17.9, 21.5, 22.0)},
    'guarda_magica': {10: (3.5, 3.5, 4.5, 6.6, 10.4, 12.6, 16.4, 22.5), 20: (1.1, 2.3, 2.3, 4.6, 7.7, 11.6, 17.8, 22.9), 50: (2.2, 3.0, 3.9, 7.9, 11.8, 18.0, 21.9, 29.3), 150: (2.9, 6.3, 7.8, 12.7, 16.6, 21.8, 29.2, 36.8)},
    'chama': {10: (1.0, 1.8, 6.7, 8.1, 10.5, 10.5, 14.6, 16.6), 20: (0.7, 4.6, 4.6, 8.5, 10.5, 10.5, 16.7, 17.5), 50: (5.1, 5.6, 5.6, 8.7, 12.7, 14.0, 17.7, 21.0), 150: (4.6, 7.7, 8.7, 12.5, 15.4, 19.2, 23.0, 26.0)},
    'foco_certeiro': {10: (3.3, 8.8, 8.8, 9.5, 12.1, 15.7, 18.5, 26.5), 20: (2.6, 6.9, 6.9, 11.8, 13.3, 18.0, 18.8, 23.4), 50: (5.8, 9.5, 9.5, 11.7, 14.9, 18.6, 19.8, 25.0), 150: (3.9, 8.5, 8.5, 10.1, 14.2, 18.3, 19.6, 21.5)},
}
def pontos(k, cat, nivel, cheio=False):
    """perto de quantos pontos de vitória o efeito vale no nível do dono (a tabela do banco), ou None se ela não tem a linha"""
    t = PONTOS.get(k)
    if not t: return None
    n = min(NIVEIS_PONTOS, key=lambda x: abs(x - (nivel or 50)))
    linha = t.get(n) or t.get(50)
    return None if not linha else linha[max(0, min(cat + (1 if cheio else 0), len(CATS) - 1))]
