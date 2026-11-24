# Motor 10: o pedido de projeto da ETAPA 4b (as masmorras e o mundo de fantasia)

Este trabalho é FORA do jogo de Ferir. O CLAUDE.md do repositório fala daquele jogo: as regras dele (abrir sessão, ler MESTRE.md, rodar scripts da raiz) NÃO valem aqui. Os arquivos da raiz do repositório (o atlas de masmorras, os compêndios, o cânone) são de OUTRO jogo: não copie nomes nem conteúdo deles. Aqui você é projetista de um motor de RPG novo, em Python (só a biblioteca padrão), todo em português, em `/home/user/ferir/motor10/`.

## 0. As regras de trabalho

1. NÃO EDITE NADA em `/home/user/ferir`. Leia o que quiser; escreva só na SUA pasta de rascunho (o caminho está no seu pedido). NUNCA rode script da raiz do repositório. Não use git para mudar nada.
2. Pode rodar os scripts de `motor10/` para MEDIR, de dentro de `motor10/`, com `PYTHONDONTWRITEBYTECODE=1` e com `MOTOR10_MUNDO` numa pasta sua de rascunho (por exemplo uma vila nova: `python3 vila_teste.py PASTA` e depois `python3 vila_teste.py magia PASTA`). A pasta `motor10/ensaio/` é o SAVE DO JOGADOR: não escreva nela e não rode comando nenhum apontando para ela (pode copiá-la para o seu rascunho). Nunca crie `motor10/mundo`.
3. Português simples e direto, sem jargão e sem travessão. Quem lê no fim é o jogador.

## 1. O que ler antes

- `motor10/LEIA.md`, `motor10/PROJETO.md` (o plano inteiro; as decisões do jogador estão na seção 12, e a etapa 4b na seção 10), `motor10/REGRAS.md` (o livro em vigor: os capítulos 1 a 3 são a pessoa, os itens e a luta; o 6 e o 7 os bichos e a caça; do 10 ao 16 os dons, a magia, as maldições e as criaturas), o fim do `motor10/MUDANCAS.md`, e o `motor10/GUIA_VILA.md` (a vila de teste que o jogador joga).
- O código que a etapa vai tocar, conforme a sua parte: `tabelas.py`, `pessoas.py`, `itens.py`, `luta.py`, `estado.py` (o único gravador: efeitos tipados, invariantes), `ato.py`, `corpo.py`, `caca.py` e `tabelas_caca.py` (a saída ao ermo é o molde mais próximo de descer numa masmorra), `bichos.py`, `tabelas_bichos.py`, `criaturas.py`, `tabelas_criaturas.py` (os povos, os chefes com fases, os covis), `talento.py` e `tabelas_talento.py` (os 16 caminhos), `magia.py`, `tabelas_magia.py`, `mercado.py`, `turno.py`, `vila_teste.py`, e os bancos de provas (`provas.py`, `provas_mundo.py` e os dos módulos).

## 2. O que o jogador decidiu (não se discute; projeta-se em cima)

O jogador gosta muito de Dungeons & Dragons e pediu que estes aspectos entrem, todos, nesta etapa, ANTES da região:
1. **As masmorras:** salas, portas, armadilhas, o escuro, o tesouro e o chefe no fundo; descer com um grupo.
2. **O ladino:** andar escondido, abrir fechadura, desarmar armadilha.
3. **Os dragões de verdade,** com covil e tesouro.
4. **Os povos para o personagem:** anão, elfo, meio-orc e outros da fantasia comum.

**O que NÃO pode entrar:** nada que seja criação exclusiva de um jogo ou livro específico, nem o nome nem a aparência (nada de "beholder", "devorador de mentes", "drow", "tiefling", "dragonborn", nem os mundos, os deuses ou as cores de dragão daquele jogo, nem a lista de magias dele). Só o que é da fantasia comum e do folclore (anão, elfo, gnomo, pequenino, meio-orc, dragão, masmorra, armadilha, fechadura, ladino) ou inventado aqui. O dragão daqui não segue o esquema de cores de lá: invente os tipos pelo lugar onde vivem ou pelo que sopram.

