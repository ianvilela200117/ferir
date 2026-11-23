# Motor 10, Projeto A: gente primeiro

## 1. A ideia
1. O mundo é uma lista de pessoas com necessidade, vontade, rotina, laços e memória; cada uma age quatro vezes por dia.
2. Preço, perigo, missão e guerra saem do que elas fazem, não de tabela.
3. Você é um de 61 "jogadores" que entraram hoje; os outros não esperam.
4. Missão tem dono e prazo: se você falta, outro faz ou alguém paga.
5. O Mestre não lembra: lê uma página gerada do estado.

## 2. Tempo e corpo
**Relógio:** dia de 4 períodos de 6 h; estação de 13 semanas; ano de 364 dias. A estação dá colheita (grão ×3 no outono, ×0 no inverno), clima (vai ao `luta.py`) e luz.

**Ação** custa horas; a longa ("forjar 5 dias") PARA com item na caixa, perigo ou medidor em 75.

**Medidores, 0–100.** Fome: +3/h; refeição −40. Sono: +4/h acordado; cama −12/h, chão −8/h. Cansaço: trabalho +3/h, pesado +6/h, luta +10; descanso −5/h, sono −10/h.

**Pena do corpo:** 50 dá −1; 75, −3; 100, −5. Vale o pior medidor, +1 por outro em 50, em todo teste, acerto, Defesa e fôlego.

**Cura:** 5% do PV por noite dormida sem fome. Ferida fecha em 5 dias; a grave em 20, ou vira sequela (Vigor contra 24).

## 3. Mapa e viagem
**Grafo:** 22 lugares (capital de 4.000, 3 vilas de 1.000, 8 aldeias de 250, 8 masmorras, 2 ermos); 30 arestas de 15–120 km.

**Aresta:** `km`, `terreno` (estrada 30 km/dia, trilha 20, serra 12), `perigo` 0–10, `fechada_ate`. `perigo` só muda por fato: +1 por bando, −1 por 4 guardas, +2 com masmorra vizinha rugindo.

**Encontro:** por período na estrada, chance de perigo×4% (noite: dobro). Aparece quem ESTÁ na aresta.

**Notícia:** todo fato vira `noticia{dia origem peso certeza}` e anda com quem viaja. Cada salto tira 15 de certeza; abaixo de 40 é boato. Você só lê o `sabe` de onde está. A janela do Sistema avisa todos na hora (primeira limpeza, Lendária nova, ranking).

## 4. A gente
**NPC** (420 com nome; o resto é número por ofício):
```
id nome lugar oficio grau patrao nivel atributos maestria veste moedas coragem
nec{fome descanso seguranca dinheiro estima}   0–100
vontade{tipo alvo prazo progresso}             uma por estação
rotina[4] tracos[2] lacos{id:{afeto divida}} memoria[12]{dia quem fato peso} sabe[20] estado
```
**RIVAL** = NPC + `classe classe_oculta guilda estilo ambicao horas_dia xp fama alvo volta_em`.

**GUILDA:** `lider membros cofre fama dominio relacoes plano`.

**Escolha** a cada período: `nota = Σ nec[n]×alivio[acao][n]×peso_traco + 30×serve_vontade − risco×(100−coragem)/100`; faz a maior. O dado sai de (semente, dia, período, id): nunca se rola de novo.

**Por dia:** trabalha (enche o estoque do lugar), come (esvazia), conversa (troca notícia e afeto), viaja, treina, rouba, briga. O rival gasta `horas_dia` (6–16) em caça, masmorra, missão do MESMO quadro seu, forja, comércio, emboscada. XP do nível n: 30×n²; caça: 20×n/hora.

**Por semana:** patrão paga (senão: afeto −10 e o homem sai); guilda troca de plano (masmorra, guerra, leilão); vontade atrasada sobe o tom (empréstimo, missão no quadro, carta a você, roubo); `dinheiro` 90 por 3 semanas faz bandido ou migrante.

**Memória:** o fato soma peso (−10 a 10) no afeto; esfria 1 por semana; peso 8, nunca.

## 5. Economia
**Bens:** 12, do grão e do ferro à matéria Épica (acima, só leilão).

**Preço:** `base×(alvo/estoque)^0,5`, de 0,25 a 4 bases; `alvo` = 14 dias de consumo. O estoque só muda por agente: produção, consumo, caravana (do barato ao caro, se o lucro paga o perigo). Você compra a 1,1 e vende a 0,8, e mexe o estoque.

