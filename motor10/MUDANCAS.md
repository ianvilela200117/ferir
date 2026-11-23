# MOTOR 10 — diário de mudanças

O livro de regras (`REGRAS.md`) não guarda história. Ela fica aqui: o que mudou, quando, por quê, e o que o banco de provas deu.

## Dia 507 (fora do jogo) — nasce o Motor 10
- **Por quê:** a revisão do motor (`../REVISAO_MOTOR10.md`) mediu que no motor antigo o nível vencia a arma. O jogador pediu: a arma decidir muito (uma arma dar chance de um nível 50 vencer um nível 500), fim do requisito por nível, o sob medida misturado com requisito por atributo, a luta parar e perguntar sempre que algo muda, e todos os módulos de combate.
- **O que entrou:** `tabelas.py` (todos os números), `itens.py` (o Livro de Itens e a janela do item), `pessoas.py` (a ficha que sai sozinha; requisito por atributo, sob medida, sintonia), `luta.py` (grupo contra grupo numa linha de casas; alcance, lugar, tempo, fôlego, golpe contra armadura, parte do corpo e ferida, durabilidade, moral, ordens e paradas), `provas.py` (o banco de provas).
- **A escala:** começou com a proteção SUBTRAINDO do golpe. O banco de provas reprovou: entre iguais de categoria alta a luta acabava em uma rodada. Passou a DIVIDIR: o que conta é a diferença de categoria entre a arma e a armadura, e o duelo entre iguais dura o mesmo em qualquer degrau.
- **Metas afrouxadas na calibração** (para o jogador confirmar): "só a arma uma categoria acima, mesmo nível" era 65 a 90% e ficou 80 a 99% (mede 93%); "mesma arma, nível 150 contra 50" era 80 a 98% e ficou 85 a 100% (mede 96%).
- **Banco de provas:** 28 de 28.
- **Falta:** a magia e os encantos de peça, os bichos, o ofício (forjar, consertar, a escada das categorias), o mundo vivo, o turno em dois comandos.

## Dia 507 (fora do jogo) — a arma mais forte ainda
- **Por quê:** o jogador viu o primeiro dial (uma arma duas categorias acima dava ao nível 50 28% contra o nível 500; três acima, 76%) e pediu "mais forte ainda". Também decidiu: **mundo novo, do zero** (o save do Ferir fica guardado como está).
- **O que mudou no `tabelas.py`:** cada categoria passou a valer o TRIPLO da de baixo (era 2,5 vezes); o bônus de acerto e de Defesa passou a +4 por categoria (era +3); a força do golpe passou a 0,03 por ponto de bônus (era 0,04); o PV passou a Vigor × 2 + nível ÷ 4 (era nível ÷ 2).
- **O que o banco mede agora:** uma arma UMA acima vence 100 níveis de diferença em 70% e dá 6% contra 450 níveis; DUAS acima dão ao nível 50 **59%** contra o nível 500; TRÊS acima, **86%**. Com a mesma arma, o nível 150 vence o 50 em 95% e o 75 vence o 50 em 52%.
- **Metas que mudaram** (seguem o pedido): as faixas das provas de arma subiram; entrou a prova "uma arma uma acima, 50 × 500" (2 a 20%). Duas provas de módulo foram afrouxadas por serem ruidosas: o alcance (as lanças têm de vencer nas duas situações, sem exigir diferença entre corredor e campo) e a moral (40% em vez de 50%).
- **Banco de provas:** 29 de 29.

