> **MOTOR 6.1 (Dia 379) — VALE ANTES DE TUDO ABAIXO.** Para retomar: `python3 contexto.py`, ler o `BRIEFING.md` (o painel) e o `MESTRE.md`, e depois a matéria de fundo (cânone, regras, estado, último bloco do diário). O jogador quer detalhe primeiro. Onde este texto mandar declarar a tabela no envelope e depois rolar, usar `selo.py` (ele escreve as duas linhas). Onde mandar rodar `reino.py semana`, não rodar: o tick semanal já roda, junto com o clima, as facções, os relógios e o livro. Correr dias: `tick.py bloco N` (saída inteira). XP e cofre: `ficha.py`. Conselho: `conselho.py`. A lista do que mudou: `MELHORIAS_v6.md`. As regras do jogo e as regras do jogador continuam as mesmas; as camadas novas (clima, facções, boatos) estão descritas lá.

# PROTOCOLO DO TURNO — o Mestre segue isto em TODA resposta (Dia 200)

## 0. Antes de responder (sempre; obrigatório depois de qualquer resumo ou conversa nova)
- Ler `claude/estado_vivo.md`, o diário mais novo (`claude/diario_sessao2f.md`) (a ficha de agora), `claude/regras_da_casa_dia199.md`, o fim do envelope mais novo (agora `claude/envelope_sessao2n.md`, desde a tarde do 210; o 2k vai da tarde do 209 à tarde do 210; o 2j vai do 207 à tarde do 209; o 2i do sótão ao Dia 206; o 2h até a rodada 7 do sótão) e o `claude/npcs.json`.
- O `estado.json` e o `estado.md` do projeto são do DIA 159: arquivo, NÃO ficha atual.

## 1. A LISTA DO QUE O MUNDO SIMULA (conferir item por item, todo turno)
Ninguém precisa me lembrar disto:
1. **Laços** (Herkald, Nouliel, Tilde, Ulurve, Brara, Aeliae): 1 momento ou 1 atrito por semana; de vez em quando, PERGUNTAR o que Ferir sente.
2. **XP de Ferir**: toda obra, encantamento, luta, descoberta, feito; conferir o nível (N custa 100 × N).
3. **XP e nível dos NPCs**: `cresce.py xp` na hora (luta: nível do inimigo × 10 cada um que lutou; ajudante 1/4; passo 500; feito 500/1.000; quem MATA um Lendário leva × 10).
4. **A semana dos NPCs**: missões, ouro e XP (`semana_npc.py`, roda no Tick).
5. **CLASSES**: todo NPC em cena age pela classe (família, assinatura, magia). Mago lança feitiço, assassino usa veneno e sombra, runista risca runa, capitão comanda. Guerreiros hábeis usam as técnicas de aura.
6. **MAGIA no mundo**: é comum. Mostrar magos, bruxas, clérigos e runistas em cena; usar o grimório (`feiticos.py`); o dano é multiplicado pelo foco.
7. **Forja e encantamento**: `obra_valor.py` (LEI DO VALOR, Dia 201: tudo soma, sem teto; reforja, conserto e reforço); mostrar a SOMA DE VALORES e os dados.
8. **Relógios** de facção, vilão, culto e Lendários; **vínculos** entre NPCs; **cobiça** das peças.
9. **Cidade**: pilares (Comida, Comércio, Dinheiro, Saúde), livro da casa (ouro que Ferir sabe e o real), comida, material, obras em andamento.
10. **Mundo** (`mundo.py` e `mundo_vivo.py` no tick; mundo.json e mundo_vivo.json: os 8 LENDÁRIOS com desejo, ambição, relógio e rival · MONSTROS GRANDES · POVOS-MONSTRO · TRAMAS de amor, ódio, ressentimento · ESPIONAGEM e redes inimigas · infiltrados): Pressão e eventos, bestiário vivo e avistamentos, fios ativos, pendentes do Envelope (quem chega quando).
11. **Ferir**: PV, Mana, Fortuna, Revés, prática das perícias, pontos de habilidade e talentos não gastos.

## 2. Antes de rolar
- Declarar no Envelope a tabela de cada dado, em **d20** (Dia 204, pedido do jogador: mais variedade), com saída SURPRESA que puxa o `gerador.py novidade`, e só depois rolar. Testes de perícia seguem o `aberto.py`.

