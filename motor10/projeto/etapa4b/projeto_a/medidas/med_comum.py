"""med_comum.py: o que as medidas do projeto A usam (só lê o motor; nada grava).
Roda de dentro de motor10/, com PYTHONDONTWRITEBYTECODE=1 e MOTOR10_MUNDO numa cópia do ensaio no rascunho."""
import os, sys, random, contextlib, io, copy, math
AQUI = os.path.dirname(os.path.abspath(__file__))
MOTOR = '/home/user/ferir/motor10'
if MOTOR not in sys.path: sys.path.insert(0, MOTOR)
import tabelas as T
import luta, estado, criaturas as CR, bichos
from pessoas import padrao, veste, ficha

COPIA = os.path.join(AQUI, 'mundos', 'ensaio_copia')


def quieto(f, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()): return f(*a, **k)


_E = None
def E():
    global _E
    if _E is None:
        os.environ['MOTOR10_MUNDO'] = COPIA; _E = estado.carrega()
    return _E


def gente(pid, **mais):
    """a pessoa do save (cópia), pronta para a luta, como entra hoje (o que veste, o PV)"""
    d = estado.lutador(E(), pid)
    d.update(mais)
    return copy.deepcopy(d)


def cheio(pid, **mais):
    """a mesma pessoa com o PV cheio e sem pena do corpo (para comparar)"""
    d = gente(pid, **mais); p = E()['gente'][pid]; d['pv'] = estado.pv_max(p); d['pena'] = 0; d['feridas'] = []; d['fol_menos'] = 0
    return d


def duelos(fa, fb, n, semente=7, surpresa=None, **kw):
    """n lutas com semente fixa. Devolve dict: vence (% de A), morre_a (% em que alguém de A morreu), morre0 (% em que o primeiro de A morreu), cai0, rodadas (mediana),
    pv0 (PV médio do primeiro de A no fim, nas que venceu)"""
    v = m = m0 = c0 = 0; rs = []; pvs = []; luta.semente(semente); r = random.Random(semente)
    for i in range(n):
        sp = surpresa(r) if callable(surpresa) else surpresa
        S = luta.nova(fa(), fb(i), quieto=True, surpresa=sp, **kw); luta.corre(S); A = [f for f in S['L'] if f['lado'] == 'A']
        v += S['fim'] == 'A'; m += any(f['estado'] == 'morto' for f in A); m0 += A[0]['estado'] == 'morto'; c0 += A[0]['estado'] in ('morto', 'caido')
        rs.append(S['r'])
        if S['fim'] == 'A': pvs.append(max(0, A[0]['pv']) / A[0]['pvmax'])
    rs.sort()
    return dict(vence=round(100 * v / n, 1), morre_a=round(100 * m / n, 1), morre0=round(100 * m0 / n, 1), cai0=round(100 * c0 / n, 1), rodadas=rs[len(rs) // 2],
                pv0=round(100 * sum(pvs) / len(pvs)) if pvs else 0, n=n)


def diz(nome, R):
    return f"{nome}: vence {R['vence']}% · alguém da casa morre {R['morre_a']}% · o primeiro morre {R['morre0']}% (cai {R['cai0']}%) · rodadas {R['rodadas']} · PV que sobra ao primeiro {R['pv0']}% ({R['n']} lutas)"


# ---------- o 2d20 que explode no 20 (a conta exata, como o caca._somas) ----------
def _somas():
    um = {}
    def d20x(p, soma, prof):
        for k in range(1, 21):
            q = p / 20
            if k == 20 and prof < 6: d20x(q, soma + 20, prof + 1)
            else: um[soma + k] = um.get(soma + k, 0) + q
    d20x(1.0, 0, 0)
    dois = {}
    for a, pa in um.items():
        for b, pb in um.items(): dois[a + b] = dois.get(a + b, 0) + pa * pb
    return dois
SOMAS = _somas()
def chance(precisa): return min(1.0, sum(p for s, p in SOMAS.items() if s >= precisa))
def pct(x): return f"{100 * x:.0f}%"
