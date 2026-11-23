# Motor 10, projeto: a magia e os encantos de peça

**Problema:** no motor antigo o feitiço de uma peça decidia a luta (um toque de 1.680).
**Saída:** a magia usa a conta do aço: o foco é a arma, a guarda é a armadura, só a diferença de categoria conta, e feitiço não tem multiplicador. De seu, ela dá alcance, área, controle, cura, clima e moral.

As seções 1 e 2 são o rascunho do capítulo 5 do `REGRAS.md`.

## 1. Capítulo 5: a magia (rascunho)

5.1 **A pessoa.** Maestria de Magia como a da arma (0 a 8). As ações saem da maior maestria.
- **Mana:** (Afinidade + Vontade) ÷ 5.
- **Conjuração:** maestria de Magia + (bônus de Afinidade + bônus de Vontade) ÷ 4 + bônus do foco.
- **Firmeza:** 24 + bônus de Vontade ÷ 2 + maestria ÷ 2 + bônus do amuleto (sem ele, metade do bônus da armadura).
- **RM:** o valor da categoria da armadura do tronco (o material não conta) ou do amuleto, o maior. Sem nada: 0,4.
- **Força do feitiço:** 1 + 0,03 por ponto de bônus de Afinidade.

5.2 **Foco e amuleto** são itens do Livro, com valor e bônus da categoria. Varinha: 1 mão, pede Vontade 40. Cajado: 2 mãos, valor × 1,25, pede Vontade 60. Sem foco: Comum, com −4. **Círculo máximo:** categoria do foco + 2 (Comum 2º, Primordial 9º) e o da maestria (Iniciante 2º, Treinado 4º, Mestre 6º, Lendário 8º).

5.3 **O custo.** Mana: 2 por círculo. Ações: 1 até o 2º círculo, 2 até o 4º, 3 até o 6º, 4 até o 8º; cada uma custa 1 de fôlego. A Mana só volta com descanso: um quarto por período, inteira com a noite dormida. Sem Mana, paga-se em PV: 3% do máximo por ponto.

5.4 **Canalizar.** O feitiço que não cabe na rodada acaba na seguinte. Até lá: −2 na Defesa; se levar dano, 2d20 + bônus de Vontade + maestria de Magia contra 26 (30 com ferida), ou perde feitiço e Mana. Lançar com inimigo colado dá a ele um golpe livre.

5.5 **O teste.** 2d20 + Conjuração contra a Defesa (o que voa) ou a Firmeza (o que prende, cega, assusta). Crítico e dois 1 como no golpe. Escuro, cobertura e gente no caminho valem como no tiro. Chuva: Chama −4. Calor: Gelo −4.

5.6 **O dano.** dado × 4,5 × valor do foco ÷ RM, vezes a força do feitiço. Teto do dado: 1 ação, 1d8; 2, 1d12 (área 1d6); 3, 2d8 (área 1d8); 4, 2d10 (área 1d10).

5.7 **A área** pega uma casa: até 4 pessoas, amigo e inimigo. Um teste contra a Defesa de cada um; quem escapa leva metade.

5.8 **A cura.** dado × 3 × valor do foco ÷ valor da **ferida mais funda** (a maior categoria que feriu a pessoa desde que ficou inteira). Teto: metade do PV máximo por dia. Ferida não fecha na luta.

5.9 **O controle** só põe estado que a luta roda (preso, chão, atordoado, abalado; no campo, neblina, escuro, lama), com prazo em rodadas. Cada controle que pega deixa o alvo **calejado**: +4 de Firmeza até o fim da luta.

5.10 **Sustentar.** Um feitiço por vez, 1 de Mana por rodada.

5.11 **Retrochoque.** Com dois 1, ou ao **forçar** um círculo acima do limite (−4; basta um 1). Volta em quem lança: (círculo)d4 × 4,5 × valor do foco ÷ a própria RM; o foco perde 1 de durabilidade. Foco acima da própria guarda: o triplo por degrau.

5.12 **Moral.** O lado sem ninguém de Magia testa a coragem contra 24 na primeira área que o pega.

## 2. O encanto de peça (5.13)

