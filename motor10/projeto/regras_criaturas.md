> **JUNTADO AO `REGRAS.md`** (capítulos 15 e 16) na integração da etapa da magia, com os acertos dela (o mau-olhado de −4, os chefes acertados, a loja que não compra peça maldita, o segredo fora do RETOMAR). O que vale é o `REGRAS.md`; este rascunho fica como registro.

# RASCUNHO dos capítulos 15 e 16: as criaturas, os covis e a vila de teste com a magia

Rascunho da frente das criaturas (etapa da magia). O integrador junta no `REGRAS.md`. Os números moram no `tabelas_criaturas.py`; a regra, no `criaturas.py` (e no `bichos.py`
e no `caca.py`, que passaram a aceitar as criaturas); as provas, no `provas_criaturas.py` (o `provas_mundo.py` o chama).

---

## 15. AS CRIATURAS

### 15.1 Dois jeitos de ser criatura

**O povo** (o goblin, o orc, o ogro, o homem-lagarto, o gigante; e os mortos que empunham: o esqueleto e o cavaleiro da cova) é **gente**. Tem a ficha de gente, com arma,
armadura e escudo de verdade, e por cima o corpo do povo: o tamanho (mexe no PV, na Defesa, no alcance da mão e em quantos batem nele de perto), os traços, a coragem e a pele
(o couro grosso do ogro e a escama do homem-lagarto valem como armadura onde a peça não cobre). Cada um tem um **posto**: o goblin de faca, o de lança e escudo, o de arco, o capataz;
o orc, o orc bruto (malho de duas mãos), o capitão. Vale a regra de ouro de sempre: conta a peça de quem bate contra a peça de quem apanha.

A peça do povo é **gasta e malfeita**. Na luta vale a categoria dela; morto o dono, não presta para vender como peça: é **sucata** (o despojo da espécie: o ferro da lâmina e o
couro da armadura, em matéria).

**A criatura de corpo** (o corpo-seco, o carniçal, a múmia, o fogo-fátuo, a alma penada, o espectro, o golem de barro, a gárgula, o elemental do fogo, a harpia, o lobisomem,
o senhor vampiro) é um **bicho**: o corpo é a arma e a armadura, com categoria (capítulo 6). Quem tem o traço **lança** sabe feitiços; o corpo é o foco, e o instinto é a mão.
O bicho que lança, lança enquanto não alcança o inimigo; ao alcance, usa o corpo.

As criaturas **não entram** na lista dos bichos do capítulo 6, e os traços novos **não entram** na lista fechada dos traços dos bichos: moram na página das criaturas. Assim as
provas da etapa 2 seguem iguais.

### 15.2 O bestiário (19 criaturas)

