# ETAPA DA MAGIA: o contrato curto (o vocabulário comum)

Este arquivo é a língua que as três frentes da onda 2 falam igual. Quem manda acima dele: a ordem de serviço, o `magia_etapa/DECISOES.md` (o juízo e as respostas M1 a M5 do jogador) e o `magia_etapa/conta/PROJETO.md` (os números). Onde este contrato diz um NOME, um CAMPO ou a FORMA de um efeito, vale o que está aqui, letra por letra.

O alicerce (onda 1) já construiu tudo o que está marcado **[pronto]**: o código existe, roda e passa nos bancos. O resto é das frentes.

## 0. O que está congelado na onda 2

Ninguém edita: `estado.py`, `ato.py`, `turno.py`, `corpo.py`, `teste.py`, `tabelas.py`, `tabelas_mundo.py`, `tabelas_talento.py`, `talento.py`, `provas_mundo.py`, `provas_talento.py`. Falta algo neles: vai em `pedidos` (o arquivo e o que falta), e o integrador faz na onda 3.
Ninguém edita `REGRAS.md`, `MUDANCAS.md`, `PROJETO.md`, `LEIA.md`, `dados/` nem `ensaio/` (o save do jogador).

**Duas armadilhas da etapa 2 (leia):**
- O `provas.py` exige que `tabelas_bichos.TRACOS` tenha de 8 a 12 traços, todos em uso e cada um com a sua prova, e que `tabelas_bichos.ESPECIES` tenha de 12 a 16 espécies. **Os traços novos não entram no `TB.TRACOS`, e as criaturas novas não entram no `TB.ESPECIES`.** Os nomes dos traços novos moram em `tabelas.TRACOS_NOVOS` (seção 9); as criaturas, em `tabelas_criaturas.ESPECIES` (frente das criaturas).
- O dom é ESCONDIDO até se mostrar (seção 8). Nenhuma conta que vai à mesa pode somar o dom que a pessoa ainda não viu.

## 1. A pessoa: os campos novos [pronto]

Todo campo tem valor padrão: o save antigo abre sem eles.

| Campo | Padrão | O que é | Verbo |
| --- | --- | --- | --- |
| `talento` | `None` | `None`: nunca rolado (save antigo). Rolado: `{caminho: grau}`, só o que não é Comum (graus −2, −1, 1, 2). `{}` = rolado e Comum em tudo | `talento poe` |
| `dom` | `{}` | `{caminho: 1 ou 2}`, no máximo um caminho | `dom poe` |
| `inclinacao` | `None` | o caminho que o jogador escolheu para o personagem (M2 b) | `inclinacao poe` |
| `feiticos` | `[]` | os nomes dos feitiços que sabe (seção 9) | `feitico aprende` / `esquece` |
| `mana` | ausente | a Mana de agora; ausente vale a cheia. Leia sempre por `estado.mana(p)`; o máximo, por `estado.mana_max(p)` | `mana soma` / `poe` |
| `tradicao` | `None` | a tradição que a pessoa segue (`arcano`, `fé`, `verde`, `pacto`): manda na volta da Mana fora da luta e no que o voto, o laço e a dívida pedem | `tradicao poe` |
| `voto` | `None` | o voto do clérigo: `{"qual": "lâmina"\|"pobreza"\|"socorro", "santuario": LUGAR, "dia": N}`; quebrado ganha `"quebrado": dia, "como": texto` | `voto poe` / `quebra` |
| `laco` | `None` | o laço do druida: `{"ermo": LUGAR, "dia": N}` | `laco poe` |
| `divida` | `0` | a dívida da bruxa (número de zero para cima) | `divida soma` |
| `funda` | ausente | a categoria da ferida mais funda desde que o PV esteve cheio (0 a 7). O gravador a apaga sozinho quando o PV enche | `funda poe` |
| `maldicoes` | `[]` | as maldições que andam nela (seção 6) | verbo `maldicao` |

**As marcas novas** (o verbo `marca.X` de sempre, só `poe`): `marca.dom_visto` = o dia em que o dom se mostrou; `marca.talento_base` = `{caminho: blocos}` no dia em que o talento foi rolado (o talento aparece 20 blocos depois); `marca.doses` = `{"dia": D, "n": poções bebidas no dia}`; `marca.curado` = `{"dia": D, "n": PV devolvidos por cura (feitiço e poção) no dia}`. Leia as duas últimas por `estado.hoje(E, p, 'doses')` e `estado.hoje(E, p, 'curado')`.

