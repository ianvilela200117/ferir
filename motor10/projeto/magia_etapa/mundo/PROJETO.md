# Motor 10, a etapa da magia e dos dons: projeto "O MUNDO PRIMEIRO"

Este projeto parte de uma pergunta: como é um mundo em que qualquer um aprende magia, há poção na prateleira, maldição que mata e quatro jeitos diferentes de fazer um feitiço? Primeiro o mundo (quem faz, de onde vem, quanto custa, o que o povo teme). Depois as regras, que saem dele.
Tudo o que está marcado **(medido)** foi rodado em rascunho por cima do motor de hoje, sem editar nada dele: a luta é a do `luta.py`, o mercado é o do `mercado.py`, e os robôs são os dos bancos (o ferreiro do `provas_oficio.py`, o ferreiro de loja do `provas_mercado.py`, o coletor do `provas_caca.py`). O que está marcado **(chute)** é número que só o banco vai dizer.
Os rascunhos e as saídas estão nesta pasta (`magia_rascunho.py`, `mede_*.py`, `saida/`). As medidas de luta são de 400 lutas por linha: balançam uns 5 pontos para cada lado.

## 0. Em uma página

1. **A lei do motor vale para tudo que é magia.** O foco é a arma, o amuleto é a armadura, a poção vale contra a categoria do que feriu, o antídoto contra a do veneno, o amuleto contra o grau da maldição. Sempre a mesma conta: o que decide é a diferença de categoria.
2. **Aço se apara com aço; feitiço se apara com amuleto.** Sem amuleto, a armadura guarda um degrau abaixo. Medido: o guerreiro sem amuleto perde para o mago igual a ele em 99% das lutas de longe. Com um amuleto da categoria, o mago de cajado fica em 50 a 59% de longe, 35% de perto e 23 a 28% colado. "Pescoço sem amuleto é por onde o feitiço entra", como "cabeça sem elmo é onde se morre".
3. **Talento é pressa e teto; dom é poder.** Toda pessoa nasce com um talento em cada uma de dez vocações (do avesso ao prodígio: o bloco de treino vale de dois terços a três). Uma em vinte e cinco nasce com um dom, que soma na conta. Medido: um dom vale de 53 a 60% entre iguais; uma categoria de peça vale 95%. Dom e mão juntos não compram uma categoria (14%).
4. **Quatro tradições, uma Mana, quatro fontes.** O mago estuda e fere de longe. O clérigo serve um santuário, cura e quebra maldição. O druida bebe da terra e manda no chão e nos bichos. A bruxa paga com sangue e amaldiçoa. Cada uma tem lista própria, um preço próprio e um jeito próprio de dar errado.
5. **A poção é um bem do mercado; o elixir é uma peça contada.** Do Comum ao Raro a poção se compra, se vende e tem preço pelo estoque, como a matéria. Do Épico para cima é item do Livro, feito com núcleo, sem loja. Medido com o robô do banco: o alquimista de loja tira 3,9 a 4,7 de prata por dia nos cinco primeiros dias e nada depois. Não é mina.
6. **A maldição tem grau, dono, relógio de seis passos e uma condição.** Um teste por virada do dia, pelo dado do mundo. Sem amuleto, no grau Comum, mata em cerca de 15 dias (conta exata). Quebra por quem a pôs, pelo clérigo, ou cumprindo a condição. A poção só ganha tempo.
7. **A peça encantada não decide entre iguais.** O feitiço gravado sai uma vez por luta e vale um degrau abaixo da peça: medido, 46 a 50% contra o gêmeo. O que vale são os efeitos passivos que o motor já tem (de 55 a 70%, medido), que passam a nascer do encanto. E encanto que falha feio amaldiçoa a peça: é de onde vêm as peças amaldiçoadas do mundo.
8. **Nada novo cria prata.** Serviço de magia é jornal (a mesma jornada de 2 blocos pagos). Donativo, dízimo e compra só mudam a prata de mão.
9. **O que achei de ruim e não escondo:** o arqueiro esmaga o mago (18 a 21%); o mago num grupo contra gente bem guardada vale menos que um quarto guerreiro (34 a 38%); o curandeiro numa luta só vale menos que um guerreiro (36%) e só se paga em lutas seguidas (65 contra 58); viver só de erva e poção dá prejuízo de meia prata por dia.
10. **Fica de fora desta etapa:** invocar, voar, iludir, ressuscitar; desfazer feitiço alheio; a poção que estraga; o canto; o dom ganho em vida; a maldição de linhagem e a peste (são das etapas 6 e 7).

## 1. O mundo com magia em todo lado

### 1.1 Quem faz o quê

| Quem | Onde vive | O que faz pelo povo | De que vive |
| --- | --- | --- | --- |
| a curandeira (ofícios `cura` e `alquimia`) | toda aldeia tem uma; a vila tem botica | trata ferida, faz remédio e poção Comum, diz se é doença ou maldição | do jornal da botica e do que vende |
| o clérigo (tradição `fé`) | onde há santuário: da vila para cima | cura na hora, abençoa, quebra maldição, enterra os mortos para que não andem | do donativo e do dízimo |
| a bruxa (tradição `pacto`) | na borda, fora da vila | põe e tira mau-olhado, lê sorte, peça e maldição, vende veneno | de quem a procura de noite |
| o mago (tradição `arcano`) | cidade e capital; em vila, só de passagem | serve a quem paga: guarda de senhor, encanto de peça, guerra | de soldo e de encomenda |
| o druida (tradição `verde`) | no ermo, do interior para dentro | acalma bicho, acha caminho, cura devagar; não entra em cidade | de troca; não usa prata à toa |
| o encantador | cidade com forja de cidade para cima | grava feitiço e efeito em peça | de encomenda |

### 1.2 De onde vem cada coisa

| Coisa | Vem de | Já existe no motor? |
| --- | --- | --- |
| erva (Comum, Incomum, Rara) | coleta no ermo; a Incomum e a Rara só do interior | sim (9.12) |
| osso (Comum a Raro) | despojo de bicho. Hoje quase não serve para nada: passa a ser a matéria do amuleto, do fetiche e do encanto. O couro segue só na armadura | sim |
| sal, carvão, remédio | bens do mercado. O sal entra na água benta e no rito de lugar; o remédio é o que a curandeira gasta ao tratar | sim (8.3) |
| **peçonha** (Incomum, Rara) | despojo novo: surucucu 1 Incomum; aranha-de-toca 1 Rara; basilisco 2 Raras. É a matéria do veneno de lâmina e do antídoto forte | **falta** (uma matéria nova) |
| **água benta** | o clérigo faz: 1 de sal e 1 bloco de reza rendem 3 | **falta** (um bem novo) |
| núcleo (Épico para cima) | chefe morto, como hoje. Entra no elixir, no foco, no amuleto e no encanto altos | sim (6.11) |
| foco e amuleto | a forja faz, como faz a adaga: 1 unidade de matéria (o cajado, 3) | **falta** (dois tipos de item) |

### 1.3 O que a gente comum sabe e teme (e o que é verdade em número)

| O povo diz | O que o motor faz |
| --- | --- |
| "Criança sem amuleto não sai de casa." | Sem amuleto, o teste diário contra maldição tem −4, e o feitiço entra pela armadura um degrau abaixo. Um amuleto Comum custa 10 de prata: duas diárias e meia. Uma casa em três tem um. |
| "Não se tira nada de morto." | Peça de morto pode estar amaldiçoada (1.5). A regra de hoje já diz que o que era do morto não muda de mão sozinho (5.11). |
| "Sal na soleira." | O sal entra no rito que limpa um lugar amaldiçoado (5.4). Na soleira, é só costume. |
| "Maldição pega quem quebra a palavra." | Juramento com testemunha de santuário, quebrado, vira a maldição da marca (5.2). |
| "A bruxa faz e a bruxa desfaz." | Quem atou desata sem teste. Morta a bruxa, o que ela atou se quebra. |
| "Mago é coisa de cidade." | Numa vila de 400 não há mago residente. Ninguém em Pedra Rasa viu uma lança de fogo. |
| "Poção de cura é coisa de guarda." | A dose Comum custa 11 na loja: onze dias do que sobra a um diarista. |
| "Veneno é crime." | Vender e usar veneno de lâmina numa vila é gancho da etapa 3 (a opinião e o guarda). |

O povo **não sabe** o grau de uma maldição, o passo em que ela está, nem quem tem dom. Isso é do Mestre, ou de quem lê (1.4).

### 1.4 O que a loja vende, e o que custa um serviço

Os preços seguem as regras de hoje: peça pela matéria que leva, vezes 6 por categoria; bem pela base, com 10% a mais na compra e 60% na venda.

| Na prateleira de uma vila | Preço |
| --- | --- |
| amuleto, varinha, símbolo, fetiche (1 unidade de matéria, como a adaga) | Comum 10 · Incomum 60 · Raro 360 (o Raro, só em cidade) |
| cajado (3 de madeira) | Comum 30 · Incomum 180 |
| remédio | 9 |
| poção de cura | Comum 11 · Incomum 66 (cidade) · Rara 396 (só de quem traz) |
| antídoto | Comum 9 · Incomum 53 |
| água-de-lua (Mana) · desate (contra maldição) · água benta | 11 · 14 · 4 |

| Serviço (a prata vai para o lugar; ninguém a cria) | Preço | Quem faz |
| --- | --- | --- |
| tratar uma ferida (ela passa a sarar em metade dos dias) | 1 remédio e 2 de prata | a curandeira |
| ler um talento (2 blocos vendo a pessoa trabalhar) | 6 | um Treinado da vocação |
| ler uma peça, uma maldição ou um dom | 5 | a bruxa (o feitiço `olho`) |
| uma cura por milagre | 3 por círculo | o clérigo |
| quebrar uma maldição | o preço de um amuleto do grau: 10, 60, 360, 2.160 | o clérigo (ou a bruxa que a pôs) |

### 1.5 Quantos há no mundo (alvo para o gerador da etapa 7; hoje é chute)

Em 10.000 pessoas: cerca de 160 com alguma mão de magia ou de botica (1,6%). Todo mundo conhece alguém que faz; quase ninguém faz.

| | Iniciantes | Treinados | Mestres | Lendários | Onde |
| --- | --- | --- | --- | --- | --- |
| botica e cura | 40 | 20 | 5 | 0 | uma por 150 pessoas |
| fé | 20 | 15 | 4 | 1 | um santuário por lugar com povo |
| arcano | 12 | 9 | 3 | 1 | só cidade e capital |
| pacto | 8 | 5 | 2 | 0 | escondidas, na borda |
| verde | 6 | 4 | 2 | 0 | um círculo por floresta grande |

