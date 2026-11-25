# ETAPA 3 (a região que responde): o contrato curto (o vocabulário comum)

A língua que as quatro frentes da onda 2 (A1, o mapa e o comércio; A2, a viagem; B1, a gente; B2, a caixa, a missão e a notícia) falam igual. Acima dele: a ordem de serviço (`etapa3/ORDEM.md`), o juízo e as respostas R1 a R4 do jogador (`etapa3/DECISOES.md`) e os dois projetos (`etapa3/projeto_a/PROJETO.md`, `projeto_b/PROJETO.md`: as regras e os números). Onde este contrato diz um NOME, um CAMPO, a FORMA de um efeito ou a ASSINATURA de uma função, vale o que está aqui, letra por letra.
O que está marcado **[pronto]** o alicerce (onda 1) já construiu: roda e passa nos bancos (o do alicerce é o `provas_3.py`). Os seis módulos novos existem como esqueleto neutro (seção 12). Cada frente enche o seu.

## 0. O que está congelado na onda 2

Ninguém edita: `estado.py`, `ato.py`, `turno.py`, `corpo.py`, `teste.py`, `tabelas.py`, `tabelas_mundo.py`, `tabelas_talento.py`, `talento.py`, `luta.py`, `pessoas.py`, `itens.py`, `bichos.py`, `criaturas.py`, `masmorra.py`, `magia.py`, `magia_mundo.py`, `alquimia.py`, `encanto.py`, `maldicao.py`, `povos.py`, `dragoes.py`, `rapida.py`, `fixtura3.py`, `vila_teste.py`, `provas.py`, `provas_mundo.py`, `provas_3.py` e os bancos de antes (`provas_*.py` que não são de uma frente). Falta algo neles: vai em `projeto/etapa3/pedidos_SUAFRENTE.md` (o arquivo e o que falta), e o integrador faz na onda 3.
Cada frente possui: **A1** `regiao.py`, `tabelas_regiao.py`, `provas_regiao.py`, `mercado.py`; **A2** `viagem.py`, `tabelas_viagem.py`, `provas_viagem.py`, `caca.py`; **B1** `gente.py`, `tabelas_gente.py`, `provas_gente.py`, `manha.py`; **B2** `caixa.py`, `missoes.py`, `noticias.py`, `tabelas_caixa.py`, `provas_caixa.py`, `oficio.py`. E o rascunho do capítulo dela: `projeto/regras_regiao.md` (21), `regras_viagem.md` (22), `regras_gente.md` (23), `regras_caixa.md` (24).
Ninguém edita `REGRAS.md`, `MUDANCAS.md`, `PROJETO.md`, `LEIA.md`, `GUIA_VILA.md`, `dados/` nem `ensaio/` (o save do jogador: nem rodar comando com `MOTOR10_MUNDO` apontando para ele; copie-o).

**As armadilhas de sempre (leia):**
- **Nada novo cria prata, e agora o gravador confere:** fora de evento `gera` ou `mestre`, o evento que muda a soma da prata do mundo é RECUSADO, com a conta (seção 3). A prata só muda de mão, no mesmo evento: o que sai de um entra noutro.
- **A vila de teste de hoje não muda quando ninguém tem a região:** num save sem `rotas.json`, sem bolsa e sem ninguém de papel, o seu módulo não faz nada (o banco K2 compara a vila de teste com e sem os seis módulos, byte a byte, e a MESA). Gancho novo não põe linha para quem não tem nada de novo.
- **O dado do mundo sai de `estado.sorte(E, chave)`; o do jogador, de `teste.rola`** (rolado uma vez; o que o personagem não pode saber, como "rolagem oculta").
- **Quem lê o registro inteiro lê por `estado.eventos(E, desde)`**, nunca o `eventos.jsonl` direto: a estação que acaba vai comprimida para `eventos/` (seção 2).
- **Todo número mora numa página `tabelas*.py`.** O vocabulário (os nomes que o gravador confere) mora no `tabelas_mundo.py`; os números de cada frente, na página dela, com as mesmas chaves.
- O `provas.py 600` (114 de 114), o `provas_mundo.py` (225 de 225) e o `estresse.py 1500` (0 erros) seguem passando sem mexer em faixa.

## 1. O gravador por toque [pronto]

