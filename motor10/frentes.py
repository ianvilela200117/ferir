#!/usr/bin/env python3
"""frentes.py — MOTOR 10, ETAPA FINAL: AS FRENTES. Doze no Dia 1 (4 ameaças, 4 ambições, 2 faltas, 2 mistérios), mais a calamidade; outras nascem do chão por limiar
(o celeiro baixo faz a fome) e da morte do personagem (o nêmesis). Cada uma tem dono, meta e um RELÓGIO DE 6 PASSOS; cada passo muda número (fecha estrada, mata gente,
leva prata, esvazia celeiro) e manda o sinal pela notícia. O relógio é oculto: o personagem vê os sinais que chegaram, e investiga para saber mais (um campo por vez).
Por semana, cada frente rola contra a resistência do lugar. A MISSÃO CUMPRIDA CONTRA ELA tira um passo (qualquer um pode cumprir); de volta ao zero, está barrada.
Morto o dono, limpa a masmorra, investigado o mistério: barrada. O passo 6 é o desfecho, sem volta. A janela do mundo conta o fim de cada uma.

  python3 frentes.py ver                    as frentes que o personagem conhece (pelos sinais que chegaram aonde ele está), com o que já descobriu
  python3 frentes.py investigar FID         investiga (um bloco; Percepção e manha contra a frente): abre o próximo campo oculto (o passo, o dono, a meta, onde)
  python3 frentes.py mestre                 SÓ O MESTRE: todas, com o relógio, o dono e o que cada passo faz
"""
import sys
import tabelas as T
import tabelas_mundo as M
import tabelas_regiao as R
import estado


def tem(E): return bool((E.get('mundo') or {}).get('meta'))
def todas(E): return E['mundo'].get('frentes') or {}
def ativas(E): return {k: f for k, f in todas(E).items() if not f.get('fim')}


def _dono_nome(E, dono):
    k, _, v = str(dono).partition(':')
    if dono in E['gente']: return 'de ' + E['gente'][dono]['nome']
    if k == 'covil': return f"da toca {estado.de(E, v)}" if v in E['lugares'] else 'da toca'
    if k == 'chefe': return estado.de(E, E['lugares'][v]['masmorra']) if v in E['lugares'] else 'da masmorra'
    if k == 'dragao': d = (E['lugares'].get(v) or {}).get('dragao') or {}; n = d.get('nome', 'o dragão'); return n.split(' ', 1)[1] if n.split(' ', 1)[0] in ('o', 'a') and ' ' in n else n
    if k == 'casa': return f"dos {(E['mundo'].get('casas') or {}).get(v, {}).get('nome', v)[3:]}"
    if k == 'guilda': return estado.de_nome((E['mundo'].get('guildas') or {}).get(v, {}).get('nome', v))
    if k == 'lugar': return estado.de(E, v) if v in E['lugares'] else ''
    if k == 'esp': esp, _, er = v.partition('@'); return estado.de(E, er) if er in E['lugares'] else ''
    if k == 'masmorra': return estado.de(E, v) if v in E['lugares'] else ''
    return str(dono)


def vivo_dono(E, f):
    """o dono da frente ainda está lá? (a pessoa viva, a toca com gente, o chefe vivo, o dragão no covil, a casa viva, a guilda com gente, a criatura no ermo)"""
    d = f['dono']; k, _, v = str(d).partition(':')
    if d in E['gente']: return E['gente'][d]['estado'] == 'vivo'
    if k == 'covil': return bool(((E['lugares'].get(v) or {}).get('covil') or {}).get('cabecas', 0) > 0 or ((E['lugares'].get(v) or {}).get('bichos') or {}).get(f.get('especie') or 'goblin', 0) > 0)
    if k == 'chefe': ch = (E['lugares'].get(v) or {}).get('chefe') or {}; return bool(ch.get('vivo', False))
    if k == 'dragao': return isinstance((E['lugares'].get(v) or {}).get('dragao'), dict)
    if k == 'casa': return bool((E['mundo'].get('casas') or {}).get(v, {}).get('viva')) and any(g.get('casa') == v and g['estado'] == 'vivo' for g in E['gente'].values())
    if k == 'guilda': return any(g.get('guilda') == v and g['estado'] == 'vivo' for g in E['gente'].values())
    if k == 'esp': esp, _, er = v.partition('@'); return ((E['lugares'].get(er) or {}).get('bichos') or {}).get(esp, 0) > 0
    return True


