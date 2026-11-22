# O PROTÓTIPO da revisão do Motor 10 (Dia 507). NÃO É REGRA: serve só para medir.
# Lê o luta.py de hoje e troca três coisas, em memória:
#   D1  ações = 1 + nível ÷ 100 (o Livro)
#   D2  a "mão da experiência" (nível ÷ 5 no dano) nunca passa do dano médio da própria arma
#   D3  aço contra aço: arma 2 ou mais categorias abaixo da armadura do alvo só fere no crítico
#       (as fichas trazem "arma_cat" e "arm_cat", de 0 = Comum a 7 = Primordial)
import pathlib
import types

NOVO_TOPO = '''DIV_AC=100
def acoes(nivel): return max(1,min(8,1+nivel//DIV_AC))
TETO_EXP=True
ACO=True
def media(dado):
    n,f=map(int,dado.split('d')); return n*(f+1)/2
def exp(x):
    e=x['nivel']//5
    return min(e,int(media(x['dado'])*x['mult'])) if TETO_EXP else e
def aco_fraco(at,al):
    return ACO and at.get('arma_cat') is not None and al.get('arm_cat') is not None and at['arma_cat']<=al['arm_cat']-2'''

TROCAS = [
    ("def acoes(nivel): return max(1,min(8,1+nivel//60))", NOVO_TOPO),
    ("+g['nivel']//5", "+exp(g)"),
    ("+M['nivel']//5", "+exp(M)"),
    ("{g['nivel']//5}", "{exp(g)}"),
    ("{M['nivel']//5}", "{exp(M)}"),
    ("if J['fum'] or (t<dfM and not crit) or (g.get('so20') and not crit):",
     "if J['fum'] or (t<dfM and not crit) or ((g.get('so20') or aco_fraco(g,M)) and not crit):"),
    ("if J['fum'] or (t<df and not crit): P(",
     "if J['fum'] or (t<df and not crit) or (aco_fraco(M,g) and not crit): P("),
    ("if not J2['fum'] and (t2>=M['df']+(OFF if DOIS else 0) or cr2):",
     "if not J2['fum'] and (cr2 or (t2>=M['df']+(OFF if DOIS else 0) and not aco_fraco(g,M))):"),
]


def monta():
    """devolve o módulo do protótipo (o luta.py de hoje com as três trocas)"""
    raiz = pathlib.Path(__file__).resolve().parents[2]
    s = (raiz / 'luta.py').read_text(encoding='utf-8')
    for a, b in TROCAS:
        assert a in s, 'o luta.py mudou; a troca não achou: ' + a[:70]
        s = s.replace(a, b)
    m = types.ModuleType('luta10')
    exec(compile(s, 'luta10 (protótipo)', 'exec'), m.__dict__)
    return m