`estado.aplica(E, tipo, efeitos, onde, quem, texto)` é a mesma porta, com a mesma forma e as mesmas recusas. O que mudou por dentro: **o ensaio copia só o que os efeitos nomeiam** (`estado._toca`): a pessoa, o lugar, o item, a obra, a rota, a notícia, o pedido, a missão; o resto do ensaio são os mesmos objetos do estado, que nenhum efeito muda. A morte (`['pessoa', ID, 'estado', 'poe', 'morto']`) e o efeito torto copiam tudo, como antes.
- **Consequência para quem escreve código:** nunca mude o estado à mão (o `E['gente'][x][...] = ...` fora do `estado.py`): com o gravador por toque, a mudança à mão pode ficar no estado (antes, ela se perdia no próximo evento). O efeito é a única porta.
- `MOTOR10_GRAVADOR=inteiro` roda o gravador de antes (a cópia inteira); `MOTOR10_GRAVADOR=confere` roda os dois em cada evento e quebra o programa (`AssertionError`) no primeiro evento em que o estado, o evento ou a recusa diferem. **Use o `confere` no seu banco, uma vez, antes de entregar.**
- **Medido:** um ano da vila de teste com a magia e a 4b, o personagem na rotina (5.524 eventos): de 6,7 a 8,6 s com o gravador de antes, 0,8 s com o por toque, o mesmo estado e o mesmo registro, byte a byte. `provas.py 600` e `provas_mundo.py` inteiros com `confere`: nenhum evento diferente.
- Verbo novo de uma frente não existe: o verbo é do alicerce (seção 4). O `estado._toca` conhece todos os verbos desta seção.

## 2. Os arquivos do save e o registro [pronto]

`estado.ARQS = ('relogio', 'lugares', 'gente', 'itens', 'turno', 'rotas', 'noticias', 'caixa', 'missoes')`. Os quatro novos têm padrão (`estado.PADRAO`): `rotas = {}` · `noticias = {seq: 0, ativas: {}}` · `caixa = {seq: 0, abertos: {}}` · `missoes = {seq: 0, itens: {}}`. O save que não os tem abre com o padrão (`estado.carrega`, `estado.padroes(E)`) e o `grava` só os escreve quando deixam de ser o padrão (ou se o arquivo já existe). O estado montado à mão ganha o padrão no primeiro `aplica`.
**O registro:** o `eventos.jsonl` é a ESTAÇÃO ABERTA. Quando o `grava` escreve o primeiro evento de uma estação nova, o arquivo aberto vai comprimido (gzip) para `eventos/ANO_ESTACAO.jsonl.gz` (`estado.arq_estacao(ano, est)`: `eventos/1_primavera.jsonl.gz`, `1_verao`, `1_outono`, `1_inverno`, `2_primavera`...), e começa outro.
- `estado.eventos(E=None, desde=0)` → a lista dos eventos de id maior que `desde`, em ordem: das estações que acabaram (só abre as que ainda podem ter evento depois de `desde`), da aberta e, com `E`, os que ainda não foram gravados (`E['_novos']`). É a função única de quem lê o histórico.
- `estado.prata_do_mundo(E)` → as moedas da gente + o caixa (`estoque.prata`) e a `bolsa` dos lugares + a `guarda` das missões.

## 3. A conta da prata em cada evento [pronto]

Fora de evento `gera` ou `mestre`, o gravador soma, nas entradas que o evento tocou, o que mudou na prata (as moedas, o `estoque.prata`, a `bolsa`, a `guarda`) e **recusa o evento cuja soma não é zero**: `evento "X" recusado, nada mudou. A prata não nasce nem some fora de evento "gera" ou "mestre": este evento faria nascer N de prata (Nome +N, ...). A prata só muda de mão: ...`. A morte (as moedas vão ao estoque do lugar) soma zero. **Medido nos bancos de hoje: nenhum ato fazia prata nascer ou sumir** (o banco inteiro roda com a conta ligada).

## 4. Os verbos novos, com a forma exata [pronto]

