# Etapa 3, projeto B: a gente que responde

Projetista B. Dono de `gente` (os nomeados e a memória), `caixa`, `missoes` e `noticias`. As medidas são de verdade: rodei o motor de hoje com um protótipo das regras deste projeto (os scripts estão em `medidas/`; os mundos ficaram no rascunho, fora do repositório). Onde escrevo "chute", não medi.

---

## 0. O juízo, em uma página (para o jogador)

1. **150 pessoas com nome vivem na região sem você.** Cada uma tem um papel (o ferreiro, a taverneira, o guarda, o mercador), uma rotina de 6 blocos que diz onde está e o que faz (sai de uma tabela, não grava nada), uma bolsa que anda com a prata do lugar, até 6 laços, e um querer por semana que vira ato: encomendar uma peça, mandar consertar, pedir uma missão, viajar, fazer amizade ou brigar, furtar (o ladino), falar de você, cobrar de você, agradecer você.
2. **Cada uma lembra de você: até 12 fatos com peso.** A opinião é a soma (de −10 a 10), em cima do que o lugar diz de você (a fama). O fato leve esfria em um mês; o grave (salvou a vida dele, alguém dele morreu com você) nunca. A mesa diz a palavra e o porquê: "Lino desconfia de você: não respondeu quando ele pediu".
3. **A notícia anda uma rota por dia** e vira boato depois do quarto salto. Você só lê o que chegou aonde está. A mesa traz o que se diz de você e dois fatos que não tocam você.
4. **A caixa só recebe de quem tem motivo no estado** (a peça gasta, a prateleira vazia, o roubo do covil, a memória ruim). Prazo de 2 a 3 dias; calado, vale o padrão, sempre com custo (o cliente vai ao outro ferreiro, e lembra). Cabem 7.
5. **A missão guarda a paga** (sai da bolsa de quem pede e fica guardada: a prata não some nem nasce). Qualquer um pode cumprir: o guarda de Ribeira pega a missão que você não pegou.
6. **O ferreiro tem cliente:** a gente que precisa de peça, a loja que repõe a prateleira e quem quer conserto. O cliente paga o valor inteiro (a loja, 60%), adianta 30% e o resto fica guardado até a entrega.
7. **Quem vai junto pede paga quando o perigo chega ao limite dele, e recusa o que passa dele.** Pela parte do despojo, como hoje, ele só vai ao que não o assusta, e só se não desgosta de você.
8. **O furto entra ligado:** a vítima que não viu dá pela falta, a vila fica de olho, quem é pego paga o triplo, e quem lembra do crime com −6 ou pior não negocia com você.

**O que medi** (um ano de região, 144 nomeados, 3 sementes): o atento recebe de 1,3 a 1,6 pedidos por semana e nunca mais de 3 abertos; o mudo deixa vencer todos, e a opinião média em Pedra Rasa fica 1,2 a 2 pontos abaixo da do atento. A encomenda rende ao ferreiro de começo de +0,15 a +1,2 de prata por dia; no melhor caso possível (fama 100 em toda a região, preço 20% abaixo, a demanda alta), +3,4. O furto, com a pena contada, rende de −0,8 a +0,3 por dia (a diária é 4). Um ano de mundo custa de 5 a 9 segundos com o gravador que só copia o que toca (proposta para o alicerce); com o gravador de hoje, 2,6 minutos (passa da meta).

**As quatro perguntas** estão na seção 10. **Os três riscos** estão na seção 11.

---

## 1. O que medi, e o que é chute

Os scripts (rodam de dentro de `motor10/`, com `PYTHONDONTWRITEBYTECODE=1`, e escrevem só no rascunho):

| Script | O que faz |
| --- | --- |
| `medidas/m0_base.py` | o custo de hoje: a vila de teste, 60 dias, sem nada da etapa 3 |
| `medidas/cow.py` | o gravador que só copia o que o evento toca (a proposta para o alicerce), com as mesmas recusas |
| `medidas/tab_b.py` | o rascunho da página `tabelas_gente.py` (todos os números deste projeto) |
| `medidas/proto_b.py` | o protótipo das regras: a gente, a memória, a notícia, a caixa, a missão, a encomenda, o furto; e um ARREMEDO da metade A (14 lugares novos e 24 rotas em volta de Pedra Rasa e Vau Seco, para a notícia andar e a gente morar) |
| `medidas/m2_ano.py` | um ano: a vila de teste do ferreiro, a região, 144 nomeados e o robô (atento ou mudo) |
| `medidas/m3_furto.py` | o robô ladino em Pedra Rasa, 30 vidas de 30 dias |
| `medidas/m4_cena.py` | a MESA de hoje com a região, as seções deste projeto, e o preço de quem vai junto |

O que o protótipo usa do motor de verdade: o relógio, o `ato.passa`, a virada de todos os módulos de hoje (o mercado de 16 lugares, a toca, a cripta, o Tição), a prata, as peças, a forja (`oficio.forjar`, com o dado de verdade), a compra na loja. O que é arremedo: o mapa e as rotas (da metade A), a viagem (o robô "leva" o recado esperando os blocos da rota, sem encontro), a freguesia que leva peças da prateleira (chute: 1 por semana numa vila), e a conta rápida da luta de quem não é o personagem (uma tabela pelo teto contra o grau, até a etapa 5 trazer a de verdade).

| Medida | Resultado | Como |
| --- | --- | --- |
| o dia de mundo, gravador de hoje | 18 ms (a vila sozinha, 17 pessoas); **423 a 446 ms** com a região e 144 nomeados (2,6 a 2,7 minutos por ano: **falha a meta 10**) | m0, m2 (30 e 60 dias) |
| o dia de mundo, gravador que só copia o que toca | **14 a 20 ms** (5 a 7 segundos por ano); o melhor caso de fama e de demanda, 26 ms (9 s) | m2, 364 dias, 3 sementes |
| o mesmo mundo com os dois gravadores | **igual, byte a byte** (gente, lugares, itens, relógio, turno, eventos), em 60 dias com forja, encomenda, missão e dado preso | m2 `dados=7`, com e sem `cow` |
| o custo da gente sozinha | 5,6 ms por dia (2 s por ano): 14 eventos a mais por dia no motor e 9 no armazém novo | m2 com e sem `sem_b` |
| o peso, no Dia 365 | a memória, o querer, os laços e a fama: 37 a 125 KB; as notícias ativas: 8 a 26 KB; a caixa: menos de 1 KB; as missões: 60 a 80 KB (sem podar as fechadas; podando, uns 10, chute); o registro de eventos da gente: 1,2 a 1,8 MB por ano | m2 |
| o registro de eventos do mundo inteiro | **10,5 a 11 MB por ano** na região de 16 lugares; quase tudo é do que já existe (a produção e o consumo de cada lugar, todo dia, e os blocos do personagem) | m2 |
| a caixa do atento | 67 a 83 itens no ano (1,3 a 1,6 por semana); no máximo 3 abertos; nenhum forçado | m2, 3 sementes |
| a caixa do mudo | 27 a 38 itens, todos vencidos | m2 |
| a opinião em Pedra Rasa (Dia 365) | atento +2,9 a +3,6; mudo +1,5 a +1,7. Na região: +0,9 a +1,6 contra +0,1 a +0,2 | m2 |
| quantos lembram de você | atento: 105 a 120 dos 144 (de 4 a 6 fatos em média, 12 no máximo); mudo: 8 a 18 | m2 |
| a renda do ferreiro de começo | jornal de 6 a 12 por dia (a regra de hoje: o Treinado ganha o salário de oficial); encomenda líquida de +0,15 a +1,2; levar recado, de 1,7 a 3,5 por dia de calendário (com a viagem de arremedo) | m2 |
| a encomenda no melhor caso | +3,2 a +3,4 por dia (fama 100 em todo lugar, preço × 0,8, demanda alta) | m2 |
| a prata do mundo | fecha em toda rodada (63.374 no começo e no fim) | m2 |
| a prata de Pedra Rasa | **de 2.000 para perto de zero em todas as rodadas**: o jornal do personagem leva de 2.700 a 3.400 no ano, e a bolsa da gente se enche do caixa do lugar | m2 |
| o furto, robô guloso (Iniciante, Agilidade 60) | **−0,76 por dia** (levou 1,13, multas 1,90); 6,05 por dia nos 5 primeiros dias; morre de fome nas 30 vidas (ninguém o serve, e o robô não sai da vila) | m3 |
| o furto, robô prudente (para quando é pego) | −0,06 por dia; a bolsa anda +0,12 por dia, contra +1,03 do diarista; 9 de 30 morrem | m3 |
| o furto, Treinado (Agilidade 70), prudente | +0,33 por dia; 9,6 nos 5 primeiros dias | m3 |
| o furto sem a memória (o 18.13 sozinho) | +1,22 por dia (11,6 nos 5 primeiros dias) | m3 |
| a MESA de hoje com a região | **14,6 KB** no Dia 61 (o mercado 4,0; o SÓ O MESTRE 3,5; o "Aqui" 2,0) | m4 |
| as seções deste projeto na MESA | 0,9 a 1,3 KB (8 pessoas, a caixa, o quadro, o que se diz, dois fatos) | m2, m4 |

