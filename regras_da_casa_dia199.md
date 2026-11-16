# REGRAS DA CASA — Dias 199-200 (pedido do jogador; valem daqui em diante)

## 1. OBRA DO DADO — script `obra_dado.py`
- **Sem alvo.** Os dados escolhem a categoria até o teto.
- **CDs fixas, iguais para todos:** Comum 15 · Incomum 25 · Raro 35 · Épico 45 · Único 55 · Lendário 70 · Mítico 85 · Primordial 100.
- **Rolagem:** 2d20 EXPLOSIVOS (cada 20 rola de novo e soma) + BASE.
- **BASE** = média dos 4 bônus (Matéria, Processo, Técnica, Acaso) + nível ÷ 10 + 2 por ajudante (máx. +6).
- **TETO DURO** (o material ruim não faz milagre): o menor entre
  - o melhor material (≥1/5 da massa) + 1 categoria;
  - a oficina (improvisada Incomum · comum Raro · boa Épico · mestra Lendário · lendária Mítico);
  - a RECEITA, que só se exige de LENDÁRIO para cima (Receita Mestra + condição; Mítico pede também núcleo). **Épico e Único não pedem receita.**
- **MAESTRIA (teto mole):** acima da categoria natural da maestria, −10 por categoria (Leigo Comum · Iniciante Incomum · Treinado Raro · Mestre Único · Lendário sem penalidade).
- **Os dados:**
  - cada 20 (também os que explodem): +1 efeito e uma peculiaridade;
  - os dois dados abrindo em 20: obra-prima;
  - três 20 ou mais: maravilha · cinco ou mais: LENDA;
  - SOBRA no teto: +1 efeito a cada 10 acima do limiar (máx. +3; 30+ também maravilha);
  - um dado em 1: complicação · os dois em 1: a peça se perde;
  - 1 em cada 10 obras ganha uma peculiaridade.
- **Efeitos:** sorteados em tabelas d20 por tipo. O que não cabe na peça é pulado. O ÚNICO tem 3 efeitos, um deles MAGIA de 1º a 3º círculo, sorteada no grimório.
- **ENCANTAMENTO:** limiar = CD da categoria da peça. Total ≥ limiar: inteiro · −10: uma vez mais fraco · −20: duas vezes · abaixo: o condutor se perde. Cada peça aceita 1 encantamento (2 com condutividade 5+, 3 se Lendária).
- **Simulado:** aprendiz (base 10): Raro 10% · Herkald (31): Único 40% · Ferir (39-40): Único 77% · Lendário 20% (com a receita e a condição).

## 2. REQUISITO DE NÍVEL (Dia 200)
- Para usar a peça inteira: Comum 1 · Incomum 5 · Raro 20 · Épico 40 · Único 70 · Lendário 110 · Mítico 180 · Primordial 260.
- Abaixo do requisito, a peça rende uma categoria abaixo, e o efeito de cima dorme.

## 3. MAGIA MAIS FORTE (Dia 200) — grimório `feiticos.py`
- O dano e a cura do feitiço são multiplicados pelo FOCO de quem lança: Comum ×1 · Incomum ×1,25 · Raro ×1,5 · Épico ×2 · Único ×3 · Lendário ×5 · Mítico ×10. Em ÁREA, metade do multiplicador (mínimo ×1).
- Um feitiço preso numa peça usa a categoria da peça como foco.
- Dano base do motor (X.8): 1º-3º círculo = 2d6 × círculo; 4º-6º = 4d6 × círculo.
- Grimório do mundo: 72 feitiços, 12 escolas, 1º a 4º círculo, de ataque, defesa, cura e utilidade.
- Magos seguem frágeis no corpo a corpo.
- Feitiço conhecido conta como receita de encantamento (pode ser imbuído). Feitiço novo se aprende com um mestre, um livro (a biblioteca de Telosus), uma compra ou uma pesquisa.

## 4. TÉCNICAS DE AURA para guerreiros (Dia 200)
- Luta Treinado: 1 técnica · Mestre: 2 · Lendário: 3. São feitiços de 1º–2º círculo de corpo (Pedra, Vento, Sangue, Tempo, Mente, Luz, Elo).
- Lançadas com Vigor ou Vontade + Luta; custam Estamina = círculo; 1x por cena.
- Escolhas: a Eliane tem Pele de Pedra e Fôlego de Ferro · o Graur, Raiz de Pedra menor · o Tamel, Calma.

