#!/usr/bin/env python3
"""missoes.py — MOTOR 10, ETAPA FINAL: O QUADRO DE MISSÕES. Cada lugar de povo tem um quadro; quem tem motivo no estado põe a missão nele (o caçador contra os lobos,
o mercador que quer escolta, o senhor contra a frente, a guilda contra a masmorra) e paga da bolsa dele. Qualquer um pode cumprir: o personagem e os rivais.
A MISSÃO CONTRA A FRENTE, cumprida, tira um passo dela. Quem toma e não cumpre perde fama, e quem pediu lembra.

  python3 missoes.py ver                  o quadro do lugar do personagem e as missões que ele tomou
  python3 missoes.py toma MID             toma a missão (só no lugar do quadro dela)
  python3 missoes.py entrega MID          confere e cumpre: a entrega sai da carga; a caça, a limpeza, a morte e a escolta se conferem pelo que aconteceu; a paga sai da bolsa de quem pediu
  python3 missoes.py larga MID            larga a missão tomada (perde fama; quem pediu lembra)
Tipos: caça (matar N de uma espécie num ermo) · entrega (levar N de um bem a quem pediu) · limpar (a masmorra, até o chefe) · matar (o dono da frente, ou o chefe)
· escolta (levar alguém até um lugar) · investigar (abrir o que a frente esconde)
"""
import json, os, sys
import tabelas as T
import tabelas_mundo as M
import tabelas_regiao as R
import estado


def tem(E): return bool((E.get('mundo') or {}).get('meta'))
def todas(E): return E['mundo'].get('missoes') or {}
def abertas(E, lid=None): return {k: m for k, m in todas(E).items() if m['estado'] == 'aberta' and (lid is None or m['onde'] == lid)}


def _quem(E, de):
    return E['gente'][de]['nome'] if de in E['gente'] else E['lugares'][de]['nome'] if de in E['lugares'] else str(de)


def _bolsa(E, de):
    return E['gente'][de]['moedas'] if de in E['gente'] else E['lugares'][de]['estoque'].get('prata', 0) if de in E['lugares'] else 0


def texto(E, m):
    a = m.get('alvo'); t = m['tipo']
    if t == 'caça': return f"matar {estado.tantos(m['n'], (estado.especie(a) or {}).get('nome', a), (estado.especie(a) or {}).get('plural'))}" + (f" {estado.em(E, m['ermo'])}" if m.get('ermo') in E['lugares'] else '')
    if t == 'entrega': return f"trazer {m['n']} de {estado.nome_bem(a)} a {_quem(E, m['de'])}"
    if t == 'limpar': return f"limpar {E['lugares'][a]['nome'] if a in E['lugares'] else a}, até o chefe do fundo"
    if t == 'matar': return f"acabar com {m.get('nome_alvo') or a}"
    if t == 'escolta': return f"levar {_quem(E, m['quem_vai'])} até {E['lugares'][a]['nome'] if a in E['lugares'] else a}, vivo"
    if t == 'investigar': return f"descobrir o que há por trás {estado.de_nome(m.get('nome_alvo') or 'do mistério')}"
    return t


def posta(E, de, lid, tipo, alvo, n=1, paga=None, prazo=None, frente=None, ermo=None, quem_vai=None, nome_alvo=None, cat=0):
    """põe a missão no quadro (um evento "missao"), se há vaga e a mesma ainda não está lá. A paga é da bolsa de quem pede (até 60% dela). Devolve o id, ou None."""
    if not tem(E) or lid not in E['lugares']: return None
    if len(abertas(E, lid)) >= R.QUADRO.get(E['lugares'][lid].get('tipo'), 1): return None
    if any(m['tipo'] == tipo and m.get('alvo') == alvo and m['estado'] in ('aberta', 'tomada') for m in todas(E).values()): return None
    rs = estado.sorte(E, f'missao|{lid}|{tipo}|{alvo}')
    base, vezes = R.MISSAO_PAGA[tipo]; quer = paga if paga is not None else int(base * (vezes ** cat) * (n if tipo in ('caça', 'entrega') else 1))
    paga = int(min(quer, _bolsa(E, de) * 0.6))
    if paga < 3: return None
    W = E['mundo']; k = ((W.get('seq') or {}).get('missao') or 0) + 1; mid = f'm{k:04d}'
    reg = dict(de=de, onde=lid, tipo=tipo, alvo=alvo, n=n, paga=paga, prazo=prazo or E['relogio']['dia'] + rs.randint(*R.MISSAO_PRAZO), frente=frente, estado='aberta', quem=None,
               desde=E['relogio']['dia'], cat=cat)
    if ermo: reg['ermo'] = ermo
    if quem_vai: reg['quem_vai'] = quem_vai
    if nome_alvo: reg['nome_alvo'] = nome_alvo
    estado.aplica(E, 'missao', [['mundo', 'seq', 'missao', 'soma', 1], ['mundo', 'missoes', mid, 'poe', reg]], onde=lid, quem=[de] if de in E['gente'] else [],
                  texto=f"no quadro {estado.de(E, lid)}: {texto(E, reg)} ({paga} de prata; {_quem(E, de)})")
    return mid


