# MOTOR 10 — o motor novo, para um MUNDO NOVO

Esta pasta NÃO faz parte do save do Ferir. Nada daqui vale para aquele jogo, e nenhum script daqui lê ou escreve os arquivos dele.
É o motor que o jogador mandou fazer depois da revisão do Dia 507 (`../REVISAO_MOTOR10.md`), para começar um mundo do zero.

Para trabalhar no Motor 10, ler nesta ordem:
1. `PROJETO.md`: o plano, as etapas e as decisões do jogador (o que já foi decidido está marcado).
2. `REGRAS.md`: o livro de regras (um só, por assunto).
3. `MUDANCAS.md`: o que mudou, quando e por quê.

Conferir que tudo segue de pé: `python3 provas.py 600` (a luta, os itens e os bichos), `python3 provas_mundo.py` (o mundo: as etapas 1 e 2) e `python3 estresse.py 1500`.
Para experimentar: `python3 vila_teste.py PASTA` cria a vila de teste, fora do cânone (o guia é o `GUIA_VILA.md`).
Os números moram nas páginas `tabelas*.py`. Só o `estado.py` grava o mundo. Os rascunhos de projeto ficam em `projeto/`.

## A vila de teste do jogador (`ensaio/`)

O jogador está jogando uma vila de teste, fora do cânone, para sentir a luta, a forja e o custo de viver, e mandar mudar o que quiser. O save é a pasta `ensaio/` (Maro, guerreiro, em Pedra Rasa).
Para retomar, de dentro de `motor10/`:
1. `export MOTOR10_MUNDO=ensaio`
2. ler `ensaio/RETOMAR.md` (o que houve e as PERGUNTAS ABERTAS: o jogador responde por código, "1a.2b");
3. `python3 turno.py responde "1a.2b"` e `python3 turno.py abre` (a `MESA.md` traz o que é preciso para narrar);
4. jogar pelos comandos do `GUIA_VILA.md`; todo dado sai de script e rola uma vez;
5. no fim: duas perguntas (`turno.py pergunta`), `turno.py fecha "o que houve"`, e commit e push.
O que o jogador mandar mudar no motor vira regra no `REGRAS.md`, com linha no `MUDANCAS.md`, e só vale depois de os bancos passarem.
