rascunho: o DESENHO.md manda (depois da revisão: nenhuma classe toca o total nem o teto da obra, nem a Mítica e a Primordial; a cadeia do Legatário são as quatro obras do mestre; o Fiel do Santuário no lugar do Juramentado; as geradas são função pura da semente; os feitos tortos são um banco de 32 ou mais, 12 por mundo, e as listas daqui são só o começo; o voto para e pergunta)

# D5 — AS CLASSES (Motor 10, parte 2)

Desenho do campo D5: o que é uma classe, a escada das raridades, as três chaves, como o mundo oferece e o jogador escolhe, uma por vez e a segunda com tributo, o que
a classe dá, a fraqueza e o voto, os degraus dentro da classe, como se perde, o núcleo feito à mão (46 classes), o gerador (perto de mil classes por mundo; mais de
3 milhões no espaço das sementes), a gente do mundo com classe e a medida na régua. **Nada disto está no motor.** Os números são de partida; quem decide é o banco.

**Como se mediu.** O pacote de cada classe de luta (as assinaturas dela juntas, mais a passiva) entrou no remendo de luta do D3 (uma cópia fora do repositório, com
três ganchos a mais: o golpe de voto, a resistência à carga e a coragem; nada tocou o save) e rodou o duelo de iguais do banco: nível 50, mão de Mestre, tudo Raro,
começando perto, **8.000 lutas por linha** (erro de ±0,6; as rodadas de ensaio, 4.000, ±0,8), metade com a classe no lado A. As de grupo, no **3 contra 3** de
iguais (3.000 lutas, ±1,2). As de ofício, na **régua de feitio do D2** (pontos de feitio por obra, pela regra exata da faixa, nos cinco ferreiros de referência). A
gente, em **três mundos de teste** gerados (sementes 101 a 103; nunca o mundo de verdade). A crônica, em 40 sementes de exemplo do `historia.py`.
Marcas: **(m)** medido · **(c)** conta · **(d)** desenho, sem vitória a medir.

**Quatro palavras.** **Raridade** é o lugar da classe na escada (Comum a Primordial). **Degrau da classe** é o quanto ela cresceu dentro dela (Recebida, Firmada,
Plena). **Grau** é o da habilidade, do D3 (Iniciante, Aprendiz, Adepto, Perito, Mestre, Grão-Mestre: **I·Ap·Ad·P·M·GM**). **Mão** é a maestria (Leigo a Lendário).

---

## 1. O que o jogador pediu e o que esta parte entrega

> **Dia 34:** "em SATISFY, eles usam habilidades de classe para batalhar entre outras coisas, convencer, trabalhar e copiar. Existem essas habilidades, exemplo a
> dança da espada de [um ferreiro lendário]."
> **Dia 35:** "Mesma coisa com habilidades, dons, talentos [...] Tipo assim, um Berserker que quando entra em fúria tanto tempo, ele consegue mais dano [...] Fora as
> classes, tem classe secreta, classe lendária, classes épicas, tem várias classes, milhões de classes. Paladino, bruxa de sangue, essas coisas."
> **Dia 24:** "[...] deve existir a possibilidade desde a apelação até o normal e fraco."

**O que entrega:**
1. **O sistema** (2.1 a 2.9): a escada de oito raridades e as Secretas; as três chaves (número, feito, segredo); a OFERTA do mundo e o "aceito" do jogador; uma classe
   por vez, a linha, e a segunda só da Rara para cima, com tributo; as assinaturas, as passivas e a variedade de estados; a fraqueza, o voto e a penitência; os três
   degraus dentro da classe; como se perde.
2. **O núcleo feito à mão** (2.10): 46 classes. Ficha completa das 10 Comuns, 8 Incomuns e 11 Raras (3 secretas); ficha curta das de cima. O paladino de Belogar é o
   **Fiel do Santuário** (e o **Fiador de Juras**, Lendário); a bruxa de sangue, a **Sangradeira**; o berserker, o **Sanhudo**.
3. **O caminho de Ferord** (2.11): da Comum (Malhador) à Lendária herdada de um mestre ferreiro morto da crônica (o Legatário da Bigorna), passo a passo.
4. **Milhões de classes** (2.12): as cruzadas de duas e de três mães, as Lendárias que nascem dos mortos da crônica, as Únicas de quem lidera uma medida, as
   Secretas por feito torto, os nomes do `nomes.py`.
5. **A gente do mundo com classe** (2.13) e **o que muda no mundo** (2.14): a encomenda, a fama, a cobiça.
6. **A medida** (2.15) e o banco (5).

### O que a medida mostrou antes de tudo (cinco achados que mudaram o desenho)
1. **Com as assinaturas no Iniciante (o que o D3 propôs), a raridade não aparece no dia em que a classe chega.** As Raras entraram com +1,5 a +7,6 e as Épicas
   com +2,5 e +2,6 (m): a Épica nova valia menos que a Rara. Por isso **a assinatura nova entra no grau da raridade**: Comum no Iniciante, Incomum e Rara no Aprendiz,
   Épica e Única no Adepto, Lendária pela cadeia. Assim a Comum chega valendo um efeito fraco, a Rara um normal, a Épica um forte (2.15).
2. **Três assinaturas de luta no Grão-Mestre passam do teto da Rara.** O Malheiro com Trunfos, Tranco e Quebra deu +25,5 no topo; o Sanhudo com Sanha e Teima, +20,3 a
   +22,0 (m). A regra nova: **uma assinatura forte de duelo por classe**; as outras dão estado, grupo, ofício, fala ou andar. O Malheiro cai para +16,5 (m).
3. **As de grupo explodem no grupo.** O Alferes com o Brado no Grão-Mestre deu +35,5 no 3 contra 3 (m). No Alferes, o Brado para no Mestre: +26,2 (m).
4. **O item segue decidindo.** O Legatário no topo, tudo Raro, contra o conjunto Épico sem classe vence 16,3% (m); com uma segunda classe por cima, 22,7% (m). A pior
   dupla medida dá +34,9 entre iguais: abaixo de 40.
5. **A classe de ofício nunca mexe na chance da categoria.** A linha inteira do ferreiro ligada (prumo 5, têmpera 3, lastro e o molde): a chance de cada categoria
   muda **0** (c, conta exata). O que a classe dá na forja é efeito, cheio, tempo e matéria; a escada medida e a Lendária de 1 em 4 ficam como estão.

---

## 2. As regras, para a mesa

### 2.1 O que é uma classe
Uma IDENTIDADE que o mundo reconhece: um nome, uma raridade, três assinaturas ou mais, uma fraqueza e, da Rara para cima, um voto ou um fardo. **Não se escolhe num
menu: o mundo reconhece e oferece; o jogador aceita ou recusa.**

| Traço | O que é |
| --- | --- |
| raridade | Comum, Incomum, Rara, Épica, Única, Lendária, Mítica, Primordial; e as Secretas (de Rara a Lendária) |
| mães | o caminho (ou os caminhos) de onde ela vem: um dos 17 (as quatro mãos de arma, os nove ofícios, as quatro tradições) |
| chaves | NÚMERO (a mão), FEITO (o que se fez, com risco, registrado), SEGREDO (quem ensina, ou o escrito): 2.3 |
| assinaturas | habilidades do catálogo do D3 (a origem "classe" dele) ou próprias da classe, e passivas. Não ocupam vaga (D3 2.1) |
| fraqueza | toda classe tem uma, escrita e pequena: morde numa situação |
| voto ou fardo | da Rara para cima: uma promessa que se quebra (2.7) ou um peso que morde em cena |
| linha | as classes que têm uma mãe em comum. Subir na linha guarda as assinaturas antigas (2.5) |

### 2.2 A escada

| Raridade | Quantas | Chaves (número · feito · segredo) | Quem oferece | Assinaturas | A nova entra no | Teto do grau | Estados | Dano fixo | O preço | Valor: entrada · topo |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Comum** | uma por caminho (10 feitas à mão; 7 pelo molde) | Iniciante · o trabalho visto · — | o povo do lugar | 1 habilidade e 2 passivas | Iniciante | Perito | 1 família | 0 | fraqueza leve | 1 a 5 · até 10 |
| **Incomum** | uma ou duas por caminho (8 feitas à mão) | Treinado · o EXAME de quem sabe · — | quem tem a mão de Mestre no caminho | 2 habilidades e 1 passiva | Aprendiz | Mestre | 2 | 0 | fraqueza | 3 a 7 · até 12 |
| **Rara** | 8 feitas à mão e as cruzadas de duas mães (130 pares) | Treinado nas duas mães (ou Mestre numa mão de arma, se as duas mães são de luta) · a PROVA, uma vez só · — | quem sabe, ou a cena | 3 habilidades, uma própria | Aprendiz | Grão-Mestre | 3 | até 3% | fraqueza e voto ou fardo | 5 a 10 · até 20 |
| **Épica** | 5 feitas à mão e as cruzadas de três mães (598 trios) | Mestre numa mãe e Treinado na outra (nas outras duas, na de três mães) · um FEITO do mundo · o SEGREDO | o guardião do segredo | 4 habilidades, uma forte | Adepto | Grão-Mestre | 4 | até 5% | e um preço que dói | 10 a 20 · até 26 |
| **Única** | uma viva por vez: 8 medidas e 3 feitos únicos | Mestre no caminho · o primeiro da MEDIDA por uma estação, ou o feito único · — | a medida (o rol, o ranking) | 4 | Adepto | Grão-Mestre | 4 | até 5% | a cobiça: o mundo sabe | 10 a 20 · até 30 |
| **Lendária** | uma por mundo cada: 1 por lenda morta e por mestre de peça Única ou Lendária (9 a 18 por mundo) | Lendário na mãe · o LEGADO (a peça, o caderno, o túmulo) · a CADEIA | o legado chama quem tem a mão | 5, uma de teto apelão | Iniciante, e +1 grau por obra do mestre reforjada (até o Perito) | Grão-Mestre | 5 | até 10% | o preço de entrada | 15 a 25 · até 40 |
| **Mítica** | quase nenhuma (1 feita à mão) | um núcleo Mítico, um pacto ou um ano de vida · um rito | o rito | 5 e uma regra do mundo que dobra | por evento | Grão-Mestre | 5 | até 10% | o preço do pacto (SÓ O MESTRE) | por evento, até 40 |
| **Primordial** | uma, dormindo na crônica | só por evento do Mestre | — | o mundo muda ao redor | por evento | — | — | — | o mundo inteiro quer o que ela guarda | — |
| **Secreta** | 12 feitos tortos × o caminho de quem faz (204 por mundo) | só o FEITO TORTO, nunca listado | ninguém: o próprio feito | como a raridade dela | idem | idem | idem | idem | o fardo que nasce junto | idem |

