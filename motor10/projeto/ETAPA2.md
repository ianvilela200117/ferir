# ETAPA 2 — viver de um ofício: o contrato de construção

Quatro módulos entram no Motor 10 nesta etapa: **os bichos**, **o ofício** (forjar, consertar, ajustar), **o mercado** e **a caça e a coleta**.
Este arquivo é o contrato entre quem constrói cada um. Ler antes: `../LEIA.md`, `../PROJETO.md`, `../REGRAS.md` (capítulos 1 a 5), o cabeçalho do `../estado.py`, as páginas `../tabelas*.py` e o `../provas_mundo.py`.

## AVISO: esta é a SEGUNDA tentativa (leia antes de tudo)

A primeira frota foi cortada no meio. O que ela fez está no disco e não é para refazer:

- **O ofício está INTEIRO** (`oficio.py`, `tabelas_oficio.py`, `provas_oficio.py`, `projeto/regras_oficio.md`): 14 de 15 provas; a da Lendária não bate, e isso está dito no banco dele. Ninguém o reescreve.
- **Os bichos estão QUASE PRONTOS.** `luta.py`, `pessoas.py`, `itens.py`, `tabelas.py`, `provas.py`, `estresse.py`, `bichos.py` e `tabelas_bichos.py` já foram mudados pelo construtor anterior. Hoje `python3 provas.py` passa **72 de 72** (as 51 metas antigas e as 21 dos bichos, B1 a B8) e o `estresse.py` roda sem erro. **O construtor dos bichos NÃO recomeça:** lê o que está no disco, confere contra a seção 4 (a API fixa, a lista fechada de traços, a moral, a frase da ameaça, o corpo que não é peça, o estresse com bichos), termina o que faltar, escreve o capítulo `projeto/regras_bichos.md` (que não existe ainda) e entrega o relatório. A linha de base dele é 72 de 72, não 51.
- **Faltam inteiros:** o mercado e a caça. Depois, a revisão, a integração e a vila de teste.

## 0. Como trabalhar (vale para todos)

1. **Isto é FORA do jogo do Ferir.** O `CLAUDE.md` da raiz é do jogo: NÃO siga o ritual de abertura dele. **NUNCA rode script da raiz do repositório** (eles rolam dado e mexem num save que está em uso). Trabalhe só dentro de `motor10/`. Não use git. Não toque em nada fora de `motor10/`.
2. **Cada um tem os seus arquivos** (seção 2). Não edite arquivo de outro dono nem os do alicerce. Precisa de algo neles? Escreva o pedido no seu relatório final (`pedidos`) e contorne enquanto isso.
3. **Só `estado.aplica()` muda o mundo.** Nada de escrever JSON por fora. Evento sem efeito não existe. Os verbos estão no cabeçalho do `estado.py` (`pessoa` com `carga.BEM`, `lugar`, `estoque`, `item` com `nasce`/`onde`/`sob_medida`/`historia`/`some`, `obra`).
4. **A prata não nasce nem some.** Ela passa do bolso da pessoa (`moedas`) para o estoque do lugar (`estoque.prata`) e de volta. Só os eventos `gera` e `mestre` podem criar prata. Toda prova de módulo confere que a soma fecha.
5. **O tempo só anda por `ato.passa()`** (ele cuida do corpo, da virada do dia e das paradas). Todo ato custa blocos (1 bloco = 4 horas).
6. **O dado:** teste de quem está em cena sai de `teste.rola()` (dado de verdade, uma vez, fica no caderno do turno). O acaso do mundo (o que nasce, o que aparece) sai de `estado.sorte(E, chave)`: mesma semente, mesmo mundo.
7. **Números só nas páginas `tabelas_*.py`** do módulo. Código em Python puro, no estilo dos arquivos que já existem. Tudo em português. Sem argumento, o script só imprime o uso.
8. **Provas numa pasta de rascunho:** nunca num save. Use `provas_mundo.vila()` como base e a variável `MOTOR10_MUNDO` quando precisar de arquivos.
9. **Cada módulo entrega:** o script (funções para importar e linha de comando), a página de tabelas, `mesa(E)` (as linhas dele para a `MESA.md`), `virada(E)` se o mundo dele anda sozinho, o `provas_<módulo>.py` com `provas(n)` que devolve `[(nome, o que deu, passou?)]`, e o capítulo dele para o livro em `projeto/regras_<módulo>.md` (no estilo do `REGRAS.md`: numerado, curto, sem história, com as tabelas).

