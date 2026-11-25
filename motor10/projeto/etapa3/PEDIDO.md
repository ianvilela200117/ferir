# Motor 10: o pedido de projeto da ETAPA 3 (a região que responde)

Este trabalho é FORA do jogo de Ferir. O CLAUDE.md do repositório fala daquele jogo: as regras dele (abrir sessão, ler MESTRE.md, rodar scripts da raiz) NÃO valem aqui. Os arquivos da raiz do repositório (o atlas, os compêndios, o cânone, os mapas) são de OUTRO jogo: não copie nomes nem conteúdo deles. Aqui você é projetista de um motor de RPG novo, em Python (só a biblioteca padrão), todo em português, em `/home/user/ferir/motor10/`.

## 0. As regras de trabalho

1. NÃO EDITE NADA em `/home/user/ferir`, a não ser dentro da SUA pasta de projeto (o caminho está no seu pedido). NUNCA rode script da raiz do repositório. Não use git para nada.
2. Pode rodar os scripts de `motor10/` para MEDIR, de dentro de `motor10/`, com `PYTHONDONTWRITEBYTECODE=1` e com `MOTOR10_MUNDO` numa pasta de rascunho FORA do repositório (o caminho está no seu pedido). Por exemplo, uma vila nova inteira: `python3 vila_teste.py PASTA`, depois `python3 vila_teste.py magia PASTA` e `python3 vila_teste.py fantasia PASTA`. A pasta `motor10/ensaio/` é o SAVE DO JOGADOR: não escreva nela e não rode comando nenhum apontando para ela (pode copiá-la para o seu rascunho). Nunca crie `motor10/mundo`.
3. Os seus scripts de medida ficam em `SUA_PASTA/medidas/` e rodam de dentro de `motor10/`. O mundo que eles criam fica no rascunho de fora, nunca no repositório.
4. Português simples e direto, sem jargão e sem travessão. Quem lê no fim é o jogador.

## 1. O que ler antes

- `motor10/LEIA.md`, `motor10/PROJETO.md` (o plano inteiro: o mundo na seção 3, o turno e o gravador na 6, os dados e os scripts na 8, o banco do mundo na 9, as etapas na 10; as decisões do jogador estão na seção 12, e o que a etapa 2 deixou para decidir, na 13), o `motor10/GUIA_VILA.md` (a vila de teste que o jogador joga, e a seção "O que ainda NÃO existe"), e o fim do `motor10/MUDANCAS.md`.
- `motor10/REGRAS.md`: os capítulos 1 a 3 (a pessoa, os itens, a luta), o 5 (o tempo, o corpo, o estado e o turno), o 7 a 9 (o ofício, o mercado, a caça e a coleta), o 14 (a magia no mundo e os serviços), o 17 e o 18 (as masmorras e o ladino, com o furto escrito e desligado) e o 20 (os dragões, o ataque à aldeia).
- O código que a etapa vai tocar, conforme a sua parte: `estado.py` (o único gravador: efeitos tipados, invariantes, o `valida`), `tabelas_mundo.py`, `ato.py` (o `passa`, os atos), `corpo.py`, `turno.py` (o `abre`, a `MESA.md`, o `fecha`, as perguntas), `pessoas.py`, `mercado.py` e `tabelas_mercado.py`, `caca.py` e `tabelas_caca.py` (a saída ao ermo é o molde mais próximo da viagem), `bichos.py`, `criaturas.py` (o covil que rouba da vila), `manha.py` (o furto desligado), `dragoes.py` (Vau Seco e o Tição, que já existem longe de Pedra Rasa), `vila_teste.py`, e os bancos (`provas.py`, `provas_mundo.py` e os dos módulos).

## 2. O que o jogador decidiu (não se discute; projeta-se em cima)

