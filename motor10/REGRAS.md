# MOTOR 10 — O LIVRO DE REGRAS

Este é o livro de regras do Motor 10. É um só, por assunto, sem história: o que mudou e quando fica no `MUDANCAS.md`.
Os números moram todos nas páginas `tabelas*.py`. Nenhuma regra vale antes de passar no banco de provas (`python3 provas.py` e `python3 provas_mundo.py`).

**Estado:** estão escritos e provados os capítulos 1 a 4 (a pessoa, os itens, a luta, o banco de provas), o capítulo 5 (o tempo, o corpo, o estado e o turno: a etapa 1 do mundo) e os capítulos 6 a 9 (os bichos, o ofício, o mercado, a caça e a coleta: a etapa 2, "viver de um ofício"). Todas as metas passam. Duas foram fechadas por decisão do jogador: a Lendária é difícil de propósito, e a meta dela é o dia da primeira tentativa (7.13); a loja paga 40% pelas peças, e com isso forjar para a loja deixou de ser mina (8.8, 8.13). O plano do resto está no `PROJETO.md`. A vila de teste está no `GUIA_VILA.md`.

**Precedência:** este livro manda. Regra antiga do save do Ferir não vale aqui.

**O dado:** todo teste é **2d20 + o que a pessoa soma**, contra um número. Cada 20 rola de novo e soma. O script rola; ninguém rola de cabeça.

---

## 1. A pessoa

1.1 **Atributos.** Seis: Força, Agilidade, Vigor, Vontade, Percepção, Afinidade. O bônus de um atributo é o atributo ÷ 10.

1.2 **Nível.** Cada nível dá 1 ponto de atributo e um quarto de ponto de PV. Fora isso, o nível não soma em nada na luta: nem no acerto, nem no dano, nem nas ações.

1.3 **Maestria** na arma: Leigo 0, Iniciante 2, Treinado 4, Mestre 6, Lendário 8. Vem de treino e de feito, não de nível. Um grau de maestria (2 pontos) vale +2 no acerto e +1 na Defesa.

1.4 **O que sai disso** (o script calcula; ninguém digita):

| | Conta |
| --- | --- |
| PV | Vigor × 2 + nível ÷ 4 |
| Fôlego | 6 + bônus de Vigor |
| Acerto | maestria + (bônus de Força + bônus de Agilidade) ÷ 4 + o bônus da arma |
| Defesa | 22 + bônus de Agilidade ÷ 2 + maestria ÷ 2 + o da armadura + **o que apara melhor** (o escudo ou a própria arma) |
| Força do golpe | o dano vezes 1 + 0,03 por ponto de bônus de Força (arco e adaga: Agilidade; besta: fixo, 1,2) |
| Ações por rodada | **2, para todo mundo** |
| A ação a mais (o esforço) | uma, só para golpear, pelo dobro do fôlego. Mestre: pelo fôlego normal. Lendário: mais uma, pelo dobro |
| Reações por rodada | 1; Lendário 2 |
| Iniciativa | 2d20 + bônus de Percepção + bônus de Agilidade + o da armadura, **rolada a cada rodada** |

1.5 **O que apara.** O escudo dá 4 mais o bônus da categoria dele, e só com arma de uma mão. A arma dá o bônus da categoria dela (a espada e o montante, +2). Vale o maior dos dois: uma espada Única apara melhor que um escudo Raro. Arco e besta não aparam. Arma quebrada ou largada não apara.

1.6 **Gente gerada** (o mundo, os testes) nasce com Força 70, Agilidade 60, Vigor 70 (o guerreiro) e reparte os pontos do nível. Um guerreiro de nível 20 tem Força 76: ainda não veste placa nem empunha arma pesada sem pagar por isso (2.7).

---

## 2. Os itens

2.1 **O Livro de Itens.** Toda arma, armadura e escudo é um registro (`itens.py`): nome, categoria, durabilidade, efeitos, dono, quem fez, e a história. O núcleo de um chefe (6.11) também é item do Livro. **Peça que não está no Livro não existe.** A ficha de luta sai sozinha do que a pessoa veste (`pessoas.py`).

2.2 **As oito categorias** e o que cada uma vale:

| Categoria | Valor (arma e armadura) | Bônus (acerto, ou Defesa ao aparar) | Durabilidade |
| --- | --- | --- | --- |
| Comum | 1 | 0 | 10 |
| Incomum | 3 | +4 | 20 |
| Raro | 9 | +8 | 30 |
| Épico | 27 | +12 | 40 |
| Único | 81 | +16 | 50 |
| Lendário | 243 | +20 | 60 |
| Mítico | 729 | +24 | 80 |
| Primordial | 2.187 | +28 | 100 |

2.3 **A regra de ouro: o item decide.** Cada categoria vale o triplo da de baixo, e o que conta é a **diferença** entre a arma de quem bate e a armadura de quem apanha:

| A arma está… | O golpe vale |
| --- | --- |
| na mesma categoria da armadura | × 1 |
| uma acima | × 3 |
| duas acima | × 9 |
| três acima | × 27 |
| uma abaixo | um terço |
| duas abaixo | um nono |
| três abaixo ou mais | quase nada (o aço não passa) |

Parte do corpo sem armadura conta como um degrau abaixo do Comum. **Cabeça sem elmo é onde se morre.**

2.4 **As armas.**

| Arma | Dado | Golpe | Alcance | Mãos | Peso | Ofício |
| --- | --- | --- | --- | --- | --- | --- |
| mãos | 1d4 | impacto | 1 casa | 1 | leve | nunca quebram |
| adaga | 1d4 | ponta | 1 | 1 | leve | arma de reserva; pede Agilidade |
| espada | 1d8 | corte | 1 | 1 | média | apara: +2 na Defesa |
| maça | 1d8 | impacto | 1 | 1 | média | amassa a placa |
| lança | 1d8 | ponta | 2 | 1 | média | bate por cima do ombro de quem está na frente |
| machado | 1d10 | corte | 1 | 1 | pesada | |
| martelo | 1d10 | impacto | 1 | 1 | pesada | amassa a placa |
| montante | 1d12 | corte | 1 | 2 | pesada | apara: +2 na Defesa |
| alabarda | 1d12 | corte | 2 | 2 | pesada | alcance |
| malho | 1d12 | impacto | 1 | 2 | pesada | amassa a placa |
| arco | 1d8 | ponta | à distância (12 casas) | 2 | média | pede Agilidade |
| besta | 1d10 | ponta | à distância (12 casas) | 2 | média | recarrega 1 ação; a força é fixa |

- Arma de duas mãos de corpo a corpo: o valor vezes 1,25, e não se usa escudo. (Arco e besta não ganham isso.)
- Arma pesada: 2 de fôlego por golpe.
- Arma de alcance 2 contra quem está colado: −2 (a haste atrapalha).

2.5 **As armaduras.** A peça cobre partes do corpo (cabeça, tronco, braços, pernas). O elmo é uma peça à parte.

| Material | Proteção | Pede de Força | Fôlego | Defesa | Iniciativa |
| --- | --- | --- | --- | --- | --- |
| couro (ou nada) | 0,7 do valor | 40 | nada | +3 | +2 |
| malha | o valor | 60 | nada | 0 | 0 |
| placa | 1,4 do valor | 80 | 1 por rodada em que a pessoa golpeia ou anda | −2 | −2 |

A Defesa e a iniciativa são as da peça que cobre o tronco. O couro deixa esquivar; a placa prende e protege.

2.6 **O golpe contra o material.** A proteção da peça vezes:

| | couro | malha | placa |
| --- | --- | --- | --- |
| corte | 0,85 | 1,1 | 1,3 |
| ponta | 1 | 0,85 | 1,15 |
| impacto | 1,15 | 1 | 0,7 |

O fio abre o couro e escorrega no metal; a ponta abre o elo da malha; o malho amassa a placa.

2.7 **O requisito é por atributo, nunca por nível.** Qualquer pessoa empunha qualquer peça, de qualquer categoria.
- A peça pede **Força pelo peso**: leve 40, média 60, pesada 80 (a adaga e o arco pedem Agilidade; o escudo pede 60). A categoria não muda o que ela pede.
- **Faltou atributo, a peça pesa:** −1 no acerto (arma) ou na Defesa (armadura, escudo) a cada 5 pontos que faltam, e +1 de fôlego a cada 10. A falta conta peça por peça.

2.8 **Sob medida.** Peça feita ou ajustada por um ferreiro para um dono, com o nome gravado:
- **para o dono**, pede 10 a menos por grau do ferreiro (graus 1 a 4) e assenta (+1 no acerto ou na Defesa; a armadura protege um décimo a mais);
- **na mão de outro**, rende uma categoria abaixo.
- **O dono é uma pessoa, não um nome:** a peça ajustada no mundo guarda quem é o dono. Na mão de outra pessoa de mesmo nome, é peça de outro.

2.9 **Sintonia.** A pessoa sustenta **Vontade ÷ 20** peças Épicas ou melhores (no mínimo uma), as melhores primeiro. Cada peça que passa disso **dorme**: rende uma categoria abaixo e os efeitos dela não valem (nem o "leve", nem o "não quebra"). Vontade 55 sustenta duas: quem quer o conjunto inteiro treina a Vontade.

2.10 **Durabilidade.** O aço gasta o aço.
- **Aparado:** o golpe que erra por não mais que o bônus do escudo (ou da arma que apara) foi aparado. Dos dois aços que se encontraram, o de categoria **menor** perde 1.
- **O aço não passa:** o golpe que acerta e tira 0 gasta 1 da arma.
- **Dois 1:** a arma perde 1.
- **A armadura** perde 1 quando leva golpe de arma de categoria maior (2, se a arma está duas ou mais acima), e 1 em todo crítico. O escudo em uso perde 1 quando o dono leva um crítico.
- **O uso:** no fim da luta, toda peça que entrou nela perde 1.
- **A zero, quebra:** a arma vira um pedaço de ferro Comum com −4 no acerto, sem aparo e sem efeito; a armadura desfeita não protege e perde os efeitos.
- As mãos e a peça com "não quebra" não gastam. Consertar é ofício de ferreiro, fora da luta.
- A durabilidade gasta volta ao Livro de Itens a cada vez que a luta é guardada.

2.11 **Efeitos.** Uma peça só leva efeito que a luta sabe rodar, e só no tipo de peça certo:

| Efeito | O que faz | Vale em |
| --- | --- | --- |
| sangra | a ferida que ela abre sangra por cinco rodadas | arma |
| critico_19 | o 19 também é crítico | arma |
| derruba | uma vez por luta, o golpe que fere derruba (não derruba quem é maior que quem bate: 6.5) | arma |
| devolve N | quem golpeia o dono corpo a corpo leva N (o teto é 4 por degrau da categoria: Comum 4, Raro 12, Lendário 24) | armadura |
| firme | o dono não é derrubado | armadura, escudo |
| leve / pesa | pede 20 a menos / a mais de atributo | todas |
| nao_quebra | não perde durabilidade | todas |

2.12 **A janela do item** aparece na cena quando a peça nasce, muda de mão ou quebra (`python3 itens.py janela ID`).

---

## 3. A luta

3.1 **O campo** é uma linha de casas (1 casa ≈ 3 m). Cada lado tem a frente e a linha de trás. A luta começa **longe** (8 casas), **perto** (3) ou **colada** (1). O cenário é conferido antes de qualquer dado: nome repetido, tempo que não existe ou chave errada, e a luta não começa.

3.2 **A rodada.** Todos rolam a iniciativa e agem nessa ordem. No seu turno a pessoa recupera 1 de fôlego e faz as suas 2 ações (e o esforço, se quiser golpear mais uma vez). Quem foi **surpreendido** perde o turno da primeira rodada.

3.3 **As ações:**
- **golpear** quem a arma alcança (custa o fôlego da arma);
- **atirar** em quem está a 2 casas ou mais (com inimigo colado, o atirador puxa a segunda arma, ou as mãos);
- **andar** 2 casas (custa 1 de fôlego);
- **tomar fôlego** (+1d4+1, e +2 na Defesa até o próximo turno);
- **levantar-se**, **apanhar a arma**, **recarregar**, **esperar** (+2 na Defesa).

3.4 **O golpe.** 2d20 + acerto contra a Defesa.
- **Crítico:** um dado deu 20 e o outro, 11 ou mais. Acerta sempre, os dados do dano dobram e a proteção vale a metade.
- **Dois 1:** erra, e a arma perde 1 de durabilidade.
- **Onde cai** (d10): 1 cabeça · 2-3 braços · 4-7 tronco · 8-10 pernas.
- **O dano:** dado × 4 × o valor da arma ÷ a proteção da parte atingida, vezes a força do golpe.

3.5 **Mirar a fresta.** Contra armadura de categoria maior que a arma, quem golpeia pode mirar: **−8 no acerto**, e se acertar a armadura conta **uma categoria abaixo**. O script mira sozinho quando compensa (quem tem acerto de sobra mira; quem mal acerta, não). É o que o mestre faz contra o encouraçado, e é por isso que só a armadura não segura um nível muito maior.

3.6 **Distância e alcance.**
- A arma de 1 casa bate em quem está colado. A lança e a alabarda batem a 2 casas.
- **O alcance bate primeiro:** quem ENTRA no alcance de uma arma mais longa que a sua leva um golpe livre (gasta a reação de quem bate).
- **Afastar-se** de um inimigo colado dá a ele um golpe livre. No recuo, de qualquer um que esteja colado; no avanço, só de quem não está seguro por dois dos seus.
- Golpe ou tiro com alguém de pé no caminho: −2. Atirar no mesmo turno em que recuou de alguém colado: −4.
- O atirador sozinho (sem ordem) se afasta de quem colou nele e atira.

3.7 **Grupo contra grupo.**
- **O cerco:** em campo aberto, só 4 batem corpo a corpo no mesmo alvo na mesma rodada, mais 2 com arma de alcance 2, por cima do ombro.
- **O flanco:** cada um que já bateu no alvo nesta rodada tira 3 da Defesa dele para o próximo (até −9). Ser cercado mata.
- **A linha segura:** ninguém atravessa um inimigo de pé, a não ser que dois dos seus já estejam em cima de cada um daquela casa. Quem sobra **contorna** e chega à linha de trás.
- **Guardar alguém:** quem guarda fica a 1 casa do guardado e põe o corpo na frente do golpe (gasta a reação). Sem caminho até o guardado, luta como soldado.

3.8 **O lugar.**
- **Estreito** (largura N): só N de cada lado cabem em cada casa. Ninguém contorna. Quem vem atrás pode **trocar de lugar** (gasta a ação de andar) com o da frente que não vai avançar: o atirador, o caído, o sem fôlego, quem recebeu ordem de recuar ou de tomar fôlego. E quem recua troca com o de trás que quer ir para a frente.
- **Alto:** quem está no alto tem +1 no golpe e +2 no tiro; quem sobe anda 1 casa por ação.
- **Cobertura:** −4 no tiro contra quem a tem.
- **Sem saída:** quem quebra ali não foge, rende-se.

3.9 **O tempo e o chão** entram sozinhos, do dia:

| | Efeito |
| --- | --- |
| escuro | −4 no golpe, −8 no tiro |
| chuva | −4 no tiro |
| vento | −2 no tiro |
| neblina | −4 no tiro; não se atira além de 3 casas |
| lama | anda-se 1 casa por ação |
| calor | malha e placa custam 1 de fôlego a mais por rodada |
| água (pela cintura) | anda-se 1 casa; −2 na Defesa; 1 de fôlego a mais por rodada |

3.10 **Fôlego.** Cada golpe e cada passo custam. Quem **começa o turno com fôlego zero** faz uma ação só; e enquanto está a zero tem −4 no acerto e na Defesa. Quem não tem fôlego para o golpe toma fôlego.

3.11 **Posturas.** Firme (nada muda) · agressiva (+2 no acerto, −2 na Defesa; gasta o esforço até o fim do fôlego) · defensiva (−2 no acerto, +2 na Defesa, +1 de fôlego por rodada; não faz o esforço). Sem ordem, o esforço é usado enquanto sobra um terço do fôlego.

3.12 **Ferida.** Um golpe que tira um quarto do PV máximo abre uma ferida na parte atingida (o crítico abre com 5%). Com metade do PV máximo, a ferida é **grave**.

| Parte | Ferida | Grave |
| --- | --- | --- |
| cabeça | atordoado: perde 1 ação | perde 2 ações |
| braços | −2 no acerto | −4, e larga a arma |
| tronco | perde 3 de fôlego e sangra | perde 6 e sangra |
| pernas | vai ao chão | vai ao chão e não anda mais (−2 na Defesa) |

**O sangue:** a ferida do tronco, a ferida grave e a da arma que "sangra" tiram, por rodada, um quinto do golpe que as abriu, por 3 rodadas (5, se grave ou da arma que sangra). No chão: −4 na Defesa, e levantar gasta uma ação. A ferida fica depois da luta.

3.13 **Cair e morrer.** A zero de PV a pessoa cai. Se o golpe que a derrubou tirou mais da metade do PV máximo, ela morre na hora. Caída, rola 1d20 por rodada contra 12: três falhas, morre; três sucessos, fica estável. **No fim da luta,** os caídos do lado que ficou com o campo são estancados pelos seus; os outros rolam até o fim.

3.14 **Moral.** Quem não é de ferro testa a coragem (2d20 + bônus de Vontade; +2 com o líder de pé; +2 se o seu lado tem mais gente; −4 se o outro tem o dobro):

| O susto | Contra |
| --- | --- |
| viu um golpe terrível num dos seus (metade do PV de uma vez), a 2 casas | 24 |
| está abaixo de um quarto do PV | 26 |
| metade do seu lado caiu | 26 |
| o líder caiu ou fugiu | 29 |

Falhou por pouco: **fraqueja**, e segue na luta com o ânimo abalado (−2 no acerto). Falhou de novo, ou por 10 ou mais: **quebra**. Quem quebra foge (e leva um golpe livre de quem está colado), ou **se rende** se está muito ferido ou sem saída. Rendido é prisioneiro, com nome.
- **Quem fugia e leva, de costas, o golpe que o põe no chão (ou lhe prende a perna) não sai:** segue na luta, onde caiu.
- **Ninguém se rende a um bicho:** quem quebraria se rendendo foge; sem saída, fica abalado e luta.
- **Quem ficou com o campo não testa a coragem:** sem inimigo de pé, ninguém foge nem se rende.
**Quem o jogador comanda nunca foge nem se rende pelo dado:** ele fraqueja (fica abalado), a luta para, e a escolha é do jogador.

3.15 **O impasse e a retirada.** Oito rodadas seguidas sem ninguém ferir ninguém de verdade (menos de 2% do PV, somado), e os dois lados se separam. A luta que chega a 60 rodadas acaba em empate.
**Sair da luta:** quem tem ordem de recuar e acaba a rodada a 8 casas ou mais de todo inimigo de pé saiu da luta. Quem persegue anda o mesmo que quem foge: só se sai com alguém segurando a passagem, com o chão a favor, ou se o outro lado não vier atrás.

3.16 **A luta para e pergunta.** O script roda turno a turno. Quando algo muda, ele para **ali, no meio da rodada**, e mostra o quadro:
- a luta vai começar;
- alguém da casa cai, morre, foge, se rende, ou tem uma peça quebrada;
- o líder do outro lado cai ou foge, ou alguém de lá se rende;
- quem o jogador comanda é ferido, passa de metade ou de um quarto do PV, fica sem fôlego, fraqueja, perde o alvo, ou está segurando onde só apanha;
- quem o jogador mandou tomar fôlego encheu o fôlego (a ordem acabou);
- passam três rodadas sem novidade.

O jogador então dá a ordem de quem ele comanda, e a ordem do grupo (só o lado dele recebe ordem; nome ou ação que não existe é recusado, com a lista do que vale):
`atacar [alvo]` (se o alvo está longe, vai até ele, contornando se a linha deixar) · `segurar` (não anda; bate em quem chega) · `avancar` · `recuar` (mantém distância) · `folego` · `guardar NOME`, e no fim a postura.
A ordem do grupo é uma palavra: `atacar`, `segurar` ou `recuar`.
**A ordem `folego` acaba quando o fôlego enche:** daí em diante a pessoa segura (bate em quem chega), e a luta para e pergunta. Ninguém fica tomando fôlego de fôlego cheio enquanto o inimigo chega.

---

## 4. O banco de provas

Toda mudança de regra ou de número roda `python3 provas.py`. Meta que falha: a mudança não entra, ou a meta muda com a palavra do jogador.
A medição completa está em `dados/provas_saida.txt` (600 lutas por meta). **79 de 79 passam:** as 53 metas deste capítulo e as 26 dos bichos (6.14).

### Quem vence

| O que se mede | Meta | Medido |
| --- | --- | --- |
| iguais em tudo | 44 a 56% | 50% |
| mesmo nível, só a arma uma categoria acima | 85 a 100% | 95% |
| mesmo nível, o conjunto uma categoria acima | 92 a 100% | 95% |
| mesma arma, nível 75 contra 50 | 50 a 68% | 55% |
| mesma arma, nível 150 contra 50 | 80 a 100% | 88% |
| o mesmo, com a maestria igual (o nível sozinho) | 60 a 92% | 82% |
| uma categoria na arma contra 100 níveis (50 × 150) | 55 a 85% | 78% |
| uma arma uma acima, nível 50 × nível 500 | 2 a 20% | 8% |
| duas categorias na arma contra 150 níveis (50 × 200) | 85 a 100% | 94% |
| **uma arma duas acima, nível 50 × nível 500** | 45 a 75% | **63%** |
| o mesmo com o nível 40, e com o nível 60 | 25 a 75%, 45 a 80% | 59%, 67% |
| **uma arma três acima, nível 50 × nível 500** | 80 a 100% | **93%** |
| só a armadura duas acima, nível 50 × nível 500 | 1 a 45% | 7% |
| só a armadura uma acima, mesmo nível | 75 a 97% | 92% |
| só a armadura duas acima contra 100 níveis (50 × 150) | 75 a 100% | 93% |
| o conjunto duas acima (com Vontade para ele), 50 × 500 | 95 a 100% | 100% |
| **um nível 50 de conjunto Lendário × dez de nível 275 de Raro** | 85 a 100% | **92%** |
| um nível 90 de conjunto Mítico × dez de nível 275 de Raro | 90 a 100% | 100% |
| o mesmo, só com a arma Mítica (armadura Rara) | 0 a 40% | 12% |
| um nível 120 de Lendário × dez de nível 60 de Único (uma categoria abaixo) | 15 a 60% | 49% |
| o mesmo, com os dez na mesma categoria | 0 a 5% | 0% |
| o mesmo, com o um DUAS categorias acima | 90 a 100% | 100% |
| um nível 120 de Lendário × dez soldados Comuns | 97 a 100% | 100% |

**Como ler:** a arma decide mais que a armadura, e as duas juntas decidem quase tudo. O nível ajuda devagar: 100 níveis valem menos que uma categoria na arma. Contra muitos, uma categoria é moeda no ar e duas categorias no conjunto vencem.

### Quanto dura

| | Meta | Medido |
| --- | --- | --- |
| duelo entre iguais (nível 50, Raro) | 4 a 9 rodadas | 4 |
| duelo entre iguais (nível 150, Lendário) | 4 a 9 rodadas | 4 |
| cinco contra cinco | 4 a 12 rodadas | 5 |
| a luta em que o aço não passa (só a armadura duas acima, 50 × 500) | 4 a 30 rodadas | 12 |

### As armas entre si

Cada arma de guerra, com cada armadura, todas Raras, no nível 60, contra todas as outras. A meta: nenhuma montagem com média abaixo de 35% nem acima de 65%. Medido: a melhor 62% (malho e placa), a pior 36% (machado, escudo e couro). Nenhuma escolha é a única certa: o impacto vence a placa, a ponta vence a malha, o couro age primeiro, a lança manda no corredor.

### Os módulos (cada coisa que interfere, interfere para o lado certo)

| Módulo | O que se mediu |
| --- | --- |
| alcance | três lanças contra três espadas: 70% num corredor de um, 40% em campo aberto |
| distância | a arqueira contra o infante: 34% começando longe, 16% começando colada |
| tempo | a mesma arqueira: 11% na neblina, 34% com tempo limpo, 59% na lama |
| lugar | um contra quatro: 48% em campo aberto, 85% num corredor de um |
| golpe contra armadura | contra a placa: o malho 78%, o montante 46% |
| requisito | placa em quem não tem Força: Defesa 28,5 contra 36,5; fôlego 5 por rodada contra 1 |
| fôlego | quem começa o turno a zero faz uma ação só |
| sob medida | a mesma peça: +28 e × 304 no dono; +19 e × 101 na mão de outro |
| sintonia | o conjunto Épico contra três de nível 100: 62% com Vontade para as quatro peças, 20% sem |
| parte do corpo | o mesmo guerreiro sem o elmo, contra o de elmo: 32% |
| durabilidade | o mestre de nível 300 com espada Comum quebra a espada na armadura Única em 98% das lutas |
| impasse | espada Comum contra armadura Épica dos dois lados: os lados se separam em 100% |
| moral | seis contra um muito mais forte: alguém foge ou se rende em 42% das lutas; quem o jogador comanda, nunca |
| cerco e contorno | dez contra um: 4 batem por rodada; sete contra uma linha de um: os que sobram chegam em quem está atrás em 100% |
| para e pergunta | para antes da 1ª rodada; cumpre a ordem; em 95% das lutas houve parada no meio da rodada |
| a ordem de fôlego | 60 lutas com a ordem dada de fôlego cheio e o inimigo longe: nenhuma ação gasta tomando fôlego à toa; a luta parou e avisou nas 60 |
| o registro na ordem | 120 lutas de um lanceiro contra dois de adaga, 95 golpes de "o alcance bate primeiro": em nenhuma a linha do passo veio depois do golpe (ninguém avança, no registro, depois de cair ou de morrer) |
| retirada | com dois guardas segurando o corredor, quem recebe ordem de recuar sai da luta em 100% |
| cenário conferido | nome repetido e tempo que não existe: recusado antes de qualquer dado |

---

## 5. O mundo: o tempo, o corpo, o estado e o turno (etapa 1)

Os números deste capítulo moram no `tabelas_mundo.py`; as provas, no `provas_mundo.py` (as 12 da etapa 1 e as 13 que a etapa 2 pôs no alicerce: 25 de 25).

5.1 **O tempo.** O dia tem 6 blocos de 4 horas: madrugada, alvorada, manhã, tarde, entardecer, noite. Semana de 7 dias, estação de 91, ano de 364. Todo ato custa blocos. A madrugada e a noite são escuras: a luta ao ar livre ganha "escuro" sozinha.

5.2 **O corpo** tem três medidores, de 0 a 10:

| | Sobe | Desce | Cobra |
| --- | --- | --- | --- |
| Fome | +1 a cada 2 blocos | refeição −3 (1 de prata) | em 4: −2; em 7: −4, e 5% do PV máximo a cada virada do dia |
| Sono | +1 por bloco acordado | −3 por bloco na cama; −2 no chão | em 6: −2; em 8: −4, e Vontade contra 28 a cada bloco, ou **dorme ali mesmo**, no chão, até o sono baixar de 6 |
| Cansaço | bloco pesado +2, leve +1, luta +2 | −3 por bloco na cama; −2 no chão; −1 descansando | cada 3 pontos tiram 1 do fôlego máximo; em 9: −2 |

**A pena do corpo** é a pior das três (não somam) e entra em todo teste, no acerto e na Defesa. O mesmo homem, com sono 8 e cansaço 9, vence a si mesmo descansado em 23% das lutas.

5.3 **Curar.** Cada bloco dormido sem fome (abaixo de 4) devolve 5% do PV máximo, em no máximo dois blocos por dia: um décimo por noite. A ferida sara com **7 dias de repouso**; a grave, com **21**. Dia com dois blocos pesados não conta como repouso. Estar ferido custa: quem não trabalha não ganha.

5.4 **Viver.** Refeição 1 de prata; cama 2 por noite. O diarista ganha 2 por bloco. Uma refeição por dia segura a fome.
- **A cama é por noite, não por deitada.** A cama paga vale 6 blocos (um dia inteiro) a contar do bloco em que se pagou, no lugar onde se pagou. Dormir de novo nesse prazo não cobra. Passado o prazo, ou em outro lugar, paga-se outra. O sono que atravessa o prazo paga a noite seguinte; sem prata para ela, a pessoa acorda ali. A `MESA.md` diz até quando a cama está paga.
- **Quem não tem fome não come:** com a fome em zero a refeição é recusada, e nada é cobrado.
- **A jornada são 2 blocos pagos por dia.** O lugar não paga mais que isso a ninguém: o terceiro bloco é recusado. O `ato.py trabalhar` e o jornal da oficina (7.12) contam juntos. Sobra 1 de prata por dia ao diarista.
- **O lugar paga com a prata dele** (8.6). Sem prata, não há serviço pago, e o comando diz isso.
- **Quem carrega comida come da própria carga,** sem pagar: 1 de comida, fome −3 (`ato.py comer carga`).

| Grau de ofício | Por bloco | Por dia (a jornada) |
| --- | --- | --- |
| diarista | 2 | 4 |
| aprendiz | 3 | 6 |
| oficial | 6 | 12 |
| mestre | 10 | 20 |

**O grau de ofício** é o posto da pessoa no lugar. Decide o salário do `ato.py trabalhar` e o esforço do bloco (pesado para o diarista e o aprendiz; leve para o oficial e o mestre). Não sobe sozinho: é o Mestre que o dá em cena, por evento (`estado.py mestre '[["pessoa","eu","grau_oficio","poe","oficial"]]' "o que houve"`). Na bancada, o jornal paga pelo que a mão vale, e nunca menos que o posto (7.12).

5.5 **Treinar.** Bloco de treino é pesado. A maestria numa arma sobe aos 40 blocos (Iniciante), 160 (Treinado), 500 (Mestre) e 1.500 (Lendário). De Mestre para cima, os blocos não bastam: é preciso um **feito** com a arma, que o mundo registra.

