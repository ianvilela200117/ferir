# MOTOR 10 — MUNDO B: SISTEMAS PRIMEIRO

## 1. A ideia em cinco linhas
1. O mundo é um grafo de lugares com **estoque, gente, bichos e força**. Um relógio (`mundo.tick`) roda tudo, com ou sem o personagem.
2. **Evento é limiar cruzado**, não sorteio: grão abaixo de 10 dias, nasce a fome.
3. Gente e rivais vivem **dentro dos sistemas**: mesmo estoque, mesmo preço, mesmas masmorras, mesmo `luta.py`.
4. O personagem é **uma linha entre 161**. O que ele não faz, outro faz e leva a fama, ou o lugar paga.
5. O raro é **contável**. O que um rival pega saiu do mundo.

## 2. O tempo e o corpo
- **Bloco** = 4 h, 6 por dia. Semana 7 dias; estação 91; ano 364.
- **Estações:** colheita × 0,5 · 1 · 2,5 · 0. Inverno: viagem × 1,5, lenha × 3. O clima do dia entra no `TEMPO` da luta.
- **Corpo** (`corpo.py`; 0 a 100), somado à ficha de luta:
  - **Fome:** +5 por bloco; refeição −15 (2 c × índice do grão). 60: −1 nos testes. 85: −3, fôlego −2. 100: −5% do PV por dia.
  - **Sono:** +15 por bloco acordado; dormido −30. 70: −2. 90: −4, e Vontade contra 26 ou dorme.
  - **Cansaço:** braçal +15, viagem +10, luta +10 e +2 por rodada; sono −30. 50: fôlego −2. 80: fôlego −4, testes −2.
  - **Ferida** (a do `luta.py`): fecha em 10 dias; grave, 30; com curandeiro, metade. PV: +10% por noite.

## 3. O mapa e a viagem
- Uma região: **14 lugares** (1 capital, 2 cidades, 5 vilas, 6 postos), 6 ermos, 8 masmorras (3 a 9 andares), 20 rotas.
- Rota: 2 a 12 blocos a pé.
- `perigo = 0,5 × pressão do ermo + 2 × bando − 10 × patrulha`. Com 70, caravana não passa.
- **Encontro** por bloco: perigo ÷ 400 (noite × 2). Quem aparece sai da contagem real do ermo ou do bando.
- **Notícia:** evento de `peso` 1 a 5 chega em `dia + distância ÷ 3` e não passa de `peso × 8` blocos. Calcula-se do registro; o personagem só lê o que chegou.

## 4. A gente
- **Povo** (9.000): contagem por lugar e ofício. Come, produz, migra (1% por semana), morre de fome (2%). Faminto sem ofício engrossa o bando.
- **Nomeado** (120): `id, nome, lugar, oficio, patrao, nivel, atributos, maestria, equip[], dinheiro, corpo, rotina{bloco: ponto}, quer{tipo, alvo, ate}, lacos{id: -100..100}, opiniao_pj, vivo`. Por dia: rotina, trabalho, comida ao preço do dia. Por semana: `quer` sai da maior falta (fome, dívida, medo, ambição, laço) e vira ato com efeito: migra, encomenda, denuncia, entra num bando.
- **Rival** (40 "jogadores"; 6 guildas): mais `classe, guilda, xp, fama, ousadia, plano{atividade, alvo, ate}, grupo[], feitos[]`. Por semana: escolhe o plano de maior `ganho × chance − risco × (1 − ousadia)` entre as missões, masmorras e leilões que o personagem vê. Por dia: executa; a luta roda no `luta.py`; compra no mercado real.
- **Guilda, facção:** `id, membros, cofre, fama, sede, territorio[], rumo, rel{}`. Por semana: recruta, paga, toma masmorra (pedágio), disputa material, enfrenta ou ignora ameaça.
- **Ranking** semanal, com quem passou o personagem.

## 5. A economia
- Cobre (c); prata = 100 c; ouro = 100 pratas. Doze bens, do grão ao ferro.
- `preço = base × (alvo ÷ estoque)^0,6`, de 0,3 × a 5 ×; `alvo` = 30 dias de consumo. Compra +10%, venda −10%. **Toda compra mexe no estoque.**
- Produção = `produz × estação × braços × (1 − dano)`. Caravana semanal leva do barato ao caro; assaltada, a carga vira força do bando.
- Viver: 7 c por dia. Braçal 8; aprendiz 15; oficial 40; escolta 20.
- Peça de loja: Comum 60 c, × 6 por categoria, até Épico. De Único para cima: leilão, encomenda, despojo.
- **Para viver:** braço, ofício por peça, caça, coleta, mina, comércio, escolta, missão, torneio.