**Maestria e treino:** `tabelas_mundo.OFICIOS` ganhou `alquimia`, `encanto`, `arcano`, `fé`, `verde` e `pacto`. Logo `maestria.arcano`, `treino.fé`, `maestria.alquimia` já gravam. As tradições sobem por `tabelas_mundo.MAESTRIA_BLOCOS` (a das armas: 40, 160, 500, 1.500); a alquimia e o encanto, por `tabelas_oficio.OFICIO_BLOCOS` (a da forja: 50, 150, 375, 1.000). Os blocos de estudo de um feitiço contam como treino da tradição dele.

## 2. O lugar: os campos novos [pronto]

| Campo | Padrão | O que é |
| --- | --- | --- |
| `botica` | ausente | a bancada da alquimia, de 0 a 4 (como a `oficina`); lugar sem o campo não tem botica |
| `runas` | ausente | a bancada do encanto, de 0 a 4 |
| `santuario` | ausente | o santuário, de 0 a 4 (o voto se faz nele; a prece enche a Mana nele) |
| `maldito` | ausente | o lugar maldito: um MOLDE de maldição (seção 6) |
| `covil` | ausente | o covil (frente das criaturas): um registro livre `{...}`; se tiver `cabecas`, é inteiro de zero para cima. **Não guarda prata:** o tesouro do covil é a prata do estoque do ermo (`estoque.prata`), contada como toda prata |

Tudo pelo verbo `lugar` de sempre: `['lugar', LUGAR, 'botica', 'poe', 1]`, `['lugar', LUGAR, 'covil', 'poe', {...}]`, `['lugar', LUGAR, 'covil.cabecas', 'soma', -1]`.
A contagem do ermo (`bichos`, `teto`) e o encontro da saída de caça aceitam as espécies de `tabelas_bichos.ESPECIES` **e** as de `tabelas_criaturas.ESPECIES` (`estado.especie(nome)` devolve o registro de uma ou de outra, ou None; a página é lida se existir).

## 3. O item: os tipos e os campos novos [pronto]

`itens.item(tipo, cat, nome=None, ...)` monta o registro; `['item', 'nasce', registro]` grava.

| Tipo | Campos | Uso (onde se veste) | Matéria (unidades) · preço Comum pela regra de hoje |
| --- | --- | --- | --- |
| `foco` | `forma`: `varinha` \| `cajado` \| `símbolo` \| `talismã` | `foco` (um por pessoa) | varinha 2 de madeira e 1 de osso, 30 · cajado 4 de madeira e 1 de osso, 50 · símbolo 3 de metal, 30 · talismã 2 de osso e 1 de couro, 30 |
| `amuleto` | | `pescoco` (um por pessoa) | 1 de osso, **10** |
| `elixir` | `pocao` (chave da seção 5), categoria do Épico para cima | não se veste; bebido, `some` | o preço da poção da categoria (6 vezes 6 por categoria) |
| `escrito` | `feiticos`: lista de nomes (seção 9) | não se veste | 30 o de grau 1, vezes 6 por grau (a categoria do escrito é o maior grau menos 1) |

`itens.item('foco', 'Comum', forma='cajado')`, `itens.item('amuleto', 0)`, `itens.item('elixir', 3, pocao='cura')`, `itens.item('escrito', 0, 'Cartilha do arcano', feiticos=['seta', 'luz'])`. O preço sai de `tabelas_mundo.peso_da_peca(tipo, cobre, familia, forma)` (o mercado já o lê por `peso_do_item`). A loja ainda não os põe na prateleira: isso é do mercado (frente do mundo).

**Campos novos nas peças de sempre (arma, armadura, escudo):**
- `encantos`: lista de `{"feitico": NOME, "grau": 0 a 4 (o grau de quem gravou: Iniciante 1 a Lendário 4), "feito_por": PESSOA ou None, "dia": N, "gasto": None ou o bloco absoluto em que foi solto}`. Um por peça; dois do Único para cima (`tabelas_mundo.encantos_max(cat)`). Volta a carregar 1 bloco depois de solto (`estado.encanto_carregado(E, enc)`). Foco e amuleto não levam encanto.
- `maldita`: um MOLDE de maldição (seção 6), ou ausente.
- `benta`: o bloco absoluto até o qual a arma está benta (7 dias), ou ausente.
- `veneno`: `{"cat": K, "ate": bloco absoluto}` a dose passada na lâmina (seca em 1 dia), ou ausente.

