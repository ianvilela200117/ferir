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
