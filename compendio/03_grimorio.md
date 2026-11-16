# GRIMÓRIO COMPLETO

Treze escolas, do 1º ao 9º círculo, 247 feitiços aqui e mais 39 no **Livro Nove** (286 ao todo; os truques, o ritual, a concentração, o pergaminho, o choque de feitiços e o feitiço composto também estão lá). **A lista é fechada.** O Mestre não inventa feitiço fora dela. Um feitiço novo só nasce de **Receita Mestra** ou de **pacto**, e entra nesta lista quando nasce. Esta regra da casa (Dia 356) substitui a linha do Motor que dizia "6º a 9º: o Mestre revela em jogo".

## Como a magia funciona (Motor X.8 e casa)

| Círculo | Quem chega | Custo | Dano num alvo | Em massa |
| --- | --- | --- | --- | --- |
| 1º a 3º | Magia Treinado | círculo × 5 de Mana | 2d6 × círculo | — |
| 4º a 6º | Magia Mestre e nível 50 | círculo × 5 | 4d6 × círculo | 1d6 × 20 soldados comuns |
| 7º e 8º | Magia Lendário, nível 150 e um **componente raro** | círculo × 5 | 10d6 × círculo | 1d6 × 100 |
| 9º | Magia Lendário, nível 300 e Receita Mestra ou pacto | 100 e **um preço** | 100d6 | o nome de uma cidade |

- **Teste:** d20 + bônus do atributo + maestria de Magia + bônus do foco. Contra um alvo, rola contra a Resistência Mental dele (10 + bônus de Vontade + nível ÷ 10). Em área, rola contra CD 15 + círculo × 5.
  - **Em luta (casa, Dia 379: magia disputada):** o feitiço de dano rola como um golpe, 2d20 + ataque contra a Defesa + 14 do alvo. Pega em cheio: dano inteiro. O alvo resiste: metade. Um 20 que morde dobra os dados. Dois 1: o feitiço se desfaz. É assim que o `luta.py` roda.
- **MAGIA MAIS FORTE (casa, Dia 200):** o dano e a cura são multiplicados pelo **foco** de quem lança: Comum ×1 · Incomum ×1,25 · Raro ×1,5 · Épico ×2 · Único ×3 · Lendário ×5 · Mítico ×10 · Primordial ×20 (casa, Dia 356). Em área, vale metade do multiplicador (no mínimo ×1): **todo feitiço marcado "(área)" entra na ficha de combate com a metade, mesmo contra um alvo só** (conferido no Dia 437: a Chuva de Brasas estava inteira nas fichas e foi acertada). Um feitiço preso numa peça usa a categoria da peça como foco.
- **Saber um feitiço** é poder lançá-lo (Magia) e poder imbuí-lo (Encantamento): o feitiço conhecido conta como receita de encantamento.
- **Aprender:** uma aula por semana com quem sabe (o Colégio, um mestre ou um grimório). Do 7º círculo para cima só se aprende com um Lendário, com uma Receita Mestra ou com um grimório antigo.
- **Sem foco material** (veja a tabela das escolas), o custo de Mana dobra.
- **Retrochoque:** conjurar sem Mana ou tirar 1 natural causa círculo × 1d10 de dano no conjurador. Do 7º círculo para cima, também tira 1 ponto permanente de Vigor ou de Vontade.
- **Sangue e Osso cobram sempre:** 1d6 × círculo de PV por conjuração e 1 ponto de desgaste permanente a cada 10 conjurações.
- **Tipos:** ataque · defesa · cura · utilidade · *arma* (feito para ir numa peça como encantamento; todo feitiço pode ir numa peça).
- **Técnicas de Aura** dos guerreiros: veja o fim deste grimório.

| Escola | Atributo | Foco material |
| --- | --- | --- |
| Chama | Int | pederneira ou brasa |
| Gelo | Int | água ou neve |
| Pedra | Int | uma pedra |
| Vento | Int | uma pena |
| Luz | Sab | vela ou vidro |
| Raiz | Sab | semente ou folha viva |
| Sombra | Von | pano preto |
| Sangue | Afi | o próprio sangue (cobra sempre) |
| Osso | Von | osso (cobra sempre) |
| Vazio | Von | algo quebrado |
| Elo | Afi | metal ou argola |
| Tempo | Int | areia |
| Mente | Von | a palavra |

## CHAMA (Int)