- **O raro continua contado.** Foco e amuleto são peças: das 12 Épicas do mundo, 3 são focos ou amuletos; das 4 Únicas, 1; das 3 Lendárias, 1. A conta do mundo não sobe.
- **Peças amaldiçoadas:** nascem de encanto que falhou feio e de quem morreu amaldiçoado vestindo a peça. Alvo: 1 em cada 20 peças Raras ou melhores achadas em ruína.
- **Dos 40 rivais,** 8 lançam feitiço (3 magos, 3 clérigos, 1 druida, 1 bruxo). O resto usa amuleto: é o que faz o mago valer menos contra eles do que contra um bando sem amuleto (3.9).

## 2. A. Os dons e os talentos

### 2.1 O que são

- **Vocação:** um grupo de caminhos que se aprendem do mesmo jeito. São dez, e cobrem tudo que tem maestria no motor.
- **Talento:** o jeito que a pessoa tem para UMA vocação. Toda pessoa tem um grau de talento em cada uma das dez. Muda a **pressa** (quanto vale cada bloco de treino) e o **teto** (até onde a mão sobe). Não soma em conta nenhuma.
- **Dom:** uma coisa rara, de nascença, com nome, de uma lista fechada. Soma na conta: é o **poder**. Uma pessoa em 25 tem um.

```python
# tabelas_dons.py
VOCACOES = {
    'guerra': ['punho', 'adaga', 'espada', 'maça', 'machado', 'martelo', 'lança', 'montante', 'alabarda', 'malho'],
    'tiro':   ['arco', 'besta'],
    'forja':  ['forja', 'couro'],
    'mato':   ['caça', 'coleta'],
    'trato':  ['comércio'],
    'botica': ['cura', 'alquimia'],
    'arcano': ['arcano'], 'fé': ['fé'], 'verde': ['verde'], 'pacto': ['pacto'],
}
TALENTOS = {-1: 'avesso', 0: 'comum', 1: 'jeitoso', 2: 'talentoso', 3: 'prodígio'}
RENDE = {-1: 2 / 3, 0: 1, 1: 1.5, 2: 2, 3: 3}      # quanto vale UM bloco de treino na conta da maestria
TETO = {-1: 4}                                    # o avesso para em Treinado; os outros vão até Lendário
SEM_FEITO = {3: 6}                                # o prodígio chega a Mestre sem o feito (o de Lendário, todos devem)
NASCE = [(100, -1), (845, 0), (965, 1), (995, 2), (1000, 3)]      # o dado do mundo (1 a 1000), por vocação
SANGUE = 2                                        # filho de quem é jeitoso ou mais numa vocação: rola isto de vezes e fica com o melhor
DOM_CHANCE = 40                                   # em 1000: a pessoa nasce com um dom (uma em dez dessas, com dois)
```

| Talento | Quantos (por vocação) | O bloco vale | Os blocos de arma até cada grau (hoje: 40, 160, 500, 1.500) | Treinado em (a 3,5 blocos por dia) | Teto |
| --- | --- | --- | --- | --- | --- |
| avesso | 10% | dois terços | 60, 240, e para aí | 69 dias | Treinado |
| comum | 74,5% | 1 | 40, 160, 500, 1.500 | 46 dias | Lendário, com os feitos de hoje |
| jeitoso | 12% | 1,5 | 27, 107, 333, 1.000 | 30 dias | Lendário |
| talentoso | 3% | 2 | 20, 80, 250, 750 | 23 dias | Lendário |
| prodígio | 0,5% | 3 | 13, 53, 167, 500 | 15 dias | Lendário; Mestre sem o feito |

A tabela do ofício (50, 150, 375, 1.000), a da caça e da coleta e a dos dias de negócio seguem a mesma conta: o número da tabela não muda; muda quanto vale o bloco de quem treina.

Com dez vocações, uma pessoa tem em média uma em que é avessa e uma em que tem jeito. Três em dez são talentosas em alguma coisa, quase sempre na que não praticam. Em 10.000 pessoas há 50 prodígios da forja, e a maior parte nunca pegou num martelo: achar um é coisa que se joga.

### 2.2 Os dons (lista fechada: só entra o que o motor sabe rodar)

| Dom | Vocação | O que soma | Medido entre iguais |
| --- | --- | --- | --- |
| mão certa | guerra | +2 no acerto de corpo a corpo | 60% |
| olho longe | tiro | +2 no tiro | (como o de cima) |
| couro grosso | o corpo | PV × 1,15 | 59% |
| fôlego fundo | o corpo | +2 de fôlego | 53% |
| pé leve | o corpo | +2 na Defesa | 57% |
| mão de fogo | forja | +2 no teste de forjar, ajustar e encantar | vale um grau de maestria |
| faro | mato | +2 no rastro e na coleta | idem |
| língua de prata | trato | a loja paga 5 pontos a mais | vale um grau de comércio |
| mão que fecha | botica | +2 no teste de alquimia; o que ela cura, cura um quarto a mais | (chute) |
| veia funda | magia | Mana × 1,5 | (chute) |
| voz que manda | magia | +2 na Conjuração | 57 a 60% |
| pele de sal | a alma | +4 no teste diário contra maldição | (conta: dobra o prazo) |

**A régua, medida (nível 50, tudo Raro, mão de Mestre):** iguais 48 a 54%. Um grau de maestria a mais: 56 a 67%. Um dom: 53 a 60%. **A arma uma categoria acima: 95%.** Contra a arma uma acima, quem tem o dom vence 5%; com o dom e um grau de maestria a mais, 14%; Mestre com dom contra Leigo de arma melhor, 24%. Nenhum dom vale mais que um grau de maestria, e nem os dois juntos chegam perto de uma categoria.

### 2.3 Como nascem, e quem sabe

- **Gente gerada:** no evento que a faz nascer, o dado do mundo (`estado.sorte`) rola cada vocação e o dom. Quem o gerador faz aventureiro rola de novo a vocação que segue até ter jeito nela, e tem o dobro de chance de dom: talento puxa a pessoa para o caminho.
- **O personagem do jogador:** escolhe UMA vocação em que é talentoso. O mundo rola as outras nove e o dom, e guarda. (É a pergunta 2 do fim.)
- **O herdeiro:** rola tudo, com o sangue: na vocação em que o pai ou a mãe tinha jeito, rola duas vezes e fica com o melhor. O filho do guerreiro pode nascer prodígio do arcano. Herda o sangue; não herda a mão.
- **Descobre fazendo.** O talento fica escondido (na `MESA.md`, só na parte do Mestre) até aparecer:
  - quando a pessoa chega a Iniciante numa vocação, a mesa diz com quantos blocos chegou e o nome do talento;
  - o avesso descobre quando passa do número do comum sem subir ("já devia ter pegado");
  - **ler o talento:** um Treinado da vocação vê a pessoa trabalhar 2 blocos e testa Percepção contra 24 (rolagem oculta). Passou, diz. Custa 6 de prata. Em Pedra Rasa lê-se guerra, tiro, forja, mato, botica, fé e pacto. Arcano e verde, não: é ir à cidade ou ao mato.
- **O dom aparece na primeira vez que conta:** a rolagem mostra "+2 do dom", e a mesa passa a dizer o nome.

### 2.4 O que isso faz com as metas de hoje

- **A pessoa comum não muda.** Talento 0 e nenhum dom: todo número de hoje fica igual. Os robôs dos bancos são comuns. Prova nova: o retrato do estado de três vidas de robô, com e sem o módulo, é idêntico.
- **A escada do ferreiro, por talento (medido: o robô do `provas_oficio.py`, 10 vidas por linha, na forja mestra com o preparo todo):**

| Talento na forja | A primeira Rara | A primeira Épica | A primeira Única |
| --- | --- | --- | --- |
| avesso | Dia 24 | Dia 80 | não nasce na metade das vidas até o Dia 200 |
| comum (a régua do banco: 17, 59, 177) | Dia 17 | Dia 59 | Dia 177 |
| jeitoso | Dia 13 | Dia 44 | Dia 151 |
| talentoso | Dia 10 | Dia 30 | Dia 131 |
| prodígio | Dia 10 | Dia 26 | Dia 114 |

O prodígio ganha um mês na Épica e dois na Única. Não ganha mais porque a obra pede os blocos dela (27 e 81) e o dado é o mesmo. O talento adianta a mão; não adianta a bancada nem acha núcleo. "A conquista é difícil" fica de pé.
- **O avesso não tranca nada,** só o topo: para em Treinado. Na forja isso quer dizer nunca ter a mão que a obra Única pede.

### 2.5 Uma cena na vila de teste

Maro treina a espada: `python3 ato.py treinar 3 espada`. Ele escolheu guerra como a vocação dele. A resposta: "Maro treina 3 blocos com espada (rendem 6: talentoso em guerra). Espada: 46 de 160 para Treinado." Um comum estaria em 43. A este passo ele é Treinado em 17 dias de treino, não em 34.

Na forja, Zeca, o aprendiz, já fez 60 blocos de bancada e segue Leigo. `python3 dons.py ler forja quem=zeca com=bento` custa 2 blocos do Bento e 6 de prata. Sai "rolagem oculta". Na parte do Mestre: Percepção do Bento, 23 contra 24, falha. Bento coça a cabeça e não sabe dizer. No dia seguinte, de novo: 31 contra 24. "Zeca é avesso à forja: cada bloco rende dois terços, e ele para em Treinado."

O que ninguém em Pedra Rasa sabe ler está só na parte do Mestre: `Zeca: arcano, prodígio (oculto)`. Se um dia alguém lhe puser uma varinha na mão, ele chega a Iniciante no arcano em 14 blocos de estudo, não em 40, e a mesa conta.

## 3. B. A magia na luta

### 3.1 A conta (a do aço, espelhada)

| | O aço (hoje) | A magia |
| --- | --- | --- |
| quanto se acerta | Acerto = maestria + (Força + Agilidade) ÷ 40 + bônus da arma | **Conjuração** = maestria da tradição + (Afinidade + Vontade) ÷ 40 + bônus do foco |
| contra o quê | a Defesa: 22 + Agilidade ÷ 20 + maestria ÷ 2 + armadura + o que apara (escudo ou arma) | **o que voa:** a mesma Defesa, mas quem apara é o amuleto (o bônus da categoria dele). **O que prende, assusta ou amaldiçoa:** a **Firmeza** = 22 + Vontade ÷ 20 + a maior maestria ÷ 2 + bônus do amuleto |
| quanto tira | dado × 4 × valor da arma ÷ proteção da parte, vezes a força | dado × 4 × valor do foco ÷ **guarda**, vezes 1 + 0,03 por ponto de bônus de Afinidade |
| a proteção | a armadura, parte por parte, com o material | a **guarda**: o valor da categoria do amuleto. Sem amuleto, a armadura do tronco **um degrau abaixo** (sem armadura: um degrau abaixo do Comum). Não olha material nem parte do corpo |
| crítico e dois 1 | dados em dobro, proteção pela metade; dois 1 gastam a arma | iguais; dois 1 é o **erro da tradição** (3.4) |
| o tempo e o lugar | chuva, escuro, cobertura, alguém no caminho | o feitiço que voa segue as regras do tiro |