---

## 2. As regras, com números

Todos os números estão no rascunho `medidas/tab_b.py`, que é a página `tabelas_gente.py` proposta.

### 2.1 A gente com nome

- **Quem:** 150 na região (a seção 3 do `PROJETO.md`). O gerador põe por tipo de lugar a lista de papéis de `POVOAR`: aldeia 4 (alcaide, taverneiro, caçador, lavrador), vila 9 (mais ferreiro, mercador, guarda, curandeiro, lenhador), cidade 15 (mais mestre ferreiro, encantador, capitão, sacerdote, caravaneiro, ladino), capital 30. Com os 16 de Pedra Rasa, deu 144 no arremedo.
- **O papel** (`PAPEIS`): a rotina, o grau de ofício, o molde, o nível, a mão, as peças do ofício (o que ele usa e o que vai encomendar quando quebrar), o desgaste delas por semana e o ponto onde trabalha. Os da vila de teste ganham o papel que já têm (Bento ferreiro, Dalva taverneira, Tomé guarda, Quim ladino, Durva ferreira de passagem, Anselmo mago, Joana bruxa...).
- **A bolsa:** cada grau quer ter uma bolsa (`BOLSA`: diarista 15, aprendiz 30, oficial 60, mestre 150; o mercador 2,5 vezes, o nobre 10, o capitão 2). A vila de teste já nasce perto disso (Ivo 12, Rute 25, Tomé 40, Bento 60, Lino 150).
- **A semana de cada um** (no dia da semana dele: um sétimo da gente por dia, para o custo não pesar num dia só): a bolsa anda para o alvo. Abaixo dele, o lugar paga a sobra da semana (a jornada menos o viver: diarista 7, aprendiz 21, oficial 63, mestre 119); acima, o que passa volta ao caixa do lugar. **A prata só muda de mão.** Quem junta para uma encomenda tem o alvo mais o preço da peça. Depois, a peça do ofício gasta (o guarda 0,3 ponto por semana, o caçador 0,5) e o querer sai.
- **O nomeado novo sai do povo em número de A:** quem morre ou vai embora é trocado, na virada da estação, por um do povo do lugar (o povo perde 1; nasce a pessoa com o papel que faltou e um nome de `nomes`). A etapa 7 põe os dela pela mesma porta (seção 3.6).

### 2.2 A rotina de 6 blocos

Uma tabela (`ROTINAS`): para cada bloco, o ponto e o que faz. Não grava nada: o lugar da pessoa segue só na ficha (`lugar`); o ponto sai da tabela e do papel.

| Rotina | madrugada | alvorada | manhã | tarde | entardecer | noite |
| --- | --- | --- | --- | --- | --- | --- |
| ofício | casa, dorme | casa, dorme | o ponto do ofício, trabalha | idem | taverna, conversa | casa, dorme |
| campo | casa | ermo, trabalha | ermo | praça, vende | taverna | casa |
| taverna | casa | casa | taverna, trabalha | taverna | taverna | taverna |
| guarda | casa | casa | praça, vigia | praça, vigia | taverna | praça, vigia |
| santuário | santuário | santuário, reza | santuário | praça | santuário | santuário |
| passagem | pousada | pousada | praça | mercado | taverna | pousada |
| nobre | casa | casa | casa, recebe | praça, passeia | casa, janta | casa |
| ladino | casa | casa | praça | mercado | taverna | praça |

Para que serve: a mesa diz o que cada um faz agora; o furto só se tenta em ponto público, contra quem está lá; quem estava no mesmo ponto é testemunha; o guarda que vigia aquele ponto naquele bloco pesa no furto; o laço nasce de quem se encontra na taverna. Quem viaja está na estrada (a viagem de A).

### 2.3 O querer da semana

Um por pessoa, por semana. Cada querer só entra no sorteio (o dado do mundo, `estado.sorte`) se o motivo dele está no estado; "nada" sempre pode. O querer vira ato com efeito no mesmo dia, num evento do gravador.

| Querer | O motivo (tem de estar no estado) | Peso | O ato |
| --- | --- | --- | --- |
| encomendar | a peça do ofício falta ou quebrou | 6 | se tem a prata, escolhe o ferreiro (2.10); se não, junta (o alvo da bolsa sobe) |
| melhorar | a bolsa tem 2 vezes o preço da arma uma categoria acima | 1 | encomenda essa |
| consertar | a peça do ofício abaixo de 60% | 8 | escolhe o ferreiro e paga o conserto (2% do preço por ponto) |
| missão | o alcaide: o covil roubou a vila, o bicho do ermo saiu; o mercador: a carga a levar, a rota de perigo | 4 (alcaide × 3, mercador × 2) | a missão nasce, com a paga guardada (2.9) |
| viajar | um laço noutro lugar; o mercador, o caravaneiro | 1 (mercador × 3) | a viagem de A (a pessoa sai e volta) |
| laço | alguém na taverna com ele | 2 | o laço sobe 2 (70%) ou cai 2; ao passar de +6 ou de −5, notícia ("estão sempre juntos", "brigaram na taverna") |
| falar de você | a opinião dele sobre você, 4 ou mais, para cima ou para baixo | 3 | notícia no lugar: até 3 ali guardam "ouviu falar bem (mal) de você" |
| cobrar | um fato dele sobre você de −5 ou pior, e nenhuma cobrança aberta dele | 5 | a caixa (2.8) |
| agradecer | um fato de +6 ou mais, ainda não agradecido | 3 | a caixa: uma oferta (até um quinto da bolsa dele) |
| furtar | o papel ladino, e a bolsa abaixo do alvo | 4 | o furto de pessoa a pessoa (2.12) |
| nada | sempre | 8 | |

Medido (um ano, 144 nomeados): cerca de 6.900 quereres; 4.500 "nada"; 1.100 laços (com 90 a 120 notícias); 350 consertos; 90 encomendas; 630 missões pedidas (240 a 260 nasceram: o resto não tinha motivo ou prata); 300 viagens.

### 2.4 Os laços

Até 6 por pessoa, `{quem: valor}` de −10 a 10, na ficha de quem sente (cada lado o seu). O gerador põe 1 ou 2 no lugar e, em um de cada cinco, um parente num lugar vizinho (+7). A etapa 7 põe as famílias da história. Para que servem: quem ouve primeiro a notícia de alguém são os de laço com ele; o cliente prefere o ferreiro amigo (peso × (1 + laço ÷ 3)); a vítima do furto pega fica com −6 no laço com o ladrão; a morte de alguém vira memória grave nos de laço (etapa 6: a família que cobra).

