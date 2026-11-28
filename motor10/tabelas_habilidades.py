"""tabelas_habilidades.py — MOTOR 10, A PARTE 2, FASE 2: AS HABILIDADES E O TESTE DE FALA (o contrato: projeto/etapa_efeitos/DESENHO.md, seção 6; o capítulo 29 e o 30).

Nenhum número de habilidade mora fora desta página. Uma HABILIDADE é um jeito de fazer, com nome, que muda um número ou uma regra quando a pessoa age (6.1):
  campo (batalhar · curar · convencer · trabalhar · copiar · mover · lançar) · tipo (ativa, passiva, reação, postura, acesa, declarada, de cargas) · ritmo (de mão, de luta,
  de dia, de cena) · custo · caminho (um dos 17, que segura o grau: as de arma usam a maior mão de arma da família dela) · teto (a força no Grão-Mestre) · origem (até que grau sobe).
O GRAU (Iniciante, Aprendiz, Adepto, Perito, Mestre, Grão-Mestre: I·Ap·Ad·P·M·GM) sobe pelo uso, para sempre (6.2), contado em MARCAS de cena, com sete freios; e a PILHA
cresce dentro da cena (6.3). O grau é o teto da pilha. A força que cada grau deixa é a régua de 3.1: I até o fraco (5 pontos), Ap e Ad até o normal (10), P e M até o forte (20),
GM até o teto dela. "+6,2" quer dizer que quem tem a habilidade vence 56,2% do duelo de iguais (nível 50, mão de Mestre, tudo Raro, começando perto).
O TESTE DE FALA (6.6) só rola no pedido que o jogador declara (`fala.py pede`), com o degrau e a chance mostrados antes; a conversa comum segue pela opinião.
"""
import tabelas_efeitos as TE

GRAUS = ('Iniciante', 'Aprendiz', 'Adepto', 'Perito', 'Mestre', 'Grão-Mestre')
CURTO = ('I', 'Ap', 'Ad', 'P', 'M', 'GM')
GM = 5
MARCAS = (0, 10, 30, 80, 200, 500)          # as marcas que cada grau pede (a escada do Ferir, em marcas de cena), vezes o talento do caminho
DESCONTO = (0, 0, 1, 1, 2, 2)               # o desconto da marca pelo próprio grau (o Mestre aprende menos de cada cena)
MAO_DO_GRAU = (0, 0, 0, 2, 4, 6)            # a mão no caminho que segura o grau: Perito pede Iniciante, Mestre Treinado, Grão-Mestre Mestre
FEITO_DO_GRAU = {4: 'vencer com ela uma cena de dureza 5', 5: 'um segundo feito, diante de alguém com nome, que vira notícia'}
FEITO_DUREZA = 5
FORCA_DO_GRAU = ('fraco', 'normal', 'normal', 'forte', 'forte', None)     # a força que o grau deixa (None: o teto da habilidade)
MARCA_MAX = 6               # uma marca por cena, de 0 a 6: dureza + 1 (usada 3 vezes ou mais, ou a de luta ou de dia venceu a cena) − o desconto do grau
USOS_MAIS = 3               # usada tantas vezes na cena: +1 na marca
DUREZA_1_ATE = 2            # a dureza 1 dá marca até o Adepto; do Adepto em diante, não (quem só bate em fraco para no Adepto)
DUREZA = (0.10, 0.30, 0.55, 0.80)           # a chance de dar errado: menos de 10% dureza 1 · 10 a 29% 2 · 30 a 54% 3 · 55 a 79% 4 · 80% ou mais 5
DUREZA_TRATAR = dict(leve=2, grave=3, caido=4)  # sem chance a medir, a coisa diz: no tratamento, a ferida leve 2, a grave 3, quem caiu 4
DUREZA_OBRA_SEM_RISCO = 1   # o conserto e o ajuste não falham: dureza 1 (dão marca até o Adepto)
VAGAS = 6                   # cada pessoa guarda até 6 habilidades (as da classe não ocupam vaga); a sétima pede esquecer uma
TETO_TALENTO = {-2: 2, -1: 4}               # o talento tranca: o Negado para no Adepto, o Lerdo no Mestre (os outros, no Grão-Mestre)
UM_GRAU_POR_DIA = True
GRAU_MAIS = 1               # cada grau acima do Iniciante dá +1 em todo teste que a própria habilidade rola (quando a tabela dela não diz outro número)


def dureza(chance_errar):
    """a dureza (1 a 5) pela chance de dar errado, que o script já sabe antes do dado"""
    return 1 + sum(1 for x in DUREZA if chance_errar >= x)


def forca_do_grau(k, g):
    """a força que o grau g deixa nesta habilidade (nunca acima do teto dela)"""
    f = FORCA_DO_GRAU[g] or HABILIDADES[k]['teto']; t = HABILIDADES[k]['teto']
    return f if TE.FORCAS.index(f) <= TE.FORCAS.index(t) else t


def pontos_do_grau(k, g): return TE.FORCA_PONTOS[forca_do_grau(k, g)]


