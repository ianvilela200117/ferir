# MOTOR 6.1 — o que mudou no motor (Dia 379)

As regras do jogo não mudaram. Mudou a máquina: o que o Mestre fazia à mão ou de cabeça agora é do script, e retomar a campanha custa uma página em vez de um milhão de letras.

## 0. MOTOR 6.1: detalhe primeiro (pedido do jogador)
O padrão agora é a **saída inteira**. O resumo virou opção (`tick.py bloco N resumo`). O BRIEFING é o painel de números e datas, não o substituto da leitura do cânone, das regras e do estado. E entraram quatro camadas novas de simulação, que são **regra nova do motor** (cada uma desliga em `motor.json`, em "camadas"):

- **Calendário vivo:** cada dia sai com a data (12 luas de 30 dias e 5 Dias Mudos, pelo Livro), a lua nova, a lua cheia, o começo de estação e o aviso dos Dias Mudos (sem forja grande, sem magia de 4º círculo para cima, sem casamento).
- **Clima por cidade e por estação** (`clima.py`): Ireviel, o Porto, Levis e Farenta têm céu e vento rolados por dia, com persistência (o tempo de hoje tende a repetir o de ontem). Cada estado traz o efeito na cena (neblina, lama, barco que não sai, calor na forja). O **rio** tem nível, sobe com chuva e degelo e desce com sol. Na semana, o clima pesa na Comida e no Comércio de cada cidade antes do dado do reino.
- **Turno das facções** (`faccoes.py`): as 28 facções do mundo, que eram só texto, ganham força, relógio do objetivo e postura para a casa. Toda semana cada uma age: racha, junta gente, avança, briga com outra da mesma terra, procura a casa, ganha patrono, faz gesto público. Objetivo cumprido muda a terra dela.
- **Voto do conselho por cadeira** (`conselho.py`): cada conselheiro presente vota pelo dado mais a inclinação que o Mestre declara antes. Maioria vence, a Intendente desempata, e o voto vencido fica anotado na ficha de quem perdeu.
- **Boatos:** toda notícia que chega traz como chega: fiel, exagerada, incompleta ou falsa. Onde a casa tem célula de espionagem viva, chega fiel.
- **A semana dos NPCs com conteúdo:** PROBLEMA e MISSÃO já saem com o que foi (doença, dívida, rival, contato novo, achado).
- **Fichas de NPC inteiras** em cena: `npc.py cena` mostra as 10 últimas notas sem cortar.

## 0b. MOTOR 6.2: revisão de combate e de equilíbrio (pedido do jogador: corrigir tudo, avisando)
Medido por simulação (milhares de lutas e de semanas). Regras do jogador que mudaram:
- **INICIATIVA (nova).** O grupo agia sempre primeiro. Em fichas iguais, isso dava 55% de vitória no nível 110 e 61% no 230 só pela ordem. Agora cada lado rola 2d20 + nível ÷ 10 (o grupo usa a média) e quem ganha age primeiro na rodada 1. Fichas iguais: 50% a 50%. Surpresa segue valendo. Desliga: `ini=nao`.
- **MAGIA DISPUTADA (muda a resistência).** O alvo resistia com 2d20 + o ataque dele contra CD 30 + 14, igual para qualquer lançador: de nível 155 para cima resistia sempre, bicho pequeno nunca. Agora o feitiço joga como golpe: 2d20 + ataque do lançador contra a Defesa + 14. Em cheio: inteiro. Resiste: metade. 20 que morde: dados dobrados. Dois 1: desfaz. Regra antiga: `magia=velha`.
- **REDES INIMIGAS APRENDEM (escolha 5b).** Cada agente pego faz a rede se recolher 2 semanas e voltar com +2 de força, até 26. Antes perdiam um agente em 8 de cada 10 semanas e entravam 1 em 30.
- **PROBLEMA DO REINO só em pilar 2 ou menos (escolha 6b).** Pilar em 3 ou 4 só recua no 1 natural. Eram 4 problemas por semana.
- **FILA DE XP dos NPCs.** Com XP guardado para 4 níveis ou mais, sobe 2 por semana; para 10 ou mais, sobe 3. Lendários, 1 por mês.
- **TETO de crescimento de monstro:** até 15% (+5) acima do nível em que foi achado. Antes subia sem fim.
Regras das camadas novas que acertei: clima na Comida (de 38% para 18% das semanas de verão) e facções (de 95% cumprindo o objetivo em um ano para 3 em 10).
O que medi e deixei como está, porque é escolha de tom e não erro: o dano maciço que mata (mais da metade do PV num golpe), o teste de morte contra 12, a casca (RD) por categoria que zera golpe pequeno, e o acerto que some quando a defesa passa 25 pontos do ataque (só o 20 que morde entra).

