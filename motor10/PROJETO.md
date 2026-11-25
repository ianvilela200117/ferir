# MOTOR 10 — O PROJETO DO RESTO

**Todas as etapas estão feitas** (a última, a etapa final: `projeto/ETAPA_FINAL.md`). O mundo novo está em `mundo/`, pronto para a criação do personagem (`LEIA.md`, `GUIA_MUNDO.md`).

O núcleo está pronto e provado: a luta, os itens, a ficha que sai sozinha e os bichos (`REGRAS.md`, 80 de 80 no `provas.py`). As etapas 1 e 2 do mundo estão feitas, e o `provas_mundo.py` passa inteiro (98 de 98). Duas metas da etapa 2 foram fechadas por decisão do jogador (seção 12, 9 e 10): a Lendária é difícil de propósito, e a loja paga 40% pelas peças.
Este é o plano do que falta até o Dia 1 de um **mundo novo, do zero**: o mundo vivo, a magia, os bichos, o ofício e o turno.
Três projetos inteiros foram escritos de três ângulos (estão em `projeto/`, como rascunho). Aqui está o que ficou de cada um, com os números e as etapas.
**As decisões do jogador já estão tomadas (seção 12) e o plano abaixo já as segue.**

## 1. Em uma página

1. O mundo é uma região de **16 lugares** com estoque, gente, bichos e força contados. Um relógio só roda tudo, com você ou sem você.
2. Nele vivem **10.000 pessoas em número, 150 com nome e ficha, e 40 aventureiros rivais**, gente do próprio mundo, de todos os níveis, que disputa a mesma escada pela mesma regra e morre de vez.
2b. **O mundo já é velho quando você nasce:** de 400 a 1.000 anos de história gerada (casas, reinos, guerras, lendas, ruínas, peças com dono e passado). Você nasce numa casa, com parentes.
3. **O raro é contado.** Doze peças Épicas, quatro Únicas, três Lendárias no mundo inteiro. O que um rival leva, saiu do mundo.
4. **Doze frentes** (ameaças, ambições, faltas, mistérios) têm dono, meta e um relógio de 6 passos. Cada passo muda número: fecha estrada, mata gente, sobe preço.
5. O que toca você cai numa **caixa de entrada com prazo**. Calar tem preço escrito, e a caixa se resolve sozinha.
6. **Nada acontece sem número.** Um gravador só mexe no estado; evento sem efeito é recusado.
7. O turno são **dois comandos**: `abre` (a página do Mestre, gerada do estado) e `fecha` (que recusa fechar se algo ficou solto).
8. O Mestre lê **30 KB** ao abrir a sessão (hoje são de 246 a 632 KB), e nada depende da memória dele.

## 2. O que ficou de cada projeto

| Projeto | A ideia | O que ficou | O que não ficou, e por quê |
| --- | --- | --- | --- |
| **B, sistemas primeiro** | lugares com estoque e gente; evento é limiar cruzado | **o chão do mundo:** estoque, preço, ecologia contada, um gravador, os robôs de prova | sozinho dá gráfico, não dá drama |
| **C, drama primeiro** | frentes com relógio; um diretor que só escolhe a cena | **o enredo:** as frentes, os 12 verbos fechados, o nêmesis, o diretor neutro, o tempo de forja | os moldes de frente acabam em um ano; por isso o chão de B também gera frentes |
| **A, gente primeiro** | 480 agentes que agem 4 vezes por dia | **o rosto:** a memória dos nomeados (o que lembram de você, com peso), a notícia que anda e vira boato, a página que traz dois fatos que não tocam você | 480 agentes dão preço louco ou parado e levam meses para afinar; ficam 150 nomeados com rotina e um querer por semana |

## 3. O mundo

**Tempo.** Bloco de 4 horas, 6 por dia; semana de 7 dias; estação de 91; ano de 364. A estação muda a colheita (× 0,5 · 1 · 2,5 · 0), a estrada e o tempo do dia, que entra sozinho na luta.

**Corpo** (três medidores de 0 a 10, mais as feridas da luta):

