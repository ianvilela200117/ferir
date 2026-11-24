#!/usr/bin/env python3
"""provas_dragoes.py — MOTOR 10, ETAPA 4b: O BANCO DE PROVAS DOS DRAGÕES (capítulo 20; frente D; o contrato: projeto/ETAPA_4B.md; as metas: projeto_b, seção 9).

  AS ESPÉCIES (as 15 chaves, na forma dos bichos) · DR1 o filhote foge ferido · DR2 do jovem ao ancião em casa · DR3 o ancião contra seis · DR4 a categoria decide
  · DR5 o dragão não se caça sozinho · DR6 a pergunta do pedido (o jovem da serra no covil contra 4 de nível 50) · DR7 a fase (para e pergunta; no covil nunca foge;
  fora dele o da serra foge) · DR8 dormindo · DR9 o registro e a luta (o PV de agora, o morto, o coração, o fugido) · O ROUBO DE QUEM DORME (a vigília, o punhado,
  acordar) · MI1 a prata do mundo · MI2 a venda em Pedra Rasa · MI3 o dragão morto não volta · MI4 o ladrão robô · MI5 um ano do jovem ao lado da aldeia · MI6 os covis
  juntos · O TIÇÃO NA VILA DE TESTE (E4 a: numa cópia do save do jogador, nada escrito nele).
As lutas são as do luta.py de verdade (dado de ensaio, com semente). O mundo é de rascunho (a vila de teste em memória, a vila de prova); o save do jogador (ensaio/) só
é LIDO, numa cópia temporária. O ladrão robô usa o dado do ladino de verdade (manha.testa): varia um pouco de rodada para rodada, e a faixa tem folga.
Uso: python3 provas_dragoes.py [N]      (N escala as lutas: 300 de padrão, como o provas_mundo.py, que também roda este banco)
"""
import contextlib, copy, io, json, math, os, shutil, sys, tempfile
import tabelas as T
import tabelas_mundo as M
import tabelas_bichos as TB
import tabelas_criaturas as TC
import tabelas_dragoes as TD
import estado, bichos, luta, dragoes, turno, ato
import provas_mundo as PM
from itens import item

AQUI = os.path.dirname(os.path.abspath(__file__))
REF = TC.REF                    # o homem do degrau: o nível de referência de cada categoria (a régua das criaturas)
IDADES_CHEFE = ('jovem', 'adulto', 'velho', 'ancião')
GIRA = dict(jovem='serra', adulto='brejo', velho='grutas', ancião='serra')     # nas metas de 200 lutas por linha, um tipo por idade (os três passam pelas idades)


def quieto(f, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()): return f(*a, **k)


def sn(x): return 'sim' if x else 'NÃO'
def pc(x): return f'{x:g}%'
def V(c): return 80 if c >= 3 else None            # do Épico para cima, o homem do degrau tem Vontade 80 (sem ela a armadura grande dorme)


# ---------------------------------------------------------------- AS ESPÉCIES ----------------------------------------------------------------
def _especies(n):
    E = TD.ESPECIES; pvs = {i: dragoes.pv_max('serra', i) for i in TD.IDADES}; ruim = []
    if len(E) != 15 or set(E) != {TD.chave(t, i) for t in TD.TIPOS for i in TD.IDADES}: ruim.append('as 15 chaves')
    for k, e in E.items():
        i = e['dragao']['idade']; t = e['dragao']['tipo']
        if set(e) - {'fases', 'dragao'} != set(TB.ESPECIES['corça']): ruim.append(f'{k}: a forma')
        if bichos.especie(k) is not e or estado.especie(k) is not e: ruim.append(f'{k}: as portas (bichos.especie, estado.especie)')
        if e['chefe'] != (i != 'filhote') or e['moral'] != ('testa' if i == 'filhote' else 'firme'): ruim.append(f'{k}: o chefe e a moral')
        if e['nucleo'] != (e['cat'] >= TD.NUCLEO_DESDE): ruim.append(f'{k}: o núcleo')
        if bool(e['fases']) != e['chefe'] or (e['fases'] and bool(e['fases'][0].get('foge')) != (t == 'serra')): ruim.append(f'{k}: a fase')
        if any(x not in TB.TRACOS and x not in T.TRACOS_NOVOS for x in e['tracos'] + [y for f in e['fases'] for y in f.get('ganha', [])]): ruim.append(f'{k}: um traço que a luta não roda')
        if ('peçonha' in ''.join(e['despojo'])) != (t == 'brejo'): ruim.append(f'{k}: a peçonha')
    p = dragoes.dragao('serra', 'jovem'); f = dragoes.dragao('grutas', 'filhote')
    if not (p.get('lider') and p['moral'] == 'firme' and f['moral'] == 'testa'): ruim.append('o lutador (o chefe firme, o filhote que testa)')
    if 'dragão' not in TB.ESPECIES or any(k in TB.ESPECIES for k in E) or not 12 <= len(TB.ESPECIES) <= 16: ruim.append('a página dos bichos ficou como era')
    gancho = [g for g in ('bloco', 'casa', 'vestiu', 'voce', 'retomar', 'recusa_fecha', 'pode_vestir') if callable(getattr(dragoes, g, None))]
    if gancho: ruim.append(f"o dragoes.py tem função com nome de gancho dos módulos: {', '.join(gancho)}")
    if [dragoes.idade_da_cat(c) for c in range(1, 6)] != list(TD.IDADES) or dragoes.tipo_do_lugar('brejo') != 'brejo' or dragoes.tipo_do_lugar(None) != 'grutas': ruim.append('as contas de quem gera o covil')
    return [('D0 AS ESPÉCIES: os 3 tipos nas 5 idades, na forma dos bichos (as portas de hoje as leem); o filhote é bicho que testa a coragem, do jovem para cima chefe de moral firme '
             '(só a fase o tira da luta); o núcleo só do adulto (Épico) para cima; a fuga só no da serra; a peçonha só no verme; todo traço é dos que a luta roda; o dragão do capítulo 6 segue na página dos bichos; o módulo só tem os ganchos que usa (a virada, a mesa, o SÓ O MESTRE)',
             f"PV {' · '.join(f'{i} {v}' for i, v in pvs.items())}; " + ('tudo certo' if not ruim else 'ERRADO: ' + '; '.join(ruim[:4])), not ruim and list(pvs.values()) == [147, 480, 817, 1100, 1337])]


