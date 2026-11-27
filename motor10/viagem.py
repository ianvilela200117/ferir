#!/usr/bin/env python3
"""viagem.py — MOTOR 10, ETAPA FINAL: A VIAGEM PELAS ESTRADAS. Ir de um lugar de povo ao vizinho é andar os blocos da estrada (esforço leve), com quem vai junto.
ENQUANTO A VIAGEM ESTÁ ABERTA, A GENTE ESTÁ NA ESTRADA (marca.viagem): os atos da vila são recusados; come-se da carga.
O ENCONTRO, a cada bloco, pelo acaso do mundo: a chance sai do perigo da estrada e dos salteadores contados nela (de noite, mais). Quem aparece sai da conta real:
os SALTEADORES da estrada (pedem pedágio; quem não paga, luta ou foge) ou um BICHO do ermo por onde a estrada passa. O que morre sai da conta (o bando da estrada,
os bichos do ermo). A prata dos salteadores é o estoque da estrada (o pedágio e o roubo vão para lá; quem os vence a reparte). A morte na estrada deixa tudo nela.

  python3 viagem.py ver                          a viagem aberta (ou as estradas daqui)
  python3 viagem.py ir DESTINO [com=ID,ID]       sai pela estrada até o lugar vizinho (o id ou o nome dele) e anda até chegar ou até algo aparecer
  python3 viagem.py pagar                        paga o pedágio aos salteadores e segue
  python3 viagem.py atacar [inicio=perto|longe]  ataca o que apareceu: monta a luta (a do ato.py luta) e mostra o quadro
  python3 viagem.py fugir                        foge (Agilidade de quem comanda, contra o bando): passando, volta ao lugar de onde saiu; falhando, luta surpreendido
  python3 viagem.py luta ["Nome: ordem"]...      roda a luta aberta; no fim, as contas (quem morreu sai da conta; o despojo; a prata do bando)
  python3 viagem.py segue                        segue o caminho                · python3 viagem.py volta    dá meia-volta (anda de volta o que já andou)
  python3 viagem.py acampa N                     dorme N blocos na estrada, no chão (o encontro pode vir de noite)
  python3 viagem.py larga "por quê"              SÓ O MESTRE: fecha a viagem sem as contas (todos ficam no lugar de onde saíram)
"""
import json, os, sys
import tabelas as T
import tabelas_mundo as M
import tabelas_regiao as R
import tabelas_bichos as TB
import estado, ato, corpo


def tem(E): return bool((E.get('mundo') or {}).get('meta'))
def _p(E, pid): return E['gente'][pid]
def minha(E, pid):
    """a viagem que a pessoa comanda (o registro), ou recusa"""
    v = (_p(E, pid).get('marca') or {}).get('viagem')
    if not isinstance(v, dict): sys.exit(f"{_p(E, pid)['nome']} não está viajando (`viagem.py ir DESTINO`)")
    if v.get('de') is not None: sys.exit(f"{_p(E, pid)['nome']} vai junto na viagem de {_p(E, v['de'])['nome']}: quem comanda é quem decide")
    return dict(v)


def _todos(E, pid, v): return [pid] + [c for c in v.get('com', []) if E['gente'].get(c, {}).get('estado') == 'vivo']


def _marca(E, pid, v, texto, mais=(), tipo='viagem'):
    estado.aplica(E, tipo, [['pessoa', pid, 'marca.viagem', 'poe', v]] + list(mais), onde=estado.onde(E, pid), quem=_todos(E, pid, v) if v else [pid], texto=texto)


def _destino(E, lid, alvo):
    import regiao
    for e, o in regiao.estradas(E, lid):
        nm = E['lugares'][o]['nome']
        if alvo in (o, e) or alvo.lower() in (nm.lower(), nm.lower().split(' ', 1)[-1]): return e, o
    return None, None


