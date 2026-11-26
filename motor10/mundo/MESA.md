# MESA · turno 15 · Dia 35, manhã (8h) · primavera

## Você
**Ferord**, nível 5 · PV 111/111 · 8 de prata · em Pedra Velha
Corpo: sem fome (fome 3) · sem sono (sono 1) · com forças (cansaço 0)
```
Ferord (nível 5, mão de Iniciante) · PV 111/111 · fôlego 11 · 2 ações (a mais: 1 pelo dobro do fôlego)
  Martelo Incomum de Ferord: acerto +5,75 · 1d10 × 3 (impacto), força × 1,18 · 3 de fôlego por golpe
  Defesa 32,5 · proteção: tronco 0,7 · braços 0,7 · pernas 0,7 · cabeça 1
```
Peças (`ato.py vestir ITEM` · `ato.py tirar ITEM`): i0659 Couro de Ferord (Comum, 10/10) · EM USO, no corpo · i0660 Elmo de Ferord (Comum, 10/10) · EM USO, na cabeça · i0677 Martelo Incomum de Ferord (Incomum, 20/20) · EM USO, na mão · o 19 também é crítico · i0682 Jogo de Forja de Ferord (Comum, 10/10) · ferramenta, na carga · +1 no teste do ofício dela · i0691 Martelo de Forja de Ferord (Incomum, 20/20) · ferramenta, na carga
Carga: 1 de metal Comum, 1 de madeira Comum
Treino: forja: 154 blocos (Treinado) · martelo: 40 blocos (Iniciante) · comércio: 5 dias de negócio (Leigo)
Com a forja você pega depressa (Jeitoso): o que os outros firmam em 375 blocos, você firma em 250.
Do povo dos humanos, 20 anos: a medida de todos.

## Aqui
**Pedra Velha** · comida no lugar: 12.171 · há cama
Quem está aqui: Filipa (o ferreiro; conserta e vende o que forja), Berareu (lavra a terra), Félix (da taverna; sabe de tudo o que se conta), Adelaide (aprende o ofício da casa), Osorino (da guarda de Pedra Velha), Nora (caça no ermo e vende o couro), Paio (cura ferida e colhe erva), Tânia (mercador; compra e vende, e leva carga pela estrada), Erado (o mais velho do lugar; sabe das histórias antigas)

**O que dá para fazer, e o que custa** (1 bloco = 4 horas):
- comer: 1 de prata, fome −3 (`ato.py comer`; da sua carga, sem pagar: `ato.py comer carga`)
- dormir: cama por 2 de prata, e a sua está paga até o Dia 35, noite (20h); cada bloco tira 3 de sono e de cansaço (no chão, 2) e devolve PV (`ato.py dormir N`)
- trabalhar (aprendiz): 3 de prata por bloco, esforço pesado; a jornada são 2 blocos pagos por dia (hoje: 0 de 2) (`ato.py trabalhar N`)
- treinar com uma arma: esforço pesado; a maestria sobe aos 40, 160, 500, 1.500 blocos (`ato.py treinar N ARMA`)
- descansar, esperar (`ato.py descansar N`, `ato.py esperar N`) · lutar (`ato.py luta nova CENARIO ARQ`) · testar (`teste.py`)

## O mercado
**Pedra Velha** · 360 de povo · a loja tem 1.719 de prata (sem prata, ela não compra) · comprar custa 10% a mais · a loja paga 60% do preço pelos bens e 40% do valor pelas peças (a sua mão em comércio: Leigo)