| Círculo | Feitiço | Efeito | Tipo |
| --- | --- | --- | --- |
| 1º | **Faísca** | 2d6 de fogo num alvo a 9 m | ataque |
| 1º | **Alma de Brasa** | a peça guarda fogo: 1x por cena +1d6 de fogo no golpe ou acende qualquer coisa | arma |
| 2º | **Dardo Arcano** | 4d6, ignora armadura leve | ataque |
| 2º | **Calor de Forja** | um metal à mão fica em brasa por 1 minuto (molda sem fornalha; quem segura sem luva solta) | utilidade |
| 3º | **Flor de Brasa** | bola de fogo de 3 m de raio, 6d6 (área) | ataque |
| 3º | **Mão de Forja** | a mão do conjurador vira brasa por 1 cena: toque 6d6 de fogo e solda metal sem fornalha | arma |
| 4º | **Chuva de Brasas** | 9 m, 8d6 de fogo, o chão queima 2 rodadas (área) | ataque |
| 4º | **Muralha de Fogo** | um muro de 12 m × 3 m arde por 1 cena; quem atravessa leva 8d6 (área) | defesa |
| 5º | **Lança de Magma** | 20d6 de fogo num alvo a 30 m; a armadura de metal dele fica em brasa (−2 de Defesa até tirar) | ataque |
| 5º | **Coração de Fornalha** | uma forja ou fogueira fica 1 dia no calor de uma Fornalha Mestra (+2 no Processo de quem forja nela) | utilidade |
| 5º | **Pele de Brasa** | por 1 cena, quem toca ou golpeia o alvo corpo a corpo leva 4d6 de fogo; RD +5 contra frio | defesa |
| 6º | **Sol de Mão** | uma esfera de 9 m de raio explode a 60 m: 24d6 de fogo (área), e o chão queima 3 rodadas | ataque |
| 6º | **Passo de Brasa** | o conjurador some numa chama e sai de outra a até 1 km | utilidade |
| 6º | **Forja Sem Mão** | 1 dia: um martelo invisível bate sozinho numa obra Comum a Rara enquanto o ferreiro dorme (a obra anda 8 horas) | utilidade |
| 7º | **Chuva de Estrelas** | 12 rodadas de fogo do céu num raio de 30 m, 70d6 na primeira e 4d6 nas outras (área). Componente: um núcleo de Fogo Raro | ataque |
| 7º | **Alma de Fornalha** | um fogo vira criatura (Épica, nível = do conjurador ÷ 2) e serve 1 dia. Componente: brasa de uma forja que nunca apagou | utilidade |
| 8º | **Coroa de Fogo** | por 1 cena o conjurador arde: imune a fogo, +80d6 num golpe ou feitiço por rodada, quem está a 6 m leva 6d6. Componente: um núcleo de Fogo Épico | arma |
| 8º | **Cidade em Brasa** | um quarteirão inteiro pega fogo que água não apaga, por 1 dia. Componente: cinza de uma cidade que já queimou | ataque |
| 9º | **O Olho da Chama** | por um instante a Chama Sem Fim olha: 100d6 em tudo num raio de 1 km, e a terra vira vidro. PREÇO: o conjurador perde uma mão para sempre, e a coberta afina ali (magia selvagem por um ano) | ataque |

## GELO (Int)

| Círculo | Feitiço | Efeito | Tipo |
| --- | --- | --- | --- |
| 1º | **Frio de Mão** | congela água, conserva comida um mês, ou 2d6 de frio no toque | utilidade |
| 1º | **Gelo no Chão** | 3 m de chão viram gelo por 1 cena: Agilidade CD 15 ou cai | utilidade |
| 2º | **Névoa Fria** | esconde uma área de 9 m por 1 cena | utilidade |
| 2º | **Ponte de Gelo** | uma passarela de gelo de 10 m sobre água ou abismo, por 1 hora | utilidade |
| 3º | **Geada de Lâmina** | o golpe congela: −4 de Defesa e Lento 1 rodada | arma |
| 3º | **Muralha de Gelo** | bloqueia uma passagem (RD 12, 60 PV) | defesa |
| 4º | **Inverno Breve** | 16d6 de frio num alvo, que fica preso no gelo 1 rodada | ataque |
| 4º | **Lança de Gelo** | 16d6 de frio num alvo a 30 m; se cair a 0 PV, vira estátua | ataque |
| 5º | **Tumba de Gelo** | prende um alvo num bloco de gelo por 3 rodadas (Força CD 35 para sair); dentro, não respira nem sangra | ataque |
| 5º | **Inverno de Campo** | 1 dia de neve e gelo num raio de 1 km: rios congelam, tropa marcha à metade | utilidade |
| 5º | **Armadura de Gelo** | RD +8 e imune a fogo por 1 cena; quem golpeia corpo a corpo fica Lento 1 rodada | defesa |
| 6º | **Nevasca** | 3 rodadas de nevasca em 18 m: 24d6 de frio na primeira e 4d6 nas outras, ninguém enxerga (área) | ataque |
| 6º | **Castelo de Gelo** | ergue uma torre de gelo de 10 m com portas e escadas, que dura até o degelo | defesa |
| 6º | **Sono Branco** | um ferido grave dorme no gelo sem piorar por 1 mês | cura |
| 7º | **Rio Parado** | um rio inteiro congela por 1 dia em 1 km de largura; barcas presas, tropa atravessa. Componente: água de uma fonte que nunca gelou | utilidade |
| 7º | **Coração Gelado** | 70d6 de frio num alvo; se cair a 0, o coração vira gelo e não ressuscita. Componente: um núcleo de Gelo Raro | ataque |
| 8º | **Inverno Eterno** | um vale fica no inverno por um ano. Componente: neve dos Picos Brancos colhida em noite sem lua | utilidade |
| 8º | **Exército de Gelo** | ergue 100 soldados de gelo (comuns) por 1 dia. Componente: um núcleo de Gelo Épico | utilidade |
| 9º | **O Hálito da Mãe Branca** | tudo num raio de 1 km congela de uma vez: 100d6 e quem morre fica de pé, em gelo, para sempre. PREÇO: o conjurador nunca mais sente calor (−5 em Vigor, para sempre), e a Mãe Branca sabe o nome dele | ataque |