5.6 **O ato longo para.** Dormir, trabalhar, treinar ou esperar vários blocos para quando o corpo cruza um limiar (fome, sono, cansaço), e diz por quê. Quem cai no sono (5.2) dorme onde está, e esses blocos passam.

5.7 **O estado e o gravador único.** O save é uma pasta com o relógio, os lugares, a gente, o Livro de Itens, o caderno do turno e o registro de eventos. **Só `estado.aplica()` muda o mundo.** Um evento sem efeito é recusado: o que não muda número não aconteceu. O evento cujos efeitos não mudam nada (somar no que já está no teto) não entra no registro. Um evento com um efeito errado é recusado inteiro: nada muda pela metade. Cada fato mora num lugar só (o dono de uma peça, só no Livro de Itens). O que o Mestre inventa em cena entra por um evento "mestre", com os mesmos efeitos (`estado.py mestre`).
- **Lugar e gente nascem por evento** (`gera` ou `mestre`), com nome, nível, atributos e lugar; o resto tem padrão.
- **O que é conta só aceita número, na faixa dele:** a contagem dos bichos, a matéria do ermo, o povo, a oficina, o alvo de peças da loja (8.8), a carga (inteira, e só dos bens que existem).
- **O item sem dono está num lugar.** Ali ele é da loja (8.8), a não ser que esteja **solto**: caído no chão, de quem achar (9.10).
- **Os invariantes** (`estado.py valida`) cobrem também a obra, o núcleo, o ermo, o lugar e a saída de caça. O `fecha` recusa o turno com qualquer um quebrado.

5.8 **O dado de quem está em cena** (`teste.py`): 2d20 + bônus do atributo + a pena do corpo, contra um número. O comando declara e rola no mesmo passo, uma vez, e o resultado fica escrito no turno. A rolagem oculta aparece na mesa só como "rolagem oculta"; a verdade vai para a parte do Mestre.

5.9 **A luta dentro do mundo** (`ato.py luta`). Quem tem ficha no mundo entra com o que veste hoje, o PV, as feridas e a pena do corpo. Acabada, a luta volta ao estado num evento só: PV, feridas novas, mortes, o cansaço e a durabilidade das peças. O save guarda o caminho do arquivo da luta relativo à pasta dele: a pasta pode mudar de lugar.
- **O arquivo da luta fica dentro do save.** No `ato.py luta nova CENARIO.json LUTA.json`, o segundo nome dito sem pasta fica na pasta do save, em `lutas/` (criada se faltar), como as lutas da caça. Dito com pasta, fica onde se disse: se a pasta não existe, a recusa é uma frase; se fica fora do save, o comando avisa que a luta não vai junto se o save mudar de lugar. O `luta roda` e o `luta larga` acham a luta só pelo nome.
- **Com uma luta aberta, o mundo não anda.** Até ela acabar, nenhum ato que mexe no mundo é aceito, de ninguém: nem dormir, nem comer, nem trabalhar, nem negociar, nem forjar, nem sair para caçar, nem abrir outra luta. O relógio fica parado.
- **Valem só a própria luta e a mão do Mestre:** `ato.py luta roda` (na caça, `caca.py luta`, com as contas no fim) e `estado.py mestre`. O dado de cena (`teste.py`) e as perguntas e notas do turno também valem: não mexem no mundo.
- **A recusa diz como sair:** como seguir a luta, e como o Mestre a solta se o arquivo se perdeu ou a cena mudou (`ato.py luta larga`; na caça, `caca.py larga`). A `MESA.md` abre com o aviso.

5.10 **O turno em dois comandos.**
- `turno.py abre` só lê e gera a `MESA.md`: você, o lugar, o que dá para fazer e o que custa, as perguntas abertas, e o SÓ O MESTRE.
- `turno.py responde "1a.2b"` confere cada código contra as perguntas abertas. Código que não bate é recusado, e nada é marcado. **Cada pergunta guarda o número com que foi aberta até o turno fechar:** responder a 1 não faz da 2 a nova 1. A pergunta já respondida recusa segunda resposta. A pergunta aberta no meio do turno ganha o número seguinte. No fechar, as que ficam são numeradas de novo, de 1 em diante: é com esse número que o `RETOMAR.md` as mostra.
- `turno.py fecha "o que houve"` **recusa** se: há luta aberta · há menos de 2 perguntas abertas · o relógio não andou (a não ser que se diga `parado`) · o estado quebrou um invariante. Passando, gera o `RETOMAR.md` (o agora, o que houve, os fatos do registro, a saída de caça que ficou aberta, as perguntas, o que só o Mestre sabe) e a `MESA.md` nova. Com `git`, guarda e envia, e avisa se o envio falhou.
- **O `RETOMAR.md` nunca corta calado.** O que se repete todo dia (comer, dormir, a cama, descansar, esperar) vira uma linha por dia. O mesmo fato repetido no dia vira uma linha, com a conta. O mundo andando sozinho (o dia que vira, o lugar que produz e consome, o ermo que se refaz) e o mundo nascendo não são fato do turno; a morte de alguém sempre é. Se ainda assim os fatos passam de 40 linhas, ficam as mais novas, e a primeira diz quantas ficaram de fora e como lê-las (`estado.py eventos N`). O evento gravado sem texto entra assim mesmo, com o número e o tipo dele. E o `estado.py mestre` recusa o texto vazio: o que o Mestre decide em cena vai para o registro com o que houve.

5.11 **A morte.** Todo mundo morre de vez. A regra é uma só, para a fome, a luta e a mão do Mestre: **o morto não fica com nada.**
- As peças dele (as vestidas, as guardadas e os núcleos) caem **soltas** onde ele morreu, com a história escrita e a marca de quem eram (`corpo`).
- As obras dele se desfazem: a matéria se perde; o núcleo cai com o resto.
- A carga e a prata ficam no estoque do lugar onde ele morreu. Num lugar com povo, o povo fica com elas. No ermo, ficam no chão, junto do corpo.
- **O que era de um morto não muda de mão sozinho.** Na vila ou no ermo, quem fica com as peças, a carga e a prata é decisão de cena: o Mestre registra por evento (`itens.py dono ITEM PESSOA`, `estado.py mestre`). No ermo, quem passa num rastro acha o corpo e lê o que ficou com ele (9.10), e mais nada. A família, o guarda e a herança são da etapa 6.
- **Morto não age:** todo ato dele é recusado antes de cobrar qualquer coisa. A `MESA.md` e o `RETOMAR.md` abrem dizendo quando e onde ele morreu, sem a lista de atos. O turno fecha. O herdeiro é da etapa 6.

5.12 **Fora.** Quem saiu para o ermo (9.2) está lá, não no lugar onde mora, até voltar. Os atos da vila (dormir na pousada, trabalhar, treinar, comprar, vender, forjar, consertar) são recusados, para quem comanda a saída e para quem foi junto. No ermo come-se da própria carga.

5.13 **Vestir e guardar.** `ato.py vestir ITEM` empunha ou veste uma peça da pessoa; `ato.py tirar ITEM` a guarda. Não gasta bloco, e não se faz no meio de uma luta.
- A arma vai na mão (`arma`) ou de reserva (`arma2`); o escudo, no braço; a armadura, no corpo.
- A peça que estava no mesmo lugar vai para a guarda: a outra arma, o outro escudo, a armadura que cobre a mesma parte.
- A peça comprada, forjada ou achada chega **guardada**. A ficha de luta só conta o que está em uso.

---

## 6. Os bichos (etapa 2)

Os números moram no `tabelas_bichos.py`; as provas, no `provas.py` (o bloco OS BICHOS). A luta é a do capítulo 3, sem tirar nada: o `luta.py` roda o bicho como roda gente.

6.1 **O bicho é uma ficha de luta.** Tem os seis atributos, nível e **instinto**, que é a maestria dele (Leigo 0 a Lendário 8) e vale tudo o que a maestria vale: acerto, Defesa, a ação a mais, as reações. As contas são as do capítulo 1. Muda só o que vem do corpo e do tamanho:

| | Conta |
| --- | --- |
| PV | (Vigor × 2 + nível ÷ 4) × o do tamanho |
| Acerto | instinto + (bônus de Força + bônus de Agilidade) ÷ 4 + o bônus da categoria do corpo |
| Defesa | 22 + bônus de Agilidade ÷ 2 + instinto ÷ 2 + a do couro + a do tamanho + o bônus da categoria do corpo (o corpo apara) |
| Fôlego, força do golpe, ações, reações, iniciativa | como gente (a iniciativa leva a do couro) |

6.2 **O corpo é a arma.** O valor (× 1, 3, 9, 27...) e o bônus de acerto saem da **categoria do corpo**; o alcance, do tamanho. A regra de ouro (2.3) vale igual: conta a diferença entre a arma de quem bate e a armadura de quem apanha. O golpe do corpo entra na tabela do golpe contra o material (2.6) como o de qualquer arma. Quem tem mais de uma arma alterna, golpe a golpe.

| Arma do corpo | Dado | Golpe | Fôlego |
| --- | --- | --- | --- |
| dente | 1d4 | ponta | 1 |
| casco | 1d4 | impacto | 1 |
| presa, ferrão | 1d6 | ponta | 1 |
| garra | 1d8 | corte | 1 |
| chifre | 1d10 | ponta | 2 |
| cauda | 1d10 | impacto | 2 |
| bocarra | 1d12 | ponta | 2 |

6.3 **O corpo é a armadura.** Cobre o corpo todo, a cabeça também. Vale como um material de armadura da categoria do corpo, sem pedir Força, sem custar fôlego e sem esquentar no calor:

| Couro | Vale como | Proteção | Defesa | Iniciativa |
| --- | --- | --- | --- | --- |
| pelo | couro | 0,7 do valor | +3 | +2 |
| escama | malha | o valor | 0 | 0 |
| carapaça | placa | 1,4 do valor | −2 | −2 |

Mirar a fresta (3.5) vale contra o bicho de categoria maior que a arma, menos contra o de couraça.

6.4 **O corpo não é peça.** Não está no Livro de Itens, não tem dono, não quebra, não gasta e não ocupa sintonia. O bicho ferido no braço não larga arma nenhuma.
**Mas o aço gasta nele** (2.10): a arma de categoria menor que o corpo, aparada por ele, perde 1; o golpe que não tira nada gasta a arma; a armadura de quem apanha de um corpo de categoria maior gasta.

6.5 **O tamanho.**

| Tamanho | PV | Alcança | Batem nele por rodada (de perto · de haste) | Toma de um corredor | Defesa |
| --- | --- | --- | --- | --- | --- |
| pequeno | × 0,6 | 1 casa | 2 · 1 | meia vaga | +2 |
| médio (e gente) | × 1 | 1 casa | 4 · 2 | 1 vaga | 0 |
| grande | × 1,5 | 2 casas | 6 · 3 | 2 vagas | −2 |
| enorme | × 2,5 | 3 casas | 8 · 4 | 3 vagas | −4 |

- **O alcance bate primeiro** (3.6): o grande e o enorme dão o golpe livre em quem entra no alcance deles com arma mais curta.
- **Apertado:** o bicho que toma mais vagas do que o corredor tem fica sozinho na casa e luta com −2 no acerto e na Defesa por vaga que falta. Dois pequenos cabem numa vaga.
- **Ninguém derruba nem agarra quem é maior que ele.** Vale para os traços e para o efeito "derruba" das armas. A ferida na perna (3.12) derruba qualquer um.
- Num corredor, só troca de lugar quem toma o mesmo tanto.

6.6 **Os traços.** A lista é fechada: são dez, e a luta roda todos. Traço fora da lista é recusado antes de qualquer dado.

| Traço | O que faz |
| --- | --- |
| matilha | O golpe que fere um alvo em que outro da matilha já bateu nesta rodada o derruba. Com outro da matilha de pé, +4 na coragem. |
| bote | Na primeira rodada, +20 na iniciativa. O primeiro golpe dele na luta tem +8 e rola os dados 3 vezes; quem ele ferir vai ao chão e perde 1 ação. |
| investida | O golpe dado depois de correr 2 casas ou mais desde o último tem +8, rola os dados 3 vezes e derruba quem ferir. |
| veneno | O golpe do corpo que fere envenena: por 4 rodadas a vítima perde, no fim de cada uma, metade do que o golpe tirou, e tem −2 no acerto. Não acumula: vale a pior mordida, e o prazo recomeça. O que sobra corre depois da luta: deixa por um fio (1 de PV), mas sozinho não mata. |
| agarra | O golpe que fere quem está **colado** agarra (um de cada vez). O agarrado não anda, não recua, não troca de lugar, e tem −4 no acerto e −4 na Defesa. O bicho bate primeiro em quem agarrou, e só solta quando passa um turno sem feri-lo, cai, foge ou se afasta. |
| voa | Arma de alcance 1 tem −6 contra ele. A linha não o segura, não leva golpe livre ao se afastar nem ao fugir, e não pisa a lama nem a água. Num corredor, no chão ou agarrado, não voa. |
| regenera | No começo de cada turno dele, recupera 15% do PV máximo. |
| apavora | Quando a luta começa, quem não é de ferro, do outro lado, testa a coragem contra 28 (3.14). |
| couraça | Não tem fresta: ninguém mira a fresta nele, e o crítico não corta a proteção dele pela metade. |
| sopro | Uma rodada sim, uma não, por 3 de fôlego: um ataque em cada inimigo a até 4 casas, de 1d8 com o valor da categoria do corpo e força fixa de 1,2. Não se apara (conta só a Defesa sem escudo e sem arma), não olha o material da armadura, e ninguém se põe na frente. O tempo e a cobertura valem como num tiro. O bicho sopra quando pega dois ou mais, ou quando não alcança ninguém de outro jeito. |

6.7 **A moral do bicho.** O bicho não fica abalado nem se rende: **luta ou foge.**
Testa 2d20 + bônus de Vontade + a coragem da espécie (+2 com o alfa de pé; +2 se o lado dele tem mais gente de pé; −4 se o outro tem o dobro; +4 da matilha):

| O susto | Contra |
| --- | --- |
| levou a primeira ferida (3.12) | 26 |
| está abaixo de um quarto do PV | 26 |
| viu um golpe terrível num do bando, a 2 casas | 24 |
| metade do lado dele caiu | 26 |
| o alfa caiu ou fugiu | 29 |

Cada susto testa uma vez por luta; o golpe terrível, uma vez em cada rodada em que acontece.

- **Falhou, foge:** sai da luta, e leva um golpe livre de quem o alcança (quem voa, não).
- **Quem não anda não foge.** O bicho que está no chão não testa: o susto fica para quando ele se levantar. O que levou, de costas, o golpe que o pôs no chão não sai: segue na luta. O de perna presa (a ferida grave nas pernas, 3.12) vale como encurralado.
- **Encurralado** (o lado dele não tem saída, ou ele não tem pernas para correr): não foge. Na primeira falha fica encurralado e luta até o fim, com +2 no acerto.
- **O chefe não testa.**
- **Ninguém se rende a um bicho:** quem quebraria se rendendo (3.14) foge; sem saída, fica abalado e luta.
- **Quem ficou com o campo não testa a coragem:** sem inimigo de pé, ninguém foge nem se rende. (Vale para gente também.)