**As leis do motor, que a etapa não pode quebrar:**
- **O item decide.** Cada categoria (Comum, Incomum, Raro, Épico, Único, Lendário, Mítico, Primordial) vale 3 vezes a de baixo. Talento, dom e agora o POVO não podem valer mais que uma categoria de peça (o Grande Dom vale um grau de maestria e perde 94% para a arma uma acima: o povo tem de pesar menos ou igual).
- **Aprende-se fazendo:** a maestria sobe por blocos de prática (40, 160, 500, 1.500 nas armas), vezes o talento. Não há experiência por matar.
- **Vida única,** com herdeiro. Rivais nativos que morrem de vez. O mundo não gira em torno do personagem.
- **A luta para e pergunta** sempre que algo muda. Quem o jogador comanda nunca foge nem se rende pelo dado.
- **Todo número mora nas páginas `tabelas*.py`.** Nenhuma regra vale antes de passar no banco de provas. O que não bate fica falhando às claras.
- **Só o `estado.py` grava o mundo,** por eventos com efeitos tipados; os invariantes são conferidos. O tempo só anda pelo `ato.passa`, em blocos de 4 horas. O dado do mundo sai de `estado.sorte`; o dado do jogador, de `teste.rola`, declarado e rolado uma vez; o que o personagem não pode saber sai como "rolagem oculta".
- **A economia é frágil:** a prata não nasce nem some (o tesouro de uma masmorra ou de um dragão é prata que já existe no mundo, posta pelo gerador); a loja paga 40% pelas peças e 60% pelos bens, e não compra peça maldita; forjar para a loja não é mina. Todo caminho novo de renda (o tesouro, a fechadura, o furto) precisa de meta no banco que impeça a mina.
- **O que o jogador já decidiu e segue valendo:** a Lendária é difícil de propósito; a caça de começo fica como está; a magia é a da etapa da magia (capítulos 10 a 16); o conserto pago prende quem espera (um bloco por peça).
- **O save do jogador tem de seguir abrindo:** todo campo novo tem valor padrão para o save antigo. A etapa entra no `ensaio/` por um comando que só acrescenta (como o `vila_teste.py magia`).

## 3. O que cada projeto tem de cobrir (a sua parte está no seu pedido)

Para a sua parte:
- **As regras, com números:** tabelas que caberiam num `tabelas_*.py`, contas feitas, e medidas de rascunho contra a luta e o motor de hoje (rode o motor: monte lutas, conte, meça). Diga o que mediu e o que é chute.
- **O estado:** como fica guardado (campos da pessoa, do lugar, do item; eventos e efeitos novos; invariantes), sempre com valor padrão para o save antigo.
- **Os comandos e a mesa:** o que o Mestre roda, o que a `MESA.md` mostra, onde a luta para e pergunta, o que vai ao SÓ O MESTRE.
- **Uma cena jogada** na vila de teste, em comandos e números, de dois ou três parágrafos.
- **As metas do banco:** o que medir, com faixa e com o jeito de medir (robôs, quantas lutas, quantas vidas), incluindo as que impedem a mina e as que mostram que a pessoa comum (humana, sem nada) segue igual à de hoje.
- **A construção:** os arquivos novos e os que mudam, o que cada um expõe, e como repartir entre poucos construtores sem que dois mexam no mesmo arquivo. Diga onde a sua parte toca a parte do outro projetista.
- **O que fica de fora** desta etapa (simples onde der: o motor já tem mais de 16 mil linhas).
- **No máximo quatro perguntas ao jogador,** cada uma com opções e a sua recomendação. Só o que é gosto dele; o que é conta, decida você.

Honestidade: o que você não sabe, o que pode quebrar o equilíbrio, e o que mediu de verdade.
