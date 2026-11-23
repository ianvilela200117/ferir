# A CAÇA E A COLETA: o ermo contado, o rastro, a ameaça lida antes, o despojo (etapa 2)

> **RASCUNHO GUARDADO.** O capítulo que vale é o 9 do `../REGRAS.md`, que a integração da etapa 2 acertou (regras mudadas e números medidos de novo). O que está aqui é o texto do construtor, de antes da revisão: as tabelas de medida e as réguas são daquele dia.

Capítulo para o `REGRAS.md` (o número 9 é provisório: quem monta o livro o acerta). Os números moram no `tabelas_caca.py`; os dos bichos, no `tabelas_bichos.py`; as provas, no `provas_caca.py`.
O comando é o `caca.py`. Tudo o que ele faz entra por evento (`cacar`, `coletar`, `despojo`, `ninhada`). A luta é a do `ato.py luta` (5.9), sem tirar nada.

## 9. A caça e a coleta

9.1 **O ermo** é um lugar com bichos contados e matéria contada: `bichos` e `teto` (espécie: quantos há, quantos cabem), `coleta` e `coleta_teto` (matéria com categoria: quanto há, quanto cabe). **O que se tira, sai. O que nasce, nasce devagar.**
Caça-se e coleta-se no ermo **vizinho** do lugar onde a pessoa mora (`lugar.vizinhos`). A contagem é do Mestre. O que todo mundo sabe é a fartura, em palavras:

| Há, do teto | O povo diz |
| --- | --- |
| três quartos ou mais | há fartura |
| de 40% a três quartos | há, mas rareou |
| de 10% a 40% | é raro ver |
| menos de 10% | quase sumiu |
| nada | sumiu |

Dos chefes ninguém sabe de graça: acha-se no rastro.

9.2 **A saída** é um ato só: a ida, os blocos de procura (ou de coleta) e a volta. A pessoa segue morando no lugar dela.
- A ida custa 1 bloco (o ermo pode dizer outro número em `longe`); a volta, o mesmo. A procura vai de 1 a 6 blocos; sem dizer, 2.
- A ida, a volta e a procura são blocos **leves**; a coleta é bloco **pesado**. Cada luta cansa 2 (5.2).
- A saída aberta fica escrita na pessoa (`marca.caca`) até a volta: sobrevive a fechar e abrir o estado, e a `MESA.md` a mostra. Por isso a escolha diante do bicho pode ser uma pergunta do turno.
- A procura **para** quando aparece alguma coisa e quando o corpo cruza um limiar (5.6). Acabados os blocos, a volta sai sozinha.
- **Quem vai junto** (`com=`) é gente do mundo que está no mesmo lugar: entra na luta ao lado do caçador. O corpo dos companheiros só sente a luta (o cansaço da caminhada deles é da etapa 3).

9.3 **O rastro.** Um teste por bloco de procura (5.8): **2d20 + Percepção ÷ 10 + maestria de caça**, com a pena do corpo, contra a fartura do ermo:

| O número | |
| --- | --- |
| a base | 20 |
| a categoria do bicho (o raro é arisco) | Comum 0 · Incomum +2 · Raro +4 · Épico +6 · Único +8 · Lendário +10 |
| é chefe | +4 |
| o que falta da espécie | +12 × (1 − contagem ÷ teto): na metade do teto, +6; sumida, +12 |
| de noite ou de madrugada | −4 no teste |

Sem alvo ("o que aparecer"), o número é a base mais o que falta do ermo inteiro, e a espécie sai da sorte do mundo, com o peso da contagem de cada uma.

9.4 **O que aparece sai da contagem real:** um bicho, um bando, ou nada. O bando é o da espécie (6.9), **nunca maior do que a contagem**. Com a espécie a zero, quem passa no teste acha um rastro velho e mais nada.

9.5 **O acaso.** No bloco em que o rastro **falha** (e em todo bloco de coleta), pode aparecer o que não se procurava. A chance, por bloco, é a soma de contagem × ousadia de todas as espécies do ermo, dividida por 1.500 (nunca mais que metade). **Esse bicho viu o caçador.**

