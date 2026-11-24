# GUIA DA VILA DE TESTE (fora do cânone)

A vila de teste é um mundo pequeno para experimentar o Motor 10 depois da etapa 2: a luta, a caça, a forja e o custo de viver.
**Nada dela vale para jogo nenhum.** Serve para o jogador dar opinião antes de o motor seguir.

## Criar

De dentro de `motor10/`:

```
python3 vila_teste.py PASTA [comeco=ferreiro|cacador|guerreiro] [nome=NOME] [semente=N]
export MOTOR10_MUNDO=PASTA
python3 turno.py abre
```

A pasta tem de ser nova: o comando recusa escrever por cima. Tudo nasce por eventos `gera`, e o registro fica em `PASTA/eventos.jsonl`.
Sem `comeco=`, o personagem é o guerreiro. Sem `nome=`: Aldo (ferreiro), Cira (caçadora), Maro (guerreiro).

## O que há

**Pedra Rasa**, uma vila de 400 pessoas, no Dia 1 da primavera:
- **pousada:** cama por 2 de prata a noite (paga uma vez, vale o dia inteiro: dormir de novo nas 24 horas seguintes não cobra), refeição por 1;
- **mercado:** os bens no ponto do ano, a matéria Comum e Incomum, e 2.000 de prata contada (loja sem prata não compra);
- **a prateleira:** 15 peças. Comuns a 30 de prata (espada, maça, machado, lança, arco, armadura de couro, armadura de malha, escudo), a adaga a 10, os elmos de couro e de malha a 8, e quatro Incomuns a 180 (espada, lança, armadura de couro, escudo). A arma vale pela matéria que leva: o preço de tabela é o da espada (3 de matéria); a adaga (1) vale um terço, o martelo e a besta (4), 40, e o montante, a alabarda e o malho (5), 50;
- **a loja farta:** a loja quer ter 11 peças Comuns e 4 Incomuns, que é o que a prateleira tem ao nascer. Pelas peças paga 40% do valor a quem não tem mão de comércio (pelos bens, 60%), 20% a menos por cada peça igual que já tem, e também 20% a menos por cada peça da mesma categoria além dessas 11 (ou 4). Quem compra da prateleira abre espaço de novo;
- **a forja da vila:** oficina 1 (+1 no teste); o fogo e a bigorna servem até o Incomum (+4 nas obras Comuns e Incomuns); conserta, paga, até o Raro.

**A Mata do Corvo**, o ermo vizinho, a 1 bloco de ida e 1 de volta. É a borda de uma floresta:

| Bicho | Quantos | Grau | O que é |
| --- | --- | --- | --- |
| corça | 80 | F | a presa de quem começa; anda só ou em duas |
| javali | 40 | E | investe de longe e derruba |
| lobo | 12 | D | bando de 3 a 5, com alfa |
| urso | 3 | D | grande; agarra |
| pantera | **1** | C | o bicho raro: dá couro e osso Raros |
| serpe | **1** | B | o chefe: enorme, sopra, envenena; morta, dá um **núcleo Épico** |

A pantera e a serpe foram postas ali à mão, para o teste: pela tabela (REGRAS 9.15), a pantera só vive do interior da floresta para dentro, e a serpe é bicho de serra e de ruína. Por isso quem sai atrás da serpe lê um aviso de que ali não é lugar dela.
**Para tirar:** madeira Comum 200 e erva Comum 60. É o que a tabela dá à borda de uma floresta: **a borda só dá matéria Comum.** Minério não há (é de serra, de caverna e de ruína), e a matéria Incomum e a Rara só há do interior para cima.
Um bloco de coleta que passa no teste rende 2 de madeira ou 1 de erva, e o que falha não rende nada. O personagem de começo acerta de 7 a 8 blocos em 10. A saída de coleta vai de 1 a 4 blocos (com a ida e a volta, um dia inteiro): na mais longa, o que ele tira vale no máximo 9 de prata na loja.
A matéria pede mão: a Incomum, Iniciante em coleta (40 blocos); a Rara, Treinado (160). O Ivo e a Nara são Iniciantes (cada um nasce com os 40 blocos que explicam a mão).
A contagem é do Mestre (`caca.py conta`; na `MESA.md`, fica na seção SÓ O MESTRE). O povo só sabe a fartura, em palavras, e não sabe da serpe. Quem sai atrás da serpe não lê o número do rastro: a rolagem sai como "rolagem oculta".

**Gente com nome e ficha de luta** (todos em Pedra Rasa; quem tem mão num ofício ou numa arma nasce com os blocos de treino dela):

