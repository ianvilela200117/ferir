#!/usr/bin/env python3
"""provas_habilidades.py — MOTOR 10, A PARTE 2, FASE 2: O BANCO DAS HABILIDADES E DA FALA (o contrato: projeto/etapa_efeitos/DESENHO.md, seção 10, as metas HB1 a HB13, e B0, B2, B3).

As lutas são as do banco (o duelo de iguais: nível 50, mão de Mestre, tudo Raro, começando perto; espelhado: metade com a habilidade no lado A, metade no B), com semente própria
(à parte dos outros blocos). Os mundos são de prova (provas_mundo.vila, numa pasta de rascunho): nada toca um save de verdade. O B1 (o ano) é o provas_ano, que o provas_mundo roda.
  B0 A LUTA DE SEMPRE: as mesmas lutas ao acaso, sem habilidade, no motor de antes desta fase (o commit B0_REF, tirado do git) e no de agora: iguais, dado por dado.
  HB1 A RÉGUA (cada habilidade de luta em cada grau, 8.000 lutas por linha) · HB2 O ITEM DECIDE · HB3 A PILHA · HB4 O CONTROLE NÃO TRAVA · HB5 O RITMO · HB6 OS FREIOS
  · HB7 A FALA, A CONTA · HB8 A ESCOLHA DO JOGADOR · HB9 A MINA · HB10 A FORJA (e o B2) · HB11 COPIAR E O ESTALO · HB12 A MESA E A ORDEM · HB13 LANÇAR · B3 O ITEM DECIDE.

Uso: python3 provas_habilidades.py [N] [so=HB1,HB7]      N = lutas por linha da HB1 (padrão 8.000, o do contrato); as outras metas escalam com ele
     hb1=CHAVE,...   só essas habilidades na HB1 (a mesma semente do banco inteiro: a linha sai igual)
"""
import contextlib, io, json, math, os, random, shutil, statistics, subprocess, sys, tempfile
import luta
import tabelas as T
import tabelas_habilidades as H
import tabelas_efeitos as TE
import tabelas_talento as TT
import habilidade, estado, teste, fala
from pessoas import padrao, veste
from itens import item

FOLGA = 1.5                 # a folga das habilidades nas bordas da faixa (seção 10)
B0_REF = 'b431264'          # o commit do motor de antes da fase 2 (a fase 1b no save): o B0 roda as mesmas lutas nele e no de agora
R = 2


def _f(x): return f'{x:+.1f}'.replace('.', ',')


def quieto(f, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()): return f(*a, **k)


# ---------- as lutas do banco ----------
def lado(nome, hab, fam, cat=R, arm=R, nivel=50, esc=True, **kw):
    e = arm if (esc and T.FAMILIAS[fam]['maos'] == 1) else None
    return veste(padrao(nome, nivel, **({'habilidades': dict(hab)} if hab else {}), **kw), arma=(fam, cat), armadura=('malha', arm), escudo=e)


def vence(faz_a, faz_b, n, seed, **kw):
    D0 = luta.D; luta.semente(seed); v = 0.0
    try:
        for _ in range(n):
            S = luta.nova(faz_a(), faz_b(), quieto=True, **{**dict(inicio='perto'), **kw}); luta.corre(S)
            v += 1 if S['fim'] == 'A' else 0 if S['fim'] == 'B' else 0.5
    finally: luta.D = D0
    return v / max(1, n)


