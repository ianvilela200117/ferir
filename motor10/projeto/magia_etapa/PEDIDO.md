# Motor 10: o pedido de projeto da ETAPA DA MAGIA E DOS DONS

Este trabalho é FORA do jogo de Ferir. O CLAUDE.md do repositório fala daquele jogo: as regras dele (abrir sessão, ler MESTRE.md, rodar scripts da raiz) NÃO valem aqui. Aqui você é projetista de um motor de RPG novo, em Python (só a biblioteca padrão), todo em português, em `/home/user/ferir/motor10/`.

## 0. As regras de trabalho

1. NÃO EDITE NADA em `/home/user/ferir`. Outro agente está consertando o motor agora: leia, mas não escreva. NUNCA rode script da raiz do repositório. Não use git para mudar nada.
2. Pode rodar os scripts de `motor10/` para MEDIR (com `PYTHONDONTWRITEBYTECODE=1`, de dentro de `motor10/`, e com `MOTOR10_MUNDO` numa pasta sua de rascunho). Não toque em `motor10/ensaio/` (é o save do jogador). Os arquivos de `motor10/` podem mudar enquanto você lê (o conserto em andamento): se um comando der erro de sintaxe, espere um pouco e tente de novo.
3. O que você escreve vai para a SUA pasta de rascunho (o caminho está no seu pedido).
4. Português simples e direto, sem jargão e sem travessão. Quem lê no fim é o jogador.

## 1. O que ler antes

- `motor10/LEIA.md`, `motor10/PROJETO.md` (o plano inteiro e as decisões do jogador, seções 12 e 13), `motor10/REGRAS.md` (o livro em vigor: leia inteiro; os capítulos 1 a 3 são a pessoa, os itens e a luta), o fim do `motor10/MUDANCAS.md`.
- `motor10/projeto/magia.md`: o rascunho antigo da magia. Foi escrito para a primeira versão da luta e não cobre poção, maldição, tradição nem talento. É ponto de partida, não contrato.
- O código que a magia vai tocar: `tabelas.py`, `pessoas.py`, `itens.py`, `luta.py` (a luta roda turno a turno, para e pergunta; os bichos já têm traços como veneno, sopro e apavora), `estado.py` (o único gravador: efeitos tipados, invariantes), `corpo.py`, `ato.py`, `oficio.py` e `tabelas_oficio.py` (a forja: o molde para a alquimia e o encanto), `mercado.py`, `caca.py` e `tabelas_caca.py` (a erva já se colhe), `bichos.py` e `tabelas_bichos.py`, `turno.py`, `vila_teste.py`, e os bancos de provas (`provas.py`, `provas_mundo.py` e os três dos módulos).

## 2. O que o jogador decidiu (não se discute; projeta-se em cima)

**Sobre a magia (palavras dele):** "a magia é algo extremamente importante nesse mundo e tem para todo lado: poções, maldições e magias mesmo, de ataque e defesa."
1. **Qualquer um aprende magia,** como se aprende uma arma. Mas "eu quero que os DONS E TALENTOS digam se vai aprender mais rápido ou mais devagar ou vai ser mais poderoso, assim como qualquer coisa: como ferreiro, guerreiro, clérigo, druida, mago e outros."
   - Ou seja: dons e talentos são um sistema da PESSOA, que vale para TODO caminho (arma, ofício, magia), não só para a magia.
   - E ele pensa em caminhos de magia diferentes: o mago, o clérigo, o druida "e outros".
2. **A Mana volta devagar durante a luta** (não só com descanso).
3. **A maldição pode durar dias e até matar,** se ninguém a quebrar.
4. **Magia contra aço:** o jogador ainda NÃO respondeu. A proposta do orquestrador, que vale até ele dizer outra coisa: a mesma conta do aço. O foco (varinha, cajado, símbolo) é a arma de quem lança e tem categoria; quem tem o foco melhor vence, como com a espada. Mantém a regra-mãe do motor.