- **Valor** = pontos de vitória no duelo de iguais (a régua do PROJETO 2.1), **na entrada** (o dia em que chega) e **no topo** (todas as assinaturas no teto do grau).
  A classe de grupo mede-se no 3 contra 3; a de ofício, na régua de feitio do D2 (entrada: Comum até 0,15 · Incomum e Rara até 0,30 · Épica e Única até 0,60 ·
  Lendária até 1,20; topo: no máximo uma força acima); a de fala, nos pontos de chance do teste de fala (D3 2.6). Os medidos estão em 2.15.
- **À mesa:** "no dia em que chega, a classe Comum vale um efeito fraco, a Rara um normal, a Épica um forte, a Lendária saída da cadeia um forte alto. Depois cresce
  pelo uso, como as habilidades, até o topo da raridade."
- **Uma forte de duelo por classe.** A raridade sobe a variedade, não o dano (PESQUISA, lição 11): cada classe tem no máximo uma assinatura de teto forte (ou apelão)
  no duelo; as outras põem estados, ajudam o grupo, trabalham, falam ou andam.
- **O dano fixo** (a passiva que soma dano sempre) entra no grupo TÉCNICA do D1, junto com as habilidades (até +40%). O dano contra um tipo vale o dobro do teto. O
  número fixo (acerto, Defesa, coragem, resistência à carga) entra na conta P3 do D1: somado ao das peças e das habilidades, até +8 cada. Ninguém fica imune.

### 2.3 As três chaves

| Chave | O que é | Como o script vê |
| --- | --- | --- |
| NÚMERO | a mão nas mães da classe | a maestria (já existe) |
| FEITO | o que a pessoa fez, com risco | o **trabalho visto** (contagens nos eventos); a **prova** (um ato declarado); o **feito do mundo** (o que vira notícia, 22.3, com a pessoa nele) |
| SEGREDO | quem ensina, ou o escrito | a gente com nome que tem a classe (ou a mão de Mestre nas mães) e opinião 3 ou mais sobre você; o escrito (item `escrito` com `classe`); o lugar (o túmulo, a oficina velha) |

- **O trabalho visto (Comum):** 50 blocos de bancada no ofício ou 20 obras rematadas · 10 saídas ao ermo com rastro · 5 lutas de verdade vencidas · 30 dias de guarda
  num lugar · 10 tratamentos · 5 viagens de negócio com lucro · 10 bênçãos dadas · 5 vezes andou escondido com risco (a lista inteira em `tabelas_classes`).
- **O exame (Incomum):** a obra, o tiro, o tratamento ou a venda feitos diante de quem tem a mão de Mestre no caminho (ou a classe Incomum ou maior dele) e não o odeia
  (opinião 0 ou mais). Quem examina cobra o salário de um bloco da mão dele (14.7). Reprovar não fecha nada: tenta-se de novo.
- **A prova (Rara):** um ato declarado, **uma vez só**, com a chance mostrada antes (o script faz a conta e rola uma vez). Passou, a classe é oferecida na hora.
  Falhou, **aquela classe fecha para sempre** (as outras ficam abertas). A oferta da prova fica aberta até o jogador dizer "faço agora": ele escolhe a hora.
- **O feito do mundo (Épica):** o que vira notícia com a pessoa nele. **O segredo:** quem ensina pede 10 blocos de lição juntos (no salário dele); o escrito, 30
  blocos de estudo.
- **A pista.** O jogo nunca lista a chave inteira: a classe só aparece na mesa quando a oferta chega. Antes disso, o que se sabe vem do mundo: quem tem a classe conta
  como a ganhou (o `saber.py`, do tamanho do saber dele), a notícia de quem a ganhou ("dizem que..."), o escrito. O banco confere que toda classe do núcleo tem pelo
  menos uma fonte de pista no mundo gerado (meta 6).

### 2.4 Como chega: o mundo oferece, o jogador escolhe
Quando as chaves fecham, o `classe.py reconhece` (no fim de cada ato, como o talento que aparece) põe a **OFERTA** na caixa (22.4) e numa pergunta do turno.
**Nada entra sem o "aceito".** Um exemplo, com Ferord hoje:

> 🜂 **O MUNDO RECONHECE.** No lugar onde você trabalha já te chamam de **MALHADOR** (classe Comum, da forja). Ela dá **O Malho Quente** (habilidade; entra no
> Iniciante; a obra de 3 blocos ou mais que fecha quente ganha prumo), **Olho de Oficina** (lê à vista a categoria e a durabilidade de uma peça) e **Mão de Vila**
> (o conserto devolve 7 por bloco, não 5). Fraqueza: longe de um lugar de povo, o conserto rende a metade e o Malho não esquenta. Sem voto.
> **Pergunta 3.** (a) aceito · (b) agora não (a oferta volta em 28 dias)

| Raridade | Quem oferece | Se recusa |
| --- | --- | --- |
| Comum | o povo do lugar (a notícia: "o malhador de...") | volta em 28 dias |
| Incomum | quem examinou (a gente com nome) | volta em 28 dias |
| Rara | quem sabe (um mestre, um templo, um capitão), ou a própria cena, propõe a PROVA | a prova não fecha; volta em 28 dias |
| Épica | o guardião do segredo (um mestre vivo, ou o escrito achado) | uma vez por estação |
| Única | a medida, no fim da estação | o segundo da medida recebe a oferta |
| Lendária | o legado (a peça, o caderno, o túmulo) chama quem tem a mão Lendária | o legado espera outra pessoa |
| Secreta | o feito torto: "algo mudou em você" | não volta |

- **Aceitar deixa** a classe que se tinha, se não é da mesma linha (2.5): a oferta diz isso antes, com o que se perde.
- **A gente do mundo** aceita ou recusa pela semente (o rival aceita o que sobe a conta dele; quem tem família no lugar recusa a classe que o leva embora).

### 2.5 Uma por vez; a linha; a segunda classe e o tributo
- **Uma classe por vez.** Aceitar outra deixa a de antes.
- **A LINHA.** A classe nova que tem entre as mães um caminho da que você tem é da mesma linha. **Subir na linha guarda as assinaturas antigas** como de classe (não
  ocupam vaga), cada uma com o teto que tinha. Ex.: Malhador (forja) → Temperador (forja) → Marcador de Runas (forja e encanto): o Malho Quente segue de classe, até o Perito.
- **Fora da linha**, as assinaturas antigas viram habilidades comuns: ocupam vaga (sem vaga, o jogador escolhe o que esquecer), guardam o grau e param no Perito
  (o teto da lição, D3 2.7).
- **A SEGUNDA CLASSE** (duas identidades): só quando as duas são Rara ou maior **e a primeira está Plena** (2.8). Chega como qualquer classe, pelas três chaves dela,
  e cobra o **TRIBUTO**:
  1. as assinaturas da segunda param no Mestre, nunca no Grão-Mestre;
  2. as duas fraquezas mordem, e os dois votos valem;
  3. a marca da cena (D3 2.2) vai às assinaturas de uma classe só (a mais usada na cena): quem faz duas coisas aprende metade de cada;
  4. se o nível voltar a subir (o desenho dos dons, D4), metade dos pontos de cada subida vai para o atributo escrito na segunda (a Força do Sanhudo, a Afinidade do Marcador).
- **Medido:** a pior dupla (o Legatário no topo, com o Malheiro de segunda) dá +34,9 entre iguais e vence 22,7% contra o conjunto Épico sem classe (m). O teto da
  Lendária já segura o duelo; o tributo segura a escada do grau e a variedade (uma pessoa não junta tudo).

### 2.6 O que a classe dá
- **As assinaturas** são habilidades do catálogo do D3 ou **próprias** (só daquela classe; não se copiam, D3 2.7). A nova entra no grau da raridade (2.2), sobe pelo uso
  pela escada do D3 (com os freios dele: a marca da cena, um grau por dia, a mão que segura o grau, o feito do Mestre) e para no teto da raridade.
- **As passivas** valem sempre, sem grau: uma regra pequena (ler à vista, o pedágio pela metade) ou um número fixo pequeno.
- **A variedade:** as famílias de estado que a classe põe ou aguenta (cabeça, pernas, sangue, ânimo, exposto e amolecido, mana, veneno, fogo): Comum 1, Incomum 2,
  Rara 3, Épica 4, Única 4, Lendária 5. E os campos (batalhar, curar, convencer, trabalhar, copiar, mover): da Rara para cima, pelo menos dois.

### 2.7 A fraqueza e o voto
- **A fraqueza** é escrita, pequena e de situação (−2 numa coisa, numa hora). Nunca tira a escolha do jogador.
- **O voto** (Rara para cima, nas classes que o pedem) é uma promessa que **o script vê**: a ordem de recuar, o golpe em quem se rendeu, o pedido de socorro recusado na
  caixa, a peça forjada para quem a classe proíbe. Algumas classes deixam escolher entre dois ou três votos ao aceitar.
- **Quebrar o voto:** a classe **APAGA** na hora (as assinaturas dormem, a passiva some; a mesa diz). Abre a **PENITÊNCIA**: 28 dias para um feito de dureza 4 a
  serviço do voto (o script vê). Feito, a classe acende um degrau abaixo (nunca abaixo de Recebida). Sem ele, a classe se perde (as assinaturas viram comuns, no
  Perito) e a porta fecha. Algumas abrem a secreta sombria: o Fiel do Santuário que quebra vira **Cinza-de-Voto**.
- **O fardo** (nas classes sem voto) é um peso que morde em cena sem quebrar nada: a notícia que leva o nome dele, a fera que o caça, a guerra que o chama.

### 2.8 Os degraus dentro da classe

| Degrau | Como chega | O que dá |
| --- | --- | --- |
| **RECEBIDA** | aceitar | as assinaturas no grau de entrada; as passivas |
| **FIRMADA** | todas as habilidades da classe no Adepto ou acima, e um feito com ela (uma cena de dureza 3 ou mais vencida usando uma assinatura) | a porta da classe de cima na linha (a oferta da Incomum pede a Comum Firmada, quando a pessoa já tem uma classe na linha); a passiva com número vai ao valor cheio |
| **PLENA** | todas no Mestre (ou no teto, se o teto é menor) e um feito de dureza 5 com a classe, que vira notícia | o TÍTULO ("Ferord, o Malhador": a fama soma de novo o da raridade, 2.14); a porta da segunda classe (Rara para cima); ensina as assinaturas do D3 da classe como mestre (D3 2.7) |

À mesa: "CLASSE: Malhador (Comum) · Firmada · Malho Quente no Adepto, 31 de 80 · para Plena: o Malho no Perito e um feito de dureza 5".

