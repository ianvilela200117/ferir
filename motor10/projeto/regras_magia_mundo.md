> **JUNTADO AO `REGRAS.md`** (capítulos 12 a 14) na integração da etapa da magia, com os acertos dela (o mau-olhado de −4, os chefes acertados, a loja que não compra peça maldita, o segredo fora do RETOMAR). O que vale é o `REGRAS.md`; este rascunho fica como registro.

# O MUNDO DA MAGIA: a bancada, as maldições e a magia fora da luta (etapa da magia)

> **RASCUNHO DO CONSTRUTOR (a frente do mundo).** Capítulos para o `REGRAS.md` (os números 12, 13 e 14 são provisórios: quem monta o livro os acerta). Os números moram no `tabelas_magia_mundo.py` (o preço dos bens novos, no `tabelas_mercado.py`); a regra, no `alquimia.py`, `encanto.py`, `maldicao.py`, `magia_mundo.py`, `oficio.py` e `mercado.py`; as provas, no `provas_magia.py` (o `provas_mundo.py` o roda).

## 12. A bancada da magia: a alquimia e o encanto

12.1 **Uma bancada só, quatro lugares.** A obra de vários dias é a da forja (capítulo 7): a matéria entra quando ela abre, os blocos somam de um dia para o outro, o ato para quando o corpo pede, e o teste sai uma vez, quando os blocos fecham. O que muda é a bancada e a mão:

| Ofício | A bancada (campo do lugar, 0 a 4) | O que faz | A escada da mão |
| --- | --- | --- | --- |
| forja, couro | `oficina` | arma, armadura, escudo | 50 · 150 · 375 · 1.000 blocos |
| alquimia | `botica` (panela, botica de vila, botica de cidade, laboratório, grande laboratório) | a leva de poção | a mesma |
| encanto | `runas` (pedra riscada, mesa de runas, oficina de runas, grande oficina, oficina mestra) | o foco, o amuleto, a gravação de um feitiço numa peça | a mesma |
| fé | `santuario` | o jornal do santuário (a prece, o voto e os ritos são do capítulo 14) | a das armas |

O teste é sempre o da forja: **2d20 + a maestria do ofício + Afinidade ÷ 10 + a bancada + o preparo, contra 28 + 6 por categoria.** O preparo são quatro, de +2 cada, até +8, cada um com alcance (a categoria mais alta a que serve): na alquimia, a receita, o ajudante, o fogo e a vidraria; no encanto, a receita, o ajudante, a tinta e a pedra. O DOM do ofício entra dentro do teto de +8 (capítulo 10). Sem a bancada no lugar, a obra não abre.

12.2 **A leva.** Rende 2 doses do Comum ao Raro (bens, na carga: `cura:0`) e 6 elixires do Épico para cima (itens do Livro de Itens, contados no mundo; a leva pede matéria Rara e um NÚCLEO da categoria: um núcleo Épico vira seis elixires ou uma espada). Blocos pesados: 1, 3, 9, 27, 81, 243. Falhar por 1 a 4: sai uma categoria abaixo (a Comum sai aguada: 1 dose). Por 5 ou mais: a matéria some, e o núcleo também. De Mestre para cima a mão pede o feito: uma leva Épica nascida (Mestre), uma Única (Lendário).

12.3 **As nove receitas.** A matéria vai na categoria da leva. Toda receita custa 8 de preço de base na Comum (vezes 6 por categoria), dois terços do que valem as 2 doses: comprada na loja e vendida à loja, a leva não paga a matéria.