| Criatura | Grau | Categoria | É | Bando | Traços | O que se sabe |
| --- | --- | --- | --- | --- | --- | --- |
| goblin | F | Comum | povo, pequeno | 2 a 4 | noturno | miúdo, frágil e covarde; nunca anda sozinho; mora em toca e rouba de noite |
| corpo-seco | E | Comum | corpo | 1 a 3 | sem vida, agarra, noturno | lento e sem dor; quem ele agarra não recua |
| esqueleto | E | Comum | povo (espada e escudo) | 2 a 4 | sem vida, ossos, noturno | a ponta e o fio passam entre os ossos: pede maça |
| orc | D | Incomum | povo | 2 a 4 | noturno | forte e mal treinado: vale pelo que veste e pelo número |
| fogo-fátuo | D | Incomum | corpo, pequeno | 1 a 3 | voa, imaterial, lança (a seta) | a luz que chama para o fundo do brejo |
| alma penada | D | Incomum | corpo | 1 a 2 | sem vida, imaterial, apavora | o aço comum passa por ela quase sem ferir |
| homem-lagarto | D | Incomum | povo (escama) | 2 a 3 | | de lança e escudo, segura um vau |
| carniçal | D | Incomum | corpo | 2 a 4 | sem vida, veneno, matilha, noturno | come os mortos e caça em roda |
| harpia | D | Incomum | corpo (fera) | 2 a 4 | voa | vem de cima, em bando |
| golem de barro | D | Incomum | corpo | 1 a 2 | sem vida, resiste | guarda o posto e a magia escorre nele |
| gárgula | C | Rara | corpo | 1 a 2 | voa, bote | parece pedra até cair em cima de quem passa |
| ogro | C | Raro | povo, grande (couro grosso) | 1 a 2 | | o tronco alcança antes da espada |
| múmia | C | Rara | corpo | 1 | sem vida, agarra, apavora, amaldiçoa | a maldição da cova |
| espectro | C | Raro | corpo | 1 | sem vida, imaterial, dreno, amaldiçoa | bebe a vida de quem toca |
| lobisomem | C | Raro | corpo (fera) | 1 | regenera, amaldiçoa, noturno | a mordida deixa a maldição da lua |
| elemental do fogo | C | Raro | corpo | 1 | sem vida, ardente, resiste | quem bate de perto se queima |
| cavaleiro da cova | B | Épico | povo (montante, placa) | 1 | sem vida, noturno | um mestre de armas que não cansa |
| gigante | B | Épico | povo, enorme | 1 | | oito batem nele, mas o tronco pega a três casas |
| senhor vampiro | B | Épico | corpo, CHEFE | 1 | dreno, regenera, apavora, noturno, lança (medo, sangria) | de dia é menos |

Só criatura do folclore e da fantasia comum; nada que seja criação de um jogo ou livro.
`criaturas.py lista` mostra a tabela; `criaturas.py ver NOME` dá a ficha; `bichos.py ameaca NOME` (ou `criaturas.py ameaca NOME`) dá a frase.

### 15.3 Os traços novos (a frase de cada um)

A luta roda os nove (capítulo 11; os números no `tabelas_magia.py`). A frase que a mesa lê:
- **resiste**: o corpo guarda contra a magia inteiro (não só 60%), e a Firmeza leva o bônus inteiro do corpo.
- **imaterial**: não tem carne; arma sem encanto e sem bênção conta uma categoria abaixo (o golpe vale um terço); o feitiço e a peça encantada contam inteiros; não vai ao chão nem é agarrado.
- **amaldiçoa**: a ferida que abre põe uma maldição da categoria do corpo, no passo 1 (ela anda dia a dia até alguém a quebrar: capítulo 13). Cada criatura que amaldiçoa tem o seu molde
  (a múmia: a maldição da cova; o espectro: o frio; o lobisomem: a maldição da lua; o vampiro: a sede).
- **lança**: sabe feitiços (a lista vem na ameaça), com a Mana e a Conjuração do instinto e da categoria do corpo.
- **sem vida**: não sangra, o veneno não pega e não foge; não cansa, mas não faz a ação a mais; a zero de PV se desfaz.
- **ossos**: o corte e a ponta valem metade; o impacto, inteiro.
- **dreno**: recupera em PV metade do que o golpe do corpo tira.
- **ardente**: quem golpeia de perto leva o fogo de volta (4 por categoria do corpo, a contar do Comum); a ferida que o corpo abre queima 5 rodadas.
- **noturno**: o escuro não tira nada do golpe nem do tiro.

### 15.4 A ameaça lida antes

Antes da luta lê-se a ameaça, como a do bicho: o grau, a categoria, o tamanho, quantos são (e quanto o bando pesa para quem está sozinho), os traços com a frase de cada um, o que
se sabe, e se foge. O povo diz o que veste, posto por posto ("veste peças Comuns gastas e malfeitas: goblin: adaga, couro; goblin lanceiro: lança, couro, escudo..."), e a conta da regra
de ouro contra o que você veste. O morto que anda diz que não foge. Quem lança diz o que lança. Do **chefe** ninguém sabe de graça: o Mestre lê a frase dele (`criaturas.py ameaca CHEFE`)
quando a cena o põe à frente (o que lança, com quem vem, e como muda ferido).

