# GUIA DO MUNDO NOVO (o Motor 10 inteiro)

O mundo de verdade mora em `motor10/mundo/` (gerado por `gera.py mundo semente=5`). A regra: `REGRAS.md`, capítulos 1 a 30. Este guia é a cola do Mestre.

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
- Habilidades (REGRAS 29): `habilidade.py mao` (a linha do turno), `ver CHAVE`, `copia CHAVE de=PID chance` (a chance, sem rolar) e `copia CHAVE de=PID` (a tentativa), `ensina PID CHAVE`, `estuda ITEM`, `ferro PACIENTE`,
  `paciencia`, `tempera`; na luta, `luta "Nome: fazer roda em ALVO"` e as outras palavras de 29.4; SÓ O MESTRE: `licao CHAVE "como"`, e o estalo e a subida da gente nas notas do turno.
- A fala (REGRAS 30; a resposta 5a): o teste só no pedido que o jogador declara, em dois passos. `fala.py conta PID DEGRAU [jeito=] [caminho=]` mostra o degrau e a chance, sem rolar
  (vai à mesa, e o jogador decide: a pergunta do turno); `fala.py pede PID DEGRAU "o quê"` só rola o pedido que acabou de ser mostrado (no turno seguinte, depois do código dele,
  roda o `conta` de novo, que não rola nada, e o `pede`). O regateio, a caixa e a missão: `regateia|caixa|missao ... conta`, depois sem o `conta`. SÓ O MESTRE: `fala.py gente PID DEGRAU "o quê"`.
  O Mestre nunca rola fala pelo personagem sem a ordem dele; a conversa comum segue pela opinião e pela memória.

## O que o Mestre lembra
- O mundo anda sozinho a cada dia que vira (os rivais, as frentes, as notícias, a gente): o personagem só sabe o que chegou aonde ele está.
- O que a cena inventa entra por evento do Mestre (`estado.py mestre '[...]' "o que houve"`), com os mesmos verbos.
- A semente que reprova no banco do ano não vira save; o mundo de verdade é a semente 5.
