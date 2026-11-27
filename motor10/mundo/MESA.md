# MESA · turno 19 · Dia 53, manhã (8h) · primavera

## Você
**Ferord**, nível 5 · PV 111/111 · 67 de prata · em Pedra Velha
Corpo: sem fome (fome 3) · sem sono (sono 1) · com forças (cansaço 0)
```
Ferord (nível 5, mão de Iniciante) · PV 111/111 · fôlego 11 · 2 ações (a mais: 1 pelo dobro do fôlego)
  Martelo Incomum de Ferord: acerto +5,75 · 1d10 × 3 (impacto), força × 1,18 · 3 de fôlego por golpe
  Defesa 32,5 · proteção: tronco 0,7 · braços 0,7 · pernas 0,7 · cabeça 1
```
Peças (`ato.py vestir ITEM` · `ato.py tirar ITEM`): i0659 Couro de Ferord (Comum, 10/10) · EM USO, no corpo · i0660 Elmo de Ferord (Comum, 10/10) · EM USO, na cabeça · i0677 Martelo Incomum de Ferord (Incomum, 20/20) · EM USO, na mão · o crítico é 19/11 (o de antes: o que nasceu, nasceu) · i0682 Jogo de Forja de Ferord (Comum, 10/10) · ferramenta, na carga · afinada · i0691 Martelo de Forja de Ferord (Incomum, 20/20) · ferramenta, na carga · i0701 Tenaz de Ferord (Comum, 10/10) · ferramenta, na carga · afinada · i0713 Segunda Tenaz de Ferord (Incomum, 20/20) · ferramenta, na carga
Carga: 1 de metal Comum, 1 de madeira Comum
Treino: forja: 194 blocos (Treinado) · martelo: 51 blocos (Iniciante) · comércio: 7 dias de negócio (Leigo)
Com a forja você pega depressa (Jeitoso): o que os outros firmam em 375 blocos, você firma em 250.
Do povo dos humanos, 20 anos: a medida de todos.

## Aqui
**Pedra Velha** · comida no lugar: 10.194 · há cama
Quem está aqui: Filipa (o ferreiro; conserta e vende o que forja), Berareu (lavra a terra), Félix (da taverna; sabe de tudo o que se conta), Adelaide (aprende o ofício da casa), Osorino (da guarda de Pedra Velha), Nora (caça no ermo e vende o couro), Paio (cura ferida e colhe erva), Tânia (mercador; compra e vende, e leva carga pela estrada), Erado (o mais velho do lugar; sabe das histórias antigas)

**O que dá para fazer, e o que custa** (1 bloco = 4 horas):
- comer: 1 de prata, fome −3 (`ato.py comer`; da sua carga, sem pagar: `ato.py comer carga`)
- dormir: cama por 2 de prata, e a sua está paga até o Dia 53, noite (20h); cada bloco tira 3 de sono e de cansaço (no chão, 2) e devolve PV (`ato.py dormir N`)
- trabalhar (aprendiz): 3 de prata por bloco, esforço pesado; a jornada são 2 blocos pagos por dia (hoje: 0 de 2) (`ato.py trabalhar N`)
- treinar com uma arma: esforço pesado; a maestria sobe aos 40, 160, 500, 1.500 blocos (`ato.py treinar N ARMA`)
- descansar, esperar (`ato.py descansar N`, `ato.py esperar N`) · lutar (`ato.py luta nova CENARIO ARQ`) · testar (`teste.py`)

## O mercado
**Pedra Velha** · 360 de povo · a loja tem 1.601 de prata (sem prata, ela não compra) · comprar custa 10% a mais · a loja paga 60% do preço pelos bens e 40% do valor pelas peças (a sua mão em comércio: Leigo)

