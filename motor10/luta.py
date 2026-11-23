#!/usr/bin/env python3
"""luta.py — MOTOR 10: A LUTA. Grupo contra grupo, numa linha de casas (1 casa ≈ 3 m), turno a turno.

O que entra na conta (as regras estão no REGRAS.md; os números, no tabelas.py):
  1 distância e alcance · 2 o lugar (estreito, alto, cobertura, sem saída) · 3 o tempo (escuro, chuva, lama, neblina, vento, calor, água)
  4 fôlego · 5 golpe contra armadura · 6 parte do corpo e ferida · 7 durabilidade · 8 moral · 9 grupo contra grupo
  10 A LUTA PARA E PERGUNTA: quando algo muda, o turno acaba e o script devolve o quadro; a ordem do jogador volta por `ordem`.

Uso em código:
  S = nova(lado_a, lado_b, inicio='perto', lugar={...}, tempo=[...])     (listas de pessoas do pessoas.py; o lado A é o do jogador)
  corre(S, interativo=True)      roda até uma PARADA ou o fim · ordem(S, 'Nome: atacar Alvo agressiva')
  resultado(S)                   quem venceu, mortos, caídos, presos, feridas, peças quebradas
Uso de linha de comando (a luta de verdade: dado de verdade, o estado guardado num arquivo entre uma ordem e outra):
  python3 luta.py nova CENARIO.json lutas/NOME.json                       monta a luta e mostra o quadro
  python3 luta.py roda lutas/NOME.json ["Nome: ordem"] ["grupo: ordem"]   roda até a próxima PARADA (ou o fim) com as ordens dadas
       ordem: atacar [alvo] · segurar · avancar · recuar · folego · guardar NOME, e no fim a postura (firme, agressiva, defensiva)
       ordem do grupo: atacar · segurar · recuar
  python3 luta.py demo           uma luta de exemplo num corredor, com as paradas
"""
import json, math, random, secrets, sys
import tabelas as T
from pessoas import ficha


class Dados:
    def __init__(s, semente=None): s.r = random.Random(semente) if semente is not None else None
    def d(s, n): return s.r.randint(1, n) if s.r else secrets.randbelow(n) + 1
D = Dados()


def semente(n):
    """só para o simulador: dados que se repetem"""
    global D
    D = Dados(n)


def d20x():
    t = [D.d(20)]
    while t[-1] == 20: t.append(D.d(20))
    return t


def jogada(bonus, crit19=False):
    a, b = d20x(), d20x(); n = (a[0], b[0])
    return dict(total=sum(a) + sum(b) + bonus, falha=n == (1, 1), crit=(max(n) >= (19 if crit19 else 20) and min(n) >= T.CRIT_OUTRO))


def chance(falta):
    """a chance de 2d20 dar pelo menos `falta` (sem contar o 20 que explode; o crítico acerta sempre)"""
    n = math.ceil(falta)
    if n <= 2: return 1.0
    return max(0.05, sum(min(s - 1, 41 - s) for s in range(n, 41)) / 400)


def rola(dado, dobra=False):
    n, f = map(int, dado.split('d'))
    return sum(D.d(f) for _ in range(n * (2 if dobra else 1)))


# ---------- montar a luta ----------
SINONIMOS = {'colada': 'colado', 'água pela cintura': 'água', 'agua': 'água', 'tras': 'trás'}


def _confere(lado_a, lado_b, inicio, lugar, tempo, surpresa):
    """o cenário é conferido ANTES de qualquer dado: erro de digitação não derruba a luta no meio"""
    E = []
    if not (inicio in T.INICIO or (isinstance(inicio, int) and inicio >= 1)): E.append(f'início desconhecido: "{inicio}" (use: {", ".join(T.INICIO)}, ou um número de casas)')
    for t in tempo:
        if t not in T.TEMPO: E.append(f'tempo desconhecido: "{t}" (use: {", ".join(T.TEMPO)})')
    for k, v in lugar.items():
        if k not in ('largura', 'alto', 'cobertura', 'sem_saida'): E.append(f'chave de lugar desconhecida: "{k}" (use: largura, alto, cobertura, sem_saida)')
        elif k == 'largura' and not (v is None or (isinstance(v, int) and v >= 1)): E.append('a largura é um número de 1 para cima')
        elif k != 'largura' and v not in (None, 'A', 'B'): E.append(f'"{k}" diz de que lado: "A" ou "B" (veio "{v}")')
    if surpresa not in (None, 'A', 'B'): E.append(f'a surpresa diz o lado surpreendido: "A" ou "B" (veio "{surpresa}")')
    if not lado_a or not lado_b: E.append('cada lado precisa de pelo menos uma pessoa')
    nomes = [p['nome'] for p in lado_a + lado_b]
    if any(n.lower() == 'grupo' or ':' in n for n in nomes): E.append('ninguém pode se chamar "grupo" nem ter dois-pontos no nome (a ordem usa os dois)')
    for n in sorted(set(x for x in nomes if nomes.count(x) > 1)): E.append(f'nome repetido: "{n}" (cada um na luta tem um nome só dele)')
    for lado in (lado_a, lado_b):
        for p in lado:
            if p.get('linha') not in (None, 'frente', 'trás'): E.append(f'{p["nome"]}: a linha é "frente" ou "trás" (veio "{p.get("linha")}")')
            if p.get('moral') not in (None, 'testa', 'firme'): E.append(f'{p["nome"]}: a moral é "testa" ou "firme" (veio "{p.get("moral")}")')
            if p.get('papel') not in (None, 'frente', 'guarda'): E.append(f'{p["nome"]}: o papel é "frente" ou "guarda" (veio "{p.get("papel")}")')
            if p.get('guarda') and p['guarda'] not in [q['nome'] for q in lado if q is not p]: E.append(f'{p["nome"]} guarda "{p["guarda"]}", que não está do lado dele')
    if E: sys.exit('O cenário tem problema. Nenhum dado foi rolado.\n  - ' + '\n  - '.join(E))