# ---------- AS ORIGENS (6.5): de onde veio diz até que grau sobe ----------
ORIGENS = ('classe', 'mestre', 'licao', 'estalo', 'livro', 'legado')
ORIGEM_DIZ = dict(classe='da classe', mestre='de um mestre', licao='da lição (a cena)', estalo='do estalo', livro='do livro', legado='do legado de um mestre morto', copia='da cópia (colher o jeito)')
ORIGEM_TETO = dict(classe=5, mestre=4, licao=3, estalo=3, livro=4, legado=5, copia=4)      # a classe: Comum Perito, Incomum Mestre, Rara para cima Grão-Mestre (fase 4: até lá, a do Mestre)
ORIGEM_CURTA = dict(C='classe', Me='mestre', Li='licao', E='estalo', Lv='livro', Lg='legado')
APELAO_SO_DE = ('legado', 'classe')         # o apelão de habilidade só nasce de legado ou de classe Lendária, sem exceção
ENSINA_DESDE = 3            # o mestre que ensina tem a habilidade no Perito ou mais
ENSINA_OPINIAO = dict(fraco=3, normal=3, forte=6)    # a estima que o mestre pede (a opinião dele sobre o aprendiz); ninguém vivo ensina um apelão
ENSINA_BLOCOS = dict(fraco=10, normal=20, forte=40)  # os blocos de treino juntos
LIVRO_BLOCOS = dict(fraco=10, normal=10, forte=30)   # o estudo do escrito (teto normal: 10 blocos; forte: 30)
LEGADO_LUTAS = 5            # o legado: 5 lutas de verdade com a peça do mestre morto, ou 30 blocos no caderno dele
LEGADO_BLOCOS = 30
ESTALO = {3: 0.08, 2: 0.04}  # o estalo: em luta de verdade com a arma, rolagem oculta: 8% com dureza 3 ou mais, 4% com 2 (nada com 1); no máximo um por semana
ESTALO_SEMANA = 7
ESTALO_LISTA = {             # a lista curta do estalo, por família de arma (6.5)
    'martelo': ('tranco', 'golpe_quebra'), 'maça': ('tranco', 'golpe_quebra'), 'malho': ('tranco', 'golpe_quebra', 'varrida'),
    'espada': ('riposta', 'corte_fundo'), 'montante': ('riposta', 'corte_fundo', 'varrida'),
    'adaga': ('corte_fundo',), 'machado': ('corte_fundo', 'varrida'),
    'lança': ('rasteira', 'manter'), 'alabarda': ('rasteira', 'manter'),
    'arco': ('mira_firme',), 'besta': ('mira_firme',),
}
COPIA = dict(base=0.40, acima=0.10, abaixo=0.15, colher=0.05, min=0.05, max=0.90, tentativas=3, teto=4, ver=3)      # 6.5: colher o jeito
COPIA_PEDE = dict(fraco=2, normal=4, forte=6)        # a mão que a técnica pede para copiar: fraco Iniciante, normal Treinado, forte Mestre (apelão e assinatura não se copiam)
ECO_MAX = 3                 # o Eco de Golpe copia no máximo 3 técnicas assim

# ---------- AS PILHAS DA CENA (6.3): a pilha cresce dentro da cena; o grau é o teto dela ----------
RODA_BATIDA = 0.05          # cada batida: +5% de dano (TÉCNICA)
RODA_ACERTO_A_CADA = 2      # a cada 2 batidas, +1 no acerto (P3)
RODA_FECHO_DESDE = 3        # o fecho pede 3 batidas ou mais; sem a ordem, sai sozinho aos 4 (ou no teto, se o teto é menor)
RODA_FECHO_SOZINHO = 4
RODA_FECHO_FUNDO = 2        # o fecho fundo: os dados da arma rolam 1 vez a mais a cada 2 batidas (o maior entre isso, o crítico e o Golpe do Fim: P2)
RODA_FECHO_TRANCO = 3       # o fecho tranco: carga de cabeça 3 por batida
RODA_ABRIR = -2             # o ABRIR (Perito): a primeira batida que acerta em cada turno tira 2 da Defesa do alvo até o fim do turno (não soma com o aberto: P3)
RODA_ENTRA = (0, 0, 0, 0, 1, 2)             # o Mestre entra quente (a primeira batida da luta já conta 1); o Grão-Mestre entra com 2
SANHA_PONTO = 0.05          # cada ponto da Sanha: +5% de dano (TÉCNICA); a cada 2, +1 no acerto
SANHA_ACERTO_A_CADA = 2
SANHA_DEFESA = -1           # o preço: −1 na Defesa enquanto dura
SANHA_CORAGEM = 4           # +4 na coragem (P3)
SANHA_CABECA = 3            # com 3 pontos, a ferida leve na cabeça não atordoa
SANHA_CANSA_A_CADA = 2      # no fim, +1 de cansaço a cada 2 pontos (o maior que ela teve)
ESTANCA_CURA = (0.04, 0.03)  # a Mão que Estanca: a atadura cura 4% do PV máximo, +3% por ponto da pilha (no teto do dia, P7)
ESTANCA_LEVANTA = 0.10       # a Mão que Estanca do Grão-Mestre: o caído colado levanta com 10% do PV (no teto do dia), uma vez por luta; do Mestre, o caído colado fica firme
ESQUENTA_DIAS = 0.5          # a Mão que Esquenta: +½ dia de repouso no próximo, por ponto da pilha (os pacientes tratados no dia)
ESQUENTA_CANSA_A_CADA = 2
FIO_MAIS = 2                 # o Fio da Conversa: +2 no próximo pedido por fio; com 3 fios, o pedido sobe um degrau sem subir a CD
FIO_DEGRAU = 3
MALHO_PRUMO = 2              # o Malho Quente: a obra que fecha quente ganha prumo igual a metade do calor
MALHO_CANSA_A_CADA = 2
CORRENTE_CONJ = 1            # A Corrente: cada feitiço seguido dá +1 na Conjuração (no teto de +8) e +5% de dano de feitiço (TÉCNICA)
CORRENTE_DANO = 0.05
TRUNFO_CONDICOES = ('carga', 'pernas', 'abalado', 'metade')      # a condição do trunfo: carga>=N (a barra de cabeça do alvo), pernas>=N, abalado, metade (abaixo de metade do PV)
TRUNFO_USOS = ('dano', 'rasteira', 'corte', 'tranco', 'ameaca', 'nao')
TRUNFO_DESDE = dict(dano=0, rasteira=0, corte=2, tranco=3, ameaca=4, nao=0)    # os efeitos abrem com o grau: I a rasteira; Ad o corte; P o tranco; M a ameaça
TRUNFO_CORTE = (0.20, 3)     # o trunfo de corte: filete de 1/5 por 3
TRUNFO_AMEACA = 18           # a ameaça: coragem contra 18 + o dado
BRADO_CASAS = 3
MIRA_FRESTA = -5            # a Mira Firme do Perito: mirar a fresta, no tiro, pede −5 (e não os −8 de tabelas.MIRA_ACERTO; o contrato dizia −4: DESENHO 12.4)
FERRO_CANSA = 1             # o Ferro em Brasa dói: +1 de cansaço em quem o leva
FERRO_LEVE_DIAS = 1         # fora da luta (1 bloco), a ferida leve sara com 1 dia de repouso; no Grão-Mestre, a grave com 3
FERRO_GRAVE_DIAS = 3