### 2.5 A memória e a opinião

- **Até 12 fatos**, na ficha de quem lembra: `[dia, tipo, peso, de quem, canal, texto]`. O tipo é de uma lista fechada (`FATOS`), com o peso, o eixo da fama que a notícia dele mexe, os pontos de fama, o alcance da notícia e a frase do porquê.

| Fato | Peso | Fato | Peso |
| --- | --- | --- | --- |
| fez a peça que pediu, no prazo | +3 | não entregou a peça que prometeu | −4 |
| fez a peça, com atraso | +1 | recusou o pedido | −1 |
| cumpriu a missão que ele pediu | +5 | não respondeu (calou) | −2 |
| salvou a vida dele | +8 | falhou na missão que pegou | −4 |
| pagou o que devia | +1 | ele se feriu indo com você | −2 |
| deu-lhe alguma coisa | +2 | alguém dele morreu indo com você | −8 |
| ouviu falar de você | o peso da notícia | roubou dele (viu) | −6 |
| | | viu você roubar | −3 |
| | | desconfia que você o roubou | −2 |

- **O canal:** quem viu guarda o peso inteiro; quem ouviu a notícia, a metade; do boato, um quarto (sempre pelo menos 1).
- **Esfria:** o fato de peso até 3 perde 1 a cada 28 dias; de 4 a 7, a cada 56; de 8 para cima, nunca. A conta sai na hora de ler: o esfriar não grava evento nenhum.
- **Cheia, esquece:** o 13º fato faz sair o de menor peso de hoje (o mais velho, no empate). A regra mora no gravador (o verbo `junta`), não em quem chama.
- **A opinião** é a soma dos pesos de hoje, mais o **tom do lugar** (a fama: +1 a cada 25 pontos de feito e de ofício somados, −1 a cada 10 de crime; de −3 a +2), de −10 a 10. Palavras: até −7 "odeia você"; −6 a −4 "não gosta"; −3 a −1 "desconfia"; 0 "não tem opinião"; +1 a +3 "simpatiza"; +4 a +6 "gosta"; +7 a +10 "confia em você".
- **O que a opinião faz** (tudo pela conta, sem dado): −6 ou pior, quem atende (a loja, a taverna, a forja, o alcaide que dá serviço) não negocia com você; −4 ou pior, não lhe pede nada e não vai junto; +2 ou mais, a missão dele vem à sua caixa (e não só ao quadro); +4, quem vai junto pede a metade; +7, vai pela parte, de graça.
- **De quem se lembra:** nesta etapa, só do personagem (o campo "de quem" já aceita qualquer pessoa: os rivais da etapa 5 e o herdeiro da 6 entram sem mudar a forma). O que a gente sente uma pela outra são os laços.

### 2.6 A fama

Na ficha de quem é falado: `fama[lugar][eixo] = [pontos, dia]`, três eixos (ofício, feito, crime), de 0 a 100. **Sobe quando a notícia chega ao lugar** (a do boato, pela metade) e **esfria 1 ponto a cada 28 dias** (a conta sai na hora de ler). **Quem serve na bancada fica conhecido:** a cada 10 blocos de bancada no lugar (obra, conserto, jornal), +1 de ofício ali. Medido: o ferreiro que só serve o jornal chega a 67 a 74 de ofício em Pedra Rasa no Dia 365; o que também entrega, a 86 a 93. Para que serve: o tom da opinião de todo o lugar (2.5), a escolha do cliente (2.10), a missão dirigida (feito de 10 por grau), e a vigia contra quem tem fama de crime (2.12). O ferreiro de nome que já existe tem a fama de ofício do grau dele (aprendiz 5, oficial 15, mestre 35).

### 2.7 A notícia

- **Nasce no mesmo evento do que a causou** (o efeito `['noticia', 'nasce', ...]`): a encomenda entregue, a missão cumprida ou falhada, o furto, a morte, o roubo do covil, o laço que passou do limiar, quem fala de você. A frase sai dos efeitos.
- **Anda uma rota por dia:** na virada, cada notícia que chegou ontem a um lugar, e ainda não passou do alcance dela, chega hoje aos vizinhos pelas rotas abertas de A. O alcance vem do tipo (o laço e a suspeita, 1 salto; o crime e a missão, 2; a peça Rara, 3; o feito grande e o dragão, 5 ou mais).
- **Depois do quarto salto, vira boato:** a frase perde o nome de quem fez ("dizem que um ferreiro de longe...") e pesa um quarto.
- **Quem guarda:** em cada lugar aonde chega a notícia sobre você, até 3 nomeados guardam um fato "ouviu" (primeiro os de laço com quem está nela, depois o do mesmo ofício, depois o taverneiro).
- **Sai do arquivo** 28 dias depois de parar de andar (o registro de eventos guarda tudo). Medido: de 0,7 a 1,2 notícias por dia na região, de 8 a 45 ativas.
- **Você só lê o que chegou aonde está.** A janela do mundo (a peça Única, a primeira limpeza) é da etapa 5: ela avisa todos na hora, por cima disto.

### 2.8 A caixa

`{de, pede, prazo, opções, padrão, custo, motivo}`. **Só escreve quem tem motivo no estado:** o motivo aponta o que existe (a peça gasta, a prateleira abaixo do alvo, a missão, o fato da memória); o gravador recusa o item sem ele. Os moldes:

| Molde | Pede | Prazo | Opções | Calado (o padrão, com o custo) |
| --- | --- | --- | --- | --- |
| encomenda | a peça, o preço, o sinal, a entrega | 2 dias | aceitar · pedir 20% a mais (aceita se a opinião dele é +2) · recusar | recusa: ele vai a outro ferreiro, lembra "calou" (−2), a fama de ofício ali cai 1 |
| loja | a peça para a prateleira, a 60% do valor | 4 dias | aceitar · recusar | o mercador pede a outro |
| conserto | a peça dele, os pontos, a paga | 2 dias | aceitar · recusar | ele leva a outro, e lembra |
| missão (dirigida) | o que fazer, a paga, a caução | 2 dias | pegar · recusar | vai ao quadro, e ele lembra |
| cobrança | a prata, pelo fato que ele lembra | 3 dias | pagar · negar | ele se queixa ao alcaide: fama de crime +5, notícia |
| oferta | a prata ou o favor | 3 dias | aceitar · recusar | a oferta se perde, e ele se sente desfeitado |

Cabem 7: o oitavo força o mais velho (vale o padrão dele). O item que vence em um dia vira pergunta do turno sozinho, com os códigos ligados a `caixa.py responde`: o `fecha` recusa sem isso (a seção 6 do `PROJETO.md`).
Medido: o atento recebe 1,3 a 1,6 por semana (encomendas, a loja, consertos, recados), nunca mais de 3 abertos; o mudo, 0,5 a 0,7 por semana (só pede quem tem opinião +2 ou fama, e o mudo tem menos de tudo). **A caixa não enche nem seca:** fica em 1 a 3 por semana para quem trabalha. O melhor caso de fama passa de 4 por semana.

### 2.9 A missão