```
['rota', 'nasce', RID, {a, b, blocos, tipo, ermo, expoe, nome, falta, aberta}]     só em gera ou mestre
['rota', RID, 'falta', 'poe', {bem: n}] · ['rota', RID, 'falta.BEM', 'soma'|'poe', n] · ['rota', RID, 'aberta', 'poe', True|False]      em qualquer evento
['rota', RID, 'blocos'|'tipo'|'ermo'|'expoe'|'nome', 'poe', v]      só em gera ou mestre (as pontas a e b nunca mudam: outra rota nasce)
['pessoa', PID, 'papel', 'poe', PAPEL | None]                          só em gera ou mestre
['pessoa', PID, 'memoria', 'junta', [dia, tipo, peso, de_quem, canal, texto]]   o 13º faz esquecer o de menor |peso de hoje| (o mais velho, no empate), no próprio verbo
['pessoa', PID, 'memoria', 'esquece', I] · ['pessoa', PID, 'memoria', 'retribui', [dia, tipo]]   (retribui guarda [dia, tipo] em marca.retribui; o fato tem de estar lá)
['pessoa', PID, 'querer', 'poe', {t, desde, ...} | None]
['pessoa', PID, 'mora', 'poe', LUGAR | None] · ['pessoa', PID, 'mapa', 'poe', {lugares: [...], rotas: [...]} | None] · ['pessoa', PID, 'mapa', 'junta', {lugares, rotas}]
['pessoa', PID, 'marca.viagem', 'poe', {...} | None] · 'marca.preso' {ate: BLOCO} · 'marca.preco' fator · 'marca.retribui' [[dia, tipo], ...]
['lacos', A, B, 'soma'|'poe', n]       o laço de gente, na ficha de A (cada lado o seu); inteiro de −10 a 10 (a soma pára no teto; zero tira o laço); até 6.
                                       NÃO É o ['pessoa', PID, 'laco', 'poe', {ermo, dia}] da magia (o druida com o ermo), que segue como está.
['fama', PID, LUGAR, EIXO, 'soma', n]  soma à fama de hoje (já esfriada) e grava o dia; de 0 a 100
['noticia', 'nasce', {tipo, texto, onde, sobre, quem, eixo, fama, peso, alcance, dia, em}]     o gravador dá o id (n0001); sem "em", nasce em {onde: [dia, 0]}
['noticia', NID, 'chega', LUGAR, SALTOS]      grava em[LUGAR] = [hoje, SALTOS] (se já chegou lá, nada muda) · ['noticia', NID, 'some']
['caixa', 'abre', {de, para, molde, pede, prazo, opcoes, padrao, custo, motivo}]     o gravador dá o id (c0001), "aberto" (o bloco de agora) e "dia"; "para" é o personagem se não se diz
['caixa', CID, 'fecha', 'feito'|'vencido'|'forcado']                                    o pedido sai de "abertos" (o registro de eventos guarda tudo)
['missao', 'abre', {de, onde, tipo, grau, alvo, paga, caucao, prazo, guarda, ...}]   o gravador dá o id (ms0001); nasce "aberta", sem "quem"
['missao', MID, CAMPO, 'poe', v]       CAMPO de MISSAO_MUDA (quem, estado aberta|pega, prazo, caucao, paga, alvo, item, feito, nota); o resto (de, onde, tipo, grau...) só em gera ou mestre
['missao', MID, 'guarda', 'soma', n]   a guarda é prata: inteiro de zero para cima, e só muda de mão no mesmo evento
['missao', MID, 'fecha', 'cumprida'|'falhada'|'vencida'|'largada']   grava o estado e "fechada" (o dia) · ['missao', MID, 'some']   só a fechada e sem guarda
['lugar', LID, 'bolsa'|'safra'|'pos'|'bando'|'vigia'|'tipo', 'poe'|'soma', v]       os campos novos do lugar, pelo verbo de sempre (a faixa no gravador)
['item', 'nasce', {tipo: 'animal', qual, leva, come, cat, nome, dur, dono|onde}] · ['item', 'nasce', {tipo: 'carro', leva, so_estrada, cat, nome, dur, dono|onde}]
```
O id que o gravador vai dar (para o mesmo evento apontar para a entrada): `estado.proximo_id(E, 'noticias'|'caixa'|'missoes')`. **O `soma` só soma número:** para mexer dentro de um registro, ponha o registro inteiro (`poe`).

## 5. Os campos novos e as funções de leitura [pronto]

Todo campo tem padrão: o save antigo abre sem eles.

