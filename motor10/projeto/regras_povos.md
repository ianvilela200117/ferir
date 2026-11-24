# OS POVOS DO PERSONAGEM (etapa 4b)

> **RASCUNHO DO CONSTRUTOR (a frente P, os povos).** Capítulo para o `REGRAS.md` (o número 19 é provisório: quem monta o livro o acerta). Os números moram no `tabelas_povos.py`; a regra, no `povos.py` (e no núcleo, que lê a página direto: o gravador, o lutador, o talento, a luta); as provas, no `provas_povos.py` (o `provas_mundo.py` o roda).

## 19. Os povos

19.1 **Seis povos: o humano, o anão, o elfo, o meio-orc, o pequenino e o gnomo.** O humano é a medida de todos: é a pessoa de antes desta etapa, sem tirar nem pôr. Os outros mexem nos atributos **com a soma igual** (o que ganham num, perdem noutro), têm de nenhum a dois traços, uma coragem, um corpo, uma tendência nos talentos, a vida longa e um +2 num teste do ladino. **A lei:** nenhum povo pesa mais que o Grande Dom, em condição nenhuma; a peça uma categoria acima segue vencendo. Quem não tem o povo escrito é humano (o save antigo, a gente de hoje). **O povo não se troca depois de nascer.** Ficam de fora: o meio-elfo, os povos das criaturas como personagem (o goblin, o orc) e todo povo de jogo ou livro.

19.2 **Os números de cada povo.**

| Povo | Força | Agilidade | Vigor | Vontade | Percepção | Afinidade | Traços | Coragem | Corpo |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **humano** | 0 | 0 | 0 | 0 | 0 | 0 | | 0 | gente |
| **anão** | 0 | −5 | +2 | +5 | −2 | 0 | vê no escuro, resiste a veneno | 0 | gente |
| **elfo** | −10 | +10 | −3 | −10 | +8 | +5 | vê no escuro | 0 | gente |
| **meio-orc** | +5 | 0 | 0 | 0 | 0 | −5 | vê no escuro | 0 | gente |
| **pequenino** | −15 | +5 | +3 | +5 | +2 | 0 | | +4 | miúdo |
| **gnomo** | −10 | 0 | 0 | −5 | +5 | +10 | vê no escuro | 0 | miúdo |

**A soma de cada linha é zero.** Quem nasce tem os atributos do começo (ou do molde) mais os do povo, e são esses que ficam gravados: o povo não soma de novo em conta nenhuma. A frase que o jogador lê está no `povos.py ver POVO`:

| Povo | A frase |
| --- | --- |
| humano | a medida de todos: nada a mais, nada a menos |
| anão | duro, teimoso e de vista curta; vê na penumbra das minas, e o veneno o pega pela metade |
| elfo | leve e de olho longo, frágil de corpo e de pouca paciência; vê na penumbra |
| meio-orc | forte e de sangue quente; vê na penumbra, como o pai orc |
| pequenino | miúdo, rijo e sem medo: o pavor pega pouco nele, e anda sem ser ouvido |
| gnomo | miúdo, curioso e de mão fina; vê na penumbra, e o mecanismo não tem segredo para ele |

19.3 **Os traços do povo** (uma lista fechada, à parte dos traços dos bichos e da magia: não ligam a luta de magia).
- **Vê no escuro.** Na luta, de perto, o escuro pesa só a metade: −2 no golpe, e não −4. **No tiro e no feitiço que voa, o escuro pesa inteiro**, como em todos (−8): vê-se o vulto de perto, não o alvo de longe. Fora da luta, anda, procura, abre e desarma sem luz (a regra da masmorra, capítulo 17); o grupo em que todos veem no escuro dispensa a tocha. Com a tocha acesa ninguém tem o escuro, e o traço não soma nada.
- **Resiste a veneno.** O veneno que entra (do bicho, da criatura, da lâmina) tira por rodada a metade do que tiraria.
- **A coragem** (um número, não um traço): soma no teste de coragem, como a do povo das criaturas. O pequenino tem +4. Só aparece diante do que apavora (o dragão, a hidra, a alma penada) e dos sustos da luta.

