rascunho: o DESENHO.md manda (depois da revisão: a régua é 1 ou 2 → 4, 3 a 5 → 3, 6 a 8 → 2, 9 a 16 → 1; na categoria do teto a régua para em 2, e o quase só vale abaixo do teto; as contas da seção 5.6 do contrato substituem as daqui; a fase 1a fecha sozinha; nenhuma fraqueza, dom ou classe toca o total)

# D2 — A FORJA DA PARTE 2: a faixa, o teto de efeitos, o cheio e as ferramentas que melhoram a obra

Desenho de regras (não é código ainda). Campo: a forja e o couro pela Lei do Valor (REGRAS 7.3, 7.6, 7.14 a 7.16), os efeitos que nascem da soma, e as ferramentas.
Duas palavras, para não confundir:
- **FAIXA (da soma):** o trecho entre a CD de uma categoria e a CD da de cima (a Incomum vai de 55 a 79).
- **FORÇA (do efeito):** fraco, normal, forte, apelão. É o que o PROJETO 2.1 chama de "faixa do efeito"; aqui se diz força.

Todo número abaixo saiu de conta exata do 2d20 explosivo (em frações, pela mesma regra do dado do `oficio.dist_valor`), conferida por sorteio, salvo onde se diz que é escolha de desenho.

---

## 1. O que o jogador pediu, e o que esta parte entrega

**Os trechos (palavras dele):**
- Dia 24: "Quero forjar equipamento para melhorar os itens que forjo." E: "deve existir a possibilidade desde a apelação até o normal e fraco."
- Dia 31: "eram os dados e as somas que indicavam se seria incomum, comum ou épica." (feito: a Lei do Valor.)
- Dia 35, o pedido central: "Vamos fingir que eu tenho que arranjar 35 para pegar Incomum. E aí eu consigo 45 [...] 50 já vai para raro [...] Eu ganho um Incomum com 2 efeitos extras [...] Quanto mais perto eu chego do raro, sem passar do raro, mais efeitos extras. Aí, por exemplo, eu tiro 51. Aí eu pego o raro, em vez de pegar um Incomum com 3, 4 efeitos extras." E: "eu quero efeitos tops, efeitos que fazem diferença [...] que eu posso montar uma build boa."

**O que esta parte entrega:**
1. **A régua da faixa**, na forma do exemplo dele: dentro da faixa, quanto mais perto da CD de cima, mais efeitos (0, 1, 2, 3, e 4 colado na CD). Passou da CD, vira a categoria de cima.
2. **O que acontece no teto** (a de cima trancada): a soma que passa conta como colada. O dado nunca anda ao contrário.
3. **O teto de efeitos novo** (a Incomum leva até 4) e o **CHEIO**: o que passa do teto enche um efeito com o número da categoria de cima.
4. **A prova** de que a chance de cada categoria não muda: a escada medida e a Lendária de 1 em 4 ficam como estão.
5. **Como se escolhem os efeitos**: quem forja escolhe; o mundo escolhe sozinho, pela semente.
6. **Doze efeitos de ferramenta**, do fraco ao apelão, medidos. Nenhum novo mexe no total. Diz o que a tenaz Incomum de Ferord pode levar.
7. O couro, os outros ofícios e as ideias da pesquisa: o que entra agora e o que fica para depois.

**A consequência maior, dita logo:** hoje sai efeito em perto de 1 obra em 10 (só pelos 20). Com a faixa, sai efeito em 6 ou 7 obras em 10, e a média vai de 0,1 para 1,0 a 1,5 efeito por obra. A categoria segue decidindo (×3); o efeito decide entre iguais. Por isso os números de cada efeito (o catálogo do desenho dos efeitos) têm de ser calibrados para essa frequência.

---

## 2. As regras, para a mesa

### 2.1 A régua da faixa: conta-se o que falta para a CD de cima

A categoria sai como hoje: a maior CD que o total alcança, até o teto. Depois, olha-se **quanto faltou para a CD de cima**:

| Faltou para a CD de cima | Efeitos da faixa | O nome à mesa |
| --- | --- | --- |
| 17 ou mais | 0 | o terço de baixo |
| 9 a 16 | 1 | o terço do meio |
| 4 a 8 | 2 | o terço de cima |
| 2 ou 3 | 3 | colada |
| 1 | 4 | no fio |

A mesma régua vale em toda faixa. Em totais:

| Faixa | 0 efeito | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| Comum (22 a 54) | 22 a 38 | 39 a 46 | 47 a 51 | 52 e 53 | 54 |
| Incomum (55 a 79) | 55 a 63 | 64 a 71 | 72 a 76 | 77 e 78 | 79 |
| Rara (80 a 104) | 80 a 88 | 89 a 96 | 97 a 101 | 102 e 103 | 104 |
| Épica (105 a 129) | 105 a 113 | 114 a 121 | 122 a 126 | 127 e 128 | 129 |
| Única (130 a 154) | 130 a 138 | 139 a 146 | 147 a 151 | 152 e 153 | 154 |
| Lendária (155 a 179) | 155 a 163 | 164 a 171 | 172 a 176 | 177 e 178 | 179 |

**De onde veio.** O exemplo dele tem uma faixa de 15 (de 35 a 50): com 45 faltam 5 e saem 2 efeitos; colado, 3 ou 4. As nossas faixas têm 25. Escalando por 25/15, os terços caem em 8 e 16: falta até 8 dá 2, falta até 16 dá 1. É a forma dele nas CDs reais. A Beira da pesquisa (efeito só a 8 da CD) era mais estreita do que ele pediu.
- **Uma régua só, contada pelo que falta.** A faixa da Comum é mais larga (33): pela régua única, a metade de baixo dela não dá efeito. É de propósito: a Comum custa 1 bloco, e a régua não pode virar mina de efeito barato.
- **A Lendária fecha em 180,** a CD da Mítica pelo passo de 25 (ninguém forja Mítica: `FORJA_ATE = 5`). De 180 para cima é o teto (2.2).

