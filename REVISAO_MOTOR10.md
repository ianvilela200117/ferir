# REVISÃO DO MOTOR — Dia 507 (pedido do jogador)

> O jogador pediu uma revisão grande antes de decidir se recomeça: o equipamento tem de pesar mais que o nível (como no Overgeared), o combate tem de ser mais avançado, a simulação mais viva, as regras mais claras, e o Mestre não pode esquecer coisas.
> Este arquivo é o diagnóstico e a proposta. **Nenhuma regra mudou.** O jogo está parado no Dia 507 (o túmulo, sala 6; o "1b" não foi rolado). Toda mudança espera a palavra do jogador.
> As medições rodaram no simulador (`luta.py` em modo de régua, fora do jogo); os scripts estão em `sims/revisao_motor10/`.

## 1. Em uma página

1. **Você tem razão: hoje o nível vence a arma.** Um nível 275 de espada comum mata um nível 60 vestido de Mítico em uma rodada. O Livro manda o contrário (Lei 1: "o item vence o nível"); foram as regras da casa, somadas uma a uma desde o Dia 203, que viraram a balança.
2. **O equipamento está travado três vezes:** pelo requisito de nível, por não existir um Livro de Itens (a peça é um parágrafo; a ficha de luta é digitada à mão) e porque a escada acabou cedo (a primeira Primordial saiu no Dia 210).
3. **A luta se decide antes de começar:** 9 das 15 lutas com a saída guardada acabaram em 1 ou 2 rodadas, rodando sozinhas, sem uma decisão sua lá dentro.
4. **O mundo gera muito e cobra pouco:** 829 itens da agenda estão vencidos sem tratar, e quase todo evento é uma frase sem efeito em número (seção 5).
5. **As regras estão em camadas sem revogação**, e é por isso que o Mestre esquece: abrir uma sessão pede de 246 a 632 KB de leitura, com o formato do turno escrito de cinco jeitos (seção 6).
6. **A proposta (MOTOR 10)** conserta isso em seis frentes, com números já medidos num protótipo: o item vence o nível; o Livro de Itens; o combate avançado e jogado; o mundo que cobra; um livro de regras só; e um banco de provas.
7. **Recomeçar:** recomendo recomeçar no mesmo mundo, mas só depois de o motor novo estar escrito e testado (seção 8).

## 2. O nível vence a arma (dá para medir)

### O que o Livro diz
- Lei 1: "O ITEM VENCE O NÍVEL. Uma diferença de duas categorias de equipamento não é compensada por nível." (`SATISFY_v5.2_Motor_de_Mundo_texto.txt`, linha 113)
- "A arma decide quem morre; o braço ajuda." (X.2)
- "O nível ajuda devagar, e o item decide." (linha 226)

### O que o jogo faz hoje

| | O Livro | O jogo hoje |
| --- | --- | --- |
| Ações por rodada | 1 + nível ÷ 100 | 1 + nível ÷ 60 (o bicho ainda soma o corpo) |
| Dano do golpe | dado × categoria + Força ÷ 10 | o mesmo **+ nível ÷ 5** ("mão da experiência", Dia 203) |
| Contra-golpes | uma Reação para cada um | por nível: nenhum abaixo do 120; um, dois e três aos 120, 240 e 360 |
| Multiplicador da arma | × 1 a × 500 pela categoria | **× 1 a × 3 nas fichas de gente**, digitado à mão |
| RD da armadura | 0 a 100 pela categoria | **2 a 10 nas fichas de gente** |
| Arma duas categorias abaixo | "só fere com 20" (linha 4062) | não existe para gente |

Cada mudança fazia sentido no dia em que entrou. Somadas, apagaram a Lei 1.

### Exemplos das fichas de verdade
- O Moreth (nível 234, duas armas Míticas): o golpe é 1d10 × 3 + 15 + 46. Dos 77 de dano médio, **46 vêm do nível e 16 da arma Mítica**.
- A lança **Primordial** do Eiagrir está na ficha como × 3. Os soldados da hoste lutam com × 2,5, que na tabela do Livro é o de uma arma **Rara**.
- A Couraça **Mítica** do Moreth vale RD 8. Pela tabela do Livro seria 50.

### As medições (3 a 4 mil duelos por linha)