- **Mana** = (Afinidade + Vontade) ÷ 5. O aprendiz de mago tem 27; o mago de nível 50, 32.
- **Custa** 2 × o círculo + 1 de Mana: 3, 5, 7, 9. **Volta 1 no começo de cada turno de quem lança,** na luta (decisão do jogador). Fora da luta, pela fonte da tradição (3.4).
- **O círculo** que a pessoa alcança é a maestria ÷ 2: Iniciante o 1º, Treinado o 2º, Mestre o 3º, Lendário o 4º.
- **O tempo de lançar** está em cada feitiço: 1 ação ou 2 (a rodada inteira). O esforço (a ação a mais) segue só para golpear.
- **O que interrompe:**
  - lançar (ou beber poção) com inimigo colado dá a UM deles um golpe livre, que gasta a reação dele;
  - se esse golpe fere e o feitiço é de 2 ações, quem lança testa 2d20 + bônus de Vontade + maestria contra 26: falhou, perde o feitiço e a Mana (medido: cortado em 47 de 92);
  - quem vai ao chão perde o feitiço.
- **Aprender um feitiço:** 9 blocos de estudo por círculo, com quem sabe ou com o escrito, e um teste no fim (2d20 + maestria + Afinidade ÷ 10 contra 24 + 4 por círculo). Falhou: mais 3 blocos. O feitiço sabido é uma marca da pessoa (`sabe`).

### 3.2 O foco e o amuleto (itens do Livro, com categoria, durabilidade e sintonia como qualquer peça)

| Peça | Mãos | O que tem de seu |
| --- | --- | --- |
| varinha | 1 | não apara; a outra mão fica livre para o escudo ou a adaga |
| cajado | 2 | o feitiço vale × 1,25; apara e bate como uma maça da categoria dele |
| símbolo (fé) | nenhuma: vai ao pescoço | é o foco do clérigo e conta como amuleto um degrau abaixo. Por isso o clérigo luta de maça e escudo |
| ramo vivo (verde) | 2 | um cajado de madeira; não perde durabilidade ao ar livre |
| fetiche (pacto) | 1 | feito de osso; guarda o pertence da vítima |
| amuleto | pescoço (uso novo: `amuleto`) | apara feitiço (o bônus da categoria) e é a guarda (o valor da categoria) |

- Sem foco lança-se com as mãos: um degrau abaixo do Comum, e −4.
- O amuleto gasta 1 quando apara feitiço de foco de categoria maior, e 1 em todo crítico de feitiço. O foco gasta 1 no erro. Os dois gastam 1 pelo uso, no fim da luta.
- Foco e amuleto Épicos ou melhores ocupam lugar na sintonia. Quem tem Vontade alta sustenta mais: o mago de nível 50 (Vontade 77) sustenta três; o guerreiro (55), duas.

### 3.3 O que medi contra a luta de hoje (nível 50, tudo Raro, amuleto Raro dos dois lados, salvo dito)

| O que se mede | Medido |
| --- | --- |
| guerreiro × guerreiro (a régua) · arqueiro × guerreiro, de longe e de perto | 52% · 37% e 23% |
| mago × mago | 50 a 52%; a Mana seca na rodada 7 em metade das lutas |
| **mago de cajado × guerreiro:** longe · perto · colado | **50 a 59% · 35 a 38% · 23 a 28%** |
| mago de varinha × guerreiro: longe · perto · colado | 34 a 36% · 16% · 10% (com varinha e escudo, de longe: 44%) |
| o mago só com a faísca, de longe | 10 a 14%: sem a geada, que prende quem vem, ele é um arqueiro pior |
| **mago × guerreiro SEM amuleto:** longe · perto | **99% · 76%** (com o amuleto um degrau abaixo: 95%) |
| se a armadura valesse inteira contra magia (a outra opção da pergunta 1): longe · perto | 75% · 44% |
| mago com o foco uma categoria acima × guerreiro: longe · perto | 96% · 69% |
| mago × guerreiro só com o AMULETO uma acima | 1%: cada feitiço tira 3% do PV |
| nível 50 com o foco duas acima × nível 500: longe · perto | 87% · 42% (o aço, no banco: 63%) |
| nível 50 com o foco uma acima × nível 500, de longe | 18% (o aço: 8%) |
| mago 50 × guerreiro 150 · mago 150 × guerreiro 50 | 16% · 70% |
| o dano de um feitiço que pega num igual | a mediana é 11 a 14% do PV (um golpe de espada: 11,5%); a lança de fogo, 25%, e abre ferida metade das vezes |
| a Mana, lançando sem parar | seca entre a rodada 6 e a 7; daí em diante, uma faísca a cada três rodadas |
| o erro (dois 1) | 0,25% dos lances |
| **mago de cajado × arqueiro, de longe** | **18 a 21%** (de varinha: 8%) |
| 3 guerreiros e 1 mago com a área × 4 guerreiros com amuleto igual · um abaixo · sem amuleto | 34 a 38% · 78% · 88% (a régua: 50%) |
| mago Épico sozinho × 10 Incomuns · o guerreiro de conjunto Épico contra os mesmos | 81 a 83% · 61 a 70% |
| 4 guerreiros e 1 clérigo × 5 guerreiros (a régua: 44 a 53%) | 36% (a cura devolve 24% do PV, 3 a 4 vezes por luta) |
| três salas seguidas (5 Raros contra 3 ondas de 6): 5 guerreiros · com o clérigo · com o mago | 58% · **65%** · 50%; com o clérigo morrem 2,0 da casa, sem ele 2,4 |
| o símbolo um degrau abaixo do que feriu | a cura cai de 24% para 8% do PV |
| **o mago de começo** (nível 5, varinha Comum, faísca e escudo) × o guerreiro de começo sem amuleto: longe · perto | 84% · 53% |
| o mesmo, com o guerreiro de amuleto Comum (10 de prata) | 29% |
| o mago de começo × a corça · o javali · 3 lobos | 89% · 10% · 0% (o guerreiro de começo × o javali: 68%) |
| se o esforço valesse para feitiço de 1 ação (pela Mana em dobro): cajado, longe · perto · colado | 66% · 47% · 38% (é a pergunta 4) |

**Como ler.** De longe o mago de cajado é moeda no ar contra o aço; de perto o aço manda. Quem decide é o amuleto do outro: contra gente sem amuleto o mago é uma arma uma categoria acima. O arqueiro é o terror do mago: três flechas por rodada, sem Mana. Sozinho no mato o mago morre (o javali chega nele). No grupo ele vale pelo que o outro lado NÃO tem. Triângulo: o guerreiro vence o arqueiro, o arqueiro vence o mago, o mago de longe empata com o guerreiro e esmaga quem veio sem amuleto.

### 3.4 As tradições (uma Mana, quatro fontes)

| | **Arcano (o mago)** | **Fé (o clérigo)** | **Verde (o druida)** | **Pacto (a bruxa)** |
| --- | --- | --- | --- | --- |
| de onde vem o poder | estudo | um santuário e um voto | a terra viva | um pacto, sangue e nomes |
| foco | varinha, cajado | símbolo | ramo vivo | fetiche |
| a Mana volta | com o sono (toda); 10% por bloco acordado | só rezando: 1 bloco no santuário, toda; 1 bloco de reza em outro lugar, metade, uma vez por dia | só ao ar livre: 25% por bloco no ermo; toda, dormindo no mato. Na vila, nada | como o mago. E com sangue: 5% do PV máximo dão 3 de Mana na hora |
| faz melhor | ferir de longe, a área, prender, o escudo | curar, estancar, abençoar, quebrar maldição, ferir o que é torto | prender, mudar o chão e o céu, mandar em bicho, curar devagar | amaldiçoar, enfraquecer, assustar, ler, desatar |
| não faz | curar; quebrar maldição | ferir gente viva de longe; área | nada sob teto de pedra (corredor, ruína, cidade: −4); fogo | curar os outros; proteger; área |
| o que custa | livro e mestre (aprender é caro) | o **dízimo** (um décimo do que ganhou desde a última reza vai para o santuário) e o **gume** (com arma de corte ou ponta na mão, a Mana não volta) | o **ferro**: de malha ou placa, −4 na Conjuração. E dormir no mato | o **sangue** (PV), o **pertence** (para atar de longe) e a **fama**: a vila sabe quem ela é |
| quando dá errado (dois 1) | **retrochoque:** vai ao chão e perde 1 ação | **o céu se cala:** a Mana vai a zero até a próxima reza | **a terra cobra:** fôlego a zero e 2 de cansaço | **volta nela:** leva o próprio feitiço (a maldição, um grau abaixo) |
| como se treina | blocos de estudo (leves), com livro ou mestre | blocos de serviço no santuário (é o jornal dele) | blocos de vigília no ermo (e o acaso rola: bicho aparece) | blocos de vigília de noite, com o fetiche |

- Qualquer pessoa aprende qualquer uma, e mais de uma. A Mana é uma só, e volta pela regra da tradição em que a pessoa tem a maior mão. O custo de uma tradição vale sempre que se usa feitiço dela.
- **Cabe a quarta, e é a bruxaria:** a maldição precisa de dono no mundo. A "alquimia de guerra" não é tradição: são duas receitas (o veneno de lâmina e o frasco de fogo, 4.2). O canto fica de fora: o que ele daria (coragem) está na bênção.

### 3.5 A lista de partida (20 feitiços; `tabelas_magia.py`)

