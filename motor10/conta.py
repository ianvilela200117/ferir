#!/usr/bin/env python3
"""conta.py — MOTOR 10, ETAPA FINAL: A CONTA RÁPIDA DA LUTA. Longe do personagem, a luta dos rivais (contra a masmorra, o bicho, a frente, o outro no torneio)
não roda rodada a rodada: sai de uma curva — a chance de um lado vencer pela diferença de categoria (a arma de um contra a armadura do outro, a regra de ouro),
o PV somado, quantos são, a defesa, a mão e a força. A curva é AFINADA CONTRA O `luta.py` (as lutas de verdade, milhares), e o banco confere que ela erra
menos de 8 pontos (a meta 8 do PROJETO, seção 9).

  python3 conta.py afina [N]          roda N casos (padrão 900), cada um 24 lutas de verdade, e acha os pesos da curva (grava em dados/conta_pesos.json)
  python3 conta.py confere [N]        N casos novos: o erro médio da curva contra a luta de verdade (padrão 300)
(A PARTE 2, FASE 2) A ACESA NA CONTA: quem traz uma habilidade acesa de luta (a Roda com arma de peso, a Sanha, o Rito de Veia) leva, por cima da curva, o que ela vale no duelo de
iguais pelo grau (os pontos do banco, provas_habilidades HB1: a vitória a mais vira a diferença no logit). Os casos ao acaso do `afina` e do `confere` não têm habilidade: a meta 8 não
muda.
"""
import json, math, os, random, sys
import tabelas as T
import tabelas_bichos as TB
import luta, bichos
from pessoas import padrao, veste
from itens import item

AQUI = os.path.dirname(os.path.abspath(__file__))
ARQ = os.path.join(AQUI, 'dados', 'conta_pesos.json')
PESOS_PADRAO = [0.0, 1.0, 0.3, -0.3, 0.3, 0.3, 0.2, 0.1] + [0.0] * 18
_PESOS = None


def pesos():
    global _PESOS
    if _PESOS is None:
        try: _PESOS = json.load(open(ARQ, encoding='utf-8'))['pesos']
        except (OSError, ValueError, KeyError): _PESOS = list(PESOS_PADRAO)
    return _PESOS


def _perfil(f):
    """o que pesa de um lutador (já montado pela luta: luta.nova)"""
    arma = f.get('arma') if isinstance(f.get('arma'), dict) else None
    atk = arma.get('cat', 0) if arma else 0
    if f.get('feiticos') and f.get('foco_cat') is not None: atk = max(atk, f['foco_cat'])
    tr = (f.get('partes') or {}).get('tronco'); arm = tr['cat'] if isinstance(tr, dict) else -1
    esc = (f.get('escudo') or {}).get('bonus', 0) if isinstance(f.get('escudo'), dict) else 0
    return dict(atk=atk, arm=arm, pv=max(1, f.get('pv', f.get('pvmax', 1))), df=f.get('def_fixa', 20) + esc, ma=f.get('maestria', 0) or 0, fo=f.get('forca_b', 5) or 5,
                tr=set(f.get('tracos') or []), oc=f.get('ocupa', 1) or 1, tras=f.get('linha') == 'trás' or (arma or {}).get('distancia', False), acesa=_acesa(f, arma))


# (fase 2) os pontos da acesa por grau no duelo de iguais (I·Ap·Ad·P·M·GM): os do banco (o duelo da HB1, medido no conserto da fase 2 com 40.000 lutas por grau, mais preciso que
# a HB1 de 8.000; o Rito de Veia do Perito ao GM, a média de três sementes). A Roda é a que 6.7 manda remedir: o banco fica no lugar do rascunho. Sem a chave, os do contrato (medido).
ACESA_PONTOS = dict(roda=(4.5, 6.2, 10.4, 15.6, 17.9, 24.5), sanha=(4.0, 5.3, 8.7, 10.9, 13.1, 15.8), rito_veia=(0.6, 6.2, 9.7, 16.0, 20.2, 20.7))


