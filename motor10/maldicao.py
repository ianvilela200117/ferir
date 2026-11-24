#!/usr/bin/env python3
"""maldicao.py — MOTOR 10: AS MALDIÇÕES (etapa da magia, capítulo 13). Os números moram no tabelas_magia_mundo.py; o registro e o molde, no tabelas_mundo.py.

  UMA MALDIÇÃO é um registro na pessoa: nome, categoria, TIPO (míngua, chaga, azar, insônia, marca: o sinal), um RELÓGIO de 6 passos, a ORIGEM (feitiço, bicho, lugar, peça,
    juramento), quem a rogou e a CONDIÇÃO que a quebra. Não é estado de luta: é coisa de dias, e a única coisa desta etapa que mata fora da luta sem ser fome.
  O RELÓGIO: na virada de cada dia o mundo rola (o dado do mundo, oculto) 2d20 + a força (2 + 4 por categoria) contra a Firmeza do amaldiçoado (o amuleto compra tempo).
    Venceu, anda um passo. 1 a marca (nada) · 2 o peso (−1 em tudo) · 3 a míngua (−2; a noite não devolve PV) · 4 a chaga (−2; a ferida não sara, a Mana não volta fora
    da luta) · 5 o fim à vista (−4; cada virada tira 10% do PV máximo) · 6 a morte (na virada, com a causa escrita). Da categoria da guarda, mata em cerca de 15 dias;
    num aldeão sem amuleto, a Comum em cerca de 10; nunca antes de 5. Anda para TODA gente amaldiçoada: o mundo não gira em torno do personagem.
  DE ONDE VEM: a PEÇA MALDITA, ao ser posta em uso (e a mão não a larga enquanto a maldição dura); o LUGAR MALDITO, a cada bloco passado nele (o dado contra a Firmeza);
    o feitiço (a praga da bruxa: magia_mundo); o bicho que amaldiçoa (a luta); o juramento quebrado (o voto do clérigo, a dívida da bruxa).
  COMO SE QUEBRA: cumprindo a CONDIÇÃO (devolver a peça ao lugar dela; matar o bicho naquele ermo; o perdão ou a morte de quem rogou; ficar 7 dias fora do lugar; a dívida
    zerada: o estado confere na virada; cumprir o jurado e queimar o laço, o Mestre atesta); o RITO DO CLÉRIGO (quebrar-maldição: 1 bloco, 6 de Mana, uma tentativa por dia,
    2d20 + Conjuração contra 28 + a força + 2 por passo além do primeiro; falhou por 5 ou mais, ele leva a marca); a POÇÃO só ganha tempo (a de categoria maior quebra,
    a igual recua 2 passos, a menor segura 1 dia). Dormir, comer, curar o PV e mudar de lugar não quebram.
  O QUE A MESA MOSTRA, em três degraus: não sabe (passo 1: nada); desconfia (do passo 2: o sinal e o que pesa, sem nome nem prazo); sabe (alguém leu: tudo).
    O SÓ O MESTRE vê tudo de todos. O RETOMAR leva as maldições do personagem que ele sente; o `turno.py fecha` recusa com uma no passo 4 sem pergunta aberta sobre ela.

Uso (o personagem do jogador, ou quem=ID):
  python3 maldicao.py ver [ALVO]                          as maldições de alguém, como a pessoa as conhece (sem ALVO: o personagem)
  python3 maldicao.py mestre [ALVO]                       tudo (SÓ O MESTRE): a força, a Firmeza, a chance de andar amanhã, a condição
  python3 maldicao.py rito ALVO [MID] [paga=N] quem=CLERIGO    o rito de quebrar (1 bloco): quem tem o feitiço tenta; o personagem ajudado paga (o preço de tabela, se não disser)
  python3 maldicao.py devolver ITEM                       devolve a peça maldita ao lugar dela (estando lá): a maldição que veio dela quebra
  python3 maldicao.py perdoa ALVO MID quem=QUEM_ROGOU     quem rogou desata sem teste
  python3 maldicao.py cumpre ALVO MID "como foi"          o Mestre atesta que a condição se cumpriu (cumprir, queimar, ou o que o estado não sabe conferir)
  python3 maldicao.py poe ALVO "Nome" CATEGORIA TIPO CONDICAO [de=feitiço|bicho|lugar|peça|juramento] [fonte=X] [rogou=ID] "como foi"    o Mestre põe uma maldição
  python3 maldicao.py peca ITEM "Nome" CATEGORIA TIPO [onde=LUGAR] "como foi"     o Mestre amaldiçoa uma peça (quebra: devolvê-la a ONDE; sem onde: o lugar dela agora)
  python3 maldicao.py lugar "Nome" CATEGORIA TIPO "como foi"                      o Mestre amaldiçoa o lugar onde a pessoa está (quebra: 7 dias longe dele)
TIPO: míngua chaga azar insônia marca · CONDICAO: devolver matar perdao morte sair cumprir queimar divida
"""
import json, math, os, sys
import tabelas as T
import tabelas_mundo as M
import tabelas_magia_mundo as W
import estado, ato, teste, talento
from itens import cat_i

