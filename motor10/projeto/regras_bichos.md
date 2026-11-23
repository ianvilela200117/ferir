# OS BICHOS (etapa 2)

Capítulo para o `REGRAS.md` (o número 6 é provisório: quem monta o livro o acerta). Os números moram no `tabelas_bichos.py`; as provas, no `provas.py` (bloco OS BICHOS).
A luta é a do capítulo 3, sem tirar nada: o `luta.py` roda o bicho como roda gente. O comando para olhar é o `bichos.py`; ele não rola dado de jogo nem mexe em save.

## 6. Os bichos

6.1 **O bicho é uma ficha de luta.** Tem os seis atributos, nível e **instinto**, que é a maestria dele (Leigo 0 a Lendário 8) e vale tudo o que a maestria vale: acerto, Defesa, a ação a mais, as reações. As contas são as do capítulo 1. Muda só o que vem do corpo e do tamanho:

| | Conta |
| --- | --- |
| PV | (Vigor × 2 + nível ÷ 4) × o do tamanho |
| Acerto | instinto + (bônus de Força + bônus de Agilidade) ÷ 4 + o bônus da categoria do corpo |
| Defesa | 22 + bônus de Agilidade ÷ 2 + instinto ÷ 2 + a do couro + a do tamanho + o bônus da categoria do corpo (o corpo apara) |
| Fôlego, força do golpe, ações, reações, iniciativa | como gente (a iniciativa leva a do couro) |

6.2 **O corpo é a arma.** O valor (× 1, 3, 9, 27...) e o bônus de acerto saem da **categoria do corpo**; o alcance, do tamanho. A regra de ouro (2.3) vale igual: conta a diferença entre a arma de quem bate e a armadura de quem apanha. O golpe do corpo entra na tabela do golpe contra o material (2.6) como o de qualquer arma. Quem tem mais de uma arma alterna, golpe a golpe.

| Arma do corpo | Dado | Golpe | Fôlego |
| --- | --- | --- | --- |
| dente | 1d4 | ponta | 1 |
| casco | 1d4 | impacto | 1 |
| presa, ferrão | 1d6 | ponta | 1 |
| garra | 1d8 | corte | 1 |
| chifre | 1d10 | ponta | 2 |
| cauda | 1d10 | impacto | 2 |
| bocarra | 1d12 | ponta | 2 |

6.3 **O corpo é a armadura.** Cobre o corpo todo, a cabeça também. Vale como um material de armadura da categoria do corpo, sem pedir Força, sem custar fôlego e sem esquentar no calor:

| Couro | Vale como | Proteção | Defesa | Iniciativa |
| --- | --- | --- | --- | --- |
| pelo | couro | 0,7 do valor | +3 | +2 |
| escama | malha | o valor | 0 | 0 |
| carapaça | placa | 1,4 do valor | −2 | −2 |

Mirar a fresta (3.5) vale contra o bicho de categoria maior que a arma, menos contra o de couraça.

6.4 **O corpo não é peça.** Não está no Livro de Itens, não tem dono, não quebra, não gasta e não ocupa sintonia. O bicho ferido no braço não larga arma nenhuma.
**Mas o aço gasta nele** (2.10): a arma de categoria menor que o corpo, aparada por ele, perde 1; o golpe que não tira nada gasta a arma; a armadura de quem apanha de um corpo de categoria maior gasta.

6.5 **O tamanho.**

| Tamanho | PV | Alcança | Batem nele por rodada (de perto · de haste) | Toma de um corredor | Defesa |
| --- | --- | --- | --- | --- | --- |
| pequeno | × 0,6 | 1 casa | 2 · 1 | meia vaga | +2 |
| médio (e gente) | × 1 | 1 casa | 4 · 2 | 1 vaga | 0 |
| grande | × 1,5 | 2 casas | 6 · 3 | 2 vagas | −2 |
| enorme | × 2,5 | 3 casas | 8 · 4 | 3 vagas | −4 |

