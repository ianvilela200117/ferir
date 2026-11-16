# RETOMAR — manhã do Dia 437, Zythir, a sala 5 limpa (MOTOR 8: G1 a G22)

## Primeiro
1. `python3 contexto.py` e ler o BRIEFING.md, o MESTRE.md e o protocolo_do_turno.md (o MOTOR 7.2 e as regras da casa G1 a G10 estão no fim dele).
2. Ler o ESTILO_NARRATIVO.md antes de narrar.
3. `python3 tracos.py cena Nome` antes de pôr fala em NPC. A inclinação de voto sai de `tracos.py inclina`, não da cabeça.
4. O envelope atual é `envelope_sessao2o.md` (aberto no 427, 15:05, porque o 2n passou de 400 KB; é nele que o `selo.py` escreve agora). A última PARADA está no fim do 2o (PARADA: MANHÃ DO 437, Zythir, a sala 4); a do 426 → 427 está no fim do `envelope_sessao2n.md`. O diário é `diario_sessao2f.md` (o fim dele é o meio-dia do 433). O estado está em `estado_vivo.md` (bloco "MEIO-DIA DO 433").
5. O save canônico é o do Dia 396 em diante. O bloco 379-384 rolado num chat antigo sobre o save velho foi ANULADO.

## Onde paramos
Manhã do 437, ZYTHIR, a SALA 5 LIMPA: o guarda HUIR (Épico 78, Espinho; o nome do gerador, Thuula, trocado) morto na 1ª rodada pelo Moreth, pego de SURPRESA (o favor do eco); ninguém ferido; o rei 84/402; despojos nee 30, yeviel 60, núcleo Épico de Espinho; TC37 [2] o covil sem tesouro · à frente: a SALA 6 (TESOURO Único, G17: rolar pelo selo ao entrar), a 7 (ARMADILHA: passa sem dado, o favor do eco), a 8 (a RAINHA da colmeia, PERIGO Épico), a 9 (O CORAÇÃO: OCULTO, o rei TUIR vivo, e o guardião Único) · o eco de Tuir está no livro (npc.py, nível 160) · A CARTA DO TOLVANE dada à mesa no 437 (o Mestre a esqueceu no turno do 436): o Celocus não respondeu; mostrou HADUN à venda (OCULTO: pena do HUSGARN, servo do Skorval) · a saída para Farenta no amanhecer do 438 (Farenta ~443; OCULTO: a Elaeva chega às terras de Farenta no 444) · ERRO DO MESTRE corrigido no 437: a saída do gerador cortada (head -12); o resto (drops, comportamento, sinal) rolado uma vez pelo código do gerador (obras/zythir_sala5_guarda_resto.txt).