PASSOS = M.MALDICAO_PASSOS
FEM = ['Comum', 'Incomum', 'Rara', 'Épica', 'Única', 'Lendária', 'Mítica', 'Primordial']


def _d20x(r):
    """um d20 do MUNDO em que o 20 rola de novo e soma (o mesmo dado do teste.py, mas da semente: mesma semente, mesmo mundo)"""
    t = r.randint(1, 20); s = t
    while t == 20: t = r.randint(1, 20); s += t
    return s


# ---------- pôr ----------
def registro(molde, de, fonte=None, quem=None, condicao=None, passo=1, sabe=0):
    """o registro de uma maldição (sem id: o gravador dá) a partir de um MOLDE {nome, cat, tipo, condicao}"""
    return dict(nome=molde['nome'], cat=molde['cat'], tipo=molde['tipo'], passo=passo, de=de, fonte=fonte, quem=quem,
                condicao=json.loads(json.dumps(condicao or molde['condicao'])), sabe=sabe, suspensa=None)


def poe(E, pid, molde, de, fonte=None, quem=None, condicao=None, passo=1, sabe=0):
    """os efeitos que põem uma maldição em alguém (quem chama aplica, no evento do próprio ato)"""
    return [['maldicao', pid, 'poe', registro(molde, de, fonte, quem, condicao, passo, sabe)]]


def molde(nome, cat, tipo, condicao):
    m = dict(nome=nome, cat=cat_i(cat), tipo=tipo, condicao=condicao)
    e = estado._molde_erro(m)
    if e: sys.exit(e)
    return m


# ---------- ler ----------
def firmeza(E, pid, visivel=False):
    """a Firmeza contra a maldição: a conta única do estado (estado.firmeza: Vontade, a maior maestria, o dom de tradição, o amuleto ou metade da armadura do tronco, e a poção
    de guarda valendo amuleto da categoria dela enquanto dura). `visivel`: só o dom que a pessoa já viu (a conta que vai à mesa)"""
    return estado.firmeza(E, pid, visivel)


def chance(E, pid, m):
    """a chance de esta maldição andar um passo na próxima virada (a conta exata do 2d20 que rola de novo)"""
    import oficio
    return oficio.chance_de(math.ceil(firmeza(E, pid) - W.forca(m['cat'])))


def degrau(m): return max(m.get('sabe', 0), 1 if m.get('passo', 1) >= 2 else 0)        # o que a pessoa sabe: 0 nada, 1 desconfia, 2 sabe


def pesa(m):
    """o que o passo faz, em palavras"""
    k = m['passo']; pena = M.MALDICAO_PENA.get(k, 0)
    L = [f'−{-pena} em todo teste'] if pena else []
    if k >= M.MALDICAO_SEM_NOITE: L.append('a noite não devolve PV')
    if k >= M.MALDICAO_SEM_SARAR: L += ['a ferida não sara', 'a Mana não volta fora da luta']
    if k >= 5: L.append(f'cada virada tira {W.FIM_PV:.0%} do PV máximo')
    return '; '.join(L) or 'nada ainda'


def _lugar(E, x): return E['lugares'][x]['nome'] if x in E['lugares'] else x
def _em(E, x): return estado.em(E, x) if x in E['lugares'] else f'em {x}'
def _quem(E, x): return E['gente'][x]['nome'] if x in E['gente'] else x


def diz_condicao(E, c):
    t = c.get('tipo'); L = E['itens']['itens']
    if t == 'devolver': return f"devolver {L[c['item']]['nome'] if c.get('item') in L else 'a peça'} ao lugar dela, {_em(E, c.get('onde'))}"
    if t == 'matar': return f"matar {c.get('especie', 'o bicho')} {_em(E, c.get('ermo'))}" if c.get('ermo') else f"matar {c.get('especie', 'o bicho')}"
    if t == 'perdao': return f"o perdão de quem rogou" + (f" ({_quem(E, c['quem'])})" if c.get('quem') else '')
    if t == 'morte': return 'a morte de quem rogou'
    if t == 'sair': return f"ficar {W.SAIR_DIAS} dias sem pôr o pé {_em(E, c.get('lugar'))}"
    if t == 'divida': return 'pagar a dívida até zerar'
    if t == 'queimar': return 'queimar o laço que quem rogou guarda' + (f": {c['texto']}" if c.get('texto') else '')
    return c.get('texto') or 'cumprir o que se jurou (ou a penitência de um clérigo Mestre)'


def _origem(E, m):
    de, f = m.get('de'), m.get('fonte')
    if de == 'peça':
        it = E['itens']['itens'].get(f); n = it['nome'] if it else f
        return estado.de_nome(n) if n.split(' ')[0] in ('a', 'o', 'as', 'os') else f"da peça {n}"      # "da Espada do Guardião"; "da peça Cajado de Anselmo"
    if de == 'lugar': return f"do lugar: {_lugar(E, f)}"
    if de == 'bicho': return f"de um bicho ({f})" if f else 'de um bicho'
    if de == 'feitiço': return 'de um feitiço' + (f" de {_quem(E, m['quem'])}" if m.get('quem') else '')
    return 'de um juramento quebrado'


