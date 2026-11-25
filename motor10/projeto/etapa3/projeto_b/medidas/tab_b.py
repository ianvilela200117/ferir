"""tab_b.py — RASCUNHO da página `tabelas_gente.py` do projeto B (etapa 3): os números da gente que responde.

É o que o protótipo de medida (proto_b.py) usa. No motor de verdade estes números moram numa página só (tabelas_gente.py), e o banco os confere.
Tudo aqui é proposta: o que a medida mostrou está no PROJETO.md, ao lado de cada número.
"""

# ---------- a bolsa: quanto a gente com nome guarda (a prata anda entre a bolsa e o caixa do lugar, uma vez por semana) ----------
BOLSA = dict(diarista=15, aprendiz=30, oficial=60, mestre=150)      # o que cada grau quer ter na bolsa (a vila de teste nasce perto disso: Ivo 12, Rute 25, Tomé 40, Bento 60)
BOLSA_PAPEL = dict(mercador=2.5, nobre=10, capitao=2)                # o papel que guarda mais (Lino, 150)
VIVER_DIA = 3                                                       # o que a pessoa gasta por dia para viver (a cama e a comida do personagem: 3)
# a semana: a bolsa anda para o alvo. Abaixo dele, o lugar paga a sobra da semana (a jornada menos o viver: diarista 7, aprendiz 21, oficial 63, mestre 119);
# acima dele, o que passa volta ao caixa do lugar (a pessoa gasta). Quem junta para uma encomenda tem o alvo mais o preço dela.

# ---------- a rotina: onde a pessoa está e o que faz em cada bloco (madrugada, alvorada, manhã, tarde, entardecer, noite). Não grava nada: sai desta tabela ----------
ROTINAS = {
    'oficio':    [('casa', 'dorme'), ('casa', 'dorme'), ('oficio', 'trabalha'), ('oficio', 'trabalha'), ('taverna', 'conversa'), ('casa', 'dorme')],
    'campo':     [('casa', 'dorme'), ('ermo', 'trabalha'), ('ermo', 'trabalha'), ('praça', 'vende'), ('taverna', 'conversa'), ('casa', 'dorme')],
    'taverna':   [('casa', 'dorme'), ('casa', 'dorme'), ('taverna', 'trabalha'), ('taverna', 'trabalha'), ('taverna', 'trabalha'), ('taverna', 'trabalha')],
    'guarda':    [('casa', 'dorme'), ('casa', 'dorme'), ('praça', 'vigia'), ('praça', 'vigia'), ('taverna', 'conversa'), ('praça', 'vigia')],
    'santuario': [('santuário', 'dorme'), ('santuário', 'reza'), ('santuário', 'trabalha'), ('praça', 'conversa'), ('santuário', 'trabalha'), ('santuário', 'dorme')],
    'passagem':  [('pousada', 'dorme'), ('pousada', 'dorme'), ('praça', 'à toa'), ('mercado', 'à toa'), ('taverna', 'conversa'), ('pousada', 'dorme')],
    'nobre':     [('casa', 'dorme'), ('casa', 'dorme'), ('casa', 'recebe'), ('praça', 'passeia'), ('casa', 'janta'), ('casa', 'dorme')],
    'ladino':    [('casa', 'dorme'), ('casa', 'dorme'), ('praça', 'à toa'), ('mercado', 'à toa'), ('taverna', 'conversa'), ('praça', 'à toa')],
}
PUBLICOS = ('oficio', 'taverna', 'praça', 'mercado', 'pousada')      # onde se furta (a casa e o santuário, não; o ermo é fora)