## 6. As coisas para fazer e a escada
- **Missões** nascem do estado (grão abaixo de 20 dias: escolta; bando acima de 30: caçada). `grau` F a SS = a categoria do que se enfrenta. Paga uma peça de loja um grau abaixo. Rivais aceitam também.
- **Ocultas** (classe, título): gatilhos conferidos pelo script a cada evento.
- **Forja:** 3 materiais da categoria + teste contra `22 + 4 × categoria` (Comum 0). Soma: maestria (0 a 8), bônus da ferramenta, oficina (vila 0, cidade 2, capital 4). Maestria: Iniciante 30 dias de bancada; Treinado 120; Mestre 400 e uma obra.
- **Masmorra:** a primeira limpeza de cada andar paga uma vez no mundo. **Torneio** por estação; **leilão** mensal.
- **A escada** (dia da primeira peça; o que trava):
  - Incomum, 5 a 15: dinheiro.
  - Raro, 30 a 60: 60 bichos vivos; forja de cidade.
  - Épico, 120 a 200: 8 bichos, 1 novo a cada 45 dias; 12 peças no mundo.
  - Único, 300 a 450: 2 bichos, 1 novo a cada 180 dias; 3 peças; a forja da coroa (fama 60) ou a sua (5 ouros e um núcleo).
  - Lendário, 700 a 1.000: 1 peça; núcleo só de calamidade.
  - Mítico e Primordial: ano 4 em diante, talvez nunca.
- **Falhar custa.** Forja: por 1 a 4, sai uma categoria abaixo; por 5 ou mais, o material some. Missão: caução de 20%, fama −2 × grau, e o dano acontece. Torneio: ferida e a peça apostada.

## 7. O medo
- **Morte.** Nativo: final. "Jogador" (personagem e rivais): acorda 3 dias depois no templo; perde a **melhor peça vestida** (fica com quem matou; pode ser retomada), a moeda, a carga e 3 níveis. Os 3 dias correm sem ele.
- **Ameaça:** nasce de limiar (ninhada, bando, fome) ou da **calamidade** semeada (5 etapas em 2 anos). `etapa, forca, alvo, chefe, proximo_passo, ritmo (10 a 30 dias), sinais[]`. Etapa 2: rota +20. 3: o alvo perde 20% da gente. 4: o lugar cai, com a loja e a gente. 5: novo alvo. Contida (força aplicada ≥ a dela), recua; quem conteve leva fama e despojo.
- **O jogador vê** os sinais (notícia atrasada), o aviso a um passo, o corpo, a caixa. **Oculto** (`oculto.json`): força, etapa, data, chefe, planos dos rivais. Investigar (contra 26, 30, 34) abre um campo.

## 8. Do evento ao número
- Evento = `{id, dia, bloco, tipo, lugar, quem[], efeitos[], peso}`. Efeito é operação tipada: `["estoque","vila3","grão",-40]`, `["vivo","g031",false]`.
- `estado.aplica()` é a **única** função que grava. Evento sem efeito é recusado. O texto sai de molde.
- Fato criado em cena (promessa, dívida) entra por `fato.py`, com efeito e data.
- **Caixa** (só o que é dele): `{id, nasce, prazo, de, tipo, opcoes[{cod, efeitos}], padrao, peso}`. Prazo: convite 2 dias, encomenda 3, desafio 5. Vencido, vale `padrao`, **sempre com custo** (o cliente vai ao rival: opinião −5, o rival sobe). Teto de 7 abertos.

## 9. Gerar o mundo e criar o personagem
`gera.py semente=N`, nesta ordem: mapa · recursos · povo · estoque a 30 dias · ecologia (12 espécies a 60% do teto) · três facções e 6 guildas · nomeados, 3 laços cada · rivais, nível 1 a 15 · Livro de Itens (toda peça Rara ou melhor, perto de 300) · calamidade e 2 ameaças latentes · **30 dias sem jogador** · banco de provas; reprovada, troca-se a semente.

`cria.py` (igual para os rivais): nome; origem (lugar, um ofício Iniciante, um conhecido); 40 por atributo e 90 pontos (teto 80); nível 1; peças Comuns; 50 c. Classe ganha-se no mundo.

