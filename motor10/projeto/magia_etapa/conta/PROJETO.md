# Motor 10, etapa da magia e dos dons: o projeto pela conta

Projetista: a conta e o equilíbrio primeiro. Parti da luta e dos itens que existem e perguntei: que conta de magia, de talento, de poção e de maldição cabe na lei "o item decide" sem virar atalho?
Tudo o que está marcado **medido** saiu de rascunhos por cima do `luta.py` de hoje, nesta pasta (`rascunho_magia.py`, `mede_final.py`, `mede_acde.py`, `mede_a2.py`, `mede_cd.py`, `mede_trad.py`, `mede_bencao.py`; as saídas estão nos `saida_*.txt`). O rascunho troca três funções da luta só na memória e não escreve nada em `motor10/`. Com a mesma semente, as lutas sem magia dão os mesmos números do motor puro (20%, 49% e 49% em 1.500 lutas de cada), e as metas de base batem com o banco (iguais 50%; arqueira longe 36%; arma uma acima 94%).
O que está marcado **conta** é conta exata do dado ou dos blocos. O que está marcado **chute** ninguém mediu.

## 0. Em uma página

1. **Dois botões na pessoa, para todo caminho.** O **talento** diz a pressa de aprender e o teto. O **dom** diz o poder. São 16 caminhos: quatro mãos de arma, oito ofícios, quatro tradições de magia. Quem não tem nada de especial é exatamente a pessoa de hoje: o banco não muda.
2. **O talento nunca vale uma categoria.** O prodígio aprende com metade dos blocos; o Grande Dom vale um grau de maestria (medido: 56 a 61% contra o gêmeo). Contra o gêmeo com a arma uma categoria acima, o Grande Dom vence 6%.
3. **A magia usa a conta do aço, linha por linha.** O foco é a arma (valor × 3 por categoria, bônus + 4). O amuleto é a armadura contra a magia. Só a diferença de categoria conta.
4. **Sem amuleto, a armadura guarda contra a magia 0,6 do valor dela.** É o "lutar sem elmo" da magia: custa de 24 a 27 pontos num duelo contra um mago (o elmo custa 18). Medi as três opções (0,33 · 0,6 · 1) e esta é a que pesa sem virar peça obrigatória.
5. **O mago é um arqueiro que gasta Mana.** Entre iguais, contra quem tem amuleto: 36% de longe, 18% de perto, 10% colado (a arqueira: 36 e 13). O que ele tem de seu é a área (o grupo com um mago de área no lugar de um guerreiro: 62 a 63%), o controle e a rajada curta.
6. **A Mana é o fôlego da magia.** (Afinidade + Vontade) ÷ 10 + maestria. Volta 1 por rodada na luta. Lançando sem parar, seca na rodada 8; a volta dá um terço a mais de lances numa luta longa.
7. **Quatro tradições que não são a mesma lista:** o mago (estudo; fere de longe e em área; não cura), o clérigo (um voto; cura, benze, quebra maldição; luta na linha, de malha e escudo), o druida (o laço com um ermo contado; o chão, os bichos, o veneno) e a bruxa (um pacto com dívida; a maldição, o medo, o roubo de vida).
8. **A cura segue a lei ao contrário:** dado × 6 × 3 elevado a (categoria da cura menos categoria da ferida mais funda). Uma poção desfaz pouco mais de um golpe da categoria dela, e um terço disso na categoria de cima. É o que impede a poção barata de valer em luta cara.
9. **A maldição é um relógio de 6 passos na pessoa.** Todo dia o mundo rola a força dela contra a Firmeza do amaldiçoado. Da categoria da guarda dele, mata em cerca de 15 dias; num aldeão sem amuleto, em 10. Quebra-se cumprindo a condição, com um clérigo ou com poção de categoria maior.
10. **O encanto de peça vale um degrau abaixo e sai uma vez por luta.** Medido: num igual não decide (48 a 52%); contra oito de uma categoria abaixo, rende de 8 a 11 pontos. Ocupa sintonia.
11. **Nada vira mina.** A poção Comum vale 6; quem compra a erva e vende a poção não ganha nada (conta: de 0 a +1,5 de prata por dia). Toda renda nova tem meta no banco.
12. **Simples onde deu:** nenhum estado novo de luta além de cinco; os campos do tempo são os que já existem (neblina, escuro, lama); o ofício novo copia a forja.

---

## A. Os dons e os talentos

### A.1 O que é cada um

- **Talento** é quanto a pessoa aprende depressa num caminho, e até onde a mão dela sobe. Tem cinco graus. Não soma nada em conta nenhuma.
- **Dom** é poder de nascença num caminho. Soma na conta como maestria que ninguém treinou. Tem dois graus e é raro. A pessoa tem no máximo um.
- Os dois nascem com a pessoa e não mudam. Uma pessoa pode ser prodígio sem dom (aprende depressa e pesa o mesmo que os outros) ou ter um Grande Dom e ser lerda (a força bruta que custa a aprender a liturgia).

### A.2 Os caminhos (16)

| Tipo | Caminhos | O que o talento apressa |
| --- | --- | --- |
| mãos de arma (4) | `fio` (adaga, espada, machado, montante) · `haste` (lança, alabarda) · `peso` (maça, martelo, malho) · `tiro` (arco, besta) | os blocos de treino de cada arma daquela mão (40, 160, 500, 1.500) |
| ofícios (8) | `forja` · `couro` · `caça` · `coleta` · `comércio` · `cura` · e os dois novos: `alquimia` · `encanto` | os blocos de bancada, de procura, de coleta; os dias de negócio |
| tradições (4) | `arcano` (o mago) · `fé` (o clérigo) · `verde` (o druida) · `pacto` (a bruxa) | os blocos de estudo da tradição e de cada feitiço |

A ficha só guarda o que não é comum: `talento: {"forja": 1, "arcano": -1}` e `dom: {"fé": 1}`.

### A.3 O talento, em números

| Grau | Nome | Blocos de cada grau de maestria | Nas armas (Iniciante, Treinado, Mestre, Lendário) | Teto | Quantos nascem assim, por caminho |
| --- | --- | --- | --- | --- | --- |
| −2 | Negado | o dobro | 80 · nada | Iniciante | 2 em 100 |
| −1 | Lerdo | uma vez e meia | 60 · 240 · 750 · nada | Mestre | 10 em 100 |
| 0 | Comum | os de hoje | 40 · 160 · 500 · 1.500 | Lendário | 76 em 100 |
| +1 | Jeitoso | dois terços | 27 · 107 · 334 · 1.000 | Lendário | 10 em 100 |
| +2 | Prodígio | a metade | 20 · 80 · 250 · 750 | Lendário | 2 em 100 |

- O feito que Mestre e Lendário pedem não muda: o talento apressa os blocos, não dispensa o feito.
- "Qualquer um aprende magia": o Negado também aprende, até Iniciante (os feitiços de grau 1), com o dobro dos blocos.
- Com 16 caminhos, uma pessoa tem em média 1,6 caminho em que é Jeitosa, e 1 pessoa em 4 é Prodígio em alguma coisa. Quase sempre em coisa que ela não faz: prodígio no ofício que a pessoa segue é 2 em 100.
- Sugestão para o gerador (não é regra): quem nasce escolhe o caminho com peso 3 onde é Jeitoso e peso 6 onde é Prodígio. Assim, entre os 190 com nome, espera-se de 4 a 10 prodígios no próprio ofício.

### A.4 O dom, em números

| Grau | Soma na conta do caminho | Quantos nascem assim |
| --- | --- | --- |
| Dom | +1 (meio grau de maestria) | 45 em 1.000 pessoas |
| Grande Dom | +2 (um grau inteiro) | 5 em 1.000 pessoas |

Num mundo de 10.000: cerca de 450 Dons e 50 Grandes Dons. Entre os 190 com nome: 8 ou 9 Dons e 1 Grande Dom. O caminho do dom sai da sorte do mundo entre os 16, com peso 3 onde a pessoa já é Jeitosa ou Prodígio.

O que o "+1 ou +2" quer dizer em cada tipo de caminho:

| Caminho | Onde soma | O que NÃO dá |
| --- | --- | --- |
| mão de arma | no acerto com arma daquela mão; e a metade na Defesa (como a maestria) | a ação a mais e a reação a mais (são de Mestre e de Lendário) |
| tradição | na Conjuração; a metade na Firmeza; e o mesmo número na Mana | abrir feitiço de grau maior |
| ofício de bancada (forja, couro, alquimia, encanto) | no teste da obra, **como um preparo que nasce com a pessoa: preparo e dom juntos não passam de +8** | passar do teto: o melhor ferreiro possível segue acertando a Lendária 1 vez em 4 |
| caça, coleta, cura | no teste do rastro, da coleta, do tratamento | a mão que a matéria pede (segue sendo tranca) |
| comércio | 2,5 pontos (Dom) ou 5 (Grande Dom) no que a loja paga, sem passar do teto de 80% e 60% | |

**Por que o teto de +8 na bancada.** A decisão 9 do jogador diz que a chance da Lendária não sobe. Conta exata: o melhor ferreiro possível acerta 25,7%; com +2 por fora acertaria 32,2% (1 em 3). Dentro do teto, o dom vale um preparo a menos para ganhar no mundo (e um preparo de alcance Lendário só se ganha em cena): é muito, e não fura a decisão. O ferreiro Treinado na obra Rara, sem preparo inteiro, passa de 52,5% a 61,7% com o Grande Dom.

### A.5 Como nascem, e quem sabe

- **Toda gente gerada:** o dado do mundo (`estado.sorte`, com a chave `talento|pessoa|caminho`). Um d100 por caminho, um d1000 para o dom. Mesma semente, mesma gente.
- **O sangue** (para a etapa 7, a história): filho de quem é Jeitoso ou Prodígio rola duas vezes naquele caminho e fica com o melhor. Filho de quem tem dom herda um Dom no mesmo caminho 1 vez em 4.
- **O personagem do jogador:** recomendo o mesmo dado de todo mundo, mais **uma inclinação** que o jogador escolhe: naquele caminho o d100 rola duas vezes e vale o melhor (Jeitoso ou mais: 23 em 100, em vez de 12). É a pergunta 3.
- **Ninguém nasce sabendo.** O talento **aparece fazendo:** depois de 20 blocos num caminho, a `MESA.md` ganha a frase ("com a espada você pega depressa"; "o arcano lhe custa"). Antes disso, o número mora só no SÓ O MESTRE.
- O dom **se mostra** no primeiro teste em que foi ele que fez passar (o script sabe: "sem o dom, falhava"), ou quando alguém o lê: um clérigo ou uma bruxa Treinados, rito de 1 bloco, 10 de prata para quem lê.
- Dos outros, a MESA só mostra o que o lugar sabe ("dizem que o menino da forja tem mão"). O Mestre vê tudo.

### A.6 Contra a lei "o item decide" (medido)

Nível 50, tudo Raro, os dois com amuleto; de 1.000 a 1.500 lutas por linha.

