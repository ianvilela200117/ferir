#!/usr/bin/env python3
"""habilidade.py — MOTOR 10, A PARTE 2, FASE 2: AS HABILIDADES (o contrato: projeto/etapa_efeitos/DESENHO.md, seção 6; o capítulo 29; os números no tabelas_habilidades.py).

O luta.py chama daqui o que a habilidade pede, e SÓ numa luta em que alguém traz habilidade (S['hab']): a luta sem habilidade é a de sempre, dado por dado (como a magia).
  A PILHA DA CENA (6.3): a RODA DO MALHO conta batidas (cada golpe dela, acerte ou não; o golpe que fere quem dança tira 1; dois 1, ou outra ação que não golpear ou tomar
  fôlego, zera), com o FECHO (fundo ou tranco), o ABRIR e as figuras; a SANHA acende sem ação no primeiro sangue ao alcance e soma no turno e no golpe que tira PV; os TRUNFOS
  vão ao dano ou ao efeito, um por turno, por uma ordem com condição que o script resolve (nunca uma parada por golpe). As DECLARADAS (o Tranco, o Corte Fundo, a Rasteira) fazem
  do primeiro golpe do turno o da técnica; o TRANCO tira o turno seguinte dentro da regra de 1 turno em 3 (3.5). As REAÇÕES (a Riposta, o Manter à Distância, a Vigília) saem
  sozinhas quando cabem (`sem riposta` as desliga). A pilha: o dano a mais vai ao grupo TÉCNICA (até +40%); o acerto, a Defesa e a coragem ao teto de +8 (P3); o fecho fundo
  multiplica os dados da arma (o maior entre ele, o crítico e o Golpe do Fim, nunca mais de 4); o dado somado (o trunfo, o Rito de Veia) entra uma vez e não dobra no crítico.
  O GRAU PELO USO (6.2): uma marca por cena (dureza + 1 se usou 3 vezes ou se a de luta venceu, − o desconto), com os sete freios; a subida aparece na saída do ato.
  AS ORIGENS (6.5): o mestre, a lição, o estalo, o livro, o legado (a classe chega na fase 4); copiar, com três tentativas.

Uso (o personagem do jogador, ou quem=ID):
  python3 habilidade.py ver [CHAVE]              o catálogo (52), ou uma habilidade grau a grau
  python3 habilidade.py mao                      a linha 🛠️ do turno (as suas habilidades: grau, marcas, a de luta, a pilha da cena)
  python3 habilidade.py esquece CHAVE            esquece uma habilidade (a vaga volta; as marcas dela se perdem)
  python3 habilidade.py sobe                     confere a subida de grau (o fim do ato já confere sozinho)
  python3 habilidade.py ensina PID CHAVE [blocos=N]   o mestre (PID), no mesmo lugar, ensina: uma jornada de treino juntos (2 blocos; 10, 20 ou 40 ao todo, pelo teto dela),
                                                 com a estima e o grau dele conferidos; no último bloco, ela nasce
  python3 habilidade.py estuda ITEM              estuda o escrito com a técnica (os blocos do livro), ou o caderno de um legado (30 blocos)
  python3 habilidade.py copia CHAVE de=PID chance    a chance de colher o jeito e as tentativas que restam, SEM ROLAR (mostre à mesa antes)
  python3 habilidade.py copia CHAVE de=PID       uma tentativa de colher o jeito (um dia de treino; a chance vai na linha de cima; rolagem de verdade, uma vez)
  python3 habilidade.py licao CHAVE "como"       SÓ O MESTRE: o gatilho escrito da lição aconteceu (nasce no Iniciante, se há vaga)
  python3 habilidade.py ferro PACIENTE           o Ferro em Brasa fora da luta (1 bloco, juntos): a ferida leve sara com 1 dia de repouso (no Grão-Mestre, a grave com 3); dói
  python3 habilidade.py paciencia | tempera      acende a de dia de trabalho (a Paciência; a Têmpera Certa, numa obra de hoje)
  Na luta (luta.py roda / ato.py luta roda): "Nome: fazer roda [em ALVO] [fecho=fundo|tranco] [sempre] [postura]" · "Nome: fazer fecho" · "Nome: fazer sanha" ·
    "Nome: fazer tranco|corte|rasteira [em ALVO] [sempre]" · "Nome: fazer brado|rito|mira|varrida [sempre]" · "Nome: fazer ferro [ALIADO] [sempre]" · "Nome: fazer sopro ALIADO" ·
    "Nome: fazer voto [sempre]" (o Golpe de Voto de quem o jogador comanda só gasta a Mana com a ordem) · "Nome: sem voto" · "Nome: atar CAÍDO" (a Mão que Estanca do Mestre) ·
    "Nome: trunfo=tranco se carga>=6, senão dano" · "Nome: sem riposta" · a postura "bigorna"
"""
import math, re, sys
if __name__ == '__main__': sys.modules.setdefault('habilidade', sys.modules[__name__])
import tabelas as T
import tabelas_habilidades as H
import tabelas_efeitos as TE
import tabelas_talento as TT
import luta as L

NOMES = {k: h['nome'] for k, h in H.HABILIDADES.items()}
RITMO_DIZ = dict(mao='de mão', luta='de luta', dia='de dia', cena='de cena', reacao='reação', acesa='acesa', declarada='declarada', cargas='de cargas')
def nome(k): return NOMES.get(k, k)
def Nome(k): n = nome(k); return n[:1].upper() + n[1:]


def _contrai(prep, k):
    """'de', 'em' ou 'por' com o artigo do nome: do Tranco, na Sanha, nos Trunfos, pelo Corte Fundo"""
    n = nome(k); art, _, resto = n.partition(' ')
    return f"{dict(de='d', em='n', por='pel')[prep]}{art} {resto}" if art in ('o', 'a', 'os', 'as') and resto else f"{prep} {n}"


def de(k): return _contrai('de', k)


def em(k): return _contrai('em', k)
def grau_diz(g): return H.GRAUS[max(0, min(H.GM, g))]
def _conta(S, k, v=1): c = S.setdefault('conta', {}); c[k] = c.get(k, 0) + v


# ---------- quem tem o quê ----------
def grau_de(reg):
    """o grau de um registro de habilidade (o do estado: {grau, marcas, ...}; o da prova: o número)"""
    if isinstance(reg, bool): return 0
    if isinstance(reg, int): return max(0, min(H.GM, reg))
    return max(0, min(H.GM, int((reg or {}).get('grau', 0) or 0))) if isinstance(reg, dict) else 0


def habs(p):
    """{chave: grau} das habilidades da pessoa (do estado ou da prova): o que a ficha de luta leva"""
    hb = p.get('habilidades') or {}
    return {k: grau_de(v) for k, v in hb.items() if k in H.HABILIDADES} if isinstance(hb, dict) else {}


def tem(f, k): return k in (f.get('hab') or {})
def g(f, k): return (f.get('hab') or {}).get(k, -1)
def n(f, k, campo): return H.num(k, campo, g(f, k))


def _usa(f, k, v=1):
    u = f.setdefault('hab_usos', {}); u[k] = u.get(k, 0) + v


def _fam(w): return ((w or {}).get('item') or {}).get('familia') if isinstance((w or {}).get('item'), dict) else (w or {}).get('familia')


def _familia(S, w):
    """a família da arma em uso (o S['itens'] guarda a peça)"""
    it = S['itens'].get(w['item']) if isinstance(w.get('item'), str) else w.get('item')
    return (it or {}).get('familia') or ('punho' if 'mãos' in w.get('nome', '') else None)


def arma_ok(S, f, k, w=None):
    """a arma em uso serve a esta habilidade? (a Roda pede arma de peso, ou a peça do legado dela; a Riposta, quem apara: a espada, o montante ou o escudo)"""
    w = w or L.arma_de(S, f); arms = H.HABILIDADES[k].get('armas')
    if k == 'riposta':
        gb, gp = L.guarda_de(S, f); return gb > 0 and (gp is f.get('escudo') or _familia(S, w) in H.APARA)
    if arms is None: return True
    fam = _familia(S, w)
    if fam in arms: return True
    if k == 'roda':
        it = S['itens'].get(w['item']) if isinstance(w.get('item'), str) else w.get('item')
        return bool(((it or {}).get('legado') or {}).get('tecnica') == 'roda')
    return False


# ---------- a luta: prepara, o começo do turno, o robô ----------
def tem_hab(S): return any(f.get('hab') for f in S['L'])


def prepara(S, f):
    """os campos da luta de habilidade em cada lutador (DESENHO 9.4: hab, acesa, batidas, sanha, corrente, trunfos [restam, lados], trunfo_ordem, usos, de_luta, sem_riposta)"""
    hb = dict(f.get('hab') or {}); f['hab'] = hb; tr = None
    if 'trunfos' in hb:
        q, lados = H.num('trunfos', 'dados', hb['trunfos']); tr = [max(0, q - int(f.get('trunfos_gastos') or 0)), lados]
    f.update(acesa=None, batidas=0, sanha=0, sanha_max=0, sanha_arma=False, sanha_vezes=0, corrente=0, trunfos=tr, trunfo_ordem=f.get('trunfo_ordem'), trunfo_t=-1,
             usos={}, de_luta=[], sem_riposta=bool(f.get('sem_riposta')), hab_usos=dict(f.get('hab_usos') or {}), decl=None, decl_ok=False, roda_entrou=False, fecho_tipo='fundo',
             fecho_ja=False, abrir_t=-1, abrir_de=None, sangue_r=-1, estanca=[0, -1], rito=None, mira=0, mira_t=-1, varrida=None, mana_curta=False, rito_cedo=0, cansa_mais=0,
             hab_dia=list(f.get('hab_dia') or []), voto_r=-1, voto_ordem=None, levantou=False, recuos=0, vigiou_r=-1, caiu_r=None, hab_feitas=[])
    # hab_dia: as de dia (o Sopro de Volta) já gastas HOJE, numa luta de antes (o estado.lutador as traz pelo `usada`): de dia é uma por dia, não uma por luta
    # roda_entrou: a entrada quente do Mestre e do Grão-Mestre é a da primeira batida DA LUTA (uma vez; acender a Roda de novo não a repõe)
    # voto_ordem: o Golpe de Voto de quem o jogador comanda só gasta a Mana com a ordem (`fazer voto [sempre]`); o robô o usa sozinho


def traz_cabeca(S):
    """a luta em que alguém traz carga de cabeça por habilidade (o Tranco, o fecho tranco da Roda do Adepto, o trunfo de tranco do Perito): só nela a ferida grave na cabeça
    conta como turno perdido e dá a cabeça firme (3.5)"""
    return any(('tranco' in (f.get('hab') or {})) or (f.get('hab') or {}).get('roda', -1) >= 2 or (f.get('hab') or {}).get('trunfos', -1) >= 3 for f in S['L'])


def comeco(S, f):
    """o começo do turno: a Sanha soma 1; o Rito conta os turnos; a declarada fica pronta para o primeiro golpe; o robô escolhe o que acende e o que declara"""
    if not f.get('hab') or f['estado'] != 'pe': return
    f['decl_ok'] = True
    if f.get('corrente') and f.get('perde_turno'): f['corrente'] = 0          # ser atordoado zera a Corrente
    if f['acesa'] == 'sanha': _sanha_mais(S, f, 1)
    if f['acesa'] == 'rito_veia' and f['rito'] and f['turnos_n'] > f['rito'][1]: _apaga(S, f, 'o Rito de Veia acabou')
    if not f.get('controla'): _robo(S, f)


def _forte(S, f, al):
    """o mais forte entre os inimigos ao alcance (o tranco do robô vai nele)"""
    return max(al, key=lambda e: (e.get('nivel', 0), e['pvmax'], e['nome'])) if al else None


def _robo(S, f):
    """A REGRA CURTA de quem o jogador não comanda (6.4): a Roda sempre que a arma deixa, com o fecho aos 4; a Sanha quando colado e acima de metade do PV; o tranco no mais forte;
    o Corte Fundo e a Rasteira no primeiro golpe de cada turno; o trunfo no dano (na ameaça contra quem fraquejou); a riposta sempre"""
    hb = f['hab']; w = L.arma_de(S, f); inim = L.inimigos(S, f)
    rito_vale = f['acesa'] == 'rito_veia' and bool(f.get('rito')) and f['turnos_n'] <= f['rito'][1]
    if 'roda' in hb and arma_ok(S, f, 'roda', w):
        if f['acesa'] != 'roda' and not rito_vale: acende(S, f, 'roda')      # o Rito aceso segue até acabar (a Roda volta depois)
    elif 'sanha' in hb and f['acesa'] is None and not f['sanha_arma'] and f['sanha_vezes'] < n(f, 'sanha', 'usos') and f['pv'] > f['pvmax'] * 0.5 and any(L.dist(f, e) <= 1 for e in inim):
        f['sanha_arma'] = True
    al = [x[0] for x in L.alvos(S, f, w, cerco=False)]
    if 'tranco' in hb and arma_ok(S, f, 'tranco', w) and f['usos'].get('tranco', 0) < n(f, 'tranco', 'usos'):
        fo = _forte(S, f, inim)
        if fo is not None: f['decl'] = dict(k='tranco', alvo=fo['nome'], sempre=True)
    elif 'corte_fundo' in hb and arma_ok(S, f, 'corte_fundo', w): f['decl'] = dict(k='corte_fundo', alvo=None, sempre=True)
    elif 'rasteira' in hb and arma_ok(S, f, 'rasteira', w): f['decl'] = dict(k='rasteira', alvo=None, sempre=True)
    elif f.get('decl') and not f.get('controla'): f['decl'] = None
    if 'varrida' in hb and f['varrida'] is None: f['varrida'] = 'sempre'


def postura(S, f, o):
    """a postura nova (a Guarda de Bigorna): quem o jogador comanda a diz no fim da ordem; o robô que a tem fica nela. Na Sanha não se guarda: com ela acesa, a postura
    defensiva e a bigorna voltam a firme (a ordem que as pede é recusada antes do dado; esta é a rede, para a postura que já estava)"""
    if f.get('acesa') == 'sanha' and f['postura'] in ('defensiva', 'bigorna'): f['postura'] = 'firme'; return
    if 'bigorna' in (f.get('hab') or {}) and not f.get('controla') and f['postura'] == 'firme' and f.get('acesa') != 'sanha': f['postura'] = 'bigorna'


# ---------- acender e apagar (uma acesa por vez) ----------
def acende(S, f, k):
    """acende k (a Roda, a Sanha, o Rito de Veia): acender outra apaga a primeira (6.1). Acender a que já está acesa não muda a pilha (a ordem `fazer roda fecho=tranco`
    com a Roda acesa só troca o fecho: as batidas ficam, e a entrada quente é uma por luta)"""
    if f['acesa'] == k: return
    if f['acesa']: _apaga(S, f, f"{Nome(k)} apaga {nome(f['acesa'])}")
    f['acesa'] = k; _conta(S, 'acende_' + k)
    if k == 'sanha':
        f['sanha'] = 1; f['sanha_max'] = max(f['sanha_max'], 1); f['sanha_arma'] = False; f['sanha_vezes'] += 1; f['sangue_r'] = S['r']; _usa(f, 'sanha')
        if f['postura'] in ('defensiva', 'bigorna'): f['postura'] = 'firme'
        L.diz(S, f"    {f['nome']} entra na SANHA")
        if f['lado'] == 'B': _para_lado_a(S, f"{f['nome']} acendeu a Sanha")
    if k == 'roda': f['batidas'] = 0


def _apaga(S, f, porque=''):
    k = f.get('acesa')
    if not k: return
    if k == 'sanha':
        f['cansa_mais'] += f['sanha_max'] // H.SANHA_CANSA_A_CADA; f['sanha_max'] = 0; f['sanha'] = 0
        if f.get('controla'): L._para(S, f, f"a Sanha de {f['nome']} apagou" + (f" ({porque})" if porque else ''))
        L.diz(S, f"    a Sanha de {f['nome']} apaga" + (f" ({porque})" if porque else ''))
    if k == 'roda': f['batidas'] = 0
    if k == 'rito_veia': f['rito'] = None
    f['acesa'] = None