| Quem | O que é | Nível | Peças |
| --- | --- | --- | --- |
| Bento | o ferreiro (Treinado na forja) | 28 | martelo, armadura de couro |
| Dalva | a taverneira | 12 | adaga |
| Rute | a caçadora (Treinada no arco e no rastro) | 22 | arco Incomum, adaga, armadura de couro |
| Tomé | o guarda (Treinado na lança) | 30 | lança Incomum, escudo, malha e elmo |
| Ivo | o lenhador | 14 | machado |
| Nara | a curandeira | 16 | adaga |
| Lino | o mercador da loja | 10 | nenhuma |
| Zeca | o aprendiz da forja | 3 | nenhuma |

**O personagem** (nível 5, 30 de prata, atributos que somam 340):

| Começo | A mão de Iniciante | Peças Comuns | Leva |
| --- | --- | --- | --- |
| ferreiro | forja e martelo; conhece a receita das peças Comuns (+2) | martelo, armadura de couro | 4 de metal e 2 de madeira Comuns |
| cacador | rastro e arco | arco, adaga de reserva, armadura de couro | 2 de comida |
| guerreiro | espada | espada, escudo, armadura de malha | nada |

## Os comandos de um turno

O Mestre abre com `python3 turno.py abre`: a `MESA.md` traz o personagem, o lugar, o mercado, a oficina, a caça e as perguntas abertas.

| Para | Comando |
| --- | --- |
| comer, dormir, trabalhar | `ato.py comer` (da própria carga: `ato.py comer carga`) · `ato.py dormir N [chao]` · `ato.py trabalhar N` (2 blocos pagos por dia) |
| treinar, descansar, esperar | `ato.py treinar N ARMA` · `ato.py descansar N` · `ato.py esperar N` |
| ver, vestir e guardar peças | `ato.py pecas` · `ato.py vestir ITEM [arma\|arma2\|escudo]` · `ato.py tirar ITEM` · `itens.py janela ITEM` |
| comprar e vender | `mercado.py ver` · `mercado.py comprar BEM N` · `mercado.py vender tudo` · `mercado.py comprar ITEM` · `mercado.py vender ITEM` |
| forjar | `oficio.py pede arma adaga Comum` (a matéria e a chance, sem abrir nada) · `oficio.py forjar arma adaga Comum "Nome" blocos=1` · `oficio.py continua` |
| consertar, ajustar, servir na forja | `oficio.py consertar ITEM pago` (um bloco de espera por peça; a prata arredonda para cima) · `oficio.py ajustar ITEM` · `oficio.py jornal N` |
| sair para caçar | `caca.py sair alvo=corça blocos=2 [com=rute]` |
| diante do bicho | `caca.py atacar inicio=longe vantagem=alto,cerco` · `caca.py deixar` · `caca.py fugir` |
| a luta | `caca.py luta "Nome: atacar" ["grupo: atacar"]` até acabar (as ordens: atacar, segurar, avancar, recuar, folego, guardar NOME; a ordem `folego` acaba quando o fôlego enche; `recuar` é a retirada: a pessoa anda para trás e, a 8 casas de todo inimigo de pé, sai da luta) |
| depois da luta | `caca.py sangue` (a presa que fugiu ferida) · `caca.py segue` · `caca.py volta` |
| tirar matéria | `caca.py coletar madeira:0 blocos=2` (na Mata do Corvo: `madeira:0` e `erva:0`; o número é a categoria: 0 Comum, 1 Incomum, 2 Rara) |
| um teste de cena | `teste.py "o que se tenta" Atributo contra=N [oculto]` |
| uma luta com gente | `ato.py luta nova CENARIO.json briga.json` · `ato.py luta roda briga.json "Nome: ordem"` (no cenário, quem é do mundo entra como `{"id": "tome"}`; o segundo nome, dito sem pasta, fica dentro do save, em `lutas/`) |
| o que o Mestre decide em cena | `estado.py mestre '[["pessoa","eu","moedas","soma",5]]' "achou cinco moedas"` |
| conferir | `estado.py valida` · `estado.py pessoa ID` (quem não é o personagem aparece como volta à cena agora) · `corpo.py ver` · `estado.py eventos` · `caca.py conta` (só o Mestre) |
| as respostas do jogador | `turno.py responde "1a.2b"` (vale como ele escreve: "1c.2 a", "1c, 2a", "1c 2a") |
| fechar o turno | `turno.py pergunta "texto" "a=..." "b=..."` (duas, pelo menos; o comando diz o número que a pergunta terá na lista do RETOMAR) · `turno.py fecha "o que houve"` |

Enquanto há uma luta aberta, o mundo não anda: todo outro ato é recusado, de qualquer pessoa, até a luta acabar ou o Mestre a soltar (`ato.py luta larga ARQ.json "por quê"`; na caça, `caca.py larga "por quê"`). A recusa diz como seguir.
Com a luta aberta, a última linha de cada comando diz só a hora: o PV, o fôlego e as feridas que valem são os do quadro da luta. De quem morreu, a última linha diz só a hora e a morte.