### 2.2 No teto: a soma que passa da CD trancada conta como colada

O teto tranca a categoria de cima: a matéria (sem núcleo, nada passa da Rara), a porta do degrau (Leigo e Iniciante param na matéria), o núcleo, ou a Lendária. **O total que passa da CD trancada conta como colado: falta 1, 4 efeitos.**

**Por quê: o dado nunca anda ao contrário.** Mestre, matéria Rara, teto Rara, sem dado especial. Os efeitos da faixa por total:

| Leitura do teto | 95 | 100 | 103 | 104 | 105 | 110 | 120 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **colada (esta)** | 1 | 2 | 3 | 4 | 4 | 4 | 4 |
| conta como o terço de cima | 1 | 2 | 3 | 4 | 2 | 2 | 2 |
| não dá nada | 1 | 2 | 3 | 4 | 0 | 0 | 0 |

Nas outras duas leituras, tirar mais no dado dá menos efeito. A conta de todas as faixas e tetos (933 totais) achou zero inversões com a leitura colada.

**A mina de efeitos baratos, medida.** Quem soma muito acima da faixa da obra vive no teto:

| Quem, que obra | Sai no teto | Dessas, cheias (no teto de efeitos) |
| --- | --- | --- |
| Ferord (2d20 + 23), matéria Comum, teto Incomum | 15,1% das obras | 6,9% |
| um Mestre (2d20 + 35), matéria Comum, teto Incomum | 56,2% | 8,0% |
| o melhor possível (2d20 + 52), matéria Comum, teto Incomum | 90,2% | 39,3% |
| o melhor possível (2d20 + 82), matéria Rara, teto Rara | 90,2% | 62,3% |

O melhor ferreiro do mundo tira Incomum cheia de matéria Comum, em 1 bloco, e Rara cheia de matéria Rara sem núcleo. Três coisas seguram isso:
- o teto de efeitos (2.4);
- a loja paga pela categoria, não pelo efeito (`mercado.valor`): a prova FORJAR PARA A LOJA NÃO É MINA não muda;
- a meta do duelo (seção 5, meta 10): a magra de cima vence a cheia de baixo.

Se o duelo falhar, a saída é conferir o tamanho dos efeitos (o desenho dos efeitos), não a régua.

### 2.3 Os dados especiais, o quase e a obra-prima: tudo soma

**Efeitos = os da faixa + 1 por 20 + o quase, até o teto de efeitos da categoria.** Os dados especiais seguem como estão:

| O que sai | O que faz agora |
| --- | --- |
| cada 20 (o que abre e os da cadeia) | +1 efeito, como hoje. O 20 empurra o total e às vezes joga a peça no fundo da faixa de cima: o +1 do 20 compensa |
| os dois abrindo em 20 (obra-prima) | a peça sobe uma categoria se o teto deixa, e **a faixa fica** (conta-se na faixa que o total alcançou). No teto, +1 efeito que pode passar do teto de efeitos (como hoje) |
| um abrindo em 1 | a peça cai uma categoria (a Comum sai tosca), e **a faixa fica**: o 1 tira a categoria, não tira os efeitos |
| os dois abrindo em 1 | a matéria e o núcleo se perdem. A ferramenta Épica segura (Comum tosca, **sem efeito**) |
| abaixo de 22 | perde-se. A ferramenta Rara segura a 5 (Comum tosca, **sem efeito**) |
| o QUASE (poder da ferramenta Única ou melhor) | +1 efeito quando faltou 6 ou menos: no teto também (o teto conta como colado), e com ou sem dado especial (o quase segue a faixa) |

**Por que o 1 e os dois 1 não mudam.** Qualquer mexida neles muda a chance da categoria. O "1 com escolha" da pesquisa (ficar na categoria com um defeito) subiria a Lendária acima de 1 em 4. A única mudança é a faixa ficar no 1. Tirá-la custaria até 0,11 efeito por obra, e o 1 já tira uma categoria.

### 2.4 O teto de efeitos e o CHEIO

| Categoria | Hoje | **Novo** |
| --- | --- | --- |
| Comum | 1 | **2** |
| Incomum | 1 | **4** |
| Rara | 2 | **4** |
| Épica | 2 | **5** |
| Única | 3 | **5** |
| Lendária | 3 | **6** |
| Mítica | 3 | **6** |
| Primordial | 3 | **7** |

À mesa: "a Comum leva 2; a Incomum e a Rara, 4; e daí +1 a cada duas categorias".
- **A Incomum leva 4** porque é o pedido: colada na Rara, "3, 4 efeitos extras". A Rara não pode levar menos que a Incomum.
- **A Comum leva 2** pela mina (1 bloco de matéria Comum). A Comum de Ferord (matéria Comum) levaria 1,08 efeito em média com teto 3; com 2, leva 0,98, e a sobra vira cheio.
- **Forjar Comum sem parar** dá a Ferord uma Comum de 2 efeitos em 1 obra de 4, a 1 bloco cada. São efeitos fracos, com o número da Comum, numa peça que vale ×1; a Incomum magra vale ×3. É vantagem de ferreiro no começo, não mina: a loja paga a Comum pelo preço da Comum.
- **A obra-prima no teto** passa o teto de efeitos em 1 (como hoje), e o molde de mestre (2.8) também. Nada mais passa.

**O CHEIO.** O que passa do teto de efeitos não se perde: **cada efeito a mais enche um efeito de número com o número da categoria de cima**. A Rara cheia leva o Gume da Épica: empata no efeito com a Épica magra e nunca passa. A categoria segue valendo ×3.
- Um cheio por efeito, no máximo.
- Só nos efeitos de número (dano, acerto, defesa, devolve, sangria...).
- A peça sem efeito de número para encher perde a sobra.

