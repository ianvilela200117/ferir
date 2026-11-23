#!/usr/bin/env python3
"""pessoas.py — MOTOR 10: A FICHA DE LUTA SAI SOZINHA do que a pessoa é (atributos, maestria) e do que ela veste (itens.py).

Ninguém digita ataque, Defesa nem dano. Vestiu, a ficha muda.

O REQUISITO é por ATRIBUTO, nunca por nível: a peça pede Força (ou Agilidade) pelo PESO dela.
  Faltou atributo: a peça pesa (−1 no acerto ou na Defesa a cada 5 que faltam; +1 de fôlego a cada 10). A falta conta peça por peça.
  SOB MEDIDA (feita ou ajustada pelo ferreiro para um dono, com o nome gravado): para o dono, pede 10 a menos por grau do
  ferreiro e assenta; na mão de outro, rende uma categoria abaixo.
  SINTONIA: a pessoa sustenta Vontade ÷ 20 peças Épicas ou melhores (as melhores primeiro). As que passam disso rendem uma
  categoria abaixo, e os efeitos delas dormem.

Uso (para olhar): python3 pessoas.py padrao NIVEL [molde=guerreiro|arqueiro|comum] [arma=FAMILIA:CAT] [armadura=MATERIAL:CAT] [escudo=CAT]
"""
import sys
import tabelas as T
from itens import item, cat_i, pede


def padrao(nome, nivel, molde='guerreiro', maestria=None, atributos=None, **mais):
    """uma pessoa GERADA daquele nível: os atributos de nascença do molde mais 1 ponto por nível, repartidos como o molde reparte"""
    if molde not in T.MOLDES: sys.exit(f'molde desconhecido: "{molde}" (use: {", ".join(T.MOLDES)})')
    base, pts = T.MOLDES[molde]
    at = {k: base[k] + int(nivel * pts[k]) for k in T.ATRIBUTOS}
    at.update(atributos or {})
    p = dict(nome=nome, nivel=nivel, atributos=at, maestria=T.maestria_tipica(nivel) if maestria is None else maestria, equip={})
    p.update(mais)
    return p


def veste(p, arma=None, armadura=None, escudo=None, arma2=None, elmo=None, pecas=None):
    """veste a pessoa. Cada peça é um registro do Livro de Itens, ou um atalho para testes e gente miúda:
    arma e arma2 = ('espada', categoria) · armadura = ('malha', categoria): o corpo E um elmo igual (elmo=False tira o elmo)
    · elmo = ('malha', categoria) · escudo = categoria · pecas = mais registros de armadura."""
    arm = []
    if isinstance(armadura, dict): arm.append(armadura)
    elif armadura is not None:
        arm.append(item('armadura', armadura[1], material=armadura[0]))
        if elmo is None: elmo = armadura
    if isinstance(elmo, dict): arm.append(elmo)
    elif elmo: arm.append(item('armadura', elmo[1], material=elmo[0], cobre=['cabeça']))
    arm += list(pecas or [])
    faz = lambda x: x if x is None or isinstance(x, dict) else item('arma', x[1], familia=x[0])
    p['equip'] = dict(arma=faz(arma), arma2=faz(arma2), escudo=escudo if escudo is None or isinstance(escudo, dict) else item('escudo', escudo), armaduras=arm)
    return p


def _maestria(p, familia):
    """a maestria da pessoa NESTA arma: um número só (gente gerada) ou um por família de arma (gente do mundo)"""
    m = p['maestria']
    return m.get(familia, 0) if isinstance(m, dict) else m


def _assenta(it, p, dorme):
    """(a categoria que a peça rende, o que falta de atributo, o bônus de assento) para ESTA pessoa"""
    a, q = pede(it, dorme); c = it['cat'] - (T.SINTONIA_ABAIXO if dorme else 0); mais = 0
    sm = it.get('sob_medida')
    if sm:
        if sm['dono'] == p['nome']: q -= T.SOB_MEDIDA * sm.get('grau', 1); mais = 1
        else: c -= T.NAO_E_DELE
    return max(0, c), max(0, q - p['atributos'][a]), mais