| O que mudou num guerreiro, contra ele mesmo | Vitória |
| --- | --- |
| nada (controle) | 51% |
| **só o número do nível, de 95 para 180** (mesma arma, mesma ficha) | **99%** |
| a arma, de Rara para Mítica, como as fichas tratam (× 2,5 para × 3) | 57% |
| a armadura, de Rara para Mítica, como as fichas tratam (RD 6 para 8) | 54% |

| Duelo | Hoje |
| --- | --- |
| nível 60 de Mítico contra nível 275 de arma **Comum**, pelas fichas como o save as monta | **0%** |
| o mesmo, com as peças valendo pela tabela do Livro | 7% |
| um nível 90 de Mítico contra **três** de nível 275 mal armados | 0% |

## 3. Os equipamentos se limitam muito

1. **O requisito de nível.** Pela regra da casa: Raro 20, Épico 40, Único 70, Lendário 110, Mítico 180, Primordial 260 (o Livro pede mais: 30, 70, 110, 150, 250, 350). Abaixo dele a peça rende uma categoria abaixo e o efeito de cima dorme. Quase ninguém da casa usa inteiro o que o rei forja: foi preciso o Sob Medida (−10 a −40 conforme o grau) e, depois do reset do rei no 478, a "Mão de Rei" por cima.
2. **Não existe Livro de Itens.** O Livro manda ("uma peça que não está no Livro não existe"), mas:
   - as peças do rei são parágrafos de 500 letras no `estado_vivo.md`;
   - **0 de 138 NPCs** têm equipamento como dado;
   - só **14 pessoas** têm ficha de luta, e ela é digitada à mão. Quem não tem (o Gonde, a guarda) "recua";
   - peça nova só muda a luta se alguém lembrar de digitar. O raio da Couraça do Moreth ("quem o golpeia leva 10") nunca rodou.
3. **A escada acabou cedo.** A primeira Primordial saiu no Dia 210. Do 210 ao 325 saíram pelo menos 15 peças Míticas ou Primordiais. Desde então toda obra é do topo, e o topo vale × 3 na luta: a categoria inflou e o efeito murchou.
4. **Quem decide a luta é o feitiço da peça**, não a peça: a Lança do Sol × 10, o Toque do Ceifador × 20 (cerca de 1.680 num toque). O golpe de arma virou enfeite.

## 4. O combate hoje

- **Curto demais:** das 15 lutas de verdade com a saída guardada, 7 acabaram na 1ª rodada e 2 na 2ª.
- **Roda sozinho:** a luta inteira sai de um comando. Você decide antes (ir ou não ir) e lê o resultado. A única parada é a da G9, quando alguém da casa cai.
- **Só existe "um contra o grupo".** Dois grupos (a casa contra os 24 herdeiros) não cabem no `luta.py`.
- **Não entram na conta:** distância e alcance, lugar estreito, terreno, o tempo que faz, cansaço, durabilidade da arma, parte do corpo ferida, tipo de arma contra tipo de armadura, moral do grupo.

## 5. O mundo: gera muito, cobra pouco

**O que roda sozinho de verdade:** o relógio, o tempo de 4 cidades e o rio, o índice de preço de 5 bens, os 6 pilares de 4 cidades, o XP semanal dos NPCs, a força e o relógio de 22 facções e 6 guildas, e 18 Lendários.

**Mas quase tudo o que "acontece" sai como frase** para o Mestre interpretar:
- das 20 linhas da tabela de eventos do mundo, nenhuma mexe em número. "A rota fecha, mudando os preços" não toca o mercado;
- das 20 linhas da ação dos Lendários, nenhuma tem efeito no estado;
- o preço oscila sozinho, mas nenhuma compra lê o preço. O cofre da semana é um número fixo (+6.457 − 8.930).

**A agenda é o retrato disso:**
- 1.047 itens desde o Dia 380; **829 vencidos sem tratar**;
- chegam 6,6 notícias por dia, 4,3 delas marcadas "toca a casa". Só 15 de 845 foram fechadas;
- 17 pedidos de audiência, ofertas de aliança e ameaças esperam desde o Dia 442, e são impressos de novo todo dia.

**O resto que se produz e não se usa:**
- 69 fios abertos, 68 sem toque há mais de 70 dias;
- 63 tramas entre NPCs (43 "explodiram"), sem efeito em nada;
- 937 faíscas impressas e não guardadas;
- 23 vilões gerados. Nenhum script os move.