- **O alcance bate primeiro** (3.6): o grande e o enorme dão o golpe livre em quem entra no alcance deles com arma mais curta.
- **Apertado:** o bicho que toma mais vagas do que o corredor tem fica sozinho na casa e luta com −2 no acerto e na Defesa por vaga que falta. Dois pequenos cabem numa vaga.
- **Ninguém derruba nem agarra quem é maior que ele.** Vale para os traços e para o efeito "derruba" das armas. A ferida na perna (3.12) derruba qualquer um.
- Num corredor, só troca de lugar quem toma o mesmo tanto.

6.6 **Os traços.** A lista é fechada: são dez, e a luta roda todos. Traço fora da lista é recusado antes de qualquer dado.

| Traço | O que faz |
| --- | --- |
| matilha | O golpe que fere um alvo em que outro da matilha já bateu nesta rodada o derruba. Com outro da matilha de pé, +4 na coragem. |
| bote | Na primeira rodada, +20 na iniciativa. O primeiro golpe dele na luta tem +8 e rola os dados 3 vezes; quem ele ferir vai ao chão e perde 1 ação. |
| investida | O golpe dado depois de correr 2 casas ou mais desde o último tem +8, rola os dados 3 vezes e derruba quem ferir. |
| veneno | O golpe do corpo que fere envenena: por 4 rodadas a vítima perde, no fim de cada uma, metade do que o golpe tirou, e tem −2 no acerto. Não acumula: vale a pior mordida, e o prazo recomeça. O que sobra corre depois da luta: deixa por um fio (1 de PV), mas sozinho não mata. |
| agarra | O golpe que fere quem está **colado** agarra (um de cada vez). O agarrado não anda, não recua, não troca de lugar, e tem −4 no acerto e −4 na Defesa. O bicho bate primeiro em quem agarrou, e só solta quando passa um turno sem feri-lo, cai, foge ou se afasta. |
| voa | Arma de alcance 1 tem −6 contra ele. A linha não o segura, não leva golpe livre ao se afastar nem ao fugir, e não pisa a lama nem a água. Num corredor, no chão ou agarrado, não voa. |
| regenera | No começo de cada turno dele, recupera 15% do PV máximo. |
| apavora | Quando a luta começa, quem não é de ferro, do outro lado, testa a coragem contra 28 (3.14). |
| couraça | Não tem fresta: ninguém mira a fresta nele, e o crítico não corta a proteção dele pela metade. |
| sopro | Uma rodada sim, uma não, por 3 de fôlego: um ataque em cada inimigo a até 4 casas, de 1d8 com o valor da categoria do corpo e força fixa de 1,2. Não se apara (conta só a Defesa sem escudo e sem arma), não olha o material da armadura, e ninguém se põe na frente. O tempo e a cobertura valem como num tiro. O bicho sopra quando pega dois ou mais, ou quando não alcança ninguém de outro jeito. |

6.7 **A moral do bicho.** O bicho não fica abalado nem se rende: **luta ou foge.**
Testa 2d20 + bônus de Vontade + a coragem da espécie (+2 com o alfa de pé; +2 se o lado dele tem mais gente de pé; −4 se o outro tem o dobro; +4 da matilha):

| O susto | Contra |
| --- | --- |
| levou a primeira ferida (3.12) | 26 |
| está abaixo de um quarto do PV | 26 |
| viu um golpe terrível num do bando, a 2 casas | 24 |
| metade do lado dele caiu | 26 |
| o alfa caiu ou fugiu | 29 |

Cada susto testa uma vez por luta; o golpe terrível, uma vez em cada rodada em que acontece.

- **Falhou, foge:** sai da luta, e leva um golpe livre de quem o alcança (quem voa, não).
- **Encurralado** (o lado dele não tem saída): não foge. Na primeira falha fica encurralado e luta até o fim, com +2 no acerto.
- **O chefe não testa.**
- **Ninguém se rende a um bicho:** quem quebraria se rendendo (3.14) foge; sem saída, fica abalado e luta.
- **Quem ficou com o campo não testa a coragem:** sem inimigo de pé, ninguém foge nem se rende. (Vale para gente também.)

