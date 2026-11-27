#!/usr/bin/env python3
"""pessoas.py — MOTOR 10: A FICHA DE LUTA SAI SOZINHA do que a pessoa é (atributos, maestria) e do que ela veste (itens.py).

Ninguém digita ataque, Defesa nem dano. Vestiu, a ficha muda.

O REQUISITO é por ATRIBUTO, nunca por nível: a peça pede Força (ou Agilidade) pelo PESO dela.
  Faltou atributo: a peça pesa (−1 no acerto ou na Defesa a cada 5 que faltam; +1 de fôlego a cada 10). A falta conta peça por peça.
  SOB MEDIDA (feita ou ajustada pelo ferreiro para um dono, com o nome gravado): para o dono, pede 10 a menos por grau do
  ferreiro e assenta; na mão de outro, rende uma categoria abaixo. O dono é reconhecido pelo id da pessoa, quando a peça o guarda; senão, pelo nome.
  SINTONIA: a pessoa sustenta Vontade ÷ 20 peças Épicas ou melhores (as melhores primeiro). As que passam disso rendem uma
  categoria abaixo, e os efeitos delas dormem.

  O BICHO (bichos.py) tem a mesma ficha: o corpo dele é a arma e a armadura, com categoria. O corpo não é peça: não está no
  Livro de Itens, não quebra, não tem dono e não ocupa sintonia. O tamanho mexe no PV, no alcance, no cerco, no corredor e na Defesa.
  DA ETAPA DA MAGIA (o contrato: projeto/ETAPA_MAGIA.md, seção 10):
  O DOM de uma mão de arma soma no acerto com as armas dela, e metade na Defesa (a ação e a reação a mais não: são da maestria).
  O POVO (goblin, orc, ogro...) é gente: veste peças de verdade, e o campo `povo` põe por cima o tamanho, os traços, a coragem e a pele (o couro onde a peça não cobre).
  O POVO DO PERSONAGEM (etapa 4b: anão, elfo...) não é esse campo: o estado.lutador traz só os traços (tabelas.TRACOS_POVO) e a coragem dele, e a ficha os leva.
  A MANHA (etapa 4b): a ficha leva a mão de manha (`manha`), para o golpe pelas costas da luta.
  A ficha já traz, com valor neutro, os campos da magia (feitiços, Mana, tradição, foco, amuleto, dom, Firmeza, traços, fases, poções): a luta de magia os usa.
  A MAGIA NA LUTA (capítulo 11; os números no tabelas_magia.py): o FOCO e o AMULETO se vestem (veste(..., foco=('cajado', 2), amuleto=2)) e entram na sintonia, como toda
  peça Épica ou melhor; a PEÇA ENCANTADA (arma, armadura ou escudo com encanto) ocupa sintonia de qualquer categoria, e a que dorme não solta o encanto.
  As mãos do foco: a varinha, o símbolo e o talismã vão na mão do escudo (lança-se de arma e escudo). O CAJADO pede as duas mãos: é a arma (bate como maça leve,
  1d6 de impacto, com a mão de maça, e apara com o bônus da categoria); a arma de antes fica de reserva (a segunda arma) e o escudo não entra.
  A Firmeza na ficha: a base comum, com o melhor entre o bônus do amuleto e metade do da armadura do tronco (com o traço "resiste", o da armadura inteiro).

Uso (para olhar): python3 pessoas.py padrao NIVEL [molde=guerreiro|arqueiro|comum] [arma=FAMILIA:CAT] [armadura=MATERIAL:CAT] [escudo=CAT]
"""
import sys
import tabelas as T
import tabelas_talento as TT
import tabelas_magia as TM
import tabelas_efeitos as TE
from itens import item, cat_i, pede


def padrao(nome, nivel, molde='guerreiro', maestria=None, atributos=None, **mais):
    """uma pessoa GERADA daquele nível: os atributos de nascença do molde mais 1 ponto por nível, repartidos como o molde reparte"""
    molde = 'clérigo' if molde == 'clerigo' else molde
    if molde not in T.MOLDES and molde not in TM.MOLDES: sys.exit(f'molde desconhecido: "{molde}" (use: {", ".join(list(T.MOLDES) + list(TM.MOLDES))})')
    base, pts = T.MOLDES[molde] if molde in T.MOLDES else TM.MOLDES[molde]      # os de quem lança (mago, clérigo, druida, bruxa) moram na página da magia
    at = {k: base[k] + int(nivel * pts[k]) for k in T.ATRIBUTOS}
    at.update(atributos or {})
    p = dict(nome=nome, nivel=nivel, atributos=at, maestria=T.maestria_tipica(nivel) if maestria is None else maestria, equip={})
    p.update(mais)
    return p


def veste(p, arma=None, armadura=None, escudo=None, arma2=None, elmo=None, pecas=None, foco=None, amuleto=None):
    """veste a pessoa. Cada peça é um registro do Livro de Itens, ou um atalho para testes e gente miúda:
    arma e arma2 = ('espada', categoria) · armadura = ('malha', categoria): o corpo E um elmo igual (elmo=False tira o elmo)
    · elmo = ('malha', categoria) · escudo = categoria · pecas = mais registros de armadura · foco = ('cajado', categoria) · amuleto = categoria."""
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
    if foco is not None: p['equip']['foco'] = foco if isinstance(foco, dict) else item('foco', foco[1], forma=foco[0])
    if amuleto is not None: p['equip']['amuleto'] = amuleto if isinstance(amuleto, dict) else item('amuleto', amuleto)
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
        # de quem é o ajuste: pelo ID da pessoa, quando a peça o guarda e quem veste tem ficha no mundo (dois de mesmo nome não dividem a peça); senão, pelo nome
        dele = sm['id'] == p['id'] if sm.get('id') and p.get('id') else sm['dono'] == p['nome']
        if dele: q -= T.SOB_MEDIDA * sm.get('grau', 1); mais = 1
        else: c -= T.NAO_E_DELE
    return max(0, c), max(0, q - p['atributos'][a]), mais


