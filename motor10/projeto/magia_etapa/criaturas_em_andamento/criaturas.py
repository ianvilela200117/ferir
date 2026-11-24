"""criaturas.py — RASCUNHO da parte J: a ficha das criaturas novas, por cima do pessoas.py e do bichos.py de hoje (a cópia em base/).

  povo(linha)            a pessoa pronta para a luta, de uma linha do TROPA (gente com corpo de monstro: veste arma, armadura e escudo)
  bando_povo(linha, n)   n deles, com nome cada um
  ficha_j(p)             a ficha de luta: a de gente ou a de bicho (pessoas.ficha), mais o que é novo (o corpo do povo, os traços novos, as artes do chefe)
"""
import os, sys, random
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, 'base'))
import tabelas as T
import tabelas_bichos as TB
import pessoas, bichos
from itens import item
import tabelas_criaturas as TC


def _tosca(it):
    """a peça da tropa: o atalho de gente miúda (vale a categoria na luta e não tem registro no Livro)"""
    d = max(2, int(it['dur'][1] * TC.TOSCA_DUR)); it['dur'] = [d, d]; it['tosca'] = True
    return it


def povo(que, nome=None, arma=None, armadura=None, escudo=None, **mais):
    """a pessoa de uma linha do TROPA. arma / armadura / escudo: um registro do Livro (a peça do chefe), no lugar da peça de atalho da linha.
    mais: o que muda na pessoa (nivel, maestria, lider, guarda, linha, moral, atributos...)."""
    L = TC.TROPA[que]; P = TC.POVOS[L['povo']]; c = mais.pop('cat', L['cat']); nivel = mais.pop('nivel', L['nivel'])       # cat: o mesmo povo com o conjunto de outra categoria (o posto)
    at = {k: P['base'][k] + int(nivel * P['pts'][k]) for k in T.ATRIBUTOS}; at.update(mais.pop('atributos', None) or {})
    p = dict(nome=nome or f"{P['artigo']} {L['nome']}", nivel=nivel, atributos=at, maestria=mais.pop('maestria', L['maestria']), equip={},
             povo=dict(especie=que, povo=L['povo'], tamanho=P['tamanho'], tracos=list(P['tracos']), coragem=P['coragem'], couro=P.get('couro'), cat=c))
    def faz_arma(x): return None if x is None else _tosca(item('arma', min(7, c + x[1]), familia=x[0]))
    arm = []
    if isinstance(armadura, dict): arm.append(armadura)
    elif L['armadura']:
        mat, elmo = L['armadura']; arm.append(_tosca(item('armadura', c, material=mat)))
        if elmo: arm.append(_tosca(item('armadura', c, material=mat, cobre=['cabeça'])))
    p['equip'] = dict(arma=arma if isinstance(arma, dict) else faz_arma(L['arma']), arma2=faz_arma(L['arma2']),
                      escudo=escudo if isinstance(escudo, dict) else (_tosca(item('escudo', c)) if L['escudo'] else None), armaduras=arm)
    if L.get('lider'): p['lider'] = True
    p.update(mais)
    return p


def bando_povo(que, n=None, sorte=None, primeiro=1, **mais):
    L = TC.TROPA[que]; lo, hi = L['bando']
    if n is None: n = lo if lo == hi else (sorte or random).randint(lo, hi)
    if n == 1 and primeiro == 1: return [povo(que, **mais)]
    return [povo(que, nome=f"{L['nome']} {i + primeiro}", **mais) for i in range(n)]


def _ficha_povo(p):
    """a ficha de gente (o que veste decide), com o corpo do povo por cima: o tamanho, os traços, a coragem e a pele"""
    b = p['povo']; q = {k: v for k, v in p.items() if k != 'povo'}; F = pessoas.ficha(q); tam = TB.TAMANHOS[b['tamanho']]
    F['pvmax'] = int(F['pvmax'] * tam['pv']); F['pv'] = min(p.get('pv', F['pvmax']), F['pvmax']); F['def_fixa'] += tam['defesa']
    F.update(povo=b['especie'], tamanho=b['tamanho'], ocupa=tam['ocupa'], cerco=list(tam['cerco']), tracos=list(b['tracos']), coragem=b.get('coragem', 0))
    for w in (F['arma'], F['arma2'], F['punho']):
        if w and not w['distancia']: w['alcance'] = max(w['alcance'], tam['alcance'])       # a arma na mão de quem é grande alcança o que o braço alcança
    if b.get('couro'):                                      # a pele que vale como armadura onde a peça não cobre (a escama do homem-lagarto)
        como = TB.COUROS[b['couro']]; mat = T.MATERIAIS[como]; c = b['cat']
        corpo = dict(tipo='corpo', cat=c, nome=f"o corpo de {p['nome']}", dur=[1, 1], efeitos=[dict(chave='nao_quebra')])
        for parte in T.PARTES:
            if parte not in F['partes'] or F['partes'][parte]['rd'] < T.RD[c] * mat['rd']:
                F['partes'][parte] = dict(nome=f"{b['couro']} {T.CATS[c]}", cat=c, material=como, rd=T.RD[c] * mat['rd'], item=corpo)
        F['nuas'] = [x for x in T.PARTES if x not in F['partes']]; F['fontes'].append(dict(item=corpo, efeitos={'nao_quebra': True}))
        if not any('tronco' in (x.get('cobre') or []) for x in (p.get('equip') or {}).get('armaduras') or []):
            F['def_fixa'] += mat['defesa'] - T.SEM_ARMADURA['defesa']; F['ini_mod'] = mat['ini']
    return F