## 1. O que o jogador decidiu (e pesa nesta etapa)

- **O item decide a luta** (`REGRAS.md` 2.3). Um bicho segue a mesma conta: o corpo dele é a arma e a armadura, com categoria.
- **Todo mundo morre de vez,** o personagem também. O perigo tem de ser legível antes da luta.
- **O ritmo é o rápido:** pelo caminho comum, a primeira peça Rara perto do dia 20 a 30, a Épica do 60, a Única do 160, a Lendária do 360. **Os dias não são tranca:** não há regra de calendário. O que tranca é o que existe no mundo (matéria, núcleo, maestria, oficina).
- **O raro é contado.** Bicho raro tem número no mundo e demora a nascer de novo. Núcleo é item do Livro de Itens.
- Quer um mundo duro, com consequência, onde conquistar custe.

## 2. Os donos dos arquivos

| Módulo | É dono de | Não toca |
| --- | --- | --- |
| **bichos** | `luta.py`, `tabelas.py`, `pessoas.py`, `itens.py`, `provas.py`, `bichos.py` (novo), `tabelas_bichos.py` (novo), `projeto/regras_bichos.md` | o resto |
| **ofício** | `oficio.py`, `tabelas_oficio.py`, `provas_oficio.py`, `projeto/regras_oficio.md` | o resto |
| **mercado** | `mercado.py`, `tabelas_mercado.py`, `provas_mercado.py`, `projeto/regras_mercado.md` | o resto |
| **caça** | `caca.py`, `tabelas_caca.py`, `provas_caca.py`, `projeto/regras_caca.md` | o resto (lê o `bichos.py` pronto) |

Do alicerce, ninguém edita: `estado.py`, `ato.py`, `turno.py`, `corpo.py`, `teste.py`, `tabelas_mundo.py`, `provas_mundo.py`, `REGRAS.md`, `PROJETO.md`, `MUDANCAS.md`.

## 3. A língua comum (já está no `tabelas_mundo.py`)

- **Bens** na carga da pessoa e no estoque do lugar: `comida`, `lenha`, `carvão`, `sal`, `pano`, `remédio`, `ferramenta`; e a **matéria com categoria**, de chave `"nome:categoria"`: `metal:0`, `couro:1`, `osso:2`, `madeira:0`, `erva:1` (`M.materia()`, `M.le_materia()`).
- A matéria comum vai até o Raro (`MATERIA_ATE = 2`). **Do Épico para cima a obra pede um NÚCLEO:** item do Livro, `dict(tipo='nucleo', cat=k, nome=..., dur=[1, 1], dono=..., onde=..., de=ESPÉCIE, historia=[])`.
- **Preço de peça:** 30 de prata a Comum, vezes 6 por categoria; a loja vende até o Épico. Conserto na oficina de outro: 2% do preço por ponto.
- **O lugar** pode ter: `tipo` (vila, cidade, ermo, masmorra), `pop`, `estoque` (com `prata`), `produz` (bem: quanto por dia), `oficina` (0 a 4), `cama`, `vizinhos` (ids), `bichos` e `teto` (espécie: quantos), `coleta` e `coleta_teto` (bem: quanto).
- **A pessoa** tem: `carga`, `maestria` e `treino` (por arma e por ofício: `forja`, `couro`, `caça`, `coleta`, `comércio`, `cura`), `grau_oficio`.
- **Viagem ainda não existe** (é da etapa 3). Nesta etapa, caçar e coletar são "sair para o ermo vizinho e voltar": um ato só, que conta os blocos de ida e de volta, e a pessoa segue morando no lugar dela.

## 4. Os bichos

**A ideia:** um bicho é uma ficha de luta como qualquer outra. O corpo é a arma (garra, presa, chifre, cauda, casco, ferrão) e a armadura (pelo, escama, carapaça), com categoria, e a regra de ouro vale igual. Ele tem tamanho, traços e moral.

