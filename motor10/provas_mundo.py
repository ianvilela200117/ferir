#!/usr/bin/env python3
"""provas_mundo.py — MOTOR 10: O BANCO DE PROVAS DO MUNDO. Cada etapa do PROJETO.md entra aqui com as suas metas.

ETAPA 1, "um dia numa vila": o gravador único, o relógio, o corpo, os atos, a ferida que dura, a luta que volta ao estado, abrir e fechar o turno.
ETAPA 2, o alicerce (o que a integração pôs nele): a morte numa regra só, nascer por evento, vestir e guardar, a jornada, comer da carga, os invariantes novos,
o evento que não muda nada; a cama por noite, a luta aberta que tranca o mundo, o RETOMAR que não corta calado, o sob medida pelo id, as entradas tortas e a língua
da mesa (a segunda volta); e depois os bancos dos módulos (o mercado, o ofício, a caça e a coleta).
As provas rodam numa pasta de rascunho (nunca num save de verdade).

Uso: python3 provas_mundo.py [N]             N = lutas da prova do corpo (padrão 300)
     python3 provas_mundo.py vila PASTA       cria uma vila de prova numa pasta, para experimentar os comandos:
                                              MOTOR10_MUNDO=PASTA python3 turno.py abre
"""
import contextlib, copy, io, json, os, shutil, sys, tempfile
import tabelas as T
import tabelas_mundo as M
import estado, corpo, ato, teste, turno, luta
from itens import item
from pessoas import ficha


def vila(semente=1, prata=30, caixa=2000):
    """uma vila de prova: um lugar (com a prata de tabela de uma vila de 400: 5 por cabeça), o personagem com uma espada e um couro Comuns, 30 de prata"""
    E = estado.novo(semente)
    E['lugares']['vila'] = dict(nome='a Vila de Prova', em='na Vila de Prova', tipo='vila', cama=True, estoque=dict(comida=2000, prata=caixa))
    at = dict(Força=65, Agilidade=60, Vigor=65, Vontade=50, Percepção=50, Afinidade=45)
    E['gente']['eu'] = dict(nome='Aldric', jogador=True, lugar='vila', grau_oficio='diarista', nivel=1, atributos=at, maestria={}, treino={}, moedas=prata,
                            corpo=dict(fome=0, sono=0, cansaco=0), pv=T.pv_max(at['Vigor'], 1), feridas=[], estado='vivo', marca={})
    estado.aplica(E, 'gera', [['item', 'nasce', item('arma', 0, 'Espada do Aldric', familia='espada', dono='eu')], ['item', 'nasce', item('armadura', 0, 'Gibão do Aldric', material='couro', dono='eu')]], texto='o mundo de prova nasce')
    estado.aplica(E, 'gera', [['item', 'i0001', 'uso', 'poe', 'arma'], ['item', 'i0002', 'uso', 'poe', 'veste']], texto='o Aldric se veste')
    return E


def dia_de_rotina(E, comer=True, dormir=True, trabalha=True):
    """um dia: dorme a madrugada e a alvorada, come, trabalha a manhã e a tarde, e fica à toa até a meia-noite"""
    if dormir: ato.dormir(E, 'eu', 2, para=False)
    else: ato.passa(E, 'eu', 2, 'esperar', para=False)
    if comer: ato.comer(E, 'eu')
    if trabalha: ato.passa(E, 'eu', 2, 'trabalhar', esforco='pesado', mais=lambda i: [['estoque', 'vila', 'prata', 'soma', -2], ['pessoa', 'eu', 'moedas', 'soma', 2]], para=False)
    else: ato.passa(E, 'eu', 2, 'descansar', esforco='descanso', para=False)
    ato.passa(E, 'eu', 2, 'esperar', para=False)


def recusa(f):
    """roda f e devolve o texto da recusa (ou None se passou)"""
    try:
        with contextlib.redirect_stdout(io.StringIO()): f()
    except SystemExit as e: return str(e)
    return None


def provas(n):
    out = []; ok = lambda nome, deu, passa: out.append((nome, deu, bool(passa)))
    # 1 a rotina sustenta
    E = vila(); E['relogio']['bloco'] = 0; E['turno']['aberto']['bloco'] = 0; pior = 0
    for _ in range(30): dia_de_rotina(E); pior = min(pior, corpo.pena(E['gente']['eu']))
    p = E['gente']['eu']
    ok('A ROTINA: 30 dias dormindo, comendo uma vez e trabalhando dois blocos', f"pior pena {pior}; prata 30 → {p['moedas']}; o corpo no fim: {corpo.diz(p)}", pior == 0 and 50 <= p['moedas'] <= 70 and not estado.valida(E))
    # 2 quem não dorme
    E = vila(); n_feitos, pq = ato.passa(E, 'eu', 18, 'esperar'); p = E['gente']['eu']
    E2 = vila(); ato.passa(E2, 'eu', 9, 'esperar', para=False)
    ok('O SONO: acordado sem parar, o ato longo para sozinho; com 9 blocos acordado, a pena é −4', f"parou em {n_feitos} blocos ({pq}); pena {corpo.pena(E2['gente']['eu'])}", n_feitos <= 6 and pq and corpo.pena(E2['gente']['eu']) == -4)
    # 3 quem não come
    E = vila(); E['relogio']['bloco'] = 0
    for _ in range(6): dia_de_rotina(E, comer=False, trabalha=False)
    p = E['gente']['eu']; ok('A FOME: seis dias sem comer', f"fome {p['corpo']['fome']}; PV {p['pv']} de {estado.pv_max(p)}; pena {corpo.pena(p)}", p['corpo']['fome'] == 10 and p['pv'] <= 0.9 * estado.pv_max(p) and corpo.pena(p) == -4)
    # 4 a ferida que dura
    E = vila(prata=200); E['relogio']['bloco'] = 0
    estado.aplica(E, 'mestre', [['ferida', 'eu', 'abre', 'braços', False], ['ferida', 'eu', 'abre', 'tronco', True]], texto='feridas de prova')
    for _ in range(6): dia_de_rotina(E, trabalha=False)
    seis = len(E['gente']['eu']['feridas']); dia_de_rotina(E, trabalha=False); sete = len(E['gente']['eu']['feridas'])
    for _ in range(13): dia_de_rotina(E, trabalha=False)
    vinte = len(E['gente']['eu']['feridas']); dia_de_rotina(E, trabalha=False); vinteum = len(E['gente']['eu']['feridas'])
    Et = vila(); Et['relogio']['bloco'] = 0; estado.aplica(Et, 'mestre', [['ferida', 'eu', 'abre', 'braços', False]], texto='ferida de prova')
    for _ in range(10): dia_de_rotina(Et)                    # trabalhando pesado dois blocos por dia
    ok('A FERIDA: sara com 7 dias de repouso (a grave, com 21); trabalhando pesado, não sara', f'feridas no dia 6, 7, 20, 21: {seis}, {sete}, {vinte}, {vinteum}; trabalhando 10 dias: {len(Et["gente"]["eu"]["feridas"])}',
       (seis, sete, vinte, vinteum) == (2, 1, 1, 0) and len(Et['gente']['eu']['feridas']) == 1)
    # 5 a noite devolve o PV
    E = vila(); E['relogio']['bloco'] = 0; estado.aplica(E, 'mestre', [['pessoa', 'eu', 'pv', 'soma', -60]], texto='apanhou'); pv0 = E['gente']['eu']['pv']
    dia_de_rotina(E, trabalha=False); um = E['gente']['eu']['pv'] - pv0
    ok('A NOITE: dois blocos dormidos sem fome devolvem um décimo do PV', f'{um} de {estado.pv_max(E["gente"]["eu"])}', um == 2 * int(estado.pv_max(E['gente']['eu']) * M.CURA_BLOCO))
    # 6 o gravador recusa, e recusa inteiro
    E = vila(); antes = json.dumps({k: E[k] for k in estado.ARQS}, sort_keys=True, ensure_ascii=False)
    casos = [('evento sem efeito', lambda: estado.aplica(E, 'mestre', [])), ('evento que não existe', lambda: estado.aplica(E, 'milagre', [['relogio', 1]])),
             ('verbo que não existe', lambda: estado.aplica(E, 'mestre', [['clima', 'vila', 'sol']])), ('campo que não existe', lambda: estado.aplica(E, 'mestre', [['pessoa', 'eu', 'sorte', 'soma', 5]])),
             ('pagar o que não tem (depois de um efeito bom)', lambda: estado.aplica(E, 'mestre', [['pessoa', 'eu', 'fome', 'soma', 2], ['pessoa', 'eu', 'moedas', 'soma', -999]])),
             ('pessoa que não existe', lambda: estado.aplica(E, 'mestre', [['pessoa', 'ninguém', 'pv', 'soma', 1]])), ('estoque que não há', lambda: estado.aplica(E, 'mestre', [['estoque', 'vila', 'ferro', 'soma', -1]])),
             ('vestir peça no lugar errado', lambda: estado.aplica(E, 'mestre', [['item', 'i0002', 'uso', 'poe', 'arma']])), ('dar peça a quem não existe', lambda: estado.aplica(E, 'mestre', [['item', 'i0001', 'dono', 'poe', 'fantasma']]))]
    rec = [nome for nome, f in casos if recusa(f)]; igual = antes == json.dumps({k: E[k] for k in estado.ARQS}, sort_keys=True, ensure_ascii=False)
    ok('O GRAVADOR: nove eventos errados são recusados, e o estado não muda nem pela metade', f'{len(rec)} de {len(casos)} recusados; estado {"intacto" if igual else "MUDOU"}', len(rec) == len(casos) and igual)
    # 7 os invariantes pegam o que for plantado por fora
    E = vila(); limpo = estado.valida(E); E['gente']['eu']['moedas'] = -5; E['gente']['eu']['corpo']['sono'] = 14; E['itens']['itens']['i0001']['dono'] = 'fantasma'; E['gente']['eu']['lugar'] = 'lugar nenhum'
    E['gente']['eu']['pv'] = 9999; E['lugares']['vila']['estoque']['comida'] = -1
    achou = estado.valida(E); ok('OS INVARIANTES: seis estragos plantados por fora do gravador', f'limpo: {len(limpo)} problema(s); estragado: {len(achou)}', not limpo and len(achou) >= 6)
    # 8 o corpo entra na luta
    E = vila(); so = lambda: [estado.lutador(E, 'eu', nome='descansado')]; E3 = vila(); E3['gente']['eu']['corpo'].update(sono=8, cansaco=9)
    cansado = lambda: [estado.lutador(E3, 'eu', nome='moído')]; luta.semente(4); v, _ = luta.duelos(cansado, so, n=n, inicio='colado'); luta.D = luta.Dados()
    fc, fd = ficha(cansado()[0]), ficha(so()[0])
    ok('O CORPO NA LUTA: o mesmo homem, moído (sono 8, cansaço 9), contra ele descansado', f"vence {v}%; fôlego {fc['folmax']} contra {fd['folmax']}; acerto {fc['arma']['acerto']:g} contra {fd['arma']['acerto']:g}", v <= 35 and fc['folmax'] < fd['folmax'])
    # 9 a luta volta ao estado, por evento
    d = tempfile.mkdtemp(prefix='m10_'); os.environ['MOTOR10_MUNDO'] = d
    try:
        E = vila(); estado.grava(E)
        json.dump(dict(inicio='colado', A=[dict(id='eu', controla=True)], B=[dict(nome='o ladrão de galinhas', nivel=3, molde='comum', veste=dict(arma=['adaga', 'Comum']))]), open(os.path.join(d, 'cen.json'), 'w'))
        with contextlib.redirect_stdout(io.StringIO()):
            ato.luta_nova(E, os.path.join(d, 'cen.json'), os.path.join(d, 'luta.json')); aberta = recusa(lambda: turno.fecha(estado.carrega(), 'tentando fechar com a luta aberta'))
            for _ in range(60):
                E = estado.carrega(); S = json.load(open(os.path.join(d, 'luta.json')))
                if S['fim']: break
                ato.luta_roda(E, os.path.join(d, 'luta.json'), ['Aldric: atacar']); estado.grava(E)
        E = estado.carrega(); S = json.load(open(os.path.join(d, 'luta.json'))); f = S['L'][0]; p = E['gente']['eu']
        evs = [json.loads(x) for x in open(os.path.join(d, 'eventos.jsonl'), encoding='utf-8').read().splitlines()]; ev = [e for e in evs if e['tipo'] == 'luta']
        certo = (p['estado'] == 'morto') == (f['estado'] == 'morto') and (p['estado'] == 'morto' or p['pv'] == max(1, f['pv'])) and len(p['feridas']) == len(f['feridas']) and len(ev) == 1 and E['turno']['lutas'][0]['fim']
        ok('A LUTA VOLTA AO ESTADO: PV, feridas e morte entram por um evento só; com a luta aberta o turno não fecha', f"a luta acabou ({S['fim']}); o Aldric: {p['estado']}, PV {p['pv']}, {len(p['feridas'])} ferida(s); eventos de luta: {len(ev)}; fechar com ela aberta: {'recusado' if aberta else 'ACEITO'}", certo and aberta)
        # 10 o turno: abre, pergunta, responde, fecha
        E = vila(); estado.grava(E); r1 = recusa(lambda: turno.fecha(estado.carrega(), 'nada'))            # sem perguntas e com o relógio parado
        E = estado.carrega(); turno.pergunta(E, 'O que fazer de manhã?', ['a=trabalhar', 'b=treinar']); turno.pergunta(E, 'E a noite?', ['a=dormir na pousada', 'b=dormir no chão']); estado.grava(E)
        r2 = recusa(lambda: turno.fecha(estado.carrega(), 'nada'))                                           # relógio parado
        r3 = recusa(lambda: turno.responde(estado.carrega(), '3a')); r4 = recusa(lambda: turno.responde(estado.carrega(), '1z'))
        E = estado.carrega(); turno.responde(E, '1a.2b'); ato.trabalhar(E, 'eu', 2); ato.comer(E, 'eu'); teste.rola(E, 'ouvir a conversa na taverna', 'Percepção', 26, oculto=True); estado.grava(E)
        r5 = recusa(lambda: turno.fecha(estado.carrega(), 'trabalhou'))                                      # as duas perguntas foram respondidas: faltam novas
        E = estado.carrega(); turno.pergunta(E, 'Amanhã?', ['a=trabalhar de novo', 'b=ir à forja']); turno.pergunta(E, 'O dinheiro?', ['a=guardar', 'b=comprar um elmo']); estado.grava(E)
        with contextlib.redirect_stdout(io.StringIO()): fim = turno.fecha(estado.carrega(), 'O Aldric trabalhou a manhã e a tarde e comeu na taverna.')
        ret = open(os.path.join(d, 'RETOMAR.md'), encoding='utf-8').read(); mesa = open(os.path.join(d, 'MESA.md'), encoding='utf-8').read(); E = estado.carrega()
        certo = all([r1, r2, r3, r4, r5]) and 'fechado' in fim and E['turno']['n'] == 2 and len(E['turno']['perguntas']) == 2 and 'OCULTA' in ret and 'trabalha' in ret and 'Amanhã?' in mesa
        ok('O TURNO: cinco fechamentos e respostas erradas são recusados; o certo fecha e gera o RETOMAR e a MESA', f"recusas: {sum(bool(x) for x in (r1, r2, r3, r4, r5))} de 5; RETOMAR {len(ret.encode())} bytes; MESA {len(mesa.encode())} bytes", certo and len(ret.encode()) <= 6000 and len(mesa.encode()) <= 8000)
    finally:
        os.environ.pop('MOTOR10_MUNDO', None); shutil.rmtree(d, ignore_errors=True)
    # 11 mesmo começo, mesmos atos: mesmo mundo
    def roda(sem):
        E = vila(sem); E['relogio']['bloco'] = 0
        for _ in range(12): dia_de_rotina(E, dormir=False, trabalha=True)
        return json.dumps({k: E[k] for k in estado.ARQS}, sort_keys=True, ensure_ascii=False)
    ok('O MESMO MUNDO: mesma semente e mesmos atos dão o mesmo estado; semente diferente, não', 'conferido em 12 dias sem dormir (o acaso do sono entra)', roda(7) == roda(7) and roda(7) != roda(8))
    # 12 o treino
    E = vila(prata=200); E['relogio']['bloco'] = 0
    for _ in range(14):
        ato.dormir(E, 'eu', 2, para=False); ato.comer(E, 'eu'); ato.treinar(E, 'eu', 3, 'espada'); ato.passa(E, 'eu', 1, 'descansar', esforco='descanso', para=False)
    p = E['gente']['eu']; m14 = p['maestria'].get('espada', 0); b14 = p['treino']['espada']; estado.aplica(E, 'mestre', [['pessoa', 'eu', 'treino.espada', 'soma', 600]], texto='anos de treino, para a prova'); ato._sobe_maestria(E, 'eu', 'espada')
    ok('O TREINO: 42 blocos com a espada fazem um Iniciante; 600 blocos fazem um Treinado, e Mestre só com um feito', f"depois de 14 dias: {T.MAESTRIAS[m14]} ({b14} blocos); com 600 a mais: {T.MAESTRIAS[E['gente']['eu']['maestria']['espada']]}", m14 == 2 and E['gente']['eu']['maestria']['espada'] == 4)
    return out