### 2.9 Como se perde
1. **Trocar** por outra fora da linha (2.5).
2. **Quebrar o voto** e não fazer a penitência (2.7).
3. **A Única** passa a quem supera na medida, no fim da estação. Quem perde guarda as assinaturas como comuns (no Perito), e o título vira "o que foi".
4. **A Lendária** volta ao legado na morte do dono: a peça, o caderno ou o túmulo chamam o próximo. Se o legado se destrói, a classe some do mundo.
5. **A morte** leva todas. O herdeiro (25.4) não herda classe, como não herda a mão; mas o legado da Lendária fica na família, e o herdeiro com as chaves pode ouvi-lo.
6. **A Mítica** cobra o pacto; **a Primordial**, só por evento.

### 2.10 O núcleo feito à mão (46 classes)
**Como ler.** **H** = habilidade do catálogo do D3 (sobe pelo uso) · **P** = própria da classe (habilidade só dela; os números por grau na ordem I·Ap·Ad·P·M·GM) ·
**ps** = passiva (sem grau). "Medido" = entrada · topo. **Na mesa**, toda classe aparece em "Você" (a linha da classe, o degrau, o que falta para o próximo) e as
ordens das habilidades são as do D3 (`fazer HABILIDADE`); a coluna diz só o que é a mais.

#### Comuns (a assinatura entra no Iniciante; teto Perito; sem voto)

| Classe (mãe) | Chaves | As três assinaturas | Fraqueza | Medido · na mesa |
| --- | --- | --- | --- | --- |
| **MALHADOR** (forja) | forja Iniciante · 50 blocos de bancada ou 20 obras | H **O Malho Quente** · ps **Olho de Oficina** (lê à vista a categoria e a durabilidade) · ps **Mão de Vila** (o conserto devolve 7 por bloco; com a ferramenta de mão de reparo, vale o maior) | longe de lugar de povo, o conserto rende a metade e o Malho não esquenta | feitio +0,12 · +0,24 (m) · a janela da peça mostra a categoria sem ler |
| **RISCADOR** (encanto) | encanto Iniciante · 5 gravações tentadas, ou 5 focos e amuletos feitos | H **O Traço Fiel** (nova para o catálogo do D3, teto normal: na gravação, errar por até 1·1·2·2·3·4 grava inteiro) · ps **Pedra que Lembra** (o grau 1 grava com um bloco a menos) · ps **Olho de Runa** (sabe à vista se a peça tem encanto, e de que grau) | o encanto falho tira 5 de durabilidade a mais | (d) · a chance de gravar inteiro na conta |
| **GUARDA-LINHA** (qualquer mão de arma) | Iniciante numa mão · 30 dias de guarda num lugar, ou 5 lutas defendendo um lugar de povo | H **Guarda de Bigorna** · ps **O Posto** (no lugar onde serve, +2 na coragem) · ps **Olho de Sentinela** (+2 em notar a emboscada ali) | −2 no acerto no turno em que anda mais de 2 casas | +1,2 · +6,9 (m) · a postura `bigorna` |
| **PELEJADOR** (fio) | fio Iniciante · 5 lutas de verdade vencidas | H **Riposta** · ps **O Primeiro Talho** (+2 no acerto no primeiro golpe da luta) · ps **Cara de Briga** (+2 no jeito duro da fala) | o guarda e o senhor do lugar começam com −1 de opinião | +3,9 · +7,4 (m) |
| **MATEIRO** (caça) | caça Iniciante · 10 saídas ao ermo com rastro | H **Faro de Trilha** · ps **O Ermo Conhecido** (no ermo de 10 saídas, nunca é surpreendido) · ps **Pé no Mato** (no ermo, o primeiro recuo da luta anda 3 casas) | entre muros, −2 em notar e no rastro | (d) |
| **ERVEIRO** (coleta ou cura) | coleta ou cura Iniciante · 20 colheitas de erva ou 10 tratamentos | H **Mão que Esquenta** · ps **Olho da Erva** (a coleta de erva rende 1 a mais por saída) · ps **Chá de Cama** (o remédio dele soma meio dia de repouso) | −2 na coragem | (d) |
| **TROPEIRO** (comércio) | comércio Iniciante · 5 viagens de negócio com lucro | H **Língua de Feira** · ps **O Preço do Outro Lado** (sabe o preço de um bem no lugar vizinho) · ps **Pé de Estrada** (o pedágio pela metade) | com carga na estrada, o perigo sobe um | (c: a fala do D3) |
| **BENZEDOR** (fé) | fé Iniciante · 10 bênçãos dadas de graça | H **O Benzimento** (nova para o D3: de dia, +1·+1·+2·+2·+3·+4 na coragem e na Firmeza contra maldição por um dia, em 1·2·3·4·6 pessoas; no GM, a casa inteira) · ps **Sente o Mau-Olhado** (sabe, sem rito, se alguém perto tem maldição andando) · ps **Mão de Casa** (a bênção custa 1 de Mana a menos) | não cobra a bênção (o serviço dele é sempre de graça, 14.7) | (d) |
| **ESGUEIRO** (manha) | manha Iniciante · 5 vezes andou escondido ou abriu fechadura com risco | H **Passo Manso** · ps **Mão no Bolso** (+2 em achar) · ps **Cara de Ninguém** (a notícia do furto dele anda uma estrada a menos) | quem o pega lembra −3, não −2 | (d) |
| **CURTIDOR** (couro) | couro Iniciante · 50 blocos de bancada ou 20 obras de couro | H **Ajuste Fino** · ps **Olho de Pele** (sabe à vista a categoria do couro de um bicho morto) · ps **Mão de Correia** (o conserto de couro devolve 7 por bloco) | −1 na fala com nobre (o curtume fede) | (d) |

As outras 7 Comuns (haste, peso, tiro, alquimia, arcano, verde, pacto) saem do **molde de Comum**: a primeira habilidade da lista da mãe (2.12) e duas passivas da
tabela do caminho; o nome, do `nomes.py`.

#### Incomuns (a nova entra no Aprendiz; teto Mestre; sem voto)

| Classe (mãe) | Chaves (o exame) | As três assinaturas | Fraqueza | Medido · na mesa |
| --- | --- | --- | --- | --- |
| **TEMPERADOR** (forja) | forja Treinado · a OBRA-MESTRA: uma peça Incomum ou melhor, com efeito, mostrada a quem tem forja de Mestre | H **A Paciência** · H **Ler a Peça** · ps **O Fogo Certo** (+1 de prumo na obra de matéria Incomum ou melhor) | fora da própria oficina, o prumo de todas as fontes vale 0 e A Paciência não acende (só a faixa: o total nunca muda, o contrato 5.5) | feitio +0,12 · +0,24 (m); com o Malho da linha, +0,48 no topo |
| **RUNEIRO** (encanto) | encanto Treinado · gravar sem errar um feitiço de grau 1 diante de quem tem encanto de Mestre, ou numa mesa de runas 2 ou mais | H **O Traço Fiel** · H **Ler a Peça** · ps **A Runa que Volta** (a peça que ele grava solta o feitiço duas vezes por luta; do Único, três) | cada gravação dá +1 de cansaço | (d) · a peça dele vende como peça e encanto |
| **BESTEIRO** (tiro) | tiro Treinado · uma estação de guarda atirando, ou 10 lutas com arco ou besta | H **Mira Firme** · H **Pé de Lebre** · ps **Recarga de Muralha** (a besta recarrega de graça uma vez por luta; a fresta pede −6, não −8) | colado, perde a primeira ação do turno | (d: o duelo de arqueiros) |
| **ESTANCADOR** (cura) | cura Treinado · 20 feridas tratadas, 3 delas graves | H **Mão que Estanca** · H **Trato de Campo** · ps **Mão Firme** (o tratamento dele soma 2 dias de repouso, não 1) | o pedido de cura na caixa, recusado, custa −3 de opinião | (d) |
| **PREGOEIRO** (comércio) | comércio Treinado · um leilão vencido, ou 10 vendas numa praça num dia | H **O Fio da Conversa** · H **Voz da Praça** · ps **O Lance Alto** (quem dá lance contra ele paga 5% a mais) | todo mundo o conhece: −4 em andar escondido em lugar de povo | (c: a fala do D3) |
| **ANTEPARO** (qualquer mão de arma) | Treinado numa mão · ter guardado alguém numa luta em que você caiu | H **Guarda de Bigorna** · H **A Vigília** · ps **O Corpo na Frente** (guardar não gasta a reação, uma vez por rodada) | não golpeia no turno em que guarda | +3,1 · +9,6 (m) |
| **MONTEIRO** (caça) | caça Treinado · 3 bichos de grau B ou maior caçados | H **Faro de Trilha** · H **A Picada** · ps **O Bicho Lido** (lê o grau e os traços de um bicho à vista; +1 no acerto contra o bicho que rastreou) | contra gente, −1 no acerto | (d) |
| **BOTICÁRIO** (alquimia) | alquimia Treinado · 10 levas de poção vendidas | H **A Medida Certa** (nova para o D3: a leva rende 0·0·1·1·1·2 poção a mais) · H **Olho de Avaliador** · ps **Nariz da Botica** (sabe à vista se a poção ou o veneno é o que diz) | −1 na opinião de sacerdote (o enxofre) | (d) |

#### Raras (a nova entra no Aprendiz; teto Grão-Mestre; fraqueza e voto ou fardo; a PROVA é uma vez só)