`{de, onde, tipo, grau, alvo, paga, caução, prazo, quem, estado, guarda}`.
- **Os tipos** (lista fechada): levar (carga ou recado até um lugar), escoltar (alguém por uma rota), caçar (o bicho que saiu do ermo), limpar (a toca, o covil), buscar (matéria de um ermo), encomenda (a obra do ofício, 2.10). A etapa 6 põe a missão contra a frente (o campo `frente`).
- **A paga pelo grau do perigo** (`PAGA_GRAU`: F 10, E 25, D 60, C 200, B 800, A 3.000, S 10.000); levar paga 5 mais 3 por bloco de caminho, ida e volta (o diarista ganha 2 por bloco). **A caução é 20%.** O prazo, 14 dias.
- **A paga fica guardada** desde que a missão nasce: sai da bolsa de quem pede (ou do caixa do lugar, se é o alcaide pelo lugar) e vai para o campo `guarda` da missão, que entra na soma da prata do mundo. Sem a prata, a missão não nasce. Quem pega paga a caução, que também fica guardada.
- **Cumprida:** a paga e a caução vão a quem cumpriu; a memória de quem pediu (+5) e a notícia (fama de feito pelo grau). **Falhada ou largada:** tudo volta a quem pediu (a caução de quem falhou fica com ele) e ele lembra (−4). **Vencida sem ninguém:** a paga volta; o motivo segue no estado, e o querer pode voltar na semana seguinte.
- **Cumprir é mudar o estado de verdade:** a missão de caçar fecha quando a contagem do ermo caiu pelo que ela pede, por mão de quem a pegou (o abate do evento `despojo`); a de levar, quando a carga chegou ao lugar pela viagem de A; a de limpar, quando o covil caiu. `missao.py cumpre` confere e recusa o que não aconteceu.
- **Qualquer um pode cumprir:** o guarda, o caçador, o capitão e o caravaneiro de lá ou de perto, com o teto para o grau, pegam a missão do quadro (o dado do mundo), e cumprem ou falham em 2 a 5 dias pela conta rápida (até a etapa 5, uma tabela: o teto acima do grau, 90%; igual, 65%; abaixo, 25%, e morre em 15% das falhas). Voltam com as peças gastas (−3), e isso dá serviço ao ferreiro. Medido: 190 a 230 missões cumpridas ou falhadas por nomeados no ano; nenhuma morte nas 3 sementes (o nomeado quase nunca pega o que passa do teto).

### 2.10 A encomenda ao ofício (o cliente do ferreiro e do encantador)

- **Quem pede:** o nomeado com o motivo (a peça do ofício que falta ou quebrou; melhorar, se é rico), **e a loja**, quando a freguesia de A leva peças da prateleira e ela fica abaixo do alvo (o mercador pede a peça a 60% do valor, uma por semana).
- **A escolha do ferreiro** (o dado do mundo, com peso): os ferreiros de nome do lugar e dos vizinhos a até 4 blocos, e o personagem, desde que a forja do lugar sirva à categoria (a Rara pede a forja de cidade; a Épica, a grande forja). Peso: (1 + fama de ofício ÷ 10) × (1 + opinião ÷ 3, ou laço ÷ 3) ÷ o fator de preço² (o personagem diz o preço dele: `gente.py preco 0.8`), metade se é noutro lugar. Opinião −4 ou pior: não pede.
- **O preço é o valor da peça** (8.8 do `REGRAS.md`), inteiro; sob medida, o mesmo (o ajuste é serviço à parte). O sinal, 30%, vai ao ferreiro na hora; o resto fica guardado na missão. A entrega: a peça muda de dono (`missao.py entrega ID ITEM`), vai ao uso do cliente, e a velha vai ao fogo (sai do Livro; a matéria dela volta ao estoque do lugar). **O atraso** tira 10% por dia da paga guardada (até a metade), que volta ao cliente. **Uma semana depois do prazo sem a peça:** o resto volta ao cliente, e o ferreiro devolve o sinal em dobro (o que tiver; o que faltar vira dívida e cobrança).
- **O conserto para o cliente:** a mesma conta de hoje (2% do preço por ponto ao ferreiro, 5 pontos por bloco, 1 de matéria a cada 10 pontos), com a peça do cliente na bancada do ferreiro. É um comando novo (`oficio.py consertar ITEM para=DONO`): hoje só se conserta a peça sua.
- **O ajudante:** o aprendiz de nome serve de ajudante na obra (o preparo +2 que hoje é marca do Mestre) pelo salário dele por bloco, se a opinião dele não é −4 ou pior (`gente.py chama zeca ajudante`).
- **O encantador:** o cliente rico (o capitão, o nobre, o caravaneiro) com peça Incomum ou melhor pede um feitiço gravado. O preço: o valor da essência em dobro, mais um terço do valor da peça (o encanto vale um degrau abaixo dela). A peça segue do cliente: ele vai até a mesa de runas (a viagem de A) e a gravação usa o `encanto.py gravar ITEM FEITICO para=DONO` que já existe. Quem ensina o encanto é o encantador de nome da cidade (o estudo pela lição: o salário do grau dele por bloco, só na jornada dele). **Não medi:** é pouca gente rica e o personagem começa Leigo no encanto (chute: de 5 a 10 pedidos por ano na região).
- **Medido:** o ferreiro de começo recebe de 2 a 3 encomendas de gente, de 19 a 28 pedidos da loja e 12 consertos no ano; a encomenda líquida (a paga menos a matéria) dá de +0,15 a +1,2 por dia. Os ferreiros de nome fazem de 58 a 88 encomendas e de 230 a 370 peças para a loja. No melhor caso (fama 100 em todo lugar, preço × 0,8, a demanda alta), o personagem pega 44 a 49 encomendas e 91 pedidos da loja: +3,2 a +3,4 por dia. **A encomenda não é mina:** o que ela paga é a prata que a gente juntou, e a gente só junta quando precisa.

### 2.11 Quem vai junto

O teto de cada um é o grau de perigo que ele enfrenta sem medo: (a mão na arma em uso ÷ 2 + 3 × a categoria da arma + a categoria da armadura) ÷ 2, arredondado para baixo (0 = F, 1 = E, 2 = D). Na vila de teste: Ivo e Quim F; Brasco E; Rute e Tomé D; Durva e Ilvena C. O perigo da saída: o grau do bicho procurado (ou do pior do ermo, se "o que aparecer"), da rota (A) ou da masmorra.

| O perigo menos o teto dele | O que ele pede |
| --- | --- |
| −1 ou menos | vai pela parte do despojo (como hoje), se a opinião não é negativa; senão, a diária |
| 0 (o limite dele) | a diária (a jornada do grau: Rute 6, Tomé 12) e a parte |
| +1 | três diárias e a parte, e só com opinião +2 ou mais (ou se ele precisa de prata: a bolsa abaixo da metade do alvo) |
| +2 ou mais | recusa |

Opinião −4 ou pior: recusa tudo. +4: metade. +7: vai pela parte, de graça. O querer dele pesa: quem está viajando ou juntando para uma peça não sai por mais de um dia. A paga sai antes, no comando (`caca.py sair ... com=rute paga=6`): sem ela, o comando recusa e diz o preço e o porquê. Depois, a memória (ferido indo com você, −2; alguém dele morreu, −8, nos de laço). Medido (a conta, `m4`): contra o lobo, Rute pede 6 e a parte, Tomé 12 e a parte; contra a cripta, os dois recusam com opinião 0 (aceitam com +2, por 18 e 36); Durva e Ilvena vão ao lobo e à toca pela parte. **Muda a cripta de hoje:** com Tomé e Rute de opinião +2, a descida custa 54 de prata antes de entrar (o prudente tirava 6 por dia nos 5 primeiros dias, FA5): a cripta passa a pedir amigo ou prata.

### 2.12 O furto (o 18.13, ligado)

