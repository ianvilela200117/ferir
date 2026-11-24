# RASCUNHO do capítulo 17: as masmorras

Rascunho da frente M (a masmorra) da etapa 4b. O integrador junta no `REGRAS.md`. Os números moram no `tabelas_masmorra.py` (e os testes do ladino, no `tabelas_manha.py`); a regra, no `masmorra.py`; o chefe novo, no `tabelas_criaturas.py`; as provas, no `provas_masmorra.py` (o `provas_mundo.py` o chama). O contrato de nomes e campos é o `projeto/ETAPA_4B.md`.

---

## 17. AS MASMORRAS

### 17.1 A masmorra e a sala

**A masmorra é um lugar do mapa** (tipo `masmorra`), vizinho de uma vila ou de um ermo, a alguns blocos de caminho (`longe`). Por dentro ela tem **salas**, e cada sala é um lugar pequeno (tipo `sala`), ligado às outras por passagens (os `vizinhos` da sala, que valem para os dois lados). Por ser lugar, a sala usa as regras de sempre: quem mora ali está contado (`bichos`), a prata e os bens estão no estoque dela, a peça largada fica nela, e quem morre lá dentro deixa tudo na sala.

Nenhuma sala é vizinha do que não é sala: a vila lista a masmorra, nunca uma sala dela (a mesa da caça nunca a confunde com um ermo). A masmorra não tem bichos nem matéria: quem mora está nas salas; quem vagueia, em `vagantes`.

| A masmorra guarda | O que é |
| --- | --- |
| o molde | cripta, mina, ruína, toca ou covil |
| os níveis | de 1 a 3 (ou mais); cada descida de nível soma uma categoria (nas criaturas, nas armadilhas, nas fechaduras e no tesouro) |
| a entrada | a sala onde se chega, no nível 1 |
| as portas | uma por passagem que tem porta: aberta, fechada, trancada (com fechadura), emperrada ou arrombada; de madeira, de ferro ou de pedra |
| o alarme | de 0 (quieta) a 5 (acordada) |
| quem vagueia | os que andam e não moram em sala nenhuma |
| a primeira limpeza | o dia, quem e o chefe, quando o chefe do fundo cai pela primeira vez |

| A sala guarda | O que é |
| --- | --- |
| a largura | 1 (corredor de um), 2 (sala estreita) ou nada (sala aberta): é a largura da luta |
| acesa | há fogo aceso: a luz é de todos |
| a categoria | a de quem mora ali (a do nível; a espécie de categoria maior fica na dela) |
| atento | quem mora ali dorme, está à toa ou alerta |
| as armadilhas | no chão, numa porta ou no que a sala guarda; escondida, achada, desarmada ou disparada |
| o que guarda | o baú, o sarcófago, o nicho (com fechadura ou sem); fechado, a prata e as peças da sala estão dentro |
| os segredos | as passagens escondidas: achada, vira passagem como as outras |
| o chefe | quem manda ali (um chefe das criaturas, ou um bicho chefe); o dragão mora no registro dele |

### 17.2 Descer

A descida é como a saída de caça: **um ato aberto**, escrito em quem comanda (a descida) e em quem vai junto. Quem está na descida **está fora**: os atos da vila são recusados (come-se da própria carga, bebe-se a poção), a cama não vale, e o dia lá dentro não é dia de repouso para a ferida.

