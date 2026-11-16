> **MOTOR 6.1 (Dia 379) — VALE ANTES DE TUDO ABAIXO.** Para retomar: `python3 contexto.py`, ler o `BRIEFING.md` (o painel) e o `MESTRE.md`, e depois a matéria de fundo (cânone, regras, estado, último bloco do diário). O jogador quer detalhe primeiro. Onde este texto mandar declarar a tabela no envelope e depois rolar, usar `selo.py` (ele escreve as duas linhas). Onde mandar rodar `reino.py semana`, não rodar: o tick semanal já roda, junto com o clima, as facções, os relógios e o livro. Correr dias: `tick.py bloco N` (saída inteira). XP e cofre: `ficha.py`. Conselho: `conselho.py`. A lista do que mudou: `MELHORIAS_v6.md`. As regras do jogo e as regras do jogador continuam as mesmas; as camadas novas (clima, facções, boatos) estão descritas lá.

# SAVE DO FERIR — SATISFY (Motor de Mundo v5.2) — parado na MANHÃ DO 336 (antes do tick 336: a lei contra a Mamiltia e o Erymir esperam o rei; a barca da zeieth chega ao Delta ~338). NOVO: reino.py (gerenciamento das cidades e do reino; rodar `python3 reino.py semana N` no tick semanal e `python3 reino.py estado`)

Este pacote é o save inteiro da campanha solo de Ferir, com o Claude como Mestre.
Tem tudo: regras, ficha, diários, envelopes (as rolagens ocultas), NPCs, mundo, os scripts dos dados e as ferramentas de conferência.

## Como continuar em outro chat
1. Num Projeto do Claude (o mesmo "save" ou um novo, em qualquer conta), suba **todos os arquivos** deste pacote para o conhecimento do Projeto: os da raiz, a pasta `arquivo_dia159/` (o atlas é o cânone secreto do mundo) e o PDF do Motor.
2. Abra um chat novo dentro do Projeto e cole a mensagem abaixo, trocando as reticências pelas suas escolhas.

## Mensagem para colar no chat novo
> Este Projeto é o save da minha campanha solo de SATISFY (Motor de Mundo v5.2). Você é o Mestre e escreve em português. Antes de responder, leia nesta ordem: `LEIA-ME_PRIMEIRO.md`, `protocolo_do_turno.md`, `canone.md`, `estado_vivo.md`, `regras_da_casa_dia199.md`, o fim de `diario_sessao2f.md`, o fim de `envelope_sessao2m.md` e `npcs.json`. Copie todos os scripts (.py), os .json, os `tick_*.txt` e a pasta `arquivo_dia159/` para uma pasta de trabalho e role os dados por eles, como diz o protocolo. Rode `python3 conferidor.py 259` e `python3 noticias.py 257 262` antes de narrar. Paramos no fim do Dia 259; a última resposta me deu as perguntas do bloco. Minhas escolhas são: ...

## Onde paramos
- **ATUALIZAÇÃO (blocos 260-266, chat novo):** o último bloco foi da noite do 263 ao fim do 266 (caça ao Murrask, a Lucissi, o tick semanal). ver o fim de `diario_sessao2f.md`, o fim de `envelope_sessao2m.md` e o topo dos Pendentes em `estado_vivo.md`. Cofre 1.414; o arvel na mão; a caça ao Murrask à espera da régua; a mãe do aprendiz quer a Lança do Bren; a Liga recusou e ameaça. Rodar `python3 conferidor.py 263` e `python3 noticias.py 263 268`.

