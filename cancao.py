#!/usr/bin/env python3
"""cancao.py — MOTOR 9 (G28): CANÇÕES DE FEITO (Livro Nove 11).

Um feito grande, cantado: d20 + o PRESTÍGIO do reino (é a Fama do rei, 0 a 10) (+5 se quem compõe é Cantor de Feitos).
  até 5 não pega · 6-15 pega na região (reputação +5 nas cidades dela) · 16-19 CORRE O MUNDO (+1 de prestígio e
  +1 permanente num atributo, entre dois que o Mestre oferece; anda 1 no relógio de um rival) · 20+ tudo isso e um título (G22).
Uma canção por lua (30 dias). O contratado custa 500.

Uso:
  python3 cancao.py ver
  python3 cancao.py compoe "O FEITO" [cantor="Nome"] [mestre] [contratado]     mestre: é Cantor de Feitos (+5); contratado: −500 do cofre
"""
import subprocess, sys
from nucleo import d, carrega, grava, anota, dia_atual, P

ARQ = 'cancoes.json'


def main():
    a = sys.argv[1:]; S = carrega(ARQ, {'cancoes': []}); C = S['cancoes']
    if not a or a[0] == 'ver':
        if not a: print(__doc__)
        print(f'CANÇÕES DE FEITO (G28): {len(C)}')
        for c in C: print(f"  Dia {c['dia']}: {c['feito']} · d20 [{c['dado']}] + {c['bonus']} = {c['total']} → {c['resultado']}")
        return
    if a[0] == 'compoe' and len(a) >= 2:
        dia = dia_atual()
        if C and dia - C[-1]['dia'] < 30: sys.exit(f"uma canção por lua: a última foi no Dia {C[-1]['dia']}; a próxima só no {C[-1]['dia'] + 30}.")
        prest = carrega('reino.json')['reino'].get('prestigio', 0); bonus = prest + (5 if 'mestre' in a else 0)
        if 'contratado' in a: subprocess.run([sys.executable, P('ficha.py'), 'cofre', '-500', f'{dia}: o cantor contratado ({a[1][:40]})'], capture_output=True)
        r = d(20); t = r + bonus
        res = 'não pega' if t <= 5 else 'pega na REGIÃO: reputação +5 nas cidades dela' if t <= 15 else 'CORRE O MUNDO: +1 de prestígio, +1 permanente num atributo (entre dois oferecidos) e 1 no relógio de um rival' + (' · E UM TÍTULO com efeito (G22)' if t >= 20 else '')
        cantor = next((x[7:] for x in a if x.startswith('cantor=')), 'um cantor')
        C.append({'dia': dia, 'feito': a[1], 'cantor': cantor, 'dado': r, 'bonus': bonus, 'total': t, 'resultado': res}); grava(ARQ, S)
        if t >= 16: subprocess.run([sys.executable, P('reino.py'), 'valor', 'prestigio', '1', f'a canção do feito: {a[1][:50]}'], capture_output=True)
        txt = f"CANÇÃO DE FEITO (G28): \"{a[1]}\", por {cantor}: d20 [{r}] + {bonus} (prestígio {prest}{', Cantor de Feitos +5' if 'mestre' in a else ''}) = {t} → {res}"
        anota('- ' + txt); print(txt); return
    sys.exit(__doc__)


if __name__ == '__main__':
    main()