| Espécie | Ousadia (o quanto vem ao encontro de gente) | Investe (em quem não o atacou) |
| --- | --- | --- |
| corça | 0,1 | nunca |
| ratazana | 0,4 | 30% |
| javali | 0,4 | 35% |
| lobo | 1 | 70% |
| surucucu | 0,5 | 50% |
| urso | 0,6 | 50% |
| pantera, trasgo, serpe | 1 | 90% |
| aranha-de-toca | 0,6 | 80% |
| grifo | 0,8 | 60% |
| basilisco | 0,6 | 70% |
| hidra | 0,6 | 90% |
| dragão | 1 | 80% |

Na borda da floresta, com tudo no teto, o acaso é de 3% por bloco de rastro falhado.

9.6 **A ameaça é lida antes.** Quando o bicho aparece, a saída para. O caçador lê a frase do `bichos.ameaca` (6.12), com a conta da regra de ouro já feita para a arma e a armadura que ele veste, e o que a posição lhe dá. Então escolhe: **atacar, deixar ou fugir.** Não há luta antes da escolha.

9.7 **A posição** é o que o rastro deu a quem **viu primeiro** (passou no teste):
- se atacar, **o bicho é surpreendido** (perde o primeiro turno, 3.2);
- a luta começa **longe** ou **perto**, à escolha; passando por 5 ou mais, pode começar **colada**;
- **cada 5 pontos de margem dão uma vantagem de terreno, à escolha, até duas:**

| Vantagem | O que é, na luta (3.8) |
| --- | --- |
| alto | o caçador no alto: +1 no golpe, +2 no tiro, e quem sobe anda 1 casa por ação |
| cerco | o bicho sem saída: não foge; encurralado, luta até o fim (6.11) |
| estreito | uma passagem de um: o bando chega um de cada vez, e o bicho grande luta apertado |
| cobertura | o caçador com cobertura: −4 no tiro e no sopro contra ele |

- **deixar** o bicho que não o viu não custa nada: a procura segue. **Fugir** dele é recuar sem ser visto, largar a caçada e voltar.

9.8 **O bicho que viu o caçador** (o acaso) não é surpreendido, e não há terreno a escolher:
- **atacar:** a luta começa perto;
- **deixar** (ficar onde está): o bicho **investe** pela índole da espécie (9.5), e aí a luta é a mesma; se não investe, vai embora, e a procura segue;
- **fugir:** o bicho vem atrás com a chance de investir **mais 20 pontos** (quem corre chama). Se vem, é teste de **Agilidade contra 20 + Agilidade ÷ 10 do bicho**. Passou, escapou, e a saída acaba. Falhou, foi **alcançado**: a luta começa colada, e **o caçador é o surpreendido**.

9.9 **A luta é a do `ato.py luta`** (5.9), com as paradas e as ordens do capítulo 3. O `caca.py` só monta o cenário e chama o `ato.luta_nova`: a casa são o caçador (comandado pelo jogador) e quem veio junto, com o que vestem hoje, o PV, as feridas e a pena do corpo; o outro lado são os bichos, com a ficha do capítulo 6.
- A luz é a do bloco em que o bicho apareceu: o encontro da noite e da madrugada é uma luta no escuro (3.9).
- Com a luta aberta, a saída não segue e o turno não fecha (5.10).
- A luta roda pelo `caca.py luta "Nome: ordem"`, que é o `ato.py luta roda` e, no fim, faz as contas; ou pelo próprio `ato.py luta roda`, e as contas saem no comando seguinte do `caca.py`.

9.10 **As contas da luta** entram num evento só (`despojo`):
- **bicho morto sai da contagem.** O caído é rematado por quem ficou com o campo; se a casa não ficou com o campo, o caído que não morreu segue vivo. **O que fugiu segue no ermo.**
- **se a casa ficou com o campo, o despojo de cada carcaça entra na carga** de quem comanda a saída (ou do companheiro vivo, se ele morreu): de cada bem, da metade ao inteiro da tabela da espécie (6.10, `bichos.despojo`);
- **o núcleo do chefe entra no Livro de Itens** (2.1) no mesmo evento: `de` é a espécie; o dono é quem ficou com o campo (e `onde` fica vazio: peça com dono não está largada); a história diz o dia, o bicho e o ermo;
- **quem perde o campo deixa a carcaça no mato:** nada entra em carga nenhuma. O núcleo do chefe que morreu assim nasce no ermo: sem dono, com `onde` no ermo;
- **quem perdeu e vive volta na hora.** O que foi deixado por morto (caiu e não morreu, 3.13) volta arrastando-se: 1 bloco a mais. Quem ficou com o campo pode seguir a procura;
- **quem morre no ermo fica lá com o que vestia:** as peças seguem no Livro de Itens, sem dono, com `onde` no ermo, e a história diz com quem ficaram. O estado não fica com peça vestida num morto;
- **quem passa num rastro naquele ermo acha o que ficou no chão** (o núcleo da carcaça velha, as peças junto do corpo): passa a ser dele.