6.8 **O grau** é o que o caçador lê. Casa com a categoria do corpo, e fala de **um** bicho contra um homem do mesmo degrau (o conjunto da categoria do bicho).
**O bando pesa mais:** para quem está sozinho, **2 ou 3 juntos valem um grau acima; 4 ou mais, dois graus acima.** Duas corças valem grau E; quatro lobos, grau B.

| Grau | Categoria | O que diz |
| --- | --- | --- |
| F | Comum | presa: sozinha quase nunca derruba um homem armado, mas o golpe de sorte abre ferida |
| E | Comum | perigo de morte para quem está sozinho com peças Comuns |
| D | Incomum | perigo de morte para um homem armado, mesmo com peças Incomuns |
| C | Raro | mata um veterano |
| B | Épico | pede um grupo |
| A | Único | pede um grupo de mestres |
| S | Lendário | calamidade |

6.9 **As espécies** (catorze; cada uma é uma linha do `tabelas_bichos.py`).

| Espécie | Grau | Categoria | Tamanho | Nível | Instinto | O corpo: armas · couro | Traços | Coragem | Anda | Onde vive |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ratazana | F | Comum | pequeno | 3 | Leigo | dente · pelo | matilha | −2 | 3 a 6 | brejo, ruína, caverna |
| corça | F | Comum | médio | 4 | Leigo | casco · pelo | — | −6 | 1 a 2 | floresta, campo |
| javali | E | Comum | médio | 10 | Leigo | presa · pelo | investida | +4 | só | floresta, brejo |
| lobo | D | Incomum | médio | 20 | Iniciante | presa · pelo | matilha | 0 | 3 a 5, com alfa | floresta, serra, campo |
| surucucu | D | Incomum | médio | 25 | Iniciante | dente · escama | bote, veneno | +2 | só | brejo, floresta, ruína |
| urso | D | Incomum | grande | 35 | Treinado | garra, presa · pelo | agarra | +2 | só | floresta, serra, caverna |
| aranha-de-toca | C | Raro | médio | 45 | Iniciante | ferrão · carapaça | veneno | +2 | 2 a 3 | caverna, ruína, floresta |
| pantera | C | Raro | médio | 50 | Mestre | garra, presa · pelo | bote | +4 | só | floresta, serra |
| grifo | C | Raro | grande | 55 | Mestre | garra, presa · pelo | voa | +2 | 1 a 2 | serra |
| trasgo | C | Raro | grande | 55 | Iniciante | garra · pelo | regenera | +2 | só | brejo, caverna, ruína |
| basilisco | B | Épico | grande | 90 | Mestre | presa, cauda · escama | couraça, veneno | +4 | só | ruína, caverna, brejo |
| serpe | B | Épico | enorme | 100 | Treinado | bocarra, cauda · escama | sopro, veneno | chefe | só | serra, ruína |
| hidra | A | Único | enorme | 150 | Mestre | bocarra · escama | regenera, veneno, apavora | chefe | só | brejo, ruína |
| dragão | S | Lendário | enorme | 220 | Lendário | garra, bocarra, cauda · escama | voa, sopro, couraça, apavora | chefe | só | serra, ruína |

Na tabela e no cenário, a aranha-de-toca é `aranha` (o comando aceita os dois nomes).

A ficha que sai da conta, e o que o bicho inteiro rende:

| Espécie | Força · Agilidade · Vigor · Vontade · Percepção | PV | Fôlego | Acerto | Defesa | Golpe (dado × valor) | Despojo |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ratazana | 35 · 70 · 35 · 30 · 55 | 42 | 9 | +2,5 | 30,5 | 1d4 × 1 | 1 de comida, 1 de couro Comum |
| corça | 45 · 70 · 45 · 30 · 70 | 91 | 10 | +2,75 | 28,5 | 1d4 × 1 | 6 de comida, 2 de couro Comum, 1 de osso Comum |
| javali | 70 · 50 · 100 · 50 · 45 | 202 | 16 | +3 | 27,5 | 1d6 × 1 | 6 de comida, 2 de couro Comum, 2 de osso Comum |
| lobo | 60 · 75 · 40 · 40 · 70 | 85 | 10 | +9,25 | 33,5 | 1d6 × 3 | 3 de comida, 2 de couro Incomum, 1 de osso Incomum |
| surucucu | 60 · 90 · 60 · 40 · 70 | 126 | 12 | +9,75 | 31,5 | 1d4 × 3 | 2 de comida, 2 de couro Incomum, 1 de osso Incomum |
| urso | 100 · 50 · 80 · 50 · 50 | 252 | 14 | +11,75 | 31,5 | 1d8 × 3 · 1d6 × 3 | 10 de comida, 4 de couro Incomum, 2 de osso Incomum |
| aranha-de-toca | 50 · 80 · 40 · 40 · 60 | 91 | 10 | +13,25 | 33 | 1d6 × 9 | 1 de couro Raro, 1 de osso Raro |
| pantera | 100 · 95 · 100 · 50 · 80 | 212 | 16 | +18,75 | 40,5 | 1d8 × 9 · 1d6 × 9 | 4 de comida, 2 de couro Raro, 1 de osso Raro |
| grifo | 95 · 85 · 85 · 55 · 90 | 274 | 14 | +18,25 | 38 | 1d8 × 9 · 1d6 × 9 | 6 de comida, 2 de couro Raro, 2 de osso Raro |
| trasgo | 80 · 45 · 105 · 50 · 40 | 334 | 16 | +13 | 34 | 1d8 × 9 | 3 de couro Raro, 3 de osso Raro |
| basilisco | 100 · 65 · 100 · 60 · 60 | 333 | 16 | +22 | 38 | 1d6 × 27 · 1d10 × 27 | 5 de couro Raro, 4 de osso Raro |
| serpe | 85 · 60 · 75 · 70 · 70 | 437 | 13 | +19,5 | 35 | 1d12 × 27 · 1d10 × 27 · sopro 1d8 × 27 | 12 de comida, 6 de couro Raro, 5 de osso Raro e **um núcleo Épico** |
| hidra | 120 · 55 · 110 · 80 · 70 | 642 | 17 | +26,25 | 39,5 | 1d12 × 81 | 8 de couro Raro, 6 de osso Raro e **um núcleo Único** |
| dragão | 180 · 70 · 240 · 100 · 90 | 1.337 | 30 | +34,25 | 45,5 | 1d8, 1d12, 1d10 × 243 · sopro 1d8 × 243 | 12 de couro Raro, 10 de osso Raro e **um núcleo Lendário** |

6.10 **O bando.** Quantos andam juntos sai do acaso do mundo, entre os dois números da espécie. No bando de alfa (o lobo), o primeiro é o líder: caído ou fugido ele, os outros testam a coragem contra 29.

6.11 **O despojo** sai da tabela: de cada bem, **de metade (arredondada para cima) ao inteiro**, pelo acaso do mundo. A matéria tem a categoria do bicho, até o Raro; do Épico para cima, o corpo rende matéria Rara.
**Só o chefe dá núcleo:** sempre um, da categoria dele. O núcleo é item do Livro de Itens (2.1; tipo `nucleo`), com a espécie de que veio, e nasce por evento, com dono ou com lugar. Não se veste, não gasta e não se vende em loja.
Rende despojo o bicho que ficou no campo de quem venceu, morto ou caído. O que fugiu não rende. Tirar o bicho da contagem do ermo e pôr o despojo na carga é ato da caça, por evento.

6.12 **A ameaça** é a frase que o caçador lê **antes** da luta (`bichos.ameaca`). Diz: o grau e o que ele quer dizer; a categoria; o tamanho e o que ele muda; quantos são; o corpo; cada traço, com os números; o que se sabe da espécie; se foge ou se é chefe; e a conta da regra de ouro. Com a categoria da arma e da armadura de quem lê, a conta já vem feita.
Da espécie que anda em bando, avisa que o grau é o de um só, quanto vale o bando (6.8), quantos batem num homem por rodada e o que o corredor muda. Do bicho pequeno, avisa que o traço dele não derruba nem agarra gente.

6.13 **No cenário da luta** (`luta.py nova`, `ato.py luta nova`), um bicho é `{"nome": "lobo 1", "nivel": 0, "bicho": "lobo"}`: a espécie inteira sai da tabela. O Mestre monta o bicho fora do comum com `bichos.bicho(espécie, tamanho=..., cat=..., tracos=[...])`.
O bicho não tem ficha no mundo: a luta que volta ao estado (5.9) não o grava, e a contagem do ermo não muda sozinha.
Na `MESA.md` (`bichos.mesa`), cada espécie contada no lugar do personagem ou num vizinho aparece uma vez, com o resumo dela: sem a contagem e sem os chefes.
No registro da luta, o golpe que cai nos braços ou nas pernas de um bicho é dito "patas da frente" e "patas de trás"; a regra é a mesma (3.4).

6.14 **Medido** (`python3 provas.py`, 600 lutas por meta; o bloco OS BICHOS: 26 de 26).

| O que se mede | Meta | Medido |
| --- | --- | --- |
| um nível 50, tudo Raro, contra a pantera (Rara, média, sozinha) | 40 a 60% | 46% |
| o mesmo homem com a arma uma categoria acima vence; com uma abaixo, perde | 80% ou mais | 87% e 92% |
| quatro lobos contra um nível 30 de conjunto Incomum: em campo aberto, e num corredor de um | 10 a 35%; 20 pontos a mais | 14% e 69% |
| a serpe contra quatro de nível 60: de conjunto Raro, e de conjunto Épico | 5 a 30%; 55 a 90% | 24% e 66% |
| o tamanho (pequeno, médio, grande, enorme): PV · alcance · quantos batem nele | para o lado certo | 100, 168, 252, 420 · 1, 1, 2, 3 casas · 2, 4, 6, 8 |
| cada traço, com ele e sem ele | 8 pontos ou mais | de 11 (agarra) a 34 (veneno) |
| o bicho comum ferido foge das lutas que perde | 30% ou mais | 32% |
| o encurralado e o chefe fogem; alguém se rende a um bicho | nunca | 0, 0 e 0 vezes |
| o bicho no chão ou de perna presa foge | nunca | 0 de 720 fugas (o golpe pelas costas segurou 26) |
| a luta de um contra um bicho do mesmo degrau (mediana) | 3 a 9 rodadas | de 3 a 5 |

Em B4, o conjunto Épico é o de gente gerada: no nível 60 a Vontade sustenta duas peças Épicas (2.9), e a armadura dorme. Com Vontade 80, os quatro vencem a serpe em 100%.
**A régua** (`bichos.py mede ESPECIE NIVEL CATEGORIA`) mede qualquer encontro em lutas de ensaio, sem guardar nada. O que ela mostra: na mesma categoria, o bicho sozinho de grau D ou C é moeda no ar, e o bando mata; com o conjunto uma categoria acima, o homem vence quase sempre; do grau B para cima, um homem só não basta.
**O teste de estresse** (`python3 estresse.py 1500`): 1.500 lutas ao acaso, 712 com bichos misturados, nenhum erro e nenhum invariante quebrado.

---

## 7. O ofício (etapa 2)

Os números moram no `tabelas_oficio.py`; as provas, no `provas_oficio.py`. O comando é o `oficio.py`. Tudo entra por evento, e a prata só muda de mão. Quem está fora (5.12) não trabalha na bancada.

7.1 **A oficina.** Forjar, consertar e ajustar pedem uma oficina no lugar (`lugar.oficina`, de 0 a 4). Lugar sem o campo não tem oficina. O nível soma no teste.

| Nível | Oficina | Soma no teste | O ferreiro do lugar conserta (pago) até |
| --- | --- | --- | --- |
| 0 | bancada | 0 | Incomum |
| 1 | forja de vila | +1 | Raro |
| 2 | forja de cidade | +2 | Épico |
| 3 | grande forja | +3 | Único |
| 4 | forja mestra | +4 | Lendário |

7.2 **A bancada.** Bloco de bancada é bloco **pesado**: um bloco de forjar, de consertar, de ajustar ou de jornal. Cada um soma 1 ao treino do ofício.
Há dois ofícios de bancada: **forja** (armas, malha, placa, escudos) e **couro** (a armadura de couro). Cada um tem a sua maestria.

7.3 **Forjar.** Sem requisito de nível e sem tranca de maestria: quem tem a matéria e uma oficina pode abrir a obra.

| Categoria | Blocos de bancada | O teste é contra | Matéria | A mão que a obra pede |
| --- | --- | --- | --- | --- |
| Comum | 1 | 28 | da categoria | Leigo |
| Incomum | 3 | 34 | da categoria | Leigo |
| Raro | 9 | 40 | da categoria | Iniciante |
| Épico | 27 | 46 | matéria Rara e um **núcleo** Épico | Treinado |
| Único | 81 | 52 | matéria Rara e um núcleo Único | Mestre |
| Lendário | 243 | 58 | matéria Rara e um núcleo Lendário | Lendário |

- **O teste final** é um só, no último bloco: **2d20 + maestria do ofício + Afinidade ÷ 10 + a oficina (0 a 4) + o preparo (até +8)**, contra **28 + 6 por categoria**. A pena do corpo entra, como em todo teste.
- **A mão que a obra pede** é conselho, não tranca: abaixo dela a conta quase não fecha, e o comando avisa antes de abrir. (Para consertar sozinho, ela é o que se pede: 7.10.)
- **O núcleo** é item do Livro de Itens (tipo `nucleo`), da categoria da obra, na mão de quem forja. Um núcleo só entra numa obra por vez.
- Acima do Lendário ninguém forja (ainda).

7.4 **A matéria de cada peça** (na categoria da obra; do Épico para cima, matéria Rara):

| Peça | Matéria |
| --- | --- |
| adaga | 1 de metal |
| espada, maça | 3 de metal |
| machado | 2 de metal, 1 de madeira |
| martelo | 3 de metal, 1 de madeira |
| lança | 1 de metal, 2 de madeira |
| montante | 5 de metal |
| alabarda | 3 de metal, 2 de madeira |
| malho | 4 de metal, 1 de madeira |
| arco | 3 de madeira |
| besta | 3 de madeira, 1 de metal |
| escudo | 2 de madeira, 1 de metal |
| armadura de couro (corpo · elmo) | 4 · 1 de couro |
| armadura de malha (corpo · elmo) | 4 · 1 de metal |
| armadura de placa (corpo · elmo) | 8 · 2 de metal |

A armadura gasta por parte coberta: tronco 2, braços 1, pernas 1, cabeça 1 (a placa, o dobro).
É por esta mesma tabela que a arma e o escudo valem na loja: pelas unidades de matéria que levam (8.8).

7.5 **A obra fica aberta.** A matéria sai da carga e entra na obra **quando ela abre**. Os blocos somam de um dia para o outro; a obra mora no estado e sobrevive a fechar o turno.
O ato de trabalhar para quando o corpo cruza um limiar (5.6). O teste só sai quando os blocos fecham. Trabalha-se na oficina onde a obra abriu.
**Largar a obra:** com zero blocos, a matéria volta; com um bloco ou mais, a matéria se perde. O núcleo fica com o dono: só o teste o gasta.
A obra de quem morreu se desfaz na hora (5.11): a matéria se perde, e o núcleo que estava nela cai solto com o resto do que era dele.