`estado.lutador` já entrega as cópias das peças com o que venceu tirado (`benta` e `veneno` vencidos somem da cópia) e com `carregado: True/False` em cada encanto.

## 4. O que o gravador faz sozinho [pronto]

- **A morte:** as maldições que andavam no morto vão para `pessoa.morte.maldicoes`; a lista dele fica vazia. A peça maldita cai solta com o corpo, ainda maldita.
- **A peça maldita não sai:** enquanto o dono tem uma maldição andando com `de: "peça"` e `fonte` igual ao id da peça, a peça não sai de uso nem muda de dono (recusa: "a mão não larga a peça"). Quebre a maldição no mesmo evento, antes de mexer na peça.
- **A ferida funda** some quando o PV enche.
- **O talento e o dom** só se gravam em evento `gera`, `mestre` ou `talento`; o talento já rolado só se troca em evento `mestre`.

## 5. Os bens novos [pronto]

Chave na carga e no estoque, como a matéria: `nome:categoria`.
- **As poções do Comum ao Raro são bens** (`tabelas_mundo.POCOES`, `POCAO_ATE = 2`): `cura:0`, `antídoto:1`, `veneno:2` (a dose de veneno de lâmina: 1 dose = 1 golpe), `mana:0`, `guarda:1`, `fúria:0`, `vigília:0`, `quebra-maldição:1`. Do Épico para cima é **elixir** (item, seção 3). O remédio segue o bem de sempre (`remédio`).
- **A peçonha** (despojo do bicho de veneno, da categoria dele até a Rara): `peçonha:0`, `peçonha:1`, `peçonha:2` (é matéria: `tabelas_mundo.MATERIAS`).
- **A água benta:** `água benta` (sem categoria, como o remédio).
- `estado.nome_bem` diz à mesa: "poção de cura Comum", "antídoto Raro", "veneno de lâmina Incomum", "peçonha Rara".
O preço e o consumo do povo são do mercado (frente do mundo): `tabelas_mercado` ainda não os conhece, e nada mais muda por eles existirem.

## 6. As maldições: o registro e o molde [pronto]

**O registro** (o que anda numa pessoa, em `pessoa.maldicoes`):
```
{"id": "m0003", "nome": "a Mão Fria", "cat": 1, "tipo": "míngua", "passo": 2, "desde": 12, "de": "peça", "fonte": "i0031", "quem": null,
 "condicao": {"tipo": "devolver", "item": "i0031", "onde": "capela"}, "sabe": 0, "suspensa": null}
```
- `id`: o gravador dá (não venha no `poe`). `cat`: 0 a 7. `passo`: 1 a 6 (padrão 1). `desde`: o dia (padrão hoje).
- `tipo` (o sinal e a cor; o relógio é um só, o do `conta` D.3): `míngua`, `chaga`, `azar`, `insônia`, `marca` (`tabelas_mundo.MALDICAO_TIPOS`).
- `de` (a origem): `feitiço`, `bicho`, `lugar`, `peça`, `juramento`. `fonte`: o id ou nome de onde veio (pessoa, espécie, lugar, peça). `quem`: a pessoa que rogou, ou null.
- `condicao`: `{"tipo": ...}` com o tipo de `devolver`, `matar`, `perdao`, `morte`, `sair`, `cumprir`, `queimar`, `divida` e os campos que a frente quiser.
- `sabe`: o degrau de saber guardado, 0 (não sabe), 1 (desconfia), 2 (sabe: alguém leu). Só sobe. A mesa mostra `max(sabe, 1 se passo >= 2)`.
- `suspensa`: o último dia em que o relógio não anda (a poção que "segura"), ou null.

**O molde** (o que mora numa peça `maldita` ou num lugar `maldito`): `{"nome", "cat", "tipo", "condicao"}`.

