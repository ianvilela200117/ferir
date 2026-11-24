"""m9: a conta exata de ROUBAR O TESOURO de um dragão que dorme (a regra proposta: a vigília do dragão; o teste do ladrão é o do projeto A, aqui um bônus genérico).
O dado do motor: 2d20, e cada 20 rola de novo e soma (teste.rola). Calcula a chance por bloco e o que o ladrão leva em média antes de o dragão acordar."""
from functools import lru_cache

def d20x():
    """a distribuição de um d20 que explode (corta em 3 explosões: o resto é menor que 1 em 8.000)"""
    out = {}
    for a in range(1, 20): out[a] = out.get(a, 0) + 1 / 20
    for b in range(1, 20): out[20 + b] = out.get(20 + b, 0) + 1 / 400
    for c in range(1, 21): out[40 + c] = out.get(40 + c, 0) + 1 / 8000
    return out
D = d20x()
DD = {}
for a, pa in D.items():
    for b, pb in D.items(): DD[a + b] = DD.get(a + b, 0) + pa * pb
def passa(bonus, contra): return sum(p for s, p in DD.items() if s + bonus >= contra)

VIG = 22; SOBE = 2; PUNHADO = 100
DRAGAO = {'jovem': 75, 'adulto': 85, 'velho': 90, 'ancião': 90}      # a Percepção
print(f'a vigília do dragão que dorme: {VIG} + Percepção ÷ 10, e +{SOBE} a cada bloco de garimpo no mesmo sono; cada bloco que passa leva um punhado ({PUNHADO} de prata, ou uma peça)')
for ladrao, bon in (('Agilidade 60, sem mão de ladino (+6)', 6), ('Agilidade 70, Iniciante (+9)', 9), ('Agilidade 70, Treinado (+11)', 11), ('Agilidade 80, Mestre (+14)', 14), ('o mesmo, sem luz e vendo no escuro (+16)', 16)):
    L = []
    for idade, per in DRAGAO.items():
        v = VIG + per // 10; ps = [passa(bon, v + SOBE * k) for k in range(30)]
        esp = 0; viva = 1
        for p in ps: viva *= p; esp += viva           # blocos que passam, em média, se ele segue até acordar o dragão
        um = ps[0]; dois = ps[0] * ps[1]
        L.append(f"{idade}: 1º bloco {100 * um:.0f}% · 2 seguidos {100 * dois:.0f}% · leva em média {esp * PUNHADO:.0f}")
    print(f'  {ladrao:<42} ' + ' | '.join(L))
