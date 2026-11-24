#!/usr/bin/env python3
"""provas_fantasia.py — MOTOR 10: O BANCO DA INTEGRAÇÃO DA ETAPA 4b (as metas que cruzam as frentes: a masmorra, o ladino, os povos e os dragões; o contrato: projeto/ETAPA_4B.md).

FA1 O COMANDO `vila_teste.py fantasia` numa cópia do save do jogador: só eventos do gerador; nada de antes muda além do que o comando acrescenta (a manha rolada de quem já nasceu,
    a segunda inclinação do personagem, e na vila a gente, a loja da descida e a cripta por vizinha); a prata nova é só a dos lugares e da gente nova; o relógio não anda;
    o segredo vai ao SÓ O MESTRE; a segunda vez recusa sem mudar nada; grava e abre de novo.
FA2 A VILA NOVA COM `povo=`: cada povo nasce inteiro (a soma dos atributos é a do começo, a idade de adulto do povo, a armadura do corpo miúdo feita para ele, em uso);
    sem povo, o personagem de sempre; com povo=humano, os mesmos atributos, talentos e dons; a segunda inclinação só no humano; e o +2 do povo nos testes do ladino, no teto.
FA3 O ROUBO DO COVIL PELA MASMORRA (o robô ladrão pelos comandos da descida, o dado do ladino de verdade): quem não passa pela vigília acorda o dragão, e a luta abre ali, sem
    fuga; um ano ao lado de um covil com um dragão jovem: morre no ano em 80% das vidas ou mais, e tira até 6 de prata por dia de vida (a faixa do MI4).
FA4 QUEM VÊ NO ESCURO NA MASMORRA: fora da luta, o grupo em que todos veem no escuro anda sem tocha no passo de sempre, procura, abre e desarma; o grupo misto anda no dobro,
    e o humano não procura; na luta, o grupo que vê no escuro vence, no escuro, mais que o humano no escuro e menos que o humano com luz.
FA5 A MINA QUE SE PROCURA: o personagem que desce a cripta e vende tudo o que lhe coube não passa de 12 de prata por dia nos cinco primeiros dias (o que tira lá dentro
    e vende, menos as tochas e a parte dos outros nas peças, sem o custo de viver: a conta da meta da forja do mercado). Duas linhas: o robô prudente com Tomé e Rute; e o
    robô guloso (o do verificador) com a gente forte da vila inteira (vila_teste.fantasia), que não espera sarar e pega todas as peças que pode pagar.
FA6 O ANÃO NA PEDRA: o achar da masmorra (a armadilha e a passagem escondida) é "na pedra" pelo molde dela (a cripta, a mina e a ruína; a toca e o covil, não).
Os mundos são de rascunho (pastas temporárias); o save do jogador (ensaio/) só é LIDO, numa cópia. As lutas têm semente; o dado do jogador, nos robôs, também.
Uso: python3 provas_fantasia.py [N]      (o provas_mundo.py também roda este banco)
"""
import contextlib, copy, io, os, shutil, sys, tempfile
import tabelas as T
import tabelas_mundo as M
import tabelas_povos as TP
import tabelas_talento as TT
import tabelas_manha as TMH
import tabelas_masmorra as K
import estado, ato, turno, teste, talento, luta, mercado, povos, manha, dragoes, vila_teste
import masmorra as MS
import provas_mundo as PM
import provas_masmorra as PMS
from itens import item

AQUI = os.path.dirname(os.path.abspath(__file__))


def quieto(f, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()): return f(*a, **k)
def recusa(f): return PM.recusa(f)
def sn(x): return 'sim' if x else 'NÃO'
def pct(x): return f"{100 * x:.1f}%".replace('.', ',')
def num(x, k=2): return f"{x:.{k}f}".replace('.', ',')


@contextlib.contextmanager
def pasta(prefixo='m10_fant_'):
    d = tempfile.mkdtemp(prefix=prefixo); antes = os.environ.get('MOTOR10_MUNDO'); os.environ['MOTOR10_MUNDO'] = d
    try: yield d
    finally:
        if antes is None: os.environ.pop('MOTOR10_MUNDO', None)
        else: os.environ['MOTOR10_MUNDO'] = antes
        shutil.rmtree(d, ignore_errors=True)


# ---------------------------------------------------------------- FA1 O COMANDO NA CÓPIA DO SAVE ----------------------------------------------------------------
VILA_MUDA = {'povos', 'vizinhos', 'feira_masmorra', 'estoque', 'produz', 'alvo_pecas'}      # o que a etapa muda na vila: a gente, a cripta por vizinha, a loja da descida (a tocha, a gazua)