def provas_alicerce2(n=300):
    """ETAPA 2, o alicerce: o que a integração pôs no estado.py, no ato.py e no turno.py para os quatro módulos caberem"""
    import oficio, mercado
    out = []; ok = lambda nome, deu, passa: out.append((nome, deu, bool(passa)))
    prata_do_mundo = lambda E: sum(p['moedas'] for p in E['gente'].values()) + sum(l['estoque'].get('prata', 0) for l in E['lugares'].values())
    retrato = lambda E: json.dumps({k: E[k] for k in estado.ARQS}, sort_keys=True, ensure_ascii=False)
    def quieto(f, *a, **k):
        with contextlib.redirect_stdout(io.StringIO()): return f(*a, **k)
    # 13 nascer por evento
    E = estado.novo(5); at = dict(Força=60, Agilidade=60, Vigor=60, Vontade=50, Percepção=50, Afinidade=50)
    estado.aplica(E, 'gera', [['lugar', 'nasce', 'aldeia', dict(nome='a Aldeia', em='na Aldeia', tipo='vila', cama=True, estoque=dict(comida=50, prata=100))],
                              ['lugar', 'nasce', 'mato', dict(nome='o Mato', tipo='ermo', vizinhos=['aldeia'], bichos={'corça': 3}, teto={'corça': 5})],
                              ['pessoa', 'nasce', 'ana', dict(nome='Ana', nivel=3, atributos=at, lugar='aldeia', moedas=7, maestria={'espada': 2}, jogador=True)]], texto='o mundo nasce')
    p = E['gente']['ana']; nasceu = p['pv'] == estado.pv_max(p) and p['corpo'] == dict(fome=0, sono=0, cansaco=0) and p['moedas'] == 7 and E['lugares']['mato']['bichos'] == {'corça': 3} and not estado.valida(E); antes = retrato(E)
    casos = [('gente num evento que não é de nascer', lambda: estado.aplica(E, 'compra', [['pessoa', 'nasce', 'bia', dict(nome='Bia', nivel=1, atributos=at, lugar='aldeia')]])),
             ('lugar num evento que não é de nascer', lambda: estado.aplica(E, 'venda', [['lugar', 'nasce', 'x', dict(nome='X')]])), ('a mesma pessoa duas vezes', lambda: estado.aplica(E, 'gera', [['pessoa', 'nasce', 'ana', dict(nome='Ana', nivel=1, atributos=at, lugar='aldeia')]])),
             ('gente sem atributos', lambda: estado.aplica(E, 'gera', [['pessoa', 'nasce', 'bia', dict(nome='Bia', nivel=1, lugar='aldeia')]])), ('gente num lugar que não existe', lambda: estado.aplica(E, 'gera', [['pessoa', 'nasce', 'bia', dict(nome='Bia', nivel=1, atributos=at, lugar='lua')]])),
             ('um segundo personagem do jogador', lambda: estado.aplica(E, 'gera', [['pessoa', 'nasce', 'bia', dict(nome='Bia', nivel=1, atributos=at, lugar='aldeia', jogador=True)]])),
             ('lugar com bicho que não existe', lambda: estado.aplica(E, 'gera', [['lugar', 'nasce', 'y', dict(nome='Y', bichos={'unicórnio': 2})]])), ('peça que nasce sem dono e sem lugar', lambda: estado.aplica(E, 'gera', [['item', 'nasce', item('arma', 0, familia='adaga')]]))]
    rec = [x for x, f in casos if recusa(f)]
    ok('NASCER: lugar e gente nascem por evento (`gera` ou `mestre`), com os padrões postos; fora disso, ou tortos, são recusados', f"um lugar, um ermo e uma pessoa nascidos, o estado inteiro: {'sim' if nasceu else 'NÃO'}; {len(rec)} de {len(casos)} nascimentos errados recusados; estado {'intacto' if antes == retrato(E) else 'MUDOU'}",
       nasceu and len(rec) == len(casos) and antes == retrato(E))
    # 14 a morte, uma regra só
    E = vila(prata=40); estado.aplica(E, 'gera', [['lugar', 'vila', 'oficina', 'poe', 2], ['pessoa', 'eu', 'maestria.forja', 'poe', 4], ['pessoa', 'eu', 'carga.metal:2', 'soma', 3], ['pessoa', 'eu', 'carga.comida', 'soma', 5],
                                                  ['item', 'nasce', item('arma', 1, 'Lança guardada', familia='lança', dono='eu')], ['item', 'nasce', item('nucleo', 3, 'Núcleo de prova', de='serpe', dono='eu')]], texto='o que ele tem')
    quieto(oficio.forjar, E, 'eu', oficio.molde('arma', 3, 'Espada da Prova', familia='espada'), blocos=0); p0 = prata_do_mundo(E); n_itens = len(E['itens']['itens']); cx = E['lugares']['vila']['estoque']['prata']
    estado.aplica(E, 'mestre', [['pessoa', 'eu', 'pv', 'soma', -9999], ['pessoa', 'eu', 'estado', 'poe', 'morto']], texto='o Aldric morre, para a prova'); m = E['gente']['eu']; L = E['itens']['itens']
    caiu = len(L) == n_itens and all(it['dono'] is None and it['onde'] == 'vila' and it.get('solto') and not it.get('uso') for it in L.values()) and not E['itens']['obras']
    nada = m['moedas'] == 0 and not m['carga'] and E['lugares']['vila']['estoque']['prata'] == cx + 40 and E['lugares']['vila']['estoque']['comida'] == 2005 and m['morte'] == dict(dia=1, bloco=2, onde='vila', prata=40, carga={'comida': 5})       # a morte guarda também o que ele deixou (a MESA de quem morreu diz)
    antes = retrato(E); atos = [('comer', lambda: ato.comer(E, 'eu')), ('dormir na cama', lambda: ato.dormir(E, 'eu', 2)), ('trabalhar', lambda: ato.trabalhar(E, 'eu', 1)), ('treinar', lambda: ato.treinar(E, 'eu', 1, 'espada')),
                                ('esperar', lambda: ato.esperar(E, 'eu', 1)), ('vestir', lambda: ato.vestir(E, 'eu', 'i0001')), ('testar', lambda: teste.rola(E, 'levantar-se', 'Vontade', 20)),
                                ('receber uma peça', lambda: estado.aplica(E, 'mestre', [['item', 'i0001', 'dono', 'poe', 'eu']]))]
    rec = [x for x, f in atos if recusa(f)]; mesa = turno.mesa(E)
    ok('A MORTE, UMA REGRA SÓ: o morto não fica com nada (as peças e o núcleo caem soltos onde ele morreu, a obra se desfaz, a carga e a prata ficam no lugar); morto não age, e nada é cobrado dele; a MESA abre com a morte',
       f"as {n_itens} peças (duas vestidas, uma guardada, o núcleo que estava na obra) soltas na vila, e a obra desfeita: {'sim' if caiu else 'NÃO'}; a carga e os 40 de prata no estoque do lugar: {'sim' if nada else 'NÃO'}; a prata do mundo fecha: {'sim' if prata_do_mundo(E) == p0 else 'NÃO'}; "
       f"estado {'inteiro' if not estado.valida(E) else 'QUEBRADO'}; {len(rec)} de {len(atos)} atos do morto recusados, sem mudar nada: {'sim' if antes == retrato(E) else 'NÃO'}; a MESA diz que ele morreu e não lista atos: {'sim' if 'MORREU' in mesa and 'ato.py comer' not in mesa else 'NÃO'}",
       caiu and nada and prata_do_mundo(E) == p0 and not estado.valida(E) and len(rec) == len(atos) and antes == retrato(E) and 'MORREU' in mesa and 'ESTÁ MORTO' not in mesa and 'ato.py comer' not in mesa)
    # 15 vestir e guardar
    E = vila(); estado.aplica(E, 'gera', [['item', 'nasce', item('arma', 1, 'Arco de prova', familia='arco', dono='eu')], ['item', 'nasce', item('armadura', 1, 'Cota de prova', material='malha', dono='eu')],
                                          ['item', 'nasce', item('armadura', 0, 'Elmo de prova', material='couro', cobre=['cabeça'], dono='eu')], ['item', 'nasce', item('escudo', 0, 'Escudo de prova', dono='eu')],
                                          ['item', 'nasce', item('nucleo', 3, 'Núcleo de prova', dono='eu')], ['item', 'nasce', item('arma', 0, 'Adaga da loja', familia='adaga', onde='vila')]], texto='peças de prova')
    arco, cota, elmo, escudo, nucleo, loja = (f'i{k:04d}' for k in range(3, 9)); f0 = ficha(estado.lutador(E, 'eu'))['arma']['nome']; L = lambda: E['itens']['itens']
    quieto(ato.vestir, E, 'eu', arco); trocou = L()[arco]['uso'] == 'arma' and L()['i0001']['uso'] is None and ficha(estado.lutador(E, 'eu'))['arma']['nome'] == 'Arco de prova' != f0
    quieto(ato.vestir, E, 'eu', 'i0001', 'arma2'); quieto(ato.vestir, E, 'eu', cota); quieto(ato.vestir, E, 'eu', elmo); quieto(ato.vestir, E, 'eu', escudo)
    vestiu = L()['i0001']['uso'] == 'arma2' and L()[cota]['uso'] == 'veste' and L()['i0002']['uso'] is None and L()[elmo]['uso'] == 'veste' and L()[escudo]['uso'] == 'escudo'       # a cota tira o gibão (cobrem o mesmo); o elmo soma
    quieto(ato.tirar, E, 'eu', elmo); tirou = L()[elmo]['uso'] is None; antes = retrato(E)
    casos = [('vestir um núcleo', lambda: ato.vestir(E, 'eu', nucleo)), ('vestir a peça da loja', lambda: ato.vestir(E, 'eu', loja)), ('a armadura na mão', lambda: ato.vestir(E, 'eu', cota, 'arma')), ('o que já está em uso', lambda: ato.vestir(E, 'eu', arco)),
             ('guardar o que já está guardado', lambda: ato.tirar(E, 'eu', elmo)), ('o que não está no Livro', lambda: ato.vestir(E, 'eu', 'i9999'))]
    rec = [x for x, f in casos if recusa(f)]; evs = sum(e['tipo'] == 'vestir' for e in E['_novos'])
    ok('VESTIR E GUARDAR: `ato.py vestir` e `ato.py tirar` mudam o que a pessoa usa, por evento, e a ficha de luta segue; a peça que estava no mesmo lugar vai para a guarda',
       f"empunhar o arco guarda a espada, e a ficha passa a ser a do arco: {'sim' if trocou else 'NÃO'}; a espada de reserva, a cota (que tira o gibão), o elmo e o escudo: {'sim' if vestiu else 'NÃO'}; tirar o elmo: {'sim' if tirou else 'NÃO'}; "
       f"{evs} eventos `vestir`; {len(rec)} de {len(casos)} pedidos errados recusados; estado {'intacto' if antes == retrato(E) else 'MUDOU'} e {'inteiro' if not estado.valida(E) else 'QUEBRADO'}",
       trocou and vestiu and tirou and evs == 6 and len(rec) == len(casos) and antes == retrato(E) and not estado.valida(E))
    # 16 a jornada, o lugar sem prata, comer da carga
    E = vila(prata=10); E['relogio']['bloco'] = 0; quieto(ato.dormir, E, 'eu', 2, para=False); txt = quieto(ato.trabalhar, E, 'eu', 4); p = E['gente']['eu']; pago = p['moedas'] == 10 - M.CAMA_PRECO + M.JORNADA * M.SALARIO['diarista'] and 'jornada' in txt
    de_novo = recusa(lambda: ato.trabalhar(E, 'eu', 1)); quieto(ato.passa, E, 'eu', 2, 'esperar', para=False); quieto(ato.dormir, E, 'eu', 2, para=False); quieto(ato.trabalhar, E, 'eu', 1); amanha = E['gente']['eu']['moedas'] == p['moedas'] - M.CAMA_PRECO + M.SALARIO['diarista']
    E2 = vila(caixa=1); sem_prata = recusa(lambda: ato.trabalhar(E2, 'eu', 1)) or ''; E3 = vila(prata=0); estado.aplica(E3, 'mestre', [['pessoa', 'eu', 'carga.comida', 'soma', 2], ['pessoa', 'eu', 'fome', 'soma', 5]], texto='fome e merenda')
    sem = recusa(lambda: ato.comer(E3, 'eu')) or ''; c0 = E3['lugares']['vila']['estoque']['comida']; quieto(ato.comer, E3, 'eu', da_carga=True); q = E3['gente']['eu']
    carga = q['corpo']['fome'] == 2 and q['carga'] == {'comida': 1} and q['moedas'] == 0 and E3['lugares']['vila']['estoque']['comida'] == c0
    ok('A JORNADA E A MERENDA: o lugar paga a cada pessoa no máximo 2 blocos de serviço por dia; sem prata, diz que não tem com que pagar; e quem carrega comida come da própria carga, sem pagar',
       f"pediu 4 blocos, trabalhou e recebeu {M.JORNADA}: {'sim' if pago else 'NÃO'}; mais um no mesmo dia: {'recusado' if de_novo else 'ACEITO'}; no dia seguinte, trabalha de novo: {'sim' if amanha else 'NÃO'}; "
       f"lugar com 1 de prata: «{sem_prata[:60]}»; sem prata no bolso, a taverna recusa («{sem[:44]}») e a carga serve: fome 5 → 2, a comida do lugar intacta: {'sim' if carga else 'NÃO'}",
       pago and de_novo and amanha and 'não tem prata' in sem_prata and 'custa' in sem and carga)
    # 17 os invariantes da etapa 2: o que se planta por fora é acusado, o valida nunca quebra, e o gravador recusa o mesmo estrago quando vem por evento
    def mundo2():
        E = vila(prata=300); estado.aplica(E, 'gera', [['lugar', 'vila', 'oficina', 'poe', 2], ['lugar', 'vila', 'pop', 'poe', 400], ['pessoa', 'eu', 'maestria.forja', 'poe', 4], ['pessoa', 'eu', 'carga.metal:2', 'soma', 3],
                                                       ['lugar', 'nasce', 'mata', dict(nome='a Mata', tipo='ermo', vizinhos=['vila'], bichos={'corça': 40}, teto={'corça': 80}, coleta={'erva:0': 10}, coleta_teto={'erva:0': 60})],
                                                       ['pessoa', 'nasce', 'bera', dict(nome='Bera', nivel=5, atributos=dict(E['gente']['eu']['atributos']), lugar='vila')],
                                                       ['item', 'nasce', item('nucleo', 3, 'Núcleo de prova', de='serpe', dono='eu')], ['item', 'nasce', item('arma', 0, 'Adaga da loja', familia='adaga', onde='vila')]], texto='o mundo da prova')
        quieto(oficio.forjar, E, 'eu', oficio.molde('arma', 3, 'Espada da Prova', familia='espada'), blocos=0); return E
    G = lambda E: E['gente']; Lg = lambda E: E['lugares']; I = lambda E: E['itens']['itens']; O = lambda E: E['itens']['obras']['o0001']
    saida = dict(ermo='mata', casa='vila', quer='caça', alvo=None, restam=2, com=[], dia=1, fase='procura', encontro=None, luta=None, lutas=0, parou=None, sangue=None)
    estragos = [('obra com 999 de 27 blocos', lambda E: O(E).update(blocos=999), [['obra', 'o0001', 'blocos', 'poe', 999]]), ('obra com blocos negativos', lambda E: O(E).update(blocos=-5), [['obra', 'o0001', 'blocos', 'soma', -5]]),
                ('obra num lugar que não existe', lambda E: O(E).update(lugar='lua'), [['obra', 'o0001', 'lugar', 'poe', 'lua']]), ('o núcleo da obra some do Livro', lambda E: I(E).pop('i0003'), None),
                ('o núcleo da obra em outra mão', lambda E: I(E)['i0003'].update(dono='bera'), None), ('a matéria da obra vira texto', lambda E: O(E).update(materia='nada'), [['obra', 'o0001', 'materia', 'poe', 'nada']]),
                ('núcleo sem dono e sem lugar', lambda E: I(E)['i0003'].update(dono=None), None), ('núcleo de categoria 42', lambda E: I(E)['i0003'].update(cat=42), [['item', 'nasce', dict(tipo='nucleo', cat=42, nome='torto', dur=[1, 1], dono='eu')]]),
                ('núcleo gasto', lambda E: I(E)['i0003'].update(dur=[0, 1]), [['item', 'i0003', 'dur', 'soma', -1]]), ('peça de um morto', lambda E: (G(E)['bera'].update(estado='morto', pv=0), I(E)['i0004'].update(dono='bera', onde=None)), None),
                ('peça solta com dono', lambda E: I(E)['i0001'].update(solto=True), [['item', 'i0001', 'solto', 'poe', True]]), ('morto com prata e carga', lambda E: G(E)['bera'].update(estado='morto', pv=0, moedas=9, carga={'comida': 2}), None),
                ('mais bichos do que o teto', lambda E: Lg(E)['mata']['bichos'].update(corça=999), None), ('espécie que não existe', lambda E: Lg(E)['mata']['bichos'].update(unicórnio=5), [['lugar', 'mata', 'bichos.unicórnio', 'poe', 5]]),
                ('contagem que não é número', lambda E: Lg(E)['mata']['bichos'].update(corça='muitas'), [['lugar', 'mata', 'bichos.corça', 'poe', 'muitas']]), ('a contagem inteira trocada por um texto', lambda E: Lg(E)['mata'].update(bichos='nenhum'), [['lugar', 'mata', 'bichos', 'poe', 'nenhum']]),
                ('matéria do ermo negativa', lambda E: Lg(E)['mata']['coleta'].update({'erva:0': -3}), [['lugar', 'mata', 'coleta.erva:0', 'poe', -3]]), ('povo negativo', lambda E: Lg(E)['vila'].update(pop=-50), [['lugar', 'vila', 'pop', 'poe', -50]]),
                ('oficina de nível 99', lambda E: Lg(E)['vila'].update(oficina=99), [['lugar', 'vila', 'oficina', 'poe', 99]]), ('preparo que alcança a categoria 99', lambda E: Lg(E)['vila'].update(preparo=dict(fogo=99)), [['lugar', 'vila', 'preparo.fogo', 'poe', 99]]),
                ('o lugar produz prata', lambda E: Lg(E)['vila'].update(produz=dict(prata=50)), [['lugar', 'vila', 'produz.prata', 'poe', 50]]), ('vizinho que não existe', lambda E: Lg(E)['vila'].update(vizinhos=['mata', 'lua']), [['lugar', 'vila', 'vizinhos', 'poe', ['mata', 'lua']]]),
                ('a saída de caça com lixo dentro', lambda E: G(E)['eu']['marca'].update(caca=dict(fase='luta', ermo='mata')), None), ('a saída para um ermo que não existe', lambda E: G(E)['eu']['marca'].update(caca=dict(saida, ermo='lua')), None),
                ('foi junto numa saída que não existe', lambda E: G(E)['bera']['marca'].update(caca=dict(de='eu', ermo='mata')), None), ('carga de um bem que não existe', lambda E: G(E)['eu']['carga'].update(unicórnio=2), [['pessoa', 'eu', 'carga.unicórnio', 'soma', 2]]),
                ('meia unidade na carga', lambda E: G(E)['eu']['carga'].update({'metal:2': 2.5}), [['pessoa', 'eu', 'carga.metal:2', 'soma', 0.5]]), ('maestria fora da escada', lambda E: G(E)['eu']['maestria'].update(forja=3), [['pessoa', 'eu', 'maestria.forja', 'poe', 3]]),
                ('grau de ofício que não existe', lambda E: G(E)['eu'].update(grau_oficio='rei'), [['pessoa', 'eu', 'grau_oficio', 'poe', 'rei']])]
    limpo = estado.valida(mundo2()); calados = []; quebrou = []; passou = []
    for nome, planta, efeitos in estragos:
        E = mundo2(); planta(E)
        try:
            if not estado.valida(E): calados.append(nome)
        except Exception as x: quebrou.append(f'{nome} ({type(x).__name__})')
        if efeitos:
            E = mundo2(); antes = retrato(E)
            if not recusa(lambda: estado.aplica(E, 'mestre', efeitos)) or antes != retrato(E): passou.append(nome)
    por_evento = sum(1 for _, _, ef in estragos if ef)
    ok('OS INVARIANTES DA ETAPA 2: os estragos plantados por fora nas estruturas novas (obra, núcleo, peça, ermo, lugar, saída, carga) são acusados um a um; o `valida` nunca quebra; e o gravador recusa o mesmo estrago quando ele vem por evento',
       f"limpo: {len(limpo)} problema(s); {len(estragos) - len(calados) - len(quebrou)} de {len(estragos)} estragos acusados" + (f" (calou em: {', '.join(calados)})" if calados else '') + (f" (QUEBROU em: {', '.join(quebrou)})" if quebrou else '')
       + f"; por evento `mestre`: {por_evento - len(passou)} de {por_evento} recusados, sem mudar nada" + (f" (passaram: {', '.join(passou)})" if passou else ''), not limpo and not calados and not quebrou and not passou)
    # 18 o evento que não muda nada não entra no registro
    E = vila(); E['relogio']['bloco'] = 0; n0 = E['relogio']['eventos']
    nulos = [estado.aplica(E, 'mestre', ef) for ef in ([['pessoa', 'eu', 'fome', 'soma', -3]], [['item', 'i0001', 'uso', 'poe', 'arma']], [['item', 'i0001', 'dur', 'soma', 5]], [['pessoa', 'eu', 'pv', 'soma', 50]], [['lugar', 'vila', 'cama', 'poe', True]])]
    calou = all(x is None for x in nulos) and E['relogio']['eventos'] == n0; vazio = recusa(lambda: estado.aplica(E, 'mestre', []))
    real = estado.aplica; cont = dict(todos=0, nulos=0)
    def conta(E, tipo, efeitos, **k):
        a = json.dumps({x: E[x] for x in ('lugares', 'gente', 'itens')}, sort_keys=True) + str(estado.agora(E)); ev = real(E, tipo, efeitos, **k)
        if ev: cont['todos'] += 1; cont['nulos'] += a == json.dumps({x: E[x] for x in ('lugares', 'gente', 'itens')}, sort_keys=True) + str(estado.agora(E))
        return ev
    estado.aplica = conta
    try:
        for _ in range(8): dia_de_rotina(E, comer=False, dormir=False)          # oito dias sem comer nem dormir: os medidores batem no teto, e os efeitos do corpo deixam de mudar número
    finally: estado.aplica = real
    ok('O QUE NÃO MUDA NÃO ACONTECEU: o evento cujos efeitos não mudam nada (somar no que já está no teto, pôr o que já está posto) não entra no registro; o evento sem efeito segue recusado',
       f"cinco eventos sem mudança: {'nenhum registrado' if calou else 'REGISTRADOS'}; evento vazio: {'recusado' if vazio else 'ACEITO'}; em oito dias sem comer nem dormir (o corpo no teto), {cont['todos']} eventos registrados, {cont['nulos']} sem mudança",
       calou and vazio and cont['todos'] > 40 and cont['nulos'] == 0)
    # 19 a cama é por noite
    conta_cama = lambda E: sum(1 for e in E['_novos'] if e['texto'].endswith('paga a cama'))
    E = vila(prata=20); p0 = prata_do_mundo(E)
    diz_mesa = False
    for antes_de_dormir in (0, 1, 2):                        # dorme nos blocos 0, 2 e 5 depois de pagar: três deitadas no prazo de uma cama
        quieto(ato.passa, E, 'eu', antes_de_dormir, 'esperar', para=False); quieto(ato.dormir, E, 'eu', 1, para=False); diz_mesa = diz_mesa or 'paga até o Dia 2, manhã' in turno.mesa(E)
    tres = (conta_cama(E), E['gente']['eu']['moedas'])
    quieto(ato.dormir, E, 'eu', 1, para=False); venceu = (conta_cama(E), E['gente']['eu']['moedas'])                                                        # o bloco 6 depois de pagar: o prazo venceu, paga outra noite
    E2 = vila(prata=20); quieto(ato.dormir, E2, 'eu', 8, para=False); longo = (conta_cama(E2), E2['gente']['eu']['moedas'], estado.agora(E2))                # oito blocos seguidos: duas noites
    E3 = vila(prata=3); txt = quieto(ato.dormir, E3, 'eu', 8, para=False); curto = (conta_cama(E3), E3['gente']['eu']['moedas'], estado.agora(E3) - 2)       # sem prata para a segunda noite: o sono para ali
    E4 = vila(prata=20); quieto(ato.dormir, E4, 'eu', 1, para=False)
    estado.aplica(E4, 'mestre', [['lugar', 'nasce', 'outra', dict(nome='a Outra Vila', em='na Outra Vila', tipo='vila', cama=True, estoque=dict(comida=10, prata=0))], ['pessoa', 'eu', 'lugar', 'poe', 'outra']], texto='muda de vila')
    quieto(ato.dormir, E4, 'eu', 1, para=False); outra = (conta_cama(E4), E4['gente']['eu']['moedas'])                                                      # em outro lugar, outra cama
    E5 = vila(prata=20); quieto(ato.dormir, E5, 'eu', 1, chao=True, para=False); chao = (conta_cama(E5), E5['gente']['eu']['moedas'])
    fecha = all(prata_do_mundo(x) == p0 for x in (E, E2, E4, E5)) and not any(estado.valida(x) for x in (E, E2, E3, E4, E5))
    ok(f'A CAMA É POR NOITE: a cama paga vale {M.CAMA_VALE} blocos (um dia inteiro) a contar do bloco em que se pagou, no lugar onde se pagou; dormir de novo nesse prazo não cobra; passado o prazo, ou em outro lugar, paga-se outra; a MESA diz até quando está paga',
       f"três deitadas no mesmo dia: {tres[0]} cama paga, prata 20 → {tres[1]}; a MESA diz até quando: {'sim' if diz_mesa else 'NÃO'}; a quarta, com o prazo vencido: {venceu[0]} pagas, prata {venceu[1]}; oito blocos seguidos: {longo[0]} noites pagas, prata {longo[1]}; "
       f"com 3 de prata, o sono de oito para em {curto[2]} blocos («{txt.split('PAROU: ')[-1][:38]}»); em outro lugar: {outra[0]} pagas, prata {outra[1]}; no chão: {chao[0]} pagas; a prata do mundo {'fecha' if fecha else 'NÃO FECHA'}",
       tres == (1, 18) and diz_mesa and venceu == (2, 16) and longo == (2, 16, 10) and curto == (1, 1, 6) and 'a cama paga venceu' in txt and outra == (2, 16) and chao == (0, 20) and fecha)
    # 20 a luta aberta tranca o mundo
    import caca
    d = tempfile.mkdtemp(prefix='m10_'); os.environ['MOTOR10_MUNDO'] = d
    try:
        E = vila(prata=40); at = dict(E['gente']['eu']['atributos'])
        estado.aplica(E, 'gera', [['lugar', 'vila', 'oficina', 'poe', 1], ['pessoa', 'eu', 'carga.comida', 'soma', 3], ['pessoa', 'eu', 'carga.metal:0', 'soma', 3], ['pessoa', 'eu', 'fome', 'soma', 4],
                                  ['pessoa', 'nasce', 'bera', dict(nome='Bera', nivel=5, atributos=at, lugar='vila', moedas=20)], ['item', 'nasce', item('arma', 0, 'Adaga de prova', familia='adaga', dono='eu')],
                                  ['lugar', 'nasce', 'mata', dict(nome='a Mata', em='na Mata', tipo='ermo', vizinhos=['vila'], bichos={'corça': 80}, teto={'corça': 80}, coleta={'madeira:0': 50}, coleta_teto={'madeira:0': 50})],
                                  ['lugar', 'vila', 'vizinhos', 'poe', ['mata']]], texto='o mundo da prova')
        quieto(mercado.funda, E, 'vila', 400); estado.grava(E)
        json.dump(dict(inicio='colado', A=[dict(id='eu', controla=True)], B=[dict(nome='o ladrão de galinhas', nivel=3, molde='comum', veste=dict(arma=['adaga', 'Comum']))]), open(os.path.join(d, 'cen.json'), 'w'))
        arq = os.path.join(d, 'briga.json'); quieto(ato.luta_nova, E, os.path.join(d, 'cen.json'), arq); antes = retrato(E); relogio = estado.agora(E)
        atos = [('dormir', lambda: ato.dormir(E, 'eu', 1)), ('comer', lambda: ato.comer(E, 'eu')), ('comer da carga', lambda: ato.comer(E, 'eu', da_carga=True)), ('trabalhar', lambda: ato.trabalhar(E, 'eu', 1)),
                ('treinar', lambda: ato.treinar(E, 'eu', 1, 'espada')), ('descansar', lambda: ato.descansar(E, 'eu', 1)), ('esperar', lambda: ato.esperar(E, 'eu', 1)), ('vestir', lambda: ato.vestir(E, 'eu', 'i0003', 'arma2')),
                ('tirar', lambda: ato.tirar(E, 'eu', 'i0001')), ('outra pessoa espera', lambda: ato.esperar(E, 'bera', 1)), ('outra pessoa dorme', lambda: ato.dormir(E, 'bera', 2)), ('comprar', lambda: mercado.comprar(E, 'eu', 'comida', 1)),
                ('vender', lambda: mercado.vender_cesta(E, 'eu')), ('outra pessoa compra', lambda: mercado.comprar(E, 'bera', 'comida', 1)), ('servir na forja', lambda: oficio.jornal(E, 'eu', 1)),
                ('forjar', lambda: oficio.forjar(E, 'eu', oficio.molde('arma', 0, 'Adaga nova', familia='adaga'), blocos=1)), ('outra pessoa sai para caçar', lambda: caca.sair(E, 'bera', 'mata', blocos=1)),
                ('outra pessoa sai para tirar lenha', lambda: caca.coletar(E, 'bera', 'madeira:0', 'mata', blocos=1)), ('abrir outra luta', lambda: ato.luta_nova(E, os.path.join(d, 'cen.json'), os.path.join(d, 'briga2.json'))),
                ('fechar o turno', lambda: turno.fecha(E, 'no meio da luta')), ('um evento de compra direto no gravador', lambda: estado.aplica(E, 'compra', [['pessoa', 'eu', 'moedas', 'soma', -1], ['estoque', 'vila', 'prata', 'soma', 1]])),
                ('um evento do gerador', lambda: estado.aplica(E, 'gera', [['pessoa', 'eu', 'moedas', 'soma', 5]])), ('o relógio direto no gravador', lambda: estado.aplica(E, 'esperar', [['relogio', 1]]))]
        frases = [(nome, recusa(f)) for nome, f in atos]; rec = [nome for nome, fr in frases if fr]; diz = all(fr and 'luta aberta' in fr and 'ato.py luta roda' in fr and 'ato.py luta larga' in fr for _, fr in frases if _ != 'fechar o turno')
        parado = antes == retrato(E) and relogio == estado.agora(E); mesa_diz = 'LUTA ABERTA' in turno.mesa(E).split('## Você')[0]
        mestre = bool(estado.aplica(E, 'mestre', [['pessoa', 'eu', 'moedas', 'soma', 1]], texto='a mão do Mestre passa'))
        for _ in range(200):
            S = json.load(open(arq, encoding='utf-8'))
            if S['fim']: break
            quieto(ato.luta_roda, E, arq, ['Aldric: atacar'] if S['L'][0]['estado'] == 'pe' else [])
        S = json.load(open(arq, encoding='utf-8')); acabou = bool(S['fim']) and not estado.luta_aberta(E); vivo = E['gente']['eu']['estado'] == 'vivo'
        depois = recusa(lambda: ato.esperar(E, 'bera', 1)) is None and estado.agora(E) == relogio + 1                                      # acabada a luta, o mundo anda de novo
        json.dump(dict(inicio='longe', A=[dict(id='bera', controla=True)], B=[dict(nome='o ladrão de galinhas', nivel=3, molde='comum', veste=dict(arma=['adaga', 'Comum']))]), open(os.path.join(d, 'cen2.json'), 'w'))
        quieto(ato.luta_nova, E, os.path.join(d, 'cen2.json'), os.path.join(d, 'briga3.json')); trancou = bool(recusa(lambda: ato.esperar(E, 'bera', 1)))
        quieto(ato.luta_larga, E, os.path.join(d, 'briga3.json'), 'a cena mudou'); solta = trancou and recusa(lambda: ato.esperar(E, 'bera', 1)) is None       # o Mestre solta a luta, e o mundo anda
        # a caça não quebra: a luta de caça abre (a nota da saída entra), tranca o mundo para os outros, roda pelo `caca.py luta`, e as contas saem
        cacou = None
        if E['gente']['bera']['estado'] == 'vivo':
            estado.aplica(E, 'mestre', [['pessoa', 'bera', 'fome', 'soma', -10], ['pessoa', 'bera', 'sono', 'soma', -10], ['pessoa', 'bera', 'cansaco', 'soma', -10], ['pessoa', 'nasce', 'caio', dict(nome='Caio', nivel=5, atributos=at, lugar='vila', moedas=20)],
                                        ['item', 'nasce', item('arma', 0, 'Arco da Bera', familia='arco', dono='bera')]], texto='a Bera se apronta')
            estado.aplica(E, 'mestre', [['item', f"i{E['itens']['seq']:04d}", 'uso', 'poe', 'arma']], texto='a Bera empunha o arco')
            for _ in range(40):
                R = quieto(caca.sair, E, 'bera', 'mata', alvo='corça', blocos=4)
                if R.get('fase') == 'encontro' or E['gente']['bera']['estado'] != 'vivo': break
                if caca.saida(E['gente']['bera']): quieto(caca.volta, E, 'bera')                                                           # o corpo pediu no meio da procura: volta, e tenta de novo
                estado.aplica(E, 'mestre', [['pessoa', 'bera', 'fome', 'soma', -10], ['pessoa', 'bera', 'sono', 'soma', -10], ['pessoa', 'bera', 'cansaco', 'soma', -10]], texto='a Bera descansa')
            if R.get('fase') == 'encontro':
                R = quieto(caca.atacar, E, 'bera'); s = caca.saida(E['gente']['bera']); antes = retrato(E); frase = estado.luta_diz(E) or ''
                aberta = R.get('fase') == 'luta' and s['fase'] == 'luta' and estado.luta_aberta(E) == s['luta'] and 'caca.py luta' in frase and 'quem=bera' in frase
                presos = [recusa(f) for f in (lambda: ato.esperar(E, 'caio', 1), lambda: caca.sair(E, 'caio', 'mata', blocos=1), lambda: caca.volta(E, 'bera'), lambda: ato.comer(E, 'eu') if vivo else ato.esperar(E, 'caio', 2))]
                preso = all(presos) and antes == retrato(E)
                for _ in range(80):
                    try: R = quieto(caca.luta_roda, E, 'bera', ['Bera: atacar'])
                    except SystemExit: R = quieto(caca.luta_roda, E, 'bera', [])
                    if R.get('fase') != 'luta': break
                cacou = aberta and preso and R.get('fase') != 'luta' and not estado.luta_aberta(E) and recusa(lambda: ato.esperar(E, 'caio', 1)) is None and not estado.valida(E)
        ok('A LUTA ABERTA TRANCA O MUNDO: enquanto há luta aberta, nenhum ato que grava é aceito, de ninguém (nem o relógio anda), fora a própria luta e a mão do Mestre; a recusa diz como acabar ou soltar a luta; acabada ou solta, o mundo anda de novo; e a caça segue inteira',
           f"{len(rec)} de {len(atos)} atos recusados com a luta aberta" + (f" (passaram: {', '.join(n for n, fr in frases if not fr)})" if len(rec) < len(atos) else '') + f"; a frase diz como seguir e como soltar: {'sim' if diz else 'NÃO'}; o estado e o relógio {'não mexeram' if parado else 'MEXERAM'}; "
           f"a MESA abre com o aviso: {'sim' if mesa_diz else 'NÃO'}; a mão do Mestre passa: {'sim' if mestre else 'NÃO'}; a luta acaba pelo `ato.py luta roda` e o mundo anda: {'sim' if acabou and depois else 'NÃO'}; o Mestre solta outra com `luta larga`: {'sim' if solta else 'NÃO'}; "
           f"na caça: a luta abre, tranca os outros, roda pelo `caca.py luta` e fecha com as contas: {'sim' if cacou else 'NÃO' if cacou is not None else 'o encontro de prova não saiu'}",
           len(rec) == len(atos) and diz and parado and mesa_diz and mestre and acabou and depois and solta and cacou)
    finally:
        os.environ.pop('MOTOR10_MUNDO', None); shutil.rmtree(d, ignore_errors=True)
    # 21 o RETOMAR não corta calado
    d = tempfile.mkdtemp(prefix='m10_'); os.environ['MOTOR10_MUNDO'] = d
    def dia(E):                                              # um dia de atos pela porta da frente: dorme dois blocos, come, trabalha dois, espera dois
        ato.dormir(E, 'eu', 2, para=False); ato.comer(E, 'eu'); ato.trabalhar(E, 'eu', 2); ato.esperar(E, 'eu', 2)
    try:
        E = vila(prata=60); estado.aplica(E, 'gera', [['lugar', 'nasce', 'mata', dict(nome='a Mata', tipo='ermo', vizinhos=['vila'], bichos={'corça': 1000}, teto={'corça': 2000})], ['pessoa', 'eu', 'fome', 'soma', 1]], texto='o mundo da prova')
        quieto(mercado.funda, E, 'vila', 400); E['relogio']['bloco'] = 0; E['turno'].update(aberto=dict(dia=1, bloco=0), evento0=E['relogio']['eventos']); estado.grava(E)
        E = estado.carrega(); estado.aplica(E, 'mestre', [['pessoa', 'eu', 'moedas', 'soma', 1]], texto='O PRIMEIRO FATO: achou uma moeda no Dia 1')
        for _ in range(2): quieto(dia, E)
        turno.pergunta(E, 'a?', ['a=x', 'b=y']); turno.pergunta(E, 'b?', ['a=x', 'b=y']); todos = turno._eventos_desde(E['turno']['evento0']) + E['_novos']
        with contextlib.redirect_stdout(io.StringIO()): turno.fecha(E, 'dois dias de rotina')
        ret = open(os.path.join(d, 'RETOMAR.md'), encoding='utf-8').read(); linhas = [x for x in ret.split('**Os fatos do turno**')[1].split('## PERGUNTAS')[0].splitlines() if x.startswith('- ')]
        tipos = {e['tipo'] for e in todos}; rotina = [x for x in linhas if 'a rotina:' in x]; n_curto = len(linhas)
        curto = ('O PRIMEIRO FATO' in ret and 'ficaram de fora' not in ret and len(rotina) == 2 and all('come' in x and 'paga a cama' in x and 'dorme (na cama) (× 2)' in x for x in rotina)
                 and {'producao', 'consumo', 'ninhada', 'virada'} <= tipos and 'se refaz' not in ret and 'o dia vira' not in ret and len(linhas) == 1 + 2 + 2)        # o primeiro fato, a rotina de cada dia, o trabalho de cada dia
        E = estado.carrega(); estado.aplica(E, 'mestre', [['pessoa', 'eu', 'moedas', 'soma', 1]], texto='O FATO MAIS ANTIGO do turno comprido')
        for j in range(6):
            quieto(dia, E)
            for k in range(8): estado.aplica(E, 'mestre', [['pessoa', 'eu', 'moedas', 'soma', 1]], texto=f'fato {k + 1} do dia {j + 1} do turno comprido')
        turno.pergunta(E, 'c?', ['a=x', 'b=y']); todos = turno._eventos_desde(E['turno']['evento0']) + E['_novos']; inteiras = turno.fatos(todos, teto=10 ** 9)
        with contextlib.redirect_stdout(io.StringIO()): turno.fecha(E, 'seis dias cheios')
        ret = open(os.path.join(d, 'RETOMAR.md'), encoding='utf-8').read(); linhas = [x for x in ret.split('**Os fatos do turno**')[1].split('## PERGUNTAS')[0].splitlines() if x.startswith('- ')]
        fora = len(inteiras) - (len(linhas) - 1); aviso = linhas[0] if linhas else ''
        comprido = (len(inteiras) > M.RETOMAR_FATOS and len(linhas) == M.RETOMAR_FATOS and f'ficaram de fora {fora} fatos mais antigos' in aviso and f'estado.py eventos {len(todos)}' in aviso and linhas[1:] == inteiras[fora:]
                    and 'O FATO MAIS ANTIGO' not in ret and 'fato 8 do dia 6' in ret)
        # o evento gravado SEM TEXTO (a mão do Mestre, por código) não some calado: entra nos fatos com o número e o tipo dele
        E = estado.carrega(); ev = estado.aplica(E, 'mestre', [['pessoa', 'eu', 'moedas', 'soma', 500]], texto=''); turno.pergunta(E, 'd?', ['a=x', 'b=y']); ato.esperar(E, 'eu', 1)
        with contextlib.redirect_stdout(io.StringIO()): turno.fecha(E, 'quinhentas moedas sem dizer de onde')
        ret2 = open(os.path.join(d, 'RETOMAR.md'), encoding='utf-8').read(); mudo = f"(evento #{ev['id']}, mestre, sem texto" in ret2.split('**Os fatos do turno**')[1]
        ok('O RETOMAR NÃO CORTA CALADO: o que se repete todo dia (comer, dormir, a cama, esperar) vira uma linha por dia; o mundo andando sozinho (a virada, a produção, o consumo, o ermo que se refaz) não entra; se os fatos passam do teto, a primeira linha diz quantos ficaram de fora e como lê-los; '
           'e o evento gravado sem texto entra com o número dele',
           f"turno de dois dias: {n_curto} linhas, a rotina numa linha por dia, o primeiro fato lá, nenhum aviso de corte: {'sim' if curto else 'NÃO'}; turno de seis dias cheios: {len(inteiras)} linhas de fatos para um teto de {M.RETOMAR_FATOS}; "
           f"a primeira linha avisa («{aviso[2:70]}...»): {'sim' if comprido else 'NÃO'}; o evento do Mestre gravado sem texto (500 de prata) aparece nos fatos com o número dele: {'sim' if mudo else 'NÃO'}; RETOMAR {len(ret.encode())} bytes",
           curto and comprido and mudo and len(ret.encode()) <= 6000)
    finally:
        os.environ.pop('MOTOR10_MUNDO', None); shutil.rmtree(d, ignore_errors=True)
    # 22 o sob medida é de uma pessoa, não de um nome
    E = vila(); at = dict(E['gente']['eu']['atributos'])
    estado.aplica(E, 'gera', [['pessoa', 'nasce', 'xara', dict(nome='Aldric', nivel=1, atributos=at, lugar='vila')], ['item', 'nasce', item('arma', 2, 'Espada sob medida', familia='espada', dono='eu', sob=dict(dono='Aldric', grau=2, id='eu'))],
                              ['item', 'nasce', item('arma', 2, 'Espada antiga', familia='espada', dono='xara', sob=dict(dono='Aldric', grau=2))]], texto='dois de mesmo nome')
    nova, antiga = (f'i{k:04d}' for k in (3, 4)); estado.aplica(E, 'gera', [['item', nova, 'uso', 'poe', 'arma'], ['item', antiga, 'uso', 'poe', 'arma']], texto='empunham')
    dono = ficha(estado.lutador(E, 'eu'))['arma']; estado.aplica(E, 'mestre', [['item', nova, 'dono', 'poe', 'xara'], ['item', antiga, 'dono', 'poe', 'eu']], texto='trocam de espada')
    estado.aplica(E, 'gera', [['item', nova, 'uso', 'poe', 'arma'], ['item', antiga, 'uso', 'poe', 'arma']], texto='empunham'); xara = ficha(estado.lutador(E, 'xara'))['arma']; pelo_nome = ficha(estado.lutador(E, 'eu'))['arma']
    ok('SOB MEDIDA É DE UMA PESSOA, NÃO DE UM NOME: a peça ajustada guarda o id do dono; na mão de outro de MESMO NOME rende uma categoria abaixo; a peça antiga, que só guarda o nome, segue valendo pelo nome',
       f"no dono: × {dono['mult']:g}, acerto +{dono['acerto']:g}; na mão do xará (mesmo nome, outro id): × {xara['mult']:g}, acerto +{xara['acerto']:g}; a peça sem id, pelo nome: × {pelo_nome['mult']:g}",
       dono['mult'] == T.MULT[2] and xara['mult'] == T.MULT[1] and xara['acerto'] < dono['acerto'] and pelo_nome['mult'] == T.MULT[2])
    # 23 as entradas tortas: uma frase por erro, e nada cobrado
    import subprocess
    E = vila(prata=10); antes = retrato(E); sem_fome = recusa(lambda: ato.comer(E, 'eu')) or ''; estado.aplica(E, 'mestre', [['pessoa', 'eu', 'carga.comida', 'soma', 1]], texto='merenda'); a2 = retrato(E)
    sem_fome2 = recusa(lambda: ato.comer(E, 'eu', da_carga=True)) or ''; nada = 'não tem fome' in sem_fome and 'não tem fome' in sem_fome2 and a2 == retrato(E) and E['gente']['eu']['moedas'] == 10
    E2 = vila(prata=10); E2['lugares']['vila']['estoque']['comida'] = 0; estado.aplica(E2, 'mestre', [['pessoa', 'eu', 'fome', 'soma', 5]], texto='fome'); sem_comida = recusa(lambda: ato.comer(E2, 'eu')) or ''
    E3 = vila(prata=1); estado.aplica(E3, 'mestre', [['pessoa', 'eu', 'sono', 'soma', 5]], texto='sono'); sem_cama = recusa(lambda: ato.dormir(E3, 'eu', 2)) or ''
    E4 = vila(prata=50); estado.aplica(E4, 'gera', [['lugar', 'vila', 'oficina', 'poe', 1], ['item', 'i0001', 'dur', 'soma', -1]], texto='a espada gasta um ponto'); so_um = quieto(oficio.consertar, E4, 'eu', 'i0001', pontos=5, pago=True)['texto']
    d = tempfile.mkdtemp(prefix='m10_'); amb = dict(os.environ, MOTOR10_MUNDO=d, PYTHONDONTWRITEBYTECODE='1'); aqui = os.path.dirname(os.path.abspath(__file__))
    try:
        os.environ['MOTOR10_MUNDO'] = d; E = vila(); estado.aplica(E, 'gera', [['lugar', 'vila', 'oficina', 'poe', 1]], texto='a oficina'); estado.grava(E); os.environ.pop('MOTOR10_MUNDO', None)
        def roda(*a, mundo=True):
            r = subprocess.run([sys.executable] + list(a), cwd=aqui, env=amb if mundo else {k: v for k, v in amb.items() if k != 'MOTOR10_MUNDO'} | dict(MOTOR10_MUNDO=os.path.join(d, 'nao_ha')), capture_output=True, text=True)
            return (r.stdout + r.stderr).strip()
        tortas = [('oficio.py', 'jornal', '0'), ('oficio.py', 'jornal', 'x'), ('mercado.py', 'funda', 'abc'), ('mercado.py', 'funda', '-5'), ('ato.py', 'dormir', 'muito'), ('ato.py', 'treinar', '2'), ('ato.py', 'vestir'),
                  ('oficio.py', 'consertar'), ('mercado.py', 'comprar'), ('teste.py', 'abrir a porta'), ('turno.py', 'responde'), ('caca.py', 'coletar'), ('estado.py', 'mestre', '[["pessoa","eu","moedas","soma",500]]', ''),
                  ('ato.py', 'luta', 'nova', os.path.join(aqui, 'dados', 'cenario_exemplo.json'), os.path.join(d, 'pasta_que_nao_ha', 'luta.json'))]
        saidas = [(' '.join(a), roda(*a)) for a in tortas]; frase = [n for n, o in saidas if o and len(o.splitlines()) == 1 and 'Traceback' not in o and 'Uso' not in o]
        corpo_uso = roda('corpo.py', mundo=False); usa = 'Uso' in corpo_uso and 'não há mundo' not in corpo_uso and 'Traceback' not in corpo_uso; corpo_ver = roda('corpo.py', 'ver')
        os.environ['MOTOR10_MUNDO'] = d; intacto = estado.carrega()['gente']['eu']['moedas'] == 30 and not estado.carrega()['turno']['lutas']; os.environ.pop('MOTOR10_MUNDO', None)      # nenhum dos pedidos tortos cobrou, deu prata ou abriu luta
        # a luta aberta só com o nome do arquivo fica DENTRO do save (em lutas/, criada na hora), e o save guarda o caminho relativo: a luta vai junto se a pasta mudar de lugar
        cen = os.path.join(d, 'cen.json'); json.dump(dict(inicio='perto', A=[dict(id='eu', controla=True)], B=[dict(nome='lobo 1', bicho='lobo')]), open(cen, 'w', encoding='utf-8'), ensure_ascii=False)
        nova = roda('ato.py', 'luta', 'nova', cen, 'briga.json'); os.environ['MOTOR10_MUNDO'] = d; guardada = estado.carrega()['turno']['lutas']; pelo_nome = ato._arq_luta('briga.json'); os.environ.pop('MOTOR10_MUNDO', None)
        dentro = (os.path.exists(os.path.join(d, 'lutas', 'briga.json')) and not os.path.exists(os.path.join(aqui, 'briga.json')) and guardada == [dict(arq=os.path.join('lutas', 'briga.json'), fim=None)] and 'lutas/briga.json' in nova
                  and 'Traceback' not in nova and pelo_nome == os.path.join(d, 'lutas', 'briga.json') and 'largada' in roda('ato.py', 'luta', 'larga', 'briga.json', 'fim da prova'))      # o `luta roda` e o `luta larga` acham a luta só pelo nome
    finally:
        os.environ.pop('MOTOR10_MUNDO', None); shutil.rmtree(d, ignore_errors=True)
    ok('AS ENTRADAS TORTAS: o pedido errado ganha UMA frase que diz o que está errado (não o uso inteiro, nem erro de programa), e nada é cobrado: comer sem fome, lugar sem comida, cama sem prata, conserto pedido a mais, número que não é número',
       f"comer sem fome (na taverna e da carga): recusado, sem cobrar: {'sim' if nada else 'NÃO'} («{sem_fome[:34]}»); lugar sem comida: «{sem_comida[:38]}»; cama sem prata: «{sem_cama[:28]}»; conserto de 5 pontos numa peça com 1 gasto avisa: {'sim' if 'só tinha' in so_um else 'NÃO'}; "
       f"{len(frase)} de {len(tortas)} comandos tortos respondem com uma frase só (entre eles: o evento do Mestre sem texto, `caca.py coletar` sem dizer o quê, a luta nova numa pasta que não existe)" + (f" (não: {', '.join(n for n, o in saidas if n not in frase)})" if len(frase) < len(tortas) else '')
       + f", e nada mudou: {'sim' if intacto else 'NÃO'}; `corpo.py` sem argumento só diz o uso, sem abrir mundo: {'sim' if usa else 'NÃO'}; a luta aberta só com o nome do arquivo fica dentro do save, em lutas/, com o caminho relativo guardado: {'sim' if dentro else 'NÃO'}",
       nada and 'não há comida' in sem_comida and 'a cama custa' in sem_cama and 'só tinha' in so_um and len(frase) == len(tortas) and intacto and usa and 'Aldric' in corpo_ver and dentro)
    # 24 a língua da mesa: as frases de gente não dependem de gênero; a categoria não se diz duas vezes; a unidade certa
    E = vila(); p = E['gente']['eu']; ditos = []
    for fome in (0, 4, 7):
        for sono in (0, 6, 8):
            for cansaco in (0, 9):
                antes_c = corpo.faixas(p); p['corpo'].update(fome=fome, sono=sono, cansaco=cansaco); ditos += [corpo.diz(p), corpo.cruzou(p, dict(fome=0, sono=0, cansaco=0)) or '']
    p['corpo'].update(fome=1, sono=3, cansaco=3); ditos.append(quieto(ato.dormir, E, 'eu', 3)); estado.aplica(E, 'gera', [['lugar', 'vila', 'oficina', 'poe', 1], ['pessoa', 'eu', 'treino.comércio', 'soma', 1], ['pessoa', 'eu', 'treino.espada', 'soma', 1]], texto='um dia de negócio')
    pede = oficio.pede(E, 'eu', oficio.molde('arma', 2, familia='espada')); voce = '\n'.join(turno._voce(E)); luta.semente(3)
    S = luta.nova([estado.lutador(E, 'eu')], [estado.lutador(E, 'eu', nome='a outra', id=None)], inicio='colado', quieto=False); S['L'][0]['estado'] = 'caido'; S['L'][1]['estado'] = 'morto'; S['L'][0]['abalado'] = True; S['fim'] = 'B'; quadro = luta.situacao(S); fim = luta.resultado_diz(S); luta.D = luta.Dados()
    ruins = [w for w in ('exausto', 'faminto', 'desperto', 'descansado', 'inteiro (', 'CAÍDO', 'MORTO', 'abalado', 'atordoado', 'mortos:', 'caídos:', 'bloco(s)', 'Raro (Raro)', '1 blocos') if w in '\n'.join(ditos + [pede, voce, quadro, fim])]
    # o sinal de menos e a vírgula da mesa; e do morto só se diz que morreu
    from itens import janela
    S2 = luta.nova([estado.lutador(E, 'eu')], [estado.lutador(E, 'eu', nome='a outra', id=None)], inicio='colado', quieto=False); luta._ferida(S2, S2['L'][1], 'braços', False, luta.arma_de(S2, S2['L'][0]), 5); ferida = S2['log'][-1]
    gibao = janela(E['itens']['itens']['i0002']); estado.aplica(E, 'mestre', [['pessoa', 'eu', 'estado', 'poe', 'morto'], ['pessoa', 'eu', 'pv', 'soma', -999]], texto='morre, para a prova'); morto = '\n'.join(turno._voce(E))
    miudos = '−' in ferida and not any(c + ' no acerto' in ferida for c in ('-1', '-2', '-3', '-4')) and 'Proteção: 0,7' in gibao and '0.7' not in gibao and 'MORREU' in morto and 'MORREU:' not in morto and 'com forças' not in morto and 'sem fome' not in morto
    certo = (not ruins and 'no limite das forças' in ''.join(ditos) and 'acorda com o sono em dia' in ditos[-1] and pede.startswith('espada Rara ·') and 'comércio: 1 dia de negócio' in voce and 'espada: 1 bloco' in voce
             and 'CAIU' in quadro and 'MORREU' in quadro and 'fraquejou' in quadro and 'morreram: a outra' in fim and 'caíram: Aldric' in fim and miudos)
    ok('A LÍNGUA DA MESA: as frases de gente servem a qualquer pessoa (não dependem de gênero); a categoria concorda com a peça e não se diz duas vezes; o comércio conta dias de negócio, e o plural é plural',
       f"o corpo, o sono, o quadro e o fim da luta: {'nenhuma palavra presa a gênero' if not ruins else 'SOBROU: ' + ', '.join(ruins)}; «{ditos[-1].split('PAROU: ')[-1]}»; `oficio.py pede arma espada Raro` abre com «{pede.split(' · ')[0]}»; "
       f"o treino na MESA: «{voce.split('Treino: ')[-1]}»; o quadro diz CAIU e MORREU; o fim: «{fim}»; a ferida no braço com o sinal de menos da mesa («{ferida.strip().split(': ')[-1]}»), a janela com vírgula («{gibao.splitlines()[2].split('      ')[0]}»), "
       f"e do morto a MESA só diz que morreu: {'sim' if miudos else 'NÃO'}", certo)
    # 25 as perguntas guardam o número com que foram abertas, até o turno fechar
    d = tempfile.mkdtemp(prefix='m10_'); os.environ['MOTOR10_MUNDO'] = d
    try:
        E = vila(); turno.pergunta(E, 'Forja ou caça?', ['a=forja', 'b=caça']); turno.pergunta(E, 'Segue na forja?', ['a=segue', 'b=vai caçar']); quieto(ato.esperar, E, 'eu', 1)
        quieto(turno.fecha, E, 'um bloco de espera'); ret = open(os.path.join(d, 'RETOMAR.md'), encoding='utf-8').read(); lido = '1. Forja ou caça?' in ret and '2. Segue na forja?' in ret
        E = estado.carrega(); r1 = turno.responde(E, '1a'); estado.grava(E); E = estado.carrega(); de_novo = recusa(lambda: turno.responde(E, '1a')) or ''; outra = recusa(lambda: turno.responde(E, '1b')) or ''; fora = recusa(lambda: turno.responde(E, '3a')) or ''
        r2 = turno.responde(E, '2b'); resp = [(r['n'], r['cod'], r['texto']) for r in E['turno']['respondidas']]; n3 = turno.pergunta(E, 'E amanhã?', ['a=dorme', 'b=treina']); mesa = turno.mesa(E)
        turno.pergunta(E, 'E depois?', ['a=fica', 'b=parte']); quieto(ato.esperar, E, 'eu', 1); quieto(turno.fecha, E, 'respondeu as duas'); ret2 = open(os.path.join(d, 'RETOMAR.md'), encoding='utf-8').read(); E = estado.carrega()
        certo = (lido and 'Ficam abertas: 2.' in r1 and 'já foi respondida' in de_novo and 'já foi respondida' in outra and 'não bate em nenhuma pergunta aberta' in fora and r2.startswith('2b: Segue na forja? → vai caçar')
                 and resp == [(1, 'a', 'Forja ou caça?'), (2, 'b', 'Segue na forja?')] and n3.startswith('pergunta 1 aberta: é o número dela na lista do RETOMAR') and 'guarda como 3' in n3 and '3. E amanhã?' in mesa and '1. E amanhã?' in ret2 and '2. E depois?' in ret2 and [q['n'] for q in E['turno']['perguntas']] == [1, 2])
    finally:
        os.environ.pop('MOTOR10_MUNDO', None); shutil.rmtree(d, ignore_errors=True)
    ok('AS PERGUNTAS GUARDAM O NÚMERO com que foram abertas até o turno fechar: responder uma não muda o número das outras; a já respondida recusa segunda resposta; a pergunta nova ganha o número seguinte; no fechar, as que ficam são numeradas de novo, de 1 em diante',
       f"com as perguntas 1 e 2 do RETOMAR abertas: `responde 1a` deixa a outra como 2 («{r1.splitlines()[-1]}»); `responde 1a` de novo e `responde 1b`: {'recusados' if de_novo and outra else 'ACEITOS'} («{de_novo[:44]}...»); `responde 2b` marca a segunda («{r2}»); "
       f"a pergunta aberta depois fica no caderno como 3 até o turno fechar, e o comando diz o número que ela terá na lista do RETOMAR («{n3.split(':')[0]}»); fechado o turno, o RETOMAR as lista como 1 e 2: {'sim' if certo else 'NÃO'}", certo)
    return out


