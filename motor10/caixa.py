#!/usr/bin/env python3
"""caixa.py — MOTOR 10, etapa 3: A CAIXA DE ENTRADA (o pedido com prazo, de quem tem motivo no estado; calado, vale o padrão; cabem 7). ESQUELETO NEUTRO: a frente B2 o enche.

O esqueleto não abre pedido nem responde; os pedidos abertos já se leem do estado (caixa.json), e o turno.py já faz do pedido que vence em um dia uma pergunta do turno,
ligada a `caixa.py responde ID LETRA`. O contrato: projeto/ETAPA_3.md, seção 12.

  python3 caixa.py                  esta ajuda
  python3 caixa.py ver              os pedidos abertos do save (MOTOR10_MUNDO)
  python3 caixa.py responde ID LETRA    (ainda não)
"""
import sys
import estado


def abertos(E, para=None):
    """os pedidos abertos na caixa de alguém (o personagem, se não se diz), pelo prazo: [registro]"""
    para = para or estado.eu(E); C = (E.get('caixa') or {}).get('abertos') or {}
    return sorted((c for c in C.values() if isinstance(c, dict) and c.get('para') == para), key=lambda c: (c.get('prazo', 0), c.get('id', '')))


def abre(E, de, molde, pede, opcoes, padrao, prazo_dias, motivo, custo='', para=None):
    """os efeitos que abrem um pedido (['caixa', 'abre', reg]; o oitavo força o mais velho antes). O esqueleto: []"""
    return []


def responde(E, cid, letra, **mais):
    """o que o personagem responde (o turno liga a pergunta a isto): os efeitos do que ele escolheu. O esqueleto recusa"""
    sys.exit('ainda não: a caixa é da frente B2 (caixa.py é o esqueleto do alicerce)')


def virada(E): return None       # o pedido que venceu vale o padrão, com o custo
def mesa(E): return []           # "A caixa (N de 7)"
def so_mestre(E): return []


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[:1] == ['ver']:
        E = estado.carrega(); L = abertos(E)
        for c in L: print(f"{c['id']} · {E['gente'][c['de']]['nome']}: {c['pede']} · prazo: bloco {c['prazo']} · " + ' · '.join(f'{k}) {v}' for k, v in c['opcoes'].items()) + f" · calado: {c['padrao']}")
        if not L: print('a caixa está vazia')
    elif a: sys.exit('ainda não: a caixa é da frente B2 (caixa.py é o esqueleto do alicerce)')
    else: print(__doc__)