```
python3 masmorra.py ver                                     a masmorra vizinha (o que se diz dela), a descida aberta, o mapa visto, o que se faz daqui
python3 masmorra.py descer [MASMORRA] [com=ID,ID] [ordem=ID,...] [luz=tocha|feitiço|nada] [quem_luz=ID]
python3 masmorra.py ir SALA [escondido]                     1 lance (escondido 2; no escuro, o dobro)
python3 masmorra.py escutar SALA [quem=ID]                  1 lance; rolagem oculta
python3 masmorra.py procurar [quem=ID]                      2 lances; uma rolagem oculta para cada coisa escondida da sala
python3 masmorra.py abrir SALA|guardado [chave|gazua|grampo|força] [quem=ID]     1 lance por tentativa
python3 masmorra.py desarmar [N] [quem=ID] · contornar [N] · disparar [N]       1 lance
python3 masmorra.py atacar [inicio=longe|perto|colado] [passagem] · esperar · recuar
python3 masmorra.py luta ["Nome: ordem"]                    a luta aberta (o ato.py luta roda); acabada, as contas saem sozinhas
python3 masmorra.py pegar [tudo|prata|ITEM] [quem=ID]       1 lance
python3 masmorra.py descansar N [vigia=ID] · ordem ID,ID,... · luz tocha|feitiço|nada [quem=ID]
python3 masmorra.py voltar · sair                           1 lance por sala até a entrada · a volta para casa
SÓ O MESTRE: masmorra.py mapa [MASMORRA] · gera MOLDE "Nome" [vizinho=LUGAR] [niveis=N] [cat=K] [longe=N] · larga "por quê"
```

`quem=ID` é quem comanda; dito de alguém que foi junto, é quem faz (procura, abre, desarma, escuta, pega), na descida de quem comanda.

### 17.3 O tempo: o lance e o bloco

O relógio só anda em blocos. Lá dentro cada ação custa **lances de 20 minutos**, e **doze lances fecham um bloco** pelo `ato.passa`, para o grupo inteiro (o esforço leve da procura de caça). O bloco que fecha é um bloco como os outros (a fome, o sono, o cansaço, quem cai no sono, a virada do dia), e mais: a tocha de quem leva a luz se gasta, o alarme cai, o treino do ladino conta, e o mundo rola o que vagueia.

| Ação | Lances |
| --- | --- |
| ir à sala vizinha | 1; escondido, 2; sem luz e sem quem veja no escuro, o dobro |
| escutar uma porta | 1 |
| procurar na sala | 2 |
| abrir, desarmar, arrombar | 1 por tentativa |
| contornar a armadilha do chão, dispará-la de longe | 1 |
| pegar o que a sala guarda | 1 |
| a luta (o fôlego e a ferida amarrada, depois) | 1 |
| esperar escondido | 1 |
| tirar quem caiu no fosso | 1 |
| voltar | 1 por sala |
| descansar | blocos inteiros (o bloco aberto fecha antes) |

**Descer** é a ida (os blocos de `longe`); **sair** fecha o bloco aberto (o resto conta como bloco inteiro) e faz a volta. Medido (MA1, em 20 masmorras do gerador): N lances andam ⌈N ÷ 12⌉ blocos, mais a ida e a volta, e cada bloco gasta uma tocha.

### 17.4 A luz e o escuro

| | O que faz |
| --- | --- |
| a tocha | um bem da carga (a loja a vende). Arde um bloco: quando o bloco fecha, gasta-se uma de quem leva a luz. A última que começa a arder, a mesa avisa; acabada, a luz acaba (outra tocha de outro: `luz tocha quem=ID`) |
| o feitiço luz | 4 de Mana por bloco, de quem o sabe; sem Mana para o bloco seguinte, apaga |
| sem luz | quem não vê no escuro anda no dobro dos lances, não procura, não abre fechadura e não desarma (arromba, sim); a luta tem o escuro (−4 no golpe, −8 no tiro) |
| quem vê no escuro | anda, procura, abre e desarma sem luz; na luta, o escuro tira dele só a metade (capítulo 19) |
| a sala acesa | a luz é de todos |
| a luz se vê | quem anda com luz tem −6 no andar escondido contra quem está no escuro |

Uma luz só serve a todos. Na luta, quem leva a tocha a larga no chão: a luz fica, e ninguém perde a mão do escudo. **No descanso a tocha não arde** (dorme-se no escuro; quem acorda acende de novo). Medido (MA2): o grupo da vila contra seis esqueletos numa sala aberta vence 81% com luz e perto de 29% no escuro.

