"""m8: o protótipo da VIDA DO DRAGÃO (a regra proposta, escrita aqui em rascunho), um ano inteiro ao lado de uma aldeia, sobre o gravador de verdade (eventos "mestre"; o mundo é
uma cópia da vila de teste carregada em memória e NUNCA gravada). Mede: quantas vezes ele ataca, quanta comida e prata leva, quanta gente morre, se a prata do mundo fecha."""
import sys, io, contextlib
sys.path.insert(0, '/tmp/claude-0/-home-user-ferir/2caa978a-1aa4-5b05-88b7-11bcda935cb0/scratchpad/masmorras/projeto_b/medidas')
from base_b import *
import estado, mercado
import tabelas_mundo as M

# A REGRA PROPOSTA (os números do tabelas_dragoes.VIDA)
VIDA = {   # dorme: dias de sono depois de comer · come: comida de uma refeição grande · prata: o que leva da vila no ataque (de, até) · mata: gente que morre no ataque (de, até)
           # tributo: a fração da prata da vila que ele cobra por estação (do adulto para cima); quem paga não é atacado
    'jovem':  dict(dorme=(20, 40), come=30, prata=(5, 20), mata=(0, 1), tributo=0),
    'adulto': dict(dorme=(30, 60), come=60, prata=(20, 60), mata=(0, 3), tributo=0.03),
    'velho':  dict(dorme=(90, 180), come=120, prata=(50, 150), mata=(1, 5), tributo=0.05),
    'ancião': dict(dorme=(300, 400), come=200, prata=(100, 300), mata=(2, 8), tributo=0.08),
}


def virada(E, lid):
    l = E['lugares'][lid]; d = dict(l['covil']['dragao']); V = VIDA[d['idade']]; dia = E['relogio']['dia']; r = estado.sorte(E, f'dragao|{lid}|{dia}'); vila = d['vila']; v = E['lugares'][vila]
    if dia < d['dorme_ate']: return None
    ef = []; txt = []
    # a estação: o tributo (do adulto para cima). Pago, ele não ataca a vila nesta estação
    est = (dia - 1) // M.ESTACAO
    if V['tributo'] and d.get('tributo_est') != est:
        q = int(v['estoque'].get('prata', 0) * V['tributo'])
        if q > 0: ef += [['estoque', vila, 'prata', 'soma', -q], ['estoque', lid, 'prata', 'soma', q]]; txt.append(f'a vila paga o tributo: {q} de prata'); d['tributo_est'] = est; d['pago'] = True
        else: d['pago'] = False
    if V['tributo'] and d.get('pago'):
        # pago o tributo, ele come da caça do ermo (fora desta conta) e volta a dormir
        d['dorme_ate'] = dia + r.randint(*V['dorme']); txt.append('come do ermo e dorme')
    else:
        q = min(V['come'], int(v['estoque'].get('comida', 0))); p = min(r.randint(*V['prata']), int(v['estoque'].get('prata', 0))); m = min(r.randint(*V['mata']), int(v.get('pop', 0)))
        if q: ef.append(['estoque', vila, 'comida', 'soma', -q])
        if p: ef += [['estoque', vila, 'prata', 'soma', -p], ['estoque', lid, 'prata', 'soma', p]]
        if m: ef.append(['lugar', vila, 'pop', 'soma', -m])
        d['ataques'] = d.get('ataques', 0) + 1; d['mortos'] = d.get('mortos', 0) + m; d['comida'] = d.get('comida', 0) + q; d['levou'] = d.get('levou', 0) + p
        d['dorme_ate'] = dia + r.randint(*V['dorme']); txt.append(f'ataca de noite: leva {q} de gado, {p} de prata; morrem {m}')
    c = dict(l['covil']); c['dragao'] = d; ef.insert(0, ['lugar', lid, 'covil', 'poe', c])
    with contextlib.redirect_stdout(io.StringIO()): estado.aplica(E, 'mestre', ef, onde=lid, texto='o dragão: ' + '; '.join(txt))
    return d


def ano(idade, pop=120, tesouro=400, semente=1):
    E = estado.carrega(); E['relogio']['semente'] = semente
    with contextlib.redirect_stdout(io.StringIO()):
        estado.aplica(E, 'gera', [['lugar', 'nasce', 'vau', dict(nome='Vau Seco', em='em Vau Seco', tipo='aldeia', estoque={})],
                                  ['lugar', 'nasce', 'covil', dict(nome='a Serra Fria', em='na Serra Fria', tipo='ermo', habitat='serra', perigo=3, longe=3, estoque={'prata': tesouro},
                                                                   covil=dict(nome='o covil do dragão', dragao=dict(nome='o dragão da Serra Fria', tipo='serra', idade=idade, vila='vau', dorme_ate=3)))]],
                      texto='rascunho: a aldeia e o covil')
        mercado.funda(E, 'vau', pop, como='rascunho')
    vila0 = dict(prata=E['lugares']['vau']['estoque'].get('prata', 0), pop=E['lugares']['vau']['pop'], comida=E['lugares']['vau']['estoque'].get('comida', 0))
    mundo0 = mercado.prata_do_mundo(E); d = None
    for _ in range(364):
        with contextlib.redirect_stdout(io.StringIO()):
            estado.aplica(E, 'tempo', [['relogio', M.BLOCOS_DIA]], texto='um dia')
            mercado.virada(E)
        d = virada(E, 'covil') or d
    d = E['lugares']['covil']['covil']['dragao']; v = E['lugares']['vau']
    return dict(ataques=d.get('ataques', 0), mortos=d.get('mortos', 0), comida=d.get('comida', 0), levou=d.get('levou', 0), pop=(vila0['pop'], v['pop']),
                prata_vila=(vila0['prata'], v['estoque'].get('prata', 0)), tesouro=(tesouro, E['lugares']['covil']['estoque'].get('prata', 0)), mundo=(mundo0, mercado.prata_do_mundo(E)),
                comida_vila=(vila0['comida'], int(v['estoque'].get('comida', 0))))


for idade, pop, tes in (('jovem', 120, 400), ('adulto', 400, 1500), ('adulto', 120, 1500), ('velho', 1500, 4000), ('ancião', 4000, 8000)):
    for sem in (1, 2, 3):
        x = ano(idade, pop, tes, sem)
        print(f"{idade:<7} ao lado de uma vila de {pop} (semente {sem}): {x['ataques']} ataques, {x['mortos']} mortos (o povo: {x['pop'][0]} → {x['pop'][1]}), "
              f"{x['comida']} de gado levado (a comida da vila: {x['comida_vila'][0]} → {x['comida_vila'][1]}), {x['levou']} de prata levada no ataque; a prata da vila {x['prata_vila'][0]} → {x['prata_vila'][1]}; "
              f"o tesouro {x['tesouro'][0]} → {x['tesouro'][1]}; a prata do mundo {x['mundo'][0]} → {x['mundo'][1]}")
