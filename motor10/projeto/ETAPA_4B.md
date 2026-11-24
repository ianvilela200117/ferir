# ETAPA 4b (as masmorras e o mundo de fantasia): o contrato curto (o vocabulário comum)

A língua que as quatro frentes da onda 2 (M, a masmorra; L, o ladino; P, os povos; D, os dragões) falam igual. Acima dele: a ordem de serviço, o `etapa4b/DECISOES.md` (o juízo e as respostas E1 a E4) e os dois projetos (`etapa4b/projeto_a/PROJETO.md`, `projeto_b/PROJETO.md`: os números). Onde este contrato diz um NOME, um CAMPO, a FORMA de um efeito ou a ASSINATURA de uma função, vale o que está aqui, letra por letra.
O que está marcado **[pronto]** o alicerce (onda 1) já construiu: roda e passa nos bancos (o do alicerce é o `provas_4b.py`). Os quatro módulos novos existem como esqueleto neutro (seção 12: o humano, sem manha, nenhum dragão, nenhuma masmorra). Cada frente enche o seu.

## 0. O que está congelado na onda 2

Ninguém edita: `estado.py`, `ato.py`, `turno.py`, `corpo.py`, `teste.py`, `tabelas.py`, `tabelas_mundo.py`, `tabelas_talento.py`, `talento.py`, `luta.py`, `pessoas.py`, `magia.py`, `itens.py`, `bichos.py`, `criaturas.py`, `caca.py`, `provas.py`, `provas_mundo.py`, `provas_4b.py`, `vila_teste.py`. Também não: `tabelas_bichos.py`, `provas_talento.py`, `provas_criaturas.py`, `provas_magia.py`, `provas_caca.py`. Falta algo neles: vai em `pedidos` (o arquivo e o que falta), e o integrador faz na onda 3.
Ninguém edita `REGRAS.md`, `MUDANCAS.md`, `PROJETO.md`, `LEIA.md`, `GUIA_VILA.md`, `dados/` nem `ensaio/` (o save do jogador: nem rodar comando com `MOTOR10_MUNDO` apontando para ele; copie-o).
Cada frente escreve o rascunho do capítulo dela em `projeto/regras_masmorra.md` (17), `regras_manha.md` (18), `regras_povos.md` (19), `regras_dragoes.md` (20).

**As armadilhas de sempre (leia):**
- O `provas.py` exige de 8 a 12 traços em `tabelas_bichos.TRACOS` e de 12 a 16 espécies em `tabelas_bichos.ESPECIES`. **Nada novo entra lá.** Os traços do povo moram em `tabelas.TRACOS_POVO` (seção 8); os dragões, em `tabelas_dragoes.ESPECIES`; o guardião da cripta, em `tabelas_criaturas.CHEFES`.
- O dom é ESCONDIDO até se mostrar: nenhuma conta que vai à mesa soma o dom que a pessoa ainda não viu (o `manha.testa` já cuida disso).
- **A pessoa comum (humana, sem manha, fora de masmorra, sem dragão) é a de hoje:** a luta de quem não tem traço do povo, manha de Treinado nem a fase `foge` é a de sempre, dado por dado (o banco compara com o motor de antes). A MESA de hoje sai igual: gancho novo não põe linha para quem não tem nada de novo.
- **Nada novo cria prata.** O tesouro é prata posta pelo gerador (evento `gera`); depois só muda de mão. Toda renda nova tem meta no banco.

## 1. A pessoa: os campos novos [pronto]

Todo campo tem valor padrão: o save antigo abre sem eles.

| Campo | Padrão | O que é | Verbo |
| --- | --- | --- | --- |
| `povo` | ausente = `humano` | o nome do povo (`tabelas_povos.POVOS`: `humano`, `anão`, `elfo`, `meio-orc`, `pequenino`, `gnomo`). Não se troca depois de nascer | `povo poe`, só em evento `gera` ou `mestre` |
| `idade` | ausente = não se sabe | os anos (inteiro). Nesta etapa só se escreve: não anda | `idade poe`, só em `gera` ou `mestre` |
| `inclinacao2` | ausente | a segunda inclinação do PERSONAGEM humano (E2 b): um caminho, diferente da `inclinacao`. Só vale para caminho ainda não rolado | `inclinacao2 poe`, só em `gera`, `mestre` ou `talento` |
| `maestria.manha`, `treino.manha` | Leigo, 0 | a manha é o 17º caminho, um ofício (`tabelas_mundo.OFICIOS`) | os verbos de sempre |
| `talento.manha`, `dom.manha` | Comum, sem dom | o talento e o dom no caminho da manha (seção 10) | os de sempre |

