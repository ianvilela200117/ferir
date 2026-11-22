#!/usr/bin/env python3
"""pessoas.py — MOTOR 10: A FICHA DE LUTA SAI SOZINHA do que a pessoa é (atributos, maestria) e do que ela veste (itens.py).

Ninguém digita ataque, Defesa nem dano. Vestiu, a ficha muda.

O REQUISITO é por ATRIBUTO, nunca por nível: a peça pede Força (ou Agilidade) pelo PESO dela.
  Faltou atributo: a peça pesa (−1 no acerto ou na Defesa a cada 5 que faltam; +1 de fôlego a cada 10).
  SOB MEDIDA (feita ou ajustada pelo ferreiro para um dono, com o nome gravado): para o dono, pede 10 a menos por grau do
  ferreiro e assenta (+1); na mão de outro, rende uma categoria abaixo.
  SINTONIA: a pessoa sustenta Vontade ÷ 20 peças Épicas ou melhores com efeito desperto. As que passam disso dormem
  (os números da categoria seguem valendo; os efeitos, não).

Uso (para olhar): python3 pessoas.py padrao NIVEL [arma=FAMILIA:CAT] [armadura=MATERIAL:CAT] [escudo=CAT]
"""
import sys
import tabelas as T
from itens import item, cat_i, pede, tem

BASE = {'Força': 85, 'Agilidade': 70, 'Vigor': 75, 'Vontade': 55, 'Percepção': 55, 'Afinidade': 45}
PONTOS = {'Força': 0.30, 'Agilidade': 0.20, 'Vigor': 0.25, 'Vontade': 0.10, 'Percepção': 0.10, 'Afinidade': 0.05}   # 1 ponto por nível


def maestria_tipica(nivel):
    """a maestria que um combatente costuma ter naquele nível (para gerar gente; não é regra de quem joga)"""
    return 0 if nivel < 10 else 2 if nivel < 25 else 4 if nivel < 50 else 6 if nivel < 150 else 8


def padrao(nome, nivel, maestria=None, atributos=None, **mais):
    """um combatente comum daquele nível: os pontos do nível repartidos como um guerreiro reparte"""
    at = {k: BASE[k] + int(nivel * PONTOS[k]) for k in T.ATRIBUTOS}
    at.update(atributos or {})
    p = dict(nome=nome, nivel=nivel, atributos=at, maestria=maestria_tipica(nivel) if maestria is None else maestria, equip={})
    p.update(mais)
    return p


def veste(p, arma=None, armadura=None, escudo=None, arma2=None):
    """veste um conjunto simples: arma=('espada', cat) · armadura=('malha', cat) (corpo e elmo) · escudo=cat. Também aceita o registro do item."""
    def faz(x, tipo):
        if x is None or isinstance(x, dict): return x
        if tipo == 'arma': return item('arma', x[1], familia=x[0])
        return item('escudo', x)
    p['equip'] = {}
    if arma is not None: p['equip']['arma'] = faz(arma, 'arma')
    if arma2 is not None: p['equip']['arma2'] = faz(arma2, 'arma')
    if escudo is not None: p['equip']['escudo'] = faz(escudo, 'escudo')
    if armadura is not None:
        if isinstance(armadura, dict): p['equip']['corpo'] = armadura
        else:
            p['equip']['corpo'] = item('armadura', armadura[1], material=armadura[0])
            p['equip']['elmo'] = item('armadura', armadura[1], material=armadura[0], cobre=['cabeça'])
    return p


def _assenta(it, p):
    """(categoria que a peça rende, o que falta de atributo, bônus de assento) para ESTA pessoa"""
    a, q = pede(it); c = it['cat']; mais = 0
    sm = it.get('sob_medida')
    if sm:
        if sm['dono'] == p['nome']: q -= T.SOB_MEDIDA * sm.get('grau', 1); mais = 1
        else: c = max(0, c - T.NAO_E_DELE)
    return c, max(0, q - p['atributos'][a]), mais


