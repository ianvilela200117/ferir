#!/usr/bin/env python3
"""cria.py — MOTOR 10, ETAPA FINAL: O PERSONAGEM NASCE NO MUNDO, DENTRO DE UMA CASA. O mundo já é velho; o personagem é de uma família que existe nele
(com parentes vivos, um lugar, um ofício) e nasce pelo dado do mundo (uma vez): os atributos do berço mais os do povo, o talento e o dom com a inclinação, a idade.
A VIDA É UMA SÓ: em vida, nomeia-se um herdeiro (um parente, um aprendiz, um jurado); morto o personagem, o jogo segue com ele (`herda`), e quem matou vira o nêmesis.

  python3 cria.py ofertas                                    os povos, os seis berços (as famílias do mundo) e os caminhos da inclinação
  python3 cria.py perguntas                                  abre as perguntas da criação no caderno do turno (o jogador responde por código: "1a.2c.3e.4r")
  python3 cria.py nasce "1a.2c.3e[.4r]" nome=NOME            o personagem nasce pelas respostas (1: o povo · 2: o berço · 3: a inclinação · 4: a segunda, só do humano)
  python3 cria.py nasce povo=POVO berco=N inclinacao=CAMINHO [inclinacao2=CAMINHO] nome=NOME       o mesmo, por extenso
  python3 cria.py herdeiro PID                               nomeia o herdeiro (um parente, aprendiz ou jurado, vivo)
  python3 cria.py herda                                      morto o personagem: o jogo passa ao herdeiro (a casa, as peças que o matador não levou, a memória pela metade)
"""
import json, os, re, sys
import tabelas as T
import tabelas_mundo as M
import tabelas_regiao as R
import tabelas_povos as TP
import tabelas_talento as TT
import estado

LETRAS = 'abcdefghijklmnopqrstuvwxyz'
POVOS = list(TP.POVOS)


def tem(E): return bool((E.get('mundo') or {}).get('meta'))


def bercos(E):
    """os seis berços tirados do mundo (o acaso do mundo escolhe a família de cada molde): [{molde, chefe, lugar, casa, diz}]"""
    out = []; r = estado.sorte(E, 'cria|bercos')
    for molde, (papel, tipos, sobre, *_rest) in R.BERCOS.items():
        cands = [k for k, p in E['gente'].items() if p.get('papel') == papel and p['estado'] == 'vivo' and not p.get('rival') and not p.get('jogador')
                 and E['lugares'][p['lugar']].get('tipo') in tipos and (molde != 'nobre' or E['lugares'][p['lugar']].get('tipo') != 'capital')]
        if not cands: cands = [k for k, p in E['gente'].items() if p.get('papel') == papel and p['estado'] == 'vivo' and not p.get('rival') and not p.get('jogador')]
        if not cands: continue
        k = r.choice(sorted(cands)); p = E['gente'][k]; casa = p.get('casa'); nc = (E['mundo'].get('casas') or {}).get(casa, {}).get('nome', '')
        parentes = [E['gente'][x]['nome'] for x, t in (p.get('lacos') or {}).items() if E['gente'].get(x, {}).get('estado') == 'vivo']
        out.append(dict(molde=molde, chefe=k, lugar=p['lugar'], casa=casa, povo=estado.povo(p),
                        diz=f"{'criado no santuário por ' if molde == 'templo' else 'da casa ' + estado.de_nome(nc) + ', ' if nc else ''}{p['nome']} ({p.get('papel')}) {estado.em(E, p['lugar'])}"
                            + (f"; parentes vivos: {', '.join(parentes)}" if parentes and molde != 'templo' else '') + f" — {sobre}"))
    return out


def ofertas(E):
    L = ['OS POVOS (o povo muda os atributos, com a soma igual, e dá os traços; só o humano tem a segunda inclinação):']
    L += [f"  {LETRAS[i]}) {p}: {TP.POVOS[p]['frase']}" for i, p in enumerate(POVOS)]
    L += ['', 'OS BERÇOS (a família onde você nasce: o lugar, o ofício, os parentes, o que você leva):']
    for i, b in enumerate(bercos(E)):
        _, _, _, at, ma, _, pecas, prata, carga, _, mag = R.BERCOS[b['molde']]
        L.append(f"  {LETRAS[i]}) {b['diz']} · leva: {', '.join((q or t) + ' ' + T.CATS[c] for t, q, c, _, _ in pecas)}, {prata} de prata" + (f", {', '.join(f'{v} de {estado.nome_bem(k)}' for k, v in carga.items())}" if carga else ''))
    L += ['', 'A INCLINAÇÃO (o caminho em que o dado do talento rola duas vezes e vale o melhor):']
    L += [f"  {LETRAS[i]}) {c}: {TT.O_QUE[c]}" for i, c in enumerate(TT.CAMINHOS)]
    return '\n'.join(L)


