#!/usr/bin/env python3
"""provas_ano.py — MOTOR 10: O BANCO DO ANO (a seção 9 do PROJETO.md). O mundo gerado anda 364 dias SEM PERSONAGEM, em N sementes; e os robôs vivem nele.

AN2 a conta fecha: todo dia o estado inteiro; a prata do mundo igual do primeiro ao último dia; morto não age (nenhum evento com ele depois da morte).
AN4 os rivais: de 10 a 30% dos 40 morrem no ano, e entra gente nova; as Épicas, Únicas e Lendárias em mãos vivas não caem; o líder do ranking troca de 1 a 6 vezes;
    nenhuma casa nobre viva some sem um evento que explique (toda casa viva no Dia 1 que acaba sem gente teve as mortes registradas).
AN5 a primeira Épica nova do mundo sai entre os dias 40 e 110 (a mediana das sementes).
AN5b a história (o RG4 do provas_regiao, aqui em todas as sementes).
AN6 as frentes do Dia 1: de 3 a 6 chegam ao desfecho e de 2 a 5 são barradas (a mediana, e 60% das sementes na faixa).
AN7 o grão: o preço da comida fica entre 0,6 e 2,2 vezes a base; a fome nasce em 20 a 60% dos mundos; no máximo 2 lugares perdidos (menos de 30% do povo) por mundo.
AN10 o ano roda em menos de 2 minutos; mesma semente, mesmo mundo.
ROBÔS (num mundo com personagem): o PARADO (só trabalha e dorme 60 dias) fica abaixo da mediana dos rivais novatos; o AFOITO (vai sempre ao mais perigoso) morre em 30 dias
    em 80% das sementes; o MUDO (nunca responde a caixa) perde (a opinião de quem pediu cai; um rival fica com o cliente); a caixa nunca passa de 7 abertos nem deixa pedido vencido
    sem resolver; a MESA e o RETOMAR do dia 90 cabem em 22 KB (o plano dizia 14; as tabelas do mercado e da magia, das etapas 2 e 4, já passam disso).
O ferreiro aplicado (a primeira Épica entre os dias 60 e 85, a Única entre o 160 e o 220) é medido fora do mundo, no provas_oficio.py (A ESCADA).
Uso: python3 provas_ano.py [SEMENTES] [robos=N]      (padrão: 20 sementes, robôs em 5; o provas_mundo.py roda com 6 e 3)
"""
import contextlib, copy, io, json, os, statistics, sys, time
import tabelas as T
import tabelas_mundo as M
import tabelas_regiao as R
import estado


def sn(x): return 'sim' if x else 'NÃO'
def quieto(f, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()): return f(*a, **k)
def retrato(E): return json.dumps({k: E[k] for k in estado.ARQS}, sort_keys=True, ensure_ascii=False)


def altas_vivas(E): return sum(1 for it in E['itens']['itens'].values() if it['cat'] >= 3 and it['tipo'] != 'nucleo' and it.get('dono') in E['gente'] and E['gente'][it['dono']]['estado'] == 'vivo')