O nome do povo não vai à luta: o lutador leva só os traços e a coragem. **Na luta, o corpo miúdo é do tamanho de gente:** uma vaga no corredor, quatro batem nele, o PV de gente (o tamanho pequeno dos bichos, posto em gente, venceria o gêmeo só 30% das vezes: seria castigo, não traço).

19.4 **O corpo e a armadura.** A armadura é feita para um corpo, o **talhe**: a de gente (sem marca) ou a miúda (do pequenino e do gnomo). **A armadura de outro corpo não serve até ser ajustada:** vestir é recusado com a frase "A armadura de malha Comum é de gente grande: não serve no corpo de Pipa. Um ferreiro a ajusta (`oficio.py ajustar ITEM para=ID`)." O ajuste de hoje resolve (1 bloco e o teste de sempre: o Bento, Treinado, ajusta uma peça Comum contra 22): o ajuste que acerta **recorta a peça para o corpo de quem a pede**, para os dois lados (a de gente vira miúda; a miúda vira de gente). **A arma e o escudo não têm corpo:** o requisito de Força já cobra (o pequenino paga com a espada e mais com o malho; a adaga e o arco pedem Agilidade). As peças do começo do personagem miúdo já nascem miúdas.

19.5 **A tendência nos talentos.** Cada povo tem um caminho a favor e um contra. No caminho a favor o dado do talento rola duas vezes e vale o melhor; no contra, duas vezes e vale o pior. A inclinação do personagem que cai no caminho a favor soma mais um dado (melhor de três); no contra, os dois se anulam. Os outros caminhos rolam como hoje, com a mesma chave do dado do mundo: **o humano nasce igual ao de hoje, caminho por caminho.**

| Povo | A favor | Contra |
| --- | --- | --- |
| anão | a forja | o verde |
| elfo | o arco e a besta | as armas de peso |
| meio-orc | as armas de peso | o encanto |
| pequenino | a manha | as armas de haste |
| gnomo | o encanto | as armas de peso |

| | Negado | Lerdo | Comum | Jeitoso | Prodígio | Jeitoso ou melhor |
| --- | --- | --- | --- | --- | --- | --- |
| como hoje (uma vez) | 2% | 10% | 76% | 10% | 2% | 12% |
| a favor (melhor de dois) | 0,04% | 1,4% | 76,0% | 18,6% | 3,96% | **22,6%** |
| a favor e a inclinação (melhor de três) | 0% | 0,2% | 68,0% | 26,0% | 5,9% | 31,9% |
| contra (pior de dois) | 3,96% | **18,6%** | 76,0% | 1,4% | 0,04% | 1,4% |

Na média, a favor vale um quarto de grau de talento: é pressa e teto, nunca poder.

19.6 **A vida longa.** Nesta etapa **a idade só se escreve:** quem nasce agora (o personagem) tem a idade de adulto do povo mais um d10 (o dado do mundo); o save antigo fica sem idade (não se sabe). O ano que passa, a velhice e a morte de velho são da etapa 7. Ninguém vivo passa do máximo do povo (o gravador recusa, o `valida` acusa).

| Povo | Adulto aos | Velho aos | Vive até |
| --- | --- | --- | --- |
| humano | 16 | 60 | 90 |
| anão | 30 | 200 | 300 |
| elfo | 80 | 500 | 800 |
| meio-orc | 14 | 50 | 75 |
| pequenino | 25 | 80 | 130 |
| gnomo | 35 | 250 | 400 |

19.7 **O povo no ofício do ladino** (capítulo 18). O povo soma +2 num teste da manha, e nunca mais que +2 num teste (o mesmo teto do Grande Dom). O humano não soma nada.

| Povo | +2 em |
| --- | --- |
| anão | achar a armadilha e a passagem na pedra (a cripta, a mina, a ruína) |
| elfo | achar a armadilha e a passagem escondida |
| meio-orc | arrombar |
| pequenino | andar escondido |
| gnomo | abrir fechadura e desarmar armadilha |

