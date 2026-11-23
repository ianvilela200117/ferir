# MOTOR 10 — O LIVRO DA LUTA E DOS ITENS

Este é o livro de regras do Motor 10. É um só, por assunto, sem história: o que mudou e quando fica no `MUDANCAS.md`.
Os números moram todos no `tabelas.py`. Nenhuma regra vale antes de passar no banco de provas (`python3 provas.py`).

**Estado:** estão escritos e provados os capítulos 1 a 4 (a pessoa, os itens, a luta, o banco de provas) e o capítulo 5 (o tempo, o corpo, o estado e o turno: a etapa 1 do mundo). O plano do resto está no `PROJETO.md`.

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

2.1 **O Livro de Itens.** Toda arma, armadura e escudo é um registro (`itens.py`): nome, categoria, durabilidade, efeitos, dono, quem fez, e a história. **Peça que não está no Livro não existe.** A ficha de luta sai sozinha do que a pessoa veste (`pessoas.py`).

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
| derruba | uma vez por luta, o golpe que fere derruba | arma |
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

Falhou por pouco: fica **abalado** (−2 no acerto). Falhou de novo, ou por 10 ou mais: **quebra**. Quem quebra foge (e leva um golpe livre de quem está colado), ou **se rende** se está muito ferido ou sem saída. Rendido é prisioneiro, com nome.
**Quem o jogador comanda nunca foge nem se rende pelo dado:** ele fraqueja (fica abalado), a luta para, e a escolha é do jogador.

3.15 **O impasse e a retirada.** Oito rodadas seguidas sem ninguém ferir ninguém de verdade (menos de 2% do PV, somado), e os dois lados se separam. A luta que chega a 60 rodadas acaba em empate.
**Sair da luta:** quem tem ordem de recuar e acaba a rodada a 8 casas ou mais de todo inimigo de pé saiu da luta. Quem persegue anda o mesmo que quem foge: só se sai com alguém segurando a passagem, com o chão a favor, ou se o outro lado não vier atrás.

3.16 **A luta para e pergunta.** O script roda turno a turno. Quando algo muda, ele para **ali, no meio da rodada**, e mostra o quadro:
- a luta vai começar;
- alguém da casa cai, morre, foge, se rende, ou tem uma peça quebrada;
- o líder do outro lado cai ou foge, ou alguém de lá se rende;
- quem o jogador comanda é ferido, passa de metade ou de um quarto do PV, fica sem fôlego, fraqueja, perde o alvo, ou está segurando onde só apanha;
- passam três rodadas sem novidade.

O jogador então dá a ordem de quem ele comanda, e a ordem do grupo (só o lado dele recebe ordem; nome ou ação que não existe é recusado, com a lista do que vale):
`atacar [alvo]` (se o alvo está longe, vai até ele, contornando se a linha deixar) · `segurar` (não anda; bate em quem chega) · `avancar` · `recuar` (mantém distância) · `folego` · `guardar NOME`, e no fim a postura.
A ordem do grupo é uma palavra: `atacar`, `segurar` ou `recuar`.

---

## 4. O banco de provas

Toda mudança de regra ou de número roda `python3 provas.py`. Meta que falha: a mudança não entra, ou a meta muda com a palavra do jogador.
A medição completa está em `dados/provas_saida.txt` (600 lutas por meta). **51 de 51 passam.**

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
| um nível 120 de Lendário × dez de nível 60 de Único (uma categoria abaixo) | 15 a 60% | 51% |
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
| alcance | três lanças contra três espadas: 71% num corredor de um, 42% em campo aberto |
| distância | a arqueira contra o infante: 35% começando longe, 14% começando colada |
| tempo | a mesma arqueira: 12% na neblina, 35% com tempo limpo, 60% na lama |
| lugar | um contra quatro: 40% em campo aberto, 87% num corredor de um |
| golpe contra armadura | contra a placa: o malho 75%, o montante 45% |
| requisito | placa em quem não tem Força: Defesa 28,5 contra 36,5; fôlego 5 por rodada contra 1 |
| fôlego | quem começa o turno a zero faz uma ação só |
| sob medida | a mesma peça: +28 e × 304 no dono; +19 e × 101 na mão de outro |
| sintonia | o conjunto Épico contra três de nível 100: 59% com Vontade para as quatro peças, 17% sem |
| parte do corpo | o mesmo guerreiro sem o elmo, contra o de elmo: 34% |
| durabilidade | o mestre de nível 300 com espada Comum quebra a espada na armadura Única em 96% das lutas |
| impasse | espada Comum contra armadura Épica dos dois lados: os lados se separam em 100% |
| moral | seis contra um muito mais forte: alguém foge ou se rende em 44% das lutas; quem o jogador comanda, nunca |
| cerco e contorno | dez contra um: 4 batem por rodada; sete contra uma linha de um: os que sobram chegam em quem está atrás em 100% |
| para e pergunta | para antes da 1ª rodada; cumpre a ordem; em 93% das lutas houve parada no meio da rodada |
| retirada | com dois guardas segurando o corredor, quem recebe ordem de recuar sai da luta em 100% |
| cenário conferido | nome repetido e tempo que não existe: recusado antes de qualquer dado |

---

## 5. O mundo: o tempo, o corpo, o estado e o turno (etapa 1)

Os números deste capítulo moram no `tabelas_mundo.py`; as provas, no `provas_mundo.py` (12 de 12).

5.1 **O tempo.** O dia tem 6 blocos de 4 horas: madrugada, alvorada, manhã, tarde, entardecer, noite. Semana de 7 dias, estação de 91, ano de 364. Todo ato custa blocos. A madrugada e a noite são escuras: a luta ao ar livre ganha "escuro" sozinha.