Enquanto a saída de caça está aberta, o personagem está no ermo: comer na taverna, dormir na pousada, vender e forjar são recusados até o `caca.py volta`.

**Quem vai junto tem parte.** O despojo reparte-se em partes iguais entre os que lutaram até o fim (de pé no campo, ou caídos nele e vivos). Quem saiu da luta antes do fim não leva nada, nem que seja quem comanda: mandar o grupo atacar e recuar para fora da luta deixa o despojo todo com os outros.
Só sai da luta quem recua para longe de inimigo de pé: se o último bicho cai enquanto alguém recuava, a luta acabou, e ele ficou com o campo como os outros (e leva a parte dele).
**O que era de um morto não muda de mão sozinho.** Quem passa num rastro na mata acha o corpo e lê o que ficou com ele (as peças, a carga, a prata). Quem fica com o quê é decisão de cena: o Mestre registra com `itens.py dono ITEM PESSOA` e `estado.py mestre`.

## Quem vai junto: como o Mestre cuida de um companheiro

- **O corpo dele anda com o seu.** Quem vai junto passa os mesmos blocos da saída, com o mesmo esforço: tem fome, sono e cansaço, e a pena do corpo entra na luta dele.
- **Em casa ele cuida de si.** Ninguém precisa mandar o companheiro comer nem dormir. Quando ele volta à cena (você o chama de novo com `com=`, ou o Mestre o faz agir com `quem=`), o motor acerta primeiro o tempo que ele passou na vila, contado do último bloco em que esteve em cena. Passados **3 blocos ou mais** (dois blocos inteiros em casa), a fome, o sono e o cansaço voltam a zero. A cada **6 blocos** (um dia), ele ganha uma noite de cura (um décimo do PV) e um dia de repouso nas feridas. Não custa prata.
- **Dois blocos em casa bastam para o corpo; a cura pede um dia.** Uma saída de 4 blocos (a ida, 2 de procura, a volta) e 2 blocos de sono fecham um dia redondo para o personagem, e o companheiro descansa junto: quem volta à meia-noite e sai de novo às 8h vai de corpo zerado. Com um bloco só em casa, ou saindo logo em seguida, ele leva o que a última saída deixou. E quem sai todo dia não ganha a noite de cura: para o PV e a ferida, deixe-o um dia inteiro na vila.
- **A mesa avisa.** Ao abrir a saída, sai uma linha de ATENÇÃO se quem vai junto não vai inteiro (ferida aberta, PV abaixo de 90%, ou o corpo cobrando), e a `MESA.md` traz o estado dele enquanto a saída está aberta. Para olhar antes de chamar: `estado.py pessoa rute` mostra como ela volta à cena agora.
- **No ermo ele come sozinho,** se tem comida na carga, quando a fome chega a 4 (sai uma linha na mesa). A comida dele vem da parte dele no despojo. O personagem come quando você manda (`ato.py comer carga`).
- **Ferida e PV pedem dias,** não blocos: a ferida sara com 7 dias de repouso (21, a grave). O dia de luta e o dia de saída ao ermo não contam como repouso, para ninguém.
- **Não use `quem=` para fazer o tempo passar de graça.** Quando outra pessoa age (`ato.py esperar 6 quem=zeca`), o relógio anda para todos: o corpo do personagem passa os mesmos blocos, como quem espera, e o ato do outro para quando o personagem cruza um limiar. A última linha diz como ficaram os dois.

## Três dias jogados na conferência (a caçadora, semente 1)

- **Dia 1:** comeu (1 de prata) e saiu atrás de corça, viu primeiro, atacou de longe, do alto e com o cerco: três flechas erradas, três certas, a corça caiu. Despojo: 3 de comida, 1 de couro, 1 de osso. Vendeu tudo por 5 de prata. Comeu de novo (1). Cama: 2.
- **Dia 2:** comprou 1 de metal por 4, forjou uma adaga Comum num bloco (62% de chance; passou), mandou consertar o arco (1 ponto: 1 de prata e um bloco de espera), trabalhou a jornada (2 blocos, 4 de prata), o terceiro bloco foi recusado. Comeu (1). Cama: 2.
- **Dia 3:** vendeu a adaga velha por 3 (a adaga vale 10, a loja paga 40% pelas peças e já tinha uma), saiu com a Rute atrás de javali. O javali fugiu por um fio; seguiu o sangue e o achou. Comeu da própria carga. Despojo: 5 de comida, 2 de couro, 1 de osso: 5 de prata na loja. Cama: 2.
- **A conta:** de 30 para 33 de prata em três dias. Entraram 17 (5 da corça, 4 da jornada, 3 da adaga, 5 do javali) e saíram 14 (três refeições, 3; três noites de cama, 6; o metal, 4; o conserto do arco, 1). A caça pagou a cama e a comida e pouco mais, e a adaga vendida quase pagou o metal da nova. (A venda da adaga e a jornada foram refeitas pela regra de hoje: quando este diário foi jogado, toda arma Comum valia 30 e a loja pagou 12 pela adaga, e o terceiro bloco de trabalho ainda era pago.)

