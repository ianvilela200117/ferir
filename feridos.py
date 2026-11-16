#!/usr/bin/env python3
"""feridos.py — FERIMENTO QUE DURA (MOTOR 6.3; regra nova, liga e desliga em motor.json: camadas.ferimentos).
Quem CAI numa luta (0 PV e sobrevive) ou RECUA ferido não volta inteiro no dia seguinte. O luta.py chama isto sozinho no fim
de uma luta de verdade. A tabela, d20 (+3 se caiu a 0 PV; −3 se há quem saiba Medicina por perto):
  até 8   LEVE: 1d3+1 dias; luta com −2 no ataque e na defesa
  9-15    SÉRIO: 1d6+6 dias de cama; não luta
  16-19   GRAVE: 2d6+10 dias; não luta; fica uma MARCA (d6: 1 manca · 2 mão fraca · 3 um olho pior · 4 cicatriz que todos veem · 5 dor que volta no frio · 6 medo do que o feriu)
  20+     PARA SEMPRE: 30 dias e perde algo de vez (o Mestre decide com o jogador)
Uso:
  python3 feridos.py ver                       quem está ferido e até quando
  python3 feridos.py rola NOME [caiu] [medicina] ["o que o feriu"]
  python3 feridos.py alta NOME                 curado antes da hora (magia, milagre)
  python3 feridos.py dia DIA                   dá alta a quem cumpriu os dias (o tick chama sozinho)
"""
import sys
from nucleo import d, carrega, grava, dia_atual, anota
ARQ = 'feridos.json'
MARCA = ['manca', 'mão fraca', 'um olho pior', 'cicatriz que todos veem', 'dor que volta no frio', 'medo do que o feriu']


def rola(nome, caiu=False, medicina=False, causa=''):
    F = carrega(ARQ, {'feridos': []}); dia = dia_atual()
    r = d(20); mod = (3 if caiu else 0) - (3 if medicina else 0); t = r + mod
    if t <= 8: dias = d(3) + 1; grau, efeito = 'LEVE', 'luta com −2 no ataque e na defesa'
    elif t <= 15: dias = d(6) + 6; grau, efeito = 'SÉRIO', 'de cama; não luta'
    elif t <= 19: dias = d(6) + d(6) + 10; grau, efeito = 'GRAVE', 'não luta · MARCA: ' + MARCA[d(6) - 1]
    else: dias = 30; grau, efeito = 'PARA SEMPRE', 'não luta; perde algo de vez (decidir com o jogador)'
    F['feridos'] = [x for x in F['feridos'] if x['nome'] != nome] + [{'nome': nome, 'grau': grau, 'efeito': efeito, 'desde': dia, 'ate': dia + dias, 'causa': causa}]
    grava(ARQ, F)
    txt = f"FERIMENTO de {nome}: d20 [{r}]{mod:+d} = {t} → {grau}: {efeito} · {dias} dias (até o Dia {dia + dias})" + (f' · {causa}' if causa else '')
    print('  ' + txt); anota('- ' + txt)
    return grau


def main():
    a = sys.argv[1:]
    F = carrega(ARQ, {'feridos': []})
    if not a or a[0] == 'ver':
        for x in F['feridos']: print(f"{x['nome']}: {x['grau']} ({x['efeito']}) até o Dia {x['ate']}" + (f" · {x['causa']}" if x.get('causa') else ''))
        if not F['feridos']: print('ninguém ferido.')
    elif a[0] == 'rola' and len(a) > 1:
        rola(a[1], 'caiu' in a, 'medicina' in a, next((x for x in a[2:] if x not in ('caiu', 'medicina')), ''))
    elif a[0] == 'alta' and len(a) > 1:
        F['feridos'] = [x for x in F['feridos'] if x['nome'].lower() != a[1].lower()]; grava(ARQ, F); print(f'{a[1]}: alta.')
    elif a[0] == 'dia' and len(a) > 1:
        dia = int(a[1]); fora = [x for x in F['feridos'] if x['ate'] <= dia]
        if fora:
            F['feridos'] = [x for x in F['feridos'] if x['ate'] > dia]; grava(ARQ, F)
            for x in fora: print(f"  ALTA: {x['nome']} está de pé de novo ({x['grau']}, ferido desde o {x['desde']})")
        for x in F['feridos']: print(f"  FERIDO: {x['nome']} ({x['grau']}: {x['efeito']}) até o Dia {x['ate']}")
    else: print(__doc__)


if __name__ == '__main__':
    main()
