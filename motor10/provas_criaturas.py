#!/usr/bin/env python3
"""provas_criaturas.py — MOTOR 10, ETAPA DA MAGIA: O BANCO DE PROVAS DAS CRIATURAS E DA VILA (capítulos 15 e 16; o contrato: projeto/ETAPA_MAGIA.md).

As metas da frente das criaturas (a ordem de serviço, seção 2): os bandos contra o homem do degrau deles; os chefes com os lacaios contra um grupo de quatro;
a patrulha goblin da vila contra o guerreiro de nível 5 de peças Comuns; limpar um covil não é mina; e o resto que a frente entrega (o bestiário, a ameaça, os
chefes mágicos, a vida do covil, a caça com criaturas, a peçonha, a vila de teste com a magia). A luta é a do luta.py (com a magia da frente da luta), com
semente fixa: a mesma rodada dá o mesmo número. As provas que mexem no mundo rodam em pastas temporárias (MOTOR10_MUNDO); nunca num save.

Uso: python3 provas_criaturas.py [N]      N = o tamanho das amostras (padrão 300; as metas de frequência usam no mínimo o que dizem)
     (o `python3 provas_mundo.py` também roda este banco)
"""
import contextlib, io, json, os, random, shutil, sys, tempfile
import tabelas as T
import tabelas_mundo as M
import tabelas_bichos as TB
import tabelas_criaturas as TC
import tabelas_mercado as C
import estado, ato, caca, bichos, criaturas as CR, luta, talento
from pessoas import padrao, veste, ficha

# ---------- as faixas (do contrato: não se mexem) ----------
BANDO = (35, 65)            # um bando de goblins e um de orcs contra o homem do degrau deles
CHEFE = (30, 70)            # o chefe com os lacaios contra um grupo de quatro
PATRULHA = (40, 75)         # a patrulha goblin da vila contra o guerreiro de nível 5 de peças Comuns: vence nesta faixa...
PATRULHA_MORRE = 15         # ... e morre em tanto % ou menos
LIMPA = 3                   # limpar um covil não rende mais que tantas diárias por dia de trabalho, com o risco contado
DIARIA = M.SALARIO['diarista'] * 2
QUANTAS = (15, 25)          # de 15 a 25 criaturas novas
CHEFES_MIN = 4              # pelo menos quatro chefes mágicos, com lacaios e fases


def quieto(f, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()): return f(*a, **k)


def recusa(f):
    try: quieto(f)
    except SystemExit as x: return str(x) or 'recusado'
    return None


# ---------- quem luta ----------
def guerreiro():
    """o guerreiro de nível 5 de peças Comuns: o personagem que a vila de teste dá ao começo "guerreiro" (espada, escudo e malha, sem elmo)"""
    import vila_teste as V
    c = V.COMECOS['guerreiro']
    return veste(dict(nome='Maro', nivel=V.NIVEL, atributos=dict(c['atributos']), maestria=dict(c['maestria']), equip={}), arma=('espada', 0), armadura=('malha', 0), escudo=0, elmo=False)


def homem(c, k=''):
    """o homem do degrau (o mesmo do provas.py): espada, malha, elmo e escudo da categoria, no nível de referência dela"""
    return veste(padrao(f'homem {k}'.strip(), TC.REF[c]), arma=('espada', c), armadura=('malha', c), escudo=c)


def duelos(fa, fb, n, semente=7, surpresa=None, **kw):
    """n lutas (semente fixa). Devolve (% de vitória de A, % em que alguém de A morreu, % em que o primeiro de A morreu, a conta somada da magia)"""
    v = m = m0 = 0; conta = {}; luta.semente(semente); r = random.Random(semente)
    for i in range(n):
        sp = surpresa(r) if callable(surpresa) else surpresa
        S = luta.nova(fa(), fb(i), quieto=True, surpresa=sp, **kw); luta.corre(S); A = [f for f in S['L'] if f['lado'] == 'A']
        v += S['fim'] == 'A'; m += any(f['estado'] == 'morto' for f in A); m0 += A[0]['estado'] == 'morto'
        for k, q in (S.get('conta') or {}).items(): conta[k] = conta.get(k, 0) + q
    return round(100 * v / n), round(100 * m / n), round(100 * m0 / n, 1), conta


PLURAL = ['Comuns', 'Incomuns', 'Raros', 'Épicos', 'Únicos', 'Lendários', 'Míticos', 'Primordiais']
def faixa(x, f): return f[0] <= x <= f[1]
def sn(x): return 'sim' if x else 'NÃO'


# ---------- o mundo de prova: a vila de teste com a magia, numa pasta temporária ----------
class Mundo:
    def __init__(s, semente=1, magia=True):
        s.d = tempfile.mkdtemp(prefix='provas_criaturas_'); s.antes = os.environ.get('MOTOR10_MUNDO'); os.environ['MOTOR10_MUNDO'] = s.d
        import vila_teste, turno
        s.E = quieto(vila_teste.cria, 'guerreiro', None, semente, talentos=True); estado.grava(s.E); quieto(turno.abre, s.E)
        if magia: quieto(vila_teste.magia, s.E)
    def __enter__(s): return s
    def __exit__(s, *a):
        os.environ.pop('MOTOR10_MUNDO', None)
        if s.antes is not None: os.environ['MOTOR10_MUNDO'] = s.antes
        shutil.rmtree(s.d, ignore_errors=True)