**Os passos** (`tabelas_mundo.MALDICAO_PASSOS`, `MALDICAO_PENA`): 1 a marca (nada) · 2 o peso (−1) · 3 a míngua (−2; a noite não devolve PV) · 4 a chaga (−2; as feridas não saram; a Mana não volta fora da luta) · 5 o fim à vista (−4; a frente do mundo tira 10% do PV na virada) · 6 a morte (a frente do mundo mata, no mesmo evento, com a causa escrita).
**Já feito no `corpo.py`:** `corpo.pena(p)` soma a pior pena de maldição à pena do corpo (entra em todo teste e na luta); `corpo.pena_maldicao(p)` dá só ela; `corpo.passo_maldicao(p)` dá o maior passo; a noite não cura do passo 3; a ferida não sara do passo 4 (o descanso em casa também). A volta da Mana fora da luta confere `corpo.passo_maldicao(p) >= 4`.

## 7. Os verbos novos do gravador, com a forma exata [pronto]

```
['pessoa', ID, 'talento', 'poe', {caminho: grau}]       graus −2, −1, 1, 2 (o 0 não se escreve); só em gera, mestre ou talento
['pessoa', ID, 'dom', 'poe', {caminho: grau}]           grau 1 ou 2, no máximo um caminho; {} = sem dom
['pessoa', ID, 'inclinacao', 'poe', CAMINHO ou None]    só o personagem do jogador
['pessoa', ID, 'mana', 'soma', N]                       fica entre 0 e a Mana máxima (o que passa, o gravador corta)
['pessoa', ID, 'mana', 'poe', N]                        N entre 0 e a máxima (fora disso, recusa)
['pessoa', ID, 'feitico', 'aprende', NOME]  ·  ['pessoa', ID, 'feitico', 'esquece', NOME]
['pessoa', ID, 'tradicao', 'poe', TRADICAO ou None]
['pessoa', ID, 'voto', 'poe', {"qual", "santuario", "dia"} ou None]  ·  ['pessoa', ID, 'voto', 'quebra', 'como foi']
['pessoa', ID, 'laco', 'poe', {"ermo", "dia"} ou None]
['pessoa', ID, 'divida', 'soma', N]                     nunca abaixo de zero (recusa)
['pessoa', ID, 'funda', 'poe', CATEGORIA ou None]
['maldicao', ID, 'poe', REGISTRO]                       põe uma maldição (sem "id": o gravador dá)
['maldicao', ID, MID, 'passo', N]                       anda N passos (+1; a poção: −2); fica entre 1 e 6
['maldicao', ID, MID, 'quebra', 'como foi']             sai da pessoa
['maldicao', ID, MID, 'sabe', DEGRAU]                   0, 1 ou 2; só sobe
['maldicao', ID, MID, 'suspensa', DIA ou None]
['maldicao', ID, MID, 'condicao', {"tipo": ...}]
['item', IID, 'uso', 'poe', 'foco' | 'pescoco']         (e os de sempre)
['item', IID, 'encanto', 'grava', {"feitico", "grau", "feito_por", "dia"}]
['item', IID, 'encanto', 'gasta', INDICE]               marca o bloco de agora; volta a carregar 1 bloco depois
['item', IID, 'encanto', 'apaga', INDICE]
['item', IID, 'maldita', 'poe', MOLDE ou None]
['item', IID, 'benta', 'poe', BLOCO ou None]            só arma
['item', IID, 'veneno', 'poe', {"cat", "ate"} ou None]  só arma
['lugar', LUGAR, 'botica' | 'runas' | 'santuario', 'poe', 0 a 4 ou None]
['lugar', LUGAR, 'maldito', 'poe', MOLDE ou None]  ·  ['lugar', LUGAR, 'covil', 'poe', {...} ou None]
['obra', 'abre', {..., "tipo": "leva" | "gravar"}]      a leva da alquimia e a gravação do encanto usam a obra de sempre
```
Os invariantes novos (`estado.valida`): talento e dom na tabela; feitiço sabido existe; Mana entre 0 e a máxima; tradição, voto (com santuário que existe) e laço (com ermo que existe) certos; dívida de zero para cima; funda de 0 a 7; toda maldição tem id, nome, categoria, passo de 1 a 6, tipo, origem e condição da lista; morto sem maldição andando; tipo de item e uso casados; um foco e um amuleto em uso por pessoa; encantos só em arma, armadura e escudo, até o máximo da categoria; elixir do Épico para cima; escrito com feitiço que existe; botica, runas e santuário de 0 a 4; covil sem prata.

## 8. Os talentos e os dons [pronto]