## 0c. MOTOR 6.3: as nove melhorias pedidas no Dia 383
1. **Viagem e recado com distância** (`viagem.py`): lê a tabela de distâncias do Livro, soma os trechos, olha o tempo na saída e põe a chegada na agenda.
2. **Fichas de combate únicas** (`combate.py`, `fichas_combate.json`): monta o arquivo de luta com o nível de hoje; avisa ficha velha e quem está ferido.
3. **Cerco geral** (`cerco.py`, pasta `cercos/`): o cerco da Elaeva virou um motor que serve para qualquer fera ou muralha.
4. **Recursos do dia** (`ficha.py recurso|usa|volta`): a Visão do Tempo e os usos de peça contados; o que é "por dia" volta no tick.
5. **Legitimidade e prestígio como moeda** (`reino.py legit|prest`): passar por cima do voto custa; legitimidade 5 ou menos pesa na Ordem toda semana.
6. **Ferimento que dura** (`feridos.py`; o `luta.py` chama sozinho) e **lealdade dos NPCs** (`npc.py lealdade`; três votos vencidos no conselho tiram 1).
7. **Mercado vivo** (`mercado.py`): índice de preço de grão, sal, ferro, carvão e peixe por cidade, movido por clima, rio e pilares; pão caro tira Ordem.
8. **Teste do motor** (`teste_motor.py`): roda tudo numa cópia, inclusive um tick semanal, e avisa o que cai. O `salvar.py` roda a versão rápida.
9. **Envelope novo** (`envelope_sessao2n.md`). O antigo (673 KB) fica de arquivo.
E um conserto: `nomes.py SONORIDADE N livre` confere as 3 letras no cânone e no Livro (o antigo `prefixo.py` não olhava o Livro e deixou passar um nome que já era de uma terra).

## 0d. MOTOR 6.4: as seis melhorias pedidas no Dia 387
1. **Julgamento como procedimento** (`julgamento.py`): provas e testemunhas com peso dos dois lados, a balança diz o que a praça espera, e a sentença mexe na legitimidade e na lealdade.
2. **Tratados que o motor cobra** (`tratados.py`): cada acordo com cláusulas e prazo; na semana, o tick mostra o que vence e rola se o outro lado cumpre.
3. **Batalha de exércitos** (`batalha.py`, pasta `batalhas/`): hoste contra hoste por rodadas, com qualidade, moral, terreno, comando e heróis que pesam como centenas. Tem régua (`sim=`).
4. **Painel do jogador** (`painel.py` → `painel.html`): uma página com data, tempo, Ferir, o reino, a agenda, os fios, o mercado e as distâncias. Nada oculto entra.
5. **Onde está cada um** (`onde.py`): quem está fora de Ireviel e quem está em viagem; o `viagem.py ... leva=Nome` atualiza sozinho e a ficha de cena avisa.
6. **Crônica por lua** (`cronica.py` → `cronica.md`): o índice da campanha mês a mês do calendário, tirado dos Pendentes.

## A. Leitura (o que ficou do 6.0, agora como opção)
1. **BRIEFING.md** (`contexto.py`): uma página (~3.700 tokens) montada dos arquivos de estado. Substitui ler `estado_vivo.md` (111 mil letras), o fim do envelope (680 mil) e `npcs.json` (210 mil) a cada conversa.
2. **Bloco de dias** (`tick.py bloco N` / `ate DIA`): vários dias numa chamada, com resumo só do que toca a casa. Um tick semanal inteiro tinha ~22 mil letras; o resumo tem um terço. O resto fica em `tick_N.txt`.
3. **Paradas automáticas:** o bloco para sozinho em item de agenda marcado, relógio que encheu ou cofre negativo.
4. **`npc.py cena NOME...`:** fichas curtas de quem está em cena. `npc.py arquiva` tira as notas velhas do arquivo principal sem apagar nada.
5. **`MESTRE.md`:** instruções curtas do Mestre para colar no Projeto. **`motor.py`:** a cola de todos os comandos numa tela.
6. **Lista "vigia"** (`motor.json`): o que conta como "toca a casa". `motor.py vigia +Nome`.

## B. Dados honestos por construção
7. **`selo.py`:** a tabela é gravada no envelope antes do dado, pelo script. Sem declaração não rola; não rola duas vezes; tabela com buraco é recusada.
8. **`selo.py lote`:** todas as tabelas de um bloco numa chamada (declara todas, depois rola todas).
9. **`selo.py conselho`:** o jeito rápido (pesos no d20, com o 20 natural de SURPRESA). O jeito completo é o `conselho.py`, voto por cadeira.
10. **`rotina.json`:** as tabelas "de sempre" da semana (laço, chamado, vínculos) são declaradas e roladas pelo tick semanal.
11. **`reino.py` com dado verdadeiro** (`secrets`), como o resto. Antes usava o gerador comum do Python.

