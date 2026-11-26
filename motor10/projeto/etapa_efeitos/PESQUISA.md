# A PESQUISA DA PARTE 2 (RPG de mesa, jogos, novels e animes, história)

Para a etapa dos efeitos do Motor 10 (o `PROJETO.md` desta pasta, parte 2). Feita para ler no celular: frases curtas, tabelas onde ajudam.

O que as obras fazem fica separado do que propomos. Tudo o que vem sob **PROPOSTA PARA BELOGAR** é desenho nosso: nada disso está no motor ainda, e todo número de proposta é de partida (quem decide é o banco).

---

## 1. Para que serve e como foi feita

**O pedido do jogador, em três linhas:**
1. Efeitos de item fortes, que montam um jeito de lutar (a "build": "15% a mais de dano, 50% a mais", atordoar, sangrar, medo), do fraco ao apelão, balanceados; na forja, quanto mais perto da CD da categoria de cima sem passar, mais efeitos (passou, vira a de cima).
2. Habilidades que dão mais a cada uso (a dança da espada que encadeia golpes, a fúria que cresce), de luta, cura, convencer e trabalho; os estados; os dons ("a cada subida, +2 atributos", "+20% no dano das habilidades", "foge mais longe").
3. Classes de todas as raridades, até as secretas ("paladino, bruxa de sangue"), na trilha de Overgeared (o jogo SATISFY). E "pesquisar RPG de fantasia e animes de RPG, história de RPG".

**Como foi feita.** Cinco frentes, cada uma buscando na rede e lendo as fontes:

| Frente | Achados | Conferidos na fonte | De memória ou fonte fraca |
| --- | --- | --- | --- |
| Novels, manhwa e animes de mundo de jogo | 21 | 15 | 6 |
| RPG de mesa: mecânicas e história | 25 | 14 | 11 |
| Jogos eletrônicos: itens, raridades, afixos, forja | 23 | 17 | 6 |
| Classes, habilidades que crescem e estados (jogos) | 24 | 21 | 3 |
| Histórias de RPG e mitos de ferreiros | 24 | 18 | 6 |
| **Total** | **117** | **85** | **32** |

- Perto de 280 endereços citados (seção 6). Os relatórios das frentes não contaram as buscas: o número exato delas não se sabe.
- **O que não se conseguiu conferir.** A wiki de Overgeared ficou fora da rede desta sessão; os números dela vêm de traduções de fãs que divergem (+7%, +10%, +12%). Ficaram de memória partes de Solo Leveling, Overlord, Log Horizon, Shangri-La Frontier e Tensei Slime. No RPG de mesa: Blades in the Dark, os jogos PbtA, GURPS, Vampiro, a lista de condições da 5ª edição e a 4ª edição. Nos jogos: a força estelar do MapleStory, a têmpera do Diablo IV, as cinzas de guerra do Elden Ring, Borderlands e The Witcher 3. Nos mitos: pedaços do Kalevala, de Goibniu e da Kusanagi.
- **A revisão.** Oito números duvidosos foram conferidos de novo na rede, depois do relatório das frentes (o sangue e o congelamento do Elden Ring, o potencial do MapleStory, a resistência do Darkest Dungeon, a Fúria do Path of Exile, o dano persistente do Pathfinder 2ª, o retorno decrescente do World of Warcraft e as contagens do Shadow of the Demon Lord); onde a fonte desmentiu, o texto foi corrigido e diz o que mudou. As fontes dessa conferência estão no fim da seção 6. A conta da Beira (3.3) foi refeita à parte e bate.
- **As regras desta pesquisa.** Número não conferido leva "(não verificado)". A obra aparece só como fonte: nenhum nome de personagem, habilidade, classe, lugar ou item de outra obra vira conteúdo de Belogar (mito e folclore de domínio público servem de inspiração). Os nomes em MAIÚSCULAS são provisórios: antes da mesa, passam pelo `nomes.py` e pela checagem das três letras contra o cânone.
- **O que o motor já tem, e que muda a leitura de tudo.** A categoria vale ×3 no golpe e +4 no acerto (REGRAS 2.2 e 2.3: "o item decide"). A forja é a Lei do Valor (7.3). A luta tem ferida por parte do corpo, sangue, atordoado, ao chão, moral, preso e o **calejo** (cada controle que pega soma 4 na Firmeza até o fim da luta, 11.2). A **sintonia** (2.9) já é um orçamento de peças. O talento e o dom (10) já existem. E não há nível de MMO: o nível de 1.2 dá só 1 ponto de atributo e um quarto de PV; a escada é a maestria.

---

## 2. O que se aprendeu (as 15 lições maiores)

1. **A categoria é o teto; a feitura é o recheio.** A sobra do dado compra melhorias (Genesys); o raro sai bom ou ruim (Diablo II); o "sopro" do ferreiro lendário dá extras (Overgeared). Em Belogar a categoria vale ×3: o recheio decide entre peças da mesma categoria e nunca vira a de cima.
2. **Separe o tipo do tamanho.** O mesmo efeito cresce em passo fixo pela raridade: 4, 7, 10, 13% (MapleStory); razão perto de 1 : 1,5 : 2 : 2,5 (Hades, não verificado). O jogador aprende o efeito uma vez e lê qualquer peça.
3. **Escreva a regra da pilha antes dos efeitos.** Porcentagem que soma sem regra quebra o jogo (o laço de ofícios do Skyrim). Chance e resistência empilham em curva e nunca chegam a 100% (Risk of Rain 2; a tenacidade do League of Legends).
4. **Potência fixa, duração que cresce.** Vulnerável vale sempre +50% e Fraco sempre −25%; o que empilha são as rodadas (Slay the Spire). O amedrontado N cai 1 por rodada (Pathfinder 2ª).
5. **Todo controle tem freio contra a trava.** O segundo atordoar vale metade, e depois o alvo fica imune por um tempo (World of Warcraft); depois do atordoar vem +50% de resistência (Darkest Dungeon). O motor já tem o seu: o calejo.
6. **Estado construído vale mais que estado sorteado.** A barra de sangria enche golpe a golpe e estoura em 15% da vida máxima + 100 (Elden Ring); a armadura cai antes do controle pegar (Divinity: Original Sin 2). O jogador vê chegar e planeja.
7. **Todo apelão leva um freio que se sente em toda luta.** Devorar só 10 vezes por dia depois do remendo (Bofuri); o dobro de dano recebido na sobrecarga (Hollow Knight); vida 1 ou nunca crítico (Path of Exile); a arma maldita que cobra sangue (Shield Hero).
8. **O que cresce tem teto, quebra e conta.** A fúria acaba no turno em que não se bate nem se apanha (D&D 5ª); a Fúria vai até 50 e decai fora da briga (Path of Exile). Teto pela maestria, zera no erro, cobra cansaço no fim.
9. **Sobe pelo uso, com desconto pelo próprio grau.** Só sobe se o dado passar o valor atual (RuneQuest, Call of Cthulhu); o ganho cai com o nível da arma e nunca passa de um degrau por luta (Final Fantasy II, fórmula da comunidade); cada jeito de treinar tem teto (Mabinogi). O mestre só cresce contra coisa à altura.
10. **Classe rara é prêmio de história.** O assassino de prestígio tem de matar alguém só para virar assassino (Pathfinder 1ª); o cavaleiro sombrio pede 20 mortes e uma rede de ofícios (Final Fantasy Tactics); a cadeia da classe lendária tem prazo e perda para sempre (Overgeared). Três chaves: maestria, feito, segredo.
11. **Raridade de classe sobe a variedade, não o dano.** As classes escondidas se distinguiam pela variedade de estados (Overgeared); poucas portas largas embaixo, muitas estreitas em cima (Shadow of the Demon Lord: 4 caminhos de novato e 16 de perito no livro básico; o editor fala em 24 peritos e 76 mestres, sem dizer se conta os suplementos).
12. **Poder pago com o que gera história.** O golpe divino gasta o recurso depois de ver o acerto (D&D); custo e ganho saem do mesmo dado (Blood Hunter); a magia de sangue corta a cura em 90% (Dragon Age). Troca de recurso sem ganho ninguém usa: o Path of Exile tirou a sua (versão 3.14).
13. **O único no mundo tem dono e muda de mãos.** A habilidade dada a quem reage mais rápido (Sword Art Online); a runa mestra, uma por exército (Warhammer). Em Belogar, o único vem da história gerada e chega por boato.
14. **A peça vale pela história.** A espada do pai, reforjada, racha a bigorna (Gram); o nome ganho por um feito (Kusanagi, não verificado); relíquias no punho (Durendal); o nome do ferreiro gravado na arma (Ragnarok Online).
15. **Quanto mais famoso o ferreiro, mais o poder quer possuí-lo.** O rei aleija e prende o ferreiro (Völundr); o ferreiro vence a guerra sem empunhar (Goibniu); a classe "fraca" de ofício vira a mais forte fabricando (Arifureta).

---

## 3. Por campo

Em cada campo: o que as obras fazem (com números e fonte), o que o motor já tem, e a PROPOSTA PARA BELOGAR.

### 3.1 Os efeitos de item

**O que as obras fazem**
- **Diablo II:** o item mágico tem 1 ou 2 afixos; o raro, de 2 a 6 (até 3 de cada tipo), quase sempre 2 a 4. Dois tipos (prefixo e sufixo) impedem que tudo vire dano.
- **MapleStory (potencial):** a mesma linha cresce em passo fixo: 4, 7, 10 e 13% de atributo principal nas faixas rara, épica, única e lendária, em peça de nível 151 ou mais; até 3 linhas por peça (conferido de novo; peça de nível menor rola menos).
- **Hades:** a mesma bênção em quatro raridades; no Hades II, um dano de 20 a 50% na comum chega a 50 a 125% na heroica (não verificado).
- **Diablo IV:** o afixo maior é o mesmo afixo com 1,5 vez o valor.
- **Slay the Spire:** Vulnerável, +50% de dano recebido; Fraco, −25% de dano feito; Frágil, −25% de bloqueio. A pilha é a duração.
- **Elden Ring:** a sangria estoura em 15% da vida máxima + 100 (+200 na arma que sangra sem a afinidade de sangue; no chefe, 10,5%); o congelamento, em 10% + 30 (no chefe, 7%), e o alvo leva +20% de dano por 30 s, até levar fogo (conferido de novo nas duas wikis do jogo).
- **Hollow Knight:** um amuleto dá +50% de dano por 3 entalhes, e quebra quando o dono morre; passar do orçamento dobra o dano recebido.
- **Lost Ark:** a marca negativa pesa em degraus: −2, −4, −6% de ataque; −5, −10, −15% de defesa.
- **Path of Exile:** a passiva-chave troca uma regra por um preço absoluto (a vida vira 1; nunca crítico).
- **Bloodborne:** bater logo devolve parte da vida perdida (a wiki diz 5 s; os testes, uns 2,5 s).
- **Borderlands:** a lendária tem um efeito que muda o comportamento da arma, com uma frase (não verificado).
- **Mitos:** a lança que não erra (Goibniu), a espada que pede sangue (Tyrfing), o escudo que conta o mundo (Hefesto).

**O que o motor já tem.** Oito efeitos pequenos (sangra, critico_19, derruba, devolve, firme, leve, pesa, nao_quebra). A régua de faixas do PROJETO 2.1, medida no duelo de iguais: fraco, +2 a 5 pontos de vitória; normal, +5 a 10; forte, +10 a 20; apelão, +20 a 40. E a porta: o fraco do Comum, o normal do Incomum, o forte do Épico, o apelão do Lendário.

**Por que os números de Belogar são pequenos.** Uma categoria acima vale ×3 no golpe e +4 no acerto. Só no dano, +15% é cerca de um oitavo de categoria; +50%, pouco mais de um terço; dobrar o dano, dois terços. O item continua decidindo; o efeito decide entre iguais.

**Onde caem os dois números do pedido.** O "+15%" é o Gume da Rara (ou o Fio Faminto, já na Incomum, com o seu risco). O "+50%" é o Gume da Mítica, ou chega antes com preço: o ferro rancoroso na Épica, ou a Sanha cheia de um Mestre (6 pontos, +30%) com um Gume Épico de +20%: grupos diferentes multiplicam (a regra da pilha, abaixo), 1,3 × 1,2, perto de +56%, e só enquanto a Sanha dura. Assim o jogador vê o 15% cedo e o 50% como prêmio ou como conta a pagar.

**PROPOSTA PARA BELOGAR**

1. **Dois tipos de efeito.** Os de NÚMERO (dano, acerto, chance, sangria) crescem com a categoria. Os de REGRA (segundo golpe, ceifadora, imortal) têm faixa fixa e só abrem na categoria da porta.
2. **A porta e quantos cabem.** O teto de efeitos de hoje (REGRAS 7.6 e 7.15) segue da Comum à Lendária; a Beira (3.3) enche até ele. Só a Mítica e a Primordial mudam, e é mudança proposta.

| Categoria | Faixa mais alta | Efeitos na peça (hoje) | Proposta |
| --- | --- | --- | --- |
| Comum | fraco | até 1 | igual |
| Incomum | normal | até 1 | igual |
| Rara | normal | até 2 | igual |
| Épica | forte | até 2 | igual |
| Única | forte | até 3 | e a MARCA-MÃE (3.3) |
| Lendária | apelão | até 3 | e o PODER DE LENDA, com um dito (uma regra só dela) |
| Mítica | apelão | até 3 ("da Única para cima, 3") | até 4 (pede núcleo) |
| Primordial | apelão | até 3 | até 5 (pede núcleo) |

3. **O tamanho, por faixa e por categoria.** Dentro de cada faixa, o primeiro número é o da categoria de baixo.

| Efeito | fraco (Comum) | normal (Incomum · Rara) | forte (Épica · Única) | apelão (Lendária · Mítica · Primordial) |
| --- | --- | --- | --- | --- |
| GUME: dano a mais, no fim da conta | +5% | +10% · +15% | +20% · +30% | +40% · +50% · +60% |
| CERTEIRA: acerto | +1 | +2 | +3 | +4 |
| GUARDA: Defesa | +1 | +2 | +3 | +4 |
| VELOZ: iniciativa | +2 | +4 | age primeiro na 1ª rodada | uma ação a mais na 1ª rodada |
| ATURDIR: perde 1 ação (pela CARGA, 3.2) | não | carga 1 · 2 | carga 2 · 3 | carga 4; no crítico, perde 2 ações |
| SANGRIA | sangra 5 rodadas (o de hoje) | o sangue tira 1/4 do golpe, não 1/5 | SANGRIA ABERTA pela carga: uma ferida leve e 3 rodadas de sangue | JORRA: só para com o amparo da fé ou ferro em brasa |
| MEDO | não | quem ela fere testa a coragem contra 24 | TEMÍVEL: quem a vê erguida testa contra 24, uma vez por luta | PRESENÇA: contra 29, como o líder caído |
| EXPOSTO: o alvo leva +50% de dano de golpe | não | 1 rodada, pela carga | 1 rodada sempre que o golpe fere | 2 rodadas, e o vizinho também |
| VAMPIRA: cura parte do dano feito | não | não | 10% · 15%, dentro do teto da cura do dia | 25% · 30% · 35%, idem |
| PERFURA | não | a proteção conta 0,8 | a proteção conta 0,5 | a armadura conta uma categoria abaixo (a fresta, sem o −8) |
| CRÍTICO | não | o 19 também (o critico_19 de hoje) | de 18 a 20 | de 17 a 20, e o crítico vale ×4 (o golpe do fim do PROJETO) |
| REGENERA (armadura) | não | não | 2% · 3% do PV máximo por rodada, dentro do teto do dia | 5%, e fecha uma ferida leve no fim da luta |

