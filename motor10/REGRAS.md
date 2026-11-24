# MOTOR 10 — O LIVRO DE REGRAS

Este é o livro de regras do Motor 10. É um só, por assunto, sem história: o que mudou e quando fica no `MUDANCAS.md`.
Os números moram todos nas páginas `tabelas*.py`. Nenhuma regra vale antes de passar no banco de provas (`python3 provas.py` e `python3 provas_mundo.py`).

**Estado:** estão escritos e provados os capítulos 1 a 4 (a pessoa, os itens, a luta, o banco de provas), o capítulo 5 (o tempo, o corpo, o estado e o turno: a etapa 1 do mundo), os capítulos 6 a 9 (os bichos, o ofício, o mercado, a caça e a coleta: a etapa 2, "viver de um ofício") e os capítulos 10 a 16 (a etapa da magia: os dons e os talentos, a magia na luta, a alquimia e o encanto, as maldições, a magia no mundo, as criaturas, os covis e a vila de teste com a magia). Todas as metas passam. Duas foram fechadas por decisão do jogador: a Lendária é difícil de propósito, e a meta dela é o dia da primeira tentativa (7.13); a loja paga 40% pelas peças, e com isso forjar para a loja deixou de ser mina (8.8, 8.13). Na etapa da magia, o mau-olhado tira 4 (o projeto dizia 2: 11.13), e dois chefes foram acertados por isso (15.8). O plano do resto está no `PROJETO.md`. A vila de teste está no `GUIA_VILA.md`.

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
| pernas | vai ao chão | vai ao chão e fica com a perna presa: levanta-se, mas não sai mais do lugar (−2 na Defesa) |

**O sangue:** a ferida do tronco, a ferida grave e a da arma que "sangra" tiram, por rodada, um quinto do golpe que as abriu, por 3 rodadas (5, se grave ou da arma que sangra). O que o sangue tira (e o que o veneno tira, 6.6) sai escrito no registro, no fim de cada rodada ("Cira sangra 13 (37/121)"): a conta dos golpes fecha com o quadro. No chão: −4 na Defesa, e levantar gasta uma ação. A ferida fica depois da luta; o fim da luta lista só as feridas abertas nela.

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
**Sair da luta:** quem tem ordem de recuar anda para trás enquanto houver inimigo de pé a menos de 8 casas, e, se acaba a rodada a 8 casas ou mais de todo inimigo de pé, saiu da luta. Quem persegue anda o mesmo que quem foge: só se sai com alguém segurando a passagem, com o chão a favor, ou se o outro lado não vier atrás.
**A retirada só existe com inimigo de pé.** Se o último inimigo cai, a luta acabou: quem recuava não "sai", fica com o campo como os outros (e tem a parte dele no despojo, 9.10).

3.16 **A luta para e pergunta.** O script roda turno a turno. Quando algo muda, ele para **ali, no meio da rodada**, e mostra o quadro:
- a luta vai começar;
- alguém da casa cai, morre, foge, se rende, ou tem uma peça quebrada;
- o líder do outro lado cai ou foge, ou alguém de lá se rende;
- quem o jogador comanda é ferido, passa de metade ou de um quarto do PV, fica sem fôlego, fraqueja, perde o alvo, ou está segurando onde só apanha;
- quem o jogador mandou tomar fôlego encheu o fôlego (a ordem acabou);
- passam três rodadas sem novidade.

O jogador então dá a ordem de quem ele comanda, e a ordem do grupo (só o lado dele recebe ordem; nome ou ação que não existe é recusado, com a lista do que vale):
`atacar [alvo]` (se o alvo está longe, vai até ele, contornando se a linha deixar) · `segurar` (não anda; bate em quem chega) · `avancar` · `recuar` (a retirada: anda para trás até ficar a 8 casas de todo inimigo de pé, 3.15) · `folego` · `guardar NOME`, e no fim a postura.
A ordem do grupo é uma palavra: `atacar`, `segurar` ou `recuar`.
**A ordem `folego` acaba quando o fôlego enche:** daí em diante a pessoa segura (bate em quem chega), e a luta para e pergunta. Ninguém fica tomando fôlego de fôlego cheio enquanto o inimigo chega.

---

## 4. O banco de provas

Toda mudança de regra ou de número roda `python3 provas.py`. Meta que falha: a mudança não entra, ou a meta muda com a palavra do jogador.
A medição completa está em `dados/provas_saida.txt` (600 lutas por meta). **114 de 114 passam:** as 54 metas deste capítulo, as 26 dos bichos (6.14) e as 34 da magia na luta (11.13). O banco do mundo (`python3 provas_mundo.py`, saída em `dados/provas_mundo_saida.txt`) passa 148 de 148: as etapas 1 e 2, os dons e os talentos (10), a magia do mundo (12 a 14) e as criaturas (15 e 16). O `python3 estresse.py 1500` roda lutas ao acaso (e 500 de magia) e confere os invariantes (`dados/estresse_saida.txt`).

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
| retirada | com dois guardas segurando o corredor, quem recebe ordem de recuar sai da luta em 83% (nas outras, os guardas vencem antes de ele chegar a 8 casas, e ele fica com o campo) |
| a retirada só com inimigo de pé | 150 lutas de dois contra um ladrão, com um dos dois recuando: ninguém "sai da luta" depois de o último inimigo cair (antes do acerto, 135 vezes), e quem recuava fica com o campo |
| cenário conferido | nome repetido e tempo que não existe: recusado antes de qualquer dado |

---

## 5. O mundo: o tempo, o corpo, o estado e o turno (etapa 1)

Os números deste capítulo moram no `tabelas_mundo.py`; as provas, no `provas_mundo.py` (as 12 da etapa 1, as 13 que a etapa 2 pôs no alicerce e as 9 do acerto da terceira volta: 34 de 34).

5.1 **O tempo.** O dia tem 6 blocos de 4 horas: madrugada, alvorada, manhã, tarde, entardecer, noite. Semana de 7 dias, estação de 91, ano de 364. Todo ato custa blocos. A madrugada e a noite são escuras: a luta ao ar livre ganha "escuro" sozinha.

5.2 **O corpo** tem três medidores, de 0 a 10:

| | Sobe | Desce | Cobra |
| --- | --- | --- | --- |
| Fome | +1 a cada 2 blocos | refeição −3 (1 de prata) | em 4: −2; em 7: −4, e 5% do PV máximo a cada virada do dia |
| Sono | +1 por bloco acordado | −3 por bloco na cama; −2 no chão | em 6: −2; em 8: −4, e Vontade contra 28 a cada bloco, ou **dorme ali mesmo**, no chão, até o sono baixar de 6 |
| Cansaço | bloco pesado +2, leve +1, luta +2 | −3 por bloco na cama; −2 no chão; −1 descansando | cada 3 pontos tiram 1 do fôlego máximo; em 9: −2 |

**A pena do corpo** é a pior das três (não somam) e entra em todo teste, no acerto e na Defesa. O mesmo homem, com sono 8 e cansaço 9, vence a si mesmo descansado em 23% das lutas.

5.3 **Curar.** Cada bloco dormido sem fome (abaixo de 4) devolve 5% do PV máximo, em no máximo dois blocos por dia: um décimo por noite. A ferida sara com **7 dias de repouso**; a grave, com **21**. **Não conta como repouso:** o dia com dois blocos pesados, o dia em que a pessoa lutou, e o dia em que ela passou um bloco ou mais numa saída ao ermo (a ida, a procura, a coleta e a volta contam). Estar ferido custa: quem não trabalha não ganha, e quem sai para caçar não sara.

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

5.6 **O ato longo para.** Dormir, trabalhar, treinar ou esperar vários blocos para quando o corpo cruza um limiar (fome, sono, cansaço), e diz por quê. Quem cai no sono (5.2) dorme onde está, e esses blocos passam. O ato de outra pessoa para também quando é o personagem, que esperava, quem cruza o limiar (5.14).

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
- **A última linha de cada comando não mente.** Com a luta aberta ela diz só a hora, e que o PV, o fôlego e as feridas que valem são os do quadro da luta (o save só os recebe quando a luta acaba). De quem morreu, diz só a hora e a morte.

5.10 **O turno em dois comandos.**
- `turno.py abre` só lê e gera a `MESA.md`: você, o lugar, o que dá para fazer e o que custa, as perguntas abertas, e o SÓ O MESTRE.
- `turno.py responde "1a.2b"` confere cada código contra as perguntas abertas. Vale como o jogador escreve: com espaço entre o número e a letra, e com ponto, vírgula ou espaço entre os códigos ("1c.2 a", "1c, 2a", "1c 2a"). Código que não bate é recusado, e nada é marcado. **Cada pergunta guarda o número com que foi aberta até o turno fechar:** responder a 1 não faz da 2 a nova 1. A pergunta já respondida recusa segunda resposta. A pergunta aberta no meio do turno ganha o número seguinte. No fechar, as que ficam são numeradas de novo, de 1 em diante: é com esse número que o `RETOMAR.md` as mostra, e é esse o número que o `turno.py pergunta` diz ao abrir (o número do código que o jogador vai escrever).
- `turno.py fecha "o que houve"` **recusa** se: há luta aberta · há menos de 2 perguntas abertas · o relógio não andou (a não ser que se diga `parado`) · o estado quebrou um invariante. Passando, gera o `RETOMAR.md` (o agora, o que houve, os fatos do registro, a saída de caça que ficou aberta, as perguntas, o que só o Mestre sabe) e a `MESA.md` nova. Com `git`, guarda e envia, e avisa se o envio falhou.
- **O `RETOMAR.md` nunca corta calado.** O que se repete todo dia (comer, dormir, a cama, descansar, esperar) vira uma linha por dia. O mesmo fato repetido **em seguida** no mesmo dia vira uma linha, com a conta e as horas do primeiro ao último ("Dia 2, manhã a noite: Maro espera o conserto (× 4)"); o que aconteceu depois de outro fato fica na linha e na hora dele. O mundo andando sozinho (o dia que vira, o lugar que produz e consome, o ermo que se refaz, quem descansou em casa) e o mundo nascendo não são fato do turno; a morte de alguém sempre é. Se ainda assim os fatos passam de 40 linhas, ficam as mais novas, e a primeira diz quantas ficaram de fora e como lê-las (`estado.py eventos N`). O evento gravado sem texto entra assim mesmo, com o número e o tipo dele. E o `estado.py mestre` recusa o texto vazio: o que o Mestre decide em cena vai para o registro com o que houve.

5.11 **A morte.** Todo mundo morre de vez. A regra é uma só, para a fome, a luta e a mão do Mestre: **o morto não fica com nada.**
- As peças dele (as vestidas, as guardadas e os núcleos) caem **soltas** onde ele morreu, com a história escrita e a marca de quem eram (`corpo`).
- As obras dele se desfazem: a matéria se perde; o núcleo cai com o resto.
- A carga e a prata ficam no estoque do lugar onde ele morreu. Num lugar com povo, o povo fica com elas. No ermo, ficam no chão, junto do corpo.
- **O que era de um morto não muda de mão sozinho.** Na vila ou no ermo, quem fica com as peças, a carga e a prata é decisão de cena: o Mestre registra por evento (`itens.py dono ITEM PESSOA`, `estado.py mestre`). No ermo, quem passa num rastro acha o corpo e lê o que ficou com ele (9.10), e mais nada. A família, o guarda e a herança são da etapa 6.
- **Morto não age:** todo ato dele é recusado antes de cobrar qualquer coisa. A `MESA.md` e o `RETOMAR.md` abrem dizendo quando e onde ele morreu, sem a lista de atos. A `MESA.md` diz o que ficou com o corpo (as peças, uma a uma) e para onde foram a carga e a prata, com quanto era: num lugar com povo, ficaram com o povo (entraram no estoque e no caixa do lugar); no ermo, no chão, junto do corpo. O turno fecha. O herdeiro é da etapa 6.

5.12 **Fora.** Quem saiu para o ermo (9.2) está lá, não no lugar onde mora, até voltar. Os atos da vila (dormir na pousada, trabalhar, treinar, comprar, vender, forjar, consertar) são recusados, para quem comanda a saída e para quem foi junto. No ermo come-se da própria carga.

5.13 **Vestir e guardar.** `ato.py vestir ITEM` empunha ou veste uma peça da pessoa; `ato.py tirar ITEM` a guarda. Não gasta bloco, e não se faz no meio de uma luta.
- A arma vai na mão (`arma`) ou de reserva (`arma2`); o escudo, no braço; a armadura, no corpo.
- A peça que estava no mesmo lugar vai para a guarda: a outra arma, o outro escudo, a armadura que cobre a mesma parte.
- A peça comprada, forjada ou achada chega **guardada**. A ficha de luta só conta o que está em uso.

5.14 **O relógio é um só, e o corpo de cada um.**
- **O tempo passa para o personagem, aja quem agir.** Quando o relógio anda por ato de outra pessoa (`quem=ID`), o corpo do personagem passa os mesmos blocos, no mesmo evento, como quem espera: a fome e o sono sobem, e a virada do dia cobra dele igual. As paradas do corpo valem para ele também: se ele cruza um limiar, ou cai no sono (5.2), o ato do outro para, e o comando diz por quê. Não vale para quem morreu, e não dobra quando o personagem já está no ato (vai junto na saída: aí o corpo dele já passa os blocos). A última linha do comando diz como ficou quem agiu e, embaixo, como ficou o personagem.
- **Quem não é o personagem cuida de si quando não está em cena** (o descanso em casa). Cada pessoa com ficha guarda o bloco em que o corpo dela foi mexido pela última vez (o último bloco em que esteve em cena). Quando ela volta a agir (um ato com `quem=`, a entrada numa saída com `com=`, a entrada numa luta), **antes de mais nada** o motor acerta, num evento só, o tempo que passou desde esse bloco:

| Desde o último bloco em cena passaram | O que muda |
| --- | --- |
| menos de 3 blocos | nada: ela ainda carrega o que a última saída deixou |
| 3 blocos ou mais | a fome, o sono e o cansaço voltam a zero (comeu e dormiu por conta própria) |
| cada 6 blocos inteiros (um dia) | além disso, uma noite dormida de cura (um décimo do PV máximo, a mesma do personagem: 5.3) e um dia de repouso nas feridas; a Mana de quem lança volta pela regra da tradição dela (14.3) |

  **Como contar:** o bloco em que ela voltou é o último em cena. Quem volta do ermo no bloco da noite (chega à meia-noite) e é chamada de novo às 8h passou 3 blocos: descansou (foram dois blocos inteiros em casa, o mesmo sono que refaz o personagem). Chamada às 4h, passou 2: não descansou. Chamada no bloco seguinte ao da volta, passou 1: vai como chegou.
  A noite de cura pede um dia: quem sai todo dia zera a fome, o sono e o cansaço, mas não ganha PV nem repouso na ferida enquanto não ficar um dia inteiro sem ser chamada.

  **O personagem nunca ganha descanso de graça:** ele come, dorme e paga. Quem está fora, no ermo, numa saída aberta, não está em casa: lá ninguém descansa assim.
  Não há rotina simulada (acordar, trabalhar, comprar: é da etapa 3). É só o acerto do corpo, feito quando a pessoa volta à cena; não gasta prata nem comida de ninguém. O evento ("Rute descansou em casa") não é fato do turno e não entra no `RETOMAR.md`. O `estado.py pessoa ID` e o `corpo.py ver ID` mostram a pessoa como ela volta à cena agora.
  Os números (3 e 6) moram no `tabelas_mundo.py` (`CASA_ZERA`, `CASA_NOITE`). No save de antes desta regra, quem não tem a marca conta como descansado (o corpo a zero), sem noite de cura.

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
| o mesmo homem com a arma uma categoria acima vence; com uma abaixo, perde | 80% ou mais | 88% e 91% |
| quatro lobos contra um nível 30 de conjunto Incomum: em campo aberto, e num corredor de um | 10 a 35%; 20 pontos a mais | 15% e 69% |
| a serpe contra quatro de nível 60: de conjunto Raro, e de conjunto Épico | 5 a 30%; 55 a 90% | 22% e 64% |
| o tamanho (pequeno, médio, grande, enorme): PV · alcance · quantos batem nele | para o lado certo | 100, 168, 252, 420 · 1, 1, 2, 3 casas · 2, 4, 6, 8 |
| cada traço, com ele e sem ele | 8 pontos ou mais | de 10 (agarra) a 31 (veneno, regenera) |
| o bicho comum ferido foge das lutas que perde | 30% ou mais | 31% |
| o encurralado e o chefe fogem; alguém se rende a um bicho | nunca | 0, 0 e 0 vezes |
| o bicho no chão ou de perna presa foge | nunca | 0 de 720 fugas (o golpe pelas costas segurou 26) |
| a luta de um contra um bicho do mesmo degrau (mediana) | 3 a 9 rodadas | de 3 a 5 |

Em B4, o conjunto Épico é o de gente gerada: no nível 60 a Vontade sustenta duas peças Épicas (2.9), e a armadura dorme. Com Vontade 80, os quatro vencem a serpe em 100%.
**A régua** (`bichos.py mede ESPECIE NIVEL CATEGORIA`) mede qualquer encontro em lutas de ensaio, sem guardar nada. O que ela mostra: na mesma categoria, o bicho sozinho de grau D ou C é moeda no ar, e o bando mata; com o conjunto uma categoria acima, o homem vence quase sempre; do grau B para cima, um homem só não basta.
**O teste de estresse** (`python3 estresse.py 1500`): 1.500 lutas ao acaso, 729 com bichos misturados, nenhum erro e nenhum invariante quebrado.

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
- **Pago ao ferreiro do lugar:** **2% do preço da peça por ponto**, em prata inteira (arredonda para cima: um ponto de uma peça Comum custa 1 de prata), que vai para o estoque do lugar; um bloco de espera a cada 10 pontos ou parte, **por peça** (mandar consertar quatro peças leva quatro blocos). A oficina conserta até a categoria do nível dela mais um (7.1). O preço da peça segue o tamanho dela (8.8): a armadura, o que cobre (consertar um elmo custa um quarto); a arma, a matéria que leva (consertar uma adaga custa um terço; um montante, cinco terços).

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

7.13 **Medido** (`python3 provas_oficio.py`; 15 de 15. A prova da Lendária julga duas coisas: o dia em que a primeira obra fecha, e a peça rara de propósito, que nasce em pelo menos uma e em menos da metade das vidas. Os números da tabela vêm de 21 rodadas: treze da medida, cinco da conferência e três do acerto). O dado é o de verdade, e a medida muda de uma rodada para outra: por isso a tabela diz o centro do que se viu ("cerca de") e a faixa vista. **Uma rodada nova pode sair um pouco fora da faixa vista; o que não pode é sair da meta.** O robô ferreiro vive de verdade: dorme na cama e paga uma noite por dia, come e paga, vive do jornal, faz 3,5 blocos de bancada por dia. Sobe um degrau de cada vez, e só abre a obra quando tem a mão que ela pede.
**Com que a escada vale:** na forja mestra (+4), com os quatro preparos (+8) desde o Dia 1, e com matéria e núcleo novos a cada obra.

| A primeira peça | Meta (o dia) | Medido (o dia em que metade das vidas já a tinha; na Lendária, o dia em que a primeira obra fecha) | A primeira obra fecha | Núcleos por vida | Com um núcleo só, nasce em |
| --- | --- | --- | --- | --- | --- |
| Rara | 15 a 30 | Dia 17 (em duas das 21 rodadas, Dia 20) | Dia 17 | (cerca de 1,7 leva de matéria, visto de 1,6 a 1,9; a pior vida, de 4 a 9) | |
| Épica | 45 a 80 | Dia 59 (numa das 21 rodadas, Dia 51) | Dia 51 | cerca de 2,5 (visto de 1,9 a 3,2; a pior vida: de 6 a 14) | cerca de um terço das vidas (visto de 20 a 52%) |
| Única | 130 a 200 | Dia 177 em treze das 21 rodadas; Dia 154 em cinco; Dia 189 numa; Dia 200 em duas, em cima do limite | Dia 131 | cerca de 3,5 (visto de 2,7 a 4,2; a pior vida: de 7 a 14) | cerca de um quarto das vidas (visto de 10 a 46%) |
| Lendária | 300 a 450 (a primeira OBRA fecha: a primeira tentativa); **e** a peça nasce, até o Dia 450, em pelo menos 1 e em menos da metade das 30 vidas | Dia 356, em todas as rodadas. **A peça é rara de propósito:** nasceu até o Dia 450 em 3 a 12 de 30 vidas | Dia 356 | cerca de 2,5 (visto de 2,2 a 2,8) | cerca de 12% das vidas (visto de 0 a 24%; a conta exata: 15%) |

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
- **O que a meta mede** são duas coisas. O dia em que a primeira tentativa fecha: Dia 356, no melhor caminho. E a raridade: a peça tem de nascer em pelo menos uma vida do robô e em menos da metade delas (se a chance subisse, ou se a peça deixasse de nascer, a prova falharia). Até o Dia 450 cabem duas tentativas, e a peça nasce em cerca de um quarto das vidas do robô. Em média, uma Lendária custa quatro tentativas ao melhor ferreiro do mundo: perto de 280 dias de bancada e quatro núcleos Lendários.
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

8.13 **Medido** (`python3 provas_mercado.py`; 17 de 17). Toda prova confere que a soma da prata do mundo fecha. Os números da decisão do jogador estão escritos nas provas: pelas peças a loja paga de 40 a 60% (a espada Rara: 432 a um Leigo, 648 a um Lendário em comércio; 432, 302, 43 e 72 pela nova, a gasta, a quebrada e a sob medida).

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
- **Com a loja pagando 40% pelas peças** (decisão do jogador), rende cerca de 4,7 nos 5 primeiros dias: é a matéria de começo (4 de metal e 2 de madeira) virando uma alabarda, que a loja paga por 20, e pouco mais. Depois disso quase nenhuma peça paga a matéria, e o ferreiro vive do jornal. A exceção é moeda no ar: um arco Incomum que dá certo paga 72 por cerca de 41 de madeira, com 52,5% de chance de dar certo.
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
- **Quem vai junto cuida de si** (5.14). Ao entrar na saída, o tempo que ele passou na vila é acertado antes de mais nada: com 3 blocos ou mais desde o último bloco em cena (dois blocos inteiros em casa), vai de corpo zerado (e, a cada 6, com uma noite de cura); com menos, leva o que a última saída deixou. **Se não vai inteiro** (ferida aberta, PV abaixo de 90%, ou o corpo cobrando pena ou fôlego), a mesa diz ao abrir a saída, e a `MESA.md` traz o estado dele enquanto a saída está aberta.
- **Com a saída aberta, a pessoa está fora** (5.12): os atos da vila são recusados, para ela e para quem foi junto. No ermo come-se da própria carga. **Quem vai junto e tem comida na carga come sozinho** quando a fome dele chega ao primeiro limiar (fome 4), e sai uma linha na mesa; o personagem come quando o jogador manda.
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

9.17 **Medido** (`python3 provas_caca.py`; 32 de 32: as 30 de antes e as duas de quem vai junto, 9.2). O dado é o de verdade: as medidas mudam de uma rodada para outra. A coluna "Medido" diz o centro do que se viu ("cerca de") e, entre parênteses, a faixa vista em 23 rodadas do banco (15 da medida, 5 da conferência, 3 do acerto). **Uma rodada nova pode sair um pouco fora da faixa vista; o que não pode é sair da meta.**
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

**O que a meta não mede, e a mesa sente.** Na loja, o que o caçador tira vale cerca de 5 de prata por dia (visto de 4,6 a 5,2); o conserto leva perto de 0,7; a cama e a comida, 3. **No bolso dos que chegam vivos fica cerca de +1,2 por dia** (visto de +1,0 a +1,4; o diarista fica com +1,00), e morre, em média, um em cada cinco no mês. O cauteloso, que só encurrala a corça sozinha e do alto, tira cerca de 1,8 diária (visto de 1,7 a 1,9) e fere-se em cerca de 1,7% das saídas (visto de 1,0 a 2,6%: quase sempre abaixo da faixa). A caça de começo paga pouco mais que a diária, e mata: o jogador decidiu que fica assim (é para quem aceita o risco).

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
- **Gente sem rotina.** O relógio é um só e o tempo passa para o personagem, aja quem agir; quem não é o personagem descansa em casa quando não está em cena (5.14). Mas ninguém além do personagem tem rotina: não acorda, não trabalha, e o descanso em casa não gasta prata nem comida do lugar (o personagem paga a cama e a refeição; o companheiro, não). **Quem sai todo dia não sara:** dois blocos em casa zeram a fome, o sono e o cansaço de quem vai junto, mas a noite de cura e o dia de repouso da ferida pedem um dia inteiro sem ser chamado; o personagem, que dorme toda noite, recupera um décimo do PV por noite. A rotina de verdade é da etapa 3.
- **Não há viagem.** O ermo é o vizinho, a um número fixo de blocos.
- **Não há peso.** A carga não tem limite, e a comida não estraga: quem compra na colheita e vende na entressafra ganha de 38 a 62% em meio ano, sem trabalho e sem risco.
- **A taverna tem preço fixo:** 1 de prata o ano inteiro. O mercado sabe dizer o que a refeição valeria no dia (`mercado.refeicao`), e ninguém cobra isso ainda.
- **A prata do lugar não se repõe.** Uma vila de 400 tem 2.000: quatro peças Raras de tipos diferentes levam 1.274 (432, 345, 276 e 221: a loja farta, 8.8), e as nove de preço de tabela levam 1.866. Conforme o tipo e a ordem, a prata acaba entre a quarta e a décima terceira peça, ou não acaba: vendendo primeiro o montante, a alabarda e o malho (1.756), a quarta já é recusada; começando pela adaga, vendem-se as quinze e sobram 136.
- **A coleta de quem já tem mão não tem meta.** A de começo tem (K1 a K4, 9.17). A do Treinado no interior foi só medida: rende de 6,5 a 9,8 diárias por dia no primeiro mês.
- **O povo não passa fome,** e o bicho não vem à vila: é das frentes.
- **Não há tempo de céu** na caça: só o escuro entra sozinho na luta.
- **A morte não tem herdeiro** (etapa 6). Na vila e no ermo, quem fica com o que o morto largou é decisão de cena, por evento (5.11).
- **A caça de começo é para quem aceita o risco** (decisão do jogador). No bolso sobra ao caçador o mesmo que ao diarista, um em cada cinco morre no mês, e a corça escoiceia em vez de fugir. Fica assim.
- **Quem vai junto não pede paga.** Vai quando é chamado e leva a parte dele do despojo (9.10). Se o companheiro pede prata, recusa o perigo ou cobra depois, decide o jogador.

---

## 10. Os dons e os talentos (etapa da magia)