**Prata (p):** braçal 4 p/dia; artesão 12; comer 2; cama 2; espada Comum 60; cada categoria ×5. Moeda só nasce de cunhagem e prêmio do Sistema.

**Para viver:** jornal, aprendiz, obra, encomenda, caça, escolta, missão, despojo, comércio, oficina própria.

## 6. Fazer e conquistar
**Missão:** necessidade de um agente no quadro, paga do bolso DELE. Grau F a SS = categoria que o perigo pede. Caução 20%; prazo 3–14 dias. Vencida, o moleiro vai sem escolta e o dado decide.

**Masmorra:** 2 F, 1 E, 1 D, 2 C, 1 B, 1 A selada. O chefe veste a categoria do grau (C: Épico). `pressao` +1/dia; em 100 transborda sobre a aldeia vizinha; limpar zera. Primeira limpeza: peça da categoria.

**Ofício:** peça de categoria k (Comum 0, Lendário 5) pede grau k, 3 matérias k, forja nível k, 2^k dias e teste contra 20+4k. Falhou: perde 1 matéria e a peça sai uma abaixo.

**Mais:** torneio por estação, encomenda com sinal, leilão semanal, 12 classes ocultas.

**A escada** (dia da primeira peça):
- Rara, 20–35: grau 2; matéria no mercado.
- Épica, 70–110: matéria só de chefe C (20%; volta em 14 dias): 10 por ano para 61.
- Única, 250–400: chefe B (25%; 28 dias) ou a primeira limpeza: corrida.
- Lendária, 600–900: núcleo de um dos 3 grandes monstros, grau 5, técnica de missão oculta.

Teto no Dia 1: 3 Lendárias com dono, 1 Mítica selada, 0 Primordial.

**Falhar custa:** a matéria; a caução, fama −2×grau e a memória de quem pediu; o sinal em dobro; a morte.

## 7. O medo
**Nativo** morre para sempre; companheiro contratado é nativo.

**Você** volta em 48 h, no templo. Perde uma peça vestida (sorteio com peso pela categoria; um rival pode aparecer com a sua espada), as moedas do bolso (não as do banco) e 10% do XP; leva −2 por 3 dias. Nessas 48 h o mundo anda e a caixa se resolve sozinha.

**Ameaça:** `dono tipo passos[{condicao efeito dias}] passo relogio alvo`. É o plano de um agente: masmorra que transborda, bando, grande monstro, guilda hostil, caçador pago, peste.

**Você vê:** sinal (notícia com certeza), faixa (calma, inquieta, rugindo). **Oculto:** relógio, alvo, nível e peça do chefe, quem pagou o caçador. Investigar é ação com teste.

## 8. Do evento ao número
Só `fatos.aplica(evento)` muda o estado. Evento: `{dia hora tipo quem alvo lugar efeitos[{caminho op valor}]}`; `tipo` da tabela `EVENTOS`. Sem efeito, é recusado.

Aplicar muda o JSON, escreve em `fatos.jsonl` (único histórico; o diário sai dele), cria a notícia e grava a memória de quem viu.

O que o Mestre inventa entra por `transferir`, `laco`, `ferir`, `mover`, `saber` ou `promessa`. Fora disso, não aconteceu.

**Caixa de entrada:** `{de tipo chegou prazo opcoes[{cod texto efeitos}] padrao}`. Só escreve quem tem motivo no estado; promessa sua entra aqui. Vencido o prazo, o relógio aplica o `padrao`, com custo, e o `abre` conta. Máximo 7 abertos: o oitavo resolve o de menor peso.

## 9. Gerar mundo e personagem
`gera.py SEMENTE`, em ordem: mapa; 60 anos de história (3 lendas mortas, guerras velhas); povo (7.000 em número; 420 com nome, laço e dívida); estoques de 14 dias; masmorras; 60 rivais nível 1 e 8 guildas; 4 ameaças; 14 dias de aquecimento e provas curtas. Semente reprovada não vira save.

`cria.py`: origem (1 de 3 vilas); começo (ferreiro, guerreiro, caçador, mercador, andarilho); 405 pontos de atributo, mínimo 40; ofício grau 1; uma arma em Iniciante; peças Comuns, 30 p, 3 dias de comida; UM laço (o mestre que o acolhe) e UMA dívida (40 p).

## 10. O turno
`turno.py abre` só lê. Gera `ABERTURA.md` (até 8 KB): relógio e clima; corpo e bolso; quem está aqui (até 8: o que faz, quer e lembra de você); caixa por prazo e o que se resolveu sozinho; notícias e janelas; o que fazer aqui, com horas e preço; perigo conhecido; 5 linhas só para o Mestre; perguntas abertas, cada código ligado a um comando.