- Se o desenho preferir chance a carga no aturdir: normal 10 a 15%, forte 20 a 25%, apelão 33%, sempre pelo calejo.
- O teto da cura do dia já existe (11.7: nunca mais que metade do PV máximo). A vampira e a regenera entram nele, e por isso não viram imortalidade.
- Quem o jogador comanda, no medo, só fraqueja, e a luta para e pergunta (a regra de hoje, 3.14).

4. **Os efeitos de REGRA, por faixa** (o catálogo do PROJETO 2.1, mais os desta pesquisa):
- **fraco:** leve, não quebra, luz, sangra, CAÇADORA (+15% de dano contra um tipo de bicho).
- **normal:** firme, derruba, devolve, fôlego (o golpe custa 1 a menos), aparadora (+2 na Defesa ao aparar). DESFORRA: ferido nesta rodada, se acerta até o fim da seguinte, a última ferida leve desce um degrau (nunca a grave). FIO MANSO: o erro crítico nunca fere aliado nem inocente, e desarmar ou nocautear ganha +3. FIO FAMINTO: +15% de dano (Rara, +20%), e no erro crítico o golpe pega o aliado mais perto. Os dois fios se excluem.
- **forte:** segundo golpe (uma vez por luta), elemental (fogo ou gelo: um dado a mais por categoria, e a queimadura), refletora (o escudo devolve um feitiço por luta). ENREGELAR, pela carga: +2 em todo golpe contra ele por 3 rodadas; o fogo apaga. ESCUDO QUE CONTA: uma vez por cena, os aliados que o veem saem do abalado.
- **apelão:** ceifadora (quem mata golpeia de novo), tempestade (o golpe pega todos os vizinhos), imortal (uma vez por dia, fica com 1 PV em vez de cair), domínio (solta um feitiço de grau 4 uma vez por dia). PONTA CERTA: uma vez por cena, o golpe que errou por 5 ou menos acerta. O PODER DE LENDA: uma regra só daquela peça, com o seu dito ("a lâmina que lembra: o 3º golpe seguido no mesmo alvo ignora a armadura").

5. **A REGRA DA PILHA** (escrita antes de qualquer efeito):
- O % de dano soma dentro do mesmo grupo (os efeitos das peças) e multiplica entre grupos (peça × técnica × dom). No máximo 3 grupos.
- Toda chance e toda resistência empilham em curva: total = 1 − (1 − a) × (1 − b)... Nunca acima de 75%.
- O golpe de área, o de duas armas e o golpe múltiplo somam metade da carga (arredonda para baixo, mínimo 1).
- O % entra no fim da conta, fora do dado: a explosão do 2d20 não muda.

6. **Como se equilibra o apelão: seis freios, e todo apelão leva pelo menos dois.**
   1. **A porta:** só do Lendário para cima (PROJETO 2.1). Mítica e Primordial pedem núcleo.
   2. **O orçamento:** a peça com apelão ocupa 2 lugares na sintonia (2.9: Vontade ÷ 20). A que passa dorme.
   3. **Um por vez:** um apelão acordado por pessoa; o segundo dorme.
   4. **O teto de usos:** o apelão que se chama tem os usos do dia escritos na ficha (de 1 a 3).
   5. **O preço ou a condição:** um preço que dói (vida, cansaço, um passo de maldição) ou uma condição (só na Sanha, só à noite, só contra quem quebrou um voto).
   6. **O banco:** cada um medido contra a régua (20 a 40 pontos); acima de 40 não entra. E o ano (`provas_ano.py`) confere que os rivais com apelão não matam o dragão no primeiro mês (PROJETO 2.5).

7. **O preço compra um degrau de porta.** A única exceção à porta é a peça que paga:
- FERRO RANCOROSO (a série amaldiçoada de Shield Hero): um apelão já na Épica (ex.: +50% de dano na Sanha), e cada uso anda um passo de uma maldição (o relógio de 6 passos do capítulo 13). Nasce de forja em luto, raiva ou vingança declarada. Só sai com a CONTRAPEÇA, de mesma categoria e forjada em paz, que Ferord pode vender a quem carrega o ferro.
- PEÇA DE VIDRO (Hollow Knight): um forte já na Rara (Gume +30%), que se parte quando o dono vai ao chão numa luta.

### 3.2 Os estados na luta

**O que as obras fazem**
- **Slay the Spire:** potência fixa (Vulnerável +50%, Fraco −25%); aplicar de novo soma rodadas, nunca o %.
- **Pathfinder 2ª:** amedrontado N dá −N em todos os testes e cai 1 no fim de cada turno. O dano persistente para com um teste simples CD 15 no d20 (30%); com uma ajuda que serve ao caso (atar a ferida, jogar água no fogo), CD 10 (55%) (conferido de novo, em fontes secundárias).
- **World of Warcraft:** o mesmo controle repetido logo em seguida dura 100%, depois 50%, depois não pega (por muito tempo foram três degraus, com 25% no meio, numa janela de 18 s). Na expansão Midnight, pelas notas da versão de teste, o jogador fica imune já depois de 2, a janela caiu para 16 s, e os monstros deixam de ficar imunes. (Corrigido: a fração de 1/16 nos monstros não se confirmou.)
- **Darkest Dungeon:** depois do atordoar, +50% de resistência no turno seguinte (+100% se for atordoado de novo; conferido de novo). O sangramento empilha, cada pilha com prazo próprio. Na Porta da Morte, quem zerou não morre na hora, mas cada golpe pede um teste.
- **Pillars of Eternity II:** cada atributo tem três males em degrau (mancando, imobilizado, paralisado); a resistência desce um degrau, nunca zera.
- **Divinity: Original Sin 2:** o controle físico só pega com a armadura física zerada; o mágico, com a mágica; aí pega sempre.
- **Elden Ring:** a barra enche golpe a golpe e estoura contra a robustez do alvo.
- **League of Legends:** as reduções de controle multiplicam: 30%, 30% e 25% deixam 36,75% da duração, não 15%.
- **Total War: Warhammer:** a moral vai de firme a vacilando a quebrada; a unidade que foge vezes demais não volta (o "três vezes": não verificado).
- **Tormenta20:** abalado (−2) de novo vira apavorado, que foge (por resumos de jogadores: não verificado).
- **Warhammer Fantasy Roleplay 4ª:** Medo N tira níveis de sucesso; no Terror N, quem falha ganha N condições de quebrado e vai ao chão.
- **Solo Leveling:** o Medo dá −50% em todos os atributos (de memória: não verificado): legível, e apelão demais para um 2d20.

**O que o motor já tem.** Atordoado (ferida na cabeça: perde 1 ação; grave, 2). O sangue (um quinto do golpe por rodada, 3 rodadas; 5 se grave ou da arma que sangra). Ao chão (−4 na Defesa; levantar custa uma ação) e a perna presa. O veneno (um quarto do golpe por 3 rodadas, −2 no acerto). A moral (fraqueja com −2; quebra: foge ou se rende). A lista fechada do 11.5 (preso, cego, mau-olhado de −4, benzido, enjoado...). Dois freios: o **calejo** e **as penas que não somam** (de mau-olhado, veneno e maldição, vale a pior). E quem o jogador comanda nunca foge nem se rende pelo dado.

**PROPOSTA PARA BELOGAR**

1. **A lista segue fechada; entram três estados (mudança proposta no 11.5).** EXPOSTO (leva +50% no dano de golpe, depois da armadura). AMOLECIDO (faz −25% de dano). ACUADO (o degrau do medo entre o abalado e a quebra). Efeito novo aponta para um estado da lista; estado novo só entra por regra escrita.
2. **Potência fixa, duração em rodadas.** Exposto e Amolecido valem sempre o mesmo; aplicar de novo soma rodadas, até 3; o % nunca soma.
3. **A ESCADA DO MEDO** (a moral do 3.14, com um degrau no meio):

| Degrau | O que faz | Como sai |
| --- | --- | --- |
| ABALADO (o fraquejar de hoje) | −2 no acerto | desce um degrau a cada 2 rodadas sem susto novo |
| ACUADO (novo) | −4; só defende ou recua; não avança contra a fonte | idem |
| QUEBRA (a de hoje) | foge ou se rende | quem fugiu 3 vezes na mesma luta não volta |

Cada golpe de medo é um teste de coragem: falhou, sobe um degrau. Quem o jogador comanda para no abalado, e a luta para e pergunta.

4. **O freio do controle: o calejo para tudo.** Aturdir, preso, ao chão de efeito e medo: cada um que pega soma 4 contra a mesma família até o fim da luta. É o que a magia já mede (a meta M21: o controle pega em 55 a 75%; calejado duas vezes, em 25 a 40%). Chefe e bicho grande começam a luta com um calejo. Ninguém é imune por inteiro: resistir tira 4 ou desce um degrau, nunca zera. Só o corpo dá imunidade (o traço "sem vida" não sangra nem sente medo).
5. **A CARGA, o estado construído.** Aturdir, Sangria Aberta, Enregelar e Exposto de arma não rolam chance por golpe. Cada golpe que acerta soma a carga do efeito (3.1); quando passa da resistência do alvo, estoura e zera. Proposta de resistência: 6 + bônus de Vigor ÷ 2 (chefe e bicho grande, +4). Uma carga para cada família.
6. **A GUARDA ROTA** (Divinity 2). Contra parte do corpo coberta por armadura de categoria igual ou maior que a arma, a carga entra pela metade. Com a peça daquela parte quebrada, ou a parte nua, entra inteira. Casa com a ferida por parte (3.12).
7. **A SANGRIA EM FILETES** (Darkest Dungeon). Cada fonte de sangue é um filete, com prazo próprio; no máximo 3 por pessoa. A ATADURA (1 ação de quem está colado) corta o filete mais forte; o amparo da fé estanca tudo, como hoje. Variante (Pathfinder 2ª): no fim da rodada, 1d20; 15 ou mais estanca sozinho (30%); com atadura, 10 ou mais (55%).
8. **As resistências multiplicam** (a tenacidade do LoL). Duas fontes de 25% cortam 44%, não 50%. Arredonda para baixo; o controle que pegou dura ao menos 1 rodada. A mesma conta vale para todo "% a menos" de Belogar.
9. **As penas não somam** (o 11.5, estendido). De abalo, mau-olhado, veneno, maldição e amolecido, vale a pior; ela soma com a pena do corpo.
10. **O CAÍDO QUE SANGRA** (a Porta da Morte do Darkest Dungeon, à moda do motor). Quem caiu já rola 1d20 contra 12 a cada rodada; com filete aberto, cada rodada dá −2 no próximo teste. O sangue não mata o caído direto: apressa.

### 3.3 A forja

**O que as obras fazem**
- **Genesys (o Star Wars da FFG):** o teste decide se a peça sai; o que sobra no dado (vantagens, triunfos) compra melhorias na peça pronta. Os custos exatos não foram conferidos.
- **Overgeared:** sem o "sopro", a peça sai só com o que a receita dá; com ele, ganha opções, e uma Rara com extras pode passar uma Épica sem. O sopro não dispara sempre (os números das traduções divergem: não verificado).
- **Diablo IV:** a obra-prima antiga dava +5% por grau e +25% num afixo sorteado nos graus 4, 8 e 12 (o sistema já mudou).
- **Lost Ark:** a lapidação começa em 75%; cada sucesso tira 10 da próxima, cada falha soma 10, entre 25% e 75% (o piso, de uma fonte só).
- **Black Desert:** cada falha soma uma "pilha" que aumenta a próxima chance, com teto suave perto de 70% nas armas. A fórmula nunca foi publicada.
- **Ragnarok Online:** a chance soma perícia, atributos, nível e bigorna (até uns +10%). Cada pó de estrela tira 15%; cada pedra de elemento, 20%. Um, dois ou três pós dão +5, +10 ou +40 de dano: o terceiro salta. A arma leva o nome do ferreiro, e há um ranking de ferreiros. (O peso da destreza e da sorte, +0,1% por ponto, é crença da comunidade: não verificado.)
- **Diablo IV e III:** extrair o poder de uma lendária destrói a peça e o guarda para gravar em outra; o Cubo guarda três poderes.
- **Path of Exile 2:** o Orbe Vaal dá um de quatro resultados (nada, refaz afixos, um encanto especial, um encaixe a mais; os 25% cada: não verificado) e trava a peça para sempre.
- **MapleStory:** a força estelar arrisca destruir a peça a partir de 15 estrelas, com proteção paga (as chances se contradizem entre fontes: não verificado).
- **Skyrim:** os ofícios se alimentam (o encanto melhora a alquimia, que melhora o encanto). Sem a falha da restauração, o laço para em uns +29%; com ela, ia ao infinito.
- **Warhammer:** no máximo 3 runas por peça e 1 runa mestra, gravada primeiro; no jogo de batalha, cada runa mestra uma vez por exército.
- **Mitos:** o fole que não pode parar e o martelo que saiu de cabo curto (Brokkr e Eitri); a espada do pai reforjada (Gram); as relíquias no punho (Durendal).

**O que o motor já tem.** A Lei do Valor (CDs 22, 55, 80, 105, 130, 155; o teto pela matéria e pelo núcleo; a porta do degrau). Os dados especiais: cada 20, +1 efeito por escolher até o teto; os dois 20, a obra-prima; um 1, cai uma categoria; os dois 1, perde-se tudo. As ferramentas: a Única dá o QUASE (+1 efeito a 6 ou menos da CD de cima); a Lendária, ACIMA DO FERRO. O teto de efeitos (Comum e Incomum, 1; Rara e Épica, 2; da Única para cima, 3). Quem forjou escolhe o efeito. E uma decisão do jogador: **a chance da Lendária não sobe.**

**PROPOSTA PARA BELOGAR**

1. **A BEIRA, a regra pedida pelo jogador.** Conta-se quanto faltou para a CD da categoria de cima:

| Onde a soma caiu | O que a peça ganha |
| --- | --- |
| faltou 9 ou mais | só a base (e os 20 do dado, como hoje) |
| faltou 4 a 8 | +1 efeito |
| faltou 1 a 3 (o fio da navalha) | +2 efeitos, ou 1 efeito CHEIO |
| passou da CD | a peça sobe uma categoria, e a Beira recomeça na faixa nova |
| no teto (a categoria de cima está trancada) | passar da CD de cima vale +2 |