## 5. TESTE ABERTO — `aberto.py`
- d20 EXPLOSIVO + bônus + nível ÷ 10, fora do combate.
- Falha por 10+: falha feia (surpresa ruim) · passa por 10+: ganho · passa por 20+: extraordinário (surpresa boa).
- 20 e 1 naturais puxam surpresa. No teste oposto, o empate fica com o NPC.

## 6. LISTAS DO MUNDO maiores
- d10/d12/d20, sempre com uma saída SURPRESA que puxa o `gerador.py novidade`.

## 7. O MUNDO CRESCE — `cresce.py`, `semana_npc.py`, `npcs.json`
- XP do que o NPC faz: luta, nível do inimigo × 10 para cada um que lutou (× 10 se o inimigo é Lendário) · ajudante de obra 1/4 · passo de agenda 500 · feito 500/1.000 · missão pela letra.
- Custo do nível: 100 × nível. No máximo 1 nível por Tick (Lendários, 1 por mês).
- No Tick semanal, cada NPC com ocupação vive a semana: problema · rotina · passo (500) · missão (1.000 XP e ouro) · surpresa.
- Classe de cada NPC no livro, e ela pesa em cena.

## 8. CONTRA O ESQUECIMENTO
- `protocolo_do_turno.md`, com a lista do que o mundo simula, lido em toda resposta.
- `estado_vivo.md`, a ficha de agora.
- Auditoria a cada 5 dias, sozinho.

---
# DIA 201 — A LEI DO VALOR (pedido do jogador; substitui a Obra do Dado, os tetos e a receita obrigatória)
**Ideia:** nada tem teto; tudo tem VALOR, e os valores SOMAM ao dado. O dado continua soberano: facilita, nunca decide sozinho.

## 1. Forja (`obra_valor.py`)
TOTAL = **2d20 explosivos** + MÃO + MATERIAL + FERRAMENTAS + OFICINA + RECEITA + AJUDANTES + EXTRAS (+% e CD − X dos efeitos)
- **MÃO:** maestria (Leigo 0 · Iniciante 3 · Treinado 6 · Mestre 9 · Lendário 12) + atributo do ofício ÷ 10 + Sorte ÷ 20 + nível ÷ 10 + talentos e habilidades (cada um com o seu número na ficha).
- **MATERIAL** (o melhor que for ≥ 1/5 da massa): sucata −3 · Comum 0 · Incomum 2 · Raro 4 · Épico 7 · Único 10 · Lendário 14 · Mítico 18 · Primordial 24; + afinidade da Essência com a peça e propriedades (dureza, maleabilidade) de +1 a +3.
- **FERRAMENTAS:** martelo + bigorna inteiros, 1 de apoio (tenaz, fole, buril) pela metade: improvisada −2 · Comum 0 · Incomum 1 · Raro 2 · Épico 3 · Único 5 · Lendário 7 · Mítico 10 · Primordial 14; + os efeitos delas (ex.: "Eu Bato Junto" +2).
- **OFICINA:** campo −4 · improvisada −2 · comum 0 · boa 2 · grande 3 · mestra 4 · lendária 6 · mítica 8 · primordial 12.
- **RECEITA (nunca obrigatória, só bônus):** Fragmento 1 · Esboço 2 · Receita 4 · Mestra 5 · condição cumprida +3.
- **AJUDANTES:** Iniciante/Treinado +1, Mestre ou acima +2; máx. +6. Ganham 1/4 do XP.
- **EXTRAS e encantos de ferramenta:** número fixo (+1 a +8 pela categoria: Incomum 1 · Raro 2 · Épico 3 · Único 5 · Lendário 8 · Mítico 12), **CD − X** (metade do número), **+10% dos valores** (só Lendário ou acima), **o 19 também explode** (Sorte), **rerrola o dado mais baixo** (Alma Ouvida).
- **CDs (iguais para todos):** Comum 15 · Incomum 26 · Raro 42 · Épico 55 · Único 68 · Lendário 84 · Mítico 102 · Primordial 125.
- **Os dados:** cada 20 explode (rola outro e soma) e dá +1 efeito e uma peculiaridade · os dois abrindo em 20 = obra-prima · 3 vintes = maravilha · 5 = lenda · QUASE (a 3 ou menos da CD seguinte) = +1 efeito · um 1 = complicação · dois 1 = a peça se perde.
- **Simulado (100 mil):** aprendiz (8): Raro 12% · aprendiz com material Lendário (22): Raro 57%, Único 3% · Herkald (42): Único 32%, Lendário 5% · Ferir (55, material Raro): Único 84%, Lendário 23%, Mítico 2,6% · Ferir com Veydun, Receita Mestra e condição (71): Lendário 84%, Mítico 18%.
- **Política das rerrolagens (Alma Ouvida, Fortuna):** rerrola o dado que deu 1, ou o mais baixo se deu 7 ou menos (sem alvo escolhido). Na reforja: rerrola se a peça não subiu.

