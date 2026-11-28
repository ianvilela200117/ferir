#!/usr/bin/env python3
"""rivais.py — MOTOR 10, ETAPA FINAL: A CORRIDA. Os 40 aventureiros nativos (6 guildas e os que andam sozinhos, de novatos a Lendas) disputam a mesma escada,
pela mesma regra: por semana escolhem um plano (a missão do quadro, a masmorra que ninguém limpou, o chefe do ermo, a forja do núcleo, o descanso); no dia marcado,
resolvem pela CONTA RÁPIDA (conta.py, afinada contra o luta.py). Ganham prata, fama, peças e núcleos; MORREM DE VEZ (o que levavam fica onde caíram).
A cada estação entra gente nova; toda semana sai o RANKING; no verão, o TORNEIO do rei; a cada estação, o LEILÃO da capital (o que é Único ou maior não tem loja).
A JANELA DO MUNDO conta a todos na hora: a primeira limpeza de uma masmorra, a peça Única ou maior que nasce, a Lenda que morre.

  python3 rivais.py ranking                 o ranking da semana (o que o povo sabe)
  python3 rivais.py ver PID                 um rival: quem é, a guilda, a fama, o que veste (o plano dele é segredo: SÓ O MESTRE, com `mestre`)
  python3 rivais.py mestre                  SÓ O MESTRE: os planos de todos (e as habilidades escondidas, a parte 2, fase 2)
  python3 rivais.py leilao                  o próximo leilão: os lotes e os lances
  python3 rivais.py lance ITEM PRATA        o personagem dá um lance (vale no dia do leilão, se ele estiver na capital e tiver a prata)
"""
import math, sys
import tabelas as T
import tabelas_mundo as M
import tabelas_regiao as R
import estado


def tem(E): return bool((E.get('mundo') or {}).get('meta'))
def rivais(E, vivos=True): return [k for k, p in E['gente'].items() if isinstance(p, dict) and p.get('rival') and (not vivos or p['estado'] == 'vivo')]
def faixa(p): n = p['nivel']; return 'novato' if n < 15 else 'oficial' if n < 50 else 'veterano' if n < 120 else 'Lenda'
def plano(p): x = (p.get('marca') or {}).get('plano'); return x if isinstance(x, dict) else None


def pecas_em_uso(E, pid): return [it for it in E['itens']['itens'].values() if it.get('dono') == pid and it.get('uso')]
def pontos(E, pid):
    p = E['gente'][pid]; us = pecas_em_uso(E, pid)
    a = max([it['cat'] for it in us if it['tipo'] in ('arma', 'foco')] + [0]); b = max([it['cat'] for it in us if it['tipo'] == 'armadura' and 'tronco' in (it.get('cobre') or ['tronco'])] + [0])
    return int((p.get('fama') or 0) + R.RANKING_PECA * (a + b))


def grupo(E, pid):
    """quem vai com o rival: os da guilda dele que estão na mesma casa, vivos e sem plano (o de maior nível comanda)"""
    p = E['gente'][pid]; g = p.get('guilda')
    if not g: return [pid]
    return [pid] + [k for k in rivais(E) if k != pid and E['gente'][k].get('guilda') == g and E['gente'][k]['lugar'] == p['lugar'] and not plano(E['gente'][k]) and not estado.fora(E, k)][:3]


# ---------- a ameaça de cada alvo, em lutadores (para a conta rápida) ----------
def _bando(esp, n, rs, cat=None):
    import bichos
    B = bichos.bando(esp, rs, n=max(1, n))
    if cat is not None:
        for b in B:
            if isinstance(b, dict) and b.get('cat_corpo') is not None: pass
    return B


def ameaca_nivel(E, mid, nv, rs):
    """os moradores de um nível da masmorra, em lutadores (o chefe do fundo e a guarda dele, o dragão)"""
    import bichos, criaturas
    B = []
    for s in nv['salas']:
        l = E['lugares'][s]
        for esp, q in (l.get('bichos') or {}).items():
            if isinstance(q, (int, float)) and q >= 1 and estado.especie(esp): B += _bando(esp, int(q), rs)
        ch = l.get('chefe')
        if isinstance(ch, dict) and ch.get('vivo'):
            try: B += [bichos.bicho(ch['qual'])] if estado.especie(ch['qual']) else criaturas.chefe(ch['qual'], lacaios=False)
            except (SystemExit, AttributeError, KeyError): pass
        d = l.get('dragao')
        if isinstance(d, dict):
            import tabelas_dragoes as TD
            try: B.append(bichos.bicho(TD.chave(d['tipo'], d['idade'])))
            except (SystemExit, AttributeError, KeyError): pass
    return B


def _lutadores(E, ids):
    out = []
    for k in ids:
        estado.em_cena(E, k); out.append(estado.lutador(E, k))
    return out


def chance_contra(E, ids, B):
    import conta
    if not B: return 1.0
    try: return conta.chance(_lutadores(E, ids), B)
    except (SystemExit, KeyError, ValueError, ZeroDivisionError): return 0.0


# ---------- o plano da semana ----------
def virada(E):
    if not tem(E): return
    hoje = E['relogio']['dia']
    for pid in rivais(E):                                    # o dia: quem tem plano para hoje, resolve
        p = E['gente'].get(pid)
        if p and p['estado'] == 'vivo' and plano(p) and plano(p).get('ate', 0) <= hoje: resolve(E, pid)
    if (hoje - 1) % M.SEMANA == 0:
        for pid in sorted(rivais(E), key=lambda k: -E['gente'][k]['nivel']):
            p = E['gente'].get(pid)
            if p and p['estado'] == 'vivo' and not plano(p) and not estado.fora(E, pid): escolhe(E, pid)
        ranking(E); acha(E)
    if (hoje - 1) % M.ESTACAO == 0 and hoje > 1: novos(E)
    if hoje % R.RIVAL['leilao_cada'] == R.RIVAL['leilao_dia']: leilao(E)
    if (hoje - 1) % M.ANO + 1 == R.RIVAL['torneio_dia']: torneio(E)
    janela(E)


