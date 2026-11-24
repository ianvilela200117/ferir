#!/usr/bin/env python3
"""criaturas.py — MOTOR 10, ETAPA DA MAGIA: AS CRIATURAS (capítulos 15 e 16; os números no tabelas_criaturas.py; o contrato: projeto/ETAPA_MAGIA.md).

  O POVO (goblin, orc, ogro, homem-lagarto, gigante; e os mortos que empunham: o esqueleto e o cavaleiro da cova) é GENTE: a ficha de gente, com arma, armadura e
    escudo de verdade, e o corpo do povo por cima (o tamanho, os traços, a coragem e a pele). Cada um tem um POSTO (o goblin de faca, o lanceiro, o arqueiro, o capataz).
    A peça do povo é GASTA E MALFEITA: na luta vale a categoria dela; morto o dono, é sucata (o despojo da espécie), nunca peça de vender.
  A CRIATURA DE CORPO (o corpo-seco, o carniçal, a múmia, o fogo-fátuo, a alma penada, o espectro, o golem de barro, a gárgula, o elemental do fogo, a harpia,
    o lobisomem, o senhor vampiro) é um bicho (bichos.py): o corpo é a arma e a armadura. Quem tem o traço "lança" sabe feitiços, e o corpo é o foco dele.
  OS CHEFES MÁGICOS (o xamã goblin, o senhor da guerra orc, o necromante, a bruxa do brejo, o senhor vampiro) vêm com os lacaios: lançam, mudam de FASE
    (a luta para e pergunta), dão o brado, erguem os mortos.
  O COVIL: a toca de um povo num ermo (lugar.covil). As cabeças SÃO a contagem da espécie no ermo (lugar.bichos.goblin), contada ao lado da fauna: a patrulha que
    o caçador encontra sai dela, e quem morre sai dela. O bando come da caça do ermo, rouba da vila vizinha (a comida e a prata vão para o estoque do ermo: o TESOURO da
    toca), cria devagar até o teto, definha com fome; caído o líder, outro sobe em alguns dias; a toca que ninguém incomoda ganha um chefe. Tudo por evento "covil".
    Quem fica com o campo NA TOCA (caca.py sair ERMO alvo=toca) leva o tesouro inteiro.

Uso em código (o que as outras frentes chamam):
  criatura(especie, nome=None, posto=None, **mais)    o lutador pronto para o luta.nova (gente, povo ou corpo)
  bando(especie, sorte=None, n=None, primeiro=1, **mais)   os que andam juntos (a patrulha do povo: o bando_postos da espécie; o corpo: como o bicho)
  chefe(qual, lacaios=True, **mais)                   o chefe e os lacaios, prontos para a luta (o primeiro é o chefe)
  toca(E, lid, n=None)                                quem está na toca (o chefe e a guarda, o líder, e o resto pelos postos)
  despojo(especie, sorte=None)                        ({bem: quantos}, None): a sucata do povo; o corpo pela tabela (o bicho de veneno dá peçonha)
  ameaca(especie, n=None, arma=None, armadura=None)   a frase que se lê antes da luta (o bichos.ameaca chama daqui para o povo)
  poe_covil(E, lid, especie, ...) · virada(E) · so_mestre(E) · voce(E)
Uso de linha de comando (só olha, a não ser o `covil poe`):
  python3 criaturas.py lista                          as criaturas, do grau F ao S, e os chefes
  python3 criaturas.py ver ESPECIE|CHEFE              a ficha de luta, o despojo e a ameaça
  python3 criaturas.py ameaca ESPECIE [N] [arma=CATEGORIA] [armadura=CATEGORIA]
  python3 criaturas.py tracos                         as frases dos traços novos
  python3 criaturas.py mede ESPECIE|CHEFE NIVEL CATEGORIA [N] [lutas=200] [homens=1] [arma=espada] [armadura=malha]   a régua, em lutas de ensaio
  python3 criaturas.py covil [ERMO]                   SÓ O MESTRE: o covil de um ermo (as cabeças, o líder, o chefe, a fome, o tesouro)
  python3 criaturas.py covil poe ERMO ESPECIE [cabecas=N] [tesouro=N] [chefe=sim]  SÓ O MESTRE: funda um covil num ermo que já existe (o tesouro sai do nada: evento "mestre")
"""
import math, random, sys
import tabelas as T
import tabelas_bichos as TB
import tabelas_criaturas as TC
from itens import item, cat_i

TOSCA_DUR = 0.5             # a peça do povo é gasta: tem tanto da durabilidade de uma nova (malfeita: na mão de quem a tira de um morto, é sucata)


# ---------- quem é quem ----------
def especie(k):
    if k not in TC.ESPECIES: sys.exit(f'criatura desconhecida: "{k}" (as que há: {", ".join(TC.ESPECIES)})')
    return TC.ESPECIES[k]


def e_povo(k): return bool((TC.ESPECIES.get(k) or {}).get('povo'))
def e_chefe(k): return k in TC.CHEFES
def _fem(e): return e.get('artigo') == 'a'
def _s(n, um, muitos): return um if n == 1 else muitos
def _nome(e, n=1): return f"{e['artigo']} {e['nome']}" if n == 1 else f"{n} {e['plural']}"
def _e(L): L = list(L); return ''.join(L) if len(L) <= 1 else ', '.join(L[:-1]) + ' e ' + L[-1]


