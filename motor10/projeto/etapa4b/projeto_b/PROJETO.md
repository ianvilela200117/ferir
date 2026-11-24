# Projeto B da etapa 4b: os dragões e os povos do personagem

Rascunho de projeto. Nada daqui é regra até passar no banco de provas. A outra metade da etapa (as masmorras e o ladino) é do projeto A; onde as duas se tocam está na seção 11. Li o rascunho do projeto A (`projeto_a/PROJETO.md`) e uso os nomes dele (a `manha`, o lance, a tocha, a sala, o `vila_teste.py masmorra`).

## 0. Em uma página

1. **Três tipos de dragão, pelo lugar onde vivem:** o **dragão da serra** (voa e sopra fogo), o **verme do brejo** (sem asas; o bafo e a cauda envenenam) e o **dragão das grutas** (sem asas; vê no escuro e enrosca). Nada de cor. Cada tipo tem a sua fúria quando ferido, e luta melhor em casa (o brejo na água, as grutas no escuro).
2. **Cinco idades, uma por grau:** o filhote (D, Incomum, médio, PV 147), o jovem (C, Raro, grande, PV 480), o adulto (B, Épico, enorme, PV 817), o velho (A, Único, enorme, PV 1.100) e o ancião (S, Lendário, enorme, PV 1.337: o dragão do capítulo 6). **Tudo roda com os traços que a luta já tem.** O que falta é uma coisa só: a fase **foge** (o dragão da serra, ferido fora do covil, vai embora pelo ar).
3. **Medido, a pergunta do pedido:** quatro de nível 50 de peças Raras contra o dragão jovem no covil vencem **70%**, morrem **0,46 por luta**, e alguém morre em **33%** das lutas. **Com a arma Épica, vencem 96%** (morre alguém em 7%); com tudo Incomum, **0%**. A categoria da peça é o que decide, como sempre.
4. **O núcleo:** do adulto para cima o dragão dá o núcleo da categoria dele (Épico, Único, Lendário), a matéria da escada da forja. O filhote e o jovem dão couro e osso (Incomum e Raro), sem núcleo.
5. **O covil é uma masmorra do projeto A** (o molde `covil`) ou um ermo. **O tesouro é prata que já existe**, posta pelo gerador, mais as peças de quem o dragão matou. **A vida do dragão** é contada todo dia: dorme semanas ou anos, acorda, ataca a vila dele (o jovem) ou cobra tributo (do adulto para cima), e a prata que ele leva vai para o tesouro: a prata do mundo fecha em todo passo (medido).
6. **Contra a mina:** a loja só paga o que tem (o despojo e o tesouro do jovem levam 1.229 dos 2.000 de prata de Pedra Rasa, e a peça Épica é recusada); o dragão morto não volta; roubar o tesouro de quem dorme é possível, mas **o ladrão robô morre no ano em 93 a 99% das vidas**.
7. **Seis povos entram agora:** humano, anão, elfo, meio-orc, pequenino e gnomo. Cada um mexe nos seis atributos **com a soma igual**, tem de um a dois traços (ver no escuro, resistir a veneno, coragem), um **corpo** (gente ou miúdo: a armadura é feita para o corpo), **uma tendência** nos talentos (um caminho a favor, um contra), a vida longa e um bônus de +2 num teste do ladino.
8. **A lei, medida (4.000 lutas por linha):** nenhum povo vence o humano de peças iguais mais que o Grande Dom vence o gêmeo (59,8%), em nenhuma condição: espada, arco, adaga, no claro e no escuro, no nível 5 e no 50 (medido: de 40,4 a 58,6%). Contra o humano com a arma uma acima, nenhum passa de 5,8%. **O humano é a pessoa de hoje, dado por dado.**
9. **Ver no escuro, para o povo, tira a metade do escuro na luta** (−2 no golpe, −4 no tiro), e não o escuro inteiro: o escuro inteiro (o "noturno" do goblin) passou do Grande Dom (62,3%). Fora da luta (andar, procurar, abrir sem tocha), vale o que o projeto A diz.
10. **A vila de teste ganha**, por um comando que só acrescenta: uma anã ferreira, um meio-orc e uma elfa de passagem, uma pequenina que mora lá, duas armaduras miúdas na loja, e **o Tição, um dragão jovem longe**, na Serra Fria, que ataca uma aldeia que o Maro não alcança: a ameaça que se conta e não se caça no nível 5. **O Maro segue humano.** A vila nova nasce com o personagem de outro povo (`povo=`).

## 1. O que medi, e como

Tudo rodou do rascunho, lendo o motor de hoje (`/home/user/ferir/motor10`), de dentro de `motor10/`, com `PYTHONDONTWRITEBYTECODE=1` e o `MOTOR10_MUNDO` numa pasta minha (uma vila de teste nova, e uma cópia do `ensaio/` só para ler). Nada foi gravado no motor nem no save do jogador. As lutas são as do `luta.py` de verdade, com semente fixa. **O que a luta ainda não roda** (ver no escuro pela metade, resistir a veneno, a coragem do povo e a fase "foge") eu emulei por embrulho, no rascunho, só para medir; a construção os faz de verdade, e o banco mede de novo. Os arquivos estão em `projeto_b/medidas/`:

| Arquivo | O que mede | Lutas |
| --- | --- | --- |
| `m1_atributos.py` → `m1_saida.txt` | quanto vale cada atributo, o tamanho pequeno, o escuro e o noturno, no duelo de nível 50, tudo Raro | 4.000 por linha |
| `m2_povos.py`, `m6_povos.py` → `m2_saida.txt`, `m6_saida.txt`, `m6_saida_v3.txt` | as três voltas dos povos contra o humano: espada, arco, adaga, claro e escuro, nível 5 e 50, arma uma acima, contra a aranha | 3.000 a 4.000 |
| `m3_dragoes.py`, `m3b_jovem.py` → `m3_*.txt` | o primeiro desenho das idades e as variantes do jovem | 300 a 600 |
| `m4_fases.py`, `m5_final.py`, `m5b_serra.py` → `m4_saida.txt`, `m5_*.txt` | as fúrias de cada tipo, a fase "foge", o corredor, o dragão dormindo | 300 a 400 |
| `m11_final.py` → `m11_jovem.txt`, `m11_idades.txt` | **a proposta final do dragão**: as cinco idades e os três tipos em casa, a categoria uma acima e uma abaixo, o jovem contra o grupo de nível 50 | 400 a 600 |
| `m12_filhote.py` → `m12_saida.txt` | o filhote como bicho que foge | 1.500 |
| `m7_despojo.py` → `m7_saida.txt` | o despojo e o tesouro do jovem e do adulto vendidos na loja de Pedra Rasa (o mercado de verdade, num mundo de rascunho carregado e nunca gravado) | |
| `m8_vida.py` → `m8_saida_v2.txt` | o protótipo da vida do dragão, um ano, sobre o gravador de verdade (eventos "mestre" num mundo de rascunho) | 3 sementes por linha |
| `m9_roubo.py`, `m9b_roubo_A.py`, `m9c_ladrao_ano.py` → `m9*_saida.txt` | a conta exata de roubar o tesouro, com o teste do projeto A; o ladrão robô num ano | 20.000 vidas |
| `m10_cena.py` → `m10_saida.txt` | a luta da cena jogada: o Maro e a anã contra três esqueletos, de dia e de noite | 1.500 |

**O que é medida de verdade:** as lutas (com o que falta emulado, dito acima), a venda na loja, a soma da prata do mundo, as contas exatas do dado. **O que é rascunho:** a vida do dragão (a regra foi escrita no protótipo, não no motor) e o ladrão robô (a conta do dado é exata; a vida dele, simulada fora da luta).

## 2. Os dragões de verdade

### 2.1 Os três tipos

| Tipo | Onde vive | O sopro | Traços do tipo | A fúria (a fase) | Em casa |
| --- | --- | --- | --- | --- | --- |
| **o dragão da serra** | serra, ruína alta | o fogo | voa | abaixo de 30% do PV: **no covil, desce ao chão em fúria** (perde "voa", ganha "ardente": quem o golpeia de perto se queima, e a ferida que ele abre queima); **fora do covil, foge pelo ar** | ao ar livre |
| **o verme do brejo** (sem asas) | brejo | o bafo podre | veneno (o sopro e a cauda envenenam) | abaixo de 50%: **enrosca na lama** (ganha "agarra") | na água pela cintura (o tempo "água", para os dois lados) |
| **o dragão das grutas** (sem asas) | caverna, ruína funda, o fundo de masmorra | a brasa e a fumaça | noturno (vê no escuro), agarra | abaixo de 50%: **bebe o sangue de quem prende** (ganha "dreno") | no escuro |

O "dragão", o "verme" e a "serpe" são da fantasia comum e do folclore; os tipos são pelo lugar. Não há cor, nem o sopro de raio ou de ácido.

### 2.2 As cinco idades

| Idade | Anos | Grau | Corpo (garra e couro) | Tamanho | Nível | Instinto | Força · Agilidade · Vigor · Vontade · Percepção · Afinidade | PV | Acerto | Defesa | Traços da idade |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **filhote** | até 30 | D | Incomum | médio | 30 | Iniciante | 70 · 80 · 70 · 50 · 70 · 40 | 147 | +9,75 | 31 | sopro |
| **jovem** | 30 a 150 | C | Raro | grande | 80 | Mestre | 120 · 70 · 150 · 60 · 75 · 45 | 480 | +18,75 | 34,5 | sopro, apavora |
| **adulto** | 150 a 500 | B | Épico | enorme | 110 | Mestre | 140 · 70 · 150 · 80 · 85 · 50 | 817 | +23,25 | 36,5 | sopro, apavora, couraça |
| **velho** | 500 a 1.000 | A | Único | enorme | 160 | Mestre | 160 · 70 · 200 · 90 · 90 · 55 | 1.100 | +27,75 | 40,5 | sopro, apavora, couraça, resiste |
| **ancião** | mais de 1.000 | S | Lendário | enorme | 220 | Lendário | 180 · 70 · 240 · 100 · 90 · 60 | 1.337 | +34,25 | 45,5 | sopro, apavora, couraça, resiste |