## 2. Encantamento
TOTAL = 2d20 + MÃO de Encantamento + CONDUTOR (valor de material) + ferramenta (anel, buril, luvas) + oficina + ajudantes.
**LIMIAR** = CD da categoria da peça + círculo (1º −10 · 2º −5 · 3º 0 · 4º +5 · 5º +10 · 6º +15 · 7º +20). Inteiro · −10 uma vez mais fraco · −20 duas vezes · abaixo, perde o condutor. Peça aceita 1 encantamento (2 com condutividade 5+; 3 se Lendária).

## 3. Testes e combate (`aberto.py`)
- Bônus = SOMA DE VALORES (atributo, perícia, equipamento, encantos, talentos, apoio, terreno) + nível ÷ 10. d20 explosivo.
- **O 20 MORDE:** se o 20 (com a explosão) não chega, ainda é SUCESSO MÍNIMO. No ATAQUE o 20 acerta sempre, dano de crítico (dados da arma dobrados), a RD do alvo conta só metade, +1 dado de dano por 20 a mais na cadeia. Um nível 10 de Força 10 com um 20 FERE uma Lendária (arranha, não mata: os PV dela são outra conta).
- **O 1:** falha sempre; a surpresa ruim só vem se nem com o 1 o bônus chegava.
- **Peças de valor no corpo:** anel, broche, amuleto e insígnia dão um número a um tipo de teste (Incomum +1 · Raro +2 · Épico +3 · Único +5 · Lendário +8 · Mítico +12), ou CD − metade, ou o 19 explode.

## 4. Reforja, conserto e reforço (peças já feitas)
- **REFORJA (subir de categoria):** a peça entra como material da própria categoria (ou o material novo, se for melhor) +2 ("o aço já conhece a forma"); rola a obra normal. Se o total passa a CD da categoria de cima, ela SOBE (pode pular mais de uma), MANTÉM todos os efeitos e o encantamento e ganha os efeitos novos da categoria (e o de magia, se chegar a Única). Se não passa: fica como está, inteira; gasta só o material novo (≥ 1/5 da massa da peça). Um 1: racha (conserto antes da próxima reforja). Dois 1: cai uma categoria e perde o efeito mais fraco (nunca se perde inteira). **1 reforja por peça por semana** (o aço descansa). Tempo: 1 dia até Raro · 2 dias Épico e Único · 3 dias Lendário+. XP: só a diferença entre a categoria nova e a velha.
- **CONSERTO:** CD da categoria − 20 (mínimo 10), 1/10 da massa em material; +20 sobre a CD: a peça volta melhor (uma marca); um par de 1 tira o efeito mais fraco. XP: 1/4 da categoria.
- **REFORÇO DE ENCANTAMENTO:** o que saiu mais fraco pode ser refeito 1x por semana com meio condutor; se não chegar a inteiro, fica como estava (nunca piora).
- **TROCAR ENCANTAMENTO:** tira o velho (o condutor dele se perde) e encanta o novo.
- **AJUSTE A OUTRO DONO:** 1 dia, CD da categoria − 20.

## 5. O mundo se move (`mundo.py`, roda no `tick.py`)
Todo dia: 1 novidade longe (d20 do que · região · quando a notícia chega: 1 hoje · 2-3 em 1d3 · 4-5 em 1d6 · 6 só se alguém for atrás). Todo Tick semanal: 3 novidades e 1 em 6 de abrir uma TERRA ALÉM DO MAPA. Tudo entra no cânone (`mundo.json`).

## 6. Valor das peças de Ferir na Lei do Valor
Martelo de Mestre (Épico +3, e "Eu Bato Junto" +2: acordou, porque o requisito do Épico agora é 40) · A MATRIZ (bigorna Lendária +7) · Tenaz de Cinza (Rara, apoio +1) · Fornalha que Não Apaga (lendária +6) · no encantamento: anel O Fio do Ferreiro (rende Épico até o 70: +3) e luvas de forjador (+1). As peças já feitas ficam como saíram: rolaram pelas regras do tempo delas.