def ficha_j(p):
    """a ficha de luta de qualquer um: gente, bicho, povo. Põe o que é novo: os traços novos e as artes do chefe (pela conta da magia)"""
    if isinstance(p.get('bicho'), str): p = bichos.bicho(p['bicho'], **{k: v for k, v in p.items() if k not in ('bicho', 'nivel')})       # o atalho do cenário
    F = _ficha_povo(p) if p.get('povo') else pessoas.ficha(p)
    at = p['atributos']; F.setdefault('tracos', []); F.setdefault('tamanho', 'médio')
    e = TB.ESPECIES.get(F.get('bicho') or '', {}); mais = dict(e.get('mais') or {}); mais.update(p.get('mais') or {})
    cat = (p.get('bicho') or {}).get('cat') if isinstance(p.get('bicho'), dict) else None
    if cat is None: cat = (p.get('povo') or {}).get('cat', F['arma']['cat'])
    F['aco'] = TC.PEDE_PRATA if ('imaterial' in F['tracos'] or 'pede prata' in F['tracos']) else 0
    if F.get('bicho'):
        for w in F['armas_corpo'] + [F['arma'], F['punho']]:
            if w['golpe'] in TC.CRUS: w['cru'] = True
            if 'ardente' in F['tracos']: w['efeitos'] = dict(w['efeitos'], sangra=True)
        if 'ardente' in F['tracos']: F['fontes'][0]['efeitos'] = dict(F['fontes'][0]['efeitos'], devolve=TC.ardente(cat))
        if 'atira' in F['tracos']:
            t = dict(TC.ATIRA_PADRAO, **(mais.get('tiro') or {})); base = F['armas_corpo'][0]
            F['tiro'] = dict(base, nome=f"{t['nome']} {T.CATS[cat]}", dado=t['dado'], golpe=t['golpe'], alcance=t['alcance'], distancia=True, folego=t['folego'], aparo=0, corpo=True, efeitos={'nao_quebra': True})
    # quem lança: as artes, as fases, a Mana, a Conjuração e a Firmeza (as fórmulas são as da conta da magia, B.1 a B.3)
    artes = p.get('artes') if p.get('artes') is not None else mais.get('artes')
    foco = p.get('foco', cat); m = F['maestria']; af, vo = at['Afinidade'], at['Vontade']; trad = p.get('tradicao', 'Afinidade')
    F['conj'] = TC.conj(p.get('mao_magia', m), at[trad], foco) + (0 if artes is None or p.get('foco') is not None or F.get('bicho') else -4)       # sem foco: como foco Comum com −4 (o bicho lança pelo corpo)
    tr = F['partes'].get('tronco'); F['amuleto'] = p.get('amuleto')
    F['firmeza'] = TC.firmeza(vo, m, F['amuleto'], tr['cat'] if tr else None, inteiro='resiste' in F['tracos'])
    F['mana'] = F['manamax'] = TC.mana_max(af, vo, p.get('mao_magia', m)) if artes else 0
    F['artes'] = [dict(a) for a in artes or []]; F['fases'] = [dict(x) for x in p.get('fases') or []]
    for k in ('desfaz', 'fica', 'chefe'):
        if k in p: F[k] = p[k]
    corpo = dict(tipo='corpo', cat=foco, nome=f"a arte de {p['nome']}", dur=[1, 1], efeitos=[dict(chave='nao_quebra')]); F['arma_arte'] = {}
    for a in F['artes']:
        if a['tipo'] == 'ataque':
            F['arma_arte'][a['nome']] = dict(nome=a['nome'], cat=foco, dado=a['dado'], golpe='magia', alcance=a.get('alcance', 6), distancia=True, maos=1, recarga=0, haste=False,
                                             mult=T.MULT[foco] * (1.25 if p.get('cajado') else 1), acerto=F['conj'], aparo=0, folego=0, fmult=1 + (at[trad] // 10) * 0.03, efeitos={'nao_quebra': True},
                                             area=bool(a.get('area')), magia=True, item=corpo)
    return F


def faz(que, nome=None, **mais):
    """uma criatura pelo nome da tabela: de corpo (TC.CORPOS, ou as 14 de hoje) ou de povo (TC.TROPA)"""
    if que in TC.TROPA: return povo(que, nome=nome, **mais)
    return bichos.bicho(que, nome=nome, **mais)


def faz_bando(que, n=None, sorte=None, **mais):
    if que in TC.TROPA: return bando_povo(que, n=n, sorte=sorte, **mais)
    return bichos.bando(que, sorte, n=n, **mais)
