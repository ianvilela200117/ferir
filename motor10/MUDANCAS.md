# MOTOR 10 — diário de mudanças

O livro de regras (`REGRAS.md`) não guarda história. Ela fica aqui: o que mudou, quando, por quê, e o que o banco de provas deu.

## Dia 507 (fora do jogo) — nasce o Motor 10
- **Por quê:** a revisão do motor (`../REVISAO_MOTOR10.md`) mediu que no motor antigo o nível vencia a arma. O jogador pediu: a arma decidir muito (uma arma dar chance de um nível 50 vencer um nível 500), fim do requisito por nível, o sob medida misturado com requisito por atributo, a luta parar e perguntar sempre que algo muda, e todos os módulos de combate.
- **O que entrou:** `tabelas.py` (todos os números), `itens.py` (o Livro de Itens e a janela do item), `pessoas.py` (a ficha que sai sozinha; requisito por atributo, sob medida, sintonia), `luta.py` (grupo contra grupo numa linha de casas; alcance, lugar, tempo, fôlego, golpe contra armadura, parte do corpo e ferida, durabilidade, moral, ordens e paradas), `provas.py` (o banco de provas).
- **A escala:** começou com a proteção SUBTRAINDO do golpe. O banco de provas reprovou: entre iguais de categoria alta a luta acabava em uma rodada. Passou a DIVIDIR: o que conta é a diferença de categoria entre a arma e a armadura, e o duelo entre iguais dura o mesmo em qualquer degrau.
- **Metas afrouxadas na calibração** (para o jogador confirmar): "só a arma uma categoria acima, mesmo nível" era 65 a 90% e ficou 80 a 99% (mede 93%); "mesma arma, nível 150 contra 50" era 80 a 98% e ficou 85 a 100% (mede 96%).
- **Banco de provas:** 28 de 28.
- **Falta:** a magia e os encantos de peça, os bichos, o ofício (forjar, consertar, a escada das categorias), o mundo vivo, o turno em dois comandos.

## Dia 507 (fora do jogo) — a arma mais forte ainda
- **Por quê:** o jogador viu o primeiro dial (uma arma duas categorias acima dava ao nível 50 28% contra o nível 500; três acima, 76%) e pediu "mais forte ainda". Também decidiu: **mundo novo, do zero** (o save do Ferir fica guardado como está).
- **O que mudou no `tabelas.py`:** cada categoria passou a valer o TRIPLO da de baixo (era 2,5 vezes); o bônus de acerto e de Defesa passou a +4 por categoria (era +3); a força do golpe passou a 0,03 por ponto de bônus (era 0,04); o PV passou a Vigor × 2 + nível ÷ 4 (era nível ÷ 2).
- **O que o banco mede agora:** uma arma UMA acima vence 100 níveis de diferença em 70% e dá 6% contra 450 níveis; DUAS acima dão ao nível 50 **59%** contra o nível 500; TRÊS acima, **86%**. Com a mesma arma, o nível 150 vence o 50 em 95% e o 75 vence o 50 em 52%.
- **Metas que mudaram** (seguem o pedido): as faixas das provas de arma subiram; entrou a prova "uma arma uma acima, 50 × 500" (2 a 20%). Duas provas de módulo foram afrouxadas por serem ruidosas: o alcance (as lanças têm de vencer nas duas situações, sem exigir diferença entre corredor e campo) e a moral (40% em vez de 50%).
- **Banco de provas:** 29 de 29.