1. **O save novo só nasce com o motor inteiro** (decisão 20). Esta etapa é a primeira das quatro que faltam (3, 5, 6 e 7). O personagem do Dia 1 será humano, ferreiro, com as inclinações na forja e no encanto: a região tem de ter onde ele viva disso (forjas de níveis diferentes, a forja de cidade que o Raro pede, uma mesa de runas e quem ensine o encanto).
2. **O que a etapa entrega** (seção 10 do `PROJETO.md`): o mapa, a viagem, os nomeados com memória, a notícia, a caixa e as missões. **O que se joga ao fim:** viajar, ter cliente, ter prazo.
3. **O mundo é de verdade:** vive com você ou sem você; quem o personagem não vê também age; o mundo não gira em torno do personagem. Os rivais aventureiros, as guildas e o ranking são da etapa 5; as frentes, a calamidade, o herdeiro e o diretor, da 6; a história de séculos, da 7. Esta etapa deixa os ganchos para elas, sem fazê-las.
4. **Valem as leis e as decisões antigas:** o item decide (cada categoria vale 3 da de baixo); aprende-se fazendo; vida única; a Lendária difícil de propósito; a loja paga 40% pelas peças e 60% pelos bens; o conserto pago prende quem espera; a caça de começo fica como está; a luta à moda da mesa só nas grandes (F1 b); frota enxuta.

**As leis do motor, que a etapa não pode quebrar:**
- **Todo número mora nas páginas `tabelas*.py`.** Nenhuma regra vale antes de passar no banco de provas. O que não bate fica falhando às claras.
- **Só o `estado.py` grava o mundo,** por eventos com efeitos tipados de uma lista fechada; evento sem efeito é recusado; os invariantes são conferidos. O tempo só anda pelo `ato.passa`, em blocos de 4 horas. O dado do mundo sai de `estado.sorte`; o dado do jogador, de `teste.rola`, declarado e rolado uma vez; o que o personagem não pode saber sai como "rolagem oculta".
- **Cada fato num lugar só.** O dono da peça só no Livro de Itens; onde a pessoa está, só na ficha dela. A memória de alguém, a notícia, a caixa e a missão também moram num lugar só cada uma.
- **A economia é frágil:** a prata não nasce nem some sem um motivo escrito no estado. Hoje a prata do lugar não se repõe e ninguém além do personagem compra da prateleira (seção 13 do `PROJETO.md`): esta etapa resolve isso, e todo caminho novo de renda (o frete, o atravessador, a missão, o furto, a encomenda) precisa de meta no banco que impeça a mina.
- **O Mestre não esquece:** a `MESA.md` sai do estado e tem meta de 8 KB (hoje a do `ensaio/` já passa de 16 KB: diga como a região cabe nela, ou o que sai dela). O que o Mestre lê ao abrir a sessão tem meta de 30 KB no total.
- **Velocidade:** um ano inteiro de mundo sem jogador tem de rodar em menos de 2 minutos (seção 9, meta 10). Diga quanto o seu desenho custa por dia de mundo.
- **O save do jogador tem de seguir abrindo:** todo campo novo tem valor padrão para o save antigo. A etapa entra no `ensaio/` por um comando que só acrescenta (como o `vila_teste.py magia` e o `fantasia`): a região nasce EM VOLTA do que já existe (Pedra Rasa, a Mata do Corvo, a Cova Velha e a cripta, Vau Seco, a Serra Fria e o Tição), sem recriar nada.
- **A etapa 7 vai fazer nascer a região a partir da história.** O gerador da região desta etapa tem de aceitar que a história ponha nele as casas, as ruínas, os donos das peças altas e os mortos: diga qual é a porta de entrada.

## 3. As duas metades (a sua está no seu pedido)