```python
K_CURA = 6                  # a cura: dado × isto × valor do foco ÷ valor da FERIDA FUNDA (a maior categoria que feriu a pessoa desde que ficou inteira)
MANA = lambda circ: 2 * circ + 1
# circ · ações · alcance em casas · contra · o que faz
FEITICOS = {
 # ARCANO
 'faisca':    dict(trad='arcano', circ=1, acoes=1, alc=8, contra='defesa',  dado='1d8'),
 'escudo':    dict(trad='arcano', circ=1, acoes=1, alvo='si', dura=3, poe='escudo'),          # um escudo da categoria do foco (4 + o bônus), contra aço, tiro e feitiço
 'geada':     dict(trad='arcano', circ=2, acoes=1, alc=6, contra='firmeza', dado='1d4', poe=('preso', 1)),
 'lanca':     dict(trad='arcano', circ=2, acoes=2, alc=8, contra='defesa',  dado='2d8'),
 'flor':      dict(trad='arcano', circ=3, acoes=2, alc=8, contra='defesa',  dado='1d6', area=4),   # até 4 da mesma casa, amigo e inimigo
 # FÉ
 'estancar':  dict(trad='fé', circ=1, acoes=1, alc=1, tira='sangra', estabiliza=True),
 'bencao':    dict(trad='fé', circ=1, acoes=1, alvo='casa', dura=5, coragem=4, firmeza=2, tira='abalado'),
 'cura':      dict(trad='fé', circ=2, acoes=1, alc=2, cura='2d6'),
 'luz':       dict(trad='fé', circ=2, acoes=1, alc=6, contra='defesa', dado='1d10', so=('morto', 'amaldiçoado')),
 'quebrar':   dict(trad='fé', circ='grau+1', blocos=1, alc=1, contra='maldição'),              # fora da luta (5.4)
 # VERDE
 'raizes':    dict(trad='verde', circ=1, acoes=1, alc=6, contra='firmeza', poe=('preso', 2), chao='terra'),
 'voz':       dict(trad='verde', circ=1, acoes=1, alc=8, contra='firmeza', so=('bicho',), moral=26),   # o bicho testa a coragem; fora da luta, o que viu o druida não investe
 'lama':      dict(trad='verde', circ=2, acoes=2, alvo='campo', poe_campo='lama', sustenta=1),
 'nevoa':     dict(trad='verde', circ=2, acoes=2, alvo='campo', poe_campo='neblina', sustenta=1),
 'seiva':     dict(trad='verde', circ=2, acoes=1, alc=1, regenera=0.05, dura=4),
 # PACTO
 'quebranto': dict(trad='pacto', circ=1, acoes=1, alc=6, contra='firmeza', poe=('quebranto', 3)),   # −2 no acerto e na Defesa
 'olho':      dict(trad='pacto', circ=1, blocos=1, le=('maldição', 'encanto', 'dom')),         # fora da luta: 2d20 + Conjuração contra 24 + 4 por grau
 'medo':      dict(trad='pacto', circ=2, acoes=1, alc=6, contra='firmeza', moral=26),
 'dreno':     dict(trad='pacto', circ=2, acoes=1, alc=4, contra='defesa', dado='1d6', volta=0.5),
 'atar':      dict(trad='pacto', circ='grau+1', acoes=2, alc=6, contra='firmeza', maldicao=True),   # com o pertence: 1 bloco, de qualquer distância
}
ESTADOS = dict(preso='não anda; −2 na Defesa', quebranto='−2 no acerto e na Defesa', escudo='Defesa + 4 + bônus do foco')
CALEJO = 4                  # cada feitiço que prende ou enfraquece deixa o alvo com isto a mais de Firmeza até o fim da luta
```

Medidos em rascunho: faísca, escudo, geada, lança, flor e cura. Os outros catorze são chute até o banco. A lama e a névoa mexem no campo com os estados de tempo que a luta já roda (`lama`, `neblina`).

### 3.6 Os bichos com magia

- **O que os traços de hoje já fazem:** o `veneno` passa a ter a categoria do corpo (é o que o antídoto olha); o `sopro` segue contra a armadura, porque é fogo e não feitiço; o `apavora` é teste de coragem, e a bênção ajuda; o `regenera` não muda.
- **A ficha:** a guarda do bicho é o valor da categoria do corpo. A Firmeza é 22 + Vontade ÷ 20 + instinto ÷ 2 + bônus da categoria. O corpo apara feitiço como apara aço.
- **Quatro traços novos** (a lista fechada passa de 10 a 14):

| Traço | O que faz |
| --- | --- |
| resiste | a guarda contra magia vale um degrau a mais |
| sem_corpo | arma sem encanto vale um degrau abaixo nele; a luz e a água benta valem inteiras |
| amaldiçoa | o golpe do corpo que fere faz a vítima testar a Firmeza: falhou, pega a maldição da espécie no passo 1, com o grau da categoria do corpo |
| lança | a cada 2 rodadas solta um feitiço da tabela, sem Mana (como o sopro) |

- **Três espécies novas, e duas que mudam:**

| Espécie | Grau | Onde | O corpo e os traços |
| --- | --- | --- | --- |
| fogo-fátuo | F, Comum | brejo, ruína, floresta, só de noite | pequeno; `voa`, `lança` (quebranto), `resiste`. Rende 1 de osso Comum |
| morto-que-anda | D, Incomum | ruína, caverna | médio; garra, pelo; `amaldiçoa` (chaga); não testa a coragem; o veneno não pega nele |
| assombro | C, Raro | ruína | médio; `sem_corpo`, `amaldiçoa` (míngua), `apavora` |
| hidra e dragão | | | ganham `resiste`. As provas de hoje não mudam: nenhuma tem mago |

### 3.7 Como a luta para e pergunta com magia em campo

Paradas novas, além das de hoje:
- alguém do outro lado começou um feitiço de 2 ações (dá tempo de cortar: é a hora de mandar bater nele);
- quem o jogador comanda ficou com um quarto da Mana, ou sem Mana;
- quem o jogador comanda foi preso, enfraquecido, amaldiçoado ou perdeu o feitiço;
- o erro de alguém da casa;
- alguém da casa caiu ou passou de um quarto do PV e há na casa quem cure ou tenha poção.

Ordens novas: `lancar FEITICO [alvo]` · `beber BEM` · `usar ITEM [alvo]` (o encanto) · `curar NOME`. O quadro ganha a Mana de cada um e os estados com prazo.
Quem o jogador comanda nunca foge pelo dado: o `medo` nele vira "fraqueja", e a luta para. Quem não é comandado lança por uma regra curta e escrita (`magia.escolhe`): prende quem vem, cura quem está abaixo de metade, afasta-se de quem colou, ergue o escudo contra tiro.

### 3.8 Uma cena na vila de teste

O personagem é Ilan, o aprendiz de mago (o começo novo `comeco=mago`): nível 5, arcano Iniciante, varinha, couro e amuleto Comuns, Mana 27, sabe a faísca e o escudo. `python3 caca.py sair alvo=javali com=tome` e, achado o rastro, `python3 caca.py atacar inicio=longe vantagem=alto`. A ameaça já veio lida: "javali, grau E, Comum. A sua varinha é Comum: o feitiço passa inteiro."

`python3 caca.py luta "Ilan: lancar faisca javali" "grupo: segurar"`. Rodada 1: o javali vem; Ilan gasta 6 de Mana em duas faíscas (2d20 + 7,25 do alto contra 27,5): uma erra, a outra tira 22 dos 202 do javali. Rodada 2: o javali corre e investe em Tomé, que segura a frente. A luta para: "Tomé foi ao chão · o javali está a 2 casas de Ilan".

`"Ilan: lancar faisca"` por mais duas rodadas. Nova parada: "Ilan está com 6 de Mana (um quarto)". Em quatro rodadas foram 8 faíscas, 4 acertos e 87 de PV: nem metade do bicho. Quem o mata é a lança Incomum de Tomé, que vale o triplo naquele couro. Medido: esse mago, sozinho, vence o javali em 10% das vezes. A magia abre e escolhe; o aço fecha.

### 3.9 O que isto quer dizer para o mundo

O valor de um mago depende de quantos amuletos o outro lado tem. Um bando de estrada sem amuleto é presa de um aprendiz. Uma guarda de cidade com amuleto um degrau abaixo ainda perde (78%). Rivais e Lendas vivas andam de amuleto: contra eles o mago é um a mais, e não o dono da luta. Por isso o amuleto vira a peça que todo mundo quer, e o encantador e o ourives têm serviço.

## 4. C. As poções e a alquimia

### 4.1 O ofício (no molde da forja)

- **A botica** é a oficina da alquimia: `lugar.botica`, de 0 a 4 (panela, botica de vila, botica de cidade, laboratório, grande laboratório). Soma no teste.
- **A fornada** é a obra: a matéria entra quando abre, 3^categoria blocos pesados de bancada (1, 3, 9; a Épica, 27), e um teste no fim: **2d20 + maestria de alquimia + Afinidade ÷ 10 + botica + preparo contra 28 + 6 por categoria.** O preparo são os quatro de hoje com outros nomes (receita e ajudante, da pessoa; alambique e vidraria, do lugar).
- **Rende 3 doses.** Falhar por 1 a 4: sai **aguada**, 1 dose. Por 5 ou mais: a matéria some. Por 10 ou mais numa fornada Incomum ou melhor: a fumaça, −2 em tudo até dormir.
- **A maestria** sobe por blocos de bancada, pela tabela do ofício (50, 150, 375, 1.000). O feito de Mestre é um elixir Épico; o de Lendário, um Único.
- **Do Comum ao Raro, a dose é um BEM** (`cura:0`, `antídoto:1`): vai na carga, tem estoque e preço pelo estoque, e o povo a gasta. **Do Épico para cima é o elixir, um ITEM do Livro** (tipo `elixir`): leva um núcleo da categoria, é contado e não tem loja. É o mesmo corte da matéria e do núcleo.

```python
# tabelas_alquimia.py
DOSES = 3; AGUADA = 1
BASE_POCAO = {'cura': 10, 'antídoto': 8, 'desate': 12, 'veneno': 15, 'fogo': 12}     # a dose Comum; vezes 6 por categoria (como a matéria)
SEM_CATEGORIA = {'água-de-lua': 10, 'água benta': 3}                                 # bens sem categoria, como o remédio (8, que já existe)
CONSUMO_POCAO = {'cura': 0.002, 'antídoto': 0.001, 'desate': 0.0005, 'água-de-lua': 0.0005}   # por cabeça, por dia: a vila de 400 gasta 0,8 dose de cura por dia; o alvo da loja são 24
RECEITAS = {                # o que entra numa fornada, na categoria dela
    'remédio':     {'erva': 6},
    'cura':        {'erva': 6},
    'antídoto':    {'erva': 4, 'osso': 2},        # do Incomum para cima, mais 1 de peçonha da categoria
    'água-de-lua': {'erva': 6, 'sal': 1},
    'desate':      {'erva': 6, 'sal': 2, 'osso': 1},
    'veneno':      {'peçonha': 3},                # só Incomum e Raro: é o que há de peçonha
    'fogo':        {'carvão': 6, 'erva': 3},      # só Incomum e Raro
}
DOSES_DIA = lambda vigor: max(2, vigor // 20)
ENJOO = (24, 4)             # passou das doses do dia: Vigor contra 24 + 4 por dose a mais, ou a poção não vale e fica −2 em tudo até dormir
BOTICA_PRODUZ = {1: 0, 2: 1, 3: 2}      # a botica do lugar faz poção até esta categoria (a de vila, só Comum)
```

### 4.2 O que cada poção faz

| Poção | O que faz | A categoria |
| --- | --- | --- |
| remédio | com quem tem mão de cura, a ferida passa a contar o repouso em dobro (7 dias viram 4; 21 viram 11) | não tem |
| **cura** | devolve **2d6 × 6 × valor da poção ÷ valor da ferida funda**, e estanca o sangue | da categoria do que feriu: 42 de PV, um quarto. Uma acima: o triplo. Uma abaixo: um terço. Duas abaixo: quase nada |
| antídoto | acaba o veneno da categoria dele ou menor; uma abaixo, o veneno passa a tirar um terço. Bebido até 1 bloco antes, o veneno não pega | o veneno do bicho tem a categoria do corpo: a surucucu pede antídoto Incomum |
| água-de-lua | devolve 8 de Mana | não tem |
| desate | a maldição de grau igual ou menor não testa por 3 dias. Não quebra | o grau da maldição |
| veneno de lâmina | passado na arma (dura 1 bloco), o primeiro golpe que fere envenena como o traço `veneno`. Só pega em arma da categoria dele ou menor | a da arma |
| frasco de fogo | arremessado a 4 casas: 1d6 × o valor da categoria em até 4 de uma casa; não se apara | vale contra a armadura, como o sopro |
| elixir (Épico para cima) | o mesmo que a de cura ou o antídoto, na categoria dele; é item, com janela | 1 núcleo por fornada de 3 |