## 3. Rolagens
- OBRA: `obra_valor.py`. Teste: `aberto.py` (DOIS DADOS desde o 207: soma de valores + 2d20 explosivos + nível ÷ 10, CD +10; o 20 morde com o outro dado 11+). Combate: X.2 com o 20 que morde; contra MONSTRO ou um contra muitos, `luta.py` (LEI DA FERA + LEI DAS AÇÕES, Dia 203: ações por nível, sem bônus de grupo, golpe que varre, nível ÷ 5 no dano). ANTES de toda luta: simular (`luta.py ARQ sim=2000`, sem valor de jogo) e DECLARAR A RÉGUA no Envelope e ao jogador quando ele puder saber.
- MUNDO: `mundo.py` roda no tick; cada novidade que chega a Ireviel entra na cena do dia em que chega. EXPANDIR: todo turno, pelo menos 1 coisa nova do mundo em cena (gente, lugar, notícia, magia).
- Dado que o personagem não vê aparece como "rolagem oculta".
- ENCANTAMENTO: a PEÇA e o FEITIÇO são escolhidos pelos DADOS (d da peça livre, d do feitiço conhecido; o que não cabe rerrola). Nunca perguntar ao jogador.
- FAÍSCAS: toda resposta usa pelo menos 1 faísca (`mundo_vivo.py faisca 3`) ou do tick: uma ideia nova que junta coisas que já existem. Anotar no Envelope qual foi usada.
- TRAMA que EXPLODE vira cena na mesma resposta. Notícia que chega hoje (mundo.py, mundo_vivo.py) entra na cena de hoje.
- O MESTRE MELHORA SOZINHO: a cada auditoria, escrever no REGISTRO 1 coisa que esqueci e 1 sistema que ajustei.

## 3b. Conferências que eu já esqueci (auditoria 203)
- Mortos não vivem a semana · toda tabela que um script cita ("lista de segredos") tem de existir ANTES de rolar · peça nova no corpo de alguém entra nos bônus dele (espionagem, testes) · cobiça rola toda semana · resultado de Lendário só depois dos choques · estado de infiltrado é só 'solto'/'identificado' (pista em campo à parte) · a CD de espionagem vem do ESTADO da cidade (atualizar quando a cidade mudar).

## 4. Ticks
- `tick.py dia` todo dia. No semanal ele roda o `semana_npc.py` e o `cresce.py tick` e imprime o checklist. Na auditoria (a cada 5 dias), conferir TUDO sozinho e escrever no REGISTRO o que achei.

## 5. Fim do turno
- Envelope (oculto), Diário (cânone), `estado_vivo.md`, `npcs.json`: ler cada um inteiro e salvar no projeto.

## 6. A resposta
⏳ PENDENTE · 🕰️ RELÓGIO · 🎲 ROLAGEM · 🎭 CENA · 👁️ O QUE VOCÊ VÊ · 🧵 FIOS ATIVOS (máx. 7) · 🎯 OPÇÕES · 📊 ESTADO (com Laços) · 📜 REGISTRO.
- Leitura da escolha ambígua no topo. Não facilitar; propor ideias de equipamento; admitir erro (regra 14).

## REGRA DO JOGADOR (Dia 362): sem régua na mesa
- Não mostrar régua de combate ao jogador, a não ser quando Ferir tiver em jogo o poder ou a percepção de ver o futuro (a Visão do Tempo: uma hora à frente, luta curta, só quando ele a usa). Sem isso, o Mestre só pergunta e deixa o jogador "se lascar". A régua segue escondida no envelope para as decisões dos NPCs (o Marechal, o conselho). A parada do bloco é por decisão, não por régua.

## O PEDIDO DO JOGADOR (Dia 366): o tom
- "Quero que você como mestre me leve a uma história que dê medo, emoção, imprevisibilidade, e quando eu conquistar algo eu sinta que conquistei por merecer." O Mestre: perigo de verdade e consequência que fica; nada de atalho nem vitória de graça; o mundo age pelas próprias razões; surpresa pelo dado, nunca contra ele; a conquista vem do plano, do preço pago e do risco corrido.
- OBJETIVO DO JOGADOR (366): ACABAR COM A LIGA DE VEZ. "Quando a gente enfiar a faca, tem que rodar": todos mortos, presos ou servindo a casa.

