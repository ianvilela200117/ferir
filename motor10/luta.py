#!/usr/bin/env python3
"""luta.py — MOTOR 10: A LUTA. Grupo contra grupo, numa linha de casas (1 casa ≈ 3 m), rodada a rodada.

O que entra na conta (as regras estão no REGRAS.md; os números, no tabelas.py):
  1 distância e alcance · 2 o lugar (estreito, alto, cobertura) · 3 o tempo (escuro, chuva, lama, neblina, vento, calor, água)
  4 fôlego · 5 golpe contra armadura · 6 parte do corpo e ferida · 7 durabilidade · 8 moral · 9 grupo contra grupo
  10 A LUTA PARA E PERGUNTA: quando algo muda, a rodada acaba e o script devolve a situação; a ordem do jogador volta por `ordens`.

Uso em código:
  S = nova(lado_a, lado_b, inicio='perto', lugar={...}, tempo=[...])     (listas de pessoas do pessoas.py; quem tem controla=True recebe ordem)
  corre(S, interativo=True)      roda até uma PARADA ou o fim · S['ordens'][nome] = dict(acao=..., alvo=..., postura=...)
  resultado(S)                   quem venceu, mortos, caídos, presos, feridas, peças quebradas
Uso de linha de comando (a luta de verdade: dado de verdade, o estado guardado num arquivo entre uma ordem e outra):
  python3 luta.py nova CENARIO.json lutas/NOME.json                       monta a luta e mostra o quadro
  python3 luta.py roda lutas/NOME.json ["Nome: ordem"] ["grupo: ordem"]   roda até a próxima PARADA (ou o fim) com as ordens dadas
       ordem: atacar [alvo] · segurar · avancar · recuar · folego · guardar NOME, e no fim a postura (firme, agressiva, defensiva)
  python3 luta.py demo           uma luta de exemplo num corredor, com as paradas
"""
import copy, json, random, secrets, sys
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
    return dict(total=sum(a) + sum(b) + bonus, nat=n, falha=n == (1, 1),
                crit=(max(n) >= (19 if crit19 else 20) and min(n) >= T.CRIT_OUTRO))


def rola(dado, dobra=False):
    n, f = map(int, dado.split('d'))
    return sum(D.d(f) for _ in range(n * (2 if dobra else 1)))


# ---------- montar a luta ----------
def nova(lado_a, lado_b, inicio='perto', lugar=None, tempo=None, surpresa=None, quieto=False):
    S = dict(r=0, L=[], itens={}, lugar=dict(lugar or {}), tempo=list(tempo or []), log=[], paradas=[], fim=None, ordens={}, surpresa=surpresa, quieto=quieto, sem_parada=0)
    sep = T.INICIO[inicio] if isinstance(inicio, str) else inicio
    for lado, gente, x0, tras in (('A', lado_a, 0, -1), ('B', lado_b, sep, 1)):
        larg = S['lugar'].get('largura') or 99; cheio = {}
        for p in sorted(gente, key=lambda p: p.get('linha') == 'trás'):
            f = ficha(p); f['lado'] = lado
            x = x0 + (tras if p.get('linha') == 'trás' else 0)
            while cheio.get(x, 0) >= larg: x += tras
            cheio[x] = cheio.get(x, 0) + 1
            f.update(x=x, estado='pe', feridas=[], sangra=False, atordoado=0, chao=False, preso=False, abalado=False, reac=f['reacoes'], postura='firme',
                     usou=[], testou=[], morte=[0, 0], agressor=None, recarga=0, sem_arma=False, resguardo=False, ini=sum(d20x()) + sum(d20x()) + f['percep_b'] + f['agil_b'])
            f.setdefault('moral', 'testa'); f.setdefault('papel', 'frente')
            for w in (f['arma'], f['arma2']):
                if w: w['item'] = _guarda_item(S, w['item'])
            for pc in f['partes'].values(): pc['item'] = _guarda_item(S, pc['item'])
            if f['escudo']: f['escudo']['item'] = _guarda_item(S, f['escudo']['item'])
            S['L'].append(f)
    S['paradas'].append('a luta vai começar')
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
def tem_tempo(S, k): return k in S['tempo']
def arma_de(f):
    """a arma em uso agora: a principal; a segunda (ou as mãos) se a principal caiu, ou se é de tiro e há inimigo colado"""
    return f['_w']


