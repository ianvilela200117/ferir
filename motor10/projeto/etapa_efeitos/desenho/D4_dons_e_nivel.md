rascunho: o DESENHO.md manda (depois da revisão: o par da forja é Força·Vigor e a Lei do Valor não vê a Afinidade da subida; o dom desperto por feito; o fardo de quem o jogador comanda é preço, nunca proibição; a jura para e pergunta; a Fome de Crescer não vale na forja; os feitos primeiros só pela forma e três exemplos)

# D4 — OS DONS E O NÍVEL (Motor 10, parte 2)

Desenho do campo D4: o nível (em duas variantes), o que a subida dá, os três dons pedidos nas duas leituras, os outros dons (de nascença, de feito, os juramentos,
as alcunhas, os vícios de ofício), como eles nascem na gente do mundo, e o banco. **Nada disto está no motor.** Os números são de partida; quem decide é o banco.

**Como se mediu.** Um remendo em memória do `luta.py` (fora do repositório, sem tocar save nenhum) pôs cada dom num gancho e rodou o duelo de iguais do banco:
nível 50 (mão de Mestre), espada, malha e escudo Raros, começando perto. **Duas rodadas de 4.000 lutas por linha (8.000; erro de ±1,1 ponto)**, metade com o dom
de cada lado. A fuga rodou 4.000 lutas por linha (±1,6). O ritmo do nível saiu de 300 carreiras simuladas de Ferord. Três mundos de rascunho (o `gera.py` em pasta
de rascunho, sementes 101 a 103) deram a gente gerada: uns 200 nomeados, mediana 17 a 18, quartis 10 e 28, máximo 170 a 190 (o mundo de verdade: 19, 10, 28 e 165).
Nas tabelas: **(m)** medido · **(c)** conta · **(d)** desenho, sem vitória a medir · **(p)** veio da `PESQUISA.md`. "+9,1" quer dizer: quem tem o dom vence 59,1%.

---

## 1. O que o jogador pediu e o que esta parte entrega

> **Dia 24:** "além do item, efeitos, habilidades e magias devem ser muito determinantes [...] deve existir a possibilidade desde a apelação até o normal e fraco."
>
> **Dia 34:** "em SATISFY, eles usam habilidades de classe para batalhar entre outras coisas, convencer, trabalhar e copiar."
>
> **Dia 35:** "Mesma coisa com habilidades, dons, talentos [...] dons: a pessoa tem um dom que toda vez que ela sobe de nível, ela ganha 2 atributos. Toda vez que ela
> usa uma skill de dano, ela ganha 20% a mais de dano [...] Toda vez que ela foge, ela consegue ir mais tanto [...] que eu posso montar uma build boa, entendeu?"

**O que entrega:**
1. **O nível, em duas variantes** (2.2 e 2.3): **A**, o nível sobe com a experiência de verdade (luta pela força do inimigo, obra pela categoria, grau novo, feito,
   viagem, ensino, missão), com a régua calibrada no mundo e o ritmo medido; **B**, a subida é o grau novo e o degrau de classe, e o nível fica como está.
   **Recomendo A.**
2. **O que a subida dá** (2.4): 1 ponto por nível (A) ou 2 por subida (B), no **par de atributos do caminho do feito**, com a regra da metade e o teto 100.
   O que nunca muda: o item decide (medido).
3. **Os três dons pedidos, nas duas leituras** (2.5), cada um medido, com o fardo e a recomendação: o SANGUE LARGO (os atributos a cada subida), a MÃO PESADA
   (o dano das técnicas: o fixo, ou o PESO DA MÃO, que acumula a cada uso) e o PÉ LIGEIRO (a fuga mais longe: o fixo, ou o pé que cresce a cada fuga).
4. **Mais 32 dons** (2.6 a 2.8): 11 raros de nascença, 11 de feito (o feito torto) e 4 sem par, 6 juramentos; mais as **alcunhas** (2.9) e **17 vícios de ofício** (2.10).
5. **O que o personagem do jogador pode ter e como descobre** (2.11), e **como nasce na gente do mundo** (2.12).
6. **O banco** (seção 5): nenhum dom de nascença passa de um grau de maestria; os de feito, de dois; o ritmo da variante A.

### O que a medida mostrou antes de tudo (os achados que mudam o desenho)
1. **O nível pesa pouco, e de propósito.** Do nível 5 ao 40 (35 pontos pelo molde) vale de +10,8 a +12,9 (m, duas montagens), perto de um grau de maestria;
   100 níveis valem +30,2 (m). O nível 40 contra o nível 5 de arma uma categoria acima vence só 11,6% (m).
2. **Quem escolhe onde põe muda o tamanho do nível.** No mesmo 40 contra 5, os pontos pelo molde dão +10,8; metade na Força e metade no Vigor, +16,9; **tudo no Vigor,
   +24,7** (m). O Vigor dá 2 de PV por ponto. Daí o par do caminho, a metade e o teto (2.4).
3. **O Sangue Largo ao pé da letra precisa de teto.** No nível 50, um ponto a mais por nível (+50) dá +15,9 pelo molde e +28,4 tudo no Vigor (m); com teto de +20,
   fica entre +4,2 e +8,0 em todos os níveis medidos (m).
4. **O fardo da pesquisa mata a Mão Pesada.** Com +1 de fôlego por técnica, o dom vai de +7,9 a −6,7 e −12,1 (m): o fôlego é o recurso mais escasso da luta.
5. **O que acumula rende pouco no duelo curto e muito na luta longa.** O duelo de iguais acaba na 4ª rodada. O Peso da Mão dá +9,1 no duelo e leva a luta contra um chefe
   de PV dobrado de 11,5% para 20,7% de vitória (o Gume de +20% em todo golpe: 18,2%) (m).
6. **O pé que foge não ganha luta: salva a vida.** Quem recua quando a luta vira cai ou morre em 40,9% das lutas; com o Pé Ligeiro, em 24,3%. A vitória não muda
   (26,5% e 26,8%) (m).
7. **A jura da pesquisa não paga.** A Mão Certa de 1 a 4 dá +1,5 (m): o crítico que ela tira vale o que a janela dá. De 1 a 5, +6,0 (m).

---

## 2. As regras, para a mesa

### 2.1 A régua de tudo: um grau de maestria
O 10.7 mediu o Grande Dom contra o gêmeo e disse: **vale um grau de maestria**. É a régua deste desenho.

| O que se mediu (nível 50, tudo Raro, perto) | Vence | Pontos | Leitura |
| --- | --- | --- | --- |
| gêmeos | 50,1% | 0 | |
| Dom +1 | 57,2% | +7,2 | |
| **Grande Dom +2** (+2 no acerto, +1 na Defesa) | **60,9%** | **+10,9** | **um grau**: o teto do dom de nascença e da jura |
| dom +4 (+4 no acerto, +2 na Defesa) | 69,5% | +19,5 | **dois graus**: o teto do dom de feito |
| Mestre contra Treinado (o grau de verdade, com o esforço barato) | 65,3% | +15,3 | o grau inteiro vale mais que o Grande Dom |