| | Sobe | Desce | Cobra |
| --- | --- | --- | --- |
| Fome | +1 a cada 2 blocos | refeição −3 | em 4: −2 em todo teste; em 7: −4 e 5% do PV por dia |
| Sono | +1 por bloco acordado | −3 por bloco dormido | em 6: −2; em 8: −4, e dorme ali se falhar Vontade contra 28 |
| Cansaço | bloco pesado +2, leve +1 | sono −3 | cada 3 pontos tiram 1 do fôlego máximo; em 9: −2 em tudo |

Ferida sara em 7 dias; a grave, em 21 (com curandeiro, metade). PV: 10% por noite dormida sem fome.

**Mapa.** 1 capital (4.000), 2 cidades (1.500), 5 vilas (400), 8 aldeias e postos (120); 6 ermos com bichos contados; 8 masmorras; 24 rotas de 1 a 6 blocos. Cada rota tem `perigo`, que sai da conta: bichos do ermo, bando, patrulha. Quem aparece no encontro sai da contagem real.

**Gente.** O povo é número por lugar e ofício: come, produz, migra, passa fome, engrossa o bando. Os **150 nomeados** têm ficha de luta, rotina de 6 blocos, um querer por semana (que vira ato com efeito), laços, e **memória**: até 12 fatos com peso, de onde sai a opinião sobre você, com os porquês.

**Rivais.** 40 aventureiros nativos, em 6 guildas e alguns sozinhos, espalhados por todos os níveis: há novatos como você, veteranos e três Lendas vivas. Por semana escolhem um plano entre as mesmas missões, masmorras e leilões que você vê; por dia, executam. Compram no mesmo mercado. **Morrem de vez**, e a cada ano gente nova chega à idade de pegar em armas. Longe de você a luta deles sai de uma conta rápida, calibrada contra o `luta.py` (erro menor que 8 pontos). O ranking sai toda semana.

**A história.** O gerador não começa no Dia 1: ele roda de 400 a 1.000 anos em passos largos (ano a ano) antes de você nascer. Disso saem as casas e as linhagens, os reinos e as fronteiras, as guerras e as dívidas de sangue, as lendas mortas, as ruínas (que são as masmorras, cada uma com a sua origem) e a história de cada peça alta: quem forjou, quem perdeu, quem tem hoje. O presente é a ponta dessa história, e a crônica fica à disposição do Mestre e, aos pedaços, da gente do mundo, que conta o que sabe.

**Economia.** Prata. Viver custa 3 por dia; o diarista ganha 4; o oficial, 12 (a jornada são 2 blocos pagos por dia). Preço = base × √(alvo ÷ estoque), entre 0,4 e 3 vezes. **Toda compra mexe no estoque, a sua também.** Peça de loja: Comum 30, vezes 6 por categoria, até o Épico (6.480). De Único para cima não há loja: leilão, encomenda ou despojo.

**Frentes.** Doze no Dia 1 (4 ameaças, 4 ambições, 2 faltas, 2 mistérios), e o chão gera outras por limiar: grão abaixo de 10 dias, nasce a fome; ninhada acima do teto, nasce a praga. Cada uma rola por semana contra a resistência do lugar. Missão cumprida contra ela tira um passo; qualquer um pode cumprir. O passo 6 é o desfecho, sem volta.

**Notícia e janela.** Todo evento vira notícia, que anda uma rota por dia e vira boato depois do quarto salto. Você só lê o que chegou aonde está. A **janela do mundo** avisa a todos na hora: primeira limpeza de masmorra, peça Única ou maior, classe oculta achada, frente que acaba.

**A caixa.** `{de, pede, prazo, opções, padrão}`. Só escreve quem tem motivo no estado. Vencido o prazo, vale o padrão, sempre com custo (o cliente vai ao rival; a opinião cai). Cabem 7; o oitavo força o mais velho.

## 4. A conquista, em números

O item decide a luta; por isso a escada das peças É a escada do poder, e ela é trancada pelo que existe no mundo.