**As marcas novas** (o verbo `marca.X` de sempre, `poe`):
- `marca.masmorra` = **a descida aberta** (frente M). Em quem comanda: `{"masmorra": MID, "sala": SALA, "com": [ids], "ordem": [ids], "lances": N, "luz": {"tipo": "tocha" | "feitiço" | null, "quem": ID | null}, "fase": "anda" | "encontro" | "luta" | ..., "luta": ARQ | null, "caminho": [salas], ...}` (o resto é da frente M). Em quem vai junto: `{"de": QUEM_COMANDA}`. O gravador confere a masmorra, a sala dela, `com` (pessoas que existem), `lances` (inteiro de zero para cima), `fase` (texto) e, na fase `luta`, o arquivo `luta`.
- `marca.mapa` = `{MID: {...}}`: o que a pessoa viu de cada masmorra (frente M; o herdeiro não sabe o mapa do morto).
- `marca.feito_manha` = a maior categoria que a pessoa abriu ou desarmou de verdade (frente L).
- `marca.talento_novos` = a lista dos caminhos novos (`tabelas_talento.NOVOS`, hoje só `manha`) que a pessoa já rolou. Quem tem o talento rolado e não tem a manha nesta lista é gente de antes da etapa: falta-lhe rolar a manha (`talento.falta(p)`).

**Ler sempre por estas funções** [pronto]: `estado.povo(p)` (o nome; `humano` se ausente) · `estado.corpo_de(p)` (`gente` ou `miúdo`) · `estado.serve(it, p)` (a peça serve no corpo dela?) · `estado.descida(E, pid)` (o registro da descida dela, o de quem comanda, ou None) · `estado.quem_desce(E, pid)` (quem comanda, ou None).

## 2. O lugar: a masmorra, a sala, a gente e o dragão [pronto: o gravador confere a forma]

**A masmorra** é um lugar `tipo: "masmorra"`, vizinho de uma vila ou de um ermo (a vila a lista nos `vizinhos`; ela lista a vila), com `longe` (os blocos de caminho). **A masmorra não tem `bichos`, `teto` nem `coleta`** (senão a caça a listaria como ermo): quem mora está nas salas; quem vagueia, em `vagantes`.

| Campo da masmorra | Padrão | Forma |
| --- | --- | --- |
| `molde` | (não é masmorra) | um de `tabelas_mundo.MOLDES`: `cripta`, `mina`, `ruína`, `toca`, `covil` |
| `niveis` | | `[{"n": 1, "cat": 0, "salas": [ids]}, ...]`: n de 1 em diante, em ordem; `cat` de 0 a 7; cada sala da masmorra está em um nível só, o dela |
| `entrada` | | a sala onde se chega (do nível 1) |
| `portas` | `{}` | `{"SALA_A\|SALA_B": porta}`, as duas salas em ordem alfabética, de uma passagem que existe (ou de um segredo). porta = `{"estado": um de PORTAS, "material": um de PORTA_MATERIAL, "cat": 0 a 7, "fechadura": cat ou null, "miudos": true (só passa o corpo miúdo; opcional)}` |
| `alarme` | 0 | inteiro de 0 a `ALARME_MAX` (5) |
| `vagantes` | `{}` | `{espécie: quantos}`, inteiros de zero para cima, espécies que o gravador conhece |
| `limpa` | null | a primeira limpeza: `{"dia": N, "quem": [ids], "chefe": "nome"}` |
| `origem` | `""` | texto (o gerador da história, etapa 7) |

`tabelas_mundo`: `PORTAS = ('aberta', 'fechada', 'trancada', 'emperrada', 'arrombada')` · `PORTA_MATERIAL = ('madeira', 'ferro', 'pedra')` · `ALARME_MAX = 5` · `ARMADILHAS = ('dardo', 'lâmina', 'fosso', 'pedra', 'gás', 'runa', 'alarme')` (os números de cada uma moram no `tabelas_masmorra.ARMADILHAS`, com estas chaves) · `ATENTOS = (-1, 0, 1)`.

**A sala** é um lugar `tipo: "sala"`. Usa os campos que o lugar já tem: `vizinhos` (as salas ligadas por passagem; a passagem vale para os dois lados), `bichos` e `teto` (quem mora ali, contado; o `teto` só para quem cria), `estoque` (a prata e os bens dali), `coleta` e `coleta_teto` (a mina), `sobre` (a frase da mesa). E os novos:

| Campo da sala | Padrão | Forma |
| --- | --- | --- |
| `masmorra` | (não é sala) | o id da masmorra (que existe) |
| `nivel` | | o n do nível em que ela está |
| `largura` | ausente = aberta | inteiro de 1 para cima (1 corredor, 2 sala estreita), ou ausente/null |
| `acesa` | não | sim ou não (o fogo aceso: a luz é de todos) |
| `cat` | a da espécie | 0 a 7: a categoria de quem mora ali (a espécie de categoria maior fica na dela) |
| `atento` | 0 | −1 dormindo, 0 à toa, +1 alerta |
| `armadilhas` | `[]` | `[{"tipo": um de ARMADILHAS, "cat": 0 a 7, "onde": "chão" \| "guardado" \| "porta:SALA", "achada": dia ou null, "feita": null \| "desarmada" \| "disparada"}]`; `porta:SALA` aponta uma sala vizinha (ou de um segredo) |
| `guardado` | null | `{"nome": "o baú das oferendas", "fechadura": cat ou null, "aberto": sim ou não}` |
| `segredos` | `[]` | `[{"para": SALA, "cat": 0 a 7}]`: a passagem escondida; achada, sai daqui e entra nos `vizinhos` das duas salas |
| `chefe` | null | `{"qual": CHEFE, "vivo": sim ou não}`: CHEFE é um de `tabelas_criaturas.CHEFES`, ou uma espécie com `chefe` (bicho, criatura). **O dragão não vai aqui**: a sala do covil dele leva `dragao` (abaixo) |
| `do_morto` | ausente = nada | `{bem: quanto}` (o acerto): a parte do `estoque` que ficou junto do corpo de quem morreu na sala (a carga e a prata dele, que a regra da morte põe no estoque). Não é tesouro: o `pegar`, o "Dentro:" e o tesouro do dragão não a contam (`estado.livre`), e o estoque não desce abaixo dela sem o Mestre soltá-la no mesmo evento (`['lugar', SALA, 'do_morto.prata', 'soma', -N]` antes do `['estoque', ...]`) |