| Classe (mães) | Chaves e a PROVA | As três assinaturas (a forte primeiro) | Fraqueza | Voto ou fardo | Medido · na mesa |
| --- | --- | --- | --- | --- | --- |
| **MALHEIRO DE GUERRA** (peso e forja) | peso e forja Treinado · vencer uma luta de dureza 4 com arma de peso da própria mão | H **Trunfos** · H **Golpe de Quebra** · P **Fio Assentado** (1 bloco de bancada: a arma de um aliado, não a sua, ganha +5%·+5%·+6%·+7%·+8%·+10% de dano, grupo PEÇAS, até a próxima luta) | os Trunfos só valem com arma de peso | FARDO: quando uma frente de ameaça chega ao passo 4 no lugar dele, o senhor o chama à guerra (a caixa; recusar, −3 de opinião) | +6,4 · +16,5 (m) · a ordem `fio ALIADO` |
| **MARCADOR DE RUNAS** (forja e encanto) | forja e encanto Treinado · a peça Incomum ou melhor que ele forjou, gravada na primeira tentativa (Afinidade 70 e mesa de runas 1: 48% numa Incomum, 26% numa Rara; c) | P **Runa na Brasa** (diz o feitiço ao abrir a obra de arma, armadura ou escudo; no remate, o teste do encanto rola à parte, sem os blocos do encanto e, até o Raro, sem a essência) · H **O Traço Fiel** · H **Ler a Peça** · e ps **A Peça que Canta** (a peça que nasce encantada ganha +1 de prumo) | na Runa na Brasa, o encanto que falha por 5 ou mais racha a peça (cai uma categoria) | FARDO: a peça marcada leva o sinete dele; quando uma mata alguém com nome, a notícia leva o nome dele, e a família do morto lembra (−2) | feitio +0,12 e o tempo: a gravação não pede 1, 3 ou 9 blocos (Incomum, Rara, Épica) · `forjar ... runa=FEITICO` |
| **FIEL DO SANTUÁRIO** (fé e uma mão de arma) — o paladino | fé Treinado com voto feito num santuário e Treinado numa mão · vencer uma luta de dureza 4 contra maldito, morto ou espírito sem quebrar o voto | H **Golpe de Voto** · P **Chama de Voto** (uma aura por vez, a 3 casas: do escudo +1·+1·+2·+2·+2·+3 na Defesa; da lâmina +5%·+5%·+7%·+8%·+9%·+10% de dano, TÉCNICA; do firme +2·+2·+3·+3·+4·+4 na coragem) · H **A Jura** | o voto | VOTO: o do santuário (14.2) e um de armas, escolhido ao aceitar: o ESCUDO (não deixa cair quem está sob a sua guarda sem ter guardado), a LÂMINA LIMPA (não golpeia quem se rendeu ou está no chão desarmado) ou a ESTRADA (não recusa escolta pedida por quem não pode pagar) | +7,3 · +17,9 (m, a chama do escudo) · `fazer chama escudo\|lamina\|firme`; o voto na ficha |
| **SANHUDO** (as mãos de arma) — o berserker | Mestre numa mão de arma, ou Treinado em duas · vencer uma luta abaixo de um quarto do PV | H **Sanha** · P **Pele de Brasa** (na Sanha com 3 pontos ou mais: I·Ap firme · Ad e a primeira ferida grave da luta vira leve · do Perito, também a segunda) · P **Sono de Pedra** (depois de uma luta com a Sanha, a noite tira o cansaço dela e soma um dia de repouso) | −2 na fala com quem o viu na Sanha | VOTO: não recua de luta começada (a ordem de recuar ou de render-se, dada por ele, quebra o voto, salvo se todos os seus já caíram) | +6,2 · +16,3 (m); com a Teima que a prova ensina (a lição do D3), +7,0 · +20,3 · a recusa da ordem `recuar` diz o preço |
| **SANGRADOR DE CAMPO** (cura e fio) | cura e fio Treinado · salvar quem já rolava a morte no chão | H **Sopro de Volta** (a forte, no grupo) · H **Corte Fundo** · H **Mão que Estanca** | −2 na fala com quem ele não tratou (o povo o teme) | FARDO: no ermo, o encontro com bicho de matilha vem com um a mais (o cheiro de sangue) | duelo +3,2 · +7,1 (m); a força dele é o grupo (d) |
| **ESPREITADOR** (caça e tiro) | caça e tiro Treinado · caçar sozinho um bicho de grau C ou maior | P **Presa Jurada** (jura uma presa: um bicho, uma espécie ou uma pessoa com nome; +5%·+5%·+7%·+8%·+10%·+15% de dano contra ela, TÉCNICA, e +2 para segui-la; troca só quando ela morre ou passa uma estação) · H **Mira Firme** · H **Faro de Trilha** | −2 contra gente que não é a presa | FARDO: a presa jurada que escapa volta a caçá-lo; no ermo dela, a primeira rodada é dela | (d) · `jura PRESA` |
| **MEDIANEIRO** (comércio e manha) | comércio e manha Treinado · ganhar um pedido grande das duas partes de uma briga no mesmo dia | H **O Fio da Conversa** · H **A Palavra Firme** · P **A Brecha** (uma vez por pedido da caixa, troca o padrão por outra opção sem o custo; do Perito, também na missão) | quem perde a mediação lembra −3 | VOTO: não quebra acordo que mediou | (c: a fala do D3) · a opção nova na pergunta da caixa |
| **LÂMINA DE CENTELHA** (arcano e fio) | arcano e fio Treinado · vencer uma luta de dureza 4 lançando e golpeando na mesma rodada | P **Golpe de Rito** (a liga mão e tradição de 2.12, na forma do arcano: depois de ver o acerto, 2 de Mana, o alvo fica exposto até o fim da rodada) · H **Riposta** · P **Passo do Raio** (1 de Mana: anda 4 casas sem golpe livre, uma vez por rodada) | de placa, nenhum feitiço | FARDO: a luta em que lança e golpeia dá +1 de cansaço | (c: perto de +9 · +18) |
| **BIGORNA-VIVA** (secreta; qualquer mão) | FEITO TORTO: apanhar 20 golpes numa luta sem golpear, e viver | P **As Brasas** (cada golpe recebido sem revidar dá 1 brasa, até 3·3·4·4·5·5; o golpe seguinte solta todas: +10% de dano por brasa, TÉCNICA) · H **Guarda de Bigorna** · H **Teima** | −2 no acerto enquanto junta | FARDO: soltar 5 brasas dá +1 de cansaço na manhã seguinte | (d) |
| **OSSEIRO** (secreta; forja ou couro) | FEITO TORTO: forjar com a matéria de três bichos de espécies diferentes que ele mesmo matou | P **A Parentela** (2 peças da mesma fera: +2 na resistência a uma carga e na coragem; 4 peças: o pavor daquela espécie não pega) · H **Ler a Peça** · ps **Olho de Pele** | — | FARDO: aquela espécie o caça (no ermo dela, o encontro vem a ele) | (d) |
| **INSONE DA FORJA** (secreta; forja) | FEITO TORTO: três dias sem dormir na forja, e uma obra Rara no fim | P **Vigília da Brasa** (trabalha de noite sem a pena do sono na bancada) · H **O Malho Quente** · H **A Paciência** | a cama cura pela metade | FARDO: os olhos fundos: −1 na fala com quem o vê de dia | (d) |

#### Épicas (ficha curta; a nova entra no Adepto; teto Grão-Mestre)

| Classe (mães) | Chaves: número · feito do mundo · segredo | As quatro assinaturas (a forte primeiro) | Fraqueza e preço | Medido |
| --- | --- | --- | --- | --- |
| **SANGRADEIRA** (pacto e fio) — a bruxa de sangue | pacto Mestre e fio Treinado · pagar uma dívida inteira com o próprio sangue · uma sangradeira viva ensina, ou o escrito | H **Rito de Veia** · P **Modo Rubro** (o feitiço custa vida a 80% e sobe um grau de efeito; enquanto aceso, a cura recebida vale um décimo) · P **As Gotas** (guarda até 5, do sangue de quem caiu sangrando perto; cada uma paga um rito sem PV) · H **Corte Fundo** | sem cura de magia na cena do rito; a MANCHA que o povo vê (−2 na fala com quem viu) | +14,0 · +25,2 (m) |
| **MESTRE DE MOLDE** (forja e encanto) | forja Mestre e encanto Treinado · uma peça Épica com o seu sinete em uso por outra pessoa · o caderno de um mestre, ou a lição de quem tem forja de Mestre e o estima | P **O Molde** (ao abrir a obra, diz um efeito; se a peça sai na categoria da obra ou acima, com efeito da faixa, ganha o dito, dentro do teto; um molde por obra: não soma com o molde da ferramenta Lendária) · H **Têmpera Certa** · H **O Risco do Talho** · P **Sinete de Mestre** (a peça com o sinete vale 25% a mais na loja, dentro do teto; a encomenda de fora vem a ele) | o rival que forja copia, por estação, um efeito de uma peça dele | feitio +0,44 · +0,63 (m) |
| **ALFERES** (duas mãos de arma) | Mestre numa mão e Treinado noutra · comandar e vencer com metade do seu lado no chão · um alferes velho passa o pendão | H **Brado de Guerra** (no Alferes, até o Mestre) · H **Guarda de Bigorna** · P **O Pendão** (aliados a 3 casas: +2 na coragem; +4 do Mestre) · P **Formar** (ordem nova: o flanco não tira Defesa dos seus) | se o pendão cai, todos os seus testam a coragem | 3 contra 3: +13,4 · +26,2 (m); no duelo, +8,2 · +19,8 |
| **CHAMADOR DO ERMO** (verde e caça) | verde Mestre e caça Treinado · tirar uma frente do ermo do laço · o druida do lugar, de opinião 3 ou mais | P **Chamar a Fera** (até 2 bichos do ermo do laço, de categoria até a do foco) · P **O Laço Firme** (a fera do laço não o ataca) · H **Faro de Trilha** · H **A Picada** | o ermo caçado o enfraquece (14.2) | (d) |
| **ARMADOR DE HOSTE** (forja e uma mão de arma) | forja Mestre e Treinado numa mão · uma frente de ameaça barrada com ele na luta · o caderno da oficina de três mãos | P **A Oficina de Três Mãos** (com carpinteiro e rebitador, a tropa começa cada dia de batalha com as armas inteiras; por noite, uma peça Comum por grau) · H **Varrida** · H **Mão de Reparo** · P **Fio Assentado** | o inimigo manda matar o ferreiro (a frente o põe como alvo) | (d) |
| **CINZA-DE-VOTO** (secreta) | quebrar o voto do Fiel do Santuário | P **Golpe de Cinza** (o Golpe de Voto vira susto: o alvo testa a coragem contra 18 + o grau) · P **Chama Morta** (assusta todos a 3 casas, os seus também) · H **Teima** · H **Ameaça Surda** | sem a Mana da fé, para sempre | (d) |
| **ECO DE FERIDA** (secreta) | sobreviver a três técnicas diferentes que o derrubaram | P **Eco** (a forma forte do Eco de Golpe do D3: copia a técnica que o feriu com 20·20·25·30·40·50%; guarda 3, um degrau abaixo) · H **Olho de Luta** · H **Teima** · H **Colher o Jeito** | a técnica copiada custa o dobro | (d) |
| **SOLDADOR DA ENCRUZILHADA** (secreta; forja) | um pacto feito em cena numa encruzilhada, sendo ferreiro | P **Solda de Pacto** (junta matérias que não se juntam: +1 efeito fora do teto, uma vez por obra) · P **Grilhão Soldado** (prende a um objeto até vencer Força contra 28) · H **O Malho Quente** · H **Ler a Peça** | a entidade vem cobrar (o preço no SÓ O MESTRE) | (d) |

#### Únicas, Lendárias, Mítica e Primordial (ficha curta)