def diz(E, pid, m, mestre=False):
    """a linha de uma maldição: como a pessoa a conhece (pelo degrau de saber), ou tudo (o Mestre). None: a pessoa não sabe dela"""
    p = E['gente'][pid]; g = degrau(m)
    if mestre:
        return (f"{p['nome']}: {m['id']} {m['nome']} ({FEM[m['cat']]}, {m['tipo']}), passo {m['passo']} de 6 ({PASSOS[m['passo'] - 1]}) desde o Dia {m.get('desde')}; força +{W.forca(m['cat'])} "
                f"contra Firmeza {firmeza(E, pid):g}".replace('.', ',') + f": anda na virada com {chance(E, pid, m):.0%}; {_origem(E, m)}; quebra: {diz_condicao(E, m['condicao'])}; "
                f"a pessoa {('não sabe', 'desconfia', 'sabe')[g]}" + (f"; SEGURADA até o Dia {m['suspensa']}" if m.get('suspensa') is not None and m['suspensa'] >= E['relogio']['dia'] else ''))
    if g == 0: return None
    if g == 1: return f"ALGO ESTÁ ERRADO: {p['nome']} {W.SINAIS.get(m['tipo'], 'não está bem')}. Pesa: {pesa(m)}. (Quem lê diz o que é: um clérigo, ou uma bruxa.)"
    return (f"MALDIÇÃO: {m['nome']} ({FEM[m['cat']]}, {m['tipo']}), passo {m['passo']} de 6 ({PASSOS[m['passo'] - 1]}): {pesa(m)}. Desde o Dia {m.get('desde')}. "
            f"Veio {_origem(E, m)}. Quebra: {diz_condicao(E, m['condicao'])}; ou o rito de um clérigo ({W.preco_quebrar(m['cat'])} de prata, de pessoa a pessoa)")


def minhas(p): return [m for m in p.get('maldicoes') or [] if isinstance(m, dict)]


# ---------- as condições que o estado sabe conferir ----------
def _matou(E, pid, especie, ermo, desde):
    """a pessoa matou (ficou com o campo e tirou da contagem) um bicho desta espécie neste ermo, desde o dia dito? Lê o registro de eventos (o arquivo e o que ainda não foi gravado)"""
    def bate(ev):
        return (ev.get('tipo') == 'despojo' and pid in (ev.get('quem') or []) and (ermo is None or ev.get('onde') == ermo) and ev.get('dia', 0) >= (desde or 0)
                and any(isinstance(x, list) and len(x) == 5 and x[0] == 'lugar' and x[2] == f'bichos.{especie}' and x[3] == 'soma' and x[4] < 0 for x in ev.get('efeitos', [])))
    if any(bate(ev) for ev in E.get('_novos', [])): return True
    arq = os.path.join(estado.pasta(), 'eventos.jsonl')
    if not os.path.exists(arq): return False
    with open(arq, encoding='utf-8') as f:
        for linha in f:
            if '"despojo"' in linha and f'bichos.{especie}' in linha:
                try:
                    if bate(json.loads(linha)): return True
                except ValueError: continue
    return False


def cumpridas(E, pid):
    """[(maldição, como)] das maldições desta pessoa cuja condição o estado vê cumprida (a morte de quem rogou, a dívida zerada, os dias longe do lugar, o bicho morto, a peça devolvida)"""
    p = E['gente'][pid]; dia = E['relogio']['dia']; out = []; L = E['itens']['itens']
    for m in minhas(p):
        c = m.get('condicao') or {}; t = c.get('tipo')
        if t in ('morte', 'perdao') and m.get('quem') in E['gente'] and E['gente'][m['quem']]['estado'] == 'morto': out.append((m, f"{_quem(E, m['quem'])}, que a rogou, morreu"))      # morta quem rogou, o que ela atou se desfaz
        elif t == 'divida' and not (p.get('divida') or 0): out.append((m, 'a dívida zerou'))
        elif t == 'sair' and estado.onde(E, pid) != c.get('lugar') and isinstance(c.get('visto'), int) and dia - c['visto'] >= W.SAIR_DIAS: out.append((m, f"{W.SAIR_DIAS} dias longe de {_lugar(E, c.get('lugar'))}"))
        elif t == 'matar' and c.get('especie') and _matou(E, pid, c['especie'], c.get('ermo'), m.get('desde')): out.append((m, f"{c['especie']} morreu pela mão de {p['nome']}"))
        elif t == 'devolver' and c.get('item') in L and not L[c['item']].get('dono') and L[c['item']].get('onde') == c.get('onde'): out.append((m, 'a peça voltou ao lugar dela'))
    return out