def _escolhe_arma(S, f):
    w = f['arma']; colado = any(dist(f, e) <= 1 for e in inimigos(S, f))
    if f['sem_arma'] or (w['distancia'] and colado): w = f['arma2'] or f['_punho']
    f['_w'] = w


def alvos(S, f, w):
    """[(inimigo, penalidade)] que esta arma alcança agora"""
    out = []
    for e in inimigos(S, f):
        dd = dist(f, e)
        if w['distancia']:
            if dd < 2 or dd > w['alcance']: continue
            if tem_tempo(S, 'neblina') and dd > 3: continue
        elif dd > max(1, w['alcance']): continue
        pen = T.ENTRE if entre(S, f, e) and S['lugar'].get('alto') != f['lado'] else 0
        out.append((e, pen))
    return out


# ---------- o golpe ----------
def golpe(S, a, e, w, livre=''):
    g = next((x for x in de_pe(S, e['lado']) if x.get('guarda') == e['nome'] and x is not e and dist(x, e) <= 1 and x['reac'] > 0), None)
    if g: g['reac'] -= 1; diz(S, f"  {g['nome']} se põe na frente de {e['nome']}"); e = g
    tiro = w['distancia']; pa, pd = T.POSTURAS[a['postura']], T.POSTURAS[e['postura']]
    bon = w['acerto'] + pa[0] - (T.SEM_FOLEGO if a['fol'] <= 0 else 0) - (2 if a['abalado'] else 0)
    bon -= sum(4 if gr else 2 for p, gr in a['feridas'] if p == 'braços')
    for k in S['tempo']:
        bon += T.TEMPO[k].get('tiro' if tiro else 'acerto', 0)
    if S['lugar'].get('alto') == a['lado']: bon += T.ALTO['tiro' if tiro else 'acerto']
    if tiro and S['lugar'].get('cobertura') == e['lado']: bon += T.COBERTURA
    if entre(S, a, e) and S['lugar'].get('alto') != a['lado']: bon += T.ENTRE
    df = e['defesa'] + pd[1] - (T.SEM_FOLEGO if e['fol'] <= 0 else 0) - (4 if e['chao'] else 0) - (2 if e['preso'] else 0) + (2 if e['resguardo'] else 0)
    df += sum(T.TEMPO[k].get('defesa', 0) for k in S['tempo'])
    j = jogada(bon, crit19=bool(w['efeitos'].get('critico_19'))); it_w = S['itens'][w['item']]
    cab = f"  {a['nome']} {'atira em' if tiro else 'golpeia'} {e['nome']}" + (f' ({livre})' if livre else '')
    if j['falha']:
        diz(S, f"{cab}: dois 1, erra feio"); _gasta(S, a, w, it_w, 1); return
    if j['total'] < df and not j['crit']:
        diz(S, f"{cab}: {j['total']:g} contra {df:g}, erra"); return
    parte = T.ONDE[D.d(10)]; pc = e['partes'].get(parte); prot = T.NU
    if pc and S['itens'][pc['item']]['dur'][0] > 0:
        prot = pc['rd'] * T.MATRIZ[w['golpe']][pc['material']] / (2 if j['crit'] else 1)
    base = rola(w['dado'], dobra=j['crit']) * T.K_DANO * w['mult']
    dano = int(base / prot * w['fmult'])
    if pc and S['itens'][pc['item']]['dur'][0] > 0:        # o aço gasta o aço
        it_p = S['itens'][pc['item']]
        if pc['cat'] > w['cat']: _gasta(S, a, w, it_w, 1)
        if w['cat'] > pc['cat'] or j['crit']: _gasta_armadura(S, e, pc, it_p, 2 if w['cat'] >= pc['cat'] + 2 else 1)
    e['pv'] -= dano; e['agressor'] = a['nome']
    diz(S, f"{cab}: {j['total']:g} contra {df:g}{', CRÍTICO' if j['crit'] else ''}, {parte}: {dano} ({max(e['pv'], 0)}/{e['pvmax']})"
        + (' · o aço não passa' if dano == 0 else ''))
    if not tiro and e['efeitos'].get('devolve') and a['estado'] == 'pe':
        a['pv'] -= e['efeitos']['devolve']; diz(S, f"    a armadura de {e['nome']} devolve {e['efeitos']['devolve']} em {a['nome']} ({max(a['pv'], 0)}/{a['pvmax']})")
        if a['pv'] <= 0: _cai(S, a, 0)
    if dano <= 0: return
    terrivel = dano >= e['pvmax'] * T.FERIDA_GRAVE
    if e['pv'] <= 0: _cai(S, e, dano)
    elif dano >= e['pvmax'] * T.FERIDA or j['crit']: _ferida(S, e, parte, terrivel, w)
    if w['efeitos'].get('derruba') and 'derruba' not in a['usou'] and e['estado'] == 'pe' and not e['efeitos'].get('firme'):
        a['usou'].append('derruba'); e['chao'] = True; diz(S, f"    {e['nome']} vai ao chão")
    if terrivel:
        for o in de_pe(S, e['lado']):
            if o is not e and dist(o, e) <= 2: _moral(S, o, 'golpe_terrivel')
    if e['estado'] == 'pe' and e['pv'] < e['pvmax'] * 0.25: _moral(S, e, 'ferido_grave')


