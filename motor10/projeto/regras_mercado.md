# O MERCADO: o preço que sai do estoque, a prata contada, as peças da loja (etapa 2)

> **RASCUNHO GUARDADO.** O capítulo que vale é o 8 do `../REGRAS.md`, que a integração da etapa 2 acertou (regras mudadas e números medidos de novo). O que está aqui é o texto do construtor, de antes da revisão: as tabelas de medida e as réguas são daquele dia.

Capítulo para o `REGRAS.md` (o número 8 é provisório: quem monta o livro o acerta). Os números moram no `tabelas_mercado.py`; as provas, no `provas_mercado.py`.
O comando é o `mercado.py`. Tudo o que ele faz entra por evento (`compra`, `venda`, `producao`, `consumo`), e a prata só muda de mão.

## 8. O mercado

8.1 **Onde há mercado.** Num lugar com povo contado (`lugar.pop`). **Lugar sem povo não tem mercado:** ali não se compra, não se vende, e a virada do dia não faz nada.
O mercado de um lugar é o estoque dele (`lugar.estoque`), a prata dele (`estoque.prata`) e as peças que estão nele sem dono.

8.2 **O preço de um bem** sai do estoque: **base × √(alvo ÷ estoque)**, nunca abaixo de 0,4 nem acima de 3 vezes a base.

| O lugar tem | O bem vale |
| --- | --- |
| nada, ou até um nono do alvo | × 3 (o teto) |
| um quarto do alvo | × 2 |
| metade do alvo | × 1,41 |
| o alvo | × 1 (a base) |
| o dobro do alvo | × 0,71 |
| o quádruplo | × 0,5 |
| 6,25 vezes o alvo, ou mais | × 0,4 (o chão) |

8.3 **O alvo** é o estoque que o lugar quer ter: **30 dias do consumo do povo** dele. A comida é a exceção: **60 dias**, porque se colhe uma vez por ano e o celeiro tem de atravessar o inverno e a entressafra.

| Bem | Base (prata) | Consumo por pessoa, por dia | O alvo numa vila de 400 |
| --- | --- | --- | --- |
| comida | 1 | 1 | 24.000 |
| lenha | 1 | 0,25 (no verão × 0,75; no inverno × 1,5) | 3.000 |
| carvão | 2 | 0,02 | 240 |
| sal | 3 | 0,02 | 240 |
| pano | 5 | 0,01 | 120 |
| remédio | 8 | 0,005 | 60 |
| ferramenta | 12 | 0,005 | 60 |

Uma unidade de comida é uma refeição: alimenta uma pessoa por um dia.

8.4 **A matéria** tem categoria, e o preço dela é vezes 6 a cada categoria, como o das peças. O povo gasta um sexto a cada categoria acima.

| Matéria | Comum | Incomum | Rara | Consumo por pessoa, por dia (Comum) |
| --- | --- | --- | --- | --- |
| metal | 3 | 18 | 108 | 0,01 |
| couro | 2 | 12 | 72 | 0,01 |
| osso | 1 | 6 | 36 | 0,005 |
| madeira | 2 | 12 | 72 | 0,02 |
| erva | 2 | 12 | 72 | 0,01 |

O povo de um lugar tira matéria até o Incomum. **A Rara ninguém produz:** só existe no mercado a que alguém trouxe do ermo ou da masmorra, e o povo a consome devagar.
Do Épico para cima não há matéria: há núcleo (7.3), e núcleo não se negocia em loja.

8.5 **Comprar e vender.** Toda compra mexe no estoque, e por isso no preço: a do jogador também.
- **O lote é pago unidade a unidade:** cada uma já mexe no preço da seguinte. Comprar tudo de uma vez custa o mesmo que comprar aos poucos.
- **Comprar custa 10% a mais** que o preço. **A loja paga de 60 a 80% do preço**, conforme a mão de comércio de quem vende (8.7).
- **A prata é inteira:** a compra arredonda para cima, a venda para baixo. A venda que não chega a 1 de prata é recusada. Quem vende vários bens de uma vez (a cesta) arredonda uma vez só.
- **Comprar e vender de volta sempre perde:** 45% com mão de Leigo, 27% com a melhor mão que existe.
- O bem comprado entra na carga da pessoa; o vendido sai dela e entra no estoque do lugar.

8.6 **A prata é contada.** Ela passa do bolso da pessoa para o estoque do lugar e de volta; nenhum negócio a cria nem a apaga. **Loja sem prata não compra:** se a prata do lugar não paga o lote, a venda é recusada, e o comando diz até quanto ela compra hoje.
É a mesma prata que paga o salário de quem trabalha no lugar.

8.7 **A mão de comércio** (`maestria.comércio`) decide quanto a loja paga a quem vende. Sobe por **dias de negócio**: o dia em que a pessoa fecha pelo menos um negócio de 10 de prata ou mais conta um (um por dia).