| Classe | Chaves | As assinaturas | Fraqueza e preço | Medido |
| --- | --- | --- | --- | --- |
| **REI DOS MALHOS** (Única; forja) | forja Mestre · o primeiro do ROL DOS MALHOS por uma estação (2.12) | P **A Encomenda do Rei** (o rei e as guildas mandam a obra grande a ele: a caixa) · P **A Bigorna Real** (na obra de núcleo, +1 de prumo e o QUASE da ferramenta Única, sem ela) · H **Ler a Peça** · H **Brio de Oficina** | o segundo do rol sabe, e o rei quer exclusividade | (d) |
| **CAÇADOR DO ÚNICO** (Única) | sobreviver a um ser único da história e ficar com uma parte dele | P **A Marca** (naquela parte do corpo não se veste armadura; +2 para seguir e entender o ser e a cria) · P **Carcaça Única** (a matéria do ser vira peça Única por definição) · H **Faro de Trilha** · H **Pé de Lebre** | o ser, ou a cria, vem atrás | (d) |
| **GRAVADOR DO NOME** (Única; encanto e forja) | encanto e forja Mestre · o escrito da MARCA-MÃE (o gancho do D2, para depois) | P **A Marca-Mãe** (o único vivo que a grava) · P **O Nome que Fica** (a peça marcada não se apaga por magia abaixo do grau 4) · H **O Traço Fiel** · H **Ler a Peça** | cada Marca-Mãe custa um ano de vida | (d) |
| **A LÂMINA-MOR** (Única; mão de arma) | Mestre numa mão · o primeiro do ranking (24.4) por uma estação | P **O Nome Temido** (quem começa a luta contra ele testa a coragem contra 22) · P **Desafio** (chama a duelo diante de testemunhas: recusar custa 5 de fama a quem foi chamado) · H **Riposta** · H **Teima** | todo novato quer o lugar: o desafio chega à caixa | (d) |
| **LEGATÁRIO DA BIGORNA** (Lendária; forja e peso; um por mestre ferreiro morto da crônica) | forja Lendário e peso Treinado · o legado do mestre (a peça, o caderno ou a oficina) · a CADEIA DO LEGATÁRIO (2.11) | H **Roda do Malho** (teto apelão; entra pela cadeia) · P **O Golpe do Mestre** (o fecho próprio da Roda, pelo tema da peça do mestre: "do Silêncio" ata, "do Lobo" sangra, "da Serra" expõe, "das Cinzas" queima, D1 2.12) · P **A Firmeza do Mestre** (+4 na resistência a toda carga e na coragem; nunca imune) · H **Ler a Peça** (uma categoria acima) · H **Mão de Reparo** · ps +10% de dano com arma da própria mão | o preço de entrada: a mão de arma volta um grau (e volta em metade dos blocos) | +20,4 · +28,0 (m); contra o conjunto Épico sem classe, vence 16,3% |
| **FIADOR DE JURAS** (Lendária; fé e arma) | Fiel do Santuário Pleno, fé Lendário, um voto mantido por um ano · o legado de uma lenda morta que fechou a fenda dos mortos ou curou a peste | H **Golpe de Voto** · P **Chama do Reino** (a Chama de Voto pega o grupo todo, a 5 casas) · P **A Jura que Prende** (quem jura diante dele não mente naquele dia) · H **Guarda de Bigorna** · H **A Jura** · ps +10% de dano | se quebra um voto, vira Cinza-de-Voto na hora, e a chama vira medo dos seus | +15,1 · +24,0 (m) |
| **O LEGADO DE [uma lenda]** (Lendária gerada) | uma por lenda morta da crônica: 2.12 | o molde pelo feito da lenda | o preço de entrada | (o banco mede cada molde) |
| **VOLTADO DA COVA** (Lendária, secreta) | cair e rolar a morte no chão em três lutas, ficar estável nas três sem amparo, e viver | P **A Morte Solta** (uma vez por luta, ao cair, rola a morte com +4; estável, levanta no fim da rodada com um quarto do PV) · P **O Medo Para** (o medo nele para no abalado) · P **Os Mortos Falam** (os mortos de Belogar o reconhecem e vêm falar) · H **Teima** · H **A Vigília** | a cura de magia nele vale a metade | (d) |
| **FERREIRO DO FRIO** (Mítica; forja) | um núcleo Mítico e um rito numa noite do latido | P **Forja Fria** (a peça fria fere espírito e fada como prata e recusa encanto inimigo) · P **Uma Vez na Vida** (uma vez, a obra nasce com o teto de efeitos da categoria que saiu, todos cheios, e o núcleo não se perde; a categoria e o teto não mudam) · H **O Malho Quente** · H **Ler a Peça** · H **Têmpera Certa** | o fogo não o aquece (o frio vira pena do corpo) | por evento |
| **HERDEIRO DO PRIMEIRO FOLE** (Primordial) | só por evento do Mestre: um núcleo Primordial, a mão Lendária de forja e o lugar onde a crônica diz que o primeiro fogo dorme | onde acende o fogo, a obra tem o quase e o lastro sem ferramenta e +3 de prumo (soma até 5; o total não muda); uma vez por estação, a peça nasce com uma Marca-Mãe sem gravador; nenhuma peça dele dorme na sintonia de quem ele escolhe (PESQUISA 3.6) | o fogo o reconhece; a coroa e a igreja querem o fogo de volta | por evento |

### 2.11 O caminho de Ferord (forja e encanto, da Comum à Lendária)
Hoje: nível 5, forja Treinado (154 blocos de bancada), martelo Iniciante, encanto Leigo. Os blocos de cada mão são os da tabela, vezes o talento (o que a MESA já mostra).

| Raridade | Classe | O que pede | Onde ele está | O que dá na forja |
| --- | --- | --- | --- | --- |
| Comum | **MALHADOR** | forja Iniciante · 50 blocos de bancada | as duas chaves já fecham: a oferta chega no primeiro turno com a regra | o Malho Quente: +0,12 de feitio na entrada, +0,24 no Perito (m) |
| Incomum | **TEMPERADOR** | forja Treinado · a obra-mestra (Incomum ou melhor, com efeito) mostrada a quem tem forja de Mestre (o mestre ferreiro da capital tem) · o Malhador Firmado, se aceitou o Malhador | a tenaz Incomum que ele junta serve, se nascer Incomum ou Rara com efeito: perto de 1 em 3 por obra (D2: 27,5% Incomum com efeito e 4,5% Rara) | +1 de prumo na matéria Incomum; a linha vai a +0,48 no topo (m) |
| ao lado | **RISCADOR · RUNEIRO** | encanto Iniciante · Treinado (50 e 150 blocos de encanto) | encanto Leigo | o Traço Fiel; a peça que solta o feitiço duas vezes |
| Rara | **MARCADOR DE RUNAS** | forja e encanto Treinado · a prova: a peça que forjou, gravada na primeira tentativa | falta o encanto Treinado. A prova, com Afinidade 70 e mesa de runas 1: 48% numa Incomum, 26% numa Rara (c); ele escolhe a hora | a Runa na Brasa: a obra encantada poupa os blocos do encanto e a essência até o Raro |
| Épica | **MESTRE DE MOLDE** | forja Mestre (375 blocos e um feito) e encanto Treinado · uma Épica com o sinete dele nas mãos de outro · o caderno ou um mestre que o estime | — | o Molde e a Têmpera: +0,44 de feitio na entrada, +0,63 no topo (m) |
| Única | **REI DOS MALHOS** ou **GRAVADOR DO NOME** | o primeiro do rol por uma estação · ou o escrito da Marca-Mãe | — | a encomenda do rei; ou a Marca-Mãe |
| Lendária | **LEGATÁRIO DA BIGORNA DE [o mestre]** | forja Lendário (1.000 blocos e um feito) e peso Treinado · o legado do mestre · as quatro obras do mestre | a primeira obra Lendária fecha perto do dia 260 a 356, pelo talento (10.8) | a Roda, o golpe do mestre, a ferramenta do mestre (só do legatário) |

- **Qual mestre.** O Legatário guarda o legado de um mestre ferreiro morto da crônica de Belogar. No mundo de Ferord, os candidatos são os que a crônica já nomeia (o
  PROJETO 2.3 cita cinco que forjaram martelos de nome). Qual deles chama, onde está o legado e o prazo da cadeia, o Mestre lê na crônica (SÓ O MESTRE).
- **A CADEIA DO LEGATÁRIO: AS QUATRO OBRAS DO MESTRE** (o contrato, 8.6, manda):
  - **Aceitar o legado:** quem tem a forja Lendária e toca o legado recebe o chamado (a oferta). Aceitar dá na hora a Roda do Malho no Iniciante (origem
    legado) e abre um prazo: 2d20 dias, rolagem oculta.
  - **As quatro obras:** reforjar de memória quatro peças do mestre, cada uma num lugar da crônica de Belogar onde ela fez história (quais peças e onde, o Mestre
    lê na crônica). Cada obra reforjada sobe a Roda um grau (até o Perito; a mão que segura o grau, D3 2.2), e a peça sai Rara, sem os efeitos de nome. Nenhuma obra
    "devolve um golpe": o que se aprende é o ofício do mestre.
  - **O prazo vencido** põe +4 na dureza das obras que faltam. **O fim:** a classe Lendária e a ferramenta do mestre (Lendária, `so_legatario`). A Roda chega no
    grau que as obras deram: com as quatro, no Perito (+16,9 sozinha, no D3).

### 2.12 Milhões de classes: o gerador

| Fonte | Quantas por mundo | Como nasce | Raridade |
| --- | --- | --- | --- |
| o núcleo feito à mão | 46 | este desenho | todas |
| o molde de Comum | 7 | a primeira habilidade da lista da mãe e duas passivas da tabela do caminho | Comum |
| as CRUZADAS de duas mães | 130 pares (sem duas tradições: uma tradição por pessoa, 14.2); 8 feitas à mão, 122 geradas | uma assinatura de cada mãe (a semente escolhe na lista dela) e a LIGA do tipo do par; a fraqueza da mãe mais forte; o fardo da tabela | Rara |
| as cruzadas de três mães | 598 trios (no máximo uma tradição) | uma assinatura de cada mãe e a liga do primeiro par | Épica |
| as LENDÁRIAS da crônica | 9 a 18 (média 14,2 em 40 sementes; c) | uma por lenda morta e por mestre de peça Única ou Lendária (o `historia.py`): o molde pelo feito, o tema da peça e a família dela | Lendária |
| as ÚNICAS das medidas | 8 medidas e 3 feitos únicos | o primeiro da medida por uma estação | Única |
| as SECRETAS | 12 feitos tortos × 17 caminhos = 204 | o feito torto; uma assinatura vem da lista do caminho de quem fez | Rara a Lendária |
| **total** | **perto de 1.000 (993 na conta)** | | |

- **O espaço das sementes:** a semente escolhe o nome (3 agentes e 3 raízes por caminho), a assinatura de cada mãe e a variante da liga. Dá **50.400 Raras cruzadas e
  3.056.292 Épicas** diferentes (c), e as Lendárias, 2.640 moldes vezes o nome da lenda: **mais de 3 milhões de classes**, cada uma montada de peças medidas.