### 17.5 O grupo e a ordem de marcha

Quem vai junto é gente do lugar, viva e sem saída nem descida aberta: entra nas lutas, passa os mesmos blocos e tem parte no que se pega. **A ordem de marcha** (muda a qualquer hora, sem lance) diz quem pisa primeiro (a armadilha do chão é dele), quem olha primeiro (a armadilha vista de passagem, a atenção) e quem fica na frente na luta; quem atira (o arco, a besta) vai atrás. Num corredor de um, a luta põe um atrás do outro, na ordem.

### 17.6 O encontro: quem vê primeiro

Quando o grupo entra numa sala com gente (ou gente chega a ele), a descida **para e conta o que se vê**.

1. **O grupo anda escondido** (`ir SALA escondido`): o grupo anda no passo do mais barulhento. Rola quem anda pior escondido (o dado do ladino, capítulo 18: 2d20 + Agilidade ÷ 10 + a manha − a armadura do tronco − a luz) contra **20 + a Percepção ÷ 10 do melhor vigia da sala**, +4 se estão alertas, −6 se dormem (o morto não dorme). Rolagem oculta. Passou: o grupo **vê primeiro** (no escuro, sem ninguém que veja nele, só ouve: sabe que há gente, não quantos). Escolhe: atacar (eles perdem o primeiro turno; a luta começa perto, colada, ou longe numa sala aberta), esperar escondido (1 lance) ou recuar sem ser visto.
2. **Não escondido, ou falhou**: eles notam o grupo. Se estão alertas (ou o alarme está em 2 ou mais), ou são de emboscada (a gárgula, a aranha), quem vai na frente testa a atenção (2d20 + Percepção ÷ 10 + a manha contra 20 + a Agilidade ÷ 10 deles; oculta): falhou, **o grupo é surpreendido**. À toa, ninguém é surpreendido.
3. **A porta fechada** com gente atrás: quem está do outro lado ouve, e a luta começa colada.
4. **Puxar para o corredor**: quem não foi pego desprevenido e entrou vindo de um corredor de um pode esperar na boca dele (`atacar passagem`): a luta é na largura do corredor, e eles vêm um a um.

**Recuar**: sem ser visto, ninguém vem atrás. Visto, as feras e o povo vêm atrás pela índole da espécie (a tabela da caça); o morto lento não sai da sala dele. Quem vem atrás chega na sala de trás, e a luta abre ali.

Do chefe ninguém sabe de graça: a mesa o nomeia quando a cena o põe à frente, e o Mestre lê o que se sabe dele (no SÓ O MESTRE). Medido (MA3): ver primeiro leva o grupo de 77% a perto de 90%; ser surpreendido o derruba a perto de 48%.

### 17.7 A luta lá dentro

A luta é a do `ato.py luta`, com as paradas de sempre. A masmorra só monta o cenário: o grupo na ordem de marcha (quem comanda, no comando; quem atira, atrás), a largura da sala, a luz ou o escuro, a surpresa, o chefe (dos chefes das criaturas, sem os lacaios: a guarda é quem mora na sala), o dragão (frente D) e quem mora ali. **No covil, o lado do dragão não tem saída** (ele luta até morrer; fora do covil, o que voa pode fugir ferido: capítulo 20).

**As contas**, num evento só, quando a luta acaba:
- quem morreu sai da contagem da sala (o caído é rematado por quem ficou com o campo; o povo rendido sai como o morto);
- **quem fugiu some no escuro**: sai da sala e passa a vaguear pela masmorra;
- **o despojo pela categoria de quem morreu** (a matéria na categoria dele, até a Rara), em partes iguais entre quem lutou até o fim;
- o chefe que cai deixa a sala; o chefe que é povo deixa a sucata das peças dele (o guardião da cripta: metal e osso Comuns); do Épico para cima, deixa o núcleo;
- o chefe do fundo que cai pela primeira vez é **a primeira limpeza** (o dia, quem e o chefe ficam escritos na masmorra);
- a luta soma 1 no alarme; e soma 1 lance.