- **Dom de nascença e jura:** até o Grande Dom no mesmo cenário (no mesmo nível e categoria), com 1,6 de folga. **Dom de feito:** até o dom +4 (cerca de +20).
- A régua foi medida também nos níveis 10, 20 (tudo Incomum) e 150 (tudo Lendário): o Grande Dom dá 59,4%, 60,1% e 61,8% (m). Todo dom de luta deste desenho fica
  abaixo dele ou empata, nos quatro (seção 5, DN1).

### 2.2 O nível, variante A: a experiência pelos feitos
**A régua.** Todo feito tem um NÍVEL. A experiência que ele dá depende do nível do feito contra o nível de quem fez:

| O feito tem nível... | Experiência |
| --- | --- |
| o dobro do seu ou mais | 40 |
| acima do seu (até o dobro) | 20 |
| de 2/3 do seu até o seu | 10 |
| abaixo de 2/3 do seu | 0 |

**100 de experiência = 1 nível** (o que passa fica para o próximo). No máximo **100 por evento** e **100 por dia**: nunca mais de um nível de uma vez.
Não há tabela que cresce: todo nível pede os mesmos 100. O que fica difícil, subindo, é achar feito à altura (a régua acima); é ela que segura o ritmo e o mundo.

**O nível do feito:**

| O feito | Nível do feito |
| --- | --- |
| a obra (forja, couro, encanto, alquimia), pela categoria que SAIU | Comum 5 · Incomum 10 · Rara 20 · Épica 40 · Única 80 · Lendária 160. A primeira de cada categoria, da Rara para cima, conta o dobro |
| o inimigo vencido (caiu, morreu, fugiu ou se rendeu), para cada um que o feriu | o nível dele, **dobrado a cada categoria que o conjunto dele passa o seu** (pela metade a cada uma abaixo). O conjunto: a maior categoria entre a arma e a armadura do tronco; no bicho, a do corpo |
| o grau novo, em qualquer dos 17 caminhos | Iniciante 10 · Treinado 25 · Mestre 50 · Lendário 150 (os degraus da `maestria_tipica`) |
| o aprendiz que firma um grau com o seu ensino | o nível do grau dele (a mesma tabela) |
| a missão cumprida | 10, dobrado a cada categoria do alvo (Comum 10, Incomum 20, Rara 40...) |
| o feito do cânone (o Mestre o escreve num evento) | pequeno 10 · do lugar 25 · da região 50 · do reino 100 · de lenda 200 |
| a primeira chegada a um lugar de povo; a primeira descida a uma masmorra | **10 fixos**, fora da régua (16 lugares e 8 masmorras no mapa) |

- **Não dão experiência:** o conserto, o ajuste, o jornal, a venda, o treino (eles dão maestria, que é outra escada), a luta perdida sem ninguém vencido, o bicho que só
  se colhe. O feito que já não ensina (abaixo de 2/3) não dá nada: forjar Comum para de dar no nível 8, Incomum no 16, Rara no 31.
- **Por que assim (c).** Quem vive de feitos de nível D sobe até perto de **1,5 × D** e para: ali o feito cai abaixo de 2/3. É o "o mestre só cresce contra coisa
  à altura" da pesquisa (p, lição 9), e é o que faz o mundo gerado fazer sentido sem mexer nele:

| Quem | O feito do dia a dia | Sobe até perto de | O mundo gerado (mediana e de–a; nos rivais, a faixa) |
| --- | --- | --- | --- |
| aprendiz | a obra Comum (5) | 7 | 6 (3–8) |
| ferreiro de vila | a Incomum e a Rara (10–20) | 15–30 | 27 (18–40) |
| guarda | o salteador (6–30), de peça igual | 9–45 | 17,5 (10–34) |
| caçador | a corça e o javali (4–10), o lobo às vezes (20) | 6–30 | 18 (14–29) |
| capitão, senhor | o veterano, o dono da frente (25–45) | 38–68 | 41 (31–66) |
| veterano | o bicho de grau C (40–60), de peça igual | 60–90 | 50–100 |
| Lenda | o grau B e A (90–150), de peça igual | 135–225 | 120–200 |

**O ritmo (m, 300 carreiras desde o Dia 35, nível 5).** A forja segue a escada do 10.8 (talento Comum: a 1ª Rara ~17, Épica 51, Única 131, Lendária 356); a obra sai
inteira em 70%, uma abaixo em 25%, perdida em 5%; ele veste o que forja (Incomum até o Dia 70, Rara até 160, Épica até 380, Única depois) e só luta com quem a peça
dele vence (inimigos do motor: bichos, criaturas, salteadores); os graus novos vêm nos dias da escada.

| Perfil | Nível 10 | 15 | 20 | 30 | 40 | No Dia 935 |
| --- | --- | --- | --- | --- | --- | --- |
| **o ferreiro** (forja 3 dias em 4; uma luta a cada 10 dias) | Dia 62 (58–67) | 113 | **188** (168–208) | 430 (378–480) | depois do Dia 935 | nível 39 |
| **o ferreiro que caça** (meio a meio; uma luta a cada 3 dias) | Dia 55 (51–59) | 82 | **115** (108–125) | 216 (200–237) | **359** (331–386) | nível 55 |
| o aventureiro (forja 1 dia em 4; luta 3 dias em 5, atrás do que está à altura) | Dia 47 | 62 | 78 | 114 | 164 (159–170) | nível 145 |

Num jogo normal (o ferreiro que às vezes caça e viaja), **Ferord chega ao 10 perto do Dia 60, ao 20 entre os Dias 115 e 190, e ao 40 perto do Dia 360 se sair para o
mundo** (o ferreiro que não sai fica nos 30). Um ano depois ele é um "oficial" (15 a 40), como o ferreiro de cidade.

**A gente do mundo também sobe, pela mesma régua, só em evento:**
- quem luta numa luta que volta ao estado (o guarda que lutou ao lado, o salteador que derrubou alguém) ganha o que a régua dá, no mesmo evento "luta";
- **os rivais**: o plano cumprido (a masmorra limpa, o chefe morto, a missão) é um feito do nível do alvo, para cada um do grupo; com isso, o novato vira oficial
  e a notícia conta;
- ninguém mais sobe sozinho: a vida de quem não entra em cena não se conta. Os pontos do NPC vão pelo molde, no mesmo evento.

**Na entrada da regra:** todos começam com experiência 0 no nível que têm. O que Ferord já fez não conta para trás.

### 2.3 O nível, variante B: o grau novo
- **A subida** é cada grau novo de maestria (Iniciante, Treinado, Mestre, Lendário) em qualquer dos 17 caminhos, e cada degrau de classe (do desenho das classes).
  O nível de 1.2 fica como está (só evento do Mestre). Não se cria nível escondido (p, 3.5).
- **Cada subida dá 2 pontos** de atributo, no par do caminho (2.4): um em cada, ou os dois num.
- **O ritmo (c):** Ferord, ferreiro, num ano: comércio Iniciante (~Dia 100), forja Mestre (~120), encanto Iniciante (~150), martelo Treinado (~275), forja Lendário
  (~360): 4 a 5 subidas, +8 a +10 pontos. Se caça e anda, 7 a 8 subidas (+14 a +16). Na variante A, no mesmo ano: +23 (o ferreiro) e +37 (o que caça).