def _fa1(n):
    nome = ('FA1 O COMANDO `vila_teste.py fantasia` numa cópia do save do jogador: só eventos do gerador; nada de antes muda além do que ele acrescenta; a prata nova é só a dos lugares e da '
            'gente nova; o relógio não anda; o segredo vai ao SÓ O MESTRE; a segunda vez recusa sem mudar nada; grava e abre')
    src = os.path.join(AQUI, 'ensaio')
    if not os.path.exists(os.path.join(src, 'relogio.json')): return [(nome, 'não há o save do jogador para copiar', True)]
    with pasta() as d:
        dst = os.path.join(d, 'save'); shutil.copytree(src, dst); os.environ['MOTOR10_MUNDO'] = dst
        E = estado.carrega(); A = copy.deepcopy({k: E[k] for k in ('gente', 'itens', 'lugares', 'relogio')}); p0 = mercado.prata_do_mundo(E); n0 = E['relogio']['eventos']
        if 'cripta' in E['lugares'] or 'quim' in E['gente']:
            t = recusa(lambda: vila_teste.fantasia(E)) or ''
            return [(nome, f"o save já tem a etapa 4b: a segunda vez recusa ({t[:80]}); o estado {'inteiro' if not estado.valida(E) else 'QUEBRADO'}", bool(t) and not estado.valida(E))]
        if estado.luta_aberta(E):
            t = recusa(lambda: vila_teste.fantasia(E)) or ''
            return [(nome, f"há luta aberta no save: o comando recusa antes de mudar qualquer coisa ({t[:60]})", bool(t) and E['relogio']['eventos'] == n0)]
        eu = E['gente'].get('eu') or {}
        inc2 = 'manha' if eu.get('estado') == 'vivo' and povos.de(eu) == 'humano' and not eu.get('inclinacao2') and 'manha' in talento.falta(eu) else None
        torto = recusa(lambda: vila_teste.fantasia(E, 'fio')); torto_ok = bool(torto) and E['relogio']['eventos'] == n0       # a segunda inclinação num caminho já rolado: recusa antes de tudo
        nev, L = quieto(vila_teste.fantasia, E, inc2)
        evs = E['_novos'][-(E['relogio']['eventos'] - n0):]
        so_gera = len(evs) == nev and all(e['tipo'] == 'gera' for e in evs)
        segredo = [e for e in evs if any(isinstance(x, list) and len(x) > 3 and ((x[0] == 'lugar' and x[1] == 'nasce' and isinstance(x[3], dict) and x[3].get('tipo') in ('masmorra', 'sala'))
                                                                                     or x[2] in ('dragao', 'talento')) for x in e['efeitos'])]
        no_mestre = bool(segredo) and all(turno.secreto(e) for e in segredo)
        dois = recusa(lambda: vila_teste.fantasia(E)); n1 = E['relogio']['eventos']
        # nada de antes muda além do que a etapa acrescenta
        ruim = []
        for k, p in A['gente'].items():
            q = E['gente'][k]
            for c in set(p) | set(q):
                if p.get(c) == q.get(c): continue
                if c == 'talento' or (c == 'inclinacao2' and k == 'eu'): continue
                if c == 'marca' and {m for m in set(p.get('marca') or {}) | set(q.get('marca') or {}) if (p.get('marca') or {}).get(m) != (q.get('marca') or {}).get(m)} <= {'talento_novos', 'talento_base'}: continue
                ruim.append(f'{k}.{c}')
        for k, it in A['itens']['itens'].items():
            if E['itens']['itens'].get(k) != it: ruim.append(f'item {k}')
        for k, l in A['lugares'].items():
            m = E['lugares'][k]
            for c in set(l) | set(m):
                if l.get(c) == m.get(c): continue
                if k == 'vila' and c in VILA_MUDA:
                    if c == 'estoque' and {b for b in set(l.get(c) or {}) | set(m.get(c) or {}) if (l.get(c) or {}).get(b) != (m.get(c) or {}).get(b)} - {'tocha'}: ruim.append('vila.estoque (fora a tocha)')
                    continue
                ruim.append(f'{k}.{c}')
        relogio = (E['relogio']['dia'], E['relogio']['bloco'], E['relogio']['semente']) == (A['relogio']['dia'], A['relogio']['bloco'], A['relogio']['semente'])
        roladas = [k for k in A['gente'] if A['gente'][k].get('estado') == 'vivo' and talento.falta(A['gente'][k]) and not talento.falta(E['gente'][k])]
        faltam = [k for k, p in E['gente'].items() if p.get('estado') == 'vivo' and talento.falta(p)]
        novos_l = [k for k in E['lugares'] if k not in A['lugares']]; novos_p = [k for k in E['gente'] if k not in A['gente']]
        prata_nova = mercado.prata_do_mundo(E) - p0
        esperado = sum(int((E['lugares'][k].get('estoque') or {}).get('prata', 0)) for k in novos_l) + sum(int(E['gente'][k].get('moedas', 0)) for k in novos_p)
        P = estado.valida(E)
        estado.grava(E); E2 = estado.carrega(); volta = not estado.valida(E2) and 'cripta' in E2['lugares'] and 'quim' in E2['gente'] and E2['relogio']['eventos'] == n1
    ok = (so_gera and no_mestre and bool(dois) and n1 == E['relogio']['eventos'] and torto_ok and not ruim and relogio and not faltam and prata_nova == esperado and not P and volta
          and (inc2 is None or E['gente']['eu'].get('inclinacao2') == inc2))
    return [(nome, f"{nev} eventos, todos do gerador: {sn(so_gera)} ({len(segredo)} com o mapa, o dragão ou o talento, ao SÓ O MESTRE: {sn(no_mestre)}); a manha rolada de {len(roladas)} "
                   f"pessoas (falta a alguém: {', '.join(faltam) or 'ninguém'}); a segunda inclinação do personagem: {E['gente']['eu'].get('inclinacao2') or 'nenhuma'}; "
                   f"lugares novos: {len(novos_l)}, gente nova: {', '.join(E['gente'][k]['nome'] for k in novos_p)}; mudou de antes, fora o previsto: {', '.join(ruim) or 'nada'}; o relógio igual: {sn(relogio)}; "
                   f"prata nova {prata_nova} (a dos lugares e da gente nova: {esperado}); a inclinação num caminho já rolado: {'recusada antes de tudo' if torto_ok else 'ACEITA'}; "
                   f"a segunda vez: {'recusada' if dois and n1 == E['relogio']['eventos'] else 'ACEITA'}; o estado {'inteiro' if not P else 'QUEBRADO: ' + P[0]}; grava e abre: {sn(volta)}", ok)]


