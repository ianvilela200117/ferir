# MOTOR 10 — O LIVRO DA LUTA E DOS ITENS

Este é o livro de regras do Motor 10. É um só, por assunto, sem história: o que mudou e quando fica no `MUDANCAS.md`.
Os números moram todos no `tabelas.py`. Nenhuma regra vale antes de passar no banco de provas (`python3 provas.py`).

**Estado (Dia 507):** estão escritos e provados os capítulos 1 a 4 (a pessoa, os itens, a luta, o banco de provas). Faltam a magia, os bichos e o mundo (capítulo 5).

**Precedência:** este livro manda. Onde ele cala, vale o Livro do Mundo (o compêndio). Regra antiga do save do Ferir não vale aqui.

**O dado:** todo teste é **2d20 + o que a pessoa soma**, contra um número. Cada 20 rola de novo e soma. O script rola; ninguém rola de cabeça.

---

## 1. A pessoa

1.1 **Atributos.** Seis entram na luta: Força, Agilidade, Vigor, Vontade, Percepção, Afinidade. O bônus de um atributo é o atributo ÷ 10.

1.2 **Nível.** Cada nível dá 1 ponto de atributo e meio ponto de PV. Fora isso, o nível não soma em nada na luta: nem no acerto, nem no dano, nem nas ações.

1.3 **Maestria** na arma: Leigo 0, Iniciante 2, Treinado 4, Mestre 6, Lendário 8. Vem de treino e de feito, não de nível.

1.4 **O que sai disso** (o script calcula):

| | Conta |
| --- | --- |
| PV | Vigor × 2 + nível ÷ 2 |
| Fôlego | 6 + bônus de Vigor |
| Acerto | maestria + (bônus de Força + bônus de Agilidade) ÷ 4 + o bônus da arma |
| Defesa | 24 + bônus de Agilidade ÷ 2 + maestria ÷ 2 + o bônus do escudo (sem escudo: metade do bônus da arma, ao aparar) |
| Força do golpe | o dano vezes 1 + 0,04 por ponto de bônus de Força (arco: Agilidade) |
| Ações por rodada | 2; Mestre 3; Lendário 4 |
| Reações por rodada | 1; Lendário 2 |

---

## 2. Os itens

2.1 **O Livro de Itens.** Toda arma, armadura e escudo é um registro (`itens.py`): nome, categoria, durabilidade, efeitos, dono, quem fez, e a história. **Peça que não está no Livro não existe.** A ficha de luta sai sozinha do que a pessoa veste (`pessoas.py`).

2.2 **As oito categorias** e o que cada uma vale:

| Categoria | Valor (arma e armadura) | Bônus (acerto ou Defesa) | Durabilidade |
| --- | --- | --- | --- |
| Comum | 1 | 0 | 10 |
| Incomum | 2,5 | +3 | 20 |
| Raro | 6 | +6 | 30 |
| Épico | 15 | +9 | 40 |
| Único | 40 | +12 | 50 |
| Lendário | 100 | +15 | 60 |
| Mítico | 250 | +18 | 80 |
| Primordial | 600 | +21 | 100 |

2.3 **A regra de ouro: o item decide.** Cada categoria vale 2,5 vezes a de baixo, e o que conta é a **diferença** entre a arma de quem bate e a armadura de quem apanha:

| A arma está… | O golpe vale |
| --- | --- |
| na mesma categoria da armadura | × 1 |
| uma acima | × 2,5 |
| duas acima | × 6 |
| três acima | × 15 |
| uma abaixo | × 0,4 |
| duas abaixo | × 0,16 |
| três abaixo ou mais | quase nada (só o crítico arranha) |

Parte do corpo sem armadura conta como um degrau abaixo do Comum.

2.4 **As armas.**

