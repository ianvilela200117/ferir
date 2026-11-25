#!/usr/bin/env python3
"""noticias.py — MOTOR 10, ETAPA FINAL: A NOTÍCIA. Todo evento que importa vira notícia, que nasce num lugar de povo e anda UMA ESTRADA POR DIA;
do quarto salto em diante é boato ("dizem que..."). O personagem só lê o que chegou aonde ele está. A JANELA DO MUNDO chega a todo lugar no mesmo dia.

  python3 noticias.py ver [LUGAR]        as notícias que chegaram a um lugar (ao do personagem, sem LUGAR)
  python3 noticias.py todas              SÓ O MESTRE: todas, com onde nasceram e até onde andaram
"""
import sys
import tabelas_mundo as M
import tabelas_regiao as R
import estado


def tem(E): return bool((E.get('mundo') or {}).get('meta'))


def origem(E, lid):
    """o lugar de povo de onde uma notícia parte: o próprio (se é de povo), a ponta da estrada, o vizinho do ermo, o vizinho da masmorra da sala"""
    Ls = E['lugares']; l = Ls.get(lid) if isinstance(lid, str) else None
    if not isinstance(l, dict): return None
    if l.get('tipo') in M.POVOADOS: return lid
    if l.get('tipo') == 'estrada': return l['ponta'][0]
    if l.get('tipo') == 'sala': return origem(E, l.get('masmorra'))
    for v in l.get('vizinhos') or []:
        if isinstance(Ls.get(v), dict) and Ls[v].get('tipo') in M.POVOADOS: return v
    for v in l.get('vizinhos') or []:
        o = origem(E, v) if isinstance(Ls.get(v), dict) and Ls[v].get('tipo') not in ('sala', 'masmorra') and v != lid else None
        if o: return o
    return None


def nova(E, onde, texto, peso=1, tags=(), janela=False, ja=()):
    """os efeitos que fazem nascer uma notícia (vão no evento de quem a causa, ou num evento "noticia"). [] se o mundo não tem região ou o lugar não manda notícia.
    `ja`: os efeitos que vão no mesmo evento antes destes (as outras notícias dele contam no número)"""
    if not tem(E): return []
    o = origem(E, onde)
    if not o: return []
    W = E['mundo']; n = ((W.get('seq') or {}).get('noticia') or 0) + 1 + sum(1 for x in ja if list(x[:3]) == ['mundo', 'seq', 'noticia']); nid = f'n{n:05d}'; dia = E['relogio']['dia']
    chegou = {k: [dia, 0] for k, l in E['lugares'].items() if isinstance(l, dict) and l.get('tipo') in M.POVOADOS} if janela else {o: [dia, 0]}
    return [['mundo', 'seq', 'noticia', 'soma', 1], ['mundo', 'noticias', nid, 'poe', dict(dia=dia, onde=o, texto=texto, peso=peso, tags=list(tags), chegou=chegou, janela=bool(janela))]]


def da(E, onde, texto, peso=1, tags=(), janela=False, tipo='noticia'):
    """faz nascer a notícia num evento só dela"""
    ef = nova(E, onde, texto, peso, tags, janela)
    if ef: estado.aplica(E, tipo, ef, onde=onde, texto=('a janela do mundo: ' if janela else 'notícia: ') + texto)
    return ef


def virada(E):
    """um salto por dia: de cada lugar aonde a notícia chegou antes de hoje, ela vai aos vizinhos pelas estradas abertas; a velha some"""
    if not tem(E): return
    import regiao
    hoje = E['relogio']['dia']; G = regiao.grafo(E); ef = []
    for nid, n in (E['mundo'].get('noticias') or {}).items():
        if hoje - n['dia'] > R.NOTICIA_DURA: ef.append(['mundo', 'noticias', nid, 'poe', None]); continue
        ch = dict(n['chegou']); novo = False
        for lid, (d, s) in list(n['chegou'].items()):
            if d >= hoje: continue
            for y, e, bl, ab in G.get(lid, []):
                if ab and y not in ch: ch[y] = [hoje, s + 1]; novo = True
        if novo: ef.append(['mundo', 'noticias', nid, 'chegou', 'poe', ch])
    if ef: estado.aplica(E, 'noticia', ef, texto='as notícias andam')


def diz(E, n, saltos):
    t = n['texto']
    return (f"dizem que {t[0].lower() + t[1:]}" if saltos >= R.BOATO_SALTO and not n.get('janela') else t)


def chegadas(E, lid):
    """as notícias que chegaram a um lugar: [(dia em que chegou, saltos, notícia)], das mais novas"""
    out = [(n['chegou'][lid][0], n['chegou'][lid][1], n) for n in (E['mundo'].get('noticias') or {}).values() if lid in n.get('chegou', {})]
    return sorted(out, key=lambda x: (-x[0], -x[2]['peso']))


def mesa(E):
    if not tem(E): return []
    pid = estado.eu(E)
    if not pid or E['gente'][pid]['estado'] != 'vivo' or estado.fora(E, pid): return []
    lid = E['gente'][pid]['lugar']; ch = chegadas(E, lid)[:R.MESA_NOTICIAS]
    if not ch: return []
    return ['**Notícias que chegaram aqui** (as mais novas):'] + [f"- Dia {d}" + (f" (de {E['lugares'][n['onde']]['nome']})" if n['onde'] != lid else '') + f": {diz(E, n, s)}" for d, s, n in ch]


def gera(E, r):
    """as notícias do Dia 1: o que anda sendo contado (o dragão que cobra, as estradas com salteador, a guilda de fama)"""
    if not tem(E): return []
    ef = []
    for lid, l in E['lugares'].items():
        d = l.get('dragao') if isinstance(l, dict) else None
        if isinstance(d, dict) and d.get('vila'): ef += nova(E, d['vila'], f"{d['nome'][0].upper() + d['nome'][1:]}, o dragão da serra, cobra de {E['lugares'][d['vila']]['nome']}: quem não paga, arde", 3, ('dragão',), ja=ef)
    piores = sorted((e for e in E['lugares'] if E['lugares'][e].get('tipo') == 'estrada'), key=lambda e: -E['lugares'][e].get('bando', 0))[:2]
    for e in piores:
        if E['lugares'][e].get('bando', 0) >= 4: ef += nova(E, E['lugares'][e]['ponta'][0], f"salteadores {estado.em(E, e)}: os mercadores andam em grupo", 2, ('estrada',), ja=ef)
    if ef: estado.aplica(E, 'gera', ef, texto='as notícias do Dia 1')
    return [f"As notícias do Dia 1: {len([x for x in ef if x[1] == 'noticias'])}."]


if __name__ == '__main__':
    import signal; hasattr(signal, 'SIGPIPE') and signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    a = sys.argv[1:]
    if not a or a[0] not in ('ver', 'todas'): print(__doc__); sys.exit()
    E = estado.carrega()
    if a[0] == 'ver':
        lid = a[1] if len(a) > 1 else (E['gente'][estado.eu(E)]['lugar'] if estado.eu(E) else None)
        if lid not in E['lugares']: sys.exit('diga o lugar: `noticias.py ver LUGAR`')
        for d, s, n in chegadas(E, lid): print(f"- Dia {d}: {diz(E, n, s)}")
    else:
        for nid, n in (E['mundo'].get('noticias') or {}).items(): print(f"- {nid} Dia {n['dia']} em {E['lugares'][n['onde']]['nome']}: {n['texto']} · chegou a {len(n['chegou'])} lugares")