def plural(nome):
    """o plural de um nome de criatura ("goblin lanceiro" → "goblins lanceiros", "orc da guarda" → "orcs da guarda", "carniçal" → "carniçais")"""
    for e in list(TC.ESPECIES.values()) + list(TB.ESPECIES.values()):
        if nome == e['nome']: return e.get('plural') or (e['nome'][:-2] + 'ões' if e['nome'].endswith('ão') else e['nome'] + 's')
    out = []; parou = False
    for w in nome.split(' '):
        if parou or w in ('da', 'do', 'de', 'das', 'dos'): parou = True; out.append(w); continue
        out.append('-'.join((p[:-1] + 'is' if p.endswith('l') else p[:-2] + 'ões' if p.endswith('ão') else p if p.endswith('s') else p + 's') for p in w.split('-')))
    return ' '.join(out)


def lacaios_diz(C):
    """os lacaios de um chefe, em palavras: 2 goblins da guarda, o capataz goblin, 4 goblins..."""
    L = []
    for esp, posto, q, ch in C['lacaios']:
        e = TB.ESPECIES.get(esp) or TC.ESPECIES[esp]; nm = ch.get('nome') or (e['postos'][posto]['nome'] if posto else e['nome'])
        L.append((nm if nm.startswith(('o ', 'a ')) else f"{e['artigo']} {nm}") if q == 1 else f"{q} {plural(nm.removeprefix('o ').removeprefix('a '))}")
    return _e(L)


def chave(x):
    """a criatura pelo nome da tabela ou pelo nome que vai à mesa ("alma-penada" ou "alma penada"); o chefe pelo nome dele"""
    for k, d in TC.ESPECIES.items():
        if x in (k, d['nome']): return k
    for k, d in TC.CHEFES.items():
        if x in (k, d.get('nome')): return k
    return x


def _tosca(it):
    d = max(2, int(it['dur'][1] * TOSCA_DUR)); it['dur'] = [d, d]; it['tosca'] = True
    return it


def _nivel_de(e, c, mais):
    """a criatura de outra categoria (o esqueleto Raro do necromante) sobe de nível como o homem do degrau sobe"""
    if c == e['cat'] or 'nivel' in mais: return mais.pop('nivel', e['nivel'])
    return max(1, round(e['nivel'] * TC.REF.get(c, TC.REF[5]) / TC.REF.get(e['cat'], 10)))


def criatura(esp, nome=None, posto=None, **mais):
    """O LUTADOR PRONTO de uma criatura: o povo (gente que veste, pelo posto) ou o corpo (o bicho da tabela, com os feitiços e as fases dele).
    mais: o que muda (cat, nivel, maestria, atributos, lider, guarda, linha, moral, arma, armadura, escudo...). O chefe sozinho: o_chefe(qual)."""
    if esp in TC.CHEFES and esp not in TC.ESPECIES: return o_chefe(esp, nome=nome, **mais)
    e = especie(esp)
    if not e.get('povo'):
        import bichos
        return bichos.bicho(esp, nome=nome, **mais)
    P = TC.POVOS[e['povo']]; ps = e['postos']; posto = posto or next(iter(ps))
    if posto not in ps: sys.exit(f"{e['nome']}: posto desconhecido: \"{posto}\" (os que há: {', '.join(ps)})")
    po = ps[posto]; pm = dict(po['mais']); c = cat_i(mais.pop('cat', e['cat']))
    nivel = mais.pop('nivel') if 'nivel' in mais else pm.pop('nivel', None) if 'nivel' in pm else _nivel_de(e, c, {})
    m = mais.pop('maestria') if 'maestria' in mais else pm.pop('maestria', e['instinto'] if c == e['cat'] else min(6, T.maestria_tipica(nivel)))
    at = {k: P['base'][k] + int(nivel * P['pts'][k]) for k in T.ATRIBUTOS}; at.update(mais.pop('atributos', None) or {})
    p = dict(nome=nome or (po['nome'] if po['nome'].startswith(('o ', 'a ')) else f"{e['artigo']} {po['nome']}"), nivel=nivel, atributos=at, maestria=m, equip={},
             povo=dict(especie=esp, povo=e['povo'], tamanho=P['tamanho'], tracos=list(P['tracos']), coragem=P['coragem'], couro=P['couro'], cat=c))
    def faz(x): return None if not x else _tosca(item('arma', min(7, c + x[1]), familia=x[0]))
    arm = []
    a = mais.pop('armadura', po['armadura'])
    if isinstance(a, dict): arm.append(a)
    elif a:
        arm.append(_tosca(item('armadura', c, material=a[0])))
        if a[1]: arm.append(_tosca(item('armadura', c, material=a[0], cobre=['cabeça'])))
    arma = mais.pop('arma', None); esc = mais.pop('escudo', None)
    p['equip'] = dict(arma=arma if isinstance(arma, dict) else faz(arma or po['arma']), arma2=faz(po['arma2']),
                      escudo=esc if isinstance(esc, dict) else (_tosca(item('escudo', c)) if (po['escudo'] if esc is None else esc) else None), armaduras=arm)
    if po.get('linha'): p['linha'] = po['linha']
    if posto == e.get('lider'): p['lider'] = True
    p['posto'] = posto
    p.update(mais)
    return p


