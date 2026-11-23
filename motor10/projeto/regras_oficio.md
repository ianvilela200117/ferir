# O OFÍCIO: forjar, consertar e ajustar (etapa 2)

Capítulo para o `REGRAS.md` (o número 7 é provisório: quem monta o livro o acerta). Os números moram no `tabelas_oficio.py`; as provas, no `provas_oficio.py`.
O comando é o `oficio.py`. Tudo o que ele faz entra por evento (`forjar`, `consertar`, `ajustar`, `trabalhar`), e a prata só muda de mão.

## 7. O ofício

7.1 **A oficina.** Forjar, consertar e ajustar pedem uma oficina no lugar (`lugar.oficina`, de 0 a 4). Lugar sem o campo não tem oficina. O nível soma no teste.

| Nível | Oficina | Soma no teste | O ferreiro do lugar conserta (pago) até |
| --- | --- | --- | --- |
| 0 | bancada | 0 | Incomum |
| 1 | forja de vila | +1 | Raro |
| 2 | forja de cidade | +2 | Épico |
| 3 | grande forja | +3 | Único |
| 4 | forja mestra | +4 | Lendário |

7.2 **A bancada.** Bloco de bancada é bloco **pesado**: um bloco de forjar, de consertar, de ajustar ou de jornal. Cada um soma 1 ao treino do ofício.
Há dois ofícios de bancada: **forja** (armas, malha, placa, escudos) e **couro** (a armadura de couro). Cada um tem a sua maestria.

7.3 **Forjar.** Sem requisito de nível e sem tranca de maestria: quem tem a matéria e uma oficina pode abrir a obra.

| Categoria | Blocos de bancada | O teste é contra | Matéria | A mão que a obra pede |
| --- | --- | --- | --- | --- |
| Comum | 1 | 28 | da categoria | Leigo |
| Incomum | 3 | 34 | da categoria | Leigo |
| Raro | 9 | 40 | da categoria | Iniciante |
| Épico | 27 | 46 | matéria Rara e um **núcleo** Épico | Treinado |
| Único | 81 | 52 | matéria Rara e um núcleo Único | Mestre |
| Lendário | 243 | 58 | matéria Rara e um núcleo Lendário | Lendário |

- **O teste final** é um só, no último bloco: **2d20 + maestria do ofício + Afinidade ÷ 10 + a oficina (0 a 4) + o preparo (até +8)**, contra **28 + 6 por categoria**. A pena do corpo entra, como em todo teste.
- **A mão que a obra pede** é conselho, não tranca: abaixo dela a conta quase não fecha, e o comando avisa antes de abrir. (Para consertar sozinho, ela é o que se pede: 7.10.)
- **O núcleo** é item do Livro de Itens (tipo `nucleo`), da categoria da obra, na mão de quem forja. Um núcleo só entra numa obra por vez.
- Acima do Lendário ninguém forja (ainda).

7.4 **A matéria de cada peça** (na categoria da obra; do Épico para cima, matéria Rara):

| Peça | Matéria |
| --- | --- |
| adaga | 1 de metal |
| espada, maça | 3 de metal |
| machado | 2 de metal, 1 de madeira |
| martelo | 3 de metal, 1 de madeira |
| lança | 1 de metal, 2 de madeira |
| montante | 5 de metal |
| alabarda | 3 de metal, 2 de madeira |
| malho | 4 de metal, 1 de madeira |
| arco | 3 de madeira |
| besta | 3 de madeira, 1 de metal |
| escudo | 2 de madeira, 1 de metal |
| armadura de couro (corpo · elmo) | 4 · 1 de couro |
| armadura de malha (corpo · elmo) | 4 · 1 de metal |
| armadura de placa (corpo · elmo) | 8 · 2 de metal |

A armadura gasta por parte coberta: tronco 2, braços 1, pernas 1, cabeça 1 (a placa, o dobro).

7.5 **A obra fica aberta.** A matéria sai da carga e entra na obra **quando ela abre**. Os blocos somam de um dia para o outro; a obra mora no estado e sobrevive a fechar o turno.
O ato de trabalhar para quando o corpo cruza um limiar (5.6). O teste só sai quando os blocos fecham. Trabalha-se na oficina onde a obra abriu.
**Largar a obra:** com zero blocos, a matéria volta; com um bloco ou mais, a matéria se perde. O núcleo fica com o dono: só o teste o gasta.
A obra de quem morreu se desfaz na virada do dia.

7.6 **Falhar custa.**

| O teste | O que sai |
| --- | --- |
| passa | a peça, na categoria da obra |
| falha por 1 a 4 | a peça **uma categoria abaixo** (o núcleo se gasta nela). O Comum sai **tosco**: Comum, com metade da durabilidade |
| falha por 5 ou mais | nada: **a matéria some, e o núcleo sai do Livro de Itens** |

