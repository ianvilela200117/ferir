#!/usr/bin/env python3
"""provas_mundo.py — MOTOR 10: O BANCO DE PROVAS DO MUNDO. Cada etapa do PROJETO.md entra aqui com as suas metas.

ETAPA 1, "um dia numa vila": o gravador único, o relógio, o corpo, os atos, a ferida que dura, a luta que volta ao estado, abrir e fechar o turno.
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


def vila(semente=1, prata=30):
    """uma vila de prova: um lugar, o personagem com uma espada e um couro Comuns, 30 de prata"""
    E = estado.novo(semente)
    E['lugares']['vila'] = dict(nome='a Vila de Prova', em='na Vila de Prova', tipo='vila', cama=True, estoque=dict(comida=2000, prata=5000))
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


def main():
    if sys.argv[1:2] == ['vila'] and len(sys.argv) == 3:
        os.environ['MOTOR10_MUNDO'] = os.path.abspath(sys.argv[2])
        if os.path.exists(os.path.join(estado.pasta(), 'relogio.json')): sys.exit(f'já há um mundo em {estado.pasta()}: não escrevo por cima.')
        estado.grava(vila()); print(f'vila de prova criada em {estado.pasta()}. Experimente: MOTOR10_MUNDO={estado.pasta()} python3 turno.py abre'); return True
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    print('BANCO DE PROVAS DO MUNDO · etapa 1: um dia numa vila\n')
    res = provas(n)
    for nome, deu, passa in res: print(f"  {'passa' if passa else 'FALHA'}  {nome}: {deu}")
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