def _marca_plano(E, ids, pl, texto, mais=()):
    ef = [['pessoa', ids[0], 'marca.plano', 'poe', pl]] + [['pessoa', k, 'marca.plano', 'poe', dict(o_que='junto', de=ids[0], ate=pl['ate'])] for k in ids[1:]] + list(mais)
    estado.aplica(E, 'rival', ef, onde=E['gente'][ids[0]]['lugar'], quem=ids, texto=texto)


def escolhe(E, pid):
    """o rival escolhe o plano da semana: a melhor coisa que a ousadia dele aceita (a missão, a masmorra, o chefe, a forja); senão, caça para viver"""
    import regiao, missoes
    p = E['gente'][pid]; hoje = E['relogio']['dia']; rs = estado.sorte(E, f'rival|plano|{pid}'); ids = grupo(E, pid); ous = R.RIVAL['ousadia'][faixa(p)]
    if p['pv'] < estado.pv_max(p) * 0.7 or p.get('feridas'):
        return _marca_plano(E, [pid], dict(o_que='descansa', ate=hoje + 7), f"{p['nome']} descansa a semana")
    nuc = next((i for i, it in E['itens']['itens'].items() if it.get('dono') == pid and it.get('tipo') == 'nucleo' and it['cat'] >= 3), None)
    if nuc:                                                 # a peça do núcleo: só quem tem a prata da obra a manda fazer (senão, junta antes)
        import mercado, itens
        cat = E['itens']['itens'][nuc]['cat']; custo = int(mercado.valor(itens.item('arma', cat, familia='espada')) * R.RIVAL['forja_paga'])
        if p['moedas'] >= custo * R.RIVAL['forja_sinal']: return _marca_plano(E, [pid], dict(o_que='forja', alvo=nuc, ate=hoje + 3 ** cat), f"{p['nome']} leva o núcleo ao ferreiro da capital")
    perto = regiao.saltos(E, regiao_lugar(E, p['lugar'])); op = []; longe = R.RIVAL['longe'][faixa(p)]
    for mid, m in missoes.abertas(E).items():                # as missões do quadro, ao alcance (a que já não tem alvo, ninguém toma)
        if perto.get(m['onde'], 99) > longe or m['tipo'] in ('entrega', 'escolta'): continue
        if m['tipo'] == 'investigar':                        # investigar não é luta: a chance é a do olho (a Percepção e a manha)
            c = min(0.8, R.RIVAL['olho'] + (p['atributos']['Percepção'] - 50) / 100 + 0.06 * (p.get('maestria') or {}).get('manha', 0))
            if c >= ous: op.append((c * (m['paga'] + 12 * R.MISSAO_FAMA['investigar']), 'missao', mid, c))
            continue
        if m['tipo'] == 'limpar' and (E['lugares'].get(m.get('alvo')) or {}).get('limpa'): continue
        B = _ameaca_missao(E, m, rs)
        if not B: continue
        c = chance_contra(E, ids, B)
        if c >= ous: op.append((c * (m['paga'] + 12 * R.MISSAO_FAMA[m['tipo']]), 'missao', mid, c))
    for mid, m in E['lugares'].items():                      # as masmorras que ninguém limpou, ao alcance
        if m.get('tipo') != 'masmorra' or m.get('limpa') or m.get('molde') == 'covil' or perto.get(regiao_lugar(E, mid), 99) > longe: continue
        cs = [chance_contra(E, ids, ameaca_nivel(E, mid, nv, rs)) for nv in m['niveis'][:3]]
        c = math.prod(cs) if cs else 0
        valor = sum(estado.livre(E, s_).get('prata', 0) for nv in m['niveis'] for s_ in nv['salas']) + 150 * len(m['niveis']) + 400
        if c >= ous * 0.8: op.append((c * valor, 'masmorra', mid, c))
    for e, l in E['lugares'].items():                        # o chefe do ermo (o núcleo)
        if l.get('tipo') != 'ermo' or perto.get(regiao_lugar(E, e), 99) > longe: continue
        for esp, q in (l.get('bichos') or {}).items():
            if q >= 1 and (estado.especie(esp) or {}).get('chefe') and estado.especie(esp).get('cat', 0) >= 3:
                c = chance_contra(E, ids, _bando(esp, 1, rs))
                if c >= ous and (p.get('fama') or 0) >= R.RIVAL['chefe_fama']: op.append((c * (300 * estado.especie(esp)['cat'] + 100), 'chefe', f'{e}|{esp}', c))
    if op:
        op.sort(reverse=True); _, tipo, alvo, c = op[0]
        if tipo == 'missao':
            m = missoes.todas(E)[alvo]
            return _marca_plano(E, ids, dict(o_que='missao', alvo=alvo, ate=hoje + rs.randint(2, 6), c=round(c, 2)), f"{p['nome']} toma a missão {alvo} ({missoes.texto(E, m)})",
                                mais=[['mundo', 'missoes', alvo, 'estado', 'poe', 'tomada'], ['mundo', 'missoes', alvo, 'quem', 'poe', pid]])
        if tipo == 'masmorra':
            n = len(E['lugares'][alvo]['niveis']); return _marca_plano(E, ids, dict(o_que='masmorra', alvo=alvo, ate=hoje + R.RIVAL['dias_masmorra'][0] + R.RIVAL['dias_masmorra'][1] * n, c=round(c, 2)),
                                                                     f"{p['nome']} parte para {E['lugares'][alvo]['nome']}" + (f" com {len(ids) - 1} da guilda" if len(ids) > 1 else ''))
        return _marca_plano(E, ids, dict(o_que='chefe', alvo=alvo, ate=hoje + rs.randint(3, 6), c=round(c, 2)), f"{p['nome']} sai atrás do chefe {estado.de(E, alvo.split('|')[0])}")
    return _marca_plano(E, [pid], dict(o_que='caca', ate=hoje + rs.randint(3, 6)), f"{p['nome']} caça para viver")