**A conta inteira, em ordem** (o que o `_resolve` novo faz):
1. A categoria k, como hoje (a maior CD alcançada, até o teto).
2. Falta = CD de cima − total (a CD de cima da Lendária é 180). Se k é o teto, a falta é no mínimo 1.
3. Faixa = régua(falta − prumo); com o lastro, 0 vira 1.
4. n = faixa + vintes + brasa (os 19) + quase.
5. Os dados: dois 1, um 1, dois 20, abaixo de 22 (a tabela de 2.3).
6. Efeitos = mínimo(teto de efeitos da categoria final, n) + obra-prima no teto (+1) + molde (+1, se a peça sai na categoria da obra ou acima).
7. Cheios = mínimo(efeitos de número, sobra acima do teto + têmpera).

### 2.5 A prova: a chance de cada CATEGORIA não muda

Os passos 2 a 7 só contam efeitos: não tocam no total nem no passo 1.
- **A conta.** Com o MESMO dado do `oficio.dist_valor` (o `_UM`, cortado em 4 voltas), a categoria do resolve novo bateu com a do `oficio.dist_valor` de hoje em 2.982 casos: soma de −10 a 200 (de 3 em 3), teto 0 a 5, sem ferramenta e com cada ferramenta da Comum à Lendária. **A maior diferença foi 0** (nem na última casa do número). Com o prumo, o lastro, a brasa e a têmpera ligados, mais 320 casos, também 0.
- **O sorteio.** A regra escrita de novo, do zero, com o dado rolado como o `teste.py` rola, em 200 mil obras por perfil: a maior diferença numa casa (categoria, efeitos) foi 0,14 ponto. O erro do sorteio é de 0,11 ponto por desvio.
- **O que isso garante.** As metas T1 a T5 da Lei do Valor e a escada do robô (que usa martelo e tenaz lisos, entregues pelo banco) não mudam. A escada pelo talento (10.8) e a Lendária de 1 em 4 do melhor ferreiro também não.

### 2.6 As contas exatas: quanto sai de cada coisa

**"Ferord hoje"** é a soma que a mesa mostra hoje, tirada com `oficio.valor` da ficha dele:
- Treinado na forja (4) + Afinidade 75 (7) + forja de vila (1) + preparo +6 (a receita, o fogo e a bigorna, até o Incomum).
- No lugar do martelo, o martelo de forja Incomum (3). No da tenaz, o jogo Comum afinado (1, e mais 1 da afinada).
- Dá **2d20 + 23** na matéria Comum e **2d20 + 38** na Incomum (a obra da tenaz: 1 de metal e 1 de madeira Incomuns).

Os números são % por obra; "cheios" é por 100 obras.

**Ferord hoje, matéria Comum** (2d20 + 23; teto Incomum)

| a peça sai | chance | 0 efeito | 1 | 2 | 3 | 4 | 5 ou mais | cheios |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Comum | 84,6% | 26,0 | 34,2 | 24,4 | · | · | · | 10,8 |
| Incomum | 15,1% | 7,0 | 3,1 | 2,9 | 1,0 | 0,8 | 0,2 | 1,3 |

Perde 0,25% · 0,99 efeito por obra (hoje: 0,10) · peça com efeito 66,8% (hoje: 9,8%).

**Ferord hoje, matéria Incomum: a tenaz** (2d20 + 38; teto Rara)

| a peça sai | chance | 0 efeito | 1 | 2 | 3 | 4 | 5 ou mais | cheios |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Comum | 32,2% | 2,0 | 6,9 | 23,4 | · | · | · | 14,5 |
| Incomum | 63,0% | 35,5 | 19,1 | 5,3 | 1,8 | 1,3 | · | 0,5 |
| Rara | 4,5% | · | 2,9 | 0,9 | 0,2 | 0,3 | 0,2 | 0,5 |

Perde 0,25% · 1,01 efeito por obra (hoje: 0,11) · peça com efeito 62,3%. **A Incomum com 3 ou 4 efeitos, colada na Rara, sai em 3,1% das obras:** é o prêmio do pedido. A Comum que errou a Incomum por pouco sai 3 vezes em 4 com 2 efeitos, e quase metade das vezes com um cheio.

**Um Mestre, matéria Rara** (Mestre, Afinidade 80, grande forja, preparo +8, martelo e tenaz Raros: 2d20 + 65; teto Rara)

| a peça sai | chance | 0 efeito | 1 | 2 | 3 | 4 | 5 ou mais | cheios |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Comum | 6,0% | · | 2,0 | 4,0 | · | · | · | 2,0 |
| Incomum | 20,0% | 3,0 | 1,6 | 7,7 | 4,9 | 2,9 | · | 0,1 |
| Rara | 73,8% | 34,5 | 23,0 | 7,3 | 2,2 | 6,4 | 0,2 | 6,6 |

1,24 efeito por obra · peça com efeito 62,3%. O 6,4% de Raras com 4 efeitos é o teto colado (2.2).

**O mesmo Mestre, núcleo Épico** (2d20 + 80; teto Épica)

| a peça sai | chance | 0 efeito | 1 | 2 | 3 | 4 | 5 ou mais | cheios |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Incomum | 9,1% | 3,0 | 4,0 | 2,0 | · | 0,1 | · | 0,0 |
| Rara | 55,2% | 3,8 | 19,2 | 20,2 | 8,2 | 3,8 | · | 0,1 |
| Épica | 35,4% | 22,5 | 5,3 | 3,1 | 1,9 | 0,6 | 2,1 | 0,7 |

1,38 efeito por obra · peça com efeito 70,5%.

**O melhor possível, núcleo Lendário** (Lendário, Afinidade 100, forja mestra, preparo +8, martelo e tenaz Lendários: 2d20 + 127; teto Lendária; com o quase)