### 15.5 O povo foge, se rende e não fica

O povo testa a coragem como gente (com a coragem do povo: o goblin −4, o orc +2). Abalado, foge ou se rende. **Quem se rende a quem fica com o campo sai da contagem do ermo** (vai preso,
ou é rematado: a cena decide), e o despojo dele é o de um morto. Caído o líder do bando (o capataz goblin, o capitão orc), o bando testa a coragem. O morto que anda não testa nada.

### 15.6 O despojo

- **O povo:** a sucata das peças, da categoria do bando (o goblin: 1 de metal e 1 de couro Comuns; o orc: 1 de metal e 1 de couro Incomuns), de metade ao inteiro, como o bicho.
  A peça do povo nunca vira peça de vender: assim um bando morto não enche a loja de espadas.
- **O corpo:** a tabela da espécie, como o bicho (osso, couro, carvão do elemental, pano da múmia; o ser de magia não deixa nada).
- **A peçonha:** todo bicho e toda criatura de veneno dá peçonha da categoria dele, até a Rara (a surucucu, a aranha-de-toca, o basilisco, a serpe, a hidra, o carniçal).
- **O chefe de corpo** (o senhor vampiro) dá núcleo, como todo chefe.
- **A prata** não sai do corpo de ninguém: é a que o bando juntou, e mora no tesouro da toca (16.2).

### 15.7 Os chefes mágicos

Cada um vem com os lacaios, lança (ou solta o encanto da peça), e muda de **fase** abaixo de uma fração do PV: a luta para e pergunta. As fases só usam o que a luta roda: ganhar e
perder traços, aprender feitiço, recobrar Mana, o **brado** (os do lado dele ficam benzidos por 3 rodadas: +2 no acerto e +2 na coragem) e **erguer** os mortos.

| Chefe | Grau | O que é | Lança | Fases | Lacaios |
| --- | --- | --- | --- | --- | --- |
| o xamã goblin | D | goblin do pacto, talismã e amuleto Incomuns, atrás da linha | mau-olhado, medo, sangria | abaixo de 50%: uiva (brado), recobra 3 de Mana | 2 goblins da guarda (põem o corpo na frente dele), o capataz, 4 de faca, 2 de lança, 2 de arco |
| o senhor da guerra orc | C | orc mestre de armas, machado Raro com o encanto do medo (uma vez por luta) | (o encanto) | abaixo de 50%: entra em fúria e urra (brado) | 2 orcs da guarda (Raros), 4 orcs, 2 orcs brutos |
| a bruxa do brejo | C | bruxa do pacto, talismã Raro | mau-olhado, medo, sangria, nó | abaixo de 40%: larga a pele de velha (a faca dela passa a amaldiçoar), recobra 6 de Mana | o trasgo, 3 fogos-fátuos Raros, 3 afogados (corpos-secos Raros) |
| o necromante | B | do pacto, talismã Épico, frágil, atrás dos mortos | sangria, mau-olhado, nó, medo | abaixo de 70% e de 35%: ergue 3 mortos (dos dois lados) | o cavaleiro da cova (guarda), 6 esqueletos Raros |
| o senhor vampiro | B | criatura de corpo, CHEFE, atrás dos lacaios (lança de longe; ao alcance, usa o corpo) | medo, sangria | abaixo de 30%: a sede (cada ferida que abre amaldiçoa) | 3 carniçais, 3 lobos |

### 15.8 As medidas (o banco: `provas_criaturas.py`)

- **O bando contra o homem do degrau** (espada, malha, elmo e escudo da categoria, no nível de referência: o Comum 10, o Incomum 30): o bando que um homem do degrau enfrenta de igual
  para igual é de **quatro goblins** (o homem vence cerca de 54%) e de **dois orcs** (cerca de 44%). Contra três goblins ele vence 78%; contra três orcs, 10%. A faixa: de 35 a 65%.