| Arma | Dado | Golpe | Alcance | Mãos | Peso |
| --- | --- | --- | --- | --- | --- |
| mãos, adaga | 1d4 | impacto, ponta | 1 casa | 1 | leve |
| espada | 1d8 | corte | 1 | 1 | média |
| maça | 1d8 | impacto | 1 | 1 | média |
| lança | 1d8 | ponta | 2 | 1 | média |
| machado | 1d10 | corte | 1 | 1 | pesada |
| martelo | 1d10 | impacto | 1 | 1 | pesada |
| montante | 1d12 | corte | 1 | 2 | pesada |
| alabarda | 1d12 | corte | 2 | 2 | pesada |
| malho | 1d12 | impacto | 1 | 2 | pesada |
| arco | 1d8 | ponta | à distância | 2 | média |
| besta | 1d10 | ponta | à distância (recarrega 1 ação) | 2 | média |

Arma de duas mãos: o valor vezes 1,25, e não se usa escudo. Arma pesada: 2 de fôlego por golpe.

2.5 **As armaduras.** A peça cobre partes do corpo (cabeça, tronco, braços, pernas).

| Material | Proteção | Pede de Força | Fôlego |
| --- | --- | --- | --- |
| couro | metade do valor | 40 | nada |
| malha | o valor | 60 | nada |
| placa | uma vez e meia o valor | 80 | 1 por rodada em que a pessoa age |

2.6 **O golpe contra o material.** A proteção da peça vezes:

| | couro | malha | placa |
| --- | --- | --- | --- |
| corte | 0,85 | 1,25 | 1,5 |
| ponta | 1 | 0,85 | 1,15 |
| impacto | 1,15 | 1 | 0,7 |

O fio abre o couro e escorrega no metal; a ponta abre o elo da malha; o malho amassa a placa.

2.7 **O requisito é por atributo, nunca por nível.** Qualquer pessoa empunha qualquer peça, de qualquer categoria.
- A peça pede **Força pelo peso**: leve 40, média 60, pesada 80 (a adaga e o arco pedem Agilidade). A categoria não muda o que ela pede.
- **Faltou atributo, a peça pesa:** −1 no acerto (arma) ou na Defesa (armadura, escudo) a cada 5 pontos que faltam, e +1 de fôlego a cada 10.

2.8 **Sob medida.** Peça feita ou ajustada por um ferreiro para um dono, com o nome gravado:
- **para o dono**, pede 10 a menos por grau do ferreiro (graus 1 a 4) e assenta (+1 no acerto ou na Defesa; a armadura protege um décimo a mais);
- **na mão de outro**, rende uma categoria abaixo.

2.9 **Sintonia.** A pessoa sustenta **Vontade ÷ 20** peças Épicas ou melhores com efeito desperto (no mínimo uma). As que passam disso **dormem**: os números da categoria seguem valendo, os efeitos não.

2.10 **Durabilidade.** O aço gasta o aço:
- a arma perde 1 quando bate numa armadura de categoria maior, e 1 quando o dono tira dois 1;
- a armadura perde 1 quando leva golpe de arma de categoria maior ou um crítico (2, se a arma está duas categorias acima);
- **a zero, quebra:** a arma vira um pedaço de ferro Comum com −4 no acerto; a parte da armadura deixa de proteger.
- Consertar é ofício de ferreiro, fora da luta.

2.11 **Efeitos.** Uma peça só leva efeito que a luta sabe rodar. Os de hoje: a ferida sangra · o 19 também é crítico · o golpe derruba (1 vez por luta) · devolve dano em quem golpeia · o dono não é derrubado · leve (pede 20 a menos) · pesa (pede 20 a mais) · não quebra.

2.12 **A janela do item** aparece na cena quando a peça nasce, muda de mão ou quebra (`python3 itens.py janela ID`).

---

## 3. A luta

3.1 **O campo** é uma linha de casas (1 casa ≈ 3 m). Cada lado tem a frente e a linha de trás. A luta começa **longe** (8 casas), **perto** (3) ou **colada** (1).

3.2 **A rodada.** No começo da luta, cada um rola a iniciativa (2d20 + bônus de Percepção + bônus de Agilidade) e age nessa ordem até o fim. No turno, a pessoa recupera 1 de fôlego e gasta as suas ações.

3.3 **As ações:**
- **golpear** quem a arma alcança (custa o fôlego da arma);
- **atirar** em quem está a 2 casas ou mais (arco e besta não atiram com inimigo colado: a pessoa puxa a segunda arma);
- **andar** 2 casas (custa 1 de fôlego);
- **tomar fôlego** (+1d4+1, e +2 na Defesa até o próximo turno);
- **levantar-se**, **apanhar a arma**, **recarregar**, **esperar** (+2 na Defesa).