def _efeitos(it, dorme, cat=None, apelao=True, salvo=False):
    """(a parte 2, fase 1b) {chave: número} dos efeitos que valem nesta peça agora: nenhum na que dorme ou quebrou; o número de cada efeito de luta sai da categoria que ela
    RENDE (cat: a sob medida na mão de outro rende uma abaixo), e o cheio, da de cima (tabelas_efeitos.valor; a peça nunca guarda o número). O apelão de regra da peça que não é
    a escolhida dorme, só ele (apelao=False); o Imortal já gasto hoje (o `gasto` da peça) ou o salvamento de 1 PV já usado no dia (salvo) não vale. Os de antes: o critico_19 e o
    sangra valem True (a luta lê); o `devolve N` vale o % da categoria."""
    if dorme or it['dur'][0] <= 0: return {}
    c = it['cat'] if cat is None else cat; out = {}
    for e in it.get('efeitos', []):
        k = e['chave']
        if k in TE.EFEITOS:
            if TE.apelao_de_regra(k) and not apelao: continue
            if k == 'imortal' and salvo: continue
            v = TE.valor(k, c, bool(e.get('cheio')))
            if v is None: continue
            out[k] = (v, e.get('contra')) if k == 'cacadora' else v
        else: out[k] = e.get('valor', True)
    return out


def _dom(p, familia):
    """o dom da pessoa na mão desta arma (0 se não tem): soma no acerto, e metade na Defesa"""
    d = p.get('dom'); return int(d.get(TT.caminho_de(familia), 0)) if isinstance(d, dict) and familia in sum(TT.MAOS.values(), ()) else 0


def _arma(it, p, dorme, apelao=True):
    f = T.FAMILIAS[it['familia']]; c, falta, mais = _assenta(it, p, dorme); at = p['atributos']; tiro = bool(f.get('distancia'))
    quebrada = it['dur'][0] <= 0; dom = _dom(p, it['familia'])
    if quebrada: c = 0
    ef = _efeitos(it, dorme, c, apelao)
    w = dict(nome=it['nome'] + (' (quebrou)' if quebrada else ''), cat=c, dado=f['dado'], golpe=f['golpe'], alcance=f['alcance'], distancia=tiro, maos=f['maos'],
                recarga=f.get('recarga', 0), haste=f['alcance'] == 2 and not tiro,
                mult=T.MULT[c] * (T.DUAS_MAOS if f['maos'] == 2 and not tiro else 1),
                acerto=T.acerto_base(_maestria(p, it['familia']), at['Força'], at['Agilidade']) + T.BON[c] + mais - falta // T.FALTA_ACERTO + (T.QUEBRADA if quebrada else 0) + p.get('pena', 0) + dom,
                aparo=0 if tiro or quebrada else T.BON[c] + f.get('apara', 0),
                folego=1 + (1 if f['peso'] == 'pesada' and not ef.get('folego') else 0) + falta // T.FALTA_FOLEGO,      # (fase 1b) o Fôlego: a arma pesada custa 1 a menos
                fmult=T.BESTA_FORCA if it['familia'] == 'besta' else T.forca_mult(at[f.get('atributo', 'Força')]),
                efeitos=ef, item=it)
    if dom: w['dom'] = dom                                  # a luta sabe quando foi o dom que fez o golpe passar (marca.dom_visto)
    if isinstance(it.get('veneno'), dict) and not quebrada: w['veneno'] = it['veneno'].get('cat', 0)        # a dose de veneno na lâmina (a magia na luta)
    if it.get('encantos') or it.get('benta'): w['magica'] = True                                           # encantada ou benta: conta inteira contra o imaterial
    return w