| Poção | Matéria da leva | O que faz (fora da luta) |
| --- | --- | --- |
| cura | 4 de erva | devolve 1d8 × 6 × 3^(categoria da poção − categoria da ferida mais funda) de PV |
| antídoto | 3 de erva, 2 de osso | tira o veneno até a categoria dele (só serve na luta) |
| veneno de lâmina | 4 de peçonha (até o Raro) | passa-se na arma: a primeira ferida que ela abrir envenena (1 dose = 1 golpe); é crime nas vilas |
| Mana | 4 de erva | devolve 4 de Mana por degrau (Comum 4, Incomum 8, Raro 12) |
| guarda | 2 de osso, 3 de erva | por 1 bloco, conta como amuleto da categoria dela |
| fúria | 3 de erva, 2 de osso | +2 no acerto e −2 na Defesa por 5 rodadas (só serve na luta) |
| vigília | 4 de erva | tira 3 de sono e 2 de cansaço (uma por dia) |
| quebra-maldição | 2 de água benta, 3 de erva, 2 de osso | quebra a maldição de categoria menor; recua 2 passos a da mesma; segura 1 dia a maior |
| remédio | 3 de erva Comum (rende 1) | o bem que já existia: é o que gasta quem trata a ferida (capítulo 14) |

A **peçonha** é despojo novo do bicho de veneno (da categoria dele até a Rara); a **água benta**, o clérigo benze (capítulo 14).

12.4 **Beber fora da luta** (`alquimia.py beber cura:0 [alvo=ID]`; na luta é a ordem `beber`). Não gasta bloco. **Vigor ÷ 30 doses por dia, no mínimo 1**; cada uma além disso pede Vigor contra 24 + 4 por dose a mais: falhou, a poção se gasta, não faz nada, e a pessoa enjoa (−2 em tudo por 1 bloco). **A cura tem teto:** por pessoa e por dia, feitiço e poção somados nunca devolvem mais que metade do PV máximo. **A ferida mais funda** (`funda`) é a maior categoria que feriu a pessoa desde que ela esteve inteira; apaga quando o PV enche. Por isso a poção barata não serve em luta cara: a da categoria da ferida desfaz cerca de um golpe; uma abaixo, um terço disso. Dá-se de beber a quem está junto. O antídoto e a fúria fora da luta não fazem nada (recusa, antes de gastar).

12.5 **O veneno de lâmina** (`alquimia.py lamina [ARMA]`): uma dose na arma de corte ou de ponta; seca em um dia; numa lâmina de categoria maior que a dose, um terço por degrau. É crime nas vilas: a loja não o compra nem o vende (quem vende é a bruxa, de pessoa a pessoa).

12.6 **O foco e o amuleto** se fazem no encanto, na mesa de runas, como a forja faz a adaga: a varinha (2 de madeira, 1 de osso), o cajado (4 e 1), o símbolo (3 de metal), o talismã (2 de osso, 1 de couro), o amuleto (1 de osso); do Épico para cima, matéria Rara e um núcleo. Blocos, teste e falha da forja. Consertam-se na mesa de runas (a mão de encanto, ou pago). Valem pela matéria que levam: o amuleto Comum, 10 de prata; a varinha, 30; o cajado, 50.

12.7 **Gravar um feitiço numa peça** (`encanto.py gravar ITEM FEITICO [para=DONO] [com=QUEM_SABE]`). A arma, a armadura ou o escudo (o foco e o amuleto já são magia). Quem grava sabe o feitiço, ou tem ao lado quem sabe; o encanto leva o grau de quem sabe (Iniciante 1 a Lendário 4). A **essência** da categoria da peça: até o Raro, 4 de osso e 2 de erva; do Épico para cima, um núcleo. Um terço dos blocos da forja (Comum e Incomum 1, Raro 3, Épico 9, Único 27, Lendário 81). O teste da forja contra 28 + 6 por categoria da peça. Falhou por 1 a 4: grava um grau abaixo. Por 5 ou mais: a essência some e a peça perde 5 de durabilidade. **Por 10 ou mais, a peça sai MALDITA**, e é de onde vêm as peças malditas do mundo: quem a puser em uso pega a maldição, que só quebra devolvendo a peça à mesa de runas onde se gravou. Um encanto por peça; dois do Único para cima. Na luta (frente da luta): o dono solta o feitiço uma vez, a peça vale foco um degrau abaixo, e volta a carregar 1 bloco depois.

