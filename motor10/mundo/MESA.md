# MESA · turno 6 · Dia 4, manhã (8h) · primavera

## Você
**Ferord**, nível 5 · PV 111/111 · 39 de prata · em Pedra Velha
Corpo: sem fome (fome 2) · sem sono (sono 0) · com forças (cansaço 1)
```
Ferord (nível 5, mão de Iniciante) · PV 111/111 · fôlego 11 · 2 ações (a mais: 1 pelo dobro do fôlego)
  Martelo de Ferord: acerto +1,75 · 1d10 × 1 (impacto), força × 1,18 · 3 de fôlego por golpe
  Defesa 28,5 · proteção: tronco 0,7 · braços 0,7 · pernas 0,7 · cabeça 1
```
Peças (`ato.py vestir ITEM` · `ato.py tirar ITEM`): i0658 Martelo de Ferord (Comum, 10/10) · EM USO, na mão · i0659 Couro de Ferord (Comum, 10/10) · EM USO, no corpo · i0660 Elmo de Ferord (Comum, 10/10) · EM USO, na cabeça
Carga: 3 de metal Comum, 2 de madeira Comum
Treino: forja: 61 blocos (Iniciante) · martelo: 40 blocos (Iniciante)
Do povo dos humanos, 20 anos: a medida de todos.

## Aqui
**Pedra Velha** · comida no lugar: 16.450 · há cama
Quem está aqui: Filipa (o ferreiro; conserta e vende o que forja), Berareu (lavra a terra), Félix (da taverna; sabe de tudo o que se conta), Adelaide (aprende o ofício da casa), Osorino (da guarda de Pedra Velha), Nora (caça no ermo e vende o couro), Paio (cura ferida e colhe erva), Tânia (mercador; compra e vende, e leva carga pela estrada), Erado (o mais velho do lugar; sabe das histórias antigas)

**O que dá para fazer, e o que custa** (1 bloco = 4 horas):
- comer: 1 de prata, fome −3 (`ato.py comer`; da sua carga, sem pagar: `ato.py comer carga`)
- dormir: cama por 2 de prata, e a sua está paga até o Dia 5, madrugada (0h); cada bloco tira 3 de sono e de cansaço (no chão, 2) e devolve PV (`ato.py dormir N`)
- trabalhar (aprendiz): 3 de prata por bloco, esforço pesado; a jornada são 2 blocos pagos por dia (hoje: 0 de 2) (`ato.py trabalhar N`)
- treinar com uma arma: esforço pesado; a maestria sobe aos 40, 160, 500, 1.500 blocos (`ato.py treinar N ARMA`)
- descansar, esperar (`ato.py descansar N`, `ato.py esperar N`) · lutar (`ato.py luta nova CENARIO ARQ`) · testar (`teste.py`)

## O mercado
**Pedra Velha** · 360 de povo · a loja tem 1.761 de prata (sem prata, ela não compra) · comprar custa 10% a mais · a loja paga 60% do preço pelos bens e 40% do valor pelas peças (a sua mão em comércio: Leigo)

| bem | no lugar | preço do dia (× a base) | comprar | a loja paga | você carrega |
| --- | --- | --- | --- | --- | --- |
| comida | 16.450 | 1,15 (× 1,15) | 10 por 13 | 6 por 10 |  |
| lenha | 2.700 | 1,00 (× 1,00) | 10 por 12 | 5 por 10 |  |
| carvão | 216 | 2,00 (× 1,00) | 10 por 23 | 11 por 10 |  |
| sal | 216 | 3,00 (× 1,00) | 10 por 34 | 17 por 10 |  |
| pano | 109 | 4,98 (× 1,00) | 1 por 6 | 2 por 1 |  |
| remédio | 54 | 8,00 (× 1,00) | 1 por 9 | 4 por 1 |  |
| ferramenta | 53 | 12,11 (× 1,01) | 1 por 14 | 7 por 1 |  |
| metal Comum | 108 | 3,00 (× 1,00) | 10 por 34 | 17 por 10 | 3 |
| couro Comum | 108 | 2,00 (× 1,00) | 10 por 23 | 11 por 10 |  |
| osso Comum | 55 | 0,99 (× 0,99) | 10 por 12 | 5 por 10 |  |
| madeira Comum | 217 | 2,00 (× 1,00) | 10 por 23 | 11 por 10 | 2 |
| erva Comum | 106 | 2,02 (× 1,01) | 10 por 23 | 11 por 10 |  |
| metal Incomum | 18 | 18,00 (× 1,00) | 1 por 21 | 10 por 1 |  |
| couro Incomum | 18 | 12,00 (× 1,00) | 1 por 14 | 7 por 1 |  |
| osso Incomum | 9 | 6,00 (× 1,00) | 1 por 7 | 3 por 1 |  |
| madeira Incomum | 35 | 12,17 (× 1,01) | 1 por 14 | 7 por 1 |  |
| erva Incomum | 18 | 12,00 (× 1,00) | 1 por 14 | 7 por 1 |  |