def contra_frente(E, pid, lid):
    """quem manda (o senhor, o capitão, o mestre da guilda) põe no quadro a missão contra a frente que ameaça as terras dele"""
    import regiao
    perto = regiao.saltos(E, lid)
    for fid, f in (E['mundo'].get('frentes') or {}).items():
        if f.get('fim') or f.get('onde') is None or perto.get(regiao_lugar(E, f['onde']), 99) > 2 or f['passo'] < 1: continue
        tipo = {'mistério': 'investigar'}.get(f['tipo'], 'matar' if f.get('alvo_missao') == 'matar' else f.get('alvo_missao') or 'investigar')
        alvo = f.get('alvo') or fid
        if posta(E, pid, lid, tipo, alvo, frente=fid, nome_alvo=f.get('nome_alvo') or f['nome'], cat=f.get('cat', 1)): return


def regiao_lugar(E, lid):
    import noticias
    return noticias.origem(E, lid)


def limpar(E, pid, lid):
    import masmorra
    ok = lambda m: E['lugares'].get(m, {}).get('tipo') == 'masmorra' and not E['lugares'][m].get('limpa') and E['lugares'][m].get('molde') != 'covil'      # ninguém paga para acordar dragão
    ms = [m for m in (E['lugares'][lid].get('vizinhos') or []) if ok(m)]
    for e in (E['lugares'][lid].get('vizinhos') or []):
        ms += [m for m in (E['lugares'].get(e, {}).get('vizinhos') or []) if ok(m) and m not in ms]
    for m in ms:
        cat = E['lugares'][m]['niveis'][-1]['cat']
        if posta(E, pid, lid, 'limpar', m, cat=min(cat, 3)): return


# ---------- cumprir ----------
def _abates(E, pid, esp, desde_ev):
    """quantos da espécie a pessoa (ou o grupo dela) tirou da contagem desde aquele evento (pelo registro: os eventos em que ela estava)"""
    n = 0
    arq = os.path.join(estado.pasta(), 'eventos.jsonl'); evs = []
    if os.path.exists(arq): evs = [json.loads(l) for l in open(arq, encoding='utf-8').read().splitlines() if l]
    for e in evs + E['_novos']:
        if e['id'] <= desde_ev or pid not in (e.get('quem') or []): continue
        for x in e.get('efeitos') or []:
            if isinstance(x, list) and len(x) == 5 and x[0] == 'lugar' and x[2] == f'bichos.{esp}' and x[3] == 'soma' and x[4] < 0: n += -x[4]
    return n


def confere(E, mid, pid):
    """a missão está cumprida por esta pessoa? (verdade, por quê)"""
    m = todas(E)[mid]; t = m['tipo']; a = m.get('alvo')
    if t == 'caça':
        k = _abates(E, pid, a, m.get('ev0', 0)); return k >= m['n'], f"{k} de {m['n']}"
    if t == 'entrega':
        tem_ = (E['gente'][pid].get('carga') or {}).get(a, 0); return tem_ >= m['n'], f"carrega {tem_} de {m['n']}"
    if t == 'limpar':
        lp = E['lugares'].get(a, {}).get('limpa'); return bool(lp) and pid in (lp.get('quem') or []), ('limpa por você' if lp and pid in (lp.get('quem') or []) else 'limpa por outros' if lp else 'ainda não foi limpa')
    if t == 'matar':
        import frentes
        f = (E['mundo'].get('frentes') or {}).get(m.get('frente')) if m.get('frente') else None
        if f: return f.get('fim') == 'barrada', ('a frente foi barrada' if f.get('fim') == 'barrada' else 'a frente segue')
        return False, 'sem alvo'
    if t == 'escolta':
        q = E['gente'].get(m.get('quem_vai')) or {}; return q.get('lugar') == a and q.get('estado') == 'vivo' and E['gente'][pid]['lugar'] == a, f"{q.get('nome', '?')} está {estado.em(E, q['lugar']) if q.get('lugar') in E['lugares'] else '?'}"
    if t == 'investigar':
        oc = E['mundo'].get('oculto') or {}; k = sum(1 for c in oc if c.startswith(f"frente.{m.get('frente') or a}.")); return k >= 2, f"{k} de 2 coisas descobertas"
    return False, '?'


