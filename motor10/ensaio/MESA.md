# MESA · turno 9 · Dia 8, alvorada (4h) · primavera

## Você
**Maro**, nível 5 · PV 141/141 · 5 de prata · em Pedra Rasa
Corpo: sem fome (fome 3) · sem sono (sono 0) · com forças (cansaço 3) · fôlego máximo −1
```
Maro (nível 5, mão de Iniciante) · PV 141/141 · fôlego 12 · 2 ações (a mais: 1 pelo dobro do fôlego)
  Espada de Maro: acerto +5,25 · 1d8 × 1 (corte), força × 1,21 · 1 de fôlego por golpe
  Defesa 30 (com Escudo de Maro) · proteção: cabeça 1 · tronco 1 · braços 1 · pernas 1
```
Peças (`ato.py vestir ITEM` · `ato.py tirar ITEM`): i0010 elmo de malha Comum (9/10) · EM USO, na cabeça · i0028 Espada de Maro (Comum, 7/10) · EM USO, na mão · i0029 Escudo de Maro (Comum, 9/10) · EM USO, no braço · i0030 Armadura de malha de Maro (Comum, 9/10) · EM USO, no corpo · i0044 a Espada do Guardião (Incomum, 20/20) · na guarda
Carga: 4 de comida, 1 de metal Comum, 1 de couro Comum (`ato.py comer carga` come da sua comida)
Treino: espada: 42 blocos (Iniciante) · caça: 6 blocos (Leigo)

## Aqui
**Pedra Rasa** · comida no lugar: 17.611 · há cama
Quem está aqui: Bento (o ferreiro da vila; conserta e vende o que forja), Dalva (a taverneira da pousada; sabe de tudo o que se conta), Rute (a caçadora; conhece a Mata do Corvo), Tomé (o guarda da vila), Ivo (o lenhador; tira madeira na borda da mata), Nara (a curandeira; colhe erva e trata ferida), Lino (o mercador da loja), Zeca (o aprendiz da forja; novo, quer aprender), Anselmo (o mago velho; ensina o arcano a quem paga, e lê o que os outros não leem), Lúcia (a clériga do santuário; cura quem pede e quebra maldição com rito), Joana (a bruxa que mora na choupana da borda da Mata do Corvo; lê a sorte, amaldiçoa por encomenda e vende veneno de lâmina, escondido), Durva (anã, ferreira de passagem; forja e conserta, e vai junto se a chamam), Brasco (meio-orc, guarda de caravana de passagem; viu o que o dragão deixou em Vau Seco), Ilvena (elfa, caçadora de passagem; segue rastro de noite), Nena Ramalho (pequenina, faz o pão da pousada; mora na vila), Quim (o sobrinho do Lino; abre trinco, anda calado e acha o que os outros não veem)
Perto daqui: a Cripta da Cova Velha, a 1 bloco: dizem que os mortos da Cova Velha subiam de uma escada, debaixo do mausoléu quebrado. O que se sabe e como descer: `masmorra.py ver`.

**O que dá para fazer, e o que custa** (1 bloco = 4 horas):
- comer: 1 de prata, fome −3 (`ato.py comer`; da sua carga, sem pagar: `ato.py comer carga`)
- dormir: cama por 2 de prata, e a sua está paga até o Dia 8, noite (20h); cada bloco tira 3 de sono e de cansaço (no chão, 2) e devolve PV (`ato.py dormir N`)
- trabalhar (diarista): 2 de prata por bloco, esforço pesado; a jornada são 2 blocos pagos por dia (hoje: 0 de 2) (`ato.py trabalhar N`)
- treinar com uma arma: esforço pesado; a maestria sobe aos 40, 160, 500, 1.500 blocos (`ato.py treinar N ARMA`)
- descansar, esperar (`ato.py descansar N`, `ato.py esperar N`) · lutar (`ato.py luta nova CENARIO ARQ`) · testar (`teste.py`)

## O mercado
**Pedra Rasa** · 400 de povo · a loja tem 2.005 de prata (sem prata, ela não compra) · comprar custa 10% a mais · a loja paga 60% do preço pelos bens e 40% do valor pelas peças (a sua mão em comércio: Leigo)

