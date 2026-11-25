# MESA · a criação · Dia 1, manhã (8h) · primavera · ano 1218 do Reino de Belogar

**O mundo:** Belogar: 16 lugares de povo (9.895 pessoas em número), 156 com nome, 40 aventureiros rivais, 8 masmorras, 825 anos de história.
O personagem ainda não nasceu. O jogador escolhe o povo, o berço e a inclinação (e diz o nome); o dado do mundo faz o resto, uma vez.

OS POVOS (o povo muda os atributos, com a soma igual, e dá os traços; só o humano tem a segunda inclinação):
  a) humano: a medida de todos: nada a mais, nada a menos
  b) anão: duro, teimoso e de vista curta; vê na penumbra das minas, e o veneno o pega pela metade
  c) elfo: leve e de olho longo, frágil de corpo e de pouca paciência; vê na penumbra
  d) meio-orc: forte e de sangue quente; vê na penumbra, como o pai orc
  e) pequenino: miúdo, rijo e sem medo: o pavor pega pouco nele, e anda sem ser ouvido
  f) gnomo: miúdo, curioso e de mão fina; vê na penumbra, e o mecanismo não tem segredo para ele

OS BERÇOS (a família onde você nasce: o lugar, o ofício, os parentes, o que você leva):
  a) da casa dos Dorneles, Filipa (ferreiro) em Pedra Velha; parentes vivos: Berareu — cresceu na forja da família; tem a mão de Iniciante no martelo e na forja · leva: martelo Comum, couro Comum, 30 de prata, 4 de metal Comum, 2 de madeira Comum
  b) da casa dos Amado, Teresa (caçador) em Castro Real; parentes vivos: Erarina — cresceu no mato com a família de caçadores; tem a mão de Iniciante no rastro e no arco · leva: arco Comum, adaga Comum, couro Comum, 20 de prata, 3 de comida
  c) da casa dos Mota, Terinada (guarda) em Ribeira da Névoa — cresceu na casa da guarda; tem a mão de Iniciante na espada · leva: espada Comum, escudo Comum, malha Comum, 30 de prata
  d) da casa dos Pardo, Fausto (mercador) em Vale do Corvo — cresceu atrás do balcão da casa de comércio; tem a mão de Iniciante no comércio e na adaga · leva: adaga Comum, couro Comum, 120 de prata, 4 de pano
  e) criado no santuário por Zeno (sacerdote) em Ribeira da Névoa — deixado no santuário quando criança, e criado lá; tem a mão de Iniciante na cura e na maça, e sabe a luz · leva: maça Comum, couro Comum, 10 de prata, 3 de erva Comum
  f) da casa dos Terigar, Orlando (senhor) em Várzea Brava; parentes vivos: Dalva — da casa nobre que manda no lugar; tem a mão de Iniciante na espada, a espada da família e inimigos que nunca viu · leva: espada Incomum, escudo Comum, malha Comum, 80 de prata

A INCLINAÇÃO (o caminho em que o dado do talento rola duas vezes e vale o melhor):
  a) fio: as armas de fio (adaga, espada, machado, montante)
  b) haste: as armas de haste (lança, alabarda)
  c) peso: as armas de peso (maça, martelo, malho)
  d) tiro: o arco e a besta
  e) forja: a forja
  f) couro: o couro
  g) caça: a caça
  h) coleta: a coleta
  i) comércio: o comércio
  j) cura: a cura
  k) alquimia: a alquimia
  l) encanto: o encanto
  m) manha: a manha (andar escondido, escutar, achar e desarmar armadilha, abrir fechadura)
  n) arcano: o arcano
  o) fé: a fé
  p) verde: o verde
  q) pacto: o pacto