def provas_volta3(n=300):
    """ETAPA 2, o acerto da terceira volta: o relógio único e o corpo de quem não é o personagem (o tempo passa para o personagem, aja quem agir; quem não é o personagem
    descansa em casa quando não está em cena); o dia de luta ou de saída ao ermo não é repouso; a última linha que não mente; o registro da luta que fecha a conta;
    o RETOMAR que só junta o que vem seguido; as perguntas como o jogador escreve; a MESA de quem morreu; e as frases acertadas."""
    import re, subprocess
    import oficio, mercado, caca, bichos, pessoas
    out = []; ok = lambda nome, deu, passa: out.append((nome, deu, bool(passa))); sn = lambda x: 'sim' if x else 'NÃO'
    prata_do_mundo = lambda E: sum(p['moedas'] for p in E['gente'].values()) + sum(l['estoque'].get('prata', 0) for l in E['lugares'].values())
    def quieto(f, *a, **k):
        with contextlib.redirect_stdout(io.StringIO()): return f(*a, **k)
    def mais_um(E, pid='zeca', nome='Zeca', **mais):          # mais uma pessoa com ficha na vila de prova (nasce por evento)
        estado.aplica(E, 'gera', [['pessoa', 'nasce', pid, dict(nome=nome, nivel=3, atributos=dict(E['gente']['eu']['atributos']), lugar='vila', moedas=20, **mais)]], texto=f'{nome} nasce')
    def mundo2(**k):
        E = vila(**k); mais_um(E); E['relogio']['bloco'] = 0; return E
    tempo = lambda E, blocos: estado.aplica(E, 'tempo', [['relogio', blocos]], texto='o tempo passa, sem ninguém em cena')
    # 1 o tempo passa para o personagem, aja quem agir (J3)
    E = mundo2(); t0 = estado.agora(E); r1 = quieto(ato.esperar, E, 'zeca', 6); seis = (estado.agora(E) - t0, dict(E['gente']['eu']['corpo']), dict(E['gente']['zeca']['corpo'])); linha = ato.ultima_linha(E, 'zeca')
    E2 = mundo2(); E2['gente']['eu']['corpo']['sono'] = 3; t0 = estado.agora(E2); r2 = quieto(ato.esperar, E2, 'zeca', 6); parou = (estado.agora(E2) - t0, E2['gente']['eu']['corpo']['sono'], E2['gente']['zeca']['corpo']['sono'])
    E3 = mundo2(); estado.aplica(E3, 'mestre', [['pessoa', 'zeca', 'sono', 'soma', 6]], texto='o Zeca com sono'); quieto(ato.dormir, E3, 'zeca', 2, chao=True); dorme = (E3['gente']['eu']['corpo']['sono'], E3['gente']['zeca']['corpo']['sono'])                 # o outro dorme; o personagem espera acordado
    E4 = mundo2(); ato.passa(E4, 'zeca', 2, 'esperar', esforco='leve', com=['eu'], para=False); junto = dict(E4['gente']['eu']['corpo'])                                   # o personagem já está no ato (vai junto): não dobra
    E5 = mundo2(); E5['gente']['eu']['corpo']['fome'] = 7; E5['relogio']['bloco'] = M.BLOCOS_DIA - 1; pv0 = E5['gente']['eu']['pv']; ato.passa(E5, 'zeca', 1, 'esperar', para=False); virada = pv0 - E5['gente']['eu']['pv']   # a virada cobra dele igual
    E6 = mundo2(); estado.aplica(E6, 'mestre', [['pessoa', 'eu', 'estado', 'poe', 'morto']], texto='morre, para a prova'); c6 = dict(E6['gente']['eu']['corpo']); quieto(ato.esperar, E6, 'zeca', 2); morto = c6 == E6['gente']['eu']['corpo']
    E7 = mundo2(); quieto(ato.esperar, E7, 'eu', 2); proprio = (dict(E7['gente']['eu']['corpo']), dict(E7['gente']['zeca']['corpo']))                                     # o ato do próprio personagem não mexe no corpo de quem não está em cena
    certo = (seis == (6, dict(fome=3, sono=6, cansaco=0), dict(fome=3, sono=6, cansaco=0)) and 'Aldric está com sono (esperava' in r1 and parou == (3, 6, 3) and 'PAROU: Aldric está com sono (esperava' in r2
             and dorme == (2, 6 + 2 * M.SONO_CHAO) and junto == dict(fome=1, sono=2, cansaco=2) and virada == max(1, int(estado.pv_max(E5['gente']['eu']) * M.FOME_PV)) and morto
             and proprio == (dict(fome=1, sono=2, cansaco=0), dict(fome=0, sono=0, cansaco=0)) and len(linha.splitlines()) == 2 and linha.splitlines()[1].startswith('Aldric, que esperava: PV '))
    ok('O TEMPO PASSA PARA O PERSONAGEM, AJA QUEM AGIR: quando o relógio anda por ato de outra pessoa (quem=ID), o corpo do personagem passa os mesmos blocos, como quem espera; se ele cruza um limiar, o ato do outro para, e a mesa diz por quê; não dobra quando ele já está no ato, e não vale para quem morreu',
       f"`ato.py esperar 6 quem=zeca`: o relógio anda {seis[0]} blocos e o corpo do personagem vai a fome {seis[1]['fome']}, sono {seis[1]['sono']} (o do Zeca: fome {seis[2]['fome']}, sono {seis[2]['sono']}); com o personagem a sono 3, o ato do Zeca para em {parou[0]} blocos («{r2.split('PAROU: ')[-1]}»); "
       f"o Zeca dorme 2 blocos e o personagem, acordado, vai a sono {dorme[0]}; indo junto no ato do outro, passa os blocos uma vez só (sono {junto['sono']}, cansaço {junto['cansaco']}); a virada do dia cobra a fome dele ({virada} de PV); morto, o corpo não muda: {sn(morto)}; "
       f"a última linha traz os dois: «{linha.splitlines()[-1][:60]}...»", certo)
    # 2 quem não é o personagem descansa em casa (J1, a regra)
    suja = lambda E, pid: estado.aplica(E, 'mestre', [['pessoa', pid, 'fome', 'soma', 4], ['pessoa', pid, 'sono', 'soma', 8], ['pessoa', pid, 'cansaco', 'soma', 10], ['pessoa', pid, 'pv', 'soma', -40], ['ferida', pid, 'abre', 'pernas', False]], texto='volta de uma saída dura')
    limpo = dict(fome=0, sono=0, cansaco=0); sujo = dict(fome=4, sono=8, cansaco=10)
    E = mundo2(); suja(E, 'zeca'); z = lambda: E['gente']['zeca']; pvm = estado.pv_max(z()); pv0 = z()['pv']; noite = M.CURA_DIA * max(1, int(pvm * M.CURA_BLOCO)); marcou = z()['marca'].get('cena') == estado.agora(E)
    tempo(E, 2); e2 = estado.em_cena(E, 'zeca'); dois = dict(z()['corpo']) == sujo and e2 is None                                    # menos de 3 blocos: nada muda
    tempo(E, 1); e3 = estado.em_cena(E, 'zeca'); tres = dict(z()['corpo']) == limpo and z()['pv'] == pv0 and z()['feridas'][0]['repouso'] == 0   # 3 blocos: o corpo a zero, sem noite de cura
    de_novo = estado.em_cena(E, 'zeca') is None; fato = turno.fatos([e3]) if e3 else ['?']; um_evento = bool(e3) and e3['tipo'] == 'casa' and e3['texto'] == 'Zeca descansou em casa'
    tempo(E, 3); estado.em_cena(E, 'zeca'); uma = (z()['pv'] - pv0, z()['feridas'][0]['repouso']); tempo(E, 5); estado.em_cena(E, 'zeca'); ainda = z()['pv'] - pv0; tempo(E, 1); estado.em_cena(E, 'zeca'); outra = (z()['pv'] - pv0, z()['feridas'][0]['repouso'])
    conta_certa = uma == (noite, 1) and ainda == noite and outra == (2 * noite, 2)       # olhar aos 3 blocos não perde a noite dos 6; aos 11 ainda é uma; aos 12, duas: nenhuma noite se perde nem se conta duas vezes
    E = mundo2(); suja(E, 'zeca'); tempo(E, 2 * M.CASA_NOITE + 1); estado.em_cena(E, 'zeca'); duas = (dict(z()['corpo']), z()['pv'] - pv0, z()['feridas'][0]['repouso'])         # 13 blocos: duas noites
    E = mundo2(); suja(E, 'zeca'); tempo(E, M.FERIDA_DIAS[0] * M.CASA_NOITE); estado.em_cena(E, 'zeca'); sete = (z()['pv'], len(z()['feridas']))                             # sete dias: o PV cheio e a ferida sarada
    E = mundo2(); suja(E, 'eu'); tempo(E, 30); eu_nada = estado.em_cena(E, 'eu') is None and corpo.casa(E, 'eu') == [] and dict(E['gente']['eu']['corpo']) == sujo      # o personagem nunca descansa de graça
    E = mundo2(); suja(E, 'zeca'); z()['marca'].pop('cena'); tempo(E, 60); estado.em_cena(E, 'zeca'); antigo = (dict(z()['corpo']), z()['pv'] - pv0, z()['feridas'][0]['repouso'])   # o save de antes da regra (sem a marca): descansado, sem noite de cura
    E = mundo2(); suja(E, 'zeca'); z()['marca']['caca'] = dict(de='eu', ermo='vila'); tempo(E, 30); no_ermo = estado.em_cena(E, 'zeca') is None and dict(z()['corpo']) == sujo      # quem está fora, numa saída aberta, não está em casa
    E = mundo2(); suja(E, 'zeca'); tempo(E, 12); p0 = prata_do_mundo(E); c0 = E['lugares']['vila']['estoque']['comida']; r = quieto(ato.esperar, E, 'zeca', 1); pelo_ato = z()['corpo']['fome'] == 0 and z()['corpo']['sono'] == 1 and prata_do_mundo(E) == p0 and E['lugares']['vila']['estoque']['comida'] == c0
    certo = (conta_certa and marcou and dois and tres and de_novo and um_evento and fato == ['- (nenhum fato registrado neste turno)'] and duas == (limpo, 2 * noite, 2) and sete == (pvm, 0) and eu_nada and antigo == (limpo, 0, 0) and no_ermo and pelo_ato
             and (M.CASA_ZERA, M.CASA_NOITE) == (3, 6))
    ok('O DESCANSO EM CASA: quem não é o personagem cuida de si quando não está em cena. Ao voltar a agir, o tempo fora de cena é acertado antes de mais nada, num evento só: menos de 3 blocos, nada muda; 3 ou mais, a fome, o sono e o cansaço voltam a zero; a cada 6, uma noite de cura e um dia de repouso. O personagem nunca descansa de graça',
       f"o Zeca com fome 4, sono 8, cansaço 10, 40 de PV a menos e uma ferida: depois de 2 blocos fora de cena, igual: {sn(dois)}; depois de 3, o corpo a zero e o PV e a ferida como estavam: {sn(tres)} (um evento «{e3['texto'] if e3 else '?'}», que não entra nos fatos do RETOMAR; chamar de novo não muda nada: {sn(de_novo)}); "
       f"aos 6 blocos, uma noite (+{uma[0]} de PV, {uma[1]} dia de repouso), aos 11 ainda uma, aos 12 a segunda: {sn(conta_certa)}; de uma vez, depois de 13 blocos, duas noites: +{duas[1]} de PV e {duas[2]} dias de repouso; depois de 7 dias, PV {sete[0]}/{pvm} e {sete[1]} ferida; o personagem, no mesmo estado, 30 blocos depois: nada: {sn(eu_nada)}; o save antigo (sem a marca), 60 blocos depois: o corpo a zero e nenhuma noite de cura: {sn(antigo == (limpo, 0, 0))}; "
       f"quem está no ermo, numa saída aberta, não descansa: {sn(no_ermo)}; o ato com quem= acerta antes de agir, e não gasta prata nem comida do lugar: {sn(pelo_ato)}", certo)
    # 3 o dia de luta ou de saída ao ermo não é dia de repouso (J11)
    d = tempfile.mkdtemp(prefix='m10_'); os.environ['MOTOR10_MUNDO'] = d; D0 = luta.D
    try:
        E = vila(prata=200); E['relogio']['bloco'] = 0
        estado.aplica(E, 'gera', [['lugar', 'nasce', 'mata', dict(nome='a Mata', em='na Mata', tipo='ermo', vizinhos=['vila'], coleta={'madeira:0': 50}, coleta_teto={'madeira:0': 50})], ['lugar', 'vila', 'vizinhos', 'poe', ['mata']]], texto='o ermo da prova')
        estado.aplica(E, 'mestre', [['ferida', 'eu', 'abre', 'braços', False]], texto='ferida de prova'); rep = lambda: E['gente']['eu']['feridas'][0]['repouso']
        dia_de_rotina(E, trabalha=False); d1 = rep()                                                                     # um dia parado: conta
        quieto(ato.dormir, E, 'eu', 2, para=False); quieto(ato.comer, E, 'eu'); quieto(caca.coletar, E, 'eu', 'madeira:0', blocos=1); pesados = E['gente']['eu']['marca'].get('pesados', 0)
        ato.passa(E, 'eu', 1, 'esperar', para=False); d2 = rep()                                                         # o dia da saída (a ida, um bloco de coleta, a volta: um bloco pesado só): não conta
        quieto(ato.dormir, E, 'eu', 2, para=False); quieto(ato.comer, E, 'eu'); luta.semente(21)
        json.dump(dict(inicio='colado', A=[dict(id='eu', controla=True)], B=[dict(nome='o bêbado', nivel=1, molde='comum')]), open(os.path.join(d, 'cen.json'), 'w')); quieto(ato.luta_nova, E, os.path.join(d, 'cen.json'), 'briga.json')
        for _ in range(60):
            if not estado.luta_aberta(E): break
            quieto(ato.luta_roda, E, 'briga.json', ['Aldric: atacar'])
        vivo = E['gente']['eu']['estado'] == 'vivo' and not estado.luta_aberta(E); ato.passa(E, 'eu', 4, 'esperar', para=False) if vivo else None; d3 = rep() if vivo else None      # o dia da luta: não conta
        dia_de_rotina(E, trabalha=False) if vivo else None; d4 = rep() if vivo else None                                                                                              # mais um dia parado: conta
    finally:
        luta.D = D0; os.environ.pop('MOTOR10_MUNDO', None); shutil.rmtree(d, ignore_errors=True)
    ok('O REPOUSO: o dia em que a pessoa lutou, ou passou um bloco ou mais numa saída ao ermo, não conta para a ferida sarar (como já não contava o dia de dois blocos pesados)',
       f"uma ferida, quatro dias: parado, {d1} dia de repouso; no dia da saída ao ermo (um bloco pesado só: {pesados}), segue em {d2}; no dia de uma luta (com um bêbado, sem mais nada), segue em {d3}; parado de novo, {d4}", (d1, d2, d3, d4) == (1, 1, 1, 2) and pesados == 1)
    # 4 a última linha não mente (J4)
    d = tempfile.mkdtemp(prefix='m10_'); amb = dict(os.environ, MOTOR10_MUNDO=d, PYTHONDONTWRITEBYTECODE='1'); aqui = os.path.dirname(os.path.abspath(__file__)); D0 = luta.D
    roda = lambda *a: (lambda r: (r.stdout + r.stderr).strip())(subprocess.run([sys.executable] + list(a), cwd=aqui, env=amb, capture_output=True, text=True))
    try:
        os.environ['MOTOR10_MUNDO'] = d; E = vila(); mais_um(E); normal = ato.ultima_linha(E, 'eu'); estado.grava(E)
        json.dump(dict(inicio='longe', A=[dict(id='eu', controla=True)], B=[dict(nome='o guarda', nivel=40, veste=dict(arma=['espada', 'Raro'], armadura=['malha', 'Raro'], escudo='Raro'))]), open(os.path.join(d, 'cen.json'), 'w'))
        roda('ato.py', 'luta', 'nova', os.path.join(d, 'cen.json'), 'briga.json'); fim = ''
        aberta = roda('ato.py', 'luta', 'roda', 'briga.json', 'Aldric: folego').splitlines()[-1]         # de fôlego cheio e com o inimigo a 8 casas, a ordem de fôlego acaba e a luta para na 1ª rodada, ainda aberta: seja qual for o dado
        for _ in range(60):
            x = roda('ato.py', 'luta', 'roda', 'briga.json', 'Aldric: atacar')
            if 'FIM:' in x or 'já acabou' in x: fim = x; break
        E = estado.carrega(); morreu = E['gente']['eu']['estado'] == 'morto'; ultima = fim.splitlines()[-1] if fim else ''
        if not morreu: estado.aplica(E, 'mestre', [['pessoa', 'eu', 'estado', 'poe', 'morto']], texto='morre, para a prova'); ultima = ato.ultima_linha(E, 'eu')
        de_outro = ato.ultima_linha(E, 'zeca')
    finally:
        luta.D = D0; os.environ.pop('MOTOR10_MUNDO', None); shutil.rmtree(d, ignore_errors=True)
    tem_pv = lambda x: bool(re.search(r'PV \d', x)) or 'de prata' in x or 'sem fome' in x
    certo = tem_pv(normal) and 'LUTA ABERTA' in aberta and not tem_pv(aberta) and 'Aldric morreu no Dia' in ultima and not tem_pv(ultima) and len(ultima.splitlines()) == 1 and 'que esperava' not in de_outro and tem_pv(de_outro)
    ok('A ÚLTIMA LINHA NÃO MENTE: com a luta aberta diz só a hora e que vale o quadro da luta (o PV do save é o de antes dela); de quem morreu, só a hora e a morte, também no `ato.py luta`',
       f"sem luta: «{normal.split(' · ', 2)[-1][:40]}...»; com a luta aberta (`ato.py luta roda`): «{aberta.split(' · ', 2)[-1]}»; depois de o personagem morrer" + (' na luta' if morreu else '') + f": «{ultima.split(' · ', 2)[-1]}»", certo)
    # 5 o registro da luta fecha a conta: o sangue e o veneno escritos, o FIM só com as feridas desta luta, a perna presa (J6, J7, J12)
    E = vila(); estado.aplica(E, 'mestre', [['ferida', 'eu', 'abre', 'pernas', False]], texto='a ferida velha'); luta.semente(5); D0b = luta.D
    S = luta.nova([estado.lutador(E, 'eu')], [estado.lutador(E, 'eu', nome='o outro', id=None, feridas=[])], inicio='colado', quieto=False); a, b = S['L']; S['comecou'] = True; S['r'] = 1
    a['pv'] = 50; a['sangra'] = [13, 3]; b['veneno'] = [7, 2]; pvb = b['pv']; luta._fecha_rodada(S); sangue = [x.strip() for x in S['log'] if 'sangra' in x or 'veneno' in x]
    b['estado'] = 'morto'; S['fim'] = 'A'; velha = luta.resultado_diz(S); luta._ferida(S, a, 'braços', False, luta.arma_de(S, b), 40); nova = luta.resultado_diz(S)
    luta._ferida(S, a, 'pernas', True, luta.arma_de(S, b), 80); perna = S['log'][-1].strip(); a['chao'] = True; S['fim'] = None; b['estado'] = 'pe'; S['log'] = []; luta.ordem(S, 'Aldric: atacar'); luta._turno(S, a); levanta = next((x.strip() for x in S['log'] if 'se levanta' in x), '')
    quadro = luta.situacao(S); luta.D = luta.Dados()
    certo = (sangue == [f"Aldric sangra 13 (37/{a['pvmax']})", f"o outro perde 7 para o veneno ({pvb - 7}/{b['pvmax']})"] and 'feridas' not in velha and 'feridas: Aldric (braços)' in nova and 'pernas' not in nova
             and 'não sai mais do lugar' in perna and 'não anda mais' not in perna and 'não sai do lugar' in levanta and 'perna presa' in quadro)
    ok('O REGISTRO DA LUTA FECHA A CONTA: o que o sangue e o veneno tiram sai escrito no fim de cada rodada; o FIM lista só as feridas abertas nesta luta; e quem tem a perna presa "não sai mais do lugar" (levantar-se, pode)',
       f"«{' · '.join(sangue)}»; com uma ferida velha nas pernas e nenhuma nova, o FIM diz «{velha.split(' · ')[-1]}»; com uma nova nos braços, «{nova.split(' · ')[-1]}»; a ferida grave nas pernas: «{perna.split(': ', 1)[-1][:70]}», e depois «{levanta}»", certo)
    # 6 o RETOMAR junta só fatos iguais SEGUIDOS, e diz as horas (J8)
    ev = lambda i, dia, bloco, texto, tipo='consertar': dict(id=i, dia=dia, bloco=bloco, tipo=tipo, onde='vila', quem=['eu'], efeitos=[['relogio', 1]], texto=texto)
    F = turno.fatos([ev(1, 2, 2, 'Maro espera o conserto'), ev(2, 2, 3, 'Maro espera o conserto'), ev(3, 2, 3, 'Maro come', 'comer'), ev(4, 2, 4, 'Maro espera o conserto'), ev(5, 2, 5, 'Maro espera o conserto'),
                     ev(6, 3, 4, 'Cira luta com a corça', 'cacar'), ev(7, 3, 4, 'Cira fica com o campo', 'despojo'), ev(8, 3, 5, 'Cira luta com a corça', 'cacar'), ev(9, 3, 5, 'Cira luta com a corça', 'cacar')])
    quer = ['- Dia 2, manhã a noite: Maro espera o conserto (× 4)', '- Dia 2, a rotina: Maro come', '- Dia 3, entardecer: Cira luta com a corça', '- Dia 3, entardecer: Cira fica com o campo', '- Dia 3, noite: Cira luta com a corça (× 2)']
    ok('O RETOMAR JUNTA SÓ O QUE VEM SEGUIDO: o mesmo fato repetido em seguida vira uma linha, com a conta e as horas do primeiro ao último; o que aconteceu depois de outro fato fica na linha e na hora dele',
       ' · '.join(x[2:] for x in F), F == quer)
    # 7 as perguntas, como o jogador escreve (J9)
    E = vila(); [turno.pergunta(E, f'Pergunta {k}?', ['a=sim', 'b=não', 'c=talvez']) for k in (1, 2, 3, 4)]
    r1 = turno.responde(E, '1c.2 a'); r2 = turno.responde(E, '3 a, 4 c'); quatro = [(x['n'], x['cod']) for x in E['turno']['respondidas']]
    E = vila(); [turno.pergunta(E, f'Pergunta {k}?', ['a=sim', 'b=não']) for k in (1, 2)]; r3 = turno.responde(E, '1b 2a'); n3 = turno.pergunta(E, 'Nova?', ['a=sim', 'b=não']); n4 = turno.pergunta(E, 'Outra?', ['a=sim', 'b=não'])
    def com_duas():
        X = vila(); turno.pergunta(X, 'A?', ['a=sim', 'b=não']); turno.pergunta(X, 'B?', ['a=sim', 'b=não']); return X
    ruins = {c: (recusa(lambda c=c: turno.responde(com_duas(), c)) or '') for c in ('1x', '2', 'abc', '1a.9b', '1a zz', '1a.1b')}
    certo = (quatro == [(1, 'c'), (2, 'a'), (3, 'a'), (4, 'c')] and len(E['turno']['respondidas']) == 2 and n3.startswith('pergunta 1 aberta') and 'guarda como 3' in n3 and n4.startswith('pergunta 2 aberta') and 'guarda como 4' in n4
             and all(ruins.values()) and 'falta a letra' in ruins['2'] and 'não entendi' in ruins['abc'])
    ok('AS PERGUNTAS, COMO O JOGADOR ESCREVE: o `responde` aceita espaço entre o número e a letra, e ponto, vírgula ou espaço entre os códigos; o `pergunta` diz o número que a pergunta terá na lista do RETOMAR (o do código)',
       f"«1c.2 a» e «3 a, 4 c» marcam as quatro: {sn(quatro == [(1, 'c'), (2, 'a'), (3, 'a'), (4, 'c')])}; «1b 2a» marca as duas; com a 1 e a 2 respondidas, a pergunta nova: «{n3.split(':')[0]}» (o caderno a guarda como 3 até fechar) e «{n4.split(':')[0]}»; "
       f"os códigos tortos seguem recusados ({len([x for x in ruins.values() if x])} de {len(ruins)}: «{ruins['2'][:44]}...»)", certo)
    # 8 a MESA de quem morreu diz o que ficou com o corpo e para onde foi a prata (J13)
    E = vila(prata=13); estado.aplica(E, 'mestre', [['pessoa', 'eu', 'carga.comida', 'soma', 2], ['pessoa', 'eu', 'carga.couro:0', 'soma', 1]], texto='a carga'); p0 = prata_do_mundo(E); cx = E['lugares']['vila']['estoque']['prata']
    E['lugares']['vila']['pop'] = 400; estado.aplica(E, 'mestre', [['pessoa', 'eu', 'estado', 'poe', 'morto']], texto='morre na vila'); na_vila = '\n'.join(turno._voce(E)); regra = E['lugares']['vila']['estoque']['prata'] == cx + 13 and prata_do_mundo(E) == p0
    E2 = vila(prata=13); estado.aplica(E2, 'gera', [['lugar', 'nasce', 'mata', dict(nome='a Mata', em='na Mata', tipo='ermo', vizinhos=['vila'], bichos={'corça': 5}, teto={'corça': 5})], ['lugar', 'vila', 'vizinhos', 'poe', ['mata']]], texto='o ermo')
    E2['gente']['eu']['marca']['caca'] = dict(ermo='mata', casa='vila', quer='caça', alvo=None, restam=1, com=[], dia=1, fase='procura', encontro=None, luta=None, lutas=0, parou=None, sangue=None)
    estado.aplica(E2, 'mestre', [['pessoa', 'eu', 'estado', 'poe', 'morto'], ['pessoa', 'eu', 'marca.caca', 'poe', None]], texto='morre na mata'); no_ermo = '\n'.join(turno._voce(E2)); mesa2 = turno.mesa(E2)
    E3 = vila(prata=13); estado.aplica(E3, 'mestre', [['pessoa', 'eu', 'estado', 'poe', 'morto']], texto='morre'); E3['gente']['eu']['morte'] = dict(dia=1, bloco=2, onde='vila'); antigo = '\n'.join(turno._voce(E3))      # o save de antes: a morte não guardou quanto ele deixou
    certo = ('ficaram soltas: Espada do Aldric (i0001), Gibão do Aldric (i0002)' in na_vila and 'A carga (2 de comida, 1 de couro Comum) e a prata (13) ficaram com o povo do lugar: entraram no estoque e no caixa da Vila de Prova' in na_vila and regra
             and 'no estoque do lugar)' not in na_vila and 'A prata (13) ficou no chão, junto do corpo' in no_ermo and 'a contagem na Mata' in mesa2 and 'no chão na Mata (soltas' in mesa2 and 'A carga e a prata ficaram' in antigo)
    ok('A MESA DE QUEM MORREU diz o que ficou com o corpo e para onde foram a carga e a prata, com as palavras certas (a regra não muda: na vila ficam com o lugar; no ermo, no chão)',
       f"na vila: «{na_vila.split('Com o corpo')[-1].split(' O que era')[0][:200]}»; a prata do morto entrou no caixa do lugar e a do mundo fecha: {sn(regra)}; no ermo: «{no_ermo.split('). ')[-1].split(' O que era')[0][:80]}», e o SÓ O MESTRE traz a contagem e o que está no chão: {sn('a contagem na Mata' in mesa2)}", certo)
    # 9 as frases acertadas (J5, J10, J12, J14)
    E = vila(); estado.aplica(E, 'mestre', [['pessoa', 'eu', 'carga.comida', 'soma', 6], ['pessoa', 'eu', 'fome', 'soma', 8], ['pessoa', 'eu', 'sono', 'soma', 8]], texto='para a prova')
    restam = quieto(ato.comer, E, 'eu', da_carga=True); estado.aplica(E, 'mestre', [['pessoa', 'eu', 'carga.comida', 'soma', -3]], texto='gasta'); resta = quieto(ato.comer, E, 'eu', da_carga=True)
    ficha = pessoas.linha(pessoas.ficha(estado.lutador(E, 'eu')))                                                    # com sono 8 (pena −4), o acerto do Leigo fica negativo
    estado.aplica(E, 'gera', [['item', 'nasce', item('armadura', 0, 'elmo de malha Comum', material='malha', cobre=['cabeça'], dono='eu')], ['lugar', 'vila', 'oficina', 'poe', 1], ['item', 'i0001', 'dur', 'soma', -7]], texto='o elmo e a forja')
    elmo = quieto(ato.vestir, E, 'eu', 'i0003').splitlines()[0]; pecas = ' · '.join(ato.diz_pecas(E, 'eu')); oficina = '\n'.join(oficio.ver(E, 'eu')); serpe = bichos.ameaca('serpe'); aranha = bichos.ameaca('aranha')
    certo = ('restam 5 de comida' in restam and 'resta 1 de comida' in resta and 'acerto −' in ficha and '+−' not in ficha and '(na cabeça)' in elmo and 'EM USO, na cabeça' in pecas and 'EM USO, no corpo' in pecas
             and estado.nome_bem('couro:0') == 'couro Comum' and estado.nome_bem('madeira:2') == 'madeira Rara' and estado.nome_bem('comida') == 'comida' and 'escama Épica' in serpe and 'escama Épico' not in serpe and 'carapaça Rara' in aranha
             and 'bloco de espera por peça' in oficina and 'arredonda para cima' in oficina and 'de prata e 1 bloco de espera' in oficina)
    ok('AS FRASES ACERTADAS: o plural ("restam 5"), o sinal do número ("acerto −0,25", sem "+−"), o elmo "na cabeça", o nome do bem que a MESA usa ("couro Comum"), a categoria que concorda ("escama Épica"), e a oficina da MESA dizendo que o conserto pago gasta um bloco por peça e arredonda a prata para cima',
       f"«{restam.split('; ')[-1].rstrip(')')}» e «{resta.split('; ')[-1].rstrip(')')}»; «{ficha.splitlines()[1].split(' · ')[0].strip()}»; «{elmo}»; couro:0 é «{estado.nome_bem('couro:0')}»; a serpe: «{(re.search(r'escama [^ ,]+', serpe) or [None])[0]}»; "
       f"a oficina: «{next((x for x in oficina.splitlines() if 'consertar Espada' in x), '?')[2:]}»", certo)
    return out


