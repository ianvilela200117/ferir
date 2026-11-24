#!/usr/bin/env python3
"""luta.py — MOTOR 10: A LUTA. Grupo contra grupo, numa linha de casas (1 casa ≈ 3 m), turno a turno.

O que entra na conta (as regras estão no REGRAS.md; os números, no tabelas.py):
  1 distância e alcance · 2 o lugar (estreito, alto, cobertura, sem saída) · 3 o tempo (escuro, chuva, lama, neblina, vento, calor, água)
  4 fôlego · 5 golpe contra armadura · 6 parte do corpo e ferida · 7 durabilidade · 8 moral · 9 grupo contra grupo
  10 A LUTA PARA E PERGUNTA: quando algo muda, o turno acaba e o script devolve o quadro; a ordem do jogador volta por `ordem`.
     O que a luta diz de GENTE não depende de gênero (a luta não sabe o gênero de ninguém): CAIU, MORREU, FRAQUEJA, "levou uma ferida". Do bicho, a espécie diz o gênero.
  11 OS BICHOS (bichos.py; os números, no tabelas_bichos.py): o corpo é a arma e a armadura, com categoria, e não é peça (não quebra);
     o tamanho mexe no PV, no alcance, no cerco, no corredor e na Defesa; os traços (lista fechada); a moral do bicho (foge ferido, não se rende).

Uso em código:
  S = nova(lado_a, lado_b, inicio='perto', lugar={...}, tempo=[...])     (listas de pessoas do pessoas.py; o lado A é o do jogador)
  corre(S, interativo=True)      roda até uma PARADA ou o fim · ordem(S, 'Nome: atacar Alvo agressiva')
  resultado(S)                   quem venceu, mortos, caídos, presos, feridas, peças quebradas
Uso de linha de comando (a luta de verdade: dado de verdade, o estado guardado num arquivo entre uma ordem e outra):
  python3 luta.py nova CENARIO.json lutas/NOME.json                       monta a luta e mostra o quadro
  python3 luta.py roda lutas/NOME.json ["Nome: ordem"] ["grupo: ordem"]   roda até a próxima PARADA (ou o fim) com as ordens dadas
       ordem: atacar [alvo] · segurar · avancar · recuar · folego · guardar NOME, e no fim a postura (firme, agressiva, defensiva)
              (a ordem `folego` acaba quando o fôlego enche: daí a pessoa segura, e a luta para e pergunta)
              (a ordem `recuar` é a retirada: a pessoa anda para trás enquanto houver inimigo de pé a menos de 8 casas; a 8 casas de todos, no fim da rodada, sai da luta.
               SEM INIMIGO DE PÉ NÃO HÁ RETIRADA: a luta acabou, e quem recuava ficou com o campo como os outros)
       ordem do grupo: atacar · segurar · recuar
  python3 luta.py demo           uma luta de exemplo num corredor, com as paradas
"""
import json, math, random, secrets, sys
import tabelas as T
import tabelas_bichos as TB
from criaturas import ficha_j as ficha
import tabelas_criaturas as TC
import criaturas as CR


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


def rola(dado, vezes=1):
    n, f = map(int, dado.split('d'))
    return sum(D.d(f) for _ in range(n * vezes))


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
            if p.get('guarda') and p['guarda'] not in [q['nome'] for q in lado if q is not p]: E.append(f'{p["nome"]} guarda "{p["guarda"]}", que não está do mesmo lado')
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
            f = ficha(p); f['lado'] = lado; oc = f.get('ocupa', 1)       # o que cada um toma do corredor: gente 1; o bicho, pelo tamanho
            x = x0 + (tras if p.get('linha') == 'trás' else 0)
            while cheio.get(x, 0) and cheio[x] + oc > larg: x += tras
            cheio[x] = cheio.get(x, 0) + oc
            f.update(x=x, estado='pe', feridas=[], sangra=None, atordoado=0, chao=False, preso=False, abalado=False, reac=f['reacoes'], postura='firme',
                     usou=[], testou=[], morte=[0, 0], agressor=None, recarga=0, sem_arma=False, resguardo=False, fugiu=False, golpeado=[], ini=0, pv_visto=f['pv'],
                     veneno=None, agarrado=None, encurralado=False, golpes=0, andou_t=0, feriu_t=[], sopro_r=0)
            f.setdefault('moral', 'testa'); f.setdefault('papel', 'guarda' if f.get('guarda') else 'frente'); _estado_j(f)
            f['feridas'] = f.pop('feridas0'); f['feridas_antes'] = len(f['feridas'])
            for parte, grave in f['feridas']:               # a ferida que a pessoa já traz entra na luta com ela
                if parte == 'tronco': f['fol'] = max(0, f['fol'] - T.FERIDAS['tronco'][1 if grave else 0])
                if parte == 'pernas' and grave: f['preso'] = True
            for w in [f['arma'], f['arma2'], f['punho']] + f.get('armas_corpo', []) + [f.get('sopro'), f.get('tiro')] + list(f.get('arma_arte', {}).values()):
                if w: w['item'] = _guarda_item(S, w['item'])
            for pc in f['partes'].values(): pc['item'] = _guarda_item(S, pc['item'])
            for src in f['fontes']: src['item'] = _guarda_item(S, src['item'])
            if f['escudo']: f['escudo']['item'] = _guarda_item(S, f['escudo']['item'])
            if f['fol_rodada'] + f['arma']['folego'] > f['folmax']: S['avisos'].append(f"{f['nome']} veste mais peso do que o fôlego aguenta: vai lutar sem fôlego")
            if f['nuas'] and f['partes']: S['avisos'].append(f"{f['nome']} está sem proteção em: {', '.join(f['nuas'])}")
            if oc > larg: S['avisos'].append(f"{f['nome']} é maior que o corredor: luta sem espaço")
            S['L'].append(f)
    return S


def _guarda_item(S, it):
    for k, v in S['itens'].items():
        if v is it: return k
    k = f"p{len(S['itens']) + 1}"; S['itens'][k] = it
    return k


# ---------- olhar o campo ----------
def diz(S, txt):
    if not S['quieto']: S['log'].append(TB.contrai(txt))
def _n(x): return f'{x:g}'.replace('.', ',')                 # 23,5
def _oa(f): return 'A' if f.get('bicho') and TB.ESPECIES.get(f['bicho'], {}).get('artigo') == 'a' else 'O'       # ENCURRALADA: o gênero do BICHO, que a espécie diz. De gente a luta não sabe o gênero: as frases de gente não dependem dele
def _acoes(n): return f"{n} {'ação' if n == 1 else 'ações'}"
def _parte(e, parte): return TB.PARTES_BICHO.get(parte, parte) if e.get('bicho') else parte                       # bicho não tem braços
SUSTOS = dict(lider_caiu='o líder caiu', metade_caiu='metade dos seus caiu', golpe_terrivel='o golpe terrível', ferido_grave='por um fio', ferido='a ferida', pavor='o pavor')
def de_pe(S, lado=None): return [f for f in S['L'] if f['estado'] == 'pe' and (lado is None or f['lado'] == lado)]
def outro(lado): return 'B' if lado == 'A' else 'A'
def inimigos(S, f): return de_pe(S, outro(f['lado']))
def dist(a, b): return abs(a['x'] - b['x'])
def frente(f): return 1 if f['lado'] == 'A' else -1
def entre(S, a, b): return any(min(a['x'], b['x']) < o['x'] < max(a['x'], b['x']) for o in de_pe(S) if o is not a and o is not b)
def lider(S, lado): return next((f for f in S['L'] if f['lado'] == lado and f.get('lider')), None)
def por_nome(S, nome): return next((f for f in S['L'] if f['nome'] == nome), None)
def inteiro(S, chave): return S['itens'][chave]['dur'][0] > 0
def tem(f, traco): return traco in f.get('tracos', ())          # o traço de bicho (lista fechada do tabelas_bichos)


def _agarrado(S, f):
    """quem agarra este lutador agora (ou None). O bicho que cai, foge ou se afasta solta: só se agarra quem está colado."""
    if not f.get('agarrado'): return None
    g = por_nome(S, f['agarrado'])
    if g and g['estado'] == 'pe' and dist(g, f) <= 1: return g
    f['agarrado'] = None
    return None


def _nao_anda(S, f): return bool(f['preso'] or f.get('raiz', 0) > 0 or _agarrado(S, f))
def _no_ar(S, f): return tem(f, 'voa') and not f['chao'] and not f['preso'] and not S['lugar'].get('largura') and not _agarrado(S, f)
def _derruba(S, a, e): return e['estado'] == 'pe' and not efeito(S, e, 'firme') and e.get('ocupa', 1) <= a.get('ocupa', 1) and not tem(e, 'imaterial')      # ninguém derruba quem é maior que ele


def _apertado(S, f):
    """o bicho maior que o corredor luta apertado"""
    larg = S['lugar'].get('largura')
    return TB.APERTADO * math.ceil(f['ocupa'] - larg) if larg and f.get('ocupa', 1) > larg else 0