## PEDRA (Int)

| Círculo | Feitiço | Efeito | Tipo |
| --- | --- | --- | --- |
| 1º | **Mão de Pedra** | o punho ou a arma vira pedra: +2 de dano, não quebra | arma |
| 1º | **Pedra que Fala** | sabe o que passou por cima de uma pedra no último dia (peso, número, direção) | utilidade |
| 2º | **Pele de Pedra** | +4 de Defesa por 3 rodadas | defesa |
| 2º | **Abrir a Rocha** | abre uma passagem de 1 m em rocha ou muro de pedra (1 minuto) | utilidade |
| 3º | **Raiz de Pedra** | o alvo não pode ser derrubado, empurrado nem arrastado por 1 cena | defesa |
| 3º | **Muro Erguido** | ergue um muro de pedra de 6 m × 3 m (permanente) | defesa |
| 4º | **Tremor** | quem está a 12 m cai (Agilidade CD 25) e leva 4d6 | ataque |
| 4º | **Mão da Terra** | uma mão de pedra agarra um alvo a 18 m: preso e 16d6 por rodada até ele vencer Força CD 30 | ataque |
| 5º | **Terremoto** | tudo em 18 m cai e leva 20d6; muros de pedra rangem (área) | ataque |
| 5º | **Corpo de Pedra** | por 1 cena o conjurador vira pedra viva: RD +10, Força +20, movimento à metade | defesa |
| 5º | **Abrir Caminho** | abre um túnel de 3 m × 3 m × 30 m em rocha (10 minutos), escorado | utilidade |
| 6º | **Golem de Pedra** | ergue um golem de pedra (Épico, nível = do conjurador ÷ 2) que serve 1 dia | utilidade |
| 6º | **Engolir** | o chão engole um alvo até o peito (Agilidade CD 45): preso até ser cavado | ataque |
| 6º | **Muralha de Cidade** | ergue 60 m de muralha de 6 m de altura, permanente | defesa |
| 7º | **A Montanha Cai** | uma encosta desaba sobre 60 m: 70d6 e tudo fica soterrado (área). Componente: um núcleo de Terra Raro | ataque |
| 7º | **Veio Chamado** | um veio de metal sobe à superfície onde ele existe a até 1 km (revela e expõe). Componente: um lingote do mesmo metal | utilidade |
| 8º | **Fortaleza do Chão** | ergue uma fortaleza de pedra com muralha, torres e porta em 1 hora, permanente. Componente: pedra de uma fortaleza caída | defesa |
| 8º | **Coração da Montanha** | o conjurador e 10 aliados não podem ser movidos, derrubados nem esmagados por 1 dia; RD +15 | defesa |
| 9º | **Abrir a Terra** | a terra se abre numa fenda de 1 km que engole o que estiver em cima. PREÇO: um deus dorme menos ali (um monstro grande acorda em 1d6 meses), e o conjurador fica preso ao chão: nunca mais flutua, voa ou atravessa água funda | ataque |

## VENTO (Int)

| Círculo | Feitiço | Efeito | Tipo |
| --- | --- | --- | --- |
| 1º | **Empurrão** | empurra 2 m, ou apaga fogo pequeno | utilidade |
| 1º | **Passo de Vento** | +6 m de movimento e salto triplo por 1 rodada | defesa |
| 2º | **Voz no Vento** | a voz chega a 1 km, ou uma conversa longe é ouvida | utilidade |
| 2º | **Ar Limpo** | tira fumaça, gás e névoa de 9 m; respira bem por 1 hora debaixo d'água ou na fumaça | utilidade |
| 3º | **Escudo de Vento** | projéteis erram com 1-10 no d20 por 1 cena | defesa |
| 3º | **Lâmina de Vento** | 6d6 num alvo a 18 m, atravessa cobertura leve | ataque |
| 4º | **Tempestade Local** | 3 rodadas de vento e raio, 4d6 por rodada em 9 m (área) | ataque |
| 4º | **Asas de Vento** | voa por 1 cena (movimento × 2) | utilidade |
| 5º | **Ciclone** | um redemoinho de 6 m anda 12 m por rodada por 3 rodadas: 20d6, joga longe quem pega (área) | ataque |
| 5º | **Vento de Viagem** | uma barca ou caravana anda o dobro por 1 dia | utilidade |
| 5º | **Raio** | 20d6 de raio num alvo a 60 m, e salta para mais 2 a 9 m dele (metade) | ataque |
| 6º | **Tempestade** | 1 hora de tempestade em 1 km: raio cai 1d6 vezes por rodada onde o conjurador mandar (24d6 cada, área) | ataque |
| 6º | **Andar no Ar** | 10 aliados andam no ar por 1 hora | utilidade |
| 6º | **Muralha de Vento** | um muro de vento de 30 m: projétil não passa, criatura pequena é jogada longe | defesa |
| 7º | **Furacão** | um furacão anda 1 km arrasando: 70d6 em tudo no caminho, navios afundam. Componente: um núcleo de Vento Raro | ataque |
| 7º | **Corpo de Vento** | por 1 cena o conjurador vira vento: só magia o fere, passa por frestas, voa | defesa |
| 8º | **O Céu Fecha** | uma região de 10 km fica 1 dia sem sol, com chuva e raio; tropa e caravana param. Componente: uma pena de ave que voa acima das nuvens | utilidade |
| 8º | **Martelo do Céu** | um raio de 80d6 cai num alvo a até 1 km que o conjurador vê. Componente: um núcleo de Raio Épico | ataque |
| 9º | **O Fôlego dos Deuses** | um vento varre um país inteiro: frotas afundam, muralhas caem, a colheita voa. PREÇO: o conjurador perde a voz para sempre (não fala, não lança feitiço de Palavra), e a coberta afina | ataque |

