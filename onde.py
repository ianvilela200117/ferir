#!/usr/bin/env python3
"""onde.py — ONDE ESTÁ CADA UM (MOTOR 6.4): onde.json. Quem não está na lista está em Ireviel.
O viagem.py com leva=Nome,Nome já muda o lugar de quem viaja. O npc.py cena mostra onde a pessoa está, para o Mestre
não pôr em cena quem saiu da cidade.
Uso:
  python3 onde.py ver [LUGAR]                 quem está fora de Ireviel (ou quem está num lugar)
  python3 onde.py poe "NOME[,NOME]" LUGAR ["motivo"]
  python3 onde.py viaja "NOME[,NOME]" DESTINO CHEGA_DIA    em viagem; no dia da chegada passa a estar lá
  python3 onde.py volta "NOME[,NOME]"         está em Ireviel de novo (sai da lista)
"""
import sys
from nucleo import carrega, grava, dia_atual
ARQ = 'onde.json'


def lugar_de(nome, O=None, dia=None):
    O = O if O is not None else carrega(ARQ, {}); dia = dia or dia_atual(); x = O.get(nome)
    if not x: return 'Ireviel'
    if x['lugar'].lower() == 'ireviel' and (not x.get('chega') or x['chega'] <= dia): return 'Ireviel'
    if x.get('chega') and x['chega'] > dia: return f"em viagem para {x['lugar']} (chega no Dia {x['chega']})"
    return x['lugar']


def main():
    a = sys.argv[1:]; O = carrega(ARQ, {}); dia = dia_atual()
    if not a or a[0] == 'ver':
        filtro = a[1].lower() if len(a) > 1 else None
        for n in sorted(O):
            l = lugar_de(n, O, dia)
            if l == 'Ireviel' and not filtro: continue
            if not filtro or filtro in l.lower(): print(f"{n}: {l}" + (f" · {O[n]['motivo']}" if O[n].get('motivo') else ''))
        if not O: print('todos em Ireviel.')
        return
    nomes = [x.strip() for x in a[1].split(',') if x.strip()] if len(a) > 1 else []
    if a[0] == 'poe' and len(a) > 2:
        for n in nomes: O[n] = {'lugar': a[2], 'desde': dia, 'motivo': a[3] if len(a) > 3 else ''}
    elif a[0] == 'viaja' and len(a) > 3:
        for n in nomes: O[n] = {'lugar': a[2], 'chega': int(a[3]), 'desde': dia, 'motivo': ''}
    elif a[0] == 'volta':
        for n in nomes: O.pop(n, None)
    else: print(__doc__); return
    O = {k: v for k, v in O.items() if v['lugar'].lower() != 'ireviel' or (v.get('chega') and v['chega'] > dia)}
    grava(ARQ, O)
    for n in nomes: print(f'{n}: {lugar_de(n, O, dia)}')


if __name__ == '__main__':
    main()