def arma_de(S, f):
    """a arma em uso agora: a principal; a segunda (ou as mãos) se a principal caiu, ou se é de tiro e há inimigo colado"""
    if f.get('bicho'):
        if f.get('tiro') and not any(dist(f, e) <= max(1, f['armas_corpo'][0]['alcance']) for e in inimigos(S, f)): return f['tiro']       # ATIRA: de longe, o tiro do corpo
        return f['armas_corpo'][f['golpes'] % len(f['armas_corpo'])]      # o bicho alterna as armas do corpo, golpe a golpe
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
    """o CERCO: em campo aberto só tantos batem corpo a corpo no mesmo alvo na mesma rodada (em volta do bicho, pelo tamanho dele)"""
    if S['lugar'].get('largura'): return True
    longe = w['haste'] and dist(f, e) == 2
    if any(n == f['nome'] for n, _ in e['golpeado']): return True
    perto, haste = e.get('cerco') or (T.CERCO, T.CERCO_HASTE)
    return sum(1 for _, l in e['golpeado'] if l == longe) < (haste if longe else perto)


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
    S['ult'] = None
    g = None if w.get('area') else next((x for x in de_pe(S, e['lado']) if x.get('guarda') == e['nome'] and x is not e and dist(x, e) <= 1 and x['reac'] > 0), None)
    if g: g['reac'] -= 1; diz(S, f"  {g['nome']} se põe na frente de {e['nome']}"); e = g
    tiro = w['distancia']; pa, pd = T.POSTURAS[a['postura']], T.POSTURAS[e['postura']]
    if not tiro and not livre and not any(n == a['nome'] for n, _ in e['golpeado']): e['golpeado'].append([a['nome'], bool(w['haste'] and dist(a, e) == 2)])
    bon = w['acerto'] + pa[0] - (T.SEM_FOLEGO if a['fol'] <= 0 else 0) + (T.ABALADO if a['abalado'] else 0)
    bon += sum(T.FERIDAS['braços'][1 if gr else 0] for p, gr in a['feridas'] if p == 'braços')
    bon += sum(T.TEMPO[k].get('tiro' if tiro else 'acerto', 0) for k in S['tempo'] if not (k == 'escuro' and tem(a, 'noturno')))
    if S['lugar'].get('alto') == a['lado']: bon += T.ALTO['tiro' if tiro else 'acerto']
    if tiro and S['lugar'].get('cobertura') == e['lado']: bon += T.COBERTURA
    if entre(S, a, e) and S['lugar'].get('alto') != a['lado'] and not w.get('area'): bon += T.ENTRE
    if w['haste'] and dist(a, e) <= 1: bon += T.HASTE_COLADO
    if tiro and a['fugiu']: bon += T.TIRO_FUGINDO
    esp = _golpe_especial(S, a, w, livre); mb, md = _dos_bichos(S, a, e, w, esp); bon += mb      # o bote e a investida; o que os traços e o tamanho mexem
    df = md + (e['def_fixa'] if w.get('area') or w.get('cru') else defesa_de(S, e)) + pd[1] - (T.SEM_FOLEGO if e['fol'] <= 0 else 0) + (T.CHAO if e['chao'] else 0) + (T.PRESO if e['preso'] else 0) + (T.RESGUARDO if e['resguardo'] else 0)
    df += sum(T.TEMPO[k].get('defesa', 0) for k in S['tempo'])
    df -= T.FLANCO * min(T.FLANCO_MAX, sum(1 for n, _ in e['golpeado'] if n != a['nome']))       # cercado: cada um que já bateu nele abre a guarda para o próximo
    tr = e['partes'].get('tronco')                                                                   # mirar a fresta: só contra armadura melhor que a arma, e só quando compensa
    mira = bool(tr and inteiro(S, tr['item']) and tr['cat'] > w['cat'] and not tem(e, 'couraça') and not w.get('area') and not w.get('cru') and not w.get('magia') and chance(df - bon - T.MIRA_ACERTO) * T.MIRA_PROT > chance(df - bon))
    if mira: bon += T.MIRA_ACERTO
    if w['item'] not in S['usadas']: S['usadas'].append(w['item'])
    for pc in list(e['partes'].values()) + ([e['escudo']] if e['escudo'] else []):
        if pc['item'] not in S['usadas']: S['usadas'].append(pc['item'])
    j = jogada(bon, crit19=bool(w['efeitos'].get('critico_19')))
    cab = f"  {a['nome']} {'sopra em' if w.get('area') else 'atira em' if tiro else 'golpeia'} {e['nome']}" + (f' ({livre})' if livre and not w.get('area') else '') + (f" ({esp['nome']})" if esp else '') + (' mirando a fresta' if mira else '') + (' (no ar)' if not tiro and w['alcance'] < 2 and _no_ar(S, e) else '')
    if (a.get('bicho') or a.get('povo')) and not w.get('area') and not w.get('magia'): a['golpes'] += 1; a['andou_t'] = 0
    if j['falha']:
        diz(S, f"{cab}: dois 1, erra feio"); _gasta(S, a, w, 1); return
    if j['total'] < df and not j['crit']:
        gb, gp = guarda_de(S, e); aparado = not tiro and gb > 0 and df - j['total'] <= gb
        diz(S, f"{cab}: {_n(j['total'])} contra {_n(df)}, {'aparado' if aparado else 'erra'}")
        if aparado and gp['cat'] != w['cat']:                # dois aços se encontram: o pior gasta
            if gp['cat'] > w['cat']: _gasta(S, a, w, 1)
            elif gp is e['escudo']: _gasta_armadura(S, e, gp['nome'], gp['item'], 1)
            else: _gasta(S, e, gp, 1)
        return
    parte = T.ONDE[D.d(10)]; pc = e['partes'].get(parte); vestida = bool(pc and inteiro(S, pc['item']))
    prot = pc['rd'] * (1 if w.get('area') or w.get('cru') or w.get('magia') else T.MATRIZ[w['golpe']][pc['material']]) / (2 if j['crit'] and not tem(e, 'couraça') else 1) if vestida else T.NU
    if mira and vestida and pc['cat'] > w['cat']: prot /= T.MIRA_PROT
    if w.get('magia'): prot = _guarda_m(S, e) / (2 if j['crit'] else 1)                    # A GUARDA contra a magia (a conta da magia, B.1): o amuleto, ou 0,6 da armadura do tronco; sem material, sem parte do corpo, sem fresta
    if e.get('aco') and not _magica(w): prot *= 3 ** e['aco']                              # O AÇO COMUM conta tantas categorias abaixo (o imaterial, o lobisomem)
    dano = int(rola(w['dado'], max(2 if j['crit'] else 1, esp['dados'] if esp else 1)) * T.K_DANO * w['mult'] / prot * w['fmult'])
    if tem(e, 'ossos') and w['golpe'] in ('corte', 'ponta'): dano = int(dano * TC.OSSOS)        # OSSOS: o fio e a ponta passam entre eles
    # o aço gasta o aço
    if dano == 0: _gasta(S, a, w, 1)
    if vestida and not w.get('magia') and (w['cat'] > pc['cat'] or j['crit']): _gasta_armadura(S, e, pc['nome'], pc['item'], 2 if w['cat'] >= pc['cat'] + 2 else 1)
    esc = e['escudo']
    if j['crit'] and esc and inteiro(S, esc['item']) and arma_de(S, e)['maos'] == 1: _gasta_armadura(S, e, esc['nome'], esc['item'], 1)
    e['pv'] -= dano; e['agressor'] = a['nome']
    diz(S, f"{cab}: {_n(j['total'])} contra {_n(df)}{', CRÍTICO' + (' (a couraça não abre)' if tem(e, 'couraça') else '') if j['crit'] else ''}, {_parte(e, parte)}: {dano} ({max(e['pv'], 0)}/{e['pvmax']})" + (' · o aço não passa' if dano == 0 else ''))
    dv = efeito(S, e, 'devolve')
    if not tiro and dv and a['estado'] == 'pe' and not (tem(e, 'ardente') and dist(a, e) > 1):
        a['pv'] -= dv; diz(S, f"    a armadura de {e['nome']} devolve {dv} em {a['nome']} ({max(a['pv'], 0)}/{a['pvmax']})"); S['dano_r'] += dv / a['pvmax']
        if a['pv'] <= 0: _cai(S, a, 0)
    S['ult'] = [e['nome'], dano]
    if dano <= 0: return
    S['dano_r'] += dano / e['pvmax']
    if tem(a, 'dreno') and (w.get('corpo') or w.get('magia')) and a['estado'] == 'pe' and a['pv'] < a['pvmax']:
        g = min(a['pvmax'] - a['pv'], max(1, int(dano * TC.DRENO))); a['pv'] += g; diz(S, f"    {a['nome']} bebe a vida que tirou (+{g}: {a['pv']}/{a['pvmax']})")
    if e.get('prepara') and e['estado'] == 'pe': _concentra(S, e, dano >= e['pvmax'] * T.FERIDA or (j['crit'] and dano >= e['pvmax'] * T.FERIDA_MIN))
    terrivel = dano >= e['pvmax'] * T.FERIDA_GRAVE; abertas = len(e['feridas'])
    if e['pv'] <= 0: _cai(S, e, dano)
    elif dano >= e['pvmax'] * T.FERIDA or (j['crit'] and dano >= e['pvmax'] * T.FERIDA_MIN): _ferida(S, e, parte, terrivel, w, dano)
    if w['efeitos'].get('derruba') and 'derruba' not in a['usou'] and _derruba(S, a, e):
        a['usou'].append('derruba'); e['chao'] = True; diz(S, f"    {e['nome']} vai ao chão")
    if a.get('bicho') or e.get('bicho') or a.get('tracos') or e.get('tracos'): _depois_do_golpe(S, a, e, w, dano, esp, len(e['feridas']) > abertas)
    if e.get('fases') and e['estado'] == 'pe': _fase(S, e)
    if terrivel:
        for o in de_pe(S, e['lado']):
            if o is not e and dist(o, e) <= 2: _moral(S, o, 'golpe_terrivel')
    if e['estado'] == 'pe' and e['pv'] < e['pvmax'] * 0.25: _moral(S, e, 'ferido_grave')