def prata_do_mundo(E): return sum(p['moedas'] for p in E['gente'].values()) + sum(int(l.get('estoque', {}).get('prata', 0)) for l in E['lugares'].values())


def um_dia(E):
    """o dia passa sem ninguém agir: o relógio anda e a parte do mundo que importa aqui vira (a fauna cria; o covil vive). Devolve os eventos do dia."""
    estado.aplica(E, 'tempo', [['relogio', M.BLOCOS_DIA]], texto='um dia sem ninguém'); caca.virada(E); CR.virada(E)
    evs = list(E.get('_novos') or [])
    if '_novos' in E: E['_novos'].clear()
    return evs


# ---------- as provas ----------
def _bestiario(n):
    """C1. o bestiário: de 15 a 25 criaturas, todas montam e dão ficha; os traços só da lista fechada; as frases dos nove traços novos; as duas trancas da etapa 2"""
    out = []; mal = []; esp = TC.ESPECIES
    novos = set(T.TRACOS_NOVOS); velhos = set(TB.TRACOS)
    for k, e in esp.items():
        try:
            p = CR.criatura(k, posto=e['bando_postos'][0][0]) if e.get('povo') else CR.criatura(k); F = ficha(p)
            if F['pvmax'] <= 0 or not set(F['tracos']) <= (novos | velhos): mal.append(f'{k}: ficha torta')
        except (Exception, SystemExit) as x: mal.append(f'{k}: {type(x).__name__} {x}')
        if e['grau'] not in TB.GRAU_DA_CAT[e['cat']] or e['tamanho'] not in TB.TAMANHOS or not set(e['tracos']) <= (novos | velhos) or any(h not in caca.K.HABITATS for h in e['habitat']):
            mal.append(f'{k}: tabela torta')
        for b in e['despojo']:
            nm, c = M.le_materia(b)
            if (c is not None and (nm not in M.MATERIAS or c > M.MATERIA_ATE)) or (c is None and C.base(b) is None): mal.append(f'{k}: despojo "{b}" desconhecido')
    trancas = not (set(esp) & set(TB.ESPECIES)) and not (novos & velhos) and 12 <= len(TB.ESPECIES) <= 16 and 8 <= len(TB.TRACOS) <= 12
    frases = set(TC.TRACOS) == novos and all(len(v) > 20 and '—' not in v for v in TC.TRACOS.values())
    povos = sum(1 for e in esp.values() if e.get('povo')); mortos = sum(1 for e in esp.values() if 'sem vida' in e['tracos']); lancam = [k for k, e in esp.items() if 'lança' in e['tracos']]
    out.append(('C1 O BESTIÁRIO: de 15 a 25 criaturas novas (os povos que vestem peças, os mortos que andam, os seres de magia, as feras que faltam); todas montam e dão ficha; os traços só da lista fechada; '
                'as frases dos nove traços novos moram no tabelas_criaturas.TRACOS; e as duas trancas da etapa 2 seguem (nenhuma criatura no tabelas_bichos.ESPECIES, nenhum traço novo no tabelas_bichos.TRACOS)',
                f"{len(esp)} criaturas ({povos} de povo, {mortos} sem vida, as que lançam: {', '.join(lancam)}); com ficha e tabela certas: {len(esp) - len(set(m.split(':')[0] for m in mal))}"
                + (f" (tortas: {'; '.join(mal[:3])})" if mal else '') + f"; as frases dos traços novos: {sn(frases)}; as trancas: {sn(trancas)}",
                faixa(len(esp), QUANTAS) and not mal and frases and trancas))
    return out