| O que se mede | Vence |
| --- | --- |
| gêmeos | 50% |
| Dom (+1 no acerto, +0,5 na Defesa) contra o gêmeo | 54 a 55% |
| Grande Dom (+2 no acerto, +1 na Defesa) contra o gêmeo | 56 a 61% |
| um grau de maestria inteiro a mais (Lendário contra Mestre) | 64% |
| Mestre contra Treinado · Treinado contra Iniciante | 66% · 59% |
| Mestre com Grande Dom contra Lendário sem dom | 49% |
| **Grande Dom contra o gêmeo com a arma UMA categoria acima** | **5 a 6%** |
| Lendário com Grande Dom contra Mestre comum com a arma uma acima | 10% |
| mago com Grande Dom contra o mago gêmeo | 56% |
| mago com Grande Dom contra o guerreiro com amuleto, de longe (sem dom: 36%) | 46% |

**Como ler:** o Grande Dom vale um grau de maestria e nada mais. Uma categoria de peça vale de quatro a sete vezes isso (95% contra 56 a 61%). O talento não entra na conta: só decide em que dia a pessoa chega a cada grau.

### A.7 O que isso faz com as metas que já existem

- **Nada, para a pessoa comum.** O robô do banco não tem talento nem dom: multiplica por 1 e soma zero. As 79 e as 87 provas ficam como estão. É a primeira prova da etapa.
- **A escada do ofício, pelo talento (conta dos blocos; 3,5 blocos de bancada por dia, como o robô):**

| Talento | A 1ª obra Rara fecha no dia | Épica | Única | Lendária | Mestre numa arma (2 blocos de treino por dia) |
| --- | --- | --- | --- | --- | --- |
| Negado | 32 | não abre | não abre | não abre | nunca |
| Lerdo | 24 | 72 | 184 | não abre | Dia 375 |
| Comum (o banco de hoje) | 17 | 51 | 131 | 356 | Dia 250 |
| Jeitoso | 13 | 37 | 95 | 260 | Dia 167 |
| Prodígio | 10 | 30 | 77 | 213 | Dia 125 |

- **O prodígio anda uma categoria à frente do comum em boa parte do caminho, e nunca duas.** Do Dia 10 ao 17, do 30 ao 51 e do 77 ao 131 ele tem a peça de cima e o comum ainda não: 82 dos primeiros 131 dias. É o preço de "aprende mais rápido", e o núcleo segue sendo o que tranca: 6 Épicos e 2 Únicos por ano no mundo inteiro.
- **Um aviso:** a decisão 3 diz "a primeira tentativa de Lendária perto do 360, pelo melhor caminho". Com o prodígio, o melhor caminho passa a ser o Dia 213. Se for cedo demais, o Prodígio vira "dois terços dos blocos" (Lendária no Dia 260) e o Jeitoso "quatro quintos".

### A.8 Cena de exemplo (vila de teste)

Maro é guerreiro, com 40 blocos de espada (Iniciante). O dado do mundo, na criação, deu a ele Jeitoso em `fio` e Lerdo em `arcano`; ele não sabe. `python3 ato.py treinar 2 espada`, dia após dia. No bloco 60 de espada (20 desde que o jogo começou), a MESA ganha: **"Com a espada você pega depressa: o que os outros levam 160 blocos para firmar, você firma em 107."** Treinado sai no bloco 107: perto do Dia 34, em vez do 60.

Na forja, Zeca, o aprendiz de nível 3, faz a primeira adaga dele: `python3 oficio.py forjar arma adaga Comum "Adaga do Zeca" quem=zeca`. Ele é Leigo: soma 4 da Afinidade, 1 da oficina e 4 do fogo e da bigorna da vila. Os dados dão 18: 27 contra 28. Mas Zeca tem um Grande Dom na forja que ninguém conhece, e o preparo dele (4) com o dom (2) não passa de 8: são 29. A saída diz: **"Passou por 1. Sem o dom, saía tosca."** A MESA do dia traz a janela: "Há alguma coisa nas mãos do menino da forja." No SÓ O MESTRE estava escrito desde o Dia 1.

### A.9 A página de números

```python
# tabelas_talento.py
MAOS = dict(fio=('adaga', 'espada', 'machado', 'montante'), haste=('lança', 'alabarda'), peso=('maça', 'martelo', 'malho'), tiro=('arco', 'besta'))
CAMINHOS = list(MAOS) + ['forja', 'couro', 'caça', 'coleta', 'comércio', 'cura', 'alquimia', 'encanto', 'arcano', 'fé', 'verde', 'pacto']
TALENTO = {-2: ('Negado', 2.0, 2), -1: ('Lerdo', 1.5, 6), 0: ('Comum', 1.0, 8), 1: ('Jeitoso', 2 / 3, 8), 2: ('Prodígio', 0.5, 8)}   # nome · vezes os blocos · teto
TALENTO_D100 = [(2, -2), (12, -1), (88, 0), (98, 1), (100, 2)]      # até 2: Negado; até 12: Lerdo; até 88: Comum; até 98: Jeitoso; 99 e 100: Prodígio
DOM = {1: ('Dom', 1), 2: ('Grande Dom', 2)}                          # o que soma na conta do caminho
DOM_D1000 = [(5, 2), (50, 1)]                                        # até 5: Grande Dom; até 50: Dom; o resto: nada
DOM_PESO = 3                # o dom cai com este peso no caminho em que a pessoa já tem talento
APARECE = 20                # blocos num caminho para o talento aparecer na MESA
INCLINACAO = 2              # quantas vezes o personagem rola o d100 no caminho que o jogador escolheu
def blocos(tabela, grau, talento): return math.ceil(tabela[grau] * TALENTO[talento][1])
def caminho_de(chave): return next((m for m, fs in MAOS.items() if chave in fs), chave)      # 'espada' é do caminho 'fio'
```

---

## B. A magia na luta

### B.1 A conta, linha por linha com a do aço

| | O aço (hoje) | A magia |
| --- | --- | --- |
| quem bate soma | Acerto = maestria + (bônus de Força + de Agilidade) ÷ 4 + bônus da arma | **Conjuração** = maestria da tradição + bônus do atributo da tradição ÷ 2 + bônus do foco |
| contra | a Defesa | **o que voa** (seta, lança, raio): a Defesa, inteira, como um tiro. **A área:** a Defesa sem escudo e sem arma, como o sopro. **O que prende, assusta ou amaldiçoa:** a **Firmeza** |
| o tamanho | dado × 4 × valor da arma ÷ proteção da parte × força do golpe | dado × 4 × valor do foco ÷ **guarda** × força do feitiço (1 + 0,03 por ponto de bônus do atributo da tradição) |
| a proteção | a armadura da parte atingida, com o material | **a guarda:** o valor do amuleto; ou 0,6 do valor da armadura do tronco, o que for maior. Sem um nem outro: um terço. O material não conta, a parte do corpo não conta, não há fresta |
| crítico | dados em dobro, proteção pela metade | igual: dados em dobro, guarda pela metade |
| o fôlego | 6 + bônus de Vigor | **Mana** = (Afinidade + Vontade) ÷ 10 + maestria da tradição |

**Firmeza** = 22 + bônus de Vontade ÷ 2 + a maior maestria da pessoa ÷ 2 + o bônus do amuleto (sem amuleto: metade do bônus da armadura do tronco) + o calejo (B.5). É a Defesa da cabeça: a mesma forma da Defesa do corpo.

O feitiço que tira um quarto do PV máximo abre ferida, como um golpe, numa parte sorteada (as feridas, o sangue, a queda e a moral são os de hoje). Chuva, vento, neblina, escuro, cobertura e gente no caminho valem para o feitiço que voa como valem para um tiro.

### B.2 O foco e o amuleto: itens com categoria

| Peça | Mãos | Valor | Apara | Pede | De quem é | Matéria (unidades) · preço Comum |
| --- | --- | --- | --- | --- | --- | --- |
| varinha | 1 | o da categoria | não | Afinidade 40 | arcano | 2 de madeira, 1 de osso · 30 |
| cajado | 2 | × 1,25 (como toda arma de duas mãos) | o bônus da categoria; bate como arma leve de 1d6, impacto | Afinidade 60 | arcano, verde | 4 de madeira, 1 de osso · 50 |
| símbolo | 1 | o da categoria | não | Vontade 60 | fé | 3 de metal · 30 |
| talismã | 1 | o da categoria | não | Vontade 40 | pacto | 2 de osso, 1 de couro · 30 |
| **amuleto** | nenhuma (no pescoço; um só) | a guarda | não | nada | todos | 1 de osso · 10 |

- São itens do Livro de Itens (`tipo: foco`, com `forma`; `tipo: amuleto`). Categoria, durabilidade, dono, história, janela: tudo como as outras peças. O preço segue a regra de hoje (vale pela matéria que leva), vezes 6 por categoria. Do Épico para cima pedem núcleo, como toda obra.
- **Requisito por atributo, nunca por nível** (a lei de hoje): faltou Afinidade ou Vontade, −1 na Conjuração a cada 5 pontos. Um Leigo empunha um cajado Lendário e ele vale 243: o que lhe falta é a mão (a Conjuração) e o feitiço sabido.
- **Sem foco:** lança-se com as mãos, como foco Comum com −4. Foco de outra tradição rende uma categoria abaixo (a regra do "não é dele").
- **Gastam:** o foco perde 1 por luta em que lançou e 1 a cada retrochoque. O amuleto perde 1 quando leva feitiço de foco de categoria maior, e 1 por luta em que guardou. A zero, não valem.
- **Sintonia:** foco e amuleto Épicos ou melhores ocupam lugar, como toda peça alta (Vontade ÷ 20). Quem quer o conjunto e o amuleto treina a Vontade.
- O amuleto Comum custa 10 de prata: no mundo em que a magia tem para todo lado, o povo anda de figa no pescoço. Sugestão para o gerador: metade dos combatentes com nome traz amuleto da categoria do conjunto; a outra metade, nenhum. O amuleto abaixo da armadura só ajuda a Firmeza, e só do Épico para cima.

**Por que 0,6.** Medi o duelo e o grupo com as três guardas possíveis para quem não tem amuleto:

| A armadura, sem amuleto, guarda contra a magia | Mago contra guerreiro SEM amuleto (longe · perto · colado) | Quatro e um mago de área contra cinco SEM amuleto |
| --- | --- | --- |
| um terço do valor (um degrau abaixo) | 78% · 59% · 31% | 98% |
| **0,6 do valor (a proposta)** | **63% · 42% · 19%** | **84 a 86%** |
| o valor inteiro (o amuleto só serviria à Firmeza) | 40% · 24% · 10% | 65% |
| para comparar: COM amuleto da categoria | 36% · 18% · 10% | 62 a 63% |

Com um terço, o amuleto vira a quinta peça obrigatória e a área apaga um grupo. Com o valor inteiro, o amuleto quase não importa. Com 0,6, não ter amuleto contra um mago custa o que custa lutar sem elmo, e um pouco mais.

### B.3 A Mana

