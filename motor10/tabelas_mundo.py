"""tabelas_mundo.py — MOTOR 10: TODOS os números do mundo num lugar só (o tempo, o corpo, viver, treinar).

Os números da luta e dos itens moram no tabelas.py. Mudar o mundo é mudar esta página e rodar `provas_mundo.py`.
"""

# ---------- o tempo ----------
BLOCO_HORAS = 4
BLOCOS = ['madrugada', 'alvorada', 'manhã', 'tarde', 'entardecer', 'noite']    # 6 blocos de 4 horas; o dia começa à meia-noite
BLOCOS_DIA = len(BLOCOS)
ESCUROS = (0, 5)            # blocos sem luz: a luta ao ar livre ganha "escuro"
SEMANA = 7
ESTACAO = 91
ANO = 364
ESTACOES = ['primavera', 'verão', 'outono', 'inverno']
ESTACOES_ARQ = ['primavera', 'verao', 'outono', 'inverno']      # o nome da estação no arquivo do registro que acabou (eventos/1_verao.jsonl.gz: sem acento no nome do arquivo)
COLHEITA = [0.5, 1, 2.5, 0]

# ---------- o corpo (três medidores de 0 a 10) ----------
MEDIDORES = ['fome', 'sono', 'cansaco']
MED_MAX = 10
FOME_A_CADA = 2             # a fome sobe 1 a cada tantos blocos
REFEICAO = -3               # uma refeição tira isto da fome
SONO_ACORDADO = 1           # por bloco acordado
SONO_CAMA = -3              # por bloco dormido numa cama
SONO_CHAO = -2              # por bloco dormido no chão
ESFORCO = dict(pesado=2, leve=1, nada=0, descanso=-1)     # o cansaço que um bloco de cada tipo dá
CANSACO_CAMA = -3           # o cansaço que um bloco dormido tira (no chão: SONO_CHAO)
# a pena do corpo: vale a PIOR das três (não somam), em todo teste, no acerto e na Defesa
PENAS = dict(fome=[(7, -4), (4, -2)], sono=[(8, -4), (6, -2)], cansaco=[(9, -2)])
LIMIARES = dict(fome=(4, 7), sono=(6, 8), cansaco=(9,))   # ao cruzar um destes, a ação longa PARA
CANSACO_FOLEGO = 3          # cada tantos pontos de cansaço tiram 1 do fôlego máximo
FOLEGO_MIN = 2
FOME_PV = 0.05              # com fome 7 ou mais na virada do dia: perde esta fração do PV máximo
SONO_CAI = (8, 28)          # com sono 8 ou mais, por bloco acordado: Vontade contra isto, ou dorme ali mesmo (no chão, até o sono baixar do primeiro limiar)
CURA_BLOCO = 0.05           # PV que um bloco dormido devolve (fração do máximo), sem fome 4 ou mais
CURA_DIA = 2                # ... em no máximo tantos blocos por dia (10% por noite dormida)
FERIDA_DIAS = (7, 21)       # dias de repouso para a ferida sarar (ferida, grave)
PESADOS_SEM_REPOUSO = 2     # dia com tantos blocos pesados não conta para sarar (nem o dia em que a pessoa lutou, nem o dia em que passou um bloco ou mais numa saída ao ermo)
LUTA_CANSA = 2              # uma luta cansa isto

# ---------- o descanso em casa (quem NÃO é o personagem cuida de si quando não está em cena; o personagem nunca descansa de graça) ----------
CASA_ZERA = 3               # passados tantos blocos ou mais do último bloco em cena (o bloco em que o corpo foi mexido pela última vez): a fome, o sono e o cansaço voltam a zero (comeu e dormiu por conta própria); com menos, nada muda.
                            # Quem volta no bloco da noite e é chamado às 8h passou 3: são dois blocos inteiros em casa
CASA_NOITE = 6              # a cada tantos blocos inteiros passados (um dia): uma noite dormida de cura (CURA_BLOCO × CURA_DIA do PV máximo) e um dia de repouso nas feridas
INTEIRO_PV = 0.9            # ao abrir uma saída, a mesa diz o estado de quem vai junto se ele não está inteiro: PV abaixo desta fração do máximo, ferida aberta, ou o corpo cobrando