- É um feitiço gravado numa peça. O passivo segue sendo "efeito" (2.11).
- **Pede:** quem grava sabe o feitiço, tem uma Essência da categoria da peça e passa no teste do ofício.
- **Quantos:** um por peça; dois de Único para cima. Essências opostas não moram juntas.
- **Círculo:** até a categoria + 1.
- **Na luta:** o dono solta com as ações do feitiço e a Mana dele, **uma vez por luta**. A Conjuração usa a maestria de quem gravou (graus 1 a 4: 2, 4, 6, 8).
- **Escala:** arma, armadura e escudo são foco **um degrau abaixo** da própria categoria. O foco vale inteiro.
- **Sintonia:** peça encantada de qualquer categoria ocupa um lugar (Vontade ÷ 20). A que dorme não solta.
- **Por que não quebra a luta:** contra um igual, o encanto de dano vale um terço de um golpe, sai uma vez e custa ação e Mana. Ele dá alcance, controle, luz e cura. Contra a multidão duas categorias abaixo, limpa a casa: aí a Lendária muda tudo.

## 3. Feitiços de partida (`tabelas_magia.py`)

Mana e ações saem do círculo. `alc` em casas.

```python
FEITICOS = {
 'faisca':          dict(escola='Chama',  circ=1, alc=8, alvo='um',      contra='defesa',  dano='1d8'),
 'flor_de_brasa':   dict(escola='Chama',  circ=3, alc=8, alvo='casa',    contra='defesa',  dano='1d6', meio=True),
 'geada':           dict(escola='Gelo',   circ=2, alc=6, alvo='um',      contra='firmeza', dano='1d4', poe=('preso', 1)),
 'nevoa_fria':      dict(escola='Gelo',   circ=2, alvo='campo', poe_campo='neblina', sustenta=True),
 'pele_de_pedra':   dict(escola='Pedra',  circ=2, alc=1, alvo='aliado',  poe=('pele', 3)),
 'empurrao':        dict(escola='Vento',  circ=1, alc=4, alvo='um',      contra='firmeza', empurra=2),
 'escudo_de_vento': dict(escola='Vento',  circ=3, alc=2, alvo='aliado',  poe=('desvia', 3)),
 'luz':             dict(escola='Luz',    circ=1, alvo='campo', tira_campo='escuro', sustenta=True),
 'cura_menor':      dict(escola='Luz',    circ=2, alc=1, alvo='aliado',  cura='1d8'),
 'clarao':          dict(escola='Luz',    circ=3, alc=4, alvo='casa',    contra='firmeza', poe=('cego', 1)),
 'raizes':          dict(escola='Raiz',   circ=3, alc=6, alvo='um',      contra='firmeza', poe=('preso', 2)),
 'breu':            dict(escola='Sombra', circ=2, alvo='campo', poe_campo='escuro', sustenta=True),
 'medo':            dict(escola='Sombra', circ=3, alc=6, alvo='um',      contra='firmeza', moral='medo'),
 'fechar_ferida':   dict(escola='Sangue', circ=2, alc=1, alvo='aliado',  cura='1d6', tira='sangra', paga_pv=0.05),
 'segurar_o_fio':   dict(escola='Osso',   circ=2, alc=4, alvo='caido',   estabiliza=True),
 'desfazer':        dict(escola='Vazio',  circ=3, alc=8, alvo='feitico', contra='conj', reacao=True),
 'partilhar_a_dor': dict(escola='Elo',    circ=3, alc=2, alvo='aliado',  poe=('elo', 0), sustenta=True),
 'pressa':          dict(escola='Tempo',  circ=2, alc=1, alvo='aliado',  poe=('pressa', 1), uma_vez=True),
 'distrair':        dict(escola='Mente',  circ=1, alc=6, alvo='um',      contra='firmeza', poe=('sem_reacao', 1)),
 'calma':           dict(escola='Mente',  circ=2, alc=2, alvo='casa',    tira='abalado'),
}
```

`ESTADOS` novos: cego (−4 no golpe, −8 no tiro); pele (+4 na Defesa); desvia (−8 no tiro contra o alvo); pressa (+1 ação); elo (metade do dano do alvo vem para quem lança). `paga_pv`: PV em vez de Mana.

## 4. Ganchos

