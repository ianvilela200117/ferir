# Projeto A da etapa 4b: as masmorras e o ladino

Rascunho de projeto. Nada daqui é regra até passar no banco de provas. A outra metade da etapa (os dragões e os povos do personagem) é do projeto B; onde as duas se tocam está na seção 10.

## 0. Em uma página

1. **A masmorra é um lugar do mapa** (tipo `masmorra`), vizinho de uma vila ou de um ermo, a alguns blocos de caminho. Por dentro ela tem **salas**, e cada sala é um lugar pequeno (tipo `sala`), ligado às outras por passagens. Assim a contagem das criaturas, a prata no chão, a peça largada e a morte de quem cai lá dentro usam as regras que o motor já tem, sem regra nova.
2. **Cada sala guarda** o que mora nela (criaturas contadas, ou o chefe), a porta de cada passagem (fechada, trancada, emperrada ou escondida), as armadilhas, o escuro (toda sala é escura, menos a que tem fogo aceso), o que está guardado (um baú, um sarcófago, um nicho, com fechadura), e a escada para o nível de baixo.
3. **De onde vem:** cinco moldes (a cripta, a mina abandonada, a ruína, a toca grande, o covil), de 3 a 16 salas por nível, de 1 a 3 níveis. **A cada descida, as criaturas, as armadilhas, as fechaduras e o tesouro sobem uma categoria.** O chefe mora no fundo, com as fases que a luta já roda.
4. **A memória:** a sala limpa fica limpa. Volta só o que tem motivo: o bicho que cria (o rato, a aranha), o bando de fora que acha a masmorra vazia (em meses), e o morto que o chefe vivo levanta. O tesouro levado não volta nunca.
5. **Descer** é como a saída de caça: um ato aberto, escrito na pessoa, que sobrevive a fechar o turno. Lá dentro o tempo anda em **lances de 20 minutos**; doze lances fecham um bloco, e só então o relógio anda, pelo `ato.passa`, como sempre.
6. **A luz** é uma tocha (um bem, 1 de prata, arde um bloco) ou o feitiço luz (4 de Mana por bloco). Sem luz, quem não vê no escuro luta com −4 no golpe e −8 no tiro, anda devagar e não procura, não abre e não desarma. **Medido: o grupo da vila contra seis esqueletos vence 81% com luz e 29% no escuro.**
7. **O encontro** é o da caça: quem vê primeiro escolhe. Andar escondido é um teste do mais barulhento do grupo contra a Percepção de quem vigia; a armadura pesada e a luz atrapalham. **Medido: ver primeiro leva o grupo de 77% a 90%; ser surpreendido o derruba a 48%.**
8. **A armadilha e a fechadura seguem "o item decide":** a armadilha bate pela conta do aço (o valor da categoria dela contra a proteção de quem pega), e a gazua conta contra a fechadura como a arma contra a armadura. **Medido: um dardo Comum tira 20 do Maro; um Raro o mata na hora em 46% das vezes; contra quem veste malha Rara, o dardo Raro tira 19.**
9. **O ladino é o 17º caminho, a `manha`:** andar escondido, achar e desarmar armadilha, abrir fechadura. Sobe por blocos como as armas (40, 160, 500, 1.500, vezes o talento), com feito de Mestre para cima, e usa a **gazua**, peça com categoria. O **golpe pelas costas** (de Treinado em diante) é proposta à parte, medida dentro da lei do item. O **furto** fica escrito e entra na etapa 3 (pergunta 1).
10. **O tesouro é prata que já existe**, posta pelo gerador, mais peças (às vezes malditas) e, do Épico para cima, o núcleo do chefe. Não se refaz: descer de novo numa masmorra limpa não rende (a meta mede).
11. **A vila de teste ganha a Cripta da Cova Velha**: 7 salas sob a cova que o Maro já limpou, com corpos-secos, esqueletos, ratos, um dardo, uma runa, uma porta de ferro, um baú, um nicho escondido e o guardião da cripta no fundo. Entra por `vila_teste.py masmorra ensaio`, que só acrescenta. **Medido em robô (rascunho): com Tomé e Rute, o grupo limpa a cripta em 91% das vidas e o Maro morre em 10%; sozinho, morre em 96%.**

## 1. O que eu medi, e como

Tudo rodou de dentro do rascunho, lendo o motor de hoje (`/home/user/ferir/motor10`), com `PYTHONDONTWRITEBYTECODE=1` e o `MOTOR10_MUNDO` numa **cópia** do `ensaio/` (o Maro de hoje: nível 5, PV 141, espada, escudo, malha e elmo Comuns, Força 70, Agilidade 60, Percepção 50). Nada foi gravado no motor nem no save do jogador. As lutas são as do `luta.py` de verdade, com semente fixa. Os arquivos ficam ao lado deste:

| Arquivo | O que mede | Lutas |
| --- | --- | --- |
| `m1_lutas.py` → `m1_saida.txt` | o Maro e o grupo da vila contra esqueletos, corpos-secos e ratos: sala aberta, corredor de um, com luz e no escuro, a surpresa | 500 por linha |
| `m2_armadilhas.py` → `m2_saida.txt` | a armadilha que dispara, pela conta do aço, contra o Maro, o Tomé, a Rute e um nível 50 de malha Rara; e a conta exata do 2d20 de cada teste do ladino | 20.000 disparos por linha |
| `m3_chefe.py` → `m3_saida.txt` | os candidatos a chefe da cripta; o golpe pelas costas contra o gêmeo e contra a arma uma acima | 500 por linha |
| `m4_descida.py` → `m4_saida_*.txt` | **rascunho** do robô que desce a cripta inteira: a luta de verdade, e o resto (lance, luz, armadilha, fechadura, o que vagueia) escrito à mão pela proposta | 300 vidas por linha |
| `m5_surpresa.py` → `m5_saida.txt` | o que valem ver primeiro, ser surpreendido, a luz e o corredor no grupo | 500 por linha |

**O que é medida de verdade:** as lutas (m1, m3, m5), o golpe da armadilha (m2, pela conta do aço do `tabelas.py`), as chances dos testes (a conta exata, como o `caca._somas`). **O que é rascunho:** o robô da descida (m4) usa a luta de verdade, mas a casca da masmorra foi escrita à mão; os números dele são a ordem de grandeza, e o banco de verdade (seção 12) mede de novo pelo `masmorra.py`.

## 2. A masmorra como lugar

### 2.1 O que ela é no estado

**A masmorra** é um lugar (`tipo: "masmorra"`), com nome, vizinhos (a vila ou o ermo de onde se chega) e `longe` (os blocos de caminho, como o ermo). Os campos novos:

| Campo | O que guarda | Padrão (save antigo) |
| --- | --- | --- |
| `molde` | cripta, mina, ruína, toca, covil | (não é masmorra) |
| `niveis` | a lista dos níveis: `{n, cat, salas: [ids]}` | |
| `entrada` | a sala onde se chega | |
| `portas` | uma porta por passagem, com a chave `"SALA1\|SALA2"` (as duas em ordem): material, categoria, `estado` (aberta, fechada, trancada, emperrada, arrombada), `fechadura` (categoria ou nada), `chave` (o item que abre). A armadilha da porta mora na lista da sala de onde se abre; a passagem escondida mora nos `segredos` da sala até alguém a achar (cada fato num lugar só) | sem porta: passagem livre |
| `alarme` | de 0 a 5: o quanto a masmorra está acordada | 0 |
| `vagantes` | `{espécie: quantos}`: os que andam e não moram em sala nenhuma | nenhum |
| `limpa` | a primeira limpeza: `{dia, quem, chefe}` | nada (nunca limpa) |
| `origem` | o que o gerador da história conta dela (etapa 7) | texto vazio |

**A sala** é um lugar (`tipo: "sala"`), com `masmorra` (o id dela), `nivel`, `vizinhos` (as salas ligadas por passagem) e os campos que o lugar já tem e que aqui servem de novo:
- `bichos` e `teto`: quem mora ali, **contado** (o gravador já confere a espécie; bicho ou criatura). O `teto` só existe para quem cria (o rato, a aranha); o morto e o povo não têm teto na sala.
- `estoque`: a prata e os bens que estão ali (no chão, ou dentro do que a sala guarda). Conta na prata do mundo sem mudar nada no gravador.
- as peças com `onde` na sala e `solto`: o achado, como no ermo.

E os campos novos da sala:

| Campo | O que guarda | Padrão |
| --- | --- | --- |
| `largura` | a largura que a luta usa: 1 (corredor), 2 (sala estreita), ou nada (sala aberta) | aberta |
| `acesa` | há fogo aceso ali (o acampamento dos goblins): a luz é de todos | não |
| `cat` | a categoria das criaturas da sala (a do nível); a espécie de categoria maior fica na dela | a da espécie |
| `atento` | quem mora ali: −1 dormindo, 0 à toa, +1 alerta | 0 |
| `armadilhas` | a lista: `{tipo, cat, onde: chão \| porta:SALA \| guardado, achada: dia, feita: desarmada \| disparada}` | nenhuma |
| `guardado` | o baú, o sarcófago, o nicho: `{nome, fechadura, aberto, itens}`; fechado ele, a prata e as peças da sala estão dentro | nada |
| `segredos` | as passagens escondidas: `{para: SALA, cat}`; achada, sai daqui e vira passagem (os vizinhos das duas salas e, se tem, a porta) | nenhum |
| `chefe` | o chefe que mora ali: `{qual, vivo}` (um dos `tabelas_criaturas.CHEFES`, ou um bicho chefe) | nenhum |
| `coleta`, `coleta_teto` | na mina, o minério da categoria do nível (a regra da coleta, sem mudar nada) | |
| `sobre` | o que se vê ao entrar (a frase da mesa) | |

**Por que a sala é um lugar:** a morte já põe as peças do morto soltas no lugar onde ele morreu e a prata no estoque desse lugar; a caça já cria o bicho no lugar que tem teto (`caca.virada`); o achado solto já é de quem o pega. Com a sala como lugar, a pessoa que morre na sala 4 deixa tudo na sala 4, o rato da sala 4 cria na sala 4, e a prata do baú é contada na soma do mundo. O preço disso: mais lugares no `lugares.json` (a região da etapa 3, com 8 masmorras de 4 a 30 salas, ganha de 100 a 200), e nenhuma sala pode ser vizinha de vila (senão a mesa da caça a listaria).

### 2.2 De onde vem: os moldes

| Molde | Salas por nível | Níveis | Quem mora (pela categoria do nível) | Armadilhas | O que guarda | O chefe do fundo |
| --- | --- | --- | --- | --- | --- | --- |
| **cripta** | 4 a 8 | 1 a 2 | esqueleto, corpo-seco, carniçal, alma penada; do Raro para cima múmia e espectro; ratazana nos ninhos | dardo, lâmina, runa, gás | oferendas (prata), peças velhas (às vezes malditas), o túmulo do chefe | o guardião da cripta (novo, abaixo); no Épico, o necromante |
| **mina** abandonada | 6 a 12 | 1 a 3 | ratazana, aranha-de-toca, trasgo, golem de barro; um bando de goblins ou de orcs (covil) | fosso, pedra, alarme | o minério da categoria (coleta contada), ferramentas, a paga perdida (prata) | o xamã goblin ou o senhor da guerra orc |
| **ruína** | 8 a 16 | 1 a 3 | esqueleto, gárgula, golem, fogo-fátuo, harpia | todas | o tesouro do senhor antigo: prata, peças altas, um escrito | a bruxa do brejo, o necromante ou o senhor vampiro |
| **toca** grande | 5 a 10 | 1 a 2 | goblins, orcs, homens-lagarto, ogro (o covil de hoje, crescido) | fosso, alarme | o que o bando roubou (prata da região) | o xamã goblin ou o senhor da guerra orc |
| **covil** | 3 a 6 | 1 | um bicho chefe e o que come as sobras | nenhuma (o fosso e a água da caverna, que são do lugar) | o que o bicho juntou: a prata e as peças de quem ele comeu | a serpe, a hidra; **o dragão é do projeto B** |

**A forma** (o gerador): a entrada; um caminho principal até a escada (ou até o chefe, no último nível); de uma a três salas de lado (becos com tesouro ou armadilha); e, em um nível de cada três, uma sala escondida (um segredo). Os corredores são de largura 1; as salas, de largura 2 ou abertas (a cripta e a mina têm mais corredor; a ruína e a toca, mais sala aberta).