10.1 **Dois botões na pessoa, para todo caminho.** O **talento** diz a pressa de aprender e até onde a mão sobe; não soma em conta nenhuma. O **dom** diz o poder: soma na conta como maestria que ninguém treinou. Os dois nascem com a pessoa e não mudam. Quem não tem nada de especial é a pessoa de antes desta etapa: os blocos de sempre, a conta de sempre.

10.2 **Os caminhos (16).**

| Tipo | Caminhos | O que o talento apressa |
| --- | --- | --- |
| mãos de arma | `fio` (adaga, espada, machado, montante) · `haste` (lança, alabarda) · `peso` (maça, martelo, malho) · `tiro` (arco, besta) | os blocos de treino de cada arma daquela mão |
| ofícios | `forja` · `couro` · `caça` · `coleta` · `comércio` · `cura` · `alquimia` · `encanto` | os blocos de bancada, de procura, de coleta; os dias de negócio |
| tradições | `arcano` (o mago) · `fé` (o clérigo) · `verde` (o druida) · `pacto` (a bruxa) | os blocos de estudo da tradição e de cada feitiço |

O soco não é de mão nenhuma. A ficha só guarda o que não é Comum: `talento: {"fio": 1, "arcano": -1}`, `dom: {"forja": 2}`.

10.3 **O talento.**

| Grau | Nome | Blocos de cada grau de maestria | Nas armas (Iniciante, Treinado, Mestre, Lendário) | Até onde a mão sobe | Quantos nascem assim, por caminho |
| --- | --- | --- | --- | --- | --- |
| −2 | Negado | o dobro | 80 · nada | Iniciante | 2 em 100 |
| −1 | Lerdo | uma vez e meia | 60 · 240 · 750 · nada | Mestre | 10 em 100 |
| 0 | Comum | os de sempre | 40 · 160 · 500 · 1.500 | Lendário | 76 em 100 |
| +1 | Jeitoso | dois terços | 27 · 107 · 334 · 1.000 | Lendário | 10 em 100 |
| +2 | Prodígio | a metade | 20 · 80 · 250 · 750 | Lendário | 2 em 100 |

- Os blocos arredondam para cima. O feito que Mestre e Lendário pedem não muda: o talento apressa os blocos, não dispensa o feito.
- Vale em toda escada: as armas, a forja e o couro (50, 150, 375, 1.000 de bancada), a caça e a coleta, o comércio (os dias de negócio), a alquimia e o encanto (a tabela da forja) e as tradições (a das armas).
- O teto não tira o que a pessoa já tem: só a impede de subir mais. Quem chega ao teto com os blocos de cima lê "a mão não sobe mais: o talento para em Mestre".
- Qualquer um aprende magia: o Negado também, até Iniciante, com o dobro dos blocos.

10.4 **O dom.**

| Grau | Soma na conta do caminho | Quantos nascem assim |
| --- | --- | --- |
| Dom | +1 | 45 em 1.000 pessoas |
| Grande Dom | +2 | 5 em 1.000 pessoas |

A pessoa tem no máximo um. O caminho sai do dado entre os 16, com peso 3 onde ela já é Jeitosa ou Prodígio. Cada caminho tem o seu nome à mesa (a mão do fogo, o faro, a língua do negócio, a mão que fecha, a centelha, a graça...).

| Caminho | Onde o dom soma | O que não dá |
| --- | --- | --- |
| mão de arma | no acerto com as armas dessa mão; e metade na Defesa | a ação e a reação a mais (são da maestria) |
| tradição | na Conjuração; metade na Firmeza; o mesmo na Mana | abrir feitiço de grau maior |
| ofício de bancada (forja, couro, alquimia, encanto) | no teste da obra, como um preparo que nasce com a pessoa: **preparo e dom juntos não passam de +8** | a chance da Lendária não sobe: o melhor ferreiro possível segue acertando 1 vez em 4 |
| caça, coleta, cura | no teste do rastro, da coleta, do tratamento | a mão que a matéria pede |
| comércio | 2,5 pontos (Dom) ou 5 (Grande Dom) no que a loja paga, sem passar de 80% pelos bens e 60% pelas peças | |

O dom de tradição soma também na Mana máxima de verdade; a mesa só mostra a Mana que a pessoa conhece, sem o dom que ela ainda não viu (na MESA, na ficha e no quadro da luta).

10.5 **Como nascem.** Pelo dado do mundo (mesma semente, mesma gente): um d100 por caminho (até 2, Negado; até 12, Lerdo; até 88, Comum; até 98, Jeitoso; 99 e 100, Prodígio) e um d1000 para o dom (até 5, Grande Dom; até 50, Dom). **O personagem do jogador** escolhe uma **inclinação**: naquele caminho o d100 rola duas vezes e vale o melhor (Jeitoso ou mais: perto de 23 em 100, em vez de 12). A vila de teste nova nasce assim (`vila_teste.py PASTA ... inclinacao=CAMINHO`); quem já existia ganha os seus pelo `vila_teste.py magia`.

10.6 **Ninguém nasce sabendo.**
- **O talento aparece fazendo:** 20 blocos no caminho depois de rolado, a MESA, em "Você", diz: "Com as armas de fio você pega depressa (Jeitoso): o que os outros firmam em 160 blocos, você firma em 107." Antes disso, só o Mestre sabe.
- **O dom fica escondido** até o primeiro teste em que foi ele que fez a diferença. Escondido, ele entra no dado, mas não na conta que vai à mesa: a mesa vê o total sem ele, e o veredito é o mesmo. Quando decide, a saída diz "sem o dom, não passava" (ou "saía pior", na bancada), e a MESA passa a dizê-lo. Na luta, o golpe que só passou por causa dele diz "acerta por pouco: sem o dom, errava". No comércio, a primeira venda em que ele pagou a mais diz "o comprador paga mais do que costuma: você tem jeito para o negócio". Também se mostra quando alguém o lê (o feitiço `ler`, ou um clérigo).
- Dos outros, a MESA não diz nada; o SÓ O MESTRE mostra o talento e o dom de quem está com o personagem.

10.7 **Dentro da lei "o item decide"** (medido no banco, 4.000 lutas por linha, nível 50, tudo Raro; com 8.000: o Dom 56%, o Grande Dom 61%): o Dom contra o gêmeo vence de 51 a 58%; o Grande Dom, de 54 a 64%; o Grande Dom contra o gêmeo com a arma uma categoria acima, até 15%; o Mestre com Grande Dom contra o Lendário sem dom, de 42 a 58%. O Grande Dom vale um grau de maestria e nada mais; uma categoria de peça vale muitas vezes isso.

10.8 **A escada pelo talento** (a conta dos blocos: 3,5 blocos de bancada por dia; a obra só abre com a mão que pede; 2 blocos de treino de arma por dia):

| Talento na forja | A 1ª obra Rara fecha no dia | Épica | Única | Lendária | Mestre numa arma |
| --- | --- | --- | --- | --- | --- |
| Negado | 32 | não abre | não abre | não abre | nunca |
| Lerdo | 24 | 72 | 184 | não abre | Dia 375 |
| Comum | 17 | 51 | 131 | 356 | Dia 250 |
| Jeitoso | 13 | 37 | 95 | 260 | Dia 167 |
| Prodígio | 10 | 30 | 77 | 213 | Dia 125 |

O prodígio anda uma categoria à frente do comum em boa parte do caminho, e nunca duas. O que tranca segue sendo o núcleo e a mão.

10.9 **A cena.** Zeca, o aprendiz da forja, tem um Grande Dom que ninguém conhece. Na primeira adaga, os dados dão o bastante para a conta da mesa errar por 1; o dom (preparo 4 e dom 2, dentro do teto de +8) faz passar. A saída diz: "Foi o dom que fez a diferença: há alguma coisa nas mãos de Zeca." A partir dali a MESA dele diz "Há alguma coisa em você: a mão do fogo (a forja), um Grande Dom".

---

## 11. A magia na luta (etapa da magia)

Este capítulo diz como a magia entra na luta: quem lança, a conta, a Mana, o tempo de lançar, o que dá errado, os estados com prazo, a poção bebida na luta, a peça encantada, os nove traços novos e as fases do chefe. Os números moram no `tabelas_magia.py` (os da luta) e no `tabelas.py` (a base comum: os feitiços, o foco, a guarda, a Firmeza, a Mana e a cura). A regra mora no `magia.py`, e o `luta.py` a chama.

**A pessoa comum é a de hoje.** A magia só liga numa luta em que alguém traz feitiço, foco, amuleto, peça encantada, poção, elixir, veneno na lâmina, traço novo, fases ou pena de maldição. A luta sem nada disso é a de sempre, dado por dado (conferido com semente fixa).

### 11.1 Quem lança

Lança quem sabe feitiços: gente, povo (goblin, orc...) ou bicho com o traço **lança**. Cada feitiço é de uma tradição (o mago, `arcano`; o clérigo, `fé`; o druida, `verde`; a bruxa, `pacto`); a luz é de todas.

- **A Conjuração** (o acerto de quem lança) = a mão da tradição do feitiço + o dom nela + metade do bônus do atributo dela (arcano e pacto: Afinidade; fé: Vontade; verde: Percepção) + o bônus do foco. A pena do corpo (fome, sono, cansaço, maldição) entra, como em todo teste.
- **O foco** é a arma de quem lança: varinha e cajado (arcano), cajado (verde), símbolo (fé), talismã (pacto). O cajado vale 1,25, como toda arma de duas mãos. Foco de outra tradição rende uma categoria abaixo. Sem foco, lança-se com as mãos: como foco Comum, com −4. Faltou o atributo que o foco pede: −1 na Conjuração a cada 5 pontos.
- **As mãos do foco.** A varinha, o símbolo e o talismã vão na mão do escudo: lança-se de arma e escudo. O **cajado pede as duas mãos**: ele é a arma (bate como maça leve, 1d6 de impacto, com a mão de maça; apara com o bônus da categoria); a arma de antes fica de reserva e o escudo não entra.
- **O bicho que lança** usa o corpo como foco (a categoria dele) e o instinto como mão.
- **A mão é conselho, não tranca.** Cada grau pede uma mão (grau 1, Iniciante; 2, Treinado; 3, Mestre; 4, Lendário). Abaixo dela o lance é **forçado**: −4 por grau de mão que falta.

### 11.2 A conta (a do aço, linha por linha)

| | O aço | A magia |
| --- | --- | --- |
| quem bate | o acerto | a Conjuração |
| contra | a Defesa | o que **voa** (seta, lança de fogo, raio, castigo, espinho, sangria): a Defesa inteira, como um tiro. A **área** (bola de fogo): a Defesa sem escudo e sem arma. O que **prende, assusta ou amaldiçoa**: a **Firmeza** |
| o tamanho | dado × 4 × valor da arma ÷ proteção da parte | dado × 4 × valor do foco ÷ **guarda** × força do feitiço (1 + 0,03 por ponto de bônus do atributo da tradição) |
| a proteção | a armadura da parte atingida | **a guarda**: o amuleto, ou 0,6 do valor da armadura do tronco, o que for maior (sem nada, um terço). O material e a parte do corpo não contam |
| crítico | dados em dobro, proteção pela metade | dados em dobro, guarda pela metade |

- **A Firmeza** (a Defesa da cabeça) = 22 + metade do bônus de Vontade + metade da maior mão da pessoa + metade do dom de tradição + o melhor entre o bônus do amuleto e metade do bônus da armadura do tronco; mais o **calejo**: cada controle que pega soma 4 até o fim da luta (ninguém fica preso a luta inteira).
- O feitiço que voa sente o tempo, o alto, a cobertura e a gente no caminho, como um tiro. O feitiço que tira um quarto do PV abre ferida, numa parte sorteada; o resto (o sangue, a queda, a moral) é o de sempre.
- **O amuleto gasta:** 1 por luta em que guardou, e 1 a cada feitiço de foco maior que ele. **O foco gasta** 1 por luta em que lançou e 1 a cada retrochoque. A zero, não valem. O desgaste volta ao estado como o das outras peças.
- **A sintonia:** foco e amuleto Épicos ou melhores ocupam lugar, como toda peça alta; **toda peça encantada ocupa lugar, de qualquer categoria**. A que dorme rende uma categoria abaixo, e o encanto dela não sai.

### 11.3 A Mana

- O máximo: (Afinidade + Vontade) ÷ 10 + a mão da tradição + o dom nela. O custo é o do `tabelas.FEITICOS`: 2 por grau (o truque, 1); o que prende, afugenta, amedronta ou cura, de grau 1, custa 3 (prender, raízes, afugentar, medo, cura); a área, 2 a mais (a bola de fogo e a guarda, 6). A luz e a névoa custam 1 por rodada para durar.
- **Na luta, volta 1 no começo de cada turno** de quem lança (de quem sabe feitiço; quem não sabe não ganha Mana na luta).
- **Lançar no osso:** sem Mana, só por ordem do jogador (`osso`): cada ponto que falta custa 5% do PV máximo, e o lance é forçado.
- O que sobrou volta ao estado no fim da luta.

### 11.4 O tempo de lançar e o que dá errado

| Grau | Ações | Observação |
| --- | --- | --- |
| truque e grau 1 | 1 | |
| grau 2 | 2 (o turno inteiro) | |
| grau 3 | 2, e **longo**: sai no começo do turno seguinte | quem canaliza e apanha testa a concentração |

