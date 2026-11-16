#!/usr/bin/env python3
"""julgamento.py — O JULGAMENTO DO REI como procedimento (MOTOR 6.4; regra nova): julgamentos.json.
Um caso tem acusador, réu, a lei invocada, PROVAS e TESTEMUNHAS dos dois lados. Cada prova pesa de 1 a 3. Cada testemunha
fala diante de todos e rola d20 (+2 se é gente de nome; −2 se tem interesse no caso): até 5 SE DESMENTE (peso 0) ·
6-15 vale o peso · 16+ COMOVE a praça (peso +1). A BALANÇA é a soma da acusação menos a da defesa:
  +2 ou mais: a praça espera CONDENAÇÃO · −2 ou menos: espera ABSOLVIÇÃO · no meio: a praça está DIVIDIDA.
A SENTENÇA é do rei (ou do conselho, por conselho.py). O que ela custa ou rende:
  sentença do lado da balança: legitimidade +1 · contra a balança: legitimidade −1 (−2 se absolve gente da casa contra a prova)
  praça dividida: nada na legitimidade; o lado que perde guarda mágoa (o Mestre abre um fio)
  réu da casa condenado: lealdade −2 dele · réu da casa absolvido com justiça: lealdade +1 dele
  pena de MORTE ou de EXÍLIO pesa em dobro para os dois lados
Uso:
  python3 julgamento.py abre ID "o caso" acusador="NOME" reu="NOME[,NOME]" lei="a lei invocada"
  python3 julgamento.py prova ID acusacao|defesa PESO "o que é"
  python3 julgamento.py testemunha ID acusacao|defesa PESO "NOME" [nome] [interesse]
  python3 julgamento.py ver [ID]
  python3 julgamento.py sentenca ID culpado|inocente|meio "a pena ou o acordo" [morte|exilio] [casa]
"""
import sys
from nucleo import d, carrega, grava, anota, dia_atual
ARQ = 'julgamentos.json'


def balanca(J):
    ac = sum(x['peso'] for x in J['itens'] if x['lado'] == 'acusacao'); de = sum(x['peso'] for x in J['itens'] if x['lado'] == 'defesa')
    b = ac - de
    return ac, de, b, ('CONDENAÇÃO' if b >= 2 else 'ABSOLVIÇÃO' if b <= -2 else 'DIVIDIDA')


def ver(J):
    ac, de, b, esp = balanca(J)
    print(f"JULGAMENTO ({J['id']}) {J['caso']} · acusa: {J['acusador']} · réu: {J['reu']} · lei: {J['lei']} · {J['estado']}")
    for x in J['itens']:
        print(f"   [{x['lado']}] peso {x['peso']} · {x['txt']}")
    print(f"   BALANÇA: acusação {ac} − defesa {de} = {b:+d} → a praça espera {esp}" + (f" · SENTENÇA: {J['sentenca']}" if J.get('sentenca') else ''))


def main():
    a = sys.argv[1:]; T = carrega(ARQ, {'casos': {}}); dia = dia_atual()
    if not a or a[0] == 'ver':
        for J in T['casos'].values():
            if len(a) < 2 or J['id'] == a[1]: ver(J)
        if not T['casos']: print('nenhum julgamento aberto.')
        return
    if a[0] == 'abre' and len(a) > 2:
        op = {x.split('=')[0]: x.split('=', 1)[1] for x in a[3:] if '=' in x}
        T['casos'][a[1]] = {'id': a[1], 'caso': a[2], 'acusador': op.get('acusador', '?'), 'reu': op.get('reu', '?'), 'lei': op.get('lei', '?'), 'dia': dia, 'estado': 'aberto', 'itens': []}
        grava(ARQ, T); anota(f"- JULGAMENTO ABERTO ({a[1]}) [Dia {dia}]: {a[2]} · acusa {op.get('acusador')} · réu {op.get('reu')} · lei: {op.get('lei')}"); ver(T['casos'][a[1]]); return
    J = T['casos'].get(a[1]) if len(a) > 1 else None
    if not J: sys.exit('caso não achado. ' + __doc__)
    if a[0] == 'prova' and len(a) > 4:
        J['itens'].append({'lado': a[2], 'peso': max(1, min(3, int(a[3]))), 'txt': 'PROVA: ' + a[4]})
        grava(ARQ, T); anota(f"- JULGAMENTO ({J['id']}) prova da {a[2]}, peso {a[3]}: {a[4]}"); ver(J)
    elif a[0] == 'testemunha' and len(a) > 4:
        mod = (2 if 'nome' in a[5:] else 0) - (2 if 'interesse' in a[5:] else 0); r = d(20); t = r + mod; p = max(1, min(3, int(a[3])))
        vale, como = (0, 'SE DESMENTE diante de todos') if t <= 5 else (p, 'fala firme') if t <= 15 else (p + 1, 'COMOVE a praça')
        J['itens'].append({'lado': a[2], 'peso': vale, 'txt': f'TESTEMUNHA {a[4]}: d20 [{r}]{mod:+d} = {t} → {como}'})
        grava(ARQ, T); anota(f"- JULGAMENTO ({J['id']}) testemunha da {a[2]}, {a[4]}: d20 [{r}]{mod:+d} = {t} → {como} (peso {vale})"); ver(J)
    elif a[0] == 'sentenca' and len(a) > 3:
        ac, de, b, esp = balanca(J); v = a[2]; dobro = 2 if ('morte' in a[4:] or 'exilio' in a[4:]) else 1; casa = 'casa' in a[4:]
        if esp == 'DIVIDIDA': leg, porque = 0, 'a praça estava dividida: metade aceita, metade guarda mágoa'
        elif (esp == 'CONDENAÇÃO' and v == 'culpado') or (esp == 'ABSOLVIÇÃO' and v == 'inocente'): leg, porque = 1, 'a sentença foi a que a praça esperava'
        elif v == 'meio': leg, porque = 0, 'o meio-termo não agrada nem ofende'
        else: leg, porque = (-2 if (casa and v == 'inocente') else -1) * dobro, 'a sentença foi contra o que a praça viu' + (' e o rei protegeu os seus' if casa and v == 'inocente' else '')
        J['estado'] = 'julgado'; J['sentenca'] = f'{v.upper()}: {a[3]}'; grava(ARQ, T)
        print(f"SENTENÇA ({J['id']}): {v.upper()} — {a[3]} · a praça esperava {esp} ({b:+d}) → legitimidade {leg:+d} ({porque})")
        if leg: print(f'   → python3 reino.py legit {leg:+d} "julgamento {J["id"]}"')
        if casa: print(f"   → réu da casa: python3 npc.py lealdade NOME {'-2' if v == 'culpado' else '+1'} \"julgamento {J['id']}\"")
        anota(f"- SENTENÇA ({J['id']}) [Dia {dia}]: {v.upper()} — {a[3]} · balança {b:+d} ({esp}) → legitimidade {leg:+d} ({porque})")
    else: print(__doc__)


if __name__ == '__main__':
    main()
