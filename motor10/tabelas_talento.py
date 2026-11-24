"""tabelas_talento.py — MOTOR 10: TODOS os números dos dons e dos talentos (etapa da magia, capítulo 10).

Dois botões na pessoa, para todo caminho. O TALENTO diz a pressa de aprender e o teto (não soma em conta nenhuma). O DOM diz o poder (soma na conta, como maestria
que ninguém treinou). Quem não tem nada de especial é exatamente a pessoa de hoje: multiplica por 1 e soma zero.
Mudar os dons e os talentos é mudar esta página e rodar `provas_talento.py` (o `provas_mundo.py` também o roda).
"""
import math

# ---------- os caminhos (17): quatro mãos de arma, nove ofícios, quatro tradições ----------
MAOS = {'fio': ('adaga', 'espada', 'machado', 'montante'), 'haste': ('lança', 'alabarda'), 'peso': ('maça', 'martelo', 'malho'), 'tiro': ('arco', 'besta')}      # o soco não é de mão nenhuma
OFICIOS = ['forja', 'couro', 'caça', 'coleta', 'comércio', 'cura', 'alquimia', 'encanto', 'manha']       # a manha (etapa 4b): o ofício do ladino (andar escondido, escutar, achar, desarmar, abrir)
TRADICOES = ['arcano', 'fé', 'verde', 'pacto']
CAMINHOS = list(MAOS) + OFICIOS + TRADICOES
def caminho_de(chave): return next((m for m, fs in MAOS.items() if chave in fs), chave)      # 'espada' é do caminho 'fio'; 'forja' é dela mesma
NOVOS = ['manha']           # os caminhos que entraram depois da etapa da magia: quem já tinha o talento rolado rola só estes (talento.rola_caminho), sem mexer no dom
ANTIGOS = [c for c in CAMINHOS if c not in NOVOS]      # os 16 de antes: o dom se sorteia entre eles como sempre (uma segunda sorte o passa a um caminho novo, na proporção)

# ---------- o talento: cinco graus (nome · vezes os blocos de cada grau de maestria · o teto da mão) ----------
TALENTO = {-2: ('Negado', 2.0, 2), -1: ('Lerdo', 1.5, 6), 0: ('Comum', 1.0, 8), 1: ('Jeitoso', 2 / 3, 8), 2: ('Prodígio', 0.5, 8)}       # M3 a: o Prodígio aprende com a metade
TALENTO_D100 = [(2, -2), (12, -1), (88, 0), (98, 1), (100, 2)]      # o d100 do mundo em cada caminho: até 2, Negado; até 12, Lerdo; até 88, Comum; até 98, Jeitoso; 99 e 100, Prodígio
INCLINACAO = 2              # no caminho que o jogador escolhe para o personagem, o d100 rola tantas vezes e vale o melhor (M2 b); vale também para a segunda inclinação do personagem humano (E2 b)
TENDENCIA = 1               # a tendência do povo (etapa 4b): no caminho a favor, mais tantos dados (vale o melhor); no contra, mais tantos (vale o pior). O que soma e o que tira se anulam
APARECE = 20                # blocos feitos no caminho, depois de rolado, para o talento aparecer na MESA (quem aprende depressa percebe fazendo)
def vezes(grau): return TALENTO[grau][1]
def blocos(n, grau): return math.ceil(round(n * TALENTO[grau][1], 6))      # n blocos para quem tem este talento (arredondados para cima: o Jeitoso firma em 107 o que pede 160)

# ---------- o dom: dois graus (o nome · o que soma na conta do caminho) ----------
DOM = {1: ('Dom', 1), 2: ('Grande Dom', 2)}
DOM_D1000 = [(5, 2), (50, 1)]       # o d1000 do mundo, um por pessoa: até 5, Grande Dom; até 50, Dom; o resto, nada. A pessoa tem no máximo um
DOM_PESO = 3                # o caminho do dom sai entre os 16, com este peso onde a pessoa já é Jeitosa ou Prodígio
DOM_COMERCIO = {1: 0.025, 2: 0.05}      # no comércio o dom soma isto na fração que a loja paga (sem passar do teto: 80% pelos bens, 60% pelas peças)
# o nome do dom de cada caminho, para a mesa ("Há alguma coisa nas suas mãos: a mão que fecha")
DOM_NOME = {'fio': 'o fio na mão', 'haste': 'a haste certa', 'peso': 'o braço pesado', 'tiro': 'o olho do tiro', 'forja': 'a mão do fogo', 'couro': 'a mão do couro',
            'caça': 'o faro', 'coleta': 'o olho da terra', 'comércio': 'a língua do negócio', 'cura': 'a mão que fecha', 'alquimia': 'o nariz da botica', 'encanto': 'a mão das runas',
            'arcano': 'a centelha', 'fé': 'a graça', 'verde': 'o sangue verde', 'pacto': 'o olho torto', 'manha': 'a mão leve'}
DOM_ONDE = {'mao': 'no acerto com as armas dessa mão, e metade na Defesa', 'bancada': 'no teste da obra, dentro do teto de +8 do preparo', 'rastro': 'no teste',
            'comércio': 'no que a loja lhe paga', 'tradicao': 'na Conjuração, metade na Firmeza, e o mesmo na Mana', 'manha': 'nos testes do ladino (andar escondido, escutar, achar, desarmar, abrir)'}

# ---------- a mesa: como cada caminho se diz ----------
O_QUE = {'fio': 'as armas de fio (adaga, espada, machado, montante)', 'haste': 'as armas de haste (lança, alabarda)', 'peso': 'as armas de peso (maça, martelo, malho)',
         'tiro': 'o arco e a besta', 'forja': 'a forja', 'couro': 'o couro', 'caça': 'a caça', 'coleta': 'a coleta', 'comércio': 'o comércio', 'cura': 'a cura',
         'alquimia': 'a alquimia', 'encanto': 'o encanto', 'arcano': 'o arcano', 'fé': 'a fé', 'verde': 'o verde', 'pacto': 'o pacto',
         'manha': 'a manha (andar escondido, escutar, achar e desarmar armadilha, abrir fechadura)'}