## LUZ (Sab)

| Círculo | Feitiço | Efeito | Tipo |
| --- | --- | --- | --- |
| 1º | **Luz Menor** | luz de tocha por 1 hora, ou cega 1 rodada com 18-20 | utilidade |
| 1º | **Benção de Luz** | +2 num teste de um aliado e cura 1d6 | cura |
| 2º | **Cura Menor** | cura 4d6 | cura |
| 2º | **Ver o Escondido** | revela invisível e ilusão a 9 m por 1 cena | utilidade |
| 3º | **Purificar** | remove maldição, veneno ou doença de um | cura |
| 3º | **Clarão** | cega todos a 9 m por 1 rodada (Vontade) | defesa |
| 4º | **Lança do Sol** | 16d6 de luz, dobrado contra mortos e sombra | ataque |
| 4º | **Cura Maior** | cura 16d6 e tira Sangrando, Atordoado e Envenenado | cura |
| 5º | **Cura em Roda** | cura 20d6 em até 6 aliados a 9 m (área: metade do multiplicador) | cura |
| 5º | **Escudo de Luz** | um domo de 6 m por 1 cena: morto-vivo e sombra não entram, projéteis −4 | defesa |
| 5º | **Verdade** | numa área de 9 m ninguém consegue mentir por 1 cena (Vontade CD 40) | utilidade |
| 6º | **Erguer o Caído** | devolve à vida quem morreu há até 1 hora, com 1 PV e −1 permanente num atributo | cura |
| 6º | **Sol de Meio-Dia** | luz de sol num raio de 300 m por 1 hora: mortos-vivos levam 4d6 por rodada, sombra não age | ataque |
| 6º | **Selo Santo** | sela uma porta, túmulo ou cripta contra mortos e sombras por um ano | defesa |
| 7º | **Ressurreição** | devolve à vida quem morreu há até 1 mês, inteiro. Componente: um núcleo de Luz Raro e algo que o morto amou | cura |
| 7º | **Lança da Aurora** | 70d6 de luz num alvo, triplicado contra mortos e sombra. Componente: orvalho colhido na primeira luz | ataque |
| 8º | **Dia Sem Noite** | uma cidade não tem noite por 7 dias: nenhum morto-vivo anda, nenhuma sombra esconde. Componente: um núcleo de Luz Épico | utilidade |
| 8º | **Curar a Cidade** | cura toda doença de uma cidade (Febre incluída, mas não a do pó: o pó volta). Componente: água de três templos | cura |
| 9º | **O Olhar da Luz que Cega** | a Luz que Cega olha por um instante: todo morto-vivo e toda sombra num raio de 10 km se desfaz; quem olha fica cego. PREÇO: o conjurador fica cego para sempre, e a Lumine sabe onde ele está | ataque |

## RAIZ (Sab)

| Círculo | Feitiço | Efeito | Tipo |
| --- | --- | --- | --- |
| 1º | **Broto** | uma semente vira planta adulta em 1 minuto; ou acha erva comum a 1 km | utilidade |
| 1º | **Espinho** | 2d6 de espinho num alvo a 9 m; Sangrando 1 rodada | ataque |
| 2º | **Pele de Casca** | +4 de Defesa contra dano físico por 1 cena; vulnerável a fogo | defesa |
| 2º | **Falar com Bicho** | fala com um animal por 1 cena (ele responde como bicho) | utilidade |
| 3º | **Raízes que Prendem** | raízes prendem tudo em 6 m por 2 rodadas (Força CD 25) | ataque |
| 3º | **Cura da Mata** | cura 6d6 e tira veneno de planta ou bicho | cura |
| 4º | **Forma de Fera** | vira um animal grande (urso, lobo, águia) por 1 cena, com os PV dele somados | utilidade |
| 4º | **Mata Fechada** | uma área de 30 m vira mata fechada por 1 dia: movimento à metade para quem não é da mata | defesa |
| 5º | **Praga** | 20d6 em todos num raio de 9 m e a colheita ali morre por um ano (área) | ataque |
| 5º | **Colheita Boa** | um campo de 1 km rende o dobro nesta colheita (Comida +1 na cidade por uma estação, 1x por estação) | utilidade |
| 5º | **Árvore que Anda** | uma árvore vira guardião (Épico, nível = do conjurador ÷ 2) por 1 dia | utilidade |
| 6º | **Caminho da Mata** | o conjurador e 10 aliados entram numa árvore e saem noutra da mesma espécie a até 100 km | utilidade |
| 6º | **Enxame** | um enxame cobre 18 m por 3 rodadas: 24d6 na primeira e 4d6 nas outras (área) | ataque |
| 6º | **Remédio Vivo** | cura uma doença de uma aldeia inteira (até 200 pessoas) | cura |
| 7º | **A Mata Acorda** | uma floresta inteira luta por 1 dia contra quem o conjurador apontar. Componente: seiva de uma árvore de mil anos | ataque |
| 7º | **Forma de Fera Antiga** | vira uma fera Épica por 1 cena, com os PV e golpes dela. Componente: um osso dela | utilidade |
| 8º | **Primavera** | uma região de 10 km sara de praga, seca ou maldição de terra. Componente: semente do Sono Verde | cura |
| 8º | **Fome da Terra** | a terra come uma tropa: 80d6 em todos num campo de 300 m (área). Componente: um núcleo de Vida Épico | ataque |
| 9º | **O Sono Verde Sonha** | uma região inteira vira mata em um dia: cidades, muros e estradas cobertos. PREÇO: o conjurador vira árvore aos poucos (perde 1 de Agilidade por mês até parar) e o Sono Verde se mexe | utilidade |