def _golpe_especial(S, a, w, livre):
    """o BOTE (o primeiro golpe do bicho na luta) e a INVESTIDA (o golpe depois de correr): acertam mais, rolam os dados mais vezes e derrubam"""
    if not (a.get('bicho') or a.get('povo')) or w['distancia'] or livre: return None
    if tem(a, 'bote') and 'bote' not in a['usou']:
        a['usou'].append('bote'); return dict(nome='bote', acerto=TB.BOTE['acerto'], dados=TB.BOTE['dados'])
    if tem(a, 'investida') and a['andou_t'] >= TB.INVESTIDA['casas']: return dict(nome='investida', acerto=TB.INVESTIDA['acerto'], dados=TB.INVESTIDA['dados'])
    return None


def _dos_bichos(S, a, e, w, esp):
    """o que os traços, o tamanho e a moral dos bichos mexem neste golpe: (no acerto de quem bate, na Defesa de quem apanha). Entre gente, (0, 0)."""
    bon = esp['acerto'] if esp else 0; df = 0
    if a.get('maldito'): bon += TC.MAU_OLHADO['acerto']
    if e.get('maldito'): df += TC.MAU_OLHADO['defesa']
    if a.get('brado'): bon += TC.BRADO['acerto']
    if a.get('veneno'): bon += TB.VENENO['acerto']
    if _agarrado(S, a): bon += TB.AGARRADO['acerto']
    if _agarrado(S, e): df += TB.AGARRADO['defesa']
    if S['lugar'].get('largura'): bon += _apertado(S, a); df += _apertado(S, e)
    if a.get('encurralado'): bon += TB.ENCURRALADO
    if not w['distancia'] and w['alcance'] < 2 and _no_ar(S, e): bon += TB.VOA
    return bon, df


def _depois_do_golpe(S, a, e, w, dano, esp, abriu):
    """o golpe feriu, e um dos dois é bicho: o bote, a investida e a matilha derrubam, o veneno entra, o que agarra segura, e o bicho ferido testa a coragem"""
    if not e['chao'] and _derruba(S, a, e) and (esp or (tem(a, 'matilha') and w.get('corpo') and sum(1 for n, _ in e['golpeado'] if n != a['nome'] and tem(por_nome(S, n), 'matilha')) >= TB.MATILHA)):
        e['chao'] = True; diz(S, f"    {e['nome']} vai ao chão" + ('' if esp else ' (a matilha derruba)'))
        if esp and esp['nome'] == 'bote': e['atordoado'] = max(e['atordoado'], TB.BOTE['atordoa'])           # pego de surpresa
    if w.get('corpo') and not w.get('area') and e['estado'] == 'pe':
        if tem(a, 'veneno') and not tem(e, 'sem vida'):
            q = max(1, int(dano * TB.VENENO['fracao'])); ant = e['veneno'] or [0, 0]
            e['veneno'] = [max(q, ant[0]), TB.VENENO['rodadas']]; diz(S, f"    o veneno entra em {e['nome']} ({e['veneno'][0]} por rodada)")
        if tem(a, 'agarra') and a['estado'] == 'pe' and dist(a, e) <= 1 and e.get('ocupa', 1) <= a['ocupa'] and not tem(e, 'imaterial') and not w.get('distancia') and not any(o is not e and o['estado'] == 'pe' and _agarrado(S, o) is a for o in S['L']):
            if e.get('agarrado') != a['nome']:
                e['agarrado'] = a['nome']; diz(S, f"    {a['nome']} AGARRA {e['nome']}"); _para(S, e, f"{a['nome']} agarrou {e['nome']}", so_controlado=True)
            if e['nome'] not in a['feriu_t']: a['feriu_t'].append(e['nome'])
    if abriu and e.get('bicho') and e['estado'] == 'pe': _moral(S, e, 'ferido')


def _gasta(S, a, w, n):
    it = S['itens'][w['item']]
    if w['efeitos'].get('nao_quebra') or it['dur'][0] <= 0: return
    it['dur'][0] = max(0, it['dur'][0] - n)
    if it['dur'][0] == 0:
        diz(S, f"    ✖ {w['nome']} de {a['nome']} QUEBRA"); _para(S, a, f"{w['nome']} de {a['nome']} quebrou")
        w.update(acerto=w['acerto'] - T.BON[w['cat']] + T.QUEBRADA, mult=T.MULT[0] * (T.DUAS_MAOS if w['maos'] == 2 and not w['distancia'] else 1), cat=0, efeitos={}, aparo=0, nome=w['nome'] + ' (quebrou)')


def _gasta_armadura(S, e, nome, chave, n):
    it = S['itens'][chave]
    if it['dur'][0] <= 0 or any(src['item'] == chave and src['efeitos'].get('nao_quebra') for src in e['fontes']): return
    it['dur'][0] = max(0, it['dur'][0] - n)
    if it['dur'][0] == 0: diz(S, f"    ✖ {nome} de {e['nome']} se desfaz"); _para(S, e, f"{nome} de {e['nome']} quebrou")


def _ferida(S, e, parte, grave, w, dano):
    e['feridas'].append([parte, grave]); g = 1 if grave else 0; txt = f"    FERIDA{' GRAVE' if grave else ''} em {e['nome']}, {_parte(e, parte)}: "; sangra = (grave or bool(w['efeitos'].get('sangra'))) and not tem(e, 'sem vida')
    if parte == 'cabeça': e['atordoado'] = max(e['atordoado'], T.FERIDAS['cabeça'][g]); txt += f"a cabeça roda (perde {_acoes(e['atordoado'])})"
    elif parte == 'braços':
        txt += f"{T.FERIDAS['braços'][g]:+d} no acerto".replace('-', '−')
        if grave and not e['sem_arma'] and not e.get('bicho'): e['sem_arma'] = True; txt += ' e larga a arma'
    elif parte == 'tronco' and tem(e, 'sem vida'): txt += 'não sente'
    elif parte == 'tronco': e['fol'] = max(0, e['fol'] - T.FERIDAS['tronco'][g]); sangra = True; txt += 'perde o fôlego'
    else:
        firme = bool(efeito(S, e, 'firme'))
        if not firme: e['chao'] = True
        e['preso'] = e['preso'] or grave                    # a perna presa: a pessoa ainda se levanta, mas não sai mais do lugar
        txt += ('a perna cede, mas a peça firme segura de pé' if firme else 'vai ao chão') + ('; com a perna presa, não sai mais do lugar (levantar-se, pode)' if grave else '')
    if sangra:
        n = T.SANGRA_RODADAS[1 if grave or w['efeitos'].get('sangra') else 0]; q = max(1, int(dano * T.SANGRA)); ant = e['sangra'] or [0, 0]
        e['sangra'] = [max(q, ant[0]), max(n, ant[1])]; txt += f' · sangra {e["sangra"][0]} por {e["sangra"][1]} rodadas'
    diz(S, txt); _para(S, e, f"{e['nome']} levou uma ferida ({_parte(e, parte)}{', grave' if grave else ''})", so_controlado=True)


def _cai(S, e, dano):
    macico = dano > e['pvmax'] * 0.5 or tem(e, 'sem vida')
    e['estado'] = 'morto' if macico else 'caido'; e['pv'] = min(e['pv'], 0)
    diz(S, f"    ☠ {e['nome']} MORRE" if macico else f"    ▼ {e['nome']} CAI")
    _para(S, e, f"{e['nome']} {'morreu' if macico else 'caiu'}")
    if e.get('desfaz'): _desfaz(S, e)
    aliados = de_pe(S, e['lado'])
    if e.get('lider'):
        for o in aliados: _moral(S, o, 'lider_caiu')
    if len(aliados) * 2 <= len([f for f in S['L'] if f['lado'] == e['lado']]):
        for o in aliados: _moral(S, o, 'metade_caiu')
    _fim(S)


