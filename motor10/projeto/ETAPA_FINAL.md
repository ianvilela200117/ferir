# ETAPA FINAL (as etapas 3, 5, 6 e 7): o contrato curto

O que falta do `PROJETO.md` até o Dia 1 do mundo novo: a região que responde (3), a corrida (5), o medo (6) e a história com a criação do personagem (7).
Este contrato é o que vale, letra por letra, onde diz um NOME, um CAMPO, a FORMA de um efeito ou a ASSINATURA de uma função. As escolhas feitas onde o
plano deixava em aberto estão em `etapa_final/DECISOES.md`, para o jogador rever.

**O fim desta obra:** `motor10/mundo/` gerado por uma semente que passa o banco do ano, sem personagem, com as perguntas da criação abertas
(`turno.py abre` mostra a MESA da criação; `cria.py nasce ...` faz o personagem). Daí em diante joga-se pelo turno de sempre.

## 0. O que não pode quebrar
- Os bancos de hoje: `provas.py 600` (114 de 114), `provas_mundo.py` (225 de 225), `estresse.py 1500` (sem erro). A vila de teste e o `ensaio/` abrem e jogam como antes:
  **todo campo novo tem padrão**, e o save antigo (sem `mundo.json`) abre com o mundo vazio.
- Um gravador só (`estado.aplica`); evento sem efeito é recusado; cada fato num lugar só; nada novo cria prata fora do evento `gera`/`mestre`
  (a prata de quem morre segue a regra da morte; a paga de missão sai da bolsa de quem paga; o leilão e o torneio só mudam prata de mão).
- Nomes de gente e de lugar saem do gerador do motor (`nomes.py`); nada de nome, lugar ou criação exclusiva de livro ou jogo.
- O personagem continua o único que não descansa de graça; o mundo anda com ele ou sem ele (`regiao.anda`).

## 1. O estado: o arquivo novo e o verbo novo
O save ganha **`mundo.json`** (`E['mundo']`), um dicionário de SEÇÕES. Ausente: `{}` (o save antigo). `estado.ARQS` passa a ter `'mundo'`.

| Seção | Forma | O que é |
| --- | --- | --- |
| `meta` | `{nome, ano0, anos, reino, semente_historia, vistos: {...}}` | a região, o ano do Dia 1, quantos anos de história; `vistos` (o que a janela já anunciou) |
| `casas` | `{CID: {nome, sede, tipo: nobre\|comum, fundada, viva, ramo: [...], lema}}` | as casas e famílias (a gente aponta a casa em `pessoa.casa`) |
| `reinos` | `{RID: {nome, fundado, caiu, casa}}` | o reino de hoje e os que caíram |
| `cronica` | lista de `{ano, texto, onde, tags}` | a história (só o gerador escreve; o Mestre lê, a gente conta pedaços) |
| `frentes` | `{FID: {nome, tipo, dono, onde, meta, passo 0..6, forca, resiste, passos: [6 textos], efeitos: [6 listas], fim: null\|'desfecho'\|'barrada', desde, ult, molde}}` | as frentes |
| `guildas` | `{GID: {nome, sede, lider, fama}}` | as guildas (os membros apontam `pessoa.guilda`) |
| `missoes` | `{MID: {de, onde, tipo, alvo, n, paga, prazo, frente, estado: aberta\|tomada\|cumprida\|falhou\|venceu, quem, desde, base}}` | o quadro de missões |
| `caixa` | `{XID: {de, pede, prazo, opcoes: {letra: texto}, efeitos: {letra: [efeitos]}, padrao: letra, motivo, desde, fim: null\|letra}}` | a caixa de entrada do personagem |
| `noticias` | `{NID: {dia, onde, texto, peso, tags, chegou: {LUGAR: [dia, saltos]}}}` | o que aconteceu, andando pelas estradas |
| `ranking` | `{semana, lista: [[pid, pontos]], lider, trocas}` | o ranking da semana |
| `janela` | lista de `{dia, texto}` | o que o mundo inteiro fica sabendo na hora |
| `oculto` | `{CHAVE: dia}` | o que o personagem já descobriu investigando (`frente.FID.passo`, `frente.FID.dono`...) |
| `leilao`, `torneio` | registros livres do módulo `rivais` | o próximo leilão e o próximo torneio |
| `seq` | `{tipo: n}` | os contadores dos ids |

**O verbo `mundo`** (o gravador confere a forma de cada seção; as ligações são do `valida`):
```
['mundo', SECAO, ID, 'poe', registro ou None]           põe ou tira um registro (seções de dicionário)
['mundo', SECAO, ID, 'CAMPO[.SUB]', 'poe'|'soma', valor]  muda um campo de um registro (soma só em número)
['mundo', SECAO, 'junta', valor]                         junta à lista (cronica, janela)
['mundo', 'meta', 'CAMPO[.SUB]', 'poe', valor]            a meta
['mundo', 'seq', TIPO, 'soma', 1]                         o contador
```
`casas`, `reinos`, `cronica` e `meta.ano0`/`anos` só em evento `gera` ou `mestre`.