## SOMBRA (Von)

| Círculo | Feitiço | Efeito | Tipo |
| --- | --- | --- | --- |
| 1º | **Passo Mudo** | não faz som por 1 cena | utilidade |
| 1º | **Sombra Amiga** | +4 em Furtividade por 1 cena na penumbra | defesa |
| 2º | **Manto de Sombra** | invisível no escuro por 1 cena, ou até atacar | defesa |
| 2º | **Olho da Sombra** | vê pelos olhos de uma sombra a 30 m | utilidade |
| 3º | **Medo** | o alvo foge 1d4 rodadas (Vontade) | ataque |
| 3º | **Porta de Sombra** | salta de uma sombra a outra a até 30 m | utilidade |
| 4º | **Noite Fechada** | apaga toda luz em 18 m por 1 cena | defesa |
| 4º | **Lâmina de Sombra** | 16d6 de sombra num alvo; ignora armadura | ataque |
| 5º | **Exército de Sombras** | 10 sombras (Raras) lutam por 3 rodadas | ataque |
| 5º | **Sumir de Vez** | invisível por 1 hora, mesmo atacando (mas quem é atingido sabe de onde veio) | defesa |
| 5º | **Pesadelo** | um alvo que dorme sonha o pior medo dele: não descansa e acorda com −4 em tudo por 1 dia | ataque |
| 6º | **Estrada de Sombra** | 10 aliados entram numa sombra e saem noutra a até 50 km | utilidade |
| 6º | **Roubar a Sombra** | arranca a sombra do alvo: ele não cura nem descansa até ela voltar (1 semana ou o conjurador devolver) | ataque |
| 6º | **Casa Escondida** | uma casa inteira some da vista e da magia de procura por um mês | defesa |
| 7º | **Noite Sobre a Cidade** | uma cidade fica no escuro absoluto por 1 dia; só a luz mágica do 7º ou mais acende. Componente: um núcleo de Sombra Raro | utilidade |
| 7º | **Duplo de Sombra** | uma cópia de sombra do conjurador age por 1 dia, com metade do nível dele. Componente: o espelho de um morto | utilidade |
| 8º | **Engolir na Sombra** | o alvo é engolido pela própria sombra e some por 1 dia (Vontade CD 55); se falhar duas vezes, volta louco. Componente: um núcleo de Sombra Épico | ataque |
| 8º | **Mil Olhos** | o conjurador vê por todas as sombras de uma cidade por 1 dia. Componente: os olhos de uma ave noturna | utilidade |
| 9º | **A Noite Que Não Acaba** | uma região de 10 km fica na noite por um mês; as sombras andam sozinhas. PREÇO: a sombra do conjurador vai embora para sempre e trabalha contra ele | ataque |

## SANGUE (Afi)

| Círculo | Feitiço | Efeito | Tipo |
| --- | --- | --- | --- |
| 1º | **Sangue Quente** | +4 contra frio, veneno e doença por 1 dia (custa 1d6 de PV) | defesa |
| 1º | **Gosto de Sangue** | sabe o nome, a família e a doença de quem deixou uma gota | utilidade |
| 2º | **Fechar Ferida** | para o Sangrando e cura 2d6 de outro, com o próprio sangue | cura |
| 2º | **Rastro de Sangue** | segue quem sangrou num raio de 1 km por 1 dia | utilidade |
| 3º | **Frenesi** | +4 de Força e −3 de Defesa por 3 rodadas | arma |
| 3º | **Laço de Sangue** | dois que dividem sangue sabem a dor e o lugar um do outro por 1 mês | utilidade |
| 4º | **Corrente de Sangue** | drena 16d6 e devolve metade a quem lança | ataque |
| 4º | **Ferver o Sangue** | 16d6 num alvo que sangra; ele fica Sangrando (2d6 por rodada) | ataque |
| 5º | **Doar a Vida** | passa até 100 PV do conjurador para outro, inteiros | cura |
| 5º | **Marionete** | controla o corpo de um alvo que sangra por 3 rodadas (Vontade CD 40 a cada rodada) | ataque |
| 5º | **Sangue de Ferro** | por 1 cena o conjurador não sangra, não cai a 0 enquanto tiver Mana (cada golpe que o levaria a 0 custa 10 de Mana) | defesa |
| 6º | **Chuva de Sangue** | 24d6 em todos que sangram a 18 m, e metade volta ao conjurador como cura (área) | ataque |
| 6º | **Laço de Família** | sabe onde está todo parente vivo de alguém, e fala com um deles por 1 minuto | utilidade |
| 6º | **Sangue Novo** | tira uma doença do sangue (veneno, Febre do brejo, maldição de sangue), mesmo antiga | cura |
| 7º | **Exército Ferido** | todos os inimigos que sangram num campo de 300 m perdem 1d6 × 10 PV por rodada por 3 rodadas. Componente: sangue de um Lendário | ataque |
| 7º | **Corpo Emprestado** | o conjurador mora no corpo de outro por 1 dia (Vontade CD 55). Componente: o sangue dele e um fio de cabelo | utilidade |
| 8º | **Pacto de Sangue** | um pacto entre dois que o sangue cobra: quem quebra morre em 1 dia. Componente: um cálice de therk ou ouro de templo | utilidade |
| 8º | **Vida Longa** | o alvo para de envelhecer por 10 anos. Componente: o coração de uma fera Épica que bebeu sangue | cura |
| 9º | **O Rio Vermelho** | todo sangue inimigo num raio de 1 km obedece por um instante: 100d6. PREÇO: o conjurador perde metade do sangue para sempre (PV máximo à metade) e a sede de sangue: −5 em Vontade | ataque |

