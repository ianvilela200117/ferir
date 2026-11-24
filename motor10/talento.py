#!/usr/bin/env python3
"""talento.py — MOTOR 10: OS DONS E OS TALENTOS (etapa da magia, capítulo 10). Os números moram no tabelas_talento.py.

  O TALENTO (cinco graus, por caminho) diz a pressa de aprender e o teto da mão: os blocos de cada grau de maestria vezes o talento (o Prodígio, a metade; o Negado, o dobro),
    e o Negado não passa de Iniciante, o Lerdo não passa de Mestre. Não soma em conta nenhuma.
  O DOM (dois graus, num caminho só, raro) soma na conta como maestria que ninguém treinou: na arma (o acerto, e metade na Defesa); na bancada, dentro do teto de +8 do preparo;
    no rastro, na coleta e na cura; no comércio, no que a loja paga; na tradição, na Conjuração, metade na Firmeza e o mesmo na Mana.
  Os dois nascem com a pessoa, pelo dado do MUNDO (estado.sorte), e não mudam. O personagem do jogador escolhe uma inclinação: naquele caminho o dado rola duas vezes (M2 b).
  NINGUÉM NASCE SABENDO: o talento aparece na MESA 20 blocos depois de rolado, no caminho; o dom fica ESCONDIDO até o teste em que fez a diferença (o script sabe:
    "sem o dom, não passava"), ou até alguém o ler. Escondido, ele entra no dado (teste.rola, dom=) e não entra em conta nenhuma que vai à mesa.
  A pessoa comum (sem talento, sem dom) é a pessoa de hoje: multiplica por 1 e soma zero.

Uso (para olhar; não grava nada): python3 talento.py ver [ID]        o que a pessoa sabe de si (sem ID: o personagem)
                                  python3 talento.py mestre [ID]     tudo (SÓ O MESTRE)
"""
import sys
import tabelas as T
import tabelas_mundo as M
import tabelas_talento as TT


def caminho_de(chave): return TT.caminho_de(chave)


# ---------- ler a pessoa ----------
def rolado(p): return isinstance(p.get('talento'), dict)                  # o talento já foi rolado? (None: save antigo, ou gente que ninguém rolou)
def talentos(p): t = p.get('talento'); return dict(t) if isinstance(t, dict) else {}
def grau(p, chave): return int(talentos(p).get(caminho_de(chave), 0))     # −2 a 2; 0 é o Comum (e quem não foi rolado)
def vezes(p, chave): return TT.vezes(grau(p, chave))
def blocos(p, chave, n): return TT.blocos(n, grau(p, chave))              # n blocos para esta pessoa, neste caminho (o estudo de um feitiço: 3, 6, 18, 54, 162)
def teto(p, chave): return TT.TALENTO[grau(p, chave)][2]                  # o grau mais alto que a mão sobe


def pede(p, chave, tabela, g):
    """os blocos que o grau `g` de maestria pede a ESTA pessoa no caminho da chave (a tabela vezes o talento), ou None se o grau passa do teto dela"""
    return None if g > teto(p, chave) else TT.blocos(tabela[g], grau(p, chave))


def doms(p): d = p.get('dom'); return dict(d) if isinstance(d, dict) else {}       # o dom de verdade
def visto(p): return bool((p.get('marca') or {}).get('dom_visto'))       # o dom já se mostrou (marca.dom_visto: o dia)?
def doms_vistos(p): return doms(p) if visto(p) else {}
def dom(p, chave): return int(doms(p).get(caminho_de(chave), 0))         # o dom de verdade neste caminho: o que entra no dado e na luta
def dom_visto(p, chave): return dom(p, chave) if visto(p) else 0         # o que a pessoa já sabe: o que entra na conta que vai à mesa
def oculto(p, chave): return dom(p, chave) - dom_visto(p, chave)         # o que vai escondido no dado (teste.rola, dom=)
def kw(p, chave):
    """o que se passa ao teste.rola por causa do dom escondido: {} se não há (assim o dado de quem não tem dom é chamado como sempre foi)"""
    o = oculto(p, chave)
    return {'dom': o} if o else {}


def decidiu(r):
    """o dom escondido fez passar este teste (o r do teste.rola)? Ou o módulo já marcou que ele mudou a faixa (r['fez'])"""
    d = r.get('dom') or 0
    return bool(d) and (bool(r.get('fez')) or (r['total'] >= r['contra'] and r['total'] - d < r['contra']))