| Categoria | Dia da primeira (jogando bem) | Quantas no Dia 1 | O que tranca |
| --- | --- | --- | --- |
| Incomum | 5 a 10 | à venda | dinheiro: 180 de prata |
| Raro | 20 a 30 | 60 | material de masmorra ou de bicho contado; ofício Treinado; forja de cidade |
| Épico | 60 a 85 | 12 | núcleo de chefe (nascem 6 por ano no mundo todo); 27 blocos de forja |
| Único | 160 a 220 | 4 | núcleo de chefe maior (2 por ano) ou primeira limpeza; 81 blocos; Mestre |
| Lendário | a primeira tentativa perto do 360; a peça é rara de propósito | 3, com as Lendas | núcleo de calamidade; 243 blocos de bancada (cerca de 70 dias) por tentativa; o dado rola uma vez, no fim; o melhor ferreiro possível acerta 1 em 4 |
| Mítico | depois do ano 2 | 1, dormindo | |
| Primordial | talvez nunca | 0 | |

**Estes dias não são tranca.** Não há regra que diga "antes do dia tal, não". São o dia em que um jogador aplicado costuma chegar lá pelo caminho comum (juntar o material, subir o ofício, forjar). O que tranca é o que existe no mundo. Quem achar outro caminho chega antes: tomar a peça de quem a tem, herdar, ganhar de um senhor, ser o primeiro a limpar uma ruína, comprar num leilão, roubar. Como o item decide a luta, uma peça alta nas mãos no dia 20 é possível, e muda tudo. E pinta um alvo nas suas costas.

**Forjar:** material da categoria (do Épico para cima, um núcleo, que é item contado, com dono e lugar) + tempo de 3^categoria blocos + teste: 2d20 + maestria + Afinidade ÷ 10 + oficina (0 a 4) + preparo (até +8, cada +2 ganho no mundo: receita, ajudante, fogo, bigorna) contra 28 + 6 por categoria.
**Falhar custa:** por menos de 5, a peça sai uma categoria abaixo; por 5 ou mais, o material some. Missão falhada: a caução, a fama, e o dano acontece. Masmorra: a morte.
**Consertar** devolve a durabilidade (2% do preço por ponto). Toda luta gasta 1 de cada peça usada: o ferreiro tem serviço.

## 5. O medo

- **Todo mundo morre de vez. Você também.** A vida é uma só.
- **O herdeiro.** Em vida você nomeia quem segue: um filho, um irmão, um aprendiz, um companheiro jurado. É uma pessoa do mundo, com ficha própria, que vive e pode morrer antes de você. Morto o personagem, o jogo continua com o herdeiro: ele herda a casa, a oficina, as dívidas, os amigos e os inimigos, e as peças que o matador não levou. **Não herda o nível nem a maestria:** tem os dele. Quem morre sem herdeiro deixa a casa acabar, e o jogo recomeça com um estranho no mesmo mundo, que lembra do morto.
- **O nêmesis:** quem mata você fica com o que você vestia e vira uma frente pessoal do herdeiro.
- **Você vê** os sinais que a notícia trouxe, os prazos, o perigo das estradas que andou. **Fica oculto** o relógio de cada frente, a força, o chefe, os planos dos rivais, onde estão os núcleos. Investigar é ação com teste, e abre um campo por vez.
- **O diretor** só escolhe quais frentes entram em cena no dia (até 3). Não toca em dado, relógio nem estoque: o banco prova que o estado final é idêntico com ele ligado e desligado. Depois de queda ou peça perdida, ele não empilha ameaça; mas também não inventa alívio que não exista.

## 6. Como o Mestre não esquece