## MOTOR 7.2 (Dia 402, pedido do rei; o jogador foi avisado)
- **G1 · A GUILDA DOS AVENTUREIROS (Ireviel; abre no 412; mestre: o Starkald):** na abertura 2d6+6 membros (nível 10 a 40). Toda semana: **missões privadas** d20 (1-8 nada · 9-16 um contrato · 17-19 dois · 20 surpresa: gerador missão; a coroa leva 1d6×20 por contrato) · **missão da cidade** (a coroa paga 300 por semana) d20 + nível do mestre ÷ 20: 1-3 desastre (1d4 feridos, d20 cada: 1-3 morre) · 4-9 1d6 kg Comum · 10-15 1d4 kg Incomum ou 0,5 kg Raro · 16-18 1 kg Raro e um RUMOR DE NÚCLEO (fera Épica+ do bestiário: vira Caçada) · 19+ 0,5 kg Épico ou NÚCLEO À VENDA (d6: 1-5 Épico, 3d6×1.000 · 6 Único, 3d6×3.000; dura uma semana) · 20 natural: isso e surpresa. **Ordem de compra:** a Intendente compra se o cofre ficar acima de 10.000; senão o rei decide.
- **G2 · A GUILDA DOS MINEIROS (Levis; abre no 409; mestre: o Gurka; forma C, só as minas de baixo):** 200 por semana · 2d6×10 kg de ferro por semana (um quinto à forja; o resto ao mercado: o ferro cai 5 por semana até 80 em Levis e Ireviel) · Comércio de Levis +1 enquanto funcionar · d20: 20 → veio novo (d6: 1-3 Incomum · 4-5 Raro · 6 Épico; 1d4 kg) · Saúde de Levis +1 no 423.
- **G3 · O RECRUTAMENTO:** 20 lanças da cidade (prontas no 423; +280 por semana) · o CHAMADO ANUNCIADO: +3 no chamado da semana; quem entra pede uma peça da forja (Raro+) no lugar de soldo, dentro de uma lua.
- **G4 · A CURA:** sara 1/10 do PV máximo por noite de descanso, para todos.
- **TETO LENDÁRIO DE UMA PEÇA QUE ALCANÇOU MAIS:** ficam 3 efeitos e a magia, pela ordem rolada.
- **G5 · O ESTOQUE DA CIDADE (403, ordem do rei; vale desde a semana do 406):** a Intendente separa 400 por semana para material de forja nos mercados das quatro cidades; d20 por semana: 1-10 Comum, 2d6 kg (12/kg) · 11-17 Incomum, 1d4 kg (50/kg) · 18-19 Raro, 1 kg (200/kg) · 20 Épico, 0,5 kg (800/kg: passa do orçamento, o rei decide) ou um rumor de núcleo; o que sobra volta ao cofre; núcleos pela ordem do G1 (compra se o cofre ficar acima de 10.000); nomes do Livro pelo gerador.py material. · **O CHAMADO** rola **d20+3** desde o 406 (G3; corrigido na rotina.json).
- **G6 · O DESCONTO DOS FORÇADOS (noite do 406, palavra do rei; o jogador foi avisado):** enquanto os condenados ao trabalho forçado servirem (hoje **87**: os 78 do Ardenghi, os 2 saqueadores da costa, o Skarkek e os 6 da guarda da Torre Acesa; cinco anos a contar do 401 e do 404), toda **OBRA DO REINO** nova (`reino.py projeto`, em qualquer das quatro cidades) custa **quatro quintos** do preço: cobrar com `ficha.py cofre` o valor já descontado, arredondado para cima. **Não vale** para obra já paga, forja, material, soldo nem para a despesa semanal das guildas. Quem foge, morre, é resgatado ou toma a marca da Mão Queimada sai da conta: com **menos de 44** servindo (a metade) o desconto acaba. Lembrar na auditoria de 5 em 5 dias: contar os forçados.
- **G7 · A SÉRIE DE OFÍCIO (dia 422, palavra do rei; o jogador foi avisado):** a forja grande pode trocar a SÉRIE de armas da semana por uma série de FERRAMENTAS para uma cidade (picaretas, ferraduras e eixos, arados, anzóis e âncoras, lâminas de físico): custo de 300 a 600 conforme a série (a cidade de fora paga metade); UMA série por semana na forja grande, e na semana dela a série de armas não sai (o Herkald não ganha o XP das armas). Outras forjas do reino (a fundição velha de Levis; ferreiros pagos em Farenta) podem fazer uma série ao mesmo tempo, pagas à parte. EFEITO quando fica pronta: **+1 (mod) num pilar da cidade, até o 480** (o inverno; o motivo leva 'até o 480' para vencer sozinho). Não acumula: duas séries no mesmo pilar da mesma cidade valem +1. Não substitui obra: a obra dá passo DE VEZ; a série só ajuda o dado.

