rascunho: o DESENHO.md manda (depois da revisão: a cabeça firme vai até o fim do segundo turno em que o alvo age, e ninguém perde mais de 1 turno em cada 3; as fontes novas de medo testam juntas, uma vez por rodada, com o calejo de ânimo; os dados do golpe rolam o maior entre crítico, fecho e Golpe do Fim, e o teto da pilha é ×7 do golpe de hoje; Perfura, Golpe de Quebra e mira na fresta são um efeito só; o Fole entrou na Robusta; o cheio se mede na faixa de cima; o degrau emprestado só em peça de até 4 efeitos)

# D1 — A BASE DA LUTA E OS EFEITOS DE ITEM DE LUTA (Motor 10, parte 2)

Desenho do campo D1: a base da luta (a pilha, os estados, a carga, o calejo, o medo) e os efeitos das peças de luta (arma, armadura, escudo, foco, amuleto).
Os efeitos de ferramenta, a Beira e o cheio na forja são do D2. **Nada disto está no motor.** Os números são de partida, medidos por simulação; quem decide é o banco.

**Como se mediu.** Um remendo em memória do `luta.golpe` (fora do repositório, sem tocar no save) pôs um gancho para cada efeito e rodou o duelo de iguais do banco:
nível 50 (mão de Mestre), espada, malha e escudo Raros, começando perto. **20.000 lutas por linha**, metade com o efeito no lado A e metade no B (a vantagem de lado some).
O erro de uma linha é de ±0,7 ponto (o 3 contra 3 rodou 6.666 lutas, ±1,2; o um contra dez, 2.000, ±2,2; o mago contra mago, 5.000, ±1,4).
"+6,2" quer dizer: quem tem o efeito vence 56,2% (a régua conta pontos acima de 50). Nas tabelas, **(m)** é medido; **(c)** é conta, interpolada entre linhas
medidas; **(d)** é desenho, escolha de regra sem vitória a medir. O que veio da `PESQUISA.md` sem medida diz "a pesquisa".

---

## 1. O que o jogador pediu e o que esta parte entrega

> **Dia 24:** "além do item, efeitos, habilidades e magias devem ser muito determinantes [...] sem falar nos efeitos dos itens que tem q ser muito importante e apelão.
> Lógico, balanceado de acordo com tudo, porém [...] deve existir a possibilidade desde a apelação até o normal e fraco."
>
> **Dia 35:** "E os efeitos, eu quero efeitos tops, efeitos que fazem diferença. 15% a mais de dano, 50% a mais de dano [...] que eu posso montar uma build boa, entendeu?
> [...] Efeito de stun [...] sangramento [...] medo".

**O que entrega:**
1. **A regra da pilha** (2.2): como somam e multiplicam dano, acerto, chance e resistência, com os tetos.
2. **Os estados** (2.3 a 2.7): a lista fechada estendida (o EXPOSTO, o AMOLECIDO e o ACUADO entram), a **carga** (o estado que se constrói golpe a golpe), o **calejo** para todo
   controle, a regra contra o atordoar em cadeia, a **escada do medo**, e o que muda no que a luta já faz.
3. **O catálogo** (2.8 a 2.10): **51 efeitos: 22 de número** (o valor em cada categoria, da Comum à Primordial) e **29 de regra** (com faixa e porta), para as cinco peças de luta,
   do fraco ao apelão. **O +15% é o Gume da Incomum** (o que Ferord já forja). **O +50% é o Gume da Lendária**, o cheio da Única, e a Sede do ferro rancoroso numa Épica.
4. **Os freios do apelão** e os dois efeitos com preço que adiantam a porta (2.11).
5. **As peças do mundo** com efeitos: a semente, o nome, o tesouro, o rival; no mundo de verdade, só por evento do Mestre (2.12).
6. **A conta**: cada efeito principal medido e posto na régua de faixas (2.13), e o que o banco tem de medir (seção 5).

### O que a medida mostrou antes de tudo (os seis achados que mudam o desenho)
1. **Entre iguais, um golpe tira o mesmo em qualquer categoria** (o ×3 da arma e o da armadura se anulam): perto de 20 PV no nível 50, contra 176 de PV. Todo efeito tem de
   ser **proporção** (% do golpe, faces do dado, carga contra a resistência), nunca número fixo. O `devolve` de hoje é fixo e quebra: o teto da Comum (4) vale **+7,3**, normal
   numa peça Comum; o teto da Rara (12) vale **+21,3**, apelão numa Rara.
2. **O crítico é o efeito mais forte por ponto.** O `critico_19` de hoje vale **+11,9** (forte), e a obra-prima o dá desde a Comum.
3. **Um ponto de acerto vale 3,6 pontos de vitória; um de Defesa, 3,5; os primeiros 10% de dano, 3,6.** A categoria inteira (+4 e ×3) vale 45.
4. **O atordoar de uma ação não pesa nada** entre Mestres (pela carga de 1 a 6: de 0 a +2,5; pela chance de 10 a 33% por golpe: de +0,5 a +1,8): eles têm três ações
   por rodada. O atordoar que vale **tira o turno e abre a guarda**: de +8,0 a +22,1.
5. **O medo decide o duelo**, porque quem quebra foge ou se rende: o teste contra 20 a cada golpe que fere já dá +10,4.
6. **Os efeitos de grupo não se medem no duelo.** A ceifadora dá +0,9 no 3 contra 3 de iguais e +15,8 no um contra dez; a tempestade de "todos os colados" dá +44 no um
   contra dez (passa do apelão) e precisou de freio.

---

## 2. As regras (para a mesa)

### 2.1 A régua, por categoria
A régua é a do `PROJETO.md` (2.1), medida no duelo de iguais, com a peça com o efeito contra a mesma sem ele. **A categoria da peça diz até que faixa o efeito dela pode ir:**

| Categoria da peça | Faixa mais alta | Pontos de vitória que o efeito pode dar |
| --- | --- | --- |
| Comum | fraco | até 5 |
| Incomum, Rara | normal | até 10 |
| Épica, Única | forte | até 20 |
| Lendária, Mítica, Primordial | apelão | até 40 |

- **Efeito de NÚMERO** cresce com a categoria: o mesmo efeito, um valor por categoria, cada um dentro da faixa daquela categoria (ou abaixo dela, nunca acima).
- **Efeito de REGRA** tem faixa fixa e só entra da categoria da porta para cima (fraco do Comum, normal do Incomum, forte do Épico, apelão do Lendário).
- **O efeito de grupo** (ceifadora, tempestade, temível, escudo que conta) mede-se no grupo: no um contra dez do banco (O NÚMERO CONTA: um Lendário de nível 120 contra
  dez Únicos de nível 60, hoje perto de 50%) ou no 3 contra 3 de iguais. **A perfura** mede-se contra a armadura uma categoria acima (entre iguais ela não age).

### 2.2 A regra da pilha
**P1. O dano é uma conta só, no fim.** `dano = o de hoje (dado × 4 × valor da arma ÷ proteção × força) × (1 + PEÇAS) × (1 + TÉCNICA) × (1 + DOM) × ESTADOS × (1 − COURAÇA)`,
arredondado para baixo uma vez, no fim. O dano 0 segue 0 (o aço que não passa, não passa).

| Grupo | O que entra | Como soma | Teto |
| --- | --- | --- | --- |
| PEÇAS | Gume, Caçadora, a Sede do rancoroso (no feitiço: a Chama) | soma | +100% |
| TÉCNICA | as habilidades acesas (a Sanha, a Roda; do desenho das habilidades) | soma | +40% |
| DOM | o dom de dano (a Mão Pesada; do desenho dos dons) | soma | +20% |
| ESTADOS | exposto ×1,5 (no alvo); amolecido ×0,75 (em quem bate) | multiplica | um de cada |
| COURAÇA | a couraça do alvo (no feitiço: a guarda mágica) | curva (P4) | 75% |