- **Um gravador só** (`estado.aplica`). Evento = `{dia, tipo, onde, quem, efeitos}`, com efeitos de 12 verbos fechados (estoque, preço, rota, perigo, povo, pessoa, laço, fama, item, frente, missão, caixa). Sem efeito, é recusado. A frase da mesa e a notícia saem dos efeitos.
- **Cada fato num lugar só.** O dono da peça está só no Livro de Itens; onde a pessoa está, só na ficha dela.
- **`turno.py abre`** só lê, e gera a `MESA.md` (até 8 KB): relógio e tempo · corpo e bolso · quem está aqui (o que faz, o que quer, o que lembra de você) · a caixa por prazo · notícias chegadas · o que dá para fazer aqui, com blocos e preço · a pauta do diretor · dois fatos que não tocam você · SÓ O MESTRE · as perguntas abertas, cada código ligado a um comando.
- **`turno.py fecha` recusa** se há: dado declarado sem rolar · luta aberta · blocos do dia que não fecham · nome fora da lista de gente · peça fora do Livro · item da caixa a um dia do prazo fora das perguntas · menos de 2 perguntas · invariante quebrado (moeda negativa, peça com dois donos, morto agindo). Passando, anda o mundo, gera o `RETOMAR.md`, faz commit e push, e avisa se o push falhou.
- **Ao abrir a sessão:** `CLAUDE.md` 2 KB · `MESTRE.md` 6 · `COLA.md` (gerada das tabelas) 8 · `RETOMAR.md` 6 · `MESA.md` 8. **Total: 30 KB.** O `REGRAS.md` vira consulta.

## 7. O que falta na luta

**A magia** usa a conta do aço: o foco é a arma, a guarda (armadura ou amuleto) é a armadura, e só a diferença de categoria conta. De seu ela dá alcance, área, controle, cura, clima e moral. Custa Mana (volta 1 por turno na luta, e o resto com descanso, oração ou o lugar, conforme a tradição) e ações; feitiço longo pode ser cortado por quem fere o mago. Sem amuleto, a armadura guarda 60% do valor contra a magia. **Encanto de peça:** um feitiço gravado, que sai uma vez por luta e vale um degrau abaixo da peça; contra um igual não decide, contra a multidão duas categorias abaixo limpa a casa. **Feita:** a regra em vigor está nos capítulos 10 a 16 do `REGRAS.md`; o `projeto/magia.md` é o rascunho antigo, guardado como história.
Padrões que valem se você não disser outra coisa: seis escolas para começar; a área fere amigo; a cura tem teto por dia e é presa à ferida mais funda; o retrochoque derruba.

**Os bichos:** o corpo é a arma e a armadura (garra Rara, couro Épico), com categoria como qualquer peça. O tamanho dá alcance, PV e quantos cabem no cerco. Traços saem de uma lista fechada que a luta sabe rodar. O núcleo do chefe é item contado.

**O ofício:** a seção 4, mais o sob medida (graus 1 a 4) e o conserto, que já estão no Livro de Itens.

## 8. Dados e scripts

`mundo/`: `relogio` · `lugares` (povo, estoque, produz, oficina, dano) · `rotas` · `ermos` (espécies contadas, masmorras) · `gente` (nomeados, rivais, você) · `guildas` · `frentes` · `missoes` · `caixa` · `noticias` · `oculto` · `diretor` · `turno_aberto` · `eventos.jsonl` (o único histórico; o diário sai dele). Os itens moram no `itens.json` do save (o `dados/itens.json` é só o Livro solto da luta fora do mundo).

Scripts novos, cerca de 5.500 linhas: `tabelas_mundo` · `estado` · `corpo` · `ato` · `oficio` · `bichos` · `mercado` · `viagem` · `gente` · `rivais` · `frentes` · `missoes` · `caixa` · `diretor` · `magia` e `tabelas_magia` · `turno` · `gera` · `cria` · `provas_mundo`. Sem argumento, todo script só imprime o uso.

## 9. O banco de provas do mundo

365 dias sem jogador, em 20 sementes. A semente que reprova não vira save.