6.8 **O grau** é o que o caçador lê. Casa com a categoria do corpo, e fala de **um** bicho contra um homem do mesmo degrau (o conjunto da categoria do bicho). O bando pesa mais.

| Grau | Categoria | O que diz |
| --- | --- | --- |
| F | Comum | presa: sozinha quase nunca derruba um homem armado, mas o golpe de sorte abre ferida |
| E | Comum | perigo para quem está sozinho e mal armado |
| D | Incomum | perigo para um homem armado |
| C | Raro | mata um veterano |
| B | Épico | pede um grupo |
| A | Único | pede um grupo de mestres |
| S | Lendário | calamidade |

6.9 **As espécies** (catorze; cada uma é uma linha do `tabelas_bichos.py`).

| Espécie | Grau | Categoria | Tamanho | Nível | Instinto | O corpo: armas · couro | Traços | Coragem | Anda | Onde vive |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ratazana | F | Comum | pequeno | 3 | Leigo | dente · pelo | matilha | −2 | 3 a 6 | brejo, ruína, caverna |
| corça | F | Comum | médio | 4 | Leigo | casco · pelo | — | −6 | 1 a 2 | floresta, campo |
| javali | E | Comum | médio | 10 | Leigo | presa · pelo | investida | +4 | só | floresta, brejo |
| lobo | D | Incomum | médio | 20 | Iniciante | presa · pelo | matilha | 0 | 3 a 5, com alfa | floresta, serra, campo |
| surucucu | D | Incomum | médio | 25 | Iniciante | dente · escama | bote, veneno | +2 | só | brejo, floresta, ruína |
| urso | D | Incomum | grande | 35 | Treinado | garra, presa · pelo | agarra | +2 | só | floresta, serra, caverna |
| aranha-de-toca | C | Raro | médio | 45 | Iniciante | ferrão · carapaça | veneno | +2 | 2 a 3 | caverna, ruína, floresta |
| pantera | C | Raro | médio | 50 | Mestre | garra, presa · pelo | bote | +4 | só | floresta, serra |
| grifo | C | Raro | grande | 55 | Mestre | garra, presa · pelo | voa | +2 | 1 a 2 | serra |
| trasgo | C | Raro | grande | 55 | Iniciante | garra · pelo | regenera | +2 | só | brejo, caverna, ruína |
| basilisco | B | Épico | grande | 90 | Mestre | presa, cauda · escama | couraça, veneno | +4 | só | ruína, caverna, brejo |
| serpe | B | Épico | enorme | 100 | Treinado | bocarra, cauda · escama | sopro, veneno | chefe | só | serra, ruína |
| hidra | A | Único | enorme | 150 | Mestre | bocarra · escama | regenera, veneno, apavora | chefe | só | brejo, ruína |
| dragão | S | Lendário | enorme | 220 | Lendário | garra, bocarra, cauda · escama | voa, sopro, couraça, apavora | chefe | só | serra, ruína |

Na tabela e no cenário, a aranha-de-toca é `aranha` (o comando aceita os dois nomes).

A ficha que sai da conta, e o que o bicho inteiro rende:

| Espécie | Força · Agilidade · Vigor · Vontade · Percepção | PV | Fôlego | Acerto | Defesa | Golpe (dado × valor) | Despojo |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ratazana | 35 · 70 · 35 · 30 · 55 | 42 | 9 | +2,5 | 30,5 | 1d4 × 1 | 1 de comida, 1 de couro Comum |
| corça | 45 · 70 · 45 · 30 · 70 | 91 | 10 | +2,75 | 28,5 | 1d4 × 1 | 6 de comida, 2 de couro Comum, 1 de osso Comum |
| javali | 70 · 50 · 100 · 50 · 45 | 202 | 16 | +3 | 27,5 | 1d6 × 1 | 6 de comida, 2 de couro Comum, 2 de osso Comum |
| lobo | 60 · 75 · 40 · 40 · 70 | 85 | 10 | +9,25 | 33,5 | 1d6 × 3 | 3 de comida, 2 de couro Incomum, 1 de osso Incomum |
| surucucu | 60 · 90 · 60 · 40 · 70 | 126 | 12 | +9,75 | 31,5 | 1d4 × 3 | 2 de comida, 2 de couro Incomum, 1 de osso Incomum |
| urso | 100 · 50 · 80 · 50 · 50 | 252 | 14 | +11,75 | 31,5 | 1d8 × 3 · 1d6 × 3 | 10 de comida, 4 de couro Incomum, 2 de osso Incomum |
| aranha-de-toca | 50 · 80 · 40 · 40 · 60 | 91 | 10 | +13,25 | 33 | 1d6 × 9 | 1 de couro Raro, 1 de osso Raro |
| pantera | 100 · 95 · 100 · 50 · 80 | 212 | 16 | +18,75 | 40,5 | 1d8 × 9 · 1d6 × 9 | 4 de comida, 2 de couro Raro, 1 de osso Raro |
| grifo | 95 · 85 · 85 · 55 · 90 | 274 | 14 | +18,25 | 38 | 1d8 × 9 · 1d6 × 9 | 6 de comida, 2 de couro Raro, 2 de osso Raro |
| trasgo | 80 · 45 · 105 · 50 · 40 | 334 | 16 | +13 | 34 | 1d8 × 9 | 3 de couro Raro, 3 de osso Raro |
| basilisco | 100 · 65 · 100 · 60 · 60 | 333 | 16 | +22 | 38 | 1d6 × 27 · 1d10 × 27 | 5 de couro Raro, 4 de osso Raro |
| serpe | 85 · 60 · 75 · 70 · 70 | 437 | 13 | +19,5 | 35 | 1d12 × 27 · 1d10 × 27 · sopro 1d8 × 27 | 12 de comida, 6 de couro Raro, 5 de osso Raro e **um núcleo Épico** |
| hidra | 120 · 55 · 110 · 80 · 70 | 642 | 17 | +26,25 | 39,5 | 1d12 × 81 | 8 de couro Raro, 6 de osso Raro e **um núcleo Único** |
| dragão | 180 · 70 · 240 · 100 · 90 | 1.337 | 30 | +34,25 | 45,5 | 1d8, 1d12, 1d10 × 243 · sopro 1d8 × 243 | 12 de couro Raro, 10 de osso Raro e **um núcleo Lendário** |

6.10 **O bando.** Quantos andam juntos sai do acaso do mundo, entre os dois números da espécie. No bando de alfa (o lobo), o primeiro é o líder: caído ou fugido ele, os outros testam a coragem contra 29.

6.11 **O despojo** sai da tabela: de cada bem, **de metade (arredondada para cima) ao inteiro**, pelo acaso do mundo. A matéria tem a categoria do bicho, até o Raro; do Épico para cima, o corpo rende matéria Rara.
**Só o chefe dá núcleo:** sempre um, da categoria dele. O núcleo é item do Livro de Itens (2.1; tipo `nucleo`), com a espécie de que veio, e nasce por evento, com dono ou com lugar.
Rende despojo o bicho que ficou no campo de quem venceu, morto ou caído. O que fugiu não rende. Tirar o bicho da contagem do ermo e pôr o despojo na carga é ato da caça, por evento.

6.12 **A ameaça** é a frase que o caçador lê **antes** da luta (`bichos.ameaca`). Diz: o grau e o que ele quer dizer; a categoria; o tamanho e o que ele muda; quantos são; o corpo; cada traço, com os números; o que se sabe da espécie; se foge ou se é chefe; e a conta da regra de ouro. Com a categoria da arma e da armadura de quem lê, a conta já vem feita.
Da espécie que anda em bando, avisa que o grau é o de um só, quantos batem num homem por rodada e o que o corredor muda. Do bicho pequeno, avisa que o traço dele não derruba nem agarra gente.