`tabelas_talento.py` (os números) e `talento.py` (a regra). Os 16 caminhos: `fio` (adaga, espada, machado, montante), `haste` (lança, alabarda), `peso` (maça, martelo, malho), `tiro` (arco, besta), `forja`, `couro`, `caça`, `coleta`, `comércio`, `cura`, `alquimia`, `encanto`, `arcano`, `fé`, `verde`, `pacto`. O soco (`punho`) não é de caminho nenhum.

| O que se chama | O que devolve |
| --- | --- |
| `talento.caminho_de(chave)` | `'espada'` → `'fio'`; `'forja'` → `'forja'` |
| `talento.grau(p, chave)` | o grau do talento no caminho da chave (−2 a 2; 0 se não rolado) |
| `talento.pede(p, chave, tabela, grau)` | os blocos que o grau pede para ESTA pessoa (a tabela vezes o talento, arredondado para cima), ou `None` acima do teto |
| `talento.blocos(p, chave, n)` | `n` blocos vezes o talento (para o estudo de um feitiço: 3, 6, 18, 54, 162) |
| `talento.teto(p, chave)` | o grau mais alto que a mão sobe (Negado: Iniciante; Lerdo: Mestre; os outros: Lendário) |
| `talento.dom(p, chave)` | o dom de verdade no caminho (0, 1, 2): é o que entra na conta e no dado |
| `talento.dom_visto(p, chave)` | o dom que a pessoa já viu (0 até se mostrar): é o que entra na conta que vai à mesa |
| `talento.oculto(p, chave)` | `dom − dom_visto`: o que vai escondido no dado |
| `talento.kw(p, chave)` | `{'dom': n}` se há dom escondido, senão `{}`: chame `teste.rola(..., **talento.kw(p, c))` (assim quem não tem dom chama o dado como sempre, e o dado posto dos bancos segue servindo) |
| `talento.rola(E, pid, inclinacao=None)` | os efeitos do nascimento pelo dado do mundo (talento, dom, `marca.talento_base`, e a inclinação) |
| `talento.nasce(E, pid, registro, inclinacao=None)` | o registro de `['pessoa', 'nasce', ...]` com o talento e o dom já rolados |
| `talento.mostra(E, pid)` | o efeito que revela o dom (`marca.dom_visto`), ou `[]` se já se mostrou |
| `talento.decidiu(r)` | o dom escondido fez passar este teste (o `r` do `teste.rola`)? |

**O que já está ligado:** a escada de toda maestria (armas no `ato.py`; forja e couro no `oficio.py`; caça e coleta no `caca.py`; comércio no `mercado.py`) pede `talento.pede` e respeita o teto. O dom soma: na arma (acerto, e metade na Defesa, só com arma daquela mão); na bancada, dentro do teto de +8 do preparo; no rastro e na coleta; no comércio, 2,5 ou 5 pontos no que a loja paga (sem passar de 80% e 60%). **Falta a frente de cada um ligar:** as tradições (dom na Conjuração, metade na Firmeza, o mesmo na Mana: `estado.mana_max` já soma), a alquimia e o encanto (dentro do teto de +8), a cura (no tratamento).

**O dado com dom escondido:** `teste.rola(E, o_que, atributo, contra, mais=VISIVEL + talento.dom_visto(p, c), **talento.kw(p, c))`. O dado posto à mão de um banco tem de aceitar `dom=0` (veja `provas_talento.dado_posto`). `teste.total_visto(r)` dá o total como a mesa o vê. A mesa vê o total sem o dom quando ele não decidiu; quando decidiu, vê "sem o dom, falhava" e quem chamou aplica `talento.mostra(E, pid)` no mesmo evento do ato. Teste de três faixas (a bancada): quem chama põe `r['fez'] = True` se o dom mudou a faixa, antes do `teste.diz`.
**Quando aparece:** o talento, 20 blocos depois de rolado, no caminho (`talento.aparece`); o dom, no teste em que decidiu, ou quando alguém o lê (o feitiço `ler`, ou o clérigo; a frente do mundo aplica `talento.mostra`). O módulo `talento` põe as frases no "Você" da MESA e tudo no SÓ O MESTRE.
**O nascimento:** a vila de teste nova (`vila_teste.py PASTA ... [inclinacao=CAMINHO]`) já nasce com talentos. Para quem já existe, `talento.rola` (a frente das criaturas chama no `vila_teste.py magia`; quem tem `talento` diferente de `None` já foi rolado). A gente dos bancos (`provas_mundo.vila()`) não rola: é a pessoa comum de hoje.