| Onde | Campo | Forma | Padrão |
| --- | --- | --- | --- |
| rota (`rotas.json`) | `a`, `b` | dois lugares que existem, diferentes; nenhuma outra rota com as mesmas pontas | |
| | `blocos` · `tipo` · `ermo` · `expoe` | 1 a 6 (`ROTA_BLOCOS`) · um de `ROTAS` (estrada, caminho, trilha, fora) · um lugar ermo, ou None · de 0 a 1 (1 cruza, 0,3 passa perto) | ermo None, expoe 1 |
| | `nome` · `falta` · `aberta` | texto ou None · {bem: n ≥ 0} (o que o carreto deixou ontem) · sim ou não | None, {}, sim |
| lugar | `tipo` | um de `TIPOS_LUGAR` (vila, ermo, masmorra, sala, capital, cidade, aldeia, fronteira) | o de hoje |
| | `bolsa` · `safra` · `pos` · `bando` · `vigia` | prata do povo, inteiro ≥ 0 · de 0,3 a 1,5 (`SAFRA`) · [x, y] de 0 a 100 · inteiro de 0 a 50, só em ermo · [dias] | sem bolsa (o preço usa só o caixa) · 1 · nada · 0 · nada |
| pessoa | `papel` | um de `PAPEIS` (ou de `tabelas_gente.PAPEIS`, se B1 acrescentar) | sem papel: não é gente da região |
| | `mora` | um lugar (a casa: a cama, a jornada, a rotina) | o `lugar` (`estado.mora(p)`) |
| | `mapa` | {lugares: [ids], rotas: [ids]} (o que o personagem conhece: R4 a) | nada |
| | `memoria` | até 12 fatos `[dia, tipo, peso, de_quem, canal, texto]`: tipo de `FATOS` (ou `tabelas_gente.FATOS`), peso de −10 a 10, de_quem uma pessoa que existe (viva ou morta), canal de `CANAIS` (viu, ouviu, boato) | [] |
| | `querer` | {t: um de `QUERERES` (ou `tabelas_gente.QUERERES`), desde: dia, ...} | nada |
| | `lacos` · `fama` | {pessoa: −10 a 10, sem zero}, até 6 · {lugar: {eixo de `FAMA_EIXOS` (oficio, feito, crime): [pontos 0 a 100, dia]}} | {} · {} |
| | `marca.viagem` | em quem comanda: `{rota, origem, destino, feito, blocos, com, fase, ...}` (origem e destino são as pontas da rota; feito de 0 a blocos; fase de `VIAGEM_FASES`: estrada, encontro, luta, acampa, parada; com a fase luta, `luta`: o arquivo). Em quem vai junto: `{de: QUEM_COMANDA}` e mais nada. O resto dos campos é de A2 | nada |
| | `marca.preso` · `marca.preco` · `marca.retribui` | {ate: o bloco (estado.agora) em que acaba} · de 0,6 a 1,5 (`PRECO_FAIXA`) · [[dia, tipo]] | nada · 1 · nada |
| notícia (`noticias.json` ativas) | `id, tipo, texto, onde, sobre, quem, eixo, fama, peso, alcance, dia, em` | em = {lugar: [dia, saltos]}: saltos ≤ alcance; dia − dia da notícia ≥ saltos | |
| pedido (`caixa.json` abertos) | `id, de, para, molde, pede, prazo, aberto, dia, opcoes, padrao, custo, motivo` | opcoes {letra: texto} (2 ou mais); padrao uma delas; prazo > aberto (blocos de `estado.agora`); de e para vivos; motivo = {tipo: um de `MOTIVOS`, id} que existe ({tipo: 'memoria', id: PESSOA, fato: [dia, tipo]}: o fato está na memória dela); até 7 por pessoa (`CAIXA_MAX`) | |
| missão (`missoes.json` itens) | `id, de, onde, tipo, grau, alvo, paga, caucao, prazo, quem, estado, guarda, dia, fechada` | tipo de `MISSOES`; grau de `GRAUS` (F, E, D, C, B, A, S); paga, caução e guarda inteiros ≥ 0; quem vivo ou a missão fechada; a fechada não guarda prata | |
| item | tipo `animal` · tipo `carro` | qual de `ANIMAIS` (mula, boi), leva > 0, come ≥ 0 · leva > 0, so_estrada sim ou não; nenhum dos dois gasta (dur [1, 1]) | |

**Ler sempre por estas funções:** `estado.viagem(E, pid)` (o registro de quem comanda, ou None) · `estado.quem_viaja(E, pid)` · `estado.fora(E, pid)` (quem viaja: o `ermo` da rota; sem ermo, a ponta mais perto: a origem até a metade, depois o destino) · `estado.preso(E, pid)` (o bloco até quando, ou None) · `estado.mora(p)` · `estado.peso_hoje(fato, dia)` (o fato esfria: `ESFRIA` = até 3, perde 1 a cada 28 dias; até 7, a cada 56; de 8 para cima, nunca) · `estado.fama_hoje(p, lugar, eixo, dia)` (esfria 1 a cada `FAMA_ESFRIA` = 28 dias) · `estado.na_cena(E)` (quem está em cena: seção 10) · `estado.proximo_id(E, arq)` · `estado.prata_do_mundo(E)` · `estado.eventos(E, desde)`.

## 6. O que o gravador faz sozinho [pronto]