Exemplo: Gume Épico (+30%) e a Sanha cheia de um Mestre (+30%), contra um alvo exposto: × 1,3 × 1,3 × 1,5 = **× 2,5**. O maior possível (Primordial, técnica e dom no teto,
alvo exposto) é × 2 × 1,4 × 1,2 × 1,5 = × 5: menos que duas categorias (× 9). **O item segue decidindo.**

**P2. O % entra fora do dado.** O 2d20 que explode, o crítico e a força do golpe seguem como hoje; o % multiplica o resultado.
**P3. Número fixo soma, com teto.** Acerto, Defesa, Firmeza e coragem que vêm de efeitos somam entre peças até **+8 cada** (duas categorias de bônus).
**P4. Chance e resistência em curva:** `1 − (1 − a) × (1 − b)`. Duas couraças de 25% cortam 44%, não 50%. Teto 75%. **Ninguém é imune por efeito** (só pelo corpo: o
"sem vida" não sangra nem sente medo).
**P5. O mesmo efeito em duas peças não soma: vale o maior.** Efeitos diferentes do mesmo grupo somam (Gume e Caçadora).
**P6. O crítico:** vale a melhor faixa entre as fontes (2.8); nunca melhor que 17/7.
**P7. A cura** (vampira, regenera, seiva, poção, feitiço) soma no teto do dia: metade do PV máximo (11.7).
**P8. O golpe extra** (segundo golpe, ceifadora, varredura, tempestade, o golpe livre) não puxa outro golpe extra e põe metade da carga (para baixo, no mínimo 1).
**P9. Estado tem potência fixa e prazo que soma.** O exposto é sempre +50%; aplicar de novo soma rodadas, até 3; o % nunca soma.

### 2.3 Os estados: a lista fechada estendida
Efeito novo aponta para um estado desta lista; estado novo só entra por regra escrita.

| Estado | O que faz | Prazo | Calejo (2.5) | Hoje ou novo |
| --- | --- | --- | --- | --- |
| ATORDOADO | **pela carga: perde o turno seguinte inteiro e fica aberto** (−4 na Defesa) até o fim da rodada seguinte. Pela ferida na cabeça: perde 1 ação (grave: 2), como hoje | o turno seguinte | cabeça | a carga é nova |
| AO CHÃO | −4 na Defesa; levantar gasta 1 ação | até levantar | pernas | hoje |
| PRESO | não anda (perna grave; prender e raízes, 2 turnos) | o de hoje | pernas | hoje |
| SANGRANDO, em filetes | cada fonte de sangue é um **filete**: tira por rodada a fração do golpe que o abriu, com prazo próprio; **até 3 filetes** | o de cada filete | — (é dano) | muda |
| ENVENENADO | o de hoje (6.6, 11.7) | o de hoje | — | hoje |
| ABALADO · ACUADO · QUEBRA | a escada do medo (2.6) | | ânimo | o ACUADO é novo |
| EXPOSTO | **leva +50% no dano** de golpe e de feitiço que fere | o fim da rodada (Expõe) ou da seguinte (Escancara); soma até 3 | — (não tira ação) | novo |
| AMOLECIDO | **faz −25% de dano** | o fim da rodada seguinte; soma até 3 | — (não tira ação) | novo |
| ATADO | o nó de hoje (a Mana não volta; cada feitiço custa 1 a mais), posto também pelo efeito Atar | 2 turnos | mana | hoje |
| os da magia (11.5) | benzido, mau-olhado, guardado, cego, com seiva, com fúria, enjoado | os de hoje | — | hoje |

- **A ATADURA** (ordem nova, `atar [ALIADO]`): 1 ação, em si ou num aliado colado; corta o filete mais forte. O amparo da fé estanca todos, como hoje. Quem o jogador não
  comanda ata a si mesmo quando os filetes somados tiram 5% do PV por rodada ou mais e não há inimigo colado (desenho).
- **O filete da ferida** é o sangue de hoje (um quinto do golpe, 3 rodadas; 5 se grave) e segue um só (o maior, como hoje); **só os efeitos abrem filetes a mais**. Assim a luta
  sem efeito sangra como hoje, dado por dado. Um quarto filete toma o lugar do mais fraco.
- **O exposto e o amolecido não são controle** (não tiram ação nem passo): não têm calejo. O freio deles é a potência fixa (P9) e o "um de cada" da pilha.

### 2.4 A carga (o estado construído golpe a golpe)
O atordoar e o atar **não rolam chance por golpe** (nem o derrubar das técnicas, quando vier). Cada golpe que tira PV soma a carga do efeito na barra da família, no alvo.
Quando a barra chega à **resistência**, o estado pega, a barra volta a zero e o alvo ganha um calejo da família.

- **RESISTÊNCIA = 6 + bônus de Vigor ÷ 2 + 4 por calejo da família** (+4 de saída no chefe e no bicho grande; a Robusta soma). No nível 50 do banco, 10; em Ferord (Vigor 55), 8,5.
- **O item decide também aqui:** contra armadura de categoria maior que a arma, a carga entra pela metade (para baixo); na parte nua, em dobro. Entre iguais, inteira.
- **Uma barra por família** (cabeça, mana, pernas): a peça, a técnica e o trunfo enchem a mesma barra. Não há duas barras de atordoar.
- **A mesa vê a barra do inimigo** ("carga de cabeça 6/10"): o jogador planeja o golpe que fecha.
- **Por que carga e não chance** (medido, o mesmo atordoar de perder o turno e abrir): a carga 3, 4 e 6 dá **+8,0, +9,8 e +13,3**; a chance de 10, 15, 20 e 30% por golpe (com a
  cabeça firme e o calejo cortando a metade a cada um) dá **+3,8, +6,5, +7,4 e +9,9**. A carga 3 vale a chance de 25%; mas a chance rola um dado a mais em cada golpe e pode
  pegar no primeiro golpe da luta por sorte, e a carga não rola nada, aparece no quadro e se planeja. **Recomendo a carga.**
- **Por que perder o turno, e não uma ação** (medido): perder 1 ação, com carga de 1 a 6, dá de 0 a +2,5 (quem tem três ações por rodada mal sente); perder o turno, sem abrir,
  dá +3,0 a +8,2; perder o turno **e abrir** dá +8,0 a +22,1. Só o último é o "stun" do pedido.

### 2.5 O calejo para todo controle, e o atordoar que não encadeia
**O calejo** (o de hoje só vale contra feitiço, 11.2) passa a valer para todo controle, **por família**: cada controle que pega soma **+4 na resistência daquela família**
até o fim da luta (e +4 na Firmeza contra o feitiço daquela família). As famílias: **cabeça** (atordoar; o raio que atordoa), **pernas** (derrubar, prender, raízes),
**mana** (atar, o nó), **ânimo** (o medo, que tem a escada no lugar da barra). O calejo de hoje da Firmeza segue como está (a meta M21 não muda); o feitiço que pega soma
também no calejo da família dele. Família diferente não calejeia: quem monta atordoar e medo tem dois freios separados, e por isso a variedade paga.

**A regra contra o atordoar em cadeia** (cinco freios juntos):
1. A carga tira o turno **uma vez** e zera; a próxima pede a barra cheia de novo.
2. **Cabeça firme:** do atordoar até o fim do primeiro turno em que o alvo volta a agir, os golpes não somam carga de cabeça. (Na medida, ela durou até o fim da rodada
   seguinte; a regra escrita é um pouco mais dura contra a cadeia e garante que ninguém perde dois turnos seguidos.)
3. O calejo: cada atordoar soma 4 na resistência (no banco, 10, 14, 18: o segundo pede 40% mais golpes, o terceiro 80%).
4. Chefe e bicho grande começam a luta com um calejo em cada família.
5. Medido: só com o calejo (sem a cabeça firme e sem abrir), a carga 4, 6 e 10 dá +6,6, +10,8 e +16,2; com a cabeça firme, sem abrir, a carga 4 e 6 dá +4,3 e +8,2 (a
   cabeça firme corta perto de um terço); com a cabeça firme e abrindo (a regra), a carga 10 dá +19,2 e a 15 só chega a +22,1: o freio segura o teto do atordoar no começo
   do apelão. No 3 contra 3, a carga 4 e a 6 dão +17,6 e +21,7 (o aberto vale para os três que batem).