---
# DIA 201 (noite) — O MUNDO VIVO (pedido do jogador)
- `mundo_vivo.py` roda no tick todo dia e toda semana; o estado fica em `mundo_vivo.json`.
- **Os 8 Lendários** (motor XVI.5, mundo de poder alto): cada um com frente, região, nível, régua, OBRA DE VIDA, relógio de 8, ritmo, RIVAL lendário, desejo, medo, ambição e peças. Todo Tick semanal o relógio de quem chegou na data anda, e um d12 diz o que ele faz de visível no mundo; rivais que andam na mesma semana se chocam (d20 + régua; quem perde recua 2). Em qualquer dia, com 1-2 no d6, um deles faz algo. A notícia chega pelo d6 do mundo.
- **Monstros grandes** (Épico, Lendário, Mítico, Primordial): d10 por semana (dorme, caça, migra, ataca, cria, marca território, é caçado, cresce, é visto, surpresa). Os que dormem acordam com 20 no d20.
- **Povos-monstro** (goblins, hobgoblins, orcs, kobolds, gnolls, homens-lagarto, trolls, ogros, homens-rato, harpias, homens-peixe, gigantes de pedra): bandos com chefe de classe, número, desejo, relação com os humanos e plano de 6; d10 por semana.
- **Tramas** (ódio, amor, ressentimento, dívida, rivalidade, inveja, desejo secreto, lealdade cega, medo, traição pendente, vingança jurada, paixão proibida): intensidade 0-4; d6 por semana (1 esfria · 5-6 esquenta); em 4 EXPLODE e vira cena; em 0 apaga. Toda semana nasce uma trama nova entre gente que já existe.
- **Faíscas do Mestre**: ideias que juntam quem já existe + um verbo + um porquê; o Mestre usa pelo menos 1 por resposta.
- **Espionagem da casa**: chefe (bônus) + células por cidade (força 1-3, CD da cidade). Relatório semanal: falha feia (um agente cai, a célula perde 1, o outro lado sabe) · nada · RUMOR VERDADEIRO · SEGREDO · SEGREDO GRANDE + oportunidade. Operação extra numa cidade: `mundo_vivo.py espiao CIDADE`.
- **Contra-espionagem**: bônus que treina (+1 em 5-6 no d6 por semana, até +30). Toda semana cada REDE INIMIGA tenta entrar (oposto): se entra, descobre um segredo da casa; se perde por 10, um agente dela cai. Todo dia a contra rola contra cada INFILTRADO solto: PISTA (passa por 0) ou IDENTIFICADO (passa por 10).
- **Encantamento**: a peça e o feitiço são escolhidos pelos DADOS, nunca pelo jogador nem pelo Mestre.

---
# DIA 202 — A LEI DA FERA (combate justo contra monstros; pedido do jogador) — `luta.py`
- **Ações por rodada do monstro** = 1 + nível ÷ 100 + categoria (Raro 1 · Épico 2 · Único 2 · Lendário 3 · Mítico 4 · Primordial 5) + 1 a cada 3 inimigos além do primeiro (máx. +2).
- **Fôlego de fera:** contra grupo, PV máximo × (1 + 0,10 por inimigo além do primeiro), até × 1,5.
- **Couro:** RD mínima pela categoria (Raro 5 · Épico 10 · Único 15 · Lendário 25 · Mítico 40 · Primordial 60).
- **Poder assinatura:** Raro a cada 2 rodadas; Épico ou mais toda rodada.
- **Reação:** golpe de 10% do PV ou crítico leva contra-golpe imediato (Raro 1 por rodada · Épico 2 · Lendário 3 · Mítico 4).
- **Fúria** abaixo de 50% (+1 ação, poder recarrega) · **moral** abaixo de 25% (1-3 foge).
- **Recuo** da gente: PV a 40% (heróis 25%), 1-4 no d6 sai viva da luta.
- **0 PV (motor X.6):** desacordado; teste de morte d20 contra 12 por rodada (3 falhas morre, 3 sucessos estável); golpe em caído = 2 falhas; **dano maciço** (mais da metade do PV máximo num golpe) mata na hora; estancar = Medicina CD 15.
- **Fraqueza do nome:** quem grita o nome (gasta a ação) tira do monstro 1 ação e o poder naquela rodada.
- **A régua é declarada ANTES de toda luta** (simulação do luta.py sem valor de jogo, e a leitura do motor VIII.3).
- Simulado: a luta do 201 com estas regras: a casa vence ou espanta ~78%; cada miliciano morre ~50%; os heróis 1-8%.

