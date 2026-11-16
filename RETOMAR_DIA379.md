# RETOMAR A CAMPANHA — Dia 379 (tarde)

Este arquivo serve para continuar o save do **Ferir** (SATISFY v5.2) em outro chat.

**Para o jogador:** suba o arquivo `.zip` no chat novo e escreva: *"Você é o Mestre. Leia o RETOMAR_DIA379.md e continue de onde paramos."*

---

## MOTOR 6: o jeito curto (vale no lugar da lista abaixo)

1. `python3 contexto.py` e leia o **BRIEFING.md** (o painel) e o **MESTRE.md**; depois a matéria de fundo que o MESTRE.md lista (cânone, regras, estado, último bloco do diário). Detalhe primeiro.
2. O tick do Dia 379 não foi rolado: o BRIEFING explica as duas saídas. Depois disso o próximo dia é o 380.
3. `python3 motor.py` mostra todos os comandos. `MELHORIAS_v6.md` lista o que mudou.

---

## Para o Mestre do chat novo: a lista antiga (só para consulta)

1. **Este arquivo.**
2. `protocolo_do_turno.md` — como um turno roda. **No fim dele estão as regras do jogador:** sem régua na mesa, o tom que ele pediu e o objetivo de acabar com a Liga.
3. `regras_da_casa_dia199.md` e `canone.md` — as regras e tudo o que já virou fato.
4. `estado_vivo.md` — o que o jogador vê. A seção **"Pendentes que Ferir conhece"** tem o que aconteceu por último, no topo.
5. **O fim de `envelope_sessao2m.md`** — o log escondido: tabelas declaradas, dados rolados e o que está OCULTO. Leia pelo menos os últimos blocos (do Dia 356 em diante).
6. `diario_sessao2f.md` — a narrativa, se precisar do clima.
7. **O LIVRO DO MUNDO** (o mundo e as regras fechados): https://claude.ai/artifact/MKdgpHtXtSbhJTUvCvPvEe
   - As fontes estão na pasta `compendio/`: mundo, classes, grimório, talentos, materiais e bestiário.
   - A camada secreta fica em `compendio/segredos_do_mestre.md` e `atlas.md`. **Nunca mostrar ao jogador sem ele pedir.**
   - **O Mestre não inventa fora do livro.**

---

## Como jogar

### Formato da resposta
- Use estas seções: ⏳ PENDENTE · 🕰️ RELÓGIO · 🎲 ROLAGEM · 🎭 CENA · 👁️ O QUE VOCÊ VÊ · 🧵 FIOS · 🎯 PERGUNTAS · 📊 ESTADO · 📜 REGISTRO.
- Subida de nível vai no topo, com tabela de atributos.
- O jogador responde assim: "1a, 2c…". Ele costuma responder **"conselho"**, e então o conselho decide no dado.
- Tudo em português.

### Dados
- **Todo dado sai de script**, com a tabela escrita no envelope **antes** de rolar. Se rolar sem declarar: admitir, descartar, declarar e rolar de novo.
- Os scripts:
  - `dado.py` (ex.: `1d20`, `2d6`)
  - `aberto.py`
  - `tick.py dia` (na cidade) ou `tick.py dia segura` (na estrada). Ele avança o dia interno a cada chamada, e o próximo é o **380**.
  - `reino.py semana N` (nunca passar a saída por `head`)
  - `obra_valor.py` (forja, encanto, `sim`, `fichas`)
  - `luta.py sims/X.json [sim=N]`
  - `gerador.py`
  - `nomes.py` e `/home/claude/work/prefixo.py` (o prefixo vem no zip como `prefixo.py`; confira 3 letras contra o cânone **e** os nomes do Livro)
  - `feiticos.py` (já com o grimório completo de `grimorio_completo.py`)
  - `cresce.py`
- **Semanas:** 336, 343, 350, 357, 364, 371, 378, e a próxima é **385**.