`responde "1a.2b"` confere os códigos e executa. `age ACAO horas=N` anda o mundo.

`fecha` RECUSA com: dado declarado sem rolar ou sem aplicar; nome novo fora do `gente.json`; relógio parado; menos de 2 perguntas; item da caixa a 24 h do prazo fora das perguntas; invariante quebrado (moeda negativa, peça com dois donos, morto agindo). Senão gera `RETOMADA.md`, faz commit e push, e avisa se o push falhou.

O Mestre lê ao abrir: `CLAUDE.md` 2 KB, `REGRAS.md` 14, `MUNDO.md` 10, `RETOMADA.md` 5, `ABERTURA.md` 8: **39 KB**.

## 11. Dados e scripts
`save/`: `mundo.json`, `lugares.json` (pop estoque sabe; arestas), `gente.json`, `guildas.json`, `itens.json` (Raro ou melhor; o resto no `veste`), `masmorras.json`, `ameacas.json`, `missoes.json`, `caixa.json`, `noticias.json`, `eu.json` (corpo oficio fama classe), `turno.json`, `fatos.jsonl`. Cada fato num lugar só: o dono da peça, só no `itens.json`.

Scripts e linhas (o nome diz o assunto; sem argumento, só imprimem o uso): `tabelas_mundo.py` 300; `estado.py` (dado por semente, invariantes) 250; `fatos.py` 300; `gera.py` 600; `gente.py` 550; `rivais.py` 450; `economia.py` 350; `mapa.py` 300; `poder.py` (luta rápida longe de você, medida do `luta.py`) 150; `fazer.py` (missão, masmorra, torneio, encomenda, leilão) 500; `ameacas.py` 250; `corpo.py` 150; `caixa.py` 200; `mundo.py` 250; `turno.py` 500; `cria.py` 200; `provas_mundo.py` 400. Total: 5.700.

## 12. Banco de provas
365 dias, sem jogador, 10 sementes.
1. Rivais: o primeiro no nível 60–85; mediana 30–45; o líder troca 3–10 vezes.
2. Peças: 6–14 Épicas novas, 0–2 Únicas, 0 Lendária; F a C limpas antes do dia 120; B em até 60% das sementes.
3. Grão: preço semanal em 0,5–2,5 bases em 95% das semanas; e há carestia (2 bases).
4. Ameaças: nascem 8–14; 25–45% chegam ao fim; a capital cai em até 5% das sementes.
5. Caixa (boneco mudo): 0 vencidos sem resolução; 0,5–1,5 chegadas por dia; nunca mais de 7 abertos.
6. Gente: morrem 3–8% dos nomeados; cada vila em ±20% de povo; nenhum morto age; a soma das moedas fecha.
7. Missões: rivais pegam 50–70%; toda vencida tem fato.
8. Máquina: `poder.py` erra até 8 pontos contra o `luta.py`; 365 dias em 90 s; `ABERTURA.md` até 8 KB; mesma semente, mesmo estado.

## 13. Construção e riscos
**Etapas:** E1 estado, fatos, corpo, turno, uma aldeia: joga-se um dia. E2 gera, gente, economia, mapa: vive-se de um ofício e viaja-se. E3 caixa, missões, notícia: prazos. E4 rivais, guildas, masmorras: a corrida. E5 ameaças, morte, torneio, classes ocultas: o medo. E6 dez sementes, calibração, Dia 1.

**Riscos:**
1. A emergência não fecha: 480 agentes dão preço louco ou parado, e parte do "emergente" acaba afinada à mão.
2. Vivo no JSON, morto na mesa: o Mestre vê uma fatia. A ABERTURA traz sempre 2 fatos que não tocam você.
3. A corrida desanda; não há elástico, só a matéria finita segura o topo.

**Fraquezas do ângulo:** rotina não dá enredo (por isso a ameaça tem molde escrito); cada agente é raso (5 necessidades, 2 traços); 93% do povo não é agente; erro de regra se espalha calado até o banco pegar.

## Escolhas do jogador
1. Morrer: a) volta com perda (seção 7); b) vida única; c) vida única só em zonas marcadas.
2. Rivais: a) "jogadores" que falam do jogo como jogo; b) aventureiros nativos.
3. Escada: a) a da seção 6; b) mais rápida; c) mais lenta.
4. Começo: a) o servidor abre hoje; b) você entra um ano atrasado.
