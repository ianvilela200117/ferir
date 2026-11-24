import re
s = open('aplica.py', encoding='utf-8').read()
def tr(de, para, n=1):
    global s
    c = s.count(de)
    assert c == n, (c, de[:80])
    s = s.replace(de, para)
s = s.replace('incorpóreo', 'imaterial')
tr("TC.MALDITO", "TC.MAU_OLHADO", 3)
# a fresta, o material, a guarda contra a magia
tr("and not tem(e, 'couraça') and not w.get('area') and not w.get('cru') and chance(\")", "and not tem(e, 'couraça') and not w.get('area') and not w.get('cru') and not w.get('magia') and chance(\")")
tr("prot = pc['rd'] * (1 if w.get('area') or w.get('cru') else T.MATRIZ[w['golpe']][pc['material']])\")", "prot = pc['rd'] * (1 if w.get('area') or w.get('cru') or w.get('magia') else T.MATRIZ[w['golpe']][pc['material']])\")")
tr("      \"    if e.get('aco') and not _magica(w): prot *= 3 ** e['aco']",
   "      \"    if w.get('magia'): prot = _guarda_m(S, e) / (2 if j['crit'] else 1)                    # A GUARDA contra a magia (a conta da magia, B.1): o amuleto, ou 0,6 da armadura do tronco; sem material, sem parte do corpo, sem fresta\\n\"\n"
   "      \"    if e.get('aco') and not _magica(w): prot *= 3 ** e['aco']")
tr("troca('o bote e a investida de quem empunha arma',",
   "troca('o feitiço não gasta a armadura', \"    if vestida and (w['cat'] > pc['cat'] or j['crit']): _gasta_armadura(\", \"    if vestida and not w.get('magia') and (w['cat'] > pc['cat'] or j['crit']): _gasta_armadura(\")\n"
   "troca('o bote e a investida de quem empunha arma',")
# a concentração (a conta da magia, B.4)
tr("      \"    if e.get('prepara') and e['estado'] == 'pe' and dano >= e['pvmax'] * TC.CORTA: _corta(S, e)\\n\")",
   "      \"    if e.get('prepara') and e['estado'] == 'pe': _concentra(S, e, dano >= e['pvmax'] * T.FERIDA or (j['crit'] and dano >= e['pvmax'] * T.FERIDA_MIN))\\n\")")
tr("troca('a ferida corta a arte anunciada', \"    diz(S, txt); _para(S, e, f\\\"{e['nome']} levou uma ferida\", \"    if e.get('prepara'): _corta(S, e)\\n    diz(S, txt); _para(S, e, f\\\"{e['nome']} levou uma ferida\")\n", "")
# o turno: a arte de 2 ações e a longa gastam o turno
tr("      \"        else: ac = _decide(S, f, pagou)\\n\"", "      \"        else: f['feitas_t'] = feitas; ac = _decide(S, f, pagou)\\n\"")
tr("\"        elif ac[0] == 'arte': _faz_arte(S, f, ac[1], agora=len(ac) > 2)\\n        elif ac[0] == 'golpe':",
   "\"        elif ac[0] == 'arte':\\n            _faz_arte(S, f, ac[1], agora=len(ac) > 2)\\n            if len(ac) <= 2 and (ac[1].get('acoes', 1) >= 2 or ac[1].get('prepara')): _fim(S); break\\n        elif ac[0] == 'golpe':")
# o estado novo
tr("f.update(raiz=0, maldito=False, brado=0, arte_r={}, fase=0, prepara=None, arte_t=0, erguido=False, levantado=False)",
   "f.update(raiz=0, maldito=False, brado=0, arte_r={}, fase=0, prepara=None, arte_t=0, erguido=False, levantado=False, calejo=0, feitas_t=0)")
# o começo do turno: quem caiu, foi atordoado ou agarrado perde o feitiço longo sem teste
tr("    if f.get('fases'): _fase(S, f)\n\n\ndef _corta(S, e):\n",
   "    if f.get('prepara') and (f['chao'] or f['atordoado'] or _agarrado(S, f)): _corta(S, f)\n    if f.get('fases'): _fase(S, f)\n\n\n"
   "def _guarda_m(S, e):\n    \"\"\"a guarda contra a magia: o valor do amuleto, ou 0,6 do valor da armadura do tronco (o couro do bicho também), o que for maior; sem um nem outro, um terço\"\"\"\n"
   "    tr = e['partes'].get('tronco'); g = T.NU\n"
   "    if tr and inteiro(S, tr['item']): g = T.RD[tr['cat']] * (1 if tem(e, 'resiste') else TC.GUARDA_ARMADURA)\n"
   "    if e.get('amuleto') is not None: g = max(g, T.RD[e['amuleto']])\n    return g\n\n\n"
   "def _concentra(S, e, ferida):\n    \"\"\"quem canaliza um feitiço longo e leva dano testa a concentração: 2d20 + Vontade ÷ 10 + maestria contra 28 (32 se o golpe abriu ferida)\"\"\"\n"
   "    S['conc_t'] = S.get('conc_t', 0) + 1\n"
   "    if sum(d20x()) + sum(d20x()) + e['vontade_b'] + e['maestria'] < TC.CONCENTRA + (TC.CONCENTRA_FERIDA if ferida else 0): _corta(S, e)\n\n\n"
   "def _corta(S, e):\n")
# a Conjuração contra a Firmeza, com o calejo
tr("    return sum(d20x()) + sum(d20x()) + a['conj'] < e.get('firmeza', 26)\n",
   "    pega = sum(d20x()) + sum(d20x()) + a['conj'] + (TC.MAU_OLHADO['acerto'] if a.get('maldito') else 0) >= e.get('firmeza', 26) + TC.CALEJO * e.get('calejo', 0)\n"
   "    if pega: e['calejo'] = e.get('calejo', 0) + 1\n    return pega\n")
# a arte de 2 ações só sai com o turno inteiro
tr("        if f['fase'] < a.get('fase', 0) or f['fase'] > a.get('ate_fase', 9): continue\n",
   "        if f['fase'] < a.get('fase', 0) or f['fase'] > a.get('ate_fase', 9): continue\n        if (a.get('acoes', 1) >= 2 or a.get('prepara')) and f.get('feitas_t', 0) > 0: continue\n")
# lançar com inimigo colado dá golpe livre
tr("    if a.get('prepara') and not agora:\n        f['prepara'] = a['nome']",
   "    if a.get('mana') and not agora:\n        col = [e for e in inimigos(S, f) if dist(f, e) <= 1]\n        if col: _golpe_livre(S, f, 'lança com inimigo colado', quem=col)\n        if f['estado'] != 'pe': return\n"
   "    if a.get('prepara') and not agora:\n        f['prepara'] = a['nome']")
# o medo: um alvo, pela Firmeza; o grito do chefe: todos ao alcance
tr("        for e in al: _moral(S, e, 'grito ' + a['nome'])\n",
   "        for e in (um if a.get('um') else al):\n            if a.get('contra') == 'F' and not _resiste(S, f, e): diz(S, f\"    {e['nome']} resiste\"); continue\n            _moral(S, e, 'grito ' + a['nome'])\n")
open('aplica.py', 'w', encoding='utf-8').write(s)
print('ok')
