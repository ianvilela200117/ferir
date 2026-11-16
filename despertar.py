#!/usr/bin/env python3
"""despertar.py — MOTOR 9 (G26): o DESPERTAR de quem passou dos níveis 100, 200 e 300 (um Dom por marco).

O rei escolhe o dele (o jogador). Os outros recebem no dado (d12), UMA vez, anotado no envelope:
à vista para os heróis da casa (os que têm ficha de combate), OCULTO para o resto do mundo.
Sair o mesmo Dom duas vezes é o SEGUNDO GRAU dele (o número dobra; o preço também).
Os Dons que pesam na luta vão sozinhos para a ficha de combate (o luta.py roda):
  Segundo Coração → segundo_coracao · Voz de Mando → voz_mando · Pele do Mundo → rd_ess {Essência: 5} · Passo Certo → ini +2

Uso:
  python3 despertar.py ver            quem tem Dom (o que a casa sabe; com "tudo", também os ocultos)
  python3 despertar.py rola           rola o que falta para todos (npcs.json e os grandes do mundo_vivo.json)
"""
import sys
from nucleo import d, carrega, grava, anota

DONS = ['Segundo Coração', 'Mão do Mundo', 'Olho Aberto', 'Sangue Grosso', 'Voz de Mando', 'Pele do Mundo', 'Fôlego Sem Fundo', 'Sorte Velha',
        'Nome que Anda', 'Mão que Doma', 'Passo Certo', 'Memória de Rei']
ESS = ['Fogo', 'Gelo', 'Raio', 'Podridão', 'Sombra', 'Espinho', 'Água', 'Terra']
FORA = ('Tuir', 'Zyza')   # o eco e os servos não despertam


def quantos(nv): return min(3, (nv or 0) // 100)


def na_ficha(f, dons):
    for k in ('segundo_coracao', 'voz_mando', 'rd_ess'): f.pop(k, None)
    for dn in dons:
        if dn.startswith('Segundo Coração'): f['segundo_coracao'] = f.get('segundo_coracao', 0) + 1
        elif dn.startswith('Voz de Mando'): f['voz_mando'] = True
        elif dn.startswith('Pele do Mundo'):
            e = dn.split(': ')[1].rstrip(')'); f.setdefault('rd_ess', {}); f['rd_ess'][e] = f['rd_ess'].get(e, 0) + 5
        elif dn.startswith('Passo Certo'): f['ini'] = f.get('nivel_ref', f.get('nivel', 20)) // 10 + 2


def rola_um(nome, nv, tem):
    novos = []
    while len(tem) + len(novos) < quantos(nv):
        r = d(12); dn = DONS[r - 1]
        if dn == 'Pele do Mundo': dn += f' (Essência: {ESS[d(8) - 1]})'
        novos.append((r, dn))
    return novos


def main():
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    N = carrega('npcs.json'); M = carrega('mundo_vivo.json'); F = carrega('fichas_combate.json')
    casa = set(F['fichas']) - {'Mamiltia'}
    grandes = {x['nome']: x for x in M.get('lendarios', [])}
    if a[0] == 'ver':
        for nome, v in sorted(list(N.items()) + [(k, g) for k, g in grandes.items() if k not in N], key=lambda kv: -(kv[1].get('nivel') or 0)):
            if v.get('dons') and (nome in casa or 'tudo' in a): print(f"{nome} ({v.get('nivel')}): {' · '.join(v['dons'])}" + ('' if nome in casa else ' (OCULTO)'))
        return
    if a[0] == 'rola':
        vis, oc = [], []
        for nome, v in list(N.items()) + [(k, g) for k, g in grandes.items() if k not in N]:
            if nome in FORA or quantos(v.get('nivel')) == 0: continue
            novos = rola_um(nome, v.get('nivel'), v.get('dons', []))
            if not novos: continue
            v['dons'] = v.get('dons', []) + [dn for _, dn in novos]
            txt = f"{nome} ({v.get('nivel')}): " + ' · '.join(f'd12 [{r}] {dn}' for r, dn in novos)
            (vis if nome in casa else oc).append(txt); print(txt + ('' if nome in casa else ' (OCULTO)'))
            if nome in F['fichas']: na_ficha(F['fichas'][nome], v['dons'])
            if nome in grandes and nome in N: grandes[nome]['dons'] = v['dons']
        grava('npcs.json', N); grava('mundo_vivo.json', M); grava('fichas_combate.json', F)
        if vis: anota('- O DESPERTAR (G26; despertar.py) dos heróis da casa: ' + ' | '.join(vis))
        if oc: anota('- (OCULTO) O DESPERTAR (G26) dos de fora e dos grandes do mundo: ' + ' | '.join(oc))
        if not vis and not oc: print('ninguém a despertar.')
        return
    sys.exit(__doc__)


if __name__ == '__main__':
    main()