def perguntas(E):
    """abre as perguntas da criação no caderno do turno (as que já estão abertas não se abrem de novo)"""
    import turno
    t = E['turno']
    if any(q.get('cria') for q in t['perguntas']): return 'as perguntas da criação já estão abertas.'
    bs = bercos(E); ops = []
    ops.append(('Que povo? (o povo muda os atributos e dá os traços)', [f"{LETRAS[i]}={p}" for i, p in enumerate(POVOS)], 'povo'))
    ops.append(('Que berço? (a família onde você nasce: `cria.py ofertas` conta cada uma)', [f"{LETRAS[i]}={b['diz'].split(' — ')[0]}" for i, b in enumerate(bs)], 'berco'))
    ops.append(('Que inclinação? (o caminho em que o dado do talento rola duas vezes)', [f"{LETRAS[i]}={c}" for i, c in enumerate(TT.CAMINHOS)], 'inclinacao'))
    ops.append(('Se humano, a segunda inclinação? (outro caminho; quem não é humano responde "r")', [f"{LETRAS[i]}={c}" for i, c in enumerate(TT.CAMINHOS)] + [f"{LETRAS[len(TT.CAMINHOS)]}=nenhuma"], 'inclinacao2'))
    for txt, opc, campo in ops:
        turno.pergunta(E, txt, opc); t['perguntas'][-1]['cria'] = campo
    return 'as perguntas da criação estão abertas (e o nome, o jogador diz por extenso).'


def _le_codigos(E, codigos):
    """'1a.2c.3e.4r' contra as perguntas da criação (pela ordem: povo, berço, inclinação, segunda): {povo, berco, inclinacao, inclinacao2}"""
    cods = dict((int(n), l.lower()) for n, l in re.findall(r'(\d+)\s*([a-zA-Z])', codigos))
    campos = ['povo', 'berco', 'inclinacao', 'inclinacao2']; out = {}
    for i, c in enumerate(campos, 1):
        if i not in cods: continue
        k = LETRAS.index(cods[i])
        if c == 'povo': out[c] = POVOS[k] if k < len(POVOS) else sys.exit(f'o povo "{cods[i]}" não existe (a a {LETRAS[len(POVOS) - 1]})')
        elif c == 'berco': out[c] = k
        else:
            if k == len(TT.CAMINHOS) and c == 'inclinacao2': continue
            out[c] = TT.CAMINHOS[k] if k < len(TT.CAMINHOS) else sys.exit(f'o caminho "{cods[i]}" não existe')
    return out