- **Lançar com o inimigo colado** dá a ele um golpe livre. Se o golpe fere, quem lança testa a concentração; falhou, o feitiço se perde (a Mana já foi).
- **A concentração:** 2d20 + bônus de Vontade + mão da tradição contra 28 (32 se o golpe abriu ferida). Quem cai, vai ao chão, fica atordoado ou é agarrado perde o feitiço longo sem teste.
- **O retrochoque:** dois 1 no dado (1 lance em 400); no lance forçado, basta um 1 (1 em 10). Quem lança vai ao chão, perde 1 ação, e o foco perde 1. No forçado, leva ainda o próprio feitiço contra a própria guarda.
- A armadura cobra o fôlego dela na rodada em que se lança, como quando se golpeia. Lançar não gasta fôlego.

### 11.5 Os estados com prazo (lista fechada)

| Estado | O que faz | Quanto dura |
| --- | --- | --- |
| preso (prender, raízes) | não anda, não recua, não troca de lugar; bate e lança | 2 turnos dele |
| guardado (escudo) | +4 na Defesa | 4 turnos dele |
| benzido (bênção) | +2 no acerto, +2 na coragem | até o fim da luta (o brado do chefe: 3 rodadas) |
| mau-olhado | −4 no acerto, na Defesa e na Conjuração | até o fim da luta |
| com seiva | volta 5% do PV por rodada | 5 rodadas |
| com a Mana atada (nó) | a Mana não volta, e cada feitiço custa 1 a mais | 4 turnos dele |
| guardado pela fé (guarda) | conta como tendo amuleto da categoria do foco | 4 turnos dele |
| cego | −4 no golpe, −8 no tiro e no feitiço que voa | o prazo de quem o pôs |
| com fúria (poção) | +2 no acerto e −2 na Defesa, se a arma é até a categoria da poção | 5 rodadas |
| enjoado (poção a mais) | −2 em tudo | até o fim da luta |

- **As penas de magia não somam:** de mau-olhado, veneno e maldição vale a pior. Essa pior soma com a pena do corpo.
- **O campo:** a luz tira o escuro e a névoa põe neblina ou lama, enquanto quem lançou paga 1 de Mana por rodada e está de pé. Valem para os dois lados.
- **O medo e o afugentar:** se o lance pega a Firmeza, o alvo testa a coragem contra 26 (o afugentar, só no bicho que não é chefe). Quem o jogador comanda só fraqueja, e a luta para.

### 11.6 Os feitiços na luta

Os nomes, as tradições, os graus e o custo são os do `tabelas.FEITICOS`. Na luta:

- **arcano:** seta (1d8, a 8 casas) · prender (preso 2 turnos) · escudo (em si ou num aliado a 4 casas) · lança de fogo (2d8; a ferida que abre queima 5 rodadas) · bola de fogo (1d8 em até 4 na casa escolhida, amigo ou inimigo) · raio (2d10, longo; se abre ferida, atordoa 1 ação).
- **fé:** cura (1d8 × 6 × 3 elevado a categoria do foco menos categoria da ferida mais funda; com o teto do dia) · bênção · amparo (estanca o sangue, tira veneno até a categoria do foco, firma quem caiu) · castigo (2d8 em quem é maldito: amaldiçoado, com peça maldita, que amaldiçoa ou imaterial; 1d4 nos outros) · guarda (até 4 na casa de quem lança).
- **verde:** raízes (preso 2 turnos) · espinho (1d6 e veneno: um quarto do golpe por 3 rodadas) · névoa (neblina ou lama) · afugentar · seiva · chamar (longo; só num ermo contado: um bicho do ermo, até a categoria do foco, vem lutar ao lado. Só atende o bicho de verdade: os do capítulo 6 e as criaturas que são fera, a harpia e o lobisomem; o povo e os mortos não ouvem o druida. A luta do mundo sabe o ermo: o da saída de caça, ou o lugar de quem luta). O druida cujo ermo do laço foi caçado até o fim perde 2 ou 4 na Conjuração do verde (capítulo 14), também na luta.
- **pacto:** mau-olhado · medo · sangria (1d6 a 4 casas; quem lança recupera metade do que tirou: não é cura) · nó.
- **Ritos, fora da luta:** quebrar maldição, ler e praga.

### 11.7 Beber na luta e a cura

- **Beber é 1 ação.** Dar de beber a um aliado colado (ou caído ao lado), também. A poção do Comum ao Raro sai da carga; o elixir (do Épico para cima) some.
- **Quantas o corpo aguenta:** Vigor ÷ 30 por dia (no mínimo 1), contando as que bebeu fora da luta no mesmo dia. Cada uma além disso pede 2d20 + bônus de Vigor contra 24 + 4 por poção a mais (o dado vai à mesa, passe ou falhe): falhou, não faz nada, e enjoa; o enjoo segue fora da luta até o fim do bloco, como o da poção bebida fora dela.
- A cura (de poção, de feitiço e da seiva) segue a lei ao contrário e **nunca devolve mais que metade do PV máximo no dia**, tudo somado.
- **Quem caiu e recebe cura fica firme** (não morre no chão), mas não se levanta nesta luta.
- Na luta se bebem: cura, antídoto (tira o veneno até a categoria dele), Mana (4, 8, 12, 16), guarda (conta como amuleto da categoria até o fim da luta) e fúria. O veneno de lâmina se passa na arma fora da luta; a vigília e a quebra-maldição se bebem fora dela.
- **O veneno na lâmina:** a primeira vez que a arma tira sangue, a vítima perde por rodada um quarto do golpe, por 3 rodadas, com o −2 no acerto do veneno; numa lâmina acima da dose, um terço disso por degrau. A dose acaba ali.
- **A ferida funda** (a maior categoria que tirou PV desde o PV cheio) é contada em toda luta, com ou sem magia: o sangue e o veneno contam como Comum. É ela que a cura confere.

### 11.8 A peça encantada

O dono solta o feitiço gravado **uma vez por luta**, com as ações do feitiço e sem Mana. A peça vale como foco **um degrau abaixo** da categoria dela. A Conjuração é 2 por grau de quem gravou + metade do bônus de Afinidade do dono + o bônus desse foco. A peça que dorme (sintonia) não solta. O encanto solto volta ao estado (descarregado; carrega de novo fora da luta).

### 11.9 Os nove traços novos

| Traço | Na luta |
| --- | --- |
| resiste | a guarda contra a magia é o corpo inteiro (não 0,6), e a Firmeza leva o bônus inteiro dele |
| imaterial | a arma sem encanto e sem bênção conta uma categoria abaixo; o feitiço e a peça encantada contam inteiros; não vai ao chão nem é agarrado |
| amaldiçoa | a ferida que ele abre põe uma maldição da categoria do corpo, no passo 1 (volta ao estado) |
| lança | lança os feitiços dele pelo instinto, com o corpo de foco |
| sem vida | não sangra, o veneno não pega, não testa a coragem, não cansa, não faz a ação a mais; a zero de PV se desfaz |
| ossos | o corte e a ponta valem metade; o impacto, inteiro |
| dreno | recupera metade do que o golpe do corpo tira (o sopro também é golpe do corpo: drena de cada um que pega) |
| ardente | quem o golpeia de perto leva o fogo de volta (o teto do "devolve" da categoria); a ferida que o corpo abre queima 5 rodadas |
| noturno | o escuro não tira nada do golpe, do tiro nem do feitiço que voa |

### 11.10 As fases do chefe

O chefe pode trazer fases. Ao cruzar o limiar do PV (por exemplo, abaixo de metade), ele muda uma vez por fase: ganha e perde traços, aprende feitiços, recobra Mana, dá o **brado** (os do lado dele ficam benzidos por 3 rodadas) e **ergue** mortos: até N dos mortos mais perto levantam do lado dele, como "sem vida", com metade do PV. O morto erguido é outro lutador, sem registro no mundo; o morto segue morto. A luta para e pergunta.

### 11.11 A luta para e pergunta, e as ordens

**Paradas novas:** o outro lado começa um feitiço longo · quem o jogador comanda fica preso, leva mau-olhado, tem a Mana atada, falha o medo, perde um feitiço, sofre retrochoque, leva uma maldição · a Mana de quem ele comanda cai abaixo de um terço · ele não tem Mana para o feitiço da ordem · o campo muda · o chefe muda de fase · um da casa cai e há cura ao alcance (a frase diz quem).

**Ordens novas, só para quem o jogador comanda** (quem ele comanda não lança, não bebe e não solta encanto sozinho):
- `lancar FEITICO [em ALVO | casa N] [sempre] [osso] [neblina|lama]`: uma vez (depois volta a ordem de antes); com `sempre`, até a Mana acabar, o alvo cair ou vir outra ordem. Fora do alcance, anda até ele.
- `beber POCAO [em ALIADO]`: a poção (`cura`, `cura:1`, `antídoto`...).
- `usar [PECA] [em ALVO | casa N]`: solta o encanto.

A ordem é conferida antes de qualquer dado: o feitiço que a pessoa não sabe, o rito, o alvo do lado errado, a casa para quem não é de área, a poção que ela não leva ou que não se bebe na luta, o encanto que já saiu: tudo é recusado com a frase.

**Os outros** (aliados e inimigos) seguem uma regra curta (`magia.escolhe`): a peça encantada quando vale; a poção de cura abaixo de metade do PV (nunca além do que o corpo aguenta); cura quem está abaixo de metade; protege, benze (só sem ninguém colado) e guarda; prende quem ainda vem chegando; a área só onde há dois inimigos ou mais e nenhum amigo; o resto, o maior dano que a Mana paga. Quem só fere de longe e não tem o que lançar espera a Mana voltar.

**O quadro** ganha, por pessoa, a Mana, o que canaliza e os estados com prazo; e a linha do campo. **A ficha** ganha a linha da magia (a Mana, o que sabe, a Conjuração, a Firmeza, o foco, o amuleto, o encanto), só de quem tem magia.

### 11.12 O que a luta devolve ao estado

Do lutador do mundo: a Mana que sobrou, as poções bebidas e as doses gastas, o elixir bebido, o encanto solto, a dose da lâmina, a maldição posta nele, o dom que decidiu um lance, a ferida funda, as poções e a cura do dia, a dívida do feitiço de pacto (grau 2 para cima: o nó soma 1), o enjoo e o desgaste do foco e do amuleto. Tudo num evento só.

**O que vem do mundo para a luta:** a bênção dada antes dela (`magia_mundo.py lancar bênção`: a luta que abrir até o fim do bloco seguinte tem a pessoa benzida), a poção de guarda bebida antes (vale amuleto da categoria dela até o fim do bloco), a pena do laço do druida e a pena das maldições. Quem vem de um cenário, fora do mundo, veste também foco e amuleto (`"foco": ["cajado", "Raro"]`, `"amuleto": "Raro"`).

### 11.13 As metas (o banco: `python3 provas.py 600`; só a magia: `python3 provas.py 600 magia`)

Nível 50, tudo Raro, quando não diz outra coisa. 600 lutas por meta no duelo e no grupo, mais onde a faixa é estreita.

| Meta | Faixa | Deu (a rodada final da integração) |
| --- | --- | --- |
| M1 mago contra mago | 44 a 56% | 48% |
| M2 mago contra o guerreiro com amuleto: longe, perto, colado | 28 a 45 · 12 a 28 · 4 a 16 | 43, 22, 14 |
| M3 sem amuleto, o mago ganha | 15 a 35 pontos | +24 e +20 |
| M4 o foco uma acima: longe, perto | 85 a 100 · 65 a 90 | 96 e 82 |
| M5 contra o amuleto uma acima · o conjunto uma acima | 2 a 18 · 0 a 8 | 10 e 1 |
| M6 nível 50, foco duas acima, contra nível 500: longe, perto | 65 a 92 · 15 a 40 | 84 e 26 |
| M7 o mesmo com o foco uma acima, de longe | 5 a 30 | 24 |
| M8 nenhum feitiço mata de PV cheio sem crítico entre iguais; mediana até 45% (a seta, 20%) | sim | sim (seta 16%, raio 39%) |
| M9 a Mana seca na rodada · a volta rende a mais | 6 a 10 · 25 a 50% | 8 · +36% |
| M10 o mago no grupo: sem área · com área · contra quem não tem amuleto | 40 a 55 · 52 a 70 · 75 a 92 | 52, 64, 82 |
| M11 o mesmo no corredor | 50 a 68 | 52 |
| M12 o clérigo na linha: campo, corredor; benzendo antes | 42 a 58 · 48 a 64 · 5 a 14 | 45, 52, +13 |
| M13 o druida · a bruxa | 45 a 62 · 42 a 58 | 51 · 52 |
| M14 a bruxa sozinha, de longe | 5 a 20 | 13 |
| M15 o longo sob uma flecha · duas | 15 a 35% · 25 a 50% | 34 e 46 |
| M16 com um guarda de escudo na frente | 3 pontos a menos ou mais | 5,5 a menos |
| M17 o retrochoque: comum, forçado | 0,1 a 0,5% · 8 a 12% | 0,27 e 9,65 |
| M18 o mago contra 8 · 12 soldados | 55 a 85 · 35 a 70 | 78 e 52 |
| M19 a pantera longe, perto; o trasgo | 35 a 60 · 0 a 12 · 30 a 55 | 47, 5, 42 |
| M20 cada traço novo, com e sem | 8 pontos ou mais | todos (de 9 a 74) |
| M21 o controle pega · calejado duas vezes | 55 a 75% · 25 a 40% | 66 e 30 |
| P1 a P4, P9 a poção e o veneno | as do projeto | todas passam |
| E1 a E3 a peça encantada | as do projeto | todas passam |
| e mais: as fases do chefe, a ordem, a pessoa comum, a luta que volta ao estado (a maga ferida bebe, vive, e a Mana, a poção e o foco voltam conferidos) | sim | sim |