# ---------- O CATÁLOGO (52) ----------
# chave: nome (à mesa), campo, tipo, ritmo, custo, caminho, teto, origens (as letras do contrato), armas (as famílias em que vale; None: todas), ordem (a palavra do `fazer`),
# g (os números por grau, I·Ap·Ad·P·M·GM), medido (os pontos de vitória do contrato por grau, ou None), mede ('m' medido, 'c' conta, 'd' desenho; 'remede': a HB1 remede pelas regras
# de P2 e P3), cena (onde o banco a mede), licao (o gatilho da lição), faz (a frase).
PESO = ('maça', 'martelo', 'malho')
FIO = ('adaga', 'espada', 'machado', 'montante')
HASTE = ('lança', 'alabarda')
TIRO = ('arco', 'besta')
IMPACTO = ('maça', 'martelo', 'malho', 'punho')
APARA = ('espada', 'montante')              # quem apara: a espada, o montante e o escudo (a Riposta)

HABILIDADES = {
    # ---- BATALHAR ----
    'roda': dict(nome='a Roda do Malho', campo='batalhar', tipo='acesa', ritmo='mao', custo='o fôlego do martelo', caminho='peso', teto='apelão', origens=('Lg', 'C'), armas=PESO, ordem='roda',
                 g=dict(batidas=(2, 3, 3, 4, 5, 6)), medido=(2.1, 5.0, 9.6, 16.9, 20.4, 24.7), mede='remede', cena='duelo de martelo',
                 faz='a dança do martelo no compasso da bigorna: cada golpe da Roda, acerte ou não, é uma batida (+5% de dano; a cada 2, +1 no acerto); do Adepto, o FECHO (fundo ou tranco); do Perito, o ABRIR; o Mestre entra quente; o Grão-Mestre entra com 2 e o golpe que o fere não tira batida'),
    'sanha': dict(nome='a Sanha', campo='batalhar', tipo='acesa', ritmo='luta', custo='−1 na Defesa; não recua, não guarda, não lança; no fim, +1 de cansaço a cada 2 pontos', caminho='arma', teto='forte',
                  origens=('C', 'Me'), armas=None, ordem='sanha', g=dict(pontos=(2, 3, 4, 5, 6, 8), usos=(1, 1, 1, 1, 2, 2)), medido=(4.6, 6.0, 9.5, 9.7, 13.5, 16.8), mede='m', cena='duelo de espada',
                  faz='a fúria: acende sem ação no primeiro golpe que tira PV de alguém ao alcance; +1 ponto no começo de cada turno e por golpe que tira PV, dado ou levado (+5% de dano; a cada 2, +1 no acerto); +4 na coragem; com 3 pontos a ferida leve na cabeça não atordoa; a rodada sem sangue perde metade; sem fôlego, apaga'),
    'trunfos': dict(nome='os Trunfos', campo='batalhar', tipo='cargas', ritmo='luta', custo='os dados por luta (voltam com um bloco de descanso)', caminho='arma', teto='forte', origens=('C', 'Me'), armas=None, ordem='trunfo',
                    g=dict(dados=((1, 4), (1, 6), (2, 4), (2, 6), (2, 8), (3, 6))), medido=(4.5, 8.5, 9.4, 13.7, 17.5, 18.2), mede='m', cena='duelo de espada',
                    faz='cada trunfo gasta um dado: um por turno, no primeiro golpe que acerta e cumpre a condição, no dano (o dado soma uma vez, sem dobrar no crítico) ou no efeito: rasteira (I), corte (Ad), tranco (P), ameaça (M)'),
    'tranco': dict(nome='o Tranco de Luta', campo='batalhar', tipo='declarada', ritmo='luta', custo='os usos por luta', caminho='peso', teto='forte', origens=('E', 'Me'), armas=IMPACTO, ordem='tranco',
                   g=dict(usos=(1, 1, 1, 2, 2, 3), acerto=(-2, -1, 0, 0, 0, 0)), medido=(2.5, 3.7, 4.0, 8.7, 10.0, 12.3), mede='remede', cena='duelo de martelo',
                   faz='o golpe declarado que acerta tira o turno seguinte do alvo e lhe dá o calejo de cabeça (nunca na cabeça firme; ninguém perde mais de 1 turno em cada 3); do Mestre, esse calejo não sobe a resistência'),
    'corte_fundo': dict(nome='o Corte Fundo', campo='batalhar', tipo='declarada', ritmo='mao', custo='−2 no acerto do golpe declarado', caminho='fio', teto='normal', origens=('E', 'C'), armas=FIO, ordem='corte',
                        g=dict(filete=((0.20, 3), (0.25, 3), (1 / 3, 3), (1 / 3, 4), (0.50, 3), (0.50, 4)), acerto=(-2,) * 6), medido=(1.1, 1.4, 4.9, 4.1, 7.9, 7.3), mede='m', cena='duelo de espada',
                        faz='o primeiro golpe do turno (−2 no acerto) abre um filete de sangue'),
    'rasteira': dict(nome='a Rasteira', campo='batalhar', tipo='declarada', ritmo='mao', custo='−2 no acerto do golpe declarado', caminho='haste', teto='normal', origens=('E', 'Me'), armas=HASTE + PESO, ordem='rasteira',
                     g=dict(carga=(3, 4, 5, 6, 7, 8), acerto=(-2,) * 6), medido=None, mede='d', cena='duelo de lança',
                     faz='o primeiro golpe do turno (−2 no acerto) soma carga de pernas: cheia, ao chão'),
    'riposta': dict(nome='a Riposta', campo='batalhar', tipo='reacao', ritmo='mao', custo='a reação', caminho='fio', teto='normal', origens=('E', 'Me', 'C'), armas=APARA, ordem=None,
                    g=dict(margem=(2, 3, 4, 5, 6, 8), acerto=(-2, -2, -1, -1, 0, 0)), medido=(3.5, 6.0, 6.7, 7.6, 9.5, 9.5), mede='m', cena='duelo de espada',
                    faz='o golpe que erra você por pouco (e que você apara) devolve um golpe livre'),
    'golpe_quebra': dict(nome='o Golpe de Quebra', campo='batalhar', tipo='passiva', ritmo='mao', custo='+1 de fôlego no golpe em que vale', caminho='peso', teto='normal', origens=('E', 'C'), armas=IMPACTO, ordem=None,
                         g=dict(prot=(0.8, 0.75, 0.67, 0.6, 0.57, 0.55)), medido=(-0.4, 0.1, 2.5, 5.3, 6.9, 9.5), mede='m', cena='contra a armadura uma acima',      # (DESENHO 12.4: o Mestre e o GM, ×0,57 e ×0,55; o contrato, ×0,55 e ×0,5, mediu +9,6 e +12,7)
                         faz='contra armadura de categoria maior que a arma, a proteção conta menos (o mesmo efeito da Perfura e da mira na fresta: vale o maior)'),
    'bigorna': dict(nome='a Guarda de Bigorna', campo='batalhar', tipo='postura', ritmo='mao', custo='o acerto a menos', caminho='arma', teto='forte', origens=('C', 'Me'), armas=None, ordem='bigorna',
                    g=dict(defesa=(1, 2, 2, 3, 3, 4), acerto=(-1, -1, -1, -1, 0, 0)), medido=(-0.4, 2.9, 2.9, 6.7, 8.6, 11.9), mede='m', cena='duelo de espada',
                    faz='a postura `bigorna`: Defesa a mais, acerto a menos; do Adepto, firme (a perna ferida não derruba)'),
    'brado': dict(nome='o Brado de Guerra', campo='batalhar', tipo='ativa', ritmo='luta', custo='1 ação, uma vez por luta', caminho='arma', teto='forte', origens=('C', 'Li'), armas=None, ordem='brado',
                  g=dict(cd=(20, 21, 22, 24, 26, 29)), medido=(2.5, 2.0, 3.8, 5.2, 8.8, 13.5), mede='m', cena='duelo de espada', licao='vencer com metade dos seus no chão',
                  faz='quem está a 3 casas testa a coragem (a escada do medo; testa junto das outras fontes novas, no fim da rodada)'),
    'teima': dict(nome='a Teima', campo='batalhar', tipo='passiva', ritmo='mao', custo='—', caminho='arma', teto='normal', origens=('Li', 'C'), armas=None, ordem=None,
                  g=dict(acerto=(1, 1, 2, 2, 3, 4)), medido=(2.1, 1.5, 3.9, 3.6, 4.8, 5.8), mede='m', cena='duelo de espada', licao='vencer abaixo de 1/4 do PV',
                  faz='abaixo de metade do PV, acerto a mais'),
    'varrida': dict(nome='a Varrida', campo='batalhar', tipo='ativa', ritmo='luta', custo='os usos por luta', caminho='arma', teto='normal', origens=('E', 'C'), armas=('montante', 'machado', 'malho', 'alabarda'), ordem='varrida',
                    g=dict(usos=(1, 1, 2, 2, 3, 3), inteiro=(False, False, False, False, False, True)), medido=None, mede='c', cena='um contra três',
                    faz='o golpe que acerta pega também um outro inimigo colado, com metade do dano (no Grão-Mestre, o dano inteiro)'),
    'manter': dict(nome='o Manter à Distância', campo='batalhar', tipo='reacao', ritmo='mao', custo='a reação', caminho='haste', teto='normal', origens=('E', 'Me'), armas=HASTE, ordem=None,
                   g=dict(acerto=(1, 1, 2, 2, 3, 4), segura=(False, False, False, True, True, True)), medido=None, mede='d', cena='lança contra espada, de longe',
                   faz='o golpe livre em quem entra no seu alcance, com acerto a mais; do Perito, se fere, ele não entra'),
    'mira_firme': dict(nome='a Mira Firme', campo='batalhar', tipo='ativa', ritmo='mao', custo='1 ação mirando', caminho='tiro', teto='normal', origens=('C', 'Me', 'E'), armas=TIRO, ordem='mira',      # o E: a lista curta do estalo de 6.5 (arco e besta; DESENHO 12.4)
                       g=dict(acerto=(2, 3, 3, 4, 4, 5), fresta=(False, False, False, True, True, True)), medido=None, mede='d', cena='duelo de arqueiros',
                       faz='1 ação mirando: o próximo tiro tem acerto a mais; do Perito, mirar a fresta pede −5, não −8'),
    'golpe_voto': dict(nome='o Golpe de Voto', campo='batalhar', tipo='ativa', ritmo='mao', custo='2 de Mana (fé), um por rodada', caminho='fé', teto='normal', origens=('C',), armas=None, ordem=None,
                       g=dict(dano=(0.10, 0.15, 0.20, 0.20, 0.25, 0.30), mana=(2,) * 6, dobro=(False,) * 3 + (True,) * 3), medido=None, mede='c', cena='o clérigo de maça contra o igual (e contra o maldito)',
                       faz='depois do acerto, dano a mais (TÉCNICA); o dobro contra o maldito, do Perito em diante (a força forte abre no Perito: DESENHO 12.4)'),
    'rito_veia': dict(nome='o Rito de Veia', campo='batalhar', tipo='acesa', ritmo='luta', custo='1 ação e 1d6 de PV que nada reduz (no Grão-Mestre, 1d4); a cura de magia na cena vale metade', caminho='pacto', teto='forte',
                      origens=('C',), armas=None, ordem='rito', g=dict(dado=(4, 4, 6, 6, 8, 8), turnos=(1, 2, 2, 3, 3, 3), custo=(6, 6, 6, 6, 6, 4)), medido=(1.5, 7.1, 11.5, 16.7, 20.2, 20.1), mede='m', cena='duelo de espada',
                      faz='por N turnos (o de abrir é o primeiro), +1 dado em cada golpe e feitiço (o dado somado: não dobra no crítico)'),      # (DESENHO 12.4: o turno de abrir conta; contar os N depois dele mediu +6,7 · +11,7 · +16,4 · +18,3 · +23,7 · +24,2, fora da faixa em cinco graus)
    # ---- CURAR ----
    'estanca': dict(nome='a Mão que Estanca', campo='curar', tipo='ativa', ritmo='mao', custo='1 ação, em si ou num aliado colado', caminho='cura', teto='forte', origens=('C', 'Me'), armas=None, ordem='atar',
                    g=dict(filetes=(1, 1, 2, 2, 3, 99), pilha=(1, 1, 2, 2, 3, 4), firma=(False, False, False, False, True, True), levanta=(False,) * 5 + (True,)), medido=None, mede='d', cena='três contra três',
                    faz='atar corta filetes e cura 4% do PV máximo, +3% por ponto da pilha (cada atadura seguida na luta; no teto do dia); do Mestre, firma o caído; no Grão-Mestre, o caído levanta com 10% do PV, uma vez por luta'),
    'esquenta': dict(nome='a Mão que Esquenta', campo='curar', tipo='passiva', ritmo='cena', custo='+1 de cansaço a cada 2 tratados', caminho='cura', teto='normal', origens=('C', 'Me'), armas=None, ordem=None,
                     g=dict(pilha=(1, 1, 2, 2, 3, 4)), medido=None, mede='c', cena='o tratar',
                     faz='cada paciente tratado no dia dá +½ dia de repouso no próximo (até +½·+½·+1·+1·+1½·+2); um bloco sem tratar quebra a pilha'),
    'trato': dict(nome='o Trato de Campo', campo='curar', tipo='passiva', ritmo='mao', custo='—', caminho='cura', teto='normal', origens=('C', 'Lv'), armas=None, ordem=None,
                  g=dict(dias=(0.5, 0.5, 1, 1, 1.5, 2), dois=(False,) * 3 + (True,) * 3, grave_treinado=(False,) * 4 + (True, True)), medido=None, mede='c', cena='o tratar',
                  faz='o tratar soma repouso; do Perito, trata 2 por bloco (`tratar PACIENTE e=OUTRO`); do Mestre, a ferida grave pede só a mão de Treinado'),
    'ferro_brasa': dict(nome='o Ferro em Brasa', campo='curar', tipo='ativa', ritmo='mao', custo='dói: +1 de cansaço; na luta, perde 1 ação (do Mestre, não)', caminho='forja', teto='normal', origens=('Li', 'Me'), armas=None, ordem='ferro',
                        g=dict(luta=(False, False, True, True, True, True), sem_acao=(False,) * 4 + (True, True), grave=(False,) * 5 + (True,)), medido=None, mede='d', cena='três contra três', licao='estancar alguém com o ferro da forja',
                        faz='o ferro quente estanca todos os filetes (1 ação na luta, do Adepto; 1 bloco fora, `habilidade.py ferro PACIENTE`: a ferida leve sara com 1 dia de repouso; no Grão-Mestre, a grave com 3)'),
    'sopro_volta': dict(nome='o Sopro de Volta', campo='curar', tipo='ativa', ritmo='dia', custo='1 ação, colado; 2 de cansaço a quem ergue', caminho='cura', teto='forte', origens=('C',), armas=None, ordem='sopro',
                        g=dict(pv=(0.05, 0.05, 0.10, 0.10, 0.15, 0.20)), medido=None, mede='d', cena='três contra três',
                        faz='quem caiu nesta luta levanta com parte do PV (no teto do dia)'),
    'vigilia': dict(nome='a Vigília', campo='curar', tipo='reacao', ritmo='mao', custo='a reação', caminho='cura', teto='normal', origens=('Li', 'Me', 'C'), armas=None, ordem=None,
                    g=dict(qualquer=(False, False, True, True, True, True), casas=(1, 1, 1, 1, 1, 2)), medido=None, mede='d', cena='três contra três', licao='ficar de pé sobre um caído até o fim da luta',
                    faz='um aliado a 1 casa cai: você gasta a reação e o firma (I·Ap só se não golpeou na rodada; no GM, a 2 casas)'),
    'benzimento': dict(nome='o Benzimento', campo='curar', tipo='ativa', ritmo='dia', custo='—', caminho='fé', teto='normal', origens=('C',), armas=None, ordem=None,
                       g=dict(mais=(1, 1, 2, 2, 3, 4), pessoas=(1, 2, 3, 4, 6, 99)), medido=None, mede='d', cena='contra maldição',
                       faz='coragem e Firmeza contra maldição por um dia, em quem se benze (no GM, a casa inteira)'),
    # ---- CONVENCER ----
    'fio_conversa': dict(nome='o Fio da Conversa', campo='convencer', tipo='passiva', ritmo='cena', custo='no 3º fio, −1 na opinião de quem ouve, ganhe ou perca', caminho='comércio', teto='forte', origens=('C', 'Me'), armas=None, ordem=None,
                         g=dict(fios=(1, 1, 2, 2, 3, 3)), medido=None, mede='c', cena='a fala',
                         faz='cada pedido ganho no mesmo lugar no dia dá +2 no próximo; com 3 fios, o pedido sobe um degrau sem subir a CD; falhou, o fio rompe e quem ouviu lembra (−1)'),
    'lingua': dict(nome='a Língua de Feira', campo='convencer', tipo='ativa', ritmo='dia', custo='uma vez por loja por dia', caminho='comércio', teto='normal', origens=('C', 'Me'), armas=None, ordem=None,
                   g=dict(mais=(2, 2, 3, 3, 4, 5), prateleira=(False, False, False, True, True, True)), medido=None, mede='c', cena='o regateio',
                   faz='soma no teste de preço (o regateio); do Perito, regateia também a compra da prateleira'),
    'palavra_firme': dict(nome='a Palavra Firme', campo='convencer', tipo='passiva', ritmo='mao', custo='—', caminho='comércio', teto='normal', origens=('C', 'Me'), armas=None, ordem=None,
                          g=dict(duro=(3, 2, 2, 1, 1, 0), nao_ofende=(False,) * 4 + (True, True)), medido=None, mede='c', cena='a fala',
                          faz='o jeito duro fica mais barato (a CD do duro sobe menos); do Mestre, o duro que falha por menos de 5 não ofende'),
    'voz_praca': dict(nome='a Voz da Praça', campo='convencer', tipo='ativa', ritmo='dia', custo='—', caminho='comércio', teto='forte', origens=('C', 'Li'), armas=None, ordem=None,
                      g=dict(ouvem=(3, 5, 8, 12, 20, 999)), medido=None, mede='d', cena='a fala', licao='vencer um leilão falando',
                      faz='um teste vale para todos os que ouvem (o pregão, o leilão, a tropa), e a notícia anda uma estrada a mais'),
    'avaliador': dict(nome='o Olho de Avaliador', campo='convencer', tipo='passiva', ritmo='mao', custo='—', caminho='comércio', teto='fraco', origens=('C', 'Lv'), armas=None, ordem=None,
                      g=dict(ve=('o degrau certo', 'o degrau certo', 'a opinião exata', 'a CD', 'o querer da semana', 'o fato de maior peso que ele guarda')), medido=None, mede='d', cena='a fala',
                      faz='antes do teste, a mesa mostra o que ele sabe do outro'),
    'ameaca_surda': dict(nome='a Ameaça Surda', campo='convencer', tipo='ativa', ritmo='mao', custo='o jeito duro com Força', caminho='manha', teto='normal', origens=('Li', 'Me', 'C'), armas=None, ordem=None,
                         g=dict(mais=(0, 1, 1, 2, 2, 3)), medido=None, mede='c', cena='a fala', licao='ganhar uma briga sem tirar a arma',
                         faz='soma na ameaça (o duro com Força); passou, ele não age contra você no dia'),
    'penhor': dict(nome='o Penhor', campo='convencer', tipo='ativa', ritmo='cena', custo='a promessa empenhada', caminho='fé', teto='normal', origens=('C',), armas=None, ordem=None,
                   g=dict(cumprida=(2, 2, 3, 3, 4, 5), quebrada=(-4, -4, -5, -5, -6, -6)), medido=None, mede='d', cena='a memória',
                   faz='a promessa empenhada pesa na memória: cumprida, ele lembra mais; quebrada, menos'),
    # ---- TRABALHAR (nunca no total: a chance da categoria não muda) ----
    'malho_quente': dict(nome='o Malho Quente', campo='trabalhar', tipo='passiva', ritmo='cena', custo='+1 de cansaço a cada 2 de calor', caminho='forja', teto='forte', origens=('C', 'Li'), armas=None, ordem=None,
                         g=dict(calor=(2, 2, 3, 4, 5, 6)), medido=None, mede='c', cena='a régua de feitio', licao='fechar no dia uma obra de 9 blocos esquentada',
                         faz='cada bloco seguido na mesma obra, no dia, esquenta 1; a obra que fecha quente ganha prumo igual a metade do calor (outro ato no meio, ou a noite, esfria)'),
    'paciencia': dict(nome='a Paciência', campo='trabalhar', tipo='ativa', ritmo='dia', custo='um dia sem pressa', caminho='forja', teto='normal', origens=('C', 'Me'), armas=None, ordem=None,
                      g=dict(prumo=(0, 0, 1, 1, 1, 2), passiva=(False,) * 4 + (True, True)), medido=None, mede='c', cena='a régua de feitio',
                      faz='um dia sem pressa: −1 de cansaço por bloco pesado; do Adepto, prumo nas obras do dia; do Mestre, vale sempre'),
    'tempera_certa': dict(nome='a Têmpera Certa', campo='trabalhar', tipo='ativa', ritmo='dia', custo='uma obra por dia', caminho='forja', teto='forte', origens=('C', 'Me'), armas=None, ordem=None,
                          g=dict(cheios=(1, 1, 1, 1, 2, 3), so_teto=(True, True, True, False, False, False)), medido=None, mede='c', cena='a régua de feitio',
                          faz='uma obra do dia nasce com efeitos de número cheios (I, Ap e Ad só no teto: DESENHO 12.4); vale o maior com a têmpera da ferramenta'),
    'brio': dict(nome='o Brio de Oficina', campo='trabalhar', tipo='passiva', ritmo='mao', custo='—', caminho='forja', teto='forte', origens=('Li', 'C'), armas=None, ordem=None,
                 g=dict(prumo=(1, 1, 2, 2, 2, 3)), medido=None, mede='c', cena='a régua de feitio', licao='uma humilhação pública na forja',
                 faz='com um rival ou um mestre de forja com nome olhando, prumo a mais'),
    'reparo': dict(nome='a Mão de Reparo', campo='trabalhar', tipo='passiva', ritmo='mao', custo='—', caminho='forja', teto='fraco', origens=('C', 'Me'), armas=None, ordem=None,
                   g=dict(bloco=(6, 7, 8, 8, 9, 10)), medido=None, mede='d', cena='o conserto',
                   faz='o conserto devolve mais por bloco (vale o maior entre as fontes)'),
    'ajuste_fino': dict(nome='o Ajuste Fino', campo='trabalhar', tipo='passiva', ritmo='mao', custo='—', caminho='forja', teto='fraco', origens=('C', 'Me'), armas=None, ordem=None,
                        g=dict(blocos=(0, 1, 1, 2, 2, 3), teste=(1, 1, 2, 2, 3, 3)), medido=None, mede='d', cena='o ajuste',
                        faz='o ajuste sob medida pede menos blocos (no mínimo 1) e soma no teste'),
    'ler_peca': dict(nome='o Ler a Peça', campo='trabalhar', tipo='passiva', ritmo='mao', custo='—', caminho='forja', teto='normal', origens=('C',), armas=None, ordem=None,
                     g=dict(le=('a categoria', 'e a durabilidade', 'os efeitos', 'o cheio e o sinete', 'a maldição e o encanto', 'o poder de lenda')), medido=None, mede='d', cena='a janela',
                     faz='lê à vista, sem teste, o que a peça é'),
    'faro_trilha': dict(nome='o Faro de Trilha', campo='trabalhar', tipo='passiva', ritmo='mao', custo='—', caminho='caça', teto='normal', origens=('C',), armas=None, ordem=None,
                        g=dict(mais=(1, 1, 2, 2, 3, 4)), medido=None, mede='c', cena='a caça', faz='soma no rastro da caça'),
    'traco_fiel': dict(nome='o Traço Fiel', campo='trabalhar', tipo='passiva', ritmo='mao', custo='—', caminho='encanto', teto='normal', origens=('C',), armas=None, ordem=None,
                       g=dict(erra=(1, 1, 2, 2, 3, 4)), medido=None, mede='d', cena='a gravação', faz='na gravação, errar por pouco grava inteiro'),
    'medida_certa': dict(nome='a Medida Certa', campo='trabalhar', tipo='passiva', ritmo='mao', custo='—', caminho='alquimia', teto='normal', origens=('C',), armas=None, ordem=None,
                         g=dict(pocoes=(0, 0, 1, 1, 1, 2)), medido=None, mede='d', cena='a leva', faz='a leva de poção rende mais'),
    # ---- COPIAR ----
    'colher_jeito': dict(nome='o Colher o Jeito', campo='copiar', tipo='ativa', ritmo='cena', custo='um dia de treino por tentativa', caminho='arma', teto='forte', origens=('Lv', 'Me', 'C'), armas=None, ordem=None,
                         g=dict(chance=(0.05, 0.10, 0.15, 0.20, 0.25, 0.30)), medido=None, mede='d', cena='a cópia', faz='a cópia de uma técnica vista (+5% por grau na chance)'),
    'olho_luta': dict(nome='o Olho de Luta', campo='copiar', tipo='passiva', ritmo='mao', custo='—', caminho='arma', teto='normal', origens=('E', 'C'), armas=None, ordem=None,
                      g=dict(estalo=(0.01, 0.01, 0.02, 0.02, 0.03, 0.04)), medido=None, mede='d', cena='o estalo', faz='o estalo com chance a mais, e escolhe entre duas técnicas da família'),
    'risco_talho': dict(nome='o Risco do Talho', campo='copiar', tipo='ativa', ritmo='cena', custo='1 dia por categoria da peça', caminho='forja', teto='forte', origens=('C', 'Lv'), armas=None, ordem=None,
                        g=dict(mais=(0, 1, 2, 3, 4, 5)), medido=None, mede='d', cena='a cópia de peça',
                        faz='estuda uma peça Rara ou melhor: 2d20 + mão de forja + o grau contra 28 + 6 por categoria; passou, o efeito de regra dela entra no livro de talhos (três tentativas por peça)'),
    'eco_golpe': dict(nome='o Eco de Golpe', campo='copiar', tipo='passiva', ritmo='mao', custo='—', caminho='arma', teto='normal', origens=('Li', 'C'), armas=None, ordem=None,
                      g=dict(chance=(0.05, 0.06, 0.07, 0.08, 0.10, 0.12)), medido=None, mede='d', cena='a cópia', licao='sobreviver a três técnicas que o derrubaram',
                      faz='a técnica que o feriu nesta luta: rolagem oculta para copiá-la; no máximo 3 copiadas assim'),
    # ---- MOVER ----
    'pe_lebre': dict(nome='o Pé de Lebre', campo='mover', tipo='passiva', ritmo='mao', custo='—', caminho='arma', teto='forte', origens=('Li', 'C'), armas=None, ordem=None,
                     g=dict(casas=(3, 3, 3, 3, 4, 4), todo=(False, True, True, True, True, True), livre=(0, 0, -4, -4, -4, -4), sai=(8, 8, 8, 6, 6, 4)), medido=None, mede='m', cena='a fuga', licao='fugir de uma luta de dureza 4 ou 5 e viver',
                     faz='no recuo, mais casas (I: só o primeiro recuo da luta); do Adepto, o golpe livre de quem fica pega −4; do Perito, sai da luta a 6 casas; no GM, a 4'),
    'picada': dict(nome='a Picada', campo='mover', tipo='passiva', ritmo='mao', custo='—', caminho='caça', teto='normal', origens=('C', 'Li'), armas=None, ordem=None,
                   g=dict(mata=((4, 3), (4, 3), (3, 2), (3, 2), (3, 2), (2, 1))), medido=None, mede='d', cena='o ermo', faz='abre trilha no mato com a ferramenta que fez'),
    'passo_manso': dict(nome='o Passo Manso', campo='mover', tipo='passiva', ritmo='mao', custo='—', caminho='manha', teto='normal', origens=('C',), armas=None, ordem=None,
                        g=dict(mais=(1, 1, 2, 2, 3, 4)), medido=None, mede='c', cena='a manha', faz='soma no andar escondido e no escutar; do Mestre, a emboscada que arma é surpresa na 1ª rodada'),
    'romper_linha': dict(nome='o Romper a Linha', campo='mover', tipo='ativa', ritmo='luta', custo='o golpe livre de quem segura', caminho='arma', teto='normal', origens=('E', 'Li'), armas=None, ordem=None,
                         g=dict(usos=(1, 1, 1, 2, 2, 2)), medido=None, mede='d', cena='o corredor', faz='atravessa a casa de um inimigo seguro só por um dos seus, levando o golpe livre dele'),
    'marcha_longa': dict(nome='a Marcha Longa', campo='mover', tipo='passiva', ritmo='mao', custo='—', caminho='coleta', teto='fraco', origens=('Li', 'Lv'), armas=None, ordem=None,
                         g=dict(cansaco=(1,) * 6), medido=None, mede='d', cena='a estrada', faz='a estrada pesa menos: −1 de cansaço por dia de estrada'),
    # ---- LANÇAR ----
    'corrente': dict(nome='a Corrente', campo='lançar', tipo='passiva', ritmo='cena', custo='golpear, andar ou ser atordoado zera', caminho='magia', teto='forte', origens=('C', 'Me', 'Lv'), armas=None, ordem=None,
                     g=dict(pilha=(2, 3, 3, 4, 5, 6)), medido=None, mede='d', cena='mago contra mago',
                     faz='cada feitiço seguido dá +1 na Conjuração (no teto de +8) e +5% de dano de feitiço (TÉCNICA)'),
    'mao_rito': dict(nome='a Mão no Rito', campo='lançar', tipo='passiva', ritmo='mao', custo='—', caminho='magia', teto='normal', origens=('C', 'Me'), armas=None, ordem=None,
                     g=dict(devolve=(True, True, False, False, True, True), cedo=(0, 0, 1, 1, 1, 1)), medido=None, mede='d', cena='mago contra mago',
                     faz='I·Ap: o feitiço longo que se perde devolve metade da Mana; Ad·P: o longo sai uma rodada mais cedo, uma vez por luta; M·GM: as duas coisas (o "sempre" do contrato media +25: DESENHO 12.4)'),
    'mana_curta': dict(nome='a Mana Curta', campo='lançar', tipo='passiva', ritmo='luta', custo='—', caminho='magia', teto='normal', origens=('C', 'Lv'), armas=None, ordem=None,
                       g=dict(menos=(1, 1, 1, 1, 2, 2)), medido=None, mede='d', cena='mago contra mago', faz='o primeiro feitiço de cada luta custa menos Mana'),
}