- **`tabelas_magia.py` (novo):** `K_CURA`, `MANA_DIV`, `MANA_CIRC`, `TEMPO_CIRC`, `DADO_TETO`, `FOCOS`, `CIRC_FOCO`, `CIRC_MAESTRIA`, `ENCANTO_DEGRAU`, `ENCANTOS_POR_PECA`, `AREA_ALVOS`, `CALEJO`, `CONCENTRA`, `SEM_MANA`, `CURA_TETO`, `ESTADOS`, `FEITICOS`.
- **`itens.py`:** `item()` aceita `tipo='foco'` e `'amuleto'`; o registro ganha `encantos` (`feitico`, `grau`, `feito_por`, `dia`); função e comando `encanta` (recusa lugar cheio, círculo alto, Essência oposta); `pede()` e `janela()` leem foco e encantos.
- **`pessoas.py`:** a pessoa ganha `maestria_magia`, `feiticos`, `mana`, `funda`, `cura_hoje`; `veste(foco=, amuleto=)`; `ficha()` soma `manamax`, `mana`, `conj`, `rm`, `firmeza`, `foco`, `feiticos`, `encantos`; `com_efeito` conta toda peça com `encantos`; `linha()` mostra a magia.
- **`magia.py` (novo):** `lanca(S, f, feitico, alvo, via)`, `dano_magico`, `cura`, `poe`, `retrochoque`, `concentra`, `passa`, `campo_passa`, `escolhe` (quem não é do jogador), `janela` (a do feitiço), `confere` (recusa dado acima do teto e estado desconhecido).
- **`luta.py`:** `nova()` cria `canaliza`, `postos`, `calejo`, `sustenta`, `S['campo']`; `_decide()` devolve `('lanca', feitico, alvo)`; `_turno()` chama `magia.passa` e roda `lanca`; `golpe()` grava `e['funda']`, chama `magia.concentra` e lê `postos` na Defesa; `rodada()` chama `magia.campo_passa`; `_moral()` ganha `medo` e `feitico`; `ordem()` aceita `lancar FEITICO [alvo | casa N]`; `_para()` ganha três paradas (feitiço longo do outro lado; Mana a um quarto; retrochoque); `situacao()` mostra Mana, canalização e campo; `_fecha_gente()` devolve `mana`, `funda`, `cura_hoje`.
- **`provas.py`:** `METAS_MAGIA`, `modulos_magia()`.

## 5. Metas

Entre parênteses: rascunho por cima do `luta.py` (fora do repositório; 600 lutas por linha; só Faísca e Raízes). Só com a Faísca, longe, o mago vence 27%; a arqueira, 34%. Área, cura, Mana e encanto não foram medidos.

1. Mago × mago, perto: 44–56% (49).
2. Mago × guerreiro com amuleto (iguais, Raro, nível 50): longe 40–65% (53), perto 15–40% (24), colado 0–15% (4).
3. Sem amuleto, o guerreiro perde 8 pontos ou mais (16).
4. Foco uma acima × guerreiro, perto: 50–75% (56–62). Mago × conjunto uma acima: 0–10% (0–2).
5. Nível 50 com foco duas acima × nível 500, longe: 30–60% (38–44).
6. Entre iguais, nenhum feitiço tira mais de 40% do PV na mediana, nem mata de PV cheio sem crítico.
7. Guerreiro com um encanto de dano × o gêmeo sem: 50–62%; com três: 55–72%.
8. Quatro Raros × doze Incomuns num corredor de dois: trocar um guerreiro por um mago rende 10 pontos. Mago Lendário × dez Únicos: 0–35%.
9. Cinco × cinco, um curandeiro no lugar de um guerreiro: 48–68%, até 14 rodadas. Foco Raro em ferida Lendária: até 2% do PV por lance.
10. Lançando sem parar, a Mana seca entre a rodada 5 e a 9.
11. Feitiço de 3 ações sob flecha: perdido em 30–60%; com guarda, 15 pontos a menos.
12. Retrochoque: 0,2–0,5% dos lances; 8–12% dos forçados; de 3º círculo com foco duas acima da guarda, derruba em 80% ou mais.

Os 29 de hoje continuam passando: ficha sem magia não muda.

## 6. Etapas

1. `tabelas_magia.py`, foco, amuleto, ficha. Metas 1 e 6.
2. `magia.py`: dano, Mana, canalizar, retrochoque, ordem `lancar`. Metas 2 a 5, 10 a 12.
3. Estados com prazo, calejo, campo, área, moral. Meta 8.
4. Cura e ferida funda. Meta 9.
5. Encanto e sintonia. Meta 7.
6. `escolhe`, paradas, janelas; capítulo 5 no `REGRAS.md`; `MUDANCAS.md`.

Ficam para outros módulos: aprender feitiço (mundo); o teste e a matéria de gravar (ofício); a RM e a Firmeza dos bichos.

## Escolhas do jogador

1. Escolas: a) as 13 do grimório; b) as 24 Essências; c) seis para começar.
2. Encanto: a) um degrau abaixo, uma vez por luta; b) inteiro, uma vez por dia; c) só passivo.
3. Mana: a) só volta com descanso; b) volta devagar na luta.
4. Retrochoque: a) pode matar; b) só derruba.
5. Área: a) fere amigo; b) não.
6. Cura: a) presa à ferida mais funda, com teto por dia; b) só o teto; c) livre.