## Dia 507 (fora do jogo) — a revisão do núcleo e os consertos
- **Por quê:** uma revisão adversarial do núcleo (três leitores independentes: regra contra código, a luta jogada de verdade, o equilíbrio) achou 30 defeitos. Os que valiam foram consertados antes de qualquer Dia 1.
- **O nível entrava escondido pelas ações.** A maestria típica dava 2, 3 ou 4 ações, e o nível 49 → 50 valia mais que cem níveis. Agora **todo mundo tem 2 ações**; a terceira (o esforço) é só para golpear e custa o dobro do fôlego (Mestre: o normal; Lendário: mais uma). As provas de nível medem também 40 e 60, e uma prova mede o nível com a maestria igual.
- **A luta para no MEIO da rodada.** O script roda turno a turno; a parada vem logo depois do turno em que algo mudou, antes dos turnos que faltam.
- **Quem o jogador comanda não foge nem se rende pelo dado:** fraqueja (abalado), a luta para e ele escolhe.
- **A iniciativa é rolada a cada rodada** (com a armadura: couro +2, placa −2).
- **Grupo contra grupo de verdade:** o cerco (4 de perto mais 2 de haste por alvo, por rodada), o flanco (−3 na Defesa por atacante que já bateu, até −9), o contorno (quem sobra passa pela linha que os outros seguram), a troca de lugar no corredor, o guarda sem caminho que luta como soldado, o impasse (8 rodadas sem dano de verdade).
- **O que apara:** o escudo dá 4 + o bônus da categoria; a arma dá o bônus da dela; vale o maior. Uma arma boa também defende. O duelo entre iguais passou a durar o mesmo em qualquer categoria (4 rodadas no Raro e no Lendário; antes, 4 e 2).
- **Mirar a fresta** (nova): contra armadura melhor que a arma, −8 no acerto e a armadura conta uma categoria abaixo. O script mira quando compensa. Sem isso, só a armadura duas acima vencia mais que só a arma (72% contra 59%) e a luta se arrastava por 28 rodadas.
- **As armaduras ganharam ofício:** couro 0,7 do valor, +3 na Defesa, +2 na iniciativa; placa 1,4 do valor, −2 e −2, 1 de fôlego por rodada. O corte contra a malha passou a 1,1 e contra a placa a 1,3. A espada e o montante aparam (+2). A arma de alcance 2 tem −2 contra quem está colado. O arco e a besta não ganham o 1,25 das duas mãos; atirar depois de recuar tem −4.
- **A ferida e o sangue:** o crítico só abre ferida se tirar 5% do PV; o sangue é um quinto do golpe que abriu a ferida, e estanca (3 rodadas; 5 se grave). Antes, um arranhão de crítico sangrava até a morte.
- **A durabilidade:** a arma já não gasta a cada golpe em armadura melhor (isso quebrava a arma do nível alto e era o que fazia a armadura vencer). Gasta quando é aparada por aço melhor, quando o golpe não passa, e em dois 1. Toda peça usada perde 1 no fim da luta. O escudo gasta. A peça quebrada perde aparo e efeitos. As mãos não quebram. A durabilidade volta ao Livro de Itens a cada vez que a luta é guardada.
- **A sintonia** conta todas as peças Épicas ou melhores (não só as de efeito desperto); a que dorme rende uma categoria abaixo e perde os efeitos. Efeito na peça errada é recusado; o "devolve" tem teto pela categoria.
- **Entrada conferida:** o cenário (nomes repetidos, tempo, lugar, linha, moral, guarda) e as ordens (nome, ação, alvo) são conferidos antes de qualquer dado; o erro vem com a lista do que vale. O cenário aceita elmo e lista de peças; o quadro avisa a parte do corpo sem proteção.
- **O fim da luta:** quando os dois lados caem, ninguém vence; os caídos de quem ficou com o campo são estancados, os outros rolam até o fim.
- **Números que mudaram no `tabelas.py`:** o tamanho do golpe 4,5 → 4; a Defesa de base 24 → 22; a gente gerada nasce com atributos menores (Força 70), para o requisito morder nos níveis baixos.
- **Metas que mudaram** (para o jogador confirmar):
  - "um nível 120 de Lendário × dez de nível 60 de Único" era 0 a 25% (media 2%) e ficou **15 a 60% (mede 51%)**. É a consequência do cerco: antes os dez batiam todos de uma vez. Hoje, contra dez, uma categoria de vantagem é moeda no ar; na mesma categoria os dez vencem sempre; duas acima, o um vence sempre.
  - "só a arma duas acima, 50 × 500" subiu de 59% para **63%**; três acima, de 86% para **93%**.
  - "mesma arma, nível 150 contra 50" caiu de 95% para 88% (a faixa passou a 80 a 100%).
  - a prova de moral (alguém foge ou se rende) passou de 40% para 30% de piso, por ser ruidosa.