As armas do corpo: o filhote, garra e presa; do jovem em diante, garra, bocarra e cauda (alterna golpe a golpe, como todo bicho). O couro é escama (vale como malha). O sopro é o do capítulo 6: uma rodada sim, uma não, um ataque de 1d8 com o valor da categoria do corpo em cada inimigo a até 4 casas, que não se apara.
**O ancião é o dragão do capítulo 6** (os mesmos números), com o tipo, a fase e o "resiste". O dragão do capítulo 6 fica na página dos bichos como está (o banco o usa); o gerador da etapa 7 deixa de pô-lo na fauna do coração da serra e põe um covil no lugar.
**O filhote é bicho:** testa a coragem e foge ferido. **Do jovem para cima, é chefe:** não foge pelo susto, e só a fase o tira da luta.

### 2.3 Na luta: os traços que já rodam, e o que falta

| Traço (a luta de hoje) | Quem tem | O que faz no dragão |
| --- | --- | --- |
| sopro | todos | pega o grupo inteiro a até 4 casas; com veneno, envenena cada um; com ardente, a ferida queima |
| voa | a serra | a espada e a maça têm −6 contra ele; num corredor, no chão ou agarrado, não voa |
| apavora | do jovem para cima | quem começa a luta testa a coragem contra 28 (o humano de nível 50 foge em 13,75% e fraqueja em 33,75%; quem o jogador comanda só fraqueja) |
| couraça | do adulto para cima | sem fresta, e o crítico não corta a escama pela metade |
| resiste | o velho e o ancião | a magia escorre no couro velho: a guarda contra o feitiço é o corpo inteiro |
| veneno | o brejo | o golpe e o sopro envenenam |
| agarra, noturno | as grutas | prende quem está colado; o escuro não lhe tira nada |
| ardente, agarra, dreno | as fúrias | (a fase, abaixo) |

**O que não usei, e por quê:** "regenera" como fúria do brejo (medido: o adulto passava a vencer 99% dos grupos do degrau; o jovem, 60%: forte demais num corpo de 800 PV); "lança" (o dragão velho que fala e lança feitiços fica para depois); "imaterial" (não é dragão).
**O que falta, uma coisa só:** a fase **foge**. Hoje "o chefe não foge" (16.7). A proposta: a fase pode dizer `foge`; quando o limiar chega, se o dragão voa, não está num corredor e **o lado dele tem saída** (fora do covil), ele sai pelo ar (quem voa não leva golpe livre) e a luta para e pergunta; senão, a fase vale como fúria (perde e ganha os traços dela). **No covil, o cenário diz `sem_saida` do lado do dragão:** ele defende o tesouro até o fim. Fugido, ele volta ao covil com o PV que tinha e sara 10% por dia dormindo.

### 2.4 O corpo e o núcleo

| Idade | O despojo (o corpo inteiro: de metade ao inteiro, como todo bicho) | O núcleo |
| --- | --- | --- |
| filhote | 4 de comida, 3 de couro Incomum, 2 de osso Incomum | não |
| jovem | 10 de comida, 5 de couro Raro, 4 de osso Raro | não |
| adulto | 8 de couro Raro, 6 de osso Raro | **Épico** |
| velho | 10 de couro Raro, 8 de osso Raro | **Único** |
| ancião | 12 de couro Raro, 10 de osso Raro | **Lendário** |

O verme do brejo dá, além disso, peçonha (1 Incomum no filhote; 2 Raras do jovem para cima). A matéria segue a regra 6.11 (a categoria do bicho até o Raro; do Épico para cima, Rara). **O núcleo é o coração do dragão:** item do Livro, `de` o dragão, com o nome dele ("o coração do Tição"), contado, que não se vende em loja. **Só do adulto para cima**, porque a escada da forja só pede núcleo do Épico para cima (o núcleo Raro não serviria a obra nenhuma). O dragão morto não renasce (o Lendário de hoje também não): os núcleos de dragão de um mundo são os dos dragões que ele tem.

### 2.5 Medido: o grupo de nível 50 contra o dragão jovem

O jovem da serra, com a fúria, no covil (sem saída para ele), 600 lutas por linha (`m11_jovem.txt`):

| O grupo | Vence | Mortos por luta | Morre alguém |
| --- | --- | --- | --- |
| **4 de nível 50, espada, malha e escudo Raros** | **70,3%** | **0,46** | **33,0%** |
| 4, misto (2 espadas, 1 lança, 1 arco atrás), Raros | 82,5% | 0,31 | 23,7% |
| 5, Raros | 89,5% | 0,27 | 19,3% |
| 6, Raros | 92,3% | 0,23 | 15,8% |
| **4 com a arma Épica** (o resto Raro) | **95,7%** | 0,08 | 7,2% |
| 4 com a armadura e o escudo Épicos (a arma Rara) | 95,3% | 0,06 | 5,0% |
| 4, tudo Épico | 100% | 0,00 | 0,2% |
| **4, tudo Incomum** | **0%** | 2,27 | 99% |
| 4 Raros, **ele dormindo** (surpreendido: perde o primeiro turno) | 80,8% | 0,32 | 24,0% |
| 4 Raros, num corredor de largura 2 (ele não voa) | 64,2% | 0,66 | 47,0% |
| 4 Raros, **fora do covil** (ele foge ferido) | 79,3% (e ele **fugiu em 79%**) | 0,37 | 27,7% |
| um homem de nível 50, Raro | 0,5% | | morre em 51% |

**Como ler:** o jovem é a primeira caça de dragão de um grupo de veteranos, e mata um em cada três grupos que o enfrentam. **Uma categoria na arma muda tudo** (de 70% para 96%, e de 0,46 morto por luta para 0,08); uma abaixo, é morte certa. O corredor não ajuda o grupo contra um bicho só: bate menos gente nele, mesmo com o dragão apertado e sem voar (o jovem: 70% na câmara aberta, 64% num corredor de 2, 53% num de 1; o adulto: 64%, 52% e 17%; `m13_saida.txt`). Pegá-lo dormindo vale 10 pontos.

### 2.6 Medido: as idades contra o grupo do degrau

Cada tipo em casa, com a fúria; o grupo é o "homem do degrau" das criaturas (espada, malha, elmo e escudo da categoria, no nível de referência: Incomum 30, Raro 50, Épico 90, Único 120, Lendário 150), **com Vontade 80 do Épico para cima**, para sustentar o conjunto (2.9; sem isso a armadura dorme e o adulto vence 99%: medido). Duas rodadas, de 400 e de 600 lutas por linha (`m11_idades.txt` e `m13_saida.txt`; o filhote, `m12_saida.txt`); a tabela mostra as duas:

| Idade | Quem enfrenta | A serra | O brejo | As grutas | Faixa proposta |
| --- | --- | --- | --- | --- | --- |
| filhote | um homem do degrau | 61,9% | 54,4% | 52,1% | 40 a 65% |
| jovem | 4 do degrau | 69,5 e 70,3% | 65,5 e 67,2% | 57,0 e 58,5% | 50 a 75% |
| adulto | 4 do degrau | 64,0 e 63,7% | 57,2 e 57,7% | 52,8 e 54,8% | 45 a 70% |
| velho | 4 do degrau | 41,2 e 41,0% | 37,8 e 37,2% | 31,5 e 31,7% | 25 a 50% |
| ancião | 4 do degrau | 15,8 e 13,3% | 18,0 e 15,8% | 11,8 e 11,2% | 5 a 25% |
| ancião | 6 do degrau | 80,5 e 79,8% | 83,5 e 84,3% | 78,2 e 79,2% | 65 a 90% |
| do jovem ao ancião | 4 com o conjunto uma acima | 99,5 a 100% | | | 90% ou mais |
| do jovem ao ancião | 4 com o conjunto uma abaixo | 0 a 1% | | | 10% ou menos |
| do jovem ao ancião | um homem do degrau | 0 a 0,5% | | | até 5% |

**Mortos por luta, nos grupos de 4 do degrau:** o jovem, de 0,47 a 0,72; o adulto, de 0,77 a 1,19; o velho, de 1,24 a 1,60; o ancião, de 1,77 a 1,90. O filhote mata o homem do degrau em 24 a 31% das lutas (e foge em 20 a 29%).
**Como ler:** quanto mais velho, mais ele pede gente além da peça. O ancião é a calamidade: quatro heróis Lendários morrem quase todos; seis vencem quatro vezes em cinco. Em toda idade, a peça uma categoria acima vence sempre, e uma abaixo morre sempre.
**As fúrias que testei e larguei** (`m4_saida.txt`, `m5_*.txt`, `m5b_saida.txt`): o fogo da serra a 50% deixava o velho com 12% e o ancião com 0,3% (forte demais); a 30% e descendo ao chão, ficou com os outros dois tipos.

## 3. O covil e o tesouro

### 3.1 Onde mora

**O covil é uma masmorra do projeto A**, de molde `covil`: a boca, as galerias, e a **câmara do tesouro** (aberta: ali ele voa e sopra), onde mora o dragão. A sala do dragão leva o `chefe` de A e o meu registro, `dragao` (seção 5). Quando a masmorra não estiver pronta, ou o covil for pequeno, o covil é **um ermo** com o registro `dragao` (como a toca de hoje é um ermo com `covil`). Nos dois casos: **o tesouro é o estoque do lugar** (a prata e os bens) **e as peças com `onde` ali, sem dono e não soltas** (guardadas: quem passa no rastro não as acha; só quem fica com o campo, ou o ladrão).

### 3.2 O tesouro: prata do mundo