def regiao_lugar(E, lid):
    import noticias
    return noticias.origem(E, lid) or lid


def _ameaca_missao(E, m, rs):
    t = m['tipo']; a = m.get('alvo')
    if t == 'caça' and estado.especie(a): return _bando(a, m.get('n', 1), rs)
    if t == 'limpar' and a in E['lugares']: return [b for nv in E['lugares'][a]['niveis'] for b in ameaca_nivel(E, a, nv, rs)][:8]
    if t == 'matar':
        f = (E['mundo'].get('frentes') or {}).get(m.get('frente')) or {}
        d = f.get('dono')
        if d in E['gente']: return _lutadores(E, [d]) if E['gente'][d]['estado'] == 'vivo' else None
        k, _, v = str(d).partition(':')
        if k == 'dragao' and isinstance((E['lugares'].get(v) or {}).get('dragao'), dict):
            import bichos, tabelas_dragoes as TD; dr = E['lugares'][v]['dragao']; return [bichos.bicho(TD.chave(dr['tipo'], dr['idade']))]
        if k == 'esp': esp, _, er = v.partition('@'); return _bando(esp, 1, rs)
        if k == 'covil': return _bando(f.get('especie') or 'goblin', 6, rs)
    return None


# ---------- o dia marcado: a conta rápida ----------
def resolve(E, pid):
    p = E['gente'][pid]; pl = plano(p); ids = [pid] + [k for k in rivais(E) if (plano(E['gente'][k]) or {}).get('de') == pid]
    f = globals().get('_r_' + pl['o_que'])
    if f:
        try: f(E, pid, ids, pl)
        except SystemExit: pass
    for k in ids:                                            # o plano acaba (de quem ainda vive)
        if E['gente'][k]['estado'] == 'vivo' and plano(E['gente'][k]): estado.aplica(E, 'rival', [['pessoa', k, 'marca.plano', 'poe', None]], onde=E['gente'][k]['lugar'], quem=[k], texto=f"{E['gente'][k]['nome']} volta para casa")


def _perde(E, ids, c, onde, rs, oque):
    """a luta perdida: cada um pode morrer (pelo quanto a luta era ruim) ou sair ferido"""
    import noticias
    mortos = []
    for k in ids:
        q = E['gente'][k]
        if rs.random() < R.RIVAL['morre'] * (1 - c) * (1 if k == ids[0] else R.RIVAL['morre_junto']):
            ef = [['pessoa', k, 'lugar', 'poe', q['lugar']]]
            if onde in E['lugares'] and E['lugares'][onde].get('tipo') in ('ermo', 'sala', 'estrada'): ef = [['pessoa', k, 'lugar', 'poe', onde]]      # morre lá: o que levava fica lá
            ef.append(['pessoa', k, 'estado', 'poe', 'morto']); lenda = q['nivel'] >= 120
            txt = f"{q['nome']}, {'a Lenda' if lenda else 'aventureiro'}{', ' + E['mundo']['guildas'][q['guilda']]['nome'] if q.get('guilda') in (E['mundo'].get('guildas') or {}) else ''}, morreu {estado.em(E, onde)} ({oque})"
            ef += noticias.nova(E, onde, txt, 3 if lenda else 2, ('morte', 'rival'), janela=lenda, ja=ef) + ([['mundo', 'janela', 'junta', dict(dia=E['relogio']['dia'], texto=txt)]] if lenda else [])
            estado.aplica(E, 'rival', ef, onde=onde, quem=[k], texto=txt); mortos.append(k)
            _recolhe(E, k, q.get('guilda'))
        elif rs.random() < R.RIVAL['fere']:
            dano = -int(estado.pv_max(q) * rs.uniform(0.3, 0.7))
            estado.aplica(E, 'rival', [['pessoa', k, 'pv', 'soma', dano], ['ferida', k, 'abre', rs.choice(T.PARTES), rs.random() < 0.3]], onde=q['lugar'], quem=[k], texto=f"{q['nome']} volta ferido")
    return mortos


def _recolhe(E, morto, gid):
    """a guilda recolhe o corpo de quem morreu e as peças que ficaram com ele (o líder vivo da guilda fica com elas); sem guilda, ficam onde ele caiu"""
    if not gid: return
    vivos = [k for k in rivais(E) if E['gente'][k].get('guilda') == gid]
    if not vivos: return
    lider = max(vivos, key=lambda k: E['gente'][k]['nivel'])
    ef = [['item', i, 'dono', 'poe', lider] for i, it in E['itens']['itens'].items() if it.get('corpo') == morto and it.get('solto') and not it.get('dono')]
    if ef: estado.aplica(E, 'rival', ef, onde=E['gente'][lider]['lugar'], quem=[lider], texto=f"a guilda recolhe o corpo de {E['gente'][morto]['nome']}, e {E['gente'][lider]['nome']} fica com as peças dele")