Quem perde o campo recua à sala de trás (e quem viu pode vir atrás). Com o alarme em 4 ou mais, **quem está numa sala vizinha vem** ver o barulho: chega logo depois da luta (nunca no meio dela).

### 17.8 As armadilhas

**A armadilha bate como uma arma da categoria dela** (a conta do aço): o dano é dado × 4 × o valor da categoria ÷ a proteção da parte que ela pega (o material contra o golpe; a parte nua conta um terço). O crítico é o da luta. A zero de PV, morre quem levou mais da metade do PV num golpe; quem não, cai e fica com 1. A ferida e a grave são as da luta.

| Armadilha | O golpe | Quem pega | Como se escapa | Barulho |
| --- | --- | --- | --- | --- |
| dardo | 1d6, ponta | quem pisa ou quem abre | o acerto: 2d20 + 6 + o bônus da categoria contra a Defesa sem escudo | não |
| lâmina | 1d10, corte | quem passa | o acerto | não |
| fosso | 2d6, impacto, nas pernas (da Incomum para cima, estacas: ponta); quem cai fica no fundo (1 lance para tirar) | o primeiro da fila | Agilidade contra 20 + 6 por categoria | +1 |
| pedra | 2d8, impacto (cabeça 3 em 10) | quem passa | Agilidade contra 20 + 6 por categoria | +1 |
| gás | 1d6 pela guarda (o amuleto, ou 0,6 da armadura do tronco) | todos | Vigor contra 20 + 6 por categoria: passou, a metade | não |
| runa | 1d8 pela guarda; da Incomum para cima, amaldiçoa (a marca da runa, da categoria dela; quebra com 7 dias sem pôr o pé na sala) | quem pisa | o acerto contra a Firmeza | +1 |
| alarme | nada | ninguém | | +2 |

**Achar**: quem vai na frente olha de graça ao entrar na sala (o chão) e ao chegar à porta, 6 mais difícil (oculta); **procurar** é a rolagem inteira (2d20 + Percepção ÷ 10 + a manha contra 20 + 6 por categoria; oculta). A armadilha do que a sala guarda só se acha procurando.

**A do chão achada para o grupo** à entrada da sala. Resolve-se assim: **desarmar** (2d20 + Agilidade ÷ 10 + a manha contra 24 + 8 × (a categoria dela − a da gazua); sem gazua, um degrau abaixo do Comum; falhar por 5 ou mais a dispara em quem desarmava), **contornar** (1 lance, sem teste; o fosso num corredor de um pede pular, cada um), **disparar de longe** (1 lance; faz o barulho dela) ou voltar. A da porta: desarmar, disparar de longe, ou abrir assim mesmo (ela pega quem abre). A do baú: desarmar, ou abrir e levar. Cada armadilha dispara uma vez. Achada, a do chão nunca mais pega o grupo por descuido.

Medido (MA7, a conta do aço): o dardo Comum nunca mata quem está de PV cheio sem crítico; o dardo Raro mata na hora metade das vezes quem veste peças Comuns; em quem veste malha Rara tira perto de 11% do PV.

### 17.9 As portas e as fechaduras

| Porta | O que faz |
| --- | --- |
| aberta, arrombada, ou sem porta | passa-se |
| fechada | abre-se ao passar, de graça; quem está do outro lado ouve |
| trancada | a chave (sem teste), a gazua ou o grampo (a conta da fechadura), ou a força |
| emperrada | só a força |
| de ferro ou de pedra | escutar através dela é mais difícil (26 contra 22 da madeira; os mortos, que não respiram, mais 6) |
| só para miúdos | só passa o grupo todo de corpo miúdo |