def _moral(S, f, motivo):
    if f['moral'] == 'firme' or f['estado'] != 'pe' or (motivo in f['testou'] and motivo != 'golpe_terrivel') or f.get('moral_r') == [S['r'], motivo]: return
    if not inimigos(S, f): return                           # sem inimigo de pé não há de quem fugir nem a quem se render: quem ficou com o campo não testa a coragem
    bicho = f.get('bicho') and not f.get('controla')
    if bicho and f['chao'] and not f['preso'] and S['lugar'].get('sem_saida') != f['lado']: return       # o bicho no chão não tem como correr agora: o susto fica para quando ele se levantar
    f['testou'].append(motivo); f['moral_r'] = [S['r'], motivo]
    meus, deles = len(de_pe(S, f['lado'])), len(de_pe(S, outro(f['lado'])))
    ld = lider(S, f['lado']); bon = f['vontade_b'] + f.get('coragem', 0) + (T.MORAL_LIDER if ld and ld['estado'] == 'pe' and ld is not f else 0)
    if tem(f, 'matilha') and any(o is not f and tem(o, 'matilha') for o in de_pe(S, f['lado'])): bon += TB.MATILHA_CORAGEM       # a matilha dá coragem
    bon += T.MORAL_MAIS if meus > deles else T.MORAL_MENOS if deles >= 2 * meus else 0
    if f.get('brado'): bon += TC.BRADO['coragem']
    t = sum(d20x()) + sum(d20x()) + bon; cd = T.MORAL[motivo] if motivo in T.MORAL else TB.PAVOR if motivo == 'pavor' else S['cd_j'][motivo] if motivo in S.get('cd_j', {}) else TB.MORAL[motivo]; que = SUSTOS.get(motivo, motivo.replace('_', ' '))
    if t >= cd: return
    if bicho:       # o BICHO não fica abalado nem se rende: foge. Encurralado (sem saída, ou sem pernas para correr), luta até o fim
        if S['lugar'].get('sem_saida') == f['lado'] or f['preso']:
            if not f.get('encurralado'): f['encurralado'] = True; diz(S, f"    {f['nome']} está ENCURRALAD{_oa(f)}: não tem {'para onde' if not f['preso'] else 'pernas para'} fugir ({que}: {t} contra {cd})")
            return
        f['estado'] = 'fugiu'; diz(S, f"    {f['nome']} FOGE ({que}: {t} contra {cd})"); _para(S, f, f"{f['nome']} fugiu")
        if not _no_ar(S, f): _golpe_livre(S, f, 'pelas costas')      # quem voa sai por cima
        if _nao_saiu(S, f): return
        if f.get('lider'):
            for o in de_pe(S, f['lado']): _moral(S, o, 'lider_caiu')
        _fim(S); return
    if f.get('controla'):       # quem o jogador comanda não foge nem se rende pelo dado: fica abalado, e a escolha é do jogador
        f['abalado'] = True; diz(S, f"    {f['nome']} FRAQUEJA ({que}: {t} contra {cd})"); _para(S, f, f"{f['nome']} fraquejou ({que}): seguir lutando assim, recuar ou render-se é escolha sua"); return
    if t > cd - T.MORAL_QUEBRA and not f['abalado']:
        f['abalado'] = True; diz(S, f"    {f['nome']} FRAQUEJA ({que}: {t} contra {cd})"); return
    rende = f['pv'] < f['pvmax'] * 0.25 or S['lugar'].get('sem_saida') == f['lado']
    if rende and inimigos(S, f) and all(o.get('bicho') for o in inimigos(S, f)):       # ninguém se rende a um bicho: foge, se tem por onde
        if S['lugar'].get('sem_saida') == f['lado']:
            f['abalado'] = True; diz(S, f"    {f['nome']} não tem a quem se render nem por onde fugir ({que}: {t} contra {cd})"); return
        rende = False
    f['estado'] = 'rendido' if rende else 'fugiu'
    diz(S, f"    {f['nome']} {'SE RENDE' if rende else 'FOGE'} ({que}: {t} contra {cd})")
    _para(S, f, f"{f['nome']} {'se rendeu' if rende else 'fugiu'}")
    if not rende: _golpe_livre(S, f, 'pelas costas')
    if not rende and _nao_saiu(S, f): return
    if f.get('lider'):
        for o in de_pe(S, f['lado']): _moral(S, o, 'lider_caiu')
    _fim(S)


def _nao_saiu(S, f):
    """quem fugia e levou, de costas, o golpe que o pôs no chão (ou lhe prendeu a perna) NÃO SAIU: segue na luta, onde caiu. Devolve True se foi assim."""
    if f['estado'] != 'fugiu' or not (f['chao'] or f['preso']): return False
    f['estado'] = 'pe'; txt = f"{f['nome']} fugiu"
    if txt in S['paradas']: S['paradas'].remove(txt)
    if f['preso'] and f.get('bicho') and not f.get('controla'): f['encurralado'] = True
    diz(S, f"    {f['nome']} NÃO SAI: o golpe {'prendeu-lhe a perna' if f['preso'] else 'pôs no chão quem fugia'}" + (f" (ENCURRALAD{_oa(f)}: luta até o fim)" if f.get('encurralado') else ''))
    return True


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
def _passo(S, f=None):
    if f is not None and _no_ar(S, f): return T.PASSO          # quem voa não pisa na lama nem na água
    return min([T.PASSO] + [T.TEMPO[k]['passo'] for k in S['tempo'] if 'passo' in T.TEMPO[k]])


def _ordem_de(S, a):
    """a ordem que vale para este lutador agora (a dele, se o jogador o comanda; a do grupo, se é do lado A e não guarda ninguém)"""
    if a.get('controla'): return (S['ordens'].get(a['nome']) or {}).get('acao')
    return S['ordens'].get('grupo') if a['lado'] == 'A' and a['papel'] != 'guarda' else None


def _fica(S, a):
    """este aliado não vai para a frente: num corredor, quem vem atrás pode trocar de lugar com ele"""
    if a['chao'] or _nao_anda(S, a) or a['fol'] <= 0 or arma_de(S, a)['distancia']: return True
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
        if (larg and not tem(f, 'imaterial')) or not avanca: return ''
        if _no_ar(S, f) or tem(f, 'imaterial'): return 'contorna'                      # quem voa passa por cima da linha
        colados = [a for a in de_pe(S, f['lado']) if a is not f and any(dist(a, e) <= 1 for e in la)]
        return 'contorna' if len(colados) >= T.SEGURA * len(la) else ''
    if larg:
        meus = [a for a in de_pe(S, f['lado']) if a['x'] == nx and a is not f]      # a casa está cheia? (cada um toma o seu tanto; o bicho grande demais cabe sozinho, apertado)
        if meus and sum(a.get('ocupa', 1) for a in meus) + f.get('ocupa', 1) > larg: return 'troca' if any(_troca(S, f, a, avanca) for a in meus) else ''
    return 'sim'


def _troca(S, f, a, avanca):
    """f pode trocar de lugar com o aliado a? (a não vai para onde f vai, os dois tomam o mesmo tanto do corredor, e ninguém tira do lugar quem o bicho agarrou)"""
    return _fica(S, a) == avanca and a.get('ocupa', 1) == f.get('ocupa', 1) and not _agarrado(S, a)


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
    avanca = not recuo; passo = _passo(S, f)
    if avanca and dx == frente(f) and S['lugar'].get('alto') == outro(f['lado']) and not _no_ar(S, f): passo = 1       # subindo
    if not _livre(S, f, f['x'] + dx, avanca): return 0
    colados = [e for e in inimigos(S, f) if dist(f, e) <= 1 and abs(e['x'] - (f['x'] + dx)) > dist(f, e)]
    if avanca: colados = [e for e in colados if len([a for a in de_pe(S, f['lado']) if a is not f and dist(a, e) <= 1]) < T.SEGURA]
    if colados and not _no_ar(S, f) and not tem(f, 'imaterial'):                            # quem voa sai por cima: não dá as costas a ninguém
        if recuo: f['fugiu'] = True
        _golpe_livre(S, f, 'no recuo' if recuo else 'pelo flanco', quem=colados)
    andou = 0
    for _ in range(passo):
        if f['estado'] != 'pe' or f['chao'] or _nao_anda(S, f): break      # o golpe que o pegou no caminho o parou
        nx = f['x'] + dx; como = _livre(S, f, nx, avanca)
        if not como: break
        al = alvos(S, f, arma_de(S, f))
        if avanca and como == 'sim' and (any(x[0] is ate for x in al) if ate else al): break    # já alcança: para aqui
        if como == 'troca':
            o = next(a for a in de_pe(S, f['lado']) if a['x'] == nx and a is not f and _troca(S, f, a, avanca))
            o['x'] = f['x']; diz(S, f"  {f['nome']} troca de lugar com {o['nome']}")
        elif como == 'contorna': diz(S, f"  {f['nome']} contorna a linha")
        de = f['x']; f['x'] = nx; andou += 1
        if avanca: _golpe_livre(S, f, 'o alcance bate primeiro', vinha_de=de)
        if como != 'sim': break
    return andou


def _decide(S, f, pagou):
    """o que este lutador faz com a ação: ('golpe', alvo) · ('anda', lado, recuo?, até quem) · ('folego',) · ('levanta',) · ('pega',) · ('recarrega',) · ('espera',) · ('sopro',)"""
    w = arma_de(S, f); o = S['ordens'].get(f['nome']) or {}
    if not f.get('controla'): o = dict(acao=_ordem_de(S, f)) if _ordem_de(S, f) else {}
    acao = o.get('acao', 'atacar'); f['postura'] = o.get('postura', f['postura'] if f.get('controla') else 'firme')
    custo = w['folego'] + (0 if pagou else _peso(S, f))
    if acao == 'folego' and f['fol'] >= f['folmax']:        # A ORDEM DE TOMAR FÔLEGO ACABA QUANDO O FÔLEGO ENCHE: daí em diante segura (bate em quem chega), e a luta para e pergunta
        acao = 'segurar'; (S['ordens'].get(f['nome']) or {}).update(acao='segurar')
        _para(S, f, f"{f['nome']} recuperou o fôlego ({f['fol']}/{f['folmax']}): a ordem de tomar fôlego acabou, e agora segura até nova ordem", so_controlado=True)
    if acao == 'folego' or f['fol'] < min(custo, f['folmax']): return ('folego',)
    if f['chao']: return ('levanta',)
    if f.get('artes'):
        x = _arte(S, f)
        if x: return ('arte', x)
    if f.get('fica') and f['fase'] < 1 and not any(dist(f, e) <= f['fica'] for e in inimigos(S, f)) and len(de_pe(S, f['lado'])) * 2 > len([x for x in S['L'] if x['lado'] == f['lado']]): return ('espera',)
    colado = any(dist(f, e) <= 1 for e in inimigos(S, f))
    if f['sem_arma'] and not colado: return ('pega',)
    preso = _nao_anda(S, f)                                     # a perna que não anda mais, ou o bicho que o agarra
    tras = -frente(f); pode_recuar = not preso and bool(_livre(S, f, f['x'] + tras, False))
    if acao == 'recuar':                                    # A RETIRADA: quem recua ANDA PARA TRÁS enquanto houver inimigo de pé a menos de RETIRADA casas (a 8 de todos, no fim da rodada, saiu da luta)
        if min([dist(f, e) for e in inimigos(S, f)] or [T.RETIRADA]) < T.RETIRADA and pode_recuar: return ('anda', tras, True, None)
        acao = 'atacar' if colado else 'segurar'            # longe o bastante, segura; encurralado, luta
    if w['distancia'] and f['recarga'] > 0: return ('recarrega',)
    if not f.get('controla') and f['arma']['distancia'] and not f['sem_arma'] and colado and pode_recuar and not f['fugiu']: return ('anda', tras, True, None)   # o atirador se afasta de quem colou
    al = alvos(S, f, w); nome = o.get('alvo'); pref = next((x for x in inimigos(S, f) if x['nome'] == nome), None) if nome else None
    if nome and not pref:
        if f.get('controla'): _para(S, f, f"o alvo de {f['nome']} ({nome}) não está mais de pé")
        o['alvo'] = None
    if f.get('bicho') and not pref: pref = next((x[0] for x in al if _agarrado(S, x[0]) is f), None)      # o bicho não larga quem agarrou
    if f.get('sopro') and f['sopro_r'] <= 0 and f['fol'] >= f['sopro']['folego']:              # o SOPRO: quando pega dois ou mais, ou quando não alcança ninguém de outro jeito
        n = len(_no_sopro(S, f))
        if n >= 2 or (n == 1 and not al): return ('sopro',)
    if pref and not any(x[0] is pref for x in al) and not preso:      # o alvo da ordem está fora de alcance: vai até ele
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
        if not preso and _livre(S, f, f['x'] + s, True): return ('anda', s, False, None)     # sem caminho até o guardado, luta como soldado
    if preso: return ('espera',)
    if acao == 'segurar':
        apanha = any(arma_de(S, e)['distancia'] or dist(e, f) <= max(1, arma_de(S, e)['alcance']) for e in inimigos(S, f))
        if not apanha: return ('espera',)
        if f.get('controla'):
            _para(S, f, f"{f['nome']} está ao alcance deles e não alcança ninguém: segurar assim é só apanhar"); return ('espera',)
    dx = _rumo(S, f, w)
    return ('anda', dx, False, None) if dx else ('espera',)