A regra do 18.13 fica (de dia, na vila, contra alguém com nome, uma tentativa por alvo por dia; 2d20 + Agilidade ÷ 10 + a mão + o dom contra 20 + Percepção ÷ 10 da vítima, +4 se é guarda ou mercador; leva 1d6 × (1 + metade do grau); pego por 5 ou mais, paga o triplo ao caixa do lugar, ou 3 dias preso). O que entra agora:
- **Só no ponto público onde a vítima está** (a rotina), e **+4 se um guarda vigia aquele ponto** naquele bloco.
- **A vila fica de olho:** cada falta descoberta põe +2 em todo furto ali por 28 dias (até +8); e a fama de crime de quem furta soma +1 a cada 10.
- **Quem não viu dá pela falta** na virada (60%, rolagem oculta): nasce a notícia "sumiu prata da bolsa de Dalva", a vigia sobe, e a vítima desconfia de quem estava no ponto (a chance é 1 ÷ quantos estavam, mais a fama de crime): "desconfia que você o roubou", −2, e +3 de fama de crime.
- **Pego:** a vítima lembra "roubou dele" (−6, e o laço do ladrão de nome cai 6), quem estava no ponto "viu você roubar" (−3), a notícia anda 2 saltos, +10 de fama de crime. Preso: `marca.preso` (como a saída: os atos da vila são recusados até o fim).
- **E o resto da vida:** quem lembra do crime com −6 ou pior não negocia. Roubar a taverneira e o mercador fecha a comida da vila.
- **O ladino de nome também furta** (o querer furtar, pela mesma conta e o dado do mundo): o mundo rouba sem você.
- **Medido** (30 vidas de 30 dias): o guloso tira 6 por dia nos 5 primeiros dias e depois perde (−0,76 por dia no mês); o prudente, que para quando é pego, fica com −0,06; o Treinado prudente, +0,33. A meta do 18.13 ("rende, com a pena contada, menos que a diária") passa com folga. O robô, que nunca sai da vila, morre de fome em 9 a 30 das 30 vidas: com a viagem de A, quem rouba a vila tem de ir embora.

### 2.13 O mundo sem você

O banco roda o ano com o personagem parado: a gente encomenda (58 a 88 peças ao ano aos ferreiros de nome), conserta (300 a 360), pede e cumpre missões (190 a 230), viaja (300), faz amizade e briga (90 a 120 notícias), o Quim furta, a loja repõe a prateleira, o covil rouba e a vila fala disso, as notícias andam. Nada disso precisa do personagem; o que o toca chega à caixa dele.

---

## 3. O estado

### 3.1 Os campos novos da pessoa (todos com padrão; o save antigo abre igual)

| Campo | Forma | Padrão (save antigo) |
| --- | --- | --- |
| `papel` | um nome de `PAPEIS` | sem o campo: não é gente da região (não tem rotina, nem querer, nem bolsa que anda: como hoje) |
| `memoria` | lista de até 12 `[dia, tipo, peso, de quem, canal, texto]` | `[]` |
| `querer` | `{t, desde, peca, preco}` ou nada | nada |
| `lacos` | `{id: valor}`, até 6 | `{}` |
| `fama` | `{lugar: {eixo: [pontos, dia]}}` | `{}` |
| `marca.preso` | `{ate: bloco}` | nada |
| `marca.retribui` | os fatos já agradecidos | nada |
| `marca.preco` | o fator de preço do ferreiro (o personagem) | 1 |

No lugar: `vigia` (os dias das faltas descobertas; padrão, nada). No item: nada novo (a peça do cliente que o ferreiro conserta segue do cliente).

### 3.2 Os arquivos novos do save

`noticias.json` (`{seq, ativas: {id: {de, s, t, x, e, f, a, p, d, em: {lugar: [dia, saltos]}}}}`), `caixa.json` (`{seq, abertos: {id: {...}}}`), `missoes.json` (`{seq, itens: {id: {...}}}`). O arquivo que falta abre vazio. Entram em `estado.ARQS`, e o gravador os copia por entrada, não inteiros (3.4).

### 3.3 Os eventos e os efeitos novos

| Efeito | O que faz |
| --- | --- |
| `['pessoa', id, 'papel', 'poe', papel]` | só em evento `gera` ou `mestre` |
| `['pessoa', id, 'memoria', 'junta', fato]` · `'esquece', i` · `'retribui', [dia, tipo]` | o 13º faz esquecer o de menor peso, no próprio verbo |
| `['pessoa', id, 'querer', 'poe', reg ou None]` | |
| `['laco', a, b, 'soma'\|'poe', n]` | na ficha de a; de −10 a 10; até 6 |
| `['fama', quem, lugar, eixo, 'soma', n]` | soma à fama de hoje (já esfriada) e grava o dia; de 0 a 100 |
| `['noticia', 'nasce', reg]` · `[..., id, 'chega', lugar, saltos]` · `[..., id, 'some']` | |
| `['caixa', 'abre', reg]` · `[..., id, 'fecha', 'feito'\|'vencido'\|'forcado']` | abre recusa sem motivo, com 7 abertos (o chamador força o mais velho antes) |
| `['missao', 'abre', reg]` · `[..., id, campo, 'poe', v]` · `[..., id, 'guarda', 'soma', n]` · `[..., id, 'fecha', desfecho]` · `[..., id, 'some']` | a guarda é prata: só muda de mão com a bolsa ou o caixa no mesmo evento |

Os tipos de evento novos (`tabelas_mundo.EVENTOS`): `gente` (a semana: a bolsa, o desgaste, o querer), `noticia` (o dia das notícias), `caixa`, `missao`, `encomenda`, `furto`, `companhia`. `gente` e `noticia` entram em `MUNDO_SOZINHO` (não são fato do turno, a não ser que toquem o personagem ou alguém morra).

### 3.4 Os invariantes (`estado.valida`)

- **A prata do mundo é gente + lugares + a guarda das missões**, e fecha (o `prata_do_mundo` do mercado e do ofício passa a somar a guarda).
- A memória: no máximo 12; o tipo da lista; o peso de −10 a 10; "de quem" é uma pessoa que existe (viva ou morta). Os laços: pessoas que existem, de −10 a 10, até 6. A fama: de 0 a 100, lugar que existe. O papel: da tabela.
- A notícia: os lugares existem; os saltos não passam do alcance; nenhuma chega a um lugar a k saltos antes do dia k.
- A caixa: no máximo 7; quem pede está vivo; o motivo existe; o padrão é uma das opções; o prazo depois da abertura.
- A missão: quem pede existe; a guarda de zero para cima; quem pegou está vivo, ou a missão fechou; a encomenda pega aponta uma peça que existe quando é entregue.
- O preso não age (o `presente` recusa, como recusa quem está fora).

### 3.5 Quanto pesa

Medido no Dia 365 (3.6 para o save do jogador): os campos da gente, de 37 a 125 KB (a memória é quase tudo: 4 a 9 fatos em média; com os 12 de todos, perto de 175 KB, conta); as notícias, de 8 a 26 KB; a caixa, menos de 1 KB; as missões, de 60 a 80 KB sem podar (com `missao some` 28 dias depois de fechar, uns 10 KB: chute). **Total da gente que responde: de 150 a 230 KB no estado, e de 1,2 a 1,8 MB por ano no registro de eventos.** O registro do mundo inteiro passa de 10 MB por ano já hoje, com 16 mercados (3.7).

### 3.6 O save do jogador e a porta da etapa 7

- **No `ensaio/`:** o comando da região (de A, `vila_teste.py regiao PASTA`) chama a parte de B, `gente.povoa_regiao(E)`, que só acrescenta: o papel dos 16 de Pedra Rasa (uma tabela fixa: Bento ferreiro, Quim ladino...), os nomeados dos lugares novos de A (do povo deles), os laços, e nada mais (a memória vazia, a fama zero; a bolsa de cada um fica como está e anda dali). Recusa rodar duas vezes. O Maro começa sem fama e ninguém lembra dele: a vila de teste não guardou o que ele fez até hoje (dá para pôr à mão: `gente.py lembra tome cumpriu "a cripta"`).
- **A porta da etapa 7:** `gente.povoa(E, lugar, pessoas=None)`. A história entrega uma lista de pessoas já prontas (o nome, o papel, a casa e os laços de família, as peças que já estão no Livro com a história delas, e fatos de memória sobre quem ela quiser, inclusive mortos), e o gerador só completa os papéis que faltam de `POVOAR`. O "de quem" da memória já aceita o morto: a etapa 6 faz o herdeiro herdar a metade do que lembram do pai.

### 3.7 O custo por dia, e o que o alicerce precisa fazer