**A chave** é uma peça do Livro de Itens (não gasta, não se vende): abre sem teste a porta ou o guardado que ela diz. **Arrombar** é 2d20 + Força ÷ 10 contra 24 + 8 × (a categoria da porta − a da arma de impacto em uso; o ombro conta um degrau abaixo do Comum); cada tentativa é 1 lance e soma 1 no alarme; falhar por 5 ou mais gasta 1 da arma. **A gazua** que falha por 5 ou mais perde 1 de durabilidade. Abrir e desarmar de verdade contam para o feito do ladino (capítulo 18). **Escutar** diz silêncio, algo se mexe (os mortos), ou vozes de poucos ou de muitos, nunca o número.

### 17.10 O alarme, o que vagueia e o descanso

**O alarme** (0 a 5): a luta +1; cada tentativa de arrombar +1; a armadilha que faz barulho +1 (o alarme, +2). Cai 1 a cada bloco sem barulho; na virada do dia volta a 0. **Com 2 ou mais**, quem mora lá está alerta (+4 na Percepção, e arma a emboscada: a atenção de quem vai na frente). **Com 4 ou mais**, quem está numa sala vizinha vem, depois da luta.

**O que vagueia**: a cada bloco que fecha lá dentro, o mundo rola (oculto) **1 em 6, mais 10 pontos por ponto de alarme**. Saindo, um bando dos `vagantes` da masmorra chega ao grupo (sai da conta da masmorra e entra na sala); quem vai na frente testa a atenção.

**O descanso lá dentro** (`descansar N`): dorme-se no chão, ali (o sono e o cansaço baixam como no chão; o PV volta pouco: para sarar, a vila). Cada bloco rola o que vagueia: **com quem vigia** (que não dorme naquele bloco), o grupo não é surpreendido; **sem vigia, é**. Não se dorme com gente de pé na sala. Medido (MA12): a chance por bloco bate a conta (16%, 27%, 37%, 47% com o alarme de 0 a 3).

### 17.11 O tesouro, e o que se pega

**O tesouro é prata que já existe**, posta pelo gerador uma vez (evento do gerador); depois, só muda de mão. A masmorra perde a que o grupo leva, e ganha a dos mortos que caem nela (que já existia).

**Pegar** (1 lance) leva o que está à vista: a prata e os bens do estoque da sala e as peças sem dono que estão nela. **A prata e os bens repartem-se em partes iguais entre quem está na descida naquela hora** (o que sobra da divisão vai, uma unidade a cada um, a começar por quem comanda); **a peça fica com quem a pega** (quem comanda, sem dizer). Com o guardado fechado, a prata e as peças estão dentro dele: abre-se antes. Não se pega nada com gente de pé na sala. O que ficou junto do corpo de quem morreu não muda de mão sozinho (cena do Mestre, como na caça).

| O gerador põe | Comum | Incomum | Raro | Épico | Único |
| --- | --- | --- | --- | --- | --- |
| prata em cada sala de tesouro (2 a 4 por nível) | 20 | 80 | 320 | 1.280 | 5.120 |
| peças | 1 a cada 3 salas do nível, da categoria dele; a da sala escondida e a do chefe, uma acima; uma em seis, maldita | | | | |
| poções | 1 ou 2 por nível, da categoria | | | | |
| núcleo | | | | o do chefe do fundo | o do chefe do fundo |

Medido (MA4): a casa da vila que vive 60 dias ao lado da cripta tira dela bem menos que uma diária por pessoa e por dia, e depois da primeira limpeza quase nada.

### 17.12 A memória: a sala limpa fica limpa

