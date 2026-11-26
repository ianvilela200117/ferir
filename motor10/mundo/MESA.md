# MESA · turno 9 · Dia 16, manhã (8h) · primavera

## Você
**Ferord**, nível 5 · PV 111/111 · 32 de prata · em Pedra Velha
Corpo: sem fome (fome 2) · sem sono (sono 1) · com forças (cansaço 0)
```
Ferord (nível 5, mão de Iniciante) · PV 111/111 · fôlego 11 · 2 ações (a mais: 1 pelo dobro do fôlego)
  Martelo de Ferord: acerto +1,75 · 1d10 × 1 (impacto), força × 1,18 · 3 de fôlego por golpe
  Defesa 28,5 · proteção: tronco 0,7 · braços 0,7 · pernas 0,7 · cabeça 1
```
Peças (`ato.py vestir ITEM` · `ato.py tirar ITEM`): i0658 Martelo de Ferord (Comum, 10/10) · EM USO, na mão · i0659 Couro de Ferord (Comum, 10/10) · EM USO, no corpo · i0660 Elmo de Ferord (Comum, 10/10) · EM USO, na cabeça
Carga: 3 de metal Comum, 2 de madeira Comum, 2 de metal Incomum
Treino: forja: 97 blocos (Iniciante) · martelo: 40 blocos (Iniciante) · comércio: 1 dia de negócio (Leigo)
Com a forja você pega depressa (Jeitoso): o que os outros firmam em 150 blocos, você firma em 100.
Do povo dos humanos, 20 anos: a medida de todos.

## Aqui
**Pedra Velha** · comida no lugar: 14.675 · há cama
Quem está aqui: Filipa (o ferreiro; conserta e vende o que forja), Berareu (lavra a terra), Félix (da taverna; sabe de tudo o que se conta), Adelaide (aprende o ofício da casa), Osorino (da guarda de Pedra Velha), Nora (caça no ermo e vende o couro), Paio (cura ferida e colhe erva), Tânia (mercador; compra e vende, e leva carga pela estrada), Erado (o mais velho do lugar; sabe das histórias antigas)

**O que dá para fazer, e o que custa** (1 bloco = 4 horas):
- comer: 1 de prata, fome −3 (`ato.py comer`; da sua carga, sem pagar: `ato.py comer carga`)
- dormir: cama por 2 de prata, e a sua está paga até o Dia 17, madrugada (0h); cada bloco tira 3 de sono e de cansaço (no chão, 2) e devolve PV (`ato.py dormir N`)
- trabalhar (aprendiz): 3 de prata por bloco, esforço pesado; a jornada são 2 blocos pagos por dia (hoje: 0 de 2) (`ato.py trabalhar N`)
- treinar com uma arma: esforço pesado; a maestria sobe aos 40, 160, 500, 1.500 blocos (`ato.py treinar N ARMA`)
- descansar, esperar (`ato.py descansar N`, `ato.py esperar N`) · lutar (`ato.py luta nova CENARIO ARQ`) · testar (`teste.py`)

## O mercado
**Pedra Velha** · 360 de povo · a loja tem 1.729 de prata (sem prata, ela não compra) · comprar custa 10% a mais · a loja paga 60% do preço pelos bens e 40% do valor pelas peças (a sua mão em comércio: Leigo)