- **O chefe com os lacaios contra quatro homens** do degrau em que vive: o xamã contra quatro Comuns, cerca de 47%; o senhor da guerra contra quatro Raros, 41%; a bruxa do brejo, 57%;
  o necromante contra quatro Épicos, 58%; o senhor vampiro, 45%. A faixa: de 30 a 70%.
- **A patrulha goblin contra o guerreiro de nível 5 de peças Comuns** (o começo "guerreiro" da vila de teste: espada, escudo e malha, sem elmo), como a caça a dá (de dois a quatro, de
  faca; metade das vezes ele a vê primeiro): ele vence cerca de 73% e morre em cerca de 12%. A faixa: de 40 a 75%, e morre em 15% ou menos. Contra dois: 91% e 5%; contra quatro: 51% e 27%.
  **Uma observação para o jogador:** nesta luta, quem cai do lado que perde morre na metade das vezes (o teste de morte); por isso, para morrer em 15% ou menos, ele tem de vencer
  70% ou mais. A janela da meta é estreita (de 70 a 75%), e o goblin ficou miúdo e frágil para caber nela.

---

## 16. O COVIL E A VILA DE TESTE COM A MAGIA

### 16.1 O covil é contado ao lado da fauna

O covil é a toca de um povo num ermo (`lugar.covil`). **As cabeças dele SÃO a contagem da espécie no ermo** (`lugar.bichos.goblin`), ao lado da corça e do lobo: a patrulha que o
caçador encontra sai dela, e quem morre sai dela. O registro do covil guarda o resto: o nome, o teto, se o líder está de pé, o chefe que mora ali (ou nenhum), a fome, o último roubo,
os dias sem líder, os dias de toca cheia, e os dias até chegar um bando de fora quando ela se esvazia. **O covil não guarda prata:** o tesouro da toca é o estoque do ermo, contado como toda prata.

As criaturas que não são fera (o povo, o morto, o ser de magia) **não criam na virada da caça**: o bando de um covil cria pela vida do covil; os mortos de uma cova ficam os que são.

### 16.2 A vida da toca (todo dia, evento "covil", o mundo sozinho)

1. **Come:** 0,3 de comida por goblin (0,6 por orc), primeiro do que juntou (a comida do estoque do ermo), depois da caça contada do ermo (a corça e o javali, pela fartura).
2. **Rouba:** a cada 7 dias (10 para o orc), da vila vizinha, com a chance de cabeças ÷ 20 (mais 10% por ponto de fome): 2 de comida por cabeça; uma vez em quatro, também prata
   (de 1 a 6, mais uma por quatro cabeças). O que rouba vai para o estoque do ermo: **o tesouro da toca.** A prata só muda de mão.
3. **Cria** devagar, bem comido, até o teto (16 goblins): cabeças × 2,5% × o que falta para o teto, por dia. **Definha** com fome (um a menos por dia, com a fome em 9).
4. **O líder:** caído o capataz, outro sobe em 7 dias. **O chefe:** a toca cheia (12 ou mais) por 30 dias seguidos ganha o xamã goblin. A toca vazia espera 120 dias por um bando de fora (6 goblins).

Medido (um ano sozinho, a toca da vila de teste): o bando chega ao teto (16) e não passa dele; a corça fica em 75 a 78 de 80, o javali em 38 a 39 de 40; rouba de 1.000 a 1.400 de
comida no ano (a vila produz 146.000) e de 40 a 110 de prata; o xamã sobe perto do Dia 62; a prata do mundo fecha.

### 16.3 A toca na caça

- `caca.py sair ERMO alvo=toca` procura a toca do bando: o rastro é 2 mais difícil que o da espécie, e a rolagem é **oculta** (ninguém sabe de graça se há toca, como no chefe).
- Achada, lê-se a frase da toca: de fora se contam poucos, um bando, muitos ou uma toca cheia; se há chefe, só se vê o sinal (os ossos pintados, o fumo doce). Depois, a ameaça do povo.
- A luta é com **todos os que estão lá**: o chefe e a guarda dele (se a toca tem chefe), o líder (atrás da linha) e o resto pelos postos (metade de faca, um quarto de lança, um quarto de arco).
  O chefe não é da contagem: mora no registro do covil.
