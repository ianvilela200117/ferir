# RASCUNHO do capítulo 20: os dragões

> **RASCUNHO DO CONSTRUTOR (a frente D, os dragões; etapa 4b).** Capítulo para o `REGRAS.md` (o número 20 é provisório: quem monta o livro o acerta). Os números moram no `tabelas_dragoes.py`; a regra, no `dragoes.py` (o núcleo do motor lê a página direto: o gravador, a luta, o despojo); as provas, no `provas_dragoes.py` (o `provas_mundo.py` o roda).

## 20. OS DRAGÕES

### 20.1 Três tipos, pelo lugar onde vivem

O dragão não segue esquema de cores: o tipo é o lugar onde ele vive. O dragão, o verme e a serpe são da fantasia comum e do folclore.

| Tipo | Onde vive | O sopro | Os traços do tipo | Ferido (a fase) | Em casa |
| --- | --- | --- | --- | --- | --- |
| **o dragão da serra** | serra, ruína alta | o fogo | voa | abaixo de 30% do PV: **no covil, desce ao chão em fúria** (deixa de voar; fica ardente: quem o golpeia de perto se queima, e a ferida que ele abre queima); **fora do covil, foge pelo ar** | ao ar livre |
| **o verme do brejo** (sem asas) | brejo | o bafo podre | veneno (o golpe envenena) | abaixo de 50%: **enrosca na lama** (passa a agarrar quem está colado) | na água (pesa para os dois lados) |
| **o dragão das grutas** (sem asas) | caverna, ruína funda, o fundo da masmorra | a brasa e a fumaça | noturno (o escuro não lhe tira nada), agarra | abaixo de 50%: **bebe o sangue de quem prende** (o golpe que fere o faz recobrar PV) | no escuro |

O sopro do verme não envenena: só o golpe do corpo envenena, como em todo bicho de veneno.

### 20.2 Cinco idades, uma por grau

| Idade | Anos | Grau | Categoria do corpo | Tamanho | Nível | PV | Traços da idade |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **filhote** | até 30 | D | Incomum | médio | 30 | 147 | sopro |
| **jovem** | de 30 a 150 | C | Raro | grande | 80 | 480 | sopro, apavora |
| **adulto** | de 150 a 500 | B | Épico | enorme | 110 | 817 | sopro, apavora, couraça |
| **velho** | de 500 a 1.000 | A | Único | enorme | 160 | 1.100 | sopro, apavora, couraça, resiste |
| **ancião** | mais de 1.000 | S | Lendário | enorme | 220 | 1.337 | sopro, apavora, couraça, resiste |

O corpo é a arma e a armadura, com a categoria da idade: o filhote morde e arranha (garra e presa); do jovem em diante, garra, bocarra e cauda, uma a cada golpe. A escama vale como malha. Os atributos (Força, Agilidade, Vigor, Vontade, Percepção, Afinidade): o filhote 70, 80, 70, 50, 70, 40; o jovem 120, 70, 150, 60, 75, 45; o adulto 140, 70, 150, 80, 85, 50; o velho 160, 70, 200, 90, 90, 55; o ancião 180, 70, 240, 100, 90, 60.
São quinze dragões ao todo (os três tipos nas cinco idades): `python3 dragoes.py lista`. **O ancião tem os números do dragão do capítulo 6**, com o tipo, a fase e o resiste. O dragão do capítulo 6 segue na página dos bichos, como estava.

### 20.3 Na luta

**O dragão é um bicho:** a luta o roda com os traços que já tem (o sopro, o voa, o apavora, a couraça, o resiste, o veneno, o agarra, o noturno), e vale a regra de ouro de sempre: conta a categoria da arma contra a da escama. O sopro pega o grupo inteiro a até 4 casas, a cada duas rodadas, sem aparo.
**O filhote é bicho de verdade:** ferido, testa a coragem e pode fugir; encurralado, luta até o fim. **Do jovem para cima, o dragão é chefe:** não foge pelo susto, e só a fase o tira da luta.

**A fase (o dragão ferido).** Quando o PV cai abaixo da fração do tipo, o dragão muda (a tabela de 20.1), e a luta para e pergunta.
**A fuga do que voa (a resposta E3 a do jogador).** O dragão da serra ferido, **fora do covil**, foge pelo ar: precisa estar no ar (não no chão, não agarrado, não num corredor) e ter por onde sair. Sai sem levar golpe, e a luta para e pergunta. **No covil ele não tem por onde sair** (defende o ouro) e a fase vale como fúria: luta até morrer. O dragão que fugiu volta ao covil com o PV que tinha, **dorme até sarar** (10% do PV por dia de sono) e **lembra de quem o feriu**. O verme e o dragão das grutas não voam: nunca fogem.

