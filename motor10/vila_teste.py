#!/usr/bin/env python3
"""vila_teste.py — MOTOR 10: A VILA DE TESTE. Um mundo pequeno, FORA DO CÂNONE, para o jogador experimentar a luta, a caça, a forja e o custo de viver.

  python3 vila_teste.py PASTA [comeco=ferreiro|cacador|guerreiro] [nome=NOME] [semente=N] [inclinacao=CAMINHO]

Cria, numa pasta NOVA (recusa escrever por cima de qualquer coisa), tudo por eventos "gera":
  PEDRA RASA, uma vila de 400 pessoas: pousada, mercado (os bens no ponto do ano, 15 peças Comuns e Incomuns na prateleira, 2.000 de prata contada)
    e a forja da vila (oficina 1; o fogo e a bigorna servem até o Incomum);
  A MATA DO CORVO, o ermo vizinho, a 1 bloco, borda de floresta: corça, javali, lobo e urso; e, postas à mão para o teste, UMA pantera (o bicho raro: dá couro e osso Raros)
    e UMA serpe (o chefe: dá núcleo Épico). Para tirar, o que a tabela dá à borda de uma floresta (tabelas_caca.COLETA_TETO): madeira e erva Comuns.
    A matéria Incomum e a Rara só há do interior para cima: na borda não há;
  OITO PESSOAS com nome e ficha de luta (o ferreiro, a taverneira, a caçadora, o guarda, o lenhador, a curandeira, o mercador, o aprendiz),
    cada uma com os blocos de treino que explicam a mão que tem (a tabela de cada ofício e a das armas);
  e O PERSONAGEM do começo escolhido: nível 5, a mão de Iniciante no ofício dele, peças Comuns, 30 de prata.
  OS TALENTOS E OS DONS (etapa da magia): toda a gente da vila nova nasce com eles, pelo dado do mundo (talento.py). O personagem pode ter uma INCLINAÇÃO
    (inclinacao=fio, haste, peso, tiro, forja, couro, caça, coleta, comércio, cura, alquimia, encanto, arcano, fé, verde ou pacto): naquele caminho o dado rola duas vezes
    e vale o melhor. Ninguém sabe o que tem: o talento aparece fazendo, o dom quando decide um teste. O Mestre vê tudo no SÓ O MESTRE.
Depois: MOTOR10_MUNDO=PASTA python3 turno.py abre      (o guia está no GUIA_VILA.md)

  python3 vila_teste.py magia PASTA [inclinacao=CAMINHO]

ACRESCENTA a etapa da magia a uma vila de teste QUE JÁ EXISTE (o save de quem já joga), só por eventos, sem recriar nada (recusa rodar duas vezes):
  os TALENTOS E OS DONS de quem ainda não foi rolado (o personagem com a inclinação, se o jogador escolher uma); o MAGO VELHO (Anselmo, do arcano, cajado Incomum);
  a BOTICA DA CURANDEIRA (Nara passa a ter a mão de Iniciante na alquimia); o SANTUÁRIO com a CLÉRIGA (Lúcia, voto do socorro); A MAGIA NA LOJA (as poções, a água benta,
  dois amuletos, uma varinha, um símbolo e a Cartilha do arcano: mercado.funda_magia); a BRUXA da borda da mata (Joana,
  do pacto: lê, amaldiçoa e vende veneno de pessoa a pessoa); o GRANDE DOM DE FORJA DO ZECA, que ninguém leu; a COVA VELHA (um ermo novo, vizinho da vila, com
  esqueletos e corpos-secos, e uma peça maldita largada no chão); e A TOCA DOS GOBLINS na Mata do Corvo (um covil pequeno, com um tesouro miúdo).
"""
import os, sys
import tabelas as T
import tabelas_mundo as M
import tabelas_bichos as TB
import tabelas_caca as K
import tabelas_oficio as O
import tabelas_mercado as C
import estado, mercado, turno, talento
from itens import item
from pessoas import padrao

VILA = dict(id='vila', nome='Pedra Rasa', em='em Pedra Rasa', pop=400, oficina=1, fogo=1, bigorna=1)
ERMO = dict(id='mata', nome='a Mata do Corvo', em='na Mata do Corvo', habitat='floresta', perigo=1, longe=1,
            bichos={'corça': 80, 'javali': 40, 'lobo': 12, 'urso': 3, 'pantera': 1, 'serpe': 1})                              # a pantera é o bicho raro; a serpe, o chefe (dá núcleo Épico): as duas postas à mão, para o teste
