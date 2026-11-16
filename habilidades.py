#!/usr/bin/env python3
"""habilidades.py — MOTOR 7: A FICHA DE HABILIDADES DO FERIR (grau, uso, cargas, títulos e talentos).

Cada habilidade tem GRAU e sobe PELO USO, como no Satisfy: usar em cena conta; chegar à marca sobe o grau.
  grau 1 Iniciante (0 usos) · 2 Aprendiz (10) · 3 Adepto (30) · 4 Perito (80) · 5 Mestre (200) · 6 Grão-Mestre (500)
  Regra proposta (o jogador aprova): cada grau acima do 1 dá +1 no teste da PRÓPRIA habilidade. Nada mais muda sozinho.

Uso:
  python3 habilidades.py ver
  python3 habilidades.py mao                     G24: o que o rei pode usar AGORA (carga e custo): a linha 🛠️ do turno
  python3 habilidades.py add "Nome" Ativa|Passiva|Reação|Postura|Magia "efeito" [grau=N] [usos=N] [cargas=N] [origem="classe/talento/peça"]
  python3 habilidades.py usa "Nome" [N]          conta N usos (padrão 1); avisa e anota quando sobe de grau
  python3 habilidades.py carga "Nome" -1|+1|cheio
  python3 habilidades.py titulo "Nome" "efeito" "como ganhou"
  python3 habilidades.py talento "Nome" "efeito"
"""
import sys
from nucleo import carrega, grava, anota, dia_atual, sem_acento

ARQ = 'habilidades.json'
GRAUS = ['Iniciante', 'Aprendiz', 'Adepto', 'Perito', 'Mestre', 'Grão-Mestre']
MARCAS = [0, 10, 30, 80, 200, 500]


def grau_por_usos(u):
    return max(i + 1 for i, m in enumerate(MARCAS) if u >= m)


def acha(H, nome):
    alvo = sem_acento(nome).lower()
    c = [k for k in H if sem_acento(k).lower() == alvo] or [k for k in H if alvo in sem_acento(k).lower()]
    if len(c) == 1: return c[0]
    sys.exit(f'habilidade não achada (ou ambígua): "{nome}" · {", ".join(c) or "nenhuma"}')


def opt(a, chave, padrao=None):
    return next((x[len(chave) + 1:] for x in a if x.startswith(chave + '=')), padrao)


