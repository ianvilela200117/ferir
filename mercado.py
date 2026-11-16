#!/usr/bin/env python3
"""mercado.py — O MERCADO VIVO (MOTOR 6.3; regra nova, desliga em motor.json: camadas.mercado): mercado.json.
Cada cidade do reino tem o ÍNDICE DE PREÇO de cinco coisas (100 = o preço normal do Livro; 150 = uma vez e meia).
Por semana cada índice volta um quarto do caminho para 100, balança um pouco no dado (d11 − 6, vezes 2) e leva os choques do mundo:
  Comida 0-1 na cidade: grão +40 · Comida 4: grão −5 · Comércio 0-1: tudo +15 · Comércio 4: tudo −3
  rio SECO ou em CHEIA: sal, ferro e carvão +15 em Ireviel e no Porto (a barca não passa)
  3 dias ou mais de calor forte na semana: grão +10, peixe +5 · 2 dias ou mais de tempestade: peixe +20, sal +10
EFEITO: grão a 170 ou mais numa cidade = PÃO CARO: Ordem −1 na semana seguinte (modificador com prazo no reino.json).
Uso: python3 mercado.py ver   |   python3 mercado.py semana DIA (o tick semanal chama)   |   python3 mercado.py choque CIDADE COISA +N "motivo"
"""
import sys
from nucleo import d, carrega, grava, anota, acha_nome
ARQ = 'mercado.json'
COISAS = ['grão', 'sal', 'ferro', 'carvão', 'peixe']
CID = {'Ireviel': 'Ireviel', 'o Porto de Marasar': 'o Porto de Marasar', 'Levis': 'Levis', 'Farenta': 'Farenta'}


def load():
    M = carrega(ARQ, {})
    if not M:
        M = {'cidades': {c: {k: 100 for k in COISAS} for c in CID}, 'log': []}
    return M


def ver(M):
    print('MERCADO (índice: 100 = preço normal)')
    for c, v in M['cidades'].items():
        print(f"  {c}: " + ' · '.join(f"{k} {v[k]}" + (' ▲' if v[k] >= 130 else ' ▼' if v[k] <= 80 else '') for k in COISAS))


def semana(M, dia):
    R = carrega('reino.json'); C = carrega('clima.json', {})
    ult = [h for h in C.get('historia', []) if dia - 7 < h['dia'] <= dia]
    agua = C.get('agua', 50)
    print('  O MERCADO DA SEMANA (índice de preço; 100 = normal):')
    linhas = 0
    for c in R.get('cidades', []):
        nome = next((x for x in CID if x.split()[-1] in c['nome']), None)
        if not nome: continue
        p = c['pilares']; v = M['cidades'].setdefault(nome, {k: 100 for k in COISAS})
        dias = [h['tempo'].get(nome, '') for h in ult]
        calor = sum(1 for x in dias if x == 'calor forte'); temp = sum(1 for x in dias if x == 'tempestade')
        mud = []
        for k in COISAS:
            antes = v[k]
            n = antes + (100 - antes) * 0.25 + (d(11) - 6) * 2
            if k == 'grão': n += (40 if p['Comida'] <= 1 else -5 if p['Comida'] == 4 else 0) + (10 if calor >= 3 else 0)
            n += 15 if p['Comércio'] <= 1 else -3 if p['Comércio'] == 4 else 0
            if k in ('sal', 'ferro', 'carvão') and nome in ('Ireviel', 'o Porto de Marasar') and (agua < 15 or agua >= 85): n += 15
            if k == 'peixe': n += (5 if calor >= 3 else 0) + (20 if temp >= 2 else 0)
            if k == 'sal' and temp >= 2: n += 10
            v[k] = int(max(40, min(400, round(n))))
            if abs(v[k] - antes) >= 8 or v[k] >= 130 or v[k] <= 80: mud.append(f"{k} {antes}→{v[k]}")
        if mud: print(f"   {nome}: " + ' · '.join(mud)); linhas += 1
        if v['grão'] >= 170:
            c.setdefault('mods', {}).setdefault('Ordem', []).append([-1, f"pão caro: grão a {v['grão']} (até o {dia + 6})"])
            print(f"   {nome}: PÃO CARO (grão a {v['grão']}): Ordem −1 na semana")
    if not linhas: print('   preços parados.')
    grava('reino.json', R); grava(ARQ, M)


def main():
    a = sys.argv[1:]; M = load()
    if not a or a[0] == 'ver': ver(M); grava(ARQ, M)
    elif a[0] == 'semana' and len(a) > 1: semana(M, int(a[1]))
    elif a[0] == 'choque' and len(a) > 3:
        c, _ = acha_nome(a[1], M['cidades']); k, _ = acha_nome(a[2], COISAS)
        if not c or not k: sys.exit('cidade ou coisa não achada. ' + __doc__)
        antes = M['cidades'][c][k]; M['cidades'][c][k] = max(40, min(400, antes + int(a[3].replace('+', '')))); grava(ARQ, M)
        txt = f"MERCADO: {k} em {c} {antes}→{M['cidades'][c][k]}" + (f' ({a[4]})' if len(a) > 4 else ''); print(txt); anota('- ' + txt)
    else: print(__doc__)


if __name__ == '__main__':
    main()
