#!/usr/bin/env python3
"""teste.py — MOTOR 10: O DADO DE QUEM ESTÁ EM CENA. Declarado ANTES, rolado UMA VEZ, e fica escrito no turno.

  2d20 (cada 20 rola de novo e soma) + o bônus do atributo (atributo ÷ 10) + a pena do corpo + o que mais somar, contra um número.
  Não existe rolar de novo: o comando declara e rola no mesmo passo, e o resultado vai para o caderno do turno.

Uso:
  python3 teste.py "o que se tenta" ATRIBUTO contra=N [mais=N] [quem=ID] [oculto]
  python3 teste.py "arrombar a porta" Força contra=26
  python3 teste.py "notar a emboscada" Percepção contra=30 oculto      (a mesa só vê "rolagem oculta"; o resultado fica para o Mestre)
  python3 teste.py ver                                                  as rolagens deste turno (as ocultas, inclusive)
"""
import secrets, sys
import tabelas as T
import estado, corpo


def d20x():
    t = [secrets.randbelow(20) + 1]
    while t[-1] == 20: t.append(secrets.randbelow(20) + 1)
    return t


def rola(E, o_que, atributo, contra, mais=0, quem=None, oculto=False):
    pid = quem or estado.eu(E); p = E['gente'].get(pid) or sys.exit(f'não há a pessoa "{pid}"')
    if atributo not in T.ATRIBUTOS: sys.exit(f'atributo desconhecido: "{atributo}" (use: {", ".join(T.ATRIBUTOS)})')
    if p['estado'] != 'vivo': sys.exit(f"{p['nome']} não testa nada: {estado.morte_diz(E, p)}")
    estado.em_cena(E, pid); p = E['gente'][pid]             # quem não é o personagem e volta a agir: antes de mais nada, o descanso em casa (a pena do corpo é a de agora)
    a, b = d20x(), d20x(); bonus = p['atributos'][atributo] // 10; pena = corpo.pena(p)
    total = sum(a) + sum(b) + bonus + pena + mais
    r = dict(n=len(E['turno']['dados']) + 1, dia=E['relogio']['dia'], bloco=E['relogio']['bloco'], quem=pid, o_que=o_que, atributo=atributo, dados=[a, b],
             bonus=bonus, pena=pena, mais=mais, total=total, contra=contra, passou=total >= contra, oculto=bool(oculto))
    E['turno']['dados'].append(r)
    return r


def diz(E, r, mestre=False):
    if r['oculto'] and not mestre: return f"#{r['n']} rolagem oculta ({r['o_que']})"
    p = E['gente'][r['quem']]; partes = f"{'+'.join(map(str, r['dados'][0]))} e {'+'.join(map(str, r['dados'][1]))}, +{r['bonus']} de {r['atributo']}"
    if r['pena']: partes += f", −{-r['pena']} do corpo"
    if r['mais']: partes += f", {r['mais']:+d}".replace('-', '−')
    return f"#{r['n']} {p['nome']}, {r['o_que']}: {partes} = {r['total']} contra {r['contra']}: {'PASSA' if r['passou'] else 'FALHA'}" + (' (OCULTA)' if r['oculto'] else '')


if __name__ == '__main__':
    import signal; hasattr(signal, 'SIGPIPE') and signal.signal(signal.SIGPIPE, signal.SIG_DFL)      # a saída cortada (`| head`) acaba o comando calada, sem erro de programa: tudo já foi gravado antes de falar
    a = sys.argv[1:]
    if not a: print(__doc__); sys.exit()
    E = estado.carrega()
    if a[0] == 'ver':
        print('\n'.join(diz(E, r, mestre=True) for r in E['turno']['dados']) or '(nenhuma rolagem neste turno)'); sys.exit()
    op = dict(x.split('=', 1) for x in a if '=' in x); pos = [x for x in a if '=' not in x]
    if len(pos) < 2 or 'contra' not in op: sys.exit('diga o que se tenta, o atributo e contra que número: `python3 teste.py "arrombar a porta" Força contra=26`')
    def num(k, pad=None):
        v = op.get(k, pad)
        try: return int(v)
        except (TypeError, ValueError): sys.exit(f'"{k}=" pede um número inteiro (veio "{v}")')
    r = rola(E, pos[0], pos[1], num('contra'), mais=num('mais', 0), quem=op.get('quem'), oculto='oculto' in pos)
    estado.grava(E); print(diz(E, r))