def _efeitos(it, dorme):
    return {} if dorme or it['dur'][0] <= 0 else {e['chave']: e.get('valor', True) for e in it.get('efeitos', [])}


def _arma(it, p, dorme):
    f = T.FAMILIAS[it['familia']]; c, falta, mais = _assenta(it, p, dorme); at = p['atributos']; tiro = bool(f.get('distancia'))
    quebrada = it['dur'][0] <= 0
    if quebrada: c = 0
    return dict(nome=it['nome'] + (' (quebrada)' if quebrada else ''), cat=c, dado=f['dado'], golpe=f['golpe'], alcance=f['alcance'], distancia=tiro, maos=f['maos'],
                recarga=f.get('recarga', 0), haste=f['alcance'] == 2 and not tiro,
                mult=T.MULT[c] * (T.DUAS_MAOS if f['maos'] == 2 and not tiro else 1),
                acerto=T.acerto_base(_maestria(p, it['familia']), at['Força'], at['Agilidade']) + T.BON[c] + mais - falta // T.FALTA_ACERTO + (T.QUEBRADA if quebrada else 0) + p.get('pena', 0),
                aparo=0 if tiro or quebrada else T.BON[c] + f.get('apara', 0),
                folego=1 + (1 if f['peso'] == 'pesada' else 0) + falta // T.FALTA_FOLEGO,
                fmult=T.BESTA_FORCA if it['familia'] == 'besta' else T.forca_mult(at[f.get('atributo', 'Força')]),
                efeitos=_efeitos(it, dorme), item=it)


