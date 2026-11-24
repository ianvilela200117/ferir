"""tabelas_povos.py — MOTOR 10, ETAPA 4b: TODOS os números dos povos do personagem (capítulo 19; o contrato: projeto/ETAPA_4B.md, seções 8 e 12).

Seis povos: o humano (a medida de todos), o anão, o elfo, o meio-orc, o pequenino e o gnomo. Cada um mexe nos seis atributos COM A SOMA IGUAL (soma zero), tem de
nenhum a dois traços da lista fechada (tabelas.TRACOS_POVO), uma coragem, um CORPO (gente ou miúdo: a armadura é feita para o corpo), uma TENDÊNCIA nos talentos (um caminho
a favor, um contra), a vida longa, e um bônus de +2 num teste do ladino (o teto de +2 por teste).
O NÚCLEO DO MOTOR LÊ ESTA PÁGINA DIRETO (o gravador, o lutador, o talento, a luta): os campos de POVOS (mods, tracos, coragem, corpo, a_favor, contra, vida, frase) e os
números ESCURO e VENENO. A frente P (os povos) muda os NÚMEROS; os nomes dos campos e o humano neutro não mudam.
Esqueleto do alicerce (onda 1): os números são o rascunho do projeto B (projeto/etapa4b/projeto_b/PROJETO.md, anexo), a conferir pela frente P no banco (provas_povos.py).
"""

# ---------- os povos ----------
# mods: o que soma em cada atributo (a soma é zero) · tracos: a lista fechada (tabelas.TRACOS_POVO) · coragem: soma no teste de coragem · corpo: 'gente' ou 'miúdo'
# a_favor / contra: o caminho da tendência (tabelas_talento.TENDENCIA: melhor de dois / pior de dois) · vida: (adulto aos, velho aos, o máximo) · frase: o que o jogador lê
POVOS = {
    'humano':    dict(mods={}, tracos=[], coragem=0, corpo='gente', a_favor=None, contra=None, vida=(16, 60, 90),
                      frase='a medida de todos: nada a mais, nada a menos'),
    'anão':      dict(mods=dict(Vigor=5, Vontade=5, Agilidade=-5, Percepção=-5), tracos=['vê no escuro', 'resiste a veneno'], coragem=0, corpo='gente',
                      a_favor='forja', contra='verde', vida=(30, 200, 300),
                      frase='duro, teimoso e de vista curta; vê na penumbra das minas, e o veneno o pega pela metade'),
    'elfo':      dict(mods=dict(Agilidade=10, Percepção=10, Afinidade=5, Vigor=-5, Força=-10, Vontade=-10), tracos=['vê no escuro'], coragem=0, corpo='gente',
                      a_favor='tiro', contra='peso', vida=(80, 500, 800),
                      frase='leve e de olho longo, frágil de corpo e de pouca paciência; vê na penumbra'),
    'meio-orc':  dict(mods=dict(Força=10, Vigor=5, Afinidade=-10, Vontade=-5), tracos=['vê no escuro'], coragem=0, corpo='gente',
                      a_favor='peso', contra='encanto', vida=(14, 50, 75),
                      frase='forte e de sangue quente; vê na penumbra, como o pai orc'),
    'pequenino': dict(mods=dict(Força=-15, Agilidade=5, Percepção=5, Vontade=5), tracos=[], coragem=4, corpo='miúdo',
                      a_favor='manha', contra='haste', vida=(25, 80, 130),
                      frase='miúdo e sem medo: o pavor pega pouco nele, e anda sem ser ouvido'),
    'gnomo':     dict(mods=dict(Afinidade=10, Percepção=5, Força=-10, Vigor=-5), tracos=['vê no escuro'], coragem=0, corpo='miúdo',
                      a_favor='encanto', contra='peso', vida=(35, 250, 400),
                      frase='miúdo, curioso e de mão fina; vê na penumbra, e o mecanismo não tem segredo para ele'),
}
HUMANO = 'humano'           # quem não tem o campo `povo` é humano (o save antigo, a gente de hoje)
CORPOS = ('gente', 'miúdo')

# ---------- os traços do povo (a frase; os nomes moram no tabelas.TRACOS_POVO) ----------
TRACOS = {'vê no escuro': 'o escuro tira a metade: −2 no golpe, −4 no tiro; fora da luta, anda, procura, abre e desarma sem luz',
          'resiste a veneno': 'o veneno tira a metade por rodada'}
ESCURO = 0.5                # a fração do escuro (tabelas.TEMPO['escuro']) que ainda pesa em quem vê no escuro
VENENO = 0.5                # a fração do veneno (o que entra por rodada) que pesa em quem resiste a veneno

# ---------- o +2 do povo nos testes do ladino (os testes: tabelas_manha.TESTES; achar_pedra: o achar em lugar de pedra, a cripta, a mina, a ruína) ----------
MANHA = {'pequenino': {'escondido': 2}, 'elfo': {'achar': 2}, 'anão': {'achar_pedra': 2}, 'gnomo': {'gazua': 2, 'desarmar': 2}, 'meio-orc': {'arrombar': 2}}
MANHA_TETO = 2              # o povo não soma mais que isto num teste (um grau de maestria, o mesmo do Grande Dom)