12.8 **O jornal** da botica, da mesa de runas e do santuário paga o salário da mão (Iniciante: aprendiz; Treinado: oficial; Mestre: mestre), **dentro da mesma jornada de 2 blocos pagos por dia** que vale para o trabalhar e para o jornal da forja. Serviço de magia rende o que rende a forja: nenhuma renda nova.

## 13. As maldições

13.1 **O que é.** Um registro na pessoa: nome, categoria, **tipo** (míngua, chaga, azar, insônia, marca: o sinal que ela sente), **um relógio de 6 passos**, a **origem** (feitiço, bicho, lugar, peça, juramento), quem a rogou e a **condição** que a quebra. Não é estado de luta: é coisa de dias. É a única coisa desta etapa que mata fora da luta sem ser fome.

13.2 **O relógio.** Na virada de cada dia o mundo rola (o dado do mundo, oculto): **2d20 + a força da maldição contra a Firmeza do amaldiçoado.** A força é 2 + 4 por categoria (Comum 2, Incomum 6, Rara 10, Épica 14). A Firmeza é a da base comum (22, metade do bônus de Vontade, metade da maior maestria, metade do dom de tradição, e o bônus do amuleto; sem amuleto, metade do da armadura do tronco). Venceu, anda um passo.

| Passo | Nome | O que faz |
| --- | --- | --- |
| 1 | a marca | nada em número |
| 2 | o peso | −1 em todo teste |
| 3 | a míngua | −2; a noite dormida não devolve PV |
| 4 | a chaga | −2; as feridas não saram; a Mana não volta fora da luta |
| 5 | o fim à vista | −4; cada virada tira 10% do PV máximo |
| 6 | a morte | morre na virada, com a causa escrita |

Das penas de maldição vale a pior; ela soma com a pena do corpo, em todo teste e na luta. **Quanto tempo dá** (medido, metade das vidas, ninguém fazendo nada): o guerreiro de amuleto Raro, maldição Rara (a categoria da guarda), 15 dias; o mesmo sem amuleto, 9; o aldeão sem amuleto, maldição Comum, 10. Nenhuma mata antes de 5 dias. O amuleto compra tempo; não cura. **O relógio anda para toda gente amaldiçoada**, o personagem ou não: o mundo não gira em torno dele.

13.3 **De onde vem.**
- **A peça maldita**, ao ser posta em uso: a maldição pega no passo 1 (a pessoa só sente um frio no braço), e **a mão não larga a peça** (não sai de uso, não se vende, não muda de mão) enquanto ela durar. Ela parece uma peça comum: só quem a lê sabe.
- **O lugar maldito**: a cada bloco passado nele, o mundo rola a força dele contra a Firmeza de quem está; pegou, quebra quando a pessoa passa 7 dias sem pôr o pé lá.
- **O feitiço**: a praga da bruxa (capítulo 14).
- **O bicho que amaldiçoa**: a ferida que ele abre (a luta e as criaturas).
- **O juramento quebrado**: o voto do clérigo, a dívida da bruxa (capítulo 14).

13.4 **Como se quebra.**
1. **Cumprir a condição:** devolver a peça ao lugar dela (`maldicao.py devolver ITEM`, estando lá: a peça fica no chão, ainda maldita); matar o bicho naquele ermo; o perdão de quem rogou (`maldicao.py perdoa`), ou a morte dela; os 7 dias longe do lugar; a dívida zerada. O estado confere sozinho na virada (e o Mestre atesta o que ele não sabe conferir: cumprir o jurado, queimar o laço: `maldicao.py cumpre`).
2. **O rito do clérigo** (`maldicao.py rito ALVO quem=CLERIGO`): quem sabe quebrar-maldição (e não quebrou o voto), 1 bloco, 6 de Mana, uma tentativa por dia. **2d20 + Conjuração da fé contra 28 + a força + 2 por passo além do primeiro:** quem chega cedo se salva. Falhou por 5 ou mais: o clérigo leva a marca (a mesma maldição, no passo 1). Quem é ajudado paga, de pessoa a pessoa, um terço do preço de tabela da categoria (10, 60, 360, 2.160 de prata). O clérigo Mestre de símbolo Raro, na maldição Rara: 57% no passo 1, 48% no passo 2, 40% no 3.
3. **A poção quebra-maldição** só ganha tempo: a de categoria maior quebra; a da mesma faz recuar 2 passos; a menor segura 1 dia.
4. **O que não quebra:** dormir, comer, curar o PV, mudar de lugar (salvo a do lugar).