def main():
    if sys.argv[1:2] == ['vila'] and len(sys.argv) == 3:
        os.environ['MOTOR10_MUNDO'] = os.path.abspath(sys.argv[2])
        if os.path.exists(os.path.join(estado.pasta(), 'relogio.json')): sys.exit(f'já há um mundo em {estado.pasta()}: não escrevo por cima.')
        estado.grava(vila()); print(f'vila de prova criada em {estado.pasta()}. Experimente: MOTOR10_MUNDO={estado.pasta()} python3 turno.py abre'); return True
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    print('BANCO DE PROVAS DO MUNDO\n\netapa 1: um dia numa vila\n')
    res = provas(n)
    for nome, deu, passa in res: print(f"  {'passa' if passa else 'FALHA'}  {nome}: {deu}")
    print('\netapa 2: o alicerce (a morte, nascer, vestir, a jornada, os invariantes novos; a cama, a luta aberta, o RETOMAR, as entradas tortas)\n'); mais = provas_alicerce2(n); res += mais
    for nm, deu, passa in mais: print(f"  {'passa' if passa else 'FALHA'}  {nm}: {deu}")
    print('\netapa 2: o acerto da terceira volta (o relógio único e o corpo de quem não é o personagem; o repouso; a última linha; o registro da luta; o RETOMAR; as perguntas; a MESA de quem morreu)\n'); mais = provas_volta3(n); res += mais
    for nm, deu, passa in mais: print(f"  {'passa' if passa else 'FALHA'}  {nm}: {deu}")
    import importlib
    for nome, titulo in (('provas_mercado', 'etapa 2: o mercado'), ('provas_oficio', 'etapa 2: o ofício'), ('provas_caca', 'etapa 2: a caça e a coleta'),
                         ('provas_talento', 'etapa da magia: o alicerce (os dons e os talentos; os verbos, os tipos e os ganchos)'),
                         ('provas_magia', 'etapa da magia: o mundo da magia'), ('provas_criaturas', 'etapa da magia: as criaturas e a vila'),
                         ('provas_4b', 'etapa 4b: o alicerce (o vocabulário comum: os campos, os verbos, os invariantes; o despojo pela categoria; o 17º caminho; a luta de quem tem o traço)'),
                         ('provas_masmorra', 'etapa 4b: a masmorra'), ('provas_manha', 'etapa 4b: o ladino'), ('provas_povos', 'etapa 4b: os povos'), ('provas_dragoes', 'etapa 4b: os dragões')):     # os que ainda não existem ficam de fora
        try: mod = importlib.import_module(nome)
        except ModuleNotFoundError as e:
            if e.name != nome: raise
            continue
        print(f'\n{titulo}\n'); mais = mod.provas(n); res += mais
        for nm, deu, passa in mais: print(f"  {'passa' if passa else 'FALHA'}  {nm}: {deu}")
    print(f'\n{sum(p for _, _, p in res)} de {len(res)} provas passam.')
    return all(p for _, _, p in res)


if __name__ == '__main__':
    sys.exit(0 if main() else 1)
