#!/usr/bin/env python3
"""teste.py — MOTOR 10: O DADO DE QUEM ESTÁ EM CENA. Declarado ANTES, rolado UMA VEZ, e fica escrito no turno.

  2d20 (cada 20 rola de novo e soma) + o bônus do atributo (atributo ÷ 10) + a pena do corpo + o que mais somar, contra um número.
  Não existe rolar de novo: o comando declara e rola no mesmo passo, e o resultado vai para o caderno do turno.
  O DOM ESCONDIDO (etapa da magia; talento.py): o módulo que rola passa `dom=` com o dom que a pessoa ainda não viu. Ele entra no total; a mesa só o vê quando decidiu
  ("sem o dom, não passava"): senão a mesa vê o total sem ele, e o veredito é o mesmo. O Mestre vê sempre.

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


def rola(E, o_que, atributo, contra, mais=0, quem=None, oculto=False, dom=0, rotulo=None):
    """`rotulo`: quando o bônus do atributo e o `mais` são, juntos, uma conta só (a Conjuração da fé, no rito), a mesa vê a soma com esse nome ("+10 de Conjuração da fé"),
    e não o atributo inteiro com o resto à parte. O total não muda."""
    pid = quem or estado.eu(E); p = E['gente'].get(pid) or sys.exit(f'não há a pessoa "{pid}"')
    if atributo not in T.ATRIBUTOS: sys.exit(f'atributo desconhecido: "{atributo}" (use: {", ".join(T.ATRIBUTOS)})')
    if p['estado'] != 'vivo': sys.exit(f"{p['nome']} não testa nada: {estado.morte_diz(E, p)}")
    estado.em_cena(E, pid); p = E['gente'][pid]             # quem não é o personagem e volta a agir: antes de mais nada, o descanso em casa (a pena do corpo é a de agora)
    a, b = d20x(), d20x(); bonus = p['atributos'][atributo] // 10; pena = corpo.pena(p, estado.agora(E))
    total = sum(a) + sum(b) + bonus + pena + mais + dom
    r = dict(n=len(E['turno']['dados']) + 1, dia=E['relogio']['dia'], bloco=E['relogio']['bloco'], quem=pid, o_que=o_que, atributo=atributo, dados=[a, b],
             bonus=bonus, pena=pena, mais=mais, total=total, contra=contra, passou=total >= contra, oculto=bool(oculto))
    if rotulo: r['rotulo'] = rotulo
    if dom: r['dom'] = dom; r['fez'] = total >= contra and total - dom < contra       # o dom escondido: fez passar? (o teste de três faixas, quem chama acerta r['fez'])
    E['turno']['dados'].append(r)
    return r


def total_visto(r):
    """o total como a mesa o vê: sem o dom escondido que não decidiu"""
    d = r.get('dom') or 0
    return r['total'] if not d or r.get('fez') else r['total'] - d


def diz(E, r, mestre=False):
    if r['oculto'] and not mestre: return f"#{r['n']} rolagem oculta ({r['o_que']})"
    p = E['gente'][r['quem']]; partes = f"{'+'.join(map(str, r['dados'][0]))} e {'+'.join(map(str, r['dados'][1]))}, "
    if r.get('rotulo'): partes += f"{r['bonus'] + r['mais']:+d} de {r['rotulo']}".replace('-', '−')       # a conta inteira com o nome dela (o atributo já está dentro)
    else: partes += f"+{r['bonus']} de {r['atributo']}"
    if r['pena']: partes += f", −{-r['pena']} do corpo"
    if r['mais'] and not r.get('rotulo'): partes += f", {r['mais']:+d}".replace('-', '−')
    d = r.get('dom') or 0; mostra = bool(d) and (mestre or bool(r.get('fez')))
    if mostra: partes += f", +{d} do dom" + ('' if r.get('fez') else ' (escondido: não decidiu)')
    fez = f" (sem o dom, {'saía pior' if r.get('fez') == 'faixa' else 'não passava'})" if d and r.get('fez') else ''
    return f"#{r['n']} {p['nome']}, {r['o_que']}: {partes} = {r['total'] if mostra else total_visto(r)} contra {r['contra']}: {'PASSA' if r['passou'] else 'FALHA'}" + fez + (' (OCULTA)' if r['oculto'] else '')


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