5.2 **O corpo** tem três medidores, de 0 a 10:

| | Sobe | Desce | Cobra |
| --- | --- | --- | --- |
| Fome | +1 a cada 2 blocos | refeição −3 (1 de prata) | em 4: −2; em 7: −4, e 5% do PV máximo a cada virada do dia |
| Sono | +1 por bloco acordado | −3 por bloco na cama; −2 no chão | em 6: −2; em 8: −4, e Vontade contra 28 a cada bloco, ou dorme ali mesmo |
| Cansaço | bloco pesado +2, leve +1, luta +2 | −3 por bloco na cama; −2 no chão; −1 descansando | cada 3 pontos tiram 1 do fôlego máximo; em 9: −2 |

**A pena do corpo** é a pior das três (não somam) e entra em todo teste, no acerto e na Defesa. O mesmo homem, com sono 8 e cansaço 9, vence a si mesmo descansado em 23% das lutas.

5.3 **Curar.** Cada bloco dormido sem fome (abaixo de 4) devolve 5% do PV máximo, em no máximo dois blocos por dia: um décimo por noite. A ferida sara com **7 dias de repouso**; a grave, com **21**. Dia com dois blocos pesados não conta como repouso. Estar ferido custa: quem não trabalha não ganha.

5.4 **Viver.** Refeição 1 de prata; cama 2 por noite. O diarista ganha 2 por bloco, e a jornada são 2 blocos: sobra 1 de prata por dia. Uma refeição por dia segura a fome.

5.5 **Treinar.** Bloco de treino é pesado. A maestria numa arma sobe aos 40 blocos (Iniciante), 160 (Treinado), 500 (Mestre) e 1.500 (Lendário). De Mestre para cima, os blocos não bastam: é preciso um **feito** com a arma, que o mundo registra.

5.6 **O ato longo para.** Dormir, trabalhar, treinar ou esperar vários blocos para quando o corpo cruza um limiar (fome, sono, cansaço), e diz por quê.

5.7 **O estado e o gravador único.** O save é uma pasta com o relógio, os lugares, a gente, o Livro de Itens, o caderno do turno e o registro de eventos. **Só `estado.aplica()` muda o mundo.** Um evento sem efeito é recusado: o que não muda número não aconteceu. Um evento com um efeito errado é recusado inteiro: nada muda pela metade. Cada fato mora num lugar só (o dono de uma peça, só no Livro de Itens). O que o Mestre inventa em cena entra por um evento "mestre", com os mesmos efeitos.

5.8 **O dado de quem está em cena** (`teste.py`): 2d20 + bônus do atributo + a pena do corpo, contra um número. O comando declara e rola no mesmo passo, uma vez, e o resultado fica escrito no turno. A rolagem oculta aparece na mesa só como "rolagem oculta"; a verdade vai para a parte do Mestre.

5.9 **A luta dentro do mundo** (`ato.py luta`). Quem tem ficha no mundo entra com o que veste hoje, o PV, as feridas e a pena do corpo. Acabada, a luta volta ao estado num evento só: PV, feridas novas, mortes, o cansaço e a durabilidade das peças.

5.10 **O turno em dois comandos.**
- `turno.py abre` só lê e gera a `MESA.md`: você, o lugar, o que dá para fazer e o que custa, as perguntas abertas, e o SÓ O MESTRE.
- `turno.py responde "1a.2b"` confere cada código contra as perguntas abertas. Código que não bate é recusado, e nada é marcado.
- `turno.py fecha "o que houve"` **recusa** se: há luta aberta · há menos de 2 perguntas abertas · o relógio não andou (a não ser que se diga `parado`) · o estado quebrou um invariante. Passando, gera o `RETOMAR.md` (o agora, o que houve, os fatos do registro, as perguntas, o que só o Mestre sabe) e a `MESA.md` nova. Com `git`, guarda e envia, e avisa se o envio falhou.

---

## Os comandos

```
python3 itens.py nova arma lança Lendário "Lança do Rio Limpo" dono=Aldric feito=Bera efeito=sangra sob=Aldric:3
python3 itens.py nova armadura malha Épico "Elmo do Vau" cobre=cabeça dono=Aldric
python3 itens.py janela i0001
python3 pessoas.py padrao 50 arma=espada:Raro armadura=malha:Raro escudo=Raro
python3 luta.py nova dados/cenario_exemplo.json lutas/corredor.json
python3 luta.py roda lutas/corredor.json "Aldric: atacar o chefe agressiva" "grupo: segurar"
python3 luta.py demo
python3 provas.py

python3 provas_mundo.py                              as provas do mundo
python3 provas_mundo.py vila /caminho/da/pasta       cria uma vila de prova para experimentar
MOTOR10_MUNDO=/caminho/da/pasta python3 turno.py abre
python3 ato.py comer | dormir N | trabalhar N | treinar N ARMA | descansar N | esperar N
python3 ato.py luta nova CENARIO.json LUTA.json  ·  python3 ato.py luta roda LUTA.json "Nome: atacar"
python3 teste.py "o que se tenta" Força contra=26 [oculto]
python3 turno.py pergunta "texto" "a=..." "b=..."  ·  turno.py responde "1a.2b"  ·  turno.py fecha "o que houve"
python3 estado.py valida | eventos | pessoa ID
```

No cenário, cada pessoa veste `arma`, `arma2`, `armadura`, `elmo`, `escudo` e `pecas` (mais peças de armadura). Cada uma é o id de um item do Livro, ou um atalho para gente miúda: `["espada", "Raro"]`. O atalho de armadura veste o corpo e um elmo igual; `"elmo": false` tira o elmo.