def ir(E, pid, alvo, com=()):
    p = estado.presente(E, pid, 'viajar'); lid = p['lugar']
    import regiao
    if not regiao.povoado(E, lid): sys.exit(f"{p['nome']} não está num lugar de povo: não há estrada daqui")
    e, o = _destino(E, lid, alvo)
    if not e: sys.exit(f"não há estrada {estado.de(E, lid)} para \"{alvo}\": as que há vão para " + ', '.join(E['lugares'][o2]['nome'] for e2, o2 in regiao.estradas(E, lid)))
    l = E['lugares'][e]
    if l.get('fechada'): sys.exit(f"{l['nome']} está FECHADA ({l['fechada'].get('por')}): não se passa")
    com = [c for c in com if c != pid]
    for c in com:
        q = E['gente'].get(c) or sys.exit(f'não há a pessoa "{c}"')
        if q['estado'] != 'vivo': sys.exit(f"{q['nome']} não vai: {estado.morte_diz(E, q)}")
        if q['lugar'] != lid or estado.fora(E, c): sys.exit(f"{q['nome']} não está {estado.em(E, lid)} (ou está fora): não vai junto")
        estado.em_cena(E, c)
    v = dict(estrada=e, sai=lid, para=o, feitos=0, longe=l['longe'], com=com, fase='anda')
    _marca(E, pid, v, f"{p['nome']} sai {estado.de(E, lid)} pela {l['nome'][2:]}" + (f", com {', '.join(E['gente'][c]['nome'] for c in com)}" if com else ''),
           mais=[['pessoa', c, 'marca.viagem', 'poe', dict(de=pid)] for c in com])
    return anda(E, pid)


def _chance(E, l):
    K = R.VIAGEM; c = K['base'].get(l.get('perigo', 1), 0.03) + l.get('bando', 0) * K['por_bando']
    return c * (K['noite'] if E['relogio']['bloco'] in M.ESCUROS else 1)


def _encontro(E, pid, v):
    """rola o encontro deste bloco (o acaso do mundo). Devolve o encontro, ou None"""
    l = E['lugares'][v['estrada']]; K = R.VIAGEM; rs = estado.sorte(E, f"viagem|{pid}|{v['estrada']}|{v['feitos']}")
    if rs.random() >= _chance(E, l): return None
    ermo = l.get('passa'); bichos_ = {}
    if ermo in E['lugares']:
        import caca
        bichos_ = {x: q for x, q in caca.bichos_de(E, ermo).items() if not (estado.especie(x) or {}).get('chefe') and (estado.especie(x) or {}).get('cat', 0) <= max(1, l.get('perigo', 1))}
    if bichos_ and (rs.random() < K['bicho'] or not l.get('bando')):
        esp = rs.choices(list(bichos_), [bichos_[x] for x in bichos_])[0]; lo, hi = estado.especie(esp).get('bando', (1, 1))
        return dict(tipo='bicho', especie=esp, n=min(bichos_[esp], rs.randint(lo, hi)), viu=rs.choice(['nós', 'eles']), ermo=ermo, escuro=E['relogio']['bloco'] in M.ESCUROS)
    if not l.get('bando'): return None
    n = min(l['bando'], rs.randint(*K['grupo'])); nivel = rs.randint(*K['nivel'].get(l.get('perigo', 1), (3, 8)))
    taxa = K['taxa_cabeca'] * len(_todos(E, pid, v)) + K['taxa_salteador'] * n
    return dict(tipo='bando', n=n, nivel=nivel, taxa=taxa, viu='eles', escuro=E['relogio']['bloco'] in M.ESCUROS)