def _para_lado_a(S, txt):
    if txt not in S['paradas']: S['paradas'].append(txt)
    S['houve_parada'] = True


def _sanha_mais(S, f, q):
    if f.get('acesa') != 'sanha': return
    f['sanha'] = min(n(f, 'sanha', 'pontos'), f['sanha'] + q); f['sanha_max'] = max(f['sanha_max'], f['sanha'])


def _sanha_acende(S, a, e):
    """a Sanha armada acende sem ação no primeiro golpe que tira PV de alguém ao alcance de quem a chamou (o golpe dele, o que ele leva, o de um colado)"""
    for h in L.de_pe(S):
        if h.get('sanha_arma') and h.get('acesa') != 'sanha' and (h is a or h is e or L.dist(h, e) <= max(1, L.arma_de(S, h)['alcance'])): acende(S, h, 'sanha')


# ---------- O GOLPE ----------
def golpe_antes(S, a, e, w, livre, extra):
    """o que as habilidades põem neste golpe antes do dado: {mais (o acerto que entra no teto de +8), pena (o acerto a menos), roda, fecho, fundo, decl, ...}"""
    hg = dict(mais=0, pena=0, roda=False, fecho=None, fundo=0, decl=None, livre=livre, extra=extra, trunfo=None, voto=0)
    ha = a.get('hab') or {}; he = e.get('hab') or {}
    a['_hg'] = hg
    if not ha and not he: return hg
    if a.get('postura') == 'bigorna' and 'bigorna' in ha: hg['pena'] += n(a, 'bigorna', 'acerto')
    if e.get('postura') == 'bigorna' and 'bigorna' in he and not w.get('area'): _usa(e, 'bigorna')      # a Guarda de Bigorna é usada a cada golpe em que a Defesa dela conta (a marca e o grau)
    if a.get('acesa') == 'sanha': hg['mais'] += a['sanha'] // H.SANHA_ACERTO_A_CADA
    if 'teima' in ha and a['pv'] < a['pvmax'] * 0.5: hg['mais'] += n(a, 'teima', 'acerto'); _usa(a, 'teima')
    if livre:
        if livre == 'a riposta' and 'riposta' in ha: hg['pena'] += n(a, 'riposta', 'acerto')
        if livre == 'o alcance bate primeiro' and 'manter' in ha and arma_ok(S, a, 'manter', w): hg['mais'] += n(a, 'manter', 'acerto'); hg['manter'] = True; _usa(a, 'manter')
        if livre == 'no recuo' and he.get('pe_lebre', -1) >= 0: hg['pena'] += n(e, 'pe_lebre', 'livre')
        return hg
    if extra: return hg
    if a.get('acesa') == 'roda' and arma_ok(S, a, 'roda', w):
        gr = ha['roda']; teto = H.num('roda', 'batidas', gr)
        if not a['roda_entrou']: a['roda_entrou'] = True; a['batidas'] = max(a['batidas'], H.RODA_ENTRA[gr])
        hg['roda'] = True; hg['mais'] += a['batidas'] // H.RODA_ACERTO_A_CADA; _usa(a, 'roda')
        if gr >= 2 and a['batidas'] >= H.RODA_FECHO_DESDE and (a['fecho_ja'] or a['batidas'] >= min(H.RODA_FECHO_SOZINHO, teto)):
            hg['fecho'] = a['fecho_tipo'] if a['fecho_tipo'] in ('fundo', 'tranco') else 'fundo'
            if hg['fecho'] == 'fundo': hg['fundo'] = 1 + a['batidas'] // H.RODA_FECHO_FUNDO
    if a.get('mira') and w['distancia']: hg['mais'] += a['mira']; a['mira'] = 0; _usa(a, 'mira_firme')
    d = a.get('decl')
    if d and a.get('decl_ok') and d['k'] in ha and arma_ok(S, a, d['k'], w) and (not d.get('alvo') or d['alvo'] == e['nome']):
        k = d['k']; ok = True
        if k == 'tranco':
            ok = a['usos'].get('tranco', 0) < n(a, 'tranco', 'usos') and e['firme_cabeca'] <= 0 and not e['perde_turno'] and L._pode_perder(e)
            if ok: a['usos']['tranco'] = a['usos'].get('tranco', 0) + 1
        if ok:
            a['decl_ok'] = False; hg['decl'] = k; hg['pena'] += n(a, k, 'acerto'); _usa(a, k)
            if not d.get('sempre'): a['decl'] = None
    return hg


def acerto_mais(S, a):
    """o acerto a mais das habilidades neste golpe (entra no teto de +8 com a Certeira e a Desforra: P3)"""
    hg = a.get('_hg') or {}; return hg.get('mais', 0)


def acerto_pena(S, a):
    hg = a.get('_hg') or {}; return hg.get('pena', 0)


def defesa_mais(S, e):
    """a Defesa a mais (a Guarda de Bigorna), no teto de +8 com a Guarda do escudo"""
    return n(e, 'bigorna', 'defesa') if e.get('postura') == 'bigorna' and 'bigorna' in (e.get('hab') or {}) else 0


def defesa_pena(S, a, e):
    """o que a habilidade tira da Defesa de quem apanha: o preço da Sanha (−1)"""
    return H.SANHA_DEFESA if e.get('acesa') == 'sanha' else 0


def abrir(S, a, e):
    """o ABRIR da Roda (Perito): a primeira batida que acerta em cada turno tira 2 da Defesa do alvo até o fim do turno de quem dança (vale a pior com o aberto: P3)"""
    ab = e.get('abrir_de'); return H.RODA_ABRIR if ab and ab[0] == a['nome'] and ab[1] == S['r'] else 0


def coragem(S, f): return H.SANHA_CORAGEM if f.get('acesa') == 'sanha' else 0


def firme(S, e):
    """a Guarda de Bigorna do Adepto para cima deixa firme (a perna ferida não derruba)"""
    return e.get('postura') == 'bigorna' and (e.get('hab') or {}).get('bigorna', -1) >= 2


def quebra(S, a, w, pc, vestida):
    """o GOLPE DE QUEBRA: contra armadura de categoria maior que a arma, a proteção conta menos (o fator; vale o maior com a Perfura: P5), ou None"""
    if 'golpe_quebra' in (a.get('hab') or {}) and vestida and pc and pc['cat'] > w['cat'] and arma_ok(S, a, 'golpe_quebra', w):
        _usa(a, 'golpe_quebra'); return n(a, 'golpe_quebra', 'prot')
    return None


def dados_vezes(S, a, hg):
    """o fecho fundo: os dados da arma rolam 1 + batidas ÷ 2 vezes (o maior com o crítico e o Golpe do Fim; nunca mais de 4: P2)"""
    return min(TE.DADOS_MAX, hg.get('fundo') or 0) if hg else 0


def _cond(S, a, e, se):
    """a condição do trunfo: carga>=N, pernas>=N, abalado, metade"""
    if not se: return True
    k, v = se
    if k == 'carga': return e['barra']['cabeca'] >= v
    if k == 'pernas': return e['barra']['pernas'] >= v
    if k == 'abalado': return bool(e['abalado'] or e.get('acuado'))
    if k == 'metade': return e['pv'] < e['pvmax'] * 0.5
    return False


def _trunfo_uso(S, a, e):
    """o uso do trunfo neste golpe que acertou (a ordem com condição, um por turno), ou None"""
    tr = a.get('trunfos')
    if not tr or tr[0] <= 0 or a.get('trunfo_t') == a['turnos_n']: return None
    o = a.get('trunfo_ordem'); gt = g(a, 'trunfos')
    if o is None:
        if not a.get('controla') and gt >= H.TRUNFO_DESDE['ameaca'] and (e['abalado'] or e.get('acuado')) and e.get('moral') != 'firme': return 'ameaca'
        return 'dano'
    if o.get('uso') == 'nao': return None
    if _cond(S, a, e, o.get('se')): return o['uso']
    return o.get('senao')


def dado_extra(S, a, e, w, j, hg):
    """O DADO SOMADO (P2): o trunfo no dano e o Rito de Veia entram uma vez no dado da arma e não dobram no crítico. O trunfo de efeito rola o dado e guarda (acertou o aplica)."""
    x = 0; ha = a.get('hab') or {}
    if not ha: return 0
    d_rito = rito_dado(a)
    if d_rito: x += L.D.d(d_rito); _usa(a, 'rito_veia')
    if hg.get('livre') or hg.get('extra'): return x
    uso = _trunfo_uso(S, a, e)
    if uso and uso != 'nao':
        tr = a['trunfos']; tr[0] -= 1; a['trunfo_t'] = a['turnos_n']; v = L.D.d(tr[1]); _usa(a, 'trunfos'); _conta(S, 'trunfo_' + uso)
        if uso == 'dano': x += v
        else: hg['trunfo'] = (uso, v)
        L.diz(S, f"    o trunfo de {a['nome']} ({'no dano' if uso == 'dano' else 'na ' + uso if uso in ('rasteira', 'ameaca') else 'no ' + uso}: {v})".replace('ameaca', 'ameaça'))
        if tr[0] <= 0 and a.get('controla'): L._para(S, a, f"os trunfos de {a['nome']} acabaram")
    quer_voto = a.get('voto_ordem') if a.get('controla') else True          # quem o jogador comanda só gasta a Mana com a ordem (`fazer voto [sempre]`); o robô, sozinho
    if 'golpe_voto' in ha and quer_voto and a.get('voto_r') != S['r'] and (a.get('mana') or 0) >= n(a, 'golpe_voto', 'mana'):
        a['mana'] -= n(a, 'golpe_voto', 'mana'); a['voto_r'] = S['r']; _usa(a, 'golpe_voto')
        if a.get('voto_ordem') == 'uma': a['voto_ordem'] = None
        import magia
        hg['voto'] = n(a, 'golpe_voto', 'dano') * (2 if n(a, 'golpe_voto', 'dobro') and S.get('magia') and magia.maldito(S, e) else 1)      # o dobro contra o maldito, do Perito (o forte abre no Perito: 12.4)
    return x


def rito_dado(f):
    """o dado do RITO DE VEIA neste golpe ou feitiço (0 se não vale): por N turnos, e o turno de abrir é o primeiro deles (a leitura com que as medidas de 6.7 foram feitas:
    DESENHO 12.4; o golpe que sobra no turno de abrir já leva o dado)"""
    ri = f.get('rito') if f.get('acesa') == 'rito_veia' else None
    return ri[0] if ri and f['turnos_n'] <= ri[1] else 0


def tecnica(S, a, e, w):
    """o grupo TÉCNICA da pilha (até +40%): as batidas da Roda, os pontos da Sanha, o Golpe de Voto"""
    hg = a.get('_hg') or {}; t = 0.0
    if hg.get('roda'): t += H.RODA_BATIDA * a['batidas']
    if a.get('acesa') == 'sanha': t += H.SANHA_PONTO * a['sanha']
    t += hg.get('voto') or 0
    return t


def errou(S, a, e, w, j, df):
    """o golpe errou: a batida da Roda conta (dois 1 zeram; o fecho que erra perde metade); a RIPOSTA de quem apara"""
    hg = a.get('_hg') or {}
    if hg.get('roda'):
        teto = n(a, 'roda', 'batidas')
        if j['falha']: a['batidas'] = 0; L.diz(S, f"    a Roda de {a['nome']} perde o compasso (dois 1)")
        elif hg.get('fecho'):
            a['batidas'] //= 2; a['fecho_ja'] = False; _conta(S, 'fecho_erra')
            L.diz(S, f"    o fecho de {a['nome']} erra: a Roda perde metade ({a['batidas']} batidas)")
            if a.get('controla'): L._para(S, a, f"o fecho de {a['nome']} errou (a Roda perdeu metade)")
        else: a['batidas'] = min(teto, a['batidas'] + 1)
    he = e.get('hab') or {}
    if j['falha'] or w['distancia'] or hg.get('livre') or hg.get('extra') or 'riposta' not in he or e.get('sem_riposta'): return
    if e['estado'] != 'pe' or a['estado'] != 'pe' or e['reac'] <= 0 or S['fim'] or not arma_ok(S, e, 'riposta'): return
    falta = df - j['total']; we = L.arma_de(S, e)
    if 0 < falta <= n(e, 'riposta', 'margem') and L.dist(e, a) <= max(1, we['alcance']) and not we['distancia']:
        e['reac'] -= 1; _usa(e, 'riposta'); _conta(S, 'riposta'); L.golpe(S, e, a, we, livre='a riposta')


def acertou(S, a, e, w, j, dano, pv0, pc, vestida, extra):
    """o golpe acertou (com ou sem dano): a batida e o fecho da Roda, o ABRIR, o dançarino ferido, a Sanha, o trunfo de efeito, a declarada"""
    hg = a.get('_hg') or {}; ha = a.get('hab') or {}
    if hg.get('roda'):
        teto = H.num('roda', 'batidas', ha['roda'])
        if hg.get('fecho'):
            b = a['batidas']
            if hg['fecho'] == 'tranco' and dano > 0 and e['estado'] == 'pe': L._carga(S, e, w, 'cabeca', H.RODA_FECHO_TRANCO * b, pc, vestida, extra)
            a['batidas'] = 0; a['fecho_ja'] = False; _conta(S, 'fecho')
            L.diz(S, f"    o FECHO {hg['fecho'].upper()} de {a['nome']} gasta {b} batidas")
        else: a['batidas'] = min(teto, a['batidas'] + 1)
        if ha['roda'] >= 3 and a.get('abrir_t') != a['turnos_n'] and e['estado'] == 'pe': a['abrir_t'] = a['turnos_n']; e['abrir_de'] = (a['nome'], S['r'])
        if e['lado'] == 'A' and a['lado'] == 'B' and a['batidas'] >= H.RODA_FECHO_DESDE and ha['roda'] >= 2: _para_lado_a(S, f"{a['nome']} está com o fecho pronto")
    if dano > 0 and e.get('acesa') == 'roda' and e['batidas'] > 0 and g(e, 'roda') < H.GM: e['batidas'] -= 1
    if dano > 0:
        for f in (a, e):
            if f.get('acesa') == 'sanha' and f['estado'] == 'pe': _sanha_mais(S, f, 1)
        a['sangue_r'] = S['r']; e['sangue_r'] = S['r']
        _sanha_acende(S, a, e)
    tr = hg.get('trunfo')
    if tr and e['estado'] == 'pe':
        uso, v = tr
        if uso == 'ameaca': e['medo_fontes'][f"ameaca:{a['nome']}"] = max(e['medo_fontes'].get(f"ameaca:{a['nome']}", 0), H.TRUNFO_AMEACA + v)
        elif dano > 0:
            if uso == 'rasteira': L._carga(S, e, w, 'pernas', v, pc, vestida, extra)
            elif uso == 'tranco': L._carga(S, e, w, 'cabeca', v, pc, vestida, extra)
            elif uso == 'corte' and not L.tem(e, 'sem vida'): L._filete(S, e, max(1, int(dano * H.TRUNFO_CORTE[0])), H.TRUNFO_CORTE[1], f"trunfo:{a['nome']}", soma=False)
    k = hg.get('decl')
    if k and e['estado'] == 'pe':
        gk = ha[k]
        if k == 'tranco': _tranco(S, a, e, gk)
        elif k == 'corte_fundo' and dano > 0 and not L.tem(e, 'sem vida'):
            fr, rd = H.num('corte_fundo', 'filete', gk); L._filete(S, e, max(1, int(dano * fr)), rd, f"corte:{a['nome']}", soma=False)
        elif k == 'rasteira' and dano > 0: L._carga(S, e, w, 'pernas', H.num('rasteira', 'carga', gk), pc, vestida, extra)


