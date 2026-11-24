"""m9b: roubar o tesouro do dragão com o teste do projeto A (andar escondido: 2d20 + Agilidade ÷ 10 + manha − a armadura do tronco − 6 com luz no escuro),
contra a VIGÍLIA do dragão que proponho: 20 + Percepção ÷ 10 + 2 (o dragão dorme leve sobre o ouro, em vez do −6 de quem dorme) + 2 a cada punhado já tirado no mesmo sono.
Um punhado é um lance (20 minutos) e leva a sexta parte da prata da sala, ou uma peça (a regra de A). Compara com a vigília de A (dormindo: −6)."""
import sys
sys.path.insert(0, '.')
from m9_roubo import passa
PER = {'jovem': 75, 'adulto': 85, 'velho': 90, 'ancião': 90}
def conta(bon, base, sobe):
    esp = 0; viva = 1; seis = 1
    for k in range(6):
        p = passa(bon, base + sobe * k); viva *= p; esp += viva
    return esp, viva
for rot, bon in (('ladino Treinado de couro, no escuro (+12)', 12), ('o mesmo, com luz (+6)', 6), ('ladino Mestre de couro, no escuro (+14)', 14), ('pequenino Treinado no escuro (+14: o passo leve)', 14)):
    L = []
    for idade, per in PER.items():
        e, seis = conta(bon, 20 + per // 10 + 2, 2); eA, seisA = conta(bon, 20 + per // 10 - 6, 0)
        L.append(f'{idade}: {passa(bon, 22 + per // 10):.0%} no 1º, {e:.1f} punhados em média, os seis {seis:.0%} (com a regra de A: {eA:.1f} e {seisA:.0%})')
    print(f'  {rot:<48} ' + ' | '.join(L))