7.6 **Falhar custa.**

| O teste | O que sai |
| --- | --- |
| passa | a peça, na categoria da obra |
| falha por 1 a 4 | a peça **uma categoria abaixo** (o núcleo se gasta nela). O Comum sai **tosco**: Comum, com metade da durabilidade |
| falha por 5 ou mais | nada: **a matéria some, e o núcleo sai do Livro de Itens** |

7.7 **A peça nasce no Livro de Itens** por evento, com o dono (quem forjou), `feito_por`, o dia, e a primeira linha da história dela (quem, onde, com que núcleo).

7.8 **O preparo** é ganho no mundo. São quatro, **+2 cada um, até +8**: a **receita** e o **ajudante** (da pessoa), o **fogo** e a **bigorna** (do lugar).
Cada preparo tem **alcance**: a categoria mais alta a que ele serve. Só soma na obra que ele alcança: a receita Comum não ajuda numa peça Rara.
Nesta etapa o preparo é uma marca; o Mestre o registra quando ele é ganho em cena (`oficio.py preparo fogo Raro "como foi"`).
Sugestão para quem gera o mundo (não é regra): o fogo e a bigorna de uma forja de vila alcançam o Incomum; os de cidade, o Raro; os da grande forja, o Épico; os da forja mestra, o Único. O alcance Lendário só se ganha em cena.

7.9 **A maestria do ofício** sobe por blocos de bancada, como a das armas sobe por blocos de treino:

| Grau | Blocos de bancada | E um feito |
| --- | --- | --- |
| Iniciante | 50 | |
| Treinado | 150 | |
| Mestre | 375 | uma obra Épica (ou melhor) nascida da sua mão |
| Lendário | 1.000 | uma obra Única (ou melhor) nascida da sua mão |

A peça que sai uma categoria abaixo conta como obra da categoria em que saiu.

7.10 **Consertar** devolve durabilidade a uma peça sua. Não tem teste.
- **Você, na bancada:** 5 pontos por bloco, e 1 de matéria principal da peça (metal, couro ou madeira, na categoria dela; Rara, do Épico para cima) a cada 10 pontos ou parte. Pede a mão que a categoria pede (7.3).
- **Pago ao ferreiro do lugar:** **2% do preço da peça por ponto**, em prata inteira, que vai para o estoque do lugar; um bloco de espera a cada 10 pontos ou parte. A oficina conserta até a categoria do nível dela mais um (7.1). O preço da peça segue o tamanho dela (8.8): a armadura, o que cobre (consertar um elmo custa um quarto); a arma, a matéria que leva (consertar uma adaga custa um terço; um montante, cinco terços).

| Categoria | Preço de tabela (a espada, o escudo, a armadura inteira) | Conserto pago, por ponto | 10 pontos |
| --- | --- | --- | --- |
| Comum | 30 | 0,6 | 6 |
| Incomum | 180 | 3,6 | 36 |
| Raro | 1.080 | 21,6 | 216 |
| Épico | 6.480 | 129,6 | 1.296 |
| Único | 38.880 | 777,6 | 7.776 |
| Lendário | 233.280 | 4.665,6 | 46.656 |

7.11 **Ajustar (sob medida, 2.8)** grava um dono numa peça. Quem vai usar tem de estar ali; a peça é dele ou de quem ajusta.
- **O grau** sai da mão de quem ajusta: Iniciante 1, Treinado 2, Mestre 3, Lendário 4. Leigo não ajusta.
- **Custa** um bloco de bancada por degrau da categoria (Comum 1 ... Lendário 6) e, no fim, um teste com a mesma soma da forja, contra **22 + 6 por categoria**.
- Passou: o nome e o grau ficam gravados (e apagam o ajuste antigo). Falhou por 1 a 4: fica como estava. Falhou por 5 ou mais: a peça perde 5 de durabilidade.

7.12 **O jornal.** Servir na bancada da oficina do lugar (o conserto miúdo do povo). O bloco conta como bancada.
- **A oficina paga pelo que a mão vale:** de Iniciante, o salário de aprendiz; de Treinado, o de oficial; de Mestre para cima, o de mestre (5.4). Nunca menos que o grau de ofício que a pessoa já tem.
- **A paga segue a jornada** (5.4): 2 blocos pagos por dia, contados junto com o `ato.py trabalhar`. Passado isso, ou sem prata na oficina, o bloco é só bancada: treina, e não paga.

### Quanto se acerta (a conta exata do dado)

| Quem, onde | Comum | Incomum | Raro | Épico | Único | Lendário |
| --- | --- | --- | --- | --- | --- | --- |
| Leigo, forja de vila, sem preparo, Afinidade 50 | 48% | 26% | 12% | 5% | 3% | 1% |
| Iniciante, forja de vila, preparo inteiro até o Comum, Afinidade 50 | 86% | 32% | 15% | 7% | 4% | 2% |
| Treinado, forja de cidade, preparo inteiro até o Raro, Afinidade 50 | 93% | 77% | 52% | 10% | 5% | 3% |
| Mestre, grande forja, preparo inteiro até o Único, Afinidade 60 | 98% | 89% | 70% | 44% | 23% | 4% |
| Lendário, forja mestra, preparo inteiro, Afinidade 60 | 100% | 95% | 80% | 57% | 32% | 15% |
| Lendário, forja mestra, preparo inteiro, Afinidade 100 | 100% | 99% | 91% | 74% | 48% | 26% |

**Como ler:** cada grau de maestria vale 2 pontos; a oficina, até 4; o preparo, até 8. O dado pesa mais que tudo isso. Do Épico para cima, mesmo o melhor ferreiro perde núcleos: é para doer.

7.13 **Medido** (`python3 provas_oficio.py`; 15 de 15. Os números da tabela vêm de 21 rodadas: treze da medida, cinco da conferência e três do acerto). O dado é o de verdade, e a medida muda de uma rodada para outra: por isso a tabela diz o centro do que se viu ("cerca de") e a faixa vista. **Uma rodada nova pode sair um pouco fora da faixa vista; o que não pode é sair da meta.** O robô ferreiro vive de verdade: dorme na cama e paga uma noite por dia, come e paga, vive do jornal, faz 3,5 blocos de bancada por dia. Sobe um degrau de cada vez, e só abre a obra quando tem a mão que ela pede.
**Com que a escada vale:** na forja mestra (+4), com os quatro preparos (+8) desde o Dia 1, e com matéria e núcleo novos a cada obra.

| A primeira peça | Meta (o dia) | Medido (o dia em que metade das vidas já a tinha; na Lendária, o dia em que a primeira obra fecha) | A primeira obra fecha | Núcleos por vida | Com um núcleo só, nasce em |
| --- | --- | --- | --- | --- | --- |
| Rara | 15 a 30 | Dia 17 (em duas das 21 rodadas, Dia 20) | Dia 17 | (cerca de 1,7 leva de matéria, visto de 1,6 a 1,9; a pior vida, de 4 a 9) | |
| Épica | 45 a 80 | Dia 59 (numa das 21 rodadas, Dia 51) | Dia 51 | cerca de 2,5 (visto de 1,9 a 3,2; a pior vida: de 6 a 14) | cerca de um terço das vidas (visto de 20 a 52%) |
| Única | 130 a 200 | Dia 177 em treze das 21 rodadas; Dia 154 em cinco; Dia 189 numa; Dia 200 em duas, em cima do limite | Dia 131 | cerca de 3,5 (visto de 2,7 a 4,2; a pior vida: de 7 a 14) | cerca de um quarto das vidas (visto de 10 a 46%) |
| Lendária | 300 a 450 (a primeira OBRA fecha: a primeira tentativa) | Dia 356, em todas as rodadas. **A peça é rara de propósito:** nasceu até o Dia 450 em 3 a 12 de 30 vidas | Dia 356 | cerca de 2,5 (visto de 2,2 a 2,8) | cerca de 12% das vidas (visto de 0 a 24%; a conta exata: 15%) |

| O que mais se mede | Meta | Medido |
| --- | --- | --- |
| o melhor ferreiro possível (Lendário, oficina 4, preparo 8, Afinidade 100) acerta a Lendária | 15 a 30% | 25,7% (a conta exata; medido em 600 obras, de 24,3 a 29,7%) |
| um Iniciante em oficina de vila acerta a Comum, com os quatro preparos do Comum | 85% ou mais | 86,2% (a conta exata; medido, de 83,5 a 87,7%; sem preparo nenhum: 57,2%) |
| o mesmo acerta a Rara | menos de 25% | 15,4% (a conta exata; medido, de 12,2 a 18,0%) |
| a matéria da obra falhada some do mundo; o núcleo perdido sai do Livro | sempre | 60 obras Épicas, nenhuma conta errada |
| a obra de vários dias sobrevive a gravar e abrir o estado; o ato para quando o corpo pede | sim | sim |
| consertar 10 pontos de uma peça Rara, pago | 216 de prata, para a oficina | 216 |
| a peça ajustada rende no dono, e uma categoria abaixo na mão de outro | sim | sim |

**A Lendária é difícil de propósito** (decisão do jogador: a arma decide muito, e por isso a melhor delas tem de custar). A chance não sobe.
- **Uma tentativa é uma obra inteira:** 243 blocos de bancada. Com 3,5 blocos por dia, são cerca de **70 dias** de trabalho, com a matéria Rara e um **núcleo Lendário** dentro desde o primeiro dia.
- **O dado só rola no fim,** uma vez (7.3). Passou: a peça Lendária nasce. Falhou por 1 a 4: nasce uma peça **Única**. Falhou por 5 ou mais: a matéria some e o núcleo se perde (7.6).
- **Quem acerta:** o melhor ferreiro possível (mão de Lendário, forja mestra, os quatro preparos, Afinidade 100) acerta **1 vez em 4**. O robô do banco (Afinidade 60) acerta 1 em 6 ou 7. Quem tem menos que isso, menos ainda.
- **O que a meta mede** é o dia em que a primeira tentativa fecha: Dia 356, no melhor caminho. Até o Dia 450 cabem duas tentativas, e a peça nasce em cerca de um quarto das vidas do robô. Em média, uma Lendária custa quatro tentativas ao melhor ferreiro do mundo: perto de 280 dias de bancada e quatro núcleos Lendários.
**A escada só anda assim com núcleo à vontade.** O mundo dá 6 núcleos Épicos e 2 Únicos por ano (`PROJETO.md`). Na forja de cidade, sem preparo, a primeira Épica sai perto do Dia 100.

---

## 8. O mercado (etapa 2)

Os números moram no `tabelas_mercado.py`; as provas, no `provas_mercado.py`. O comando é o `mercado.py`. Tudo entra por evento, e a prata só muda de mão.

8.1 **Onde há mercado.** Num lugar com povo contado (`lugar.pop`). **Lugar sem povo não tem mercado:** ali não se compra, não se vende, e a virada do dia não faz nada.
O mercado de um lugar é o estoque dele (`lugar.estoque`), a prata dele (`estoque.prata`) e as peças que estão nele sem dono e que não estão soltas no chão (5.7).

8.2 **O preço de um bem** sai do estoque: **base × √(alvo ÷ estoque)**, nunca abaixo de 0,4 nem acima de 3 vezes a base.

| O lugar tem | O bem vale |
| --- | --- |
| nada, ou até um nono do alvo | × 3 (o teto) |
| um quarto do alvo | × 2 |
| metade do alvo | × 1,41 |
| o alvo | × 1 (a base) |
| o dobro do alvo | × 0,71 |
| o quádruplo | × 0,5 |
| 6,25 vezes o alvo, ou mais | × 0,4 (o chão) |

8.3 **O alvo** é o estoque que o lugar quer ter: **30 dias do consumo do povo** dele. A comida é a exceção: **60 dias**, porque se colhe uma vez por ano e o celeiro tem de atravessar o inverno e a entressafra.

| Bem | Base (prata) | Consumo por pessoa, por dia | O alvo numa vila de 400 |
| --- | --- | --- | --- |
| comida | 1 | 1 | 24.000 |
| lenha | 1 | 0,25 (no verão × 0,75; no inverno × 1,5) | 3.000 |
| carvão | 2 | 0,02 | 240 |
| sal | 3 | 0,02 | 240 |
| pano | 5 | 0,01 | 120 |
| remédio | 8 | 0,005 | 60 |
| ferramenta | 12 | 0,005 | 60 |

Uma unidade de comida é uma refeição: alimenta uma pessoa por um dia.

8.4 **A matéria** tem categoria, e o preço dela é vezes 6 a cada categoria, como o das peças. O povo gasta um sexto a cada categoria acima.

| Matéria | Comum | Incomum | Rara | Consumo por pessoa, por dia (Comum) |
| --- | --- | --- | --- | --- |
| metal | 3 | 18 | 108 | 0,01 |
| couro | 2 | 12 | 72 | 0,01 |
| osso | 1 | 6 | 36 | 0,005 |
| madeira | 2 | 12 | 72 | 0,02 |
| erva | 2 | 12 | 72 | 0,01 |

O povo de um lugar tira matéria até o Incomum. **A Rara ninguém produz:** só existe no mercado a que alguém trouxe do ermo ou da masmorra, e o povo a consome devagar.
Do Épico para cima não há matéria: há núcleo (7.3), e núcleo não se negocia em loja.

8.5 **Comprar e vender.** Toda compra mexe no estoque, e por isso no preço: a do jogador também.
- **O lote é pago unidade a unidade:** cada uma já mexe no preço da seguinte. O preço do lote é o mesmo de uma vez ou aos poucos. O troco, não: quem compra aos poucos paga o arredondamento a cada vez (10 de lenha: 12 de uma vez, 20 uma a uma).
- **Comprar custa 10% a mais** que o preço. **Pelos bens, a loja paga de 60 a 80% do preço**, conforme a mão de comércio de quem vende (8.7). **Pelas peças paga menos: de 40 a 60% do valor** (8.8).
- **A prata é inteira:** a compra arredonda para cima, a venda para baixo. A venda que não chega a 1 de prata é recusada. Quem vende vários bens de uma vez (a cesta) arredonda uma vez só.
- **Comprar e vender de volta sempre perde:** 45% com mão de Leigo, 27% com a melhor mão que existe.
- O bem comprado entra na carga da pessoa; o vendido sai dela e entra no estoque do lugar.

8.6 **A prata é contada.** Ela passa do bolso da pessoa para o estoque do lugar e de volta; nenhum negócio a cria nem a apaga. **Loja sem prata não compra:** se a prata do lugar não paga o lote, a venda é recusada, e o comando diz até quanto ela compra hoje.
É a mesma prata que paga o salário de quem trabalha no lugar (5.4), e nada a repõe: o lugar não produz prata. De onde entra prata nova é assunto da etapa 3.

8.7 **A mão de comércio** (`maestria.comércio`) decide quanto a loja paga a quem vende. Sobe por **dias de negócio**: o dia em que a pessoa fecha pelo menos um negócio de 10 de prata ou mais conta um (um por dia).