APELIDOS = {'roda': 'roda', 'roda do malho': 'roda', 'sanha': 'sanha', 'trunfo': 'trunfos', 'trunfos': 'trunfos', 'tranco': 'tranco', 'corte': 'corte_fundo', 'corte fundo': 'corte_fundo',
            'rasteira': 'rasteira', 'riposta': 'riposta', 'quebra': 'golpe_quebra', 'golpe de quebra': 'golpe_quebra', 'bigorna': 'bigorna', 'guarda de bigorna': 'bigorna', 'brado': 'brado',
            'teima': 'teima', 'varrida': 'varrida', 'manter': 'manter', 'mira': 'mira_firme', 'mira firme': 'mira_firme', 'voto': 'golpe_voto', 'golpe de voto': 'golpe_voto', 'rito': 'rito_veia',
            'rito de veia': 'rito_veia', 'estanca': 'estanca', 'esquenta': 'esquenta', 'trato': 'trato', 'ferro': 'ferro_brasa', 'ferro em brasa': 'ferro_brasa', 'sopro': 'sopro_volta',
            'vigilia': 'vigilia', 'vigília': 'vigilia', 'benzimento': 'benzimento', 'fio': 'fio_conversa', 'fio da conversa': 'fio_conversa', 'lingua': 'lingua', 'língua': 'lingua',
            'língua de feira': 'lingua', 'malho': 'malho_quente', 'malho quente': 'malho_quente', 'paciência': 'paciencia', 'têmpera': 'tempera_certa', 'tempera': 'tempera_certa',
            'corrente': 'corrente', 'mana curta': 'mana_curta', 'mão no rito': 'mao_rito', 'pé de lebre': 'pe_lebre', 'lebre': 'pe_lebre'}
