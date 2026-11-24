> **JUNTADO AO `REGRAS.md`** (capítulo 11) na integração da etapa da magia, com os acertos dela (o mau-olhado de −4, os chefes acertados, a loja que não compra peça maldita, o segredo fora do RETOMAR). O que vale é o `REGRAS.md`; este rascunho fica como registro.

# Capítulo 11. A magia na luta (rascunho da frente da luta)

Este capítulo diz como a magia entra na luta: quem lança, a conta, a Mana, o tempo de lançar, o que dá errado, os estados com prazo, a poção bebida na luta, a peça encantada, os nove traços novos e as fases do chefe. Os números moram no `tabelas_magia.py` (os da luta) e no `tabelas.py` (a base comum: os feitiços, o foco, a guarda, a Firmeza, a Mana e a cura). A regra mora no `magia.py`, e o `luta.py` a chama.

**A pessoa comum é a de hoje.** A magia só liga numa luta em que alguém traz feitiço, foco, amuleto, peça encantada, poção, elixir, veneno na lâmina, traço novo, fases ou pena de maldição. A luta sem nada disso é a de sempre, dado por dado (conferido com semente fixa).

## 11.1 Quem lança

Lança quem sabe feitiços: gente, povo (goblin, orc...) ou bicho com o traço **lança**. Cada feitiço é de uma tradição (o mago, `arcano`; o clérigo, `fé`; o druida, `verde`; a bruxa, `pacto`); a luz é de todas.

- **A Conjuração** (o acerto de quem lança) = a mão da tradição do feitiço + o dom nela + metade do bônus do atributo dela (arcano e pacto: Afinidade; fé: Vontade; verde: Percepção) + o bônus do foco. A pena do corpo (fome, sono, cansaço, maldição) entra, como em todo teste.
- **O foco** é a arma de quem lança: varinha e cajado (arcano), cajado (verde), símbolo (fé), talismã (pacto). O cajado vale 1,25, como toda arma de duas mãos. Foco de outra tradição rende uma categoria abaixo. Sem foco, lança-se com as mãos: como foco Comum, com −4. Faltou o atributo que o foco pede: −1 na Conjuração a cada 5 pontos.
- **As mãos do foco.** A varinha, o símbolo e o talismã vão na mão do escudo: lança-se de arma e escudo. O **cajado pede as duas mãos**: ele é a arma (bate como maça leve, 1d6 de impacto, com a mão de maça; apara com o bônus da categoria); a arma de antes fica de reserva e o escudo não entra.
- **O bicho que lança** usa o corpo como foco (a categoria dele) e o instinto como mão.
- **A mão é conselho, não tranca.** Cada grau pede uma mão (grau 1, Iniciante; 2, Treinado; 3, Mestre; 4, Lendário). Abaixo dela o lance é **forçado**: −4 por grau de mão que falta.

## 11.2 A conta (a do aço, linha por linha)

| | O aço | A magia |
| --- | --- | --- |
| quem bate | o acerto | a Conjuração |
| contra | a Defesa | o que **voa** (seta, lança de fogo, raio, castigo, espinho, sangria): a Defesa inteira, como um tiro. A **área** (bola de fogo): a Defesa sem escudo e sem arma. O que **prende, assusta ou amaldiçoa**: a **Firmeza** |
| o tamanho | dado × 4 × valor da arma ÷ proteção da parte | dado × 4 × valor do foco ÷ **guarda** × força do feitiço (1 + 0,03 por ponto de bônus do atributo da tradição) |
| a proteção | a armadura da parte atingida | **a guarda**: o amuleto, ou 0,6 do valor da armadura do tronco, o que for maior (sem nada, um terço). O material e a parte do corpo não contam |
| crítico | dados em dobro, proteção pela metade | dados em dobro, guarda pela metade |