def _gasta(S, a, w, it, n):
    if w['efeitos'].get('nao_quebra') or it['dur'][0] <= 0: return
    it['dur'][0] = max(0, it['dur'][0] - n)
    if it['dur'][0] == 0:
        diz(S, f"    ✖ {w['nome']} de {a['nome']} QUEBRA"); _para(S, a, f"{w['nome']} de {a['nome']} quebrou")
        w.update(acerto=w['acerto'] - T.BON[w['cat']] - 4, mult=T.MULT[0] * (T.DUAS_MAOS if w['maos'] == 2 else 1), cat=0, efeitos={}, nome=w['nome'] + ' (quebrada)')


def _gasta_armadura(S, e, pc, it, n):
    if any(x['chave'] == 'nao_quebra' for x in it.get('efeitos', [])) or it['dur'][0] <= 0: return
    it['dur'][0] = max(0, it['dur'][0] - n)
    if it['dur'][0] == 0: diz(S, f"    ✖ {pc['nome']} de {e['nome']} se desfaz"); _para(S, e, f"{pc['nome']} de {e['nome']} quebrou")


def _ferida(S, e, parte, grave, w):
    e['feridas'].append((parte, grave)); txt = f"    FERIDA{' GRAVE' if grave else ''} em {e['nome']}, {parte}: "
    if parte == 'cabeça': e['atordoado'] = max(e['atordoado'], 2 if grave else 1); txt += 'atordoado'
    elif parte == 'braços':
        txt += '−4 no acerto' if grave else '−2 no acerto'
        if grave and not e['sem_arma']: e['sem_arma'] = True; txt += ' e larga a arma'
    elif parte == 'tronco': e['fol'] = max(0, e['fol'] - (6 if grave else 3)); e['sangra'] = True; txt += 'perde o fôlego e sangra'
    else:
        if not e['efeitos'].get('firme'): e['chao'] = True
        e['preso'] = e['preso'] or grave; txt += 'vai ao chão' + (' e não anda mais' if grave else '')
    if w['efeitos'].get('sangra') or grave: e['sangra'] = True
    diz(S, txt); _para(S, e, f"{e['nome']} foi ferido ({parte}{', grave' if grave else ''})", so_controlado=True)


