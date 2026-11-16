#!/usr/bin/env python3
"""noticias.py — que NOTÍCIAS chegam a Ireviel entre dois dias (lidas dos tick_N.txt).

Uso:  python3 noticias.py DIA_INICIAL DIA_FINAL
Lista cada notícia que o tick marcou para chegar nesse intervalo, com o dia do
tick que a gerou e o texto do evento. Serve para o Mestre não esquecer de
processar uma notícia (erro achado no 253: o monstro novo de Mordun, notícia
no 253, nunca foi gerado). Roda junto com o conferidor.
"""
import sys, re, glob, os

AQUI = os.path.dirname(os.path.abspath(__file__))

def main():
    if len(sys.argv) < 3:
        print(__doc__); return
    a, b = int(sys.argv[1]), int(sys.argv[2])
    saida = []
    for f in glob.glob(os.path.join(AQUI, 'tick_*.txt')):
        m = re.search(r'tick_(\d+)\.txt', f)
        if not m: continue
        dia = int(m.group(1))
        linhas = open(f, encoding='utf-8', errors='replace').read().splitlines()
        evento, onde = '', ''
        for l in linhas:
            s = l.strip()
            m1 = re.match(r'd20 \[\d+\] (.+)', s)
            if m1: evento = m1.group(1); onde = ''; continue
            m2 = re.match(r'ONDE: d\d+ \[\d+\] (.+)', s)
            if m2: onde = m2.group(1); continue
            m3 = re.match(r'A NOTÍCIA: \[\d+\] (?:em 1d\d+ \[(\d+)\] dias|(hoje))', s)
            if m3:
                d = dia if m3.group(2) else dia + int(m3.group(1))
                if a <= d <= b: saida.append((d, dia, f'{evento} — {onde}'))
                continue
            m4 = re.search(r'notícia d20 \[\d+\] chega (?:no dia (\d+)|(hoje))', s)
            if m4:
                d = dia if m4.group(2) else int(m4.group(1))
                if a <= d <= b:
                    txt = s.split(' · notícia')[0]
                    saida.append((d, dia, txt[:200]))
    for d, t, txt in sorted(saida):
        print(f'Dia {d} (do tick {t}): {txt}')
    if not saida: print('nenhuma notícia marcada nesse intervalo.')

if __name__ == '__main__':
    main()