7.7 **A peça nasce no Livro de Itens** por evento, com o dono (quem forjou), `feito_por`, o dia, e a primeira linha da história dela (quem, onde, com que núcleo).

7.8 **O preparo** é ganho no mundo. São quatro, **+2 cada um, até +8**: a **receita** e o **ajudante** (da pessoa), o **fogo** e a **bigorna** (do lugar).
Cada preparo tem **alcance**: a categoria mais alta a que ele serve. Só soma na obra que ele alcança: a receita Comum não ajuda numa peça Rara.
Nesta etapa o preparo é uma marca; o Mestre o registra quando ele é ganho em cena (`oficio.py preparo fogo Raro "como foi"`).
Sugestão para quem gera o mundo (não é regra): o fogo e a bigorna de uma forja de vila alcançam o Incomum; os de cidade, o Raro; os da grande forja, o Épico; os da forja mestra, o Único. O alcance Lendário só se ganha em cena.

7.9 **A maestria do ofício** sobe por blocos de bancada, como a das armas sobe por blocos de treino:

| Grau | Blocos de bancada | E um feito |
| --- | --- | --- |
| Iniciante | 50 | |
| Treinado | 150 | |
| Mestre | 375 | uma obra Épica (ou melhor) nascida da sua mão |
| Lendário | 1.000 | uma obra Única (ou melhor) nascida da sua mão |

A peça que sai uma categoria abaixo conta como obra da categoria em que saiu.

7.10 **Consertar** devolve durabilidade a uma peça sua. Não tem teste.
- **Você, na bancada:** 5 pontos por bloco, e 1 de matéria principal da peça (metal, couro ou madeira, na categoria dela; Rara, do Épico para cima) a cada 10 pontos ou parte. Pede a mão que a categoria pede (7.3).
- **Pago ao ferreiro do lugar:** **2% do preço da peça por ponto**, em prata inteira, que vai para o estoque do lugar; um bloco de espera a cada 10 pontos ou parte. A oficina conserta até a categoria do nível dela mais um (7.1).

| Categoria | Preço de tabela | Conserto pago, por ponto | 10 pontos |
| --- | --- | --- | --- |
| Comum | 30 | 0,6 | 6 |
| Incomum | 180 | 3,6 | 36 |
| Raro | 1.080 | 21,6 | 216 |
| Épico | 6.480 | 129,6 | 1.296 |
| Único | 38.880 | 777,6 | 7.776 |
| Lendário | 233.280 | 4.665,6 | 46.656 |

7.11 **Ajustar (sob medida, 2.8)** grava um dono numa peça. Quem vai usar tem de estar ali; a peça é dele ou de quem ajusta.
- **O grau** sai da mão de quem ajusta: Iniciante 1, Treinado 2, Mestre 3, Lendário 4. Leigo não ajusta.
- **Custa** um bloco de bancada por degrau da categoria (Comum 1 ... Lendário 6) e, no fim, um teste com a mesma soma da forja, contra **22 + 6 por categoria**.
- Passou: o nome e o grau ficam gravados (e apagam o ajuste antigo). Falhou por 1 a 4: fica como estava. Falhou por 5 ou mais: a peça perde 5 de durabilidade.

7.12 **O jornal.** Servir na bancada da oficina do lugar (o conserto miúdo do povo): o lugar paga, por bloco, o salário do grau de ofício da pessoa (5.4), e o bloco conta como bancada. Oficina sem prata não paga.

### Quanto se acerta (a conta exata do dado)

| Quem, onde | Comum | Incomum | Raro | Épico | Único | Lendário |
| --- | --- | --- | --- | --- | --- | --- |
| Leigo, forja de vila, sem preparo, Afinidade 50 | 48% | 26% | 12% | 5% | 3% | 1% |
| Iniciante, forja de vila, preparo inteiro até o Comum, Afinidade 50 | 86% | 32% | 15% | 7% | 4% | 2% |
| Treinado, forja de cidade, preparo inteiro até o Raro, Afinidade 50 | 93% | 77% | 52% | 10% | 5% | 3% |
| Mestre, grande forja, preparo inteiro até o Único, Afinidade 60 | 98% | 89% | 70% | 44% | 23% | 4% |
| Lendário, forja mestra, preparo inteiro, Afinidade 60 | 100% | 95% | 80% | 57% | 32% | 15% |
| Lendário, forja mestra, preparo inteiro, Afinidade 100 | 100% | 99% | 91% | 74% | 48% | 26% |

**Como ler:** cada grau de maestria vale 2 pontos; a oficina, até 4; o preparo, até 8. O dado pesa mais que tudo isso. Do Épico para cima, mesmo o melhor ferreiro perde núcleos: é para doer.