13.5 **O que a mesa mostra**, em três degraus de saber:
- **não sabe** (passo 1): nada;
- **desconfia** (do passo 2): "ALGO ESTÁ ERRADO: Maro acorda mais fraco do que deitou, e isto não é doença. Pesa: −2 em todo teste; a noite não devolve PV." Sem nome, sem categoria, sem prazo;
- **sabe** (alguém leu: capítulo 14): "MALDIÇÃO: a Mão Fria (Incomum, míngua), passo 3 de 6 (a míngua): −2 em todo teste; a noite não devolve PV. Desde o Dia 12. Veio da peça Adaga do Túmulo. Quebra: devolver Adaga do Túmulo ao lugar dela, na Capela Caída; ou o rito de um clérigo (60 de prata)."

O SÓ O MESTRE vê tudo de todos (a força, a Firmeza, a chance de andar amanhã, a condição) e a rolagem oculta de cada virada do personagem. O RETOMAR leva as maldições que o personagem sente. **O `turno.py fecha` recusa** o turno com maldição do personagem no passo 4 ou mais sem uma pergunta aberta sobre ela.

## 14. A magia no mundo: estudar, as tradições, a Mana, os ritos e os serviços

14.1 **Qualquer um aprende magia**, como se aprende uma arma (`magia_mundo.py estudar FEITICO com=PESSOA|escrito=ITEM|santuario|ermo`). Um feitiço se estuda em blocos leves, vezes o talento na tradição dele: o truque 3, o grau 1 6, o grau 2 18, o grau 3 54, o grau 4 162. Os blocos de estudo são treino da tradição: a maestria sobe pela tabela das armas (40, 160, 500, 1.500; de Mestre para cima, com um feito). **A fonte:** quem saiba o feitiço e queira ensinar (cobra o salário do grau de ofício dele por bloco, e só ensina dentro da jornada dele: 2 blocos por dia); um escrito que o ensine (de graça); um santuário (os feitiços da fé, a quem tem voto); o ermo do laço (os do verde, a quem tem laço). Os seis de grau 1 de uma tradição somam 36 blocos: é quase o Iniciante.

14.2 **Uma tradição por pessoa.**

| Tradição | Como se entra | De onde vem a Mana fora da luta | O que custa |
| --- | --- | --- | --- |
| o mago (`arcano`) | estudando o primeiro feitiço | a regra geral (14.3) | o livro e as lições |
| o clérigo (`fé`) | o VOTO, num santuário (`magia_mundo.py voto lâmina\|pobreza\|socorro`) | só a PRECE: 1 bloco por dia; no santuário enche, fora dele volta a metade | quebrar o voto apaga a Mana e deixa uma marca (maldição de juramento, da categoria do santuário) |
| o druida (`verde`) | o LAÇO com um ermo vizinho (`magia_mundo.py laco ERMO`) | em dobro no ermo; a metade entre muros (cidade, masmorra) | a fartura do ermo do laço abaixo de 40% tira 2 da Conjuração; abaixo de 10%, 4 |
| a bruxa (`pacto`) | o PACTO, no escuro (madrugada ou noite): nasce devendo 1 | sozinha, só até a metade; o resto paga-se (`magia_mundo.py paga N pv\|divida`): 2% do PV máximo por ponto, ou 1 de dívida por 4 | a dívida sobe com o feitiço de grau 2 (+1), 3 (+2), 4 (+3) e a praga (a categoria mais 1); acima de Vontade ÷ 10, vira maldição nela (a Conta, que quebra quando a dívida zera) |

