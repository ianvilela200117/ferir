#!/usr/bin/env python3
"""diretor.py — MOTOR 10, ETAPA FINAL: O DIRETOR. Só escolhe quais frentes podem entrar em cena no dia (até 3) e dois fatos do mundo que não tocam o personagem
(para a cena ter vida). NÃO GRAVA NADA: não toca em dado, relógio, estoque nem frente — o banco prova que o mundo sai idêntico com ele ligado e desligado.
Depois de uma queda (ferida grave, companheiro morto, a luta perdida), ele não empilha ameaça: prefere a ambição e o mistério; mas também não inventa alívio que não exista.

  python3 diretor.py pauta            a pauta de hoje (SÓ O MESTRE)
"""
import sys
import tabelas_mundo as M
import estado


def tem(E): return bool((E.get('mundo') or {}).get('meta'))


def caiu(E, pid, dias=3):
    """o personagem caiu há pouco? (ferida grave aberta nos últimos dias, ou o PV abaixo de um terço)"""
    p = E['gente'][pid]; hoje = E['relogio']['dia']
    return any(f.get('grave') and hoje - f.get('dia', 0) <= dias for f in p.get('feridas') or []) or p['pv'] < estado.pv_max(p) / 3


def pauta(E):
    """[(fid, por quê)] até 3: as frentes vivas perto do personagem, das que andaram há pouco e das mais adiantadas"""
    import regiao, frentes
    pid = estado.eu(E)
    if not pid or E['gente'][pid]['estado'] != 'vivo': return []
    perto = regiao.saltos(E, regiao_lugar(E, estado.onde(E, pid)), so_abertas=False); hoje = E['relogio']['dia']
    cand = []
    for fid, f in frentes.ativas(E).items():
        d = perto.get(f['onde'], 99)
        if d > 2: continue
        recente = f.get('ult') is not None and hoje - f['ult'] <= 7
        cand.append(((0 if recente else 1), d, -f['passo'], fid, f))
    if caiu(E, pid):
        leves = [c for c in cand if c[4]['tipo'] not in ('ameaça', 'calamidade', 'nêmesis')]
        if leves: cand = leves
    cand.sort()
    return [(fid, f"{f['nome']} (passo {f['passo']}, a {d} estrada(s) daqui" + (', andou nesta semana' if r == 0 else '') + ')') for r, d, _, fid, f in cand[:3]]


def regiao_lugar(E, lid):
    import noticias
    return noticias.origem(E, lid) or lid


def dois_fatos(E):
    """dois fatos do mundo, de longe, dos últimos dias, que não tocam o personagem (o acaso do dia escolhe; nada é gravado)"""
    pid = estado.eu(E); hoje = E['relogio']['dia']
    ns = [n for n in (E['mundo'].get('noticias') or {}).values() if hoje - n['dia'] <= 3 and pid not in n['texto'] and 'história' not in (n.get('tags') or [])]
    if not ns: return []
    r = estado.sorte(E, 'diretor|fatos')
    return [n['texto'] for n in r.sample(ns, min(2, len(ns)))]


def so_mestre(E):
    if not tem(E) or not estado.eu(E): return []
    L = [f"a pauta do diretor (o que pode entrar em cena hoje): " + ' · '.join(t for _, t in pauta(E))] if pauta(E) else []
    df = dois_fatos(E)
    if df: L.append('dois fatos que não tocam o personagem (para a cena): ' + ' · '.join(df))
    return L


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[:1] != ['pauta']: print(__doc__); sys.exit()
    print('\n'.join(so_mestre(estado.carrega())) or 'nada na pauta.')
