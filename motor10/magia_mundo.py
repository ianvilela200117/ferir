#!/usr/bin/env python3
"""magia_mundo.py — MOTOR 10: A MAGIA FORA DA LUTA (etapa da magia, capítulo 14). Os números moram no tabelas_magia_mundo.py; os 24 feitiços e o truque, no tabelas.py.

  QUALQUER UM APRENDE MAGIA, como se aprende uma arma. Um feitiço se ESTUDA: blocos leves (truque 3; grau 1, 6; grau 2, 18; grau 3, 54; grau 4, 162), vezes o TALENTO
    na tradição dele, que contam como treino da tradição (a maestria sobe pela tabela das armas: 40, 160, 500, 1.500). Pede uma FONTE: quem o saiba e queira ensinar
    (cobra o salário dele por bloco, e só ensina dentro da jornada dele), um ESCRITO que o ensine, um SANTUÁRIO (os da fé, a quem tem voto) ou o ERMO DO LAÇO (os do verde).
  UMA TRADIÇÃO POR PESSOA: o mago (arcano) entra estudando; o clérigo (fé) faz um VOTO num santuário (da lâmina: não põe em uso arma de corte nem de ponta; da pobreza:
    não guarda mais de 50 de prata na virada; do socorro); o druida (verde) faz o LAÇO com um ermo vizinho; a bruxa (pacto) faz o PACTO no escuro e nasce devendo.
    Quebrar o voto apaga a Mana e deixa uma marca (maldição de juramento). A dívida da bruxa sobe com o feitiço forte e a praga, paga-se em PV ou queimando matéria,
    e acima de Vontade ÷ 10 vira maldição nela.
  A MANA FORA DA LUTA, por bloco: dormindo, um quarto da máxima; descansando, um oitavo; acordado e leve, 1; no bloco pesado, nada. O clérigo só a recobra com a PRECE
    (1 bloco por dia: no santuário enche, fora dele, metade); o druida, em dobro no ermo e a metade entre muros; a bruxa, sozinha só até a metade (o resto, pago).
    A maldição do passo 4 não deixa a Mana voltar.
  LANÇAR FORA DA LUTA: a cura (1d8 × 6 × 3^(categoria do foco − ferida mais funda), dentro do teto do dia), a bênção antes da luta, a seiva (dobra a cura da noite).
  OS RITOS (1 bloco leve cada): a prece; LER (a maldição, o dom ou a peça: quem sabe "ler", ou a fé de Treinado); quebrar a maldição (maldicao.py rito); a PRAGA
    (a bruxa, pelo toque: Conjuração contra a Firmeza); a água benta e a bênção da arma (no santuário). TRATAR a ferida (o ofício cura: 1 bloco e 1 remédio, um por
    dia: soma um dia de repouso às feridas). O SERVIÇO de pessoa a pessoa: o PERSONAGEM paga a quem presta (a prata muda de mão); a gente do mundo não procura serviço
    sozinha nesta etapa, e o que se faz por ela sai sem cobrança (ninguém fica rico benzendo a vila). O jornal do santuário entra na jornada.

Uso (o personagem do jogador, ou quem=ID):
  python3 magia_mundo.py ver [ID]                           a magia de alguém: a Mana, a tradição, o que sabe, o que estuda, o voto, o laço, a dívida
  python3 magia_mundo.py estudar FEITICO com=PESSOA|escrito=ITEM|santuario|ermo [blocos=N]     estuda um feitiço (sem N: até aprender, ou até o corpo parar)
  python3 magia_mundo.py voto lâmina|pobreza|socorro       faz o voto da fé, num santuário (1 bloco)
  python3 magia_mundo.py laco ERMO                          faz o laço do verde com um ermo vizinho (1 bloco)
  python3 magia_mundo.py pacto                              faz o pacto (no escuro: madrugada ou noite; 1 bloco): a bruxa nasce devendo
  python3 magia_mundo.py prece                              a prece do clérigo (1 bloco por dia): no santuário a Mana enche; fora dele, metade
  python3 magia_mundo.py paga N pv|divida                   a bruxa paga a Mana acima da metade (2% do PV máximo por ponto, ou 1 de dívida a cada 4)
  python3 magia_mundo.py divida N pv|osso|erva              a bruxa paga a dívida (rito de 1 bloco): em PV, ou queimando matéria da categoria do foco
  python3 magia_mundo.py lancar cura|bênção|seiva [alvo=ID] [paga=N]     lança fora da luta (o personagem ajudado paga a quem lança o preço da tabela, ou o combinado: paga=N)
  python3 magia_mundo.py ler maldicao|dom|peca [ALVO|ITEM] [paga=N]       o rito de ler (1 bloco); o mesmo preço nos serviços (só o personagem paga; para os outros sai de graça)
  python3 magia_mundo.py praga ALVO [tipo=míngua] ["Nome"]  a bruxa roga uma praga pelo toque (rito de 1 bloco; a dívida sobe a categoria mais 1)
  python3 magia_mundo.py agua N                             o clérigo benze N de água (num santuário; cada uma: 1 de erva Comum e 2 de Mana)
  python3 magia_mundo.py benzer ARMA [paga=N]               o clérigo benze uma arma (num santuário): conta inteira contra o que não tem corpo por 7 dias
  python3 magia_mundo.py tratar PACIENTE [paga=N]           trata as feridas de alguém (1 bloco, 1 remédio; um tratamento por paciente por dia)
  python3 magia_mundo.py jornal N                           N blocos a serviço do santuário (o salário da mão de fé, até a jornada)
  python3 magia_mundo.py compra BEM N de=QUEM [preco=P]     compra de pessoa a pessoa o que alguém leva (o veneno de lâmina, que a loja não negocia: é crime)
  python3 magia_mundo.py santuario NIVEL|nada "como foi"    o Mestre registra o santuário do lugar (0 a 4)
FEITICO: luz · arcano: seta prender escudo lança-de-fogo bola-de-fogo raio · fé: cura bênção amparo castigo guarda quebrar-maldição
         · verde: raízes espinho névoa afugentar seiva chamar · pacto: mau-olhado medo sangria ler nó praga
"""
import math, secrets, sys
import tabelas as T
import tabelas_mundo as M
import tabelas_magia_mundo as W
import estado, ato, corpo, teste, talento

tantos = estado.tantos
FEM = ['Comum', 'Incomum', 'Rara', 'Épica', 'Única', 'Lendária', 'Mítica', 'Primordial']
def _arred(x): return int(math.floor(x + 0.5))
def _nf(f): return T.nome_feitico(f)


# ---------- ler a pessoa ----------
def trad_de(p, f):
    """a tradição de um feitiço para esta pessoa: a da tabela; o truque (de todas), a tradição da pessoa, ou o arcano"""
    d = T.FEITICOS[f]['de']
    return (p.get('tradicao') or W.TRUQUE_TRADICAO) if d == 'todas' else d


def mao(p, t): m = p.get('maestria'); return m.get(t, 0) if isinstance(m, dict) else 0


def estudo_diz(p, f, n, mestre=False):
    """o estudo de um feitiço em palavras: n de quantos blocos. O Mestre vê os de verdade (vezes o talento na tradição); a pessoa, os mesmos se o talento da tradição
    já apareceu, e senão os da tabela, os de todos (o talento é segredo do Mestre até aparecer: 10.6). Quem passou dos da tabela sem aprender lê que ainda não aprendeu."""
    t = trad_de(p, f); base = W.ESTUDO[T.FEITICOS[f]['grau']]
    q = talento.blocos(p, t, base) if mestre or talento.aparece(p, talento.caminho_de(t)) else base
    return f"{n} de {q} blocos" if n < q else f"{tantos(n, 'bloco')}, {'os' if n == q else 'mais do que os'} {q} da tabela, e ainda não aprendeu"


def foco_de(E, pid):
    """o foco em uso (inteiro), ou None"""
    it = estado.pecas(E, pid)['foco']
    return it if it and it['dur'][0] > 0 else None


def bonus_foco(E, pid, t):
    """o que o foco dá na Conjuração desta tradição: o bônus da categoria; o de outra tradição, uma categoria abaixo; sem foco (ou abaixo do Comum), Comum com −4"""
    it = foco_de(E, pid)
    if not it: return W.SEM_FOCO
    c = it['cat'] - (0 if t in T.FOCOS[it['forma']]['de'] else W.FOCO_OUTRO)
    return T.BON[c] if c >= 0 else W.SEM_FOCO


def cat_foco(E, pid, t):
    """a categoria em que o foco rende para esta tradição (a da cura do feitiço): a dele; de outra tradição, uma abaixo; sem foco, Comum"""
    it = foco_de(E, pid)
    return max(0, it['cat'] - (0 if t in T.FOCOS[it['forma']]['de'] else W.FOCO_OUTRO)) if it else 0