- **Quem viaja está FORA** (como quem saiu para o ermo ou desceu): os atos da vila são recusados (`presente`: "está na estrada (a viagem está aberta)"), ninguém descansa em casa na estrada (`em_cena`), o bloco passado nela marca `marca.ermo_dia` (não é dia de repouso), e **quem morre na estrada fica no `fora` dele, com tudo** (a carga e a prata no estoque do ermo). Quem ia junto e morre sai da viagem; a de quem comanda e morre fica escrita, para A2 fazer as contas (o `valida` acusa "morreu com a viagem aberta" até `viagem.py larga`).
- **Quem está PRESO** (`marca.preso` com `ate` adiante) está no lugar dele e não age: o `presente` recusa ("está preso em X até o Dia N, bloco"). Passado o bloco, age (B1 tira a marca na virada).
- **Uma saída, uma descida e uma viagem nunca juntas** (a marca de uma recusa as outras).
- O `relogio` vai sempre copiado; o `turno` não é tocado por efeito nenhum.

## 7. Os invariantes novos (`estado.valida`; o `fecha` recusa com qualquer um quebrado) [pronto]

A rota: as pontas existem e são diferentes; os blocos de 1 a 6; o tipo da lista; o ermo existe e é ermo; nenhuma outra rota com as mesmas pontas; a falta e o aberta na forma. O lugar: o tipo da lista; a bolsa inteira ≥ 0; a colheita na faixa; a posição no quadro; o bando inteiro de 0 a 50, só em ermo; o lugar `fronteira` (o mundo de fora) não tem gente. A pessoa: o papel, a memória (até 12, os fatos na forma), o querer, os laços, a fama, o mora e o mapa na forma; no máximo uma de saída, descida e viagem; a viagem de quem comanda por uma rota que existe, entre as pontas dela; quem foi junto aponta quem comanda, com ele no `com`; o morto não comanda viagem aberta; o preso, o preço e o retribui na forma. A notícia: os lugares existem; os saltos não passam do alcance; nenhuma chega a k saltos antes do dia k. A caixa: até 7 por pessoa; quem pede e quem recebe vivos; o motivo existe; o padrão é uma das opções; o prazo depois da abertura. A missão: quem pede existe; a guarda ≥ 0; quem pegou está vivo, ou a missão fechou; a fechada não guarda prata; a peça que ela aponta (`item`, da encomenda) existe enquanto ela está aberta.

## 8. Os eventos e os módulos [pronto]

`tabelas_mundo.EVENTOS` ganhou `viagem` (um bloco de estrada, a chegada, o acampamento), `regiao` (o dia da região, a semana, a estação, o ano), `frete`, `mercado` (o dia do mercado de um lugar num evento só: a produção e o consumo, no lugar de `producao` e `consumo`), `gente` (a semana: a bolsa, o desgaste, o querer), `noticia`, `caixa`, `missao`, `encomenda`, `furto`, `companhia`. Em `MUNDO_SOZINHO` (não são fato do turno, a não ser que alguém morra): `regiao`, `mercado`, `gente`, `noticia`. **O mundo sozinho de um dia é um evento por módulo por dia** (o juízo): o dia do mercado de todos os lugares, o dia da região, a semana da gente, o dia das notícias.
`MODULOS` (a ordem em que a virada os chama): `mercado, regiao, viagem, oficio, caca, talento, magia, magia_mundo, alquimia, encanto, maldicao, criaturas, masmorra, manha, povos, dragoes, gente, missoes, caixa, noticias` (a notícia por último: anda com o que nasceu no dia). Os ganchos de sempre: `virada(E)`, `bloco(E, pid, esforco, dorme)`, `vestiu`, `pode_vestir`, `voce(E)`, `mesa(E)`, `so_mestre(E)`, `retomar(E)`, `recusa_fecha(E)`. **Os novos:**
- `negocia(E, quem, com_quem)` → `''` (negocia) ou a frase da recusa. O `estado.negocia(E, quem, com_quem)` chama os módulos e devolve a primeira recusa. **Chamado** no `mercado._vivo` (toda compra e venda na loja do lugar: `com_quem` é o id do lugar) e no `ato.comer` (a refeição do lugar, antes de cobrar: `com_quem` é o lugar). B1 decide quem atende (a taverneira, o mercador de papel do lugar).
- `companhia(E, quem, com, perigo, dias, paga=0)` → `(a frase da recusa ou '', os efeitos)`: os efeitos (a paga, de `quem` para os de `com`, e o que mais B1 quiser gravar) entram no evento que abre. O `estado.companhia(...)` chama os módulos (sem `com`, nem chama) e devolve a primeira recusa, ou `('', a soma dos efeitos)`. **Chamado** no `caca._abre` (perigo `{"ermo", "alvo"}`, dias 1; o comando ganhou `paga=N`), no `masmorra.descer` (perigo `{"masmorra"}`, dias 1; `paga=N`) e, quando A2 o fizer, no `viagem.ir` (perigo `{"rota"}`, os dias da viagem). Sem B1, vai quem foi chamado, sem paga (a regra de hoje).

