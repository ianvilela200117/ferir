# REVISÃO COMPLETA DO JOGO — MOTOR 9 (Dia 437, pedido do jogador)

**O pedido:** "revisão completa de todos os documentos do RPG; criatividade, magias, leis, habilidades, talentos, como um jogo completo, no nível das nossas inspirações".

## O que foi lido
- O Motor original inteiro pelo índice e as partes de regra (85 páginas: as 16 Leis, combate e magia, condições, técnicas compostas, lei e crime, anatomia do item).
- O Livro do Mundo: mundo, grimório (247 feitiços), classes (11 famílias, ~120 classes), talentos (~75), essências e materiais, bestiário, segredos.
- As regras da casa (199 em diante), o protocolo (G1 a G24), o MESTRE.md, o Motor 7, a ficha do rei, as fichas de combate, o gerador, os scripts que rolam.

## O que já estava no nível de um jogo completo
- **Classes:** 11 famílias, árvores de 15 nós, classes por raridade com assinatura, fraqueza e Prova, e as pontes entre famílias.
- **Magia:** 13 escolas do 1º ao 9º círculo, com preço de verdade no 9º.
- **Forja:** a Lei do Valor, os ramos do ofício, Sob Medida, Série, núcleo para Mítico.
- **Mundo vivo:** tick, facções, guildas, reputação, pilares das cidades, conselho, covis, masmorras por salas.

## ERROS ACHADOS (e o que foi feito)
1. **Feitiço em área com o multiplicador inteiro.** O grimório e a regra da casa do Dia 200 dizem: em área vale METADE do multiplicador do foco. A **Chuva de Brasas** (área) estava nas fichas do rei e do Moreth com ×10. O certo é **×5**. *Feito:* as duas fichas acertadas daqui em diante. As lutas passadas ficam como rolaram (a Lei 8 e a regra de não rolar de novo). Este erro favorecia a casa.
2. **A ficha visível do rei estava velha.** O bloco "Ferir" do `estado_vivo.md` dizia nível 143, PV 376, Inteligência 172. O `ficha.json` (o que os scripts usam) dizia 156, 402, 185. *Feito:* os números do bloco acertados; o bloco agora avisa que o número de hoje mora no `ficha.json`.
3. **A ficha de habilidades do rei (`habilidades.py`) não servia.** Tinha 16 itens marcados "conferir" e nenhum feitiço. *Feito:* refeita com os 17 feitiços, as peças com carga e as duas receitas de servo; ganhou o comando `mao`, que é a fonte da linha 🛠️ (G24).
4. **O teste de magia do grimório não era o que se joga.** O texto dizia d20 contra Resistência Mental; desde o Dia 379 a luta roda a magia disputada (2d20 + ataque contra Defesa + 14). *Feito:* o grimório explica as duas coisas.
5. **"Escola oposta" não existia.** O talento Escola Funda cobrava a mais na escola oposta e nenhum livro dizia qual era. *Feito:* a tabela está no Livro Nove 1.5.
6. **Nomes esgotados.** Três das seis sonoridades do `nomes.py` não tinham mais nenhum nome livre (por isso o gerador repetia começos). *Feito:* começos novos nas três.
7. **O calendário do Livro parava no Dia 356.** *Feito:* atualizado (hoje é o 8 da Lua da Seca; os Jogos na Lua do Vinho, Dia 490).
8. **Traço de monstro que o `luta.py` não rolava** (o grito que dá medo). *Feito* no turno da rainha; a regra geral agora é a G33: traço fora do script é declarado antes da luta.
9. **Osso preso em peça.** A regra "Sangue e Osso cobram sempre" nunca foi cobrada no Toque do Ceifador lançado pelo Foco de Osso nem pelo gorjal da Isolda. *Decisão do Mestre, escrita na G31:* peça não cobra sangue (a peça pagou na obra). Era o que se jogava; se o jogador quiser o contrário, é só dizer.

## O QUE FALTAVA (e agora existe: `compendio/08_livro_nove.md`)
| Faltava | Inspiração | O que entrou |
| --- | --- | --- |
| guerreiro de nível alto sem poder próprio (a Aura parava no 2º círculo) | as artes de espada e os golpes ligados dos romances | Aura até o 6º, 21 Artes de arma, Encadear e o Remate (G30) |
| marco nos níveis 100, 200, 300 | o despertar e a transcendência | 12 Dons com preço (G26) |
| magia sem truque, ritual, pergaminho, concentração, contra-magia para todos | os jogos de mesa | as sete regras da seção 1 e 39 feitiços novos (G31) |
| item que cresce, arma com vontade, efeito escondido, fundir e desmanchar | o ferreiro lendário | seção 7 (G32) e 8 talentos de ofício |
| poções e óleos sem lista | os jogos de mesa | 22 consumíveis com preço |
| monstro sem variedade nova, sem chefe de duas fases, sem "nomeado" | chefes de masmorra e de mundo | 16 traços, Resistência Lendária, fases, nomeados (G33) |
| filhote e montaria de monstro | os mascotes que crescem | crias e montarias (G25) |
| armadilha e enigma sem tipo; masmorra que não reage | os jogos de mesa | tabelas e o relógio da masmorra (G34) |
| lei escrita do reino | o reino do ferreiro | o Código de Ireviel: 16 éditos (G27) |
| feito que vira poder | os épicos cantados | Canções de Feito (G28) |
| fé sem efeito para o fiel | domínios e bênçãos | 10 bênçãos com voto (G29) |
| torneio | as competições entre reinos | os Jogos das Cidades |
| classes que faltavam em cada família | as duas | 11 classes novas (entre elas o **Físico de Campanha**, que encurta ferimento, e o **Armeiro dos Mortos**, o caminho do rei com os servos) |
| talentos | as duas | 32 talentos novos |

## O QUE MUDA PARA O REI AGORA
- **Um Despertar em aberto** (ele passou do 100): escolher um Dom (Livro Nove 4).
- **A Chuva de Brasas dele bate a metade** do que batia (×5).
- **O ferimento:** o Livro continua sem magia que feche ferida velha (o dado do 437 disse que não há). O que existe agora é o **Físico de Campanha** (classe) e o **Édito do Físico**: achar ou formar um é um caminho de jogo.
- **Os servos:** o Édito do Osso tira a perda de reputação dentro do reino; a bênção do Sino barateia o sangue; a classe Armeiro dos Mortos junta a forja com o osso.
- **Zythir:** o relógio da masmorra vale a partir da sala 9.

## O QUE NÃO FOI FEITO (para não esconder)
- As ~60 fichas de NPC com classe fora do Livro e os desejos e medos que faltam continuam como estavam (preenchem-se quando cada um entra em cena).
- Os traços novos de monstro não estão no `luta.py`: o Mestre aplica à mão, declarando antes (G33).
- As Artes de arma dos heróis da casa (o Moreth, o Eiagrir, a Eliane, a Isolda, o Graur) ainda não foram escolhidas: entram na ficha de combate, declaradas no envelope, antes da próxima luta de cada um.
- Os Despertares dos NPCs do mundo rolam quando eles entrarem em cena.
- O Livro em HTML (`livro_do_mundo.html`) foi refeito com a aba nova.