| a peça sai | chance | 0 efeito | 1 | 2 | 3 | 4 | 5 ou mais | cheios |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Comum (tosca) | 0,2% | 0,2 | · | · | · | · | · | 0,0 |
| Épica | 9,2% | 4,5 | 4,0 | 0,5 | · | 0,1 | 0,1 | 0,0 |
| Única | 65,2% | 9,0 | 25,2 | 8,8 | 12,0 | 6,8 | 3,3 | 0,2 |
| Lendária | 25,4% | 15,8 | 3,0 | 3,3 | 0,7 | 0,8 | 1,8 | 0,7 |

1,54 efeito por obra (hoje: 0,33) · peça com efeito 70,5% (hoje: 31,5%). **A Lendária segue em 25,4%**, a de hoje. Perto de uma Lendária em 19 nasce com 6 ou 7 efeitos.

**Um Iniciante** (2d20 + 8, matéria Comum, a porta): Comum 80,5% (com efeito em 23% delas), perde 19,5%; 0,28 efeito por obra. A mão melhor faz mais efeito: é a escada do ofício aparecendo na peça.

**A colada** (3 ou 4 efeitos só da faixa) sai em 4,6% das peças do Iniciante, 8 a 12% das de Ferord, 15 a 17% das do Mestre e 11,9% das do melhor.

### 2.7 Como se escolhem os efeitos

- **Quem escolhe.** A peça nasce com N efeitos por escolher (e C cheios). Escolhe o dono, que na forja é quem forjou, um por vez: `oficio.py efeito ITEM CHAVE [cheio]`. Cada escolha é um evento e entra na história da peça. A peça guarda o que falta escolher até o dono escolher. Sem CHAVE, o comando lista o que cabe, com o número na categoria da peça e o número cheio.
- **A porta, pela força.** Só cabe o que a categoria FINAL da peça abre: **fraco da Comum · normal da Incomum · forte da Épica · apelão da Lendária** (PROJETO 2.1). O efeito vale no tipo de peça certo, não se repete, e o "pesa" não se escolhe. Recomendação ao desenho dos efeitos: no máximo 1 apelão por peça.
- **O número.** O efeito de número leva o número da categoria da peça (a tabela do desenho dos efeitos). Cheio, leva o da categoria de cima. O devolve de hoje segue: 1 até 4 por degrau, e cheio até o teto da categoria de cima.
- **Os 8 efeitos de hoje,** pela lista do PROJETO 2.1: fracos o sangra, o leve e o nao_quebra; normais o critico_19, o derruba, o firme e o devolve. A Comum não leva mais o critico_19.
- **A peça que muda de mão** com efeito por escolher: quem a recebe escolhe. A peça vendida à loja escolhe sozinha ao entrar na prateleira, pela receita do lugar (pergunta F6).

**Sozinho (o mundo).** Quem não é o jogador escolhe na hora em que a peça nasce, pela **receita do jeito** do ferreiro (ou do dono que encomendou: o rival). O jeito sai da semente, sem gravar nada: `estado.sorte(E, "jeito|PID")`. São quatro:

| Jeito | Prefere |
| --- | --- |
| do gume | dano, crítico, sangue |
| da guarda | defesa, firmeza, aparar |
| do fôlego | leveza, não quebrar, fôlego |
| do tranco | derrubar, atordoar, medo |

A receita põe primeiro os efeitos de número (para o cheio ter onde cair), dentro da porta. O empate se desfaz pela semente (`estado.sorte(E, "efeito|ID|n")`): mesma semente, mesma escolha. O jogador também pode mandar `oficio.py efeito ITEM auto` (a receita do gume na arma, a da guarda no resto).

### 2.8 As ferramentas que melhoram a obra (o catálogo)

O martelo de forja, a tenaz e o jogo nascem pela mesma lei, com faixa e efeitos. Valem as regras de 7.14: a ferramenta só vale inteira, do dono, do ofício, e em cada lugar vale a melhor. Duas regras novas:
- **Em cada lugar, a de maior categoria; no empate, a de mais efeitos (e depois a afinada).** Valem os efeitos das duas que estão em uso (a do lugar do martelo e a do lugar da tenaz). O jogo, se é o melhor nos dois lugares, vale uma vez.
- **O mesmo efeito em duas ferramentas não soma: vale o maior número.**

Martelo e tenaz separados levam até o dobro de efeitos do jogo. É mais um motivo para forjá-los separados, como Ferord já está fazendo.

**A régua de força das ferramentas.** Mede-se em **pontos de feitio por obra** (efeitos + metade dos cheios). É a média dos cinco ferreiros de 2.6: Ferord com matéria Comum e Incomum, o Mestre com Rara e com núcleo Épico, o melhor com núcleo Lendário. Sem ferramenta, a base vai de 1,05 a 1,55. O efeito, no número da categoria da ferramenta, não pode passar do teto da força que essa categoria abre: **Comum 0,15 · Incomum e Rara 0,30 · Épica e Única 0,60 · Lendária 1,20.** É o passo ×2 da régua do duelo (5, 10, 20, 40) sobre uma base de perto de 1 efeito por obra. Grosso modo: a ferramenta fraca dá até +15% de efeitos; a apelona, até o dobro.