- **A Firmeza** (a Defesa da cabeça) = 22 + metade do bônus de Vontade + metade da maior mão da pessoa + metade do dom de tradição + o melhor entre o bônus do amuleto e metade do bônus da armadura do tronco; mais o **calejo**: cada controle que pega soma 4 até o fim da luta (ninguém fica preso a luta inteira).
- O feitiço que voa sente o tempo, o alto, a cobertura e a gente no caminho, como um tiro. O feitiço que tira um quarto do PV abre ferida, numa parte sorteada; o resto (o sangue, a queda, a moral) é o de sempre.
- **O amuleto gasta:** 1 por luta em que guardou, e 1 a cada feitiço de foco maior que ele. **O foco gasta** 1 por luta em que lançou e 1 a cada retrochoque. A zero, não valem. O desgaste volta ao estado como o das outras peças.
- **A sintonia:** foco e amuleto Épicos ou melhores ocupam lugar, como toda peça alta; **toda peça encantada ocupa lugar, de qualquer categoria**. A que dorme rende uma categoria abaixo, e o encanto dela não sai.

## 11.3 A Mana

- O máximo: (Afinidade + Vontade) ÷ 10 + a mão da tradição + o dom nela. O custo: 2 por grau (o truque, 1; a área, 2 a mais). A luz e a névoa custam 1 por rodada para durar.
- **Na luta, volta 1 no começo de cada turno** de quem lança (de quem sabe feitiço; quem não sabe não ganha Mana na luta).
- **Lançar no osso:** sem Mana, só por ordem do jogador (`osso`): cada ponto que falta custa 5% do PV máximo, e o lance é forçado.
- O que sobrou volta ao estado no fim da luta.

## 11.4 O tempo de lançar e o que dá errado

| Grau | Ações | Observação |
| --- | --- | --- |
| truque e grau 1 | 1 | |
| grau 2 | 2 (o turno inteiro) | |
| grau 3 | 2, e **longo**: sai no começo do turno seguinte | quem canaliza e apanha testa a concentração |

- **Lançar com o inimigo colado** dá a ele um golpe livre. Se o golpe fere, quem lança testa a concentração; falhou, o feitiço se perde (a Mana já foi).
- **A concentração:** 2d20 + bônus de Vontade + mão da tradição contra 28 (32 se o golpe abriu ferida). Quem cai, vai ao chão, fica atordoado ou é agarrado perde o feitiço longo sem teste.
- **O retrochoque:** dois 1 no dado (1 lance em 400); no lance forçado, basta um 1 (1 em 10). Quem lança vai ao chão, perde 1 ação, e o foco perde 1. No forçado, leva ainda o próprio feitiço contra a própria guarda.
- A armadura cobra o fôlego dela na rodada em que se lança, como quando se golpeia. Lançar não gasta fôlego.

## 11.5 Os estados com prazo (lista fechada)

| Estado | O que faz | Quanto dura |
| --- | --- | --- |
| preso (prender, raízes) | não anda, não recua, não troca de lugar; bate e lança | 2 turnos dele |
| guardado (escudo) | +4 na Defesa | 4 turnos dele |
| benzido (bênção) | +2 no acerto, +2 na coragem | até o fim da luta (o brado do chefe: 3 rodadas) |
| mau-olhado | −2 no acerto, na Defesa e na Conjuração | até o fim da luta |
| com seiva | volta 5% do PV por rodada | 5 rodadas |
| com a Mana atada (nó) | a Mana não volta, e cada feitiço custa 1 a mais | 4 turnos dele |
| guardado pela fé (guarda) | conta como tendo amuleto da categoria do foco | 4 turnos dele |
| cego | −4 no golpe, −8 no tiro e no feitiço que voa | o prazo de quem o pôs |
| com fúria (poção) | +2 no acerto e −2 na Defesa, se a arma é até a categoria da poção | 5 rodadas |
| enjoado (poção a mais) | −2 em tudo | até o fim da luta |

- **As penas de magia não somam:** de mau-olhado, veneno e maldição vale a pior. Essa pior soma com a pena do corpo.
- **O campo:** a luz tira o escuro e a névoa põe neblina ou lama, enquanto quem lançou paga 1 de Mana por rodada e está de pé. Valem para os dois lados.
- **O medo e o afugentar:** se o lance pega a Firmeza, o alvo testa a coragem contra 26 (o afugentar, só no bicho que não é chefe). Quem o jogador comanda só fraqueja, e a luta para.