def acha(E):
    """FORA DA CENA, O QUE FICOU COM UM CORPO NÃO FICA PARA SEMPRE: na semana, a peça boa (Rara ou maior) caída junto do corpo de alguém, num lugar que não é sala de masmorra
    (onde quem limpa a leva), vai para o rival mais forte que mora ali ou a uma estrada dali (achou, ou comprou do povo que achou). Perto do personagem, não: lá é cena do Mestre."""
    import regiao, noticias
    eu = estado.eu(E); perto_eu = set()
    if eu and E['gente'][eu]['estado'] == 'vivo': o = noticias.origem(E, estado.onde(E, eu)); perto_eu = {estado.onde(E, eu), o} | set(regiao.saltos(E, o, so_abertas=False)) if o else {estado.onde(E, eu)}
    for iid, it in list(E['itens']['itens'].items()):
        lid = it.get('onde')
        if not it.get('solto') or not it.get('corpo') or it['cat'] < 2 or it.get('dono') or not lid or E['lugares'].get(lid, {}).get('tipo') == 'sala' or lid in perto_eu: continue
        o = noticias.origem(E, lid); sal = regiao.saltos(E, o, so_abertas=False) if o else {}
        cands = [k for k in rivais(E) if sal.get(E['gente'][k]['lugar'], 99) <= 1 and not estado.fora(E, k)]
        if not cands: continue
        k = max(cands, key=lambda x: (E['gente'][x]['nivel'], x))
        estado.aplica(E, 'rival', [['item', iid, 'dono', 'poe', k], ['item', iid, 'historia', 'junta', f"Dia {E['relogio']['dia']}: achada com um corpo {estado.em(E, lid)}, passa a {E['gente'][k]['nome']}"]],
                      onde=lid, quem=[k], texto=f"{E['gente'][k]['nome']} fica com {it['nome']}, que estava com um corpo {estado.em(E, lid)}")


def _r_descansa(E, pid, ids, pl):
    p = E['gente'][pid]; ef = []
    if p['pv'] < estado.pv_max(p): ef.append(['pessoa', pid, 'pv', 'soma', estado.pv_max(p) - p['pv']])
    ef += [['ferida', pid, 'sara', i] for i in reversed(range(len(p.get('feridas') or [])))]
    if ef: estado.aplica(E, 'rival', ef, onde=p['lugar'], quem=[pid], texto=f"{p['nome']} sara")


def _r_caca(E, pid, ids, pl):
    p = E['gente'][pid]; rs = estado.sorte(E, f'rival|caca|{pid}'); lid = p['lugar']
    if rs.random() < R.RIVAL['caca_morre'][faixa(p)]:          # a caça para viver também mata (a decisão 11: a de começo mata um em cada cinco por mês)
        return _perde(E, [pid], 0.0, lid, rs, 'caçando para viver')
    v = rs.randint(*R.RIVAL['caca_rende'])
    v = int(min(v, E['lugares'][lid]['estoque'].get('prata', 0) * 0.02))
    if v > 0: estado.aplica(E, 'rival', [['estoque', lid, 'prata', 'soma', -v], ['pessoa', pid, 'moedas', 'soma', v], ['estoque', lid, 'couro:0', 'soma', 2]], onde=lid, quem=[pid], texto=f"{p['nome']} vende o que caçou")


def _r_missao(E, pid, ids, pl):
    import missoes
    m = missoes.todas(E).get(pl['alvo'])
    if not m or m['estado'] != 'tomada' or m.get('quem') != pid: return
    rs = estado.sorte(E, f"rival|missao|{pl['alvo']}")
    if m['tipo'] == 'investigar':                            # o olho, e não a espada: abre o que a frente esconde (dois campos), ou volta sem nada
        q = E['gente'][pid]; c = min(0.8, R.RIVAL['olho'] + (q['atributos']['Percepção'] - 50) / 100 + 0.06 * (q.get('maestria') or {}).get('manha', 0)); fid = m.get('frente')
        if rs.random() < c and fid:
            estado.aplica(E, 'rival', [['mundo', 'frentes', fid, 'exposta', 'poe', dict(dia=E['relogio']['dia'], quem=pid)]], quem=[pid], texto=f"{q['nome']} descobre o que há por trás da frente")
            missoes.cumpre(E, pl['alvo'], pid, tipo_ev='rival')        # a missão cumprida tira um passo (o missoes.cumpre faz o recua); a frente exposta perde o segredo: agora se caça o dono
        else: missoes.larga(E, pid, pl['alvo'])
        return
    B = _ameaca_missao(E, m, rs)
    if not B:                                                # o alvo já não está lá (outro limpou, matou): a missão perde o sentido; quem a tomou volta
        return estado.aplica(E, 'rival', [['mundo', 'missoes', pl['alvo'], 'estado', 'poe', 'falhou']], quem=[pid], texto=f"a missão {pl['alvo']} perde o alvo antes de {E['gente'][pid]['nome']} chegar")
    c = chance_contra(E, ids, B) if B else 0.0
    onde = m.get('ermo') or m['onde']
    if m['tipo'] == 'limpar' and m['alvo'] in E['lugares']:   # a limpeza é a descida mesma (nível a nível, pela conta): cumpre quem chega ao fundo vivo
        _limpa(E, pid, ids, m['alvo'], rs)
        lp = E['lugares'][m['alvo']].get('limpa') or {}
        if E['gente'][pid]['estado'] == 'vivo' and pid in (lp.get('quem') or []): missoes.cumpre(E, pl['alvo'], pid, tipo_ev='rival')
        elif E['gente'][pid]['estado'] == 'vivo': missoes.larga(E, pid, pl['alvo'])
        else: estado.aplica(E, 'rival', [['mundo', 'missoes', pl['alvo'], 'estado', 'poe', 'falhou']], texto=f"a missão {pl['alvo']} falhou: quem a tomou morreu")
        return
    if rs.random() < c:
        if m['tipo'] == 'caça' and m.get('ermo') in E['lugares']:
            b = (E['lugares'][m['ermo']].get('bichos') or {}).get(m['alvo'], 0); q = min(b, m['n'])
            if q: estado.aplica(E, 'rival', [['lugar', m['ermo'], f"bichos.{m['alvo']}", 'soma', -q]], onde=m['ermo'], quem=ids, texto=f"{E['gente'][pid]['nome']} mata {q} {estado.especie(m['alvo']).get('plural') or m['alvo']}")
        if m['tipo'] == 'matar' and m.get('frente'): _mata_dono(E, pid, ids, (E['mundo'].get('frentes') or {}).get(m['frente']) or {})
        if m['tipo'] != 'matar' or ((E['mundo'].get('frentes') or {}).get(m.get('frente')) or {}).get('fim') == 'barrada' or not m.get('frente'):
            missoes.cumpre(E, pl['alvo'], pid, tipo_ev='rival')
    else:
        _perde(E, ids, c, onde, rs, f"na missão {pl['alvo']}")
        if E['gente'][pid]['estado'] == 'vivo': missoes.larga(E, pid, pl['alvo'])
        else: estado.aplica(E, 'rival', [['mundo', 'missoes', pl['alvo'], 'estado', 'poe', 'falhou']], texto=f"a missão {pl['alvo']} falhou: quem a tomou morreu")


