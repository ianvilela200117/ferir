#!/usr/bin/env python3
"""noticias.py — MOTOR 10, etapa 3: A NOTÍCIA (nasce no evento que a causa, anda uma rota por dia, vira boato depois do quarto salto). ESQUELETO NEUTRO: a frente B2 o enche.

O esqueleto não faz nascer nem andar notícia; o que chegou a um lugar já se lê do estado (noticias.json). O contrato: projeto/ETAPA_3.md, seção 12.

  python3 noticias.py               esta ajuda
"""
import sys
import estado


def nasce(E, tipo, texto, onde, sobre=None, quem=None, eixo=None, fama=0, peso=0, alcance=1):
    """os efeitos que fazem nascer uma notícia (['noticia', 'nasce', reg]), para o evento que a causou. O esqueleto: []"""
    return []


def chegou(E, lugar, sobre=None):
    """as notícias que chegaram a um lugar (as ativas), as mais novas primeiro: [registro]; com `sobre`, só as que falam dessa pessoa"""
    A = (E.get('noticias') or {}).get('ativas') or {}
    L = [n for n in A.values() if isinstance(n, dict) and lugar in (n.get('em') or {}) and (sobre is None or n.get('sobre') == sobre)]
    return sorted(L, key=lambda n: (-(n['em'][lugar][0]), n.get('id', '')))


def virada(E): return None       # a notícia anda uma rota por dia; a que parou de andar sai em 28 dias
def mesa(E): return []           # "O que se diz de você" e "Dois fatos que não tocam você"
def so_mestre(E): return []


if __name__ == '__main__':
    if sys.argv[1:]: sys.exit('ainda não: a notícia é da frente B2 (noticias.py é o esqueleto do alicerce)')
    print(__doc__)
