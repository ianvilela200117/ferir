#!/usr/bin/env python3
"""magia.py — MOTOR 10, ETAPA DA MAGIA: A MAGIA NA LUTA (capítulo 11; os números no tabelas_magia.py; o contrato: projeto/ETAPA_MAGIA.md, seção 10).

O luta.py chama daqui o que a magia pede, e SÓ numa luta com magia (S['magia']: alguém traz feitiço, foco, amuleto, encanto, poção, elixir, veneno na lâmina,
traço novo, fases ou pena de maldição). A luta sem nada disso é a de sempre, dado por dado.

  QUEM LANÇA: quem traz feitiços (gente, povo, ou bicho com o traço "lança"). A Conjuração é a mão da tradição, o dom nela, metade do bônus do atributo dela
  e o bônus do foco (o bicho que lança: o instinto e o corpo). O que voa vai contra a Defesa inteira, como um tiro; a área, contra a Defesa sem escudo e sem
  arma; o que prende, assusta ou amaldiçoa, contra a Firmeza (mais o calejo). O dano é o do aço: dado × 4 × valor do foco ÷ guarda × força do feitiço.
  A Mana volta 1 no começo de cada turno de quem lança. O feitiço de grau 2 gasta o turno; o de grau 3 é LONGO: sai no começo do turno seguinte, e quem
  canaliza e apanha testa a concentração. Lançar com o inimigo colado dá a ele um golpe livre. Dois 1 no dado: RETROCHOQUE (no lance forçado, basta um 1).
  Sem Mana, pode-se lançar NO OSSO (só por ordem: cada ponto que falta custa 5% do PV máximo, e o lance é forçado).
  A POÇÃO (1 ação; dar de beber a um aliado colado, também), A PEÇA ENCANTADA (uma vez por luta, um degrau abaixo da peça), OS NOVE TRAÇOS NOVOS e AS FASES DO CHEFE.

Uso em código (o que as outras frentes chamam):
  escolhe(S, f)              o que faz agora quem o jogador não comanda e lança, bebe ou solta um encanto (gente, povo ou bicho): a ação, ou None (luta como sempre)
  tem_magia(f) · prepara(S, f) · guarda(S, e) · firmeza(S, e) · conj(S, f, feitico)      (as contas, para quem quiser ler)
  As ordens de quem o jogador comanda (luta.ordem): lancar FEITICO [em ALVO | casa N] [sempre] [osso] [neblina|lama] [dominio] · beber POCAO [em ALIADO] · usar [PECA] [em ALVO | casa N]
  (A PARTE 2, FASE 1b: os efeitos de foco e de amuleto: a Chama e a Guarda Mágica no dano, o Foco Certeiro na Conjuração, a Firmeza, a Refletora do escudo, o Domínio do foco
  (`dominio` na ordem; o robô o solta no primeiro feitiço de grau 2 ou mais), e o calejo por família: o feitiço de controle que pega soma na resistência à carga da família dele,
  e o controle de arma da mesma família soma na Firmeza contra ele, sem contar duas vezes.)
  (A PARTE 2, FASE 2: as três de lançar, só numa luta em que alguém traz habilidade: A CORRENTE (cada feitiço seguido, +1 na Conjuração no teto de +8 e +5% de dano de feitiço,
  TÉCNICA; golpear, andar ou ser atordoado zera), A MÃO NO RITO (o longo que se perde devolve metade da Mana; do Adepto, o longo sai uma rodada mais cedo uma vez por luta; do
  Mestre, sempre) e A MANA CURTA (o primeiro feitiço da luta custa menos); e o Rito de Veia (+1 dado em cada feitiço; a cura de magia em quem o abriu vale metade).)
"""
import copy, math, sys, unicodedata
import tabelas as T
import tabelas_bichos as TB
import tabelas_magia as TM
import tabelas_magia_mundo as W
import tabelas_povos as TP
import tabelas_efeitos as TE
import tabelas_habilidades as HT
import luta as L

DANO_LONGE = ('seta', 'lança-de-fogo', 'bola-de-fogo', 'raio')      # quem sabe destes e não tem o que lançar, espera a Mana voltar em vez de ir ao corpo a corpo
ORDEM_ROBO = ('cura', 'amparo', 'escudo', 'guarda', 'bênção', 'mau-olhado', 'nó', 'medo', 'afugentar', 'prender', 'raízes', 'bola-de-fogo', '*dano', 'seiva', 'luz', 'chamar')
DANO_ROBO = ('raio', 'lança-de-fogo', 'seta', 'castigo', 'espinho', 'sangria')
HOSTIS = ('dano', 'area', 'poe', 'medo')


# ---------- quem é quem ----------
def tem(f, t): return t in (f.get('tracos') or ())
def ve(f, k): return (f.get('est') or {}).get(k)                     # o estado k (o prazo ou o valor), ou None
def sem_vida(f): return tem(f, 'sem vida')
def nome(k): return T.nome_feitico(k)
def _lista(f, k): return f.setdefault(k, [])
def _s(n): return '' if n == 1 else 's'
def conta(S, k, v=1): c = S.setdefault('conta', {}); c[k] = c.get(k, 0) + v          # os contadores que as provas leem


def _sem_acento(s): return ''.join(c for c in unicodedata.normalize('NFD', s.lower()) if unicodedata.category(c) != 'Mn')


def mana_diz(f):
    """a Mana como vai à mesa: "agora/máxima", sem o dom escondido (quem traz `mana_vista` tem um dom de tradição que ainda não viu: a mesa mostra a conta que ele conhece)"""
    mx = f.get('mana_vista', f.get('mana_max', 0)); return f"{min(f.get('mana', 0), mx)}/{mx}"


def tem_magia(f):
    """este lutador traz magia para a luta? (então a luta inteira é de magia: os outros também podem ser alvo dela)"""
    return bool(f.get('feiticos') or f.get('foco') or f.get('amuleto') or f.get('encantos') or f.get('carga') or f.get('elixires') or f.get('fases') or f.get('benzido')
                or f.get('pena_magia') or f.get('maldito') or f.get('maldicoes') or any(t in T.TRACOS_NOVOS for t in f.get('tracos') or ())
                or any(w and w.get('veneno') is not None for w in (f.get('arma'), f.get('arma2'))))


