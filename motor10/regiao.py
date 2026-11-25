#!/usr/bin/env python3
"""regiao.py — MOTOR 10, ETAPA FINAL: A REGIÃO. As estradas, o povo em número (come, passa fome, sai, engrossa o bando), o comércio entre lugares,
e O RELÓGIO QUE ANDA O MUNDO SEM O PERSONAGEM (`anda`). Os números: tabelas_regiao.py; o contrato: projeto/ETAPA_FINAL.md, seções 2 e 5.

  python3 regiao.py ver                      os lugares de povo, o povo, a comida em dias, as estradas (o que se sabe)
  python3 regiao.py estradas [LUGAR]         as estradas de um lugar (do personagem, sem LUGAR): para onde, quantos blocos, o perigo que o povo conta
  python3 regiao.py anda N                   SÓ SEM PERSONAGEM (o mundo de prova, a criação): anda N dias de mundo, com a virada inteira

O MUNDO SEM REGIÃO (a vila de teste, o ensaio) não tem nada disto: a virada não faz nada, a mesa não muda.
"""
import heapq, math, sys
import tabelas_mundo as M
import tabelas_regiao as R
import tabelas_mercado as C
import estado


def tem(E): return bool((E.get('mundo') or {}).get('meta'))         # o mundo tem região? (o save antigo e a vila de teste: não)
def povoado(E, lid): return isinstance(E['lugares'].get(lid), dict) and E['lugares'][lid].get('tipo') in M.POVOADOS
def povoados(E): return [k for k, l in E['lugares'].items() if isinstance(l, dict) and l.get('tipo') in M.POVOADOS]
def aberta(E, eid): return not (E['lugares'][eid].get('fechada'))


def estradas(E, lid, abertas=False):
    """as estradas que saem de um lugar: [(estrada, o lugar do outro lado)]"""
    out = []
    for k, l in E['lugares'].items():
        if isinstance(l, dict) and l.get('tipo') == 'estrada' and lid in (l.get('ponta') or []) and (not abertas or not l.get('fechada')):
            out.append((k, l['ponta'][1] if l['ponta'][0] == lid else l['ponta'][0]))
    return out


_CACHE = {}
def grafo(E):
    """{lugar: [(outro, estrada, blocos, aberta)]} (refeito quando as estradas mudam)"""
    chave = tuple(sorted((k, tuple(l['ponta']), l['longe'], bool(l.get('fechada'))) for k, l in E['lugares'].items() if isinstance(l, dict) and l.get('tipo') == 'estrada'))
    if _CACHE.get('k') != chave:
        G = {}
        for k, l in E['lugares'].items():
            if isinstance(l, dict) and l.get('tipo') == 'estrada':
                a, b = l['ponta']; G.setdefault(a, []).append((b, k, l['longe'], not l.get('fechada'))); G.setdefault(b, []).append((a, k, l['longe'], not l.get('fechada')))
        _CACHE.clear(); _CACHE.update(k=chave, G=G)
    return _CACHE['G']


def caminho(E, a, b):
    """o caminho mais curto (em blocos) de a até b pelas estradas abertas: [(estrada, próximo lugar)], ou None"""
    G = grafo(E); dist = {a: 0}; ant = {}; fila = [(0, a)]
    while fila:
        d, x = heapq.heappop(fila)
        if x == b: break
        if d > dist.get(x, 1e9): continue
        for y, e, bl, ab in G.get(x, []):
            if ab and d + bl < dist.get(y, 1e9): dist[y] = d + bl; ant[y] = (x, e); heapq.heappush(fila, (d + bl, y))
    if b not in dist: return None
    out = []; x = b
    while x != a: px, e = ant[x]; out.append((e, x)); x = px
    return list(reversed(out))


def saltos(E, origem, so_abertas=True):
    """quantas estradas de um lugar a cada outro (a notícia anda uma por dia): {lugar: saltos}"""
    G = grafo(E); d = {origem: 0}; fila = [origem]
    for x in fila:
        for y, e, bl, ab in G.get(x, []):
            if (ab or not so_abertas) and y not in d: d[y] = d[x] + 1; fila.append(y)
    return d


def dias_de_comida(E, lid):
    l = E['lugares'][lid]; pop = l.get('pop') or 0
    return (l['estoque'].get('comida', 0) / (pop * C.consumo('comida'))) if pop else 999


def perigo_diz(E, eid):
    l = E['lugares'][eid]; b = l.get('bando', 0)
    base = {1: 'tranquila', 2: 'de assalto às vezes', 3: 'perigosa'}.get(l.get('perigo', 1), '?')
    return base + (', e contam que há salteadores nela' if b >= 6 else '')


# ---------- a virada da região ----------
def virada(E):
    if not tem(E): return
    _fome(E); _comercio(E); _patrulha(E)


def _escala_produz(l, fator):
    return [[k, round(v * fator, 4)] for k, v in (l.get('produz') or {}).items() if isinstance(v, (int, float)) and not isinstance(v, bool)]