def nova(lado_a, lado_b, inicio='perto', lugar=None, tempo=None, surpresa=None, quieto=False):
    inicio = SINONIMOS.get(inicio, inicio); tempo = [SINONIMOS.get(t, t) for t in (tempo or [])]; lugar = dict(lugar or {})
    for p in lado_a + lado_b:
        if p.get('linha') in SINONIMOS: p['linha'] = SINONIMOS[p['linha']]
    _confere(lado_a, lado_b, inicio, lugar, tempo, surpresa)
    S = dict(r=0, L=[], itens={}, lugar=lugar, tempo=tempo, log=[], paradas=['a luta vai começar'], fim=None, ordens={}, surpresa=surpresa, quieto=quieto,
             fila=[], comecou=False, usadas=[], sem_dano=0, sem_parada=0, dano_r=0, houve_parada=False, fechada=0, avisos=[])
    sep = T.INICIO[inicio] if isinstance(inicio, str) else inicio
    for lado, gente, x0, tras in (('A', lado_a, 0, -1), ('B', lado_b, sep, 1)):
        larg = lugar.get('largura') or 99; cheio = {}
        for p in sorted(gente, key=lambda p: p.get('linha') == 'trás'):
            f = ficha(p); f['lado'] = lado
            x = x0 + (tras if p.get('linha') == 'trás' else 0)
            while cheio.get(x, 0) >= larg: x += tras
            cheio[x] = cheio.get(x, 0) + 1
            f.update(x=x, estado='pe', feridas=[], sangra=None, atordoado=0, chao=False, preso=False, abalado=False, reac=f['reacoes'], postura='firme',
                     usou=[], testou=[], morte=[0, 0], agressor=None, recarga=0, sem_arma=False, resguardo=False, fugiu=False, golpeado=[], ini=0, pv_visto=f['pv'])
            f.setdefault('moral', 'testa'); f.setdefault('papel', 'guarda' if f.get('guarda') else 'frente')
            for w in (f['arma'], f['arma2'], f['punho']):
                if w: w['item'] = _guarda_item(S, w['item'])
            for pc in f['partes'].values(): pc['item'] = _guarda_item(S, pc['item'])
            for src in f['fontes']: src['item'] = _guarda_item(S, src['item'])
            if f['escudo']: f['escudo']['item'] = _guarda_item(S, f['escudo']['item'])
            if f['fol_rodada'] + f['arma']['folego'] > f['folmax']: S['avisos'].append(f"{f['nome']} veste mais peso do que o fôlego aguenta: vai lutar sem fôlego")
            if f['nuas'] and f['partes']: S['avisos'].append(f"{f['nome']} está sem proteção em: {', '.join(f['nuas'])}")
            S['L'].append(f)
    return S


def _guarda_item(S, it):
    for k, v in S['itens'].items():
        if v is it: return k
    k = f"p{len(S['itens']) + 1}"; S['itens'][k] = it
    return k


# ---------- olhar o campo ----------
def diz(S, txt):
    if not S['quieto']: S['log'].append(txt)
def de_pe(S, lado=None): return [f for f in S['L'] if f['estado'] == 'pe' and (lado is None or f['lado'] == lado)]
def outro(lado): return 'B' if lado == 'A' else 'A'
def inimigos(S, f): return de_pe(S, outro(f['lado']))
def dist(a, b): return abs(a['x'] - b['x'])
def frente(f): return 1 if f['lado'] == 'A' else -1
def entre(S, a, b): return any(min(a['x'], b['x']) < o['x'] < max(a['x'], b['x']) for o in de_pe(S) if o is not a and o is not b)
def lider(S, lado): return next((f for f in S['L'] if f['lado'] == lado and f.get('lider')), None)
def por_nome(S, nome): return next((f for f in S['L'] if f['nome'] == nome), None)
def inteiro(S, chave): return S['itens'][chave]['dur'][0] > 0


def arma_de(S, f):
    """a arma em uso agora: a principal; a segunda (ou as mãos) se a principal caiu, ou se é de tiro e há inimigo colado"""
    w = f['arma']
    if f['sem_arma'] or (w['distancia'] and any(dist(f, e) <= 1 for e in inimigos(S, f))): return f['arma2'] or f['punho']
    return w


def guarda_de(S, f):
    """(o bônus, a peça) do que apara os golpes agora: o escudo (arma de uma mão, escudo inteiro) ou a própria arma, o que for melhor"""
    w = arma_de(S, f); esc = f['escudo']
    if esc and w['maos'] == 1 and inteiro(S, esc['item']) and esc['bonus'] >= w['aparo']: return esc['bonus'], esc
    return w['aparo'], w


def defesa_de(S, f): return f['def_fixa'] + guarda_de(S, f)[0]


def efeito(S, f, chave):
    """o efeito de armadura ou escudo que está valendo agora (a peça desfeita não tem efeito)"""
    for src in f['fontes']:
        if chave in src['efeitos'] and inteiro(S, src['item']): return src['efeitos'][chave]
    return None


def _vaga(S, f, e, w):
    """o CERCO: em campo aberto só tantos batem corpo a corpo no mesmo alvo na mesma rodada"""
    if S['lugar'].get('largura'): return True
    longe = w['haste'] and dist(f, e) == 2
    if any(n == f['nome'] for n, _ in e['golpeado']): return True
    return sum(1 for _, l in e['golpeado'] if l == longe) < (T.CERCO_HASTE if longe else T.CERCO)


def alvos(S, f, w, cerco=True):
    """[(inimigo, penalidade)] que esta arma alcança agora"""
    out = []
    for e in inimigos(S, f):
        dd = dist(f, e)
        if w['distancia']:
            if dd < 2 or dd > w['alcance']: continue
            if any(dd > T.TEMPO[k]['sem_tiro_longe'] for k in S['tempo'] if 'sem_tiro_longe' in T.TEMPO[k]): continue
        else:
            if dd > max(1, w['alcance']): continue
            if cerco and not _vaga(S, f, e, w): continue
        pen = T.ENTRE if entre(S, f, e) and S['lugar'].get('alto') != f['lado'] else 0
        if w['haste'] and dd <= 1: pen += T.HASTE_COLADO
        out.append((e, pen))
    return out