- **A ferida funda** é a maior categoria que feriu a pessoa desde que ela ficou inteira. Fica escrita na pessoa (`funda`) e se apaga quando o PV enche. É o que faz a poção barata não servir a quem apanhou de aço caro, e é a mesma conta da cura do clérigo.
- **Quantas se bebem:** Vigor ÷ 20 doses por dia (no mínimo 2; Vigor 70 dá 3). Passou disso, o teste de enjoo. O elixir conta como duas.
- **Na luta:** beber é 1 ação, e quem está colado ganha o golpe livre. Passar veneno na arma não se faz em luta.
- **Quanto dura:** a de cura, o antídoto e a água-de-lua são na hora; o veneno na lâmina, 1 bloco; o desate, 3 dias. A poção guardada não estraga nesta etapa (a comida também não).

### 4.3 Preço, e a meta que impede a mina

A fornada de cura Comum: 6 de erva (12 de prata na base) viram 3 doses (30 na base). Na loja as três rendem 17 e a erva custa 14: quem compra a erva na loja ganha 3 quando acerta e perde 14 quando erra. Cada fornada vendida baixa o preço da dose uns 6% (o alvo da loja são 24 doses).

| O que se mede (30 vidas por linha, com os robôs dos bancos e o mercado de verdade) | Meta | Medido |
| --- | --- | --- |
| **o alquimista de loja:** o personagem de começo da vila de teste, com mão de Iniciante e 9 de erva, compra a erva na loja, destila o que mais rende e vende à loja | nos 5 primeiros dias, em média no máximo 6 de prata por dia e no pior caso 12; do Dia 6 ao 30, no máximo 4 (as metas do ferreiro de loja) | 3,9 a 4,7 por dia nos 5 primeiros dias (o pior caso, 5,6); do Dia 6 ao 30, entre −0,04 e 0,05. A prata fecha. No bolso, com a jornada: +6,6 a +7,6 e depois +3,0 por dia |
| o mesmo, sem erva de começo | o mesmo | 0,2 por dia, e nada depois |
| **o ervateiro:** o coletor de começo do banco colhe erva na borda da floresta, destila cura e vende | de 1,0 a 2,0 diárias por dia ao preço de base (a meta K1 da coleta) | 1,15 diária; na loja, 2,4 de prata por dia; **no bolso, −0,5 por dia**; sai ferido ou morto em 0,3 a 0,8% das saídas |
| o ervateiro que vende a erva crua (hoje) | não tem meta | 0,73 a 0,77 diária; no bolso, −1,0 por dia |
| o ervateiro que destila remédio | de 1,0 a 2,0 | 0,88 a 0,99: abaixo da faixa |
| com a receita de 9 de erva por fornada (a primeira que tentei) | | o alquimista de loja: 2,8 por dia e zero depois; o ervateiro: 0,67 diária. Por isso a receita ficou em 6 |
| 2 poções de cura da categoria do aço, num duelo entre iguais (bebe abaixo de 40% do PV) | 52 a 65% | 59%, com a dose devolvendo 24% do PV. Medido antes, com a dose em 16%: 51 a 57%; uma categoria abaixo, 48%; uma acima, 63%; cinco poções, 54% (beber custa ação e golpe livre) |
| o veneno de lâmina da categoria da arma, num duelo entre iguais | 58 a 72% | 64% com um golpe por dose (com três golpes por dose: 69 a 71%); o veneno um degrau abaixo da arma não pega: 47% |

**Por que não vira mina:** comprar custa 10% a mais e a loja paga 60%; o alvo da loja é pequeno (24 doses), e o preço cede depressa; o povo gasta pouco (0,8 por dia) e a botica da vila já faz isso. O ganho é o da primeira fornada, como a alabarda do ferreiro de loja.
**O que a medida mostra de incômodo:** a erva rende 1 por bloco e a lenha 2, pelo mesmo preço (tabela de hoje). Quem vive só de colher erva e destilar perde meia prata por dia. A botica se sustenta com o jornal (4.4), como a forja. É a pergunta 6.
**O veneno Raro custa caro de propósito:** 3 de peçonha Rara (três aranhas-de-toca, bicho de grau C) por fornada de 3 doses; a dose vale 540 de prata na base, meia espada Rara por luta. Um antídoto da categoria (1 ação) o acaba.

### 4.4 O que a curandeira faz (o ofício `cura`, que hoje só tem o nome)

- **Tratar:** 1 bloco e 1 remédio; a ferida do tratado passa a contar repouso em dobro. Sem teste, como o conserto. Pede mão de Iniciante (ferida) ou de Treinado (ferida grave).
- **Distinguir:** a Treinada diz se é doença ou maldição (Percepção contra 24). Não diz qual.
- **O jornal da botica** (e o do santuário) paga pelo que a mão vale, **dentro da mesma jornada de 2 blocos pagos por dia** que já vale para trabalhar e para o jornal da forja. Por construção, serviço de magia rende o que rende a forja: aprendiz 6, oficial 12, mestre 20 de prata por dia. Nenhuma renda nova.

### 4.5 Uma cena na vila de teste

Lia começa como boticária (`comeco=boticario`: alquimia e coleta de Iniciante, 6 de erva, 30 de prata). `python3 alquimia.py pede cura Comum` responde: "6 de erva Comum (você tem 6) · 1 bloco pesado · 2d20 + 15 (mão 2, Afinidade 6, botica 1, preparo 6) contra 28: acerta 83% · sai aguada 10% · perde tudo 7%." `python3 alquimia.py destilar cura Comum`: 31 contra 28, saem 3 doses.

`python3 mercado.py vender cura:0 3`: a loja paga 17 de prata, e a dose cai de 10,0 para 9,4. `python3 mercado.py comprar erva:0 6` custa 14. A segunda fornada falha por 2: sai aguada, 1 dose, 5 de prata. Em dois blocos Lia ganhou 22 e gastou 14. A terceira já não paga a erva, e a mesa diz. Lia serve o jornal da botica da Nara: `python3 alquimia.py jornal 2`, 6 de prata.

De tarde Maro volta da mata com 60 de 141 de PV, mordido por lobo (Incomum). `python3 alquimia.py beber cura:0`: "a ferida funda é Incomum, a poção é Comum: vale um terço. +14 de PV." Com a Incomum, que só a cidade vende por 66, seriam 42.

## 5. D. As maldições

### 5.1 O que é

Um mal que fica. Tem **tipo** (lista fechada de cinco), **grau** (uma categoria, de Comum a Lendário: a do foco, do bicho, do lugar ou da peça que a pôs), **passo** (de 1 a 6, como o relógio das frentes), **dono** (de onde veio) e **condição** (o que a quebra). Mora na pessoa (`pessoa.maldicoes`), na peça (`item.maldicao`) ou no lugar (`lugar.maldicao`).

**O teste do dia.** A cada virada do dia, pelo dado do mundo (`estado.sorte`: mesma semente, mesma sorte; nunca se rola de novo):
**2d20 + Vontade ÷ 10 + bônus do amuleto (sem amuleto: −4) contra 22 + bônus do grau.**
- Falhou: um passo a mais. Passou por 10 ou mais: um passo a menos (nunca abaixo de 1, salvo as que saem sozinhas).
- No passo 6 vem o desfecho. O ato longo (dormir, forjar 70 dias) **para** quando o passo sobe, como para quando o corpo cruza um limiar.

```python
# tabelas_maldicao.py: cada tipo mexe em coisa que o motor já tem
MALDICOES = {
 'míngua':  dict(mata=True,  por_passo=dict(pv_max=-0.08), trava='cura_da_noite', sinal='acorda mais fraco do que deitou'),
 'chaga':   dict(mata=True,  por_passo=dict(pv_dia=-0.03), trava='repouso',       sinal='a ferida não fecha'),
 'azar':    dict(mata=False, sai_sozinha=True, pena=[0, -1, -1, -2, -2, -3],      sinal='tudo sai torto'),
 'insônia': dict(mata=False, sai_sozinha=True, sono_menos=[0, 1, 1, 2, 2, 3],     sinal='não descansa nem dormindo'),
 'marca':   dict(mata=False, loja=-0.10, ninguem_vai_junto=True, bicho_investe=0.2, sinal='desviam os olhos'),
}
TESTE_BASE = 22; SEM_AMULETO = -4; RECUA = 10; PASSOS = 6
QUEBRAR = (26, 2)           # o clérigo: 2d20 + Conjuração contra 26 + bônus do grau + 2 por passo
DONATIVO = lambda grau: 10 * 6 ** grau
```

No passo 6: a míngua e a chaga matam. O azar e a insônia ficam como estão até alguém quebrar (a insônia deixa a pessoa em sono 8 para sempre, e o corpo cobra). A marca fica até a condição se cumprir.

### 5.2 De onde vem

| Origem | Como pega | Grau |
| --- | --- | --- |
| feitiço | a bruxa: `atar`, contra a Firmeza, à vista; ou de qualquer distância, com um pertence da vítima | a categoria do fetiche |
| bicho | o traço `amaldiçoa`: o golpe que fere, se a vítima falha a Firmeza | a categoria do corpo |
| lugar | `lugar.maldicao`: quem passa um bloco ali testa como no teste do dia. Falhou, pega | o do lugar |
| peça amaldiçoada | ao vestir, e a cada virada enquanto vestir: testa a Firmeza; falhou, pega. Pega, a peça não sai mais do uso enquanto a maldição durar | a categoria da peça |
| juramento quebrado | o Mestre registra o juramento (`marca.juramento`: a quem, o quê, diante de que santuário) e, quebrado, a marca | o do santuário |

### 5.3 Quanto tempo dá (a conta exata do dado do motor, 2d20 em que o 20 rola de novo)

| A vítima (Vontade 50) | O dado precisa de | Falha por dia | Chega ao passo 6 em média em | 1 em 10 já chegou no dia | Metade | 9 em 10 |
| --- | --- | --- | --- | --- | --- | --- |
| amuleto um grau ACIMA da maldição | 13 | 16% | só 4 em 10 chegam, em 400 dias | 40 | 179 | |
| amuleto do grau da maldição | 17 | 30% | 48 dias | 13 | 36 | 97 |
| **sem amuleto, maldição Comum** (ou amuleto um grau abaixo) | 21 | 47% | **15 dias** | 7 | 13 | 25 |
| sem amuleto, maldição Incomum | 25 | 64% | 9 dias | 5 | 8 | 13 |
| sem amuleto, maldição Rara | 29 | 77% | 7 dias | 5 | 6 | 9 |
| sem amuleto, maldição Épica ou maior | 33 | 87% | 6 dias | 5 | 6 | 8 |