def _fome(E):
    """o povo que não tem o que comer morre e sai; o celeiro baixo empurra gente para o vizinho mais farto e para a estrada (o bando)"""
    for lid in povoados(E):
        l = E['lugares'][lid]; pop = l.get('pop') or 0
        if pop < 2: continue
        dias = dias_de_comida(E, lid)
        if dias >= R.FOME_DIAS: continue
        rs = estado.sorte(E, f'regiao|fome|{lid}'); ef = []; txt = []
        mortos = int(round(pop * R.FOME_MORRE)) if l['estoque'].get('comida', 0) < 1 else 0
        viz = [(o, e) for e, o in estradas(E, lid, abertas=True) if povoado(E, o)]
        sai = max(1 if rs.random() < pop * R.MIGRA else 0, int(pop * R.MIGRA * (2 if mortos else 1)))
        if viz and sai:
            melhor = max(viz, key=lambda x: dias_de_comida(E, x[0]))[0]
            if dias_de_comida(E, melhor) > dias:
                lo = E['lugares'][melhor]; po = lo.get('pop') or 0
                ef += [['lugar', lid, 'pop', 'soma', -sai], ['lugar', melhor, 'pop', 'soma', sai]]
                ef += [['lugar', melhor, 'produz.' + k, 'poe', v] for k, v in _escala_produz(lo, (po + sai) / max(1, po))]
                txt.append(f"{sai} {'pessoa sai' if sai == 1 else 'pessoas saem'} {estado.de(E, lid)} para {E['lugares'][melhor]['nome']}")
            else: sai = 0
        else: sai = 0
        if mortos: ef.append(['lugar', lid, 'pop', 'soma', -mortos]); txt.append(f"a fome leva {mortos} {estado.em(E, lid)}")
        novo = pop - sai - mortos
        for e, o in estradas(E, lid):
            if rs.random() < R.BANDO_FOME and E['lugares'][e].get('bando', 0) < R.BANDO_TETO and novo > 2:
                ef += [['lugar', e, 'bando', 'soma', 1], ['lugar', lid, 'pop', 'soma', -1]]; novo -= 1; txt.append(f"um faminto vira salteador {estado.em(E, e)}")
        if novo != pop and novo > 0: ef += [['lugar', lid, 'produz.' + k, 'poe', v] for k, v in _escala_produz(l, novo / pop)]
        if ef: estado.aplica(E, 'regiao', ef, onde=lid, texto='; '.join(txt) or 'o celeiro baixo')
        try: import frentes
        except ModuleNotFoundError: frentes = None
        if frentes and hasattr(frentes, 'limiar_fome'): frentes.limiar_fome(E, lid, dias)


def _comercio(E):
    """os mercadores (em número) levam o que sobra para onde falta, pelas estradas abertas e sem bando grosso: a prata vai de quem compra para quem vende"""
    import mercado
    K = R.COMERCIO; feitos = set()
    for eid, l in list(E['lugares'].items()):
        if not isinstance(l, dict) or l.get('tipo') != 'estrada' or l.get('fechada') or l.get('bando', 0) >= 8: continue
        a, b = l['ponta']
        if not (povoado(E, a) and povoado(E, b)): continue
        ef = []; txt = []; cx = {a: E['lugares'][a]['estoque'].get('prata', 0), b: E['lugares'][b]['estoque'].get('prata', 0)}      # a prata de cada ponta, com o que este evento já moveu
        for bem in K['bens']:
            pa, pb = mercado.preco(E, a, bem), mercado.preco(E, b, bem)
            if not pa or not pb: continue
            de, para = (a, b) if pb > pa * K['razao'] else (b, a) if pa > pb * K['razao'] else (None, None)
            if not de or (de, para, bem) in feitos: continue
            tem = E['lugares'][de]['estoque'].get(bem, 0); q = int(min(tem * K['lote'], mercado.alvo(E, para, bem) * K['teto']))
            if q < 1: continue
            preco = (mercado.preco(E, de, bem) + mercado.preco(E, para, bem)) / 2; v = int(q * preco)
            if v < 1 or cx[para] < v: continue
            cx[para] -= v; cx[de] += v
            ef += [['estoque', de, bem, 'soma', -q], ['estoque', para, bem, 'soma', q], ['estoque', para, 'prata', 'soma', -v], ['estoque', de, 'prata', 'soma', v]]
            feitos.add((de, para, bem)); txt.append(f"{q} de {estado.nome_bem(bem)} {estado.de(E, de)} para {E['lugares'][para]['nome']}")
        if ef: estado.aplica(E, 'regiao', ef, onde=eid, texto='o comércio: ' + '; '.join(txt))


