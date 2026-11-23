#!/usr/bin/env python3
"""provas_mundo.py — MOTOR 10: O BANCO DE PROVAS DO MUNDO. Cada etapa do PROJETO.md entra aqui com as suas metas.

ETAPA 1, "um dia numa vila": o gravador único, o relógio, o corpo, os atos, a ferida que dura, a luta que volta ao estado, abrir e fechar o turno.
ETAPA 2, o alicerce (o que a integração pôs nele): a morte numa regra só, nascer por evento, vestir e guardar, a jornada, comer da carga, os invariantes novos,
o evento que não muda nada; e depois os bancos dos módulos (o mercado, o ofício, a caça e a coleta).
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
    ok('A ROTINA: 30 dias dormindo, comendo uma vez e trabalhando dois blocos', f"pior pena {pior}; prata 30 → {p['moedas']}; corpo {p['corpo']}", pior == 0 and 50 <= p['moedas'] <= 70 and not estado.valida(E))
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
    nada = m['moedas'] == 0 and not m['carga'] and E['lugares']['vila']['estoque']['prata'] == cx + 40 and E['lugares']['vila']['estoque']['comida'] == 2005 and m['morte'] == dict(dia=1, bloco=2, onde='vila')
    antes = retrato(E); atos = [('comer', lambda: ato.comer(E, 'eu')), ('dormir na cama', lambda: ato.dormir(E, 'eu', 2)), ('trabalhar', lambda: ato.trabalhar(E, 'eu', 1)), ('treinar', lambda: ato.treinar(E, 'eu', 1, 'espada')),
                                ('esperar', lambda: ato.esperar(E, 'eu', 1)), ('vestir', lambda: ato.vestir(E, 'eu', 'i0001')), ('testar', lambda: teste.rola(E, 'levantar-se', 'Vontade', 20)),
                                ('receber uma peça', lambda: estado.aplica(E, 'mestre', [['item', 'i0001', 'dono', 'poe', 'eu']]))]
    rec = [x for x, f in atos if recusa(f)]; mesa = turno.mesa(E)
    ok('A MORTE, UMA REGRA SÓ: o morto não fica com nada (as peças e o núcleo caem soltos onde ele morreu, a obra se desfaz, a carga e a prata ficam no lugar); morto não age, e nada é cobrado dele; a MESA abre com a morte',
       f"as {n_itens} peças (duas vestidas, uma guardada, o núcleo que estava na obra) soltas na vila, e a obra desfeita: {'sim' if caiu else 'NÃO'}; a carga e os 40 de prata no estoque do lugar: {'sim' if nada else 'NÃO'}; a prata do mundo fecha: {'sim' if prata_do_mundo(E) == p0 else 'NÃO'}; "
       f"estado {'inteiro' if not estado.valida(E) else 'QUEBRADO'}; {len(rec)} de {len(atos)} atos do morto recusados, sem mudar nada: {'sim' if antes == retrato(E) else 'NÃO'}; a MESA diz que ele morreu e não lista atos: {'sim' if 'ESTÁ MORTO' in mesa and 'ato.py comer' not in mesa else 'NÃO'}",
       caiu and nada and prata_do_mundo(E) == p0 and not estado.valida(E) and len(rec) == len(atos) and antes == retrato(E) and 'ESTÁ MORTO' in mesa and 'ato.py comer' not in mesa)
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
    print('\netapa 2: o alicerce (a morte, nascer, vestir, a jornada, os invariantes novos)\n'); mais = provas_alicerce2(n); res += mais
    for nm, deu, passa in mais: print(f"  {'passa' if passa else 'FALHA'}  {nm}: {deu}")
    import importlib
    for nome, titulo in (('provas_mercado', 'etapa 2: o mercado'), ('provas_oficio', 'etapa 2: o ofício'), ('provas_caca', 'etapa 2: a caça e a coleta')):
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