- **O tamanho:** (Afinidade + Vontade) ÷ 10 + maestria da tradição. O mago de nível 50 tem 22; o aprendiz de começo (Afinidade 70, Vontade 55, Iniciante), 14; o guerreiro que nunca estudou, 9, que não lhe servem de nada até aprender um feitiço.
- **O custo:** 2 por grau do feitiço (truque: 1). A área custa 2 a mais. Sustentar custa 1 por rodada.
- **Na luta volta 1 no começo de cada turno** (decisão do jogador: devagar). Medido, só de seta e sem parar: seca na rodada 8 (sem a volta, na 7); em 20 rodadas, 15 setas em vez de 11. Se voltassem 2, não secava nunca: por isso é 1.
- **Fora da luta, por bloco:** dormindo, um quarto do máximo; descansando, um oitavo; em bloco leve, 1 ponto; em bloco pesado, nada. Cada tradição muda isto (B.6).
- **Sem Mana, pode-se lançar no osso:** cada ponto que falta custa 5% do PV máximo, e o lance é **forçado** (B.4). É escolha do jogador: a luta para e pergunta.

### B.4 O tempo de lançar, o que interrompe, o que dá errado

| Grau | A mão que o feitiço pede | Mana | Tempo | Dado de dano típico |
| --- | --- | --- | --- | --- |
| truque | 10 blocos da tradição | 1 | 1 ação | nenhum |
| 1 | Iniciante | 2 | 1 ação | 1d8 |
| 2 | Treinado | 4 | 2 ações (o turno inteiro: não anda) | 2d8 |
| 3 | Mestre | 6 | **longo:** gasta as 2 ações agora e só sai no começo do turno seguinte | 2d10 |
| 4 | Lendário | 8 | longo de duas rodadas | 3d10 (chute) |

- **A mão é conselho, não tranca,** como na forja: abaixo dela o lance é forçado, com −4 por grau que falta.
- **Lançar com inimigo colado** dá a ele um golpe livre (gasta a reação dele). Se o golpe fere, testa a concentração.
- **A concentração:** quem está canalizando um feitiço longo e leva dano rola 2d20 + bônus de Vontade + maestria contra 28 (32 se o golpe abriu ferida). Falhou: perde o feitiço e a Mana. Quem cai, é derrubado, atordoado ou agarrado perde sem teste.
- **Medido:** sob uma arqueira, de 25 a 27% dos feitiços longos se perdem; sob duas, 35 a 36%; sob duas, com um guarda de escudo na frente do mago, 31%. Cada teste falha 28 a 30% das vezes.
- **O retrochoque:** dois 1 no dado (1 lance em 400). No lance forçado, basta um 1 (1 em 10). Quem lança vai ao chão, perde 1 ação, e o foco perde 1 de durabilidade. No forçado, leva ainda o próprio feitiço contra a própria guarda.
- **Lançar não gasta fôlego.** A armadura pesada cobra o fôlego dela na rodada em que a pessoa lança, como cobra quando golpeia. A placa já pede Força 80: o mago de Força 47 que a veste perde 6 na Defesa, além dos 2 da placa, e paga 4 de fôlego por rodada. A regra do requisito já cuida do "mago de armadura", sem regra nova.

### B.5 O controle, e os estados (lista fechada)

Só entra estado que a luta sabe rodar. Dos dez abaixo, cinco já existem.

| Estado | O que faz | Na luta de hoje |
| --- | --- | --- |
| preso (N turnos) | não anda, não recua, não troca de lugar; bate e lança | já existe (a perna presa, o agarrado) |
| no chão | −4 na Defesa; levantar gasta uma ação | já existe |
| atordoado (N) | perde N ações | já existe |
| abalado | −2 no acerto | já existe |
| medo | um teste de coragem contra o número do feitiço; quem o jogador comanda só fraqueja, e a luta para | já existe (a moral) |
| cego (N turnos) | o escuro só para ele: −4 no golpe, −8 no tiro e no feitiço que voa | novo |
| guardado (N turnos) | +4 na Defesa | novo |
| benzido (até o fim da luta) | +2 no acerto e +4 na coragem | novo |
| mau-olhado (até o fim da luta) | −2 no acerto, na Defesa e na Conjuração | novo |
| com seiva (N rodadas) | recupera 5% do PV máximo por rodada | novo (é o "regenera" dos bichos, menor) |

- **O campo** usa o tempo que já existe: um feitiço põe `neblina`, `escuro` ou `lama`, ou tira o `escuro` (a luz). Vale para os dois lados.
- **Calejo:** cada controle que pega soma 4 na Firmeza do alvo até o fim da luta. Ninguém fica preso a luta inteira.
- **As penas de magia não somam entre si:** de mau-olhado, veneno e maldição vale a pior. Essa pior soma com a pena do corpo (fome, sono, cansaço).
- **A chance de pegar (conta exata):** mago Mestre de foco Raro (Conjuração +18) num guerreiro de nível 50:

| O alvo | Firmeza | Pega | Calejado uma vez | Duas |
| --- | --- | --- | --- | --- |
| com amuleto Raro | 35,5 | 66% | 48% | 32% |
| sem amuleto (armadura Rara) | 31,5 | 80% | 66% | 48% |
| com amuleto Épico | 39,5 | 48% | 32% | 20% |
| soldado de nível 20, Comum, sem amuleto | 25,5 | 95% | 86% | 74% |

O foco uma categoria acima soma 4: no guerreiro com amuleto Raro, 80%. Uma abaixo: 48%.

### B.6 As tradições

| | O mago (`arcano`) | O clérigo (`fé`) | O druida (`verde`) | A bruxa (`pacto`) |
| --- | --- | --- | --- | --- |
| atributo da Conjuração | Afinidade | Vontade | Percepção | Afinidade |
| foco | varinha, cajado | símbolo | cajado (vivo) | talismã |
| de onde vem o poder | do estudo: livro e mestre | de um **voto** a um Poder, feito num santuário | do **laço** com um ermo | de um **pacto**: toma emprestado e deve |
| como a Mana volta fora da luta | a regra geral | só com a prece: 1 bloco por dia; no santuário enche, fora dele enche a metade | no ermo, em dobro; entre muros (cidade, masmorra), a metade | sozinha, só até a metade; o resto paga-se: 2% do PV máximo por ponto, ou 1 de dívida por 4 de Mana |
| faz melhor | ferir de longe; a área; prender; o escudo | curar; benzer; guardar o grupo contra magia; quebrar maldição | o chão e o tempo (raízes, neblina, lama); os bichos; o veneno; a cura lenta | amaldiçoar; o medo; roubar vida; atar a Mana de outro; ler o oculto |
| não faz | não cura; não quebra maldição | não fere de longe quem não é maldito; não tem área de dano | não usa fogo; entre paredes de pedra, −4 na Conjuração | não cura (só troca); não protege |
| o que custa | o livro (prata e blocos); o feitiço longo que se perde | o voto (escrito na ficha; quebrou, perde a Mana e ganha uma maldição); a cura tem teto por dia | o ermo do laço: com a fartura dele abaixo de 40%, −2; abaixo de 10%, −4 | a dívida: feitiço de grau 2 soma 1, de grau 3 soma 2, de grau 4 soma 3; a praga soma a categoria dela mais 1; dívida acima de Vontade ÷ 10 vira maldição nela |
| o lugar na luta | atrás, de couro e cajado | **na linha, de malha, escudo e maça** (a mão na arma costuma ficar um grau abaixo) | atrás, ou no mato | atrás; péssima sozinha |
| na vila de teste | Anselmo, o velho | Nara, a curandeira | Rute sabe um truque | Quitéria, na borda da mata |

- **O voto do clérigo** é uma regra que o estado sabe conferir. Três de partida: **da lâmina** (não põe em uso arma de corte nem de ponta), **da pobreza** (na virada do dia não guarda mais de 50 de prata: o resto vai para o santuário, que é um lugar com estoque) e **do socorro** (não recusa cura pedida na caixa de entrada: etapa 3).
- **O laço do druida** liga a magia ao ermo contado da etapa 2: o druida que deixa caçar a mata até o fim perde a força. A fartura é a média de contagem ÷ teto das espécies e da matéria do ermo.
- **A dívida da bruxa** não some com prata (a prata não nasce nem some): paga-se em PV num rito de 1 bloco (1 ponto por 5% do PV máximo) ou queimando matéria (4 de osso ou de erva da categoria do foco por ponto).
- **Cabe a quarta?** Sim, e recomendo a bruxaria agora, porque a maldição precisa de dono. A alquimia de guerra (o frasco de arremesso) e o canto ficam de fora desta etapa.

**As tradições na luta (medido; nível 50, tudo Raro, o guerreiro com amuleto):**

| | De longe | De perto | No grupo de cinco, no lugar de um guerreiro (a base: 46 a 52%) |
| --- | --- | --- | --- |
| o mago (seta, lança, prender, escudo; com a bola, no grupo) | 36 a 39% | 18 a 20% | 62 a 63% com a área; 47% sem ela |
| o druida (raízes; espinho com veneno) | 35% | 20% | 53% |
| o clérigo (maça, escudo, malha; cura) | 32% | 32 a 37% | 44 a 52%; benzendo os quatro antes, 52% (os cinco benzidos, sem ele na luta: 59%) |
| a bruxa (mau-olhado; sangria) | 12% | 6% | 48% |

Num corredor de dois, em lutas de 11 rodadas: o mago de área 58 a 59%, o clérigo 56 a 57%, e a arqueira 70 a 72% (ela não fica sem flecha: é o que a Mana custa).

### B.7 A lista de partida (24 feitiços e um truque)

`alc` em casas. Contra: D é a Defesa, A é a área (Defesa sem aparo), F é a Firmeza. Os marcados com (m) foram medidos no rascunho (da lança de fogo e do raio, só o dano; da bênção, só o +2 dado antes da luta).