---
# DIA 203 — A LEI DAS AÇÕES (pedido do jogador: "uma Lendária contra 10 nível 30 batendo 1 também é injusto"; "o monstro crescer pelo tamanho do grupo só se for poder dele") — `luta.py` v2
- **Ações por rodada = 1 + nível ÷ 60** (máx. 8), para gente e monstro: 1-59 → 1 · 60-119 → 2 · 120-179 → 3 · 180-239 → 4 · 240-299 → 5 · 300-359 → 6 · 360-419 → 7 · 420+ → 8.
- O MONSTRO soma o CORPO da categoria (é dele): Raro +1 · Épico +2 · Único +2 · Lendário +3 · Mítico +4 · Primordial +5.
- **Fim** do bônus de ação por tamanho do grupo e do fôlego de grupo. Só como PODER próprio do monstro ("fúria do bando", "fôlego do bando": enxames, hidras).
- **Golpe que varre:** derrubou alguém com metade do nível ou menos → o golpe segue no próximo ao alcance (1 vez por ação).
- **Contra-golpe da gente** de nível alto: 120+ → 1 por rodada · 240+ → 2 · 360+ → 3 (o monstro segue pela categoria).
- **Mão da experiência:** todo golpe de arma ou garra soma **nível ÷ 5** ao dano. Feitiço não (o foco já multiplica).
- Simulado: Lendária 340 × 10 de nível 30: vence 100% em 1 rodada (antes 5) · Eliane 91 × 10 de nível 30: vence 59% · Lendária 340 × 10 VETERANOS de nível 150: 51% × 49% · Laennor inteiro × a casa: a fera morre 69%, foge 31%; arqueiros morrem 30-47%.

## Auditoria do Dia 203 (sozinho)
- CORRIGIDO: os aros do Graur somam na contra-espionagem (+5) · a COBIÇA voltou a rolar (Matriz, Fornalha, aros) · os MORTOS não vivem mais a semana (semana_npc, cresce) · a contra-espionagem tem uma LISTA DE SEGREDOS DA CASA · a obra de um Lendário só se completa DEPOIS dos choques de rivais.
- PROPOSTAS (o jogador decide): (1) XP de obra: a mesma receita repetida na semana rende metade · (2) REFORJA: cada categoria além da primeira pede +10 · (3) feitiço preso na peça usa o foco da categoria em que o dono a usa (pelo requisito) · (4) espionagem: CDs Marasar 40 · Farenta 35 · Levis 30 · Delta 25.

---
# DIA 204 — o jogador aceita as 4 propostas (com o ajuste da espionagem) e pede eventos em d20
- **XP de obra:** a mesma receita repetida na mesma semana rende METADE.
- **Reforja:** cada categoria além da primeira pede +10 no total (`obra_valor.py`). Simulado: Ferir com uma peça Rara: Única 89%, Lendária 29%.
- **Feitiço preso na peça:** o foco é a categoria EM QUE O DONO USA a peça (pelo requisito de nível).
- **Espionagem pelo estado da cidade (soma de valores, como a forja):** CD = 20 + tamanho (aldeia 0 · vila 2 · cidade 5 · capital 10) + ordem (nenhuma 0 · fraca 2 · guarda 5 · guarda forte 8) + riqueza (pobre 0 · média 2 · rica 4) + rede inimiga local ÷ 4 − problemas (cerco ou guerra 6 · peste ou fome 4 · caos ou sucessão 4 · monstro perto 2 · refugiados 2 · feira grande 2) − amigos da casa ali (2 cada). Muda quando a cidade muda (`mundo_vivo.json`, celulas → estado).
- **EVENTOS em d20** (mais variedade): tick.py (evento local com 20 saídas · avistamento 1-7 · EVENTO DE MUNDO e encadeamento com 20 saídas cada · vínculos e cobiça) · mundo_vivo.py (Lendários 20 ações · monstros 20 · povos 20 · tramas: 1-3 esfria, 14-19 esquenta, 20 esquenta 2 · a notícia: 1-4 hoje, 5-10 em 1d3, 11-17 em 1d6, 18-20 só se alguém for atrás) · as LISTAS DO MESTRE passam a d20, sempre com uma SURPRESA.