- **A qualidade:** nenhuma classe gerada traz regra nova. As peças são as habilidades do D3 (medidas grau a grau), as dez ligas, os dez moldes de Lendária e as
  tabelas de fraqueza e fardo, todos escritos à mão e medidos. O banco mede cada liga e cada molde na faixa da raridade (meta 9). E o jogador só vê o que lhe é
  oferecido e a pista: o catálogo nunca vai inteiro à mesa.
- **As listas das mães** (a semente escolhe uma): fio Riposta, Corte Fundo, Varrida · haste Rasteira, Manter à Distância · peso Tranco de Luta, Golpe de Quebra,
  Varrida · tiro Mira Firme, Pé de Lebre · forja O Malho Quente, A Paciência, Ler a Peça, Mão de Reparo, Brio de Oficina · couro Ajuste Fino, Mão de Reparo ·
  caça Faro de Trilha, Pé de Lebre, A Picada · coleta A Picada, Marcha Longa · comércio Língua de Feira, Olho de Avaliador, O Fio da Conversa · cura Mão que Estanca,
  Mão que Esquenta, Trato de Campo, Ferro em Brasa · alquimia A Medida Certa, Olho de Avaliador · encanto O Traço Fiel, Ler a Peça · manha Passo Manso, Romper a Linha
  · as tradições, um feitiço de grau 1 da tradição, sabido sem estudo e 1 de Mana mais barato.

**As LIGAS** (a assinatura própria de cada cruzada, pelo tipo do par; a semente escolhe a variante):

| Par (quantos) | Variante A | Variante B |
| --- | --- | --- |
| mão e mão (6) | **MÃO DUPLA:** a mão mais baixa das duas luta como a mais alta (acerto e Defesa), com a arma dela | **TROCA LIGEIRA:** trocar entre as duas armas não gasta ação, e o primeiro golpe depois da troca tem +2 |
| mão e ofício (36) | **O OFÍCIO NA LUTA,** pelo ofício: forja +5% de dano com arma da própria mão · couro +1 na Defesa com couro da própria mão · caça +5% contra bicho · coleta uma ação a mais na 1ª rodada no ermo · comércio o rendido paga resgate (1d6 × 5 de prata) · cura a atadura sem ação, uma vez por luta · alquimia o óleo de lâmina dura a luta inteira · encanto o encanto da arma solta duas vezes · manha o golpe pelas costas com um dado a mais | **A LUTA NO OFÍCIO:** no dia de uma luta vencida, o ofício rende um passo a mais (na bancada +1 de prumo; na coleta, 1 a mais; na loja, +5 pontos; no tratamento, +½ dia) |
| mão e tradição (16) | **GOLPE DE RITO:** depois de ver o acerto, 2 de Mana: fé +20% de dano (o dobro contra maldito) · arcano exposto até o fim da rodada · verde preso por 1 turno (calejo de pernas) · pacto um filete de 1/4 por 3 rodadas, pago com 2% do PV | **ARMA DE FOCO:** a arma vale foco um degrau abaixo, e lançar com ela na mão não pede a mão livre |
| ofício e ofício (36) | **A OBRA CRUZADA:** o que um ofício produz, usado no outro, rende um passo a mais (na bancada +1 de prumo; na botica +1 poção; na loja +5 pontos; no tratamento +½ dia) | **O ATALHO:** a obra de um dos dois leva um bloco a menos (mínimo 1) com a mão de Treinado no outro |
| ofício e tradição (36) | **O RITO DO OFÍCIO:** fé a obra nasce benta (conta inteira contra o que não tem corpo por 7 dias) · arcano a obra guarda um truque · verde a matéria do ermo do laço dá +1 de prumo · pacto o sangue na têmpera (5% do PV por +1 de prumo, até 2) | **A MANA NA MÃO:** 1 de Mana por bloco tira 1 de cansaço do bloco pesado |

**As LENDÁRIAS da crônica.** Cada lenda morta do `historia.py` deixa uma Lendária: **O LEGADO DE [nome], [o do feito]** ("o Legado de Aldo, o da Ponte"). O mestre
ferreiro deixa o **Legatário da Bigorna** dele (a linhagem da Roda pela família da peça: peso aturde, fio sangra, haste derruba, tiro prende). O molde pelo feito:

| O feito da lenda | O golpe perdido (teto apelão) | Resiste (+4) |
| --- | --- | --- |
| matou o [fera] | **O Golpe no Coração:** contra bicho ou criatura grande, a proteção conta pela metade e o crítico abre no 18 | ânimo (o pavor) |
| segurou sozinho a ponte | **Ninguém Passa:** na ordem segurar, quem passa leva golpe livre, e a Defesa sobe +2 por inimigo colado (até +6) | pernas |
| desceu à ruína e voltou | **O Fio da Volta:** na masmorra, a saída se abre no mapa, e o primeiro golpe de cada luta lá dentro é de surpresa | ânimo |
| fechou a fenda dos mortos | **O Selo da Fenda:** contra morto e espírito, carga de cabeça 6 por golpe, e o golpe conta inteiro | mana |
| levou o povo pela serra | **A Marcha do Inverno:** a comitiva anda 3 dias sem cansaço nem fome; na luta, os seus não fraquejam no primeiro susto | ânimo |
| venceu o torneio três anos | **A Terceira Vez:** no um contra um, cada rodada soma +1 no acerto (até +4), e a Riposta não gasta reação | cabeça |
| quebrou o cerco | **Romper o Cerco:** atravessa a linha inimiga (o Romper a Linha no topo), e os seus que o seguem também | pernas |
| expulsou os orcs até o último | **A Caça ao Último:** quem foge dele leva o golpe livre com +4 e o dano inteiro; o povo que ele venceu testa a coragem contra 26 ao vê-lo | ânimo |
| achou o veio de ferro | **O Olho do Veio:** a matéria que ele colhe dá +2 de prumo na obra | coragem |
| curou a peste | **A Mão da Peste:** trata 5 por dia e a doença não o pega; na luta, a atadura fecha todos os filetes dos seus colados | veneno |

As outras quatro assinaturas: P **A Peça e a Mão** (com a peça da lenda na mão, o poder de lenda dela não dobra o lugar na sintonia e vale sempre; sem ela, o dito vale
uma vez por dia; D1 2.11 e 2.12), a resistência +4, uma H do campo do feito (Faro de Trilha, A Vigília, Passo Manso, O Benzimento, Marcha Longa, Riposta, Romper a
Linha, Brado de Guerra, Ler a Peça, Mão que Esquenta) e ps +10% de dano. **Chaves:** Lendário na mãe (a família da peça; o foco, a tradição); o legado (a peça, ou o
túmulo onde a lenda morreu); a cadeia de quatro passos (o lugar do feito, o lugar da morte, a peça, e a prova do feito: um bicho de grau B para o mata-fera, uma luta de
um contra três para a ponte...).

**As ÚNICAS das medidas** (o script conta toda semana; vale a estação inteira; a oferta vai ao primeiro, se ele tem a mão de Mestre no caminho):
o **rol dos malhos** (a soma de 3 elevado à categoria das peças Raras ou melhores com o sinete da pessoa, em uso por alguém vivo) → REI DOS MALHOS · o **ranking**
(24.4) → A LÂMINA-MOR · a **caça** (bichos de grau C ou maior mortos) → O CAÇADOR-MOR · a **bolsa** (a prata ganha em venda) → O SENHOR DA BALANÇA · a **cura**
(tratados) → A MÃO DO REINO · a **masmorra** (salas limpas) → O DESBRAVADOR · o **medo** (frentes barradas com a pessoa no evento) → O ESCUDO DO REINO · o **encanto**
(gravações que pegaram) → O RUNEIRO-MOR. E os três feitos únicos: o CAÇADOR DO ÚNICO, o GRAVADOR DO NOME e O MATA-SERPE (o primeiro a matar um dragão no mundo).
As que não estão em 2.10 seguem o molde da medida: duas habilidades da lista do caminho e duas próprias da tabela da medida.

**As SECRETAS por feito torto** (o script vê o feito; a oferta diz só "algo mudou em você"; uma assinatura vem da lista do caminho de quem fez: o mesmo feito faz uma
classe diferente num ferreiro e num sacerdote):

| Feito torto | Secreta | Raridade |
| --- | --- | --- |
| apanhar 20 golpes numa luta sem golpear, e viver | Bigorna-Viva | Rara |
| forjar com três feras de espécies diferentes que ele matou | Osseiro | Rara |
| três dias sem dormir na forja, e uma Rara no fim | Insone da Forja | Rara |
| sete dias seguidos numa masmorra sem sair | O QUE MORA EMBAIXO | Rara |
| usar num feito a peça de um morto, sem a família dele saber | O DEVEDOR DE MORTO | Rara |
| quebrar o voto do Fiel do Santuário | Cinza-de-Voto | Épica |
| sobreviver a três técnicas diferentes que o derrubaram | Eco de Ferida | Épica |
| um pacto feito em cena numa encruzilhada, sendo ferreiro | Soldador da Encruzilhada | Épica |
| matar quem é o seu mestre (o laço) | O SEM-MESTRE | Épica |
| vencer sozinho contra três ou mais, com todos os seus caídos | O ÚLTIMO DE PÉ | Épica |
| cair e rolar a morte em três lutas, estável sem amparo | Voltado da Cova | Lendária |
| comer o coração do dragão que matou | SANGUE DE SERPE | Lendária |

**Os nomes** (`nomes.py`, uma função nova, `Nomes.classe`): a cruzada leva o agente de uma mãe e a raiz da outra ("o Talhador da Brasa", "o Seteiro do Voto"); a
Épica de três, um título e duas raízes ("o Arauto da Runa e do Faro"); a Lendária, "o Legado de [nome], o [do feito]"; a Única, o nome da medida; a secreta, o nome
fixo. A tabela `RAIZES` traz 3 agentes e 3 raízes por caminho, escritos à mão (forja: Foleiro, Brasador, Bigorneiro · da Bigorna, do Fole, da Brasa; encanto: Traçador,
Sinaleiro, Entalhador · da Runa, do Traço, do Sinal; caça: Batedor, Rastreiro, Farejador · do Faro, da Trilha, do Rastro). O filtro é o de hoje (`famoso`, `feio`),
mais: nenhum nome repetido no mundo, e nenhum que comece com a palavra de uma classe do núcleo.

### 2.13 A gente do mundo com classe
**Quem tem a chave do número** (os três mundos de teste: 596 pessoas vivas; m): nenhuma 21,6% (criança, aprendiz, lavrador, ancião) · Comum 38,3% · Incomum 23,3% ·
Rara 15,8% (o caçador, arco e caça Treinado; o capitão, espada e lança) · Épica 1,0% (seis veteranos) · Única e Lendária 0.