# ---------- viver (em prata) ----------
REFEICAO_PRECO = 1
CAMA_PRECO = 2              # por noite (paga-se ao deitar numa pousada)
CAMA_VALE = 6               # a cama paga vale tantos blocos (um dia inteiro), a contar do bloco em que se pagou, no lugar onde se pagou: dormir de novo nesse prazo não cobra
SALARIO = dict(diarista=2, aprendiz=3, oficial=6, mestre=10)      # por bloco trabalhado
JORNADA = 2                 # a jornada: o lugar paga a cada pessoa no máximo tantos blocos de serviço por dia (trabalhar e o jornal da oficina contam juntos)
ESFORCO_OFICIO = dict(diarista='pesado', aprendiz='pesado', oficial='leve', mestre='leve')

# ---------- o vocabulário comum dos bens (etapa 2: o mercado, o ofício e a caça falam a mesma língua) ----------
# a matéria de ofício tem categoria; a chave dela, na carga e no estoque, é "nome:categoria" ("metal:0", "couro:2", "osso:1")
MATERIAS = ['metal', 'couro', 'osso', 'madeira', 'erva', 'peçonha']      # a peçonha (etapa da magia): o despojo do bicho de veneno, da categoria dele até a Rara (a alquimia faz dela o veneno de lâmina)
def materia(nome, cat): return f'{nome}:{cat}'
def le_materia(chave):
    n, _, c = chave.partition(':')
    return (n, int(c)) if c.isdigit() else (chave, None)
BENS = ['comida', 'lenha', 'carvão', 'sal', 'pano', 'remédio', 'ferramenta', 'água benta', 'tocha']     # os bens sem categoria ("prata" é o dinheiro do lugar, no estoque dele); a água benta é da etapa da magia; a tocha, da 4b (arde um bloco)
# AS POÇÕES (etapa da magia): do Comum ao Raro são BENS, com a chave "nome:categoria" na carga e no estoque, como a matéria ("cura:0", "veneno:2": 1 dose de veneno = 1 golpe);
# do Épico para cima são ELIXIR, item do Livro de Itens (tipo 'elixir', com 'pocao'), contado no mundo. O nome à mesa é o daqui (estado.nome_bem)
POCOES = {'cura': 'poção de cura', 'antídoto': 'antídoto', 'veneno': 'veneno de lâmina', 'mana': 'poção de Mana', 'guarda': 'poção de guarda', 'fúria': 'poção de fúria',
          'vigília': 'poção de vigília', 'quebra-maldição': 'poção de quebra-maldição'}