def confere(E, pid):
    """quebra, num evento, as maldições desta pessoa cuja condição se cumpriu. Devolve as frases (vazio: nada)"""
    p = E['gente'].get(pid)
    if not p or p['estado'] != 'vivo': return []
    q = cumpridas(E, pid)
    if not q: return []
    estado.aplica(E, 'maldicao', [['maldicao', pid, m['id'], 'quebra', como] for m, como in q], onde=estado.onde(E, pid), quem=[pid],
                  texto='; '.join(f"a maldição de {p['nome']} se desfaz ({como})" for m, como in q))
    return [f"A maldição se desfaz: {como}." for m, como in q]


# ---------- o relógio: a virada do dia ----------
def virada(E):
    """o dia virou: para toda gente viva com maldição, primeiro quebram as que tiveram a condição cumprida; depois o relógio de cada uma anda (o dado do mundo, oculto):
    o passo 5 come 10% do PV máximo, o passo 6 mata no mesmo evento. A maldição segurada (a poção) não anda no dia que a segurou."""
    ontem = E['relogio']['dia'] - 1; eu = estado.eu(E)
    for pid in list(E['gente']):
        p = E['gente'][pid]
        if not isinstance(p, dict) or p.get('estado') != 'vivo' or not minhas(p): continue
        confere(E, pid); p = E['gente'][pid]
        if not minhas(p): continue
        fir = firmeza(E, pid); ef = []; morre = None; pv = p['pv']; notas = []
        for m in minhas(p):
            if m.get('suspensa') is not None and m['suspensa'] >= ontem: notas.append(f"{m['nome']} segurada pela poção: não anda"); continue
            if m['passo'] == 5:
                perde = max(1, int(estado.pv_max(p) * W.FIM_PV)); pv -= perde; ef.append(['pessoa', pid, 'pv', 'soma', -perde])
                if pv <= 0 and not morre: morre = m
            r = estado.sorte(E, f"maldicao|{pid}|{m['id']}"); a, b = _d20x(r), _d20x(r); tot = a + b + W.forca(m['cat']); anda = tot >= fir
            notas.append(f"{m['nome']}: {a} + {b} + {W.forca(m['cat'])} = {tot} contra {fir:g}: ".replace('.', ',') + (f"anda ao passo {m['passo'] + 1} ({PASSOS[min(5, m['passo'])]})" if anda else 'não anda'))
            if anda:
                ef.append(['maldicao', pid, m['id'], 'passo', 1])
                if m['passo'] + 1 >= len(PASSOS) and not morre: morre = m
        if pid == eu and notas: E['turno']['notas'].append(f"rolagem oculta, a maldição na virada do Dia {ontem}: " + ' · '.join(notas))
        if not ef: continue
        if morre: ef.append(['pessoa', pid, 'estado', 'poe', 'morto'])
        estado.aplica(E, 'virada', ef, onde=estado.onde(E, pid), quem=[pid],
                      texto=f"{p['nome']} morre da maldição: {morre['nome']} ({PASSOS[-1]})" if morre else 'o dia vira')


# ---------- o lugar maldito, a cada bloco; e os dias longe dele ----------
def bloco(E, pid, esforco, dorme):
    """os efeitos de UM bloco: no lugar maldito, quem ainda não tem a maldição dele rola (o dado do mundo) a força contra a Firmeza; quem tem uma maldição que se quebra
    longe de um lugar e está nele, o dia em que foi visto lá se renova"""
    p = E['gente'][pid]
    if p.get('estado') != 'vivo': return []
    lid = estado.onde(E, pid); l = E['lugares'].get(lid) or {}; mold = l.get('maldito'); ms = minhas(p); ef = []; dia = E['relogio']['dia']
    if not isinstance(mold, dict) and not ms: return []
    for m in ms:
        c = m.get('condicao') or {}
        if c.get('tipo') == 'sair' and c.get('lugar') == lid and c.get('visto') != dia: ef.append(['maldicao', pid, m['id'], 'condicao', dict(c, visto=dia)])
    if isinstance(mold, dict) and not any(m.get('de') == 'lugar' and m.get('fonte') == lid for m in ms):
        r = estado.sorte(E, f'lugar_maldito|{pid}|{lid}')
        if _d20x(r) + _d20x(r) + W.forca(mold['cat']) >= firmeza(E, pid):
            ef += poe(E, pid, mold, 'lugar', fonte=lid, condicao=dict(mold['condicao'], tipo='sair', lugar=lid, visto=dia))
    return ef


# ---------- a peça maldita, ao ser posta em uso ----------
def vestiu(E, pid, iid):
    """depois de alguém pôr uma peça em uso: a peça MALDITA põe a maldição dela (passo 1; a pessoa não sabe) e a mão não a larga mais enquanto ela durar"""
    it = E['itens']['itens'].get(iid) or {}; mold = it.get('maldita'); p = E['gente'][pid]
    if not isinstance(mold, dict) or any(m.get('de') == 'peça' and m.get('fonte') == iid for m in minhas(p)): return ''
    cond = dict(mold['condicao'])
    if cond.get('tipo') == 'devolver': cond.setdefault('item', iid)
    estado.aplica(E, 'maldicao', poe(E, pid, mold, 'peça', fonte=iid, condicao=cond), onde=estado.onde(E, pid), quem=[pid], texto=f"um frio sobe pelo braço de {p['nome']} ao pôr em uso {it['nome']}")
    return f"Um frio sobe pelo braço de {p['nome']}, e passa."


