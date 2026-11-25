#!/usr/bin/env python3
"""gente.py — MOTOR 10, ETAPA FINAL: A GENTE COM NOME. A MEMÓRIA (até 12 fatos com peso, de quem e do quê), a OPINIÃO que sai dela (com os porquês),
os LAÇOS (pai, irmão, aprendiz, jurado...) e O QUERER DA SEMANA: no primeiro dia de cada semana, cada nomeado quer uma coisa do papel dele, e o querer vira
ato com efeito (o ferreiro forja para a loja, o caçador caça, o guarda patrulha, o senhor paga a missão contra a frente, o velho conta a história...).
Quando o querer toca o personagem (e há motivo no estado), vira pedido na caixa.

  python3 gente.py ver PID                    quem é, o que lembra (SÓ O MESTRE vê tudo), o que acha do personagem e por quê
  python3 gente.py quem [LUGAR]               a gente com nome de um lugar (do personagem, sem LUGAR), com o que acha dele
  python3 gente.py lembra PID "fato" PESO [de=QUEM]      o Mestre põe um fato na memória de alguém (peso de −5 a 5; de quem: o personagem, se não disser)
"""
import sys
import tabelas as T
import tabelas_mundo as M
import tabelas_regiao as R
import estado


def tem(E): return bool((E.get('mundo') or {}).get('meta'))


def lembra(E, pid, de, o_que, peso):
    """o efeito que põe um fato na memória de alguém (vai no evento de quem causa). [] se a pessoa não há, morreu ou é o personagem"""
    p = E['gente'].get(pid) if isinstance(pid, str) else None
    if not isinstance(p, dict) or p.get('estado') != 'vivo' or p.get('jogador') or pid == de: return []
    return [['pessoa', pid, 'memoria', 'junta', dict(dia=E['relogio']['dia'], de=de, o_que=o_que, peso=max(-M.MEMORIA_PESO, min(M.MEMORIA_PESO, int(peso))))]]


def opiniao(E, pid, sobre):
    """(a opinião de pid sobre `sobre`, de −10 a 10; os porquês: os três fatos de maior peso)"""
    mem = [m for m in (E['gente'].get(pid, {}).get('memoria') or []) if m.get('de') == sobre]
    v = max(-M.OPINIAO_MAX, min(M.OPINIAO_MAX, sum(m['peso'] for m in mem)))
    return v, [m['o_que'] for m in sorted(mem, key=lambda m: (-abs(m['peso']), -m['dia']))[:3]]


def diz(v):
    return next(t for lim, t in R.OPINIAO_DIZ if v <= lim)


def lacos_de(E, pid): return dict(E['gente'].get(pid, {}).get('lacos') or {})
LACO_DIZ = {'pai': 'pai/mãe', 'mãe': 'pai/mãe', 'filho': 'filho/filha', 'irmão': 'irmão/irmã', 'cônjuge': 'cônjuge', 'aprendiz': 'aprendiz', 'mestre': 'mestre'}
def laco_diz(t): return LACO_DIZ.get(t, t)          # o motor não sabe o gênero de ninguém: o laço vai à mesa nas duas formas


def parentes(E, pid):
    """os parentes vivos de alguém (pelos laços dele)"""
    return [k for k, t in lacos_de(E, pid).items() if t in ('pai', 'mãe', 'filho', 'irmão', 'cônjuge', 'parente') and E['gente'].get(k, {}).get('estado') == 'vivo']


# ---------- o querer da semana ----------
def _vivos_nomeados(E):
    return [k for k, p in E['gente'].items() if isinstance(p, dict) and p.get('estado') == 'vivo' and not p.get('jogador') and not p.get('rival') and p.get('papel') and not estado.fora(E, k)]