def _cai(S, e, dano):
    macico = dano > e['pvmax'] * 0.5
    e['estado'] = 'morto' if macico else 'caido'; e['pv'] = min(e['pv'], 0)
    diz(S, f"    ☠ {e['nome']} MORRE" if macico else f"    ▼ {e['nome']} CAI")
    _para(S, e, f"{e['nome']} {'morreu' if macico else 'caiu'}")
    aliados = de_pe(S, e['lado'])
    if e.get('lider'):
        for o in aliados: _moral(S, o, 'lider_caiu')
    tot = [f for f in S['L'] if f['lado'] == e['lado']]
    if len(aliados) * 2 <= len(tot):
        for o in aliados: _moral(S, o, 'metade_caiu')


def _moral(S, f, motivo):
    if f['moral'] == 'firme' or f['estado'] != 'pe' or (motivo in f['testou'] and motivo != 'golpe_terrivel') or f.get('_moral_r') == [S['r'], motivo]: return
    f['testou'].append(motivo); f['_moral_r'] = [S['r'], motivo]
    meus, deles = len(de_pe(S, f['lado'])), len(de_pe(S, outro(f['lado'])))
    ld = lider(S, f['lado']); bon = f['vontade_b'] + (T.MORAL_LIDER if ld and ld['estado'] == 'pe' and ld is not f else 0)
    bon += T.MORAL_MAIS if meus > deles else T.MORAL_MENOS if deles >= 2 * meus else 0
    t = sum(d20x()) + sum(d20x()) + bon; cd = T.MORAL[motivo]
    if t >= cd: return
    if t >= cd - 10 and not f['abalado']:
        f['abalado'] = True; diz(S, f"    {f['nome']} fica ABALADO ({motivo.replace('_', ' ')}: {t} contra {cd})"); return
    rende = f['pv'] < f['pvmax'] * 0.25 or S['lugar'].get('sem_saida') == f['lado']
    f['estado'] = 'rendido' if rende else 'fugiu'
    diz(S, f"    {f['nome']} {'SE RENDE' if rende else 'FOGE'} ({motivo.replace('_', ' ')}: {t} contra {cd})")
    _para(S, f, f"{f['nome']} {'se rendeu' if rende else 'fugiu'}")
    if not rende: _golpe_livre(S, f, 'ele dá as costas')
    if f.get('lider'):
        for o in de_pe(S, f['lado']): _moral(S, o, 'lider_caiu')


def _golpe_livre(S, f, porque, so_alcance=False):
    for e in sorted(inimigos(S, f), key=lambda e: -e['_w']['alcance']):
        w = e['_w']
        if e['reac'] <= 0 or w['distancia'] or dist(e, f) > max(1, w['alcance']): continue
        if so_alcance and w['alcance'] <= f['_w']['alcance']: continue
        e['reac'] -= 1; golpe(S, e, f, w, livre=porque); return


def _para(S, f, txt, so_controlado=False):
    """uma PARADA: o que faz a luta parar e perguntar. Vale o que toca o lado do jogador (A) ou o líder do outro."""
    if so_controlado and not f.get('controla'): return
    if f['lado'] == 'A' or f.get('lider') or 'rendeu' in txt:
        if txt not in S['paradas']: S['paradas'].append(txt)


# ---------- o turno de cada um ----------
def _anda(S, f, sentido):
    passo = min([T.PASSO] + [T.TEMPO[k]['passo'] for k in S['tempo'] if 'passo' in T.TEMPO[k]])
    if sentido > 0 and S['lugar'].get('alto') == outro(f['lado']): passo = 1
    if sentido < 0 and any(dist(f, e) <= 1 for e in inimigos(S, f)): _golpe_livre(S, f, 'ele recua')
    larg = S['lugar'].get('largura'); andou = 0
    for _ in range(passo):
        if f['estado'] != 'pe' or f['chao'] or f['preso']: break    # o golpe que o pegou no caminho o parou
        nx = f['x'] + sentido * frente(f)
        ini_la = [e for e in inimigos(S, f) if e['x'] == nx]
        if sentido > 0 and not f['_w']['distancia'] and alvos(S, f, f['_w']) and not ini_la: break    # já alcança alguém: para aqui
        if ini_la:
            # campo aberto: quem sobra depois de cada inimigo estar seguro por SEGURA contorna e entra na casa deles
            colados = [a for a in de_pe(S, f['lado']) if a is not f and any(dist(a, e) <= 1 for e in ini_la)]
            if larg or len(colados) < T.SEGURA * len(ini_la) or f['x'] == nx: break
        if larg and len([a for a in de_pe(S, f['lado']) if a['x'] == nx]) >= larg: break
        f['x'] = nx; andou += 1
        if sentido > 0: _golpe_livre(S, f, 'o alcance bate primeiro', so_alcance=True)
    return andou