## O que ainda NÃO existe

- **Viagem.** Só há a vila e o ermo vizinho. Estrada, rota e dormir no mato por escolha são da etapa 3.
- **Gente com rotina.** Os oito têm nome e ficha de luta, mas não agem sozinhos, não compram e não lembram. O corpo deles só anda quando estão em cena; fora de cena, descansam em casa (ver "Quem vai junto"), sem gastar prata nem comida da vila.
- **Missões, encomendas e clientes.** Ninguém pede nada, e ninguém além do personagem compra peça: a prateleira não escoa. Por isso a loja farta não desenche sozinha: depois de três ou quatro peças vendidas, só volta a pagar bem quando alguém compra da prateleira.
- **Magia e encanto de peça.**
- **Morte com herdeiro.** O personagem morre de vez; o que era dele cai onde morreu, e não passa a ninguém sem uma decisão de cena; a `MESA.md` diz que morreu. O herdeiro, a família que cobra e o nêmesis são da etapa 6.
- **Paga de companheiro.** Quem vai junto numa saída não pede prata nem recusa o perigo: leva a parte dele do despojo, e só.
- **Peso e teto de carga;** comida que estraga.
- **Bicho que vem à vila;** caçadores do povo; rivais.
- **Tempo de céu** (chuva, neblina): só entra na luta se o Mestre puser no cenário.

## O que olhar para dar opinião

1. **A luta.** A caçada de corça é a mais simples: veja se o quadro, as paradas e as ordens se leem bem. Depois chame a Rute (`com=rute`) e tente o javali. Quem quiser medo: três lobos, de perto.
2. **O perigo lido antes.** A frase da ameaça diz o que o bicho é? O grau F da corça e o E do javali batem com o que a luta entregou? Duas corças juntas já valem grau E.
3. **A caça como ofício.** Uma corça rende de 3 a 6 de comida, 1 ou 2 de couro e 1 de osso: de 3 a 7 de prata na loja. Viver custa 3 por dia. É pouco, e mata: o jogador decidiu que fica assim (a caça de começo é para quem aceita o risco).
4. **A forja.** O ferreiro novo acerta a peça Comum em cerca de 8 de cada 10 (com o fogo, a bigorna e a receita), e a Incomum em 5 de cada 10. **Forjar para a loja quase não paga:** a loja paga 40% pelas peças, e a prateleira já nasce cheia. A matéria de começo vira uma peça que rende uns 20 de prata, e depois disso quase nenhuma peça nova paga a própria matéria (um arco Incomum que dá certo paga 72 por 41 de madeira, e é moeda no ar: dá certo 5 vezes em 10); o ferreiro vive do jornal (6 de prata por dia, até a jornada). Forja-se para vestir (a espada Comum custa 30 na prateleira e 10 de metal na bancada) e para subir a mão. A obra Rara pede 9 blocos e matéria Rara, que a loja não tem e a mata, que é borda, não dá: na vila de teste só há o couro e o osso da única pantera (dão para uma peça pequena de couro Raro; para o resto, o Mestre põe a matéria por `estado.py mestre`). A Épica pede, além disso, o núcleo da serpe.
5. **O custo de viver.** Cama 2 por noite, refeição 1, jornada de 2 blocos a 2 de prata: sobra 1 por dia. A espada Comum a 30, a Incomum a 180 (as outras armas, pela matéria que levam). O conserto pago de uma espada Comum custa 0,6 de prata por ponto, em prata inteira e arredondada para cima (um ponto custa 1; cinco pontos, 3), e gasta um bloco de espera por peça (a cada 10 pontos ou parte): mandar consertar quatro peças leva quatro blocos.
6. **O mercado.** Compre e venda e veja o preço andar. A quem não tem mão de comércio, a loja paga 60% pelos bens e 40% pelas peças.
7. **A mesa do Mestre.** A `MESA.md` traz o que é preciso para narrar um turno? Falta alguma coisa? Sobra?
8. **A coleta como ofício.** Dois blocos de lenha por dia rendem cerca de 6 de prata ao preço de base e 3 na loja: paga a cama e a comida, e não sobra. O diarista fica com 1 por dia sem sair da vila, e na mata o lobo aparece. A matéria que vale mais (a Incomum, a Rara) pede mão e fica no interior, que a vila de teste não tem. É assim que a coleta de começo deve ser?