| bem | no lugar | preço do dia (× a base) | comprar | a loja paga | você carrega |
| --- | --- | --- | --- | --- | --- |
| comida | 14.675 | 1,21 (× 1,21) | 10 por 14 | 7 por 10 |  |
| lenha | 2.700 | 1,00 (× 1,00) | 10 por 12 | 5 por 10 |  |
| carvão | 216 | 2,00 (× 1,00) | 10 por 23 | 11 por 10 |  |
| sal | 215 | 3,01 (× 1,00) | 10 por 34 | 17 por 10 |  |
| pano | 110 | 4,95 (× 0,99) | 1 por 6 | 2 por 1 |  |
| remédio | 52 | 8,15 (× 1,02) | 1 por 10 | 4 por 1 |  |
| ferramenta | 52 | 12,23 (× 1,02) | 1 por 14 | 7 por 1 |  |
| metal Comum | 109 | 2,99 (× 1,00) | 10 por 34 | 17 por 10 | 3 |
| couro Comum | 107 | 2,01 (× 1,00) | 10 por 23 | 11 por 10 |  |
| osso Comum | 55 | 0,99 (× 0,99) | 10 por 12 | 5 por 10 |  |
| madeira Comum | 217 | 2,00 (× 1,00) | 10 por 23 | 11 por 10 | 2 |
| erva Comum | 105 | 2,03 (× 1,01) | 10 por 23 | 11 por 10 |  |
| metal Incomum | 16 | 19,09 (× 1,06) | 1 por 22 | 11 por 1 | 2 |
| couro Incomum | 16 | 12,73 (× 1,06) | 1 por 15 | 7 por 1 |  |
| osso Incomum | 11 | 5,43 (× 0,90) | 1 por 7 | 3 por 1 |  |
| madeira Incomum | 35 | 12,17 (× 1,01) | 1 por 14 | 7 por 1 |  |
| erva Incomum | 19 | 11,68 (× 0,97) | 1 por 14 | 6 por 1 |  |

**A magia** (as poções até a Rara; a água benta; a peçonha):
| bem | no lugar | preço do dia (× a base) | comprar | a loja paga | você carrega |
| --- | --- | --- | --- | --- | --- |
| poção de cura Comum | 5 | 6,24 (× 1,04) | 1 por 8 | 3 por 1 |  |
| antídoto Comum | 2 | 5,75 (× 0,96) | 1 por 8 | 3 por 1 |  |
| poção de Mana Comum | 1 | 6,00 (× 1,00) | 1 por 10 | 2 por 1 |  |
| poção de guarda Comum | 1 | 6,00 (× 1,00) | 1 por 10 | 2 por 1 |  |
| poção de fúria Comum | 1 | 6,00 (× 1,00) | 1 por 10 | 2 por 1 |  |
| poção de quebra-maldição Comum | 1 | 6,24 (× 1,04) | 1 por 10 | 3 por 1 |  |
| água benta | 6 | 2,85 (× 0,95) | 6 por 32 | 12 por 10 |  |

**A prateleira** (peças do Livro de Itens; o preço é o de tabela, menos o desgaste; a arma vale pela matéria que leva, e a armadura pelo que cobre):
- novas, a 8 de prata cada (Comum): i0214 elmo de couro Comum · i0216 elmo de malha Comum
- novas, a 10 de prata cada (Comum): i0207 adaga Comum · i0222 amuleto Comum · i0223 amuleto Comum
- novas, a 30 de prata cada (Comum): i0208 espada Comum · i0209 maça Comum · i0210 machado Comum · i0211 lança Comum · i0212 arco Comum · i0213 armadura de couro Comum · i0215 armadura de malha Comum · i0217 escudo Comum · i0224 varinha Comum · i0225 símbolo Comum · i0226 Cartilha do arcano
- novas, a 180 de prata cada (Incomum): i0218 espada Incomum · i0219 lança Incomum · i0220 armadura de couro Incomum · i0221 escudo Incomum

**As suas peças** (o que a loja paga: 40% do valor; 20% a menos por peça igual que ela já tem, e por peça da mesma categoria além das que quer ter; a que está em uso não se vende sem guardar): i0658 Martelo de Ferord (Comum, 10/10) EM USO: 16 · i0659 Couro de Ferord (Comum, 10/10) EM USO: 7 · i0660 Elmo de Ferord (Comum, 10/10) EM USO: 1

Negociar não gasta bloco: `mercado.py comprar BEM N` · `mercado.py vender BEM N|tudo` · `mercado.py vender tudo` (a cesta: um troco só) · `mercado.py comprar ITEM` · `mercado.py vender ITEM` · `mercado.py preco BEM N` (só olha)

## A oficina
**Pedra Velha:** forja de vila (+1) · conserta, pago, até o Raro
Mão: forja Iniciante (97 blocos de bancada; Treinado aos 150)
Preparo (+2 cada, na obra que ele alcança): receita: até o Incomum · ajudante: não há · fogo: até o Incomum · bigorna: até o Incomum
Matéria na carga: 3 de metal Comum, 2 de madeira Comum, 2 de metal Incomum