def virada(E):
    """no primeiro dia de cada semana (o dia que acabou de virar é o 1, 8, 15...), cada nomeado quer uma coisa do papel dele"""
    if not tem(E) or (E['relogio']['dia'] - 1) % M.SEMANA != 0: return
    for pid in _vivos_nomeados(E):
        p = E['gente'][pid]; Q = R.QUERER.get(p['papel'])
        if not Q: continue
        rs = estado.sorte(E, f'querer|{pid}'); q = rs.choices([x for x, _ in Q], [w for _, w in Q])[0]
        f = globals().get('_q_' + q)
        if f:
            try: f(E, pid, p, rs)
            except SystemExit: pass                         # o querer que não cabe (faltou prata, faltou matéria) não acontece: a semana passa


def _ap(E, pid, ef, texto):
    if ef: estado.aplica(E, 'querer', ef, onde=E['gente'][pid]['lugar'], quem=[pid], texto=texto)


def _paga(E, lid, pid, v):
    """a prata do lugar vai para a pessoa (o lugar compra o que ela fez), até o que o lugar tem"""
    v = int(min(v, E['lugares'][lid]['estoque'].get('prata', 0)))
    return [['estoque', lid, 'prata', 'soma', -v], ['pessoa', pid, 'moedas', 'soma', v]] if v > 0 else []


def _q_forja(E, pid, p, rs):
    import mercado, itens
    lid = p['lugar']; est = E['lugares'][lid]['estoque']
    if est.get('metal:0', 0) < 3: return
    fam = rs.choice(['espada', 'lança', 'machado', 'adaga', 'maça']); it = itens.item('arma', 0, familia=fam, onde=lid)
    v = int(mercado.valor(it) * 0.4)
    _ap(E, pid, [['estoque', lid, 'metal:0', 'soma', -3], ['item', 'nasce', it]] + _paga(E, lid, pid, v), f"{p['nome']} forja {it['nome']} para a loja {estado.de(E, lid)}")


def _q_curte(E, pid, p, rs):
    import mercado, itens
    lid = p['lugar']; est = E['lugares'][lid]['estoque']
    if est.get('couro:0', 0) < 4: return
    it = itens.item('armadura', 0, material='couro', onde=lid); v = int(mercado.valor(it) * 0.4)
    _ap(E, pid, [['estoque', lid, 'couro:0', 'soma', -4], ['item', 'nasce', it]] + _paga(E, lid, pid, v), f"{p['nome']} curte o couro e faz {it['nome']} para a loja")


def _ermo_perto(E, lid, quer=None):
    import caca
    es = [e for e in (E['lugares'][lid].get('vizinhos') or []) if e in E['lugares'] and caca.e_ermo(E, e)]
    if quer: es = [e for e in es if any(caca.bichos_de(E, e).get(x, 0) > 0 for x in quer)]
    return es[0] if es else None


def _q_caca(E, pid, p, rs):
    import caca, mercado
    lid = p['lugar']; e = _ermo_perto(E, lid, ('corça', 'javali', 'ratazana'))
    if not e: return
    b = caca.bichos_de(E, e); esp = max((x for x in ('corça', 'javali', 'ratazana') if b.get(x, 0) > 0), key=lambda x: b[x])
    teto = caca.teto_de(E, e).get(esp, 1); n = 2 if b[esp] > teto * 0.6 else 1
    ef = [['lugar', e, f'bichos.{esp}', 'soma', -n], ['estoque', lid, 'comida', 'soma', 4 * n], ['estoque', lid, 'couro:0', 'soma', n]]
    ef += _paga(E, lid, pid, int(4 * n * mercado.preco(E, lid, 'comida') * 0.6))
    _ap(E, pid, ef, f"{p['nome']} caça {estado.tantos(n, estado.especie(esp)['nome'], estado.especie(esp).get('plural'))} {estado.em(E, e)} e vende a carne e o couro")


def _q_tira(E, pid, p, rs):
    import mercado
    lid = p['lugar']; bem = {'lenhador': 'madeira:0', 'mineiro': 'metal:0', 'pescador': 'comida', 'lavrador': 'comida'}.get(p['papel'], 'comida'); n = 3
    _ap(E, pid, [['estoque', lid, bem, 'soma', n]] + _paga(E, lid, pid, int(n * mercado.preco(E, lid, bem) * 0.6)), f"{p['nome']} tira {n} de {estado.nome_bem(bem)} e vende no lugar")