- **A gente do mundo** não sobe (a maestria dela nasce pronta).

| | A (experiência) | B (o grau novo) |
| --- | --- | --- |
| o que o jogador lê | "nível 7 · 60/100" e "subiu de nível" | o nível parado no 5; "subiu" a cada grau |
| o que conta | luta, obra, grau, feito, viagem, ensino, missão | só o grau e a classe |
| subidas por ano (Ferord) | 23 a 37 níveis | 4 a 8 subidas |
| pontos por ano | +23 a +37 | +8 a +16 |
| o que pede ao motor | dois campos, uma régua, o gancho nos eventos que dão feito | o gancho no grau novo |
| o mundo | os rivais e quem luta sobem | ninguém muda |

**Recomendo A.** É a língua do pedido ("toda vez que ela sobe de nível"); o número da ficha ganha vida; a luta, a viagem e o feito passam a contar, não só a forja;
e A contém B, porque o grau novo é um feito. O custo é pequeno: o script faz a conta no evento que já existe.

### 2.4 O que a subida dá (nas duas) e o que nunca muda
- **Os pontos:** 1 por nível (A, como hoje no 1.2) ou 2 por subida (B). O quarto de PV por nível fica (A).
- **Onde: o par do caminho.** O ponto vai para um dos dois atributos do caminho do feito que fechou o nível (em B, do caminho do grau). **O jogador escolhe entre os
  dois** (vira pergunta na MESA); o NPC põe pelo molde.

| Caminho do feito | O par | Caminho do feito | O par |
| --- | --- | --- | --- |
| fio | Agilidade · Força | cura | Afinidade · Vontade |
| haste | Força · Vigor | alquimia | Afinidade · Percepção |
| peso | Força · Vigor | encanto | Afinidade · Vontade |
| tiro | Agilidade · Percepção | manha | Agilidade · Percepção |
| forja | Força · Afinidade | arcano | Afinidade · Vontade |
| couro | Agilidade · Afinidade | fé | Vontade · Vigor |
| caça | Percepção · Agilidade | verde | Vigor · Percepção |
| coleta | Percepção · Vigor | pacto | Vontade · Afinidade |
| comércio | Vontade · Percepção | a estrada (lugar novo, masmorra nova) | Vigor · Percepção |
| a missão, o feito do cânone | qualquer um | a luta | o caminho da arma usada (sem arma: Força · Vigor) |

- **A metade:** nenhum atributo recebe mais da metade dos pontos de subida já postos (os dois primeiros são livres). **O teto:** a subida não leva atributo acima
  de 100; o ponto que não cabe vai ao outro do par, e se nenhum cabe, a qualquer um abaixo de 100.
- **Por que o teto 100:** o melhor ferreiro possível do banco tem Afinidade 100 (T9); acima disso a Lendária dele subiria de 1 em 4. Com o teto, não sobe (c).
  Ferord (Afinidade 75) pode chegar a 100 pela forja: +3 no total da obra, em anos.

| Quem escolhe onde põe (o 40 contra o 5 de partida, mão de Treinado, tudo Raro) | Vence (m) |
| --- | --- |
| pelo molde (o de hoje) | 60,8% |
| o ferreiro: Força 18 e Afinidade 17 | 56,5% |
| metade no Vigor, metade na Força (o pior que o par e a metade deixam) | 66,9% |
| um terço no Vigor, na Força e na Agilidade | 66,6% |
| tudo no Vigor (**proibido** pela metade) | 74,7% |

**O que nunca muda: o item decide** (m). O nível 40 (metade Força, metade Vigor) contra o nível 5 de arma uma categoria acima vence 11,6%; com o Sangue Largo cheio,
12,9%; o nível 80, 18,8%. A categoria inteira vale +45 (D1); 35 níveis valem perto de um grau de maestria. O nível segue sem somar no acerto, no dano e nas ações.

### 2.5 Os três dons pedidos, nas duas leituras
São dons raros de nascença (2.6), cada um com o fardo e o momento em que se mostra.

**SANGUE LARGO** ("toda vez que ela sobe de nível, ela ganha 2 atributos")

| Leitura | A regra | Medido |
| --- | --- | --- |
| fixa | quando se mostra, +10 pontos de uma vez, no par do caminho que o mostrou | +5,5 no nível 40, +4,4 no 20 (metade Força, metade Vigor) |
| **toda vez que** | **cada subida dá o dobro: 2 pontos por nível (A), 4 por subida (B), até +20 a mais na vida**, pelas regras de 2.4 | **+20, metade Força e Vigor: nível 10 +7,9 · nível 20 +6,8 a +8,0 · nível 40 +8,0 · nível 150 +6,2**; pelo molde, nível 50: +4,2. Sem o teto (+50 no nível 50): +15,9 pelo molde, +28,4 no Vigor |

- **O fardo:** o corpo grande come. A fome sobe 1 a cada bloco, não a cada 2.
- **Mostra-se** na primeira subida depois de rolado: "o corpo cresce mais que o dos outros: 2 pontos".
- **Recomendo a toda vez que:** é o que ele pediu, cresce com o personagem, e o teto o deixa abaixo do Grande Dom em todo nível medido. Na gente do mundo, quem nasce
  com ele ganha os pontos a mais do nível que já tem, até +20.

**MÃO PESADA** ("toda vez que ela usa uma skill de dano, ela ganha 20% a mais de dano")

| Leitura | A regra | Medido |
| --- | --- | --- |
| fixa | +20% no dano das técnicas de dano (o grupo DOM da pilha do D1) | +7,9 se todo golpe é técnica (o teto; +9,4 no nível 10), +2,8 com uma técnica por turno; na luta longa, de 11,5% para 14,5% (18,5% se todo golpe é técnica) |
| **toda vez que: o PESO DA MÃO** | **cada técnica de dano que acerta põe 1 peso na mão, até 3. Cada peso: +20% no dano de TODO golpe dele. Um turno inteiro sem golpear tira todos** | **+9,1 no duelo** (níveis 10, 20, 150: +8,2, +7,5, +9,5); **na luta longa, de 11,5% para 20,7%** |

- **O que se mediu antes:** o que soma a cada técnica e vale só na técnica (de +5% a +20% por uso, zerando no erro) rende pouco: de −0,3 a +5,5 (m). O fardo da pesquisa (+1 de fôlego por
  técnica) leva a fixa a −6,7 e −12,1 (m); o "a técnica que erra abre a guarda" (−2 na Defesa), a −1,5 e +1,6 (m).