**Na bancada** (bloco pesado; `oficio.py pede ...` diz a matéria e a chance antes de abrir):
- forjar: Comum 1, Incomum 3, Raro 9, Épico 27, Único 81, Lendário 243 blocos; do Épico para cima pede núcleo. Falhar por 5 ou mais: a matéria some.
- o conserto pago (`oficio.py consertar ITEM pago`): 2% do preço da peça por ponto, em prata inteira (arredonda para cima: um ponto de uma espada Comum custa 1 de prata), e um bloco de espera por peça (a cada 10 pontos ou parte): mandar consertar quatro peças leva quatro blocos
- ajustar (sob medida): grau 1; de 1 (Comum) a 6 blocos (Lendário) e um teste contra 22 + 6 por categoria
- jornal: 3 de prata por bloco de bancada a serviço da oficina (paga-se pelo que a mão vale: aprendiz), até a jornada (2 blocos pagos por dia; hoje: 0) (`oficio.py jornal N`)

## A caça e a coleta
- **a Charneca dos Sinos** (campo, borda), a 2 blocos [`charneca_dos_sinos`] · caça: corça (há fartura), lobo (há fartura), lobisomem (há pouco, e sempre foi assim) · tira-se: erva Comum (há fartura), madeira Comum (há fartura)
- A sua mão: caça Leigo (0 blocos), coleta Leigo (0 blocos). O rastro: 2d20 + 4 contra 20 ou mais (o bicho arisco e o que rareou pedem mais; de noite, −4). A coleta: 2d20 + 6 (minério, madeira) ou + 4 (erva) contra 20, mais 8 por categoria, e o que rareou pede mais; o bloco que passa rende 1 de minério, 2 de madeira ou 1 de erva, e o que falha não rende.
- `caca.py sair [ERMO] [alvo=ESPECIE] [blocos=N]` (ida, N de procura, volta; N de 1 a 6, 2 se não disser) · `caca.py coletar BEM [ERMO] [blocos=N]` (N de 1 a 4)

## Os bichos daqui (o que todo mundo sabe; a frase inteira: `bichos.py ameaca ESPECIE`)
- corça (grau F, Comum, média, de 1 a 2) · lobo (grau D, Incomum, médio, bando de 3 a 5: matilha) · lobisomem (grau C, Raro, médio, sozinho: regenera, amaldiçoa, noturno)

## A magia daqui
Os serviços, de pessoa a pessoa (o personagem paga a quem presta; o que ele faz pela gente do mundo sai sem cobrança): ler 10 · cura 3 o lance · bênção 5 por pessoa · tratar 2 e o remédio · benzer a arma 5 · o rito de quebrar: Comum 10, Incomum 60, Rara 360 de prata
- Paio trata ferida (2 de prata e um remédio; um tratamento por dia)
- o santuário (+1): o voto se faz aqui; a prece enche a Mana; a água benta e a bênção da arma (`magia_mundo.py agua N`, `benzer ARMA`); o jornal (`magia_mundo.py jornal N`)

## A botica e as poções
**Pedra Velha:** panela (+0) · a leva Comum: 1 bloco pesado, 4 de matéria, rende 2 doses (`alquimia.py pede cura Comum`)

**Estradas daqui** (`viagem.py ir DESTINO`):
- para Souto Negro: 2 blocos; de assalto às vezes
- para Castro do Sal: 2 blocos; de assalto às vezes
- para Várzea Brava: 3 blocos; de assalto às vezes
- para Ribeira da Névoa: 3 blocos; de assalto às vezes

**O que a gente daqui lembra de você:**
- Filipa (pai/mãe): confia em você (+6) — é do meu sangue; Ferord aprendeu comigo a receita do Incomum, em três dias de bancada; Ferord pediu que eu lhe ensinasse o Incomum, e passou o dia comigo na bancada, até o limite das forças
- Berareu (parente): gosta de você (+2) — é do meu sangue

**O ranking da semana 3** (fama e peças): 1. Drastum (340) · 2. Nynena (340) · 3. Taskin (323) · 4. Mirys (164) · 5. Ernesto (119) · você: 0