# ---------- os papéis: o que a pessoa é no lugar (o gerador de gente lê daqui; a história da etapa 7 pode trazer o seu) ----------
# papel: (rotina, grau de ofício, molde, nível (de, até), maestria, peças [(tipo, família ou material, categoria, cobre, uso)], desgaste por semana, o ponto do ofício)
PAPEIS = {
    'alcaide':    ('oficio', 'oficial', 'comum', (15, 30), {'comércio': 2}, [('arma', 'adaga', 0, None, 'arma')], 0, 'praça'),
    'ferreiro':   ('oficio', 'oficial', 'guerreiro', (20, 35), {'forja': 4, 'martelo': 2}, [('arma', 'martelo', 0, None, 'arma'), ('armadura', 'couro', 0, None, 'veste')], 0, 'forja'),
    'mestre_ferreiro': ('oficio', 'mestre', 'guerreiro', (35, 60), {'forja': 6, 'martelo': 4}, [('arma', 'martelo', 1, None, 'arma'), ('armadura', 'couro', 1, None, 'veste')], 0, 'forja'),
    'aprendiz':   ('oficio', 'aprendiz', 'comum', (3, 10), {}, [], 0, 'forja'),
    'taverneiro': ('taverna', 'oficial', 'comum', (8, 20), {'comércio': 2}, [('arma', 'adaga', 0, None, 'arma')], 0, 'taverna'),
    'mercador':   ('oficio', 'oficial', 'comum', (8, 20), {'comércio': 4}, [], 0, 'mercado'),
    'guarda':     ('guarda', 'oficial', 'guerreiro', (18, 35), {'lança': 4}, [('arma', 'lança', 0, None, 'arma'), ('escudo', None, 0, None, 'escudo'), ('armadura', 'malha', 0, None, 'veste')], 0.3, 'praça'),
    'capitao':    ('guarda', 'mestre', 'guerreiro', (40, 70), {'espada': 6}, [('arma', 'espada', 1, None, 'arma'), ('escudo', None, 1, None, 'escudo'), ('armadura', 'malha', 1, None, 'veste')], 0.3, 'praça'),
    'cacador':    ('campo', 'aprendiz', 'arqueiro', (12, 28), {'arco': 4, 'caça': 4}, [('arma', 'arco', 0, None, 'arma'), ('armadura', 'couro', 0, None, 'veste')], 0.5, 'ermo'),
    'lenhador':   ('campo', 'diarista', 'guerreiro', (8, 18), {'machado': 2, 'coleta': 2}, [('arma', 'machado', 0, None, 'arma')], 0.3, 'ermo'),
    'lavrador':   ('campo', 'diarista', 'comum', (3, 12), {}, [], 0, 'ermo'),
    'curandeiro': ('oficio', 'aprendiz', 'comum', (10, 20), {'cura': 2}, [('arma', 'adaga', 0, None, 'arma')], 0, 'botica'),
    'sacerdote':  ('santuario', 'oficial', 'comum', (15, 40), {'fé': 4}, [], 0, 'santuário'),
    'encantador': ('oficio', 'mestre', 'comum', (25, 50), {'encanto': 4}, [], 0, 'runas'),
    'caravaneiro': ('passagem', 'oficial', 'guerreiro', (20, 35), {'malho': 4}, [('arma', 'malho', 0, None, 'arma'), ('armadura', 'malha', 0, None, 'veste')], 0.5, 'praça'),
    'nobre':      ('nobre', 'mestre', 'comum', (10, 30), {'espada': 2}, [('arma', 'espada', 1, None, 'arma')], 0, 'casa'),
    'ladino':     ('ladino', 'diarista', 'arqueiro', (10, 20), {'manha': 2, 'adaga': 2}, [('arma', 'adaga', 0, None, 'arma')], 0, 'praça'),
    'mago':       ('oficio', 'oficial', 'comum', (20, 50), {'arcano': 4}, [], 0, 'casa'),
    'bruxa':      ('oficio', 'aprendiz', 'comum', (15, 40), {'pacto': 4}, [], 0, 'casa'),
}
# quantos de cada papel por tipo de lugar (o gerador; a vila de teste já tem os dela)
POVOAR = {
    'capital': ['alcaide', 'capitao', 'guarda', 'guarda', 'guarda', 'guarda', 'mestre_ferreiro', 'ferreiro', 'aprendiz', 'encantador', 'taverneiro', 'taverneiro', 'mercador', 'mercador',
                'mercador', 'curandeiro', 'sacerdote', 'nobre', 'nobre', 'nobre', 'caravaneiro', 'caravaneiro', 'ladino', 'cacador', 'lavrador', 'lavrador', 'lenhador', 'aprendiz', 'guarda', 'ferreiro'],
    'cidade': ['alcaide', 'capitao', 'guarda', 'guarda', 'mestre_ferreiro', 'aprendiz', 'encantador', 'taverneiro', 'mercador', 'mercador', 'curandeiro', 'sacerdote', 'caravaneiro', 'ladino', 'cacador'],
    'vila': ['alcaide', 'ferreiro', 'taverneiro', 'mercador', 'guarda', 'curandeiro', 'cacador', 'lenhador', 'lavrador'],
    'aldeia': ['alcaide', 'taverneiro', 'cacador', 'lavrador'],
}