**Os votos:** da lâmina (não pôr em uso arma de corte nem de ponta: pôr é quebrar), da pobreza (na virada, a prata acima de 50 vai para o caixa do santuário), do socorro (não recusar cura pedida: a etapa 3). **A dívida** paga-se num rito de 1 bloco (`magia_mundo.py divida N pv|osso|erva`): 1 ponto a cada 5% do PV máximo, ou queimando 4 de osso ou de erva da categoria do foco.

14.3 **A Mana fora da luta**, por bloco: dormindo, um quarto da máxima; descansando, um oitavo; acordado e leve (ou parado), 1; no bloco pesado, nada. A tradição muda isto (14.2). A maldição do passo 4 não deixa a Mana voltar. A Mana máxima é (Afinidade + Vontade) ÷ 10 + a maestria da melhor tradição + o dom nela.

14.4 **Lançar fora da luta** (`magia_mundo.py lancar FEITICO [alvo=ID]`; não gasta bloco): a **cura** (1d8 × 6 × 3^(a categoria do foco − a ferida mais funda), dentro do teto do dia; o foco de outra tradição rende uma categoria abaixo, e sem foco, Comum), a **bênção** antes da luta (a luta que abrir até o fim do bloco seguinte leva o benzido), a **seiva** (a cura dos blocos dormidos do dia seguinte vale em dobro). O resto só muda número na luta. O feitiço custa a Mana da tabela; o de pacto de grau 2 para cima soma dívida.

14.5 **Os ritos** (1 bloco leve cada):
- **a prece** do clérigo (uma por dia);
- **ler** (`magia_mundo.py ler maldicao|dom|peca`): quem sabe o feitiço ler, ou a fé de Treinado para cima; 2 de Mana. Lê toda maldição de alguém (passa a saber tudo), o dom de alguém (ele se mostra), ou uma peça (se é maldita, que maldição e o que a quebra; e os encantos);
- **quebrar a maldição** (capítulo 13);
- **a praga** da bruxa, pelo toque (`magia_mundo.py praga ALVO [tipo=]`): 6 de Mana; 2d20 + Conjuração do pacto contra a Firmeza do alvo; pegou, uma maldição da categoria do foco dela, que quebra com o perdão ou a morte dela; a dívida sobe pegue ou não;
- **a água benta** (`magia_mundo.py agua N`, num santuário): cada uma, 1 de erva Comum e 2 de Mana; até 3 por rito;
- **benzer a arma** (`magia_mundo.py benzer ARMA`, num santuário): 2 de Mana; por 7 dias ela conta inteira contra o que não tem corpo.

14.6 **Tratar a ferida** (`magia_mundo.py tratar PACIENTE`): o ofício `cura`. 1 bloco leve e 1 remédio (da carga do paciente, ou da de quem trata, que cobra o preço de base dele); um tratamento por paciente por dia; pede mão de cura de Iniciante (de Treinado, se há ferida grave). Soma 1 dia de repouso a todas as feridas do paciente: tratado todo dia, a ferida sara na metade do tempo. O dom da cura soma meio dia por grau, e se mostra no primeiro tratamento.

14.7 **Os serviços, de pessoa a pessoa.** Quem é ajudado paga quem presta (evento `servico`: a prata só muda de mão): ler 10 · a cura 3 por lance · a bênção 5 por pessoa · tratar 2 e o remédio · benzer a arma 5 · o rito de quebrar, um terço do preço de tabela da categoria · a lição, o salário de quem ensina. A gente do mundo não procura serviço sozinha nesta etapa (é da etapa 3): a única renda que a magia dá a quem presta, fora o que o personagem pagar, é o jornal (12.8).