# ---------------------------------------------------------------- FA2 A VILA NOVA COM povo= ----------------------------------------------------------------
def _fa2(n):
    ruim = []; linhas = []
    base = vila_teste.cria('guerreiro', semente=3, talentos=True)
    hum = vila_teste.cria('guerreiro', semente=3, talentos=True, povo='humano')
    b, h = base['gente']['eu'], hum['gente']['eu']
    if not (b['atributos'] == h['atributos'] and b.get('talento') == h.get('talento') and b.get('dom') == h.get('dom') and 'povo' not in b and h.get('povo') == 'humano'):
        ruim.append('o humano de povo=humano não é o de sempre')
    soma0 = sum(vila_teste.COMECOS['guerreiro']['atributos'].values())
    for pv, r in TP.POVOS.items():
        for comeco in vila_teste.COMECOS:
            E = vila_teste.cria(comeco, semente=5, talentos=True, povo=pv); eu = E['gente']['eu']
            soma = sum(eu['atributos'].values()) == sum(vila_teste.COMECOS[comeco]['atributos'].values())
            idade = r['vida'][0] < eu.get('idade', -1) <= r['vida'][0] + TP.IDADE_DADO
            arms = [it for it in E['itens']['itens'].values() if it.get('dono') == 'eu' and it['tipo'] == 'armadura']
            talhe = all((it.get('talhe') == 'miúdo') == (r.get('corpo') == 'miúdo') and it.get('uso') == 'veste' for it in arms)
            if not (soma and idade and talhe and eu.get('povo') == pv and not estado.valida(E)): ruim.append(f'{pv}/{comeco}')
        linhas.append(f"{pv} {E['gente']['eu']['idade']} anos")
    so_humano = bool(recusa(lambda: vila_teste.cria('guerreiro', talentos=True, povo='anão', inclinacao2='fio')))
    duas = bool(recusa(lambda: vila_teste.cria('guerreiro', talentos=True, inclinacao='fio', inclinacao2='fio')))
    H2 = vila_teste.cria('guerreiro', semente=3, talentos=True, inclinacao='fio', inclinacao2='manha'); h2 = H2['gente']['eu']
    inc2 = h2.get('inclinacao2') == 'manha' and h2.get('inclinacao') == 'fio' and not estado.valida(H2)
    # o +2 do povo nos testes do ladino (manha.testa soma povos.manha, cortado no MANHA_TETO): a mesma pessoa com e sem o povo
    E = vila_teste.cria('guerreiro', semente=5, talentos=True); mh = []
    for pv in TP.POVOS:
        for t in TMH.TESTES:
            for pedra in (False, True):
                p = E['gente']['eu']; q = dict(p, povo=pv)
                E['gente']['eu'] = q; com = manha._soma(E, 'eu', t, pedra=pedra); E['gente']['eu'] = p; sem = manha._soma(E, 'eu', t, pedra=pedra)
                quer = min(TP.MANHA_TETO, (TP.MANHA.get(pv) or {}).get(t, 0) + ((TP.MANHA.get(pv) or {}).get('achar_pedra', 0) if t == 'achar' and pedra else 0))
                if com - sem != quer or quer > TP.MANHA_TETO: mh.append(f'{pv}/{t}')
    bonus = ', '.join(f"{pv}: " + ' e '.join(f"+{v} {k}" for k, v in (TP.MANHA.get(pv) or {}).items()) for pv in TP.POVOS if TP.MANHA.get(pv))
    ok = not ruim and so_humano and duas and inc2 and not mh
    return [('FA2 A VILA NOVA COM `povo=` (os 6 povos, os 3 começos): a soma dos atributos é a do começo; a idade de adulto do povo; a armadura do corpo miúdo nasce miúda e em uso; '
             'com povo=humano, os mesmos atributos, talentos e dons de sempre; a segunda inclinação só no humano, noutro caminho; o +2 do povo nos testes do ladino, no teto de +2',
             f"tortos: {', '.join(ruim) or 'nenhum'} ({soma0} de soma no guerreiro; " + ', '.join(linhas) + f"); a segunda inclinação no anão: {'recusada' if so_humano else 'ACEITA'}; igual à primeira: "
             f"{'recusada' if duas else 'ACEITA'}; o humano com fio e manha: {sn(inc2)}; o bônus do povo no dado do ladino ({bonus}): " + ('certo, no teto, em todos os testes' if not mh else 'ERRADO em ' + ', '.join(mh[:6])), ok)]