| bem | no lugar | preço do dia (× a base) | comprar | a loja paga | você carrega |
| --- | --- | --- | --- | --- | --- |
| comida | 10.194 | 1,46 (× 1,46) | 10 por 17 | 8 por 10 |  |
| lenha | 2.700 | 1,00 (× 1,00) | 10 por 12 | 5 por 10 |  |
| carvão | 217 | 2,00 (× 1,00) | 10 por 23 | 11 por 10 |  |
| sal | 215 | 3,01 (× 1,00) | 10 por 34 | 17 por 10 |  |
| pano | 111 | 4,93 (× 0,99) | 1 por 6 | 2 por 1 |  |
| remédio | 57 | 7,79 (× 0,97) | 1 por 9 | 4 por 1 |  |
| ferramenta | 55 | 11,89 (× 0,99) | 1 por 14 | 7 por 1 |  |
| metal Comum | 104 | 3,06 (× 1,02) | 10 por 35 | 17 por 10 | 1 |
| couro Comum | 117 | 1,92 (× 0,96) | 10 por 22 | 11 por 10 |  |
| osso Comum | 56 | 0,98 (× 0,98) | 10 por 12 | 5 por 10 |  |
| madeira Comum | 215 | 2,00 (× 1,00) | 10 por 23 | 11 por 10 | 1 |
| erva Comum | 103 | 2,05 (× 1,02) | 10 por 24 | 12 por 10 |  |
| metal Incomum | 14 | 20,41 (× 1,13) | 1 por 23 | 12 por 1 |  |
| couro Incomum | 18 | 12,00 (× 1,00) | 1 por 14 | 7 por 1 |  |
| osso Incomum | 16 | 4,50 (× 0,75) | 1 por 6 | 2 por 1 |  |
| madeira Incomum | 31 | 12,93 (× 1,08) | 1 por 15 | 7 por 1 |  |
| erva Incomum | 13 | 14,12 (× 1,18) | 1 por 16 | 8 por 1 |  |

**A magia** (as poções até a Rara; a água benta; a peçonha):
| bem | no lugar | preço do dia (× a base) | comprar | a loja paga | você carrega |
| --- | --- | --- | --- | --- | --- |
| poção de Mana Comum | 1 | 6,00 (× 1,00) | 1 por 10 | 2 por 1 |  |
| poção de guarda Comum | 1 | 6,00 (× 1,00) | 1 por 10 | 2 por 1 |  |
| poção de fúria Comum | 1 | 6,00 (× 1,00) | 1 por 10 | 2 por 1 |  |
| água benta | 7 | 2,63 (× 0,88) | 7 por 36 | 12 por 10 |  |

**A prateleira** (peças do Livro de Itens; o preço é o de tabela, menos o desgaste; a arma vale pela matéria que leva, e a armadura pelo que cobre). A loja está farta: tem 1 peça Comum além das 16 que ela quer ter:
- novas, a 8 de prata cada (Comum): i0214 elmo de couro Comum · i0216 elmo de malha Comum
- novas, a 10 de prata cada (Comum): i0207 adaga Comum · i0222 amuleto Comum · i0223 amuleto Comum
- novas, a 30 de prata cada (Comum): i0208 espada Comum · i0209 maça Comum · i0210 machado Comum · i0211 lança Comum · i0212 arco Comum · i0213 armadura de couro Comum · i0215 armadura de malha Comum · i0217 escudo Comum · i0224 varinha Comum · i0225 símbolo Comum · i0226 Cartilha do arcano · i0711 machado Comum
- novas, a 180 de prata cada (Incomum): i0218 espada Incomum · i0219 lança Incomum · i0220 armadura de couro Incomum · i0221 escudo Incomum

**As suas peças** (o que a loja paga: 40% do valor; 20% a menos por peça igual que ela já tem, e por peça da mesma categoria além das que quer ter; a que está em uso não se vende sem guardar): i0659 Couro de Ferord (Comum, 10/10) EM USO: 6 · i0660 Elmo de Ferord (Comum, 10/10) EM USO: 1 · i0677 Martelo Incomum de Ferord (Incomum, 20/20) EM USO: 96

Negociar não gasta bloco: `mercado.py comprar BEM N` · `mercado.py vender BEM N|tudo` · `mercado.py vender tudo` (a cesta: um troco só) · `mercado.py comprar ITEM` · `mercado.py vender ITEM` · `mercado.py preco BEM N` (só olha)