- **O fardo:** na fixa, o braço pesado come o aço (a arma dele perde 1 de durabilidade a mais por luta). No Peso, **no fim da luta, +1 de cansaço por peso que havia**.
- **Mostra-se** no primeiro peso: a MESA passa a mostrar "a mão pesa: 1".
- **Antes das técnicas existirem** (o desenho das habilidades), o esforço (a ação a mais) conta como técnica de dano.
- **Recomendo o Peso da Mão.** É a leitura ao pé da letra, tem contador à vista e decisão (seguir batendo para não perder o peso), e é o dom do chefe: a luta longa.
  **Pede ao D1** o grupo DOM até +60% com o Peso cheio (os outros dons de dano, +20%); a pilha inteira vai a ×6,7, ainda abaixo das duas categorias (×9). Medido com
  o Peso: a Rara com o Grande Dom, o Peso e o Sangue Largo cheio contra a Épica sem nada vence 11,4% (a meta T7 é até 15%).

**PÉ LIGEIRO** ("toda vez que ela foge, ela consegue ir mais tanto")

| Leitura | A regra |
| --- | --- |
| fixa | no recuo e na fuga, **3 casas por ação, não 2**, no turno em que não golpeia nem atira; o golpe livre do recuo contra ele tem −4; no teste de fuga da estrada e da caça, +4 |
| **toda vez que: o pé que cresce** | **as fugas que contam fazem o pé**: de 0 a 2, +1 casa e +2 no teste · de 3 a 9, e o golpe livre contra ele −4, +4 no teste · de 10 a 24, **+2 casas**, +6 no teste · 25 ou mais, +8 no teste, e na estrada salteador a pé não o alcança |

| O que se mediu (nível 50, tudo Raro; 4.000 lutas) | Sai da luta | Separam | Cai | Morre |
| --- | --- | --- | --- | --- |
| recua desde o começo, perto, sem o dom | 51,0% | 27,8% | 17,2% | 4,1% |
| o mesmo, com +1 casa e o −4 | 91,8% | 4,2% | 3,7% | 0,4% |
| o mesmo, com +2 casas e o −4 | 98,0% | 0,8% | 1,2% | 0,2% |
| luta colado e recua abaixo da metade do PV, sem o dom | 6,7% | 26,0% | 31,3% | 9,6% |
| o mesmo, com +1 casa e o −4 | 44,3% | 4,8% | 18,3% | 6,0% |
| o mesmo, com +2 casas e o −4 | 47,3% | 4,8% | 15,4% | 6,5% |

- A vitória não muda (26,5%, 26,8%, 26,1%); o −2 de coragem do fardo também não pesa no duelo (49,9%). O −4 no golpe livre soma pouco: o que salva é a casa a mais.
- **O pé não vale no turno em que golpeia ou atira:** é para sair, não para lutar andando. Se valesse, o arqueiro que recua e atira iria de 10,6% para 13,4% (m).
- **A fuga que conta:** sair da luta (3.15) ou fugir pela moral de uma luta em que corria perigo (o inimigo de nível do feito de 2/3 do dele para cima, ou ele abaixo
  de metade do PV), ou passar no teste de fuga da estrada ou da caça. **Uma por dia.**
- **O fardo:** −2 na coragem (o pé quer ir antes da cabeça). No que cresce, da 3ª fuga vista em diante nasce a alcunha ruim "Pé-de-Vento" (2.9).
- **Mostra-se** no primeiro recuo: "recua 3 casas".
- **Recomendo o pé que cresce:** é o "dom que cresce a cada uso" do pedido, premia um jeito de jogar e conta história (o medroso que vira impossível de pegar).
  O teto (+2 casas) para onde a medida mostra que já não há o que ganhar.

### 2.6 Os dons raros de nascença (os 3 pedidos e mais 11)
A pessoa tem no máximo um. Cada um tem um fardo que se sente em cena e se mostra quando decide (como o dom de hoje, 10.6). Os de luta, medidos contra o Grande Dom
(+10,9): todos abaixo.

| Dom | O que faz | O fardo | Mostra-se quando | Medido |
| --- | --- | --- | --- | --- |
| SANGUE LARGO | 2.5 | a fome em dobro | a 1ª subida | +4,2 a +8,0 |
| MÃO PESADA | 2.5 (o Peso da Mão) | +1 de cansaço por peso no fim | o 1º peso | +9,1 |
| PÉ LIGEIRO | 2.5 (o pé que cresce) | −2 na coragem | o 1º recuo | a queda de 40,9% para 24,3% |
| COURO DE BIGORNA (p) | a armadura protege um décimo a mais; a pele conta como couro Comum onde não há peça | a subida nunca põe ponto em Força nem em Agilidade | o golpe que, sem ele, abria ferida | +5,4 (m) |
| OSSO DURO | a primeira ferida grave de cada dia vira leve | a ferida dele sara com um dia de repouso a mais | a 1ª grave que vira leve | +1,5 (m) |
| PEITO DE CARVALHO | +4 na coragem | nunca se rende: quebra fugindo; nem o jogador pode mandá-lo render-se | o teste de coragem que só passou por ele | +1,1 no duelo (m); no grupo, mais |
| SONO DE LEBRE | nunca é surpreendido (a luta, a estrada, o bicho que viu primeiro) | a cama tira 2 de sono por bloco, não 3 | a 1ª surpresa que não pegou | a surpresa vale 3,5 (m) |
| OLHO DE GATO | no escuro, o golpe dele perde só a metade (como o povo que vê no escuro, 19.14); no tiro, inteiro | no calor, −1 no tiro | o golpe no escuro que só acertou por ele | o do povo (m, 19.14) |
| FÔLEGO DE MULA | +2 de fôlego máximo | a fome sobe 1 a mais por dia | o fôlego acima do de sempre gasto | +2,8 (m, o Fole do D1) |
| SANGUE QUENTE | abaixo de metade do PV, +3 no acerto | abaixo de um quarto, não recua nem guarda | o golpe que só acertou por ele | +4,5 (m) |
| VOZ DE COMANDO | os aliados a 3 casas: +2 na coragem | quem pode escolher alvo escolhe ele primeiro | o teste de um aliado que só passou por ela | (d; o 3 contra 3) |
| OLHO DE LIGA (p) | lê a categoria, os efeitos e o dono de uma peça só de olhar | a cara o entrega: a loja paga 2,5 pontos a menos e cobra 2,5 a mais | o 1º olhar | (d) |
| MÃO DE OURIVES | na forja e no couro, **prumo +2** (só nos efeitos, como o prumo do D2; soma com o da ferramenta) | o trabalho grosso a cansa: o conserto e o jornal contam metade dos blocos para a maestria | a obra que, sem ele, saía com menos efeitos | +0,28 efeito por obra (c, D2) |
| FOME DE CRESCER (p) | enquanto persegue um desejo declarado (uma frase e um caminho, na ficha), os blocos desse caminho rendem como um degrau de talento acima, **nunca além do Prodígio** | cumprido ou trocado o desejo, o dom apaga para sempre | o grau que firma antes do tempo | (c: a linha do 10.8 de cima) |

- **A forja e a Lendária.** Nenhum dom toca a categoria da obra: a Mão de Ourives soma só na faixa (os efeitos), e a Fome de Crescer muda a linha da pessoa no 10.8,
  não a tabela (ninguém passa do Prodígio). A chance da Lendária do melhor ferreiro segue 1 em 4.