# ---------- quebrar ----------
def quebra(E, pid, mid, como):
    """os efeitos que quebram uma maldição (quem chama aplica, no evento do próprio ato)"""
    return [['maldicao', pid, mid, 'quebra', como]]


def pela_pocao(E, pid, m, cat):
    """os efeitos da poção quebra-maldição numa maldição: de categoria maior, quebra; igual, o relógio recua 2 passos; menor, segura 1 dia"""
    if cat > m['cat']: return [['maldicao', pid, m['id'], 'quebra', f"a poção quebra-maldição {FEM[min(cat, len(FEM) - 1)]}"]]
    if cat == m['cat']: return [['maldicao', pid, m['id'], 'passo', -W.QUEBRA_RECUA]] if m['passo'] > 1 else []
    return [['maldicao', pid, m['id'], 'suspensa', E['relogio']['dia']]]


def diz_pocao(m, cat, b):
    if cat > m['cat']: return f"algo frio deixa o corpo de {b['nome']}: a maldição se quebra" + (f" ({m['nome']})" if degrau(m) == 2 else '')
    if cat == m['cat']: return f"o peso recua" + (f": {m['nome']} volta ao passo {max(1, m['passo'] - W.QUEBRA_RECUA)}" if degrau(m) == 2 else '') if m['passo'] > 1 else 'nada muda: a maldição está no primeiro passo'
    return 'o peso segura por hoje: na virada a maldição não anda'


def _alvo_presente(E, quem, alvo):
    q = E['gente'].get(alvo) or sys.exit(f'não há a pessoa "{alvo}"')
    if q['estado'] != 'vivo': sys.exit(f"{q['nome']} {estado.morte_diz(E, q)}")
    if alvo != quem and estado.onde(E, alvo) != estado.onde(E, quem): sys.exit(f"{q['nome']} não está com {E['gente'][quem]['nome']}: o rito pede o toque")
    return q


def rito(E, quem, alvo, mid=None, paga=None):
    """O RITO DE QUEBRAR (1 bloco leve, 6 de Mana, uma tentativa por dia de quem o faz): quem sabe quebrar-maldição (e não quebrou o voto) tenta, na maldição dita (sem dizer:
    a de passo mais alto). 2d20 + Conjuração da fé contra 28 + a força + 2 por passo além do primeiro. Falhou por 5 ou mais: quem tentou leva a marca (a mesma maldição, no passo 1).
    O personagem ajudado paga a quem faz (de pessoa a pessoa: o preço de tabela da categoria, se não disser); o rito pela gente do mundo sai sem cobrança (magia_mundo.preco_servico)."""
    import magia_mundo
    c = magia_mundo.lancador(E, quem, 'quebrar-maldição'); q = _alvo_presente(E, quem, alvo); dia = E['relogio']['dia']
    ms = minhas(q)
    if not ms: sys.exit(f"{q['nome']} não tem maldição andando")
    m = next((x for x in ms if x['id'] == mid), None) if mid else max(ms, key=lambda x: (x['passo'], x['cat']))
    if m is None: sys.exit(f"{q['nome']} não tem a maldição \"{mid}\"")
    if (c.get('marca') or {}).get('quebrar_dia') == dia: sys.exit(f"{c['nome']} já tentou o rito hoje: uma tentativa por dia")
    preco = magia_mundo.preco_servico(E, alvo, quem, W.preco_quebrar(m['cat']), paga)
    if preco and q['moedas'] < preco: sys.exit(f"o rito de {c['nome']} custa {preco} de prata; {q['nome']} tem {q['moedas']}")
    custo = T.FEITICOS['quebrar-maldição']['mana']; contra = W.QUEBRAR[0] + W.forca(m['cat']) + W.QUEBRAR[1] * (m['passo'] - 1)
    pg = [['pessoa', alvo, 'moedas', 'soma', -preco], ['pessoa', quem, 'moedas', 'soma', preco]] if preco else []
    def mais(i): return [['pessoa', quem, 'mana', 'soma', -custo], ['pessoa', quem, 'marca.quebrar_dia', 'poe', dia], ['pessoa', quem, 'treino.fé', 'soma', 1]] + pg
    n, pq = ato.passa(E, quem, W.RITO_BLOCOS, 'rito', esforco='leve', mais=mais, com=[alvo] if alvo != quem else (), texto=f"{c['nome']} faz o rito de quebrar a maldição de {q['nome']}" + (f" (por {preco} de prata)" if preco else ''))
    if not n: sys.exit(f"o rito não se fez: {pq}")
    vis, real = magia_mundo.conjuracao(E, quem, 'fé', visivel=True), magia_mundo.conjuracao(E, quem, 'fé')
    c = E['gente'][quem]; atr = c['atributos']['Vontade'] // 10
    r = teste.rola(E, f"quebrar {m['nome'] if degrau(m) == 2 else 'a maldição'} de {q['nome']}", 'Vontade', contra, mais=int(vis) - atr, quem=quem, rotulo='Conjuração da fé', **({'dom': int(real) - int(vis)} if int(real) > int(vis) else {}))
    q = E['gente'][alvo]; m = next((x for x in minhas(q) if x['id'] == m['id']), None)
    if m is None: return dict(fim='sumiu', texto=teste.diz(E, r) + '\nA maldição já não estava lá quando o rito acabou.')
    margem = r['total'] - r['contra']; ef = []
    if margem >= 0: ef.append(['maldicao', alvo, m['id'], 'quebra', f"o rito de {c['nome']}"]); txt = f"{c['nome']} quebra a maldição de {q['nome']}" + (f" ({m['nome']})" if degrau(m) == 2 else '')
    else:
        txt = f"o rito de {c['nome']} não quebra a maldição de {q['nome']}"
        if margem <= -W.QUEBRAR_MARCA:
            ef += poe(E, quem, m, 'feitiço', fonte=alvo, condicao=dict(tipo='cumprir', texto='a marca do rito falhado: a penitência de um clérigo Mestre'), sabe=2); txt += f", e {c['nome']} leva a marca dela"      # quem fez o rito sabe que levou a marca
    if talento.decidiu(r): ef += talento.mostra(E, quem)
    if ef: estado.aplica(E, 'rito', ef, onde=estado.onde(E, quem), quem=list(dict.fromkeys([quem, alvo])), texto=txt)
    return dict(fim='quebrou' if margem >= 0 else 'marca' if margem <= -W.QUEBRAR_MARCA else 'falhou', texto=teste.diz(E, r) + f"\n  (Conjuração da fé {int(vis)}; contra: 28 + força {W.forca(m['cat'])} + 2 por passo além do primeiro)\n" + txt[0].upper() + txt[1:] + '.')