# ---------- o golpe ----------
def golpe(S, a, e, w, livre=''):
    g = next((x for x in de_pe(S, e['lado']) if x.get('guarda') == e['nome'] and x is not e and dist(x, e) <= 1 and x['reac'] > 0), None)
    if g: g['reac'] -= 1; diz(S, f"  {g['nome']} se põe na frente de {e['nome']}"); e = g
    tiro = w['distancia']; pa, pd = T.POSTURAS[a['postura']], T.POSTURAS[e['postura']]
    if not tiro and not livre and not any(n == a['nome'] for n, _ in e['golpeado']): e['golpeado'].append([a['nome'], bool(w['haste'] and dist(a, e) == 2)])
    bon = w['acerto'] + pa[0] - (T.SEM_FOLEGO if a['fol'] <= 0 else 0) + (T.ABALADO if a['abalado'] else 0)
    bon += sum(T.FERIDAS['braços'][1 if gr else 0] for p, gr in a['feridas'] if p == 'braços')
    bon += sum(T.TEMPO[k].get('tiro' if tiro else 'acerto', 0) for k in S['tempo'])
    if S['lugar'].get('alto') == a['lado']: bon += T.ALTO['tiro' if tiro else 'acerto']
    if tiro and S['lugar'].get('cobertura') == e['lado']: bon += T.COBERTURA
    if entre(S, a, e) and S['lugar'].get('alto') != a['lado']: bon += T.ENTRE
    if w['haste'] and dist(a, e) <= 1: bon += T.HASTE_COLADO
    if tiro and a['fugiu']: bon += T.TIRO_FUGINDO
    df = defesa_de(S, e) + pd[1] - (T.SEM_FOLEGO if e['fol'] <= 0 else 0) + (T.CHAO if e['chao'] else 0) + (T.PRESO if e['preso'] else 0) + (T.RESGUARDO if e['resguardo'] else 0)
    df += sum(T.TEMPO[k].get('defesa', 0) for k in S['tempo'])
    df -= T.FLANCO * min(T.FLANCO_MAX, sum(1 for n, _ in e['golpeado'] if n != a['nome']))       # cercado: cada um que já bateu nele abre a guarda para o próximo
    tr = e['partes'].get('tronco')                                                                   # mirar a fresta: só contra armadura melhor que a arma, e só quando compensa
    mira = bool(tr and inteiro(S, tr['item']) and tr['cat'] > w['cat'] and chance(df - bon - T.MIRA_ACERTO) * T.MIRA_PROT > chance(df - bon))
    if mira: bon += T.MIRA_ACERTO
    if w['item'] not in S['usadas']: S['usadas'].append(w['item'])
    for pc in list(e['partes'].values()) + ([e['escudo']] if e['escudo'] else []):
        if pc['item'] not in S['usadas']: S['usadas'].append(pc['item'])
    j = jogada(bon, crit19=bool(w['efeitos'].get('critico_19')))
    cab = f"  {a['nome']} {'atira em' if tiro else 'golpeia'} {e['nome']}" + (f' ({livre})' if livre else '') + (' mirando a fresta' if mira else '')
    if j['falha']:
        diz(S, f"{cab}: dois 1, erra feio"); _gasta(S, a, w, 1); return
    if j['total'] < df and not j['crit']:
        gb, gp = guarda_de(S, e); aparado = not tiro and gb > 0 and df - j['total'] <= gb
        diz(S, f"{cab}: {j['total']:g} contra {df:g}, {'aparado' if aparado else 'erra'}")
        if aparado and gp['cat'] != w['cat']:                # dois aços se encontram: o pior gasta
            if gp['cat'] > w['cat']: _gasta(S, a, w, 1)
            elif gp is e['escudo']: _gasta_armadura(S, e, gp['nome'], gp['item'], 1)
            else: _gasta(S, e, gp, 1)
        return
    parte = T.ONDE[D.d(10)]; pc = e['partes'].get(parte); vestida = bool(pc and inteiro(S, pc['item']))
    prot = pc['rd'] * T.MATRIZ[w['golpe']][pc['material']] / (2 if j['crit'] else 1) if vestida else T.NU
    if mira and vestida and pc['cat'] > w['cat']: prot /= T.MIRA_PROT
    dano = int(rola(w['dado'], dobra=j['crit']) * T.K_DANO * w['mult'] / prot * w['fmult'])
    # o aço gasta o aço
    if dano == 0: _gasta(S, a, w, 1)
    if vestida and (w['cat'] > pc['cat'] or j['crit']): _gasta_armadura(S, e, pc['nome'], pc['item'], 2 if w['cat'] >= pc['cat'] + 2 else 1)
    esc = e['escudo']
    if j['crit'] and esc and inteiro(S, esc['item']) and arma_de(S, e)['maos'] == 1: _gasta_armadura(S, e, esc['nome'], esc['item'], 1)
    e['pv'] -= dano; e['agressor'] = a['nome']
    diz(S, f"{cab}: {j['total']:g} contra {df:g}{', CRÍTICO' if j['crit'] else ''}, {parte}: {dano} ({max(e['pv'], 0)}/{e['pvmax']})" + (' · o aço não passa' if dano == 0 else ''))
    dv = efeito(S, e, 'devolve')
    if not tiro and dv and a['estado'] == 'pe':
        a['pv'] -= dv; diz(S, f"    a armadura de {e['nome']} devolve {dv} em {a['nome']} ({max(a['pv'], 0)}/{a['pvmax']})"); S['dano_r'] += dv / a['pvmax']
        if a['pv'] <= 0: _cai(S, a, 0)
    if dano <= 0: return
    S['dano_r'] += dano / e['pvmax']
    terrivel = dano >= e['pvmax'] * T.FERIDA_GRAVE
    if e['pv'] <= 0: _cai(S, e, dano)
    elif dano >= e['pvmax'] * T.FERIDA or (j['crit'] and dano >= e['pvmax'] * T.FERIDA_MIN): _ferida(S, e, parte, terrivel, w, dano)
    if w['efeitos'].get('derruba') and 'derruba' not in a['usou'] and e['estado'] == 'pe' and not efeito(S, e, 'firme'):
        a['usou'].append('derruba'); e['chao'] = True; diz(S, f"    {e['nome']} vai ao chão")
    if terrivel:
        for o in de_pe(S, e['lado']):
            if o is not e and dist(o, e) <= 2: _moral(S, o, 'golpe_terrivel')
    if e['estado'] == 'pe' and e['pv'] < e['pvmax'] * 0.25: _moral(S, e, 'ferido_grave')


def _gasta(S, a, w, n):
    it = S['itens'][w['item']]
    if w['efeitos'].get('nao_quebra') or it['dur'][0] <= 0: return
    it['dur'][0] = max(0, it['dur'][0] - n)
    if it['dur'][0] == 0:
        diz(S, f"    ✖ {w['nome']} de {a['nome']} QUEBRA"); _para(S, a, f"{w['nome']} de {a['nome']} quebrou")
        w.update(acerto=w['acerto'] - T.BON[w['cat']] + T.QUEBRADA, mult=T.MULT[0] * (T.DUAS_MAOS if w['maos'] == 2 and not w['distancia'] else 1), cat=0, efeitos={}, aparo=0, nome=w['nome'] + ' (quebrada)')


def _gasta_armadura(S, e, nome, chave, n):
    it = S['itens'][chave]
    if it['dur'][0] <= 0 or any(src['item'] == chave and src['efeitos'].get('nao_quebra') for src in e['fontes']): return
    it['dur'][0] = max(0, it['dur'][0] - n)
    if it['dur'][0] == 0: diz(S, f"    ✖ {nome} de {e['nome']} se desfaz"); _para(S, e, f"{nome} de {e['nome']} quebrou")