def _mata_dono(E, pid, ids, f):
    d = f.get('dono'); k, _, v = str(d).partition(':')
    if d in E['gente'] and E['gente'][d]['estado'] == 'vivo':
        estado.aplica(E, 'rival', [['pessoa', d, 'estado', 'poe', 'morto'], ['pessoa', pid, 'fama', 'soma', 6]], onde=E['gente'][d]['lugar'], quem=ids + [d], texto=f"{E['gente'][pid]['nome']} mata {E['gente'][d]['nome']}")
    elif k == 'esp':
        esp, _, er = v.partition('@')
        if ((E['lugares'].get(er) or {}).get('bichos') or {}).get(esp, 0) > 0: estado.aplica(E, 'rival', [['lugar', er, f'bichos.{esp}', 'soma', -1], ['pessoa', pid, 'fama', 'soma', 6]], onde=er, quem=ids, texto=f"{E['gente'][pid]['nome']} mata o {esp} {estado.em(E, er)}")
    elif k == 'dragao' and isinstance((E['lugares'].get(v) or {}).get('dragao'), dict):
        estado.aplica(E, 'rival', [['lugar', v, 'dragao', 'poe', None], ['pessoa', pid, 'fama', 'soma', 15]], onde=v, quem=ids, texto=f"{E['gente'][pid]['nome']} mata o dragão {estado.em(E, v)}")


def _limpa(E, pid, ids, mid, rs, ate=None):
    """a descida que deu certo (nível a nível, até onde a conta deixar): quem mora sai, o tesouro (a prata livre e as peças guardadas) muda de mão, o chefe morre
    (e dá o núcleo, do Épico para cima); limpa até o fundo, é a primeira limpeza (a janela do mundo)"""
    import itens, noticias
    m = E['lugares'][mid]; feitos = 0
    for nv in m['niveis'][:ate]:
        c = chance_contra(E, [k for k in ids if E['gente'][k]['estado'] == 'vivo'], ameaca_nivel(E, mid, nv, rs))
        if rs.random() >= c:
            _perde(E, [k for k in ids if E['gente'][k]['estado'] == 'vivo'], c, nv['salas'][0], rs, f"descendo {estado.de(E, mid)}")
            return feitos
        ef = []; prata = 0
        for s in nv['salas']:
            l = E['lugares'][s]
            for esp, q in (l.get('bichos') or {}).items():
                if isinstance(q, (int, float)) and q >= 1: ef.append(['lugar', s, f'bichos.{esp}', 'soma', -int(q)])
            ch = l.get('chefe')
            if isinstance(ch, dict) and ch.get('vivo'):
                ef.append(['lugar', s, 'chefe', 'poe', dict(ch, vivo=False)])
                if nv['cat'] >= 3: ef.append(['item', 'nasce', itens.item('nucleo', nv['cat'], f"núcleo {T.CATS[nv['cat']]} {estado.de_nome(ch['qual'])}", dono=pid, de=ch['qual'], historia=[f"Dia {E['relogio']['dia']}: tirado {estado.de_nome(ch['qual'])} por {E['gente'][pid]['nome']} {estado.em(E, mid)}"])])
            livre = estado.livre(E, s).get('prata', 0)
            if livre: ef.append(['estoque', s, 'prata', 'soma', -livre]); prata += livre
            if isinstance(l.get('guardado'), dict) and not l['guardado'].get('aberto'): ef.append(['lugar', s, 'guardado', 'poe', dict(l['guardado'], aberto=True)])
            for iid, it in E['itens']['itens'].items():          # o tesouro guardado, e o que ficou com o corpo de quem caiu ali antes (fora da cena, quem limpa leva)
                if it.get('onde') == s and it.get('tipo') != 'chave' and (not it.get('solto') or it.get('corpo')):
                    ef.append(['item', iid, 'dono', 'poe', pid]); ef.append(['item', iid, 'historia', 'junta', f"Dia {E['relogio']['dia']}: tirada {estado.de(E, mid)} por {E['gente'][pid]['nome']}"])
        vivos = [k for k in ids if E['gente'][k]['estado'] == 'vivo']
        if prata and vivos:
            cada, resto = divmod(prata, len(vivos)); ef += [['pessoa', k, 'moedas', 'soma', cada + (1 if i < resto else 0)] for i, k in enumerate(vivos)]
        ef.append(['pessoa', pid, 'fama', 'soma', 2 + nv['cat']])
        estado.aplica(E, 'rival', ef, onde=mid, quem=vivos, texto=f"{E['gente'][pid]['nome']} limpa o nível {nv['n']} {estado.de(E, mid)}" + (f" ({prata} de prata)" if prata else ''))
        feitos += 1
    if feitos == len(m['niveis']) and not E['lugares'][mid].get('limpa'):
        vivos = [k for k in ids if E['gente'][k]['estado'] == 'vivo']; txt = f"{E['gente'][pid]['nome']} limpou {E['lugares'][mid]['nome']} pela primeira vez"
        chefe = next((x['chefe']['qual'] for s in m['niveis'][-1]['salas'] if isinstance((x := E['lugares'][s]).get('chefe'), dict)), '')
        estado.aplica(E, 'rival', [['lugar', mid, 'limpa', 'poe', dict(dia=E['relogio']['dia'], quem=vivos, chefe=chefe)], ['pessoa', pid, 'fama', 'soma', 10],
                                   ['mundo', 'janela', 'junta', dict(dia=E['relogio']['dia'], texto=txt)]] + noticias.nova(E, mid, txt, 3, ('janela', 'masmorra'), janela=True),
                      onde=mid, quem=vivos, texto=txt)
    return feitos