POCAO_ATE = 2              # a poção é bem até o Raro; do Épico para cima, elixir
POCAO_BASE = 6             # o preço de tabela da poção Comum (vezes PECA_VEZES por categoria): é o do elixir também, pela regra do peso_da_peca
MATERIA_ATE = 2             # a matéria comum vai até o Raro; do Épico para cima a obra pede um NÚCLEO (item do Livro de Itens, tipo 'nucleo', contado no mundo)
PECA_BASE = 30              # o preço de tabela de uma peça Comum nova, em prata: o da espada, do escudo e da armadura que cobre tronco, braços e pernas (as outras: peso_da_peca)
PECA_VEZES = 6              # ... vezes isto a cada categoria
PECA_LOJA_ATE = 3           # a loja vende até o Épico; daí para cima, só leilão, encomenda ou despojo
CONSERTO_PONTO = 0.02       # consertar na oficina de outro: esta fração do preço da peça por ponto de durabilidade
PARTE_PESO = dict(cabeça=1, tronco=2, braços=1, pernas=1)      # quanto pesa cada parte do corpo numa armadura: na matéria que ela leva (o ofício) e no preço (o mercado)
CORPO_PESO = 4              # a armadura de tabela cobre tronco, braços e pernas: 4 pontos. O preço de tabela é o dela; a que cobre menos vale a proporção (o elmo: um quarto)
# a matéria de cada arma e do escudo, em unidades (na categoria da obra; do Épico para cima, matéria Rara mais um núcleo). O ofício gasta isto na obra (tabelas_oficio),
# e o mercado tira daqui o preço: A ARMA VALE PELA MATÉRIA QUE LEVA, como a armadura vale pelo que cobre
MATERIA_ARMA = {
    'adaga':    dict(metal=1),
    'espada':   dict(metal=3),
    'maça':     dict(metal=3),
    'machado':  dict(metal=2, madeira=1),
    'martelo':  dict(metal=3, madeira=1),
    'lança':    dict(metal=1, madeira=2),
    'montante': dict(metal=5),
    'alabarda': dict(metal=3, madeira=2),
    'malho':    dict(metal=4, madeira=1),
    'arco':     dict(madeira=3),
    'besta':    dict(madeira=3, metal=1),
}                                               # as mãos ("punho") não se forjam
MATERIA_ESCUDO = dict(madeira=2, metal=1)
PECA_DE_TABELA = 'espada'   # o preço de tabela (PECA_BASE, vezes PECA_VEZES por categoria) é o desta arma: as outras valem a proporção das unidades de matéria que levam
# a matéria do foco (pela forma) e do amuleto (etapa da magia): valem pela matéria que levam, como a arma
MATERIA_FOCO = {'varinha': dict(madeira=2, osso=1), 'cajado': dict(madeira=4, osso=1), 'símbolo': dict(metal=3), 'talismã': dict(osso=2, couro=1)}
MATERIA_AMULETO = dict(osso=1)
MATERIA_GAZUA = dict(metal=1)       # a gazua (etapa 4b): vale pela matéria, como a adaga (Comum 10 de prata); a forja a faz com 1 de metal da categoria
def peso_da_peca(tipo, cobre=None, familia=None, forma=None):
    """a fração do preço de tabela que uma peça vale pelo tamanho. A armadura, pelo que cobre: os pontos de corpo ÷ CORPO_PESO (o elmo: um quarto).
    A arma, o escudo, o foco e o amuleto, pela matéria que levam: as unidades de matéria ÷ as da espada (a adaga: um terço; o montante: cinco terços; o escudo: 1;
    o cajado: cinco terços; o amuleto: um terço, 10 de prata o Comum). O elixir vale o preço da poção (POCAO_BASE); o escrito, o preço de tabela.
    A arma que a tabela não conhece vale o preço de tabela. A gazua vale pela matéria (a da adaga); a chave não tem preço (a loja não a compra nem a vende)."""
    if tipo == 'chave': return 0.0
    if tipo == 'armadura': return sum(PARTE_PESO.get(x, 0) for x in (cobre or ['tronco', 'braços', 'pernas'])) / CORPO_PESO
    if tipo == 'elixir': return POCAO_BASE / PECA_BASE
    mat = MATERIA_ESCUDO if tipo == 'escudo' else MATERIA_ARMA.get(familia) if tipo == 'arma' else MATERIA_FOCO.get(forma) if tipo == 'foco' else MATERIA_AMULETO if tipo == 'amuleto' else MATERIA_GAZUA if tipo == 'gazua' else None
    return sum(mat.values()) / sum(MATERIA_ARMA[PECA_DE_TABELA].values()) if mat else 1.0
def peso_do_item(it): return peso_da_peca(it.get('tipo'), it.get('cobre'), it.get('familia'), it.get('forma'))       # o mesmo, lido de um item do Livro de Itens
OFICINA_MAX = 4             # a oficina de um lugar vai de 0 (bancada) a isto (forja mestra)
PERIGO_MAX = 3              # o perigo de um ermo vai de 1 (a borda) a isto (o coração)

# ---------- treinar ----------
MAESTRIA_BLOCOS = {2: 40, 4: 160, 6: 500, 8: 1500}       # blocos de treino ou de luta com a arma para cada grau (o ofício que ainda não tem tabela própria, como a cura, segue esta)
MAESTRIA_FEITO = 6          # deste grau para cima, além dos blocos, pede um FEITO com a arma (o mundo registra)