Nunca menos de 5 dias: um passo por dia. Cada grau de diferença entre o amuleto e a maldição muda o prazo de semanas para meses, ou de semanas para dias. As que saem sozinhas (o azar, a insônia): com amuleto do grau, saem em 82% dos casos; sem amuleto, em 37%.

### 5.4 Como se quebra

| Caminho | Como | Custo |
| --- | --- | --- |
| cumprir a condição | cada maldição nasce com uma, de um molde fechado por origem: devolver a peça ao lugar de onde saiu · matar o bicho que mordeu (um da espécie, naquele ermo) · o perdão de quem recebeu o juramento, ou cumprir o jurado · queimar o pertence que a bruxa guarda | uma cena, ou uma caçada |
| o clérigo | `quebrar`: 1 bloco, no santuário, 2d20 + Conjuração contra 26 + bônus do grau + 2 por passo. Uma tentativa por dia. Falhou por 5 ou mais: ele também pega, no passo 1 | o donativo: 10, 60, 360, 2.160 |
| quem pôs | a bruxa desata sem teste. Morta ela, quebra | o que ela pedir; ou a vida dela |
| a poção | o desate do grau suspende o teste por 3 dias; a água benta dá +4 no teste de hoje | 14 de prata na Comum: compra tempo |
| o lugar | 1 bloco de rito no lugar, com 3 de sal e 3 de água benta, e o teste do clérigo contra o grau do lugar | limpa o lugar para todos |

A chance do clérigo (conta exata; Treinado, símbolo do grau da maldição): no passo 1, 53%; no passo 3, 36%; no passo 5, 23%. Com o símbolo um grau acima: 70%, 53% e 36%. **Quem chega cedo se salva.** O Mestre de fé acerta 62% no passo 1.

### 5.5 Como fica guardada, e como a MESA mostra

- **No estado:** `pessoa.maldicoes = [{tipo, grau, passo, dia, de, condicao, sabe, suspensa_ate}]`. Verbos novos do gravador: `['maldicao', id, 'poe', registro]` · `['maldicao', id, indice, 'passo', +1 ou −1]` · `['maldicao', id, indice, 'quebra']` · `['maldicao', id, indice, campo, 'poe', valor]`. Na peça e no lugar, pelo `poe` de sempre.
- **Invariantes:** tipo na tabela; grau de 0 a 7; passo de 1 a 6; morto não tem maldição ativa (ela fica escrita na morte dele, e a peça amaldiçoada cai com o corpo, ainda amaldiçoada); peça amaldiçoada em uso tem dono com a maldição dela.
- **A MESA mostra o que o personagem sabe,** em três degraus:
  1. **não sabe** (passo 1): nada na parte pública. O teste do dia sai como "rolagem oculta";
  2. **desconfia** (do passo 2 em diante): o sinal, em palavras. "Maro acorda mais fraco do que deitou. Isto não é doença." Sem tipo, sem grau, sem prazo;
  3. **sabe** (alguém leu): "MALDIÇÃO: míngua, grau Incomum, passo 3 de 6 · PV máximo −24% · testa a cada virada: 2d20 + 1 contra 26 · quebra: devolver a espada à Cova Velha, ou o santuário (60 de prata)".
- **No SÓ O MESTRE,** sempre tudo: tipo, grau, passo, dono, condição e a rolagem do dia. O `RETOMAR.md` leva a linha de cada passo que subiu.

### 5.6 Uma cena na vila de teste

Na Cova Velha (a ruína pequena que a vila de teste ganha, 7.1) há uma espada Incomum no chão, junto de ossos. `python3 caca.py sair cova blocos=2`, o rastro acha a peça, e o Mestre a passa para Maro por evento. `python3 ato.py vestir i0031`: a ficha salta (acerto +4, o golpe vale o triplo). Na parte do Mestre: "i0031 está amaldiçoada (míngua, Incomum). Maro falhou a Firmeza: passo 1." Na mesa, nada.

Maro dorme. Na virada: "rolagem oculta". No terceiro dia `python3 ato.py dormir 3` para no meio: "PAROU: Maro acorda mais fraco do que deitou. Isto não é doença." O PV máximo caiu de 141 para 118. `python3 ato.py tirar i0031` é recusado: "a mão não larga a espada."

`python3 maldicao.py ler com=zuza` custa 5 de prata e um teste dela (oculto). Passou: a mesa agora diz tudo. Sem amuleto, contra o grau Incomum, Maro precisa de 25 no dado: falha em 64% dos dias e tem cerca de 9 dias no total. Três saídas: levar a espada de volta à Cova (2 blocos de ida, e o assombro mora lá); a Irmã Celina (60 de prata que ele não tem; Treinada, símbolo Incomum, no passo 2: 44% por tentativa); ou comprar um amuleto Comum por 10 e um desate por 14 para ganhar uma semana enquanto junta a prata.

## 6. E. A peça encantada

- **Encantar é ofício de bancada, feito por quem lança.** Pede: a peça; quem sabe o feitiço (ou o efeito); um **catalisador** da categoria da peça (do Comum ao Raro, 3 de osso dessa categoria; do Épico para cima, um núcleo); uma oficina; 3^categoria blocos. O teste é o da forja, com a maestria da TRADIÇÃO no lugar da do ofício: 2d20 + maestria + Afinidade ÷ 10 + oficina + preparo contra 28 + 6 por categoria.
- **Falhar custa:** por 1 a 4, não pega e o catalisador some. Por 5 ou mais, a peça perde 5 de durabilidade. **Por 10 ou mais, ou com dois 1, a peça sai amaldiçoada** (a marca, no grau da peça). É de onde vêm as peças amaldiçoadas do mundo.
- **Um encanto por peça; dois do Único para cima.** Há dois tipos:
  - **passivo:** um efeito da lista de hoje (2.11). Hoje eles não têm origem; passam a nascer assim. Cada tradição grava os seus: o arcano, `critico_19` e `leve`; a fé, `firme` e `nao_quebra`; o verde, `devolve` (espinho); o pacto, `sangra` e `derruba`;
  - **ativo:** um feitiço da lista de quem grava. O dono solta com as ações do feitiço, **sem Mana, uma vez por luta**, pela ordem `usar ITEM`. A peça vale como foco **um degrau abaixo** da categoria dela, e a Conjuração usa o grau de quem gravou (2 por grau de maestria).
- **Sintonia:** toda peça com encanto ATIVO ocupa um lugar (Vontade ÷ 20), de qualquer categoria. A que dorme não solta. O efeito passivo segue como hoje.

| O que rende na luta (medido; nível 50, tudo Raro, contra o gêmeo) | |
| --- | --- |
| espada com o encanto ativo de faísca · de lança de fogo · de geada | 46% · 50% · 48%: **não decide** |
| a mesma lança de fogo contra o gêmeo SEM amuleto | 57% |
| conjunto Lendário com a área na espada × dez Raros de nível 275 (sem o encanto, no banco: 90 a 92%) | 86%: não ajuda; a espada já resolve |
| os passivos de hoje: `sangra` · `derruba` · `critico_19` · `devolve 12` (o teto do Raro) | 55% · 57% · 64% · 70% |

**Como fica dentro da lei.** O encanto ativo dá opção (prender de longe quem usa arco, um escudo para quem usa arma de duas mãos, uma cura de bolso), não vitória: contra um igual de amuleto, um degrau abaixo tira 3 a 8% do PV. O passivo vale de meio grau de maestria a quase dois, sempre longe dos 95% de uma categoria. O `devolve` no teto (70%) é o mais forte do motor de hoje: fica dito, e a meta nova o vigia.

**Uma cena na vila de teste.** Tomé quer o escudo `firme`, e quem grava esse efeito é a fé. `python3 encanto.py pede i0012 firme com=celina` responde: "escudo Comum · 1 bloco na forja · 3 de osso Comum · 2d20 + 13 (fé 4, Afinidade 6, forja 1, a receita dela 2) contra 28: pega 77% · não pega 12% · estraga 11%, e em 3 de cada 100 a peça sai amaldiçoada". O osso custa 4 de prata na loja, e a Irmã cobra 6 pelo bloco.

`python3 encanto.py gravar i0012 firme com=celina`: 30 contra 28, pegou. A janela do escudo ganha a linha "Efeitos: o dono não é derrubado · gravado por Celina, Dia 14". Na próxima caçada o javali investe em Tomé e ele fica de pé. Se a soma tivesse ficado em 18 ou menos (os dados dando 5 ou menos), o escudo sairia com a marca, grau Comum, e quem o embraçasse testaria a Firmeza contra 22.

## 7. F. A vila de teste, com magia

### 7.1 O que muda em Pedra Rasa e na mata

| O que entra | Números |
| --- | --- |
| a botica da Nara | `botica` 1; alambique e vidraria até o Comum. Nara passa a Treinada em cura e alquimia, com o dom "mão que fecha" |
| o santuário da Pedra do Poço | `santuario` 1. **Irmã Celina** (nova): nível 18, fé Treinada, símbolo Incomum; sabe estancar, bênção, cura, luz, e quebrar até o Incomum |
| **Zuza, a bruxa** (nova) | mora na borda da mata: nível 24, pacto Treinada, fetiche Incomum; sabe quebranto, olho, medo, atar. Ata e desata por prata |
| a prateleira do Lino | mais 3 amuletos Comuns e 1 Incomum, 1 varinha, 1 cajado e 1 símbolo Comuns (o alvo de peças sobe junto). Bens no alvo: 24 de cura, 12 de antídoto, 6 de água-de-lua, 6 de desate, 6 de água benta |
| os talentos dos oito | pelo dado do mundo, e três postos à mão: Rute, talentosa no tiro; Bento, jeitoso na forja; **Zeca, avesso à forja e prodígio do arcano (oculto)** |
| a Mata do Corvo | mais 4 surucucus (a peçonha Incomum) e 6 fogos-fátuos (só de noite) |
| **a Cova Velha** (novo ermo, a 2 blocos) | ruína de borda: ratazana 30, morto-que-anda 3, um assombro (posto à mão), erva Comum 30. O lugar tem a chaga, grau Comum. No chão, uma espada Incomum com a míngua |
| três começos novos | `boticario` (alquimia e coleta de Iniciante, 6 de erva) · `novico` (fé de Iniciante, símbolo Comum, estancar e bênção; serve no santuário) · `mago` (arcano de Iniciante, varinha e amuleto Comuns, faísca e escudo) |

O guerreiro Maro (o save do jogador, em `ensaio/`) não muda de ficha: ganha os talentos pelo dado, guerra à escolha do jogador, e segue sem amuleto até comprar um.

### 7.2 A mesa do Mestre ganha quatro blocos (cada módulo põe o seu, como hoje)