| O que | Volta? |
| --- | --- |
| o morto que anda | só se o chefe da masmorra está vivo: ele ergue **um a cada 10 dias**, até o que cada sala tinha; morto o chefe, nunca mais |
| o bicho que cria (o rato) | pela regra da caça, na sala que tem o ninho (o teto): o casal de fora, e depois a cria, até o teto |
| quem fugiu de uma luta | já vagueia pela masmorra (17.7) |
| **um bando de fora** | quando o nível fica sem quem mande (sem chefe vivo e sem morador que não seja bicho que cria), **120 dias depois** chega um bando da lista do molde (na cripta, goblins), sem tesouro: traz só o que é dele |
| o chefe | morto, morto |
| o tesouro levado | **nunca** |
| a armadilha disparada ou desarmada, a porta arrombada | ficam como ficaram |
| o alarme | cai 1 por bloco sem barulho; na virada, volta a 0 |

### 17.13 O mapa é segredo

**A MESA, com a descida aberta** (seção "A masmorra"): onde o grupo está e o que se vê, a luz (quem leva, quantas tochas, quantos lances faltam para o bloco fechar), o alarme em palavras, o grupo na ordem de marcha com o PV, **o mapa que o grupo viu** (as salas, as passagens e as portas; a sala que ninguém viu é "uma passagem"), o que há para pegar, as armadilhas achadas, e o que dá para fazer daqui. Sem descida, a mesa não ganha linha nenhuma.

**O SÓ O MESTRE**: com a descida aberta, o mapa inteiro, sala por sala (quem mora, quantos, se dormem; as armadilhas; as portas e as fechaduras; o tesouro; os segredos; o chefe; as chaves); sem ela, uma linha por masmorra vizinha. As rolagens ocultas (escutar, procurar, a de passagem, o andar escondido, a atenção) vão ao SÓ O MESTRE com o número; à mesa sai só "rolagem oculta".

**O que o personagem sabe mora nele** (o mapa de cada masmorra que ele viu): o herdeiro não sabe o mapa do morto. **O evento que cria a masmorra é segredo** (vai ao SÓ O MESTRE do RETOMAR). O RETOMAR leva a descida aberta. Medido (MA14): a mesma descida, com e sem o chefe atrás da porta, dá o mesmo texto até a porta abrir.

### 17.14 Os moldes e o gerador

| Molde | Salas por nível | Níveis | Quem mora | Armadilhas | O chefe do fundo | O bando de fora |
| --- | --- | --- | --- | --- | --- | --- |
| cripta | 4 a 8 | 1 a 2 | esqueleto, corpo-seco, carniçal, alma penada, múmia, espectro; ratazana nos ninhos | dardo, lâmina, runa, gás | o guardião da cripta (Comum e Incomum); o necromante (do Épico) | goblins |
| mina | 6 a 12 | 1 a 3 | aranha, trasgo, golem de barro; goblins e orcs; ratazana nos ninhos | fosso, pedra, alarme | o xamã goblin; o senhor da guerra | goblins, orcs |
| ruína | 8 a 16 | 1 a 3 | esqueleto, gárgula, golem de barro, fogo-fátuo, harpia | todas | a bruxa do brejo; o necromante | goblins, orcs |
| toca | 5 a 10 | 1 a 2 | goblins, orcs, homens-lagarto, ogro | fosso, alarme | o xamã goblin; o senhor da guerra | goblins, orcs |
| covil | 3 a 6 | 1 | um bicho chefe e o que come as sobras | nenhuma | a serpe, a hidra; o dragão (capítulo 20) | |

`masmorra.py gera MOLDE "Nome"` (SÓ O MESTRE) faz uma masmorra inteira pelo dado do mundo, num evento do gerador (segredo): a entrada; um caminho até a escada (no último nível, até a porta de ferro trancada do fundo); de 1 a 3 salas de lado; no primeiro nível (e a cada 3), uma sala escondida. Quem mora sai da lista do molde, só espécies da categoria do nível ou abaixo; os corredores saem pela fração do molde. Medido (MA1): os cinco moldes nascem inteiros, e o gerador é segredo do Mestre.