def devolver(E, pid, iid):
    """devolve a peça maldita ao lugar dela (a pessoa tem de estar lá): a maldição que veio dela quebra, e a peça fica no chão, sem dono, ainda maldita (quem a puser em uso de novo...)"""
    p = E['gente'].get(pid) or sys.exit(f'não há a pessoa "{pid}"')
    if p['estado'] != 'vivo': sys.exit(f"{p['nome']} não age: {estado.morte_diz(E, p)}")
    estado.sem_luta(E); estado.em_cena(E, pid)
    it = E['itens']['itens'].get(iid) or sys.exit(f'não há o item "{iid}" no Livro de Itens')
    if it.get('dono') != pid: sys.exit(f"{it['nome']} não é de {p['nome']}")
    m = next((x for x in minhas(p) if x.get('de') == 'peça' and x.get('fonte') == iid), None)
    aqui = estado.onde(E, pid)
    if m is None or (m.get('condicao') or {}).get('tipo') != 'devolver':
        sys.exit(f"{it['nome']} não traz maldição que se quebre devolvendo" + ('' if m else f" (nada anda em {p['nome']} que tenha vindo dela)"))
    onde = m['condicao'].get('onde')
    if onde != aqui: sys.exit(f"o lugar {estado.de_nome(it['nome'])} não é aqui" + (f": é {estado.em(E, onde)}" if degrau(m) == 2 and onde in E['lugares'] else ' (quem lê a maldição diz onde é)'))
    ef = [['maldicao', pid, m['id'], 'quebra', f"devolveu {it['nome']}"], ['item', iid, 'uso', 'poe', None], ['item', iid, 'dono', 'poe', None], ['item', iid, 'onde', 'poe', aqui], ['item', iid, 'solto', 'poe', True],
          ['item', iid, 'historia', 'junta', f"Dia {E['relogio']['dia']}: {p['nome']} a devolveu {estado.em(E, aqui)}"]]
    estado.aplica(E, 'maldicao', ef, onde=aqui, quem=[pid], texto=f"{p['nome']} devolve {it['nome']} ao lugar dela: a maldição se desfaz")
    return f"{p['nome']} deixa {it['nome']} {estado.em(E, aqui)}, onde a peça estava: a maldição se desfaz. A peça fica no chão, ainda maldita."


def perdoa(E, alvo, mid, quem):
    """quem rogou desata sem teste"""
    q = E['gente'].get(alvo) or sys.exit(f'não há a pessoa "{alvo}"'); r = E['gente'].get(quem) or sys.exit(f'não há a pessoa "{quem}"')
    if r['estado'] != 'vivo': sys.exit(f"{r['nome']} {estado.morte_diz(E, r)}")
    estado.sem_luta(E)
    m = next((x for x in minhas(q) if x['id'] == mid), None) or sys.exit(f"{q['nome']} não tem a maldição \"{mid}\"")
    if m.get('quem') != quem: sys.exit(f"não foi {r['nome']} quem rogou {m['nome']}: só quem rogou desata")
    estado.aplica(E, 'maldicao', [['maldicao', alvo, mid, 'quebra', f"o perdão de {r['nome']}"]], onde=estado.onde(E, quem), quem=[quem, alvo], texto=f"{r['nome']} desata a maldição que rogou em {q['nome']}")
    return f"{r['nome']} desata a maldição: {q['nome']} está livre dela."