# ---------------------------------------------------------------- FA3 O ROUBO DO COVIL PELA MASMORRA ----------------------------------------------------------------
def _covil_de_prova(s, idade='jovem'):
    """a vila de prova com um covil do gerador (molde covil, a categoria da idade) por vizinho, a porta do fundo já aberta, e o ladrão: o ladino Treinado de couro, Agilidade 80
    (o do MI4). O dragão dorme sobre o tesouro"""
    E = PM.vila(s); estado.aplica(E, 'gera', [['lugar', 'vila', 'pop', 'poe', 400]], texto='a vila tem povo')
    g = E['gente']['eu']; g['atributos']['Agilidade'] = 80; g['maestria']['manha'] = 4
    cat = TD_cat(idade)
    estado.aplica(E, 'gera', MS.gera(E, 'covil', 'a Gruta de Prova', 'vila', cat=cat, longe=1), texto='o covil')
    mid = next(k for k, l in E['lugares'].items() if l.get('tipo') == 'masmorra'); f = MS.fundo(E, mid)
    ef = [['lugar', mid, f'portas.{k}', 'poe', dict(p, estado='aberta')] for k, p in (E['lugares'][mid].get('portas') or {}).items()]
    if ef: estado.aplica(E, 'gera', ef, texto='as portas já abertas')
    d = dragoes.de(E, f); tem = int((E['lugares'][f].get('estoque') or {}).get('prata', 0)); sono = max(1, (d.get('dorme_ate') or E['relogio']['dia'] + 1) - E['relogio']['dia'])
    estado.aplica(E, 'gera', [['lugar', f, 'dragao', 'poe', None]], texto='prova')                  # o tesouro do MI4 (300 de prata no jovem): o mundo de prova é pequeno, e o teto do gerador é uma fração dele
    estado.aplica(E, 'gera', dragoes.poe(E, f, d['tipo'], d['idade'], d['nome'], vila=d.get('vila'), tesouro=max(0, TESOURO_MI4[idade] - tem), dorme=sono), texto='o dragão dorme sobre o tesouro')
    return E, mid, f


TESOURO_MI4 = dict(jovem=300, adulto=1500)           # o tesouro do ladrão robô do MI4 (provas_dragoes)


def TD_cat(idade):
    import tabelas_dragoes as TD
    return TD.IDADES[idade]['cat']


def _caminho(E, de_, para):
    """as salas do caminho mais curto (pelas passagens), sem a de partida"""
    ant = {de_: None}; fila = [de_]
    while fila:
        x = fila.pop(0)
        if x == para: break
        for v in E['lugares'][x].get('vizinhos') or []:
            if v not in ant and (E['lugares'].get(v) or {}).get('tipo') == 'sala': ant[v] = x; fila.append(v)
    c = []; x = para
    while x is not None and x != de_: c.append(x); x = ant.get(x)
    return c[::-1]


def _luta_ate_o_fim(E):
    for _ in range(300):
        d = MS.descida(E['gente']['eu'])
        if not d or d.get('fase') != 'luta': return
        try: quieto(MS.luta_roda, E, 'eu', ['Aldric: atacar'])
        except SystemExit: quieto(MS.luta_roda, E, 'eu', [])
    raise RuntimeError('a luta não acaba')


def _ladrao(s, idade='jovem'):
    """UMA VIDA DO LADRÃO: a cada sono do dragão, desce no escuro, anda escondido até a câmara, pega um punhado e sai (recuar, sair). Quem acorda o dragão luta ali."""
    E, mid, f = _covil_de_prova(s, idade); ini = E['relogio']['dia']; m0 = E['gente']['eu']['moedas']; C = dict(punhados=0, lutas=0, acordou_na_porta=0, abriu_na_hora=0, recuou=0, tirou=0)
    while E['relogio']['dia'] < ini + M.ANO and E['gente']['eu']['estado'] == 'vivo':
        if dragoes.vigilia(E, f) is None:
            dr = dragoes.de(E, f)
            if not dr: break
            estado.aplica(E, 'tempo', [['relogio', M.BLOCOS_DIA]], texto='um dia'); dragoes.virada(E); continue
        estado.aplica(E, 'gera', [['pessoa', 'eu', m, 'soma', -M.MED_MAX] for m in M.MEDIDORES], texto='o ladrão descansou em casa')
        quieto(MS.descer, E, 'eu', mid, luz='nada')
        for sala in _caminho(E, MS.descida(E['gente']['eu'])['sala'], f):
            R = quieto(MS.ir, E, 'eu', sala, escondido=True)
            if R.get('fase') == 'luta': C['lutas'] += 1; C['acordou_na_porta'] += 1; C['abriu_na_hora'] += 1; _luta_ate_o_fim(E); break
            if R.get('fase') == 'encontro' and sala == f: break
        if E['gente']['eu']['estado'] != 'vivo': break
        d = MS.descida(E['gente']['eu'])
        if d and d.get('fase') == 'encontro' and d['encontro'].get('viu') == 'grupo' and dragoes.vigilia(E, f) is not None:
            m1 = E['gente']['eu']['moedas']; R = quieto(MS.punhado, E, 'eu')
            if R.get('fase') == 'luta': C['lutas'] += 1; C['abriu_na_hora'] += 1; _luta_ate_o_fim(E)
            elif E['gente']['eu']['moedas'] > m1 or R.get('fase') == 'encontro': C['punhados'] += 1; C['tirou'] += E['gente']['eu']['moedas'] - m1      # o que o punhado deu (morto depois, conta igual: é o que a renda tirou do tesouro)
        if E['gente']['eu']['estado'] != 'vivo': break
        d = MS.descida(E['gente']['eu'])
        if d and d.get('fase') == 'encontro':
            try: quieto(MS.recuar, E, 'eu'); C['recuou'] += 1
            except SystemExit: pass
        if E['gente']['eu']['estado'] != 'vivo': break
        d = MS.descida(E['gente']['eu'])
        if d and d.get('fase') == 'luta': _luta_ate_o_fim(E)
        if E['gente']['eu']['estado'] != 'vivo': break
        if MS.descida(E['gente']['eu']):
            try: quieto(MS.sair, E, 'eu')
            except SystemExit: quieto(MS.larga, E, 'eu', 'o robô não acha a saída')
        if E['gente']['eu']['estado'] != 'vivo': break
        dr = dragoes.de(E, f)
        falta = max(1, (dr['dorme_ate'] - E['relogio']['dia']) if dr and isinstance(dr.get('dorme_ate'), int) else 1)
        falta = min(falta, ini + M.ANO - E['relogio']['dia'])
        if falta <= 0: break
        estado.aplica(E, 'tempo', [['relogio', M.BLOCOS_DIA * falta]], texto='os dias de sono'); dragoes.virada(E)
    C.update(morreu=E['gente']['eu']['estado'] != 'vivo', dias=max(1, E['relogio']['dia'] - ini), levou=E['gente']['eu']['moedas'] - m0, inteiro=not estado.valida(E))
    return C


