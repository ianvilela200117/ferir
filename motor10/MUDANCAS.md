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