**A regra no `gera.py`** (pela semente; a gente não recebe oferta: nasce com a classe que a mão e a vida dela explicam):
- **Comum** a quem tem a mão de Iniciante no caminho do papel (o trabalho do papel é o trabalho visto).
- **Incomum** à metade dos que têm a chave dela (passou no exame).
- **Rara** a 1 em 3 dos que têm a chave dela (passou na prova): a feita à mão do par, se há; senão, a cruzada.
- **Épica** a 1 em 2 dos que têm a chave (os veteranos). **Única:** o primeiro de cada medida no Dia 1, se tem a mão. **Lendária:** nenhuma; todas dormem no legado.
- **Esperado por mundo** (c, a regra nos mundos de teste): sem classe 21,6% · Comum 55,3% · Incomum 17,1% · Rara 5,4% (umas 11 pessoas) · Épica 0,5% (uma) · de 0
  a 3 Únicas · nenhuma Lendária.
- **Os rivais:** novato Comum · oficial Comum ou Incomum · veterano Rara (um em quatro, Épica) · Lenda Épica, e o primeiro do ranking com A LÂMINA-MOR.
  Para isso, o `gera.py` dá ao veterano e à Lenda uma segunda mão de Treinado pela semente (hoje eles têm uma só: nos mundos de teste, nenhuma Lenda tem a chave da Épica).
- **Os ofícios do mundo:** o mestre ferreiro da capital (forja 6) nasce Temperador ou Mestre de Molde (meio a meio): o rival que forja (D1 2.12) escolhe os efeitos
  com os números da classe dele.

### 2.14 O que muda no mundo: a encomenda, a fama, a cobiça
- **A ENCOMENDA.** Quem precisa de uma obra procura a classe (o querer da semana, 22.2): o capitão manda a lança ao Temperador antes do Malhador. À caixa do personagem
  (22.4) chegam pedidos pela classe dele: Comum, o conserto do vizinho; Incomum, a encomenda da guarda; Rara, a peça marcada de um nobre; Épica, a obra de outro lugar;
  Única e Lendária, a do rei. O prazo e a paga sobem com a raridade.
- **A FAMA.** Ganhar a classe soma fama (o ranking, 24.4): Rara +5, Épica +10, Única +20, Lendária +30; ficar Plena soma o mesmo de novo. A Rara e a Épica viram
  notícia no lugar (22.3); a Única e a Lendária vão à JANELA DO MUNDO.
- **A COBIÇA.** A classe Épica de ofício sobe um passo da cobiça da coroa (o gancho da PESQUISA 3.8.2, quando entrar); a Única, um; a Lendária, dois. A Única de luta
  tem o segundo da medida atrás dela; da Lendária, quem quer o legado sabe que ele volta na morte do dono (o Mestre pode abrir uma frente de ambição).
- **A CORRIDA.** Os rivais disputam as mesmas ofertas (a medida da Única, o legado da Lendária): o banco do ano mede (meta 13).

### 2.15 A medida (o resumo medido)

| Raridade | Faixa: entrada · topo | Medido (duelo de iguais, salvo o dito) |
| --- | --- | --- |
| Comum | 1 a 5 · até 10 | Guarda-Linha +1,2 · +6,9 · Pelejador +3,9 · +7,4 · Malhador, feitio +0,12 · +0,24 |
| Incomum | 3 a 7 · até 12 | Anteparo +3,1 · +9,6 · Temperador, feitio +0,12 · +0,24 |
| Rara | 5 a 10 · até 20 | Sanhudo +6,2 · +16,3 · Malheiro +6,4 · +16,5 · Fiel do Santuário +7,3 · +17,9 · Sangrador (duelo; o campo dele é o grupo) +3,2 · +7,1 · Marcador, feitio +0,12 e o tempo |
| Épica | 10 a 20 · até 26 | Sangradeira +14,0 · +25,2 · Alferes (3 contra 3) +13,4 · +26,2 · Mestre de Molde, feitio +0,44 · +0,63 |
| Única | 10 a 20 · até 30 | (d) |
| Lendária | 15 a 25 · até 40 | Legatário +20,4 · +28,0 · Fiador de Juras +15,1 · +24,0 |
| o item decide | o de cima vence 60% ou mais | o Legatário no topo, tudo Raro, contra o conjunto Épico sem classe: o Épico vence 83,7%; com o martelo Épico só, 78,3% |
| a segunda classe | até 40 | Legatário no topo e Malheiro de segunda: +34,9 (contra o conjunto Épico, 22,7%) · Malheiro no topo e Sanhudo de segunda: +20,5 |

- **O que saiu da medida** (m): três assinaturas de luta numa classe passam do topo (Malheiro com Tranco +25,5; Sanhudo com a Teima +20,3 a +22,0): por isso uma forte
  de duelo por classe. O Alferes com o Brado no Grão-Mestre, +35,5 no grupo: por isso o Brado dele para no Mestre. A linha do ferreiro no topo com o prumo 5, a têmpera
  3, o lastro e o molde dá +1,79 de feitio: é o teto que o D2 já desenhou para as ferramentas Lendárias (classe e ferramenta dividem os tetos do D2: o prumo até 5,
  um molde por obra, a têmpera e o lastro valem o maior), nunca acima dele.
- **Onde cai o pedido:** o paladino é o Fiel do Santuário (o golpe de voto e a chama); a bruxa de sangue é a Sangradeira (paga com vida, sobe um grau de efeito, a cura
  some); o berserker é o Sanhudo (a Sanha que cresce com o tempo e o sangue; não recua); a "dança da espada do ferreiro lendário" é a Roda do Legatário (+24,7 no topo,
  no D3); a classe secreta, a Lendária e as milhões, 2.12.

---

## 3. Os dados: o que muda na ficha, no item, no mundo e nos eventos

- **A pessoa** (`gente.json`):
  - `classe`: `{chave, desde: dia, via: "oferta"|"prova"|"segredo"|"medida"|"legado"|"torto"|"gera", degrau: 0|1|2, voto: {qual, desde}|null, apagada: {dia, ate,
    motivo}|null, linha: [as chaves anteriores da linha]}` · `classe2`: o mesmo, a segunda (ausente se não há) · `classes_fechadas`: `[CHAVE]` (a prova falhada; o voto
    sem penitência).
  - `marca.ofertas`: `{CHAVE: {dia, ate, recusas, prova: true|null}}` · `marca.cadeia`: `{classe, obras: [dias], faltam: [...]}` (o prazo fica no `mundo.oculto`).
  - As assinaturas moram nas `habilidades` do D3, com `origem: "classe:CHAVE"` e `classe: true` (não ocupam vaga).
- **O mundo** (`mundo.json`):
  - `mundo.classes`: `{CHAVE: {nome, raridade, tipo: "cruzada"|"tres"|"lendaria"|"unica"|"secreta"|"molde", maes: [...], partes: {a escolha da semente}, de: o nome da lenda
    ou do mestre, legado: IID ou lugar, medida, dono: PID|null, desde}}`. Só as geradas (função pura da semente e da crônica, uma vez, no `gera.py`); o núcleo mora
    em `tabelas_classes.py`.
  - `mundo.medidas`: `{MEDIDA: {valores: {PID: n}, lider, desde}}` · `mundo.oculto.cadeia_PID`: o prazo da cadeia.
- **O item:** `legado: {classe: CHAVE, de: nome}` (a peça, o caderno, a ferramenta do mestre) · o `escrito` ganha `classe: CHAVE` (o segredo da Épica) · a ferramenta do
  mestre ganha `so_legatario: PID`.
- **Os verbos do `estado.py`** (no molde de `feitico aprende` e do `voto`):
  - `['pessoa', id, 'classe', 'toma', {chave, via, voto}]`: só nos eventos "classe", "gera" e "mestre"; do personagem, só com a oferta aberta e o "aceito" dele.
  - `['pessoa', id, 'classe', 'degrau', n]` (só +1) · `['pessoa', id, 'classe', 'apaga', {dia, motivo}]` · `['pessoa', id, 'classe', 'acende', {}]` ·
    `['pessoa', id, 'classe', 'deixa', motivo]` · `['pessoa', id, 'classe', 'fecha', CHAVE]` · `['pessoa', id, 'classe2', 'toma'|'deixa', ...]`.
  - Os de hoje servem para o resto: `['pessoa', id, 'marca.ofertas', 'poe', ...]`, `['mundo', 'classes', CHAVE, 'dono', 'poe', PID|null]`, `['mundo', 'medidas', M, 'poe',
    ...]`, `['pessoa', id, 'fama', 'soma', n]`, `['item', id, 'historia', 'junta', ...]`.
  - **Tipos de evento novos:** "classe" (a oferta, o aceito, a recusa, a prova, o degrau, o apagar, o deixar) e "medida" (a conta da semana).
- **`estado.valida`:** a chave existe (no núcleo ou no `mundo.classes`); as três chaves fecham no dia (a mão; o feito nos eventos; o segredo); uma classe por vez, e a
  segunda só com as duas Rara ou maior e a primeira Plena; a Única e a Lendária com um dono só; a Lendária só com a cadeia inteira; o degrau só +1 e com as habilidades
  no grau; a classe apagada não dá assinatura; nada fechado volta a abrir.

---

## 4. Onde entra no motor

| Arquivo · função | O que muda | Novo? |
| --- | --- | --- |
| `tabelas_classes.py` | a ESCADA (grau de entrada, teto, contagens, faixas, dano fixo), o TRABALHO VISTO, as PROVAS, o NÚCLEO (as 46), o MOLDE DE COMUM, as LISTAS das mães, as LIGAS, os MOLDES DE LENDÁRIA, as MEDIDAS, os FEITOS TORTOS, os VOTOS, as FRAQUEZAS por caminho, as RAIZES dos nomes | novo |
| `classe.py` (do Motor 10; o da raiz é do Ferir) | `ver`, `mesa` (a linha), `reconhece(E, pid)` (as chaves → a oferta), `aceita`, `recusa`, `prova`, `degrau`, `apaga`/`acende`, `deixa`, `segunda`, `cadeia` (as obras e o prazo oculto), `medidas` (a conta da semana), `gera_mundo` (as cruzadas, as Lendárias da crônica, as Únicas, as secretas), `so_mestre` | novo |
| `habilidade.py` (o do D3) | a origem "classe": a assinatura entra no grau da raridade (2.2) e para no teto dela; as exceções por classe (o Brado do Alferes no Mestre); a linha guarda as antigas; fora da linha, viram comuns no Perito; as habilidades novas: O Traço Fiel, A Medida Certa, O Benzimento, e as próprias das classes | muda |
| `nomes.py` | `Nomes.classe(tipo, maes, semente)` e o filtro do núcleo | muda |
| `estado.py` | os verbos e a validação de 3 | muda |
| `gera.py` | a gente nasce com a classe (2.13); a segunda mão do veterano e da Lenda; o `mundo.classes` | muda |
| `ato.py` (`luta_fecha`, o remate da obra, `_ficha`) | o feito para a prova e o degrau (a dureza, a luta vencida abaixo de 1/4 do PV, os golpes levados sem revidar, a obra-mestra, a gravação na 1ª tentativa); chama o `classe.reconhece` no fim do ato | muda |
| `oficio.py` · `encanto.py` | as passivas e as próprias de ofício (o Fogo Certo, a Runa na Brasa, o Traço Fiel, o Molde da classe, o Sinete); a fraqueza do −2 fora da oficina (só desce) | muda |
| `luta.py` (pelos ganchos do `habilidade.py`) | a passiva de luta (coragem, resistência à carga, dano fixo no grupo TÉCNICA); a ordem `fazer chama`, `formar`, `jura`; o voto que a luta vê (recuar, golpear quem se rendeu) | muda |
| `turno.py` · `caixa.py` | a linha CLASSE na MESA; a OFERTA como pergunta e pedido; a encomenda pela classe; no SÓ O MESTRE, a classe dos outros, as secretas perto de abrir e o prazo da cadeia | muda |
| `noticias.py` · `rivais.py` · `conta.py` | a notícia da Rara e da Épica, a JANELA da Única e da Lendária; o rival aceita a oferta que sobe a conta dele; a classe entra como traço na conta rápida | muda |
| `provas_classes.py` · `provas_ano.py` | o banco de 5 | novo, muda |
| `REGRAS.md` (cap. 30, as classes) · `MUDANCAS.md` | | muda |