# ---------- os eventos (o que pode acontecer; evento fora desta lista é recusado) ----------
EVENTOS = ['tempo', 'virada', 'comer', 'dormir', 'trabalhar', 'treinar', 'descansar', 'esperar', 'vestir', 'luta', 'compra', 'venda', 'cura', 'mestre', 'gera',
           'forjar', 'consertar', 'ajustar', 'cacar', 'coletar', 'despojo', 'producao', 'consumo', 'ninhada', 'casa',
           'talento', 'estudar', 'lancar', 'rito', 'beber', 'alquimia', 'encantar', 'maldicao', 'servico', 'covil',        # os da etapa da magia (projeto/ETAPA_MAGIA.md, seção 11)
           'masmorra', 'masmorra_vida', 'dragão',        # os da etapa 4b (projeto/ETAPA_4B.md, seção 5): os atos da descida; a vida da masmorra na virada; a vida do dragão
           'viagem', 'regiao', 'frete', 'mercado', 'gente', 'noticia', 'caixa', 'missao', 'encomenda', 'furto', 'companhia']      # os da etapa 3 (projeto/ETAPA_3.md, seção 5)
NASCE = ('gera', 'mestre')  # só nestes eventos nasce lugar, nasce gente e nasce prata
NA_LUTA = ('luta', 'mestre')        # com uma luta aberta no mundo, só estes eventos entram: a luta que volta ao estado e a mão do Mestre (e a nota da saída de caça que diz que está naquela luta)
ROTINA = ('comer', 'dormir', 'descansar', 'esperar')      # o que se repete todo dia: no RETOMAR, os eventos destes tipos viram UMA linha por dia
MUNDO_SOZINHO = ('virada', 'producao', 'consumo', 'ninhada', 'casa', 'covil', 'masmorra_vida', 'dragão', 'regiao', 'mercado', 'gente', 'noticia')     # o mundo andando sozinho (o dia que vira, o lugar que produz e consome, o ermo que se refaz, quem descansou em casa): não é fato do turno, a não ser que alguém morra
RETOMAR_FATOS = 40          # o teto de linhas de fatos no RETOMAR.md; passando disso, a primeira linha diz quantos ficaram de fora e como lê-los
OFICIOS = ['forja', 'couro', 'caça', 'coleta', 'comércio', 'cura', 'alquimia', 'encanto', 'arcano', 'fé', 'verde', 'pacto', 'manha']      # os ofícios que têm maestria e treino, como as armas
                            # (maestria.forja, treino.caça); da etapa da magia: a alquimia e o encanto (sobem pela tabela da forja) e as quatro tradições (sobem pela das armas);
                            # da etapa 4b: a manha, o ofício do ladino (sobe pela das armas)
MODULOS = ['mercado', 'regiao', 'viagem', 'oficio', 'caca', 'talento', 'magia', 'magia_mundo', 'alquimia', 'encanto', 'maldicao', 'criaturas', 'masmorra', 'manha', 'povos', 'dragoes',
           'gente', 'missoes', 'caixa', 'noticias']      # a etapa 3: a região e a viagem logo depois do mercado (o dia do mercado, e então o da região); a gente, as missões, a caixa e, por último, a notícia (que anda com o que nasceu no dia)
# os módulos do mundo (o que ainda não existe fica de fora sem quebrar nada: estado.modulos). Cada um pode ter: virada(E) (roda quando o dia vira) · bloco(E, pid, esforco, dorme)
# (os efeitos de UM bloco em quem age, vai junto ou espera: a volta da Mana) · vestiu(E, pid, iid) (depois de pôr uma peça em uso) · voce(E) (linhas no "Você" da MESA) · mesa(E) ·
# so_mestre(E) (linhas para o SÓ O MESTRE) · retomar(E) (linhas para o RETOMAR.md) · recusa_fecha(E) (os motivos para o turno não fechar)
# · pode_vestir(E, pid, iid) (etapa 4b: antes de pôr uma peça em uso; devolve '' ou a frase da recusa)
OBRAS = ('forjar', 'ajustar', 'leva', 'gravar')       # os tipos de obra (a obra de vários dias): forjar e ajustar (o ofício); a leva da alquimia e a gravação do encanto (etapa da magia)