## 9. A base comum da magia (`tabelas.py`) [pronto]

As duas frentes leem daqui; a frente da luta afina os SEUS números no `tabelas_magia.py` e não redefine estes.
- `T.TRADICOES = {arcano: Afinidade, fé: Vontade, verde: Percepção, pacto: Afinidade}`: o atributo da Conjuração.
- `T.FOCOS[forma]`: `maos`, `vezes` (o cajado: 1,25), `pede` (atributo, quanto), `de` (tradições), e o cajado `apara`, `dado` 1d6, `golpe` impacto. Foco de outra tradição rende uma categoria abaixo; sem foco, Comum com −4 (números da frente da luta). A regra das mãos do foco (o cajado pede as duas; o de uma mão com arma e escudo) também é da frente da luta: o `ato.py vestir` só põe o foco em uso.
- `T.conjuracao(maestria, atributo, foco_cat, dom=0)` = maestria + dom + (atributo ÷ 10) ÷ 2 + bônus do foco.
- `T.firmeza(vontade, maestria_maior, amuleto_cat=None, tronco_cat=None, dom=0)` = 22 + (Vontade ÷ 10) ÷ 2 + maior maestria ÷ 2 + dom ÷ 2 + o bônus do amuleto (sem amuleto: metade do bônus da armadura do tronco). Fora da luta: `estado.firmeza(E, pid)`. O calejo é da luta.
- `T.guarda(amuleto_cat, tronco_cat)`: o valor do amuleto, ou 0,6 do valor da armadura do tronco (`GUARDA_ARMADURA`, M1 a), o maior; sem um nem outro, um terço.
- `T.mana_max(afinidade, vontade, maestria, dom=0)` = (Afinidade + Vontade) ÷ 10 + maestria + dom; a pessoa: `estado.mana_max(p)` (a melhor tradição dela, com o dom).
- `T.cura(dado, cat_cura, cat_funda)` = dado × 6 × 3^(cura − funda); `T.CURA_TETO = 0,5` do PV máximo por dia (feitiço e poção somados); `T.doses_dia(vigor)` = Vigor ÷ 30, no mínimo 1; `T.ENJOO = (24, 4)`.
- **`T.FEITICOS[nome]` = `{de, grau, mana, fora}`** (os nomes, as tradições, os graus e o custo não mudam; o resto dos números é do `tabelas_magia.FEITICOS`, com as mesmas chaves). Os 24 e o truque, com estes nomes exatos:
  `luz` (todas, truque) · arcano: `seta`, `prender`, `escudo`, `lança-de-fogo`, `bola-de-fogo`, `raio` · fé: `cura`, `bênção`, `amparo`, `castigo`, `guarda`, `quebrar-maldição` · verde: `raízes`, `espinho`, `névoa` (névoa ou lamaçal: quem lança escolhe `neblina` ou `lama`), `afugentar`, `seiva`, `chamar` · pacto: `mau-olhado`, `medo`, `sangria`, `ler`, `nó`, `praga`.
- **`T.TRACOS_NOVOS`** (a lista fechada dos traços novos que a luta roda; ver seção 10).

## 10. O lutador: o que entra e o que volta

