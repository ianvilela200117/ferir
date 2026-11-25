#!/usr/bin/env python3
"""regiao.py — MOTOR 10, etapa 3: A REGIÃO (o mapa, as rotas, o povo em número, o comércio entre lugares). ESQUELETO NEUTRO do alicerce: a frente A1 o enche.

O que o esqueleto já faz (só lê o estado: não é regra): os vizinhos por rota, a distância em blocos pelo caminho mais curto, a rota entre dois lugares.
O resto não faz nada (o gerador não gera, o dia da região não anda, o perigo é zero, a guarda é zero), e a mesa não ganha linha.
O contrato (os nomes, as formas, o que cada função devolve): projeto/ETAPA_3.md, seção 12.

  python3 regiao.py                 esta ajuda
  python3 regiao.py mapa            as rotas do save (MOTOR10_MUNDO), uma por linha
"""
import heapq, sys
import estado


def gera(E, semente, planta=None):
    """os efeitos (evento "gera") que fazem nascer a região em volta do que existe, pela semente, com a planta (a porta da etapa 7). O esqueleto não gera nada: []"""
    return []


def virada(E):
    """o dia da região (o povo, a bolsa, o carreto, a freguesia, a caça do povo, a fome, a migração, o bando; a semana; a estação; o ano). O esqueleto: nada"""
    return None


def rotas_de(E, lid, abertas=True):
    """as rotas que saem de um lugar: [(id, rota)], na ordem do arquivo (só as abertas, se `abertas`)"""
    return [(k, r) for k, r in (E.get('rotas') or {}).items() if isinstance(r, dict) and lid in (r.get('a'), r.get('b')) and (r.get('aberta', True) or not abertas)]


def vizinhos(E, lid, abertas=True):
    """os vizinhos por rota: [(lugar, rota, blocos)], na ordem do arquivo das rotas (a rota fechada não leva ninguém nem notícia)"""
    return [(r['b'] if r['a'] == lid else r['a'], k, r['blocos']) for k, r in rotas_de(E, lid, abertas)]


def rota_entre(E, a, b):
    """o id da rota que liga a e b (aberta ou não), ou None"""
    return next((k for k, r in (E.get('rotas') or {}).items() if isinstance(r, dict) and {r.get('a'), r.get('b')} == {a, b}), None)


def caminho(E, a, b, abertas=True, conhece=None):
    """o caminho mais curto em blocos de a até b: (blocos, [lugares de a até b], [rotas]); None se não há. `conhece`: só as rotas desta lista (o mapa do personagem)"""
    fila = [(0, a, [a], [])]; visto = set()
    while fila:
        d, x, ls, rs = heapq.heappop(fila)
        if x == b: return d, ls, rs
        if x in visto: continue
        visto.add(x)
        for y, k, bl in vizinhos(E, x, abertas):
            if y not in visto and (conhece is None or k in conhece): heapq.heappush(fila, (d + bl, y, ls + [y], rs + [k]))
    return None


def distancia(E, a, b, abertas=True):
    """os blocos de a até b pelo caminho mais curto (0 se é o mesmo lugar), ou None se não há caminho"""
    c = caminho(E, a, b, abertas)
    return c[0] if c else None


def guardas(E, lid):
    """quantos do povo do lugar são guarda (a parte do povo pelo tipo do lugar: tabelas_regiao). O esqueleto: 0"""
    return 0


def perigo(E, rota):
    """o perigo de uma rota, por bloco: {"bicho": chance, "bando": chance, "patrulha": parte, "palavra": o que o jogador lê, "pior": espécie ou None}. O esqueleto: segura"""
    return dict(bicho=0.0, bando=0.0, patrulha=0.0, palavra='segura', pior=None)


def mesa(E): return []          # "Daqui se vai a" (frente A1)
def so_mestre(E): return []      # a conta de verdade do perigo das rotas daqui, o bando mais perto, a colheita (frente A1)


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[:1] == ['mapa']:
        E = estado.carrega()
        for k, r in (E.get('rotas') or {}).items(): print(f"{k}: {E['lugares'][r['a']]['nome']} a {E['lugares'][r['b']]['nome']}, {estado.tantos(r['blocos'], 'bloco')} de {r['tipo']}" + ('' if r.get('aberta', True) else ' (fechada)'))
        if not E.get('rotas'): print('o save não tem rotas (a região ainda não nasceu)')
    elif a: sys.exit('ainda não: a região é da frente A1 (regiao.py é o esqueleto do alicerce)')
    else: print(__doc__)