## 9. A conta rápida provisória (`rapida.py`) [pronto]

Uma tabela só (`tabelas_mundo.RAPIDA`), para quem não é o personagem e não está em cena: pela diferença **teto − grau** (de −2 para baixo, a linha −2; de 1 para cima, a 1): `cumpre` e `morre_falha` (a missão, projeto B: 90%, 65%, 25%, 5%; morre em 15% das falhas acima do teto) e `vence` e `morre` (o encontro na estrada, pelas lutas medidas pelo projeto A; com companhia, a morte vezes `RAPIDA_COMPANHIA` = 0,5). `RAPIDA_DIAS` (2 a 5) e `RAPIDA_GASTA` (3 pontos nas peças). A etapa 5 troca a tabela; os nomes das funções ficam.
- `rapida.teto(E, pid)` → 0 (F) a 6 (S): (a mão na arma em uso ÷ 2 + 3 × a categoria da arma + a categoria da armadura) ÷ 2, para baixo. **É o único teto:** `gente.teto` devolve este.
- `rapida.grau(letra_ou_n)` · `rapida.letra(n)` · `rapida.linha(dif)`.
- `rapida.missao(E, pid, grau, chave)` → `{cumpre, morre, dias, gasta, linha}` · `rapida.encontro(E, pid, grau, chave, com=0)` → `{vence, morre, linha}`. O dado é `estado.sorte(E, 'rapida|...|PID|CHAVE')`: quem chama dá uma chave única por caso. Não grava nada.

## 10. A MESA [pronto]

- **O orçamento** (`tabelas_mundo.MESA_TETO`, em KB de 1.000 letras do arquivo; `MESA_TOTAL` = 8): você 1,0 · aqui 0,8 · rotas ("Daqui se vai a") 0,6 · viagem 0,7 · gente ("Quem está aqui") 1,0 · caixa 0,8 · quadro ("O quadro", "O que se diz de você", "Dois fatos que não tocam você", "O que se conta") 0,7 · mercado 0,8 · oficios ("A oficina", "A caça", "Os bichos", "A magia", "A botica") 0,8 · perguntas 0,5 · mestre 1,0. A seção conta na parte pelo começo do título (`MESA_SECOES`): **dê às suas seções títulos que comecem como na lista.** `turno.orcamento(txt)` → `[(parte, KB, teto)]` + o total; `turno.avisos(txt)` → as linhas das que passam; o `turno.py abre` as imprime depois da MESA. A MESA do `ensaio/` hoje: 14,0 KB (era 16,4; o corte do SÓ O MESTRE), com o mercado (4,5), a oficina, a caça e a magia (4,2) e o "Aqui" (2,0) acima do teto: são os cortes das frentes (A1 o mercado em seis linhas; A2 a caça numa linha; B1 o "Quem está aqui" no lugar da lista do "Aqui"; B2 a oficina) e do integrador (a magia e a botica).
- **A ordem:** as seções dos módulos da etapa 3 vêm primeiro (`MESA_ORDEM`: regiao, viagem, gente, caixa, missoes, noticias), depois as de hoje, na ordem de `MODULOS`. **Com a viagem aberta**, o "Aqui" vira uma linha ("está na estrada, de X para Y") e só os módulos de `MESA_NA_ESTRADA` (viagem, gente, caixa, missoes, noticias) põem seção.
- **O SÓ O MESTRE só de quem está em cena:** `estado.na_cena(E)` = o personagem, quem vai junto com ele (a saída, a descida, a viagem) e quem esteve num ato deste turno (o `quem` dos eventos desde `turno.evento0`, fora o `gera` e o mundo sozinho) e está onde ele está. Os módulos de `MESA_SO_CENA` (talento, magia_mundo, manha) recebem no `so_mestre` uma vista do estado com só essa gente; o resto sai em **`talento.py mestre`** (sem id: o talento, o dom e a magia de todos os vivos). A gente de B1 usa `estado.na_cena` direto.
- **A caixa vira pergunta sozinha:** o pedido do personagem que vence em até `CAIXA_PERGUNTA` (6) blocos aparece em "Perguntas abertas" como "(da caixa, vence em um dia...)"; o `turno.fecha` o põe nas perguntas (a pergunta guarda `caixa: CID`, e o texto diz `caixa.py responde CID LETRA`). O `turno.responde` guarda o `caixa` na resposta e diz o comando; o `fecha` **recusa** o pedido respondido que segue aberto ("cumpra com `caixa.py responde CID LETRA`") e o que vence em um dia fora das perguntas.
- **A viagem aberta não impede o turno de fechar:** fica na pessoa (`marca.viagem`), o RETOMAR diz "(a viagem está aberta)" e o `viagem.retomar(E)` põe a linha dela; o `turno.py abre` a retoma.