### 2.6 A escada do medo
| Degrau | O que faz | Como se chega |
| --- | --- | --- |
| firme | nada | — |
| ABALADO (o "fraqueja" de hoje) | −2 no acerto | firme, falhar a coragem por menos de 10 |
| ACUADO (novo) | −4 no acerto; não avança contra quem o assustou (só segura, guarda, toma fôlego ou recua) | abalado, falhar por menos de 5 |
| QUEBRA (a de hoje) | foge ou se rende | firme e falhar por 10 ou mais; abalado e falhar por 5 ou mais; acuado e falhar |

- O acuado desce para abalado depois de 2 rodadas sem susto novo; o abalado fica até o fim da luta, como hoje.
- **Quem o jogador comanda para no abalado**, e a luta para e pergunta (como hoje). O bicho foge no primeiro que falha (como hoje).
- O medo de peça testa no máximo **uma vez por rodada** por fonte, e só em quem a peça tira PV. Contra quem tem moral firme (o chefe), não age.
- **Medido:** o módulo 8 do banco (seis contra um muito mais forte: alguém foge ou se rende) dá **39%** com esta escada (hoje 52%, em 3.000 lutas; a meta é 30% ou mais).
  A escada da pesquisa (um degrau por falha) dava 16% e reprovava; por isso esta guarda a dureza de hoje no primeiro susto.

### 2.7 O que muda no que a luta já faz
1. **O `devolve`** deixa de ser fixo: devolve uma fração do dano levado (2.8, armadura). A peça que já tem `devolve N` passa ao da categoria dela, por evento do Mestre.
2. **O `critico_19`** vira o efeito Crítico, que cresce com a categoria (2.8). O de hoje (19/11) é o valor da Épica. A peça que já o tem: pergunta 1 (seção 6).
3. **O `sangra`** vira o valor Comum da Sangria (a ferida que ela abre sangra 5 rodadas), e o sangue ganha os filetes (só para efeito).
4. **A moral de gente ganha o ACUADO** (2.6). É a única mudança que toca toda luta, com ou sem efeito; o módulo 8 a mede.
5. **O atordoar ganha a carga** (perde o turno e abre); o atordoar da ferida na cabeça segue o de hoje (1 ação; grave, 2), e passa a dar a cabeça firme.
6. **O calejo vale para todo controle**, por família (2.5). O `derruba` de hoje (uma vez por luta) entra no calejo de pernas.
7. **Fora isso, a luta sem efeito é a de hoje, dado por dado** (com semente fixa, como na etapa da magia).

### 2.8 O catálogo: os efeitos de NÚMERO (22)
Cada célula: o valor, e entre parênteses os pontos de vitória medidos (m), contados (c) ou de desenho (d). O valor **não se guarda na peça**: sai da categoria dela (a peça
que dorme na sintonia rende uma abaixo e tem os efeitos dormindo, como hoje). No arco e na besta valem os de arma, menos o Fôlego, a Varredura e a Tempestade (que são de perto).

**Arma (10)**

| Efeito | Comum | Incomum | Rara | Épica | Única | Lendária | Mítica | Primordial |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GUME: dano a mais | +10% (3,6 m) | **+15% (6,2 m)** | +20% (7,3 m) | +30% (13,0 m) | +40% (16,7 m) | **+50% (20,5 m)** | +75% (26,5 m) | +100% (30,7 m) |
| CERTEIRA: acerto | +1 (4,0 m) | +2 (7,3 m) | +2 (7,3 m) | +3 (10,9 m) | +4 (14,5 m) | +5 (17 c) | +6 (19,3 m) | +8 (23 c) |
| CRÍTICO: a face alta / o outro dado (hoje 20/11) | 20/9 (3,0 m) | 20/7 (6,8 m) | 20/6 (8,3 c) | 19/11 (12,2 m) | 19/9 (16,9 m) | 18/9 (24,9 m) | 17/9 (30,4 m) | 17/7 (33,8 m) |
| CAÇADORA: dano a mais contra um tipo (bicho, morto, povo, gente ou dragão, escolhido na forja) | os números do Gume, só contra o tipo; soma com o Gume | | | | | | | |
| VAMPIRA: cura parte do dano que faz (no teto do dia) | 15% (3,4 m) | 25% (6,0 m) | 35% (8,2 m) | 50% (11,2 m) | 60% (12 c) | 75% (14 c) | 90% (15 c) | 100% (16 c) |
| SANGRIA: o sangue que ela abre | a ferida sangra 5 rodadas (1,1 m) | cada golpe que fere abre um filete de 1/5 do golpe por 2 rodadas (5 c) | 1/5 por 3 (7,3 m) | os filetes somam: 1/5 por 3 (14,5 m) | somam: 1/4 por 4 (17 c) | somam: 1/4 por 5, e a atadura não estanca (21 c) | somam: 1/3 por 5 (25 c) | somam: 1/3 por 6 (28 c) |
| ATURDIR: carga de cabeça por golpe (atordoa: perde o turno e abre) | — | 3 (8,0 m) | 4 (9,8 m) | 6 (13,3 m) | 8 (15,1 m) | 10 (19,2 m) | 12 (19,5 m) | 15 (22,1 m) |
| MEDO: quem ela fere testa a coragem contra | — | 17 (4,8 m) | 18 (6,0 m) | 20 (10,4 m) | 22 (15,0 m) | 24 (19,8 m) | 26 (25,3 m) | 29 (32,0 m) |
| SEGUNDO GOLPE: vezes por luta em que o golpe que acerta dá outro, de graça | 1 (3,8 m) | 2 (7,9 m) | 2 (7,9 m) | 3 (11 c) | 4 (14 c) | 5 (17 c) | 6 (19 c) | 8 (22 c) |
| PERFURA: contra armadura de categoria MAIOR que a arma, a proteção conta | ×0,9 (2 c) | ×0,8 (4,6 m) | ×0,67 (9,3 m) | ×0,6 (14 c) | ×0,55 (18 c) | ×0,45 (28 c) | ×0,4 (32,8 m) | ×0,35 (38 c) |

**Armadura (6; o Temível também no escudo)**

| Efeito | Comum | Incomum | Rara | Épica | Única | Lendária | Mítica | Primordial |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| COURAÇA: dano de golpe recebido a menos | 5% (3 c) | 10% (6,4 m) | 12% (7,5 c) | 20% (12,5 c) | 25% (15,6 m) | 33% (21,3 m) | 40% (25 c) | 50% (31 c) |
| DEVOLVE: parte do dano levado volta em quem golpeia de perto | 10% (3,0 m) | 15% (5,2 m) | 20% (7,5 m) | 30% (10,9 m) | 40% (15 c) | 50% (19,5 m) | 65% (25 c) | 80% (30 c) |
| REGENERA: do PV máximo por rodada (no teto do dia) | 1% (1,5 c) | 2% (3,5 m) | 3% (7,3 m) | 4% (9 c) | 5% (10,5 m) | 6% (12 c) | 7% (13 c) | 8% (14,7 m) |
| TEMÍVEL: quem começa a luta contra o dono testa a coragem contra | 20 (2,7 m) | 22 (5 c) | 24 (7,4 m) | 26 (10,5 c) | 29 (15,2 m) | 31 (18 c) | 33 (21 c) | 35 (24 c) |
| FOLE: fôlego máximo a mais | +1 (1 c) | +2 (2,8 m) | +2 | +3 | +3 | +4 (3,4 m) | +4 | +5 |
| ROBUSTA: soma na resistência à carga e na coragem | +3 | +4 | +6 (m: a carga 6 cai de +13,3 para +9,1) | +8 | +10 | +12 | +14 | +16 |

