# MOTOR 7 — personalidade, habilidades e classes dentro do motor (Dia 396)

Pedido do jogador: a densidade do Satisfy em personalidade, habilidades, talentos e classes; narração melhor; mundo denso nos detalhes. As mudanças entram equilibradas, a critério do Mestre: o que mexe em número fica como PROPOSTA até o jogador aprovar.

## O que entrou

### 1. `tracos.py` — personalidade que pesa
- **Traços em lista** em todos os 93 NPCs: 62 saíram do texto da ficha (`migra`); 31 não tinham nenhum e ganharam 2 pelo dado (`completa`, anotado no envelope como oculto).
- **28 traços no catálogo**, cada um empurrando eixos (misericordia, rigor, risco, cautela, gasto, poupar, honra, segredo, guerra, paz, tradicao, novidade, rei, povo, fe, saber). `python3 tracos.py catalogo`.
- **Voto do conselho pelos traços:** `python3 tracos.py inclina A=misericordia,rei B=rigor fora=Tolvane` devolve a linha pronta para o `conselho.py`. O Mestre só marca os eixos de cada opção.
- **Opinião sobre o rei**, com motivo e prazo: `tracos.py opiniao NOME +10 "motivo" dias=60`. Entra no voto pelo eixo `rei` e na resistência social.
- **Resistência social:** `tracos.py resiste NOME EIXO` dá a CD com a conta aberta (nível, traços, teimosia, opinião).
- **Traço ganho ou perdido pelo que o NPC viveu:** `tracos.py traco NOME +VINGATIVO "motivo"`.
- **Voz:** `tracos.py voz NOME "como fala"`; seis vozes gravadas (Eliane, Nouliel, Herkald, Sira, Graur, Tilde).
- **Cartão de cena:** `tracos.py cena NOME NOME` (traços, opinião, voz, assinaturas e fraqueza da classe, desejo, medo, linha vermelha).

### 2. `habilidades.py` — a ficha de habilidades do Ferir
- `habilidades.json` semeado do estado_vivo: 16 habilidades, 9 talentos, 1 título, 7 perícias. Cargas: Visão do Tempo 2, Chuva de Brasas 7, Peça que lembra 1.
- **Grau pelo uso:** Iniciante 0 · Aprendiz 10 · Adepto 30 · Perito 80 · Mestre 200 · Grão-Mestre 500. `habilidades.py usa "Nome"` conta e avisa a subida.
- Todas começam no grau 1, porque o contador nasce hoje: nenhum bônus de graça.
- Títulos e talentos com efeito escrito: `habilidades.py titulo` e `talento`.

### 3. `classe.py` — a classe do NPC com o que ela faz
- Lê o Livro (`compendio/04_classes.md`) e grava na ficha as 3 assinaturas e a fraqueza: **33 de 93 NPCs** casaram com uma classe do Livro.
- `classe.py faltam` lista os 60 de fora (classes da casa ou nomes que o Livro não tem: Intendente, Podestà, Runista, Forjador de Guerra...). Falta decidir, um a um: corrigir o nome ou escrever a classe no Livro.

### 4. `ESTILO_NARRATIVO.md` — como se escreve a cena
Regras de ofício e uma conferência de saída. Ler todo turno, antes de narrar.

## PROPOSTAS que mexem em número: **APROVADAS PELO JOGADOR no Dia 400** (valem como regra da casa)
1. Cada grau de habilidade acima do 1 dá +1 no teste da própria habilidade.
2. A opinião entra no voto: opinião ÷ 20 na opção marcada com o eixo `rei`.
3. A CD social: 10 + nível ÷ 10 + traços contra o eixo + 3 se TEIMOSO − opinião ÷ 10; contra NPC importante o Mestre ainda soma o contexto.
4. O teto das inclinações pelos traços: de −5 a +5 por opção.

## O que falta (dizer ao jogador, não esconder)
- Conferir o tipo e o efeito das 16 habilidades semeadas contra o Livro; dar efeito ao título "Quem Bate Frio".
- Os 60 NPCs com classe fora do Livro.
- Desejo, medo, segredo e linha vermelha só em 9 dos 93: preencher pelo gerador quando cada um entrar em cena.
- Opinião: só três têm registro (Graur, Herkald, Nouliel). O resto começa em zero e ganha história jogando.
- O `teste_motor.py` ainda não cobre os três scripts novos.
- O `npc.py cena` antigo não mostra traços nem voz: usar `tracos.py cena`.

## Ideias para o mundo ficar mais denso (não construídas)
1. **Lugares com ficha:** cada lugar com cheiro, som, luz, um detalhe fixo e quem está sempre lá.
2. **Peças com história:** cada obra do rei com o registro de por onde passou e quem morreu com ela na mão.
3. **Boato com dono:** todo rumor tem quem o espalha e por quê; o rei pode seguir o fio.
4. **Calendário vivo:** festas, feiras e luas com efeito, para o tempo ter textura.
5. **Agenda própria dos conselheiros:** cada cadeira traz uma pauta sua à mesa, pelos traços e pela opinião.
6. **Recrutamento com ficha inteira:** quem chega pelo chamado vem com classe do Livro, traços, voz, desejo e uma razão para ter vindo.
