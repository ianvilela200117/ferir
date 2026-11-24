"""aplica.py — RASCUNHO: monta o luta_j.py, que é o luta.py de hoje (a cópia em base/) com os remendos da parte J.
Cada remendo troca um trecho exato, uma vez só; se o luta.py mudar e o trecho não existir mais, este script para e diz qual.
Uso: python3 aplica.py     (escreve luta_j.py nesta pasta e conta as linhas tocadas)
"""
import os
AQUI = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(AQUI, 'base', 'luta.py'), encoding='utf-8').read()
R = []          # (rótulo, de, para)
def troca(rotulo, de, para): R.append((rotulo, de, para))

troca('a ficha nova', "from pessoas import ficha\n", "from criaturas import ficha_j as ficha\nimport tabelas_criaturas as TC\nimport criaturas as CR\n")
troca('o estado novo de cada um', "            f.setdefault('moral', 'testa'); f.setdefault('papel', 'guarda' if f.get('guarda') else 'frente')\n",
      "            f.setdefault('moral', 'testa'); f.setdefault('papel', 'guarda' if f.get('guarda') else 'frente'); _estado_j(f)\n")
troca('as armas novas no registro da luta', "            for w in [f['arma'], f['arma2'], f['punho']] + f.get('armas_corpo', []) + [f.get('sopro')]:\n",
      "            for w in [f['arma'], f['arma2'], f['punho']] + f.get('armas_corpo', []) + [f.get('sopro'), f.get('tiro')] + list(f.get('arma_arte', {}).values()):\n")
troca('o enraizado não anda', "def _nao_anda(S, f): return bool(f['preso'] or _agarrado(S, f))", "def _nao_anda(S, f): return bool(f['preso'] or f.get('raiz', 0) > 0 or _agarrado(S, f))")
troca('ninguém derruba quem não tem corpo', "return e['estado'] == 'pe' and not efeito(S, e, 'firme') and e.get('ocupa', 1) <= a.get('ocupa', 1)",
      "return e['estado'] == 'pe' and not efeito(S, e, 'firme') and e.get('ocupa', 1) <= a.get('ocupa', 1) and not tem(e, 'imaterial')")
troca('o tiro do corpo', "    if f.get('bicho'): return f['armas_corpo'][f['golpes'] % len(f['armas_corpo'])]      # o bicho alterna as armas do corpo, golpe a golpe\n",
      "    if f.get('bicho'):\n"
      "        if f.get('tiro') and not any(dist(f, e) <= max(1, f['armas_corpo'][0]['alcance']) for e in inimigos(S, f)): return f['tiro']       # ATIRA: de longe, o tiro do corpo\n"
      "        return f['armas_corpo'][f['golpes'] % len(f['armas_corpo'])]      # o bicho alterna as armas do corpo, golpe a golpe\n")
# --- o golpe ---
troca('o golpe diz o que tirou', "def golpe(S, a, e, w, livre=''):\n", "def golpe(S, a, e, w, livre=''):\n    S['ult'] = None\n")
troca('noturno', "    bon += sum(T.TEMPO[k].get('tiro' if tiro else 'acerto', 0) for k in S['tempo'])\n",
      "    bon += sum(T.TEMPO[k].get('tiro' if tiro else 'acerto', 0) for k in S['tempo'] if not (k == 'escuro' and tem(a, 'noturno')))\n")
troca('o golpe cru não se apara', "    df = md + (e['def_fixa'] if w.get('area') else defesa_de(S, e))", "    df = md + (e['def_fixa'] if w.get('area') or w.get('cru') else defesa_de(S, e))")
troca('não se mira a fresta com o golpe cru', "and not tem(e, 'couraça') and not w.get('area') and chance(", "and not tem(e, 'couraça') and not w.get('area') and not w.get('cru') and not w.get('magia') and chance(")
troca('o golpe cru não olha o material', "    prot = pc['rd'] * (1 if w.get('area') else T.MATRIZ[w['golpe']][pc['material']])", "    prot = pc['rd'] * (1 if w.get('area') or w.get('cru') or w.get('magia') else T.MATRIZ[w['golpe']][pc['material']])")
troca('o aço comum e os ossos',
      "    dano = int(rola(w['dado'], max(2 if j['crit'] else 1, esp['dados'] if esp else 1)) * T.K_DANO * w['mult'] / prot * w['fmult'])\n",
      "    if w.get('magia'): prot = _guarda_m(S, e) / (2 if j['crit'] else 1)                    # A GUARDA contra a magia (a conta da magia, B.1): o amuleto, ou 0,6 da armadura do tronco; sem material, sem parte do corpo, sem fresta\n"
      "    if e.get('aco') and not _magica(w): prot *= 3 ** e['aco']                              # O AÇO COMUM conta tantas categorias abaixo (o imaterial, o lobisomem)\n"
      "    dano = int(rola(w['dado'], max(2 if j['crit'] else 1, esp['dados'] if esp else 1)) * T.K_DANO * w['mult'] / prot * w['fmult'])\n"
      "    if tem(e, 'ossos') and w['golpe'] in ('corte', 'ponta'): dano = int(dano * TC.OSSOS)        # OSSOS: o fio e a ponta passam entre eles\n")