# ---------- o querer da semana (um por pessoa; o dia da semana de cada um sai do nome: um sétimo da gente por dia) ----------
# querer: o peso, quando o motivo está no estado. "nada" sempre pode.
QUERER = dict(encomendar=6, melhorar=1, consertar=8, missao=4, viajar=1, laco=2, falar=3, cobrar=5, retribuir=3, furtar=4, nada=8)
QUERER_PAPEL = dict(mercador=dict(viajar=3, missao=2), alcaide=dict(missao=3), ladino=dict(furtar=1))       # multiplica o peso pelo papel
GASTA = 0.6                 # a peça abaixo desta fração da durabilidade pede conserto
QUEBRA = 0.0                # quebrada (ou faltando), pede peça nova
MELHORA = 2.0               # quer a peça uma categoria acima quem tem na bolsa esta vez o preço dela
RESERVA = 1.0               # na encomenda, o cliente paga o sinal agora e guarda o resto; junta até ter o preço inteiro
SINAL = 0.3                 # a fração do preço que vai adiantada
PRAZO_RESPOSTA = 12         # blocos para responder na caixa (dois dias)
PRAZO_OBRA = 3              # a entrega: os blocos de bancada da peça ÷ 2, mais estes dias
ATRASO = 0.1                # cada dia de atraso tira isto da paga (até a metade)
FAMA_FERREIRO = dict(aprendiz=5, oficial=15, mestre=35)
FAMA_BANCADA = 10           # a cada tantos blocos de bancada no lugar (a obra, o conserto, o jornal), +1 de fama de ofício ali: quem serve na forja fica conhecido
MISSAO_GASTA = 3            # quem cumpre (ou falha) uma missão de luta volta com a arma e a armadura gastas disto      # a fama de ofício de quem já tem a forja do lugar (o ferreiro de nome) no lugar dele

# ---------- a loja que encomenda (a freguesia de A compra da prateleira; a loja repõe com o ferreiro) ----------
FREGUESIA = dict(vila=1.0, cidade=3.0, capital=8.0, aldeia=0.3)     # ARREMEDO (chute, até a metade A medir): peças Comuns que o povo leva da prateleira por semana
LOJA_PAGA = 0.6             # a loja que encomenda paga esta fração do valor (a loja paga 40% pela peça que lhe oferecem; pela que ela pede, 60%)

# ---------- a memória: até 12 fatos, com peso; a opinião é a soma (de −10 a 10), com os porquês ----------
MEMORIA = 12
FATOS = {   # tipo: (peso, o eixo da fama que a notícia dele mexe, os pontos de fama, o alcance da notícia em saltos, o texto)
    'entregou':     (3, 'ofício', 3, 1, 'fez a peça que pediu, no prazo'),
    'entregou_tarde': (1, 'ofício', 1, 1, 'fez a peça que pediu, com atraso'),
    'falhou_obra':  (-4, 'ofício', -3, 1, 'não entregou a peça que prometeu'),
    'recusou':      (-1, None, 0, 0, 'recusou o pedido dele'),
    'calou':        (-2, None, 0, 0, 'não respondeu quando ele pediu'),
    'pagou':        (1, None, 0, 0, 'pagou o que devia'),
    'cumpriu':      (5, 'feito', 4, 2, 'cumpriu a missão que ele pediu'),
    'falhou_missao': (-4, 'feito', -2, 2, 'falhou na missão que pegou'),
    'salvou':       (8, 'feito', 10, 3, 'salvou a vida dele'),
    'deu':          (2, None, 0, 0, 'deu-lhe alguma coisa'),
    'feriu_junto':  (-2, None, 0, 0, 'ele se feriu indo com você'),
    'morreu_junto': (-8, None, 0, 2, 'alguém dele morreu indo com você'),
    'roubou':       (-6, 'crime', 10, 2, 'roubou dele'),
    'viu_roubar':   (-3, 'crime', 0, 0, 'viu você roubar'),
    'suspeita':     (-2, 'crime', 3, 1, 'desconfia que você o roubou'),
    'ouviu':        (0, None, 0, 0, 'ouviu falar de você'),     # o peso vem da notícia que chegou
}
CANAL = dict(viu=1.0, ouviu=0.5, boato=0.25)        # quem viu lembra o peso inteiro; quem ouviu, a metade; do boato, um quarto (sempre pelo menos 1)
ESFRIA = [(3, 28), (7, 56)]                         # o fato de peso até 3 perde 1 a cada 28 dias; até 7, a cada 56; de 8 para cima, nunca esfria
OPINIAO = [(-7, 'odeia você'), (-4, 'não gosta de você'), (-1, 'desconfia de você'), (0, 'não tem opinião sobre você'), (3, 'simpatiza com você'), (6, 'gosta de você'), (10, 'confia em você')]
RECUSA_NEGOCIO = -6         # com a opinião até aqui, quem atende (a loja, a taverna, a forja) não negocia com você
NAO_PEDE = -4               # com a opinião até aqui, a pessoa não lhe pede nada nem vai junto
DIRIGE = 2                  # com a opinião daqui para cima (ou a fama de feito), a missão vem à sua caixa, e não só ao quadro
FAMA_TOM = dict(feito=25, ofício=25, crime=-10)     # o pano de fundo da opinião, em todo mundo do lugar: +1 a cada 25 de feito e de ofício somados, −1 a cada 10 de crime
TOM = (-3, 2)               # ... de −3 a +2 (o que cada um lembra soma por cima)
FAMA_ESFRIA = 28            # a fama perde 1 ponto a cada tantos dias, em cada eixo (a conta sai na hora de ler: não grava nada)