def nasce(E, povo, berco, inclinacao, nome, inclinacao2=None):
    """O PERSONAGEM NASCE (o dado do mundo, uma vez): no lugar da família, nível 5, os atributos do berço + o povo + o dado, o talento e o dom com a inclinação,
    as peças, a prata e a carga do berço, a mão de Iniciante (com o treino que a explica), os laços com os parentes (e a memória deles)."""
    import povos, talento, vila_teste, itens, gente
    if not tem(E): sys.exit('este mundo não tem região: o personagem do mundo novo nasce no mundo do gera.py')
    if any(p.get('jogador') and p['estado'] == 'vivo' for p in E['gente'].values()): sys.exit('o personagem já existe (e está vivo)')
    if povo not in TP.POVOS: sys.exit(f'povo desconhecido: "{povo}" (os que há: {", ".join(POVOS)})')
    if inclinacao not in TT.CAMINHOS: sys.exit(f'inclinação desconhecida: "{inclinacao}"')
    if inclinacao2 is not None and (povo != 'humano' or inclinacao2 not in TT.CAMINHOS or inclinacao2 == inclinacao): sys.exit('a segunda inclinação é só do humano, e é outro caminho')
    if not nome or not nome.strip(): sys.exit('o personagem tem nome: `nome=NOME`')
    bs = bercos(E)
    if not isinstance(berco, int) or not 0 <= berco < len(bs): sys.exit(f'o berço vai de 0 a {len(bs) - 1} (ou a letra, nas respostas)')
    b = bs[berco]; papel, _, sobre, at0, ma, grau, pecas, prata, carga, laco, mag = R.BERCOS[b['molde']]
    mortos = [k for k, p in E['gente'].items() if p.get('jogador')]          # o que morreu sem herdeiro sai da cadeira do jogador antes (a vida segue com um estranho)
    if mortos: estado.aplica(E, 'heranca', [['pessoa', k, 'jogador', 'poe', None] for k in mortos], texto='o personagem morto sai da cadeira do jogador')
    r = estado.sorte(E, 'cria|nasce'); at = dict(at0)
    for _ in range(2):                                      # o dado do mundo: dois pares de atributos trocam 5 pontos (a soma não muda)
        a, c = r.sample(T.ATRIBUTOS, 2); at[a] += 5; at[c] -= 5
    lugar = b['lugar']; chefe = b['chefe']; ch = E['gente'][chefe]
    reg = dict(nome=nome.strip(), nivel=R.NIVEL_PERSONAGEM, atributos=at, lugar=lugar, grau_oficio=grau, maestria=dict(ma), treino=vila_teste.treino_da_mao(ma),
               marca={'prep_receita': 0} if b['molde'] == 'forja' else {}, carga=dict(carga), moedas=0, jogador=True,
               sobre=sobre + (' (de criação: o sangue é de outro povo)' if povo != b['povo'] and b['molde'] != 'templo' else ''), casa=b['casa'] if b['molde'] != 'templo' else None,
               pais=[chefe] if laco == 'pai' else [])
    reg = povos.nasce(E, 'eu', reg, povo)
    if mag: reg['feiticos'] = list(mag['feiticos'])
    reg = talento.nasce(E, 'eu', reg, inclinacao, inclinacao2)
    if reg.get('casa') is None: reg.pop('casa')
    lacos = {chefe: laco}
    for k, t in (ch.get('lacos') or {}).items():               # a família do chefe é a sua: os filhos dele são seus irmãos; o cônjuge, também da casa
        if E['gente'].get(k, {}).get('estado') == 'vivo' and t in ('filho', 'cônjuge', 'irmão') and laco == 'pai': lacos[k] = 'irmão' if t == 'filho' else 'parente'
    reg['lacos'] = lacos
    paga = min(prata, E['lugares'][lugar]['estoque'].get('prata', 0))      # a prata do berço sai da casa (do lugar): nada novo cria prata
    ef = [['pessoa', 'nasce', 'eu', reg], ['estoque', lugar, 'prata', 'soma', -paga], ['pessoa', 'eu', 'moedas', 'soma', paga]]
    volta = {'pai': 'filho', 'mestre': 'aprendiz', 'irmão': 'irmão', 'parente': 'parente'}
    for k, t in lacos.items():
        ef.append(['pessoa', k, 'lacos.eu', 'poe', volta.get(t, 'parente')])
    s0 = E['itens']['seq']; miudo = TP.POVOS[povo]['corpo'] == 'miúdo'
    for i, (tipo, qual, cat, cobre, uso) in enumerate(pecas):
        nm = f"{(qual or tipo).capitalize()} de {nome}" if tipo != 'escudo' else f"Escudo de {nome}"
        kw = dict(familia=qual) if tipo == 'arma' else dict(material=qual, cobre=cobre, **({'talhe': 'miúdo'} if miudo else {})) if tipo == 'armadura' else {}
        it = itens.item(tipo, cat, nm, dono='eu', historia=[f"Dia {E['relogio']['dia']}: da casa {estado.de_nome(E['mundo']['casas'].get(b['casa'], {}).get('nome', 'da família'))}" if b['casa'] else f"Dia {E['relogio']['dia']}: do santuário"], **kw)
        ef.append(['item', 'nasce', it])
        if uso: ef.append(['item', f"i{s0 + i + 1:04d}", 'uso', 'poe', uso])
    estado.aplica(E, 'gera', ef, onde=lugar, quem=['eu'], texto=f"{nome} nasce para o jogo: {sobre} (do povo dos {TP.PLURAL[povo]})")
    mem = []
    for k, t in lacos.items(): mem += gente.lembra(E, k, 'eu', 'é do meu sangue' if t in ('pai', 'irmão', 'parente') else 'criei no santuário', 4 if t in ('pai', 'mestre') else 2)
    if mem: estado.aplica(E, 'gera', mem, onde=lugar, quem=['eu'], texto=f"a família de {nome}")
    E['turno']['perguntas'] = [q for q in E['turno']['perguntas'] if not q.get('cria')]
    P = estado.valida(E)
    if P: sys.exit('O PERSONAGEM NASCEU TORTO:\n  ' + '\n  '.join(P))
    p = E['gente']['eu']
    return (f"{nome} nasceu {estado.em(E, lugar)}: {p['idade']} anos, do povo dos {TP.PLURAL[povo]}, {sobre}.\n"
            f"Atributos: {', '.join(f'{k} {v}' for k, v in p['atributos'].items())} · PV {p['pv']} · {p['moedas']} de prata.\n"
            f"Família: {_familia_diz(E, lacos)}.\n"
            f"Inclinação: {inclinacao}" + (f" e {inclinacao2}" if inclinacao2 else '') + ". O talento e o dom foram rolados (ninguém sabe ainda o que tem: aparece fazendo).")