troca('o feitiço não gasta a armadura', "    if vestida and (w['cat'] > pc['cat'] or j['crit']): _gasta_armadura(", "    if vestida and not w.get('magia') and (w['cat'] > pc['cat'] or j['crit']): _gasta_armadura(")
troca('o bote e a investida de quem empunha arma', "    if a.get('bicho') and not w.get('area'): a['golpes'] += 1; a['andou_t'] = 0\n",
      "    if (a.get('bicho') or a.get('povo')) and not w.get('area') and not w.get('magia'): a['golpes'] += 1; a['andou_t'] = 0\n")
troca('o corpo que arde só queima quem está perto', "    if not tiro and dv and a['estado'] == 'pe':\n", "    if not tiro and dv and a['estado'] == 'pe' and not (tem(e, 'ardente') and dist(a, e) > 1):\n")
troca('o dreno, a arte cortada, a fase',
      "    if dano <= 0: return\n    S['dano_r'] += dano / e['pvmax']\n",
      "    S['ult'] = [e['nome'], dano]\n"
      "    if dano <= 0: return\n    S['dano_r'] += dano / e['pvmax']\n"
      "    if tem(a, 'dreno') and (w.get('corpo') or w.get('magia')) and a['estado'] == 'pe' and a['pv'] < a['pvmax']:\n"
      "        g = min(a['pvmax'] - a['pv'], max(1, int(dano * TC.DRENO))); a['pv'] += g; diz(S, f\"    {a['nome']} bebe a vida que tirou (+{g}: {a['pv']}/{a['pvmax']})\")\n"
      "    if e.get('prepara') and e['estado'] == 'pe': _concentra(S, e, dano >= e['pvmax'] * T.FERIDA or (j['crit'] and dano >= e['pvmax'] * T.FERIDA_MIN))\n")
troca('os traços de quem empunha arma', "    if a.get('bicho') or e.get('bicho'): _depois_do_golpe(S, a, e, w, dano, esp, len(e['feridas']) > abertas)\n",
      "    if a.get('bicho') or e.get('bicho') or a.get('tracos') or e.get('tracos'): _depois_do_golpe(S, a, e, w, dano, esp, len(e['feridas']) > abertas)\n"
      "    if e.get('fases') and e['estado'] == 'pe': _fase(S, e)\n")
troca('o bote e a investida do povo', "    if not a.get('bicho') or w['distancia'] or livre: return None\n", "    if not (a.get('bicho') or a.get('povo')) or w['distancia'] or livre: return None\n")
troca('a praga e o brado', "    bon = esp['acerto'] if esp else 0; df = 0\n",
      "    bon = esp['acerto'] if esp else 0; df = 0\n"
      "    if a.get('maldito'): bon += TC.MAU_OLHADO['acerto']\n    if e.get('maldito'): df += TC.MAU_OLHADO['defesa']\n    if a.get('brado'): bon += TC.BRADO['acerto']\n")
troca('o veneno não pega em quem não tem vida', "        if tem(a, 'veneno'):\n", "        if tem(a, 'veneno') and not tem(e, 'sem vida'):\n")
troca('ninguém agarra quem não tem corpo', "        if tem(a, 'agarra') and a['estado'] == 'pe' and dist(a, e) <= 1 and e.get('ocupa', 1) <= a['ocupa'] and not any(",
      "        if tem(a, 'agarra') and a['estado'] == 'pe' and dist(a, e) <= 1 and e.get('ocupa', 1) <= a['ocupa'] and not tem(e, 'imaterial') and not w.get('distancia') and not any(")
# --- a ferida, a queda, a moral ---
troca('quem não tem vida não sangra', "sangra = grave or bool(w['efeitos'].get('sangra'))\n", "sangra = (grave or bool(w['efeitos'].get('sangra'))) and not tem(e, 'sem vida')\n")
troca('... nem perde o fôlego', "    elif parte == 'tronco': e['fol'] = max(0, e['fol'] - T.FERIDAS['tronco'][g]); sangra = True; txt += 'perde o fôlego'\n",
      "    elif parte == 'tronco' and tem(e, 'sem vida'): txt += 'não sente'\n"
      "    elif parte == 'tronco': e['fol'] = max(0, e['fol'] - T.FERIDAS['tronco'][g]); sangra = True; txt += 'perde o fôlego'\n")
troca('quem não tem vida se desfaz', "    macico = dano > e['pvmax'] * 0.5\n", "    macico = dano > e['pvmax'] * 0.5 or tem(e, 'sem vida')\n")
troca('morto o chefe que os ergueu, os mortos caem', "    _para(S, e, f\"{e['nome']} {'morreu' if macico else 'caiu'}\")\n",
      "    _para(S, e, f\"{e['nome']} {'morreu' if macico else 'caiu'}\")\n    if e.get('desfaz'): _desfaz(S, e)\n")
