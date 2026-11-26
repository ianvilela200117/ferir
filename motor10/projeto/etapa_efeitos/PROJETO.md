# A ETAPA DOS EFEITOS — o projeto (Motor 10)

## O pedido do jogador (Dia 24 do mundo novo, palavras dele)
> "Lógico que equipamentos devem entrar na forja. [...] Além do item, efeitos, habilidades e magias devem ser muito determinantes, e bem feitos, com habilidades,
> efeitos e magias que mudam tudo, assim como item, sem falar nos efeitos dos itens, que têm que ser muito importantes e apelões. Lógico, balanceado de acordo com tudo,
> porém habilidade, efeitos, magias, itens, efeitos de itens, entre outros, deve existir a possibilidade desde a apelação até o normal e fraco."

## O que o motor já tinha (medido no Dia 24)
- **Efeitos de item:** 8 que a luta roda (sangra, critico_19, derruba, devolve, firme, leve, pesa, nao_quebra). Todos pequenos. **Nenhuma peça do mundo tem efeito**
  (as 13 peças com nome da história, de Épica a Mítica, nasceram com a lista vazia), e a forja não dava efeito nenhum.
- **Magias:** 24 feitiços e o truque, graus 0 a 4, em quatro tradições; o encanto grava um feitiço numa peça (uma, e duas do Único para cima).
- **Habilidades:** não existem. A maestria de arma soma acerto; a de ofício soma no teste.
- **Dons e talentos:** existem (Lerdo, Jeitoso, Prodígio, Dom escondido).

## Parte 1 — FEITA no Dia 24 (REGRAS 7.14 a 7.16; MUDANCAS.md)
- A ferramenta do ofício (o jogo de forja e o de couro), do Comum +1 ao Lendário +6, com um poder por categoria (o da Lendária é o "apelão" da forja: a peça nasce uma
  categoria acima).
- A obra-prima: a peça que passa por 10, 20, 30 ganha 1, 2, 3 efeitos por escolher (teto pela categoria), entre os que a luta já roda.

## Parte 2 — a etapa grande (a construir)
### 2.1 Os efeitos de item, em quatro faixas
Cada efeito tem uma FAIXA, e a categoria da peça diz até que faixa ela pode levar:

| Faixa | Pode estar em | Medida no banco da luta (duelo de iguais, a peça com o efeito contra a mesma sem ele) |
| --- | --- | --- |
| fraco | do Comum para cima | a vitória sobe de 2 a 5 pontos |
| normal | do Incomum para cima | de 5 a 10 pontos |
| forte | do Épico para cima | de 10 a 20 pontos |
| apelão | do Lendário para cima | de 20 a 40 pontos (muda a luta) |

Um começo de catálogo (cada um vira um gancho no `luta.py` e uma linha no `itens.EFEITOS`, com a faixa):
- **fraco:** certeira (+1 no acerto), guarda (+1 na defesa), leve, nao_quebra, sangra, caçadora (+dano contra um tipo de bicho), luz (a peça clareia o escuro).
- **normal:** critico_19, derruba, firme, devolve, veloz (age antes), folego (um golpe custa 1 de fôlego a menos), aparadora (+2 na defesa quando apara).
- **forte:** segundo golpe (um golpe a mais, uma vez por luta), vampira (cura uma parte do dano que faz), perfura (a proteção conta pela metade), elemental (fogo ou gelo:
  um dado a mais por categoria e a queimadura), temível (o inimigo testa a moral ao ver a peça), regenera (a armadura devolve PV por rodada), refletora (o escudo devolve
  um feitiço por luta).
- **apelão:** ceifadora (quem mata golpeia de novo), golpe do fim (crítico de 17 a 20, e o crítico vale quatro vezes), tempestade (o golpe pega todos os vizinhos),
  imortal (uma vez por dia, o dono fica com 1 PV em vez de cair), domínio (a peça solta um feitiço de grau 4 uma vez por dia).

### 2.2 As peças do mundo com efeitos
- As peças com nome da história (as 13 de Épica a Mítica, como o Malho do Silêncio) ganham efeitos da faixa da categoria, sorteados pela semente do mundo e com o nome
  e a história delas (o Malho do Silêncio: algo de silêncio, o feitiço que cala).
- O tesouro da masmorra e do dragão: a peça Rara ou melhor sai com efeito, com a chance pela categoria.
- O rival que forja (a capital) e o ferreiro do mundo: a obra-prima deles escolhe sozinha (pela semente).

### 2.3 As habilidades (a maestria vira técnica)
- **Arma:** cada família ganha uma técnica no Treinado, uma melhor no Mestre e uma "apelona" no Lendário. Exemplos: o martelo esmaga (a proteção conta menos), a espada
  riposta, a lança mantém à distância, o arco mira (um tiro a mais de acerto). Cada uma tem um custo (fôlego, uma vez por luta) e uma medida no banco da luta.
- **Ofício:** a forja de Mestre lê os efeitos de uma peça; a de Lendário refaz a obra que falhou uma vez por obra. O ladino, o caçador e o curandeiro, o mesmo caminho.
- **Magia:** a maestria da tradição abre a forma forte do feitiço (o mesmo feitiço, mais longe, mais gente, mais dano).

### 2.4 As magias que mudam tudo
- Um quinto degrau, acima do grau 4: os feitiços "apelões" (parar o tempo da luta por uma rodada, a chuva de fogo, trazer de volta quem caiu nesta luta), com custo de
  verdade: muita Mana, um núcleo, ou anos de vida (como as Míticas do Ferir).
- Conferir a força dos 24 de hoje pela mesma régua de faixas, e subir os que estão fracos demais.

### 2.5 O equilíbrio (o banco)
- O banco da luta (`provas.py`) ganha uma prova por faixa: cada efeito, cada técnica e cada feitiço novo medido contra a meta da faixa dele.
- O banco do ano (`provas_ano.py`) confere que o mundo não explode: os rivais com peças fortes não matam o dragão no primeiro mês, e a corrida continua com mortos.
- A semente que reprova não vira save; o mundo de verdade só ganha os efeitos das peças da história por evento do Mestre, com o jogador sabendo.

## A ordem proposta
1. Os efeitos de item novos (2.1) com os ganchos na luta, e a prova por faixa.
2. As peças do mundo com efeitos (2.2), no mundo de verdade por evento do Mestre.
3. As habilidades de arma e de ofício (2.3).
4. O quinto degrau da magia e a régua dos 24 feitiços (2.4).