| Grau | A loja paga pelos bens | A loja paga pelas peças | Dias de negócio | E um feito |
| --- | --- | --- | --- | --- |
| Leigo | 60% | 40% | | |
| Iniciante | 65% | 45% | 20 | |
| Treinado | 70% | 50% | 80 | |
| Mestre | 75% | 55% | 250 | um negócio só de 1.000 de prata ou mais |
| Lendário | 80% | 60% | 750 | um negócio só de 10.000 de prata ou mais |

8.8 **As peças da loja** são itens do Livro de Itens com `onde` no lugar, sem dono e que não estão soltos, **até o Épico**. Daí para cima, e para núcleo, não há loja: leilão, encomenda ou despojo.
- **O valor** de uma peça é o preço de tabela da categoria (Comum 30, vezes 6 por categoria: Incomum 180, Raro 1.080, Épico 6.480), **na proporção do tamanho dela** (as duas regras abaixo), **menos o conserto que ela pede** (7.10: 2% do preço dela por ponto gasto), e nunca menos que a sucata.
- **A armadura vale pelo que cobre.** O preço de tabela é o da que cobre tronco, braços e pernas. Cada parte pesa: tronco 2, braços 1, pernas 1, cabeça 1, de 4. O elmo vale um quarto; só o tronco, metade.
- **A arma vale pela matéria que leva.** O preço de tabela é o da espada, que leva 3 unidades de matéria (7.4). Cada arma vale a proporção das unidades de matéria dela, metal e madeira somados; o escudo, a das dele (3: o preço de tabela). Vale no que a loja pede, no que ela paga e no conserto pago (7.10).

| Arma | Unidades de matéria | Comum | Incomum | Rara |
| --- | --- | --- | --- | --- |
| adaga | 1 | 10 | 60 | 360 |
| espada, maça, machado, lança, arco; o escudo | 3 | 30 | 180 | 1.080 |
| martelo, besta | 4 | 40 | 240 | 1.440 |
| montante, alabarda, malho | 5 | 50 | 300 | 1.800 |

- **Quebrada** (durabilidade 0), vale **sucata: 10%** do preço dela, nova.
- **Sob medida** (2.8), vale como **uma categoria abaixo**: na mão de outro é isso que ela rende.
- **A loja pede** o valor, sem os 10% dos bens. **Pelas peças a loja paga menos que pelos bens: 40% do valor** a quem não tem mão de comércio, e 5 pontos a mais por grau, até 60% (8.7; `tabelas_mercado.PAGA_PECA`). É o que fecha a conta de quem forja para vender com o salário de quem trabalha (8.13), e é por isso que a espada tirada de um morto rende pouco na loja. E paga **20% a menos por cada peça igual que já tem na prateleira** (mesmo tipo, mesma família ou material, mesma categoria; o recorte da armadura não conta).
- **A loja farta conta a prateleira inteira da categoria.** Cada lugar tem um **alvo de peças por categoria**: o que o gerador pôs na prateleira ao abrir a loja (a vila, 11 Comuns e 4 Incomuns; a cidade, 11 e 9), guardado no lugar, por evento (`lugar.alvo_pecas`).
  A loja paga **também 20% a menos por cada peça da mesma categoria que a prateleira já tem acima desse alvo**, seja de que tipo for. As duas contas se multiplicam. O que a loja pede não muda.
  **Quem compra da prateleira abre espaço de novo.** Categoria sem alvo (a Rara, numa vila) tem alvo zero: a primeira peça sai inteira, e a segunda já acha uma acima.
  O mercado aberto antes de esta regra existir não guardou alvo: vale o da tabela do tipo do lugar.
  Numa vila com a prateleira no alvo, quatro peças Comuns de tipos que a loja não tem, vendidas uma atrás da outra por um Leigo, saem por 40%, 32%, 26% e 20% do valor.
- Comprada, a peça ganha dono e chega guardada (5.13); vendida, fica sem dono e com `onde` no lugar. As duas coisas entram na história dela.
- **A peça em uso não se vende:** guarda-se antes (`ato.py tirar ITEM`).

| Uma espada Rara | Vale | A loja paga a um Leigo |
| --- | --- | --- |
| nova (30/30) | 1.080 | 432 |
| gasta (15/30) | 756 | 302 |
| quebrada (0/30) | 108 | 43 |
| sob medida para outro | 180 | 72 |

8.9 **A virada do dia.** Em cada lugar com povo, nesta ordem, e sem mexer na prata:
- **O lugar produz** o que está em `lugar.produz` (bem: quanto por dia). **Toda produção acompanha o preço:** a quantidade vezes o fator do preço do dia, entre a metade e o dobro.
  Quando falta, o povo dobra o serviço; quando sobra, corta pela metade.
  **A comida, além disso, é colheita:** vezes a estação (`tabelas_mundo.COLHEITA`: primavera 0,5 · verão 1 · outono 2,5 · inverno 0).
- **O povo consome** o que a tabela diz, até onde o estoque dá.
- A parte quebrada de uma quantidade vira a chance de mais uma unidade, pelo acaso do mundo: mesma semente, mesmo mercado.

Por isso **o preço anda sozinho:** o que foi comprado a mais volta em cerca de dois meses; o que foi vendido a mais escoa mais devagar; a lenha encarece no inverno.

8.10 **O ano da comida** (medido numa vila de 400 cuja produção de tabela é igual ao que ela come; o ciclo se repete igual, ano após ano):

| Quando | A comida vale |
| --- | --- |
| o Dia 1 (começo da primavera) | × 1,13 |
| o fim da primavera (o pico: a entressafra) | × 1,73 |
| o fim do verão | × 1,13 |
| depois da colheita (o fim do outono: o piso) | × 0,66 |
| o fim do inverno | × 1,14 |

**A comida é mais cara na entressafra, do fim do inverno ao fim da primavera, e mais barata depois da colheita.** O pico do ano é o fim da primavera, não o fim do inverno: a colheita da primavera é meia e o celeiro segue caindo até o verão. No verão, com a comida cara, o povo produz mais, e o preço cede.
**O celeiro se acerta sozinho.** O lugar que colhe 10% a menos do que come não desanda: acha outro ciclo, mais caro (de × 0,70 a × 2,18). O que colhe 10% a mais, um mais barato (× 0,63 a × 1,42).
Com 20% a menos a comida bate no teto toda entressafra (medido em rascunho): é fome, e é assunto das frentes.

8.11 **Negociar não gasta bloco** (como comer). Só se negocia no lugar onde a pessoa mora, e estando lá: quem saiu para o ermo (5.12) não compra nem vende. Morto não negocia.

8.12 **Abrir um mercado** é coisa do gerador, ou do Mestre, por um evento `gera` (`mercado.py funda POVO`). Ele põe: o povo; a produção igual ao consumo desse povo, menos a da matéria Rara (o preço de equilíbrio fica na base);
o estoque no alvo (a comida, no ponto do ano: 47 dias de celeiro no fim do inverno); a prateleira do tipo do lugar (peças Comuns e algumas Incomuns) e o alvo de peças por categoria (o que a prateleira nasce tendo: 8.8); e, se o lugar não tem prata, **5 de prata por pessoa**
(aldeia de 120: 600; vila de 400: 2.000; cidade de 1.500: 7.500).

8.13 **Medido** (`python3 provas_mercado.py`; 17 de 17). Toda prova confere que a soma da prata do mundo fecha.

| O que se mede | Meta | Medido |
| --- | --- | --- |
| comprar sobe o preço e vender desce; comprar e vender de volta perde | 20% ou mais | 600 idas e voltas: a menor perda, 45,5% (Leigo) e 27,3% (Lendário) |
| a prata do mundo antes e depois de 200 negócios ao acaso | a mesma | 12.200 e 12.200 |
| o preço nunca sai da faixa; a loja sem prata recusa a compra | 0,4 a 3 bases | 22 bens, 308 estoques: nenhum fora; recusa |
| um ano de viradas numa vila de 400: a comida, mais cara na entressafra (do fim do inverno ao fim da primavera) e mais barata depois da colheita | 0,6 a 2,2 bases | de × 0,66 (depois da colheita) a × 1,73 (o fim da primavera); no fim do inverno, × 1,14 |
| o diarista vive: o salário de um dia paga a cama e a comida | sobra de 0 a 2 | sobra de 0 a 0,86; 1,00 comendo na taverna |
| peça gasta vale menos que nova; quebrada vale sucata | sim | a espada Rara: 1.080, 756 e 108; a loja paga a um Leigo 432, 302 e 43 |
| a armadura vale pelo que cobre (placa Incomum) | a proporção | o corpo 180; só o tronco 90; o elmo 45 |
| a arma vale pela matéria que leva (as onze armas e o escudo, Comuns e Incomuns) | a proporção das unidades de matéria; a espada, o preço de tabela | Comuns: a adaga 10, a espada 30, o martelo 40, o montante 50; Incomuns: 60, 180, 240 e 300; consertar 5 pontos de uma Incomum, pago: 6 na adaga, 18 na espada, 30 no montante |
| a loja farta: 14 adagas iguais (cada uma vale 10), numa vila com a prateleira no alvo | cada uma vale menos | 3, 2, 1 e recusa as outras onze |
| a loja farta da categoria inteira: depois dessas, um malho, que a loja não tinha | sai por menos que os 20 inteiros | sai por 10 (há três peças Comuns acima do alvo); um arco Incomum sai pelos 72 inteiros, e um machado Incomum, logo depois, por 57 |
| quem compra da prateleira abre espaço de novo | a loja volta a pagar mais | comprada de volta uma adaga, a loja passa de 8 a 10 pela mesma alabarda |
| **forjar para a loja não é mina.** O ferreiro de começo da vila de teste compra a matéria na loja, forja o que mais rende e vende à loja; mede-se o que a forja lhe rende (o que a loja paga pelas peças, menos a matéria), em 30 vilas por escada | nos 5 primeiros dias, em média no máximo 6 de prata por dia, e no pior caso no máximo 12; do Dia 6 ao 30, em média no máximo 4 | cerca de 4,7 por dia nos 5 primeiros dias (visto de 4,4 a 4,9 em cinco rodadas; o pior caso, 5,0), e quase nada depois (visto de 0 a 0,6) |

**Como a meta do ferreiro de loja fechou.** O robô vive de verdade na vila de teste (come, dorme, paga a cama) e é ganancioso: em todo bloco de bancada escolhe a peça que mais rende hoje (o que a loja pagaria, pesado pela chance de acertar, menos a matéria). Quando nenhuma peça paga a matéria, serve o jornal. O dado da forja é o de verdade, e a medida muda um pouco de uma rodada para outra.
- **Antes de qualquer regra,** a forja rendia ao robô cerca de 17 de prata por dia só com peças Comuns, e cerca de 31 com Incomuns (o pior caso, 65), sem fim.
- **Com a arma pela matéria e a loja farta da categoria inteira** (8.8), rendia cerca de 8 e cerca de 11 nos 5 primeiros dias, e nada depois. Ainda passava da meta.
- **Com a loja pagando 40% pelas peças** (decisão do jogador), rende cerca de 4,7 nos 5 primeiros dias: é a matéria de começo (4 de metal e 2 de madeira) virando uma alabarda, que a loja paga por 20, e pouco mais. Depois disso nenhuma peça paga a matéria, e o ferreiro vive do jornal.
- **No bolso,** com a cama, a comida e o jornal, o robô fica com cerca de +7,7 de prata por dia nos 5 primeiros dias e cerca de +3,2 depois.
- **Para que serve forjar, então:** para vestir a si mesmo por menos do que a loja pede (a espada Comum custa 30 na prateleira e 10 de metal na bancada), para subir a mão, e, quando houver fregueses e encomendas (etapa 3), para vender a quem paga o valor inteiro.

---

## 9. A caça e a coleta (etapa 2)

Os números moram no `tabelas_caca.py`; os dos bichos, no `tabelas_bichos.py`; as provas, no `provas_caca.py`. O comando é o `caca.py`. Tudo entra por evento. A luta é a do `ato.py luta` (5.9), sem tirar nada.

9.1 **O ermo** é um lugar com bichos contados e matéria contada: `bichos` e `teto` (espécie: quantos há, quantos cabem), `coleta` e `coleta_teto` (matéria com categoria: quanto há, quanto cabe). **O que se tira, sai. O que nasce, nasce devagar.**
Caça-se e coleta-se no ermo **vizinho** do lugar onde a pessoa mora (`lugar.vizinhos`). A contagem é do Mestre. O que todo mundo sabe é a fartura, em palavras:

| Há, do teto | O povo diz |
| --- | --- |
| três quartos ou mais | há fartura |
| de 40% a três quartos | há, mas rareou |
| de 10% a 40% | é raro ver |
| menos de 10% | quase sumiu |
| nada | sumiu |

**Com o teto pequeno, "há fartura" enganaria, e a palavra é outra.** Da espécie de que cabem até 3 no ermo, o povo diz só "há pouco, e sempre foi assim". Da matéria de que cabem até 10 unidades, "é coisa pouca, e sempre foi assim". Dos chefes ninguém sabe de graça: acha-se no rastro.

9.2 **A saída** é um ato só: a ida, os blocos de procura (ou de coleta) e a volta. A pessoa segue morando no lugar dela.
- A ida custa 1 bloco (o ermo pode dizer outro número em `longe`); a volta, o mesmo. A procura vai de 1 a 6 blocos; sem dizer, 2. A coleta vai de 1 a 4: com a ida e a volta ao ermo vizinho, é um dia inteiro.
- A ida, a volta e a procura são blocos **leves**; a coleta é bloco **pesado**. Cada luta cansa 2 (5.2).
- A saída aberta fica escrita na pessoa (`marca.caca`) até a volta: sobrevive a fechar e abrir o estado, e a `MESA.md` a mostra. Por isso a escolha diante do bicho pode ser uma pergunta do turno.
- A procura **para** quando aparece alguma coisa e quando o corpo cruza um limiar (5.6). Acabados os blocos, a volta sai sozinha.
- **Quem vai junto** (`com=`) é gente do mundo que está no mesmo lugar: entra na luta ao lado do caçador, fica marcado na saída de quem comanda, e o corpo dele passa os mesmos blocos, com o mesmo esforço. Quem decide é quem comanda. **Quem vai junto tem parte no despojo** (9.10): não é mão de graça.
- **Com a saída aberta, a pessoa está fora** (5.12): os atos da vila são recusados, para ela e para quem foi junto. No ermo come-se da própria carga.
- **Quem cai no sono no ermo dorme ali** (5.2), e a procura para. Bicho não acha quem dorme no mato: essa regra ainda não existe.

9.3 **O rastro.** Um teste por bloco de procura (5.8): **2d20 + Percepção ÷ 10 + maestria de caça**, com a pena do corpo, contra a fartura do ermo:

| O número | |
| --- | --- |
| a base | 20 |
| a categoria do bicho (o raro é arisco) | Comum 0 · Incomum +2 · Raro +4 · Épico +6 · Único +8 · Lendário +10 |
| é chefe | +4 |
| o que falta da espécie | +12 × (1 − contagem ÷ teto): na metade do teto, +6; sumida, +12 |
| de noite ou de madrugada | −4 no teste |

Sem alvo ("o que aparecer"), o número é a base mais o que falta do ermo inteiro, e a espécie sai da sorte do mundo, com o peso da contagem de cada uma.