def pontos(hab, fam, n, seed, **kw):
    """os pontos de vitória da habilidade no duelo de iguais, espelhado: (a vitória de quem tem, metade em cada lado) − 50"""
    com = lambda: [lado('com', hab, fam)]; sem = lambda: [lado('sem', None, fam)]
    a = vence(com, sem, n // 2, seed, **kw); b = vence(sem, com, n - n // 2, seed + 7919, **kw)
    return 100 * (a + (1 - b)) / 2 - 50


def delta(faz_com, faz_sem, faz_contra, n, seed, **kw):
    return 100 * (vence(faz_com, faz_contra, n, seed, **kw) - vence(faz_sem, faz_contra, n, seed, **kw))


# ---------- HB1 A RÉGUA ----------
DUELO = dict(roda='martelo', sanha='espada', trunfos='espada', tranco='martelo', corte_fundo='espada', riposta='espada', bigorna='espada', brado='espada', teima='espada', rito_veia='espada')


def _cenas(k, g, n, seed):
    """os pontos das habilidades medidas fora do duelo de iguais (o cenário de cada uma: 6.7)"""
    hb = {k: g}
    if k == 'golpe_quebra':          # contra a armadura uma acima: a vitória com ela − sem ela, contra o mesmo lado
        return delta(lambda: [lado('a', hb, 'martelo')], lambda: [lado('a', None, 'martelo')], lambda: [lado('b', None, 'martelo', arm=R + 1)], n, seed)
    if k == 'rasteira': return pontos(hb, 'lança', n, seed)
    if k == 'varrida':               # um contra três mais fracos
        tres = lambda: [lado(f'b{i}', None, 'espada', cat=1, arm=1, nivel=30) for i in range(3)]
        return delta(lambda: [lado('a', hb, 'montante')], lambda: [lado('a', None, 'montante')], tres, n, seed)
    if k == 'manter':                # a lança contra a espada, de longe
        return delta(lambda: [lado('a', hb, 'lança')], lambda: [lado('a', None, 'lança')], lambda: [lado('b', None, 'espada')], n, seed, inicio='longe')
    if k == 'mira_firme':            # o duelo de arqueiros, de longe, o outro de couro uma acima (onde a fresta vale: o robô não mira, DESENHO 12.4)
        arq = lambda nm, h, arm=R: [veste(padrao(nm, 50, molde='arqueiro', **({'habilidades': h} if h else {})), arma=('arco', R), arma2=('adaga', R), armadura=('couro', arm))]
        return delta(lambda: arq('a', hb), lambda: arq('a', None), lambda: arq('b', None, arm=R + 1), n, seed, inicio='longe')
    if k in ('golpe_voto', 'golpe_voto@maldito'):      # o clérigo de maça contra o igual vivo (o teto normal) e contra o MALDITO de verdade (a peça maldita na mão: magia.maldito;
        import provas                                  # o dobro, o teto forte). O "sem vida" de antes não é maldito (o magia.maldito não o conta): a casa media o vivo
        cl = lambda h: [provas.clerigo('c', **({'habilidades': {'golpe_voto': g}} if h else {}))]
        maldita = dict(nome='a praga do fio', cat=R, tipo='míngua', condicao={'tipo': 'nunca'}) if k.endswith('@maldito') else None
        outro = lambda: [veste(padrao('m', 50), arma=item('arma', R, familia='espada', **({'maldita': maldita} if maldita else {})), armadura=('malha', R), escudo=R)]
        return delta(lambda: cl(hb), lambda: cl(None), outro, n, seed)
    if k == 'estanca':               # o três contra três: um dos três ata e cura
        tres = lambda pre, h: [lado(f'{pre}{i}', h if i == 0 else None, 'espada') for i in range(3)]
        return delta(lambda: tres('a', hb), lambda: tres('a', None), lambda: tres('b', None), n, seed)
    return None


FORA_DO_DUELO = ('golpe_quebra', 'rasteira', 'varrida', 'manter', 'mira_firme', 'golpe_voto', 'golpe_voto@maldito', 'estanca')
TETO_CENA = {'golpe_voto@maldito': 'forte'}          # o Golpe de Voto contra o maldito: o teto forte (6.7: "normal; forte contra o maldito")
# AS CASAS DE BORDA, decididas ANTES de rodar (pelas medidas da construção e do conserto: a menos de 2 pontos do teto da faixa + 1,5): medidas no modo longo (2,5 vezes as
# lutas, de saída; nunca uma segunda medida só da casa que reprovou). Assim o acaso de 8.000 lutas (±0,6 a um desvio) não reprova a casa que está dentro.
BORDA = {('roda', 0), ('roda', 2), ('trunfos', 0), ('trunfos', 2), ('riposta', 5), ('rito_veia', 2), ('rito_veia', 4), ('rito_veia', 5), ('golpe_quebra', 4), ('golpe_quebra', 5),
         ('mira_firme', 3), ('mira_firme', 4), ('mira_firme', 5), ('golpe_voto', 5)}       # (o conserto, a 20.000 e 40.000 lutas: a Roda I +4,5 e Ad +10,4; os Trunfos I +5,0 e Ad +9,7; a Riposta GM +10,3; o Rito Ad +10,2, M +20,2, GM +20,7; o Golpe de Voto GM +10,0)
LONGO = 2.5


def banda(k, g):
    """a força que o grau g deixa nesta casa (6.2), pelo teto dela (a cena contra o maldito tem o teto forte)"""
    kk = k.split('@')[0]; t = TETO_CENA.get(k, H.HABILIDADES[kk]['teto']); f = H.FORCA_DO_GRAU[g] or t
    return TE.FORCA_PONTOS[f if TE.FORCAS.index(f) <= TE.FORCAS.index(t) else t]


HB1_SO = None


def hb1(n):
    """HB1 A RÉGUA: cada habilidade de luta em cada grau, MEDIDA UMA VEZ, com o mesmo N para todas as casas, decidido antes de ver o resultado (n lutas no duelo; n/2 lutas pareadas
    nas cenas próprias, que medem com e sem ela contra o mesmo lado): dentro da força que o grau deixa (6.2: I até 5, Ap e Ad até 10, P e M até 20, GM até o teto dela; a folga
    de 1,5), nenhuma acima de 40 — é isso que passa ou reprova, pela leitura do DESENHO 12.4. E a distância às medidas (m) da tabela de 6.7 (do rascunho): escrita, casa por casa,
    em todas as que têm medida (as do duelo e as de cena própria). Pela letra (a tabela a ±1,5 também reprova), o banco diz se passaria."""
    linhas = []; fora_banda = []; fora_tabela = []; i = 0
    for k in list(DUELO) + list(FORA_DO_DUELO):
        i += 1
        if HB1_SO and k not in HB1_SO and k.split('@')[0] not in HB1_SO: continue      # `hb1=CHAVE,...`: só essas (a semente de cada uma é a mesma do banco inteiro)
        kk = k.split('@')[0]; h = H.HABILIDADES[kk]; vals = []
        med = h.get('medido') if '@' not in k else None
        for g in range(6):
            sd = 61000 + 100 * i + g; n0 = n if k in DUELO else max(400, n // 2)
            if (k, g) in BORDA: n0 = int(n0 * LONGO)          # a casa de borda: o modo longo, decidido antes
            v = pontos({k: g}, DUELO[k], n0, sd) if k in DUELO else _cenas(k, g, n0, sd)
            if v > banda(k, g) + FOLGA or v > 40: fora_banda.append(f"{nome(kk)}{' (contra o maldito)' if '@' in k else ''} {H.CURTO[g]} {_f(v)} (até {banda(k, g)})")
            if med and h['mede'] == 'm' and abs(v - med[g]) > FOLGA: fora_tabela.append(f"{nome(kk)} {H.CURTO[g]} {_f(v)} (o rascunho {_f(med[g])})")
            vals.append(_f(v) + ('*' if (k, g) in BORDA else ''))
        cena = 'contra o maldito' if '@' in k else DUELO.get(k, 'cena própria')
        linhas.append(f"{nome(kk)} ({cena}): " + ' · '.join(vals) + (f" [o rascunho: {' · '.join(_f(x) for x in med)}{', remede' if h['mede'] == 'remede' else ''}]" if med else f" ({h['mede']})"))
        print(f"    HB1 {linhas[-1]}", flush=True)
    ok = not fora_banda                                     # (DESENHO 12.4) passa pela faixa do grau; a tabela de 6.7 a ±1,5 vai escrita (pela letra, reprova)
    return [(f"HB1 A RÉGUA: cada habilidade de luta em cada grau, medida uma vez com o N decidido antes ({n} lutas por casa no duelo; {max(400, n // 2)} pareadas nas cenas próprias; as casas de borda, marcadas com *, {LONGO:g} vezes isso), na força que o grau deixa (I até 5, Ap e Ad até 10, P e M até 20, GM até o teto dela; a folga de 1,5) e nunca acima de 40 (a leitura do DESENHO 12.4); e a distância às medidas (m) do rascunho (6.7)",
             ('; '.join(linhas)) + (f" · FORA DA FAIXA: {', '.join(fora_banda)}" if fora_banda else ' · todas na faixa do grau')
             + (f" · a mais de 1,5 das medidas (m) do rascunho: {len(fora_tabela)} casas ({', '.join(fora_tabela)}): pela letra da HB1 (a tabela a ±1,5), REPROVA" if fora_tabela else ' · todas as (m) a ±1,5 do rascunho: pela letra, passa também'), ok)]


def nome(k): return habilidade.nome(k)


# ---------- HB2 e B3 O ITEM DECIDE ----------
TOPO = dict(roda=5, trunfos=5, riposta=5)


def hb2(n):
    """HB2 O ITEM DECIDE: a Roda, os Trunfos e a Riposta no Grão-Mestre (martelo Raro) contra o martelo uma acima sem nada, e contra o conjunto uma acima (o de cima vence 60% ou mais);
    e o B3 da fase: contra o conjunto DUAS acima (85% ou mais)"""
    nn = max(2000, n // 2); com = lambda: [lado('com', TOPO, 'martelo')]
    arma = 100 - 100 * vence(com, lambda: [lado('e', None, 'martelo', cat=R + 1)], nn, 62001)
    conj = 100 - 100 * vence(com, lambda: [lado('e', None, 'martelo', cat=R + 1, arm=R + 1)], nn, 62002)
    dois = 100 - 100 * vence(com, lambda: [lado('e', None, 'martelo', cat=R + 2, arm=R + 2)], nn, 62003)
    iguais = pontos(TOPO, 'martelo', nn, 62004)
    return [(f"HB2 O ITEM DECIDE: a Roda, os Trunfos e a Riposta no Grão-Mestre, martelo Raro, contra o martelo Épico sem nada e contra o conjunto Épico (o de cima vence 60% ou mais; o contrato mediu 70,3 e 79,2)",
             f"entre iguais as três juntas valem {_f(iguais)} (abaixo de 40); o martelo Épico vence {arma:.1f}%; o conjunto Épico, {conj:.1f}%".replace('.', ','), arma >= 60 and conj >= 60 and iguais < 40),
            (f"B3 O ITEM DECIDE (fase 2): o topo das habilidades contra o conjunto uma acima (60% ou mais) e DUAS acima (85% ou mais)",
             f"uma acima vence {conj:.1f}%; duas acima, {dois:.1f}%".replace('.', ','), conj >= 60 and dois >= 85)]


# ---------- HB3 A PILHA ----------
def hb3(n):
    """HB3 A PILHA: o grupo TÉCNICA em 10.000 golpes nunca passa de +40% (a Roda no topo com o Golpe de Voto: 30% + 30%); a segunda acesa apaga a primeira; os dados rolam o maior
    entre o fecho, o crítico e o Golpe do Fim, nunca mais de 4; o dado somado (o trunfo, o Rito) entra uma vez e não dobra no crítico; o teto da pilha (EF4: nunca mais de 7 vezes)"""
    import provas
    med = []; xs = []; orig = habilidade.dado_extra; tec_max = [0.0]; tec_o = habilidade.tecnica
    def conta_x(S, a, e, w, j, hg):
        x = orig(S, a, e, w, j, hg); xs.append((j['crit'], x, len(hg.get('_x', []))))
        hg.setdefault('_x', []).append(1); return x
    def tec(S, a, e, w):
        t = tec_o(S, a, e, w); tec_max[0] = max(tec_max[0], min(TE.PILHA['tecnica'], t)); return t
    habilidade.dado_extra = conta_x; habilidade.tecnica = tec
    D0 = luta.D; luta.semente(63001); golpes = 0
    try:
        while golpes < 10000:
            a = provas.clerigo('a', habilidades=dict(roda=5, golpe_voto=5, trunfos=5)); b = provas.clerigo('b', habilidades=dict(roda=5, golpe_voto=5, rito_veia=5))
            S = luta.nova([a], [b], quieto=True, inicio='perto'); S['mede'] = med; luta.corre(S); golpes = len(med)
    finally: luta.D = D0; habilidade.dado_extra = orig; habilidade.tecnica = tec_o
    duas = lado('x', dict(roda=5, sanha=5), 'martelo'); S = luta.nova([duas], [lado('y', None, 'martelo')], quieto=True); f = luta.por_nome(S, 'x')
    habilidade.acende(S, f, 'roda'); um = f['acesa']; habilidade.acende(S, f, 'sanha'); dois_ = f['acesa']
    mult = max((m['mult'] for m in med), default=1); vz = max((m['vezes'] for m in med), default=1); teto = max((m['final'] / m['hoje'] for m in med if m['hoje'] > 0), default=0)
    duplo = sum(1 for c, x, k in xs if k > 0)
    ok = mult <= 1 + TE.PILHA['tecnica'] + 1e-9 and tec_max[0] <= TE.PILHA['tecnica'] + 1e-9 and vz <= TE.DADOS_MAX and teto <= TE.TETO_PILHA + 1e-9 and um == 'roda' and dois_ == 'sanha' and duplo == 0
    return [("HB3 A PILHA: a TÉCNICA nunca acima de +40% (a Roda no topo, o Golpe de Voto e o trunfo juntos, 10.000 golpes); a segunda acesa apaga a primeira; os dados nunca mais de 4 vezes; o dado somado uma vez por golpe (não dobra no crítico); o teto da pilha (×7)",
             f"{golpes} golpes: a TÉCNICA no máximo +{100 * tec_max[0]:.0f}% (o fator da pilha {mult:.2f}); os dados no máximo {vz} vezes; o golpe no máximo {teto:.2f} vezes o de hoje; o dado somado duas vezes num golpe: {duplo}; acender a Sanha com a Roda acesa: fica {dois_}".replace('.', ','), ok)]


# ---------- HB4 O CONTROLE NÃO TRAVA ----------
def hb4(n):
    """HB4 O CONTROLE NÃO TRAVA: o Tranco (o do Mestre e o do Grão-Mestre) e o fecho tranco da Roda no topo, contra o igual e contra o chefe: em cada 3 turnos seguidos, o alvo age em 2"""
    nn = max(300, n // 10); res = []; ok = True
    for nome_, hb, fecho in (('o Tranco do Mestre', dict(tranco=4), None), ('o Tranco do Grão-Mestre', dict(tranco=5), None), ('o fecho tranco da Roda no topo', dict(roda=5, tranco=5), 'tranco')):
        for chefe in (False, True):
            D0 = luta.D; luta.semente(64001 + len(res)); turnos = 0; perd = 0; ruim = 0
            try:
                for _ in range(nn):
                    a = lado('a', hb, 'martelo'); b = lado('b', None, 'martelo', **({'moral': 'firme'} if chefe else {}))
                    S = luta.nova([a], [b], quieto=True, inicio='perto'); S['mede_turnos'] = {}
                    if fecho: luta.por_nome(S, 'a')['fecho_tipo'] = fecho
                    luta.corre(S); t = S['mede_turnos'].get('b', []); turnos += len(t); perd += sum(t)
                    ruim += sum(1 for i in range(len(t) - 2) if sum(t[i:i + 3]) >= 2)
            finally: luta.D = D0
            res.append(f"{nome_} contra {'o chefe' if chefe else 'o igual'}: {100 * perd / max(1, turnos):.0f}% dos turnos perdidos, {ruim} janelas com 2 perdidos")
            ok = ok and ruim == 0
    return [("HB4 O CONTROLE NÃO TRAVA: o Tranco (do Mestre e do Grão-Mestre) e o fecho tranco no topo, contra o igual e contra o chefe: em cada 3 turnos seguidos, o alvo age em 2 (as faixas de EF5)", '; '.join(res), ok)]


# ---------- HB5 O RITMO e HB6 OS FREIOS (o simulador de marcas) ----------
def vida_marcas(rs, dias, lutas_semana=3, durezas=((2, 0.3), (3, 0.5), (4, 0.2)), usa3=0.8, talento=0, k='roda', portas=False, so_d1=False):
    """o simulador do grau: uma vida de `dias` dias com tantas cenas por semana (a marca da cena; um grau por dia; o talento; sem as portas da mão e do feito). Devolve o dia de cada grau."""
    g = 0; m = 0; chegou = {0: 0}; vz = TT.vezes(talento); teto = H.TETO_TALENTO.get(talento, H.GM)
    for dia in range(1, dias + 1):
        if rs.random() < lutas_semana / 7:
            d = 1 if so_d1 else rs.choices([x for x, _ in durezas], [p for _, p in durezas])[0]
            m += habilidade.marca_cena(d, 3 if rs.random() < usa3 else 1, False, k, g)
        if g < min(H.GM, teto) and m >= math.ceil(round(H.MARCAS[g + 1] * vz, 6)): g += 1; chegou[g] = dia
    return chegou, g


def hb5(n):
    """HB5 O RITMO: o simulador de marcas, os perfis de 6.2 (sem as portas da mão e do feito): o aventureiro (3 lutas por semana) chega a Adepto do dia 10 ao 30, a Perito do 40 ao 90,
    a Mestre do 120 ao 220"""
    rs = random.Random(65001); vs = [vida_marcas(rs, 2000)[0] for _ in range(400)]
    med = {g: statistics.median([v.get(g, 9999) for v in vs]) for g in range(1, 6)}
    um = [vida_marcas(rs, 4000, lutas_semana=1)[0] for _ in range(200)]; med1 = {g: statistics.median([v.get(g, 9999) for v in um]) for g in range(1, 6)}
    ok = 10 <= med[2] <= 30 and 40 <= med[3] <= 90 and 120 <= med[4] <= 220
    return [("HB5 O RITMO: o aventureiro (3 lutas por semana; dureza 2, 3 e 4 em 30, 50 e 20% das cenas; usada 3 vezes em 8 de 10): Adepto do dia 10 ao 30, Perito do 40 ao 90, Mestre do 120 ao 220 (sem as portas)",
             'o aventureiro: ' + ' · '.join(f"{H.GRAUS[g]} no dia {med[g]:.0f}" for g in range(1, 6)) + '; quem luta uma vez por semana: ' + ' · '.join(f"{H.CURTO[g]} {med1[g]:.0f}" for g in range(1, 6)), ok)]


def mundo_de_prova():
    """a vila de prova (provas_mundo.vila) com o personagem e um mercador com nome (quem ouve)"""
    import provas_mundo as PM
    E = PM.vila(); at = dict(Força=50, Agilidade=50, Vigor=50, Vontade=50, Percepção=50, Afinidade=50)
    estado.aplica(E, 'gera', [['pessoa', 'nasce', 'otelo', dict(nome='Otelo', nivel=20, atributos=at, lugar='vila', moedas=200, papel='mercador', maestria={'comércio': 4})]], texto='o mercador da prova')
    E['lugares']['vila']['pop'] = 400
    return E


def _mestre(E, ef, txt='a prova'): return estado.aplica(E, 'mestre', ef, texto=txt)


def hb6(n):
    """HB6 OS FREIOS: o farm (só dureza 1) para no Adepto; nunca dois graus num dia; sem a mão ou o feito, não sobe; o Negado para no Adepto (no simulador e no gravador)"""
    rs = random.Random(66001); ok = {}
    ok['farm'] = all(vida_marcas(rs, 2000, lutas_semana=21 / 7 * 7, so_d1=True)[1] == 2 for _ in range(100))
    ok['negado'] = all(vida_marcas(rs, 4000, talento=-2)[1] <= 2 for _ in range(100)) and all(vida_marcas(rs, 6000, talento=-1)[1] <= 4 for _ in range(50))
    E = mundo_de_prova()
    _mestre(E, [['pessoa', 'eu', 'habilidade', 'aprende', dict(chave='roda', origem='legado')], ['pessoa', 'eu', 'hab.roda', 'soma', 600]], 'a Roda de prova')
    um = habilidade.sobe(E, 'eu'); dois = habilidade.sobe(E, 'eu'); g1 = E['gente']['eu']['habilidades']['roda']['grau']
    ok['um_por_dia'] = g1 == 1 and len(um) == 1 and not any('SOBE' in x for x in dois)
    duas = PM_recusa(lambda: estado.aplica(E, 'habilidade', [['pessoa', 'eu', 'hab.roda', 'grau', 2], ['pessoa', 'eu', 'hab.roda', 'grau', 3]], texto='dois graus'))
    ok['dois_no_evento'] = bool(duas)
    for d in range(1, 4):
        _mestre(E, [['relogio', 6]], 'um dia passa'); habilidade.sobe(E, 'eu')
    g = E['gente']['eu']['habilidades']['roda']['grau']
    ok['sem_mao'] = g == 2 and 'falta a mão' in habilidade.falta_para(E, 'eu', 'roda')       # o Perito pede a mão de Iniciante no peso
    _mestre(E, [['pessoa', 'eu', 'maestria.martelo', 'poe', 4], ['relogio', 6]]); habilidade.sobe(E, 'eu'); _mestre(E, [['relogio', 6]]); habilidade.sobe(E, 'eu')
    g = E['gente']['eu']['habilidades']['roda']['grau']
    ok['sem_feito'] = g == 3 and 'falta o feito' in habilidade.falta_para(E, 'eu', 'roda')
    ok['verbo_sem_feito'] = bool(PM_recusa(lambda: estado.aplica(E, 'habilidade', [['pessoa', 'eu', 'hab.roda', 'grau', 4]], texto='sem o feito')))
    ok['mestre_sem_feito'] = bool(PM_recusa(lambda: _mestre(E, [['pessoa', 'eu', 'hab.roda', 'grau', 4]], 'o Mestre sobe sem o feito')))      # o grau do evento do Mestre também é conferido
    # o gravador (9.5): o verbo no tipo de evento dele, a marca de 0 a 6 por cena, um feito por cena
    _mestre(E, [['pessoa', 'eu', 'habilidade', 'aprende', dict(chave='teima', origem='licao')]], 'a Teima de prova')
    ok['marca_no_tipo'] = bool(PM_recusa(lambda: estado.aplica(E, 'compra', [['pessoa', 'eu', 'hab.teima', 'soma', 2]], texto='a marca na compra')))
    ok['marca_ate_6'] = bool(PM_recusa(lambda: estado.aplica(E, 'habilidade', [['pessoa', 'eu', 'hab.teima', 'soma', 500]], texto='500 marcas'))) and \
        bool(PM_recusa(lambda: estado.aplica(E, 'luta', [['pessoa', 'eu', 'hab.teima', 'soma', 4], ['pessoa', 'eu', 'hab.teima', 'soma', 3]], texto='duas marcas na cena')))
    ok['um_feito'] = bool(PM_recusa(lambda: estado.aplica(E, 'luta', [['pessoa', 'eu', 'hab.teima', 'feito', dict(dia=1, como='x')]] * 2, texto='dois feitos'))) and \
        bool(PM_recusa(lambda: estado.aplica(E, 'habilidade', [['pessoa', 'eu', 'hab.teima', 'feito', dict(dia=1, como='x')]], texto='o feito fora da cena')))
    ok['aprende_no_tipo'] = bool(PM_recusa(lambda: estado.aplica(E, 'compra', [['pessoa', 'eu', 'habilidade', 'aprende', dict(chave='brado', origem='licao')]], texto='nasce na compra')))
    ok['marca_na_cena'] = not PM_recusa(lambda: estado.aplica(E, 'luta', [['pessoa', 'eu', 'hab.teima', 'soma', 6]], texto='a marca da luta'))
    ok['estado'] = not estado.valida(E)
    import copy                                             # os invariantes: o Mestre e o Grão-Mestre sem o feito, e acima do teto do talento, o valida pega
    E2 = copy.deepcopy(E); E2['gente']['eu']['habilidades']['teima'].update(grau=3, marcas=999); E2['gente']['eu']['habilidades']['roda'].update(grau=4, marcas=999)
    ok['valida_feito'] = any('pede o feito' in x for x in estado.valida(E2))
    falhas = [k for k, v in ok.items() if not v]
    return [("HB6 OS FREIOS: o farm (só dureza 1) para no Adepto; nunca dois graus num dia (nem dois num evento); sem a mão ou sem o feito, não sobe, nem pelo evento do Mestre (a mesa diz o que falta); o Negado para no Adepto e o Lerdo no Mestre; o gravador recusa o verbo fora do tipo de evento dele, a marca acima de 6 numa cena e o segundo feito; o valida pega o grau sem o feito",
             f"{sum(ok.values())} de {len(ok)} conferências" + (f" (falham: {', '.join(falhas)})" if falhas else '') + f"; a Roda de prova: {habilidade.grau_diz(E['gente']['eu']['habilidades']['roda']['grau'])}, {habilidade.falta_para(E, 'eu', 'roda')}", not falhas)]


def PM_recusa(f):
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()): f()
    except SystemExit as e: return str(e) or 'recusado'
    return None


# ---------- HB7 A FALA, A CONTA e HB8 A ESCOLHA DO JOGADOR ----------
def _exata(c):
    """as faixas pela conta exata do 2d20 que explode (independente da mesa: enumera os dois dados e a explosão até 3 vezes); o duro ofende em toda falha (a Palavra Firme do
    Mestre, só a partir de 5)"""
    um = {}
    for a in range(1, 21):
        if a < 20: um[a] = um.get(a, 0) + 1 / 20
        else:
            for b in range(1, 21):
                if b < 20: um[20 + b] = um.get(20 + b, 0) + 1 / 400
                else:
                    for c_ in range(1, 21): um[40 + c_] = um.get(40 + c_, 0) + 1 / 8000
    s2 = {}
    for x, p in um.items():
        for y, q in um.items(): s2[x + y] = s2.get(x + y, 0) + p * q
    m = lambda lim: sum(p for s, p in s2.items() if s + c['soma'] - c['cd'] >= lim)
    passa = m(0); bem = m(H.FALA_BEM)
    ofende = 0 if c['jeito'] == 'manso' else (1 - m(-(H.FALA_PALAVRA_FIRME - 1)) if c.get('pf') else 1 - passa) if c['jeito'] == 'duro' else 1 - m(-H.FALA_OFENDE + 1)
    return dict(bem=bem, preco=passa - bem, nao=1 - passa - ofende, ofende=ofende, passa=passa)


def _margem(m):
    """o teste.rola de prova que dá a margem pedida (a faixa conferida sem o acaso): o dado de verdade rola, e o total é posto"""
    orig = teste.rola
    def r(E, o_que, atributo, contra, mais=0, quem=None, **k):
        x = orig(E, o_que, atributo, contra, mais=mais, quem=quem, **k); x['total'] = contra + m; x['passou'] = m >= 0; return x
    return orig, r


def _pede(E, deg, o_que, jeito='firme', margem=None, ouvinte='otelo', **kw):
    """o pedido de prova, nos dois passos da resposta 5a (a conta à mesa, e depois o dado); com `margem`, a faixa sai sem o acaso"""
    quieto(fala.conta_pedido, E, 'eu', ouvinte, deg, jeito)
    if margem is None: return quieto(fala.pede, E, 'eu', ouvinte, deg, o_que, jeito, **kw)
    orig, r = _margem(margem); teste.rola = r
    try: return quieto(fala.pede, E, 'eu', ouvinte, deg, o_que, jeito, **kw)
    finally: teste.rola = orig


def hb7(n):
    """HB7 A FALA, A CONTA: a chance da mesa contra a exata (o firme e o duro); 400 rolagens com o teste.rola nas faixas a 4 desvios; o manso nunca ofende; o duro que falha ofende
    sempre (a Palavra Firme do Mestre salva quem falha por menos de 5); a memória só pelas faixas, uma linha por conversa, SOMANDO as falas do dia; o "não" vale no dia; as
    habilidades de fala até +8; nenhum dado de fala do personagem sem o `fala.py pede`, e o pede só depois da conta mostrada (a resposta 5a)"""
    E = mundo_de_prova(); ok = {}; L_ = []
    for deg in H.FALA_ORDEM:
        c = fala.conta(E, 'eu', 'otelo', deg); x = _exata(c); cd = fala.conta(E, 'eu', 'otelo', deg, 'duro'); xd = _exata(cd)
        ok[f'exata_{deg}'] = all(abs(c[k] - x[k]) < 0.005 for k in ('bem', 'preco', 'nao', 'ofende')) and all(abs(cd[k] - xd[k]) < 0.005 for k in ('bem', 'preco', 'nao', 'ofende'))
        L_.append(f"{H.FALA_DIZ[deg]} passa {fala._pct(c['passa'])} (exata {fala._pct(x['passa'])}; duro: passa {fala._pct(cd['passa'])}, ofende {fala._pct(cd['ofende'])})")
    c = fala.conta(E, 'eu', 'otelo', 'pequeno'); conta_ = dict(bem=0, preco=0, nao=0, ofende=0); man = 0; nn = 400
    for i in range(nn):
        r = teste.rola(E, 'a prova da fala', c['atributo'], c['cd'], mais=c['mais'], quem='eu'); conta_[fala._faixa(r['total'] - r['contra'], 'firme')] += 1
        rm = teste.rola(E, 'a prova do manso', 'Vontade', c['cd'] - 4, mais=c['mais'], quem='eu'); man += fala._faixa(rm['total'] - rm['contra'], 'manso') == 'ofende'
    E['turno']['dados'].clear()
    for k in conta_:
        p = c[k]; sd = math.sqrt(max(p * (1 - p), 1e-9) / nn); ok[f'rola_{k}'] = abs(conta_[k] / nn - p) <= 4 * sd + 1e-9
    ok['manso'] = man == 0
    # o 2º passo sem o 1º: recusado (a resposta 5a: a chance à mesa antes do dado)
    d0 = len(E['turno']['dados'])
    ok['conta_antes'] = bool(PM_recusa(lambda: fala.pede(E, 'eu', 'otelo', 'pequeno', 'sem mostrar'))) and len(E['turno']['dados']) == d0
    # o duro que falha ofende sempre; a memória soma na linha do dia (o manso ganho, +1; o duro que ofende, −3: fica −2, numa linha só)
    R1, _ = _pede(E, 'pequeno', 'um favor', 'manso', margem=8)
    R2, _ = _pede(E, 'grande', 'um favor grande', 'duro', margem=-3)
    linhas = [m for m in E['gente']['otelo'].get('memoria') or [] if m.get('de') == 'eu' and m.get('dia') == E['relogio']['dia']]
    import gente
    ok['duro_ofende'] = R1['faixa'] == 'bem' and R2['faixa'] == 'ofende'
    ok['uma_linha_soma'] = len(linhas) == 1 and linhas[0]['peso'] == -2 and gente.opiniao(E, 'otelo', 'eu')[0] == -2
    ok['ofendido_nao_ouve'] = bool(PM_recusa(lambda: fala.conta_pedido(E, 'eu', 'otelo', 'medio')))
    _mestre(E, [['relogio', 6]], 'um dia passa')
    # o "não" vale no dia: o mesmo degrau ou menor, recusado; o maior, pode
    R3, _ = _pede(E, 'medio', 'um empréstimo', 'firme', margem=-3)
    ok['nao_no_dia'] = R3['faixa'] == 'nao' and bool(PM_recusa(lambda: fala.conta_pedido(E, 'eu', 'otelo', 'pequeno'))) and not PM_recusa(lambda: fala.conta_pedido(E, 'eu', 'otelo', 'grande'))
    E['turno'].pop('fala_vista', None)
    # a Palavra Firme do Mestre: o duro que falha por menos de 5 não ofende; por 5 ou mais, ofende
    _mestre(E, [['pessoa', 'eu', 'habilidade', 'aprende', dict(chave='palavra_firme', origem='classe:Medianeiro', grau=4, feitos=[dict(dia=1, como='a prova')])], ['relogio', 6]])
    fx = []
    for mg in (-1, -4, -5, -12):
        _mestre(E, [['relogio', 6], ['pessoa', 'otelo', 'memoria', 'poe', []]], 'um dia passa (e Otelo esquece: cada caso parte da opinião 0)'); R_, _ = _pede(E, 'pequeno', f'o duro {mg}', 'duro', margem=mg); fx.append(R_['faixa'])
    ok['palavra_firme'] = fx == ['nao', 'nao', 'ofende', 'ofende']
    cpf = fala.conta(E, 'eu', 'otelo', 'pequeno', 'duro'); ok['palavra_firme_conta'] = abs(cpf['ofende'] - _exata(cpf)['ofende']) < 0.005
    _mestre(E, [['pessoa', 'eu', 'habilidade', 'aprende', dict(chave='fio_conversa', origem='classe:Pregoeiro', grau=5, feitos=[dict(dia=1, como='a prova')] * 2)],
                ['pessoa', 'eu', 'habilidade', 'aprende', dict(chave='ameaca_surda', origem='classe:Cinza', grau=5, feitos=[dict(dia=1, como='a prova')] * 2)],
                ['pessoa', 'eu', 'marca.fio', 'poe', dict(lugar='vila', dia=E['relogio']['dia'], n=3)]])
    c8 = fala.conta(E, 'eu', 'otelo', 'pequeno', 'duro', ameaca=True, mais_hab=(5, 'a Língua de Feira +5'))
    ok['teto_8'] = c8['hab'] == H.FALA_HAB_TETO
    d0 = len(E['turno']['dados'])
    for i in range(50): quieto(fala.da_gente, E, 'otelo', 'pequeno', 'vender o sal mais caro')
    ok['so_pede'] = not any(r['quem'] == 'eu' for r in E['turno']['dados'][d0:])
    ok['estado'] = not estado.valida(E)
    falhas = [k for k, v in ok.items() if not v]
    return [("HB7 A FALA, A CONTA: a chance da mesa contra a exata (o firme e o duro); 400 rolagens com o teste.rola nas faixas a 4 desvios; o manso nunca ofende; o duro que falha ofende sempre (a Palavra Firme do Mestre salva quem falha por menos de 5); a memória só pelas faixas, uma linha por conversa, somando; o \"não\" vale no dia; as habilidades de fala até +8; nenhum dado de fala do personagem sem o fala.py pede, e o pede só depois da conta mostrada",
             f"Ferord-de-prova (Vontade 50, opinião 0) a quem ouve com Vontade 50: {' · '.join(L_)}; 400 rolagens do pequeno: bem {conta_['bem']}, com preço {conta_['preco']}, não {conta_['nao']}, ofende {conta_['ofende']} "
             f"(a conta: {100 * c['bem']:.0f}/{100 * c['preco']:.0f}/{100 * c['nao']:.0f}/{100 * c['ofende']:.0f}%); o manso ofendeu {man} vezes; a Palavra Firme do Mestre no duro que falha por 1, 4, 5 e 12: {', '.join(fx)}; {sum(ok.values())} de {len(ok)} conferências" + (f" (falham: {', '.join(falhas)})" if falhas else ''), not falhas)]


def hb8(n):
    """HB8 A ESCOLHA DO JOGADOR: 200 falas da gente no personagem: nenhuma muda o estado dele sem a resposta; a mesa sempre diz o preço de recusar"""
    E = mundo_de_prova(); antes = json.dumps(E['gente']['eu'], sort_keys=True); diz = 0; passou = 0
    for i in range(200):
        R_, txt = quieto(fala.da_gente, E, 'otelo', H.FALA_ORDEM[i % 4], f'o pedido {i}')
        diz += 'recusar' in txt; passou += R_['passou']
        E['turno']['perguntas'].clear()
    depois = json.dumps(E['gente']['eu'], sort_keys=True)
    return [("HB8 A ESCOLHA DO JOGADOR: 200 falas da gente no personagem: nenhuma muda o estado dele sem a resposta; a mesa sempre diz o preço de recusar",
             f"200 falas ({passou} convenceram): o personagem {'não mudou' if antes == depois else 'MUDOU'}; o preço de recusar dito em {diz} de 200", antes == depois and diz == 200)]


# ---------- HB9 A MINA ----------
def hb9(n):
    """HB9 A MINA: FORJAR PARA A LOJA com a Língua de Feira no Grão-Mestre (o ferreiro de loja do provas_mercado regateia uma vez por loja por dia, antes de vender): as faixas de hoje"""
    import provas_mercado as PMe, mercado
    orig = mercado.vender_peca; orig_cria = None
    import vila_teste
    orig_cria = vila_teste.cria
    def cria(*a, **k):
        E = orig_cria(*a, **k)
        estado.aplica(E, 'mestre', [['pessoa', 'eu', 'habilidade', 'aprende', dict(chave='lingua', origem='classe:Tropeiro', grau=5, feitos=[dict(dia=1, como='a prova')] * 2)]], texto='a Língua de Feira no topo')
        return E
    def vende(E, pid, iid):
        lid = E['gente'][pid]['lugar']
        if ((E['gente'][pid].get('marca') or {}).get('regateio_dia') or {}).get(lid) != E['relogio']['dia']:
            if not PM_recusa(lambda: fala.regateia(E, pid, iid, 2, so_conta=True)): PM_recusa(lambda: fala.regateia(E, pid, iid, 2))      # os dois passos (a resposta 5a)
        return orig(E, pid, iid)
    mercado.vender_peca = vende; vila_teste.cria = cria
    try:
        sementes = max(PMe.MINA_SEMENTES, n // 400); media = lambda X: sum(X) / len(X)
        Rr = {nome_: [quieto(PMe.ferreiro_de_loja, s, cats) for s in range(1, sementes + 1)] for nome_, cats in (('só peças Comuns', (0,)), ('Comuns e Incomuns', (0, 1)))}
    finally: mercado.vender_peca = orig; vila_teste.cria = orig_cria
    m5 = {k: media([V['rende'][0] for V in vs]) for k, vs in Rr.items()}; p5 = {k: max(V['rende'][0] for V in vs) for k, vs in Rr.items()}; m30 = {k: media([V['rende'][1] for V in vs]) for k, vs in Rr.items()}
    todas = [V for vs in Rr.values() for V in vs]; fecha = all(V['prata'] and V['inteiro'] and V['vivo'] for V in todas)
    certo = max(m5.values()) <= PMe.MINA_COMECO[0] and max(p5.values()) <= PMe.MINA_COMECO[1] and max(m30.values()) <= PMe.MINA_DEPOIS and fecha
    return [(f"HB9 A MINA: FORJAR PARA A LOJA NÃO É MINA com a Língua de Feira no Grão-Mestre (regateia uma vez por loja por dia, antes de vender): nos {PMe.MINA_DIAS[0]} primeiros dias, em média no máximo {PMe.MINA_COMECO[0]} por dia e no pior {PMe.MINA_COMECO[1]}; depois, no máximo {PMe.MINA_DEPOIS}",
             f"{sementes} vilas por escada. " + ' · '.join(f"{k}: {m5[k]:.2f} por dia (o pior {p5[k]:.2f}), {m30[k]:.2f} depois".replace('.', ',') for k in Rr) + f"; a prata {'fecha' if fecha else 'NÃO FECHA'}", certo)]


# ---------- HB10 A FORJA (e o B2) ----------
def hb10(n):
    """HB10 A FORJA: a chance de cada categoria com as habilidades de trabalho ligadas (o prumo de todas as fontes até 5, a têmpera até 3) igual à do oficio.dist_valor (diferença 0, o B2);
    cada uma dentro do teto de feitio da força do grau (fraco 0,15 · normal 0,30 · forte 0,60), na média dos cinco ferreiros (a régua da FJ7)"""
    import oficio, tabelas_oficio as O, provas_oficio as PO
    dif = 0.0; casos = 0
    for soma in range(-10, 201, 3):
        for teto in range(0, 6):
            ref = oficio.dist_valor(soma, teto)
            for pr, tp in ((5, 0), (3, 3), (5, 3), (2, 1)):
                d = oficio.dist_efeitos(soma, teto, prumo=pr, tempera=tp); cat = {}
                for k, q in d.items(): cat[k[0]] = cat.get(k[0], 0) + q
                dif = max(dif, max(abs(cat.get(c, 0) - ref.get(c, 0)) for c in set(cat) | set(ref))); casos += 1
    base = {x[0]: PO._feitio(oficio.dist_efeitos(x[1], x[2], x[3])) for x in PO.REF}
    def ganho(**kw): g = [PO._feitio(oficio.dist_efeitos(s, t, fc, **kw)) - base[nm] for nm, s, t, fc, oc in PO.REF]; return sum(g) / len(g)
    def ganho_teto(tp):                     # a Têmpera Certa do Iniciante e do Aprendiz: só na peça que sai no teto
        g = []
        for nm, s, t, fc, oc in PO.REF:
            d0 = oficio.dist_efeitos(s, t, fc); d1 = oficio.dist_efeitos(s, t, fc, tempera=tp)
            f0 = sum((k[1] + k[2] / 2) * q for k, q in d0.items() if k[0] is not None and k[0] != t); f1 = sum((k[1] + k[2] / 2) * q for k, q in d1.items() if k[0] == t)
            g.append(f0 + f1 - base[nm])
        return sum(g) / len(g)
    linhas = []; dentro = True
    for k in ('malho_quente', 'paciencia', 'brio', 'tempera_certa'):
        vs = []
        for g in range(6):
            if k == 'malho_quente': v = ganho(prumo=H.num(k, 'calor', g) // H.MALHO_PRUMO)
            elif k in ('paciencia', 'brio'): v = ganho(prumo=H.num(k, 'prumo', g))
            else: v = ganho_teto(H.num(k, 'cheios', g)) if H.num(k, 'so_teto', g) else ganho(tempera=H.num(k, 'cheios', g))
            teto = O.FORCA_FEITIO[H.forca_do_grau(k, g)]             # a força que o grau deixa (6.2), nunca acima da dela (o teto da habilidade)
            dentro = dentro and v <= teto + 1e-9 and v >= -1e-9; vs.append(v)
        linhas.append(f"{nome(k)}: " + ' · '.join(f"{v:+.2f}" for v in vs).replace('.', ','))
    return [("HB10 A FORJA: com as de trabalho ligadas (o prumo até 5, a têmpera até 3), a chance de cada categoria igual à do dist_valor (B2: diferença até 1e−12); cada uma, grau a grau, no teto de feitio da força do grau (fraco 0,15 · normal 0,30 · forte 0,60; a média dos cinco ferreiros)",
             f"{casos} casos: a diferença máxima {dif:.1e}; a régua de feitio por grau (I·Ap·Ad·P·M·GM): {'; '.join(linhas)}", dif <= 1e-12 and dentro)]


# ---------- HB11 COPIAR E O ESTALO ----------
def hb11(n):
    """HB11 COPIAR E O ESTALO: a chance de colher o jeito de 5 a 90%; três tentativas e fecha; a cópia para no Mestre; o estalo em 4 a 8% das lutas (dureza 2 e 3), nunca dois na mesma semana"""
    E = mundo_de_prova(); ok = {}; p = E['gente']['eu']
    chs = []
    for mao in (0, 2, 4, 6, 8):
        for k in ('teima', 'riposta', 'sanha'):
            for cj in (None, 0, 5):
                q = dict(p, maestria={'espada': mao}, habilidades=({'colher_jeito': {'grau': cj}} if cj is not None else {})); chs.append(habilidade.chance_copia(q, k))
    ok['faixa'] = min(chs) >= 0.05 - 1e-9 and max(chs) <= 0.90 + 1e-9
    _mestre(E, [['pessoa', 'eu', 'copia.teima', 'soma', 1]] * 3)
    ok['tres'] = bool(PM_recusa(lambda: _mestre(E, [['pessoa', 'eu', 'copia.teima', 'soma', 1]])))
    _mestre(E, [['pessoa', 'eu', 'habilidade', 'aprende', dict(chave='riposta', origem='copia')], ['pessoa', 'eu', 'hab.riposta', 'soma', 600], ['pessoa', 'eu', 'maestria.espada', 'poe', 8]])
    ok['para_no_mestre'] = habilidade.teto_de(E['gente']['eu'], 'riposta') == 4 and bool(PM_recusa(lambda: _mestre(E, [['pessoa', 'eu', 'hab.riposta', 'grau', 5]])))
    ok['apelao'] = bool(PM_recusa(lambda: _mestre(E, [['pessoa', 'eu', 'habilidade', 'aprende', dict(chave='roda', origem='copia')]])))
    _mestre(E, [['pessoa', 'eu', 'habilidade', 'esquece', 'riposta']])
    S = luta.nova([lado('eu', None, 'espada')], [lado('x', None, 'espada')], quieto=True); f = luta.por_nome(S, 'eu'); f['id'] = 'eu'; S['usadas'] = [f['arma']['item']]
    estalos = []; rolou = 0; nn = 1000; primeiro = None; G0 = teste.GERADOR_CEM; teste.GERADOR_CEM = random.Random(69001)      # (o banco) o dado de cem com semente fixa: a meta reproduzível
    try:
        while rolou < nn:                                   # uma luta por dia; conta só as lutas em que o estalo pode sair (fora da trava da semana: a rolagem acontece)
            S['dureza'] = dict(A=3 if rolou % 2 else 2, B=3); d0 = len(E['turno']['dados'])
            ef, frase, so_m = habilidade.estalo(E, S, f, 'eu')
            rolou += len(E['turno']['dados']) - d0
            if ef:
                novas = [x[4]['chave'] for x in ef if x[2] == 'habilidade']; estalos.append(E['relogio']['dia'])
                if primeiro is None: primeiro = novas
                _mestre(E, ef, 'o estalo de prova'); _mestre(E, [['pessoa', 'eu', 'habilidade', 'esquece', k] for k in novas])
            _mestre(E, [['relogio', 6]], 'um dia'); E['turno']['dados'].clear(); E['_novos'].clear()
    finally: teste.GERADOR_CEM = G0
    taxa = len(estalos) / max(1, rolou); semana = all(b - a >= H.ESTALO_SEMANA for a, b in zip(estalos, estalos[1:]))
    ok['estalo'] = 0.04 <= taxa <= 0.08; ok['semana'] = semana and bool(estalos)
    ok['olho_no_primeiro'] = bool(primeiro) and 'olho_luta' in primeiro
    # o estalo da gente do mundo é segredo (6.4): à mesa, no máximo "algo acendeu em X", sem o nome; o nome vai ao SÓ O MESTRE
    E2 = mundo_de_prova(); _mestre(E2, [['pessoa', 'nasce', 'zeca', dict(nome='Zeca', nivel=20, atributos=dict(Força=50, Agilidade=50, Vigor=50, Vontade=50, Percepção=50, Afinidade=50), lugar='vila', moedas=0, papel='guarda', maestria={'espada': 4})]])
    S2 = luta.nova([lado('eu', None, 'espada'), lado('Zeca', None, 'espada')], [lado('x', None, 'espada')], quieto=True); g_ = luta.por_nome(S2, 'Zeca'); g_['id'] = 'zeca'
    luta.por_nome(S2, 'eu')['id'] = 'eu'; S2['usadas'] = [g_['arma']['item']]; S2['dureza'] = dict(A=3, B=3); sec = None; G0 = teste.GERADOR_CEM; teste.GERADOR_CEM = random.Random(69002)
    try:
        for _ in range(400):
            ef2, mesa2, so2 = habilidade.estalo(E2, S2, g_, 'zeca')
            if ef2: sec = (ef2, mesa2, so2); break
            _mestre(E2, [['relogio', 6]], 'um dia')
    finally: teste.GERADOR_CEM = G0
    ok['segredo'] = bool(sec) and not any(habilidade.nome(x[4]['chave']).lower() in sec[1].lower() for x in sec[0] if x[2] == 'habilidade') and 'só o Mestre' in sec[2] and 'Zeca' in sec[1]
    # o LEGADO (6.5): a peça de um mestre morto usada em 5 lutas de verdade ensina a técnica dela (do legado: até o Grão-Mestre), no evento da luta; quem já a tem por origem
    # igual ou maior (a classe), não (e a luta não é recusada por isso); o legado com técnica que não nasce de legado é recusado no item
    E3 = mundo_de_prova(); arma = next(i for i, it in E3['itens']['itens'].items() if it.get('dono') == 'eu' and it.get('uso') == 'arma')
    ok['legado_item'] = bool(PM_recusa(lambda: _mestre(E3, [['item', arma, 'legado', 'poe', dict(tecnica='sanha', de='o velho Bramo')]])))
    _mestre(E3, [['item', arma, 'legado', 'poe', dict(tecnica='roda', de='o velho Bramo')]], 'a peça do mestre morto')
    Sx = dict(mundo=True, usadas=[arma]); fx = dict(estado='pe'); antes = []
    for i in range(H.LEGADO_LUTAS):
        antes.append('roda' in (E3['gente']['eu'].get('habilidades') or {}))
        estado.aplica(E3, 'luta', habilidade.legado_luta(E3, Sx, fx, 'eu'), texto=f'a luta {i + 1} com a peça do mestre')
    rg = (E3['gente']['eu'].get('habilidades') or {}).get('roda') or {}
    ok['legado'] = not any(antes) and str(rg.get('origem', '')).startswith('legado') and bool(Sx.get('hab_mesa')) and not estado.valida(E3)
    _mestre(E3, [['pessoa', 'eu', 'habilidade', 'esquece', 'roda'], ['pessoa', 'eu', 'habilidade', 'aprende', dict(chave='roda', origem='classe:Malhador')]], 'a Roda da classe')
    ef3 = habilidade.legado_luta(E3, Sx, fx, 'eu')
    ok['legado_classe'] = not any(x[2] == 'habilidade' for x in ef3) and not PM_recusa(lambda: estado.aplica(E3, 'luta', ef3, texto='mais uma luta com a peça'))
    ok['estado'] = not estado.valida(E)
    falhas = [k for k, v in ok.items() if not v]
    return [("HB11 COPIAR E O ESTALO (E O LEGADO): a chance de colher o jeito de 5 a 90%; três tentativas e fecha; a cópia para no Mestre (e o apelão não se copia); o estalo em 4 a 8% das lutas de verdade em que pode sair (dureza 2 e 3), nunca dois na mesma semana; o primeiro estalo traz o Olho de Luta; o estalo da gente do mundo só no SÓ O MESTRE; a peça do legado ensina na 5ª luta de verdade (e não a quem já tem a técnica por origem igual ou maior)",
             f"a chance de 5 a 90%: de {100 * min(chs):.0f}% a {100 * max(chs):.0f}%; o estalo em {f'{100 * taxa:.1f}'.replace('.', ',')}% de {rolou} lutas em que podia sair (a conta: 6%, metade com dureza 2 e metade com 3; o dado de cem com semente fixa), {len(estalos)} estalos, {'nunca' if semana else 'DOIS'} na mesma semana; o primeiro trouxe {', '.join(habilidade.nome(k) for k in (primeiro or []))}; {sum(ok.values())} de {len(ok)} conferências" + (f" (falham: {', '.join(falhas)})" if falhas else ''), not falhas)]


# ---------- HB12 A MESA E A ORDEM ----------
def hb12(n):
    """HB12 A MESA E A ORDEM: a linha (grau, marcas, a de luta), o quadro (batidas, pontos, trunfos), a ordem errada recusada antes do dado com a frase, o trunfo nunca para a luta"""
    E = mundo_de_prova(); ok = {}
    _mestre(E, [['pessoa', 'eu', 'habilidade', 'aprende', dict(chave='sanha', origem='mestre')], ['pessoa', 'eu', 'habilidade', 'aprende', dict(chave='malho_quente', origem='licao')], ['pessoa', 'eu', 'hab.sanha', 'soma', 4]])
    lin = habilidade.mao(E, 'eu'); ok['linha'] = 'Iniciante' in lin and 'marcas' in lin and 'de luta' in lin and 'vagas' in lin
    luta.semente(67001)
    a = lado('Aldric', dict(roda=3, trunfos=3, sanha=2), 'martelo', controla=True); b = lado('Bruto', dict(sanha=3), 'espada')
    S = luta.nova([a], [b], inicio='colado'); S['comecou'] = True
    erradas = ['Aldric: fazer riposta', 'Aldric: fazer brado', 'Aldric: fazer sanha defensiva', 'Aldric: trunfo=ameaca', 'Aldric: fazer voo', 'Aldric: atacar Bruto bigorna']
    log0 = list(S['log']); st0 = luta.D.r.getstate(); frases = [PM_recusa(lambda o=o: luta.ordem(S, o)) for o in erradas]
    ok['recusa'] = all(frases) and luta.D.r.getstate() == st0 and S['log'] == log0
    luta.ordem(S, 'Aldric: fazer roda em Bruto'); luta.ordem(S, 'Aldric: trunfo=tranco se carga>=6, senão dano')
    paradas = []
    while luta.corre(S, interativo=True) == 'parada':
        paradas += S['paradas']
        if S['r'] >= 2 and 'Roda' in luta.situacao(S): ok['quadro'] = True
        if S['fim']: break
    paradas += S['paradas']; q = luta.situacao(S)
    ok.setdefault('quadro', 'batidas' in q or 'trunfos' in q)
    ok['trunfo_nao_para'] = not any('trunfo' in x and 'acabaram' not in x for x in paradas)
    ok.update(_hb12_ordem())
    falhas = [k for k, v in ok.items() if not v]
    return [("HB12 A MESA E A ORDEM: a linha mostra grau, marcas e a de luta; o quadro mostra batidas, pontos e trunfos; a ordem errada é recusada antes do dado, com a frase (também os trunfos acabados e a Sanha, acesa ou armada, com a postura defensiva ou a bigorna); o trunfo nunca para a luta; refazer a Roda não zera as batidas; o Sopro de Volta é de dia (duas lutas no mesmo dia); a Guarda de Bigorna conta o uso (e toda habilidade do duelo, usada, conta o uso); o `fazer mira sempre` mira e atira até a ordem mudar; o Golpe de Voto de quem o jogador comanda só com a ordem; a Mão que Estanca do Mestre firma o caído e a do Grão-Mestre o levanta",
             f"a linha: «{lin[:150]}…»; as recusas: «{(frases[0] or '')[:70]}» · «{(frases[2] or '')[:70]}»; {sum(ok.values())} de {len(ok)} conferências" + (f" (falham: {', '.join(falhas)})" if falhas else ''), not falhas)]


def _hb12_ordem():
    """as conferências novas da HB12 (o conserto da fase 2): cada uma numa luta pequena, sem dado de verdade (as recusas vêm antes do dado)"""
    ok = {}
    def luta_de(ha, hb_=None, fa='martelo', fb='espada', **kw):
        a = lado('Aldric', ha, fa, controla=True); b = lado('Bruto', hb_, fb, **kw); S = luta.nova([a], [b], inicio='colado', quieto=True); S['comecou'] = True
        return S, luta.por_nome(S, 'Aldric')
    S, f = luta_de(dict(trunfos=3)); f['trunfos'][0] = 0
    ok['trunfos_acabados'] = bool(PM_recusa(lambda: luta.ordem(S, 'Aldric: trunfo=dano'))) and not PM_recusa(lambda: luta.ordem(S, 'Aldric: trunfo=nao'))
    S, f = luta_de(dict(sanha=3, bigorna=3), fa='espada'); habilidade.acende(S, f, 'sanha')
    ok['sanha_postura'] = all(PM_recusa(lambda o=o: luta.ordem(S, o)) for o in ('Aldric: atacar Bruto defensiva', 'Aldric: atacar Bruto bigorna', 'Aldric: segurar defensiva'))
    S, f = luta_de(dict(sanha=3, bigorna=3), fa='espada'); luta.ordem(S, 'Aldric: fazer sanha')
    ok['sanha_armada'] = bool(PM_recusa(lambda: luta.ordem(S, 'Aldric: atacar Bruto bigorna')))
    S, f = luta_de(dict(roda=5)); luta.ordem(S, 'Aldric: fazer roda em Bruto'); f['batidas'] = 5; f['roda_entrou'] = True
    luta.ordem(S, 'Aldric: fazer roda em Bruto fecho=tranco')
    ok['roda_refeita'] = f['batidas'] == 5 and f['roda_entrou'] and f['fecho_tipo'] == 'tranco'
    E = mundo_de_prova()                                    # o Sopro de Volta é de dia: gasto numa luta de hoje, a luta seguinte do mesmo dia não o tem
    _mestre(E, [['pessoa', 'eu', 'habilidade', 'aprende', dict(chave='sopro_volta', origem='classe:Sangrador', grau=2)], ['pessoa', 'eu', 'hab.sopro_volta', 'usada', E['relogio']['dia']]])
    d = estado.lutador(E, 'eu'); S = luta.nova([d, lado('Ali', None, 'espada')], [lado('B', None, 'espada')], quieto=True); f = luta.por_nome(S, d['nome'])
    x = luta.por_nome(S, 'Ali'); x['estado'] = 'caido'; x['caiu_r'] = 1; x['x'] = f['x']
    ok['sopro_de_dia'] = 'sopro_volta' in f['hab_dia'] and habilidade.decide(S, f, {}, False) is None
    luta.semente(67011); S, f = luta_de(None, dict(bigorna=3), fb='espada'); S['quieto'] = True; luta.corre(S)
    ok['bigorna_usos'] = (luta.por_nome(S, 'Bruto').get('hab_usos') or {}).get('bigorna', 0) > 0
    import provas
    luta.semente(67012); gastos = []
    for ordem in (None, 'fazer voto sempre'):               # o Golpe de Voto de quem o jogador comanda: sem a ordem, nunca gasta a Mana; com ela, gasta
        c = provas.clerigo('Aldric', habilidades={'golpe_voto': 3}, controla=True); S = luta.nova([c], [lado('Bruto', None, 'espada')], inicio='colado', quieto=True); S['comecou'] = True
        luta.ordem(S, 'Aldric: atacar Bruto'); f = luta.por_nome(S, 'Aldric')
        if ordem: luta.ordem(S, f'Aldric: {ordem}')
        for _ in range(4):
            if S['fim'] or luta.corre(S, interativo=True) != 'parada': break
        gastos.append((f.get('hab_usos') or {}).get('golpe_voto', 0))
    ok['voto_ordem'] = gastos[0] == 0 and gastos[1] > 0
    luta.semente(67013); sem_uso = []                    # cada habilidade de luta do duelo, usada pelo robô, conta o uso (a marca e o grau vêm dele: 6.2)
    for k, fam in DUELO.items():
        for _ in range(3):
            S = luta.nova([lado('a', {k: 3}, fam)], [lado('b', None, fam)], quieto=True); luta.corre(S)
            if (luta.por_nome(S, 'a').get('hab_usos') or {}).get(k, 0) > 0: break
        else: sem_uso.append(k)
    ok['usos_contam'] = not sem_uso
    luta.semente(67014); miras = []                      # `fazer mira` sem `sempre` mira uma vez; com `sempre`, mira e atira até a ordem mudar (6.4)
    for ordem in ('fazer mira', 'fazer mira sempre'):
        S = luta.nova([lado('Aldric', dict(mira_firme=2), 'arco', controla=True, molde='arqueiro')], [lado('Bruto', None, 'espada')], inicio='longe', quieto=True); S['comecou'] = True
        luta.ordem(S, 'Aldric: atacar Bruto'); luta.ordem(S, f'Aldric: {ordem}'); f = luta.por_nome(S, 'Aldric')
        for _ in range(8):
            if S['fim'] or luta.corre(S, interativo=True) != 'parada': break
        miras.append((f.get('hab_feitas') or []).count('mira_firme'))          # as vezes que mirou (a ação)
    ok['mira_sempre'] = miras[0] == 1 and miras[1] >= 2
    for gr, quer in ((4, 'firma'), (5, 'levanta')):           # a Mão que Estanca: do Mestre, o caído colado fica firme; no Grão-Mestre, levanta
        S = luta.nova([lado('Aldric', dict(estanca=gr), 'espada', controla=True), lado('Ali', None, 'espada')], [lado('Bruto', None, 'espada')], inicio='longe', quieto=True); S['comecou'] = True
        f = luta.por_nome(S, 'Aldric'); x = luta.por_nome(S, 'Ali'); x['estado'] = 'caido'; x['pv'] = 0; x['x'] = f['x']; x['morte'] = [0, 1]
        luta.ordem(S, 'Aldric: atar Ali'); ac = luta._decide(S, f, False); luta._ata(S, f, ac[1])
        ok[f'estanca_{quer}'] = (x['morte'][0] >= 3 and x['estado'] == 'caido') if quer == 'firma' else (x['estado'] == 'pe' and x['pv'] > 0)
    return ok


# ---------- HB13 LANÇAR ----------
def hb13(n):
    """HB13 LANÇAR: A Corrente, A Mão no Rito e A Mana Curta no mago contra mago (o do banco, de longe), por grau: na força do grau (6.2) e no teto delas (A Corrente forte; as outras
    normal); a Conjuração no teto de +8"""
    import provas, magia
    nn = max(1000, n // 4); linhas = []; dentro = True
    for k in ('corrente', 'mao_rito', 'mana_curta'):
        vs = []
        for g in range(6):
            sabe = ('seta', 'lança-de-fogo', 'raio', 'escudo')
            com = lambda: [provas.mago('a', sabe=sabe, habilidades={k: g})]; sem = lambda: [provas.mago('a', sabe=sabe)]; contra = lambda: [provas.mago('b', sabe=sabe)]
            v = delta(com, sem, contra, nn, 68001 + 10 * g + len(linhas) * 100, inicio='longe'); vs.append(v)
            dentro = dentro and v <= H.pontos_do_grau(k, g) + FOLGA
        linhas.append(f"{nome(k)}: " + ' · '.join(_f(v) for v in vs))
    m = provas.mago('a', sabe=('seta',), habilidades={'corrente': 5}); S = luta.nova([m], [provas.mago('b')], quieto=True); f = luta.por_nome(S, 'a')
    c0 = magia.conj(S, f, 'seta')[0]; f['corrente'] = 6; c1 = magia.conj(S, f, 'seta')[0]
    teto = c1 - c0 <= TE.FIXO_TETO
    return [("HB13 LANÇAR: A Corrente, A Mão no Rito e A Mana Curta no mago contra mago (de longe), por grau, na força do grau e no teto delas (a Corrente forte; as outras normal); a Conjuração no teto de +8",
             f"{'; '.join(linhas)} (a vitória com ela − sem ela, {nn} lutas por linha); a Corrente cheia soma {c1 - c0:g} na Conjuração", dentro and teto)]


# ---------- B0 ----------
def b0(n):
    """B0 A LUTA DE SEMPRE (fase 2): as lutas de hoje, sem habilidade (gente, bichos e magia, ao acaso, com semente fixa), no motor de antes da fase 2 (B0_REF) e no de agora,
    com a escada do medo LIGADA (ela é a regra de hoje desde a 1b): iguais, dado por dado"""
    import provas
    aqui = os.path.dirname(os.path.abspath(__file__)); k = max(200, n // 40); tmp = tempfile.mkdtemp(prefix='m10_b0f2_')
    try:
        raiz = subprocess.run(['git', 'rev-parse', '--show-toplevel'], cwd=aqui, capture_output=True, text=True).stdout.strip()
        arq = subprocess.run(['git', 'archive', B0_REF, 'motor10'], cwd=raiz, capture_output=True)
        if arq.returncode or not raiz: return [('B0 A LUTA DE SEMPRE (fase 2)', f'sem o motor de antes no git ({B0_REF}): não conferido', False)]
        subprocess.run(['tar', '-x', '-C', tmp], input=arq.stdout, check=True)
        script = os.path.join(tmp, 'b0_lutas.py'); open(script, 'w', encoding='utf-8').write(provas._B0_SCRIPT.replace("if hasattr(luta, 'ESCADA'): luta.ESCADA = False\n", ''))
        res = {}
        for nome_, pasta in (('antes', os.path.join(tmp, 'motor10')), ('agora', aqui)):
            sai = os.path.join(tmp, f'{nome_}.json')
            r = subprocess.run([sys.executable, script, pasta, str(k), sai], capture_output=True, text=True)
            if r.returncode: return [('B0 A LUTA DE SEMPRE (fase 2)', f'o motor {nome_} quebrou: {r.stderr[-300:]}', False)]
            res[nome_] = json.load(open(sai, encoding='utf-8'))
        dif = [a['i'] for a, b in zip(res['antes'], res['agora']) if a['h'] != b['h']]
    finally: shutil.rmtree(tmp, ignore_errors=True)
    return [(f'B0 A LUTA DE SEMPRE (fase 2): {k} lutas ao acaso sem habilidade (gente, bichos e magia), no motor de antes da fase 2 ({B0_REF}) e no de agora, com a escada do medo ligada: iguais, dado por dado',
             f'{k - len(dif)} de {k} lutas iguais, linha por linha' + (f'; DIFERENTES: {dif[:10]}' if dif else ''), not dif)]


METAS = (('B0', b0), ('HB1', hb1), ('HB2', hb2), ('HB3', hb3), ('HB4', hb4), ('HB5', hb5), ('HB6', hb6), ('HB7', hb7), ('HB8', hb8), ('HB9', hb9), ('HB10', hb10), ('HB11', hb11),
         ('HB12', hb12), ('HB13', hb13))


def main():
    a = sys.argv[1:]; n = int(a[0]) if a and a[0].isdigit() else 8000
    so = next((x.split('=', 1)[1].split(',') for x in a if x.startswith('so=')), None)
    global HB1_SO; HB1_SO = next((x.split('=', 1)[1].split(',') for x in a if x.startswith('hb1=')), None)
    os.environ['MOTOR10_MUNDO'] = tempfile.mkdtemp(prefix='m10_hab_')          # os mundos de prova: numa pasta de rascunho (nada toca um save de verdade)
    print(f'BANCO DAS HABILIDADES E DA FALA (a parte 2, fase 2: B0, HB1 a HB13, B3) · {n} lutas por linha da HB1\n', flush=True)
    ok = tot = 0
    for nome_, f in METAS:
        if so and nome_ not in so: continue
        try: res = f(n)
        except (SystemExit, Exception) as e:
            import traceback; res = [(f'{nome_}', f'A PROVA QUEBROU: {type(e).__name__}: {e} · {traceback.format_exc().splitlines()[-3].strip()}', False)]
        for nm, deu, passa in res:
            ok += passa; tot += 1; print(f"  {'passa' if passa else 'FALHA'}  {nm}: {deu}", flush=True)
    print(f'\n{ok} de {tot} metas passam.')
    return ok == tot


if __name__ == '__main__':
    sys.exit(0 if main() else 1)