def _q_serve(E, pid, p, rs):
    lid = p['lugar']
    if E['lugares'][lid]['estoque'].get('comida', 0) < 3: return
    _ap(E, pid, [['estoque', lid, 'comida', 'soma', -3]] + _paga(E, lid, pid, 4), f"{p['nome']} serve a semana na taverna")


def _q_lucra(E, pid, p, rs):
    lid = p['lugar']; _ap(E, pid, _paga(E, lid, pid, rs.randint(2, 6)), f"{p['nome']} fecha os negócios da semana")


def _q_colhe(E, pid, p, rs):
    import caca, mercado
    lid = p['lugar']; e = _ermo_perto(E, lid)
    if not e or caca.coleta_de(E, e).get('erva:0', 0) < 2: return
    _ap(E, pid, [['lugar', e, 'coleta.erva:0', 'soma', -2], ['estoque', lid, 'remédio', 'soma', 1]] + _paga(E, lid, pid, int(mercado.preco(E, lid, 'remédio') * 0.6)),
        f"{p['nome']} colhe erva {estado.em(E, e)} e faz remédio")


def _q_estuda(E, pid, p, rs):
    c = p.get('tradicao') or ('manha' if p['papel'] == 'ladino' else None)
    if c: _ap(E, pid, [['pessoa', pid, f'treino.{c}', 'soma', 6]], f"{p['nome']} estuda a semana")


def _q_treina(E, pid, p, rs):
    of = next(iter(p.get('maestria') or {}), None) or 'coleta'
    _ap(E, pid, [['pessoa', pid, f'treino.{of}', 'soma', 6]], f"{p['nome']} treina o ofício da casa")


def _q_corte(E, pid, p, rs): _ap(E, pid, [['pessoa', pid, 'fama', 'soma', 1]], f"{p['nome']} se mostra na corte")


def _q_imposto(E, pid, p, rs):
    lid = p['lugar']; v = int(E['lugares'][lid]['estoque'].get('prata', 0) * R.IMPOSTO)
    _ap(E, pid, _paga(E, lid, pid, v), f"{p['nome']} cobra o imposto {estado.de(E, lid)}")


def _q_patrulha(E, pid, p, rs):
    import regiao, noticias
    lid = p['lugar']; ests = [(e, o) for e, o in regiao.estradas(E, lid) if E['lugares'][e].get('bando', 0) > 0]
    if not ests: return
    e, o = max(ests, key=lambda x: E['lugares'][x[0]]['bando']); b = E['lugares'][e]['bando']
    forca = p['nivel'] // 10 + rs.randint(1, 10) + rs.randint(1, 10) + (4 if p['papel'] == 'capitão' else 0)
    if forca >= 10 + b:
        n = min(b, 2 if p['papel'] == 'capitão' else 1)
        _ap(E, pid, [['lugar', e, 'bando', 'soma', -n], ['pessoa', pid, 'fama', 'soma', 1]], f"{p['nome']} patrulha {E['lugares'][e]['nome']} e tira {estado.tantos(n, 'salteador', 'salteadores')} dela")
    elif b >= 6 and rs.random() < 0.08:
        _ap(E, pid, [['pessoa', pid, 'estado', 'poe', 'morto']] + noticias.nova(E, lid, f"{p['nome']}, {p.get('sobre', '')}, morreu numa emboscada {estado.em(E, e)}", 3, ('morte',)),
            f"{p['nome']} cai numa emboscada {estado.em(E, e)} e morre")


def _q_furta(E, pid, p, rs):
    if rs.random() > R.FURTO[0]: return
    lid = p['lugar']; alvos = [k for k in _vivos_nomeados(E) if k != pid and E['gente'][k]['lugar'] == lid and E['gente'][k]['moedas'] > 20]
    if not alvos: return
    v = rs.choice(alvos); q = min(40, int(E['gente'][v]['moedas'] * rs.uniform(0.1, 0.3)))
    if rs.random() < R.FURTO[1]: _ap(E, pid, lembra(E, v, pid, 'tentou me roubar e a guarda pegou', -3), f"{p['nome']} tenta furtar {E['gente'][v]['nome']}, e a guarda pega")
    else: _ap(E, pid, [['pessoa', v, 'moedas', 'soma', -q], ['pessoa', pid, 'moedas', 'soma', q]], f"alguém furta {q} de prata de {E['gente'][v]['nome']}")