6.13 **No cenário da luta** (`luta.py nova`, `ato.py luta nova`), um bicho é `{"nome": "lobo 1", "nivel": 0, "bicho": "lobo"}`: a espécie inteira sai da tabela. O Mestre monta o bicho fora do comum com `bichos.bicho(espécie, tamanho=..., cat=..., tracos=[...])`.
O bicho não tem ficha no mundo: a luta que volta ao estado (5.9) não o grava, e a contagem do ermo não muda sozinha.
Na `MESA.md` (`bichos.mesa`), uma linha por lugar, o do personagem e os vizinhos, com o resumo de cada espécie contada ali: sem a contagem e sem os chefes.

### A régua do grau (medida)

Cada espécie contra o homem do degrau dela: gente gerada, de espada, malha e escudo da categoria do bicho, no nível 10 (Comum), 30 (Incomum), 50 (Raro), 90 (Épico), 120 (Único), 150 (Lendário); do Épico para cima, com Vontade 80, para o conjunto não dormir (2.9). 600 lutas por casa, começando a 3 casas.

| Espécie | Grau | Quantos | O homem do mesmo degrau vence | Com o conjunto uma categoria acima |
| --- | --- | --- | --- | --- |
| corça | F | 1 · 2 | 99% · 95% | 100% |
| ratazana | F | 1 · 3 · 4 · 6 | 100% · 74% · 59% · 36% | 100% · 100% · 99% · 98% |
| javali | E | 1 | 68% | 99% |
| lobo | D | 1 · 3 · 4 · 5 | 95% · 38% · 19% · 8% | 99% · 97% · 94% · 88% |
| surucucu | D | 1 | 55% | 100% |
| urso | D | 1 | 49% | 100% |
| aranha-de-toca | C | 1 · 2 · 3 | 80% · 33% · 5% | 99% · 99% · 96% |
| pantera | C | 1 | 46% | 98% |
| grifo | C | 1 · 2 | 48% · 8% | 100% · 99% |
| trasgo | C | 1 | 46% | 98% |
| basilisco | B | 1 | 19% | 100% |
| serpe | B | 1 | 15% | 98% |
| hidra | A | 1 | 0% | 55% (de Lendário) |
| dragão | S | 1 | 0% | — |

**Como ler:** o item decide contra o bicho também. Na mesma categoria, o bicho sozinho de grau D ou C é moeda no ar, e o bando mata. Com o conjunto uma categoria acima, o homem vence quase sempre, mesmo o bando. Do grau B para cima, um homem só não basta.

O caçador de começo (nível 10, conjunto Comum), em 1.000 lutas de ensaio por linha:

| O encontro | Vence | Fica carcaça | Todos fogem | Perde | Sai ferido, caído ou morto | Caído ou morto |
| --- | --- | --- | --- | --- | --- | --- |
| uma corça, de espada, malha e escudo | 99% | 44% | 56% | 1% | 14% | 1% |
| uma corça surpreendida, de arco e couro, de longe | 96% | 27% | 69% | 3% | 5% | 3% |
| duas corças, de espada, malha e escudo | 96% | 55% | 41% | 4% | 28% | 4% |
| três ratazanas | 73% | 70% | 3% | 27% | 47% | 20% |
| seis ratazanas | 38% | 38% | 0% | 62% | 69% | 47% |
| o javali | 68% | 43% | 25% | 32% | 50% | 30% |
| o javali surpreendido | 78% | 51% | 28% | 22% | 29% | 21% |
| o javali, de arco e couro, de longe, surpreendido | 44% | 21% | 23% | 56% | 60% | 54% |
| o javali, o mesmo caçador de conjunto Incomum | 98% | 82% | 16% | 2% | 12% | 3% |
| quatro lobos, o mesmo caçador de conjunto Incomum | 12% | 10% | 3% | 88% | 78% | 73% |