**O que entra** (o dicionário que vai ao `pessoas.ficha` e ao `luta.nova`). Gente do mundo: `estado.lutador(E, pid)` [pronto] já traz, além do de hoje: `feiticos`, `mana`, `mana_max`, `tradicao`, `dom`, `pena_magia` (a pior pena de maldição: já está dentro de `pena`), `maldicoes` (cópia), `funda`, `doses` e `curado` (os de hoje), `carga` (só as poções e as doses de veneno que leva), `elixires` (`[{id, pocao, cat, nome}]`) e, no `equip`, `foco` e `amuleto`. Para a MESA, `estado.lutador(E, pid, visivel=True)` dá só o dom que a pessoa viu.
**Quem lança, seja gente, povo ou bicho:** quem traz `feiticos` (lista de nomes) e `mana` (e, se quiser, `mana_max`, `tradicao` e o foco: gente e povo no `equip['foco']`; o bicho com o traço `lança`, pela categoria do corpo e pelo instinto). Quem traz `feiticos` sem `mana` começa com `T.mana_max`.
**O povo** (goblin, orc, ogro...) é gente: a ficha de gente, com arma, armadura e escudo de verdade, mais o campo `povo = {"especie", "povo", "tamanho", "tracos", "coragem", "couro", "cat"}`. **[pronto]** `pessoas.ficha` aplica o tamanho (PV, Defesa, alcance da mão, cerco, quanto ocupa: `TB.TAMANHOS`), os traços, a coragem e a pele (o `couro` vale como armadura onde a peça não cobre). Gente comum também pode trazer `tracos`.
**A ficha já traz com valor neutro** [pronto]: `F['feiticos']`, `mana`, `mana_max`, `tradicao`, `foco`, `amuleto`, `dom`, `pena_magia`, `firmeza` (já calculada pela base comum), `tracos`, `fases`, `carga`, `elixires`, `doses`, `curado`, `funda`, `maldicoes`. A frente da luta põe o resto (Conjuração, guarda, estados, calejo, a sintonia do foco, do amuleto e da peça encantada) e registra o foco e o amuleto em `S['itens']` no `luta.nova`, para o desgaste deles voltar ao estado como o das outras peças. O dom de arma já está no acerto e na Defesa; a arma traz `w['dom']`, e o golpe que passou só por ele já põe `dom_fez` [pronto].

**O que volta ao estado** (`ato.luta_fecha`) [pronto]: do lutador que tem `id` no mundo, se vier no fim da luta:
- `mana` (a de agora) · `funda` · `doses` · `curado` (os totais do dia);
- `gastou` = `{bem: quanto}` (poção bebida, dose de veneno: sai da carga) · `elixires_gastos` = `[id]` (somem) · `venenos_gastos` = `[id da arma]` (a dose da lâmina se gastou) · `encantos_gastos` = `[[id, índice]]`;
- `maldicoes_postas` = `[registro]` (maldição posta NELE na luta, pelo traço `amaldiçoa` ou outro) · `marcas` = `{chave: valor}` (vira `marca.chave`) · `dom_fez` = True (o dom decidiu um golpe: vira `marca.dom_visto`).
O que não mudou não gera efeito: a luta sem magia volta ao estado igual a hoje (o banco confere). Bichos e criaturas sem `id` não voltam ao estado (a caça conta o que morreu).

**Os traços novos** (`T.TRACOS_NOVOS`; a luta roda todos, cada um com prova de 8 pontos ou mais, a meta M20; a frase de cada um mora na página das criaturas, os números na da magia):

| Traço | O que faz |
| --- | --- |
| `resiste` | o corpo guarda contra a magia inteiro (não 0,6), e a Firmeza leva o bônus inteiro do corpo |
| `imaterial` | arma sem encanto e sem bênção conta uma categoria abaixo contra ele; feitiço e peça encantada contam inteiros; não é derrubado nem agarrado |
| `amaldiçoa` | a ferida que ele abre põe uma maldição da categoria do corpo, no passo 1 (volta em `maldicoes_postas`) |
| `lança` | sabe feitiços da lista (`feiticos`), com Mana e Conjuração pelo instinto e pela categoria do corpo |
| `sem vida` | não sangra, o veneno não pega, não testa a coragem (não foge), o fôlego não gasta e não faz a ação a mais; a zero de PV se desfaz (não fica caído) |
| `ossos` | o golpe de corte e o de ponta valem metade; o de impacto, inteiro |
| `dreno` | recupera em PV metade do que o golpe do corpo tira |
| `ardente` | quem golpeia de perto leva o fogo de volta (o teto do `devolve` da categoria); a ferida que o corpo abre queima cinco rodadas, como a que sangra |
| `noturno` | o escuro não tira nada do golpe nem do tiro |

**As fases do chefe** (o lutador pode trazer `fases`, uma lista; a luta roda): `{"abaixo": fração do PV máximo, "diz": frase, "ganha": [traços], "perde": [traços], "feiticos": [nomes a mais], "mana": quanto volta, "brado": true (os do lado dele ficam benzidos por 3 rodadas), "ergue": N (levanta N caídos como `sem vida` do lado dele)}`. Ao cruzar o limiar, o chefe muda, a luta para e pergunta. Lacaios: os campos de hoje (`guarda`, `lider`).

## 11. Os ganchos [pronto]