**O que não existe:**
- onde cada pessoa está (só 10 nomes têm lugar; o resto "está em Ireviel") e o que ela faz no dia;
- horas do dia (a hora é um texto) e cansaço (o campo existe na ficha e nada o lê);
- fome, sono e doença por pessoa;
- relação entre NPCs que guarde valor;
- população que nasce, morre e migra;
- hoste com soldo e comida;
- boato que anda por estrada;
- o tempo na luta, e o tempo fora das 4 cidades (o rei está em Lumade sem clima).

## 6. As regras em camadas, e por que o Mestre esquece

### Camadas sem revogação
O sistema-base, as regras da casa (em ordem de data: cada "Dia" revoga o anterior sem riscar), o protocolo, os "MOTOR 6 a 9b" e o Livro Nove foram empilhados. Não há ordem de precedência escrita. O resultado:

- **o formato do turno** está em seis lugares, de cinco jeitos (12 blocos no `CLAUDE.md`, 11 no RETOMAR, 10 no LEIA-ME, 9 no `MESTRE.md`, 9 com outro nome no protocolo);
- **o dado do teste** tem duas versões escritas (d20 explosivo; 2d20 com CD +10), e a resistência em luta tem três;
- **a régua** tem quatro: "simular e declarar ao jogador antes de toda luta", "sem régua na mesa", "roda escondida" e "só quando o jogador pedir";
- **"ler cada arquivo inteiro"** no protocolo, **"não reler"** no `MESTRE.md`;
- as regras do jogador estão copiadas em 5 lugares; a leitura de abertura, em 6; o fim do turno, em 4;
- há sete numerações ao mesmo tempo (G1 a G41, P1 a P4, Leis 1 a 16, "Lei do Valor, da Fera, das Ações, das Caçadas", MOTOR 6 a 9b);
- há texto vencido escrito como vigente: caminhos `claude/…`, "o envelope atual é o 2n", "o próximo é no 408", "PARADA: manhã do 437", e o LEIA-ME inteiro (parado na manhã do 336).

**O custo de abrir uma sessão:** 6 arquivos e 246 KB pelo `CLAUDE.md`; 11 arquivos e 632 KB seguindo as remissões. Dos 107 KB do RETOMAR, 102 são histórico.

### Por que o Mestre esquece
- **As regras pedem memória.** Um checklist semanal de 12 itens (metade é só lembrete), 11 itens "todo turno", seis livros atualizados à mão por turno, e dezenas de "o Mestre lembra" e "o Mestre confere".
- **O estado mora em dois lugares.** O rei é nível 50 na ficha e nível 1 na ficha de luta. O cofre é 53.547 na ficha e 62.383 no texto do `estado_vivo.md`.
- **Texto casado com texto.** No Tick 504, três mortos ganharam XP (a Mamiltia, morta no 448; o Pelaccino, no 344; o Quthemnus, no 404). O painel ainda lista cinco monstros mortos como perigo e pede "obra nova" para o Teraseth, que morreu.
- **Só nesta sessão:** uma magia do rei fora da lista de habilidades; a Defesa do Moreth pendente do 428 ao 507; um dado cujo modificador o script não somou.

A auditoria do código achou mais (para conferir um a um na hora de consertar): o tick grava por cima do que o clima escreveu; `semana_npc.py` rola e grava XP se for chamado sem argumento; "preso" casado por texto faz 14 NPCs pularem a semana; faltam os arquivos dos ticks 503 a 506.

## 7. A proposta: MOTOR 10

O princípio: **o script faz a conta, o Mestre narra e pergunta, e você decide mais vezes.** A complexidade nova mora no script, não na sua resposta.

### 7.1 O item vence o nível (medido num protótipo)

Cinco regras:

1. **A ficha de luta sai sozinha** do que a pessoa veste (o Livro de Itens), dos atributos e da maestria. Ninguém mais digita ataque e dano.
2. **A peça vale pela tabela do Livro:** arma × 1 a × 500, armadura RD 0 a 100, bônus +2 a +50.
3. **O nível para de somar direto.** As ações voltam a 1 + nível ÷ 100. A "mão da experiência" (nível ÷ 5 no dano) continua, mas **nunca passa do dano da própria arma**: o veterano dobra o que o aço dá, não inventa aço.
4. **Aço contra aço:** arma duas ou mais categorias abaixo da armadura do alvo só fere no crítico. É a regra do Livro que nunca rodou para gente.
5. **O requisito** deixa de ser só nível (pergunta 2, no fim).