**A magia** (as poções até a Rara; a água benta; a peçonha):
| bem | no lugar | preço do dia (× a base) | comprar | a loja paga | você carrega |
| --- | --- | --- | --- | --- | --- |
| poção de cura Comum | 5 | 6,24 (× 1,04) | 1 por 8 | 3 por 1 |  |
| antídoto Comum | 2 | 5,75 (× 0,96) | 1 por 8 | 3 por 1 |  |
| poção de Mana Comum | 1 | 6,00 (× 1,00) | 1 por 10 | 2 por 1 |  |
| poção de guarda Comum | 1 | 6,00 (× 1,00) | 1 por 10 | 2 por 1 |  |
| poção de fúria Comum | 1 | 6,00 (× 1,00) | 1 por 10 | 2 por 1 |  |
| poção de vigília Comum | 1 | 6,24 (× 1,04) | 1 por 10 | 3 por 1 |  |
| poção de quebra-maldição Comum | 1 | 6,24 (× 1,04) | 1 por 10 | 3 por 1 |  |
| água benta | 5 | 3,12 (× 1,04) | 5 por 29 | 13 por 10 |  |

**A prateleira** (peças do Livro de Itens; o preço é o de tabela, menos o desgaste; a arma vale pela matéria que leva, e a armadura pelo que cobre):
- novas, a 8 de prata cada (Comum): i0214 elmo de couro Comum · i0216 elmo de malha Comum
- novas, a 10 de prata cada (Comum): i0207 adaga Comum · i0222 amuleto Comum · i0223 amuleto Comum
- novas, a 30 de prata cada (Comum): i0208 espada Comum · i0209 maça Comum · i0210 machado Comum · i0211 lança Comum · i0212 arco Comum · i0213 armadura de couro Comum · i0215 armadura de malha Comum · i0217 escudo Comum · i0224 varinha Comum · i0225 símbolo Comum · i0226 Cartilha do arcano
- novas, a 180 de prata cada (Incomum): i0218 espada Incomum · i0219 lança Incomum · i0220 armadura de couro Incomum · i0221 escudo Incomum

**As suas peças** (o que a loja paga: 40% do valor; 20% a menos por peça igual que ela já tem, e por peça da mesma categoria além das que quer ter; a que está em uso não se vende sem guardar): i0658 Martelo de Ferord (Comum, 10/10) EM USO: 16 · i0659 Couro de Ferord (Comum, 10/10) EM USO: 7 · i0660 Elmo de Ferord (Comum, 10/10) EM USO: 1

Negociar não gasta bloco: `mercado.py comprar BEM N` · `mercado.py vender BEM N|tudo` · `mercado.py vender tudo` (a cesta: um troco só) · `mercado.py comprar ITEM` · `mercado.py vender ITEM` · `mercado.py preco BEM N` (só olha)

## A oficina
**Pedra Velha:** forja de vila (+1) · conserta, pago, até o Raro
Mão: forja Iniciante (61 blocos de bancada; Treinado aos 150)
Preparo (+2 cada, na obra que ele alcança): receita: até o Comum · ajudante: não há · fogo: até o Incomum · bigorna: até o Incomum
Matéria na carga: 3 de metal Comum, 2 de madeira Comum

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
- Filipa (pai/mãe): confia em você (+5) — é do meu sangue; Ferord pediu que eu lhe ensinasse o Incomum, e passou o dia comigo na bancada, até o limite das forças
- Berareu (parente): gosta de você (+2) — é do meu sangue