| bem | no lugar | preço do dia (× a base) | comprar | a loja paga | você carrega |
| --- | --- | --- | --- | --- | --- |
| comida | 17.611 | 1,17 (× 1,17) | 10 por 13 | 7 por 10 | 4 |
| lenha | 3.000 | 1,00 (× 1,00) | 10 por 12 | 5 por 10 |  |
| carvão | 240 | 2,00 (× 1,00) | 10 por 23 | 11 por 10 |  |
| sal | 240 | 3,00 (× 1,00) | 10 por 34 | 17 por 10 |  |
| pano | 120 | 5,00 (× 1,00) | 1 por 6 | 2 por 1 |  |
| remédio | 60 | 8,00 (× 1,00) | 1 por 9 | 4 por 1 |  |
| ferramenta | 60 | 12,00 (× 1,00) | 1 por 14 | 7 por 1 |  |
| metal Comum | 121 | 2,99 (× 1,00) | 10 por 34 | 17 por 10 | 1 |
| couro Comum | 125 | 1,96 (× 0,98) | 10 por 23 | 11 por 10 | 1 |
| osso Comum | 65 | 0,96 (× 0,96) | 10 por 12 | 5 por 10 |  |
| madeira Comum | 240 | 2,00 (× 1,00) | 10 por 23 | 11 por 10 |  |
| erva Comum | 120 | 2,00 (× 1,00) | 10 por 23 | 11 por 10 |  |
| metal Incomum | 19 | 18,47 (× 1,03) | 1 por 21 | 10 por 1 |  |
| couro Incomum | 21 | 11,71 (× 0,98) | 1 por 14 | 6 por 1 |  |
| osso Incomum | 9 | 6,32 (× 1,05) | 1 por 8 | 3 por 1 |  |
| madeira Incomum | 41 | 11,85 (× 0,99) | 1 por 14 | 7 por 1 |  |
| erva Incomum | 22 | 11,44 (× 0,95) | 1 por 13 | 6 por 1 |  |

**A magia** (as poções até a Rara; a água benta; a peçonha):
| bem | no lugar | preço do dia (× a base) | comprar | a loja paga | você carrega |
| --- | --- | --- | --- | --- | --- |
| poção de cura Comum | 4 | 7,35 (× 1,22) | 1 por 9 | 4 por 1 |  |
| antídoto Comum | 3 | 4,95 (× 0,82) | 1 por 6 | 2 por 1 |  |
| poção de Mana Comum | 1 | 6,00 (× 1,00) | 1 por 10 | 2 por 1 |  |
| poção de guarda Comum | 1 | 6,00 (× 1,00) | 1 por 10 | 2 por 1 |  |
| poção de fúria Comum | 1 | 6,00 (× 1,00) | 1 por 10 | 2 por 1 |  |
| poção de quebra-maldição Comum | 1 | 6,57 (× 1,10) | 1 por 11 | 3 por 1 |  |
| antídoto Incomum | 1 | 36,00 (× 1,00) | 1 por 57 | 17 por 1 |  |
| poção de Mana Incomum | 1 | 36,00 (× 1,00) | 1 por 57 | 17 por 1 |  |
| poção de guarda Incomum | 1 | 36,00 (× 1,00) | 1 por 57 | 17 por 1 |  |
| poção de fúria Incomum | 1 | 36,00 (× 1,00) | 1 por 57 | 17 por 1 |  |
| poção de vigília Incomum | 1 | 36,00 (× 1,00) | 1 por 57 | 17 por 1 |  |
| poção de quebra-maldição Incomum | 1 | 36,00 (× 1,00) | 1 por 57 | 17 por 1 |  |
| água benta | 4 | 3,67 (× 1,22) | 4 por 26 | 15 por 10 |  |

**A descida** (a tocha arde um bloco na masmorra):
| bem | no lugar | preço do dia (× a base) | comprar | a loja paga | você carrega |
| --- | --- | --- | --- | --- | --- |
| tocha | 120 | 1,00 (× 1,00) | 10 por 12 | 5 por 10 |  |