### 17.15 A Cripta da Cova Velha (a vila de teste)

Os mortos da Cova Velha subiam de algum lugar: sob o mausoléu quebrado há uma escada. A cripta tem 7 salas num nível só, Comum, a 1 bloco de Pedra Rasa, com o guardião no fundo. O povo diz que "os mortos da Cova Velha subiam de uma escada, debaixo do mausoléu quebrado"; o resto é do Mestre.

```
[1] a escada (corredor de um) ── porta de madeira, fechada ── [2] o corredor dos nichos (corredor de um): 2 corpos-secos; um dardo Comum no chão
[2] ── [3] o ossário (sala aberta): 3 esqueletos; 10 de prata na tigela
[2] ── [4] a capela (sala de 2): 4 ratazanas dormindo (o ninho); o baú das oferendas (fechadura Comum, um dardo Comum nela): 25 de prata, a maça, uma poção de cura, a chave de ferro
[3], [4] ── [5] os degraus (corredor de um): uma runa Comum no chão
[5] ── porta de ferro, trancada (fechadura Incomum; a chave de ferro a abre) ── [6] a câmara do guardião (sala de 2): o guardião da cripta e 2 esqueletos;
        o sarcófago (fechadura Comum): 30 de prata e o escudo do guardião (Incomum); uma passagem escondida (Incomum) para
[7] o nicho escondido (corredor de um): 15 de prata e a gazua Incomum
Vagueiam: um corpo-seco e três ratazanas. A prata da cripta: 80.
```

**O guardião da cripta** (um chefe novo, `tabelas_criaturas.CHEFES`): o cavaleiro da cova na categoria da cripta (Comum), de montante e placa velha, nível 25, mão de Treinado; abaixo de metade do PV bate o pé, dá o brado e ergue até dois mortos da sala; a guarda são os dois esqueletos da câmara. Vivo, ergue de novo um morto a cada 10 dias.

**Entra por `masmorra.na_vila(E)`** (o `vila_teste.py fantasia` do integrador a chama): um evento do gerador, que é segredo; recusa a segunda vez, e recusa a vila sem a Cova Velha (a etapa da magia). A prata nova é 80.

Medido (MA6, o robô de verdade pelo `masmorra.py`, 150 vidas por linha, até 20 dias; desce quando todos estão inteiros; o guarda na frente; recua abaixo de 30% do PV; o prudente não abre a porta do fundo com alguém abaixo de 75%):

| Quem desce | Limpa a cripta | O Maro morre |
| --- | --- | --- |
| Maro, Tomé e Rute, prudentes | perto de 92% | perto de 8% (metade das mortes na câmara do guardião) |
| os três e um ladino na frente (ele procura e desarma; atrás na luta) | perto de 97% | perto de 1% |
| o Maro sozinho | 0% | perto de 97% |

A cripta não é para o Maro sozinho. Com Tomé e Rute é dura e justa: o fundo mata, a capela de ratos alertas morde, e quem põe o guarda na frente e descansa antes do chefe vive.

### 17.16 Os ganchos

- **O covil do dragão** (frente D): a sala do covil leva o registro do dragão; a masmorra monta a luta com `dragoes.monta` (o lado dele sem saída), faz as contas com `dragoes.depois_da_luta`, e a vigília dele é o número contra o qual o grupo anda escondido (`dragoes.vigilia`).
- **O ladino** (frente L): todo teste de manha é o `manha.testa`; o treino na masmorra (no máximo 1 por bloco, de quem andou escondido, escutou, procurou, abriu ou desarmou) é o `manha.treino`; o feito é o `manha.feito`.
- **Quem vê no escuro** (frente P): `povos.ve_no_escuro`.
- **A janela do mundo, os rivais e a história** (etapas 5 e 7): a primeira limpeza fica escrita na masmorra; o gerador recebe a origem (o texto) e a prata do orçamento da história.