**As frentes que você conhece** (pelos sinais; `frentes.py investigar FID`):
- f11 · alguém some na borda do mato em Souto Negro
- f01 · mais salteadores aparecem na estrada em Castro Real
- f02 · o bando da toca cresce em Penha das Rosas
- f06 · o mercador compra todo o metal que acha em Vale do Corvo
- f09 · o rio baixa em Pedra Verde

**Notícias que chegaram aqui** (as mais novas):
- Dia 16 (de Souto Negro): Alguém some na borda do mato em Souto Negro
- Dia 16 (de Castro do Sal): Ofélia conta da história: no ano 827, morre Sílvia (de velho, na cama); Davi assume a casa dos Orirena.
- Dia 14 (de Ribeira do Lobo): Nynena mata serpe nos Penhascos das Águas
- Dia 12 (de Penha das Rosas): dizem que o bando da toca cresce em Penha das Rosas
- Dia 12 (de Pinhal do Ferro): dizem que helena conta da história: no ano 961, marelão expulsou os orcs da serra até o último.
- Dia 11 (de Coval do Vento): Lino conta da história: no ano 1057, morre Perado (de peste); Rosa assume a casa dos Orirena.

## Perguntas abertas
1. A notícia do Dia 16: alguém sumiu na borda do mato, em Souto Negro (a vila vizinha, a 2 blocos de estrada). Todo mundo daqui sabe que na Charneca dos Sinos há um lobisomem (há pouco, e sempre foi assim: grau C, regenera, amaldiçoa, anda de noite)?  **a)** segue a rotina: não é assunto de ferreiro · **b)** pergunta na vila o que se sabe, à noite, na taverna, sem perder a jornada: Nora caça na Charneca, Paio colhe erva lá, Osorino é da guarda, Félix ouve tudo · **c)** investiga a frente: 1 bloco leve e um teste, rolado uma vez (2d20 + 4 da Percepção contra 26: quase metade das vezes); se passa, descobre uma coisa: o relógio dela, quem está por trás, o que quer ou onde é o centro
2. O martelo Incomum (32 de prata; faltam o 3º metal, 22 hoje, e a madeira, 14; a forja em 97 de 100: Treinado hoje à noite)?  **a)** compra hoje o 3º metal (22; fica com 10), antes que o mercador de Vale do Corvo chegue aqui; a madeira e a obra no Dia 18 (3 blocos; Treinado, com a receita e começando descansado: 74%) · **b)** junta e compra o metal e a madeira juntos no Dia 18 (36 de prata hoje) e forja no mesmo dia, com a mesma chance

