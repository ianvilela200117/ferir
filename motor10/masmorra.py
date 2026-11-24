#!/usr/bin/env python3
"""masmorra.py — MOTOR 10, ETAPA 4b: AS MASMORRAS (capítulo 17; os números no tabelas_masmorra.py; o contrato: projeto/ETAPA_4B.md, seções 1, 2 e 12).

  A masmorra é um lugar do mapa (tipo "masmorra"), vizinho de uma vila ou de um ermo; por dentro tem salas, e cada sala é um lugar pequeno (tipo "sala") ligado às
  outras por passagens. Assim a contagem das criaturas, a prata no chão, a peça largada e a morte de quem cai lá dentro usam as regras de hoje. Descer é um ato aberto,
  escrito em quem comanda (marca.masmorra: a descida), e quem está na descida está FORA (estado.fora diz a sala). Lá dentro o tempo anda em lances de 20 minutos;
  doze lances fecham um bloco pelo ato.passa. A luz, o escuro, quem vê primeiro, as armadilhas e as fechaduras (pela conta do aço), o alarme, o que vagueia, o chefe no
  fundo, o tesouro (prata que já existe) e a memória (a sala limpa fica limpa).

  ESQUELETO DO ALICERCE (onda 1): as funções do contrato, neutras (nenhuma masmorra). A frente M (a masmorra) enche tudo sem mudar a assinatura nem o que cada
  função devolve.

Uso em código (o que as outras frentes chamam):
  de(E, lid) · salas(E, mid) · gera(E, molde, nome, vizinho, niveis=None, cat=None, longe=None, origem='') · poe(E, planta) · na_vila(E, vila='vila')
  virada(E) · voce(E) · mesa(E) · so_mestre(E) · retomar(E) · recusa_fecha(E)
Uso de linha de comando (frente M): python3 masmorra.py ver | descer ... | ir SALA | escutar | procurar | abrir | desarmar | ... (projeto A, seção 3.1)
"""
import sys


def de(E, lid):
    """o id da masmorra deste lugar (o lugar é a masmorra, ou uma sala dela), ou None"""
    l = E['lugares'].get(lid) if isinstance(lid, str) else None
    if not isinstance(l, dict): return None
    if l.get('tipo') == 'masmorra': return lid
    return l.get('masmorra') if l.get('tipo') == 'sala' and l.get('masmorra') in E['lugares'] else None


def salas(E, mid):
    """as salas da masmorra, nível a nível (a ordem dos níveis dela)"""
    m = E['lugares'].get(mid) or {}
    return [s for nv in m.get('niveis') or [] for s in nv.get('salas') or [] if s in E['lugares']]


def gera(E, molde, nome, vizinho, niveis=None, cat=None, longe=None, origem=''):
    """(frente M) os efeitos que criam uma masmorra pelo dado do mundo (evento gera: segredo)"""
    sys.exit('gerar masmorra é da frente M (o esqueleto ainda não faz)')


def poe(E, planta):
    """(frente M) os efeitos da masmorra feita à mão (a Cripta da Cova Velha)"""
    sys.exit('pôr masmorra é da frente M (o esqueleto ainda não faz)')


def voce(E): return []
def mesa(E): return []          # (frente M) só com a descida aberta
def so_mestre(E): return []
def retomar(E): return []
def recusa_fecha(E): return []


def na_vila(E, vila='vila'):
    """(frente M) a Cripta da Cova Velha: aplica os eventos dela (gera) e devolve as linhas. O esqueleto não põe nada."""
    return []


if __name__ == '__main__':
    print(__doc__)
