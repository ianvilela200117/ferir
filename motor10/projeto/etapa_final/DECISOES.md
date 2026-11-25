# As escolhas da etapa final (para o jogador rever)

Onde o plano deixava aberto, ficou o padrão abaixo. Cada linha diz o que ficou, a outra saída e o que ela mudaria. Mande mudar por código, como sempre.

1. **A estrada é um lugar** (como o ermo e a sala): o que cai nela fica nela, quem morre nela fica nela, e o bando é contado nela. A outra saída: a estrada só como
   número entre dois lugares (mais simples, mas a morte na estrada não teria onde deixar as coisas).
2. **O personagem nasce no nível 5** (o da vila de teste, onde a luta foi afinada), com a mão de Iniciante no ofício da família. A outra saída: nível 1 (a luta
   de começo fica mais dura do que o banco mediu).
3. **Os seis berços saem das famílias do mundo** (ferreiro de vila, caçadores de aldeia, guarda de cidade, mercador da capital, enjeitado do templo, casa nobre menor).
   O povo escolhido que não é o da família nasce acolhido nela (filho de criação). A outra saída: o povo decide os berços que aparecem.
4. **Os 150 nomeados e os 40 rivais são gente à parte** (190 com ficha). A outra saída: os rivais entre os 150.
5. **O querer dos nomeados é semanal e sai de uma tabela por papel** (o ferreiro forja para a loja, o caçador caça, o mercador leva carga, o guarda patrulha, o senhor
   paga a missão contra a frente...). Cada querer muda número. A outra saída: o querer livre, escolhido pelo Mestre (fica à mão dele por `estado.py mestre`).
6. **A notícia anda uma estrada por dia, de lugar de povo em lugar de povo**, e vira boato do quarto salto em diante (o texto ganha "dizem que"). A janela do mundo
   chega a todo lugar no mesmo dia.
7. **A conta rápida da luta dos rivais** é uma curva (a chance pela diferença de força, a força tirada da ficha e das peças), afinada contra o `luta.py` no banco.
8. **O herdeiro herda as peças que ficaram com o corpo e que o matador não levou** (a família recolhe), a casa, e a memória dos outros pela metade.
   O matador fica com o que o morto vestia. A outra saída: o herdeiro só herda o que estava guardado em casa (não há casa-cofre ainda).

## O que a construção e a afinação decidiram (para rever)

9. **A afinação pelo banco do ano** (os números no `tabelas_regiao.py`): a ousadia dos rivais (a chance mínima que aceitam: novato 25%, oficial 33%, veterano 50%, Lenda 60%);
   a morte de quem perde a luta da conta rápida (70% vezes o quanto era ruim; quem vai junto, 60% disso); a caça para viver também mata (0,1% a 0,8% por semana); a guilda
   recolhe o corpo, e o povo acha a peça de quem caiu (fora da cena do personagem); a forja do núcleo (o mestre ferreiro da capital com forja 6, o sinal de 40%, 8% do valor,
   27 dias para a Épica); as frentes rolam contra 17 (3 a menos nos dois primeiros passos), a missão só barra no passo zero, o rival que investiga expõe (tira um passo) e não
   barra; as duas faltas do Dia 1 saem de quatro (a seca, a mina, a praga do gado, o sal); a fome nasce com o celeiro abaixo de 8 dias. A outra saída de cada um: o número.
10. **O torneio é só entre os rivais** (a conta rápida, um contra um). O personagem ainda não entra nele: entrar pede a luta de verdade, rodada a rodada, e fica para quando o
    jogador quiser (a regra cabe: o convite pela caixa, a luta pelo `ato.py luta`).
11. **O ferreiro aplicado da meta 9** (a primeira Épica entre os dias 60 e 85, a Única entre o 160 e o 220) segue medido fora do mundo, no `provas_oficio.py` (A ESCADA). No mundo,
    a primeira Épica nova sai das mãos dos rivais no dia 42 (mediana de 20 anos).
12. **A MESA e o RETOMAR cabem em uns 20 KB** (o plano dizia 14). O que pesa são as tabelas do mercado e da magia das etapas 2 e 4. Cortar é escolha de gosto.
13. **O motor não sabe o gênero de ninguém:** o laço vai à mesa nas duas formas (pai/mãe, filho/filha, irmão/irmã), e o texto evita o gênero onde pode.
14. **O nêmesis bicho:** quando quem matou não tem ficha (o bicho, o bando da estrada), o que o morto vestia fica guardado onde ele caiu (a toca, a estrada), e a frente do nêmesis
    leva o nome do bicho ou do bando.
15. **O dragão ancião:** dorme de 400 a 700 dias; a frente dele rola a cada 28 dias; no passo 6 ele acorda e passa a cobrar do lugar mais perto (a vida do dragão da etapa 4b).
16. **O nível não sobe** (como em todas as etapas): o personagem começa no 5, e o que cresce é a mão, as peças, a fama, a casa.
17. **A memória que se escreve sozinha** vem das missões, da caixa, da família, da luta ao lado na estrada e da herança; o resto da cena, o Mestre põe (`gente.py lembra`).
