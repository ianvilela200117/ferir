# MUNDO C — drama primeiro: frentes e diretor

## 1. A ideia em cinco linhas
1. O mundo são 12 FRENTES: ameaças, ambições e faltas, com dono, meta e relógio de 6 passos. Cada passo muda número.
2. Elas andam por dado, com ou sem o personagem, e nasceram sem ele.
3. Dezesseis RIVAIS sobem a mesma escada pela mesma regra. As peças altas são contadas: o que um leva, acabou.
4. Um DIRETOR escolhe o que entra em cena. Não toca em dado, relógio nem estoque.
5. O que toca o personagem cai numa CAIXA com prazo. Calar tem preço escrito.

## 2. O tempo e o corpo
- Dia: 6 blocos de 4 horas. Semana: 7 dias. Estação: 13 semanas. Toda ação custa blocos. Inverno: sem colheita, e +1 bloco por aresta.
- Medidores de 0 a 10:
  - **Fome:** +1 a cada 2 blocos; refeição −3. Em 4: −2 em todo teste. Em 7: −4 e −5% do PV máximo por dia.
  - **Sono:** +1 por bloco acordado; −3 por bloco dormido. Em 6: −2. Em 8: −4, e dorme ali se falhar Vontade contra 28.
  - **Cansaço:** bloco pesado (marcha, forja, luta) +2; leve +1; sono −3. Cada 3 pontos tiram 1 do fôlego máximo. Em 9: −2 em tudo.
  - **Ferida** (REGRAS 3.10): sara em 7 dias; grave, em 21. Dia com 2 blocos pesados não conta. PV: +10% do máximo por noite dormida.

## 3. O mapa e a viagem
- Grafo: 3 regiões, 24 lugares (3 cidades, 6 vilas, 8 masmorras, 7 ermos), 34 arestas com `blocos` (1 a 6), `perigo` (0 a 5) e `aberta`.
- Encontro: por bloco de viagem, 5% por ponto de perigo (+5% à noite), da tabela do lugar (bicho, viajante, bandido, rival, achado). As frentes mudam `perigo` e `aberta`.
- Notícia: todo evento gera uma. Anda 1 aresta aberta por dia e perde precisão do 4º salto em diante. O personagem só lê as que chegaram aonde está.
- Anúncio do mundo (janela do sistema): chega a todos no dia. Só para primeira limpeza de masmorra, peça Única ou maior, classe oculta achada e frente que acaba.

## 4. A gente
- **NPC** (120 com ficha; o resto é `pop`): `id, nome, lugar, oficio, nivel, atributos, equip[], moedas, rotina[6], quer{tipo,alvo,prazo}, lacos{id:-5..5}, opiniao{valor,porque[]}, estado[], frente`.
- **RIVAL** (16) = NPC mais `classe, estilo, ambicao, fama, guilda, plano{alvo,passo,fim}, ousadia, rancor, trunfo` (oculto).
- **GUILDA** (4): `mestre, membros[], cofre, fama, sede, dominio[], politica`.
- **Por dia:** o NPC cumpre a rotina, produz para o estoque e come. O rival faz uma ação do plano (treinar, caçar, forjar, comerciar, cumprir missão). A expedição sai da conta rápida: 2d20 + `poder` contra `30+12×grau`, com `poder = nível÷5+12×categoria+maestria`. Falhou: ferido 1d6 dias. Por 10 ou mais: morre (seção 7).
- **Por semana:** o NPC resolve o `quer` (vender, mudar-se, casar, vingar), que mexe em laço, lugar ou moeda. O rival passa ao degrau seguinte. A guilda paga soldo, recruta, compra (o preço sobe) e disputa masmorra, onde cobra pedágio.

## 5. A economia
- Moeda: prata (P). Ração 1 por dia; pousada 2; diarista ganha 4; mestre de ofício 20.
- Dez bens com estoque por lugar, do grão ao remédio. O estoque muda por produção, consumo (grão: `pop÷100` por dia), caravana semanal por aresta aberta e frente.
- Preço: `base×√(alvo÷estoque)`, entre 0,4 e 3 vezes. A loja paga 60%. Toda compra mexe no estoque, a do jogador também.
- Peça: 30 P, vezes 6 por categoria. Lendária não tem preço. Conserto: 2% por ponto.
- Para viver: diária, ofício, encomenda, caça, missão, comércio de estrada, torneio, soldo.