- **Você:** a linha da Mana, os feitiços que sabe, as doses de hoje, o talento já descoberto, o dom já visto, a maldição até onde sabe.
- **A botica e o santuário:** o que há para comprar e o que custa cada serviço; a conta da fornada.
- **Quem está aqui:** de cada nomeado, o que ele sabe fazer que se vê (a Irmã cura; Zuza lê).
- **SÓ O MESTRE:** os talentos e dons ocultos de quem está em cena, as maldições inteiras com a rolagem do dia, as peças amaldiçoadas, o que o lugar tem.

**Uma cena, para sentir a prateleira.** `python3 turno.py abre` traz: "Loja: amuleto Comum 10 · poção de cura 11 (há 24) · antídoto 9 · desate 14 · Santuário: cura 6 · quebrar maldição Comum 10". Maro tem 30 de prata. `python3 mercado.py comprar i0044` (o amuleto) e `python3 mercado.py comprar cura:0 1` levam 21.

`python3 ato.py vestir i0044` põe o amuleto no pescoço, e na ficha entra "Guarda contra magia: 1 (amuleto Comum)"; antes era um terço. Contra a faísca de um aprendiz, cada acerto passa a tirar 15% do PV dele, e não 46%: medido, o guerreiro de começo vai de 16% para 71% contra o mago de começo, de longe. É a melhor compra de 10 de prata que há em Pedra Rasa.

### 7.3 Os ganchos para as etapas seguintes

- **A região (3):** os santuários formam rede (o juramento vale de um para outro); a bruxa tem opinião contra ela e clientes de noite; veneno e maldição são crime com quem cobre; rota que passa por lugar amaldiçoado tem perigo a mais; encomenda de amuleto e de encanto é o primeiro freguês que paga o valor inteiro.
- **Os rivais (5):** 8 dos 40 lançam; guilda de alquimistas e ordem de clérigos entram como guildas; o leilão ganha focos, amuletos e elixires; a janela do mundo avisa a primeira peça Única encantada.
- **As frentes (6):** a peste é uma maldição de lugar que cresce (o mesmo relógio de 6 passos, e limpar o lugar tira um passo); a caça às bruxas é uma ambição; quem morre amaldiçoado deixa a peça amaldiçoada para o herdeiro; a maldição do moribundo vira o nêmesis.
- **A história (7):** o gerador distribui talento, dom, tradição e peça amaldiçoada pelos números de 1.5, e toda peça amaldiçoada tem quem a amaldiçoou.

## 8. G. O banco de provas da etapa

Quatro bancos novos (`provas_dons.py`, `provas_magia.py`, `provas_alquimia.py`, `provas_maldicao.py`), chamados pelo `provas_mundo.py`. **M** é medido em rascunho; **C** é chute.

| Meta | Faixa | Como se mede | Medido ou chute |
| --- | --- | --- | --- |
| A1. a pessoa comum não muda | os bancos de hoje passam; o retrato de 3 vidas de robô é idêntico com e sem o módulo | os bancos de hoje, e uma comparação de estado | C |
| A2. um dom entre iguais | 52 a 68% | 600 duelos por dom, nível 50, Raro | M: 53 a 60 |
| A3. dom e um grau de maestria contra a arma uma acima | no máximo 25% | 600 duelos | M: 14 |
| A4. a primeira Épica do robô ferreiro: prodígio · talentoso · jeitoso · avesso | Dia 20 a 35 · 25 a 40 · 35 a 55 · 65 a 95 | o robô do `provas_oficio.py`, 30 vidas | M: 26 · 30 · 44 · 80 |
| A5. a contagem em 10.000 pessoas geradas | prodígios por vocação 30 a 70; dons 340 a 460 | o gerador, 5 sementes | C (conta: 50 e 400) |
| A6. o talento oculto não sai na parte pública antes de aparecer | nunca | o texto da MESA em 200 vidas | C |
| B1. mago × mago | 44 a 56% | 600 duelos | M: 50 a 52 |
| B2. mago de cajado × guerreiro com amuleto: longe · perto · colado | 45 a 62 · 28 a 45 · 12 a 30 | 600 por linha | M: 50 a 59 · 35 a 38 · 23 a 28 |
| B3. o mesmo, o guerreiro sem amuleto: longe · perto | 90 ou mais · 65 a 88 | 600 por linha | M: 99 · 76 |
| B4. foco uma acima × guerreiro, perto · mago × amuleto uma acima | 55 a 80 · 0 a 8 | 600 por linha | M: 69 · 1 |
| B5. nível 50, foco duas acima × nível 500, perto | 30 a 60% | 600 duelos | M: 42 |
| B6. o dano de um feitiço de 1 ação num igual | mediana de 8 a 20% do PV; nunca mais de 40% sem crítico | os lances de B1 e B2 | M: 11 a 14 |
| B7. a Mana, lançando sem parar | seca entre a rodada 5 e a 8 | os mesmos | M: 6 a 7 |
| B8. o erro · o feitiço de 2 ações cortado por quem está colado | 0,1 a 0,5% · 35 a 65% | 20.000 lances | M: 0,25 · 51 |
| B9. mago de cajado × arqueiro, de longe | 10 a 35% | 600 duelos | M: 18 a 21 |
| B10. 3 guerreiros e 1 mago × 4: amuleto igual · um abaixo · sem | 28 a 50 · 65 ou mais · 80 ou mais | 600 por linha | M: 34 a 38 · 78 · 88 |
| B11. o clérigo: 5 × 5 no lugar de um guerreiro · três salas seguidas, contra 5 guerreiros | 28 a 50% · 5 pontos a mais | 600 lutas; 300 descidas | M: 36 · 65 contra 58 |
| B12. a cura um degrau abaixo do que feriu | um terço (com 2 pontos de folga) | as curas de B11 | M: 8% contra 24% |
| B13. o mago de começo × guerreiro de começo sem amuleto · com · × o javali | 70 ou mais · 20 a 40 · 5 a 25 | 600 por linha | M: 84 · 29 · 10 |
| B14. cada traço novo de bicho, com ele e sem ele | 8 pontos ou mais | 600 por traço | C |
| B15. a luta para quando deve; a ordem `lancar` se cumpre | em 100% das lutas com feitiço de 2 ações do outro lado | 200 lutas | C |
| B16. o estresse com magia misturada | nenhum erro | `estresse.py 1500` | C |
| C1. o alquimista de loja | até 6 por dia nos 5 primeiros dias (pior caso 12); até 4 depois | o robô do ferreiro de loja, 30 vilas | M: 3,9 a 4,7 (5,6); 0,0 |
| C2. o ervateiro que destila cura | 1,0 a 2,0 diárias ao preço de base | o coletor do banco, 30 vidas | M: 1,15 (no bolso, −0,5) |
| C3. a prata do mundo e a matéria fecham | sempre | toda prova da alquimia | M: fecha |
| C4. 2 poções da categoria num duelo · uma abaixo · uma acima | 52 a 65 · 44 a 54 · 58 a 72 | 600 por linha | M: 59 · 48 · 63 (as duas últimas, com a dose em 16% do PV) |
| C5. o veneno de lâmina da categoria · um degrau abaixo | 58 a 72 · 44 a 56 | 600 por linha | M: 64 · 47 |
| C6. o Iniciante acerta a fornada Comum · a Rara | 80% ou mais · menos de 25% | conta exata, e 600 fornadas | M: 83,5 · C |
| C7. poção Incomum vendida numa vila que não a faz | no máximo 30 de prata por dia de ida e volta | um robô atravessador | C: **risco** (11.1) |
| D1. a maldição Comum, sem amuleto, Vontade 50, chega ao passo 6 | média de 12 a 20 dias; nunca antes de 5 | conta exata, e 2.000 vidas | M: 15 (metade até o dia 13) |
| D2. com amuleto do grau · um grau acima | média de 35 a 70 dias · menos da metade morre em 400 dias | idem | M: 48 · 41% |
| D3. o clérigo Treinado quebra no passo 1 · no passo 5 | 45 a 60% · 15 a 30% | conta exata | M: 53 · 23 |
| D4. mesma semente, mesmo passo no mesmo dia; o ato longo para quando o passo sobe | sempre | 60 vidas | C |
| D5. a MESA não mostra o que o personagem não sabe; os invariantes novos | nunca vaza | o texto da MESA em 200 vidas | C |
| E1. o encanto ativo × o gêmeo · × o gêmeo sem amuleto | 44 a 58 · 50 a 66 | 600 por linha | M: 46 a 50 · 57 |
| E2. nenhum efeito passivo vale mais que | 72% entre iguais | 600 por efeito | M: de 55 a 70 (`devolve` no teto) |
| E3. a peça encantada que dorme não solta; falha de 10 ou mais amaldiçoa | sempre | 60 obras de mão posta | C |
| F1. a vila de teste nasce inteira; uma saída de erva de um dia vende por no máximo 12 de prata | sim; 200 vilas | o `vila_teste.py` e a meta K4 de hoje | C |
| F2. o noviço e a boticária de jornal ficam, no bolso, como o ferreiro de jornal | de +2 a +4 por dia | o robô do jornal, 30 vidas | C (por construção) |

Todas as metas de hoje seguem valendo e têm de passar antes e depois.

## 9. H. Como construir

**Três levas. Cada arquivo tem um dono só em cada leva.**

**Leva 0, um construtor (o alicerce e os ganchos).** Mexe uma vez em cada arquivo velho e cria os módulos novos vazios. No fim, os bancos de hoje passam e o estado de uma vida de robô é idêntico ao de antes.
- `tabelas_mundo.py`: eventos novos (`lancar`, `destilar`, `beber`, `encantar`, `rezar`, `estudar`, `maldicao`), ofícios (`alquimia`, `arcano`, `fé`, `verde`, `pacto`), módulos (`dons`, `magia`, `alquimia`, `maldicao`), a matéria `peçonha` e os bens novos.
- `estado.py`: os campos da pessoa (`talento`, `dom`, `sabe`, `mana`, `funda`, `doses`, `maldicoes`); o verbo `maldicao`; os tipos de item `foco`, `amuleto`, `elixir`; o uso `amuleto`; `item.encantos` e `item.maldicao`; `lugar.botica`, `lugar.santuario`, `lugar.maldicao`; os invariantes; `lutador()` leva a Mana, os feitiços e a ferida funda.
- `itens.py`: os tipos novos, e a janela (o encanto, a maldição só se foi lida).
- `pessoas.py`: a ficha chama `magia.na_ficha(p, F)` e `dons.na_ficha(p, F)`.
- `ato.py` e `corpo.py`: o gancho por bloco (cada módulo pode ter `bloco(E, pid)`, que devolve efeitos e uma parada), a parada vinda da virada, `dons.rende` no treino e `dons.teto` no subir, e `luta_fecha` devolve a Mana, a ferida funda e a maldição pega na luta.
- `oficio.py`, `caca.py`, `mercado.py`: só as chamadas a `dons.rende`, `dons.teto` e `dons.soma`.
- os módulos vazios: `dons.py` (devolve 1, 8 e 0), `magia.py`, `alquimia.py`, `maldicao.py`, e as quatro páginas `tabelas_*.py` com os números deste projeto.

