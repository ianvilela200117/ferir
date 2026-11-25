# MOTOR 10 — o motor novo, para um MUNDO NOVO

Esta pasta NÃO faz parte do save do Ferir. Nada daqui vale para aquele jogo, e nenhum script daqui lê ou escreve os arquivos dele.
É o motor que o jogador mandou fazer depois da revisão do Dia 507 (`../REVISAO_MOTOR10.md`), para começar um mundo do zero.

Para trabalhar no Motor 10, ler nesta ordem:
1. `PROJETO.md`: o plano, as etapas e as decisões do jogador (o que já foi decidido está marcado).
2. `REGRAS.md`: o livro de regras (um só, por assunto).
3. `MUDANCAS.md`: o que mudou, quando e por quê.

Conferir que tudo segue de pé: `python3 provas.py 600` (a luta, os itens, os bichos e a magia na luta; uns 5 minutos), `python3 provas_mundo.py` (o mundo: as etapas 1 e 2, a magia, as criaturas, a etapa 4b e a etapa final, com o ano em 20 sementes; uns 20 minutos; 248 de 248) e `python3 estresse.py 1500` (lutas ao acaso, com e sem magia). As saídas da última rodada ficam em `dados/`.
Para experimentar: `python3 vila_teste.py PASTA [povo=POVO] [inclinacao2=CAMINHO]` cria a vila de teste, fora do cânone (o guia é o `GUIA_VILA.md`); `python3 vila_teste.py magia PASTA` acrescenta a etapa da magia a uma vila que já existe, e `python3 vila_teste.py fantasia PASTA [inclinacao2=CAMINHO]` acrescenta a etapa 4b a uma vila que já tem a magia.
Os números moram nas páginas `tabelas*.py`. Só o `estado.py` grava o mundo. Os rascunhos de projeto ficam em `projeto/` (os contratos: `projeto/ETAPA_MAGIA.md` e `projeto/ETAPA_4B.md`).

## A etapa da magia (feita)

Os dons e os talentos (capítulo 10 do `REGRAS.md`), a magia na luta (11), a alquimia e o encanto (12), as maldições (13), a magia no mundo (14), as criaturas (15) e os covis e a vila de teste com a magia (16).
Os módulos novos: `talento.py`, `magia.py`, `magia_mundo.py`, `alquimia.py`, `maldicao.py`, `encanto.py`, `criaturas.py`; as páginas novas: `tabelas_talento.py`, `tabelas_magia.py`, `tabelas_magia_mundo.py`, `tabelas_criaturas.py`.
Os bancos novos (o `provas_mundo.py` roda os três): `provas_talento.py`, `provas_magia.py`, `provas_criaturas.py`; as metas da magia na luta estão no `provas.py` (`python3 provas.py 600 magia`).

## A etapa 4b (feita): as masmorras e o mundo de fantasia

As masmorras (capítulo 17 do `REGRAS.md`), o ladino (18), os povos do personagem (19) e os dragões (20). O juízo e as respostas do jogador (E1 a E4): `projeto/etapa4b/DECISOES.md`.
Os módulos novos: `masmorra.py`, `manha.py`, `povos.py`, `dragoes.py`; as páginas novas: `tabelas_masmorra.py`, `tabelas_manha.py`, `tabelas_povos.py`, `tabelas_dragoes.py`.
Os bancos novos (o `provas_mundo.py` roda os seis): `provas_4b.py` (o alicerce), `provas_masmorra.py`, `provas_manha.py`, `provas_povos.py`, `provas_dragoes.py` e `provas_fantasia.py` (a integração: o comando da vila, o povo do personagem, o covil pela masmorra, quem vê no escuro, a mina, o anão na pedra).

O verificador independente conferiu a 4b e achou 13 defeitos; o acerto os consertou, com prova no banco (`MUDANCAS.md`, "Etapa 4b, segunda volta").
**Depois dela, a etapa final** (as etapas 3, 5, 6 e 7: a região, a corrida, o medo, a história e a criação): ver abaixo.

## A vila de teste do jogador (`ensaio/`)

**O save do jogador já tem a etapa da magia** (posta no turno 5 com `vila_teste.py magia ensaio inclinacao=fio`: a inclinação do Maro, escolhida pelo jogador, é nas lâminas).
**A etapa 4b ainda não está no save:** entra com `python3 vila_teste.py fantasia ensaio [inclinacao2=manha]` (só por eventos; recusa rodar duas vezes; com a luta aberta, espera ela fechar). A segunda inclinação do Maro só pode ser a manha, o único caminho que ele ainda não rolou: é escolha do jogador.

O jogador está jogando uma vila de teste, fora do cânone, para sentir a luta, a forja e o custo de viver, e mandar mudar o que quiser. O save é a pasta `ensaio/` (Maro, guerreiro, em Pedra Rasa).
Para retomar, de dentro de `motor10/`:
1. `export MOTOR10_MUNDO=ensaio`
2. ler `ensaio/RETOMAR.md` (o que houve e as PERGUNTAS ABERTAS: o jogador responde por código, "1a.2b");
3. `python3 turno.py responde "1a.2b"` e `python3 turno.py abre` (a `MESA.md` traz o que é preciso para narrar);
4. jogar pelos comandos do `GUIA_VILA.md`; todo dado sai de script e rola uma vez;
5. no fim: duas perguntas (`turno.py pergunta`), `turno.py fecha "o que houve"`, e commit e push.
O que o jogador mandar mudar no motor vira regra no `REGRAS.md`, com linha no `MUDANCAS.md`, e só vale depois de os bancos passarem.

## A etapa final (feita): a região que responde, a corrida, o medo, a história e a criação do personagem

As estradas e a viagem, a gente com memória e o querer da semana, a notícia, a caixa, as missões (capítulos 21 a 23 do `REGRAS.md`); os 40 rivais, a conta rápida, o ranking,
o torneio e o leilão (24); as frentes, a calamidade, o herdeiro e o nêmesis, o diretor (25); a história de 400 a 1.000 anos e o mundo gerado (26); a criação do personagem dentro
de uma casa (27). O contrato: `projeto/ETAPA_FINAL.md`; as escolhas para o jogador rever: `projeto/etapa_final/DECISOES.md`.
Os módulos novos: `tabelas_regiao`, `nomes`, `historia`, `gera`, `regiao`, `viagem`, `gente`, `noticias`, `caixa`, `missoes`, `frentes`, `rivais`, `conta`, `diretor`, `cria`;
os bancos: `provas_regiao.py` (as peças) e `provas_ano.py` (o ano em 20 sementes e os robôs), os dois no `provas_mundo.py`.

## O MUNDO NOVO (o jogo de verdade): `mundo/`

**O mundo está pronto e o personagem ainda não nasceu.** É a semente 5 (a primeira que passou em todas as faixas do banco do ano). O guia do Mestre: `GUIA_MUNDO.md`.
Para começar, de dentro de `motor10/` (o mundo novo é o padrão: sem `MOTOR10_MUNDO`):
1. `python3 turno.py abre` mostra a MESA da criação: os povos, os seis berços (famílias do mundo) e os caminhos; as perguntas já estão abertas.
2. O jogador responde por código ("1a.2c.3e.4r") e diz o nome: `python3 turno.py responde "..."` e `python3 cria.py nasce "..." nome=NOME`.
3. Daí em diante, o turno de sempre (`GUIA_MUNDO.md`), e no fim de cada turno: `python3 turno.py fecha "o que houve" git`.