# ---------- a magia no estado (etapa da magia: o vocabulário que o gravador confere; os números de cada frente moram nas páginas delas) ----------
BANCADA_MAX = 4             # a botica, as runas e o santuário de um lugar vão de 0 a isto (como a oficina)
VOTOS = ('lâmina', 'pobreza', 'socorro')       # os votos do clérigo: não põe em uso arma de corte nem de ponta · não guarda mais de 50 de prata na virada · não recusa cura pedida
MALDICAO_TIPOS = ('míngua', 'chaga', 'azar', 'insônia', 'marca')      # o sinal e a cor da maldição (o relógio é um só, de 6 passos)
MALDICAO_ORIGENS = ('feitiço', 'bicho', 'lugar', 'peça', 'juramento')
MALDICAO_CONDICOES = ('devolver', 'matar', 'perdao', 'morte', 'sair', 'cumprir', 'queimar', 'divida')       # o que a quebra (o tipo da condição; os campos são de quem a põe)
MALDICAO_PASSOS = ['a marca', 'o peso', 'a míngua', 'a chaga', 'o fim à vista', 'a morte']                 # os passos 1 a 6 do relógio
MALDICAO_PENA = {2: -1, 3: -2, 4: -2, 5: -4}   # a pena em todo teste, pelo passo (das penas de magia vale a pior; ela soma com a pena do corpo)
MALDICAO_SEM_NOITE = 3      # deste passo em diante, a noite dormida não devolve PV
MALDICAO_SEM_SARAR = 4      # deste passo em diante, as feridas não saram e a Mana não volta fora da luta
ENJOO_PENA = -2             # quem enjoou da poção a mais (marca.enjoo = {ate: bloco}) leva isto em todo teste até aquele bloco (soma com a pena do corpo; a luta tem o mesmo número)
MALDICAO_SABE = 2           # o degrau de saber vai de 0 (não sabe) a 1 (desconfia) e 2 (sabe: alguém leu)
def encantos_max(cat): return 2 if cat >= 4 else 1      # encantos numa peça: um; dois do Único para cima
ENCANTO_VOLTA = 1           # o encanto solto volta a carregar tantos blocos depois, fora da luta
VENENO_DURA = BLOCOS_DIA    # a dose de veneno passada na lâmina seca em tantos blocos (um dia)
BENTA_DURA = 7 * BLOCOS_DIA     # a arma benta pelo clérigo vale tantos blocos (7 dias)
ESTADOS = ['vivo', 'morto']

# ---------- a etapa 4b no estado (as masmorras e o mundo de fantasia: o vocabulário que o gravador confere; os números de cada frente moram nas páginas delas) ----------
MOLDES = ('cripta', 'mina', 'ruína', 'toca', 'covil')          # os moldes da masmorra (tabelas_masmorra.MOLDES tem os números, com estas chaves)
ARMADILHAS = ('dardo', 'lâmina', 'fosso', 'pedra', 'gás', 'runa', 'alarme')      # a lista fechada (tabelas_masmorra.ARMADILHAS tem os números, com estas chaves)
ARMADILHA_ONDE = ('chão', 'guardado')                           # e "porta:SALA" (pega quem abre a porta daquela passagem)
ARMADILHA_FEITA = ('desarmada', 'disparada')                    # a armadilha resolvida fica assim (cada uma dispara uma vez)
PORTAS = ('aberta', 'fechada', 'trancada', 'emperrada', 'arrombada')     # o estado da porta de uma passagem
PORTA_MATERIAL = ('madeira', 'ferro', 'pedra')
ALARME_MAX = 5              # o alarme da masmorra vai de 0 (quieta) a isto (acordada)
ATENTOS = (-1, 0, 1)        # quem mora na sala: dormindo, à toa, alerta