**Os níveis e o grau:** o nível 1 tem a categoria do molde; **cada descida soma uma categoria** (nas criaturas, nas armadilhas, nas fechaduras e no tesouro). O grau que a mesa lê é o do capítulo 6: E e F no Comum, D no Incomum, C no Raro, B no Épico. Medido (m3), o motivo de não pular degrau: o guardião da cripta Incomum (montante e placa Incomuns) contra o grupo da vila de peças Comuns vence 87% das lutas (o grupo vence 13%); o mesmo guardião Comum perde 98% delas.

### 2.3 A memória: a sala limpa fica limpa?

**Fica.** O que volta, e em quanto tempo (o mundo sozinho, na virada do dia):

| O que | Volta? | Quando |
| --- | --- | --- |
| o morto que anda (esqueleto, corpo-seco, múmia) | não, sozinho | só se o chefe da masmorra levanta: o vivo ergue **um a cada 10 dias** (o `COVA_ERGUE` que já existe), até o que a sala tinha; morto o chefe, nunca mais |
| o bicho que cria (rato, aranha, trasgo) | sim, pela regra da caça (a sala tem teto) | o rato que sumiu espera um casal de fora (em média 60 dias, Comum), e depois cria 4% por dia |
| o povo (goblins, orcs) | pela vida do covil, se a sala tem covil | a toca vazia espera 120 dias (goblin) ou 240 (orc) por um bando de fora (a regra de hoje) |
| **um bando de fora** | se o nível inteiro fica vazio | 120 dias depois de o nível ficar vazio, chega um bando da lista do molde (a conta da toca vazia de hoje; sem tesouro: ele traz só o que é dele) |
| o chefe | não | morto, morto; um chefe novo só chega com o bando de fora (o xamã, se a toca enche) |
| o tesouro levado | **nunca** | a prata não nasce |
| a armadilha disparada ou desarmada, a porta arrombada | não | ficam como ficaram |
| o alarme | cai | 1 por bloco sem barulho; na virada, volta a 0 |

### 2.4 O chefe no fundo

O chefe mora na última sala do último nível, com a guarda dele. É um dos chefes que a luta já roda (`tabelas_criaturas.CHEFES`: o xamã goblin, o senhor da guerra orc, a bruxa do brejo, o necromante, o senhor vampiro), ou um bicho chefe (a serpe, a hidra, o dragão do projeto B), escolhido pela categoria do último nível. As fases são as de hoje (ganhar e perder traço, recobrar Mana, o brado, erguer os mortos), e a luta para e pergunta quando ele muda.
**O chefe novo da cripta, o guardião da cripta** (`tabelas_criaturas.CHEFES`): o cavaleiro da cova na categoria do nível, de montante e placa velha, nível 25, mão de Treinado; abaixo de metade do PV bate o pé, dá o brado e ergue até dois mortos da sala; a guarda são dois esqueletos. Medido (m3, 500 lutas): o Comum, contra Maro, Tomé e Rute de PV cheio, perde 98% das lutas numa sala aberta e mata alguém da casa em 8%; no escuro, 85% e 27%; contra Maro e Tomé, 62% e 39%; contra o Maro sozinho (sem a guarda), o Maro vence 6% e morre em 64%.
**O núcleo:** do Épico para cima, o chefe do fundo dá o núcleo dele (o mesmo Livro de Itens da caça). Os chefes das masmorras entram na conta dos núcleos do mundo (6 Épicos e 2 Únicos por ano, `PROJETO.md`): o gerador da região os conta.
**A sucata do chefe de povo:** a montante e a placa dele são gastas e malfeitas, como as do povo: viram matéria da categoria dele (o cavaleiro Comum: metal Comum).

## 3. Como se desce

### 3.1 Os comandos

O modelo é a saída de caça (`caca.py`): um ato aberto, escrito em quem comanda (`marca.masmorra`), com quem vai junto marcado (`marca.masmorra = {de: quem comanda}`). Enquanto a descida está aberta, o grupo está **fora**: os atos da vila são recusados (o `estado.fora` passa a ler também a descida), come-se da própria carga, bebe-se a poção, e a cura da clériga vale como na saída ao ermo.

```
python3 masmorra.py ver                                       a masmorra vizinha (o que se sabe), a descida aberta, o mapa que o grupo viu, a mão do ladino
python3 masmorra.py descer [MASMORRA] [com=ID,ID] [ordem=ID,ID,...] [luz=tocha|feitiço|nada] [quem_luz=ID]
                                                              a ida (os blocos de caminho) e a entrada; o grupo chega à primeira sala
python3 masmorra.py ir SALA [escondido]                       anda à sala vizinha pela passagem (1 lance; escondido, 2)
python3 masmorra.py escutar SALA                              escuta à porta da passagem (1 lance; rolagem oculta)
python3 masmorra.py procurar [quem=ID]                        procura na sala: armadilha, passagem escondida, o que está guardado (2 lances; ocultas)
python3 masmorra.py abrir SALA|guardado [gazua|chave|força] [quem=ID]      a porta da passagem, ou o baú (1 lance por tentativa)
python3 masmorra.py desarmar [N] [quem=ID]                    a armadilha achada (1 lance por tentativa; falhar por 5 ou mais a dispara)
python3 masmorra.py contornar [N] · disparar [N]              passa ao largo da armadilha do chão (1 lance) · dispara de longe a do chão ou da porta (1 lance; barulho)
python3 masmorra.py atacar [inicio=longe|perto|colado] · esperar · recuar        diante do que apareceu (como na caça: atacar, deixar, fugir)
python3 masmorra.py luta "Nome: ordem" ["grupo: ordem"]       a luta aberta (é o `ato.py luta roda`); acabada, as contas
python3 masmorra.py pegar [tudo|prata|ITEM] [quem=ID]         o que a sala guarda (1 lance)
python3 masmorra.py descansar N [vigia=ID]                    dorme N blocos no chão, ali; o que vagueia rola a cada bloco
python3 masmorra.py ordem ID,ID,ID · luz tocha|feitiço|nada [quem=ID]        a ordem de marcha · acender ou apagar a luz (sem lance)
python3 masmorra.py voltar                                    volta pelas salas já andadas até a entrada (1 lance por sala)
python3 masmorra.py sair                                      sai pela entrada e volta para casa (fecha o bloco aberto, e a volta)
(SÓ O MESTRE) python3 masmorra.py mapa [MASMORRA] · conta · gera MOLDE "Nome" [vizinho=LUGAR] [niveis=N] [cat=K] [longe=N] · larga "por quê"
python3 manha.py ver [ID] · treinar N                         a mão do ladino · o treino em casa (pede uma gazua; bloco pesado)
```

### 3.2 O tempo: o lance e o bloco

O relógio só anda pelo `ato.passa`, em blocos de 4 horas. Lá dentro, cada ação custa **lances** (20 minutos); a descida conta os lances, e **quando chegam a 12, o `ato.passa` anda um bloco** para todo o grupo (o esforço leve da procura de caça), e o resto fica para o bloco seguinte. Nada do motor muda: o bloco que fecha é um bloco como os outros (a fome, o sono, o cansaço, o limiar que para o ato, a virada do dia, o corpo do personagem que espera). Cada ação diz, na saída, quantos lances faltam para fechar o bloco.

| Ação | Lances |
| --- | --- |
| ir à sala vizinha | 1 (escondido 2; sem luz, e sem quem veja no escuro, 2; carregando um caído, 2) |
| escutar uma porta | 1 |
| procurar na sala | 2 (todas as coisas escondidas da sala, uma rolagem oculta para cada) |
| abrir, desarmar, arrombar | 1 por tentativa |
| contornar a armadilha achada, ou dispará-la de longe | 1 |
| pegar o que a sala guarda | 1 |
| a luta (o que vem depois dela: o fôlego, amarrar a ferida) | 1 |
| voltar | 1 por sala andada |
| tirar alguém do fosso | 1 |
| descansar | em blocos inteiros (o bloco que estava aberto fecha antes) |

**Sair** fecha o bloco aberto (o resto conta como bloco inteiro) e faz a volta (os blocos de `longe`). **O bloco na masmorra** marca `marca.ermo_dia`, como a saída ao ermo: o dia da descida não é dia de repouso para a ferida (a regra de hoje, sem mudar o `corpo.py`).
**Medido (rascunho, m4):** a cripta de teste inteira (7 salas, 5 lutas) leva de 2 a 3 blocos lá dentro (o robô, que nem sempre procura tudo, fica em cerca de 2 por descida), mais 1 de ida e 1 de volta: um dia inteiro.

### 3.3 O escuro e a luz

| | O que faz |
| --- | --- |
| **a tocha** | um bem da carga (base 1 de prata; a vila a vende). Arde um bloco: quando o bloco fecha, gasta-se uma da carga de quem leva a luz. Na luta, quem a leva a larga no chão: a luz fica, e ninguém perde a mão do escudo |
| **o feitiço luz**, fora da luta | 4 de Mana por bloco (na luta segue a regra de hoje: 1 para acender e 1 por rodada). Anselmo, de Mana 19, alumia uns quatro blocos e chega à luta sem Mana |
| **sem luz** (para quem não vê no escuro) | anda com o dobro dos lances; não procura, não abre com gazua, não desarma (arromba, sim); a luta tem o escuro (−4 no golpe, −8 no tiro) |
| **quem vê no escuro** (o povo do projeto B; as criaturas noturnas) | anda, procura, abre e luta no escuro sem pena; a luta lhe dá o traço "noturno", que já existe |
| **a luz se vê de longe** | quem anda com luz tem −6 no andar escondido contra quem está no escuro |
| **a sala acesa** | a luz é de todos, e a tocha não denuncia ninguém |

A luta da masmorra diz no cenário `luz: true` quando há luz (o `ato.luta_nova` não põe o escuro da noite), e `tempo: ["escuro"]` quando não há. **Medido (m1 e m5, 500 lutas por linha):**

| Luta | Com luz | No escuro |
| --- | --- | --- |
| Maro contra um esqueleto | vence 71%, morre em 20% | 48%, morre em 35% |
| Maro, Tomé e Rute contra quatro esqueletos | 97%, morre alguém em 8% | 79%, em 34% |
| os três contra seis esqueletos (Maro na frente) | 81%, em 27% | 29%, em 75% |
| os três contra seis esqueletos (Tomé na frente) | 77%, em 31% | 28%, em 70% |
| os três contra oito goblins da toca | 95%, em 11% | 80%, em 27% |

O escuro pesa mais contra o esqueleto que contra o goblin porque o goblin é frágil: a luz é o que separa a cripta de um cemitério de aventureiros. Com uma tocha por bloco, a cripta de teste custa de 2 a 3 tochas por descida (medido, m4: 2,9 por vida).

### 3.4 O grupo e a ordem de marcha

- **Quem vai junto** é gente do mundo que está no mesmo lugar (`com=`), como na caça: entra nas lutas, o corpo passa os mesmos blocos, cuida de si em casa, e **tem parte** no que se acha (seção 6).
- **A ordem de marcha** é a lista do grupo (`ordem=`; muda a qualquer hora, sem lance: `masmorra.py ordem`): o primeiro é quem pisa primeiro (a armadilha do chão é dele), quem olha primeiro (a armadilha de passagem e a emboscada), e quem fica na frente na luta. O cenário da luta põe o grupo nessa ordem; quem é de trás (o arqueiro, o mago, o ladino) vai com `linha: trás`. Num corredor de um, o `luta.py` já põe um atrás do outro, e já sabe trocar de lugar (quem recua troca com quem vem).
- **O corredor de um** é a arma do grupo pequeno, e já está medido no livro (um contra quatro: 48% aberto, 85% no corredor). Na cripta (m1 e m5): os três contra seis esqueletos vencem 99% no corredor e 77% a 81% na sala aberta. **Puxar o inimigo para o corredor** não é regra nova: quem vê primeiro escolhe onde começa (a sala onde está, ou recuar um passo para a passagem e esperar).
- **Uma luz só serve a todos** (o grupo anda junto); quem quer andar no escuro, e ver, é o batedor que vê no escuro (o projeto B).

### 3.5 O encontro: quem vê primeiro