def cumpre(E, mid, pid, tipo_ev='missao', texto=None):
    """a missão foi cumprida: a paga sai da bolsa de quem pediu (até o que ele tem), a fama sobe, quem pediu lembra, a frente recua um passo"""
    import gente, noticias
    m = todas(E)[mid]; de = m['de']; paga = int(min(m['paga'], _bolsa(E, de)))
    ef = [['mundo', 'missoes', mid, 'estado', 'poe', 'cumprida'], ['mundo', 'missoes', mid, 'quem', 'poe', pid], ['pessoa', pid, 'fama', 'soma', R.MISSAO_FAMA[m['tipo']]]]
    if paga > 0: ef += ([['pessoa', de, 'moedas', 'soma', -paga]] if de in E['gente'] else [['estoque', de, 'prata', 'soma', -paga]]) + [['pessoa', pid, 'moedas', 'soma', paga]]
    if m['tipo'] == 'entrega':
        ef += [['pessoa', pid, f"carga.{m['alvo']}", 'soma', -m['n']]] + ([['pessoa', de, f"carga.{m['alvo']}", 'soma', m['n']]] if de in E['gente'] else [['estoque', de, m['alvo'], 'soma', m['n']]])
    if de in E['gente']: ef += gente.lembra(E, de, pid, f"cumpriu a missão que eu paguei ({texto_curto(E, m)})", 3)
    ef += noticias.nova(E, m['onde'], f"{E['gente'][pid]['nome']} cumpriu a missão {estado.de(E, m['onde'])}: {texto(E, m)}", 1, ('missão',))
    estado.aplica(E, tipo_ev, ef, onde=m['onde'], quem=[pid] + ([de] if de in E['gente'] else []), texto=texto or f"{E['gente'][pid]['nome']} cumpre a missão {mid}: {texto(E, m)} ({paga} de prata)")
    if m.get('frente'):
        try: import frentes; frentes.recua(E, m['frente'], f"a missão {mid} cumprida por {E['gente'][pid]['nome']}")
        except (ModuleNotFoundError, AttributeError): pass
    return paga


def texto_curto(E, m): return texto(E, m).split(',')[0]


def toma(E, pid, mid):
    p = estado.presente(E, pid, 'tomar missão')
    m = todas(E).get(mid) or sys.exit(f'não há a missão "{mid}" (`missoes.py ver`)')
    if m['estado'] != 'aberta': sys.exit(f'a missão {mid} não está aberta ({m["estado"]})')
    if m['onde'] != p['lugar']: sys.exit(f"a missão {mid} está no quadro {estado.de(E, m['onde'])}: só se toma lá")
    estado.aplica(E, 'missao', [['mundo', 'missoes', mid, 'estado', 'poe', 'tomada'], ['mundo', 'missoes', mid, 'quem', 'poe', pid], ['mundo', 'missoes', mid, 'ev0', 'poe', E['relogio']['eventos']]],
                  onde=p['lugar'], quem=[pid], texto=f"{p['nome']} toma a missão {mid}: {texto(E, m)}")
    return f"{p['nome']} tomou a missão {mid}: {texto(E, m)} · paga {m['paga']} · prazo: Dia {m['prazo']}."


def entrega(E, pid, mid):
    p = E['gente'].get(pid) or sys.exit('não há essa pessoa')
    m = todas(E).get(mid) or sys.exit(f'não há a missão "{mid}"')
    if m['estado'] != 'tomada' or m.get('quem') != pid: sys.exit(f'{p["nome"]} não tem a missão {mid} tomada')
    ok, pq = confere(E, mid, pid)
    if not ok: sys.exit(f"a missão {mid} ainda não está cumprida: {pq}")
    if m['tipo'] == 'entrega' and p['lugar'] != m['onde']: sys.exit(f"a entrega é {estado.em(E, m['onde'])}")
    paga = cumpre(E, mid, pid)
    return f"Missão {mid} cumprida ({pq}): {paga} de prata, fama +{R.MISSAO_FAMA[m['tipo']]}."


def larga(E, pid, mid):
    import gente
    m = todas(E).get(mid) or sys.exit(f'não há a missão "{mid}"')
    if m['estado'] != 'tomada' or m.get('quem') != pid: sys.exit(f'não é missão tomada por essa pessoa')
    ef = [['mundo', 'missoes', mid, 'estado', 'poe', 'falhou'], ['pessoa', pid, 'fama', 'soma', R.MISSAO_FALHA[0]]] + (gente.lembra(E, m['de'], pid, 'tomou a minha missão e largou', R.MISSAO_FALHA[1]) if m['de'] in E['gente'] else [])
    estado.aplica(E, 'missao', ef, onde=m['onde'], quem=[pid], texto=f"{E['gente'][pid]['nome']} larga a missão {mid}")
    return f"Missão {mid} largada."