def _peso(S, f):
    """o fôlego que a armadura cobra numa rodada em que a pessoa se mexe (o couro do bicho é o corpo dele: não pesa nem esquenta)"""
    return f['fol_rodada'] + sum(T.TEMPO[k].get('folego', 0) for k in S['tempo']) + (sum(T.TEMPO[k].get('folego_armadura', 0) for k in S['tempo']) if not f.get('bicho') and any(p['material'] != 'couro' for p in f['partes'].values()) else 0)


def _no_sopro(S, f):
    """os inimigos de pé que o sopro deste bicho pega agora"""
    alc = min([f['sopro']['alcance']] + [T.TEMPO[k]['sem_tiro_longe'] for k in S['tempo'] if 'sem_tiro_longe' in T.TEMPO[k]])       # o tempo vale como num tiro
    return [e for e in inimigos(S, f) if dist(f, e) <= alc]


def _turno_do_bicho(S, f, fim=False):
    """o que só o bicho faz no começo e no fim do turno dele: a carne que fecha, o sopro que volta, a presa que ele solta"""
    if fim:
        for v in S['L']:
            if v.get('agarrado') == f['nome'] and v['nome'] not in f['feriu_t']: v['agarrado'] = None; diz(S, f"  {f['nome']} solta {v['nome']}")
        return
    f['feriu_t'] = []
    if f['sopro_r'] > 0: f['sopro_r'] -= 1
    if tem(f, 'regenera') and f['pv'] < f['pvmax']:
        g = min(f['pvmax'] - f['pv'], max(1, int(f['pvmax'] * TB.REGENERA))); f['pv'] += g; S['dano_r'] -= g / f['pvmax']
        diz(S, f"  {f['nome']} regenera (+{g}: {f['pv']}/{f['pvmax']})")


def _diz_passo(S, txt, i0):
    """a linha do passo entra no registro ANTES do golpe que o alcance deu no caminho (o passo veio primeiro, e foi ao entrar no alcance que ele apanhou):
    assim ninguém aparece avançando depois de cair ou de morrer. Só a ordem das linhas muda; nenhum dado é rolado aqui."""
    if S['quieto']: return
    pos = next((i for i in range(i0, len(S['log'])) if '(o alcance bate primeiro)' in S['log'][i]), len(S['log']))
    S['log'].insert(pos, TB.contrai(txt))


def _turno(S, f):
    f['resguardo'] = False; f['reac'] = f['reacoes']; f['fugiu'] = False
    zerado = f['fol'] <= 0                                     # começou o turno sem fôlego: uma ação só
    f['fol'] = min(f['folmax'], f['fol'] + 1 + T.POSTURAS[f['postura']][2])
    custos = [1] if zerado else [1] * T.ACOES + ([] if tem(f, 'sem vida') else list(f['esforcos']))
    if f.get('bicho'): _turno_do_bicho(S, f)
    _comeco_j(S, f)
    if f['atordoado']:
        perde = min(len(custos), f['atordoado']); custos = custos[perde:]; f['atordoado'] = 0; diz(S, f"  {f['nome']} ainda sente o golpe: perde {_acoes(perde)}")
    pagou = False; feitas = 0
    for mult in custos:
        if f['estado'] != 'pe' or S['fim']: break
        if f.get('prepara') and feitas == 0 and not f['chao']: ac = ('arte', next(x for x in f['artes'] if x['nome'] == f['prepara']), True)
        else: f['feitas_t'] = feitas; ac = _decide(S, f, pagou)
        w = arma_de(S, f)
        if feitas >= T.ACOES:                                  # a ação A MAIS (o esforço): só para golpear, e guardando um terço do fôlego (a postura agressiva gasta tudo)
            if ac[0] != 'golpe' or f['postura'] == 'defensiva': break
            if f['fol'] - w['folego'] * mult < (0 if f['postura'] == 'agressiva' else f['folmax'] // 3): break
        feitas += 1
        if ac[0] in ('golpe', 'anda', 'sopro') and not pagou: pagou = True; f['fol'] -= _peso(S, f)
        if ac[0] == 'folego':
            g = rola(T.TOMA_FOLEGO[0]) + T.TOMA_FOLEGO[1]; tinha = max(f['fol'], 0); f['fol'] = min(f['folmax'], tinha + g); f['resguardo'] = True
            diz(S, f"  {f['nome']} toma fôlego (+{f['fol'] - tinha}: {f['fol']}/{f['folmax']})" if f['fol'] > tinha else f"  {f['nome']} se resguarda (o fôlego já está cheio: {f['fol']}/{f['folmax']})")
        elif ac[0] == 'levanta': f['chao'] = False; diz(S, f"  {f['nome']} se levanta" + (' (com a perna presa: não sai do lugar)' if f['preso'] else ''))
        elif ac[0] == 'pega': f['sem_arma'] = False; diz(S, f"  {f['nome']} apanha a arma")
        elif ac[0] == 'recarrega': f['recarga'] -= 1
        elif ac[0] == 'espera': f['resguardo'] = True; break
        elif ac[0] == 'anda':
            i0 = len(S['log']); k = _anda(S, f, ac[1], recuo=ac[2], ate=ac[3])
            if not k: f['resguardo'] = True; break
            f['fol'] -= mult; _diz_passo(S, f"  {f['nome']} {'recua' if ac[2] else 'avança'} ({k} casa{'s' if k > 1 else ''})", i0)
            if f.get('bicho') and not ac[2]: f['andou_t'] += k               # a investida conta as casas corridas desde o último golpe
        elif ac[0] == 'arte':
            _faz_arte(S, f, ac[1], agora=len(ac) > 2)
            if len(ac) <= 2 and (ac[1].get('acoes', 1) >= 2 or ac[1].get('prepara')): _fim(S); break
        elif ac[0] == 'golpe':
            golpe(S, f, ac[1], w); f['fol'] -= w['folego'] * mult; f['recarga'] = w['recarga'] if w['distancia'] else 0
        elif ac[0] == 'sopro':
            ws = f['sopro']; f['fol'] -= ws['folego'] * mult; f['sopro_r'] = f.get('sopro_rec', TB.SOPRO['recarga']); diz(S, f"  {f['nome']} SOPRA")
            for e in _no_sopro(S, f):
                if f['estado'] == 'pe' and e['estado'] == 'pe': golpe(S, f, e, ws, livre='o sopro')
        _fim(S)
    if f.get('bicho'): _turno_do_bicho(S, f, fim=True)
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
    if S['r'] == 1:                                         # o que APAVORA: quem começa a luta contra ele testa a coragem
        for lado in 'AB':
            if any(tem(b, 'apavora') for b in de_pe(S, lado)):
                for o in de_pe(S, outro(lado)): _moral(S, o, 'pavor')
    vivos = de_pe(S)
    for f in S['L']: f['golpeado'] = []
    for f in vivos: f['ini'] = sum(d20x()) + sum(d20x()) + f['percep_b'] + f['agil_b'] + f['ini_mod'] + (TB.BOTE['ini'] if S['r'] == 1 and tem(f, 'bote') else 0)
    S['fila'] = [f['nome'] for f in sorted(vivos, key=lambda f: -f['ini'])]


def _fecha_rodada(S):
    if S['fechada'] == S['r']: return
    S['fechada'] = S['r']
    for f in S['L']:                                        # o sangue e a vida por um fio
        if f['estado'] == 'pe' and f['sangra']:
            q = f['sangra'][0]; f['pv'] -= q; f['sangra'][1] -= 1; S['dano_r'] += q / f['pvmax']
            if f['sangra'][1] <= 0: f['sangra'] = None
            diz(S, f"  {f['nome']} sangra {q} ({max(f['pv'], 0)}/{f['pvmax']})")       # o que o sangue tira fica escrito: a conta dos golpes fecha com o quadro
            if f['pv'] <= 0: diz(S, f"  {f['nome']} sangra até cair"); _cai(S, f, 0)
        elif f['estado'] == 'caido' and max(f['morte']) < 3:
            ok = D.d(20) >= T.MORTE_CD; f['morte'][0 if ok else 1] += 1
            if f['morte'][1] >= 3: f['estado'] = 'morto'; diz(S, f"  ☠ {f['nome']} morre no chão"); _para(S, f, f"{f['nome']} morreu no chão")
    for f in S['L']:                                        # o veneno
        if f['estado'] == 'pe' and f.get('veneno'):
            q = f['veneno'][0]; f['pv'] -= q; f['veneno'][1] -= 1; S['dano_r'] += q / f['pvmax']
            if f['veneno'][1] <= 0: f['veneno'] = None
            diz(S, f"  {f['nome']} perde {q} para o veneno ({max(f['pv'], 0)}/{f['pvmax']})")      # como o sangue: o que o veneno tira fica escrito
            if f['pv'] <= 0: diz(S, f"  {f['nome']} cai pelo veneno"); _cai(S, f, 0)
    for f in de_pe(S):                                      # a retirada: quem recua e ficou longe de todo inimigo de pé saiu da luta
        ini = inimigos(S, f)                                # SEM INIMIGO DE PÉ NÃO HÁ RETIRADA: a luta acabou, e quem recuava ficou com o campo como os outros
        if _ordem_de(S, f) == 'recuar' and ini and not S['fim'] and all(dist(f, e) >= T.RETIRADA for e in ini):
            f['estado'] = 'saiu'; diz(S, f"  {f['nome']} SAI DA LUTA"); _para(S, f, f"{f['nome']} saiu da luta")
    _fim(S)
    S['sem_dano'] = 0 if S['dano_r'] >= T.IMPASSE_MIN else S['sem_dano'] + 1
    if S['sem_dano'] >= T.IMPASSE and not S['fim']:
        S['fim'] = 'impasse'; diz(S, f"  IMPASSE: {T.IMPASSE} rodadas em que ninguém feriu ninguém de verdade. Os dois lados se separam.")
    if S.get('escuro_r'):
        S['escuro_r'] -= 1
        if S['escuro_r'] <= 0 and 'escuro' in S['tempo']: S['tempo'].remove('escuro'); diz(S, '  o escuro chamado se desfaz')
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
        if f['estado'] == 'pe' and f.get('veneno'):         # o veneno que sobra corre depois da luta: deixa por um fio, mas sozinho não mata
            q = min(f['pv'] - 1, f['veneno'][0] * f['veneno'][1]); f['veneno'] = None
            if q > 0: f['pv'] -= q; diz(S, f"  {f['nome']} ainda perde {q} para o veneno depois da luta ({f['pv']}/{f['pvmax']})")
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
                feridas={f['nome']: f['feridas'][f.get('feridas_antes', 0):] for f in S['L'] if f['feridas'][f.get('feridas_antes', 0):]},      # só as feridas abertas NESTA luta (a que a pessoa já trazia não é notícia do fim)
                quebradas=[it.get('nome', k) for k, it in S['itens'].items() if it['dur'][0] <= 0 and it.get('nome') != 'as mãos'])