## 6. As coisas para fazer e a escada
- **Missão:** graus F a SS, casados com a categoria (D Incomum, C Raro, B Épico, A Único, S Lendário). Tem `grau, de, prazo, alvo` (predicado do estado), `paga` (metade do preço da categoria), `falha[]`. Nasce de passo de frente ou de `quer`. Quem cumpre primeiro, leva.
- **Masmorra:** grau, 3 a 9 andares, chefe; reabre em 28 dias. A primeira limpeza dá o núcleo e o anúncio; as seguintes, material uma categoria abaixo.
- **Forja:** a obra não passa da categoria do material; do Épico para cima, o material é um núcleo. Teste: 2d20 + maestria + `Afinidade÷10` + oficina (0 a 4) + preparo, contra `28+6×categoria`. Tempo: `3^categoria` blocos (1 a 243). Preparo: cada +2 se ganha no mundo (receita, ajudante, fogo, bigorna), até +8.
- Mais: encomenda sob medida com prazo; torneio por estação; 8 classes ocultas, de um dono só, com gatilho oculto.
- **A escada.** Núcleo é item contado, com `onde`; nascem 4 Épicos e 1 Único por ano. Dia-alvo, quantas há no Dia 1, o que tranca:
  - Incomum, dia 10: à venda; 180 P.
  - Raro, dia 30: 60 peças; masmorra C ou ofício Treinado.
  - Épico, dia 90: 12 núcleos; chefe B; 27 blocos.
  - Único, dia 240: 4 núcleos; chefe A; 81 blocos.
  - Lendário, dia 540: 3 com as Lendas, 1 núcleo; 243 blocos; o melhor ferreiro acerta 23%.
  - Mítico, depois do ano 2: 1, dormindo.
- **Falhar:** obra que falha por menos de 5 sai uma categoria abaixo; por mais, o material some. Missão: os efeitos de `falha`. Masmorra: a morte.

## 7. O medo
- **Morte.** NPC morre de vez. Rival e personagem voltam e pagam: 10% dos níveis; metade das moedas; a peça de maior categoria cai e fica no Livro, sem dono; 3 dias fora, com o mundo andando. Quem vence o personagem ou pega a peça caída ganha `rancor` e vira frente pessoal: o nêmesis.
- **Ameaça:** cada frente rola por semana 2d20 + `forca` contra a `resistencia` do lugar (30 + guarda + obras). Passou: +1 passo, com os efeitos. O passo 6 é o desfecho, sem volta. Missão cumprida contra ela: −1 passo. Rivais e NPCs também cumprem.
- **Vê-se:** o sinal de cada passo que a notícia trouxe, os prazos, o perigo das estradas andadas, os graus. **Oculto:** o relógio, o `trunfo`, os gatilhos, onde estão os núcleos.
- **Diretor:** `tensao` de 0 a 10 (+2 ferida grave, queda ou peça perdida; +1 passo que toca o personagem; −2 missão cumprida ou obra feita; −1 dia calmo). Pauta: até 3 frentes por dia, por `nota = 2×passo + 2×max(0,4−saltos) + laço + dias_sem_cena÷3`. Tensão 7 ou mais: uma ameaça só, mais um respiro real pendente; não havendo, nada se inventa. Tensão 2 ou menos por 5 dias: entra o sinal da ameaça de maior nota.

## 8. Do evento ao número, e a caixa
- Evento = `{id, dia, tipo, onde, quem[], efeitos[]}`. Os efeitos saem de 12 verbos fechados: `estoque, preco, rota, perigo, pop, npc, laco, fama, item, frente, missao, caixa`. O `eventos.py` recusa evento sem efeito. A frase da mesa e a notícia são geradas dos efeitos.
- **Caixa:** `{id, de, pede, prazo, opcoes[{cod,efeitos}], padrao}`. Prazo de 1 a 14 dias. Vencido, vale a `padrao`: a pior para quem calou. Cabem 7; o oitavo força o mais velho.

## 9. Gerar o mundo e o personagem
- `gera_mundo.py SEMENTE`, nesta ordem: mapa; bens e estoques; população e 120 NPCs; itens e núcleos; 8 masmorras (graus D a S); 16 rivais e 4 guildas; 3 Lendas; 8 classes ocultas; 12 frentes (4 ameaças, 4 ambições, 2 faltas, 2 mistérios) de 20 moldes; 30 dias de aquecimento sem jogador; provas rápidas.
- **Personagem:** nível 1, sem classe. Atributos 50, mais 60 pontos. Uma origem entre seis (aprendiz de ferreiro, caçador, recruta, mascate, noviço, mineiro) dá ofício Iniciante, peças Comuns, 30 P e um item na caixa.