def bando(esp, sorte=None, n=None, primeiro=1, lider=False, toca=False, **mais):
    """os que andam juntos, com nome cada um. O povo: os postos pelo bando_postos da espécie (o primeiro posto leva o que sobra); com lider=True, o primeiro é o líder
    (a patrulha anda sem ele: o líder fica na toca). O corpo: como o bicho (bichos.bando)."""
    e = especie(esp)
    if not e.get('povo'):
        import bichos
        return bichos.bando(esp, sorte, n=n, primeiro=primeiro, **mais)
    lo, hi = e['bando']
    if n is None: n = lo if lo == hi else (sorte or random.SystemRandom()).randint(lo, hi)
    if n <= 0: return []
    postos = []
    if lider and e.get('lider'): postos.append(e['lider'])
    resto = n - len(postos); conta = {}; bp = e['toca_postos'] if toca else e['bando_postos']
    for ps, fr in bp[1:]: conta[ps] = int(resto * fr) if resto >= 3 else 0
    if resto >= 3 and not any(conta.values()) and len(bp) > 1: conta[bp[1][0]] = 1
    conta = {bp[0][0]: resto - sum(conta.values()), **conta}
    for ps, q in conta.items(): postos += [ps] * q
    if n == 1 and primeiro == 1: return [criatura(esp, posto=postos[0], **mais)]
    out = []; num = {}
    for ps in postos:
        po = e['postos'][ps]
        if ps == e.get('lider'): out.append(criatura(esp, posto=ps, **mais)); continue
        num[ps] = num.get(ps, 0) + 1
        out.append(criatura(esp, nome=f"{po['nome']} {num[ps] + primeiro - 1}", posto=ps, **mais))
    return out


def o_chefe(qual, nome=None, **mais):
    """o chefe sozinho (sem os lacaios), pronto para a luta"""
    C = TC.CHEFES[qual]
    if C.get('especie'):
        import bichos
        e = TC.ESPECIES[C['especie']]
        p = bichos.bicho(C['especie'], nome=nome or f"{e['artigo']} {e['nome']}", lider=True, **mais); p['chefe'] = True
        if C.get('linha') and 'linha' not in mais: p['linha'] = C['linha']          # o chefe que lança fica atrás dos lacaios: o bicho que lança só lança enquanto não alcança
        return p
    ext = {k: mais.pop(k) for k in list(mais) if k in ('arma', 'armadura', 'escudo')}
    if C.get('povo'):
        c = C['cat']
        arma = ext.get('arma') or _tosca(item('arma', c, familia=C['arma'][0]))
        p = criatura(C['povo'], nome=nome or C['nome'], posto=C['posto'], cat=c, nivel=C['nivel'], maestria=C['maestria'], atributos=dict(C.get('atributos') or {}), arma=arma,
                     escudo=ext.get('escudo', _tosca(item('escudo', c)) if C.get('escudo') else False), **({'armadura': ext['armadura']} if 'armadura' in ext else {'armadura': C['armadura']} if 'armadura' in C else {}))
    else:
        from pessoas import padrao, veste
        p = padrao(nome or C['nome'], C['nivel'], molde=C['molde'], maestria=dict(C['maestria']) if isinstance(C['maestria'], dict) else C['maestria'], atributos=dict(C.get('atributos') or {}))
        mat = C.get('armadura')
        veste(p, arma=ext.get('arma') or (C['arma'][0], C['cat']), armadura=ext.get('armadura') or ((mat[0], C['cat']) if mat else None), elmo=None if mat and mat[1] else False,
              escudo=ext.get('escudo') or (C['cat'] if C.get('escudo') else None))
    eq = p['equip']
    if C.get('foco'): eq['foco'] = item('foco', C['foco'][1], forma=C['foco'][0])
    if C.get('amuleto') is not None: eq['amuleto'] = item('amuleto', C['amuleto'])
    if C.get('encanto') and eq.get('arma'):
        eq['arma'] = dict(eq['arma'], encantos=[dict(feitico=C['encanto']['feitico'], grau=C['encanto']['grau'], feito_por=None, dia=0, gasto=None)])
    for k in ('tradicao', 'linha', 'moral'):
        if C.get(k): p[k] = C[k]
    if C.get('feiticos'): p['feiticos'] = list(C['feiticos'])
    if C.get('fases'): p['fases'] = [dict(x) for x in C['fases']]
    if C.get('maldicao'): p['maldicao'] = dict(C['maldicao'])
    p.update(lider=True, chefe=True); p.update(mais)
    return p


def chefe(qual, lacaios=True, **mais):
    """O CHEFE E OS LACAIOS, prontos para a luta: o primeiro da lista é o chefe; os primeiros `guarda` lacaios põem o corpo na frente dele"""
    if qual not in TC.CHEFES: sys.exit(f'chefe desconhecido: "{qual}" (os que há: {", ".join(TC.CHEFES)})')
    C = TC.CHEFES[qual]; b = o_chefe(qual, **mais); L = [b]
    if not lacaios: return L
    k = 0; num = {}
    for esp, posto, q, ch in C['lacaios']:
        ch = dict(ch); base = ch.pop('nome', None)
        if esp in TB.ESPECIES:
            import bichos
            base = base or TB.ESPECIES[esp]['nome']
            for i in range(q): num[base] = num.get(base, 0) + 1; L.append(bichos.bicho(esp, nome=f"{base} {num[base]}", **ch))
        else:
            e = especie(esp); base = base or (e['postos'][posto]['nome'] if posto else e['nome']).removeprefix('o ').removeprefix('a ')
            for i in range(q):
                num[base] = num.get(base, 0) + 1; nm = f"{base} {num[base]}" if not (posto and posto == e.get('lider')) else e['postos'][posto]['nome']
                L.append(criatura(esp, nome=nm, posto=posto, **ch) if e.get('povo') else criatura(esp, nome=nm, **ch))
        for x in L[1 + k:]:
            if k < C.get('guarda', 0): x['guarda'] = b['nome']; x['linha'] = 'trás'
            k += 1
    return L