def _tranco(S, a, e, gk):
    """o TRANCO DE LUTA: o golpe declarado que acerta tira o turno seguinte e dá o calejo de cabeça (nunca na cabeça firme; ninguém perde mais de 1 em cada 3); do Mestre,
    esse calejo não sobe a resistência"""
    if e['firme_cabeca'] > 0 or e['perde_turno'] or not L._pode_perder(e): return
    e['perde_turno'] = True; e['aberto'] = S['r'] + 1; _conta(S, 'tranco'); _conta(S, 'atordoa')
    if gk < 4: e['calejo_f']['cabeca'] += 1
    L.diz(S, f"    o TRANCO de {a['nome']}: {e['nome']} fica ATORDOADO (perde o próximo turno e fica aberto)")
    L._para(S, e, f"{e['nome']} ficou atordoado (perde o próximo turno)", so_controlado=True)


def extras(S, a, w, r):
    """a VARRIDA (os usos por luta): o golpe que acertou pega também um outro colado, com metade do dano (no Grão-Mestre, inteiro). Com a Varredura ou a Tempestade da arma,
    vale o maior (P5): a habilidade não soma"""
    ha = a.get('hab') or {}
    if 'varrida' not in ha or not a.get('varrida') or not r or not r.get('acertou') or w['distancia'] or a['estado'] != 'pe' or S['fim']: return
    ef = w.get('efeitos') or {}
    if ef.get('varredura') or ef.get('tempestade') or not arma_ok(S, a, 'varrida', w) or a['usos'].get('varrida', 0) >= n(a, 'varrida', 'usos'): return
    outros = [o for o in L.inimigos(S, a) if o is not r['e'] and L.dist(a, o) <= 1]
    if not outros: return
    o = min(outros, key=lambda x: (x['pv'] / x['pvmax'], x['nome'])); a['usos']['varrida'] = a['usos'].get('varrida', 0) + 1; _usa(a, 'varrida'); _conta(S, 'varrida')
    if a['varrida'] == 'uma': a['varrida'] = None
    L.golpe(S, a, o, w, livre='a varrida', extra=True if n(a, 'varrida', 'inteiro') else 'meio')


def sanha_cabeca(e): return e.get('acesa') == 'sanha' and e.get('sanha', 0) >= H.SANHA_CABECA


def fresta(S, a, w):
    """a MIRA FIRME do Perito em diante: mirar a fresta, no tiro, pede −5 e não −8 (o acerto da mira na fresta que o luta.py usa), ou None (o uso conta só no tiro que mira: `mirou`)"""
    if w['distancia'] and 'mira_firme' in (a.get('hab') or {}) and H.num('mira_firme', 'fresta', g(a, 'mira_firme')): return H.MIRA_FRESTA
    return None


def mirou(a): _usa(a, 'mira_firme')


def lancou(S, f):
    """A CORRENTE: cada feitiço seguido soma 1 (até o teto do grau); vale no feitiço seguinte"""
    if 'corrente' in (f.get('hab') or {}):
        f['corrente'] = min(n(f, 'corrente', 'pilha'), (f.get('corrente') or 0) + 1); _usa(f, 'corrente')


# ---------- o turno: a decisão, a ação, o fim da rodada ----------
def decide(S, f, o, pagou):
    """a ação de habilidade deste lutador agora (('hab', CHAVE, alvo)), ou None (segue a decisão de sempre)"""
    if f['estado'] != 'pe' or f['chao'] or not f.get('hab'): return None
    hb = f['hab']
    if f.get('controla'):
        if o.get('acao') != 'fazer': return None
        k = o['hab']; ant = o.get('antes'); sempre = o.get('sempre')
        def volta_ordem():
            if ant: S['ordens'][f['nome']] = ant
            else: S['ordens'].pop(f['nome'], None)
        why = _nao_pode(S, f, k, o.get('alvo'))
        if why:                                             # sem `sempre`, a ordem de uma vez que não pôde para a luta; com `sempre`, acabou o que paga: volta a ordem de antes
            volta_ordem(); L._para(S, f, (f"a ordem {_contrai('de', k)} acabou: {why}" if sempre else f"a habilidade da ordem não pôde: {why}"), so_controlado=True); return None
        if sempre:                                          # (6.4) com `sempre`, a ordem vale até acabar o que paga, o alvo cair ou vir outra ordem
            if k == 'mira_firme' and f.get('mira'): return None                 # a Mira Firme com `sempre`: mira, atira, mira, atira (o tiro sai pela ordem de sempre, com a mira)
            if k == 'ferro_brasa' and not L._filetes_rodada(_alvo_ferro(S, f, o.get('alvo'))): return None      # sem sangue a estancar, a ação é a de sempre
            return ('hab', k, o.get('alvo'))
        volta_ordem(); return ('hab', k, o.get('alvo'))
    inim = L.inimigos(S, f); w = L.arma_de(S, f)
    if 'brado' in hb and not f['usos'].get('brado') and inim:
        perto = [e for e in inim if L.dist(f, e) <= H.BRADO_CASAS]
        if len(perto) >= min(2, len(inim)): return ('hab', 'brado', None)
    if 'rito_veia' in hb and not f['usos'].get('rito_veia') and f['acesa'] != 'rito_veia' and f['pv'] > f['pvmax'] * 0.25 and L.alvos(S, f, w, cerco=False): return ('hab', 'rito_veia', None)
    if 'sopro_volta' in hb and 'sopro_volta' not in f['hab_dia']:
        c = [x for x in S['L'] if x['lado'] == f['lado'] and x['estado'] == 'caido' and L.dist(f, x) <= 1 and x.get('caiu_r') is not None]
        if c: return ('hab', 'sopro_volta', c[0]['nome'])
    if 'ferro_brasa' in hb and g(f, 'ferro_brasa') >= 2 and not any(L.dist(f, e) <= 1 for e in inim) and L._ataveis_rodada(f) >= f['pvmax'] * TE.ATAR_SOZINHO * 2: return ('hab', 'ferro_brasa', None)
    if 'estanca' in hb and not any(L.dist(f, e) <= 1 for e in inim):
        cai = [x for x in caidos_ataveis(S, f) if max(x['morte']) < 3 or (H.num('estanca', 'levanta', g(f, 'estanca')) and not f.get('levantou'))]
        if cai: return ('atar', cai[0]['nome'])            # do Mestre, firma o caído colado (no Grão-Mestre, uma vez por luta, ele levanta)
        alv = [x for x in L.de_pe(S, f['lado']) if L.dist(f, x) <= 1 and x['pv'] < x['pvmax'] * 0.6 and x.get('curado', 0) < int(x['pvmax'] * T.CURA_TETO)]
        if alv: return ('atar', min(alv, key=lambda x: x['pv'] / x['pvmax'])['nome'])
    return None


def caidos_ataveis(S, f):
    """os caídos colados do lado de f que a Mão que Estanca do Mestre em diante alcança (firmar; no Grão-Mestre, levantar), vivos"""
    if g(f, 'estanca') < 4: return []
    return [x for x in S['L'] if x is not f and x['lado'] == f['lado'] and x['estado'] == 'caido' and L.dist(f, x) <= 1]


def _alvo_ferro(S, f, alvo):
    o = L.por_nome(S, alvo) if alvo else None
    return o if o and o['estado'] == 'pe' and o['lado'] == f['lado'] and L.dist(f, o) <= 1 else f


def _nao_pode(S, f, k, alvo=None):
    """por que a habilidade da ordem não pode agora (a frase), ou ''"""
    if k == 'brado' and f['usos'].get('brado'): return 'o Brado já saiu nesta luta'
    if k == 'rito_veia' and f['usos'].get('rito_veia'): return 'o Rito de Veia já saiu nesta luta'
    if k == 'mira_firme' and not L.arma_de(S, f)['distancia']: return 'a Mira Firme pede arco ou besta na mão'
    if k == 'sopro_volta':
        if 'sopro_volta' in f['hab_dia']: return 'o Sopro de Volta é de dia: já saiu hoje'
        x = L.por_nome(S, alvo or '')
        if not x or x['estado'] != 'caido' or L.dist(f, x) > 1: return f'{alvo} não está caído ao seu lado'
    return ''


def faz(S, f, ac):
    """a ação de habilidade (o luta._turno chama): o Brado, o Rito de Veia, a Mira Firme, o Ferro em Brasa, o Sopro de Volta"""
    k = ac[1]; alvo = L.por_nome(S, ac[2]) if len(ac) > 2 and ac[2] else None; _usa(f, k); f['hab_feitas'].append(k)
    if k == 'brado':
        f['usos']['brado'] = 1; cd = n(f, 'brado', 'cd'); ouvem = [e for e in L.inimigos(S, f) if L.dist(f, e) <= H.BRADO_CASAS]
        for e in ouvem: e['medo_fontes'][f"brado:{f['nome']}"] = max(e['medo_fontes'].get(f"brado:{f['nome']}", 0), cd)
        L.diz(S, f"  {f['nome']} dá o BRADO DE GUERRA (coragem contra {cd}: {', '.join(e['nome'] for e in ouvem) or 'ninguém ouve'})"); _conta(S, 'brado')
    elif k == 'rito_veia':
        f['usos']['rito_veia'] = 1; q = L.D.d(n(f, 'rito_veia', 'custo')); f['pv'] -= q; S['dano_r'] += q / f['pvmax']
        acende(S, f, 'rito_veia'); f['rito'] = [n(f, 'rito_veia', 'dado'), f['turnos_n'] + n(f, 'rito_veia', 'turnos') - 1]      # [o dado, o último turno]: o de abrir é o primeiro dos N (12.4)
        L.diz(S, f"  {f['nome']} abre o RITO DE VEIA: paga {q} de PV ({max(f['pv'], 0)}/{f['pvmax']}); +1d{f['rito'][0]} em cada golpe e feitiço por {n(f, 'rito_veia', 'turnos')} turno(s)")
        if f['pv'] <= 0: L._cai(S, f, 0)
    elif k == 'mira_firme':
        f['mira'] = n(f, 'mira_firme', 'acerto'); f['mira_t'] = f['turnos_n']; L.diz(S, f"  {f['nome']} mira (+{f['mira']} no próximo tiro)")
    elif k == 'ferro_brasa':
        o = _alvo_ferro(S, f, ac[2] if len(ac) > 2 else None)
        q = L._filetes_rodada(o); o['filetes'] = []; o['sangra'] = None; o.pop('queimando', None); f['cansa_mais'] += 0 if o is not f else H.FERRO_CANSA
        if o is not f: o['cansa_mais'] = o.get('cansa_mais', 0) + H.FERRO_CANSA
        if not n(f, 'ferro_brasa', 'sem_acao'): o['atordoado'] = max(o['atordoado'], 1)
        L.diz(S, f"  {f['nome']} passa o FERRO EM BRASA {'em si' if o is f else 'em ' + o['nome']}: estanca todo o sangue ({q} por rodada)" + ('' if n(f, 'ferro_brasa', 'sem_acao') else '; dói: perde 1 ação'))
    elif k == 'sopro_volta' and alvo and alvo['estado'] == 'caido':
        teto = max(0, int(alvo['pvmax'] * T.CURA_TETO) - alvo.get('curado', 0)); gpv = max(1, min(teto, int(alvo['pvmax'] * n(f, 'sopro_volta', 'pv'))))
        alvo['estado'] = 'pe'; alvo['pv'] = gpv; alvo['curado'] = alvo.get('curado', 0) + gpv; alvo['morte'] = [0, 0]; f['hab_dia'].append('sopro_volta'); f['cansa_mais'] += 2
        L.diz(S, f"  {f['nome']} dá o SOPRO DE VOLTA: {alvo['nome']} se levanta ({gpv}/{alvo['pvmax']})"); _conta(S, 'sopro')


def acao(S, f, ac):
    """o que a ação escolhida faz com a pilha: a outra ação zera a Roda; tomar fôlego ou recuar apaga a Sanha; golpear ou andar zera a Corrente"""
    if not f.get('hab'): return
    if f.get('batidas') and ac[0] not in ('golpe', 'folego'): f['batidas'] = 0; _conta(S, 'roda_zera')
    if f.get('acesa') == 'sanha' and (ac[0] == 'folego' or (ac[0] == 'anda' and ac[2])): _apaga(S, f, 'sem fôlego' if ac[0] == 'folego' else 'recuou')
    if f.get('corrente') and ac[0] in ('golpe', 'anda'): f['corrente'] = 0


def fecha_rodada(S):
    """o fim da rodada: a Sanha sem sangue perde metade; a pilha da Mão que Estanca quebra na rodada sem atar"""
    for f in L.de_pe(S):
        if not f.get('hab'): continue
        if f.get('acesa') == 'sanha' and f.get('sangue_r') != S['r']:
            f['sanha'] //= 2
            if f['sanha'] <= 0: _apaga(S, f, 'a rodada sem sangue')
        if f['estanca'][1] != S['r']: f['estanca'][0] = 0


def ata(S, f, nome_alvo=None):
    """a MÃO QUE ESTANCA no atar: corta filetes (1·1·2·2·3·todos) e cura 4% do PV máximo, +3% por ponto da pilha (cada atadura seguida na luta), no teto do dia.
    Do Mestre, atar o CAÍDO colado o firma (não rola a morte); no Grão-Mestre, uma vez por luta, ele levanta com 10% do PV (no teto do dia; sem teto, só firma)."""
    x = L.por_nome(S, nome_alvo) if nome_alvo else None
    if x is not None and x in caidos_ataveis(S, f): return _ata_caido(S, f, x)
    o = x if x is not None and x['estado'] == 'pe' and x['lado'] == f['lado'] and L.dist(f, x) <= 1 else f
    gr = g(f, 'estanca'); pil = _pilha_estanca(S, f, gr)
    cortados = _corta(o, H.num('estanca', 'filetes', gr))
    teto = max(0, int(o['pvmax'] * T.CURA_TETO) - o.get('curado', 0))
    gpv = min(o['pvmax'] - o['pv'], teto, max(1, int(o['pvmax'] * (H.ESTANCA_CURA[0] + H.ESTANCA_CURA[1] * pil[0]))))
    if gpv > 0: o['pv'] += gpv; o['curado'] = o.get('curado', 0) + gpv; S['dano_r'] -= gpv / o['pvmax']
    _usa(f, 'estanca'); _conta(S, 'estanca')
    L.diz(S, f"  {f['nome']} {'se ata' if o is f else 'ata ' + o['nome']} com a Mão que Estanca: corta {cortados} filete(s)" + (f", cura {gpv} ({o['pv']}/{o['pvmax']})" if gpv > 0 else '') + f" (pilha {pil[0]})")


def _pilha_estanca(S, f, gr):
    pil = f['estanca']
    pil[0] = min(H.num('estanca', 'pilha', gr), pil[0] + 1 if pil[1] in (S['r'], S['r'] - 1) else 1); pil[1] = S['r']
    return pil


def _corta(o, corta):
    """corta até `corta` filetes de o, do mais forte ao mais fraco (o da ferida e os dos efeitos; os que não se atam ficam); devolve quantos cortou"""
    cortados = 0
    while corta > 0 and (o['sangra'] or [x for x in o['filetes'] if not x[3]]):
        cands = [('ferida', o['sangra'])] if o['sangra'] else []
        cands += [('efeito', x) for x in o['filetes'] if not x[3]]
        qual, x = max(cands, key=lambda c: c[1][0])
        if qual == 'ferida': o['sangra'] = None; o.pop('queimando', None)
        else: o['filetes'].remove(x)
        corta -= 1; cortados += 1
    return cortados