def anda(E, pid):
    """anda os blocos que faltam, um a um, rolando o encontro; chega, ou para no encontro (ou no corpo que cobra)"""
    p = _p(E, pid); v = minha(E, pid); L = []
    if v['fase'] != 'anda': sys.exit(f"a viagem está em {v['fase']}: resolva antes (`viagem.py ver`)")
    while v['feitos'] < v['longe']:
        com = [c for c in v.get('com', []) if E['gente'].get(c, {}).get('estado') == 'vivo']
        enc = _encontro(E, pid, v)
        k, pq = ato.passa(E, pid, 1, 'viagem', esforco='leve', texto=f"{p['nome']} anda {estado.em(E, v['estrada'])}", com=com)
        v = minha(E, pid) if isinstance((_p(E, pid).get('marca') or {}).get('viagem'), dict) else v
        if _p(E, pid)['estado'] != 'vivo': return f"{p['nome']} morreu na estrada."
        v['feitos'] += k
        if enc:
            v.update(fase='encontro', encontro=enc); _marca(E, pid, v, f"{_diz_enc(E, enc)} {estado.em(E, v['estrada'])}")
            return '\n'.join(L + [le(E, pid)])
        _marca(E, pid, v, f"{p['nome']} anda {estado.em(E, v['estrada'])} ({v['feitos']} de {v['longe']} blocos)")
        if pq: return '\n'.join(L + [f"A viagem para: {pq}. `viagem.py segue` continua; `viagem.py acampa N` dorme na estrada; `ato.py comer carga` come da carga."])
    return chega(E, pid, L)


def chega(E, pid, L=()):
    v = minha(E, pid); todos = _todos(E, pid, v); ef = []
    for q in todos:
        andou = sorted(set(((E['gente'][q].get('marca') or {}).get('andou') or []) + [v['estrada']]))
        ef += [['pessoa', q, 'lugar', 'poe', v['para']], ['pessoa', q, 'marca.andou', 'poe', andou]]
    ef += [['pessoa', q, 'marca.viagem', 'poe', None] for q in todos[1:]]
    _marca(E, pid, None, f"{_e(E, todos)} {'chega' if len(todos) == 1 else 'chegam'} {estado.em(E, v['para']) if False else 'a ' + E['lugares'][v['para']]['nome']}", mais=ef)
    return '\n'.join(list(L) + [f"{_e(E, todos)} {'chegou' if len(todos) == 1 else 'chegaram'} a {E['lugares'][v['para']]['nome']} ({estado.quando(E)})."])


def _e(E, ids):
    n = [E['gente'][k]['nome'] for k in ids]
    return n[0] if len(n) == 1 else ', '.join(n[:-1]) + ' e ' + n[-1]


def _diz_enc(E, enc):
    if enc['tipo'] == 'bando': return f"{enc['n']} salteadores fecham o caminho e pedem {enc['taxa']} de prata"
    e = estado.especie(enc['especie']); nm = e['nome'] if enc['n'] == 1 else e.get('plural') or e['nome'] + 's'
    return f"aparece{'m' if enc['n'] > 1 else ''} {enc['n']} {nm}" + (' (viram vocês primeiro)' if enc['viu'] == 'eles' else ' (vocês viram primeiro)')


def le(E, pid):
    v = minha(E, pid); enc = v.get('encontro') or {}
    if v['fase'] != 'encontro': return ver(E, pid)
    if enc['tipo'] == 'bando':
        return (f"NA ESTRADA ({v['feitos']} de {v['longe']} blocos): {enc['n']} salteadores (nível perto de {enc['nivel']}, espada ou lança e couro) fecham o caminho e pedem "
                f"{enc['taxa']} de prata para deixar passar. `viagem.py pagar` · `viagem.py atacar` · `viagem.py fugir` (Agilidade contra {R.VIAGEM['fuga'] + enc['n']}).")
    import bichos
    return f"NA ESTRADA ({v['feitos']} de {v['longe']} blocos): {_diz_enc(E, enc)}.\n{bichos.ameaca(enc['especie'], n=enc['n'])}\n`viagem.py atacar` · `viagem.py fugir`."