| bem | no lugar | preço do dia (× a base) | comprar | a loja paga | você carrega |
| --- | --- | --- | --- | --- | --- |
| comida | 12.171 | 1,33 (× 1,33) | 10 por 15 | 7 por 10 |  |
| lenha | 2.700 | 1,00 (× 1,00) | 10 por 12 | 5 por 10 |  |
| carvão | 219 | 1,99 (× 0,99) | 10 por 23 | 11 por 10 |  |
| sal | 215 | 3,01 (× 1,00) | 10 por 34 | 17 por 10 |  |
| pano | 115 | 4,85 (× 0,97) | 1 por 6 | 2 por 1 |  |
| remédio | 52 | 8,15 (× 1,02) | 1 por 10 | 4 por 1 |  |
| ferramenta | 51 | 12,35 (× 1,03) | 1 por 14 | 7 por 1 |  |
| metal Comum | 109 | 2,99 (× 1,00) | 10 por 34 | 17 por 10 | 1 |
| couro Comum | 110 | 1,98 (× 0,99) | 10 por 23 | 11 por 10 |  |
| osso Comum | 58 | 0,96 (× 0,96) | 10 por 12 | 5 por 10 |  |
| madeira Comum | 212 | 2,02 (× 1,01) | 10 por 23 | 11 por 10 | 1 |
| erva Comum | 103 | 2,05 (× 1,02) | 10 por 24 | 12 por 10 |  |
| metal Incomum | 14 | 20,41 (× 1,13) | 1 por 23 | 12 por 1 |  |
| couro Incomum | 18 | 12,00 (× 1,00) | 1 por 14 | 7 por 1 |  |
| osso Incomum | 14 | 4,81 (× 0,80) | 1 por 6 | 2 por 1 |  |
| madeira Incomum | 32 | 12,73 (× 1,06) | 1 por 15 | 7 por 1 |  |
| erva Incomum | 17 | 12,35 (× 1,03) | 1 por 14 | 7 por 1 |  |

**A magia** (as poções até a Rara; a água benta; a peçonha):
| bem | no lugar | preço do dia (× a base) | comprar | a loja paga | você carrega |
| --- | --- | --- | --- | --- | --- |
| antídoto Comum | 1 | 8,13 (× 1,35) | 1 por 13 | 3 por 1 |  |
| poção de Mana Comum | 1 | 6,00 (× 1,00) | 1 por 10 | 2 por 1 |  |
| poção de guarda Comum | 1 | 6,00 (× 1,00) | 1 por 10 | 2 por 1 |  |
| poção de fúria Comum | 1 | 6,00 (× 1,00) | 1 por 10 | 2 por 1 |  |
| água benta | 7 | 2,63 (× 0,88) | 7 por 36 | 12 por 10 |  |

**A prateleira** (peças do Livro de Itens; o preço é o de tabela, menos o desgaste; a arma vale pela matéria que leva, e a armadura pelo que cobre):
- novas, a 8 de prata cada (Comum): i0214 elmo de couro Comum · i0216 elmo de malha Comum
- novas, a 10 de prata cada (Comum): i0207 adaga Comum · i0222 amuleto Comum · i0223 amuleto Comum
- novas, a 30 de prata cada (Comum): i0208 espada Comum · i0209 maça Comum · i0210 machado Comum · i0211 lança Comum · i0212 arco Comum · i0213 armadura de couro Comum · i0215 armadura de malha Comum · i0217 escudo Comum · i0224 varinha Comum · i0225 símbolo Comum · i0226 Cartilha do arcano
- novas, a 180 de prata cada (Incomum): i0218 espada Incomum · i0219 lança Incomum · i0220 armadura de couro Incomum · i0221 escudo Incomum

**As suas peças** (o que a loja paga: 40% do valor; 20% a menos por peça igual que ela já tem, e por peça da mesma categoria além das que quer ter; a que está em uso não se vende sem guardar): i0659 Couro de Ferord (Comum, 10/10) EM USO: 7 · i0660 Elmo de Ferord (Comum, 10/10) EM USO: 1 · i0677 Martelo Incomum de Ferord (Incomum, 20/20) EM USO: 96

Negociar não gasta bloco: `mercado.py comprar BEM N` · `mercado.py vender BEM N|tudo` · `mercado.py vender tudo` (a cesta: um troco só) · `mercado.py comprar ITEM` · `mercado.py vender ITEM` · `mercado.py preco BEM N` (só olha)

## A oficina
**Pedra Velha:** forja de vila (+1) · conserta, pago, até o Raro
Mão: forja Treinado (154 blocos de bancada; Mestre aos 375 e uma obra Épica)
Preparo (+2 cada, na obra que ele alcança): receita: até o Incomum · ajudante: não há · fogo: até o Incomum · bigorna: até o Incomum
Ferramentas (somam na Lei do Valor): martelo de forja: i0691 Martelo de Forja de Ferord (Incomum), +4 · tenaz: i0682 Jogo de Forja de Ferord (Comum) (o jogo: martelo e tenaz), +1
Matéria na carga: 1 de metal Comum, 1 de madeira Comum