**As leis do motor, que a magia não pode quebrar:**
- **O item decide.** Cada categoria (Comum, Incomum, Raro, Épico, Único, Lendário, Mítico, Primordial) vale 3 vezes a de baixo. Uma arma duas categorias acima dá a um nível 50 cerca de 63% contra um nível 500. Não há requisito de nível para usar peça; há requisito por atributo e o sob medida.
- **A conquista é difícil.** O raro é contado no mundo. A Lendária é difícil de propósito (uma tentativa são 70 dias de bancada, e o melhor ferreiro acerta 1 em 4).
- **O mundo é duro e não gira em torno do personagem.** Vida única, com herdeiro. Rivais nativos que morrem de vez.
- **A luta para e pergunta** sempre que algo muda. Quem o jogador comanda nunca foge nem se rende pelo dado.
- **Todo número mora nas páginas `tabelas*.py`.** Nenhuma regra vale antes de passar no banco de provas. O que não bate fica falhando às claras.
- **Só o `estado.py` grava o mundo,** por eventos com efeitos tipados; os invariantes são conferidos. O tempo só anda pelo `ato.passa`. O dado do mundo sai de `estado.sorte`; o dado do jogador, de `teste.rola`, declarado e rolado uma vez.
- **A economia fechou há pouco e é frágil:** a prata não nasce nem some; a loja paga 40% pelas peças e 60% pelos bens; forjar para a loja não é mina; o coletor e o caçador de começo vivem no limite (1 a 2 diárias). Poção, ingrediente e serviço de magia NÃO podem virar mina nova: todo caminho de renda novo precisa de meta no banco.

## 3. O que o projeto tem de cobrir

**A. Os dons e os talentos** (para todo caminho: armas, ofícios, e cada tradição de magia).
- O que é um talento e o que é um dom; quantos graus; quão raros; como nascem (o dado do mundo, para toda gente gerada; e o personagem do jogador); se a pessoa sabe o que tem ou descobre fazendo.
- O que mudam, em números: a pressa de aprender (os blocos de cada grau de maestria, que hoje são 40, 160, 500 e 1.500 nas armas), o teto (até onde a mão sobe) e o poder (o que soma na conta).
- Como convivem com a lei "o item decide": talento não pode valer mais que uma categoria de peça.
- O que isso faz com as metas que já existem (a escada do ofício, o treino das armas): o banco de hoje tem de seguir passando para a pessoa de talento comum.

**B. A magia na luta** (ataque, defesa, controle, cura), por cima da luta que existe.
- A conta (acerto, dano, defesa contra magia), o foco e o amuleto como itens com categoria, a Mana (com a volta devagar na luta), o tempo de lançar, o que interrompe, o que acontece quando dá errado.
- As tradições: pelo menos o mago, o clérigo e o druida; diga o que cada uma tem de seu (de onde vem o poder, o que faz melhor, o que não faz, o que custa) e se cabe uma quarta (bruxaria, alquimia de guerra, canto). Uma tradição não pode ser só "a mesma lista com outro nome".
- A lista de partida de feitiços, com números.
- Os bichos com magia (o que os traços de hoje já fazem e o que falta: resistência, firmeza).
- Como a luta "para e pergunta" com magia em campo.

**C. As poções e a alquimia.** Um ofício novo, no molde da forja (obra, teste, falhar custa, maestria por blocos). Ingredientes que já existem no mundo (erva, osso, couro, núcleo) e os que faltam. O que cada poção faz, por categoria; quanto dura; quantas se bebem; o veneno de lâmina; o antídoto. Preço, e a meta que impede a mina.

**D. As maldições.** O que são, de onde vêm (feitiço, bicho, lugar, peça amaldiçoada, juramento quebrado), o que fazem por dia, como pioram, como matam, e como se quebram (clérigo, poção, cumprir a condição). Como ficam guardadas no estado e como a MESA as mostra.

**E. A peça encantada.** Como um feitiço entra numa peça, o que pede, o que rende na luta, e como fica dentro da lei "o item decide" e da sintonia que já existe.

**F. A magia em todo lado.** O que muda na vila de teste (quem lança, o que há na prateleira, que bicho usa magia), o que a gente comum sabe, o que a loja vende, o que a curandeira faz. E os ganchos para as etapas seguintes (a região, os rivais, as frentes).