def _q_conta(E, pid, p, rs):
    import noticias
    C = E['mundo'].get('cronica') or []
    if not C or rs.random() > 0.3: return
    x = rs.choice(C)
    _ap(E, pid, noticias.nova(E, p['lugar'], f"{p['nome']} conta da história: no ano {x['ano']}, {x['texto'][0].lower() + x['texto'][1:]}", 0, ('história',)), f"{p['nome']} conta uma história antiga")


def _q_recompensa(E, pid, p, rs):
    import missoes, caca
    lid = p['lugar']; e = _ermo_perto(E, lid, ('lobo', 'urso', 'aranha', 'javali'))
    if not e: return
    b = caca.bichos_de(E, e); esp = next((x for x in ('urso', 'aranha', 'lobo', 'javali') if b.get(x, 0) >= 3), None)
    if esp and hasattr(missoes, 'posta'): missoes.posta(E, pid, lid, 'caça', esp, n=min(3, b[esp]), ermo=e)


def _q_escolta(E, pid, p, rs):
    import missoes, regiao
    lid = p['lugar']; ests = [(e, o) for e, o in regiao.estradas(E, lid, abertas=True) if E['lugares'][e].get('bando', 0) >= 3 and regiao.povoado(E, o)]
    if ests and hasattr(missoes, 'posta'): e, o = rs.choice(ests); missoes.posta(E, pid, lid, 'escolta', o, n=1, quem_vai=pid)


def _q_contra_frente(E, pid, p, rs):
    import missoes
    if hasattr(missoes, 'contra_frente'): missoes.contra_frente(E, pid, p['lugar'])


def _q_limpar(E, pid, p, rs):
    import missoes
    if hasattr(missoes, 'limpar'): missoes.limpar(E, pid, p['lugar'])


def _q_pede_materia(E, pid, p, rs):
    """o ferreiro sem metal pede ao personagem, se o personagem está no lugar e o ferreiro não o detesta"""
    import caixa, mercado
    eu = estado.eu(E)
    if not eu or E['gente'][eu]['estado'] != 'vivo' or E['gente'][eu]['lugar'] != p['lugar'] or estado.fora(E, eu): return
    if opiniao(E, pid, eu)[0] < -2 or E['lugares'][p['lugar']]['estoque'].get('metal:0', 0) >= 6: return
    n = 3; paga = int(n * mercado.preco(E, p['lugar'], 'metal:0') * 1.3) + 2; prazo = E['relogio']['dia'] + rs.randint(*R.CAIXA_PRAZO)
    rival = next((k for k in _vivos_nomeados(E) if k != pid and E['gente'][k]['papel'] in ('mineiro', 'mercador') and E['gente'][k]['lugar'] == p['lugar']), None)
    efs = dict(a=[['pessoa', eu, 'carga.metal:0', 'soma', -n], ['estoque', p['lugar'], 'metal:0', 'soma', n], ['pessoa', pid, 'moedas', 'soma', -paga], ['pessoa', eu, 'moedas', 'soma', paga]] + lembra(E, pid, eu, 'me trouxe o metal quando faltou', 2),
               b=lembra(E, pid, eu, 'disse que não tinha o metal', -1),
               c=lembra(E, pid, eu, 'calou quando pedi o metal', -R.CAIXA_CUSTO) + (lembra(E, pid, rival, 'me arranjou o metal', 1) if rival else []))
    caixa.nova(E, pid, f"{n} de metal Comum (paga {paga} de prata)", prazo, dict(a='entrega o metal', b='diz que não tem', c='cala'), efs, 'c', motivo=f"a forja {estado.de(E, p['lugar'])} está sem metal")


def gera(E, r):
    """o Dia 1: a gente já se conhece (os laços da família vêm do gerador); nada mais a fazer aqui"""
    return []