def _ata_caido(S, f, o):
    """a Mão que Estanca do Mestre no caído colado: corta os filetes e o FIRMA (não rola mais a morte); a do Grão-Mestre, uma vez por luta, o LEVANTA com 10% do PV (no teto do dia)"""
    gr = g(f, 'estanca'); pil = _pilha_estanca(S, f, gr); cortados = _corta(o, H.num('estanca', 'filetes', gr))
    teto = max(0, int(o['pvmax'] * T.CURA_TETO) - o.get('curado', 0)); gpv = min(teto, max(1, int(o['pvmax'] * H.ESTANCA_LEVANTA)))
    _usa(f, 'estanca'); _conta(S, 'estanca')
    if H.num('estanca', 'levanta', gr) and not f.get('levantou') and gpv > 0:
        o['estado'] = 'pe'; o['pv'] = gpv; o['curado'] = o.get('curado', 0) + gpv; o['morte'] = [0, 0]; f['levantou'] = True; S['dano_r'] -= gpv / o['pvmax']; _conta(S, 'estanca_levanta')
        L.diz(S, f"  {f['nome']} ata {o['nome']} com a Mão que Estanca: corta {cortados} filete(s), e {o['nome']} SE LEVANTA ({gpv}/{o['pvmax']}; uma vez por luta)"); return
    o['morte'] = [max(3, o['morte'][0]), o['morte'][1]]; _conta(S, 'estanca_firma')
    L.diz(S, f"  {f['nome']} ata {o['nome']}, caído, com a Mão que Estanca: corta {cortados} filete(s); {o['nome']} fica firme (não rola mais a morte)")


def caiu(S, e):
    """alguém caiu: a VIGÍLIA de um aliado a 1 casa (2 no Grão-Mestre) gasta a reação e o firma (não rola a morte); a marca da queda, para o Sopro de Volta"""
    e['caiu_r'] = S['r']
    if e['estado'] != 'caido': return
    for v in L.de_pe(S, e['lado']):
        if v is e or 'vigilia' not in (v.get('hab') or {}) or v['reac'] <= 0: continue
        gv = g(v, 'vigilia')
        if L.dist(v, e) > H.num('vigilia', 'casas', gv): continue
        if not H.num('vigilia', 'qualquer', gv) and any(n_ == v['nome'] for n_, _ in sum((x['golpeado'] for x in S['L']), [])): continue
        v['reac'] -= 1; e['morte'] = [3, e['morte'][1]]; _usa(v, 'vigilia'); _conta(S, 'vigilia')
        L.diz(S, f"    {v['nome']} se põe sobre {e['nome']} (a Vigília): {e['nome']} fica firme, não rola a morte"); return


def recuo(S, f):
    """o PÉ DE LEBRE: as casas de cada recuo (o primeiro da luta no Iniciante; todo recuo do Aprendiz), ou 0"""
    if 'pe_lebre' not in (f.get('hab') or {}): return 0
    gr = g(f, 'pe_lebre'); f['recuos'] = f.get('recuos', 0) + 1
    if f['recuos'] > 1 and not H.num('pe_lebre', 'todo', gr): return 0
    _usa(f, 'pe_lebre'); return H.num('pe_lebre', 'casas', gr)


def retirada(S, f):
    """a distância em que quem recua sai da luta (8; o Pé de Lebre do Perito, 6; do Grão-Mestre, 4)"""
    return H.num('pe_lebre', 'sai', g(f, 'pe_lebre')) if 'pe_lebre' in (f.get('hab') or {}) else T.RETIRADA


def segura(S, e, r):
    """o MANTER À DISTÂNCIA do Perito: o golpe livre que fere quem entra no alcance o segura fora"""
    return bool(r and r.get('dano', 0) > 0 and (e.get('_hg') or {}).get('manter') and g(e, 'manter') >= 3)


# ---------- a ordem (luta.ordem chama), conferida inteira antes de qualquer dado ----------
FAZ_ACAO = ('brado', 'rito_veia', 'mira_firme', 'ferro_brasa', 'sopro_volta')
RESERVADAS = ('sempre', 'firme', 'agressiva', 'defensiva', 'bigorna')
RE_TRUNFO = re.compile(r'\btrunfo\s*=\s*(.+?)(?=\s+(?:sem riposta|com riposta|sem voto|com voto|sempre|firme|agressiva|defensiva|bigorna)\b|$)')
SANHA_NAO = 'a Sanha não cabe em postura defensiva (nem na bigorna): na fúria não se guarda'


def _le_trunfo(f, spec):
    """'tranco se carga>=6, senão dano' → {uso, se: (carga, 6), senao}"""
    s = spec.strip().lower().replace('senao', 'senão').replace('ameaça', 'ameaca'); m = re.match(r'^(\w+)(?:\s+se\s+(.+?))?(?:\s*,?\s*senão\s+(\w+))?$', s)
    if not m: sys.exit(f'o trunfo se diz assim: trunfo=tranco se carga>=6, senão dano (usos: {", ".join(H.TRUNFO_USOS)}; condições: carga>=N, pernas>=N, abalado, metade)')
    uso, cond, senao = m.groups(); gt = g(f, 'trunfos')
    for u in (uso, senao):
        if u is None: continue
        if u not in H.TRUNFO_USOS: sys.exit(f'o trunfo vai a: {", ".join(H.TRUNFO_USOS)} (veio "{u}")')
        if gt < H.TRUNFO_DESDE[u]: sys.exit(f'o trunfo de {u} abre no {grau_diz(H.TRUNFO_DESDE[u])} (os Trunfos de {f["nome"]} estão no {grau_diz(gt)})')
    se = None
    if cond:
        c = re.match(r'^(carga|pernas)\s*>=\s*(\d+)$', cond.strip()) or re.match(r'^(abalado|metade)$', cond.strip())
        if not c: sys.exit(f'a condição do trunfo é uma de: carga>=N, pernas>=N, abalado, metade (veio "{cond}")')
        se = (c.group(1), int(c.group(2))) if c.lastindex == 2 else (c.group(1), 0)
    return dict(uso=uso, se=se, senao=senao)


def ordem(S, f, resto):
    """as palavras novas da ordem de quem o jogador comanda (conferidas antes do dado; a errada é recusada com a frase): `fazer HABILIDADE ...`, `trunfo=...`, `sem riposta`,
    `com riposta`. Devolve o resto da ordem de sempre (texto), ou None se a ordem toda foi de habilidade e não muda a ação"""
    hb = f.get('hab') or {}; txt = resto; mexe = []                 # (conferida inteira antes de mexer em qualquer coisa: a ordem recusada não deixa nada pela metade)
    sanha = f.get('acesa') == 'sanha' or f.get('sanha_arma')
    m = RE_TRUNFO.search(txt)
    if m:
        if 'trunfos' not in hb: sys.exit(f'{f["nome"]} não tem os Trunfos')
        tro = _le_trunfo(f, m.group(1))
        if f.get('trunfos') and f['trunfos'][0] <= 0 and tro['uso'] != 'nao': sys.exit(f'os trunfos de {f["nome"]} acabaram nesta luta (voltam com um bloco de descanso)')
        mexe.append(('trunfo_ordem', tro)); txt = (txt[:m.start()] + txt[m.end():]).strip()
    for frase, campo, k_, v in (('sem riposta', 'sem_riposta', 'riposta', True), ('com riposta', 'sem_riposta', 'riposta', False), ('sem voto', 'voto_ordem', 'golpe_voto', None), ('com voto', 'voto_ordem', 'golpe_voto', 'sempre')):
        if re.search(r'\b' + frase + r'\b', txt):
            if k_ not in hb: sys.exit(f'{f["nome"]} não tem {nome(k_)}')
            mexe.append((campo, v)); txt = re.sub(r'\s*\b' + frase + r'\b', '', txt).strip()
    pal = txt.split()
    if pal and pal[-1] in ('defensiva', 'bigorna') and sanha: sys.exit(SANHA_NAO)      # (6.4) a Sanha com postura defensiva é recusada antes do dado (acesa ou armada)
    if pal and pal[-1] == 'bigorna' and 'bigorna' not in hb: sys.exit(f'{f["nome"]} não tem a Guarda de Bigorna (a postura "bigorna")')
    if not pal or pal[0] != 'fazer':
        for campo, v in mexe: f[campo] = v
        if not pal: return None
        if pal[0] in ('recuar', 'guardar', 'lancar') and f.get('acesa') == 'sanha': _apaga(S, f, 'a ordem de ' + pal[0])
        return txt
    r = _fazer(S, f, pal, hb, sanha)                        # pode recusar (sys.exit) sem ter mexido em nada; só depois valem o trunfo= e o sem riposta da mesma ordem
    for campo, v in mexe: f[campo] = v
    return r


def _fazer(S, f, pal, hb, sanha):
    """a ordem `fazer HABILIDADE [em ALVO] [opções] [sempre] [postura]`: conferida antes de mexer; devolve o resto da ordem de sempre, ou None"""
    if len(pal) < 2: sys.exit('fazer o quê? (fazer roda · fecho · sanha · tranco · corte · rasteira · brado · rito · mira · varrida · voto · ferro · sopro)')
    post = pal.pop() if pal[-1] in RESERVADAS[1:] else None; sempre = 'sempre' in pal; pal = [x for x in pal if x != 'sempre']
    opc = {x.split('=', 1)[0]: x.split('=', 1)[1] for x in pal if '=' in x}; pal = [x for x in pal if '=' not in x]
    alvo = None
    if 'em' in pal:
        i = pal.index('em'); nm = ' '.join(pal[i + 1:]); pal = pal[:i]
        x = next((y for y in S['L'] if y['nome'].lower() == nm.lower() and y['estado'] == 'pe'), None)
        if not x: sys.exit(f'em quem? De pé: {", ".join(y["nome"] for y in L.de_pe(S))}')
        alvo = x['nome']
    pedido = ' '.join(pal[1:]); k = 'fecho' if pedido == 'fecho' else H.chave(pedido)
    if k is None and pal[1] not in ('fecho',):
        nomes_al = [y['nome'].lower() for y in S['L']]; resto_nome = ' '.join(pal[2:])
        k = H.chave(pal[1])
        if k and resto_nome and resto_nome.lower() in nomes_al: alvo = next(y['nome'] for y in S['L'] if y['nome'].lower() == resto_nome.lower())
        elif k and resto_nome: k = None
    if k is None: sys.exit(f'habilidade desconhecida: "{pedido}" (as de luta de {f["nome"]}: {", ".join(nome(x) for x in hb if x in H.LUTA) or "nenhuma"})')
    if post == 'bigorna' and 'bigorna' not in hb: sys.exit(f'{f["nome"]} não tem a Guarda de Bigorna (a postura "bigorna")')
    if post in ('defensiva', 'bigorna') and (sanha or k == 'sanha'): sys.exit(SANHA_NAO)
    w = L.arma_de(S, f)
    if k == 'fecho':
        if f.get('acesa') != 'roda': sys.exit(f'o fecho é da Roda acesa ({f["nome"]} não está dançando: `fazer roda`)')
        if g(f, 'roda') < 2: sys.exit('o fecho abre no Adepto da Roda')
        f['fecho_ja'] = True
        if opc.get('fecho') in ('fundo', 'tranco'): f['fecho_tipo'] = opc['fecho']
        return None
    if k not in hb: sys.exit(f'{f["nome"]} não tem {nome(k)}')
    h = H.HABILIDADES[k]
    if k != 'estanca' and not arma_ok(S, f, k, w): sys.exit(f'{Nome(k)} pede {", ".join(h["armas"] or ())} na mão ({f["nome"]} empunha {w["nome"]})')
    ant = S['ordens'].get(f['nome']); ant = ant.get('antes') if ant and ant.get('acao') in ('fazer', 'atar', 'animar', 'lancar', 'beber', 'usar') else ant
    if k == 'roda':
        if 'fecho' in opc:
            if opc['fecho'] not in ('fundo', 'tranco'): sys.exit('o fecho é fundo ou tranco')
            if g(f, 'roda') < 2: sys.exit('o fecho abre no Adepto da Roda')
            f['fecho_tipo'] = opc['fecho']
        acende(S, f, 'roda'); return ' '.join(['atacar'] + ([alvo] if alvo else []) + ([post] if post else []))
    if k == 'sanha':
        if f['sanha_vezes'] >= n(f, 'sanha', 'usos'): sys.exit(f'a Sanha de {f["nome"]} já saiu nesta luta ({n(f, "sanha", "usos")} por luta)')
        if f.get('acesa') == 'roda': _apaga(S, f, 'a Sanha')
        f['sanha_arma'] = True; return ' '.join(['atacar'] + ([alvo] if alvo else []) + ([post] if post else []))
    if k in H.DECLARADAS:
        if k == 'tranco' and f['usos'].get('tranco', 0) >= n(f, 'tranco', 'usos'): sys.exit(f'o Tranco de {f["nome"]} já foi gasto nesta luta ({n(f, "tranco", "usos")} por luta)')
        f['decl'] = dict(k=k, alvo=alvo, sempre=sempre); return ' '.join(['atacar'] + ([alvo] if alvo else []) + ([post] if post else []))
    if k == 'varrida':
        if f['usos'].get('varrida', 0) >= n(f, 'varrida', 'usos'): sys.exit(f'a Varrida de {f["nome"]} já foi gasta nesta luta')
        f['varrida'] = 'sempre' if sempre else 'uma'; return ' '.join(['atacar'] + ([alvo] if alvo else []) + ([post] if post else []))
    if k == 'trunfos': sys.exit('o trunfo é uma ordem com condição: trunfo=tranco se carga>=6, senão dano')
    if k == 'golpe_voto':                                   # o Golpe de Voto de quem o jogador comanda: só com a ordem (uma vez, ou `sempre`); `sem voto` desliga
        if (f.get('mana') or 0) < n(f, 'golpe_voto', 'mana'): sys.exit(f'o Golpe de Voto pede {n(f, "golpe_voto", "mana")} de Mana ({f["nome"]} tem {f.get("mana") or 0})')
        f['voto_ordem'] = 'sempre' if sempre else 'uma'; return ' '.join(['atacar'] + ([alvo] if alvo else []) + ([post] if post else []))
    if k in FAZ_ACAO:
        why = _nao_pode(S, f, k, alvo)
        if why: sys.exit(why)
        if k == 'ferro_brasa' and g(f, 'ferro_brasa') < 2: sys.exit('o Ferro em Brasa vale na luta do Adepto em diante (antes, 1 bloco fora dela: `habilidade.py ferro PACIENTE`)')
        f['controla'] = True; S['ordens'][f['nome']] = dict(acao='fazer', hab=k, alvo=alvo, antes=ant, **({'sempre': True} if sempre else {}), **({'postura': post} if post else {})); return None
    if k == 'estanca': sys.exit('a Mão que Estanca age no `atar` (em si, ou num aliado colado)')
    sys.exit(f'{Nome(k)} não se faz por ordem: {"vale sozinha" if h["tipo"] in ("passiva", "reacao") else "fora da luta"}')