| Feitiço | Tradição | Grau | Mana | Tempo | Alc | Contra | O que faz |
| --- | --- | --- | --- | --- | --- | --- | --- |
| luz | todas | truque | 1, e 1 por rodada | 1 ação | campo | nada | tira o `escuro` do campo enquanto durar |
| seta (m) | arcano | 1 | 2 | 1 ação | 8 | D | 1d8 |
| prender (m) | arcano | 1 | 3 | 1 ação | 6 | F | preso por 2 turnos |
| escudo (m) | arcano | 1 | 2 | 1 ação | 4 | nada | ele ou um aliado: guardado (+4 na Defesa) por 4 turnos |
| lança de fogo (m) | arcano | 2 | 4 | 2 ações | 8 | D | 2d8; a ferida que abrir queima (sangra por 5 rodadas) |
| bola de fogo (m) | arcano | 2 | 6 | 2 ações | 8 | A | 1d8 em cada um na casa, até 4, **amigo ou inimigo** |
| raio (m) | arcano | 3 | 6 | longo | 8 | D | 2d10; se abrir ferida, atordoa 1 ação |
| cura (m) | fé | 1 | 3 | 1 ação | toque | nada | devolve 1d8 × 6 × 3^(foco − ferida mais funda) de PV (C.3) |
| bênção (m) | fé | 1 | 2 | 1 ação; ou antes da luta | 4 | nada | benzido até o fim da luta |
| amparo | fé | 1 | 2 | 1 ação | toque | nada | estanca o sangue; tira veneno até a categoria do foco; firma quem caiu (não morre no chão) |
| castigo | fé | 2 | 4 | 2 ações | 6 | D | 2d8 em quem é maldito (amaldiçoado, com peça maldita, bicho que amaldiçoa ou imaterial); nos outros, 1d4 |
| guarda | fé | 2 | 6 | 2 ações | a casa dele | nada | até 4 aliados: contam como tendo amuleto da categoria do foco por 4 turnos |
| quebrar maldição | fé | 3 | 6 | rito de 1 bloco, fora da luta | toque | a maldição | D.4 |
| raízes (m) | verde | 1 | 3 | 1 ação | 6 | F | preso por 2 turnos; em chão de terra, 3 |
| espinho (m) | verde | 1 | 2 | 1 ação | 6 | D | 1d6, e envenena (um quarto do golpe por 3 rodadas, −2 no acerto) |
| névoa ou lamaçal | verde | 1 | 2, e 1 por rodada | 1 ação | campo | nada | põe `neblina` ou `lama` enquanto durar |
| afugentar | verde | 1 | 3 | 1 ação | 6 | F | o bicho testa a coragem contra 26 (o chefe, não) |
| seiva | verde | 2 | 4 | 2 ações | toque | nada | com seiva por 5 rodadas; fora da luta, dobra a cura da noite |
| chamar | verde | 3 | 6 | longo; só no ermo | o ermo | nada | um bicho da contagem real do ermo, até a categoria do foco, vem lutar ao lado; se morre, sai da contagem |
| mau-olhado (m) | pacto | 1 | 2 | 1 ação | 6 | F | mau-olhado até o fim da luta |
| medo | pacto | 1 | 3 | 1 ação | 6 | F | o alvo testa a coragem contra 26 |
| sangria (m) | pacto | 1 | 2 | 1 ação | 4 | D | 1d6, e ela recupera metade do que tirou |
| ler | pacto | 1 | 2 | rito de 1 bloco | toque | oculto | lê uma maldição (a categoria, o passo, a condição), um dom, ou uma peça |
| nó | pacto | 2 | 4 | 2 ações | 6 | F | por 4 turnos a Mana do alvo não volta e cada feitiço dele custa 1 a mais |
| praga | pacto | 3 | 6, e dívida | rito de 1 bloco, com um laço (um objeto do alvo, ou o toque) | qualquer | F | põe uma maldição da categoria do foco (D) |

**Quanto um feitiço tira num igual (medido; o guerreiro com amuleto Raro tem 176 de PV):**

| | Acerta | Por acerto (média, com os críticos) | Por lance |
| --- | --- | --- | --- |
| seta | 45% | 37 (21% do PV) | 16 |
| lança de fogo | 41% | 73 (41%) | 30 |
| raio (2d10, longo) | 44 a 46% | 91 a 94 (51 a 53%) | 40 a 44 |
| seta, no alvo sem amuleto | 45% | 61 (35%) | 27 |
| para comparar: um golpe de espada (conta) | 43% | 27 (15%) | 12 |

A seta com cajado vale uma flecha. O que a magia tem a mais por lance, paga em Mana, em PV (o mago tem 136 contra 176) e em não aparar com escudo.

**Aprender um feitiço:** blocos de estudo (leves), que contam como treino da tradição: truque 3 · grau 1, 6 · grau 2, 18 · grau 3, 54 · grau 4, 162 (vezes o talento). Pede uma fonte: quem o saiba e queira ensinar (cobra o salário dele por bloco: de 6 a 10 de prata), um escrito (item do Livro, tipo `escrito`: 30 de prata o de grau 1, vezes 6 por grau), um santuário (fé) ou o ermo do laço (verde). Os seis de grau 1 de uma tradição somam 36 blocos: é quase o Iniciante (40).

```python
# tabelas_magia.py (o começo)
K_MAGIA = 4.0               # o tamanho do feitiço entre iguais: o mesmo K do aço
GUARDA_ARMADURA = 0.6       # sem amuleto, a armadura do tronco (e o couro do bicho) guarda contra a magia esta fração do valor
GUARDA_NU = 1 / 3
FIRMEZA_BASE = 22; CALEJO = 4
def conjuracao(maestria, atributo, foco_cat): return maestria + (atributo // 10) / 2 + T.BON[foco_cat]
def firmeza(vontade, maestria, amuleto_cat, armadura_cat): return FIRMEZA_BASE + (vontade // 10) / 2 + maestria / 2 + (T.BON[amuleto_cat] if amuleto_cat is not None else T.BON[armadura_cat] / 2 if armadura_cat is not None else 0)
def mana_max(afinidade, vontade, maestria): return (afinidade + vontade) // 10 + maestria
MANA_LUTA = 1; MANA_BLOCO = dict(dormindo=0.25, descanso=0.125, leve=1, pesado=0)
GRAUS = [dict(mao=0, mana=1, tempo=1), dict(mao=2, mana=2, tempo=1), dict(mao=4, mana=4, tempo=2), dict(mao=6, mana=6, tempo='longo'), dict(mao=8, mana=8, tempo='longo2')]
AREA_MANA = 2; AREA_ALVOS = 4; SUSTENTA = 1
CONCENTRA = 28; CONCENTRA_FERIDA = 4; FORCADO = -4; SEM_MANA_PV = 0.05; SEM_FOCO = -4
ESTUDO = [3, 6, 18, 54, 162]; MAGIA_BLOCOS = {2: 40, 4: 160, 6: 500, 8: 1500}
FOCOS = dict(varinha=dict(maos=1, vezes=1, pede=('Afinidade', 40), de=('arcano',)), cajado=dict(maos=2, vezes=1.25, pede=('Afinidade', 60), de=('arcano', 'verde'), apara=True, dado='1d6'),
             simbolo=dict(maos=1, vezes=1, pede=('Vontade', 60), de=('fé',)), talisma=dict(maos=1, vezes=1, pede=('Vontade', 40), de=('pacto',)))
TRADICOES = dict(arcano='Afinidade', fé='Vontade', verde='Percepção', pacto='Afinidade')
FEITICOS = {
    'seta':    dict(de='arcano', grau=1, alc=8, contra='defesa', dano='1d8'),
    'prender': dict(de='arcano', grau=1, mana=3, alc=6, contra='firmeza', poe=('preso', 2)),
    'bola':    dict(de='arcano', grau=2, alc=8, contra='area', dano='1d8', fere_amigo=True),
    'cura':    dict(de='fé', grau=1, mana=3, alc=1, cura='1d8'),
    # ... os outros vinte, como na tabela acima
}
```

### B.8 Os bichos com magia

- **O que os traços de hoje já fazem:** o `veneno` passa a ter resposta (o antídoto e o amparo). O `sopro` fica como está (é fogo: bate na armadura inteira), e o amuleto também guarda contra ele: vale o melhor dos dois. O `apavora` ganha resposta na bênção (+4 na coragem). O `regenera` é o molde da seiva.
- **A guarda do bicho:** o couro vale 0,6 contra a magia, como a armadura. A Firmeza dele leva metade do bônus do corpo.
- **O que falta, e entra (quatro traços; a lista passa de 10 a 14):**

| Traço novo | O que faz | Quem ganha |
| --- | --- | --- |
| `resiste` | o corpo guarda contra a magia inteiro, e a Firmeza leva o bônus inteiro | basilisco, hidra, dragão |
| `imaterial` | arma sem encanto e sem bênção conta uma categoria abaixo contra ele; feitiço e peça encantada contam inteiros | os dois bichos novos |
| `amaldiçoa` | a ferida que ele abre põe uma maldição da categoria do corpo, no passo 1 (D) | a aparição |
| `lança` | sabe um feitiço da lista, com Mana e Conjuração pelo instinto e pela categoria do corpo | o fogo-fátuo (seta) |

- **Dois bichos novos:** o **fogo-fátuo** (grau D, Incomum, pequeno; voa, imaterial, lança seta; brejo e ruína) e a **aparição** (grau C, Rara, média; imaterial, amaldiçoa; só ruína; não dá despojo).
- **Medido:** o mago Raro contra a pantera, de longe, 51 a 52% (o guerreiro, de perto: 46%); de perto, 4 a 5% (o bote o mata no primeiro turno). Contra o trasgo, 43% (o guerreiro: 51%). Três guerreiros e um mago contra a serpe: 13 a 14% (os quatro guerreiros: de 14 a 20% aqui; 24% no banco). O mago sozinho não é caçador; de longe, com alguém na frente, vale um arqueiro.

### B.9 A luta para e pergunta, com magia em campo

Paradas novas (além das de hoje):
- alguém do outro lado **começa um feitiço longo** (dá tempo de ir em cima dele, ou de pôr o escudo);
- quem o jogador comanda fica **preso, cego, com mau-olhado, ou falha o teste de medo**; **perde um feitiço** na concentração; sofre **retrochoque**;
- a **Mana** de quem ele comanda cai abaixo de um terço, e de novo quando não paga o feitiço que tinha ordem de lançar;
- um feitiço **muda o campo** (neblina, escuro, lama, luz);
- um da casa cai e há **cura ou poção ao alcance** (a parada de hoje ganha a frase).

Ordens novas, só para quem o jogador comanda:
`lancar FEITICO [em ALVO | casa N]` (uma vez) · `lancar FEITICO sempre` (até acabar a Mana, o alvo cair ou vir outra ordem) · `beber POCAO` · `usar PECA` (o encanto dela).
**Quem o jogador comanda não lança, não bebe e não gasta encanto sozinho:** a Mana e o frasco são dele. Os outros (aliados e inimigos) escolhem por uma regra fixa e curta (`magia.escolhe`): cura quem está abaixo de metade; prende quem ainda vem chegando; a área só onde há dois inimigos ou mais e nenhum amigo; o resto, o maior dano que a Mana paga.
O quadro (`situacao`) ganha, por pessoa: Mana, o que está canalizando, os estados com prazo. E a linha do campo.

### B.10 A lei, medida com magia

Nível 50, tudo Raro; duas baterias de 600 lutas por linha.

| O que se mede | Vence | O mesmo no aço (o banco) |
| --- | --- | --- |
| mago contra mago | 49% | 50% |
| mago com o foco uma acima contra o guerreiro igual, com amuleto: de longe · de perto | 95 a 96% · 80 a 81% | 95% |
| mago contra o guerreiro com o amuleto uma acima | 8 a 9% | 8% (a armadura uma acima) |
| mago contra o guerreiro com o conjunto uma acima | 0 a 1% | |
| nível 50, foco uma acima, contra nível 500 com amuleto, de longe | 22 a 24% | 8% |
| **nível 50, foco duas acima, contra nível 500 com amuleto: de longe · de perto** | **82 a 84% · 24 a 26%** | 63% |
| mago de nível 150 contra o de nível 50, mesmas peças | 85 a 86% | 88% |
| mago Mestre contra mago Iniciante, mesmo nível e peças | 71 a 73% | |
| um mago Raro contra 5, 8 e 12 soldados Comuns sem amuleto, de longe (120 lutas) | 96 a 97% · 72 a 77% · 47 a 55% | o guerreiro contra 12: 98 a 99% |
| quatro e um mago de área contra cinco: com amuleto · sem | 62 a 63% · 84 a 86% | |