## 10. O laço do turno
- `turno.py abre` gera a `MESA.md` (12 KB): hora, clima, corpo · caixa por prazo, com códigos · quem está aqui · preços · notícias · missões · ranking · ações com custo em blocos · SÓ O MESTRE · o esqueleto das perguntas.
- `turno.py age` executa uma resposta. O relógio **para** em item de peso 3, encontro, limiar do corpo ou prazo a um dia. "Rotina" pula dias até uma parada.
- `turno.py fecha` **recusa** com: bloco sem ação; luta aberta; dado declarado e não rolado; `valida` falho (id órfão, morto com rotina, peça sem dono, moeda que não fecha); arquivo acima do teto. Passando, gera o `RETOMAR.md` (6 KB) e o diário, e guarda no git.
- **Abrir a sessão:** `MESTRE.md` (6 KB), `RETOMAR.md`, `MESA.md`: **24 KB**. O `REGRAS.md` é consulta.

## 11. Dados e scripts
`save/`: `relogio.json` · `lugares.json` {povo{}, estoque{}, produz{}, lei, dono, oficina, dano} · `rotas.json` {a, b, blocos, bando, patrulha, aberta} · `ermos.json` {especies{n, teto}, masmorras{andares, primeira_de, dono}} · `gente.json` (nomeados, rivais, personagem) · `guildas.json` · `itens.json` · `missoes.json` · `caixa.json` · `ameacas.json` · `oculto.json` · `eventos.jsonl`. Cada fato num lugar só: quem está onde sai de `gente[id].lugar`.

Scripts (linhas): `tabelas_mundo.py` (250) · `estado.py`: carrega, valida, aplica (300) · `gera.py`, `cria.py` (650) · `mundo.py`: clima, produção, preço, caravana, ecologia, povo (600) · `gente.py`, `rivais.py` (750) · `corpo.py`, `mercado.py`, `viagem.py` (600) · `missoes.py`, `ameacas.py`, `caixa.py`, `fato.py` (850) · `turno.py` (450) · `provas_mundo.py` (350). Total: 4.800.

## 12. O banco de provas do mundo
365 dias sem jogador, 20 sementes:
1. Grão na capital: máximo ÷ mínimo entre 1,4 e 3; salário do braçal ÷ custo de vida: 0,9 a 1,3.
2. Gente de cada lugar: 70% a 130%; até 2 vilas perdidas.
3. Rivais: o primeiro no nível 55 a 80; 3 a 8 com peça Épica; até 1 com Única.
4. 20% a 60% dos rivais morreram; 3 a 5 das 8 masmorras com dono.
5. 6 a 14 ameaças; 50% a 80% contidas antes da etapa 4; a calamidade na etapa 2 ou 3.
6. Nenhuma espécie extinta; rota fechada em até 25% dos dias.
7. Peças novas: Épico 4 a 10, Único 0 a 2, Lendário 0.
8. 100% dos eventos com efeito; nenhum id órfão; MESA até 12 KB.
9. Caixa com jogador mudo: 3 a 8 itens por semana, **zero vencidos**.
10. Robô ferreiro: primeira Épica entre os dias 120 e 200; nenhuma Única antes do 300. Robô parado: abaixo da mediana do ranking no dia 60.

## 13. A ordem de construção e os riscos
1. **Um dia numa vila** (`estado`, corpo, `turno`): trabalhar, comer, dormir, lutar.
2. **A região** (mapa, economia, viagem): comerciar, viajar, ser assaltado.
3. **A gente** (nomeados, caixa, missões, forja): encomenda, prazo.
4. **Os rivais** (guildas, masmorras, ranking): a corrida.
5. **O medo** (ecologia, ameaças, morte): perder.
6. **O gerador e o ano de prova**; depois, o Dia 1.

**Riscos:**
1. **Sistema não conta história.** É o ponto fraco do ângulo: estoque dá gráfico, não drama. O remédio é parcial: ameaça com chefe de nome, a calamidade, nomeados que dão rosto. Vilão com plano pessoal não sai de sistema.
2. **Espiral** (fome, fuga, menos colheita). Freios: migração, importação a 3 ×, teto de preço.
3. **O povo é contagem**, e erro de um sistema vaza para os outros. Defesa: gravador único e banco de provas.

## Escolhas que só o jogador pode fazer
1. **A morte:** a) como acima · b) final, com herdeiro · c) três vidas.
2. **O começo:** a) todos no Dia 1 · b) chegar um ano atrasado.
3. **O passo:** a) bloco a bloco · b) rotina que pula dias.
4. **O tamanho:** a) uma região funda · b) três rasas.