def nasce(E, molde, dono, onde, alvo=None, cat=1, ermo=None, estrada=None, especie=None, texto=None, tipo_ev='frente', forca=None, mais=None):
    """faz nascer uma frente (um evento; o nascimento é segredo do Mestre: o primeiro sinal é o passo 1). Devolve o id."""
    tp, nome, meta, passos, efeitos, alvo_m, barra = R.FRENTES[molde]
    W = E['mundo']; n = ((W.get('seq') or {}).get('frente') or 0) + 1; fid = f'f{n:02d}'
    rs = estado.sorte(E, f'frente|{fid}|nasce')
    reg = dict(nome=nome.format(dono=_dono_nome(E, dono)).replace('  ', ' '), publico=f"{passos[0].split(':')[0]} {estado.em(E, onde)}", tipo=tp, molde=molde, dono=dono, onde=onde,
               meta=meta, passo=0, forca=forca if forca is not None else rs.randint(*R.FRENTE_ROLA['forca']) + (R.FRENTE_ROLA['ambicao'] if tp == 'ambição' else 0), passos=list(passos), fim=None, desde=E['relogio']['dia'], ult=None,
               alvo_missao=alvo_m, alvo=alvo, cat=cat, barra=barra)
    if ermo: reg['ermo'] = ermo
    if estrada: reg['estrada'] = estrada
    if especie: reg['especie'] = especie
    reg.update(mais or {})
    estado.aplica(E, tipo_ev, [['mundo', 'seq', 'frente', 'soma', 1], ['mundo', 'frentes', fid, 'poe', reg]], onde=onde, texto=texto or f"nasce a frente {fid}: {reg['nome']} (segredo do Mestre)")
    return fid


def _janela(E, onde, texto):
    import noticias
    return [['mundo', 'janela', 'junta', dict(dia=E['relogio']['dia'], texto=texto)]] + noticias.nova(E, onde, texto, 3, ('janela',), janela=True)


def _efeitos(E, fid, f, k):
    """os verbos do passo k, feitos em efeitos do gravador (o que não cabe, fica de fora)"""
    import regiao, missoes
    onde = f['onde']; l = E['lugares'][onde]; ef = []; txt = []; rs = estado.sorte(E, f'frente|{fid}|passo|{k}')
    for v in R.FRENTES[f['molde']][4][k - 1]:
        verbo = v[0]
        if verbo == 'estoque':
            q = int(l['estoque'].get(v[1], 0) * v[2])
            if q: ef.append(['estoque', onde, v[1], 'soma', q])
        elif verbo == 'prata':
            q = int(l['estoque'].get('prata', 0) * -v[1])
            if q > 0:
                ef.append(['estoque', onde, 'prata', 'soma', -q])
                if f['dono'] in E['gente'] and E['gente'][f['dono']]['estado'] == 'vivo': ef.append(['pessoa', f['dono'], 'moedas', 'soma', q])
                else: ef.append(['estoque', f.get('ermo') or f.get('estrada') or onde, 'prata', 'soma', q]) if (f.get('ermo') or f.get('estrada')) else ef.pop()
        elif verbo == 'povo':
            pop = l.get('pop') or 0; q = int(pop * v[1])
            if q and pop + q > 0:
                ef.append(['lugar', onde, 'pop', 'soma', q]); ef += [['lugar', onde, 'produz.' + b, 'poe', x] for b, x in regiao._escala_produz(l, (pop + q) / pop)]
        elif verbo in ('rota', 'bando'):
            e = f.get('estrada') or next((x for x, o in regiao.estradas(E, onde)), None)
            if e and verbo == 'rota': ef.append(['lugar', e, 'fechada', 'poe', dict(por=f['nome'], dia=E['relogio']['dia']) if v[1] == 'fecha' else None])
            elif e: ef.append(['lugar', e, 'bando', 'soma', min(v[1], R.BANDO_TETO - E['lugares'][e].get('bando', 0))]) if E['lugares'][e].get('bando', 0) < R.BANDO_TETO else None
        elif verbo == 'bichos':
            er = f.get('ermo'); b = (E['lugares'].get(er) or {}).get('bichos') or {}
            if not er or not b: continue
            esp = f.get('especie') if f.get('especie') in b else max(b, key=lambda x: b[x])
            q = v[1] if v[1] > 0 else -min(-v[1], int(b.get(esp, 0)))
            if q > 0: ef += [['lugar', er, f'teto.{esp}', 'soma', q], ['lugar', er, f'bichos.{esp}', 'soma', q]]
            elif q < 0: ef.append(['lugar', er, f'bichos.{esp}', 'soma', q])
        elif verbo == 'vagantes':
            m = f.get('alvo') if (E['lugares'].get(f.get('alvo')) or {}).get('tipo') == 'masmorra' else None
            if m: ef.append(['lugar', m, 'vagantes.esqueleto', 'soma', v[1]])
        elif verbo == 'produz':
            q = (l.get('produz') or {}).get(v[1])
            if isinstance(q, (int, float)): ef.append(['lugar', onde, f'produz.{v[1]}', 'poe', round(q * v[2], 4)])
        elif verbo == 'morre':
            cands = [x for x, g in E['gente'].items() if g.get('papel') == v[1] and g['lugar'] == onde and g['estado'] == 'vivo' and not g.get('jogador') and not estado.fora(E, x) and x != f['dono']]
            if cands:
                x = rs.choice(sorted(cands)); ef.append(['pessoa', x, 'estado', 'poe', 'morto']); txt.append(f"{E['gente'][x]['nome']} morreu")
        elif verbo == 'fama':
            if f['dono'] in E['gente'] and E['gente'][f['dono']]['estado'] == 'vivo': ef.append(['pessoa', f['dono'], 'fama', 'soma', v[1]])
            elif str(f['dono']).startswith('guilda:'):
                g = str(f['dono']).split(':', 1)[1]
                if g in (E['mundo'].get('guildas') or {}): ef.append(['mundo', 'guildas', g, 'fama', 'soma', v[1]])
        elif verbo == 'acorda':
            s = str(f['dono']).split(':', 1)[1]; d = dict((E['lugares'].get(s) or {}).get('dragao') or {})
            if d: d['dorme_ate'] = None; d['vila'] = onde; d['fama'] = sorted(set((d.get('fama') or []) + [onde])); ef.append(['lugar', s, 'dragao', 'poe', d])
        elif verbo == 'casa':
            cid = str(f['dono']).split(':', 1)[1]; cap = next((x for x, y in E['lugares'].items() if y.get('tipo') == 'capital'), None)
            if cap and cid in (E['mundo'].get('casas') or {}): ef += [['lugar', cap, 'casa', 'poe', cid]]
    return ef, txt