ERMO['coleta'] = K.materia(ERMO['habitat'], ERMO['perigo'])      # a matéria é a que a tabela dá a este tipo de ermo (a borda só dá matéria Comum): a vila de teste não desmente a regra
# quem tem nome: (id, nome, o que é, nível, molde, grau de ofício, maestria, prata, as peças: (tipo, família ou material, categoria, cobre, uso))
GENTE = [
    ('bento', 'Bento', 'o ferreiro da vila; conserta e vende o que forja', 28, 'guerreiro', 'oficial', {'forja': 4, 'martelo': 2}, 60,
     [('arma', 'martelo', 0, None, 'arma'), ('armadura', 'couro', 0, None, 'veste')]),
    ('dalva', 'Dalva', 'a taverneira da pousada; sabe de tudo o que se conta', 12, 'comum', 'oficial', {'comércio': 2, 'adaga': 2}, 80,
     [('arma', 'adaga', 0, None, 'arma')]),
    ('rute', 'Rute', 'a caçadora; conhece a Mata do Corvo', 22, 'arqueiro', 'aprendiz', {'arco': 4, 'caça': 4, 'adaga': 2}, 25,
     [('arma', 'arco', 1, None, 'arma'), ('arma', 'adaga', 0, None, 'arma2'), ('armadura', 'couro', 0, None, 'veste')]),
    ('tome', 'Tomé', 'o guarda da vila', 30, 'guerreiro', 'oficial', {'lança': 4, 'espada': 2}, 40,
     [('arma', 'lança', 1, None, 'arma'), ('escudo', None, 0, None, 'escudo'), ('armadura', 'malha', 0, None, 'veste'), ('armadura', 'malha', 0, ['cabeça'], 'veste')]),
    ('ivo', 'Ivo', 'o lenhador; tira madeira na borda da mata', 14, 'guerreiro', 'diarista', {'machado': 2, 'coleta': 2}, 12,
     [('arma', 'machado', 0, None, 'arma')]),
    ('nara', 'Nara', 'a curandeira; colhe erva e trata ferida', 16, 'comum', 'aprendiz', {'cura': 2, 'coleta': 2}, 30,
     [('arma', 'adaga', 0, None, 'arma')]),
    ('lino', 'Lino', 'o mercador da loja', 10, 'comum', 'oficial', {'comércio': 4}, 150, []),
    ('zeca', 'Zeca', 'o aprendiz da forja; novo, quer aprender', 3, 'comum', 'aprendiz', {}, 5, []),
]
# os começos: os atributos (a soma é a mesma: 340), a mão de Iniciante, o treino que a explica, o grau de ofício, as peças Comuns e a carga.
# O `sobre` não depende de gênero: o nome do personagem é o jogador quem dá
COMECOS = dict(
    ferreiro=dict(sobre='vive da forja, com a mão de Iniciante', atributos=dict(Força=65, Agilidade=50, Vigor=65, Vontade=50, Percepção=45, Afinidade=65), grau_oficio='aprendiz',
                  maestria={'forja': 2, 'martelo': 2}, treino={'forja': 50, 'martelo': 40}, marca={'prep_receita': 0}, carga={'metal:0': 4, 'madeira:0': 2},
                  pecas=[('arma', 'martelo', 0, None, 'arma'), ('armadura', 'couro', 0, None, 'veste')]),
    cacador=dict(sobre='vive da caça, com a mão de Iniciante no rastro e no arco', atributos=dict(Força=55, Agilidade=70, Vigor=60, Vontade=45, Percepção=70, Afinidade=40), grau_oficio='diarista',
                 maestria={'caça': 2, 'arco': 2}, treino={'caça': 40, 'arco': 40}, marca={}, carga={'comida': 2},
                 pecas=[('arma', 'arco', 0, None, 'arma'), ('arma', 'adaga', 0, None, 'arma2'), ('armadura', 'couro', 0, None, 'veste')]),
    guerreiro=dict(sobre='vive das armas, com a mão de Iniciante na espada', atributos=dict(Força=70, Agilidade=60, Vigor=70, Vontade=50, Percepção=50, Afinidade=40), grau_oficio='diarista',
                   maestria={'espada': 2}, treino={'espada': 40}, marca={}, carga={},
                   pecas=[('arma', 'espada', 0, None, 'arma'), ('escudo', None, 0, None, 'escudo'), ('armadura', 'malha', 0, None, 'veste')]),
)
NIVEL = 5
PRATA = 30
NOMES = dict(ferreiro='Aldo', cacador='Cira', guerreiro='Maro')