Quando o grupo entra numa sala com alguém (ou alguém chega até ele), o comando para e conta o que se vê, como a caça conta o bicho. Do chefe, ninguém sabe de graça: o Mestre lê a frase dele quando a cena o põe à frente.

1. **O grupo anda escondido** (`ir SALA escondido`): **o grupo anda no passo do mais barulhento.** Rola quem tem o pior número: 2d20 + Agilidade ÷ 10 + manha (+ o dom) − a armadura do tronco (couro 0, malha −3, placa −6) − a luz (−6, se o grupo leva luz e a sala está no escuro), contra **20 + Percepção ÷ 10 do melhor vigia da sala**, mais 4 se estão alertas, menos 6 se dormem (o morto não dorme). Rolagem oculta: o número diria quantos e quem são.
   - Passou: **o grupo vê primeiro** (se pode ver: luz, ou quem vê no escuro; no escuro sem ver, o grupo só ouve: sabe que há gente, não quantos). Escolhe: **atacar** (os de lá surpreendidos: perdem o primeiro turno; começa perto, ou longe se a sala é aberta, ou o grupo recua um passo e espera no corredor), **recuar** sem ser visto, ou **esperar** escondido (um lance: a sala segue como está, e o grupo escolhe de novo).
2. **Não escondido, ou falhou:** os de lá notam o grupo. Se estão alertas (o alarme da seção 3.6), ou são de emboscada (a gárgula, a aranha, quem a sala diz), **quem vai na frente** rola Percepção + manha contra 20 + Agilidade ÷ 10 deles: falhou, **o grupo é surpreendido** (perde o primeiro turno). Se estão à toa, ninguém é surpreendido e a luta começa perto.
3. **A porta** muda a distância: abrir uma porta com gente atrás dela começa colado.

**Medido (m5, o grupo da vila, Tomé na frente, 500 lutas):**

| | Ninguém surpreso | O grupo surpreende | O grupo é surpreendido |
| --- | --- | --- | --- |
| contra seis esqueletos | vence 77%, morre alguém em 31% | 90%, em 23% | 48%, em 57% |
| contra oito goblins da toca | 95%, em 11% | 99%, em 2% | 75%, em 36% |

**A chance de ver primeiro** (a conta exata, m2), contra esqueletos (Percepção 41) e goblins (61):

| Quem é o mais barulhento | Esqueletos, no escuro | com luz | alertas, com luz | Goblins, no escuro | com luz |
| --- | --- | --- | --- | --- | --- |
| o Maro de malha (+6 −3) | 53% | 29% | 18% | 44% | 23% |
| a Rute de couro (+8) | 74% | 48% | 32% | 66% | 40% |
| um ladino Iniciante de couro (+7 +2) | 77% | 53% | 36% | 70% | 44% |
| um ladino Treinado de couro (+8 +4) | 86% | 66% | 48% | 81% | 57% |
| quem veste placa (+6 −6) | 40% | 20% | 12% | 32% | 15% |

Por isso o ladino anda na frente sozinho (é ele o mais barulhento de um grupo de um), e o grupo de malha quase nunca surpreende ninguém com uma tocha na mão. E por isso ver no escuro (o projeto B) vale tanto: tira a luz da conta.

### 3.6 O alarme, o que vagueia e o descanso

**O alarme** (0 a 5, na masmorra): a luta +1; cada tentativa de arrombar +1; a armadilha que faz barulho (pedra, fosso +1; alarme +2). Cai 1 a cada bloco sem barulho. Com 2 ou mais, os que moram ali estão alertas (+4 na Percepção, e armam a emboscada); com 4 ou mais, **os da sala vizinha vêm**: um encontro logo depois da luta (o reforço não entra no meio da luta: a luta de hoje não sabe disso, e fica de fora).

**O que vagueia:** a cada bloco que fecha lá dentro, o mundo rola (o dado do mundo, oculto): **1 em 6, mais 10 pontos por ponto de alarme**. Saindo, vem um bando dos `vagantes` da masmorra (que saem da conta dela). Ele chega ao grupo: quem vai na frente testa a atenção (item 2 do encontro). Na cripta de teste, os vagantes são um corpo-seco e três ratos; medido (m4), o grupo cruza com eles cerca de uma vez por vida.

**O descanso lá dentro** (`descansar N`): é dormir no chão (o `ato.passa` com `dorme='chao'`, como quem cai no sono no ermo): o sono e o cansaço baixam 2 por bloco, o PV volta 5% por bloco (dois por dia, como em casa), a Mana volta pela regra da tradição (o druida, a metade entre muros). **Cada bloco rola o que vagueia.** Com quem vigia (`vigia=ID`, que não dorme naquele bloco), o grupo não é surpreendido; sem vigia, é. A conta: dois blocos de sono com o alarme em 1 dão 46% de visita (com o alarme em 0, 31%); o descanso lá dentro serve para o sono e a Mana, não para o PV (10% por noite). Para o PV, voltar à vila.

### 3.7 A retirada pelas salas limpas

`masmorra.py voltar` refaz o caminho andado (`caminho` na descida) até a entrada: 1 lance por sala, sem encontro nas salas limpas (só o que vagueia, no bloco que fecha). **Quem foge de uma luta** (a ordem `recuar` até sair da luta, a regra 3.15 de hoje) pode ser seguido: as feras e o povo alerta vêm atrás pela índole da espécie (a tabela da caça, `indole`); o morto lento (o esqueleto, o corpo-seco) não passa da sala dele. Quem vem atrás chega na sala seguinte, e a luta abre ali, de novo: num corredor de um, o grupo que recuou luta um contra um.

### 3.8 A luta para e pergunta

A luta é a do `ato.py luta`, sem tirar nada: o `masmorra.py` só monta o cenário (o grupo na ordem de marcha, a largura da sala, a luz ou o escuro, a surpresa, o chefe e a guarda dele pela forma curta das criaturas) e chama o `ato.luta_nova`; no fim, faz as contas (seção 6). Tudo o que o capítulo 3 e o 11 param, para (quem cai, o chefe que muda de fase, quem fraqueja). **A masmorra para, fora da luta,** e pergunta quando:
- aparece alguém (o encontro: atacar, esperar, recuar; a luta só abre depois da escolha);
- a passagem tem porta trancada ou emperrada (gazua, chave, força, ou deixar);
- a armadilha é achada (desarmar, contornar, disparar de longe, ou deixar);
- a armadilha dispara (o dano, a ferida, quem caiu no fosso);
- a última tocha começa a arder (o bloco que vem é o último com luz), e quando a luz acaba;
- o corpo de alguém do grupo cruza um limiar (a fome, o sono, o cansaço), ou alguém fica abaixo de metade do PV;
- o barulho trouxe gente (o alarme em 4);
- o grupo chega à escada (descer é escolha) e à porta do chefe;
- a sala tem o que pegar.

### 3.9 O que a mesa mostra, e o que vai ao SÓ O MESTRE

**A `MESA.md`, com a descida aberta** (cabe em 1,5 KB): onde o grupo está e o que se vê ali; a luz (quem leva, quantas tochas na carga, quantos lances faltam para o bloco fechar); quanto tempo dentro; o alarme em palavras ("a cripta está quieta", "há barulho", "a cripta está acordada"); o grupo na ordem de marcha, com o PV; **o mapa que o grupo viu** (as salas vistas, as passagens e as portas, as armadilhas achadas, o que ficou para trás); o que dá para fazer daqui, com os lances; a mão do ladino com a conta de cada teste. Sem descida: a masmorra vizinha e o que se sabe dela ("dizem que os mortos da Cova Velha subiam de uma escada").
**O SÓ O MESTRE:** o mapa inteiro, sala por sala (quem mora, quantos, se dormem; as armadilhas, achadas ou não; as fechaduras e as chaves; o tesouro; os segredos; o chefe e as fases dele); o alarme e a chance do que vagueia no bloco; os vagantes; e as rolagens ocultas (escutar, procurar, a armadilha de passagem, o andar escondido, a atenção), com os números.
**O que o personagem sabe** mora nele (`marca.mapa.MASMORRA`: as salas e passagens vistas, as armadilhas achadas): o herdeiro não sabe o mapa do morto.
**O `RETOMAR.md`** leva a descida aberta (como leva a saída de caça) e os fatos; **o gerador da masmorra é segredo** (o evento que cria as salas vai ao SÓ O MESTRE do RETOMAR, pelo `turno.secreto`, como o covil e a peça maldita).

## 4. As armadilhas e as fechaduras

### 4.1 A lei: o item decide também aqui

- **A armadilha bate como uma arma da categoria dela:** o dano é o da luta, dado × 4 × o valor da categoria (1, 3, 9, 27...) ÷ a proteção da parte que ela pega (a armadura dali, com o material contra o golpe; a parte nua conta um terço). O dardo e a lâmina rolam o acerto: **2d20 + 6 + o bônus da categoria, contra a Defesa sem escudo e sem aparo** (ninguém levanta o escudo para o que sai da parede). O crítico é o da luta. A ferida, a ferida grave, a queda e a morte na hora (o golpe que tira mais de metade do PV) são as da luta.
- **A gazua é a arma; a fechadura é a armadura.** Conta a diferença: **2d20 + Agilidade ÷ 10 + manha (+ o dom), contra 24 + 8 × (a categoria da fechadura − a da gazua)**. Sem gazua (o grampo, a ponta da faca), conta um degrau abaixo do Comum. É a mesma conta para desarmar (a armadilha no lugar da fechadura) e, com a Força e a arma de impacto em uso no lugar da gazua, para arrombar.
- **Achar** não tem ferramenta: é o olho. **2d20 + Percepção ÷ 10 + manha (+ o dom), contra 20 + 6 por categoria** do que está escondido (a armadilha, a passagem escondida, o fundo falso).

### 4.2 As armadilhas (lista fechada: só o que a mesa sabe rodar)

| Armadilha | O golpe | Quem pega | Como se escapa | Barulho |
| --- | --- | --- | --- | --- |
| **dardo** | 1d6, ponta | quem pisa ou quem abre | o acerto contra a Defesa sem escudo | não |
| **lâmina** | 1d10, corte | quem passa | o acerto | não |
| **fosso** | 2d6, impacto, nas pernas; quem cai fica no fundo (1 lance para tirar); da Incomum para cima, com estacas (ponta) | o primeiro da fila | Agilidade contra 20 + 6 por categoria | +1 |
| **pedra** | 2d8, impacto (cabeça 3 em 10, tronco 7 em 10) | quem passa | Agilidade contra 20 + 6 por categoria | +1 |
| **gás** | 1d6 ÷ a guarda (o amuleto, ou 0,6 da armadura do tronco, como a magia) | **todos na sala** | Vigor contra 20 + 6 por categoria: passou, a metade | não |
| **runa** | 1d8 ÷ a guarda; da Incomum para cima, **amaldiçoa** (passo 1, da categoria da runa; quebra com 7 dias longe da masmorra, a regra do lugar maldito, ou o rito) | quem pisa | o acerto contra a Firmeza | +1 |
| **alarme** | nada | ninguém | | +2 |

**Onde fica:** no chão da sala (pega o primeiro da fila que entra), na porta (pega quem abre), no guardado (pega quem abre o baú). **Cada armadilha dispara uma vez**, e fica disparada.
**Achar de passagem:** quem vai na frente rola, de graça, ao entrar na sala ou ao chegar à porta, **6 mais difícil** (oculta). Procurar (2 lances) é a rolagem inteira.
**Achada, a armadilha se resolve de quatro jeitos:** desarmar (a conta da gazua; **falhar por 5 ou mais a dispara** em quem desarmava); contornar a do chão (1 lance, sem teste; o fosso num corredor de um pede pular: Agilidade contra 20 + 6 por categoria, ou cair); dispará-la de longe, a do chão e a da porta (1 lance; faz o barulho dela); ou deixá-la. A do baú não se contorna: desarma-se, ou abre-se o baú e ela dispara.

**Medido (m2, 20.000 disparos por linha; o que a armadilha tira quando pega, de um PV de 141 do Maro, malha e elmo Comuns, Defesa sem escudo 26):**

