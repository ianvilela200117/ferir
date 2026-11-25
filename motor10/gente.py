#!/usr/bin/env python3
"""gente.py — MOTOR 10, etapa 3: A GENTE QUE LEMBRA (os nomeados com papel, rotina, bolsa, querer, laços, memória, opinião e fama). ESQUELETO NEUTRO: a frente B1 o enche.

O esqueleto não faz nada: ninguém tem rotina nem querer, ninguém lembra, a opinião é zero, quem é chamado vai junto sem paga (a regra de hoje) e toda loja negocia.
A fama já se lê do estado (estado.fama_hoje), e o teto sai da conta rápida (rapida.teto). O contrato: projeto/ETAPA_3.md, seção 12.

  python3 gente.py                  esta ajuda
"""
import sys
import estado, rapida


def povoa(E, lugar, pessoas=None):
    """os efeitos (evento "gera") que põem a gente com nome num lugar, pela lista de papéis, e as pessoas prontas que a história der (a porta da etapa 7). O esqueleto: []"""
    return []


def povoa_regiao(E):
    """a gente da região inteira (o vila_teste.py regiao chama): aplica os seus eventos "gera" e devolve as linhas que contam o que pôs. O esqueleto: nada, []"""
    return []


def ponto(E, pid, bloco=None):
    """onde a pessoa está e o que faz neste bloco (a rotina: uma tabela, não grava nada): (o ponto, o que faz). O esqueleto: ("casa", None)"""
    return ('casa', None)


def opiniao(E, quem, de=None):
    """o que `quem` acha de `de` (o personagem, se não se diz): (o número de −10 a 10, a palavra, [os porquês]). O esqueleto: (0, "não tem opinião", [])"""
    return (0, 'não tem opinião', [])


def lembra(E, quem, tipo, de=None, canal='viu', texto='', peso=None):
    """os efeitos que gravam um fato na memória de `quem` (['pessoa', quem, 'memoria', 'junta', fato]). O esqueleto: []"""
    return []


def tom(E, lugar, de=None):
    """o tom do lugar sobre alguém (a fama somada, de −3 a +2). O esqueleto: 0"""
    return 0


def fama(E, quem, lugar, eixo=None):
    """a fama de hoje (esfriada) de alguém num lugar: o número de um eixo, ou {eixo: número} sem eixo"""
    dia = E['relogio']['dia']; p = E['gente'][quem]
    return estado.fama_hoje(p, lugar, eixo, dia) if eixo else {e: estado.fama_hoje(p, lugar, e, dia) for e in estado.M.FAMA_EIXOS}


def teto(E, pid): return rapida.teto(E, pid)          # o teto é um fato só: o da conta rápida


def vai_junto(E, quem, com_quem, perigo, dias):
    """o que `com_quem` pede para ir com `quem` ao perigo: {"vai": sim ou não, "paga": prata, "diz": a frase}. O esqueleto: vai, sem paga (a regra de hoje)"""
    return dict(vai=True, paga=0, diz='')


def companhia(E, quem, com, perigo, dias, paga=0):
    """o gancho companhia (o estado.companhia chama ao abrir a saída, a descida e a viagem): (a frase da recusa ou '', os efeitos da paga). O esqueleto: ('', [])"""
    return '', []


def negocia(E, quem, com_quem):
    """o gancho negocia (o mercado e a refeição chamam antes de vender): '' (negocia) ou a frase da recusa. O esqueleto: ''"""
    return ''


def virada(E): return None       # a semana de cada um (a bolsa, o desgaste, o querer que vira ato), o nomeado que se repõe
def mesa(E): return []           # "Quem está aqui"
def so_mestre(E): return []      # os números da opinião, os quereres escondidos


if __name__ == '__main__':
    if sys.argv[1:]: sys.exit('ainda não: a gente é da frente B1 (gente.py é o esqueleto do alicerce)')
    print(__doc__)
