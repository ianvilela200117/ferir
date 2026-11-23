#!/usr/bin/env python3
"""estado.py — MOTOR 10: O ESTADO DO MUNDO E O ÚNICO GRAVADOR.

O save é uma pasta (`mundo/`, ou a que estiver em MOTOR10_MUNDO) com: relogio.json · lugares.json · gente.json · itens.json
· turno.json · eventos.jsonl (o único histórico; o diário sai dele).
  CADA FATO NUM LUGAR SÓ: o dono de uma peça e onde ela está vestida moram só no itens.json; onde a pessoa está, só na ficha dela.
  SÓ `aplica()` MUDA O ESTADO. Um evento é {dia, bloco, tipo, onde, quem, efeitos, texto}; sem efeito, é recusado.
  Um efeito é uma operação tipada de uma lista fechada:
    ['relogio', blocos]                              o tempo anda
    ['pessoa', id, campo, 'soma'|'poe', valor]       moedas · pv · fome · sono · cansaco · lugar · estado · nivel · treino.X · maestria.X (X: arma ou ofício) · marca.X
                                                     · carga.BEM (o que a pessoa carrega: só 'soma', nunca abaixo de zero)
    ['lugar', id, campo ou campo.sub, 'soma'|'poe', valor]   um número ou uma marca do lugar (bichos.lobo, coleta.minério, oficina); 'soma' nunca abaixo de zero
    ['ferida', id, 'abre', parte, grave]  ·  ['ferida', id, 'repousa', n]  ·  ['ferida', id, 'sara', indice]
    ['estoque', lugar, bem, 'soma', valor]
    ['item', id, campo, 'poe'|'soma', valor]         dono · uso · dur
    ['item', 'nasce', registro]                      uma peça nova entra no Livro de Itens (o id sai da sequência); também núcleos (tipo 'nucleo')
    ['item', id, 'onde', 'poe', lugar]  ·  ['item', id, 'sob_medida', 'poe', {dono, grau}]  ·  ['item', id, 'historia', 'junta', 'texto']  ·  ['item', id, 'some']
    ['obra', 'abre', registro]  ·  ['obra', id, campo, 'soma'|'poe', valor]  ·  ['obra', id, 'fecha']      a obra em andamento (forja de vários dias)
  O que o Mestre inventa em cena entra por um evento "mestre", com os mesmos efeitos. Fora disso, não aconteceu.

Uso (para olhar): python3 estado.py valida | python3 estado.py eventos [N] | python3 estado.py pessoa ID
"""
import copy, hashlib, json, os, random, sys
import tabelas as T
import tabelas_mundo as M

AQUI = os.path.dirname(os.path.abspath(__file__))
ARQS = ('relogio', 'lugares', 'gente', 'itens', 'turno')
PARTES_VESTE = ('arma', 'arma2', 'escudo', 'veste')


def pasta(): return os.environ.get('MOTOR10_MUNDO') or os.path.join(AQUI, 'mundo')


# ---------- ler e gravar ----------
def carrega():
    p = pasta()
    if not os.path.exists(os.path.join(p, 'relogio.json')): sys.exit(f'não há mundo em {p} (falta o relogio.json)')
    E = {k: json.load(open(os.path.join(p, k + '.json'), encoding='utf-8')) for k in ARQS}
    E['_novos'] = []
    return E