def _decide(S, f):
    _escolhe_arma(S, f); w = f['_w']; o = S['ordens'].get(f['nome']) or {}
    if not f.get('controla'):
        og = S['ordens'].get('grupo') if f['lado'] == 'A' else None
        o = dict(acao=og) if og and f['papel'] != 'guarda' else {}
    acao = o.get('acao', 'atacar'); f['postura'] = o.get('postura', f['postura'] if f.get('controla') else 'firme')
    if acao == 'folego' or f['fol'] < w['folego'] + f['fol_rodada']: return ('folego',)
    if f['chao']: return ('levanta',)
    if f['sem_arma'] and not any(dist(f, e) <= 1 for e in inimigos(S, f)): return ('pega',)
    if acao == 'recuar':
        if min([dist(f, e) for e in inimigos(S, f)] or [9]) < 3 and not f['preso']: return ('anda', -1)
        acao = 'segurar'
    if w['distancia'] and f['recarga'] > 0: return ('recarrega',)
    al = alvos(S, f, w)
    if al:
        nome = o.get('alvo'); e = next((x for x in al if x[0]['nome'] == nome), None)
        if not e:
            if nome and nome != 'o mais ferido' and not any(x['nome'] == nome for x in inimigos(S, f)) and f.get('controla'): _para(S, f, f'o alvo de {f["nome"]} ({nome}) não está mais de pé')
            limpos = [x for x in al if x[1] == 0] or al
            ag = next((x for x in limpos if x[0]['nome'] == f['agressor']), None)
            e = ag if ag and D.d(10) <= 6 else min(limpos, key=lambda x: x[0]['pv'] / x[0]['pvmax'])
        return ('golpe', e[0])
    gd = next((x for x in de_pe(S, f['lado']) if x['nome'] == f.get('guarda')), None)
    if gd:
        if dist(f, gd) > 1 and not f['preso']: return ('anda', 1 if (gd['x'] - f['x']) * frente(f) > 0 else -1)
        return ('espera',)
    if acao == 'segurar' or f['preso'] or (w['distancia'] and not tem_tempo(S, 'neblina')): return ('espera',)
    return ('anda', 1)


def _turno(S, f):
    f['resguardo'] = False; f['reac'] = f['reacoes']
    f['fol'] = min(f['folmax'], f['fol'] + 1 + T.POSTURAS[f['postura']][2])
    n = f['acoes'] if f['fol'] > 0 else 1
    if f['atordoado']:
        perde = min(n, f['atordoado']); n -= perde; f['atordoado'] = 0; diz(S, f"  {f['nome']} está atordoado: perde {perde} ação(ões)")
    pagou = False
    for _ in range(n):
        if f['estado'] != 'pe' or S['fim']: break
        ac = _decide(S, f); w = f['_w']
        if ac[0] in ('golpe', 'anda') and not pagou:      # o peso da armadura, uma vez por rodada em que a pessoa se mexe
            pagou = True
            f['fol'] -= f['fol_rodada'] + sum(T.TEMPO[k].get('folego', 0) for k in S['tempo']) + (sum(T.TEMPO[k].get('folego_armadura', 0) for k in S['tempo']) if any(p['material'] != 'couro' for p in f['partes'].values()) else 0)
        if ac[0] == 'folego':
            g = D.d(4) + 1; f['fol'] = min(f['folmax'], max(f['fol'], 0) + g); f['resguardo'] = True; diz(S, f"  {f['nome']} toma fôlego (+{g}: {f['fol']}/{f['folmax']})")
        elif ac[0] == 'levanta': f['chao'] = False; diz(S, f"  {f['nome']} se levanta")
        elif ac[0] == 'pega': f['sem_arma'] = False; diz(S, f"  {f['nome']} apanha a arma")
        elif ac[0] == 'recarrega': f['recarga'] -= 1
        elif ac[0] == 'espera': f['resguardo'] = True; break
        elif ac[0] == 'anda':
            f['fol'] -= 1; k = _anda(S, f, ac[1])
            if k: diz(S, f"  {f['nome']} {'avança' if ac[1] > 0 else 'recua'} ({k} casa{'s' if k > 1 else ''})")
            else: f['resguardo'] = True; break
        elif ac[0] == 'golpe':
            f['fol'] -= w['folego']; f['recarga'] = w.get('recarga', 0) if w['distancia'] else 0
            golpe(S, f, ac[1], w)
        _fim(S)
    if f['estado'] == 'pe' and f['fol'] <= 0 and f.get('controla'): _para(S, f, f"{f['nome']} está sem fôlego")