def _r_masmorra(E, pid, ids, pl):
    if E['lugares'].get(pl['alvo'], {}).get('limpa'): return
    _limpa(E, pid, ids, pl['alvo'], estado.sorte(E, f"rival|desce|{pid}|{pl['alvo']}"))


def limpa_da_guilda(E, gid, mid):
    """o desfecho da frente da corrida: a guilda limpa a masmorra (pela conta, nível a nível)"""
    ids = [k for k in rivais(E) if E['gente'][k].get('guilda') == gid]
    if ids and mid in E['lugares'] and not E['lugares'][mid].get('limpa'):
        lider = max(ids, key=lambda k: E['gente'][k]['nivel']); _limpa(E, lider, [lider] + [k for k in ids if k != lider][:3], mid, estado.sorte(E, f'guilda|{gid}|{mid}'))


def _r_chefe(E, pid, ids, pl):
    import itens, noticias
    e, _, esp = pl['alvo'].partition('|'); rs = estado.sorte(E, f"rival|chefe|{pid}|{e}")
    if (E['lugares'].get(e, {}).get('bichos') or {}).get(esp, 0) < 1: return
    c = chance_contra(E, ids, _bando(esp, 1, rs))
    if rs.random() < c:
        cat = estado.especie(esp)['cat']; txt = f"{E['gente'][pid]['nome']} mata {estado.especie(esp)['nome']} {estado.em(E, e)}" + noticias.sinete(E, pid)       # (fase 1a) o sinete da arma vai na notícia
        estado.aplica(E, 'rival', [['lugar', e, f'bichos.{esp}', 'soma', -1], ['pessoa', pid, 'fama', 'soma', 3 + cat],
                                   ['item', 'nasce', itens.item('nucleo', cat, f"núcleo {T.CATS[cat]} {estado.de_nome(estado.especie(esp)['nome'])}", dono=pid, de=esp, historia=[f"Dia {E['relogio']['dia']}: tirado por {E['gente'][pid]['nome']} {estado.em(E, e)}"])]]
                      + noticias.nova(E, e, txt, 2, ('rival',)), onde=e, quem=ids, texto=txt)
    else: _perde(E, ids, c, e, rs, f"contra {estado.especie(esp)['nome']}")


def _r_forja(E, pid, ids, pl):
    """a peça do núcleo, pelo melhor ferreiro da capital: a chance pela maestria dele; inteira, a peça nasce na categoria do núcleo; por pouco, uma abaixo; senão, o núcleo se perde"""
    import itens, mercado, noticias
    p = E['gente'][pid]; nu = E['itens']['itens'].get(pl['alvo'])
    if not nu or nu.get('dono') != pid: return
    cap = next((k for k, l in E['lugares'].items() if l.get('tipo') == 'capital'), p['lugar'])
    ferr = max((k for k, q in E['gente'].items() if q.get('papel') == 'ferreiro' and q['estado'] == 'vivo' and q['lugar'] == cap), key=lambda k: (E['gente'][k].get('maestria') or {}).get('forja', 0), default=None)
    ma = (E['gente'][ferr].get('maestria') or {}).get('forja', 4) if ferr else 4; ch = R.RIVAL['forja_chance'].get(ma, 0.25) * (0.75 ** max(0, nu['cat'] - 3))      # cada categoria acima do Épico, mais difícil
    rs = estado.sorte(E, f"rival|forja|{pid}|{pl['alvo']}"); x = rs.random(); cat = nu['cat']
    usa = next((it for it in pecas_em_uso(E, pid) if it['tipo'] in ('arma', 'foco')), None)
    novo_cat = cat if x < ch else cat - 1 if x < ch + 0.25 else None
    ef = [['item', pl['alvo'], 'some']]
    if novo_cat is not None:
        kw = dict(familia=usa.get('familia')) if usa and usa['tipo'] == 'arma' else dict(familia='espada')
        it = itens.item('arma', novo_cat, f"{(usa or {}).get('familia', 'espada').capitalize()} de {p['nome']}", dono=pid, historia=[f"Dia {E['relogio']['dia']}: forjada na capital com um núcleo, para {p['nome']}"], **kw)
        paga = int(min(p['moedas'], mercado.valor(itens.item('arma', nu['cat'], familia='espada')) * R.RIVAL['forja_paga'])); s0 = E['itens']['seq']
        ef += [['item', 'nasce', it]] + [['item', x['id'], 'uso', 'poe', None] for x in pecas_em_uso(E, pid) if x.get('uso') == 'arma'] + [['item', f"i{s0 + 1:04d}", 'uso', 'poe', 'arma']]
        if paga and ferr: ef += [['pessoa', pid, 'moedas', 'soma', -paga], ['pessoa', ferr, 'moedas', 'soma', paga]]
        txt = f"o ferreiro da capital forja para {p['nome']} uma peça {T.CATS[novo_cat]}"
        if novo_cat >= 4: ef += [['mundo', 'janela', 'junta', dict(dia=E['relogio']['dia'], texto=f"Nasce uma peça {T.CATS[novo_cat]}: {it['nome']}")]] + noticias.nova(E, cap, f"Nasce uma peça {T.CATS[novo_cat]}: {it['nome']}, de {p['nome']}", 3, ('janela', 'peça'), janela=True)
    else: txt = f"o núcleo de {p['nome']} se perde na forja"
    estado.aplica(E, 'rival', ef, onde=cap, quem=[pid] + ([ferr] if ferr else []), texto=txt)