## 11. A fixtura (`fixtura3.py`) [pronto]

`fixtura3.cria(semente=3)` → a vila de teste do ferreiro (a magia e a 4b) com a região pequena em volta, em memória; `fixtura3.poe(E)` põe a região num mundo que já tem a vila de teste (recusa a segunda vez); `python3 fixtura3.py PASTA [semente=N]` grava numa pasta nova. Os ids: povoados `telhal` (Telhal Alto, cidade, 1.500, oficina 2, runas 1, botica 1, santuário 1), `ribanceira` (Ribanceira, vila, 400, oficina 1, botica 1), `cerro` (Cerro Manso, aldeia, 120, sem cama nem prateleira); o ermo `charco` (o Charco do Cerro, brejo, a borda, vizinho de Cerro Manso); as rotas `r_vila_telhal` (estrada, 3 blocos, ermo mata, expõe 0,3), `r_vila_cerro` (caminho, 2, ermo charco, expõe 1), `r_telhal_ribanceira` (caminho, 4, campo aberto); a bolsa (5 por pessoa) em `vila` e nos três povoados; a gente de papel: `bento` (ferreiro), `dalva` (taverneiro), `tome` (guarda), e as novas `ilmara` (Ilmara Tojal, encantador, oficial, em Telhal Alto), `belmiro` (Belmiro Sarça, mercador, oficial, na Ribanceira), `odilia` (Odília Penedo, alcaide, aprendiz, em Cerro Manso), com `mora`. Ninguém tem memória, querer, laço nem fama: é a gente de B1 que os põe.

## 12. O que cada módulo novo expõe (os nomes que os outros chamam)

Tudo abaixo existe no esqueleto [pronto, neutro]; cada frente enche o seu sem mudar a assinatura nem a forma do que devolve. **Nenhuma grava sozinha, a não ser o `main` e as que dizem "aplica":** devolvem efeitos, e quem chama os põe no evento dele. O esqueleto que já lê o estado (os vizinhos, a distância, o que chegou, os abertos, o quadro) é leitura, não regra: a frente pode refinar, sem mudar a forma.

**`regiao.py` (A1)**
- `gera(E, semente, planta=None)` → efeitos (evento `gera`; o que é segredo, como o bando, vai ao SÓ O MESTRE pelo `turno.secreto`) · `virada(E)` (o dia da região: um evento `regiao` por dia; o de `mercado`, um por dia) · `mesa(E)` ("Daqui se vai a") · `so_mestre(E)`.
- `rotas_de(E, lid, abertas=True)` → `[(rid, rota)]` · `vizinhos(E, lid, abertas=True)` → `[(lugar, rid, blocos)]` (a rota fechada não leva ninguém nem notícia) · `rota_entre(E, a, b)` → rid ou None · `caminho(E, a, b, abertas=True, conhece=None)` → `(blocos, [lugares], [rotas])` ou None (`conhece`: só estas rotas, o mapa do personagem) · `distancia(E, a, b, abertas=True)` → blocos ou None.
- `guardas(E, lid)` → quantos do povo são guarda · `perigo(E, rid)` → `{"bicho", "bando", "patrulha", "palavra", "pior"}` (a chance por bloco; a palavra que o jogador lê: segura, fala-se de..., perigosa, só com escolta).

**`viagem.py` (A2)**
- `ir(E, pid, destino, por=None, com=(), noite=False, paga=0)` (aplica; o esqueleto recusa "ainda não") · `blocos_ate(E, a, b, estacao=None)` → blocos ou None (com o inverno) · `anda_npc(E, pid, destino)` → efeitos (a viagem do nomeado, pela `rapida.encontro`) · `carga(E, pid)` → `{"peso", "teto", "leva", "pesado"}`.
- `virada(E)` (a comida da carga que estraga, a viagem dos nomeados) · `mesa(E)` ("A viagem", só aberta) · `retomar(E)` · `so_mestre(E)` · `recusa_fecha(E)`.