| | Comum | Incomum | Rara |
| --- | --- | --- | --- |
| dardo | pega 57%; tira 20; nunca mata | pega 74%; tira 59; ferida em 34%, grave em 12%; mata na hora em 4% | pega 86%; tira 172; **mata na hora em 46%** |
| lâmina | pega 57%; tira 24 | pega 74%; tira 71; grave em 28%; mata em 4% | pega 87%; tira 210; mata em 54% |
| fosso | pega 19%; tira 28 | pega 43%; tira 84; grave em 30%; mata em 1% | pega 68%; tira 253; mata em 62% |
| pedra | pega 19%; tira 36 | pega 43%; tira 108; mata em 10% | pega 68%; tira 325; mata em 64% |
| gás (pela guarda) | pega todos; tira 13 | tira 48; ferida em 44% | tira 172; mata em 55% |
| runa | pega 58%; tira 37; ferida em 21%; mata em 1% | pega 74%; tira 107; mata em 13% | pega 86%; tira 316; mata em 66% |

**O mesmo contra quem veste malha Rara** (nível 50, PV 176): o dardo Raro tira 19, a lâmina 23, o fosso 28, a pedra 36, o gás 18, a runa 37. **A armadilha Rara num grupo de peças Comuns mata metade dos que pega; no grupo de peças Raras, arranha.** A Rute, de couro e sem elmo, sente a falta do elmo: a lâmina Comum tira dela 54 (e a Incomum mata em 25%).
**O gás pela guarda** é escolha minha: medido sem a guarda (passando a armadura inteira), o gás Raro matava 20% até quem veste malha Rara, e a lei do item não valia nele. Pela guarda, vale.

### 4.3 As portas e as fechaduras

| Porta | O que faz |
| --- | --- |
| aberta, ou sem porta | passa-se |
| fechada | abre-se ao passar (de graça); quem está do outro lado ouve |
| emperrada | só pela força (a conta de arrombar, com a categoria da porta) |
| trancada | a chave, a gazua (a conta da fechadura), ou a força |
| escondida | não aparece até alguém achar (procurar: 20 + 6 por categoria do segredo); achada, vira uma passagem como as outras |
| de ferro ou de pedra | escutar através dela é 4 mais difícil |

**A chave** é um item novo do Livro de Itens (tipo `chave`, com a porta ou o guardado que abre): fica com quem a pega, morre com quem morre, e abre sem teste.
**Arrombar** é 2d20 + Força ÷ 10 contra 24 + 8 × (a categoria da porta − a da arma de impacto em uso: a maça, o martelo, o malho; sem ela, o ombro conta um degrau abaixo do Comum). **Cada tentativa é 1 lance e soma 1 no alarme.** Falhar por 5 ou mais gasta 1 da arma. A porta arrombada fica arrombada.

**Medido (m2, a conta exata):**

| Quem | Com a gazua da mesma categoria | Uma abaixo | Duas abaixo | Três abaixo | Falha por 5 ou mais (mesma / uma abaixo) |
| --- | --- | --- | --- | --- | --- |
| o Maro (Agilidade 60, Leigo) | 66% | 32% | 12% | 5% | 19% / 52% |
| a Rute (Agilidade 82, Leiga) | 74% | 40% | 15% | 5% | 14% / 43% |
| o ladino Iniciante (Agilidade 70) | 77% | 44% | 18% | 6% | 11% / 38% |
| o ladino Treinado (Agilidade 80) | 86% | 57% | 26% | 9% | 5% / 26% |
| o ladino Mestre (Agilidade 90) | 93% | 70% | 36% | 13% | 1% / 16% |
| o ladino Lendário (Agilidade 100) | 98% | 81% | 48% | 20% | 0% / 9% |

| Arrombar | porta Comum, com maça Comum | Comum, no ombro | Incomum, com maça Comum | Incomum, no ombro | Rara, com maça Comum |
| --- | --- | --- | --- | --- | --- |
| o Maro e o Tomé (Força 70 e 79) | 70% | 36% | 36% | 13% | 13% |
| um bruto de Força 100 | 81% | 48% | 48% | 20% | 20% |

| Achar | Comum | Incomum | Rara | Épica | Única | De passagem: Comum, Incomum |
| --- | --- | --- | --- | --- | --- | --- |
| o Maro (Percepção 50) | 77% | 53% | 29% | 13% | 6% | 53%, 29% |
| o ladino Iniciante (Percepção 60) | 86% | 66% | 40% | 20% | 9% | 66%, 40% |
| o ladino Treinado (Percepção 60) | 91% | 74% | 48% | 26% | 12% | 74%, 48% |
| o ladino Mestre (Percepção 70) | 96% | 84% | 62% | 36% | 18% | 84%, 62% |

| Escutar (oculta) | porta de madeira (22) | de ferro (26) | mortos atrás da madeira (os mortos não respiram: 28) |
| --- | --- | --- | --- |
| o Maro | 70% | 53% | 44% |
| o ladino Treinado | 86% | 74% | 66% |

**Como ler:** o leigo abre a fechadura da categoria da gazua dele 2 vezes em 3; uma acima, 1 vez em 3, e entorta a gazua na metade das tentativas. O ladino Treinado abre a de cima mais que a metade das vezes. A fechadura duas acima da gazua quase não abre, nem para o Mestre: **a gazua da categoria é o que tranca**, como a arma. Escutar diz "silêncio", "algo se mexe" ou "vozes, de poucos" ou "de muitos", nunca o número.

## 5. O ladino

### 5.1 O 17º caminho: a manha

**Entra um 17º caminho, a `manha`** (o ofício do ladino), do tipo dos ofícios (como a caça): andar escondido, escutar, achar e desarmar armadilha, abrir fechadura (e o furto, quando entrar). Um caminho só para tudo isso, porque é uma mão só, e porque um 18º e um 19º caminho para a fechadura e para o passo macio fariam o ladino pagar três escadas pelo que o guerreiro paga numa.

| | A manha |
| --- | --- |
| a escada | a das armas: **40, 160, 500, 1.500 blocos**, vezes o talento (o Jeitoso: 27, 107, 334, 1.000; o Prodígio: 20, 80, 250, 750) |
| o feito | Mestre: **abrir uma fechadura Rara, ou desarmar uma armadilha Rara**, de verdade (não no treino); Lendário: a Épica. Como a caça pede a carcaça Rara |
| o que a mão soma | o grau em pontos (Iniciante +2, Treinado +4, Mestre +6, Lendário +8) em todo teste do ladino (seção 4) |
| o dom | **"a mão leve"**: +1 ou +2 no teste, escondido até decidir um (a regra do capítulo 10, sem mudar nada) |
| o talento | rola pelo dado do mundo como os outros; aparece depois de 20 blocos de manha |
| **como se treina** | **na masmorra:** cada bloco que fecha lá dentro, em que a pessoa andou escondida, escutou, procurou, abriu ou desarmou, soma **1 bloco de treino** (no máximo 1 por bloco, como a procura da caça). **Em casa:** `manha.py treinar N`, com uma gazua (a fechadura velha, o passo macio no pátio): bloco **pesado**, como o treino de arma |
| quanto leva | Iniciante em 20 dias de 2 blocos de treino (o Jeitoso, 14); Treinado em 80; Mestre, 250 dias e o feito |

**O que muda nos talentos:** a ficha só guarda o que não é Comum, e o sorteio de cada caminho tem a chave dele (`talento|PESSOA|manha`): **os 16 caminhos de quem já existe saem iguais**. O que muda é o sorteio do caminho do dom (agora entre 17): a gente nova de uma vila nova pode ter o dom noutro caminho. No save que já existe, `vila_teste.py masmorra` rola só o caminho novo de quem já foi rolado (um evento do gerador, que é segredo), e não mexe no dom.

### 5.2 Andar escondido e ver primeiro

É a seção 3.5. O que é só do ladino: **ir sozinho na frente** (`ir SALA escondido quem=ID`), o batedor. Sozinho, ele é o mais barulhento de um grupo de um: um ladino Treinado de couro vê primeiro uma sala de esqueletos 86% das vezes no escuro (se vê no escuro) e 66% com uma tocha. Visto, a luta abre ali, com ele na frente e o resto do grupo atrás dele, na passagem de onde veio: é o risco da manha (o ladino de couro na frente de uma sala inteira).

### 5.3 O golpe pelas costas (proposta)

**O que a luta e a caça já fazem:** quem vê primeiro ataca com o outro lado surpreendido, e quem foi surpreendido perde o primeiro turno (a luta de hoje). Isso já é o golpe pelas costas do grupo. Medido (m3, 500 lutas, nível 50, tudo Raro, o ladino de espada e couro contra o gêmeo de espada, malha e escudo, colados): **sem surpresa o ladino vence 19%; surpreendendo, 32%.**
**O que eu proponho a mais, só para quem tem a manha:** de **Treinado** em diante, o primeiro golpe de corpo a corpo da luta contra quem foi surpreendido tem **+4 no acerto e rola os dados 3 vezes** (o bote do bicho, sem derrubar). Medido (m3):

| O ladino surpreende... | sem o golpe | +4, dados 2 vezes | **+4, dados 3 vezes** | +8, dados 3 vezes |
| --- | --- | --- | --- | --- |
| o gêmeo (tudo Raro) | 32% | 34% | **43%** | 49% |
| o de arma Épica | 8% | 9% | **15%** | 15% |
| o de conjunto Épico | 7% | 7% | **12%** | 12% |
| o gêmeo, o ladino de adaga | 14% | 14% | **19%** | 25% |

**Dentro da lei:** o golpe vale cerca de 11 pontos contra o gêmeo, o mesmo que o Grande Dom (de 54 a 64%, capítulo 10), e quem tem a arma uma acima segue vencendo 85% mesmo pego pelas costas. Por isso escolhi +4 e 3 vezes, e não +8 (que dá 18 pontos). Mexe em três lugares pequenos: `tabelas.COSTAS = dict(desde=4, acerto=4, dados=3)`, a ficha (`pessoas.ficha` leva a manha), e um ramo no `luta._golpe_especial`. **A luta de quem não tem manha de Treinado é a de sempre, dado por dado.** É a pergunta 3.

### 5.4 A gazua

| | A gazua |
| --- | --- |
| o que é | uma peça do Livro de Itens (tipo novo, `gazua`), com categoria e durabilidade (Comum 10, Incomum 20...). Não se veste: vai na guarda, e o teste usa a melhor que a pessoa leva |
| quem faz | a forja, como a adaga: **1 de metal** da categoria; 1 bloco a Comum, 3 a Incomum, 9 a Rara; do Épico para cima, matéria Rara e um núcleo (a lei da forja) |
| quanto vale | o da adaga (1 unidade de matéria): Comum 10, Incomum 60, Rara 360. A loja a vende e a compra a 40% (ter gazua não é crime: é ferramenta de serralheiro) |
| gasta | falhar por 5 ou mais tira 1 de durabilidade; a zero, quebra. Conserta-se na forja |

### 5.5 O furto: fica escrito, e entra na etapa 3

A regra está pronta: `manha.py furtar ALVO` (na vila, de dia, alvo com nome, uma tentativa por alvo por dia): 2d20 + Agilidade ÷ 10 + manha (+ o dom) contra 20 + Percepção ÷ 10 da vítima, mais 4 se ela é guarda ou mercador. Passou: leva 1d6 × (1 + metade do grau de manha) de prata, até o que ela tem. Falhou por 5 ou mais: **é crime, como o veneno de lâmina**: devolve, paga o triplo ao caixa da vila (sem prata: 3 dias preso, com os atos da vila recusados). Falhou por menos: nada.
**Por que não agora (a conta):** o ladino Iniciante passa contra a Dalva 77% das vezes e é pego em 11%; leva 7 de prata em média; com a pena do triplo, ganha cerca de 3 por tentativa. Com onze pessoas de nome na vila e uma tentativa por pessoa por dia, são cerca de **34 de prata por dia**, até esvaziar a bolsa da vila inteira (perto de 570, que nada repõe: na vila de teste ninguém trabalha nem ganha), e o Treinado tira o dobro. Nesta etapa a vítima não lembra, o guarda não desconfia e a vila não tem justiça; isso é a etapa 3 (a gente com memória e rotina). Lá, o furto entra com a meta "rende, com a pena contada, menos que a diária". É a pergunta 1.

## 6. O tesouro e a economia

### 6.1 O que cada masmorra guarda

