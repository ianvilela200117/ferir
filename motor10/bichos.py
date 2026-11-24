#!/usr/bin/env python3
"""bichos.py — MOTOR 10: OS BICHOS. Um bicho é uma ficha de luta como qualquer outra.

O corpo é a ARMA (garra, presa, chifre, cauda, casco, ferrão) e a ARMADURA (pelo, escama, carapaça), com CATEGORIA, e a regra de
ouro vale igual: conta a diferença entre a arma de quem bate e a armadura de quem apanha. O corpo NÃO É PEÇA: não está no Livro de
Itens, não tem dono, não quebra, não ocupa sintonia. O TAMANHO mexe no PV, no alcance, no cerco, no corredor e na Defesa. Os TRAÇOS
são uma lista fechada que a luta roda. O bicho comum FOGE ferido; o encurralado e o chefe, não. O DESPOJO sai da tabela.
As regras estão no projeto/regras_bichos.md; os números, no tabelas_bichos.py; as provas, no provas.py (bloco OS BICHOS).

Uso em código (a caça usa isto):
  tabelas_bichos.ESPECIES[especie]         nome, cat, grau, tamanho, bando, despojo, nucleo, habitat (e o resto da ficha)
  bicho(especie, nome=None, **mais)        a pessoa pronta para o luta.nova (e para a lista "B" do cenário do ato.py luta)
  bando(especie, sorte, n=None)            a lista: quantos andam juntos sai da sorte (o acaso do mundo: estado.sorte(E, chave)); a espécie de alfa traz o líder
  despojo(especie, sorte, cat=None)        ({bem: quantidade}, o registro do núcleo ou None); com `cat`, na categoria de quem morreu (etapa 4b)
  ameaca(especie, n=None, arma=None, armadura=None)     a frase que o caçador lê ANTES da luta
  resumo(especie, n=None)                  a espécie numa linha curta · mesa(E): as linhas dos bichos para a MESA.md (sem contagem e sem chefes)
Uso de linha de comando (só olha: não rola dado de jogo nem mexe em save):
  python3 bichos.py lista                  as espécies, do grau F ao S
  python3 bichos.py ver ESPECIE            a ficha de luta, o despojo e a ameaça
  python3 bichos.py ameaca ESPECIE [N] [arma=CATEGORIA] [armadura=CATEGORIA]
  python3 bichos.py tracos                 os traços que a luta roda, e os tamanhos
  python3 bichos.py mede ESPECIE NIVEL CATEGORIA [N] [lutas=200] [arma=espada] [armadura=malha] [homens=1] [inicio=perto] [surpresa=bicho|homem]
                                           a régua: N bichos contra um homem daquele nível e conjunto, em lutas de ensaio
No cenário da luta (luta.py nova, ato.py luta nova), um bicho é {"nome": "lobo 1", "nivel": 0, "bicho": "lobo"} (a espécie
inteira sai da tabela), ou a pessoa que o bicho() devolve, tal qual.
AS CRIATURAS (etapa da magia: criaturas.py, tabelas_criaturas.py) passam pelas mesmas portas: especie(), bicho(), bando(), despojo(), ameaca(), resumo() e mesa()
aceitam as espécies do tabelas_criaturas.ESPECIES (a de corpo é um bicho; a de POVO é gente que veste, e o bicho() a entrega pronta pelo criaturas.criatura) e os
chefes do tabelas_criaturas.CHEFES (o chefe sozinho). No cenário: {"bicho": "goblin", "nome": "goblin 1", "posto": "lanceiro"} ou {"bicho": "xamã goblin"}.
As frases dos traços novos moram no tabelas_criaturas.TRACOS (nunca no tabelas_bichos.TRACOS).
OS DRAGÕES (etapa 4b: tabelas_dragoes.ESPECIES, frente D) são bichos: especie(), bicho(), ameaca() e despojo() os aceitam ({"bicho": "dragão-da-serra-jovem"}).
O DESPOJO PELA CATEGORIA DE QUEM MORREU (etapa 4b): despojo(esp, sorte, cat) põe a matéria na categoria do morto (até a Rara); o núcleo só do Épico para cima.
"""
import math, random, sys
import tabelas as T
import tabelas_bichos as TB
import tabelas_mundo as M
from itens import item, cat_i

