#!/usr/bin/env python3
"""reputacao.py — G21, A REPUTAÇÃO DA CASA (Dia 433, pedido do jogador): um número de −100 a +100 por CIDADE, por PODER
(Lendário, Doge, clã) e por GUILDA (G12). Fica em mundo_vivo.json ("reputacao").

Faixas (o que o número abre ou fecha):
  +75 ou mais  HONRADO: preço −20%; a cidade avisa do perigo; gente se oferece sem pedir
  +25 a +74    AMIGO: preço −10%; missões melhores; a porta abre
  −24 a +24    NEUTRO
  −25 a −74    DESCONFIADO: preço +20%; portas fechadas; ninguém conta nada
  −75 ou menos INIMIGO: ninguém vende; ameaça; espião
Guia de quanto muda: um favor grande ou uma vitória pela cidade +10 · uma promessa cumprida +5 · uma promessa quebrada −15 ·
passar por cima da lei da cidade −10 · gente da cidade morta pela casa −20 · uma obra pública na cidade +5.

Uso:
  python3 reputacao.py ver
  python3 reputacao.py muda "QUEM" +N|-N "motivo"
"""
import sys
from nucleo import carrega, grava, anota, dia_atual


def faixa(v):
    return 'HONRADO' if v >= 75 else 'amigo' if v >= 25 else 'neutro' if v > -25 else 'desconfiado' if v > -75 else 'INIMIGO'


def main():
    a = sys.argv[1:]
    M = carrega('mundo_vivo.json')
    R = M.setdefault('reputacao', {})
    if not a or a[0] == 'ver':
        print('A REPUTAÇÃO DA CASA (G21)')
        for k, v in sorted(R.items(), key=lambda x: -x[1]['valor']):
            print(f"  {v['valor']:+4d} {faixa(v['valor']):11s} {k}" + (f" · {v['log'][-1]}" if v.get('log') else ''))
        return
    if a[0] == 'muda' and len(a) >= 3:
        quem, n = a[1], int(a[2]); mot = a[3] if len(a) > 3 else ''
        v = R.setdefault(quem, {'valor': 0, 'log': []})
        antes = v['valor']; v['valor'] = max(-100, min(100, antes + n))
        v['log'] = (v.get('log', []) + [f"{dia_atual()}: {n:+d} ({mot})"])[-8:]
        grava('mundo_vivo.json', M)
        anota(f"- REPUTAÇÃO (G21) {quem}: {antes:+d} → {v['valor']:+d} ({faixa(v['valor'])}) · {mot}")
        print(f"{quem}: {antes:+d} → {v['valor']:+d} ({faixa(v['valor'])}) · {mot}")
        return
    print(__doc__)


if __name__ == '__main__':
    main()