def _familia_diz(E, lacos):
    import gente
    return ', '.join(f"{E['gente'][k]['nome']} ({gente.laco_diz(t)})" for k, t in lacos.items())


def herdeiro(E, pid):
    eu = estado.eu(E) or sys.exit('não há personagem'); p = E['gente'][eu]
    if p['estado'] != 'vivo': sys.exit('o herdeiro se nomeia em vida')
    q = E['gente'].get(pid) or sys.exit(f'não há a pessoa "{pid}"')
    t = (p.get('lacos') or {}).get(pid)
    if t not in M.HERDA_LACOS: sys.exit(f"{q['nome']} não é parente, aprendiz nem jurado de {p['nome']} (os laços: {', '.join(f'{E['gente'][k]['nome']} ({v})' for k, v in (p.get('lacos') or {}).items() if k in E['gente'])})")
    estado.aplica(E, 'herdeiro', [['pessoa', eu, 'herdeiro', 'poe', pid]], onde=p['lugar'], quem=[eu, pid], texto=f"{p['nome']} nomeia {q['nome']} herdeiro")
    return f"{q['nome']} é o herdeiro de {p['nome']}."


def _matador(E, eu):
    """quem matou o personagem: o lado vencedor da última luta em que ele morreu (a pessoa com ficha, ou o bicho, ou o bando da estrada), ou None"""
    for l in reversed(E['turno'].get('lutas') or []):
        try: S = json.load(open(estado.arq_abre(l['arq']), encoding='utf-8'))
        except (OSError, ValueError): continue
        me = next((f for f in S['L'] if f.get('id') == eu), None)
        if not me or me['estado'] != 'morto': continue
        vivos = [f for f in S['L'] if f['lado'] != me['lado'] and f['estado'] == 'pe']
        if not vivos: return None
        f = max(vivos, key=lambda x: x.get('nivel', 0))
        return f.get('id') or f.get('bicho') or f.get('povo') or f['nome']
    return None