**G. O banco de provas da etapa:** as metas, com faixa e com o jeito de medir (robôs, quantas lutas, quantas vidas). Diga quais você já mediu em rascunho e quais são chute.

**H. Como construir:** a ordem, os arquivos novos e os que mudam, o que cada um expõe, e como repartir entre construtores sem que dois mexam no mesmo arquivo.

**I. O que é do jogador decidir:** no máximo seis perguntas, cada uma com opções e a sua recomendação.

## 4. O que se espera de um bom projeto

- Números, não só ideias: tabelas que caberiam num `tabelas_magia.py`, contas feitas, e pelo menos algumas medidas de rascunho contra a luta de hoje (por exemplo: quanto um feitiço de dano tira num igual; o mago contra o guerreiro; quanto a Mana dura).
- Coisas que se jogam: para cada parte, uma cena de exemplo de dois ou três parágrafos, em comandos e números, na vila de teste.
- Simples onde der: o motor já tem 10 mil linhas. Diga o que você deixaria de fora desta etapa.
- Honestidade: o que você não sabe, o que pode quebrar o equilíbrio, e o que mediu de verdade.

---

## 5. ACRÉSCIMO DO JOGADOR (chegou depois de os três projetistas começarem)

O jogador disse, depois: **"não esquece das criaturas mágicas, orcs, goblins, entre outros que tem em RPG como Dungeons and Dragons. Chefes mágicos, entre outros."**

Isto é parte da etapa: **J. As criaturas e os povos monstruosos.**
- Hoje o motor só tem BICHOS (14 espécies, do grau F ao S: `bichos.py`, `tabelas_bichos.py`, REGRAS capítulo 6): o corpo é a arma e a armadura, com categoria; traços que a luta roda; o chefe dá núcleo.
- Falta: os POVOS que usam arma, armadura e magia (goblins, orcs, ogros, e outros), os MORTOS que andam, os seres de magia (elementais, espíritos, golens), e os CHEFES MÁGICOS (o xamã, o necromante, o dragão que lança, o rei morto), com o que cada um faz na luta, onde vive, o que carrega e o que larga.
- Só criatura do folclore e da fantasia comum (goblin, orc, ogro, troll, esqueleto, fantasma, vampiro, lobisomem, harpia, minotauro, gigante, elemental, golem, quimera, bruxa, demônio, dragão...) ou inventada aqui. NADA que seja criação exclusiva de um jogo ou livro específico: nem o nome, nem a aparência.

**Dois projetistas a mais estão escrevendo só esta parte,** em:
- `/tmp/claude-0/-home-user-ferir/2caa978a-1aa4-5b05-88b7-11bcda935cb0/scratchpad/magia/criaturas_luta/PROJETO.md` (o bestiário e a luta: fichas, traços, a magia dos monstros, os chefes mágicos, medidos contra a luta de hoje)
- `/tmp/claude-0/-home-user-ferir/2caa978a-1aa4-5b05-88b7-11bcda935cb0/scratchpad/magia/criaturas_mundo/PROJETO.md` (os povos no mundo: onde vivem, como se organizam, o que carregam, o que o despojo faz com a economia, e os ganchos para masmorras e frentes)

**Para os três projetistas da magia:** se você ainda não entregou, não precisa projetar o bestiário; basta que a sua conta de magia sirva também para um monstro que lança (o xamã, o chefe mágico) e para a resistência dos monstros à magia.
**Para os juízes:** não tire nota de um projeto por não trazer as criaturas (o pedido chegou depois). Se os dois arquivos acima já existirem quando você ler, leia-os e diga, no seu juízo, o que deles o contrato tem de ter e o que está errado.
**Para o sintetizador:** o contrato TEM de ter a parte J (as criaturas, os povos e os chefes mágicos), com um construtor dono dela. Leia os dois arquivos acima inteiros. Se algum não existir ainda, espere alguns minutos e olhe de novo (até três vezes); se não vier, escreva a parte J você mesmo, mais curta, e diga isso em `riscos`.