**O que a sala guarda (cada fato num lugar só):** a prata e os bens são o `estoque` dela (menos o `do_morto`, que é de um corpo: `estado.junto(E, SALA)`; o resto, `estado.livre(E, SALA)`, é o tesouro); as peças, as do Livro com `onde` nela. **Numa sala (e no covil), a peça sem dono e não solta está GUARDADA** (no baú, no tesouro: só quem abre ou fica com o campo a pega); a solta está no chão, de quem achar. Com um `guardado` fechado, o estoque e as peças guardadas estão dentro dele (o `guardado` não lista itens).

**A gente do lugar** (P): `povos` = `{povo: fração}`, ausente = toda humana; as frações de 0 a 1, somando até 1.
**O dragão** (D): `dragao` = o registro do dragão que mora no lugar (uma sala de covil, ou um ermo), ou ausente. `{"nome", "tipo": um de tabelas_dragoes.TIPOS, "idade": uma de tabelas_dragoes.IDADES, "pv": N (ausente: cheio), "dorme_ate": dia ou null, "punhados": N, "vila": LUGAR ou null, ...}` (o resto dos campos é da frente D: `prata_sono`, `tributo`, `ult_ataque`, `ataques`, `desde`, `feriu`). **Não guarda prata:** o tesouro é o estoque do lugar e as peças guardadas nele.

Tudo pelo verbo `lugar` de sempre: a forma no `poe` e no `nasce`; os invariantes (seção 7) no `valida`.
**Os campos que a frente M grava a mais** (o gravador já os aceita; registrados pelo integrador): no `chefe` da sala, `ergue` (`{SALA: {espécie: quantos}}`, os mortos que ele ergue de novo) e `ergueu` (o dia); no nível, `vazio` (o dia em que ficou sem quem mande); na masmorra, `sobre` (o que o povo diz dela); na descida (`marca.masmorra`), `caminho`, `anterior`, `blocos`, `treino`, `barulho`, `encontro`, `armadilha`, `casa`, `dia`.

## 3. O item e o bem [pronto]

`itens.item(tipo, cat, nome=None, ...)` monta o registro; `['item', 'nasce', registro]` grava.

| Tipo | Como se monta | O que é |
| --- | --- | --- |
| `gazua` | `itens.item('gazua', cat)` → "gazua Comum", durabilidade da categoria (Comum 10, Incomum 20...) | a ferramenta do ladino: não se veste; o teste usa a melhor inteira que a pessoa leva (`manha.gazua_de`). Vale pela matéria (`tabelas_mundo.MATERIA_GAZUA = dict(metal=1)`: o preço da adaga, Comum 10). Gasta (`dur soma`) e se conserta |
| `chave` | `itens.item('chave', 0, "a chave de ferro", abre="cripta_4\|cripta_5")` | abre sem teste a porta (`"SALA_A\|SALA_B"`, a chave das `portas`) ou o guardado de uma sala (`"SALA"`). 1/1, não gasta; preço 0: **a loja não compra nem vende chave** |

**A armadura é feita para um corpo, o `talhe`:** ausente = de gente; `"miúdo"` = do pequenino e do gnomo (`itens.item('armadura', 0, material='malha', talhe='miúdo')` → "armadura de malha miúda Comum"). Só a armadura (a arma e o escudo não). A que não serve não entra em uso. **Não confunda com o `corpo` de uma peça solta** (de quem era o morto junto de quem ela caiu: a regra da morte de hoje).
**O bem novo:** `tocha` (`tabelas_mundo.BENS`), na carga e no estoque. O preço e o consumo são do mercado (frente L).

## 4. O que o gravador faz sozinho [pronto]

- **Quem está numa descida está FORA:** `estado.fora(E, pid)` e `estado.onde` dão a sala do grupo (a de quem comanda). Logo: os atos da vila são recusados (`presente`, com a frase da descida), ninguém descansa em casa lá dentro, o bloco passado lá marca `marca.ermo_dia` (não é dia de repouso para a ferida), e a morte lá dentro deixa tudo na sala.
- **A morte na descida:** quem ia junto e morre sai dela. Quem comanda e morre **solta quem ia junto** (saem sozinhos: cena do Mestre); a descida do morto fica escrita para as contas, e o `valida` acusa "morreu com a descida aberta" até a frente M fechá-la (`sair`/`larga quem=ID`), como na caça.
- **Uma saída e uma descida não andam juntas:** pôr `marca.caca` em quem tem a descida aberta (ou o contrário) é recusado.
- **A luta da descida:** a nota `['pessoa', P, 'marca.masmorra', 'poe', {..., "fase": "luta", "luta": ARQ}]` entra com a luta aberta (como a da caça), e a frase da tranca diz `masmorra.py luta "Nome: ordem"` e `masmorra.py larga "por quê"`.
- **A armadura que não serve não entra em uso:** `['item', I, 'uso', 'poe', 'veste']` é recusado (a frase diz que um ferreiro a ajusta); mudar o `talhe` de uma peça em uso que deixaria de servir também.
- **O caminho novo de quem já nasceu:** o talento já rolado só se troca em evento `mestre`, a não ser que o efeito só ACRESCENTE os caminhos que faltam (`talento.falta`): esse entra em `gera` ou `talento` (é o `talento.rola_caminho`).