**Como ler:** o foco decide como a espada decide. Para o mago, a distância pesa mais que para qualquer outro: duas categorias de foco valem mais de 80% de longe e 25% de perto. Contra a multidão o mago vale menos que o guerreiro de armadura, porque morre cercado.

### B.11 Cena de exemplo (vila de teste)

Maro e Anselmo, o mago velho (nível 34, arcano Treinado, cajado Incomum, Mana 19, Conjuração +12), acham quatro lobos na borda da Mata do Corvo, a 3 casas. A luta para antes da primeira rodada. Ordens: `"Maro: segurar defensiva"` `"Anselmo: lancar bola em lobo 1"`.

A bola custa 6 de Mana e o turno inteiro. Contra cada lobo na casa, 2d20 + 12 contra 29,5 (a Defesa do lobo sem o aparo): pega 66%. O dano: 1d8 × 4 × 3 (Incomum) × 1,25 (cajado) ÷ 1,8 (o pelo Incomum vale 0,6 de 3) × 1,24 = cerca de 46 por lobo, de 85 de PV. Três pegam: os três perdem perto de metade do PV e ficam feridos, e um deles falha a coragem e foge (o bicho ferido testa). A luta para de novo: "o lobo 3 fugiu".

Na rodada 3 os lobos chegam em Maro. Anselmo, depois de duas bolas, tem 9 de Mana e a ordem `lancar seta sempre`: 48% de acerto, 46 de dano. Na rodada 4 a luta para: **"Anselmo está com a Mana abaixo de um terço (5 de 19)."** O jogador escolhe: a última seta, ou guardar para o escudo em Maro.

---

## C. As poções e a alquimia

### C.1 O ofício, no molde da forja

- **Ofício novo: `alquimia`,** com maestria por blocos de bancada como a forja (50, 150, 375, 1.000) e feito para Mestre (uma leva Épica) e Lendário (uma Única).
- **A bancada** é a `botica` do lugar (0 a 4, como a oficina; soma no teste). Lugar sem o campo não tem botica.
- **A obra é a leva.** A matéria entra quando a leva abre; os blocos somam de um dia para o outro; o teste é um só, no fim; falhar custa. É o `oficio.py` com outra tabela.

| Categoria | Blocos | Contra | Matéria da leva | Rende |
| --- | --- | --- | --- | --- |
| Comum | 1 | 28 | 4 da categoria | 2 doses |
| Incomum | 3 | 34 | 4 da categoria | 2 doses |
| Rara | 9 | 40 | 4 da categoria | 2 doses |
| Épica | 27 | 46 | 4 de matéria Rara e **um núcleo Épico** | 6 doses |
| Única · Lendária | 81 · 243 | 52 · 58 | 4 de matéria Rara e um núcleo da categoria | 6 doses |

- **O teste:** 2d20 + maestria de alquimia + Afinidade ÷ 10 + a botica + o preparo (receita, ajudante, fogo, vidraria: +2 cada um; com o dom, até +8) contra 28 + 6 por categoria.
- **Falhar:** por 1 a 4, a leva sai uma categoria abaixo (a Comum sai aguada: uma dose só). Por 5 ou mais, a matéria some, e o núcleo também.
- **Do Épico para cima a dose é item do Livro** (`tipo: elixir`), contada no mundo. Um núcleo Épico vira seis elixires ou uma espada: é escolha que dói, porque nascem 6 núcleos Épicos por ano.

### C.2 Os ingredientes

- **Os que já existem:** a erva (colhe-se com Percepção; volta 4% por dia), o osso e o couro (despojo), o núcleo.
- **Os que faltam (dois, e só):** a **glândula** (despojo novo do bicho de `veneno`: surucucu, aranha, basilisco, serpe, hidra; 1 por bicho, da categoria dele até a Rara) e a **água benta** (um clérigo benze 1 de erva com 2 de Mana num santuário: é serviço, não matéria nova no ermo).
- Não entra frasco, nem sal, nem fogo como bem: a leva já custa o bloco e a botica.

### C.3 As receitas (nove)

| Poção | Matéria | O que faz | Dura |
| --- | --- | --- | --- |
| **cura** | erva | devolve 1d8 × 6 × 3^(categoria da poção − categoria da ferida mais funda) de PV | na hora |
| remédio (o bem que já existe) | 3 de erva Comum rendem 1 | o dia de repouso da ferida conta em dobro | 1 dia |
| antídoto | erva e osso | tira veneno até a categoria dele | na hora |
| **veneno de lâmina** | glândula | a primeira ferida que a arma abrir na luta envenena: um quarto do golpe por 3 rodadas e −2 no acerto. Numa lâmina de categoria maior que a dose, um terço disso por degrau | uma luta; seca em 1 dia |
| Mana | erva | devolve 4 de Mana por degrau: 4, 8, 12, 16 | na hora |
| guarda | osso e erva | por 1 bloco, conta como amuleto da categoria da poção | 1 bloco |
| fúria | erva e osso | +2 no acerto e −2 na Defesa por 5 rodadas; **só alcança quem empunha arma até a categoria da poção** (a regra do alcance do preparo) | 5 rodadas |
| vigília | erva | tira 3 de sono e 2 de cansaço; uma por dia | na hora |
| quebra-maldição | água benta e osso | maldição de categoria menor que a poção: quebra. Igual: recua 2 passos. Maior: segura 1 dia | D.4 |

- **A ferida mais funda** é a maior categoria que tirou PV da pessoa desde que ela esteve inteira (arma, corpo de bicho, foco). Mora na ficha (`funda`) e apaga quando o PV enche. Fome, sangue e veneno contam como Comum.
- **Por que a cura segue a categoria.** Sem isso, a poção Comum de 6 de prata valeria o mesmo numa luta de aço Lendário. Com isso, a poção Rara desfaz um golpe Raro e pouco (27 de PV, medido), um terço de um golpe Épico, e nada de um Lendário. O preço sobe 6 vezes por categoria com a matéria, e a cura acompanha.
- **Beber é 1 ação.** Dar de beber a um aliado colado, também.
- **Quantas se bebem: Vigor ÷ 30 por dia, no mínimo 1** (o guerreiro de começo, 2; Vigor 120, 4). Cada uma além disso pede Vigor contra 24 + 4 por poção a mais: falhou, a poção não faz nada e a pessoa enjoa (−2 em tudo por 1 bloco).
- **A cura tem teto:** por pessoa e por dia, feitiço e poção somados não devolvem mais que metade do PV máximo. A marca da ferida não fecha com cura: sara com repouso, como hoje.

### C.4 Medido no duelo (nível 50, tudo Raro; 1.000 lutas; o robô bebe abaixo de metade do PV)

| | Vence o gêmeo |
| --- | --- |
| 1 poção de cura Rara · 2 · 3 | 56% · 61% · 60% (a terceira não soma: beber custa a ação) |
| 1 poção Épica (uma categoria acima da ferida: devolve 76 de PV) | 61% |
| 2 poções Incomuns (uma abaixo: 9 de PV cada) | 50% |
| uma dose de veneno Raro, com a regra do bicho (metade do golpe, 4 rodadas) | 59 a 64% |
| a mesma dose valendo um quarto do golpe | 61% (o que pesa é o −2 no acerto, não o dano) |
| veneno e 2 poções | 70% |
| **2 poções contra o gêmeo com a arma uma categoria acima** | **4%** |

O frasco ajuda e não decide: tudo junto (70%) vale pouco mais que um grau de maestria (64 a 66%), e nada contra uma categoria. O veneno é o mais forte dos três; por isso a dose de lâmina dura 3 rodadas e não 4 (meta: 52 a 62%; ainda por medir com a regra proposta).

### C.5 O preço, e a meta que impede a mina

- **A poção até a Rara é um bem com categoria** (`cura:0`, `antidoto:1`, `veneno:2`...), na carga e no estoque, com o preço do mercado de hoje: base × √(alvo ÷ estoque).
- **Base: 6 de prata a Comum, vezes 6 por categoria** (36 a Incomum, 216 a Rara). A matéria da dose (2 de erva: 4 de prata) fica em dois terços do preço.
- **O povo gasta pouco:** 0,0005 por pessoa por dia de cada poção Comum (um sexto a cada categoria). A vila de 400 quer **6 poções Comuns** de cada na prateleira e 1 Incomum. A loja enche depressa, como com as peças.
- **A conta (com a fórmula do mercado de hoje, 30 dias, 400 vidas):**

| O alquimista de começo (3,5 blocos de bancada por dia, acerta 86%) | Prata por dia, dias 1 a 5 | Dias 6 a 30 |
| --- | --- | --- |
| compra a erva e vende a poção, com a prateleira no alvo | 0 (nenhuma leva paga a erva) | 0 |
| o mesmo, numa vila com uma poção só na prateleira (preço no teto) | +0,2 (o pior caso: +0,4) | 0 |
| o mesmo, com a melhor mão de comércio que existe | +1,1 (o pior caso: +1,5) | 0 |
| colhe a própria erva um dia e faz a poção no outro | +1,7 | +1,2 (a erva crua, vendida, dava +1,8) |
| se a poção Comum valesse 12 em vez de 6 (povo gastando como gasta remédio) | +3,6 | 0 |

- **A meta:** a mesma do ferreiro de loja. Nos 5 primeiros dias, em média no máximo 6 de prata por dia e no pior caso 12; do Dia 6 ao 30, no máximo 4. Pela conta, passa com folga. Faz-se poção para beber e para quem paga o valor inteiro (o freguês, na etapa 3).
- **O risco que fica dito:** o coletor Treinado no interior já rende de 6,5 a 9,8 diárias e não tem meta. Virar erva Rara em poção Rara soma metade a isso. A meta dele tem de nascer junto.

### C.6 Cena de exemplo

Nara tem botica 1 e a receita Comum. `python3 alquimia.py fazer cura Comum`: 4 de erva saem da carga, 1 bloco. O teste: 2d20 + 2 (Iniciante) + 5 (Afinidade 52) + 1 (botica) + 2 (receita) = +10 contra 28: acerta 66%. Passou: 2 doses de `cura:0`.

Maro compra duas: `python3 mercado.py comprar cura:0 2`. A prateleira tinha 6; a primeira sai por 6,6 e a segunda por 7,2: 14 de prata. Na mata, um lobo lhe abre o braço (o corpo do lobo é Incomum: a ferida mais funda de Maro passa a Incomum). `"Maro: beber cura"`: 1d8 × 6 ÷ 3, cerca de 9 de PV, de 141. A MESA já avisava: **"Poção Comum em ferida Incomum vale um terço."** A Incomum custa 36 e a vila tem uma.

---

## D. As maldições

### D.1 O que são

Uma maldição é um registro na pessoa, com categoria, um relógio de 6 passos e uma condição que a quebra. Não é estado de luta: é coisa de dias. É a única coisa nesta etapa que mata fora da luta sem ser fome.

```
pessoa.maldicoes = [{"id": "m3", "nome": "a Mão Fria", "cat": 1, "passo": 2, "desde": 12, "de": "peça", "fonte": "i0031",
                     "quem": null, "condicao": {"tipo": "devolver", "item": "i0031", "onde": "capela"}, "sabe": ["de", "passo"]}]
```

