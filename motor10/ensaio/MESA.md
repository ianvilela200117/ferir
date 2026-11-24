# MESA · turno 4 · Dia 2, tarde (12h) · primavera

## Você
**Maro**, nível 5 · PV 141/141 · 23 de prata · FORA, na Mata do Corvo (mora em Pedra Rasa)
Corpo: sem fome (fome 1) · sem sono (sono 2) · com forças (cansaço 2)
```
Maro (nível 5, mão de Iniciante) · PV 141/141 · fôlego 13 · 2 ações (a mais: 1 pelo dobro do fôlego)
  Espada de Maro: acerto +5,25 · 1d8 × 1 (corte), força × 1,21 · 1 de fôlego por golpe
  Defesa 30 (com Escudo de Maro) · proteção: cabeça 1 · tronco 1 · braços 1 · pernas 1
```
Peças (`ato.py vestir ITEM` · `ato.py tirar ITEM`): i0010 elmo de malha Comum (10/10) · EM USO, no corpo · i0028 Espada de Maro (Comum, 10/10) · EM USO, na mão · i0029 Escudo de Maro (Comum, 10/10) · EM USO, no braço · i0030 Armadura de malha de Maro (Comum, 10/10) · EM USO, no corpo
Treino: espada: 41 blocos (Iniciante) · caça: 1 bloco (Leigo)

## Aqui
**Maro está fora, na Mata do Corvo.** Enquanto a saída estiver aberta, os atos da vila não valem (comer da carga vale: `ato.py comer carga`). O que há à frente está em "A caça e a coleta".

## A caça e a coleta
- **SAÍDA ABERTA:** caçando corça na Mata do Corvo desde o Dia 2; resta 1 bloco; À FRENTE: 2 corças: `caca.py atacar`, `deixar` ou `fugir` (a ameaça e o que a posição dá: `caca.py ver`)
- **a Mata do Corvo** (floresta, borda), a 1 bloco [`mata`] · caça: corça (há fartura), javali (há fartura), lobo (há fartura), urso (há pouco, e sempre foi assim), pantera (há pouco, e sempre foi assim) · tira-se: madeira Comum (há fartura), erva Comum (há fartura)
- A sua mão: caça Leigo (1 bloco), coleta Leigo (0 blocos). O rastro: 2d20 + 5 contra 20 ou mais (o bicho arisco e o que rareou pedem mais; de noite, −4). A coleta: 2d20 + 7 (minério, madeira) ou + 5 (erva) contra 20, mais 8 por categoria, e o que rareou pede mais; o bloco que passa rende 1 de minério, 2 de madeira ou 1 de erva, e o que falha não rende.
- `caca.py sair [ERMO] [alvo=ESPECIE] [blocos=N]` (ida, N de procura, volta; N de 1 a 6, 2 se não disser) · `caca.py coletar BEM [ERMO] [blocos=N]` (N de 1 a 4)

## Os bichos daqui (o que todo mundo sabe; a frase inteira: `bichos.py ameaca ESPECIE`)
- corça (grau F, Comum, média, de 1 a 2) · javali (grau E, Comum, médio, sozinho: investida) · lobo (grau D, Incomum, médio, bando de 3 a 5: matilha) · urso (grau D, Incomum, grande, sozinho: agarra) · pantera (grau C, Raro, média, sozinha: bote)

## Perguntas abertas
1. Diante das duas corças (Maro viu primeiro; elas perdem o primeiro turno), o que ele faz?  **a)** ataca, começando de perto · **b)** ataca, começando de longe · **c)** deixa as duas irem e segue a procura (resta 1 bloco) · **d)** larga a caçada e volta para a vila
2. Se uma corça fugir ferida, Maro segue o rastro de sangue?  **a)** segue · **b)** não segue

## SÓ O MESTRE
- a contagem na Mata do Corvo: corça 80/80 · javali 40/40 · lobo 12/12 · urso 3/3 · pantera 1/1 · serpe 1/1 · acaso 3% por bloco
- o estado está inteiro.