| Grau | A loja paga | Dias de negócio | E um feito |
| --- | --- | --- | --- |
| Leigo | 60% | | |
| Iniciante | 65% | 20 | |
| Treinado | 70% | 80 | |
| Mestre | 75% | 250 | um negócio só de 1.000 de prata ou mais |
| Lendário | 80% | 750 | um negócio só de 10.000 de prata ou mais |

8.8 **As peças da loja** são itens do Livro de Itens com `onde` no lugar e sem dono, **até o Épico**. Daí para cima, e para núcleo, não há loja: leilão, encomenda ou despojo.
- **O valor** de uma peça é o preço de tabela da categoria (Comum 30, vezes 6 por categoria: Incomum 180, Raro 1.080, Épico 6.480) **menos o conserto que ela pede** (7.10: 2% do preço por ponto gasto), e nunca menos que a sucata.
- **Quebrada** (durabilidade 0), vale **sucata: 10%** do preço de tabela.
- **Sob medida** (2.8), vale como **uma categoria abaixo**: na mão de outro é isso que ela rende.
- **A loja pede** o valor, sem os 10% dos bens. **A loja paga** a parte dela (60 a 80%, 8.7), e **20% a menos por cada peça igual que já tem na prateleira** (mesmo tipo, família ou material, partes e categoria).
- Comprada, a peça ganha dono; vendida, fica sem dono e com `onde` no lugar. As duas coisas entram na história dela.

| Uma espada Rara | Vale | A loja paga a um Leigo |
| --- | --- | --- |
| nova (30/30) | 1.080 | 648 |
| gasta (15/30) | 756 | 453 |
| quebrada (0/30) | 108 | 64 |
| sob medida para outro | 180 | 108 |

8.9 **A virada do dia.** Em cada lugar com povo, nesta ordem, e sem mexer na prata:
- **O lugar produz** o que está em `lugar.produz` (bem: quanto por dia). **Toda produção acompanha o preço:** a quantidade vezes o fator do preço do dia, entre a metade e o dobro.
  Quando falta, o povo dobra o serviço; quando sobra, corta pela metade.
  **A comida, além disso, é colheita:** vezes a estação (`tabelas_mundo.COLHEITA`: primavera 0,5 · verão 1 · outono 2,5 · inverno 0).
- **O povo consome** o que a tabela diz, até onde o estoque dá.
- A parte quebrada de uma quantidade vira a chance de mais uma unidade, pelo acaso do mundo: mesma semente, mesmo mercado.

Por isso **o preço anda sozinho:** o que foi comprado a mais volta em cerca de dois meses; o que foi vendido a mais escoa mais devagar; a lenha encarece no inverno.

8.10 **O ano da comida** (medido numa vila de 400 cuja produção de tabela é igual ao que ela come; o ciclo se repete igual, ano após ano):

| Quando | A comida vale |
| --- | --- |
| o Dia 1 (começo da primavera) | × 1,13 |
| o fim da primavera (o pico: a entressafra) | × 1,73 |
| o fim do verão | × 1,13 |
| depois da colheita (o fim do outono: o piso) | × 0,66 |
| o fim do inverno | × 1,14 |

**O pico do ano é o fim da primavera, não o fim do inverno:** a colheita da primavera é meia e o celeiro segue caindo até o verão. No verão, com a comida cara, o povo produz mais, e o preço cede.
**O celeiro se acerta sozinho.** O lugar que colhe 10% a menos do que come não desanda: acha outro ciclo, mais caro (de × 0,70 a × 2,18). O que colhe 10% a mais, um mais barato (× 0,63 a × 1,42).
Com 20% a menos a comida bate no teto toda entressafra (medido em rascunho): é fome, e é assunto das frentes.

8.11 **Negociar não gasta bloco** (como comer). Só se negocia no lugar onde a pessoa está. Morto não negocia.

8.12 **Abrir um mercado** é coisa do gerador, ou do Mestre, por um evento `gera` (`mercado.py funda POVO`). Ele põe: o povo; a produção igual ao consumo desse povo, menos a da matéria Rara (o preço de equilíbrio fica na base);
o estoque no alvo (a comida, no ponto do ano: 47 dias de celeiro no fim do inverno); a prateleira do tipo do lugar (peças Comuns e algumas Incomuns); e, se o lugar não tem prata, **5 de prata por pessoa**
(aldeia de 120: 600; vila de 400: 2.000; cidade de 1.500: 7.500).

### O banco de provas do mercado

Roda em mundos de rascunho: a vila de prova da etapa 1, com um mercado aberto de 400 pessoas e 2.000 de prata no lugar. **Toda prova confere que a soma da prata do mundo fecha** e que o estado segue inteiro.