CORPO = ('cat', 'armas', 'couro', 'tamanho', 'tracos', 'coragem')        # o que é do corpo; o resto do que se passa em `mais` é da pessoa


def _tc():
    """a página das criaturas (etapa da magia), ou None se ainda não existe"""
    try: import tabelas_criaturas as TC
    except ModuleNotFoundError as x:
        if x.name != 'tabelas_criaturas': raise
        return None
    return TC


def _td():
    """a página dos dragões (etapa 4b), ou None se ainda não existe"""
    try: import tabelas_dragoes as TD
    except ModuleNotFoundError as x:
        if x.name != 'tabelas_dragoes': raise
        return None
    return TD


def especie(e):
    """o registro da espécie: um bicho (tabelas_bichos.ESPECIES), uma criatura (tabelas_criaturas.ESPECIES) ou um dragão (tabelas_dragoes.ESPECIES, etapa 4b)"""
    if e in TB.ESPECIES: return TB.ESPECIES[e]
    TC = _tc()
    if TC and e in TC.ESPECIES: return TC.ESPECIES[e]
    TD = _td()
    if TD and e in TD.ESPECIES: return TD.ESPECIES[e]
    sys.exit(f'espécie desconhecida: "{e}" (as que existem: {", ".join(list(TB.ESPECIES) + (list(TC.ESPECIES) if TC else []) + (list(TD.ESPECIES) if TD else []))})')


def _povo_ou_chefe(esp):
    """a espécie de POVO (gente que veste) ou o chefe das criaturas: quem a monta é o criaturas.py"""
    TC = _tc()
    return bool(TC and esp not in TB.ESPECIES and ((esp in TC.ESPECIES and TC.ESPECIES[esp].get('povo')) or (esp in TC.CHEFES and esp not in TC.ESPECIES)))


def frase(t):
    """a frase de um traço: o da etapa 2 (tabelas_bichos.TRACOS) ou o novo (tabelas_criaturas.TRACOS)"""
    if t in TB.TRACOS: return TB.TRACOS[t]
    TC = _tc()
    return TC.TRACOS.get(t, t) if TC else t


def bicho(esp, nome=None, **mais):
    """a pessoa pronta para o luta.nova. `mais` muda o corpo (cat, armas, couro, tamanho, tracos, coragem) ou a pessoa
    (nivel, atributos, instinto, lider, moral, linha, pv, feridas...): serve ao Mestre para o bicho fora do comum, e às provas."""
    if _povo_ou_chefe(esp):
        import criaturas
        return criaturas.criatura(esp, nome=nome, **mais)
    e = especie(esp)
    corpo = dict(especie=esp, cat=e['cat'], armas=list(e['armas']), couro=e['couro'], tamanho=e['tamanho'], tracos=list(e['tracos']), coragem=e['coragem'])
    for k in CORPO:
        if k in mais: corpo[k] = mais.pop(k)
    corpo['cat'] = cat_i(corpo['cat'])
    at = dict(e['atributos']); at.update(mais.pop('atributos', None) or {})
    p = dict(nome=nome or f"{e['artigo']} {e['nome']}", nivel=mais.pop('nivel', e['nivel']), atributos=at, maestria=mais.pop('instinto', e['instinto']), equip={}, moral=e['moral'], bicho=corpo)
    if e.get('feiticos'): p['feiticos'] = list(e['feiticos'])           # a criatura que lança (o traço "lança"): o corpo é o foco, o instinto é a mão
    if e.get('fases'): p['fases'] = [dict(x) for x in e['fases']]
    if e.get('maldicao'): p['maldicao'] = dict(e['maldicao'])            # o molde da maldição que o traço "amaldiçoa" põe
    if e.get('chefe') and esp not in TB.ESPECIES: p['lider'] = True
    p.update(mais)
    return p