# ---------- o quadro ----------
def linha(S, f):
    """o que as habilidades põem na linha do lutador no quadro: as batidas e o fecho, os pontos da Sanha, os trunfos, a de luta gasta, a declarada"""
    hb = f.get('hab') or {}
    if not hb or f['estado'] != 'pe': return ''
    L_ = []
    if f.get('acesa') == 'roda':
        teto = n(f, 'roda', 'batidas'); pronto = g(f, 'roda') >= 2 and f['batidas'] >= H.RODA_FECHO_DESDE
        L_.append(f"Roda {f['batidas']}/{teto} batidas" + (', fecho pronto' if pronto else ''))
    if f.get('acesa') == 'sanha': L_.append(f"Sanha {f['sanha']}/{n(f, 'sanha', 'pontos')} pontos")
    elif f.get('sanha_arma'): L_.append('Sanha armada (acende no primeiro sangue)')
    if f.get('acesa') == 'rito_veia' and f.get('rito'): L_.append(f"Rito de Veia (+1d{f['rito'][0]}, até o turno {f['rito'][1]})")
    if f.get('trunfos'): L_.append(f"trunfos {f['trunfos'][0]} de d{f['trunfos'][1]}" + (f" ({_diz_trunfo(f['trunfo_ordem'])})" if f.get('trunfo_ordem') else ''))
    if f.get('decl'): L_.append(f"declarou {nome(f['decl']['k'])}" + (f" em {f['decl']['alvo']}" if f['decl'].get('alvo') else '') + (' (sempre)' if f['decl'].get('sempre') else ''))
    gastas = [nome(k) for k in ('tranco', 'brado', 'rito_veia', 'varrida') if k in hb and f['usos'].get(k, 0) >= (n(f, k, 'usos') if 'usos' in H.HABILIDADES[k]['g'] else 1)]
    if 'sanha' in hb and f['sanha_vezes'] >= n(f, 'sanha', 'usos') and f.get('acesa') != 'sanha': gastas.append('a Sanha')
    if gastas: L_.append('gastou ' + ', '.join(gastas))
    if f.get('corrente'): L_.append(f"Corrente {f['corrente']}/{n(f, 'corrente', 'pilha')}")
    if f.get('sem_riposta'): L_.append('sem riposta')
    if f.get('postura') == 'bigorna': L_.append('na bigorna')
    return ''.join(' · ' + x for x in L_)


def _diz_trunfo(o):
    if not o: return 'no dano'
    s = {'ameaca': 'na ameaça', 'nao': 'guardados', 'dano': 'no dano'}.get(o['uso'], 'no ' + o['uso'] if o['uso'] != 'rasteira' else 'na rasteira')
    if o.get('se'): s += f" se {o['se'][0]}" + (f">={o['se'][1]}" if o['se'][0] in ('carga', 'pernas') else '')
    if o.get('senao'): s += f", senão {o['senao']}"
    return s


# ---------- A MARCA DA CENA E O GRAU (6.2) ----------
def caminho_hab(p, k):
    """o caminho que segura o grau da habilidade nesta pessoa (as de arma, a maior mão de arma da família dela; as de magia, a melhor tradição)"""
    c = H.HABILIDADES[k]['caminho']
    ma = p.get('maestria') or {}
    if not isinstance(ma, dict): return c
    if c == 'arma':
        fam = max([x for x in ma if x in T.FAMILIAS and x != 'punho'] or ['espada'], key=lambda x: (ma.get(x, 0), x)); return TT.caminho_de(fam)
    if c == 'magia': return max(T.TRADICOES, key=lambda t: (ma.get(t, 0), t))
    return c


def mao_no(p, k):
    import talento
    return talento.mao_no(p, caminho_hab(p, k))


def marca_cena(dureza, usos, venceu, k, grau):
    """A MARCA DA CENA (uma por cena, de 0 a 6): dureza + 1 (se usou 3 vezes ou mais, ou se a de luta ou de dia venceu a cena) − o desconto do grau; a dureza 1 não dá marca do
    Adepto em diante (o freio 4)"""
    if usos <= 0 or dureza <= 0: return 0
    if dureza <= 1 and grau >= H.DUREZA_1_ATE: return 0
    m = dureza + (1 if usos >= H.USOS_MAIS or (venceu and k in H.DE_LUTA) else 0) - H.DESCONTO[grau]
    return max(0, min(H.MARCA_MAX, m))


def teto_de(p, k, reg=None):
    """até que grau esta habilidade sobe nesta pessoa: a origem (6.5), o talento (o Negado para no Adepto, o Lerdo no Mestre) e o apelão (só legado ou classe)"""
    import talento
    reg = reg if reg is not None else (p.get('habilidades') or {}).get(k) or {}
    org = str((reg or {}).get('origem') or 'licao').split(':')[0]
    t = H.ORIGEM_TETO.get(org, 3)
    t = min(t, H.TETO_TALENTO.get(talento.grau(p, caminho_hab(p, k)), H.GM))
    return t


def pede_marcas(p, k, grau):
    """as marcas que o grau pede nesta pessoa (vezes o talento do caminho: o Prodígio a metade, o Negado o dobro)"""
    import talento
    return math.ceil(round(H.MARCAS[grau] * TT.vezes(talento.grau(p, caminho_hab(p, k))), 6))


def falta_para(E, pid, k):
    """o que falta para o próximo grau ('' se pode subir; senão a frase)"""
    p = E['gente'][pid]; reg = (p.get('habilidades') or {}).get(k) or {}; gr = grau_de(reg); prox = gr + 1
    if gr >= H.GM: return 'no topo'
    if prox > teto_de(p, k, reg): return f"para no {grau_diz(teto_de(p, k, reg))} ({_porque_teto(p, k, reg)})"
    if reg.get('marcas', 0) < pede_marcas(p, k, prox): return f"{reg.get('marcas', 0)} de {pede_marcas(p, k, prox)} marcas"
    if mao_no(p, k) < H.MAO_DO_GRAU[prox]: return f"tem as marcas para {grau_diz(prox)}; falta a mão de {T.MAESTRIAS[H.MAO_DO_GRAU[prox]]} em {caminho_hab(p, k)}"
    if prox >= 4 and len(reg.get('feitos') or []) < prox - 3: return f"tem as marcas para {grau_diz(prox)}; falta o feito ({H.FEITO_DO_GRAU[prox]})"
    if reg.get('dia_grau') == E['relogio']['dia']: return 'um grau por dia: amanhã'
    return ''


def _porque_teto(p, k, reg):
    import talento
    org = str(reg.get('origem') or 'licao').split(':')[0]
    tt = H.TETO_TALENTO.get(talento.grau(p, caminho_hab(p, k)))
    if tt is not None and tt < H.ORIGEM_TETO.get(org, 3): return f"o talento {TT.TALENTO[talento.grau(p, caminho_hab(p, k))][0]} em {caminho_hab(p, k)}"
    return f"a origem: {H.ORIGEM_DIZ.get(org, org)}"


def sobe(E, pid, k=None):
    """a subida de grau (um por dia, um por evento): as marcas vezes o talento, a mão no caminho, o feito do Mestre e do Grão-Mestre, o teto da origem e do talento. Devolve as linhas
    da mesa ("A RODA DO MALHO SOBE: Adepto → Perito"; "tem as marcas para Mestre; falta o feito")"""
    import estado
    p = E['gente'].get(pid)
    if not p or p['estado'] != 'vivo': return []
    out = []
    for kk in ([k] if k else list(p.get('habilidades') or {})):
        reg = (p.get('habilidades') or {}).get(kk)
        if not isinstance(reg, dict): continue
        gr = grau_de(reg); fal = falta_para(E, pid, kk)
        if fal == '':
            estado.aplica(E, 'habilidade', [['pessoa', pid, f'hab.{kk}', 'grau', gr + 1]], onde=p['lugar'], quem=[pid], texto=f"{p['nome']}: {nome(kk)} sobe a {grau_diz(gr + 1)}")
            p = E['gente'][pid]; out.append(f"★ {Nome(kk).upper()} SOBE: {grau_diz(gr)} → {grau_diz(gr + 1)}" + _abre(kk, gr + 1))
        elif fal.startswith('tem as marcas') or fal.startswith('para no') and reg.get('marcas', 0) >= pede_marcas(p, kk, min(H.GM, gr + 1)):
            out.append(f"{Nome(kk)}: {fal}")
    return out


def _abre(k, gr):
    """o que o grau novo abre (a frase da subida)"""
    if k == 'roda': return {1: ' (teto 3 batidas)', 2: ' (abre o FECHO)', 3: ' (teto 4 batidas; abre o ABRIR)', 4: ' (teto 5; entra quente)', 5: ' (teto 6; entra com 2; o golpe que o fere não tira batida)'}.get(gr, '')
    if k == 'sanha': return f" (teto {H.num('sanha', 'pontos', gr)} pontos)"
    if k == 'trunfos': q, l = H.num('trunfos', 'dados', gr); return f" ({q} de d{l} por luta)"
    return ''


def volta(E, S, f, pid, ja=()):
    """O QUE A LUTA DEVOLVE AO ESTADO DAS HABILIDADES (num evento só, com a luta; 9.4): as marcas de cada habilidade usada (a dureza da luta, de conta.chance ao abrir), o feito
    (vencer com ela uma cena de dureza 5; o segundo, diante de alguém com nome), a de dia gasta, o cansaço da Sanha e do Ferro, os trunfos gastos. O estalo vem à parte (estalo)."""
    import estado
    p = E['gente'][pid]; ef = []; hb = p.get('habilidades') or {}
    if f['estado'] == 'morto': return ef
    ef += _vistas(E, S, f, pid) + legado_luta(E, S, f, pid)
    if f.get('acesa') == 'sanha': f['cansa_mais'] = f.get('cansa_mais', 0) + f.get('sanha_max', 0) // H.SANHA_CANSA_A_CADA
    if f.get('cansa_mais'): ef.append(['pessoa', pid, 'cansaco', 'soma', int(f['cansa_mais'])])      # (também em quem não tem habilidade: o Ferro em Brasa de um aliado dói nele)
    if not f.get('hab'): return ef
    tr = f.get('trunfos')
    if tr is not None and 'trunfos' in hb:
        q = H.num('trunfos', 'dados', grau_de(hb['trunfos']))[0] - tr[0]
        if q > 0: ef.append(['pessoa', pid, 'marca.trunfos', 'poe', dict(n=q, em=estado.agora(E))])
    venceu = S.get('fim') == f['lado']; d = (S.get('dureza') or {}).get(f['lado'], 0)
    nomeado = next((x for x in S['L'] if x.get('id') and x['lado'] != f['lado'] and x['id'] in E['gente']), None)      # o segundo feito: diante de alguém com nome (do outro lado)
    for k, usos in (f.get('hab_usos') or {}).items():
        reg = hb.get(k)
        if not isinstance(reg, dict) or usos <= 0: continue
        gr = grau_de(reg); m = marca_cena(d, usos, venceu, k, gr)
        if m > 0: ef.append(['pessoa', pid, f'hab.{k}', 'soma', m])
        ef += feito(E, pid, k, m, d, venceu, f"venceu com {nome(k)} uma luta de dureza {d}", diante=nomeado['nome'] if nomeado else None, ja=list(ja) + ef)
    for k in f.get('hab_dia') or []:
        if k in hb: ef.append(['pessoa', pid, f'hab.{k}', 'usada', E['relogio']['dia']])
    return ef


def feito(E, pid, k, marcas_novas, dureza, venceu, como, diante=None, ja=()):
    """O FEITO DO MESTRE E DO GRÃO-MESTRE (6.2), em qualquer cena com risco (a luta, a obra que remata, a conversa): vencer com a habilidade uma cena de dureza 5. Só conta quando
    a pessoa já tem as marcas do grau que o feito abre (o primeiro, as do Mestre; o segundo, as do Grão-Mestre: com as desta cena); o segundo pede alguém com nome diante (na luta,
    do outro lado) e vira notícia. Devolve os efeitos (o feito e a notícia), ou []."""
    p = E['gente'][pid]; reg = (p.get('habilidades') or {}).get(k)
    if not isinstance(reg, dict) or not venceu or dureza < H.FEITO_DUREZA: return []
    nf = len(reg.get('feitos') or [])
    if nf >= 2 or (nf == 1 and not diante): return []
    if reg.get('marcas', 0) + max(0, marcas_novas) < pede_marcas(p, k, 4 + nf): return []
    txt = como + (f", diante de {diante}" if nf == 1 else '')
    ef = [['pessoa', pid, f'hab.{k}', 'feito', dict(dia=E['relogio']['dia'], como=txt)]]
    if nf == 1:                                             # o segundo feito vira notícia
        import noticias, estado
        ef += noticias.nova(E, estado.onde(E, pid), f"{p['nome']} {txt}", peso=2, tags=('feito', 'habilidade'), ja=list(ja))
    return ef


def _vistas(E, S, f, pid):
    """as técnicas de batalhar que o outro lado usou nesta luta de verdade (para colher o jeito: vista 3 vezes, em 3 lutas, ou de quem foi vencido); o apelão e a assinatura não"""
    p = E['gente'][pid]; m = p.get('marca') or {}; vistas = dict(m.get('vistas') or {}); venc = list(m.get('vencidas') or []); mudou = False; venceu = S.get('fim') == f['lado']
    hoje = set()                                            # uma vez por luta, por mais que a usem
    for o in S['L']:
        if o['lado'] == f['lado']: continue
        for k, u in (o.get('hab_usos') or {}).items():
            if u > 0 and k in H.HABILIDADES and H.HABILIDADES[k]['campo'] == 'batalhar' and not H.apelao(k) and k not in (p.get('habilidades') or {}):
                if k not in hoje: vistas[k] = vistas.get(k, 0) + 1; hoje.add(k); mudou = True
                if venceu and o['estado'] != 'pe' and k not in venc: venc.append(k)
    return ([['pessoa', pid, 'marca.vistas', 'poe', vistas]] + ([['pessoa', pid, 'marca.vencidas', 'poe', venc]] if venc != list(m.get('vencidas') or []) else [])) if mudou else []


def dureza_luta(S):
    """a dureza da luta para cada lado (6.2: a chance de perder, pela conta rápida, ao abrir; entre iguais, 3)"""
    import conta
    try:
        pa = [conta._perfil(f) for f in S['L'] if f['lado'] == 'A']; pb = [conta._perfil(f) for f in S['L'] if f['lado'] == 'B']
        p = conta.chance_perfis(pa, pb)
    except (KeyError, ValueError, ZeroDivisionError, TypeError): p = 0.5
    return dict(A=H.dureza(1 - p), B=H.dureza(p))


def estalo(E, S, f, pid):
    """O ESTALO (6.5): em luta de verdade com a arma, rolagem oculta (8% com dureza 3 ou mais, 4% com 2; o Olho de Luta soma), no máximo um por semana; acende uma técnica da
    família da arma que a pessoa não tem (a lista curta). O PRIMEIRO estalo da pessoa traz também o Olho de Luta (a origem E de 6.7), se há vaga. Devolve (efeitos, a frase da
    mesa, a frase do SÓ O MESTRE): o estalo do personagem vai à mesa; o da gente do mundo é segredo (6.4: as habilidades escondidas e as rolagens do estalo são do Mestre), e à
    mesa vai no máximo "algo acendeu em X", sem o nome, se o personagem está na luta."""
    import estado, teste
    p = E['gente'][pid]
    if f['estado'] != 'pe' or not isinstance(f.get('arma'), dict) or f['arma']['item'] not in S.get('usadas', []): return [], '', ''
    d = (S.get('dureza') or {}).get(f['lado'], 0)
    if d < 2: return [], '', ''
    m = p.get('marca') or {}; dia = E['relogio']['dia']
    if isinstance(m.get('estalo'), int) and dia - m['estalo'] < H.ESTALO_SEMANA: return [], '', ''
    fam = _familia(S, f['arma']); hb = p.get('habilidades') or {}
    novas = [k for k in H.ESTALO_LISTA.get(fam, ()) if k not in hb and 'E' in H.HABILIDADES[k]['origens']]
    if not novas or vagas_usadas(p) >= H.VAGAS: return [], '', ''
    ch = H.ESTALO[3 if d >= 3 else 2] + (H.num('olho_luta', 'estalo', grau_de(hb['olho_luta'])) if 'olho_luta' in hb else 0)
    r = teste.rola_cem(E, f"o estalo ({p['nome']}, na luta com {f['arma']['nome']})", ch, quem=pid, oculto=True)
    if not r['passou']: return [], '', ''
    rnd = estado.sorte_fixa(E, f"estalo|{pid}|{dia}")
    if 'olho_luta' in hb and len(novas) >= 2 and p.get('jogador'): k, k2 = rnd.sample(novas, 2)        # o OLHO DE LUTA: escolhe entre duas da família (a primeira já entra)
    else: k, k2 = rnd.choice(novas), None
    ef = [['pessoa', pid, 'habilidade', 'aprende', dict(chave=k, origem='estalo')], ['pessoa', pid, 'marca.estalo', 'poe', dia]]
    olho = 'marca' not in p or 'estalo' not in m
    olho = olho and 'olho_luta' not in hb and vagas_usadas(p) + 2 <= H.VAGAS        # o primeiro estalo abre o olho (a origem E do Olho de Luta), se cabe na vaga
    if olho: ef.insert(1, ['pessoa', pid, 'habilidade', 'aprende', dict(chave='olho_luta', origem='estalo')])
    frase = f"algo acendeu em {p['nome']}: {Nome(k)} (do estalo, no Iniciante)" + (f"; e, no primeiro estalo, {nome('olho_luta')} se abre" if olho else '')
    if k2:
        import turno
        try: frase += '; o Olho de Luta viu também ' + nome(k2) + ': ' + turno.pergunta(E, f"O estalo de {p['nome']}: {Nome(k)} acendeu, e o Olho de Luta deixa trocar {_contrai('por', k2)}. Qual fica?",
                                                                                     [f"a=fica {nome(k)}", f"b=troca {_contrai('por', k2)} (o Mestre, num evento: esquece a primeira e aprende a outra, do estalo)"])
        except (SystemExit, KeyError): pass
    if p.get('jogador'): return ef, frase, ''
    eu = estado.eu(E); viu = bool(eu) and any(x.get('id') == eu for x in S['L'])
    return ef, (f"algo acendeu em {p['nome']}" if viu else ''), f"(só o Mestre) o estalo: {frase}"