def passo(E, fid, porque='a semana'):
    """a frente anda um passo: os efeitos dele, o sinal na notícia; o sexto é o desfecho (e a janela do mundo)"""
    import noticias
    f = todas(E)[fid]; k = f['passo'] + 1; ef, txt = _efeitos(E, fid, f, k)
    sinal = f['passos'][k - 1]; sinal_txt = f"{sinal[0].upper() + sinal[1:]} {estado.em(E, f['onde'])}" + (f" ({'; '.join(txt)})" if txt else '')
    ef += [['mundo', 'frentes', fid, 'passo', 'poe', k], ['mundo', 'frentes', fid, 'ult', 'poe', E['relogio']['dia']]] + noticias.nova(E, f['onde'], sinal_txt, 2, ('frente', fid), ja=ef)
    if k >= M.FRENTE_PASSOS: ef += [['mundo', 'frentes', fid, 'fim', 'poe', 'desfecho']] + _janela(E, f['onde'], f"{f['nome'][0].upper() + f['nome'][1:]}: {sinal}. Não tem volta.")
    estado.aplica(E, 'frente', ef, onde=f['onde'], texto=f"a frente {fid} ({f['nome']}) anda ao passo {k}: {sinal}")
    if k >= M.FRENTE_PASSOS and f['molde'] == 'guilda':
        try: import rivais; rivais.limpa_da_guilda(E, str(f['dono']).split(':', 1)[1], f.get('alvo'))
        except (ModuleNotFoundError, AttributeError): pass
    if k >= M.FRENTE_PASSOS: _abre_estradas(E, fid)


def _abre_estradas(E, fid):
    f = todas(E)[fid]; ef = [['lugar', e, 'fechada', 'poe', None] for e, l in E['lugares'].items() if isinstance(l, dict) and isinstance(l.get('fechada'), dict) and l['fechada'].get('por') == f['nome']]
    if ef and f.get('fim') == 'barrada': estado.aplica(E, 'frente', ef, onde=f['onde'], texto=f"com a frente {fid} barrada, a estrada abre de novo")