**A, o chão da região:** o mapa (a região de 16 lugares da seção 3, com os ermos, as masmorras e as 24 rotas; o gerador por semente); a viagem (andar uma rota em blocos, com o corpo, a estação, dormir no mato, o perigo da rota que sai da conta, o encontro que sai da contagem real, quem vai junto, a carga e o seu peso, a comida que estraga); o povo em número (come, produz, compra, migra, passa fome); o comércio entre lugares (o preço que difere de lugar para lugar, quem leva os bens de um ao outro, a prata do lugar que se repõe, a freguesia que compra da prateleira, o atravessador da seção 13); os ofícios pela região (as forjas e as mesas de runas de níveis diferentes, quem ensina o quê e onde); o bicho que sai do ermo e o povo que caça e coleta. **É dono de:** `lugares` (o mapa, as rotas, o estoque, o povo em número) e do que anda neles.

**B, a gente que responde:** os nomeados da região (a seção 3 fala de 150), com rotina de 6 blocos, um querer por semana que vira ato com efeito, laços entre si, e a MEMÓRIA (até 12 fatos com peso, de onde sai a opinião sobre o personagem, com os porquês); a fama; a notícia que anda uma rota por dia e vira boato depois do quarto salto (você só lê o que chegou aonde está); a caixa de entrada com prazo (`{de, pede, prazo, opções, padrão}`; só escreve quem tem motivo no estado; vencido o prazo vale o padrão, com custo; cabem 7); as missões (quem pede, a caução, a paga, o prazo, a fama; qualquer um pode cumprir); a encomenda ao ofício (o cliente do ferreiro e do encantador); quem vai junto pede paga, ou recusa o perigo, pela opinião e pelo querer dele; o furto, que está escrito e desligado no capítulo 18 e entra agora, quando a gente lembra de quem a roubou. **É dona de:** `gente` (os nomeados e a memória), `caixa`, `missoes` e `noticias`.

**Onde as metades se tocam** (cada projetista diz o que precisa do outro, e propõe a forma): a notícia anda pelas rotas de A; a missão leva o personagem pela viagem de A; o cliente de B compra com a prata e no mercado de A; o povo em número de A é de onde saem os nomeados novos de B e quem engrossa o bando. Os verbos novos do gravador (rota, caixa, missão, fama, laço, notícia: seção 6 do `PROJETO.md`) e a `MESA.md` são de um alicerce comum, que se constrói primeiro.

## 4. O que cada projeto tem de cobrir

Para a sua parte:
- **As regras, com números:** tabelas que caberiam num `tabelas_*.py`, contas feitas, e medidas de rascunho contra o motor de hoje (rode o motor: crie vilas, ande o tempo, meça). Diga o que mediu e o que é chute.
- **O estado:** como fica guardado (campos da pessoa, do lugar, do item; arquivos novos do save; eventos e efeitos novos; invariantes), sempre com valor padrão para o save antigo. Quanto pesa em KB num ano de mundo.
- **Os comandos e a mesa:** o que o Mestre roda, o que a `MESA.md` mostra (e o que sai dela para caber), onde o jogo para e pergunta, o que vai ao SÓ O MESTRE.
- **Uma cena jogada** na vila de teste com a região em volta, em comandos e números, de dois ou três parágrafos (o Maro, ou o ferreiro do Dia 1).
- **As metas do banco:** o que medir, com faixa e com o jeito de medir (robôs, quantos dias, quantas sementes), incluindo as que impedem a mina, as que mostram que o mundo anda sem o personagem, e as que mostram que a vila de teste de hoje segue igual quando ninguém sai dela.
- **A construção:** os arquivos novos e os que mudam, o que cada um expõe, e como repartir entre poucos construtores sem que dois mexam no mesmo arquivo. Diga o que vai no alicerce comum.
- **O que fica de fora** desta etapa (simples onde der: o motor já tem mais de 23 mil linhas).
- **No máximo quatro perguntas ao jogador,** cada uma com opções e a sua recomendação. Só o que é gosto dele; o que é conta, decida você.

Honestidade: o que você não sabe, o que pode quebrar o equilíbrio, e o que mediu de verdade. Escreva o projeto em `SUA_PASTA/PROJETO.md` (direto ao ponto: o jogador lê o juízo, não o projeto inteiro; o orquestrador lê tudo).