### 2.7 Os dons de feito (o feito torto)
- **Quem faz primeiro no mundo ganha o dom, e ninguém mais.** Ninguém nasce com eles. O mundo confere o feito depois de cada evento (do personagem e dos rivais).
- **A semente escolhe 7 dos 11 que valem neste mundo**, e a crônica fecha 1 ou 2 deles (o morto da história que o fez primeiro): quem lê este desenho não sabe quais
  estão abertos. O boato conta os que alguém ganhou.
- No máximo **dois por pessoa**: o terceiro feito dá a experiência e a alcunha, não o dom. Os que se usam têm a **lei do cansaço** (os usos do dia, na ficha).
- Teto: dois graus de maestria (o dom +4, +19,5).

| O feito (o primeiro do mundo a...) | O dom | Usos | Medido |
| --- | --- | --- | --- |
| matar sozinho um bicho de grau C ou maior com uma arma que ele mesmo forjou | A MÃO QUE FEZ: +2 no acerto com as armas da própria forja | sempre | +7,8 (m) |
| sobreviver a uma luta contra quem tinha o conjunto duas categorias acima | O QUE O FERRO NÃO MATOU: o golpe que o derrubaria o deixa com 1 PV | 1 por dia | +5,6 (m, o Imortal do D1) |
| fazer render um bando inteiro (3 ou mais) sem matar nenhum | VOZ QUE DOBRA: com 1 ação, todo inimigo a 3 casas testa a coragem contra 24 | 1 por luta, 2 por dia | +7,4 (m, o Temível 24 do D1) |
| firmar três que rolavam a morte, no mesmo dia | MÃOS QUE PUXAM: com 1 ação, quem caiu colado fica estável e para de sangrar | 1 por dia | (d) |
| andar as 24 estradas do mapa | PÉ DE ESTRADA: cada trecho de estrada leva 1 bloco a menos (no mínimo 1); o bando da estrada não o surpreende | sempre | (d) |
| vencer de mãos nuas quem empunhava arma Rara ou melhor | PUNHO DE MALHO: as mãos batem como maça da categoria da melhor peça que veste, até Rara | sempre | (d; é a maça) |
| vender numa loja, por 1.000 de prata ou mais, uma peça que ele forjou | NOME DE PRAÇA: a loja paga 5 pontos a mais pelas peças dele (até 60%) | sempre | (c: o Grande Dom do comércio) |
| forjar uma peça com o núcleo de um bicho que ele mesmo matou | LAÇO DE NÚCLEO: a peça com núcleo da própria caça nasce com +1 efeito (no teto; a sobra enche) | sempre | (c, D2) |
| forjar uma peça com 4 efeitos ou mais | O FOGO GUARDADO: numa obra, prumo +5 | 1 obra por dia | +0,72 efeito naquela obra (c, D2) |
| descer ao último nível de uma masmorra e voltar sozinho | O QUE VOLTOU DO FUNDO: na masmorra, o escuro não pesa no golpe (no tiro, metade); +4 para achar armadilha | sempre | (d) |
| ferir um dragão e viver | LAMBIDO DO FOGO: o fogo (o sopro, a brasa, o feitiço) tira dele um terço a menos | sempre | (d; o banco mede contra o sopro) |

**O DOM SEM PAR (p):** quatro dons presos a uma MEDIDA do mundo. O dono é quem lidera a medida; a cada estação, se outro passou à frente, uma rolagem oculta (metade)
passa o dom. O personagem sabe por boato ("dizem que o mais temido do reino agora é...").

| Medida | O dom de quem lidera |
| --- | --- |
| A MÃO DO REINO: mais peças Raras ou melhores forjadas | prumo +1 em toda obra; a loja paga 2,5 pontos a mais pelas peças dele |
| O COURO MAIS CORTADO: mais feridas graves vividas | a primeira ferida grave de cada luta vira leve |
| O PÉ MAIS ANDADO: mais estradas andadas | nunca é surpreendido na estrada |
| O MAIS TEMIDO: mais inimigos vencidos de nível acima do seu | quem começa a luta contra ele testa a coragem contra 22 |

### 2.8 Os juramentos (trocar uma regra por um preço absoluto)
- Escolhidos, não sorteados. **Um por pessoa.** Jura-se em cena, diante de um santuário ou de uma testemunha com nome (evento "jura").
- **Quebrar:** o ganho acaba, quem viu lembra (−2), e aquela jura não se faz de novo. **Desfazer por vontade:** um ano de vida ou um núcleo Épico ou melhor (p).
- O preço é absoluto: o script recusa a ordem que a jura não deixa ("a jura não deixa recuar").
- Teto: um grau (o Grande Dom).

| Jura | O que dá | O preço | Medido |
| --- | --- | --- | --- |
| DA MÃO CERTA (p) | o golpe e o tiro que erram por 1 a **5** acertam | na luta, o dado dele nunca explode e nunca dá crítico | +6,0 (m); de 1 a 4, +1,5; de 1 a 6, +10,4 |
| DO CORPO DE PEDRA (p) | não sangra, não se envenena, a perna ferida não o derruba, a ferida do tronco não lhe tira fôlego | nunca recua, nunca foge, nunca se rende | +4,6 (m); com o passo curto da pesquisa, +0,5 (por isso saiu) |
| DO SANGUE NO FEITIÇO (p) | o feitiço custa uma ferida leve no braço em vez da Mana e sai um grau acima no efeito | a Mana dele não volta mais sozinha (só a poção e o rito) | (d; o banco mede no mago contra mago) |
| DO NOME CALADO | o nome dele não anda: nenhum feito dele vira notícia, nenhuma peça leva o sinete, a cobiça pela peça alta não o acha | nunca tem alcunha nem fama, não entra no ranking nem no torneio; a loja paga a ele como a um estranho | (d) |
| DO FERRO DADO | na forja e no couro, prumo +4 (só nos efeitos) | nunca vende nem troca o que forja: dá, ou guarda | +0,57 efeito por obra (c, D2) |
| DO ÚLTIMO DE PÉ | com um aliado caído na luta, +2 no acerto e não testa a coragem | não recua nem foge enquanto houver um caído vivo do seu lado | (d; o 3 contra 3) |

### 2.9 As alcunhas (os títulos que andam com a notícia)
- **Nascem de um feito público** que vira notícia com o nome da pessoa: a obra Única ou maior (a janela do mundo), a primeira limpeza de uma masmorra, o dono de uma
  frente morto, o torneio vencido, o dom de feito ganho. **As ruins também:** o furto visto, a 3ª fuga vista (o Pé Ligeiro), a morte de alguém da guarda, a jura quebrada.
- **O nome sai do feito** pelo script, num molde de frase ("o da Lâmina do Conde", "Mata-Hidra", "o Pé-de-Vento"). O jogador pode recusar uma alcunha boa; a ruim, não.
- **Anda com a notícia (22.3):** quem tem nome, onde a notícia chegou, ganha a memória "ouviu falar" (+2; onde chegou como boato, +1; a ruim, −2 e −1). A alcunha de
  ofício (forja, couro, comércio) faz a loja de onde a notícia chegou pagar 2,5 pontos a mais pelas peças dele.