# ---------------------------------------------------------------- A LUTA (DR1 a DR8) ----------------------------------------------------------------
def _dr1(n):
    L = max(300, 2 * n); R = {t: dragoes.mede(t, 'filhote', REF[1], 1, homens=1, lutas=L, covil=False) for t in TD.TIPOS}
    return [('DR1 O FILHOTE (bicho: ferido, testa a coragem e foge) contra um homem do degrau (nível 30, conjunto Incomum), cada tipo em casa: o homem vence de 40 a 65%, e o filhote foge em parte das lutas',
             ' · '.join(f"{t}: vence {pc(r['vence'])}, o filhote foge em {pc(r['fugiu'])}, o homem morre em {pc(r['alguem'])}" for t, r in R.items()) + f' ({L} lutas por linha)',
             all(40 <= r['vence'] <= 65 and r['fugiu'] > 0 for r in R.values()))]


FAIXA2 = dict(jovem=(50, 75), adulto=(45, 70), velho=(25, 50), ancião=(5, 25))


def _dr2(n):
    L = max(200, (4 * n) // 3); R = {}; out = []
    for i in IDADES_CHEFE:
        c = TD.IDADES[i]['cat']; R[i] = {t: dragoes.mede(t, i, REF[c], c, homens=4, lutas=L, vontade=V(c)) for t in TD.TIPOS}
    for i, (lo, hi) in FAIXA2.items():
        out.append((f"DR2 O {i.upper()} em casa (no covil, com a fase) contra 4 do degrau (nível {REF[TD.IDADES[i]['cat']]}, {T.CATS[TD.IDADES[i]['cat']]}): o grupo vence de {lo} a {hi}%",
                    ' · '.join(f"{t}: {pc(r['vence'])} ({r['mortos']} mortos por luta)" for t, r in R[i].items()) + f' ({L} lutas por linha)', all(lo <= r['vence'] <= hi for r in R[i].values())))
    return out


def _dr3(n):
    L = max(200, (4 * n) // 3); c = TD.IDADES['ancião']['cat']; R = {t: dragoes.mede(t, 'ancião', REF[c], c, homens=6, lutas=L, vontade=80) for t in TD.TIPOS}
    return [('DR3 O ANCIÃO (a calamidade) contra 6 do degrau (nível 150, tudo Lendário): o grupo vence de 65 a 90%',
             ' · '.join(f"{t}: {pc(r['vence'])} ({r['mortos']} mortos por luta)" for t, r in R.items()) + f' ({L} lutas por linha)', all(65 <= r['vence'] <= 90 for r in R.values()))]


def _dr4(n):
    L = max(100, (2 * n) // 3); acima = {}; abaixo = {}
    for i in IDADES_CHEFE:
        c = TD.IDADES[i]['cat']; t = GIRA[i]
        acima[i] = dragoes.mede(t, i, REF[c], c + 1, homens=4, lutas=L, vontade=80)
        abaixo[i] = dragoes.mede(t, i, REF[c], c - 1, homens=4, lutas=L, vontade=V(c))
    return [('DR4 A CATEGORIA DECIDE: 4 do degrau com o conjunto uma acima vencem 90% ou mais; com o conjunto uma abaixo, 10% ou menos (do jovem ao ancião, em casa)',
             'uma acima: ' + ', '.join(f"{i} ({GIRA[i]}) {pc(acima[i]['vence'])}" for i in IDADES_CHEFE) + ' · uma abaixo: ' + ', '.join(f"{i} {pc(abaixo[i]['vence'])}" for i in IDADES_CHEFE) + f' ({L} lutas por linha)',
             all(acima[i]['vence'] >= 90 and abaixo[i]['vence'] <= 10 for i in IDADES_CHEFE))]


def _dr5(n):
    L = max(100, (2 * n) // 3); R = {}
    for i in IDADES_CHEFE:
        c = TD.IDADES[i]['cat']; R[i] = dragoes.mede(GIRA[i], i, REF[c], c, homens=1, lutas=L, vontade=V(c))
    return [('DR5 O DRAGÃO NÃO SE CAÇA SOZINHO: um homem do degrau contra o jovem ou maior vence até 5%',
             ', '.join(f"{i} ({GIRA[i]}) {pc(r['vence'])} (morre em {pc(r['alguem'])})" for i, r in R.items()) + f' ({L} lutas por linha)', all(r['vence'] <= 5 for r in R.values()))]


def _dr6_8(n):
    L = max(200, 2 * n)
    base = dragoes.mede('serra', 'jovem', 50, 2, lutas=L)
    epica = dragoes.mede('serra', 'jovem', 50, 2, arma=3, lutas=L)
    incomum = dragoes.mede('serra', 'jovem', 50, 1, lutas=L)
    covil = dragoes.mede('serra', 'jovem', 50, 2, lutas=L, interativo=True, semente=23)
    fora = dragoes.mede('serra', 'jovem', 50, 2, lutas=L, covil=False, interativo=True, semente=23)
    outros = {t: dragoes.mede(t, 'jovem', 50, 2, lutas=max(100, L // 3), covil=False, interativo=True, semente=29) for t in ('brejo', 'grutas')}
    dorme = dragoes.mede('serra', 'jovem', 50, 2, lutas=L, dorme=True)
    out = [('DR6 A PERGUNTA DO PEDIDO: o jovem da serra no covil contra 4 de nível 50 de espada, malha e escudo Raros vence de 55 a 80%; com a arma Épica, 90% ou mais; tudo Incomum, até 5%',
            f"Raros: {pc(base['vence'])} ({base['mortos']} mortos por luta; morre alguém em {pc(base['alguem'])}) · a arma Épica: {pc(epica['vence'])} ({epica['mortos']} mortos por luta) · tudo Incomum: {pc(incomum['vence'])} ({L} lutas por linha)",
            55 <= base['vence'] <= 80 and epica['vence'] >= 90 and incomum['vence'] <= 5)]
    para = covil['para'] == covil['fase'] and fora['para'] == fora['fase'] and all(r['para'] == r['fase'] for r in outros.values()) and covil['fase'] > 0
    out.append(('DR7 A FASE: toda fase que chega para a luta e pergunta; no covil (sem saída para ele) o dragão nunca foge e a fúria vale; fora do covil, o da serra foge ferido pelo ar de 60 a 95% das lutas; o que não voa nunca foge',
                f"no covil: a fase em {pc(covil['fase'])}, a luta parou em {pc(covil['para'])}, fugiu em {pc(covil['fugiu'])} · fora: a fase em {pc(fora['fase'])}, parou em {pc(fora['para'])}, fugiu em {pc(fora['fugiu'])} (o grupo vence {pc(fora['vence'])}) · "
                + ', '.join(f"{t} fora do covil: fugiu em {pc(r['fugiu'])}" for t, r in outros.items()),
                para and covil['fugiu'] == 0 and 60 <= fora['fugiu'] <= 95 and all(r['fugiu'] == 0 for r in outros.values())))
    out.append(('DR8 DORMINDO: o grupo que pega o dragão dormindo (ele perde o primeiro turno) vence 5 pontos ou mais acima do que o enfrenta acordado (o jovem da serra no covil, 4 de nível 50 Raros)',
                f"dormindo {pc(dorme['vence'])} contra acordado {pc(base['vence'])}: {dorme['vence'] - base['vence']:+.1f} pontos", dorme['vence'] - base['vence'] >= 5))
    return out


# ---------------------------------------------------------------- O REGISTRO E A LUTA (DR9), O ROUBO ----------------------------------------------------------------
def _mundo_covil(tipo='serra', idade='jovem', tesouro=300, dorme=0, pecas=True, semente=1):
    """a vila de prova (com povo) e um ermo vizinho com um dragão sobre o tesouro (300 de prata e duas peças guardadas); quatro caçadores na vila"""
    E = PM.vila(semente)
    at = dict(Força=80, Agilidade=60, Vigor=80, Vontade=60, Percepção=50, Afinidade=40)
    ef = [['lugar', 'nasce', 'covil', dict(nome='a Serra de Prova', em='na Serra de Prova', tipo='ermo', habitat='serra', perigo=3, longe=2, estoque={}, vizinhos=['vila'], bichos={}, teto={})],
          ['lugar', 'vila', 'vizinhos', 'poe', ['covil']], ['lugar', 'vila', 'pop', 'poe', 120]]
    ef += [['pessoa', 'nasce', f'cac{j}', dict(nome=f'Caçador {j}', nivel=50, atributos=at, lugar='vila')] for j in range(1, 5)]
    estado.aplica(E, 'gera', ef, texto='a serra de prova e os caçadores')
    E2 = dict(E, lugares=dict(E['lugares']))
    ef = dragoes.poe(E2, 'covil', tipo, idade, 'o Brasido', vila='vila', tesouro=tesouro, dorme=dorme)
    if pecas: ef += [['item', 'nasce', dict(item('arma', 2, 'a Espada do Morto', familia='espada'), onde='covil')], ['item', 'nasce', dict(item('escudo', 1, 'o escudo do morto'), onde='covil')]]
    estado.aplica(E, 'gera', ef, onde='covil', texto='o covil do Brasido')
    return E


def _luta_com(E, lid, cat, nivel=50, k=4, covil=True, semente=3, ate=None, tentativas=40):
    """a luta dos caçadores (homens do degrau com os ids deles) contra o dragão do lugar, montado como a masmorra o monta (dragoes.monta); `ate`: tenta outras sementes
    até a luta acabar como se quer (morto, fugiu)"""
    p, dorme = dragoes.monta(E, lid); p = dict(p); esp = p.pop('bicho')
    for s in range(semente, semente + tentativas):
        luta.semente(s)
        A = [dict(dragoes.homem(f'Caçador {j}', nivel, cat), id=f'cac{j}') for j in range(1, k + 1)]
        S = luta.nova(A, [bichos.bicho(esp, **p)], quieto=True, inicio='perto', surpresa='B' if dorme else None, **({'lugar': dict(sem_saida='B')} if covil else {}))
        luta.corre(S); d = S['L'][-1]
        if ate is None or d['estado'] == ate: return S
    return S


def _dr9(n):
    out = []; R = {}
    # 1 o PV de agora entra na luta
    E = _mundo_covil(); estado.aplica(E, 'mestre', [['lugar', 'covil', 'dragao.pv', 'poe', 200]], texto='o dragão ferido')
    p, dorme = dragoes.monta(E, 'covil'); S = luta.nova([dragoes.homem('h', 50, 2)], [bichos.bicho(p.pop('bicho'), **p)], quieto=True)
    R['entra com o PV de agora (200 de 480)'] = S['L'][-1]['pv'] == 200 and S['L'][-1]['pvmax'] == 480 and not dorme
    # 2 o jovem morto: sai do registro; o corpo e o tesouro em partes iguais; as peças com quem comanda; sem núcleo
    E = _mundo_covil(); m0 = PM_prata(E); S = _luta_com(E, 'covil', 4, ate='morto'); cs = ['cac1', 'cac2', 'cac3', 'cac4']
    antes = {c: E['gente'][c].get('moedas', 0) for c in cs}
    ef, partes, L = dragoes.depois_da_luta(E, 'covil', S, S['fim'] == 'A', cs)
    estado.aplica(E, 'despojo', ef, onde='covil', texto='as contas da luta com o dragão')
    g = E['gente']; its = E['itens']['itens'].values(); conta = lambda b: [(g[c].get('carga') or {}).get(b, 0) for c in cs]
    R['o jovem morto sai do registro'] = dragoes.de(E, 'covil') is None and S['L'][-1]['estado'] == 'morto'
    R['o corpo e o tesouro em partes iguais (300 de prata, de 3 a 5 de couro Raro, de 2 a 4 de osso Raro)'] = (sum(g[c]['moedas'] - antes[c] for c in cs) == 300 and 3 <= sum(conta('couro:2')) <= 5
        and 2 <= sum(conta('osso:2')) <= 4 and all(max(conta(b)) - min(conta(b)) <= 1 for b in ('couro:2', 'osso:2', 'comida')) and max(g[c]['moedas'] - antes[c] for c in cs) - min(g[c]['moedas'] - antes[c] for c in cs) <= 1)
    R['as peças do tesouro com quem comanda'] = all(it.get('dono') == 'cac1' for it in its if it['nome'] in ('a Espada do Morto', 'o escudo do morto'))
    R['o jovem não dá núcleo'] = not any(it['tipo'] == 'nucleo' for it in its)
    R['a prata do mundo não muda'] = PM_prata(E) == m0 and not estado.valida(E)
    txt2 = ' '.join(L)
    # 3 o adulto morto: o coração (núcleo Épico) com quem comanda
    E = _mundo_covil('grutas', 'adulto'); S = _luta_com(E, 'covil', 5, nivel=90, ate='morto')
    ef, partes, L = dragoes.depois_da_luta(E, 'covil', S, S['fim'] == 'A', ['cac1', 'cac2', 'cac3', 'cac4']); estado.aplica(E, 'despojo', ef, onde='covil', texto='as contas')
    nuc = [it for it in E['itens']['itens'].values() if it['tipo'] == 'nucleo']
    R['o adulto morto dá o coração (um núcleo Épico, com o nome dele, com quem comanda)'] = len(nuc) == 1 and nuc[0]['cat'] == 3 and nuc[0]['nome'] == 'o coração do Brasido' and nuc[0]['dono'] == 'cac1' and nuc[0]['de'] == 'dragão-das-grutas-adulto'
    # 4 o fugido: o PV volta ao registro, dorme até sarar, lembra de quem o feriu; sara dormindo
    E = _mundo_covil(); S = _luta_com(E, 'covil', 2, covil=False, ate='fugiu'); f = S['L'][-1]
    ef, partes, L = dragoes.depois_da_luta(E, 'covil', S, S['fim'] == 'A', ['cac1', 'cac2', 'cac3', 'cac4']); estado.aplica(E, 'despojo', ef, onde='covil', texto='as contas')
    d = dragoes.de(E, 'covil'); dia = E['relogio']['dia']
    R[f"fugido, o PV volta ao registro ({f['pv']} de 480), ele dorme até sarar e lembra de quem o feriu"] = f['estado'] == 'fugiu' and d is not None and d.get('pv') == f['pv'] and d['dorme_ate'] > dia and set(d.get('feriu') or []) >= {'cac1', 'cac2', 'cac3', 'cac4'} and not partes
    for _ in range(3): estado.aplica(E, 'tempo', [['relogio', M.BLOCOS_DIA]], texto='um dia'); dragoes.virada(E)
    R['três dias dormindo: sara 10% do PV por dia'] = dragoes.de(E, 'covil').get('pv', 480) == min(480, f['pv'] + 3 * 48)
    R['o estado fica inteiro'] = not estado.valida(E)
    ruim = [k for k, v in R.items() if not v]
    return [('DR9 O REGISTRO E A LUTA: o dragão entra com o PV de agora; morto, sai do registro, o corpo e o tesouro vão para quem ficou com o campo (as peças com quem comanda) e o coração '
             'entra no Livro (só do adulto para cima); fugido, o PV volta ao registro, e ele dorme até sarar',
             ' · '.join(f'{k}: {sn(v)}' for k, v in R.items()) + f' · o que a mesa leu: "{txt2[:160]}"', not ruim)]


def PM_prata(E): return sum(p['moedas'] for p in E['gente'].values()) + sum((l.get('estoque') or {}).get('prata', 0) for l in E['lugares'].values())


def _roubo(n):
    R = {}
    E = _mundo_covil(dorme=30); d = dragoes.de(E, 'covil')
    R['dormindo, a vigília do jovem é 29 (20 + 75 ÷ 10 + 2)'] = dragoes.vigilia(E, 'covil') == 29 and not dragoes.acordado(E, 'covil') and d['prata_sono'] == 300
    ef, txt = dragoes.punhado(E, 'covil', 'eu'); estado.aplica(E, 'masmorra', ef, onde='covil', texto='um punhado')
    R['o punhado é a sexta parte da prata do sono (50), e a vigília sobe 2'] = E['gente']['eu']['moedas'] == 30 + 50 and dragoes.vigilia(E, 'covil') == 31
    for _ in range(5): ef, txt = dragoes.punhado(E, 'covil', 'eu'); estado.aplica(E, 'masmorra', ef, onde='covil', texto='um punhado')
    R['seis punhados levam a prata toda; a vigília chega a 41'] = E['gente']['eu']['moedas'] == 330 and dragoes.vigilia(E, 'covil') == 41
    ef, txt = dragoes.punhado(E, 'covil', 'eu'); estado.aplica(E, 'masmorra', ef, onde='covil', texto='um punhado')
    R['acabada a prata, o punhado é uma peça'] = sum(1 for it in E['itens']['itens'].values() if it.get('dono') == 'eu' and it.get('onde') is None and it['nome'] in ('a Espada do Morto', 'o escudo do morto')) == 1
    estado.aplica(E, 'masmorra', dragoes.acorda(E, 'covil'), onde='covil', texto='o dragão acorda')
    R['acordado, ninguém rouba (sem vigília), e monta diz que não dorme'] = dragoes.acordado(E, 'covil') and dragoes.vigilia(E, 'covil') is None and dragoes.monta(E, 'covil')[1] is False
    R['o estado fica inteiro'] = not estado.valida(E)
    return [('O ROUBO DE QUEM DORME: a vigília é 20 + Percepção ÷ 10 + 2, mais 2 a cada punhado do sono; o punhado é a sexta parte da prata de quando ele adormeceu (acabada a prata, uma peça); acordado, ninguém rouba',
             ' · '.join(f'{k}: {sn(v)}' for k, v in R.items()), all(R.values()))]


# ---------------------------------------------------------------- A MINA (MI1 a MI6) ----------------------------------------------------------------
def _ano(E, dias):
    """os dias andando (o mundo sozinho: o mercado, a caça, o dragão...), sem ninguém agir"""
    for _ in range(dias): estado.aplica(E, 'tempo', [['relogio', M.BLOCOS_DIA]], texto='um dia'); ato._mundo_vira(E)


def _mina(n):
    import mercado, vila_teste
    out = []
    E = quieto(vila_teste.cria, 'guerreiro', semente=1); passos = []; mundo = lambda: mercado.prata_do_mundo(E)
    m0 = mundo(); L = dragoes.na_vila(E); m1 = mundo(); passos.append(('pôr o Tição e Vau Seco (o gera: 300 do tesouro e 600 da aldeia)', m1 - m0, m1 - m0 == TD.VILA_TESTE['dragao']['tesouro'] + 5 * TD.VILA_TESTE['aldeia']['pop']))
    cov = TD.VILA_TESTE['covil']['id']; vau = TD.VILA_TESTE['aldeia']['id']; tes0 = dragoes._prata(E, cov); v0 = dict(pop=E['lugares'][vau]['pop'], prata=dragoes._prata(E, vau))
    MI6 = (tes0, m1)
    _ano(E, M.ANO); m2 = mundo(); d = dragoes.de(E, cov); tes1 = dragoes._prata(E, cov); v1 = dict(pop=E['lugares'][vau]['pop'], prata=dragoes._prata(E, vau))
    passos.append(('um ano da vida dele', m2 - m1, m2 == m1))
    # a luta: quatro de nível 50 com tudo Épico no covil (vencem sempre); o tesouro para quem ficou com o campo
    at = dict(Força=80, Agilidade=60, Vigor=80, Vontade=80, Percepção=50, Afinidade=40)
    estado.aplica(E, 'gera', [['pessoa', 'nasce', f'cac{j}', dict(nome=f'Caçador {j}', nivel=50, atributos=at, lugar='vila')] for j in range(1, 5)], texto='quatro caçadores de passagem')
    m2b = mundo()
    if not dragoes.acordado(E, cov): estado.aplica(E, 'mestre', dragoes.acorda(E, cov), onde=cov, texto='o dragão acorda')
    S = _luta_com(E, cov, 3, ate='morto')
    ef, partes, Lf = dragoes.depois_da_luta(E, cov, S, S['fim'] == 'A', ['cac1', 'cac2', 'cac3', 'cac4']); estado.aplica(E, 'despojo', ef, onde=cov, texto='as contas da luta com o Tição')
    m3 = mundo(); passos.append(('a luta e o tesouro levado', m3 - m2b, m3 == m2b))
    # a venda em Pedra Rasa: o corpo inteiro, depois as peças; a Épica que a caixa não paga é recusada
    caixa0 = mercado.caixa(E, 'vila'); precos = []; pagou = 0; recusas = []
    for c in ('cac1', 'cac2', 'cac3', 'cac4'):
        for b in ('couro:2', 'osso:2', 'peçonha:2'):
            while E['gente'][c].get('carga', {}).get(b, 0) > 0:
                antes = E['gente'][c]['moedas']; q = 1       # a matéria, uma a uma: o preço cai a cada venda (a comida fica com quem a levou)
                try: quieto(mercado.vender, E, c, b, q)
                except SystemExit as x: recusas.append(f'{b}: {str(x)[:60]}'); break
                pagou += E['gente'][c]['moedas'] - antes
                if b == 'couro:2': precos.append(E['gente'][c]['moedas'] - antes)
    for it in [it for it in E['itens']['itens'].values() if it.get('dono') == 'cac1']:
        antes = E['gente']['cac1']['moedas']
        try: quieto(mercado.vender_peca, E, 'cac1', it['id'])
        except SystemExit as x: recusas.append(f"{it['nome']}: {str(x)[:60]}"); continue
        pagou += E['gente']['cac1']['moedas'] - antes
    m4 = mundo(); passos.append(('a venda', m4 - m3, m4 == m3))
    estado.aplica(E, 'mestre', [['item', 'nasce', item('armadura', 3, 'a malha Épica do tesouro', material='malha', dono='cac2')]], texto='a peça Épica de um tesouro de adulto')
    epica = [it['id'] for it in E['itens']['itens'].values() if it['nome'] == 'a malha Épica do tesouro'][0]; caixa1 = mercado.caixa(E, 'vila')
    try: quieto(mercado.vender_peca, E, 'cac2', epica); epica_recusada = False
    except SystemExit: epica_recusada = True
    out.append(('MI1 A PRATA DO MUNDO: pôr o dragão (o tesouro conta uma vez, no gera), um ano da vida dele, a luta, o tesouro levado e a venda: a mesma antes e depois de cada passo',
                ' · '.join(f'{t}: {dx:+d}' for t, dx, _ in passos), all(ok for _, _, ok in passos)))
    cai = len(precos) >= 2 and all(a >= b for a, b in zip(precos, precos[1:])) and precos[-1] < precos[0]
    out.append(('MI2 O CORPO E O TESOURO DO JOVEM VENDIDOS EM PEDRA RASA: a loja paga até a caixa dela; o preço da matéria Rara cai a cada venda; a peça que a caixa não paga é recusada',
                f"a loja pagou {pagou} (a caixa: {caixa0} → {caixa1}); o couro Raro, peça a peça: {', '.join(map(str, precos))}; a malha Épica (a caixa não a paga): recusada {sn(epica_recusada)}"
                + (f"; recusas no caminho: {'; '.join(recusas[:2])}" if recusas else ''), pagou <= caixa0 and cai and epica_recusada))
    # o dragão morto não volta
    _ano(E, M.ANO); tes2 = dragoes._prata(E, cov)
    out.append(('MI3 O DRAGÃO MORTO NÃO VOLTA: 364 viradas depois, não há dragão no covil, e o estoque do covil não cresceu',
                f"o dragão: {dragoes.de(E, cov)}; a prata do covil depois da luta e um ano depois: 0 e {tes2}; o estado {'inteiro' if not estado.valida(E) else 'QUEBRADO'}",
                dragoes.de(E, cov) is None and tes2 == 0 and not estado.valida(E)))
    out.append(('MI5 UM ANO DO JOVEM AO LADO DE UMA ALDEIA DE 120 (o Tição e Vau Seco): a aldeia perde até 10% do povo e até metade da prata; o tesouro cresce o que a aldeia perde',
                f"{int(d.get('ataques') or 0) - 1} ataques no ano; o povo {v0['pop']} → {v1['pop']}; a prata da aldeia {v0['prata']} → {v1['prata']}; o tesouro {tes0} → {tes1}",
                v0['pop'] - v1['pop'] <= 0.10 * v0['pop'] and v0['prata'] - v1['prata'] <= v0['prata'] / 2 and tes1 - tes0 == v0['prata'] - v1['prata'] and int(d.get('ataques') or 0) > 1))
    out.append(('MI6 OS COVIS JUNTOS: até 25% da prata do mundo (a vila de teste com o Tição)', f"os covis: {MI6[0]} de {MI6[1]} ({100 * MI6[0] / MI6[1]:.1f}%)", MI6[0] <= TD.TESOURO_MUNDO * MI6[1]))
    return out


def _mi4(n):
    """o ladrão robô: o ladino Treinado de couro (Agilidade 80), no escuro, entra uma vez por sono, tira um punhado e sai; falhou o teste (o dado do ladino, de verdade:
    manha.testa contra dragoes.vigilia), o dragão acorda, e a luta é de verdade. Um ano ao lado do jovem e do adulto, com a vida do dragão (dragoes.virada)."""
    import manha
    vidas = max(100, (2 * n) // 3); R = {}
    for idade, tes in (('jovem', 300), ('adulto', 1500)):
        base = PM.vila(7); estado.aplica(base, 'gera', [['lugar', 'vila', 'pop', 'poe', 400]], texto='a vila tem povo')
        g = base['gente']['eu']; g['atributos']['Agilidade'] = 80; g['maestria']['manha'] = 4
        estado.aplica(base, 'gera', [['lugar', 'nasce', 'covil', dict(nome='o covil de prova', em='no covil de prova', tipo='ermo', habitat='serra', perigo=3, longe=2, estoque={}, vizinhos=['vila'], bichos={}, teto={})],
                                     ['lugar', 'vila', 'vizinhos', 'poe', ['covil']]], texto='o covil')
        mortos = 0; dias = 0; levou = 0; punhados = 0; lutas = 0
        for vida in range(vidas):
            E = copy.deepcopy(base); E['_novos'] = []; E['relogio']['semente'] = 1000 + vida; ini = E['relogio']['dia']; vivo = True; m0 = E['gente']['eu']['moedas']
            sono = estado.sorte(E, f'robô|{vida}').randint(*TD.VIDA[idade]['dorme'])         # o ano começa com o dragão adormecendo sobre o tesouro
            E2 = dict(E, lugares=dict(E['lugares'])); estado.aplica(E, 'gera', dragoes.poe(E2, 'covil', 'serra', idade, 'o Velador', vila='vila', tesouro=tes, dorme=sono), onde='covil', texto='o dragão')
            while E['relogio']['dia'] < ini + M.ANO:
                v = dragoes.vigilia(E, 'covil')
                if v is not None:
                    mais = manha.mais_barulhento(E, ['eu'], luz=False)[1]
                    r = manha.testa(E, 'eu', 'escondido', contra=v, o_que='pegar um punhado do tesouro', oculto=True, mais=mais)
                    if r['passou']:
                        ef, _ = dragoes.punhado(E, 'covil', 'eu')
                        if ef: estado.aplica(E, 'masmorra', ef, onde='covil', texto='um punhado'); punhados += 1
                    else:
                        estado.aplica(E, 'masmorra', dragoes.acorda(E, 'covil'), onde='covil', texto='o dragão acorda')
                        p, _ = dragoes.monta(E, 'covil'); p = dict(p); esp = p.pop('bicho'); lutas += 1; luta.semente(5000 + lutas)       # acordado, ele age antes da fuga: a luta abre ali, perto, ninguém surpreendido
                        S = luta.nova([estado.lutador(E, 'eu')], [bichos.bicho(esp, **p)], quieto=True, inicio='perto', lugar=dict(sem_saida='B')); luta.corre(S)
                        if S['L'][0]['estado'] in ('morto', 'caido'): vivo = False; break
                d = dragoes.de(E, 'covil'); falta = max(1, (d['dorme_ate'] - E['relogio']['dia']) if isinstance(d.get('dorme_ate'), int) else 1)
                falta = min(falta, ini + M.ANO - E['relogio']['dia'])
                if falta <= 0: break
                estado.aplica(E, 'tempo', [['relogio', M.BLOCOS_DIA * falta]], texto='os dias de sono'); dragoes.virada(E)
            mortos += not vivo; dias += E['relogio']['dia'] - ini; levou += E['gente']['eu']['moedas'] - m0
        R[idade] = dict(morre=round(100 * mortos / vidas, 1), por_dia=round(levou / max(1, dias), 2), levou=round(levou / vidas), punhados=round(punhados / vidas, 1))
    return [('MI4 O LADRÃO ROBÔ (o ladino Treinado de couro, no escuro, com o dado do ladino de verdade): um punhado por sono, um ano ao lado do jovem e do adulto; morre no ano em 80% das vidas ou mais, '
             f'e tira por dia de vida até 6 de prata (uma diária e meia)',
             ' · '.join(f"{i}: morre em {pc(r['morre'])}, leva {r['levou']} de prata por vida ({r['punhados']} punhados), {r['por_dia']} por dia de vida" for i, r in R.items()) + f' ({vidas} vidas cada)',
             all(r['morre'] >= 80 and r['por_dia'] <= 6 for r in R.values()))]


# ---------------------------------------------------------------- O TIÇÃO NA VILA DE TESTE (E4 a) ----------------------------------------------------------------
def _ticao(n):
    """numa cópia do save do jogador (o ensaio/ só é LIDO): o dragoes.na_vila acrescenta o Tição longe, em Vau Seco, só por eventos, e recusa rodar duas vezes"""
    src = os.path.join(AQUI, 'ensaio')
    if not os.path.exists(os.path.join(src, 'relogio.json')): return [('O TIÇÃO NA VILA (E4 a)', 'não há o save do jogador para copiar', True)]
    d = tempfile.mkdtemp(prefix='provas_dragoes_'); antes = os.environ.get('MOTOR10_MUNDO')
    try:
        shutil.copytree(src, os.path.join(d, 'm')); os.environ['MOTOR10_MUNDO'] = os.path.join(d, 'm')
        E = estado.carrega(); A = copy.deepcopy({k: E[k] for k in ('lugares', 'gente', 'itens')}); vila = 'vila' if 'vila' in E['lugares'] else next(k for k, l in E['lugares'].items() if l.get('tipo') == 'vila')
        import mercado
        m0 = mercado.prata_do_mundo(E); n0 = len(E['_novos']); mesa0 = turno.mesa(E)
        L = dragoes.na_vila(E, vila); C = TD.VILA_TESTE; cov = C['covil']['id']; vau = C['aldeia']['id']; dr = dragoes.de(E, cov)
        igual = all(E['lugares'][k] == v for k, v in A['lugares'].items()) and E['gente'] == A['gente'] and all(E['itens']['itens'].get(k) == v for k, v in A['itens']['itens'].items())
        novos = E['_novos'][n0:]; segredo = [turno.secreto(e) for e in novos]
        txt = turno.mesa(E); linha = next((x for x in dragoes.mesa(E) if x.startswith('- ')), '')
        so = ' '.join(dragoes.so_mestre(E)); dois = PM.recusa(lambda: dragoes.na_vila(E, vila))
        longe = cov not in (E['lugares'][vila].get('vizinhos') or []) and vau not in (E['lugares'][vila].get('vizinhos') or [])
        sem_num = not any(ch in linha for ch in ('PV', 'prata', 'vigília', 'tesouro'))
        ok1 = (igual and dr and dr['nome'] == C['dragao']['nome'] and dr['idade'] == 'jovem' and dr['dorme_ate'] == E['relogio']['dia'] + C['dragao']['dorme'] and longe and dois
               and mercado.prata_do_mundo(E) - m0 == C['dragao']['tesouro'] + 5 * C['aldeia']['pop'] and segredo[-1] and not any(segredo[:-1]) and linha and linha in txt and sem_num
               and 'Vau Seco fica longe' in linha and len(dragoes.guardadas(E, cov)) == 2 and not estado.valida(E) and 'O que se conta' not in mesa0)
        dias = max(0, dr['dorme_ate'] - E['relogio']['dia']) + 3
        quieto(_ano, E, dias); d2 = dragoes.de(E, cov); P = estado.valida(E)
        ok2 = d2 and int(d2.get('ataques') or 0) >= 2 and not P and mercado.prata_do_mundo(E) == m0 + C['dragao']['tesouro'] + 5 * C['aldeia']['pop']
        return [('O TIÇÃO NA VILA DE TESTE (E4 a), numa cópia do save do jogador: o dragoes.na_vila só acrescenta (o que existia sai igual), põe Vau Seco e a Serra Fria longe '
                 '(não são vizinhas da vila), o Tição dormindo sobre 300 de prata e duas peças (o covil vai ao SÓ O MESTRE), a pousada conta dele sem número, e recusa rodar duas vezes; '
                 'quando ele acorda, ataca Vau Seco, e a prata do mundo fecha',
                 f"o que existia igual: {sn(igual)}; longe: {sn(longe)}; o covil em segredo: {sn(segredo[-1] if segredo else False)}; a prata nova (o gera): {C['dragao']['tesouro'] + 5 * C['aldeia']['pop']}; "
                 f"a MESA diz: \"{linha[2:]}\"; duas vezes: {'recusa' if dois else 'NÃO RECUSA'}; {dias} dias depois: {int(d2.get('ataques') or 0) - 1} ataque(s) novo(s), estado {'inteiro' if not P else 'QUEBRADO: ' + P[0]}",
                 bool(ok1 and ok2))]
    finally:
        os.environ.pop('MOTOR10_MUNDO', None)
        if antes is not None: os.environ['MOTOR10_MUNDO'] = antes
        shutil.rmtree(d, ignore_errors=True)


def provas(n=300):
    out = []
    for f in (_especies, _dr1, _dr2, _dr3, _dr4, _dr5, _dr6_8, _dr9, _roubo, _mina, _mi4, _ticao):
        try: out += f(n)
        except (Exception, SystemExit) as x:
            import traceback; out.append((f'{f.__name__}: a prova quebrou', f'{type(x).__name__}: {x} · ' + ' | '.join(traceback.format_exc().splitlines()[-4:-1]).strip(), False))
    return out


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 300
    print('BANCO DE PROVAS DOS DRAGÕES (etapa 4b, capítulo 20)\n')
    res = provas(n)
    for nome, deu, passa in res: print(f"  {'passa' if passa else 'FALHA'}  {nome}: {deu}")
    print(f'\n{sum(p for _, _, p in res)} de {len(res)} provas passam.')
    return all(p for _, _, p in res)


if __name__ == '__main__':
    import signal; hasattr(signal, 'SIGPIPE') and signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    sys.exit(0 if main() else 1)