## 5. Os eventos novos [pronto]

`tabelas_mundo.EVENTOS` ganhou **`masmorra`** (os atos da descida: fato do turno), **`masmorra_vida`** (a vida da masmorra na virada: o alarme que cai, o morto que o chefe ergue, o bando de fora) e **`dragão`** (a vida do dragão); os dois últimos estão em `MUNDO_SOZINHO` (não são fato). O treino da manha em casa é o `treinar` de hoje; o furto (etapa 3) não entra agora.
**O SÓ O MESTRE** (`turno.secreto`): o evento `gera` ou `mestre` que faz nascer um lugar `masmorra` ou `sala`, ou que põe `dragao`, `armadilhas`, `segredos`, `guardado`, `portas`, `vagantes` ou `chefe` num lugar, vai ao SÓ O MESTRE do RETOMAR, e não aos fatos (o tesouro posto no mesmo evento vai junto). A manha rolada depois também (o `talento` é segredo desde a magia).

## 6. Os verbos novos do gravador, com a forma exata [pronto]

```
['pessoa', ID, 'povo', 'poe', POVO ou None]          só em gera ou mestre; None tira (volta a humano)
['pessoa', ID, 'idade', 'poe', ANOS ou None]         só em gera ou mestre; inteiro de zero até o máximo do povo
['pessoa', ID, 'inclinacao2', 'poe', CAMINHO ou None]   só em gera, mestre ou talento; só o personagem humano; outro caminho que não a inclinacao
['pessoa', 'nasce', ID, {..., "povo": POVO, "idade": N, "inclinacao2": CAMINHO}]
['pessoa', ID, 'marca.masmorra', 'poe', {...} ou None]   (em quem vai junto: {"de": QUEM})  ·  'marca.mapa' · 'marca.feito_manha' · 'marca.talento_novos'
['pessoa', ID, 'maestria.manha', 'poe', GRAU]  ·  ['pessoa', ID, 'treino.manha', 'soma', BLOCOS]
['pessoa', ID, 'talento', 'poe', {..., "manha": GRAU}]   já rolado: só em mestre, ou em gera/talento se só acrescenta o que falta
['pessoa', ID, 'carga.tocha', 'soma', N]  ·  ['estoque', LUGAR, 'tocha', 'soma', N]
['item', 'nasce', itens.item('gazua', CAT, dono=ID)]  ·  ['item', 'nasce', itens.item('chave', 0, NOME, abre=ALVO, onde=SALA)]
['item', IID, 'talhe', 'poe', 'miúdo' ou None]       só armadura (o corpo para que foi feita)
['lugar', 'nasce', MID, {"nome", "tipo": "masmorra", "molde", "niveis", "entrada", "portas", "alarme", "vagantes", "longe", "vizinhos": [VILA]}]     só em gera ou mestre
['lugar', 'nasce', SALA, {"nome", "tipo": "sala", "masmorra": MID, "nivel": N, "largura", "cat", "atento", "armadilhas", "guardado", "segredos", "chefe", "bichos", "teto", "estoque", "sobre"}]
['lugar', SALA, 'vizinhos', 'poe', [...]]  ·  ['lugar', SALA, 'bichos.esqueleto', 'soma', -2]  ·  ['lugar', SALA, 'atento' | 'armadilhas' | 'guardado' | 'segredos' | 'chefe', 'poe', ...]
['lugar', MID, 'portas.SALA_A|SALA_B', 'poe', {...}]  ·  ['lugar', MID, 'alarme', 'poe', N]  ·  ['lugar', MID, 'vagantes.corpo-seco', 'soma', -1]  ·  ['lugar', MID, 'limpa', 'poe', {...}]
['lugar', LUGAR, 'povos', 'poe', {povo: fração}]  ·  ['lugar', LUGAR, 'dragao', 'poe', {...} ou None]  ·  ['lugar', LUGAR, 'dragao.pv', 'poe', N]
['estoque', SALA, 'prata', 'soma', -30] com ['pessoa', P, 'moedas', 'soma', 8]       a prata muda de mão no mesmo evento
```
A sala é um lugar como os outros: a peça que cai (`onde`, `solto`), o achado e a contagem usam os verbos de sempre. **O `soma` só soma número:** para mexer dentro de um registro (a descida, o dragão), ponha o registro inteiro (`poe`), ou use `campo.sub`.
**A ordem dentro do evento que cria a masmorra:** o `nasce` confere a FORMA de cada campo e que os `vizinhos` já existem; nasça a masmorra e as salas primeiro e ponha os vizinhos depois, no mesmo evento (e a vila ganha a masmorra nos vizinhos dela). As LIGAÇÕES (a entrada, os níveis, as portas, a passagem dos dois lados, a chave) não se conferem no `aplica`: é o `estado.valida` que as confere (e o `fecha` recusa). Quem cria uma masmorra confere `estado.valida(E) == []` no banco dele.