**Como ler:** a presa foge ferida em metade das lutas e leva o couro. Até a corça abre ferida uma vez em sete, porque todo crítico que tira 5% do PV abre ferida (3.12). O bando de ratazanas e o javali não são presa para quem veste Comum.

### O banco de provas dos bichos

`python3 provas.py` (600 lutas por meta). As 51 metas dos capítulos 1 a 4 seguem passando, com as mesmas faixas. **76 de 76 passam.**

| O que se mede | Meta | Medido |
| --- | --- | --- |
| B1: um nível 50, tudo Raro, contra a pantera (Rara, média, sozinha) | 40 a 60% | 49% |
| B2: o mesmo homem com a arma uma categoria acima vence | 80% ou mais | 88% |
| B2: com a arma uma categoria abaixo, perde | 80% ou mais | 88% |
| B3: quatro lobos contra um nível 30 de conjunto Incomum, em campo aberto | 10 a 35% | 20% |
| B3: o mesmo num corredor de um | 20 pontos a mais | 71% (+51) |
| B4: a serpe contra quatro de nível 60 de conjunto Raro | 5 a 30% | 20% |
| B4: a serpe contra quatro de nível 60 de conjunto Épico | 55 a 90% | 65% |
| B5: o tamanho (pequeno, médio, grande, enorme): PV | cresce | 100, 168, 252, 420 |
| B5: alcance · quantos batem nele · quantos cabem na frente de um corredor de dois | para o lado certo | 1, 1, 2, 3 casas · 2, 4, 6, 8 · 4, 2, 1, 1 |
| B5: Defesa · quanto o homem acerta | o maior é mais fácil | 39,5 a 33,5 · 47%, 59%, 63%, 73% |
| B6: cada traço, com ele e sem ele | 8 pontos ou mais | a tabela abaixo |
| B7: o bicho comum ferido foge das lutas que perde | 30% ou mais | 42% de 1.034 lutas |
| B7: o encurralado e o chefe fogem; alguém se rende a um bicho | nunca | 0, 0 e 0 vezes |
| B8: duração de um contra um bicho do mesmo degrau (mediana) | 3 a 9 rodadas | a pantera 3; javali 3, surucucu 3, urso 3, trasgo 5, basilisco 4 |

**Em B4, o conjunto Épico é o de gente gerada:** no nível 60 a Vontade é 56 e sustenta duas peças Épicas (2.9), a arma e o escudo; a armadura dorme e rende como Rara. Com Vontade para o conjunto inteiro (80), os quatro vencem a serpe em 100% das lutas.
**Em B7, a conta é de todas as espécies juntas.** Espécie por espécie, a que mais foge é o basilisco (81%) e a que menos foge é a ratazana (31%, e de 15 a 31% conforme a amostra): ela costuma morrer do primeiro golpe.

| Traço | A luta | O outro lado vence com o traço | Sem ele | Diferença |
| --- | --- | --- | --- | --- |
| matilha | quatro lobos contra um nível 30 de conjunto Incomum | 16% | 38% | 22 |
| bote | a pantera contra um nível 50 de conjunto Raro | 52% | 70% | 18 |
| investida | o javali, de longe, contra um nível 10 de conjunto Comum | 59% | 76% | 17 |
| veneno | a surucucu contra um nível 30 de conjunto Incomum | 54% | 85% | 31 |
| agarra | o urso contra um nível 30 de conjunto Incomum | 50% | 63% | 13 |
| voa | o grifo contra um nível 50 de conjunto Raro, de espada (de lança: 58%) | 49% | 65% | 16 |
| regenera | o trasgo contra um nível 50 de conjunto Raro | 50% | 80% | 30 |
| apavora | a hidra contra quatro de nível 120 de conjunto Único | 49% | 70% | 21 |
| couraça | o basilisco contra quatro de nível 60 de conjunto Raro | 14% | 43% | 29 |
| sopro | a serpe contra quatro de nível 60 de conjunto Épico | 67% | 86% | 19 |