### D.2 De onde vêm

| Fonte | Como pega | A condição que costuma quebrar |
| --- | --- | --- |
| feitiço (a praga da bruxa) | rito com um laço; Conjuração contra a Firmeza | o perdão de quem rogou, ou a morte dela |
| bicho (`amaldiçoa`) | a ferida que ele abre | matar aquele bicho |
| lugar (`lugar.maldito`, com categoria) | a cada bloco passado lá, o mundo rola a força contra a Firmeza | sair e não voltar por 7 dias |
| peça amaldiçoada (efeito novo `maldita`) | ao pôr em uso. A peça não se tira nem se vende enquanto durar; rende inteira | devolver a peça ao lugar dela |
| juramento quebrado | o voto do clérigo; a dívida da bruxa; a promessa jurada num santuário | cumprir o que se jurou, ou uma penitência dada por um clérigo Mestre |

### D.3 O que fazem por dia, como pioram, como matam

Na virada de cada dia o mundo rola (o dado do mundo, `estado.sorte`): **2d20 + a força da maldição contra a Firmeza do amaldiçoado.** A força é 2 + 4 por categoria (Comum +2, Incomum +6, Rara +10, Épica +14). Venceu, anda um passo.

| Passo | Nome | O que faz |
| --- | --- | --- |
| 1 | a marca | nada em número; ele sabe que algo o tocou |
| 2 | o peso | −1 em todo teste |
| 3 | a míngua | −2; a noite dormida não devolve PV |
| 4 | a chaga | −2; as feridas não saram e a Mana não volta fora da luta |
| 5 | o fim à vista | −4; perde 10% do PV máximo a cada virada |
| 6 | a morte | morre na virada, por evento, com a causa escrita; o que era dele cai como em toda morte |

**Quanto tempo dá (4.000 vidas por linha; metade morre até o dia dito, se ninguém fizer nada):**

| A maldição | Aldeão sem amuleto (Firmeza 24) | Guerreiro de armadura Rara, sem amuleto (31,5) | O mesmo com amuleto Raro (35,5) |
| --- | --- | --- | --- |
| Comum | 10 dias (anda 48% dos dias) | 24 dias | 41 dias |
| Incomum | 7 dias | 15 dias | 23 dias |
| Rara | 6 dias | 10 dias | 15 dias |
| Épica | 5 dias | 7 dias | 10 dias |

Nenhuma mata antes de 5 dias. O amuleto compra tempo; não cura.

**A pena, medida na luta** (o amaldiçoado contra ele mesmo são): com −1, vence 42%; com −2, 38%; com −4, 26%.

### D.4 Como se quebram

1. **Cumprir a condição.** Quebra na hora, sem dado. Toda maldição tem uma, e o estado sabe conferir (o item voltou ao lugar; o bicho morreu; a dívida zerou; quem rogou morreu).
2. **O clérigo,** com o feitiço de grau 3: rito de 1 bloco, 6 de Mana, uma tentativa por dia. 2d20 + Conjuração contra 28 + a força. Clérigo Mestre de foco Raro (conta): na maldição Rara, 57%; na Épica, 40%; na Incomum, 74%. Falhou por 5 ou mais: o clérigo leva a marca. O serviço custa um terço do preço de tabela da categoria (10, 60, 360, 2.160 de prata), de pessoa a pessoa.
3. **A poção quebra-maldição:** de categoria maior, quebra; igual, recua 2 passos (nunca abaixo do 1); menor, segura 1 dia.
4. **O que não quebra:** dormir, comer, curar o PV, trocar de lugar (salvo a do lugar).

### D.5 No estado e na MESA

- **Um efeito tipado novo,** de lista fechada como os outros: `['maldicao', pessoa, 'poe', registro]` · `['maldicao', pessoa, id, 'passo', +1 ou −N]` · `['maldicao', pessoa, id, 'quebra', 'como']` · `['maldicao', pessoa, id, 'sabe', campo]`.
- **Invariantes novos:** passo de 1 a 6; categoria da tabela; toda maldição tem fonte e condição; morto não tem maldição andando; peça `maldita` em uso tem a maldição dela no dono.
- **Na MESA, em "Você":** `MALDIÇÃO: a Mão Fria, passo 3 de 6 (a míngua): −2 em todo teste; a noite não devolve PV. Desde o Dia 12. Você sabe: veio da adaga do túmulo. Não sabe: o que a quebra (um clérigo ou uma bruxa lê).`
- **No SÓ O MESTRE:** a categoria, a força, a chance de andar amanhã, a condição inteira, quem rogou. A rolagem da virada é oculta.
- **No `RETOMAR.md`** a maldição sempre entra, como a morte. E **o `fecha` recusa** o turno com maldição do personagem no passo 4 ou mais sem uma pergunta aberta sobre ela.
- **Gente com nome também é amaldiçoada,** e o relógio anda para ela como para o personagem: o mundo não gira em torno dele. Nesta etapa, só para quem o Mestre marcar (J.7).

### D.6 Cena de exemplo

Na Capela Caída (a ruína nova da vila de teste), Maro acha uma adaga Incomum num túmulo. `python3 ato.py vestir i0031`: a peça é `maldita`. O evento põe "a Mão Fria", Incomum, passo 1. A Firmeza de Maro fora da luta: 22 + 2,5 + 1 + 0 (amuleto Comum) = 25,5. A cada virada o mundo rola 2d20 + 6: anda 57% dos dias. Metade dos Maros morre em 8 dias, e nenhum antes de 5.

No Dia 3 a MESA diz "passo 3: a míngua". Nara lê a maldição (10 de prata): a condição é devolver a adaga ao túmulo, onde mora a aparição. Tentar o rito, ela pode: Conjuração +5,5 contra 34: 23% por dia, e falhando por 5 ou mais ela mesma leva a marca. A vila só tem quebra-maldição Comum: segura um dia por 6 de prata. O jogador escolhe: gastar prata para ganhar dias, ir à cidade atrás de um clérigo de verdade, ou voltar à capela com −2 em tudo.

---

## E. A peça encantada

- **O que é:** um feitiço da lista gravado numa arma, armadura ou escudo. Foco e amuleto não levam encanto: já são magia. O registro ganha `encanto: {feitico, grau, feito_por, dia}`. Um por peça; dois, do Único para cima.
- **O ofício é o `encanto`** (o mesmo que faz focos e amuletos), com bancada própria no lugar (`mesa_de_runas`, 0 a 4) e a maestria por blocos da forja.
- **O que pede:** a peça pronta; quem grava sabe o feitiço (ou tem ao lado, de ajudante, quem sabe); e uma **essência** da categoria da peça: até a Rara, 4 de osso e 2 de erva da categoria; do Épico para cima, **um núcleo da categoria**. O encanto disputa o núcleo com a forja.
- **Os blocos:** um terço dos da forja (Comum e Incomum 1, Rara 3, Épica 9, Única 27, Lendária 81).
- **O teste:** o da forja, com a maestria de encanto, contra 28 + 6 por categoria. Encantar uma peça Épica é tão difícil quanto forjá-la. Falhou por 1 a 4: grava um grau abaixo. Por 5 ou mais: a essência some (o núcleo também) e a peça perde 5 de durabilidade.
- **Na luta:** o dono solta o feitiço **uma vez por luta**, com as ações do feitiço e sem Mana (a carga é da peça, e volta com 1 bloco fora da luta). A peça vale como **foco um degrau abaixo** da categoria dela. A Conjuração é 2 por grau de quem gravou + Afinidade do dono ÷ 20 + o bônus desse foco.
- **A sintonia:** toda peça encantada ocupa um lugar de sintonia, de qualquer categoria (hoje só as Épicas ou melhores ocupam). A que dorme não solta. É o que impede o conjunto de cinco encantos.
- **Dois efeitos passivos novos** na lista de 2.11 (que fica com dez): `benta` (a arma conta inteira contra o imaterial; um clérigo a benze por rito, sem essência, e dura 7 dias) e `maldita` (D.2).

**Dentro da lei (medido; nível 50, espada Rara, 1.000 lutas):**

| A espada Rara traz gravado | Vence o gêmeo |
| --- | --- |
| seta: de perto · de longe | 48% · 52% |
| prender · escudo · lança de fogo | 50% · 51% · 50% |
| se o encanto valesse a categoria inteira: seta · lança | 54% · 58% |
| a bola, contra oito Incomuns com amuleto (sem o encanto: 28%) | 39% |
| a bola, contra oito Comuns com amuleto (sem o encanto: 76%) | 84% |

Um degrau abaixo e uma vez por luta: num igual o encanto não decide; contra a multidão de baixo, ajuda. O valor dele é o que a espada não faz: prender o urso antes de ele abraçar, a luz no escuro, a guarda do grupo, a cura de um golpe.

**Cena de exemplo.** Anselmo (Iniciante em encanto) grava `prender` na lança Incomum de Tomé: 4 de osso e 2 de erva Incomuns (48 de prata de matéria), 1 bloco. O teste: 2d20 + 2 + 8 (Afinidade 80) = +10 contra 34: acerta 40%, e em 43% das vezes a matéria some e a lança perde 5. Passou. Na mata, o urso vem. `"Tomé: usar lança"`: a lança vale como foco Comum; Conjuração 2 + 2 + 0 = +4 contra a Firmeza do urso, 28,5 (22, mais 2,5 da Vontade, 2 do instinto e 2 do corpo Incomum): pega 36%. Pegou: o urso fica preso por 2 turnos a 2 casas, onde a lança alcança e a pata não. A peça ocupa o único lugar de sintonia de Tomé (Vontade 53).

---

## F. A magia em todo lado

**Na vila de teste (o que muda no `vila_teste.py`):**

| O quê | Hoje | Com a etapa |
| --- | --- | --- |
| Nara, a curandeira | cura 2, coleta 2 | clériga Iniciante (voto do socorro), símbolo Comum, sabe cura e amparo; botica 1; lê maldição |
| Anselmo, o velho (novo) | | mago de nível 34, arcano Treinado e Lerdo (por isso ficou na vila), cajado Incomum; ensina seta, prender, escudo e luz a 6 de prata por bloco; Iniciante em encanto |
| Quitéria (nova) | | bruxa Treinada, numa cabana na borda da mata; lê, vende veneno, roga praga por paga, e deve |
| Rute, a caçadora | arco 4, caça 4 | Jeitosa no verde; sabe afugentar |
| Tomé, o guarda | lança Incomum | traz um amuleto Comum |
| Zeca, o aprendiz | nada | Grande Dom na forja, que ninguém sabe |
| a prateleira | 15 peças | mais: 6 poções de cura e 2 antídotos Comuns, 1 cura Incomum, 1 quebra-maldição Comum, 2 amuletos Comuns (10 de prata), 1 varinha e 1 símbolo Comuns, e o escrito "Cartilha do arcano" (seta e luz) |
| os ermos | a Mata do Corvo | mais 2 fogos-fátuos na mata; e **a Capela Caída** (ruína de borda, a 2 blocos, lugar maldito Comum): ratazanas, surucucu, uma aparição, e a adaga do túmulo |
| os começos | ferreiro, caçador, guerreiro | mais o **aprendiz de mago** (Afinidade 70, arcano Iniciante com 40 blocos, varinha Comum, sabe seta e luz) |