def cumpre(E, alvo, mid, como):
    """o Mestre atesta que a condição se cumpriu (evento "mestre")"""
    q = E['gente'].get(alvo) or sys.exit(f'não há a pessoa "{alvo}"')
    m = next((x for x in minhas(q) if x['id'] == mid), None) or sys.exit(f"{q['nome']} não tem a maldição \"{mid}\"")
    if not como.strip(): sys.exit('diga como a condição se cumpriu: `maldicao.py cumpre ALVO MID "como foi"`')
    estado.aplica(E, 'mestre', [['maldicao', alvo, mid, 'quebra', como]], onde=estado.onde(E, alvo), quem=[alvo], texto=f"a maldição de {q['nome']} se desfaz: {como}")
    return f"A maldição de {q['nome']} se desfaz: {como}."


# ---------- o Mestre põe ----------
def amaldicoa_peca(E, iid, nome, cat, tipo, onde=None, como=''):
    """o Mestre (ou o gerador) amaldiçoa uma peça: o molde dela, com a condição de devolvê-la a ONDE (sem onde: o lugar em que ela está, ou onde o dono está)"""
    it = E['itens']['itens'].get(iid) or sys.exit(f'não há o item "{iid}" no Livro de Itens')
    onde = onde or it.get('onde') or (estado.onde(E, it['dono']) if it.get('dono') else None)
    if onde not in E['lugares']: sys.exit(f'diga para onde a peça tem de voltar (onde=LUGAR)')
    mo = molde(nome, cat, tipo, dict(tipo='devolver', item=iid, onde=onde))
    estado.aplica(E, 'mestre', [['item', iid, 'maldita', 'poe', mo]], onde=onde, texto=f"{it['nome']} é maldita" + (f': {como}' if como else ''))
    return f"{it['nome']} fica maldita ({nome}, {FEM[mo['cat']]}, {tipo}): quem a puser em uso pega a maldição; quebra devolvendo-a {estado.em(E, onde)}."


def amaldicoa_lugar(E, lid, nome, cat, tipo, como=''):
    """o Mestre (ou o gerador) amaldiçoa um lugar: quem passa um bloco nele rola a força contra a Firmeza; quebra ficando 7 dias longe"""
    l = E['lugares'].get(lid) or sys.exit(f'não há o lugar "{lid}"')
    mo = molde(nome, cat, tipo, dict(tipo='sair', lugar=lid))
    estado.aplica(E, 'mestre', [['lugar', lid, 'maldito', 'poe', mo]], onde=lid, texto=f"{l['nome']} é um lugar maldito" + (f': {como}' if como else ''))
    return f"{l['nome']} fica maldito ({nome}, {FEM[mo['cat']]}, {tipo}): a cada bloco lá, o mundo rola a força dele contra a Firmeza de quem está."


# ---------- a mesa ----------
def voce(E):
    pid = estado.eu(E); p = E['gente'].get(pid) if pid else None
    if not isinstance(p, dict) or p.get('estado') != 'vivo': return []
    return list(dict.fromkeys(x for x in (diz(E, pid, m) for m in minhas(p)) if x))      # duas maldições que a pessoa só sente pesam igual: uma linha


def so_mestre(E):
    """toda maldição andando no mundo, e todo lugar e peça malditos (o Mestre vê tudo)"""
    L = [f"maldição de {diz(E, pid, m, mestre=True)}" for pid, p in E['gente'].items() if isinstance(p, dict) and p.get('estado') == 'vivo' for m in minhas(p)]
    L += [f"lugar maldito: {l['nome']} ({l['maldito']['nome']}, {FEM[l['maldito']['cat']]}, {l['maldito']['tipo']})" for l in E['lugares'].values() if isinstance(l.get('maldito'), dict)]
    L += [f"peça maldita: {i} {it['nome']} ({it['maldita']['nome']}, {FEM[it['maldita']['cat']]}, {it['maldita']['tipo']}); quebra: {diz_condicao(E, it['maldita']['condicao'])}"
          for i, it in E['itens']['itens'].items() if isinstance(it.get('maldita'), dict)]
    return L


def retomar(E):
    """o RETOMAR leva toda maldição do personagem que ele sente (a que ele não sabe fica no SÓ O MESTRE)"""
    L = voce(E)
    return ['**A maldição:** ' + ' · '.join(L)] if L else []