def _fa3(n):
    vidas = max(40, n // 5); out = []
    with pasta():
        for s in range(1, vidas + 1):
            luta.semente(3000 + s)
            with PMS.dado_semente(4000 + s): out.append(_ladrao(s))
        # as recusas e o caminho certo, à mão: o dragão acordado que viu o grupo vem atrás; o que acorda não deixa recuar
        E, mid, f = _covil_de_prova(1)
        estado.aplica(E, 'masmorra', dragoes.acorda(E, f), texto='o dragão acorda')
        quieto(MS.descer, E, 'eu', mid, luz='nada'); fase = None
        for sala in _caminho(E, MS.descida(E['gente']['eu'])['sala'], f): fase = quieto(MS.ir, E, 'eu', sala).get('fase')
        vem = None
        if fase == 'encontro': vem = quieto(MS.recuar, E, 'eu').get('fase')
    mortos = sum(C['morreu'] for C in out) / len(out); dias = sum(C['dias'] for C in out); levou = sum(C['tirou'] for C in out); por_dia = levou / dias
    na_hora = sum(C['abriu_na_hora'] for C in out); lutas = sum(C['lutas'] for C in out)
    certo = all(C['inteiro'] for C in out)
    ok = mortos >= 0.80 and por_dia <= 6 and certo and na_hora == lutas and vem == 'luta'
    return [('FA3 O ROUBO DO COVIL PELA MASMORRA (o ladino Treinado de couro, Agilidade 80, no escuro, pelos comandos da descida, com o dado do ladino de verdade): a cada sono do dragão jovem, '
             'desce escondido até a câmara, pega um punhado e sai; quem não passa pela vigília (na porta da câmara ou no punhado) acorda o dragão, e a luta abre ali, sem fuga; o dragão acordado '
             'que viu o grupo vem atrás; um ano: morre em 80% das vidas ou mais e tira até 6 de prata por dia de vida (a faixa do MI4)',
             f"morre no ano em {pct(mortos)} das {len(out)} vidas; leva {num(levou / len(out), 1)} de prata por vida ({num(sum(C['punhados'] for C in out) / len(out), 1)} punhados), "
             f"{num(por_dia)} por dia de vida; {lutas} lutas com o dragão, todas abertas na hora ({sum(C['acordou_na_porta'] for C in out)} acordado na porta da câmara); "
             f"o dragão acordado vem atrás de quem recua: {sn(vem == 'luta')}; o estado inteiro em todas: {sn(certo)}", ok)]


# ---------------------------------------------------------------- FA4 QUEM VÊ NO ESCURO NA MASMORRA ----------------------------------------------------------------
def _fa4(n):
    R = {}
    with pasta():
        E = PMS.vila(2, tochas=0); quieto(povos.na_vila, E)
        estado.aplica(E, 'gera', [['pessoa', 'eu', 'povo', 'poe', 'anão'], ['item', 'nasce', item('gazua', 0, dono='eu')]], texto='o personagem é anão (prova)')
        # o grupo de anões, sem luz
        quieto(MS.descer, E, 'eu', 'cripta', com=['durva'], ordem=['durva', 'eu'], luz='nada')
        l0 = MS.descida(E['gente']['eu'])['lances']; quieto(MS.ir, E, 'eu', 'cripta_2'); d = MS.descida(E['gente']['eu'])
        R['anda'] = d['lances'] - l0 == K.CUSTO['ir']
        quieto(MS.larga, E, 'eu', 'prova')
        E = PMS.vila(2, tochas=0); quieto(povos.na_vila, E)
        estado.aplica(E, 'gera', [['pessoa', 'eu', 'povo', 'poe', 'anão'], ['item', 'nasce', item('gazua', 0, dono='eu')], ['lugar', 'cripta_4', 'bichos.ratazana', 'soma', -4],
                                  ['lugar', 'cripta_2', 'bichos.corpo-seco', 'soma', -2], ['lugar', 'cripta_2', 'armadilhas', 'poe', []],
                                  ['lugar', 'cripta', 'portas.cripta_1|cripta_2', 'poe', dict(estado='aberta', material='madeira', cat=0, fechadura=None)]], texto='o corredor e a capela vazios (prova)')
        quieto(MS.descer, E, 'eu', 'cripta', com=['durva'], ordem=['durva', 'eu'], luz='nada')
        for s_ in ('cripta_2', 'cripta_4'):
            r = quieto(MS.ir, E, 'eu', s_)
            if r.get('fase') == 'luta': PMS.luta_robo(E, 'eu')
        procura = not recusa(lambda: quieto(MS.procurar, E, 'eu', quem='eu'))
        desarma = not recusa(lambda: quieto(MS.desarmar, E, 'eu', 1, quem='eu')) if MS._achadas(E, 'cripta_4') else True
        abre = not recusa(lambda: quieto(MS.abrir, E, 'eu', 'guardado', 'gazua', quem='eu'))
        R['faz'] = procura and abre and desarma
        quieto(MS.larga, E, 'eu', 'prova')
        # o grupo misto (o anão e o Tomé), sem luz: anda no dobro; o humano não procura, o anão sim
        E = PMS.vila(2, tochas=0); estado.aplica(E, 'gera', [['pessoa', 'eu', 'povo', 'poe', 'anão'], ['lugar', 'cripta_2', 'bichos.corpo-seco', 'soma', -2], ['lugar', 'cripta_2', 'armadilhas', 'poe', []]], texto='prova')
        quieto(MS.descer, E, 'eu', 'cripta', com=['tome'], ordem=['tome', 'eu'], luz='nada')
        quieto(MS.abrir, E, 'eu', 'cripta_2'); l0 = MS.descida(E['gente']['eu'])['lances']; quieto(MS.ir, E, 'eu', 'cripta_2'); l1 = MS.descida(E['gente']['eu'])['lances']
        R['misto'] = l1 - l0 == 2 * K.CUSTO['ir']
        R['humano_nao'] = bool(recusa(lambda: quieto(MS.procurar, E, 'eu', quem='tome'))) and not recusa(lambda: quieto(MS.procurar, E, 'eu', quem='eu'))
        quieto(MS.larga, E, 'eu', 'prova')
        # a luta no escuro: Maro, Tomé e Rute contra seis esqueletos (a MA2), humanos e com o traço
        k = max(300, n); P = PMS._grupo_vila()
        tr = lambda x: dict(x, tracos=list(x.get('tracos') or []) + ['vê no escuro'])
        hum = lambda: [P('eu'), P('tome'), P('rute', linha='trás')]
        vee = lambda: [tr(P('eu')), tr(P('tome')), tr(P('rute', linha='trás'))]
        import bichos
        seis = lambda: bichos.bando('esqueleto', n=6)
        luz, _ = PMS._duelos(hum, seis, k, inicio='perto'); esc, _ = PMS._duelos(hum, seis, k, inicio='perto', tempo=['escuro']); ve, _ = PMS._duelos(vee, seis, k, inicio='perto', tempo=['escuro'])
    ok = R['anda'] and R['faz'] and R['misto'] and R['humano_nao'] and esc < ve < luz
    return [('FA4 QUEM VÊ NO ESCURO NA MASMORRA: sem tocha, o grupo de anões anda no passo de sempre, procura, abre com a gazua e desarma; o grupo misto anda no dobro, e o humano não procura '
             '(o anão sim); na luta, contra seis esqueletos, o grupo que vê no escuro vence no escuro mais que o humano no escuro e menos que o humano com luz',
             f"anda no passo de sempre: {sn(R['anda'])}; procura, abre e desarma: {sn(R['faz'])}; o grupo misto no dobro: {sn(R['misto'])}; o humano não procura e o anão sim: {sn(R['humano_nao'])}; "
             f"a luta ({k} por linha): humanos com luz {pct(luz)}, humanos no escuro {pct(esc)}, os mesmos vendo no escuro {pct(ve)}", ok)]


# ---------------------------------------------------------------- FA5 A MINA QUE SE PROCURA ----------------------------------------------------------------
def _rende(E, pid):
    """o que a cripta rende à pessoa (como o MINA_COMECO do mercado: o que entra menos o que a atividade gasta, sem o custo de viver): a prata que ela tira lá
    dentro (evento masmorra), o que a loja paga pelo que ela vende (venda), menos as tochas (compra)"""
    r = {'masmorra': 0, 'venda': 0, 'tochas': 0}; arq = os.path.join(estado.pasta(), 'eventos.jsonl')
    import json
    gravados = [json.loads(x) for x in open(arq, encoding='utf-8')] if os.path.exists(arq) else []      # o que já foi para o arquivo, e o que ainda está na memória
    for e in gravados + list(E['_novos']):
        tipo = e['tipo'] if e['tipo'] in ('masmorra', 'venda') else 'tochas' if e['tipo'] == 'compra' and 'tocha' in (e.get('texto') or '') else None
        if tipo: r[tipo] += sum(x[4] for x in e['efeitos'] if isinstance(x, list) and x[:4] == ['pessoa', pid, 'moedas', 'soma'])
    return r


FORTE = ('durva', 'brasco', 'ilvena', 'tome', 'rute')       # a gente forte da vila de teste com a etapa inteira (vila_teste.fantasia): quem o robô guloso leva


def _guloso(s, dias=5):
    """UMA VIDA DO ROBÔ GULOSO (o do verificador): a etapa inteira na vila (vila_teste.fantasia); desce às 8h quando todos têm metade do PV, com a gente forte da vila,
    sem prudência; o personagem pega tudo o que pode (a peça, pagando a parte dos outros) e vende tudo. Devolve o que a cripta lhe rendeu por dia (a conta do FA5)"""
    luta.semente(31 * s)
    with PMS.dado_semente(37 * s):
        E = vila_teste.cria(semente=s); quieto(vila_teste.magia, E); quieto(vila_teste.fantasia, E)
        p0 = PMS.prata_do_mundo(E); d0 = E['relogio']['dia']; com = [c for c in FORTE if c in E['gente']]
        ordem = [c for c in ('durva', 'brasco', 'tome') if c in com] + ['eu'] + [c for c in com if c not in ('durva', 'brasco', 'tome')]
        while E['relogio']['dia'] - d0 < dias and E['gente']['eu']['estado'] == 'vivo':
            vistas = set(((E['gente']['eu'].get('marca') or {}).get('mapa') or {}).get('cripta', {}).get('salas') or [])
            if PMS.esgotada(E) and 'cripta_7' in vistas: PMS.em_casa(E, 'eu'); continue
            vivos = [c for c in com if E['gente'][c]['estado'] == 'vivo' and E['gente'][c]['lugar'] == E['gente']['eu']['lugar']]
            if E['relogio']['bloco'] == 2 and all(E['gente'][c]['pv'] >= 0.5 * estado.pv_max(E['gente'][c]) for c in ['eu'] + vivos):
                t = (E['gente']['eu'].get('carga') or {}).get('tocha', 0)
                if t < 3: PMS.compra_tochas(E, 'eu', 3 - t)
                try: PMS.desce(E, 'eu', vivos, [x for x in ordem if x in ['eu'] + vivos], prudente=False)
                except SystemExit: pass
                PMS.vende(E, 'eu')
                if E['gente']['eu']['estado'] == 'vivo' and E['relogio']['bloco'] != 2:
                    falta = (2 - E['relogio']['bloco']) % M.BLOCOS_DIA
                    if falta: quieto(ato.dormir, E, 'eu', falta, chao=E['gente']['eu']['moedas'] < M.CAMA_PRECO, para=False)
            else: PMS.em_casa(E, 'eu')
        eu = E['gente']['eu']
        if eu['estado'] == 'vivo': PMS.vende(E, 'eu')
        r = _rende(E, 'eu')
        return dict(rende=(r['masmorra'] + r['venda'] + r['tochas']) / dias, vivo=eu['estado'] == 'vivo', fecha=PMS.prata_do_mundo(E) == p0)


def _fa5(n):
    vidas = max(16, n // 15); out = []
    for s in range(1, vidas + 1):
        with pasta():                                       # uma pasta por vida: o registro de eventos é só desta vida
            luta.semente(9 * s)
            with PMS.dado_semente(13 * s): C, E = PMS.vida(s, 'grupo', dias=5, vender=True)
            eu = E['gente']['eu']
            if eu['estado'] == 'vivo': PMS.vende(E, 'eu')
            r = _rende(E, 'eu'); D5 = 5
            out.append(dict(rende=(r['masmorra'] + r['venda'] + r['tochas']) / D5, tirou=r['masmorra'] / D5, vendeu=r['venda'] / D5, tochas=-r['tochas'] / D5, liq=(eu['moedas'] - vila_teste.PRATA) / D5,
                            vivo=eu['estado'] == 'vivo', limpa=C['limpa'], fecha=C['prata_fecha']))
    vivos = [o for o in out if o['vivo']] or out; md = lambda c: sum(o[c] for o in vivos) / len(vivos)
    media = md('rende'); pior = max(o['rende'] for o in vivos)
    gul = []
    for s in range(1, vidas + 1):
        with pasta(): gul.append(_guloso(s))
    gv = [o for o in gul if o['vivo']] or gul; mg = sum(o['rende'] for o in gv) / len(gv)
    ok = media <= 12 and mg <= 12 and all(o['fecha'] for o in out + gul)
    return [('FA5 A MINA QUE SE PROCURA: o personagem desce a Cripta da Cova Velha (até 5 dias), pega o que lhe cabe (a prata repartida; a peça com quem a pega, que paga a parte dos outros) '
             'e vende tudo o que pode na loja: o que a cripta lhe rende nos cinco primeiros dias (o que tira e vende, menos as tochas; como a meta da forja do mercado) é até 12 de prata por dia em média, '
             'com o robô prudente e Tomé e Rute, e com o robô guloso e a gente forte da vila (Durva, Brasco, Ilvena, Tomé e Rute)',
             f"o prudente, {len(out)} vidas (limpam {pct(sum(o['limpa'] for o in out) / len(out))}; morre o personagem em {pct(1 - sum(o['vivo'] for o in out) / len(out))}): rende {num(media)} de prata por dia em média "
             f"(a prata tirada lá dentro, já com a parte dos outros paga, {num(md('tirou'))}, a loja {num(md('vendeu'))}, as tochas −{num(md('tochas'))}; a melhor vida, {num(pior)}); no bolso, livre do custo de viver, {num(md('liq'))} por dia; "
             f"o guloso com a gente forte, {len(gul)} vidas (morre o personagem em {pct(1 - sum(o['vivo'] for o in gul) / len(gul))}): rende {num(mg)} por dia em média (a melhor vida, {num(max(o['rende'] for o in gv))}); "
             f"a prata do mundo fecha em todas: {sn(all(o['fecha'] for o in out + gul))}", ok)]


# ---------------------------------------------------------------- FA6 O ANÃO NA PEDRA ----------------------------------------------------------------
def _fa6(n):
    """FA6. O ANÃO NA PEDRA (o capítulo 19.7): o achar da masmorra (a armadilha e a passagem escondida) leva o "na pedra" pelo molde dela (a cripta, a mina e a ruína, sim;
    a toca e o covil, não), e não pelo tipo da armadilha. O +2 que o anão ganha com ele, o FA2 confere"""
    visto = []; real = manha.testa
    def espia(E, pid, teste, *a, **k):
        if teste == 'achar': visto.append(bool(k.get('pedra')))
        return real(E, pid, teste, *a, **k)
    def procura(E):
        visto.clear(); quieto(MS.procurar, E, 'eu'); return list(visto)
    with pasta():
        E = PMS.vila(1); arm = [dict(tipo='dardo', cat=0, onde='porta:cripta_5', achada=None, feita=None)]; seg = [dict(para='cripta_4', cat=0)]
        estado.aplica(E, 'mestre', [['lugar', x, 'bichos', 'poe', {}] for x in ('cripta_2', 'cripta_3')] + [['lugar', 'cripta_2', 'armadilhas', 'poe', []], ['lugar', 'cripta_3', 'armadilhas', 'poe', arm],
                                    ['lugar', 'cripta_3', 'segredos', 'poe', seg]], texto='o ossário com uma armadilha na porta e uma passagem escondida (a prova)')
        quieto(MS.descer, E, 'eu', 'cripta', com=['tome', 'rute'], luz='tocha'); quieto(MS.ir, E, 'eu', 'cripta_2'); quieto(MS.ir, E, 'eu', 'cripta_3')
        MS._manha().testa = espia
        try:
            cripta = procura(E)
            estado.aplica(E, 'mestre', [['lugar', 'cripta', 'molde', 'poe', 'toca'], ['lugar', 'cripta_3', 'armadilhas', 'poe', arm], ['lugar', 'cripta_3', 'segredos', 'poe', seg]], texto='a mesma sala, numa toca (a prova)')
            toca = procura(E)
        finally: MS._manha().testa = real
        moldes = {m: MS.na_pedra(dict(E, lugares=dict(E['lugares'], cripta=dict(E['lugares']['cripta'], molde=m))), 'cripta_3') for m in M.MOLDES}
    ok = cripta == [True, True] and toca == [False, False] and moldes == {m: m in K.PEDRA for m in M.MOLDES} and set(K.PEDRA) == {'cripta', 'mina', 'ruína'}
    return [('FA6 O ANÃO NA PEDRA: na masmorra de pedra (a cripta, a mina, a ruína), o achar da armadilha e da passagem escondida conta como "na pedra" (o +2 do anão); na toca e no covil, não; '
             'o que decide é o molde da masmorra, e não o tipo da armadilha',
             f"a armadilha e a passagem procuradas na cripta: {'na pedra' if cripta == [True, True] else cripta}; as mesmas numa toca: {'fora da pedra' if toca == [False, False] else toca}; "
             f"os moldes de pedra: {', '.join(m for m, v in moldes.items() if v)}", ok)]


METAS = [_fa1, _fa2, _fa3, _fa4, _fa5, _fa6]


def provas(n=300):
    """as metas da integração: a lista de (nome, o que deu, passa)"""
    res = []
    for f in METAS:
        try: res += f(n)
        except SystemExit as x: res.append((f.__name__.strip('_').upper(), f'RECUSADO NO MEIO: {x}', False))
    return res


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 300
    print('BANCO DA INTEGRAÇÃO DA ETAPA 4b (vila_teste.py fantasia, povo=, o covil pela masmorra, quem vê no escuro, a mina)\n')
    res = provas(n)
    for nome, deu, passa in res: print(f"  {'passa' if passa else 'FALHA'}  {nome}: {deu}")
    print(f'\n{sum(p for _, _, p in res)} de {len(res)} provas passam.')
    return all(p for _, _, p in res)


if __name__ == '__main__':
    sys.exit(0 if main() else 1)