# ---------- gente nova, ranking, torneio, leilão, janela ----------
def novos(E):
    """a cada estação, quem chega à idade de pegar em armas: novatos, nas vilas e cidades, com a prata que a família dá"""
    import gera, nomes, talento, pessoas, vila_teste, itens, regiao
    vivos = len(rivais(E)); falta = int((40 - vivos) * R.RIVAL['novos'])
    rs = estado.sorte(E, 'rival|novos'); N = nomes.Nomes(rs, usados=[g['nome'] for g in E['gente'].values()])
    for _ in range(max(0, falta)):
        lid = rs.choice([k for k in regiao.povoados(E) if E['lugares'][k]['tipo'] in ('vila', 'cidade', 'capital') and E['lugares'][k]['estoque'].get('prata', 0) > 50])
        nome = N.gente('humano'); pid = gera.slug(nome, set(E['gente'])); nivel = rs.randint(5, 10); fam = rs.choice(['espada', 'lança', 'machado', 'arco'])
        at = pessoas.padrao(nome, nivel, molde='arqueiro' if fam == 'arco' else 'guerreiro')['atributos']; ma = {fam: 2}; prata = 20
        reg = talento.nasce(E, pid, dict(nome=nome, nivel=nivel, atributos=at, lugar=lid, grau_oficio='oficial', maestria=ma, treino=vila_teste.treino_da_mao(ma), moedas=0,
                                         sobre='aventureiro novato, anda sozinho', papel='aventureiro', rival=True, fama=0, idade=16 + rs.randint(0, 6)))
        s0 = E['itens']['seq']
        estado.aplica(E, 'gera', [['pessoa', 'nasce', pid, reg], ['estoque', lid, 'prata', 'soma', -prata], ['pessoa', pid, 'moedas', 'soma', prata],
                                  ['item', 'nasce', itens.item('arma', 0, f'{fam.capitalize()} de {nome}', familia=fam, dono=pid)], ['item', 'nasce', itens.item('armadura', 0, f'Couro de {nome}', material='couro', dono=pid)],
                                  ['item', f'i{s0 + 1:04d}', 'uso', 'poe', 'arma'], ['item', f'i{s0 + 2:04d}', 'uso', 'poe', 'veste']], onde=lid, quem=[pid], texto=f"{nome} chega à idade de pegar em armas {estado.em(E, lid)}")
        import habilidade                                   # (a parte 2, fase 2) e com as habilidades que a mão e a vida explicam, pela semente (o novato de mão Iniciante: nenhuma)
        hv = habilidade.efeitos_da_vida(E, pid)
        if hv: estado.aplica(E, 'gera', hv, onde=lid, quem=[pid], texto=f"{nome} traz da vida {len(hv)} habilidade(s)")