## Correção do Dia 204 (noite): erro no luta.py
- O script dobrava o dano de quem não tem Essência contra quem não tem fraqueza (vazio contava como igual). Afetou as lutas de GENTE contra gente; as dos monstros com fraqueza (o Laennor) não. Corrigido. Números certos: Lendária 340 × 10 de nível 30: vence 100% · Eliane 91 × 10 de nível 30: vence 97% · Lendária 340 × 10 veteranos de 150: vence 99% · o sótão (casa + Thuron + Ferir × o Pelaccino 110): ele cai 30%, foge 40%, a casa recua 30%.

---
# DIA 205 — O CERCO (pedido do jogador: as réguas de antes, sem o erro) — `luta.py`
- **A guarda tem limite:** cada um defende por rodada tantos golpes quanto as suas AÇÕES. Cada golpe a mais que recebe na mesma rodada acha uma brecha: **−1 na Defesa, acumulando, até −7**. Vale para gente e monstro, dos dois lados.
- Achado por grade (cerco por golpe e por pessoa, passo 1-5, teto 2-20, mão da experiência ÷5 e ÷10); só este bate as réguas que o jogador achou justas.
- Simulado: Eliane 91 × 10 de nível 30: ela vence 60% · Lendária 340 × 10 veteranos de 150 SEM EQUIPAMENTO (armadura comum, RD 6, dos dois lados): 50% · a mesma com a armadura dela (RD 20): 75% · Lendária × 10 de nível 30: 100% · o Laennor contra a casa: sem mudança (72/28).
- Conserto junto: na luta retomada no meio, o máximo de PV é o VERDADEIRO (`pvmax_real`), não o atual (o recuo e o dano maciço saíam errados).
- Fuga barrada: quem guarda a saída (gasta 1 ação) faz teste oposto contra a fuga do inimigo; ganhando, ele luta até cair.

## DOIS DADOS (Dia 207, pedido do jogador: "dá mais poder aos dados")
- **COMBATE (luta.py):** ataque = 2d20 (cada 20 explode à parte) + ataque, contra DEFESA + 14. O +14 (e não +10) foi achado por simulação: com dois dados as pontas abrem, e com +10 o bando de fracos ganhava quase sempre. Com +14 e o CERCO como está: Eliane × 10 de nível 30 = ela vence 52% · Lendária nua × 10 veteranos de 150 = 47% · de armadura = 78% · Laennor × a casa = morre 63%, foge 34%. (Com +15: 60% · 63% · 85%.)
- **O 20 MORDE** (crítico, acerta sempre, RD pela metade) só quando o OUTRO dado dá 11 ou mais; cada 20 da jogada soma +1 dado no crítico. **Dois 1:** erra sempre.
- Resistências dentro da luta (veneno, área, magia, fuga): 2d20, CD + 14. Medicina: 2d20 + Medicina contra 25. **Teste de morte: continua 1 d20 contra 12.**
- **TESTE ABERTO (aberto.py) e ESPIONAGEM (mundo_vivo.py):** 2d20; CD fixa + 10; teste oposto: os dois lados com 2d20. Os graus seguem a margem (10 e 20): os extremos vêm mais vezes.
- **FORJA (obra_valor.py):** já era 2d20 explosivos desde a Lei do Valor (201); não muda.
- Listas de resultado (1-20 para sortear o que acontece) seguem d20: são oráculo, não teste.


## REGRA DA FAMÍLIA (Dia 210, decisão do jogador)
- "Todos que chegarem com família para resgatar, vamos resgatar. Não quero ninguém aqui com a família na mão dos inimigos." Quem entra para a casa e tem parente preso, refém ou acorrentado por inimigo: a casa o tira de lá (missão da casa, planejada com o conselho). Primeiros: o filho do KREINE (a galé da Liga do 218) e o filho do DRARON (aprendiz preso por dívida ao MORMIR, em Quoine).