## 2. A estrada (o lugar `tipo: "estrada"`)
As 24 estradas são lugares: `{nome, tipo: 'estrada', ponta: [A, B], longe: blocos 1..6, perigo: 1..3, bando: inteiro, passa: ERMO ou null, fechada: null ou {por, dia}}`.
A estrada **não tem `vizinhos`, `bichos`, `teto` nem `coleta`** (a caça nunca a lista); as pontas são lugares de povo que existem, e cada par tem no máximo uma estrada.
O estoque dela é o chão (o que cai na estrada fica nela). `regiao.estradas(E, lid)` dá as estradas de um lugar; `regiao.vizinhos(E, lid)`, os lugares do outro lado.
**Quem viaja está FORA:** `marca.viagem = {estrada, de, para, feitos, longe, com: [ids], fase: 'anda'|'encontro'|'luta', encontro, luta}` (em quem vai junto: `{de: QUEM}`).
`estado.fora` dá a estrada; `presente` recusa os atos da vila; a morte na estrada deixa tudo nela. Viagem, saída de caça e descida nunca juntas.

## 3. A pessoa: os campos novos (todos com padrão)
| Campo | Padrão | Verbo | Eventos |
| --- | --- | --- | --- |
| `casa` | nenhuma | `poe` CID | gera, mestre, heranca |
| `pais` | `[]` | `poe` [pid] | gera, mestre |
| `lacos.PID` | nenhum | `poe` tipo (`pai`, `mãe`, `filho`, `irmão`, `cônjuge`, `aprendiz`, `mestre`, `jurado`, `amigo`, `rival`, `inimigo`) ou None | todos |
| `memoria` | `[]` | `junta` `{dia, de, o_que, peso -5..5}` (guarda 12: sai o de menor peso, o mais velho) · `poe` [] | todos |
| `fama` | 0 | `soma` | todos |
| `querer` | nenhum | `poe` `{o_que, alvo, ate}` ou None | todos |
| `papel` | nenhum | `poe` texto (`tabelas_regiao.PAPEIS`) | gera, mestre |
| `guilda` | nenhuma | `poe` GID ou None | todos |
| `rival` | não | `poe` True/None (o aventureiro nativo) | gera, mestre |
| `herdeiro` | nenhum | `poe` PID ou None (só o personagem) | herdeiro, mestre |
| `jogador` | — | `poe` True/None: só em `heranca` (o herdeiro assume quando o personagem morreu) | heranca |
A opinião de A sobre B = a soma dos pesos das memórias de A com `de == B`, entre −10 e 10; os porquês são as três de maior peso (`gente.opiniao`).
A morte guarda também `morte.vestia` (os ids que estavam em uso), para o nêmesis.

## 4. Os eventos novos e os módulos
`EVENTOS` ganha: `viagem`, `noticia`, `caixa`, `missao`, `rival`, `frente`, `semana`, `herdeiro`, `heranca`, `leilao`, `torneio`, `regiao`, `querer`, `investigar`.
`MUNDO_SOZINHO` ganha: `noticia`, `rival`, `frente`, `semana`, `regiao`, `querer` (o mundo andando: vira notícia, não fato do turno; a morte sempre é fato).
`MODULOS` ganha, nesta ordem (é a ordem da virada): `regiao`, `gente`, `missoes`, `rivais`, `frentes`, `caixa`, `noticias`, `viagem`, `diretor`.

| Módulo | O que faz | Comandos |
| --- | --- | --- |
| `tabelas_regiao` | todos os números da região, da gente, dos rivais, das frentes, da história e da criação | — |
| `nomes` | os nomes de gente (por povo) e de lugar, pelo acaso do mundo | `nomes.py gente POVO N`, `nomes.py lugar N` |
| `historia` | gera de 400 a 1.000 anos (função pura da semente): reinos, casas, guerras, lendas, ruínas, as peças altas com a cadeia de donos, a crônica | `historia.py SEMENTE` (só mostra) |
| `gera` | o mundo inteiro por eventos `gera` numa pasta nova | `gera.py PASTA [semente=N]` |
| `regiao` | as estradas; a virada do povo em número (fome, migração, bando que engrossa); o comércio entre lugares; `anda(E, dias)` (o mundo sem o personagem) | `regiao.py ver`, `regiao.py mapa` |
| `viagem` | ir pela estrada; o encontro (bando ou bicho do ermo que ela passa); a luta e as contas | `viagem.py ver`, `ir DESTINO [com=]`, `atacar`, `pagar`, `fugir`, `luta "..."`, `segue`, `larga` |
| `gente` | a memória e a opinião; o querer semanal dos nomeados (vira ato com efeito); os laços | `gente.py ver PID`, `lembra PID "fato" PESO`, `quem LUGAR` |
| `noticias` | a notícia que nasce de um evento; anda uma estrada por dia; boato do 4º salto | `noticias.py ver` |
| `caixa` | os pedidos com prazo; o padrão com custo; 7 no máximo | `caixa.py ver`, `responde XID LETRA`, `pergunta XID` |
| `missoes` | o quadro; tomar, cumprir, falhar; a missão contra a frente tira um passo | `missoes.py ver`, `toma MID`, `entrega MID`, `confere` |
| `rivais` | os 40 aventureiros: o plano da semana, o dia, a conta rápida, a morte, a gente nova; o ranking; o torneio; o leilão; a janela | `rivais.py ranking`, `ver PID`, `leilao`, `lance LOTE N`, `torneio` |
| `frentes` | as 12 frentes e as que nascem por limiar; a rolagem da semana; o passo e o desfecho; a calamidade; o nêmesis; investigar | `frentes.py ver` (só o que se sabe), `mestre`, `investigar FID` |
| `diretor` | só LÊ: escolhe até 3 frentes para a cena do dia | `diretor.py pauta` |
| `cria` | as ofertas da criação; o personagem nasce numa casa, com parentes; o herdeiro; a herança | `cria.py ofertas`, `nasce povo= berco= inclinacao= [inclinacao2=] nome=`, `herdeiro PID`, `herda` |