def prepara(S, f):
    """os campos da luta de magia, em cada lutador de uma luta com magia (quem veio sem a ficha inteira ganha o valor neutro)"""
    f.setdefault('est', {}); f.setdefault('calejo', 0); f.setdefault('canaliza', None)
    for k in ('feiticos', 'tracos', 'fases', 'encantos', 'elixires'): f[k] = list(f.get(k) or [])
    f['carga'] = {b: q for b, q in (f.get('carga') or {}).items() if q}
    for i, x in enumerate(f['elixires']): x.setdefault('id', f"elixir {i + 1} de {f['nome']}")
    at = f.setdefault('atributos', {'Afinidade': 40, 'Vontade': f['vontade_b'] * 10, 'Vigor': 50})
    f.setdefault('m_trad', {t: f.get('maestria', 0) for t in T.TRADICOES}); f.setdefault('cat_corpo', 0); f.setdefault('pena', 0); f.setdefault('afin_b', at.get('Afinidade', 40) // 10)
    f.setdefault('firmeza0', T.FIRMEZA_BASE + f['vontade_b'] / 2 + f.get('maestria', 0) / 2); f.setdefault('doses', 0); f.setdefault('curado', 0)
    if f.get('benzido'): f['est']['benzido'] = TM.PRAZO_SEM_FIM
    if isinstance(f.get('guarda_p'), int) and not isinstance(f['guarda_p'], bool): f['est']['guarda_p'] = max(f['guarda_p'], f['est'].get('guarda_p', -1) if f['est'].get('guarda_p') is not None else -1)      # a poção de guarda bebida antes da luta (marca.guarda)
    if sem_vida(f): f['moral'] = 'firme'                                # quem não tem vida não testa a coragem: não foge
    if f['feiticos']:
        if not f.get('mana_max'): f['mana_max'] = T.mana_max(at.get('Afinidade', 40), at.get('Vontade', 45), f.get('maestria', 0))
        f['mana'] = f['mana_max'] if f.get('mana') is None else max(0, min(f['mana'], f['mana_max']))


# ---------- a conta ----------
def trad_de(f, k):
    """a tradição pela qual se lança k: a do feitiço; o truque, a melhor mão de quem lança"""
    de = T.FEITICOS[k]['de']
    if de != 'todas': return de
    mt = f.get('m_trad') or {}
    return max(T.TRADICOES, key=lambda t: (mt.get(t, 0), t == f.get('tradicao')))


def foco(S, f, trad):
    """(a categoria que o foco rende para esta tradição, o que tira da Conjuração, × o valor). Sem foco: Comum, −4. Foco de outra tradição: uma categoria abaixo.
    O bicho que lança: o corpo é o foco."""
    if f.get('bicho'): return f.get('cat_corpo', 0), 0, 1.0
    k = f.get('foco')
    if k and L.inteiro(S, k) and f.get('foco_cat') is not None:
        fo = T.FOCOS[S['itens'][k]['forma']]; c = f['foco_cat'] - (0 if trad in fo['de'] else TM.FOCO_OUTRA)
        if c >= 0: return c, -f.get('foco_falta', 0), fo['vezes']
    return 0, TM.SEM_FOCO, 1.0


def penas(S, f):
    """as penas da luta na mão de quem lança: o abalo, o braço ferido, o enjoo, e a pior pena de magia (mau-olhado, veneno, maldição: não somam; a da maldição já está na pena do corpo)"""
    pm = f.get('pena_magia', 0) or 0; ol = TM.ESTADOS['olhado']['conj'] if ve(f, 'olhado') else 0; vn = TB.VENENO['acerto'] if f.get('veneno') else 0
    return (L._medo_acerto(f) + sum(T.FERIDAS['braços'][1 if gr else 0] for p, gr in f['feridas'] if p == 'braços')
            + (TM.ESTADOS['enjoo'] if ve(f, 'enjoo') else 0) + min(pm, ol, vn) - pm)


def conj(S, f, k, fonte=None):
    """(a Conjuração, a categoria do foco, × o valor do foco, o dom que entrou, a força do feitiço) para lançar k agora"""
    at = f.get('atributos') or {}
    if fonte is not None:                                   # a peça encantada: 2 por grau de quem gravou, o bônus de Afinidade do dono ÷ 2, e a peça como foco um degrau abaixo
        e = f['encantos'][fonte]; c = e['cat']
        base = TM.ENCANTO['por_grau'] * e['grau'] + f.get('afin_b', 4) / 2 + T.BON[c]; return base + f.get('pena', 0) + penas(S, f), c, 1.0, 0, T.forca_mult(at.get('Afinidade', 40))
    trad = trad_de(f, k); c, mais, vezes = foco(S, f, trad); a = at.get('Afinidade' if f.get('bicho') else T.TRADICOES[trad], 40)
    m = f.get('maestria', 0) if f.get('bicho') else (f.get('m_trad') or {}).get(trad, 0)
    dom = 0 if f.get('bicho') else int((f.get('dom') or {}).get(trad, 0) or 0)
    laco = (f.get('pena_laco') or 0) if trad == 'verde' else 0         # o druida cujo ermo do laço foi caçado até o fim perde a força (magia_mundo.pena_laco: o estado.lutador traz)
    fc = 0 if f.get('bicho') else min(TE.FIXO_TETO, (_fx_foco(S, f, 'foco_certeiro') or 0) + (f.get('corrente') or 0) * HT.CORRENTE_CONJ)       # (fase 1b) o Foco Certeiro do foco; (fase 2) a Corrente (P3: até +8)
    return m + dom + (a // 10) / 2 + T.BON[c] + mais + laco + f.get('pena', 0) + penas(S, f) + fc, c, vezes, dom, T.forca_mult(a)


def _fx_foco(S, f, k):
    """(fase 1b) um efeito do foco de quem lança (a Chama, o Foco Certeiro, o Domínio): só o foco inteiro, em uso"""
    fo = f.get('foco')
    if not fo or not L.inteiro(S, fo): return None
    return next((src['efeitos'].get(k) for src in f.get('fontes') or [] if src.get('item') == fo), None)


def falta_mao(f, k, fonte=None):
    """quantos graus de mão faltam para k (abaixo da mão o lance é forçado). A peça encantada e o bicho que lança não forçam."""
    if fonte is not None or f.get('bicho'): return 0
    return max(0, math.ceil((TM.MAO[T.FEITICOS[k]['grau']] - (f.get('m_trad') or {}).get(trad_de(f, k), 0)) / 2))


def custo(f, k): return T.FEITICOS[k]['mana'] + (TM.NO_CUSTO if ve(f, 'no') else 0)
def acoes(ac): return 1 if ac[0] == 'bebe' else TM.ACOES[T.FEITICOS[ac[1]]['grau']]


def jogada(bon, forcado=False):
    """o dado do lance: 2d20 que explodem no 20, como o golpe. Dois 1: o retrochoque (no lance forçado, basta um 1)."""
    a, b = L.d20x(), L.d20x(); n = (a[0], b[0])
    return dict(total=sum(a) + sum(b) + bon, falha=n == (1, 1) or (forcado and 1 in n), crit=max(n) >= 20 and min(n) >= T.CRIT_OUTRO)


def guarda(S, e):
    """(o que DIVIDE o feitiço, a chave do amuleto se foi ele que guardou): o amuleto (ou a guarda do clérigo, ou a poção de guarda), ou 0,6 da armadura do tronco
    (o couro do bicho também; com o traço "resiste", inteira), o que for maior; sem nada disso, um terço. O material e a parte do corpo não contam."""
    g = T.GUARDA_NU; am = None; s = e.get('est') or {}; k = e.get('amuleto')
    if k and L.inteiro(S, k) and e.get('amuleto_cat') is not None: g = T.MULT[e['amuleto_cat']]; am = k
    for c in ((s.get('guarda') or [None])[0], s.get('guarda_p')):
        if c is not None and T.MULT[c] > g: g = T.MULT[c]; am = None
    tr = e['partes'].get('tronco')
    if tr and L.inteiro(S, tr['item']):
        v = T.RD[tr['cat']] * (1 if tem(e, 'resiste') else T.GUARDA_ARMADURA)
        if v > g: g = v; am = None
    return g, am


def firmeza(S, e, k=None):
    """a Firmeza na luta: a base (a Vontade, a maior mão, o dom de tradição) e o melhor entre o amuleto (ou a guarda) e metade da armadura do tronco
    (com "resiste", inteira); mais o calejo (cada controle que já pegou). (Fase 1b) Mais o efeito Firmeza do amuleto (P3: até +8); e o calejo POR FAMÍLIA: contra o feitiço k,
    vale o maior entre o calejo de hoje (+4 por controle de feitiço que pegou, geral) e o +4 por controle de arma da mesma família (a carga): os dois caminhos não somam (M21 igual)"""
    s = e.get('est') or {}; b = 0; am = e.get('amuleto')          # (o amuleto tem nome próprio: o `k` é o feitiço, e a família do calejo sai dele)
    if am and L.inteiro(S, am) and e.get('amuleto_cat') is not None: b = T.BON[e['amuleto_cat']]
    for c in ((s.get('guarda') or [None])[0], s.get('guarda_p')):
        if c is not None: b = max(b, T.BON[c])
    tr = e['partes'].get('tronco')
    if tr and L.inteiro(S, tr['item']): b = max(b, T.BON[tr['cat']] * (1 if tem(e, 'resiste') else 0.5))
    fam = TE.FEITICO_FAMILIA.get(k); cf = (e.get('calejo_f') or {}).get(fam, 0) if fam else 0
    return e.get('firmeza0', T.FIRMEZA_BASE) + b + max(TM.CALEJO * e.get('calejo', 0), TE.CALEJO_FIRMEZA * cf) + min(TE.FIXO_TETO, L.efeito(S, e, 'firmeza') or 0)


def defesa_mais(S, e):
    """o que a magia mexe na Defesa: o escudo do mago, a fúria, o enjoo, o mau-olhado (que não soma com a pena da maldição: vale a pior)"""
    s = e.get('est') or {}; d = 0
    if s.get('guardado'): d += TM.ESTADOS['guardado']['defesa']
    if s.get('furia'): d += TM.ESTADOS['furia']['defesa']
    if s.get('enjoo'): d += TM.ESTADOS['enjoo']
    pm = e.get('pena_magia', 0) or 0
    return d + min(pm, TM.ESTADOS['olhado']['defesa'] if s.get('olhado') else 0) - pm


def defesa(S, a, e, area):
    """a Defesa contra o feitiço que voa (inteira, como contra um tiro) ou contra a área (sem escudo e sem arma, como contra o sopro)"""
    pd = T.POSTURAS.get(e['postura']) or T.POSTURAS['firme']          # (a postura nova `bigorna`, da fase 2, vale pela habilidade: habilidade.defesa_mais)
    df = (e['def_fixa'] if area else L.defesa_de(S, e)) + pd[1] - (T.SEM_FOLEGO if e['fol'] <= 0 else 0) + (T.CHAO if e['chao'] else 0) + (T.PRESO if e['preso'] else 0) + (T.RESGUARDO if e['resguardo'] else 0)
    df += sum(T.TEMPO[k].get('defesa', 0) for k in S['tempo']) + defesa_mais(S, e)
    if S.get('hab'):                                        # (fase 2) como no golpe: a Guarda de Bigorna contra o que voa (no teto de +8; contra a área, não, como o escudo), e o −1 da Sanha
        import habilidade
        if not area and habilidade.defesa_mais(S, e): df += min(TE.FIXO_TETO, habilidade.defesa_mais(S, e)); habilidade._usa(e, 'bigorna')
        df += habilidade.defesa_pena(S, a, e)
    return df - T.FLANCO * min(T.FLANCO_MAX, sum(1 for n, _ in e['golpeado'] if n != a['nome']))


def mira(S, a, e, area):
    """o que pesa no feitiço que voa, como num tiro: o tempo (o escuro não, para quem é noturno), o alto, a cobertura, a gente no caminho, a cegueira"""
    b = sum(T.TEMPO[k].get('tiro', 0) for k in S['tempo'] if not (k == 'escuro' and tem(a, 'noturno')))
    if 'escuro' in S['tempo'] and tem(a, 'vê no escuro') and not tem(a, 'noturno'): b -= T.TEMPO['escuro']['tiro'] * (1 - TP.ESCURO_TIRO)      # quem vê no escuro (o povo, etapa 4b): o feitiço que voa é tiro (ESCURO_TIRO: inteiro)
    if S['lugar'].get('alto') == a['lado']: b += T.ALTO['tiro']
    if S['lugar'].get('cobertura') == e['lado']: b += T.COBERTURA
    if not area and L.entre(S, a, e) and S['lugar'].get('alto') != a['lado']: b += T.ENTRE
    if ve(a, 'cego'): b += TM.ESTADOS['cego']['tiro']
    return b


# ---------- o que a magia mexe no golpe de aço (o luta.golpe chama) ----------
def no_golpe(S, a, e, w):
    """(no acerto de quem bate, na Defesa de quem apanha): a bênção, a fúria, a cegueira, o enjoo, o escuro de quem é noturno, as penas de magia que não somam"""
    tiro = w['distancia']; sa = a.get('est') or {}; b = 0
    if sa.get('benzido') and not w.get('area'): b += TM.ESTADOS['benzido']['acerto']
    if sa.get('furia') and w['cat'] <= sa['furia'][1]: b += TM.ESTADOS['furia']['acerto']
    if sa.get('cego'): b += TM.ESTADOS['cego']['tiro' if tiro else 'golpe']
    if sa.get('enjoo'): b += TM.ESTADOS['enjoo']
    if tem(a, 'noturno') and 'escuro' in S['tempo']: b -= T.TEMPO['escuro']['tiro' if tiro else 'acerto']        # o escuro não tira nada de quem é noturno
    pm = a.get('pena_magia', 0) or 0; vn = TB.VENENO['acerto'] if a.get('veneno') else 0; ol = TM.ESTADOS['olhado']['acerto'] if sa.get('olhado') else 0
    b += min(pm, ol, vn) - pm - vn                              # vale a pior (a da maldição já está no acerto; a do veneno, no golpe de sempre)
    if w.get('corpo'): w['queima'] = tem(a, 'ardente')          # a ferida que o corpo ardente abre queima
    return b, defesa_mais(S, e)


def dano_aco(S, a, e, w, dano):
    """os traços novos no golpe de aço que passou: o osso (corte e ponta pela metade) e o imaterial (a arma sem encanto nem bênção conta uma categoria abaixo)"""
    if tem(e, 'ossos') and w['golpe'] in ('corte', 'ponta'): dano = int(dano * TM.OSSOS)
    if tem(e, 'imaterial') and not w.get('magica') and not w.get('area'): dano = int(dano / 3 ** TM.IMATERIAL)
    return dano


def fogo_de_volta(S, a, e, w):
    """o corpo ardente: quem o golpeia de perto leva o fogo de volta (4 por degrau da categoria do corpo: tabelas_magia.ardente_fogo)"""
    if w['distancia'] or w.get('area') or a['estado'] != 'pe' or L.dist(a, e) > 1 or tem(a, 'ardente'): return
    q = TM.ardente_fogo(e.get('cat_corpo', 0)); a['pv'] -= q; S['dano_r'] += q / a['pvmax']
    L.diz(S, f"    o fogo de {e['nome']} queima {a['nome']} ({max(a['pv'], 0)}/{a['pvmax']})")
    if a['pv'] <= 0: L._cai(S, a, 0)


def feriu(S, a, e, w, dano, abriu):
    """o golpe de aço tirou PV: a dose da lâmina, o dreno, a maldição de quem amaldiçoa, a concentração de quem canaliza e a fase do chefe"""
    if w.get('veneno') is not None and not w.get('corpo') and not w.get('area'):
        if e['estado'] == 'pe' and not sem_vida(e):            # A DOSE NA LÂMINA: a primeira vez que a arma tira sangue envenena; numa lâmina acima da dose, um terço por degrau
            fr = TM.VENENO_LAMINA['fracao'] * TM.VENENO_LAMINA['acima'] ** max(0, w['cat'] - w['veneno']) * (TP.VENENO if tem(e, 'resiste a veneno') else 1); q = max(1, int(dano * fr)); ant = e['veneno'] or [0, 0]      # quem resiste a veneno (o povo): a metade
            e['veneno'] = [max(q, ant[0]), TM.VENENO_LAMINA['rodadas']]; e['veneno_cat'] = max(e.get('veneno_cat', 0), w['veneno'])
            L.diz(S, f"    o veneno da lâmina entra em {e['nome']} ({e['veneno'][0]} por rodada)")
        iid = S['itens'][w['item']].get('id'); w['veneno'] = None; conta(S, 'doses_lamina')
        if iid: _lista(a, 'venenos_gastos').append(iid)
    if tem(a, 'dreno') and w.get('corpo') and a['estado'] == 'pe' and a['pv'] < a['pvmax']:
        g = min(a['pvmax'] - a['pv'], max(1, int(dano * TM.DRENO))); a['pv'] += g; S['dano_r'] -= g / a['pvmax']
        L.diz(S, f"    {a['nome']} bebe a vida que tirou (+{g}: {a['pv']}/{a['pvmax']})")
    if abriu and tem(a, 'amaldiçoa'): amaldicoa(S, a, e)
    apanhou(S, e, dano, abriu)


def apanhou(S, e, dano, abriu):
    """quem levou dano: quem canaliza testa a concentração (ou perde sem teste: caído, no chão, atordoado ou agarrado); o chefe muda de fase"""
    if e.get('canaliza'):
        if e['estado'] != 'pe' or e['chao'] or e['atordoado'] or e.get('perde_turno') or L._agarrado(S, e): perde(S, e, 'sem teste')
        elif dano > 0: concentra(S, e, abriu)
    if e.get('fases') and e['estado'] == 'pe': fase(S, e)


def amaldicoa(S, a, e):
    """o traço "amaldiçoa": a ferida que ele abre põe uma maldição da categoria do corpo dele, no passo 1 (volta ao estado em maldicoes_postas)"""
    fonte = a.get('bicho') or a.get('povo') or a['nome']
    if e['estado'] == 'morto' or any(m.get('fonte') == fonte for m in e.get('maldicoes_postas') or []): return
    mo = dict(a.get('maldicao') or TM.MALDICAO_BICHO)
    _lista(e, 'maldicoes_postas').append(dict(nome=TB.contrai(mo['nome'].format(quem=a['nome'])), cat=a.get('cat_corpo', 0), tipo=mo['tipo'], condicao=dict(mo['condicao']), passo=1,
                                             de='bicho' if (a.get('bicho') or a.get('povo')) else 'feitiço', fonte=fonte, quem=a.get('id'), sabe=0))
    conta(S, 'maldicoes')
    L.diz(S, f"    {e['nome']} sente o frio de uma maldição")
    L._para(S, e, f"{e['nome']} levou uma maldição de {a['nome']}", so_controlado=True)


def concentra(S, f, ferida):
    """quem canaliza e leva dano: 2d20 + bônus de Vontade + mão da tradição contra 28 (32 se o golpe abriu ferida). Falhou: perde o feitiço (a Mana já foi)."""
    c = f['canaliza']; m = f.get('maestria', 0) if f.get('bicho') else (f.get('m_trad') or {}).get(c['trad'], 0)
    t = sum(L.d20x()) + sum(L.d20x()) + f['vontade_b'] + m; cd = TM.CONCENTRA + (TM.CONCENTRA_FERIDA if ferida else 0); conta(S, 'conc_testes')
    if t >= cd: L.diz(S, f"    {f['nome']} segura o feitiço ({t} contra {cd})"); return True
    conta(S, 'conc_falhas'); perde(S, f, f'{t} contra {cd}'); return False


def perde(S, f, porque):
    """o feitiço que se canalizava se perde (a Mana dele já foi)"""
    c = f['canaliza']; f['canaliza'] = None; conta(S, 'conc_perdidos')
    gr = (f.get('hab') or {}).get('mao_rito', -1) if S.get('hab') else -1
    if gr >= 0 and HT.num('mao_rito', 'devolve', gr) and c.get('fonte') is None and f.get('mana_max'):      # (fase 2) a Mão no Rito do Iniciante e do Aprendiz: o longo perdido devolve metade da Mana
        q = T.FEITICOS[c['nome']]['mana'] // 2; f['mana'] = min(f['mana_max'], f['mana'] + q); f.setdefault('hab_usos', {})['mao_rito'] = f['hab_usos'].get('mao_rito', 0) + 1
    if porque == 'sem teste': conta(S, 'conc_cortes' if f['estado'] == 'pe' else 'conc_caiu')
    L.diz(S, f"    {f['nome']} PERDE O FEITIÇO ({nome(c['nome'])}: {porque})")
    L._para(S, f, f"{f['nome']} perdeu o feitiço ({nome(c['nome'])})", so_controlado=True)


def _para_todos(S, txt):
    """a parada que vale para os dois lados (o feitiço longo do outro lado, o campo que muda, o chefe que muda de fase)"""
    if txt not in S['paradas']: S['paradas'].append(txt)
    S['houve_parada'] = True


def _gasta(S, f, k, n, que):
    """o foco ou o amuleto gasta (a zero, não vale)"""
    it = S['itens'][k]
    if it['dur'][0] <= 0: return
    it['dur'][0] = max(0, it['dur'][0] - n)
    if it['dur'][0] == 0: L.diz(S, f"    ✖ {it['nome']} de {f['nome']} se desfaz"); L._para(S, f, f"{it['nome']} de {f['nome']} se desfez")


# ---------- lançar ----------
def dominio_pronto(S, f):
    """(fase 1b) o DOMÍNIO do foco (inteiro, em uso) ainda não saiu nesta luta?"""
    return bool(_fx_foco(S, f, 'dominio')) and f.get('usou', []).count('dominio') < TE.DOMINIO_USOS


def lanca(S, f, k, alvo=None, casa=None, fonte=None, osso=False, campo=None, dominio=False):
    """lança k: a Mana sai na hora; com o inimigo colado, ele bate antes (e quem apanhou testa a concentração); o longo começa a canalizar.
    (Fase 1b) Com o DOMÍNIO (uma vez por luta): sem Mana, sem ser longo, e os dados rolados duas vezes."""
    g = T.FEITICOS[k]['grau']; forc = falta_mao(f, k, fonte); forcado = forc > 0
    if dominio and fonte is None and dominio_pronto(S, f):
        f['usou'].append('dominio'); conta(S, 'dominio'); L.diz(S, f"  {f['nome']} lança {nome(k)} pelo Domínio: sem Mana, de uma vez, os dados rolados duas vezes")
        if f.get('foco') and f['foco'] not in S['usadas']: S['usadas'].append(f['foco'])
    else: dominio = False
    if dominio: pass
    elif fonte is None:
        q = custo(f, k)
        if S.get('hab') and 'mana_curta' in (f.get('hab') or {}) and not f.get('mana_curta'):      # (fase 2) A MANA CURTA: o primeiro feitiço da luta custa menos
            f['mana_curta'] = True; q = max(0, q - HT.num('mana_curta', 'menos', f['hab']['mana_curta'])); f.setdefault('hab_usos', {})['mana_curta'] = 1
        if f['mana'] >= q: f['mana'] -= q; conta(S, 'mana_gasta', q)
        else:                                                    # NO OSSO: o que falta sai do PV, e o lance é forçado
            pv = math.ceil((q - f['mana']) * TM.SEM_MANA_PV * f['pvmax']); conta(S, 'mana_gasta', f['mana']); f['mana'] = 0; f['pv'] -= pv; forcado = True; S['dano_r'] += pv / f['pvmax']
            L.diz(S, f"  {f['nome']} lança {nome(k)} NO OSSO: falta Mana, e paga {pv} de PV ({max(f['pv'], 0)}/{f['pvmax']})")
            if f['pv'] <= 0: L._cai(S, f, 0); return
        if f.get('foco') and f['foco'] not in S['usadas']: S['usadas'].append(f['foco'])      # o foco perde 1 por luta em que lançou
        if f.get('tradicao') == 'pacto' and T.FEITICOS[k]['de'] == 'pacto' and g in W.DIVIDA_GRAU: f['divida'] = f.get('divida', 0) + W.DIVIDA_GRAU[g]      # o feitiço de pacto soma dívida, como fora da luta (volta ao estado)
        _aviso_mana(S, f)
    else:
        e = f['encantos'][fonte]; e['carregado'] = False; iid = S['itens'][e['item']].get('id')
        if iid: _lista(f, 'encantos_gastos').append([iid, e['idx']])
        L.diz(S, f"  {f['nome']} solta o encanto de {e['nome']}")
    colados = [x for x in L.inimigos(S, f) if L.dist(f, x) <= 1]
    if colados:                                                  # lançar com o inimigo colado: ele bate antes
        pv0 = f['pv']; L._golpe_livre(S, f, 'lança com o inimigo colado', quem=colados)
        if f['estado'] != 'pe': return
        if f['pv'] < pv0:
            f['canaliza'] = dict(nome=k, trad=trad_de(f, k)); ok = concentra(S, f, pv0 - f['pv'] >= f['pvmax'] * T.FERIDA)
            if not ok: return
            f['canaliza'] = None
    if S.get('hab') and f.get('hab'): import habilidade; habilidade.lancou(S, f)      # (fase 2) A Corrente soma depois do feitiço (vale no seguinte)
    cedo = bool(S.get('hab') and g in TM.LONGO and not dominio and _cedo(S, f))       # (fase 2) A MÃO NO RITO: o longo sai uma rodada mais cedo
    if g in TM.LONGO and not dominio and not cedo:              # O LONGO: gasta o turno agora e sai no começo do turno seguinte (o Domínio o solta de uma vez)
        f['canaliza'] = dict(nome=k, alvo=alvo, casa=casa, trad=trad_de(f, k), fonte=fonte, forc=forc, forcado=forcado, r=TM.LONGO[g], campo=campo)
        L.diz(S, f"  {f['nome']} começa a canalizar {nome(k)}" + (f" em {alvo}" if alvo else '') + ' (sai no começo do próximo turno)'); conta(S, 'longos')
        if f['lado'] == 'B': _para_todos(S, f"{f['nome']} começou a canalizar {nome(k)}: sai no próximo turno, se ninguém o atrapalhar")
        return
    resolve(S, f, k, alvo, casa, fonte, forc, forcado, campo, dominio)


def _cedo(S, f):
    """(fase 2) a Mão no Rito: do Adepto, o longo sai uma rodada mais cedo uma vez por luta; do Mestre, sempre"""
    gr = (f.get('hab') or {}).get('mao_rito', -1)
    if gr < 2: return False
    if HT.num('mao_rito', 'cedo', gr) <= f.get('rito_cedo', 0): return False
    f['rito_cedo'] = f.get('rito_cedo', 0) + 1; f.setdefault('hab_usos', {})['mao_rito'] = f['hab_usos'].get('mao_rito', 0) + 1
    L.diz(S, f"  a Mão no Rito: o feitiço longo de {f['nome']} sai de uma vez"); return True


def _aviso_mana(S, f):
    if not f.get('controla') or not f.get('mana_max'): return
    if f['mana'] < f['mana_max'] * TM.MANA_AVISO:
        if not f.get('avisou_mana'): f['avisou_mana'] = True; L._para(S, f, f"{f['nome']} está com a Mana abaixo de um terço ({mana_diz(f).replace('/', ' de ')})")
    else: f['avisou_mana'] = False


def _inimigo(S, f, alvo, alc):
    """o alvo hostil: o que veio (se ainda está de pé e ao alcance), senão o inimigo mais perto ao alcance"""
    e = L.por_nome(S, alvo) if alvo else None
    if e is not None and e['estado'] == 'pe' and e['lado'] != f['lado'] and L.dist(f, e) <= max(alc, 1): return e
    al = [x for x in L.inimigos(S, f) if L.dist(f, x) <= max(alc, 1)]
    return min(al, key=lambda x: L.dist(f, x)) if al else None


def _aliado(S, f, alvo, alc, caido=False):
    """o alvo amigo: o que veio (de pé, ou caído se a cura o alcança) ao alcance; senão, quem lança"""
    a = L.por_nome(S, alvo) if alvo else None
    if a is not None and a['lado'] == f['lado'] and (a['estado'] == 'pe' or (caido and a['estado'] == 'caido')) and L.dist(f, a) <= max(alc, 1): return a
    return f


def _dom_fez(S, f, dom, j, contra):
    if dom and not j['crit'] and j['total'] - dom < contra:      # o dom de tradição decidiu este lance (a luta que volta ao estado faz disto a marca.dom_visto)
        if f.get('controla') and not f.get('dom_fez'): L.diz(S, f"    ({f['nome']} acerta por pouco: sem o dom, errava)")
        f['dom_fez'] = True


def _dano(S, f, e, dado, c, vezes, fm, crit, dominio=False, chama=False):
    """o tamanho do feitiço: dado × 4 × valor do foco ÷ guarda × força (o crítico dobra os dados e corta a guarda pela metade). O amuleto que guardou gasta.
    (Fase 1b) A PILHA no feitiço: a Chama do foco (PEÇAS), o alvo exposto e quem lança amolecido (ESTADOS), a Guarda Mágica do alvo (a couraça do feitiço, em curva);
    o Domínio rola os dados duas vezes (nunca mais de 4); e o teto da pilha (7 vezes o feitiço de hoje, com os mesmos dados)."""
    g, am = guarda(S, e)
    if am:
        if am not in S['usadas']: S['usadas'].append(am)            # o amuleto perde 1 por luta em que guardou...
        if c > e['amuleto_cat']: _gasta(S, e, am, 1, 'amuleto')      # ... e 1 a cada feitiço de foco maior que ele
    vh = 2 if crit else 1; m = 1
    ch = _fx_foco(S, f, 'chama') if (f is not e or chama) and not f.get('bicho') else None      # (no próprio corpo, só o feitiço que a Refletora devolveu leva a Chama de quem lançou; o retrochoque, não)
    if ch: m *= 1 + min(TE.PILHA['pecas'], ch)
    if e.get('exposto', -1) >= S['r']: m *= TE.EXPOSTO
    if f.get('amolecido', -1) >= S['r']: m *= TE.AMOLECIDO
    gm = L.efeito(S, e, 'guarda_magica')
    if gm: m *= 1 - TE.curva(gm)
    hb = S.get('hab') and f.get('hab') and f is not e      # (fase 2) a Corrente (TÉCNICA) e o Rito de Veia (o dado somado) no feitiço de quem as tem
    tec = (f.get('corrente') or 0) * HT.CORRENTE_DANO if hb else 0
    if tec: m *= 1 + min(TE.PILHA['tecnica'], tec)
    import habilidade
    rito = habilidade.rito_dado(f) if hb else 0
    if m == 1 and not dominio and not rito: return int(L.rola(dado, vh) * TM.K * T.MULT[c] * vezes / (g / (2 if crit else 1)) * fm)
    nd, fd = map(int, dado.split('d')); vz = min(TE.DADOS_MAX, vh * 2) if dominio else vh; rolos = [L.D.d(fd) for _ in range(nd * vz)]
    xr = L.D.d(rito) if rito else 0                         # o dado somado: uma vez, sem dobrar no crítico (P2)
    hoje = int(sum(rolos[:nd * vh]) * TM.K * T.MULT[c] * vezes / (g / (2 if crit else 1)) * fm)
    return min(TE.TETO_PILHA * hoje, int((sum(rolos) + xr) * TM.K * T.MULT[c] * vezes / (g / (2 if crit else 1)) * fm * m))      # o dano 0 de hoje segue 0 (P1), com ou sem o dado do Rito


def fere(S, a, e, dano, crit, k, c, queima=False, atordoa=0):
    """o fim de um feitiço que tira PV: a ferida, a queda, a moral, a concentração e a fase (como o fim do golpe de aço)"""
    e['pv'] -= dano; e['agressor'] = a['nome']; conta(S, k + '_acertos'); conta(S, k + '_dano', dano); conta(S, k + '_frac', dano / e['pvmax'])
    L.diz(S, f"    {nome(k)}: {dano} em {e['nome']} ({max(e['pv'], 0)}/{e['pvmax']})")
    if dano <= 0: return False
    S['dano_r'] += dano / e['pvmax']
    if e.get('funda') is None or e['funda'] < c: e['funda'] = c
    terrivel = dano >= e['pvmax'] * T.FERIDA_GRAVE; abertas = len(e['feridas']); parte = T.ONDE[L.D.d(10)]
    if e['pv'] <= 0: L._cai(S, e, dano)
    elif dano >= e['pvmax'] * T.FERIDA or (crit and dano >= e['pvmax'] * T.FERIDA_MIN): L._ferida(S, e, parte, terrivel, dict(efeitos={}, queima=queima), dano)
    abriu = len(e['feridas']) > abertas
    if abriu and atordoa and e['estado'] == 'pe': e['atordoado'] = max(e['atordoado'], atordoa); L.diz(S, f"    {e['nome']} fica atordoado (perde {L._acoes(atordoa)})")
    if e.get('bicho') and abriu and e['estado'] == 'pe': L._moral(S, e, 'ferido')
    if terrivel:
        for o in L.de_pe(S, e['lado']):
            if o is not e and L.dist(o, e) <= 2: L._moral(S, o, 'golpe_terrivel')
    if e['estado'] == 'pe' and e['pv'] < e['pvmax'] * 0.25: L._moral(S, e, 'ferido_grave')
    apanhou(S, e, dano, abriu)
    return abriu


def retro(S, f, k, j, c, vezes, fm, forcado):
    """o RETROCHOQUE: quem lança vai ao chão e perde 1 ação, e o foco perde 1; no forçado, leva ainda o próprio feitiço contra a própria guarda"""
    if not j['falha']: return False
    conta(S, 'retrochoque'); f['chao'] = True; f['atordoado'] = max(f['atordoado'], 1)
    L.diz(S, f"  {f['nome']} lança {nome(k)}: {'um 1 no lance forçado' if forcado else 'dois 1'}, RETROCHOQUE (vai ao chão e perde 1 ação)")
    if f.get('foco') and not f.get('bicho'): _gasta(S, f, f['foco'], 1, 'foco')
    L._para(S, f, f"{f['nome']} sofreu o retrochoque de {nome(k)}", so_controlado=True)
    if forcado and TM.FEITICOS[k].get('dado'): fere(S, f, f, _dano(S, f, f, TM.FEITICOS[k]['dado'], c, vezes, fm, False), False, k, c)
    return True


def maldito(S, e):
    """é maldito? (o castigo fere inteiro): amaldiçoado, com peça maldita, bicho que amaldiçoa, ou imaterial"""
    return bool(e.get('maldicoes') or e.get('maldicoes_postas') or e.get('maldito') or tem(e, 'amaldiçoa') or tem(e, 'imaterial'))


def _refletora(S, f, e, k):
    """(fase 1b) A REFLETORA: uma vez por luta, o feitiço que voa contra o dono do escudo (inteiro, com a arma de uma mão em uso) volta em quem lançou, e rola de novo, contra a
    defesa dele (o feitiço não chega ao dono: é devolvido antes do dado; com a Chama de quem lançou). A outra leitura, a de gastar a Refletora só no feitiço que pegaria no
    dono, mediu +23,1 no banco (o teto do forte é 20): fica a de devolver o primeiro (+20,0)"""
    if e is f or 'refletora' in e.get('usou', []) or not L.efeito(S, e, 'refletora'): return e
    e['usou'].append('refletora'); conta(S, 'refletora')
    L.diz(S, f"  a Refletora de {e['nome']} devolve {nome(k)} em {f['nome']}")
    return f


def resolve(S, f, k, alvo=None, casa=None, fonte=None, forc=0, forcado=False, campo=None, dominio=False):
    """o feitiço sai (o curto, na hora; o longo, no começo do turno seguinte). (Fase 1b) O Domínio: os dados rolados duas vezes; a Refletora: o feitiço volta em quem lançou
    (rola de novo, contra ele; o dano devolvido leva a Chama de quem lançou)"""
    sp = TM.FEITICOS[k]; t = sp['tipo']; bon, c, vezes, dom, fm = conj(S, f, k, fonte); bon += TM.FORCADO * forc; conta(S, 'lances')
    if t in ('dano', 'poe', 'medo'):
        e = _inimigo(S, f, alvo, sp['alc'])
        if e is None: L.diz(S, f"  {f['nome']} lança {nome(k)}, mas não há em quem"); return
        e = _refletora(S, f, e, k); refl = e is f
        if t == 'dano':
            j = jogada(bon + mira(S, f, e, False), forcado); df = defesa(S, f, e, False); conta(S, k + '_lances')
            if retro(S, f, k, j, c, vezes, fm, forcado): return
            if j['total'] < df and not j['crit']: L.diz(S, f"  {f['nome']} lança {nome(k)} em {e['nome']}: {L._n(j['total'])} contra {L._n(df)}, erra"); return
            _dom_fez(S, f, dom, j, df)
            dado = sp['dado'] if not sp.get('dado_outro') or maldito(S, e) else sp['dado_outro']
            L.diz(S, f"  {f['nome']} lança {nome(k)} em {e['nome']}: {L._n(j['total'])} contra {L._n(df)}" + (', CRÍTICO' if j['crit'] else ''))
            pv0 = max(e['pv'], 0); dano = _dano(S, f, e, dado, c, vezes, fm, j['crit'], dominio, chama=refl); fere(S, f, e, dano, j['crit'], k, c, sp.get('queima'), sp.get('atordoa', 0)); tirou = min(dano, pv0)
            if tirou > 0 and sp.get('rouba') and f['estado'] == 'pe' and f['pv'] < f['pvmax']:
                g = min(f['pvmax'] - f['pv'], int(tirou * sp['rouba'])); f['pv'] += g; S['dano_r'] -= g / f['pvmax']; L.diz(S, f"    {f['nome']} recupera {g} ({f['pv']}/{f['pvmax']})")
            if tirou > 0 and sp.get('veneno') and e['estado'] == 'pe' and not sem_vida(e):
                q = max(1, int(tirou * sp['veneno'][0])); ant = e['veneno'] or [0, 0]; e['veneno'] = [max(q, ant[0]), sp['veneno'][1]]; e['veneno_cat'] = max(e.get('veneno_cat', 0), c)
                L.diz(S, f"    o veneno entra em {e['nome']} ({e['veneno'][0]} por rodada)")
            return
        if t == 'medo' and sp.get('so_bicho') and not e.get('bicho'): L.diz(S, f"  {f['nome']} lança {nome(k)} em {e['nome']}: só o bicho se afugenta"); return
        j = jogada(bon, forcado); fz = firmeza(S, e, k); conta(S, k + '_lances')
        if retro(S, f, k, j, c, vezes, fm, forcado): return
        if j['total'] < fz and not j['crit']: L.diz(S, f"  {f['nome']} lança {nome(k)} em {e['nome']}: {L._n(j['total'])} contra a Firmeza {L._n(fz)}, não pega"); return
        _dom_fez(S, f, dom, j, fz); e['calejo'] = e.get('calejo', 0) + 1; conta(S, k + '_acertos')
        fam = TE.FEITICO_FAMILIA.get(k)
        if fam and isinstance(e.get('calejo_m'), dict): e['calejo_m'][fam] += 1        # (fase 1b) o feitiço de controle que pega dá também +4 na resistência à carga da família dele
        L.diz(S, f"  {f['nome']} lança {nome(k)} em {e['nome']}: {L._n(j['total'])} contra a Firmeza {L._n(fz)}, PEGA")
        if t == 'medo': L._moral(S, e, 'medo'); return
        s = e.setdefault('est', {}); q = sp['poe']; s[q] = max(s.get(q) or 0, sp['dur'])
        txt = dict(preso=f"está PRESO por {sp['dur']} turnos: não anda", olhado=f"leva o MAU-OLHADO ({TM.ESTADOS['olhado']['acerto']} no acerto, {TM.ESTADOS['olhado']['defesa']} na Defesa e {TM.ESTADOS['olhado']['conj']} na Conjuração)".replace('-', '−'), no=f"tem a Mana ATADA por {sp['dur']} turnos")[q]
        L.diz(S, f"    {e['nome']} {txt}"); L._para(S, e, f"{e['nome']} {txt}", so_controlado=True)
        return
    if t == 'area':
        x = casa if casa is not None else (L.por_nome(S, alvo) or _inimigo(S, f, None, sp['alc']) or {}).get('x')
        if x is None or abs(x - f['x']) > sp['alc']: L.diz(S, f"  {f['nome']} lança {nome(k)}, mas não alcança"); return
        L.diz(S, f"  {f['nome']} lança {nome(k)} na casa {x}"); feitos = 0
        for e in [o for o in L.de_pe(S) if o['x'] == x and o is not f][:TM.AREA_ALVOS]:   # a área fere amigo e inimigo
            if f['estado'] != 'pe' or e['estado'] != 'pe': continue
            j = jogada(bon + mira(S, f, e, True), forcado); df = defesa(S, f, e, True); conta(S, k + '_lances')
            if retro(S, f, k, j, c, vezes, fm, forcado): return
            if j['total'] < df and not j['crit']: L.diz(S, f"    em {e['nome']}: {L._n(j['total'])} contra {L._n(df)}, erra"); continue
            _dom_fez(S, f, dom, j, df); feitos += 1
            L.diz(S, f"    em {e['nome']}: {L._n(j['total'])} contra {L._n(df)}" + (', CRÍTICO' if j['crit'] else ''))
            fere(S, f, e, _dano(S, f, e, sp['dado'], c, vezes, fm, j['crit'], dominio), j['crit'], k, c)
        return
    if forcado and retro(S, f, k, jogada(0, True), c, vezes, fm, True): return        # o que não rola contra ninguém, rola só para o retrochoque do lance forçado
    if t == 'escudo':
        a = _aliado(S, f, alvo, sp['alc']); s = a.setdefault('est', {}); s['guardado'] = max(s.get('guardado') or 0, sp['dur'])
        L.diz(S, f"  {f['nome']} ergue o escudo {'em si' if a is f else 'em ' + a['nome']} (+{TM.ESTADOS['guardado']['defesa']} na Defesa por {sp['dur']} turnos)")
    elif t == 'bencao':
        a = _aliado(S, f, alvo, sp['alc']); a.setdefault('est', {})['benzido'] = TM.PRAZO_SEM_FIM; conta(S, 'bencaos')
        L.diz(S, f"  {f['nome']} benze {'a si' if a is f else a['nome']} (+{TM.ESTADOS['benzido']['acerto']} no acerto e +{TM.ESTADOS['benzido']['coragem']} na coragem até o fim da luta)")
    elif t == 'guarda':
        ok = [o for o in L.de_pe(S, f['lado']) if o['x'] == f['x']][:TM.AREA_ALVOS]
        for o in ok: o.setdefault('est', {})['guarda'] = [c, sp['dur']]
        L.diz(S, f"  {f['nome']} guarda {', '.join(o['nome'] for o in ok)} (contam como tendo amuleto {T.CATS[c]} por {sp['dur']} turnos)")
    elif t == 'cura':
        a = _aliado(S, f, alvo, sp['alc'], caido=True); g = cura(S, a, sp['dado'], c); conta(S, 'cura_lances'); conta(S, 'cura_pv', g)
        L.diz(S, f"  {f['nome']} cura {'a si' if a is f else a['nome']} (+{g}: {a['pv']}/{a['pvmax']})" + ('' if g else ': a cura do dia já chegou ao teto, ou não havia o que curar'))
        if a['estado'] == 'caido': _firma(S, a)
    elif t == 'amparo':
        a = _aliado(S, f, alvo, sp['alc'], caido=True); feito = []
        if a.get('sangra') or a.get('filetes'): a['sangra'] = None; a.pop('queimando', None); a['filetes'] = []; feito.append('estanca o sangue')      # (fase 1b) todos os filetes, como hoje
        if a.get('veneno') and a.get('veneno_cat', 0) <= c: a['veneno'] = None; feito.append('tira o veneno')
        if a['estado'] == 'caido' and max(a['morte']) < 3: a['morte'][0] = 3; feito.append('firma quem caiu')
        L.diz(S, f"  {f['nome']} ampara {'a si' if a is f else a['nome']}: " + (', '.join(feito) if feito else 'nada a fazer'))
    elif t == 'seiva':
        a = _aliado(S, f, alvo, sp['alc']); s = a.setdefault('est', {}); s['seiva'] = max(s.get('seiva') or 0, sp['dur'])
        L.diz(S, f"  {f['nome']} dá a seiva a {'si' if a is f else a['nome']} ({TM.ESTADOS['seiva']:.0%} do PV por rodada, por {sp['dur']} rodadas)")
    elif t == 'campo': poe_campo(S, f, k, campo)
    elif t == 'chamar': chama(S, f, c)


def cura(S, a, dado, c):
    """devolve dado × 6 × 3^(categoria da cura − categoria da ferida mais funda), sem passar do PV máximo nem do teto do dia (metade do PV máximo, feitiço e poção somados)"""
    teto = max(0, int(a['pvmax'] * T.CURA_TETO) - a.get('curado', 0))
    g = max(0, min(a['pvmax'] - a['pv'], teto, int(T.cura(L.rola(dado), c, a.get('funda')))))
    if S.get('hab') and (a.get('usos') or {}).get('rito_veia'): g //= 2           # (fase 2) o Rito de Veia: a cura de magia na cena vale metade em quem o abriu
    a['pv'] += g; a['curado'] = a.get('curado', 0) + g; S['dano_r'] -= g / a['pvmax']
    return g


def _firma(S, a):
    """quem caiu e recebe cura (ou poção) fica firme: não morre no chão, mas não se levanta nesta luta"""
    if max(a['morte']) < 3: a['morte'][0] = 3
    L.diz(S, f"    {a['nome']} fica firme no chão: não morre, mas não se levanta nesta luta")


def poe_campo(S, f, k, qual=None):
    """o feitiço de campo: a luz tira o escuro; a névoa põe neblina ou lama. Dura enquanto quem lançou paga 1 de Mana por rodada (e está de pé)."""
    sp = TM.FEITICOS[k]; cp = S.setdefault('campo', {})
    if sp.get('tira'):
        tinha = sp['tira'] in S['tempo']
        if tinha: S['tempo'].remove(sp['tira'])
        cp[k] = dict(quem=f['nome'], tira=sp['tira'], tinha=tinha); txt = f"a luz de {f['nome']} {'tira o escuro' if tinha else 'acende'}"
    else:
        q = qual if qual in sp['poe_campo'] else sp['poe_campo'][0]; poe = q not in S['tempo']
        if poe: S['tempo'].append(q)
        cp[k] = dict(quem=f['nome'], poe=q, pos=poe); txt = f"{f['nome']} chama a {q}"
    L.diz(S, f"  {txt}"); _para_todos(S, f"o campo mudou: {txt}")


def acaba_campo(S, k):
    v = (S.get('campo') or {}).pop(k, None)
    if not v: return
    if v.get('tinha') and v['tira'] not in S['tempo']: S['tempo'].append(v['tira'])
    if v.get('pos') and v['poe'] in S['tempo']: S['tempo'].remove(v['poe'])
    txt = f"{'a luz' if v.get('tira') else 'a ' + v['poe']} de {v['quem']} se desfaz"
    L.diz(S, f"  {txt}"); _para_todos(S, f"o campo mudou: {txt}")


def chama(S, f, c):
    """o "chamar" do druida: um bicho da contagem do ermo onde se luta (S['ermo']), até a categoria do foco, vem lutar ao lado de quem chamou.
    Só atende o bicho de verdade: os da página dos bichos e as criaturas que são fera (a harpia, o lobisomem); o povo e os mortos não ouvem o druida."""
    import bichos
    from pessoas import ficha
    ok = []
    for esp in S.get('ermo') or []:
        e = TB.ESPECIES.get(esp)
        if e is None:
            try:
                import tabelas_criaturas as TC; e = TC.ESPECIES.get(esp)
            except ImportError: e = None
            if e is not None and not e.get('fera'): e = None
        if e is not None and e.get('cat', 9) <= c and not e.get('chefe'): ok.append((e['cat'], esp))
    if not ok: L.diz(S, f"  {f['nome']} chama, e nada do ermo responde"); return
    esp = max(ok)[1]; n = 1; nm = f"{esp} chamado"
    while L.por_nome(S, nm): n += 1; nm = f"{esp} chamado {n}"
    b = L._entra(S, ficha(bichos.bicho(esp, nome=nm)), f['lado'], f['x'])
    S.setdefault('chamados', []).append(dict(especie=esp, nome=b['nome'], lado=f['lado']))
    L.diz(S, f"  {f['nome']} chama, e {b['nome']} vem do ermo lutar ao lado"); _para_todos(S, f"{b['nome']} veio do ermo ao chamado de {f['nome']}")


# ---------- beber ----------
def _pocao(f, bem):
    """(o tipo, a categoria, o id do elixir) da poção que o lutador leva: 'cura:1' (bem da carga) ou 'elixir:ID'"""
    if bem.startswith('elixir:'):
        x = next((x for x in f.get('elixires') or [] if x['id'] == bem[7:]), None)
        return (x['pocao'], x['cat'], x['id']) if x else (None, None, None)
    n, _, c = bem.partition(':')
    return (n, int(c), None) if (f.get('carga') or {}).get(bem, 0) > 0 and c.isdigit() else (None, None, None)


def pocoes(f, tipo):
    """[(categoria, bem)] das poções deste tipo que o lutador leva, da melhor para a pior"""
    out = [(int(b.partition(':')[2]), b) for b, q in (f.get('carga') or {}).items() if q > 0 and b.partition(':')[0] == tipo and b.partition(':')[2].isdigit()]
    out += [(x['cat'], 'elixir:' + x['id']) for x in f.get('elixires') or [] if x.get('pocao') == tipo]
    return sorted(out, key=lambda t: -t[0])


def nome_pocao(n, c): return f"{('o elixir de ' + n) if c > 2 else ({'antídoto': 'o antídoto', 'cura': 'a poção de cura', 'mana': 'a poção de Mana', 'guarda': 'a poção de guarda', 'fúria': 'a poção de fúria'}.get(n, n))} {T.CATS[c]}"


def bebe(S, f, bem, alvo=None):
    """beber (1 ação): a poção sai da carga (ou o elixir some) na hora; dar de beber a um aliado colado, também. Além do que o corpo aguenta no dia (Vigor ÷ 30),
    cada poção pede Vigor contra 24 + 4 por poção a mais: falhou, não faz nada e enjoa."""
    a = L.por_nome(S, alvo) if alvo else f
    if a is None or a['lado'] != f['lado'] or a['estado'] not in ('pe', 'caido') or L.dist(f, a) > 1: a = f
    n, c, eid = _pocao(f, bem)
    if n is None: return
    if eid: f['elixires'] = [x for x in f['elixires'] if x['id'] != eid]; _lista(f, 'elixires_gastos').append(eid)
    else:
        f['carga'][bem] -= 1; gs = f.setdefault('gastou', {}); gs[bem] = gs.get(bem, 0) + 1
        if f['carga'][bem] <= 0: f['carga'].pop(bem)
    conta(S, 'pocoes'); qp = nome_pocao(n, c); quem = f"{f['nome']} bebe {qp}" if a is f else f"{f['nome']} dá de beber {qp} a {a['nome']}"
    a['doses'] = a.get('doses', 0) + 1; at = a.get('atributos') or {}; lim = T.doses_dia(at.get('Vigor', 50))
    if a['doses'] > lim:
        cd = T.ENJOO[0] + T.ENJOO[1] * (a['doses'] - lim); t = sum(L.d20x()) + sum(L.d20x()) + at.get('Vigor', 50) // 10
        if t < cd: a.setdefault('est', {})['enjoo'] = True; L.diz(S, f"  {quem}: o corpo não aguenta mais hoje (Vigor {t} contra {cd}): não faz nada, e enjoa ({TM.ESTADOS['enjoo']} em tudo)".replace('-', '−')); return
        L.diz(S, f"  {a['nome']} já passou do que o corpo aguenta hoje, e aguenta mais esta (Vigor {t} contra {cd})")      # o dado que passou também vai à mesa
    if n == 'cura':
        g = cura(S, a, TM.POCAO_CURA, c); conta(S, 'pocao_pv', g); L.diz(S, f"  {quem} (+{g}: {a['pv']}/{a['pvmax']})" + ('' if g else ': a cura do dia já chegou ao teto'))
        if a['estado'] == 'caido': _firma(S, a)
    elif n == 'antídoto':
        ok = bool(a.get('veneno')) and a.get('veneno_cat', 0) <= c
        if ok: a['veneno'] = None
        L.diz(S, f"  {quem}: " + ('o veneno sai' if ok else 'o veneno é forte demais para ele' if a.get('veneno') else 'não havia veneno'))
    elif n == 'mana':
        g = min(a.get('mana_max', 0) - a.get('mana', 0), TM.POCAO_MANA * (c + 1)) if a.get('mana_max') else 0
        if g: a['mana'] += g
        L.diz(S, f"  {quem} (+{g} de Mana" + (f": {mana_diz(a)})" if a.get('mana_max') else ')'))
    elif n == 'guarda':
        s = a.setdefault('est', {}); s['guarda_p'] = max(c, s.get('guarda_p') if s.get('guarda_p') is not None else -1)
        L.diz(S, f"  {quem}: conta como tendo amuleto {T.CATS[c]} até o fim da luta")
    elif n == 'fúria':
        a.setdefault('est', {})['furia'] = [TM.ESTADOS['furia']['rodadas'], c]
        w = L.arma_de(S, a); L.diz(S, f"  {quem}: " + (f"+{TM.ESTADOS['furia']['acerto']} no acerto e {TM.ESTADOS['furia']['defesa']} na Defesa por {TM.ESTADOS['furia']['rodadas']} rodadas" if w['cat'] <= c else f"a fúria {T.CATS[c]} não alcança quem empunha {w['nome']}").replace('-', '−'))


# ---------- a luta chama no começo e no fim de cada turno, e no fim de cada rodada ----------
def comeco(S, f):
    """o começo do turno: a Mana volta (menos a de quem está com o nó), o campo se paga, o feitiço longo sai (ou se perde sem teste)"""
    if f.get('feiticos') and f.get('mana_max') and not ve(f, 'no'): f['mana'] = min(f['mana_max'], f['mana'] + TM.MANA_LUTA)
    for k, v in list((S.get('campo') or {}).items()):
        if v['quem'] == f['nome']:
            if f.get('mana', 0) >= TM.SUSTENTA: f['mana'] -= TM.SUSTENTA
            else: acaba_campo(S, k)
    c = f.get('canaliza')
    if c:
        if f['chao'] or f['atordoado'] or f.get('perde_turno') or L._agarrado(S, f): perde(S, f, 'sem teste'); return
        c['r'] -= 1
        if c['r'] <= 0:
            f['canaliza'] = None; L.diz(S, f"  {f['nome']} solta {nome(c['nome'])}"); resolve(S, f, c['nome'], c['alvo'], c['casa'], c['fonte'], c['forc'], c['forcado'], c.get('campo')); L._fim(S)


def fim_turno(S, f):
    """os prazos que contam em turnos de quem os tem: preso, cego, guardado, nó, a guarda do clérigo"""
    s = f.get('est') or {}
    if sem_vida(f): f['fol'] = f['folmax']
    for k in ('preso', 'cego', 'guardado', 'no'):
        if s.get(k):
            s[k] -= 1
            if s[k] <= 0:
                s.pop(k)
                if k == 'preso' and f['estado'] == 'pe': L.diz(S, f"  {f['nome']} se solta")
    if s.get('guarda'):
        s['guarda'][1] -= 1
        if s['guarda'][1] <= 0: s.pop('guarda')


def fecha_rodada(S):
    """o fim da rodada: a seiva cura, os prazos em rodadas andam (a fúria, o benzido do brado), o campo de quem caiu se desfaz, o chefe muda de fase"""
    for f in L.de_pe(S):
        s = f.get('est') or {}
        if s.get('seiva'):
            teto = max(0, int(f['pvmax'] * T.CURA_TETO) - f.get('curado', 0))
            g = min(f['pvmax'] - f['pv'], teto, max(1, int(f['pvmax'] * TM.ESTADOS['seiva'])))
            if g > 0: f['pv'] += g; f['curado'] = f.get('curado', 0) + g; S['dano_r'] -= g / f['pvmax']; L.diz(S, f"  {f['nome']} se refaz com a seiva (+{g}: {f['pv']}/{f['pvmax']})")
            s['seiva'] -= 1
            if s['seiva'] <= 0: s.pop('seiva')
        if s.get('benzido') and s['benzido'] < TM.PRAZO_SEM_FIM:
            s['benzido'] -= 1
            if s['benzido'] <= 0: s.pop('benzido')
        if s.get('furia'):
            s['furia'][0] -= 1
            if s['furia'][0] <= 0: s.pop('furia')
    for k, v in list((S.get('campo') or {}).items()):
        q = L.por_nome(S, v['quem'])
        if not q or q['estado'] != 'pe': acaba_campo(S, k)
    for f in S['L']:
        if f.get('canaliza') and f['estado'] != 'pe': perde(S, f, 'sem teste')        # quem caiu (pelo sangue, pelo veneno) perde o feitiço que canalizava
        if f.get('fases') and f['estado'] == 'pe': fase(S, f)


def fecha_luta(S):
    """a luta acabou: o campo se desfaz e o feitiço que se canalizava se perde (a Mana dele já foi)"""
    for k in list(S.get('campo') or {}): (S['campo'].pop(k, None))
    for f in S['L']:
        f['canaliza'] = None; f.pop('_restam', None)


# ---------- as fases do chefe ----------
def fase(S, e):
    """o chefe cruzou o limiar do PV: ganha e perde traços, aprende feitiços, recobra Mana, dá o brado (os seus ficam benzidos) e ergue os mortos; a luta para e pergunta.
    A FASE "foge" (etapa 4b, E3 a): se ele está no ar (voa, e não está no chão, preso, agarrado nem num corredor) e o lado dele tem saída (o cenário não diz sem_saida dele),
    foge pelo ar, sem golpe livre; senão, a fase vale como fúria (perde e ganha os traços dela). No covil, quem monta a luta põe sem_saida do lado do dragão."""
    for i, fs in enumerate(e['fases'], 1):
        if e.get('fase', 0) >= i or e['estado'] != 'pe' or e['pv'] > e['pvmax'] * fs.get('abaixo', 0): continue
        e['fase'] = i
        if fs.get('foge') and L._no_ar(S, e) and S['lugar'].get('sem_saida') != e['lado']:
            e['estado'] = 'fugiu'; txt = fs.get('foge_diz') or 'foge pelo ar, ferido'
            L.diz(S, f"  ◆ {e['nome']}: {txt} ({max(e['pv'], 0)}/{e['pvmax']})"); _para_todos(S, f"{e['nome']} fugiu: {txt}"); conta(S, 'fugas')
            if e.get('lider'):
                for o in L.de_pe(S, e['lado']): L._moral(S, o, 'lider_caiu')
            L._fim(S); return
        e['tracos'] = [t for t in e.get('tracos') or [] if t not in (fs.get('perde') or [])] + [t for t in fs.get('ganha') or [] if t not in (e.get('tracos') or [])]
        if sem_vida(e): e['moral'] = 'firme'
        if fs.get('feiticos'):
            e['feiticos'] = list(dict.fromkeys(list(e.get('feiticos') or []) + list(fs['feiticos'])))
            if not e.get('mana_max'): at = e.get('atributos') or {}; e['mana_max'] = T.mana_max(at.get('Afinidade', 40), at.get('Vontade', 45), e.get('maestria', 0)); e['mana'] = 0
        if fs.get('mana') and e.get('mana_max'): e['mana'] = min(e['mana_max'], e.get('mana', 0) + fs['mana'])
        L.diz(S, f"  ◆ {e['nome']}: {fs.get('diz', 'muda')}"); _para_todos(S, f"{e['nome']} mudou: {fs.get('diz', 'muda')}"); conta(S, 'fases')
        if fs.get('brado'):
            for o in L.de_pe(S, e['lado']):
                s = o.setdefault('est', {}); s['benzido'] = max(s.get('benzido') or 0, TM.BRADO)
            L.diz(S, f"    o brado de {e['nome']}: os seus ficam benzidos por {TM.BRADO} rodadas")
        if fs.get('ergue'): ergue(S, e, int(fs['ergue']))


def ergue(S, e, n):
    """levanta até n mortos (os mais perto dele), como "sem vida", do lado de quem os ergue. O corpo que se ergue é outro lutador: o morto segue morto."""
    mortos = sorted([o for o in S['L'] if o['estado'] == 'morto' and not o.get('erguido') and not tem(o, 'imaterial') and o is not e], key=lambda o: L.dist(o, e))[:n]
    for o in mortos:
        o['erguido'] = True; f = copy.deepcopy(o)
        for k in ('id', 'controla', 'lider', 'guarda', 'gastou', 'elixires_gastos', 'venenos_gastos', 'encantos_gastos', 'maldicoes_postas', 'marcas', 'dom_fez', 'erguido', 'estavel', 'moral_r', 'avisou_fol', 'avisou_mana', 'fase'):
            f.pop(k, None)
        nm = f"{o['nome']}, morto que anda"; i = 1
        while L.por_nome(S, nm): i += 1; nm = f"{o['nome']}, morto que anda ({i})"
        f.update(nome=nm, feridas=[], pv=max(1, int(f['pvmax'] * TM.ERGUE_PV)), moral='firme', papel='frente', est={}, calejo=0, canaliza=None, feiticos=[], mana=0, mana_max=0,
                 carga={}, elixires=[], encantos=[], fases=[], tracos=list(dict.fromkeys(list(f.get('tracos') or []) + ['sem vida'])), funda=None, doses=0, curado=0)
        f = L._entra(S, f, e['lado'], o['x']); f['chao'] = True
        L.diz(S, f"    {o['nome']} SE ERGUE, morto, do lado de {e['nome']}")
    if mortos: conta(S, 'erguidos', len(mortos))


# ---------- o que cada um decide ----------
def decide(S, f, o, pagou):
    """a ação de magia deste lutador agora, ou None (luta como sempre). Quem o jogador comanda só lança, bebe ou solta o encanto por ordem."""
    if f['estado'] != 'pe' or f['chao']: return None
    if f.get('controla'):
        a = o.get('acao')
        if a not in ('lancar', 'beber', 'usar'): return None
        return dict(lancar=_ordem_lancar, beber=_ordem_beber, usar=_ordem_usar)[a](S, f, o)
    return escolhe(S, f)


def _volta(S, f, txt=None):
    """a ordem de magia acabou (ou não pôde): volta a ordem de antes; a frase, se vier, para a luta"""
    o = S['ordens'].get(f['nome']) or {}; antes = o.get('antes')
    if antes: S['ordens'][f['nome']] = antes
    else: S['ordens'].pop(f['nome'], None)
    if txt: L._para(S, f, txt, so_controlado=True)


def _vai(S, f, x):
    """anda na direção da casa x (para pôr o alvo ao alcance), se pode"""
    if L._nao_anda(S, f) or x == f['x']: return ('espera',)
    dx = 1 if x > f['x'] else -1
    return ('anda', dx, False, None) if L._livre(S, f, f['x'] + dx, True) else ('espera',)


def _ordem_lancar(S, f, o, fonte=None):
    k = o['feitico']; sp = TM.FEITICOS[k]; t = sp['tipo']
    if TM.ACOES[T.FEITICOS[k]['grau']] > f.get('_restam', 0): return ('espera',)           # não cabe no que sobrou do turno: espera o próximo
    if fonte is None and f['mana'] < custo(f, k) and not o.get('osso') and not (o.get('dominio') and dominio_pronto(S, f)):
        _volta(S, f, f"{f['nome']} não tem Mana para {nome(k)} ({f['mana']} de {custo(f, k)}): lançar no osso custa PV (a ordem: lancar {k} osso)"); return None
    alvo = o.get('alvo'); casa = o.get('casa')
    if alvo:
        e = L.por_nome(S, alvo)
        if e is None or e['estado'] not in ('pe', 'caido') or (e['estado'] == 'caido' and t not in ('cura', 'amparo')):
            _volta(S, f, f"o alvo de {f['nome']} ({alvo}) não está mais de pé"); return None
        if L.dist(f, e) > max(sp['alc'], 1): return _vai(S, f, e['x'])
    elif casa is not None:
        if abs(casa - f['x']) > sp['alc']: return _vai(S, f, casa)
    elif t in HOSTIS:
        al = L.inimigos(S, f)
        if not al: return None
        e = min(al, key=lambda x: L.dist(f, x))
        if L.dist(f, e) > max(sp['alc'], 1): return _vai(S, f, e['x'])
        alvo = e['nome']
    return ('lanca', k, alvo, casa, dict(fonte=fonte, osso=o.get('osso'), campo=o.get('campo'), ordem=True, dominio=o.get('dominio') and fonte is None))


def _ordem_beber(S, f, o):
    bem = o['bem']
    if ':' not in bem or (bem.startswith('elixir:') and _pocao(f, bem)[0] is None) or (not bem.startswith('elixir:') and _pocao(f, bem)[0] is None):
        ps = pocoes(f, bem.partition(':')[0] if not bem.startswith('elixir:') else '')
        if not ps: _volta(S, f, f"{f['nome']} não tem mais {bem.partition(':')[0]} para beber"); return None
        bem = ps[0][1]
    if o.get('alvo'):
        a = L.por_nome(S, o['alvo'])
        if a is None or a['estado'] not in ('pe', 'caido'): _volta(S, f, f"{o['alvo']} não está mais na luta para beber"); return None
        if L.dist(f, a) > 1: return _vai(S, f, a['x'])
    return ('bebe', bem, o.get('alvo'), dict(ordem=True))


def _ordem_usar(S, f, o):
    i = o['encanto']; e = (f.get('encantos') or [])[i] if i < len(f.get('encantos') or []) else None
    if e is None or not e['carregado'] or e['dorme']: _volta(S, f, f"o encanto de {f['nome']} não está pronto (já saiu nesta luta, ou a peça dorme)"); return None
    return _ordem_lancar(S, f, dict(o, feitico=e['feitico']), fonte=i)


def _fim_da_ordem(S, f):
    o = S['ordens'].get(f['nome']) or {}
    if o.get('acao') in ('lancar', 'beber', 'usar') and not o.get('sempre'): _volta(S, f)
    elif o.get('sempre') and f.get('mana', 0) < custo(f, o['feitico']):
        _volta(S, f, f"{f['nome']} ficou sem Mana para seguir lançando {nome(o['feitico'])} ({f.get('mana', 0)} de {custo(f, o['feitico'])})")


def faz(S, f, ac):
    """a ação de magia (o luta._turno chama): lançar, soltar o encanto ou beber"""
    if ac[0] == 'bebe': bebe(S, f, ac[1], ac[2]); x = ac[3]
    else:
        x = ac[4]; dm = x.get('dominio') or (not x.get('ordem') and x.get('fonte') is None and T.FEITICOS[ac[1]]['grau'] >= 2 and dominio_pronto(S, f))      # (fase 1b) o robô solta o Domínio no primeiro feitiço de grau 2 ou mais
        lanca(S, f, ac[1], ac[2], ac[3], fonte=x.get('fonte'), osso=x.get('osso'), campo=x.get('campo'), dominio=dm)
    if x.get('ordem'): _fim_da_ordem(S, f)


# ---------- O ROBÔ: quem o jogador não comanda ----------
def escolhe(S, f):
    """A REGRA CURTA de quem o jogador não comanda (gente, povo ou bicho que lança, bebe ou solta um encanto). Devolve a ação, ou None (luta como sempre).
    A peça encantada, quando vale; a poção de cura abaixo de metade do PV; cura quem está abaixo de metade; protege, benze e guarda; prende quem ainda vem chegando;
    a área só onde há dois inimigos ou mais e nenhum amigo; o resto, o maior dano que a Mana paga. Quem só fere de longe e não tem o que lançar espera a Mana voltar.
    O bicho que lança, lança enquanto não alcança o inimigo neste turno; ao alcance, usa o corpo (o instinto)."""
    inim = L.inimigos(S, f); restam = f.get('_restam', 0)
    if not inim or restam <= 0: return None
    perto = min(inim, key=lambda e: L.dist(f, e)); d = L.dist(f, perto)
    for i, e in enumerate(f.get('encantos') or []):                     # a peça encantada (uma vez por luta)
        if e['carregado'] and not e['dorme'] and TM.ACOES[T.FEITICOS[e['feitico']]['grau']] <= restam:
            r = _encanto_robo(S, f, e['feitico'], perto, d, i)
            if r: return r
    r = _bebe_robo(S, f)
    if r: return r
    sabe = f.get('feiticos') or []
    if not sabe: return None
    if f.get('bicho') and d <= L._passo(S, f) * T.ACOES and not L._nao_anda(S, f): return None      # o bicho que lança, lança enquanto não alcança; ao alcance, usa o corpo
    mana = f.get('mana', 0); pode = lambda k: k in sabe and TM.FEITICOS[k]['tipo'] != 'rito' and mana >= custo(f, k) and TM.ACOES[T.FEITICOS[k]['grau']] <= restam
    for k in ORDEM_ROBO:
        if k == '*dano':
            al = [e for e in inim if L.dist(f, e) <= 8]
            if not al: continue
            e = min(al, key=lambda e: e['pv'] / e['pvmax'])
            for n in DANO_ROBO:
                if not pode(n) or L.dist(f, e) > TM.FEITICOS[n]['alc'] or (n == 'raio' and d <= 1) or (n == 'castigo' and not maldito(S, e)): continue
                return ('lanca', n, e['nome'], None, {})
            continue
        if pode(k):
            r = _alvo_robo(S, f, k, inim, perto, d)
            if r: return r
    if any(k in sabe for k in DANO_LONGE) and d > 1 and (any(L.dist(f, e) <= 8 for e in inim) or mana < 2): return ('espera',)       # sem o que lançar: espera a Mana voltar
    return None


def _encanto_robo(S, f, k, perto, d, i):
    """quando a peça encantada vale a pena: prender quem vem chegando sem arma de tiro; ferir de 2 casas para lá; o escudo de perto; a área na casa do mais perto"""
    sp = TM.FEITICOS[k]; t = sp['tipo']; x = dict(fonte=i)
    if t == 'poe' and sp['poe'] == 'preso' and 2 <= d <= sp['alc'] and not L.arma_de(S, perto)['distancia']: return ('lanca', k, perto['nome'], None, x)
    if t in ('dano', 'poe', 'medo') and not (t == 'poe' and sp['poe'] == 'preso') and 2 <= d <= sp['alc']: return ('lanca', k, perto['nome'], None, x)
    if t == 'area' and 2 <= d <= sp['alc']: return ('lanca', k, None, perto['x'], x)
    if t == 'escudo' and d <= 3 and not ve(f, 'guardado'): return ('lanca', k, f['nome'], None, x)
    if t in ('bencao', 'seiva') and d <= 2 and not ve(f, 'benzido' if t == 'bencao' else 'seiva'): return ('lanca', k, f['nome'], None, x)
    if t == 'cura' and f['pv'] < f['pvmax'] * TM.ROBO['cura']: return ('lanca', k, f['nome'], None, x)
    if t == 'guarda' and any(e.get('feiticos') for e in L.inimigos(S, f)): return ('lanca', k, None, None, x)
    if t == 'campo' and sp.get('tira') in S['tempo'] and not tem(f, 'noturno'): return ('lanca', k, None, None, x)
    return None


def _bebe_robo(S, f):
    """a poção de quem o jogador não comanda: a cura abaixo de metade do PV; a Mana quando não paga nem o mais barato; o antídoto quando o veneno pesa;
    a guarda contra quem lança; a fúria no corpo a corpo. Nunca além do que o corpo aguenta no dia."""
    if f.get('doses', 0) >= T.doses_dia((f.get('atributos') or {}).get('Vigor', 50)): return None
    if not f.get('carga') and not f.get('elixires'): return None
    if f['pv'] < f['pvmax'] * TM.ROBO['bebe'] and f.get('curado', 0) < int(f['pvmax'] * T.CURA_TETO):
        ps = pocoes(f, 'cura')
        if ps: return ('bebe', ps[0][1], None, {})
    if f.get('feiticos') and f.get('mana_max') and f.get('mana', 0) < min(custo(f, k) for k in f['feiticos']):
        ps = pocoes(f, 'mana')
        if ps: return ('bebe', ps[0][1], None, {})
    if f.get('veneno') and f['veneno'][0] * f['veneno'][1] >= f['pvmax'] * TM.ROBO['antidoto']:
        ps = [p for p in pocoes(f, 'antídoto') if p[0] >= f.get('veneno_cat', 0)]
        if ps: return ('bebe', ps[0][1], None, {})
    g, _ = guarda(S, f)
    if any(e.get('feiticos') for e in L.inimigos(S, f)) and not ve(f, 'guarda_p'):
        ps = [p for p in pocoes(f, 'guarda') if T.MULT[p[0]] > g]
        if ps: return ('bebe', ps[0][1], None, {})
    if not ve(f, 'furia') and any(L.dist(f, e) <= 1 for e in L.inimigos(S, f)):
        ps = [p for p in pocoes(f, 'fúria') if p[0] >= L.arma_de(S, f)['cat']]
        if ps: return ('bebe', ps[0][1], None, {})
    return None


def _alvo_robo(S, f, k, inim, perto, d):
    """o alvo da regra curta para o feitiço k, ou None (não vale lançar k agora)"""
    sp = TM.FEITICOS[k]; t = sp['tipo']; meus = L.de_pe(S, f['lado']); cal = TM.ROBO['calejo']; ao = lambda e: L.dist(f, e) <= max(sp['alc'], 1)
    if t == 'cura':
        al = [x for x in meus if ao(x) and x['pv'] < x['pvmax'] * TM.ROBO['cura'] and x.get('curado', 0) < int(x['pvmax'] * T.CURA_TETO)]
        return ('lanca', k, min(al, key=lambda x: x['pv'] / x['pvmax'])['nome'], None, {}) if al else None
    if t == 'amparo':
        al = [x for x in S['L'] if x['lado'] == f['lado'] and x['estado'] == 'caido' and ao(x) and max(x['morte']) < 3]
        al += [x for x in meus if ao(x) and ((x.get('sangra') and x['sangra'][0] * x['sangra'][1] >= x['pvmax'] * TM.ROBO['antidoto']) or (x.get('veneno') and x['veneno'][0] * x['veneno'][1] >= x['pvmax'] * TM.ROBO['antidoto']))]
        return ('lanca', k, al[0]['nome'], None, {}) if al else None
    if t == 'escudo':
        if not ve(f, 'guardado') and d <= 2: return ('lanca', k, f['nome'], None, {})
        al = [x for x in meus if x is not f and ao(x) and not ve(x, 'guardado') and any(L.dist(x, e) <= 1 for e in inim)]
        return ('lanca', k, max(al, key=lambda x: sum(1 for e in inim if L.dist(x, e) <= 1))['nome'], None, {}) if al else None
    if t == 'guarda':
        c = foco(S, f, trad_de(f, k))[0]; casa = [x for x in meus if x['x'] == f['x']]
        if any(e.get('feiticos') for e in inim) and sum(1 for x in casa if guarda(S, x)[0] < T.MULT[c] and not ve(x, 'guarda')) >= 2: return ('lanca', k, None, None, {})
        return None
    if t == 'bencao':                                       # benze quem já está no corpo a corpo, mas só enquanto ninguém está colado em quem lança (lançar colado dá o golpe livre)
        if d <= 1: return None
        al = [x for x in meus if x is not f and ao(x) and not ve(x, 'benzido') and not x.get('feiticos') and any(L.dist(x, e) <= 1 for e in inim)]
        return ('lanca', k, al[0]['nome'], None, {}) if al else None
    if t == 'poe':
        q = sp['poe']; c = [e for e in inim if ao(e) and not ve(e, q) and e.get('calejo', 0) < cal]
        if q == 'no': c = [e for e in c if e.get('feiticos')]
        if q == 'preso': c = [e for e in c if L.dist(f, e) >= 2 and not L.arma_de(S, e)['distancia'] and not e['preso'] and not any(L.dist(o, e) <= max(1, L.arma_de(S, e)['alcance']) for o in meus)]
        return ('lanca', k, min(c, key=lambda e: L.dist(f, e))['nome'], None, {}) if c else None
    if t == 'medo':
        c = [e for e in inim if ao(e) and e.get('moral') != 'firme' and e.get('calejo', 0) < cal and not e.get('controla') and (e.get('bicho') or not sp.get('so_bicho'))]
        return ('lanca', k, min(c, key=lambda e: L.dist(f, e))['nome'], None, {}) if c else None
    if t == 'area':
        casas = {}
        for e in inim:
            if abs(e['x'] - f['x']) <= sp['alc'] and e['x'] != f['x']: casas.setdefault(e['x'], []).append(e)
        boas = [v for x, v in casas.items() if len(v) >= 2 and not any(o['x'] == x for o in meus)]
        return ('lanca', k, None, max(boas, key=len)[0]['x'], {}) if boas else None
    if t == 'seiva':
        al = [x for x in meus if ao(x) and x['pv'] < x['pvmax'] * TM.ROBO['seiva'] and not ve(x, 'seiva')]
        return ('lanca', k, min(al, key=lambda x: x['pv'] / x['pvmax'])['nome'], None, {}) if al else None
    if t == 'campo':
        if sp.get('tira') and sp['tira'] in S['tempo'] and k not in (S.get('campo') or {}) and not all(tem(x, 'noturno') for x in meus): return ('lanca', k, None, None, {})
        return None
    if t == 'chamar':
        return ('lanca', k, None, None, {}) if S.get('ermo') and len(meus) < len(inim) and d > 1 else None
    return None


# ---------- a ordem (luta.ordem chama): conferida inteira antes de qualquer dado ----------
PALAVRAS = ('em', 'casa')
FLAGS = ('sempre', 'osso', 'neblina', 'lama', 'dominio')


def _acha_feitico(f, pal):
    alvo = None
    for k in T.FEITICOS:
        if _sem_acento(k) == _sem_acento('-'.join(pal)): alvo = k
    return alvo


def ordem(S, f, acao, pal):
    """a ordem de magia de quem o jogador comanda, conferida: o feitiço que ele sabe (e que se lança na luta), o alvo de pé, a casa ao alcance; a poção que leva; o encanto carregado"""
    antes = S['ordens'].get(f['nome']); antes = antes.get('antes') if antes and antes.get('acao') in ('lancar', 'beber', 'usar') else antes
    o = dict(acao=acao, antes=antes); fl = []
    while pal and pal[-1] in FLAGS: fl.append(pal.pop())
    corte = next((i for i, x in enumerate(pal) if x in PALAVRAS), len(pal)); cab, resto = pal[:corte], pal[corte:]
    if resto:
        if resto[0] == 'casa':
            if len(resto) != 2 or not resto[1].lstrip('-').isdigit(): sys.exit(f'"casa" pede o número da casa (veio "{" ".join(resto)}")')
            o['casa'] = int(resto[1])
        else:
            nm = ' '.join(resto[1:]); e = next((x for x in S['L'] if x['nome'].lower() == nm.lower() and x['estado'] in ('pe', 'caido')), None)
            if not nm or e is None: sys.exit(f'em quem? Na luta: {", ".join(x["nome"] for x in L.de_pe(S))}')
            o['alvo'] = e['nome']
    if acao == 'lancar':
        if not cab: sys.exit(f'lançar o quê? {f["nome"]} sabe: {", ".join(f.get("feiticos") or []) or "nenhum feitiço"}')
        k = _acha_feitico(f, cab)
        if k is None: sys.exit(f'feitiço desconhecido: "{" ".join(cab)}" (os que há: {", ".join(T.FEITICOS)})')
        if k not in (f.get('feiticos') or []): sys.exit(f'{f["nome"]} não sabe {nome(k)} (sabe: {", ".join(f.get("feiticos") or []) or "nenhum feitiço"})')
        _confere_feitico(S, f, k, o)
        if 'dominio' in fl and not dominio_pronto(S, f): sys.exit(f'{f["nome"]} não tem o Domínio pronto (o foco com ele, inteiro, uma vez por luta)')
        o.update(feitico=k, sempre='sempre' in fl, osso='osso' in fl, campo=next((x for x in fl if x in ('neblina', 'lama')), None), dominio='dominio' in fl)
    elif acao == 'beber':
        if len(cab) != 1: sys.exit(f'beber o quê? {f["nome"]} leva: {", ".join(_leva(f)) or "nenhuma poção"}')
        b = cab[0]; n = b.partition(':')[0]
        if n in TM.NAO_SE_BEBE: sys.exit(f'{TM.NAO_SE_BEBE[n]}')
        if not pocoes(f, n) or (':' in b and _pocao(f, b)[0] is None): sys.exit(f'{f["nome"]} não leva "{b}" (leva: {", ".join(_leva(f)) or "nenhuma poção"})')
        if o.get('alvo') and L.por_nome(S, o['alvo'])['lado'] != f['lado']: sys.exit('dar de beber, só a quem é do seu lado')
        o['bem'] = b
    else:
        es = [(i, e) for i, e in enumerate(f.get('encantos') or []) if e['carregado'] and not e['dorme']]
        if cab: es = [(i, e) for i, e in es if _sem_acento(' '.join(cab)) in _sem_acento(e['nome']) or _sem_acento(' '.join(cab)) in ('arma', 'escudo', 'armadura') and _sem_acento(' '.join(cab)) in _sem_acento(e['nome'] + ' ' + _tipo(S, e))]
        if not es: sys.exit(f'{f["nome"]} não tem encanto pronto' + (f' em "{" ".join(cab)}"' if cab else '') + ' (o encanto sai uma vez por luta; a peça que dorme não solta)')
        i, e = es[0]; _confere_feitico(S, f, e['feitico'], o); o['encanto'] = i
    return o


def _tipo(S, e): return S['itens'][e['item']].get('tipo', '') if isinstance(e['item'], str) else e['item'].get('tipo', '')


def _leva(f): return [b for b, q in (f.get('carga') or {}).items() if q > 0] + ['elixir:' + x['id'] for x in f.get('elixires') or []]


def _confere_feitico(S, f, k, o):
    t = TM.FEITICOS[k]['tipo']
    if t == 'rito': sys.exit(f'{nome(k)} é rito de 1 bloco: faz-se fora da luta')
    if t == 'chamar' and not S.get('ermo'): sys.exit(f'{nome(k)} só vale no ermo (a luta não está num ermo contado)')
    a = L.por_nome(S, o['alvo']) if o.get('alvo') else None
    if a is not None:
        if t in HOSTIS and a['lado'] == f['lado']: sys.exit(f'{nome(k)} vai num inimigo ({a["nome"]} é do seu lado)')
        if t in ('escudo', 'bencao', 'cura', 'amparo', 'seiva') and a['lado'] != f['lado']: sys.exit(f'{nome(k)} vai em quem é do seu lado')
        if a['estado'] == 'caido' and t not in ('cura', 'amparo'): sys.exit(f'{a["nome"]} caiu: só a cura e o amparo vão em quem caiu')
    if o.get('casa') is not None and t != 'area': sys.exit(f'{nome(k)} não vai numa casa: diga em quem (em NOME)')


# ---------- o que vai ao quadro ----------
def linha(S, f):
    """o que a magia põe na linha do lutador no quadro: a Mana, o que canaliza, os estados com prazo"""
    L_ = []; s = f.get('est') or {}
    if f.get('feiticos') and f.get('mana_max') and f['estado'] in ('pe', 'caido'): L_.append(f"Mana {mana_diz(f)}")
    if f['estado'] == 'pe':
        c = f.get('canaliza')
        if c: L_.append(f"CANALIZANDO {nome(c['nome'])}" + (f" em {c['alvo']}" if c.get('alvo') else ''))
        for k, txt in (('preso', 'preso pelo feitiço'), ('cego', 'cego'), ('guardado', 'com o escudo'), ('no', 'com a Mana atada')):
            if s.get(k): L_.append(f"{txt} ({s[k]} turno{_s(s[k])})")
        if s.get('guarda'): L_.append(f"guardado como por amuleto {T.CATS[s['guarda'][0]]} ({s['guarda'][1]} turno{_s(s['guarda'][1])})")
        if s.get('guarda_p') is not None: L_.append(f"com a poção de guarda {T.CATS[s['guarda_p']]}")
        if s.get('benzido'): L_.append('benzido' + (f" ({s['benzido']} rodada{_s(s['benzido'])})" if s['benzido'] < TM.PRAZO_SEM_FIM else ''))
        if s.get('olhado'): L_.append('com mau-olhado')
        if s.get('seiva'): L_.append(f"com seiva ({s['seiva']} rodada{_s(s['seiva'])})")
        if s.get('furia'): L_.append(f"com fúria ({s['furia'][0]} rodada{_s(s['furia'][0])})")
        if s.get('enjoo'): L_.append('enjoado')
    return ''.join(' · ' + x for x in L_)


def campo(S):
    """a linha do campo no quadro: o que os feitiços puseram ou tiraram"""
    cp = S.get('campo') or {}
    if not cp: return ''
    return 'CAMPO: ' + ' · '.join((f"a luz de {v['quem']}" if v.get('tira') else f"a {v['poe']} de {v['quem']}") + ' (1 de Mana por rodada)' for v in cp.values())


def cura_ao_alcance(S, e):
    """a parada de quem caiu do lado da casa ganha a frase quando há cura ou poção ao alcance"""
    if e['lado'] != 'A': return ''
    for o in L.de_pe(S, 'A'):
        if L.dist(o, e) > 1: continue
        if 'cura' in (o.get('feiticos') or []) and o.get('mana', 0) >= custo(o, 'cura'): return f" (há cura ao alcance: {o['nome']} sabe curar)"
        if pocoes(o, 'cura'): return f" (há cura ao alcance: {o['nome']} leva poção de cura)"
    return ''