def _fim(S):
    for lado in 'AB':
        if not de_pe(S, lado) and not S['fim']: S['fim'] = outro(lado)


def rodada(S):
    S['r'] += 1; S['paradas'] = []; diz(S, f"— RODADA {S['r']} —")
    pv0 = {f['nome']: f['pv'] for f in S['L'] if f.get('controla')}
    for f in S['L']:
        f['_punho'] = f.get('_punho') or dict(nome='as mãos', cat=0, dado='1d4', mult=1, golpe='impacto', alcance=1, distancia=False, maos=1, recarga=0,
                                               acerto=f['arma']['acerto'] - T.BON[f['arma']['cat']], folego=1, fmult=f['arma']['fmult'], efeitos={}, item=_guarda_item(S, dict(dur=[9999, 9999], efeitos=[])))
        _escolhe_arma(S, f)
    for f in sorted(de_pe(S), key=lambda f: -f['ini']):
        if f['estado'] != 'pe' or S['fim']: continue
        if S['r'] == 1 and S['surpresa'] == f['lado']: continue
        _turno(S, f)
    for f in S['L']:                                        # o fim da rodada: o sangue e a vida por um fio
        if f['estado'] == 'pe' and f['sangra']:
            x = max(1, int(f['pvmax'] * T.SANGRA)); f['pv'] -= x
            if f['pv'] <= 0: diz(S, f"  {f['nome']} sangra ({x})"); _cai(S, f, 0)
        elif f['estado'] == 'caido' and max(f['morte']) < 3:
            ok = D.d(20) >= T.MORTE_CD; f['morte'][0 if ok else 1] += 1
            if f['morte'][1] >= 3: f['estado'] = 'morto'; diz(S, f"  ☠ {f['nome']} morre no chão"); _para(S, f, f"{f['nome']} morreu no chão")
    _fim(S)
    for f in S['L']:
        if f.get('controla') and f['estado'] == 'pe':
            for lim in (0.5, 0.25):
                if pv0[f['nome']] >= f['pvmax'] * lim > f['pv']: _para(S, f, f"{f['nome']} está abaixo de {int(lim * 100)}% do PV")
    S['sem_parada'] = 0 if S['paradas'] else S['sem_parada'] + 1
    if S['sem_parada'] >= 3 and not S['fim']: S['paradas'].append('três rodadas sem novidade'); S['sem_parada'] = 0


def corre(S, interativo=False, maximo=60):
    """roda até acabar. Com interativo, devolve 'parada' sempre que houver o que perguntar (a ordem volta em S['ordens'])."""
    primeiro = True
    while not S['fim'] and S['r'] < maximo:
        if interativo and S['paradas'] and not (primeiro and S['r'] > 0): return 'parada'
        primeiro = False
        rodada(S)
    if not S['fim']: S['fim'] = 'empate'
    return 'fim'


def resultado(S):
    q = lambda est: [f['nome'] for f in S['L'] if f['estado'] == est]
    return dict(vencedor=S['fim'], rodadas=S['r'], mortos=q('morto'), caidos=q('caido'), fugiram=q('fugiu'), presos=q('rendido'),
                feridas={f['nome']: f['feridas'] for f in S['L'] if f['feridas']},
                quebradas=[it.get('nome', k) for k, it in S['itens'].items() if it['dur'][0] <= 0])