| Idade | A prata (o teto, na conta da prata do mundo) | No mundo do `PROJETO.md` (perto de 55.000) | Peças | A melhor peça |
| --- | --- | --- | --- | --- |
| filhote | nada | | nenhuma | |
| jovem | até 1% | até 550 | 2 a 3 | Rara |
| adulto | até 3% | até 1.650 | 3 a 5 | uma Épica (das 12 contadas) |
| velho | até 6% | até 3.300 | 4 a 6 | uma Única, se houver sem dono (das 4) |
| ancião | até 10% | até 5.500 | 5 a 8 | uma Lendária, se houver sem dono (das 3); senão Única |
| **todos os covis juntos** | **até 25% da prata do mundo** | | | |

**De onde vem a prata:** o gerador da história (etapa 7) tira dos lugares a prata que o dragão levou em séculos (o tributo e os ataques) e a põe no covil: a soma não muda. **As peças** são as dos que morreram ali (a cadeia de donos sem buraco: "o último dono morreu no covil do Tição, no ano 812"). Na vila de teste, como a toca de hoje, o tesouro nasce por um evento do gerador (300 de prata, seção 7). **O tesouro não se refaz** a não ser pela vida do dragão (que tira dos lugares, 3.3): morto o dragão, o covil fica vazio.
**A divisão** é a de A e a da caça: a prata e os bens em partes iguais entre quem lutou até o fim; as peças com quem comanda, e o resto é cena.

### 3.3 A vida do dragão (o mundo sozinho; evento "dragão", todo dia)

| Idade | Dorme depois de comer | O ataque (sem tributo pago) | O tributo (por estação, da vila dele) |
| --- | --- | --- | --- |
| filhote | (não ataca vila: caça no ermo) | | |
| jovem | 20 a 40 dias | leva 30 de gado (a comida da vila), de 5 a 20 de prata, e mata de 0 a 1 | não cobra |
| adulto | 30 a 60 | 60 de gado, de 20 a 60 de prata, de 0 a 3 mortos | 3% da prata da vila |
| velho | 90 a 180 | 120 de gado, de 50 a 150 de prata, de 1 a 5 mortos | 5% |
| ancião | 300 a 400 | 200 de gado, de 100 a 300 de prata, de 2 a 8 mortos | 8% |

1. **Dormindo** (o dia antes de `dorme_ate`): nada acontece; o ferido sara 10% do PV por dia.
2. **Acordado:** do adulto para cima, se a estação ainda não foi paga, a vila paga o tributo (sai do estoque dela e entra no do covil); pago, ele come no ermo e volta a dormir. Sem tributo (o jovem), ou sem prata para pagar, **ataca de noite**: o gado sai do estoque da vila (comido), a prata vai para o tesouro, e o povo da vila cai dos mortos. Depois dorme.
3. O acaso é o do mundo (`estado.sorte`); a prata só muda de mão.

**Medido no protótipo** (`m8_saida_v2.txt`; um ano, três sementes): o jovem ao lado de uma aldeia de 120 ataca **12 a 13 vezes**, mata **5 a 7** (o povo de 120 vai a 113 a 115), leva 360 a 390 de gado e **139 a 187 de prata** (a aldeia vai de 600 a 413 a 461; o tesouro, de 400 a 539 a 587). O adulto ao lado de uma vila de 400 recebe o tributo todas as estações (a vila vai de 2.000 a 1.772) e não ataca ninguém; o velho tira de uma cidade de 1.500 cerca de 1.070 no ano; o ancião, de uma capital de 4.000, de 1.600 a 3.070. **A prata do mundo fechou em todas as linhas.** O primeiro rascunho (o jovem dormindo 8 a 14 dias e matando até 2) matava 30 de 120 no ano: larguei.

### 3.4 Roubar o tesouro de quem dorme

É o "roubar o covil do dragão" do `PROJETO.md`, e a regra é a do projeto A (o lance, o andar escondido do mais barulhento, o punhado: a sexta parte da prata que havia quando ele adormeceu, ou uma peça). **O que é meu é o lado do dragão: a vigília.**
- **O dragão dorme leve sobre o ouro:** contra **20 + Percepção ÷ 10 + 2**, e **+2 a cada punhado já tirado no mesmo sono** (o ouro mexido o inquieta). Não vale o −6 de quem dorme: com ele, um ladino Treinado no escuro levaria os seis punhados (o tesouro inteiro) em 49 a 65% das vezes.
- **Acordado, ninguém rouba:** o ladrão é visto. **O dragão que acorda na câmara não é surpreendido**, a luta começa perto, e ele age antes de qualquer fuga pelas galerias.
- A rolagem é oculta (à mesa, só "rolagem oculta"; o número no SÓ O MESTRE): quem rouba não sabe o quanto falta para ele acordar.

**A conta exata** (`m9b_saida.txt`; o ladino Treinado de couro, Agilidade 80: +12 no escuro, +6 com tocha):

| | Jovem | Adulto | Velho e ancião |
| --- | --- | --- | --- |
| o 1º punhado, no escuro | 70% | 66% | 62% |
| punhados em média até ele acordar, no escuro | 1,5 | 1,3 | 1,2 |
| o 1º punhado, com tocha | 44% | 40% | 36% |
| os seis punhados seguidos, no escuro | 1% | 1% | 0% |

**O ladrão robô num ano** (`m9c_saida.txt`; entra uma vez por sono, tira um punhado e sai; se acorda o dragão, morre: um homem contra o jovem vence 0,5%): ao lado do jovem, **morre no ano em 99%** das vidas e tira em média 91 de prata (1,3 por dia de vida); ao lado do adulto, morre em 97% e tira 376 (4,5 por dia de vida, perto da diária). É aposta, não renda.

### 3.5 Quantos há num mundo

Na região do `PROJETO.md` (16 lugares, 6 ermos, 8 masmorras): de 0 a 2 filhotes, de 1 a 3 jovens, 1 ou 2 adultos, 0 ou 1 velho, 0 ou 1 ancião. E **um só no mundo inteiro, o que dorme**: o dragão Mítico do quadro da conquista ("Mítico: 1, dormindo"), que é da etapa 6 (seção 12). Não há ovo nesta etapa: **o dragão não cria**; morto, não volta. Os núcleos de dragão de uma região são, no máximo, 2 Épicos, 1 Único e 1 Lendário, uma vez: entram na conta dos núcleos do mundo, não por cima dela.

### 3.6 O que impede a mina

| O caminho | O que o tranca | Medido |
| --- | --- | --- |
| **vender o despojo e o tesouro** | a loja paga o que tem, paga 40% pelas peças, fica farta, e o preço da matéria cai a cada venda; do Único para cima não há loja | o jovem inteiro em Pedra Rasa: a loja paga **1.229** (o couro Raro de 111 a 37, peça a peça; a espada Rara 432, o escudo Raro 345) e a caixa dela vai de **2.000 a 771**; do adulto, a peça Épica é **recusada** (a caixa não paga 2.592) |
| **o tesouro** | é prata que já existe; não renasce; o dragão só o refaz tirando dos lugares | a prata do mundo fecha em toda conta (o protótipo e a venda) |
| **o dragão que volta** | não volta: o dragão não cria e o morto não renasce | (meta MI3) |
| **o roubo** | a vigília que sobe; quem o acorda morre | morre no ano em 93 a 99% |
| **o mesmo dragão duas vezes** | o que fugiu volta ao covil, e o tesouro está lá; a segunda luta é a mesma luta, com o PV que ele tiver | |

Matar um dragão jovem rende, uma vez, cerca de 1.630 de prata a quem o mata (400 do tesouro e 1.229 da loja, que fica quase sem prata), repartidos por quatro: perto de 400 cada um, com uma chance em três de alguém não voltar.

## 4. Os povos do personagem

### 4.1 Quais entram agora

**Entram seis:** o humano, o anão, o elfo, o meio-orc, o pequenino e o gnomo. **Ficam de fora:** o meio-elfo (fácil de pôr depois: a mesma tabela), os povos das criaturas como personagem (o goblin, o orc) e qualquer povo de jogo ou livro. O meio-orc existe porque o orc existe no mundo (capítulo 15).

### 4.2 Os números de cada povo

| Povo | Força | Agilidade | Vigor | Vontade | Percepção | Afinidade | Traços | Coragem | Corpo |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **humano** | 0 | 0 | 0 | 0 | 0 | 0 | | 0 | gente |
| **anão** | 0 | −5 | +5 | +5 | −5 | 0 | vê no escuro, resiste a veneno | 0 | gente |
| **elfo** | −10 | +10 | −5 | −10 | +10 | +5 | vê no escuro | 0 | gente |
| **meio-orc** | +10 | 0 | +5 | −5 | 0 | −10 | vê no escuro | 0 | gente |
| **pequenino** | −15 | +5 | 0 | +5 | +5 | 0 | | +4 | miúdo |
| **gnomo** | −10 | 0 | −5 | 0 | +5 | +10 | vê no escuro | 0 | miúdo |

**A soma de cada linha é zero.** O personagem nasce com os atributos do começo (340) mais os do povo: o guerreiro pequenino tem Força 55, Agilidade 65, Vigor 70, Vontade 55, Percepção 55 e Afinidade 40 (340). A gente gerada, o molde mais o povo. **Os atributos gravados já são os de quem nasceu:** o povo não soma de novo em conta nenhuma.

| Povo | A tendência (seção 4.5): a favor · contra | No teste do ladino (o +2 que A pede) | A frase que o jogador lê |
| --- | --- | --- | --- |
| humano | | | a medida de todos: nada a mais, nada a menos |
| anão | forja · verde | +2 em achar a armadilha e a passagem de pedra | duro, teimoso e de vista curta; vê na penumbra das minas, e o veneno o pega pela metade |
| elfo | tiro · peso | +2 em achar (a armadilha, a passagem escondida) | leve e de olho longo, frágil de corpo e de pouca paciência; vê na penumbra |
| meio-orc | peso · encanto | +2 em arrombar | forte e de sangue quente; vê na penumbra, como o pai orc |
| pequenino | manha · haste | +2 em andar escondido | miúdo e sem medo: o pavor pega pouco nele, e anda sem ser ouvido |
| gnomo | encanto · peso | +2 em abrir fechadura e desarmar | miúdo, curioso e de mão fina; vê na penumbra, e o mecanismo não tem segredo para ele |