O que o protótipo deu, com as fichas montadas sempre pela conta do Livro:

| Duelo (vitória do primeiro) | Motor de hoje | Protótipo |
| --- | --- | --- |
| nível 60 de Mítico × nível 275 de **Comum** | 7% | **100%** |
| nível 60 de Mítico × nível 275 de **Raro** | 1% | **98%** |
| nível 60 de Mítico × nível 275 de **Épico** | 0% | **78%** |
| nível 60 de Mítico × nível 275 de **Único** (só uma categoria abaixo) | 0% | 0% |
| duas categorias: nível 60 de Único × nível 120 de Raro | 52% | **99%** |
| a mesma arma (Épico): nível 70 × nível 80 | 41% | 38% |
| a mesma arma (Épico): nível 70 × nível 95 | 18% | 16% |
| um nível 90 de Mítico sob medida × **três** de nível 275 de Raro | 20% | **98%** |
| o mesmo × **dez** de nível 275 de Raro | 0% | 1% |
| duração de um duelo | 1 a 2 rodadas | 5 a 6 rodadas |

(No protótipo, o Mítico na mão do nível 60 rende Lendário, pela regra do requisito de hoje: ele está abaixo do 180. "Sob medida" quer dizer rendendo inteiro.)

**Leitura:** duas categorias de vantagem vencem até 200 níveis de diferença. Uma categoria não vence. Com a mesma arma, o nível decide. E dez ainda ganham de um (falta a ele golpe em área). É a Lei 1 do Livro, e é o que você viu no Overgeared.

**O que ainda falta calibrar** (o protótipo é uma prova, não a regra pronta):
- com a mesma arma, 10 níveis de diferença dão 62% a 38%, e 25 níveis dão 84% a 16%. Pode estar íngreme demais;
- os feitiços de peça (× 10 e × 20) têm de entrar na mesma escala, senão continuam decidindo a luta sozinhos;
- cada categoria de bicho precisa da sua prova (os números deles já estão na escala do Livro).

### 7.2 O Livro de Itens e a janela do Satisfy

- **`itens.json`:** toda peça Rara ou melhor, com nome, categoria, dono, onde está, peso, durabilidade, requisito, quem fez, a história, e cada efeito escrito como regra que o script roda.
- **Vestir é um comando.** A ficha de luta se refaz na hora. Peça nova muda a próxima luta sem ninguém lembrar.
- **O inimigo também veste.** O que ele usa cai como despojo de verdade, e a cobiça passa a ter alvo de verdade.
- **A janela de item**, como no romance, aparece na cena quando a peça nasce, muda de mão ou quebra:

```
[ Lança do Rio Limpo ]
Categoria: Primordial      Durabilidade: 412/412      Peso: 3,1 kg
Ataque: 1d10 × 500 · +50   Crítico: 19-20
Efeitos: sangra · volta à mão (9 m) · o golpe derruba (1x por cena)
Encanto: Lança do Sol (2x por cena)
Dono: Eiagrir (sob medida)   Feita por: Ferir, noite do 303
```

- **Os avisos do sistema** no mesmo tom: nível, título, missão oculta, habilidade que subiu de grau.
- **A escada de volta.** Num jogo novo, cada categoria é um capítulo: a primeira Única é uma vitória, a primeira Lendária muda a casa, a Mítica pede núcleo e viagem, a Primordial muda uma lei do mundo (como o Livro já diz). Proponho um teto do mundo para peças, como já existe para os Lendários de carne e osso.

### 7.3 Combate avançado, e jogado

O que passa a interferir. Cada linha é um módulo do script, que se liga e desliga no `motor.json`:

| Módulo | O que faz |
| --- | --- |
| 1. Distância e alcance | Três faixas: longe, perto, colado. A lança bate antes; o arco não serve colado; avançar gasta ação. |
| 2. O lugar | Estreito (só dois batem lado a lado), alto, coberto, escuro, água pela cintura. O corredor do túmulo passa a valer. |
| 3. O tempo e o chão do dia | A chuva, a lama, a neblina e o calor do tick entram na luta sozinhos. |
| 4. Fôlego | Cada ação custa; armadura pesada custa mais; sem fôlego, perde ações. Luta longa cansa, e ter reserva importa. |
| 5. Golpe contra armadura | Corte, ponta e impacto contra couro, malha e placa, além da Essência. |
| 6. Parte do corpo | Golpe forte ou crítico acerta um lugar: braço (a arma cai), perna (não avança), tronco (perde fôlego), cabeça (atordoa). A ferida fica. A armadura passa a ser por parte: elmo, peito, braços, pernas, escudo. São mais peças para o ferreiro fazer. |
| 7. Durabilidade | Arma e armadura gastam e quebram na luta. O Reparo de Campo do rei vira ação de verdade, antes e depois. |
| 8. Moral dos dois lados | O líder cai e o bando racha. Rendição e prisioneiros com nome. |
| 9. Grupo contra grupo | Cada lado com várias fichas. A guarda ganha ficha pelo que veste. Acaba o "recua com a Matriz". |
| 10. A luta para e pergunta | No começo de cada rodada em que algo mudou (alguém caiu, o chefe mudou de fase, o rei virou alvo, o fôlego acabou), o script para e você dá a ordem do rei: bater em quem, guardar quem, usar qual peça, recuar. Sem mudança, a rodada corre. |

A ficha de cada um continua cabendo em três linhas na mesa. O que cresce é o que o script leva em conta.

### 7.4 O mundo que cobra

1. **Todo evento mexe em número, ou não existe.** A tabela do mundo passa a mudar preço, pilar, rota e força. Menos eventos, todos com consequência.
2. **A agenda vira caixa de entrada com prazo.** O que toca a casa pede decisão do rei ou da Intendente. Sem decisão, resolve-se sozinho no prazo, com custo. Nada fica vencido.
3. **Gente com lugar e rotina.** Cada NPC importante tem onde está, o que faz hoje e o que quer nesta semana. A relação entre eles guarda valor, e a opinião sobre o rei é lançada sozinha pelo que ele fez.
4. **O corpo e as horas do rei.** O dia em períodos (manhã, tarde, noite, madrugada), e cada ação custa tempo. Fome, sono, cansaço e ferida entram nos testes. É a parte do "estar vivo lá dentro".
5. **Economia de verdade.** O preço do mercado é o que a casa paga e recebe. Há estoque nas cidades; a série da forja vende pelo preço do dia; a hoste tem soldo e comida.
6. **Inimigos com plano.** Cada vilão e cada facção hostil tem um relógio com passos concretos contra a casa. Ele anda sozinho e aparece como fato, não como lembrete.
7. **Boato por estrada.** A notícia viaja pelo mapa, em dias de viagem. O rei só sabe o que chegou aonde ele está.
8. **O tempo onde o rei está**, entrando na viagem, na colheita e na luta.
9. **População** que nasce, morre e migra, puxada pelos pilares.

### 7.5 Regras claras, e um Mestre que não esquece

1. **Um livro de regras só**, por assunto, sem história. O que mudou e quando vai para um diário de mudanças à parte. As G, as Leis e os "MOTOR N" viram capítulos de uma numeração só.
2. **Uma linha de precedência** e **um dado só, com uma escala de CD só**, para tudo.
3. **O estado mora em dado; o texto é gerado.** O `estado_vivo.md` (266 KB), o RETOMAR (107 KB) e o BRIEFING deixam de ser escritos à mão.
4. **Abrir a sessão** passa a ser um arquivo de regras e uma página de retomada gerada.
5. **O turno em dois comandos.** `abre` mostra o que tem de ser tratado: a caixa de entrada, as pendências, as habilidades à mão, quem está onde, o tempo que faz. `fecha` recusa fechar se sobrou coisa (livro por atualizar, selo aberto, item vencido) e guarda no GitHub.
6. **O script soma todo modificador do dado** e reconhece gente por identificador, não por texto ("morto", "preso").
7. **Nenhum script rola ou grava ao ser chamado sem argumento.**

### 7.6 O banco de provas

Hoje o `teste_motor.py` só confere se os comandos abrem. Não mede equilíbrio, e foi assim que a Lei 1 se perdeu sem ninguém ver.

No Motor 10, cada regra de luta passa por **metas escritas e medidas** antes de valer. Por exemplo:
- duas categorias acima vencem 75% ou mais, até 200 níveis de diferença;
- com a mesma arma, 25 níveis de diferença dão de 60% a 70% (hoje dão 84%);
- uma luta entre iguais dura de 4 a 8 rodadas;
- dez soldados Comuns não derrubam um Lendário bem armado; cem derrubam.

