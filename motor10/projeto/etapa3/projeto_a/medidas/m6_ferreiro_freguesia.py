#!/usr/bin/env python3
"""m6_ferreiro_freguesia.py — MEDIDA (projeto A, etapa 3): FORJAR PARA A LOJA segue sem ser mina quando há FREGUESIA (o povo compra da prateleira e os ferreiros do povo
a refazem)? O robô é o do provas_mercado (ferreiro_de_loja: o ferreiro de começo da vila de teste, ganancioso, 30 dias), com o dia da região do protótipo ligado em Pedra Rasa
(a bolsa do povo, a freguesia, a forja do povo, a caça do povo; sem rotas). Compara com o motor de hoje. A meta do banco: nos 5 primeiros dias, em média até 6 por dia
(o pior caso até 12); do Dia 6 ao 30, em média até 4.

Roda de dentro de motor10/:  PYTHONDONTWRITEBYTECODE=1 python3 projeto/etapa3/projeto_a/medidas/m6_ferreiro_freguesia.py [vidas=30] [cats=0,1]
Tudo em memória.
"""
import os, sys
sys.path.insert(0, os.getcwd()); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
op = dict(x.split('=', 1) for x in sys.argv[1:] if '=' in x); N = int(op.get('vidas', 30)); CATS = tuple(int(x) for x in op.get('cats', '0,1').split(','))
import estado, provas_mercado, proto_regiao as R
R.instala(); R.TAB['SAFRA_NA_VILA'] = False


class _Mod: pass
REG = _Mod(); REG.__name__ = 'proto_regiao'
def _virada(E):
    if E['lugares']['vila'].get('bolsa') is None: estado.aplica(E, 'gera', [['lugar', 'vila', 'bolsa', 'poe', 2000]], texto='(medida) a bolsa do povo de Pedra Rasa')
    R.virada(E)
REG.virada = _virada


def roda(com):
    estado.modulos()
    estado._MODS[:] = [m for m in estado._MODS if getattr(m, '__name__', '') != 'proto_regiao'] + ([REG] if com else [])
    if com: R.moeda_na_loja()
    vs = [provas_mercado.ferreiro_de_loja(s, CATS) for s in range(1, N + 1)]
    m5 = sum(v['rende'][0] for v in vs) / N; p5 = max(v['rende'][0] for v in vs); m30 = sum(v['rende'][1] for v in vs) / N
    pc = [sum(v['pecas']) for v in vs]; bolso = [sum(v['no_bolso']) / 2 for v in vs]
    return m5, p5, m30, sum(pc) / N, sum(bolso) / N


for nome, com in (('o motor de hoje', False), ('com a freguesia (o protótipo)', True)):
    m5, p5, m30, pc, bolso = roda(com)
    print(f"{nome:32}: o que a forja rende (vendas menos matéria), em prata por dia: nos 5 primeiros dias {m5:.2f} em média, {p5:.2f} no pior caso; do Dia 6 ao 30, {m30:.2f} · "
          f"{pc:.1f} peças vendidas por vida · {N} vidas, categorias {CATS}")