def mostra(E, pid):
    """o efeito que revela o dom (a pessoa viu que tem), ou [] se não tem dom ou já se mostrou. Quem chama põe no evento do próprio ato."""
    p = E['gente'][pid]
    return [] if visto(p) or not doms(p) else [['pessoa', pid, 'marca.dom_visto', 'poe', E['relogio']['dia']]]


# ---------- quando o talento aparece ----------
def no_caminho_t(treino, c): return sum((treino or {}).get(f, 0) for f in TT.MAOS[c]) if c in TT.MAOS else (treino or {}).get(c, 0)
def no_caminho(p, c): return no_caminho_t(p.get('treino'), c)            # os blocos (no comércio, os dias de negócio) feitos no caminho, até hoje
def base(treino): return {c: n for c in TT.CAMINHOS if (n := no_caminho_t(treino, c)) > 0}


def aparece(p, c):
    """o talento deste caminho já aparece? (rolado, não é Comum, e a pessoa fez 20 blocos no caminho desde que foi rolado)"""
    if not rolado(p) or not grau(p, c): return False
    return no_caminho(p, c) - ((p.get('marca') or {}).get('talento_base') or {}).get(c, 0) >= TT.APARECE


def tabela_de(c):
    """(a tabela de blocos do caminho, a palavra no singular, no plural): as armas e as tradições, a das armas; a forja, o couro, a alquimia e o encanto, a da forja;
    a caça e a coleta, as delas; o comércio, os dias de negócio"""
    c = caminho_de(c)
    if c in ('forja', 'couro', 'alquimia', 'encanto'):
        import tabelas_oficio as O; return O.OFICIO_BLOCOS, 'bloco', 'blocos'
    if c in ('caça', 'coleta'):
        import tabelas_caca as K; return (K.CACA_BLOCOS if c == 'caça' else K.COLETA_BLOCOS), 'bloco', 'blocos'
    if c == 'comércio':
        import tabelas_mercado as C; return C.COMERCIO_DIAS, 'dia de negócio', 'dias de negócio'
    return M.MAESTRIA_BLOCOS, 'bloco', 'blocos'


def mao_no(p, c):
    m = p.get('maestria') or {}
    if not isinstance(m, dict): return 0
    return max([m.get(f, 0) for f in TT.MAOS[c]] + [0]) if c in TT.MAOS else m.get(c, 0)


def frase(p, c):
    """o talento de um caminho em palavras, como a MESA o diz quando ele aparece"""
    g = grau(p, c); nome, _, tt = TT.TALENTO[g]; tab, um, muitos = tabela_de(c); o_que = TT.O_QUE[c]; O_que = o_que[0].upper() + o_que[1:]
    prox = next((k for k in sorted(tab) if k > mao_no(p, c) and k <= tt), None)
    abre = {2: f"{O_que}: aprende muito depressa ({nome})", 1: f"Com {o_que} você pega depressa ({nome})", -1: f"{O_que} lhe custa ({nome})", -2: f"{O_que} não é para você ({nome})"}[g]
    conta = (f": o que os outros firmam em {tab[prox]} {um if tab[prox] == 1 else muitos}, você firma em {TT.blocos(tab[prox], g)}" if prox else '')
    return abre + conta + (f"; a mão não passa de {T.MAESTRIAS[tt]}" if tt < max(T.MAESTRIAS) else '') + '.'


def frase_dom(c, g):
    onde = TT.DOM_ONDE['mao' if c in TT.MAOS else 'bancada' if c in ('forja', 'couro', 'alquimia', 'encanto') else 'comércio' if c == 'comércio' else 'tradicao' if c in TT.TRADICOES else 'rastro']
    return f"Há alguma coisa em você: {TT.DOM_NOME[c]} ({TT.O_QUE[c]}), um {TT.DOM[g][0]}: soma +{g} {onde}."


# ---------- o nascimento ----------
def _sorteia(E, pid, inclinacao=None):
    """o talento e o dom de alguém, pelo dado do mundo (mesma semente, mesma gente)"""
    import estado
    if inclinacao is not None and inclinacao not in TT.CAMINHOS: sys.exit(f'inclinação desconhecida: "{inclinacao}" (os caminhos: {", ".join(TT.CAMINHOS)})')
    tal = {}
    for c in TT.CAMINHOS:
        r = estado.sorte(E, f'talento|{pid}|{c}'); d = r.randint(1, 100)
        if c == inclinacao: d = max([d] + [r.randint(1, 100) for _ in range(TT.INCLINACAO - 1)])
        g = next(g for ate, g in TT.TALENTO_D100 if d <= ate)
        if g: tal[c] = g
    r = estado.sorte(E, f'dom|{pid}'); d = r.randint(1, 1000); gd = next((g for ate, g in TT.DOM_D1000 if d <= ate), 0)
    dm = {r.choices(TT.CAMINHOS, weights=[TT.DOM_PESO if tal.get(c, 0) >= 1 else 1 for c in TT.CAMINHOS])[0]: gd} if gd else {}
    return tal, dm