1. Nenhum item da caixa vence sem resolução; nunca mais de 7 abertos.
2. Todo evento aplicou efeito; morto não age; estoque nunca negativo; a soma das moedas fecha.
3. Diretor neutro: estado final idêntico com ele ligado e desligado.
4. Rivais: de 10 a 30% morrem no ano, e entram outros tantos novos; o número de peças Épicas, Únicas e Lendárias em mãos vivas não cai; o líder do ranking troca de 1 a 6 vezes; nenhuma casa grande some sem um evento que a explique.
5. A primeira Épica nova do mundo sai entre os dias 40 e 110.
5b. **A história:** em 20 sementes, toda peça Única ou maior tem a cadeia de donos sem buraco; toda ruína tem origem; nenhuma pessoa viva é mais velha que o seu povo permite; toda casa viva tem pelo menos um herdeiro possível.
6. Das 12 frentes, de 3 a 6 chegam ao fim e de 2 a 5 são barradas.
7. Grão entre 0,6 e 2,2 vezes a base; fome em 20 a 60% dos mundos; no máximo 2 vilas perdidas.
8. A conta rápida erra menos de 8 pontos contra o `luta.py`.
9. **Robôs:** o ferreiro aplicado faz a primeira Épica entre os dias 60 e 85 e a primeira Única entre o 160 e o 220; o parado está abaixo da mediana dos da idade dele no dia 60; o afoito morre em 30 dias em 80% das sementes; o mudo perde por calar (a opinião média sobre ele cai, um rival fica com os clientes).
10. No dia 365, `RETOMAR.md` + `MESA.md` cabem em 14 KB; o ano roda em menos de 2 minutos; mesma semente, mesmo mundo.

## 10. As etapas

Cada etapa acaba em algo que se joga, com as suas provas passando. Cada uma é mais ou menos uma sessão longa de trabalho.

| Etapa | O que entra | O que se joga |
| --- | --- | --- |
| 1. Um dia numa vila **(FEITA: 12 de 12 no `provas_mundo.py`)** | o gravador, o relógio, o corpo, os atos, a ferida que dura, `abre` e `fecha` | trabalhar, comer, dormir, treinar, lutar |
| 2. Viver de um ofício **(FEITA: 80 de 80 no `provas.py`, com os bichos; 98 de 98 no `provas_mundo.py`; `estresse.py 1500` sem erro)** | estoque e preço, forjar e consertar, os bichos, a caça | viver de ferreiro ou de caçador. **A vila de teste** (fora do cânone): `vila_teste.py` e `GUIA_VILA.md` |
| 3. A região que responde **(FEITA, na etapa final: capítulos 21 a 23)** | mapa, viagem, nomeados com memória, notícia, caixa, missões | viajar, ter cliente, ter prazo |
| 4. A magia, os dons e as criaturas **(FEITA, antes da 3, por decisão do jogador (12.13): 114 de 114 no `provas.py`; 148 de 148 no `provas_mundo.py`, duas vezes; `estresse.py 1500` sem erro)** | os dons e os talentos em todo caminho; a magia na luta (quatro tradições, 24 feitiços e o truque, nove traços novos, as fases do chefe); a alquimia, o encanto e as maldições; estudar, o voto, o laço e o pacto; 19 criaturas, 5 chefes mágicos e os covis (capítulos 10 a 16 do `REGRAS.md`) | o mago, o clérigo, o druida, a bruxa, a poção, a maldição, a peça encantada, o goblin e a toca. **A vila de teste com a magia:** `vila_teste.py magia PASTA` |
| 4b. As masmorras e o mundo de fantasia **(FEITA, antes da 3, por decisão do jogador (12.16), e conferida pelo verificador independente: 114 de 114 no `provas.py`; 225 de 225 no `provas_mundo.py`, duas vezes; `estresse.py 1500` sem erro; a vila de teste ganha a etapa com `vila_teste.py fantasia`)** | as masmorras (salas, portas, armadilhas, o escuro, o tesouro e o chefe no fundo); o ladino (andar escondido, abrir fechadura, desarmar armadilha); os dragões de verdade, com covil e tesouro; os povos para o personagem (anão, elfo, meio-orc e outros da fantasia comum) | descer numa masmorra com um grupo, roubar o covil do dragão, nascer anão ou elfo |
| 5. A corrida **(FEITA, na etapa final: capítulo 24; a conta rápida erra 5 pontos)** | rivais, guildas, ranking, torneio, leilão, a janela do mundo | disputar |
| 6. O medo **(FEITA, na etapa final: capítulo 25)** | frentes, calamidade, a morte e o herdeiro, nêmesis, diretor | perder |
| 7. A história e o ano de prova **(FEITA, na etapa final: capítulos 26 e 27; o banco do ano passa em 20 sementes; o mundo de verdade é `mundo/`, semente 5)** | o gerador que roda de 400 a 1.000 anos, 20 sementes, a calibração, a criação do personagem dentro de uma casa | **o Dia 1** |