- **No máximo 3.** A quarta boa tira a boa mais velha; a ruim só sai com um feito bom no mesmo lugar ou depois de um ano. Não há conta nova: a alcunha vira memória.

### 2.10 Os vícios de ofício (as passivas pequenas do Treinado)
Cada caminho no Treinado deixa um vício, que vale em qualquer classe. **Três vagas; +1 no primeiro Mestre.** Trocar leva um dia na oficina do caminho. Os de luta
somam pouco: três juntos, até +5 (c; o banco confere).

| Caminho | Vício | O que faz |
| --- | --- | --- |
| fio | o corte limpo | a ferida que ele abre sangra 1 rodada a mais |
| haste | o cabo comprido | +2 no golpe livre de "o alcance bate primeiro" |
| peso | o pé plantado | +2 contra ir ao chão (o derruba, a matilha, o bote, a investida) |
| tiro | o olho que mede o vento | a chuva e o vento tiram 1 a menos no tiro |
| forja | o olho do fogo | lê a categoria e a durabilidade de toda peça de metal à vista; o conserto rende 2 pontos a mais por bloco |
| couro | a costura dupla | a armadura de couro que ele veste perde 1 de durabilidade a menos por luta |
| caça | o rastro fresco | +1 no rastro |
| coleta | a mão que acha | +1 na coleta |
| comércio | a primeira venda | +1 ponto no que a loja paga, na primeira venda do dia |
| cura | a atadura firme | a atadura corta 1 filete a mais |
| alquimia | a dose certa | a poção que ele faz cura +1 por dose |
| encanto | a runa paciente | o encanto que falha tira 5 de durabilidade a menos |
| manha | o pé de gato | +1 para andar escondido |
| arcano | a reserva | +1 de Mana máxima |
| fé | a reza curta | o primeiro feitiço da fé de cada luta custa 1 de Mana a menos |
| verde | o cheiro do mato | no ermo do laço, o bicho não o surpreende |
| pacto | a praga comprida | o mau-olhado dele dura 1 rodada a mais |

### 2.11 O que o personagem do jogador pode ter, e como descobre

| Tipo | Pode ter? | Como descobre |
| --- | --- | --- |
| dom raro de nascença | **qualquer um dos 14**, se a semente der (2.12) | **escondido até decidir**, como o dom de hoje: entra no dado e não na conta da mesa; quando faz a diferença, a saída diz "sem o dom, ..." e a MESA passa a dizê-lo. Os que mudam o que se vê (o Peso, o pé, o Sangue Largo) se mostram na primeira vez que agem. O feitiço `ler` e o clérigo também o leem |
| dom de feito | o que ainda estiver aberto | na hora: "algo mudou em você" (e a notícia anda) |
| dom sem par | se liderar a medida | pelo boato, na estação |
| jura | qualquer uma, uma só | ele escolhe |
| alcunha | as que ganhar | quando chega aonde a notícia chegou ("aqui o chamam de...") |
| vício | **o da forja, já** (Ferord é Treinado na forja); os outros no Treinado de cada caminho | ele escolhe |

### 2.12 Como nasce na gente do mundo
- **O dom raro:** um d1000 por pessoa pela semente (`dom_raro|PESSOA`): até 20, um dom raro (2%). **Os rivais rolam dois dados e vale o melhor (~4%).** O dom sai da
  lista com peso 3 no que combina com a pessoa: os de luta para o guerreiro, o arqueiro, o guarda e o aventureiro; a Mão de Ourives, o Olho de Liga e a Fome de Crescer
  para quem tem forja ou couro. Num mundo de ~200 nomeados e 40 rivais, nascem perto de **6 pessoas com dom raro** (c).
- **Quem já existe** (o mundo de hoje, Ferord) rola uma vez, num evento "talento" (como a manha da etapa 4b). O resultado é rolagem oculta: fica no SÓ O MESTRE.
- **O personagem do jogador rola dois dados, como os rivais (~4%)** (pergunta 6).
- **Os feitos tortos:** a semente escolhe os 7 que valem; a crônica (`historia.py`) fecha 1 ou 2, com o nome do morto que os fez.
- **As juras:** 1 em 100 dos que lutam (pela semente), e todo Fiel do Santuário do desenho das classes.
- **As alcunhas:** as Lendas nascem com 1 ou 2, tiradas da crônica; os veteranos, com uma, metade das vezes.
- **Os vícios:** quem tem Treinado nasce com um vício por caminho de Treinado, até 3, pelo molde.

### 2.13 Um exemplo de mesa (variante A)
> Ferord, nível 5 (0/100), forja a tenaz Incomum: a obra Incomum tem nível 10, o dobro do 5: **+40** (40/100). Outra Incomum: +40 (80/100). A primeira Rara
> (nível 20, e a primeira conta 40) dá +40 e passa de 100: **sobe ao nível 6** (20/100). Dali em diante a Incomum dá 20 (está acima do 6, não é o dobro). A MESA pergunta:
> "🎯 1. Subiu ao nível 6 (fechou com a forja): o ponto vai para a) Força (65) ou b) Afinidade (75)". O jogador responde "1b"; o evento "nivel" põe Afinidade 76.

---

## 3. Os dados

### 3.1 Na pessoa (`gente.json`; nada sai)
| Campo | Forma | O que é |
| --- | --- | --- |
| `experiencia` | inteiro de 0 a 99 | a experiência para o próximo nível (A) |
| `pontos` | inteiro, 0 ou mais | os pontos de atributo por pôr |
| `marca.par` | [atributo, atributo] ou nada | o par que o feito que fechou o nível oferece (B: o do caminho da subida) |
| `marca.postos` | {atributo: n} | os pontos de subida já postos em cada um (a metade) |
| `dom_raro` | uma chave de `tabelas_dons.RAROS`, ou ausente | o dom raro de nascença |
| `marca.raro_visto` · `marca.raro_n` | o dia · inteiro | o dom raro já se mostrou · o que o dom que cresce juntou (os pontos do Sangue Largo, as fugas do Pé) |
| `dons_feito` | [chave], até 2 | os dons de feito |
| `juramento` | {chave, dia, onde, quebra?} | a jura (como o `voto` de hoje) |
| `alcunhas` | [{nome, boa, ev, dia}], até 3 | as alcunhas |
| `vicios` | [chave] | os vícios postos |
| `marca.usos` | {chave: [dia, n]} | a lei do cansaço |

### 3.2 No mundo (`mundo.json`)
`feitos`: {chave: {quem, dia, ev}} (o feito que já tem dono, ou que a crônica fechou) · `feitos_vale`: [chave] (os 7 deste mundo; SÓ O MESTRE) ·
`sem_par`: {medida: {quem, desde}}.

### 3.3 Na luta (o arquivo da luta, por lutador)
`peso` (0 a 3, e a rodada do último golpe) · `pe` (as casas a mais no recuo) e `livre_menos` · `jura` · `raro` · `nao_recua` (a jura que não deixa) · **`feriram`**
(novo: os nomes de quem tirou PV deste lutador na luta inteira; o `golpeado` de hoje zera a cada rodada e não serve). A luta que volta ao
estado (o evento "luta", 11.12) leva também a experiência de cada um que feriu um inimigo vencido, o cansaço do Peso e a fuga que conta.