def _ameaca(n):
    """C2. a ameaça lida antes: toda criatura tem a frase dela, com o grau, a categoria e a frase de cada traço (os novos, da página das criaturas); o povo diz o que veste;
    o morto que anda diz que não foge; e o bichos.ameaca nunca procura traço novo no tabelas_bichos.TRACOS (com um tabelas_bichos.TRACOS que estoura no traço novo, segue saindo)"""
    class Estoura(dict):
        def __getitem__(s, k):
            if k in T.TRACOS_NOVOS: raise KeyError(f'traço novo procurado no tabelas_bichos.TRACOS: {k}')
            return dict.__getitem__(s, k)
    velho = TB.TRACOS; TB.TRACOS = Estoura(velho); mal = []
    try:
        for k, e in TC.ESPECIES.items():
            try:
                a = bichos.ameaca(k); a3 = bichos.ameaca(k, n=3, arma=0, armadura=0)
                if not all(x in a for x in (f"grau {e['grau']}", T.CATS[e['cat']])) or any(TC.frase(t) not in a for t in e['tracos']) or '—' in a: mal.append(k)
                if e.get('povo') and 'É POVO' not in a: mal.append(k)
                if 'sem vida' in e['tracos'] and 'pode fugir' in a: mal.append(k)
                if e.get('feiticos') and 'Lança:' not in a: mal.append(k)
            except (Exception, SystemExit) as x: mal.append(f'{k} ({type(x).__name__}: {x})')
        ch = {q: CR.ameaca_chefe(q) for q in TC.CHEFES}
    finally: TB.TRACOS = velho
    g = bichos.ameaca('goblin', n=3, arma=0, armadura=0); esp = bichos.ameaca('espectro')
    certo = not mal and all('CHEFE' in v for v in ch.values()) and 'veste peças' in g and 'gastas e malfeitas' in g and 'não foge' in esp
    return [('C2 A AMEAÇA LIDA ANTES: toda criatura tem a frase dela (o grau, a categoria, a frase de cada traço; o povo diz o que veste; o morto que anda diz que não foge; quem lança diz o que lança), '
             'e a do chefe diz o que ele lança e como muda; o bichos.ameaca não procura traço novo no tabelas_bichos.TRACOS',
             f"{len(TC.ESPECIES) - len(set(mal))} de {len(TC.ESPECIES)} criaturas com a frase certa" + (f" (tortas: {', '.join(mal[:4])})" if mal else '') + f"; os {len(ch)} chefes: {sn(all('CHEFE' in v for v in ch.values()))}; "
             f"o goblin: «{g.split('É POVO: ')[1][:90]}...»", certo)]