## 7. Os invariantes novos (`estado.valida`; o `fecha` recusa com qualquer um quebrado) [pronto]

A pessoa: o povo da tabela; até a idade máxima dele; a `inclinacao2` como na seção 1; a armadura em uso serve no corpo; caça e descida nunca juntas; quem comanda está numa sala da masmorra dele; quem foi junto aponta quem comanda, vivo, com ele no `com`; o morto não tem descida aberta.
O item: a chave abre uma porta (das `portas` da masmorra das duas salas) ou um guardado que existem; o `talhe` só em armadura, e só `miúdo`.
O lugar: a masmorra tem molde, níveis em ordem com salas dela no nível certo, a entrada no nível 1, portas de passagens (ou segredos) que existem, e não tem bichos, teto nem coleta; a sala é de uma masmorra que existe e está no nível que diz; **os vizinhos de uma sala são salas da mesma masmorra, e a passagem vale para os dois lados; nenhum lugar que não é sala tem sala por vizinha** (a mesa da caça nunca lista uma sala); a armadilha da porta é de uma passagem dela; a do guardado pede guardado; o `do_morto` só em sala, e cada bem dele até o que o estoque tem; as frações de `povos` somam até 1; o `dragao` com tipo e idade da tabela, PV até o máximo (quando a espécie existe) e vila que existe; um nome de dragão mora num lugar só.
**A soma dos covis até 25% da prata do mundo é META (MI6), não invariante:** um mundo de prova pequeno passa disso.

## 8. Os traços do povo e a coragem (lista fechada nova) [pronto]

`tabelas.TRACOS_POVO = ('vê no escuro', 'resiste a veneno')`; a frase no `tabelas_povos.TRACOS`; os números no `tabelas_povos` (`ESCURO = 0.5`, `VENENO = 0.5`: a frente P afina; o nome do campo não muda). **Não ligam a luta de magia** (não estão no `TRACOS_NOVOS`).
- `vê no escuro`: no golpe o escuro tira dele só `ESCURO` do que tiraria (−2 em vez de −4); no tiro e no feitiço que voa, `ESCURO_TIRO` (1,0: pesa inteiro, −8). Medido pela frente P: com a metade também no tiro, o arqueiro que vê no escuro vencia o humano de 63 a 66% de noite, acima do Grande Dom (a meta PO1b).
- `resiste a veneno`: o veneno que entra nele (do bicho, da criatura, da lâmina) tira por rodada `VENENO` do que tiraria.
- a coragem (número): soma no teste de coragem (o pavor do dragão, o susto).
`estado.lutador(E, pid)` leva `tracos` e `coragem` do povo só para quem os tem; a ficha de gente os aceita e os mostra. **O nome do povo não vai ao lutador** (o `povo` do lutador é o corpo das criaturas). O corpo miúdo, na luta, é do tamanho de gente. **Fora da luta**, quem vê no escuro anda, procura, abre e desarma sem luz (frente M, por `povos.ve_no_escuro(p)`).

## 9. A luta: o golpe pelas costas, a fase `foge`, o despojo e o núcleo [pronto]

- **O golpe pelas costas (E1 a):** `tabelas.COSTAS = dict(desde=4, acerto=4, dados=3)`. Quem tem `maestria.manha` de Treinado ou mais (a ficha leva `manha`) dá, na primeira rodada, contra o lado surpreendido, o primeiro golpe de corpo a corpo da luta com +4 e os dados 3 vezes ("pelas costas"); não derruba. Vale quando o cenário diz `"surpresa": "B"` (é a frente M que monta).
- **A fase `foge` (E3 a):** a fase pode trazer `"foge": true` (e `"foge_diz"`; padrão "foge pelo ar, ferido"). No limiar, **se ele está no ar** (voa, e não está no chão, preso, agarrado nem num corredor) **e o lado dele tem saída** (sem `"lugar": {"sem_saida": LADO}`), sai da luta pelo ar, sem golpe livre, e a luta para e pergunta; senão, a fase vale como fúria (perde e ganha os traços dela). **No covil, quem monta a luta põe `sem_saida` do lado do dragão.** O que fugiu fica `"estado": "fugiu"`, com o PV que tinha. O dragão chefe vem com `"moral": "firme"` (não foge pelo susto: só a fase o tira).
- **O despojo pela categoria de quem morreu (o defeito do projeto A, consertado em toda parte):** `bichos.despojo(especie, sorte=None, cat=None)` e `criaturas.despojo(especie, sorte=None, cat=None)`: com `cat` (na luta, o `cat_corpo` do lutador), a matéria que está na categoria da espécie vai para a de quem morreu (até a Rara); a que a tabela põe noutra categoria anda junto, a mesma distância (de 0 à Rara); a mesma quantidade, os mesmos dados (`bichos.na_cat`). Sem `cat`, ou na categoria da espécie, é a tabela de hoje. A caça já passa a categoria de cada morto. **Quem conta um morto passa a categoria dele.**
- **O núcleo só do Épico para cima:** `tabelas_bichos.NUCLEO_DESDE = 3`, na categoria de quem morreu. Os chefes das criaturas não têm núcleo no despojo: o chefe do fundo do Épico para cima dá o dele pela conta da masmorra (`['item', 'nasce', itens.item('nucleo', CAT, ..., de=QUAL)]`).
- **Os dragões são bichos:** `estado.especie`, `bichos.especie`, `bichos.bicho`, `bichos.ameaca`, `bichos.despojo` e o atalho do cenário (`{"bicho": "dragão-da-serra-jovem", "nome": "o Tição", "pv": 350}`) leem `tabelas_dragoes.ESPECIES` (frente D).