Antes (a sala 4):
Manhã do 437, ZYTHIR, a SALA 4 (a PASSAGEM escondida da 4 desce direto à 6; o FAVOR do eco gasto: a armadilha da 7 passa sem dado e o guarda da 5 é pego de SURPRESA, ele não age na 1ª rodada; masmorra.py ver Zythir tudo: a 4 é SEGREDO, a 5 PERIGO Épico, a 6 TESOURO Único, a 7 ARMADILHA (notar CD 23; 6d6 e uma condição), a 8 PERIGO Épico (a RAINHA da colmeia, pelo eco de Tuir), a 9 o CORAÇÃO: o prisioneiro (OCULTO: o próprio TUIR, vivo) com o guardião Único; +2 nos perigos da volta). O tick do 437 JÁ RODOU. O rei 84/402 (a ficha de combate agora tem o Gibão e o 'desfaz'); o Moreth 578, o Eiagrir 228 (sem noite completa de cura: conferir na G9); a Tigra (15), o cabo Gonde (30, o elmo) e os 10. A Eliane de cama em Levis até o 443. A saída a Farenta no 438 (OCULTO: a ELAEVA chega às terras de Farenta no 444). O eco de Tuir DEVE UM FAVOR ao rei.
- OCULTOS: a ALMISION acordou a Elaeva e deu o nome do Adurel (a palavra da Mamiltia chega no 440) · a Groa passou a medida da Fornalha (o cobrador identificado) · o Odrum sócio da Moeda Velha no que a frota perdida deu · o Krothos tem 1 cria · as surpresas do Rio Vermelho e das Mães da Porta (consequência antiga) na fila da G8-C.
- A ORDEM DO REI contra a revolta de Marasar chega a Ireviel no meio-dia do 434: a força do Graur (as 20 lanças, a guarda que pode sair, a Guilda e 1d6+4 magos da Chama da Hoste: rolar os números) sai à tarde e chega a Marasar no 435 (batalha.py; os Fiéis do Doge Velho, força 6) · o Facio vai com eles, para ser entregue à Skotha · a LEGITIMIDADE caiu a 9 (o rei passou por cima do voto do conselho).
- Ireviel sabe e o rei ainda não: a Eloune morta pelo Teraseth (o recado dele, com o coração DE PRESENTE, alcança a barca no 434: agenda #448, oculto) · a contra IDENTIFICOU o homem das guildas de Steunn (o cobrador da Groa; a Sira o vigia; OCULTO: a Groa passou a ele uma medida da Fornalha) · o Celocus pagou os 800.
- OCULTOS que vêm: 433 a notícia de que o TERASETH MATOU A ELOUNE (432) e manda o coração (núcleo Épico de Água) ao rei DE PRESENTE: alcança a barca no 434 (agenda) · 436 a carta do Tolvane: o Celocus não respondeu e mostrou HADUN à venda · a GROA PASSOU uma medida da Fornalha ao homem das guildas de Steunn (infiltrado, furt 6; a contra já notou 'alguém estranho', 432) · o vilão novo ZEAZHIS (150) em Yaelane (notícia no 433) · a revolta de Marasar é dos FIÉIS DO DOGE VELHO (a casa já sabe) · o NPC antigo que volta mudado em Levis (LV31: tabela quando o rei chegar) · em Levis, a SOUANE pôs a Brara sob a proteção dela (429).
- A barca da Liga (ouro, papéis e a carta do Ceduion à Leliel, OCULTO) foi rio acima, à frente do rei; o recado à Sira desceu na barca rápida.

Antes (a noite do 428, Ireviel):
- O dia 428: o conselho deu teto e trabalho ao FACIO; os BARQUEIROS avisados se armam; o recado à SKOTHA chega a Marasar no 429 (rolar a resposta; e no 430 chega a notícia da cidade que se rebela em Marasar: o recado entra numa cidade em revolta); a SIRA tirou pouco do preso da Liga; a ELAEVA ferida (fiel); o TERASETH caça a Eloune SOZINHO (OCULTO: no 432, agenda #436); os DO CROQUE vêm à caçada do rei; o GIUNN dos Jurados quer a Tilde; a disputa da BRECHA; os 20 voluntários da LUZ DO CAIS; o sapato e o olho dos OLHOS PINTADOS no muro da casa.
- O rio voltou a NORMAL: a barca a Levis sai no amanhecer do 429 e chega no 433 (rodar `viagem.py vai ... Levis saida=429 leva=...` na saída; a ISYZIS está no rio acima de Levis, no caminho).
- A noite do 427 (antes): a ALIANÇA com a LURENTETTA (Mítica 774) aceita; o FACIO contou que os nomes do livro foram à LELIEL; o rei leu o núcleo de Espinho; nasceram os RENDIDOS DE MARASAR.

Antes (noite do 427, o cais; Levis ficou para depois por causa do rio cheio):
- O MOREK MORTO (amanhecer do 427, na água rasa da forquilha): numa rodada o Toque do rei e as Lanças do Sol do Moreth e do Eiagrir o puseram de 955 a 96; ele fugiu, a fuga falhou feio, e a LANÇA DO BREN voltou à mão da Eliane com o sangue dele. Ninguém caiu; o Eiagrir levou 186 (87 de PV).
- DESPOJOS: o NÚCLEO ÚNICO DE ESPINHO (serve para peça Mítica) · ssythis 3 kg · laliel 6 kg · heald 3 kg · sasis 3 kg. A MISSÃO dos Barqueiros do Livro pagou 3.000 e a informação: o patrono deles é a SKOTHA.
- O BJORVUNN (noite do 426) contou do ULMIR: Único 178, de Raio, nas salinas do Delta, fraco a Água; o coração é um NÚCLEO ÚNICO DE RAIO. A TESSAL e a LILE acharam ALNESAR: nas colinas a leste de Ireviel, a 2 dias; numa metade há um núcleo e nada mora lá (entrar custa uma luta); na outra, bandidos guardam um segredo de facção (entrar pede uma chave).
- O tick semanal do 427: no cais esperam o ENVIADO DA LURENTETTA (aliança contra a Elaeva, que matou o povo dela) e o FACIO, caído. Os pescadores viram a ELOUNE no lodaçal perto do cais afundado. Em Levis, o Culto do Xaathis venceu a BIGORNA LIVRE (força 1).
- Ferir nível 155, XP 1.204.674 (faltam 4.426 para o 156), PV 194/400. Cofre 16.748 (livro da semana −2.750; +3.000 da missão). Próximo tick semanal no 434.

## O QUE JÁ FOI RESPONDIDO E ROLADO (noite do 406 → amanhecer do 407)
- **1b (MN7 9):** a MAMILTIA aceitou o NOME (o Adurel, Zisrir), NÃO aceita a Almision como prova, manda os olhos dela a Zisrir (~434), fica e pagou a METADE (3.000 XP e 1.500). O Fumigador sai com ela até o 417.
- **3a (MD7 [6]) e 2a:** a ELIANE em pessoa leva a escolta dos Salineiros (6 lanças, 5 de selkos); o DRARON e um capuz levam o aviso a Farenta; com o rei, ao MIVOR: o Moreth, o Eiagrir, o Hruthos, o Tuald de guia e 8 lanças (no cordão, por ordem da Marechal). As duas colunas estão SAINDO pelo portão no amanhecer do 407 (agenda #242 ainda aberta: fechar quando o rei confirmar). (OCULTO) SC7 [6]: a recompensa dos Salineiros não existe mais · CH7 [1]: quem pediu o aviso mente sobre algo.
- **4a:** REGRA G6 (obra nova do reino a quatro quintos).
- **A cidade (3a):** a Intendente governa, o Graur guarda. NL7 [5] / NLp7 [1]: a Nouliel pediu UMA LINHA SELADA (portão, poterna e guarda da Fornalha só mudam com a palavra dela); o rei selou. GR7 [1]: o Graur ficou ferido (opinião −5 → +5).
- **"Reforjar o que já tenho; o Foco de Osso e o restante se for rápido":** o FOCO DE OSSO já é PRIMORDIAL (não há reforja). A obra da noite, sob a Visão (1 das 2): a LANÇA DE GUERRA com eiurvo 0,4 kg e ziza 0,2 kg (RF7: soma 100 + [7]+[19] = 126): alcançou Mítica; sem núcleo ficou LENDÁRIA (XP +2.200). O "QUASE" do script NÃO vale na reforja (compara com a CD sem o acréscimo): consertar o obra_valor.py na auditoria do 408. FERIR NÍVEL 144.
- **TICK DO 407 JÁ RODADO** (tick_407.txt; o rei "na estrada"): Ireviel limpo com VENTO FORTE; rio 6/100; encontro de estrada [16] nada; nenhum avistamento. HI7 [1] (oculto): a contra fechou o nome do HIALD antes do amanhecer; HIs7 [4]: a Sira sabe que ele é do BORECCI e veio pela TILDE, não a ordem (a ordem real, oculta: LEVAR A MENINA VIVA A STEUNN; ele nunca machuca uma criança).
- **AINDA POR NARRAR DO 407 (a cidade, depois que o rei decidir):** os JURADOS DE STEUNN pedem audiência (#229) · os FIÉIS DO DOGE VELHO ameaçam ou sabotam (#232; declarar tabela) · notícias que chegam: a rota da costa fecha (chega FALSA) · a Mamiltia recruta (FIEL; a gente de Telosus já está no portão) · a Vathexa atrai monstros em Steunn (EXAGERADA) · os Vradda em guerra (EXAGERADA) · os Sem-Coroa têm patrono (INCOMPLETA) · lei nova em Yaelane (chega no 408) · o Gorine fez uma obra (chega no 408) · a trama Ruddo → Seline (o gesto dela: de trouxa pronta no portão) · faíscas do tick guardadas: [Sira procura a Guardiã da Tenaz, por vingança] · [Almision foge de Eiandald, por causa da Fornalha] · [Oslo salva Eiandald, por um núcleo de monstro] (o Oslo vai com a Eliane).
- **A CAÇADA:** arquivos em sims/mivor_406_*.json (régua OCULTA no envelope: as lanças na linha morrem; o bicho foge em ~1 de cada 5 lutas). Antes da luta: trocar a arma do rei na ficha de combate pela Lança de Guerra LENDÁRIA (Vento: dobra só o golpe de arma, não a magia) e decidir o que é "fogo comum" (a 2ª fraqueza, a descobrir). O Mivor FALA E MENTE e nunca é surpreendido (oculto).

## RESPONDIDO NO PORTÃO (407): 1b · 2a com ganchos e arpões · 3a · 4b · 5b
- O HIALD solto e vigiado; a TILDE não sai da Fornalha. (OCULTO) o dia da cidade já rolado: HM7 [2] / HH7 [12]: o Hiald só trabalha e ao escurecer pergunta pela menina · FQ7 [4] / FH7 [11]: os Fiéis sabotam um bem da casa EM MARASAR à noite (agenda oculta no 408: declarar o quê) · JH7 [4]: os Jurados de Steunn batem de manhã (a Intendente recebe: decidir o que ela faz quando o rei voltar) · GV7 [1]: o Graur cumpre a linha à letra.
- SOB MEDIDA 4 lançado (ficha: desconto 40). A LANÇA DE GUERRA MÍTICA (um ano de vida; ficha: anos_de_vida_pagos 1; XP +7.500). Ficha de combate do rei refeita (lança 1d10 x3, Vento; magia 16d6 x10, sem Essência).
- A VISÃO (1 das 2) mostrou a primeira hora da cidade: nada contra a casa; o Graur rígido.
- NO LEITO SECO (OCULTO): MV7 [3]: o Mivor espera à vista e FALA primeiro · MVf7 [1]: quer GANHAR TEMPO (diz que vai embora com a chuva) e AFUNDA DEVAGAR enquanto fala · MVv7 [5]: meia verdade (ele precisa mesmo do leito seco; o resto torce) · PV7 15 e PV7b [4]: NEM O REI NEM NINGUÉM NOTOU que ele afunda. REGRA PARA O PRÓXIMO TURNO (declarar antes de rolar): cada troca de fala desce o casco um terço; na terceira ele some debaixo do leito; se a luta começar com ele meio enterrado, declarar o que muda. OS GANCHOS (declarar): quando o MORAL der FOGE, o cordão lança: d20−2: até 8 arrebenta e afunda · 9-14 preso uma rodada · 15+ preso até cair. A 2ª fraqueza (fogo comum = fogo de lenha, óleo, tocha; magia não) segue por descobrir.

## RESPONDIDO NO LEITO (407): 1c com condição · caçar outro já · 2b
- O MIVOR (MVp7 15, MVq7 [3]): aceita DE VERDADE guardar o lado norte por DOIS SACOS DE SAL por semana; primeira paga até o amanhecer do 408; o rei NÃO respondeu ainda. (oculto) se pago, cumpre; se não, declarar o que ele faz.
- O VORTHEN MORTO (VT7; 2 rodadas; ninguém caiu; uma lança ferida leve). NÚCLEO ÉPICO DE GELO, vorthil 4 kg, vorgel 2. XP +770.
- A cidade no 407: os Jurados marcados para o 408 (JU7 [4]); o Hiald só perguntou pela menina; (OCULTO) os Fiéis sabotam um bem da casa em Marasar esta noite (agenda oculta do 408); a notícia da costa chegou FALSA (dizem que reabriu; fechou).
- A Visão do Tempo: 1/2 ainda hoje.

## RESPONDIDO (anoitecer do 407 → 408): 1a com a aliança · a ferramenta · 3b · 4a
- HIc7 18: o HIALD contou tudo (levar a Tilde viva a Steunn, à feira). À espera da palavra do rei.
- OB407 (soma 108 + [12]+[8] = 128): o BERÇO DE SELO, MÍTICO (teto do núcleo Épico); magia rerrolada (fogo não cabe no gelo): GOLEM DE PEDRA. Ficha de encanto: 135 (obra_valor.py, linha do ferir_enc). NÍVEL 145.
- MVa7 16: o MIVOR aceita ficar depois da chuva por um LEITO DE PEDRA e o sal. Despesa +24.
- TICK DO 408 RODADO (tick_408.txt): evento local nada; Farenta Saúde 3 e Dinheiro 2; FIs7 [4]: a shasha da semana queimada em Marasar; JUq7 [6] SURPRESA (novidade [12]: uma lei muda e alguém sofre): LEITURA: as guildas de Steunn fecharam a estrada de pedra ao minério dos clãs de cima enquanto a Tilde não for julgada na feira (é a mão do Borecci; liga com a ordem do Hiald e com o desafio da feira). A APLICAR quando o rei responder: o ferro sobe em Levis e Ireviel enquanto durar (declarar quanto).
- (OCULTO) VILÃO NOVO: VEYTOR (150, as Fundas do Norte; método: exército; obra: conquistar uma região; a notícia chega no 410) · as missões: a Eliane chega às Salinas entre o 408 e o 409 (SC7: a recompensa não existe mais); o Draron a Farenta no 409 (CH7: quem pediu mente): RESOLVER no próximo bloco · faíscas do 408 guardadas: [a mestra Carea ama em segredo a Sira] · [Grerkur esconde um filho de Kasgal] · [o Médico Cinzento vende algo a Kreine].
- AUDITORIA DO 408: o conferidor só repetiu avisos já vistos (fichas sem nível; a acusação do vaduar quente citada, não a casa); cofre certo pela ficha: 27.178. A consertar: o QUASE da reforja no obra_valor.py; o tick_406.txt que não veio no zip.

## RESPONDIDO (408): 1a · 2a · 3d (sondagem MN408) · encantar as mais fortes · Lumade
- O leito do Mivor: obra aberta (reino.py), 1.200 pagos, pronta no 420. O Hiald fica, vigiado.
- MN408: A 3 · B 1 · C 3; a Intendente em C. Os Jurados AINDA SEM RESPOSTA (estão na estalagem do cais).
- ENC8: Toque do Ceifador no Foco de Osso, INTEIRO; XP 50.000; NÍVEL 148; ficha de combate do rei: magia 24d6 x10.
- A ORDEM DOS ENCANTOS ('as mais fortes primeiro'; uma por noite; uma peça leva um encanto só): depois do Foco, as Míticas sem encanto: o Gibão de Orloxa, o Berço de Selo, a Lança de Vestrin (Hruthos), a Lança de Veydun (Eiagrir), a Couraça de Ascra, o Trebuchete; conferir o Martelo de Zeieth (Primordial). O feitiço é do dado entre os de 6º círculo que o rei sabe (o que não cabe rerrola).
- AINDA POR RESOLVER (oculto): as duas missões chegam ao destino no 409 (SC7, CH7) · o vilão Veytor (notícia no 410) · o ferro sobe com a estrada de pedra fechada (declarar quanto).

## RESPONDIDO (408 noite → 411): 1c · 2c · 3a · 4a
- JE8 3: os Jurados perceberam; Steunn 0. ALMA NO AÇO 4 no obra_valor.py (+3). ENC9: o Gorjal da Isolda, Toque do Ceifador, 206, 2x por cena. NÍVEL 152.
- (OCULTO) EB1 [2] a emboscada nos VAUS DE CIMA · EB2 [4] 50: o SHYSSIS e um CAPITÃO pago do Ardenghi · EB3 [4] o ARDENGHI em LEVIS · EB4 [3] um olho no PORTÃO DO NORTE (um carregador do cais) e pombo · EB5 [3] seguraram e mandaram batedores · BT10 5: os batedores viram o grupo sem ser vistos · EB6 2: RECUARAM PARA LEVIS. Fichas de combate do Shyssis, do capitão e do Ardenghi: AINDA NÃO GERADAS (gerar antes da luta).
- SB8 9: a Sira só sabia 'rio acima'. RT11 25: o grupo achou o acampamento, quantos, dois bandos, a moeda P.A. e o bilhete 'sem a pedra. Levis.'.
- TICKS 409-411 rodados. 409: Casa dos Mineiros (MI9 90 kg; 18 kg à forja; despesa 7.040; Levis Comércio +1 mod) · EL9 [4] a ELOUNE mais faminta (notícia fiel; núcleo Épico de Água) · a Souane: um culto mostra o sinal no Delta (fiel). 410: notícias: Veytor (fiel), o Bruur deixou cair um drop em Marasar (exagerada); missão de Zisrir (longe). 411: FEIRA GRANDE EM LEVIS (notícia no 412; TOCA A CASA) · evento de mundo: receita nova circula → aliança inesperada (ler quando chegar) · Pressão zerou.
- MISSÕES (OCULTO, resolvidas no 409; contar quando a Eliane e o Draron voltarem, 411-412): SCr 11: o salineiro ENTREGUE depois de briga com os bandidos das salinas; uma lança ferida leve; SCp [3]: a GUILDA DOS SALINEIROS rachou e não tem os mil (a recompensa não existe) · CHr 16: o aviso chegou ao TIRELLO; CHm [1]: o aviso é ISCA da Chama da Hoste para os Olhos Pintados se mexerem em Farenta. Fechar a agenda #239 quando chegarem.
- Faíscas guardadas: [a Sira acusa em público o Cerrini, por causa da Matriz] (411) · [o Draron vende algo a Tano, por dinheiro da Liga] (411) · [a Isolda → Almision, ressentimento: um gesto dela] (409; usado na cena: a pergunta da data).

## RESPONDIDO (411 → 415): 1a,b · 2b · 3 Casa Firme (o ponto do 150 ficou sem resposta)
- CASA FIRME: reino.py mod Ordem +1 nas quatro cidades; ficha talento_150.
- (OCULTO) EB7 [5] os de cavalo junto · EB8 [5] 35 descalços · EB9 [3] de frente na marcha · EB10 Shyssis 45 · EB11 capitão 62 · CR12 (combate rápido): 56×49 (metade), 69×31 (destroçada); CRe [1] o capitão e os 15 a cavalo fogem para Levis, ~10 descalços somem; CRf [4] e CRh [2] o Shyssis morto; ninguém da casa arranhado. Relógio dos Descalços → Matriz FECHADO.
- TICKS 412-415 rodados (estrada). 412: a Guilda abre (GU12 13 membros); facção nova VARAST em Ireviel (fiel); feira grande de Levis (fiel). 413 SEMANAL: ver tick_413.txt: cofre 23.888; Ireviel Saúde 3, Ordem 4, Defesa 3; MARASAR Comércio 1 + SURTO DE DOENÇA e um ACHADO debaixo da cidade; FARENTA SURPRESA (não resolvida); relações: Doge +3, Steunn −1, Do Junco −3, Colégio +3, Leliel −5; a contra PEGOU UM AGENTE DO ARDENGHI em Ireviel (provável o olho do portão; o rei não sabe); os CONSELHEIROS entraram e acharam um segredo [3]; PELACCINO → GRAUR EXPLODE esta semana; LAÇO: a BRARA, MOMENTO (usar em Levis); vínculos Krernos–Graur sobe, Nouliel–Herkald sobe; SURPRESAS de NPC a resolver na volta: Krernos, Nouliel, Skedda, Iorin, Thuron, capuz 4, Kreine, Ulnar, Starkald, Holgir, Fabaino (Hruthos resolvida: o GUNDALD); a Bigorna Livre pede audiência (#281). 414: AL14 [5] (OCULTO) a ALMISION OFENDIDA FOI EMBORA (Escola Única −1); o DRASSA viaja de Levis. 415: tempestade em Levis; DR14 [2] e DR15 12: o Drassa contou.
- (OCULTO) AR14 [5]: o ARDENGHI arma uma recepção · LV1 [3] em LEVIS-BAIXA, nas ruas do culto · LV2 [1] 40 do culto e um SACERDOTE-MAGO · LV3 o Ardenghi nível 63 · mais o capitão (62) e os 15 pagos. Gerar fichas de combate antes da luta.

## RESPONDIDO (415): 1b · 2b · 3a
- ALMA NO AÇO 5 (+4) no obra_valor.py. ENT15 10 → FORTUNA → ENT15f 23; OLH1 [4], OLH2 13; SUR15 [2] sem surpresa; MAL1/MAL2 o Moreth resistiu; BL15 (batalha.py levis_fundicao_415): 2 rodadas, os cinco inteiros; ARD1 [5] o ARDENGHI MORTO; RUI1 [4]; SAC1 [5]; CAS1 [3], CAS2 4.000; LIV1 [2]; LIV2 [1]. XP +16.300 a cada um; NÍVEL 153. Culto do Xaathis força 5.
- O TICK DO 416 AINDA NÃO RODOU (parada na madrugada). O laço da semana (a Brara, MOMENTO) foi usado na cena da fundição.
- AINDA POR CONTAR AO REI (ele está fora desde o 410): tudo o que está no bloco anterior do tick 413 (Marasar com surto de doença; a contra pegou um agente do Ardenghi; o Pelaccino e o Graur; as surpresas dos NPCs), a ALMISION ofendida que foi embora (414), as duas missões (o salineiro entregue, a guilda sem os mil; o aviso é isca), a facção nova Varast, a Bigorna Livre pedindo audiência (#281, atrasada), o Fumigador que tem de sair no 417.
- Fios a tocar quando o rei decidir: F16 (o Ardenghi pagava...) e F33 (a lista de inimigos: riscar o Ardenghi).

## RESPONDIDO (416): 1 · 2a · 3 · 4b · 5a
- MÃO QUE ENCANTA 5 no obra_valor.py (+10). DRs 25: o Drassa serve; bolsa 700 no cofre. DRl [3] e DRc [1,4] = 2.500; DRb [4] o armazém (600 kg de ferro, carvão), DRm [2] 2 barras de VADUAR (~1 kg).
- (OCULTO) XC1 [5] os 12 nas minas de baixo · XC2 [4] o líder (120) é da ALA DO ARDENGHI · XC3 [5] o líder FORA DE LEVIS, a caminho de LUMGAL (a estrada de Lumade passa por lá) · XC4 [1] só se escondiam. MN16 25: pegos sem luta; MN16b 5: ninguém falou; BRx [5] na muralha; LV16 3: Ordem de Levis −1 (mod, duas semanas).
- A CARTA: viagem.py, agenda #290: chega a Ireviel no 421. Ao chegar: rolar a escolta da Marechal (com quem a Matriz sobe; se o Tolvane vem para falar com o Celocus) e mandar a resposta com as notícias da casa que o rei não sabe (o 413 semanal; a Almision ofendida que foi embora no 414; as missões; o Fumigador no 417).
- TICK 416 rodado (tick_416.txt): evento local MK16 [3] FALTA FERRO em Levis (110) · EVENTO DE MUNDO: 'a coberta afina' + Vingança (ler quando aparecer) · o Maneus avistado (longe) · CE16 [2]: o CELOCUS desabou a boca da passagem do ADUREL em Zisrir (fiel; chegou a Levis) · rota fechada no brejo do oeste (notícia no 422) · notícias: o Isyzis atrai monstros acima de Levis (fiel) · os Fiéis do Doge Velho dão um passo · alguém grande passou a proteger a Moeda Velha · trama Isolda → Almision: o gesto dela foi a pergunta pela maga · faíscas guardadas: [Naera deve a vida à Almision] · [Naera encomenda peça ao Gorine] · [Leliel acusa o Braeth].
- A Bigorna Livre de Levis pede audiência (#281, atrasada): o rei está em Levis: pode receber.

## RESPONDIDO (416 → 421): 1c · 2a · 3 (a posição: perdoar tudo por porcentagem baixa) · voltar à capital
- BRm [1]: a Brara contrariada (−5). Ferro de Levis 95. Vaduar +0,5 kg (com o rei); os 300 kg da coroa descem de barca (declarar a chegada; o laço da semana do 420 é um MOMENTO com a BRARA: usar na barca do ferro, com um recado dela).
- TICKS 417-421 rodados (tick_417 a tick_421). EN17 [5] CR17 [2] o caçador passa ao largo · EN19 [4] RF19 [5] 35 refugiados da ala do cais de Levis (descem para Ireviel) · EN20 [4] refugiados da enchente · MM17 [1] a Mamiltia partiu no 417 com o Fumigador · 418 AUDITORIA: avisos velhos · 420 SEMANAL: DS20 a ENCHENTE no bairro dos refugiados (grande; 11 mortos; Ordem −1 e Dinheiro −1, mod 2 semanas) · CZ20 [1] 'o rei necromante' na Fornalha · NL20 [6] o decreto dos barcos da Nouliel contestado pelos barqueiros · o leito do Mivor pronto (Defesa +1 mod) · a contra pegou 4 agentes (Liga, Descalços, Lumine, Clã do Hrotgar) · chegaram 2 pelo chamado (gerar ao receber) · livro 420: cofre 26.648 (+100 da Chama: 26.748).
- SURPRESAS DOS NPCs (413 e 420) ROLADAS no envelope (SURP 413/420): interpretar quando cada um entrar em cena. Já usadas: o GRAUR [6] um culto mostra o sinal = o dente do Xaathis na poterna. Também em aberto: os PROBLEMAS do Ouvald (segredo quase vem à tona), do Odrum (coração), do Dolassi (roubado), do Mormir (com a lei); os FEITOS do Eiagrir, do Tuald, do Skarkek e do Ulounn (trazem informação; declarar qual); o TALENTO de Farenta; os ACHADOS de Marasar (413) e de Levis (420); as audiências pendentes: a Bigorna Livre (#281) e os Sem-Torre (#332).
- CORREÇÃO DE DADO: o Pelaccino estava morto desde o 344 e a trama dele com o Graur rodava; fechada; tirado dos presos.
- (OCULTO) o Celocus: no 420 o MEDO dele (a prisão) aparece: foge, se esconde ou faz algo desesperado (notícia no 423); no 421 a ambição avança (notícia no 422). Os conselheiros da Liga souberam o segredo [3] (a Mãe Verde) no 413.
- LM421 (sondagem): C 4 (Nouliel, Graur, Sira, Herkald) · A 2 (Thuron, Tolvane) · B 2 (Eliane, Isolda); o Thuron magoado (lealdade 5/10).

## RESPONDIDO (421 noite): 1a,b · 2, 3c, 4 ao conselho · 5 o reino é a prioridade
- ES421 (A, desempate), AG421 (C 4-3-1; a Isolda lealdade 4/10), BC421 (A, desempate). Interrogatórios: AGq1 [3] AGi1 26 AGn1 [3] Draek · AGq2 [3] AGi2 22 AGn2 [5] Yeane (novo, 51) · AGq3 [4] AGi3 15 · AGq4 [4] AGi4 12 · AGi5 29 AGn5 [6] a SELINE.
- O TOLVANE a Lumade (TV22 [4] o Hruthos e 6 lanças; viagem.py: chega no 432). Regras da estrada e da negociação DECLARADAS no envelope (TVL): Lumgal ~428 d6 1-2 o líder do Xaathis; a negociação com o Celocus pela XXIII.25.
- O TICK DO 422 AINDA NÃO RODOU (a parada é na noite do 421).
- Apagados os mods 'a conquista' vencidos (Levis 332, Farenta 356).
- AS IDEIAS DO CONSELHO (nenhuma escolhida ainda; custos e efeitos ditos ao jogador; a REGRA G7, a Série de Ofício, só entra se o rei escolher uma série de ferramentas):
  1 GRÃO PARA MARASAR (Krernos): 2 barcas, 800; Comida de Marasar +1 (mod, duas semanas); 1 dia de rio.
  2 PICARETAS PARA AS MINAS DE BAIXO (Herkald e o Gurka): Série de Ofício, uma semana da forja grande; 60 picaretas e marretas Raras; 240 kg do ferro da coroa; 600 (metade paga por Levis); minério 2d6×10 → 3d6×10 por semana e Saúde de Levis +1 (mod, até o inverno).
  3 FERRADURAS E EIXOS (o Graur): Série de Ofício, uma semana; 300 ferraduras e 20 eixos; 400; a hoste montada e as caravanas um dia mais rápidas na estrada do rio; Defesa de Ireviel +1 (mod, até o inverno).
  4 O BAIRRO NOVO NO ALTO E O DIQUE (a Nouliel e a Eliane): obra do reino, 4.000 → 3.200 pela G6, 21 dias, os forçados trabalham; Saúde +1 e Ordem +1 DE VEZ em Ireviel; fim do risco de enchente ali; o rei pode bater a comporta (uma noite).
  5 CAIXAS DE FÍSICO (o Thuron): o rei bate as lâminas numa noite; 12 caixas; 500; Saúde +1 (mod, até o inverno) em Ireviel e em Levis.
  6 RASGAR EM PRAÇA AS DÍVIDAS PEQUENAS DE LEVIS do livro do Ardenghi (a Sira): 0 de ouro; precisa de alguém em Levis (a Brara ou um enviado); Ordem de Levis +1 (mod) e o culto do Xaathis perde a promessa (rolar o efeito no culto).
  7 ANZÓIS, CHUMBADAS E ÂNCORAS PARA FARENTA (a Isolda): Série pequena; 300; Dinheiro de Farenta +1 (mod, até o inverno).
  Limites: a forja grande faz UMA série por semana (2, 3 e 7 disputam as semanas; a série de armas da semana não sai); o rei bate UMA obra por noite (a comporta do 4, as lâminas do 5).

## RESPONDIDO (425): 1b morte · 2b o rei caça o Morek · 3a o Thuron · 4a o Teraseth · 5c as duas audiências
- EP24 sentença: MORTE (legit 10/10); cumprida pela Eliane ao amanhecer do 425.
- CP24 [1] Raro → gerador: 'Varula' (bate em Varogh) → NEANE (Raro 62, Sombra) · LN24 luta.py: morto na 1ª rodada (ERRO DO MESTRE: 'acoes':1 por cima da lei; não mudou o desfecho) · DR24a [3] 5 kg draek · DR24b [1] eryra · DR24c [1] sangue de Sombra · XP 620.
- TICK 425 (tick_425.txt): local briga na feira; Eliane de alta; o mundo: lugar novo VEYOL (Gogrunn, notícia em 5 dias); o Ceduion (reitor de Telosus) compra/toma/destrói algo da Obra (notícia 429); notícias: Quneus deixa drop em Mordun · FENRON caça perto do brejo (FIEL) · festival nas Montanhas de Fogo; faíscas ocultas: Eiundunn esconde um filho do Ardenghi (fome) · Herkald sonha com Gorra (sal) · ULURVE CHANTAGEIA AELIAE (uma receita perdida).
- LM25 O MOREK (sims/morek_425_saida.txt): SU25 [5] acordou · TR25a/b 26 de fogo · luta: o grupo cai em 4 rodadas · MORTOS Isolda, Starkald, Goir · Moreth PARA SEMPRE (455), Eiagrir GRAVE (442), Ferir LEVE (427) · PF25 [1] PF25c [3] ele leva o Goir · PF25b [4] PF25d [1] as barcas trazem a Isolda · DZ25: o rei pega a febre (15 vs 22), o Moreth e o Eiagrir não · FC25 [14] o físico cura a febre · XP 1.220 (rei, Moreth, Eiagrir) · PV do rei 11/398.
- TH25 [5] o Thuron não lê a letra.
- luta.py: o REFLEXO 18-20 passa a rodar (cópia luta_425_backup.py); o rei sem 'imune_empurrao' contra a raiz (prende, não empurra).
- reino: Ireviel Ordem −1 (até o 439); Saúde +1 (caixas, até o 480).

## RESPONDIDO (426, segunda vez): 1 'corrigir tudo e simule de novo, de um jeito de isso não acontecer de novo'
- ANULADA a LM25 e o que nasceu dela (ver o envelope). Ficam: o Neane, TR25 (2414), SU25 [5], os ticks 425 e 426, os Sem-Torre (despesa 7.700), o arado Mítico, BR26, CX26, PE26, AL26, MM25, os recados.
- REGRA G9 escrita no protocolo; combate.py (conferência e conferido=1; cópia combate_426_backup.py); luta.py (vários feitiços em 'magias'; ⛔ G9 no fim; cópia luta_426_backup.py); fichas: Isolda (Toque do gorjal), Ferir (Toque e Chuva de Brasas), Moreth (Lança do Sol e Chuva de Brasas da espada), Eiagrir (Lança do Sol), feitiços desde a 1ª rodada.
- LM26 (sims/morek_426_saida.txt): o Morek FOGE a 467/2440 (moral [2]) · mortos o Starkald e o Goir · a Isolda GRAVE (447, manca) · EC26a [19] EC26b [14] os dois ERGUIDOS · EC26c [1] Starkald −1 Força · EC26d [10] Goir −1 Vontade · MF26 [3] rio abaixo para sarar · DZ26: só o Starkald pega a febre (4+12), FC26 [17] curada · XP 1.220 a seis · PV do rei 153 (114 + a noite).
- A reação da Isolda ao pedido de desculpas (IS25a [15]) vale de pé, na cama dela.

## RESPONDIDO (427): 1a voltar ao Morek · 2a,b o Bjorvunn e Alnesar · (pergunta fora do jogo: app ou Claude Code, respondida sem dado)
- BJ26 [16] BJ26c [5] BJ26w [6] → gerador: o ULMIR (drops renomeados) · BJ26k [6] sabe tudo · TS26 [19] a Tessal acha Alnesar.
- TICK 427 SEMANAL (tick_427.txt): local SURPRESA → NV27 [3] o FACIO, NV27b [2] caído · EV27 [4] a Eloune no lodaçal do cais afundado · LU27 [3] LU27b [4] a Lurentetta: aliança contra a Elaeva · facções (G8-D rodou: a Guarda do Pedágio NÃO DORME, força 2) · o Xaathis vence a Bigorna Livre (FIEL) · LIVRO −2.750 · ATRASO DE SURPRESAS DE NPC DO TICK (16, regra C: soltar uma ou mais por cena): Eliane, Ulurve, Brara, Brua, Kreine, Veyula, Selvil, Tedulteth, Groa, Donione, Starkald, Vrethur, Tuald, Gerva, Ulounn, Hassa (gerador novidade cada, quando entrarem em cena).
- FD27 [14] a água rasa (+2 Defesa) · LM27 (sims/morek_427_saida.txt): 955 → 96 numa rodada; moral [1] foge · FG27 (aberto.py oposto): 24 contra 61, FALHA FEIA: O MOREK MORRE · DR27 3/6/3/3 kg · DZ27E 27 (o Eiagrir não pega) · XP 6.100 a quatro; 6.000 da missão ao rei → NÍVEL 155 · COFRE +3.000.

## RESPONDIDO (427 noite): 1a aceitar a aliança antes de ouvir o preço · 2 'avaliar o que seria mais proveitoso a nós' · 3a Levis primeiro, Alnesar na volta · 4a o rei ouve o Facio
- ERRO DO MESTRE corrigido à mesa: a Lurentetta é MÍTICA (774), não Lendária. A obra dela e o LU27b juntos: a Elaeva matou o povo das salinas, a Liga deixou morrer.
- YV27a [1] LANÇAS · YV27c [6]+2 (a surpresa boa do saber do rei) = 20 lanças · YV27d [6] a guarda dela (80 a 110) e a campeã MIE (150) · YV27b [1] o preço: uma peça Lendária ou melhor · YV27e [2] uma ARMA, até o 487 · YV27f [5] o YAVOR nível 80 · tratado `lurentetta` vigente.
- FC27a [1] o Facio POBRE · FC27b [5] a Liga passou os nomes do livro à LELIEL · (OCULTO) FC27c [12] ele disse a verdade.
- G10 (pergunta 2): o REI forja EXTRAORDINÁRIO (57 vs 30): tudo e a pista do zeieth · a NOULIEL dinheiro FALHA FEIA (rolagem oculta à mesa: ela acha que o núcleo vale uns 5.000; a verdade, 3d6×3.000, está no envelope) · a ELIANE guerra FALHA. A escolha do núcleo segue com o jogador (pergunta 1 abaixo).
- CL27 [3] (a surpresa ruim do saber da Nouliel): TEMPESTADE no amanhecer do 428; a barca não sai (+1 dia) · EL27 [1] (a surpresa atrasada da Eliane, G8-C): nasce OS RENDIDOS DE MARASAR (força 4, hostis). A fila de surpresas atrasadas do tick cai para 15: Ulurve, Brara, Brua, Kreine, Veyula, Selvil, Tedulteth, Groa, Donione, Starkald, Vrethur, Tuald, Gerva, Ulounn, Hassa.
- Faísca usada: o Mormir (Sem-Torre) e a Seline (só a imagem: ele junto da banca fechada dela, com um papel queimado; a traição pela receita perdida segue no envelope).

## RESPONDIDO (428): 1a a ARMADURA Mítica de Espinho com o zeieth (falta para quem; antes o rei quis saber das armas e armaduras: fato da ficha, sem dado) · 2 conselho (o Facio) · 3a,b avisar os Barqueiros e a Skotha, e a Sira · 4a o Rendido vai · 'precisamos de mais núcleos'
- ERRO DO MESTRE (G9): a ficha de combate da Eliane trazia na Lança do Bren os efeitos da Lança de Vestrin; corrigida em fichas_combate.json. No LM27 o +7 dela não pesou; no FG27, sem ele, a fuga segue falha feia: o Morek segue morto.
- CF28 o conselho: B (teto e trabalho; 3 a 3; a Intendente) · tick 428: Ireviel limpo depois da trovoada; o rio NORMAL; MUNDO [1] uma cidade se rebela em MARASAR (notícia no 430) · IR28 [3] · TR28 [6] → novidade [7] → TF28 [2] os DO CROQUE, TF28b [1] (o TR28b não vale) · JS28 [6] → novidade [3] → JS28s [3] o GIUNN (GI28 [4]: 35) · FB28 [6] → novidade [7] → FB28s [2] os DA BRECHA VELHA · LC28 [3], LC28n [4] = 20 · OP28 [4] · FE28 [1] · BL28 [3] · SR28 [1]+8 = 9 (o SR28b não vale) · (OCULTO) TE28 [4]: o Teraseth caça a Eloune no 432.
- Auditoria do 428: o conferidor sem aviso novo de cânone (a linha 753 do diário é o contrato falso do Quthemnus; Hassa/Kassa e Neane/Yeane são gente diferente: marcados em conferidor_visto.txt) · os forçados seguem 87 (G6 vale) · o tick não grava tick_N.txt quando a saída vai para arquivo: o tick_428.txt foi copiado da saída inteira.

## RESPONDIDO (428 noite → 430): verificar o nível do NPC · aumentar as defesas · 1a a armadura ao Moreth · 2a,c a Isyzis e o Bruur · depois de Levis, a Eloune · planos para os monstros · 3c · 4a · 5a
- FORA DO JOGO: o Graur subiu certo (70→75; um por tick); a ficha de combate dele acertada (combate.py poe); o `cresce.py ver` quebrava com as 3 fichas sem nível (Girendino, Lile, Gicilla): corrigido para mostrar 0.
- DEFESA: obra do reino 'a muralha do rio e as torres de vigia' (2.800 com a G6; pronta no 449; Defesa +1 de vez) · REGRA G11 escrita no protocolo (8 postos; despesa 8.100) · o plano no campanha_cacada.md.
- BR28 o conselho: A, a terra aos Filhos da Brecha (5 a 1) · GI28b [4] o convite do Giunn · TI28 [3] a Tilde pergunta por quê · LC28v [4] os voluntários nível 10 a 20, na Guilda · GR28 [5] (a surpresa atrasada da GROA, novidade [10]) o homem das guildas de Steunn · (OCULTO) GR28b [4] uma medida ou um desenho da Fornalha (agenda 431).
- OB428 (obras/couraca_espinho_moreth_428.txt): soma 114 · [9]+[1] → Mão que Não Treme, Alma Ouvida, Fortuna → 142 · TETO do núcleo Único: MÍTICA +1 efeito · XP 10.000 → FERIR 156 · ajudantes 2.500 (Tilde, Iorin, Herkald, Groa) · Fortuna 2/3, Revés 4/6.
- 429: tick (Loula: LO29 [2] um coveiro fora do portão) · MR29 (OCULTO) [1] a revolta de Marasar é dos FIÉIS DO DOGE VELHO · SK29 [3] a Skotha pede o Facio · SB29 [5] a SOUANE pôs a BRARA sob a proteção dela, em praça, em Levis (a casa sabe quando o rei chegar a Levis) · as partidas (o viagem.py leu 6 dias a pé: corrigido para a barca) · a série de Farenta (Dinheiro +1 até o 480).
- 430: tick em estrada · EN30 [5] a barca da Liga · LB30 [5] · (OCULTO) LB30c [5] ouro e papéis · LI30 [1] · MM30 [4] a pena da Mamiltia · GB30 [7]+2 = 9 · LN30 [1] · TH30 [4] · (OCULTO) IZ30 [1] · (OCULTO) FA30 [1] o SYESS (gerador; o nome Veyssa trocado) · FAÍSCA: o Ceduion vende à Leliel (a carta, oculta, nos papéis da barca).

## RESPONDIDO (430 → 432): 1c deixar a barca da Liga passar, recado à Sira · 2b SÉRIE DE MESTRE 2 · 3a manter os 8 postos · pergunta fora do jogo: as guildas do mundo (o Mestre propôs a G12; espera a aprovação)
- SÉRIE DE MESTRE 2: renda_casa 3.960, despesa 8.280 (ficha.py fixo).
- 431: LB31 [3] · VX31 [2]+2 = 4 (a vigia falhou) · (OCULTO) GR31 [3] a Groa passa a medida · HG31 [6] → novidade [2] monstro novo nas Fundas (RIUNN, Incomum 14) · LV31 [6] → novidade [9] um NPC antigo volta mudado (em Levis) · a pressão encheu (G8-A).
- 432: BR32 [3] · (OCULTO) TE32 [19], TE32p [6] · MR30 [4] · PM30 [5] · ST32 [2] os Caçadores Livres · (OCULTO) CL32 [6] → novidade [1] o hadun · o vilão ZEAZHIS.

## RESPONDIDO (432 noite → 433): 1 'quero entregá-lo, ele não vale tanto assim' (a letra b dizia recusar: valeu a palavra: ENTREGAR) · 2b acabar com a revolta já, ao lado da Skotha · 3a a G12 aprovada · pergunta fora do jogo: D&D e o Satisfy
- Legitimidade 10 → 9 · CH33 [6] a Chama da Hoste vai · FL33 [1] os Filhos do Livro não vão.
- G12: GU1-GU6 (obras/g12_geracao.txt), GU1x-GU6x, (OCULTO) GU4h [6] não foi a Tocha Branca que feriu a Elaeva · GUIr [18] · guildas.py escrito e ligado ao tick semanal (depois das facções) · a regra no protocolo; CLAUDE.md e MESTRE.md: G1 a G12.
- 433: EN33 [4] · CE33 [1] · a contra identificou o cobrador · a auditoria (acima, no envelope).

## RESPONDIDO (433, meio-dia): 1a parar e revistar · 2 'pode aplicar todos' (o MOTOR 8)
- MOTOR 8: G13 a G22 no protocolo; luta.py (covil e lendárias, testado em cópia), masmorra.py, reputacao.py (partida no envelope), a exaustão na ficha; CLAUDE.md e MESTRE.md: G1 a G22; a cola do motor.
- (OCULTO) HC33 [4] o capitão da Liga (90) · RV33 [4] fala e suborna · SU33 [3] 1.500 · (OCULTO) CR33 [6] a carroça vai a um comprador do Delta · G10 notar do rei: SUCESSO COM GANHO (a carroça; pesa como moeda; a estrada do sal).

## RESPONDIDO (433, tarde): 1d perguntar e investigar; recusar o ouro; 'se ele tiver o direito, não mexo um dedo'
- A lei (fato da ficha): o rio fechado à Liga (255, 260), a paz caída (339), a lei do 323 · CA34 [2] o capitão diz a verdade em parte · G10 gente do rei EXTRAORDINÁRIO (e a surpresa boa: Levis +5) · G10 notar da Eliane SUCESSO · (OCULTO) PP34 [5] a arca na popa · LP34 [1] os Devolvidos · FC34 [5] a carroça na estalagem.

## RESPONDIDO (433, noite): 1a prender e tomar pela lei; 'por que se arriscar?' · 2a tomar a carroça · 3a ler a carta
- AR35 [1] rendem-se · PG35 [4] o dinheiro (o triplo) · CT35 [4] · AR35b [5] · CR35 40 × 23 · QB35 [6] rendem-se · (OCULTO até abrir) OU35 11 × 500 = 5.500 (confisco) · LT35 [5] cifra · G10 magia EXTRAORDINÁRIO · LC35 [3] · FE35 [1] o SAL · QF35 [4] os olhos da Mamiltia · a Leliel → forquilha 1/4 · a Eliane +1.400 e exaustão 1.

## RESPONDIDO (434): 1a julgar em Levis · 2c o sal à Mamiltia e à Lurentetta, o segredo e a carta guardados, cobrar o Ceduion
- O tick semanal do 434 e tudo o que veio dele (no envelope). O julgamento LV34 (provas e testemunhas; balança +10).

## RESPONDIDO (434 noite → 435): 1b trabalho forçado aos 32 · 2c o ouro em pão e físicos e a guarda com a Brara · 3b a Isyzis depois de Levis
- LV34 sentença (legitimidade 10) · G6 119 · cofre −5.500 · Levis Comida 2 (+1 mod), Saúde +1 mod · OR35 [20] natural → a Tigra; Ordem 1 · BR35 [1] a partilha · BG35 [6] → Zythir · BT35 a batalha (oculta até o 436) · PD35 [3] · CF35 [6] · FC35 [2] · os recados (441, 438/440, 453).

## RESPONDIDO (435 noite → 436): 1c direto a Farenta, a pena quando a fera chegar · 2a a fundição à Brara · 3a Zythir já e o registro à Bigorna
- BR36 [4] · CA36 [1] · (OCULTO) EZ36 444 · ZC36 [4] Único · a senha (EXTRAORDINÁRIO) · (OCULTO) ZP36 [1] o prisioneiro é o rei Tuir · AL36 [3] a Tigra · LZ36 a sala 1 (o ERRO da ficha do rei corrigido: o Gibão) · TZ36 [18] · PA36 [3] o elmo · o tick do 436: MG36 [3] o Loula, QS36 [3] um Sem-Torre some, (OCULTO) MM36 [1].

## RESPONDIDO (436 → 437): 1b sair, dormir e voltar · 2a o elmo a um da guarda · a pergunta fora do jogo: a janela de contexto
- CB36 [2] o cabo GONDE (30) · o tick do 437 · o notar EXTRAORDINÁRIO (o favor do eco) · SZ37 [2] · WZ37 [3] a Primeira Liga · HZ37 [1]+2 · TZ37 [5] a rainha.

## RESPONDIDO (437, a sala 3): 1a a porta da sala 4 · 2a o favor do eco (o caminho seguro)
- SG37 [2] a passagem que contorna a sala 5.

## RESPONDIDO (437, a sala 4): 1b com condição: 'pergunte se conseguimos vencer fácil; se não, vamos ao tesouro'
- TU37 [4] o eco é nível 160 · a régua OCULTA (sims/zythir_s5_regua.txt): o Huir morre em 100%, ninguém morre, o rei cai em 2% · o saber do eco (guerra média): 44 vs 25, GANHO: 'é fácil' e 'o golpe procura o mais fraco: o rei' · LH37 a luta: o Huir cai na 1ª rodada · TC37 [2] nada no covil.

## PERGUNTAS ABERTAS (o jogador ainda NÃO respondeu; esperar a resposta antes de rolar)
1. ZYTHIR, A SALA 6 (o TESOURO): a) entrar, pegar o tesouro e sair hoje (Farenta no amanhecer do 438, como está) · b) entrar e seguir hoje: a 7 (o eco guia) e a RAINHA na 8 (com o rei a 84/402; se alguém sair ferido, a saída para Farenta atrasa) · c) outra.
2. A CARTA DO TOLVANE (o Celocus calado e a carga de HADUN à venda em Lumade): a) o Tolvane compra uma amostra e descobre de onde vem a carga · b) o Tolvane pergunta ao Celocus, sem comprar · c) deixar quieto por ora.

## Regras do jogador em vigor
- Formato: ⏳ PENDENTE · 🕰️ RELÓGIO · 🎲 ROLAGEM · 🎭 CENA · 👁️ O QUE VOCÊ VÊ · 🏙️ CIDADE E FORJA · 🧵 FIOS · 🎯 PERGUNTAS · 📊 ESTADO · 📜 REGISTRO. O jogador responde "1a.2b…"; "conselho" quer dizer que o conselho decide por voto.
- Dado só de script, com a tabela declarada no envelope ANTES de rolar.
- Sem régua, a não ser pela VISÃO DO TEMPO (2 por dia; mostra 1 hora). Fora disso: "deixe eu me lascar e só pergunte".
- Tom: medo, emoção, imprevisibilidade; conquistar por merecer. Objetivo: eliminar a Liga de vez (mortos, presos ou servindo) e levar alguns inimigos a ZERO.
- Blocos longos: rodar os dias até a próxima decisão de verdade.
- A casa só trabalha vaduar A FRIO. Teto do mundo: 15 Lendários · 3 Míticos · 3 Primordiais.
- Tentar encantar toda peça forjada, com a Visão antes. Mítica pede núcleo (ou um ano de vida do ferreiro); sem isso o teto é Lendário (3 efeitos e a magia, pela ordem rolada).
- O conselho vota; TUDO PASSA PELA INTENDENTE (a Nouliel desempata). Julgamentos vão ao conselho logo depois das batalhas.
- Modo de morte REALISTA.
- Nada de zip a cada turno: só quando o jogador pede.
- Reler o motor e rodar o conferidor a cada 5 dias (o próximo é no 408).
- Avisar o jogador de toda mudança de regra.

## Motor 7.1 e 7.2 (aprovados pelo jogador no 400)
- 7.1: o conselho.py conta votos vencidos SEGUIDOS (3 seguidos = −1 de lealdade; zera quando a cadeira vence). O batalha.py tem o bônus de 'surpresa' na 1ª rodada.
- 7.2: G1 Guilda dos Aventureiros (abre no 412; o Starkald) · G2 Guilda dos Mineiros (Levis, abre no 409; o Gurka) · G3 recrutamento (20 lanças no 423; o chamado rola d20+3; quem entra pede peça Rara+) · G4 cura de 1/10 do PV por noite · G5 estoque da cidade (400 por semana desde o 406).
- G6 (406): o desconto dos forçados: obra NOVA do reino a quatro quintos enquanto pelo menos 44 dos 87 servirem (protocolo_do_turno.md).

## Ainda não processado (não esconder do jogador)
- AUDITORIA DO 408: as surpresas da semana do capuz 4, do Kreine, da Carea, do Vrethur e do Dotocci; o conferidor; reler o motor.
- (OCULTO) o HIALD é homem do Borecci; a ordem é LEVAR A TILDE A STEUNN; nunca machuca uma criança. Está nos infiltrados (furt 4): o tick diário o rola contra a contra-espionagem 35.
- Agenda: 407 os Jurados de Steunn pedem audiência, aviso dos Fiéis do Doge Velho, a rota da costa fecha, a Mão Queimada de Telosus manda gente a Ireviel · 408 obras de Farenta prontas · 409 prazo da Mamiltia e a casa dos Mineiros · 411 as missões · 412 a Guilda dos Aventureiros · 413 tick semanal · 414 a Almision · 423 as lanças e Levis Saúde +1 · 429 a peça tem de chegar à Higrunn · 433 o Celocus paga · ~480 a caçada da Elaeva com a Mamiltia.
- As peças do Rindald e do Fabaino (dentro de uma lua).
- Subida de nível de Ferir (144): +2 atributos (Int +1, Afinidade +1), PV +2, Mana +1, Foco +1 a cada 5 níveis; pontos no 144/147/150; talento no 150.

## Notas técnicas
- `selo.py lote`: ID repetido ou buraco na tabela faz o lote inteiro ser recusado CALADO (o grep não mostra nada).
- `reino.py projeto` não cobra: cobrar com `ficha.py cofre`.
- `gerador.py material` pede "Raro" com maiúscula.
- Nome gerado que não está no Livro fechado vira o mais próximo do compêndio.