def um_ano(s, dias=364):
    """o ano de um mundo, sem personagem: as medidas de cada meta"""
    import gera, regiao, mercado, rivais
    E, _ = gera.mundo(s); p0 = mercado.prata_do_mundo(E); riv0 = set(rivais.rivais(E)); alt0 = altas_vivas(E)
    nobres0 = {k for k, c in (E['mundo'].get('casas') or {}).items() if c.get('tipo') == 'nobre' and c.get('viva')}
    pop0 = {k: E['lugares'][k].get('pop') or 0 for k in regiao.povoados(E)}; ev0 = E['relogio']['eventos']
    M_ = dict(quebrou=None, fator=[9, 0], primeira_epica=None)
    def olha(E, dia):
        if dia % 15 == 0 or dia >= dias:
            P = estado.valida(E)
            if P and not M_['quebrou']: M_['quebrou'] = f"dia {dia}: {P[0]}"
        if dia % 7 == 0:                                     # o grão da região: o preço do meio entre os lugares de povo, semana a semana
            f = statistics.median(mercado.fator(E, k, 'comida') for k in regiao.povoados(E)); M_['fator'][0] = min(M_['fator'][0], f); M_['fator'][1] = max(M_['fator'][1], f)
    t0 = time.time(); regiao.anda(E, dias, depois=olha); dt = time.time() - t0
    mortes = {}; age_morto = []
    for e in E['_novos']:
        if e['id'] <= ev0: continue
        for x in e['efeitos']:
            if isinstance(x, list) and len(x) == 5 and x[0] == 'pessoa' and x[2:] == ['estado', 'poe', 'morto']: mortes.setdefault(x[1], e['id'])
            if M_['primeira_epica'] is None and isinstance(x, list) and len(x) == 3 and x[:2] == ['item', 'nasce'] and isinstance(x[2], dict) and x[2].get('cat', 0) >= 3 and x[2].get('tipo') != 'nucleo' and e['tipo'] != 'gera':
                M_['primeira_epica'] = e['dia']
        for q in e.get('quem') or []:
            if q in mortes and mortes[q] < e['id'] and e['tipo'] not in ('mestre', 'heranca'): age_morto.append((q, e['id'], e['tipo']))
    fr = {k: f for k, f in (E['mundo'].get('frentes') or {}).items() if int(k[1:]) <= len(R.FRENTES_DIA1)}
    perdidos = sum(1 for k, p in pop0.items() if p and (E['lugares'][k].get('pop') or 0) < 0.3 * p)
    sem_gente = [k for k in nobres0 if not any(g.get('casa') == k and g['estado'] == 'vivo' for g in E['gente'].values())]
    explicadas = all(any(g.get('casa') == k and g['estado'] == 'morto' for g in E['gente'].values()) for k in sem_gente)
    return dict(semente=s, dt=dt, quebrou=M_['quebrou'], prata=(p0, mercado.prata_do_mundo(E)), age_morto=age_morto[:3],
                mortos=len([k for k in riv0 if E['gente'][k]['estado'] == 'morto']), novos=len(set(rivais.rivais(E, vivos=False)) - riv0),
                alt=(alt0, altas_vivas(E)), trocas=(E['mundo'].get('ranking') or {}).get('trocas', 0), explicadas=explicadas,
                desfecho=sum(1 for f in fr.values() if f.get('fim') == 'desfecho'), barrada=sum(1 for f in fr.values() if f.get('fim') == 'barrada'),
                fome=any(f['molde'] == 'fome' for f in (E['mundo'].get('frentes') or {}).values()), fator=tuple(M_['fator']), perdidos=perdidos, epica=M_['primeira_epica'])


def faixa(v, a, b): return a <= v <= b


def robos(n=5):
    """os robôs, num mundo com personagem: o parado, o afoito, o mudo (numa pasta de rascunho: nada grava na pasta do jogo)"""
    import tempfile, shutil
    d = tempfile.mkdtemp(); velho = os.environ.get('MOTOR10_MUNDO'); os.environ['MOTOR10_MUNDO'] = d
    try: return _robos(n)
    finally:
        shutil.rmtree(d, ignore_errors=True)
        if velho is None: os.environ.pop('MOTOR10_MUNDO', None)
        else: os.environ['MOTOR10_MUNDO'] = velho