**Na bancada** (bloco pesado; `oficio.py pede ...` diz a matéria e a chance antes de abrir):
- forjar (a LEI DO VALOR: a soma decide a categoria): escolhe-se a peça e a matéria que entra; os blocos vêm da matéria (Comum 1, Incomum 3, Raro 9); do Épico para cima, a matéria Rara e um núcleo (Épico 27, Único 81, Lendário 243 blocos). A peça sai na maior categoria cuja CD a soma alcança (Comum 22 · Incomum 55 · Raro 80 · Épico 105 · Único 130 · Lendário 155), até o teto (sem núcleo, uma acima da matéria e nunca acima do Raro); abaixo da CD do Comum, a matéria se perde. `oficio.py pede ...` diz a chance de cada categoria.
- o conserto pago (`oficio.py consertar ITEM pago`): 2% do preço da peça por ponto, em prata inteira (arredonda para cima: um ponto de uma espada Comum custa 1 de prata), e um bloco de espera por peça (a cada 10 pontos ou parte): mandar consertar quatro peças leva quatro blocos
- ajustar (sob medida): grau 2; de 1 (Comum) a 6 blocos (Lendário) e um teste contra 22 + 6 por categoria
- jornal: 6 de prata por bloco de bancada a serviço da oficina (paga-se pelo que a mão vale: oficial), até a jornada (2 blocos pagos por dia; hoje: 0) (`oficio.py jornal N`)

## A caça e a coleta
- **a Charneca dos Sinos** (campo, borda), a 2 blocos [`charneca_dos_sinos`] · caça: corça (há fartura), lobo (é raro ver), lobisomem (há pouco, e sempre foi assim) · tira-se: erva Comum (há fartura), madeira Comum (há fartura)
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
- Filipa (pai/mãe): faria tudo por você (+7) — é do meu sangue; Ferord forjou na minha forja o primeiro martelo Incomum dele, e saiu dos bons; Ferord aprendeu comigo a receita do Incomum, em três dias de bancada
- Berareu (parente): gosta de você (+2) — é do meu sangue
- Adelaide: gosta de você (+3) — Ferord me deu o martelo da casa, o primeiro que ele usou na forja; Ferord me deu um jogo de forja, o martelo e a tenaz que ele mesmo fez
- Erado: gosta de você (+1) — Ferord quis ouvir de mim a história do Malho de Brarku

**O ranking da semana 5** (fama e peças): 1. Drastum (342) · 2. Nynena (340) · 3. Taskin (324) · 4. Mirys (164) · 5. Ernesto (119) · você: 5

**As frentes que você conhece** (pelos sinais; `frentes.py investigar FID`):
- f11 · alguém some na borda do mato em Souto Negro
- f05 · a casa junta aliados em Pedra Verde
- f01 · mais salteadores aparecem na estrada em Castro Real (barrada)
- f02 · o bando da toca cresce em Penha das Rosas
- f08 · a guilda junta gente em Penha das Rosas

**Notícias que chegaram aqui** (as mais novas):
- Dia 35 (de Castro Real): O bando de Sara na estrada acabou: o dono dela caiu.
- Dia 31 (de Pedra Verde): A casa junta prata em Pedra Verde
- Dia 31 (de Vale do Corvo): Isabel conta da história: no ano 1177, morre Domingas (de febre); Valinado assume a casa dos Astolan.
- Dia 31 (de Vale do Corvo): Josefa conta da história: no ano 851, aerine morre na Toca do Touro; o Arco do Rei Velho fica com o corpo.
- Dia 31 (de Castro Branco): Selelina conta da história: no ano 716, a velha atalaia que os bichos tomaram no ano 716, quando a guarda deixou de subir.
- Dia 30 (de Souto Negro): Acham um corpo sem sangue em Souto Negro (Irino morreu)

## Perguntas abertas
1. O que Ferord junta agora (8 de prata; a jornada de oficial deixa uns 9 por dia; com o martelo de forja Incomum, a obra de matéria Incomum sai Incomum 63%, Rara 5% e Comum 32%; a rotina segue até a prata e para no primeiro sinal)?  **a)** a tenaz Incomum: 1 de metal e 1 de madeira Incomum (38 hoje, uns 4 dias); completa o par: a tenaz vai de +1 a +3 · **b)** o escudo Incomum: 2 de madeira e 1 de metal Incomum (uns 53, uns 5 dias) · **c)** a malha Incomum no tronco: 2 de metal Incomum (uns 46, uns 5 dias)
2. (Fora do jogo) A parte 2: as habilidades de classe (batalhar, convencer, trabalhar, copiar) e os efeitos de itens do fraco ao apelão?  **a)** começar agora: o jogo para enquanto o Mestre constrói e prova · **b)** jogar mais uns turnos antes e construir depois