- **A gente custa 5,6 ms por dia de mundo** (2 segundos por ano): 14 eventos a mais por dia no gravador e 9 nos arquivos novos.
- **O gravador de hoje é o gargalo, e não a gente:** ele copia o estado inteiro a cada evento. Com 144 nomeados e 16 mercados, são 423 a 446 ms por dia (2,6 minutos por ano: a meta 10 falha antes de qualquer regra nova). O `medidas/cow.py` mostra o conserto: a cópia de ensaio rasa, que só copia a pessoa, o lugar, o item ou a entrada que o efeito nomeia (o que mexe em muita coisa, como a morte, copia o arquivo inteiro, como hoje). **Medido: de 14 a 20 ms por dia, e o mesmo mundo, byte a byte, em 60 dias com forja, encomenda e missão.** É a primeira coisa do alicerce.
- **O registro de eventos:** os 16 mercados escrevem dois eventos por dia cada um, com todos os bens. Proposta para o alicerce e para A: o mundo sozinho de um dia num evento só por módulo. (Não medi quanto cai.)

---

## 4. Os comandos e a mesa

### 4.1 Os comandos

| Comando | O que faz |
| --- | --- |
| `gente.py aqui` | quem está no lugar: o que faz agora, o que quer (o que se sabe), o que lembra de você, com os porquês |
| `gente.py ver ID` | a ficha da pessoa: o papel, a rotina do dia, o querer, os laços que se sabem, a memória sobre você (a palavra e os porquês) |
| `gente.py preco F` | o fator de preço do ferreiro (de 0,6 a 1,5) |
| `gente.py chama ID [ajudante\|junto]` | o que ele pede para ajudar na bancada ou ir junto, e por quê (só olha) |
| `gente.py lembra ID TIPO "o que houve"` | o Mestre grava um fato de cena |
| `gente.py mestre` | SÓ O MESTRE: os números da opinião, os quereres escondidos, quem desconfia de quem |
| `caixa.py ver` · `caixa.py responde ID LETRA [preco=N]` | a caixa por prazo; responder (o turno liga a pergunta a este comando) |
| `missao.py ver` · `pega ID` · `cumpre ID` · `entrega ID ITEM` · `larga ID` | o quadro do lugar; pegar (paga a caução); dar por cumprida (confere o estado); entregar a encomenda; largar (perde a caução) |
| `missao.py pede TIPO ...` | o Mestre (ou a cena) põe uma missão, com a paga guardada de quem pede |
| `noticias.py` · `noticias.py mestre` | o que chegou aqui; SÓ O MESTRE: tudo, e aonde chegou |
| `manha.py furtar ALVO` | o furto, ligado (o dado do jogador, declarado e rolado uma vez) |
| `caca.py sair ... com=ID paga=N` (e `masmorra.py descer`, e a viagem de A) | quem vai junto: sem a paga que ele pede, recusa com o preço |
| `oficio.py consertar ITEM para=DONO` | o conserto da peça do cliente |

### 4.2 A MESA (8 KB): o que entra e o que sai

A MESA de hoje com a região mediu 14,6 KB. As seções de B, no protótipo, mediram de 0,9 a 1,3 KB. Proposta de orçamento (o alicerce mede, e o banco reprova o que passar):

| Seção | KB | O que muda |
| --- | --- | --- |
| a cabeça, Você | 0,8 | como hoje |
| Aqui (o lugar, o que fazer e quanto custa) | 1,0 | sai a lista de 16 nomes com descrição (vai para "Quem está aqui") |
| **Quem está aqui** (B) | 1,0 | até 8 (os que estão em ponto público agora, depois os de opinião mais forte): o nome, o papel, o que faz, o que quer, o que lembra de você; "e mais N (`gente.py aqui`)" |
| **A caixa** (B) | 0,8 | por prazo, uma linha cada, com as opções e o padrão |
| **O quadro, o que se diz de você, dois fatos que não tocam você** (B) | 0,7 | até 3 missões, 3 notícias sobre você, 2 de fora (a pousada que conta do Tição entra aqui) |
| O mercado | 1,0 | sai a tabela inteira (vai para `mercado.py ver`): fica a prata da loja, o que você carrega, o que mudou mais de 20% na semana, e a prateleira contada por categoria (hoje, 4,0) |
| A oficina | 0,5 | hoje, 1,1 |
| A caça, a coleta e os bichos | 0,6 | a lista dos bichos vai para `caca.py ver` (hoje, 1,7) |
| A magia e a botica | 0,4 | uma linha por quem serve (hoje, 1,2) |
| Perguntas abertas | 0,3 | |
| SÓ O MESTRE | 1,0 | o talento e o dom só de quem está em cena (hoje lista todos os presentes: 3,5); o resto em `talento.py mestre`; de B, 4 linhas: o querer escondido de quem está aqui, quem desconfia de você, a rolagem oculta do "dá pela falta", o padrão da caixa que vence hoje |

O jeito, visto no protótipo (Dia 61 do robô que não respondia):
```
## Quem está aqui
- Lino (mercador), trabalha (mercado) · desconfia de você (não respondeu quando ele pediu)
- Brasco (caravaneiro), à toa (praça) · desconfia de você (não respondeu quando ele pediu)
- Bento (ferreiro), trabalha (forja) · não tem opinião sobre você
...
## A caixa (1 de 7)
- c4 · Lino quer para a loja: espada Comum, por 18 de prata · prazo: 1 dia · a) aceitar · b) recusar · calado: recusar (o mercador pede a outro)
## Dois fatos que não tocam você
- os goblins da Mata do Corvo levaram comida de Pedra Rasa (Dia 57)
- Pedro Correia e Rosa Prado estão sempre juntos (Dia 53, Ribeira)
```

### 4.3 Onde o jogo para e pergunta

- O item da caixa que vence em um dia vira pergunta, sozinho, com o código ligado ao comando (o `fecha` recusa sem ele).
- Quem vai junto: o comando recusa sem a paga, e diz o preço e o porquê; o Mestre pergunta ao jogador.
- O preço da encomenda (aceitar, pedir mais, recusar) é a pergunta da caixa.
- O furto: o jogador declara; o dado rola uma vez; o "dá pela falta" é rolagem oculta.
- A cobrança: pagar ou negar.

### 4.4 O que vai ao SÓ O MESTRE

Os números da opinião (a mesa só diz a palavra e os porquês, se o jogador escolher assim: pergunta 3); os quereres escondidos (furtar, cobrar antes de cobrar); quem desconfia de quem; o "dá pela falta" e o furto do ladino de nome; as notícias que ainda não chegaram aonde o personagem está; a conta rápida das missões dos nomeados.

---

## 5. Uma cena jogada (a vila de teste do ferreiro, com a região em volta)

**Dia 61, manhã, Pedra Rasa.** Aldo serve o jornal na forja há dois meses (`oficio.py jornal 2` todo dia: 170 blocos de bancada, a mão de Treinado desde o Dia 50, o jornal pago como oficial, a fama de ofício ali perto de 10, o tom da vila em zero) e não respondeu dois pedidos: Lino e Brasco "desconfiam de você (não respondeu quando ele pediu)", −2 cada. A MESA traz: "c4 · Lino quer para a loja: espada Comum, por 18 de prata (a loja repõe a prateleira: 10 de 11)". A freguesia levou da prateleira uma espada e uma lança nesta semana. O jogador responde "1a" (`caixa.py responde c4 a`). Aldo compra 3 de metal Comum (`mercado.py comprar metal:0 3`, 11 de prata) e chama o Zeca de ajudante (`gente.py chama zeca ajudante`: o Zeca pede 3 de prata pelo bloco, o salário de aprendiz). Forja a espada num bloco: a chance, com a receita, o fogo, a bigorna e o ajudante, é 93% (89% sem o Zeca: `oficio.py pede arma espada Comum`); passou, 33 contra 28. `missao.py entrega m9 i0197`: a espada vai à prateleira, a loja paga 18 do caixa de Pedra Rasa, Lino passa a simpatizar com você (−2 de antes, +3 agora: fez a peça no prazo), e a notícia "o ferreiro de Pedra Rasa fez a espada da loja" chega amanhã a Ribeira e a Cancela (um salto). Na conta: 18 − 11 − 3 = 4 de prata por um bloco, menos do que o jornal paga por bloco ao oficial (6). Vale porque é o terceiro bloco do dia, que o lugar não paga (a jornada são 2), e porque Lino lembra.

