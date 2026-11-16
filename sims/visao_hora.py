#!/usr/bin/env python3
"""visao_hora.py — A VISÃO DO TEMPO sobre uma batalha: só a PRIMEIRA HORA (uma rodada do batalha.py), N futuros.
Sem valor de jogo (régua). Usa a mesma conta do batalha.py: não inventa regra.
Uso: python3 sims/visao_hora.py NOME_DA_BATALHA [N]
"""
import sys, os, json, random, copy
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import batalha as Bt
Bt.SIM = True
def uma_hora(B):
    B = copy.deepcopy(B); A_, B_ = B['lados']['A'], B['lados']['B']; ini = {k: Bt.homens(v) for k, v in B['lados'].items()}
    fa, fb = Bt.forca(A_, B['terreno'], A_.get('defende')), Bt.forca(B_, B['terreno'], B_.get('defende'))
    ra = Bt.d(20) + Bt.d(20) + A_.get('comando', 0); rb = Bt.d(20) + Bt.d(20) + B_.get('comando', 0); D = ra - rb
    pa = max(0.02, min(0.25, 0.08 * (fb / fa) ** 0.5 * (1 - D / 40))); pb = max(0.02, min(0.25, 0.08 * (fa / fb) ** 0.5 * (1 + D / 40)))
    for lado, p in ((A_, pa), (B_, pb)):
        for u in lado['unidades']: u['homens'] = max(0, int(round(u['homens'] * (1 - p))))
    quebra = {'A': False, 'B': False}; fer = []
    for k, lado, p, perdeu in (('A', A_, pa, D < 0), ('B', B_, pb, D > 0)):
        if p > 0.15 or Bt.homens(lado) < ini[k] / 2:
            for u in list(lado['unidades']):
                if Bt.d(6) > u.get('moral', 3): quebra[k] = True; lado['unidades'].remove(u)
        if perdeu:
            for h in lado.get('herois', []):
                if Bt.d(20) == 1: fer.append(h['nome'])
    return ini['A'] - Bt.homens(A_) if not quebra['A'] else None, pb, quebra, fer, ini, int(round(ini['B'] * pb)), fa, fb
def main():
    nome = sys.argv[1]; n = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
    f = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'batalhas', nome + '.json'); B = json.load(open(f, encoding='utf-8'))
    ca = []; cb = []; qa = qb = 0; fer = {}
    for _ in range(n):
        a, pb, q, fr, ini, caidosB, fa, fb = uma_hora(B)
        ca.append(a if a is not None else ini['A']); cb.append(caidosB); qa += q['A']; qb += q['B']
        for x in fr: fer[x] = fer.get(x, 0) + 1
    ca.sort(); cb.sort()
    print(f"A VISÃO DO TEMPO · {B['nome']} · uma hora, {n} futuros (sem valor de jogo) · força {fa:.0f} × {fb:.0f}")
    print(f"  {B['lados']['A']['nome']}: caem {ca[n // 2]} (de {ca[n // 10]} a {ca[9 * n // 10]}) de {ini['A']} · quebram em {100 * qa / n:.0f}%")
    print(f"  {B['lados']['B']['nome']}: caem {cb[n // 2]} (de {cb[n // 10]} a {cb[9 * n // 10]}) de {ini['B']} · QUEBRAM E FOGEM dentro da hora em {100 * qb / n:.0f}%")
    print('  herói nosso ferido na hora: ' + (' · '.join(f'{k} {100 * v / n:.1f}%' for k, v in sorted(fer.items())) if fer else 'nenhum em nenhum futuro'))
main()