**O covil não ajuda o grupo contra o dragão.** Num corredor ele luta apertado e não voa, mas bate menos gente num bicho só: contra o dragão se luta na câmara aberta.

### 20.4 O corpo e o coração

| Idade | O corpo (o despojo: de metade ao inteiro, como todo bicho) | O coração |
| --- | --- | --- |
| filhote | 4 de comida, 3 de couro Incomum, 2 de osso Incomum | não |
| jovem | 10 de comida, 5 de couro Raro, 4 de osso Raro | não |
| adulto | 8 de couro Raro, 6 de osso Raro | **um núcleo Épico** |
| velho | 10 de couro Raro, 8 de osso Raro | **um núcleo Único** |
| ancião | 12 de couro Raro, 10 de osso Raro | **um núcleo Lendário** |

O verme do brejo dá, além disso, peçonha (1 Incomum no filhote; 2 Raras do jovem para cima). A matéria segue a regra de sempre (a categoria do bicho, até a Rara), e sai na categoria de quem morreu.
**O coração é o núcleo do dragão**, com o nome dele ("o coração do Tição"), contado no Livro de Itens, e não se vende em loja. **Só do adulto para cima**, porque a escada da forja só pede núcleo do Épico para cima. **O dragão morto não volta** e o dragão não cria (não há ovo nesta etapa): os corações de um mundo são os dos dragões que ele tem.

### 20.5 O covil e o tesouro

**O covil** é uma sala de masmorra (o molde covil: a boca, as galerias e a câmara do tesouro, aberta, onde ele voa e sopra) ou um ermo, com o dragão morando ali.
**O tesouro** é a prata e os bens guardados no lugar, e as peças guardadas nele (de quem morreu ali). **É prata que já existe:** o gerador da história a tira dos lugares que o dragão saqueou e a põe no covil, e depois ela só muda de mão. O tesouro não se refaz, a não ser pela vida do dragão, que tira dos lugares (20.6).

| Idade | A prata (até, na conta da prata do mundo) | Peças | A melhor peça |
| --- | --- | --- | --- |
| filhote | nada | nenhuma | |
| jovem | 1% | 2 a 3 | Rara |
| adulto | 3% | 3 a 5 | Épica |
| velho | 6% | 4 a 6 | Única, se houver sem dono |
| ancião | 10% | 5 a 8 | Lendária, se houver sem dono |
| **todos os covis juntos** | **25% da prata do mundo** | | |

**Morto o dragão, quem ficou com o campo leva:** o corpo, a prata e os bens em partes iguais entre quem lutou até o fim; as peças do tesouro e o coração com quem comanda. Sem ninguém com o campo, o coração fica no chão, junto do corpo, e o tesouro fica onde está.

### 20.6 A vida do dragão (o mundo sozinho, todo dia)

| Idade | Dorme depois de comer | O ataque (de noite) | O tributo (por estação, da vila dele) |
| --- | --- | --- | --- |
| filhote | de 10 a 20 dias | não ataca vila: caça no ermo | |
| jovem | de 20 a 40 dias | come 30 de gado, leva de 5 a 20 de prata, mata de 0 a 1 | não cobra |
| adulto | de 30 a 60 dias | 60 de gado, de 20 a 60 de prata, de 0 a 3 mortos | 3% da prata da vila |
| velho | de 90 a 180 dias | 120 de gado, de 50 a 150 de prata, de 1 a 5 mortos | 5% |
| ancião | de 300 a 400 dias | 200 de gado, de 100 a 300 de prata, de 2 a 8 mortos | 8% |

1. **Dormindo:** nada acontece; o ferido sara 10% do PV por dia.
2. **Acordado:** do adulto para cima, se a vila dele ainda não pagou a estação, ela paga o tributo (a prata sai da vila e entra no tesouro), e ele come no ermo. Sem tributo (o jovem), ou sem prata para pagar, **ataca de noite**: o gado é comido (sai da comida da vila), a prata vai para o tesouro, e morre gente do povo da vila. Depois, dorme.
3. O acaso é o do mundo; a prata só muda de mão.

**Nesta etapa nenhum dragão adulto mora perto de vila:** o tributo seca a prata da vila, e nada a repõe antes da etapa 3. Medido: um ano do jovem ao lado de uma aldeia de 120 dá de 12 a 13 ataques; o povo vai de 120 a perto de 112, a prata da aldeia de 600 a perto de 450, e o tesouro cresce o mesmo tanto que a aldeia perde.