| Efeito | Força (abre na) | O que faz | Número pela categoria da ferramenta | Medido (pontos de feitio por obra) |
| --- | --- | --- | --- | --- |
| **afinada** (já existe) | fraco (Comum) | +1 no total do ofício, uma vez por obra. É a ÚNICA que mexe no total: fica +1, não cresce | +1 | +0,02 nos efeitos; +2,8 pontos na chance da Incomum (a obra da tenaz) |
| **brasa** | fraco (Comum) | o dado que abre em 19 dá +1 efeito, como o 20 (não rola de novo, não soma) | — | +0,09 |
| **recobro** | fraco (Comum) | a obra perdida devolve metade da matéria, para baixo; o núcleo se perde como sempre | — | matéria |
| **mão de reparo** | fraco (Comum) | o conserto na bancada devolve 10 pontos por bloco, não 5 | — | tempo, fora da escada |
| **mão de medida** | fraco (Comum) | o ajuste sob medida leva metade dos blocos (para cima) e soma +2 no teste dele | — | tempo, fora da escada |
| **sinete** | fraco (Comum) | a peça nasce com o sinete de quem a forjou: a janela diz, e a notícia de um feito com ela leva o nome do ferreiro | — | assinatura, sem luta |
| **prumo** | normal (Incomum) | a falta para a CD de cima conta N a menos, só para os efeitos | Incomum 1 · Rara 2 · Épica 3 · Única 4 · Lendária 5 | +0,14 · +0,28 · +0,43 · +0,57 · +0,72 |
| **poupa-ferro** | normal (Incomum) | a obra gasta 1 a menos da matéria principal, se a peça leva 3 ou mais dela (a espada com 2 de metal) | — | matéria: um terço da espada |
| **lastro** | forte (Épica) | a peça que alcança uma categoria nasce com pelo menos 1 efeito da faixa (o terço de baixo dá 1) | — | +0,36 |
| **têmpera** | forte (Épica) | N efeitos de número da peça nascem cheios | Épica 1 · Única 2 · Lendária 3 | +0,33 · +0,48 · +0,55 |
| **molde de mestre** | apelão (Lendária) | ao abrir a obra, diz-se um efeito (`molde=CHAVE`, da força que a obra abre). Se a peça sai na categoria da obra ou acima, nasce com ele, fora do teto de efeitos. Se sai abaixo, o molde se perde | — | +0,60 |
| **degrau emprestado** | apelão (Lendária) | um efeito da peça pode ser da força de cima (o forte na Incomum e na Rara; o apelão na Épica e na Única), com o número da categoria da peça; um por peça | — | no duelo: dentro da régua da força de cima |

- Todos cabem no teto da força. O prumo na Única fica em 0,57 (o teto é 0,60); o quase, poder da Única, dá +0,18, para comparar.
- O cheio vale nas ferramentas de número: o prumo cheio de uma tenaz Incomum é 2, o número da Rara.
- **O que mexe no total foi evitado de propósito:** muda a chance da categoria e a escada. Também ficaram de fora o que encurta o tempo da obra (a escada é medida em dias) e o que devolve o núcleo (o núcleo é o freio da escada: 6 Épicos e 2 Únicos por ano).
- **Os conjuntos, medidos.** Um Mestre com martelo e tenaz Épicos (prumo 3, lastro, têmpera 1, brasa), na obra de núcleo Épico, vai de 1,40 a 2,70 pontos de feitio por obra, com efeito em toda peça. O melhor ferreiro com tudo Lendário (prumo 5, lastro, têmpera 3, brasa, molde) vai a 3,87. A Lendária dele nasce com 2 a 8 efeitos (7 ou mais em 1 de 10) e 1,8 cheio em média. É o topo do jogo: cada uma dessas ferramentas é, ela mesma, uma obra Lendária.

**A tenaz Incomum de Ferord.** A obra é a de 2.6 (2d20 + 38): sai Incomum em 63% (com efeito em 27,5% das obras: 1 efeito 19,1%; 2, 5,3%; 3 ou 4, 3,1%), Comum em 32% (quase sempre com 1 ou 2 efeitos fracos) e Rara em 4,5% (sempre com efeito).
- **Incomum ou Rara, ela pode levar:** os fracos (afinada, brasa, recobro, mão de reparo, mão de medida, sinete) e os normais (prumo: 1 na Incomum, 2 na Rara, um a mais se cheio; poupa-ferro). Até 4.
- **Comum, só os fracos,** até 2. Aí ela disputa o lugar da tenaz com o jogo Comum afinado: vale a de mais efeitos.
- **Um detalhe da regra de hoje:** a tenaz Incomum lisa empurra o jogo afinado para fora dos dois lugares, e a soma sobe só 1 (de 38 para 39, não para 40). Se ela nascer afinada, sobe 2.
- **A ordem que recomendo:** prumo (é o que melhora toda peça que vier: +0,12 efeito por obra), depois afinada (devolve o +1), depois brasa. Com prumo, afinada e brasa, a obra de matéria Incomum dele vai de 1,08 a 1,30 pontos de feitio; com o prumo cheio, a 1,42.

### 2.9 O couro e os outros ofícios

- **O couro:** a mesma lei e a mesma faixa (já está em `VALOR_OFICIOS`). O jogo de couro (a faca e a sovela) leva os mesmos efeitos de ferramenta.
- **O encanto** (o foco e o amuleto), **a alquimia, a gravação e o ajuste** ficam no teste de passar nesta parte.
  - O encanto segue com os efeitos pela margem (10, 20, 30 dão 1, 2, 3), agora nos tetos novos: o foco Comum pode levar 2.
  - A alquimia não tem efeito (a poção é bem). A gravação e o ajuste passam ou falham.
  - Levar o encanto para uma Lei do Valor própria, com CDs e faixa, é para quando a magia for revista.

### 2.10 As ideias da pesquisa: o que entra agora e o que fica