**Escudo (1)**

| Efeito | Comum | Incomum | Rara | Épica | Única | Lendária | Mítica | Primordial |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GUARDA: Defesa | +1 (3,8 m) | +2 (6,8 m) | +2 (6,8 m) | +3 (10,0 m) | +4 (12,4 m) | +5 (14 c) | +6 (16,2 m) | +8 (19 c) |

**Foco (2) e amuleto (3)** (medidos no mago contra mago do banco, a M1: cajado, couro e amuleto Raros; 5.000 lutas por linha, ±1,4)

| Efeito | Comum | Incomum | Rara | Épica | Única | Lendária | Mítica | Primordial |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CHAMA (foco): dano de feitiço a mais | os números do Gume (+15%: 4,6 m; +30%: 7,2 m) | | | | | | | |
| FOCO CERTEIRO (foco): Conjuração | os números da Certeira (+2: 7,4 m) | | | | | | | |
| GUARDA MÁGICA (amuleto): dano de feitiço recebido a menos | os números da Couraça (15%: 6,2 m) | | | | | | | |
| FIRMEZA (amuleto): Firmeza | +1 | +2 | +2 | +3 | +4 (7,0 m) | +5 | +6 | +8 |
| CORAGEM (amuleto): coragem | +2 | +3 | +4 (corta o Medo 22 de +15,0 para +5,1: m) | +5 | +6 | +7 | +8 | +10 |

- **Onde ficam o +15% e o +50%.** O Gume da Incomum é +15%: Ferord chega nele na próxima obra boa. O +50% é o Gume da Lendária, o **cheio** da Única (2.10), e a **Sede**
  do ferro rancoroso numa Épica (2.11): prêmio alto, ou conta a pagar.
- **A Caçadora** vale o mesmo que o Gume quando o alvo é do tipo, e nada nos outros: sozinha é pior que o Gume, e é a escolha de quem se especializa (Gume +20% e Caçadora
  +20% contra bicho dão +40% contra bicho).
- **A Perfura** não age entre iguais: é o abridor de couraça, para o chefe e o cavaleiro de armadura melhor. O Gume de +50% contra a armadura uma acima dá +10,2; a Perfura
  de ×0,5 dá +21,9 ali.
- **A Vampira** não passa do forte no duelo: o teto da cura do dia a segura. No um contra dez, 25% já dá +20,7: é a peça de quem luta contra muitos.
- **O Medo** testa uma vez por rodada (2.6), só em quem tira PV. Contra o bicho, faz fugir a caça (quem caça escolhe outra peça). A Coragem do amuleto é o contraveneno.
- **O Aturdir** cresce devagar no alto (19,2 na Lendária, 22,1 na Primordial): é o freio contra a cadeia (2.5) que segura o teto. No grupo ele vale mais (o aberto é para todos).
- **O Fole** fica fraco em toda categoria: é o conforto de quem veste placa e bate de malho (o fôlego que a armadura come). A **Robusta** e a **Coragem** são os contra:
  a Robusta +6 corta a carga 6 de +13,3 para +9,1 (m), e o banco mede cada uma contra o efeito de mesma categoria (seção 5).

### 2.9 O catálogo: os efeitos de REGRA (29)
Faixa fixa; entra da porta para cima. (m) medido; (c) conta; (d) desenho, sem vitória a medir.

| Faixa e porta | Efeito | Peça | O que faz | Medida |
| --- | --- | --- | --- | --- |
| fraco (Comum) | LEVE · PESA · NÃO QUEBRA | todas | os de hoje (pede 20 a menos · 20 a mais · não gasta) | (d) |
| fraco | DERRUBA | arma | uma vez por luta, o golpe que fere derruba (hoje) | +3,2 (m) |
| fraco | FIRME | armadura, escudo | o dono não é derrubado (hoje) | contra o Derruba (d) |
| fraco | LUZ | todas | a peça clareia: o escuro não pesa no golpe do dono (no tiro, metade) | (d) |
| fraco | FIO MANSO | arma | o golpe que mataria quem já está abaixo de 1/4 do PV o deixa caído, vivo: para fazer preso | (d) |
| fraco | ARRANCADA | arma, armadura | uma ação a mais na primeira rodada | +2,7 (m) |
| fraco | APARADORA | escudo, espada, montante | quem tem o golpe aparado pelo dono perde 1 de fôlego | (d) |
| normal (Incomum) | EXPÕE | arma | o golpe que fere deixa o alvo **exposto** até o fim da rodada | +7,1 (m) |
| normal | PONTA CERTA | arma | uma vez por luta, o golpe que errou por 5 ou menos acerta | +5,1 (m); três vezes por luta, +13,1 (m) |
| normal | DESFORRA | arma | ferido por alguém, o dono tem +2 no acerto contra ele até o fim do turno seguinte | +5 (c) |
| forte (Épica) | ESCANCARA | arma | o golpe que fere deixa o alvo **exposto** até o fim da rodada seguinte | +15,5 (m) |
| forte | AMOLECE | arma | o golpe que fere deixa o alvo **amolecido** até o fim da rodada seguinte | +11,5 (m) |
| forte | FÔLEGO | arma pesada | o golpe da arma pesada custa 1 de fôlego a menos (na espada, nada: −0,3) | +13,3 (m, martelo) |
| forte | CEIFADORA | arma | quem derruba um inimigo golpeia de novo, de graça, outro que alcança | +15,8 no um contra dez (m); +0,9 no 3 contra 3 (m) |
| forte | VARREDURA | arma de corte ou impacto | cada golpe que acerta pega também **um** outro inimigo colado, com **metade** do dano (rola o acerto dele) | +14,6 no um contra dez; +11,0 no 3 contra 3 (m) |
| forte | BRASA | arma | cada golpe que fere abre um filete de **fogo** (1/5 do golpe, 3 rodadas; os de fogo somam); queima também quem não tem vida; a água e o amparo apagam | +14,5 (m, como a Sangria Épica) |
| forte | ATAR (o silêncio) | arma | carga de mana 4 por golpe: o alvo fica atado (o nó) por 2 turnos | (d; o banco mede contra o mago) |
| forte | REFLETORA | escudo | uma vez por luta, o feitiço que voa contra o dono volta em quem lançou (rola de novo, contra a Defesa dele) | (d; o banco mede na M2) |
| forte | ESCUDO QUE CONTA | escudo | uma vez por luta (1 ação), os aliados a 2 casas descem um degrau do medo e ganham +2 na coragem até o fim da luta | (d; 3 contra 3) |
| forte | GUARDIÃ | escudo | guardar um aliado colado não gasta a reação, uma vez por rodada | (d; 3 contra 3) |
| apelão (Lendária) | GOLPE DO FIM | arma | o crítico é 17/11 e rola os dados **4 vezes** (não 2) | +35,2 (m) |
| apelão | TEMPESTADE | arma de corte ou impacto | cada golpe que acerta pega também **um** outro inimigo colado, com o dano **inteiro** | +20,6 no um contra dez (m) |
| apelão | IMORTAL | armadura, amuleto | **uma vez por dia**, o dono fica com 1 PV em vez de cair (e não morre do golpe) | +5,6 (m), no duelo e no um contra dez: a régua não o mede, porque ele compra a vida (que é uma só), não a vitória; a porta é de desenho |
| apelão | DOMÍNIO | foco | **uma vez por luta**, um feitiço que o dono sabe sai sem Mana, sem ser longo, e com os dados rolados duas vezes | (c: o banco mede na M1) |
| apelão | PODER DE LENDA | a peça com nome | uma regra só daquela peça, com o seu dito (2.12) | cada um medido, de 20 a 40 |
| preço (uma porta antes) | A SEDE (o ferro rancoroso) · O VIDRO | arma · qualquer peça | 2.11 | a Sede: perto de +28 numa Épica (c); o Vidro: o efeito de cima |