def resultado_diz(S):
    """o fim da luta numa linha, para a mesa (o resultado() é o mesmo, em registro, para os scripts)"""
    R = resultado(S); quem = dict(A='a casa fica com o campo', B='o outro lado fica com o campo', impasse='impasse: os dois lados se separam', empate='empate: ninguém fica com o campo').get(R['vencedor'], str(R['vencedor']))
    L = [f"{quem}, em {R['rodadas']} rodada{'s' if R['rodadas'] != 1 else ''}"]
    for k, nome in (('mortos', 'morreram'), ('caidos', 'caíram'), ('fugiram', 'fugiram'), ('sairam', 'saíram da luta'), ('presos', 'renderam-se')):
        if R[k]: L.append(f"{nome}: {', '.join(R[k])}")
    if R['feridas']: L.append('feridas: ' + '; '.join(f"{n} ({' e '.join(_parte(por_nome(S, n) or {}, p) + (', grave' if g else '') for p, g in fs)})" for n, fs in R['feridas'].items()))
    if R['quebradas']: L.append('peças quebradas: ' + ', '.join(R['quebradas']))
    return ' · '.join(L)


def situacao(S):
    """o quadro que o jogador vê quando a luta para"""
    lado = dict(A='a casa', B='o outro lado'); lg = S['lugar'] or {}
    lugar = [x for x in ([f"corredor de {lg['largura']}" if lg.get('largura') else ''] + [f"{lado.get(lg[k], lg[k])} {txt}" for k, txt in (('alto', 'no alto'), ('cobertura', 'com cobertura'), ('sem_saida', 'sem saída')) if lg.get(k)]) if x]
    lugar += [f'{k}: {v}' for k, v in lg.items() if k not in ('largura', 'alto', 'cobertura', 'sem_saida')]
    L = [f"RODADA {S['r']} · " + ' · '.join(S['tempo'] or ['tempo limpo']) + (f" · lugar: {', '.join(lugar)}" if lugar else '')]
    for lado, nome in (('A', 'A CASA'), ('B', 'O OUTRO LADO')):
        L.append(nome + ':')
        for f in S['L']:
            if f['lado'] != lado: continue
            oa = _oa(f); est = dict(pe='no chão' if f['chao'] else 'de pé', caido='CAIU', morto='MORREU', fugiu='fugiu', rendido='rendeu-se', saiu='saiu')[f['estado']]
            fer = ', '.join(_parte(f, p) + (' (grave)' if g else '') for p, g in f['feridas'])
            L.append(f"  {f['nome']:<22} {est:<8} PV {max(f['pv'], 0):>4}/{f['pvmax']:<4} fôlego {max(f['fol'], 0):>2}/{f['folmax']:<2} casa {f['x']:>3}"
                     + (f" · feridas: {fer}" if fer else '') + (f" · sangrando ({f['sangra'][0]} por rodada)" if f['sangra'] and f['estado'] == 'pe' else '')
                     + (' · fraquejou' if f['abalado'] else '') + (' · no chão' if f['chao'] and f['estado'] != 'pe' else '') + (' · sem a arma' if f['sem_arma'] else '') + (' · perna presa: não sai do lugar' if f['preso'] and f['estado'] == 'pe' else '')
                     + (f" · com veneno ({f['veneno'][0]} por rodada)" if f.get('veneno') and f['estado'] == 'pe' else '') + (f" · {f['agarrado']} não solta" if f['estado'] == 'pe' and _agarrado(S, f) else '')
                     + (f" · bicho {f['tamanho']}" + (', no ar' if f['estado'] == 'pe' and _no_ar(S, f) else '') + (', encurralad' + oa.lower() if f.get('encurralado') else '') if f.get('bicho') else ''))
    if S['r'] == 0 and S['avisos']: L.append('AVISOS: ' + ' · '.join(S['avisos']))
    if S['paradas']: L.append('PAROU PORQUE: ' + ' · '.join(S['paradas']))
    return '\n'.join(L)


# =====================================================================================================================
# PARTE J (RASCUNHO): o que as criaturas novas pedem da luta. Tudo daqui para baixo é novo.
# =====================================================================================================================
def _estado_j(f):
    """o estado novo de cada lutador (o que os traços novos e as artes dos chefes mexem)"""
    f.update(raiz=0, maldito=False, brado=0, arte_r={}, fase=0, prepara=None, arte_t=0, erguido=False, levantado=False, calejo=0, feitas_t=0)
    f.setdefault('tracos', []); f.setdefault('mana', 0); f.setdefault('artes', []); f.setdefault('fases', [])
    if 'sem vida' in f['tracos']: f['moral'] = 'firme'


def _magica(w):
    """esta arma fere inteiro quem o aço comum mal toca? (GANCHO: a prata é do ofício; a bênção e o encanto são da magia)"""
    return bool(w.get('magia') or w.get('area') or any(w['efeitos'].get(k) for k in ('prata', 'benta', 'encantada')))


def _comeco_j(S, f):
    """o começo do turno de cada um: o que tem prazo anda, quem não tem vida não cansa, a Mana volta devagar"""
    if f['raiz'] > 0:
        f['raiz'] -= 1
        if f['raiz'] == 0: diz(S, f"  {f['nome']} se solta")
    if f['brado'] > 0: f['brado'] -= 1
    for k in list(f['arte_r']):
        if f['arte_r'][k] > 0: f['arte_r'][k] -= 1
    if tem(f, 'sem vida'): f['fol'] = f['folmax']
    if f.get('manamax'): f['mana'] = min(f['manamax'], f['mana'] + TC.MANA_VOLTA)
    if tem(f, 'regenera') and not f.get('bicho') and f['pv'] < f['pvmax']:
        g = min(f['pvmax'] - f['pv'], max(1, int(f['pvmax'] * TB.REGENERA))); f['pv'] += g; S['dano_r'] -= g / f['pvmax']; diz(S, f"  {f['nome']} regenera (+{g}: {f['pv']}/{f['pvmax']})")
    if f.get('prepara') and (f['chao'] or f['atordoado'] or _agarrado(S, f)): _corta(S, f)
    if f.get('fases'): _fase(S, f)


def _guarda_m(S, e):
    """a guarda contra a magia: o valor do amuleto, ou 0,6 do valor da armadura do tronco (o couro do bicho também), o que for maior; sem um nem outro, um terço"""
    tr = e['partes'].get('tronco'); g = T.NU
    if tr and inteiro(S, tr['item']): g = T.RD[tr['cat']] * (1 if tem(e, 'resiste') else TC.GUARDA_ARMADURA)
    if e.get('amuleto') is not None: g = max(g, T.RD[e['amuleto']])
    return g