19.8 **A gente do mundo.** Cada lugar pode dizer de que povos é a gente dele (`povos`: a fração de cada povo, somando até 1; sem o campo, toda humana); cada pessoa com nome guarda o dela. A proposta para o gerador da região (etapa 7; aqui é chute, na página: `tabelas_povos.GENTE`): a capital 80 humanos em 100 (6 anões, 5 pequeninos, 4 meio-orcs, 3 elfos, 2 gnomos); a cidade da serra 65 anões; a vila da floresta funda 65 elfos; as tocas da colina 60 gnomos; a aldeia da fronteira dos orcs 25 meio-orcs; a vila do campo 14 pequeninos; os 40 rivais (etapa 5) 70 humanos. A loja de cada lugar põe na prateleira as armaduras dos corpos da gente dele, na proporção (etapa 7).

19.9 **O personagem escolhe o povo ao nascer**, junto com a inclinação: `python3 vila_teste.py PASTA povo=anão` (a vila nova; o comando é do integrador). Nasce com os atributos do começo mais os do povo, os traços, a idade de adulto do povo mais um d10, a tendência e, se o corpo é miúdo, as peças do começo miúdas. **A segunda inclinação é só do personagem humano** (capítulo 10). **O Maro segue humano:** o save não tem o campo, e o comando que acrescenta a etapa não toca nele.

19.10 **A vila de teste ganha a gente de outros povos** (`povos.na_vila`, parte do `vila_teste.py fantasia`; só por eventos do gerador, sem recriar nada; recusa entrar duas vezes):
- **Durva**, anã, ferreira de passagem (nível 34; forja e martelo Treinados; martelo e armadura de couro Incomuns; 40 de prata; 112 anos). Vai junto se a chamam, como Tomé, e vê no escuro.
- **Brasco**, meio-orc, guarda de caravana de passagem (nível 26; malho Treinado; malho e malha Comuns; 30 de prata; 31 anos). Passou por Vau Seco e viu o que o dragão deixou (capítulo 20).
- **Ilvena**, elfa, caçadora de passagem (nível 38; arco e caça Treinados; arco Incomum, adaga Comum, couro Incomum; 25 de prata; 240 anos).
- **Nena Ramalho**, pequenina, faz o pão da pousada e mora na vila (nível 9; coleta Iniciante; 12 de prata; 44 anos).
- **Pedra Rasa ganha a sua gente:** em cada 100, 88 humanos, 8 pequeninos, 2 anões e 2 meio-orcs.
- **Na prateleira:** uma armadura de couro miúda, uma de malha miúda e um elmo miúdo de malha, todos Comuns.

Os talentos e os dons dessa gente saem pelo dado do mundo, com a tendência do povo (ninguém sabe o que tem). A prata que nasce: a das quatro pessoas (107).

19.11 **A mesa.** No **Você**, quem é de outro povo ganha uma linha ("Do povo dos pequeninos, 27 anos: corpo miúdo (a armadura de gente grande não serve até um ferreiro ajustar); coragem +4 diante do que apavora; +2 em andar escondido."); o humano de hoje não ganha linha nenhuma (a MESA dele sai igual), e o humano que nasceu com a idade escrita ganha só "Do povo dos humanos, 22 anos: a medida de todos." Em **Quem está aqui**, a gente de outro povo diz o povo no começo do que ela é ("Durva (anã, ferreira de passagem; ...)"); e, como essa lista corta em 12 nomes, uma linha à parte diz todos os de outro povo que estão ali ("De outros povos, aqui: Durva (anã), Brasco (meio-orc), Ilvena (elfa), Nena Ramalho (pequenina)."; quem não diz o povo no começo do que é aparece como "Quim (do povo dos pequeninos)"). Sem ninguém de outro povo por perto, a linha não aparece. O povo não tem segredo: nada vai ao SÓ O MESTRE.

19.12 **Os comandos.**
```
python3 povos.py lista              os povos, para o jogador escolher
python3 povos.py ver POVO           os atributos, os traços, a coragem, o corpo, a tendência, a vida, o teste do ladino
```

19.13 **As metas** (o banco: `python3 provas_povos.py [N]`, com 4 × N lutas por linha, de semente fixa; a meta pede 4.000: `provas_povos.py 1000`). Os números das duas rodadas: 4.000 lutas por linha (a meta) e 1.200 (o padrão do `provas_mundo.py`):