- **`tabelas_mundo.MODULOS`** = `mercado`, `oficio`, `caca`, `talento`, `magia`, `magia_mundo`, `alquimia`, `encanto`, `maldicao`, `criaturas`. O módulo que ainda não existe fica de fora sem quebrar nada (`estado.modulos(gancho)`, importado uma vez só). Cada módulo pode ter:
  `virada(E)` (o dia vira) · `bloco(E, pid, esforco, dorme)` (efeitos de UM bloco no corpo de quem age, junto e espera: a volta da Mana fora da luta; devolve a lista de efeitos, sem aplicar) · `vestiu(E, pid, iid)` (depois de alguém pôr uma peça em uso: a peça maldita; aplica o que for e devolve o texto, ou '') · `voce(E)` (linhas no "Você" da MESA) · `mesa(E)` · `so_mestre(E)` · `retomar(E)` · `recusa_fecha(E)` (a lista dos motivos para o `turno.py fecha` recusar: a maldição no passo 4 sem pergunta aberta).
- **Quem põe o quê na MESA:** `talento` (as frases do talento e do dom, e o SÓ O MESTRE deles) · `magia_mundo` (a Mana, os feitiços, a tradição, o voto, o laço, a dívida; o que o lugar ensina e vende) · `maldicao` (cada maldição pelo degrau de saber; tudo no SÓ O MESTRE; toda maldição do personagem no RETOMAR; o `recusa_fecha`) · `alquimia` (a botica) · `criaturas` (a ameaça lida antes; o covil no SÓ O MESTRE).
- **Os eventos novos** (`tabelas_mundo.EVENTOS`): `talento`, `estudar`, `lancar` (feitiço fora da luta), `rito` (1 bloco: quebrar, ler, benzer, praga, prece), `beber` (fora da luta; passar veneno na lâmina), `alquimia`, `encantar`, `maldicao`, `servico` (serviço de magia pago de pessoa a pessoa), `covil` (a vida do covil: mundo sozinho).
- **Os bancos:** o `provas_mundo.py` chama, quando existirem, `provas_talento.py` (o alicerce), `provas_magia.py` (frente do mundo) e `provas_criaturas.py` (frente das criaturas). A frente da luta põe as metas dela no `provas.py` e no `estresse.py`.

## 12. O que cada frente expõe (os nomes que as outras chamam)

- **Magia na luta:** `magia.escolhe(S, f)` (quem o jogador não comanda: gente, povo ou bicho que lança); `tabelas_magia.FEITICOS[nome]` (os números de luta de cada feitiço); as ordens `lancar FEITICO [em ALVO | casa N] [sempre]`, `beber POCAO`, `usar PECA`. Cria `/tmp/claude-0/-home-user-ferir/2caa978a-1aa4-5b05-88b7-11bcda935cb0/scratchpad/magia/construcao/MAGIA_PRONTA` ao terminar.
- **O mundo da magia:** `magia_mundo.estudar`, `aprende`, a volta da Mana (`bloco`), o voto, o laço, a dívida, `beber` fora da luta, a cura fora da luta; `alquimia.*` (a leva no molde da forja, a botica, as nove receitas); `maldicao.poe(E, pid, molde, de, fonte, quem=None)` (os efeitos), `maldicao.virada(E)`, `quebra`, `rito`; o encanto (`encantar`), o amuleto, os focos e os escritos na prateleira; os serviços como jornal. No mercado [pronto]: `mercado.parte(p, vista)`, `parte_peca(p, vista)`, `paga(..., vista)`, `paga_peca(..., vista)` (com `vista=True`, a conta que a pessoa faz, sem o dom escondido); o dom do comércio já se mostra na venda.
- **As criaturas e a vila:** `tabelas_criaturas.ESPECIES` (o gravador lê os nomes), `tabelas_criaturas.TRACOS` (a frase de cada traço novo), `criaturas.criatura(especie, nome=None, **mais)` e `criaturas.bando(...)` (o lutador pronto), `bichos.ameaca` para os dois; o covil; `vila_teste.py magia PASTA [inclinacao=CAMINHO]` (chama `talento.rola` para quem tem `talento` igual a `None`).

## 13. Lembretes da ordem que mais pesam aqui

A pessoa comum é a pessoa de hoje: os bancos de hoje passam sem mexer em faixa. Nada novo cria prata: a prata só muda de mão (pessoa, estoque do lugar), e toda renda nova tem meta. Todo número mora numa página `tabelas*.py`. O que vai à mesa é português simples, sem jargão e sem travessão. Saída longa vai para arquivo.