- **Metas novas:** o nível 40 e o 60; o nível com a maestria igual; só a armadura (três provas); a fantasia (um nível 50 de conjunto Lendário × dez de nível 275 de Raro: 92%); as armas entre si (nenhuma montagem abaixo de 35% nem acima de 65%); a duração da luta em que o aço não passa; e onze provas de módulo a mais.
- **A retirada** (nova): quem tem ordem de recuar e acaba a rodada a 8 casas de todo inimigo de pé saiu da luta.
- **Teste de estresse:** 2.500 lutas montadas ao acaso (1 a 6 contra 1 a 8, todas as armas e categorias, corredores, tempo, guardas, ordens ao acaso, o estado indo ao arquivo e voltando), sem erro e sem quebrar nenhuma destas garantias: ninguém de pé com PV zero, o comandado nunca foge pelo dado, o corredor nunca tem mais gente que a largura, a durabilidade nunca sai da faixa, todo caído tem destino no fim.
- **Banco de provas:** 51 de 51.
- **O que ficou para os módulos seguintes:** a ferida que dura depois da luta (pede o estado das pessoas), a morte do personagem do jogador (decisão dele), a magia, os bichos, o ofício.

## Dia 507 (fora do jogo) — o projeto do resto, e a etapa 1 do mundo
- **`PROJETO.md`:** três projetos inteiros do mundo vivo (gente primeiro, sistemas primeiro, drama primeiro) foram escritos e julgados. Ficou: os sistemas como chão, as frentes como enredo, a memória dos nomeados como rosto. O plano tem a escada das peças em números, o banco de provas do mundo, sete etapas até o Dia 1 e seis decisões que são do jogador. Os rascunhos ficam em `projeto/`.
- **Etapa 1, "um dia numa vila"** (não depende de nenhuma das seis decisões): `tabelas_mundo.py` (os números do mundo), `estado.py` (o estado e o único gravador, com os invariantes), `corpo.py` (fome, sono, cansaço, a ferida que dura), `ato.py` (comer, dormir, trabalhar, treinar, descansar, esperar, e a luta dentro do mundo), `teste.py` (o dado declarado e rolado uma vez), `turno.py` (`abre`, `pergunta`, `responde`, `nota`, `fecha`), `provas_mundo.py`.
- **Na luta:** a ficha aceita maestria por arma, a pena do corpo, o fôlego que o cansaço tira e as feridas que a pessoa já traz. A luta do mundo não grava no Livro de Itens: a durabilidade volta por evento.
- **Banco de provas do mundo:** 12 de 12 (a rotina de 30 dias se sustenta e sobra 1 de prata por dia; quem não dorme para e leva −4; seis dias sem comer tiram um quinto do PV; a ferida sara em 7 dias de repouso e a grave em 21, e não sara com trabalho pesado; nove eventos errados são recusados sem mudar nada; seis estragos plantados são achados; o homem moído vence a si mesmo descansado em 23%; a luta volta ao estado num evento só; cinco fechamentos errados são recusados). **Banco da luta:** segue 51 de 51.
- **Falta na etapa 1, de propósito:** o corpo dos outros (entra com os nomeados, na etapa 3) e a morte do personagem (é a decisão 1 do jogador).

