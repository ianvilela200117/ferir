#!/usr/bin/env python3
"""corpo.py — MOTOR 10: O CORPO. Fome, sono e cansaço (0 a 10), a ferida que dura, o PV que volta com a noite.

Este script não grava nada: ele só diz QUAIS EFEITOS um bloco de tempo tem no corpo. Quem aplica é o estado.py.
  a pena do corpo (a PIOR das três, não somam) entra em todo teste, no acerto e na Defesa;
  cada 3 pontos de cansaço tiram 1 do fôlego máximo;
  a ferida sara com dias de REPOUSO: não conta o dia de dois blocos pesados, nem o dia em que a pessoa lutou, nem o dia em que passou um bloco ou mais numa saída ao ermo;
  O DESCANSO EM CASA (`casa`): quem NÃO é o personagem cuida de si quando não está em cena. Fora de cena por 3 blocos ou mais, a fome, o sono e o cansaço voltam a zero;
  a cada 6 blocos inteiros, uma noite de cura e um dia de repouso nas feridas. O personagem nunca descansa de graça.

Uso (para olhar): python3 corpo.py ver [ID]      o corpo de alguém (sem ID: o do personagem)
"""
import sys
import tabelas_mundo as M


def pena(p):
    """a pena do corpo de hoje (0 ou negativa): vale o pior dos três medidores"""
    pior = 0
    for m, faixas in M.PENAS.items():
        for limiar, v in faixas:
            if p['corpo'][m] >= limiar: pior = min(pior, v); break
    return pior


def folego_menos(p): return p['corpo']['cansaco'] // M.CANSACO_FOLEGO


def faixa(p, m):
    """em quantos limiares o medidor já passou (0, 1 ou 2): serve para saber quando a ação longa para"""
    return sum(1 for l in M.LIMIARES[m] if p['corpo'][m] >= l)


def faixas(p): return {m: faixa(p, m) for m in M.MEDIDORES}       # o retrato dos limiares, para comparar depois (cruzou)


def cruzou(p, antes):
    """o que o corpo cruzou para cima desde `antes` (o que faixas() devolveu): a frase que faz o ato longo parar, ou None"""
    nomes = dict(fome=['', 'está com fome', 'passa fome'], sono=['', 'está com sono', 'está caindo de sono'], cansaco=['', 'está no limite das forças'])       # frases que servem a qualquer pessoa: não dependem de gênero
    L = [nomes[m][faixa(p, m)] for m in M.MEDIDORES if faixa(p, m) > antes[m]]
    return f"{p['nome']} " + ' e '.join(L) if L else None


def diz(p):
    c = p['corpo']; pn = pena(p); fm = folego_menos(p)
    nomes = dict(fome=['sem fome', 'com fome', 'passando fome'], sono=['sem sono', 'com sono', 'caindo de sono'], cansaco=['com forças', 'no limite das forças'])
    partes = [f"{nomes[m][faixa(p, m)]} ({m.replace('cansaco', 'cansaço')} {c[m]})" for m in M.MEDIDORES]
    return ' · '.join(partes) + (f' · pena −{-pn} em todo teste' if pn else '') + (f' · fôlego máximo −{fm}' if fm else '')


def bloco(E, pid, esforco='nada', dorme=None):
    """os efeitos de UM bloco no corpo de alguém. esforco: pesado, leve, nada, descanso. dorme: None, 'cama' ou 'chao'.
    Chamar ANTES de o relógio andar (a fome sobe pelo relógio de agora)."""
    import estado
    p = E['gente'][pid]; ef = []; t = estado.agora(E)
    if (t + 1) % M.FOME_A_CADA == 0: ef.append(['pessoa', pid, 'fome', 'soma', 1])
    if estado.fora(E, pid) and p.get('marca', {}).get('ermo_dia') != E['relogio']['dia']: ef.append(['pessoa', pid, 'marca.ermo_dia', 'poe', E['relogio']['dia']])       # o dia em que passou um bloco numa saída ao ermo não é dia de repouso (virada)
    if dorme:
        q = M.SONO_CAMA if dorme == 'cama' else M.SONO_CHAO
        ef.append(['pessoa', pid, 'sono', 'soma', q]); ef.append(['pessoa', pid, 'cansaco', 'soma', M.CANSACO_CAMA if dorme == 'cama' else M.SONO_CHAO])
        hoje = p.get('marca', {}); curou = hoje.get('curou', 0) if hoje.get('curou_dia') == E['relogio']['dia'] else 0
        if p['corpo']['fome'] < M.LIMIARES['fome'][0] and curou < M.CURA_DIA and p['pv'] < estado.pv_max(p):
            ef.append(['pessoa', pid, 'pv', 'soma', max(1, int(estado.pv_max(p) * M.CURA_BLOCO))])
            ef.append(['pessoa', pid, 'marca.curou_dia', 'poe', E['relogio']['dia']]); ef.append(['pessoa', pid, 'marca.curou', 'poe', curou + 1])
    else:
        ef.append(['pessoa', pid, 'sono', 'soma', M.SONO_ACORDADO])
        if M.ESFORCO[esforco]: ef.append(['pessoa', pid, 'cansaco', 'soma', M.ESFORCO[esforco]])
        if esforco == 'pesado':
            hoje = p.get('marca', {}); n = hoje.get('pesados', 0) if hoje.get('pesados_dia') == E['relogio']['dia'] else 0
            ef.append(['pessoa', pid, 'marca.pesados_dia', 'poe', E['relogio']['dia']]); ef.append(['pessoa', pid, 'marca.pesados', 'poe', n + 1])
    return ef