**A bruxa no grupo** falhava com o mau-olhado do projeto (−2: 37 a 40%, faixa de 42 a 58). O projeto a mediu com um cajado que valia inteiro, e o cajado não é foco do pacto: com o talismã (× 1,0, sem aparar), ela ficava atrás. Medido, com 4.000 lutas por linha: o mau-olhado de −3 a põe em 42 a 43% (raspando a faixa); a sangria de 2d6 a põe em 43%, mas sozinha ela passa a 29% (a M14 pede até 20); o alcance da sangria e a ordem da regra curta, nada. **O mau-olhado passou a tirar 4** no acerto, na Defesa e na Conjuração: a bruxa no grupo dá 49 a 52%, e sozinha 13 a 14%. Dois chefes que lançam o mau-olhado passaram da faixa deles com isso e foram acertados (capítulo 15).

### 11.14 O que mudou do projeto, e por quê

- **O benzido dá +2 na coragem**, não +4: com +4, benzer os quatro antes da luta rendia 15 pontos, acima da meta (5 a 14).
- **Quem caiu e recebe cura não se levanta nesta luta** (fica firme, e a cura conta): o clérigo que levantava os caídos no corredor passava da faixa.
- **O preso do feitiço não troca de lugar** no corredor (o da perna presa segue como hoje).
- **Quem cai, vai ao chão, fica atordoado ou é agarrado perde o feitiço longo sem teste** (a regra do projeto, que a medida do projeto não tinha): a flecha corta mais feitiços do que o projeto dizia, e as metas M15 e M16 contam a concentração e o corte juntos.
- **A Firmeza leva o melhor entre o amuleto e metade da armadura**, na luta e fora dela (a base comum, `tabelas.firmeza`, levava o amuleto mesmo quando ele era menor: um amuleto Comum baixava a Firmeza de quem veste armadura Rara, também contra a maldição).
- **O mau-olhado tira 4, não 2** (acima: a bruxa no grupo).

---

## 12. A bancada da magia: a alquimia e o encanto (etapa da magia)

12.1 **Uma bancada só, quatro lugares.** A obra de vários dias é a da forja (capítulo 7): a matéria entra quando ela abre, os blocos somam de um dia para o outro, o ato para quando o corpo pede, e o teste sai uma vez, quando os blocos fecham. O que muda é a bancada e a mão:

| Ofício | A bancada (campo do lugar, 0 a 4) | O que faz | A escada da mão |
| --- | --- | --- | --- |
| forja, couro | `oficina` | arma, armadura, escudo | 50 · 150 · 375 · 1.000 blocos |
| alquimia | `botica` (panela, botica de vila, botica de cidade, laboratório, grande laboratório) | a leva de poção | a mesma |
| encanto | `runas` (pedra riscada, mesa de runas, oficina de runas, grande oficina, oficina mestra) | o foco, o amuleto, a gravação de um feitiço numa peça | a mesma |
| fé | `santuario` | o jornal do santuário (a prece, o voto e os ritos são do capítulo 14) | a das armas |

O teste é sempre o da forja: **2d20 + a maestria do ofício + Afinidade ÷ 10 + a bancada + o preparo, contra 28 + 6 por categoria.** O preparo são quatro, de +2 cada, até +8, cada um com alcance (a categoria mais alta a que serve): na alquimia, a receita, o ajudante, o fogo e a vidraria; no encanto, a receita, o ajudante, a tinta e a pedra. O DOM do ofício entra dentro do teto de +8 (capítulo 10). Sem a bancada no lugar, a obra não abre.

12.2 **A leva.** Rende 2 doses do Comum ao Raro (bens, na carga: `cura:0`) e 6 elixires do Épico para cima (itens do Livro de Itens, contados no mundo; a leva pede matéria Rara e um NÚCLEO da categoria: um núcleo Épico vira seis elixires ou uma espada). Blocos pesados: 1, 3, 9, 27, 81, 243. Falhar por 1 a 4: sai uma categoria abaixo (a Comum sai aguada: 1 dose). Por 5 ou mais: a matéria some, e o núcleo também. De Mestre para cima a mão pede o feito: uma leva Épica nascida (Mestre), uma Única (Lendário).

12.3 **As nove receitas.** A matéria vai na categoria da leva. A receita custa 8 de preço de base na Comum (vezes 6 por categoria), dois terços do que valem as 2 doses; a quebra-maldição custa mais (14 na Comum, 54 na Incomum, 294 na Rara: as 2 de água benta valem 3 cada e não sobem com a categoria); o remédio, 6 (rende 1, que vale 8). Comprada na loja e vendida à loja, a leva não paga a matéria (a MG8).

| Poção | Matéria da leva | O que faz (fora da luta) |
| --- | --- | --- |
| cura | 4 de erva | devolve 1d8 × 6 × 3^(categoria da poção − categoria da ferida mais funda) de PV |
| antídoto | 3 de erva, 2 de osso | tira o veneno até a categoria dele (só serve na luta) |
| veneno de lâmina | 4 de peçonha (até o Raro) | passa-se na arma: a primeira ferida que ela abrir envenena (1 dose = 1 golpe); é crime nas vilas |
| Mana | 4 de erva | devolve 4 de Mana por degrau (Comum 4, Incomum 8, Raro 12) |
| guarda | 2 de osso, 3 de erva | até o fim do bloco, conta como amuleto da categoria dela (contra a maldição, o lugar maldito e a magia na luta que abrir nele) |
| fúria | 3 de erva, 2 de osso | +2 no acerto e −2 na Defesa por 5 rodadas (só serve na luta) |
| vigília | 4 de erva | tira 3 de sono e 2 de cansaço (uma por dia) |
| quebra-maldição | 2 de água benta, 3 de erva, 2 de osso | quebra a maldição de categoria menor; recua 2 passos a da mesma; segura 1 dia a maior |
| remédio | 3 de erva Comum (rende 1) | o bem que já existia: é o que gasta quem trata a ferida (capítulo 14) |

A **peçonha** é despojo novo do bicho de veneno (da categoria dele até a Rara); a **água benta**, o clérigo benze (capítulo 14).

12.4 **Beber fora da luta** (`alquimia.py beber cura:0 [alvo=ID]`; na luta é a ordem `beber`). Não gasta bloco. **Vigor ÷ 30 doses por dia, no mínimo 1**; cada uma além disso pede Vigor contra 24 + 4 por dose a mais: falhou, a poção se gasta, não faz nada, e a pessoa enjoa (−2 em todo teste até o fim do bloco, também numa luta que abrir nele). **A cura tem teto:** por pessoa e por dia, feitiço e poção somados nunca devolvem mais que metade do PV máximo. **A ferida mais funda** (`funda`) é a maior categoria que feriu a pessoa desde que ela esteve inteira; apaga quando o PV enche. Por isso a poção barata não serve em luta cara: a da categoria da ferida desfaz cerca de um golpe; uma abaixo, um terço disso. Dá-se de beber a quem está junto. O antídoto e a fúria fora da luta não fazem nada, e a poção de cura em quem está com o PV cheio também não (recusa, antes de gastar, como o comer sem fome).

12.5 **O veneno de lâmina** (`alquimia.py lamina [ARMA]`): uma dose na arma de corte ou de ponta; seca em um dia; numa lâmina de categoria maior que a dose, um terço por degrau. É crime nas vilas: a loja não o compra nem o vende (quem vende é a bruxa, de pessoa a pessoa).

12.6 **O foco e o amuleto** se fazem no encanto, na mesa de runas, como a forja faz a adaga: a varinha (2 de madeira, 1 de osso), o cajado (4 e 1), o símbolo (3 de metal), o talismã (2 de osso, 1 de couro), o amuleto (1 de osso); do Épico para cima, matéria Rara e um núcleo. Blocos, teste e falha da forja. Consertam-se na mesa de runas (a mão de encanto, ou pago). Valem pela matéria que levam: o amuleto Comum, 10 de prata; a varinha, 30; o cajado, 50.

12.7 **Gravar um feitiço numa peça** (`encanto.py gravar ITEM FEITICO [para=DONO] [com=QUEM_SABE]`). A arma, a armadura ou o escudo (o foco e o amuleto já são magia). Quem grava sabe o feitiço, ou tem ao lado quem sabe; o encanto leva o grau de quem sabe (Iniciante 1 a Lendário 4). A **essência** da categoria da peça: até o Raro, 4 de osso e 2 de erva; do Épico para cima, um núcleo. Um terço dos blocos da forja (Comum e Incomum 1, Raro 3, Épico 9, Único 27, Lendário 81). O teste da forja contra 28 + 6 por categoria da peça. Falhou por 1 a 4: grava um grau abaixo. Por 5 ou mais: a essência some e a peça perde 5 de durabilidade. **Por 10 ou mais, a peça sai MALDITA**, e é de onde vêm as peças malditas do mundo: quem a puser em uso pega a maldição, que só quebra devolvendo a peça à mesa de runas onde se gravou. Um encanto por peça; dois do Único para cima. Na luta (capítulo 11): o dono solta o feitiço uma vez, a peça vale foco um degrau abaixo, e volta a carregar 1 bloco depois.

12.8 **O jornal** da botica, da mesa de runas e do santuário paga o salário da mão (Iniciante: aprendiz; Treinado: oficial; Mestre: mestre), **dentro da mesma jornada de 2 blocos pagos por dia** que vale para o trabalhar e para o jornal da forja. Serviço de magia rende o que rende a forja: nenhuma renda nova.

## 13. As maldições (etapa da magia)

13.1 **O que é.** Um registro na pessoa: nome, categoria, **tipo** (míngua, chaga, azar, insônia, marca: o sinal que ela sente), **um relógio de 6 passos**, a **origem** (feitiço, bicho, lugar, peça, juramento), quem a rogou e a **condição** que a quebra. Não é estado de luta: é coisa de dias. É a única coisa desta etapa que mata fora da luta sem ser fome.

13.2 **O relógio.** Na virada de cada dia o mundo rola (o dado do mundo, oculto): **2d20 + a força da maldição contra a Firmeza do amaldiçoado.** A força é 2 + 4 por categoria (Comum 2, Incomum 6, Rara 10, Épica 14). A Firmeza é a da base comum (22, metade do bônus de Vontade, metade da maior maestria, metade do dom de tradição, e o melhor entre o bônus do amuleto e metade do da armadura do tronco: o amuleto fraco não tira o que a armadura boa dá). Venceu, anda um passo.

| Passo | Nome | O que faz |
| --- | --- | --- |
| 1 | a marca | nada em número |
| 2 | o peso | −1 em todo teste |
| 3 | a míngua | −2; a noite dormida não devolve PV |
| 4 | a chaga | −2; as feridas não saram; a Mana não volta fora da luta |
| 5 | o fim à vista | −4; cada virada tira 10% do PV máximo |
| 6 | a morte | morre na virada, com a causa escrita |

Das penas de maldição vale a pior; ela soma com a pena do corpo, em todo teste e na luta. **Quanto tempo dá** (medido, metade das vidas, ninguém fazendo nada): o guerreiro de amuleto Raro, maldição Rara (a categoria da guarda), 15 dias; o mesmo sem amuleto, 9; o aldeão sem amuleto, maldição Comum, 10. Nenhuma mata antes de 5 dias. O amuleto compra tempo; não cura. **O relógio anda para toda gente amaldiçoada**, o personagem ou não: o mundo não gira em torno dele.

13.3 **De onde vem.**
- **A peça maldita**, ao ser posta em uso: a maldição pega no passo 1 (a pessoa só sente um frio no braço), e **a mão não larga a peça** (não sai de uso, não se vende, não muda de mão) enquanto ela durar. Ela parece uma peça comum: só quem a lê sabe. **A loja não compra peça maldita**, nem a que ninguém pôs em uso: o mercador pega para avaliar e larga depressa, sem saber dizer por quê (é a única pista de graça; e assim a armadilha não vira prata).
- **O lugar maldito**: a cada bloco passado nele, o mundo rola a força dele contra a Firmeza de quem está; pegou, quebra quando a pessoa passa 7 dias sem pôr o pé lá.
- **O feitiço**: a praga da bruxa (capítulo 14).
- **O bicho que amaldiçoa**: a ferida que ele abre (a luta e as criaturas).
- **O juramento quebrado**: o voto do clérigo, a dívida da bruxa (capítulo 14).

13.4 **Como se quebra.**
1. **Cumprir a condição:** devolver a peça ao lugar dela (`maldicao.py devolver ITEM`, estando lá: a peça fica no chão, ainda maldita; quem sabe de onde ela é, porque alguém leu, e sai ao ermo dela levando-a, para na chegada, antes da procura: dá tempo de devolver); matar o bicho naquele ermo (quebra na hora, no acerto da caça); o perdão de quem rogou (`maldicao.py perdoa`), ou a morte dela; os 7 dias longe do lugar; a dívida zerada. O estado confere sozinho na virada (e o Mestre atesta o que ele não sabe conferir: cumprir o jurado, queimar o laço: `maldicao.py cumpre`).
2. **O rito do clérigo** (`maldicao.py rito ALVO quem=CLERIGO`): quem sabe quebrar-maldição (e não quebrou o voto), 1 bloco, 6 de Mana, uma tentativa por dia. **2d20 + Conjuração da fé contra 28 + a força + 2 por passo além do primeiro:** quem chega cedo se salva. Falhou por 5 ou mais: o clérigo leva a marca (a mesma maldição, no passo 1). O personagem ajudado paga, de pessoa a pessoa, um terço do preço de tabela da categoria (10, 60, 360, 2.160 de prata); o rito pela gente do mundo sai sem cobrança (14.7). O clérigo Mestre de símbolo Raro, na maldição Rara: 57% no passo 1, 48% no passo 2, 40% no 3.
3. **A poção quebra-maldição** só ganha tempo: a de categoria maior quebra; a da mesma faz recuar 2 passos; a menor segura 1 dia.
4. **O que não quebra:** dormir, comer, curar o PV, mudar de lugar (salvo a do lugar).