**Dia 62.** Na caixa: "c5 · Tomé quer consertar a Lança de Tomé (6 pontos), por 22 de prata · prazo: 2 dias". A lança é Incomum: o conserto pede 1 de metal Incomum (20 de prata na loja) e 2 blocos. Aldo responde "2b" (recusar): Tomé leva a lança ao Bento e lembra "recusou o pedido" (−1). No quadro de Pedra Rasa, a missão do alcaide: "caçar os lobos que atacaram o rebanho de Cancela, grau D, 60 de prata, caução 12". O teto de Aldo é F: a missão não vem à caixa dele, só ao quadro. Ele tenta levar gente: `caca.py sair mata alvo=lobo com=rute,tome` recusa e diz "Rute pede 6 de prata e a parte (o lobo é o limite dela); Tomé pede 12 e a parte". Aldo tem perto de 300. Paga 18 (`... paga=18`), pega a missão (12 de caução, guardada), e o resto é a caçada do capítulo 9: a missão fecha quando a contagem de lobos da Mata do Corvo cair pelo que ela pede, pela mão do grupo (`missao.py cumpre m11` confere o despojo).

**Dia 66, sem Aldo.** Em Ribeira, Gaspar Seixas, o guarda, pegou no quadro de lá a escolta do mercador até Pinhal (a rota de perigo 2, grau E, 25 de prata, caução 5); cumpriu em 3 dias, voltou com a lança gasta em 3 e mandou consertá-la ao ferreiro de Ribeira. A notícia "Gaspar Seixas cumpriu a missão do mercador de Ribeira" chega a Pedra Rasa no Dia 67 (um salto), e vai à mesa entre os fatos que não tocam Aldo. No SÓ O MESTRE: o Quim quer furtar (a bolsa dele está em 4 de 15) e vai à praça de tarde, onde Dalva não está; a vigia de Pedra Rasa está em +2 (uma falta descoberta no Dia 59).

---

## 6. As metas do banco (`provas_gente.py`; o `provas_mundo.py` o roda)

Robôs: o **atento** (responde tudo o que a mão dele faz), o **mudo** (nunca responde), o **parado** (não faz nada), o **guloso** e o **prudente** no furto, o **melhor caso** (fama 100, preço × 0,8, demanda alta). 365 dias, 20 sementes, na vila de teste com a região de A (no protótipo, 3 sementes com o arremedo).

| Meta | O que se mede | Faixa | Medido no protótipo |
| --- | --- | --- | --- |
| GE1 o mundo anda sem você | o parado: notícias que nascem; encomendas e missões de nomeados; laços que viram notícia; ao menos uma notícia por semana chega a Pedra Rasa sem tocar o personagem | 0,3 a 3 por dia; 20 ou mais encomendas e 50 ou mais missões no ano; sim | 0,7 a 1,2; 58 a 88 e 190 a 230; sim |
| GE2 a prata fecha | gente + lugares + guarda das missões, todo dia, toda semente | igual | igual (63.374) |
| GE3 o mudo perde por calar | a opinião média em Pedra Rasa no Dia 365, o atento menos o mudo; os clientes do mudo vão a outro ferreiro | 1 ponto ou mais; 70% ou mais | 1,2 a 2,0; 100% |
| GE4 a caixa não enche nem seca | itens por semana do atento; nunca mais de 7; o oitavo força | 0,5 a 5; sim; até 2% | 1,3 a 1,6; máximo 3; 0 |
| GE5 só escreve quem tem motivo | o banco tira o motivo (conserta a peça, enche a prateleira, apaga o fato) e tenta abrir: recusa | sempre | (a construir) |
| GE6 a memória cabe | ninguém com mais de 12; o peso esfria pela tabela; a opinião de −10 a 10 | sempre | máximo 12 |
| GE7 a notícia anda uma rota por dia | nenhuma chega a k saltos antes do dia k; boato no 5º salto; sai 28 dias depois de parar | sempre | pela construção (a construir com o mapa fixo) |
| GE8 a encomenda não é mina | a encomenda líquida por dia: o ferreiro de começo; o melhor caso | até 2; até 6 | 0,15 a 1,2; 3,2 a 3,4 |
| GE9 a missão não é mina | o atento que pega toda missão de levar: a paga por dia de viagem (com a viagem de A) | até a diária de oficial (12) | 1,7 a 3,5 por dia de calendário (a viagem é arremedo) |
| GE10 o furto não é renda | 30 vidas de 30 dias, o Iniciante e o Treinado, guloso e prudente: o furto com a pena; a bolsa contra a do diarista | menos de 4 por dia; abaixo do diarista | −0,76 a +0,33; +0,12 e +0,28 contra +1,03 |
| GE11 quem vai junto | o pedido segue a tabela nas quatro faixas; ninguém vai a dois acima do teto; opinião −4, recusa | a conta exata | sim (m4) |
| GE12 o tempo | o ano com 150 nomeados, a região e o robô; o gravador novo dá o mesmo mundo que o de hoje | menos de 2 minutos; igual byte a byte | 5 a 9 s (o de hoje: 2,6 min); igual |
| GE13 o peso | os arquivos da gente no Dia 365; o registro de B por ano | até 300 KB; até 2 MB | 150 a 230 KB; 1,2 a 1,8 MB |
| GE14 a mesa | as seções de B; a MESA inteira do atento no Dia 365 | até 2,5 KB; até 8 KB | 0,9 a 1,3; 14,6 hoje (pede os cortes de 4.2) |
| GE15 a vila de teste de hoje segue igual | no mundo sem ninguém de papel, o módulo da gente não faz nada (o mesmo mundo, ligado e desligado, como a MG1); os bancos de hoje passam inteiros; com a região, as metas antigas (a forja de loja, a caça, a coleta, a cripta, o Tição) seguem na faixa | sempre | (a construir) |
| GE16 a gente se repõe | os nomeados por lugar no Dia 365 | de 80 a 120% do começo | 144 de 144 (ninguém morreu) |

---

## 7. Onde toca a metade A

| O que B precisa | De A, nesta forma (proposta) |
| --- | --- |
| a notícia anda pelas rotas | `rotas`: `{a: {b: {blocos, perigo, aberta}}}`; B só lê `vizinhos(E, lugar)` e `rota_aberta(E, a, b)`. A rota fechada não leva notícia |
| a missão de levar e de escoltar, e a viagem do nomeado | `viagem.anda(E, pid, destino, com=[...])`, que chama, antes de sair, o gancho `companhia` de B para cada um de `com` (o preço e a recusa); e o perigo da rota em grau (F a S), para a conta de quem vai junto |
| o cliente compra no mercado de A | a compra de quem não é o personagem (`mercado.compra_de(E, pid, bem, n)`) e o valor da peça (8.8). A taverna e a loja chamam o gancho `negocia` de B antes de vender (a opinião −6 recusa) |
| a loja que encomenda | quantas peças a freguesia leva da prateleira por semana, por lugar (no arremedo: vila 1, cidade 3, capital 8; chute) |
| a prata entre lugares | **o número mais importante:** o caixa de Pedra Rasa vai de 2.000 a perto de zero em um ano em todas as rodadas (o jornal do personagem leva de 2.700 a 3.400; a bolsa da gente se enche do caixa do lugar; as aldeias perdem de 10 a 50% para as vilas e as cidades, porque é lá que estão os ferreiros e quem cumpre missões). A reposição de A tem de cobrir isso, sem virar fonte |
| os nomeados novos | o povo em número do lugar (`lugar.pop`) perde 1 quando nasce um nomeado; quem migra com o povo (A) leva o nomeado junto (a notícia é de B) |
| o bicho que sai do ermo | o evento de A é o motivo da missão de caçar do alcaide (B lê o evento da semana) |
| os ofícios pela região | `oficina`, `runas` e `ensina: {ofício: grau}` no lugar (A); o gerador de B põe ali quem tem a mão para ensinar (o papel mestre ferreiro, encantador) |
| a MESA | A põe o lugar, as rotas e a viagem no "Aqui"; B, as quatro seções de 4.2 |