| Ideia (PESQUISA 3.3) | Fase 1? | Com que números, e por quê |
| --- | --- | --- |
| o molde de mestre | **sim, como efeito de ferramenta Lendária** (2.8) | +1 efeito fora do teto, dito ao abrir: +0,60 ponto de feitio. O "molde por grau de maestria" da pesquisa é técnica de ofício (o desenho das habilidades). Os dois não se somam: um molde por obra |
| o calo do malho | **não** | a própria faixa já é a piedade: quem erra por pouco ganha efeito (a Comum que errou a Incomum por pouco sai com 2 efeitos e cheio). Se voltar: +1 de calo por obra que sai abaixo da matéria, até +4, contando como prumo; zera quando a faixa dá 3 ou mais |
| o decalque | depois, com as habilidades de copiar | desmancha uma peça Rara ou melhor (ela some), e o efeito vai ao livro de talhos. Gravado em peça nova, sai com o número da categoria de baixo até o 3º decalque do mesmo efeito. O poder de lenda só com núcleo |
| o enxerto | depois (pede um bem novo, o pó de um mineral) | −6 no total por enxerto, até 3, por escolha (a chance da categoria só desce). Um, dois ou três dão o Gume +5%, +10%, +25% (o salto). Os números dependem do Gume do desenho dos efeitos |
| o banho negro | depois | uma vez por peça Rara ou melhor, depois de pronta, 1d4 pelo script: 1 nada · 2 um efeito vira cheio · 3 uma marca torta e um efeito novo · 4 racha e cai uma categoria. A peça fica selada |
| a marca-mãe | depois, com o catálogo dos efeitos | um lugar à parte, da Única para cima, gravado primeiro; nenhuma se repete no mundo enquanto a peça viver |
| o nome ganho | depois, com os feitos e a fama | a peça Rara ou melhor que decide um feito registrado ganha nome e +1 efeito ligado ao feito, fora do teto. Um nome por peça; da Única para cima, dois |
| a reforja de linhagem | depois, **com a regra mudada** | a memória (+10, ou +15 se de herói morto) soma só na FAIXA (como prumo), nunca no total: a escada e a Lendária de 1 em 4 ficam. Herda 1 efeito; não sai abaixo da categoria antiga menos uma (isso só tira falha, não sobe a Lendária). Uma vez por linhagem |

Também não entram: o "1 com escolha" (muda a chance da categoria) e "a mão assentada" (+3% por grau nos números: é técnica de ofício, do desenho das habilidades).

### 2.11 Um exemplo de mesa

> Ferord forja a tenaz Incomum. 2d20 + 38. Dados: 9 e 18, total 65. **Incomum**; faltaram 15 para a Rara (80): o terço do meio, **1 efeito por escolher**. Cabem: afinada, brasa, recobro, mão de reparo, mão de medida, sinete, prumo 1 (cheio: 2), poupa-ferro. O jogador escolhe: `oficio.py efeito ITEM prumo`.
>
> Outra rolagem: 20 (que rola de novo: 6) e 14, total 26 + 14 + 38 = 78. Incomum, faltaram 2: colada, 3 da faixa, +1 do 20 = **4 efeitos**, no teto da Incomum.
>
> Outra: total 81. **Rara**; faltaram 24 para a Épica: 0 efeito. A Rara magra vale mais que a Incomum de 4: a categoria é ×3.

---

## 3. Os dados: o que muda na ficha, no item, na obra e nos eventos

- **A pessoa:** não muda. O jeito de quem forja sozinho sai da semente, sem gravar.
- **O item** (`itens.json`):
  - `efeitos`: cada um `{chave, valor?, cheio?, emprestado?}`. O número do efeito sai da tabela pela categoria (e +1 categoria se `cheio`); o devolve segue com `valor`.
  - `efeitos_livres` (existe).
  - `cheios_livres` (novo, inteiro ≥ 0): quantos dos efeitos ainda por escolher podem ser cheios.
  - `teto_efeitos` (novo, gravado ao nascer): o teto de efeitos da categoria, mais a obra-prima no teto e o molde. Peça antiga sem o campo: o teto da categoria.
  - `sinete` (novo, opcional): o id de quem forjou, quando a ferramenta tem sinete.
  - A primeira linha da história diz a faixa: "faltaram 6 para a Rara: 2 da faixa, 1 do 20".
- **A obra:** `molde` (novo, opcional), a chave escolhida ao abrir, quando a ferramenta tem o molde de mestre.
- **Os verbos do `estado.py`** (os mesmos, com validação a mais):
  - `['item', id, 'efeito', 'junta', {chave, cheio?, valor?, emprestado?}]`. Confere: a força cabe na porta da categoria (+1 se `emprestado`, e só um por peça); `cheio` só em efeito de número; `len(efeitos) + 1 ≤ teto_efeitos`.
  - `['item', id, 'cheios_livres', 'poe'|'soma', n]` (novo, como o `efeitos_livres`).
  - `teto_efeitos` e `sinete` vêm no registro do `['item', 'nasce', ...]`; mudar depois só em evento "mestre".
  - `['obra', 'abre', registro]` aceita `molde`.
- **`estado.valida`:** `cheios_livres` inteiro ≥ 0; efeitos (os escolhidos e os por escolher) até `teto_efeitos`; cheio só em efeito de número; a força de cada efeito dentro da porta (com o emprestado).
- **As tabelas** (`tabelas_oficio.py`):
  - `REGUA_FAIXA = ((1, 4), (3, 3), (8, 2), (16, 1))`, `VALOR_CD_ACIMA = 180`.
  - `EFEITOS_MAX = (2, 4, 4, 5, 5, 6, 6, 7)`, `FORCA_PORTA = dict(fraco=0, normal=1, forte=3, apelão=5)`.
  - `FERRAMENTA_EFEITOS` = {chave: (força, números por categoria ou None)} para os 12 de 2.8.
  - Os efeitos de luta ganham a força e os números no catálogo do desenho dos efeitos (`itens.EFEITOS`).

---

## 4. Onde entra no motor