def treino_da_mao(maestria):
    """os blocos de treino que explicam a mão de alguém: para cada arma ou ofício, os blocos que a tabela pede para o grau que a pessoa tem (as armas, a forja e o couro, a caça,
    a coleta; no comércio, os dias de negócio). O ofício que ainda não tem tabela própria (a cura) segue a tabela geral, a das armas (tabelas_mundo.MAESTRIA_BLOCOS):
    TODA mão nasce com os blocos dela."""
    tabela = lambda k: {'forja': O.OFICIO_BLOCOS, 'couro': O.OFICIO_BLOCOS, 'caça': K.CACA_BLOCOS, 'coleta': K.COLETA_BLOCOS, 'comércio': C.COMERCIO_DIAS}.get(k, M.MAESTRIA_BLOCOS)
    return {k: tabela(k)[g] for k, g in maestria.items() if g in tabela(k)}


def _peca(tipo, qual, cat, cobre, de, dono):
    nome = dict(arma=qual, escudo='escudo').get(tipo) or ('elmo de ' + qual if cobre == ['cabeça'] else 'armadura de ' + qual)
    return item(tipo, cat, f"{nome.capitalize()} de {de}", familia=qual if tipo == 'arma' else None, material=qual if tipo == 'armadura' else None, cobre=cobre, dono=dono)


def _veste(E, pid, nome, pecas):
    """as peças de alguém nascem (um evento) e são postas em uso (outro)"""
    if not pecas: return
    s0 = E['itens']['seq']
    estado.aplica(E, 'gera', [['item', 'nasce', _peca(t, q, c, cb, nome, pid)] for t, q, c, cb, _ in pecas], onde=VILA['id'], quem=[pid], texto=f'as peças de {nome}')
    estado.aplica(E, 'gera', [['item', f'i{s0 + k + 1:04d}', 'uso', 'poe', uso] for k, (_, _, _, _, uso) in enumerate(pecas) if uso], onde=VILA['id'], quem=[pid], texto=f'{nome} se veste')


def cria(comeco='guerreiro', nome=None, semente=1, talentos=False, inclinacao=None):
    """o mundo da vila de teste, inteiro, por eventos "gera". Devolve o estado (quem chama grava).
    talentos: a gente nasce com os talentos e os dons pelo dado do mundo (a vila nova do comando nasce assim; a dos bancos, não: é a pessoa comum de hoje).
    inclinacao: o caminho que o jogador escolhe para o personagem (só com talentos)."""
    if comeco not in COMECOS: sys.exit(f'começo desconhecido: "{comeco}" (os que há: {", ".join(COMECOS)})')
    nasce = lambda pid, r, inc=None: talento.nasce(E, pid, r, inc) if talentos else r
    c = COMECOS[comeco]; nome = nome or NOMES[comeco]; E = estado.novo(semente); v, e = VILA, ERMO
    estado.aplica(E, 'gera', [['lugar', 'nasce', v['id'], dict(nome=v['nome'], em=v['em'], tipo='vila', cama=True, estoque={})],
                              ['lugar', 'nasce', e['id'], dict(nome=e['nome'], em=e['em'], tipo='ermo', habitat=e['habitat'], perigo=e['perigo'], longe=e['longe'], estoque={}, vizinhos=[v['id']],
                                                               teto=dict(e['bichos']), bichos=dict(e['bichos']), coleta_teto=dict(e['coleta']), coleta=dict(e['coleta']))],
                              ['lugar', v['id'], 'vizinhos', 'poe', [e['id']]]], texto=f"nascem {v['nome']} e {e['nome']} (a vila de teste, fora do cânone)")
    mercado.funda(E, v['id'], v['pop'], como='a feira e a loja da vila de teste')
    estado.aplica(E, 'gera', [['lugar', v['id'], 'oficina', 'poe', v['oficina']], ['lugar', v['id'], 'preparo.fogo', 'poe', v['fogo']], ['lugar', v['id'], 'preparo.bigorna', 'poe', v['bigorna']]],
                  onde=v['id'], texto=f"a forja de {v['nome']}: oficina {v['oficina']}; o fogo e a bigorna servem até o {T.CATS[v['fogo']]}")
    for pid, n, sobre, nivel, molde, grau, maestria, prata, pecas in GENTE:
        estado.aplica(E, 'gera', [['pessoa', 'nasce', pid, nasce(pid, dict(nome=n, nivel=nivel, atributos=padrao(n, nivel, molde=molde)['atributos'], lugar=v['id'], grau_oficio=grau, maestria=dict(maestria), treino=treino_da_mao(maestria), moedas=prata, sobre=sobre))]],
                      onde=v['id'], quem=[pid], texto=f'{n}, {sobre}')
        _veste(E, pid, n, pecas)
    estado.aplica(E, 'gera', [['pessoa', 'nasce', 'eu', nasce('eu', dict(nome=nome, nivel=NIVEL, atributos=dict(c['atributos']), lugar=v['id'], grau_oficio=c['grau_oficio'], maestria=dict(c['maestria']), treino=dict(c['treino']),
                                                              marca=dict(c['marca']), carga=dict(c['carga']), moedas=PRATA, jogador=True, sobre=c['sobre']), inclinacao)]], onde=v['id'], quem=['eu'], texto=f"{nome}, {c['sobre']}: o personagem")
    _veste(E, 'eu', nome, c['pecas'])
    P = estado.valida(E)
    if P: sys.exit('A VILA DE TESTE NASCEU QUEBRADA (não foi gravada):\n  ' + '\n  '.join(P))
    return E


