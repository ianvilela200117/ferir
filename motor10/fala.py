#!/usr/bin/env python3
"""fala.py — MOTOR 10, A PARTE 2, FASE 2: O TESTE DE FALA (o contrato: projeto/etapa_efeitos/DESENHO.md, 6.6 e a resposta 5a; o capítulo 30; os números no tabelas_habilidades.py).

O TESTE SÓ RODA NO PEDIDO QUE O JOGADOR DECLARA (a resposta 5a), EM DOIS PASSOS: `fala.py conta` mostra o degrau e a chance de cada faixa, sem rolar (e guarda no caderno do
turno o pedido que foi mostrado); `fala.py pede` só rola o pedido que foi mostrado, no mesmo bloco e com a mesma conta (senão recusa: "mostre antes"). Assim o jogador vê a
chance a tempo de desistir. A conversa comum segue como hoje, pela opinião e pela memória. O Mestre nunca rola fala pelo personagem sem a ordem dele.
  A CONTA (declarada antes, rolada uma vez pelo teste.rola): 2d20 + bônus de Vontade (no jeito duro de ameaça, de Força) + a mão do caminho (comércio no negócio; a do ofício quando
  se fala dele; fé no sermão; manha na mentira) + a opinião dele sobre você (−10 a +10; com −6 ou menos, ele não ouve pedido nenhum) + as habilidades de fala (até +8) − a pena do
  corpo, contra 22 + 6 por degrau (pequeno, médio, grande, absurdo) + metade do bônus de Vontade de quem ouve. O JEITO: manso (CD −4, nunca ofende), firme, duro (CD +4; falhar
  ofende sempre: só a Palavra Firme do Mestre salva o duro que falha por menos de 5).
  AS FAIXAS: passou por 6 ou mais, ganha e leva mais um passo · por 0 a 5, ganha com um preço (a mesa dá dois ou três e o jogador escolhe um, ou desiste) · falhou por 1 a 9, não
  ganha · por 10 ou mais (no duro, por 1 ou mais), não ganha e ofende (no manso, é só "não"). A MEMÓRIA, só pelas faixas: uma linha por conversa (a mesma pessoa, no mesmo dia):
  o que as falas do dia põem SOMA nessa linha (o −3 da ofensa depois de um +1 do manso deixa −2). O "NÃO" VALE NO DIA: depois de um "não", a mesma pessoa não ouve outro pedido do
  mesmo degrau ou menor até o dia seguinte (um maior, pode); depois de uma ofensa, nenhum.
  O PREÇO: um passo é 5 pontos no que a loja paga ou cobra, uma vez por loja por dia, nunca acima dos tetos de hoje (80% pelos bens, 60% pelas peças; na compra, nunca abaixo da
  base). Na caixa e na missão, o pedido se negocia pelo mesmo teste. A FALA DA GENTE NO PERSONAGEM só põe preço na recusa: aceitar ou recusar é sempre do jogador.

Uso (o personagem do jogador, ou quem=ID):
  python3 fala.py conta PID DEGRAU [jeito=manso|firme|duro] [caminho=negocio|oficio:OFICIO|sermao|mentira] [ameaca]     a conta e a chance de cada faixa, sem rolar (o 1º passo)
  python3 fala.py pede PID DEGRAU "o quê" [jeito=] [caminho=] [ameaca]       o pedido mostrado: o dado uma vez, a faixa, a memória, o preço (o 2º passo)
  python3 fala.py regateia BEM|ITEM [passos=1|2|3] [jeito=] [conta]          o regateio na loja daqui (pequeno, médio, grande): `conta` mostra; sem ela, rola o que foi mostrado
  python3 fala.py caixa XID prazo|paga [DEGRAU] [jeito=] [conta]             o pedido da caixa negociado (mais prazo: pequeno; mais paga: médio +25%, grande +50%)
  python3 fala.py missao MID [jeito=] [conta]                                a paga da missão +50% (pedido grande)
  python3 fala.py gente PID DEGRAU "o quê" [caminho=]                        SÓ O MESTRE: a gente do mundo pede ao personagem (o dado dela contra a Vontade dele): a mesa diz o preço de recusar
"""
import math, sys
import tabelas as T
import tabelas_habilidades as H
import estado, teste, corpo


def _n(x): return f'{x:g}'.replace('.', ',')
def _pct(x): return f"{int(100 * x + 0.5 + 1e-4)}%"            # meio para cima (7,5% → 8%; a conta do 2d20 corta a 3ª explosão, que pesa menos de 0,0001%)
def _sinal(v): return f"{v:+d}".replace('-', '−')
def degrau_de(d):
    d = (d or '').lower().replace('é', 'e')
    if d not in H.FALA_DEGRAUS: sys.exit(f'o degrau do pedido é um de: {", ".join(H.FALA_DIZ[x] for x in H.FALA_ORDEM)} (veio "{d}")')
    return d


def _jeito(j):
    j = (j or 'firme').lower()
    if j not in H.FALA_JEITOS: sys.exit(f'o jeito é manso, firme ou duro (veio "{j}")')
    return j


def _hab(p, k):
    r = (p.get('habilidades') or {}).get(k); return r.get('grau', 0) if isinstance(r, dict) else (r if isinstance(r, int) else None)