## Etapa 2 (fora do jogo) — viver de um ofício: os bichos, o ofício, o mercado, a caça; a revisão e a integração
- **Por quê:** a etapa 2 do `PROJETO.md`. Quatro construtores escreveram um módulo cada um, pelo contrato `projeto/ETAPA2.md`; três revisores (o gravador único, o equilíbrio, a mesa jogada) trouxeram mais de trinta achados; a integração consertou, juntou o livro e fez a vila de teste.
- **O que entrou:**
  - **os bichos** (`bichos.py`, `tabelas_bichos.py`, o bloco OS BICHOS do `provas.py`): 14 espécies do grau F ao S, o corpo como arma e armadura com categoria, 4 tamanhos, 10 traços que a luta roda, a moral do bicho, o despojo e o núcleo do chefe, a ameaça lida antes;
  - **o ofício** (`oficio.py`, `tabelas_oficio.py`, `provas_oficio.py`): a obra de vários dias, o teste final, falhar custa, o preparo, a maestria por blocos de bancada, consertar, ajustar, o jornal;
  - **o mercado** (`mercado.py`, `tabelas_mercado.py`, `provas_mercado.py`): o preço que sai do estoque, a prata contada, as peças da loja, a virada do dia, o ano da comida, a mão de comércio;
  - **a caça e a coleta** (`caca.py`, `tabelas_caca.py`, `provas_caca.py`): o ermo contado, o rastro, o encontro, a posição, a luta do `ato.py`, o despojo, a presa ferida, a coleta, a virada;
  - **a vila de teste** (`vila_teste.py`, `GUIA_VILA.md`), fora do cânone;
  - **o livro:** os capítulos 6 a 9 do `REGRAS.md`.