## SOB MEDIDA, os graus (Dia 210)
- Ramo Oficina. Grau 1 (nível 1): −10 no requisito para o portador · grau 2 (nível 20): −20 · grau 3 (nível 50): −30 · grau 4 pede nível 100. Vale para peça feita, reforjada, consertada ou AJUSTADA por Ferir com o portador ao lado e o nome gravado; segue o grau de Ferir sem refazer a peça. Ferir está no GRAU 3 desde o 210.
- ASSINATURA (talento de Ferir desde o 210): obra Épica ou melhor dá +1 de Fama (no máximo 1 por mês); toda peça com a marca pode ser rastreada até Ferir.
- MÃO QUE NÃO TREME 3 (Dia 211, o ponto guardado do 54): +3 em toda obra (era +2); 1x por dia um 1 natural vira 2.
- AJUSTE (Dia 211): usa a regra do CONSERTO (CD da categoria − 20); passa: a peça fica Sob Medida para o portador presente; passa por 20: e ganha uma marca (+1 de durabilidade).

- SÉRIE DE MESTRE (ramo Oficina, o ponto do 57, Dia 213): a forja grande, com a ordem de Ferir, faz a série UMA CATEGORIA ACIMA.
- TABELA CONDICIONAL (auditoria 213): uma tabela que vale "se X" só rola DEPOIS que X sair. Rolada antes, o resultado é descartado (ou, se o jogador não viu e a tabela é a verdade do mundo, fica como verdade oculta e o erro se anota).
- SIMULAR ANTES (regra do jogador, Dia 216): antes de toda OBRA ou ENCANTAMENTO com risco de perda, o Mestre mostra a simulação (obra_valor.py sim, ou o limiar contra a soma no encantamento) e o jogador confirma. O que o Mestre propõe sem mostrar a chance e dá errado por isso se desfaz (o caso do encantamento do 215).
- MODO DE BLOCOS (pedido do jogador, Dia 217): o Mestre corre vários dias com as ordens de pé e só para num ponto de decisão (luta grande sem régua aprovada, coisa que não se desfaz, escolha que só o jogador pode fazer).
- ENCANTAR NAS NOITES LIVRES (ordem de pé, Dia 217): só com chance ≥ 90%; abaixo disso o Mestre pergunta. Os pontos de habilidade vão ao Encantamento.
- SÉRIE ÉPICA (aprovada pelo conselho, Dia 217): a forja grande, com o Herkald e a Série de Mestre, faz 2d6 + 2 armas Épicas por semana (rola no tick semanal), 30 de ouro por peça, a cidade paga metade; o Herkald ganha 1/10 do XP de cada peça.
- SURPRESA NAS TABELAS (fixada no 218): SURPRESA = 20 NATURAL, ou total ≥ 20 quando a tabela não tem faixa acima; sempre por cima do resultado alto, sem baixá-lo.
- MAGIA QUE CABE NA PEÇA (regra do jogador, Dia 224): quando se rola um feitiço para uma peça (encantamento ou o efeito de magia da obra), entram na lista só os feitiços que cabem no TIPO da peça; se o d72 da obra der um que não cabe, rerrola. Os 12 de Ferir: ARMA: Alma de Brasa · Faca Acesa · Faísca · Flor de Brasa · Geada de Lâmina · Sono do Ferro · Chuva de Brasas · Quebra-Ossos · ARMADURA e ESCUDO: Pele de Pedra · Fio de Elo · Alma de Brasa (aquece quem veste) · FOCO, JOIA e OBJETO: Fio de Elo · Sussurro · Falar com Morto · Faísca · Flor de Brasa · Chuva de Brasas · Quebra-Ossos · FERRAMENTA: Fio de Elo · Sussurro · Alma de Brasa. Vale daqui para a frente; o que já saiu fica, salvo pedido do jogador.

## CONFERIR ANTES DE NARRAR (Dia 244, pedido do jogador depois de "você está alucinando")
- No começo de cada bloco o Mestre lê o canone.md. Todo fato antigo que entra na cena (quem é, onde mora, o que fez, de onde vem uma coisa) passa antes por `python3 confere.py TERMO`. Se não há nada escrito, o fato não existe: declarar tabela e rolar, nunca inventar como se fosse antigo.
- Erro achado vira linha nova no canone.md, na hora.

## CONFERIDOR DE 5 EM 5 DIAS (pedido do jogador, Dia 248)
- Nos dias de AUDITORIA do tick (a cada 5 dias: 253, 258, 263…) e no começo de cada sessão: `python3 conferidor.py DIA`. Ele acha: tick semanal sem PILARES, a trama do jogador rolada, nomes repetidos ou parecidos, nomes novos sem declaração, fichas sem nível, o cofre do estado diferente do envelope, e frases que contrariam o cânone. Cada aviso é olhado, corrigido ou explicado no envelope, e o que já foi resolvido vai para o conferidor_visto.txt.