**O quadro de missões daqui** (`missoes.py toma MID`):
- m0003 · matar 3 lobos na Charneca dos Sinos · 19 de prata · prazo: Dia 9 · de Nora

**O ranking da semana 1** (fama e peças): 1. Drastum (340) · 2. Nynena (334) · 3. Taskin (324) · 4. Mirys (165) · 5. Ernesto (119) · você: 0

**Notícias que chegaram aqui** (as mais novas):
- Dia 4 (de Ribeira do Lobo): O Brasa, o dragão da serra, cobra de Ribeira do Lobo: quem não paga, arde
- Dia 3 (de Castro Real): salteadores na estrada de Castro Real a Coval do Vento: os mercadores andam em grupo
- Dia 1: salteadores na estrada de Pedra Velha a Souto Negro: os mercadores andam em grupo

## Perguntas abertas
1. O Dia 4 de Ferord (39 de prata; a forja em 61 de 150; a receita de Filipa em 7 de 10 blocos; acordou com cansaço 1)?  **a)** o ritmo de ontem: 3 blocos junto de Filipa (a jornada paga e 1 sem paga), come às 16h e dorme 3, das 20h às 8h: a receita do Incomum entra no fim do dia; acorda no Dia 5 sem cansaço · **b)** de manhã forja o escudo Comum com a matéria da carga (2 de madeira e 1 de metal, 1 bloco, 86%; o bloco conta como bancada junto de Filipa) e depois serve a jornada; come e dorme 3: a receita entra no fim do dia; acorda sem cansaço · **c)** 4 blocos (a jornada e 2 sem paga), come às 16h e dorme 2: a receita entra no 3º bloco, e o 4º o leva ao limite (cansaço 9: −2 em todo teste até dormir); acorda no Dia 5 com cansaço 3 · **d)** só a jornada, e a tarde na taverna, perguntando a Félix e a quem passa quem sabe feitiço por estas bandas (para gravar runas com quem sabe ao lado): a receita fica em 9 de 10
2. Com a receita na mão, para onde vai Ferord?  **a)** fica: a forja de Pedra Velha, a jornada e a prática, juntando os 77 de prata do martelo Incomum (só com a jornada, por volta do Dia 17) · **b)** Ribeira da Névoa: 3 blocos de estrada (de assalto às vezes), a forja de cidade e a mesa de runas, para ver e voltar; lá se paga a cama e a comida de lá, e são dias sem a jornada daqui · **c)** os lobos de Nora: pergunta na vila quem iria junto (Nora, que caça; Osorino, da guarda) e o que pedem, sem tomar ainda (19 de prata, até o Dia 9)