## 5. A virada (um relógio só)
Por dia, na ordem de `MODULOS`: o mercado, o ofício, a caça, a magia, as criaturas, a masmorra, os dragões (como hoje); depois `regiao` (o povo come o que há,
a fome mata e expulsa, o bando engrossa perto da fome, o comércio leva o que sobra para onde falta, a frente de fome nasce do celeiro baixo), `gente` (no primeiro dia da
semana, o querer de cada nomeado; o querer vencido vira ato), `missoes` (as vencidas), `rivais` (o dia de cada um; na semana, o plano e o ranking; na estação, o leilão;
no ano, o torneio e a gente nova), `frentes` (na semana, a rolagem), `caixa` (o prazo vencido vale o padrão), `noticias` (um salto).
Tudo pelo acaso do mundo (`estado.sorte`): mesma semente, mesmo mundo. O dado do jogador é só o dele.
**O custo:** o povo é número (sem pessoa por cabeça); os nomeados e os rivais agem uma vez por semana e resolvem no dia marcado; o `aplica` copia só o que o evento mexe.

## 6. A história e o mundo gerado (as metas do gerador)
16 lugares de povo (1 capital de ~4.000, 2 cidades de ~1.500, 5 vilas de ~400, 8 aldeias e postos de ~120), 6 ermos, 8 masmorras (com origem na história),
24 estradas (o grafo é conexo), ~150 nomeados (com papel, casa, parentes, talento e dom), 40 rivais em 6 guildas e soltos (3 Lendas vivas), o raro contado
(~60 Raras, 12 Épicas, 4 Únicas, 3 Lendárias com as Lendas, 1 Mítica dormindo no covil da calamidade), 12 frentes (4 ameaças, 4 ambições, 2 faltas, 2 mistérios).
Toda peça Única ou maior tem a cadeia de donos na `historia` dela, ano a ano, até o dono de hoje; toda masmorra tem `origem`; ninguém vivo passa da idade do povo;
toda casa viva tem um herdeiro possível.

## 7. A criação (o fim desta obra)
`cria.py ofertas` (só lê) dá: os 6 povos; 6 BERÇOS tirados das famílias do mundo (o lugar, o ofício, o povo da família, o que se ganha, os parentes vivos, uma linha da
história); os 17 caminhos para a inclinação. As perguntas da criação ficam abertas no caderno do turno. `cria.py nasce` faz o personagem (o dado do mundo, uma vez):
nível 5, os atributos do berço mais o povo mais o dado, o talento e o dom com a inclinação, a idade, as peças e a prata do berço, a mão de Iniciante no ofício da família,
os laços com os parentes (e a memória deles), no lugar da família, no Dia 1.
O herdeiro: `cria.py herdeiro PID` (um parente, aprendiz ou jurado, vivo). Morto o personagem: `cria.py herda` passa o jogo ao herdeiro (a casa, as peças que o matador
não levou, a memória dos outros pela metade); o matador fica com o que o morto vestia e vira a frente `nêmesis`. Sem herdeiro, `cria.py ofertas` volta com berços novos.

## 8. O turno
A MESA ganha (só para quem tem a região): as estradas daqui (blocos, perigo que se sabe, fechada), quem está aqui com o que lembra de você, a caixa por prazo,
as notícias chegadas, o quadro de missões, a pauta do diretor e dois fatos que não tocam você. O `fecha` passa a recusar: pedido da caixa com prazo até amanhã
sem pergunta aberta ligada a ele; viagem torta; as invariantes novas.

## 9. Os bancos
`provas_regiao.py` (as peças: o gravador novo, a estrada e a viagem, a memória, a notícia, a caixa, a missão, os rivais e a conta rápida, as frentes, o diretor,
o herdeiro, a criação, o gerador e a história) e `provas_ano.py` (365 dias sem jogador em N sementes: as metas 1 a 10 e 5b da seção 9 do `PROJETO.md`).
Os dois entram no `provas_mundo.py`. As saídas ficam em `dados/`.
