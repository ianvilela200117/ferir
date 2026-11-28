#!/usr/bin/env python3
"""caixa.py — MOTOR 10, ETAPA FINAL: A CAIXA DE ENTRADA DO PERSONAGEM. O que toca o personagem chega como pedido com prazo: {de, pede, prazo, opções, padrão}.
Só escreve quem tem motivo no estado (o ferreiro sem matéria, o parente com fome, o capitão contra a frente...). Cabem 7; o oitavo força o mais velho.
VENCIDO O PRAZO, VALE O PADRÃO, sempre com custo (quem pediu lembra que você calou; o cliente vai ao rival). Calar tem preço escrito.

  python3 caixa.py ver                    os pedidos abertos, por prazo (o que cada opção faz, e o padrão)
  python3 caixa.py responde XID LETRA     o jogador escolheu: vale a opção (os efeitos dela, num evento só); a opção que não cabe mais é recusada
  python3 caixa.py pergunta XID           abre a pergunta do turno ligada ao pedido (o `turno.py fecha` recusa fechar com pedido vencendo amanhã sem pergunta ligada)
(A PARTE 2, FASE 2: o pedido de quem tem nome se NEGOCIA pelo teste de fala, no pedido que o jogador declara: `fala.py caixa XID prazo|paga [DEGRAU]` (mais prazo: pequeno, +2 dias;
mais paga: médio +25%, grande +50%). Ganhar muda o pedido; perder deixa como era. O capítulo 30.)
"""
import sys
import tabelas_mundo as M
import tabelas_regiao as R
import estado


def tem(E): return bool((E.get('mundo') or {}).get('meta'))
def abertos(E): return sorted(((k, x) for k, x in (E['mundo'].get('caixa') or {}).items() if x.get('fim') is None), key=lambda kx: (kx[1]['prazo'], kx[0]))


def nova(E, de, pede, prazo, opcoes, efeitos, padrao, motivo='', tipo='caixa', mais=()):
    """põe um pedido na caixa (um evento). `efeitos`: {letra: [efeitos]} (o que cada escolha faz; o padrão é o que vale se ninguém responder).
    Se a caixa está cheia, o mais velho vence antes, pelo padrão dele. Devolve o id do pedido, ou None (sem personagem vivo, ou sem região)."""
    eu = estado.eu(E)
    if not tem(E) or not eu or E['gente'][eu]['estado'] != 'vivo': return None
    ab = abertos(E)
    while len(ab) >= M.CAIXA_MAX: vence(E, ab[0][0], forcado=True); ab = abertos(E)
    W = E['mundo']; n = ((W.get('seq') or {}).get('caixa') or 0) + 1; xid = f'cx{n:04d}'
    reg = dict(de=de, pede=pede, prazo=prazo, opcoes=dict(opcoes), efeitos={k: list(v) for k, v in efeitos.items()}, padrao=padrao, motivo=motivo, desde=E['relogio']['dia'], fim=None)
    estado.aplica(E, tipo, [['mundo', 'seq', 'caixa', 'soma', 1], ['mundo', 'caixa', xid, 'poe', reg]] + list(mais), onde=E['gente'][eu]['lugar'], quem=[eu],
                  texto=f"pedido na caixa ({xid}): {_de_quem(E, de)} pede {pede} (até o Dia {prazo})")
    return xid


def _de_quem(E, de):
    if de in E['gente']: return E['gente'][de]['nome']
    if de in E['lugares']: return E['lugares'][de]['nome']
    return str(de)


def _aplica_opcao(E, xid, letra, tipo='caixa', porque=''):
    x = E['mundo']['caixa'][xid]; ef = list(x['efeitos'].get(letra) or []) + [['mundo', 'caixa', xid, 'fim', 'poe', letra]]
    return estado.aplica(E, tipo, ef, onde=E['gente'][estado.eu(E)]['lugar'] if estado.eu(E) else None, quem=[k for k in (estado.eu(E),) if k],
                         texto=f"o pedido {xid} ({_de_quem(E, x['de'])}: {x['pede']}): {x['opcoes'][letra]}" + (f" ({porque})" if porque else ''))