### 2.10 O efeito cheio (para o D2)
Se a Beira do D2 der o **cheio**, o efeito de número sai com o valor **da coluna à direita** (a categoria de cima): a Incomum cheia tem o Gume de +20%; a Única cheia, o de
+50%. O cheio pode passar a faixa da categoria em um degrau (é a peça que quase subiu), nunca em dois; a Primordial cheia fica na Primordial. Os de regra não têm cheio.
**O item segue decidindo** (medido: a arma uma categoria acima, sem efeito, contra a de baixo com efeitos cheios da categoria de cima; hoje, sem efeito nenhum, 94,8%):

| A arma de baixo (Rara) leva | A de cima (Épica), sem nada, vence |
| --- | --- |
| nada | 94,8% |
| três magros da Rara (Gume +20%, Certeira +2 e um crítico menor, de +6,8) | 89,6% |
| dois cheios (Gume +30% e Certeira +3) | 88,4% |
| dois cheios (Gume +30% e Crítico 19/11) | 82,9% |
| três cheios (mais a Certeira) | 80,7% |
| quatro cheios (mais a Vampira de 15%) | 80,2% |
| cinco cheios (Gume, Certeira, Crítico e a Vampira de 50%) | 78,9% |
| quatro cheios com o Medo 20 no lugar da Vampira | 76,7% |
| quatro magros da Rara (Gume +20%, Certeira +2, Crítico 20/6, Medo 18) | 86,0% (8.000 lutas) |
| **seis cheios, os mais fortes** (Gume, Certeira, Crítico, Vampira 50%, Medo 20 e Aturdir 6) | **62,0%** (8.000 lutas) |

Com até cinco efeitos cheios, a peça de cima ainda vence perto de quatro lutas em cinco. O teto de efeitos do D2 (Comum 2, Incomum e Rara 4, Épica e Única 5, Lendária e
Mítica 6, Primordial 7; mais a obra-prima e o molde) cabe nesta conta: no pior caso (seis, todos cheios e os mais fortes, o que quase nunca sai), a de cima ainda vence 62%.
O item segue decidindo, e a peça de baixo cheia vira escolha de verdade ("o Incomum com 3, 4 efeitos" do pedido). O que a pilha não deixa é a soma passar do teto (P1, P3).

### 2.11 Os freios do apelão, e os efeitos com preço
**Todo apelão leva pelo menos dois freios** (a pesquisa, 3.1):
1. **A porta:** só da Lendária para cima (a Lendária sai em 1 de cada 4 vidas, 7.13; a Mítica e a Primordial pedem núcleo).
2. **A sintonia dobrada:** a peça com um apelão de regra ocupa **2 lugares** (2.9: Vontade ÷ 20). Ferord, de Vontade 50, sustenta uma peça assim e mais nenhuma Épica.
3. **Um por vez:** um apelão de regra acordado por pessoa; o de outra peça dorme (só ele: o resto da peça vale).
4. **Os usos:** o que se chama tem usos escritos (o Imortal, uma vez por dia; o Domínio, uma por luta).
5. **O preço ou a condição:** o rancor, o vidro, ou a condição do poder de lenda (só à noite, só contra quem quebrou um voto, só na Sanha).
6. **O banco:** de 20 a 40 pontos; acima de 40, não entra (a tempestade de "todos os colados" deu +44 e foi cortada para um; com metade do dano, +38,1).

Os de número que chegam ao apelão (Gume, Crítico, Medo, Couraça, Devolve, Perfura, Sangria, Aturdir, Temível, da Lendária para cima) têm os dois freios de sempre: a porta
e a sintonia (toda peça Épica ou melhor ocupa lugar). Não dobram lugar.

**Os efeitos com preço (o preço compra uma porta):**
- **O FERRO RANCOROSO** (arma; porta Épica, não Lendária). Nasce de forja em luto, raiva ou vingança declarada (a cena diz; o D2 dá o gatilho). **A SEDE**: o dono a acorda
  com 1 ação (ordem `sede`): **+50% de dano** até o fim da luta, no grupo das peças (com o Gume Épico, +80%: perto de +28, apelão, numa Épica). **O preço:** a peça é
  maldita (13.3: a mão não a larga), e **cada luta em que a Sede acorda anda um passo da maldição dela** (o relógio de 6 passos, 13.2). Essa maldição não rola na virada:
  só anda pelo uso, e desce um passo a cada 7 dias sem a Sede. Sai com a **CONTRAPEÇA**: uma peça da mesma categoria, forjada em paz, posta na mão de quem carrega o ferro
  (quebra a maldição, e a Sede some). Ferord pode vender a contrapeça a quem carrega um.
- **A PEÇA DE VIDRO** (qualquer peça; porta uma abaixo). Leva **um efeito de regra da faixa de cima** (um forte numa Rara, um apelão numa Única) **ou um de número com o
  valor de duas categorias acima** (o Gume de +40% numa Rara: +16,7). **O preço:** quando o dono cai numa luta, a peça **se parte** (vai a zero de durabilidade) e o efeito de
  vidro some para sempre; consertar devolve a peça sem ele.
- **Uma porta adiantada por peça.** O vidro (daqui), a Sede (daqui) e o degrau emprestado (o poder da ferramenta Lendária, no D2) não somam: a peça leva no máximo um efeito
  acima da porta dela.

### 2.12 As peças do mundo com efeitos
- **As peças altas da história** (o `historia.py` gera as Épicas, Únicas, Lendárias e a Mítica, de nome "o Gume da Aurora", "a Couraça do Inverno"). Ganham efeitos **pela
  semente** (função pura da semente do mundo e do nome da peça): tantos quanto o teto de efeitos da categoria (são obras-primas), o primeiro tirado do **tema do nome**, os outros
  pela semente entre os que cabem na peça e na porta; a Lendária e a Mítica ganham também um **poder de lenda** do tema. A semente nunca dá cheio nem efeito com preço.

| O nome diz | O efeito do nome | O poder de lenda (Lendária e acima; um dito, medido de 20 a 40) |
| --- | --- | --- |
| da Aurora · da Vigília | Luz; Certeira | "a primeira luz": no começo da luta, os aliados a 2 casas saem do abalado e o dono tem a Arrancada |
| do Juramento · da Promessa | Firmeza; Robusta | "o voto que segura": o Imortal contra quem o dono jurou, sem gastar o uso do dia |
| da Última Noite · do Eclipse · do Corvo | Medo; Temível | "a noite que não acaba": o escuro não pesa para o dono e pesa o dobro nos inimigos |
| do Rei Velho · da Ponte · da Coroa Partida | Guarda; Guardiã | "ninguém passa": quem o dono guarda não leva golpe enquanto o dono estiver de pé |
| da Serra · do Inverno | Couraça; Expõe (o gelo) | "o frio que prende": o alvo exposto pela peça fica também preso enquanto exposto |
| do Lobo · do Sangue Antigo · da Viúva · da Fome | Sangria; Vampira | "a lâmina que lembra": o terceiro golpe seguido no mesmo alvo ignora a armadura |
| das Cinzas · do Primeiro Fogo | Brasa; Chama | "o fogo que pula": o filete de fogo passa para quem está colado no queimado |
| da Maré · do Exílio | Arrancada; Ponta Certa | "a volta da maré": uma vez por luta, o dono troca de lugar com quem o golpeou, e golpeia |
| dos Sete | Segundo Golpe; Varredura | "os sete de uma vez": uma vez por luta, o golpe pega todos os colados, com o dano inteiro |
| do Silêncio | Atar; Aturdir | "o silêncio": o alvo atado também não dá o brado nem chama (não lança, não comanda) |

- **No mundo de verdade, só por evento do Mestre, com o jogador sabendo** (PROJETO 2.5). O Mestre lê o que a semente dá (`efeitos.py semente ITEM`, só olha) e grava por um
  evento "mestre" com `['item', id, 'efeito', 'junta', ...]`. O jogador sabe que as peças da história ganharam efeitos; o que cada uma tem, ele descobre ao ver a peça (a janela
  do item) ou por boato.