- **O CHEIO:** o efeito de número sai com o valor de base da categoria de cima. A Rara cheia dá Gume +20%, o da Épica: empata com a Épica magra no efeito, nunca passa. E a categoria segue valendo ×3 no golpe.
- **O teto de efeitos corta, e o que ele corta vira cheio.** A Incomum no fio da navalha leva 1 efeito, cheio.
- **Por que no teto passar vale +2:** com menos, passar da CD daria menos que ficar a 1 ponto dela (o dado ao contrário). A mina de efeitos baratos fica segura pelo teto de efeitos (Comum e Incomum, 1).
- **Quanto sai.** Conta exata do 2d20 explosivo, feita para esta pesquisa e refeita na revisão (bate até a casa decimal), sem os dados especiais e contando a linha "no teto" (não é prova do banco):

| Quem forja (a soma da tabela 7.3) | +1 efeito | +2 efeitos |
| --- | --- | --- |
| Ferord no Dia 34, matéria Comum (2d20 + 21) | 15,5% | 6,8% |
| Ferord no Dia 34, matéria Incomum (2d20 + 36) | 18,8% | 13,5% |
| um Mestre, matéria Rara (2d20 + 65) | 17,9% | 16,5% |
| o mesmo, núcleo Épico (2d20 + 80) | 23,9% | 14,8% |

A Beira dá efeito em 22 a 39% das obras. Somada aos 20 do dado (perto de 1 obra em 10), algo entre 3 e 5 obras em 10 sairão com efeito; a conta exata vai ao banco. A Beira favorece quem está quase subindo de categoria: é o "quanto mais perto, mais efeitos" do pedido.

2. **O QUASE vira alargar a Beira.** Com a ferramenta Única, faltar 1 a 6 dá +2, e 7 a 11 dá +1.
3. **O DADO 1 COM ESCOLHA** (o martelo de cabo curto de Brokkr e Eitri). Um dado abrindo em 1: quem forjou escolhe entre a peça cair uma categoria (hoje) ou ficar na categoria com um DEFEITO DE NASCENÇA: um efeito forte a mais e uma exigência ("só se empunha de luva de ferro", "pesa como a de cima", "não corta em noite sem lua"). A exigência pode pedir a encomenda de uma peça par.
4. **O CALO DO MALHO** (a piedade de Black Desert e Lost Ark). A obra que não alcança a categoria mirada e perde matéria de verdade dá +1 de calo (teto +6; um por dia). O calo soma **só na conta da Beira**, nunca na categoria: a escada medida (Rara no Dia 17, Épica no 59, Única no 177) e a Lendária de 1 em 4 ficam como estão. Se com o calo a soma passaria da CD de cima, vale +2, e a peça não sobe. Zera quando a Beira dá +2.
5. **O MOLDE DE MESTRE** (a criação de receitas de Overgeared). A cada grau de forja, a partir do Treinado, Ferord fixa 1 molde: uma peça e 1 efeito garantido, de faixa até a da categoria mirada. O resto vem da Beira. A peça de molde leva o SINETE do ferreiro: a janela do item mostra quem a fez, a fama sobe quando ela circula, e quem a vê sabe de quem é (bom e ruim).
6. **A MÃO ASSENTADA.** Cada grau de forja acima do Iniciante soma +3% nos números dos efeitos que a pessoa forja (Lendário: +9%). Não mexe na categoria.
7. **O DECALQUE** (copiar um efeito; os aspectos do Diablo IV). Com mão de encanto de Treinado, Ferord desmancha uma peça Rara ou melhor (ela some), e o efeito entra no seu LIVRO DE TALHOS. Gravado em peça nova, sai com o número da categoria de baixo, até ele decalcar 3 peças com o mesmo efeito (aí sai inteiro). O poder de lenda só se decalca com núcleo. E COPIAR O RISCO: um dia estudando uma peça alheia, nas mãos, dá o molde dela um degrau abaixo.
8. **O NOME GANHO** (Kusanagi, não verificado; o nome na arma do Ragnarok). A peça Rara ou melhor que decide um feito registrado ganha nome e 1 efeito ligado ao feito, na faixa da categoria ("Corta-Brasa": resistência a fogo e Gume contra o que queima). Um nome por peça; da Única para cima, dois. O nome anda com a notícia: fama, e cobiça (ladrões, o rei).
9. **A REFORJA DE LINHAGEM** (Gram). A peça quebrada com história entra como MATÉRIA DE MEMÓRIA: +10 na Lei do Valor (+15 se foi de um herói morto), herda 1 efeito, e não sai abaixo da categoria antiga menos uma. Uma vez por linhagem.
10. **O ENXERTO** (o pó de estrela do Ragnarok). Antes de rolar, até 3 enxertos de um mineral raro de Belogar: cada um tira 6 da soma. Um dá Gume +5%; dois, +10%; três, +25% (o salto). Se a soma ainda alcança a CD mirada, a peça sai com o Gume e o nome do ferreiro gravado.
11. **O BANHO NEGRO** (o Orbe Vaal). Uma vez por peça Rara ou melhor, depois de pronta, 1d4: 1, nada; 2, um efeito vira cheio; 3, uma MARCA TORTA (um defeito sorteado: frágil, pesada, ruidosa) e um efeito novo; 4, a peça racha e cai uma categoria. Em todos os casos a peça fica SELADA: não aceita mais nada.
12. **A MARCA-MÃE** (a runa mestra). Só da Única para cima, uma por peça, gravada primeiro. Nenhuma Marca-Mãe se repete no mundo enquanto a peça viver: a segunda tentativa falha, e o ferreiro ouve o nome da primeira.

### 3.4 As habilidades

**O que as obras fazem**
- **Overgeared:** a esgrima herdada do ferreiro lendário libera 5 técnicas, depois 6, depois 7 (não verificado). A fusão perde força, mas garante 3 golpes e tem recarga própria; com a passiva desligada, o herói ganha +10% de ataque, de chance e de dano de crítico (pelas traduções de fãs). As habilidades de ofício nascem de cena (a fúria aprendida numa briga com um ferreiro) e da afinidade com mestres NPC.
- **D&D 5ª, o bárbaro:** a fúria dá de +2 a +4 de dano e resistência ao dano físico, dura 10 rodadas e acaba no turno em que não se ataca nem se apanha. Dois usos no começo; ilimitados no nível 20.
- **Path of Exile:** a Fúria sobe ao bater e apanhar, até 50 (+1% de dano de ataque cada), e cai 1 a cada meio segundo fora da briga. No PoE 2, até 30, e cai mais depressa (conferido de novo).
- **Diablo II:** o Frenesi acelera a cada acerto; a velocidade vale para tudo, o dano só para a própria técnica (não verificado).
- **D&D 5ª, o mestre de batalha:** 4 dados d8 (d10 no nível 10, d12 no 18), uma manobra por ataque; o dado soma ao dano mesmo se o alvo resistir.
- **RuneQuest e Call of Cthulhu:** o sucesso marca a perícia; no fim, rola-se 1d100 e, se passar o valor atual, ela soma 1d10.
- **Final Fantasy II:** cada arma sobe pelo uso, até 16. Pela fórmula da comunidade, o ganho = ataques + grau do inimigo − nível da arma; nunca mais de um nível por batalha.
- **Mabinogi:** cada degrau tem jeitos de treino com teto de vezes; no topo, uma prova.
- **Burning Wheel:** acima de certo ponto, só contam os testes difíceis e desafiadores (os números: não verificado).
- **Romancing SaGa 2:** a técnica nova "acende" no meio da luta, com chance maior contra inimigo do nível da técnica.
- **Final Fantasy V:** o mago azul aprende a magia do inimigo quando ela o acerta (30 magias).
- **Solo Leveling:** o herói extrai o inimigo morto, com chance que cai com a força dele (fórmulas de jogos de fãs: não verificado).
- **Vampire Survivors:** a arma evolui com o nível máximo, a passiva certa e um baú depois dos 10 minutos.
- **Dragon Age: Origins:** a magia de sangue paga com vida, a 80% do custo, e corta a cura recebida em 90%.
- **Ragnarok Online, o ferreiro:** a martelada no chão atordoa numa área de 5 × 5 com 30 a 70% de chance; a aceleração dá +30% de velocidade a ele e +20% ao grupo.
- **D&D 4ª:** poderes à vontade, por encontro e diários (não verificado).

**O que o motor já tem.** A maestria por blocos (Leigo a Lendário; Mestre e Lendário pedem um feito). O PROJETO 2.3 escolheu a escada do Ferir para as habilidades de classe: Iniciante 0, Aprendiz 10, Adepto 30, Perito 80, Mestre 200 e Grão-Mestre 500 usos, cada grau +1 no teste da própria habilidade, nos quatro campos (batalhar, convencer, trabalhar, copiar), com custo em fôlego, Mana ou cargas.

**PROPOSTA PARA BELOGAR**

1. **O freio do uso, para nada explodir.**
- Conta o uso com risco: a luta de verdade, a obra que pode falhar, a fala que pode dar errado.
- Uma marca por cena. Do Adepto para cima, o uso contra quem é mais fraco não conta: usos que contam = usos (até 5) + a dureza do inimigo (1 a 5) − o grau.
- Nunca mais de um grau por dia. Mestre e Grão-Mestre pedem um feito, como a maestria.
2. **Os três ritmos.** DE MÃO (sempre). DE LUTA (uma vez por luta, ou por cena de conversa ou de obra). DE DIA (uma vez por dia: a forte). A de dia não acumula: o mundo dá luta sem aviso.
3. **A que encadeia: a RODA DO MALHO** (a dança do ferreiro).
- Cada golpe da Roda que acerta em seguida dá 1 ELO. Cada elo: +5% de dano nos golpes da Roda, só nela; a cada 2 elos, +1 no acerto.
- O teto vai de 2 elos a 6, pelo grau da Roda: Iniciante e Aprendiz 2, Adepto 3, Perito 4, Mestre 5, Grão-Mestre 6 (os graus da habilidade, do PROJETO 2.3).
- Com 4 elos, o esforço sai pelo fôlego normal, como no Mestre (o que "vaza" para fora da Roda).
- A Roda segue a arma da linhagem: o martelo dos mestres da crônica, ou a lâmina, se o mestre herdado foi de espada. A dança é a mesma; muda o que o fecho faz melhor (o martelo aturde, a lâmina sangra).
- Com 3 elos ou mais, o FECHO gasta a corrente num golpe: a carga de aturdir igual aos elos, ou um filete de sangue de tantas rodadas, ou o golpe que não deixa aparar.
- Errar tira 2 elos (do Mestre para cima, 1). Ser atordoado, ir ao chão ou fazer outra coisa zera.
- As figuras: ABRIR (tira 2 da Defesa do alvo até o próximo golpe), PRENDER (carga de preso), FIEIRA (encadeia), FECHO. Duas figuras usadas juntas muitas vezes dão uma FIGURA FILHA: menos dano, mais certeza (três golpes que não erram por 1 a 4, sem elo).
- Quem luta sem a Roda ganha +5% de dano no estilo próprio: largar a herança é escolha, não erro.
4. **A fúria que cresce: a SANHA.**
- Entra com 1 ação. Cresce com o tempo e com o sangue: +1 ponto no começo de cada turno em que segue na Sanha, +1 por golpe que fere e +1 por ferida recebida, até 2 por rodada. É o "quanto mais tempo em fúria, mais dano" do pedido; o teto e a quebra abaixo seguram.
- Cada ponto: +5% de dano, no fim da conta.
- O teto é a maestria da arma: Iniciante 2, Treinado 4, Mestre 6, Lendário 8 (até +40%).
- Com 3 pontos ou mais, a ferida leve não atordoa. Uma rodada sem ferir nem ser ferido, perde metade.
- O preço: não recua, não guarda, não lança, não faz ofício fino; −2 em juízo; ao sair, +1 de cansaço a cada 2 pontos que teve. É DE LUTA: uma por luta (o Sanhudo de Mestre, duas).
5. **Os TRUNFOS** (as manobras do mestre de batalha). Dois dados d6 por luta no Treinado; três d8 no Mestre; quatro d10 no Lendário. Voltam com um bloco de descanso. Um por golpe, gasto **depois de ver o acerto**: soma o dado ao dado da arma e tenta um efeito. AMEAÇA (coragem contra 24), RASTEIRA (ao chão), CORTE FUNDO (um filete de sangue), TRANCO (+3 de carga de aturdir). O dado soma no dano mesmo se o alvo resiste.
6. **O que cresce dentro da cena, fora da luta.** A Roda e a Sanha somam a cada golpe; o pedido quer o mesmo na cura, na fala e no trabalho. As três seguem o mesmo molde: sobe a cada acerto seguido, tem teto pelo grau, quebra no erro e cobra no fim.

| Habilidade | Campo | Cresce com | Cada ponto dá | Teto (Iniciante · Adepto · Mestre · Grão-Mestre) | Quebra | O preço |
| --- | --- | --- | --- | --- | --- | --- |
| A MÃO QUE ESQUENTA | cura | cada tratamento que dá certo no mesmo dia (ou cada atadura seguida na luta) | +1 no próximo tratamento | 2 · 3 · 4 · 5 | o tratamento que falha zera | +1 de cansaço a cada 2 tratados |
| O FIO DA CONVERSA | convencer | cada teste de fala ganho na mesma conversa | +2 no próximo pedido da cena, e o pedido pode subir um degrau | 1 · 2 · 3 · 3 (até +6) | falhou, o fio rompe e ele lembra (−2) | ele sente a pressão: no 3º ponto, a opinião dele cai 1, ganhe ou perca |
| O MALHO QUENTE | trabalho | cada bloco de bancada seguido na mesma obra, sem parar | a cada 2 pontos, +1 só na conta da Beira (3.3), nunca na categoria | 2 · 3 · 4 · 5 | parar no meio, ou mudar de obra, zera | o cansaço do bloco sobe 1 a cada 2 pontos |

- O Malho Quente soma só na Beira pela mesma razão do calo (3.3, item 4): a escada medida da forja e a Lendária de 1 em 4 não mudam.
- Cada uma sobe de grau pelo uso, com o freio do item 1.