## A oficina
**Pedra Velha:** forja de vila (+1) · conserta, pago, até o Raro
Mão: forja Treinado (194 blocos de bancada; Mestre aos 375 e uma obra Épica)
Preparo (+2 cada, na obra que ele alcança): receita: até o Incomum · ajudante: não há · fogo: até o Incomum · bigorna: até o Incomum
Ferramentas (somam na Lei do Valor): martelo de forja: i0691 Martelo de Forja de Ferord (Incomum), +3 · tenaz: i0713 Segunda Tenaz de Ferord (Incomum), +3
A sua receita (a ferramenta que nasce com efeitos escolhe por ela, na hora): tenaz: prumo, afinada, fagulha
Matéria na carga: 1 de metal Comum, 1 de madeira Comum

**Na bancada** (bloco pesado; `oficio.py pede ...` diz a matéria e a chance antes de abrir):
- forjar (a LEI DO VALOR: a soma decide a categoria): escolhe-se a peça e a matéria que entra; os blocos vêm da matéria (Comum 1, Incomum 3, Raro 9); do Épico para cima, a matéria Rara e um núcleo (Épico 27, Único 81, Lendário 243 blocos). A peça sai na maior categoria cuja CD a soma alcança (Comum 22 · Incomum 55 · Raro 80 · Épico 105 · Único 130 · Lendário 155), até o teto (sem núcleo, uma acima da matéria e nunca acima do Raro); abaixo da CD do Comum, a matéria se perde. `oficio.py pede ...` diz a chance de cada categoria.
- o conserto pago (`oficio.py consertar ITEM pago`): 2% do preço da peça por ponto, em prata inteira (arredonda para cima: um ponto de uma espada Comum custa 1 de prata), e um bloco de espera por peça (a cada 10 pontos ou parte): mandar consertar quatro peças leva quatro blocos
- ajustar (sob medida): grau 2; de 1 (Comum) a 6 blocos (Lendário) e um teste contra 22 + 6 por categoria
- jornal: 6 de prata por bloco de bancada a serviço da oficina (paga-se pelo que a mão vale: oficial), até a jornada (2 blocos pagos por dia; hoje: 0) (`oficio.py jornal N`)

## A caça e a coleta
- **a Charneca dos Sinos** (campo, borda), a 2 blocos [`charneca_dos_sinos`] · caça: corça (há fartura), lobo (sumiu), lobisomem (há pouco, e sempre foi assim) · tira-se: erva Comum (há fartura), madeira Comum (há fartura)
- A sua mão: caça Leigo (0 blocos), coleta Leigo (0 blocos). O rastro: 2d20 + 4 contra 20 ou mais (o bicho arisco e o que rareou pedem mais; de noite, −4). A coleta: 2d20 + 6 (minério, madeira) ou + 4 (erva) contra 20, mais 8 por categoria, e o que rareou pede mais; o bloco que passa rende 1 de minério, 2 de madeira ou 1 de erva, e o que falha não rende.
- `caca.py sair [ERMO] [alvo=ESPECIE] [blocos=N]` (ida, N de procura, volta; N de 1 a 6, 2 se não disser) · `caca.py coletar BEM [ERMO] [blocos=N]` (N de 1 a 4)

## Os bichos daqui (o que todo mundo sabe; a frase inteira: `bichos.py ameaca ESPECIE`)
- corça (grau F, Comum, média, de 1 a 2) · lobisomem (grau C, Raro, médio, sozinho: regenera, amaldiçoa, noturno)

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

**O ranking da semana 8** (fama e peças): 1. Drastum (350) · 2. Taskin (326) · 3. Nynena (324) · 4. Mirys (164) · 5. Ernesto (119) · você: 5

**As frentes que você conhece** (pelos sinais; `frentes.py investigar FID`):
- f09 · o rio baixa em Pedra Verde
- f10 · o sal some da feira em Castro Branco
- f08 · a guilda junta gente em Penha das Rosas
- f04 · o dragão é visto sobre o lugar em Ribeira do Lobo
- f11 · alguém some na borda do mato em Souto Negro · o relógio: passo 2 de 6