## 11.6 Os feitiços na luta

Os nomes, as tradições, os graus e o custo são os do `tabelas.FEITICOS`. Na luta:

- **arcano:** seta (1d8, a 8 casas) · prender (preso 2 turnos) · escudo (em si ou num aliado a 4 casas) · lança de fogo (2d8; a ferida que abre queima 5 rodadas) · bola de fogo (1d8 em até 4 na casa escolhida, amigo ou inimigo) · raio (2d10, longo; se abre ferida, atordoa 1 ação).
- **fé:** cura (1d8 × 6 × 3 elevado a categoria do foco menos categoria da ferida mais funda; com o teto do dia) · bênção · amparo (estanca o sangue, tira veneno até a categoria do foco, firma quem caiu) · castigo (2d8 em quem é maldito: amaldiçoado, com peça maldita, que amaldiçoa ou imaterial; 1d4 nos outros) · guarda (até 4 na casa de quem lança).
- **verde:** raízes (preso 2 turnos) · espinho (1d6 e veneno: um quarto do golpe por 3 rodadas) · névoa (neblina ou lama) · afugentar · seiva · chamar (longo; só num ermo contado: um bicho do ermo, até a categoria do foco, vem lutar ao lado).
- **pacto:** mau-olhado · medo · sangria (1d6 a 4 casas; quem lança recupera metade do que tirou: não é cura) · nó.
- **Ritos, fora da luta:** quebrar maldição, ler e praga.

## 11.7 Beber na luta e a cura

- **Beber é 1 ação.** Dar de beber a um aliado colado (ou caído ao lado), também. A poção do Comum ao Raro sai da carga; o elixir (do Épico para cima) some.
- **Quantas o corpo aguenta:** Vigor ÷ 30 por dia (no mínimo 1). Cada uma além disso pede 2d20 + bônus de Vigor contra 24 + 4 por poção a mais: falhou, não faz nada, e enjoa.
- A cura (de poção, de feitiço e da seiva) segue a lei ao contrário e **nunca devolve mais que metade do PV máximo no dia**, tudo somado.
- **Quem caiu e recebe cura fica firme** (não morre no chão), mas não se levanta nesta luta.
- Na luta se bebem: cura, antídoto (tira o veneno até a categoria dele), Mana (4, 8, 12, 16), guarda (conta como amuleto da categoria até o fim da luta) e fúria. O veneno de lâmina se passa na arma fora da luta; a vigília e a quebra-maldição se bebem fora dela.
- **O veneno na lâmina:** a primeira vez que a arma tira sangue, a vítima perde por rodada um quarto do golpe, por 3 rodadas, com o −2 no acerto do veneno; numa lâmina acima da dose, um terço disso por degrau. A dose acaba ali.
- **A ferida funda** (a maior categoria que tirou PV desde o PV cheio) é contada em toda luta, com ou sem magia: o sangue e o veneno contam como Comum. É ela que a cura confere.

## 11.8 A peça encantada

O dono solta o feitiço gravado **uma vez por luta**, com as ações do feitiço e sem Mana. A peça vale como foco **um degrau abaixo** da categoria dela. A Conjuração é 2 por grau de quem gravou + metade do bônus de Afinidade do dono + o bônus desse foco. A peça que dorme (sintonia) não solta. O encanto solto volta ao estado (descarregado; carrega de novo fora da luta).

## 11.9 Os nove traços novos

