#!/usr/bin/env python3
"""missoes.py — MOTOR 10, etapa 3: AS MISSÕES (quem pede, a paga guardada desde que nasce, a caução, o prazo; qualquer um pode cumprir). ESQUELETO NEUTRO: a frente B2 o enche.

O esqueleto não abre nem fecha missão; o quadro de um lugar já se lê do estado (missoes.json). A paga guardada (a "guarda") é prata: conta na prata do mundo, e só muda
de mão no mesmo evento em que sai (ou entra) numa bolsa ou num caixa. O contrato: projeto/ETAPA_3.md, seção 12.

  python3 missoes.py                esta ajuda
  python3 missoes.py ver            o quadro do lugar do personagem (MOTOR10_MUNDO)
"""
import sys
import estado
import tabelas_mundo as M


def quadro(E, lugar):
    """as missões abertas de um lugar (as que ninguém pegou ainda, e as pegas), pelo prazo: [registro]"""
    I = (E.get('missoes') or {}).get('itens') or {}
    return sorted((m for m in I.values() if isinstance(m, dict) and m.get('onde') == lugar and m.get('estado') not in M.MISSAO_FECHA), key=lambda m: (m.get('prazo', 0), m.get('id', '')))


def abre(E, de, onde, tipo, grau, alvo, paga, prazo, caucao=None):
    """os efeitos que abrem uma missão, com a paga guardada (a guarda sai de quem pede no mesmo evento). O esqueleto: []"""
    return []


def pega(E, pid, mid): sys.exit('ainda não: as missões são da frente B2 (missoes.py é o esqueleto do alicerce)')
def cumpre(E, mid, pid=None): sys.exit('ainda não: as missões são da frente B2 (missoes.py é o esqueleto do alicerce)')
def entrega(E, mid, iid): sys.exit('ainda não: as missões são da frente B2 (missoes.py é o esqueleto do alicerce)')
def fecha(E, mid, desfecho): sys.exit('ainda não: as missões são da frente B2 (missoes.py é o esqueleto do alicerce)')


def virada(E): return None       # a missão vencida; o nomeado que pega do quadro e cumpre pela conta rápida
def mesa(E): return []           # "O quadro"
def so_mestre(E): return []


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[:1] == ['ver']:
        E = estado.carrega(); L = quadro(E, E['gente'][estado.eu(E)]['lugar'])
        for m in L: print(f"{m['id']} · {E['gente'][m['de']]['nome']}: {m['tipo']}, grau {m['grau']}, {m['paga']} de prata (caução {m.get('caucao', 0)}) · até o Dia {m['prazo']}")
        if not L: print('o quadro está vazio')
    elif a: sys.exit('ainda não: as missões são da frente B2 (missoes.py é o esqueleto do alicerce)')
    else: print(__doc__)
