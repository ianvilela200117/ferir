# MOTOR 10 — O PROJETO DO RESTO

O núcleo está pronto e provado: a luta, os itens, a ficha que sai sozinha (`REGRAS.md`, 51 de 51 no banco de provas).
Este é o plano do que falta até o Dia 1 de um **mundo novo, do zero**: o mundo vivo, a magia, os bichos, o ofício e o turno.
Três projetos inteiros foram escritos de três ângulos (estão em `projeto/`, como rascunho). Aqui está o que ficou de cada um, com os números, as etapas e as seis decisões que são suas.

## 1. Em uma página

1. O mundo é uma região de **16 lugares** com estoque, gente, bichos e força contados. Um relógio só roda tudo, com você ou sem você.
2. Nele vivem **10.000 pessoas em número, 150 com nome e ficha, e 40 rivais** que começaram no mesmo dia que você e sobem a mesma escada pela mesma regra.
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

**Rivais.** 40 "jogadores" em 6 guildas e alguns sozinhos. Por semana escolhem um plano entre as mesmas missões, masmorras e leilões que você vê; por dia, executam. Compram no mesmo mercado. Longe de você a luta deles sai de uma conta rápida, calibrada contra o `luta.py` (erro menor que 8 pontos). O ranking sai toda semana.

**Economia.** Prata. Viver custa 3 por dia; o diarista ganha 4; o oficial, 12. Preço = base × √(alvo ÷ estoque), entre 0,4 e 3 vezes. **Toda compra mexe no estoque, a sua também.** Peça de loja: Comum 30, vezes 6 por categoria, até o Épico (6.480). De Único para cima não há loja: leilão, encomenda ou despojo.

**Frentes.** Doze no Dia 1 (4 ameaças, 4 ambições, 2 faltas, 2 mistérios), e o chão gera outras por limiar: grão abaixo de 10 dias, nasce a fome; ninhada acima do teto, nasce a praga. Cada uma rola por semana contra a resistência do lugar. Missão cumprida contra ela tira um passo; qualquer um pode cumprir. O passo 6 é o desfecho, sem volta.

**Notícia e janela.** Todo evento vira notícia, que anda uma rota por dia e vira boato depois do quarto salto. Você só lê o que chegou aonde está. A **janela do mundo** avisa a todos na hora: primeira limpeza de masmorra, peça Única ou maior, classe oculta achada, frente que acaba.

**A caixa.** `{de, pede, prazo, opções, padrão}`. Só escreve quem tem motivo no estado. Vencido o prazo, vale o padrão, sempre com custo (o cliente vai ao rival; a opinião cai). Cabem 7; o oitavo força o mais velho.

## 4. A conquista, em números

O item decide a luta; por isso a escada das peças É a escada do poder, e ela é trancada pelo que existe no mundo.

| Categoria | Dia da primeira (jogando bem) | Quantas no Dia 1 | O que tranca |
| --- | --- | --- | --- |
| Incomum | 8 a 15 | à venda | dinheiro: 180 de prata |
| Raro | 30 a 45 | 60 | material de masmorra ou de bicho contado; ofício Treinado; forja de cidade |
| Épico | 90 a 130 | 12 | núcleo de chefe (nascem 4 por ano no mundo todo); 27 blocos de forja |
| Único | 240 a 330 | 4 | núcleo de chefe maior (1 por ano) ou primeira limpeza; 81 blocos; Mestre |
| Lendário | 540 a 720 | 3, com as Lendas | núcleo de calamidade; 243 blocos (40 dias); o melhor ferreiro acerta 1 em 5 |
| Mítico | depois do ano 2 | 1, dormindo | |
| Primordial | talvez nunca | 0 | |

**Forjar:** material da categoria (do Épico para cima, um núcleo, que é item contado, com dono e lugar) + tempo de 3^categoria blocos + teste: 2d20 + maestria + Afinidade ÷ 10 + oficina (0 a 4) + preparo (até +8, cada +2 ganho no mundo: receita, ajudante, fogo, bigorna) contra 28 + 6 por categoria.
**Falhar custa:** por menos de 5, a peça sai uma categoria abaixo; por 5 ou mais, o material some. Missão falhada: a caução, a fama, e o dano acontece. Masmorra: a morte.
**Consertar** devolve a durabilidade (2% do preço por ponto). Toda luta gasta 1 de cada peça usada: o ferreiro tem serviço.

## 5. O medo

