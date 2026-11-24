# MESA · turno 3 · Dia 2, alvorada (4h) · primavera

## Você
**Maro**, nível 5 · PV 141/141 · 31 de prata · em Pedra Rasa
Corpo: sem fome (fome 0) · sem sono (sono 0) · com forças (cansaço 0)
```
Maro (nível 5, mão de Iniciante) · PV 141/141 · fôlego 13 · 2 ações (a mais: 1 pelo dobro do fôlego)
  Espada de Maro: acerto +5,25 · 1d8 × 1 (corte), força × 1,21 · 1 de fôlego por golpe
  Defesa 30 (com Escudo de Maro) · proteção: tronco 1 · braços 1 · pernas 1 · SEM PROTEÇÃO: cabeça
```
Peças (`ato.py vestir ITEM` · `ato.py tirar ITEM`): i0028 Espada de Maro (Comum, 10/10) · EM USO, na mão · i0029 Escudo de Maro (Comum, 10/10) · EM USO, no braço · i0030 Armadura de malha de Maro (Comum, 10/10) · EM USO, no corpo
Treino: espada: 41 blocos (Iniciante)

## Aqui
**Pedra Rasa** · comida no lugar: 18.625 · há cama
Quem está aqui: Bento (o ferreiro da vila; conserta e vende o que forja), Dalva (a taverneira da pousada; sabe de tudo o que se conta), Rute (a caçadora; conhece a Mata do Corvo), Tomé (o guarda da vila), Ivo (o lenhador; tira madeira na borda da mata), Nara (a curandeira; colhe erva e trata ferida), Lino (o mercador da loja), Zeca (o aprendiz da forja; novo, quer aprender)

**O que dá para fazer, e o que custa** (1 bloco = 4 horas):
- comer: 1 de prata, fome −3 (`ato.py comer`; da sua carga, sem pagar: `ato.py comer carga`)
- dormir: cama por 2 de prata, e a sua está paga até o Dia 2, noite (20h); cada bloco tira 3 de sono e de cansaço (no chão, 2) e devolve PV (`ato.py dormir N`)
- trabalhar (diarista): 2 de prata por bloco, esforço pesado; a jornada são 2 blocos pagos por dia (hoje: 0 de 2) (`ato.py trabalhar N`)
- treinar com uma arma: esforço pesado; a maestria sobe aos 40, 160, 500, 1.500 blocos (`ato.py treinar N ARMA`)
- descansar, esperar (`ato.py descansar N`, `ato.py esperar N`) · lutar (`ato.py luta nova CENARIO ARQ`) · testar (`teste.py`)

## O mercado
**Pedra Rasa** · 400 de povo · a loja tem 1.999 de prata (sem prata, ela não compra) · comprar custa 10% a mais · a loja paga 60% do preço pelos bens e 40% do valor pelas peças (a sua mão em comércio: Leigo)

| bem | no lugar | preço do dia (× a base) | comprar | a loja paga | você carrega |
| --- | --- | --- | --- | --- | --- |
| comida | 18.625 | 1,14 (× 1,14) | 10 por 13 | 6 por 10 |  |
| lenha | 3.000 | 1,00 (× 1,00) | 10 por 12 | 5 por 10 |  |
| carvão | 240 | 2,00 (× 1,00) | 10 por 23 | 11 por 10 |  |
| sal | 240 | 3,00 (× 1,00) | 10 por 34 | 17 por 10 |  |
| pano | 120 | 5,00 (× 1,00) | 1 por 6 | 2 por 1 |  |
| remédio | 60 | 8,00 (× 1,00) | 1 por 9 | 4 por 1 |  |
| ferramenta | 60 | 12,00 (× 1,00) | 1 por 14 | 7 por 1 |  |
| metal Comum | 120 | 3,00 (× 1,00) | 10 por 34 | 17 por 10 |  |
| couro Comum | 120 | 2,00 (× 1,00) | 10 por 23 | 11 por 10 |  |
| osso Comum | 60 | 1,00 (× 1,00) | 10 por 12 | 5 por 10 |  |
| madeira Comum | 240 | 2,00 (× 1,00) | 10 por 23 | 11 por 10 |  |
| erva Comum | 120 | 2,00 (× 1,00) | 10 por 23 | 11 por 10 |  |
| metal Incomum | 21 | 17,57 (× 0,98) | 1 por 20 | 10 por 1 |  |
| couro Incomum | 19 | 12,31 (× 1,03) | 1 por 14 | 7 por 1 |  |
| osso Incomum | 9 | 6,32 (× 1,05) | 1 por 8 | 3 por 1 |  |
| madeira Incomum | 40 | 12,00 (× 1,00) | 1 por 14 | 7 por 1 |  |
| erva Incomum | 20 | 12,00 (× 1,00) | 1 por 14 | 7 por 1 |  |