def _patrulha(E):
    """a guarda (em número) de cada lugar patrulha as estradas dele: às vezes tira um salteador"""
    ef = []
    for lid in povoados(E):
        g = E['lugares'][lid].get('guarda') or 0
        if not g: continue
        rs = estado.sorte(E, f'regiao|patrulha|{lid}')
        for e, o in estradas(E, lid):
            if E['lugares'][e].get('bando', 0) > 0 and rs.random() < g * R.GUARDA_PATRULHA / max(1, len(estradas(E, lid))) and not any(x[1] == e for x in ef):
                ef.append(['lugar', e, 'bando', 'soma', -1])
    if ef: estado.aplica(E, 'regiao', ef, texto=f"a guarda tira {estado.tantos(len(ef), 'salteador', 'salteadores')} das estradas")


# ---------- o mundo sem o personagem ----------
def anda(E, dias=1, depois=None):
    """anda `dias` dias inteiros de mundo (a virada de todos os módulos, na ordem), SEM personagem vivo. `depois(E, dia)` roda no fim de cada dia (o banco olha)."""
    import ato
    eu = estado.eu(E)
    if eu and E['gente'][eu]['estado'] == 'vivo': sys.exit('há um personagem vivo: o mundo anda pelos atos dele (ato.py), não pelo `anda`')
    estado.sem_luta(E)
    for _ in range(dias):
        falta = M.BLOCOS_DIA - E['relogio']['bloco']
        estado.aplica(E, 'tempo', [['relogio', falta]], texto='o dia vira')
        ato._mundo_vira(E)
        if depois: depois(E, E['relogio']['dia'])


# ---------- a mesa ----------
def mesa(E):
    if not tem(E): return []
    pid = estado.eu(E)
    if not pid or E['gente'][pid]['estado'] != 'vivo': return []
    lid = E['gente'][pid]['lugar']
    if estado.fora(E, pid) or not povoado(E, lid): return []
    sabe = set(((E['gente'][pid].get('marca') or {}).get('andou') or []))
    L = ['**Estradas daqui** (`viagem.py ir DESTINO`):']
    for e, o in sorted(estradas(E, lid), key=lambda x: E['lugares'][x[0]]['longe']):
        l = E['lugares'][e]
        L.append(f"- para {E['lugares'][o]['nome']}: {estado.tantos(l['longe'], 'bloco')}; {perigo_diz(E, e)}" + (' (você já andou nela)' if e in sabe else '')
                 + (f" · FECHADA ({l['fechada'].get('por')})" if l.get('fechada') else ''))
    return L


def so_mestre(E):
    if not tem(E): return []
    pid = estado.eu(E)
    if not pid: return []
    lid = E['gente'][pid]['lugar']
    b = [f"{E['lugares'][e]['nome']}: {E['lugares'][e].get('bando', 0)}" for e, o in estradas(E, lid)]
    fome = [f"{E['lugares'][x]['nome']} ({dias_de_comida(E, x):.0f} dias)" for x in povoados(E) if dias_de_comida(E, x) < R.FOME_DIAS]
    return ([f"os salteadores nas estradas daqui: {'; '.join(b)}"] if b else []) + ([f"celeiro baixo: {', '.join(fome)}"] if fome else [])


def ver(E):
    if not tem(E): return 'este mundo não tem região (é a vila de teste, ou um save antigo).'
    W = E['mundo']; L = [f"A REGIÃO DE {W['meta']['nome'].upper()} · ano {W['meta']['ano0']} · {estado.quando(E)}"]
    for lid in sorted(povoados(E), key=lambda k: -(E['lugares'][k].get('pop') or 0)):
        l = E['lugares'][lid]
        L.append(f"- {l['nome']} [{lid}] · {l['tipo']} · {int(l.get('pop') or 0)} de povo · comida para {dias_de_comida(E, lid):.0f} dias · estradas: "
                 + ', '.join(f"{E['lugares'][o]['nome']} ({E['lugares'][e]['longe']})" for e, o in estradas(E, lid)))
    return '\n'.join(L)


if __name__ == '__main__':
    import signal; hasattr(signal, 'SIGPIPE') and signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    a = sys.argv[1:]
    if not a or a[0] not in ('ver', 'estradas', 'anda'): print(__doc__); sys.exit()
    E = estado.carrega()
    if a[0] == 'ver': print(ver(E))
    elif a[0] == 'estradas':
        lid = a[1] if len(a) > 1 else (E['gente'][estado.eu(E)]['lugar'] if estado.eu(E) else None)
        if lid not in E['lugares']: sys.exit('diga o lugar: `regiao.py estradas LUGAR`')
        for e, o in estradas(E, lid): print(f"- {E['lugares'][e]['nome']}: para {E['lugares'][o]['nome']}, {estado.tantos(E['lugares'][e]['longe'], 'bloco')}; {perigo_diz(E, e)}")
    else:
        if len(a) != 2 or not a[1].isdigit(): sys.exit('diga quantos dias: `regiao.py anda 7`')
        anda(E, int(a[1])); estado.grava(E); print(f"o mundo andou {a[1]} dias: {estado.quando(E)}")