**Leva 1, quatro construtores ao mesmo tempo.** Cada um é dono do seu módulo, da sua página de tabelas, do seu banco e dos arquivos velhos que só ele toca (a luta e os bichos são de B; o mercado é de C; A e D não tocam arquivo velho).

| Construtor | É dono de | O que expõe |
| --- | --- | --- |
| **A, os dons** | `dons.py`, `tabelas_dons.py`, `provas_dons.py` | `nasce(E, pid, escolha=None)` · `rende(p, caminho)` · `teto(p, caminho)` · `soma(p, onde)` · `na_ficha(p, F)` · `revela(E, pid, vocacao)` · `ler(E, pid, vocacao, com)` · `mesa(E)` · `so_mestre(E)` |
| **B, a magia e a luta** | `magia.py`, `tabelas_magia.py`, `provas_magia.py`, **`luta.py`**, `estresse.py`, `tabelas_bichos.py`, `bichos.py` | `na_ficha(p, F)` · `lanca(S, f, feitico, alvo, via=None)` · `passa(S, f)` · `escolhe(S, f)` · `confere(feitico)` · `bloco(E, pid)` (a Mana fora da luta) · `aprende(E, pid, feitico, com)` · `estudar`, `rezar`, `vigilia` · `mesa(E)`. No `luta.py`: a ação `lanca`, as ordens e paradas novas, os estados com prazo, os quatro traços |
| **C, a botica e o encanto** | `alquimia.py`, `encanto.py`, `tabelas_alquimia.py`, `provas_alquimia.py`, **`mercado.py`**, `tabelas_mercado.py` | `pede`, `destilar`, `continua`, `larga`, `beber(E, pid, bem)`, `untar(E, pid, item, bem)`, `tratar(E, pid, quem)`, `jornal` · `encanto.pede`, `encanto.gravar` · `virada(E)` · `mesa(E)`. No `mercado.py`: os bens novos, a botica que produz, a prateleira com foco e amuleto |
| **D, as maldições** | `maldicao.py`, `tabelas_maldicao.py`, `provas_maldicao.py` | `poe(E, pid, tipo, grau, de)` · `virada(E)` (o teste do dia, pelo dado do mundo) · `bloco(E, pid)` (o lugar) · `efeitos(p)` (o que cada passo tira) · `ler(E, pid, com)` · `quebrar(E, pid, i, com)` · `cumpre(E, pid, i)` · `veste(E, pid, item)` · `mesa(E)` · `so_mestre(E)` · `retomar(E)` |

Onde dois se tocam, a leva 0 já deixou a assinatura: a luta pede a maldição por `maldicao.poe`; a cura do clérigo e a poção usam a mesma `magia.cura(valor, funda)`; o encanto usa `magia.confere` e, quando falha feio, `maldicao.poe`.

**Leva 2, um construtor e dois verificadores (o fecho).** `vila_teste.py` (7.1), `GUIA_VILA.md`, os capítulos 10 a 14 do `REGRAS.md`, o `MUDANCAS.md`, o `provas_mundo.py` chamando os quatro bancos. Os verificadores jogam três vilas (o mago, a boticária, o guerreiro amaldiçoado), procuram jeito de enriquecer depressa com poção, serviço e encanto, e rodam todos os bancos.

**Tamanho:** cerca de 1.900 linhas novas (dons 250, magia 550, alquimia e encanto 450, maldição 300, tabelas 350) e 350 mexidas nos arquivos de hoje, mais os bancos.

## 10. I. O que é do jogador decidir

1. **A guarda contra magia** (é o que faltava da "magia contra aço").
   **a)** o amuleto é a armadura contra magia; sem ele, a armadura vale um degrau abaixo. Medido: sem amuleto, o guerreiro perde 99% de longe e 76% de perto.
   **b)** a armadura vale inteira e o amuleto só apara. Medido: 75% e 44%.
   **c)** só o amuleto guarda; sem ele, a pessoa está nua.
   *Recomendo a:* é a lei do motor sem exceção, faz do amuleto a peça que todo mundo quer, e um amuleto Comum custa 10 de prata.
2. **Os talentos do primeiro personagem.**
   **a)** você escolhe uma vocação em que é talentoso; o mundo rola as outras nove e o dom, escondidos.
   **b)** o mundo rola tudo, e você descobre fazendo.
   **c)** você escolhe três (um talentoso, um jeitoso, um avesso) e nada fica escondido.
   *Recomendo a.* Os herdeiros rolam tudo, com o sangue: é o que faz cada herdeiro ser outra pessoa.
3. **A quarta tradição.**
   **a)** a bruxaria entra agora. **b)** só as três agora, e a maldição vem de bicho, lugar e peça. **c)** outra (o canto).
   *Recomendo a:* a maldição precisa de dono no mundo.
4. **A força do mago sozinho.**
   **a)** fica como medido: cajado contra aço, 50 a 59% de longe, 35% de perto, 23 a 28% colado.
   **b)** o esforço passa a valer para feitiço de 1 ação, pela Mana em dobro. Medido: 66%, 47% e 38%, e a Mana seca na rodada 4.
   *Recomendo a.* A magia já manda em quem não tem amuleto; com b o mago passa o guerreiro também de perto.
5. **O veneno de lâmina.**
   **a)** existe para todos, um golpe por dose, e é crime nas vilas. Medido: 64% entre iguais.
   **b)** três golpes por dose. Medido: 69 a 71%.
   **c)** só bicho e vilão; o jogador não usa.
   *Recomendo a.*
6. **A botica como ofício de começo.** Medido: quem vive só de colher erva e destilar perde meia prata por dia; a lenha empata; o diarista ganha uma.
   **a)** fica assim: a botica se paga com o jornal, como a forja.
   **b)** a erva passa a render 2 por bloco, como a lenha. Mexe numa tabela de hoje; pela conta, a meta K1 segue na faixa.
   **c)** a poção de cura sobe de 10 para 12 na base.
   *Recomendo a.*

## 11. O que não sei, o que pode quebrar, e o que medi de verdade

### 11.1 O que pode quebrar o equilíbrio

- **O arqueiro contra o mago (18 a 21%).** A resposta do mago é chão, névoa e um guarda, não número. Se o jogador quiser o mago de pé contra o arco, o escudo arcano tem de valer mais contra tiro. Não mexi.
- **O mago no grupo contra gente de amuleto (34 a 38%; a régua é 50%).** A área de 1d6 rende pouco: com 1d8 e menos Mana deu 36%, nada mudou. O que muda é o amuleto do outro lado (78% e 88%). Se o mundo gerado der amuleto a todo mundo, o mago vira peso. O número de 1.5 (quantos andam de amuleto) é o que afina isso.
- **O curandeiro numa luta só (36%).** Com a cura em 16% do PV não valia nem em três salas (54 contra 56); com 24% vale (65 contra 58). Fiquei com 24% (`K_CURA` 6). Mais que isso e ninguém morre.
- **Sem amuleto é sentença (99%).** É de propósito, mas quer dizer que o primeiro bandido com varinha mata o personagem que não comprou o seu. A mesa tem de avisar, como avisa do elmo.
- **A poção Incomum numa vila que não a faz** nasce com o preço no teto (o triplo), como a matéria Rara de hoje. Quem trouxer da cidade vende a primeira por três vezes a base. Pus a meta C7 e não medi: não há viagem ainda.
- **O `devolve` no teto vale 70%** no motor de hoje. Com o encanto ele passa a ter fábrica. A meta E2 o segura em 72%.
- **A maldição em quem não é o jogador.** O nomeado amaldiçoado morre em duas semanas se ninguém fizer nada, e hoje ninguém age sozinho. Até a etapa 3, maldição em nomeado só por mão do Mestre.
- **Treinar magia estudando é bloco leve.** O mago cansa menos que o guerreiro e treina mais blocos por dia. Pode ser que o arcano suba depressa demais. Não medi.

### 11.2 O que não sei

- Se quatro tradições com vinte feitiços cabem numa etapa só. Catorze dos vinte nunca rodaram. Se apertar, saem primeiro o verde (pede chão e céu na luta) e depois o pacto na luta, ficando a bruxa só com o atar e o ler.
- Quanto custa aprender (9 blocos por círculo) e ensinar. É chute.
- Se "descobre fazendo" diverte ou irrita. O jogador vê os blocos e faz a conta. A pergunta 2 deixa a saída.
- A conta rápida dos rivais (etapa 5) vai precisar de um número para a magia. Não pensei nele.

### 11.3 O que medi de verdade

| Rascunho | O que é | Saída |
| --- | --- | --- |
| `mede_dons.py` | a luta de hoje, com dom e maestria postos na ficha; 600 lutas por linha | `saida/dons.txt` |
| `magia_rascunho.py` e `mede_magia*.py` | a magia por cima do `luta.py` (o turno, a decisão e a ficha trocados só na memória): faísca, geada, lança, escudo, área, cura, poção, veneno, encanto; 400 lutas por linha | `saida/magia_luta*.txt` |
| `mede_alquimia.py` | os bens novos postos na tabela só na memória; o mercado de verdade; o robô do ferreiro de loja com botica no lugar da forja; o coletor do banco colhendo erva; 30 vidas por linha | `saida/alquimia*.txt` |
| `mede_talento.py` | o robô ferreiro do banco com o bloco valendo mais ou menos; 10 vidas por talento. O comum deu 17, 59 e 177: bate com o banco | `saida/talento.txt` |
| `mede_maldicao.py` | a conta exata do dado do motor; não é simulação | `saida/maldicao.txt` |

**Limites das medidas.** A gente gerada do motor tem uma maestria só para tudo: o arqueiro e o clérigo de prova lutam de espada como Mestres, e o meu mago tem mão de Iniciante no cajado. Isso pesa contra o mago nas comparações de grupo. Quem lança segue uma regra simples (prende quem vem, afasta-se, cura abaixo de metade): um jogador faz melhor. E o motor estava sendo consertado enquanto eu media: as réguas (guerreiro contra guerreiro, a escada do comum, a meta do ferreiro de loja) bateram com os números do livro, e é por elas que confio no resto.

### 11.4 O que deixo de fora desta etapa

Invocar, voar, iludir, mudar de forma, ressuscitar (morto é morto) · desfazer feitiço alheio · feitiço que se sustenta, além de lama e névoa · escolas dentro do arcano · deuses com nome e listas por deus · o canto · o grimório como item · poção que estraga, frasco e peso · dom ganho em vida e dom maior · familiar e bicho companheiro · maldição de linhagem, peste e caça às bruxas (ganchos em 7.3) · o gerador que distribui tudo isso pelo mundo (etapa 7).