def bando(esp, sorte=None, n=None, primeiro=1, **mais):
    """os bichos que andam juntos, com nome cada um. Quantos: da sorte (um random.Random; o do mundo é o estado.sorte), ou n.
    Na espécie que segue um alfa, o primeiro é o líder: caído ele, o bando testa a coragem.
    primeiro: de que número os nomes partem (um segundo bando da mesma espécie na mesma luta parte de onde o outro parou, e não traz outro alfa)."""
    if _povo_ou_chefe(esp):
        import criaturas
        return criaturas.bando(esp, sorte, n=n, primeiro=primeiro, **mais)
    e = especie(esp); lo, hi = e['bando']
    if n is None: n = lo if lo == hi else (sorte or random.SystemRandom()).randint(lo, hi)
    if n == 1 and primeiro == 1: return [bicho(esp, **mais)]
    out = [bicho(esp, nome=f"{e['nome']} {i + primeiro}", **mais) for i in range(n)]
    if e['alfa'] and primeiro == 1: out[0]['nome'] = f"{e['artigo']} {e['nome']} alfa"; out[0]['lider'] = True
    return out


def na_cat(bem, cat_esp, cat):
    """O DESPOJO PELA CATEGORIA DE QUEM MORREU (etapa 4b, o defeito achado pelo projeto A, consertado em toda parte): a matéria que está na categoria da espécie
    (até a Rara) vai para a categoria de quem morreu (até a Rara); a que a tabela põe noutra categoria anda junto, a mesma distância (de 0 à Rara). O bem sem categoria
    (a comida, o pano) fica como está. Sem `cat`, ou na categoria da espécie, é a tabela de hoje."""
    n, c = M.le_materia(bem)
    if c is None or cat is None or cat == cat_esp: return bem
    alvo = cat if c == min(cat_esp, M.MATERIA_ATE) else c + (cat - cat_esp)
    return M.materia(n, max(0, min(M.MATERIA_ATE, alvo)))


def despojo(esp, sorte=None, cat=None):
    """o que o bicho morto rende: ({bem: quantidade}, o núcleo). A luta estraga: de cada bem sai de metade ao inteiro da tabela.
    O núcleo (só o chefe dá, e só do Épico para cima: tabelas_bichos.NUCLEO_DESDE) é o registro pronto para o ['item', 'nasce', registro]: falta pôr o dono ou o lugar.
    `cat`: a categoria de quem morreu (etapa 4b; na luta, o cat_corpo do lutador): a matéria e o núcleo saem nela. Sem ela, a da espécie (a tabela de hoje)."""
    TC = _tc()
    if esp not in TB.ESPECIES and TC and esp in TC.ESPECIES:
        import criaturas
        return criaturas.despojo(esp, sorte, cat=cat)
    e = especie(esp); r = sorte or random.SystemRandom(); bens = {}; c = e['cat'] if cat is None else cat_i(cat)
    for bem, q in e['despojo'].items():
        lo = max(1, math.ceil(q * TB.DESPOJO_MIN)); k = na_cat(bem, e['cat'], c); bens[k] = bens.get(k, 0) + (lo if lo >= q else r.randint(lo, q))
    nucleo = item('nucleo', c, f"núcleo de {e['nome']}", de=esp) if e['nucleo'] and c >= TB.NUCLEO_DESDE else None
    return bens, nucleo


# ---------- a ameaça: o que o caçador lê antes da luta ----------
VEZES = {0: 'passa inteiro', 1: 'vale o triplo', 2: 'vale nove vezes', -1: 'vale um terço', -2: 'vale um nono'}
NO_COURO = dict(pelo='no pelo', escama='na escama', carapaça='na carapaça')


def _vezes(d): return VEZES.get(d, 'vale vinte e sete vezes ou mais' if d > 0 else 'quase não passa')
def _menos(x): return f'{x:+d}'.replace('-', '−')


def _tamanho_diz(t, fem):
    tam = TB.TAMANHOS[t]; m = TB.TAMANHOS['médio']; L = []; nele = 'nela' if fem else 'nele'
    if tam['defesa'] > 0: L.append(f"difícil de acertar: {_menos(tam['defesa'])} na Defesa")
    if tam['defesa'] < 0: L.append(f"fácil de acertar: {_menos(tam['defesa'])} na Defesa")
    if tam['alcance'] > 1: L.append(f"alcança {tam['alcance']} casas e bate primeiro em quem chega com arma mais curta")
    if tam['cerco'] != m['cerco']: L.append(f"{tam['cerco'][0]} batem {nele} de perto na mesma rodada")
    if tam['ocupa'] < 1: L.append('cabem dois numa vaga de corredor')
    if tam['ocupa'] > 1: L.append(f"toma {tam['ocupa']} vagas de um corredor; em lugar mais estreito, luta apertado")
    return (t[:-1] + 'a' if fem and t.endswith('o') else t) + (f" ({'; '.join(L)})" if L else '')