## 10. Os talentos: o 17º caminho, a tendência e a segunda inclinação [pronto]

`tabelas_talento`: `OFICIOS` ganhou `manha` (17 caminhos); `NOVOS = ['manha']` e `ANTIGOS` (os 16 de antes); `DOM_NOME['manha'] = 'a mão leve'`; `TENDENCIA = 1`; `INCLINACAO` vale para as duas inclinações. A escada da manha é a das armas (`tabelas_mundo.MAESTRIA_BLOCOS`: 40, 160, 500, 1.500, vezes o talento).

| O que se chama | O que faz |
| --- | --- |
| `talento.falta(p)` | os caminhos novos que a pessoa já rolada ainda não rolou: `['manha']` para a gente de antes da etapa; `[]` para quem não foi rolado ou já rolou tudo |
| `talento.rola_caminho(E, pid, caminho='manha', inclinacao2=None)` | os efeitos que rolam SÓ esse caminho em quem já nasceu (os 16 não se rolam de novo; **o dom não muda**): o talento acrescido, a `marca.talento_novos`, a base dos blocos e, para o personagem humano, a `inclinacao2` (só no caminho que se rola agora). Evento `gera` ou `talento` |
| `talento.nasce(E, pid, registro, inclinacao=None, inclinacao2=None)` · `talento.rola(E, pid, inclinacao=None, inclinacao2=None)` | os de hoje, com a tendência do povo do registro (ou da pessoa) e a segunda inclinação; já põem `marca.talento_novos` |

**O dado de cada caminho** (a chave de sempre, `talento|PESSOA|CAMINHO`): cada inclinação ali soma um dado (vale o melhor); o caminho a favor do povo soma `TENDENCIA` dado (o melhor), o contra, `TENDENCIA` (o pior); os dois se anulam. **O humano nasce igual ao de hoje.** **O dom** sorteia-se entre os 16 de antes; uma segunda sorte (`dom|PESSOA|novos`) o passa à manha na proporção do peso dela (a chance de 17 caminhos; quem não caiu nela tem o dom de hoje).

## 11. Os ganchos e os módulos [pronto]

`tabelas_mundo.MODULOS` ganhou `masmorra`, `manha`, `povos`, `dragoes` (o que não existe fica de fora). Os ganchos de sempre: `virada(E)`, `bloco(E, pid, esforco, dorme)`, `vestiu(E, pid, iid)`, `voce(E)`, `mesa(E)`, `so_mestre(E)`, `retomar(E)`, `recusa_fecha(E)`. **O novo:** `pode_vestir(E, pid, iid)`, que o `ato.vestir` chama ANTES de montar o evento: `''` (pode) ou a frase da recusa. O `povos` já o tem: "A armadura de malha é de gente grande: não serve no corpo de Pipa. Um ferreiro a ajusta (`oficio.py ajustar ITEM para=ID`)."
**O ajuste recorta a peça:** o `oficio.py ajustar ITEM para=ID` que acerta grava o `talhe` da armadura no corpo de quem a pede (tirando-a de uso antes, se preciso). A forja de uma armadura miúda (a peça da obra com `talhe: 'miúdo'`) é da frente L, se quiser.
**A mesa:** a seção da masmorra só aparece com a descida aberta (`masmorra.mesa`); o "Aqui" e o RETOMAR já dizem "na descida" (e não "a saída está aberta").

## 12. O que cada módulo novo expõe (os nomes que os outros chamam)

Tudo abaixo existe no esqueleto [pronto, neutro]; cada frente enche o seu sem mudar a assinatura nem o que devolve. **Nenhuma grava sozinha, a não ser `na_vila` e o `main`:** devolvem efeitos, e quem chama os põe no evento dele. `E` é o estado; `p`, o registro da pessoa.