### 3.4 Os eventos e os verbos (`estado.py`)
| Efeito | Novo? | O que faz | Em que evento |
| --- | --- | --- | --- |
| `['pessoa', id, 'experiencia', 'soma', n]` | novo | n de 1 a 100; recusa se o resultado passa de 99 sem o `nivel` no mesmo evento | luta, forjar (e o de cada ofício: encantar, alquimia), treinar (o grau novo), viagem, masmorra, missao, rival, mestre |
| `['pessoa', id, 'nivel', 'soma', 1]` | já existe | o nível que sobe | os mesmos |
| `['pessoa', id, 'pontos', 'soma', ±n]` | novo (campo de soma, nunca abaixo de 0) | ganha na subida, gasta ao pôr | os mesmos; nivel |
| `['pessoa', id, 'atributos.X', 'soma', n]` | **novo** (hoje não há verbo para atributo) | põe o ponto; recusa X fora do par, acima de 100 pela subida, além da metade, ou sem pontos | **nivel** (novo), mestre, gera |
| `['pessoa', id, 'dom_raro', 'poe', chave]` | novo | o dom raro | gera, mestre, talento |
| `['pessoa', id, 'dons_feito', 'junta', chave]` com `['mundo', 'feitos', chave, 'poe', {...}]` | novo | o dom de feito; recusa o terceiro e o feito com dono | o evento do feito, mestre |
| `['pessoa', id, 'juramento', 'poe', {...}]` · `['pessoa', id, 'juramento', 'quebra', 'como']` | novo | a jura | **jura** (novo), luta, mestre |
| `['pessoa', id, 'alcunha', 'junta', {...}]` · `['pessoa', id, 'alcunha', 'tira', nome]` | novo | a alcunha | noticia, mestre |
| `['pessoa', id, 'vicio', 'poe', [chaves]]` | novo | os vícios (a troca gasta o dia) | **vicio** (novo), mestre |
| `['pessoa', id, 'marca.X', 'poe', v]` · `['mundo', 'sem_par', M, 'poe', {...}]` | já existem | as marcas; o sem par da estação | os de sempre; estacao |

---

## 4. Onde entra no motor
| Arquivo | Função | O que muda (M) ou é novo (N) |
| --- | --- | --- |
| `tabelas_dons.py` | (página nova) | N: a régua (40/20/10, 100, o teto do evento e do dia), os níveis do feito, os pares, a metade, o teto 100; os dons raros (chave, o que faz, o fardo, quando se mostra, os pesos), os feitos tortos, o sem par, as juras, os vícios, os moldes de alcunha. Nenhum número de dom fora dela |
| `nivel.py` | (novo) | N: `feito(E, pid, nivel_feito, caminho, porque)` → os efeitos; `poe(E, pid, atributo)` (o comando `nivel.py poe Força`); os pontos do NPC pelo molde; `voce(E)`, `so_mestre(E)` |
| `dons.py` | (novo) | N: `rola(E, pid)` (a semente); `mostra`; `confere(E, ev)` (o feito torto depois de cada evento); `jura`, `quebra`; `alcunha(E, noticia)`; `vicio`; `sem_par(E)` (por estação) |
| `estado.py` | `CAMPOS`, `aplica`, `valida` | M: os campos e os verbos de 3.4; os eventos "nivel", "jura", "vicio"; a metade e o teto na validação |
| `pessoas.py` | `ficha`, `padrao` | M: a ficha lê o dom raro (coragem, fôlego, a pele), a jura e os vícios; o `padrao` dá ao nascido com Sangue Largo os pontos a mais |
| `luta.py` | `golpe`, `jogada` | M: o Peso da Mão (no grupo DOM da pilha do D1), a Mão Certa (a janela; sem explosão nem crítico), o Couro de Bigorna |
| `luta.py` | `_anda`, `_passo`, `_golpe_livre`, `_decide`, `ordem` | M: o Pé Ligeiro (as casas, o −4, só no turno sem golpe); a ordem `recuar` recusada pelas juras |
| `luta.py` | `_ferida`, `_moral`, `nova`, `_fecha_luta` | M: o Osso Duro, o Corpo de Pedra, o Peito de Carvalho, o Sono de Lebre; o `golpe` (e o dano do feitiço, `magia.py`) marca `feriram`; o fim da luta faz dele os feitos → a experiência no evento "luta" |
| `oficio.py` | `_resolve`, `sobe` | M: a obra que fecha dá a experiência da categoria que saiu; o grau novo é feito; a Mão de Ourives, a Jura do Ferro Dado e o Fogo Guardado entram como prumo (D2) |
| `viagem.py`, `caca.py` | `fugir`, a chegada | M: o Pé Ligeiro no teste de fuga; o lugar novo e a masmorra nova dão 10 |
| `missoes.py` | `cumpre` | M: a missão é feito |
| `rivais.py`, `conta.py` | o plano cumprido | M: o rival sobe pela mesma régua (o alvo do plano) |
| `talento.py`, `gera.py`, `cria.py` | `nasce`, `_registro` | M: o dom raro nasce com a pessoa (o personagem e os rivais, dois dados) |
| `historia.py` | a crônica | M: fecha 1 ou 2 feitos tortos; as alcunhas das Lendas |
| `noticias.py` | | M: o feito público com nome vira alcunha |
| `turno.py` (a MESA) | "Você" | M: nível e experiência; os pontos por pôr (viram pergunta); os dons vistos, a jura, as alcunhas, os vícios |
| `provas_dons.py` | (novo) | N: o banco (seção 5); o `provas_mundo.py` o roda |
| `provas_ano.py` | | M: o ano com os rivais subindo |

---

## 5. O banco (`provas_dons.py`; as metas)
O padrão é o do banco de hoje: o duelo de iguais do nível 50, tudo Raro, perto; 4.000 lutas por linha (±1,6), com metade de cada lado.