def ameaca(esp, n=None, arma=None, armadura=None):
    """a frase que o caçador lê ANTES da luta: o grau, o tamanho, o corpo, o que se sabe, se foge. Com n, quantos são;
    com a categoria da arma e da armadura de quem lê, a conta da regra de ouro já feita."""
    TD = _td(); dr = (TD.ESPECIES.get(esp) or {}).get('dragao') if TD else None
    if isinstance(dr, dict):                    # o dragão (etapa 4b): a frase dele é a do dragoes.ameaca (a fase, a fuga pelo ar, o coração)
        import dragoes
        return dragoes.ameaca(dr['tipo'], dr['idade'], arma=arma, armadura=armadura)
    if _povo_ou_chefe(esp):
        import criaturas
        return criaturas.ameaca_chefe(esp) if esp not in (_tc().ESPECIES) else criaturas.ameaca(esp, n=n, arma=arma, armadura=armadura)
    e = especie(esp); c = e['cat']; C = T.CATS[c]; lo, hi = e['bando']; fem = e['artigo'] == 'a'; dele = 'dela' if fem else 'dele'; so = 'sozinha' if fem else 'sozinho'; tam = TB.TAMANHOS[e['tamanho']]
    quantos = f'são {n}' if n and n > 1 else f'está {so}' if n == 1 else f'anda {so}' if hi == 1 else f'anda em bando de {lo} a {hi}' if lo > 1 else f'anda {so} ou em {hi}'
    if e['alfa'] and (n is None or n > 1): quantos += ', atrás de um alfa'
    L = [f"{e['nome'].upper()} · grau {e['grau']} ({C}): {TB.GRAU_DIZ[e['grau']]} · {_tamanho_diz(e['tamanho'], fem)} · {quantos}."]
    armas = e.get('armas_diz') or (e['armas'][0] if len(e['armas']) == 1 else ', '.join(e['armas'][:-1]) + ' e ' + e['armas'][-1])      # a criatura pode dizer o corpo com outro nome (o punho do golem)
    from itens import FEM
    L.append(f"O corpo: {armas} de categoria {C}; {e['couro']} {(FEM if e['couro'].endswith('a') else T.CATS)[c]}, que vale como {TB.COUROS[e['couro']]}.")       # a categoria concorda com o couro: pelo Comum, escama Épica, carapaça Rara
    if e['tracos']: L.append('Traços: ' + '. '.join(f'{t.capitalize()}: {frase(t)}' for t in e['tracos']) + '.')       # os novos (etapa da magia) moram no tabelas_criaturas.TRACOS
    if e.get('feiticos'): L.append('Lança: ' + ', '.join(T.nome_feitico(k) for k in e['feiticos']) + '.')
    if tam['ocupa'] < 1 and any(t in TB.PEDE_TAMANHO for t in e['tracos']):       # ninguém derruba nem agarra quem é maior que ele: o traço do bicho pequeno não pega gente
        L.append(f"Por ser pequen{'a' if fem else 'o'}, não derruba nem agarra gente: só quem é do tamanho {dele}.")
    if (n or hi) > 1:                                       # o bando: o grau fala de um só, e o cerco e o flanco são os de toda luta (tabelas.py)
        vaga = int(1 / tam['ocupa']); chegam = 'só um chega' if vaga <= 1 else f'só {vaga} chegam'
        if n and n > 1: g2 = TB.grau_do_bando(e['grau'], n); vale = f"{n} junt{'a' if fem else 'o'}s valem grau {g2} para quem está sozinho ({TB.GRAU_DIZ[g2]})"
        else: ga, gb = TB.grau_do_bando(e['grau'], max(lo, 2)), TB.grau_do_bando(e['grau'], hi); vale = f"o bando vale grau {ga}" + (f' a {gb}' if gb != ga else '') + f" para quem está sozinho ({TB.GRAU_DIZ[gb]})"
        L.append(f"EM BANDO, o grau {e['grau']} é o de {'uma' if fem else 'um'} só: {vale}. Até {T.CERCO} batem em você de perto na mesma rodada, e cada um que já bateu tira {T.FLANCO} da sua Defesa "
                 f"para o próximo (até {_menos(-T.FLANCO * T.FLANCO_MAX)}); num corredor de um, {chegam} de cada vez.")
    L.append(f"Sabe-se: {e['sabe']}.")
    if e['chefe']: L.append(f"É chefe: não foge, e {'morta' if fem else 'morto'} dá um núcleo {C}.")
    elif 'sem vida' in e['tracos']: L.append('Não tem vida: não foge, luta até se desfazer.')
    else: L.append(f"Ferid{'a' if fem else 'o'}, testa a coragem ({_menos(e['coragem'])}) e pode fugir; encurralad{'a' if fem else 'o'}, luta até o fim.")
    if arma is None and armadura is None:
        if c == 0: L.append(f"A conta: é Comum. Qualquer arma passa inteira {NO_COURO[e['couro']]} {dele}; o golpe {dele} passa inteiro em armadura Comum, vale um terço na Incomum, e o triplo em parte do corpo sem armadura.")
        else: L.append(f"A conta: arma abaixo de {C} {_vezes(-1)} {NO_COURO[e['couro']]} {dele} (duas abaixo, {_vezes(-2).replace('vale ', '')}); em armadura abaixo de {C}, o golpe {dele} {_vezes(1)}.")
    else:
        if arma is not None: a = cat_i(arma); L.append(f"A sua arma ({T.CATS[a]}) {NO_COURO[e['couro']]} {dele} ({C}): o golpe {_vezes(a - c)}.")
        if armadura is not None: a = cat_i(armadura); L.append(f"O golpe {dele} ({C}) na sua armadura ({T.CATS[a]}): {_vezes(c - a)}.")
    return ' '.join(L)