def _cajado(it, p, dorme, apelao=True):
    """o CAJADO na mão é a arma: bate como maça leve (1d6, impacto, com a mão de maça e o que a arma leve pede de Força), apara com o bônus da categoria
    e, como toda arma de duas mãos, vale × 1,25"""
    fo = T.FOCOS['cajado']; at = p['atributos']; quebrada = it['dur'][0] <= 0
    c = 0 if quebrada else max(0, it['cat'] - (T.SINTONIA_ABAIXO if dorme else 0)); falta = max(0, T.PEDE_PESO['leve'] - at['Força'])
    return dict(nome=it['nome'] + (' (quebrou)' if quebrada else ''), cat=c, dado=fo['dado'], golpe=fo['golpe'], alcance=1, distancia=False, maos=2, recarga=0, haste=False,
                mult=T.MULT[c] * fo['vezes'], acerto=T.acerto_base(_maestria(p, 'maça'), at['Força'], at['Agilidade']) + T.BON[c] - falta // T.FALTA_ACERTO + (T.QUEBRADA if quebrada else 0) + p.get('pena', 0) + _dom(p, 'maça'),
                aparo=0 if quebrada else T.BON[c], folego=1 + falta // T.FALTA_FOLEGO, fmult=T.forca_mult(at['Força']), efeitos=_efeitos(it, dorme, c, apelao), item=it)


def _tracos(p, tracos):
    for t in tracos:
        if t not in TB_TRACOS() and t not in T.TRACOS_NOVOS and t not in T.TRACOS_POVO: sys.exit(f'{p["nome"]}: traço desconhecido: "{t}" (os que a luta roda: {", ".join(list(TB_TRACOS()) + list(T.TRACOS_NOVOS) + list(T.TRACOS_POVO))})')
    return list(tracos)


def TB_TRACOS():
    import tabelas_bichos as TB
    return TB.TRACOS


def _magia_neutra(F, p, tradicao_m=0):
    """os campos da magia na ficha, com valor neutro (a luta de magia os usa; quem não tem nada disso luta como hoje)"""
    at = p['atributos']; eq = p.get('equip') or {}; fe = list(p.get('feiticos') or []); dm = p.get('dom') if isinstance(p.get('dom'), dict) else {}
    dt = max([dm.get(t, 0) for t in T.TRADICOES] + [0])
    mx = p.get('mana_max')
    if mx is None: mx = T.mana_max(at['Afinidade'], at['Vontade'], tradicao_m, dt) if (fe or p.get('mana') is not None) else 0      # quem traz feitiços sem Mana começa com a cheia
    F.update(feiticos=fe, tradicao=p.get('tradicao'), mana_max=mx, mana=min(mx, p['mana']) if p.get('mana') is not None else mx, foco=eq.get('foco'), amuleto=eq.get('amuleto'),
             dom=dict(dm), pena_magia=p.get('pena_magia', 0), carga=dict(p.get('carga') or {}), elixires=[dict(x) for x in p.get('elixires') or []],
             doses=p.get('doses', 0), curado=p.get('curado', 0), funda=p.get('funda'), fases=[dict(x) for x in p.get('fases') or []], maldicoes=[dict(x) for x in p.get('maldicoes') or []])
    if p.get('mana_vista') is not None: F['mana_vista'] = p['mana_vista']       # a máxima que a pessoa conhece (o dom de tradição escondido): só a mesa a usa


def ficha_bicho(p):
    """a ficha de luta de um BICHO (a pessoa que o bichos.bicho devolve). O corpo é a arma e a armadura, com categoria, e não é peça:
    um registro só para o corpo todo, sem id e sem dono, que não quebra e não entra na conta da sintonia."""
    import tabelas_bichos as TB
    b = p['bicho']; at = p['atributos']; m = p['maestria']; c = b['cat']
    if b['tamanho'] not in TB.TAMANHOS: sys.exit(f'{p["nome"]}: tamanho desconhecido: "{b["tamanho"]}" (use: {", ".join(TB.TAMANHOS)})')
    if b['couro'] not in TB.COUROS: sys.exit(f'{p["nome"]}: couro desconhecido: "{b["couro"]}" (use: {", ".join(TB.COUROS)})')
    if not b['armas'] or any(x not in TB.ARMAS_CORPO for x in b['armas']): sys.exit(f'{p["nome"]}: as armas do corpo são: {", ".join(TB.ARMAS_CORPO)} (veio {b["armas"]})')
    _tracos(p, b['tracos'])                                 # os da etapa 2 (tabelas_bichos.TRACOS) e os da etapa da magia (tabelas.TRACOS_NOVOS)
    tam = TB.TAMANHOS[b['tamanho']]; como = TB.COUROS[b['couro']]; mat = T.MATERIAIS[como]
    corpo = dict(tipo='corpo', cat=c, nome=f"o corpo de {p['nome']}", dur=[1, 1], efeitos=[dict(chave='nao_quebra')])
    acerto = T.acerto_base(m, at['Força'], at['Agilidade']) + T.BON[c] + p.get('pena', 0)
    def arma(nome):
        a = TB.ARMAS_CORPO[nome]
        return dict(nome=f'{nome} {T.CATS[c]}', cat=c, dado=a['dado'], golpe=a['golpe'], alcance=tam['alcance'], distancia=False, maos=1, recarga=0, haste=False, mult=T.MULT[c],
                    acerto=acerto, aparo=T.BON[c], folego=a['folego'], fmult=T.forca_mult(at['Força']), efeitos={'nao_quebra': True}, corpo=True, item=corpo)
    F = dict(nome=p['nome'], nivel=p['nivel'], maestria=m, pvmax=int(T.pv_max(at['Vigor'], p['nivel']) * tam['pv']), folmax=max(T.FOLEGO_MIN, T.folego_max(at['Vigor']) - p.get('fol_menos', 0)),
             esforcos=T.esforcos(m), reacoes=T.reacoes(m), vontade_b=at['Vontade'] // 10, percep_b=at['Percepção'] // 10, agil_b=at['Agilidade'] // 10, forca_b=at['Força'] // 10, dormem=[],
             bicho=b.get('especie') or 'bicho', tamanho=b['tamanho'], tracos=list(b['tracos']), ocupa=tam['ocupa'], cerco=list(tam['cerco']), coragem=b.get('coragem', 0))
    F['pv'] = min(p.get('pv', F['pvmax']), F['pvmax']); F['fol'] = F['folmax']
    F['arma'] = arma(b['armas'][0]); F['arma2'] = None; F['punho'] = arma(b['armas'][0]); F['armas_corpo'] = [arma(x) for x in b['armas']]
    if 'sopro' in b['tracos']:
        F['sopro'] = dict(nome='o sopro', cat=c, dado=TB.SOPRO['dado'], golpe='sopro', alcance=TB.SOPRO['alcance'], distancia=True, maos=1, recarga=0, haste=False, mult=T.MULT[c],
                          acerto=acerto, aparo=0, folego=TB.SOPRO['folego'], fmult=TB.SOPRO['forca'], efeitos={'nao_quebra': True}, corpo=True, area=True, item=corpo)
    F['partes'] = {parte: dict(nome=f"{b['couro']} {T.CATS[c]}", cat=c, material=como, rd=T.RD[c] * mat['rd'], item=corpo) for parte in T.PARTES}
    F['nuas'] = []; F['fontes'] = [dict(item=corpo, efeitos={'nao_quebra': True})]; F['escudo'] = None; F['fol_rodada'] = 0; F['ini_mod'] = mat['ini']
    F['def_fixa'] = T.defesa_base(m, at['Agilidade']) + mat['defesa'] + tam['defesa'] + p.get('pena', 0)
    F['feridas0'] = [list(x) for x in p.get('feridas', [])]
    for k in ('id', 'lado', 'papel', 'moral', 'lider', 'guarda', 'controla', 'linha', 'pavor'):
        if k in p: F[k] = p[k]
    _magia_neutra(F, p, m)
    F['firmeza'] = T.firmeza(at['Vontade'], m, c if 'resiste' in F['tracos'] else None, None if 'resiste' in F['tracos'] else c)       # o corpo do bicho: metade do bônus (com resiste, inteiro)
    F.update(atributos=dict(at), afin_b=at['Afinidade'] // 10, pena=p.get('pena', 0), benzido=bool(p.get('benzido')), m_trad={t: m for t in T.TRADICOES}, cat_corpo=c,
             foco_cat=None, foco_falta=0, amuleto_cat=None, encantos=[], maldito=False, firmeza0=T.firmeza(at['Vontade'], m))      # o bicho que lança: o corpo é o foco, o instinto é a mão
    if p.get('maldicao'): F['maldicao'] = dict(p['maldicao'])          # o molde da maldição que o traço "amaldiçoa" põe (senão, o da página da magia)
    return F


def _povo(F, p):
    """O POVO (etapa da magia): a ficha de gente, com o corpo do povo por cima. O tamanho mexe no PV, na Defesa, no alcance da mão, no cerco e no corredor (como no bicho);
    os traços e a coragem são os do povo; a pele (couro) vale como armadura onde a peça não cobre."""
    import tabelas_bichos as TB
    b = p['povo']; tam = TB.TAMANHOS.get(b.get('tamanho', 'médio')) or sys.exit(f'{p["nome"]}: tamanho desconhecido: "{b.get("tamanho")}" (use: {", ".join(TB.TAMANHOS)})')
    F['pvmax'] = int(F['pvmax'] * tam['pv']); F['pv'] = min(p.get('pv', F['pvmax']), F['pvmax']); F['def_fixa'] += tam['defesa']
    F.update(povo=b.get('especie') or b.get('povo'), tamanho=b.get('tamanho', 'médio'), ocupa=tam['ocupa'], cerco=list(tam['cerco']), coragem=b.get('coragem', 0), cat_corpo=b.get('cat', 0))
    F['tracos'] = _tracos(p, list(dict.fromkeys(list(F.get('tracos') or []) + list(b.get('tracos') or []))))
    for w in (F['arma'], F['arma2'], F['punho']):
        if w and not w['distancia']: w['alcance'] = max(w['alcance'], tam['alcance'])       # a arma na mão de quem é grande alcança o que o braço alcança
    if b.get('couro'):
        if b['couro'] not in TB.COUROS: sys.exit(f'{p["nome"]}: couro desconhecido: "{b["couro"]}" (use: {", ".join(TB.COUROS)})')
        como = TB.COUROS[b['couro']]; mat = T.MATERIAIS[como]; c = b.get('cat', 0)
        corpo = dict(tipo='corpo', cat=c, nome=f"o corpo de {p['nome']}", dur=[1, 1], efeitos=[dict(chave='nao_quebra')])
        for parte in T.PARTES:
            if parte not in F['partes'] or F['partes'][parte]['rd'] < T.RD[c] * mat['rd']:
                F['partes'][parte] = dict(nome=f"{b['couro']} {T.CATS[c]}", cat=c, material=como, rd=T.RD[c] * mat['rd'], item=corpo)
        F['nuas'] = [x for x in T.PARTES if x not in F['partes']]; F['fontes'].append(dict(item=corpo, efeitos={'nao_quebra': True}))
        if not any('tronco' in (x.get('cobre') or []) for x in (p.get('equip') or {}).get('armaduras') or [] if x):
            F['def_fixa'] += mat['defesa'] - T.SEM_ARMADURA['defesa']; F['ini_mod'] = mat['ini']


def ficha(p):
    """a ficha de luta desta pessoa, hoje, com o que ela veste"""
    if p.get('bicho'):
        if isinstance(p['bicho'], str):                     # o atalho do cenário ({"nome": ..., "nivel": 0, "bicho": "lobo"}): a espécie inteira sai da tabela
            import bichos
            return ficha(bichos.bicho(p['bicho'], **{k: p[k] for k in ('nome', 'id', 'papel', 'moral', 'lider', 'guarda', 'controla', 'linha', 'pv', 'feridas', 'pena', 'fol_menos') if k in p}))      # o povo (goblin, orc) volta como gente, com as peças dele
        return ficha_bicho(p)
    at = p['atributos']; eq = dict(p.get('equip') or {}); foco = eq.get('foco'); cajado = bool(foco and foco.get('forma') == 'cajado')
    if cajado: eq['arma2'] = eq.get('arma2') or eq.get('arma'); eq['arma'] = None; eq['escudo'] = None      # O CAJADO pede as duas mãos: é a arma; a de antes fica de reserva, e o escudo não entra
    fam = 'maça' if cajado else (eq.get('arma') or {}).get('familia', 'punho'); m = _maestria(p, fam)
    arm = [x for x in eq.get('armaduras') or [] if x]
    todas = [x for x in (eq.get('arma'), eq.get('arma2'), eq.get('escudo')) if x] + arm + [x for x in (foco, eq.get('amuleto')) if x]
    # SINTONIA: as peças Épicas ou melhores (e toda peça encantada, de qualquer categoria), da melhor para a pior; as que passam do limite dormem. (Fase 1b) A peça com um
    # APELÃO DE REGRA ocupa 2 lugares, e só um apelão de regra fica acordado por pessoa: o da melhor peça acordada; o das outras dorme (só ele: o resto da peça vale)
    # Os 2 lugares são o preço do apelão ACORDADO: o da peça escolhida (a primeira peça de apelão, na ordem, que cabe com os 2 lugares). A outra peça de apelão tem o apelão
    # dormindo de qualquer jeito (um por pessoa) e ocupa 1 lugar, como toda peça alta: o resto dela vale (4.5.3). Sem isso, com Vontade 60 a armadura Lendária de Imortal ao
    # lado da arma Lendária de Golpe do Fim dormia inteira (4 lugares de 3), e com Vontade 80 ficava acordada: a mesma peça valia diferente. No empate de categoria, a ordem
    # da peça: arma, segunda arma, escudo, armaduras, foco, amuleto (o capítulo 28)
    altas = sorted([it for it in todas if it['cat'] >= T.SINTONIA_DESDE or it.get('encantos')], key=lambda i: -i['cat'])
    limite = max(1, at['Vontade'] // T.SINTONIA); usados = 0; sono = set(); escolhida = None
    for it in altas:
        if escolhida is None and _tem_apelao(it) and usados + 2 <= limite: escolhida = id(it); usados += 2
        elif usados + 1 <= limite: usados += 1
        else: sono.add(id(it))
    dorme = lambda it: id(it) in sono
    apelao = lambda it: it is None or not _tem_apelao(it) or id(it) == escolhida
    F = dict(nome=p['nome'], nivel=p['nivel'], maestria=m, pvmax=T.pv_max(at['Vigor'], p['nivel']), folmax=max(T.FOLEGO_MIN, T.folego_max(at['Vigor']) - p.get('fol_menos', 0)),
             esforcos=T.esforcos(m), reacoes=T.reacoes(m), vontade_b=at['Vontade'] // 10, percep_b=at['Percepção'] // 10, agil_b=at['Agilidade'] // 10,
             forca_b=at['Força'] // 10, dormem=[it['nome'] for it in altas if id(it) in sono])
    apelao_dorme = [it['nome'] for it in altas if id(it) not in sono and _tem_apelao(it) and id(it) != escolhida]
    if apelao_dorme: F['apelao_dorme'] = apelao_dorme       # (fase 1b) a peça acordada cujo apelão de regra dorme (um por pessoa)
    F['pv'] = p.get('pv', F['pvmax']); F['fol'] = F['folmax']
    punho = item('arma', 0, 'as mãos', familia='punho', efeitos=[dict(chave='nao_quebra')])
    F['arma'] = _cajado(foco, p, dorme(foco), apelao(foco)) if cajado else _arma(eq.get('arma') or punho, p, dorme(eq['arma']) if eq.get('arma') else False, apelao(eq.get('arma')))
    F['arma2'] = _arma(eq['arma2'], p, dorme(eq['arma2']), apelao(eq['arma2'])) if eq.get('arma2') else None
    F['punho'] = _arma(punho, p, False)
    # a armadura, parte por parte (a melhor peça que cobre a parte)
    F['partes'] = {}; falta_arm = 0; fol_arm = 0; F['fontes'] = []; corpo = T.SEM_ARMADURA
    salvo = bool(p.get('salvo_dia'))                        # (fase 1b) o salvamento de 1 PV do dia já foi (um por dia, venha de onde vier)
    for it in arm:
        c, falta, mais = _assenta(it, p, dorme(it)); mat = T.MATERIAIS[it['material']]
        falta_arm += falta; fol_arm = max(fol_arm, mat['folego'])
        F['fontes'].append(dict(item=it, efeitos=_efeitos(it, dorme(it), c, apelao(it), salvo)))
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
        F['fontes'].append(dict(item=esc, efeitos=_efeitos(esc, dorme(esc), c, apelao(esc)), escudo=True))
    for it, k in ((eq.get('amuleto'), 'amuleto'), (foco, 'foco')):     # (fase 1b) o amuleto e o foco também são fontes de efeito (a Firmeza, a Coragem, a Guarda Mágica, o Imortal; a Chama, o Foco Certeiro, o Domínio)
        if it and it.get('efeitos'): F['fontes'].append(dict(item=it, efeitos=_efeitos(it, dorme(it), it['cat'], apelao(it), salvo), **{k: True}))
    F['fol_rodada'] = fol_arm + falta_arm // T.FALTA_FOLEGO; F['ini_mod'] = corpo['ini']
    for k in ('id', 'lado', 'papel', 'moral', 'lider', 'guarda', 'controla', 'linha'):
        if k in p: F[k] = p[k]
    dm = _dom(p, fam)
    if dm: F['def_fixa'] += dm / 2                          # o dom da mão da arma na mão: metade na Defesa, como a maestria
    mm = p['maestria']; trad = p.get('tradicao')
    mt = (mm.get(trad, 0) if trad else max([mm.get(t, 0) for t in T.TRADICOES] + [0])) if isinstance(mm, dict) else (mm or 0)
    _magia_neutra(F, p, mt); F['tracos'] = _tracos(p, p.get('tracos') or [])
    if p.get('coragem'): F['coragem'] = p['coragem']                                # a coragem do povo do personagem (etapa 4b): soma no teste de coragem
    if isinstance(mm, dict) and (mm.get('manha') or 0) > 0: F['manha'] = mm['manha']       # a mão de manha (etapa 4b): o golpe pelas costas
    if p.get('maldicao'): F['maldicao'] = dict(p['maldicao'])
    _magia_ficha(F, p, eq, dorme)
    if p.get('povo'): _povo(F, p)
    _fx(F, p)
    _firmeza(F, p)
    # (fase 1b) o que cada peça com id RENDE agora para esta pessoa (a mesa mostra o número do efeito por ela: a sob medida na mão de outro rende uma abaixo; a que dorme na
    # sintonia rende uma abaixo e tem os efeitos dormindo; a quebrada não tem efeito; o apelão de regra que não é o acordado dorme sozinho)
    F['rende'] = {it['id']: dict(cat=0 if it['dur'][0] <= 0 else _assenta(it, p, dorme(it))[0], dorme=dorme(it), quebrada=it['dur'][0] <= 0, apelao_dorme=_tem_apelao(it) and not apelao(it) and not dorme(it))
                  for it in todas if it.get('id')}
    return F


def _tem_apelao(it): return bool(it) and any(isinstance(e, dict) and TE.apelao_de_regra(e.get('chave')) for e in it.get('efeitos') or [])


def maior(fontes, k):
    """P5: o mesmo efeito de duas fontes vale o maior (o número que cresce: tabelas_efeitos.ordem_valor), ou None"""
    vs = [s['efeitos'][k] for s in fontes if k in s['efeitos']]
    return max(vs, key=lambda v: TE.ordem_valor(k, v)) if vs else None


def _fx(F, p):
    """(a parte 2, fase 1b) a PILHA DAS PEÇAS ACORDADAS na ficha: F['fx'] = {chave: número} dos efeitos de armadura, escudo, amuleto e foco (o mesmo efeito de duas fontes vale
    o maior: P5); os números fixos novos com o teto (P3: até +8; a resistência à carga até +16; a Robusta põe metade na coragem); o fôlego máximo da Robusta. A arma leva os dela
    (F['arma']['efeitos']). A luta relê das fontes inteiras (a peça desfeita perde os efeitos). E o gancho das provas: p['fx_prova'] põe números nas fontes (o banco mede assim)."""
    fp = p.get('fx_prova') or {}
    for alvo, d in fp.items():
        if alvo == 'arma':
            for w in (F['arma'], F.get('arma2')):
                if not w: continue
                if d.get('folego') and not w['efeitos'].get('folego') and T.FAMILIAS.get((w.get('item') or {}).get('familia'), {}).get('peso') == 'pesada': w['folego'] -= 1     # o Fôlego posto pelo banco: o que o _arma faz com o da peça
                w['efeitos'].update(d)
        else:
            src = next((s for s in F['fontes'] if s.get(alvo) or (alvo == 'armadura' and s['item'].get('tipo') == 'armadura')), None)
            if src is None:
                it = (F.get('foco') if alvo == 'foco' else F.get('amuleto') if alvo == 'amuleto' else None) or dict(tipo=alvo, cat=0, nome=f'({alvo} de prova)', dur=[1, 1], efeitos=[])
                src = dict(item=it, efeitos={}, **{alvo: True}); F['fontes'].append(src)
            src['efeitos'].update(d)
    fx = {}
    for s in F['fontes']:
        for k in s['efeitos']:
            if k in TE.EFEITOS: fx[k] = maior(F['fontes'], k)
    F['fx'] = fx
    rb = fx.get('robusta')
    if rb: F['folmax'] += rb[1]; F['fol'] = F['folmax']; F['robusta_fol'] = rb[1]     # a Robusta (com o antigo Fole): o fôlego máximo a mais (a luta o tira se a armadura se desfaz)


def _magia_ficha(F, p, eq, dorme):
    """o que a luta de magia lê da ficha (capítulo 11): a mão de cada tradição, o foco e o amuleto com a categoria que rendem hoje (a sintonia: o que dorme rende uma abaixo;
    o que quebrou não vale), o que falta do atributo que o foco pede, os encantos das peças e quais dormem, e se a pessoa traz peça maldita"""
    at = p['atributos']; mm = p['maestria']
    F.update(atributos=dict(at), afin_b=at['Afinidade'] // 10, pena=p.get('pena', 0), benzido=bool(p.get('benzido')), guarda_p=p.get('guarda_p'), pena_laco=p.get('pena_laco', 0), cat_corpo=0,
             m_trad={t: (mm.get(t, 0) if isinstance(mm, dict) else (mm or 0)) for t in T.TRADICOES}, foco_cat=None, foco_falta=0, amuleto_cat=None, encantos=[])
    fo = eq.get('foco'); am = eq.get('amuleto')
    if fo and fo['dur'][0] > 0:
        a, q = pede(fo, dorme(fo)); F['foco_cat'] = max(0, fo['cat'] - (T.SINTONIA_ABAIXO if dorme(fo) else 0)); F['foco_falta'] = max(0, q - at[a]) // TM.FALTA
    if am and am['dur'][0] > 0: F['amuleto_cat'] = max(0, am['cat'] - (T.SINTONIA_ABAIXO if dorme(am) else 0))
    for it in [x for x in (eq.get('arma'), eq.get('arma2'), eq.get('escudo')) if x] + [x for x in eq.get('armaduras') or [] if x]:
        for i, e in enumerate(it.get('encantos') or []):
            c = max(0, it['cat'] - (T.SINTONIA_ABAIXO if dorme(it) else 0) - TM.ENCANTO['abaixo'])
            F['encantos'].append(dict(item=it, idx=i, feitico=e['feitico'], grau=e.get('grau', 1), cat=c, carregado=bool(e.get('carregado', e.get('gasto') is None)), dorme=dorme(it), nome=it['nome']))
    F['maldito'] = any(x and x.get('maldita') for x in [eq.get('arma'), eq.get('arma2'), eq.get('escudo'), fo, am] + list(eq.get('armaduras') or []))


def _firmeza(F, p):
    """a Firmeza da ficha: a base comum (tabelas.firmeza, sem a guarda) e o melhor entre o bônus do amuleto e metade do da armadura do tronco (com "resiste", inteiro).
    O calejo é da luta."""
    mm = p['maestria']; maior = max([v for v in mm.values() if isinstance(v, (int, float))] + [0]) if isinstance(mm, dict) else (mm or 0)
    dmt = max([F['dom'].get(t, 0) for t in T.TRADICOES] + [0]); F['firmeza0'] = T.firmeza(p['atributos']['Vontade'], maior, None, None, dmt)
    tr = F['partes'].get('tronco'); b = T.BON[F['amuleto_cat']] if F['amuleto_cat'] is not None else 0
    if tr and tr['item']['dur'][0] > 0: b = max(b, T.BON[tr['cat']] * (1 if 'resiste' in F['tracos'] else 0.5))
    F['firmeza'] = F['firmeza0'] + b + min(TE.FIXO_TETO, (F.get('fx') or {}).get('firmeza') or 0)        # (fase 1b) o efeito Firmeza do amuleto, no teto de +8


def defesa(F, w=None, escudo_inteiro=True):
    """a Defesa com a arma w na mão: a fixa, mais o que apara melhor: o escudo (arma de uma mão e escudo inteiro) ou a própria arma"""
    w = w or F['arma']
    esc = F['escudo']['bonus'] if F['escudo'] and w['maos'] == 1 and escudo_inteiro else 0
    return F['def_fixa'] + max(esc, w['aparo'])


def linha(F):
    """a ficha em três linhas, para a mesa (os números com vírgula)"""
    import re
    return re.sub(r'(?<![\w])-(\d)', r'−\1', re.sub(r'(\d)\.(\d)', r'\1,\2', _linha(F)))       # 29,5 · −2


def conj_ficha(F, trad=None):
    """(a tradição, a Conjuração) que a ficha mostra: a da tradição da pessoa (ou a melhor mão), com o foco que rende para ela (sem foco: Comum, −4), o dom e a pena do corpo"""
    trad = trad or F.get('tradicao') or max(T.TRADICOES, key=lambda t: F['m_trad'].get(t, 0)); fo = F.get('foco'); c, mais = 0, TM.SEM_FOCO
    if isinstance(fo, dict) and F.get('foco_cat') is not None:
        k = F['foco_cat'] - (0 if trad in T.FOCOS[fo['forma']]['de'] else TM.FOCO_OUTRA)
        if k >= 0: c, mais = k, -F.get('foco_falta', 0)
    return trad, F['m_trad'].get(trad, 0) + int((F.get('dom') or {}).get(trad, 0) or 0) + (F['atributos'][T.TRADICOES[trad]] // 10) / 2 + T.BON[c] + mais + F.get('pena', 0)


def _magia_linha(F):
    """a linha da magia na ficha (só de quem tem magia: feitiço, foco ou amuleto)"""
    fo, am = F.get('foco') if isinstance(F.get('foco'), dict) else None, F.get('amuleto') if isinstance(F.get('amuleto'), dict) else None
    if not (F.get('feiticos') or fo or am): return ''
    L = []
    if F.get('feiticos'):
        trad, cj = conj_ficha(F); L.append(f"magia ({trad}): Mana {F['mana']}/{F['mana_max']} · sabe: {', '.join(T.nome_feitico(k) for k in F['feiticos'])} · Conjuração {cj:+g}")
    L.append(f"Firmeza {F['firmeza']:g}")
    if fo: L.append(f"foco: {fo['nome']}" + (' (dorme: rende uma abaixo)' if fo['nome'] in F['dormem'] else '') + (f", falta atributo (−{F['foco_falta']})" if F.get('foco_falta') else ''))
    elif F.get('feiticos'): L.append(f'sem foco (lança com as mãos: Comum, {TM.SEM_FOCO})'.replace('-', '−'))
    L.append(f"amuleto: {am['nome']}" + (' (dorme)' if am['nome'] in F['dormem'] else '') if am else 'sem amuleto: contra a magia, a armadura guarda 0,6')
    if F.get('encantos'): L.append('encanto: ' + ', '.join(f"{T.nome_feitico(e['feitico'])} em {e['nome']}" + ('' if e['carregado'] else ' (descarregado)') + (' (dorme)' if e['dorme'] else '') for e in F['encantos']))
    return '\n  ' + ' · '.join(L)


def _linha(F):
    if F.get('bicho'):
        w = F['arma']; pt = F['partes']['tronco']; ext = ' + '.join('1' if x == 1 else '1 pelo dobro do fôlego' for x in F['esforcos'])
        return (f"{F['nome']} (bicho {F['tamanho']}, nível {F['nivel']}, instinto de {T.MAESTRIAS.get(F['maestria'], F['maestria'])}) · PV {F['pv']}/{F['pvmax']} · fôlego {F['folmax']} · {T.ACOES} ações (a mais: {ext})\n"
                f"  o corpo é a arma: " + ' · '.join(f"{x['nome']} ({x['dado']} × {x['mult']:g}, {x['golpe']})" for x in F['armas_corpo']) + f" · acerto {w['acerto']:+g} · força × {w['fmult']:.2f} · alcança {w['alcance']} casa{'s' if w['alcance'] != 1 else ''}"
                + (f" · {F['sopro']['nome']} ({F['sopro']['dado']} × {F['sopro']['mult']:g}, a {F['sopro']['alcance']} casas)" if F.get('sopro') else '') + '\n'
                f"  Defesa {defesa(F):g} · o corpo é a armadura: {pt['nome']} (proteção {pt['rd']:g}, vale como {pt['material']}) · cerco: {F['cerco'][0]} de perto e {F['cerco'][1]} de haste · ocupa {F['ocupa']:g} de um corredor"
                + (f" · traços: {', '.join(F['tracos'])}" if F['tracos'] else '') + (f" · coragem {F['coragem']:+d}" if F.get('moral') != 'firme' else ' · não foge')
                + (f"\n  lança pelo instinto: {', '.join(T.nome_feitico(k) for k in F['feiticos'])} · Mana {F['mana']}/{F['mana_max']}" if F.get('feiticos') else ''))
    w = F['arma']; ps = ' · '.join(f"{k} {v['rd']:g}" for k, v in F['partes'].items()) or 'sem armadura'
    ext = ' + '.join('1' if x == 1 else '1 pelo dobro do fôlego' for x in F['esforcos'])
    return (f"{F['nome']} (nível {F['nivel']}, mão de {T.MAESTRIAS.get(F['maestria'], F['maestria'])}) · PV {F['pv']}/{F['pvmax']} · fôlego {F['folmax']} · {T.ACOES} ações (a mais: {ext})\n"
            f"  {w['nome']}: acerto {w['acerto']:+g} · {w['dado']} × {w['mult']:g} ({w['golpe']}), força × {w['fmult']:.2f} · {w['folego']} de fôlego por golpe"
            + (f", mais {F['fol_rodada']} por rodada da armadura" if F['fol_rodada'] else '') + '\n'
            f"  Defesa {defesa(F):g}" + (f" (com {F['escudo']['nome']})" if F['escudo'] and w['maos'] == 1 else '') + f" · proteção: {ps}"
            + (f" · SEM PROTEÇÃO: {', '.join(F['nuas'])}" if F['nuas'] and F['partes'] else '') + (f" · DORMEM: {', '.join(F['dormem'])}" if F['dormem'] else '')
            + (f" · O APELÃO DORME (um acordado por pessoa): o de {', '.join(F['apelao_dorme'])}" if F.get('apelao_dorme') else '') + _povo_linha(F) + _magia_linha(F))


def _povo_linha(F):
    """o que o povo do personagem põe na ficha (etapa 4b): os traços dele e a coragem; de quem não tem nada disso, nada (a linha de hoje sai igual)"""
    tp = [t for t in F.get('tracos') or [] if t in T.TRACOS_POVO]
    return (f" · {', '.join(tp)}" if tp else '') + (f" · coragem {F['coragem']:+d}" if F.get('coragem') and not F.get('povo') else '') + (f" · manha de {T.MAESTRIAS.get(F['manha'], F['manha'])}" if F.get('manha') else '')


if __name__ == '__main__':
    import signal; hasattr(signal, 'SIGPIPE') and signal.signal(signal.SIGPIPE, signal.SIG_DFL)      # a saída cortada (`| head`) acaba o comando calada, sem erro de programa: tudo já foi gravado antes de falar
    a = sys.argv[1:]
    if len(a) < 2 or a[0] != 'padrao' or not a[1].isdigit(): sys.exit('diga o nível, em número: `python3 pessoas.py padrao 50 arma=espada:Raro armadura=malha:Raro escudo=Raro`' if a[:1] == ['padrao'] else __doc__)
    op = dict(x.split('=', 1) for x in a[2:])
    par = lambda s: (s.split(':')[0], cat_i(s.split(':')[1]))
    p = veste(padrao('exemplo', int(a[1]), molde=op.get('molde', 'guerreiro')), arma=par(op['arma']) if 'arma' in op else None,
              armadura=par(op['armadura']) if 'armadura' in op else None, escudo=cat_i(op['escudo']) if 'escudo' in op else None)
    print(linha(ficha(p)))