def _ferida(S, e, parte, grave, w, dano):
    e['feridas'].append([parte, grave]); g = 1 if grave else 0; txt = f"    FERIDA{' GRAVE' if grave else ''} em {e['nome']}, {parte}: "; sangra = grave or bool(w['efeitos'].get('sangra'))
    if parte == 'cabeça': e['atordoado'] = max(e['atordoado'], T.FERIDAS['cabeça'][g]); txt += 'atordoado'
    elif parte == 'braços':
        txt += f"{T.FERIDAS['braços'][g]} no acerto"
        if grave and not e['sem_arma']: e['sem_arma'] = True; txt += ' e larga a arma'
    elif parte == 'tronco': e['fol'] = max(0, e['fol'] - T.FERIDAS['tronco'][g]); sangra = True; txt += 'perde o fôlego'
    else:
        if not efeito(S, e, 'firme'): e['chao'] = True
        e['preso'] = e['preso'] or grave; txt += 'vai ao chão' + (' e não anda mais' if grave else '')
    if sangra:
        n = T.SANGRA_RODADAS[1 if grave or w['efeitos'].get('sangra') else 0]; q = max(1, int(dano * T.SANGRA)); ant = e['sangra'] or [0, 0]
        e['sangra'] = [max(q, ant[0]), max(n, ant[1])]; txt += f' · sangra {e["sangra"][0]} por {e["sangra"][1]} rodadas'
    diz(S, txt); _para(S, e, f"{e['nome']} foi ferido ({parte}{', grave' if grave else ''})", so_controlado=True)


def _cai(S, e, dano):
    macico = dano > e['pvmax'] * 0.5
    e['estado'] = 'morto' if macico else 'caido'; e['pv'] = min(e['pv'], 0)
    diz(S, f"    ☠ {e['nome']} MORRE" if macico else f"    ▼ {e['nome']} CAI")
    _para(S, e, f"{e['nome']} {'morreu' if macico else 'caiu'}")
    aliados = de_pe(S, e['lado'])
    if e.get('lider'):
        for o in aliados: _moral(S, o, 'lider_caiu')
    if len(aliados) * 2 <= len([f for f in S['L'] if f['lado'] == e['lado']]):
        for o in aliados: _moral(S, o, 'metade_caiu')
    _fim(S)


def _moral(S, f, motivo):
    if f['moral'] == 'firme' or f['estado'] != 'pe' or (motivo in f['testou'] and motivo != 'golpe_terrivel') or f.get('moral_r') == [S['r'], motivo]: return
    f['testou'].append(motivo); f['moral_r'] = [S['r'], motivo]
    meus, deles = len(de_pe(S, f['lado'])), len(de_pe(S, outro(f['lado'])))
    ld = lider(S, f['lado']); bon = f['vontade_b'] + (T.MORAL_LIDER if ld and ld['estado'] == 'pe' and ld is not f else 0)
    bon += T.MORAL_MAIS if meus > deles else T.MORAL_MENOS if deles >= 2 * meus else 0
    t = sum(d20x()) + sum(d20x()) + bon; cd = T.MORAL[motivo]; que = motivo.replace('_', ' ')
    if t >= cd: return
    if f.get('controla'):       # quem o jogador comanda não foge nem se rende pelo dado: fica abalado, e a escolha é do jogador
        f['abalado'] = True; diz(S, f"    {f['nome']} FRAQUEJA ({que}: {t} contra {cd})"); _para(S, f, f"{f['nome']} fraquejou ({que}): lutar abalado, recuar ou render-se é escolha sua"); return
    if t > cd - T.MORAL_QUEBRA and not f['abalado']:
        f['abalado'] = True; diz(S, f"    {f['nome']} fica ABALADO ({que}: {t} contra {cd})"); return
    rende = f['pv'] < f['pvmax'] * 0.25 or S['lugar'].get('sem_saida') == f['lado']
    f['estado'] = 'rendido' if rende else 'fugiu'
    diz(S, f"    {f['nome']} {'SE RENDE' if rende else 'FOGE'} ({que}: {t} contra {cd})")
    _para(S, f, f"{f['nome']} {'se rendeu' if rende else 'fugiu'}")
    if not rende: _golpe_livre(S, f, 'ele dá as costas')
    if f.get('lider'):
        for o in de_pe(S, f['lado']): _moral(S, o, 'lider_caiu')
    _fim(S)


def _golpe_livre(S, f, porque, quem=None, vinha_de=None):
    """UM golpe livre em f, de um inimigo com reação e arma de corpo a corpo que o alcance (o de arma mais longa primeiro).
    quem: só estes podem dar · vinha_de: só de quem tem arma mais longa que a de f, e só se f acabou de ENTRAR no alcance dele"""
    meu = arma_de(S, f)['alcance']
    for e in sorted(quem if quem is not None else inimigos(S, f), key=lambda e: -arma_de(S, e)['alcance']):
        w = arma_de(S, e); alc = max(1, w['alcance'])
        if e['estado'] != 'pe' or e['reac'] <= 0 or w['distancia'] or dist(e, f) > alc: continue
        if vinha_de is not None and (w['alcance'] <= meu or abs(vinha_de - e['x']) <= alc): continue
        e['reac'] -= 1; golpe(S, e, f, w, livre=porque); return


def _para(S, f, txt, so_controlado=False):
    """uma PARADA: o que faz a luta parar e perguntar. Vale o que toca o lado do jogador (A), o líder do outro, e toda rendição."""
    if so_controlado and not f.get('controla'): return
    if f['lado'] == 'A' or f.get('lider') or 'rendeu' in txt:
        if txt not in S['paradas']: S['paradas'].append(txt)
        S['houve_parada'] = True


# ---------- o turno de cada um ----------
def _passo(S):
    return min([T.PASSO] + [T.TEMPO[k]['passo'] for k in S['tempo'] if 'passo' in T.TEMPO[k]])


def _ordem_de(S, a):
    """a ordem que vale para este lutador agora (a dele, se o jogador o comanda; a do grupo, se é do lado A e não guarda ninguém)"""
    if a.get('controla'): return (S['ordens'].get(a['nome']) or {}).get('acao')
    return S['ordens'].get('grupo') if a['lado'] == 'A' and a['papel'] != 'guarda' else None