- **Quem fica com o campo na toca leva o tesouro inteiro** (a prata e a comida do estoque do ermo), repartido entre quem lutou até o fim. Caído o líder ou o chefe, o covil fica sem ele.
- **O que cai no chão de um ermo com toca, o bando junta:** a carga e a prata de quem morre ali entram no tesouro da toca, e a mesa diz assim.

**Limpar um covil não é mina** (medido): a casa de três (o guerreiro de nível 5, Tomé e Rute), 60 dias ao lado da toca da vila de teste, saindo quando os três estão inteiros e
esperando quando alguém está ferido, tira cerca de **0,5 diária por dia de trabalho de cada um** (a melhor vida, cerca de 1,6), e morre alguém da casa em 1 ou 2 vidas de cada 12.
O primeiro assalto rende o tesouro (20 de prata, na vila de teste) e a sucata; os seguintes, quase só sucata, e o bando que fugiu volta devagar.

### 16.4 O Mestre funda um covil

`criaturas.py covil poe ERMO goblin [cabecas=N] [tesouro=N] [chefe=sim]` (ou `orc`): num ermo que já existe, por um evento "mestre" (o tesouro é prata que nasce, como tudo o que o
Mestre põe). `criaturas.py covil [ERMO]` mostra o covil (SÓ O MESTRE; a mesa traz a linha dele no SÓ O MESTRE).

### 16.5 A vila de teste com a etapa inteira

A vila nova (`vila_teste.py PASTA ... [inclinacao=CAMINHO]`) nasce com os talentos e os dons. Para **a vila que já existe** (o save de quem já joga):

```
python3 vila_teste.py magia PASTA [inclinacao=CAMINHO]
```

Acrescenta, **só por eventos, sem recriar nada** (e recusa rodar duas vezes):
1. **Os talentos e os dons** de quem ainda não foi rolado; o personagem com a inclinação, se o jogador escolher uma (só vale enquanto o talento dele não foi rolado).
2. **Anselmo, o mago velho** (nível 40, arcano Treinado: a luz, a seta, o escudo, prender, a lança de fogo; cajado Incomum, amuleto Comum).
3. **A botica da curandeira:** Pedra Rasa ganha a botica (1), e Nara a mão de Iniciante na alquimia.
4. **O santuário** (1) e **Lúcia, a clériga** (nível 35, fé de Mestre, voto do socorro: a cura, a bênção, o amparo, o castigo, quebrar maldição; símbolo Comum).
5. **Joana, a bruxa** da choupana na borda da Mata do Corvo (nível 30, pacto Treinado: o mau-olhado, o medo, a sangria, ler, o nó; deve 2; leva 3 doses de veneno de lâmina e erva).
6. **O Grande Dom de forja do Zeca**, o aprendiz, que ninguém leu (aparece quando decidir um teste na bancada, ou quando alguém o ler).
7. **A Cova Velha**, um ermo novo vizinho da vila (ruína, borda): 3 esqueletos e 2 corpos-secos, e **a Espada do Guardião** largada no chão (Incomum, maldita: a Mão Fria, míngua;
   quem a puser em uso pega a maldição; quebra devolvendo-a à cova).
8. **A toca dos goblins** na Mata do Corvo: 8 goblins (teto 16), o capataz, 20 de prata no tesouro.

A prata que nasce: a das três pessoas novas (145) e o tesouro da toca (20). Nada mais muda: a gente, os itens e o tempo de antes seguem como estavam.

### 16.6 O que fica para depois

O covil não ataca a vila nem gente na rua (o roubo é contado, não jogado); o bando que fugiu não se junta a outro covil; os povos não comerciam; o necromante e a bruxa do brejo não
têm covil próprio na vila de teste (o Mestre põe quando quiser); masmorras, frentes e rivais são das etapas 5 e 6.