### 4.3 Os traços do povo (uma lista fechada nova)

| Traço | O que faz | Por que não o do bicho |
| --- | --- | --- |
| **vê no escuro** | na luta, o escuro tira a **metade**: −2 no golpe, −4 no tiro (e no feitiço que voa). Fora da luta, anda, procura, abre e desarma sem tocha (a regra de A) | o "noturno" do goblin tira o escuro inteiro: medido no gêmeo, no escuro, 62,3%, acima do Grande Dom (59,8%) |
| **resiste a veneno** | o veneno do bicho e da criatura tira a metade por rodada | (não há traço de bicho assim) |
| **coragem** (um número, não um traço) | soma no teste de coragem, como a do povo das criaturas | |

A lista nova mora no `tabelas_povos.py`, ao lado da dos bichos e da magia, e **não liga a luta de magia** (a luta com um anão é a luta de sempre, com duas linhas a mais). **O pavor do dragão, medido na conta exata** (2d20 + Vontade ÷ 10 + coragem + 2 do lado maior, contra 28): o humano de nível 50 foge em 13,75% e fraqueja em 33,75%; o pequenino foge em 3,75% e fraqueja em 22,5%.

### 4.4 O corpo miúdo e a peça sob medida

- **Na luta, o miúdo é do tamanho de gente:** uma vaga no corredor, quatro batem nele, o PV de gente. A regra do "pequeno" dos bichos (PV × 0,6, Defesa +2, dois por vaga), medida no corpo de gente, vence o gêmeo só 30,4%: não serve a um povo de personagem.
- **A armadura tem corpo:** a de gente não serve no miúdo, e a miúda não serve em gente. Vestir a que não serve é recusado, com a frase: "A armadura de malha é de gente grande: não serve no corpo de Pipa. Um ferreiro a ajusta (`oficio.py ajustar`)."
- **O ajuste que já existe resolve:** o `oficio.py ajustar ITEM para=ID` grava o dono e **recorta a peça para o corpo dele** (os blocos e o teste de hoje: o Bento, Treinado, ajusta uma peça Comum em 1 bloco, contra 22). Feita na forja para alguém miúdo (`para=`), a peça já nasce miúda.
- **A arma e o escudo não têm corpo:** o requisito por atributo já cobra (o pequenino de Força 55 paga −1 com a espada e mais com o malho; a adaga e o arco pedem Agilidade).
- **A loja do lugar** tem as armaduras dos corpos da gente dele (seção 4.8); a vila de teste ganha duas miúdas.

### 4.5 A tendência nos talentos

No caminho **a favor**, o d100 do talento rola duas vezes e vale o melhor; no caminho **contra**, duas vezes e vale o pior. A inclinação do personagem, se cair no caminho a favor, soma mais um dado (melhor de três); se cair no contra, os dois se anulam (rola uma vez). Os outros caminhos rolam como hoje, com a mesma chave do dado do mundo: **o humano nasce igual ao de hoje, caminho por caminho.**

| | Negado | Lerdo | Comum | Jeitoso | Prodígio | Jeitoso ou melhor |
| --- | --- | --- | --- | --- | --- | --- |
| como hoje (uma vez) | 2% | 10% | 76% | 10% | 2% | 12% |
| a favor (melhor de dois) | 0,04% | 1,4% | 76,0% | 18,6% | 3,96% | **22,6%** |
| a favor e a inclinação (melhor de três) | 0% | 0,2% | 68,0% | 26,0% | 5,9% | 31,9% |
| contra (pior de dois) | 3,96% | **18,6%** | 76,0% | 1,4% | 0,04% | 1,4% |

Na média, a favor vale **+0,25 de grau** de talento (menos que um grau, como a lei pede). É pressa e teto, nunca poder: o anão nasce mais vezes Jeitoso na forja, e a Lendária segue difícil para ele como para todos.

### 4.6 A vida longa

| Povo | Adulto aos | Velho aos | Vive até (o máximo) |
| --- | --- | --- | --- |
| humano | 16 | 60 | 90 |
| anão | 30 | 200 | 300 |
| elfo | 80 | 500 | 800 |
| meio-orc | 14 | 50 | 75 |
| pequenino | 25 | 80 | 130 |
| gnomo | 35 | 250 | 400 |

**Nesta etapa a idade só se escreve:** a pessoa nasce com ela (o personagem, com a idade de adulto do povo e mais um d10), e o save antigo fica sem idade (não se sabe). O ano que passa, a velhice e a morte de velho são da etapa 7, como a meta 5b do `PROJETO.md` ("nenhuma pessoa viva é mais velha que o seu povo permite") já pede. **Para o herdeiro** (etapa 6): o herdeiro de um elfo pode ser um bisneto, e o anão espera 30 anos para o filho pegar em armas.

### 4.7 A lei, medida

Nível 50, tudo Raro, 4.000 lutas por linha (`m6_saida_v3.txt`); o humano contra o humano é o `m2_saida.txt` (3.000):

| Povo contra o humano de peças iguais | Espada, malha, escudo | No escuro | Contra a arma uma acima | Nível 5, tudo Comum | Arco contra arco, de longe | Adaga e couro | Contra a aranha-de-toca (veneno) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| humano (a régua) | 48,9% | 48,2% | 5,0% | 49,6% | | | 80,1% |
| anão | 53,9% | 58,6% | 5,8% | 52,0% | 49,8% | 51,7% | 85,0% |
| elfo | 47,7% | 53,6% | 4,0% | 44,4% | 50,4% | 49,4% | 77,1% |
| meio-orc | 53,6% | 58,2% | 5,8% | 55,7% | 51,9% | 52,4% | 83,3% |
| pequenino | 48,9% | 47,7% | 4,7% | 41,5% | 49,4% | 50,4% | 79,1% |
| gnomo | 43,8% | 50,2% | 3,8% | 40,4% | 43,6% | 44,9% | 77,2% |
| **o Grande Dom contra o gêmeo** | **59,8%** | | até 15% (10.7) | | | | **83,6%** |

**Como ler:** o anão e o meio-orc são um pouco melhores no aço (o Vigor); o elfo e o pequenino, iguais com a arma deles; o gnomo, pior no aço e melhor na bancada e na magia. **Ninguém passa do Grande Dom**, nem no escuro. O ponto mais perto da linha: o anão contra a aranha (85,0 contra 83,6, dentro do erro do dado), porque o veneno pela metade e o Vigor somam ali; a meta aceita até 2 pontos acima do Grande Dom na mesma condição.
**Como cheguei:** a primeira volta (`m2_saida.txt`) tinha o anão com Vigor +10, que no escuro dava 62,9%, e o gnomo a 35,5% no nível 5; a segunda (`m6_saida.txt`) pôs a coragem +4 no pequenino com Agilidade +10, que passava a 57,9% no arco. Na terceira, os números acima. **O que cada atributo vale** (`m1_saida.txt`): Vigor +10, 56,3% (é o atributo da luta: o PV); Agilidade +10, 53,8%; Força, Vontade e Percepção +10, de 49,5 a 50%.

### 4.8 A gente do mundo

Cada lugar guarda de que povos é a gente dele (`povos`, frações); cada pessoa com nome guarda o dela. **A proposta para o gerador** (etapa 7; aqui é chute):

| Lugar | humano | anão | elfo | meio-orc | pequenino | gnomo |
| --- | --- | --- | --- | --- | --- | --- |
| a capital | 80 | 6 | 3 | 4 | 5 | 2 |
| uma cidade | 85 | 5 | 2 | 3 | 4 | 1 |
| a cidade da serra (os salões dos anões) | 25 | 65 | 0 | 2 | 3 | 5 |
| a vila da floresta funda (o bosque dos elfos) | 30 | 0 | 65 | 0 | 5 | 0 |
| vila e aldeia do campo | 80 | 2 | 1 | 2 | 14 | 1 |
| aldeia da fronteira dos orcs | 70 | 3 | 0 | 25 | 2 | 0 |
| as tocas da colina (os gnomos) | 20 | 10 | 0 | 0 | 10 | 60 |
| **os 40 rivais** (etapa 5) | 70 | 10 | 8 | 6 | 4 | 2 |

A loja de cada lugar põe na prateleira as armaduras dos corpos da gente dele, na proporção.

### 4.9 O personagem do jogador

O jogador escolhe o povo ao nascer, junto com a inclinação: `vila_teste.py PASTA povo=anão` (e, no mundo da etapa 7, nasce numa casa daquele povo). **O povo não se troca depois.** O Maro do `ensaio/` não tem o campo: é humano, e segue humano. O comando que acrescenta a etapa ao save não toca no Maro.

## 5. O estado

**Todo campo novo tem valor padrão: o save antigo abre igual.**

| Onde | Campo | Padrão | O que é | Verbo |
| --- | --- | --- | --- | --- |
| pessoa | `povo` | ausente = humano | o nome do povo (`tabelas_povos.POVOS`) | `['pessoa', ID, 'povo', 'poe', 'anão']`, só em "gera" e "mestre"; no nascer, o registro traz |
| pessoa | `idade` | ausente = não se sabe | os anos | `['pessoa', ID, 'idade', 'poe', 40]` (só "gera" e "mestre" nesta etapa) |
| item | `corpo` | ausente = gente | `miúdo`, só em armadura | `['item', ID, 'corpo', 'poe', 'miúdo' \| None]` (o ajuste e a forja) |
| lugar | `povos` | ausente = toda humana | `{povo: fração}` da gente do lugar | o verbo `lugar` de sempre |
| lugar (ermo ou sala) | `dragao` | ausente = sem dragão | o registro do dragão do covil (abaixo) | `['lugar', ID, 'dragao', 'poe', {...} \| None]` |