def situacao(S):
    """o quadro que o jogador vê quando a luta para"""
    L = [f"RODADA {S['r']} · " + ' · '.join(S['tempo'] or ['tempo limpo']) + (f" · lugar: {S['lugar']}" if S['lugar'] else '')]
    for lado, nome in (('A', 'A CASA'), ('B', 'O OUTRO LADO')):
        L.append(nome + ':')
        for f in S['L']:
            if f['lado'] != lado: continue
            est = dict(pe='de pé', caido='CAÍDO', morto='MORTO', fugiu='fugiu', rendido='rendido')[f['estado']]
            fer = ', '.join(p + (' (grave)' if g else '') for p, g in f['feridas'])
            L.append(f"  {f['nome']:<22} {est:<8} PV {max(f['pv'], 0):>4}/{f['pvmax']:<4} fôlego {max(f['fol'], 0):>2}/{f['folmax']:<2} casa {f['x']:>3}"
                     + (f" · feridas: {fer}" if fer else '') + (' · sangrando' if f['sangra'] and f['estado'] == 'pe' else '') + (' · abalado' if f['abalado'] else '') + (' · no chão' if f['chao'] else ''))
    if S['paradas']: L.append('PAROU PORQUE: ' + ' · '.join(S['paradas']))
    return '\n'.join(L)


