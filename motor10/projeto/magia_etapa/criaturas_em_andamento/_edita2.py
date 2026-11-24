s = open('aplica.py', encoding='utf-8').read()
def tr(de, para, n=1):
    global s
    c = s.count(de); assert c == n, (c, de[:90]); s = s.replace(de, para)
# o alvo de um só: não repete o mau-olhado em quem já o tem, nem prende quem já está preso
tr("    um = [max(al, key=lambda e: (e['nome'] == f['agressor'], -e['pv'] / e['pvmax']))] if al else []\n",
   "    cand = [e for e in al if not (t == 'maldiz' and e['maldito']) and not (t == 'prende' and e['raiz'] > 0)]\n"
   "    um = [max(cand, key=lambda e: (e['nome'] == f['agressor'], -e['pv'] / e['pvmax']))] if cand else []\n")
tr("        al = [e for e in inimigos(S, f) if dist(f, e) <= a.get('alcance', 6)]; q = a.get('quando', 'sempre')\n",
   "        al = [e for e in inimigos(S, f) if dist(f, e) <= a.get('alcance', 6)]; q = a.get('quando', 'sempre')\n"
   "        if a['tipo'] == 'maldiz' and all(e['maldito'] for e in al): continue\n"
   "        if a['tipo'] == 'prende' and not a.get('area') and all(e['raiz'] > 0 for e in al): continue\n")
# a área "na casa" (a bola de fogo da lista: até 4 na casa mais cheia); a área de assinatura pega todos ao alcance
tr("        for e in (al if a.get('area') else um):\n            if f['estado'] != 'pe' or e['estado'] != 'pe': continue\n            golpe(S, f, e, w, livre=a['nome']); v = S.get('ult')\n",
   "        if a.get('casa') and al: xs = max({e['x'] for e in al}, key=lambda x: sum(1 for e in al if e['x'] == x)); al = [e for e in al if e['x'] == xs][:a['casa']]\n"
   "        for e in (al if a.get('area') else um):\n            if f['estado'] != 'pe' or e['estado'] != 'pe': continue\n            golpe(S, f, e, w, livre=a['nome']); v = S.get('ult')\n")
tr("    elif r == 'queima' and not tem(e, 'sem vida'): q = max(1, int(dano * T.SANGRA))", "    elif r == 'queima' and not tem(e, 'sem vida') and dano >= e['pvmax'] * T.FERIDA: q = max(1, int(dano * T.SANGRA))")
tr("    elif r == 'veneno' and not tem(e, 'sem vida'): q = max(1, int(dano * TB.VENENO['fracao'])); ant = e['veneno'] or [0, 0]; e['veneno'] = [max(q, ant[0]), TB.VENENO['rodadas']]",
   "    elif r == 'veneno' and not tem(e, 'sem vida'): q = max(1, int(dano * a.get('fracao', TB.VENENO['fracao']))); ant = e['veneno'] or [0, 0]; e['veneno'] = [max(q, ant[0]), a.get('rodadas_v', TB.VENENO['rodadas'])]")
tr("    elif r == 'folego':", "    elif r == 'atordoa' and dano >= e['pvmax'] * T.FERIDA: e['atordoado'] = max(e['atordoado'], 1); diz(S, f\"    {e['nome']} fica atordoado\")\n    elif r == 'folego':")
open('aplica.py', 'w', encoding='utf-8').write(s); print('ok')