### G8 — O MUNDO QUE SE MEXE (pedido do jogador, Dia 422)
- **A (tick.py, corrigida no 423 pelo jogador: 'a PRESSÃO deve rolar 3 eventos'):** quando a PRESSÃO enche, saem **3 EVENTOS DE MUNDO**: 1 LONGE (só terras fora do reino e dos vizinhos), 1 PERTO (Ireviel, Levis, Marasar, Farenta, Lumade, o Delta, o brejo do oeste, a costa) e 1 ALEATÓRIO (qualquer terra). O mundo.py do dia voltou ao de antes (1 novidade por dia, 3 no tick semanal, terra aleatória). O tick do 423 rodou com 3 novidades diárias (a leitura errada do Mestre); o que ele trouxe fica, porque já chegou à casa.
- **B (a cena):** toda cena abre com uma coisa do mundo que chega à casa **só se a casa tiver como saber** (a notícia chegou pelo dado, alguém viu, um espião, um viajante, um sinal no céu). Sem canal, não chega. Nada que JÁ CHEGOU fica guardado pelo Mestre mais de 3 dias.
- **C:** as surpresas e faíscas atrasadas saem, uma ou mais por cena, até zerar a fila.
- **D (faccoes.py):** facção INIMIGA ou hostil **não dorme**: no 2-8 da semana rola 1d6: 1-3 junta gente (força +1) · 4-6 age pelo objetivo (relógio +1). A casa vê o sinal só pelo canal de B.

### G9 — A TRAVA DA LUTA (pedido do jogador, Dia 426, depois do erro da forquilha)
- **Antes de toda luta:** `combate.py monta ...` agora mostra a CONFERÊNCIA (os feitiços e as peças de cada um na ficha, e o que o estado vivo e o cânone dizem que a pessoa carrega) e NÃO MONTA sem `conferido=1`. O Mestre confere peça por peça (gorjal, foco, maça, lança) e o nível, e acerta a ficha antes.
- **Os feitiços entram em lista** (`"magias"` no json; o luta.py usa o primeiro que tem a rodada). Quem tem feitiço forte lança desde a 1ª rodada. O feitiço da Essência que o bicho teme vai na ficha (o fogo contra o Morek).
- **Depois de toda luta:** se alguém morreu ou caiu, o luta.py imprime ⛔ G9 e o Mestre PARA DENTRO DA HORA, antes de o tempo andar, e oferece ao jogador o que o rei sabe: ERGUER O CAÍDO (Luz 6º, até 1 hora), o SERVO ARMADO (a receita do rei), Medicina, onde estão os corpos.
- **Antes de dizer "não dá":** o Mestre procura nos livros (estado vivo, cânone, grimório) o que o rei já sabe e tem. Nada de responder de memória.

### G10 — A PERGUNTA PASSA PELA CABEÇA DE QUEM RESPONDE (pedido do jogador, Dia 427)
- **Pergunta DENTRO DO JOGO** (o que o rei saberia, leria, perceberia ou acharia; o que um conselheiro aconselha): o Mestre rola o saber da pessoa com `python3 saber.py DOMINIO DIFICULDADE "pergunta" [quem=Nome] [mais=N]` e responde do tamanho da margem. Rei bom de forja responde bem de forja; rei fraco de gente responde mal de gente. O conselho também: cada cadeira rola o dela (`quem=Nome`), e quem é do ofício sabe mais.
- **Graus:** FALHA FEIA = a pessoa acredita numa coisa errada (à mesa: "o rei acha que..."; a verdade fica no envelope) · FALHA = não sabe, só o óbvio · SUCESSO = o essencial · GANHO = e um detalhe útil · EXTRAORDINÁRIO = tudo e uma pista nova.
- **O ERUDITO do rei** (talento do 120): 1 vez por sessão vira uma falha num fato verdadeiro que ele plausivelmente saberia.
- **Pergunta FORA DO JOGO** (regras, código, scripts, como o jogo funciona, "você está rolando a pressão?"): resposta inteira e direta, sem dado.
- O que o Mestre já procurou nos livros e é FATO DA FICHA (o que o rei tem, o que ele aprendeu) não se rola: o rei sabe o que está escrito que ele sabe (a G9).