def pagar(E, pid):
    v = minha(E, pid); enc = v.get('encontro') or {}; p = _p(E, pid)
    if v['fase'] != 'encontro' or enc.get('tipo') != 'bando': sys.exit('não há pedágio a pagar')
    if p['moedas'] < enc['taxa']: sys.exit(f"{p['nome']} tem {p['moedas']} de prata; o bando pede {enc['taxa']}")
    v.update(fase='anda', encontro=None)
    _marca(E, pid, v, f"{p['nome']} paga {enc['taxa']} de prata aos salteadores {estado.em(E, v['estrada'])}", mais=[['pessoa', pid, 'moedas', 'soma', -enc['taxa']], ['estoque', v['estrada'], 'prata', 'soma', enc['taxa']]])
    return f"Pagou {enc['taxa']} de prata. O bando abre o caminho.\n" + anda(E, pid)


def fugir(E, pid):
    v = minha(E, pid); enc = v.get('encontro') or {}; p = _p(E, pid)
    if v['fase'] != 'encontro': sys.exit('não há de que fugir')
    rs = estado.sorte(E, f"viagem|fuga|{pid}|{v['estrada']}|{v['feitos']}"); t = rs.randint(1, 20) + rs.randint(1, 20) + p['atributos']['Agilidade'] // 10 + corpo.pena(p, estado.agora(E))
    contra = R.VIAGEM['fuga'] + enc.get('n', 1)
    if t >= contra:
        todos = _todos(E, pid, v)
        _marca(E, pid, None, f"{p['nome']} foge e volta para {E['lugares'][v['sai']]['nome']} (Agilidade {t} contra {contra})", mais=[['pessoa', q, 'marca.viagem', 'poe', None] for q in todos[1:]])
        return f"Fugiu (Agilidade {t} contra {contra}): voltou para {E['lugares'][v['sai']]['nome']}."
    return f"A fuga falhou (Agilidade {t} contra {contra}): o que estava à frente pega vocês desprevenidos.\n" + _luta_abre(E, pid, 'perto', 'A')


def atacar(E, pid, inicio=None):
    v = minha(E, pid); enc = v.get('encontro') or {}
    if v['fase'] != 'encontro': sys.exit('não há o que atacar')
    surp = 'B' if enc.get('viu') == 'nós' else None
    return _luta_abre(E, pid, inicio or ('longe' if enc.get('viu') == 'nós' else 'perto'), surp)