## 11. Riscos

1. **Afinar um mundo leva voltas.** É para isso que existem as sementes e os robôs. Todo número deste plano é meta, não fato, até o banco medir.
2. **Vivo no arquivo, morto na mesa.** A `MESA.md` traz sempre o que os nomeados lembram de você e dois fatos que não tocam você.
3. **Os moldes de frente acabam** em cerca de um ano de jogo. O chão gera frentes novas; e moldes novos entram como conteúdo, sem mexer em regra.
4. **O motor cresce** para umas 8.000 linhas. O gravador único, os invariantes do `fecha` e os dois bancos de provas são o que impede de virar remendo de novo.

## 12. As decisões do jogador (tomadas)

1. **A morte: vida única, com herdeiro.** (Seção 5.)
2. **Os rivais: aventureiros nativos, que morrem de vez.** (Seção 3.)
3. **O ritmo: o rápido.** A primeira Épica perto do dia 60, a Única do 160, e a primeira TENTATIVA de Lendária perto do 360, pelo melhor caminho. Os dias não são tranca: quem achar outro caminho chega antes (seção 4). A Lendária em si é rara de propósito (decisão 9).
4. **O começo: um mundo que já tem história,** de 400 a 1.000 anos, e o personagem nasce nele (seção 3, "A história").
5. **A vila de teste: sim.** Quando a etapa 2 ficar pronta, joga-se uma vila fora do cânone para sentir a luta e a forja. **Está pronta:** `vila_teste.py` e `GUIA_VILA.md`.
6. **O trabalho: com a frota de agentes** nas etapas grandes.
7. **Um contra dez com uma categoria de vantagem: fica moeda no ar.**
8. **O `main`:** o Motor 10 foi levado para o `main`. O save do Ferir, que seguiu em outro chat, não foi tocado.
9. **A Lendária é difícil de propósito.** A chance não sobe: a arma decide muito, e a melhor delas tem de custar. Uma tentativa são 243 blocos de bancada (cerca de 70 dias) e um núcleo Lendário; o dado rola uma vez, no fim; o melhor ferreiro possível acerta 1 em 4. A meta do banco é o dia em que a primeira tentativa fecha (Dia 356, no melhor caminho).
10. **A loja paga 40% pelas peças** (pelos bens, 60%). Forjar para a loja deixou de ser mina, e a espada tirada de um morto rende pouco.
11. **A caça de começo fica como está:** paga o mesmo que a diária e mata um em cada cinco por mês. Caçar é para quem aceita o risco.
12. **A vila de teste: o guerreiro** (Maro), na pasta `ensaio/`.
13. **A magia é a próxima etapa, antes da região,** e é central: "tem para todo lado: poções, maldições e magias de ataque e defesa". Entram junto os **dons e talentos** (para todo caminho: ferreiro, guerreiro, clérigo, druida, mago e outros) e as **criaturas mágicas** (orcs, goblins e outras, com chefes mágicos). O juízo e as respostas do jogador estão em `projeto/magia_etapa/DECISOES.md`; o contrato de construção, em `projeto/ETAPA_MAGIA.md`.
14. **Na magia:** qualquer um aprende; talento é pressa e teto, dom é poder; a Mana volta devagar na luta; a maldição pode matar (um teste por dia); quem não tem amuleto é guardado em 60% pela armadura; o Prodígio aprende com a metade dos blocos; o personagem nasce pelo dado, com uma inclinação escolhida; o veneno de lâmina existe e é crime nas vilas.
15. **A frota passa a ser enxuta:** o orquestrador julga os projetos; poucos construtores, um revisor e um verificador.
16. **Do mundo de Dungeons & Dragons, tudo entra no plano** (o jogador gosta muito do jogo): **as masmorras vêm antes da região** (etapa 4b), com **o ladino** (andar escondido, abrir fechadura, desarmar armadilha), **os dragões de verdade** (com covil e tesouro) e **os povos para o personagem** (anão, elfo, meio-orc e outros). Só entra o que é da fantasia comum ou inventado aqui: nada que seja criação exclusiva de um jogo ou de um livro (nem o nome, nem a aparência). O que é diferente de propósito continua: a peça pesa mais que o nível, aprende-se fazendo, e a vida é única.
17. **O conserto pago fica como está:** quem manda consertar espera na forja um bloco por peça.
18. **Na etapa 4b** (respostas E1 a E4): o golpe pelas costas do ladino entra; o personagem humano ganha uma segunda inclinação (escolher humano é aprender duas coisas depressa); o dragão que voa foge ferido fora do covil e luta até morrer dentro dele; o dragão jovem da vila de teste fica longe e só se conta. O juízo inteiro está em `projeto/etapa4b/DECISOES.md`.
19. **A luta à moda da mesa, só nas grandes** (resposta F1 b): na masmorra, na toca, contra chefe e contra dragão, o Mestre narra cada rodada e para em todo momento que decide, para o jogador escolher; nas caçadas de rotina, a luta corre rápida até o fim, com a ordem dada no começo. Os dados são os mesmos nos dois jeitos: muda só como a luta é contada.
20. **O personagem do jogador nasce no mundo novo** (`mundo/`), e não numa vila de teste: o jogador quis terminar o motor antes de começar o save (feito pela etapa final). **O personagem já está escolhido:** humano, de berço ferreiro, com a primeira inclinação na forja e a segunda no encanto ("algo de ferreiro e encantamento de itens"). **O Maro não é o personagem do jogador:** o `ensaio/` não se joga mais e fica só como vila de teste que os bancos copiam para conferir o motor (por isso ninguém escreve nele).
21. **Um projeto da etapa 3 feito noutro chat não foi construído** (`projeto/etapa3/`, guardado como história): o motor que vale é o da etapa final. As respostas que o jogador deu àquele projeto (R1 b, a estrada mais dura; R2 a, quem vai junto pede paga só no limite do perigo dele; R3 a, quem é pego furtando paga o triplo e quem guarda raiva não negocia mais; R4 a, o personagem só conhece o mapa que andou e o que lhe contaram) ficam escritas como gosto dele. A R1 b já está no motor da etapa final (a chance de encontro na estrada vai de 2% a 9% por bloco, acima do que aquele projeto propunha); as outras três entram se o jogador pedir, com o banco passando.