**O que a gente comum sabe:** todo adulto sabe o que é maldição, que amuleto guarda e que clérigo quebra. 1 em 20 sabe um truque (10 blocos de alguma tradição); 1 em 100 é Iniciante. Uma vila de 400 tem uns 4 lançadores e talvez um Treinado; uma cidade de 1.500 tem botica 2, um santuário ou uma escola e 1 ou 2 Mestres; Lendários, o mundo tem contados.

**O que se vende e o que se paga (a prata só muda de mão):** a loja vende poção até a Rara, amuleto e foco até o Épico, escritos de grau 1 e 2. A curandeira trata ferida (metade do repouso, como hoje), cura (3 de prata por lance), lê maldição e dom (10), benze antes da luta (5 por pessoa) e tenta o rito. A lição custa o salário de quem ensina.

**Cena de exemplo.** Começo novo: `python3 vila_teste.py minha_vila comeco=aprendiz nome=Lia`. A `MESA.md` abre com: "Mana 14 de 14 · arcano: Iniciante (40 blocos) · sabe: seta, luz · varinha Comum na mão". Em "Aqui": "Anselmo ensina prender e escudo: 6 blocos cada, 6 de prata por bloco. Nara cura por 3 e lê por 10. Na loja: 6 poções de cura (6 cada), 2 amuletos (10), a Cartilha do arcano (30)." Lia tem 30 de prata: `python3 mercado.py comprar amuleto` leva 10, e uma lição inteira custa 36.

Ela serve dois blocos por dia na botica de Nara (`python3 alquimia.py jornal 2`: 3 de prata por bloco, de aprendiz) e estuda um: `python3 magia.py estudar prender com=anselmo`. No quarto dia de estudo, e não no sexto, a saída diz "Lia aprendeu prender": ela é Jeitosa no arcano sem saber, os 6 blocos viraram 4, e a lição saiu por 24 de prata. No bloco 20 de estudo a MESA avisa: "o arcano lhe vem fácil". À noite, `python3 turno.py abre` traz um dos dois fatos que não tocam o personagem: "Quitéria desceu à vila e saiu da loja sem comprar. Tomé não tirou a mão do amuleto."

**Ganchos para as etapas seguintes:**
- **3, a região:** escola, templo e círculo são lugares com `ensina: [feitiços]`; o freguês encomenda poção e amuleto pelo valor inteiro; a caixa de entrada recebe "a maldição de Fulano chega ao passo 5 em 3 dias" e o voto do socorro.
- **5, os rivais:** 1 rival em 4 é lançador; talento e dom saem do mesmo dado; o ranking ganha a coluna da tradição; a conta rápida da luta longe do jogador precisa de um termo para foco e amuleto (a meta do erro menor que 8 pontos vale para ela).
- **6, as frentes:** a praga que anda de lugar em lugar; o culto; o nêmesis que roga praga ao herdeiro; a maldição de sangue, que passa ao herdeiro dois passos atrás.
- **7, a história:** o dom corre no sangue das casas; toda peça maldita tem a história de quem a amaldiçoou; todo lugar maldito é uma ruína com origem.

---

## G. O banco de provas da etapa

Três bancos novos, encadeados no `provas_mundo.py` como os de hoje: `provas_talento.py`, `provas_magia.py` (a luta: magia, poção, encanto) e `provas_alquimia.py` (a bancada, o mercado, a maldição). Meta que falha fica falhando às claras.

| N.º | O que se mede | Faixa | Como se mede | Em rascunho |
| --- | --- | --- | --- | --- |
| T1 | o banco de hoje com a etapa ligada e ninguém com talento | 79 de 79 e 87 de 87; mesma semente, mesma luta | os bancos de hoje | medido em três lutas-tipo (idêntico) |
| T2 | a sorte de nascer, em 10.000 nascidos | Prodígio e Negado 1,5 a 2,5% por caminho; Jeitoso e Lerdo 8 a 12%; Dom 3,5 a 5,5% das pessoas; Grande Dom 0,3 a 0,8% | o dado do mundo, 20 sementes | conta |
| T3 | a escada do ferreiro prodígio (1ª obra fecha) | Épica 25 a 35 · Única 70 a 90 · Lendária 200 a 230 | o robô ferreiro de hoje, com talento +2; 30 vidas | conta: 30 · 77 · 213 |
| T4 | o ferreiro lerdo | Única 170 a 200; não abre a Lendária | o mesmo | conta: 184 |
| T5 | o prodígio nunca está duas categorias à frente do comum no mesmo dia | nunca | dia a dia, nas vidas de T3 | conta: nunca |
| T6 | Dom · Grande Dom contra o gêmeo | 51 a 58% · 54 a 64% | 1.000 lutas | 54 a 55% · 56 a 61% |
| T7 | Grande Dom contra a arma uma categoria acima | até 15% | 1.000 lutas | 5 a 6% |
| T8 | Mestre com Grande Dom contra Lendário sem dom | 42 a 58% | 1.000 lutas | 49% |
| T9 | o melhor ferreiro possível, com Grande Dom, acerta a Lendária | 15 a 30% (a meta de hoje) | conta exata | 25,7% (sem o teto de +8 seriam 32,2%) |
| T10 | o talento só aparece na MESA depois de 20 blocos; o dom, quando decide um teste | sempre | três vilas, lendo a MESA | não feito |
| M1 | mago contra mago | 44 a 56% | 600 lutas | 49% |
| M2 | mago contra guerreiro com amuleto: longe · perto · colado | 28 a 45 · 12 a 28 · 4 a 16 | 600 por começo | 36 a 39 · 18 a 20 · 9 a 10 |
| M3 | o mesmo, sem amuleto: quanto o mago ganha | 15 pontos ou mais, de longe e de perto | 600 por começo | +27 e +24 |
| M4 | foco uma acima contra o igual com amuleto: longe · perto | 85 a 100 · 65 a 90 | 600 | 95 a 96 · 80 a 81 |
| M5 | mago contra amuleto uma acima · contra conjunto uma acima | 2 a 18 · 0 a 8 | 600 | 8 a 9 · 0 a 1 |
| M6 | nível 50, foco duas acima, contra nível 500 com amuleto: longe · perto | 65 a 92 · 15 a 40 | 600 | 82 a 84 · 24 a 26 |
| M7 | nível 50, foco uma acima, contra nível 500, de longe | 5 a 30 | 600 | 22 a 24 |
| M8 | nenhum feitiço tira, na mediana, mais de 45% do PV de um igual com amuleto; a seta, até 20% | sim | os acertos de 600 lutas | médias: seta 21%, lança 41%, raio 51 a 53% (a mediana é menor; não tirei) |
| M9 | a Mana, só de seta: seca na rodada · a volta rende a mais em 20 rodadas | 6 a 10 · 25 a 50% | 200 lutas contra um alvo que não morre | 8 · 36% |
| M10 | grupo de cinco, um mago no lugar de um guerreiro: sem área · com área contra amuleto · contra sem amuleto | 40 a 55 · 52 a 70 · 75 a 92 | 300 lutas | 47 · 62 a 63 · 84 a 86 |
| M11 | o mesmo no corredor de dois (com área) | 50 a 68 | 300 | 58 a 59 |
| M12 | o clérigo na linha no lugar de um guerreiro: campo · corredor · benzendo antes | 42 a 58 · 48 a 64 · 5 a 14 pontos a mais | 300 a 400 | 44 a 52 · 56 a 57 · +8 a +11 |
| M13 | o druida · a bruxa no lugar de um guerreiro | 45 a 62 · 42 a 58 | 300 | 53 · 48 |
| M14 | a bruxa sozinha contra o guerreiro, de longe | 5 a 20 | 600 | 12 |
| M15 | o feitiço longo sob flecha: uma arqueira · duas | 15 a 35% perdidos · 25 a 50% | 600 | 25 a 27% · 35 a 36% |
| M16 | o mesmo sob duas arqueiras, com um guarda de escudo na frente do mago | 3 pontos a menos, ou mais | 600 | 31% contra 36% |
| M17 | retrochoque: lance comum · lance forçado | 0,1 a 0,5% · 8 a 12% | 20.000 lances | conta: 0,25% · 9,75% |
| M18 | um mago Raro contra 8 · 12 Comuns sem amuleto, de longe | 55 a 85 · 35 a 70 | 120 | 72 a 77 · 47 a 55 |
| M19 | mago Raro contra a pantera: longe · perto; contra o trasgo | 35 a 60 · 0 a 12 · 30 a 55 | 600 | 51 a 52 · 4 a 5 · 43 |
| M20 | cada traço novo de bicho, com ele e sem ele | 8 pontos ou mais | 600, como os traços de hoje | não medido |
| M21 | o controle: pega no igual com amuleto · calejado duas vezes | 55 a 75% · 25 a 40% | conta e 2.000 lances | conta: 66% · 32% |
| P1 | 1 poção da categoria · 2 · a terceira | 52 a 62 · 55 a 68 · não soma mais de 3 pontos | 1.000 | 56 · 61 · 60 |
| P2 | poção uma abaixo da ferida · uma acima | 47 a 53 · 55 a 68 | 1.000 | 50 · 61 |
| P3 | veneno de lâmina (a regra proposta) | 52 a 62 | 1.000 | 59 a 64 com a regra do bicho; a proposta, por medir |
| P4 | veneno e 2 poções · 2 poções contra a arma uma acima | até 75 · até 12 | 1.000 | 70 · 4 |
| P5 | **o alquimista de loja não é mina** | dias 1 a 5: média até 6 de prata por dia, pior caso até 12; dias 6 a 30: até 4 | o robô ganancioso de hoje, na vila de teste, 30 vilas | conta com a fórmula do mercado: 0 a +1,5 |
| P6 | o coletor que faz poção, no bolso | de −0,5 a +2 por dia | o robô coletor de hoje, com a botica; 50 vidas | conta: +1,2 a +1,7 |
| P7 | fazer amuleto e foco para a loja não é mina | a mesma faixa de P5 | o robô do ferreiro de loja, no ofício de encanto | chute: cerca de +3 no primeiro dia, caindo |
| P8 | a prata do mundo fecha; a matéria da leva falhada some; o núcleo perdido sai do Livro | sempre | 200 negócios e 60 levas | não feito |
| P9 | o limite do corpo e o teto da cura por dia | a poção a mais não cura; nunca mais que metade do PV por dia | prova posta à mão | não feito |
| D1 | a maldição da categoria da guarda mata em | 10 a 25 dias (metade das vidas) | 4.000 vidas, o dado do mundo | 15 |
| D2 | maldição Comum num aldeão sem amuleto · nenhuma mata antes de | 7 a 14 dias · 5 dias | 4.000 vidas | 10 · 5 |
| D3 | a pena: −1 · −2 · −4 contra ele mesmo são | 38 a 47 · 32 a 43 · 20 a 32 | 1.000 | 42 · 38 · 26 |
| D4 | o clérigo quebra: a da categoria do foco · a de uma acima | 45 a 65% · 30 a 45% | conta exata | 57% · 40% |
| D5 | um ano sem jogador, 20 sementes | de 0 a 6 com nome mortos de maldição; nenhuma sem fonte nem condição; morto sem relógio andando | o ano de prova (etapa 7); até lá, 60 dias na vila de teste | chute |
| D6 | a MESA e o RETOMAR mostram toda maldição do personagem; o `fecha` recusa no passo 4 sem pergunta | sempre | três vilas | não feito |
| E1 | encanto de dano num igual | 46 a 56% | 1.000 | 48 a 52% |
| E2 | encanto de área contra oito de uma categoria abaixo | 5 a 15 pontos a mais | 250 | +8 a +11 |
| E3 | a peça encantada que dorme não solta; a sintonia conta toda peça encantada | sempre | prova posta à mão | não feito |
| E4 | gravar custa o que diz: a essência some na falha grande; a chance é a da forja | sempre; a conta exata | 60 gravações | conta |
| V1 | a vila de teste nasce inteira nos quatro começos, com os lançadores, a prateleira e a capela | o estado válido | `estado.valida` | não feito |

