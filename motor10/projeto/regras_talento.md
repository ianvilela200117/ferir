> **JUNTADO AO `REGRAS.md`** (capítulo 10) na integração da etapa da magia, com os acertos dela (o mau-olhado de −4, os chefes acertados, a loja que não compra peça maldita, o segredo fora do RETOMAR). O que vale é o `REGRAS.md`; este rascunho fica como registro.

# OS DONS E OS TALENTOS (etapa da magia)

> **RASCUNHO DO CONSTRUTOR (o alicerce).** Capítulo para o `REGRAS.md` (o número 10 é provisório: quem monta o livro o acerta). Os números moram no `tabelas_talento.py`; a regra, no `talento.py`; as provas, no `provas_talento.py` (o `provas_mundo.py` o roda).

## 10. Os dons e os talentos

10.1 **Dois botões na pessoa, para todo caminho.** O **talento** diz a pressa de aprender e até onde a mão sobe; não soma em conta nenhuma. O **dom** diz o poder: soma na conta como maestria que ninguém treinou. Os dois nascem com a pessoa e não mudam. Quem não tem nada de especial é a pessoa de antes desta etapa: os blocos de sempre, a conta de sempre.

10.2 **Os caminhos (16).**

| Tipo | Caminhos | O que o talento apressa |
| --- | --- | --- |
| mãos de arma | `fio` (adaga, espada, machado, montante) · `haste` (lança, alabarda) · `peso` (maça, martelo, malho) · `tiro` (arco, besta) | os blocos de treino de cada arma daquela mão |
| ofícios | `forja` · `couro` · `caça` · `coleta` · `comércio` · `cura` · `alquimia` · `encanto` | os blocos de bancada, de procura, de coleta; os dias de negócio |
| tradições | `arcano` (o mago) · `fé` (o clérigo) · `verde` (o druida) · `pacto` (a bruxa) | os blocos de estudo da tradição e de cada feitiço |

O soco não é de mão nenhuma. A ficha só guarda o que não é Comum: `talento: {"fio": 1, "arcano": -1}`, `dom: {"forja": 2}`.

10.3 **O talento.**

| Grau | Nome | Blocos de cada grau de maestria | Nas armas (Iniciante, Treinado, Mestre, Lendário) | Até onde a mão sobe | Quantos nascem assim, por caminho |
| --- | --- | --- | --- | --- | --- |
| −2 | Negado | o dobro | 80 · nada | Iniciante | 2 em 100 |
| −1 | Lerdo | uma vez e meia | 60 · 240 · 750 · nada | Mestre | 10 em 100 |
| 0 | Comum | os de sempre | 40 · 160 · 500 · 1.500 | Lendário | 76 em 100 |
| +1 | Jeitoso | dois terços | 27 · 107 · 334 · 1.000 | Lendário | 10 em 100 |
| +2 | Prodígio | a metade | 20 · 80 · 250 · 750 | Lendário | 2 em 100 |

- Os blocos arredondam para cima. O feito que Mestre e Lendário pedem não muda: o talento apressa os blocos, não dispensa o feito.
- Vale em toda escada: as armas, a forja e o couro (50, 150, 375, 1.000 de bancada), a caça e a coleta, o comércio (os dias de negócio), a alquimia e o encanto (a tabela da forja) e as tradições (a das armas).
- O teto não tira o que a pessoa já tem: só a impede de subir mais. Quem chega ao teto com os blocos de cima lê "a mão não sobe mais: o talento para em Mestre".
- Qualquer um aprende magia: o Negado também, até Iniciante, com o dobro dos blocos.

10.4 **O dom.**

| Grau | Soma na conta do caminho | Quantos nascem assim |
| --- | --- | --- |
| Dom | +1 | 45 em 1.000 pessoas |
| Grande Dom | +2 | 5 em 1.000 pessoas |

A pessoa tem no máximo um. O caminho sai do dado entre os 16, com peso 3 onde ela já é Jeitosa ou Prodígio. Cada caminho tem o seu nome à mesa (a mão do fogo, o faro, a língua do negócio, a mão que fecha, a centelha, a graça...).