- **O nativo morre de vez.** Companheiro contratado é nativo.
- **A sua morte** é a primeira decisão da seção 11. A que recomendo: você acorda 3 dias depois no templo; a **melhor peça vestida fica com quem matou** (e pode ser retomada); perde o que carregava e um décimo dos níveis; os 3 dias correm sem você, e a caixa se resolve sozinha. Como o item decide, perder a peça é perder o degrau.
- **O nêmesis:** quem derruba você, ou pega a sua peça, vira uma frente pessoal.
- **Você vê** os sinais que a notícia trouxe, os prazos, o perigo das estradas que andou. **Fica oculto** o relógio de cada frente, a força, o chefe, os planos dos rivais, onde estão os núcleos. Investigar é ação com teste, e abre um campo por vez.
- **O diretor** só escolhe quais frentes entram em cena no dia (até 3). Não toca em dado, relógio nem estoque: o banco prova que o estado final é idêntico com ele ligado e desligado. Depois de queda ou peça perdida, ele não empilha ameaça; mas também não inventa alívio que não exista.

## 6. Como o Mestre não esquece

- **Um gravador só** (`estado.aplica`). Evento = `{dia, tipo, onde, quem, efeitos}`, com efeitos de 12 verbos fechados (estoque, preço, rota, perigo, povo, pessoa, laço, fama, item, frente, missão, caixa). Sem efeito, é recusado. A frase da mesa e a notícia saem dos efeitos.
- **Cada fato num lugar só.** O dono da peça está só no Livro de Itens; onde a pessoa está, só na ficha dela.
- **`turno.py abre`** só lê, e gera a `MESA.md` (até 8 KB): relógio e tempo · corpo e bolso · quem está aqui (o que faz, o que quer, o que lembra de você) · a caixa por prazo · notícias chegadas · o que dá para fazer aqui, com blocos e preço · a pauta do diretor · dois fatos que não tocam você · SÓ O MESTRE · as perguntas abertas, cada código ligado a um comando.
- **`turno.py fecha` recusa** se há: dado declarado sem rolar · luta aberta · blocos do dia que não fecham · nome fora da lista de gente · peça fora do Livro · item da caixa a um dia do prazo fora das perguntas · menos de 2 perguntas · invariante quebrado (moeda negativa, peça com dois donos, morto agindo). Passando, anda o mundo, gera o `RETOMAR.md`, faz commit e push, e avisa se o push falhou.
- **Ao abrir a sessão:** `CLAUDE.md` 2 KB · `MESTRE.md` 6 · `COLA.md` (gerada das tabelas) 8 · `RETOMAR.md` 6 · `MESA.md` 8. **Total: 30 KB.** O `REGRAS.md` vira consulta.

## 7. O que falta na luta

**A magia** usa a conta do aço: o foco é a arma, a guarda (armadura ou amuleto) é a armadura, e só a diferença de categoria conta. De seu ela dá alcance, área, controle, cura, clima e moral. Custa Mana (que só volta com descanso) e ações; feitiço longo pode ser cortado por quem fere o mago. **Encanto de peça:** um feitiço gravado, que sai uma vez por luta e vale um degrau abaixo da peça; contra um igual não decide, contra a multidão duas categorias abaixo limpa a casa. O rascunho inteiro está em `projeto/magia.md` (os números dele são de antes da revisão do núcleo e serão refeitos).
Padrões que valem se você não disser outra coisa: seis escolas para começar; a área fere amigo; a cura tem teto por dia e é presa à ferida mais funda; o retrochoque derruba.

**Os bichos:** o corpo é a arma e a armadura (garra Rara, couro Épico), com categoria como qualquer peça. O tamanho dá alcance, PV e quantos cabem no cerco. Traços saem de uma lista fechada que a luta sabe rodar. O núcleo do chefe é item contado.

**O ofício:** a seção 4, mais o sob medida (graus 1 a 4) e o conserto, que já estão no Livro de Itens.

## 8. Dados e scripts

`mundo/`: `relogio` · `lugares` (povo, estoque, produz, oficina, dano) · `rotas` · `ermos` (espécies contadas, masmorras) · `gente` (nomeados, rivais, você) · `guildas` · `frentes` · `missoes` · `caixa` · `noticias` · `oculto` · `diretor` · `turno_aberto` · `eventos.jsonl` (o único histórico; o diário sai dele). Os itens seguem em `dados/itens.json`.

Scripts novos, cerca de 5.500 linhas: `tabelas_mundo` · `estado` · `corpo` · `ato` · `oficio` · `bichos` · `mercado` · `viagem` · `gente` · `rivais` · `frentes` · `missoes` · `caixa` · `diretor` · `magia` e `tabelas_magia` · `turno` · `gera` · `cria` · `provas_mundo`. Sem argumento, todo script só imprime o uso.

## 9. O banco de provas do mundo