- **Espécies:** de 12 a 16, do Comum ao Lendário, com grau de F a S casado com a categoria. Há bicho de bando, bicho sozinho e chefe (que dá núcleo). Cada uma: nível, atributos, as armas do corpo, o couro, tamanho, traços, moral, o bando em que anda, o despojo (matéria com categoria e quantidade) e onde vive.
- **Tamanho** (pequeno, médio, grande, enorme): mexe no PV, no alcance, em quantos cabem no cerco em volta dele, em quanto ele ocupa de um corredor, e na Defesa (o pequeno é difícil de acertar; o enorme, fácil).
- **Traços:** uma lista FECHADA de 8 a 12 que a luta sabe rodar (por exemplo: matilha, bote, investida, veneno, agarra, voa, regenera, apavora, couraça, sopro). Traço que a luta não roda não entra. Cada traço tem prova de que mexe no resultado para o lado certo.
- **Moral:** bicho comum foge ferido; o encurralado e o chefe não.
- **O corpo não é peça:** não quebra, não muda de dono, não ocupa sintonia. O despojo sai da tabela.
- **API que a caça vai usar (fixa):** `tabelas_bichos.ESPECIES[espécie]` (com `nome`, `cat`, `grau`, `tamanho`, `bando`, `despojo`, `nucleo`, `habitat`); `bichos.bicho(espécie, nome=None, **mais)` devolve a pessoa pronta para o `luta.nova`; `bichos.bando(espécie, sorte)` devolve a lista; `bichos.despojo(espécie, sorte)` devolve `{bem: quantidade}` e se saiu núcleo; `bichos.ameaca(espécie)` devolve a frase que o caçador lê antes da luta (o grau, o tamanho, o que se sabe).
- **Provas** (no `provas.py`, num bloco novo "OS BICHOS"; as 51 metas de hoje seguem passando, sem mexer em faixa):
  1. homem contra bicho do mesmo degrau (nível 50, tudo Raro, contra um bicho Raro médio sozinho): 40 a 60%;
  2. uma categoria de vantagem na arma do homem vence o bicho em 80% ou mais; uma de desvantagem perde em 80% ou mais;
  3. bando: quatro lobos Incomuns contra um homem de conjunto Incomum: o homem vence 10 a 35% em campo aberto, e 20 pontos a mais num corredor de um;
  4. chefe enorme Épico contra quatro de nível 60 de conjunto Raro: o grupo vence 5 a 30%; contra quatro de conjunto Épico: 55 a 90%;
  5. o tamanho mexe para o lado certo (o enorme apanha de mais gente e é mais fácil de acertar; o pequeno, o contrário);
  6. cada traço muda o resultado em pelo menos 8 pontos para o lado certo;
  7. bicho comum ferido foge em 30% ou mais das lutas que perde;
  8. duração: luta de um contra um bicho do mesmo degrau, mediana de 3 a 9 rodadas.
- Rode também o teste de estresse com bichos misturados (lutas ao acaso, sem erro e sem quebrar os invariantes).

## 5. O ofício

**A ideia:** forjar é uma obra de vários dias, com matéria contada, que pode falhar e custa caro. Consertar é o pão do ferreiro. Ajustar faz a peça servir a um dono.

- **Forjar** uma peça de categoria k: a matéria (até o Raro, matéria comum de categoria k; do Épico para cima, um núcleo de categoria k mais matéria Rara), **3^k blocos pesados** de bancada (Comum 1, Incomum 3, Raro 9, Épico 27, Único 81, Lendário 243), numa oficina. No fim, um teste só: 2d20 + maestria de forja + Afinidade ÷ 10 + a oficina (0 a 4) + o preparo (até +8) contra **28 + 6 × k**.
- **A obra fica aberta** entre um dia e outro (`['obra', ...]`): a matéria entra quando ela abre; os blocos somam; o ato para quando o corpo pede; o teste só sai quando os blocos fecham.
- **Falhar custa:** por menos de 5, a peça sai uma categoria abaixo; por 5 ou mais, a matéria some (o núcleo também).
- **O preparo** é ganho no mundo, de 2 em 2: receita, ajudante, fogo, bigorna. Nesta etapa basta existir como marca da pessoa ou do lugar, com teto de +8.
- **A maestria de forja** sobe por blocos de bancada, como a das armas; de Mestre para cima pede um feito (uma obra da categoria certa).
- **Consertar:** devolve durabilidade. Feito por você: tempo e um pouco de matéria. Pago a um ferreiro: 2% do preço por ponto.
- **Ajustar (sob medida):** grava o dono numa peça; o grau sai da maestria de quem ajusta (1 a 4); custa tempo e teste.
- **Sem requisito de nível.** O que segura é a matéria, a oficina, a maestria e o dado.
- **Provas** (`provas_oficio.py`), com um **robô ferreiro que vive de verdade** (come, dorme, paga a cama) e tem a matéria na mão:
  1. a primeira peça Rara sai entre os dias 15 e 30; a primeira Épica entre o 45 e o 80 (com o núcleo na mão); a primeira Única entre o 130 e o 200; a Lendária entre o 300 e o 450;
  2. o melhor ferreiro possível (Lendário, oficina 4, preparo 8) acerta a Lendária entre 15 e 30% das vezes;
  3. um Iniciante em oficina de vila acerta a Comum em 85% ou mais, e a Rara em menos de 25%;
  4. a matéria gasta numa obra falhada some do mundo (a conta fecha); o núcleo perdido sai do Livro;
  5. a obra de vários dias sobrevive a fechar e abrir o estado; o ato para quando o corpo cruza um limiar;
  6. consertar 10 pontos de uma peça Rara custa o que a tabela diz, e a prata vai para a oficina;
  7. a peça ajustada rende no dono e rende uma categoria abaixo na mão de outro (`pessoas.ficha`).