def responde(E, xid, letra):
    x = (E['mundo'].get('caixa') or {}).get(xid) or sys.exit(f'não há o pedido "{xid}" na caixa (`caixa.py ver`)')
    if x.get('fim') is not None: sys.exit(f'o pedido {xid} já se resolveu ({x["opcoes"][x["fim"]]})')
    if letra not in x['opcoes']: sys.exit(f'o pedido {xid} não tem a opção "{letra}" (tem: {", ".join(x["opcoes"])})')
    import io, contextlib
    try:
        with contextlib.redirect_stderr(io.StringIO()): _aplica_opcao(E, xid, letra)
    except SystemExit as e: sys.exit(f'a opção "{letra}" não cabe agora: {e}')
    return f"{xid}: {x['opcoes'][letra]} — feito."


def vence(E, xid, forcado=False):
    """o prazo venceu (ou a caixa encheu): vale o padrão. Se o padrão não cabe mais (faltou a prata, a coisa), vale só o custo dele na opinião."""
    x = E['mundo']['caixa'][xid]
    try: _aplica_opcao(E, xid, x['padrao'], porque='a caixa encheu: o mais velho vence' if forcado else 'o prazo venceu: vale o padrão')
    except SystemExit:
        ef = [y for y in (x['efeitos'].get(x['padrao']) or []) if y[:1] == ['pessoa'] and len(y) == 5 and y[2] == 'memoria'] + [['mundo', 'caixa', xid, 'fim', 'poe', x['padrao']]]
        estado.aplica(E, 'caixa', ef, texto=f"o pedido {xid} venceu: o padrão não cabia; fica o custo")


def virada(E):
    if not tem(E): return
    hoje = E['relogio']['dia']
    for xid, x in abertos(E):
        if x['prazo'] < hoje: vence(E, xid)


def pergunta(E, xid):
    import turno
    x = (E['mundo'].get('caixa') or {}).get(xid) or sys.exit(f'não há o pedido "{xid}"')
    if x.get('fim') is not None: sys.exit(f'o pedido {xid} já se resolveu')
    t = E['turno']
    if any(q.get('caixa') == xid for q in t['perguntas']): sys.exit(f'o pedido {xid} já está nas perguntas abertas')
    out = turno.pergunta(E, f"[{xid}] {_de_quem(E, x['de'])} pede {x['pede']} (prazo: Dia {x['prazo']}; calar vale \"{x['opcoes'][x['padrao']]}\")", [f"{k}={v}" for k, v in x['opcoes'].items()])
    t['perguntas'][-1]['caixa'] = xid
    return out


def linhas(E):
    ab = abertos(E); hoje = E['relogio']['dia']
    return [f"- {xid} · {_de_quem(E, x['de'])} pede {x['pede']} · prazo: Dia {x['prazo']} ({'HOJE' if x['prazo'] == hoje else 'amanhã' if x['prazo'] == hoje + 1 else f'em {x['prazo'] - hoje} dias'}) · "
            + ' · '.join(f"**{k})** {v}" for k, v in x['opcoes'].items()) + f" · calar: {x['padrao']}" + (f" · ({x['motivo']})" if x.get('motivo') else '') for xid, x in ab]


def mesa(E):
    if not tem(E) or not estado.eu(E): return []
    L = linhas(E)
    return ['**A caixa** (pedidos com prazo; `caixa.py pergunta XID` abre a pergunta; `caixa.py responde XID LETRA` cumpre):'] + L if L else []


def recusa_fecha(E):
    if not tem(E) or not estado.eu(E): return []
    hoje = E['relogio']['dia']; ligadas = {q.get('caixa') for q in E['turno']['perguntas']}
    return [f"o pedido {xid} da caixa vence {'hoje' if x['prazo'] <= hoje else 'amanhã'} e não está nas perguntas abertas: `caixa.py pergunta {xid}`" for xid, x in abertos(E) if x['prazo'] <= hoje + 1 and xid not in ligadas]


if __name__ == '__main__':
    import signal; hasattr(signal, 'SIGPIPE') and signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    a = sys.argv[1:]
    if not a or a[0] not in ('ver', 'responde', 'pergunta'): print(__doc__); sys.exit()
    E = estado.carrega()
    if a[0] == 'ver': print('\n'.join(linhas(E)) or 'a caixa está vazia.')
    elif a[0] == 'responde':
        if len(a) != 3: sys.exit('use: `caixa.py responde XID LETRA`')
        print(responde(E, a[1], a[2])); estado.grava(E)
    else:
        if len(a) != 2: sys.exit('use: `caixa.py pergunta XID`')
        print(pergunta(E, a[1])); estado.grava(E)