7. **A cura.**
- A MÃO QUE ESTANCA (o ofício cura vira técnica de luta): a ATADURA corta o filete mais forte; no Adepto, dois; no Mestre, firma quem caiu, como o amparo.
- Fora da luta, tratar 2 pessoas por dia no Perito, 3 no Mestre.
- A DESFORRA (dom ou efeito, 3.1): quem bate logo depois de apanhar desce a última ferida leve.
8. **Convencer.** O motor tem a memória e a opinião (22.1), mas não um teste de fala.
- O TESTE DE FALA: 2d20 + bônus de Vontade + a mão de comércio (no negócio) + a opinião do outro sobre você, contra 22 + 4 por degrau do pedido (pequeno, médio, grande, absurdo).
- A PALAVRA FIRME (Blades in the Dark e PbtA; não verificado): antes de rolar, jeito manso (CD −5, ganho menor) ou jeito duro (CD +5, ganho maior; falhou, ele lembra −3).
- Três faixas: passou por 5 ou mais, ganha e leva mais um grau; passou por 0 a 4, ganha com um custo (ele pede algo); falhou, não ganha, e ele lembra (−2).
- Quando a gente do mundo usa a fala no personagem, o dado pesa, mas a escolha é do jogador.
9. **Trabalhar.**
- A LIÇÃO DE BANCADA (Overgeared): a técnica que nasce de cena. BRIO DE OFICINA: +2 na obra com rival olhando; nasce de uma humilhação pública na forja. A PACIÊNCIA: +2 na obra e −1 de cansaço por bloco, um dia, DE DIA; vira passiva no Mestre.
- A AFINIDADE COM UM MESTRE (0 a 5): no 5, o mestre ensina um molde ou uma técnica; Ferord devolve com um bloco de treino junto, e o mestre sobe.
- A PICADA (abrir trilha com a ferramenta que ele fez): 4 blocos de mata custam 3; no Perito, para a comitiva de até 5; no Mestre, a trilha fica no mapa, e inimigos também a usam.
10. **Copiar.**
- COLHER O JEITO (técnica de gente): depois de vê-la 3 vezes, ou de vencer quem a usa. Chance = 50% + 10% por grau de vantagem − 15% por grau de desvantagem, entre 5% e 90%. Três tentativas por técnica; falhou as três, fecha para sempre. A cópia sai um degrau abaixo (+50% vira +35%).
- O ESTALO DE LUTA (o "acender" da série SaGa): em luta de verdade, o golpe com a arma rola, oculto, um estalo: 8% contra inimigo do degrau da técnica nova; 4%, um acima ou abaixo; 0, dois abaixo. Um por luta. À mesa: "algo acendeu".
- As peças se copiam na forja (o DECALQUE e o RISCO, 3.3).
11. **O custo: as moedas que já existem.**

| Moeda | Onde já está no motor | Onde entra |
| --- | --- | --- |
| fôlego | 6 + bônus de Vigor; a arma pesada custa 2 (1.4, 3.10) | as técnicas DE MÃO |
| Mana | (Afinidade + Vontade) ÷ 10 + a mão + o dom (11.3) | o golpe de voto, os feitiços |
| vida | lançar no osso: 5% do PV por ponto; a dívida do pacto: 2% (11.3, 14.2) | o rito de veia, o modo rubro |
| cargas | não há | DE LUTA e DE DIA |
| cansaço | de 0 a 10 (5.2) | o fim da Sanha |
| voto | o voto do clérigo (14.2) | o Juramentado |
| maldição | o relógio de 6 passos (13) | o ferro rancoroso |
| anos de vida | a idade já se escreve (19.6); a velhice é da etapa 7 | o grau 5 da magia, a Marca-Mãe |

12. **Como a habilidade fica maior.**
- O DESABROCHAR (Vampire Survivors): a técnica no topo, uma peça com o efeito certo e um feito (vencer com ela alguém de categoria maior) dão a forma maior, com um efeito que a técnica não tinha.
- O GOLPE GRAVADO (as cinzas de guerra do Elden Ring; não verificado): Ferord grava, numa lâmina que forjou, a técnica de quem a domina; quem empunha a usa com metade da própria maestria. Assim as técnicas de um mestre morto vivem nas peças que ele deixou.
- FUNDIR (Tensei Slime; não verificado): uma habilidade no topo consome outra e vira a forma alta. 5% de chance, +5% a cada tentativa falha, um dia de reclusão cada.

### 3.5 Os dons

**O que as obras fazem**
- **Overgeared:** o jogador ganha 10 pontos fixos por nível; os NPCs, de 6 a 20 ao acaso. Um título de justiça dá +10 em tudo. Uma segunda classe lendária força 6 dos pontos de cada nível para a inteligência. (Tudo pelas traduções de fãs: não verificado.)
- **Skyrim:** o nível do personagem é a soma das perícias (subir custa 75 + 25 × o nível atual).
- **Dragon's Dogma 2:** 6 vagas de aumentos, que passam de uma vocação para outra.
- **Path of Exile:** a passiva-chave troca uma regra por um preço absoluto.
- **Bofuri:** a habilidade estranha nasce do feito que ninguém faz; o remendo põe teto de usos.
- **Sword Art Online:** a habilidade única, dada a quem tinha o tempo de reação mais rápido.
- **Danmachi:** um dom raro de crescer depressa, ligado a um sentimento forte.
- **Ragnarok Online:** renascer dá 100 pontos de atributo (contra 48) e +25% de vida.
- **GURPS:** a desvantagem paga a vantagem; voto e código de honra valem pontos (não verificado).

**O que o motor já tem.** O talento (Negado a Prodígio: a pressa de aprender) e o dom (+1 ou +2 num caminho: o poder), que nascem com a pessoa e ficam escondidos até decidir. O Grande Dom vale um grau de maestria e nada mais (10.7).

**PROPOSTA PARA BELOGAR**

1. **"Subir de nível" vira o GRAU NOVO.** O motor tem um nível (REGRAS 1.2), mas ele quase não pesa: 1 ponto de atributo e um quarto de PV por nível, e nada na luta. A escada de verdade é a maestria. Por isso a proposta pendura o "sobe de nível" do pedido no grau novo: cada grau novo de maestria (Iniciante, Treinado, Mestre, Lendário), em qualquer dos 17 caminhos (os 16 do 10.2 e a manha), é uma SUBIDA. Ser reconhecido numa classe, ou subir um degrau na escada dela (3.6), também é. O nível de 1.2 fica como está, e não se cria outro nível escondido.
2. **A regra geral (proposta).** Cada subida dá +2 pontos num dos dois atributos ligados ao caminho (a tabela vai no desenho), até +6 por caminho. Como o bônus é o atributo ÷ 10, é pouco, e é de propósito.
3. **Os três dons pedidos:**

| Dom | O que faz | O fardo |
| --- | --- | --- |
| SANGUE LARGO ("a cada subida, +2 atributos") | cada subida dá +2 pontos a mais, em quaisquer atributos | o corpo grande come: a fome sobe o dobro |
| MÃO PESADA ("+20% no dano das habilidades") | +20% no dano das técnicas de dano (não do golpe comum) | toda técnica de dano custa +1 de fôlego |
| PÉ LIGEIRO ("foge mais longe") | no recuo e na fuga, anda 3 casas por ação, não 2; o golpe livre de quem fica tem −4; e sai da luta (3.15) mesmo sem alguém segurando a passagem, se quem persegue não tem o mesmo pé | −2 na coragem: o pé quer ir antes da cabeça |

- **A leitura ao pé da letra do Sangue Largo** (mudança proposta, se o jogador preferir): cada nível de 1.2 dá 2 pontos em vez de 1. É mais simples, mas dobra um número que quase não pesa; pendurado no grau novo, o dom se sente.
- **A conta da Mão Pesada:** o dom é um grupo próprio na regra da pilha (3.1, item 5): multiplica com a peça e com a técnica, não soma.