CAMPOS = ('batalhar', 'curar', 'convencer', 'trabalhar', 'copiar', 'mover', 'lançar')
ACESAS = tuple(k for k, h in HABILIDADES.items() if h['tipo'] == 'acesa')          # a Roda, a Sanha, o Rito de Veia: uma acesa por vez
DECLARADAS = tuple(k for k, h in HABILIDADES.items() if h['tipo'] == 'declarada')  # o Tranco, o Corte Fundo, a Rasteira: o primeiro golpe do turno
LUTA = tuple(k for k, h in HABILIDADES.items() if h['campo'] == 'batalhar') + ('estanca', 'ferro_brasa', 'sopro_volta', 'vigilia', 'pe_lebre', 'romper_linha', 'corrente', 'mao_rito', 'mana_curta', 'eco_golpe')
DE_LUTA = tuple(k for k, h in HABILIDADES.items() if h['ritmo'] in ('luta', 'dia'))   # a de luta ou de dia que venceu a cena dá +1 na marca
FALA = ('fio_conversa', 'lingua', 'palavra_firme', 'voz_praca', 'avaliador', 'ameaca_surda', 'penhor')
TRABALHO = ('malho_quente', 'paciencia', 'tempera_certa', 'brio', 'reparo', 'ajuste_fino')