def recusa_fecha(E):
    """o turno não fecha com maldição do personagem no passo 4 ou mais sem uma pergunta aberta sobre ela"""
    pid = estado.eu(E); p = E['gente'].get(pid) if pid else None
    if not isinstance(p, dict) or p.get('estado') != 'vivo': return []
    textos = ' '.join(q.get('texto', '') for q in E['turno'].get('perguntas', [])).lower(); R = []
    for m in minhas(p):
        if m['passo'] >= M.MALDICAO_SEM_SARAR and 'maldi' not in textos and m['nome'].lower() not in textos:
            R.append(f"a maldição de {p['nome']} ({m['nome']}) está no passo {m['passo']} de 6: abra uma pergunta sobre ela (`turno.py pergunta`), que o jogador decide o que fazer")
    return R


# ---------- a linha de comando ----------
def main(a=None):
    a = sys.argv[1:] if a is None else list(a)
    op = dict(x.split('=', 1) for x in a if '=' in x); pos = [x for x in a if '=' not in x]
    cmds = ('ver', 'mestre', 'rito', 'devolver', 'perdoa', 'cumpre', 'poe', 'peca', 'lugar')
    if not pos or pos[0] not in cmds: print(__doc__); return
    falta = lambda o_que, exemplo: sys.exit(f'{o_que}: `python3 maldicao.py {exemplo}`')
    E = estado.carrega(); pid = op.get('quem') or estado.eu(E)
    if pid not in E['gente']: sys.exit(f'não há a pessoa "{pid}"')
    if pos[0] in ('ver', 'mestre'):
        alvo = pos[1] if len(pos) > 1 else estado.eu(E); q = E['gente'].get(alvo) or sys.exit(f'não há a pessoa "{alvo}"')
        L = [x for x in (diz(E, alvo, m, mestre=pos[0] == 'mestre') for m in minhas(q)) if x]
        print('\n'.join(L) or f"{q['nome']} não sente maldição nenhuma."); return
    if pos[0] == 'rito':
        if len(pos) < 2: falta('diga em quem é o rito (e quem o faz)', 'rito eu quem=nara')
        out = rito(E, pid, pos[1], pos[2] if len(pos) > 2 else None, paga=op.get('paga'))['texto']
    elif pos[0] == 'devolver': out = devolver(E, pid, pos[1] if len(pos) > 1 else falta('diga a peça', 'devolver i0031'))
    elif pos[0] == 'perdoa':
        if len(pos) < 3: falta('diga quem é perdoado e a maldição (o id dela)', 'perdoa eu m0003 quem=quiteria')
        out = perdoa(E, pos[1], pos[2], pid)
    elif pos[0] == 'cumpre':
        if len(pos) < 4: falta('diga quem, a maldição e como a condição se cumpriu', 'cumpre eu m0003 "levou a espada de volta à cova"')
        out = cumpre(E, pos[1], pos[2], pos[3])
    elif pos[0] == 'poe':
        if len(pos) < 6: falta('diga em quem, o nome, a categoria, o tipo e a condição', 'poe eu "a Mão Fria" Incomum míngua cumprir "a praga da bruxa"')
        mo = molde(pos[2], pos[3], pos[4], dict(tipo=pos[5]))
        if op.get('de', 'feitiço') not in M.MALDICAO_ORIGENS: sys.exit(f"a origem é uma de: {', '.join(M.MALDICAO_ORIGENS)}")
        q = E['gente'].get(pos[1]) or sys.exit(f'não há a pessoa "{pos[1]}"')
        cond = dict(tipo=pos[5], **({'quem': op['rogou']} if op.get('rogou') else {}))
        estado.aplica(E, 'mestre', poe(E, pos[1], mo, op.get('de', 'feitiço'), fonte=op.get('fonte'), quem=op.get('rogou'), condicao=cond), onde=estado.onde(E, pos[1]), quem=[pos[1]],
                      texto=f"o Mestre põe uma maldição em {q['nome']}" + (f": {pos[6]}" if len(pos) > 6 else ''))
        out = f"{q['nome']} pega {pos[2]} ({FEM[mo['cat']]}, {pos[4]}), no passo 1: {q['nome']} não sabe (do passo 2 desconfia)."
    elif pos[0] == 'peca':
        if len(pos) < 5: falta('diga a peça, o nome, a categoria e o tipo', 'peca i0031 "a Mão Fria" Incomum míngua onde=capela "a adaga do túmulo"')
        out = amaldicoa_peca(E, pos[1], pos[2], pos[3], pos[4], onde=op.get('onde'), como=pos[5] if len(pos) > 5 else '')
    else:
        if len(pos) < 4: falta('diga o nome, a categoria e o tipo da maldição do lugar', 'lugar "o Ar Parado" Comum azar "a capela caída"')
        out = amaldicoa_lugar(E, estado.onde(E, pid), pos[1], pos[2], pos[3], como=pos[4] if len(pos) > 4 else '')
    estado.grava(E)
    print(out)
    print(ato.ultima_linha(E, pid))


if __name__ == '__main__':
    import signal; hasattr(signal, 'SIGPIPE') and signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    main()