**O que estas decisões mudam no jeito do mundo:** não é um jogo com "jogadores" que renascem. É um mundo de verdade, velho, onde todo mundo morre uma vez. Ficam as leis dele: níveis, categorias de peça, a janela do item. Fica também a janela do mundo, como coisa que aquele mundo tem: quando uma peça Única nasce ou uma ruína é limpa pela primeira vez, todos ficam sabendo.

## 13. O que a etapa 2 deixou para o jogador decidir

Nada disto trava a etapa 3. São escolhas de gosto, que o banco mede mas não decide. A lista inteira, com os números, está no `MUDANCAS.md` e no fim do capítulo 9 do `REGRAS.md`.

1. **De onde vêm os núcleos da escada.** O ritmo decidido só vale com núcleo novo a cada obra, na melhor forja.
2. **A coleta de começo fica no zero a zero;** a de quem já tem mão, no interior, rende muito e não tem meta.
3. **A prata do lugar não se repõe,** e ninguém além do personagem compra da prateleira (a etapa 3 traz fregueses e comércio entre lugares).
4. **O atravessador de comida** (compra na colheita, vende na entressafra: 38 a 62% em meio ano, sem risco).
5. **Quem vai junto na caça** não pede paga: leva a parte dele do despojo. O que era de um morto não muda de mão sozinho: é decisão de cena.