**Notícias que chegaram aqui** (as mais novas):
- Dia 52 (de Pedra Verde): O celeiro baixa em Pedra Verde
- Dia 52 (de Castro Branco): O mercador de sal não vem mais em Castro Branco
- Dia 52 (de Vale do Corvo): Isabel conta da história: no ano 680, morre Rosanada (caçando na serra); Alelia assume a casa dos Orirena.
- Dia 52 (de Castro Real): Boskul conta da história: no ano 710, acaba a guerra do Inverno Longo: vencem os Orirena.
- Dia 51 (de Souto Negro): Vicente conta da história: no ano 577, morre Clara (à traição, por um parente); Zélia assume a casa dos Astasal.
- Dia 50: Erado conta da história: no ano 710, acaba a guerra do Inverno Longo: vencem os Orirena.

## Perguntas abertas
1. Ferord tem 67 de prata guardados para o feito do Mestre (um núcleo Épico, que não se acha à venda aqui). A forja está em 194 blocos (Mestre aos 250 e uma obra Épica). O que faz com a prata?  **a)** segue guardando (a rotina: 2 blocos pagos de forja e 1 de martelo por dia) · **b)** forja agora o elmo de malha Incomum (1 de metal Incomum, uns 22): troca o elmo de couro; nasce com os efeitos de luta pela faixa (Couraça, Firme, Robusta...) · **c)** junta mais uns 3 dias e forja a armadura de malha Incomum (4 de metal Incomum, uns 90)
2. Pela vila: não há guilda de ferreiros que alguém daqui conheça; o único mestre de forja de nome é Simão, na grande forja de Vale do Corvo (a capital, 4 blocos de estrada por Castro do Sal, de assalto às vezes). As guildas que se conhecem são de aventureiros: a Liga do Sino Rachado (de Taskin), a Ordem da Raposa e a Mesa do Corvo Branco, na capital; a Guarda das Sete Pedras (de Mirys), em Ribeira da Névoa; a Irmandade da Estrada, em Várzea da Névoa. E agora?  **a)** fica em Pedra Velha · **b)** vai a Vale do Corvo: conhecer Simão e a grande forja (lá a forja soma +3, não +1) e oferecer peças às guildas · **c)** investiga Souto Negro de novo (1 bloco: 2d20 + 4 contra 26)