def herda(E):
    """o personagem morreu: o herdeiro assume (a casa; as peças do morto que o matador não levou; a memória dos outros pela metade); quem matou vira o nêmesis"""
    import gente, frentes
    eu = next((k for k, p in E['gente'].items() if p.get('jogador')), None) or sys.exit('não há personagem')
    p = E['gente'][eu]
    if p['estado'] == 'vivo': sys.exit(f"{p['nome']} está vivo: não há o que herdar")
    h = p.get('herdeiro')
    if not h or E['gente'].get(h, {}).get('estado') != 'vivo': sys.exit(f"{p['nome']} morreu sem herdeiro vivo: o jogo recomeça com um estranho no mesmo mundo (`cria.py ofertas`, `cria.py nasce`)")
    m = p.get('morte') or {}; onde = m.get('onde'); mat = _matador(E, eu); ef = []; L = []
    vestia = set(m.get('vestia') or [])
    if mat and vestia:                                       # o matador fica com o que o morto vestia
        for iid in vestia:
            it = E['itens']['itens'].get(iid)
            if not it or it.get('dono'): continue
            if mat in E['gente'] and E['gente'][mat]['estado'] == 'vivo': ef.append(['item', iid, 'dono', 'poe', mat])
            elif it.get('solto'): ef.append(['item', iid, 'solto', 'poe', None])        # o bicho, o bando: a peça fica guardada onde ele mora
    levou = vestia if mat else set()                         # sem matador (a fome, a maldição, a queda), nada foi levado
    fica = [i for i, it in E['itens']['itens'].items() if it.get('corpo') == eu and it.get('solto') and not it.get('dono') and i not in levou]
    ef += [['item', i, 'dono', 'poe', h] for i in fica]
    for k, q in E['gente'].items():                          # a memória que os outros têm do morto passa ao herdeiro, pela metade
        if k in (eu, h) or q.get('estado') != 'vivo': continue
        v, _ = gente.opiniao(E, k, eu)
        if abs(v) >= 2: ef += gente.lembra(E, k, h, f"é do sangue de {p['nome']}", v // 2)
    if p.get('casa') and E['gente'][h].get('casa') != p['casa']: ef.append(['pessoa', h, 'casa', 'poe', p['casa']])
    ef += [['pessoa', eu, 'herdeiro', 'poe', None], ['pessoa', eu, 'jogador', 'poe', None], ['pessoa', h, 'jogador', 'poe', True]]
    estado.aplica(E, 'heranca', ef, onde=E['gente'][h]['lugar'], quem=[h], texto=f"{E['gente'][h]['nome']} herda de {p['nome']}: a casa, {len(fica)} peças, e os amigos e os inimigos dele")
    if mat: frentes.nemesis(E, h, mat if mat in E['gente'] else f"esp:{mat}@{onde}", onde or E['gente'][h]['lugar']); L.append(f"Quem matou {p['nome']} vira o nêmesis da casa.")
    return f"O jogo segue com {E['gente'][h]['nome']} ({estado.em(E, E['gente'][h]['lugar'])})." + (' ' + ' '.join(L) if L else '')


# ---------- a MESA antes do personagem: a criação ----------
def mesa_criacao(E):
    W = E['mundo']; meta = W.get('meta') or {}; Ls = E['lugares']
    pov = [k for k, l in Ls.items() if l.get('tipo') in M.POVOADOS]
    L = [f"# MESA · a criação · {estado.quando(E)} · ano {meta.get('ano0')} {estado.de_nome((W.get('reinos') or {}).get('r_hoje', {}).get('nome', 'do reino'))}", '',
         f"**O mundo:** {meta.get('nome')}: {len(pov)} lugares de povo ({f'{sum(int(Ls[k].get(chr(112) + chr(111) + chr(112)) or 0) for k in pov):,}'.replace(',', '.')} pessoas em número), {len([g for g in E['gente'].values() if not g.get('rival')])} com nome, "
         + f"{len([g for g in E['gente'].values() if g.get('rival')])} aventureiros rivais, {len([1 for l in Ls.values() if l.get('tipo') == 'masmorra'])} masmorras, {meta.get('anos')} anos de história.",
         'O personagem ainda não nasceu. O jogador escolhe o povo, o berço e a inclinação (e diz o nome); o dado do mundo faz o resto, uma vez.', '', ofertas(E)]
    return L


def mesa(E): return []


if __name__ == '__main__':
    import signal; hasattr(signal, 'SIGPIPE') and signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    a = sys.argv[1:]; op = dict(x.split('=', 1) for x in a if '=' in x); pos = [x for x in a if '=' not in x]
    if not pos or pos[0] not in ('ofertas', 'perguntas', 'nasce', 'herdeiro', 'herda'): print(__doc__); sys.exit()
    E = estado.carrega()
    if pos[0] == 'ofertas': print(ofertas(E))
    elif pos[0] == 'perguntas': print(perguntas(E)); estado.grava(E)
    elif pos[0] == 'nasce':
        if len(pos) > 1: d = _le_codigos(E, pos[1])
        else: d = dict(povo=op.get('povo'), berco=int(op['berco']) if op.get('berco', '').isdigit() else None, inclinacao=op.get('inclinacao'), inclinacao2=op.get('inclinacao2'))
        out = nasce(E, d.get('povo') or 'humano', d.get('berco'), d.get('inclinacao'), op.get('nome', ''), d.get('inclinacao2'))
        estado.grava(E)
        import turno; turno.abre(E)
        print(out + '\nA MESA se refez: `turno.py abre`.')
    elif pos[0] == 'herdeiro':
        if len(pos) != 2: sys.exit('use: `cria.py herdeiro PID`')
        print(herdeiro(E, pos[1])); estado.grava(E)
    else: print(herda(E)); estado.grava(E)