# ---------- o despojo ----------
def despojo(esp, sorte=None):
    """o que a criatura morta rende: ({bem: quantidade}, None). A luta estraga: de cada bem sai de metade ao inteiro da tabela (como no bicho).
    O povo rende a sucata das peças (a peça é gasta e malfeita); o morto que anda, o osso; o bicho de veneno, a peçonha (está na tabela da espécie)."""
    e = especie(esp); r = sorte or random.SystemRandom(); bens = {}
    for bem, q in e['despojo'].items():
        lo = max(1, math.ceil(q * TB.DESPOJO_MIN)); bens[bem] = lo if lo >= q else r.randint(lo, q)
    return bens, None


# ---------- a ameaça: o que se lê antes da luta ----------
def _veste_diz(e):
    """o que o povo veste e empunha, posto por posto (a peça é da categoria do bando)"""
    C = T.CATS[e['cat']]; L = []
    for k, po in e['postos'].items():
        arma = po['arma'][0] + (f" e {po['arma2'][0]}" if po['arma2'] else ''); a = po['armadura']
        L.append(f"{po['nome'].removeprefix('o ').removeprefix('a ')}: {arma}" + (f", {a[0]}" + (' e elmo' if a[1] else '') if a else '') + (', escudo' if po['escudo'] else ''))
    return f"veste peças {T.CATS[e['cat']] if e['cat'] else 'Comuns'} gastas e malfeitas (" + '; '.join(L) + ')'


def ameaca(esp, n=None, arma=None, armadura=None):
    """a frase que se lê ANTES da luta. O corpo: a do bicho (bichos.ameaca, com as frases dos traços novos). O povo: o grau, o tamanho, o que veste, os traços, quantos são."""
    import bichos
    e = especie(esp)
    if not e.get('povo'): return bichos.ameaca(esp, n=n, arma=arma, armadura=armadura)
    c = e['cat']; C = T.CATS[c]; lo, hi = e['bando']; fem = _fem(e); P = TC.POVOS[e['povo']]
    quantos = f'são {n}' if n and n > 1 else 'está sozinho' if n == 1 else f'anda em bando de {lo} a {hi}' if lo > 1 else f'anda sozinho ou em {hi}' if hi > 1 else 'anda sozinho'
    L = [f"{e['nome'].upper()} · grau {e['grau']} ({C}): {TB.GRAU_DIZ[e['grau']]} · {bichos._tamanho_diz(e['tamanho'], fem)} · {quantos}.",
         f"É POVO: luta como gente, e {_veste_diz(e)}" + (f"; onde a peça não cobre, a pele vale como {TB.COUROS[P['couro']]} {C}" if P['couro'] else '') + '.']
    if e['tracos']: L.append('Traços: ' + '. '.join(f'{t.capitalize()}: {TC.frase(t)}' for t in e['tracos']) + '.')
    if (n or hi) > 1:
        g2 = TB.grau_do_bando(e['grau'], n or hi)
        L.append(f"EM BANDO, o grau {e['grau']} é o de um só: {f'{n} juntos valem' if n and n > 1 else 'o bando vale'} grau {g2} para quem está sozinho ({TB.GRAU_DIZ[g2]}). "
                 f"Até {T.CERCO} batem em você de perto na mesma rodada, e cada um que já bateu tira {T.FLANCO} da sua Defesa para o próximo.")
    L.append(f"Sabe-se: {e['sabe']}.")
    if 'sem vida' in e['tracos']: L.append('Não foge e não se rende: luta até se desfazer.')
    else: L.append(f"Abalado, foge ou se rende ({bichos._menos(e['coragem'])} na coragem)" + (f"; caído o {e['postos'][e['lider']]['nome'].removeprefix('o ')}, o bando testa a coragem" if e.get('lider') else '') + '.')
    if arma is None and armadura is None:
        L.append(f"A conta: a arma e a armadura deles são {C}: o que vale é a sua peça contra a deles, como entre gente.")
    else:
        if arma is not None: a = cat_i(arma); L.append(f"A sua arma ({T.CATS[a]}) na armadura deles ({C}): o golpe {bichos._vezes(a - c)}.")
        if armadura is not None: a = cat_i(armadura); L.append(f"A arma deles ({C}) na sua armadura ({T.CATS[a]}): {bichos._vezes(c - a)}.")
    return ' '.join(L)


def ameaca_chefe(qual):
    """o que se sabe de um chefe (o Mestre lê quando a cena o põe à frente: do chefe ninguém sabe de graça)"""
    C = TC.CHEFES[qual]; b = o_chefe(qual); nm = b['nome']
    fe = b.get('feiticos') or (TC.ESPECIES.get(C.get('especie')) or {}).get('feiticos') or []
    lac = lacaios_diz(C)
    fases = b.get('fases') or []
    return (f"{nm.upper()} · CHEFE: não foge à toa. " + (f"Lança: {', '.join(T.nome_feitico(k) for k in fe)}. " if fe else '') + f"Vem com: {lac}. Sabe-se: {C['sabe']}."
            + (' Ferido, muda: ' + ' · '.join(f"abaixo de {x['abaixo']:.0%} do PV, {x.get('diz', 'muda')}" for x in fases) + '.' if fases else ''))


def ameaca_toca(E, lid, arma=None, armadura=None):
    """a toca vista de fora: quantos se contam (em palavras), se o líder está, se há chefe (só se vê o sinal), e a ameaça do povo"""
    cv = E['lugares'][lid].get('covil') or {}; esp = cv.get('especie'); n = int((E['lugares'][lid].get('bichos') or {}).get(esp, 0))
    e = especie(esp); fala = next(t for lim, t in TC.TOCA_CONTA if n <= lim)
    sinal = ' Há ossos pintados na boca da toca e um cheiro de fumo doce: alguém lá dentro mexe com coisa que não é de comer.' if cv.get('chefe') else ''
    return (f"A TOCA ({cv.get('nome', 'a toca')}): de fora se vê {fala} ({e['plural']})." + sinal + ' ' + ameaca(esp, n=max(2, n), arma=arma, armadura=armadura)
            + f" Quem fica com o campo na toca leva o que ela guarda.")