def chave(k):
    """a chave do catálogo pelo nome ou apelido (sem acento, com espaço), ou None"""
    if not isinstance(k, str): return None
    k0 = k.strip().lower()
    if k0 in HABILIDADES: return k0
    return APELIDOS.get(k0) or next((x for x, h in HABILIDADES.items() if h['nome'].lower().split(' ', 1)[-1] == k0 or h['nome'].lower() == k0), None)


def num(k, campo, g):
    """o número de um campo da habilidade no grau g (0 a 5)"""
    return HABILIDADES[k]['g'][campo][max(0, min(GM, g))]


def letras_origem(k): return tuple(ORIGEM_CURTA[x] for x in HABILIDADES[k]['origens'])
def apelao(k): return HABILIDADES[k]['teto'] == 'apelão'


# ---------- O TESTE DE FALA (6.6) ----------
FALA_DEGRAUS = dict(pequeno=22, medio=28, grande=34, absurdo=40)      # a CD de cada degrau (+ metade do bônus de Vontade de quem ouve); 22 + 6 por degrau
FALA_ORDEM = ('pequeno', 'medio', 'grande', 'absurdo')
FALA_DIZ = dict(pequeno='pequeno', medio='médio', grande='grande', absurdo='absurdo')
FALA_EXEMPLO = dict(pequeno='o que não custa a ele: uma informação comum, 1 passo de preço, um dia a mais de prazo, deixar passar',
                    medio='o que custa algo: 2 passos de preço, um adiantamento, emprestar uma ferramenta, ir junto por metade da diária',
                    grande='o que custa caro: 3 passos de preço, arriscar a pele, vender o que não queria, a paga da missão +50%',
                    absurdo='o que vai contra ele: dar de graça o que vale muito, trair o senhor, abrir a porta')