**`manha.py` e `tabelas_manha.py` (L)**
- `grau(p)` → a mão de manha (0, 2, 4, 6, 8) · `gazua_de(E, pid)` → o registro (com `id`) da melhor gazua inteira que a pessoa leva, ou None.
- `contra(E, pid, teste, cat)` → `(contra, ferramenta)` de `achar`, `gazua`, `desarmar` ou `arrombar` contra a categoria `cat`, com a ferramenta que ela leva (a gazua; no arrombar, a arma de impacto em uso); outro teste, None.
- `testa(E, pid, teste, contra=None, cat=None, o_que=None, oculto=False, mais=0, pedra=False)` → o `r` do `teste.rola` (o dado do jogador: rola uma vez), mais `teste`, `margem` (total − contra), `falhou_feio` (por `FALHA` ou mais), `ferramenta` e `efeitos` (o que entra no evento de quem chamou: o dom que se mostrou). Dê `cat` (achar, gazua, desarmar, arrombar) ou `contra` (escondido, escutar, atencao: o número de quem vigia, que quem chama faz). Soma a mão (se `TESTES[teste][1]`), o dom escondido e o +2 do povo (`povos.manha`); `mais` é o resto (a armadura e a luz); `pedra`: lugar de pedra.
- `mais_barulhento(E, ids, luz=False)` → `(pid, mais)`: quem anda pior escondido e o `mais` dele (a armadura do tronco e a luz) · `treino(E, pid, blocos=1)` → efeitos (o treino e a mão que sobe) · `feito(E, pid, cat)` → efeitos (`marca.feito_manha`) · `na_vila(E, vila='vila')` (o Quim; a tocha e a gazua na loja) · `voce(E)`, `so_mestre(E)`.
- `tabelas_manha.TESTES = {'escondido': ('Agilidade', True), 'escutar': ('Percepção', True), 'achar': ('Percepção', True), 'gazua': ('Agilidade', True), 'desarmar': ('Agilidade', True), 'arrombar': ('Força', False), 'atencao': ('Percepção', True)}` (o atributo; se a mão soma). E os números do projeto A: `ACHAR`, `GAZUA`, `SEM_GAZUA`, `FALHA`, `ARROMBAR`, `ARROMBAR_ARMAS`, `ESCUTAR`, `ESCONDIDO_ARMADURA`, `ESCONDIDO_LUZ`, `FEITO`, `TREINO_BLOCO`, `FURTO`.

**`povos.py` e `tabelas_povos.py` (P)**
- `de(p)` (o nome; `humano` se ausente) · `tracos(p)` (também `traços`) · `ve_no_escuro(p)` · `coragem(p)` · `corpo(p)` (`gente`/`miúdo`) · `serve(it, p)` (a conta do `estado.serve`) · `manha(p, teste, pedra=False)` (o bônus do povo no teste do ladino, de 0 a `MANHA_TETO`) · `frase(povo)`.
- `nasce(E, pid, registro, povo)` → o registro com os atributos mais os do povo (a soma não muda), `povo` e `idade` (a de adulto do povo mais um d10, pelo dado do mundo) · `na_vila(E, vila='vila')` (a gente de outros povos, o `povos` de Pedra Rasa, as armaduras miúdas na loja) · ganchos `pode_vestir`, `voce`, `mesa`, `so_mestre`.
- `tabelas_povos.POVOS[povo] = dict(mods={atributo: n}, tracos=[...], coragem=N, corpo='gente'|'miúdo', a_favor=CAMINHO|None, contra=CAMINHO|None, vida=(adulto, velho, máximo), frase='...')`. **O núcleo lê estes campos direto:** a frente P muda os números, não os nomes, e o `humano` fica neutro. Também: `TRACOS`, `ESCURO`, `VENENO`, `CORPOS`, `HUMANO`, `MANHA` (`{povo: {teste: n}}`, com os testes do `TESTES` e `achar_pedra`), `MANHA_TETO = 2`.

**`dragoes.py` e `tabelas_dragoes.py` (D)**
- `especie(tipo, idade)` → a chave (`tabelas_dragoes.chave`): `dragão-da-serra-jovem`, `verme-do-brejo-filhote`, `dragão-das-grutas-ancião`... · `dragao(tipo, idade, nome=None, **mais)` → o lutador (como `bichos.bicho`) · `de(E, lid)` → o registro do lugar, ou None.
- `monta(E, lid)` → `({"bicho": CHAVE, "nome": ..., "pv": ..., "lider": true}, dorme)` em forma curta para o cenário, ou None · `acordado(E, lid)` · `vigilia(E, lid)` → o número contra o qual o ladrão anda escondido (20 + Percepção ÷ 10 + 2, mais 2 por punhado do sono), ou None se acordado ou se não há · `punhado(E, lid, pid)` → `(efeitos, texto)` · `acorda(E, lid)` → efeitos.
- `depois_da_luta(E, lid, S, campo, quem)` → `(efeitos, {pessoa: {bem: quanto}}, linhas)`, como o `criaturas.depois_da_luta` (o PV de quem fugiu volta ao registro; o morto sai dele, e o corpo e o núcleo entram; o tesouro para quem ficou com o campo) · `poe(E, lid, tipo, idade, nome, vila=None, tesouro=0, dorme=0)` → efeitos (gera ou mestre: segredo) · `ameaca(tipo, idade, arma=None, armadura=None)` · `na_vila(E, vila='vila')` (o Tição longe, em Vau Seco: E4 a) · ganchos `virada` (evento `dragão`), `mesa` (o que se conta), `so_mestre`.
- `tabelas_dragoes`: `TIPOS`, `IDADES`, `DESPOJO`, `PECONHA`, `NUCLEO_DESDE`, `SARA_DORMINDO`, `TESOURO`, `TESOURO_MUNDO`, `VIDA`, `VIGILIA`, `CONTA` e **`ESPECIES`**: as 15 chaves de `chave(tipo, idade)`, cada uma na forma do `tabelas_bichos.ESPECIES` (`tabelas_bichos._esp`), mais `fases` e `dragao = {"tipo", "idade"}`; `nucleo` só do adulto para cima; `chefe` do jovem para cima. O esqueleto a deixa vazia.