def _chefes_magicos(n):
    """C3. os chefes mágicos: pelo menos quatro, cada um com lacaios; os que lançam sabem feitiços da lista (e a luta os lança); as fases só com as chaves do contrato, e a fase vira na luta"""
    chaves = {'abaixo', 'diz', 'ganha', 'perde', 'feiticos', 'mana', 'brado', 'ergue'}; L = []; mal = []
    for q, Cf in TC.CHEFES.items():
        try:
            P = CR.chefe(q); b = P[0]; Fb = ficha(b); fe = Fb['feiticos']; fases = Fb['fases']
            if len(P) < 3: mal.append(f'{q}: sem lacaios')
            if any(k not in T.FEITICOS for k in fe) or any(set(x) - chaves for x in fases): mal.append(f'{q}: feitiço ou fase fora do contrato')
            magico = bool(fe or Fb['encantos'] or 'lança' in Fb['tracos'])
            c = Cf.get('cat') if Cf.get('cat') is not None else TC.ESPECIES[Cf['especie']]['cat']
            _, _, _, conta = duelos(lambda: [homem(c, k) for k in range(4)], lambda i: CR.chefe(q), max(40, n // 6), inicio='longe')      # de longe: quem lança, lança antes de o aço chegar
            L.append((q, magico, len(P) - 1, conta.get('lances', 0), conta.get('fases', 0), conta.get('erguidos', 0)))
        except (Exception, SystemExit) as x: mal.append(f'{q}: {type(x).__name__} {x}')
    magicos = [x for x in L if x[1] and x[4] > 0 and (x[3] > 0 or x[0] == 'senhor da guerra')]
    return [('C3 OS CHEFES MÁGICOS: pelo menos quatro, cada um com os lacaios; quem lança sabe feitiços da lista e a luta os lança (a luta começa longe); as fases só com as chaves do contrato, e a fase vira na luta (a luta para e pergunta)',
             '; '.join(f"{q}: {lac} lacaios, {lan} lances e {fs} fases em {max(40, n // 6)} lutas" + (f", {er} erguidos" if er else '') for q, _, lac, lan, fs, er in L) + (f" · tortos: {'; '.join(mal)}" if mal else ''),
             len(magicos) >= CHEFES_MIN and not mal)]


def _bandos(n):
    """C4. um bando de goblins e um de orcs contra o homem do degrau deles: de 35 a 65%"""
    k = max(600, n * 2)
    g = duelos(lambda: [homem(0)], lambda i: CR.bando('goblin', n=4), k)
    o = duelos(lambda: [homem(1)], lambda i: CR.bando('orc', n=2), k)
    g3 = duelos(lambda: [homem(0)], lambda i: CR.bando('goblin', n=3), k // 2); o3 = duelos(lambda: [homem(1)], lambda i: CR.bando('orc', n=3), k // 2)
    return [('C4 UM BANDO DE GOBLINS E UM DE ORCS CONTRA O HOMEM DO DEGRAU DELES (espada, malha, elmo e escudo da categoria: o goblin é Comum, nível 10; o orc é Incomum, nível 30): '
             f'o bando que um homem do degrau enfrenta de igual para igual (quatro goblins; dois orcs) vence-o de {BANDO[0]} a {BANDO[1]}% das vezes',
             f"o homem Comum contra 4 goblins: vence {g[0]}% (morre em {g[1]}%); o homem Incomum contra 2 orcs: vence {o[0]}% (morre em {o[1]}%); "
             f"PARA COMPARAR: contra 3 goblins, {g3[0]}%; contra 3 orcs, {o3[0]}% ({k} lutas cada)", faixa(100 - g[0], BANDO) and faixa(100 - o[0], BANDO))]


def _chefes_x4(n):
    """C5. o chefe com os lacaios contra um grupo de quatro: de 30 a 70% (o grupo do degrau em que o chefe vive: o xamã, a toca de goblins Comuns; os outros, o degrau dele)"""
    k = max(300, n); res = []
    for q, c in (('xamã goblin', 0), ('senhor da guerra', 2), ('bruxa do brejo', 2), ('necromante', 3), ('vampiro', 3)):
        v, m, _, conta = duelos(lambda: [homem(c, j) for j in range(4)], lambda i: CR.chefe(q), k)
        res.append((q, c, 100 - v, m))
    return [(f'C5 O CHEFE COM OS LACAIOS CONTRA UM GRUPO DE QUATRO: cada chefe vence de {CHEFE[0]} a {CHEFE[1]}% das lutas contra quatro homens do degrau em que vive (o xamã mora numa toca de goblins Comuns: '
             'quatro homens Comuns; o senhor da guerra e a bruxa do brejo, Raros; o necromante e o senhor vampiro, Épicos)',
             '; '.join(f"{q} contra quatro {PLURAL[c]}: o chefe vence {v}% (morre alguém do grupo em {m}%)" for q, c, v, m in res) + f" ({k} lutas cada)",
             all(faixa(v, CHEFE) for _, _, v, _ in res))]


def _patrulha(n):
    """C6. a patrulha goblin da vila contra o guerreiro de nível 5 de peças Comuns: vence de 40 a 75% e morre em 15% ou menos"""
    k = max(1500, n * 4); e = TC.ESPECIES['goblin']; lo, hi = e['bando']
    v, _, m0, _ = duelos(lambda: [guerreiro()], lambda i: CR.bando('goblin', random.Random(10_000 + i)), k, surpresa=lambda r: 'B' if r.random() < 0.5 else None)
    v2 = duelos(lambda: [guerreiro()], lambda i: CR.bando('goblin', n=lo), k // 3); v4 = duelos(lambda: [guerreiro()], lambda i: CR.bando('goblin', n=hi), k // 3)
    return [(f'C6 A PATRULHA GOBLIN DA VILA CONTRA O GUERREIRO DE NÍVEL 5 DE PEÇAS COMUNS (o personagem do começo "guerreiro": espada, escudo e malha, sem elmo): a patrulha como a caça a dá '
             f'(de {lo} a {hi} goblins de faca; metade das vezes ele a vê primeiro): ele vence de {PATRULHA[0]} a {PATRULHA[1]}% e morre em {PATRULHA_MORRE}% ou menos',
             f"vence {v}%, morre em {m0:g}% ({k} lutas); contra {lo}: vence {v2[0]}%, morre em {v2[2]:g}%; contra {hi}: vence {v4[0]}%, morre em {v4[2]:g}%".replace('.', ','),
             faixa(v, PATRULHA) and m0 <= PATRULHA_MORRE)]


def _covil(n):
    """C7. o covil sozinho, um ano: o bando cresce até perto do teto e não passa dele; come da caça contada sem acabar com ela; o que rouba é pouco; a prata do mundo fecha; a toca cheia ganha o xamã"""
    mundos = max(4, n // 75); H = []
    for s in range(1, mundos + 1):
        with Mundo(s) as W:
            E = W.E; p0 = prata_do_mundo(E); xama = None; maxc = 0; evs = []
            for d in range(365):
                evs += [ev for ev in um_dia(E) if ev.get('tipo') == 'covil']; maxc = max(maxc, CR.cabecas(E, 'mata'))
                if xama is None and E['lugares']['mata']['covil'].get('chefe'): xama = d + 1
            roubo = -sum(ef[4] for ev in evs if ev.get('tipo') == 'covil' for ef in ev['efeitos'] if ef[:3] == ['estoque', 'vila', 'comida'])
            prata_roubo = -sum(ef[4] for ev in evs if ev.get('tipo') == 'covil' for ef in ev['efeitos'] if ef[:3] == ['estoque', 'vila', 'prata'])
            B = caca.bichos_de(E, 'mata'); P = estado.valida(E)
            H.append(dict(cab=CR.cabecas(E, 'mata'), maxc=maxc, xama=xama, corca=B.get('corça', 0), javali=B.get('javali', 0), fecha=prata_do_mundo(E) == p0, roubo=roubo, prata=prata_roubo, P=P,
                          tesouro=int(E['lugares']['mata'].get('estoque', {}).get('prata', 0))))
    teto = TC.COVIS['goblin']['teto']; ok = (all(h['maxc'] <= teto and h['fecha'] and not h['P'] and h['corca'] >= 40 and h['javali'] >= 20 for h in H) and sum(1 for h in H if h['xama']) >= len(H) // 2
                                            and all(h['roubo'] <= 0.02 * 400 * 365 for h in H) and all(h['cab'] >= 8 for h in H))
    xs = [h['xama'] for h in H if h['xama']]
    return [('C7 O COVIL SOZINHO, UM ANO (a toca dos goblins da vila de teste, sem ninguém para incomodar): o bando cresce até perto do teto e não passa dele; come da caça contada sem acabar com ela; '
             'o que rouba da vila é pouco (menos de 2% do que ela produz de comida); a prata do mundo fecha (a que o bando rouba vai para o tesouro da toca); e a toca cheia ganha o xamã',
             f"{len(H)} mundos: cabeças no fim {', '.join(str(h['cab']) for h in H)} (o maior: {max(h['maxc'] for h in H)}; o teto {teto}); a corça fica em {min(h['corca'] for h in H)} a {max(h['corca'] for h in H)} de 80, "
             f"o javali em {min(h['javali'] for h in H)} a {max(h['javali'] for h in H)} de 40; roubou {min(h['roubo'] for h in H)} a {max(h['roubo'] for h in H)} de comida e {min(h['prata'] for h in H)} a {max(h['prata'] for h in H)} de prata no ano "
             f"(o tesouro no fim: {min(h['tesouro'] for h in H)} a {max(h['tesouro'] for h in H)}); o xamã sobe em {len(xs)} de {len(H)} mundos" + (f" (no Dia {min(xs)} a {max(xs)})" if xs else '')
             + f"; a prata fecha em {sum(h['fecha'] for h in H)} de {len(H)}; estado inteiro em {sum(not h['P'] for h in H)} de {len(H)}", ok)]


def _limpa(n):
    """C8. limpar um covil não é mina: a CASA LIMPADORA (o guerreiro de nível 5, com Tomé e Rute, a gente de armas da vila) vive 60 dias ao lado da toca da vila. Sai atrás da toca
    quando os três estão inteiros; com alguém ferido, a casa espera (o dia de espera conta como dia de trabalho perdido); vende a sucata na loja. O que rende (o tesouro mais a sucata
    vendida, a 60% do preço de base), dividido pelos dias de trabalho de cada um, não passa de 3 diárias. O risco conta: quem morre para de render, e a meta diz quantos morreram."""
    vidas = max(12, n // 25); R = []; casa = ['eu', 'tome', 'rute']
    for s in range(1, vidas + 1):
        with Mundo(100 + s) as W:
            E = W.E; dias = 0; ganho = 0; mortos = 0; lutas = 0; saidas = 0
            vivos = lambda: [c for c in casa if E['gente'][c]['estado'] == 'vivo']
            inteiro = lambda c: E['gente'][c]['pv'] >= 0.9 * estado.pv_max(E['gente'][c]) and not E['gente'][c]['feridas']
            for d in range(60):
                if E['gente']['eu']['estado'] != 'vivo': break
                if CR.cabecas(E, 'mata') <= 0 and not E['lugares']['mata'].get('estoque', {}).get('prata'): quieto(um_dia, E); continue      # a toca vazia: a casa vive da vida dela (não conta)
                v = vivos(); dias += len(v)
                if all(inteiro(c) for c in v):
                    saidas += 1; m0 = sum(E['gente'][c]['moedas'] for c in v); com = [c for c in v if c != 'eu']
                    Rr = quieto(caca.sair, E, 'eu', 'mata', alvo='toca', blocos=4, com=com); k = 0
                    while E['gente']['eu']['estado'] == 'vivo' and k < 12 and Rr.get('fase') in ('encontro', 'luta', 'procura'):
                        k += 1
                        if Rr['fase'] == 'encontro':
                            if Rr['encontro'].get('toca') or (Rr['encontro']['viu'] == 'caçador' and Rr['encontro']['n'] <= 3): Rr = quieto(caca.atacar, E, 'eu'); lutas += 1
                            else: Rr = quieto(caca.fugir, E, 'eu')
                        elif Rr['fase'] == 'luta': Rr = quieto(caca.luta_roda, E, 'eu', ['grupo: atacar'])
                        elif Rr.get('campo'): Rr = quieto(caca.volta, E, 'eu')
                        else: Rr = quieto(caca.segue, E, 'eu')
                    if E['gente']['eu']['estado'] == 'vivo' and caca.saida(E['gente']['eu']): quieto(caca.volta, E, 'eu')
                    vv = vivos(); ganho += sum(E['gente'][c]['moedas'] for c in vv) - m0
                    for c in vv:
                        bens = {b: q2 for b, q2 in E['gente'][c].get('carga', {}).items() if q2 and b != 'comida' and C.base(b)}
                        ganho += sum(int(q2 * C.base(b) * C.PAGA) for b, q2 in bens.items())
                        if bens: estado.aplica(E, 'mestre', [['pessoa', c, 'carga.' + b, 'soma', -q2] for b, q2 in bens.items()], texto='a sucata vendida (a conta da prova)')
                for c in vivos():                           # a noite em casa (a conta da prova): a fome, o sono e o cansaço voltam a zero; o ferido recobra um sexto do PV e sara uma ferida
                    q = E['gente'][c]; cp = q['corpo']; ef = [['pessoa', c, k2, 'soma', -cp[k2]] for k2 in ('fome', 'sono', 'cansaco') if cp.get(k2)]
                    if q['pv'] < estado.pv_max(q): ef.append(['pessoa', c, 'pv', 'soma', min(estado.pv_max(q) - q['pv'], max(1, estado.pv_max(q) // 6))])
                    if q['feridas']: ef.append(['ferida', c, 'sara', 0])
                    if ef: estado.aplica(E, 'mestre', ef, texto='a noite em casa (a conta da prova)')
                quieto(um_dia, E)
            mortos = sum(1 for c in casa if E['gente'][c]['estado'] != 'vivo')
            R.append(dict(dias=dias, ganho=ganho, mortos=mortos, lutas=lutas, saidas=saidas))
    tot_d = sum(r['dias'] for r in R); tot_g = sum(r['ganho'] for r in R); por = tot_g / max(1, tot_d) / DIARIA
    melhor = max((r['ganho'] / max(1, r['dias']) / DIARIA for r in R), default=0); morreu = sum(1 for r in R if r['mortos'])
    return [(f'C8 LIMPAR UM COVIL NÃO É MINA: a casa limpadora (o guerreiro de nível 5, com Tomé e Rute) vive 60 dias ao lado da toca da vila; sai atrás dela quando os três estão inteiros e espera '
             f'quando alguém está ferido; o tesouro e a sucata vendida, divididos pelos dias de trabalho de cada um (as saídas e a espera das feridas), não passam de {LIMPA} diárias ({LIMPA * DIARIA} de prata) '
             'por dia, com o risco contado',
             f"{len(R)} vidas: {tot_g} de prata em {tot_d} dias de trabalho (de cada um) = {por:.2f} diárias por dia (a melhor vida: {melhor:.2f}); saídas por vida: {sum(r['saidas'] for r in R) / len(R):.1f}, "
             f"lutas por vida: {sum(r['lutas'] for r in R) / len(R):.1f}; morreu alguém da casa em {morreu} de {len(R)} vidas ({sum(r['mortos'] for r in R)} mortos)".replace('.', ','),
             por <= LIMPA and melhor <= 2 * LIMPA)]


def _caca(n):
    """C9. a caça com criaturas, pelo caminho da mesa: a patrulha aparece pela contagem, a ameaça sai, a luta abre pelo arquivo do cenário (a forma curta refaz o goblin), quem morre
    sai da contagem, o despojo é a sucata da tabela; a toca acha-se com rolagem oculta, e quem fica com o campo leva o tesouro inteiro (a prata do mundo fecha)"""
    achados = []; mal = []
    for s in range(1, 9):
        with Mundo(200 + s) as W:
            E = W.E; c0 = CR.cabecas(E, 'mata'); p0 = prata_do_mundo(E); t0 = int(E['lugares']['mata']['estoque'].get('prata', 0))
            Rr = quieto(caca.sair, E, 'eu', 'mata', alvo='toca', blocos=6, com=['tome', 'rute']); k = 0; toca = None; viu = False
            while k < 16 and Rr.get('fase') in ('encontro', 'luta', 'procura') and E['gente']['eu']['estado'] == 'vivo':
                k += 1
                if Rr['fase'] == 'encontro':
                    viu = True; toca = toca or bool(Rr['encontro'].get('toca')); txt = Rr['texto']
                    if Rr['encontro'].get('toca') and 'A TOCA' not in txt: mal.append(f'{s}: a toca sem a frase')
                    Rr = quieto(caca.atacar, E, 'eu', inicio='perto', vantagens=['alto'] if caca.posicao(Rr['encontro'])[1] else [])
                elif Rr['fase'] == 'luta': Rr = quieto(caca.luta_roda, E, 'eu', ['grupo: atacar'])
                else:
                    if Rr.get('campo') and toca: break
                    Rr = quieto(caca.segue, E, 'eu')
            evs = [json.loads(x) for x in open(os.path.join(W.d, 'eventos.jsonl'), encoding='utf-8')] if os.path.exists(os.path.join(W.d, 'eventos.jsonl')) else []
            evs += [ev for ev in E.get('_novos', [])]
            sai = -sum(ef[4] for ev in evs if ev.get('tipo') == 'despojo' for ef in ev['efeitos'] if ef[:3] == ['lugar', 'mata', 'bichos.goblin'])
            carga = {}
            for ev in evs:
                if ev.get('tipo') == 'despojo':
                    for ef in ev['efeitos']:
                        if ef[0] == 'pessoa' and isinstance(ef[2], str) and ef[2].startswith('carga.') and ef[3] == 'soma': carga[ef[2][6:]] = carga.get(ef[2][6:], 0) + ef[4]
            lev = int(E['lugares']['mata']['estoque'].get('prata', 0)); P = estado.valida(E)
            if P: mal.append(f'{s}: estado torto ({P[0]})')
            if prata_do_mundo(E) != p0: mal.append(f'{s}: a prata do mundo não fecha')
            if set(carga) - set(TC.ESPECIES['goblin']['despojo']) - {'comida'}: mal.append(f'{s}: despojo fora da tabela ({carga})')
            achados.append(dict(toca=toca, viu=viu, sai=sai, c0=c0, c1=CR.cabecas(E, 'mata'), t0=t0, t1=lev, carga=carga, vivo=E['gente']['eu']['estado'] == 'vivo'))
    tocas = [a for a in achados if a['toca']]; levou = [a for a in tocas if a['t1'] == 0 and a['t0'] > 0]
    ok = not mal and len(tocas) >= 3 and len(levou) >= 1 and all(a['c1'] <= a['c0'] for a in achados) and sum(a['sai'] for a in achados) > 0
    return [('C9 A CAÇA COM CRIATURAS, PELO CAMINHO DA MESA (caca.py sair mata alvo=toca, atacar, luta, as contas): a toca acha-se com rolagem oculta e a frase da toca sai; a luta abre pelo arquivo do cenário '
             '(a forma curta refaz o goblin pelo bichos.bicho); quem morre sai da contagem; o despojo é a sucata da tabela; quem fica com o campo na toca leva o tesouro inteiro; a prata do mundo fecha',
             f"{len(achados)} saídas: acharam a toca {len(tocas)}; levaram o tesouro {len(levou)}; goblins que saíram da contagem: {sum(a['sai'] for a in achados)}; "
             f"o despojo somado: {dict((b, sum(a['carga'].get(b, 0) for a in achados)) for b in TC.ESPECIES['goblin']['despojo'])}; vivos no fim: {sum(a['vivo'] for a in achados)}" + (f" · tortos: {'; '.join(mal[:3])}" if mal else ''), ok)]


def _peconha(n):
    """C10. a peçonha: todo bicho e toda criatura de veneno dá peçonha da categoria dele (até a Rara), e o despojo sai da tabela"""
    venenosos = {k: e for k, e in list(TB.ESPECIES.items()) + list(TC.ESPECIES.items()) if 'veneno' in e['tracos']}
    mal = [k for k, e in venenosos.items() if e['despojo'].get(f"peçonha:{min(e['cat'], TC.PECONHA_ATE)}", 0) < 1]
    sai = [bichos.despojo(k, random.Random(1))[0] for k in venenosos]
    ok = not mal and all(any(b.startswith('peçonha:') for b in d) for d in sai) and all(C.base(f'peçonha:{c}') for c in range(TC.PECONHA_ATE + 1))
    return [('C10 A PEÇONHA: todo bicho e toda criatura de veneno dá peçonha da categoria dele (até a Rara), e ela tem preço no mercado',
             f"{len(venenosos) - len(mal)} de {len(venenosos)} (" + ', '.join(f"{k}: peçonha:{min(e['cat'], TC.PECONHA_ATE)}" for k, e in venenosos.items()) + ')' + (f" · sem peçonha: {', '.join(mal)}" if mal else ''), ok)]


def _vila(n):
    """C11. a vila de teste com a etapa inteira: o `vila_teste.py magia` acrescenta tudo a uma vila que já existe (uma cópia do ensaio/ do jogador), só por eventos, e recusa rodar duas vezes"""
    import vila_teste as V
    aqui = os.path.dirname(os.path.abspath(__file__)); ens = os.path.join(aqui, 'ensaio')
    d = tempfile.mkdtemp(prefix='provas_criaturas_vila_'); antes = os.environ.get('MOTOR10_MUNDO')
    try:
        ja = os.path.exists(os.path.join(ens, 'lugares.json')) and 'cova' in json.load(open(os.path.join(ens, 'lugares.json'), encoding='utf-8'))      # o save do jogador já tem a etapa da magia (posta no turno 5): ela não entra duas vezes
        if os.path.exists(os.path.join(ens, 'relogio.json')) and not ja: shutil.copytree(ens, d, dirs_exist_ok=True); de = 'uma cópia do ensaio/ do jogador'
        else:
            os.environ['MOTOR10_MUNDO'] = d; E0 = quieto(V.cria, 'guerreiro', None, 1); estado.grava(E0); de = 'uma vila de teste sem talento (o ensaio/ ' + ('já tem a magia' if ja else 'não estava') + ')'
        os.environ['MOTOR10_MUNDO'] = d; E = estado.carrega(); n0 = E['relogio']['eventos']; p0 = prata_do_mundo(E); itens0 = set(E['itens']['itens']); gente0 = set(E['gente'])
        k = quieto(V.magia, E, 'fio'); import turno
        tal = [e for e in E['_novos'] if any(isinstance(x, list) and len(x) == 5 and x[0] == 'pessoa' and x[2] == 'talento' for x in e.get('efeitos', []))]
        segredo = len(tal) == 1 and turno.secreto(tal[0])        # os talentos num evento só, do gerador: vão ao SÓ O MESTRE, não aos fatos do turno
        estado.grava(E); E = estado.carrega(); P = estado.valida(E)
        dois = recusa(lambda: V.magia(estado.carrega()))
        g = E['gente']; it = E['itens']['itens']
        rolados = all(talento.rolado(p) for p in g.values() if p['estado'] == 'vivo')
        quem = {pid: (g[pid].get('tradicao'), len(g[pid].get('feiticos') or []), [x['tipo'] for x in it.values() if x.get('dono') == pid and x.get('uso') in ('foco', 'pescoco')]) for pid in ('anselmo', 'lucia', 'joana') if pid in g}
        zeca = g.get('zeca', {}); maldita = [x for x in it.values() if x.get('maldita') and x.get('onde') == 'cova' and x.get('solto')]
        cv = E['lugares']['mata'].get('covil') or {}; cova = E['lugares'].get('cova') or {}
        mudou = set(gente0) <= set(g) and itens0 <= set(it)
        ok = (not P and dois and rolados and segredo and g['eu'].get('inclinacao') == 'fio' and len(quem) == 3 and all(t and nf >= 4 and 'foco' in tp for t, nf, tp in quem.values())
              and zeca.get('dom', {}).get('forja') == 2 and not (zeca.get('marca') or {}).get('dom_visto') and E['lugares']['vila'].get('botica') == 1 and E['lugares']['vila'].get('santuario') == 1
              and len(maldita) == 1 and cova.get('tipo') == 'ermo' and any(TC.ESPECIES.get(b, {}).get('tracos') and 'sem vida' in TC.ESPECIES[b]['tracos'] for b in cova.get('bichos', {})) and cv.get('especie') == 'goblin'
              and mudou and prata_do_mundo(E) - p0 == V.TOCA['tesouro'] + sum(x[7] for x in (V.MAGO, V.CLERIGA, V.BRUXA)))
        txt = (f"em {de}: {k} eventos, estado {'inteiro' if not P else 'TORTO: ' + P[0]}; nada recriado (a gente e os itens de antes seguem): {sn(mudou)}; recusa a segunda vez: {sn(bool(dois))}; "
               f"todos com talento rolado: {sn(rolados)}, num evento só, segredo do Mestre: {sn(segredo)}; a inclinação do personagem: {g['eu'].get('inclinacao')}; " + ', '.join(f"{g[p]['nome']} ({t}, {nf} feitiços, {'+'.join(tp)})" for p, (t, nf, tp) in quem.items())
               + f"; o Zeca: dom de forja {zeca.get('dom', {}).get('forja')} (escondido: {sn(not (zeca.get('marca') or {}).get('dom_visto'))}); botica {E['lugares']['vila'].get('botica')}, santuário {E['lugares']['vila'].get('santuario')}; "
               f"a cova: {cova.get('bichos')} e {len(maldita)} peça maldita no chão; a toca: {CR.cabecas(E, 'mata')} goblins; a prata que nasceu: {prata_do_mundo(E) - p0} (a das três pessoas novas e o tesouro da toca)")
    finally:
        os.environ.pop('MOTOR10_MUNDO', None)
        if antes is not None: os.environ['MOTOR10_MUNDO'] = antes
        shutil.rmtree(d, ignore_errors=True)
    return [('C11 A VILA DE TESTE COM A ETAPA INTEIRA: o `vila_teste.py magia` acrescenta tudo a uma vila que já existe, só por eventos, e recusa rodar duas vezes: os talentos de quem não foi rolado (o personagem com a '
             'inclinação), o mago, a botica da curandeira, o santuário com a clériga, a bruxa da borda da mata, o aprendiz da forja com um dom que ninguém leu, a cova com mortos e uma peça maldita, e a toca dos goblins', txt, ok)]


def provas(n=300):
    out = []
    for f in (_bestiario, _ameaca, _chefes_magicos, _bandos, _chefes_x4, _patrulha, _covil, _limpa, _caca, _peconha, _vila):
        try: out += f(n)
        except (Exception, SystemExit) as x:
            import traceback; out.append((f'{f.__name__}: a prova quebrou', f'{type(x).__name__}: {x} · ' + ' | '.join(l.strip() for l in traceback.format_exc().splitlines()[-4:-1]), False))
    return out


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 300
    print('BANCO DE PROVAS DAS CRIATURAS E DA VILA (etapa da magia: capítulos 15 e 16)\n')
    res = provas(n)
    for nome, deu, passa in res: print(f"  {'passa' if passa else 'FALHA'}  {nome}: {deu}")
    print(f'\n{sum(p for _, _, p in res)} de {len(res)} provas passam.')
    return all(p for _, _, p in res)


if __name__ == '__main__':
    import signal; hasattr(signal, 'SIGPIPE') and signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    sys.exit(0 if main() else 1)