# ---------- o simulador (o banco de provas usa) ----------
def duelos(faz_a, faz_b, n=1000, **kw):
    """n lutas entre os lados que faz_a() e faz_b() montam. Devolve (% de vitória de A, mediana de rodadas)."""
    va = 0; rs = []
    for _ in range(n):
        S = nova(faz_a(), faz_b(), quieto=True, **kw); corre(S)
        va += 1 if S['fim'] == 'A' else 0.5 if S['fim'] == 'empate' else 0; rs.append(S['r'])
    rs.sort()
    return round(100 * va / n), rs[len(rs) // 2]


# ---------- a luta de verdade: o cenário, o arquivo da luta e as ordens ----------
def cenario(arq):
    """monta a luta de um arquivo de cenário: {"inicio","lugar","tempo","surpresa","A":[pessoa...],"B":[pessoa...]}
    pessoa = {"nome","nivel", "maestria"?, "atributos"?, "controla"?, "lider"?, "papel"?, "guarda"?, "moral"?, "linha"?,
              "veste": {"arma": ["espada","Raro"] ou o id de um item do Livro de Itens, "arma2", "armadura": ["malha","Raro"] ou id, "escudo": "Raro" ou id}}"""
    from pessoas import padrao, veste
    from itens import carrega, cat_i
    C = json.load(open(arq, encoding='utf-8')); B = carrega()['itens']
    def peca(x, tipo):
        if x is None: return None
        if isinstance(x, str) and x in B: return B[x]
        return cat_i(x) if tipo == 'escudo' else (x[0], cat_i(x[1]))
    def pessoa(d):
        d = dict(d); v = d.pop('veste', {})
        p = padrao(d.pop('nome'), d.pop('nivel'), maestria=d.pop('maestria', None), atributos=d.pop('atributos', None), **d)
        return veste(p, arma=peca(v.get('arma'), 'arma'), arma2=peca(v.get('arma2'), 'arma'), armadura=peca(v.get('armadura'), 'armadura'), escudo=peca(v.get('escudo'), 'escudo'))
    return nova([pessoa(x) for x in C['A']], [pessoa(x) for x in C['B']], inicio=C.get('inicio', 'perto'), lugar=C.get('lugar'), tempo=C.get('tempo'), surpresa=C.get('surpresa'))


def salva(S, arq):
    for f in S['L']: f.pop('_w', None)
    json.dump(S, open(arq, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


def ordem(S, txt):
    """'Nome: atacar [alvo] [postura]' · ação: atacar, segurar, avancar, recuar, folego, guardar NOME · 'grupo: segurar|atacar|recuar'"""
    quem, _, resto = txt.partition(':'); quem = quem.strip(); pal = resto.split()
    if not pal: sys.exit(f'ordem vazia: "{txt}"')
    if quem == 'grupo': S['ordens']['grupo'] = pal[0]; return
    f = next((x for x in S['L'] if x['nome'].lower() == quem.lower()), None)
    if not f: sys.exit(f'não há "{quem}" nesta luta')
    post = pal.pop() if pal[-1] in T.POSTURAS else None
    if not pal: pal = ['atacar']
    acao = pal[0]; alvo = ' '.join(pal[1:]) or None
    if acao not in ('atacar', 'segurar', 'avancar', 'recuar', 'folego', 'guardar'): sys.exit(f'ação desconhecida: "{acao}"')
    f['controla'] = True
    if acao == 'guardar': f['guarda'] = alvo
    elif acao == 'atacar': f['guarda'] = None
    S['ordens'][f['nome']] = dict(acao='atacar' if acao in ('avancar', 'guardar') else acao, alvo=alvo if acao == 'atacar' else None, **({'postura': post} if post else {}))


def _fecha_itens(S):
    """a durabilidade gasta na luta volta para o Livro de Itens"""
    from itens import carrega, grava
    B = carrega(); mudou = False
    for it in S['itens'].values():
        if it.get('id') in B['itens']: B['itens'][it['id']]['dur'] = it['dur']; mudou = True
    if mudou: grava(B)


def _demo():
    from pessoas import padrao, veste
    from itens import item
    semente(7)
    rei = veste(padrao('o ferreiro', 40, controla=True, moral='firme', linha='trás'), arma=('lança', 3), armadura=('couro', 2))
    a = [veste(padrao('Moreth', 120, moral='firme', lider=True), arma=item('arma', 4, 'a Maça do Rio', familia='maça', efeitos=[dict(chave='derruba')]), armadura=('malha', 4), escudo=3),
         veste(padrao('Gonde', 32, papel='guarda', guarda='o ferreiro', moral='firme'), arma=('espada', 2), armadura=('malha', 2), escudo=2), rei]
    b = [veste(padrao('Nutoccone', 90, lider=True), arma=('espada', 3), armadura=('malha', 2), escudo=2)] + \
        [veste(padrao(f'herdeiro {i}', 30 + 5 * i), arma=('lança' if i % 2 else 'machado', 1), armadura=('couro', 1)) for i in range(1, 7)]
    S = nova(a, b, inicio='perto', lugar=dict(largura=2, sem_saida='B'), tempo=['escuro'])
    S['ordens']['o ferreiro'] = dict(acao='segurar', postura='defensiva')
    while corre(S, interativo=True) == 'parada':
        print('\n'.join(S['log'])); S['log'] = []; print(); print(situacao(S)); print()
        if 'o ferreiro está abaixo de 50% do PV' in S['paradas']: S['ordens']['o ferreiro'] = dict(acao='recuar', postura='defensiva'); print('>>> ordem: recuar\n')
        S['paradas'] = []
    print('\n'.join(S['log'])); print(); print(situacao(S)); print(); print(json.dumps(resultado(S), ensure_ascii=False))


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[:1] == ['demo']: _demo()
    elif a[:1] == ['nova'] and len(a) >= 3:
        S = cenario(a[1]); salva(S, a[2]); print(situacao(S))
        print(f'\nA luta está em {a[2]}. As ordens: python3 luta.py roda {a[2]} "Nome: atacar Alvo agressiva" "grupo: segurar"')
    elif a[:1] == ['roda'] and len(a) >= 2:
        S = json.load(open(a[1], encoding='utf-8'))
        if S['fim']: sys.exit('esta luta já acabou.')
        for o in a[2:]: ordem(S, o)
        S['paradas'] = []; S['log'] = []; fim = corre(S, interativo=True)
        print('\n'.join(S['log'])); print(); print(situacao(S))
        if fim == 'fim': print(); print('FIM:', json.dumps(resultado(S), ensure_ascii=False)); _fecha_itens(S)
        salva(S, a[1])
    else: print(__doc__)