def repousou(E, pid):
    """o dia que está acabando conta como REPOUSO para as feridas desta pessoa? Não conta o dia de dois blocos pesados, nem o dia em que ela lutou (marca.luta_dia),
    nem o dia em que passou um bloco ou mais numa saída ao ermo (marca.ermo_dia). Chamar ANTES de o relógio virar o dia."""
    m = E['gente'][pid].get('marca') or {}; dia = E['relogio']['dia']
    pesados = m.get('pesados', 0) if m.get('pesados_dia') == dia else 0
    return pesados < M.PESADOS_SEM_REPOUSO and m.get('luta_dia') != dia and m.get('ermo_dia') != dia


def _repouso(p, pid, dias):
    """os efeitos de `dias` dias de repouso nas feridas de alguém: todas somam os dias, e a que chega ao prazo sara (7 dias; a grave, 21)"""
    ef = [['ferida', pid, 'repousa', dias]]
    for i in reversed(range(len(p['feridas']))):
        f = p['feridas'][i]
        if f['repouso'] + dias >= M.FERIDA_DIAS[1 if f['grave'] else 0]: ef.append(['ferida', pid, 'sara', i])
    return ef


def virada(E, pid):
    """os efeitos da virada do dia no corpo: a fome que come o PV, a ferida que sara com repouso"""
    import estado
    p = E['gente'][pid]; ef = []
    if p['corpo']['fome'] >= M.LIMIARES['fome'][1]: ef.append(['pessoa', pid, 'pv', 'soma', -max(1, int(estado.pv_max(p) * M.FOME_PV))])
    if p['feridas'] and repousou(E, pid): ef += _repouso(p, pid, 1)
    return ef


def fora_de_cena(E, pid):
    """há quantos blocos o corpo desta pessoa não é mexido (o gravador guarda o bloco em marca.cena, de quem não é o personagem). Quem nunca teve o corpo mexido, e a gente
    de um save de antes de a marca existir, conta como tendo descansado: tantos blocos quantos zeram o corpo, e nenhuma noite de cura que o motor não viu passar."""
    import estado
    visto = (E['gente'][pid].get('marca') or {}).get('cena'); t = estado.agora(E)
    return t - visto if isinstance(visto, int) and not isinstance(visto, bool) and 0 <= visto <= t else M.CASA_ZERA


def casa(E, pid):
    """O DESCANSO EM CASA: os efeitos do tempo que alguém que NÃO é o personagem passou fora de cena (quem aplica é o estado.em_cena, num evento só, quando a pessoa volta a agir).
    3 blocos ou mais: a fome, o sono e o cansaço voltam a zero (comeu e dormiu por conta própria). A cada 6 blocos inteiros (um dia): uma noite dormida de cura
    (a mesma do personagem: CURA_BLOCO × CURA_DIA do PV máximo) e um dia de repouso nas feridas. Menos de 3 blocos: nada muda (ela ainda carrega o que a última saída deixou)."""
    import estado
    p = E['gente'][pid]; passou = fora_de_cena(E, pid)
    if p.get('jogador') or p['estado'] != 'vivo' or passou < M.CASA_ZERA: return []
    ef = [['pessoa', pid, m, 'soma', -p['corpo'][m]] for m in M.MEDIDORES if p['corpo'][m] > 0]; noites = passou // M.CASA_NOITE
    if noites and p['pv'] < estado.pv_max(p): ef.append(['pessoa', pid, 'pv', 'soma', noites * M.CURA_DIA * max(1, int(estado.pv_max(p) * M.CURA_BLOCO))])
    if noites and p['feridas']: ef += _repouso(p, pid, noites)
    return ef


if __name__ == '__main__':
    import signal; hasattr(signal, 'SIGPIPE') and signal.signal(signal.SIGPIPE, signal.SIG_DFL)      # a saída cortada (`| head`) acaba o comando calada, sem erro de programa: tudo já foi gravado antes de falar
    a = sys.argv[1:]
    if a[:1] != ['ver'] or len(a) > 2: print(__doc__); sys.exit()
    import estado
    E = estado.carrega(); pid = a[1] if len(a) > 1 else estado.eu(E)
    p = E['gente'].get(pid) or sys.exit(f'não há a pessoa "{pid}"')
    if p['estado'] != 'vivo': print(f"{p['nome']} {estado.morte_diz(E, p)}."); sys.exit()        # do morto só se diz que morreu: não tem fome, nem sono, nem forças
    casa_ = estado.em_cena(E, pid); p = E['gente'][pid]      # quem não é o personagem aparece como VOLTA À CENA agora (o descanso em casa); este comando só olha: nada é gravado
    print(f"{p['nome']} · PV {p['pv']}/{estado.pv_max(p)} · {diz(p)}" + (' · descansou em casa desde a última vez em cena' if casa_ else ''))
    for f in p['feridas']: print(f"  ferida{' GRAVE' if f['grave'] else ''}: {f['parte']} (Dia {f['dia']}; {f['repouso']} de {M.FERIDA_DIAS[1 if f['grave'] else 0]} dias de repouso)")