### G11 — A VIGIA DO REINO (pedido do jogador, Dia 428: "temos que traçar planos para os monstros no nosso reino, não quero eles atacando livre"; o jogador foi avisado)
- **O PLANO:** todo monstro Épico ou maior nas terras do reino, e todo Raro que ameace gente, tem uma linha no `campanha_cacada.md`: quem VIGIA, quem CAÇA e em que ordem. A caçada planejada segue a G9.
- **O POSTO DE VIGIA:** gente de olho no bicho (a Guilda, os do Croque, a Luz do Cais, os salineiros, os mineiros, os barqueiros, as torres). Custa **50 por semana por posto** (a Intendente paga, no livro). No máximo **1 posto por bicho**. As torres de vigia de Ireviel (obra, pronta no 449) valem um posto de graça no rio e na várzea de Ireviel.
- **QUANDO O BICHO VIGIADO SE MEXE contra o reino** (o tick traz: caça perto do habitat, gado ou gente some, assalta estrada, destrói ponte ou mina, atrai monstros menores, cria, marca território, aparece de dia), o Mestre rola a vigia: `selo.py dr ID "a vigia de BICHO" d20+2 "1-7: não viu a tempo: o dano vem inteiro | 8-14: AVISO A TEMPO: gente abrigada e gado recolhido, o dano cai pela METADE | 15-21: o aviso e o LUGAR EXATO: o dano cai pela metade e a casa ganha um RUMOR EXATO (fraqueza, toca ou drop) | 22+: o bicho é PEGO NO LUGAR: abre caçada já, com SURPRESA na primeira rodada | 20n: SURPRESA (gerador novidade)"`.
- **O canal (G8-B):** a notícia do bicho vigiado chega no mesmo dia, pelo posto. Bicho SEM posto age livre, como antes (o dado do tick inteiro, a notícia pelo caminho de sempre).
- **Equilíbrio:** a vigia não mata nem afasta o bicho; ela tira a surpresa dele e dá à casa a hora e o lugar. Matar é a caçada.

### G12 — AS GUILDAS DO MUNDO (pedido do jogador, Dia 432: "faltam guildas pelo mundo, de verdade, que agem com chefes"; aprovada como proposta; começa no tick semanal do 434)
- **Seis guildas grandes** fora do reino (`mundo_vivo.json`, "guildas"), geradas no dado (GU1 a GU6 no envelope): o Círculo da Areia Cantante e a Torre dos Sete Véus (magos, Yaelane), os Arpões do Sal Vermelho (caçadores, Shizess), a Ordem da Tocha Branca (cruzados, Telosus), a Companhia do Último Gancho (caçadores, Qulosus) e as Mãos de Breu (ladrões, Qulosus). Cada uma tem CHEFE com nome e nível (175 a 300), dois membros fortes, força 1 a 6, cofre, FAMA, um OBJETIVO com relógio de 8 e uma postura para a casa.
- **Toda semana** o tick roda `guildas.py semana`: d20 por guilda (contratos, recrutas, objetivo, CAÇA DE MONSTRO do bestiário vivo, EXPLORAÇÃO de lugar que guarda núcleo, GUERRA DE GUILDA, compra no mercado, procura a casa, o chefe sobe, gesto público, surpresa). Hostil não dorme (como a G8-D). A tabela inteira está no cabeçalho do `guildas.py`.
- **Elas disputam com a casa:** o bicho que uma guilda mata sai do mundo (e o núcleo é dela); o lugar que ela esvazia fica vazio. O chefe de cada uma é NPC de verdade: entra em cena com `tracos.py`/`npc.py` quando aparecer (a ficha nasce na primeira cena).
- **RANKING DE FAMA** (`guildas.py ranking`), com a Guilda dos Aventureiros de Ireviel (a da casa): ela ganha fama com missão da cidade bem feita (+1), caçada de bicho Épico ou maior (+3), feito grande (+2) (`guildas.py fama casa +N "motivo"`).
- **A notícia** de cada movimento segue a G8-B (pelo dado, com atraso, ou não chega sozinha); o que toca o reino (o rio de Ireviel, um bicho das terras do reino) chega mais fácil.