# ---------- APRENDER, ESQUECER, ENSINAR, ESTUDAR, COPIAR ----------
def vagas_usadas(p): return sum(1 for r in (p.get('habilidades') or {}).values() if not (isinstance(r, dict) and r.get('classe')))


def chance_copia(p, k):
    """a chance de colher o jeito (6.5): 40% + 10% por grau de mão acima do que a técnica pede − 15% por grau abaixo + 5% por grau de Colher o Jeito, entre 5% e 90%"""
    pede = H.COPIA_PEDE.get(H.HABILIDADES[k]['teto'])
    if pede is None: return 0.0
    m = mao_no(p, k); dif = (m - pede) / 2; c = H.COPIA['base'] + (H.COPIA['acima'] * dif if dif > 0 else H.COPIA['abaixo'] * dif)
    cj = (p.get('habilidades') or {}).get('colher_jeito')
    if cj is not None: c += H.num('colher_jeito', 'chance', grau_de(cj))
    return max(H.COPIA['min'], min(H.COPIA['max'], c))


def _origem_nova(p, k, origem, vaga=True):
    """a habilidade que vem por esta origem: nasce (se há vaga), ou, se a pessoa já a tem por origem MENOR, o teto sobe e as marcas ficam (6.5). Devolve (o efeito, a frase);
    recusa (sys.exit) se ela já a tem por origem igual ou maior, ou se não há vaga"""
    reg = (p.get('habilidades') or {}).get(k); nova = origem.split(':')[0]
    ef = ['pessoa', None, 'habilidade', 'aprende', dict(chave=k, origem=origem)]
    if reg is not None:
        velha = str((reg or {}).get('origem') or '').split(':')[0] if isinstance(reg, dict) else ''
        if H.ORIGEM_TETO.get(nova, 0) > H.ORIGEM_TETO.get(velha, 0):
            return ef, f"{p['nome']} já tinha {nome(k)} ({H.ORIGEM_DIZ.get(velha, velha)}): o teto sobe para o {grau_diz(H.ORIGEM_TETO[nova])}; as marcas ficam"
        sys.exit(f"{p['nome']} já tem {nome(k)} ({H.ORIGEM_DIZ.get(velha, velha)}, até o {grau_diz(H.ORIGEM_TETO.get(velha, 3))}): {H.ORIGEM_DIZ.get(nova, nova)} não sobe o teto")
    if vaga and vagas_usadas(p) >= H.VAGAS: sys.exit(f"{p['nome']} já guarda {H.VAGAS} habilidades: esqueça uma antes (`habilidade.py esquece CHAVE`)")
    return ef, f"{Nome(k)} nasce no Iniciante ({H.ORIGEM_DIZ.get(nova, nova)}: sobe até o {grau_diz(H.ORIGEM_TETO[nova])})"


def _copia_confere(E, pid, k, de):
    """o que a tentativa de colher o jeito pede, conferido ANTES do dado (nenhuma recusa depois de rolar): devolve (p, o, k, tentativas já feitas, a chance)"""
    import estado
    p = estado.presente(E, pid, 'treinar a cópia'); k = H.chave(k) or sys.exit(f'habilidade desconhecida: "{k}"')
    o = E['gente'].get(de) or sys.exit(f'não há a pessoa "{de}"')
    ro = (o.get('habilidades') or {}).get(k)
    if ro is None: sys.exit(f"{o['nome']} não tem {nome(k)} para copiar")
    if H.apelao(k) or (isinstance(ro, dict) and ro.get('classe')): sys.exit(f"{Nome(k)} não se copia ({'o apelão' if H.apelao(k) else 'a assinatura de classe'})")
    t = (p.get('copias') or {}).get(k, 0)
    if t >= H.COPIA['tentativas']: sys.exit(f"{p['nome']} falhou três vezes {em(k)}: fechou para sempre")
    m = p.get('marca') or {}; vistas = (m.get('vistas') or {}).get(k, 0)
    if vistas < H.COPIA['ver'] and k not in (m.get('vencidas') or []):
        sys.exit(f"colher o jeito {_contrai('de', k)} pede vê-la {H.COPIA['ver']} vezes em lutas de verdade, ou vencer quem a usa ({p['nome']} a viu em {vistas}; o Mestre escreve a cena que o motor não viu: marca.vistas)")
    _origem_nova(p, k, 'copia')                             # recusa se já a tem por origem igual ou maior, ou se não há vaga
    return p, o, k, t, chance_copia(p, k)


def copia_chance(E, pid, k, de):
    """a chance de colher o jeito, SEM ROLAR (como o fala.py conta): o que a tentativa pede, a chance e as tentativas que restam"""
    p, o, k, t, ch = _copia_confere(E, pid, k, de)
    return (f"COLHER O JEITO {_contrai('de', k).upper()} (visto em {o['nome']}): a chance {round(100 * ch)}% (40% + 10% por grau de mão acima do que ela pede − 15% por grau abaixo"
            f" + o Colher o Jeito; entre 5 e 90%) · tentativa {t + 1} de {H.COPIA['tentativas']} (falhou as três, fecha para sempre) · custa um dia de treino (2 blocos pesados)")


def copia(E, pid, k, de):
    """uma TENTATIVA DE COLHER O JEITO (um dia de treino): a técnica vista 3 vezes em lutas de verdade, ou de quem foi vencido; três tentativas; a cópia nasce no Iniciante e para no
    Mestre; assinatura de classe e apelão não se copiam. Tudo conferido antes do dado; a chance vai à mesa antes da linha do dado (e `copia CHAVE de=PID chance` a mostra sem
    rolar); o dado rola uma vez (teste.rola_cem), e a tentativa vale num evento logo depois dele, ande o tempo ou não (o treino é o dia que passa)."""
    import estado, teste, ato
    p, o, k, t, ch = _copia_confere(E, pid, k, de)
    pre = f"(a chance: {round(100 * ch)}%; tentativa {t + 1} de {H.COPIA['tentativas']})"
    r = teste.rola_cem(E, f"colher o jeito {_contrai('de', k)} (visto em {o['nome']}; tentativa {t + 1} de 3)", ch, quem=pid)
    ef = [['pessoa', pid, f'copia.{k}', 'soma', 1]]; frase = ''
    if r['passou']:
        x, frase = _origem_nova(p, k, 'copia'); x[1] = pid; ef.append(x)
    estado.aplica(E, 'habilidade', ef, onde=p['lugar'], quem=[pid], texto=f"{p['nome']} tenta colher o jeito {_contrai('de', k)}: {'pegou' if r['passou'] else 'não pegou'}")
    try: nb, pq = ato.passa(E, pid, 2, 'treinar', esforco='pesado', texto=f"{p['nome']} treina para colher o jeito {_contrai('de', k)}")      # um dia de treino: a jornada (2 blocos)
    except SystemExit as x: nb, pq = 0, str(x)
    return (pre + '\n' + teste.diz(E, r) + (f"\n{p['nome']} colheu o jeito: {frase} (a cópia para no Mestre)." if r['passou'] else
                                           f"\nNão pegou." + (' Fechou para sempre (três tentativas).' if t + 1 >= 3 else f' Restam {2 - t} tentativas.'))
            + (f"\n  (o treino parou: {pq})" if pq else ''))


def ensina(E, pid, mestre, k, blocos=None):
    """o MESTRE ENSINA (6.5): quem tem a habilidade no Perito ou mais, a quem ele estima (a opinião +3, ou +6 no forte), com os blocos de treino JUNTOS (10, 20 e 40, pelo teto
    dela): os dois no mesmo lugar, o tempo passa para os dois (`ato.passa` com o mestre junto), e a conta fica em marca.ensino; no último bloco, ela nasce (de um mestre: sobe até o
    Mestre). Ninguém vivo ensina um apelão. Cada chamada é uma jornada (2 blocos), ou `blocos=N`."""
    import estado, gente, ato
    p = estado.presente(E, pid, 'treinar com o mestre'); o = E['gente'].get(mestre) or sys.exit(f'não há a pessoa "{mestre}"'); k = H.chave(k) or sys.exit(f'habilidade desconhecida: "{k}"')
    if mestre == pid: sys.exit('ninguém ensina a si mesmo')
    if o['estado'] != 'vivo': sys.exit(f"{o['nome']} {estado.morte_diz(E, o)}")
    if estado.onde(E, mestre) != estado.onde(E, pid): sys.exit(f"{o['nome']} não está com {p['nome']}: o treino é junto, no mesmo lugar")
    ro = (o.get('habilidades') or {}).get(k)
    if ro is None or grau_de(ro) < H.ENSINA_DESDE: sys.exit(f"{o['nome']} não tem {nome(k)} no Perito ou mais: não ensina")
    if H.apelao(k): sys.exit('ninguém vivo ensina um apelão (ele só nasce de legado ou de classe Lendária)')
    if 'Me' not in H.HABILIDADES[k]['origens']: sys.exit(f"{Nome(k)} não se ensina (origens: {', '.join(H.ORIGEM_DIZ[x] for x in H.letras_origem(k))})")
    op = gente.opiniao(E, mestre, pid)[0]; quer = H.ENSINA_OPINIAO[H.HABILIDADES[k]['teto']]
    if op < quer: sys.exit(f"{o['nome']} não estima {p['nome']} o bastante (a opinião {op}; pede {quer})")
    x, frase = _origem_nova(p, k, f'mestre:{mestre}'); x[1] = pid
    bl = H.ENSINA_BLOCOS[H.HABILIDADES[k]['teto']]; m = (p.get('marca') or {}).get('ensino') or {}
    feito = m.get('n', 0) if (m.get('mestre'), m.get('chave')) == (mestre, k) else 0
    vez = max(1, min(int(blocos) if blocos else 2, bl - feito))
    def mais(i):
        n_ = feito + i + 1
        return [['pessoa', pid, 'marca.ensino', 'poe', dict(mestre=mestre, chave=k, n=n_)]] + ([x] if n_ >= bl else [])
    estado.em_cena(E, mestre)
    nb, pq = ato.passa(E, pid, vez, 'habilidade', esforco='pesado', mais=mais, com=(mestre,), texto=f"{o['nome']} ensina {nome(k)} a {p['nome']}")
    fim = feito + nb >= bl
    return f"{o['nome']} ensina {nome(k)} a {p['nome']}: {feito + nb} de {bl} blocos de treino juntos" + (f". {frase}." if fim else '.') + (f' PAROU: {pq}' if pq else '')


def licao(E, pid, k, como):
    """a LIÇÃO (6.5): a primeira vez que o gatilho escrito acontece, nasce no Iniciante (se há vaga): "da cena nasceu uma habilidade"; sobe até o Perito"""
    import estado
    p = E['gente'][pid]; k = H.chave(k) or sys.exit(f'habilidade desconhecida: "{k}"')
    if 'Li' not in H.HABILIDADES[k]['origens']: sys.exit(f"{Nome(k)} não nasce de lição")
    if k not in (p.get('habilidades') or {}) and vagas_usadas(p) >= H.VAGAS: return f"da cena nasceria {nome(k)}, mas {p['nome']} já guarda {H.VAGAS} habilidades: não há vaga"
    x, frase = _origem_nova(p, k, 'licao'); x[1] = pid
    estado.aplica(E, 'habilidade', [x], onde=p['lugar'], quem=[pid], texto=f"da cena nasceu uma habilidade: {nome(k)} ({como})")
    return f"Da cena nasceu uma habilidade: {frase}."


def estuda(E, pid, iid):
    """o LIVRO (6.5): o escrito com a técnica (`tecnica`), 10 blocos de estudo (teto normal) ou 30 (forte); sobe até o Mestre. O CADERNO DO LEGADO (o escrito com `legado`:
    {tecnica, de}, de um mestre morto da crônica): 30 blocos; sobe até o Grão-Mestre (a única porta do apelão fora da classe)."""
    import estado, ato
    p = estado.presente(E, pid, 'estudar'); it = E['itens']['itens'].get(iid) or sys.exit(f'não há o item "{iid}"')
    lg = it.get('legado') if isinstance(it.get('legado'), dict) else None
    if it.get('dono') != pid or it.get('tipo') != 'escrito' or not (it.get('tecnica') or lg): sys.exit(f"{it['nome']} não é um escrito de técnica (nem o caderno de um legado) de {p['nome']}")
    if lg:
        k = lg.get('tecnica'); bl = H.LEGADO_BLOCOS; org = f"legado:{lg.get('de')}"
        if k not in H.HABILIDADES or 'Lg' not in H.HABILIDADES[k]['origens']: sys.exit("o caderno não guarda uma técnica de legado")
    else:
        k = it['tecnica']; org = f'livro:{iid}'
        if k not in H.HABILIDADES or 'Lv' not in H.HABILIDADES[k]['origens']: sys.exit(f"o escrito não ensina uma técnica de livro")
        bl = H.LIVRO_BLOCOS[H.HABILIDADES[k]['teto']]
    x, frase = _origem_nova(p, k, org); x[1] = pid
    m = (p.get('marca') or {}).get('estudo_hab') or {}
    feito = m.get('n', 0) if m.get('item') == iid else 0; vez = min(2, bl - feito)
    def mais(i):
        n_ = feito + i + 1
        return [['pessoa', pid, 'marca.estudo_hab', 'poe', dict(item=iid, n=n_)]] + ([x] if n_ >= bl else [])
    nb, pq = ato.passa(E, pid, vez, 'estudar', esforco='leve', mais=mais, texto=f"{p['nome']} estuda {it['nome']}")
    fim = feito + nb >= bl
    return f"{p['nome']} estuda {it['nome']}: {feito + nb} de {bl} blocos" + (f". {frase}." if fim else '.') + (f' PAROU: {pq}' if pq else '')