14.8 **A magia no mercado.** As poções do Comum ao Raro são bens como os outros, com preço pelo estoque: a Comum vale 6 de prata, vezes 6 por categoria. A peçonha (2 de base, Comum) e a água benta (3) também. O povo gasta pouco: a vila de 400 quer 6 poções de cura, 2 antídotos, 1 vigília e 1 quebra-maldição Comuns, e 1 cura Incomum. **A loja não negocia o veneno de lâmina** (crime). O "vender tudo" não leva as poções nem a água benta (são de usar: vendem-se pelo nome). **O foco, o amuleto e o escrito** a loja negocia como peça (paga 40% do valor, mais a mão de comércio; a loja farta conta junto com as armas da mesma categoria); o elixir não tem loja. **A parte da magia de um mercado abre-se à parte** (`mercado.py magia`, pelo Mestre ou pelo gerador): a botica do lugar faz para o povo as poções até a categoria dela (a de vila, só as Comuns: produção no consumo, prateleira no alvo); a prateleira tem cada poção que a loja negocia até uma categoria acima disso; a água benta e o quebra-maldição, onde há santuário; e amuletos, focos e um escrito na prateleira (a vila: 2 amuletos, 1 varinha, 1 símbolo e a Cartilha do arcano, que ensina seta e luz).

14.9 **Quem registra o quê** (o Mestre, ou o gerador da vila): `alquimia.py botica N`, `encanto.py runas N`, `magia_mundo.py santuario N`, `mercado.py magia`, `maldicao.py peca ITEM "Nome" CATEGORIA TIPO onde=LUGAR`, `maldicao.py lugar "Nome" CATEGORIA TIPO`, `maldicao.py poe ALVO "Nome" CATEGORIA TIPO CONDICAO`, e os preparos (`oficio.py preparo vidraria Comum "como" oficio=alquimia`).

### O banco de provas do mundo da magia (`provas_magia.py`)

| Meta | O que se mede | Faixa | Medido |
| --- | --- | --- | --- |
| MG1 | a pessoa comum: dez dias de rotina com os módulos da magia ligados e desligados | o mesmo mundo | igual (estado e eventos) |
| MG2 | estudar: grau 1 em 6 blocos (Prodígio 3); o mestre só na jornada dele; o escrito de graça; as recusas | sempre | sim |
| MG3 | a Mana fora da luta, por tradição; a prece; a maldição do passo 4 | a conta exata | sim |
| MG4 | a maldição da categoria da guarda · a Comum num aldeão · a mais curta | 10 a 25 · 7 a 14 · nunca antes de 5 dias | 15 · 10 · 5 |
| MG5 | o clérigo Mestre de símbolo Raro, na maldição Rara, passos 1 e 2 | 45 a 70% | 57% e 48% |
| MG6 | a poção da categoria · uma abaixo, em golpes médios entre iguais | 0,7 a 1,5 · até 0,5 | cerca de 1,1 · 0,35 |
| MG7 | o limite do corpo e o teto da cura do dia | sempre | sim |
| MG8 | quem compra a matéria e vende a leva, com a prateleira no alvo | o Leigo nunca ganha; a melhor mão, no máximo 6 | −3 · −1 |
| MG9 | o alquimista de loja (com botica; sem botica que produza), 30 vilas | 6 por dia (pior 12) nos 5 primeiros dias; 4 depois | 0 · 0 |
| MG10 | fazer foco e amuleto para a loja, 30 vilas | a mesma | 1,8 a 3,4 (pior 5,8) · 0 |
| MG11 | o serviço de magia: a jornada; a prata que só muda de mão | sempre | sim |
| MG12 | a peça maldita e o lugar maldito | sempre | sim |
| MG13 | gravar custa o que diz; a falha por 10 amaldiçoa a peça | sempre | sim |
| MG14 | a MESA pelos três degraus; o RETOMAR; o fecha que recusa no passo 4 | sempre | sim |
| MG15 | a prata e a matéria fecham; o núcleo perdido sai do Livro | sempre | sim |
| MG16 | o voto, o laço e a dívida | sempre | sim |
| MG17 | as recusas | todas | sim |