4. **Mais dons, raros, de nascença ou de feito.**
- FOME DE CRESCER (Danmachi): enquanto persegue um desejo declarado, os blocos rendem como um degrau de talento acima; cumprido ou trocado o desejo, o dom apaga.
- COURO DE BIGORNA (Bofuri): a pele conta como couro Comum onde não há armadura, e a armadura protege um décimo a mais; nunca mais sobe Força nem Agilidade.
- OLHO DE LIGA: lê a categoria e os efeitos de uma peça só de olhar; e diz o que vê (−2 na fala de negócio).
- DOM SEM PAR (Sword Art Online): cada mundo sorteia de 3 a 5 dons únicos, cada um preso a uma medida (o que mais forjou Raras, o que sobreviveu a mais feridas). O dono é quem lidera a medida; o dom pode migrar, por rolagem oculta, a cada estação. O jogador sabe por boato.
5. **Os DONS DE FEITO (o FEITO TORTO).** Uma tabela escondida de feitos incomuns; quem faz primeiro no mundo ganha um dom único. Exemplos: forjar com o metal ou o osso do bicho que você mesmo matou; apanhar 20 golpes numa luta sem revidar; trabalhar 3 dias sem dormir na forja. Todo dom de feito leva a LEI DO CANSAÇO: os usos do dia, escritos na ficha.
6. **As ALCUNHAS (os títulos).** O povo dá nome a um feito público ("o que forjou a lâmina do conde"). A alcunha anda com a notícia (22.3): onde a notícia chegou, +2 na fala e no preço; onde é boato, +1. No máximo 3; a alcunha ruim também anda.
7. **Os VÍCIOS DE OFÍCIO** (os aumentos do Dragon's Dogma). Cada caminho no Treinado deixa uma passiva pequena, que vale em qualquer classe (martelo: +1 contra ir ao chão; cura: a atadura corta 1 filete a mais; comércio: +1 na primeira fala do dia). Três vagas (+1 no Mestre); trocar leva um dia.
8. **Os JURAMENTOS** (a passiva-chave do PoE): o dom que troca uma regra por um preço absoluto.
- MÃO CERTA: o golpe que erra por 1 a 4 acerta; o dado nunca explode nem dá crítico.
- CORPO DE PEDRA: imune a sangria e a veneno; nunca corre nem foge (1 casa por ação).
- SANGUE NO FEITIÇO: o feitiço custa uma ferida leve em vez de Mana e sobe um grau de efeito.
- Um por pessoa. Desfazer custa um ano de vida ou um núcleo.
9. **A regra do fardo** (GURPS; não verificado). Todo dom forte traz um fardo que morde em cena pelo menos uma vez a cada 10 dias; se não morder, o Mestre cria a cena.
10. **O banco segue o 10.7.** Cada dom medido como foi medido o Grande Dom: nenhum vale mais que um grau de maestria; os de feito, no máximo dois.

### 3.6 As classes

**O que as obras fazem**
- **Overgeared:** a classe lendária de ferreiro é antes de tudo de ofício (avaliar, consertar, reforçar, criar). Traz ainda usar qualquer item, quase imunidade a estados e a esgrima herdada. Vem por herança; ao trocar de classe, o nível do herói zerou.
- **Overgeared (o ranking):** dos 10 primeiros, só um tinha classe escondida; a diferença estava na variedade de estados.
- **D&D 3.5 e Pathfinder 1ª:** a classe de prestígio só abre com requisitos (perícias, e às vezes um feito: o assassino mata alguém só para virar assassino).
- **Final Fantasy Tactics:** o mímico pede ofícios no nível 8 e no 5; o cavaleiro sombrio, 20 mortes e dois ofícios dominados.
- **Dragon Quest VI:** a vocação de cavaleiro sagrado pede dominar duas básicas (as fontes divergem em quais: não verificado).
- **Shadow of the Demon Lord:** caminho novato no nível 1, perito no 3, mestre no 7; poucos largos embaixo, muitos estreitos em cima.
- **Tormenta20:** cada classe escolhe "poderes" numa lista, em vários níveis; há uma classe de inventor.
- **Ragnarok Online:** o ferreiro que luta (a martelada no chão, a aceleração, fortalecer a arma), em cadeia de pré-requisitos; e o renascer.
- **Diablo II e D&D, o paladino:** uma aura por vez (a de força dá +40% no nível 1); o golpe divino.
- **Blood Hunter e Dragon Age:** o caçador e o mago que pagam com sangue.
- **Solo Leveling e Overgeared:** a missão de troca de classe como prova de uma vez só (de memória: não verificado).
- **Arifureta:** a classe "fraca" de ofício que vira a mais forte fabricando.

**O que o motor já tem.** Nenhuma classe no Motor 10. O PROJETO 2.3 traz do Ferir a classe com três assinaturas e uma fraqueza. (Os nomes de classe do compêndio do Ferir não se repetem aqui: Belogar tem os seus.)

**PROPOSTA PARA BELOGAR**

1. **A classe não se escolhe num menu: o mundo RECONHECE.** O título vem quando a maestria, o feito e o segredo se juntam.
2. **A escada:**

| Degrau | Quantas | Como se ganha | O que dá | O preço |
| --- | --- | --- | --- | --- |
| Comum | muitas, largas | Iniciante num caminho e o trabalho visto (um mestre, a vila) | 1 técnica de mão | quase nenhum |
| Incomum | muitas | Treinado e o exame de quem sabe (a irmandade, o mestre) | 2 técnicas | a fraqueza |
| Rara | dezenas | duas maestrias de Treinado e uma PROVA de uma vez só (falhou, a porta fecha) | 3 assinaturas: uma de cada mãe e uma própria | fraqueza e voto, ou fardo |
| Épica | poucas | Mestre num caminho, Treinado noutro, um FEITO do mundo e o SEGREDO (quem ensina, ou o escrito) | uma assinatura forte | um preço que dói |
| Única | uma viva por vez | Mestre em dois caminhos e um feito grande; passa a quem supera o dono | a assinatura que ninguém mais tem | a cobiça: o mundo sabe |
| Lendária | uma por mundo | o LEGADO de um morto da crônica (a peça, o caderno, a oficina), a mão Lendária e a cadeia de missões | uma identidade: muda o que se faz no mundo | o custo de entrada |
| Mítica | quase nenhuma | um núcleo Mítico, ou um pacto, ou um ano de vida, e um rito | uma regra do mundo dobra | o preço do pacto, no SÓ O MESTRE |
| Primordial | uma, adormecida na crônica | só por evento do Mestre: um núcleo Primordial e o lugar que a história de Belogar guarda | o mundo muda ao redor de quem a tem | o mundo inteiro quer o que ela guarda |
| Secreta (o véu) | não há lista | só por FEITO TORTO, de Rara a Lendária | o inesperado | o fardo que nasce junto |

3. **As três chaves** (a classe de prestígio): NÚMERO (a maestria), FEITO (registrado no cânone) e SEGREDO (alguém ensina, ou um escrito se acha). O jogo nunca lista a chave inteira: as pistas vêm do que a gente do mundo sabe, da notícia e do boato.
4. **A raridade sobe a variedade.** O dano-base quase não muda com a raridade (de 0 a +10%); o que sobe é o número de estados e de ferramentas: Comum 1, Incomum 2, Rara 3, Épica 4, Única e Lendária 5 ou mais.
5. **A fraqueza e o voto.** Toda classe tem uma fraqueza escrita (como no Ferir); da Rara para cima, um voto ou um fardo que morde em cena. Quebrar o voto apaga a classe e pode abrir a secreta sombria (o Juramentado vira Cinza-de-Voto).
6. **Duas identidades.** Uma classe por vez; uma segunda, só da Rara para cima, cobra TRIBUTO (Overgeared): metade dos pontos de cada subida vai para o atributo dela.
7. **O caminho natural de Ferord** (forja e encanto): MALHADOR, TEMPERADOR, MARCADOR DE RUNAS, MESTRE DE MOLDE e, se a cadeia vier, o LEGATÁRIO DA BIGORNA.

**As ideias de classe (38, de todas as raridades; as secretas no fim):**

| Classe | Raridade | O que faz (e a fraqueza) | Como se ganha |
| --- | --- | --- | --- |
| MALHADOR | Comum | o ferreiro de vila: conserta 10 pontos por bloco, não 5, e lê a categoria de uma peça à vista; fraqueza: nenhuma técnica de luta | forja de Iniciante e 20 dias de jornal numa oficina |
| GUARDA-LINHA | Comum | segura a casa: +2 na Defesa com a ordem segurar; fraqueza: −2 no acerto ao avançar | arma de Iniciante e 30 dias na guarda de um lugar |
| MATEIRO | Comum | rastro e emboscada: +2 no rastro; no ermo que conhece, nunca é surpreendido; fraqueza: −2 entre muros | caça de Iniciante e 10 saídas ao ermo |
| ERVEIRO | Comum | colhe e trata: o remédio dele vale meio dia a mais de repouso; fraqueza: foge da luta | coleta e cura de Iniciante |
| TROPEIRO | Comum | o mercador de estrada: o pedágio sai pela metade, e ele sabe o preço do outro lado; fraqueza: a carga atrai o bando | comércio de Iniciante e 5 viagens de negócio |
| BENZEDOR | Comum | a fé do povo: benze porta e ferramenta (o ferro de soleira da casa) e sente o mau-olhado; fraqueza: não cobra a bênção | fé de Iniciante e 10 bênçãos dadas de graça |
| RISCADOR | Comum | o encanto de pedra: grava o grau 1 com um bloco a menos; fraqueza: o encanto falho tira 5 de durabilidade a mais | encanto de Iniciante |
| TEMPERADOR | Incomum | o ferreiro que lê a matéria: a Beira alarga 1 ponto, e ele sabe se a matéria presta antes de abrir a obra; fraqueza: −2 fora da própria oficina | forja de Treinado e a obra-mestra aprovada pela irmandade |
| BESTEIRO | Incomum | recarrega de graça uma vez por luta; mira a fresta com −6, não −8; fraqueza: colado, perde a ação | tiro de Treinado e uma estação numa muralha |
| ESTANCADOR | Incomum | a atadura corta 2 filetes, e o tratamento dele soma 2 dias de repouso, não 1; fraqueza: não recusa socorro | cura de Treinado e 20 feridas tratadas |
| PREGOEIRO | Incomum | a voz da praça: +2 na fala, e no leilão o preço sobe; fraqueza: todo mundo o conhece | comércio de Treinado e um leilão vencido |
| ANTEPARO | Incomum | põe o corpo na frente: guardar não gasta a reação, uma vez por rodada; fraqueza: não ataca no turno em que guarda | arma de Treinado e ter guardado alguém numa luta em que caiu |
| MALHEIRO DE GUERRA | Rara | o ferreiro que luta: TREMOR DE BIGORNA (área de uma casa, carga de aturdir de 2 a 4 pela mão), FOLE ACESO (3 rodadas de esforço pelo fôlego normal), FIO ASSENTADO (Gume +5% na arma de um aliado por um dia); fraqueza: só com arma de peso | forja e peso de Treinado; a prova: matar alguém à altura com uma arma da própria mão |
| MARCADOR DE RUNAS | Rara | forja e encanto numa obra só: a peça nasce encantada, sem os blocos do encanto; fraqueza: o encanto que falha racha a peça (cai uma categoria) | forja e encanto de Treinado; a prova: uma peça que nasce encantada na primeira tentativa |
| JURAMENTADO | Rara | o voto em armas (o paladino de Belogar): GOLPE DE VOTO (depois do acerto, 2 de Mana da fé: +20% de dano, +40% contra o que o voto combate; um por rodada) e CHAMA DE VOTO (uma aura por vez, a 3 casas: do escudo, +2 na Defesa; da lâmina, +10% de dano; do firme, +4 contra o medo); fraqueza: o voto | fé com voto e uma arma de Treinado; a prova: cumprir o voto quando custou caro |
| SANHUDO | Rara | a fúria de Belogar: a SANHA (3.4) e, com 5 pontos, a primeira ferida grave da luta vira leve; fraqueza: na Sanha não recua nem guarda | arma de Treinado e vencer uma luta abaixo de um quarto do PV |
| SANGRADOR DE CAMPO | Rara | o cirurgião de guerra: CORTE FUNDO (filete pela carga), a ATADURA na luta, e trata dois por dia; fraqueza: o povo o teme (−2 na fala com quem ele não tratou) | cura e fio de Treinado; a prova: salvar quem já rolava a morte no chão |
| ESPREITADOR | Rara | caça e tiro: PRESA JURADA (+15% de dano contra o bicho jurado, que não o perde de vista); fraqueza: −2 contra gente | caça e tiro de Treinado; a prova: caçar sozinho um bicho de grau C |
| MEDIANEIRO | Rara | o negociador entre casas: a PALAVRA FIRME com +2, e acha a brecha de um contrato; fraqueza: quem perde a mediação lembra (−3) | comércio de Treinado e manha de Iniciante; a prova: fazer duas casas largarem o aço |
| SANGRADEIRA | Épica | a bruxa de sangue: RITO DE VEIA (perde 1d6 de PV que nada reduz; +1d6 no dado de cada golpe ou feitiço até o fim da cena; d8 e d10 com a mão), MODO RUBRO (o feitiço custa vida a 80%, sobe um grau de efeito, e a cura recebida vale um décimo), as GOTAS (guarda até 5, do sangue de quem caiu sangrando perto; cada uma paga um rito); fraqueza: sem cura de magia na cena do rito, e a MANCHA que o povo vê | pacto de Mestre e fio de Iniciante; o feito: pagar uma dívida inteira com o próprio sangue; o segredo: uma sangradeira viva ensina |
| MESTRE DE MOLDE | Épica | a assinatura do ferreiro: os MOLDES e o DECALQUE (3.3), e as peças dele valem +25% na loja; fraqueza: o sinete (quem vê sabe de quem é, e o rival estuda) | forja de Mestre; o feito: uma Épica com o seu sinete nas mãos de outro; o segredo: um caderno de mestre |
| ALFERES | Épica | o portador do pendão: aliados a 3 casas, +2 na coragem; o grupo ganha a ordem "formar" (o flanco não lhes tira Defesa); fraqueza: se o pendão cai, todos testam a coragem | arma de Mestre; o feito: comandar e vencer com metade do seu lado no chão |
| CHAMADOR DO ERMO | Épica | o druida de guerra: chama até 2 bichos do ermo do laço, e a fera do laço não o ataca; fraqueza: o laço (o ermo caçado o enfraquece, como hoje) | verde de Mestre e caça de Treinado; o feito: tirar uma frente do ermo do laço |
| ARMADOR DE HOSTE | Épica | a oficina de três mãos: com carpinteiro e rebitador, a tropa começa cada dia de batalha com as armas inteiras, e ele faz por noite uma peça Comum por grau; fraqueza: o inimigo manda matar o ferreiro | forja de Mestre; o feito: servir numa guerra de verdade |
| REI DOS MALHOS | Única | o primeiro do ROL DOS MALHOS (3.8): a encomenda do rei e da guilda vem a ele; fraqueza: quando outro passa no rol, a classe muda de mãos | ser o primeiro do rol por uma estação inteira |
| CAÇADOR DO ÚNICO | Única | sobreviveu a um ser único da história: a MARCA (naquela parte do corpo não se veste armadura; +2 para seguir e entender o ser), e a carcaça dele vira peça Única por definição; fraqueza: o ser, ou a cria, vem atrás | sobreviver a um ser único e ficar com uma parte dele |
| GRAVADOR DO NOME | Única | o único vivo que grava a MARCA-MÃE; fraqueza: cada Marca-Mãe custa um ano de vida | encanto e forja de Mestre; o segredo: o escrito da Marca-Mãe |
| LEGATÁRIO DA BIGORNA | Lendária | a herança de um mestre ferreiro morto: a RODA DO MALHO com as figuras dele, ler a peça uma categoria acima, consertar sem perder, +4 contra estados (não imunidade) e a ferramenta Lendária do mestre (uso: só o herdeiro); preço de entrada: a maestria de armas volta um grau (os blocos voltam na metade do tempo) | a CADEIA DO LEGATÁRIO (3.8) |
| FIADOR DE JURAS | Lendária | o Juramentado que o reino conhece: quem jura diante dele não mente naquele dia, e a Chama de Voto pega o grupo todo; fraqueza: se quebra um voto, vira Cinza-de-Voto na hora, e a chama vira medo dos seus | ser Juramentado com fé de Mestre, manter um voto por um ano e receber o legado de um santo da crônica |
| FERREIRO DO FRIO | Mítica | forja sem fogo: a peça fria fere espírito e fada como prata e recusa encanto inimigo; uma vez na vida, passa do teto sem núcleo; fraqueza: o fogo não o aquece mais (o frio vira pena do corpo) | um núcleo Mítico e um rito numa noite do latido |
| HERDEIRO DO PRIMEIRO FOLE | Primordial | o fogo que o primeiro ferreiro tomou de quem não devia (O PRIMEIRO FOLE, 3.8.2): onde ele acende o fogo, a oficina conta 4, mesmo no ermo; uma vez por estação, a peça que ele forja nasce com uma Marca-Mãe sem gravador; nenhuma peça dele dorme na sintonia de quem ele escolhe (uma pessoa por vez); fraqueza: o fogo o reconhece, e em ano de praga ou de fome o povo inteiro sabe quem ele é; a coroa e a igreja querem o fogo de volta | nenhum caminho escrito: um núcleo Primordial, a mão Lendária de forja, e o lugar onde a crônica de Belogar diz que o primeiro fogo dorme (evento do Mestre) |
| CINZA-DE-VOTO | Épica, secreta | o Juramentado cuja chama apagou: o golpe de voto dá abalo em vez de dano, e a chama assusta todos a 3 casas, aliados também | quebrar o voto de Juramentado |
| ECO DE FERIDA | Épica, secreta | copia a técnica que o feriu (20, 35 ou 50% pela mão); guarda 3, um degrau abaixo, pelo dobro do custo | sobreviver a 3 técnicas diferentes que o derrubaram |
| SOLDADOR DA ENCRUZILHADA | Épica, secreta | o pacto do ferreiro: SOLDA DE PACTO (junta matérias que não se juntam: +1 efeito) e GRILHÃO SOLDADO (prende a um objeto até vencer Força contra 28); fraqueza: a entidade vem cobrar (o preço no SÓ O MESTRE) | um pacto feito em cena numa encruzilhada |
| BIGORNA-VIVA | Rara, secreta | quanto mais apanha, mais devolve: cada golpe recebido sem revidar dá 1 brasa (até 5); solta todas num golpe (+10% de dano por brasa); fraqueza: −2 no acerto enquanto junta | apanhar 20 golpes numa luta sem revidar, e viver |
| OSSEIRO | Rara, secreta | forja com osso e couro do bicho que ele matou: a PARENTELA (2 peças da mesma fera, +1 numa resistência; 4 peças, a espécie não o assombra); fraqueza: aquela espécie o caça | forjar com a matéria de 3 bichos, de espécies diferentes, que ele mesmo matou |
| INSONE DA FORJA | Rara, secreta | trabalha de noite sem a pena do sono na bancada; fraqueza: a cama cura pela metade | 3 dias sem dormir na forja, e uma obra Rara no fim |
| VOLTADO DA COVA | Lendária, secreta | quem a morte soltou três vezes: uma vez por luta, ao cair, rola a morte com +4 e, se fica estável, levanta no fim da rodada com um quarto do PV; o medo nele para no abalado (desce um degrau, não zera); fraqueza: a cura de magia nele vale a metade, e os mortos de Belogar (o morto do morro, o espírito) o reconhecem e vêm falar | cair e rolar a morte no chão em três lutas diferentes, ficar estável nas três sem amparo de ninguém, e viver para contar |

### 3.7 A magia que muda tudo

**O que as obras fazem**
- **Overlord:** no nível 100, até 30 feitiços de supergrau, no máximo 4 por dia e sem mana; o desejo gasta a experiência de quem lança (não verificado).
- **Tensei Slime:** a habilidade tenta subir milhares de vezes, falha, e só sobe consumindo outra (não verificado).
- **Dragon Age:** a magia paga com vida a 80% do custo, e a cura recebida cai 90% enquanto o modo está aceso.
- **D&D:** o paladino decide gastar depois de ver o acerto; o crítico dobra os dados.
- **O que fica:** o feitiço supremo tem teto por dia e um custo que não é mana (a vida, o crescimento, os anos).

**O que o motor já tem.** 24 feitiços e o truque, graus 0 a 4, quatro tradições. Estudar custa 3, 6, 18, 54 e 162 blocos. O grau 4 pede a mão Lendária (abaixo dela, o lance forçado tem −4 por grau que falta). O retrochoque (1 em 400; no forçado, 1 em 10), a Mana, o lance no osso. O PROJETO 2.4 já pede um quinto degrau com custo de verdade (muita Mana, um núcleo, anos de vida).

**PROPOSTA PARA BELOGAR: o GRAU 5**
1. **Aprender:** 486 blocos (a mesma escada, vezes 3), e só de fonte rara: um escrito achado (a masmorra funda, o tesouro do dragão) ou um mestre morto (o MORRO DO MESTRE, 3.8). Ninguém vivo ensina.
2. **Lançar:** pede a mão Lendária e um feito de tradição; nunca é forçado.
3. **O preço**, escolhido ao lançar (um dos três): um núcleo Lendário ou maior; um ano de vida (o povo de vida longa paga cinco); ou um grau da mão da tradição, que some com os blocos (o RITO DE SANGUE VELHO).
4. **O teto:** uma vez por estação. O retrochoque sai num 1 no primeiro dado (1 em 20), e então o feitiço pega quem lançou.
5. **A marca no mundo:** o lugar onde se lança vira lugar maldito por uma estação (13.3), da categoria do foco. A notícia corre (22.3), e o rei e as guildas ficam sabendo.
6. **Um por tradição, para começar:**

| Tradição | Feitiço | O que faz |
| --- | --- | --- |
| arcano | A HORA PARADA | uma rodada inteira em que só quem lançou age |
| arcano | CHUVA DE BRASA | 3d8 em todos de três casas seguidas, amigo ou inimigo; a ferida queima |
| fé | O CHAMADO DE VOLTA | quem caiu nesta luta, mesmo morto nela, volta de pé com um quarto do PV; uma vez na vida de cada um |
| verde | O ERMO EM ARMAS | todo bicho do ermo do laço, até a categoria do foco, vem lutar; o ermo perde a fartura de uma estação |
| pacto | A DÍVIDA PASSADA | a dívida inteira da bruxa vai para o alvo, como maldição da categoria do foco |

7. **A medida.** Entre iguais, o grau 5 vale um apelão (20 a 40 pontos), nunca mais. E a **régua dos 24** (PROJETO 2.4): os feitiços de hoje medidos pela mesma régua de faixas, e os fracos demais sobem.

### 3.8 A história

#### 3.8.1 De onde vem tudo isto (o RPG em poucas linhas)
- **1971:** Chainmail, de Gygax e Perren: jogo de miniaturas medievais, com um suplemento de fantasia.
- **Blackmoor**, de Dave Arneson: o exército vira pessoa; dali vêm a experiência e o nível (quem fez o quê é disputado).
- **1974:** Dungeons & Dragons, de Gygax e Arneson, pela TSR; três classes no começo (não verificado).
- **1975:** o suplemento Greyhawk traz o ladrão e o paladino; sai Tunnels & Trolls, que no ano seguinte (1976) lança a primeira aventura solo (as datas: não verificado).
- **1978:** RuneQuest, sem classes: a perícia sobe pelo uso (a data, não verificada; a regra, conferida no Call of Cthulhu).
- **Começo dos anos 1980:** Ultima e Wizardry abrem o RPG de computador (as datas: não verificado).
- **1986 a 1990:** Dragon Quest junta o mapa do Ultima e a batalha do Wizardry; o primeiro Final Fantasy (1987) tem seis classes fixas; o Final Fantasy III (1990) cria a troca de ofício.
- **1996 e 2000:** Diablo e Diablo II fazem o saque com afixos e a cor da raridade (não verificado nesta pesquisa).
- **No Brasil:** Tagmar (1991), tido como o primeiro RPG feito por brasileiros; Tormenta (1999), da equipe da revista Dragão Brasil; 3D&T, o jogo nacional mais famoso; Tormenta RPG e Old Dragon (2010); Ordem Paranormal, série do streamer Cellbit que virou livro de RPG de mesa. (A Dragão Brasil em 1994, o Tormenta20 em 2019 e as datas do Ordem Paranormal: não verificado.)
- **Fim dos anos 1990:** as web novels coreanas nascem nas redes de linha discada (Chollian, Nownuri, HiTEL); Dragon Raja, de Lee Young-do, é o marco; depois vêm os portais (Munpia, Kakao Page).
- **2002:** .hack e a web novel de Sword Art Online fazem o "mergulho completo" no jogo virtual; **2010:** Log Horizon, publicado na rede (impresso a partir de 2011), leva a sério a economia e a gente.
- **Anos 2000 e 2010:** The Legendary Moonlight Sculptor (o escultor) e Overgeared (o ferreiro): a classe de ofício desprezada que vira lenda (as datas: não verificado).
- **A lição para Belogar:** o motor herda do RuneQuest (sobe pelo uso), não do D&D (o nível). Está no PROJETO do Motor 10: "a peça pesa mais que o nível, aprende-se fazendo, e a vida é única".

#### 3.8.2 Os ganchos para Belogar
Entram no mundo de verdade só por evento do Mestre, com o jogador sabendo (PROJETO 2.5). Os mestres, as peças e os lugares saem da história gerada de Belogar; aqui ficam só os moldes.

1. **A CADEIA DO LEGATÁRIO** (Overgeared). O gatilho: o rastro de um mestre ferreiro morto da crônica. Elo 0, ACEITAR O FARDO: só de aceitar ganha uma técnica pequena na hora, e abre um prazo (a guardiã do segredo vive 2d20 dias, rolado oculto, no SÓ O MESTRE). Elos 1 a 4, OS GOLPES PERDIDOS: cada um num lugar do mapa (uma pedra entalhada, um livro numa abadia, a ferramenta no túmulo, o último num concurso com o rival); cada elo dá a reforja de memória de uma peça do mestre (sai Rara, sem os efeitos de nome). Falhou o prazo: os elos que dependiam dela somem para sempre, e o resto fica mais difícil. O fim: a classe Lendária e a ferramenta "só do herdeiro".
2. **O MORRO DO MESTRE** (o Despertar de Angantyr). O túmulo cercado de fogo-fátuo (coragem contra 26 para passar). Lá dentro, o teste de fala com o morto: cada verdade sobre a linhagem ou o ofício dá +5; mentir sobe a CD em 10, e ele ataca. Ele entrega UMA coisa: o caderno (uma técnica perdida), a ferramenta (Única) ou a peça amaldiçoada. O aviso dele é lido antes da escolha.
3. **A SEDE DA BAINHA** (Tyrfing e Dáinsleif). Efeito Mítico, só por núcleo ou por forja sob coação: +50% de dano e a ferida que não fecha. Desembainhou, a cena termina com sangue (de alguém); senão, o dono se fere no braço que empunha. Três desgraças ficam ocultas no SÓ O MESTRE. O poderoso que forçar Ferord a forjar pode receber exatamente isto.
4. **O CONCURSO DO FOLE e A BRECHA DO CONTRATO** (Brokkr e Eitri). Forja em dupla, em três fases; o ajudante testa Vigor ou Vontade contra 24, 28 e 32. Um rival pode pagar um sabotador (rolagem oculta; +4 na CD da fase). Falhou uma fase, a peça sai com DEFEITO DE NASCENÇA. E o contrato do concurso pode trazer uma brecha que o jogador acha perguntando a quem sabe.
5. **A PEÇA QUE PROCRIA** (o anel do mesmo mito, que pinga oito iguais a cada nona noite). Anel ou moeda Lendária ou Mítica que a cada 9 noites gera 1d3 cópias Comuns de si. O rei vai querer.
6. **A REFORJA e A PROVA DA BIGORNA** (Gram). O jovem nobre que traz a espada partida do pai e quebra na bigorna as duas primeiras que Ferord fizer. A prova pública (a bigorna, a armadura conhecida) sobe a fama na cidade.
7. **O SOLDADOR DA ENCRUZILHADA** (O Ferreiro e o Diabo, conto tipo ATU 330; um estudo de 2016 dá a ele uns 6 mil anos, e há quem conteste). O poder de ofício virado arma (soldar tudo, prender o cobrador); a cobrança volta. Em várias versões, o ferreiro que engana o diabo não tem lugar nem no céu nem no inferno (de memória: não verificado).
8. **A OFICINA DE TRÊS MÃOS, a PONTA CERTA e A BEBIDA DO BANQUETE** (Goibniu). Na guerra, o ferreiro com o carpinteiro e o rebitador repõe as armas toda noite, e o inimigo manda matar o ferreiro. A lança que não erra (o efeito Ponta Certa). Uma receita Primordial perdida: quem bebe no banquete do ferreiro não envelhece naquele ano.
9. **FIO MANSO, FIO FAMINTO e O RUMOR DE FERRO** (Masamune e Muramasa; a lenda do córrego não tem fonte antiga, e a fama maldita foi política). A PROVA DO CÓRREGO na irmandade julga o controle além do dano. Um rival pode espalhar que as peças de Ferord são malditas: o preço cai à metade na cidade até alguém desmentir, com testemunha.
10. **A COBIÇA DA COROA** (Völundr). Uma trilha de 0 a 5. Sobe com cada peça Épica ou maior que fica conhecida, cada nome ganho, cada concurso vencido. Desce com favores ao rei, com a proteção de um rival do rei, ou com a fuga (a obra de fuga como projeto secreto, como as asas do mito).

| Passo | O que o poder faz |
| --- | --- |
| 1 | elogia e encomenda |
| 2 | exige exclusividade (vender a outro dá multa) |
| 3 | põe um guarda "para proteger" a oficina (o Mestre avisa) |
| 4 | proíbe sair da cidade (o Mestre avisa de novo) |
| 5 | prende o ferreiro na oficina-fortaleza |

11. **A MATILHA DA COLHEITA e AS NOITES DO LATIDO** (Thiess de Kaltenbrun, Livônia, 1692; a Caçada Selvagem). A fera de um ermo que, dizem, desce três noites por ano para trazer de volta o grão roubado: protege a colheita E mata o gado. Matá-la pode custar a colheita seguinte (o Mestre decide oculto se é verdade). De 3 a 5 noites por estação, a caçada passa: andar fora pede coragem contra 24.
12. **O FERRO DE SOLEIRA** (o ferro frio do folclore europeu). Ferro puro, sem liga nem encanto: +2 contra o medo de espírito e de fera encantada, e fere as fadas como prata; encanto de grau 2 ou mais tira a propriedade. Nas noites do latido, a ferradura de porta (Comum, CD 22) vende o dobro. A parteira encomenda o ferro de cama.
13. **O ESCUDO QUE CONTA, A DÍVIDA PAGA EM OBRA e A MÃO QUE NÃO MANCA** (Hefesto). O escudo gravado com a terra de quem luta (o efeito do 3.1). A obra feita por gratidão a quem salvou Ferord soma +5 na Lei do Valor, uma vez por dívida. E a ferida de perna não tira a maestria de forja: só braço e olho tiram.
14. **O ENGASTE DE RELÍQUIA** (Durendal). O punho com engastes (Rara 1, Épica 2, Lendária 4). Cada relíquia de um santo ou herói de Belogar dá um efeito pequeno e sagrado (contra mortos, contra o medo, uma cura leve por dia). Quatro juntas tornam a peça INQUEBRÁVEL: nem o dono a destrói, e ela volta ao mundo depois dele. A igreja quer as relíquias de volta.
15. **A FORJA QUE OFERECE e O MOINHO DO DOTE** (Kalevala; os detalhes, não verificados). A obra Lendária que falha por pouco oferece outra peça, uma categoria abaixo, com mau gênio (o arco que pede uma morte por dia); ficar com ela ou devolver ao fogo (a matéria volta pela metade). E o senhor do norte que pede, como dote, uma obra Primordial de fartura; quebrada, ela vira 1d6 lascas Raras espalhadas pelo mapa.
16. **A IRMANDADE DO MALHO e O RIVAL** (as guildas medievais e a obra-mestra; de memória: não verificado). O exame da obra diante de três mestres; sem ele, não se vende Rara ou melhor na cidade. O rival tem a própria régua: a cada derrota, sobe por despeito; a cada vitória dele, leva uma encomenda que era de Ferord.
17. **O ROL DOS MALHOS** (o ranking de ferreiros do Ragnarok Online). A capital guarda a fama dos ferreiros: cada peça Rara ou melhor com o sinete soma pontos, e o lugar no rol muda o preço e as encomendas. O primeiro vira o REI DOS MALHOS (3.6).
18. **O DESDÉM DO OFÍCIO** (Arifureta; The Legendary Moonlight Sculptor). Até ter feito de luta conhecido, o ferreiro é subestimado: contra quem não o conhece, age primeiro, e o primeiro golpe tem +3. O desdém some onde a fama chega.
19. **O PRIMEIRO FOLE** (Tubalcaim, Gênesis 4:22; não verificado nesta pesquisa). O mito próprio de Belogar: o primeiro ferreiro aprendeu o fogo de quem não devia. O povo chama o ferreiro para benzer ferramenta e afastar espírito; em ano de praga ou de fome, ele é o primeiro suspeito.
20. **OS RISCOS DE MESTRE** (The Witcher 3; não verificado). Os moldes das Únicas e Lendárias estão em desenhos de ferreiros antigos, guardados em casas, templos e ruínas; cada risco dá um bônus na Lei do Valor só para aquela peça.
21. **OS SERES QUE NÃO VOLTAM** (Shangri-La Frontier; não verificado). O ser único da história, morto, não volta; a carcaça dele vira peça Única; quem sobrevive a ele leva a marca (o CAÇADOR DO ÚNICO).
22. **UM GANHO POR TURNO, NEM SEMPRE NÚMERO** (o ritmo das web novels coreanas). Cada turno fecha com algo que mudou, alternando número (um bloco, uma peça) e história (uma pista, um rumor).

O arquétipo do ferro que abre a mata vem de várias tradições, inclusive de uma religião viva no Brasil (o orixá do ferro). Dela, nada entra no jogo: nem nome, nem cor, nem rito. Só o arquétipo amplo, na habilidade A PICADA (3.4).

---

## 4. O que NÃO fazer

1. **O atordoar em cadeia.** Item que atordoa em 30% dos golpes, mais a dança de três golpes por rodada, e o inimigo nunca age. O World of Warcraft resolveu com retornos decrescentes. Freio: o calejo para tudo.
2. **A porcentagem que multiplica até explodir.** O laço de ofícios do Skyrim ia ao infinito; os conjuntos de 6 peças do Diablo III viraram o único jeito de jogar (os números do D3: não verificado). Freio: a regra da pilha.
3. **"+50% em tudo".** O Medo de −50% em todos os atributos (Solo Leveling) e o +30% em tudo à noite (The Legendary Moonlight Sculptor) decidem a luta sem dado. Em Belogar, efeito sobre "tudo" só pequeno, e com prazo.
4. **A imunidade total.** A classe lendária quase imune a estados (Overgeared) mataria o sistema de estados que o jogador pediu. Resistir desce um degrau; nunca zera (por isso o Legatário tem +4 contra estados, não imunidade).
5. **O lendário sem preço.** Poder sem custo vira obrigação: todo mundo usa. Todo apelão leva dois freios (3.1).
6. **A esteira sem fim.** Refazer até o perfeito (os cubos do MapleStory, a força estelar que destrói a peça de meses, falhar de propósito para carregar a pilha do Black Desert). Freios: a piedade só na Beira, o Banho Negro que sela, uma marca por dia.
7. **Copiar tudo de todos.** Apaga a identidade das classes. Freios: a cópia sai um degrau abaixo, com vagas contadas, e a chance tem piso e teto (5% e 90%).
8. **Trocar recurso sem ganho.** A magia de sangue do Path of Exile saiu porque ninguém a usava; a do Dragon Age funciona porque dá poder e corta a cura.
9. **A classe híbrida melhor em tudo.** Mata as básicas. A cruzada herda um pouco de cada mãe e paga um preço próprio.
10. **O pré-requisito invisível.** A classe ou a dupla que o jogador nunca descobre não existe. As pistas vêm do boato e da gente do mundo.
11. **O ferreiro que arma o mundo de graça.** Sem teto, a oficina vira fábrica de poder. Freios que já existem: a sintonia de quem veste, o núcleo (6 Épicos e 2 Únicos por ano) e o tempo de bancada.
12. **O ganho de número a cada turno.** Vira inflação. Alternar número e história.
13. **Copiar nomes.** A obra é fonte; Belogar tem nome próprio para tudo.

---

## 5. O que isto muda no plano da parte 2

A ordem do PROJETO era: os efeitos de item, as peças do mundo, as habilidades, a magia de grau 5. A pesquisa pede a base da luta antes de tudo, e a Beira cedo:

1. **A base da luta, antes de qualquer efeito.** A regra da pilha, a lista fechada com os três estados novos, a carga, o calejo para tudo, a escada do medo. No `provas.py`: nenhum controle trava ninguém, e nenhuma pilha passa do teto.
2. **Os efeitos de item** (as tabelas do 3.1, de número e de regra), cada um com o seu lugar na conta da luta (`luta.py`) e a prova por faixa (PROJETO 2.1), e os freios do apelão (a sintonia dobrada, um por vez, os usos do dia).
3. **A Beira na forja** (o pedido do jogador): o cheio, o teto, o QUASE refeito, o dado 1 com escolha, o calo só na Beira. No `provas_oficio.py`: a escada medida (Rara no Dia 17, Épica no 59, Única no 177, Lendária no 356 e 1 em 4) não pode mudar.
4. **As peças do mundo com efeitos** (PROJETO 2.2), com o nome ganho, a reforja e o poder de lenda com dito; no mundo de verdade, por evento do Mestre.
5. **As habilidades de arma:** a técnica do Treinado, do Mestre e do Lendário de cada família (2.3b), a escada pelo uso com o freio; depois a Sanha, a Roda do Malho e os Trunfos, medidas pela régua.
6. **As habilidades de trabalho, cura, convencer e copiar:** primeiro o teste de fala (que não existe), depois a atadura, as três que crescem na cena (a Mão que Esquenta, o Fio da Conversa, o Malho Quente), a lição de bancada, o molde, o decalque, colher o jeito e o estalo.
7. **Os dons:** o grau novo como gatilho, a regra geral, os três dons pedidos com fardo, os dons de feito; medidos como o 10.7 mediu o Grande Dom.
8. **As classes:** a escada e as três chaves; primeiro as Comuns e Incomuns, depois as Raras cruzadas (Juramentado, Sanhudo, Malheiro, Marcador), depois as Épicas e a Sangradeira. As Únicas, as Lendárias, a Mítica, a Primordial e as secretas entram por evento do Mestre.
9. **A magia de grau 5 e a régua dos 24** (PROJETO 2.4), com o preço de verdade e a marca no lugar.
10. **O ano inteiro** (`provas_ano.py`): os rivais com tudo isso não quebram o mundo, e a semente que reprova não vira save. Os ganchos de história entram um a um, por evento do Mestre.

---

## 6. As fontes, por frente

### Frente 1: novels, manhwa e animes de mundo de jogo
- Overgeared, a forja: <https://overgeared.fandom.com/wiki/Legendary_Blacksmith's_Craftsmanship> · <https://www.lightnovelspot.com/novel/overgeared/3-chapter-97> · <https://roliascan.com/read/overgeared-novel/ch99-157624> · <https://www.wuxiaworld.com/novel/overgeared/og-chapter-99>
- Overgeared, a esgrima herdada: <https://overgeared.fandom.com/wiki/Pagma's_Sword_Dance_(Skill)> · <https://overgeared.fandom.com/wiki/Great_Swordsman_Pagma%27s_Swordsmanship> · <https://freewebnovel.com/novel/overgeared-novel/chapter-167> · <https://freenewnovel.com/book/overgeared/volume/mMxmexLX/chapter/13>
- Overgeared, a classe, os títulos e os atributos: <https://overgeared.fandom.com/wiki/Grid/Titles> · <https://tvtropes.org/pmwiki/pmwiki.php/Characters/OvergearedGrid> · <https://www.novelupdatesforum.com/threads/overgeared-stats.54513/> · <https://overgeared.fandom.com/wiki/Legendary_Great_Magician_(Quest)> · <https://www.scribd.com/document/696219238/Over-Geared>
- Overgeared, as habilidades que nascem de cena e o ranking: <https://www.wuxiaworld.com/novel/overgeared/og-chapter-13> · <https://www.wuxiaworld.com/novel/overgeared/og-chapter-18> · <https://www.wuxiaworld.com/novel/overgeared/og-chapter-40> · <https://www.wuxiaworld.com/novel/overgeared/og-chapter-1308>
- The Legendary Moonlight Sculptor: <https://the-legendary-moonlight-sculptor.fandom.com/wiki/Volume_1_Chapter_8> · <https://the-legendary-moonlight-sculptor.fandom.com/wiki/Volume_2_Chapter_7> · <https://the-legendary-moonlight-sculptor.fandom.com/wiki/Volume_3_Chapter_3>
- Solo Leveling: <https://solo-leveling.fandom.com/wiki/Sung_Jinwoo> · <https://powerlisting.fandom.com/wiki/Bloodlust_Manipulation> · <https://modrinth.com/mod/daleveling> · <https://efkrdnz.github.io/mods/solo-leveling-reawakening/guide/> · <https://sololeveling.wiki/plot-and-story/solo-leveling-system-explained>
- Bofuri: <https://www.tvtropes.org/pmwiki/pmwiki.php/Characters/BofuriIDontWantToGetHurtSoIllMaxOutMyDefense> · <https://lnori.com/book/31371/bofuri-i-dont-want-to-get-hurt-so-ill-max-out-my-defense-vol-11>
- The Rising of the Shield Hero: <https://shield-hero.fandom.com/wiki/Curse_Series> · <https://shield-hero.fandom.com/wiki/Curse_Series/Weapon_List>
- Danmachi: <https://danmachi.fandom.com/wiki/Falna> · <https://www.myanimethoughts.xyz/2021/06/skill-ability-in-danmachi.html?m=1> · <https://gamerant.com/is-it-wrong-to-pick-up-girls-in-a-dungeon-falna/>
- Tensei Shitara Slime Datta Ken: <https://breezewiki.discard.no/tensura/wiki/Raphael> · <https://www.scribd.com/document/642100878/Every-Ultimate-Skill>
- Sword Art Online: <https://otakumode.com/otapedia/anime/sword_art_online/sword_skills_sao> · <https://swordslice.com/blogs/news/the-real-power-behind-kirito-s-swordsmanship-in-sao>
- Shangri-La Frontier: <https://epicstream.com/article/shangri-la-frontier-seven-colossi> · <https://mystiqora.com/?p=3758>
- Arifureta: <https://arifureta.fandom.com/wiki/Arifureta_(Main_Series)> · <https://www.mangaupdates.com/series/kh5qawh/arifureta-shokugyou-de-sekai-saikyou>
- Overlord: <https://sportskeeda.com/anime/overlord-what-super-tier-magic-explained> · <https://overlordmaruyama.fandom.com/wiki/Tier_Spells>
- Log Horizon: de memória, sem fonte.

### Frente 2: RPG de mesa, mecânicas e história
- Genesys (o Star Wars da FFG): <https://star-wars-rpg-ffg.fandom.com/wiki/Crafting> · <https://www.fantasyflightgames.com/en/news/2016/3/24/the-inventors-handbook/>
- Ars Magica: <https://www.redcap.org/page/Ars_Magica_5E_Standard_Edition,_Chapter_Eight:_Laboratory> · <https://forum.atlas-games.com/t/lesser-enchanted-devices-and-lab-texts/6411>
- Pathfinder 2ª: <https://2e.aonprd.com/Conditions.aspx?ID=19> · <https://2e.aonprd.com/GMScreen.aspx> · <https://roll20.net/compendium/pf2/Conditions%20(Legacy)> · <https://2e.aonprd.com/Rules.aspx?ID=3603>
- Tormenta20: <https://pt.scribd.com/document/377197497/Condicoes> · <https://yggdrasilgeeknetwork.github.io/tormenta20/typedoc/classes/Condicao.html> · <https://pt.scribd.com/document/979338777/Classes> · <https://tiermaker.com/create-xy/tormenta20---classes-at-deuses-e-heris-2025-18067407>
- D&D 5ª, o bárbaro: <https://5e.d20srd.org/srd/classes/barbarian.htm> · <https://roll20.net/compendium/dnd5e/Rage> · <https://dnd5e.wikidot.com/barbarian>
- D&D 5ª, o mestre de batalha: <https://roll20.net/compendium/dnd5e/Subclasses%3ABattle%20Master?expansion=32231> · <https://dotesports.com/dnd/guides/the-best-maneuvers-for-battle-master-fighters-in-dnd-5e>
- D&D 5ª, o paladino: <https://roll20.net/compendium/dnd5e/Divine%20Smite> · <https://5e.d20srd.org/srd/classes/paladin.htm> · <https://www.enworld.org/threads/paladin-smite-damage-cap.456214/>
- Blood Hunter: <https://dnd5e.wikidot.com/blood-hunter> · <https://www.dndbeyond.com/posts/1168-blood-hunter-101-a-guide-to-matt-mercers-brutal?comment=23>
- Warhammer, as runas: <https://tow.whfb.app/magic-items/rules-of-the-runes> · <https://5th.whfb.app/magic-items/runic-magic> · <https://groups.google.com/g/wfrp3-virtual-rpg/c/6MXwOJO6miU> · <https://www.fantasyflightgames.com/en/news/2011/6/9/the-three-laws-of-rune-magic/>
- D&D 5ª, o cavaleiro rúnico e o artífice: <https://www.dndbeyond.com/classes/1350681-runecarver> · <https://dnd5e.wikidot.com/artificer:infusions>
- Warhammer Fantasy Roleplay 4ª: <https://www.cubicle7games.com/wfrp-astounding-success> · <https://www.d20radio.com/main/?p=15670> · <https://www.scribd.com/document/409959512/WFRP-4e-Cheatsheets> · <https://Www.wikipedia.org/wiki/Warhammer_Fantasy_Roleplay>
- RuneQuest e Call of Cthulhu: <https://cthulhuwiki.chaosium.com/rules/rewards-of-success.html> · <https://roll20.net/compendium/coc/Rules:The%20Game%20System>
- Burning Wheel: <https://forums.burningwheel.com/t/test-difficulty-for-advancement/11770> · <https://www.scribd.com/document/360735107/bwr-gmscrn-pdf>
- D&D 4ª: <https://www.enworld.org/threads/4th-edition-and-the-adventuring-day.696998/> · <https://www.enworld.org/goto/post?id=5941027>
- D&D 3.5 e Pathfinder 1ª, as classes de prestígio: <https://d20srd.org/srd/prestigeClasses/assassin> · <https://aonprd.com/PrestigeClassesDisplay.aspx?ItemName=Assassin> · <https://cayzle.com/3Esrd/prestigeClasses.html>
- Shadow of the Demon Lord: <https://schwalbentertainment.com/2014/11/18/playing-characters/> · <https://schwalbentertainment.com/2015/10/14/demon-lords-companion-preview-2-expert-paths/>
- A história do RPG no Brasil: <https://rpgista.com.br/2019/03/17/a-history-of-the-brazilian-rpg-scene> · <https://rpggeek.com/rpg/1294/tagmar> · <https://www.sbgames.org/sbgames2018/files/papers/IndustriaShort/188137.pdf> · <https://www.buscape.com.br/jogos/conteudo/rpg-de-mesa> · <https://ojs.uel.br/revistas/uel/index.php/projetica/article/download/39900/30838/230071>
- De memória, sem fonte: GURPS, Blades in the Dark, os jogos PbtA, Vampiro, a lista de condições da 5ª, a corrente de golpes.

### Frente 3: jogos eletrônicos, itens, raridades, afixos e forja
- Diablo II: <https://classic.battle.net/Diablo2exp/items/magic.shtml> · <https://classic.battle.net/diablo2exp/items/crafteditems.shtml> · <https://diablo2.diablowiki.net/Affix> · <https://maxroll.gg/d2/items/crafted-items>
- Diablo IV, a obra-prima, a têmpera e o afixo maior: <https://icy-veins.com/d4/guides/masterworking-guide> · <https://www.ginx.tv/en/?p=63981> · <https://game8.co/games/Diablo-4/archives/454152> · <https://icy-veins.com/d4/news/why-you-should-reroll-tempers-until-you-get-a-greater-affix/> · <https://expcarry.com/diablo-4-tempering-masterworking-guide> · <https://www.pcgamer.com/games/action/diablo-4-tempering-manuals-masterworking> · <https://www.windowscentral.com/gaming/diablo-4-tempering-guide>
- Diablo IV e III, os aspectos, o Códice e o Cubo: <https://www.icy-veins.com/d4/guides/legendary-aspects-codex-of-power-guide/> · <https://dotesports.com/diablo/news/how-to-extract-aspects-in-diablo-4> · <https://www.icy-veins.com/d4/news/all-legendary-aspects-extract-directly-to-codex-in-diablo-4-season-4/> · <https://maxroll.gg/d3/resources/kanais-cube> · <https://icy-veins.com/d3/kanais-cube-guide>
- MapleStory, o potencial e a força estelar: <https://strategywiki.org/wiki/MapleStory/Potential_System> · <https://digitaltq.com/maplestory-potential-guide> · <https://forums.maplestory.nexon.net/discussion/comment/48427> · <https://maplestorywiki.net/w/Guide:Star_Force> · <https://maplestorywiki.net/w/Star%20Force%20Enhancement> · <https://support-maplestory.nexon.com/hc/en-us/articles/204088639-How-do-I-enhance-equips-with-Star-Force>
- Lost Ark: <https://www.gamesradar.com/lost-ark-engravings-ability-stones> · <https://vulkk.com/2022/02/18/how-to-use-lost-arks-engraving-system/> · <https://lostark.wiki.fextralife.com/Ability+Stones> · <https://gamertweak.com/facet-ability-stone-lost-ark> · <https://maxroll.gg/lost-ark/resources/engraving-system-guide> · <https://lostark.wiki.fextralife.com/Engravings> · <https://gamerempire.net/lost-ark-engraving-effect-guide/>
- Ragnarok Online, a forja: <https://projectalfheim.net/wiki/index.php/Forging> · <https://www.irowiki.org/wiki/Blacksmith> · <https://wiki.ragnarevival.com/_export/xhtml/crafting/blacksmith/forging> · <https://www.scribd.com/document/362422650/Forging-IRO-Wiki>
- Black Desert: <https://grumpygreen.cricket/bdo-failstack-chart/> · <https://www.invenglobal.com/articles/1871/bdo-guide-how-to-maximize-enhancement-stacks-the-upside-of-failing> · <https://altarofgaming.com/black-desert-online-ultimate-guide-enhancing-failstacks/>
- Elden Ring: <https://eldenring.wiki.fextralife.com/Bleed> · <https://eldenring.wiki.gg/wiki/Blood_Affinity> · <https://eldenring.wiki.gg/wiki/Frostbite> · <https://eldenring.wiki.fextralife.com/Frostbite>
- Risk of Rain 2: <https://riskofrain2.fandom.com/wiki/Luck> · <https://steamcommunity.com/app/632360/discussions/0/599658601187019562/>
- Hollow Knight: <https://hollowknight.wiki/w/Overcharmed> · <https://hollowknight.wiki/w/Charm_Notches> · <https://hollowknight.wiki.fextralife.com/Charms>
- Path of Exile, as passivas-chave, a corrupção e os degraus: <https://www.poewiki.net/wiki/Keystone> · <https://www.poewiki.net/wiki/Keystone_passive_skill> · <https://maxroll.gg/poe2/resources/corruption-outcomes> · <https://maxroll.gg/poe/resources/corruption> · <https://poe2wiki.net/wiki/Vaal_Orb> · <https://sportskeeda.com/mmo/path-exile-2-poe2-item-corruption-what-vaal-orbs> · <https://www.poewiki.net/wiki/Affix> · <https://www.poe2wiki.net/wiki/Tier> · <https://www.pathofexile.com/item-data/mods>
- Hades e Hades II: <https://hades.wiki.fextralife.com/Boons> · <https://mobalytics.gg/hades-2/wiki/boons> · <https://primagames.com/gaming/hades-guide-legendary-heroic-duo-boons> · <https://hades2.wiki.fextralife.com/Boon>
- Vampire Survivors: <https://pcgamer.com/vampire-survivors-evolve-weapons-evolutions-guide> · <https://screenrant.com/vampire-survivors-weapon-evolution-guide/> · <https://www.gamespot.com/articles/vampire-survivors-how-to-evolve-weapons/1100-6508815/>
- Monster Hunter Wilds e os conjuntos: <https://kotaku.com/monster-hunter-wilds-how-do-skills-work-talismans-1851769023> · <https://game8.co/games/Monster-Hunter-Wilds/archives/482548> · <https://icy-veins.com/monster-hunter-wilds/doshaguma-armor-set> · <https://diablo.fandom.com/wiki/Item_set>
- Skyrim, o laço dos ofícios: <https://en.uesp.net/wiki/Skyrim:Fortify_Smithing> · <https://segmentnext.com/skyrim/mechanics/alchemy-restoration-loop> · <https://steamcommunity.com/app/489830/discussions/0/3196991412369592414>
- De memória, sem fonte: Borderlands e The Witcher 3; as cinzas de guerra do Elden Ring só com a página da afinidade de sangue (acima).

### Frente 4: classes, habilidades que crescem e estados (jogos)
- Slay the Spire: <https://slaythespire.wiki.gg/wiki/Debuffs> · <https://slay-the-spire.fandom.com/wiki/Vulnerable>
- World of Warcraft: <https://warcraft.wiki.gg/wiki/Diminishing_returns> · <https://maxroll.gg/wow/resources/crowd-control-diminishing-returns> · <https://www.icy-veins.com/wow/news/stunning-massive-interrupts-and-crowd-control-buff-in-pve-and-cc-nerfs-in-pvp/>
- Pillars of Eternity II: <https://pillarsofeternity2.wiki.fextralife.com/afflictions> · <https://pillarsofeternity.fandom.com/wiki/Status_effects>
- Divinity: Original Sin 2: <https://divinityoriginalsin2.wiki.fextralife.com/attribute> · <https://dos2.wiki/wiki/Stunned_(Status)> · <https://pcgamer.com/games/rpg/divinity-original-sin-2s-brilliant-armor-system-is-one-of-a-kind-in-rpgs-and-im-bummed-well-apparently-never-see-it-again>
- Path of Exile, a Fúria e as cargas: <https://www.poewiki.net/wiki/Rage> · <https://poe2wiki.net/wiki/Rage> · <https://mobalytics.gg/poe-2/guides/rage> · <https://maxroll.gg/poe/resources/charges> · <https://www.poewiki.net/wiki/Frenzy_charge>
- Diablo II, o Frenesi e o paladino: <https://diablo.fandom.com/wiki/Frenzy_(Diablo_II)> · <https://wikiwiki.jp/diablo2r/Frenzy> · <https://classic.battle.net/diablo2exp/classes/paladinstrat.shtml> · <https://diablo2.wiki.fextralife.com/Might> · <https://diablo.fandom.com/wiki/Aura>
- Ragnarok Online, o ferreiro e o renascer: <https://renewal.playragnarok.com/gameguide/classes_skill.aspx?c=11> · <https://irowiki.org/classic/Hammer_Fall> · <https://irowiki.org/wiki/Hammer_Fall> · <https://irowiki.org/classic/High_Novice> · <https://irowiki.org/classic/Transcendent> · <https://strategywiki.org/wiki/Ragnarok_Online/Jobs>
- Final Fantasy Tactics: <https://game8.co/games/Final-Fantasy-Tactics/archives/552993> · <https://primagames.com/tips/final-fantasy-tactics-war-lions-job-guide> · <https://finalfantasy.fandom.com/wiki/Final_Fantasy_Tactics_jobs>
- Dragon Quest VI: <https://dragon-quest.org/wiki/Paladin> · <https://strategywiki.org/wiki/Dragon_Quest_VI%3A_Realms_of_Revelation/All_About_Vocations> · <https://dragonquest.fandom.com/wiki/Alltrades_Abbey_(Dragon_Quest_VI)>
- Romancing SaGa 2: <https://saga.fandom.com/wiki/Glimmer> · <https://romancing-saga-2-revenge-seven.blogspot.com/p/spark-glimmer.html> · <https://www.siliconera.com/how-to-unlock-glimmer-skills-in-romancing-saga-2-revenge-of-the-seven/>
- Final Fantasy II: <https://www.rpgsite.net/feature/11516-final-fantasy-ii-how-to-level-up-and-an-explanation-on-the-leveling-system> · <https://steamcommunity.com/app/1173780/discussions/0/3043858334664562481> · <https://finalfantasy.fandom.com/wiki/Rank_(Final_Fantasy_II)>
- Mabinogi: <https://wiki.mabinogiworld.com/view/Skill> · <https://wiki.mabinogiworld.com/view/Dan> · <https://wiki.mabinogiworld.com/view/Sword_Mastery> · <https://wiki.mabinogiworld.com/view/Talk:AP_Training>
- Darkest Dungeon: <https://darkestdungeon.wiki.gg/wiki/Glossary> · <https://darkestdungeon.wiki.gg/wiki/Butcher%27s_Circus> · <https://darkestdungeon.wiki.gg/wiki/Death%27s_Door> · <https://darkestdungeon.wiki.gg/wiki/Blight>
- Bloodborne: <https://bloodborne.wiki.fextralife.com/Rally> · <https://bloodborne.wiki.fextralife.com/Regain> · <https://www.positioniseverything.net/how-to-use-bloodbornes-rally-mechanic-to-replace-lost-health/>
- Dragon Age: Origins e a magia de sangue do Path of Exile: <https://dragonage.fandom.com/wiki/Blood_Magic_(Origins)> · <https://dragonage.fandom.com/wiki/Blood_Mage_(Origins)> · <https://pathofexile.fandom.com/wiki/Version_3.14.0>
- Total War: Warhammer: <https://r2encv2.totalwar.com/en/manual/single-player/0087_enc_page_battle_play_phase_conflict_morale/index.html> · <https://totalwarwarhammer.gamepedia.com/Break> · <https://www.gamepressure.com/total-war-warhammer-2/leadership-and-exhaustion/zba33d>
- League of Legends: <https://www.esports.net/news/lol/what-is-tenacity-in-lol> · <https://lol.fandom.com/wiki/Mercury%27s_Treads> · <https://rankedkings.pages.dev/blog/what-is-max-tenacity-in-league-of-legends>
- Final Fantasy V: <https://finalfantasy.fandom.com/wiki/Blue_Mage_(Final_Fantasy_V)> · <https://rpgsite.net/feature/11955-final-fantasy-v-blue-magic-how-to-learn-every-spell-for-the-blue-mage>
- Dragon's Dogma: <https://dragonsdogma2.wiki.fextralife.com/Augments> · <https://primagames.com/tips/all-augments-in-dragons-dogma-2-and-how-to-unlock-them> · <https://dragonsdogma.wiki.fextralife.com/Vocations>
- Skyrim, o nível pela soma das perícias: <https://en.uesp.net/wiki/Skyrim:Leveling> · <https://en.uesp.net/wiki/Skyrim_talk:Leveling>
- De memória, sem fonte: a postura de Sekiro e de Dark Souls.

### Frente 5: histórias de RPG e mitos de ferreiros
- Overgeared, a cadeia da classe: <https://www.wuxiaworld.com/novel/overgeared/og-chapter-24> · <https://www.wuxiaworld.com/novel/overgeared/og-chapter-74> · <https://roliascan.com/read/overgeared-novel/ch27-157551/>
- Tyrfing e Dáinsleif: <https://en.wikipedia.org/wiki/Tyrfing> · <https://mythlok.com/weapons/dainsleif/> · <https://worldoftales.com/European_folktales/Scandinavian_folktale_28.html>
- Brokkr e Eitri: <https://en.wikipedia.org/wiki/Brokkr> · <https://en.wikipedia.org/wiki/Eitri> · <https://www.ebsco.com/research-starters/religion-and-philosophy/loki-and-dwarfs>
- Kusanagi e Durendal: <https://www.thecollector.com/legendary-swords-excalibur/> · <https://en.wikipedia.com/wiki/Durendal>
- Gram: <https://en.wikipedia.org/wiki/Gram_(mythology)> · <https://www.marxists.org/archive/morris/works/1870/volsungs/chapters/chapter15.htm> · <https://kids.britannica.com/students/article/Gram/341197>
- O Despertar de Angantyr (Hervararkviða): <https://en.wikipedia.org/wiki/Hervararkvi%C3%B0a> · <https://sacred-texts.com/neu/onp/onp07.htm> · <https://en.wikipedia.org/wiki/Hervor>
- O Ferreiro e o Diabo: <https://en.wikipedia.org/wiki/The_Smith_and_the_Devil> · <https://pmc.ncbi.nlm.nih.gov/articles/PMC4736946> · <https://www.sciencenews.org/article/no-fairy-tale-origins-some-famous-stories-go-back-thousands-years?tgt=nr>
- Goibniu: <https://en.wikipedia.org/wiki/Goibniu> · <https://britannica.com/topic/Goibhniu> · <https://celt.ucc.ie/published/T300010/text124.html>
- Masamune e Muramasa: <https://en.wikipedia.org/wiki/Muramasa> · <https://www.inkl.com/news/legend-of-japan-s-cursed-swords-perhaps-told-to-boost-tokugawa-image> · <https://japanesesword.net/blogs/news/masamune-vs-muramasa-the-greatest-rivalry-in-japanese-sword-history>
- Völundr: <https://en.wikipedia.org/wiki/Wayland_the_Smith> · <https://en.wikipedia.com/wiki/Volundarkvida> · <https://www.britannica.com/topic/Wayland-the-Smith>
- Thiess de Kaltenbrun e a Caçada Selvagem: <https://en.wikipedia.org/wiki/Thiess_of_Kaltenbrun> · <https://www.press.uchicago.edu/sites/thiess/> · <https://en.wikipedia.org/wiki/Wild_Hunt> · <https://norse-mythology.org/the-wild-hunt/>
- O ferro frio: <https://en.wikipedia.org/wiki/Iron_in_folklore> · <https://www.spookyisles.com/10-iron-folklore-facts/>
- Hefesto: <https://en.wikipedia.org/wiki/Hephaestus> · <https://www.worldhistory.org/Hephaestus/> · <https://www.theoi.com/Olympios/HephaistosWorks.html>
- Ilmarinen e o Sampo: <https://en.wikipedia.com/wiki/Sampo> · <https://standardebooks.org/ebooks/elias-lonnrot/the-kalevala/john-martin-crawford/text/chapter-10> · <https://www.ebsco.com/research-starters/literature-and-writing/kalevala-elias-lonnrot>
- Ogum (religião viva: só o arquétipo amplo): <https://www.significados.com.br/ogum/> · <https://ppgcs.ufpa.br/revistavisagem/edicao_v2_n2/artigos/ferreiros_dogum/10_FERREIROS.pdf> · <https://almapreta.com.br/sessao/quilombo/ogum-dimensao-civilizatoria-uma-leitura-para-alem-guerra/>
- A classe desprezada nos manhwa de mundo virtual: <https://www.cbr.com/virtual-reality-mmorpg-manhwa-like-sword-art-online/>
- Chainmail, Blackmoor e D&D: <https://en.wikipedia.org/wiki/Blackmoor_(campaign_setting)> · <https://www.mnhs.org/mnopedia/search/index/person/arneson-david-lance-1947-2009> · <https://gizmodo.com/5938947/discover-chainmail-gary-gygaxs-dungeons--dragons-prototype>
- O RPG japonês e a troca de ofício: <https://en.wikipedia.org/wiki/Job_system> · <https://www.denofgeek.com/?p=795043> · <https://www.gamedeveloper.com/game-platforms/the-history-of-dragon-quest>
- VRMMO e isekai: <https://sf-encyclopedia.com/entry/vrmmorpg> · <https://sf-encyclopedia.com/entry/sword_art_online> · <https://screenrant.com/dot-hack-sword-art-online-manga-video-game/>
- As web novels coreanas: <https://en.wikipedia.org/wiki/Web_novels_in_South_Korea> · <https://robynpaterson.com/webfiction-statistics-munpia>
- De memória, sem fonte: as guildas e a obra-mestra, Tubalcaim, a era do saque (Diablo, World of Warcraft).

### A conferência da revisão (oito números)
- Elden Ring, o sangue e o congelamento: <https://eldenring.wiki.fextralife.com/Bleed> · <https://eldenring.wiki.gg/wiki/Hemorrhage> · <https://eldenring.wiki.fextralife.com/Frostbite> · <https://eldenring.wiki.gg/wiki/Frostbite>
- MapleStory, o potencial: <https://strategywiki.org/wiki/MapleStory/Potential_System> · <https://digitaltq.com/maplestory-potential-guide> · <https://forums.maplestory.nexon.net/discussion/comment/48427>
- Darkest Dungeon, a resistência depois do atordoar: <https://darkestdungeon.wiki.gg/wiki/Glossary> · <https://darkestdungeon2.wiki.fextralife.com/Stun>
- Path of Exile, a Fúria: <https://www.poewiki.net/wiki/Rage> · <https://poe2wiki.net/wiki/Rage> · <https://mobalytics.gg/poe-2/guides/rage>
- Pathfinder 2ª, o dano persistente: <https://2e.aonprd.com/Conditions.aspx?ID=29> · <https://paizo.com/threads/rzs42uv2> · <https://publish.obsidian.md/merovia/PF2+Character+Building/Conditions/Persistent+Damage>
- World of Warcraft, o retorno decrescente e a Midnight: <https://warcraft.wiki.gg/wiki/Diminishing_returns> · <https://www.icy-veins.com/wow/news/stunning-massive-interrupts-and-crowd-control-buff-in-pve-and-cc-nerfs-in-pvp/> · <https://www.warcrafttavern.com/wow/news/massive-class-changes-in-the-world-of-warcraft-midnight-alpha-development-notes/>
- Shadow of the Demon Lord, as contagens: <https://www.enworld.org/goto/post?id=9494768> · <https://schwalbentertainment.com/news/page/80/> · <https://schwalbentertainment.blogspot.com/2014/11/playing-characters.html>