9.4 **O que aparece sai da contagem real:** um bicho, um bando, ou nada. O bando é o da espécie (6.9), **nunca maior do que a contagem**. Com a espécie a zero, quem passa no teste acha um rastro velho e mais nada.
**O alvo que não vive ali.** Do bicho que não é chefe, todo mundo sabe o que cada ermo tem. Sair atrás de uma espécie que aquele ermo nunca teve é **recusado antes de gastar um bloco**, e o comando diz o que vive lá.
Do chefe ninguém sabe de graça, e por isso a saída segue. Se a espécie não é bicho daquele tipo de ermo (a serpe é de serra e de ruína, não de floresta), a saída abre com um **aviso**. O aviso sai só do tipo do ermo: é o mesmo, haja ou não um chefe ali.
**Atrás de chefe, a rolagem do rastro é oculta.** O número do rastro muda com a contagem (9.3): com a serpe ali é um, sem ela é outro, e quem lesse o número saberia se há chefe. À mesa sai só "rolagem oculta"; o número e os dados ficam no SÓ O MESTRE da `MESA.md` e do `RETOMAR.md`. O que o caçador vê é o que o rastro lhe deu: o bicho, ou nada.
Quem passa no rastro atrás de um chefe que nunca viveu ali lê "nenhum sinal", e não "o rastro é velho".

9.5 **O acaso.** No bloco em que o rastro **falha** (e em todo bloco de coleta), pode aparecer o que não se procurava. A chance, por bloco, é a soma de contagem × ousadia de todas as espécies do ermo, dividida por 1.500 (nunca mais que metade). **Esse bicho viu o caçador.**

| Espécie | Ousadia (o quanto vem ao encontro de gente) | Investe (em quem não o atacou) |
| --- | --- | --- |
| corça | 0,1 | nunca |
| ratazana | 0,4 | 30% |
| javali | 0,4 | 35% |
| lobo | 1 | 70% |
| surucucu | 0,5 | 50% |
| urso | 0,6 | 50% |
| pantera, trasgo, serpe | 1 | 90% |
| aranha-de-toca | 0,6 | 80% |
| grifo | 0,8 | 60% |
| basilisco | 0,6 | 70% |
| hidra | 0,6 | 90% |
| dragão | 1 | 80% |

Na borda da floresta, com tudo no teto, o acaso é de 3% por bloco de rastro falhado.

9.6 **A ameaça é lida antes.** Quando o bicho aparece, a saída para. O caçador lê a frase do `bichos.ameaca` (6.12), com a conta da regra de ouro já feita para a arma e a armadura que ele veste, e o que a posição lhe dá. Então escolhe: **atacar, deixar ou fugir.** Não há luta antes da escolha.

9.7 **A posição** é o que o rastro deu a quem **viu primeiro** (passou no teste):
- se atacar, **o bicho é surpreendido** (perde o primeiro turno, 3.2);
- a luta começa **longe** ou **perto**, à escolha; passando por 5 ou mais, pode começar **colada**;
- **cada 5 pontos de margem dão uma vantagem de terreno, à escolha, até duas:**

| Vantagem | O que é, na luta (3.8) |
| --- | --- |
| alto | o caçador no alto: +1 no golpe, +2 no tiro, e quem sobe anda 1 casa por ação |
| cerco | o bicho sem saída: não foge; encurralado, luta até o fim (6.7) |
| estreito | uma passagem de um: o bando chega um de cada vez, e o bicho grande luta apertado |
| cobertura | o caçador com cobertura: −4 no tiro e no sopro contra ele |

- **deixar** o bicho que não o viu não custa nada: a procura segue. **Fugir** dele é recuar sem ser visto, largar a caçada e voltar.

9.8 **O bicho que viu o caçador** (o acaso) não é surpreendido, e não há terreno a escolher:
- **atacar:** a luta começa perto;
- **deixar** (ficar onde está): o bicho **investe** pela índole da espécie (9.5), e aí a luta é a mesma; se não investe, vai embora, e a procura segue;
- o que ele vai fazer (investir, vir atrás) é decidido pelo acaso do mundo **quando ele aparece**, e fica escrito: esperar não rola o dado de novo;
- **fugir:** o bicho vem atrás com a chance de investir **mais 20 pontos** (quem corre chama). Se vem, é teste de **Agilidade contra 20 + Agilidade ÷ 10 do bicho**. Passou, escapou, e a saída acaba. Falhou, foi **alcançado**: a luta começa colada, e **o caçador é o surpreendido**.

9.9 **A luta é a do `ato.py luta`** (5.9), com as paradas e as ordens do capítulo 3. O `caca.py` só monta o cenário e chama o `ato.luta_nova`: a casa são o caçador (comandado pelo jogador) e quem veio junto, com o que vestem hoje, o PV, as feridas e a pena do corpo; o outro lado são os bichos, com a ficha do capítulo 6.
- A luz é a do bloco em que o bicho apareceu: o encontro da noite e da madrugada é uma luta no escuro (3.9).
- Com a luta aberta, a saída não segue e o turno não fecha (5.10).
- A luta roda pelo `caca.py luta "Nome: ordem"`, que é o `ato.py luta roda` e, no fim, faz as contas; ou pelo próprio `ato.py luta roda`, e as contas saem no comando seguinte do `caca.py`, **antes de qualquer outra coisa, vivo ou morto quem comandava**.
- Se o arquivo da luta se perdeu, o comando recusa com uma frase, e o Mestre fecha a saída sem as contas (`caca.py larga "por quê"`).

9.10 **As contas da luta** entram num evento só (`despojo`):
- **bicho morto sai da contagem.** O caído é rematado por quem ficou com o campo; se a casa não ficou com o campo, o caído que não morreu segue vivo. **O que fugiu segue no ermo.**
- **se a casa ficou com o campo, o despojo de cada carcaça entra na carga:** de cada bem, da metade ao inteiro da tabela da espécie (6.11, `bichos.despojo`);
- **o despojo é de quem lutou até o fim.** Reparte-se em partes iguais entre os da casa que acabaram a luta **de pé no campo, ou caídos nele e vivos**. O que sobra da divisão vai, uma unidade a cada um, em roda, a começar por quem comanda. **Quem saiu da luta antes do fim** (recuou para fora dela, 3.15; fugiu; rendeu-se) **não leva nada**, nem que seja quem comanda a saída. Sozinho, o caçador que ficou com o campo leva tudo, como sempre;
- **o núcleo do chefe entra no Livro de Itens** (2.1) no mesmo evento: `de` é a espécie; o dono é quem comanda a saída, se lutou até o fim, ou o primeiro dos que ficaram (e `onde` fica vazio: peça com dono não está largada); a história diz o dia, o bicho e o ermo. O abate e o feito (9.14) vão para o mesmo;
- **quem perde o campo deixa a carcaça no mato:** nada entra em carga nenhuma. O núcleo do chefe que morreu assim nasce no ermo: sem dono, solto, com `onde` no ermo;
- **quem perdeu e vive volta na hora.** O que foi deixado por morto (caiu e não morreu, 3.13) volta arrastando-se: 1 bloco a mais. Quem ficou com o campo pode seguir a procura;
- **quem morre no ermo fica lá com tudo o que era dele** (5.11): as peças, as guardadas e os núcleos também, ficam soltas no ermo; a carga e a prata, no chão;
- **quem passa num rastro naquele ermo acha o que está solto:** o núcleo da carcaça que ninguém abriu e a peça largada passam a ser dele. **Só o que está solto:** se o lugar tem loja, a prateleira não é achado;
- **o que era de um morto não muda de mão sozinho** (5.11). Quem passa num rastro **acha o corpo** e lê o que ficou com ele (as peças, a carga, a prata), uma vez por saída, e não fica com nada. Quem fica com o quê é decisão de cena, e o Mestre registra por evento. Levar gente para morrer e voltar para apanhar o que era dela não é renda: é uma cena, com quem cobra.

9.11 **A presa ferida.** O bicho que foge **com ferida aberta** deixa sangue. Quem ficou com o campo pode segui-lo **na hora, sem gastar bloco**:
- o teste é o do rastro da espécie, **6 mais fácil**; e **3 mais difícil** a cada perseguição já feita naquele bloco (a presa ganha distância);
- passou: acha **o mesmo bicho, com o PV e as feridas com que fugiu**, e viu primeiro (a margem dá a posição, como em 9.7);
- falhou, seguiu a procura, ou voltou: perdeu-o. O bicho segue na contagem, e na próxima vez é um bicho inteiro;
- **é agora ou nunca:** se o relógio andou, o sangue esfriou.

9.12 **A coleta** (minério, madeira, erva) é uma saída como a da caça, com blocos pesados. Um teste por bloco: **2d20 + atributo ÷ 10 + maestria de coleta**, com a pena do corpo, contra **20 + 8 por categoria da matéria + 8 × o que falta dela** (1 − o que há ÷ teto).
Com o veio cheio: Comum 20, Incomum 28, Rara 36.

| Matéria | Atributo | O bloco que passa rende | Volta por dia (do teto) |
| --- | --- | --- | --- |
| minério (`metal:N`) | Força | 1 | 0,4% |
| madeira (`madeira:N`) | Força | 2 | 2% |
| erva (`erva:N`) | Percepção | 1 | 4% |

- **O bloco que passa rende o da tabela, e só isso.** Passar por muito não rende mais. **O bloco que falha não rende nada.**
- **A matéria pede mão.** É tranca, não conselho: sem a mão, o comando recusa antes de gastar a saída, e diz a mão que a matéria pede, quantos blocos de coleta a pessoa tem e quantos faltam.

| Matéria | A mão que pede (a maestria de coleta) |
| --- | --- |
| Comum | Leigo: qualquer um tira |
| Incomum | Iniciante (40 blocos de coleta) |
| Rara | Treinado (160 blocos) |

- **A borda só dá matéria Comum.** A Incomum e a Rara só há do interior para cima (9.15).
- **Nunca se tira mais do que há:** o que acabou, acabou. O que se tira sai do `coleta` do ermo e entra na carga **no mesmo evento**.
- Em todo bloco de coleta o acaso rola (9.5): quem corta lenha não está olhando o mato.

Quanto se acerta, com o veio cheio (a conta exata do dado):

| Quem | Comum | Incomum | Rara |
| --- | --- | --- | --- |
| Leigo, Força 56 (o homem de começo) | 77% | não tira | não tira |
| Iniciante, Força 56 | 83,5% | 52,5% | não tira |
| Treinado, Força 56 | 89% | 62% | 29% |
| Treinado, atributo 90 | 96% | 77% | 44% |
| Mestre, atributo 90 | 98,5% | 83,5% | 52,5% |

9.13 **A virada do dia** (`caca.virada`), em todo lugar com teto:
- **os bichos criam devagar:** de cada espécie nascem, por dia, contagem × cria × (1 − contagem ÷ teto). A cria é 4% (Comum), 2,5% (Incomum), 1% (Raro para cima). Nunca passa do teto;
- **com menos de dois, a espécie não cria:** espera um casal de fora, que vem, em média, a cada 60 dias (Comum), 100 (Incomum) ou 180 (Raro para cima). **Espécie caçada até o fim some por muito tempo;**
- **o chefe não cria:** morto, nasce outro, em média, em 180 dias (Épico) ou 364 (Único). O Lendário não nasce de novo;
- **a matéria volta** pela fração da tabela (9.12), até o teto.

A parte quebrada de cada conta vira a chance de mais um, pela sorte do mundo: mesma semente, mesmo ermo.

9.14 **A maestria de caça e a de coleta** (`maestria.caça`, `maestria.coleta`) sobem por blocos, como a das armas (5.5): 40 blocos de procura (ou de coleta) fazem um Iniciante; 160, um Treinado; 500, um Mestre; 1.500, um Lendário. A de caça soma no rastro; a de coleta soma no teste da coleta e é a mão que a matéria pede (9.12).
De Mestre para cima os blocos não bastam: pede o **feito**. Na caça, ficar com a carcaça de um bicho Raro (para Lendário, Épico). Na coleta, ter tirado matéria Rara com a própria mão.

9.15 **Povoar um ermo** (`caca.povoa`, o gerador ou o Mestre): o habitat e o perigo (1, a borda; 2, o interior; 3, o coração) dão as espécies que vivem ali, cada uma no teto, e a matéria.

| Habitat | A borda | O interior, além disso | O coração, além disso |
| --- | --- | --- | --- |
| floresta | corça 80, javali 40, lobo 12, surucucu 8, urso 3 | pantera 2, aranha 6 | |
| campo | corça 80, lobo 12 | | |
| brejo | ratazana 90, javali 40, surucucu 8 | trasgo 2 | basilisco 1, hidra 1 |
| serra | lobo 12, urso 3 | pantera 2, grifo 2 | serpe 1, dragão 1 |
| caverna | ratazana 90, urso 3 | aranha 6, trasgo 2 | basilisco 1 |
| ruína | ratazana 90, surucucu 8 | aranha 6, trasgo 2 | basilisco 1, serpe 1, hidra 1, dragão 1 |

| Habitat | A matéria da borda (o teto) | No interior, além disso | No coração, além disso |
| --- | --- | --- | --- |
| floresta | madeira Comum 200, erva Comum 60 | madeira Incomum 20, erva Incomum 10, madeira Rara 4, erva Rara 3 | |
| campo | erva Comum 80, madeira Comum 40 | erva Incomum 8 | |
| brejo | erva Comum 90, madeira Comum 60 | erva Incomum 20, erva Rara 5 | |
| serra | minério Comum 150, madeira Comum 60 | minério Incomum 20, minério Raro 5 | |
| caverna | minério Comum 100 | minério Incomum 30, minério Raro 6 | |
| ruína | minério Comum 40, erva Comum 30 | minério Incomum 10 | minério Raro 4 |

**A borda só dá matéria Comum.** A Incomum e a Rara só há do interior para cima, onde o bicho também é pior.
**O bicho raro é contado:** uma floresta inteira tem duas panteras e seis aranhas, e cada uma que morre leva meio ano para voltar.

9.16 **Na mesa.** O `caca.mesa` põe na `MESA.md`: os ermos vizinhos e o que se sabe deles (a fartura, em palavras, e a mão que cada matéria pede, se o personagem não a tem), a mão de caça e de coleta, a conta do rastro e a da coleta, a saída aberta e o que falta decidir, e o resumo dos bichos dali (`bichos.mesa`, sem os chefes). **A contagem não sai na parte pública:** o `caca.so_mestre` a põe na seção SÓ O MESTRE da página, com os chefes, a chance do acaso e o que os mortos deixaram no ermo. A saída que ficou aberta no fim do turno vai também para o `RETOMAR.md`.

9.17 **Medido** (`python3 provas_caca.py`; 30 de 30). O dado é o de verdade: as medidas mudam de uma rodada para outra. A coluna "Medido" diz o centro do que se viu ("cerca de") e, entre parênteses, a faixa vista em 23 rodadas do banco (15 da medida, 5 da conferência, 3 do acerto). **Uma rodada nova pode sair um pouco fora da faixa vista; o que não pode é sair da meta.**
O robô caçador: nível 10, gente gerada, de arco, espada de reserva, cota e elmo de malha, tudo Comum, no ermo de começo (a borda da floresta). Vive de verdade: dorme na cama e paga, come e paga, vende o despojo na loja (a 60%) e manda consertar o que veste. Procura corça, e a encurrala sempre que o rastro lhe dá o cerco.