def barra(E, fid, porque):
    f = todas(E)[fid]
    if f.get('fim'): return
    estado.aplica(E, 'frente', [['mundo', 'frentes', fid, 'fim', 'poe', 'barrada']] + _janela(E, f['onde'], f"{f['nome'][0].upper() + f['nome'][1:]} acabou: {porque}."), onde=f['onde'], texto=f"a frente {fid} é barrada: {porque}")
    _abre_estradas(E, fid)


def recua(E, fid, porque):
    """a missão contra a frente foi cumprida: um passo atrás; no zero (tendo andado), barrada"""
    f = todas(E).get(fid)
    if not f or f.get('fim'): return
    if f['passo'] <= 1: return barra(E, fid, porque)
    estado.aplica(E, 'frente', [['mundo', 'frentes', fid, 'passo', 'soma', -1]], onde=f['onde'], texto=f"a frente {fid} recua um passo: {porque}")


def _barrada(E, fid, f):
    """o que barra a frente sem missão: o dono que caiu, a masmorra limpa, o mistério investigado, o celeiro farto"""
    b = f.get('barra')
    if b in ('dono', 'covil', 'chefe', 'dragao') and not vivo_dono(E, f): return 'o dono dela caiu'
    if b in ('chefe', 'limpa'):
        m = f.get('alvo'); lp = (E['lugares'].get(m) or {}).get('limpa') if m else None
        if lp:
            if b == 'limpa' and str(f['dono']).startswith('guilda:') and any(E['gente'].get(q, {}).get('guilda') == str(f['dono']).split(':', 1)[1] for q in lp.get('quem') or []): return None
            return 'a masmorra foi limpa'
    if b == 'investigado':                                  # o personagem abriu três campos, ou alguém (um rival) a expôs
        oc = E['mundo'].get('oculto') or {}
        if f.get('exposta') or sum(1 for c in oc if c.startswith(f'frente.{fid}.')) >= 3: return 'o que ela escondia veio à luz'
    if b == 'farto':
        import regiao
        if regiao.dias_de_comida(E, f['onde']) > 30: return 'o celeiro encheu de novo'
    return None


def virada(E):
    if not tem(E): return
    hoje = E['relogio']['dia']; FR = R.FRENTE_ROLA
    for fid, f in list(ativas(E).items()):
        pq = _barrada(E, fid, f)
        if pq: barra(E, fid, pq); continue
        cada = FR['calamidade_cada'] if f['tipo'] == 'calamidade' else M.SEMANA
        if (hoje - f['desde']) % cada != 0 or hoje == f['desde']: continue
        rs = estado.sorte(E, f'frente|{fid}|rola|{hoje}'); l = E['lugares'][f['onde']]
        t = sum(rs.randint(1, FR['dado'][1]) for _ in range(FR['dado'][0])) + f['forca']
        contra = FR['contra'] + (l.get('resiste') or 0) + (l.get('guarda') or 0) // FR['resiste_guarda']
        if t >= contra: passo(E, fid)


def limiar_fome(E, lid, dias):
    """o chão faz nascer a frente: o celeiro abaixo do limiar, e nenhuma fome andando ali"""
    if dias >= R.FOME_DIAS or any(f['molde'] == 'fome' and f['onde'] == lid for f in ativas(E).values()): return
    nasce(E, 'fome', f'lugar:{lid}', lid, alvo='comida', cat=0, texto=f"o celeiro {estado.de(E, lid)} baixou do limiar: nasce a fome")


def nemesis(E, morto, matador, onde):
    """quem matou o personagem fica com o que ele vestia e vira a frente pessoal do herdeiro"""
    return nasce(E, 'nêmesis', matador, onde, alvo=matador, cat=2, forca=4, texto=f"o matador de {E['gente'][morto]['nome']} vira o nêmesis da casa dele")