### 20.7 Roubar o tesouro de quem dorme

É a cena da masmorra (capítulo 17): o grupo escondido na câmara do dragão que dorme. Cada **punhado** custa um lance e é mais um teste de andar escondido (o do mais barulhento, o dado do ladino, capítulo 18), em rolagem oculta.
- **O punhado** é a sexta parte da prata que havia no covil quando o dragão adormeceu. Acabada a prata, é uma peça guardada (a que a mão alcança).
- **A vigília do dragão** (o número contra o qual se anda escondido): **20 + Percepção ÷ 10 + 2** (ele dorme leve sobre o ouro), **e mais 2 a cada punhado já tirado no mesmo sono** (o ouro mexido o inquieta). O jovem começa em 29; o adulto, em 30; o velho e o ancião, em 31.
- **Falhou: ele acorda**, não é surpreendido, e age antes de qualquer fuga pelas galerias. **Acordado, ninguém rouba:** o ladrão é visto.
- Quem rouba não sabe o quanto falta para ele acordar (a rolagem é oculta; o número fica com o Mestre).

**O ladrão robô** (o ladino Treinado de couro, Agilidade 80, no escuro, entra uma vez por sono, tira um punhado e sai; se acorda o dragão, luta de verdade): ao lado do jovem, morre no ano em 95 a 99% das vidas e tira uns 1,3 de prata por dia de vida; ao lado do adulto, morre em 96 a 98% e tira uns 4,5 por dia de vida, perto da diária. **É aposta, não renda.**

### 20.8 O que se conta, e o que só o Mestre sabe

**Na MESA, em "O que se conta":** de cada dragão que a gente dali conhece, o boato do último ataque, sem número e sem tesouro. Exemplo: "Conta-se que o Tição, um dragão jovem da serra, mora na Serra Fria, e que há 6 dias levou gado de Vau Seco. Vau Seco fica longe daqui." Passados 60 dias do ataque, a pousada só conta que ele mora lá. Quem conhece um dragão é a vila que ele ataca e os lugares a que a fama dele chega.
**No SÓ O MESTRE:** cada dragão do mundo, com o PV, até quando dorme, a vigília, os punhados do sono, o tesouro (a prata e as peças), a vila, os ataques e de quem ele lembra.
**A ameaça** (`dragoes.py ameaca TIPO IDADE [arma=CAT] [armadura=CAT]`) é a frase do chefe: ninguém a sabe de graça; o Mestre a lê quando a cena põe o dragão à frente. Ela diz o grau, o tamanho, o corpo, os traços, a fase, o que dá morto e a conta da regra de ouro.

### 20.9 Os comandos

```
python3 dragoes.py lista                                  os quinze dragões
python3 dragoes.py ver TIPO IDADE                         a ficha de luta, o corpo, o coração e a ameaça
python3 dragoes.py ameaca TIPO IDADE [arma=CAT] [armadura=CAT]
python3 dragoes.py mede TIPO IDADE NÍVEL CATEGORIA [homens=4] [lutas=200] [covil=sim|nao] [dorme=sim] [arma=CAT] [armadura=CAT]
                                                          a régua, em lutas de ensaio (nada é guardado)
python3 dragoes.py covil [LUGAR]                          SÓ O MESTRE: o dragão, o sono, o PV, o tesouro, a vila, a vigília
python3 dragoes.py covil poe LUGAR TIPO IDADE "Nome" [vila=LUGAR] [tesouro=N] [dorme=DIAS]
                                                          o Mestre funda um covil (vai ao SÓ O MESTRE)
```
(TIPO: serra, brejo, grutas. IDADE: filhote, jovem, adulto, velho, ancião.)
Na masmorra, quem monta a luta da câmara é o `masmorra.py`: o dragão entra com o PV de agora, acordado ou dormindo, e no covil não tem por onde sair. No fim da luta, as contas do dragão saem sozinhas (o morto, o fugido, o corpo, o coração, o tesouro).

### 20.10 A vila de teste: o Tição, longe (a resposta E4 a do jogador)

O comando da vila de teste com a etapa inteira acrescenta, só por eventos, sem recriar nada (e recusa rodar duas vezes):
- **Vau Seco**, uma aldeia de 120, com mercado (600 de prata), ao pé da serra. **Fica longe:** não é vizinha de Pedra Rasa, e não há estrada daqui até lá.
- **A Serra Fria**, o ermo do covil, vizinha de Vau Seco (a 6 blocos de caminho).
- **O Tição**, dragão jovem da serra, de 60 anos, que dorme mais 20 dias sobre o tesouro: **300 de prata, a Lâmina de Vau Seco** (uma espada Rara, de quem o enfrentou por último) **e um escudo Incomum**. O último ataque a Vau Seco foi há 6 dias, e a pousada de Pedra Rasa conta.