**A prateleira** (peças do Livro de Itens; o preço é o de tabela, menos o desgaste; a arma vale pela matéria que leva, e a armadura pelo que cobre). A loja está farta: tem 2 peças Comuns além das 17 que ela quer ter:
- novas, a 8 de prata cada (Comum): i0008 elmo de couro Comum · i0054 elmo miúdo de malha Comum
- novas, a 10 de prata cada (Comum): i0001 adaga Comum · i0031 amuleto Comum · i0032 amuleto Comum · i0058 gazua Comum
- novas, a 30 de prata cada (Comum): i0002 espada Comum · i0003 maça Comum · i0004 machado Comum · i0005 lança Comum · i0006 arco Comum · i0007 armadura de couro Comum · i0009 armadura de malha Comum · i0011 escudo Comum · i0033 varinha Comum · i0034 símbolo Comum · i0035 Cartilha do arcano · i0052 armadura de couro miúda Comum · i0053 armadura de malha miúda Comum
- novas, a 180 de prata cada (Incomum): i0012 espada Incomum · i0013 lança Incomum · i0014 armadura de couro Incomum · i0015 escudo Incomum

**As suas peças** (o que a loja paga: 40% do valor; 20% a menos por peça igual que ela já tem, e por peça da mesma categoria além das que quer ter; a que está em uso não se vende sem guardar): i0010 elmo de malha Comum (9/10) EM USO: 0 · i0028 Espada de Maro (Comum, 7/10) EM USO: 5 · i0029 Escudo de Maro (Comum, 9/10) EM USO: 6 · i0030 Armadura de malha de Maro (Comum, 9/10) EM USO: 3 · i0044 a Espada do Guardião (Incomum, 20/20): 57

Negociar não gasta bloco: `mercado.py comprar BEM N` · `mercado.py vender BEM N|tudo` · `mercado.py vender tudo` (a cesta: um troco só) · `mercado.py comprar ITEM` · `mercado.py vender ITEM` · `mercado.py preco BEM N` (só olha)

## A oficina
**Pedra Rasa:** forja de vila (+1) · conserta, pago, até o Raro
Mão: forja Leigo (0 blocos de bancada; Iniciante aos 50)
Preparo (+2 cada, na obra que ele alcança): receita: não há · ajudante: não há · fogo: até o Incomum · bigorna: até o Incomum
Matéria na carga: 1 de metal Comum, 1 de couro Comum

**Na bancada** (bloco pesado; `oficio.py pede ...` diz a matéria e a chance antes de abrir):
- forjar: Comum 1, Incomum 3, Raro 9, Épico 27, Único 81, Lendário 243 blocos; do Épico para cima pede núcleo. Falhar por 5 ou mais: a matéria some.
- consertar elmo de malha Comum (i0010, 9/10): você, 1 bloco e 1 de metal Comum; pago, 1 de prata e 1 bloco de espera
- consertar Espada de Maro (i0028, 7/10): você, 1 bloco e 1 de metal Comum; pago, 2 de prata e 1 bloco de espera
- consertar Escudo de Maro (i0029, 9/10): você, 1 bloco e 1 de madeira Comum; pago, 1 de prata e 1 bloco de espera
- consertar Armadura de malha de Maro (i0030, 9/10): você, 1 bloco e 1 de metal Comum; pago, 1 de prata e 1 bloco de espera
- o conserto pago (`oficio.py consertar ITEM pago`): 2% do preço da peça por ponto, em prata inteira (arredonda para cima: um ponto de uma espada Comum custa 1 de prata), e um bloco de espera por peça (a cada 10 pontos ou parte): mandar consertar quatro peças leva quatro blocos
- ajustar (sob medida): pede mão de Iniciante
- jornal: 2 de prata por bloco de bancada a serviço da oficina (paga-se pelo que a mão vale: diarista), até a jornada (2 blocos pagos por dia; hoje: 0) (`oficio.py jornal N`)

## A caça e a coleta
- **a Mata do Corvo** (floresta, borda), a 1 bloco [`mata`] · caça: corça (há fartura), goblin (é raro ver), javali (há fartura), lobo (há fartura), urso (há pouco, e sempre foi assim), pantera (há pouco, e sempre foi assim) · tira-se: madeira Comum (há fartura), erva Comum (há fartura)
- **a Cova Velha** (ruína, borda), a 1 bloco [`cova`] · caça: corpo-seco (sumiu), esqueleto (sumiu) · tira-se: metal Comum (há fartura), erva Comum (há fartura)
- A sua mão: caça Leigo (6 blocos), coleta Leigo (0 blocos). O rastro: 2d20 + 5 contra 20 ou mais (o bicho arisco e o que rareou pedem mais; de noite, −4). A coleta: 2d20 + 7 (minério, madeira) ou + 5 (erva) contra 20, mais 8 por categoria, e o que rareou pede mais; o bloco que passa rende 1 de minério, 2 de madeira ou 1 de erva, e o que falha não rende.
- `caca.py sair [ERMO] [alvo=ESPECIE] [blocos=N]` (ida, N de procura, volta; N de 1 a 6, 2 se não disser) · `caca.py coletar BEM [ERMO] [blocos=N]` (N de 1 a 4)