- **O tesouro** (masmorra e dragão): a peça Rara ou melhor do tesouro sai com efeito pela chance da categoria (Rara 1 em 4, Épica 1 em 2, Única 3 em 4, Lendária ou acima
  sempre; um efeito, dois da Única para cima), pela semente da sala ou do covil, em rolagem oculta. **Nunca um apelão de regra** (esse fica na história e na forja).
- **O rival que forja e o ferreiro do mundo:** a obra-prima deles (os 20 da Lei do Valor e a Beira do D2) escolhe pela semente, numa lista por papel: o guerreiro (Gume, Crítico,
  Certeira), o guarda (Couraça, Guarda, Devolve), o caçador (Caçadora contra bicho, Gume, Sangria), quem lança (Chama, Foco Certeiro). Vai no mesmo evento da obra.

### 2.13 A conta esperada (o resumo medido)
| O que se mediu (duelo de iguais, 20.000 lutas, salvo o dito) | Pontos | Leitura |
| --- | --- | --- |
| o `sangra` · o `derruba` · o `critico_19` de hoje | +1,1 · +3,2 · **+11,9** | o crítico de hoje é forte |
| o `devolve` de hoje: 4 (teto Comum) · 12 (teto Raro) | **+7,3 · +21,3** | o fixo quebra |
| Gume +5% · +10% · +15% · +20% · +25% · +30% · +40% · +50% · +60% · +75% · +100% | +1,6 · +3,6 · +6,2 · +7,3 · +11,5 · +13,0 · +16,7 · +20,5 · +22,5 · +26,5 · +30,7 | ~0,4 por 1% no começo |
| Certeira +1 · +2 · +3 · +4 · +6 | +4,0 · +7,3 · +10,9 · +14,5 · +19,3 | 3,6 por ponto |
| Guarda +1 · +2 · +3 · +4 · +6 | +3,8 · +6,8 · +10,0 · +12,4 · +16,2 | 3,5 por ponto |
| Crítico 20/9 · 20/7 · 20/5 · 19/11 · 19/9 · 18/11 · 18/9 · 17/11 · 17/9 · 17/7 · 16/11 | +3,0 · +6,8 · +9,9 · +12,2 · +16,9 · +19,6 · +24,9 · +25,6 · +30,4 · +33,8 · +29,0 | ~2,7 por ponto de chance de crítico |
| o crítico que só rola os dados 3 vezes (20/11) · 19/11 ×3 · o golpe do fim (17/11 ×4) | +5,6 · +19,2 · +35,2 | |
| Couraça 10% · 15% · 25% · 33% | +6,4 · +9,5 · +15,6 · +21,3 | vale mais que o Gume do mesmo tamanho |
| Devolve 10% · 15% · 20% · 30% · 50% do dano levado | +3,0 · +5,2 · +7,5 · +10,9 · +19,5 | |
| Vampira 10% · 15% · 20% · 25% · 35% · 50% | +1,6 · +3,4 · +4,4 · +6,0 · +8,2 · +11,2 | o teto do dia a segura |
| Regenera 2% · 3% · 5% · 8% | +3,5 · +7,3 · +10,5 · +14,7 | |
| Aturdir de 1 ação, carga 1 · 2 · 3 · 4 · 6 · e a chance de 10 a 33% | 0,0 · +0,6 · +0,3 · +1,4 · +2,5 · de +0,5 a +1,8 | não pesa |
| Aturdir de perder o turno e abrir, carga 3 · 4 · 6 · 8 · 10 · 12 · 15 | +8,0 · +9,8 · +13,3 · +15,1 · +19,2 · +19,5 · +22,1 | o "stun" |
| Exposto a cada golpe: até o fim da rodada · da seguinte · pela carga 2 · 3 | +7,1 · +15,5 · +3,2 · +4,1 | a carga não serve ao exposto |
| Amolecido a cada golpe, até o fim da rodada seguinte | +11,5 | |
| Filete a cada golpe: 1/5 por 3 · 1/4 por 5 · 1/5 por 3, somando | +7,3 · +9,0 · +14,5 | |
| Medo a cada golpe contra 17 · 18 · 20 · 22 · 24 · 26 · 29 (escada de 2.6) | +4,8 · +6,0 · +10,4 · +15,0 · +19,8 · +25,3 · +32,0 | o mais forte por categoria |
| Temível contra 20 · 24 · 29 (escada de 2.6) | +2,7 · +7,4 · +15,2 | |
| Segundo golpe 1 · 2 vezes por luta · Ponta certa 1 vez · 3 vezes | +3,8 · +7,9 · +5,1 · +13,1 | a pesquisa os punha no forte e no apelão |
| Imortal (uma vez por luta) | +5,6 | vale a vida, não a vitória |
| a iniciativa a mais (+2 · +4 · +8 · +20) · a ação a mais na 1ª rodada | +0,6 · +0,4 · +0,3 · −0,6 · +2,7 | a iniciativa saiu do catálogo |
| o golpe de espada que custa 1 de fôlego a menos · o de martelo · fôlego máximo +2 · +4 | −0,3 · +13,3 · +2,8 · +3,4 | só a arma pesada |
| Perfura ×0,8 · ×0,67 · ×0,5 · ×0,4 · ×0,33, contra a armadura uma acima (hoje 8,2%) | +4,6 · +9,3 · +21,9 · +32,8 · +40,9 | |
| no um contra dez (hoje ~50%): ceifadora · em cadeia · tempestade de todos · de um · varredura · Gume +50% · vampira 25% · imortal · temível 24 · segundo golpe | +15,8 · +18,4 · +44,1 · +20,6 · +14,6 · +12,2 · +20,7 · +5,6 · +12,0 · +3,9 | |
| no 3 contra 3 (os três com o efeito): Gume +15% · ceifadora · tempestade de todos · varredura · medo 24 · aturdir carga 4 e 6 | +8,1 · +0,9 · +28,5 · +11,0 · +21,3 · +17,6 e +21,7 | |
| o duelo de um ferreiro novo (nível 10, martelo Incomum, Iniciante): Gume +15% · +30% · o `critico_19` · Certeira +2 · o `devolve` 4 | +2,8 · +8,1 · +11,4 · +5,9 · +2,2 | os % rendem menos com golpe grande |
| combinações: Gume 20% e Vampira 15% · Gume 30% e a perfura ×0,5 de sempre (em toda armadura: a que saiu) · Certeira 3 e Guarda 3 | +10,2 · +36,6 · +19,0 (a soma das partes: 10,7 · — · 20,9) | a pilha |

- **No nível 10 os % rendem menos** (o golpe tira um terço do PV, e +15% raramente muda quantos golpes faltam); o crítico rende o mesmo. A régua do banco é a do nível 50.

---

## 3. Os dados (o que muda na ficha, no item e nos eventos)

### 3.1 No item (`itens.json`: o registro de hoje ganha campos; nada sai)
| Campo | Forma | O que é |
| --- | --- | --- |
| `efeitos[]` | `{chave, cheio?, contra?, vidro?, gasto?}` (e o `emprestado?` do D2) | `chave`: uma do catálogo (`tabelas_efeitos.EFEITOS`) · `cheio: true`: o número da categoria de cima (só nos de número) · `contra`: o tipo da Caçadora (bicho, morto, povo, gente, dragão) · `vidro: true`: o efeito de vidro (2.11) · `gasto: {dia, n}`: os usos do dia já gastos (Imortal, Domínio) |
| `valor` do `devolve` | some | o devolve vira % da categoria; a peça antiga perde o número por evento do Mestre |
| `maldita` (já existe) | `true` | o ferro rancoroso é maldito (13.3) |