## MOTOR 8 (Dia 433, pedido do jogador: "pode aplicar todos"): as ideias de D&D e dos RPGs online, G13 a G22
O jogador aprovou as dez de uma vez; o Mestre as escreveu equilibradas. Valem daqui em diante; nada do que já foi rolado muda.

### G13 — O COVIL E AS AÇÕES LENDÁRIAS (luta.py)
- **AÇÕES LENDÁRIAS:** bicho Lendário faz 1 golpe a mais por rodada fora da vez dele, Mítico 2, Primordial 3, sempre em quem o feriu por último (o luta.py faz sozinho pela categoria; `"lendarias": N` na ficha muda o número; gente não tem).
- **O COVIL:** bicho Épico ou maior lutando NA TOCA dele ganha `"covil": {"nome", "dano", "cd", "efeito"}` na ficha. No começo de cada rodada, d6: 1-2 o covil respira · 3-5 acerta um do grupo (resistência d20 + nível ÷ 10 contra a CD: falha, o dano inteiro e o efeito; sucesso, metade) · 6 acerta TODOS (metade do dado; quem resiste não leva nada). O dano do covil vai pelo degrau do bicho (Épico 4d6 · Único 6d6 · Lendário 8d6 · Mítico 12d6 · Primordial 20d6; CD 15 + degrau × 2). Fora da toca, sem covil.
- Antes da luta, a G9 confere também o covil e as lendárias da ficha do bicho.

### G14 — AS MASMORRAS POR SALAS (masmorra.py)
- Lugar fechado (Ithium, Alnesar, Quoium, Iroule, Eryssa e os que vierem) vira um mapa de 5 a 9 salas, gerado no dado na primeira vez que a casa entra ou manda olhos: `masmorra.py gera NOME CAT "o que guarda"`. A última sala é O CORAÇÃO. A tabela das salas está no cabeçalho do script. A casa escolhe o caminho sala a sala; o mapa inteiro fica oculto (`masmorra.py ver NOME`; o Mestre vê tudo com "tudo").
- Uma sala por cena curta; uma masmorra grande leva um dia. Sair e voltar deixa o lugar se mexer (o que habita sabe que alguém entrou: +2 nos perigos da volta).

### G15 — O TEMPO LIVRE DA CASA (toda semana)
- No tick semanal, até 3 NPCs da casa que não estejam em missão fazem UMA atividade (o jogador escolhe; sem escolha, o Mestre pega os parados pela ficha): **TREINAR** (uma perícia ou técnica: +1 de prática; 10 semanas = sobe um grau; custa 50) · **PESQUISAR** (uma pergunta ao Livro pelo saber.py com +2) · **TRABALHAR** (1d6 × 50 ao cofre) · **FESTEJAR** (opinião +5 de alguém; um boato do tick chega à casa; custa 1d6 × 20) · **CURAR-SE** (o ferido sara o dobro na semana). O dado vai pelo selo.py.

### G16 — AS CONDIÇÕES (nome curto, efeito fixo; na ficha da luta e na cena)
- **ENVENENADO:** −2 no ataque; o dano do veneno por rodada até tratar (Medicina CD 15) · **AGARRADO:** não se move; −2 na Defesa; sair: Força ou Agilidade contra a CD de quem agarra · **CAÍDO:** −4 na Defesa contra corpo a corpo; levantar gasta 1 ação · **AMEDRONTADO:** não avança contra o que teme; −2 no ataque; Vontade CD 15 a cada rodada para sair · **CEGO:** −8 no ataque; quem o ataca, +4 · **ATORDOADO:** perde a próxima rodada · **SURDO:** não ouve aviso nem ordem; magia de voz não o pega.
- **EXAUSTÃO** (graus 1 a 5): −1 por grau em todo teste e no ataque; o 5º derruba. Ganha 1 grau: noite sem dormir; marcha forçada; calor forte de armadura (uma tarde); veneno grave. Perde 1 grau por noite de descanso (e o G4 não cura PV na noite em que tira exaustão do grau 3 para cima). Na ficha: `ficha.py set exaustao N "motivo"`; nos NPCs, uma nota.