13.5 **O que a mesa mostra**, em três degraus de saber:
- **não sabe** (passo 1): nada;
- **desconfia** (do passo 2): "ALGO ESTÁ ERRADO: Maro acorda mais fraco do que deitou, e isto não é doença. Pesa: −2 em todo teste; a noite não devolve PV." Sem nome, sem categoria, sem prazo;
- **sabe** (alguém leu: capítulo 14): "MALDIÇÃO: a Mão Fria (Incomum, míngua), passo 3 de 6 (a míngua): −2 em todo teste; a noite não devolve PV. Desde o Dia 12. Veio da peça Adaga do Túmulo. Quebra: devolver Adaga do Túmulo ao lugar dela, na Capela Caída; ou o rito de um clérigo (60 de prata)."

O SÓ O MESTRE vê tudo de todos (a força, a Firmeza, a chance de andar amanhã, a condição) e a rolagem oculta de cada virada do personagem. **O que só o Mestre sabe não vai aos fatos do RETOMAR:** o evento do Mestre ou do gerador que põe o talento ou o dom de alguém, a peça ou o lugar maldito, o covil, ou a maldição que a pessoa ainda não sente vai ao SÓ O MESTRE do RETOMAR, com o texto dele. O RETOMAR leva as maldições que o personagem sente. **O `turno.py fecha` recusa** o turno com maldição do personagem no passo 4 ou mais sem uma pergunta aberta sobre ela.

## 14. A magia no mundo: estudar, as tradições, a Mana, os ritos e os serviços (etapa da magia)

14.1 **Qualquer um aprende magia**, como se aprende uma arma (`magia_mundo.py estudar FEITICO com=PESSOA|escrito=ITEM|santuario|ermo`). Um feitiço se estuda em blocos leves, vezes o talento na tradição dele: o truque 3, o grau 1 6, o grau 2 18, o grau 3 54, o grau 4 162. Os blocos de estudo são treino da tradição: a maestria sobe pela tabela das armas (40, 160, 500, 1.500; de Mestre para cima, com um feito). **A fonte:** quem saiba o feitiço e queira ensinar (cobra o salário do grau de ofício dele por bloco, e só ensina dentro da jornada dele: 2 blocos por dia); um escrito que o ensine (de graça); um santuário (os feitiços da fé, a quem tem voto); o ermo do laço (os do verde, a quem tem laço). Os seis de grau 1 de uma tradição somam 36 blocos: é quase o Iniciante.

14.2 **Uma tradição por pessoa.**

| Tradição | Como se entra | De onde vem a Mana fora da luta | O que custa |
| --- | --- | --- | --- |
| o mago (`arcano`) | estudando o primeiro feitiço | a regra geral (14.3) | o livro e as lições |
| o clérigo (`fé`) | o VOTO, num santuário (`magia_mundo.py voto lâmina\|pobreza\|socorro`) | só a PRECE: 1 bloco por dia; no santuário enche, fora dele volta a metade | quebrar o voto apaga a Mana e deixa uma marca (maldição de juramento, da categoria do santuário) |
| o druida (`verde`) | o LAÇO com um ermo vizinho (`magia_mundo.py laco ERMO`) | em dobro no ermo; a metade entre muros (cidade, masmorra) | a fartura do ermo do laço abaixo de 40% tira 2 da Conjuração; abaixo de 10%, 4 |
| a bruxa (`pacto`) | o PACTO, no escuro (madrugada ou noite): nasce devendo 1 | sozinha, só até a metade; o resto paga-se (`magia_mundo.py paga N pv\|divida`): 2% do PV máximo por ponto, ou 1 de dívida por 4 | a dívida sobe com o feitiço de grau 2 (+1), 3 (+2), 4 (+3) e a praga (a categoria mais 1); acima de Vontade ÷ 10, vira maldição nela (a Conta, que quebra quando a dívida zera) |

**Os votos:** da lâmina (não pôr em uso arma de corte nem de ponta: pôr é quebrar), da pobreza (na virada, a prata acima de 50 vai para o caixa do santuário), do socorro (não recusar cura pedida: a etapa 3). **A dívida** paga-se num rito de 1 bloco (`magia_mundo.py divida N pv|osso|erva`): 1 ponto a cada 5% do PV máximo, ou queimando 4 de osso ou de erva da categoria do foco.

14.3 **A Mana fora da luta**, por bloco: dormindo, um quarto da máxima; descansando, um oitavo; acordado e leve (ou parado), 1; no bloco pesado, nada. A tradição muda isto (14.2). A maldição do passo 4 não deixa a Mana voltar. **Quem não é o personagem recobra a Mana no descanso em casa** (5.14): quando volta à cena, cada dia inteiro que passou em casa vale 2 blocos dormidos e 4 parados (Anselmo, de Mana 0, volta com 14 dos 19 depois de um dia); o druida segue o lugar onde mora; a bruxa, sozinha, só até a metade; o clérigo de voto inteiro reza a prece do dia em casa (onde há santuário, enche; longe, volta a metade), e essa é a prece do dia. Gastar a Mana também é estar em cena: o dia já contado não enche de novo. A Mana máxima é (Afinidade + Vontade) ÷ 10 + a maestria da melhor tradição + o dom nela (a mesa mostra a que a pessoa conhece: sem o dom que ela ainda não viu).

14.4 **Lançar fora da luta** (`magia_mundo.py lancar FEITICO [alvo=ID]`; não gasta bloco): a **cura** (1d8 × 6 × 3^(a categoria do foco − a ferida mais funda), dentro do teto do dia; o foco de outra tradição rende uma categoria abaixo, e sem foco, Comum), a **bênção** antes da luta (a luta que abrir até o fim do bloco seguinte leva o benzido), a **seiva** (a cura dos blocos dormidos do dia seguinte vale em dobro). A cura em quem está com o PV cheio é recusada antes de gastar a Mana. O resto só muda número na luta. O feitiço custa a Mana da tabela; o de pacto de grau 2 para cima soma dívida, fora ou dentro da luta (a luta a devolve ao estado).

14.5 **Os ritos** (1 bloco leve cada):
- **a prece** do clérigo (uma por dia);
- **ler** (`magia_mundo.py ler maldicao|dom|peca`): quem sabe o feitiço ler, ou a fé de Treinado para cima; 2 de Mana. Lê toda maldição de alguém (passa a saber tudo), o dom de alguém (ele se mostra), ou uma peça (se é maldita, que maldição e o que a quebra; e os encantos);
- **quebrar a maldição** (capítulo 13);
- **a praga** da bruxa, pelo toque (`magia_mundo.py praga ALVO [tipo=]`): 6 de Mana; 2d20 + Conjuração do pacto contra a Firmeza do alvo; pegou, uma maldição da categoria do foco dela, que quebra com o perdão ou a morte dela; a dívida sobe pegue ou não;
- **a água benta** (`magia_mundo.py agua N`, num santuário): cada uma, 1 de erva Comum e 2 de Mana; até 3 por rito;
- **benzer a arma** (`magia_mundo.py benzer ARMA`, num santuário): 2 de Mana; por 7 dias ela conta inteira contra o que não tem corpo.

14.6 **Tratar a ferida** (`magia_mundo.py tratar PACIENTE`): o ofício `cura`. 1 bloco leve e 1 remédio (da carga do paciente, ou da de quem trata, que cobra o preço de base dele); um tratamento por paciente por dia; pede mão de cura de Iniciante (de Treinado, se há ferida grave). Soma 1 dia de repouso a todas as feridas do paciente: tratado todo dia, a ferida sara na metade do tempo. O dom da cura soma meio dia por grau, e se mostra no primeiro tratamento.

14.7 **Os serviços, de pessoa a pessoa.** **Só o personagem paga serviço:** quem o ajuda cobra o preço da tabela (evento `servico`: a prata só muda de mão): ler 10 · a cura 3 por lance · a bênção 5 por pessoa · tratar 2 e o remédio · benzer a arma 5 · o rito de quebrar, um terço do preço de tabela da categoria · a lição, o salário de quem ensina. Outro preço combina-se com `paga=N` (um número inteiro, de 0 para cima: o negativo e o que não é número são recusados antes de tudo; a `compra` de pessoa a pessoa, com `preco=`, também). **A gente do mundo não procura serviço sozinha nesta etapa** (é da etapa 3): o que se faz por ela, inclusive o que o personagem faz (benzer, curar, ler, tratar, quebrar a maldição de alguém da vila), sai sem cobrança, e o `paga=` de quem não é o personagem é recusado. A única renda que a magia dá a quem presta, fora o que o personagem pagar, é o jornal (12.8): o personagem clérigo que benze a vila inteira cinco dias seguidos não ganha nada com isso (a MG11).

14.8 **A magia no mercado.** As poções do Comum ao Raro são bens como os outros, com preço pelo estoque: a Comum vale 6 de prata, vezes 6 por categoria. A peçonha (2 de base, Comum) e a água benta (3) também. O povo gasta pouco: a vila de 400 quer 6 poções de cura, 2 antídotos, 1 vigília e 1 quebra-maldição Comuns, e 1 cura Incomum. **A loja não negocia o veneno de lâmina** (crime). O "vender tudo" não leva as poções nem a água benta (são de usar: vendem-se pelo nome). **O foco, o amuleto e o escrito** a loja negocia como peça (paga 40% do valor, mais a mão de comércio; a loja farta conta junto com as armas da mesma categoria); o elixir não tem loja. **A parte da magia de um mercado abre-se à parte** (`mercado.py magia`, pelo Mestre ou pelo gerador): a botica do lugar faz para o povo as poções até a categoria dela (a de vila, só as Comuns: produção no consumo, prateleira no alvo); a prateleira tem cada poção que a loja negocia até uma categoria acima disso; a água benta e o quebra-maldição, onde há santuário; e amuletos, focos e um escrito na prateleira (a vila: 2 amuletos, 1 varinha, 1 símbolo e a Cartilha do arcano, que ensina seta e luz).

14.9 **Quem registra o quê** (o Mestre, ou o gerador da vila): `alquimia.py botica N`, `encanto.py runas N`, `magia_mundo.py santuario N`, `mercado.py magia`, `maldicao.py peca ITEM "Nome" CATEGORIA TIPO onde=LUGAR`, `maldicao.py lugar "Nome" CATEGORIA TIPO`, `maldicao.py poe ALVO "Nome" CATEGORIA TIPO CONDICAO`, e os preparos (`oficio.py preparo vidraria Comum "como" oficio=alquimia`).

### O banco de provas do mundo da magia (`provas_magia.py`; os números da rodada final da integração)

| Meta | O que se mede | Faixa | Medido |
| --- | --- | --- | --- |
| MG1 | a pessoa comum: dez dias de rotina com os módulos da magia ligados e desligados | o mesmo mundo | igual (estado e eventos) |
| MG2 | estudar: grau 1 em 6 blocos (Prodígio 3); o mestre só na jornada dele; o escrito de graça; as recusas | sempre | sim |
| MG3 | a Mana fora da luta, por tradição; a prece; a maldição do passo 4; quem volta à cena depois de um dia em casa (uma vez só) | a conta exata | sim (o mago de 16: 12 em casa) |
| MG4 | a maldição da categoria da guarda · a Comum num aldeão · a mais curta · o que o amuleto compra (com ele contra só a malha) | 10 a 25 · 7 a 14 · nunca antes de 5 dias · 3 dias ou mais | 15 · 10 · 5 · 6 |
| MG5 | o clérigo Mestre de símbolo Raro, na maldição Rara, passos 1 e 2 | 45 a 70% | 57% e 48% |
| MG6 | a poção da categoria · uma abaixo, em golpes médios entre iguais | 0,7 a 1,5 · até 0,5 | 1,05 · 0,36 |
| MG7 | o limite do corpo e o teto da cura do dia | sempre | sim |
| MG8 | quem compra a matéria e vende a leva, com a prateleira no alvo | o Leigo nunca ganha; a melhor mão, no máximo 6 | −3 · −1 |
| MG9 | o alquimista de loja (com botica; sem botica que produza; a teimosa, que faz a leva todo dia), 30 vilas; o guloso olha todo dia e faz quando paga (a conta da MG8) | 6 por dia (pior 12) nos 5 primeiros dias; 4 depois | 0 · 0 · −5,1 (a teimosa faz 25 levas por vida e perde) |
| MG10 | fazer foco e amuleto para a loja, 30 vilas | a mesma | 1,95 a 2,97 (pior 5,8) · 0 |
| MG11 | o serviço de magia: a jornada; a prata que só muda de mão; o preço torto; o personagem clérigo servindo a vila 5 dias | sempre; nunca mais de 12 por dia | sim; 0 por dia |
| MG12 | a peça maldita e o lugar maldito | sempre | sim |
| MG13 | gravar custa o que diz; a falha por 10 amaldiçoa a peça | sempre | sim |
| MG14 | a MESA pelos três degraus; o RETOMAR; o fecha que recusa no passo 4 | sempre | sim |
| MG15 | a prata e a matéria fecham; o núcleo perdido sai do Livro | sempre | sim |
| MG16 | o voto, o laço e a dívida | sempre | sim |
| MG17 | as recusas (com a poção e o feitiço de cura no PV cheio, a paga de quem não é o personagem, a paga negativa) | todas | sim (22) |