def _mao(p, caminho):
    """a mão do caminho da conversa: comércio no negócio; a do ofício quando se fala dele; fé no sermão; manha na mentira (sem caminho, nenhuma)"""
    ma = p.get('maestria') or {}
    if not caminho or not isinstance(ma, dict): return 0, ''
    if caminho.startswith('oficio'):
        of = caminho.partition(':')[2] or max((o for o in ('forja', 'couro', 'alquimia', 'encanto', 'cura', 'caça') if ma.get(o)), key=lambda o: ma.get(o, 0), default=None)
        return (ma.get(of, 0), f"mão de {of}") if of else (0, '')
    c = H.FALA_CAMINHO.get(caminho)
    if c is None: sys.exit(f'o caminho é negocio, oficio[:OFICIO], sermao ou mentira (veio "{caminho}")')
    return ma.get(c, 0), f"mão de {c}"


def _fios(E, pid, lid):
    """os fios do Fio da Conversa que seguem neste lugar hoje"""
    fc = (E['gente'][pid].get('marca') or {}).get('fio') or {}
    return fc.get('n', 0) if fc.get('dia') == E['relogio']['dia'] and fc.get('lugar') == lid else 0


def opiniao(E, ouvinte, pid):
    import gente
    if ouvinte not in E['gente']: return 0
    return gente.opiniao(E, ouvinte, pid)[0]


def _firme_mestre(p): gp = _hab(p, 'palavra_firme'); return gp is not None and bool(H.num('palavra_firme', 'nao_ofende', gp))