| Caminho | Onde o dom soma | O que não dá |
| --- | --- | --- |
| mão de arma | no acerto com as armas dessa mão; e metade na Defesa | a ação e a reação a mais (são da maestria) |
| tradição | na Conjuração; metade na Firmeza; o mesmo na Mana | abrir feitiço de grau maior |
| ofício de bancada (forja, couro, alquimia, encanto) | no teste da obra, como um preparo que nasce com a pessoa: **preparo e dom juntos não passam de +8** | a chance da Lendária não sobe: o melhor ferreiro possível segue acertando 1 vez em 4 |
| caça, coleta, cura | no teste do rastro, da coleta, do tratamento | a mão que a matéria pede |
| comércio | 2,5 pontos (Dom) ou 5 (Grande Dom) no que a loja paga, sem passar de 80% pelos bens e 60% pelas peças | |

10.5 **Como nascem.** Pelo dado do mundo (mesma semente, mesma gente): um d100 por caminho (até 2, Negado; até 12, Lerdo; até 88, Comum; até 98, Jeitoso; 99 e 100, Prodígio) e um d1000 para o dom (até 5, Grande Dom; até 50, Dom). **O personagem do jogador** escolhe uma **inclinação**: naquele caminho o d100 rola duas vezes e vale o melhor (Jeitoso ou mais: perto de 23 em 100, em vez de 12). A vila de teste nova nasce assim (`vila_teste.py PASTA ... inclinacao=CAMINHO`); quem já existia ganha os seus pelo `vila_teste.py magia`.

10.6 **Ninguém nasce sabendo.**
- **O talento aparece fazendo:** 20 blocos no caminho depois de rolado, a MESA, em "Você", diz: "Com as armas de fio você pega depressa (Jeitoso): o que os outros firmam em 160 blocos, você firma em 107." Antes disso, só o Mestre sabe.
- **O dom fica escondido** até o primeiro teste em que foi ele que fez a diferença. Escondido, ele entra no dado, mas não na conta que vai à mesa: a mesa vê o total sem ele, e o veredito é o mesmo. Quando decide, a saída diz "sem o dom, não passava" (ou "saía pior", na bancada), e a MESA passa a dizê-lo. Na luta, o golpe que só passou por causa dele diz "acerta por pouco: sem o dom, errava". No comércio, a primeira venda em que ele pagou a mais diz "o comprador paga mais do que costuma: você tem jeito para o negócio". Também se mostra quando alguém o lê (o feitiço `ler`, ou um clérigo).
- Dos outros, a MESA não diz nada; o SÓ O MESTRE mostra o talento e o dom de quem está com o personagem.

10.7 **Dentro da lei "o item decide"** (medido no banco, 4.000 lutas por linha, nível 50, tudo Raro; com 8.000: o Dom 56%, o Grande Dom 61%): o Dom contra o gêmeo vence de 51 a 58%; o Grande Dom, de 54 a 64%; o Grande Dom contra o gêmeo com a arma uma categoria acima, até 15%; o Mestre com Grande Dom contra o Lendário sem dom, de 42 a 58%. O Grande Dom vale um grau de maestria e nada mais; uma categoria de peça vale muitas vezes isso.

10.8 **A escada pelo talento** (a conta dos blocos: 3,5 blocos de bancada por dia; a obra só abre com a mão que pede; 2 blocos de treino de arma por dia):

| Talento na forja | A 1ª obra Rara fecha no dia | Épica | Única | Lendária | Mestre numa arma |
| --- | --- | --- | --- | --- | --- |
| Negado | 32 | não abre | não abre | não abre | nunca |
| Lerdo | 24 | 72 | 184 | não abre | Dia 375 |
| Comum | 17 | 51 | 131 | 356 | Dia 250 |
| Jeitoso | 13 | 37 | 95 | 260 | Dia 167 |
| Prodígio | 10 | 30 | 77 | 213 | Dia 125 |

O prodígio anda uma categoria à frente do comum em boa parte do caminho, e nunca duas. O que tranca segue sendo o núcleo e a mão.

10.9 **A cena.** Zeca, o aprendiz da forja, tem um Grande Dom que ninguém conhece. Na primeira adaga, os dados dão o bastante para a conta da mesa errar por 1; o dom (preparo 4 e dom 2, dentro do teto de +8) faz passar. A saída diz: "Foi o dom que fez a diferença: há alguma coisa nas mãos de Zeca." A partir dali a MESA dele diz "Há alguma coisa em você: a mão do fogo (a forja), um Grande Dom".