## Os bichos daqui (o que todo mundo sabe; a frase inteira: `bichos.py ameaca ESPECIE`)
- corça (grau F, Comum, média, de 1 a 2) · goblin (grau F, Comum, pequeno, bando de 2 a 4, povo que veste peças: noturno) · javali (grau E, Comum, médio, sozinho: investida) · lobo (grau D, Incomum, médio, bando de 3 a 5: matilha) · urso (grau D, Incomum, grande, sozinho: agarra) · pantera (grau C, Raro, média, sozinha: bote)

## A magia daqui
Os serviços, de pessoa a pessoa (o personagem paga a quem presta; o que ele faz pela gente do mundo sai sem cobrança): ler 10 · cura 3 o lance · bênção 5 por pessoa · tratar 2 e o remédio · benzer a arma 5 · o rito de quebrar: Comum 10, Incomum 60, Rara 360 de prata
- Anselmo sabe luz, seta, escudo, prender, lança de fogo: ensina a 10 de prata por bloco, até 2 blocos por dia
- Lúcia sabe luz, cura, bênção, amparo, castigo, quebrar maldição: ensina a 6 de prata por bloco, até 2 blocos por dia · lê maldição, dom e peça · quebra maldição (rito) · cura
- Joana sabe luz, mau-olhado, medo, sangria, ler, nó: ensina a 6 de prata por bloco, até 2 blocos por dia · lê maldição, dom e peça
- Nara trata ferida (2 de prata e um remédio; um tratamento por dia)
- o santuário (+1): o voto se faz aqui; a prece enche a Mana; a água benta e a bênção da arma (`magia_mundo.py agua N`, `benzer ARMA`); o jornal (`magia_mundo.py jornal N`)

## A botica e as poções
**Pedra Rasa:** botica de vila (+1) · a leva Comum: 1 bloco pesado, 4 de matéria, rende 2 doses (`alquimia.py pede cura Comum`)

De outros povos, aqui: Durva (anã), Brasco (meio-orc), Ilvena (elfa), Nena Ramalho (pequenina).

## O que se conta (os dragões de que a gente daqui sabe)
- Conta-se que o Tição, um dragão jovem da serra, mora na Serra Fria, e que há 6 dias levou gado de Vau Seco. Vau Seco fica longe daqui.

## Perguntas abertas
1. O Dia 8 (Maro com PV 141/141, 5 de prata e 4 de comida)?  **a)** a rotina: vende o despojo (uns 2 de prata), jornada (4) e treino de espada · **b)** procura a toca dos goblins, com Tomé e Rute (o que fugiu voltou para algum lugar; a procura é rolagem oculta) · **c)** javali, com a Rute · **d)** corça, sozinho · **e)** desce a Cripta da Cova Velha, com Tomé e Rute (a tocha: 1 de prata por bloco; luta grande, no jeito da mesa)
2. Maro quer começar a aprender magia?  **a)** faz o voto do socorro no santuário e estuda a cura lá, de graça (6 blocos leves com talento comum; nos blocos que sobrarem do dia) · **b)** ainda não