| Meta | O que se mede | Faixa | Deu |
| --- | --- | --- | --- |
| CO1 | a pessoa comum: a MESA, o lutador e a ficha com e sem o módulo dos povos | igual | igual |
| CO2 | as cinco lutas de semente fixa, com a gente feita pelo caminho dos povos | número por número | iguais |
| CO3 | o humano que nasce pelo povos.nasce: atributos, talentos e dons | iguais aos de hoje | 22 nascimentos, todos iguais |
| CO4 | o save numa cópia: abre, o Maro é humano; a gente nova só se acrescenta | campo por campo; recusa duas vezes | sim |
| PO1a | cada povo contra o humano de peças iguais: espada, adaga e arco de dia; espada e adaga no escuro; nível 5 e 50 | de 40 a 60% | 4.000: de 43,2 a 56,7% (o Grande Dom contra o gêmeo, 59,8%) · 1.200: de 42,8 a 58,0% (o Grande Dom, 58,6%) |
| PO1b | o arco de noite: o arqueiro que vê no escuro contra o humano | de 40 a 60% | **falha até o luta.py ler o ESCURO_TIRO**: com a metade do escuro no tiro, de 63,5 a 66,3% (4.000); com o tiro inteiro (medido por embrulho, 4.000 lutas), de 47,8 a 53,1% |
| PO2 | cada povo contra o humano com a arma uma acima | até 15% | 4.000: de 4,2 a 5,5% · 1.200: de 3,4 a 5,8% |
| PO3 | o anão contra a aranha-de-toca | até o Grande Dom mais 2 | 4.000: 83,2% contra 83,6% (o humano, 80,1%) · 1.200: 82,5% contra 84,4% |
| PO4 | a soma dos atributos, todos os começos e moldes | a do humano | sempre (186 nascimentos) |
| PO5 | a tendência, 20.000 nascimentos por povo | a favor 20 a 25%; contra 20 a 25%; o resto como hoje | de 21,9 a 23,0%; os outros caminhos sem diferença |
| PO6 | o corpo: a recusa, o ajuste, a arma e o escudo | sempre | sim |
| PO7 | o pequenino de nível 50 diante do que apavora | foge até 6% | a conta: 3,75% (o humano, 13,75%); medido, 3,2% |
| PO8 | a idade: ninguém passa do povo; o personagem nasce adulto | sempre | sim |

19.14 **O que mudou do projeto, e por quê.** O projeto mediu os povos com o traço emulado; construído, o banco achou:
1. **O atributo pesa aos degraus de 10** (o golpe, a Defesa, a iniciativa, o fôlego); só o Vigor pesa ponto a ponto (o PV). O Vigor é a alavanca: 5 pontos valem de 3 a 4 no duelo.
2. **O anão e o meio-orc passavam rente aos 60% no escuro** (59,2 e 58,8, com Vigor +5): o anão ficou com Vigor +2 (e Percepção −2), o meio-orc com Força +5 e Afinidade −5 (sem Vigor).
3. **O gnomo caía a 39% no nível 5** (abaixo dos 40, com Vigor −5): ficou sem perder Vigor (Vontade −5 no lugar). O elfo ficou com Vigor −3 e Percepção +8; o pequenino, com Vigor +3, Percepção +2 e Vontade +5 (o nível 5 dele estava rente, a 42%; a Vontade +5 mantém a fuga diante do dragão em 3,75%).
4. **O arco no escuro:** com a metade do escuro também no tiro, o arqueiro que vê no escuro vencia o arqueiro humano de noite de 63 a 67% (passa do Grande Dom; o projeto não tinha medido esta linha). O juízo da etapa deu ao golpe a metade, e ela fica; **no tiro e no feitiço que voa, o escuro pesa inteiro** (`ESCURO_TIRO = 1,0`, a página). O `luta.py` e o `magia.py` são do núcleo: o integrador liga o número (pedido), e até lá a meta PO1b falha às claras.

19.15 **O que fica de fora** (dito): o meio-elfo; o personagem de povo das criaturas; a opinião e o preconceito entre povos (a memória da gente é da etapa 3); o ano que passa e a velhice (etapa 7); a loja que põe na prateleira as armaduras pela gente do lugar (etapa 7; a vila de teste ganha as três miúdas à mão); a loja farta conta a armadura miúda e a de gente como iguais (o feitio não olha o corpo: é pequeno, e fica dito); o herdeiro de outro povo (etapa 6: o herdeiro de um elfo pode ser um bisneto).