**O registro do dragão:** `{nome, tipo, idade, pv (ausente: cheio), dorme_ate (dia), punhados (no sono de agora), vila (o lugar que ele ataca ou cobra), tributo (a estação paga), ult_ataque, ataques, desde}`. **Não guarda prata:** o tesouro é o estoque do lugar (como o covil de hoje).
**O lutador:** o `estado.lutador` leva para a luta os traços e a coragem do povo, **não o nome**: o `povo` do lutador das criaturas é o corpo do goblin (um registro), e misturar os dois quebraria a ficha.
**Os eventos:** um tipo novo, `dragão` (a vida: dormir, acordar, atacar, cobrar, sarar), do mundo sozinho (como o "covil": não é fato do turno). O resto usa os que há: o "gera" e o "mestre" põem o dragão e o tesouro; o "luta" e o "despojo" fazem as contas da luta (o PV de quem fugiu volta ao registro; o morto sai do registro, e o corpo e o núcleo entram).
**Os módulos:** `povos` e `dragoes` entram em `tabelas_mundo.MODULOS` (com os ganchos `virada`, `voce`, `mesa`, `so_mestre`, e um novo, `pode_vestir`, que o `ato.vestir` chama antes de vestir).
**Os invariantes novos** (`estado.valida`; o `fecha` recusa com qualquer um quebrado): o povo de cada pessoa é um povo da tabela; ninguém vivo passa da idade máxima do povo; o `corpo` só existe em armadura e é `miúdo`; **a armadura em uso serve no corpo de quem a veste**; as frações de `povos` somam até 1; o registro do dragão tem tipo e idade da tabela, a vila existe, o PV está entre 1 e o máximo; o mesmo dragão não mora em dois lugares; a prata dos covis do mundo não passa de 25% da prata do mundo.

## 6. Os comandos, a mesa e o SÓ O MESTRE

```
python3 povos.py lista | ver POVO          os povos (o jogador lê para escolher): os atributos, os traços, o corpo, a tendência, a vida, o teste do ladino
python3 vila_teste.py PASTA [comeco=...] [povo=POVO] [nome=...] [inclinacao=...]      a vila nova com o personagem de outro povo
python3 vila_teste.py povos PASTA          acrescenta a metade B da etapa a uma vila que já existe (só por eventos; recusa rodar duas vezes)
python3 dragoes.py lista | ver TIPO IDADE | ameaca TIPO IDADE [arma=CAT] [armadura=CAT]
python3 dragoes.py mede TIPO IDADE NIVEL CATEGORIA [homens=4] [lutas=200] [covil=sim] [dorme=sim]      a régua, em lutas de ensaio
python3 dragoes.py covil [LUGAR]           SÓ O MESTRE: o dragão, o sono, o PV, o tesouro, a vila que ele ataca
python3 dragoes.py covil poe LUGAR TIPO IDADE ["Nome"] [vila=LUGAR] [tesouro=N] [dorme=DIAS]      o Mestre funda um covil (evento "mestre")
```
**Na luta**, o dragão entra no cenário como `{"bicho": "dragão-da-serra-jovem"}` (a tabela) ou `{"dragao": "LUGAR"}` (o do covil, com o PV de agora e acordado ou não). No covil da masmorra, quem monta a luta é a masmorra de A, chamando o `dragoes.monta`.

**O que a MESA mostra:**
- **Você:** o povo do personagem e o que ele faz em uma linha ("Maro, humano"; "Pipa, pequenina: corpo miúdo (a armadura de gente não serve), coragem +4, +2 em andar escondido").
- **Quem está aqui:** cada pessoa com o povo ("Durva (anã), a ferreira de passagem").
- **O que se conta:** de cada dragão que a gente dali conhece, o boato do último ataque ("Conta-se na pousada que o Tição, um dragão jovem da Serra Fria, levou gado de Vau Seco há 6 dias. Vau Seco fica longe: a estrada é da etapa 3."). Sem número, sem tesouro.
- **SÓ O MESTRE:** o registro de cada dragão (o PV, até quando dorme, o tesouro em prata e peças, a vila, o próximo ataque provável, a vigília), e a rolagem oculta do roubo.
- **A ameaça** (`dragoes.py ameaca`) é a frase do chefe: ninguém a sabe de graça; o Mestre a lê quando a cena põe o dragão à frente. Exemplo: "O DRAGÃO JOVEM DA SERRA · grau C (Raro): mata um veterano · grande: fácil de acertar (−2 na Defesa), alcança 2 casas e bate primeiro em quem chega com arma mais curta, 6 batem nele de perto. O corpo: garra, bocarra e cauda Raras; escama Rara, que vale como malha. Sopro: a cada 2 rodadas, em todos a até 4 casas, sem aparo. Voa: a espada tem −6 contra ele. Apavora: quem começa a luta testa a coragem contra 28. Ferido, no covil desce ao chão em fúria (deixa de voar; quem o golpeia de perto se queima); fora dele, foge pelo ar. A conta: arma abaixo de Rara vale um terço na escama dele; em armadura abaixo de Rara, o golpe dele vale o triplo."

**Onde a luta para e pergunta:** as paradas de hoje servem todas (a luta vai começar; o pavor; quem o jogador comanda fraqueja; o chefe muda de fase; o líder do outro lado foge). Nova: **o dragão foge** (é a parada do líder que foge). No roubo (a cena de A), **o dragão acorda** para a descida.

## 7. A vila de teste

```
python3 vila_teste.py povos PASTA
```
Só por eventos, sem recriar nada; recusa rodar duas vezes. O integrador pode juntar este e o `vila_teste.py masmorra` de A num `vila_teste.py fantasia PASTA` que roda os dois (cada um segue recusando rodar duas vezes). Acrescenta:
1. **A gente de outros povos em Pedra Rasa** (com os talentos e os dons rolados com a tendência do povo; um evento do gerador, que é segredo):
   - **Durva**, a anã ferreira de passagem (nível 34; forja Treinada e martelo Treinado; martelo e armadura de couro Incomuns; 40 de prata; 112 anos). Vai junto se chamada, como Tomé.
   - **Brasco**, o meio-orc guarda de caravana de passagem (nível 26; malho Comum, malha Comum; 30 de prata; 31 anos).
   - **Ilvena**, a elfa caçadora de passagem (nível 38; arco e caça Treinados; arco Incomum, adaga Comum, couro Incomum; 25 de prata; 240 anos).
   - **Nena Ramalho**, a pequenina que faz o pão da pousada (nível 9; coleta Iniciante; 12 de prata; 44 anos). Mora na vila.
2. **Pedra Rasa ganha a sua gente:** `povos = {humano: 0,88, pequenino: 0,08, anão: 0,02, meio-orc: 0,02}`; e na prateleira, **duas armaduras miúdas Comuns** (couro e malha, com o elmo).
3. **O dragão longe:** um lugar novo, **a Serra Fria** (ermo, serra, perigo 3, a 6 blocos; **não é vizinho** de Pedra Rasa: não se vai lá até a etapa 3), com **o Tição**, dragão jovem da serra (60 anos), que ainda dorme 20 dias (até o Dia 28, se o comando roda no Dia 8); o tesouro: **300 de prata, a Lâmina de Vau Seco** (espada Rara, do último que o enfrentou) **e um escudo Incomum**. E **Vau Seco**, a aldeia de 120 que ele ataca (com mercado, longe também). O último ataque foi há 6 dias: a pousada conta.
4. **Nada mais muda:** o Maro segue humano; a gente, os itens e o tempo de antes seguem como estavam. A prata que nasce: a das quatro pessoas novas (107), o tesouro (300) e a caixa de Vau Seco (600).

**A vila nova com o personagem de outro povo:** `vila_teste.py PASTA povo=POVO` faz tudo o que faz hoje, com os atributos do começo mais os do povo (340), os traços, a idade, a tendência e, se o corpo é miúdo, as peças do começo miúdas. A mesma semente dá a mesma vila.

## 8. Uma cena jogada

(A luta é a do `luta.py` de verdade, com o que falta emulado: `m10_cena.py`, `m10_saida.txt`. Os comandos são os da proposta; os de A, os do rascunho dele.)

**Dia 8, manhã.** O Mestre roda `vila_teste.py povos ensaio` ("a metade B da etapa 4b entrou na vila: uns 15 eventos, nada recriado") e `turno.py abre`. Na MESA, em "Quem está aqui", aparecem Durva (anã), Brasco (meio-orc), Ilvena (elfa) e Nena (pequenina); em "O que se conta", a linha do Tição: levou gado de Vau Seco há 6 dias, e Vau Seco fica longe. O Maro paga uma refeição a Brasco, que passou por lá com a caravana. O Mestre lê para si a ameaça (`dragoes.py ameaca serra jovem arma=Comum armadura=Comum`): "a sua arma (Comum) na escama dele (Rara): o golpe vale um nono; o golpe dele na sua armadura: vale nove vezes". No SÓ O MESTRE: o Tição dorme até o Dia 28, tem 480 de PV e 300 de prata. Brasco conta o que viu, e o jogador entende sem número: aquilo não é para o nível 5. (A régua confirma: `dragoes.py mede serra jovem 50 Raro homens=1` dá 0,5% a um veterano sozinho.)

**Dia 9.** O Maro quer descer a cripta de A sob a Cova Velha sem tocha, para não ser visto de longe, e chama Durva, que vê no escuro: `masmorra.py descer cripta com=durva ordem=durva,eu luz=nada`. Ela vai na frente; ele, atrás, devagar (a regra de A: quem não vê anda com o dobro dos lances e não procura). No ossário, três esqueletos à toa ouvem a malha do Maro, e ninguém é surpreendido. A luta abre no escuro: o Maro tem −4 no golpe, Durva só −2, e o martelo dela (Incomum, de impacto) passa inteiro nos ossos. **Medido: a casa vence 84,3% e o Maro morre em 18,3%;** sem o traço da anã, 76,4% e 24,8%; com Tomé no lugar dela (humano, de lança), 60,7% e 31,6%. Com a tocha (a luz é de todos), a diferença some (Durva 88,1%, Tomé 83,1%): ver no escuro vale na hora em que falta a luz, e não mais que isso.

