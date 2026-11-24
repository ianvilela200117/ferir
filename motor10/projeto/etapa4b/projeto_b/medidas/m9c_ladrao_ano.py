"""m9c: o ladrão robô num ano ao lado do covil (a regra proposta; o teste de A). A cada sono do dragão ele entra uma vez, no escuro, e tira UM punhado (a sexta parte da prata
que havia quando o dragão dormiu) e sai. Falhou o teste: o dragão acorda na sala do tesouro, e o ladrão sozinho morre (um homem do degrau vence o jovem 0,5%: medido).
O tesouro cresce pela vida do dragão (o jovem ataca a aldeia: +5 a 20 por ataque; o adulto cobra 3% por estação de uma vila de 2.000)."""
import random, sys
sys.path.insert(0, '.')
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()): from m9_roubo import passa
def vida(idade, bon, r):
    per = {'jovem': 75, 'adulto': 85}[idade]; dorme = {'jovem': (20, 40), 'adulto': (30, 60)}[idade]
    tes = {'jovem': 300, 'adulto': 1500}[idade]; dia = 0; levou = 0; vila = 2000; punhados = 0
    while dia < 364:
        p = passa(bon, 20 + per // 10 + 2)          # o primeiro punhado do sono
        if r.random() >= p: return levou, dia, True, punhados
        q = tes // 6; tes -= q; levou += q; punhados += 1
        dia += r.randint(*dorme)
        if idade == 'jovem': g = r.randint(5, 20); tes += g
        else: g = int(vila * 0.03) if (dia // 91) != ((dia - 45) // 91) else 0; vila -= g; tes += g
    return levou, 364, False, punhados
for idade in ('jovem', 'adulto'):
    for rot, bon in (('Treinado, no escuro (+12)', 12), ('Mestre, no escuro (+14)', 14)):
        r = random.Random(1); V = [vida(idade, bon, r) for _ in range(20000)]
        mortos = sum(v[2] for v in V) / len(V); dias = sum(v[1] for v in V); levou = sum(v[0] for v in V)
        print(f'  {idade:<7} ladino {rot:<26}: morre no ano em {mortos:.0%} das vidas; leva em média {levou / len(V):.0f} de prata ({sum(v[3] for v in V) / len(V):.1f} punhados); por dia de vida, {levou / dias:.2f} de prata (a diária é 4)')