- **Prata que já existe no mundo.** O gerador da região (etapas 3 e 7) a tira da prata da história (quem morreu ali, o que o senhor antigo escondeu, o que o bando roubou); na vila de teste, o comando que acrescenta a masmorra a põe por um evento do gerador, como pôs o tesouro da toca. Depois disso, **nenhuma prata nasce**: a masmorra só perde a que o grupo leva (e ganha a dos mortos que caem nela, que é de quem já existia).
- **Peças do Livro de Itens**, da categoria do nível; a da sala escondida e a do chefe, uma acima. No mundo da etapa 3, estas são peças contadas (das 60 Raras, 12 Épicas, 4 Únicas do Dia 1), com a história de quem as perdeu ali.
- **Às vezes malditas:** uma em seis peças velhas é uma peça cujo encanto falhou por 10 ou mais (a origem das malditas que o capítulo 12 já diz). A loja não a compra, e só quem a lê sabe.
- **Poções** (bens) da categoria do nível, uma ou duas por nível.
- **O núcleo do chefe do fundo**, do Épico para cima, contado na conta do mundo (seção 2.4).
- **A matéria da mina:** o minério da categoria do nível, pela regra da coleta (o teto, a volta lenta, a mão que a matéria pede). É o "material de masmorra" que o `PROJETO.md` pede para a primeira peça Rara.
- **O despojo** de quem morre lá dentro, como na caça: a sucata do povo, o osso do morto, o couro do bicho, **na categoria de quem morreu** (ver 6.3).

### 6.2 Quanto (a tabela do gerador; chute calibrado só na cripta de teste)

| | Comum | Incomum | Raro | Épico | Único |
| --- | --- | --- | --- | --- | --- |
| prata em cada sala de tesouro (2 a 4 por nível) | 20 | 80 | 320 | 1.280 | 5.120 |
| peças por nível | 1 a cada 3 salas, da categoria; a da sala escondida e a do chefe, uma acima | | | | |
| poções por nível | 1 a 2, da categoria (do Épico para cima, elixir contado) | | | | |
| núcleo | | | | o do chefe do fundo | o do chefe do fundo |

A prata sobe 4 vezes por categoria (a peça sobe 6): o tesouro de uma masmorra alta é grande, mas não é a prata de uma cidade. Uma ruína de três níveis, do Incomum ao Épico, com três salas de tesouro por nível, guarda cerca de 5.000 de prata: um décimo da prata das lojas da região do `PROJETO.md` (perto de 50.000: 5 de prata por pessoa, a conta do `mercado.funda`, para 10.000 pessoas). **A soma das 8 masmorras da região tem de caber no orçamento da prata do mundo; isso é meta da etapa 7** (o gerador da história), e eu não medi.

### 6.3 A divisão, e o que impede a mina

**A divisão:** a prata e os bens que se pegam repartem-se **em partes iguais entre quem está na descida** naquela hora (a regra do despojo: quem vai junto tem parte, não é mão de graça). A peça fica com quem a pega (por padrão, quem comanda); de quem é a parte dos outros nas peças, é conversa de cena. O que ficou com um morto não é achado (a regra de hoje: o Mestre registra por evento).

**As metas que impedem a mina:**

| O caminho de renda | O que o tranca | A meta (seção 12) |
| --- | --- | --- |
| descer de novo na masmorra limpa | o tesouro não volta; o morto não volta sem chefe vivo; o rato volta em meses | **MA4**: depois da primeira limpeza, a descida rende menos de 0,25 diária por dia de trabalho, em 60 dias |
| o primeiro assalto | a prata é a que o gerador pôs, uma vez | **MA4**: em 60 dias de vida, a masmorra de teste rende menos de 1 diária por pessoa por dia, contando o primeiro assalto |
| vender o que se acha | a loja paga 40% pelas peças, fica farta, não compra a maldita, e tem 2.000 de prata contada | as metas do mercado de hoje (sem mudar nada) |
| **o despojo de quem tem a categoria mudada** | **hoje o `criaturas.despojo` usa a tabela da espécie, sem olhar a categoria**: o cavaleiro da cova feito Comum renderia 3 de metal Raro (cerca de 194 de prata na loja), e o esqueleto feito Raro renderia sucata Comum | **o despojo segue a categoria de quem morreu** (a matéria na categoria dele, até a Rara). Na conta da masmorra; a da caça segue como está (lá ninguém muda de categoria). **MA5** confere |
| o minério da mina | é coleta: o teto, a volta lenta (0,4% por dia), a mão que pede | as metas da coleta de hoje (K1 a K4), com a mina no lugar do ermo |
| a gazua e a tocha na loja | bens e peças como os outros (a tocha a 1; a gazua a 10) | MA9 (forjar gazua para a loja não é mina: é a adaga, com 1 de metal) |

**Medido (rascunho, m4):** o grupo da vila que limpa a cripta de teste leva, em média, **58 de prata** (de 0 a 80, conforme acha o nicho escondido e abre o baú), a maça Comum, o escudo do guardião (Incomum), a gazua Incomum (se acha o nicho: em 34% das vidas sem ladino, 48% com o Quim) e uma poção. Na loja, as três peças dariam 12, 72 e 24. É cerca de 170 de prata para três pessoas, **uma vez**: nos 60 dias, cerca de 0,9 de prata por pessoa por dia (um quarto da diária). Depois, a cripta só tem os ratos que voltarem (a regra da caça: o casal de fora em média em 60 dias), e a conta dá menos de 0,05 diária por dia. É o mesmo desenho do covil de hoje (o primeiro assalto rende o tesouro; os seguintes, quase nada).

## 7. A vila de teste: a Cripta da Cova Velha

### 7.1 O que ela é

O Maro e os seus já limparam a Cova Velha (os 3 esqueletos e os 2 corpos-secos estão em 0 no save de hoje). **Os mortos subiam de algum lugar:** sob o mausoléu quebrado há uma escada. A cripta tem 7 salas num nível só, Comum (grau E), com o guardião no fundo. Quem sabe dela: o povo diz que "os mortos da Cova Velha subiam de uma escada"; o resto é do Mestre.

```
            Pedra Rasa -- 1 bloco -- a Cova Velha (o mausoléu quebrado: a boca da cripta)
                                         |
                                  [1] a escada (vazia, escura)
                                         |  porta de madeira, fechada
                                  [2] o corredor dos nichos (corredor de 1)
                                      2 corpos-secos nos nichos, à toa
                                      dardo Comum no chão, no meio
                                  /                        \
          [3] o ossário (sala aberta)                [4] a capela (sala de 2)
              3 esqueletos, à toa                        4 ratazanas, dormindo (o ninho: cria)
              10 de prata na tigela das oferendas         o baú das oferendas: fechadura Comum, dardo Comum na fechadura;
                                                          25 de prata, a maça Comum, 1 poção de cura Comum, a chave de ferro
                                  \                        /
                                  [5] os degraus (corredor de 1)
                                      a runa Comum no chão; a porta de ferro: fechadura Incomum (a chave de ferro a abre)
                                         |
                                  [6] a câmara do guardião (sala de 2)
                                      o guardião da cripta (chefe) e 2 esqueletos
                                      o sarcófago: fechadura Comum; 30 de prata e o escudo do guardião (Incomum)
                                      uma passagem escondida (Incomum) para
                                  [7] o nicho escondido (corredor de 1): 15 de prata e a gazua Incomum

            os que vagueiam: 1 corpo-seco e 3 ratazanas · o alarme começa em 0 · a prata da cripta: 80
```

**Por que assim:** a maça (que o esqueleto pede, porque a ponta e o fio passam entre os ossos) está no meio do caminho, no baú, para quem procura; a chave da porta de ferro também, e quem não a acha tem a gazua (Incomum: o Maro abre 32% das vezes com uma gazua Comum) ou a força (36% com a maça, 13% no ombro, e o barulho); o corredor dos nichos ensina o corredor de um; o ossário aberto ensina a puxar para o corredor; a capela ensina o baú com armadilha; a runa e a porta de ferro avisam que o fundo é outra coisa; o nicho escondido paga quem procura (e dá a gazua Incomum a quem quiser ser ladino).
**A cor para o Mestre (sem regra nova):** a Espada do Guardião, a maldita que o Maro guarda, é do guardião da cripta. A maldição dela segue quebrando como hoje (devolvê-la à Cova Velha).

### 7.2 O comando que só acrescenta

```
python3 vila_teste.py masmorra PASTA
```

Só por eventos, sem recriar nada; recusa rodar duas vezes, e recusa a vila sem a etapa da magia (a cripta é sob a Cova Velha):
1. **A Cripta da Cova Velha**: a masmorra (vizinha de Pedra Rasa, a 1 bloco), as 7 salas, as portas, as armadilhas, quem mora em cada sala, o guardião, os vagantes, a prata (80, nas salas), as peças (a maça, a chave de ferro, o escudo do guardião, a gazua Incomum) e a poção. **Um evento do gerador, que é segredo** (vai ao SÓ O MESTRE do RETOMAR).
2. **Quim, o ladino da vila** (o sobrinho do Lino, que abre trinco e anda calado): nível 14, manha de Iniciante (os 40 blocos que explicam a mão), adaga e couro Comuns, uma gazua Comum, 10 de prata. Nasce com o talento e o dom rolados.
3. **A manha (o 17º caminho)** de quem já tinha o talento rolado: só esse caminho, um evento do gerador (segredo).
4. **A loja ganha a tocha** (bem; base 1; o estoque no alvo, a produção igual ao consumo) e **uma gazua Comum na prateleira**.
5. A linha que o povo conhece da cripta, para a mesa.

A prata que nasce: 80 (a cripta) e 10 (o Quim). Nada mais muda: a gente, os itens e o tempo de antes seguem como estavam.

### 7.3 Medido (rascunho do robô, m4: 300 vidas por linha, até 20 dias; o grupo desce quando todos estão inteiros)

| Quem desce, e como | Limpa a cripta | O Maro morre | Morre alguém | Onde se morre |
| --- | --- | --- | --- | --- |
| o Maro sozinho (recua abaixo de 30% do PV) | 0% | **96%** | 96% | no corredor dos nichos (163 de 288) e no ossário (123) |
| Maro, Tomé e Rute, o Maro na frente, sem cautela | 89% | 19% | 22% | |
| os três, o Maro recua abaixo de 30%, puxa os esqueletos para o corredor | 91% | 15% | 18% | na câmara do guardião (50 de 62) |
| o mesmo, **e volta para casa quando chega ao guardião com alguém abaixo de 75% do PV** (o jogador prudente) | **91%** | **10%** | **12%** | na câmara do guardião (46 de 51) |
| o prudente, com Anselmo (quatro) | 95% | 8% | 10% | |
| o prudente, com o Quim na frente (ele procura e desarma; atrás na luta) | **97%** | **4%** | 9% | |
| o prudente, com o guardião de espada e escudo (no lugar do montante) | 95% | 7% | 10% | |
| o prudente, com o guardião sem as fases | 92% | 13% | 15% | (as fases não são o que mata: é o montante) |

**Como ler:** a cripta não é para o Maro sozinho. Com Tomé e Rute ela é dura e justa: o perigo mora no fundo (nove em dez mortes são na câmara do guardião), e o jogador que descansa antes do chefe morre metade do que morre o afoito. O ladino na frente acha 2,6 armadilhas por vida (o grupo sem ele, 1,0), dispara 0,5 (sem ele, 2,0), e corta a morte do Maro pela metade. Por vida o grupo luta 5 vezes, cruza uma vez com o que vagueia, gasta 3 tochas e passa de 5 a 6 blocos entre a ida, a descida e a volta.

## 8. Uma cena jogada

(As duas lutas são do `luta.py` de verdade, com semente fixa: `m6_cena.py`, saída em `m6_saida.txt`. Os dados de fora da luta são de exemplo.)

**Dia 9, alvorada.** O Maro (PV 141, 3 tochas compradas a 1 de prata) desce com Tomé, Rute e Quim: `masmorra.py descer cripta com=tome,rute,quim ordem=quim,tome,eu,rute luz=tocha quem_luz=rute`. A ida é 1 bloco (a Cova Velha); a tocha da Rute alumia a escada e uma porta de madeira. "Escutar a porta" custa 1 lance: `masmorra.py escutar corredor`, e a mesa mostra só "rolagem oculta" (no SÓ O MESTRE: Quim, 2d20 + 6 + 2 = 25 contra 28, porque os mortos não respiram: falhou, e ele ouve silêncio). Quim abre a porta; o corredor dos nichos é de um só. De passagem, ele olha o chão (oculta: 31 contra 26) e o comando **para**: "na laje do meio, um furo na parede: um dardo". O jogador escolhe `masmorra.py desarmar` (a gazua Comum contra o dardo Comum: 77% para o Quim): 2d20 + 7 + 2 = 30 contra 24, passa. Logo adiante, dois corpos-secos nos nichos, à toa; o grupo não andava escondido (Tomé e Maro de malha), os mortos notam, e o comando para no encontro. Ninguém é surpreendido. O jogador põe o Quim para trás (`masmorra.py ordem tome,eu,quim,rute`, sem lance) e ataca: a luta abre perto, num corredor de um, com Tomé na frente.