def _ordem(esp): e = especie(esp); return (e['cat'], TB.GRAUS.index(e['grau']), e['nivel'], esp)


def resumo(esp, n=None):
    """a espécie numa linha curta (para a MESA.md e para listas): o grau, a categoria, o tamanho, quantos andam juntos e os traços"""
    e = especie(esp); lo, hi = e['bando']; fem = e['artigo'] == 'a'; t = e['tamanho']
    quantos = f'{n}' if n else ('sozinha' if fem else 'sozinho') if hi == 1 else f'bando de {lo} a {hi}' if lo > 1 else f'de 1 a {hi}'
    return f"{e['nome']} (grau {e['grau']}, {T.CATS[e['cat']]}, {t[:-1] + 'a' if fem and t.endswith('o') else t}, {quantos}" + (', povo que veste peças' if e.get('povo') else '') + (': ' + ', '.join(e['tracos']) if e['tracos'] else '') + ')'


def mesa(E):
    """as linhas dos bichos para a MESA.md (que tem teto de tamanho): cada espécie contada no lugar do personagem ou num vizinho aparece UMA vez, com o resumo dela
    e os lugares onde há. Sem a contagem (é do Mestre) e sem os CHEFES (onde há um núcleo não se sabe de graça: acha-se no rastro).
    A frase inteira de cada espécie é a ameaca(): o caçador a lê quando o bicho aparece."""
    import estado
    pid = estado.eu(E)
    if not pid: return []
    aqui = E['gente'][pid]['lugar']; onde = {}
    for lid in [aqui] + [v for v in (E['lugares'][aqui].get('vizinhos') or []) if v in E['lugares']]:
        l = E['lugares'][lid]; conta = l.get('bichos') if isinstance(l.get('bichos'), dict) else {}
        for esp, q in conta.items():
            e = estado.especie(esp)                         # o bicho e a criatura (etapa da magia) contados no ermo
            if e and not e['chefe'] and isinstance(q, (int, float)) and not isinstance(q, bool) and q > 0: onde.setdefault(esp, []).append(l.get('nome', lid))
    if not onde: return []
    varios = len({n for L in onde.values() for n in L}) > 1
    return ['## Os bichos daqui (o que todo mundo sabe; a frase inteira: `bichos.py ameaca ESPECIE`)',
            '- ' + ' · '.join(resumo(esp) + (f" [{', '.join(onde[esp])}]" if varios else '') for esp in sorted(onde, key=_ordem))]