**O que eu mediria antes de construir, e não medi:** o veneno com a regra proposta; M20; a guarda do clérigo em grupo; o cego, o medo e o nó; o grau 4; os robôs de P5 a P7 de verdade (o que tenho é a conta, não a vida inteira); e tudo de D5.

---

## H. Como construir

**A ordem, em três levas. Dentro de uma leva, ninguém mexe em arquivo de outro.**

**Leva 0, o alicerce (um construtor; curta; os bancos de hoje têm de passar inteiros no fim):**

| Arquivo | O que muda ou nasce | O que expõe |
| --- | --- | --- |
| `tabelas_talento.py` (novo) | A.9 | `CAMINHOS`, `TALENTO`, `DOM`, `blocos()`, `caminho_de()` |
| `tabelas_magia.py` (novo) | B, D e E em números | `conjuracao()`, `firmeza()`, `mana_max()`, `GRAUS`, `FOCOS`, `TRADICOES`, `FEITICOS`, `ESTADOS`, `MALDICAO_PASSOS`, `forca_maldicao()`, `ENCANTO_*` |
| `tabelas_mundo.py` | `OFICIOS` ganha alquimia, encanto e as quatro tradições; `EVENTOS` ganha estudar, alquimia, encantar, rito, maldicao; `MODULOS` ganha magia, alquimia, maldicao; os bens de poção | |
| `tabelas.py` | três moldes de gente gerada (mago, clérigo, druida) | |
| `estado.py` | campos `talento`, `dom`, `mana`, `funda`, `maldicoes`, `feiticos`, `bebeu` na pessoa; `botica`, `mesa_de_runas`, `santuario`, `maldito` no lugar; o efeito `maldicao`; a poção como bem conhecido; os invariantes novos | o gravador segue um só |
| `itens.py` | tipos `foco`, `amuleto`, `elixir`, `escrito`; campos `encanto` e `dose`; efeitos `benta` e `maldita`; a janela lê tudo isso | `item()`, `janela()` |

**Leva 1, quatro construtores ao mesmo tempo:**

| Construtor | Arquivos só dele | O que expõe |
| --- | --- | --- |
| **1. O talento** | `talento.py` (novo), `provas_talento.py` (novo); e uma linha em cada "sobe" de `ato.py`, `oficio.py`, `caca.py`, `mercado.py` | `talento.nasce(E, pid)`, `talento.pede(p, chave, tabela, grau)`, `talento.dom(p, chave)`, `talento.revela(E, pid)`, `mesa(E)`, `so_mestre(E)` |
| **2. A luta** | `pessoas.py`, `luta.py`, `magia.py` (novo), `bichos.py`, `tabelas_bichos.py`, `provas_magia.py` (novo), `estresse.py` | `magia.lanca`, `resolve`, `guarda`, `concentra`, `escolhe`, `passa` (os prazos), `bebe`, `usa_peca`; a ficha ganha `mana`, `conj`, `foco`, `amuleto`, `firmeza`, `encanto`, `funda`. Na luta: os ganchos em `nova`, `_decide`, `_turno`, `golpe`, `_para`, `ordem`, `situacao` |
| **3. A bancada** | `alquimia.py` (novo), `encanto.py` (novo), `tabelas_alquimia.py` (novo), `tabelas_mercado.py`, `provas_alquimia.py` (novo) | `alquimia.fazer`, `continua`, `larga`, `virada`, `mesa`; `encanto.gravar`, `fazer` (foco e amuleto), `benzer`. Importam do `oficio.py` e não o editam |
| **4. A maldição** | `maldicao.py` (novo), `corpo.py`, `provas_maldicao.py` (novo, chamado pelo de alquimia) | `maldicao.poe`, `virada`, `quebra`, `rito`, `pena(p)`, `mesa`, `so_mestre`, `retomar` |

**Leva 2, a costura (um construtor), e depois a conferência:**
- `ato.py` (treinar aceita tradição; `estudar`; a luta que volta ao estado devolve Mana, ferida funda e maldição; a Mana volta por bloco), `turno.py` (a MESA, o RETOMAR, o `fecha` que recusa), `vila_teste.py`, `provas.py` e `provas_mundo.py` (o encadeamento), `GUIA_VILA.md`, `REGRAS.md` (capítulos 10 a 14: os dons, a magia, a alquimia, as maldições, o encanto), `MUDANCAS.md`.
- **Dois verificadores,** como na etapa 2: um pelos bancos e pelo livro; outro jogando quatro vilas atrás de "fique forte depressa" e "fique rico depressa" (poção, amuleto, serviço de cura, lição vendida, companheiro benzido).

**O tamanho:** cerca de 2.600 linhas novas (magia 600, talento 150, alquimia 350, encanto 250, maldição 250, tabelas 300, provas 700) e 400 mexidas. O motor passa de 10 mil para 13 mil.

**O que eu deixaria de fora desta etapa:** os feitiços de grau 4 (ficam só na tabela, sem meta); o contrafeitiço como reação; a alquimia de guerra (frasco de arremesso com área); invocar além do `chamar`; voo, teleporte, ilusão e ler pensamento; ressuscitar (nunca: todo mundo morre de vez); o clima do mundo por magia; dois encantos na mesma peça; a batalha de multidão com magos (é das frentes); e o canto.

---

## I. O que é do jogador decidir

A pergunta que já estava aberta (magia contra aço) este projeto responde como o orquestrador propôs: a mesma conta, com o foco no lugar da arma. B.10 mostra que ela fecha. As seis novas:

1. **Quem não tem amuleto, quanto apanha de magia?**
   a) A armadura guarda 0,6 do valor (medido: sem amuleto, o mago passa de 36 para 63% de longe; a área, de 63 para 84%). **Recomendo.** b) Um degrau abaixo: o amuleto vira peça obrigatória (78% e 98%). c) A armadura guarda inteira: o amuleto só serve contra controle e maldição (40% e 65%).
2. **O dom do ferreiro mexe na chance da Lendária?**
   a) Não: o dom entra dentro do teto de +8 do preparo, e o melhor ferreiro possível segue em 1 em 4. **Recomendo** (é a sua decisão 9). b) Sim: soma por fora, e o Grande Dom chega a 1 em 3.
3. **Como o seu personagem ganha talento e dom?**
   a) O dado do mundo, como toda gente. b) O dado, e uma inclinação escolhida (naquele caminho rola duas vezes e vale o melhor). **Recomendo.** c) Você escolhe um caminho Jeitoso e o dado lhe dá um Lerdo em outro.
4. **Quão depressa o prodígio aprende?**
   a) Com metade dos blocos: a primeira tentativa de Lendária no Dia 213, em vez do 356. **Recomendo**, sabendo que mexe no ritmo decidido. b) Com dois terços (Dia 260). c) Com metade, mas só até Mestre; de Mestre a Lendário, como todo mundo (Dia 302).
5. **A quarta tradição entra agora?**
   a) Sim, a bruxaria, dona das maldições. **Recomendo.** b) Não: só mago, clérigo e druida; a praga fica com bicho, lugar e peça. c) Outra (o canto, a alquimia de guerra), numa etapa adiante.
6. **Quão dura é a maldição?**
   a) Um teste por dia: da categoria da guarda, mata em cerca de 15 dias; num aldeão, em 10. **Recomendo.** b) Um teste a cada 3 dias: perto de um mês e meio. c) Como em (a), mas gente com nome só morre de maldição depois de o aviso cair na sua caixa de entrada.

---

## J. Honestidade: o que não sei e o que pode quebrar

1. **Os números de luta dependem do robô.** O mago do rascunho joga por uma regra curta. Um jogador, com a luta parando e perguntando, joga melhor: recua, escolhe o alvo, guarda a Mana. Os 36% de longe são piso, não teto. Depois da primeira vila jogada, o duelo se mede de novo.
2. **A área contra quem está apinhado.** Em campo aberto a luta põe a frente inteira de um lado na mesma casa, e a bola pega quatro. Com amuleto, rende 13 pontos; sem, 34 a 36. Se for demais, o primeiro botão é o número de alvos (4 para 3); o segundo, o custo (6 para 8 de Mana).
3. **O amuleto é mais uma peça para comprar e para sustentar.** A sintonia aperta: com Vontade 55, duas peças altas acordadas, e agora há cinco candidatas. É de propósito, e encarece o caminho de todo mundo.
4. **O −2 pesa muito.** Mau-olhado, veneno e maldição dão todos −2, e −2 em tudo vale 12 pontos. Por isso não somam entre si. Somados à fome e ao sono, um personagem pode chegar a −8: a MESA tem de dizer a conta inteira antes da luta.
5. **A cura pequena pode frustrar.** O clérigo no grupo vale um guerreiro (44 a 52%), não mais. A cura dele brilha entre as lutas, e contra ferida de categoria acima vale um terço. Se o jogador quiser o curador que vira a luta, o número é o 6 da conta da cura; com 8 já medi, e não muda quase nada, porque a luta dura 5 rodadas.
6. **A alquimia eu só contei, não vivi.** A conta do mercado diz que não há mina; um robô de 30 dias pode achar um caminho que a conta não viu (o atravessador de comida, da etapa 2, também não estava em conta nenhuma).
7. **A maldição mata gente com nome longe do jogador.** Sem as etapas 3 e 6, ninguém do mundo procura um clérigo sozinho. Até lá, a virada da maldição só anda para o personagem e para quem o Mestre marcar.
8. **O prodígio muda o ritmo decidido** (pergunta 4). E num mundo de 190 com nome, 2% é pouca gente: há sementes sem nenhum prodígio no próprio ofício. Se o jogador quiser um prodígio rival garantido, é linha do gerador, não regra.
9. **O que medi de verdade:** B.2, B.6, B.7, B.8 e B.10 (600 lutas por linha; o grupo, 300); A.6 e C.4 (1.000 a 1.500); E (1.000; a multidão, 250); o relógio de D.3 (4.000 vidas, dado puro). **O que é conta exata:** a escada de A.7, o dom na forja, o controle de B.5, o rito de D.4, o mercado de C.5. **O que é chute:** o grau 4, os traços novos de bicho, os preços dos serviços, a raridade do talento, tudo de F.