**A luta** (`masmorra.py luta "Maro: atacar"`): na primeira rodada Tomé abre o tronco do primeiro corpo-seco (103 de 162, ferida grave) e a Rute, por cima do ombro, acerta a cabeça dele (106: se desfaz); na segunda, três flechas dela levam o segundo (42, 106 na cabeça, 85 nas pernas). Duas rodadas, ninguém da casa ferido. As contas: os dois saem da conta da sala, o despojo é 1 de osso Comum de cada (de metade ao inteiro), o alarme vai a 1, e o lance da luta soma: **4 lances dentro, faltam 8 para o bloco fechar**. No ossário (sala aberta), três esqueletos; o grupo recua um passo e espera na boca do corredor (`atacar inicio=perto`, do corredor): um de cada vez. Na capela, os quatro ratos dormem, e o grupo os pega surpreendidos. O Quim procura o baú (2 lances) e **o primeiro bloco fecha** ali, ao meio-dia: a tocha da Rute se gasta (restam 2), e o mundo rola o que vagueia (1 em 6, mais 10 pontos por ponto do alarme, que está em 3: 47%; não veio nada). Depois, o dardo do baú achado e desarmado, a chave de ferro, a runa achada de passagem e contornada, a porta de ferro aberta com a chave. O alarme ainda está em 2: os de lá estão alertas, e Tomé, na frente, testa a atenção (oculta: passou): ninguém é surpreendido.

**A câmara do guardião** (sala de 2; a rolagem do chefe e a frase dele são do Mestre, que a lê ao abrir a porta): o guardião e dois esqueletos. Na primeira rodada o Maro o acerta no tronco (18), o Quim tira um crítico (30, ferida), a Rute duas flechas (36 e 9), e com 74 de 158 o guardião **muda de fase**: "bate o pé: os ossos da sala se levantam", dá o brado (os seus benzidos por 3 rodadas) e a luta para e pergunta; ainda não há morto no chão para erguer. O esqueleto 1 tira 30 do Maro. Tomé tira um crítico de 54 que **desfaz a placa** do guardião, e o golpe seguinte o derruba. Na segunda e na terceira rodada caem os esqueletos (um crítico do Maro, de 87, nas pernas). **A casa fica com o campo em 3 rodadas**; o Maro com 107 de 141. A cripta é limpa pela primeira vez (`limpa: Dia 9, Maro, Tomé, Rute e Quim`), o sarcófago abre (fechadura Comum, gazua do Quim), e a prata (30) reparte-se em quatro: 8, 8, 7, 7. O Quim procura a sala (2 lances; oculta: passou) e acha a passagem do nicho; o segundo bloco fecha ali, às 16h (a segunda tocha). No nicho, mais 15 de prata e a gazua Incomum. `masmorra.py voltar` refaz as 5 salas até a escada (5 lances), `sair` fecha o terceiro bloco e faz a volta: o grupo entrou às 8h, sai às 20h, e chega a Pedra Rasa à meia-noite, com as 3 tochas gastas e cada um com a sua parte.

## 9. Os ganchos

- **A janela do mundo (etapa 5).** A primeira limpeza é a primeira vez que o chefe do fundo morre: as contas da luta põem na masmorra `limpa = {dia, quem, chefe}`, num efeito do mesmo evento. A janela, quando existir, lê esse evento e conta a todos. Até lá, a mesa da vila diz "contam na vila: a Cripta da Cova Velha foi limpa por Maro e os seus, no Dia 9". O `PROJETO.md` (seção 4) diz que a peça Única se tranca pelo "núcleo de chefe maior, ou primeira limpeza": aqui as duas coisas são uma só, o núcleo é o do chefe do fundo, e quem limpa primeiro é quem o leva; uma limpeza depois (se um chefe novo chegar) dá o núcleo do novo, e não dá janela.
- **Os rivais e as guildas (etapa 5).** Os rivais escolhem nas mesmas masmorras que o personagem vê. Deixo os dados e o lugar da conta: a força de cada masmorra (o grau de cada nível, o chefe, o tesouro que resta) e uma função que aplica a descida de longe (o tesouro passa ao rival; quem morre sai da conta; o rival que morre lá deixa as peças na sala, soltas, para quem achar; a `limpa`, se foi a primeira). A conta rápida do rival, calibrada contra a luta, é da etapa 5.
- **O gerador da história (etapa 7): as ruínas são as masmorras.** O `masmorra.gera` recebe do gerador da história a origem (quem a fez, o que a derrubou, quem morreu lá), as peças contadas com a história delas ("perdida por fulano quando o teto caiu, no ano 812"), a prata (do orçamento da história) e o chefe. A masmorra guarda o texto da origem; a gente do mundo conta pedaços dele (etapa 3).

## 10. Onde toco o outro projeto (os dragões e os povos)

**O que eu preciso do projeto B:**
1. **Quem vê no escuro.** A pessoa cujo povo vê no escuro leva o traço `noturno` (o da luta de hoje), e a masmorra lê só isso: anda, procura, abre e luta no escuro sem pena, e o grupo em que todos veem no escuro dispensa a luz (e a pena de −6 que a luz põe no andar escondido). **Ver no escuro não soma na luta contra quem tem luz:** tira a pena do escuro e mais nada.
2. **O tamanho do povo.** O pequeno toma meia vaga do corredor (a regra do bicho, 6.5): dois pequeninos lado a lado num corredor de um. A masmorra não muda nada; quem faz a ficha do povo (o projeto B) faz isso valer para gente.
3. **Os bônus do povo nos testes do ladino** (o passo leve do pequenino no andar escondido, o olho do elfo no achar, o anão que sente a pedra na passagem escondida e na armadilha de pedra): um número por povo e por teste, que o `manha.py` soma. **Teto: +2 por teste** (um grau de maestria, o mesmo do Grande Dom), para o povo pesar menos que uma categoria de peça, como a lei pede. O projeto B mede.
4. **Os dragões como chefes de covil:** o dragão é o chefe do fundo de uma masmorra de molde `covil` (a sala dele guarda `chefe: {qual}`), e o tesouro dele é o tesouro da masmorra (a regra da seção 6).

**O que eu ofereço ao projeto B:**
1. **O covil do dragão é uma masmorra:** a boca (sala de 2), as galerias (corredores de 1, onde o dragão enorme toma 3 vagas, luta apertado com −4 e não voa: a regra 6.5 e o traço "voa" de hoje), e a câmara do tesouro (aberta: lá ele voa e sopra). Ganha de graça o escuro, o alarme, o que vagueia (os que comem as sobras), a divisão do tesouro, a primeira limpeza e a janela.
2. **Roubar o covil com o dragão dormindo** (o "roubar o covil do dragão" que o `PROJETO.md` promete para esta etapa): a sala do tesouro com `atento = −1` (dormindo: −6 na Percepção dele). Cada lance passado ali é um teste de andar escondido do mais barulhento que está na sala; **pegar um punhado** (1 lance) leva a sexta parte da prata, ou uma peça. Falhou um teste: ele acorda, e o encontro é o de sempre (ele não é surpreendido; o grupo pode ser), ou a fuga pelas galerias. A conta (m2): um ladino Treinado de couro (+12), contra um dragão de Percepção 90 dormindo (contra 23), passa 89% por lance se vê no escuro e 70% com luz; seis punhados seguidos sem acordá-lo, **49% no escuro, 12% com luz**. A Percepção do dragão e se a câmara tem luz (o fogo dele) são do projeto B.
3. **O escuro tem valor medido** (seção 3.3: de 81% para 29%): é isso que o ver no escuro do povo compra na masmorra, sem somar na luta contra quem leva tocha.
4. **O caminho da manha está aberto a todo povo**; se o projeto B quiser um povo jeitoso nela (o pequenino), é o talento (a pressa), não um bônus a mais.

**Os arquivos que os dois projetos tocam** (estado.py, pessoas.py, luta.py, tabelas_mundo.py, vila_teste.py) ficam com um construtor só, na onda do alicerce e na da integração (seção 13).

## 11. O estado

**Os campos novos** (todos com valor padrão: o save antigo abre igual, e nada do que existe muda de sentido):

| Onde | Campo | Padrão |
| --- | --- | --- |
| lugar `masmorra` | `molde`, `niveis`, `entrada`, `portas`, `alarme`, `vagantes`, `limpa`, `origem` (seção 2.1) | o lugar sem `tipo: masmorra` não é masmorra |
| lugar `sala` | `masmorra`, `nivel`, `largura`, `acesa`, `cat`, `atento`, `armadilhas`, `guardado`, `segredos`, `chefe`, `sobre` (e `bichos`, `teto`, `estoque`, `coleta`, que já existem) | aberta, escura, à toa, sem nada |
| pessoa | `maestria.manha`, `treino.manha` (a manha entra em `OFICIOS`), `talento.manha`, `dom.manha` | Leigo, 0 blocos, Comum, sem dom |
| pessoa | `marca.masmorra` (a descida aberta: `{masmorra, sala, com, ordem, lances, luz: {tipo, quem}, fase, encontro, luta, lutas, caminho, manha_bloco}`; em quem vai junto, `{de: quem comanda}`) | sem descida |
| pessoa | `marca.mapa.MASMORRA` (as salas, as passagens e as armadilhas que a pessoa viu) · `marca.feito_manha` (a maior categoria aberta ou desarmada de verdade) | nada visto · sem feito |
| item | tipo `gazua` (categoria, durabilidade; vale pela matéria: 1) · tipo `chave` (`abre`: a porta ou o guardado) | |
| bem | `tocha` (na carga e no estoque) | |

**Os eventos:** um tipo novo, `masmorra` (descer, andar, escutar, procurar, abrir, desarmar, a armadilha que dispara, pegar, voltar, sair, as contas da luta, e a vida da masmorra na virada). O treino em casa é o evento `treinar` de hoje. Quando o furto entrar, `furto`.
**Os efeitos:** **nenhum verbo novo.** Tudo é o que o gravador já sabe: `['lugar', SALA, 'bichos.esqueleto', 'soma', -2]`, `['lugar', MASMORRA, 'portas.cripta_4|cripta_5', 'poe', {...}]`, `['lugar', SALA, 'armadilhas', 'poe', [...]]`, `['lugar', SALA, 'guardado', 'poe', {...}]`, `['lugar', SALA, 'vizinhos', 'poe', [...]]` (a passagem achada), `['lugar', MASMORRA, 'alarme', 'poe', 2]`, `['lugar', MASMORRA, 'limpa', 'poe', {...}]`, `['estoque', SALA, 'prata', 'soma', -30]` com `['pessoa', P, 'moedas', 'soma', 8]`, `['pessoa', P, 'carga.tocha', 'soma', -1]`, `['pessoa', P, 'marca.masmorra', 'poe', {...}]`, `['item', I, 'dono', 'poe', P]`. O `_lugar_erro` passa a conferir os campos novos (o formato de cada um), como confere o covil.
**Os invariantes novos** (`estado.valida`; o `fecha` recusa com qualquer um quebrado): toda sala é de uma masmorra que existe e está num nível dela; os vizinhos de uma sala são salas da mesma masmorra (a entrada liga ao lado de fora pela masmorra); toda porta é de uma passagem que existe; toda chave abre uma porta ou um guardado que existe; o chefe de uma sala é um chefe que a tabela conhece; quem comanda uma descida está numa sala daquela masmorra; quem foi junto aponta para alguém vivo com a descida aberta; ninguém está numa descida e numa saída de caça ao mesmo tempo.
**A morte lá dentro** é a regra de hoje: as peças soltas na sala, a carga e a prata no estoque da sala; quem ia junto e morre sai da descida; quem comanda e morre solta quem ia junto (eles saem sozinhos: é cena do Mestre, como na caça).
**`estado.fora`** passa a ler também a descida: a pessoa está na sala onde o grupo está. É a única mudança de sentido no gravador, e é o que faz a morte, a mesa e a recusa dos atos da vila valerem lá dentro sem mais nada.