| O que se mede | Meta | Medido (75 vidas de 30 dias por rodada) |
| --- | --- | --- |
| o caçador tira por dia, com o despojo ao preço de base | 1,5 a 4 diárias (a diária: 4 de prata) | cerca de 2,1 diárias (visto de 1,95 a 2,19) |
| o mesmo robô sai ferido ou morto | em 2 a 12% das saídas | em cerca de 4,5% (visto de 3,6 a 5,6%); morrem cerca de 17 de 75 em 30 dias (visto de 8 a 24) |
| o mesmo robô, afoito, morre em 30 dias | em 70% das sementes, ou mais | em 100%, em todas as rodadas; a metade até o Dia 2 |
| caçar 60 corças derruba a contagem, e o rastro fica mais difícil | sim | de 80 para cerca de 40 (visto de 31 a 46); o rastro, de 20 para 26 (visto de 25 a 27) |
| e a espécie volta a nove décimos do teto (medido do teto menos os 60) | em 30 a 120 dias | em cerca de 85 dias (visto de 68 a 98); de onde o caçador a deixou, em cerca de 47 (visto de 36 a 63) |
| nenhuma contagem negativa; o núcleo do chefe no Livro, com `de` e `onde` | sim | 150 vidas por rodada, nenhuma; sim |
| o que sai do ermo é o que entra na carga | em toda vida | 150 vidas, cerca de 2.100 bichos por rodada, nenhuma conta aberta |
| **o despojo é de quem lutou até o fim** (prova nova do acerto) | partes iguais entre os que ficaram; quem saiu da luta, nada | três desfechos postos à mão e um caminho com o dado de verdade (quem comanda manda o grupo atacar e recua para fora da luta): a carga dele não muda |
| **o que era do morto não muda de mão sozinho** (a prova QUEM MORRE NO ERMO, refeita) | quem passa num rastro acha o corpo e não fica com nada | as 6 peças, a carga e os 250 de prata seguem no chão; por um evento do Mestre, passam |
| **atrás de chefe, a rolagem do rastro é oculta** (a prova O ALVO QUE NÃO VIVE ALI, estendida) | a saída inteira igual, haja ou não um chefe | com o dado preso, o mesmo texto nos três mundos (nunca houve serpe, há uma, houve e morreu); o número (42, 30 e 42) só com o Mestre |

**O que a meta não mede, e a mesa sente.** Na loja, o que o caçador tira vale cerca de 5 de prata por dia (visto de 4,6 a 5,2); o conserto leva perto de 0,7; a cama e a comida, 3. **No bolso dos que chegam vivos fica cerca de +1,2 por dia** (visto de +1,0 a +1,4; o diarista fica com +1,00), e morre, em média, um em cada cinco no mês. O cauteloso, que só encurrala a corça sozinha e do alto, tira cerca de 1,8 diária (visto de 1,7 a 1,9) e fere-se em cerca de 1,7% das saídas (visto de 1,0 a 2,6%: quase sempre abaixo da faixa). A caça de começo paga pouco mais que a diária, e mata: se é isso que se quer, decide o jogador.

**A coleta: as metas K1 a K4.** O robô coletor de começo é o mesmo homem do caçador (nível 10, o mesmo conjunto Comum), Leigo em coleta, com a mesma vida: come, dorme, paga a cama, vende na loja, e sai uma vez por dia, de manhã, por dois blocos de coleta.
É ganancioso: tira sempre a matéria que mais vale por bloco, das que a mão dele tira (o preço de base vezes o que o bloco rende em média, pela conta exata do dado). Do bicho que aparece, foge; da presa, só sai de perto. Conta-se a matéria que chega em casa: o despojo de uma luta forçada não é coleta.

| O que se mede | Meta | Medido (o centro, e a faixa vista em 23 rodadas) |
| --- | --- | --- |
| **K1**, na borda da floresta, em 30 dias: o que ele tira, ao preço de base | 1,0 a 2,0 diárias por dia | cerca de 1,5 (visto de 1,44 a 1,56; 50 vidas por rodada; só madeira Comum) |
| e sai ferido ou morto | em 0,3 a 4% das saídas | em cerca de 1,4% (visto de 1,0 a 1,8%); morrem cerca de 14 de 50 (visto de 9 a 20) |
| **K1**, na borda da serra | 1,0 a 2,0 diárias por dia | cerca de 1,34 (visto de 1,31 a 1,36; 150 vidas por rodada; madeira Comum enquanto há, depois minério) |
| e sai ferido ou morto | em 0,3 a 4% das saídas | em cerca de 0,7% (visto de 0,4 a 0,9%: perto do chão da meta); morrem cerca de 26 de 150 (visto de 17 a 31) |
| **K2**, o mesmo robô, sozinho no mesmo ermo, dos dias 91 a 120 | 0,7 a 2,0 diárias por dia | floresta: cerca de 1,6 (visto de 1,38 a 1,71); serra: cerca de 1,18 (visto de 1,10 a 1,23; já Treinado em coleta) |
| **K3**, o Leigo de começo acerta o bloco de matéria Rara | em 15% ou menos | em 0%: o comando recusa (a matéria Rara pede mão de Treinado) |
| o bloco que falha | não rende nada | não rendeu nada, em nenhuma rodada |
| o Treinado (maestria 4, atributo 90) acerta o bloco de matéria Rara | em 35 a 60% | em 43,7% (a conta exata); medido, de 36 a 49% em 300 blocos |
| **K4**, na vila de teste, a saída de coleta mais longa (4 blocos: um dia inteiro), vendendo tudo o que tirou | no máximo 12 de prata, no pior caso de 200 vilas | 9 de prata no pior caso, em todas as rodadas (8 de madeira Comum); em média, cerca de 6,5 (visto de 6,3 a 6,8) |
| **a vila de teste segue a tabela** (prova nova do acerto) | a matéria da mata igual à da tabela (9.15), nos três começos; a gente com os blocos da mão que tem; o estado inteiro | sim, nos três |

- **Por que a floresta nunca passa de 2 diárias:** dois blocos por dia, 2 de madeira por bloco, 2 de prata cada uma: 8 de prata, se nenhum bloco falhar.
- **No ermo de borda, o que o robô tira volta:** no Dia 120 a floresta segue com 200 de 200 de madeira; a serra tem perto de 140 de 150 de minério, e a madeira dela (60) fica rala, perto de 8.
- **O que a meta não mede, e a mesa sente.** Na loja isso dá cerca de 2,9 de prata por dia na floresta e 2,6 na serra (a loja paga 60%, o preço cede um pouco e o troco arredonda para baixo); a cama e a comida levam 3.
  **No bolso, o coletor de começo fica no zero a zero:** perto de zero na floresta (visto de −0,1 a +0,1 por dia), cerca de −0,35 na serra (o diarista fica com +1,00). E morre: de um em cinco a dois em cinco por mês na floresta, perto de um em seis na serra. Quase toda saída ruim é morte, porque o bicho que alcança quem foge pega pelas costas.
- **Sem julgar (não é meta): o Treinado no interior.** O mesmo homem, já Treinado em coleta, ao lado de um ermo de interior, em 30 dias (10 vidas por rodada):
  no interior da serra, cerca de 7 diárias por dia ao preço de base (visto de 6,5 a 7,5), cerca de +19 de prata por dia no bolso (visto de +17 a +21), ferido ou morto em até 1,1% das saídas, e morreram de nenhum a 3 de 10;
  no interior da floresta, cerca de 8,5 diárias (visto de 6,6 a 9,8), cerca de +30 no bolso (visto de +25 a +35), ferido ou morto em 0,4 a 3,7% das saídas, e morreram de 1 a 5 de 10.
  São dez vidas por rodada: estes números balançam mais que os das metas.
  É a matéria Incomum e a Rara do primeiro mês; a Rara, vendida numa vila que não tinha nenhuma, onde o preço nasce perto do teto (8.2). Se é muito, decide o jogador.

### O que a etapa 2 não resolve (fica dito)

- **Só quem está em cena age.** Os caçadores do povo, os fregueses e os rivais são das etapas 3 e 5. Ninguém além do personagem compra peça: a prateleira não escoa. Com a loja pagando 40% pelas peças e farta depressa (8.8), quase nenhuma peça nova paga a própria matéria na loja de uma vila: forja-se para vestir, não para vender, até haver freguês.
- **Um relógio só.** Quando outra pessoa age (`quem=ID`), o tempo do mundo anda, e o corpo de quem ficou parado não sente. O corpo dos outros é da etapa 3.
- **Não há viagem.** O ermo é o vizinho, a um número fixo de blocos.
- **Não há peso.** A carga não tem limite, e a comida não estraga: quem compra na colheita e vende na entressafra ganha de 38 a 62% em meio ano, sem trabalho e sem risco.
- **A taverna tem preço fixo:** 1 de prata o ano inteiro. O mercado sabe dizer o que a refeição valeria no dia (`mercado.refeicao`), e ninguém cobra isso ainda.
- **A prata do lugar não se repõe.** Uma vila de 400 tem 2.000: quatro peças Raras de tipos diferentes levam 1.274 (432, 345, 276 e 221: a loja farta, 8.8); a prata dá para onze, cada uma por menos, e a décima segunda é recusada por falta de prata.
- **A coleta de quem já tem mão não tem meta.** A de começo tem (K1 a K4, 9.17). A do Treinado no interior foi só medida: rende de 6,5 a 9,8 diárias por dia no primeiro mês.
- **O povo não passa fome,** e o bicho não vem à vila: é das frentes.
- **Não há tempo de céu** na caça: só o escuro entra sozinho na luta.
- **A morte não tem herdeiro** (etapa 6). Na vila e no ermo, quem fica com o que o morto largou é decisão de cena, por evento (5.11).
- **A caça de começo é para quem aceita o risco** (decisão do jogador). No bolso sobra ao caçador o mesmo que ao diarista, um em cada cinco morre no mês, e a corça escoiceia em vez de fugir. Fica assim.
- **Quem vai junto não pede paga.** Vai quando é chamado e leva a parte dele do despojo (9.10). Se o companheiro pede prata, recusa o perigo ou cobra depois, decide o jogador.

---

## Os comandos

```
python3 provas.py 600                                as provas da luta, dos itens e dos bichos
python3 provas_mundo.py                              as provas do mundo: a etapa 1, o alicerce da etapa 2, o mercado, o ofício, a caça
python3 provas_caca.py coleta                        só as metas da coleta (K1 a K4) e a vila de teste contra a tabela
python3 estresse.py 1500                             lutas ao acaso, com bichos misturados
python3 vila_teste.py PASTA [comeco=ferreiro|cacador|guerreiro] [nome=NOME] [semente=N]      a vila de teste (GUIA_VILA.md)
export MOTOR10_MUNDO=PASTA                           o save em que os comandos abaixo mexem (sem isso: a pasta mundo/)

python3 turno.py abre                                gera e mostra a MESA.md
python3 turno.py pergunta "texto" "a=..." "b=..."  ·  turno.py responde "1a.2b"  ·  turno.py nota "só o Mestre"  ·  turno.py fecha "o que houve" [parado] [git]
python3 ato.py comer [carga] | dormir N [chao] | trabalhar N | treinar N ARMA | descansar N | esperar N
python3 ato.py pecas | vestir ITEM [arma|arma2|escudo] | tirar ITEM
python3 ato.py luta nova CENARIO.json LUTA.json  ·  ato.py luta roda LUTA.json "Nome: atacar"  ·  ato.py luta larga LUTA.json "por quê"      (LUTA.json sem pasta fica no save, em lutas/)
python3 teste.py "o que se tenta" Força contra=26 [mais=N] [quem=ID] [oculto]
python3 estado.py valida | eventos [N] | pessoa ID | lugar ID  ·  corpo.py ver [ID]
python3 estado.py mestre '[["pessoa","eu","moedas","soma",5]]' "achou cinco moedas"      o que o Mestre decide em cena, por evento

python3 mercado.py ver | preco BEM [N] | comprar BEM N | vender BEM N|tudo | vender tudo | comprar ITEM | vender ITEM
python3 mercado.py funda POVO "como foi"             o Mestre abre um mercado onde a pessoa está

python3 oficio.py ver | pede arma espada Raro
python3 oficio.py forjar arma espada Raro "Nome" [blocos=N] [nucleo=ID]  ·  forjar armadura malha Raro "Nome" [cobre=cabeça]  ·  forjar escudo Raro "Nome"
python3 oficio.py continua [OBRA] [blocos=N]  ·  larga OBRA  ·  consertar ITEM [pontos=N] [pago]  ·  ajustar ITEM [para=ID]  ·  jornal N
python3 oficio.py preparo receita|ajudante|fogo|bigorna CATEGORIA "como foi"  ·  oficio.py oficina NIVEL "como foi"      (o Mestre registra)

python3 caca.py ver | sair [ERMO] [alvo=ESPECIE] [blocos=N] [com=ID,ID] | coletar BEM [ERMO] [blocos=N]      (procura: N de 1 a 6; coleta: N de 1 a 4)
python3 caca.py atacar [inicio=longe|perto|colado] [vantagem=alto,cerco] | deixar | fugir
python3 caca.py luta "Nome: ordem" ["grupo: ordem"] | sangue | segue | volta
python3 caca.py conta [ERMO]  ·  caca.py povoa ERMO HABITAT [perigo=1] [vizinho=LUGAR]  ·  caca.py larga "por quê"      (só o Mestre)

python3 bichos.py lista | ver ESPECIE | ameaca ESPECIE [N] [arma=CATEGORIA] [armadura=CATEGORIA] | tracos
python3 bichos.py mede ESPECIE NIVEL CATEGORIA [N] [lutas=200] [arma=arco] [armadura=couro] [inicio=longe] [surpresa=bicho]      a régua (lutas de ensaio)

python3 itens.py ver [dono=ID] | janela ID           (com um mundo, lê o Livro dele)
python3 itens.py nova arma lança Raro "Nome" dono=ID | nova nucleo Épico "Nome" de=serpe dono=ID | dono ID PESSOA | conserta ID [N]      (com um mundo, por evento "mestre")
python3 pessoas.py padrao 50 arma=espada:Raro armadura=malha:Raro escudo=Raro
python3 luta.py nova dados/cenario_exemplo.json lutas/corredor.json  ·  luta.py roda lutas/corredor.json "Aldric: atacar o chefe agressiva" "grupo: segurar"  ·  luta.py demo      (a luta fora do mundo)
```

No cenário, cada pessoa veste `arma`, `arma2`, `armadura`, `elmo`, `escudo` e `pecas` (mais peças de armadura). Cada uma é o id de um item do Livro, ou um atalho para gente miúda: `["espada", "Raro"]`. O atalho de armadura veste o corpo e um elmo igual; `"elmo": false` tira o elmo. Quem é do mundo entra como `{"id": "tome"}`; um bicho, como `{"nome": "lobo 1", "bicho": "lobo"}`.