def _luta_abre(E, pid, ini, surp):
    import bichos
    v = minha(E, pid); enc = dict(v['encontro']); rs = estado.sorte(E, f"viagem|luta|{pid}|{v['estrada']}|{v['feitos']}")
    if enc['tipo'] == 'bando':
        cat = 1 if E['lugares'][v['estrada']].get('perigo', 1) >= 3 and rs.random() < 0.3 else 0
        B = [dict(nome=f"salteador {i + 1}", nivel=enc['nivel'], molde=rs.choice(['guerreiro', 'guerreiro', 'arqueiro']),
                  veste=dict(arma=[rs.choice(['espada', 'lança', 'machado', 'adaga']), T.CATS[cat]], armadura=['couro', T.CATS[0]])) for i in range(enc['n'])]
        for b in B:
            if b['molde'] == 'arqueiro': b['veste']['arma'] = ['arco', T.CATS[0]]; b['linha'] = 'trás'
    else:
        B = bichos.bando(enc['especie'], rs, n=enc['n'])
        if enc['especie'] not in TB.ESPECIES:
            import criaturas
            B = [criaturas.no_cenario(b) for b in B]
    A = [dict(id=pid, controla=True)] + [dict(id=c) for c in v.get('com', []) if E['gente'].get(c, {}).get('estado') == 'vivo']
    pasta = os.path.join(estado.pasta(), 'lutas'); os.makedirs(pasta, exist_ok=True); base = os.path.join(pasta, f"viagem_{pid}_d{E['relogio']['dia']}b{E['relogio']['bloco']}")
    json.dump(dict(inicio=ini, lugar={}, surpresa=surp, tempo=['escuro'] if enc.get('escuro') else [], luz=not enc.get('escuro'), ermo=enc.get('ermo'), A=A, B=B),
              open(base + '_cenario.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    quadro = ato.luta_nova(E, base + '_cenario.json', base + '_luta.json')
    v.update(fase='luta', luta=estado.arq_guarda(base + '_luta.json'), encontro=enc)
    _marca(E, pid, v, f"{_p(E, pid)['nome']} luta {estado.em(E, v['estrada'])} contra {_diz_enc(E, enc).split(' fecham')[0].split(' (')[0]}")
    return f"A LUTA ABRE (começa {ini}" + (', vocês surpreendidos' if surp == 'A' else ', eles surpreendidos' if surp == 'B' else '') + f").\n{quadro}\nSiga com `viagem.py luta \"{_p(E, pid)['nome']}: atacar\"`."


def luta(E, pid, ordens=()):
    v = minha(E, pid)
    if v['fase'] != 'luta': sys.exit('não há luta aberta nesta viagem')
    out = ato.luta_roda(E, v['luta'], list(ordens))
    S = json.load(open(estado.arq_abre(v['luta']), encoding='utf-8'))
    if S['fim']: out += '\n' + acerta(E, pid)
    return out


def acerta(E, pid):
    """A LUTA ACABOU: quem morreu sai da conta (o bando da estrada, os bichos do ermo); quem ficou com o campo reparte a prata do bando e o despojo dos bichos;
    quem perdeu o campo é roubado (os salteadores levam metade da prata de quem ficou vivo)"""
    import bichos, gente, noticias
    v = minha(E, pid); enc = v['encontro']; S = json.load(open(estado.arq_abre(v['luta']), encoding='utf-8')); campo = S['fim'] == 'A'
    if any(l['arq'] == v['luta'] and not l['fim'] for l in E['turno']['lutas']): ato.luta_fecha(E, S, estado.arq_abre(v['luta']))
    bs = [f for f in S['L'] if f['lado'] == 'B']; mortos = sum(1 for f in bs if f['estado'] == 'morto' or (campo and f['estado'] in ('caido', 'rendido')))
    ficaram = [f['id'] for f in S['L'] if f['lado'] == 'A' and f.get('id') in E['gente'] and f['estado'] in ('pe', 'caido') and E['gente'][f['id']]['estado'] == 'vivo'] if campo else []
    ef = []; L = []; est = v['estrada']; l = E['lugares'][est]
    if enc['tipo'] == 'bando':
        antes = max(1, l.get('bando', 0)); saem = min(mortos, l.get('bando', 0))
        if saem: ef.append(['lugar', est, 'bando', 'soma', -saem]); L.append(f"{saem} salteador(es) morreram: saem do bando da estrada.")
        bolsa = int(l['estoque'].get('prata', 0) * saem / antes) if saem else 0
        if campo and bolsa and ficaram:
            cada, resto = divmod(bolsa, len(ficaram)); ef.append(['estoque', est, 'prata', 'soma', -bolsa])
            ef += [['pessoa', q, 'moedas', 'soma', cada + (1 if i < resto else 0)] for i, q in enumerate(ficaram) if cada + (1 if i < resto else 0)]
            L.append(f"A bolsa dos salteadores mortos: {bolsa} de prata, repartida entre quem ficou com o campo.")
        if not campo:
            for f in S['L']:
                q = f.get('id')
                if f['lado'] == 'A' and q in E['gente'] and E['gente'][q]['estado'] == 'vivo' and E['gente'][q]['moedas'] > 1:
                    x = E['gente'][q]['moedas'] // 2; ef += [['pessoa', q, 'moedas', 'soma', -x], ['estoque', est, 'prata', 'soma', x]]; L.append(f"Os salteadores levam {x} de prata de {E['gente'][q]['nome']}.")
    else:
        esp = enc['especie']; ermo = enc.get('ermo'); saem = min(mortos, ((E['lugares'].get(ermo) or {}).get('bichos') or {}).get(esp, 0)) if ermo else 0
        if saem: ef.append(['lugar', ermo, f'bichos.{esp}', 'soma', -saem])
        if campo and ficaram and mortos:
            bens = {}
            for i in range(mortos):
                b, nuc = bichos.despojo(esp, estado.sorte(E, f"viagem|despojo|{pid}|{v['feitos']}|{i}"))
                for k2, q2 in b.items(): bens[k2] = bens.get(k2, 0) + q2
            for i, (k2, q2) in enumerate(bens.items()):
                cada, resto = divmod(q2, len(ficaram))
                for j, q in enumerate(ficaram):
                    n = cada + (1 if (j - i) % len(ficaram) < resto else 0)
                    if n: ef.append(['pessoa', q, 'carga.' + k2, 'soma', n])
            if bens: L.append('Despojo: ' + ', '.join(f"{q2} de {estado.nome_bem(k2)}" for k2, q2 in bens.items()) + '.')
    for q in ficaram[1:]: ef += gente.lembra(E, q, pid, 'lutou ao meu lado na estrada', 1)
    if mortos and campo: ef += noticias.nova(E, est, f"{E['gente'][pid]['nome']} venceu {'salteadores' if enc['tipo'] == 'bando' else 'bichos'} {estado.em(E, est)}" + noticias.sinete(E, pid), 1, ('estrada',))       # (fase 1a) o sinete da arma vai na notícia
    vivo = E['gente'][pid]['estado'] == 'vivo'
    if not vivo:
        v2 = None; L.append(f"{E['gente'][pid]['nome']} morreu {estado.em(E, est)}: o que levava fica na estrada.")
    elif campo or S['fim'] in ('impasse', 'empate'): v2 = dict(v, fase='anda', encontro=None, luta=None)
    else: v2 = None; L.append(f"Perderam o campo: voltam para {E['lugares'][v['sai']]['nome']}.")
    todos = _todos(E, pid, v)
    estado.aplica(E, 'viagem', ef + [['pessoa', pid, 'marca.viagem', 'poe', v2]] + ([['pessoa', q, 'marca.viagem', 'poe', None] for q in todos[1:]] if v2 is None else []),
                  onde=est, quem=todos, texto=f"as contas da luta {estado.em(E, est)}" + (': o campo é de quem viaja' if campo else ''))
    return '\n'.join(L + (['`viagem.py segue` continua o caminho.'] if v2 else []))


def segue(E, pid):
    v = minha(E, pid)
    if v['fase'] == 'luta':
        S = json.load(open(estado.arq_abre(v['luta']), encoding='utf-8'))
        if not S['fim']: sys.exit('a luta não acabou: `viagem.py luta "Nome: ordem"`')
        acerta(E, pid); v = minha(E, pid)
    if v['fase'] == 'encontro': sys.exit('há algo à frente: `viagem.py pagar`, `atacar` ou `fugir`')
    return anda(E, pid)


def volta(E, pid):
    v = minha(E, pid)
    if v['fase'] != 'anda': sys.exit('resolva antes o que está à frente')
    v.update(sai=v['para'], para=v['sai'], feitos=v['longe'] - v['feitos'])
    _marca(E, pid, v, f"{_p(E, pid)['nome']} dá meia-volta {estado.em(E, v['estrada'])}")
    return anda(E, pid)


def acampa(E, pid, n):
    v = minha(E, pid)
    if v['fase'] != 'anda': sys.exit('resolva antes o que está à frente')
    com = [c for c in v.get('com', []) if E['gente'].get(c, {}).get('estado') == 'vivo']
    for i in range(n):
        enc = _encontro(E, pid, dict(v, feitos=v['feitos'] + 100 + i))
        ato.passa(E, pid, 1, 'dormir', dorme='chao', texto=f"{_p(E, pid)['nome']} dorme {estado.em(E, v['estrada'])}", com=com, para=False)
        if enc:
            v.update(fase='encontro', encontro=dict(enc, viu='eles')); _marca(E, pid, v, f"{_diz_enc(E, enc)} no acampamento")
            return f"No meio do sono: {le(E, pid)}"
    return f"Dormiu {n} blocos na estrada. `viagem.py segue` continua."


def larga(E, pid, porque):
    p = _p(E, pid); v = (p.get('marca') or {}).get('viagem')
    if not isinstance(v, dict) or v.get('de') is not None: sys.exit(f"{p['nome']} não comanda viagem aberta")
    if v.get('fase') == 'luta':
        for l in E['turno']['lutas']:
            if l['arq'] == v.get('luta') and not l['fim']: l['fim'] = 'largada'
    todos = [pid] + [c for c in v.get('com', []) if c in E['gente']]
    estado.aplica(E, 'mestre', [['pessoa', q, 'marca.viagem', 'poe', None] for q in todos if isinstance((E['gente'][q].get('marca') or {}).get('viagem'), dict)], quem=todos,
                  texto=f"o Mestre fecha a viagem de {p['nome']}: {porque}")
    return 'A viagem foi fechada sem as contas.'


def ver(E, pid):
    p = _p(E, pid); v = (p.get('marca') or {}).get('viagem')
    if isinstance(v, dict) and v.get('de') is None:
        if v['fase'] == 'encontro': return le(E, pid)
        return f"{p['nome']} está {estado.em(E, v['estrada'])}, de {E['lugares'][v['sai']]['nome']} para {E['lugares'][v['para']]['nome']}: {v['feitos']} de {v['longe']} blocos ({v['fase']})."
    import regiao
    return '\n'.join(regiao.mesa(E)) or 'não há estrada daqui.'


def mesa(E):
    if not tem(E): return []
    eu = estado.eu(E)
    if not eu or E['gente'][eu]['estado'] != 'vivo': return []
    k = estado.viajante(E, eu)
    return [f"**A viagem:** {ver(E, k)}"] if k else []


if __name__ == '__main__':
    import signal; hasattr(signal, 'SIGPIPE') and signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    a = sys.argv[1:]; op = dict(x.split('=', 1) for x in a if '=' in x and not x.startswith('"')); pos = [x for x in a if x not in [f'{k}={v}' for k, v in op.items()]]
    cmds = ('ver', 'ir', 'pagar', 'atacar', 'fugir', 'luta', 'segue', 'volta', 'acampa', 'larga')
    if not pos or pos[0] not in cmds: print(__doc__); sys.exit()
    E = estado.carrega(); pid = op.get('quem') or estado.eu(E) or sys.exit('não há personagem')
    c = pos[0]
    if c == 'ver': print(ver(E, pid)); sys.exit()
    if c == 'ir':
        if len(pos) != 2: sys.exit('use: `viagem.py ir DESTINO [com=ID,ID]`')
        out = ir(E, pid, pos[1], [x for x in op.get('com', '').split(',') if x])
    elif c == 'atacar': out = atacar(E, pid, op.get('inicio'))
    elif c == 'luta': out = luta(E, pid, pos[1:])
    elif c == 'acampa':
        if len(pos) != 2 or not pos[1].isdigit(): sys.exit('use: `viagem.py acampa N`')
        out = acampa(E, pid, int(pos[1]))
    elif c == 'larga':
        if len(pos) != 2: sys.exit('use: `viagem.py larga "por quê"`')
        out = larga(E, pid, pos[1])
    else: out = {'pagar': pagar, 'fugir': fugir, 'segue': segue, 'volta': volta}[c](E, pid)
    estado.grava(E); print(out)