E o que A pode precisar de B: a notícia (o evento de A põe `['noticia', 'nasce', ...]` no mesmo evento: a estrada fechada, a fome, a caravana); a missão (o mercador que pede escolta); quem vai junto (o gancho).

---

## 8. A construção

**O alicerce comum** (um construtor, primeiro, sem regra nova de jogo):
1. `estado.py`: a cópia de ensaio rasa (`medidas/cow.py` é o rascunho, conferido byte a byte); os verbos novos de A e de B (3.3); os arquivos novos em `ARQS`, com o padrão vazio; os invariantes (3.4); a prata que soma a guarda das missões; o `presente` que recusa o preso.
2. `tabelas_mundo.py`: os eventos novos, o `MUNDO_SOZINHO`, os módulos novos em `MODULOS`, os ganchos novos (`negocia`, `companhia`).
3. `turno.py`: o orçamento da MESA (4.2), os cortes, e a caixa que vira pergunta sozinha; o `fecha` que recusa o item da caixa a um dia do prazo fora das perguntas.
4. Os ganchos chamados nos arquivos dos outros: `mercado.py` e `ato.comer` chamam `negocia`; `caca.py` e `masmorra.py` chamam `companhia` ao abrir com `com=`. (Assim B não mexe nesses arquivos.)

**Os construtores de B** (dois, cada um nos seus arquivos):

| Construtor | Arquivos | O que expõe |
| --- | --- | --- |
| B1, a gente | `gente.py` e `tabelas_gente.py` (novos), `manha.py` (o furto ligado), `provas_gente.py` (novo) | `povoa`, `povoa_regiao`, `ponto` (a rotina), `opiniao`, `lembra`, `tom`, `fama`, `teto`, `aceita` (o gancho `companhia`), `negocia`, `virada` (a semana e o querer), `mesa`, `so_mestre` |
| B2, a caixa, a missão e a notícia | `caixa.py`, `missoes.py`, `noticias.py`, `tabelas_caixa.py` (novos), `oficio.py` (o conserto para o cliente, o ajudante pago, a entrega da encomenda), `provas_caixa.py` (novo) | `caixa.abre`, `vence`, `responde`; `missao.abre`, `pega`, `cumpre`, `entrega`, `fecha`; `noticia.nasce`, `anda` (a virada), `chegou(E, lugar)` |

B2 depende de B1 só por funções de leitura (`opiniao`, `lembra`, `fama`): combinam a assinatura no contrato (`projeto/ETAPA_3.md`) e cada um escreve só nos arquivos dele. `vila_teste.py regiao` é de A, que chama `gente.povoa_regiao`. A integração (o banco da região inteira, as metas GE15 e GE12 com o mapa de verdade) fica para o fim, com A.

Tamanho (chute, pelo protótipo, que tem 800 linhas sem as recusas e as frases da mesa): `gente.py` 600, `caixa.py` 250, `missoes.py` 400, `noticias.py` 200, as páginas 200, os dois bancos 900.

---

## 9. O que fica de fora

- A memória da gente sobre a gente (só os laços); a conversa (o que cada um sabe, além das notícias que chegaram ao lugar dele).
- A conta rápida da luta de quem não é o personagem (etapa 5): até lá, a tabela do 2.9.
- O furto de peças, o furto de noite, arrombar casa (só prata, de dia).
- O casamento, os filhos, a herança, a família que cobra (etapas 6 e 7: os campos `lacos` e a memória dos mortos já estão prontos).
- Os rivais como clientes, o leilão, a janela do mundo (etapa 5).
- A frente que gera missão (etapa 6: o campo `frente` da missão).
- A encomenda acima do Raro (o núcleo é da história e dos rivais).
- A medida do encanto por encomenda (pouca gente rica; o personagem começa Leigo).

---

## 10. As perguntas ao jogador (no máximo quatro)

**1. Quem vai junto pede paga?** (Era a pergunta 13.5 do `PROJETO.md`.)
- **a)** só quando o perigo chega ao limite dele: ao que não o assusta, vai pela parte do despojo, como hoje; no limite, a diária; um acima, três diárias; dois acima, recusa (e a amizade desconta). **Recomendo.**
- b) sempre a diária, além da parte.
- c) nunca pede: só recusa o que passa do limite.

**2. Quem é pego furtando:**
- **a)** paga o triplo (ou vai preso), e quem lembra do crime com −6 ou pior não negocia com ele: roubar a taverneira e o mercador fecha a comida da vila. **Recomendo** (medido: o furto rende menos que a diária com folga, e é a vila que lembra).
- b) só a multa e a memória: todo mundo segue vendendo a ele.
- c) mais duro: pego uma vez, o alcaide o expulsa da vila por uma estação.

**3. O que a mesa mostra do que a gente sente:**
- **a)** a palavra e o porquê ("Lino desconfia de você: não respondeu quando ele pediu"); o número fica com o Mestre. **Recomendo.**
- b) a palavra, o porquê e o número (−2).

**4. Quanto a região pede de você:**
- **a)** como medi: de 1 a 3 pedidos por semana para quem trabalha (a encomenda, a loja, o conserto, o recado, a cobrança). **Recomendo.**
- b) mais cheia: de 3 a 6 por semana (a gente pede mais, com o mesmo motivo no estado e a paga menor).

---

## 11. Onde o desenho pode quebrar o equilíbrio (honestidade)

1. **A prata do lugar.** A bolsa da gente se enche do caixa do lugar toda semana, e o jornal do personagem tira dele de 2.700 a 3.400 por ano: Pedra Rasa seca em todas as rodadas. Se a reposição de A for fraca, os salários param, a gente não junta, a encomenda some e a região congela; se for forte, a bolsa da gente vira bomba de prata para o bolso de quem vende a ela. A gente e o mercado se calibram juntos, e eu não sei o número de A.
2. **A encomenda grande.** Uma peça Rara por encomenda paga 1.080 de prata pelo valor inteiro (a matéria, uns 324): perto de 750 de lucro, mais que dois meses de jornal de oficial. Hoje ela é rara (só o rico quer, a bolsa tem de ter o dobro do preço, a forja de cidade, a mão de Treinado), e no ano medido não houve nenhuma. Se a história da etapa 7 puser mais gente rica, ou os rivais da etapa 5 encomendarem, vira a mina. O banco precisa de uma meta para ela (quantas por ano na região, e a renda do melhor caso).
3. **A opinião que se fabrica.** Pequenos favores repetidos (o recado de 11 de prata, o conserto barato, a peça vendida pelo custo) sobem a opinião de uma vila inteira, e com +7 quem vai junto vai de graça e quem agradece dá um quinto da bolsa. No ano medido, a opinião média do atento em Pedra Rasa ficou em +3 e ninguém agradeceu com prata; mas um jogador que mira nisso pode chegar à vila que o segue de graça para a cripta e a toca. O teto de uma oferta por fato forte e a paga da companhia são o que segura; não medi o jogador que mira nisso.

Também não sei: se 1 a 3 pedidos por semana é o ritmo que o jogador quer (pergunta 4); quanto o registro de eventos cai com o mundo sozinho num evento por dia; quanto a conta rápida da etapa 5 vai mudar o número de mortes de nomeados nas missões (zero, no protótipo, porque o nomeado quase não pega o que passa do teto dele).