def _concentra(S, e, ferida):
    """quem canaliza um feitiço longo e leva dano testa a concentração: 2d20 + Vontade ÷ 10 + maestria contra 28 (32 se o golpe abriu ferida)"""
    S['conc_t'] = S.get('conc_t', 0) + 1
    if sum(d20x()) + sum(d20x()) + e['vontade_b'] + e['maestria'] < TC.CONCENTRA + (TC.CONCENTRA_FERIDA if ferida else 0): _corta(S, e)


def _corta(S, e):
    diz(S, f"    a arte de {e['nome']} ({e['prepara']}) foi CORTADA"); e['arte_r'][e['prepara']] = 2; e['prepara'] = None; S['cortadas'] = S.get('cortadas', 0) + 1


def _resiste(S, a, e):
    """GANCHO (a conta é dos projetistas da magia): a arte que prende, amaldiçoa ou assusta testa a Conjuração de quem lança contra a Firmeza do alvo"""
    pega = sum(d20x()) + sum(d20x()) + a['conj'] + (TC.MAU_OLHADO['acerto'] if a.get('maldito') else 0) >= e.get('firmeza', 26) + TC.CALEJO * e.get('calejo', 0)
    S['f_tentou'] = S.get('f_tentou', 0) + 1; S['f_pegou'] = S.get('f_pegou', 0) + pega
    if pega: e['calejo'] = e.get('calejo', 0) + 1
    return pega


def _caidos_j(S, f, a):
    """os corpos que este chefe pode erguer agora"""
    if a.get('so_seus'): return [o for o in S['L'] if o['lado'] == f['lado'] and o['estado'] == 'morto' and tem(o, 'sem vida') and not o['erguido'] and o is not f]
    return [o for o in S['L'] if o['estado'] in ('morto', 'caido') and not o['erguido'] and not tem(o, 'imaterial') and o is not f and not o.get('chefe')]


def _arte(S, f):
    """a arte que o chefe faz agora: a primeira da lista (a ordem é a preferência dele) que está pronta e tem condição. Uma por turno."""
    if f['arte_t'] == S['r'] or f['prepara']: return None
    meus = [o for o in de_pe(S, f['lado']) if o is not f]
    for a in f['artes']:
        if f['arte_r'].get(a['nome'], 0) > 0 or f['mana'] < a.get('mana', 0): continue
        if a.get('usos') is not None and f['usou'].count('arte:' + a['nome']) >= a['usos']: continue
        if f['fase'] < a.get('fase', 0) or f['fase'] > a.get('ate_fase', 9): continue
        if (a.get('acoes', 1) >= 2 or a.get('prepara')) and f.get('feitas_t', 0) > 0: continue
        al = [e for e in inimigos(S, f) if dist(f, e) <= a.get('alcance', 6)]; q = a.get('quando', 'sempre')
        if a['tipo'] == 'maldiz' and all(e['maldito'] for e in al): continue
        if a['tipo'] == 'prende' and not a.get('area') and all(e['raiz'] > 0 for e in al): continue
        if (q == 'sempre' and al) or (q == 'dois' and len(al) >= 2) or (q == 'comeco' and S['r'] <= 1) or (q == 'caidos' and len(_caidos_j(S, f, a)) >= a.get('pelo_menos', 1)) \
           or (q == 'livre' and al and not any(dist(f, e) <= 1 for e in inimigos(S, f))) or (q == 'poucos' and len(meus) < a.get('menos_de', 2)) or (q == 'ferido' and any(o['pv'] < o['pvmax'] * 0.5 for o in meus + [f])) or (q == 'meus' and meus and al): return a
    return None


def _entra(S, p, lado, x):
    """alguém entra na luta já começada (o chamado, o morto erguido)"""
    n = 1; base = p['nome']
    while por_nome(S, p['nome']): n += 1; p['nome'] = f'{base} ({n})'
    f = ficha(p); f['lado'] = lado
    f.update(x=x, estado='pe', feridas=[], sangra=None, atordoado=0, chao=False, preso=False, abalado=False, reac=f['reacoes'], postura='firme',
             usou=[], testou=[], morte=[0, 0], agressor=None, recarga=0, sem_arma=False, resguardo=False, fugiu=False, golpeado=[], ini=0, pv_visto=f['pv'],
             veneno=None, agarrado=None, encurralado=False, golpes=0, andou_t=0, feriu_t=[], sopro_r=0)
    f.setdefault('moral', 'testa'); f.setdefault('papel', 'frente'); _estado_j(f); f['feridas'] = f.pop('feridas0'); f['feridas_antes'] = 0
    for w in [f['arma'], f['arma2'], f['punho']] + f.get('armas_corpo', []) + [f.get('sopro'), f.get('tiro')] + list(f.get('arma_arte', {}).values()):
        if w: w['item'] = _guarda_item(S, w['item'])
    for pc in f['partes'].values(): pc['item'] = _guarda_item(S, pc['item'])
    for src in f['fontes']: src['item'] = _guarda_item(S, src['item'])
    if f['escudo']: f['escudo']['item'] = _guarda_item(S, f['escudo']['item'])
    S['L'].append(f)
    return f


def _faz_arte(S, f, a, agora=False):
    """o chefe faz a arte. A que se ANUNCIA (prepara) só sai no turno seguinte: a luta para e pergunta, e quem o ferir antes a corta."""
    if a.get('mana') and not agora:
        col = [e for e in inimigos(S, f) if dist(f, e) <= 1]
        if col: _golpe_livre(S, f, 'lança com inimigo colado', quem=col)
        if f['estado'] != 'pe': return
    if a.get('prepara') and not agora:
        f['prepara'] = a['nome']; f['arte_t'] = S['r']; f['mana'] -= a.get('mana', 0)
        diz(S, f"  {f['nome']} COMEÇA: {a['nome']}"); _para(S, f, f"{f['nome']} começou {a['nome']}: sai no próximo turno, se ninguém o ferir antes"); S['anunciadas'] = S.get('anunciadas', 0) + 1; return
    f['prepara'] = None; f['arte_t'] = S['r']; f['arte_r'][a['nome']] = a.get('recarga', 1) + 1; f['usou'].append('arte:' + a['nome'])
    if not a.get('prepara'): f['mana'] -= a.get('mana', 0)
    t = a['tipo']; al = [e for e in inimigos(S, f) if dist(f, e) <= a.get('alcance', 6)]; meus = de_pe(S, f['lado'])
    cand = [e for e in al if not (t == 'maldiz' and e['maldito']) and not (t == 'prende' and e['raiz'] > 0)]
    um = [max(cand, key=lambda e: (e['nome'] == f['agressor'], -e['pv'] / e['pvmax']))] if cand else []
    diz(S, f"  {f['nome']}: {a['nome'].upper()}"); S['artes_n'] = S.get('artes_n', 0) + 1
    if t == 'ataque':
        w = f['arma_arte'][a['nome']]
        if a.get('casa') and al: xs = max({e['x'] for e in al}, key=lambda x: sum(1 for e in al if e['x'] == x)); al = [e for e in al if e['x'] == xs][:a['casa']]
        for e in (al if a.get('area') else um):
            if f['estado'] != 'pe' or e['estado'] != 'pe': continue
            golpe(S, f, e, w, livre=a['nome']); v = S.get('ult')
            if v and v[1] > 0: _rider(S, f, por_nome(S, v[0]), a, v[1])
    elif t == 'grito':
        S.setdefault('cd_j', {})['grito ' + a['nome']] = a['cd']
        for e in (um if a.get('um') else al):
            if a.get('contra') == 'F' and not _resiste(S, f, e): diz(S, f"    {e['nome']} resiste"); continue
            _moral(S, e, 'grito ' + a['nome'])
    elif t == 'brado':
        for o in meus: o['brado'] = TC.BRADO['rodadas'] + 1; o['abalado'] = False
    elif t in ('maldiz', 'prende'):
        for e in (al if a.get('area') else um):
            if not _resiste(S, f, e): diz(S, f"    {e['nome']} resiste"); continue
            if t == 'maldiz': e['maldito'] = True; diz(S, f"    {e['nome']} está AMALDIÇOADO ({TC.MAU_OLHADO['acerto']} no acerto e na Defesa)".replace('-', '−')); _para(S, e, f"{e['nome']} foi amaldiçoado", so_controlado=True)
            elif not tem(e, 'imaterial') and not _no_ar(S, e): e['raiz'] = a.get('rodadas', 2); diz(S, f"    {e['nome']} está PRESO ao chão por {e['raiz']} rodadas"); _para(S, e, f"{e['nome']} está preso ao chão", so_controlado=True)
    elif t == 'atordoa':
        for e in um:
            if not _resiste(S, f, e): diz(S, f"    {e['nome']} resiste"); continue
            e['atordoado'] = max(e['atordoado'], a.get('perde', 2)); diz(S, f"    {e['nome']} fica PRESO NO OLHAR (perde {a.get('perde', 2)} ações)"); _para(S, e, f"{e['nome']} ficou preso no olhar", so_controlado=True)
    elif t == 'invoca':
        for i in range(a.get('n', 2)): o = _entra(S, CR.faz(a['que'], nome=f"{a.get('nome_de', a['que'])} chamado {i + 1}", **a.get('mais', {})), f['lado'], f['x'] - frente(f) * a.get('atras', 0)); diz(S, f"    chega {o['nome']}")
    elif t == 'levanta':
        for c in _caidos_j(S, f, a)[:a.get('n', 9)]:
            c['erguido'] = True
            if a.get('so_seus'): c.update(estado='pe', pv=int(c['pvmax'] * a.get('pv', 0.5)), chao=True, levantado=True); diz(S, f"    {c['nome']} SE ERGUE de novo ({c['pv']}/{c['pvmax']})")
            else:
                if c['estado'] == 'caido': c['estado'] = 'morto'
                o = _entra(S, CR.faz(a.get('que', 'corpo-seco'), nome=f"o morto de {c['nome']}"), f['lado'], c['x']); o['levantado'] = True; o['erguido'] = True; o['chao'] = True; diz(S, f"    {c['nome']} SE ERGUE, morto, do lado de {f['nome']}")
        _para(S, f, f"{f['nome']} ergueu os mortos")
    elif t == 'cura':
        o = min(meus, key=lambda o: o['pv'] / o['pvmax']); g = min(o['pvmax'] - o['pv'], int(o['pvmax'] * a.get('pv', 0.3))); o['pv'] += g; diz(S, f"    {o['nome']} recupera {g} ({o['pv']}/{o['pvmax']})")
    elif t == 'escuro':
        if 'escuro' not in S['tempo']: S['tempo'].append('escuro'); S['escuro_r'] = a.get('rodadas', 3) + 1; diz(S, '    cai o escuro')
    elif t == 'bebe':                                       # o chefe desfaz um dos seus para fechar a própria carne
        v = [o for o in meus if o is not f and o.get('levantado') or tem(o, 'sem vida') and o is not f]
        if v: o = min(v, key=lambda o: o['pv']); g = min(f['pvmax'] - f['pv'], int(f['pvmax'] * a.get('pv', 0.3))); f['pv'] += g; o['estado'] = 'morto'; o['pv'] = 0; diz(S, f"    {f['nome']} desfaz {o['nome']} e recupera {g} ({f['pv']}/{f['pvmax']})")
    _fim(S)