def _arma(it, p, sem_fol=0):
    f = T.FAMILIAS[it['familia']]; c, falta, mais = _assenta(it, p); at = p['atributos']
    if it['dur'][0] <= 0: c = 0   # quebrada: vale como um pedaço de ferro Comum
    atrib = f.get('atributo', 'Força')
    fm = 1.2 if it['familia'] == 'besta' else T.forca_mult(at[atrib])
    return dict(nome=it['nome'], cat=c, dado=f['dado'], mult=T.MULT[c] * (T.DUAS_MAOS if f['maos'] == 2 else 1), golpe=f['golpe'], alcance=f['alcance'],
                distancia=bool(f.get('distancia')), maos=f['maos'], recarga=f.get('recarga', 0),
                acerto=T.acerto_base(p['maestria'], at['Força'], at['Agilidade']) + T.BON[c] + mais - falta // T.FALTA_ACERTO - (4 if it['dur'][0] <= 0 else 0),
                folego=1 + (1 if f['peso'] == 'pesada' else 0) + falta // T.FALTA_FOLEGO, fmult=fm, item=it)


def ficha(p):
    """a ficha de luta desta pessoa, hoje, com o que ela veste"""
    at = p['atributos']; eq = p.get('equip', {}); m = p['maestria']
    punho = item('arma', 0, 'as mãos', familia='punho')
    # SINTONIA: as peças Épicas+ com efeito, da melhor para a pior; as que passam do limite dormem
    com_efeito = sorted([it for it in eq.values() if it and it['cat'] >= T.SINTONIA_DESDE and it.get('efeitos')], key=lambda i: -i['cat'])
    limite = max(1, at['Vontade'] // T.SINTONIA)
    dormem = {id(it) for it in com_efeito[limite:]}
    desperto = lambda it: id(it) not in dormem and it['dur'][0] > 0
    F = dict(nome=p['nome'], nivel=p['nivel'], maestria=m, pvmax=T.pv_max(at['Vigor'], p['nivel']), folmax=T.folego_max(at['Vigor']),
             acoes=T.acoes(m), reacoes=T.reacoes(m), vontade_b=at['Vontade'] // 10, percep_b=at['Percepção'] // 10, agil_b=at['Agilidade'] // 10,
             forca_b=at['Força'] // 10, dormem=[it['nome'] for it in com_efeito[limite:]])
    F['pv'] = p.get('pv', F['pvmax']); F['fol'] = F['folmax']
    F['arma'] = _arma(eq.get('arma') or punho, p)
    F['arma2'] = _arma(eq['arma2'], p) if eq.get('arma2') else None
    for w in (F['arma'], F['arma2']):
        if w: w['efeitos'] = {e['chave']: e.get('valor', True) for e in w['item'].get('efeitos', [])} if desperto(w['item']) else {}
    # a armadura, parte por parte (a melhor peça que cobre a parte)
    F['partes'] = {}; falta_arm = 0; fol_arm = 0; efeitos = {}
    for it in eq.values():
        if not it or it['tipo'] != 'armadura': continue
        c, falta, mais = _assenta(it, p); mat = T.MATERIAIS[it['material']]
        falta_arm += falta; fol_arm = max(fol_arm, mat['folego'])
        if desperto(it): efeitos.update({e['chave']: e.get('valor', True) for e in it.get('efeitos', [])})
        for parte in it['cobre']:
            rd = T.RD[c] * mat['rd'] * (1.1 if mais else 1)
            if parte not in F['partes'] or rd > F['partes'][parte]['rd']:
                F['partes'][parte] = dict(nome=it['nome'], cat=c, material=it['material'], rd=rd, item=it)
    df = T.defesa_base(m, at['Agilidade']) - falta_arm // T.FALTA_ACERTO
    esc = eq.get('escudo'); F['escudo'] = None
    if esc and F['arma']['maos'] == 1 and esc['dur'][0] > 0:
        c, falta, mais = _assenta(esc, p); df += T.BON[c] + mais - falta // T.FALTA_ACERTO; falta_arm += falta
        F['escudo'] = dict(nome=esc['nome'], cat=c, item=esc)
        if desperto(esc): efeitos.update({e['chave']: e.get('valor', True) for e in esc.get('efeitos', [])})
    elif not F['arma']['distancia']:
        df += T.BON[F['arma']['cat']] / 2     # apara com a arma
    F['defesa'] = df; F['fol_rodada'] = fol_arm + falta_arm // T.FALTA_FOLEGO; F['efeitos'] = efeitos
    for k in ('lado', 'papel', 'moral', 'lider', 'guarda', 'controla', 'linha'):
        if k in p: F[k] = p[k]
    return F


def linha(F):
    """a ficha em três linhas, para a mesa"""
    w = F['arma']; ps = ' · '.join(f"{k} {v['rd']:g}" for k, v in F['partes'].items()) or 'sem armadura'
    return (f"{F['nome']} (nível {F['nivel']}, {T.MAESTRIAS.get(F['maestria'], F['maestria'])}) · PV {F['pv']}/{F['pvmax']} · fôlego {F['folmax']} · {F['acoes']} ações\n"
            f"  {w['nome']}: acerto +{w['acerto']:g} · {w['dado']} × {w['mult']:g} ({w['golpe']}), força × {w['fmult']:.2f} · {w['folego']} de fôlego por golpe\n"
            f"  Defesa {F['defesa']:g}" + (f" (com {F['escudo']['nome']})" if F['escudo'] else '') + f" · proteção: {ps}" + (f" · DORMEM: {', '.join(F['dormem'])}" if F['dormem'] else ''))


if __name__ == '__main__':
    a = sys.argv[1:]
    if len(a) < 2 or a[0] != 'padrao': sys.exit(__doc__)
    op = dict(x.split('=', 1) for x in a[2:])
    par = lambda s: (s.split(':')[0], cat_i(s.split(':')[1]))
    p = veste(padrao('exemplo', int(a[1])), arma=par(op['arma']) if 'arma' in op else None, armadura=par(op['armadura']) if 'armadura' in op else None,
              escudo=cat_i(op['escudo']) if 'escudo' in op else None)
    print(linha(ficha(p)))