365 dias sem jogador, em 20 sementes. A semente que reprova não vira save.

1. Nenhum item da caixa vence sem resolução; nunca mais de 7 abertos.
2. Todo evento aplicou efeito; morto não age; estoque nunca negativo; a soma das moedas fecha.
3. Diretor neutro: estado final idêntico com ele ligado e desligado.
4. Rivais: o primeiro entre os níveis 55 e 85; de 2 a 5 com peça Épica; no máximo 1 com Única; nenhum com Lendária; o líder do ranking troca de 3 a 10 vezes.
5. A primeira Épica nova do mundo sai entre os dias 80 e 140.
6. Das 12 frentes, de 3 a 6 chegam ao fim e de 2 a 5 são barradas.
7. Grão entre 0,6 e 2,2 vezes a base; fome em 20 a 60% dos mundos; no máximo 2 vilas perdidas.
8. A conta rápida erra menos de 8 pontos contra o `luta.py`.
9. **Robôs:** o ferreiro aplicado faz a primeira Épica entre os dias 90 e 130 e nenhuma Única antes do 240; o parado está abaixo da mediana do ranking no dia 60; o afoito morre em 30 dias em 80% das sementes; o mudo perde por calar (a opinião média sobre ele cai, um rival fica com os clientes).
10. No dia 365, `RETOMAR.md` + `MESA.md` cabem em 14 KB; o ano roda em menos de 2 minutos; mesma semente, mesmo mundo.

## 10. As etapas

Cada etapa acaba em algo que se joga, com as suas provas passando. Cada uma é mais ou menos uma sessão longa de trabalho.

| Etapa | O que entra | O que se joga |
| --- | --- | --- |
| 1. Um dia numa vila **(FEITA: 12 de 12 no `provas_mundo.py`)** | o gravador, o relógio, o corpo, os atos, a ferida que dura, `abre` e `fecha` | trabalhar, comer, dormir, treinar, lutar |
| 2. Viver de um ofício | estoque e preço, forjar e consertar, os bichos, a caça | viver de ferreiro ou de caçador. **Aqui cabe uma vila de teste** |
| 3. A região que responde | mapa, viagem, nomeados com memória, notícia, caixa, missões | viajar, ter cliente, ter prazo |
| 4. A magia | focos, feitiços, encantos de peça | o mago, o curandeiro, a peça encantada |
| 5. A corrida | rivais, guildas, masmorras, ranking, torneio, leilão, a janela do mundo | disputar |
| 6. O medo | frentes, calamidade, morte, nêmesis, diretor | perder |
| 7. O ano de prova | o gerador em 20 sementes, a calibração, a criação do personagem | **o Dia 1** |

## 11. Riscos

1. **Afinar um mundo leva voltas.** É para isso que existem as sementes e os robôs. Todo número deste plano é meta, não fato, até o banco medir.
2. **Vivo no arquivo, morto na mesa.** A `MESA.md` traz sempre o que os nomeados lembram de você e dois fatos que não tocam você.
3. **Os moldes de frente acabam** em cerca de um ano de jogo. O chão gera frentes novas; e moldes novos entram como conteúdo, sem mexer em regra.
4. **O motor cresce** para umas 8.000 linhas. O gravador único, os invariantes do `fecha` e os dois bancos de provas são o que impede de virar remendo de novo.

## 12. As decisões que são suas

1. **A sua morte.** a) acorda em 3 dias e perde a melhor peça vestida, o que carrega e um décimo dos níveis (recomendo: é o Satisfy, e dói) · b) vida única, com herdeiro · c) três vidas.
2. **Os rivais.** a) "jogadores" como você: falam do jogo como jogo e voltam quando morrem (recomendo) · b) aventureiros nativos, que morrem de vez.
3. **O ritmo da escada** (o dia da primeira Épica, Única e Lendária, jogando bem). a) rápido: 60, 160, 360 · b) médio: 90, 240, 540 (recomendo) · c) lento: 150, 375, 850.
4. **O começo.** a) o mundo abre no seu Dia 1, todos no nível 1 (recomendo) · b) você chega um ano atrasado, com os outros na frente.
5. **A vila de teste.** a) quando a etapa 2 ficar pronta, você joga uma vila fora do cânone, para sentir a luta e a forja e mandar mudar o que não gostar (recomendo) · b) só o Dia 1, com tudo pronto.
6. **Como eu trabalho.** As duas frotas de agentes que usei gastaram, cada uma, uma janela inteira do seu limite de uso. a) sigo sozinho, etapa por etapa: mais lento, bem mais barato (recomendo) · b) uso a frota de novo nas etapas grandes.