3.4 **O golpe.** 2d20 + acerto contra a Defesa.
- **Crítico:** um dado deu 20 e o outro, 11 ou mais. Acerta sempre, os dados do dano dobram e a proteção vale a metade.
- **Dois 1:** erra, e a arma perde 1 de durabilidade.
- **Onde cai** (d10): 1 cabeça · 2-3 braços · 4-7 tronco · 8-10 pernas.
- **O dano:** dado × 4,5 × o valor da arma ÷ a proteção da parte atingida, vezes a força do golpe.

3.5 **Distância e alcance.**
- A arma de 1 casa bate em quem está colado. A lança e a alabarda batem a 2 casas, por cima do ombro de quem está na frente.
- **O alcance bate primeiro:** quem entra no alcance de uma arma mais longa que a sua leva um golpe livre (gasta a reação de quem bate).
- **Recuar** de quem está colado dá a ele um golpe livre.
- Golpe ou tiro com alguém de pé no caminho: −2.
- Ninguém atravessa um inimigo de pé. Em campo aberto, cada um segura dois; quem sobra contorna e chega à linha de trás.

3.6 **O lugar.**
- **Estreito** (largura N): só N de cada lado cabem em cada casa. Ninguém contorna.
- **Alto:** quem está no alto tem +1 no golpe e +2 no tiro; quem sobe anda 1 casa por ação.
- **Cobertura:** −4 no tiro contra quem a tem.
- **Sem saída:** quem quebra ali não foge, rende-se.

3.7 **O tempo e o chão** entram sozinhos, do dia:

| | Efeito |
| --- | --- |
| escuro | −4 no golpe, −8 no tiro |
| chuva | −4 no tiro |
| vento | −2 no tiro |
| neblina | −4 no tiro; não se atira além de 3 casas |
| lama | anda-se 1 casa por ação |
| calor | malha e placa custam 1 de fôlego a mais por rodada |
| água pela cintura | anda-se 1 casa; −2 na Defesa; 1 de fôlego a mais por rodada |

3.8 **Fôlego.** Cada golpe e cada passo custam. Com fôlego zero a pessoa tem uma ação só e −4 no acerto e na Defesa, até tomar fôlego.

3.9 **Posturas.** Firme (nada muda) · agressiva (+2 no acerto, −2 na Defesa) · defensiva (−2 no acerto, +2 na Defesa, +1 de fôlego por rodada).

3.10 **Ferida.** Um golpe que tira um quarto do PV máximo, ou um crítico que fere, abre uma ferida na parte atingida. Com metade do PV máximo, a ferida é **grave**.

| Parte | Ferida | Grave |
| --- | --- | --- |
| cabeça | atordoado: perde 1 ação | perde 2 ações |
| braços | −2 no acerto | −4, e larga a arma |
| tronco | perde 3 de fôlego e sangra | perde 6 e sangra |
| pernas | vai ao chão | vai ao chão e não anda mais |

Quem sangra perde 3% do PV máximo por rodada. No chão: −4 na Defesa, e levantar gasta uma ação. A ferida fica depois da luta.

3.11 **Cair e morrer.** A zero de PV a pessoa cai. Se o golpe que a derrubou tirou mais da metade do PV máximo, ela morre na hora. Caída, rola 1d20 por rodada contra 12: três falhas, morre; três sucessos, fica estável.

3.12 **Moral.** Quem não é de ferro testa a coragem (2d20 + bônus de Vontade; +2 com o líder de pé; +2 se o seu lado tem mais gente; −4 se o outro tem o dobro):

| O susto | Contra |
| --- | --- |
| viu um golpe terrível num dos seus (metade do PV de uma vez), a 2 casas | 24 |
| está abaixo de um quarto do PV | 26 |
| metade do seu lado caiu | 26 |
| o líder caiu ou fugiu | 29 |