def _acesa(f, arma):
    """(fase 2) os pontos de vitória da melhor habilidade acesa de luta que o lutador traz (a Roda só com arma de peso: impacto, que não é o punho), ou 0"""
    hb = f.get('hab') or {}
    if not hb: return 0.0
    import tabelas_habilidades as HT
    out = 0.0
    for k in HT.ACESAS:
        if k not in hb or HT.HABILIDADES[k].get('medido') is None: continue
        if k == 'roda' and not (arma and arma.get('golpe') == 'impacto' and arma.get('dado') != '1d4'): continue
        out = max(out, (ACESA_PONTOS.get(k) or HT.HABILIDADES[k]['medido'])[max(0, min(5, hb[k]))])
    return out


def _logit_acesa(L):
    """a média, no lado, da vitória a mais da acesa em logit (+16,9 pontos: de 50% a 66,9%)"""
    return sum(math.log((50 + x['acesa']) / (50 - x['acesa'])) for x in L if x.get('acesa')) / len(L) if L else 0.0


TRACOS_PESAM = ('sopro', 'veneno', 'regenera', 'apavora', 'voa', 'couraça', 'matilha', 'bote', 'agarra', 'investida', 'sem vida', 'imaterial', 'dreno', 'resiste')


def _lados(A, B):
    """monta a luta (sem rodar) e tira os perfis dos dois lados"""
    S = luta.nova(A, B, quieto=True)
    pa = [_perfil(f) for f in S['L'] if f['lado'] == 'A']; pb = [_perfil(f) for f in S['L'] if f['lado'] == 'B']
    return pa, pb


def _tempo(atk, alvo):
    """o log do tempo que um lado leva para derrubar o outro: o PV do alvo sobre o dano do lado (o dano: a força vezes o triplo por categoria da arma contra a armadura média do alvo)"""
    prot = sum(3 ** x['arm'] for x in alvo) / len(alvo)
    dano = sum(max(1, x['fo'] + 4) * (3 ** x['atk']) / prot for x in atk)
    return math.log(sum(x['pv'] for x in alvo) / dano)


def traços(pa, pb):
    """os traços da curva: o tempo de cada lado derrubar o outro (a regra de ouro: o triplo por categoria), a diferença de categoria, quantos são, a defesa, a mão, a força"""
    m = lambda L, k: sum(x[k] for x in L) / len(L)
    t = _tempo(pb, pa) - _tempo(pa, pb); da = m(pa, 'atk') - m(pb, 'arm'); db = m(pb, 'atk') - m(pa, 'arm')
    tr = [sum(1 for x in pb if k in x['tr']) / len(pb) - sum(1 for x in pa if k in x['tr']) / len(pa) for k in TRACOS_PESAM]      # o traço do outro lado pesa contra; o meu, a favor
    return [1.0, t, da, db, math.log(len(pa) / len(pb)), (m(pa, 'df') - m(pb, 'df')) / 10, (m(pa, 'ma') - m(pb, 'ma')) / 4, (m(pa, 'fo') - m(pb, 'fo')) / 5,
            t * abs(t) / 4, da * db / 4, (m(pa, 'oc') - m(pb, 'oc')), sum(x['tras'] for x in pa) / len(pa) - sum(x['tras'] for x in pb) / len(pb)] + tr


def chance_perfis(pa, pb, w=None):
    """a chance do lado A vencer (de 0 a 1), pelos perfis"""
    w = w or pesos(); z = sum(a * b for a, b in zip(w, traços(pa, pb)))
    if any(x.get('acesa') for x in pa + pb): z += _logit_acesa(pa) - _logit_acesa(pb)      # (fase 2) a acesa por cima da curva
    return 1 / (1 + math.exp(-max(-30, min(30, z))))


def chance(A, B, w=None):
    """a chance do lado A (lista de lutadores: pessoas.padrao vestidas, estado.lutador, bichos.bando) vencer o lado B"""
    pa, pb = _lados(A, B); return chance_perfis(pa, pb, w)


# ---------- afinar: os casos ao acaso, as lutas de verdade ----------
ESPECIES = None
def _especies():
    global ESPECIES
    if ESPECIES is None:
        import tabelas_criaturas as TC
        ESPECIES = [k for k, e in TB.ESPECIES.items() if not e.get('chefe')] + [k for k in TC.ESPECIES]
    return ESPECIES