| Traço | Na luta |
| --- | --- |
| resiste | a guarda contra a magia é o corpo inteiro (não 0,6), e a Firmeza leva o bônus inteiro dele |
| imaterial | a arma sem encanto e sem bênção conta uma categoria abaixo; o feitiço e a peça encantada contam inteiros; não vai ao chão nem é agarrado |
| amaldiçoa | a ferida que ele abre põe uma maldição da categoria do corpo, no passo 1 (volta ao estado) |
| lança | lança os feitiços dele pelo instinto, com o corpo de foco |
| sem vida | não sangra, o veneno não pega, não testa a coragem, não cansa, não faz a ação a mais; a zero de PV se desfaz |
| ossos | o corte e a ponta valem metade; o impacto, inteiro |
| dreno | recupera metade do que o golpe do corpo tira (o sopro também é golpe do corpo: drena de cada um que pega) |
| ardente | quem o golpeia de perto leva o fogo de volta (o teto do "devolve" da categoria); a ferida que o corpo abre queima 5 rodadas |
| noturno | o escuro não tira nada do golpe, do tiro nem do feitiço que voa |

## 11.10 As fases do chefe

O chefe pode trazer fases. Ao cruzar o limiar do PV (por exemplo, abaixo de metade), ele muda uma vez por fase: ganha e perde traços, aprende feitiços, recobra Mana, dá o **brado** (os do lado dele ficam benzidos por 3 rodadas) e **ergue** mortos: até N dos mortos mais perto levantam do lado dele, como "sem vida", com metade do PV. O morto erguido é outro lutador, sem registro no mundo; o morto segue morto. A luta para e pergunta.

## 11.11 A luta para e pergunta, e as ordens

**Paradas novas:** o outro lado começa um feitiço longo · quem o jogador comanda fica preso, leva mau-olhado, tem a Mana atada, falha o medo, perde um feitiço, sofre retrochoque, leva uma maldição · a Mana de quem ele comanda cai abaixo de um terço · ele não tem Mana para o feitiço da ordem · o campo muda · o chefe muda de fase · um da casa cai e há cura ao alcance (a frase diz quem).

**Ordens novas, só para quem o jogador comanda** (quem ele comanda não lança, não bebe e não solta encanto sozinho):
- `lancar FEITICO [em ALVO | casa N] [sempre] [osso] [neblina|lama]`: uma vez (depois volta a ordem de antes); com `sempre`, até a Mana acabar, o alvo cair ou vir outra ordem. Fora do alcance, anda até ele.
- `beber POCAO [em ALIADO]`: a poção (`cura`, `cura:1`, `antídoto`...).
- `usar [PECA] [em ALVO | casa N]`: solta o encanto.

A ordem é conferida antes de qualquer dado: o feitiço que a pessoa não sabe, o rito, o alvo do lado errado, a casa para quem não é de área, a poção que ela não leva ou que não se bebe na luta, o encanto que já saiu: tudo é recusado com a frase.

**Os outros** (aliados e inimigos) seguem uma regra curta (`magia.escolhe`): a peça encantada quando vale; a poção de cura abaixo de metade do PV (nunca além do que o corpo aguenta); cura quem está abaixo de metade; protege, benze (só sem ninguém colado) e guarda; prende quem ainda vem chegando; a área só onde há dois inimigos ou mais e nenhum amigo; o resto, o maior dano que a Mana paga. Quem só fere de longe e não tem o que lançar espera a Mana voltar.

**O quadro** ganha, por pessoa, a Mana, o que canaliza e os estados com prazo; e a linha do campo. **A ficha** ganha a linha da magia (a Mana, o que sabe, a Conjuração, a Firmeza, o foco, o amuleto, o encanto), só de quem tem magia.

## 11.12 O que a luta devolve ao estado

Do lutador do mundo: a Mana que sobrou, as poções bebidas e as doses gastas, o elixir bebido, o encanto solto, a dose da lâmina, a maldição posta nele, o dom que decidiu um lance, a ferida funda, as poções e a cura do dia, e o desgaste do foco e do amuleto. Tudo num evento só.

## 11.13 As metas (o banco: `python3 provas.py 600`; só a magia: `python3 provas.py 600 magia`)

Nível 50, tudo Raro, quando não diz outra coisa. 600 lutas por meta no duelo e no grupo, mais onde a faixa é estreita.

