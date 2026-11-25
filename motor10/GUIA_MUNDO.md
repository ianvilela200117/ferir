# GUIA DO MUNDO NOVO (o Motor 10 inteiro)

O mundo de verdade mora em `motor10/mundo/` (gerado por `gera.py mundo semente=5`). A regra: `REGRAS.md`, capítulos 1 a 27. Este guia é a cola do Mestre.

## Abrir a sessão
De dentro de `motor10/` (o mundo novo é o padrão; não precisa de `MOTOR10_MUNDO`):
1. `cat mundo/RETOMAR.md` (o que houve, as PERGUNTAS ABERTAS, o SÓ O MESTRE) — no começo, ainda não há: a MESA é a da criação.
2. `python3 turno.py responde "1a.2b"` (os códigos do jogador) e `python3 turno.py abre` (a `mundo/MESA.md`: tudo o que é preciso para narrar).
3. Jogar pelos comandos abaixo; todo dado sai de script e rola uma vez.
4. Fechar: duas perguntas (`turno.py pergunta "..." "a=..." "b=..."`), `python3 turno.py fecha "o que houve" git` (guarda e envia).

## A criação (o começo)
- `python3 cria.py ofertas` · `python3 cria.py perguntas` (já estão abertas no mundo novo).
- O jogador responde "1a.2c.3e.4r" (povo, berço, inclinação, segunda inclinação do humano) e diz o nome.
- `python3 turno.py responde "1a.2c.3e.4r"` e `python3 cria.py nasce "1a.2c.3e.4r" nome=NOME`; depois `turno.py abre`.
- Em vida: `python3 cria.py herdeiro PID`. Morto o personagem: `python3 cria.py herda` (ou, sem herdeiro, `cria.py ofertas` de novo).

## A cada turno
- A MESA mostra: você (corpo, ficha, peças), aqui (quem está, o mercado, a oficina, a magia), as ESTRADAS daqui, o que a gente lembra de você, as NOTÍCIAS chegadas,
  a CAIXA (pedidos com prazo), o QUADRO de missões e as suas, as FRENTES que você conhece, o RANKING; e no SÓ O MESTRE, a pauta do diretor e dois fatos de fora.
- Viajar: `viagem.py ir DESTINO [com=ID,ID]`; no encontro, `pagar`, `atacar` (e `luta "Nome: ordem"`), `fugir`; `segue`, `volta`, `acampa N`.
- A caixa: pedido vencendo amanhã vira pergunta (`caixa.py pergunta XID`); a resposta do jogador, `caixa.py responde XID LETRA`. O `fecha` recusa sem isso.
- Missões: `missoes.py ver`, `toma MID`, `entrega MID`, `larga MID`.
- Frentes: `frentes.py ver`, `investigar FID`; SÓ O MESTRE: `frentes.py mestre`.
- Gente: `gente.py ver PID`, `quem`, `lembra PID "fato" PESO` (o Mestre põe na memória o que a cena fez).
- Rivais: `rivais.py ranking`, `ver PID`, `leilao`, `lance ITEM PRATA`; SÓ O MESTRE: `rivais.py mestre`.
- O resto é o de sempre: `ato.py` (comer, dormir, trabalhar, treinar, vestir, luta), `mercado.py`, `oficio.py`, `caca.py`, `masmorra.py`, `magia_mundo.py`, `alquimia.py`...

## O que o Mestre lembra
- O mundo anda sozinho a cada dia que vira (os rivais, as frentes, as notícias, a gente): o personagem só sabe o que chegou aonde ele está.
- O que a cena inventa entra por evento do Mestre (`estado.py mestre '[...]' "o que houve"`), com os mesmos verbos.
- A semente que reprova no banco do ano não vira save; o mundo de verdade é a semente 5.