# ---------- a mesa ----------
def mesa(E):
    if not tem(E): return []
    eu = estado.eu(E)
    if not eu or E['gente'][eu]['estado'] != 'vivo' or estado.fora(E, eu): return []
    lid = E['gente'][eu]['lugar']; L = []
    for k, q in E['gente'].items():
        if k == eu or q.get('estado') != 'vivo' or q.get('lugar') != lid or estado.fora(E, k): continue
        v, pq = opiniao(E, k, eu); laco = lacos_de(E, eu).get(k)
        if v or laco: L.append(f"- {q['nome']}" + (f" ({laco_diz(laco)})" if laco else '') + f": {diz(v)}" + (f" ({v:+d})" if v else '') + (f" — {'; '.join(pq)}" if pq else ''))
    return ['**O que a gente daqui lembra de você:**'] + L if L else []


def ver(E, pid):
    p = E['gente'].get(pid) or sys.exit(f'não há a pessoa "{pid}"')
    eu = estado.eu(E); L = [f"{p['nome']} [{pid}] · {p.get('papel', '?')} · {estado.em(E, p['lugar'])} · " + (estado.morte_diz(E, p) if p['estado'] != 'vivo' else f"nível {p['nivel']}, {p.get('idade', '?')} anos")]
    if p.get('casa'): L.append(f"  casa: {(E['mundo'].get('casas') or {}).get(p['casa'], {}).get('nome', p['casa'])}")
    if p.get('lacos'): L.append('  laços: ' + ', '.join(f"{E['gente'][k]['nome']} ({laco_diz(t)})" for k, t in p['lacos'].items() if k in E['gente']))
    if eu and eu != pid:
        v, pq = opiniao(E, pid, eu); L.append(f"  sobre você: {diz(v)} ({v:+d})" + (f" — {'; '.join(pq)}" if pq else ''))
    if p.get('memoria'): L.append('  SÓ O MESTRE, a memória: ' + ' · '.join(f"Dia {m['dia']}, {E['gente'].get(m['de'], {}).get('nome', m['de'])}: {m['o_que']} ({m['peso']:+d})" for m in p['memoria']))
    if p.get('querer'): L.append(f"  quer: {p['querer'].get('o_que')}")
    return '\n'.join(L)


if __name__ == '__main__':
    import signal; hasattr(signal, 'SIGPIPE') and signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    a = sys.argv[1:]
    if not a or a[0] not in ('ver', 'quem', 'lembra'): print(__doc__); sys.exit()
    E = estado.carrega()
    if a[0] == 'ver':
        if len(a) != 2: sys.exit('use: `gente.py ver PID`')
        print(ver(E, a[1]))
    elif a[0] == 'quem':
        lid = a[1] if len(a) > 1 else (E['gente'][estado.eu(E)]['lugar'] if estado.eu(E) else None)
        if lid not in E['lugares']: sys.exit('diga o lugar: `gente.py quem LUGAR`')
        eu = estado.eu(E)
        for k, q in E['gente'].items():
            if q.get('lugar') == lid and q.get('estado') == 'vivo' and k != eu:
                print(f"- {q['nome']} [{k}]: {q.get('sobre', '')}" + (f" · {diz(opiniao(E, k, eu)[0])}" if eu else ''))
    else:
        op = dict(x.split('=', 1) for x in a[1:] if '=' in x); pos = [x for x in a[1:] if '=' not in x]
        if len(pos) != 3 or not pos[2].lstrip('-').isdigit(): sys.exit('use: `gente.py lembra PID "fato" PESO [de=QUEM]`')
        ef = lembra(E, pos[0], op.get('de') or estado.eu(E), pos[1], int(pos[2]))
        if not ef: sys.exit(f'{pos[0]} não guarda memória (não há, morreu, ou é o personagem)')
        estado.aplica(E, 'mestre', ef, quem=[pos[0]], texto=f"{E['gente'][pos[0]]['nome']} lembra: {pos[1]}"); estado.grava(E); print('feito.')