**`masmorra.py` e `tabelas_masmorra.py` (M)**
- `de(E, lid)` → o id da masmorra (o lugar é ela ou uma sala dela), ou None · `salas(E, mid)` → as salas, nível a nível · `gera(E, molde, nome, vizinho, niveis=None, cat=None, longe=None, origem='')` → efeitos (gera: segredo) · `poe(E, planta)` → efeitos da masmorra feita à mão (a Cripta da Cova Velha) · `na_vila(E, vila='vila')` · ganchos `virada` (evento `masmorra_vida`), `voce`, `mesa` (só com a descida aberta), `so_mestre`, `retomar`, `recusa_fecha`. Os comandos da descida (projeto A, seção 3.1) no `main`.
- **Quem a masmorra chama:** o `manha` (testa, mais_barulhento, treino, feito, gazua_de), `povos.ve_no_escuro`, o `dragoes` (monta, vigilia, punhado, acorda, depois_da_luta), `criaturas.chefe`/`no_cenario`, `bichos.bando`/`despojo(..., cat=)`, `ato.passa` (`com=` o grupo) e `ato.luta_nova` (o cenário com `"ermo": SALA`, `"luz": true` ou `"tempo": ["escuro"]`, `"surpresa"`, `"lugar": {"largura", "sem_saida"}`).

**O que o acerto acrescentou** (depois do verificador): `estado.junto(E, lid)` e `estado.livre(E, lid)` (a parte do estoque que ficou com um corpo, e o resto) · `masmorra.parte_peca(E, it, n, casa)` (a parte de cada um numa peça achada: o que a loja de casa daria por ela a quem é Leigo, vezes `tabelas_masmorra.PARTILHA`, dividido pelo grupo; quem fica com a peça paga a dos outros no `pegar`, e sem a prata a peça segue ali) · `masmorra.na_pedra(E, sala)` (o molde está em `tabelas_masmorra.PEDRA`: o achar do anão ganha o +2, na armadilha e na passagem) · `tabelas_masmorra.DIZ_GUARDADO` (a frase da armadilha do baú). O bloco que fecha no caminho fecha antes de o grupo olhar a sala nova (um encontro, uma atenção); o encontro de quem chega leva `chegou` (`{espécie: quantos}`), e a mesa separa quem chega de quem já estava ali.
**O que a onda 3 acrescentou** (sem mudar assinatura): `masmorra.perto(E, pid)` (a linha "Perto daqui" do "Aqui" da MESA, fora da descida) · `dragoes.cena_em_casa(tipo, covil=True)` entra no cenário de toda luta na sala onde o dragão mora · `tabelas_dragoes.NOMES` (o nome do dragão do covil do gerador) · `tabelas_masmorra.INICIO['acorda']` (o dragão que acorda: a luta abre ali, perto) · `bichos.ameaca` de uma espécie de dragão é o `dragoes.ameaca`.
**A regra do `na_vila`:** cada um aplica os SEUS eventos (tipo `gera`; o segredo vai ao SÓ O MESTRE pelo `turno.secreto`), recusa com a frase ANTES de aplicar qualquer coisa se já foi posto, e devolve as linhas que contam o que pôs. O `vila_teste.py fantasia PASTA [inclinacao2=CAMINHO]` (onda 3, pronto) roda, nesta ordem: `talento.rola_caminho` de quem já nasceu (e a `inclinacao2` do personagem humano), `povos.na_vila`, `manha.na_vila`, `masmorra.na_vila`, `dragoes.na_vila`, e grava uma vez.

## 13. Os bancos

- O `provas_mundo.py` chama, quando existirem: `provas_4b.py` (o alicerce) [pronto], `provas_masmorra.py` (M), `provas_manha.py` (L), `provas_povos.py` (P), `provas_dragoes.py` (D). **Cada banco novo expõe `provas(n)`**, que devolve a lista de `(nome, o que deu, passa)` (`n`: o número do `provas_mundo.py`, 300 de padrão, para escalar as lutas) e roda sozinho com `python3 provas_X.py [N]`.
- Mundo de prova: `estado.novo(semente)` ou `provas_mundo.vila()`, num `MOTOR10_MUNDO` de rascunho; nunca o `ensaio/`. O dado do jogador posto à mão aceita `dom=0` (o `dado_posto` do `provas_4b.py`).
- Os bancos de hoje seguem passando sem mexer em faixa (`provas.py 600`, `provas_mundo.py`, `estresse.py 1500`). Meta que não bate fica falhando às claras, com o número; afina-se o número de regra da sua parte, nunca a faixa. Todo número mora numa página `tabelas*.py`; todo campo novo tem padrão; o que vai à mesa é português simples, sem travessão.