## C. Estado que não se perde
12. **`ficha.py` / `ficha.json`:** XP, nível, atributos, PV, Mana e Foco num lugar. O XP sobe o nível sozinho e imprime a tabela; avisa ponto (a cada 3), talento (a cada 10) e marcos.
13. **Livro-caixa:** `ficha.py cofre` lança com motivo e saldo; a semana (casa + cidades − despesa) é lançada pelo tick. Material em kg com `ficha.py mat` (recusa gastar o que não há).
14. **`agenda.py`:** tudo o que tem dia. As notícias do mundo entram sozinhas e aparecem no dia em que chegam.
15. **Fios** (`agenda.py fios`): a lista do 🧵 com poeira (há quantos dias cada fio não anda).
16. **`relogio.py`:** relógios de facção com o TOTAL guardado, regra de dado fixa e desfecho escrito. O tick semanal rola todos.
17. **`obra_valor.py` lê a ficha viva:** nível e atributos de Ferir não ficam mais escritos à mão. As ferramentas passam de categoria sozinhas no nível certo (150 e 230). Herkald e Skedda leem o nível do livro dos NPCs.
18. **A semana integrada:** reino, relógios, rotina e livro rodam dentro do tick semanal. Rodar a mesma semana duas vezes é recusado.
19. **Gravação atômica** nos arquivos de estado: script que cai no meio não corrompe o JSON.

## D. Simulação
20. **Régua com distribuição** (`luta.py ARQ sim=N`): desfechos, duração, quanto sobra do monstro, quem morre, quem cai, e o veredito pela Lei das Caçadas (2%).
21. **`seed=N`** repete a mesma régua para comparar dois planos. **`regua=N`** grava a régua no envelope como OCULTO.
22. **Arquivo de luta conferido antes do dado:** campo faltando é avisado pelo nome. Os 104 arquivos de `sims/` passam.
23. **`mundo.py`:** o sub-dado já sai lido ("→ LEITURA DO DADO: febre") e o que cai em terra do reino sai marcado.
24. **`mundo_vivo.py`:** mortos fora das faíscas; aviso semanal de obra de Lendário e plano de povo prontos e parados, com `nova_obra` e `novo_plano` para sortear o seguinte.

## E. Erros que o motor antigo tinha (achados e consertados)
25. **A semana dos NPCs caía no meio** desde cerca do Dia 336: uma ficha sem nível derrubava o script e os oito NPCs depois dela no livro não viviam a semana. O tick não avisava.
26. **Script que cai agora aparece** no tick e no resumo ("CAIU NO MEIO").
27. **Modificadores com prazo não venciam:** "+1 (até o 353)" continuava somando no 378. Agora vencem na semana seguinte ao prazo. Levis e Farenta vão sentir no tick do 385.
28. **Lendários de NPC nunca subiam** (a regra "1 nível por mês" estava escrita e não rodava). Agora roda.
29. **`cresce.py` e `aberto.py` caíam** com nome errado ou uso incompleto. Agora aceitam nome sem acento ou pela metade e explicam o uso.
30. **O dia do reino estava parado no 353:** obra pública nova nasceria com data velha. Agora vem do relógio do jogo.

## F. O que o Mestre precisa decidir ao retomar (está no BRIEFING)
- O tick do **Dia 379 nunca foi rolado** (o `estado.json` está no 378; o RETOMAR dizia que o próximo era o 380). Rolar (`tick.py dia`) ou pular (`tick.py pula 379`).
- O nível da **Elaeva**: o RETOMAR diz 374; o `mundo_vivo.json` diz 376.
- Os dois **relógios de facção** foram reconstruídos do envelope, que nunca escreveu o total. Conferir.
- **Skotha, Almision e Eiandald** estão com a obra pronta e sem obra nova (o Skotha desde o 287). Quatro povos também.
- Valores fixos da semana: +2.900 e −6.046 (tirados dos livros do 371 e do 378). Ajustar com `ficha.py fixo`.

## G. Próximas camadas de realismo (ainda não fiz; diga quais quer)
1. **Mercado vivo:** preço de sal, grão, ferro, carvão e vaduar por cidade, mexendo com clima, rota fechada, guerra e o que a casa vende.
2. **Viagem com distância:** dias de estrada ou de rio por trecho, com o clima e o nível do rio pesando, e encontro pela região do bestiário.
3. **Ferimento que dura:** quem cai numa luta sai com ferida de gravidade e dias de cura, em vez de só voltar o PV.
4. **Doença e praga:** a febre anda de cidade em cidade pelo comércio, e a Saúde do pilar decide quem segura.
5. **Humor e lealdade dos NPCs da casa:** um número que sobe e desce com voto vencido, laço, paga e perda, e que pesa em traição e sacrifício.
6. **Facções grandes com ativos** (a Liga, a Leliel, a Doge, o Clã): tropas, navios, ouro e espiões contados, como o reino já tem.
7. **Fator de caos:** de 1 a 9, sobe quando a cena foge do controle e alarga a faixa de SURPRESA das tabelas.
8. **Posição e efeito** antes de cada teste (controlado, arriscado, desesperado), para o medo ficar explícito.
9. **Colheita anual:** a Lua do Grão fecha a conta do ano inteiro de clima e decide a Comida do inverno.
10. **Estoque de comida e soldo da hoste** contados por semana, com fome e deserção quando faltam.