# ---------- olhar ----------
def _lista():
    L = [f"{'espécie':<12}{'grau':<6}{'categoria':<11}{'tamanho':<9}{'bando':<8}{'traços':<34}onde vive"]
    for k, e in sorted(TB.ESPECIES.items(), key=lambda x: _ordem(x[0])):        # as criaturas (etapa da magia) têm a lista delas: criaturas.py lista
        L.append(f"{k:<12}{e['grau']:<6}{T.CATS[e['cat']]:<11}{e['tamanho']:<9}{('%d' % e['bando'][0] if e['bando'][0] == e['bando'][1] else '%d a %d' % e['bando']):<8}{(', '.join(e['tracos']) or '—'):<34}{', '.join(e['habitat'])}"
                 + (' · CHEFE (dá núcleo)' if e['chefe'] else ''))
    return '\n'.join(L)


def _ver(esp):
    from pessoas import ficha, linha
    e = especie(esp)
    return '\n'.join([linha(ficha(bicho(esp))), '  despojo (o bicho inteiro): ' + ' · '.join(f'{q} de {b}' for b, q in e['despojo'].items()) + (f" · e um núcleo {T.CATS[e['cat']]}" if e['nucleo'] else ''),
                      '  onde vive: ' + ', '.join(e['habitat']), '', ameaca(esp)])


def _tracos():
    L = ['OS TRAÇOS (a lista é fechada: só entra o que a luta roda)'] + [f'  {k:<10} {v}' for k, v in TB.TRACOS.items()]
    TC = _tc()
    if TC: L += ['', 'OS TRAÇOS NOVOS (etapa da magia: tabelas.TRACOS_NOVOS)'] + [f'  {k:<10} {v}' for k, v in TC.TRACOS.items()]
    L += ['', 'OS TAMANHOS'] + [f"  {k:<8} PV × {t['pv']:g} · alcança {t['alcance']} casa(s) · cerco {t['cerco'][0]} de perto e {t['cerco'][1]} de haste · toma {t['ocupa']:g} de um corredor · Defesa {_menos(t['defesa'])}" for k, t in TB.TAMANHOS.items()]
    L += ['', 'O CORPO: A ARMA'] + [f"  {k:<8} {a['dado']} ({a['golpe']}), {a['folego']} de fôlego por golpe" for k, a in TB.ARMAS_CORPO.items()]
    L += ['', 'O CORPO: A ARMADURA'] + [f'  {k:<9} vale como {v}' for k, v in TB.COUROS.items()]
    return '\n'.join(L)


def _inicio(x):
    """o começo da luta para a régua: longe, perto ou colado"""
    if x not in T.INICIO: sys.exit(f'início desconhecido: "{x}" (use: {", ".join(T.INICIO)})')
    return x