## OSSO (Von)

| Círculo | Feitiço | Efeito | Tipo |
| --- | --- | --- | --- |
| 1º | **Ler o Osso** | sabe como morreu quem deixou o osso | utilidade |
| 1º | **Sentir a Morte** | sabe se alguém a 30 m está morrendo, morto ou morto-vivo | utilidade |
| 2º | **Mão do Morto** | uma mão de esqueleto obedece por 1 hora (carrega, abre, segura) | utilidade |
| 2º | **Ossos que Andam** | um esqueleto pequeno (bicho) obedece por 1 dia: espia, carrega recado | utilidade |
| 3º | **Falar com Morto** | três perguntas a um morto | utilidade |
| 3º | **Armadura de Osso** | RD +4 por 1 cena | defesa |
| 4º | **Quebra-Ossos** | 16d6 e o alvo perde 1 ataque por rodada por 1 cena | ataque |
| 4º | **Servo de Osso** | ergue um esqueleto (soldado comum) por 1 dia | utilidade |
| 5º | **Reanimar** | ergue um morto como servo (o nível dele em vida, até a metade) por 1 dia; 1 servo por dia | utilidade |
| 5º | **Mão Que Seca** | 20d6 no toque; a carne do alvo seca (−4 em Força até curar com magia de 5º) | ataque |
| 5º | **Muro de Ossos** | um muro de ossos de 12 m × 3 m que agarra quem chega perto (Força CD 35) | defesa |
| 6º | **Exército de Ossos** | ergue 20 esqueletos (soldados comuns) por 1 dia | utilidade |
| 6º | **Prender a Alma** | a alma de quem morreu há até 1 hora fica presa num osso ou pedra (não vai embora, não ressuscita sem o conjurador) | utilidade |
| 6º | **Toque do Ceifador** | 24d6; se cair a 0, levanta como servo do conjurador | ataque |
| 7º | **Cemitério Acorda** | todos os mortos de um cemitério levantam e obedecem por 1 noite. Componente: terra do túmulo mais velho | utilidade |
| 7º | **Filactério** | guarda a vida do conjurador num objeto: se ele morrer, volta em 1d6 dias perto dele. Componente: um núcleo de Osso Raro e o osso do próprio conjurador | defesa |
| 8º | **Dragão de Ossos** | ergue uma fera morta Épica ou Única como servo por 1 dia. Componente: o crânio dela | utilidade |
| 8º | **Palavra de Morte** | um alvo de nível abaixo do conjurador ÷ 2 morre (Vontade CD 55); os outros levam 80d6 | ataque |
| 9º | **A Noite dos Mortos** | todos os mortos num raio de 10 km levantam e obedecem por 7 noites. PREÇO: o conjurador morre um pouco: não sara mais por magia de Luz, e todo vivo sente o frio dele (−5 em Carisma, para sempre) | utilidade |

## VAZIO (Von)