def conjuracao(E, pid, t, visivel=False):
    """a Conjuração fora da luta (a base comum, tabelas.conjuracao): a maestria da tradição, o dom nela (o que a pessoa viu, com `visivel`), metade do bônus do atributo
    da tradição, e o foco. A luta tem a dela (a frente da luta)."""
    p = E['gente'][pid]; dom = talento.dom_visto(p, t) if visivel else talento.dom(p, t)
    return mao(p, t) + dom + (p['atributos'][T.TRADICOES[t]] // 10) / 2 + bonus_foco(E, pid, t)


def mana_vista(p):
    """a Mana como a pessoa a vê: (a de agora, a máxima), sem o dom de tradição que ela ainda não viu (o estado.mana_max soma o dom de verdade; a mesa não pode)"""
    return estado.mana(p, visivel=True), estado.mana_max(p, visivel=True)


def diz_mana(p): a, b = mana_vista(p); return f"{a} de {b}"


def voto_vale(p): v = p.get('voto'); return isinstance(v, dict) and v.get('quebrado') is None
def laco_vale(E, p): l = p.get('laco'); return isinstance(l, dict) and l.get('ermo') in E['lugares']


def poder(E, p, t):
    """por que esta pessoa não tem o poder da tradição (o voto quebrado, sem laço), ou None"""
    if t == 'fé' and not voto_vale(p): return 'a fé pede um voto inteiro (`magia_mundo.py voto`)' + (' (o voto está quebrado)' if isinstance(p.get('voto'), dict) else '')
    if t == 'verde' and not laco_vale(E, p): return 'o verde pede o laço com um ermo (`magia_mundo.py laco ERMO`)'
    return None


def fartura(E, lid):
    """a fartura de um ermo (0 a 1): a média da contagem ÷ o teto das espécies e da matéria dele"""
    l = E['lugares'].get(lid) or {}; xs = []
    for conta, teto in (('bichos', 'teto'), ('coleta', 'coleta_teto')):
        for k, t in (l.get(teto) or {}).items():
            if isinstance(t, (int, float)) and t > 0: xs.append(min(1.0, (l.get(conta) or {}).get(k, 0) / t))
    return sum(xs) / len(xs) if xs else 1.0


def pena_laco(E, pid):
    """o que o laço tira da Conjuração do druida (a luta lê): a fartura do ermo do laço abaixo de 40%, −2; abaixo de 10%, −4"""
    p = E['gente'][pid]
    if p.get('tradicao') != 'verde' or not laco_vale(E, p): return 0
    f = fartura(E, p['laco']['ermo'])
    return next((v for lim, v in W.FARTURA if f < lim), 0)


def lancador(E, pid, f, fora_ok=False):
    """quem lança `f` fora da luta: presente (no lugar onde mora; com `fora_ok`, também na saída ao ermo: o que não gasta bloco), sabe o feitiço, tem a Mana e o poder da tradição"""
    if fora_ok:
        p = E['gente'].get(pid) or sys.exit(f'não há a pessoa "{pid}"')
        if p['estado'] != 'vivo': sys.exit(f"{p['nome']} não age: {estado.morte_diz(E, p)}")
        estado.sem_luta(E); estado.em_cena(E, pid); p = E['gente'][pid]
    else: p = estado.presente(E, pid, 'lançar aqui')
    t = trad_de(p, f)
    if f not in (p.get('feiticos') or []): sys.exit(f"{p['nome']} não sabe {_nf(f)}")
    pq = poder(E, p, t)
    if pq: sys.exit(f"{p['nome']} não tem o poder: {pq}")
    custo = T.FEITICOS[f]['mana']
    if estado.mana(p) < custo: sys.exit(f"{_nf(f).capitalize()} custa {custo} de Mana; {p['nome']} tem {diz_mana(p)}")
    return p


def sobe(E, pid, t):
    """a maestria de uma tradição (ou da cura) sobe pela tabela das armas (40, 160, 500, 1.500 blocos), vezes o talento, até o teto dele; de Mestre para cima, com um FEITO
    que o Mestre registra (marca.feito_TRADICAO)"""
    p = E['gente'][pid]; tem = mao(p, t); bl = (p.get('treino') or {}).get(t, 0); txt = ''
    for grau in sorted(M.MAESTRIA_BLOCOS):
        quer = talento.pede(p, t, M.MAESTRIA_BLOCOS, grau)
        if grau <= tem: continue
        if quer is None:
            if bl >= M.MAESTRIA_BLOCOS[grau]: txt = f" (a mão não sobe mais em {t}: o talento para em {T.MAESTRIAS[talento.teto(p, t)]})"
            break
        if bl < quer: continue
        if grau >= M.MAESTRIA_FEITO and (p.get('marca') or {}).get(f'feito_{t}', 0) < grau: txt = f' (tem os blocos para {T.MAESTRIAS[grau]} em {t}; falta o feito)'; break
        estado.aplica(E, 'treinar', [['pessoa', pid, 'maestria.' + t, 'poe', grau]], onde=p['lugar'], quem=[pid], texto=f"{p['nome']} chega a {T.MAESTRIAS[grau]} em {t}")
        p = E['gente'][pid]; tem = grau; txt = f'. MAESTRIA: {T.MAESTRIAS[grau]} em {t}'
    return txt


def _junto(E, pid, alvo):
    """o alvo de um feitiço ou de um rito: a própria pessoa, ou quem está com ela, vivo"""
    if alvo in (None, pid): return pid
    q = E['gente'].get(alvo) or sys.exit(f'não há a pessoa "{alvo}"')
    if q['estado'] != 'vivo': sys.exit(f"{q['nome']} {estado.morte_diz(E, q)}")
    if estado.onde(E, alvo) != estado.onde(E, pid): sys.exit(f"{q['nome']} não está com {E['gente'][pid]['nome']}")
    estado.em_cena(E, alvo); return alvo


def preco_dito(v, o_que='paga='):
    """o preço que alguém combina (paga=, preco=): um número inteiro de prata, 0 ou mais. Recusa o resto com uma frase simples, antes de montar o evento."""
    if isinstance(v, bool) or not ((isinstance(v, int) and v >= 0) or (isinstance(v, str) and v.strip().isdigit())):
        sys.exit(f'o preço ({o_que}) é um número inteiro de prata, 0 ou mais (veio "{v}")')
    return int(v)


def preco_servico(E, de, para, tabela, paga_=None):
    """O PREÇO DE UM SERVIÇO DE PESSOA A PESSOA, de quem é ajudado (`de`) para quem presta (`para`). SÓ O PERSONAGEM PAGA SERVIÇO: a gente do mundo não procura serviço
    sozinha nesta etapa (REGRAS 14.7 e 16.7), e o que se faz por ela sai sem cobrança (com paga=, recusa). O personagem paga o preço da tabela, ou o combinado (paga=, 0 ou mais)."""
    dito = None if paga_ is None else preco_dito(paga_)
    if de == para: return 0
    if de != estado.eu(E):
        if dito: sys.exit(f"{E['gente'][de]['nome']} não paga o serviço: a gente do mundo não procura serviço sozinha, e o que se faz por ela sai sem cobrança (tire o paga=)")
        return 0
    return tabela if dito is None else dito


def _paga(E, de, para, preco):
    """a paga de um serviço, de pessoa a pessoa (a prata só muda de mão; o preço sai do preco_servico). Recusa se quem paga não tem."""
    if de == para or not preco: return []
    q = E['gente'][de]
    if q['moedas'] < preco: sys.exit(f"o serviço custa {preco} de prata; {q['nome']} tem {q['moedas']}")
    return [['pessoa', de, 'moedas', 'soma', -preco], ['pessoa', para, 'moedas', 'soma', preco]]


def _rito(E, pid, mais, texto, com=(), esforco='leve'):
    """o bloco do rito (1 bloco leve); recusa se o corpo não deixou fazer"""
    n, pq = ato.passa(E, pid, W.RITO_BLOCOS, 'rito', esforco=esforco, mais=lambda i: mais, com=tuple(c for c in com if c != pid), texto=texto)
    if not n: sys.exit(f"o rito não se fez: {pq}")
    return pq


# ---------- estudar ----------
def _fonte(E, pid, f, t, fonte):
    """confere a fonte do estudo e diz quem ensina (ou None). fonte: {'com': id} | {'escrito': id} | 'santuario' | 'ermo'"""
    p = E['gente'][pid]
    if isinstance(fonte, dict) and fonte.get('com'):
        mid = fonte['com']; m = E['gente'].get(mid) or sys.exit(f'não há a pessoa "{mid}"')
        if mid == pid: sys.exit('ninguém se ensina: estude por um escrito, num santuário ou no ermo do laço')
        if m['estado'] != 'vivo' or m['lugar'] != p['lugar'] or estado.fora(E, mid): sys.exit(f"{m['nome']} não está aqui para ensinar")
        if f not in (m.get('feiticos') or []): sys.exit(f"{m['nome']} não sabe {_nf(f)}: não ensina o que não sabe")
        return mid
    if isinstance(fonte, dict) and fonte.get('escrito'):
        it = E['itens']['itens'].get(fonte['escrito']) or sys.exit(f"não há o item \"{fonte['escrito']}\" no Livro de Itens")
        if it.get('dono') != pid or it.get('tipo') != 'escrito': sys.exit(f"{it['nome']} não é um escrito de {p['nome']}")
        if f not in it.get('feiticos', []): sys.exit(f"{it['nome']} não ensina {_nf(f)} (ensina: {', '.join(_nf(x) for x in it['feiticos'])})")
        return None
    if fonte == 'santuario':
        if t != 'fé': sys.exit('o santuário ensina os feitiços da fé')
        if E['lugares'][p['lugar']].get('santuario') is None: sys.exit(f"{E['lugares'][p['lugar']]['nome']} não tem santuário")
        if not voto_vale(p): sys.exit(f"o santuário ensina a quem tem voto: {p['nome']} não tem (`magia_mundo.py voto`)")
        return None
    if fonte == 'ermo':
        if t != 'verde': sys.exit('o ermo do laço ensina os feitiços do verde')
        if not laco_vale(E, p): sys.exit(f"{p['nome']} não tem laço com ermo nenhum (`magia_mundo.py laco ERMO`)")
        return None
    sys.exit('diga de onde vem o estudo: com=PESSOA (quem ensina), escrito=ITEM, santuario (a fé) ou ermo (o verde)')


def estudar(E, pid, f, fonte, blocos=None):
    """estuda um feitiço, bloco a bloco (leve): cada bloco conta como treino da tradição; quem ensina cobra o salário dele por bloco, dentro da jornada dele.
    Para quando aprende, quando acabam os blocos pedidos, quando quem ensina não ensina mais hoje, ou quando o corpo pede."""
    if f not in T.FEITICOS: sys.exit(f'feitiço desconhecido: "{f}" (os que há: {", ".join(T.FEITICOS)})')
    p = estado.presente(E, pid, 'estudar aqui')
    if f in (p.get('feiticos') or []): sys.exit(f"{p['nome']} já sabe {_nf(f)}")
    t = trad_de(p, f); tem_t = p.get('tradicao')
    if tem_t and t != tem_t and T.FEITICOS[f]['de'] != 'todas': sys.exit(f"{p['nome']} segue o {tem_t}: uma tradição por pessoa ({_nf(f)} é do {t})")
    if not tem_t and t != 'arcano' and T.FEITICOS[f]['de'] != 'todas':
        sys.exit(f"{_nf(f).capitalize()} é do {t}: entra-se nele " + dict(fé='pelo voto, num santuário (`magia_mundo.py voto`)', verde='pelo laço com um ermo (`magia_mundo.py laco ERMO`)', pacto='pelo pacto (`magia_mundo.py pacto`)')[t])
    pq = poder(E, p, t) if T.FEITICOS[f]['de'] != 'todas' else None
    if pq: sys.exit(f"{p['nome']} não tem o poder: {pq}")
    mestre = _fonte(E, pid, f, t, fonte); grau = T.FEITICOS[f]['grau']; quer = talento.blocos(p, t, W.ESTUDO[grau])
    preco = M.SALARIO[E['gente'][mestre].get('grau_oficio', 'diarista')] if mestre else 0
    feitos = 0; pq = None; pagou = 0; alvo = None if blocos is None else int(blocos)
    while alvo is None or feitos < alvo:
        p = E['gente'][pid]; ja = int(((p.get('marca') or {}).get('estudo') or {}).get(f, 0))
        if ja >= quer: break
        if mestre:
            m = E['gente'][mestre]
            if ato.jornada(E, mestre) >= M.JORNADA: pq = f"{m['nome']} já deu a jornada de hoje ({M.JORNADA} blocos pagos): ensina de novo amanhã"; break
            if p['moedas'] < preco: pq = f"a lição custa {preco} de prata por bloco; {p['nome']} tem {p['moedas']}"; break
        def mais(i, ja=ja):
            est = dict((E['gente'][pid].get('marca') or {}).get('estudo') or {}); est[f] = ja + 1
            ef = [['pessoa', pid, 'treino.' + t, 'soma', 1], ['pessoa', pid, 'marca.estudo', 'poe', est]]
            if not E['gente'][pid].get('tradicao') and T.FEITICOS[f]['de'] != 'todas': ef.append(['pessoa', pid, 'tradicao', 'poe', t])
            if mestre: ef += [['pessoa', pid, 'moedas', 'soma', -preco], ['pessoa', mestre, 'moedas', 'soma', preco], ['pessoa', mestre, 'marca.jornada_dia', 'poe', E['relogio']['dia']], ['pessoa', mestre, 'marca.jornada', 'poe', ato.jornada(E, mestre) + 1]]
            return ef
        n, pq = ato.passa(E, pid, 1, 'estudar', esforco=W.ESTUDO_ESFORCO, mais=mais, com=(mestre,) if mestre else (), texto=f"{p['nome']} estuda {_nf(f)}" + (f" com {E['gente'][mestre]['nome']}" if mestre else ''))
        feitos += n; pagou += preco * n
        if not n or pq: break
    p = E['gente'][pid]; ja = int(((p.get('marca') or {}).get('estudo') or {}).get(f, 0)); txt = f"{p['nome']} estuda {_nf(f)} {tantos(feitos, 'bloco')}" + (f" (pagou {pagou} de prata)" if pagou else '')
    if ja >= quer and p['estado'] == 'vivo':
        est = dict((p.get('marca') or {}).get('estudo') or {}); est.pop(f, None)
        estado.aplica(E, 'estudar', [['pessoa', pid, 'feitico', 'aprende', f], ['pessoa', pid, 'marca.estudo', 'poe', est]], onde=p['lugar'], quem=[pid], texto=f"{p['nome']} aprende {_nf(f)}")
        txt += f". APRENDEU {_nf(f).upper()}"
    elif p['estado'] == 'vivo': txt += ': ' + estudo_diz(p, f, ja)          # o número que a pessoa conhece: o do talento só depois que ele aparece (10.6)
    return dict(feitos=feitos, aprendeu=ja >= quer, texto=txt + sobe(E, pid, t) + (f'. PAROU: {pq}' if pq else '.'))


def aprende(E, pid, f, como=''):
    """o Mestre (ou o gerador) registra que alguém sabe um feitiço (evento "mestre"); quem não segue tradição passa a seguir a do feitiço (o truque não muda a tradição)"""
    if f not in T.FEITICOS: sys.exit(f'feitiço desconhecido: "{f}" (os que há: {", ".join(T.FEITICOS)})')
    p = E['gente'].get(pid) or sys.exit(f'não há a pessoa "{pid}"'); t = T.FEITICOS[f]['de']
    if p.get('tradicao') and t not in ('todas', p['tradicao']): sys.exit(f"{p['nome']} segue o {p['tradicao']}: {_nf(f)} é do {t}")
    ef = [['pessoa', pid, 'feitico', 'aprende', f]] + ([['pessoa', pid, 'tradicao', 'poe', t]] if not p.get('tradicao') and t != 'todas' else [])
    if not estado.aplica(E, 'mestre', ef, onde=p['lugar'], quem=[pid], texto=f"{p['nome']} sabe {_nf(f)}" + (f': {como}' if como else '')): return f"{p['nome']} já sabia {_nf(f)}."
    return f"{p['nome']} sabe {_nf(f)}."


# ---------- entrar numa tradição ----------
def _entra(E, p, t):
    if p.get('tradicao') and p['tradicao'] != t: sys.exit(f"{p['nome']} segue o {p['tradicao']}: uma tradição por pessoa")


def voto(E, pid, qual):
    """o voto da fé, feito num santuário (1 bloco): a pessoa entra na fé (ou renova o voto, se o antigo quebrou e a marca dele já saiu)"""
    if qual not in M.VOTOS: sys.exit(f'o voto é um de: {", ".join(M.VOTOS)}')
    p = estado.presente(E, pid, 'fazer voto aqui'); _entra(E, p, 'fé'); lid = p['lugar']
    if E['lugares'][lid].get('santuario') is None: sys.exit(f"{E['lugares'][lid]['nome']} não tem santuário: o voto se faz num")
    if voto_vale(p): sys.exit(f"{p['nome']} já tem o voto {p['voto']['qual']}")
    if any(m.get('de') == 'juramento' for m in p.get('maldicoes') or [] if isinstance(m, dict)): sys.exit(f"{p['nome']} ainda carrega a marca do voto quebrado: só depois da penitência")
    arma = estado.pecas(E, pid)['arma']; arma2 = estado.pecas(E, pid)['arma2']
    if qual == 'lâmina' and any(a and T.FAMILIAS[a['familia']]['golpe'] in W.VOTO_LAMINA for a in (arma, arma2)): sys.exit('o voto da lâmina pede as mãos sem fio nem ponta: guarde a arma antes (`ato.py tirar ITEM`)')
    da = 'do' if qual == 'socorro' else 'da'
    _rito(E, pid, [['pessoa', pid, 'tradicao', 'poe', 'fé'], ['pessoa', pid, 'voto', 'poe', dict(qual=qual, santuario=lid, dia=E['relogio']['dia'])]], f"{p['nome']} faz o voto {da} {qual}")
    regra = dict(lâmina='não pôr em uso arma de corte nem de ponta', pobreza=f'não guardar mais de {W.VOTO_POBREZA} de prata na virada (o resto vai ao santuário)', socorro='não recusar cura pedida')[qual]
    return f"{p['nome']} faz o voto {da} {qual} {estado.em(E, lid)}: {regra}. Quebrar o voto apaga a Mana e deixa uma marca."


def laco(E, pid, ermo):
    """o laço do verde com um ermo vizinho (1 bloco): a Mana do druida volta em dobro no ermo, e a força dele segue a fartura do ermo"""
    p = estado.presente(E, pid, 'fazer o laço'); _entra(E, p, 'verde')
    l = E['lugares'].get(ermo) or sys.exit(f'não há o lugar "{ermo}"')
    if l.get('tipo') != 'ermo': sys.exit(f"{l['nome']} não é ermo: o laço é com o mato, o brejo, a serra")
    if ermo not in (E['lugares'][p['lugar']].get('vizinhos') or []): sys.exit(f"{l['nome']} não é vizinho {estado.de(E, p['lugar'])}")
    if laco_vale(E, p) and p['laco']['ermo'] == ermo: sys.exit(f"{p['nome']} já tem laço com {l['nome']}")
    _rito(E, pid, [['pessoa', pid, 'tradicao', 'poe', 'verde'], ['pessoa', pid, 'laco', 'poe', dict(ermo=ermo, dia=E['relogio']['dia'])]], f"{p['nome']} faz o laço com {l['nome']}")
    return f"{p['nome']} faz o laço com {l['nome']} (fartura {fartura(E, ermo):.0%}). Se o ermo for caçado até o fim, a força do laço cai."


def pacto(E, pid):
    """o pacto (no escuro; 1 bloco): a pessoa entra no pacto, e nasce devendo"""
    p = estado.presente(E, pid, 'fazer o pacto'); _entra(E, p, 'pacto')
    if p.get('tradicao') == 'pacto': sys.exit(f"{p['nome']} já tem o pacto")
    if E['relogio']['bloco'] not in W.PACTO_BLOCOS: sys.exit('o pacto se faz no escuro: na madrugada ou na noite')
    _rito(E, pid, [['pessoa', pid, 'tradicao', 'poe', 'pacto'], ['pessoa', pid, 'divida', 'soma', W.PACTO_ABRE]], f"{p['nome']} faz um rito no escuro")
    return f"{p['nome']} faz o pacto: deve {W.PACTO_ABRE}. A dívida acima de {p['atributos']['Vontade'] // W.DIVIDA_LIMITE} vira maldição."


# ---------- a Mana fora da luta ----------
def bloco(E, pid, esforco, dorme):
    """os efeitos de UM bloco em quem age, vai junto ou espera: a volta da Mana (pela tradição) e a seiva que dobra a cura da noite. Quem tem a Mana cheia não ganha efeito:
    a pessoa comum (sem magia) passa o bloco igual a hoje."""
    p = E['gente'][pid]
    if p.get('estado') != 'vivo': return []
    ef = []; mk = p.get('marca') or {}; t = estado.agora(E)
    sv = mk.get('seiva')
    if dorme and isinstance(sv, int) and not isinstance(sv, bool) and sv >= t:             # a seiva: a cura deste bloco dormido vale em dobro (as mesmas condições da noite)
        dia = E['relogio']['dia']; curou = mk.get('curou', 0) if mk.get('curou_dia') == dia else 0
        if p['corpo']['fome'] < M.LIMIARES['fome'][0] and curou < M.CURA_DIA and p['pv'] < estado.pv_max(p) and corpo.passo_maldicao(p) < M.MALDICAO_SEM_NOITE:
            ef.append(['pessoa', pid, 'pv', 'soma', max(1, int(estado.pv_max(p) * M.CURA_BLOCO)) * (W.SEIVA - 1)])
    if p.get('mana') is None or corpo.passo_maldicao(p) >= M.MALDICAO_SEM_SARAR: return ef      # a Mana que não está escrita é a cheia; a maldição do passo 4 não a deixa voltar
    q = _volta(p, estado.mana_max(p), estado.mana(p), esforco, dorme, E['lugares'].get(estado.onde(E, pid), {}).get('tipo'))
    if q > 0: ef.append(['pessoa', pid, 'mana', 'soma', q])
    return ef


def _volta(p, mx, m, esforco, dorme, tipo):
    """a Mana que UM bloco devolve fora da luta, da Mana `m` de agora (máxima `mx`): dormindo um quarto da máxima, descansando um oitavo, acordado e leve 1, pesado nada;
    o druida em dobro no ermo e a metade entre muros (`tipo`: o tipo do lugar onde está); a bruxa, sozinha só até a metade. O clérigo, nunca (só a prece)."""
    tr = p.get('tradicao')
    if m >= mx or tr == 'fé': return 0
    q = max(1, _arred(mx * W.MANA_DORME)) if dorme else max(1, _arred(mx * W.MANA_DESCANSO)) if esforco == 'descanso' else W.MANA_ACORDADO.get(esforco, 0)
    if tr == 'verde':
        if tipo == 'ermo': q = _arred(q * W.MANA_ERMO)
        elif tipo in W.MUROS: q = int(q * W.MANA_MUROS)
    if tr == 'pacto': q = max(0, min(q, int(mx * W.PACTO_SOZINHA) - m))
    return q


def casa(E, pid, noites):
    """O DESCANSO EM CASA (o gancho "casa": corpo.casa chama, no evento em que quem NÃO é o personagem volta à cena): a Mana que voltou nas `noites` (dias inteiros) que a pessoa
    passou em casa, fora de cena. Cada dia vale CASA_SONO blocos dormidos e o resto acordado, parado, pela regra de cada bloco (o druida segue o lugar onde mora; a bruxa,
    sozinha, só até a metade); o clérigo de voto inteiro reza a prece do dia em casa (no santuário enche; longe dele, a metade). A maldição do passo 4 não deixa voltar."""
    p = E['gente'][pid]
    if not noites or p.get('mana') is None or corpo.passo_maldicao(p) >= M.MALDICAO_SEM_SARAR: return []
    mx = estado.mana_max(p); m0 = m = estado.mana(p); lid = p['lugar']; tipo = E['lugares'].get(lid, {}).get('tipo')
    for _ in range(noites):
        if m >= mx: break
        if p.get('tradicao') == 'fé':
            if not voto_vale(p): break
            m = mx if E['lugares'].get(lid, {}).get('santuario') is not None else min(mx, m + int(mx * W.PRECE_FORA))
            continue
        for k in range(M.CASA_NOITE):
            m = min(mx, m + _volta(p, mx, m, W.CASA_ESFORCO, k < W.CASA_SONO, tipo))
    if m <= m0: return []
    return [['pessoa', pid, 'mana', 'soma', m - m0]] + ([['pessoa', pid, 'marca.prece_dia', 'poe', E['relogio']['dia']]] if p.get('tradicao') == 'fé' else [])      # a prece de hoje foi a de casa


def prece(E, pid):
    """a prece do clérigo (1 bloco, uma por dia): no santuário a Mana enche; fora dele, volta a metade da máxima"""
    p = estado.presente(E, pid, 'rezar aqui')
    if p.get('tradicao') != 'fé': sys.exit(f"{p['nome']} não segue a fé: a prece é do clérigo")
    pq = poder(E, p, 'fé')
    if pq: sys.exit(f"{p['nome']} não tem o poder: {pq}")
    if (p.get('marca') or {}).get('prece_dia') == E['relogio']['dia']: sys.exit(f"{p['nome']} já rezou hoje: a prece é uma por dia")
    if corpo.passo_maldicao(p) >= M.MALDICAO_SEM_SARAR: sys.exit(f"a maldição de {p['nome']} não deixa a Mana voltar (passo {corpo.passo_maldicao(p)})")
    santo = E['lugares'][p['lugar']].get('santuario') is not None; mx = estado.mana_max(p); m0 = estado.mana(p); antes = diz_mana(p)
    q = mx - m0 if santo else min(mx - m0, int(mx * W.PRECE_FORA))
    _rito(E, pid, [['pessoa', pid, 'marca.prece_dia', 'poe', E['relogio']['dia']], ['pessoa', pid, 'treino.fé', 'soma', 1]] + ([['pessoa', pid, 'mana', 'soma', q]] if q else []), f"{p['nome']} reza")
    return f"{p['nome']} reza {'no santuário' if santo else 'longe do santuário'}: Mana {antes} → {diz_mana(E['gente'][pid])}" + sobe(E, pid, 'fé')


def paga(E, pid, n, com='pv'):
    """a bruxa paga a Mana acima da metade (rito de 1 bloco): 2% do PV máximo por ponto, ou 1 de dívida a cada 4 pontos"""
    p = estado.presente(E, pid, 'pagar a Mana')
    if p.get('tradicao') != 'pacto': sys.exit(f"{p['nome']} não tem pacto: a Mana dela volta sozinha")
    n = int(n); mx = estado.mana_max(p); m0 = estado.mana(p); n = min(n, mx - m0); antes = diz_mana(p)
    if n < 1: sys.exit(f"a Mana de {p['nome']} já está cheia ({antes})")
    if com == 'pv':
        custo = math.ceil(n * W.PACTO_PV * estado.pv_max(p))
        if custo >= p['pv']: sys.exit(f"{n} de Mana custam {custo} de PV; {p['nome']} tem {p['pv']}: o pacto não cobra a vida inteira")
        ef = [['pessoa', pid, 'pv', 'soma', -custo]]; diz = f"{custo} de PV"
    elif com == 'divida': custo = math.ceil(n / W.PACTO_DIVIDA); ef = [['pessoa', pid, 'divida', 'soma', custo]]; diz = f"{custo} de dívida"
    else: sys.exit('paga-se em pv ou em divida')
    _rito(E, pid, ef + [['pessoa', pid, 'mana', 'soma', n]], f"{p['nome']} faz um rito no escuro")
    return f"{p['nome']} paga {diz}: Mana {antes} → {diz_mana(E['gente'][pid])}" + (f" (dívida {E['gente'][pid].get('divida', 0)})" if com == 'divida' else '')


def paga_divida(E, pid, n, com='pv'):
    """a bruxa paga a dívida (rito de 1 bloco): 1 ponto a cada 5% do PV máximo, ou a cada 4 de osso ou de erva da categoria do foco"""
    p = estado.presente(E, pid, 'pagar a dívida'); n = int(n); dv = p.get('divida') or 0
    if n < 1 or not dv: sys.exit(f"{p['nome']} não deve nada" if not dv else 'diga quanto pagar (1 ou mais)')
    n = min(n, dv)
    if com == 'pv':
        custo = n * max(1, math.ceil(W.DIVIDA_PV * estado.pv_max(p)))
        if custo >= p['pv']: sys.exit(f"pagar {n} custa {custo} de PV; {p['nome']} tem {p['pv']}")
        ef = [['pessoa', pid, 'pv', 'soma', -custo]]; diz = f"{custo} de PV"
    elif com in ('osso', 'erva'):
        foco = foco_de(E, pid); c = min(foco['cat'], M.MATERIA_ATE) if foco else 0; chave = M.materia(com, c); custo = n * W.DIVIDA_MATERIA
        if (p.get('carga') or {}).get(chave, 0) < custo: sys.exit(f"pagar {n} queima {custo} de {estado.nome_bem(chave)}; {p['nome']} leva {(p.get('carga') or {}).get(chave, 0)}")
        ef = [['pessoa', pid, 'carga.' + chave, 'soma', -custo]]; diz = f"{custo} de {estado.nome_bem(chave)} queimados"
    else: sys.exit('a dívida paga-se em pv, osso ou erva')
    _rito(E, pid, ef + [['pessoa', pid, 'divida', 'soma', -n]], f"{p['nome']} faz um rito no escuro")
    out = f"{p['nome']} paga {n} da dívida ({diz}): deve {E['gente'][pid].get('divida', 0)}"
    import maldicao
    for x in maldicao.confere(E, pid): out += '\n' + x
    return out


# ---------- lançar fora da luta ----------
def d(lados): return secrets.randbelow(lados) + 1


def lancar(E, pid, f, alvo=None, paga_=None):
    """lança fora da luta (não gasta bloco): a cura, a bênção (antes da luta) e a seiva (dobra a cura da noite). Os ritos têm comando próprio; o que fora da luta não
    muda número (a luz, o amparo, os de ataque) é recusado antes de gastar."""
    if f not in T.FEITICOS: sys.exit(f'feitiço desconhecido: "{f}"')
    if f in ('quebrar-maldição', 'ler', 'praga'): sys.exit(f"{_nf(f).capitalize()} é rito: `" + dict(quebrar='maldicao.py rito ALVO quem=ID').get(f.split('-')[0], f'magia_mundo.py {f} ...') + '`')
    if f not in ('cura', 'bênção', 'seiva'): sys.exit(f"{_nf(f).capitalize()} só muda número na luta (a ordem `lancar`)")
    p = lancador(E, pid, f, fora_ok=True); q = _junto(E, pid, alvo); b = E['gente'][q]; t = trad_de(p, f); dia = E['relogio']['dia']; custo = T.FEITICOS[f]['mana']
    if f == 'cura' and b['pv'] >= estado.pv_max(b): sys.exit(f"{b['nome']} está com o PV cheio ({b['pv']}/{estado.pv_max(b)}): a cura não faria nada (a Mana fica)")
    preco = preco_servico(E, q, pid, W.SERVICO['cura' if f == 'cura' else 'bencao'], paga_)
    ef = [['pessoa', pid, 'mana', 'soma', -custo], ['pessoa', pid, 'treino.' + t, 'soma', 1]] + _paga(E, q, pid, preco)
    if p.get('tradicao') == 'pacto' and T.FEITICOS[f]['de'] == 'pacto' and T.FEITICOS[f]['grau'] in W.DIVIDA_GRAU: ef.append(['pessoa', pid, 'divida', 'soma', W.DIVIDA_GRAU[T.FEITICOS[f]['grau']]])
    para = '' if q == pid else f" em {b['nome']}"
    if f == 'cura':
        c = cat_foco(E, pid, t); dado = d(8); bruto = int(T.cura(dado, c, b.get('funda'))); teto = max(0, int(estado.pv_max(b) * T.CURA_TETO) - estado.hoje(E, b, 'curado'))
        cura = max(0, min(bruto, teto, estado.pv_max(b) - b['pv']))
        if cura: ef += [['pessoa', q, 'pv', 'soma', cura], ['pessoa', q, 'marca.curado', 'poe', dict(dia=dia, n=estado.hoje(E, b, 'curado') + cura)]]
        txt = f"{p['nome']} lança cura{para}: 1d8 = {dado}, × 6 × 3^(foco {T.CATS[c]} − ferida {T.CATS[b.get('funda') or 0]}) = {bruto}; cura {cura}" + (' (o teto da cura de hoje)' if cura == teto and cura < bruto else '') + f". PV {b['pv'] + cura}/{estado.pv_max(b)}"
    elif f == 'bênção':
        ef.append(['pessoa', q, 'marca.bencao', 'poe', dict(ate=estado.agora(E) + W.BENCAO_DURA, por=pid)])
        txt = f"{p['nome']} benze {b['nome']}: a bênção vale na luta que abrir até o fim do bloco seguinte"
    else:
        ef.append(['pessoa', q, 'marca.seiva', 'poe', estado.agora(E) + M.BLOCOS_DIA])
        txt = f"{p['nome']} dá seiva a {b['nome']}: a cura dos próximos blocos dormidos (até um dia) vale em dobro"
    estado.aplica(E, 'servico' if preco else 'lancar', ef, onde=estado.onde(E, pid), quem=list(dict.fromkeys([pid, q])), texto=f"{p['nome']} lança {_nf(f)}{para}" + (f" (por {preco} de prata)" if preco else ''))
    return txt + f". Mana de {p['nome']}: {diz_mana(E['gente'][pid])}" + (f". {b['nome']} pagou {preco} de prata" if preco else '') + sobe(E, pid, t)


# ---------- os ritos ----------
def pode_ler(E, p):
    """por que a pessoa não lê (ou None): lê quem sabe o feitiço ler, ou a fé de Treinado para cima (com voto inteiro)"""
    if 'ler' in (p.get('feiticos') or []): return None
    if p.get('tradicao') == 'fé' and mao(p, 'fé') >= W.LER_FE and voto_vale(p): return None
    return 'lê quem sabe o feitiço ler (a bruxa), ou quem é da fé com mão de Treinado'


def ler(E, pid, o_que, alvo=None, paga_=None):
    """O RITO DE LER (1 bloco leve, 2 de Mana): a MALDIÇÃO de alguém (todas as que andam nele: passa a saber tudo), o DOM de alguém (ele se mostra), ou uma PEÇA
    (a dele, a de quem está com ele, ou uma solta aqui: se é maldita, que maldição, e o que a quebra; e os encantos)"""
    p = estado.presente(E, pid, 'fazer o rito aqui'); pq = pode_ler(E, p)
    if pq: sys.exit(f"{p['nome']} não lê: {pq}")
    custo = T.FEITICOS['ler']['mana']
    if estado.mana(p) < custo: sys.exit(f"o rito de ler custa {custo} de Mana; {p['nome']} tem {estado.mana(p)}")
    L = E['itens']['itens']; ef = []; t = 'pacto' if 'ler' in (p.get('feiticos') or []) else 'fé'
    if o_que == 'peca':
        it = L.get(alvo) or sys.exit(f'diga a peça (o id dela)')
        dono = it.get('dono'); aqui = estado.onde(E, pid)
        if not ((dono and estado.onde(E, dono) == aqui) or (not dono and it.get('onde') == aqui)): sys.exit(f"{it['nome']} não está aqui")
        q = dono or pid
        if isinstance(it.get('maldita'), dict): ef.append(['item', alvo, 'maldita', 'poe', dict(it['maldita'], lida=True)])
    else:
        q = _junto(E, pid, alvo or pid); b = E['gente'][q]
        if o_que == 'maldicao': ef += [['maldicao', q, m['id'], 'sabe', 2] for m in b.get('maldicoes') or [] if isinstance(m, dict) and m.get('sabe', 0) < 2]
        elif o_que == 'dom': ef += talento.mostra(E, q)
        else: sys.exit('lê-se: maldicao, dom ou peca')
    preco = preco_servico(E, q, pid, W.SERVICO['ler'], paga_)
    _rito(E, pid, [['pessoa', pid, 'mana', 'soma', -custo], ['pessoa', pid, 'treino.' + t, 'soma', 1]] + _paga(E, q, pid, preco) + ef, f"{p['nome']} faz o rito de ler" + (f" (por {preco} de prata)" if preco else ''), com=(q,))
    if o_que == 'peca':
        it = L[alvo]; mo = it.get('maldita')
        diz = (f"{it['nome']} é MALDITA: {mo['nome']} ({FEM[mo['cat']]}, {mo['tipo']}): quem a puser em uso pega a maldição, e a mão não a larga. Quebra: " + __import__('maldicao').diz_condicao(E, dict(mo['condicao'], item=alvo))) if isinstance(mo, dict) else f"{it['nome']} não traz maldição."
        enc = it.get('encantos') or []
        return diz + (' Encantos: ' + ', '.join(f"{_nf(e['feitico'])} (grau {e['grau']})" for e in enc) + '.' if enc else '')
    b = E['gente'][q]
    if o_que == 'maldicao':
        import maldicao
        ms = [maldicao.diz(E, q, m) for m in b.get('maldicoes') or [] if isinstance(m, dict)]
        return '\n'.join(ms) if ms else f"{b['nome']} não tem maldição: o que pesa é outra coisa."
    ds = talento.doms(b)
    return (f"{b['nome']} tem um dom: " + '; '.join(talento.frase_dom(c, g) for c, g in ds.items())) if ds else f"{b['nome']} não tem dom nenhum."


def praga(E, pid, alvo, tipo='míngua', nome=None):
    """A PRAGA (rito de 1 bloco, 6 de Mana, pelo toque): a bruxa roga uma maldição da categoria do foco dela. 2d20 + Conjuração do pacto contra a Firmeza do alvo.
    Pegou: a maldição anda nele (quebra com o perdão dela, ou com a morte dela). A dívida sobe a categoria mais 1, pegue ou não."""
    import maldicao
    if tipo not in M.MALDICAO_TIPOS: sys.exit(f'o tipo da maldição é um de: {", ".join(M.MALDICAO_TIPOS)}')
    p = lancador(E, pid, 'praga'); q = _junto(E, pid, alvo)
    if q == pid: sys.exit('ninguém roga praga em si mesmo')
    b = E['gente'][q]; c = cat_foco(E, pid, 'pacto'); custo = T.FEITICOS['praga']['mana']
    _rito(E, pid, [['pessoa', pid, 'mana', 'soma', -custo], ['pessoa', pid, 'divida', 'soma', c + W.DIVIDA_PRAGA], ['pessoa', pid, 'treino.pacto', 'soma', 1]], f"{p['nome']} faz um rito", com=(q,))
    vis, real = conjuracao(E, pid, 'pacto', visivel=True), conjuracao(E, pid, 'pacto'); p = E['gente'][pid]; atr = p['atributos']['Afinidade'] // 10
    fir = maldicao.firmeza(E, q)
    r = teste.rola(E, f"a praga em {b['nome']}", 'Afinidade', math.ceil(fir), mais=int(vis) - atr, quem=pid, rotulo='Conjuração do pacto', **({'dom': int(real) - int(vis)} if int(real) > int(vis) else {}))
    ef = []
    if r['passou']: ef += maldicao.poe(E, q, dict(nome=nome or W.NOMES[tipo], cat=c, tipo=tipo, condicao=dict(tipo='perdao', quem=pid)), 'feitiço', fonte=pid, quem=pid)
    if talento.decidiu(r): ef += talento.mostra(E, pid)
    if ef: estado.aplica(E, 'rito', ef, onde=estado.onde(E, pid), quem=[pid, q], texto=f"{p['nome']} faz um rito")
    return teste.diz(E, r) + f"\n  (Conjuração do pacto {int(vis)} contra a Firmeza de {b['nome']}, {fir:g})".replace('.', ',') + ('\nA praga pega: ' + (nome or W.NOMES[tipo]) + f", {FEM[c]}, no passo 1 ({b['nome']} ainda não sabe)." if r['passou'] else '\nA praga não pega.') + f" A dívida de {p['nome']}: {E['gente'][pid].get('divida', 0)}."


def agua(E, pid, n):
    """o clérigo benze água num santuário (rito de 1 bloco): cada uma pede 1 de erva Comum e 2 de Mana; até 3 por rito"""
    p = lancador(E, pid, 'bênção'); n = max(1, min(int(n), W.AGUA_BENTA_RENDE)); lid = p['lugar']
    if E['lugares'][lid].get('santuario') is None: sys.exit(f"{E['lugares'][lid]['nome']} não tem santuário: a água se benze num")
    erva = n * W.AGUA_BENTA['erva']; mana = n * W.AGUA_BENTA['mana']
    if (p.get('carga') or {}).get('erva:0', 0) < erva: sys.exit(f"{n} de água benta pedem {erva} de erva Comum; {p['nome']} leva {(p.get('carga') or {}).get('erva:0', 0)}")
    if estado.mana(p) < mana: sys.exit(f"{n} de água benta pedem {mana} de Mana; {p['nome']} tem {estado.mana(p)}")
    _rito(E, pid, [['pessoa', pid, 'carga.erva:0', 'soma', -erva], ['pessoa', pid, 'mana', 'soma', -mana], ['pessoa', pid, 'carga.água benta', 'soma', n], ['pessoa', pid, 'treino.fé', 'soma', 1]], f"{p['nome']} benze água no santuário")
    return f"{p['nome']} benze {n} de água: leva agora {(E['gente'][pid].get('carga') or {}).get('água benta', 0)} de água benta."


def benzer(E, pid, iid, paga_=None):
    """o clérigo benze uma arma num santuário (rito de 1 bloco, 2 de Mana): ela conta inteira contra o que não tem corpo por 7 dias"""
    p = lancador(E, pid, 'bênção'); lid = p['lugar']
    if E['lugares'][lid].get('santuario') is None: sys.exit(f"{E['lugares'][lid]['nome']} não tem santuário: a arma se benze num")
    it = E['itens']['itens'].get(iid) or sys.exit(f'não há o item "{iid}" no Livro de Itens')
    if it.get('tipo') != 'arma' or not it.get('dono'): sys.exit(f"{it['nome']} não é uma arma com dono")
    q = _junto(E, pid, it['dono']); preco = preco_servico(E, q, pid, W.SERVICO['benzer'], paga_)
    if estado.mana(p) < W.BENZER_ARMA: sys.exit(f"benzer a arma custa {W.BENZER_ARMA} de Mana; {p['nome']} tem {estado.mana(p)}")
    ate = estado.agora(E) + W.RITO_BLOCOS + M.BENTA_DURA
    _rito(E, pid, [['pessoa', pid, 'mana', 'soma', -W.BENZER_ARMA], ['item', iid, 'benta', 'poe', ate], ['pessoa', pid, 'treino.fé', 'soma', 1]] + _paga(E, q, pid, preco), f"{p['nome']} benze {it['nome']}", com=(q,))
    return f"{p['nome']} benze {it['nome']}: por 7 dias a arma conta inteira contra o que não tem corpo." + (f" {E['gente'][q]['nome']} pagou {preco} de prata." if preco else '')


def tratar(E, pid, paciente, paga_=None):
    """TRATAR (o ofício cura; 1 bloco leve e 1 remédio; um tratamento por paciente por dia): soma 1 dia de repouso a todas as feridas dele (o dom da cura soma meio por grau,
    e se mostra no primeiro tratamento). O remédio sai da carga do paciente, ou da de quem trata (que cobra o preço de base dele); quem é tratado paga o serviço."""
    import tabelas_mercado as C
    p = estado.presente(E, pid, 'tratar aqui'); q = _junto(E, pid, paciente); b = E['gente'][q]; dia = E['relogio']['dia']
    if not b['feridas']: sys.exit(f"{b['nome']} não tem ferida aberta")
    quer = W.TRATAR_MAO[1] if any(f['grave'] for f in b['feridas']) else W.TRATAR_MAO[0]
    if mao(p, 'cura') < quer: sys.exit(f"tratar {'ferida grave' if quer == W.TRATAR_MAO[1] else 'ferida'} pede mão de cura de {T.MAESTRIAS[quer]}; a de {p['nome']} é de {T.MAESTRIAS[mao(p, 'cura')]}")
    if (b.get('marca') or {}).get('tratado_dia') == dia: sys.exit(f"{b['nome']} já foi tratado hoje: um tratamento por dia")
    de = q if (b.get('carga') or {}).get('remédio', 0) >= 1 else pid if (p.get('carga') or {}).get('remédio', 0) >= 1 else None
    if de is None: sys.exit(f"tratar gasta 1 remédio, e nem {p['nome']} nem {b['nome']} levam (a loja vende; a botica faz)")
    preco = preco_servico(E, q, pid, W.SERVICO['tratar'] + (C.base('remédio') if de == pid else 0), paga_)
    dom = talento.dom(p, 'cura'); dias = W.TRATAR + W.TRATAR_DOM * dom
    ef = [['pessoa', de, 'carga.remédio', 'soma', -1], ['pessoa', q, 'marca.tratado_dia', 'poe', dia], ['pessoa', pid, 'treino.cura', 'soma', 1]] + _paga(E, q, pid, preco) + corpo._repouso(b, q, dias)
    if dom: ef += talento.mostra(E, pid)
    n, pq = ato.passa(E, pid, 1, 'cura', esforco='leve', mais=lambda i: ef, com=(q,) if q != pid else (), texto=f"{p['nome']} trata as feridas de {b['nome']}" + (f" (por {preco} de prata)" if preco else ''))
    if not n: sys.exit(f"o tratamento não se fez: {pq}")
    b = E['gente'][q]; sararam = sum(1 for x in ef if x[:1] == ['ferida'] and x[2] == 'sara')
    out = f"{p['nome']} trata {b['nome']}: as feridas ganham {f'{dias:g}'.replace('.', ',')} {'dia' if dias == 1 else 'dias'} de repouso" + (f"; {tantos(sararam, 'ferida sara', 'feridas saram')}" if sararam else '')
    if dom and talento.visto(E['gente'][pid]): out += f". As mãos de {p['nome']} fecham a ferida mais depressa do que deviam: é um dom."
    return out + (f". {b['nome']} pagou {preco} de prata" if preco else '') + sobe(E, pid, 'cura') + (f'. PAROU: {pq}' if pq else '.')


def compra(E, pid, bem, n, de, preco=None):
    """a compra de pessoa a pessoa (evento "servico"): o que a loja não negocia (o veneno de lâmina, que é crime) ou o que alguém vende do que leva. Quem vende entrega da carga
    dele; quem compra paga o que se combinou (sem dizer: o preço de base do bem, arredondado para cima). A prata só muda de mão."""
    import tabelas_mercado as C
    p = E['gente'].get(pid) or sys.exit(f'não há a pessoa "{pid}"'); v = E['gente'].get(de) or sys.exit(f'não há a pessoa "{de}"')
    if pid == de: sys.exit('ninguém compra de si mesmo')
    for x in (p, v):
        if x['estado'] != 'vivo': sys.exit(f"{x['nome']} {estado.morte_diz(E, x)}")
    estado.sem_luta(E); estado.em_cena(E, pid); estado.em_cena(E, de); p, v = E['gente'][pid], E['gente'][de]
    if estado.onde(E, pid) != estado.onde(E, de): sys.exit(f"{v['nome']} não está com {p['nome']}")
    if not (isinstance(n, int) and not isinstance(n, bool) or (isinstance(n, str) and n.strip().isdigit())) or int(n) < 1: sys.exit(f'diga quantas unidades, em número inteiro (1 ou mais; veio "{n}")')
    n = int(n); preco = preco_dito(preco, 'preco=') if preco is not None else None
    if (v.get('carga') or {}).get(bem, 0) < n: sys.exit(f"{v['nome']} não leva {n} de {estado.nome_bem(bem)}")
    preco = preco if preco is not None else max(1, math.ceil((C.base(bem) or 1) * n))
    if p['moedas'] < preco: sys.exit(f"{n} de {estado.nome_bem(bem)} por {preco} de prata; {p['nome']} tem {p['moedas']}")
    crime = ' (é crime aqui: quem vir, conta ao guarda)' if M.le_materia(bem)[0] in C.CRIME and E['lugares'][estado.onde(E, pid)].get('pop') else ''
    estado.aplica(E, 'servico', [['pessoa', de, 'carga.' + bem, 'soma', -n], ['pessoa', pid, 'carga.' + bem, 'soma', n], ['pessoa', pid, 'moedas', 'soma', -preco], ['pessoa', de, 'moedas', 'soma', preco]],
                  onde=estado.onde(E, pid), quem=[pid, de], texto=f"{p['nome']} compra de {v['nome']} {n} de {estado.nome_bem(bem)}")
    return f"{p['nome']} compra de {v['nome']} {n} de {estado.nome_bem(bem)} por {preco} de prata{crime}."


def poe_santuario(E, lid, nivel, como=''):
    """o Mestre (ou o gerador) registra o santuário de um lugar (0 a 4), ou tira (None)"""
    l = E['lugares'].get(lid) or sys.exit(f'não há o lugar "{lid}"')
    if nivel is not None and not 0 <= nivel <= M.BANCADA_MAX: sys.exit(f'o santuário vai de 0 a {M.BANCADA_MAX}; veio {nivel}')
    txt = f"{l['nome']} " + ('fica sem santuário' if nivel is None else f'tem agora um santuário (+{nivel})') + (f': {como}' if como else '')
    if not estado.aplica(E, 'mestre', [['lugar', lid, 'santuario', 'poe', nivel]], onde=lid, texto=txt): return f"{l['nome']} já estava assim: nada mudou."
    return txt + '.'


# ---------- o voto que se quebra, a pobreza e a dívida ----------
def quebra_voto(E, pid, como):
    """os efeitos de quebrar o voto: o voto fica quebrado, a Mana se apaga e fica a marca (maldição de juramento, da categoria do santuário)"""
    import maldicao
    p = E['gente'][pid]; v = p['voto']; c = E['lugares'].get(v.get('santuario'), {}).get('santuario') or 0
    return [['pessoa', pid, 'voto', 'quebra', como], ['pessoa', pid, 'mana', 'poe', 0]] + maldicao.poe(E, pid, dict(nome='o Voto Quebrado', cat=min(c, len(T.CATS) - 1), tipo='marca',
            condicao=dict(tipo='cumprir', texto='a penitência de um clérigo Mestre')), 'juramento', fonte=v.get('santuario'))


def vestiu(E, pid, iid):
    """o voto da lâmina: pôr em uso arma de corte ou de ponta é quebrá-lo"""
    p = E['gente'][pid]; it = E['itens']['itens'].get(iid) or {}
    if not voto_vale(p) or p['voto'].get('qual') != 'lâmina' or it.get('tipo') != 'arma' or T.FAMILIAS.get(it.get('familia'), {}).get('golpe') not in W.VOTO_LAMINA: return ''
    estado.aplica(E, 'maldicao', quebra_voto(E, pid, f"pôs em uso {it['nome']}"), onde=estado.onde(E, pid), quem=[pid], texto=f"{p['nome']} quebra o voto da lâmina")
    return f"{p['nome']} QUEBROU O VOTO DA LÂMINA ao pôr em uso {it['nome']}: a Mana se apaga, e fica uma marca (o Voto Quebrado)."


def virada(E):
    """o dia virou: o voto da pobreza leva ao santuário a prata acima de 50; a dívida acima de Vontade ÷ 10 vira maldição em quem deve (a Conta)"""
    import maldicao
    for pid in list(E['gente']):
        p = E['gente'][pid]
        if not isinstance(p, dict) or p.get('estado') != 'vivo': continue
        v = p.get('voto')
        if voto_vale(p) and v.get('qual') == 'pobreza' and p['moedas'] > W.VOTO_POBREZA and v.get('santuario') in E['lugares']:
            x = p['moedas'] - W.VOTO_POBREZA
            estado.aplica(E, 'virada', [['pessoa', pid, 'moedas', 'soma', -x], ['estoque', v['santuario'], 'prata', 'soma', x]], onde=v['santuario'], quem=[pid], texto=f"o voto de {p['nome']} leva {x} de prata ao santuário")
        p = E['gente'][pid]; dv = p.get('divida') or 0; lim = p['atributos']['Vontade'] // W.DIVIDA_LIMITE
        if dv > lim and not any(isinstance(m, dict) and (m.get('condicao') or {}).get('tipo') == 'divida' for m in p.get('maldicoes') or []):
            c = min(len(T.CATS) - 1, (dv - lim - 1) // max(1, lim))
            estado.aplica(E, 'maldicao', maldicao.poe(E, pid, dict(nome='a Conta', cat=c, tipo='míngua', condicao=dict(tipo='divida')), 'juramento', fonte='pacto', sabe=2), onde=estado.onde(E, pid), quem=[pid],
                          texto=f"a dívida de {p['nome']} vira maldição")


# ---------- a mesa ----------
def diz(E, pid, mestre=False):
    """a linha da magia de alguém (vazia: a pessoa não tem magia nenhuma)"""
    p = E['gente'][pid]; t = p.get('tradicao'); fs = p.get('feiticos') or []; est = (p.get('marca') or {}).get('estudo') or {}
    if not (t or fs or est or p.get('mana') is not None): return ''
    partes = [f"Mana {diz_mana(p)}" + (f" (de verdade, {estado.mana(p)} de {estado.mana_max(p)})" if mestre and mana_vista(p) != (estado.mana(p), estado.mana_max(p)) else '')]
    if t: partes.append(f"{dict(arcano='o arcano', fé='a fé', verde='o verde', pacto='o pacto')[t]}: {T.MAESTRIAS[mao(p, t)]} ({tantos((p.get('treino') or {}).get(t, 0), 'bloco')})")
    if fs: partes.append('sabe: ' + ', '.join(_nf(f) for f in fs))
    for f, n in est.items(): partes.append(f"estuda {_nf(f)} ({estudo_diz(p, f, n, mestre)})")      # o Mestre, o número de verdade; a pessoa, o da tabela até o talento aparecer
    v = p.get('voto')
    if isinstance(v, dict): partes.append(f"voto {'do' if v['qual'] == 'socorro' else 'da'} {v['qual']} ({estado.em(E, v['santuario']) if v.get('santuario') in E['lugares'] else ''})" + (f": QUEBRADO no Dia {v['quebrado']}" if v.get('quebrado') is not None else ''))
    if laco_vale(E, p): partes.append(f"laço com {E['lugares'][p['laco']['ermo']]['nome']} (fartura {fartura(E, p['laco']['ermo']):.0%}" + (f"; a força cai {pena_laco(E, pid)}" if pena_laco(E, pid) else '') + ')')
    if t == 'pacto' or p.get('divida'): partes.append(f"dívida {p.get('divida') or 0} (acima de {p['atributos']['Vontade'] // W.DIVIDA_LIMITE} vira maldição)")
    foco = foco_de(E, pid)
    if foco: partes.append(f"foco: {foco['nome']}")
    return f"{p['nome']}: " + ' · '.join(partes)


def voce(E):
    pid = estado.eu(E); p = E['gente'].get(pid) if pid else None
    if not isinstance(p, dict) or p.get('estado') != 'vivo': return []
    x = diz(E, pid)
    return [f"Magia: {x.split(': ', 1)[1]}"] if x else []


def mesa(E):
    """a magia daqui: quem sabe feitiço e ensina (e por quanto), o santuário, os serviços de pessoa a pessoa"""
    pid = estado.eu(E); p = E['gente'].get(pid) if pid else None
    if not isinstance(p, dict) or p.get('estado') != 'vivo' or estado.fora(E, pid): return []
    lid = p['lugar']; l = E['lugares'][lid]; L = []
    for k, q in E['gente'].items():
        if k == pid or q.get('estado') != 'vivo' or q['lugar'] != lid or estado.fora(E, k) or not q.get('feiticos'): continue
        L.append(f"- {q['nome']} sabe {', '.join(_nf(f) for f in q['feiticos'])}: ensina a {M.SALARIO[q.get('grau_oficio', 'diarista')]} de prata por bloco, até {M.JORNADA} blocos por dia"
                 + (" · lê maldição, dom e peça" if not pode_ler(E, q) else '') + (" · quebra maldição (rito)" if 'quebrar-maldição' in q['feiticos'] else '') + (" · cura" if 'cura' in q['feiticos'] else ''))
        if (q.get('maestria') or {}).get('cura', 0) >= W.TRATAR_MAO[0]: L[-1] += ' · trata ferida'
    for k, q in E['gente'].items():
        if k != pid and q.get('estado') == 'vivo' and q['lugar'] == lid and not q.get('feiticos') and (q.get('maestria') or {}).get('cura', 0) >= W.TRATAR_MAO[0]:
            L.append(f"- {q['nome']} trata ferida ({W.SERVICO['tratar']} de prata e um remédio; um tratamento por dia)")
    if l.get('santuario') is not None: L.append(f"- o santuário (+{l['santuario']}): o voto se faz aqui; a prece enche a Mana; a água benta e a bênção da arma (`magia_mundo.py agua N`, `benzer ARMA`); o jornal (`magia_mundo.py jornal N`)")
    if not L: return []
    return ['## A magia daqui', f"Os serviços, de pessoa a pessoa (o personagem paga a quem presta; o que ele faz pela gente do mundo sai sem cobrança): ler {W.SERVICO['ler']} · cura {W.SERVICO['cura']} o lance · bênção {W.SERVICO['bencao']} por pessoa · "
            f"tratar {W.SERVICO['tratar']} e o remédio · benzer a arma {W.SERVICO['benzer']} · o rito de quebrar: {', '.join(f'{FEM[c]} {W.preco_quebrar(c)}' for c in range(3))} de prata"] + L


def so_mestre(E):
    """quem lança, no lugar do personagem: a Mana, a tradição, o que sabe (tudo)"""
    pid = estado.eu(E)
    if not pid: return []
    aqui = estado.onde(E, pid)
    return [f"magia de {diz(E, k, mestre=True)}" for k, q in E['gente'].items() if isinstance(q, dict) and q.get('estado') == 'vivo' and (k == pid or estado.onde(E, k) == aqui) and diz(E, k)]


# ---------- a linha de comando ----------
def main(a=None):
    a = sys.argv[1:] if a is None else list(a)
    op = dict(x.split('=', 1) for x in a if '=' in x); pos = [x for x in a if '=' not in x]
    cmds = ('ver', 'estudar', 'voto', 'laco', 'pacto', 'prece', 'paga', 'divida', 'lancar', 'ler', 'praga', 'agua', 'benzer', 'tratar', 'jornal', 'santuario', 'compra')
    if not pos or pos[0] not in cmds: print(__doc__); return
    falta = lambda o_que, exemplo: sys.exit(f'{o_que}: `python3 magia_mundo.py {exemplo}`')
    E = estado.carrega(); pid = op.get('quem') or estado.eu(E)
    if pid not in E['gente']: sys.exit(f'não há a pessoa "{pid}"')
    num = lambda i, ex: int(pos[i]) if len(pos) > i and pos[i].isdigit() and int(pos[i]) >= 1 else falta('diga quantos, em número inteiro (1 ou mais)', ex)
    if pos[0] == 'ver':
        q = pos[1] if len(pos) > 1 else estado.eu(E)
        if q not in E['gente']: sys.exit(f'não há a pessoa "{q}"')
        estado.em_cena(E, q)                                # quem não é o personagem aparece como volta à cena agora (o descanso em casa, com a Mana); este comando só olha: nada é gravado
        print(diz(E, q) or f"{E['gente'][q]['nome']} não tem magia nenhuma (nem tradição, nem feitiço)."); return
    if pos[0] == 'estudar':
        if len(pos) < 2: falta('diga o feitiço e a fonte', 'estudar seta com=anselmo')
        fonte = {'com': op['com']} if op.get('com') else {'escrito': op['escrito']} if op.get('escrito') else ('santuario' if 'santuario' in pos[2:] else 'ermo' if 'ermo' in pos[2:] else None)
        out = estudar(E, pid, pos[1], fonte, blocos=op.get('blocos'))['texto']
    elif pos[0] == 'voto': out = voto(E, pid, pos[1] if len(pos) > 1 else falta('diga o voto', 'voto lâmina'))
    elif pos[0] == 'laco': out = laco(E, pid, pos[1] if len(pos) > 1 else falta('diga o ermo', 'laco mata'))
    elif pos[0] == 'pacto': out = pacto(E, pid)
    elif pos[0] == 'prece': out = prece(E, pid)
    elif pos[0] == 'paga': out = paga(E, pid, num(1, 'paga 4 pv'), pos[2] if len(pos) > 2 else 'pv')
    elif pos[0] == 'divida': out = paga_divida(E, pid, num(1, 'divida 1 pv'), pos[2] if len(pos) > 2 else 'pv')
    elif pos[0] == 'lancar': out = lancar(E, pid, pos[1] if len(pos) > 1 else falta('diga o feitiço', 'lancar cura alvo=eu'), alvo=op.get('alvo'), paga_=op.get('paga'))
    elif pos[0] == 'ler': out = ler(E, pid, pos[1] if len(pos) > 1 else falta('diga o que ler', 'ler maldicao eu'), pos[2] if len(pos) > 2 else None, paga_=op.get('paga'))
    elif pos[0] == 'praga': out = praga(E, pid, pos[1] if len(pos) > 1 else falta('diga em quem', 'praga tome'), tipo=op.get('tipo', 'míngua'), nome=pos[2] if len(pos) > 2 else None)
    elif pos[0] == 'agua': out = agua(E, pid, num(1, 'agua 2'))
    elif pos[0] == 'benzer': out = benzer(E, pid, pos[1] if len(pos) > 1 else falta('diga a arma', 'benzer i0007'), paga_=op.get('paga'))
    elif pos[0] == 'tratar': out = tratar(E, pid, pos[1] if len(pos) > 1 else falta('diga quem tratar', 'tratar eu'), paga_=op.get('paga'))
    elif pos[0] == 'compra':
        if len(pos) < 3 or not op.get('de'): falta('diga o bem, quantos e de quem', 'compra veneno:1 1 de=quiteria preco=40')
        out = compra(E, pid, pos[1], pos[2], op['de'], preco=op.get('preco'))
    elif pos[0] == 'jornal':
        import oficio
        out = oficio.jornal(E, pid, num(1, 'jornal 2'), oficio='fé')['texto']
    else:
        if len(pos) < 2 or not (pos[1] == 'nada' or pos[1].isdigit()): falta('diga o nível do santuário, de 0 a 4, ou "nada"', 'santuario 1 "a capela da vila"')
        out = poe_santuario(E, E['gente'][pid]['lugar'], None if pos[1] == 'nada' else int(pos[1]), como=pos[2] if len(pos) > 2 else '')
    estado.grava(E)
    print(out)
    print(ato.ultima_linha(E, pid))


if __name__ == '__main__':
    import signal; hasattr(signal, 'SIGPIPE') and signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    main()