Toda mudança de regra roda o banco de novo. Se uma meta quebra, a mudança não entra.

## 8. Recomeçar ou não

Três caminhos:

| | O que é | Ganha | Perde |
| --- | --- | --- | --- |
| **A. Seguir este save** com o Motor 10 por cima | Converter as peças em Livro de Itens, refazer todas as fichas, seguir do Dia 507 | Os 507 dias | A balança muda no meio da história (o Moreth com duas Míticas a × 100 vira um deus da noite para o dia); a escada das peças já acabou; é mais um remendo, o maior de todos |
| **B. Temporada nova no mesmo mundo** | O mundo e o Livro ficam (regiões, Essências, grimório, bestiário, classes). A campanha de Ferir vira história do mundo. Personagem novo, anos depois ou noutra terra, no Motor 10 limpo | Motor limpo, a escada inteira de novo, e um mundo que já tem passado | Ferir como personagem; a casa como está |
| **C. Do zero** | Mundo novo, personagem novo, Motor 10 limpo | Tudo coerente desde o primeiro dia | Tudo o que foi construído |

**Minha recomendação: B.** Motivos:
- o que você quer (o item decidir, a escada de equipamento, a luta jogada) mexe na fundação. Aplicado por cima do Dia 507, vira o remendo que você quer evitar;
- o mundo é a parte boa e não é remendo: são 500 dias de história, gente e lugares que um personagem novo pode encontrar como lenda;
- o rei já foi reiniciado uma vez (nível 1 no Dia 478). Um começo limpo conta melhor essa mesma história.

**A ordem importa:** primeiro o Motor 10 escrito e passando no banco de provas; só depois o Dia 1. Recomeçar no motor de hoje repetiria o caminho.

Este save não se perde em nenhum caso: está guardado no Dia 507 e pode ser retomado.

## 9. O que eu preciso que você decida

1. **O quanto a arma vence:** a) como o protótipo (duas categorias vencem até 200 níveis; uma não vence) · b) mais forte (uma categoria já vence 100 níveis) · c) mais fraco.
2. **O requisito das peças:**
   - a) como no Livro (abaixo do nível, rende uma categoria abaixo);
   - b) **o sob medida é a chave** (recomendo): peça feita sob medida pelo ferreiro, com o nome do dono gravado, rende inteira em qualquer nível, só para ele. Cada pessoa sustenta poucas (1 + nível ÷ 50). Quem compra pronta ou toma de um morto sofre o requisito. A forja vira a fonte do poder da casa: gente de nível 60 vestida pelo ferreiro vale mais que veterano de fora;
   - c) requisito por atributo (Força para arma pesada, Afinidade para peça encantada) em vez de nível.
3. **A luta parar e perguntar:** a) sempre que algo muda · b) só em luta grande (chefe, o rei em risco) · c) deixar rodar sozinha como hoje.
4. **Os módulos do combate (7.3):** todos, ou diga quais ficam de fora.
5. **O mundo (7.4):** quais três coisas você mais quer sentir primeiro.
6. **Recomeçar:** a) seguir este save · b) temporada nova no mesmo mundo · c) do zero.
7. **Começo a escrever o Motor 10?** a) sim, pela luta e pelo Livro de Itens, e trago o banco de provas antes de qualquer Dia 1 · b) ainda não.

---

**Como as medições foram feitas:** duelos no simulador do próprio `luta.py` (o modo de régua, que não grava nada), 3 a 4 mil por linha. "Pelas fichas do save" usa números como os das fichas reais (multiplicador 1 a 3, RD 2 a 8). "Pela tabela do Livro" monta a ficha pela conta do X.2: ataque = atributo ÷ 10 + maestria + bônus da arma; Defesa = 10 + Agilidade ÷ 10 + armadura; PV = Vigor ÷ 10 × 10 + nível × 2; dano = 1d10 × categoria + Força ÷ 10. O protótipo é o `luta.py` de hoje com três trocas feitas em memória (ações ÷ 100, o teto na mão da experiência, aço contra aço). Não é regra e não toca o jogo.

Para repetir: `python3 sims/revisao_motor10/mede.py` (o motor de hoje) e `python3 sims/revisao_motor10/calibra.py` (hoje contra o protótipo). As saídas desta revisão estão ao lado, em `mede_saida.txt` e `calibra_saida.txt`.