## SÓ O MESTRE
- nota: A forja segue a LEI DO VALOR desde o Dia 34 (REGRAS 7.3, 7.6, 7.14, 7.15; projeto/etapa_efeitos/LEI_DO_VALOR_juiz.txt) e, desde o Dia 37, a FAIXA da parte 2 (fase 1a; REGRAS 7.3: faltou 17 ou mais para a CD de cima, 0 efeito; 9 a 16, 1; 6 a 8, 2; 3 a 5, 3; 1 ou 2, 4; na categoria do teto, até 2; teto de efeitos 2/4/4/5/5/6/6/7, e a sobra vira cheio; os 12 efeitos de ferramenta, 7.14; só a ferramenta escolhe efeito até a fase 1b): a categoria dita é a da obra (a matéria; o núcleo do Épico para cima); a peça sai na maior CD que a soma alcança (22, 55, 80, 105, 130, 155), até o teto; a porta do degrau (mão de Treinado para subir acima da matéria). As ferramentas de Ferord: o Martelo de Forja de Ferord (i0691, Incomum, +3) no lugar do martelo; a Segunda Tenaz de Ferord (i0713, Incomum, sem efeito; nasceu no Dia 45, soma 58) no lugar da tenaz (+3): a soma da forja é 2d20 + 39; de reserva, a Tenaz de Ferord (i0701, Comum, afinada; Dia 39, soma 43) e o Jogo de Forja de Ferord (i0682, Comum, afinado) (a loja não negocia ferramenta). A receita dele: tenaz, prumo, afinada, fagulha. O que Ferord ouviu: Félix (Dia 1): as mesas de runas em Ribeira e Várzea da Névoa e a capital; o mestre Simão é o mestre ferreiro da capital. Erado (Dia 24): o Malho do Silêncio se perdeu nas Ruínas do Urso em 1210 (só o Mestre: no nível 3, Único). Félix (Dia 25): quem carrega as peças de nome. Pela vila (Dia 46): não há guilda de ferreiros que alguém daqui conheça; o único mestre de forja de nome é Simão, na grande forja de Vale do Corvo (no mundo, o único vivo com forja de Mestre); as guildas que se conhecem são de aventureiros (a Liga do Sino Rachado de Taskin, a Ordem da Raposa e a Mesa do Corvo Branco, na capital; a Guarda das Sete Pedras de Mirys, em Ribeira da Névoa; a Irmandade da Estrada, em Várzea da Névoa; a Companhia do Lobo Cinzento, pequena, ninguém daqui conhece). Só o Mestre, a crônica dos mestres ferreiros: Constança (Martelo da Aurora, Lendário, 493), Ninkel (Martelo do Rei Velho, Épico, 556), os anões da serra (Bordão da Serra, Mítico, 544), Borda (Gume do Inverno, Épico, 786), Urka (Martelo do Lobo, Lendário, 1049), Guiomar (Martelo da Fome, Épico, 1060); o Martelo do Rei Velho e o Martelo da Fome se perderam na Mina da Névoa. A frente f11 (o lobisomem da Charneca, centro em Souto Negro) está no passo 3 (Dia 36: mais um some de dentro de casa; a notícia chegou a Pedra Velha no Dia 37); Ferord sabe o relógio dela (investigou no Dia 37, 29 contra 26; o frentes.sabe cortava a chave pelo ponto e foi consertado nesse dia); a segunda investigação, no Dia 40, falhou (23 contra 26). A parte 2: o contrato é projeto/etapa_efeitos/DESENHO.md (as respostas do jogador em 12.1; as decisões do Mestre em 12.3); as fases 1a e 1b estão no motor (a faixa da forja, os efeitos de ferramenta e de luta; o martelo de Ferord fica com o critico_19); a fase 2 (as habilidades e a fala) está em construção numa cópia, /home/user/ferir-2 (ramo local fase-2, de b431264), a juntar depois da revisão, com o estado.py entrada 2. A rotina de vários dias roda pelo condutor do Mestre (cópia em saidas/rotina_condutor.py.txt); desde o Dia 40 (o jogador: "melhorar habilidade enquanto isso"), o condutor com treino (saidas/rotina_treino_condutor.py.txt): 2 blocos pagos de forja e o terceiro bloco do dia no treino do martelo. Repor esta nota, uma só, depois de cada turno.py fecha, e rodar turno.py abre.
- a contagem na Charneca dos Sinos: corça 62/80 · lobo 0/12 · lobisomem 1/1 · acaso 0% por bloco
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
- as frentes: f01 o bando de Sara na estrada (passo 2, barrada) · f02 a horda da toca do Souto das Águas (passo 2) · f03 os mortos da Cripta dos Miraves (passo 0) · f04 o dragão Brasa (passo 1) · f05 a ambição dos Astolan (passo 2) · f06 o cartel de Selina (passo 1) · f07 o culto de Moninho (passo 1) · f08 a corrida da Liga do Sino Rachado (passo 2) · f09 a seca de Pedra Verde (passo 3) · f10 a falta de sal de Castro Branco (passo 3) · f11 os sumiços da Charneca dos Sinos (passo 2) · f12 as luzes das Ruínas do Urso (passo 0) · f13 Fome da Serra, o que dorme (passo 0)
- a pauta do diretor (o que pode entrar em cena hoje): a seca de Pedra Verde (passo 3, a 2 estrada(s) daqui, andou nesta semana) · a falta de sal de Castro Branco (passo 3, a 2 estrada(s) daqui, andou nesta semana) · os sumiços da Charneca dos Sinos (passo 2, a 1 estrada(s) daqui)
- dois fatos que não tocam o personagem (para a cena): O celeiro baixa em Pedra Verde · O mercador de sal não vem mais em Castro Branco
- o estado está inteiro.