def rola(E, pid, inclinacao=None):
    """os efeitos do nascimento de quem JÁ EXISTE (o save antigo, a vila de teste que ganha a magia): o talento, o dom, a base dos blocos (o talento aparece 20 blocos
    depois), e a inclinação do personagem. Grava-se num evento "talento" (ou "gera", "mestre"). Quem já foi rolado não rola de novo."""
    p = E['gente'][pid]
    if rolado(p): sys.exit(f"{p['nome']} já tem o talento rolado: não se rola de novo")
    if inclinacao is not None and not p.get('jogador'): sys.exit('só o personagem do jogador tem inclinação')
    tal, dm = _sorteia(E, pid, inclinacao)
    ef = [['pessoa', pid, 'talento', 'poe', tal], ['pessoa', pid, 'marca.talento_base', 'poe', base(p.get('treino'))]]
    if dm: ef.append(['pessoa', pid, 'dom', 'poe', dm])
    if inclinacao: ef.append(['pessoa', pid, 'inclinacao', 'poe', inclinacao])
    return ef


def nasce(E, pid, registro, inclinacao=None):
    """o registro de quem nasce agora (['pessoa', 'nasce', pid, registro]) com o talento e o dom já rolados pelo dado do mundo"""
    if inclinacao is not None and not registro.get('jogador'): sys.exit('só o personagem do jogador tem inclinação')
    r = dict(registro); tal, dm = _sorteia(E, pid, inclinacao); r['talento'] = tal
    if dm: r['dom'] = dm
    r['marca'] = dict(r.get('marca') or {}, talento_base=base(r.get('treino')))
    if inclinacao: r['inclinacao'] = inclinacao
    return r


# ---------- a mesa ----------
def sabe(p):
    """o que a pessoa sabe de si: as frases do talento que já apareceu e do dom que já se mostrou"""
    if not rolado(p) and not doms(p): return []
    return [frase(p, c) for c in TT.CAMINHOS if aparece(p, c)] + [frase_dom(c, g) for c, g in doms_vistos(p).items()]


def tudo(p):
    """tudo, para o Mestre: os talentos que não são Comuns e o dom, dizendo o que já apareceu"""
    t = talentos(p); dm = doms(p)
    if not t and not dm: return 'Comum em tudo' if rolado(p) else 'ainda não rolado'
    L = [f"{TT.TALENTO[g][0]} em {c}" + (' (já aparece)' if aparece(p, c) else '') for c, g in t.items()]
    L += [f"{TT.DOM[g][0]} em {c} ({'já se mostrou' if visto(p) else 'escondido'})" for c, g in dm.items()]
    return ', '.join(L) + (f" · inclinação do jogador: {p['inclinacao']}" if p.get('inclinacao') else '')


def voce(E):
    """as linhas do "Você" da MESA: o talento que já apareceu e o dom que já se mostrou"""
    import estado
    pid = estado.eu(E); p = E['gente'].get(pid) if pid else None
    return sabe(p) if isinstance(p, dict) and p.get('estado') == 'vivo' else []


def so_mestre(E):
    """o SÓ O MESTRE: os talentos e os dons de quem está com o personagem (no mesmo lugar), escondidos ou não"""
    import estado
    pid = estado.eu(E)
    if not pid: return []
    aqui = estado.onde(E, pid)
    return [f"talento e dom de {x['nome']}: {tudo(x)}" for k, x in E['gente'].items()
            if isinstance(x, dict) and x.get('estado') == 'vivo' and (k == pid or estado.onde(E, k) == aqui) and (talentos(x) or doms(x))]


if __name__ == '__main__':
    import signal; hasattr(signal, 'SIGPIPE') and signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    a = sys.argv[1:]
    if not a or a[0] not in ('ver', 'mestre') or len(a) > 2: print(__doc__); sys.exit()
    import estado
    E = estado.carrega(); pid = a[1] if len(a) > 1 else estado.eu(E)
    p = E['gente'].get(pid) or sys.exit(f'não há a pessoa "{pid}"')
    if a[0] == 'mestre': print(f"{p['nome']}: {tudo(p)}")
    else: print('\n'.join(sabe(p)) or f"{p['nome']} ainda não sabe de nenhum talento nem dom em si (o talento aparece fazendo; o dom, quando decide um teste ou alguém o lê).")
