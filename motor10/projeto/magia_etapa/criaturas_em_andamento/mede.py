"""mede.py — RASCUNHO da parte J: a régua. Lutas de ENSAIO (dado de mentira, com semente; nada é guardado) no luta_j.py.

  homens(k, cat, ...)      k homens do degrau (gente gerada do banco: espada, malha e escudo da categoria; nível do REF)
  mede(faz_a, faz_b, n)    n lutas: {vence, perde, outro (impasse ou empate), rodadas (mediana), cai (dos de A, quantos caem ou morrem por luta, em média), foge (dos de B)}
"""
import os, sys, random
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI); sys.path.insert(0, os.path.join(AQUI, 'base'))
import tabelas as T
import tabelas_bichos as TB
import tabelas_criaturas as TC
import criaturas as CR
import luta_j as L
from pessoas import padrao, veste

UMA_MAO = lambda fam: T.FAMILIAS[fam]['maos'] == 1


def homens(k, cat, nivel=None, familia='espada', material='malha', pre='h', prata=False, arma=None, molde='guerreiro', vontade=80, **kw):
    """k homens do degrau `cat` (o do banco). arma: a categoria só da arma, se for outra. prata: a arma fere inteiro quem o aço comum mal toca."""
    lvl = nivel if nivel is not None else TC.REF[cat]; ca = cat if arma is None else arma
    def faz():
        out = []
        for i in range(k):
            p = veste(padrao(f'{pre}{i + 1}' if k > 1 else pre, lvl, molde=molde, atributos=({'Vontade': vontade} if max(cat, ca) >= 3 and vontade else None), **kw),
                      arma=(familia, ca), armadura=(material, cat), escudo=cat if UMA_MAO(familia) else None, arma2=('adaga', cat) if T.FAMILIAS[familia].get('distancia') else None)
            if prata: p['equip']['arma']['efeitos'].append(dict(chave='prata'))
            out.append(p)
        return out
    return faz


def junta(*fs): return lambda: [p for f in fs for p in f()]
def cri(que, n=None, **mais): return lambda: CR.faz_bando(que, n=n, sorte=random, **mais)


def mede(faz_a, faz_b, n=300, semente=1, **kw):
    L.semente(semente); random.seed(semente); m = dict(vence=0, perde=0, outro=0, cai=0, foge=0, rende=0); rs = []; extra = dict(cortadas=0, anunciadas=0, fases=0, artes=0, tentou=0, pegou=0)
    for _ in range(n):
        S = L.nova(faz_a(), faz_b(), quieto=True, **{**dict(inicio='perto'), **kw}); L.corre(S)
        m['vence'] += S['fim'] == 'A'; m['perde'] += S['fim'] == 'B'; m['outro'] += S['fim'] not in ('A', 'B'); rs.append(S['r'])
        m['cai'] += sum(f['estado'] in ('morto', 'caido') for f in S['L'] if f['lado'] == 'A'); m['foge'] += sum(f['estado'] == 'fugiu' for f in S['L'] if f['lado'] == 'B'); m['rende'] += sum(f['estado'] == 'rendido' for f in S['L'] if f['lado'] == 'B')
        extra['cortadas'] += S.get('cortadas', 0); extra['anunciadas'] += S.get('anunciadas', 0); extra['fases'] += S.get('fases_vistas', 0); extra['artes'] += S.get('artes_n', 0); extra['tentou'] += S.get('f_tentou', 0); extra['pegou'] += S.get('f_pegou', 0)
    rs.sort(); out = {k: round(100 * v / n) for k, v in m.items() if k in ('vence', 'perde', 'outro')}
    out.update(rodadas=rs[len(rs) // 2], cai=round(m['cai'] / n, 2), foge=round(m['foge'] / n, 2), rende=round(m['rende'] / n, 2), **{k: round(v / n, 2) for k, v in extra.items()})
    return out


def diz(nome, m): return f"{nome:<78} vence {m['vence']:>3}% · perde {m['perde']:>3}% · outro {m['outro']:>2}% · {m['rodadas']:>2} rodadas · caem {m['cai']:.2f} da casa · fogem {m['foge']:.2f} · rendem-se {m['rende']:.2f}"


if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    print(f'A RÉGUA DE HOJE (as 14 espécies do capítulo 6 no luta_j.py; {n} lutas por linha): o homem do degrau contra um, contra o bando, e quatro homens contra o bando')
    for esp, e in sorted(TB.ESPECIES.items(), key=lambda x: (x[1]['cat'], x[1]['nivel'])):
        if esp in TC.CORPOS: continue
        c = e['cat']; lo, hi = e['bando']
        l = diz(f"{e['nome']} (grau {e['grau']}, {T.CATS[c]}): 1 homem × 1", mede(homens(1, c), cri(esp, 1), n))
        print(l)
        if hi > 1: print(diz(f"   1 homem × {hi}", mede(homens(1, c), cri(esp, hi), n)))
        if c >= 3 or hi > 1: print(diz(f"   4 homens × {hi}", mede(homens(4, c), cri(esp, hi), n)))