9.11 **A presa ferida.** O bicho que foge **com ferida aberta** deixa sangue. Quem ficou com o campo pode segui-lo **na hora, sem gastar bloco**:
- o teste é o do rastro da espécie, **6 mais fácil**; e **3 mais difícil** a cada perseguição já feita naquele bloco (a presa ganha distância);
- passou: acha **o mesmo bicho, com o PV e as feridas com que fugiu**, e viu primeiro (a margem dá a posição, como em 9.7);
- falhou, seguiu a procura, ou voltou: perdeu-o. O bicho segue na contagem, e na próxima vez é um bicho inteiro.

9.12 **A coleta** (minério, madeira, erva) é uma saída como a da caça, com blocos pesados. Um teste por bloco: **2d20 + atributo ÷ 10 + maestria de coleta** contra **20 + 4 por categoria da matéria + 8 × o que falta dela** (1 − o que há ÷ teto).

| Matéria | Atributo | O bloco que passa rende | Volta por dia (do teto) |
| --- | --- | --- | --- |
| minério (`metal:N`) | Força | 1 | 0,4% |
| madeira (`madeira:N`) | Força | 2 | 2% |
| erva (`erva:N`) | Percepção | 1 | 4% |

Passar por 5 rende 1 a mais (e mais 1 a cada 5). Falhar por menos de 5 ainda rende 1; por 5 ou mais, nada. **Nunca se tira mais do que há:** o que acabou, acabou. O que se tira sai do `coleta` do ermo e entra na carga **no mesmo evento**.
Em todo bloco de coleta o acaso rola (9.5): quem corta lenha não está olhando o mato.

9.13 **A virada do dia** (`caca.virada`), em todo lugar com teto:
- **os bichos criam devagar:** de cada espécie nascem, por dia, contagem × cria × (1 − contagem ÷ teto). A cria é 4% (Comum), 2,5% (Incomum), 1% (Raro para cima). Nunca passa do teto;
- **com menos de dois, a espécie não cria:** espera um casal de fora, que vem, em média, a cada 60 dias (Comum), 100 (Incomum) ou 180 (Raro para cima). **Espécie caçada até o fim some por muito tempo;**
- **o chefe não cria:** morto, nasce outro, em média, em 180 dias (Épico) ou 364 (Único). O Lendário não nasce de novo;
- **a matéria volta** pela fração da tabela (9.12), até o teto.

A parte quebrada de cada conta vira a chance de mais um, pela sorte do mundo: mesma semente, mesmo ermo.

9.14 **A maestria de caça e a de coleta** (`maestria.caça`, `maestria.coleta`) sobem por blocos, como a das armas (5.5): 40 blocos de procura (ou de coleta) fazem um Iniciante; 160, um Treinado; 500, um Mestre; 1.500, um Lendário. A de caça soma no rastro; a de coleta, no teste da coleta.
De Mestre para cima os blocos não bastam: pede o **feito**. Na caça, ficar com a carcaça de um bicho Raro (para Lendário, Épico). Na coleta, ter tirado matéria Rara com a própria mão.

9.15 **Povoar um ermo** (`caca.povoa`, o gerador ou o Mestre): o habitat e o perigo (1, a borda; 2, o interior; 3, o coração) dão as espécies que vivem ali, cada uma no teto, e a matéria.

| Habitat | A borda | O interior, além disso | O coração, além disso |
| --- | --- | --- | --- |
| floresta | corça 80, javali 40, lobo 12, surucucu 8, urso 3 | pantera 2, aranha 6 | |
| campo | corça 80, lobo 12 | | |
| brejo | ratazana 90, javali 40, surucucu 8 | trasgo 2 | basilisco 1, hidra 1 |
| serra | lobo 12, urso 3 | pantera 2, grifo 2 | serpe 1, dragão 1 |
| caverna | ratazana 90, urso 3 | aranha 6, trasgo 2 | basilisco 1 |
| ruína | ratazana 90, surucucu 8 | aranha 6, trasgo 2 | basilisco 1, serpe 1, hidra 1, dragão 1 |