## 12. As metas do banco (`provas_masmorra.py` e `provas_manha.py`; o `provas_mundo.py` roda os dois)

| Meta | O que se mede | Faixa | Como se mede | Rascunho (medido aqui) |
| --- | --- | --- | --- | --- |
| **MA0** a pessoa comum é a de hoje | os bancos de antes; a luta sem ninguém de manha Treinado; os talentos dos 16 caminhos; a vila sem masmorra | igual | `provas.py 600` (114 de 114, os mesmos números com semente fixa); `provas_mundo.py`; `estresse.py 1500` (a mesma primeira linha: 721, 717, 61, 1); 10 dias de rotina com o módulo ligado e desligado: o mesmo estado | (a medir) |
| MA1 o tempo | N lances andam ⌈N ÷ 12⌉ blocos pelo `ato.passa`, mais a ida e a volta; cada bloco gasta uma tocha de quem leva a luz; acabadas as tochas, a luta seguinte tem o escuro | sempre | descidas com lances contados, em 20 mundos | |
| MA2 a luz e o escuro | o grupo da vila contra seis esqueletos, sala aberta | com luz 70 a 90%; no escuro 15 a 40% | 600 lutas cada | 81% e 29% |
| MA3 quem vê primeiro | o mesmo grupo, surpreendendo e surpreendido | +10 pontos ou mais; −15 ou mais | 600 lutas cada | 90, 77 e 48 |
| **MA4** não é mina | a casa da vila (Maro, Tomé, Rute, prudente) vive 60 dias ao lado da cripta: desce quando os três estão inteiros, vende o que acha | por pessoa e por dia de vida, no máximo 1 diária; depois da primeira limpeza, menos de 0,25 por dia de trabalho; a prata do mundo fecha | 24 vidas; o robô vive de verdade (come, dorme, paga a cama) | cerca de 0,25 e menos de 0,05 |
| MA5 o despojo pela categoria | o cavaleiro da cova Comum rende metal Comum; o esqueleto Raro, sucata Rara | sempre | as contas de lutas postas à mão | |
| **MA6** a cripta de teste | o robô de verdade, 300 vidas | o prudente de três limpa em 80% ou mais, e o Maro morre em 15% ou menos; sozinho, morre em 70% ou mais; com o ladino, morre menos que sem | pelo `masmorra.py` | 91% e 10%; 96%; 4% |
| MA7 a armadilha pelo item | o dardo Raro em quem veste Comum, e em quem veste malha Rara; o Comum em quem veste Comum | mata 35% ou mais; tira menos de 15% do PV; nunca mata de PV cheio sem crítico | 20.000 disparos | 46%; 11%; 0% |
| MA8 a gazua pelo item | o leigo de Agilidade 60: a da mesma categoria, uma acima, duas acima; o Mestre, duas acima | 55 a 75%; 20 a 40%; até 15%; menos de 40% | a conta exata e 6.000 tentativas | 66, 32, 12; 36 |
| MA9 a gazua na loja não é mina | o robô de loja do mercado, com a gazua na lista | a meta do mercado de hoje: no máximo 6 de prata por dia nos 5 primeiros dias | 30 vilas | |
| MA10 o ladino aprende fazendo | 40 blocos fazem o Iniciante (Jeitoso 27, Prodígio 20); o Mestre pede o feito; o bloco da masmorra dá no máximo 1 de treino; o treino em casa pede gazua | sempre | robôs de treino | |
| MA11 o golpe pelas costas (se entrar) | o ladino Treinado contra o gêmeo, surpreendendo; contra a arma uma acima | +5 a +15 pontos; a arma acima vence 80% ou mais | 4.000 lutas | +11; 85% |
| MA12 o que vagueia e o descanso | a chance por bloco; dormir com e sem vigia | 1 em 6 + 10 por alarme (±2 pontos); sem vigia, surpreendido sempre; com vigia, nunca | 6.000 blocos | |
| MA13 a memória | 365 dias da cripta limpa, sozinha | o morto não volta sem chefe; o rato volta e não passa do teto; o bando de fora chega 120 dias depois de o nível ficar vazio; o tesouro não volta; a prata fecha | 20 mundos | |
| MA14 o mapa é segredo | a mesa só mostra o que o grupo viu; as ocultas não vão à parte pública; o gerador vai ao SÓ O MESTRE; a mesma descida, com e sem o chefe atrás da porta, dá o mesmo texto até a porta abrir | sempre | três mundos com o dado preso | |
| MA15 a vila de teste | `vila_teste.py masmorra` numa cópia do `ensaio/`: só eventos; recusa a segunda vez; estado inteiro; a prata nova é 90; nada de antes muda | sempre | a soma dos arquivos de antes | |
| MA16 as recusas | ir à sala que não é vizinha; abrir com gazua sem gazua; procurar no escuro; pegar com inimigo de pé; descer com saída de caça aberta; os atos da vila com a descida aberta; duas descidas; a luta aberta tranca a descida | todas, com a frase, antes de gastar | à mão | |

## 13. A construção

### 13.1 Os arquivos novos

| Arquivo | O que expõe | Linhas (chute) |
| --- | --- | --- |
| `tabelas_masmorra.py` | o lance (`LANCE`, `LANCES_BLOCO`, `CUSTO`); a luz (`TOCHA_BLOCOS`, `LUZ_MANA_BLOCO`, `ESCURO_ANDA`, `LUZ_ESCONDIDO`); `ATENTO`; `ARMADURA_ESCONDIDO`; o alarme e o que vagueia (`ALARME`, `VAGA`); `ARMADILHAS` (a lista fechada), `ARMADILHA_ACERTO`, `ESQUIVA`, `PASSAGEM`; `PORTAS`; `MOLDES`; `TESOURO`; `MEMORIA` | 200 |
| `masmorra.py` | o lugar e a sala (ler, dizer); a descida (`descer`, `ir`, `escutar`, `procurar`, `abrir`, `desarmar`, `contornar`, `disparar`, `atacar`, `esperar`, `recuar`, `luta_roda`, `acerta`, `pegar`, `descansar`, `ordem`, `luz`, `voltar`, `sair`, `larga`); o gerador (`gera`); os ganchos do mundo (`virada`, `mesa`, `so_mestre`, `retomar`); os ganchos das etapas 5 e 7 (`forca`, `desce_longe`); o `main` | 900 |
| `tabelas_manha.py` | os testes do ladino (`ACHAR`, `GAZUA`, `SEM_GAZUA`, `FALHA`, `ARROMBAR`, `ESCUTAR`, `ESCONDIDO`); o feito; a gazua (`MATERIA_GAZUA`); o furto (para a etapa 3) | 60 |
| `manha.py` | `testa` (o dado do ladino: o `teste.rola` com a mão, o dom escondido e o bônus do povo do projeto B), `gazua_de`, `escondido` (o mais barulhento do grupo), `sobe` (a mão e o feito), `treinar`, `ver`; os ganchos `voce` e `mesa` (a mão do ladino); depois, `furtar` | 300 |
| `provas_masmorra.py` | MA0 a MA7, MA12 a MA16 | 700 |
| `provas_manha.py` | MA8 a MA11 | 250 |

### 13.2 Os arquivos que mudam

| Arquivo | O que muda |
| --- | --- |
| `estado.py` | `fora` lê a descida; `_morre` solta quem ia junto na descida; `_lugar_erro` confere os campos da masmorra e da sala; `valida` ganha os invariantes da seção 11; `TIPOS_ITEM` ganha `gazua` e `chave`; a tocha é bem conhecido |
| `tabelas_mundo.py` | `EVENTOS` + `masmorra`; `MODULOS` + `masmorra`, `manha`; `OFICIOS` + `manha`; `BENS` + `tocha` |
| `tabelas_talento.py`, `talento.py` | o 17º caminho em `OFICIOS`, `DOM_NOME` ("a mão leve"), `O_QUE`; `talento.rola_caminho` (rola um caminho só, para o save que já existe) |
| `itens.py` | a gazua (como a adaga) e a chave |
| `tabelas_oficio.py`, `oficio.py` | forjar a gazua |
| `tabelas_mercado.py`, `mercado.py` | a tocha (bem, base 1; o povo gasta 0,01 por pessoa por dia, chute) e a gazua na prateleira (peça, pela matéria) |
| `tabelas.py`, `pessoas.py`, `luta.py` | o golpe pelas costas (se o jogador quiser): `COSTAS`, a ficha leva a manha, um ramo no `_golpe_especial` |
| `tabelas_criaturas.py` | o guardião da cripta em `CHEFES` |
| `turno.py` | `secreto` pega o evento que cria a masmorra e o que põe armadilha, guardado e segredo |
| `vila_teste.py` | o comando `masmorra` (seção 7.2) |
| `provas_mundo.py` | roda os dois bancos novos |
| `REGRAS.md`, `GUIA_VILA.md`, `MUDANCAS.md`, `LEIA.md`, `PROJETO.md` | o capítulo 17 (as masmorras) e o 18 (o ladino); o guia da cripta; a linha da etapa |

Somando, perto de **2.400 linhas novas e 250 mudadas**: o motor cresce uns 15%.

### 13.3 Como repartir (com o projeto B, sem dois construtores no mesmo arquivo)

1. **Onda 1, o alicerce** (um construtor, para as duas metades): `estado.py`, `tabelas_mundo.py`, `tabelas_talento.py` e `talento.py`, `itens.py`, `pessoas.py`, `luta.py` e `tabelas.py`, `turno.py`. Entrega o vocabulário (os campos novos e os invariantes, a descida no `fora`, a gazua e a chave, o 17º caminho, os eventos e os módulos, o golpe pelas costas, o segredo do gerador), mais o que o projeto B pedir a esses arquivos (o povo na pessoa e na ficha, os traços dos dragões na luta), e **o contrato** das funções entre `masmorra.py`, `manha.py` e o módulo dos povos (quem chama quem, com que nomes).
2. **Onda 2, em paralelo** (nenhum arquivo em comum):
   - **construtor M, a masmorra:** `tabelas_masmorra.py`, `masmorra.py`, `tabelas_criaturas.py` (o guardião), `provas_masmorra.py`;
   - **construtor L, o ladino:** `tabelas_manha.py`, `manha.py`, `tabelas_oficio.py` e `oficio.py` (a gazua), `tabelas_mercado.py` e `mercado.py` (a tocha e a gazua), `provas_manha.py`;
   - os construtores do projeto B (os dragões, os povos), nos arquivos deles.
3. **Onda 3, a integração** (um construtor): `vila_teste.py` (o `masmorra` e o que o projeto B acrescenta; podem virar um comando só, `fantasia`), `provas_mundo.py`, `REGRAS.md`, `GUIA_VILA.md`, `MUDANCAS.md`, `LEIA.md`; joga uma cópia do `ensaio/` (a cripta com o Maro, o Tomé, a Rute e o Quim) e mede MA0, MA6 e MA15 de verdade.
4. Depois, **o revisor e o verificador**, como na etapa da magia.

O construtor M chama o `manha.testa` desde o primeiro dia: até o L entregar, um esboço com a mesma assinatura (a conta da seção 4, sem dom e sem povo) basta, e o contrato da onda 1 diz qual é.

## 14. O que fica de fora desta etapa

- **O furto** (etapa 3, com a gente que lembra e a vila com justiça): a regra fica escrita (seção 5.5).
- **O reforço no meio da luta:** quem ouve a luta chega depois dela, não durante (a luta de hoje não sabe pôr gente nova no meio, a não ser o morto erguido e o bicho chamado).
- **A tocha na mão:** quem a leva a larga no chão quando a luta começa, e ninguém perde o escudo. **Acender a luz no meio da luta**, só com o feitiço.
- A armadilha que se arma de novo; quebra-cabeças e mecanismos além da passagem escondida; nadar, escalar, corda (o Mestre narra com `teste.py`).
- O monstro que caça o grupo pela masmorra inteira (quem persegue vai até a sala seguinte).
- O mapa desenhado: a mesa dá a lista das salas e das passagens.
- O rival que desce de verdade (etapa 5) e a região com as suas masmorras (etapas 3 e 7): ficam o gerador e os ganchos.
- O ladino na caça (o passo macio atrás do bicho): a caça segue a de hoje, com o rastro dando o "viu primeiro".
- Abrir fechadura na vila (as casas, a loja de noite): etapa 3.
- O feitiço "chamar" do druida dentro da masmorra: chama só o bicho da sala onde se luta (o que o `ato.luta_nova` já faz com o lugar da luta); não procurei regra melhor.