def mede(esp, nivel, cat, n=None, lutas=200, familia='espada', material='malha', quantos=1, **kw):
    """a régua: lutas de ENSAIO (dado de mentira, com semente; nada é guardado) de n bichos contra um homem daquele nível (ou `quantos`
    homens iguais), com a arma (espada, se não se disser outra), a armadura (malha) e o escudo (se a arma é de uma mão) da categoria.
    O arqueiro e o besteiro levam uma adaga de reserva. Devolve um dicionário: rodadas (a mediana) e, em % das lutas: vence · perde ·
    carcaca (venceu e ficou bicho morto ou caído no campo) · fugiu (venceu só porque todos fugiram) · ferido (o primeiro homem saiu
    com ferida nova, caído ou morto) · caiu (o primeiro homem caiu ou morreu)."""
    import luta
    from pessoas import padrao, veste
    if familia not in T.FAMILIAS or familia == 'punho': sys.exit(f'arma desconhecida: "{familia}" (use: {", ".join(f for f in T.FAMILIAS if f != "punho")})')
    if material not in T.MATERIAIS: sys.exit(f'armadura desconhecida: "{material}" (use: {", ".join(T.MATERIAIS)})')
    c = cat_i(cat); F = T.FAMILIAS[familia]; tiro = bool(F.get('distancia')); guarda = luta.D; luta.semente(1); rs = []; m = dict(vence=0, perde=0, carcaca=0, fugiu=0, ferido=0, caiu=0)
    homem = lambda k: veste(padrao('o caçador' if quantos == 1 else f'caçador {k + 1}', nivel, molde='arqueiro' if tiro else 'guerreiro'), arma=(familia, c), armadura=(material, c),
                            escudo=c if F['maos'] == 1 else None, arma2=('adaga', c) if tiro else None)
    try:
        for i in range(lutas):
            S = luta.nova([homem(k) for k in range(quantos)], bando(esp, random.Random(i), n=n), quieto=True, **kw); luta.corre(S); h = S['L'][0]; bs = [f for f in S['L'] if f['lado'] == 'B']
            m['vence'] += S['fim'] == 'A'; m['perde'] += S['fim'] == 'B'; rs.append(S['r'])
            m['carcaca'] += S['fim'] == 'A' and any(f['estado'] in ('morto', 'caido') for f in bs); m['fugiu'] += S['fim'] == 'A' and all(f['estado'] == 'fugiu' for f in bs)
            m['caiu'] += h['estado'] in ('morto', 'caido'); m['ferido'] += h['estado'] in ('morto', 'caido') or len(h['feridas']) > h['feridas_antes']
    finally: luta.D = guarda
    rs.sort(); m = {k: round(100 * v / lutas) for k, v in m.items()}; m['rodadas'] = rs[len(rs) // 2]
    return m


def _chave(x):
    """a espécie pelo nome da tabela ou pelo nome que vai à mesa ("aranha" ou "aranha-de-toca"; das criaturas também)"""
    TC = _tc(); todas = dict(TB.ESPECIES, **(TC.ESPECIES if TC else {}))
    return next((k for k, d in todas.items() if x in (k, d['nome'])), x)


if __name__ == '__main__':
    a = sys.argv[1:]; op = dict(x.split('=', 1) for x in a if '=' in x); pos = [x for x in a if '=' not in x]
    if len(pos) > 1: pos[1] = _chave(pos[1])
    num = lambda x, que: int(x) if x.isdigit() and int(x) >= 1 else sys.exit(f'{que}: um número de 1 para cima (veio "{x}")')
    if pos == ['lista']: print(_lista())
    elif pos == ['tracos']: print(_tracos())
    elif pos[:1] == ['ver'] and len(pos) == 2: print(_ver(pos[1]))
    elif pos[:1] == ['ameaca'] and len(pos) in (2, 3): print(ameaca(pos[1], n=num(pos[2], 'quantos são') if len(pos) > 2 else None, arma=op.get('arma'), armadura=op.get('armadura')))
    elif pos[:1] == ['mede'] and len(pos) in (4, 5):
        especie(pos[1]); n = num(pos[4], 'quantos bichos') if len(pos) > 4 else None; fam = op.get('arma', 'espada'); mat = op.get('armadura', 'malha'); q = num(op.get('homens', '1'), 'quantos homens')
        sp = op.get('surpresa'); sp in (None, 'bicho', 'homem') or sys.exit(f'a surpresa diz quem foi surpreendido: bicho ou homem (veio "{sp}")')
        m = mede(pos[1], num(pos[2], 'o nível'), pos[3], n=n, lutas=num(op.get('lutas', '200'), 'quantas lutas'), familia=fam, material=mat, quantos=q, inicio=_inicio(op.get('inicio', 'perto')),
                 surpresa={'bicho': 'B', 'homem': 'A'}.get(sp))
        print(f"ENSAIO (não é a luta de verdade: dado de mentira, nada é guardado): {'um homem' if q == 1 else f'{q} homens'} de nível {pos[2]}, de {fam}, {mat}"
              f"{' e escudo' if T.FAMILIAS[fam]['maos'] == 1 else ''} {T.CATS[cat_i(pos[3])]}, contra {especie(pos[1])['nome']} ({f'{n} de uma vez' if n else 'quantos a sorte der, pelo bando da espécie'}), começando {op.get('inicio', 'perto')}{f', o {sp} surpreendido' if sp else ''}:\n"
              f"  vence {m['vence']}% (em {m['carcaca']}% fica bicho morto ou caído no campo; em {m['fugiu']}% todos fogem) · perde {m['perde']}% · mediana de {m['rodadas']} rodadas\n"
              f"  {'o homem' if q == 1 else 'o primeiro homem'} sai com ferida nova, caído ou morto em {m['ferido']}% das lutas (caído ou morto: {m['caiu']}%)")
    else: print(__doc__)