# ---------- a etapa 3 no estado (a região que responde: o vocabulário que o gravador confere; os números de cada frente moram nas páginas delas; o contrato: projeto/ETAPA_3.md) ----------
TIPOS_LUGAR = ('vila', 'ermo', 'masmorra', 'sala', 'capital', 'cidade', 'aldeia', 'fronteira')       # os tipos de lugar (a fronteira: o mundo de fora, que não tem gente)
POVOADOS = ('capital', 'cidade', 'vila', 'aldeia')                 # os tipos de lugar que são povoado (têm povo, bolsa e mercado)
ROTAS = ('estrada', 'caminho', 'trilha', 'fora')                   # o tipo da rota (fora: a que sai da região)
ROTA_BLOCOS = (1, 6)                                                # os blocos de uma rota, de ponta a ponta
ROTA_EXPOE = (1, 0.3)                                               # o quanto a rota cruza o ermo dela: cruza (1) ou passa perto (0,3)
ROTA_MUDA = ('falta', 'aberta')                                     # o que muda numa rota depois de nascer, fora do Mestre (o que o carreto deixou ontem; aberta ou fechada)
SAFRA = (0.3, 1.5)                                                  # a colheita do ano de um lugar (1: a de sempre)
BANDO_MAX = 50                                                      # os salteadores contados num ermo
POS_MAX = 100                                                       # o mapa é um quadro de 0 a isto, nos dois eixos
VIAGEM_FASES = ('estrada', 'encontro', 'luta', 'acampa', 'parada')  # a fase da viagem aberta (marca.viagem)
PRECO_FAIXA = (0.6, 1.5)                                            # o fator de preço que o ferreiro diz (marca.preco)
ANIMAIS = ('mula', 'boi')                                           # o animal de carga (item tipo "animal"); o carro (tipo "carro") não tem qual
PAPEIS = ('alcaide', 'taverneiro', 'caçador', 'lavrador', 'ferreiro', 'mercador', 'guarda', 'curandeiro', 'lenhador', 'mestre ferreiro', 'encantador', 'capitão',
          'sacerdote', 'caravaneiro', 'ladino', 'aprendiz', 'mago', 'bruxa', 'clérigo', 'alquimista', 'nobre', 'viajante')      # o papel da gente com nome (B1 pode acrescentar os seus em tabelas_gente.PAPEIS)
FATOS = ('entregou', 'atrasou', 'cumpriu', 'salvou', 'pagou', 'deu', 'ouviu', 'nao_entregou', 'recusou', 'calou', 'falhou', 'ferido', 'morto_junto', 'roubou',
         'viu_roubar', 'desconfia')                                 # o tipo de um fato da memória (os pesos e as frases: tabelas_gente.FATOS, com estas chaves; B1 pode acrescentar)
CANAIS = ('viu', 'ouviu', 'boato')                                  # como o fato chegou a quem lembra
MEMORIA_MAX = 12                                                    # quantos fatos cabem na memória de alguém: o 13º faz esquecer o mais leve de hoje (o mais velho, no empate)
PESO_MAX = 10                                                       # o peso de um fato (e o laço, e a opinião) vai de −isto a isto
ESFRIA = ((3, 28), (7, 56))                                         # o fato esfria: de peso até 3, perde 1 a cada 28 dias; até 7, a cada 56; de 8 para cima, nunca (a conta sai na hora de ler)
LACOS_MAX = 6                                                       # os laços de uma pessoa
QUERERES = ('nada', 'encomendar', 'melhorar', 'consertar', 'missao', 'viajar', 'laco', 'falar', 'cobrar', 'agradecer', 'furtar')      # o querer da semana (B1 pode acrescentar em tabelas_gente.QUERERES)
FAMA_EIXOS = ('oficio', 'feito', 'crime')                           # os eixos da fama, por lugar
FAMA_MAX = 100
FAMA_ESFRIA = 28                                                    # a fama esfria 1 ponto a cada tantos dias (a conta sai na hora de ler)
CAIXA_MAX = 7                                                       # os pedidos abertos na caixa de uma pessoa
CAIXA_FECHA = ('feito', 'vencido', 'forcado')                       # como um pedido sai da caixa
MOTIVOS = ('item', 'lugar', 'pessoa', 'missao', 'memoria', 'rota', 'noticia')     # o que o motivo de um pedido da caixa aponta (tem de existir)
MISSOES = ('levar', 'escoltar', 'caçar', 'limpar', 'buscar', 'encomenda')       # o tipo da missão
MISSAO_ESTADOS = ('aberta', 'pega', 'cumprida', 'falhada', 'vencida', 'largada')   # cumprida, falhada, vencida e largada são fechadas
MISSAO_FECHA = ('cumprida', 'falhada', 'vencida', 'largada')
MISSAO_MUDA = ('quem', 'estado', 'prazo', 'caucao', 'paga', 'alvo', 'item', 'feito', 'nota')      # o que muda numa missão depois de aberta, fora do Mestre (quem a pediu, onde, o tipo e o grau, só o Mestre)
GRAUS = ('F', 'E', 'D', 'C', 'B', 'A', 'S')                         # o grau do perigo (o bicho, a rota, a masmorra, a missão) e o teto de quem o enfrenta sem medo
NOTICIA_BOATO = 4                                                   # depois de tantos saltos a notícia vira boato (o nome some, o peso cai)