def pessoa_ao_acaso(r, nome, cat=None):
    cat = r.randint(0, 5) if cat is None else cat; niv = r.choice([5, 8, 12, 20, 30, 45, 60, 90, 130, 180])
    molde = r.choice(['guerreiro', 'guerreiro', 'arqueiro']); fam = 'arco' if molde == 'arqueiro' else r.choice(['espada', 'machado', 'lança', 'maça', 'montante'])
    p = padrao(nome, niv, molde=molde)
    ca = max(0, min(7, cat + r.choice([-1, 0, 0, 1]))); cr = max(0, min(7, cat + r.choice([-1, 0, 0, 1])))
    esc = max(0, cr - 1) if fam in ('espada', 'machado', 'lança', 'maça') and r.random() < 0.6 else None
    return veste(p, arma=item('arma', ca, familia=fam), armadura=item('armadura', cr, material=r.choice(['couro', 'malha', 'placa'])), escudo=esc)


def caso(r):
    """um caso ao acaso: um grupo de 1 a 4 contra um bando de bichos ou criaturas (ou, às vezes, contra outro grupo de gente)"""
    cat = r.randint(0, 5); A = [pessoa_ao_acaso(r, f'a{i}', cat) for i in range(r.choice([1, 1, 2, 2, 3, 4]))]
    if r.random() < 0.25: B = [pessoa_ao_acaso(r, f'b{i}', max(0, min(5, cat + r.choice([-1, 0, 1])))) for i in range(r.choice([1, 1, 2, 3]))]
    else:
        esp = r.choice(_especies()); e = bichos.especie(esp); lo, hi = e['bando']; n = r.randint(lo, max(lo, hi)) * r.choice([1, 1, 2])
        B = bichos.bando(esp, r, n=n)
    return A, B


def mede(A, B, k=24):
    import copy
    v = 0
    for _ in range(k):
        S = luta.nova(copy.deepcopy(A), copy.deepcopy(B), quieto=True); luta.corre(S, interativo=False); v += S['fim'] == 'A'
    return v / k


def afina(n=900, semente=11, k=48):
    r = random.Random(semente); dados = []
    for i in range(n):
        A, B = caso(r); pa, pb = _lados(A, B); dados.append((traços(pa, pb), mede(A, B, k)))
    w = [0.0] * len(dados[0][0])
    for it in range(6000):                                  # a curva pela verossimilhança (a descida do gradiente, devagar)
        g = [0.0] * len(w); taxa = 0.3 if it < 3000 else 0.1
        for x, y in dados:
            z = sum(a * b for a, b in zip(w, x)); p = 1 / (1 + math.exp(-max(-30, min(30, z))))
            for j in range(len(w)): g[j] += (y - p) * x[j]
        w = [a + taxa * b / len(dados) for a, b in zip(w, g)]
    erro = sum(abs(chance_perfis_x(x, w) - y) for x, y in dados) / len(dados)
    json.dump(dict(pesos=w, casos=n, erro_afinado=erro), open(ARQ, 'w', encoding='utf-8'), indent=1)
    global _PESOS; _PESOS = w
    return w, erro


def chance_perfis_x(x, w): z = sum(a * b for a, b in zip(w, x)); return 1 / (1 + math.exp(-max(-30, min(30, z))))


def confere(n=300, semente=97, k=120):
    """o erro da curva contra a luta de verdade, em casos novos. Cada caso roda k lutas (o acaso das k lutas também erra: com 120, uns 3 a 4 pontos em média)"""
    r = random.Random(semente); erros = []
    for i in range(n):
        A, B = caso(r); erros.append(abs(chance(A, B) - mede(A, B, k)))
    return sum(erros) / len(erros), sorted(erros)[int(len(erros) * 0.9)]


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a or a[0] not in ('afina', 'confere'): print(__doc__); sys.exit()
    n = int(a[1]) if len(a) > 1 and a[1].isdigit() else (900 if a[0] == 'afina' else 300)
    if a[0] == 'afina': w, e = afina(n); print(f"pesos: {[round(x, 3) for x in w]} · erro médio nos casos afinados: {e * 100:.1f} pontos")
    else: e, p90 = confere(n); print(f"erro médio da conta rápida contra o luta.py: {e * 100:.1f} pontos (90% dos casos até {p90 * 100:.1f}) em {n} casos novos")