def grava(E):
    """escreve o estado inteiro (cada arquivo de uma vez, por troca) e junta os eventos novos ao histórico"""
    p = pasta(); os.makedirs(p, exist_ok=True)
    for k in ARQS:
        tmp = os.path.join(p, k + '.json.tmp')
        json.dump(E[k], open(tmp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        os.replace(tmp, os.path.join(p, k + '.json'))
    if E['_novos']:
        with open(os.path.join(p, 'eventos.jsonl'), 'a', encoding='utf-8') as f:
            for ev in E['_novos']: f.write(json.dumps(ev, ensure_ascii=False) + '\n')
        E['_novos'] = []


def novo(semente=1):
    """um estado vazio (o gerador e as provas partem daqui)"""
    return dict(relogio=dict(semente=semente, dia=1, bloco=2, eventos=0), lugares={}, gente={}, itens=dict(seq=0, itens={}, oseq=0, obras={}),
                turno=dict(n=1, aberto=dict(dia=1, bloco=2), dados=[], lutas=[], perguntas=[], respondidas=[], notas=[]), _novos=[])


# ---------- o tempo e o acaso do mundo ----------
def agora(E): return (E['relogio']['dia'] - 1) * M.BLOCOS_DIA + E['relogio']['bloco']        # blocos desde o começo do mundo
def estacao(E): return M.ESTACOES[((E['relogio']['dia'] - 1) % M.ANO) // M.ESTACAO]
def quando(E):
    r = E['relogio']; return f"Dia {r['dia']}, {M.BLOCOS[r['bloco']]} ({r['bloco'] * M.BLOCO_HORAS}h) · {estacao(E)}"


def sorte(E, chave):
    """o acaso do MUNDO (não o dado do jogador): sai da semente, do dia, do bloco e de uma chave. Mesma semente, mesmo mundo; nunca se rola de novo."""
    r = E['relogio']; h = hashlib.sha256(f"{r['semente']}|{r['dia']}|{r['bloco']}|{chave}".encode()).digest()
    return random.Random(int.from_bytes(h[:8], 'big'))


def eu(E):
    """o id do personagem do jogador"""
    return next((k for k, p in E['gente'].items() if p.get('jogador')), None)


# ---------- o gravador ----------
CAMPOS = dict(moedas='soma', pv='soma', fome='soma', sono='soma', cansaco='soma', nivel='soma', lugar='poe', estado='poe')


def _erro(ef, porque): return f'efeito {json.dumps(ef, ensure_ascii=False)}: {porque}'


def _um(E, ef):
    """aplica UM efeito em E (que pode ser uma cópia de ensaio). Devolve None, ou o texto do erro."""
    if not isinstance(ef, (list, tuple)) or not ef: return _erro(ef, 'efeito vazio')
    v = ef[0]
    if v == 'relogio':
        if len(ef) != 2 or not isinstance(ef[1], int) or ef[1] < 1: return _erro(ef, 'o tempo anda 1 bloco ou mais')
        t = agora(E) + ef[1]; E['relogio']['dia'], E['relogio']['bloco'] = t // M.BLOCOS_DIA + 1, t % M.BLOCOS_DIA; return
    if v == 'pessoa':
        if len(ef) != 5: return _erro(ef, "use ['pessoa', id, campo, 'soma'|'poe', valor]")
        _, pid, campo, op, val = ef; p = E['gente'].get(pid)
        if not p: return _erro(ef, f'não há a pessoa "{pid}"')
        raiz, _, sub = campo.partition('.')
        if raiz == 'carga':
            if not sub or op != 'soma': return _erro(ef, "a carga muda por ['pessoa', id, 'carga.BEM', 'soma', valor]")
            d = p.setdefault('carga', {}); q = d.get(sub, 0) + val
            if q < 0: return _erro(ef, f'{p["nome"]} só carrega {d.get(sub, 0)} de {sub}')
            if q: d[sub] = q
            else: d.pop(sub, None)
            return
        if raiz in ('treino', 'maestria', 'marca'):
            if not sub: return _erro(ef, f'"{raiz}" pede o nome depois do ponto (treino.espada)')
            if raiz != 'marca' and sub not in T.FAMILIAS and sub not in M.OFICIOS: return _erro(ef, f'arma ou ofício desconhecido: "{sub}"')
            d = p.setdefault(raiz, {})
            if op == 'soma': d[sub] = d.get(sub, 0) + val
            elif op == 'poe': d[sub] = val
            else: return _erro(ef, 'a operação é "soma" ou "poe"')
            if raiz == 'maestria' and d[sub] not in T.MAESTRIAS: return _erro(ef, f'maestria fora da tabela: {d[sub]}')
            return
        if campo not in CAMPOS: return _erro(ef, f'campo desconhecido: "{campo}" (os que existem: {", ".join(CAMPOS)}, treino.ARMA, maestria.ARMA, marca.X)')
        if op != CAMPOS[campo]: return _erro(ef, f'"{campo}" só aceita "{CAMPOS[campo]}"')
        if campo == 'lugar':
            if val not in E['lugares']: return _erro(ef, f'não há o lugar "{val}"')
            p['lugar'] = val
        elif campo == 'estado':
            if val not in M.ESTADOS: return _erro(ef, f'estado desconhecido: "{val}"')
            p['estado'] = val
        elif campo in M.MEDIDORES: p['corpo'][campo] = max(0, min(M.MED_MAX, p['corpo'][campo] + val))
        elif campo == 'pv': p['pv'] = max(0, min(pv_max(p), p['pv'] + val))
        elif campo == 'moedas':
            if p['moedas'] + val < 0: return _erro(ef, f'{p["nome"]} tem {p["moedas"]} de prata e não paga {-val}')
            p['moedas'] += val
        else: p[campo] += val
        return
    if v == 'ferida':
        p = E['gente'].get(ef[1]) if len(ef) > 2 else None
        if not p: return _erro(ef, 'não há essa pessoa')
        if ef[2] == 'abre' and len(ef) == 5:
            if ef[3] not in T.PARTES: return _erro(ef, f'parte desconhecida: "{ef[3]}"')
            p['feridas'].append(dict(parte=ef[3], grave=bool(ef[4]), dia=E['relogio']['dia'], repouso=0)); return
        if ef[2] == 'repousa' and len(ef) == 4:
            for f in p['feridas']: f['repouso'] += ef[3]
            return
        if ef[2] == 'sara' and len(ef) == 4:
            if not 0 <= ef[3] < len(p['feridas']): return _erro(ef, 'não há essa ferida')
            p['feridas'].pop(ef[3]); return
        return _erro(ef, "use ['ferida', id, 'abre', parte, grave], ['ferida', id, 'repousa', n] ou ['ferida', id, 'sara', indice]")
    if v == 'lugar':
        if len(ef) != 5 or ef[3] not in ('soma', 'poe'): return _erro(ef, "use ['lugar', id, campo ou campo.sub, 'soma'|'poe', valor]")
        l = E['lugares'].get(ef[1])
        if not l: return _erro(ef, f'não há o lugar "{ef[1]}"')
        raiz, _, sub = ef[2].partition('.')
        if raiz in ('estoque', 'nome'): return _erro(ef, f'"{raiz}" não se muda por aqui (o estoque tem o verbo dele)')
        d = l.setdefault(raiz, {}) if sub else l; k = sub or raiz
        if ef[3] == 'poe': d[k] = ef[4]
        else:
            if not isinstance(d.get(k, 0), (int, float)) or isinstance(d.get(k, 0), bool): return _erro(ef, f'"{ef[2]}" não é número')
            q = d.get(k, 0) + ef[4]
            if q < 0: return _erro(ef, f'{l["nome"]} só tem {d.get(k, 0)} de {ef[2]}')
            d[k] = q
        return
    if v == 'obra':
        O = E['itens'].setdefault('obras', {})
        if len(ef) == 3 and ef[1] == 'abre':
            o = copy.deepcopy(ef[2])
            if not isinstance(o, dict) or o.get('quem') not in E['gente']: return _erro(ef, 'a obra pede um registro com "quem" (uma pessoa que existe)')
            E['itens']['oseq'] = E['itens'].get('oseq', 0) + 1; o['id'] = f"o{E['itens']['oseq']:04d}"; o.setdefault('dia', E['relogio']['dia']); O[o['id']] = o; return
        o = O.get(ef[1]) if len(ef) > 2 else None
        if not o: return _erro(ef, 'não há essa obra')
        if len(ef) == 3 and ef[2] == 'fecha': del O[ef[1]]; return
        if len(ef) == 5 and ef[3] == 'soma': o[ef[2]] = o.get(ef[2], 0) + ef[4]; return
        if len(ef) == 5 and ef[3] == 'poe': o[ef[2]] = ef[4]; return
        return _erro(ef, "use ['obra', 'abre', registro], ['obra', id, campo, 'soma'|'poe', valor] ou ['obra', id, 'fecha']")
    if v == 'estoque':
        if len(ef) != 5 or ef[3] != 'soma': return _erro(ef, "use ['estoque', lugar, bem, 'soma', valor]")
        l = E['lugares'].get(ef[1])
        if not l: return _erro(ef, f'não há o lugar "{ef[1]}"')
        q = l['estoque'].get(ef[2], 0) + ef[4]
        if q < 0: return _erro(ef, f'{l["nome"]} só tem {l["estoque"].get(ef[2], 0)} de {ef[2]}')
        l['estoque'][ef[2]] = q; return
    if v == 'item' and len(ef) == 3 and ef[1] == 'nasce':
        it = copy.deepcopy(ef[2])
        if not isinstance(it, dict) or it.get('tipo') not in ('arma', 'armadura', 'escudo', 'nucleo') or 'dur' not in it or 'cat' not in it or not it.get('nome'): return _erro(ef, 'o registro tem de sair do itens.item() (ou ser um núcleo: tipo, cat, nome, dur)')
        if it.get('dono') is not None and it['dono'] not in E['gente']: return _erro(ef, f'não há a pessoa "{it["dono"]}"')
        if it.get('onde') is not None and it['onde'] not in E['lugares']: return _erro(ef, f'não há o lugar "{it["onde"]}"')
        E['itens']['seq'] += 1; it['id'] = f"i{E['itens']['seq']:04d}"; it.setdefault('uso', None); E['itens']['itens'][it['id']] = it; return
    if v == 'item' and len(ef) == 3 and ef[2] == 'some':
        if ef[1] not in E['itens']['itens']: return _erro(ef, f'não há o item "{ef[1]}" no Livro de Itens')
        del E['itens']['itens'][ef[1]]; return
    if v == 'item':
        if len(ef) != 5: return _erro(ef, "use ['item', id, campo, 'poe'|'soma', valor], ['item', 'nasce', registro] ou ['item', id, 'some']")
        it = E['itens']['itens'].get(ef[1])
        if not it: return _erro(ef, f'não há o item "{ef[1]}" no Livro de Itens')
        _, _, campo, op, val = ef
        if campo == 'dono' and op == 'poe':
            if val is not None and val not in E['gente']: return _erro(ef, f'não há a pessoa "{val}"')
            it['dono'] = val; it['uso'] = None
            if val is not None: it['onde'] = None
            return
        if campo == 'onde' and op == 'poe':
            if val is not None and val not in E['lugares']: return _erro(ef, f'não há o lugar "{val}"')
            if val is not None and it.get('dono'): return _erro(ef, 'peça com dono não fica largada num lugar: tire o dono antes')
            it['onde'] = val; return
        if campo == 'sob_medida' and op == 'poe':
            if val is not None and not (isinstance(val, dict) and val.get('dono') and T.SOB_MEDIDA_GRAUS[0] <= val.get('grau', 0) <= T.SOB_MEDIDA_GRAUS[1]): return _erro(ef, 'o sob medida é {dono, grau de 1 a 4}, ou nada')
            it['sob_medida'] = val; return
        if campo == 'historia' and op == 'junta': it.setdefault('historia', []).append(str(val)); return
        if campo == 'nome' and op == 'poe' and val: it['nome'] = str(val); return
        if campo == 'uso' and op == 'poe':
            if val not in (None,) + PARTES_VESTE: return _erro(ef, f'uso desconhecido: "{val}" (arma, arma2, escudo, veste ou nada)')
            if val and not it.get('dono'): return _erro(ef, 'peça sem dono não se veste')
            tipo_certo = dict(arma='arma', arma2='arma', escudo='escudo', veste='armadura')
            if val and it['tipo'] != tipo_certo[val]: return _erro(ef, f'{it["nome"]} é {it["tipo"]}: não vai em "{val}"')
            it['uso'] = val; return
        if campo == 'dur' and op == 'soma': it['dur'][0] = max(0, min(it['dur'][1], it['dur'][0] + val)); return
        return _erro(ef, 'no item muda-se: dono, uso, onde, sob_medida, nome (poe) · dur (soma) · historia (junta)')
    return _erro(ef, f'verbo desconhecido: "{v}" (os que existem: relogio, pessoa, ferida, estoque, lugar, item, obra)')


def aplica(E, tipo, efeitos, onde=None, quem=(), texto=''):
    """A ÚNICA PORTA. Ensaia todos os efeitos numa cópia; se um falha, NADA muda e o erro sai com o motivo."""
    if tipo not in M.EVENTOS: sys.exit(f'evento desconhecido: "{tipo}" (os que existem: {", ".join(M.EVENTOS)})')
    if not efeitos: sys.exit(f'evento "{tipo}" sem efeito: recusado. O que não muda número não aconteceu.')
    ensaio = {k: copy.deepcopy(E[k]) for k in ARQS}
    for ef in efeitos:
        e = _um(ensaio, ef)
        if e: sys.exit(f'evento "{tipo}" recusado, nada mudou. {e}')
    ev = dict(id=E['relogio']['eventos'] + 1, dia=E['relogio']['dia'], bloco=E['relogio']['bloco'], tipo=tipo, onde=onde, quem=list(quem), efeitos=[list(x) for x in efeitos], texto=texto)
    for k in ARQS: E[k] = ensaio[k]
    E['relogio']['eventos'] = ev['id']; E['_novos'].append(ev)
    return ev


# ---------- ler o estado (ninguém guarda cópia: tudo sai daqui) ----------
def pv_max(p): return T.pv_max(p['atributos']['Vigor'], p['nivel'])


def pecas(E, pid):
    """{'arma': item, 'arma2': item, 'escudo': item, 'veste': [itens]} do que a pessoa veste agora (sai do Livro de Itens)"""
    out = dict(arma=None, arma2=None, escudo=None, veste=[])
    for it in E['itens']['itens'].values():
        if it.get('dono') == pid and it.get('uso'):
            if it['uso'] == 'veste': out['veste'].append(it)
            else: out[it['uso']] = it
    return out


def lutador(E, pid, **mais):
    """a pessoa pronta para o pessoas.ficha e o luta.nova: quem é, o que veste hoje, o PV, as feridas e a pena do corpo"""
    import corpo
    p = E['gente'][pid]; eq = pecas(E, pid)
    d = dict(id=pid, nome=p['nome'], nivel=p['nivel'], atributos=dict(p['atributos']), maestria=dict(p.get('maestria', {})), pv=p['pv'],
             feridas=[[f['parte'], f['grave']] for f in p['feridas']], pena=corpo.pena(p), fol_menos=corpo.folego_menos(p),
             equip=copy.deepcopy(dict(arma=eq['arma'], arma2=eq['arma2'], escudo=eq['escudo'], armaduras=eq['veste'])))    # cópia: a luta não mexe no Livro
    d.update(mais)
    return d


def valida(E):
    """os invariantes: o que nunca pode ser verdade. Devolve a lista dos problemas (vazia: tudo certo)."""
    P = []; r = E['relogio']
    if not (r['dia'] >= 1 and 0 <= r['bloco'] < M.BLOCOS_DIA): P.append(f'relógio fora: dia {r["dia"]}, bloco {r["bloco"]}')
    if sum(1 for p in E['gente'].values() if p.get('jogador')) > 1: P.append('há mais de um personagem do jogador')
    for pid, p in E['gente'].items():
        n = p.get('nome', pid)
        if p['lugar'] not in E['lugares']: P.append(f'{n} está num lugar que não existe: {p["lugar"]}')
        if p['moedas'] < 0: P.append(f'{n} tem moeda negativa: {p["moedas"]}')
        if p['estado'] not in M.ESTADOS: P.append(f'{n} tem estado desconhecido: {p["estado"]}')
        if not 0 <= p['pv'] <= pv_max(p): P.append(f'{n} tem PV fora da faixa: {p["pv"]} de {pv_max(p)}')
        if p['estado'] == 'vivo' and p['pv'] <= 0: P.append(f'{n} está vivo com PV zero')
        for m in M.MEDIDORES:
            if not 0 <= p['corpo'][m] <= M.MED_MAX: P.append(f'{n} tem {m} fora da faixa: {p["corpo"][m]}')
        for b, q in p.get('carga', {}).items():
            if q < 0: P.append(f'{n} carrega quantidade negativa de {b}')
        usos = [it['uso'] for it in E['itens']['itens'].values() if it.get('dono') == pid and it.get('uso') in ('arma', 'arma2', 'escudo')]
        for u in set(usos):
            if usos.count(u) > 1: P.append(f'{n} tem duas peças em "{u}"')
    for iid, it in E['itens']['itens'].items():
        if it.get('dono') is not None and it['dono'] not in E['gente']: P.append(f'{it["nome"]} ({iid}) tem dono que não existe: {it["dono"]}')
        if it.get('uso') and not it.get('dono'): P.append(f'{it["nome"]} ({iid}) está vestida sem dono')
        if it.get('uso') and it.get('dono') in E['gente'] and E['gente'][it['dono']]['estado'] == 'morto': P.append(f'{it["nome"]} ({iid}) está vestida num morto')
        if not 0 <= it['dur'][0] <= it['dur'][1]: P.append(f'{it["nome"]} ({iid}) tem durabilidade fora da faixa')
        if it.get('onde') is not None and it['onde'] not in E['lugares']: P.append(f'{it["nome"]} ({iid}) está num lugar que não existe: {it["onde"]}')
        if it.get('onde') is not None and it.get('dono'): P.append(f'{it["nome"]} ({iid}) tem dono e está largada num lugar ao mesmo tempo')
    for oid, o in E['itens'].get('obras', {}).items():
        if o.get('quem') not in E['gente'] or E['gente'][o['quem']]['estado'] == 'morto': P.append(f'a obra {oid} é de alguém que não existe ou morreu')
    for lid, l in E['lugares'].items():
        for b, q in l['estoque'].items():
            if q < 0: P.append(f'{l["nome"]} tem estoque negativo de {b}')
        for campo in ('bichos', 'coleta'):
            for b, q in l.get(campo, {}).items():
                if q < 0: P.append(f'{l["nome"]} tem {campo} negativo de {b}')
    return P


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[:1] == ['valida']:
        P = valida(carrega()); print('\n'.join(P) if P else 'o estado está inteiro.'); sys.exit(1 if P else 0)
    elif a[:1] == ['eventos']:
        arq = os.path.join(pasta(), 'eventos.jsonl'); n = int(a[1]) if len(a) > 1 else 15
        for l in (open(arq, encoding='utf-8').read().splitlines()[-n:] if os.path.exists(arq) else []):
            ev = json.loads(l); print(f"#{ev['id']} Dia {ev['dia']}, {M.BLOCOS[ev['bloco']]} · {ev['tipo']}" + (f" · {ev['texto']}" if ev['texto'] else '') + f" · {len(ev['efeitos'])} efeito(s)")
    elif a[:1] == ['pessoa'] and len(a) > 1:
        E = carrega(); p = E['gente'].get(a[1]) or sys.exit(f'não há a pessoa "{a[1]}"')
        import pessoas
        print(pessoas.linha(pessoas.ficha(lutador(E, a[1])))); print(f"  corpo: {p['corpo']} · feridas: {p['feridas']} · prata: {p['moedas']} · em {E['lugares'][p['lugar']]['nome']}")
    else: print(__doc__)