# ---------- a conta rápida provisória de quem não é o personagem (etapa 3; a etapa 5 troca esta tabela pela calibrada contra o luta.py: rapida.py) ----------
# pelo teto de quem vai (o grau que ele enfrenta sem medo) MENOS o grau do perigo (de −2 para baixo, a linha −2; de 1 para cima, a linha 1). Chute provisório, juntando os
# dois projetos: a missão é a do projeto B (cumpre 90%, 65%, 25%; morre em 15% das falhas acima do teto); o encontro na estrada segue as lutas medidas pelo projeto A
# (o Maro sozinho morre em 85% contra os lobos e em 20% contra o javali; com companhia, de metade a um quarto disso)
RAPIDA = {1: dict(cumpre=0.90, morre_falha=0.0, vence=0.90, morre=0.03),
          0: dict(cumpre=0.65, morre_falha=0.0, vence=0.65, morre=0.15),
          -1: dict(cumpre=0.25, morre_falha=0.15, vence=0.30, morre=0.45),
          -2: dict(cumpre=0.05, morre_falha=0.15, vence=0.05, morre=0.80)}
RAPIDA_COMPANHIA = 0.5                                              # com companhia (um ou mais que vão junto), a chance de morrer no encontro vezes isto
RAPIDA_DIAS = (2, 5)                                                # a missão de quem não é o personagem leva de tantos a tantos dias
RAPIDA_GASTA = 3                                                    # e as peças dele voltam gastas em tantos pontos

# ---------- a MESA (o orçamento: o teto de cada seção, em KB de 1.000 letras do arquivo; o turno.py avisa a que passa) ----------
MESA_TETO = dict(voce=1.0, aqui=0.8, rotas=0.6, viagem=0.7, gente=1.0, caixa=0.8, quadro=0.7, mercado=0.8, oficios=0.8, perguntas=0.5, mestre=1.0)
MESA_TOTAL = 8.0                                                    # a MESA inteira, no povoado e na estrada
MESA_SECOES = (('Você', 'voce'), ('Aqui', 'aqui'), ('Daqui se vai', 'rotas'), ('A viagem', 'viagem'), ('Quem está aqui', 'gente'), ('A caixa', 'caixa'),
               ('O quadro', 'quadro'), ('O que se diz', 'quadro'), ('Dois fatos', 'quadro'), ('O que se conta', 'quadro'), ('O mercado', 'mercado'),
               ('A oficina', 'oficios'), ('A caça', 'oficios'), ('Os bichos', 'oficios'), ('A magia', 'oficios'), ('A botica', 'oficios'),
               ('Perguntas', 'perguntas'), ('SÓ O MESTRE', 'mestre'))      # o título da seção (o começo dele) e a parte do orçamento em que ela conta
MESA_ORDEM = ['regiao', 'viagem', 'gente', 'caixa', 'missoes', 'noticias']       # as seções dos módulos da etapa 3 vêm antes das de hoje, nesta ordem (as de hoje seguem a ordem de MODULOS)
MESA_NA_ESTRADA = ('viagem', 'gente', 'caixa', 'missoes', 'noticias')            # com a viagem aberta, só estes módulos põem seção na MESA (saem o "Aqui", o mercado e a oficina)
MESA_SO_CENA = ('talento', 'magia_mundo', 'manha')                  # os módulos cujo SÓ O MESTRE fala de pessoas: só de quem está em cena (estado.na_cena); o resto, `talento.py mestre`
CAIXA_PERGUNTA = 6                                                  # o pedido da caixa que vence em até tantos blocos (um dia) vira pergunta do turno sozinho, e o fecha recusa sem ela