| Meta | O que se mede | Como | Faixa aceita |
| --- | --- | --- | --- |
| DN1 O DOM DE NASCENÇA NÃO PASSA DE UM GRAU | cada dom raro de luta | duelo nos níveis 10, 20, 50 e 150 (a categoria do banco em cada um) | até o Grande Dom no mesmo cenário, +1,6 de folga (medido: o Peso 57,5 a 59,5; a Mão Pesada fixa 57,9 a 59,4; o Sangue Largo +20 de 54,2 a 58,0; o Couro 55,4; contra o Grande Dom de 59,4 a 61,8) |
| DN2 O DOM DE FEITO NÃO PASSA DE DOIS GRAUS | cada dom de feito de luta | o mesmo | até o dom +4 (69,5%); medido: a Mão que Fez 57,8% |
| DN3 A JURA PAGA E NÃO PASSA DE UM GRAU | cada jura | duelo e o cenário dela | de +3 ao Grande Dom (medido: Mão Certa 56,0%, Corpo de Pedra 54,6%) |
| DN4 O ITEM DECIDE | o pior acúmulo (Grande Dom, Peso cheio, Sangue Largo +20) com a arma uma abaixo | 4.000 lutas | até 15% (T7 de hoje); medido 11,4% |
| DN5 O PÉ SALVA, NÃO VENCE | recuar desde o começo; recuar quando a luta vira | 4.000 lutas | sai da luta de 85 a 99%; a queda quando a luta vira de 18 a 30% (sem o dom, 40,9%); a vitória igual (±2) |
| DN6 O QUE CRESCE TEM TETO | o Sangue Largo, o pé, o Peso | conferência em 1.000 vidas de rascunho | o Sangue Largo para em +20; o pé conta uma fuga por dia, só a que conta, e para em +2 casas; o Peso nunca passa de 3 e apaga no turno sem golpe |
| DN7 A SORTE DE NASCER | 10.000 nascidos, 20 sementes | `dons._sorteia` | dom raro de 1,5 a 2,5% do povo; de 3 a 5% dos rivais e do personagem; ninguém com dois |
| DN8 O ESCONDIDO SE MOSTRA | cada dom raro | cenários com o dado posto | mostra-se quando decide (ou na primeira vez que age, os de 2.11); a mesa não o mostra antes; o `ler` o mostra |
| DN9 O FEITO TORTO | a semente; o primeiro; o teto | 2.000 mundos de rascunho | a mesma semente dá os mesmos 7; o feito com dono recusa o segundo; ninguém com 3 |
| DN10 A PILHA | o Peso com a pilha do D1 | 10.000 golpes ao acaso | o multiplicador nunca passa de ×7 (abaixo de duas categorias, ×9) |
| NV1 O RITMO | 300 carreiras de Ferord | a régua de 2.2 | o ferreiro: nível 10 entre os Dias 55 e 75, 20 entre 160 e 220; o que caça: 20 entre 100 e 130, 40 entre 330 e 400 |
| NV2 O MUNDO FAZ SENTIDO | o teto de cada papel pela régua | conta | cada papel do mundo gerado dentro de 1,5 × o nível dos feitos dele (2.2) |
| NV3 A SUBIDA NÃO VENCE O ITEM | o nível 40 contra o 5 de arma uma acima | 4.000 lutas | até 15% (medido 11,6%) |
| NV4 OS PONTOS | o par, a metade, o teto 100 | conferência e duelo | o 40 contra o 5, de 55 a 70% (medido 60,8% pelo molde e 66,9% no pior que se deixa); nenhum atributo acima de 100 pela subida |
| NV5 A LENDÁRIA NÃO SOBE | o melhor ferreiro possível (Afinidade 100) | o T9 de hoje | de 15 a 30% |
| NV6 O ANO | o `provas_ano.py` com os rivais subindo | o ano | os rivais não matam o dragão no primeiro mês, e a corrida continua com mortos |
| NV7 A PESSOA SEM DOM É A DE HOJE | as lutas de hoje, com semente fixa | o banco inteiro | saem iguais, dado por dado; as metas de hoje passam |

---

## 6. O que fica para depois, os riscos e as perguntas

**Para depois.**
- O degrau de classe como subida (B) e as técnicas de dano que acendem o Peso: são do desenho das habilidades e das classes. Até lá, o esforço conta como técnica.
- A Jura do Sangue no Feitiço, a Voz de Comando, a Voz que Dobra e a Jura do Último de Pé se medem no mago contra mago e no 3 contra 3 do banco.
- O texto das alcunhas (os moldes de frase) e as notícias que as levam.
- A gente que não entra em cena não sobe; se um dia o mundo pedir, uma subida por estação para quem trabalha (fica fora agora: muito evento por pouco).
- O herdeiro segue sem herdar o nível nem a mão (25.4).

**Os riscos.**
1. **A pilha do D1 com o Peso:** o grupo DOM vai a +60% e a pilha a ×6,7. O item ainda decide (11,4% medido), mas o EF3 do D1 tem de rodar de novo com o Peso.
2. **Quem lê este desenho conhece os feitos tortos:** a semente escolhe 7 de 11 e a crônica fecha alguns; ninguém sabe quais estão abertos.
3. **O min-max dos pontos:** tudo no Vigor dobraria o nível (+24,7 contra +10,8). O par, a metade e o teto o seguram (o pior permitido, +16,9).
4. **A mina de experiência:** a régua relativa fecha a obra barata (a Comum para no 8, a Incomum no 16) e o teto do dia corta a repetição.
5. **Os rivais subindo mudam a corrida:** devagar (35 níveis valem um grau), mas o `provas_ano.py` tem de passar (NV6).
6. **O dom que muda o que se vê não fica escondido:** o Peso, o pé e o Sangue Largo se mostram na primeira vez que agem. É de propósito: o jogador vê o contador.
7. **"Quem feriu" no grupo grande:** hoje a luta não guarda quem feriu quem na luta inteira (o `golpeado` zera a cada rodada); o campo novo `feriram` guarda, e o
   feitiço de área conta para quem lançou.

**As perguntas ao jogador (cada uma com a recomendação).**
1. **O nível:** (a) variante A, a experiência pelos feitos; (b) variante B, o grau novo, e o nível parado. **Recomendo (a).**
2. **Os pontos da subida:** (a) no par do caminho do feito, com a metade e o teto 100; (b) livres; (c) pelo molde, sozinhos. **Recomendo (a)**: livre, tudo vai ao
   Vigor e o nível dobra.
3. **O Sangue Largo:** (a) toda vez que (o dobro de pontos a cada subida, até +20); (b) fixo (+10 de uma vez). **Recomendo (a).**
4. **A Mão Pesada:** (a) o Peso da Mão (+20% em todo golpe por técnica que acerta, até 3); (b) a fixa (+20% só na técnica). **Recomendo (a)**, com o D1 abrindo o
   grupo DOM a +60%.
5. **O Pé Ligeiro:** (a) o pé que cresce com as fugas que contam; (b) o fixo (+1 casa, −4, +4). **Recomendo (a).**
6. **A chance de o personagem ter um dom raro:** (a) dois dados, como os rivais (~4%); (b) um, como o povo (2%). **Recomendo (a).**
7. **A gente do mundo sobe?** (a) quem entra em cena e os rivais, pela mesma régua; (b) só o personagem; (c) todos, uma vez por estação. **Recomendo (a).**
8. **Os feitos tortos:** (a) a semente escolhe 7 de 11, e a crônica fecha alguns; (b) todos os 11 valem. **Recomendo (a)**: o feito torto é para ser achado.

**Os rascunhos das contas** (fora do repositório): `/tmp/claude-0/-home-user-ferir/4088f7d7-9a0c-5212-bbb2-a884104a0915/scratchpad/D4/banco_d4.py` (o duelo com
os remendos), `/tmp/claude-0/-home-user-ferir/4088f7d7-9a0c-5212-bbb2-a884104a0915/scratchpad/D4/ritmo.py` (as 300 carreiras) e as saídas `saida_A.txt` a
`saida_D.txt` e `saida_ritmo.txt`, na mesma pasta.