- **O número nunca se guarda:** `tabelas_efeitos.valor(chave, cat, cheio, vidro)` o tira da categoria que a peça rende agora (a que dorme rende uma abaixo e tem os efeitos
  dormindo; a quebrada não tem efeito: as duas regras de hoje).
- A Sede do rancoroso é um efeito como os outros (`chave: 'sede'`), que só cabe em peça maldita.

### 3.2 Na pessoa (`gente.json`)
Nada fixo novo. A maldição do rancoroso é uma maldição de hoje (13.1) com dois campos novos e uma condição nova: `anda: 'uso'` (não rola na virada: anda pela Sede),
`desce: 7` (desce um passo a cada 7 dias sem a Sede acordar) e a condição `{tipo: 'contrapeca', cat}`.

### 3.3 Na luta (o arquivo da luta, por lutador; volta ao estado só o que é do mundo)
| Campo | O que guarda |
| --- | --- |
| `fx` | os efeitos acordados, já somados pela pilha: `{gume: 0.30, certeira: 3, critico: [19, 11], ...}`; os de regra com usos em `fx_usos` |
| `carga` | `{cabeca, mana, pernas}`: a barra de cada família |
| `calejo_f` | `{cabeca, pernas, mana, animo}`: os calejos da luta |
| `firme_cabeca` | até quando a cabeça está firme (o fim do primeiro turno em que o alvo volta a agir) |
| `filetes` | `[[por rodada, rodadas, fonte], ...]`, até 3 (o `sangra` de hoje é o filete da ferida) |
| `exposto`, `amolecido`, `aberto` | a rodada em que cada um vence |
| `medo` | o degrau, de 0 a 2 (o `abalado` de hoje é `medo ≥ 1`), e `susto_r` (a rodada do último susto) |
| `usou` (já existe) | ganha as chaves dos de uma vez por luta (segundo golpe, ponta certa, refletora, escudo que conta, arrancada) |
| `S['conta']` | os contadores que o banco lê (atordoar, exposto, filetes, degraus do medo, golpes extras, curas da vampira) |

### 3.4 Os eventos (`estado.py`)
| Efeito | Novo? | O que faz | Em que evento |
| --- | --- | --- | --- |
| `['item', id, 'efeito', 'junta', {chave, cheio?, contra?, vidro?}]` | já existe; a validação muda | confere no catálogo: o tipo de peça; a porta (a categoria ≥ a porta da faixa; com vidro, uma abaixo; a Sede, da Épica para cima e só em peça maldita); o cheio só em número; a Caçadora com `contra`; um apelão de regra por peça; o teto de efeitos da categoria (o do D2) | forjar, mestre, gera |
| `['item', id, 'efeito', 'gasta', chave]` | **novo** | marca um uso do dia (`gasto: {dia, n}`); recusa se o dia já não dá | luta, mestre |
| `['item', id, 'efeito', 'tira', chave]` | **novo** | o efeito sai da peça: o vidro que se partiu, a Sede que a contrapeça quebrou, o erro do Mestre desfeito | luta, mestre |
| `['item', id, 'dur', 'soma', -N]` | já existe | a peça de vidro que se parte vai a zero | luta |
| `['maldicao', id, 'poe', registro]` | já existe; campos novos | a maldição do rancoroso (`anda`, `desce`, a condição `contrapeca`) | forjar, mestre |
| `['maldicao', id, MID, 'passo', 1]` | já existe | o rancor que anda pela Sede | luta |

- **A luta que volta ao estado** (o evento "luta", 11.12) leva também: os usos do dia gastos, a peça de vidro partida (a durabilidade e o efeito) e os passos do rancor.
  Tudo num evento só, como hoje.
- **Nada muda sem evento:** a peça da história ganha efeito por evento "mestre" (no mundo novo, no "gera"); o tesouro, no evento da sala ou do covil; o rival, no da obra dele.

---

## 4. Onde entra no motor

| Arquivo | Função | O que muda (M) ou é novo (N) |
| --- | --- | --- |
| `tabelas_efeitos.py` | (página nova) | N: o catálogo (chave, número ou regra, peças, faixa, porta, os 8 valores, a frase), as faixas, a pilha (grupos e tetos), a carga, as famílias, a escada; `valor(chave, cat, cheio, vidro)`. Nenhum número de efeito fora dela |
| `tabelas.py` | `devolve_max` | M: sai (o devolve vira %); `CRIT_OUTRO` fica (é a base: 20/11) |
| `itens.py` | `EFEITOS`, `item()` | M: o `EFEITOS` passa a ser montado do catálogo (frase e peças); `item()` confere a porta, o tipo, o cheio, o vidro e a Caçadora |
| `pessoas.py` | `_efeitos`, `_arma`, `ficha` | M: `_efeitos` devolve `{chave: valor}` já resolvido; `ficha` monta `F['fx']` (a pilha das peças acordadas, com os tetos) e `F['fx_usos']`; a sintonia conta o apelão de regra como 2 lugares e acorda um só |
| `luta.py` | `jogada` | M: recebe a faixa do crítico (face alta, outro dado) no lugar de `crit19` |
| `luta.py` | `golpe` | M: os ganchos: acerto (Certeira, Desforra), Defesa (Guarda, aberto), o crítico e o golpe do fim, a proteção (Perfura), o dano (a pilha), e o depois do golpe (a carga, o filete, a vampira, o exposto e o amolecido, o medo, o devolve em %, o segundo golpe, a ceifadora, a varredura e a tempestade, a brasa) |
| `luta.py` | `_ferida`, `_fecha_rodada` | M: os filetes; o exposto, o amolecido e o aberto que vencem; o acuado que desce; a regenera |
| `luta.py` | `_cai` | M: o Imortal (e o vidro que se parte quando o dono cai) |
| `luta.py` | `_moral` | M: a escada (o acuado; o medo de peça, uma vez por rodada) |
| `luta.py` | `_turno`, `_abre_rodada` | M: o atordoar da carga (perde o turno, a cabeça firme), a arrancada, o Temível no começo |
| `luta.py` | `ordem`, `situacao` | M: as ordens `atar [ALIADO]` e `sede`, e `lancar ... dominio`; o quadro mostra a barra de carga do inimigo, os filetes, o exposto, o amolecido e o acuado |
| `magia.py` | `_dano`, `conj`, `firmeza`, `resolve`, `decide` | M: a Chama e a Guarda Mágica no dano, o Foco Certeiro na Conjuração, a Firmeza, a Refletora, o Domínio, o calejo por família |
| `oficio.py` | `efeitos_que_cabem`, `efeito` | M: lê o catálogo (o tipo, a porta, a Caçadora pede o tipo) |
| `historia.py`, `gera.py` | (nova) `efeitos_da_semente(semente, peca)` | N: os efeitos das peças altas pela semente e pelo tema do nome (2.12); o `gera` os põe no mundo novo |
| `efeitos.py` | (comando novo) | N: `efeitos.py ver ITEM` (a frase de cada efeito com o número de hoje) e `efeitos.py semente ITEM` (o que a semente dá; só olha) |
| `masmorra.py`, `dragoes.py` | o tesouro | M: a peça Rara ou melhor sai com efeito pela chance da categoria |
| `rivais.py` | a obra do rival | M: a obra-prima dele escolhe pela semente, pelo papel |
| `estado.py` | `aplica`, `valida` | M: os ops `gasta` e `tira`; a validação pelo catálogo; os campos novos da maldição |
| `provas.py` | (novo) `efeitos(n)` | N: o bloco EFEITOS (seção 5) |
| `estresse.py` | | M: os invariantes da pilha e da carga nas lutas ao acaso |

---

## 5. O banco (as metas, no bloco novo `provas.py efeitos`)
O padrão é o do banco de hoje: o duelo de iguais do nível 50, tudo Raro, perto. **2.000 lutas por linha** no modo de sempre (±1,6) e **20.000** no modo longo (±0,7, o
desta medida). A folga é de 1 ponto nas bordas da faixa.