## 10. O laço do turno
- `turno.py abre` só lê. Mostra, em dois blocos (MESA e SÓ MESTRE): relógio, corpo, quem está aqui, a caixa, a pauta do diretor com o motivo, notícias chegadas, preços que mudaram, missões, perguntas abertas. Até 6 KB.
- No meio: `ato.py` (toda ação, com blocos), `teste.py`, `luta.py`. Tudo grava em `turno_aberto.json`.
- `turno.py fecha` recusa se há: código do jogador sem pergunta aberta; dado sem registro; blocos do dia que não fecham; alguém citado sem id; peça fora do Livro; menos de 2 perguntas novas; prova rápida quebrada. Depois resolve a caixa vencida, anda o mundo, gera o `RETOMAR.md` e guarda no git.
- **Abrir a sessão:** `CLAUDE.md` 2 KB, `MESTRE.md` 6, `COLA.md` (gerada das tabelas) 8, `RETOMAR.md` 6, saída do `abre` 6. Total: 28 KB.

## 11. Dados e scripts
- JSON em `mundo/`: `relogio`, `mapa` (lugares, arestas), `gente`, `rivais`, `personagem` (atributos, corpo, lugar, moedas, fama, oficios), `frentes` (dono, meta, relogio, passos[6]{sinal,efeitos}, forca), `masmorras`, `missoes`, `caixa`, `noticias`, `diretor` (tensao, pauta), `turno_aberto`, `eventos.jsonl`. Os itens seguem em `dados/itens.json`.
- Scripts (linhas): `tabelas_mundo.py` 250; `gera_mundo.py` 450; `mundo.py` 400; `gente.py` 450; `frentes.py` 300; `eventos.py` 250; `caixa.py` 150; `diretor.py` 200; `ato.py` 400; `oficio.py` 250; `missoes.py` 250; `turno.py` 350; `provas_mundo.py` 350. Cerca de 4.050.

## 12. O banco de provas do mundo
365 dias, 20 sementes, sem jogador:
1. Nenhum item da caixa vence sem resolução.
2. Todo evento aplicou um efeito; morto não age; estoque nunca negativo.
3. Diretor neutro: estado final idêntico, fora o `diretor.json`, com ele ligado e desligado.
4. De 16 rivais, 2 a 5 têm peça Épica; no máximo 1, Única; nenhum, Lendária; o maior nível fica entre 60 e 90.
5. O primeiro Épico novo sai entre os dias 70 e 130.
6. Das 12 frentes, 3 a 6 chegam ao fim; 2 a 5 são barradas.
7. Grão: preço entre 0,6 e 2,2 vezes a base; fome em 20 a 60% dos mundos.
8. Os rivais fazem 30 a 70% das primeiras limpezas.
9. A conta rápida erra menos de 10 pontos contra o `luta.py`.
10. No dia 365, `RETOMAR.md` mais `abre` cabem em 14 KB.

## 13. A ordem de construção e os riscos
1. Relógio, corpo, 8 lugares, `ato.py`, `abre` e `fecha`. Joga-se: trabalhar, comer, dormir, viajar, lutar.
2. Estoque, preço, `oficio.py`, encomendas. Joga-se: viver de ferreiro.
3. NPCs com rotina, eventos, notícias, caixa. Joga-se: uma vila que responde.
4. Frentes, missões, diretor, morte. Joga-se: o medo.
5. Rivais, guildas, masmorras, torneios, classes ocultas. Joga-se: a corrida.
6. Gerador de 3 regiões e banco de 365 dias. Só então, o Dia 1.

Riscos (onde este ângulo é fraco):
- **Os moldes acabam.** Vinte moldes, com dono e lugar sorteados, dão cerca de um ano sem repetição. Depois é trabalho de autor.
- **O diretor não garante nada.** Ele só mostra. Azar em série não tem alívio. E escolher o que mostrar já puxa a decisão do jogador.
- **Todo número aqui é palpite até ser jogado.** O banco calibra, mas mede rivais, não gente.

## Escolhas do jogador
1. **A morte:** como na seção 7 (recomendo); definitiva, com herdeiro; ou branda, sem cair peça.
2. **O ritmo:** a primeira Lendária perto do dia 540 (recomendo), do 270 ou do 810.
3. **A janela do mundo:** anúncio à vista de todos (recomendo), ou tudo só por estrada.
4. **O relógio das ameaças:** só os sinais (recomendo), ou a barra de 6 passos à vista.