### O banco de provas do ofício

O robô ferreiro vive de verdade (dorme na cama e paga, come e paga, vive do jornal, 3,5 blocos de bancada por dia), tem a matéria e o núcleo de cada obra na mão,
trabalha na forja mestra com o preparo todo, e sobe um degrau de cada vez: só abre a obra de um degrau quando tem a mão que ela pede, e repete até a peça nascer.

A medida da escada é o dia em que **metade das vidas já tinha a peça** (quem nunca a teve conta como nunca). O banco roda 50 vidas; os números abaixo são de 400, medidas à parte.

| O que se mede | Meta | Medido |
| --- | --- | --- |
| a primeira peça Rara do robô nasce | dias 15 a 30 | **Dia 17** (a primeira obra fecha no Dia 17 e acerta em 60% das vidas; 1,6 obra por vida) |
| a primeira Épica | dias 45 a 80 | **Dia 59** (a primeira obra fecha no Dia 51 e acerta em 34%; 2,6 obras e núcleos por vida) |
| a primeira Única | dias 130 a 200 | **Dia 177** (a primeira obra fecha no Dia 131 e acerta em 28%; 3,8 obras e núcleos por vida) |
| a primeira Lendária | dias 300 a 450 | **NÃO BATE:** nasce em 23% das vidas até o Dia 450. A primeira obra Lendária fecha no Dia 356 e acerta em 15% |
| a primeira OBRA de cada categoria fecha (acerte ou não) | as mesmas janelas | Dias 17, 51, 131 e 356 |
| o robô vive de verdade | come, dorme, paga | 3,5 blocos de bancada, 1 cama e 1 refeição por dia; nenhuma noite no chão, nenhum teste com pena; a prata do mundo fecha |
| o melhor ferreiro possível (Lendário, forja mestra, preparo 8, Afinidade 100) acerta a Lendária | 15 a 30% | 25,7% |
| um Iniciante em forja de vila acerta a Comum (com o preparo do Comum inteiro) | 85% ou mais | 86,2% (sem preparo: 57,2%) |
| o mesmo Iniciante acerta a Rara (onde aquele preparo não alcança) | menos de 25% | 15,4% |
| a matéria da obra falhada some; o núcleo perdido sai do Livro; a prata não mexe | a conta fecha | fecha em todas as obras |
| cada margem do teste dá a saída do livro (o dado posto à mão, só nesta prova) | 13 saídas | 13 de 13 |
| a obra de vários dias sobrevive a gravar e abrir o estado; o ato para pelo corpo | sim | parou no bloco 5 de 9; voltou igual |
| consertar 10 pontos de uma peça Rara, pago | 216 de prata, para a oficina | 216 |
| a peça ajustada rende no dono; na mão de outro, uma categoria abaixo | sim | Raro, +1 no acerto; Incomum na mão de outro |
| a maestria sobe por blocos; Mestre e Lendário pedem a obra | sim | sim |
| catorze pedidos errados (sem oficina, sem matéria, sem núcleo, sem prata, sem a mão) | recusados, sem mudar nada | 14 de 14 |

**A meta que não bate, e por quê:** o melhor ferreiro possível acerta a Lendária em 26% (a meta manda 15 a 30%), e cada obra Lendária são 243 blocos, uns 70 dias.
O robô chega à mão de Lendário no Dia 286 e fecha a primeira obra no Dia 356, dentro da janela; mas com 15% de chance a peça não nasce na metade das vidas.
As duas metas só cabem juntas se a da escada for lida como "a obra fecha": nessa leitura as quatro batem (dias 17, 51, 131 e 356).

### Os comandos

```
python3 oficio.py ver                                      a oficina daqui, a sua mão, o preparo, as obras abertas, a matéria
python3 oficio.py pede arma espada Raro                    o que a obra pede e a sua chance, sem abrir nada
python3 oficio.py forjar arma espada Raro "Espada do Vau" [blocos=3] [nucleo=i0007]
python3 oficio.py forjar armadura malha Raro "Cota do Vau" [cobre=cabeça]   ·   oficio.py forjar escudo Raro "Escudo do Vau"
python3 oficio.py continua [o0001] [blocos=3]   ·   oficio.py larga o0001
python3 oficio.py consertar i0001 [pontos=10] [pago]
python3 oficio.py ajustar i0001 [para=ID]
python3 oficio.py jornal 3
python3 oficio.py preparo receita|ajudante|fogo|bigorna Raro "como foi ganho"   ·   oficio.py oficina 2 "como foi"     (o Mestre registra)
python3 provas_oficio.py                                   o banco de provas do ofício
```