def conta(E, pid, ouvinte, degrau, jeito='firme', caminho=None, ameaca=False, mais_hab=0, vont_ouvinte=None):
    """a conta do pedido, sem rolar: as parcelas, a CD, e a chance de cada faixa (exata: o 2d20 que explode do oficio._SOMAS). Serve aos dois lados: quem pede (pid) e quem ouve."""
    import oficio
    p = E['gente'][pid]; o = E['gente'].get(ouvinte) if ouvinte else None; jeito = _jeito(jeito); degrau = degrau_de(degrau)
    vb_o = ((o['atributos']['Vontade'] if o else (vont_ouvinte or 50)) // 10)
    atrib = 'Força' if (jeito == 'duro' and ameaca) else 'Vontade'; base = p['atributos'][atrib] // 10
    mao, mao_diz = _mao(p, caminho); op = opiniao(E, ouvinte, pid) if o else 0
    habs = []; hv = 0
    gf = _hab(p, 'fio_conversa'); fios = min(_fios(E, pid, estado.onde(E, pid)), H.num('fio_conversa', 'fios', gf)) if gf is not None else 0
    if fios: habs.append(f"o Fio da Conversa +{fios * H.FIO_MAIS}"); hv += fios * H.FIO_MAIS
    ga = _hab(p, 'ameaca_surda')
    if ga is not None and jeito == 'duro' and ameaca and H.num('ameaca_surda', 'mais', ga): habs.append(f"a Ameaça Surda +{H.num('ameaca_surda', 'mais', ga)}"); hv += H.num('ameaca_surda', 'mais', ga)
    if mais_hab: hv += mais_hab[0]; habs.append(mais_hab[1])
    hv = min(H.FALA_HAB_TETO, hv)
    gp = _hab(p, 'palavra_firme')
    j_cd = H.FALA_JEITOS[jeito] if not (jeito == 'duro' and gp is not None) else H.num('palavra_firme', 'duro', gp)
    cd = H.FALA_DEGRAUS[degrau] + vb_o // 2 + j_cd
    pena = corpo.pena(p, estado.agora(E))
    soma = base + mao + op + hv + pena; precisa = cd - soma
    ch = lambda x: oficio.chance_de(x)
    bem = ch(precisa + H.FALA_BEM); passa = ch(precisa); pf = jeito == 'duro' and _firme_mestre(p)
    if jeito == 'manso': ofende = 0.0
    elif jeito == 'duro': ofende = 1 - ch(precisa - (H.FALA_PALAVRA_FIRME - 1)) if pf else 1 - passa      # (6.6) no duro, falhar ofende sempre; a Palavra Firme do Mestre salva quem falha por menos de 5
    else: ofende = 1 - ch(precisa - H.FALA_OFENDE + 1)
    return dict(pid=pid, ouvinte=ouvinte, degrau=degrau, jeito=jeito, atributo=atrib, base=base, mao=mao, mao_diz=mao_diz, opiniao=op, hab=hv, habs=habs, pena=pena, cd=cd, j_cd=j_cd,
                mais=mao + op + hv, soma=soma, passa=passa, bem=bem, preco=passa - bem, nao=1 - passa - ofende, ofende=ofende, fios=fios, ameaca=ameaca, caminho=caminho,
                surdo=op <= H.FALA_SURDO, pf=pf)


def diz_conta(E, c):
    """a conta como vai à mesa, antes de rolar"""
    p = E['gente'][c['pid']]; o = E['gente'].get(c['ouvinte']); nm = o['nome'] if o else 'quem ouve'
    partes = [f"+{c['base']} de {c['atributo']}"] + ([f"+{c['mao']} da {c['mao_diz']}"] if c['mao'] else []) + ([f"{_sinal(c['opiniao'])} da opinião de {nm}"] if c['opiniao'] else [])
    partes += [x for x in c['habs']] + ([f"−{-c['pena']} do corpo"] if c['pena'] else [])
    t = (f"O PEDIDO ({H.FALA_DIZ[c['degrau']]}, jeito {c['jeito']}): 2d20 " + ' '.join(partes) + f", contra {c['cd']} (22 + 6 por degrau + metade da Vontade de {nm}"
         + (f", {_sinal(c['j_cd'])} do jeito {c['jeito']}" if c['jeito'] != 'firme' else '') + ')')
    if c['surdo']: return t + f"\n  {nm} não suporta {p['nome']} (opinião {c['opiniao']}): não ouve pedido nenhum."
    ofd = {'manso': 'nunca ofende (manso)', 'duro': f"ofende {_pct(c['ofende'])} (no duro, falhar ofende" + (': a Palavra Firme salva quem falha por menos de 5)' if c['pf'] else ' sempre)')}.get(c['jeito'], f"ofende {_pct(c['ofende'])}")
    return t + f"\n  a chance: passa {_pct(c['passa'])} (bem {_pct(c['bem'])}, com um preço {_pct(c['preco'])}) · não {_pct(c['nao'])} · {ofd}"


def _faixa(margem, jeito, pf=False):
    """a faixa do resultado: bem (6 ou mais), preco (0 a 5), nao, ofende. No manso, nunca ofende; no DURO, falhar ofende sempre (6.6), salvo a Palavra Firme do Mestre (pf), que
    deixa o duro que falha por menos de 5 no "não"; no firme, ofende quem falha por 10 ou mais"""
    if margem >= H.FALA_BEM: return 'bem'
    if margem >= 0: return 'preco'
    if jeito == 'manso': return 'nao'
    if jeito == 'duro': return 'nao' if pf and margem > -H.FALA_PALAVRA_FIRME else 'ofende'
    return 'nao' if margem > -H.FALA_OFENDE else 'ofende'


def _presentes(E, pid, ouvinte, degrau=None):
    p = estado.presente(E, pid, 'pedir')
    o = E['gente'].get(ouvinte) or sys.exit(f'não há a pessoa "{ouvinte}"')
    if o['estado'] != 'vivo': sys.exit(f"{o['nome']} {estado.morte_diz(E, o)}")
    if ouvinte == pid: sys.exit('ninguém pede a si mesmo')
    estado.em_cena(E, ouvinte)
    if estado.onde(E, ouvinte) != estado.onde(E, pid): sys.exit(f"{o['nome']} não está com {p['nome']}: o pedido se faz cara a cara")
    m = p.get('marca') or {}
    if ((m.get('surdo') or {}).get(ouvinte)) == E['relogio']['dia']: sys.exit(f"{o['nome']} não ouve pedido de {p['nome']} até amanhã (ofendido hoje)")
    nao = (m.get('nao') or {}).get(ouvinte)
    if degrau and isinstance(nao, dict) and nao.get('dia') == E['relogio']['dia'] and H.FALA_ORDEM.index(degrau) <= nao.get('degrau', -1):
        sys.exit(f"{o['nome']} já disse não a {p['nome']} hoje, num pedido {H.FALA_DIZ[H.FALA_ORDEM[nao['degrau']]]}: não ouve outro do mesmo degrau ou menor até amanhã (um maior, pode)")
    return p, o


# ---------- O PEDIDO MOSTRADO (a resposta 5a: o degrau e a chance ANTES do dado) ----------
def _chave(*partes): return '|'.join(str(x) for x in partes)


def mostra(E, pid, chave, c, txt):
    """guarda no caderno do turno o pedido cuja conta foi à mesa (o 1º passo): o `pede` só rola este, neste bloco, com esta mesma chance"""
    E['turno']['fala_vista'] = dict(pid=pid, chave=chave, dia=E['relogio']['dia'], bloco=E['relogio']['bloco'], passa=round(c['passa'], 6), bem=round(c['bem'], 6))
    return txt + "\n  (a conta foi à mesa: o jogador decide; o dado só rola com o pedido dito assim, neste bloco)"


def _visto(E, pid, chave, c, como):
    """o 2º passo: recusa o pedido cuja conta não foi mostrada (neste bloco, com esta chance) — a resposta 5a; e gasta a conta mostrada"""
    v = E['turno'].get('fala_vista') or {}
    if v.get('pid') != pid or v.get('chave') != chave or (v.get('dia'), v.get('bloco')) != (E['relogio']['dia'], E['relogio']['bloco']):
        sys.exit(f"o teste de fala só rola no pedido cuja chance foi mostrada antes (a resposta 5a): mostre primeiro, sem rolar: `{como}`")
    if abs(v.get('passa', -1) - round(c['passa'], 6)) > 1e-6 or abs(v.get('bem', -1) - round(c['bem'], 6)) > 1e-6:
        sys.exit(f"a conta mudou desde que foi mostrada (a chance agora é {_pct(c['passa'])}): mostre de novo: `{como}`")
    E['turno'].pop('fala_vista', None)


def _memoria(E, pid, ouvinte, peso, o_que):
    """UMA LINHA DE MEMÓRIA POR CONVERSA (a mesma pessoa, no mesmo dia): a primeira fala do dia a abre; as outras SOMAM o peso nela (no teto de cada fato, ±5), como a 12.4 lê
    ("pela soma"): ganhar um pedido manso e depois ofender deixa a linha em −2, não em +1"""
    import gente, tabelas_mundo as M
    o = E['gente'].get(ouvinte) or {}
    if not peso or o.get('jogador') or o.get('estado') != 'vivo': return []
    mem = [dict(m) for m in o.get('memoria') or []]
    i = next((n for n, m in enumerate(mem) if m.get('de') == pid and m.get('dia') == E['relogio']['dia'] and str(m.get('o_que', '')).startswith('a conversa')), None)
    if i is None: return gente.lembra(E, ouvinte, pid, f"a conversa: {o_que}", peso)
    novo = max(-M.MEMORIA_PESO, min(M.MEMORIA_PESO, int(mem[i]['peso']) + int(peso)))
    mem[i] = dict(mem[i], peso=novo, o_que=(mem[i]['o_que'] + f"; {o_que}")[:300])
    return [['pessoa', ouvinte, 'memoria', 'poe', mem]]


def _marcas_fala(E, pid, c, usadas, ganhou=False, diante=None):
    """a marca da cena da fala (os pedidos no mesmo lugar no dia): uma por cena, pela maior dureza, para cada habilidade de fala que agiu (a de dia que venceu soma 1); e o feito
    (vencer com ela uma cena de dureza 5: 6.2)"""
    import habilidade
    p = E['gente'][pid]; hb = p.get('habilidades') or {}; lid = estado.onde(E, pid); dia = E['relogio']['dia']
    cena = (p.get('marca') or {}).get('fala_cena') or {}
    if cena.get('lugar') != lid or cena.get('dia') != dia: cena = dict(lugar=lid, dia=dia, dureza=0, usos={}, dadas={})
    else: cena = dict(cena, usos=dict(cena.get('usos') or {}), dadas=dict(cena.get('dadas') or {}))
    d = H.dureza(1 - c['passa']); cena['dureza'] = max(cena['dureza'], d); ef = []
    for k in usadas:
        reg = hb.get(k)
        if not isinstance(reg, dict): continue
        cena['usos'][k] = cena['usos'].get(k, 0) + 1
        m = habilidade.marca_cena(cena['dureza'], cena['usos'][k], ganhou and H.HABILIDADES[k]['ritmo'] == 'dia', k, reg.get('grau', 0)) - cena['dadas'].get(k, 0)
        if m > 0: ef.append(['pessoa', pid, f'hab.{k}', 'soma', m]); cena['dadas'][k] = cena['dadas'].get(k, 0) + m
        ef += habilidade.feito(E, pid, k, max(0, m), d, ganhou, f"ganhou com {habilidade.nome(k)} um pedido de dureza {d}", diante=diante, ja=ef)
    return ef + [['pessoa', pid, 'marca.fala_cena', 'poe', cena]]


def pede(E, pid, ouvinte, degrau, o_que, jeito='firme', caminho=None, ameaca=False, mais_hab=0, efeitos_bem=None, efeitos_preco=None, tipo='fala', chave=None, como=None):
    """O PEDIDO DECLARADO (a resposta 5a): só o que foi mostrado antes (`conta`, neste bloco, com esta chance); o dado rola uma vez (teste.rola); a faixa diz o que se ganha;
    a memória, uma linha por conversa (somando); o "não" vale no dia; o Fio da Conversa anda ou rompe; a marca da cena e o feito. Devolve (o resultado, o texto)."""
    import habilidade
    jeito = _jeito(jeito); degrau = degrau_de(degrau)
    p, o = _presentes(E, pid, ouvinte, degrau); c = conta(E, pid, ouvinte, degrau, jeito, caminho, ameaca, mais_hab)
    if c['surdo']: sys.exit(diz_conta(E, c))
    _visto(E, pid, chave or _chave('pede', ouvinte, degrau, jeito, caminho or '', bool(ameaca)), c,
           como or f"fala.py conta {ouvinte} {degrau} jeito={jeito}" + (f" caminho={caminho}" if caminho else '') + (' ameaca' if ameaca else ''))
    pre = diz_conta(E, c)
    r = teste.rola(E, f"pede a {o['nome']}: {o_que} ({H.FALA_DIZ[c['degrau']]}, {c['jeito']})", c['atributo'], c['cd'], mais=c['mais'], quem=pid)
    margem = r['total'] - r['contra']; fx = _faixa(margem, c['jeito'], c['pf']); ganhou = fx in ('bem', 'preco')
    peso = 0; diz = []
    if fx == 'bem':
        diz.append('ganha, e leva mais um passo (um degrau a mais, ou um passo de preço)')
        if jeito == 'manso':
            ms = ((p.get('marca') or {}).get('manso') or {}).get(ouvinte)
            if not (isinstance(ms, int) and E['relogio']['dia'] - ms < H.FALA_MANSO_SEMANA): peso += H.FALA_MEMORIA['manso']; diz.append(f"{o['nome']} lembra bem (+1)")
        if jeito == 'duro': diz.append(f"{o['nome']} não age contra {p['nome']} hoje")
    elif fx == 'preco': diz.append('ganha COM UM PREÇO: a mesa dá dois ou três (um favor, um prazo, prata, uma promessa) e você escolhe um, ou desiste')
    elif fx == 'nao':
        diz.append('não ganha' + (' (no manso, é só "não")' if jeito == 'manso' and margem <= -H.FALA_OFENDE else ' (a Palavra Firme: o duro que falha por menos de 5 não ofende)' if jeito == 'duro' else ''))
        if c['degrau'] in ('grande', 'absurdo') or jeito == 'duro': peso += H.FALA_MEMORIA['nao_grande']
    else:
        diz.append(f"não ganha, e OFENDE: {o['nome']} não ouve pedido seu até amanhã" + (' (no duro, falhar ofende sempre)' if jeito == 'duro' and margem > -H.FALA_OFENDE else '')); peso += H.FALA_MEMORIA['ofende']
    if jeito == 'duro' and ganhou: peso += H.FALA_MEMORIA['duro']
    ef = []; usadas = []; lid = estado.onde(E, pid)
    gf = _hab(p, 'fio_conversa')
    if gf is not None:
        teto = H.num('fio_conversa', 'fios', gf)
        if c['fios'] or ganhou: usadas.append('fio_conversa')      # o Fio age quando há fio em jogo, ou quando ele anda
        if c['fios'] >= H.FIO_DEGRAU: peso -= 1; diz.append(f"o terceiro fio pesa: {o['nome']} sente a pressão (−1)")
        if ganhou: ef.append(['pessoa', pid, 'marca.fio', 'poe', dict(lugar=lid, dia=E['relogio']['dia'], n=min(teto, c['fios'] + 1))])
        elif c['fios']: ef.append(['pessoa', pid, 'marca.fio', 'poe', None]); peso -= 1; diz.append(f"o fio rompe, e {o['nome']} lembra (−1)")
        if c['fios'] >= H.FIO_DEGRAU and ganhou: diz.append('com 3 fios, o pedido vale um degrau acima (sem subir a CD)')
    if jeito == 'duro' and _hab(p, 'palavra_firme') is not None: usadas.append('palavra_firme')
    if jeito == 'duro' and ameaca and _hab(p, 'ameaca_surda') is not None: usadas.append('ameaca_surda')
    if mais_hab and len(mais_hab) > 2: usadas.append(mais_hab[2])
    m = p.get('marca') or {}
    if fx == 'ofende': ef.append(['pessoa', pid, 'marca.surdo', 'poe', dict((m.get('surdo') or {}), **{ouvinte: E['relogio']['dia']})])
    if fx == 'nao': ef.append(['pessoa', pid, 'marca.nao', 'poe', dict((m.get('nao') or {}), **{ouvinte: dict(dia=E['relogio']['dia'], degrau=H.FALA_ORDEM.index(c['degrau']))})])
    if fx == 'bem' and jeito == 'manso': ef.append(['pessoa', pid, 'marca.manso', 'poe', dict((m.get('manso') or {}), **{ouvinte: E['relogio']['dia']})])
    ef += _memoria(E, pid, ouvinte, peso, f"{o_que} ({H.FALA_DIZ[c['degrau']]}, {['não', 'ganhou'][ganhou]})")
    ef += _marcas_fala(E, pid, c, usadas, ganhou, diante=o['nome'])
    if fx == 'bem' and efeitos_bem: ef += efeitos_bem
    elif fx == 'preco' and efeitos_preco: ef += efeitos_preco
    estado.aplica(E, tipo, ef, onde=lid, quem=[pid, ouvinte], texto=f"{p['nome']} pede a {o['nome']}: {o_que} ({H.FALA_DIZ[c['degrau']]}, {jeito}): {['não ganha', 'ganha'][ganhou]}" + (' com um preço' if fx == 'preco' else ''))
    txt = pre + '\n' + teste.diz(E, r) + f"\n  {'; '.join(diz)}."
    if fx == 'preco':
        import turno
        try: txt += '\n  ' + turno.pergunta(E, f"{o['nome']} aceita o pedido ({o_que}), com um preço: qual?", ['a=um favor (ele cobra depois)', 'b=um prazo (fica para outro dia)', 'c=prata (o que ele pedir, dentro do justo)', 'd=desisto do pedido'])
        except SystemExit: pass
    sb = habilidade.sobe(E, pid)
    if sb: txt += '\n' + '\n'.join(sb)
    return dict(faixa=fx, margem=margem, rolagem=r, ganhou=ganhou, conta=c), txt


def conta_pedido(E, pid, ouvinte, degrau, jeito='firme', caminho=None, ameaca=False):
    """o 1º passo do `pede`: a conta à mesa, sem rolar, e o pedido guardado como mostrado"""
    jeito = _jeito(jeito); degrau = degrau_de(degrau); _presentes(E, pid, ouvinte, degrau)
    c = conta(E, pid, ouvinte, degrau, jeito, caminho, ameaca)
    if c['surdo']: return diz_conta(E, c)
    return mostra(E, pid, _chave('pede', ouvinte, degrau, jeito, caminho or '', bool(ameaca)), c, diz_conta(E, c))


# ---------- O REGATEIO (o preço: um passo, 5 pontos; uma vez por loja por dia) ----------
def mercador(E, lid):
    """quem ouve o regateio da loja do lugar: um mercador com nome dali (o de maior mão de comércio), ou ninguém (a loja: Vontade 50, opinião 0)"""
    cands = [k for k, q in E['gente'].items() if isinstance(q, dict) and q.get('estado') == 'vivo' and q.get('lugar') == lid and q.get('papel') == 'mercador' and not q.get('jogador')]
    return max(cands, key=lambda k: ((E['gente'][k].get('maestria') or {}).get('comércio', 0), k)) if cands else None


def _regateio(E, pid, alvo, passos, jeito):
    """o que o regateio pede, conferido antes de mostrar ou rolar: (p, lid, it, degrau, o Língua de Feira, quem ouve, a chave)"""
    import mercado
    p = estado.presente(E, pid, 'regatear'); lid = p['lugar']
    if not mercado.tem_mercado(E, lid): sys.exit(f"{E['lugares'][lid]['nome']} não tem mercado: não há com quem regatear")
    m = p.get('marca') or {}
    if (m.get('regateio_dia') or {}).get(lid) == E['relogio']['dia']: sys.exit(f"{p['nome']} já regateou na loja daqui hoje (uma vez por loja por dia)")
    passos = int(passos); degrau = {1: 'pequeno', 2: 'medio', 3: 'grande'}.get(passos) or sys.exit('o regateio é de 1, 2 ou 3 passos (pequeno, médio, grande)')
    it = E['itens']['itens'].get(alvo)
    gl = _hab(p, 'lingua')
    if it and it.get('dono') != pid and alvo in mercado.prateleira(E, lid) and not (gl is not None and H.num('lingua', 'prateleira', gl)):
        sys.exit('a peça da prateleira não se regateia (a loja pede o valor dela): só a Língua de Feira do Perito em diante regateia a compra da prateleira')
    if not it and not estado.bem_conhecido(alvo): sys.exit(f'regatear o quê? Um bem (comida, metal:0...) ou o id de uma peça (veio "{alvo}")')
    mais = (H.num('lingua', 'mais', gl), f"a Língua de Feira +{H.num('lingua', 'mais', gl)}", 'lingua') if gl is not None else 0
    quem = mercador(E, lid)
    if quem: _presentes(E, pid, quem, degrau)
    return p, lid, it, passos, degrau, mais, quem, _chave('regateia', alvo, passos, _jeito(jeito))


def regateia(E, pid, alvo, passos=1, jeito='firme', so_conta=False):
    """O REGATEIO: um pedido pequeno, médio ou grande (1, 2 ou 3 passos de preço) ao mercador da loja daqui; ganhou, o passo vale na próxima venda ou compra do alvo nesta loja,
    hoje (passou bem, um passo a mais; com 3 fios do Fio da Conversa, mais um, sem subir a CD); a Língua de Feira soma (do Perito, regateia também a compra da prateleira).
    `so_conta`: o 1º passo (a chance à mesa, sem rolar); sem ele, rola o regateio que foi mostrado."""
    p, lid, it, passos, degrau, mais, quem, chave = _regateio(E, pid, alvo, passos, jeito)
    como = f"fala.py regateia {alvo} passos={passos} jeito={_jeito(jeito)} conta"
    c = conta(E, pid, quem, degrau, jeito, 'negocio', mais_hab=mais, vont_ouvinte=50)
    if so_conta: return mostra(E, pid, chave, c, diz_conta(E, c))
    fio3 = 1 if c['fios'] >= H.FIO_DEGRAU else 0                # (6.3) com 3 fios, o pedido sobe um degrau sem subir a CD: um passo a mais
    m = p.get('marca') or {}; dia = E['relogio']['dia']
    efb = [['pessoa', pid, 'marca.regateio', 'poe', dict(lugar=lid, dia=dia, alvo=alvo, passos=passos + 1 + fio3)]]
    efp = [['pessoa', pid, 'marca.regateio', 'poe', dict(lugar=lid, dia=dia, alvo=alvo, passos=passos + fio3)]]
    dia_ef = ['pessoa', pid, 'marca.regateio_dia', 'poe', dict((m.get('regateio_dia') or {}), **{lid: dia})]
    o_que = f"regatear {estado.nome_bem(alvo) if not it else it['nome']} ({passos} passo{'s' if passos > 1 else ''} de preço)"
    onde = f"{'venda ou compra' if not it else 'venda' if it.get('dono') == pid else 'compra'} de {estado.nome_bem(alvo) if not it else it['nome']} nesta loja, hoje"
    if quem:
        R, txt = pede(E, pid, quem, degrau, o_que, jeito, caminho='negocio', mais_hab=mais, efeitos_bem=efb + [dia_ef], efeitos_preco=efp + [dia_ef], chave=chave, como=como)
        if not R['ganhou']: estado.aplica(E, 'fala', [dia_ef], onde=lid, quem=[pid], texto=f"{p['nome']} regateou e não ganhou")
        return txt + (f"\n  O regateio vale na próxima {onde}: {passos + (1 if R['faixa'] == 'bem' else 0) + fio3} passo(s) de 5 pontos" + (' (com o terceiro fio)' if fio3 else '') + '.' if R['ganhou'] else '')
    _visto(E, pid, chave, c, como); pre = diz_conta(E, c)
    r = teste.rola(E, f"{o_que} na loja ({H.FALA_DIZ[degrau]}, {c['jeito']})", c['atributo'], c['cd'], mais=c['mais'], quem=pid)
    fx = _faixa(r['total'] - r['contra'], c['jeito'], c['pf']); ganhou = fx in ('bem', 'preco')
    ef = [dia_ef] + (efb if fx == 'bem' else efp if fx == 'preco' else []) + _marcas_fala(E, pid, c, ['lingua'] if mais else [], ganhou)
    estado.aplica(E, 'fala', ef, onde=lid, quem=[pid], texto=f"{p['nome']} {o_que}: {'ganha' if ganhou else 'não ganha'}")
    return pre + '\n' + teste.diz(E, r) + (f"\n  ganhou: {passos + (1 if fx == 'bem' else 0) + fio3} passo(s) de 5 pontos na próxima {onde}." if ganhou else '\n  não ganhou: o preço fica o de sempre.')


def passos(E, pid, alvo):
    """os passos de regateio que valem agora para este alvo nesta loja (0 se nenhum)"""
    p = E['gente'][pid]; rg = (p.get('marca') or {}).get('regateio') or {}
    return int(rg.get('passos', 0)) if rg.get('lugar') == p['lugar'] and rg.get('dia') == E['relogio']['dia'] and rg.get('alvo') == alvo else 0


def gasta(pid):
    """o efeito que gasta o regateio (vai no evento da venda ou da compra)"""
    return ['pessoa', pid, 'marca.regateio', 'poe', None]


# ---------- O PEDIDO NEGOCIADO (a caixa e a missão) ----------
def _caixa_pedido(E, pid, xid, o_que, degrau):
    import caixa as CX
    x = (E['mundo'].get('caixa') or {}).get(xid) or sys.exit(f'não há o pedido "{xid}" na caixa')
    if x.get('fim') is not None: sys.exit(f'o pedido {xid} já se resolveu')
    de = x.get('de')
    if de not in E['gente']: sys.exit(f'o pedido {xid} é de {CX._de_quem(E, de)}: não há com quem falar cara a cara')
    if o_que == 'prazo':
        degrau = 'pequeno'; diz = f"o prazo vai ao Dia {x['prazo'] + H.CAIXA_PRAZO}"; efb = [['mundo', 'caixa', xid, 'prazo', 'poe', x['prazo'] + H.CAIXA_PRAZO]]
    elif o_que == 'paga':
        degrau = degrau_de(degrau or 'medio')
        if degrau not in H.CAIXA_PAGA: sys.exit('mais paga é médio (+25%) ou grande (+50%)')
        f = 1 + H.CAIXA_PAGA[degrau]; efs = {}
        for k, lista in x['efeitos'].items():
            nl = []
            for e in lista:
                if e[:1] == ['pessoa'] and len(e) == 5 and e[2] == 'moedas' and isinstance(e[4], int) and e[4] != 0 and (e[1] == pid or e[1] == de): nl.append(e[:4] + [int(math.floor(e[4] * f)) if e[4] > 0 else -int(math.floor(-e[4] * f))])
                else: nl.append(e)
            efs[k] = nl
        if efs == x['efeitos']: sys.exit(f'o pedido {xid} não paga prata a negociar')
        efb = [['mundo', 'caixa', xid, 'efeitos', 'poe', efs]]; diz = f"a paga sobe {round(100 * H.CAIXA_PAGA[degrau])}%"
    else: sys.exit('na caixa se negocia o prazo ou a paga')
    return de, degrau, diz, efb


def caixa(E, pid, xid, o_que='prazo', degrau=None, jeito='firme', so_conta=False):
    """o pedido da caixa negociado pelo mesmo teste: mais prazo (pequeno: +2 dias) ou mais paga (médio +25%, grande +50%, na prata que o personagem recebe em cada opção).
    Ganhar muda o pedido; perder deixa como era. `so_conta`: o 1º passo (a chance à mesa, sem rolar)."""
    de, degrau, diz, efb = _caixa_pedido(E, pid, xid, o_que, degrau); jeito = _jeito(jeito)
    chave = _chave('caixa', xid, o_que, degrau, jeito); como = f"fala.py caixa {xid} {o_que}" + (f" {degrau}" if o_que == 'paga' else '') + f" jeito={jeito} conta"
    if so_conta:
        _presentes(E, pid, de, degrau); c = conta(E, pid, de, degrau, jeito, 'negocio')
        return diz_conta(E, c) if c['surdo'] else mostra(E, pid, chave, c, diz_conta(E, c) + f"\n  (o que se pede: {diz})")
    R, txt = pede(E, pid, de, degrau, f"negociar o pedido {xid}: {diz}", jeito, caminho='negocio', efeitos_bem=efb, efeitos_preco=efb, chave=chave, como=como)
    return txt + (f"\n  O pedido {xid} mudou: {diz}." if R['ganhou'] else f"\n  O pedido {xid} fica como era.")


def _missao_pedido(E, pid, mid):
    import missoes
    m = missoes.todas(E).get(mid) or sys.exit(f'não há a missão "{mid}"')
    if m['estado'] not in ('aberta', 'tomada') or (m['estado'] == 'tomada' and m.get('quem') != pid): sys.exit(f'a missão {mid} não está aberta, nem tomada por você')
    if m.get('negociada'): sys.exit(f'a paga da missão {mid} já foi negociada')
    de = m['de']
    if de not in E['gente']: sys.exit(f'a missão {mid} é do quadro {estado.de(E, m["onde"])}: não há com quem falar cara a cara')
    nova = int(min(m['paga'] * (1 + H.MISSAO_PAGA), missoes._bolsa(E, de) * 0.6))
    if nova <= m['paga']: sys.exit(f"{E['gente'][de]['nome']} não tem prata para pagar mais")
    return m, de, nova


def missao(E, pid, mid, jeito='firme', so_conta=False):
    """a paga da missão +50% (pedido grande), a quem a posta; nunca acima de 60% da bolsa dele (a regra do quadro). `so_conta`: o 1º passo (a chance à mesa, sem rolar)."""
    m, de, nova = _missao_pedido(E, pid, mid); jeito = _jeito(jeito)
    chave = _chave('missao', mid, jeito); como = f"fala.py missao {mid} jeito={jeito} conta"
    if so_conta:
        _presentes(E, pid, de, 'grande'); c = conta(E, pid, de, 'grande', jeito, 'negocio')
        return diz_conta(E, c) if c['surdo'] else mostra(E, pid, chave, c, diz_conta(E, c) + f"\n  (o que se pede: a paga de {m['paga']} para {nova})")
    efb = [['mundo', 'missoes', mid, 'paga', 'poe', nova], ['mundo', 'missoes', mid, 'negociada', 'poe', True]]
    R, txt = pede(E, pid, de, 'grande', f"a paga da missão {mid} (de {m['paga']} para {nova})", jeito, caminho='negocio', efeitos_bem=efb, efeitos_preco=efb, chave=chave, como=como)
    if not R['ganhou']: estado.aplica(E, 'fala', [['mundo', 'missoes', mid, 'negociada', 'poe', True]], onde=E['gente'][pid]['lugar'], quem=[pid], texto=f"a paga da missão {mid} não sobe")
    return txt + (f"\n  A missão {mid} paga {nova}." if R['ganhou'] else f"\n  A missão {mid} paga o de antes ({m['paga']}).")


# ---------- A FALA DA GENTE NO PERSONAGEM (só põe preço na recusa) ----------
def da_gente(E, quem, degrau, o_que, pid=None, caminho=None):
    """a gente do mundo pede ao personagem (o mercador que regateia, o senhor que pede): o script rola a fala dela (o dado dela, uma vez) pela MESMA CONTA do pedido (a Vontade
    dela, a mão do caminho, a opinião de quem ouve, os fios dela no lugar e no dia, a pena do corpo) contra a CD do pedido com a Vontade dele; se passa, a mesa diz o PREÇO DE
    RECUSAR. Nada muda no personagem sem a resposta: aceitar ou recusar é sempre do jogador (a pergunta do turno guarda). Sem `caminho`, o do mercador é o negócio."""
    pid = pid or estado.eu(E); p = E['gente'][pid]; o = E['gente'].get(quem) or sys.exit(f'não há a pessoa "{quem}"'); degrau = degrau_de(degrau)
    if o['estado'] != 'vivo' or p['estado'] != 'vivo': sys.exit('quem fala e quem ouve estão vivos')
    if quem == pid: sys.exit('ninguém pede a si mesmo')
    vende = o.get('papel') == 'mercador'
    caminho = caminho or ('negocio' if vende else None)
    gl = _hab(o, 'lingua'); mais = (H.num('lingua', 'mais', gl), f"a Língua de Feira +{H.num('lingua', 'mais', gl)}") if gl is not None and caminho == 'negocio' else 0
    c = conta(E, quem, pid, degrau, 'firme', caminho, mais_hab=mais)
    r = teste.rola(E, f"pede a {p['nome']}: {o_que} ({H.FALA_DIZ[degrau]})", c['atributo'], c['cd'], mais=c['mais'], quem=quem, rotulo=f"{c['atributo']} e a conta da fala")
    preco = H.PRECO_RECUSA[degrau]
    if r['passou']:
        txt = f"{o['nome']} foi convincente: recusar custa {_sinal(preco)} na opinião de {o['nome']} sobre {p['nome']}" + (" (e, se for a loja que vende a você, ela baixa 10% se você aceitar agora)" if vende else '') + '.'
        ops = ['a=aceito', f'b=recuso (custa {_sinal(preco)} na opinião de {o["nome"]})']
    else:
        txt = f"{o['nome']} não convenceu: recusar não custa nada."; ops = ['a=aceito', 'b=recuso (sem custo)']
    import turno
    try: perg = turno.pergunta(E, f"{o['nome']} pede: {o_que}", ops)
    except SystemExit: perg = ''
    return (dict(passou=r['passou'], preco=preco if r['passou'] else 0, rolagem=r, conta=c),
            diz_conta(E, c).replace('O PEDIDO', f"O PEDIDO DE {o['nome'].upper()} A {p['nome'].upper()}", 1) + '\n' + teste.diz(E, r, mestre=True) + '\n' + txt + (f"\n  {perg}" if perg else '') + "\n  A escolha é do jogador: nada muda até a resposta.")


if __name__ == '__main__':
    import signal; hasattr(signal, 'SIGPIPE') and signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    a = sys.argv[1:]
    if not a: print(__doc__); sys.exit()
    op = dict(x.split('=', 1) for x in a if '=' in x); pos = [x for x in a if '=' not in x]
    E = estado.carrega(); pid = op.get('quem') or estado.eu(E)
    if pid not in E['gente']: sys.exit(f'não há a pessoa "{pid}"')
    j = op.get('jeito', 'firme'); cam = op.get('caminho'); am = 'ameaca' in pos; sc = 'conta' in pos[1:]; pos = [x for x in pos if x != 'ameaca'] if pos else pos
    if sc: pos = [pos[0]] + [x for x in pos[1:] if x != 'conta']
    if pos[0] == 'conta' and len(pos) == 3:
        if pos[1] not in E['gente']: sys.exit(f'não há a pessoa "{pos[1]}"')
        out = conta_pedido(E, pid, pos[1], pos[2], j, cam, am); estado.grava(E); print(out); sys.exit()
    import ato
    if pos[0] == 'pede' and len(pos) == 4: R, out = pede(E, pid, pos[1], pos[2], pos[3], j, cam, am)
    elif pos[0] == 'regateia' and len(pos) == 2: out = regateia(E, pid, pos[1], op.get('passos', 1), j, so_conta=sc)
    elif pos[0] == 'caixa' and len(pos) in (3, 4): out = caixa(E, pid, pos[1], pos[2], pos[3] if len(pos) > 3 else None, j, so_conta=sc)
    elif pos[0] == 'missao' and len(pos) == 2: out = missao(E, pid, pos[1], j, so_conta=sc)
    elif pos[0] == 'gente' and len(pos) == 4: R, out = da_gente(E, pos[1], pos[2], pos[3], pid, cam)
    else: print(__doc__); sys.exit()
    estado.grava(E); print(out)
    if not sc: print(ato.ultima_linha(E, pid))