| Arquivo · função | O que muda | Novo? |
| --- | --- | --- |
| `tabelas_oficio.py` | as constantes de 3; `falta(total, k, teto)` e `efeitos_da_faixa(total, k, teto, prumo=0, lastro=False)`; o `efeitos_da_obra` do encanto passa a usar o teto novo | muda e novo |
| `oficio._resolve` | a categoria fica igual, linha por linha. A saída ganha `falta` e `faixa`, e o QUASE passa a valer também no teto | muda |
| `oficio.dist_valor` | não muda (a chance da categoria) | — |
| `oficio.dist_efeitos(soma, teto, fc, ferr)` | a conta conjunta (categoria, efeitos, cheios) para a mesa | novo |
| `oficio.ferramentas` · `valor_ferramentas` | o desempate pelos efeitos; `efeitos_de_ferramenta(E, pid, oficio)` junta os efeitos das duas em uso (o mesmo efeito vale o maior) | muda e novo |
| `oficio.valor` · `diz_valor` · `pede` | a mesa mostra a régua de cada faixa até o teto, os efeitos por obra, a peça com efeito e a colada | muda |
| `oficio.forjar` | `molde=CHAVE` (só com o molde de mestre); o poupa-ferro na matéria que entra na obra | muda |
| `oficio._remata_valor` | `efeitos_livres`, `cheios_livres`, `teto_efeitos`, o molde, o sinete; o recobro na obra perdida; o texto "faltaram N" | muda |
| `oficio.efeito` | a porta pela força, o cheio, o emprestado, os efeitos de ferramenta; sem CHAVE, lista o que cabe; `auto` | muda |
| `oficio.escolhe_sozinho(E, iid, jeito=None)` | a receita do jeito, pela semente | novo |
| `oficio.consertar` · `ajustar` · `_remata_ajuste` | a mão de reparo; a mão de medida | muda |
| `itens.EFEITOS` · `itens.janela` | os 12 de ferramenta (tipo `ferramenta`); a janela mostra "cheio", o número de cada efeito e o sinete | muda |
| `estado.py` (item, obra, valida) | 3 | muda |
| `rivais._r_forja` | sai a chance fixa: rola a mesma lei com a soma do ferreiro da capital e o dado do mundo (`estado.sorte`), e escolhe pelo jeito do rival | muda |
| `provas_oficio.py` | as provas de 5 | novo |
| `REGRAS.md` 7.3, 7.6, 7.14 a 7.16 · `MUDANCAS.md` | reescritos pela régua, pelo teto, pelo cheio e pelo catálogo | muda |

As peças que já existem não ganham efeito retroativo. As peças da história (PROJETO 2.2) podem usar a mesma régua: uma soma sorteada pela semente dentro da faixa da categoria, e a escolha pelo nome e pela história delas (interface: `oficio.efeitos_do_mundo(E, iid)`; o desenho é de quem cuida das peças do mundo).

**A ordem de construir.** A faixa pode entrar com os 8 efeitos de hoje, marcados com a força. Mas o cheio só tem onde cair quando chegarem os efeitos de número do catálogo: o ideal é construir junto com ele, ou logo depois.

---

## 5. O banco: as metas

| # | O que se mede | Como | A faixa aceita |
| --- | --- | --- | --- |
| 1 | A CATEGORIA NÃO MUDA | a chance de cada categoria do resolve novo contra o `oficio.dist_valor` de hoje: soma −10 a 200, teto 0 a 5, ferramenta nenhuma a Lendária, e com cada efeito de ferramenta ligado | diferença máxima ≤ 1e−12 (medido: 0) |
| 2 | AS METAS DA LEI DO VALOR (T1 a T5) e A ESCADA (Rara, Épica, Única, Lendária rara de propósito; o ritmo) | as de hoje (`provas_oficio.py`) | as de hoje, sem mexer |
| 3 | A FAIXA, pela conta exata | os cinco ferreiros de 2.6 | Treinado ou melhor: peça com efeito de 55 a 75%, de 0,8 a 1,7 efeito por obra; o Iniciante, de 10 a 30%; a colada em 4 a 20% das peças; na obra da tenaz de Ferord, a Incomum com 3 ou 4 efeitos em 2 a 6% das obras (medido: 3,1%) |
| 4 | O DADO DE VERDADE | 400 obras da tenaz de Ferord com o `teste.rola` | a fração com efeito bate com a exata (62,3%) a 4 desvios |
| 5 | A MONOTONIA | todo total de toda faixa e teto, com e sem prumo e lastro | zero vezes em que mais soma dá menos efeitos da faixa |
| 6 | O TETO | o total na CD trancada e acima: matéria Comum de Treinado, a porta do Iniciante, matéria Rara, núcleo, Lendária a 180 ou mais | sempre 4 da faixa |
| 7 | O TETO DE EFEITOS E O CHEIO | peças nascidas e escolhidas | nenhuma passa do `teto_efeitos`; o cheio só em efeito de número, com o número da categoria de cima; a obra-prima no teto passa 1; sem efeito de número, a sobra se perde |
| 8 | A ESCOLHA | o comando e o sozinho | a porta pela força; sem repetir; só o dono; cada escolha é um evento; mesma semente, mesma escolha; 40 ferreiros sorteados mostram os 4 jeitos |
| 9 | AS FERRAMENTAS | a régua de 2.8; o recobro (a conta da matéria fecha); o poupa-ferro (−1 só com 3 ou mais); a mão de reparo (10 por bloco); a mão de medida; o sinete na janela; o mesmo efeito em duas ferramentas | cada efeito dentro do teto da força da categoria; o resto funciona; o mesmo efeito não soma |
| 10 | O DUELO (com o catálogo dos efeitos: `provas.py`, 4.000 lutas por linha, gente igual) | a magra de cima contra a cheia de baixo: Rara magra × Incomum de 4 efeitos (2 cheios), Épica magra × Rara cheia, Única × Épica cheia, Lendária × Única cheia | a de cima vence em 60% ou mais em cada linha |
| 11 | A LOJA | FORJAR PARA A LOJA NÃO É MINA; e o mesmo robô com uma tenaz Incomum de poupa-ferro | as faixas de hoje (6 · 12 · 4), nos dois |
| 12 | O DOM ESCONDIDO | ele se mostra quando muda a categoria ou o número de efeitos da faixa ("sem o dom, saía com menos efeitos") | mede e diz: um Treinado com Dom +1 se mostra por obra em 2,0% (categoria) + 8,4% (faixa); com Grande Dom (+2), 3,8% + 16,7% |
| 13 | A MESA | `pede` mostra a régua de cada faixa até o teto; o remate diz "faltaram N: X da faixa, Y dos 20"; a janela mostra o cheio | sim |