## 6. O mercado

**A ideia:** o preço sai do estoque, e toda compra mexe nele, a do jogador também. O lugar tem prata contada: loja sem prata não compra.

- **Preço** de um bem: base × √(alvo ÷ estoque), entre 0,4 e 3 vezes a base; o alvo são tantos dias de consumo do lugar. Comprar custa 10% a mais; a loja paga de 60 a 80%.
- **As peças** da loja são itens do Livro com `onde` no lugar e sem dono. Preço pela categoria e pela durabilidade.
- **A virada do dia:** o povo come, o lugar produz (a colheita muda com a estação), e o preço anda sozinho.
- **Comandos:** ver os preços, comprar e vender bem, comprar e vender peça. Tudo por evento, com a prata passando de um lado para o outro.
- **Provas** (`provas_mercado.py`):
  1. comprar sobe o preço e vender desce; comprar e vender de volta no mesmo lugar sempre perde (20% ou mais);
  2. a soma da prata (gente mais lugares) é a mesma antes e depois de 200 negócios ao acaso;
  3. o preço nunca sai da faixa de 0,4 a 3 bases; a loja sem prata recusa a compra;
  4. um ano de viradas numa vila de 400 pessoas: a comida fica entre 0,6 e 2,2 bases, cara no fim do inverno e barata depois da colheita;
  5. com os preços de um dia comum, o diarista vive (o salário de um dia paga a cama e a comida, com sobra de 0 a 2 de prata);
  6. peça gasta vale menos que nova; peça quebrada vale sucata.

## 7. A caça e a coleta

**A ideia:** o ermo tem bichos contados e matéria contada. O que se tira, sai. O que nasce, nasce devagar. Caçar rende mais que a diária, e pode matar.

- **Sair para caçar** no ermo vizinho: blocos de ida, de procura e de volta. Rastrear é teste (Percepção + maestria de caça) contra a fartura do ermo. O que aparece sai da **contagem real**: um bicho, um bando, ou nada. Às vezes aparece o que não se procurava.
- **Antes da luta o caçador lê a ameaça** (`bichos.ameaca`) e escolhe: atacar, deixar, fugir. A luta é a do `ato.py luta`, com paradas e ordens. Vencida, o despojo entra na carga e o bicho sai da contagem.
- **Coletar** (minério, madeira, erva): blocos e teste; tira do `coleta` do ermo.
- **A virada:** os bichos criam devagar até o teto; a matéria volta devagar. Espécie caçada demais some por muito tempo. O bicho raro (o que dá matéria Rara ou núcleo) tem poucos no mundo e demora a nascer.
- **Provas** (`provas_caca.py`), com um **robô caçador** que vive de verdade:
  1. um caçador de nível 10 com peças Comuns, no ermo de começo, tira por dia de 1,5 a 4 vezes a diária do diarista (vendendo o despojo ao preço de base), e sai ferido ou morto em 2 a 12% das saídas;
  2. o mesmo robô, afoito (ataca tudo o que aparece, até bando e bicho de grau maior), morre em 30 dias em 70% ou mais das sementes;
  3. caçar 60 bichos de uma espécie derruba a contagem, o rastro fica mais difícil, e ela leva de 30 a 120 dias para voltar a nove décimos do teto;
  4. nenhuma contagem fica negativa; o núcleo de chefe entra no Livro com `de` e `onde`;
  5. o que sai do ermo é igual ao que entra na carga (a conta fecha).

## 8. O que cada relatório final traz

`resumo` (o que fez, em poucas linhas) · `arquivos` (os que criou ou mudou) · `provas` (a saída do banco dele, inteira) · `pedidos` (mudanças que precisa em arquivos de outro dono, com o porquê) · `duvidas` (decisões de regra que tomou sozinho e que o jogador talvez queira rever).