def legado_luta(E, S, f, pid):
    """O LEGADO NA LUTA (6.5): a peça de um mestre morto (`legado`: {tecnica, de}) usada numa luta de verdade conta uma luta (marca.legado {ITEM: n}); na 5ª, a técnica nasce
    (do legado: sobe até o Grão-Mestre; o apelão da Roda só nasce assim, ou da classe Lendária). Só na luta do mundo; sem vaga, conta e espera."""
    if not S.get('mundo') or f['estado'] != 'pe' and f['estado'] != 'caido': return []
    p = E['gente'][pid]; usadas = set(S.get('usadas') or []); m = (p.get('marca') or {}).get('legado') or {}; novo = dict(m); ef = []
    for iid, it in E['itens']['itens'].items():
        lg = it.get('legado') if isinstance(it.get('legado'), dict) else None
        if not lg or it.get('dono') != pid or not it.get('uso') or iid not in usadas or it.get('tipo') == 'escrito': continue
        k = lg.get('tecnica')
        if k not in H.HABILIDADES: continue
        n_ = int(m.get(iid, 0)) + 1; novo[iid] = n_
        reg = (p.get('habilidades') or {}).get(k)
        ja = isinstance(reg, dict) and H.ORIGEM_TETO.get(str(reg.get('origem') or '').split(':')[0], 0) >= H.ORIGEM_TETO['legado']      # já a tem por origem igual ou maior: o legado não sobe o teto (e o gravador recusaria a luta)
        if n_ >= H.LEGADO_LUTAS and not ja and (reg is not None or vagas_usadas(p) < H.VAGAS):
            ef.append(['pessoa', pid, 'habilidade', 'aprende', dict(chave=k, origem=f"legado:{lg.get('de')}")])
            S.setdefault('hab_mesa', []).append((pid, f"a peça do mestre ensinou {Nome(k)} a {p['nome']} ({it['nome']}: {n_} lutas de verdade; do legado, sobe até o Grão-Mestre)"))
    return ([['pessoa', pid, 'marca.legado', 'poe', novo]] if novo != m else []) + ef


def esquece(E, pid, k):
    import estado
    p = E['gente'][pid]; k = H.chave(k) or sys.exit(f'habilidade desconhecida: "{k}"')
    if k not in (p.get('habilidades') or {}): sys.exit(f"{p['nome']} não tem {nome(k)}")
    estado.aplica(E, 'habilidade', [['pessoa', pid, 'habilidade', 'esquece', k]], onde=p['lugar'], quem=[pid], texto=f"{p['nome']} esquece {nome(k)} (as marcas se perdem)")
    return f"{p['nome']} esqueceu {nome(k)}: a vaga volta; as marcas se perderam."


# ---------- O TRABALHO (nunca no total: só o prumo, o cheio e o tempo; 6.7, trabalhar) ----------
def _reg(E, pid, k):
    r = (E['gente'][pid].get('habilidades') or {}).get(k); return r if isinstance(r, dict) else None


def olhando(E, pid, lid=None):
    """o BRIO DE OFICINA: um rival ou um mestre de forja com nome, vivo, no lugar da obra"""
    import estado
    lid = lid or E['gente'][pid]['lugar']
    return next((q for k, q in E['gente'].items() if k != pid and isinstance(q, dict) and q.get('estado') == 'vivo' and estado.onde(E, k) == lid
                 and (q.get('rival') or ((q.get('maestria') or {}).get('forja', 0) if isinstance(q.get('maestria'), dict) else 0) >= 6)), None)


def trabalho(E, pid, oficio='forja', lid=None):
    """o que as habilidades de trabalho põem na obra de hoje (a forja e o couro): {prumo, tempera, tempera_so_teto, usou: [(chave, usos)], calor, diz}"""
    import estado
    out = dict(prumo=0, tempera=0, tempera_so_teto=False, usou=[], calor=0, diz='')
    p = E['gente'][pid]; hb = p.get('habilidades') or {}
    if oficio not in ('forja', 'couro') or not hb: return out
    m = p.get('marca') or {}; dia = E['relogio']['dia']; partes = []
    if 'malho_quente' in hb:
        mq = m.get('malho') or {}; cal = mq.get('calor', 0) if mq.get('dia') == dia and mq.get('ate') == estado.agora(E) else 0
        if cal:
            pr = cal // H.MALHO_PRUMO; out['calor'] = cal; out['usou'].append(('malho_quente', cal))
            if pr: out['prumo'] += pr; partes.append(f"o Malho Quente, calor {cal}: prumo {pr}")
    if 'paciencia' in hb:
        gp = grau_de(hb['paciencia']); pr = H.num('paciencia', 'prumo', gp)
        if H.num('paciencia', 'passiva', gp) or m.get('paciencia') == dia:
            out['usou'].append(('paciencia', 1))
            if pr: out['prumo'] += pr; partes.append(f"a Paciência: prumo {pr}")
    if 'brio' in hb:
        q = olhando(E, pid, lid)
        if q: pr = H.num('brio', 'prumo', grau_de(hb['brio'])); out['prumo'] += pr; out['usou'].append(('brio', 1)); partes.append(f"o Brio de Oficina ({q['nome']} olha): prumo {pr}")
    if 'tempera_certa' in hb and m.get('tempera_certa') == dia and hb['tempera_certa'].get('usada') != dia:
        gt = grau_de(hb['tempera_certa']); out['tempera'] = H.num('tempera_certa', 'cheios', gt); out['tempera_so_teto'] = bool(H.num('tempera_certa', 'so_teto', gt))
        out['usou'].append(('tempera_certa', 1)); partes.append(f"a Têmpera Certa: {out['tempera']} cheio(s)" + (' (só no teto)' if out['tempera_so_teto'] else ''))
    out['diz'] = '; '.join(partes)
    return out


def marca_obra(E, pid, h, errar, usou_tempera=False, venceu=False):
    """a marca da obra (a cena que remata): a dureza pela chance de sair abaixo da categoria da obra ou perder; a Têmpera Certa do dia gasta; o calor que fecha com a obra; e o
    feito (6.2: vencer com ela uma cena de dureza 5; o segundo, com um rival ou um mestre de forja com nome olhando, vira notícia)"""
    import estado
    p = E['gente'][pid]; hb = p.get('habilidades') or {}; d = H.dureza(errar); ef = []
    q = olhando(E, pid) if venceu and d >= H.FEITO_DUREZA else None
    for k, usos in h.get('usou') or []:
        if k == 'tempera_certa' and not usou_tempera: continue
        reg = hb.get(k)
        if not isinstance(reg, dict): continue
        mm = marca_cena(d, usos, venceu, k, grau_de(reg))
        if mm: ef.append(['pessoa', pid, f'hab.{k}', 'soma', mm])
        ef += feito(E, pid, k, mm, d, venceu, f"fez com {nome(k)} uma obra de dureza {d}", diante=q['nome'] if q else None, ja=ef)
    if usou_tempera: ef.append(['pessoa', pid, 'hab.tempera_certa', 'usada', E['relogio']['dia']])
    if h.get('calor'): ef.append(['pessoa', pid, 'marca.malho', 'poe', None])
    return ef


def calor(E, pid, oid):
    """o calor do Malho Quente que segue nesta obra (o bloco seguido, no mesmo dia, sem outro ato no meio), ou 0"""
    import estado
    r = _reg(E, pid, 'malho_quente')
    if not r: return 0
    mq = (E['gente'][pid].get('marca') or {}).get('malho') or {}
    return mq.get('calor', 0) if mq.get('obra') == oid and mq.get('dia') == E['relogio']['dia'] and mq.get('ate') == estado.agora(E) else 0


def esquenta(E, pid, oid, calor0, feitos):
    """os blocos seguidos esquentam (até o teto do grau); o preço: +1 de cansaço a cada 2 de calor"""
    import estado
    r = _reg(E, pid, 'malho_quente')
    if not r: return
    cal = min(H.num('malho_quente', 'calor', grau_de(r)), calor0 + feitos); x = cal // H.MALHO_CANSA_A_CADA - calor0 // H.MALHO_CANSA_A_CADA
    ef = [['pessoa', pid, 'marca.malho', 'poe', dict(obra=oid, dia=E['relogio']['dia'], calor=cal, ate=estado.agora(E))]] + ([['pessoa', pid, 'cansaco', 'soma', x]] if x > 0 else [])
    estado.aplica(E, 'forjar', ef, onde=E['gente'][pid]['lugar'], quem=[pid], texto=f"o Malho Quente de {E['gente'][pid]['nome']}: calor {cal}")


def paciencia_hoje(E, pid):
    r = _reg(E, pid, 'paciencia')
    return bool(r) and (bool(H.num('paciencia', 'passiva', grau_de(r))) or (E['gente'][pid].get('marca') or {}).get('paciencia') == E['relogio']['dia'])


def reparo(E, pid):
    r = _reg(E, pid, 'reparo'); return H.num('reparo', 'bloco', grau_de(r)) if r else 0


def ajuste(E, pid):
    r = _reg(E, pid, 'ajuste_fino'); return (H.num('ajuste_fino', 'blocos', grau_de(r)), H.num('ajuste_fino', 'teste', grau_de(r))) if r else (0, 0)


def de_dia(E, pid, k):
    """acende a de dia (a Paciência, a Têmpera Certa): vale nas obras de hoje"""
    import estado
    p = E['gente'][pid]; k = H.chave(k) or sys.exit(f'habilidade desconhecida: "{k}"'); r = _reg(E, pid, k)
    if not r: sys.exit(f"{p['nome']} não tem {nome(k)}")
    if k not in ('paciencia', 'tempera_certa'): sys.exit(f"{Nome(k)} não se acende assim (as de dia de trabalho: a Paciência, a Têmpera Certa)")
    if (p.get('marca') or {}).get(k) == E['relogio']['dia']: sys.exit(f"{Nome(k)} já está acesa hoje")
    if k == 'tempera_certa' and r.get('usada') == E['relogio']['dia']: sys.exit('a Têmpera Certa já foi usada numa obra hoje')
    estado.aplica(E, 'habilidade', [['pessoa', pid, f'marca.{k}', 'poe', E['relogio']['dia']]], onde=p['lugar'], quem=[pid], texto=f"{p['nome']} acende {nome(k)} (vale hoje)")
    return f"{Nome(k)} acesa: vale nas obras de hoje" + (' (uma obra)' if k == 'tempera_certa' else '') + '.'


# ---------- O TRATAR (a pilha do dia: a Mão que Esquenta; o Trato de Campo) ----------
def trato(E, pid):
    r = _reg(E, pid, 'trato')
    return dict(dias=H.num('trato', 'dias', grau_de(r)) if r else 0, grave_treinado=bool(r and H.num('trato', 'grave_treinado', grau_de(r))), dois=bool(r and H.num('trato', 'dois', grau_de(r))))


def esquenta_pilha(E, pid):
    """A MÃO QUE ESQUENTA: os pacientes já tratados hoje, seguidos (um bloco sem tratar quebra), dão +½ dia de repouso por ponto no próximo, até o teto do grau"""
    import estado
    r = _reg(E, pid, 'esquenta'); m = (E['gente'][pid].get('marca') or {}).get('esquenta') or {}
    if not r: return dict(dias=0, n=0)
    n_ = m.get('n', 0) if m.get('dia') == E['relogio']['dia'] and estado.agora(E) - m.get('ate', -9) < 1 else 0      # um bloco sem tratar quebra a pilha
    pil = min(H.num('esquenta', 'pilha', grau_de(r)), n_)
    return dict(dias=H.ESQUENTA_DIAS * pil, n=n_)


def marca_tratar(E, pid, b, esq, tr, marca=True, chaves=('esquenta', 'trato'), pilha=True):
    """o tratamento do dia (a cena): a dureza pela ferida (leve 2, grave 3); a pilha anda (+1 de cansaço a cada 2 tratados); as marcas da Mão que Esquenta e do Trato de Campo
    (e do Ferro em Brasa fora da luta), uma por cena. `marca=False`: o segundo paciente do mesmo bloco (o Trato de Campo do Perito) anda a pilha, sem outra marca."""
    import estado
    p = E['gente'][pid]; hb = p.get('habilidades') or {}; ef = []
    d = H.DUREZA_TRATAR['grave'] if any(f['grave'] for f in b['feridas']) else H.DUREZA_TRATAR['leve']
    if 'esquenta' in hb and pilha:
        n_ = esq['n'] + 1
        ef.append(['pessoa', pid, 'marca.esquenta', 'poe', dict(dia=E['relogio']['dia'], n=n_, ate=estado.agora(E) + 1)])
        if n_ % H.ESQUENTA_CANSA_A_CADA == 0: ef.append(['pessoa', pid, 'cansaco', 'soma', 1])
    for k in (chaves if marca else ()):
        reg = hb.get(k)
        if not isinstance(reg, dict): continue
        cena = (p.get('marca') or {}).get('trata_cena') or {}
        if cena.get('dia') == E['relogio']['dia'] and k in (cena.get('dadas') or {}): continue      # uma marca por cena (o tratamento do dia)
        mm = marca_cena(d, 1, False, k, grau_de(reg))
        if mm: ef.append(['pessoa', pid, f'hab.{k}', 'soma', mm])
    if marca and any(hb.get(k) for k in chaves):
        cena = (p.get('marca') or {}).get('trata_cena') or {}
        dadas = dict(cena.get('dadas') or {}) if cena.get('dia') == E['relogio']['dia'] else {}
        for k in chaves:
            if k in hb: dadas[k] = 1
        ef.append(['pessoa', pid, 'marca.trata_cena', 'poe', dict(dia=E['relogio']['dia'], dadas=dadas)])
    return ef


def ferro(E, pid, paciente):
    """O FERRO EM BRASA FORA DA LUTA (6.7; 1 bloco, com o ferido junto): o ferro quente fecha a ferida: a leve sara com 1 dia de repouso (no Grão-Mestre, também a grave, com 3);
    dói: +1 de cansaço em quem o leva. A cena é a do tratamento do dia (a marca, uma por dia: a ferida leve 2, a grave 3)."""
    import estado, ato, magia_mundo, tabelas_mundo as M
    p = estado.presente(E, pid, 'passar o ferro em brasa'); r = _reg(E, pid, 'ferro_brasa') or sys.exit(f"{p['nome']} não tem o Ferro em Brasa")
    q = magia_mundo._junto(E, pid, paciente); b = E['gente'][q]; gr = grau_de(r)
    alvos = [i for i, x in enumerate(b['feridas']) if not x['grave'] or H.num('ferro_brasa', 'grave', gr)]
    if not alvos: sys.exit(f"{b['nome']} não tem ferida que o ferro feche" + (' (a grave, só o Ferro em Brasa do Grão-Mestre)' if b['feridas'] else ''))
    ef = []
    for i in alvos:
        x = b['feridas'][i]; quer = M.FERIDA_DIAS[1 if x['grave'] else 0] - (H.FERRO_GRAVE_DIAS if x['grave'] else H.FERRO_LEVE_DIAS)
        if x['repouso'] < quer: ef.append(['ferida', q, 'repousa', quer - x['repouso'], i])
    if not ef: sys.exit(f"as feridas de {b['nome']} já saram com {H.FERRO_LEVE_DIAS} dia de repouso: o ferro não as adianta")
    ef.append(['pessoa', q, 'cansaco', 'soma', H.FERRO_CANSA])
    ef += marca_tratar(E, pid, dict(feridas=[b['feridas'][i] for i in alvos]), dict(n=0, dias=0), None, chaves=('ferro_brasa',), pilha=False)
    nb, pq = ato.passa(E, pid, 1, 'cura', esforco='leve', mais=lambda i: ef, com=(q,) if q != pid else (), texto=f"{p['nome']} passa o ferro em brasa nas feridas de {b['nome']}")
    if not nb: sys.exit(f"o ferro não se passou: {pq}")
    sb = sobe(E, pid)
    return (f"{p['nome']} passa o ferro em brasa em {b['nome']}: {len(alvos)} ferida(s) se fecham (a leve sara com {H.FERRO_LEVE_DIAS} dia de repouso"
            + (f"; a grave, com {H.FERRO_GRAVE_DIAS}" if H.num('ferro_brasa', 'grave', gr) else '') + f"); dói: +{H.FERRO_CANSA} de cansaço em {b['nome']}"
            + (f". {'; '.join(sb)}" if sb else '') + (f'. PAROU: {pq}' if pq else '.'))