FALA_JEITOS = dict(manso=-4, firme=0, duro=4)        # o jeito, dito antes: manso CD −4 (nunca ofende); firme; duro CD +4 (na ameaça, Força no lugar da Vontade)
FALA_BEM = 6                # passou por 6 ou mais: ganha, e leva mais um passo
FALA_OFENDE = 10            # falhou por 10 ou mais: não ganha, e ofende (no manso, é só "não"; no duro, falhar ofende sempre)
FALA_PALAVRA_FIRME = 5      # a Palavra Firme do Mestre: o duro que falha por menos de 5 não ofende (é só "não", com o −1 do duro)
FALA_SURDO = -6             # com a opinião −6 ou menos, ele não ouve pedido nenhum
FALA_HAB_TETO = TE.FIXO_TETO                  # as habilidades de fala somam até +8 (P3)
FALA_MEMORIA = dict(manso=1, nao_grande=-1, duro=-1, ofende=-3)        # o que ele lembra (uma linha por conversa): +1 do manso (uma vez por semana por pessoa); −1; −1 do duro; −3 da ofensa
FALA_MANSO_SEMANA = 7
FALA_CAMINHO = dict(negocio='comércio', oficio=None, sermao='fé', mentira='manha')   # a mão do caminho: comércio no negócio; a do ofício quando se fala dele; fé no sermão; manha na mentira
PASSO_PRECO = 0.05          # um passo é 5 pontos no que a loja paga ou cobra; uma vez por loja por dia
TETO_BENS = 0.80            # nunca acima dos tetos de hoje: 80% pelos bens, 60% pelas peças (na compra, nunca abaixo da base)
TETO_PECAS = 0.60
PASSOS_COMPRA = 2           # na compra, o regateio tira até a margem da loja (os 10% de cima: dois passos); a peça da prateleira (do Perito da Língua de Feira), o mesmo
PRECO_RECUSA = dict(pequeno=-1, medio=-2, grande=-2, absurdo=-3)       # o preço de recusar a fala da gente que passou (a opinião dele)
CAIXA_PRAZO = 2             # o pedido da caixa negociado: mais prazo (pequeno) dá tantos dias
CAIXA_PAGA = dict(medio=0.25, grande=0.50)    # mais paga: médio +25%, grande +50%
MISSAO_PAGA = 0.50          # a paga da missão +50% (grande)