- **O que os revisores acharam e foi consertado** (cada um com a reprodução refeita, e quase todos com prova nova no banco):
  - **As contas do líder morto.** A luta de caça acabada pelo `ato.py luta roda` e fechada com `caca.py volta`, com quem comandava morto, pulava as contas: o chefe morto ficava na contagem e o núcleo não nascia. Agora o `volta` faz primeiro as contas, vivo ou morto quem comandava.
  - **A morte, numa regra só** (alicerce, `REGRAS.md` 5.11). Antes, quem morria no ermo deixava só o que vestia; o núcleo, a peça guardada, a carga e a prata ficavam presos no morto; e a obra do ferreiro morto quebrava o estado até a meia-noite. Agora o morto não fica com nada: tudo cai solto onde ele morreu, a obra se desfaz na hora, e a carga e a prata ficam no lugar. Vale para a fome, a luta e a mão do Mestre.
  - **Morto não age.** O morto comia, pagava a cama, e a MESA não dizia que ele morreu. Agora todo ato é recusado antes de cobrar; a MESA e o RETOMAR abrem com a morte, sem a lista de atos.
  - **Fora é fora** (5.12). Com a saída de caça aberta, a pessoa dormia na pousada, trabalhava e vendia, e passar o tempo rolava de novo o acaso do bicho. Agora quem saiu está no ermo: os atos da vila são recusados, para quem comanda e para quem foi junto. O que o bicho que viu o caçador vai fazer fica decidido quando ele aparece. O sangue esfria se o relógio anda.
  - **Quem vai junto** fica marcado na saída, não entra em duas, e o corpo dele passa os mesmos blocos.
  - **A loja não é achado.** A prateleira e "o chão do ermo" eram a mesma marca: quem passava num rastro num lugar com loja levava a prateleira inteira. Agora o que está caído tem marca própria (`solto`), e só isso se acha.
  - **Vestir e guardar** (5.13). Não havia comando: a peça comprada, forjada ou achada ficava guardada para sempre. Entraram `ato.py vestir`, `tirar` e `pecas`. A peça em uso não se vende sem guardar. A MESA mostra as peças e a carga.
  - **O `itens.py` falava com outro Livro.** Num mundo, `ver` e `janela` leem o Livro dele, e `nova`, `dono` e `conserta` entram por evento.
  - **O gravador e os invariantes.** O `estado.valida` não cobria a etapa 2 e quebrava com tipo errado. Dos 29 estragos plantados pelo revisor, acusava 3 e quebrava em 2. Hoje, no script dele, o gravador recusa 20 na entrada, o `valida` acusa 9 e nenhum dá erro de programa; no banco, 29 de 29 estragos plantados por fora são acusados. O evento que não muda nada não entra mais no registro (eram 120 em 46.195).
  - **A pasta do save pode mudar de lugar.** O caminho da luta aberta fica guardado relativo à pasta. Se o arquivo se perde, a recusa é uma frase, e o Mestre larga a saída (`caca.py larga`, `ato.py luta larga`).
  - **O bicho que "não anda mais" fugia.** Em 2.000 lutas, 9% das corças que fugiam tinham a perna presa. Agora quem está no chão não foge, e o golpe pelas costas que derruba segura a fuga (gente também).
  - **A jornada** (5.4). O livro dizia 2 blocos; o código pagava quantos o corpo aguentasse (7 de prata por dia, não 4). Agora o lugar paga 2 blocos por dia a cada pessoa, e o `trabalhar` e o jornal contam juntos.
  - **Cair no sono** era só texto. Agora quem cai dorme ali mesmo, no chão, até o sono baixar de 6.
  - **Comer da carga.** O caçador vendia a carne a 60% para comprar a refeição inteira. Agora come da própria carga.
  - **O preço da armadura** não olhava o tamanho: a manga de couro valia o mesmo que a placa inteira. Agora vale pelo que cobre, no preço e no conserto; e a loja farta conta por material, não por recorte.
  - **Nascer por evento.** Não havia verbo para nascer lugar nem gente, nem comando para o evento do Mestre. Entraram os dois verbos e o `estado.py mestre`.
  - **A mesa.** Erros de programa na linha de comando (`oficio.py quem=eu`, o bicho sem nível no cenário, `teste.py contra=abc`); os comandos gravam antes de falar; o quadro da luta já não mostra registro de programa; o gênero do bicho ("a corça ENCURRALADA"), as contrações ("na corça"), "patas da frente" em vez de braços, os números com vírgula; "há fartura" de um bicho de que só há um virou "há pouco, e sempre foi assim"; os bichos da MESA aparecem uma vez cada.
  - **`produz.prata`** fazia a virada criar prata: o gravador recusa, e a virada pula.
- **Números de regra que mudaram** (para o jogador confirmar):
  - `tabelas_mundo.JORNADA = 2` passou a valer no código (antes era só texto).
  - **O jornal paga pelo que a mão vale** (`tabelas_oficio.JORNAL_GRAU`): Iniciante, aprendiz; Treinado, oficial; Mestre, mestre. Sem isto, com o teto da jornada, o ferreiro Mestre ganhava como aprendiz e a escada atrasava (a Única ia ao Dia 217).
  - **A armadura vale pelo que cobre** (`tabelas_mundo.PARTE_PESO`): o elmo, um quarto do preço de tabela (Comum: 8 de prata, não 30). O conserto pago segue.
  - **A loja farta** conta peça igual por tipo, material e categoria (antes, também pelo recorte).
  - **Os rótulos dos graus** E e D dizem o que a régua mede; e **o bando vale mais** (`tabelas_bichos.BANDO_GRAU`): 2 ou 3 juntos, um grau acima; 4 ou mais, dois.
  - A vila de prova dos bancos abre com a prata de tabela (2.000), não com 5.000.