## SÓ O MESTRE
- nota: O Incomum de Filipa (regra de cena do Dia 2): Filipa ensina a Ferord a receita do Incomum em 10 blocos de bancada na forja de Pedra Velha, com ela ali (a jornada paga, a prática sem paga, a obra própria); bancada fora de Pedra Velha, ou sem Filipa na vila, não conta. A conta mora em marca.ensino_incomum (gente.json, eu) e no último evento do Mestre que a pôs: a cada dia de bancada com ela, estado.py mestre com ["pessoa","eu","marca.ensino_incomum","poe",TOTAL] e o texto do dia; ao chegar a 10: oficio.py preparo receita Incomum "Filipa ensinou na forja da casa". O que Ferord ouviu na taverna (Dia 1): Félix: Ribeira da Névoa (3 blocos) tem forja de cidade e mesa de runas, e Várzea da Névoa também; Vale do Corvo, a capital, tem a grande forja e a oficina de runas, e o mestre Simão (o mestre ferreiro, não de runas); ninguém que ele conheça vive de gravar runas. Erado: Pedra Velha foi saqueada nas guerras de 781, 869 e 957; Brarku, que fez forjar o Malho do Silêncio, morreu aqui em 1165. Só o Mestre: Ferord é Jeitoso na forja, sobe a Treinado aos 100 blocos (não aos 150 da MESA), e o talento aparece na MESA com a forja em 70; não dar à mesa prazo de Treinado pela conta de 150. Repor esta nota, uma só, depois de cada turno.py fecha, e rodar turno.py abre.
- a contagem na Charneca dos Sinos: corça 80/80 · lobo 12/12 · lobisomem 1/1 · acaso 1% por bloco
- talento e dom de Filipa: Lerdo em arcano
- talento e dom de Berareu: Jeitoso em fio, Prodígio em tiro, Jeitoso em caça, Jeitoso em manha, Lerdo em pacto
- talento e dom de Félix: Prodígio em peso, Jeitoso em forja, Lerdo em coleta, Lerdo em comércio
- talento e dom de Adelaide: Jeitoso em haste, Lerdo em peso, Lerdo em manha, Negado em fé, Jeitoso em verde
- talento e dom de Osorino: Jeitoso em caça, Lerdo em alquimia
- talento e dom de Nora: Lerdo em haste, Prodígio em tiro, Lerdo em caça, Prodígio em comércio, Negado em cura, Lerdo em alquimia, Jeitoso em encanto, Jeitoso em fé, Prodígio em pacto, Dom em tiro (escondido)
- talento e dom de Paio: Lerdo em coleta, Jeitoso em cura, Jeitoso em alquimia, Prodígio em manha, Jeitoso em fé
- talento e dom de Tânia: Negado em haste, Jeitoso em forja, Jeitoso em coleta, Negado em comércio, Jeitoso em manha, Lerdo em arcano
- talento e dom de Erado: Lerdo em tiro, Jeitoso em cura, Jeitoso em pacto
- talento e dom de Ferord: Prodígio em fio, Lerdo em peso, Jeitoso em tiro, Jeitoso em forja, Lerdo em cura, Jeitoso em alquimia, Jeitoso em arcano, Negado em pacto · inclinação do jogador: forja · segunda inclinação: encanto
- peça maldita: i0009 malho Raro (a praga da Mina da Névoa, Rara, insônia); quebra: devolver malho Raro ao lugar dela, no poço velho
- peça maldita: i0022 montante Comum (a praga da Toca do Sal, Comum, míngua); quebra: devolver montante Comum ao lugar dela, na sala dos presos
- a Fome da Serra (dragão ancião da serra, grau S) na câmara do tesouro: PV 1337 de 1337 · dorme até o Dia 421 (vigília 31, mais 2 por punhado; 0 tirados neste sono) · o tesouro: 1718 de prata; as peças: O Bordão da Serra · sem vila (caça no ermo) (`dragoes.py covil covil_dos_sinos_3`)
- o Brasa (dragão jovem da serra, grau C) nos Penhascos das Águas: PV 480 de 480 · dorme até o Dia 29 (vigília 29, mais 2 por punhado; 0 tirados neste sono) · o tesouro: 479 de prata; as peças: O Gume do Inverno · a vila: Ribeira do Lobo (1 ataque, o último no Dia 2) (`dragoes.py covil penhascos_das_aguas`)
- os salteadores nas estradas daqui: a estrada de Pedra Velha a Souto Negro: 4; a estrada de Castro do Sal a Pedra Velha: 1; a estrada de Pedra Velha a Várzea Brava: 2; a estrada de Ribeira da Névoa a Pedra Velha: 1
- as frentes: f01 o bando de Sara na estrada (passo 0) · f02 a horda da toca do Souto das Águas (passo 0) · f03 os mortos da Cripta dos Miraves (passo 0) · f04 o dragão Brasa (passo 0) · f05 a ambição dos Astolan (passo 0) · f06 o cartel de Selina (passo 0) · f07 o culto de Moninho (passo 0) · f08 a corrida da Liga do Sino Rachado (passo 0) · f09 a seca de Pedra Verde (passo 0) · f10 a falta de sal de Castro Branco (passo 0) · f11 os sumiços da Charneca dos Sinos (passo 0) · f12 as luzes das Ruínas do Urso (passo 0) · f13 Fome da Serra, o que dorme (passo 0)
- a pauta do diretor (o que pode entrar em cena hoje): os sumiços da Charneca dos Sinos (passo 0, a 1 estrada(s) daqui) · o bando de Sara na estrada (passo 0, a 2 estrada(s) daqui) · a ambição dos Astolan (passo 0, a 2 estrada(s) daqui)
- dois fatos que não tocam o personagem (para a cena): O Brasa, o dragão da serra, cobra de Ribeira do Lobo: quem não paga, arde · salteadores na estrada de Castro Real a Coval do Vento: os mercadores andam em grupo
- o estado está inteiro.