def resumo(E):
    v = E['lugares'][VILA['id']]; e = E['lugares'][ERMO['id']]; p = E['gente']['eu']; raro = [TB.ESPECIES[x]['nome'] for x in e['bichos'] if TB.ESPECIES[x]['cat'] >= 2 and not TB.ESPECIES[x]['chefe']]
    chefe = [TB.ESPECIES[x]['nome'] for x in e['bichos'] if TB.ESPECIES[x]['chefe']]
    return [f"{v['nome']}: {v['pop']} de povo, {v['estoque'].get('prata', 0)} de prata, {len(mercado.prateleira(E, VILA['id']))} peças na prateleira, pousada, forja (oficina {v['oficina']}).",
            f"{e['nome']}, a {e['longe']} bloco: " + ', '.join(f"{TB.ESPECIES[x]['nome']} {q}" for x, q in e['bichos'].items()) + f" (o raro: {', '.join(raro)}; o chefe: {', '.join(chefe)}); tira-se: " + ', '.join(mercado.nome_bem(b) for b in e['coleta']) + '.',
            'Gente com nome: ' + ', '.join(f"{q['nome']} ({q['sobre'].split(';')[0]})" for k, q in E['gente'].items() if k != 'eu') + '.',
            f"O personagem: {p['nome']}, nível {p['nivel']}, {p['sobre']}; {p['moedas']} de prata; " + ', '.join(it['nome'] for it in E['itens']['itens'].values() if it.get('dono') == 'eu') + '.']


# ---------- A ETAPA DA MAGIA na vila que já existe (vila_teste.py magia PASTA) ----------
MAGO = ('anselmo', 'Anselmo', 'o mago velho; ensina o arcano a quem paga, e lê o que os outros não leem', 40, 'mago', 'mestre', {'arcano': 4}, 80,
        dict(tradicao='arcano', feiticos=['luz', 'seta', 'escudo', 'prender', 'lança-de-fogo']), [('foco', 'cajado', 1, 'foco'), ('amuleto', None, 0, 'pescoco'), ('armadura', 'couro', 0, 'veste')])
CLERIGA = ('lucia', 'Lúcia', 'a clériga do santuário; cura quem pede e quebra maldição com rito', 35, 'clérigo', 'oficial', {'fé': 6, 'maça': 2}, 40,
           dict(tradicao='fé', feiticos=['luz', 'cura', 'bênção', 'amparo', 'castigo', 'quebrar-maldição']), [('foco', 'símbolo', 0, 'foco'), ('arma', 'maça', 0, 'arma'), ('armadura', 'couro', 0, 'veste')])