## Onde paramos antes (fim do Dia 259)
- **Ferir:** NÍVEL 76 (XP 289.759; o 77 em 292.700; o 78 traz 1 ponto, que vai para Encantamento). Int 105 · Afin 91 · PV 242 · Mana 84 · Magia Mestre · Encantamento 69 (81 com condutor de Hamir) · Forja 63. Ama a NOULIEL (par desde o 218).
- **Ireviel** (a casa é o governo): Comida 4/4 · Comércio 4/4 · Dinheiro 4/4 · Saúde 2/4 (febre do brejo; quarentena no cais; a Tilde doente). Contra-espionagem 35 (teto 35, pelo OLHO DO LEVE). Cofre 7.264. Hoste ~110 com 18 Épicas.
- **O Plano do Leve:** a FORQUILHA do rio (logo acima de Ireviel) está FECHADA às barcas da Liga. A galé e 18 da Companhia da Skotha guardam; balistas prontas; a Corrente do Leve fica pronta no 264. A Liga ofereceu portagem; o conselho respondeu "sim, com condições" (+500 por semana e uma carta reconhecendo Ireviel senhora da forquilha). A resposta de Marasar chega por volta do 260.
- **Chegando:** o ARVEL (300 g, Mítico de fogo) no 263, pelo Ulurve; pagam-se 9.000 (o cofre e 2 Épicas guardadas). O ORAST chega a Steunn por volta do 262.
- **Perigos:** o MURRASK (Épico 85) ronda a quarentena · a ELAEVA (Mítico) está em LEVIS · os DESCALÇOS sabem da MATRIZ · o NAUDREN segue a galé · o Hrotgar, irritado pelo Orast.
- **O mapa** atual: "Quem manda onde — o mapa do rei, Dia 336" (artifact https://claude.ai/artifact/LAWqxKMXRYPEr98Se5FVFx); o arquivo é `mapa_dia336.html` (o velho, do 257, é `mapa_ireviel.html`).
- **O MANUAL DO JOGADOR** (doc, regras do Motor + regras da casa, sem segredos): https://claude.ai/artifact/Hg4RnB97y8Vikcea92RLqh

## As perguntas em aberto (a última resposta)
1. Caçar o MURRASK (a missão da Skotha, grau D, 5 dias; a Lumine quer o contrário)?
2. A LANÇA DO BREN: a mãe do aprendiz que o Bren matou pede como paga, e o Moreth jurou a ela.
3. O THUGEK preso em Levis: o Clã pede que Ireviel o tire de lá pelo rio.
4. A MATRIZ vazou para os Descalços: o que fazer.
5. O remédio da FEBRE DO BREJO: a Tessal, o Ouvald e a técnica do Delta.

## Como o Mestre trabalha nesta campanha
- **Formato da resposta:** primeiro a leitura das escolhas e os erros admitidos; subida de nível no topo, com a tabela de atributos; depois ⏳ PENDENTE · 🕰️ RELÓGIO · 🎲 ROLAGEM · 🎭 CENA · 👁️ O QUE VOCÊ VÊ · 🏙️ CIDADE E FORJA · 🧵 FIOS ATIVOS (até 7) · 🎯 PERGUNTAS DO BLOCO (até 5) · 📊 ESTADO (com Laços) · 📜 REGISTRO.
- **Dados soberanos:** rolados por script e mostrados crus; tabela declarada no envelope ANTES de rolar; tabela condicional só depois da condição; SURPRESA no 20 natural, por cima do resultado alto.
- **Modo de blocos:** muitos dias por resposta, parando só em decisão do jogador, luta grande sem régua aprovada ou coisa irreversível.
- **Forja e encantamento:** mostrar a dificuldade ("preciso de tanto, tenho tanto" e o que se arrisca) e, com a ordem do jogador, executar. Feitiço só da lista que cabe no tipo da peça.
- **Conferir antes de narrar:** ler o `canone.md` no começo de cada bloco; `python3 confere.py TERMO` antes de usar um fato antigo; `python3 conferidor.py DIA` a cada 5 dias (dias de auditoria: 263, 268…) junto com `python3 noticias.py A B`. Erro achado vai para o cânone e para o envelope (regra 14).
- **Nomes:** o gerador repete prefixos (Kas-, Sel-, Or-, Lum-, Bra-, Vey-, Gor-). Todo nome novo passa pelo `confere.py`; se for parecido, troca.
- **Zip** só quando o jogador pedir.

## O que é cada arquivo
- **Ler primeiro:** `protocolo_do_turno.md` (o turno do Mestre) · `canone.md` (fatos conferidos que não podem ser contrariados) · `estado_vivo.md` (a ficha de Ferir, da cidade e dos pendentes; o mais novo em cima) · `regras_da_casa_dia199.md` (regras e decisões permanentes do jogador, incluindo as Políticas de Ireviel).
- **`diario_sessao2*.md`:** a história, de 2 até 2f (o 2f é o atual).
- **`envelope_sessao2*.md`:** tabelas declaradas e dados rolados, ocultos para o jogador. O atual é o **2m**.
- **`npcs.json`:** todos os NPCs (nível, XP, traços, log).
- **`mundo.json` e `mundo_vivo.json`:** o mundo (Lendários, monstros, facções, tramas, espionagem, vilões, presos, notas ocultas).
- **`estado.json`:** o relógio do tick (Pressão, cobiça).
- **Ferramentas de conferência:** `confere.py` (procura um termo em todo o save) · `conferidor.py` (a conferência de 5 em 5 dias) · `conferidor_visto.txt` (avisos já resolvidos) · `noticias.py` (as notícias marcadas pelos ticks para cada dia).
- **Scripts de jogo:** `dado.py` · `aberto.py` (teste de dois dados) · `obra_valor.py` (forja, encantamento, conserto, ajuste) · `luta.py` · `tick.py` (o dia do mundo) · `mundo.py` e `mundo_vivo.py` · `semana_npc.py` e `cresce.py` (a semana e o XP dos NPCs) · `feiticos.py` (o grimório) · `gerador.py` (NPCs, monstros, materiais, lugares, missões, SURPRESAS) · e também `nomes.py`, `obra.py`, `obra_aberta.py`, `obra_dado.py`, `tistir.py`. Os `*_d1_backup.py` são versões antigas.
- **`tick_*.txt`:** a saída de cada tick (o `noticias.py` lê daqui).
- **`sims/`:** simulações de luta usadas para declarar régua.
- **`mapa_ireviel.html`:** o mapa do que Ferir sabe (Dia 257).
- **`arquivo_dia159/`:** o save original do Dia 159; o **atlas** (cânone secreto) e o envelope velho. Os scripts acham o atlas nesta pasta.
- **`SATISFY_v5.2_Motor_de_Mundo.pdf`** e **`SATISFY_v5.2_Motor_de_Mundo_texto.txt`:** o livro de regras (o texto serve para buscar regra).

Observação: alguns arquivos citam caminhos como `claude/estado_vivo.md` ou `../pacote/`. No Projeto novo eles ficam na raiz, e isso não muda nada.

## LIVRO DO MUNDO (Dia 356)
- Página: https://claude.ai/artifact/MKdgpHtXtSbhJTUvCvPvEe (mapa do continente, mundo, classes, grimório 1º-9º, talentos, materiais, bestiário). Fontes em compendio/; refazer com `python3 compendio/build_livro.py`.
- Camada secreta: compendio/segredos_do_mestre.md. O Mestre não inventa fora do livro.

## COMO CONTINUAR EM OUTRO CHAT (Dia 379)
- Comece por RETOMAR_DIA379.md.

**MOTOR 7 (Dia 396):** leia também RETOMAR_DIA396.md, ESTILO_NARRATIVO.md e MELHORIAS_v7.md. Scripts novos: tracos.py, habilidades.py, classe.py.

**DIA 406 (motor 7.2):** comece por RETOMAR_DIA407.md (substitui o RETOMAR_DIA396.md): onde paramos, as 4 perguntas abertas e as regras em vigor. Envelope atual: envelope_sessao2n.md.
