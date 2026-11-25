#!/usr/bin/env python3
"""viagem.py — MOTOR 10, etapa 3: A VIAGEM (andar uma rota em blocos, a estação, a noite, o mato, o encontro, quem vai junto, a carga). ESQUELETO NEUTRO: a frente A2 o enche.

O esqueleto recusa abrir a viagem ("ainda não"); o resto não faz nada. Os blocos até um lugar já saem do mapa (a distância de regiao.py, sem o inverno).
Quem viaja (marca.viagem) está FORA: o estado.fora diz o ermo da rota, e o estado.presente recusa os atos da vila. O contrato: projeto/ETAPA_3.md, seção 12.

  python3 viagem.py                 esta ajuda
  python3 viagem.py ir DESTINO      (ainda não)
"""
import sys
import estado, regiao


def ir(E, pid, destino, por=None, com=(), noite=False, paga=0):
    """abre a viagem e anda (frente A2). O esqueleto recusa"""
    sys.exit('ainda não: a viagem é da frente A2 (viagem.py é o esqueleto do alicerce)')


def blocos_ate(E, a, b, estacao=None):
    """os blocos de estrada de a até b, pelo caminho mais curto, na estação (o inverno pesa no caminho e na trilha: frente A2); None se não há caminho. O esqueleto: a distância do mapa"""
    return regiao.distancia(E, a, b)


def anda_npc(E, pid, destino):
    """a viagem de quem não é o personagem (um evento por dia de estrada, o encontro pela rapida.py): os efeitos. O esqueleto: [] (ninguém anda)"""
    return []


def carga(E, pid):
    """a carga da pessoa: {"peso", "teto", "leva" (o que os animais levam), "pesado" (acima da metade do teto)}. O esqueleto: nada pesa"""
    p = E['gente'][pid]
    return dict(peso=0, teto=p['atributos']['Força'] // 2, leva=0, pesado=False)


def virada(E): return None       # a comida da carga que estraga; a viagem dos nomeados (frente A2)
def mesa(E): return []           # "A viagem" (só aberta)
def retomar(E): return []        # a viagem aberta, numa linha
def so_mestre(E): return []
def recusa_fecha(E): return []   # a viagem aberta não impede o turno de fechar: fica guardada na pessoa e retoma


if __name__ == '__main__':
    a = sys.argv[1:]
    if a: sys.exit('ainda não: a viagem é da frente A2 (viagem.py é o esqueleto do alicerce)')
    print(__doc__)
