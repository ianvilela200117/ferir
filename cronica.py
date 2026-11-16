#!/usr/bin/env python3
"""cronica.py — A CRÔNICA POR LUA (MOTOR 6.4): escreve cronica.md, o índice da campanha mês a mês do calendário.
Lê os Pendentes do estado_vivo.md (cada um começa pelo dia), agrupa pela lua e guarda a primeira frase de cada.
Serve para reler a campanha sem abrir o diário inteiro e para achar em que dia algo aconteceu.
Uso: python3 cronica.py [quieto]
"""
import re, sys
from nucleo import ler, P, calendario, dia_atual, LUAS


def main():
    est = ler('estado_vivo.md'); hoje = dia_atual()
    pend = est.split('## Pendentes que Ferir conhece', 1)
    bul = [b[2:] for b in (pend[1] if len(pend) > 1 else '').split('\n') if b.startswith('- ')]
    itens = []
    for b in bul:
        m = re.search(r'(?<![\d.])(19\d|[2-9]\d\d)(?![\d.])', b[:140])
        if not m or int(m.group(1)) > hoje + 1: continue
        txt = re.sub(r'\*\*', '', b); txt = re.sub(r'\s*\(OCULTO[^)]*\)', '', txt)
        corte = txt[:420]; corte = corte if len(txt) <= 420 else corte.rsplit(' ', 1)[0] + '…'
        itens.append((int(m.group(1)), corte))
    itens.sort()
    out = ['# A CRÔNICA DO REINO, lua a lua', '', f'(gerada por cronica.py no Dia {hoje}; a história inteira está no diário)', '']
    chave = None
    for dia, txt in itens:
        c = calendario(dia); k = (c['ano'], c['lua'])
        if k != chave:
            chave = k; out += ['', f"## {'Os Dias Mudos' if c['mudo'] else 'Lua ' + LUAS[c['lua'] - 1]} de {c['ano']} d.S. ({c['estacao']})", '']
        out.append(f'- **Dia {dia}:** {txt}')
    open(P('cronica.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    if 'quieto' not in sys.argv: print(f'cronica.md: {len(itens)} entradas, de {itens[0][0] if itens else "?"} a {itens[-1][0] if itens else "?"}')


if __name__ == '__main__':
    main()