**`gente.py` (B1)**
- `povoa(E, lugar, pessoas=None)` → efeitos (a porta da etapa 7: a gente pronta que a história der; o nomeado novo sai do povo, `['lugar', L, 'pop', 'soma', -1]`, com a parte dele da bolsa) · `povoa_regiao(E)` (aplica os seus eventos `gera` e devolve as linhas; o `vila_teste.py regiao` a chama).
- `ponto(E, pid, bloco=None)` → `(ponto, o que faz)` · `opiniao(E, quem, de=None)` → `(n de −10 a 10, a palavra, [os porquês])` · `lembra(E, quem, tipo, de=None, canal='viu', texto='', peso=None)` → efeitos · `tom(E, lugar, de=None)` → −3 a 2 · `fama(E, quem, lugar, eixo=None)` → número, ou {eixo: número} · `teto(E, pid)` (= `rapida.teto`).
- `vai_junto(E, quem, com_quem, perigo, dias)` → `{"vai", "paga", "diz"}` · os ganchos `companhia(E, quem, com, perigo, dias, paga=0)` e `negocia(E, quem, com_quem)` (seção 8) · `virada(E)` (um evento `gente` por dia) · `mesa(E)` ("Quem está aqui") · `so_mestre(E)`.

**`noticias.py` (B2)**: `nasce(E, tipo, texto, onde, sobre=None, quem=None, eixo=None, fama=0, peso=0, alcance=1)` → efeitos (no evento que causou a notícia) · `chegou(E, lugar, sobre=None)` → `[registro]`, as mais novas primeiro · `virada(E)` (anda uma rota por dia pelo `regiao.vizinhos`: um evento `noticia` por dia) · `mesa(E)` ("O que se diz de você", "Dois fatos que não tocam você") · `so_mestre(E)`.
**`caixa.py` (B2)**: `abertos(E, para=None)` → `[registro]` pelo prazo · `abre(E, de, molde, pede, opcoes, padrao, prazo_dias, motivo, custo='', para=None)` → efeitos (o oitavo força o mais velho antes, no mesmo evento) · `responde(E, cid, letra, **mais)` (aplica; o esqueleto recusa) · `virada(E)` (o vencido vale o padrão, com o custo) · `mesa(E)` ("A caixa") · `so_mestre(E)`. O comando que o turno liga: `caixa.py responde CID LETRA`.
**`missoes.py` (B2)**: `quadro(E, lugar)` → `[registro]` das abertas e pegas · `abre(E, de, onde, tipo, grau, alvo, paga, prazo, caucao=None)` → efeitos (a paga sai de quem pede no mesmo evento) · `pega(E, pid, mid)`, `cumpre(E, mid, pid=None)`, `entrega(E, mid, iid)`, `fecha(E, mid, desfecho)` (aplicam; o esqueleto recusa) · `virada(E)` (o nomeado que pega do quadro e cumpre pela `rapida.missao`) · `mesa(E)` ("O quadro") · `so_mestre(E)`.

**Quem chama quem:** a notícia anda pelo `regiao.vizinhos`; a missão dá o prazo pelo `viagem.blocos_ate`; a viagem pergunta quem vai junto pelo `estado.companhia`; a gente e a missão fora de cena resolvem pela `rapida`; o `vila_teste.py regiao PASTA [semente=N]` (integrador) chama `regiao.gera` e depois `gente.povoa_regiao`.

## 13. Os bancos

- O `provas_mundo.py` chama (o integrador acrescenta): `provas_3.py` (o alicerce) [pronto: 14 de 14], `provas_regiao.py` (A1), `provas_viagem.py` (A2), `provas_gente.py` (B1), `provas_caixa.py` (B2). **Cada banco novo expõe `provas(n)`**, que devolve a lista de `(nome, o que deu, passa)`, e roda sozinho com `python3 provas_X.py [N]`.
- Mundo de prova: `fixtura3.cria(semente)` (a região pequena), `provas_mundo.vila()` ou `estado.novo(semente)`, num `MOTOR10_MUNDO` de rascunho; nunca o `ensaio/`. O dado do jogador repetível: `provas_masmorra.dado_semente(n)` e `luta.semente(n)` (o `provas_3.dados(n)` faz os dois).
- Rode o seu banco uma vez com `MOTOR10_GRAVADOR=confere` (seção 1). Meta que não bate fica falhando às claras, com o número; afina-se o número de regra da sua parte, nunca a faixa.