def main():
    a = sys.argv[1:]
    S = carrega(ARQ, {'habilidades': {}, 'titulos': [], 'talentos': []})
    H = S['habilidades']
    if not a or a[0] == 'ver':
        if not a: print(__doc__)
        print(f'HABILIDADES DO FERIR ({len(H)})')
        for k, h in sorted(H.items(), key=lambda kv: (kv[1]['tipo'], kv[0])):
            g = h['grau']; prox = MARCAS[g] if g < 6 else None
            cg = f' · cargas {h["cargas"]["atual"]}/{h["cargas"]["max"]}' if h.get('cargas') else ''
            print(f'  [{h["tipo"]}] {k} · grau {g} {GRAUS[g - 1]} (+{g - 1}) · usos {h["usos"]}' + (f' de {prox}' if prox else '') + cg + f' · {h["efeito"]}' + (f' ({h["origem"]})' if h.get('origem') else ''))
        if S.get('pericias'): print('PERÍCIAS: ' + ' · '.join(f'{k} {v}' for k, v in S['pericias'].items()))
        if S['titulos']: print('TÍTULOS'); [print(f'  {t["nome"]}: {t["efeito"]} · {t["como"]} (Dia {t["dia"]})') for t in S['titulos']]
        if S['talentos']: print('TALENTOS'); [print(f'  {t["nome"]}: {t["efeito"]}') for t in S['talentos']]
        return
    if a[0] == 'mao':   # MOTOR 9 (437, G24): o que o rei pode usar AGORA, com a carga e o custo (a fonte da linha 🛠️ HABILIDADES À MÃO)
        F = carrega('ficha.json', {})
        pv, mana, fo, rv = F.get('pv', [0, 0]), F.get('mana', [0, 0]), F.get('fortuna', [0, 0]), F.get('reves', [0, 0])
        print(f'HABILIDADES À MÃO (G24) · PV {pv[0]}/{pv[1]} · Mana {mana[0]}/{mana[1]} · Fortuna {fo[0]}/{fo[1]} · Revés {rv[0]}/{rv[1]}')
        for tipo in ('Magia', 'Ativa', 'Reação', 'Postura'):
            for k, h in sorted(H.items()):
                if h['tipo'] != tipo: continue
                cg = h.get('cargas'); sem = cg and cg['atual'] <= 0
                print(f"  {'✗' if sem else '•'} [{tipo}] {k}" + (f" ({cg['atual']}/{cg['max']})" if cg else '') + f" · {h['efeito']}")
        if S['talentos']: print('  TALENTOS que se usam: ' + ' · '.join(t_['nome'] for t_ in S['talentos'] if any(x in t_['efeito'] for x in ('1x', 'por dia', 'por sessão', 'por cena', 'por mês', 'por obra'))))
        return
    c = a[0]
    if c == 'add' and len(a) >= 4:
        usos = int(opt(a, 'usos', 0)); g = int(opt(a, 'grau', 0)) or grau_por_usos(usos)
        usos = max(usos, MARCAS[g - 1]); cg = opt(a, 'cargas')
        H[a[1]] = {'tipo': a[2], 'efeito': a[3], 'grau': g, 'usos': usos, 'desde': dia_atual()}
        if cg: H[a[1]]['cargas'] = {'atual': int(cg), 'max': int(cg)}
        if opt(a, 'origem'): H[a[1]]['origem'] = opt(a, 'origem')
        grava(ARQ, S); print(f'{a[1]}: grau {g} {GRAUS[g - 1]}, usos {usos}')
    elif c == 'usa' and len(a) >= 2:
        k = acha(H, a[1]); n = int(a[2]) if len(a) > 2 else 1; h = H[k]
        h['usos'] += n; novo = grau_por_usos(h['usos'])
        if novo > h['grau']:
            anota(f'HABILIDADE SOBE DE GRAU: {k} {GRAUS[h["grau"] - 1]} → {GRAUS[novo - 1]} (usos {h["usos"]})')
            print(f'★ {k} SOBE: {GRAUS[h["grau"] - 1]} → {GRAUS[novo - 1]} (+{novo - 1} no teste dela)'); h['grau'] = novo
        else:
            print(f'{k}: usos {h["usos"]}' + (f' de {MARCAS[h["grau"]]}' if h['grau'] < 6 else ''))
        grava(ARQ, S)
    elif c == 'carga' and len(a) >= 3:
        k = acha(H, a[1]); cg = H[k].get('cargas') or sys.exit('essa habilidade não tem cargas')
        cg['atual'] = cg['max'] if a[2] == 'cheio' else max(0, min(cg['max'], cg['atual'] + int(a[2].replace('−', '-'))))
        grava(ARQ, S); print(f'{k}: cargas {cg["atual"]}/{cg["max"]}')
    elif c == 'titulo' and len(a) >= 4:
        S['titulos'].append({'nome': a[1], 'efeito': a[2], 'como': a[3], 'dia': dia_atual()}); grava(ARQ, S)
        anota(f'TÍTULO: {a[1]} ({a[2]}) · {a[3]}'); print(f'título gravado: {a[1]}')
    elif c == 'pericia' and len(a) >= 3:   # python3 habilidades.py pericia "Forja" "LENDÁRIO +8"
        S.setdefault('pericias', {})[a[1]] = a[2]; grava(ARQ, S); print(f'perícia gravada: {a[1]} {a[2]}')
    elif c == 'talento' and len(a) >= 3:
        S['talentos'].append({'nome': a[1], 'efeito': a[2]}); grava(ARQ, S); print(f'talento gravado: {a[1]}')
    else: print(__doc__)


if __name__ == '__main__':
    main()
