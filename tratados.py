#!/usr/bin/env python3
"""tratados.py — os ACORDOS do reino como contratos que o motor cobra (MOTOR 6.4): tratados.json.
Cada tratado tem com quem, o texto, o estado (proposto, vigente, rompido, cumprido) e CLÁUSULAS: quem deve (nos ou eles), o quê,
e de quanto em quanto tempo (a_cada=7) ou até quando (ate=DIA). Na semana, o tick mostra o que vence. Para cada cláusula DELES
que vence, d20 + a relação do reino com eles: até 4 FALHAM (atrasam, mandam menos ou não mandam) · 5+ cumprem.
Cláusula NOSSA que vence aparece como cobrança: cumprir (tratados.py pago) ou deixar passar (a relação cai).
Uso:
  python3 tratados.py ver
  python3 tratados.py novo ID "COM QUEM" "o texto do acordo" [vigente]
  python3 tratados.py clausula ID nos|eles "o quê" a_cada=N | ate=DIA
  python3 tratados.py estado ID vigente|rompido|cumprido|proposto "motivo"
  python3 tratados.py pago ID N            a cláusula N (nossa) foi cumprida neste período
  python3 tratados.py semana DIA           o que vence (o tick semanal chama)
"""
import sys
from nucleo import d, carrega, grava, anota, dia_atual, acha_nome
ARQ = 'tratados.json'


def ver(T):
    for t in T['tratados'].values():
        print(f"({t['id']}) {t['com']} · {t['estado'].upper()} · {t['texto']}")
        for i, c in enumerate(t['clausulas'], 1):
            quando = f"a cada {c['a_cada']} dias (próxima: Dia {c['proxima']})" if c.get('a_cada') else f"até o Dia {c.get('ate')}"
            print(f"     {i}. {'NÓS devemos' if c['quem'] == 'nos' else 'ELES devem'}: {c['o_que']} · {quando}" + (' · feito' if c.get('feito') else ''))
    if not T['tratados']: print('nenhum tratado.')


def main():
    a = sys.argv[1:]; T = carrega(ARQ, {'tratados': {}}); dia = dia_atual()
    if not a or a[0] == 'ver': ver(T); return
    if a[0] == 'novo' and len(a) > 3:
        T['tratados'][a[1]] = {'id': a[1], 'com': a[2], 'texto': a[3], 'estado': 'vigente' if 'vigente' in a[4:] else 'proposto', 'desde': dia, 'clausulas': [], 'log': []}
        grava(ARQ, T); print(f"tratado {a[1]} com {a[2]}: {T['tratados'][a[1]]['estado']}"); anota(f"- TRATADO ({a[1]}) [Dia {dia}] com {a[2]}: {a[3]}"); return
    if a[0] == 'semana':
        dia = int(a[1]) if len(a) > 1 else dia; R = carrega('reino.json'); rel = R.get('reino', {}).get('relacoes', {}); n = 0
        print('  OS TRATADOS (o que vence):')
        for t in T['tratados'].values():
            if t['estado'] != 'vigente': continue
            for i, c in enumerate(t['clausulas'], 1):
                vence = (c.get('a_cada') and c['proxima'] <= dia) or (c.get('ate') and c['ate'] <= dia and not c.get('feito'))
                if not vence: continue
                n += 1
                if c['quem'] == 'eles':
                    k, _ = acha_nome(t['com'].split()[-1], rel); bonus = rel.get(k, 0) if k else 0; r = d(20)
                    ok = r + bonus >= 5
                    print(f"   ({t['id']}) {t['com']} deve: {c['o_que']} → d20 [{r}]{bonus:+d} → " + ('CUMPRE (lançar o que chegou: ficha.py mat ou cofre)' if ok else 'FALHA: atrasa, manda menos ou não manda (o Mestre mostra; a relação pode cair: reino.py rel)'))
                    t['log'].append(f"{dia}: eles, cláusula {i}: [{r}]{bonus:+d} {'cumprem' if ok else 'FALHAM'}")
                else:
                    print(f"   ({t['id']}) NÓS devemos a {t['com']}: {c['o_que']} → cumprir e marcar (tratados.py pago {t['id']} {i}), ou a relação cai")
                if c.get('a_cada'): c['proxima'] += c['a_cada']
                else: c['feito'] = c['quem'] == 'eles'
        if not n: print('   nada vence nesta semana.')
        prop = [f"{t['com']} ({t['id']})" for t in T['tratados'].values() if t['estado'] == 'proposto']
        if prop: print('   à espera de começar: ' + ' · '.join(prop))
        grava(ARQ, T); return
    t = T['tratados'].get(a[1]) if len(a) > 1 else None
    if not t: sys.exit('tratado não achado. ' + __doc__)
    if a[0] == 'clausula' and len(a) > 4:
        op = {x.split('=')[0]: int(x.split('=')[1]) for x in a[4:] if '=' in x}
        c = {'quem': a[2], 'o_que': a[3]}
        if 'a_cada' in op: c['a_cada'] = op['a_cada']; c['proxima'] = dia + op['a_cada']
        else: c['ate'] = op.get('ate', dia + 30)
        t['clausulas'].append(c); grava(ARQ, T); print(f"cláusula {len(t['clausulas'])} em {t['id']}: {a[2]} · {a[3]}")
    elif a[0] == 'estado' and len(a) > 2:
        t['estado'] = a[2]; t['log'].append(f"{dia}: {a[2]} ({a[3] if len(a) > 3 else ''})")
        if a[2] == 'vigente':
            for c in t['clausulas']:
                if c.get('a_cada'): c['proxima'] = dia + c['a_cada']
        grava(ARQ, T); print(f"{t['id']}: {a[2]}"); anota(f"- TRATADO ({t['id']}) [Dia {dia}] com {t['com']}: {a[2].upper()} ({a[3] if len(a) > 3 else ''})")
    elif a[0] == 'pago' and len(a) > 2:
        c = t['clausulas'][int(a[2]) - 1]; c['feito'] = True; t['log'].append(f'{dia}: nós cumprimos a cláusula {a[2]}'); grava(ARQ, T); print('marcado como cumprido.')
    else: print(__doc__)


if __name__ == '__main__':
    main()