| Habitat | A matéria (o teto) |
| --- | --- |
| floresta | madeira Comum 200, erva Comum 60, madeira Incomum 20, erva Incomum 10; no interior, madeira Rara 4 e erva Rara 3 |
| campo | erva Comum 80, madeira Comum 40, erva Incomum 8 |
| brejo | erva Comum 90, erva Incomum 20, madeira Comum 60; no interior, erva Rara 5 |
| serra | minério Comum 150, minério Incomum 20, madeira Comum 60; no interior, minério Raro 5 |
| caverna | minério Comum 100, minério Incomum 30; no interior, minério Raro 6 |
| ruína | minério Comum 40, minério Incomum 10, erva Comum 30; no coração, minério Raro 4 |

**O bicho raro é contado:** uma floresta inteira tem duas panteras e seis aranhas, e cada uma que morre leva meio ano para voltar.

9.16 **Na mesa.** O `caca.mesa` põe na `MESA.md`: os ermos vizinhos e o que se sabe deles (a fartura, em palavras), a mão de caça e de coleta, a saída aberta e o que falta decidir, o resumo dos bichos dali (`bichos.mesa`, sem os chefes), e uma linha marcada **SÓ O MESTRE** com a contagem e a chance do acaso.

### A régua do caçador de começo (medida)

O robô das provas: nível 10, gente gerada, de arco, espada de reserva, cota e elmo de malha, tudo Comum, a ordem simples ("atacar"), no ermo de começo (a borda da floresta). As lutas são as de verdade, das vidas do banco.

| A luta (de longe, o bicho surpreendido), em 300 vidas | Lutas | Carcaças por luta | Ele cai | Ele morre |
| --- | --- | --- | --- | --- |
| uma corça, do alto e encurralada | 1.635 | 1,00 | 0,2% | 0% |
| duas corças, do alto e encurraladas | 1.560 | 1,93 | 3,7% | 2,3% |
| uma corça encurralada, sem o alto | 1.026 | 0,99 | 1,0% | 0,6% |
| duas corças, do alto, sem cerco | 989 | 0,43 | 0,7% | 0,3% |
| duas corças, do alto e numa passagem de um, sem cerco (o cauteloso) | 2.003 | 0,43 | 0,1% | 0,05% |
| uma corça, do alto, sem cerco (o cauteloso) | 1.285 | 0,25 | 0% | 0% |
| uma corça, sem terreno nenhum | 904 | 0,27 | 0,4% | 0,2% |
| a presa ferida, no fim do sangue (em qualquer posição) | 991 | 1,10 | 0,2% | 0% |
| a luta que ele não escolheu (o bicho investiu, ou o alcançou) | 22 | 0,09 | 86% | 77% |

| A vida de 30 dias (300 vidas de cada) | Tira por dia | Sai ferido ou morto | Morrem em 30 dias |
| --- | --- | --- | --- |
| o caçador do banco, que encurrala sempre que o rastro lhe dá o cerco | 1,95 diária | em 5,2% das saídas | 21% |
| o cauteloso, que só encurrala a corça sozinha, e do alto | 1,70 diária | em 1,3% das saídas | 6% |
| o afoito, que ataca tudo o que aparece | 1,6 diária, enquanto vive | | 100% (a metade até o Dia 2) |

Do que o caçador tira, a loja paga 60%: 4,6 de prata por dia. Viver custa 3, e o conserto do que ele veste, 0,7 (peça Comum aguenta dez lutas).

**Como ler:** de arco e do alto, a corça sozinha quase não fere. Quem a encurrala fica com a carcaça; quem não a encurrala fica com um quarto delas, e com o sangue das outras para seguir. Duas corças encurraladas são o dobro da carne e o perigo de verdade. O que mata o caçador de começo é o bicho que o viu e o alcançou, e a presa encurralada que chegou nele: quem cai sozinho no mato morre seis vezes em dez (3.13).
**A faixa do contrato (ferido ou morto em 2 a 12% das saídas) só é batida por quem encurrala:** o cauteloso fica abaixo dela, vive mais e ganha menos.