## SÓ O MESTRE
- nota: A forja segue a LEI DO VALOR desde o Dia 34 (REGRAS 7.3, 7.6, 7.14, 7.15; projeto/etapa_efeitos/LEI_DO_VALOR_juiz.txt): a categoria dita é a da obra (a matéria; o núcleo do Épico para cima); a peça sai na maior CD que a soma alcança (22, 55, 80, 105, 130, 155), até o teto; a porta do degrau (mão de Treinado para subir acima da matéria). As ferramentas de Ferord: o Martelo de Forja de Ferord (i0691, Incomum, +3) no lugar do martelo; o Jogo de Forja de Ferord (i0682, Comum, afinado) no lugar da tenaz (+1) e a afinada (+1). O que Ferord ouviu: Félix (Dia 1): as mesas de runas em Ribeira e Várzea da Névoa e a capital; o mestre Simão é o mestre ferreiro da capital. Erado (Dia 24): o Malho do Silêncio se perdeu nas Ruínas do Urso em 1210 (só o Mestre: no nível 3, Único). Félix (Dia 25): quem carrega as peças de nome. Só o Mestre, a crônica dos mestres ferreiros: Constança (Martelo da Aurora, Lendário, 493), Ninkel (Martelo do Rei Velho, Épico, 556), os anões da serra (Bordão da Serra, Mítico, 544), Borda (Gume do Inverno, Épico, 786), Urka (Martelo do Lobo, Lendário, 1049), Guiomar (Martelo da Fome, Épico, 1060); o Martelo do Rei Velho e o Martelo da Fome se perderam na Mina da Névoa. A frente f11 (o lobisomem da Charneca, centro em Souto Negro) está no passo 2. A rotina de vários dias roda pelo condutor do Mestre (cópia em saidas/rotina_condutor.py.txt). Repor esta nota, uma só, depois de cada turno.py fecha, e rodar turno.py abre.
- a contagem na Charneca dos Sinos: corça 71/80 · lobo 3/12 · lobisomem 1/1 · acaso 1% por bloco
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
- o Brasa (dragão jovem da serra, grau C) nos Penhascos das Águas: PV 480 de 480 · dorme até o Dia 63 (vigília 29, mais 2 por punhado; 0 tirados neste sono) · o tesouro: 497 de prata; as peças: O Gume do Inverno · a vila: Ribeira do Lobo (2 ataques, o último no Dia 29) (`dragoes.py covil penhascos_das_aguas`)
- os salteadores nas estradas daqui: a estrada de Pedra Velha a Souto Negro: 0; a estrada de Castro do Sal a Pedra Velha: 0; a estrada de Pedra Velha a Várzea Brava: 0; a estrada de Ribeira da Névoa a Pedra Velha: 0
- as frentes: f01 o bando de Sara na estrada (passo 2, barrada) · f02 a horda da toca do Souto das Águas (passo 2) · f03 os mortos da Cripta dos Miraves (passo 0) · f04 o dragão Brasa (passo 0) · f05 a ambição dos Astolan (passo 2) · f06 o cartel de Selina (passo 1) · f07 o culto de Moninho (passo 1) · f08 a corrida da Liga do Sino Rachado (passo 1) · f09 a seca de Pedra Verde (passo 1) · f10 a falta de sal de Castro Branco (passo 1) · f11 os sumiços da Charneca dos Sinos (passo 2) · f12 as luzes das Ruínas do Urso (passo 0) · f13 Fome da Serra, o que dorme (passo 0)
- a pauta do diretor (o que pode entrar em cena hoje): os sumiços da Charneca dos Sinos (passo 2, a 1 estrada(s) daqui, andou nesta semana) · a ambição dos Astolan (passo 2, a 2 estrada(s) daqui, andou nesta semana) · o cartel de Selina (passo 1, a 2 estrada(s) daqui)
- dois fatos que não tocam o personagem (para a cena): O bando de Sara na estrada acabou: o dono dela caiu. · Taskin cumpriu a missão de Souto Negro: matar 3 lobos na Charneca dos Sinos
- o estado está inteiro.