Falhou por pouco: fica **abalado** (−2 no acerto). Falhou de novo, ou por 10 ou mais: **quebra**. Quem quebra foge (e leva um golpe livre de quem está colado), ou **se rende** se está muito ferido ou sem saída. Rendido é prisioneiro, com nome.

3.13 **Guardar alguém.** Quem guarda fica a 1 casa do guardado e põe o corpo na frente do golpe (gasta a reação).

3.14 **A luta para e pergunta.** A rodada acaba e o script mostra o quadro quando:
- a luta vai começar;
- alguém da casa cai, morre, foge, se rende, ou tem uma peça quebrada;
- o líder do outro lado cai ou foge, ou alguém de lá se rende;
- quem o jogador comanda é ferido, passa de metade ou de um quarto do PV, fica sem fôlego, ou perde o alvo;
- passam três rodadas sem novidade.

O jogador então dá a ordem de quem ele comanda, e a ordem do grupo:
`atacar [alvo]` · `segurar` (não anda; bate em quem chega) · `avancar` · `recuar` (mantém distância) · `folego` · `guardar NOME`, mais a postura.

---

## 4. O banco de provas

Toda mudança de regra ou de número roda `python3 provas.py`. Meta que falha: a mudança não entra, ou a meta muda com a palavra do jogador.

As metas de hoje (a medição completa está em `dados/provas_saida.txt`):

| O que se mede | Meta | Medido |
| --- | --- | --- |
| iguais em tudo | 44 a 56% | 53% |
| mesmo nível, só a arma uma categoria acima | 80 a 99% | 93% |
| mesmo nível, o conjunto uma categoria acima | 88 a 100% | 100% |
| mesma arma, nível 75 contra 50 | 52 a 68% | 57% |
| mesma arma, nível 150 contra 50 | 85 a 100% | 96% |
| uma categoria na arma contra 100 níveis (50 × 150) | 35 a 65% | 51% |
| duas categorias na arma contra 150 níveis (50 × 200) | 60 a 95% | 86% |
| **uma arma duas acima, nível 50 × nível 500** | 10 a 40% | **28%** |
| **uma arma três acima, nível 50 × nível 500** | 55 a 90% | **76%** |
| o conjunto duas acima, nível 50 × nível 500 | 85 a 100% | 100% |
| um nível 90 de conjunto Mítico × dez de nível 275 de Raro | 90 a 100% | 100% |
| o mesmo, só com a arma Mítica | 0 a 40% | 0% |
| um nível 120 de Lendário × dez de nível 60 de Único | 0 a 25% | 1% |
| um nível 120 de Lendário × dez soldados Comuns | 97 a 100% | 100% |
| duração de um duelo entre iguais | 4 a 9 rodadas | 4 |
| duração de cinco contra cinco | 4 a 12 rodadas | 7 |

Mais onze provas de módulo: o alcance, a distância, o escuro, o corredor, o golpe contra a armadura, o requisito, o sob medida, a sintonia, a durabilidade, a moral, e a luta que para e obedece à ordem.

---

## 5. O que falta escrever (nesta ordem)

1. **A magia e os encantos de peça**, na mesma escala (o feitiço de uma peça não pode decidir a luta sozinho).
2. **Os bichos:** o corpo como arma e armadura, o tamanho, os traços.
3. **O ofício:** forjar, o sob medida, consertar, a escada das categorias, o teto do mundo para peças.
4. **O mundo vivo:** gente com lugar, rotina e vontade própria; a caixa de entrada com prazo; as horas e o corpo do personagem; a economia; os rivais.
5. **O turno em dois comandos** (`abre` e `fecha`) e o estado num lugar só.

## Os comandos

```
python3 itens.py nova arma lança Lendário "Lança do Rio Limpo" dono=Eiagrir feito=Ferir efeito=sangra sob=Eiagrir:3
python3 itens.py janela i0001
python3 pessoas.py padrao 50 arma=espada:Raro armadura=malha:Raro escudo=Raro
python3 luta.py nova dados/cenario_exemplo.json lutas/corredor.json
python3 luta.py roda lutas/corredor.json "Aldric: segurar defensiva" "grupo: segurar"
python3 luta.py demo
python3 provas.py
```