**Outro jogo, outra vila:** `vila_teste.py /tmp/pipa povo=pequenino comeco=cacador nome=Pipa`. Pipa nasce com Força 40, Agilidade 75, Vigor 60, Vontade 50, Percepção 75 e Afinidade 40 (340), 27 anos, arco e adaga Comuns e uma armadura de couro miúda. Na loja ela compra a armadura de malha de gente (`mercado.py comprar ITEM`, 30 de prata), e o `ato.py vestir` a recusa: "é de gente grande: não serve no corpo de Pipa". O jogador pede ao Bento (`oficio.py ajustar i0031 para=eu quem=bento`, 1 bloco; o teste contra 22, que o Bento passa 9 vezes em 10), e paga o serviço. A malha ajustada é de Pipa: na mão de outro miúdo, rende uma categoria abaixo (a regra do sob medida). A coragem +4 dela só aparece diante do que apavora (o dragão, a hidra, a alma penada, a múmia, o vampiro): ali Pipa fraqueja em 22,5% das vezes, e o humano em 33,75%.

## 9. As metas do banco

`provas_povos.py` e `provas_dragoes.py`; o `provas_mundo.py` roda os dois. A régua do grupo é a das criaturas (o homem do degrau), com Vontade 80 do Épico para cima.

**A pessoa comum segue igual**
| Meta | O que se mede | Faixa | Como |
| --- | --- | --- | --- |
| CO1 | os bancos de hoje | `provas.py 600`: as 114 de hoje passam; `provas_mundo.py`: as 148 de hoje passam (e as novas, à parte); `estresse.py 1500`: nenhum erro, a primeira linha igual | rodar |
| CO2 | a luta sem povo e sem dragão | igual, número por número, às de hoje | cinco lutas de semente fixa (`dados/semente_fixa_sem_magia.txt`) |
| CO3 | o humano que nasce | a vila de teste nova, com a mesma semente: os humanos com os mesmos atributos, talentos e dons, caminho por caminho | duas vilas, antes e depois |
| CO4 | o save antigo | uma cópia do `ensaio/` abre, o Maro é humano, o `valida` passa; o `vila_teste.py povos` só acrescenta (o que existia sai igual, campo por campo) e recusa rodar duas vezes | a cópia |

**Os povos**
| Meta | O que se mede | Faixa | Como | Medido (rascunho) |
| --- | --- | --- | --- | --- |
| PO1 | cada povo contra o humano de peças iguais: espada, arco, adaga; claro e escuro; nível 5 e 50 | de 40 a 60% em toda linha | 4.000 lutas por linha, com o Grande Dom medido na mesma rodada | de 40,4 a 58,6% |
| PO2 | cada povo contra o humano com a arma uma acima | até 15% | 4.000 | de 3,8 a 5,8% |
| PO3 | o veneno: o anão contra a aranha-de-toca | até o Grande Dom contra a aranha mais 2 pontos | 4.000 | 85,0 contra 83,6 |
| PO4 | a soma dos atributos | a do humano, sempre | todos os povos, todos os começos e moldes | |
| PO5 | a tendência | a favor: Jeitoso ou melhor de 20 a 25%; contra: Lerdo ou pior de 20 a 25%; os outros caminhos e o humano, como hoje | 20.000 nascimentos por povo, pelo dado do mundo | a conta: 22,6% e 22,6% |
| PO6 | o corpo | a armadura de outro corpo é recusada ao vestir; ajustada, serve; a arma e o escudo não têm corpo | os casos, à mão | |
| PO7 | a coragem contra o pavor | o pequenino de nível 50 foge até 6% | a conta e 2.000 lutas contra o jovem | a conta: 3,75% (o humano, 13,75%) |
| PO8 | a idade | ninguém vivo passa do máximo do povo; a vila nova dá ao personagem a idade de adulto do povo | o `valida`, a vila nova | |

**Os dragões**
| Meta | O que se mede | Faixa | Como | Medido (rascunho) |
| --- | --- | --- | --- | --- |
| DR1 | o filhote (foge ferido) contra um homem do degrau, cada tipo em casa | de 40 a 65% | 1.000 lutas | de 52,1 a 61,9% |
| DR2 | do jovem ao ancião, em casa, com a fase, contra 4 do degrau | jovem 50 a 75; adulto 45 a 70; velho 25 a 50; ancião 5 a 25 | 600 por linha | 57,0 a 70,3; 52,8 a 64,0; 31,5 a 41,2; 11,2 a 18,0 (duas rodadas) |
| DR3 | o ancião contra 6 do degrau | de 65 a 90% | 600 | de 78,2 a 84,3% |
| DR4 | a categoria decide: 4 do degrau com o conjunto uma acima; uma abaixo | 90% ou mais; 10% ou menos | 200 por linha | de 99,5 a 100%; de 0 a 1% |
| DR5 | o dragão não se caça sozinho: um homem do degrau contra o jovem ou maior | até 5% | 200 | de 0 a 0,5% |
| DR6 | **a pergunta do pedido:** o jovem da serra no covil contra 4 de nível 50 Raros; com a arma Épica; tudo Incomum | de 55 a 80%; 90% ou mais; até 5% | 600 | 70,3% (0,46 mortos por luta); 95,7%; 0% |
| DR7 | a fase: a luta para e pergunta; no covil o dragão nunca foge; fora dele, o da serra foge ferido | sempre; nunca; de 60 a 95% das lutas | 600 | 79% |
| DR8 | dormindo: o grupo que o surpreende | 5 pontos ou mais | 600 | +10,5 |
| DR9 | o registro e a luta: entra com o PV de agora; morto, sai do registro e o corpo e o núcleo entram no Livro (o núcleo só do adulto para cima); fugido, o PV volta ao registro | sempre | os casos, à mão, num mundo de rascunho | |

**A mina**
| Meta | O que se mede | Faixa | Medido (rascunho) |
| --- | --- | --- | --- |
| MI1 | a prata do mundo: pôr o dragão, um ano da vida dele, a luta, o tesouro levado, a venda | a mesma antes e depois de cada passo (o tesouro posto conta uma vez, no "gera") | fechou em todas as linhas |
| MI2 | o despojo e o tesouro do jovem vendidos em Pedra Rasa | a loja paga até a caixa dela; o preço da matéria Rara cai a cada venda; a peça que a caixa não paga é recusada | 1.229 de 2.000; de 111 a 37; a Épica recusada |
| MI3 | o dragão morto não volta | 364 viradas depois: sem dragão, e o estoque do covil não cresceu | |
| MI4 | o ladrão robô (o teste de A), um punhado por sono, um ano ao lado do jovem e do adulto | morre no ano em 80% das vidas ou mais; tira por dia de vida até 6 de prata (1,5 diária) | 93 a 99%; de 1,3 a 4,5 |
| MI5 | um ano do jovem ao lado de uma aldeia de 120 | perde até 10% do povo e até metade da prata; o tesouro cresce o que a aldeia perde | de 4 a 6%; de 23 a 31% |
| MI6 | os covis juntos | até 25% da prata do mundo | (o gerador da vila de teste; na etapa 7, as 20 sementes) |

## 10. A construção

**Os arquivos novos** (dois construtores, em paralelo, sem arquivo em comum):

| Arquivo | O que expõe | Linhas (chute) | Quem |
| --- | --- | --- | --- |
| `tabelas_povos.py` | `POVOS` (os atributos, os traços, a coragem, o corpo, a tendência, a vida), `TRACOS` (a lista fechada e a frase), `ESCURO` (0,5), `VENENO` (0,5), `MANHA` (o +2 de cada povo nos testes de A), `GENTE` (a composição dos lugares, para o gerador) | 110 | **P** |
| `povos.py` | `povo(p)`, `nasce(registro, povo, sorte)` (os atributos e a idade), `tracos(p)`, `coragem(p)`, `corpo(p)`, `serve(item, p)`, `manha(p, teste)`, `frase(povo)`, os ganchos `pode_vestir`, `voce`, `mesa`; `na_vila(E)` (a metade dos povos da vila de teste); o comando (`lista`, `ver`) | 250 | **P** |
| `provas_povos.py` | CO1 a CO4, PO1 a PO8 | 350 | **P** |
| `tabelas_dragoes.py` | `TIPOS`, `IDADES`, `FASE`, `DESPOJO`, `NUCLEO_DESDE`, `TESOURO`, `VIDA`, `VIGILIA`, `CONTA`, e `ESPECIES` (as 15 chaves, montadas das duas tabelas) | 150 | **D** |
| `dragoes.py` | `dragao(tipo, idade, ...)` (o lutador), `especie(k)`, `ameaca(...)`, `poe(E, ...)`, `virada(E)` (a vida), `monta(E, lid)`, `acordado(E, lid)`, `vigilia(E, lid)`, `punhado(E, lid, pid)`, `depois_da_luta(E, lid, S, campo, quem)`, `na_vila(E)`, os ganchos `mesa` e `so_mestre`, `mede(...)`; o comando | 500 | **D** |
| `provas_dragoes.py` | DR1 a DR9, MI1 a MI6 | 450 | **D** |

**Os arquivos que mudam** (o que este projeto pede a eles; todos ficam com o construtor do alicerce, o mesmo do projeto A, na onda 1):

| Arquivo | O que muda |
| --- | --- |
| `estado.py` | a pessoa: `povo` e `idade` (no nascer e no "mestre"); o item: `corpo`; o lugar: `povos` e `dragao` (o `_lugar_erro` os confere); `especie()` lê também os dragões; o `lutador` leva os traços e a coragem do povo; os invariantes da seção 5 |
| `tabelas_mundo.py` | `EVENTOS` e `MUNDO_SOZINHO` + `dragão`; `MODULOS` + `povos`, `dragoes` |
| `talento.py` | o `_sorteia` com a tendência do povo (a mesma chave do dado: o humano sai igual) |
| `pessoas.py` | aceita os traços do povo (a terceira lista); a ficha de gente leva a coragem |
| `luta.py` | duas linhas: o "vê no escuro" (a metade do escuro, no golpe e no tiro) e o "resiste a veneno" (a metade) |
| `magia.py` | a fase `foge` (com a fúria no lugar, quando não pode fugir); o feitiço que voa no escuro, para quem vê no escuro, pela metade |
| `bichos.py` | `especie()` e o atalho do cenário leem os dragões; o despojo do dragão (o núcleo só do adulto para cima) |
| `ato.py` | o `vestir` chama o gancho `pode_vestir` antes de montar o evento |
| `oficio.py` | o `ajustar` recorta o `corpo` da armadura para o dono; a armadura forjada `para=` alguém miúdo nasce miúda |
| `turno.py` | o `secreto` leva ao SÓ O MESTRE o evento que põe o dragão e o tesouro |