# ---------- O COVIL ----------
def covis(E):
    """[(lugar, registro)] dos covis do mundo"""
    return [(lid, l['covil']) for lid, l in E['lugares'].items() if isinstance(l.get('covil'), dict) and l['covil'].get('especie') in TC.ESPECIES]


def cabecas(E, lid):
    cv = E['lugares'][lid].get('covil') or {}
    return int((E['lugares'][lid].get('bichos') or {}).get(cv.get('especie'), 0)) if cv else 0


def toca(E, lid, n=None):
    """QUEM ESTÁ NA TOCA: o chefe e a guarda dele (se o covil tem chefe), o líder (se está de pé), e o resto pelos postos da espécie. Todos saem da contagem, menos o chefe."""
    cv = E['lugares'][lid]['covil']; esp = cv['especie']; e = especie(esp); n = cabecas(E, lid) if n is None else n
    L = []
    if cv.get('chefe') and cv['chefe'] in TC.CHEFES:
        C = TC.CHEFES[cv['chefe']]; g = min(C.get('guarda', 0), n); L += chefe(cv['chefe'], lacaios=False)
        for i in range(g):
            post = next((p for e2, p, _, _ in C['lacaios'] if e2 == esp), None); ch = next((c for e2, _, _, c in C['lacaios'] if e2 == esp), {})
            L.append(criatura(esp, nome=f"guarda d{'a' if C['nome'].startswith('a ') else 'o'} {C['nome'][2:]} {i + 1}", posto=post, guarda=L[0]['nome'], linha='trás', **ch))
        n -= g
    if n > 0: L += bando(esp, n=n, lider=bool(cv.get('lider', True)), toca=True)
    return L


def no_cenario(p):
    """a pessoa de uma criatura em forma curta para o arquivo do cenário da luta ({"bicho": ESPECIE, ...}): o luta.cenario a refaz pelo bichos.bicho"""
    if p.get('chefe') and p.get('povo') or (p.get('chefe') and not p.get('bicho')):
        q = next((k for k, C in TC.CHEFES.items() if C.get('nome') == p['nome']), None)
        if q: return dict(bicho=q, nome=p['nome'])
    if p.get('povo'):
        esp = p['povo']['especie']; e = TC.ESPECIES[esp]
        d = dict(bicho=esp, nome=p['nome'], posto=p.get('posto'))
        for k in ('lider', 'guarda', 'linha'):
            if k in p: d[k] = p[k]
        if p['povo'].get('cat', e['cat']) != e['cat']: d['cat'] = p['povo']['cat']
        return d
    return p


def poe_covil(E, lid, esp, cabecas_=None, tesouro=None, chefe_=False, tipo='mestre', como=''):
    """O Mestre (ou o gerador) funda um covil num ermo que já existe: o registro, as cabeças na contagem do ermo e o tesouro no estoque do ermo (a prata nasce: só
    em evento "gera" ou "mestre"). Os efeitos são aplicados num evento só."""
    l = E['lugares'].get(lid) or sys.exit(f'não há o lugar "{lid}"')
    if esp not in TC.COVIS: sys.exit(f'só há covil de: {", ".join(TC.COVIS)}')
    if l.get('pop'): sys.exit(f"{l['nome']} tem povo: covil é coisa de ermo")
    if isinstance(l.get('covil'), dict): sys.exit(f"{l['nome']} já tem covil")
    V = TC.COVIS[esp]; n = V['cabecas'] if cabecas_ is None else int(cabecas_); t = V['tesouro'] if tesouro is None else int(tesouro)
    reg = dict(especie=esp, nome=V['nome'], teto=V['teto'], lider=True, chefe=V['chefe'] if chefe_ else None, fome=0, ult_roubo=E['relogio']['dia'], sem_lider=0, cheio=0, fora=0, desde=E['relogio']['dia'])
    ef = [['lugar', lid, 'covil', 'poe', reg], ['lugar', lid, f'bichos.{esp}', 'poe', n], ['lugar', lid, f'teto.{esp}', 'poe', V['teto']]]      # o teto: o rastro fica mais difícil com o bando miúdo
    if t: ef.append(['estoque', lid, 'prata', 'soma', t])
    import estado
    estado.aplica(E, tipo, ef, onde=lid, texto=f"{V['nome']} {estado.em(E, lid)}: {n} {especie(esp)['plural']}" + (', com o chefe' if chefe_ else '') + (f': {como}' if como else ''))
    return f"{V['nome']} {estado.em(E, lid)}: {n} {especie(esp)['plural']}, {t} de prata no tesouro" + (f", e {TC.CHEFES[V['chefe']]['nome']}" if chefe_ else '') + '.'


def _vila_de(E, lid):
    """a vila vizinha de onde o bando rouba (a que tem povo e estoque), ou None"""
    for v in E['lugares'][lid].get('vizinhos') or []:
        if v in E['lugares'] and E['lugares'][v].get('pop') and isinstance(E['lugares'][v].get('estoque'), dict): return v
    return None