---

## 15. As criaturas (etapa da magia)

### 15.1 Dois jeitos de ser criatura

**O povo** (o goblin, o orc, o ogro, o homem-lagarto, o gigante; e os mortos que empunham: o esqueleto e o cavaleiro da cova) é **gente**. Tem a ficha de gente, com arma,
armadura e escudo de verdade, e por cima o corpo do povo: o tamanho (mexe no PV, na Defesa, no alcance da mão e em quantos batem nele de perto), os traços, a coragem e a pele
(o couro grosso do ogro e a escama do homem-lagarto valem como armadura onde a peça não cobre). Cada um tem um **posto**: o goblin de faca, o de lança e escudo, o de arco, o capataz;
o orc, o orc bruto (malho de duas mãos), o capitão. Vale a regra de ouro de sempre: conta a peça de quem bate contra a peça de quem apanha.

A peça do povo é **gasta e malfeita**. Na luta vale a categoria dela; morto o dono, não presta para vender como peça: é **sucata** (o despojo da espécie: o ferro da lâmina e o
couro da armadura, em matéria).

**A criatura de corpo** (o corpo-seco, o carniçal, a múmia, o fogo-fátuo, a alma penada, o espectro, o golem de barro, a gárgula, o elemental do fogo, a harpia, o lobisomem,
o senhor vampiro) é um **bicho**: o corpo é a arma e a armadura, com categoria (capítulo 6). Quem tem o traço **lança** sabe feitiços; o corpo é o foco, e o instinto é a mão.
O bicho que lança, lança enquanto não alcança o inimigo; ao alcance, usa o corpo.

As criaturas **não entram** na lista dos bichos do capítulo 6, e os traços novos **não entram** na lista fechada dos traços dos bichos: moram na página das criaturas. Assim as
provas da etapa 2 seguem iguais.

### 15.2 O bestiário (19 criaturas)

| Criatura | Grau | Categoria | É | Bando | Traços | O que se sabe |
| --- | --- | --- | --- | --- | --- | --- |
| goblin | F | Comum | povo, pequeno | 2 a 4 | noturno | miúdo, frágil e covarde; nunca anda sozinho; mora em toca e rouba de noite |
| corpo-seco | E | Comum | corpo | 1 a 3 | sem vida, agarra, noturno | lento e sem dor; quem ele agarra não recua |
| esqueleto | E | Comum | povo (espada e escudo) | 2 a 4 | sem vida, ossos, noturno | a ponta e o fio passam entre os ossos: pede maça |
| orc | D | Incomum | povo | 2 a 4 | noturno | forte e mal treinado: vale pelo que veste e pelo número |
| fogo-fátuo | D | Incomum | corpo, pequeno | 1 a 3 | voa, imaterial, lança (a seta) | a luz que chama para o fundo do brejo |
| alma penada | D | Incomum | corpo | 1 a 2 | sem vida, imaterial, apavora | o aço comum passa por ela quase sem ferir |
| homem-lagarto | D | Incomum | povo (escama) | 2 a 3 | | de lança e escudo, segura um vau |
| carniçal | D | Incomum | corpo | 2 a 4 | sem vida, veneno, matilha, noturno | come os mortos e caça em roda |
| harpia | D | Incomum | corpo (fera) | 2 a 4 | voa | vem de cima, em bando |
| golem de barro | D | Incomum | corpo | 1 a 2 | sem vida, resiste | guarda o posto e a magia escorre nele |
| gárgula | C | Rara | corpo | 1 a 2 | voa, bote | parece pedra até cair em cima de quem passa |
| ogro | C | Raro | povo, grande (couro grosso) | 1 a 2 | | o tronco alcança antes da espada |
| múmia | C | Rara | corpo | 1 | sem vida, agarra, apavora, amaldiçoa | a maldição da cova |
| espectro | C | Raro | corpo | 1 | sem vida, imaterial, dreno, amaldiçoa | bebe a vida de quem toca |
| lobisomem | C | Raro | corpo (fera) | 1 | regenera, amaldiçoa, noturno | a mordida deixa a maldição da lua |
| elemental do fogo | C | Raro | corpo | 1 | sem vida, ardente, resiste | quem bate de perto se queima |
| cavaleiro da cova | B | Épico | povo (montante, placa) | 1 | sem vida, noturno | um mestre de armas que não cansa |
| gigante | B | Épico | povo, enorme | 1 | | oito batem nele, mas o tronco pega a três casas |
| senhor vampiro | B | Épico | corpo, CHEFE | 1 | dreno, regenera, apavora, noturno, lança (medo, sangria) | de dia é menos |

Só criatura do folclore e da fantasia comum; nada que seja criação de um jogo ou livro.
`criaturas.py lista` mostra a tabela; `criaturas.py ver NOME` dá a ficha; `bichos.py ameaca NOME` (ou `criaturas.py ameaca NOME`) dá a frase.

### 15.3 Os traços novos (a frase de cada um)

A luta roda os nove (capítulo 11; os números no `tabelas_magia.py`). A frase que a mesa lê:
- **resiste**: o corpo guarda contra a magia inteiro (não só 60%), e a Firmeza leva o bônus inteiro do corpo.
- **imaterial**: não tem carne; arma sem encanto e sem bênção conta uma categoria abaixo (o golpe vale um terço); o feitiço e a peça encantada contam inteiros; não vai ao chão nem é agarrado.
- **amaldiçoa**: a ferida que abre põe uma maldição da categoria do corpo, no passo 1 (ela anda dia a dia até alguém a quebrar: capítulo 13). Cada criatura que amaldiçoa tem o seu molde
  (a múmia: a maldição da cova; o espectro: o frio; o lobisomem: a maldição da lua; o vampiro: a sede).
- **lança**: sabe feitiços (a lista vem na ameaça), com a Mana e a Conjuração do instinto e da categoria do corpo.
- **sem vida**: não sangra, o veneno não pega e não foge; não cansa, mas não faz a ação a mais; a zero de PV se desfaz.
- **ossos**: o corte e a ponta valem metade; o impacto, inteiro.
- **dreno**: recupera em PV metade do que o golpe do corpo tira.
- **ardente**: quem golpeia de perto leva o fogo de volta (4 por categoria do corpo, a contar do Comum); a ferida que o corpo abre queima 5 rodadas.
- **noturno**: o escuro não tira nada do golpe nem do tiro.

### 15.4 A ameaça lida antes

Antes da luta lê-se a ameaça, como a do bicho: o grau, a categoria, o tamanho, quantos são (e quanto o bando pesa para quem está sozinho), os traços com a frase de cada um, o que
se sabe, e se foge. O povo diz o que veste, posto por posto ("veste peças Comuns gastas e malfeitas: goblin: adaga, couro; goblin lanceiro: lança, couro, escudo..."), e a conta da regra
de ouro contra o que você veste. O morto que anda diz que não foge. Quem lança diz o que lança. Do **chefe** ninguém sabe de graça: o Mestre lê a frase dele (`criaturas.py ameaca CHEFE`)
quando a cena o põe à frente (o que lança, com quem vem, e como muda ferido).

### 15.5 O povo foge, se rende e não fica

O povo testa a coragem como gente (com a coragem do povo: o goblin −4, o orc +2). Abalado, foge ou se rende. **Quem se rende a quem fica com o campo sai da contagem do ermo** (vai preso,
ou é rematado: a cena decide), e o despojo dele é o de um morto. Caído o líder do bando (o capataz goblin, o capitão orc), o bando testa a coragem. O morto que anda não testa nada.

### 15.6 O despojo

- **O povo:** a sucata das peças, da categoria do bando (o goblin: 1 de metal e 1 de couro Comuns; o orc: 1 de metal e 1 de couro Incomuns), de metade ao inteiro, como o bicho.
  A peça do povo nunca vira peça de vender: assim um bando morto não enche a loja de espadas.
- **O corpo:** a tabela da espécie, como o bicho (osso, couro, carvão do elemental, pano da múmia; o ser de magia não deixa nada).
- **A peçonha:** todo bicho e toda criatura de veneno dá peçonha da categoria dele, até a Rara (a surucucu, a aranha-de-toca, o basilisco, a serpe, a hidra, o carniçal).
- **O chefe de corpo** (o senhor vampiro) dá núcleo, como todo chefe.
- **A prata** não sai do corpo de ninguém: é a que o bando juntou, e mora no tesouro da toca (16.2).

### 15.7 Os chefes mágicos

Cada um vem com os lacaios, lança (ou solta o encanto da peça), e muda de **fase** abaixo de uma fração do PV: a luta para e pergunta. As fases só usam o que a luta roda: ganhar e
perder traços, aprender feitiço, recobrar Mana, o **brado** (os do lado dele ficam benzidos por 3 rodadas: +2 no acerto e +2 na coragem) e **erguer** os mortos.

| Chefe | Grau | O que é | Lança | Fases | Lacaios |
| --- | --- | --- | --- | --- | --- |
| o xamã goblin | D | goblin do pacto, talismã e amuleto Incomuns, atrás da linha | mau-olhado, medo, sangria | abaixo de 50%: uiva (brado), recobra 3 de Mana | 2 goblins da guarda (põem o corpo na frente dele), o capataz, 4 de faca, 2 de lança, 2 de arco |
| o senhor da guerra orc | C | orc mestre de armas, machado Raro com o encanto do medo (uma vez por luta) | (o encanto) | abaixo de 50%: entra em fúria e urra (brado) | 2 orcs da guarda (Raros), 4 orcs, 2 orcs brutos |
| a bruxa do brejo | C | bruxa do pacto, talismã Raro | mau-olhado, medo, sangria, nó | abaixo de 40%: larga a pele de velha (a faca dela passa a amaldiçoar), recobra 6 de Mana | o trasgo, 3 fogos-fátuos Raros, 2 afogados (corpos-secos Raros) |
| o necromante | B | do pacto, talismã Épico, frágil, atrás dos mortos | sangria, nó, medo | abaixo de 70% e de 35%: ergue 3 mortos (dos dois lados) | o cavaleiro da cova (guarda), 6 esqueletos Raros |
| o senhor vampiro | B | criatura de corpo, CHEFE, atrás dos lacaios (lança de longe; ao alcance, usa o corpo) | medo, sangria | abaixo de 30%: a sede (cada ferida que abre amaldiçoa) | 3 carniçais, 3 lobos |

### 15.8 As medidas (o banco: `provas_criaturas.py`)

- **O bando contra o homem do degrau** (espada, malha, elmo e escudo da categoria, no nível de referência: o Comum 10, o Incomum 30): o bando que um homem do degrau enfrenta de igual
  para igual é de **quatro goblins** (o homem vence cerca de 54%) e de **dois orcs** (cerca de 44%). Contra três goblins ele vence 78%; contra três orcs, 10%. A faixa: de 35 a 65%.
- **O chefe com os lacaios contra quatro homens** do degrau em que vive (300 lutas cada, a rodada final): o xamã contra quatro Comuns, cerca de 53%; o senhor da guerra contra quatro Raros, 41%; a bruxa do brejo, 54%;
  o necromante contra quatro Épicos, 56%; o senhor vampiro, 45%. A faixa: de 30 a 70%. Com o mau-olhado de −4 (capítulo 11), a bruxa do brejo passava a 71% e o necromante a 76%: a bruxa
  ficou com dois afogados (eram três) e o necromante largou o mau-olhado (ergue, bebe a vida, ata a magia e gela a coragem). Menos cabeças não bastavam (o necromante com quatro esqueletos: 68%).
- **A patrulha goblin contra o guerreiro de nível 5 de peças Comuns** (o começo "guerreiro" da vila de teste: espada, escudo e malha, sem elmo), como a caça a dá (de dois a quatro, de
  faca; metade das vezes ele a vê primeiro): ele vence cerca de 73% e morre em cerca de 12%. A faixa: de 40 a 75%, e morre em 15% ou menos. Contra dois: 91% e 5%; contra quatro: 51% e 27%.
  **Uma observação para o jogador:** nesta luta, quem cai do lado que perde morre na metade das vezes (o teste de morte); por isso, para morrer em 15% ou menos, ele tem de vencer
  70% ou mais. A janela da meta é estreita (de 70 a 75%), e o goblin ficou miúdo e frágil para caber nela.


## 16. O covil e a vila de teste com a magia (etapa da magia)

### 16.1 O covil é contado ao lado da fauna

O covil é a toca de um povo num ermo (`lugar.covil`). **As cabeças dele SÃO a contagem da espécie no ermo** (`lugar.bichos.goblin`), ao lado da corça e do lobo: a patrulha que o
caçador encontra sai dela, e quem morre sai dela. O registro do covil guarda o resto: o nome, o teto, se o líder está de pé, o chefe que mora ali (ou nenhum), a fome, o último roubo,
os dias sem líder, os dias de toca cheia, e os dias até chegar um bando de fora quando ela se esvazia. **O covil não guarda prata:** o tesouro da toca é o estoque do ermo, contado como toda prata.

As criaturas que não são fera (o povo, o morto, o ser de magia) **não criam na virada da caça**: o bando de um covil cria pela vida do covil; os mortos de uma cova ficam os que são.