**O Maro não o alcança:** o Tição é a ameaça que se conta e não se caça no nível 5. Quando acorda, ataca Vau Seco, e a pousada conta de novo. A prata que nasce: a de Vau Seco (600) e o tesouro (300).

### 20.11 As medidas (o banco: `provas_dragoes.py`)

As lutas são as do motor, em ensaio; o grupo é o homem do degrau das criaturas (espada, malha, elmo e escudo da categoria, no nível de referência: Incomum 30, Raro 50, Épico 90, Único 120, Lendário 150), com Vontade 80 do Épico para cima.

| Meta | O que se mede | Faixa | Medido |
| --- | --- | --- | --- |
| DR1 | o filhote (foge ferido) contra um homem do degrau, cada tipo em casa | de 40 a 65% | de 52 a 63% (ele foge em 20 a 31%) |
| DR2 | do jovem ao ancião, em casa, no covil, contra 4 do degrau | jovem 50 a 75; adulto 45 a 70; velho 25 a 50; ancião 5 a 25 | jovem 57 a 70; adulto 53 a 64; velho 32 a 41; ancião 12 a 18 |
| DR3 | o ancião contra 6 do degrau | de 65 a 90% | de 78 a 84% |
| DR4 | o conjunto uma acima; uma abaixo | 90% ou mais; 10% ou menos | 100%; 0% |
| DR5 | um homem do degrau sozinho contra o jovem ou maior | até 5% | de 0 a 0,5% (ele morre em mais da metade) |
| DR6 | o jovem da serra no covil contra 4 de nível 50 Raros; com a arma Épica; tudo Incomum | de 55 a 80%; 90% ou mais; até 5% | 70% (0,46 morto por luta; morre alguém em 33%); 96%; 0% |
| DR7 | a fase para a luta; no covil nunca foge; fora dele, o da serra foge | sempre; nunca; de 60 a 95% | sempre; nunca; 71% |
| DR8 | dormindo (ele perde o primeiro turno) | 5 pontos ou mais | 10 pontos (81% contra 70%) |
| DR9 | o PV de agora; o morto, o corpo, o coração; o fugido | sempre | sempre |
| MI1 | a prata do mundo em cada passo (pôr o dragão, um ano, a luta, o tesouro, a venda) | a mesma (o tesouro conta uma vez, quando nasce) | fechou |
| MI2 | o corpo e o tesouro do jovem vendidos em Pedra Rasa | a loja paga até a caixa; o preço cai a cada venda; a peça que a caixa não paga é recusada | 847 de prata (a caixa de 2.000 vai a 1.153); o couro Raro de 111 a 42; a malha Épica recusada |
| MI3 | o dragão morto não volta | um ano depois, sem dragão e sem prata nova no covil | sim |
| MI4 | o ladrão robô, um ano ao lado do jovem e do adulto | morre em 80% ou mais; tira até 6 de prata por dia de vida | de 95 a 99% e de 96 a 98%; 1,2 a 1,3 e 4,4 a 4,5 |
| MI5 | um ano do jovem ao lado de uma aldeia de 120 | perde até 10% do povo e até metade da prata; o tesouro cresce o que a aldeia perde | 12 ataques; 120 a 112; 600 a 447; o tesouro de 300 a 453 |
| MI6 | os covis juntos | até 25% da prata do mundo | 9% na vila de teste |

**Como ler:** o jovem é a primeira caça de dragão de um grupo de veteranos, e mata um em cada três grupos que o enfrentam. Uma categoria na arma muda tudo; uma abaixo, é morte certa. Quanto mais velho, mais ele pede gente além da peça: o ancião é a calamidade (quatro heróis Lendários morrem quase todos; seis vencem quatro vezes em cinco).

### 20.12 O que fica para depois

- O ovo e o dragão que cria; o dragão que fala, negocia ou lança feitiços; montar dragão; o dragão aliado.
- O sopro que envenena (o verme envenena só pelo golpe).
- O dragão como frente e calamidade (etapa 6): o jovem que ataca é uma frente pronta; o que fugiu ferido volta e lembra de quem o feriu; o ancião acordando é calamidade.
- O dragão que envelhece na história e o gerador da região, com quantos dragões há e onde (etapa 7). O tributo que drena as vilas pede a prata nova da etapa 3.