## SÓ O MESTRE
- nota: O que Ferord ouviu na taverna (Dia 1): Félix: Ribeira da Névoa (3 blocos) tem forja de cidade e mesa de runas, e Várzea da Névoa também; Vale do Corvo, a capital, tem a grande forja e a oficina de runas, e o mestre Simão (o mestre ferreiro, não de runas); ninguém que ele conheça vive de gravar runas. Erado: Pedra Velha foi saqueada nas guerras de 781, 869 e 957; Brarku, que fez forjar o Malho do Silêncio, morreu aqui em 1165. A receita do Incomum de Filipa está ensinada desde o Dia 4. O talento de Ferord na forja (Jeitoso) aparece na MESA: Treinado aos 100 blocos (a linha da oficina ainda diz 150). A rotina de vários dias roda pelo condutor do Mestre (cópia em saidas/rotina_condutor.py.txt; as saídas em saidas/d*_rotina*.txt): para em pedido, notícia que toca Ferord (Pedra Velha, Charneca, Souto Negro, metal, forja, a casa), missão de ferreiro, gente de fora, metal Incomum com menos de 4 ou acima de 1,3 da base, perda de vida, evento em Pedra Velha, ou a frente f11 andando. A frente f11 (o lobisomem da Charneca, centro em Souto Negro) está no passo 1 e já é conhecida de Ferord pelo sinal. Repor esta nota, uma só, depois de cada turno.py fecha, e rodar turno.py abre.
- a contagem na Charneca dos Sinos: corça 72/80 · lobo 12/12 · lobisomem 1/1 · acaso 1% por bloco
- talento e dom de Filipa: Lerdo em arcano
- talento e dom de Berareu: Jeitoso em fio, Prodígio em tiro, Jeitoso em caça, Jeitoso em manha, Lerdo em pacto
- talento e dom de Félix: Prodígio em peso, Jeitoso em forja, Lerdo em coleta, Lerdo em comércio
- talento e dom de Adelaide: Jeitoso em haste, Lerdo em peso, Lerdo em manha, Negado em fé, Jeitoso em verde
- talento e dom de Osorino: Jeitoso em caça, Lerdo em alquimia
- talento e dom de Nora: Lerdo em haste, Prodígio em tiro, Lerdo em caça, Prodígio em comércio, Negado em cura, Lerdo em alquimia, Jeitoso em encanto, Jeitoso em fé, Prodígio em pacto, Dom em tiro (escondido)
- talento e dom de Paio: Lerdo em coleta, Jeitoso em cura, Jeitoso em alquimia, Prodígio em manha, Jeitoso em fé
- talento e dom de Tânia: Negado em haste, Jeitoso em forja, Jeitoso em coleta, Negado em comércio, Jeitoso em manha, Lerdo em arcano
- talento e dom de Erado: Lerdo em tiro, Jeitoso em cura, Jeitoso em pacto
- talento e dom de Ferord: Prodígio em fio, Lerdo em peso, Jeitoso em tiro, Jeitoso em forja (já aparece), Lerdo em cura, Jeitoso em alquimia, Jeitoso em arcano, Negado em pacto · inclinação do jogador: forja · segunda inclinação: encanto
- peça maldita: i0009 malho Raro (a praga da Mina da Névoa, Rara, insônia); quebra: devolver malho Raro ao lugar dela, no poço velho
- peça maldita: i0022 montante Comum (a praga da Toca do Sal, Comum, míngua); quebra: devolver montante Comum ao lugar dela, na sala dos presos
- a Fome da Serra (dragão ancião da serra, grau S) na câmara do tesouro: PV 1337 de 1337 · dorme até o Dia 421 (vigília 31, mais 2 por punhado; 0 tirados neste sono) · o tesouro: 1718 de prata; as peças: O Bordão da Serra · sem vila (caça no ermo) (`dragoes.py covil covil_dos_sinos_3`)
- o Brasa (dragão jovem da serra, grau C) nos Penhascos das Águas: PV 480 de 480 · dorme até o Dia 29 (vigília 29, mais 2 por punhado; 0 tirados neste sono) · o tesouro: 479 de prata; as peças: O Gume do Inverno · a vila: Ribeira do Lobo (1 ataque, o último no Dia 2) (`dragoes.py covil penhascos_das_aguas`)
- os salteadores nas estradas daqui: a estrada de Pedra Velha a Souto Negro: 1; a estrada de Castro do Sal a Pedra Velha: 0; a estrada de Pedra Velha a Várzea Brava: 1; a estrada de Ribeira da Névoa a Pedra Velha: 0
- as frentes: f01 o bando de Sara na estrada (passo 1) · f02 a horda da toca do Souto das Águas (passo 1) · f03 os mortos da Cripta dos Miraves (passo 0) · f04 o dragão Brasa (passo 0) · f05 a ambição dos Astolan (passo 0) · f06 o cartel de Selina (passo 1) · f07 o culto de Moninho (passo 1) · f08 a corrida da Liga do Sino Rachado (passo 0) · f09 a seca de Pedra Verde (passo 1) · f10 a falta de sal de Castro Branco (passo 1) · f11 os sumiços da Charneca dos Sinos (passo 1) · f12 as luzes das Ruínas do Urso (passo 0) · f13 Fome da Serra, o que dorme (passo 0)
- a pauta do diretor (o que pode entrar em cena hoje): os sumiços da Charneca dos Sinos (passo 1, a 1 estrada(s) daqui, andou nesta semana) · o culto de Moninho (passo 1, a 2 estrada(s) daqui, andou nesta semana) · o bando de Sara na estrada (passo 1, a 2 estrada(s) daqui)
- dois fatos que não tocam o personagem (para a cena): Alguém some na borda do mato em Souto Negro · Gente some de noite em Vale do Corvo
- o estado está inteiro.