### O banco de provas da caça

`python3 provas_caca.py` (o `provas_mundo.py` também o roda). As metas são as do contrato da etapa 2. O dado é o de verdade: as medidas mudam um pouco de uma rodada para outra. **18 de 18 passam.**

| O que se mede | Meta | Medido |
| --- | --- | --- |
| o caçador de nível 10, com peças Comuns, no ermo de começo, tira por dia (o despojo ao preço de base) | 1,5 a 4 diárias | 2,00 diárias (75 vidas de 30 dias; nas rodadas, de 1,9 a 2,1) |
| o mesmo robô sai ferido ou morto | em 2 a 12% das saídas | em 4,9% (nas rodadas, de 4 a 6%); morreram 17 de 75 em 30 dias |
| o mesmo robô, afoito, morre em 30 dias | em 70% das sementes, ou mais | em 100% (75 de 75); a metade até o Dia 2 |
| caçar 60 corças derruba a contagem, e o rastro fica mais difícil | sim | três mundos: de 80 para 44, 40 e 40; o rastro, de 20 para 25 e 26 |
| e a espécie volta a nove décimos do teto | em 30 a 120 dias | em 47, 50 e 51 dias sem caça |
| nenhuma contagem negativa; nunca aparece mais do que há | sim | 150 vidas, nenhuma; o ermo de 5 corças vai a zero, e vazio não dá encontro; com uma corça só, nunca aparecem duas |
| o núcleo do chefe entra no Livro de Itens com `de` e `onde` | sim | a serpe morta: núcleo Épico, `de` serpe, com dono e a história; a carcaça que ninguém abriu: núcleo no ermo, sem dono, e quem passa num rastro o acha |
| o que sai do ermo é o que entra na carga (a conta fecha) | em toda vida | 150 vidas: 2.009 bichos fora da contagem (2.001 carcaças aproveitadas, 8 deixadas no mato), 743 nascidos; nenhuma conta aberta |
| a ameaça é lida antes; deixar e fugir do bicho que não viu o caçador não custam nada | sim | a frase inteira no que ele lê; nenhuma luta, nenhum evento de luta; a saída aberta sobrevive a fechar e abrir o estado |
| o bicho que viu o caçador investe e persegue pela índole | lobo: 70% e 90% | 72% e 90%; alcançado em 21 de 45 testes de Agilidade; os 100 desfechos com o começo e a surpresa certos |
| a luta é a do `ato.py luta` | sim | abre no arquivo, registrada no turno, parada antes da 1ª rodada; um evento `luta` e um `despojo`; com ela aberta o turno não fecha |
| a presa ferida, seguida pelo sangue, é o mesmo bicho | sim | 10 de 10 com o PV e as feridas com que fugiram; o relógio não andou; a segunda perseguição pediu 3 a mais |
| quem morre no ermo fica lá com o que vestia | sim | as 4 peças no ermo, sem dono; o estado inteiro; quem passou num rastro as achou |
| a virada: de 20 em 80, a corça volta a nove décimos | em 30 a 120 dias | em 68 a 97 dias (a do meio: 74); nunca acima do teto |
| caçada até o fim, some por muito tempo | mais que a de cima | a primeira volta em 1 a 60 dias; as 72, em 128 a 197 (a do meio: 177) |
| o chefe demora a nascer | 180 dias, em média | 174 dias (60 mundos) |
| a matéria volta devagar, até o teto | sim | a mina esgotada (teto 150): 17 em 30 dias, cheia em 630; o minério Raro (teto 5): 0 em 30 dias |
| a coleta: o que se tira sai do ermo no mesmo evento; rareando, pede mais | sim | 56 de minério em 24 blocos, a conta fechada; o número vai de 20 a 26; o veio esgotado não dá mais nada |
| a maestria de caça sobe por blocos, e Mestre pede o feito | sim | 40 blocos: Iniciante; 600 sem feito: Treinado; com a carcaça Rara: Mestre; com a Épica: Lendário |
| o robô vive de verdade, e a prata do mundo fecha | sim | 0,96 refeição e 1,01 cama por dia; 353 consertos pagos; nenhum morto de fome; a prata fecha nas 75 vidas |
| vinte pedidos errados | recusados, sem mudar nada | 20 de 20; sem argumento, só o uso; sem ermo vizinho, a caça não faz nada |
| a mesa da caça é curta, e a contagem é só do Mestre | cabe nos 8 KB da `MESA.md` | 1,0 a 1,2 KB; a MESA inteira da vila de prova (mercado, forja e mata): 5,5 KB |