**O que muda no D3** (para o integrador casar): (1) a assinatura de classe entra no grau da raridade, não no Iniciante; (2) os tetos por raridade ficam os do D3
(Comum Perito, Incomum Mestre, Rara para cima Grão-Mestre), com a exceção do Brado no Alferes; (3) o catálogo ganha O Traço Fiel, A Medida Certa e O Benzimento; (4) as
classes sugeridas no catálogo do D3 batem com 2.10, salvo o Tranco de Luta, que sai do Malheiro (uma forte de duelo por classe) e fica no estalo e no mestre.

---

## 5. O banco: as metas

| # | O que se mede | Como | A faixa aceita |
| --- | --- | --- | --- |
| 1 | A LUTA DE SEMPRE | lutas sem classe, semente fixa, antes e depois | o registro igual, linha por linha |
| 2 | O DEGRAU NA RÉGUA | cada classe do núcleo, na entrada e no topo, no campo dela (duelo, 3 contra 3, feitio, fala), 8.000 lutas por linha | dentro da faixa da raridade (2.2), ±1,5; nenhuma acima de 40 |
| 3 | O ITEM DECIDE | a Lendária no topo, tudo Raro, contra o conjunto Épico sem classe | o Épico vence 60% ou mais |
| 4 | A VARIEDADE | as famílias de estado e os campos de cada classe; o dano fixo | as famílias no mínimo da raridade; dois campos da Rara para cima; o dano fixo no teto (0, 0, 3, 5, 5, 10%) |
| 5 | A SEGUNDA CLASSE | a pior dupla no topo, com o tributo | até 40 entre iguais; o item decide (meta 3) |
| 6 | A OFERTA E A PISTA | 1.000 personagens simulados; o mundo gerado | a oferta só nasce com as três chaves; nenhuma classe sem o "aceito"; a recusa volta no prazo; nunca duas ofertas da mesma classe; toda classe do núcleo com uma fonte de pista |
| 7 | A PROVA | provas declaradas e roladas pelo `teste.rola` | uma vez só; falhou, fecha para sempre; a chance mostrada bate com a exata |
| 8 | A ÚNICA E A LENDÁRIA | 20 sementes, um ano | um dono por vez; a Única passa na medida; a Lendária volta ao legado na morte; nunca dois donos |
| 9 | O GERADOR | 20 sementes | 130 cruzadas e 598 trios por mundo; as Lendárias = as lendas mais os mestres de peça Única ou Lendária; nenhum nome repetido, famoso ou feio; mesma semente, mesmas classes; cada liga e cada molde de Lendária na faixa da raridade |
| 10 | A GENTE | o mundo gerado, 20 sementes | sem classe 15 a 30% · Comum 45 a 65% · Incomum 12 a 22% · Rara 3 a 8% · Épica 0,2 a 1,5% · Única 0 a 3 · Lendária 0 |
| 11 | O VOTO | quebras simuladas | apaga na hora; a penitência no prazo acende um degrau abaixo; sem ela, perde e fecha; a mesa sempre diz |
| 12 | A FORJA | a chance da categoria com as classes de ofício ligadas, contra o `oficio.dist_valor` | a diferença 0 (medido: 0); cada classe na régua de feitio dela |
| 13 | O ANO | `provas_ano.py` com as classes | o mundo não explode: nenhum rival mata o dragão no primeiro mês; de 0 a 1 Lendária tomada por rival no ano |
| 14 | A MESA | a linha, a oferta, a pista, o SÓ O MESTRE | a linha mostra classe, degrau e o que falta; a oferta diz o que dá, o que custa e o que deixa; o SÓ O MESTRE guarda as secretas e o prazo |

---

## 6. O que fica para depois, os riscos e as perguntas

**Fica para depois:**
- as medidas que o motor ainda não conta (o rol dos malhos pede o sinete; o encanto e a cura pedem o registro por pessoa): a primeira versão traz o ranking e a caça;
- a Marca-Mãe (D2) e o Gravador do Nome; a cobiça da coroa como trilha; a reforja de memória da cadeia (a peça Rara do mestre) no detalhe;
- as tradições como mães de verdade (hoje dão um feitiço de grau 1): quando a magia for revista (PROJETO 2.4), cada tradição ganha a sua lista de técnicas;
- a medida no grupo do Sangrador, do Anteparo e do Chamador do Ermo (marcados com d).

**Os riscos:**
1. **O grau de entrada muda o que o D3 propôs.** Sem ele a raridade não se vê no dia em que chega (achado 1). Se o integrador mantiver o Iniciante, as faixas de entrada
   de 2.2 caem para "fraco" em todas, e a raridade só se vê no topo.
2. **A raridade no duelo é larga.** Classes de grupo e de ofício valem pouco no duelo (o Sangrador, +3,2 na entrada). A meta 2 mede cada uma no campo dela; a que sair abaixo da
   faixa no campo dela sobe na próxima rodada.
3. **Mil classes por mundo.** A mesa não pode afogar: só a oferta e a pista aparecem. O SÓ O MESTRE também precisa de filtro (as perto de abrir).
4. **Os rivais com classe** sobem o ranking mais depressa e podem chegar antes às Únicas. A meta 13 confere.
5. **O voto julgado pelo Mestre** é risco de discussão: os votos do núcleo são todos de coisa que o script vê.
6. **A prova da Rara que fecha para sempre** pode doer numa linha que o jogador ama (o Marcador, 48%). Por isso ele escolhe a hora e vê a chance antes (pergunta C3).

**As perguntas ao jogador** (o código responde: "C1a.C2a..."):
- **C1. Como a classe chega.** (a) O mundo oferece e você aceita ou recusa. (b) Chega sozinha quando as chaves fecham. (c) Você escolhe numa lista das que fecharam.
  **Recomendo (a):** a escolha é sua, e o mundo é que reconhece; a lista (c) mostra as chaves e mata o segredo.
- **C2. O grau de entrada.** (a) Pela raridade: Comum no Iniciante, Incomum e Rara no Aprendiz, Épica e Única no Adepto, Lendária pela cadeia. (b) Tudo no Iniciante,
  como o D3 propôs (a Épica nova entra valendo +2 a +3). **Recomendo (a):** a classe de cima tem de pesar no dia em que chega.
- **C3. A prova da Rara que falha.** (a) Aquela classe fecha para sempre, e você escolhe a hora da prova vendo a chance. (b) Fecha por um ano. (c) Não fecha.
  **Recomendo (a):** a classe rara é prêmio de história; há outras cruzadas das mesmas mães, e a linha segue (o Mestre de Molde não pede o Marcador).
- **C4. Quebrar o voto.** (a) A classe apaga, e 28 dias de penitência a acendem um degrau abaixo; sem ela, perde. (b) Perde na hora. (c) Só uma pena.
  **Recomendo (a):** consequência de verdade, com uma volta que custa.
- **C5. A segunda classe.** (a) Só da Rara para cima, com a primeira Plena, e o tributo (a segunda para no Mestre, as duas fraquezas e votos, a marca da cena a uma
  só). (b) Sem segunda classe. (c) Livre. **Recomendo (a):** duas identidades são uma conquista, não uma soma.
- **C6. O preço da Lendária.** (a) A mão de arma volta um grau (volta em metade dos blocos): o corpo desaprende para aprender a dança do mestre. (b) Sem preço além da
  cadeia. **Recomendo (a):** todo apelão leva um freio que se sente.
- **C7. Quantas classes.** (a) O núcleo (46) e as geradas (perto de mil por mundo; a mesa só mostra a oferta e a pista). (b) Só o núcleo. **Recomendo (a):** são as
  "milhões de classes" do pedido, feitas de peças medidas.
- **C8. Ferord agora.** (a) O mundo oferece o MALHADOR no primeiro turno com a regra (ele já tem as chaves). (b) Espera a obra-mestra e vem direto o Temperador.
  **Recomendo (a):** a primeira classe nasce em cena, com você vendo; o Malho Quente já ajuda a tenaz.
- **C9. A gente do mundo.** (a) Nasce com a classe pela mão e pela semente (os rivais e os ferreiros também). (b) Só o personagem tem classe. **Recomendo (a):** o mundo
  vivo tem os seus Temperadores e os seus Sanhudos, e o rival que forja forja com a classe dele.

---
*De onde vêm as contas (fora do repositório, no rascunho desta sessão; nada foi gravado no mundo):*
- `/tmp/claude-0/-home-user-ferir/4088f7d7-9a0c-5212-bbb2-a884104a0915/scratchpad/D5/hab.py` (a cópia do remendo do D3) e `classes_luta.py`, `classes_luta2.py`,
  `classes_luta3.py` (e as `_saida.txt`): os pacotes no duelo, o item decide e a segunda classe · `tres.py`: o 3 contra 3 do Alferes.
- `/tmp/claude-0/-home-user-ferir/4088f7d7-9a0c-5212-bbb2-a884104a0915/scratchpad/D5/forja_classes.py`: a linha do ferreiro na régua de feitio do D2 e a chance da categoria.
- `/tmp/claude-0/-home-user-ferir/4088f7d7-9a0c-5212-bbb2-a884104a0915/scratchpad/D5/gente_classes.py`: as chaves da gente nos mundos de teste · `contagem.py`: o
  gerador por mundo e o espaço das sementes · `cronica.py`: os mestres e as lendas da crônica.