**A prateleira** (peças do Livro de Itens; o preço é o de tabela, menos o desgaste; a arma vale pela matéria que leva, e a armadura pelo que cobre):
- novas, a 8 de prata cada (Comum): i0008 elmo de couro Comum · i0010 elmo de malha Comum
- novas, a 10 de prata cada (Comum): i0001 adaga Comum
- novas, a 30 de prata cada (Comum): i0002 espada Comum · i0003 maça Comum · i0004 machado Comum · i0005 lança Comum · i0006 arco Comum · i0007 armadura de couro Comum · i0009 armadura de malha Comum · i0011 escudo Comum
- novas, a 180 de prata cada (Incomum): i0012 espada Incomum · i0013 lança Incomum · i0014 armadura de couro Incomum · i0015 escudo Incomum

**As suas peças** (o que a loja paga: 40% do valor; 20% a menos por peça igual que ela já tem, e por peça da mesma categoria além das que quer ter; a que está em uso não se vende sem guardar): i0028 Espada de Maro (Comum, 10/10) EM USO: 9 · i0029 Escudo de Maro (Comum, 10/10) EM USO: 9 · i0030 Armadura de malha de Maro (Comum, 10/10) EM USO: 7

Negociar não gasta bloco: `mercado.py comprar BEM N` · `mercado.py vender BEM N|tudo` · `mercado.py vender tudo` (a cesta: um troco só) · `mercado.py comprar ITEM` · `mercado.py vender ITEM` · `mercado.py preco BEM N` (só olha)

## A oficina
**Pedra Rasa:** forja de vila (+1) · conserta, pago, até o Raro
Mão: forja Leigo (0 blocos de bancada; Iniciante aos 50)
Preparo (+2 cada, na obra que ele alcança): receita: não há · ajudante: não há · fogo: até o Incomum · bigorna: até o Incomum

**Na bancada** (bloco pesado; `oficio.py pede ...` diz a matéria e a chance antes de abrir):
- forjar: Comum 1, Incomum 3, Raro 9, Épico 27, Único 81, Lendário 243 blocos; do Épico para cima pede núcleo. Falhar por 5 ou mais: a matéria some.
- ajustar (sob medida): pede mão de Iniciante
- jornal: 2 de prata por bloco de bancada a serviço da oficina (paga-se pelo que a mão vale: diarista), até a jornada (2 blocos pagos por dia; hoje: 0) (`oficio.py jornal N`)

## A caça e a coleta
- **a Mata do Corvo** (floresta, borda), a 1 bloco [`mata`] · caça: corça (há fartura), javali (há fartura), lobo (há fartura), urso (há pouco, e sempre foi assim), pantera (há pouco, e sempre foi assim) · tira-se: madeira Comum (há fartura), erva Comum (há fartura)
- A sua mão: caça Leigo (0 blocos), coleta Leigo (0 blocos). O rastro: 2d20 + 5 contra 20 ou mais (o bicho arisco e o que rareou pedem mais; de noite, −4). A coleta: 2d20 + 7 (minério, madeira) ou + 5 (erva) contra 20, mais 8 por categoria, e o que rareou pede mais; o bloco que passa rende 1 de minério, 2 de madeira ou 1 de erva, e o que falha não rende.
- `caca.py sair [ERMO] [alvo=ESPECIE] [blocos=N]` (ida, N de procura, volta; N de 1 a 6, 2 se não disser) · `caca.py coletar BEM [ERMO] [blocos=N]` (N de 1 a 4)

## Os bichos daqui (o que todo mundo sabe; a frase inteira: `bichos.py ameaca ESPECIE`)
- corça (grau F, Comum, média, de 1 a 2) · javali (grau E, Comum, médio, sozinho: investida) · lobo (grau D, Incomum, médio, bando de 3 a 5: matilha) · urso (grau D, Incomum, grande, sozinho: agarra) · pantera (grau C, Raro, média, sozinha: bote)

## Perguntas abertas
1. O que Maro faz no Dia 2?  **a)** repete a rotina (jornada e um bloco de treino de espada) por vários dias: diga quantos · **b)** vai sozinho à Mata do Corvo atrás de corça · **c)** chama a Rute e vai atrás de javali (ela leva a parte dela do despojo) · **d)** vai atrás de lobos (bando de 3 a 5: perigo de morte para quem está sozinho)
2. Maro compra o elmo de malha (8 de prata) antes de se meter em luta? A cabeça está sem proteção.  **a)** compra · **b)** não compra: guarda a prata

## SÓ O MESTRE
- a contagem na Mata do Corvo: corça 80/80 · javali 40/40 · lobo 12/12 · urso 3/3 · pantera 1/1 · serpe 1/1 · acaso 3% por bloco
- o estado está inteiro.