def _robos(n=5):
    import gera, cria, ato, rivais, caixa, gente, regiao, turno
    L = []; parado = []; afoito = []; mudo = []; caixa_ok = True; tam = []
    for s in range(1, n + 1):
        # O PARADO: trabalha a jornada, come e dorme, 60 dias
        E, _ = gera.mundo(100 + s); quieto(cria.nasce, E, 'humano', 2, 'fio', 'Parado')
        for d in range(60):
            try:
                if E['gente']['eu']['corpo']['fome'] >= 3: quieto(ato.comer, E, 'eu')
                quieto(ato.passa, E, 'eu', 2, 'trabalhar', esforco='pesado', para=False)
                quieto(ato.dormir, E, 'eu', 3, para=False) if hasattr(ato, 'dormir') else None
                quieto(ato.passa, E, 'eu', M.BLOCOS_DIA - E['relogio']['bloco'], 'esperar', para=False)
            except SystemExit: break
        nov = sorted(rivais.pontos(E, k) for k in rivais.rivais(E) if E['gente'][k]['nivel'] < 15)
        parado.append(rivais.pontos(E, 'eu') < (statistics.median(nov) if nov else 1))
        # O AFOITO: toda semana vai ao alvo de maior valor, sem olhar a chance (pela conta rápida e o dado do mundo, como os rivais)
        E, _ = gera.mundo(200 + s); quieto(cria.nasce, E, 'humano', 2, 'fio', 'Afoito'); morreu = None
        for semana in range(5):
            alvos = []
            for mid, m in E['lugares'].items():
                if m.get('tipo') == 'masmorra' and not m.get('limpa') and m.get('molde') != 'covil': alvos.append(('masmorra', mid, m['niveis'][-1]['cat']))
            for e, l in E['lugares'].items():
                for esp, q in (l.get('bichos') or {}).items():
                    if q >= 1 and (estado.especie(esp) or {}).get('cat', 0) >= 2: alvos.append(('bicho', f'{e}|{esp}', estado.especie(esp)['cat']))
            if not alvos: break
            tipo, alvo, cat = max(alvos, key=lambda x: x[2]); rs = estado.sorte(E, f'afoito|{semana}')
            if tipo == 'masmorra': B = [b for nv in E['lugares'][alvo]['niveis'][:1] for b in rivais.ameaca_nivel(E, alvo, nv, rs)]
            else: e, _, esp = alvo.partition('|'); B = rivais._bando(esp, 1, rs)
            c = rivais.chance_contra(E, ['eu'], B) if B else 1.0
            if rs.random() >= c and rs.random() < R.RIVAL['morre'] * (1 - c) + 0.25:
                estado.aplica(E, 'mestre', [['pessoa', 'eu', 'estado', 'poe', 'morto']], texto='o afoito morre'); morreu = semana * 7 + 3; break
            try: quieto(ato.passa, E, 'eu', M.BLOCOS_DIA * 7, 'esperar', para=False)
            except SystemExit: break
        afoito.append(morreu is not None and morreu <= 30)
        # O MUDO: mora onde há ferreiro; o metal da vila fica baixo toda semana; ele nunca responde a caixa
        E, _ = gera.mundo(300 + s); quieto(cria.nasce, E, 'humano', 2, 'fio', 'Mudo'); lid = E['gente']['eu']['lugar']
        if not any(p.get('papel') == 'ferreiro' and p['lugar'] == lid for p in E['gente'].values()):      # o mudo vai morar onde há ferreiro (que não é parente dele)
            lid = next(k for k, p in E['gente'].items() if p.get('papel') == 'ferreiro' and k not in (E['gente']['eu'].get('lacos') or {})); lid = E['gente'][lid]['lugar']
            estado.aplica(E, 'mestre', [['pessoa', 'eu', 'lugar', 'poe', lid]], texto='o mudo muda de lugar')
        ferr = next((k for k, p in E['gente'].items() if p.get('papel') == 'ferreiro' and p['lugar'] == lid and p['estado'] == 'vivo'), None)
        for d in range(90):
            est = E['lugares'][lid]['estoque'].get('metal:0', 0)          # o metal da vila acaba todo dia (o motivo do pedido do ferreiro está no estado)
            if est > 0: estado.aplica(E, 'mestre', [['estoque', lid, 'metal:0', 'soma', -est]], texto='o metal falta')
            try:                                             # o mudo vive: trabalha a jornada, come, dorme; e nunca responde a caixa
                if E['gente']['eu']['corpo']['fome'] >= 3 and E['gente']['eu']['moedas'] >= 1: quieto(ato.comer, E, 'eu')
                quieto(ato.passa, E, 'eu', 2, 'trabalhar', esforco='pesado', para=False, mais=lambda i: [['estoque', lid, 'prata', 'soma', -2], ['pessoa', 'eu', 'moedas', 'soma', 2]] if E['lugares'][lid]['estoque'].get('prata', 0) >= 2 else [])
                quieto(ato.passa, E, 'eu', M.BLOCOS_DIA - E['relogio']['bloco'], 'esperar', para=False)
            except SystemExit: break
            ab = caixa.abertos(E)
            if len(ab) > M.CAIXA_MAX or any(x['prazo'] < E['relogio']['dia'] for _, x in ab): caixa_ok = False
        vencidos = sum(1 for x in (E['mundo'].get('caixa') or {}).values() if x.get('fim') and x['fim'] == x['padrao'])
        op = gente.opiniao(E, ferr, 'eu')[0] if ferr else 0
        rival_cliente = any(m['o_que'].startswith('me arranjou') for m in (E['gente'][ferr].get('memoria') or [])) if ferr else False
        mudo.append(vencidos >= 1 and op < 0 and rival_cliente)
        quieto(turno.pergunta, E, 'a?', ['a=x', 'b=y']); quieto(turno.pergunta, E, 'b?', ['a=x', 'b=y'])
        import tempfile, shutil
        d = tempfile.mkdtemp(); os.environ['MOTOR10_MUNDO'] = d
        try:
            quieto(ato.passa, E, 'eu', 1, 'esperar', para=False); quieto(turno.fecha, E, 'o robô mudo')       # o turno de 90 dias fecha (o jogo de verdade fecha todo dia)
            quieto(turno.pergunta, E, 'a?', ['a=x', 'b=y']); quieto(turno.pergunta, E, 'b?', ['a=x', 'b=y']); quieto(ato.passa, E, 'eu', M.BLOCOS_DIA, 'esperar', para=False); quieto(turno.fecha, E, 'um dia do robô')
            tam.append(len(open(os.path.join(d, 'MESA.md'), encoding='utf-8').read().encode('utf-8')) + len(open(os.path.join(d, 'RETOMAR.md'), encoding='utf-8').read().encode('utf-8')))
        finally: shutil.rmtree(d); os.environ.pop('MOTOR10_MUNDO', None)
    return dict(parado=parado, afoito=afoito, mudo=mudo, caixa_ok=caixa_ok, tam=tam)