def _fica(S, a):
    """este aliado não vai para a frente: num corredor, quem vem atrás pode trocar de lugar com ele"""
    if a['chao'] or a['preso'] or a['fol'] <= 0 or arma_de(S, a)['distancia']: return True
    o = _ordem_de(S, a)
    if o in ('recuar', 'folego'): return True
    if alvos(S, a, arma_de(S, a), cerco=False): return False
    g = por_nome(S, a.get('guarda') or '')
    return o == 'segurar' or bool(g and g['estado'] == 'pe' and dist(a, g) <= 1)


def _livre(S, f, nx, avanca):
    """dá para entrar na casa nx? 'sim' · 'troca' (corredor cheio: troca de lugar com um aliado) · 'contorna' (campo aberto:
    passa pela casa do inimigo que os outros seguram) · '' (não dá)"""
    larg = S['lugar'].get('largura'); la = [e for e in inimigos(S, f) if e['x'] == nx]
    if la:
        if larg or not avanca: return ''
        colados = [a for a in de_pe(S, f['lado']) if a is not f and any(dist(a, e) <= 1 for e in la)]
        return 'contorna' if len(colados) >= T.SEGURA * len(la) else ''
    if larg:
        meus = [a for a in de_pe(S, f['lado']) if a['x'] == nx and a is not f]
        if len(meus) >= larg: return 'troca' if any(_fica(S, a) == avanca for a in meus) else ''
    return 'sim'


def _rumo(S, f, w, alvo=None):
    """para que lado da linha andar (+1 ou −1) para chegar em quem a arma não alcança; 0 se não há para onde ir"""
    perto = [x[0] for x in alvos(S, f, w, cerco=False)]
    cand = [alvo] if alvo else [e for e in inimigos(S, f) if not any(e is p for p in perto)]
    cand = [e for e in cand if e['x'] != f['x']]
    if not cand: return 0
    e = min(cand, key=lambda e: dist(f, e))
    return 1 if e['x'] > f['x'] else -1


def _anda(S, f, dx, recuo=False, ate=None):
    """anda até PASSO casas para o lado dx da linha. Devolve as casas andadas.
    Quem se afasta de um inimigo colado leva o golpe livre dele (no avanço, só de quem não está seguro por dois dos seus)."""
    avanca = not recuo; passo = _passo(S)
    if avanca and dx == frente(f) and S['lugar'].get('alto') == outro(f['lado']): passo = 1       # subindo
    if not _livre(S, f, f['x'] + dx, avanca): return 0
    colados = [e for e in inimigos(S, f) if dist(f, e) <= 1 and abs(e['x'] - (f['x'] + dx)) > dist(f, e)]
    if avanca: colados = [e for e in colados if len([a for a in de_pe(S, f['lado']) if a is not f and dist(a, e) <= 1]) < T.SEGURA]
    if colados:
        if recuo: f['fugiu'] = True
        _golpe_livre(S, f, 'ele recua' if recuo else 'ele dá o flanco', quem=colados)
    andou = 0
    for _ in range(passo):
        if f['estado'] != 'pe' or f['chao'] or f['preso']: break      # o golpe que o pegou no caminho o parou
        nx = f['x'] + dx; como = _livre(S, f, nx, avanca)
        if not como: break
        al = alvos(S, f, arma_de(S, f))
        if avanca and como == 'sim' and (any(x[0] is ate for x in al) if ate else al): break    # já alcança: para aqui
        if como == 'troca':
            o = next(a for a in de_pe(S, f['lado']) if a['x'] == nx and a is not f and _fica(S, a) == avanca)
            o['x'] = f['x']; diz(S, f"  {f['nome']} troca de lugar com {o['nome']}")
        elif como == 'contorna': diz(S, f"  {f['nome']} contorna a linha")
        de = f['x']; f['x'] = nx; andou += 1
        if avanca: _golpe_livre(S, f, 'o alcance bate primeiro', vinha_de=de)
        if como != 'sim': break
    return andou


def _decide(S, f, pagou):
    """o que este lutador faz com a ação: ('golpe', alvo) · ('anda', lado, recuo?, até quem) · ('folego',) · ('levanta',) · ('pega',) · ('recarrega',) · ('espera',)"""
    w = arma_de(S, f); o = S['ordens'].get(f['nome']) or {}
    if not f.get('controla'): o = dict(acao=_ordem_de(S, f)) if _ordem_de(S, f) else {}
    acao = o.get('acao', 'atacar'); f['postura'] = o.get('postura', f['postura'] if f.get('controla') else 'firme')
    custo = w['folego'] + (0 if pagou else _peso(S, f))
    if acao == 'folego' or f['fol'] < min(custo, f['folmax']): return ('folego',)
    if f['chao']: return ('levanta',)
    colado = any(dist(f, e) <= 1 for e in inimigos(S, f))
    if f['sem_arma'] and not colado: return ('pega',)
    tras = -frente(f); pode_recuar = not f['preso'] and bool(_livre(S, f, f['x'] + tras, False))
    if acao == 'recuar':
        if min([dist(f, e) for e in inimigos(S, f)] or [9]) < 3 and pode_recuar: return ('anda', tras, True, None)
        acao = 'atacar' if colado else 'segurar'            # longe o bastante, segura; encurralado, luta
    if w['distancia'] and f['recarga'] > 0: return ('recarrega',)
    if not f.get('controla') and f['arma']['distancia'] and not f['sem_arma'] and colado and pode_recuar and not f['fugiu']: return ('anda', tras, True, None)   # o atirador se afasta de quem colou
    al = alvos(S, f, w); nome = o.get('alvo'); pref = next((x for x in inimigos(S, f) if x['nome'] == nome), None) if nome else None
    if nome and not pref:
        if f.get('controla'): _para(S, f, f"o alvo de {f['nome']} ({nome}) não está mais de pé")
        o['alvo'] = None
    if pref and not any(x[0] is pref for x in al) and not f['preso']:      # o alvo da ordem está fora de alcance: vai até ele
        dx = _rumo(S, f, w, pref)
        if dx and _livre(S, f, f['x'] + dx, True): return ('anda', dx, False, pref)
    if al:
        e = next((x for x in al if x[0] is pref), None)
        if not e:
            limpos = [x for x in al if x[1] == 0] or al
            ag = next((x for x in limpos if x[0]['nome'] == f['agressor']), None)
            e = ag if ag and D.d(10) <= 6 else min(limpos, key=lambda x: x[0]['pv'] / x[0]['pvmax'])
        return ('golpe', e[0])
    gd = next((x for x in de_pe(S, f['lado']) if x['nome'] == f.get('guarda')), None)
    if gd:
        if dist(f, gd) <= 1: return ('espera',)
        s = 1 if gd['x'] > f['x'] else -1
        if not f['preso'] and _livre(S, f, f['x'] + s, True): return ('anda', s, False, None)     # sem caminho até o guardado, luta como soldado
    if f['preso']: return ('espera',)
    if acao == 'segurar':
        apanha = any(arma_de(S, e)['distancia'] or dist(e, f) <= max(1, arma_de(S, e)['alcance']) for e in inimigos(S, f))
        if not apanha: return ('espera',)
        if f.get('controla'):
            _para(S, f, f"{f['nome']} está ao alcance deles e não alcança ninguém: segurar assim é só apanhar"); return ('espera',)
    dx = _rumo(S, f, w)
    return ('anda', dx, False, None) if dx else ('espera',)