# ---------- a notícia ----------
BOATO = 4                   # depois do quarto salto, a notícia vira boato
VIDA_NOTICIA = 28           # dias; passado isto e sem andar mais, sai do arquivo (o registro de eventos guarda)
OUVEM = 3                   # quantos nomeados de um lugar guardam a notícia que chega (os de laço com quem ela fala primeiro; depois, o do mesmo ofício; depois, o taverneiro)

# ---------- a caixa ----------
CAIXA = 7

# ---------- a missão: a paga pelo grau do perigo (F, E, D, C, B, A, S), a caução e o prazo ----------
GRAUS = ['F', 'E', 'D', 'C', 'B', 'A', 'S']
PAGA_GRAU = [10, 25, 60, 200, 800, 3000, 10000]
CAUCAO = 0.2
PRAZO_MISSAO = 14
LEVAR = (5, 3)              # levar uma carga ou um recado: 5 de prata, mais 3 por bloco de caminho, ida e volta (o diarista ganha 2 por bloco)
NOMEADO_FAZ = {1: 0.9, 0: 0.65, -1: 0.25}          # quem não é o personagem cumpre a missão (a conta rápida de etapa 5 entra aqui): pelo teto dele menos o grau
NOMEADO_MORRE = 0.15        # ... e, se falha uma missão acima do teto, morre nisto

# ---------- quem vai junto ----------
COMPANHIA = {-1: 0, 0: 1, 1: 3}     # o perigo menos o teto de quem vai: até −1 vai pela parte; no teto, pede a diária; um acima, três diárias (e só com opinião +2); dois acima, recusa
COMPANHIA_OPINIAO = [(7, 0.0), (4, 0.5)]           # opinião +7: vai de graça (só a parte); +4: metade

# ---------- o furto (capítulo 18.13, ligado com a memória e a vigia) ----------
FURTO_CONTRA = 20           # 20 + Percepção ÷ 10 da vítima
FURTO_GUARDA = 4            # mais isto se a vítima é guarda ou mercador, e mais isto se há guarda de vigia no ponto naquele bloco
FURTO_LEVA = 6              # 1d6 × (1 + metade do grau de manha)
FURTO_PENA = 3              # pego (falhou por 5 ou mais): paga o triplo ao caixa do lugar; sem prata, 3 dias preso
FURTO_PRESO = 3
DA_FALTA = 0.6              # quem foi furtado e não viu dá pela falta na virada do dia
VIGIA = (2, 28, 8)          # cada falta descoberta põe +2 em todo furto naquele lugar por 28 dias, até +8
VIGIA_FAMA = 10             # e +1 a cada 10 de fama de crime de quem furta, ali