---

## 6. O que fica para depois, os riscos e as perguntas

**Fica para depois:**
- o decalque, o enxerto, o banho negro, a marca-mãe, o nome ganho, a reforja de linhagem (2.10);
- o encanto numa Lei do Valor própria;
- a loja e o leilão pagarem pelo efeito (hoje pagam pela categoria; mexer nisso pede a prova da mina de novo);
- o ranking de ferreiros pelo sinete;
- o comando `oficio.py usa ITEM` para escolher qual ferramenta vale no empate.

**Os riscos:**
1. **Dez vezes mais efeitos.** O mundo vai se encher de peças com efeito. O tamanho de cada efeito (o catálogo) tem de ser calibrado para isso, e a meta 10 é o juiz.
2. **A mina no teto.** O melhor ferreiro tira Rara cheia de matéria Rara em 62% das Raras. O freio é a meta 10. Se ela falhar, primeiro os números dos efeitos; em último caso, o teto colado vale 3, não 4.
3. **O dom se mostra mais cedo** (meta 12): com Dom +1 ou +2, de 2 a 8% das obras hoje para 10 a 30%.
4. **Escolher cansa.** Perto de 1 efeito por obra é uma decisão por peça. Para o lote de loja existe o `auto`.
5. **O cheio depende do catálogo.** Sem os efeitos de número, só o devolve enche.
6. **O rival** ainda usa a chance fixa (o risco 6 do juiz da Lei do Valor): tem de rolar a lei, ou as peças dele ficam fora da régua.
7. **O desempate das ferramentas** (categoria, depois número de efeitos) pode não ser o que o jogador quer numa empatada: daí o `usa`, depois.

**As perguntas ao jogador** (o código responde: "F1a.F2a..."):
- **F1. A régua da faixa.** (a) A proporcional (17+ dá 0, 9 a 16 dá 1, 4 a 8 dá 2, 2 ou 3 dá 3, 1 dá 4): efeito em 6 ou 7 obras em 10, de 1,0 a 1,5 efeito por obra (Ferord: 1,0). (b) Ao pé da letra dos números do exemplo (11+ dá 0, 6 a 10 dá 1, 4 ou 5 dá 2): efeito em 4 ou 5 obras em 10, de 0,6 a 1,2 por obra (Ferord: 0,6 a 0,7). **Recomendo (a):** é a forma do exemplo na largura das nossas faixas.
- **F2. No teto.** (a) Passar da CD trancada conta como colada (4). (b) Conta 3. **Recomendo (a):** com (b), tirar mais no dado às vezes dá menos.
- **F3. O teto de efeitos.** (a) Comum 2 · Incomum e Rara 4 · Épica e Única 5 · Lendária e Mítica 6 · Primordial 7. (b) Comum 2 e 4 em todas as outras. **Recomendo (a):** a peça melhor leva mais, como no jogo que ele citou.
- **F4. O 1 do dado.** (a) A peça cai uma categoria e a faixa fica. (b) A peça cai e perde os efeitos da faixa. **Recomendo (a):** o 1 já tira uma categoria.
- **F5. O cheio.** (a) A sobra acima do teto de efeitos enche um efeito com o número da categoria de cima. (b) A sobra se perde. **Recomendo (a):** é o "efeito top" sem quebrar a regra de que a categoria decide.
- **F6. A peça vendida com efeito por escolher.** (a) A loja escolhe sozinha ao comprar. (b) Ferord tem de escolher antes de vender. **Recomendo (a):** menos trabalho de mesa no lote de loja.
- **F7. O dom e a faixa.** (a) O dom escondido se mostra também quando muda o número de efeitos. (b) Só quando muda a categoria (os efeitos saem da soma da mesa). **Recomendo (a):** com (b), a mesa mostraria uma soma que não bate com os efeitos.
- **F8. A tenaz Incomum de Ferord** (quando ela nascer com efeito). (a) Prumo, depois afinada, depois brasa. (b) Afinada primeiro (devolve o +1 na categoria). **Recomendo (a):** o prumo melhora toda peça que vier, e a afinada só soma 1.
- **F9. A próxima ideia da pesquisa, depois desta fase.** (a) O nome ganho e a reforja de linhagem (a peça com história). (b) O banho negro (a aposta depois de pronta). (c) O decalque (copiar efeito, junto das habilidades de copiar). **Recomendo (a):** liga a forja à história do mundo, que é o que o jogo de Belogar tem de seu.

---
*De onde vêm as contas (fora do repositório, no rascunho desta sessão):*
- `/tmp/claude-0/-home-user-ferir/4088f7d7-9a0c-5212-bbb2-a884104a0915/scratchpad/D2/faixa.py`: a regra exata e as tabelas.
- `/tmp/claude-0/-home-user-ferir/4088f7d7-9a0c-5212-bbb2-a884104a0915/scratchpad/D2/prova_cat.py`: a prova de que a categoria não muda.
- `/tmp/claude-0/-home-user-ferir/4088f7d7-9a0c-5212-bbb2-a884104a0915/scratchpad/D2/sorteio.py`: a conferência por sorteio.
- `/tmp/claude-0/-home-user-ferir/4088f7d7-9a0c-5212-bbb2-a884104a0915/scratchpad/D2/teto.py`: o teto e a mina.
- `/tmp/claude-0/-home-user-ferir/4088f7d7-9a0c-5212-bbb2-a884104a0915/scratchpad/D2/catalogo.py`: as ferramentas.
- `/tmp/claude-0/-home-user-ferir/4088f7d7-9a0c-5212-bbb2-a884104a0915/scratchpad/D2/extras.py`: a colada, o 1, o teto da Comum, o dom.
- `/tmp/claude-0/-home-user-ferir/4088f7d7-9a0c-5212-bbb2-a884104a0915/scratchpad/D2/ferord.py`: a soma de Ferord pelo `oficio.valor`, em memória; nada foi gravado no mundo.