| Meta | O que se mede | Como | Faixa aceita |
| --- | --- | --- | --- |
| EF1 A régua dos números | cada efeito de número, em cada uma das 8 categorias | duelo de iguais (a Perfura, contra a armadura uma acima; a Chama, o Foco Certeiro, a Guarda Mágica e a Firmeza, no mago contra mago; a Robusta, contra a carga de mesma categoria; a Coragem, contra o Medo de mesma categoria) | nunca acima do teto da faixa da categoria (Comum 5, Incomum e Rara 10, Épica e Única 20, da Lendária para cima 40); cada coluna não menor que a da esquerda |
| EF2 A régua das regras | cada efeito de regra | no cenário dele (2.9) | do piso ao teto da faixa dele |
| EF3 O item decide | a arma uma acima, sem efeito, contra a de baixo com quatro efeitos cheios; e o conjunto uma acima, sem efeito, contra o de baixo com tudo cheio | 4.000 lutas | com quatro cheios, 75% ou mais (medido: de 76,7 a 80,2%); com o teto inteiro do D2, tudo cheio e os mais fortes, 60% ou mais (medido 62,0%); o conjunto, 85% ou mais (a medir) |
| EF4 A pilha | 10.000 golpes sorteados com as piores combinações que cabem | conta | o multiplicador nunca passa de ×5; a couraça nunca de 75%; acerto, Defesa, Firmeza e coragem de efeito nunca passam de +8; o crítico nunca melhor que 17/7 |
| EF5 O atordoar não trava | a carga Primordial contra um alvo de Vigor 50 | 2.000 lutas | nenhum alvo perde o turno pela carga em dois turnos seguidos; o alvo age em pelo menos 2 de cada 3 turnos |
| EF6 O calejo | o número de golpes até o 1º e até o 2º atordoar da luta | média | o 2º pede pelo menos 1,4 vez os golpes do 1º |
| EF7 A escada do medo | o módulo 8; quem o jogador comanda contra o Medo de peça; a Coragem contra o Medo | 3.000 e 600 lutas | o módulo 8 em 30% ou mais (medido 39%); 0 fugas e 0 rendições de quem o jogador comanda; a Coragem de mesma categoria corta pelo menos metade do Medo (medido: +4 corta o Medo 22 de +15,0 para +5,1) |
| EF8 Os freios do apelão | a ficha com duas peças de apelão; a sintonia; o Imortal | conferência | só a melhor acorda; o apelão vale 2 lugares; o Imortal salva uma vez por dia, e no outro dia de novo |
| EF9 Os preços | a peça de vidro; o rancor; a contrapeça | 600 lutas | o vidro se parte em todas as lutas em que o dono cai, e só nelas; o rancor anda um passo por luta com a Sede e nenhum sem ela; a contrapeça quebra a maldição |
| EF10 A luta sem efeito | as lutas de hoje, com semente fixa | o banco inteiro | sai igual, dado por dado, menos a escada do medo; as 114 metas de hoje passam |
| EF11 As peças do mundo | a semente; o tesouro | 2.000 tesouros | a mesma semente dá os mesmos efeitos; cada peça da história com o teto de efeitos, na porta, o tema do nome no primeiro, sem cheio nem preço; o tesouro na chance da categoria (±5 pontos) e nunca com apelão de regra |
| EF12 O ano | o `provas_ano.py` com os rivais de peças de efeito | o ano | os rivais não matam o dragão no primeiro mês, e a corrida continua com mortos (PROJETO 2.5) |

---

## 6. O que fica para depois, os riscos e as perguntas

**Para depois.**
- A carga que as técnicas enchem (a Roda, o trunfo do "tranco") e o dano das técnicas e dos dons: os grupos da pilha já os esperam (TÉCNICA +40%, DOM +20%).
- Cada poder de lenda é uma regra própria: o banco mede um por um quando a peça nascer, de 20 a 40.
- O tiro: valem no arco e na besta todos os efeitos de arma, menos a Varredura, a Tempestade e o Fôlego; o Devolve (da armadura) só pega quem golpeia de perto.
- O bicho não tem peça: o corpo dele não leva efeito. O chefe que quiser algo parecido ganha traço, pela regra dos bichos.

**Os riscos.**
1. **O medo é o efeito mais forte por categoria no duelo**, junto com o crítico: contra gente que testa a coragem, quem quebra perde a luta. Contra o chefe (moral firme),
   não age; contra quem o jogador comanda, só abala. O ano (EF12) tem de olhar a gente comum do mundo (os bandos) contra rivais de peça de medo.
2. **A varredura e a tempestade** são os efeitos que mais pesam contra muitos (+14,6 e +20,6 no um contra dez); a de "todos os colados" passava do apelão (+44).
3. **A vampira contra muitos** (25% dá +20,7 no um contra dez): o teto da cura do dia é o que a segura.
4. **A escada do medo toca toda luta de gente.** O módulo 8 passa (39%), mas cai 13 pontos.
5. **Os números marcados (c) e (d)** são conta e desenho: o banco é que decide.
6. **No nível baixo os % rendem menos** (nível 10: o Gume de +15% dá +2,8), e o crítico rende o mesmo: na mão de Ferord hoje, o crítico pesa mais que o dano.
7. **A peça cheia no teto do D2** (seis efeitos, todos cheios e os mais fortes) deixa a arma de cima com 62%: ainda decide, mas por pouco. O banco vigia (EF3); se cair abaixo
   de 60, o remédio é um efeito de controle (Aturdir, Medo, Expõe, Escancara, Amolece, Atar) por peça.

**As perguntas ao jogador** (cada uma com a recomendação):
1. **O `critico_19` de hoje vale +11,9 (forte), e está no martelo Incomum de Ferord.** (a) A peça que já o tem fica com ele ("o que nasceu, nasceu"), e as novas seguem a
   tabela do Crítico (a Incomum, 20/7: +6,8). (b) Toda peça passa à tabela agora (o martelo cai para 20/7). (c) Nada muda: a obra-prima segue dando o 19 em qualquer peça.
   **Recomendo (a).**
2. **O `devolve` fixo quebra (o teto da Rara vale +21,3).** (a) Vira % do dano levado, pela categoria (2.8). (b) Segue fixo, com teto de 1 por categoria. **Recomendo (a).**
   (O D2 escreveu o devolve de hoje, de 1 a 4 por degrau; com (a), o cheio do devolve passa a ser o % da coluna de cima.)
3. **O atordoar.** (a) Pela carga: perde o turno inteiro e fica aberto (−4 na Defesa), com a cabeça firme e o calejo (+8,0 na Incomum a +22,1 na Primordial). (b) Pela carga,
   perdendo só 1 ação (não pesa: 0 a +2,5). (c) Pela chance por golpe (10 a 30%: +3,8 a +9,9, e rola um dado a cada golpe). **Recomendo (a).**
4. **A escada do medo muda toda luta de gente** (o acuado entre o abalado e a quebra). (a) Sim, a escada de 2.6. (b) Só o medo de peça usa a escada. **Recomendo (a).**
5. **O medo de peça contra o bicho.** (a) O bicho que falha foge, como hoje (a arma de medo espanta a caça; quem caça escolhe outra). (b) Contra o medo de peça, o bicho só
   fica abalado. **Recomendo (a).**
6. **Onde fica o +50%.** (a) No Gume da Lendária, no cheio da Única e na Sede do rancoroso numa Épica (com o preço). (b) Já no Gume da Única (dá +20,5: passa do forte por
   meio ponto). **Recomendo (a).**
7. **O apelão de regra ocupa 2 lugares da sintonia e só um acorda por vez.** (a) Sim. (b) Só um por vez, sem o lugar dobrado. **Recomendo (a).**
8. **A iniciativa a mais não pesa nada** (de −0,6 a +0,6). (a) Sai do catálogo, e entra a Arrancada (uma ação a mais na primeira rodada: +2,7). (b) Fica, como fraco de nome.
   **Recomendo (a).**