# ---------- A GENTE DO MUNDO (a função da semente: as habilidades que a mão e a vida explicam) ----------
MAE = {'fio': ('riposta', 'corte_fundo', 'varrida'), 'haste': ('rasteira', 'manter'), 'peso': ('tranco', 'golpe_quebra', 'varrida'), 'tiro': ('mira_firme', 'pe_lebre'),
       'forja': ('malho_quente', 'paciencia', 'reparo', 'brio'), 'couro': ('ajuste_fino', 'reparo'), 'caça': ('pe_lebre', 'picada'), 'coleta': ('picada', 'marcha_longa'),
       'comércio': ('lingua', 'avaliador', 'fio_conversa'), 'cura': ('estanca', 'esquenta', 'trato', 'ferro_brasa'), 'alquimia': ('avaliador',),
       'manha': ('romper_linha',), 'arcano': ('corrente', 'mao_rito', 'mana_curta'), 'fé': ('corrente', 'mao_rito', 'mana_curta'), 'verde': ('corrente', 'mao_rito', 'mana_curta'),
       'pacto': ('corrente', 'mao_rito', 'mana_curta')}      # as listas das mães (8.7), sem as que só a classe dá (fase 4)
LUTA_DE_MESTRE = dict(fio=('sanha', 'trunfos', 'teima', 'bigorna'), haste=('trunfos', 'teima', 'bigorna'), peso=('trunfos', 'sanha', 'bigorna', 'teima'), tiro=('teima',))
GRAU_DA_MAO = {2: 0, 4: 1, 6: 3, 8: 3}      # a mão diz o grau que a vida explica (Treinado, Aprendiz; Mestre e Lendário, Perito)
VIVE_DA_LUTA = ('guarda', 'capitão', 'senhor', 'aventureiro', 'caçador', 'nobre')


def _origem_de(k, pref):
    """a origem que a vida explica para k, entre as que o catálogo deixa, na ordem de preferência"""
    letras = H.letras_origem(k)
    return next((o for o in pref if o in letras), None)


def da_vida(E, pid):
    """AS HABILIDADES QUE A MÃO E A VIDA EXPLICAM (DESENHO 11, fase 2; 8.9 para a classe): função pura da semente e da pessoa. A mão de Treinado ou mais numa família de arma
    explica uma técnica da lista curta dela (do estalo); num ofício ou numa tradição, uma da lista da mãe (da lição ou do livro); quem vive da luta com a mão de Mestre numa arma,
    metade das vezes, uma técnica de mestre. O grau sai da mão (Treinado: Aprendiz; Mestre ou Lendário: Perito), dentro do teto da origem e do talento. Até 6. {chave: (origem, grau)}"""
    import estado, talento
    p = E['gente'][pid]; ma = p.get('maestria') or {}
    if not isinstance(ma, dict) or p.get('jogador'): return {}
    r = estado.sorte_fixa(E, f'habilidades|{pid}'); out = {}
    def poe(k, org, gr):
        if k in out or k in (p.get('habilidades') or {}) or org is None or len(out) + vagas_usadas(p) >= H.VAGAS or H.apelao(k): return
        gr = min(gr, H.ORIGEM_TETO[org], H.TETO_TALENTO.get(talento.grau(p, caminho_hab(p, k)), H.GM))
        while gr > 0 and talento.mao_no(p, caminho_hab(p, k)) < H.MAO_DO_GRAU[gr]: gr -= 1
        out[k] = (org, max(0, gr))
    armas = sorted(((v, f) for f, v in ma.items() if f in H.ESTALO_LISTA and v >= 4), key=lambda x: (-x[0], x[1]))
    for v, fam in armas[:2]:
        cands = [k for k in H.ESTALO_LISTA[fam] if 'E' in H.HABILIDADES[k]['origens']]
        if cands: poe(r.choice(cands), 'estalo', GRAU_DA_MAO[v])
    for of in ('forja', 'couro', 'caça', 'coleta', 'comércio', 'cura', 'alquimia', 'manha') + tuple(T.TRADICOES):
        v = ma.get(of, 0) or 0
        if v >= 4 and MAE.get(of):
            k = r.choice(MAE[of]); poe(k, _origem_de(k, ('licao', 'livro', 'mestre')), GRAU_DA_MAO[v])
    if (p.get('rival') or p.get('papel') in VIVE_DA_LUTA) and armas and armas[0][0] >= 6 and r.random() < 0.5:
        cam = TT.caminho_de(armas[0][1]); k = r.choice(LUTA_DE_MESTRE.get(cam, ('teima',)))
        poe(k, _origem_de(k, ('mestre', 'licao')), 2 if armas[0][0] == 6 else 3)
    return out


def efeitos_da_vida(E, pid):
    """os efeitos que dão a pessoa as habilidades da vida (o gera e a entrada da fase 2)"""
    return [['pessoa', pid, 'habilidade', 'aprende', dict(chave=k, origem=o, grau=gr)] for k, (o, gr) in sorted(da_vida(E, pid).items())]


def entrada(E):
    """(DESENHO 9.5 e 11) a ENTRADA DA FASE 2 no mundo que já existe: os rivais e os nomeados vivos recebem, pela semente, as habilidades que a mão e a vida explicam (o personagem
    não: tudo vem do mundo, em cena)"""
    ef = []
    for pid, p in sorted(E['gente'].items()):
        if isinstance(p, dict) and p.get('estado') == 'vivo' and not p.get('jogador'): ef += efeitos_da_vida(E, pid)
    return ef


# ---------- A MESA: a linha do turno, o SÓ O MESTRE ----------
def _luta_aberta_de(E, pid):
    """o lutador desta pessoa na luta aberta do mundo (a linha da mesa diz o que a luta já gastou), ou None"""
    import estado, json, os
    arq = estado.luta_aberta(E)
    if not arq: return None
    try: S = json.load(open(arq if os.path.isabs(arq) else os.path.join(estado.pasta(), arq), encoding='utf-8'))
    except (OSError, ValueError): return None
    return next((f for f in S.get('L', []) if f.get('id') == pid), None)


def _esta_cena(E, p, k):
    """as marcas que a cena aberta já deu a esta habilidade (a conversa de hoje neste lugar, que segue aberta enquanto o dia não vira): o "esta cena: +N" da linha"""
    fc = (p.get('marca') or {}).get('fala_cena') or {}
    return (fc.get('dadas') or {}).get(k, 0) if fc.get('dia') == E['relogio']['dia'] and fc.get('lugar') == p.get('lugar') else 0


def _linha_hab(E, p, pid, k, reg, fl=None):
    gr = grau_de(reg); prox = min(H.GM, gr + 1); m = reg.get('marcas', 0) if isinstance(reg, dict) else 0
    t = f"**{Nome(k)}** {grau_diz(gr)}"
    if gr < H.GM: t += f", {m} de {pede_marcas(p, k, prox)} marcas"
    h = H.HABILIDADES[k]; mk = p.get('marca') or {}; dia = E['relogio']['dia']; ec = _esta_cena(E, p, k); extra = [f"esta cena: +{ec}"] if ec else []
    if h['ritmo'] == 'dia' and isinstance(reg, dict):
        estado_dia = 'usada hoje' if reg.get('usada') == dia or (fl and k in (fl.get('hab_dia') or [])) else 'acesa hoje' if mk.get(k) == dia else 'pronta'
        t += f" (de dia: {estado_dia}" + ''.join('; ' + x for x in extra) + ')'; extra = []
    elif h['ritmo'] == 'luta':
        gasta = False
        if fl and fl.get('hab'):                            # a luta aberta: a de luta já gasta nela
            if k == 'sanha': gasta = fl.get('sanha_vezes', 0) >= H.num('sanha', 'usos', gr) and fl.get('acesa') != 'sanha'
            elif 'usos' in h['g']: gasta = (fl.get('usos') or {}).get(k, 0) >= H.num(k, 'usos', gr)
            else: gasta = bool((fl.get('usos') or {}).get(k))
            if k == 'trunfos': gasta = bool(fl.get('trunfos')) and fl['trunfos'][0] <= 0
        t += f" (de luta: {'gasta nesta luta' if gasta else 'pronta'}" + ''.join('; ' + x for x in extra) + ')'; extra = []
    if k == 'trunfos':
        q, l = H.num('trunfos', 'dados', gr); tg = mk.get('trunfos'); gastos = tg.get('n', 0) if isinstance(tg, dict) and tg.get('em') == _agora(E) else 0
        if fl and fl.get('trunfos'): gastos = q - fl['trunfos'][0]
        t += f" ({max(0, q - gastos)} de {q} d{l})"
    if k == 'malho_quente':
        mq = mk.get('malho') or {}; calor = mq.get('calor', 0) if mq.get('dia') == dia else 0
        t += f" (calor até {H.num('malho_quente', 'calor', gr)}: prumo {calor // H.MALHO_PRUMO}{' agora' if calor else ''})"
    if k == 'fio_conversa':
        fc = mk.get('fio') or {}; fios = fc.get('n', 0) if fc.get('dia') == dia and fc.get('lugar') == p['lugar'] else 0
        t += f" (fios {fios} de {H.num('fio_conversa', 'fios', gr)}" + ''.join('; ' + x for x in extra) + ')'; extra = []
    if k == 'esquenta':
        mq = mk.get('esquenta') or {}; t += f" (pilha {mq.get('n', 0) if mq.get('dia') == dia else 0} de {H.num('esquenta', 'pilha', gr)})"
    if extra: t += ' (' + '; '.join(extra) + ')'
    fal = falta_para(E, pid, k) if isinstance(reg, dict) else ''
    if fal and not fal[0].isdigit() and fal != 'no topo': t += f" · {fal}"
    return t


def _agora(E):
    import estado
    return estado.agora(E)


def mao(E, pid):
    """A LINHA DAS HABILIDADES (a 🛠️ do turno; a MESA a põe em "Você")"""
    p = E['gente'][pid]; hb = p.get('habilidades') or {}
    if not hb: return f"HABILIDADES (0 de {H.VAGAS} vagas): nenhuma ainda (a primeira nasce em cena: o mestre, a lição, o estalo, o livro, o legado; a classe, na fase 4)"
    fl = _luta_aberta_de(E, pid)
    return f"HABILIDADES ({vagas_usadas(p)} de {H.VAGAS} vagas): " + ' · '.join(_linha_hab(E, p, pid, k, r, fl) for k, r in hb.items() if k in H.HABILIDADES)


def voce(E):
    """o gancho da MESA (turno.py, em "Você"): a linha das habilidades"""
    import estado
    pid = estado.eu(E)
    if not pid or E['gente'][pid]['estado'] != 'vivo': return []
    return [mao(E, pid)]


def so_mestre(E):
    """o SÓ O MESTRE: as marcas da gente do mundo e as habilidades dos rivais (as rolagens ocultas do estalo e da cópia já vão pela lista das ocultas)"""
    out = []
    riv = [(pid, p) for pid, p in E['gente'].items() if isinstance(p, dict) and p.get('estado') == 'vivo' and not p.get('jogador') and p.get('habilidades')]
    if not riv: return out
    com = sorted(riv, key=lambda x: (-max(grau_de(r) for r in x[1]['habilidades'].values()), x[0]))[:8]
    out.append('habilidades da gente do mundo (as mais altas): ' + ' · '.join(f"{p['nome']}: " + ', '.join(f"{nome(k)} {H.CURTO[grau_de(r)]}" + (f" {r.get('marcas', 0)}m" if isinstance(r, dict) else '') for k, r in p['habilidades'].items()) for pid, p in com)
               + f" (ao todo, {len(riv)} pessoas com habilidade)")
    return out


# ---------- ver ----------
def ver(k=None):
    if k is None:
        L_ = [f"AS HABILIDADES ({len(H.HABILIDADES)}), por campo (o grau: {' · '.join(H.GRAUS)}; a força de cada grau: I até o fraco, Ap e Ad até o normal, P e M até o forte, GM até o teto)"]
        for c in H.CAMPOS:
            L_.append(f"{c.upper()}: " + ' · '.join(f"{Nome(x)} [{x}] ({h['teto']})" for x, h in H.HABILIDADES.items() if h['campo'] == c))
        return '\n'.join(L_)
    k2 = H.chave(k) or sys.exit(f'habilidade desconhecida: "{k}" (`habilidade.py ver`)')
    h = H.HABILIDADES[k2]
    L_ = [f"{Nome(k2).upper()} [{k2}] — {h['campo']} · {RITMO_DIZ.get(h['tipo'], h['tipo'])} · {RITMO_DIZ.get(h['ritmo'], h['ritmo'])} · custo: {h['custo']} · caminho: {h['caminho']} · teto: {h['teto']} · origem: {', '.join(H.ORIGEM_DIZ[x] for x in H.letras_origem(k2))}"
          + (f" · arma: {', '.join(h['armas'])}" if h.get('armas') else ''), f"  {h['faz']}"]
    def num_diz(x):
        if isinstance(x, bool): return 'sim' if x else 'não'
        if isinstance(x, tuple) and len(x) == 2 and all(isinstance(y, int) for y in x): return f"{x[0]} de d{x[1]}" if k2 == 'trunfos' else f"{x[0]} custam {x[1]}"
        if isinstance(x, tuple): return f"{round(100 * x[0])}% por {x[1]}"
        if isinstance(x, float): return f"{round(100 * x)}%" if x < 1 else f"{x:g}".replace('.', ',')
        return str(x)
    for c, v in h['g'].items(): L_.append(f"  {c}: " + ' · '.join(f"{H.CURTO[i]} {num_diz(x)}" for i, x in enumerate(v)))
    if h.get('medido'): L_.append('  medido (o contrato): ' + ' · '.join(f"{H.CURTO[i]} {x:+.1f}".replace('.', ',') for i, x in enumerate(h['medido'])) + (' (a HB1 remede pelas regras de P2 e P3)' if h['mede'] == 'remede' else ''))
    if h.get('licao'): L_.append(f"  a lição: {h['licao']}")
    return '\n'.join(L_)


if __name__ == '__main__':
    import signal; hasattr(signal, 'SIGPIPE') and signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    a = sys.argv[1:]
    if not a: print(__doc__); sys.exit()
    if a[0] == 'ver': print(ver(a[1] if len(a) > 1 else None)); sys.exit()
    import estado, ato
    op = dict(x.split('=', 1) for x in a if '=' in x); pos = [x for x in a if '=' not in x]
    E = estado.carrega(); pid = op.get('quem') or estado.eu(E)
    if pid not in E['gente']: sys.exit(f'não há a pessoa "{pid}"')
    if pos[0] == 'mao': print(mao(E, pid)); sys.exit()
    if pos[0] == 'sobe': out = '\n'.join(sobe(E, pid)) or 'nada sobe agora.'
    elif pos[0] == 'esquece' and len(pos) == 2: out = esquece(E, pid, pos[1])
    elif pos[0] == 'copia' and len(pos) == 3 and pos[2] == 'chance' and op.get('de'): print(copia_chance(E, pid, pos[1], op['de'])); sys.exit()
    elif pos[0] == 'copia' and len(pos) == 2 and op.get('de'): out = copia(E, pid, pos[1], op['de'])
    elif pos[0] == 'ensina' and len(pos) == 3: out = ensina(E, pid, pos[1], pos[2], op.get('blocos'))
    elif pos[0] == 'ferro' and len(pos) == 2: out = ferro(E, pid, pos[1])
    elif pos[0] == 'licao' and len(pos) == 3: out = licao(E, pid, pos[1], pos[2])
    elif pos[0] == 'estuda' and len(pos) == 2: out = estuda(E, pid, pos[1])
    elif pos[0] in ('paciencia', 'paciência', 'tempera', 'têmpera') and len(pos) == 1: out = de_dia(E, pid, 'paciencia' if pos[0].startswith('paci') else 'tempera_certa')
    else: print(__doc__); sys.exit()
    estado.grava(E); print(out); print(ato.ultima_linha(E, pid))