| O que se mede | Meta | Medido |
| --- | --- | --- |
| comprar sobe o preço e vender desce | sempre | 600 idas e voltas ao acaso: sempre; desfeito o negócio, o preço volta ao que era |
| comprar e vender de volta no mesmo lugar perde | 20% ou mais | no mínimo 45,5% com mão de Leigo e 27,3% com mão de Lendário |
| a soma da prata (gente mais lugares) antes e depois de 200 negócios ao acaso | a mesma | 12.200 e 12.200, e igual depois de cada negócio (dois lugares, duas pessoas, bens, cestas e peças; 231 pedidos recusados no caminho); e igual três viradas depois |
| o preço nunca sai da faixa | 0,4 a 3 bases | 22 bens em 308 estoques, de zero a um trilhão: nenhum fora |
| a loja sem prata | recusa a compra | recusa; com 7 de prata compra 13 de lenha e recusa 14 |
| um ano de viradas numa vila de 400: a comida | entre 0,6 e 2,2 bases | de × 0,66 a × 1,73 |
| ... cara no fim do inverno e barata depois da colheita | sim | × 1,14 no fim do inverno (72% acima do pós-colheita), × 0,66 depois da colheita. **Ressalva:** o fim do inverno não é o pico; o pico é o fim da primavera (× 1,73), e 178 dias do ano são mais caros que o fim do inverno |
| com os preços de um dia comum, o que sobra ao diarista (salário 4, cama 2, a comida do mercado) | 0 a 2 de prata | no alvo: 0,86 (a comida comprada para a semana) e 0 (comprada no dia); no dia mediano do ano (× 1,13): 0,71 e 0. No pico: 0,00 |
| peça gasta vale menos que nova; peça quebrada vale sucata | sim | a espada Rara: 1.080, 756 e 108 |
| as peças da loja são itens do Livro com `onde` no lugar e sem dono | sim | 15 de 15; comprar põe o dono, vender tira e põe o `onde`; 7 pedidos errados recusados |
| a loja farta paga menos | 20% por peça igual | 14 adagas iguais: 14, 11, 9, 7, 5, 4, 3, 3, 2, 1, 1, 1, e duas recusadas; ao todo 61 de prata (seriam 252) |
| o preço anda sozinho | sim | comprada a metade da lenha: × 1,41; depois × 1,15 em 30 dias, × 1,08 em 60, × 1,04 em 90. A lenha: × 0,83 no fim do verão, × 1,48 no fim do inverno |
| o celeiro se acerta sozinho | o ciclo se repete | três anos iguais (× 0,66 a × 1,73); com a safra 10% menor, × 0,70 a × 2,18; 10% maior, × 0,63 a × 1,42 |
| a mão de comércio | 60 a 80% | 100 de lenha rendem 59 a um Leigo e 79 a um Lendário; Iniciante aos 20 dias de negócio; Mestre só com o negócio grande |
| catorze pedidos errados (sem prata, sem estoque, bem que não existe, quantidade errada, morto) | recusados, sem mudar nada | 14 de 14; na vila sem povo, nada se negocia e a virada não gera evento |
| a mesa mostra os preços do lugar onde o personagem está | sim | muda de lugar, muda a mesa; a parte do mercado tem 2,5 KB |
| mesma semente, mesmo mercado | sim | 40 dias numa vila de 137 e o ano inteiro, rodados duas vezes: idênticos |

### O que este capítulo não resolve (fica dito)

- **A taverna tem preço fixo.** A refeição do `ato.py comer` custa 1 de prata o ano inteiro, e sai do mesmo celeiro. O mercado sabe dizer o que ela valeria no dia (`mercado.refeicao`: 1 de prata em 320 dias do ano, 2 nos 44 da entressafra), mas ninguém cobra isso ainda.
- **Ninguém além do jogador compra peça.** A prateleira não escoa e não se repõe sozinha: a loja farta fica farta. O freguês com nome é da etapa 3.
- **O povo não passa fome.** Com o celeiro vazio a comida vai ao teto e a taverna não serve; o povo não diminui nem vai embora. Isso é das frentes.
- **Não há caravana.** O lugar que não produz um bem fica sem ele, no teto, até alguém trazer.

### Os comandos

```
python3 mercado.py ver                       os preços daqui, a prateleira, o que você carrega e quanto a loja paga
python3 mercado.py preco couro:1 4           quanto custam 4 e quanto a loja paga por 4, sem negociar
python3 mercado.py comprar comida 7          ·   mercado.py vender couro:0 6   ·   mercado.py vender lenha tudo
python3 mercado.py vender tudo               a cesta: tudo o que você carrega e a loja negocia, num negócio só
python3 mercado.py comprar i0014             uma peça da prateleira   ·   mercado.py vender i0001   uma peça sua
python3 mercado.py funda 400 "como foi"      o Mestre abre um mercado onde a pessoa está
python3 provas_mercado.py                    o banco de provas do mercado
```

Para os outros módulos: `mercado.preco(E, lugar, bem)` · `mercado.custa(E, lugar, bem, n)` · `mercado.paga(E, pessoa, bem, n)` · `mercado.cabe(E, pessoa, bem)` (quanto a loja consegue pagar)
· `mercado.comprar` · `mercado.vender` · `mercado.vender_cesta` · `mercado.comprar_peca` · `mercado.vender_peca` · `mercado.prateleira(E, lugar)` · `mercado.funda(E, lugar, povo)` · `tabelas_mercado.base(bem)`.