BRUXA = ('joana', 'Joana', 'a bruxa que mora na choupana da borda da Mata do Corvo; lê a sorte, amaldiçoa por encomenda e vende veneno de lâmina, escondido', 30, 'bruxa', 'oficial', {'pacto': 4, 'adaga': 2}, 25,
         dict(tradicao='pacto', feiticos=['luz', 'mau-olhado', 'medo', 'sangria', 'ler', 'nó'], divida=2), [('foco', 'talismã', 0, 'foco'), ('arma', 'adaga', 0, 'arma')])
BRUXA_CARGA = {'veneno:0': 3, 'erva:0': 4}
NARA_ALQUIMIA = 2           # a curandeira passa a ter a mão de Iniciante na alquimia (a botica é dela)
ZECA_DOM = {'forja': 2}     # o aprendiz da forja tem o Grande Dom de forja, que ninguém leu (aparece quando decidir um teste, ou quando alguém o ler)
COVA = dict(id='cova', nome='a Cova Velha', em='na Cova Velha', habitat='ruína', perigo=1, longe=1, bichos={'esqueleto': 3, 'corpo-seco': 2})
PECA_MALDITA = dict(tipo='arma', familia='espada', cat=1, nome='a Espada do Guardião', maldicao=('a Mão Fria', 1, 'míngua'))      # largada na cova: quem a puser em uso pega a maldição; quebra devolvendo-a à cova
TOCA = dict(ermo='mata', especie='goblin', cabecas=8, tesouro=20)


def _peca_magia(tipo, qual, cat, de, dono):
    if tipo == 'foco': return item('foco', cat, f"{qual.capitalize()} de {de}", forma=qual, dono=dono)
    if tipo == 'amuleto': return item('amuleto', cat, f"Amuleto de {de}", dono=dono)
    return _peca(tipo, qual, cat, None, de, dono)