## POLÍTICAS DE IREVIEL (ordem do jogador, Dia 248; valem a partir do 249)
- (P1) FUNDO DOS OFÍCIOS — financiamento de negócios novos. Responsável: a NOULIEL (o livro). Capital de 3.000, uma vez, do cofre. Empréstimos de 200 a 600, com 10% de juros no total, pagos em 10 semanas; o que volta empresta de novo. No tick semanal: 1d4 pedidos (enquanto há dinheiro no fundo). Cada empréstimo, d20: 1-3 CALOTE (o dinheiro se perde) · 4-12 o negócio ABRE e paga (+15 por semana na renda, de imposto e ofício, a partir da semana seguinte) · 13-19 PROSPERA (+30 por semana) · 20 SURPRESA (gerador novidade). Com 4 negócios novos abertos, o pilar COMÉRCIO ganha +1 na rolagem semanal.
- (P2) CASA DOS ESTUDIOSOS — pesquisa e gente de fora pesquisando em Ireviel. Responsável: o CEDUION (o Colégio). Custa 100 por semana (sala, biblioteca, cartas pelo rio) + 40 por semana de bolsa por pesquisador de fora. No tick semanal, chegada, d20: 1-10 ninguém · 11-17 um pesquisador · 18-19 dois · 20 SURPRESA (um nome grande). Cada um: gerador npc + área, d6: 1 metais e forja · 2 alquimia e remédios · 3 magia e runas · 4 monstros e núcleos · 5 história e ruínas · 6 plantas e terras; nível 2d20 + 10. Cada chegada passa pelo REGISTRO (P4), d20: 1-4 é agente de alguém (a contra-espionagem rola contra ele) · 5-20 é quem diz ser. A cada 4 semanas de casa, cada pesquisador, d20: 1-10 nada ainda · 11-17 um FRAGMENTO de receita ou técnica da área (conta como FONTE: −2 na CD de uma receita) · 18-20 uma descoberta grande.
- (P3) PORTA DO MINÉRIO — entrada de minérios e materiais. Responsáveis: o ODRUM (compras) e a SKEDDA (o pedágio e os selos). Minério, metal bruto, carvão e material de monstro entram SEM PORTAGEM (a portagem cai de 300 para 200 por semana) e a forja compra na hora, a preço de tabela. No tick semanal, d20: 1-7 nada novo · 8-14 carregamento comum (ferro, cobre, carvão): a despesa da Série cai 30 naquela semana · 15-18 um material RARO à venda (gerador material) · 19-20 notícia de material ÚNICO ou LENDÁRIO (gerador material e quem traz). LEI DO VADUAR (leitura do conselho, pelo que a casa sabe desde o 238): o vaduar entra, mas DENTRO DOS MUROS SÓ SE TRABALHA A FRIO; fundição que o esquente é fechada (o pó aquecido é a febre cinza).
- (P4) SEGURANÇA E CONTRA-ESPIONAGEM. Responsáveis: o GRAUR (os capuzes, a cela, os aros), a SKEDDA (selos) e a ELIANE (a guarda). REDE DE OLHOS no cais, no mercado e entre os refugiados (100 por semana): +2 · REGISTRO DE FORASTEIROS no portão e no cais, com selo para quem fica mais de 3 dias (50 por semana): +1 · +10 GUARDAS da milícia nas ruas à noite (140 por semana): +1. Prontos no 252. TETO: a contra-espionagem treina até +30 (mundo_vivo: contra_max); o que passar de 30 fica parado até o teto subir (um chefe melhor, ou uma peça).

- (Dia 254) O CONFERIDOR roda junto com o `noticias.py` (as notícias que os ticks marcaram para cada dia), para nenhuma notícia ficar sem processar.

## SIMULAR ANTES, VERSÃO DO DIA 257 (esclarecimento do jogador)
- "Eu não tenho que saber o resultado antes; só tenho que entender se vai ser difícil ou não: preciso de tanto e tenho tanto." Antes de obra ou encantamento, o Mestre mostra a DIFICULDADE: o que precisa (CD ou limiar), o que tem (a soma) e o que se arrisca perder (material, condutor). Com a ordem do jogador, executa sem esperar outra confirmação. Se houver risco de perder algo valioso que o jogador não conhecia, o Mestre avisa ANTES e, sem ordem de pé, pergunta.