# ---------- o Dia 1 ----------
def gera(E, r):
    """as frentes do Dia 1, tiradas do mundo que o gerador fez (o pior bando, a toca maior, o chefe dos mortos, o dragão jovem, a casa ambiciosa, o mercador, o culto,
    a guilda mais forte, a vila que seca, o posto da mina, a aldeia dos sumiços, as ruínas das luzes, e o que dorme)"""
    import regiao, noticias, itens, pessoas, talento, vila_teste, nomes
    Ls = E['lugares']; G = E['gente']; feitas = []
    pov = regiao.povoados(E)
    def perto_de(lid):
        if lid in pov: return lid
        return noticias.origem(E, lid) or pov[0]
    # 1 o bando: a estrada com mais salteadores; o chefe nasce no ermo por onde ela passa (ou na ponta dela)
    est = max((e for e in Ls if Ls[e].get('tipo') == 'estrada'), key=lambda e: (Ls[e].get('bando', 0), Ls[e]['longe']))
    mora = Ls[est].get('passa') or Ls[est]['ponta'][0]; N = nomes.Nomes(r, usados=[g['nome'] for g in G.values()]); nome = N.gente('humano')
    pid = 'chefe_' + nomes._sem_acento(nome).replace(' ', '_')
    at = pessoas.padrao(nome, 28, molde='guerreiro')['atributos']; reg = talento.nasce(E, pid, dict(nome=nome, nivel=28, atributos=at, lugar=mora, grau_oficio='oficial', maestria={'lança': 4}, treino=vila_teste.treino_da_mao({'lança': 4}), moedas=r.randint(40, 90), sobre='o chefe dos salteadores da estrada', papel='ladino'))
    s0 = E['itens']['seq']
    estado.aplica(E, 'gera', [['pessoa', 'nasce', pid, reg], ['item', 'nasce', itens.item('arma', 1, f'Lança de {nome}', familia='lança', dono=pid)], ['item', 'nasce', itens.item('armadura', 0, f'Malha de {nome}', material='malha', dono=pid)],
                              ['item', f'i{s0 + 1:04d}', 'uso', 'poe', 'arma'], ['item', f'i{s0 + 2:04d}', 'uso', 'poe', 'veste']], onde=mora, quem=[pid], texto=f"{nome}, o chefe dos salteadores")
    feitas.append(nasce(E, 'bando', pid, Ls[est]['ponta'][0], alvo=pid, cat=1, estrada=est, ermo=Ls[est].get('passa')))
    if True: pass
    # 2 a horda: a toca de criatura maior
    covis = [(k, l['covil']) for k, l in Ls.items() if isinstance(l.get('covil'), dict)]
    if covis:
        k, c = max(covis, key=lambda x: x[1].get('cabecas', 0)); esp = c.get('especie') or next(iter(Ls[k].get('bichos') or {'goblin': 1}))
        feitas.append(nasce(E, 'horda', f'covil:{k}', perto_de(k), alvo=esp, cat=1, ermo=k, especie=esp))
    # 3 os mortos: a masmorra com necromante ou guardião
    for sid, s in Ls.items():
        ch = s.get('chefe') if isinstance(s, dict) else None
        if isinstance(ch, dict) and ch.get('vivo') and ch.get('qual') in ('necromante', 'guardião da cripta'):
            m = s['masmorra']; feitas.append(nasce(E, 'mortos', f'chefe:{sid}', perto_de(m), alvo=m, cat=Ls[m]['niveis'][-1]['cat'])); break
    # 4 o dragão jovem
    for k, l in Ls.items():
        d = l.get('dragao') if isinstance(l, dict) else None
        if isinstance(d, dict) and d.get('vila') and not d.get('dorme_ate'):
            feitas.append(nasce(E, 'dragão', f'dragao:{k}', d['vila'], alvo=f'dragao:{k}', cat=2, ermo=k)); break
    # 5 o trono: a casa nobre viva mais forte que não é a do rei
    rei = (E['mundo'].get('reinos') or {}).get('r_hoje', {}).get('casa')
    vass = [cid for cid, c in (E['mundo'].get('casas') or {}).items() if c.get('tipo') == 'nobre' and c.get('viva') and cid != rei and any(g.get('casa') == cid and g['estado'] == 'vivo' for g in G.values())]
    if vass:
        cid = r.choice(sorted(vass)); feitas.append(nasce(E, 'trono', f'casa:{cid}', E['mundo']['casas'][cid]['sede'], alvo=f'casa:{cid}', cat=2))
    # 6 o cartel: o mercador mais rico de uma cidade
    merc = [k for k, g in G.items() if g.get('papel') == 'mercador' and Ls[g['lugar']].get('tipo') in ('cidade', 'capital') and g['estado'] == 'vivo']
    if merc:
        k = max(merc, key=lambda x: G[x]['moedas']); feitas.append(nasce(E, 'cartel', k, G[k]['lugar'], alvo=k, cat=1))
    # 7 o culto: alguém da capital (ninguém sabe quem)
    cap = next(k for k in pov if Ls[k]['tipo'] == 'capital')
    cult = [k for k, g in G.items() if g['lugar'] == cap and g.get('papel') in ('escriba', 'bardo', 'mercador', 'taverneiro', 'curandeiro') and g['estado'] == 'vivo']
    if cult: k = r.choice(sorted(cult)); feitas.append(nasce(E, 'culto', k, cap, alvo=k, cat=2))
    # 8 a guilda: a de mais fama, atrás da masmorra funda que ninguém limpou
    gs = E['mundo'].get('guildas') or {}
    funda = sorted((k for k, l in Ls.items() if l.get('tipo') == 'masmorra' and l.get('molde') in ('ruína', 'mina', 'cripta') and not l.get('limpa')), key=lambda k: -Ls[k]['niveis'][-1]['cat'])
    if gs and funda:
        g = max(gs, key=lambda x: gs[x].get('fama', 0)); feitas.append(nasce(E, 'guilda', f'guilda:{g}', perto_de(funda[0]), alvo=funda[0], cat=Ls[funda[0]]['niveis'][-1]['cat']))
    # 9 a seca: a vila que mais produz comida; 10 a mina: o posto
    vilas = [k for k in pov if Ls[k]['tipo'] in ('vila', 'aldeia')]
    if vilas: k = max(vilas, key=lambda x: (Ls[x].get('produz') or {}).get('comida', 0)); feitas.append(nasce(E, 'seca', f'lugar:{k}', k, alvo='comida', cat=0))
    postos = [k for k in pov if Ls[k]['tipo'] == 'posto']
    if postos: k = r.choice(sorted(postos)); feitas.append(nasce(E, 'mina', f'lugar:{k}', k, alvo='ferramenta', cat=0))
    # 11 os sumiços: uma aldeia; o que leva a gente é um lobisomem posto no ermo vizinho
    ald = [k for k in pov if Ls[k]['tipo'] == 'aldeia']
    if ald:
        k = r.choice(sorted(ald)); er = next((v for v in Ls[k].get('vizinhos') or [] if Ls.get(v, {}).get('tipo') == 'ermo'), None)
        if er:
            estado.aplica(E, 'gera', [['lugar', er, 'teto.lobisomem', 'soma', 1], ['lugar', er, 'bichos.lobisomem', 'soma', 1]], onde=er, texto='um lobisomem no ermo (segredo do Mestre)')
            feitas.append(nasce(E, 'sumiços', f'esp:lobisomem@{er}', k, alvo='lobisomem', cat=2, ermo=er, especie='lobisomem'))
    # 12 as luzes: uma ruína
    ru = [k for k, l in Ls.items() if l.get('tipo') == 'masmorra' and l.get('molde') == 'ruína']
    if ru: k = r.choice(sorted(ru)); feitas.append(nasce(E, 'luzes', f'masmorra:{k}', perto_de(k), alvo=k, cat=2, ermo=next((v for v in Ls[k].get('vizinhos') or [] if Ls.get(v, {}).get('tipo') == 'ermo'), None)))
    # 13 a calamidade: o que dorme no covil
    for sid, s in Ls.items():
        d = s.get('dragao') if isinstance(s, dict) else None
        if isinstance(d, dict) and d.get('dorme_ate') and d.get('idade') == 'ancião':
            m = s['masmorra']; er = next((v for v in Ls[m].get('vizinhos') or [] if Ls.get(v, {}).get('tipo') == 'ermo'), None)
            feitas.append(nasce(E, 'calamidade', f'dragao:{sid}', perto_de(m), alvo=m, cat=5, ermo=er, forca=3)); break
    return [f"As frentes do Dia 1: {len(feitas)} (" + ', '.join(todas(E)[f]['nome'] for f in feitas) + ')']