São perto de **1.800 linhas novas e 150 mudadas**.
**Onda 1, o alicerce** (um construtor para as duas metades, como A propõe): os arquivos acima, mais os de A; entrega o contrato entre `masmorra.py`, `manha.py`, `povos.py` e `dragoes.py` (os nomes das funções da seção 11).
**Onda 2, em paralelo:** **P** (os povos) e **D** (os dragões), ao lado de M e L do projeto A. O D usa o `masmorra.py` só pelo contrato; até ele chegar, testa o covil-ermo.
**Onda 3, a integração** (um construtor): o `vila_teste.py` (o `povos`, o `povo=` da vila nova, e o `fantasia` que junta com o `masmorra` de A), o `provas_mundo.py`, os capítulos novos do `REGRAS.md` (o 19, os dragões; o 20, os povos; os 17 e 18 são de A), o `GUIA_VILA.md`, o `MUDANCAS.md` e o `LEIA.md`; joga uma cópia do `ensaio/` com as duas metades.
**Depois:** o revisor e o verificador, como na etapa da magia.

## 11. Onde toco o outro projeto

**O que preciso do projeto A:**
1. **O covil do dragão como masmorra** (o molde `covil`): a câmara do tesouro aberta, com o `chefe` dele e o meu `dragao` na sala; a masmorra chama `dragoes.monta(E, sala)` para pôr o dragão na luta (com o PV de agora, dormindo ou não), põe `sem_saida` do lado do dragão no cenário da câmara, e chama `dragoes.depois_da_luta` nas contas. O tesouro é o estoque e as peças guardadas da sala (a regra da seção 6 de A).
2. **O teste de andar escondido** (`manha.testa`), que eu uso no roubo, com o meu número do lado do dragão (`dragoes.vigilia`) e o meu punhado (`dragoes.punhado`).
3. **A tocha e o escuro** da masmorra: é o que dá valor ao meu "vê no escuro".

**O que respondo ao que A pediu:**
1. **Quem vê no escuro NÃO leva o "noturno" na luta.** Medido: o noturno no gêmeo, no escuro, vence 62,3%, acima do Grande Dom (59,8%). O povo leva o traço novo **"vê no escuro"**: na luta, o escuro tira a metade (−2 no golpe, −4 no tiro). **Fora da luta** vale o que A escreveu: anda, procura, abre e desarma sem luz, e o grupo em que todos veem no escuro dispensa a tocha (e a pena de −6 dela). Com tocha, ninguém tem o escuro, e o traço não soma nada.
2. **O pequenino não toma meia vaga.** Na luta, o corpo miúdo é do tamanho de gente; a regra do "pequeno" dos bichos, medida no corpo de gente, vence 30,4%. Se A quiser, a passagem estreita "só para miúdos" é uma boa porta de masmorra (o pequenino e o gnomo passam; gente, não).
3. **O +2 de cada povo nos testes do ladino** (o teto de A: um grau de manha): o pequenino em andar escondido; o elfo em achar; o anão em achar a armadilha e a passagem de pedra (na cripta, na mina, na ruína); o gnomo em abrir fechadura e desarmar; o meio-orc em arrombar; o humano, nada. Mora no `tabelas_povos.MANHA`; o `manha.testa` soma. A **tendência do pequenino** é a favor da `manha` (o 17º caminho de A).
4. **O roubo do covil: a vigília de A é branda demais para o dragão.** Com "dormindo, −6", um ladino Treinado no escuro leva o tesouro inteiro (os seis punhados) em 49 a 65% das vezes. Proponho, só para o dragão: 20 + Percepção ÷ 10 **+ 2** (dorme leve sobre o ouro) **e +2 por punhado já tirado no mesmo sono**; e o dragão que acorda age antes da fuga (seção 3.4). Medido: 1,2 a 1,5 punhados em média por sono, e o ladrão robô morre no ano em 93 a 99%.
5. **As galerias não ajudam o grupo contra o dragão.** A disse que nelas o dragão luta apertado e não voa: é verdade, e mesmo assim o grupo perde mais lá (o jovem: 70% na câmara aberta, 64% num corredor de 2, 53% num de 1; o adulto, enorme: 64%, 52% e 17%), porque bate menos gente num bicho só. Ao contrário dos esqueletos de A, contra o dragão se luta na câmara aberta.

**O que ofereço a A:** o dragão (o chefe de covil de toda categoria, do Incomum ao Lendário, com fase e núcleo); a régua (`dragoes.py mede`); a anã Durva, que vai junto na cripta e vê no escuro (a cena da seção 8 usa a cripta de A); e uma sugestão: o **Quim**, o ladino de A (o sobrinho do Lino), pode ser pequenino (de criação), se A gostar: o passo leve e a tendência na manha casam com ele.

**Os arquivos que os dois tocam** (`estado.py`, `tabelas_mundo.py`, `talento.py`, `pessoas.py`, `luta.py`, `turno.py`, `oficio.py`, `vila_teste.py`) ficam com um construtor só por onda, como A propõe.

## 12. Os ganchos

- **Os dragões como frente e calamidade (etapa 6).** O jovem que ataca é uma frente de ameaça pronta: o relógio de 6 passos são os ataques que crescem (o gado, a gente, a vila que queima), e a missão que tira um passo é matá-lo ou espantá-lo. O que fugiu ferido volta e **lembra de quem o feriu** (o nêmesis do dragão). O adulto e o velho são frentes de falta (o tributo empobrece a vila: a prata vai para o tesouro). O ancião acordando é **calamidade**: o fim do sono dele é o passo 1. E **o que dorme** (o Mítico, um no mundo) é a calamidade das calamidades: o núcleo Mítico, que ninguém forja ainda.
- **Os povos na história de 400 a 1.000 anos (etapa 7).** O elfo vivo lembra o que a crônica conta: é a testemunha de 600 anos (a gente do mundo conta o que sabe, e o elfo sabe mais). Os salões dos anões têm dinastias longas; o meio-orc nasce das guerras com os orcs da história. **O dragão envelhece na história:** o jovem de 500 anos atrás é o velho de hoje, e o tesouro dele é o tributo de séculos; as peças contadas que somem na história acabam no covil dele (a cadeia de donos sem buraco). A idade máxima de cada povo é a meta 5b.
- **Os rivais de outros povos (etapa 5).** Os 40 rivais nascem pela tabela da seção 4.8: uma das três Lendas vivas pode ser uma elfa de 600 anos que já enfrentou o ancião. A conta rápida dos rivais (erro menor que 8 pontos) usa o povo como usa a ficha: os traços e os atributos já estão nela.

## 13. O que fica de fora

- O **ovo de dragão** (e o dragão que cria); o dragão que fala, negocia ou lança feitiços; montar dragão; o dragão aliado.
- O **meio-elfo** e o personagem de povo das criaturas (goblin, orc).
- A **opinião e o preconceito** entre povos (a memória da gente é da etapa 3).
- O **ano que passa**, a velhice e a morte de velho (etapa 7: a idade só se escreve).
- O **mar** e o dragão do mar; o sopro de outro tamanho por idade (o alcance segue 4 casas em todos: a categoria já faz o sopro do ancião 81 vezes o do filhote).
- O **dragão do capítulo 6** segue nas tabelas da caça (o banco o usa): o gerador da etapa 7 põe covis no lugar dele.
- O **gerador da região** (quantos dragões, onde, que tesouro, que gente em cada lugar): fica a tabela e as metas; a conta é da etapa 7.

## 14. O que é chute, e os riscos

**Chute** (número que pus e não medi contra nada):
- o tamanho dos tesouros (1, 3, 6 e 10% da prata do mundo; 25% somados) e quantos dragões há numa região;
- a vida do dragão: os dias de sono, o gado, a prata e os mortos do ataque, as taxas do tributo (medi só o protótipo de um ano, não o mundo de vários anos);
- a vigília do dragão (o +2 e o +2 por punhado): a conta é exata, mas depende do teste de A, que pode mudar;
- os anos de cada idade do dragão e a vida longa de cada povo;
- a gente do mundo por lugar e os rivais por povo (seção 4.8);
- os caminhos da tendência de cada povo (são gosto: o anão na forja é o clássico; o contra de cada um, escolhi eu);
- os nomes (Durva, Brasco, Ilvena, Nena, o Tição, a Serra Fria, Vau Seco).

**Os riscos:**
1. **O que emulei pode medir diferente construído.** O "vê no escuro", o "resiste a veneno", a coragem e a fase "foge" rodaram por embrulho no rascunho. O banco (PO1 a PO3, DR6, DR7) mede de novo; se o escuro passar de 60%, o traço vira um terço do escuro, e não a metade.
2. **O anão contra o veneno está na linha** do Grande Dom (85,0 contra 83,6): a meta dá 2 pontos de folga. Se cair fora, o veneno passa a tirar dois terços (e não a metade).
3. **A luta com dragão é longa e mata muito** (o ancião: de 1,8 a 1,9 mortos por luta de quatro). É de propósito, mas o jogador pode achar duro: a pergunta 2 deixa o dragão fugir em vez de levar o grupo.
4. **O tributo drena as vilas:** de 11 a 15% da prata por ano, para sempre, sem a etapa 3 repor prata. Num mundo de vários anos, a vila do adulto fica sem prata para pagar salário. A frente (etapa 6) e a prata nova (etapa 3) têm de cuidar disso.
5. **O tesouro grande é prata, não peça:** matar o velho ou o ancião dá milhares de prata a quem o mata. Como o item decide e a loja só tem o que tem, a prata compra pouco poder; mas compra serviço e gente (etapa 3), e pode desequilibrar lá.
6. **Arquivos em comum com A** (oito): um construtor por arquivo por onda, ou haverá conflito.
7. **A magia contra os velhos:** o "resiste" do velho e do ancião deixa o mago fraco contra eles. Não medi o mago no grupo contra o dragão.
8. **O miúdo e a loja:** a loja farta conta a armadura miúda e a de gente como iguais (o feitio não olha o corpo). É pequeno, e fica dito.
9. **A MESA cresce** (já passa de 13 KB): o povo de quem está aqui e o boato do dragão somam umas 3 linhas.