def ranking(E):
    L = sorted(((k, pontos(E, k)) for k in rivais(E)), key=lambda x: -x[1])[:10]
    if not L: return
    R0 = E['mundo'].get('ranking') or {}; troca = 1 if R0.get('lider') and R0['lider'] != L[0][0] else 0
    estado.aplica(E, 'semana', [['mundo', 'ranking', 'semana', 'poe', (E['relogio']['dia'] - 1) // M.SEMANA + 1], ['mundo', 'ranking', 'lista', 'poe', [[k, v] for k, v in L]],
                                ['mundo', 'ranking', 'lider', 'poe', L[0][0]], ['mundo', 'ranking', 'trocas', 'poe', (R0.get('trocas') or 0) + troca]], texto='o ranking da semana')


def torneio(E):
    """o torneio do rei, na capital: os 8 do ranking, em chave; a luta é a conta rápida (um contra um); quem vence leva a fama e o prêmio (da bolsa do senhor da capital)"""
    import noticias, conta
    cap = next((k for k, l in E['lugares'].items() if l.get('tipo') == 'capital'), None); lista = [k for k, _ in (E['mundo'].get('ranking') or {}).get('lista', [])][:8]
    lista = [k for k in lista if E['gente'].get(k, {}).get('estado') == 'vivo' and not estado.fora(E, k)]
    if len(lista) < 4 or not cap: return
    rs = estado.sorte(E, 'torneio'); rodada = lista
    while len(rodada) > 1:
        prox = []
        for a, b in zip(rodada[::2], rodada[1::2]):
            c = conta.chance(_lutadores(E, [a]), _lutadores(E, [b])); prox.append(a if rs.random() < c else b)
        if len(rodada) % 2: prox.append(rodada[-1])
        rodada = prox
    v = rodada[0]; senhor = next((k for k, q in E['gente'].items() if q.get('papel') == 'senhor' and q['lugar'] == cap and q['estado'] == 'vivo'), None)
    premio = int(min(R.RIVAL['torneio_premio'], E['gente'][senhor]['moedas'])) if senhor else 0
    txt = f"{E['gente'][v]['nome']} vence o torneio do rei {estado.em(E, cap)}"
    estado.aplica(E, 'torneio', [['pessoa', v, 'fama', 'soma', 20]] + ([['pessoa', senhor, 'moedas', 'soma', -premio], ['pessoa', v, 'moedas', 'soma', premio]] if premio else [])
                  + [['mundo', 'janela', 'junta', dict(dia=E['relogio']['dia'], texto=txt)]] + noticias.nova(E, cap, txt, 3, ('janela', 'torneio'), janela=True), onde=cap, quem=[v], texto=txt)


def lotes(E):
    """o que vai ao leilão da capital: as peças Únicas ou maiores e os núcleos que os rivais guardam sem usar"""
    return [i for i, it in E['itens']['itens'].items() if it.get('dono') in E['gente'] and E['gente'][it['dono']].get('rival') and not it.get('uso') and (it['cat'] >= 4 or it['tipo'] == 'nucleo')]


def leilao(E):
    import mercado, noticias
    cap = next((k for k, l in E['lugares'].items() if l.get('tipo') == 'capital'), None)
    if not cap: return
    L = lotes(E); lances = (E['mundo'].get('leilao') or {}).get('lances') or {}; eu = estado.eu(E); feitos = []
    for iid in L[:6]:
        it = E['itens']['itens'][iid]; dono = it['dono']; base = int(mercado.valor(dict(it, tipo='arma') if it['tipo'] == 'nucleo' else it) * 0.5)
        cand = [(min(E['gente'][k]['moedas'], int(base * 1.5)), k) for k in rivais(E) if k != dono and E['gente'][k]['moedas'] >= base and not estado.fora(E, k)]
        if eu and str(lances.get(iid, {}).get('quem')) == eu and E['gente'][eu]['lugar'] == cap and E['gente'][eu]['moedas'] >= lances[iid]['valor'] >= base: cand.append((lances[iid]['valor'], eu))
        if not cand: continue
        v, k = max(cand)
        estado.aplica(E, 'leilao', [['item', iid, 'dono', 'poe', k], ['pessoa', k, 'moedas', 'soma', -v], ['pessoa', dono, 'moedas', 'soma', v],
                                    ['item', iid, 'historia', 'junta', f"Dia {E['relogio']['dia']}: vendida no leilão da capital a {E['gente'][k]['nome']}, por {v} de prata"]],
                      onde=cap, quem=[k, dono], texto=f"no leilão da capital, {it['nome']} vai para {E['gente'][k]['nome']} por {v} de prata"); feitos.append(it['nome'])
    if feitos: noticias.da(E, cap, f"O leilão da capital: {', '.join(feitos)}", 2, ('leilão',))
    if lances: estado.aplica(E, 'leilao', [['mundo', 'leilao', 'lances', 'poe', None]], texto='o leilão fecha os lances')


def janela(E):
    """a janela do mundo é escrita por quem faz o feito (a limpeza, a forja, a morte da Lenda, a frente que acaba); aqui não há o que fazer por dia"""
    return


def lance(E, iid, valor):
    eu = estado.eu(E) or sys.exit('não há personagem')
    if iid not in lotes(E): sys.exit(f'"{iid}" não está entre os lotes do próximo leilão (`rivais.py leilao`)')
    if E['gente'][eu]['moedas'] < valor: sys.exit(f"{E['gente'][eu]['nome']} tem {E['gente'][eu]['moedas']} de prata")
    L = dict((E['mundo'].get('leilao') or {}).get('lances') or {}); L[iid] = dict(quem=eu, valor=valor)
    estado.aplica(E, 'leilao', [['mundo', 'leilao', 'lances', 'poe', L]], quem=[eu], texto=f"{E['gente'][eu]['nome']} dá um lance de {valor} de prata em {E['itens']['itens'][iid]['nome']}")
    return 'lance guardado: vale no dia do leilão, na capital.'


def gera(E, r):
    ranking(E); return [f"O ranking do Dia 1: " + ', '.join(f"{E['gente'][k]['nome']} ({v})" for k, v in (E['mundo'].get('ranking') or {}).get('lista', [])[:5]) + '.']


def mesa(E):
    if not tem(E): return []
    eu = estado.eu(E)
    if not eu or E['gente'][eu]['estado'] != 'vivo': return []
    Rk = E['mundo'].get('ranking') or {}; L = Rk.get('lista') or []
    if not L: return []
    meu = pontos(E, eu)
    return [f"**O ranking da semana {Rk.get('semana', 1)}** (fama e peças): " + ' · '.join(f"{i + 1}. {E['gente'][k]['nome']} ({v})" for i, (k, v) in enumerate(L[:5])) + f" · você: {meu}"]


if __name__ == '__main__':
    import signal; hasattr(signal, 'SIGPIPE') and signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    a = sys.argv[1:]
    if not a or a[0] not in ('ranking', 'ver', 'mestre', 'leilao', 'lance'): print(__doc__); sys.exit()
    E = estado.carrega()
    if a[0] == 'ranking':
        for i, (k, v) in enumerate((E['mundo'].get('ranking') or {}).get('lista', [])): print(f"{i + 1}. {E['gente'][k]['nome']} [{k}] · {v} · {E['gente'][k].get('sobre', '')}")
    elif a[0] == 'ver':
        p = E['gente'].get(a[1] if len(a) > 1 else '') or sys.exit('use: `rivais.py ver PID`')
        print(f"{p['nome']} · nível {p['nivel']} · fama {p.get('fama', 0)} · {p.get('sobre', '')} · {estado.em(E, p['lugar'])}")
        for it in pecas_em_uso(E, a[1]): print(f"  {it['nome']} ({T.CATS[it['cat']]})")
    elif a[0] == 'mestre':
        for k in rivais(E, vivos=False):
            p = E['gente'][k]; hb = p.get('habilidades') or {}
            import habilidade, tabelas_habilidades as TH                # (a parte 2, fase 2) as habilidades escondidas: só o Mestre as vê
            print(f"- {p['nome']} [{k}] · nível {p['nivel']} · {p['estado']} · fama {p.get('fama', 0)} · {pontos(E, k)} pontos · plano: {plano(p)}"
                  + (f" · habilidades: {', '.join(f'{habilidade.nome(x)} {TH.CURTO[habilidade.grau_de(r)]}' for x, r in hb.items())}" if hb else ''))
    elif a[0] == 'leilao':
        for i in lotes(E): print(f"- {i} {E['itens']['itens'][i]['nome']} ({T.CATS[E['itens']['itens'][i]['cat']]}), de {E['gente'][E['itens']['itens'][i]['dono']]['nome']}")
    else:
        if len(a) != 3 or not a[2].isdigit(): sys.exit('use: `rivais.py lance ITEM PRATA`')
        print(lance(E, a[1], int(a[2]))); estado.grava(E)