# ---------- o que se sabe ----------
def sabe(E, pid, fid):
    oc = E['mundo'].get('oculto') or {}
    return [c.split('.')[-1] for c in oc if c.startswith(f'frente.{fid}.')]


def conhecidas(E, pid):
    """as frentes de que chegou sinal (notícia) ao lugar onde a pessoa está, ou que ela já investigou"""
    lid = E['gente'][pid]['lugar']; out = {}
    for n in (E['mundo'].get('noticias') or {}).values():
        tags = n.get('tags') or []
        if 'frente' in tags and lid in n.get('chegou', {}):
            fid = next((t for t in tags if t in todas(E)), None)
            if fid: out[fid] = max(out.get(fid, 0), n['dia'])
    for c in (E['mundo'].get('oculto') or {}):
        if c.startswith('frente.'): out.setdefault(c.split('.')[1], 0)
    return out


def diz(E, pid, fid):
    f = todas(E)[fid]; s = sabe(E, pid, fid)
    L = [f"{fid} · {f['nome'] if 'dono' in s else f['publico']}" + (f" ({'barrada' if f['fim'] == 'barrada' else 'chegou ao fim'})" if f.get('fim') else '')]
    if 'passo' in s: L.append(f"o relógio: passo {f['passo']} de 6")
    if 'meta' in s: L.append(f"quer {f['meta']}")
    if 'onde' in s: L.append(f"o centro dela: {E['lugares'][f['onde']]['nome']}")
    return ' · '.join(L)