### G17 — O TESOURO DO COVIL (quando o bicho Épico ou maior morre na toca dele)
- Além do núcleo e dos despojos, d20 pelo degrau do bicho: 1-6 nada além do bicho · 7-12 MOEDA dos que ele comeu: degrau × 1d6 × 100 · 13-16 MATERIAL (gerador.py material, um degrau abaixo) · 17-19 uma PEÇA ANTIGA de quem morreu ali (um degrau abaixo; tem história e às vezes dono vivo) · 20 as três coisas. Pelo selo.py; o que for de alguém, alguém vem buscar.

### G18 — O BÔNUS DE CONJUNTO (a forja do rei)
- Duas ou três peças forjadas ou AJUSTADAS pelo rei para o MESMO portador, com Sob Medida e pelo menos uma Essência em comum, podem ser marcadas como CONJUNTO (o rei declara antes da obra ou do ajuste; o ajuste de uma peça velha gasta uma noite na Fornalha).
- **2 peças:** +1 efeito MENOR de conjunto (d6 pela Essência comum: +1 na Defesa · RD +2 contra a Essência oposta · +1 no ataque · 1x por cena rerrola um teste de resistência · +1d6 de dano da Essência · não pode ser desarmado). **3 peças:** e +1 efeito MAIOR (1x por cena um feitiço da Essência de 1º a 3º círculo sem Mana · ou dobra o efeito menor). O conjunto só vale com todas vestidas; o requisito de nível de cada peça segue valendo.

### G19 — AS MISSÕES DE CLASSE (os heróis da casa)
- NPC herói da casa que passa do nível 100, 150, 200 ou 250 pode abrir uma MISSÃO DE CLASSE (o jogador pede, ou o Mestre oferece quando o NPC chega lá): uma cadeia de 3 passos (gerador.py missao, um grau por passo), na ficção do ofício dele. Cumprida: a classe sobe uma raridade (Comum → Incomum → Rara → Épica → Única → Lendária) e ganha 1 habilidade nova da árvore dele (pelo Livro). Falhada: a cadeia fecha por uma lua. Uma missão de classe por vez na casa.

### G20 — OS EVENTOS DE MUNDO COM PRAZO
- Em toda LUA NOVA, d20: 1-14 nada grande · 15-19 um EVENTO GRANDE é anunciado (d6: 1 uma horda ou bando desce · 2 uma fera grande muda de terra · 3 a coberta afina numa região (magia selvagem, mortos que se mexem) · 4 um torneio ou feira das guildas · 5 um mercado de núcleos e relíquias · 6 uma praga ou fome), com PRAZO de 2d6 + 7 dias à vista de todos · 20 dois eventos.
- Quem participa soma CONTRIBUIÇÃO (feitos na cena; as guildas da G12 rolam a delas, d20 + força × 2); no fim, a recompensa vai pelo ranking: 1º lugar fama +5 e o prêmio grande (núcleo, relíquia ou terra), 2º e 3º prêmio menor; quem não foi, nada. Se ninguém der conta, o evento cobra da terra.

### G21 — A REPUTAÇÃO (reputacao.py)
- Um número de −100 a +100 por cidade, por poder e por guilda (as faixas e o guia estão no script). Abre preço, missão e porta, ou fecha. A partida (433) saiu das relações do reino × 20, das posturas das guildas × 30 e, nas cidades e nos aliados, do que a casa viveu com eles (no envelope).

### G22 — OS TÍTULOS COM EFEITO (habilidades.py titulo)
- Todo FEITO GRANDE do rei (matar pela própria mão bicho Épico ou maior · obra Mítica ou acima · vitória em batalha que ele comandou · julgamento em praça · uma cidade salva) pode dar um TÍTULO (d6 pela ficção do feito: 1-4 nada além da glória · 5-6 um título). O título tem efeito pequeno e estreito (+1 ou +2 num teste ou contra um tipo de inimigo; uma porta que abre) e o mundo o conhece (fama da casa +1). Os títulos somam, mas cada um só vale no que nomeia.