- **Metas: o que mudou no jeito de medir, e o que não bate**
  - **NÃO É FIRME: a primeira peça Lendária entre os dias 300 e 450.** É dado de verdade: nas sete rodadas com o código final, nasceu em 13, 11, 7, 16, 5, 5 e 8 de 30 vidas até o Dia 450 (a prova passa com 15). Passou uma vez, na rodada que ficou guardada em `dados/`. Já não batia antes da integração, e o contrato o dizia. As duas metas do ofício não cabem juntas (o robô acerta a Lendária 1 vez em 6 ou 7, e cada obra são 70 dias). Na leitura "a primeira obra fecha", as quatro batem sempre (dias 17, 51, 131 e 356). Não mexi na faixa.
  - **A escada do ofício** bate (Rara no Dia 17, Épica no 59, Única no 177; nas sete rodadas a Única ficou entre o 154 e o 200, que é a borda da faixa), mas na forja mestra, com o preparo todo e núcleo novo a cada obra: 3,1 núcleos Épicos e 3,5 Únicos por vida. Com um núcleo só, a Épica nasce em 40% das vidas e a Única em 26%. O banco agora diz isso na própria linha.
  - **O caçador** bate as duas faixas (2,02 diárias ao preço de base; ferido ou morto em 4,7% das saídas), mas no bolso ficam +1,16 de prata por dia (o diarista fica com +1,00), e morreram 15 de 75 em 30 dias. O cauteloso fica abaixo da faixa de ferimento. O banco agora imprime o bolso e o conjunto.
  - **Caçada demais:** a volta passou a ser medida do fundo que a meta descreve (o teto menos os 60 caçados: de 20 em 80), porque a medida antiga dependia da pressa do caçador e falhou numa rodada em sete. Dá de 86 a 96 dias (faixa: 30 a 120). O banco imprime também a outra leitura (de onde o caçador deixou a contagem).
  - **O Iniciante acerta a Comum em 86%** só com os quatro preparos do Comum; sem preparo nenhum, 57%. O nome da prova agora diz.
  - **B7 (o bicho ferido foge):** caiu de 42% para 32% com o conserto da fuga (o piso é 30%).
- **Rejeitado, e por quê:**
  - `bichos` em `tabelas_mundo.MODULOS`: o `caca.mesa` já chama o `bichos.mesa`; entrar nos dois dobraria as linhas.
  - "O gravador recusar o evento que não muda nada": recusar derrubaria o fecho de uma luta em que o único efeito bate no teto. O evento não entra no registro, e quem chamou segue.
  - A peça que o Mestre põe num ermo sem a marca `solto` (o `valida` cala): deixou de ser estrago. É a peça que não está à venda nem é achado, posta em cena.
  - `BrokenPipeError` com a saída cortada: os comandos passaram a gravar antes de falar; o aviso do sistema em si não se trata.
- **Fica para o jogador decidir** (está no relatório da etapa e no `REGRAS.md`, "o que a etapa 2 não resolve"): se a caça de começo deve pagar mais que a diária; a presa que foge em vez de escoicear; qual é a meta da Lendária; de onde vêm os núcleos da escada; se o Comum de um novato falha quatro vezes em dez; o preço da arma pela matéria; a prata do lugar que não se repõe; o atravessador de comida; a coleta que rende mais que a caça; a refeição pelo preço do dia; a carga e a prata do morto.
- **Bancos:** `python3 provas.py 600`: 77 de 77. `python3 provas_mundo.py`: 70 de 70 na rodada guardada, e 69 de 70 nas outras (a etapa 1, 12 de 12; o alicerce da etapa 2, 6 de 6; o mercado, 15 de 15; a caça, 22 de 22; o ofício, 15 ou 14 de 15: a Lendária). `python3 estresse.py 1500`: 1.500 lutas, 735 com bichos, nenhum erro. As saídas estão em `dados/provas_saida.txt` e `dados/provas_mundo_saida.txt`.
- **A vila de teste** foi jogada três dias pela linha de comando (caçar, vender, forjar, trabalhar, dormir, fechar o turno duas vezes): o estado ficou inteiro. A caçadora foi de 30 a 44 de prata, quase tudo por uma adaga vendida.