def magia(E, inclinacao=None):
    """ACRESCENTA a etapa da magia a uma vila de teste que já existe, só por eventos (nada se recria). Recusa rodar duas vezes e recusa o mundo que não é a vila de teste."""
    import criaturas, maldicao
    v, e = VILA['id'], ERMO['id']
    if v not in E['lugares'] or e not in E['lugares'] or 'eu' not in E['gente']: sys.exit('este mundo não é a vila de teste (falta Pedra Rasa, a Mata do Corvo ou o personagem): o `magia` só acrescenta à vila de teste')
    if COVA['id'] in E['lugares'] or E['lugares'][v].get('santuario') is not None or any(k in E['gente'] for k in (MAGO[0], CLERIGA[0], BRUXA[0])):
        sys.exit('a vila de teste já tem a etapa da magia (a cova, o santuário ou a gente nova): não se acrescenta duas vezes')
    if inclinacao is not None:
        import tabelas_talento as TT
        if inclinacao not in TT.CAMINHOS: sys.exit(f'inclinação desconhecida: "{inclinacao}" (os caminhos: {", ".join(TT.CAMINHOS)})')
        if talento.rolado(E['gente']['eu']): sys.exit('o personagem já tem o talento rolado: a inclinação só vale no nascimento')
    estado.sem_luta(E); n0 = E['relogio']['eventos']
    # 1 OS TALENTOS E OS DONS de quem ainda não foi rolado (o personagem, com a inclinação): um evento só, do gerador. É segredo: vai ao SÓ O MESTRE do RETOMAR, não aos fatos
    ef, quem = [], []
    for pid, p in list(E['gente'].items()):
        if p['estado'] == 'vivo' and not talento.rolado(p): ef += talento.rola(E, pid, inclinacao if pid == 'eu' else None); quem.append(pid)
    if ef: estado.aplica(E, 'gera', ef, onde=v, quem=quem, texto=f"os talentos e os dons de {estado.tantos(len(quem), 'pessoa')} foram rolados (ninguém sabe ainda o que tem)")
    # 2 O ZECA: o Grande Dom de forja, que ninguém leu
    if 'zeca' in E['gente'] and E['gente']['zeca']['estado'] == 'vivo':
        estado.aplica(E, 'gera', [['pessoa', 'zeca', 'dom', 'poe', dict(ZECA_DOM)]], onde=v, quem=['zeca'], texto='Zeca tem um dom de forja que ninguém leu')
    # 3 A BOTICA DA CURANDEIRA e O SANTUÁRIO
    ef = [['lugar', v, 'botica', 'poe', 1], ['lugar', v, 'santuario', 'poe', 1]]
    if 'nara' in E['gente'] and E['gente']['nara']['estado'] == 'vivo':
        ef += [['pessoa', 'nara', 'maestria.alquimia', 'poe', NARA_ALQUIMIA], ['pessoa', 'nara', 'treino.alquimia', 'poe', O.OFICIO_BLOCOS[NARA_ALQUIMIA]]]
    estado.aplica(E, 'gera', ef, onde=v, texto=f"{VILA['nome']} ganha a botica da curandeira e um santuário pequeno")
    import mercado
    if mercado.tem_mercado(E, v) and not E['lugares'][v].get('feira_magia'):         # a parte da magia do mercado: as poções que a botica faz, a água benta, os amuletos, os focos e a cartilha na prateleira
        mercado.funda_magia(E, v, como='a botica de Nara e o santuário abastecem a loja')
    # 4 A GENTE NOVA: o mago, a clériga e a bruxa (com o que sabem e o que vestem)
    for pid, n, sobre, nivel, molde, grau, maestria, prata, mg, pecas in (MAGO, CLERIGA, BRUXA):
        r = dict(nome=n, nivel=nivel, atributos=padrao(n, nivel, molde=molde)['atributos'], lugar=v, grau_oficio=grau, maestria=dict(maestria), treino=treino_da_mao(maestria), moedas=prata, sobre=sobre)
        r.update({k: (list(x) if isinstance(x, list) else x) for k, x in mg.items()})
        if mg.get('tradicao') == 'fé': r['voto'] = dict(qual='socorro', santuario=v, dia=E['relogio']['dia'])
        if pid == BRUXA[0]: r['carga'] = dict(BRUXA_CARGA)
        estado.aplica(E, 'gera', [['pessoa', 'nasce', pid, talento.nasce(E, pid, r)]], onde=v, quem=[pid], texto=f'{n}, {sobre}')
        s0 = E['itens']['seq']
        estado.aplica(E, 'gera', [['item', 'nasce', _peca_magia(t, q, c, n, pid)] for t, q, c, _ in pecas], onde=v, quem=[pid], texto=f'as peças de {n}')
        estado.aplica(E, 'gera', [['item', f'i{s0 + k + 1:04d}', 'uso', 'poe', uso] for k, (_, _, _, uso) in enumerate(pecas)], onde=v, quem=[pid], texto=f'{n} se veste')
    # 5 A COVA VELHA (um ermo novo, vizinho da vila) e a peça maldita largada no chão
    c = COVA; viz = list(E['lugares'][v].get('vizinhos') or [])
    estado.aplica(E, 'gera', [['lugar', 'nasce', c['id'], dict(nome=c['nome'], em=c['em'], tipo='ermo', habitat=c['habitat'], perigo=c['perigo'], longe=c['longe'], estoque={}, vizinhos=[v],
                                                             teto=dict(c['bichos']), bichos=dict(c['bichos']), coleta_teto=K.materia(c['habitat'], c['perigo']), coleta=K.materia(c['habitat'], c['perigo']))],
                              ['lugar', v, 'vizinhos', 'poe', viz + [c['id']]]], onde=c['id'], texto=f"{c['nome']}, o cemitério velho além da vila: os mortos de lá não dormem")
    pm = PECA_MALDITA; iid = f"i{E['itens']['seq'] + 1:04d}"
    it = item(pm['tipo'], pm['cat'], pm['nome'], familia=pm['familia']); it.update(onde=c['id'], solto=True, historia=['largada na Cova Velha, junto de um morto que não se deita'])
    nm, cat, tipo = pm['maldicao']
    estado.aplica(E, 'gera', [['item', 'nasce', it], ['item', iid, 'maldita', 'poe', maldicao.molde(nm, cat, tipo, dict(tipo='devolver', item=iid, onde=c['id']))]], onde=c['id'],
                  texto=f"{pm['nome']} está largada {c['em']}: é maldita")
    # 6 A TOCA DOS GOBLINS na Mata do Corvo
    t = TOCA; criaturas.poe_covil(E, t['ermo'], t['especie'], cabecas_=t['cabecas'], tesouro=t['tesouro'], tipo='gera', como='um covil pequeno, que rouba de noite')
    P = estado.valida(E)
    if P: sys.exit('A MAGIA ENTROU TORTA NA VILA (não foi gravada):\n  ' + '\n  '.join(P))
    return E['relogio']['eventos'] - n0