## 15. As perguntas ao jogador (só gosto; o resto eu decidi pela conta)

1. **O humano ganha alguma coisa?** Hoje o humano é a medida de todos (a lei pede: a pessoa comum segue igual), e os outros povos têm traços com troca. a) o humano fica como está, sem nada a mais; b) **o personagem humano ganha uma segunda inclinação** (só o personagem; a gente do mundo segue igual: é pressa de aprender, não poder). **Recomendo b:** assim escolher humano é escolher aprender duas coisas depressa, e a lei não muda.
2. **O dragão ferido foge?** a) **foge fora do covil, se voa, e luta até morrer no covil** (medido: em campo aberto, o jovem da serra foge em 79% das lutas que perderia; volta ao covil, sara, e lembra de você); b) nunca foge: todo dragão luta até morrer; c) foge sempre que pode, até do covil, e o tesouro fica. **Recomendo a:** quem quer o núcleo vai ao covil, onde ele defende o ouro até o fim; quem o fere na estrada ganha um inimigo.
3. **O dragão jovem na vila de teste:** a) **longe, só se conta:** ataca Vau Seco, que o Maro não alcança, e a pousada fala dele; b) ataca Pedra Rasa de tempos em tempos (cerca de uma vez por mês: gado, um pouco de prata, às vezes um morto), e o Maro não tem como enfrentá-lo; c) não entra agora. **Recomendo a:** o mundo fica maior que a vila, e o dragão espera o dia em que houver estrada e peça para ele.
4. **A armadura de outro tamanho:** a) **não serve até um ferreiro ajustar** (1 bloco e o teste de hoje); b) serve, rendendo uma categoria abaixo até ajustar; c) não há tamanho de peça (o pequenino veste a armadura de gente). **Recomendo a:** é o custo de ser miúdo, e não mexe na luta (a b faria o povo pesar uma categoria, o que a lei proíbe).

## Anexo: o rascunho das duas páginas de números

```python
# tabelas_povos.py (rascunho)
POVOS = {   # mods: soma zero · tracos: a lista fechada daqui · coragem: soma no teste de coragem · corpo: gente ou miúdo
            # a favor / contra: o caminho da tendência (melhor de dois / pior de dois) · vida: (adulto aos, velho aos, máximo)
    'humano':    dict(mods={}, tracos=[], coragem=0, corpo='gente', a_favor=None, contra=None, vida=(16, 60, 90)),
    'anão':      dict(mods=dict(Vigor=5, Vontade=5, Agilidade=-5, Percepção=-5), tracos=['vê no escuro', 'resiste a veneno'], coragem=0, corpo='gente',
                      a_favor='forja', contra='verde', vida=(30, 200, 300)),
    'elfo':      dict(mods=dict(Agilidade=10, Percepção=10, Afinidade=5, Vigor=-5, Força=-10, Vontade=-10), tracos=['vê no escuro'], coragem=0, corpo='gente',
                      a_favor='tiro', contra='peso', vida=(80, 500, 800)),
    'meio-orc':  dict(mods=dict(Força=10, Vigor=5, Afinidade=-10, Vontade=-5), tracos=['vê no escuro'], coragem=0, corpo='gente',
                      a_favor='peso', contra='encanto', vida=(14, 50, 75)),
    'pequenino': dict(mods=dict(Força=-15, Agilidade=5, Percepção=5, Vontade=5), tracos=[], coragem=4, corpo='miúdo',
                      a_favor='manha', contra='haste', vida=(25, 80, 130)),
    'gnomo':     dict(mods=dict(Afinidade=10, Percepção=5, Força=-10, Vigor=-5), tracos=['vê no escuro'], coragem=0, corpo='miúdo',
                      a_favor='encanto', contra='peso', vida=(35, 250, 400)),
}
TRACOS = {'vê no escuro': 'o escuro tira a metade: −2 no golpe, −4 no tiro', 'resiste a veneno': 'o veneno tira a metade por rodada'}
ESCURO = 0.5                # a fração do escuro que pesa em quem vê no escuro
VENENO = 0.5                # a fração do veneno que pesa em quem resiste
CORPOS = ('gente', 'miúdo')
MANHA = {'pequenino': {'escondido': 2}, 'elfo': {'achar': 2}, 'anão': {'achar_pedra': 2}, 'gnomo': {'gazua': 2, 'desarmar': 2}, 'meio-orc': {'arrombar': 2}}   # o teto de A: +2
```

```python
# tabelas_dragoes.py (rascunho)
IDADES = {   # cat · tamanho · nível · instinto · (Força, Agilidade, Vigor, Vontade, Percepção, Afinidade) · armas · traços · anos · chefe
    'filhote': dict(cat=1, tamanho='médio',  nivel=30,  instinto=2, at=(70, 80, 70, 50, 70, 40),    armas=['garra', 'presa'],            tracos=['sopro'],                                anos=(0, 30),       chefe=False),
    'jovem':   dict(cat=2, tamanho='grande', nivel=80,  instinto=6, at=(120, 70, 150, 60, 75, 45),  armas=['garra', 'bocarra', 'cauda'], tracos=['sopro', 'apavora'],                     anos=(30, 150),     chefe=True),
    'adulto':  dict(cat=3, tamanho='enorme', nivel=110, instinto=6, at=(140, 70, 150, 80, 85, 50),  armas=['garra', 'bocarra', 'cauda'], tracos=['sopro', 'apavora', 'couraça'],          anos=(150, 500),    chefe=True),
    'velho':   dict(cat=4, tamanho='enorme', nivel=160, instinto=6, at=(160, 70, 200, 90, 90, 55),  armas=['garra', 'bocarra', 'cauda'], tracos=['sopro', 'apavora', 'couraça', 'resiste'], anos=(500, 1000),   chefe=True),
    'ancião':  dict(cat=5, tamanho='enorme', nivel=220, instinto=8, at=(180, 70, 240, 100, 90, 60), armas=['garra', 'bocarra', 'cauda'], tracos=['sopro', 'apavora', 'couraça', 'resiste'], anos=(1000, None),  chefe=True),
}
TIPOS = {
    'serra':  dict(nome='o dragão da serra', habitat=['serra', 'ruína'], mais=['voa'], sopro='o fogo', casa={},
                   fase=dict(abaixo=0.3, foge=True, perde=['voa'], ganha=['ardente'], diz='desce ao chão em fúria')),
    'brejo':  dict(nome='o verme do brejo', habitat=['brejo'], mais=['veneno'], sopro='o bafo podre', casa=dict(tempo=['água']),
                   fase=dict(abaixo=0.5, ganha=['agarra'], diz='enrosca na lama'), peconha=True),
    'grutas': dict(nome='o dragão das grutas', habitat=['caverna', 'ruína'], mais=['noturno', 'agarra'], sopro='a brasa e a fumaça', casa=dict(tempo=['escuro']),
                   fase=dict(abaixo=0.5, ganha=['dreno'], diz='bebe o sangue de quem prende')),
}
DESPOJO = {'filhote': {'comida': 4, 'couro:1': 3, 'osso:1': 2}, 'jovem': {'comida': 10, 'couro:2': 5, 'osso:2': 4},
           'adulto': {'couro:2': 8, 'osso:2': 6}, 'velho': {'couro:2': 10, 'osso:2': 8}, 'ancião': {'couro:2': 12, 'osso:2': 10}}
PECONHA = {'filhote': {'peçonha:1': 1}, 'outros': {'peçonha:2': 2}}           # só o verme do brejo
NUCLEO_DESDE = 3            # o núcleo (o coração) só do Épico para cima: a escada da forja não pede núcleo abaixo disso
SARA_DORMINDO = 0.10        # o dragão ferido sara isto do PV por dia de sono
TESOURO = {'jovem': (0.01, (2, 3), 2), 'adulto': (0.03, (3, 5), 3), 'velho': (0.06, (4, 6), 4), 'ancião': (0.10, (5, 8), 5)}   # a prata (fração da prata do mundo), as peças, a melhor categoria
TESOURO_MUNDO = 0.25        # todos os covis juntos
VIDA = {    # dorme: dias de sono depois de comer · come: gado de um ataque · prata e mata: (de, até) · tributo: fração da prata da vila por estação
    'jovem':  dict(dorme=(20, 40), come=30, prata=(5, 20), mata=(0, 1), tributo=0),
    'adulto': dict(dorme=(30, 60), come=60, prata=(20, 60), mata=(0, 3), tributo=0.03),
    'velho':  dict(dorme=(90, 180), come=120, prata=(50, 150), mata=(1, 5), tributo=0.05),
    'ancião': dict(dorme=(300, 400), come=200, prata=(100, 300), mata=(2, 8), tributo=0.08),
}
VIGILIA = dict(base=20, leve=2, sobe=2)      # contra 20 + Percepção ÷ 10 + 2, e +2 a cada punhado tirado no mesmo sono (o teste do ladrão é o de A)
CONTA = dict(filhote=(0, 2), jovem=(1, 3), adulto=(1, 2), velho=(0, 1), ancião=(0, 1))   # numa região de 16 lugares (para o gerador da etapa 7)
```