def virada(E):
    """O DIA VIROU, NA TOCA (evento "covil", o mundo sozinho): cada covil come (do que juntou, depois da caça contada do ermo), a fome anda, rouba da vila vizinha a cada
    tantos dias (a comida e, às vezes, a prata vão para o estoque do ermo), cria devagar até o teto, definha com fome; caído o líder, outro sobe; a toca cheia por muito
    tempo ganha um chefe; a toca vazia espera um bando de fora. O acaso é o do mundo (estado.sorte)."""
    import estado
    for lid, cv in covis(E):
        esp = cv['especie']; V = TC.COVIS.get(esp)
        if not V: continue
        l = E['lugares'][lid]; n = cabecas(E, lid); dia = E['relogio']['dia']; r = estado.sorte(E, f'covil|{lid}|{dia}'); novo = dict(cv); ef = []; txt = []
        if n <= 0:
            if not cv.get('fora'): novo['fora'] = V['vem_de_fora']; novo['chefe'] = None
            else:
                novo['fora'] = cv['fora'] - 1
                if novo['fora'] <= 0:
                    novo.update(fora=0, lider=True, chefe=None, fome=0, sem_lider=0, cheio=0); ef.append(['lugar', lid, f'bichos.{esp}', 'soma', V['novo_bando']])
                    txt.append(f"chega de fora um bando de {V['novo_bando']} {especie(esp)['plural']}")
            if novo != cv: ef.insert(0, ['lugar', lid, 'covil', 'poe', novo])
            if ef: estado.aplica(E, 'covil', ef, onde=lid, texto=f"{cv.get('nome', 'o covil')}: " + ('; '.join(txt) or 'vazio'))
            continue
        # 1 COME: do que juntou (a comida do estoque do ermo), depois da caça contada do ermo
        precisa = n * V['come']; est = l.get('estoque') or {}; tem = est.get('comida', 0); do_est = min(tem, math.floor(precisa)); precisa -= do_est
        if do_est > 0: ef.append(['estoque', lid, 'comida', 'soma', -do_est])
        B = {k: int(q) for k, q in (l.get('bichos') or {}).items() if k in V['presa'] and isinstance(q, (int, float)) and q >= 1}
        teto = l.get('teto') or {}; fart = sum(B.values()) / max(1, sum(teto.get(k, 0) for k in V['presa'] if k in teto)); comeu = {}
        while precisa > 1e-9 and B:
            if r.random() >= fart: break
            k = sorted(B)[0] if len(B) == 1 else r.choices(sorted(B), weights=[B[x] for x in sorted(B)])[0]; carne = V['presa'][k]
            if precisa < carne and r.random() > precisa / carne: precisa = 0; break
            B[k] -= 1; comeu[k] = comeu.get(k, 0) + 1; precisa = max(0, precisa - carne)
            if B[k] <= 0: del B[k]
        ef += [['lugar', lid, f'bichos.{k}', 'soma', -q] for k, q in comeu.items()]
        if comeu: txt.append('o bando caça ' + ', '.join(f"{q} {TB.ESPECIES[k]['nome'] if q == 1 else TB.ESPECIES[k]['nome'] + 's'}" for k, q in comeu.items() if k in TB.ESPECIES))
        fome = max(0, cv.get('fome', 0) - 1) if precisa <= 1e-9 else min(10, cv.get('fome', 0) + 1); novo['fome'] = fome
        # 2 ROUBA da vila vizinha, a cada tantos dias: a comida (e às vezes a prata) vai para o estoque do ermo
        v = _vila_de(E, lid)
        if v and dia - cv.get('ult_roubo', -99) >= V['rouba_cada']:
            novo['ult_roubo'] = dia
            if r.random() < n / V['rouba_chance'] + 0.1 * fome:
                q = min(int(n * V['rouba_comida']), int(E['lugares'][v]['estoque'].get('comida', 0)))
                if q > 0:
                    ef += [['estoque', v, 'comida', 'soma', -q], ['estoque', lid, 'comida', 'soma', q]]; pr = 0
                    if r.random() < V['rouba_prata']:
                        pr = min(r.randint(1, V['prata_dado']) + n // 4, int(E['lugares'][v]['estoque'].get('prata', 0)))
                        if pr > 0: ef += [['estoque', v, 'prata', 'soma', -pr], ['estoque', lid, 'prata', 'soma', pr]]
                    txt.append(f"o bando rouba de noite {estado.de(E, v)}: {q} de comida" + (f" e {pr} de prata" if pr else ''))
        # 3 CRIA (bem comido) ou DEFINHA (com fome)
        nasce = 0
        if fome < 4 and n < cv.get('teto', V['teto']):
            x = n * V['cria'] * (1 - n / cv.get('teto', V['teto'])); nasce = int(x) + (1 if r.random() < x - int(x) else 0)
        if fome >= V['definha']: nasce = -1
        if nasce: ef.append(['lugar', lid, f'bichos.{esp}', 'soma', nasce]); txt.append('nasce um no bando' if nasce > 0 else 'um do bando morre de fome')
        # 4 O LÍDER e O CHEFE
        if not cv.get('lider', True):
            novo['sem_lider'] = cv.get('sem_lider', 0) + 1
            if novo['sem_lider'] >= V['lider_dias']: novo.update(lider=True, sem_lider=0); txt.append(f"sobe outro {especie(esp)['postos'][especie(esp)['lider']]['nome'].removeprefix('o ')}")
        novo['cheio'] = cv.get('cheio', 0) + 1 if n >= V['chefe_desde'] else 0
        if not cv.get('chefe') and V.get('chefe') and novo['cheio'] >= V['chefe_dias']: novo['chefe'] = V['chefe']; txt.append(f"a toca ganha {TC.CHEFES[V['chefe']]['nome']}")
        if novo != cv: ef.insert(0, ['lugar', lid, 'covil', 'poe', novo])
        if ef: estado.aplica(E, 'covil', ef, onde=lid, texto=f"{cv.get('nome', 'o covil')} {estado.em(E, lid)}: " + ('; '.join(txt) or 'o dia passa'))


def depois_da_luta(E, lid, S, campo, quem):
    """os efeitos que a luta NA TOCA deixa no covil (o caca.acerta os põe no evento dele): o líder ou o chefe que caiu; e, se a casa ficou com o campo, o tesouro
    (o estoque do ermo) que ela leva, repartido entre quem lutou até o fim. Devolve (efeitos, {pessoa: {bem: quanto}}, frases)."""
    cv = E['lugares'][lid].get('covil')
    if not isinstance(cv, dict): return [], {}, []
    e = especie(cv['especie']); novo = dict(cv); ef = []; partes = {}; L = []
    caiu = {f['nome'] for f in S['L'] if f['lado'] == 'B' and f['estado'] in ('morto', 'caido', 'rendido')}
    lider = e['postos'][e['lider']]['nome'] if e.get('lider') else None
    if lider and (lider in caiu or f"{e['artigo']} {lider}" in caiu): novo.update(lider=False, sem_lider=0); L.append(f"O {lider.removeprefix('o ')} caiu: o bando fica sem quem mande por uns dias.")
    if cv.get('chefe') and TC.CHEFES[cv['chefe']]['nome'] in caiu: novo['chefe'] = None; novo['cheio'] = 0; L.append(f"{TC.CHEFES[cv['chefe']]['nome'].capitalize()} caiu: a toca perde o chefe.")
    if campo and quem:
        est = {b: q for b, q in (E['lugares'][lid].get('estoque') or {}).items() if isinstance(q, (int, float)) and q >= 1 and (b == 'prata' or b == 'comida')}
        for b, q in est.items():
            q = int(q); cada, resto = divmod(q, len(quem))
            for i, c in enumerate(quem):
                k = cada + (1 if i < resto else 0)
                if k: partes.setdefault(c, {})[b] = partes.get(c, {}).get(b, 0) + k
            ef.append(['estoque', lid, b, 'soma', -q])
        for c, d in partes.items():
            for b, q in d.items(): ef.append(['pessoa', c, 'moedas' if b == 'prata' else f'carga.{b}', 'soma', q])
        if est: L.append('O TESOURO DA TOCA: ' + ', '.join(f"{int(q)} de {b}" for b, q in est.items()) + (' (repartido entre quem lutou até o fim)' if len(quem) > 1 else '') + '.')
    if novo != cv: ef.insert(0, ['lugar', lid, 'covil', 'poe', novo])
    return ef, partes, L


# ---------- a mesa ----------
def so_mestre(E):
    """as linhas dos covis para o SÓ O MESTRE: os covis nos ermos vizinhos do personagem (as cabeças, o líder, o chefe, a fome, o tesouro)"""
    import estado
    pid = estado.eu(E)
    if not pid: return []
    aqui = E['gente'][pid].get('lugar'); viz = set([aqui] + list((E['lugares'].get(aqui) or {}).get('vizinhos') or []))
    L = []
    for lid, cv in covis(E):
        if lid not in viz: continue
        n = cabecas(E, lid); est = E['lugares'][lid].get('estoque') or {}; e = especie(cv['especie'])
        L.append(f"{cv.get('nome', 'o covil')} {estado.em(E, lid)}: {n} {e['plural']} (teto {cv.get('teto')})" + (f", {e['postos'][e['lider']]['nome']} de pé" if cv.get('lider', True) and e.get('lider') else ', sem líder' if e.get('lider') else '')
                 + (f", com {TC.CHEFES[cv['chefe']]['nome']}" if cv.get('chefe') else '') + f" · fome {cv.get('fome', 0)} · tesouro: {int(est.get('prata', 0))} de prata, {int(est.get('comida', 0))} de comida"
                 + (f" · vazio: chega um bando de fora em {cv['fora']} dias" if n <= 0 and cv.get('fora') else '') + f' (`caca.py sair {lid} alvo=toca`)')
    return L


# ---------- olhar ----------
def _ordem(k):
    e = TC.ESPECIES[k]; return (e['cat'], TB.GRAUS.index(e['grau']), e['nivel'], k)


def _lista():
    L = [f"{'criatura':<20}{'grau':<6}{'categoria':<11}{'tamanho':<9}{'bando':<8}{'é':<8}{'traços':<46}onde vive"]
    for k in sorted(TC.ESPECIES, key=_ordem):
        e = TC.ESPECIES[k]; b = '%d' % e['bando'][0] if e['bando'][0] == e['bando'][1] else '%d a %d' % e['bando']
        L.append(f"{k:<20}{e['grau']:<6}{T.CATS[e['cat']]:<11}{e['tamanho']:<9}{b:<8}{'povo' if e.get('povo') else 'corpo':<8}{(', '.join(e['tracos']) or 'nenhum'):<46}{', '.join(e['habitat'])}"
                 + (' · CHEFE' if e['chefe'] else '') + (f" · lança: {', '.join(e['feiticos'])}" if e.get('feiticos') else ''))
    L += ['', 'OS CHEFES MÁGICOS (com os lacaios: `criaturas.py ver CHEFE`)']
    for k, C in TC.CHEFES.items():
        L.append(f"  {k:<18} {C.get('nome') or 'o ' + TC.ESPECIES[C['especie']]['nome']} (grau {C.get('grau') or TC.ESPECIES[C['especie']]['grau']}) · com: " + lacaios_diz(C))
    return '\n'.join(L)


def _ver(x):
    from pessoas import ficha, linha
    if x in TC.CHEFES and (x not in TC.ESPECIES or TC.CHEFES[x].get('especie')):
        L = chefe(x); return '\n'.join([linha(ficha(L[0])), '', ameaca_chefe(x), '', 'OS LACAIOS:'] + [linha(ficha(p)).splitlines()[0] for p in L[1:]])
    e = especie(x)
    p = criatura(x) if not e.get('povo') else criatura(x, posto=e['bando_postos'][0][0])
    return '\n'.join([linha(ficha(p)), '  despojo (inteiro): ' + (' · '.join(f'{q} de {b}' for b, q in e['despojo'].items()) or 'nada') + (' (a sucata das peças)' if e.get('povo') else ''),
                      '  onde vive: ' + ', '.join(e['habitat']), '', ameaca(x)])


def mede(x, nivel, cat, n=None, lutas=200, familia='espada', material='malha', quantos=1, **kw):
    """a régua: lutas de ENSAIO (dado de mentira, com semente; nada é guardado) de n criaturas (ou o chefe com os lacaios) contra `quantos` homens daquele nível e conjunto.
    Devolve {vence, perde, caiu (o primeiro homem caiu ou morreu), morreu (algum homem morreu), rodadas}."""
    import luta
    from pessoas import padrao, veste
    c = cat_i(cat); F = T.FAMILIAS[familia]; tiro = bool(F.get('distancia')); guarda = luta.D; luta.semente(1); rs = []; m = dict(vence=0, perde=0, caiu=0, morreu=0)
    homem = lambda k: veste(padrao('o homem' if quantos == 1 else f'homem {k + 1}', nivel, molde='arqueiro' if tiro else 'guerreiro'), arma=(familia, c), armadura=(material, c),
                            escudo=c if F['maos'] == 1 else None, arma2=('adaga', c) if tiro else None)
    try:
        for i in range(lutas):
            B = chefe(x) if x in TC.CHEFES and x not in TC.ESPECIES else bando(x, random.Random(i), n=n)
            S = luta.nova([homem(k) for k in range(quantos)], B, quieto=True, **kw); luta.corre(S); A = [f for f in S['L'] if f['lado'] == 'A']
            m['vence'] += S['fim'] == 'A'; m['perde'] += S['fim'] == 'B'; rs.append(S['r'])
            m['caiu'] += A[0]['estado'] in ('morto', 'caido'); m['morreu'] += any(f['estado'] == 'morto' for f in A)
    finally: luta.D = guarda
    rs.sort(); m = {k: round(100 * v / lutas) for k, v in m.items()}; m['rodadas'] = rs[len(rs) // 2]
    return m


def main(a=None):
    a = sys.argv[1:] if a is None else list(a)
    op = dict(x.split('=', 1) for x in a if '=' in x); pos = [x for x in a if '=' not in x]
    if len(pos) > 1: pos[1] = chave(pos[1])
    num = lambda x, que: int(x) if x.isdigit() and int(x) >= 1 else sys.exit(f'{que}: um número de 1 para cima (veio "{x}")')
    if pos == ['lista']: print(_lista())
    elif pos == ['tracos']: print('\n'.join(['OS TRAÇOS NOVOS (a luta os roda: tabelas.TRACOS_NOVOS; os números no tabelas_magia.py)'] + [f'  {k:<10} {v}' for k, v in TC.TRACOS.items()]))
    elif pos[:1] == ['ver'] and len(pos) == 2: print(_ver(pos[1]))
    elif pos[:1] == ['ameaca'] and len(pos) in (2, 3):
        print(ameaca_chefe(pos[1]) if pos[1] in TC.CHEFES and pos[1] not in TC.ESPECIES else ameaca(pos[1], n=num(pos[2], 'quantos são') if len(pos) > 2 else None, arma=op.get('arma'), armadura=op.get('armadura')))
    elif pos[:1] == ['mede'] and len(pos) in (4, 5):
        q = num(op.get('homens', '1'), 'quantos homens'); n = num(pos[4], 'quantas criaturas') if len(pos) > 4 else None
        m = mede(pos[1], num(pos[2], 'o nível'), pos[3], n=n, lutas=num(op.get('lutas', '200'), 'quantas lutas'), familia=op.get('arma', 'espada'), material=op.get('armadura', 'malha'), quantos=q)
        print(f"ENSAIO (dado de mentira, nada é guardado): {'um homem' if q == 1 else f'{q} homens'} de nível {pos[2]}, conjunto {T.CATS[cat_i(pos[3])]}, contra {pos[1]}"
              f"{f' ({n})' if n else ''}: vence {m['vence']}% · perde {m['perde']}% · o primeiro homem cai ou morre em {m['caiu']}% · algum homem morre em {m['morreu']}% · mediana de {m['rodadas']} rodadas")
    elif pos[:1] == ['covil']:
        import estado
        E = estado.carrega()
        if len(pos) >= 4 and pos[1] == 'poe':
            print(poe_covil(E, pos[2], pos[3], cabecas_=op.get('cabecas'), tesouro=op.get('tesouro'), chefe_=op.get('chefe') == 'sim')); estado.grava(E)
        else:
            L = [x for x in so_mestre(E)] if len(pos) == 1 else []
            for lid, cv in covis(E):
                if len(pos) == 2 and lid != pos[1]: continue
                if len(pos) == 2 or not L: L.append(f"{lid}: {cv} · cabeças {cabecas(E, lid)} · estoque {E['lugares'][lid].get('estoque')}")
            print('\n'.join(L) or 'não há covil.')
    else: print(__doc__)


if __name__ == '__main__':
    import signal; hasattr(signal, 'SIGPIPE') and signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    main()