def ficha(p):
    """a ficha de luta desta pessoa, hoje, com o que ela veste"""
    at = p['atributos']; eq = p.get('equip') or {}; m = _maestria(p, (eq.get('arma') or {}).get('familia', 'punho'))
    arm = [x for x in eq.get('armaduras') or [] if x]
    todas = [x for x in (eq.get('arma'), eq.get('arma2'), eq.get('escudo')) if x] + arm
    # SINTONIA: as peças Épicas ou melhores, da melhor para a pior; as que passam do limite dormem
    altas = sorted([it for it in todas if it['cat'] >= T.SINTONIA_DESDE], key=lambda i: -i['cat'])
    limite = max(1, at['Vontade'] // T.SINTONIA)
    sono = {id(it) for it in altas[limite:]}; dorme = lambda it: id(it) in sono
    F = dict(nome=p['nome'], nivel=p['nivel'], maestria=m, pvmax=T.pv_max(at['Vigor'], p['nivel']), folmax=max(T.FOLEGO_MIN, T.folego_max(at['Vigor']) - p.get('fol_menos', 0)),
             esforcos=T.esforcos(m), reacoes=T.reacoes(m), vontade_b=at['Vontade'] // 10, percep_b=at['Percepção'] // 10, agil_b=at['Agilidade'] // 10,
             forca_b=at['Força'] // 10, dormem=[it['nome'] for it in altas[limite:]])
    F['pv'] = p.get('pv', F['pvmax']); F['fol'] = F['folmax']
    punho = item('arma', 0, 'as mãos', familia='punho', efeitos=[dict(chave='nao_quebra')])
    F['arma'] = _arma(eq.get('arma') or punho, p, dorme(eq['arma']) if eq.get('arma') else False)
    F['arma2'] = _arma(eq['arma2'], p, dorme(eq['arma2'])) if eq.get('arma2') else None
    F['punho'] = _arma(punho, p, False)
    # a armadura, parte por parte (a melhor peça que cobre a parte)
    F['partes'] = {}; falta_arm = 0; fol_arm = 0; F['fontes'] = []; corpo = T.SEM_ARMADURA
    for it in arm:
        c, falta, mais = _assenta(it, p, dorme(it)); mat = T.MATERIAIS[it['material']]
        falta_arm += falta; fol_arm = max(fol_arm, mat['folego'])
        F['fontes'].append(dict(item=it, efeitos=_efeitos(it, dorme(it))))
        if 'tronco' in it['cobre']: corpo = mat
        for parte in it['cobre']:
            prot = T.RD[c] * mat['rd'] * (T.SOB_MEDIDA_PROT if mais else 1)
            if parte not in F['partes'] or prot > F['partes'][parte]['rd']:
                F['partes'][parte] = dict(nome=it['nome'], cat=c, material=it['material'], rd=prot, item=it)
    F['nuas'] = [x for x in T.PARTES if x not in F['partes']]
    F['def_fixa'] = T.defesa_base(m, at['Agilidade']) + corpo['defesa'] - falta_arm // T.FALTA_ACERTO + p.get('pena', 0)      # a pena do corpo (fome, sono, cansaço)
    F['feridas0'] = [list(x) for x in p.get('feridas', [])]                                                             # as feridas que a pessoa já traz
    F['escudo'] = None; esc = eq.get('escudo')
    if esc:
        c, falta, mais = _assenta(esc, p, dorme(esc)); falta_arm += falta
        F['escudo'] = dict(nome=esc['nome'], cat=c, bonus=T.ESCUDO_BASE + T.BON[c] + mais - falta // T.FALTA_ACERTO, item=esc)
        F['fontes'].append(dict(item=esc, efeitos=_efeitos(esc, dorme(esc))))
    F['fol_rodada'] = fol_arm + falta_arm // T.FALTA_FOLEGO; F['ini_mod'] = corpo['ini']
    for k in ('id', 'lado', 'papel', 'moral', 'lider', 'guarda', 'controla', 'linha'):
        if k in p: F[k] = p[k]
    return F


def defesa(F, w=None, escudo_inteiro=True):
    """a Defesa com a arma w na mão: a fixa, mais o que apara melhor: o escudo (arma de uma mão e escudo inteiro) ou a própria arma"""
    w = w or F['arma']
    esc = F['escudo']['bonus'] if F['escudo'] and w['maos'] == 1 and escudo_inteiro else 0
    return F['def_fixa'] + max(esc, w['aparo'])


def linha(F):
    """a ficha em três linhas, para a mesa"""
    w = F['arma']; ps = ' · '.join(f"{k} {v['rd']:g}" for k, v in F['partes'].items()) or 'sem armadura'
    ext = ' + '.join('1' if x == 1 else '1 pelo dobro do fôlego' for x in F['esforcos'])
    return (f"{F['nome']} (nível {F['nivel']}, {T.MAESTRIAS.get(F['maestria'], F['maestria'])}) · PV {F['pv']}/{F['pvmax']} · fôlego {F['folmax']} · {T.ACOES} ações (a mais: {ext})\n"
            f"  {w['nome']}: acerto +{w['acerto']:g} · {w['dado']} × {w['mult']:g} ({w['golpe']}), força × {w['fmult']:.2f} · {w['folego']} de fôlego por golpe"
            + (f", mais {F['fol_rodada']} por rodada da armadura" if F['fol_rodada'] else '') + '\n'
            f"  Defesa {defesa(F):g}" + (f" (com {F['escudo']['nome']})" if F['escudo'] and w['maos'] == 1 else '') + f" · proteção: {ps}"
            + (f" · SEM PROTEÇÃO: {', '.join(F['nuas'])}" if F['nuas'] and F['partes'] else '') + (f" · DORMEM: {', '.join(F['dormem'])}" if F['dormem'] else ''))


if __name__ == '__main__':
    a = sys.argv[1:]
    if len(a) < 2 or a[0] != 'padrao': sys.exit(__doc__)
    op = dict(x.split('=', 1) for x in a[2:])
    par = lambda s: (s.split(':')[0], cat_i(s.split(':')[1]))
    p = veste(padrao('exemplo', int(a[1]), molde=op.get('molde', 'guerreiro')), arma=par(op['arma']) if 'arma' in op else None,
              armadura=par(op['armadura']) if 'armadura' in op else None, escudo=cat_i(op['escudo']) if 'escudo' in op else None)
    print(linha(ficha(p)))