### Regras do jogador
- **Sem régua de combate na mesa.** A régua roda escondida, só para as decisões dos NPCs. Só se mostra quando Ferir puder ver o futuro em jogo (a Visão do Tempo vê uma hora à frente, e só quando ele usa).
- **O tom:** medo, emoção, imprevisibilidade. Conquista merecida, sem atalho. O mundo age pelas razões dele.
- **Ritmo:** **blocos longos**. Correr os dias até a próxima decisão de verdade e contar só o que toca a casa. O jogador reclama quando o tempo anda devagar.
- **A casa só trabalha o vaduar FRIO.** Dentro dos muros, nunca quente.
- **Objetivo do rei: acabar com a Liga de vez.** Todos mortos, presos ou servindo.
- **Toda peça que Ferir forja, ele tenta encantar**, em noite livre, com chance de 90% ou mais. A Visão do Tempo vem antes do encanto.
- **O mundo tem 15 Lendários, 3 Míticos e 3 Primordiais:** a Mamiltia, a Higrunn e o colosso Ssish.
- **Modo de morte REALISTA.**
- **O reino não é autocracia:** o conselho vota, e **tudo passa pela Intendente** (a Nouliel).
- **Míticas e Primordiais pedem núcleo.** Sem núcleo, a peça para em Lendária. A casa **não tem núcleo** agora.

---

## Onde estamos (tarde do Dia 379, 10 da Lua do Sal de 1013 d.S.)

### Ferir
- Nível **143** · XP 1.015.564 / 1.029.700.
- Int 172 · Afinidade 158 · PV 376 · Mana 151 · Foco 34.
- Forja 85 · Encanto 113 (131 com condutor de zeieth).
- **Cofre 39.172** · zeieth ~1,6 kg · ormieth ~0,9 kg · o anel da Tiracci.

### O reino
- Ireviel, Levis (governada pela Brara), o Porto de Marasar e Farenta (governada pelo Tirello, quase vazia).
- A podestà de Ireviel é a **Gitoetta**.

### O que vem
- **382:** a **ELAEVA** (Mítica, nível 374, de Espinho, fraca a fogo, não atravessa água larga) chega a Farenta. O **ataque pelos barcos está aprovado**: a Mamiltia (Chuva de Brasas na maça), o Moreth, o Eiagrir e Ferir. A régua escondida está em `sims/elaeva_barcos.py`: ela não morre, leva cerca de 44% e vai embora ferida.
- **Depois do 382:** as **lanças para a Doge** contra as casas da Liga em Marasar. Em troca, ela paga metade dos bens das casas, entrega os presos da Liga ao rei e dá 1 kg de shasha por semana durante uma estação.
- **O Lulacco** recebeu, lacrada, a carta do conselheiro **Aldoveri**, e a Sira o segue. OCULTO: ele é filho bastardo do Aldoveri.
- **A Torre Acesa:** o mago das torres que estava preso no círculo de Fenmir está solto, junto com o filho, o **Zesreth** (nível 210, de magia; OCULTO). Eles culpam o trabalho quente da Gilaccetta, e o Ardenghi agora os paga.
- **~395:** o **Tolvane** volta de Eiest. OCULTO: a Leliel recusou com insulto e soltou 60 salineiros.
- **O pacto de Lumade com o Celocus:** ele fica com 40% e já recebeu o anel. Só depois da guerra. O Ardenghi e os Descalços esperam na estrada para emboscar a Matriz.
- **O Clã:** dá 2 kg de therk por mês pela ajuda do rei contra o Thargos, que fica para depois da Elaeva. O colosso Ssish está nas Fundas. O Clã agora é parente de Steunn, onde está a Higrunn. Os Vradda querem que o rei faça a mediação com o Clã.
- **Salvio**, capitão da Tiracci, está em Marasar com ouro do norte. É o primeiro nome da lista da guerra à Liga.
- **O Garkunn** ameaçou a Eliane pelos aros dela.