## 15. O que é chute, e os riscos

**Chute (número que eu pus e não medi contra nada, além da cripta de teste):**
- o lance de 20 minutos e o custo de cada ação em lances;
- a chance do que vagueia (1 em 6 por bloco, mais 10 pontos por alarme) e os limiares do alarme (2 acorda, 4 chama a sala vizinha);
- a tocha a 1 de prata e um bloco; o feitiço luz a 4 de Mana por bloco; o povo gastar 0,01 tocha por pessoa por dia;
- os números do andar escondido: a malha −3, a placa −6, a luz −6, o alerta +4, o dormir −6;
- o acerto da armadilha (+6 mais o bônus da categoria) e a esquiva (20 + 6 por categoria); achar contra 20 + 6, a gazua contra 24 + 8 por degrau, escutar contra 22 e 26;
- a tabela do tesouro (20 × 4 por categoria, por sala de tesouro) e a peça maldita em uma de seis;
- o bando de fora em 120 dias de nível vazio; o morto erguido a cada 10 dias;
- o furto: a quantia e a pena.

**Os riscos:**
1. **O robô da descida é rascunho.** A luta é de verdade, mas a casca (o encontro, a armadilha, a fechadura, o que vagueia) eu escrevi à mão; o `masmorra.py` de verdade pode dar outros números. A MA6 mede de novo, e pode pedir acerto no guardião (a espada no lugar do montante tira 3 pontos da morte do Maro: medido).
2. **O fundo mata.** Nove em dez mortes da cripta são na câmara do guardião, e o jogador que não descansa antes dele morre uma vez e meia mais. É de propósito (a pergunta 4 deixa o jogador escolher o tom).
3. **O despojo pela categoria** muda uma conta que já existe (`criaturas.despojo`); feito só na masmorra, a caça e o covil seguem iguais, mas o povo de categoria mudada fora da masmorra (a guarda do senhor da guerra, Rara) segue rendendo a tabela da espécie. Achei o defeito; não o conserto fora da minha metade.
4. **O 17º caminho muda o sorteio do dom** da gente nova (agora entre 17): uma prova com semente fixa que espere um dom num caminho certo cairia. Não achei nenhuma, mas o `provas_talento.py` tem de rodar.
5. **Mais lugares:** cada masmorra traz as salas como lugares. Se uma sala virar vizinha de vila por engano, a mesa da caça a listaria como ermo (o invariante novo impede).
6. **A descida aberta entre turnos** guarda os lances na pessoa; o `fecha` deixa (como a saída de caça). Se a pessoa morrer de fome lá dentro, a regra da morte vale, mas é um caminho que só o banco vai mostrar.
7. **O orçamento de prata da região** (etapa 7): a tabela do tesouro pode ser rica demais para 8 masmorras.
8. **O povo do projeto B** que vê no escuro e anda leve faz a masmorra ficar muito mais fácil para ele; o teto de +2 por teste tem de valer, e o B tem de medir.
9. **A `MESA.md` já tem 13,8 KB** (a meta do `PROJETO.md` era 8): a descida aberta soma cerca de 1,5 KB.
10. **O corredor favorece muito o grupo** (99% contra 81%): o gerador não pode fazer toda masmorra de corredor (o molde mistura).
11. **O golpe pelas costas** é um ramo novo na luta: a MA0 tem de provar que a luta de quem não tem manha Treinado é a de sempre, dado por dado.

## 16. As perguntas ao jogador (só gosto; o resto eu decidi pela conta)

1. **O furto (roubar de gente):** a) entra agora, com a regra curta (é crime: pego, devolve e paga o triplo, ou fica 3 dias preso); b) entra na etapa 3, quando a gente lembrar de quem a roubou e a vila tiver quem vigie (a regra fica escrita desde já); c) não entra. **Recomendo b:** agora, sem memória nem guarda, o ladino de começo tira cerca de 34 de prata por dia da bolsa da vila, e isso é mina.
2. **A memória da masmorra:** a) a sala limpa fica limpa, e só volta o que tem motivo (o rato que cria, o bando de fora em meses, o morto que o chefe vivo ergue); b) a masmorra se refaz sozinha em uns 30 dias (as criaturas voltam; o tesouro, não). **Recomendo a:** é o mundo de verdade, e a b vira um lugar de treino que rende despojo sem fim.
3. **O golpe pelas costas do ladino:** a) entra (de Treinado na manha, o primeiro golpe contra quem foi surpreendido tem +4 e rola os dados 3 vezes: vale uns 11 pontos, como o Grande Dom, e a arma uma acima segue vencendo); b) não entra (a surpresa já é a vantagem de quem vê primeiro: uns 13 pontos no duelo). **Recomendo a:** dá ao ladino um jeito de lutar que é só dele, sem passar da lei do item.
4. **A cripta de teste:** a) dura: o guardião de montante (com Tomé e Rute, o Maro morre em 1 descida de cada 10 se descansa antes do chefe, e em 3 de cada 20 se não); b) mais branda: o guardião de espada e escudo (o Maro morre em 1 de cada 14). **Recomendo a:** a cripta é a primeira masmorra do jogador, e ela tem de ensinar que o fundo mata e que descansar antes do chefe salva.

## Anexo: o rascunho das duas páginas de números

Os números da proposta, como cairiam nas páginas (o construtor confere os nomes no contrato da onda 1; o que é chute está na seção 15).

```python
# tabelas_masmorra.py (rascunho)
LANCE_MINUTOS = 20
LANCES_BLOCO = 12                       # doze lances fecham um bloco: só então o ato.passa anda
CUSTO = dict(ir=1, escondido=2, escuro=2, carrega=2, escutar=1, procurar=2, tenta=1, contornar=1, disparar=1, pegar=1, luta=1, voltar=1, fosso=1)
ESFORCO_BLOCO = 'leve'                  # o bloco dentro: o da procura de caça
TOCHA = dict(bem='tocha', base=1, blocos=1)                # arde um bloco; gasta-se quando o bloco fecha
LUZ_MANA_BLOCO = 4                      # o feitiço luz, fora da luta, por bloco
LUZ_ESCONDIDO = -6                      # quem anda com luz, contra quem está no escuro
ARMADURA_ESCONDIDO = dict(couro=0, malha=-3, placa=-6)     # a armadura do tronco; sem armadura, 0
ATENTO = {-1: -6, 0: 0, 1: 4}           # dormindo, à toa, alerta: na Percepção de quem vigia (o morto não dorme)
ESCONDIDO = 20                          # contra 20 + Percepção ÷ 10 do melhor vigia + ATENTO
ATENCAO = 20                            # quem vai na frente: Percepção + manha contra 20 + Agilidade ÷ 10 dos que emboscam
ALARME = dict(luta=1, arrombar=1, fosso=1, pedra=1, runa=1, alarme=2, teto=5, acalma=1, alerta=2, vem=4)
VAGA = (1 / 6, 0.10)                    # o que vagueia: por bloco dentro, mais isto por ponto de alarme
ARMADILHAS = {
    'dardo':  dict(dado='1d6',  golpe='ponta',   pega='um',    escapa='acerto', barulho=0),
    'lâmina': dict(dado='1d10', golpe='corte',   pega='um',    escapa='acerto', barulho=0),
    'fosso':  dict(dado='2d6',  golpe='impacto', pega='um',    escapa='Agilidade', parte='pernas', estacas_desde=1, barulho=1),
    'pedra':  dict(dado='2d8',  golpe='impacto', pega='um',    escapa='Agilidade', cabeca=0.3, barulho=1),
    'gás':    dict(dado='1d6',  golpe='guarda',  pega='todos', escapa='Vigor', metade=True, barulho=0),
    'runa':   dict(dado='1d8',  golpe='guarda',  pega='um',    escapa='Firmeza', amaldicoa_desde=1, barulho=1),
    'alarme': dict(dado=None,   pega='ninguém', barulho=2),
}
ARMADILHA_ACERTO = 6                    # 2d20 + isto + o bônus da categoria, contra a Defesa sem escudo (ou a Firmeza, a runa)
ESQUIVA = (20, 6)                       # Agilidade ou Vigor contra 20 + 6 por categoria
PASSAGEM = -6                           # achar de passagem: quem vai na frente, de graça, 6 mais difícil
ESCUTAR_FERRO = 4                       # a porta de ferro ou de pedra: escutar é 4 mais difícil
MOLDES = {   # salas por nível · níveis · quem mora · armadilhas · o chefe do fundo (pela categoria)
    'cripta': dict(salas=(4, 8),  niveis=(1, 2), mora=['esqueleto', 'corpo-seco', 'carniçal', 'alma-penada', 'múmia', 'espectro'], ninho=['ratazana'],
                   armadilhas=['dardo', 'lâmina', 'runa', 'gás'], chefe={0: 'guardião da cripta', 1: 'guardião da cripta', 3: 'necromante'}, corredor=0.5),
    'mina':   dict(salas=(6, 12), niveis=(1, 3), mora=['aranha', 'trasgo', 'golem-de-barro'], ninho=['ratazana'], covil=['goblin', 'orc'],
                   armadilhas=['fosso', 'pedra', 'alarme'], chefe={1: 'xamã goblin', 2: 'senhor da guerra'}, corredor=0.6, minerio=True),
    'ruína':  dict(salas=(8, 16), niveis=(1, 3), mora=['esqueleto', 'gárgula', 'golem-de-barro', 'fogo-fátuo', 'harpia'], armadilhas='todas',
                   chefe={2: 'bruxa do brejo', 3: 'necromante'}, corredor=0.3),
    'toca':   dict(salas=(5, 10), niveis=(1, 2), covil=['goblin', 'orc', 'homem-lagarto', 'ogro'], armadilhas=['fosso', 'alarme'],
                   chefe={1: 'xamã goblin', 2: 'senhor da guerra'}, corredor=0.4),
    'covil':  dict(salas=(3, 6),  niveis=(1, 1), mora=[], armadilhas=[], chefe={3: 'serpe', 4: 'hidra'}, corredor=0.5),     # o dragão: projeto B
}
SEGREDO_CADA = 3                        # uma sala escondida a cada tantos níveis
TESOURO = dict(prata=lambda c: 20 * 4 ** c, salas=(2, 4), pecas_cada=3, acima=('escondida', 'chefe'), maldita=1 / 6, pocoes=(1, 2))
MEMORIA = dict(ergue=10, vem_de_fora=120)       # o chefe vivo ergue um morto a cada tantos dias; o nível vazio espera tantos dias por um bando de fora

# tabelas_manha.py (rascunho)
ACHAR = (20, 6)                         # 2d20 + Percepção ÷ 10 + manha, contra 20 + 6 por categoria
GAZUA = (24, 8)                         # 2d20 + Agilidade ÷ 10 + manha, contra 24 + 8 × (a categoria da fechadura ou da armadilha − a da gazua)
SEM_GAZUA = -1                          # sem gazua, ela conta um degrau abaixo do Comum
FALHA = 5                               # falhar por isto ou mais: a armadilha dispara; a gazua (ou a arma de arrombar) perde 1
ARROMBAR = (24, 8)                      # 2d20 + Força ÷ 10, contra 24 + 8 × (a categoria da porta − a da arma de impacto em uso); o ombro conta −1
ESCUTAR = dict(madeira=22, ferro=26, mortos=6)
FEITO = {6: 2, 8: 3}                    # Mestre: abrir ou desarmar uma Rara de verdade; Lendário: uma Épica
MATERIA_GAZUA = dict(metal=1)           # como a adaga: a forja, o preço, o conserto
TREINO_BLOCO = 1                        # na masmorra, no máximo 1 bloco de treino de manha por bloco que fecha
FURTO = dict(contra=20, guarda=4, leva='1d6', pena=3, preso_dias=3)     # para a etapa 3

# tabelas.py (se o golpe pelas costas entrar)
COSTAS = dict(desde=4, acerto=4, dados=3)       # de Treinado na manha: o primeiro golpe de corpo a corpo contra quem foi surpreendido
```