troca('o susto das artes', "cd = T.MORAL[motivo] if motivo in T.MORAL else TB.PAVOR if motivo == 'pavor' else TB.MORAL[motivo]",
      "cd = T.MORAL[motivo] if motivo in T.MORAL else TB.PAVOR if motivo == 'pavor' else S['cd_j'][motivo] if motivo in S.get('cd_j', {}) else TB.MORAL[motivo]")
troca('o brado dá coragem', "    bon += T.MORAL_MAIS if meus > deles else T.MORAL_MENOS if deles >= 2 * meus else 0\n",
      "    bon += T.MORAL_MAIS if meus > deles else T.MORAL_MENOS if deles >= 2 * meus else 0\n    if f.get('brado'): bon += TC.BRADO['coragem']\n")
# --- andar ---
troca('quem não tem corpo atravessa a linha', "        if larg or not avanca: return ''\n        if _no_ar(S, f): return 'contorna'",
      "        if (larg and not tem(f, 'imaterial')) or not avanca: return ''\n        if _no_ar(S, f) or tem(f, 'imaterial'): return 'contorna'")
troca('... e não dá as costas a ninguém', "    if colados and not _no_ar(S, f):  ", "    if colados and not _no_ar(S, f) and not tem(f, 'imaterial'):  ")
# --- decidir e agir ---
troca('o chefe escolhe a arte', "    if f['chao']: return ('levanta',)\n    colado = any(dist(f, e) <= 1 for e in inimigos(S, f))\n",
      "    if f['chao']: return ('levanta',)\n"
      "    if f.get('artes'):\n        x = _arte(S, f)\n        if x: return ('arte', x)\n"
      "    if f.get('fica') and f['fase'] < 1 and not any(dist(f, e) <= f['fica'] for e in inimigos(S, f)) and len(de_pe(S, f['lado'])) * 2 > len([x for x in S['L'] if x['lado'] == f['lado']]): return ('espera',)\n"
      "    colado = any(dist(f, e) <= 1 for e in inimigos(S, f))\n")
troca('quem não tem vida não faz o esforço', "    custos = [1] if zerado else [1] * T.ACOES + list(f['esforcos'])\n", "    custos = [1] if zerado else [1] * T.ACOES + ([] if tem(f, 'sem vida') else list(f['esforcos']))\n")
troca('o começo do turno', "    if f.get('bicho'): _turno_do_bicho(S, f)\n    if f['atordoado']:\n", "    if f.get('bicho'): _turno_do_bicho(S, f)\n    _comeco_j(S, f)\n    if f['atordoado']:\n")
troca('a arte anunciada sai; a arte custa a ação', "        ac = _decide(S, f, pagou); w = arma_de(S, f)\n",
      "        if f.get('prepara') and feitas == 0 and not f['chao']: ac = ('arte', next(x for x in f['artes'] if x['nome'] == f['prepara']), True)\n"
      "        else: f['feitas_t'] = feitas; ac = _decide(S, f, pagou)\n"
      "        w = arma_de(S, f)\n")
troca('fazer a arte', "        elif ac[0] == 'golpe':\n            golpe(S, f, ac[1], w)", "        elif ac[0] == 'arte':\n            _faz_arte(S, f, ac[1], agora=len(ac) > 2)\n            if len(ac) <= 2 and (ac[1].get('acoes', 1) >= 2 or ac[1].get('prepara')): _fim(S); break\n        elif ac[0] == 'golpe':\n            golpe(S, f, ac[1], w)")
troca('a recarga do sopro muda com a fase', "f['sopro_r'] = TB.SOPRO['recarga']; diz(S, f\"  {f['nome']} SOPRA\")", "f['sopro_r'] = f.get('sopro_rec', TB.SOPRO['recarga']); diz(S, f\"  {f['nome']} SOPRA\")")
troca('o escuro chamado acaba', "    S['sem_parada'] = 0 if S['houve_parada'] else S['sem_parada'] + 1\n",
      "    if S.get('escuro_r'):\n        S['escuro_r'] -= 1\n        if S['escuro_r'] <= 0 and 'escuro' in S['tempo']: S['tempo'].remove('escuro'); diz(S, '  o escuro chamado se desfaz')\n"
      "    S['sem_parada'] = 0 if S['houve_parada'] else S['sem_parada'] + 1\n")

NOVO = r'''

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
'''
out = src; linhas = 0
for rot, de, para in R:
    n = out.count(de)
    if n != 1: raise SystemExit(f'REMENDO "{rot}": o trecho aparece {n} vez(es) no luta.py (tinha de ser uma). O luta.py mudou?')
    out = out.replace(de, para); linhas += 0 if de == para else max(de.count('\n'), 1)
i = out.index("# ---------- o simulador (o banco de provas usa) ----------")
out = out[:i] + NOVO.strip('\n') + '\n\n\n' + out[i:]
open(os.path.join(AQUI, 'luta_j.py'), 'w', encoding='utf-8').write(out)
print(f'luta_j.py escrito: {len(R)} remendos, {linhas} linhas do luta.py tocadas, {NOVO.count(chr(10))} linhas novas')