def _peso(S, f):
    """o fôlego que a armadura cobra numa rodada em que a pessoa se mexe"""
    return f['fol_rodada'] + sum(T.TEMPO[k].get('folego', 0) for k in S['tempo']) + (sum(T.TEMPO[k].get('folego_armadura', 0) for k in S['tempo']) if any(p['material'] != 'couro' for p in f['partes'].values()) else 0)


def _turno(S, f):
    f['resguardo'] = False; f['reac'] = f['reacoes']; f['fugiu'] = False
    zerado = f['fol'] <= 0                                     # começou o turno sem fôlego: uma ação só
    f['fol'] = min(f['folmax'], f['fol'] + 1 + T.POSTURAS[f['postura']][2])
    custos = [1] if zerado else [1] * T.ACOES + list(f['esforcos'])
    if f['atordoado']:
        perde = min(len(custos), f['atordoado']); custos = custos[perde:]; f['atordoado'] = 0; diz(S, f"  {f['nome']} está atordoado: perde {perde} ação(ões)")
    pagou = False; feitas = 0
    for mult in custos:
        if f['estado'] != 'pe' or S['fim']: break
        ac = _decide(S, f, pagou); w = arma_de(S, f)
        if feitas >= T.ACOES:                                  # a ação A MAIS (o esforço): só para golpear, e guardando um terço do fôlego (a postura agressiva gasta tudo)
            if ac[0] != 'golpe' or f['postura'] == 'defensiva': break
            if f['fol'] - w['folego'] * mult < (0 if f['postura'] == 'agressiva' else f['folmax'] // 3): break
        feitas += 1
        if ac[0] in ('golpe', 'anda') and not pagou: pagou = True; f['fol'] -= _peso(S, f)
        if ac[0] == 'folego':
            g = rola(T.TOMA_FOLEGO[0]) + T.TOMA_FOLEGO[1]; f['fol'] = min(f['folmax'], max(f['fol'], 0) + g); f['resguardo'] = True; diz(S, f"  {f['nome']} toma fôlego (+{g}: {f['fol']}/{f['folmax']})")
        elif ac[0] == 'levanta': f['chao'] = False; diz(S, f"  {f['nome']} se levanta")
        elif ac[0] == 'pega': f['sem_arma'] = False; diz(S, f"  {f['nome']} apanha a arma")
        elif ac[0] == 'recarrega': f['recarga'] -= 1
        elif ac[0] == 'espera': f['resguardo'] = True; break
        elif ac[0] == 'anda':
            k = _anda(S, f, ac[1], recuo=ac[2], ate=ac[3])
            if not k: f['resguardo'] = True; break
            f['fol'] -= mult; diz(S, f"  {f['nome']} {'recua' if ac[2] else 'avança'} ({k} casa{'s' if k > 1 else ''})")
        elif ac[0] == 'golpe':
            golpe(S, f, ac[1], w); f['fol'] -= w['folego'] * mult; f['recarga'] = w['recarga'] if w['distancia'] else 0
        _fim(S)
    if f['fol'] > 0: f['avisou_fol'] = False
    elif f['estado'] == 'pe' and f.get('controla') and not f.get('avisou_fol'): f['avisou_fol'] = True; _para(S, f, f"{f['nome']} está sem fôlego")


def _fim(S):
    if S['fim']: return
    a, b = de_pe(S, 'A'), de_pe(S, 'B')
    if not a and not b: S['fim'] = 'ninguém'
    elif not a: S['fim'] = 'B'
    elif not b: S['fim'] = 'A'


def _abre_rodada(S):
    S['r'] += 1; S['dano_r'] = 0; S['houve_parada'] = False; diz(S, f"— RODADA {S['r']} —")
    vivos = de_pe(S)
    for f in S['L']: f['golpeado'] = []
    for f in vivos: f['ini'] = sum(d20x()) + sum(d20x()) + f['percep_b'] + f['agil_b'] + f['ini_mod']
    S['fila'] = [f['nome'] for f in sorted(vivos, key=lambda f: -f['ini'])]


def _fecha_rodada(S):
    if S['fechada'] == S['r']: return
    S['fechada'] = S['r']
    for f in S['L']:                                        # o sangue e a vida por um fio
        if f['estado'] == 'pe' and f['sangra']:
            f['pv'] -= f['sangra'][0]; f['sangra'][1] -= 1; S['dano_r'] += f['sangra'][0] / f['pvmax']
            if f['sangra'][1] <= 0: f['sangra'] = None
            if f['pv'] <= 0: diz(S, f"  {f['nome']} sangra até cair"); _cai(S, f, 0)
        elif f['estado'] == 'caido' and max(f['morte']) < 3:
            ok = D.d(20) >= T.MORTE_CD; f['morte'][0 if ok else 1] += 1
            if f['morte'][1] >= 3: f['estado'] = 'morto'; diz(S, f"  ☠ {f['nome']} morre no chão"); _para(S, f, f"{f['nome']} morreu no chão")
    for f in de_pe(S):                                      # a retirada: quem recua e ficou longe de todos saiu da luta
        if _ordem_de(S, f) == 'recuar' and all(dist(f, e) >= T.RETIRADA for e in inimigos(S, f)):
            f['estado'] = 'saiu'; diz(S, f"  {f['nome']} SAI DA LUTA"); _para(S, f, f"{f['nome']} saiu da luta")
    _fim(S)
    S['sem_dano'] = 0 if S['dano_r'] >= T.IMPASSE_MIN else S['sem_dano'] + 1
    if S['sem_dano'] >= T.IMPASSE and not S['fim']:
        S['fim'] = 'impasse'; diz(S, f"  IMPASSE: {T.IMPASSE} rodadas em que ninguém feriu ninguém de verdade. Os dois lados se separam.")
    S['sem_parada'] = 0 if S['houve_parada'] else S['sem_parada'] + 1
    if S['sem_parada'] >= 3 and not S['fim']: S['paradas'].append('três rodadas sem novidade'); S['sem_parada'] = 0


def passo(S):
    """o turno de UM lutador (abre a rodada se for o caso, e a fecha depois do último)"""
    if not S['fila']: _abre_rodada(S)
    f = por_nome(S, S['fila'].pop(0))
    if f['estado'] == 'pe' and not S['fim'] and not (S['r'] == 1 and S['surpresa'] == f['lado']):
        _turno(S, f)
        for c in S['L']:                                    # quem o jogador comanda passou de metade ou de um quarto do PV?
            if c.get('controla') and c['estado'] == 'pe':
                for lim in (0.5, 0.25):
                    if c['pv_visto'] >= c['pvmax'] * lim > c['pv']: _para(S, c, f"{c['nome']} está abaixo de {int(lim * 100)}% do PV")
                c['pv_visto'] = c['pv']
    if not S['fila'] or S['fim']: S['fila'] = []; _fecha_rodada(S)


def rodada(S):
    """uma rodada inteira, sem parar (o simulador e as provas usam)"""
    passo(S)
    while S['fila']: passo(S)


def _fecha_luta(S):
    """o fim: quem caiu do lado que ficou com o campo é estancado pelos seus; os outros rolam até o fim"""
    if S.get('luta_fechada'): return
    S['luta_fechada'] = True
    for k in S['usadas']:                                   # o uso: toda peça que entrou na luta perde 1 (menos a que não quebra e a que já quebrou)
        it = S['itens'][k]
        if it['dur'][0] > 0 and not any(x.get('chave') == 'nao_quebra' for x in it.get('efeitos', [])): it['dur'][0] -= 1
    for f in S['L']:
        if f['estado'] != 'caido': continue
        if f['lado'] == S['fim']: f['estavel'] = True; continue
        while max(f['morte']) < 3: f['morte'][0 if D.d(20) >= T.MORTE_CD else 1] += 1
        if f['morte'][1] >= 3: f['estado'] = 'morto'; diz(S, f"  ☠ {f['nome']} não resiste aos ferimentos")
        else: f['estavel'] = True


def corre(S, interativo=False, maximo=T.MAX_RODADAS):
    """roda até acabar. Com interativo, devolve 'parada' antes da 1ª rodada e sempre que houver o que perguntar; a ordem volta por ordem()."""
    if interativo and not S['comecou']: S['comecou'] = True; return 'parada'
    S['comecou'] = True; S['paradas'] = []
    while not S['fim']:
        if not S['fila'] and S['r'] >= maximo: break
        passo(S)
        if interativo and S['paradas'] and not S['fim']: return 'parada'
    if not S['fim']: S['fim'] = 'empate'
    _fecha_luta(S)
    return 'fim'


def resultado(S):
    q = lambda est: [f['nome'] for f in S['L'] if f['estado'] == est]
    return dict(vencedor=S['fim'], rodadas=S['r'], mortos=q('morto'), caidos=q('caido'), fugiram=q('fugiu'), sairam=q('saiu'), presos=q('rendido'),
                feridas={f['nome']: f['feridas'] for f in S['L'] if f['feridas']},
                quebradas=[it.get('nome', k) for k, it in S['itens'].items() if it['dur'][0] <= 0 and it.get('nome') != 'as mãos'])


def situacao(S):
    """o quadro que o jogador vê quando a luta para"""
    L = [f"RODADA {S['r']} · " + ' · '.join(S['tempo'] or ['tempo limpo']) + (f" · lugar: {S['lugar']}" if S['lugar'] else '')]
    for lado, nome in (('A', 'A CASA'), ('B', 'O OUTRO LADO')):
        L.append(nome + ':')
        for f in S['L']:
            if f['lado'] != lado: continue
            est = dict(pe='de pé', caido='CAÍDO', morto='MORTO', fugiu='fugiu', rendido='rendido', saiu='saiu')[f['estado']]
            fer = ', '.join(p + (' (grave)' if g else '') for p, g in f['feridas'])
            L.append(f"  {f['nome']:<22} {est:<8} PV {max(f['pv'], 0):>4}/{f['pvmax']:<4} fôlego {max(f['fol'], 0):>2}/{f['folmax']:<2} casa {f['x']:>3}"
                     + (f" · feridas: {fer}" if fer else '') + (f" · sangrando ({f['sangra'][0]} por rodada)" if f['sangra'] and f['estado'] == 'pe' else '')
                     + (' · abalado' if f['abalado'] else '') + (' · no chão' if f['chao'] else '') + (' · sem a arma' if f['sem_arma'] else ''))
    if S['r'] == 0 and S['avisos']: L.append('AVISOS: ' + ' · '.join(S['avisos']))
    if S['paradas']: L.append('PAROU PORQUE: ' + ' · '.join(S['paradas']))
    return '\n'.join(L)


# ---------- o simulador (o banco de provas usa) ----------
def duelos(faz_a, faz_b, n=1000, **kw):
    """n lutas entre os lados que faz_a() e faz_b() montam. Devolve (% de vitória de A, mediana de rodadas)."""
    va = 0; rs = []
    for _ in range(n):
        S = nova(faz_a(), faz_b(), quieto=True, **kw); corre(S)
        va += 1 if S['fim'] == 'A' else 0 if S['fim'] == 'B' else 0.5; rs.append(S['r'])
    rs.sort()
    return round(100 * va / n), rs[len(rs) // 2]


# ---------- a luta de verdade: o cenário, o arquivo da luta e as ordens ----------
def cenario(arq):
    """monta a luta de um arquivo de cenário: {"inicio","lugar","tempo","surpresa","A":[pessoa...],"B":[pessoa...]}
    pessoa = {"nome","nivel", "molde"?, "maestria"?, "atributos"?, "controla"?, "lider"?, "guarda"?, "moral"?, "linha"?,
              "veste": {"arma", "arma2", "armadura", "elmo", "escudo", "pecas": [...]}}
    cada peça é o id de um item do Livro de Itens, ou o atalho ["espada","Raro"] (armadura: ["malha","Raro"] veste corpo e elmo; escudo: "Raro")."""
    from pessoas import padrao, veste
    from itens import carrega, cat_i
    C = json.load(open(arq, encoding='utf-8')); B = carrega()['itens']
    def peca(x, tipo):
        if x is None or x is False: return x
        if isinstance(x, str) and x in B: return B[x]
        if isinstance(x, str) and tipo != 'escudo': sys.exit(f'não há o item "{x}" no Livro de Itens (itens.py ver)')
        return cat_i(x) if tipo == 'escudo' else (x[0], cat_i(x[1]))
    def pessoa(d):
        d = dict(d); v = d.pop('veste', {})
        ruins = [k for k in v if k not in ('arma', 'arma2', 'armadura', 'elmo', 'escudo', 'pecas')]
        if ruins: sys.exit(f'{d.get("nome")}: não sei vestir "{ruins[0]}" (use: arma, arma2, armadura, elmo, escudo, pecas)')
        p = padrao(d.pop('nome'), d.pop('nivel'), molde=d.pop('molde', 'guerreiro'), maestria=d.pop('maestria', None), atributos=d.pop('atributos', None), **d)
        return veste(p, arma=peca(v.get('arma'), 'arma'), arma2=peca(v.get('arma2'), 'arma'), armadura=peca(v.get('armadura'), 'armadura'), elmo=peca(v.get('elmo'), 'armadura'),
                     escudo=peca(v.get('escudo'), 'escudo'), pecas=[peca(x, 'armadura') for x in v.get('pecas', [])])
    return nova([pessoa(x) for x in C['A']], [pessoa(x) for x in C['B']], inicio=C.get('inicio', 'perto'), lugar=C.get('lugar'), tempo=C.get('tempo'), surpresa=C.get('surpresa'))


def salva(S, arq):
    """guarda a luta no arquivo e devolve ao Livro de Itens a durabilidade gasta até aqui"""
    json.dump(S, open(arq, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    from itens import carrega, grava
    B = carrega(); mudou = False
    for it in S['itens'].values():
        if it.get('id') in B['itens'] and B['itens'][it['id']]['dur'] != it['dur']: B['itens'][it['id']]['dur'] = it['dur']; mudou = True
    if mudou: grava(B)


def ordem(S, txt):
    """'Nome: atacar [alvo] [postura]' · ação: atacar, segurar, avancar, recuar, folego, guardar NOME · 'grupo: atacar|segurar|recuar'.
    Só o lado A recebe ordem. Nome que não existe é recusado, com a lista de quem está de pé."""
    quem, _, resto = txt.partition(':'); quem = quem.strip(); pal = resto.split()
    if not pal: sys.exit(f'ordem vazia: "{txt}"')
    if quem.lower() == 'grupo':
        if len(pal) != 1 or pal[0] not in ('atacar', 'segurar', 'recuar'): sys.exit(f'a ordem do grupo é uma palavra só: atacar, segurar ou recuar (veio "{resto.strip()}")')
        S['ordens']['grupo'] = pal[0]; return
    acha = lambda nome, gente: next((x for x in gente if x['nome'].lower() == nome.lower()), None)
    meus, deles = de_pe(S, 'A'), de_pe(S, 'B')
    f = acha(quem, meus)
    if not f: sys.exit(f'não há "{quem}" de pé do seu lado. De pé: {", ".join(x["nome"] for x in meus)}')
    post = pal.pop() if pal[-1] in T.POSTURAS else None
    if not pal: pal = ['atacar']
    acao = pal[0]; resto = ' '.join(pal[1:]) or None
    if acao not in ('atacar', 'segurar', 'avancar', 'recuar', 'folego', 'guardar'): sys.exit(f'ação desconhecida: "{acao}" (use: atacar, segurar, avancar, recuar, folego, guardar)')
    alvo = None
    if acao == 'guardar':
        g = acha(resto or '', [x for x in meus if x is not f])
        if not g: sys.exit(f'guardar quem? Do seu lado, de pé: {", ".join(x["nome"] for x in meus if x is not f)}')
        f['guarda'] = g['nome']
    elif resto:
        if acao != 'atacar': sys.exit(f'"{acao}" não leva nome (veio "{resto}")')
        e = acha(resto, deles)
        if not e: sys.exit(f'não há "{resto}" de pé do outro lado. De pé: {", ".join(x["nome"] for x in deles)}')
        alvo = e['nome']
    if acao in ('atacar', 'avancar'): f['guarda'] = None
    f['controla'] = True
    S['ordens'][f['nome']] = dict(acao='atacar' if acao in ('avancar', 'guardar') else acao, alvo=alvo, **({'postura': post} if post else {}))


def _demo():
    from pessoas import padrao, veste
    from itens import item
    semente(7)
    rei = veste(padrao('o ferreiro', 40, controla=True, linha='trás'), arma=('lança', 3), armadura=('couro', 2))
    a = [veste(padrao('Moreth', 120, moral='firme', lider=True), arma=item('arma', 4, 'a Maça do Rio', familia='maça', efeitos=[dict(chave='derruba')]), armadura=('malha', 4), escudo=3),
         veste(padrao('Gonde', 32, guarda='o ferreiro', moral='firme'), arma=('espada', 2), armadura=('malha', 2), escudo=2), rei]
    b = [veste(padrao('Nutoccone', 90, lider=True), arma=('espada', 3), armadura=('malha', 2), escudo=2)] + \
        [veste(padrao(f'herdeiro {i}', 30 + 5 * i), arma=('lança' if i % 2 else 'machado', 1), armadura=('couro', 1)) for i in range(1, 7)]
    S = nova(a, b, inicio='perto', lugar=dict(largura=2, sem_saida='B'), tempo=['escuro'])
    ordem(S, 'o ferreiro: segurar defensiva')
    while corre(S, interativo=True) == 'parada':
        print('\n'.join(S['log'])); S['log'] = []; print(); print(situacao(S)); print()
        if any('abaixo de 50%' in p for p in S['paradas']): ordem(S, 'o ferreiro: recuar defensiva'); print('>>> ordem: o ferreiro recua\n')
    print('\n'.join(S['log'])); print(); print(situacao(S)); print(); print(json.dumps(resultado(S), ensure_ascii=False))


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[:1] == ['demo']: _demo()
    elif a[:1] == ['nova'] and len(a) >= 3:
        S = cenario(a[1]); S['comecou'] = True; salva(S, a[2]); print(situacao(S))
        print(f'\nA luta está em {a[2]}. As ordens: python3 luta.py roda {a[2]} "Nome: atacar Alvo agressiva" "grupo: segurar"')
    elif a[:1] == ['roda'] and len(a) >= 2:
        S = json.load(open(a[1], encoding='utf-8'))
        if S['fim']: sys.exit('esta luta já acabou.')
        for o in a[2:]: ordem(S, o)
        S['log'] = []; fim = corre(S, interativo=True)
        print('\n'.join(S['log'])); print(); print(situacao(S))
        if fim == 'fim': print(); print('FIM:', json.dumps(resultado(S), ensure_ascii=False))
        salva(S, a[1])
    else: print(__doc__)