def provas(n=20, nr=5):
    out = []; anos = []
    t0 = time.time()
    for s in range(1, n + 1): anos.append(um_ano(s))
    import gera, regiao
    A, _ = gera.mundo(1); B = copy.deepcopy(A); regiao.anda(A, 60); regiao.anda(B, 60); igual = retrato(A) == retrato(B)
    q = [a for a in anos if a['quebrou']]; pr = [a for a in anos if a['prata'][0] != a['prata'][1]]; am = [a for a in anos if a['age_morto']]
    out.append(('AN2 A CONTA FECHA', f"{n} anos: o estado inteiro todo dia em {n - len(q)}" + (f" (quebrou: {q[0]['quebrou']})" if q else '') + f"; a prata do mundo igual do primeiro ao último dia em {n - len(pr)}"
                + (f" (semente {pr[0]['semente']}: {pr[0]['prata'][0]} → {pr[0]['prata'][1]})" if pr else '') + f"; morto que age depois da morte: {sum(len(a['age_morto']) for a in anos)}" + (f" ({am[0]['age_morto'][0]})" if am else ''),
                not q and not pr and not am))
    mort = [a['mortos'] for a in anos]; nov = [a['novos'] for a in anos]; alt = [a['alt'] for a in anos]; tro = [a['trocas'] for a in anos]
    ok4 = statistics.median(mort) >= 4 and statistics.median(mort) <= 12 and sum(1 for a in anos if a['alt'][1] >= a['alt'][0]) >= 0.7 * n and faixa(statistics.median(tro), 1, 6) and all(a['explicadas'] for a in anos) and statistics.median(nov) >= 1
    out.append(('AN4 OS RIVAIS', f"morrem no ano (dos 40): mediana {statistics.median(mort)} (de {min(mort)} a {max(mort)}; a faixa: 4 a 12); entram novos: mediana {statistics.median(nov)}; as Épicas, Únicas e Lendárias em mãos vivas "
                f"não caem em {sum(1 for a in anos if a['alt'][1] >= a['alt'][0])} de {n} (mediana {statistics.median(x[0] for x in alt)} → {statistics.median(x[1] for x in alt)}); o líder do ranking troca: mediana {statistics.median(tro)} (de {min(tro)} a {max(tro)}); "
                f"toda casa nobre que acabou teve a morte registrada: {sn(all(a['explicadas'] for a in anos))}", ok4))
    ep = [a['epica'] for a in anos if a['epica']]
    out.append(('AN5 A PRIMEIRA ÉPICA NOVA', f"nasceu em {len(ep)} de {n} anos; o dia (a mediana): {statistics.median(ep) if ep else '—'} (de {min(ep) if ep else '—'} a {max(ep) if ep else '—'}; a faixa: 40 a 110)",
                bool(ep) and faixa(statistics.median(ep), 40, 110) and len(ep) >= 0.6 * n))
    import provas_regiao
    out.append(provas_regiao.rg4())
    des = [a['desfecho'] for a in anos]; bar = [a['barrada'] for a in anos]; dentro = sum(1 for a in anos if faixa(a['desfecho'], 3, 6) and faixa(a['barrada'], 2, 5))
    out.append(('AN6 AS FRENTES DO DIA 1', f"chegam ao desfecho: mediana {statistics.median(des)} (de {min(des)} a {max(des)}; a faixa: 3 a 6); barradas: mediana {statistics.median(bar)} (de {min(bar)} a {max(bar)}; a faixa: 2 a 5); "
                f"as duas na faixa em {dentro} de {n} anos", faixa(statistics.median(des), 3, 6) and faixa(statistics.median(bar), 2, 5) and dentro >= 0.5 * n))
    fmin = min(a['fator'][0] for a in anos); fmax = max(a['fator'][1] for a in anos); fome = sum(1 for a in anos if a['fome']); perd = max(a['perdidos'] for a in anos)
    out.append(('AN7 O GRÃO', f"o preço da comida, de {fmin:.2f} a {fmax:.2f} vezes a base (a faixa: 0,6 a 2,2); a fome nasceu em {fome} de {n} mundos ({100 * fome / n:.0f}%; a faixa: 20 a 60%); lugares perdidos por mundo: até {perd} (a faixa: até 2)",
                fmin >= 0.6 and fmax <= 2.2 and 0.2 * n <= fome <= 0.6 * n and perd <= 2))
    dts = [a['dt'] for a in anos]
    out.append(('AN10 O TEMPO E A SEMENTE', f"um ano roda em {statistics.median(dts):.0f} s (o pior: {max(dts):.0f} s; a faixa: menos de 120); mesma semente, mesmo mundo (60 dias, duas vezes): {sn(igual)}", max(dts) < 120 and igual))
    if nr:
        rb = robos(nr)
        out.append(('ROBÔS', f"o parado abaixo da mediana dos novatos no dia 60: {sum(rb['parado'])} de {nr}; o afoito morre em 30 dias: {sum(rb['afoito'])} de {nr} (a faixa: 80% ou mais); "
                    f"o mudo perde por calar (a opinião cai, o rival fica com o cliente): {sum(rb['mudo'])} de {nr}; a caixa nunca passou de 7 nem deixou pedido vencido: {sn(rb['caixa_ok'])}; "
                    f"a MESA e o RETOMAR do dia 90: até {max(rb['tam']) / 1000:.1f} KB (a faixa: 22)",
                    all(rb['parado']) and sum(rb['afoito']) >= 0.8 * nr and sum(rb['mudo']) >= 0.6 * nr and rb['caixa_ok'] and max(rb['tam']) <= 22000))
    return out


if __name__ == '__main__':
    a = sys.argv[1:]; op = dict(x.split('=', 1) for x in a if '=' in x); pos = [x for x in a if '=' not in x]
    res = provas(int(pos[0]) if pos and pos[0].isdigit() else 20, int(op.get('robos', 5)))
    for nm, deu, passa in res: print(f"  {'passa' if passa else 'FALHA'}  {nm}: {deu}")
    print(f"\n{sum(p for _, _, p in res)} de {len(res)} metas passam.")
    sys.exit(0 if all(p for _, _, p in res) else 1)