As duas folgas mais curtas são a do agarra e a do voa: em oito outras sementes, a menor diferença foi de 12 e de 11 pontos.

O que mais o banco confere (B+):

| | Medido |
| --- | --- |
| o corpo não é peça | em 60 lutas longas, o corpo não gastou nem ganhou dono; a espada Rara do caçador gastou em todas; o dragão com Vontade 10 não tem peça dormindo |
| a ameaça | diz o grau, a categoria, o tamanho, o corpo e os traços das 14 espécies; o aviso do bando nas 5 de bando; a ratazana não derruba gente |
| o despojo | 14 de 14 espécies dentro da tabela; a mesma sorte dá o mesmo despojo; só os três chefes dão núcleo |
| o cenário | 14 de 14 espécies com a mesma ficha pelos três caminhos, e a luta inteira depois de ir ao arquivo; traço inventado é recusado |
| o agarrado | 154 abraços em 120 lutas num corredor: o agarrado não saiu do lugar nenhuma vez; de lança, a duas casas, ninguém foi agarrado |
| quem ficou com o campo | com o inimigo morto, 0 fraquezas em 200 sustos; com ele de pé, 60 |
| as espécies | 14, do Comum ao Lendário, graus de F a S; 5 de bando, 6 que andam sós, 3 chefes; 10 traços, todos em uso; o despojo na língua comum dos bens |
| no mundo | a luta do `ato.py luta` com bichos volta ao estado por um evento; o bicho não vira gente, o corpo não entra no Livro, a contagem do ermo fica como estava; as linhas da MESA cabem em 798 bytes com 11 espécies |

**O teste de estresse** (`python3 estresse.py`): 3.000 lutas ao acaso, 1.431 com bichos misturados (bandos, bichos soltos no meio da gente, bichos do lado da casa, bichos fora do comum): nenhum erro, nenhum invariante quebrado. Em outras dez sementes, 30.000 lutas, 25.726 delas com bichos: nenhum erro.

### O que esta etapa mexeu no resto da luta

- **3.14 ganha duas linhas:** ninguém se rende a um bicho; quem ficou com o campo não testa a coragem. A segunda corrige um defeito antigo: o vencedor podia fugir ou render-se no fecho da última rodada, quando um dos seus caía sangrando.
- **2.11, "derruba":** o golpe não derruba quem é maior que quem bate.
- Por causa da correção do 3.14, a amostra das provas dos módulos (capítulo 4) mudou: as 28 metas de equilíbrio e de duração e as armas entre si deram os mesmos números; nos módulos, os números andaram dentro das faixas (o maior: um contra quatro em campo aberto, de 40% para 47%; medido à parte em 4.000 lutas, antes e depois da correção: 47%).

### Os comandos

```
python3 bichos.py lista                                  as espécies, do grau F ao S
python3 bichos.py ver urso                               a ficha de luta, o despojo e a ameaça
python3 bichos.py ameaca lobo 4 arma=Comum armadura=Incomum     a frase que o caçador lê, com a conta feita
python3 bichos.py tracos                                 os traços, os tamanhos, as armas do corpo e os couros
python3 bichos.py mede javali 10 Comum [N] [lutas=200] [arma=arco] [armadura=couro] [homens=1] [inicio=longe] [surpresa=bicho]
                                                         a régua: lutas de ensaio (dado de mentira; nada é guardado)
python3 provas.py                                        o banco de provas (o bloco OS BICHOS)
python3 estresse.py [N] [gente]                          o teste de estresse (com "gente", sem bichos)
```

Em código, a caça usa: `tabelas_bichos.ESPECIES[espécie]` · `bichos.bicho(espécie, nome=None, **mais)` · `bichos.bando(espécie, sorte, n=None)` · `bichos.despojo(espécie, sorte)` (devolve os bens e o núcleo, ou `None`) · `bichos.ameaca(espécie, n=None, arma=None, armadura=None)` · `bichos.resumo(espécie)` · `bichos.mesa(E)`.