### O que este capítulo não resolve (fica dito)

- **Só quem está em cena caça.** A contagem só cai pela mão do personagem (e de quem o Mestre puser para caçar com `quem=`). Os caçadores do povo e os rivais são da etapa 3 e da 5.
- **Não há viagem.** O ermo é o vizinho, a um número fixo de blocos. Dormir no mato, a rota e o perigo da estrada são da etapa 3.
- **O corpo dos companheiros** só sente a luta: a fome, o sono e o cansaço da caminhada deles não andam.
- **Não há peso.** A carga não tem limite: quem mata dez corças traz dez corças.
- **A carne não estraga,** e não se come da própria carga: a refeição é a da taverna (5.4).
- **Não há tempo de céu:** chuva, neblina e lama (3.9) só entram na luta se o Mestre as puser; a caça só põe o escuro.
- **O bicho não vem à vila.** A ninhada que passa do teto e vira praga é das frentes.
- **Com a saída aberta, os outros atos não são barrados.** O `caca.py` recusa abrir outra saída, mas o `ato.py` e o `mercado.py` não sabem dela: quem está no mato não dorme na pousada nem vende na loja, e quem cuida disso é o Mestre. O `turno.py fecha` também não a barra, de propósito: a escolha diante do bicho pode ficar como pergunta do turno (com a luta aberta, ele recusa).

### Os comandos

```
python3 caca.py ver                              os ermos vizinhos (o que se sabe), a sua mão, a saída aberta (e o que o caçador lê, com o bicho à frente)
python3 caca.py sair mata alvo=corça blocos=2    sai para caçar: a ida, e a procura até aparecer alguma coisa (sem alvo: o que aparecer)   ·   com=ID,ID leva gente junto
python3 caca.py atacar inicio=longe vantagem=alto,cerco      ataca o que apareceu: monta a luta e mostra o quadro
python3 caca.py luta "Aldric: atacar"            roda a luta até a próxima parada (é o ato.py luta roda); no fim, as contas do despojo
python3 caca.py sangue                           segue o sangue da presa que fugiu ferida (sem gastar bloco)
python3 caca.py deixar   ·   caca.py fugir   ·   caca.py segue   ·   caca.py volta
python3 caca.py coletar metal:0 serra blocos=2   sai para tirar matéria
python3 caca.py conta [ERMO]                     SÓ O MESTRE: a contagem, o número do rastro de cada espécie, a chance do acaso, o que ficou no chão
python3 caca.py povoa mata floresta perigo=1 vizinho=vila "como foi"      o Mestre povoa um lugar que já existe
python3 provas_caca.py                           o banco de provas da caça
```

Para os outros módulos: `caca.sair` · `caca.coletar` · `caca.atacar` · `caca.deixar` · `caca.fugir` · `caca.luta_roda` · `caca.acerta` · `caca.sangue` · `caca.segue` · `caca.volta` (todos devolvem `{fase, texto, ...}`; a fase é `encontro`, `luta`, `procura`, `fim` ou `morto`)
· `caca.saida(pessoa)` (a saída aberta) · `caca.posicao(encontro)` · `caca.bichos_de(E, lugar)` · `caca.rastro_contra(E, lugar, espécie)` · `caca.acaso(E, lugar)` · `caca.povoa(E, lugar, habitat, perigo, vizinho=)` · `caca.virada(E)` · `caca.mesa(E)` · `tabelas_caca.fauna(habitat, perigo)`.

O que a caça escreve no estado (sempre por evento): na pessoa, `marca.caca` (a saída aberta), `marca.abates` (as carcaças com que ficou), `marca.feito_caça` e `marca.feito_coleta` (a categoria mais alta que a mão já tirou), `treino.caça`, `treino.coleta`, `maestria.caça`, `maestria.coleta` e a carga; no lugar, `habitat`, `perigo`, `longe`, `bichos`, `teto`, `coleta`, `coleta_teto`; no Livro de Itens, o núcleo do chefe e as peças de quem morreu no ermo. O cenário e o arquivo de cada luta ficam na pasta `lutas/` do save.