| Meta | Faixa | Deu |
| --- | --- | --- |
| M1 mago contra mago | 44 a 56% | 48% |
| M2 mago contra o guerreiro com amuleto: longe, perto, colado | 28 a 45 · 12 a 28 · 4 a 16 | 43, 22, 14 |
| M3 sem amuleto, o mago ganha | 15 a 35 pontos | +24 e +20 |
| M4 o foco uma acima: longe, perto | 85 a 100 · 65 a 90 | 96 e 82 |
| M5 contra o amuleto uma acima · o conjunto uma acima | 2 a 18 · 0 a 8 | 10 e 1 |
| M6 nível 50, foco duas acima, contra nível 500: longe, perto | 65 a 92 · 15 a 40 | 84 e 26 |
| M7 o mesmo com o foco uma acima, de longe | 5 a 30 | 24 |
| M8 nenhum feitiço mata de PV cheio sem crítico entre iguais; mediana até 45% (a seta, 20%) | sim | sim (seta 16%, raio 39%) |
| M9 a Mana seca na rodada · a volta rende a mais | 6 a 10 · 25 a 50% | 8 · +36% |
| M10 o mago no grupo: sem área · com área · contra quem não tem amuleto | 40 a 55 · 52 a 70 · 75 a 92 | 53, 64, 86 |
| M11 o mesmo no corredor | 50 a 68 | 53 |
| M12 o clérigo na linha: campo, corredor; benzendo antes | 42 a 58 · 48 a 64 · 5 a 14 | 45, 53, +13 |
| M13 o druida · a bruxa | 45 a 62 · 42 a 58 | 49 · **37 (falha)** |
| M14 a bruxa sozinha, de longe | 5 a 20 | 8 |
| M15 o longo sob uma flecha · duas | 15 a 35% · 25 a 50% | 33 e 45 |
| M16 com um guarda de escudo na frente | 3 pontos a menos | cerca de 4 (6.000 lutas) |
| M17 o retrochoque: comum, forçado | 0,1 a 0,5% · 8 a 12% | 0,27 e 10,3 |
| M18 o mago contra 8 · 12 soldados | 55 a 85 · 35 a 70 | 77 e 55 |
| M19 a pantera longe, perto; o trasgo | 35 a 60 · 0 a 12 · 30 a 55 | 47, 4, 41 |
| M20 cada traço novo, com e sem | 8 pontos ou mais | todos (de 9 a 76) |
| M21 o controle pega · calejado duas vezes | 55 a 75% · 25 a 40% | 66 e 30 |
| P1 a P4, P9 a poção e o veneno | as do projeto | todas passam |
| E1 a E3 a peça encantada | as do projeto | todas passam |
| e mais: as fases do chefe, a ordem, a pessoa comum, a luta que volta ao estado | sim | sim |

**A bruxa no grupo falha (37%, faixa de 42 a 58).** O projeto a mediu com um cajado que valia inteiro, e o cajado não é foco do pacto: com o talismã (× 1,0, sem aparar), ela fica atrás do valor medido. Testado: o mau-olhado tirando 3 a põe em 43%, raspando a faixa; o alcance da sangria, nada. É decisão do jogador (veja o relatório).

## 11.14 O que mudou do projeto, e por quê

- **O benzido dá +2 na coragem**, não +4: com +4, benzer os quatro antes da luta rendia 15 pontos, acima da meta (5 a 14).
- **Quem caiu e recebe cura não se levanta nesta luta** (fica firme, e a cura conta): o clérigo que levantava os caídos no corredor passava da faixa.
- **O preso do feitiço não troca de lugar** no corredor (o da perna presa segue como hoje).
- **Quem cai, vai ao chão, fica atordoado ou é agarrado perde o feitiço longo sem teste** (a regra do projeto, que o rascunho medido não tinha): a flecha corta mais feitiços do que o rascunho dizia, e as metas M15 e M16 contam a concentração e o corte juntos.
- **A Firmeza leva o melhor entre o amuleto e metade da armadura** (a base comum, `tabelas.firmeza`, leva o amuleto mesmo quando ele é menor: um amuleto Comum baixava a Firmeza de quem veste armadura Rara).