## Perguntas abertas
1. Que povo? (o povo muda os atributos e dá os traços)  **a)** humano · **b)** anão · **c)** elfo · **d)** meio-orc · **e)** pequenino · **f)** gnomo
2. Que berço? (a família onde você nasce: `cria.py ofertas` conta cada uma)  **a)** da casa dos Dorneles, Filipa (ferreiro) em Pedra Velha; parentes vivos: Berareu · **b)** da casa dos Amado, Teresa (caçador) em Castro Real; parentes vivos: Erarina · **c)** da casa dos Mota, Terinada (guarda) em Ribeira da Névoa · **d)** da casa dos Pardo, Fausto (mercador) em Vale do Corvo · **e)** criado no santuário por Zeno (sacerdote) em Ribeira da Névoa · **f)** da casa dos Terigar, Orlando (senhor) em Várzea Brava; parentes vivos: Dalva
3. Que inclinação? (o caminho em que o dado do talento rola duas vezes)  **a)** fio · **b)** haste · **c)** peso · **d)** tiro · **e)** forja · **f)** couro · **g)** caça · **h)** coleta · **i)** comércio · **j)** cura · **k)** alquimia · **l)** encanto · **m)** manha · **n)** arcano · **o)** fé · **p)** verde · **q)** pacto
4. Se humano, a segunda inclinação? (outro caminho; quem não é humano responde "r")  **a)** fio · **b)** haste · **c)** peso · **d)** tiro · **e)** forja · **f)** couro · **g)** caça · **h)** coleta · **i)** comércio · **j)** cura · **k)** alquimia · **l)** encanto · **m)** manha · **n)** arcano · **o)** fé · **p)** verde · **q)** pacto · **r)** nenhuma

**Para nascer:** `cria.py nasce "1a.2c.3e.4r" nome=NOME` (os códigos das respostas), e depois `turno.py abre`.

## SÓ O MESTRE
- peça maldita: i0009 malho Raro (a praga da Mina da Névoa, Rara, insônia); quebra: devolver malho Raro ao lugar dela, no poço velho
- peça maldita: i0022 montante Comum (a praga da Toca do Sal, Comum, míngua); quebra: devolver montante Comum ao lugar dela, na sala dos presos
- a Fome da Serra (dragão ancião da serra, grau S) na câmara do tesouro: PV 1337 de 1337 · dorme até o Dia 421 (vigília 31, mais 2 por punhado; 0 tirados neste sono) · o tesouro: 1718 de prata; as peças: O Bordão da Serra · sem vila (caça no ermo) (`dragoes.py covil covil_dos_sinos_3`)
- o Brasa (dragão jovem da serra, grau C) nos Penhascos das Águas: PV 480 de 480 · ACORDADO · o tesouro: 474 de prata; as peças: O Gume do Inverno · a vila: Ribeira do Lobo (0 ataques) (`dragoes.py covil penhascos_das_aguas`)
- as frentes: f01 o bando de Sara na estrada (passo 0) · f02 a horda da toca do Souto das Águas (passo 0) · f03 os mortos da Cripta dos Miraves (passo 0) · f04 o dragão Brasa (passo 0) · f05 a ambição dos Astolan (passo 0) · f06 o cartel de Selina (passo 0) · f07 o culto de Moninho (passo 0) · f08 a corrida da Liga do Sino Rachado (passo 0) · f09 a seca de Pedra Verde (passo 0) · f10 a falta de sal de Castro Branco (passo 0) · f11 os sumiços da Charneca dos Sinos (passo 0) · f12 as luzes das Ruínas do Urso (passo 0) · f13 Fome da Serra, o que dorme (passo 0)
- a crônica tem 269 linhas (`historia` no mundo.json): as últimas: 1206: Taskin, dos anões, curou a peste em Várzea da Névoa com o que sabia do mato: todo o reino sabe o nome. · 1207: Morre Jorelada (num duelo); Gilela assume a casa dos Orirena. · 1211: Drastum, dos anões, achou o veio de ferro que fez a riqueza de Souto Negro: todo o reino sabe o nome.
- o estado está inteiro.