def _rider(S, f, e, a, dano):
    """o que a arte que feriu deixa no alvo: só estado que a luta de hoje já roda"""
    r = a.get('deixa')
    if not r or not e or e['estado'] != 'pe': return
    if r == 'chao' and _derruba(S, f, e) and not e['chao']: e['chao'] = True; diz(S, f"    {e['nome']} vai ao chão")
    elif r == 'queima' and not tem(e, 'sem vida') and dano >= e['pvmax'] * T.FERIDA: q = max(1, int(dano * T.SANGRA)); ant = e['sangra'] or [0, 0]; e['sangra'] = [max(q, ant[0]), max(T.SANGRA_RODADAS[1], ant[1])]; diz(S, f"    {e['nome']} queima ({e['sangra'][0]} por {e['sangra'][1]} rodadas)")
    elif r == 'veneno' and not tem(e, 'sem vida'): q = max(1, int(dano * a.get('fracao', TB.VENENO['fracao']))); ant = e['veneno'] or [0, 0]; e['veneno'] = [max(q, ant[0]), a.get('rodadas_v', TB.VENENO['rodadas'])]; diz(S, f"    o veneno entra em {e['nome']} ({e['veneno'][0]} por rodada)")
    elif r == 'raiz' and not tem(e, 'imaterial'): e['raiz'] = a.get('rodadas', 2); diz(S, f"    {e['nome']} está PRESO ao chão por {e['raiz']} rodadas")
    elif r == 'dreno' and f['estado'] == 'pe': g = min(f['pvmax'] - f['pv'], int(dano * TC.DRENO)); f['pv'] += g; diz(S, f"    {f['nome']} bebe a vida que tirou (+{g})")
    elif r == 'atordoa' and dano >= e['pvmax'] * T.FERIDA: e['atordoado'] = max(e['atordoado'], 1); diz(S, f"    {e['nome']} fica atordoado")
    elif r == 'folego': e['fol'] = max(0, e['fol'] - a.get('tira', 3)); diz(S, f"    {e['nome']} perde o fôlego")


def _fase(S, e):
    """o chefe muda de fase quando o PV cruza o limiar: ganha e perde traços, solta-se do que o prendia, e a luta para e pergunta"""
    for i, fs in enumerate(e['fases'], 1):
        if e['fase'] >= i or e['pv'] > e['pvmax'] * fs['abaixo'] or e['estado'] != 'pe': continue
        e['fase'] = i; e['tracos'] = [t for t in e['tracos'] if t not in fs.get('perde', [])] + list(fs.get('ganha', []))
        if fs.get('cura'): e['pv'] = min(e['pvmax'], e['pv'] + int(e['pvmax'] * fs['cura']))
        e.update(raiz=0, chao=False, atordoado=0); e['agarrado'] = None
        if fs.get('acerto'):
            for w in [e['arma'], e['arma2'], e['punho']] + e.get('armas_corpo', []):
                if w: w['acerto'] += fs['acerto']
        e['def_fixa'] += fs.get('defesa', 0)
        if fs.get('sopro_recarga') is not None: e['sopro_rec'] = fs['sopro_recarga']
        if fs.get('brado'):
            for o in de_pe(S, e['lado']): o['brado'] = TC.BRADO['rodadas'] + 1; o['abalado'] = False
        diz(S, f"  ◆ {e['nome']}: {fs['diz']}"); _para(S, e, f"{e['nome']} mudou: {fs['diz']}"); S['fases_vistas'] = max(S.get('fases_vistas', 0), i)
        if fs.get('foge'):                                  # o chefe covarde larga a luta (é roteiro, não é teste): o bando testa a coragem como se o líder tivesse caído
            e['estado'] = 'fugiu'; diz(S, f"    {e['nome']} FOGE"); _para(S, e, f"{e['nome']} fugiu")
            for o in de_pe(S, e['lado']): _moral(S, o, 'lider_caiu')
            _fim(S); return


def _desfaz(S, e):
    """morto quem os ergueu, os mortos que ele segurava de pé caem"""
    for o in de_pe(S, e['lado']):
        if o is not e and tem(o, 'sem vida') and (e['desfaz'] == 'todos' or o.get('levantado')): o['estado'] = 'morto'; o['pv'] = 0; diz(S, f"    {o['nome']} se desfaz")


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
    bicho  = {"bicho": "lobo", "nome"?: "lobo 1", "lider"?, "linha"?}     (a espécie inteira sai do tabelas_bichos.py; ou a pessoa que o bichos.bicho devolve)
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
        d = dict(d)
        if isinstance(d.get('bicho'), str):
            import bichos
            esp = d.pop('bicho'); d.pop('nivel', None); return bichos.bicho(esp, **d)
        v = d.pop('veste', {})
        ruins = [k for k in v if k not in ('arma', 'arma2', 'armadura', 'elmo', 'escudo', 'pecas')]
        if ruins: sys.exit(f'{d.get("nome")}: não sei vestir "{ruins[0]}" (use: arma, arma2, armadura, elmo, escudo, pecas)')
        p = padrao(d.pop('nome'), d.pop('nivel'), molde=d.pop('molde', 'guerreiro'), maestria=d.pop('maestria', None), atributos=d.pop('atributos', None), **d)
        return veste(p, arma=peca(v.get('arma'), 'arma'), arma2=peca(v.get('arma2'), 'arma'), armadura=peca(v.get('armadura'), 'armadura'), elmo=peca(v.get('elmo'), 'armadura'),
                     escudo=peca(v.get('escudo'), 'escudo'), pecas=[peca(x, 'armadura') for x in v.get('pecas', [])])
    return nova([pessoa(x) for x in C['A']], [pessoa(x) for x in C['B']], inicio=C.get('inicio', 'perto'), lugar=C.get('lugar'), tempo=C.get('tempo'), surpresa=C.get('surpresa'))


def salva(S, arq):
    """guarda a luta no arquivo e devolve ao Livro de Itens a durabilidade gasta até aqui"""
    json.dump(S, open(arq, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    if S.get('mundo'): return                               # luta do mundo: a durabilidade volta por evento, no ato.py (o gravador é um só)
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
    print('\n'.join(S['log'])); print(); print(situacao(S)); print(); print('FIM:', resultado_diz(S))


if __name__ == '__main__':
    import signal; hasattr(signal, 'SIGPIPE') and signal.signal(signal.SIGPIPE, signal.SIG_DFL)      # a saída cortada (`| head`) acaba o comando calada, sem erro de programa: tudo já foi gravado antes de falar
    a = sys.argv[1:]
    if a[:1] == ['demo']: _demo()
    elif a[:1] == ['nova'] and len(a) >= 3:
        try: S = cenario(a[1])
        except OSError: sys.exit(f'não há o cenário "{a[1]}"')
        except (ValueError, KeyError, TypeError) as x: sys.exit(f'o cenário "{a[1]}" não se lê ({type(x).__name__}: {x}). Veja o exemplo: dados/cenario_exemplo.json')
        S['comecou'] = True; salva(S, a[2]); print(situacao(S))
        print(f'\nA luta está em {a[2]}. As ordens: python3 luta.py roda {a[2]} "Nome: atacar Alvo agressiva" "grupo: segurar"')
    elif a[:1] == ['roda'] and len(a) >= 2:
        try: S = json.load(open(a[1], encoding='utf-8'))
        except (OSError, ValueError): sys.exit(f'não há a luta "{a[1]}" (ou o arquivo não se lê). Uma luta nova: python3 luta.py nova CENARIO.json {a[1]}')
        if S['fim']: sys.exit('esta luta já acabou.')
        for o in a[2:]: ordem(S, o)
        S['log'] = []; fim = corre(S, interativo=True)
        salva(S, a[1])                                      # grava ANTES de falar: a saída cortada não perde o que o dado rolou
        print('\n'.join(S['log'])); print(); print(situacao(S))
        if fim == 'fim': print(); print('FIM:', resultado_diz(S))
    elif a[:1] in (['nova'], ['roda']): sys.exit('diga os arquivos: `python3 luta.py nova CENARIO.json LUTA.json` · `python3 luta.py roda LUTA.json "Nome: atacar"`')
    else: print(__doc__)