def investigar(E, pid, fid):
    import ato, corpo
    p = estado.presente(E, pid, 'investigar'); f = todas(E).get(fid) or sys.exit(f'não há a frente "{fid}"')
    if fid not in conhecidas(E, pid): sys.exit(f'{p["nome"]} não sabe dessa frente (nenhum sinal dela chegou {estado.em(E, p["lugar"])})')
    falta = [c for c in R.INVESTIGA['campos'] if c not in sabe(E, pid, fid)]
    if not falta: sys.exit('já se sabe tudo o que dá para saber dela')
    rs = estado.sorte(E, f'investiga|{pid}|{fid}|{estado.agora(E)}'); ma = (p.get('maestria') or {}).get('manha', 0)
    t = rs.randint(1, 20) + rs.randint(1, 20) + p['atributos']['Percepção'] // 10 + ma + corpo.pena(p, estado.agora(E)); contra = R.INVESTIGA['contra'] + R.INVESTIGA['cat'] * f.get('cat', 1)
    ok = t >= contra; c = falta[0]
    ato.passa(E, pid, 1, 'investigar', esforco='leve', texto=f"{p['nome']} investiga {f['publico']}", mais=lambda i: [['mundo', 'oculto', f'frente.{fid}.{c}', 'poe', E['relogio']['dia']]] if ok else [])
    return f"Investigou ({t} contra {contra}): " + (f"descobriu {dict(passo='o relógio dela', dono='quem está por trás', meta='o que ela quer', onde='o centro dela')[c]}. {diz(E, pid, fid)}" if ok else 'não achou nada de novo.')


def mesa(E):
    if not tem(E): return []
    eu = estado.eu(E)
    if not eu or E['gente'][eu]['estado'] != 'vivo' or estado.fora(E, eu): return []
    k = conhecidas(E, eu)
    return ['**As frentes que você conhece** (pelos sinais; `frentes.py investigar FID`):'] + [f"- {diz(E, eu, f)}" for f in sorted(k, key=lambda x: -k[x])[:5]] if k else []


def so_mestre(E):
    if not tem(E): return []
    return ['as frentes: ' + ' · '.join(f"{k} {f['nome']} (passo {f['passo']}" + (f", {f['fim']}" if f.get('fim') else '') + ')' for k, f in todas(E).items())]


if __name__ == '__main__':
    import signal; hasattr(signal, 'SIGPIPE') and signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    a = sys.argv[1:]
    if not a or a[0] not in ('ver', 'investigar', 'mestre'): print(__doc__); sys.exit()
    E = estado.carrega(); eu = estado.eu(E)
    if a[0] == 'ver':
        if not eu: sys.exit('não há personagem')
        print('\n'.join(mesa(E)) or 'nenhum sinal de frente chegou aqui.')
    elif a[0] == 'investigar':
        if len(a) != 2: sys.exit('use: `frentes.py investigar FID`')
        print(investigar(E, eu, a[1])); estado.grava(E)
    else:
        for k, f in todas(E).items():
            print(f"{k} · {f['nome']} [{f['molde']}, {f['tipo']}] · passo {f['passo']}/6 · força {f['forca']} · em {E['lugares'][f['onde']]['nome']} · dono {f['dono']}" + (f" · {f['fim']}" if f.get('fim') else ''))
            for i, s in enumerate(f['passos'], 1): print(f"   {'>' if i == f['passo'] + 1 else ' '} {i}. {s}")