| Círculo | Feitiço | Efeito | Tipo |
| --- | --- | --- | --- |
| 1º | **Calar** | um som ou uma runa de 1º círculo some | utilidade |
| 1º | **Sentir Magia** | vê magia ativa a 18 m (círculo e escola) | utilidade |
| 2º | **Bolso Vazio** | guarda um objeto de até 5 kg num lugar que não existe (1 dia) | utilidade |
| 2º | **Mão Vazia** | desarma um alvo: a arma cai (Força CD 20) | ataque |
| 3º | **Desfazer** | apaga um feitiço de até 3º círculo | defesa |
| 3º | **Peso do Nada** | um alvo fica sem peso ou com peso dobrado por 3 rodadas | utilidade |
| 4º | **Sono do Ferro** | no toque, apaga uma magia ou um encantamento por 1 cena | defesa |
| 4º | **Selo de Silêncio** | anula magia numa área de 9 m por 1 cena | defesa |
| 5º | **Apagar** | apaga um feitiço de até 6º círculo ou um encantamento por 1 dia | defesa |
| 5º | **Lugar Nenhum** | o conjurador e 3 aliados somem para um lugar que não existe por até 1 hora (tempo passa igual fora) | defesa |
| 5º | **Rasgo** | 20d6 num alvo; feitiço ativo nele cai | ataque |
| 6º | **Campo Morto** | nenhuma magia funciona num raio de 30 m por 1 cena, nem a do conjurador | defesa |
| 6º | **Porta do Nada** | uma porta para qualquer lugar que o conjurador já viu, aberta por 1 minuto | utilidade |
| 6º | **Esquecer** | o alvo esquece a última hora (Vontade CD 45) | ataque |
| 7º | **Desfazer o Encanto** | destrói um encantamento ou uma peça mágica até Lendária (Vontade da peça CD 55). Componente: um caco de vaduar | ataque |
| 7º | **Bolso do Mundo** | guarda uma casa inteira num lugar que não existe, por um ano. Componente: uma chave quebrada | utilidade |
| 8º | **Silêncio de Região** | nenhuma magia funciona numa região de 1 km por 1 dia. Componente: 1 kg de vaduar, que se perde | defesa |
| 8º | **Apagar o Nome** | o mundo esquece um nome: quem o tinha não é lembrado por ninguém (Vontade CD 55). Componente: o nome escrito por quem o deu | ataque |
| 9º | **O Buraco no Mundo** | um raio de 1 km deixa de existir por um instante e volta vazio. PREÇO: o conjurador perde uma lembrança inteira (o Mestre escolhe a mais querida) e a magia em volta dele morre por um ano | ataque |

## ELO (Afi)

| Círculo | Feitiço | Efeito | Tipo |
| --- | --- | --- | --- |
| 1º | **Nó de Chamada** | a peça volta à mão do dono a até 30 m | utilidade |
| 1º | **Marca de Dono** | marca um objeto: sabe onde está a até 10 km por um mês | utilidade |
| 2º | **Fio de Elo** | prende um alvo a 9 m (Vontade CD 20) | ataque |
| 2º | **Elo de Guarda** | sabe quando o objeto ou a pessoa ligada é tocada, a até 1 km | utilidade |
| 3º | **Corrente de Ferro** | prende até 3 alvos a 9 m por 2 rodadas | ataque |
| 3º | **Partilhar a Dor** | metade do dano que um aliado levaria vem para o portador | defesa |
| 4º | **Elo de Juramento** | dois juram e o mundo cobra a quebra | utilidade |
| 4º | **Corrente Viva** | correntes de luz prendem até 6 alvos a 18 m por 3 rodadas (Força CD 30) | ataque |
| 5º | **Corrente Mestre** | torna um contrato escrito um contrato mágico: quebrar custa o que estiver escrito | utilidade |
| 5º | **Elo de Guerra** | até 10 aliados ligados por 1 cena: dano dividido entre todos, e todos sabem onde os outros estão | defesa |
| 5º | **Puxar** | arranca um alvo a até 60 m para junto do conjurador (Força CD 40) | ataque |
| 6º | **Laço de Servo** | um monstro de nível abaixo do conjurador obedece por 1 dia (Vontade CD 45) | ataque |
| 6º | **Âncora** | ninguém se teletransporta, some ou foge por magia num raio de 100 m por 1 cena | defesa |
| 6º | **Romper Laço** | quebra um laço mágico, juramento ou maldição de Elo de até 6º | utilidade |
| 7º | **Juramento de Cidade** | todos de uma cidade que juram ficam presos ao juramento por um ano. Componente: o selo da cidade | utilidade |
| 7º | **Corrente do Mundo** | prende um Lendário por 3 rodadas (Força ou Vontade CD 60). Componente: uma corrente de therk ou veyine | ataque |
| 8º | **Elo de Almas** | duas almas ligadas para sempre: sentem e sabem um do outro, e quando um morre o outro escolhe ir junto. Componente: dois anéis da mesma pepita | utilidade |
| 8º | **Domar** | um monstro Épico ou Único vira servo por um ano (Vontade CD 60). Componente: o nome dele | ataque |
| 9º | **O Fio do Tecelão** | reata ou corta um laço do mundo (uma linhagem, um pacto antigo, a ligação de um povo a uma terra). PREÇO: o conjurador fica sem laço nenhum: todo Laço dele cai a 0 e não sobe mais | utilidade |

## TEMPO (Int)