### 16.2 A vida da toca (todo dia, evento "covil", o mundo sozinho)

Os números são os do `tabelas_criaturas.COVIS`, um para cada povo:

| | a toca dos goblins | o acampamento orc |
| --- | --- | --- |
| come, por cabeça e por dia | 0,3 de comida | 0,6 de comida |
| rouba da vila vizinha | a cada 7 dias, com a chance de cabeças ÷ 20 | a cada 10 dias, com a chance de cabeças ÷ 12 |
| o que leva | 2 de comida por cabeça; a prata, uma vez em quatro (de 1 a 6, mais uma por quatro cabeças) | 3 de comida por cabeça; a prata, duas vezes em cinco (de 1 a 12, mais uma por quatro cabeças) |
| cria, bem comido | cabeças × 2,5% × o que falta para o teto, por dia; o teto, 16 | cabeças × 1,5% × o que falta para o teto; o teto, 12 |
| o líder caído | outro sobe em 7 dias | em 10 dias |
| o chefe | a toca com 12 ou mais por 30 dias seguidos ganha o xamã goblin | com 10 ou mais por 60 dias, o senhor da guerra |
| a toca vazia | espera 120 dias por um bando de fora, de 6 | 240 dias, por 4 orcs |
| o covil que o Mestre funda sem dizer quanto | 9 cabeças, 20 de prata no tesouro | 6 cabeças, 60 de prata |

1. **Come** primeiro do que juntou (a comida do estoque do ermo), depois da caça contada do ermo (a corça e o javali, pela fartura; o goblin também come ratazana). A fome sobe 1 no dia em que falta comida e desce 1 no dia farto.
2. **Rouba** com a chance da tabela, mais 10% por ponto de fome. O que rouba vai para o estoque do ermo: **o tesouro da toca.** A prata só muda de mão.
3. **Cria** devagar, bem comido (fome abaixo de 4), até o teto. **Definha** com fome (um a menos por dia, com a fome em 9).
4. **O líder e o chefe** como na tabela: caído o capataz, outro sobe; a toca cheia por muito tempo ganha o chefe; a toca vazia espera o bando de fora.

Medido (um ano sozinho, a toca da vila de teste): o bando chega ao teto (16) e não passa dele; a corça fica em 75 a 78 de 80, o javali em 38 a 39 de 40; rouba de 1.000 a 1.400 de
comida no ano (a vila produz 146.000) e de 40 a 110 de prata; o xamã sobe perto do Dia 62; a prata do mundo fecha.

### 16.3 A toca na caça

- `caca.py sair ERMO alvo=toca` procura a toca do bando: o rastro é 2 mais difícil que o da espécie, e a rolagem é **oculta** (ninguém sabe de graça se há toca, como no chefe).
- Achada, lê-se a frase da toca: de fora se contam poucos, um bando, muitos ou uma toca cheia; se há chefe, só se vê o sinal (os ossos pintados, o fumo doce). Depois, a ameaça do povo.
- A luta é com **todos os que estão lá**: o chefe e a guarda dele (se a toca tem chefe), o líder (atrás da linha) e o resto pelos postos (metade de faca, um quarto de lança, um quarto de arco).
  O chefe não é da contagem: mora no registro do covil.
- **Quem fica com o campo na toca leva o tesouro inteiro** (a prata e a comida do estoque do ermo), repartido entre quem lutou até o fim. Caído o líder ou o chefe, o covil fica sem ele.
- **O que cai no chão de um ermo com toca, o bando junta:** a carga e a prata de quem morre ali entram no tesouro da toca, e a mesa diz assim.

**Limpar um covil não é mina** (medido): a casa de três (o guerreiro de nível 5, Tomé e Rute), 60 dias ao lado da toca da vila de teste, saindo quando os três estão inteiros e
esperando quando alguém está ferido, tira cerca de **0,5 diária por dia de trabalho de cada um** (a melhor vida, cerca de 1,6), e morre alguém da casa em 1 ou 2 vidas de cada 12.
O primeiro assalto rende o tesouro (20 de prata, na vila de teste) e a sucata; os seguintes, quase só sucata, e o bando que fugiu volta devagar.

### 16.4 O Mestre funda um covil

`criaturas.py covil poe ERMO goblin [cabecas=N] [tesouro=N] [chefe=sim]` (ou `orc`): num ermo que já existe, por um evento "mestre" (o tesouro é prata que nasce, como tudo o que o
Mestre põe). `criaturas.py covil [ERMO]` mostra o covil (SÓ O MESTRE; a mesa traz a linha dele no SÓ O MESTRE).

### 16.5 A vila de teste com a etapa inteira

A vila nova (`vila_teste.py PASTA ... [inclinacao=CAMINHO]`) nasce com os talentos e os dons. Para **a vila que já existe** (o save de quem já joga):

```
python3 vila_teste.py magia PASTA [inclinacao=CAMINHO]
```

Acrescenta, **só por eventos, sem recriar nada** (e recusa rodar duas vezes):
1. **Os talentos e os dons** de quem ainda não foi rolado; o personagem com a inclinação, se o jogador escolher uma (só vale enquanto o talento dele não foi rolado). Tudo num evento só, do gerador: é segredo, e vai ao SÓ O MESTRE do RETOMAR, não aos fatos do turno.
2. **Anselmo, o mago velho** (nível 40, arcano Treinado: a luz, a seta, o escudo, prender, a lança de fogo; cajado Incomum, amuleto Comum).
3. **A botica da curandeira:** Pedra Rasa ganha a botica (1), e Nara a mão de Iniciante na alquimia. **A loja ganha a parte da magia** (`mercado.funda_magia`): as poções Comuns que a botica faz para o povo (cura, antídoto, vigília), as outras até a Incomum na prateleira, a água benta e o quebra-maldição (há santuário), e, na prateleira de peças, dois amuletos Comuns, uma varinha, um símbolo e a Cartilha do arcano.
4. **O santuário** (1) e **Lúcia, a clériga** (nível 35, fé de Mestre, voto do socorro: a cura, a bênção, o amparo, o castigo, quebrar maldição; símbolo Comum).
5. **Joana, a bruxa** da choupana na borda da Mata do Corvo (nível 30, pacto Treinado: o mau-olhado, o medo, a sangria, ler, o nó; deve 2; leva 3 doses de veneno de lâmina e erva).
6. **O Grande Dom de forja do Zeca**, o aprendiz, que ninguém leu (aparece quando decidir um teste na bancada, ou quando alguém o ler).
7. **A Cova Velha**, um ermo novo vizinho da vila (ruína, borda): 3 esqueletos e 2 corpos-secos, e **a Espada do Guardião** largada no chão (Incomum, maldita: a Mão Fria, míngua;
   quem a puser em uso pega a maldição, e a mão não a larga enquanto ela dura: tirar, trocar de arma e passar a outro são recusados com uma frase simples; quebra devolvendo-a à cova;
   a loja não a compra).
8. **A toca dos goblins** na Mata do Corvo: 8 goblins (teto 16), o capataz, 20 de prata no tesouro.

A prata que nasce: a das três pessoas novas (145) e o tesouro da toca (20). Nada mais muda: a gente, os itens e o tempo de antes seguem como estavam.

### 16.6 O que fica para depois

O covil não ataca a vila nem gente na rua (o roubo é contado, não jogado); o bando que fugiu não se junta a outro covil; os povos não comerciam; o necromante e a bruxa do brejo não
têm covil próprio na vila de teste (o Mestre põe quando quiser); masmorras, frentes e rivais são das etapas 5 e 6.

### 16.7 O que a etapa da magia não resolve (fica dito)

- **A gente do mundo não procura serviço sozinha.** Ninguém pede cura, leitura ou bênção ao personagem, e o voto do socorro não tem quem peça (etapa 3). Os serviços de magia rendem a quem presta só o que o personagem pagar, e o jornal.
- **Quem vai junto não pede paga,** nem o mago velho: Anselmo (nível 40, arcano Treinado) vai à caça quando chamado e leva a parte dele, como Tomé e Rute (decisão da etapa 2). Com ele, a toca e a cova ficam bem mais fáceis.
- **A vila de teste não tem mesa de runas:** o foco e o amuleto se compram na loja; fazer e gravar pede que o Mestre ponha uma (`encanto.py runas N`).
- **O elixir** (a poção do Épico para cima) não tem loja: é contado, de quem o fez para quem o recebe.
- **O estado "cego"** existe na luta, mas nenhum dos 24 feitiços o põe; não há feitiço de grau 4 (a tabela do feitiço longo de 2 rodadas está pronta). As raízes não sabem o chão (a luta não tem terreno de terra).
- **As criaturas:** o lobisomem não pede prata e a mantícora e a quimera ficaram de fora (os traços "pede prata" e "atira" não estão na lista fechada); o chefe não foge com metade do PV (a fase "foge" não existe); o golem bate com a cauda da tabela dos bichos (1d10 de impacto), e a mesa lê "punho de barro"; o senhor vampiro só lança de longe (o bicho que lança usa o corpo quando alcança). O bando que foge não se junta a outro covil; o necromante e a bruxa do brejo não têm covil próprio.
- **A meta da patrulha goblin passa na beira** (vence 73%, o teto é 75; morre em 12,3%, o teto é 15): a janela desta luta é estreita, e o goblin ficou miúdo para caber nela.

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

A etapa da magia (capítulos 10 a 16):

```
python3 provas.py 600 magia                          só as metas da magia na luta (capítulo 11)
python3 provas_talento.py 300 · provas_magia.py 300 · provas_criaturas.py 300      os bancos da etapa, sozinhos (o provas_mundo.py roda os três)
python3 vila_teste.py magia PASTA [inclinacao=CAMINHO]      acrescenta a etapa da magia a uma vila de teste que já existe (só por eventos; recusa rodar duas vezes)

python3 talento.py ver [ID] | mestre [ID]           o que a pessoa sabe de si · tudo (SÓ O MESTRE)
python3 magia_mundo.py ver [ID] | estudar FEITICO com=PESSOA|escrito=ITEM|santuario|ermo [blocos=N] | voto lâmina|pobreza|socorro | laco ERMO | pacto | prece
python3 magia_mundo.py paga N pv|divida | divida N pv|osso|erva | lancar cura|bênção|seiva [alvo=ID] [paga=N] | ler maldicao|dom|peca [ALVO|ITEM] [paga=N]
python3 magia_mundo.py praga ALVO [tipo=míngua] ["Nome"] | agua N | benzer ARMA [paga=N] | tratar PACIENTE [paga=N] | jornal N | compra BEM N de=QUEM [preco=P]
python3 magia_mundo.py santuario NIVEL|nada "como foi"          (o Mestre registra)
python3 alquimia.py ver | pede POCAO CATEGORIA | fazer POCAO CATEGORIA [blocos=N] [nucleo=ID] | continua [OBRA] [blocos=N] | larga OBRA
python3 alquimia.py beber POCAO:CAT|ELIXIR [alvo=ID] [maldicao=MID] | lamina [ARMA] [cat=K] | jornal N | botica NIVEL|nada "como foi"
python3 encanto.py ver | pede foco FORMA CATEGORIA | pede amuleto CATEGORIA | fazer foco FORMA CATEGORIA ["Nome"] | fazer amuleto CATEGORIA ["Nome"]
python3 encanto.py gravar ITEM FEITICO [para=DONO] [com=QUEM_SABE] [blocos=N] [nucleo=ID] | continua | larga OBRA | jornal N | runas NIVEL|nada "como foi"
python3 maldicao.py ver [ALVO] | mestre [ALVO] | rito ALVO [MID] [paga=N] quem=CLERIGO | devolver ITEM | perdoa ALVO MID quem=QUEM_ROGOU | cumpre ALVO MID "como foi"
python3 maldicao.py poe ALVO "Nome" CATEGORIA TIPO CONDICAO [de=...] [fonte=X] [rogou=ID] "como foi" | peca ITEM "Nome" CATEGORIA TIPO [onde=LUGAR] "como foi" | lugar "Nome" CATEGORIA TIPO "como foi"
python3 mercado.py magia ["como foi"]                o Mestre abre a parte da magia do mercado (as poções, a água benta, os amuletos, os focos e o escrito)
python3 criaturas.py lista | ver ESPECIE|CHEFE | ameaca ESPECIE [N] | tracos | mede ESPECIE|CHEFE NIVEL CATEGORIA [N] | covil [ERMO] | covil poe ERMO ESPECIE [cabecas=N] [tesouro=N] [chefe=sim]
python3 caca.py sair ERMO alvo=toca                  procura a toca do covil (a rolagem é oculta)
python3 itens.py nova foco FORMA CATEGORIA "Nome" | nova amuleto CATEGORIA "Nome" | nova elixir POCAO CATEGORIA "Nome" | nova escrito CATEGORIA "Nome" feiticos=seta,luz      (com um mundo, por evento "mestre")
```

Na luta (`ato.py luta roda`, `caca.py luta`, `luta.py roda`), as ordens novas: `lancar FEITICO [em ALVO | casa N] [sempre] [osso] [neblina|lama]` · `beber POCAO [em ALIADO]` · `usar [PECA] [em ALVO | casa N]`.
No cenário, quem não vem do mundo veste também `"foco": ["cajado", "Raro"]` e `"amuleto": "Raro"`, e pode trazer `"feiticos"`, `"tradicao"`, `"tracos"`, `"fases"` e `"carga"`; a criatura entra como o bicho: `{"bicho": "goblin"}`.
