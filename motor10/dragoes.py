#!/usr/bin/env python3
"""dragoes.py — MOTOR 10, ETAPA 4b: OS DRAGÕES (capítulo 20; os números no tabelas_dragoes.py; o contrato: projeto/ETAPA_4B.md, seções 2, 9 e 12).

  Três tipos pelo lugar (o dragão da serra, o verme do brejo, o dragão das grutas), cinco idades (do filhote ao ancião). O dragão é um bicho: a luta o roda com os traços
  que já tem, mais a fase `foge` (o que voa, ferido fora do covil, vai embora pelo ar: E3 a; no covil, quem monta a luta põe sem_saida do lado dele, e ele luta até
  morrer). O núcleo só do adulto para cima. O covil é uma sala de masmorra de molde covil (ou um ermo) com o registro `dragao`; o tesouro é o estoque do lugar e as
  peças guardadas nele: prata que já existe, posta pelo gerador. A vida do dragão (dormir, atacar, cobrar, sarar) é o evento "dragão", todo dia.

  ESQUELETO DO ALICERCE (onda 1): as funções do contrato, neutras (nenhum dragão: tabelas_dragoes.ESPECIES vazia). A frente D (os dragões) enche tudo sem mudar a
  assinatura nem o que cada função devolve.

Uso em código (o que as outras frentes chamam):
  especie(tipo, idade) · dragao(tipo, idade, nome=None, **mais) · de(E, lid) · monta(E, lid) · acordado(E, lid) · vigilia(E, lid) · punhado(E, lid, pid) · acorda(E, lid)
  depois_da_luta(E, lid, S, campo, quem) · poe(E, lid, tipo, idade, nome, vila=None, tesouro=0, dorme=0) · ameaca(tipo, idade, arma=None, armadura=None)
  virada(E) · mesa(E) · so_mestre(E) · na_vila(E, vila='vila')
"""
import sys
import tabelas_dragoes as TD


def especie(tipo, idade):
    """a chave da espécie de um dragão: 'dragão-da-serra-jovem', 'verme-do-brejo-filhote'..."""
    if tipo not in TD.TIPOS or idade not in TD.IDADES: sys.exit(f'dragão desconhecido: "{tipo} {idade}" (os tipos: {", ".join(TD.TIPOS)}; as idades: {", ".join(TD.IDADES)})')
    return TD.chave(tipo, idade)


def dragao(tipo, idade, nome=None, **mais):
    """o lutador pronto para o luta.nova (como bichos.bicho). O esqueleto ainda não tem os dragões (tabelas_dragoes.ESPECIES vazia: frente D)."""
    k = especie(tipo, idade)
    if k not in TD.ESPECIES: sys.exit(f'ainda não há o dragão "{k}" (tabelas_dragoes.ESPECIES: frente D)')
    import bichos
    return bichos.bicho(k, nome=nome, **mais)


def de(E, lid):
    """o registro do dragão que mora no lugar, ou None"""
    d = (E['lugares'].get(lid) or {}).get('dragao') if isinstance(lid, str) else None
    return d if isinstance(d, dict) else None


def acordado(E, lid):
    """o dragão do lugar está acordado? (sem dragão: não)"""
    d = de(E, lid)
    return bool(d) and not (isinstance(d.get('dorme_ate'), int) and d['dorme_ate'] > E['relogio']['dia'])


def monta(E, lid):
    """(a pessoa em forma curta para o cenário da luta, dorme) do dragão do lugar: {"bicho": CHAVE, "nome": ..., "pv": ..., "lider": true}; ou None se não há dragão
    (ou se a espécie dele ainda não existe)"""
    d = de(E, lid)
    if not d or TD.chave(d['tipo'], d['idade']) not in TD.ESPECIES: return None
    p = dict(bicho=TD.chave(d['tipo'], d['idade']), nome=d['nome'], lider=True)
    if isinstance(d.get('pv'), int): p['pv'] = d['pv']
    return p, not acordado(E, lid)


def vigilia(E, lid):
    """(frente D) o número contra o qual o ladrão anda escondido na câmara (20 + Percepção ÷ 10 + 2, mais 2 por punhado do sono); None se acordado ou se não há"""
    return None


def punhado(E, lid, pid):
    """(frente D) (efeitos, texto): a sexta parte da prata do sono, ou uma peça, para a pessoa; e o punhado contado. O esqueleto: ([], '')"""
    return [], ''


def acorda(E, lid):
    """(frente D) os efeitos de acordar o dragão. O esqueleto: []"""
    return []


def depois_da_luta(E, lid, S, campo, quem):
    """(frente D) (efeitos, {pessoa: {bem: quanto}}, linhas), como o criaturas.depois_da_luta: o PV de quem fugiu volta ao registro; o morto sai do registro e o corpo
    e o núcleo entram; o tesouro para quem ficou com o campo. O esqueleto: ([], {}, [])"""
    return [], {}, []


def poe(E, lid, tipo, idade, nome, vila=None, tesouro=0, dorme=0):
    """(frente D) os efeitos que põem o dragão e o tesouro num lugar (evento gera ou mestre: segredo)"""
    sys.exit('pôr um dragão é da frente D (o esqueleto ainda não faz)')


def ameaca(tipo, idade, arma=None, armadura=None):
    """(frente D) a frase do chefe, que o Mestre lê quando a cena põe o dragão à frente. O esqueleto: ''"""
    return ''


def mesa(E): return []          # (frente D) o que se conta dos dragões que a gente dali conhece
def so_mestre(E): return []


def na_vila(E, vila='vila'):
    """(frente D) o Tição, o dragão jovem longe, em Vau Seco (E4 a): aplica os eventos dele (gera) e devolve as linhas. O esqueleto não põe nada."""
    return []


if __name__ == '__main__':
    print(__doc__)