def resumo_magia(E):
    eu = E['gente']['eu']; tal = eu.get('talento') or {}
    return [f"Gente nova: {', '.join(E['gente'][k]['nome'] + ' (' + E['gente'][k]['sobre'].split(';')[0] + ')' for k in (MAGO[0], CLERIGA[0], BRUXA[0]))}.",
            f"{VILA['nome']} tem agora a botica de Nara e um santuário; {COVA['nome']} fica a {COVA['longe']} bloco (esqueletos e corpos-secos; e uma peça largada no chão).",
            f"Na Mata do Corvo mora um bando de goblins (a toca: `caca.py sair mata alvo=toca`).",
            f"Os talentos e os dons foram rolados (ninguém sabe o que tem: o talento aparece fazendo, o dom quando decide um teste)" + (f"; a inclinação de {eu['nome']}: {eu.get('inclinacao')}" if eu.get('inclinacao') else '') + '.']


def main(a=None):
    a = sys.argv[1:] if a is None else list(a)
    op = dict(x.split('=', 1) for x in a if '=' in x); pos = [x for x in a if '=' not in x]
    if pos[:1] == ['magia']:
        if len(pos) != 2 or any(k != 'inclinacao' for k in op): print(__doc__); return
        pasta = os.path.abspath(pos[1])
        if not os.path.exists(os.path.join(pasta, 'relogio.json')): sys.exit(f'{pasta} não tem um mundo (falta o relogio.json): crie a vila antes (`vila_teste.py PASTA`)')
        os.environ['MOTOR10_MUNDO'] = pasta; E = estado.carrega()
        n = magia(E, op.get('inclinacao')); estado.grava(E)
        print(f'A ETAPA DA MAGIA entrou na vila de {pasta} ({n} eventos, nada recriado).\n'); print('\n'.join(resumo_magia(E)))
        print('\nA MESA se refaz no próximo `turno.py abre`.'); return
    if len(pos) != 1 or any(k not in ('comeco', 'nome', 'semente', 'inclinacao') for k in op): print(__doc__); return
    pasta = os.path.abspath(pos[0])
    if os.path.exists(pasta) and (not os.path.isdir(pasta) or os.listdir(pasta)): sys.exit(f'{pasta} já existe e não está vazia: não escrevo por cima. Escolha uma pasta nova.')
    if not op.get('semente', '1').isdigit(): sys.exit(f'semente= pede um número (veio "{op["semente"]}")')
    E = cria(op.get('comeco', 'guerreiro'), op.get('nome'), int(op.get('semente', 1)), talentos=True, inclinacao=op.get('inclinacao'))
    os.makedirs(pasta, exist_ok=True); os.environ['MOTOR10_MUNDO'] = pasta
    estado.grava(E); turno.abre(E)
    open(os.path.join(pasta, 'LEIA.md'), 'w', encoding='utf-8').write(
        '# VILA DE TESTE (fora do cânone)\n\nEste save é um mundo pequeno, feito pelo `vila_teste.py` do Motor 10 para experimentar a luta, a caça, a forja e o custo de viver.\n'
        'Nada daqui vale para jogo nenhum. O guia está em `motor10/GUIA_VILA.md`.\n\n' + '\n'.join('- ' + x for x in resumo(E)) + '\n')
    print(f'A VILA DE TESTE nasceu em {pasta} (fora do cânone; {E["relogio"]["eventos"]} eventos "gera").\n')
    print('\n'.join(resumo(E)))
    print(f'\nPara jogar (de dentro de motor10/):\n  export MOTOR10_MUNDO={pasta}\n  python3 turno.py abre\nO guia: GUIA_VILA.md')


if __name__ == '__main__':
    import signal; hasattr(signal, 'SIGPIPE') and signal.signal(signal.SIGPIPE, signal.SIG_DFL)      # a saída cortada (`| head`) acaba o comando calada, sem erro de programa: a vila já foi gravada antes de falar
    main()