| Círculo | Feitiço | Efeito | Tipo |
| --- | --- | --- | --- |
| 1º | **Instante** | +4 na Iniciativa ou rerrola um teste de Agilidade | defesa |
| 1º | **Saber a Hora** | sabe a hora exata e quanto falta para o sol nascer ou pôr; acorda quando quiser | utilidade |
| 2º | **Pressa** | uma ação a mais nesta rodada (1x por cena) | arma |
| 2º | **Envelhecer** | uma corda apodrece, um metal enferruja, uma comida estraga em segundos | utilidade |
| 3º | **Voltar um Passo** | desfaz o último golpe recebido (1x por dia) | defesa |
| 3º | **Ler o Ontem** | vê o que aconteceu num lugar há até 1 dia | utilidade |
| 4º | **Visão do Tempo** | vê uma hora à frente (1x por dia) | utilidade |
| 4º | **Lento** | até 3 alvos a 18 m ficam Lentos por 3 rodadas (meia ação; Vontade CD 30) | ataque |
| 5º | **Parar a Hora** | o conjurador age 2 rodadas sozinho enquanto o mundo para (1x por dia) | arma |
| 5º | **Ler o Ano** | vê o que aconteceu num lugar há até um ano | utilidade |
| 5º | **Envelhecer o Alvo** | 20d6 e o alvo envelhece 10 anos (Vontade CD 40) | ataque |
| 6º | **Desfazer o Dia** | desfaz o último minuto para todos a 9 m (1x por semana) | defesa |
| 6º | **Pressa de Tropa** | até 20 aliados ganham uma ação a mais por rodada por 1 cena | arma |
| 6º | **Guardar a Hora** | um objeto ou corpo não envelhece nem apodrece por cem anos | utilidade |
| 7º | **Ver o Mês** | vê um mês à frente, em pedaços (3 cenas). Componente: areia de uma ampulheta que parou | utilidade |
| 7º | **Prender no Tempo** | um alvo fica parado no tempo por 1 dia (Vontade CD 55). Componente: um núcleo de Tempo Raro | ataque |
| 8º | **Voltar Atrás** | desfaz a última hora para uma cidade inteira (1x na vida do conjurador). Componente: um núcleo de Tempo Épico | defesa |
| 8º | **Juventude** | o alvo volta 20 anos (sem perder o que aprendeu). Componente: um dente de leite dele | cura |
| 9º | **Desfazer um Dia do Mundo** | um dia inteiro não aconteceu, para todo o mundo. PREÇO: o conjurador envelhece 30 anos e só ele lembra do dia que não houve | defesa |

## MENTE (Von)

| Círculo | Feitiço | Efeito | Tipo |
| --- | --- | --- | --- |
| 1º | **Sussurro** | mensagem de 20 palavras a quem conhece, a 10 km | utilidade |
| 1º | **Distrair** | um alvo perde a Reação nesta rodada (Vontade) | ataque |
| 2º | **Detectar Mentira** | sabe se uma frase é mentira | utilidade |
| 2º | **Calma** | tira medo e raiva de até 4 aliados | defesa |
| 3º | **Sono** | até 3 alvos dormem (Vontade) | ataque |
| 3º | **Ler a Superfície** | ouve o que o alvo pensa agora | utilidade |
| 4º | **Comando** | o alvo obedece uma ordem de uma palavra (Vontade CD 25) | ataque |
| 4º | **Medo em Massa** | todos os inimigos a 18 m fogem por 1d4 rodadas (Vontade CD 30) | ataque |
| 5º | **Dominar** | controla um alvo por 1 cena (Vontade CD 40 a cada 3 rodadas) | ataque |
| 5º | **Elo de Mente** | até 6 aliados falam pela mente a até 10 km por 1 dia | utilidade |
| 5º | **Golpe na Mente** | 20d6 de dano mental e Atordoado 1 rodada | ataque |
| 6º | **Apagar Lembrança** | apaga ou muda uma lembrança de até um dia (Vontade CD 45) | utilidade |
| 6º | **Multidão Mansa** | uma multidão de até 1.000 se acalma e escuta (Vontade CD 45) | utilidade |
| 6º | **Muralha da Mente** | até 10 aliados imunes a medo, sono, comando e leitura por 1 dia | defesa |
| 7º | **Exército Sonha** | uma tropa de até 1.000 dorme (Vontade CD 55). Componente: papoula colhida num campo de batalha | ataque |
| 7º | **Ler a Alma** | sabe tudo o que um alvo sabe sobre um assunto (Vontade CD 55). Componente: um objeto que ele carregou por um ano | utilidade |
| 8º | **Mudar o Coração** | muda uma lealdade ou um amor de um alvo, para sempre (Vontade CD 60). Componente: uma lágrima dele | ataque |
| 8º | **Loucura** | 80d6 de dano mental; quem cai a 0 enlouquece em vez de morrer | ataque |
| 9º | **A Voz em Todas as Cabeças** | uma ordem de cinco palavras ouvida e obedecida por todos num raio de 10 km. PREÇO: o conjurador não se lembra mais do próprio nome, e quem o conhecia também esquece um pouco | ataque |

## TÉCNICAS DE AURA (guerreiros, casa, Dia 200)

Um guerreiro sem Magia usa uma técnica de aura: Luta Treinado dá 1, Mestre dá 2 e Lendário dá 3. São do 1º ou 2º círculo, custam Estamina igual ao círculo e valem 1x por cena.

- Pele de Pedra (Pedra 2º): +4 de Defesa por 3 rodadas
- Raiz de Pedra menor (Pedra): não é derrubado por 1 rodada
- Passo de Vento (Vento 1º)
- Sangue Quente (Sangue 1º, sem custo de PV na aura)
- Fôlego de Ferro (Sangue 2º): ignora Exausto por 1 cena
- Mão de Pedra (Pedra 1º)
- Instante (Tempo 1º)
- Calma (Mente 2º): tira medo dos que estão a 6 m
- Luz no Escudo (Luz 1º): cega 1 rodada quem bate no escudo com 19-20
- Nó de Chamada (Elo 1º): a arma volta à mão