def virada(E):
    """a missão aberta que passou do prazo vence; a tomada que passou do prazo falha (quem tomou perde fama; quem pediu lembra)"""
    if not tem(E): return
    import gente
    hoje = E['relogio']['dia']
    for mid, m in list(todas(E).items()):
        if m['prazo'] >= hoje or m['estado'] not in ('aberta', 'tomada'): continue
        if m['estado'] == 'aberta': estado.aplica(E, 'missao', [['mundo', 'missoes', mid, 'estado', 'poe', 'venceu']], onde=m['onde'], texto=f"a missão {mid} venceu no quadro, sem ninguém")
        else:
            q = m['quem']; ef = [['mundo', 'missoes', mid, 'estado', 'poe', 'falhou']]
            if q in E['gente'] and E['gente'][q]['estado'] == 'vivo': ef += [['pessoa', q, 'fama', 'soma', R.MISSAO_FALHA[0]]] + (gente.lembra(E, m['de'], q, 'não cumpriu a missão no prazo', R.MISSAO_FALHA[1]) if m['de'] in E['gente'] else [])
            estado.aplica(E, 'missao', ef, onde=m['onde'], quem=[q] if q in E['gente'] else [], texto=f"a missão {mid} falhou: o prazo passou")
    for mid, m in list(todas(E).items()):                   # o quadro guarda pouco do que acabou: o que acabou há mais de 60 dias sai
        if m['estado'] not in ('aberta', 'tomada') and hoje - max(m['prazo'], m['desde']) > 60:
            estado.aplica(E, 'missao', [['mundo', 'missoes', mid, 'poe', None]], texto=f"a missão {mid} sai do quadro")


def gera(E, r):
    """o Dia 1: cada quem que manda põe no quadro o que já o preocupa (a frente perto, a masmorra ao lado), e os caçadores, as bestas"""
    import gente
    n0 = len(todas(E))
    for pid, p in list(E['gente'].items()):
        if p.get('papel') in ('senhor', 'capitão', 'mestre de guilda') and p['estado'] == 'vivo':
            contra_frente(E, pid, p['lugar']); limpar(E, pid, p['lugar'])
        elif p.get('papel') == 'caçador' and p['estado'] == 'vivo':
            gente._q_recompensa(E, pid, p, r)
    return [f"O quadro de missões do Dia 1: {len(todas(E)) - n0} missões."]


# ---------- a mesa ----------
def mesa(E):
    if not tem(E): return []
    eu = estado.eu(E)
    if not eu or E['gente'][eu]['estado'] != 'vivo': return []
    lid = E['gente'][eu]['lugar']; L = []
    minhas = [(k, m) for k, m in todas(E).items() if m['estado'] == 'tomada' and m.get('quem') == eu]
    quadro = [(k, m) for k, m in abertas(E, lid).items()] if not estado.fora(E, eu) else []
    if quadro: L += ['**O quadro de missões daqui** (`missoes.py toma MID`):'] + [f"- {k} · {texto(E, m)} · {m['paga']} de prata · prazo: Dia {m['prazo']} · de {_quem(E, m['de'])}" + (' · contra uma frente' if m.get('frente') else '') for k, m in quadro]
    if minhas: L += ['**As suas missões** (`missoes.py entrega MID`):'] + [f"- {k} · {texto(E, m)} · prazo: Dia {m['prazo']} · {confere(E, k, eu)[1]}" for k, m in minhas]
    return L


if __name__ == '__main__':
    import signal; hasattr(signal, 'SIGPIPE') and signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    a = sys.argv[1:]; op = dict(x.split('=', 1) for x in a if '=' in x); a = [x for x in a if '=' not in x]
    if not a or a[0] not in ('ver', 'toma', 'entrega', 'larga'): print(__doc__); sys.exit()
    E = estado.carrega(); pid = op.get('quem') or estado.eu(E)
    if a[0] == 'ver':
        print('\n'.join(mesa(E)) or 'nada no quadro daqui, e nenhuma missão tomada.')
    else:
        if len(a) != 2: sys.exit(f'use: `missoes.py {a[0]} MID`')
        print({'toma': toma, 'entrega': entrega, 'larga': larga}[a[0]](E, pid, a[1])); estado.grava(E)