## SÓ O MESTRE
- nota: A etapa 4b entrou no save antes do Dia 8 (vila_teste.py fantasia, inclinacao2=manha). A pergunta 1, ainda sem resposta, ganhou a opção e (a cripta).
- a contagem na Mata do Corvo: corça 76/80 · goblin 6/16 · javali 38/40 · lobo 12/12 · urso 3/3 · pantera 1/1 · serpe 1/1 · acaso 3% por bloco
- a contagem na Cova Velha: corpo-seco 0/2 · esqueleto 0/3 · acaso 0% por bloco
- talento e dom de Bento: Jeitoso em couro, Lerdo em comércio, Lerdo em alquimia
- talento e dom de Dalva: Jeitoso em haste, Lerdo em forja, Lerdo em couro, Jeitoso em alquimia, Lerdo em encanto, Lerdo em pacto
- talento e dom de Rute: Jeitoso em tiro, Jeitoso em comércio, Lerdo em alquimia, Lerdo em arcano
- talento e dom de Tomé: Lerdo em forja, Negado em fé
- talento e dom de Ivo: Jeitoso em cura
- talento e dom de Nara: Jeitoso em haste, Jeitoso em coleta, Jeitoso em alquimia (já aparece), Lerdo em pacto
- talento e dom de Lino: Jeitoso em forja, Lerdo em coleta, Lerdo em alquimia, Jeitoso em arcano
- talento e dom de Zeca: Jeitoso em haste, Prodígio em forja, Jeitoso em couro, Prodígio em coleta, Jeitoso em encanto, Lerdo em arcano, Lerdo em fé, Prodígio em verde, Grande Dom em forja (escondido)
- talento e dom de Maro: Jeitoso em haste, Jeitoso em tiro, Lerdo em fé, Jeitoso em pacto · inclinação do jogador: fio · segunda inclinação: manha
- talento e dom de Anselmo: Lerdo em haste, Jeitoso em peso, Lerdo em couro, Jeitoso em caça, Prodígio em fé, Lerdo em pacto
- talento e dom de Lúcia: Lerdo em haste, Lerdo em coleta, Lerdo em cura, Lerdo em alquimia
- talento e dom de Joana: Jeitoso em caça, Negado em manha
- talento e dom de Durva: Lerdo em comércio, Lerdo em cura, Prodígio em arcano
- talento e dom de Brasco: Lerdo em fio, Lerdo em haste, Jeitoso em comércio, Lerdo em encanto, Jeitoso em fé, Jeitoso em verde
- talento e dom de Ilvena: Jeitoso em fio, Lerdo em haste, Jeitoso em couro, Negado em caça, Lerdo em fé, Jeitoso em verde
- talento e dom de Nena Ramalho: Lerdo em fio, Jeitoso em peso, Jeitoso em caça, Lerdo em cura, Negado em verde, Lerdo em pacto, Dom em tiro (escondido)
- talento e dom de Quim: Jeitoso em fio, Jeitoso em forja, Prodígio em couro, Jeitoso em comércio, Prodígio em verde
- magia de Anselmo: Mana 19 de 19 · o arcano: Treinado (160 blocos) · sabe: luz, seta, escudo, prender, lança de fogo · foco: Cajado de Anselmo
- magia de Lúcia: Mana 17 de 19 · a fé: Mestre (502 blocos) · sabe: luz, cura, bênção, amparo, castigo, quebrar maldição · voto do socorro (em Pedra Rasa) · foco: Símbolo de Lúcia
- magia de Joana: Mana 19 de 19 · o pacto: Treinado (160 blocos) · sabe: luz, mau-olhado, medo, sangria, ler, nó · dívida 2 (acima de 7 vira maldição) · foco: Talismã de Joana
- peça maldita: i0044 a Espada do Guardião (a Mão Fria, Incomum, míngua); quebra: devolver a Espada do Guardião ao lugar dela, na Cova Velha
- a toca dos goblins na Mata do Corvo: 6 goblins (teto 16), o capataz goblin de pé · fome 0 · tesouro: 20 de prata, 0 de comida (`caca.py sair mata alvo=toca`)
- a Cripta da Cova Velha [cripta]: 11 morando nas salas, o chefe do fundo vivo, 80 de prata nas salas, alarme 0 (`masmorra.py mapa cripta`)
- a manha de Quim: Iniciante (40 blocos); gazua: Gazua de Quim (Comum)
- o Tição (dragão jovem da serra, grau C, 60 anos) na Serra Fria: PV 480 de 480 · dorme até o Dia 28 (vigília 29, mais 2 por punhado; 0 tirados neste sono) · o tesouro: 300 de prata; as peças: a Lâmina de Vau Seco e o escudo do caçador de Vau Seco · a vila: Vau Seco (1 ataque, o último no Dia 2) (`dragoes.py covil serra_fria`)
- o estado está inteiro.
