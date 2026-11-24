#!/usr/bin/env python3
"""masmorra.py — MOTOR 10, ETAPA 4b: AS MASMORRAS (capítulo 17; os números no tabelas_masmorra.py; o contrato: projeto/ETAPA_4B.md).

  A MASMORRA é um lugar do mapa (tipo "masmorra"), vizinho de uma vila ou de um ermo, a alguns blocos de caminho. Por dentro tem SALAS, e cada sala é um lugar pequeno
  (tipo "sala") ligado às outras por passagens: a contagem das criaturas, a prata no chão, a peça largada e a morte de quem cai lá dentro usam as regras de hoje.
  DESCER é um ato aberto, como a saída de caça: fica escrito em quem comanda (marca.masmorra, a descida) e em quem vai junto ({"de": quem comanda}). Quem está na
  descida está FORA (estado.fora diz a sala do grupo): os atos da vila são recusados, come-se da própria carga.
  O TEMPO lá dentro anda em LANCES de 20 minutos (ir 1, escondido 2, procurar 2, abrir 1...). Doze lances fecham um BLOCO pelo ato.passa, para o grupo inteiro: só
  então o relógio anda, a tocha de quem leva a luz se gasta, o alarme cai, o treino do ladino conta, e o mundo rola o que vagueia.
  A LUZ é a tocha (um bem da carga: arde um bloco) ou o feitiço luz (4 de Mana por bloco). Sem luz, quem não vê no escuro anda no dobro dos lances, não procura,
  não abre com gazua e não desarma (arromba, sim); a luta tem o escuro (−4 no golpe, −8 no tiro).
  O ENCONTRO: quem vê primeiro escolhe. O grupo que anda escondido rola o teste do mais barulhento (o dado do ladino) contra 20 + a Percepção ÷ 10 do melhor vigia
  da sala (alerta +4, dormindo −6; o morto não dorme): passou, vê primeiro (atacar com eles surpreendidos, esperar, recuar sem ser visto). Notado por quem está
  alerta (ou arma emboscada), quem vai na frente testa a atenção: falhou, o grupo é surpreendido. A porta fechada com gente atrás: a luta começa colada.
  A ARMADILHA bate como uma arma da categoria dela (a conta do aço). Quem vai na frente a vê de passagem, 6 mais difícil; procurar é a rolagem inteira (oculta).
  Achada: desarmar (a gazua), contornar (a do chão), disparar de longe, ou deixá-la. A FECHADURA é a armadura da gazua; a força arromba, e faz barulho.
  O ALARME (0 a 5): a luta, o arrombar e a armadilha que faz barulho o sobem; cai 1 por bloco sem barulho e volta a 0 na virada. Com 2, quem mora lá está alerta;
  com 4, quem está na sala vizinha vem, depois da luta. O QUE VAGUEIA: 1 em 6 por bloco, mais 10 pontos por ponto de alarme.
  A LUTA é a do `ato.py luta`, com as paradas de sempre: este script monta o cenário (o grupo na ordem de marcha, a largura da sala, a luz, a surpresa, o chefe) e,
  no fim, faz as contas: quem morreu sai da contagem da sala, o despojo é pela categoria de quem morreu, o chefe do fundo morto é a primeira limpeza.
  O TESOURO é prata que já existe, posta pelo gerador. Pegar reparte a prata e os bens em partes iguais entre quem está na descida; a peça fica com quem a pega.
  A MEMÓRIA: a sala limpa fica limpa. Volta só o bicho que cria (a regra da caça), o morto que o chefe vivo ergue (um a cada 10 dias) e o bando de fora que acha
  o nível vazio (em 120 dias). O tesouro levado não volta.

Uso (o personagem do jogador, ou quem=ID):
  python3 masmorra.py ver                                       a masmorra vizinha (o que se sabe), a descida aberta, o mapa que o grupo viu, o que se faz daqui
  python3 masmorra.py descer [MASMORRA] [com=ID,ID] [ordem=ID,ID,...] [luz=tocha|feitiço|nada] [quem_luz=ID]
                                                                a ida (os blocos de caminho) e a entrada
  python3 masmorra.py ir SALA [escondido]                       anda à sala vizinha (1 lance; escondido 2; no escuro, o dobro)
  python3 masmorra.py escutar SALA [quem=ID]                    escuta à porta da passagem (1 lance; rolagem oculta)
  python3 masmorra.py procurar [quem=ID]                        procura na sala: armadilha, passagem escondida (2 lances; ocultas)
  python3 masmorra.py abrir SALA|guardado [gazua|chave|força] [quem=ID]      a porta da passagem, ou o que a sala guarda (1 lance por tentativa)
  python3 masmorra.py desarmar [N] [quem=ID] · contornar [N] · disparar [N]   a armadilha achada (1 lance cada)
  python3 masmorra.py atacar [inicio=longe|perto|colado] [passagem] · esperar · recuar      diante de quem apareceu
  python3 masmorra.py luta ["Nome: ordem"] ["grupo: ordem"]     a luta aberta (é o `ato.py luta roda`); acabada, as contas
  python3 masmorra.py pegar [tudo|prata|ITEM] [quem=ID]         o que a sala guarda (1 lance)
  python3 masmorra.py descansar N [vigia=ID]                    dorme N blocos no chão, ali (o que vagueia rola a cada bloco)
  python3 masmorra.py ordem ID,ID,... · luz tocha|feitiço|nada [quem=ID]      a ordem de marcha · a luz (sem lance)
  python3 masmorra.py voltar · sair                             volta pelas salas andadas até a entrada (1 lance por sala) · sai e volta para casa
  SÓ O MESTRE: python3 masmorra.py mapa [MASMORRA] · gera MOLDE "Nome" [vizinho=LUGAR] [niveis=N] [cat=K] [longe=N] · larga "por quê"
"""
import json, math, os, random, re, sys, unicodedata
import tabelas as T
import tabelas_mundo as M
import tabelas_bichos as TB
import tabelas_masmorra as K
import tabelas_manha as TMH
import estado, ato, corpo, teste, bichos, caca

EVENTO = 'masmorra'
FICOU = ('pe', 'caido')         # quem lutou até o fim (de pé, ou caído no campo): só esses têm parte no despojo


# ---------- as palavras ----------
def _s(n, um, muitos): return um if n == 1 else muitos
def _e(L): return caca._e(list(L))
def _cap(x): return x[:1].upper() + x[1:]
def _em(E, lid): return estado.em(E, lid)
def _nm(E, lid): return E['lugares'][lid]['nome']
def _de(E, lid): return estado.de(E, lid)
def _num(d): return caca._num(d)
def _esp(esp): return estado.especie(esp) or {}
def _nome(esp, n=1): return caca._nome(esp, n)
def _sem_vida(esp): return 'sem vida' in (_esp(esp).get('tracos') or [])
def _fera(esp): return bool(_esp(esp).get('fera', True))
def _lances(n): return f"{n} {_s(n, 'lance', 'lances')}"
def _txt(x): return TB.contrai(x)
def _pn(E, pid): return E['gente'][pid]['nome']
def _a_nome(n):
    """'à capela', 'ao ossário', 'aos degraus' (a preposição a com o artigo do nome)"""
    art, _, resto = n.partition(' ')
    return ({'a': 'à ', 'o': 'ao ', 'as': 'às ', 'os': 'aos '}[art] + resto) if art in ('a', 'o', 'as', 'os') and resto else 'a ' + n
def _em_nome(n):
    art, _, resto = n.partition(' ')
    return ({'a': 'na ', 'o': 'no ', 'as': 'nas ', 'os': 'nos '}[art] + resto) if art in ('a', 'o', 'as', 'os') and resto else 'em ' + n


def _povos():
    try:
        import povos
        return povos
    except ImportError: return None


def _dragoes():
    try:
        import dragoes
        return dragoes
    except ImportError: return None


def _manha():
    import manha
    return manha


def ve_no_escuro(p):
    P = _povos()
    return bool(P and P.ve_no_escuro(p))


# ---------- o lugar (o que as outras frentes chamam) ----------
def de(E, lid):
    """o id da masmorra deste lugar (o lugar é a masmorra, ou uma sala dela), ou None"""
    l = E['lugares'].get(lid) if isinstance(lid, str) else None
    if not isinstance(l, dict): return None
    if l.get('tipo') == 'masmorra': return lid
    return l.get('masmorra') if l.get('tipo') == 'sala' and l.get('masmorra') in E['lugares'] else None


def salas(E, mid):
    """as salas da masmorra, nível a nível (a ordem dos níveis dela)"""
    m = E['lugares'].get(mid) or {}
    return [s for nv in m.get('niveis') or [] for s in nv.get('salas') or [] if s in E['lugares']]


def masmorras(E, lid):
    """as masmorras vizinhas de um lugar"""
    return [v for v in (E['lugares'][lid].get('vizinhos') or []) if (E['lugares'].get(v) or {}).get('tipo') == 'masmorra']


def _sala(E, sid): return E['lugares'][sid]
def _mid(E, sid): return _sala(E, sid)['masmorra']
def _m(E, sid): return E['lugares'][_mid(E, sid)]
def _viz(E, sid): return [v for v in (_sala(E, sid).get('vizinhos') or []) if v in E['lugares']]
def bichos_de(E, sid): return {e: int(q) for e, q in _num(_sala(E, sid).get('bichos')).items() if estado.especie(e) and q >= 1}
def _pk(a, b): return '|'.join(sorted((a, b)))
def porta(E, a, b): return (_m(E, a).get('portas') or {}).get(_pk(a, b))
def _longe(E, mid): v = E['lugares'][mid].get('longe'); return v if isinstance(v, int) and not isinstance(v, bool) and v >= 1 else 1


def _chefe_vivo(E, sid):
    c = _sala(E, sid).get('chefe')
    return c if isinstance(c, dict) and c.get('qual') and c.get('vivo', True) else None


def _dragao(E, sid):
    d = _sala(E, sid).get('dragao')
    return d if isinstance(d, dict) and d.get('nome') else None


def ocupada(E, sid): return bool(bichos_de(E, sid) or _chefe_vivo(E, sid) or _dragao(E, sid))


def _cat_de(E, sid, esp):
    """a categoria de quem mora na sala: a da sala (a do nível); a espécie de categoria maior fica na dela"""
    c = _sala(E, sid).get('cat'); ce = _esp(esp).get('cat', 0)
    return max(ce, c) if isinstance(c, int) and not isinstance(c, bool) else ce


def _nivel(E, sid):
    for nv in _m(E, sid).get('niveis') or []:
        if sid in (nv.get('salas') or []): return nv
    return {}


def fundo(E, mid):
    """a sala do fundo: a última do último nível que tem chefe (ou dragão); senão, a última do último nível"""
    m = E['lugares'][mid]; nv = (m.get('niveis') or [{}])[-1].get('salas') or []
    com = [s for s in nv if s in E['lugares'] and (E['lugares'][s].get('chefe') or E['lugares'][s].get('dragao'))]
    return (com or nv or [None])[-1]


def _chefe_nome(qual):
    import tabelas_criaturas as TC
    C = TC.CHEFES.get(qual)
    if C: return C.get('nome') or (C.get('especie') and f"{TC.ESPECIES[C['especie']]['artigo']} {TC.ESPECIES[C['especie']]['nome']}") or qual
    e = _esp(qual); return f"{e.get('artigo', 'o')} {e.get('nome', qual)}"


def _chefe_cat(qual):
    import tabelas_criaturas as TC
    C = TC.CHEFES.get(qual)
    if C: return C['cat'] if C.get('cat') is not None else TC.ESPECIES[C['especie']]['cat']
    return _esp(qual).get('cat', 0)


def _diz_bando(n, chefe=None, dragao=None):
    L = [_nome(e, q) for e, q in n.items()]
    if chefe: L.insert(0, _chefe_nome(chefe['qual']))
    if dragao: L.insert(0, dragao['nome'])
    return _e(L) or 'ninguém'


def _largura_diz(l):
    g = l.get('largura')
    return 'corredor de um' if g == 1 else f'sala de {g}' if g else 'sala aberta'


def _alarme_diz(E, mid):
    al = E['lugares'][mid].get('alarme', 0) or 0
    return f"{_cap(E['lugares'][mid]['nome'])} está {K.ALARME_DIZ.get(al, K.ALARME_DIZ[5])}"


# ---------- a descida ----------
def descida(p):
    """a descida que esta pessoa COMANDA (marca.masmorra), ou None"""
    d = (p.get('marca') or {}).get('masmorra') if isinstance(p.get('marca'), dict) else None
    return d if isinstance(d, dict) and d.get('de') is None else None


def vai_com(p):
    """de quem é a descida em que esta pessoa foi junto, ou None"""
    d = (p.get('marca') or {}).get('masmorra') if isinstance(p.get('marca'), dict) else None
    return d.get('de') if isinstance(d, dict) else None


def _grupo(E, pid, d):
    return [pid] + [c for c in d.get('com') or [] if c in E['gente'] and E['gente'][c]['estado'] == 'vivo' and vai_com(E['gente'][c]) == pid]


def _ordem(E, pid, d):
    g = _grupo(E, pid, d); o = [x for x in d.get('ordem') or [] if x in g]
    return o + [x for x in g if x not in o]


def _frente(E, pid, d): return _ordem(E, pid, d)[0]


def _solta(E, d):
    return [['pessoa', c, 'marca.masmorra', 'poe', None] for c in (d or {}).get('com') or [] if c in E['gente'] and (E['gente'][c].get('marca') or {}).get('masmorra') is not None]


def _marca(E, pid, d, texto, mais=(), tipo=EVENTO, quem=None):
    """a descida (ou None: fechada, e quem foi junto fica solto) fica escrita em quem comanda, por evento, com os efeitos da ação"""
    ant = descida(E['gente'][pid]) or d or {}
    ef = [['pessoa', pid, 'marca.masmorra', 'poe', d]] + (_solta(E, ant) if d is None else []) + list(mais)
    sala = (d or ant).get('sala')
    return estado.aplica(E, tipo, ef, onde=sala if sala in E['lugares'] else None, quem=quem or (_grupo(E, pid, ant) if ant else [pid]), texto=_txt(texto))


def _minha(E, pid, vivo=True, fases=None):
    """a pessoa e a descida que ela comanda (uma cópia); recusa, com a frase, quem não tem descida ou só foi junto na de outro"""
    p = E['gente'].get(pid) or sys.exit(f'não há a pessoa "{pid}"')
    if vai_com(p): sys.exit(f"{p['nome']} foi junto na descida de {E['gente'].get(vai_com(p), {}).get('nome', vai_com(p))}: quem decide é quem comanda (`quem={vai_com(p)}`)")
    d = descida(p)
    if not d and p['estado'] != 'vivo': sys.exit(f"{p['nome']} não age: {estado.morte_diz(E, p)}. Não há descida aberta para fechar.")
    if not d: sys.exit(f"{p['nome']} não tem descida aberta (`masmorra.py descer`)")
    if d.get('masmorra') not in E['lugares'] or d.get('sala') not in E['lugares'] or not isinstance(d.get('caminho'), list):
        sys.exit(f"a descida de {p['nome']} está torta (o estado não a descreve direito: `estado.py valida`). SÓ O MESTRE: `masmorra.py larga \"por quê\"` a fecha sem as contas")
    if vivo and p['estado'] != 'vivo': sys.exit(f"{p['nome']} não age: {estado.morte_diz(E, p)}. A descida fecha com `masmorra.py sair quem={pid}`")
    d = json.loads(json.dumps(d))
    if fases and d.get('fase') not in fases:
        if d.get('fase') == 'luta': sys.exit(f"há uma luta aberta: `masmorra.py luta \"{p['nome']}: ordem\"` (acabada, as contas)")
        if d.get('fase') == 'encontro': sys.exit(f"há gente à frente ({_diz_bando(d['encontro']['n'], d['encontro'].get('chefe') and {'qual': d['encontro']['chefe']}, d['encontro'].get('dragao') and {'nome': d['encontro']['dragao']})}): `masmorra.py atacar`, `esperar` ou `recuar`")
        if d.get('fase') == 'armadilha': sys.exit(f"há uma armadilha achada à frente: `masmorra.py desarmar`, `contornar` ou `disparar` (ou `voltar`)")
        sys.exit(f"agora não (a descida está em \"{d.get('fase')}\")")
    return p, d


def _luz_de(E, pid, d):
    """há luz para o grupo? (a tocha ou o feitiço de alguém do grupo, ou a sala acesa)"""
    lz = d.get('luz') or {}
    return bool(_sala(E, d['sala']).get('acesa') or (lz.get('tipo') and lz.get('quem') in _grupo(E, pid, d)))


def _ve(E, pid, d, quem=None):
    """quem (ou o grupo) vê o que faz: há luz, ou ele vê no escuro (sem quem: todos veem no escuro)"""
    if _luz_de(E, pid, d): return True
    if quem: return ve_no_escuro(E['gente'][quem])
    return all(ve_no_escuro(E['gente'][c]) for c in _grupo(E, pid, d))


def _alguem_ve(E, pid, d): return _luz_de(E, pid, d) or any(ve_no_escuro(E['gente'][c]) for c in _grupo(E, pid, d))


def _de_tras(E, pid):
    a = estado.pecas(E, pid)['arma']
    return bool(a and a.get('tipo') == 'arma' and (T.FAMILIAS.get(a.get('familia')) or {}).get('distancia'))


def _mapa_ef(E, pid, d, salas_=(), armadilhas=()):
    """o que o grupo viu fica escrito em cada um (marca.mapa: o herdeiro não sabe o mapa do morto)"""
    mid = d['masmorra']; ef = []
    for c in _grupo(E, pid, d):
        mp = json.loads(json.dumps((E['gente'][c].get('marca') or {}).get('mapa') or {}))
        r = mp.setdefault(mid, {}); s = r.setdefault('salas', []); a = r.setdefault('armadilhas', []); muda = False
        for x in salas_:
            if x not in s: s.append(x); muda = True
        for x in armadilhas:
            if x not in a: a.append(x); muda = True
        if muda: ef.append(['pessoa', c, 'marca.mapa', 'poe', mp])
    return ef


def _treina(d, ids):
    d['treino'] = list(dict.fromkeys(list(d.get('treino') or []) + [x for x in ids if x]))


def _alarme_ef(E, mid, n):
    m = E['lugares'][mid]; al = m.get('alarme', 0) or 0; novo = max(0, min(M.ALARME_MAX, al + n))
    return [['lugar', mid, 'alarme', 'poe', novo]] if novo != al else []


# ---------- o tempo: os lances e o bloco ----------
def _fecha_blocos(E, pid, L):
    """os lances que passaram de 12 fecham blocos (o ato.passa do grupo). Devolve o que parou (quem vagueia chegou), ou None"""
    for _ in range(50):
        p = E['gente'][pid]; d = descida(p)
        if p['estado'] != 'vivo' or not d or d.get('lances', 0) < K.LANCES_BLOCO or d.get('fase') == 'luta': return None
        R = _bloco(E, pid, L)
        if R: return R
    return None


def _bloco(E, pid, L, dorme=None, vigia=None, inteiro=False):
    """UM BLOCO lá dentro: o relógio anda para o grupo (o ato.passa), a luz se gasta, o treino do ladino conta, o alarme cai; depois, o mundo rola o que vagueia"""
    p = E['gente'][pid]; d = json.loads(json.dumps(descida(p))); mid = d['masmorra']; m = E['lugares'][mid]; g = _grupo(E, pid, d)
    if not dorme: d['lances'] = 0 if inteiro else max(0, d.get('lances', 0) - K.LANCES_BLOCO)
    d['blocos'] = d.get('blocos', 0) + 1; ef = []; luz_diz = None
    lz = d.get('luz') or {}
    if not dorme and lz.get('tipo'):
        q = lz.get('quem'); qp = E['gente'].get(q)
        if q not in g: d['luz'] = dict(tipo=None, quem=None); luz_diz = 'a luz se perdeu: o grupo está no escuro'
        elif lz['tipo'] == 'tocha':
            tem = (qp.get('carga') or {}).get('tocha', 0)
            if tem >= 1: ef.append(['pessoa', q, 'carga.tocha', 'soma', -1]); tem -= 1
            if tem <= 0: d['luz'] = dict(tipo=None, quem=None); luz_diz = f"a última tocha de {qp['nome']} se apaga: A LUZ ACABOU" + ('' if not any((E['gente'][c].get('carga') or {}).get('tocha', 0) for c in g if c != q) else ' (há tocha na carga de outro: `masmorra.py luz tocha quem=ID`)')
            elif tem == 1: luz_diz = f"a tocha de {qp['nome']} se gasta: A ÚLTIMA começa a arder"
            else: luz_diz = f"a tocha de {qp['nome']} se gasta (restam {tem})"
        else:
            mn = estado.mana(qp)
            if mn >= K.LUZ_MANA_BLOCO: ef.append(['pessoa', q, 'mana', 'soma', -K.LUZ_MANA_BLOCO]); mn -= K.LUZ_MANA_BLOCO
            if mn < K.LUZ_MANA_BLOCO: d['luz'] = dict(tipo=None, quem=None); luz_diz = f"a Mana de {qp['nome']} não sustenta o feitiço: A LUZ ACABOU"
            else: luz_diz = f"o feitiço de {qp['nome']} gasta {K.LUZ_MANA_BLOCO} de Mana (restam {mn})"
    if not dorme:
        for c in [x for x in d.get('treino') or [] if x in g]: ef += list(_manha().treino(E, c, TMH.TREINO_BLOCO) or [])
    d['treino'] = []
    al = m.get('alarme', 0) or 0
    if not d.get('barulho') and al > 0: ef.append(['lugar', mid, 'alarme', 'poe', max(0, al - K.ALARME['acalma'])])
    d['barulho'] = False
    sono = [c for c in g if c != vigia]
    ator = pid if pid in sono or not dorme else sono[0]
    com = [c for c in (g if not dorme else sono) if c != ator]
    eu = estado.eu(E); mao_vigia = []
    if dorme and vigia and vigia != eu: mao_vigia = corpo.bloco(E, vigia, 'nada', None) + ato._bloco_dos_modulos(E, vigia, 'nada', None)
    txt = (f"o grupo dorme no chão {_em(E, d['sala'])}" + (f" ({_pn(E, vigia)} vigia)" if vigia else '')) if dorme else f"um bloco passa na descida, {_em(E, d['sala'])}"
    _, pq = ato.passa(E, ator, 1, EVENTO, esforco='nada' if dorme else K.ESFORCO_BLOCO, dorme=dorme, texto=_txt(txt), com=com, para=not dorme,
                      mais=lambda i: ef + mao_vigia + [['pessoa', pid, 'marca.masmorra', 'poe', d]])
    L.append(f"UM BLOCO FECHA ({estado.quando(E)})" + (f": {luz_diz}" if luz_diz else '') + '.')
    if pq: L.append(f"O corpo: {pq}.")
    caca.merenda(E, [c for c in g if c != pid], L)
    p = E['gente'][pid]
    if p['estado'] != 'vivo': return _morreu(E, pid, L)
    return _vaga(E, pid, L, dorme=bool(dorme), vigia=vigia)


def chance_vaga(E, mid):
    """a chance do que vagueia num bloco lá dentro: 1 em 6, mais 10 pontos por ponto de alarme (até 1)"""
    return min(1.0, K.VAGA[0] + K.VAGA[1] * (E['lugares'][mid].get('alarme', 0) or 0))


def _sorteia(pesos, r):
    tot = sum(pesos.values()); x = r.random() * tot
    for k in sorted(pesos):
        x -= pesos[k]
        if x < 0: return k
    return sorted(pesos)[-1]


def _vaga(E, pid, L, dorme=False, vigia=None):
    """o mundo rola o que vagueia (oculto: o dado do mundo). Saindo, um bando dos vagantes da masmorra chega ao grupo (sai da conta dela e entra na sala)"""
    p = E['gente'][pid]; d = descida(p); mid = d['masmorra']; m = E['lugares'][mid]
    vag = {e: int(q) for e, q in _num(m.get('vagantes')).items() if q >= 1 and estado.especie(e)}
    rs = estado.sorte(E, f"masmorra|{pid}|vaga|{d.get('blocos', 0)}|{d.get('lutas', 0)}")
    x = rs.random()
    if not vag or x >= chance_vaga(E, mid): return None
    esp = _sorteia(vag, rs); n = max(1, min(vag[esp], len(bichos.bando(esp, rs))))
    sid = d['sala']
    estado.aplica(E, EVENTO, [['lugar', mid, f'vagantes.{esp}', 'soma', -n], ['lugar', sid, f'bichos.{esp}', 'soma', n], ['lugar', sid, 'atento', 'poe', 1]], onde=sid, quem=_grupo(E, pid, d),
                  texto=_txt(f"{_nome(esp, n)} {_s(n, 'chega', 'chegam')} {_em(E, sid)}, vindo do escuro"))
    if dorme: surp = None if vigia else 'A'
    else: surp = _atencao(E, pid, d, sid, L)
    enc = dict(sala=sid, onde=sid, n=bichos_de(E, sid), chefe=None, dragao=None, viu='eles', surpresa=surp, inicio=K.INICIO['vem'], ouviu=False, vem=True)
    L.append(f"QUEM VAGUEIA CHEGA: {_nome(esp, n)}" + (' (dormiam todos, sem vigia: o grupo é surpreendido)' if dorme and not vigia else ' (quem vigiava os viu chegar)' if dorme else '') + '.')
    return _encontro(E, pid, enc, L)


# ---------- o que mora na sala ----------
def _bando(E, pid, sid, k=0, para_luta=False):
    """os que moram na sala, prontos (para ler o que veem, ou para o cenário da luta): (chefe, [criaturas])"""
    import criaturas
    n = bichos_de(E, sid); ch = _chefe_vivo(E, sid); out = []; chefe_p = None
    if ch: chefe_p = _chefe_pessoa(ch['qual'])
    for esp, q in n.items():
        bs = bichos.bando(esp, estado.sorte(E, f'masmorra|{pid}|bando|{sid}|{k}|{esp}'), n=q, cat=_cat_de(E, sid, esp))
        out += bs
    return chefe_p, out


def _chefe_pessoa(qual):
    """o chefe pronto para a luta: um dos tabelas_criaturas.CHEFES (sem os lacaios: a guarda é quem mora na sala), ou uma espécie que é chefe (a serpe, a hidra)"""
    import criaturas, tabelas_criaturas as TC
    if qual in TC.CHEFES: return criaturas.chefe(qual, lacaios=False)[0]
    p = bichos.bicho(qual, lider=True); p['chefe'] = True
    return p


def _vigia(E, pid, d, sid):
    """o melhor vigia da sala: (Percepção ÷ 10, Agilidade ÷ 10 do mais ágil, atento): o morto não dorme; o alarme alto deixa todos alertas"""
    chefe_p, bs = _bando(E, pid, sid)
    todos = ([chefe_p] if chefe_p else []) + bs
    if not todos: return 0, 0, 0
    per = max(x['atributos']['Percepção'] for x in todos) // 10; agi = max(x['atributos']['Agilidade'] for x in todos) // 10
    at = _sala(E, sid).get('atento', 0) or 0
    if (E['lugares'][d['masmorra']].get('alarme', 0) or 0) >= K.ALARME['alerta']: at = max(at, 1)
    if at < 0 and all(_sem_vida(e) for e in bichos_de(E, sid)) and not (chefe_p and not _sem_vida((chefe_p.get('povo') or {}).get('especie', ''))): at = 0
    return per, agi, at


def _atencao(E, pid, d, sid, L):
    """quem vai na frente testa a atenção (oculto) contra 20 + a Agilidade ÷ 10 dos que vêm: falhou, o grupo é surpreendido. Devolve a surpresa ('A' ou None)"""
    _, agi, _ = _vigia(E, pid, d, sid); f = _frente(E, pid, d)
    r = _manha().testa(E, f, 'atencao', contra=K.ATENCAO + agi, o_que=f"notar quem chega {_em(E, sid)}", oculto=True)
    if r.get('efeitos'): estado.aplica(E, EVENTO, r['efeitos'], onde=sid, quem=[f], texto=f"{_pn(E, f)} percebe que tem um dom")
    L.append(teste.diz(E, r))
    return None if r['passou'] else 'A'


def _encontro(E, pid, enc, L):
    """alguém à frente: a descida para e pergunta (atacar, esperar, recuar)"""
    p = E['gente'][pid]; d = json.loads(json.dumps(descida(p))); sid = enc['sala']
    d.update(fase='encontro', encontro=enc)
    mais = [] if enc.get('viu') == 'grupo' or _sala(E, sid).get('atento') == 1 else [['lugar', sid, 'atento', 'poe', 1]]
    quem = _diz_bando(enc['n'], enc.get('chefe') and {'qual': enc['chefe']}, enc.get('dragao') and {'nome': enc['dragao']})
    _marca(E, pid, d, (f"o grupo vê {quem} {_em(E, sid)}, sem ser visto" if enc['viu'] == 'grupo' and not enc.get('ouviu') else f"o grupo ouve gente {_em(E, sid)}, no escuro" if enc.get('ouviu')
                       else f"{quem} {_s(sum(enc['n'].values()) + bool(enc.get('chefe')) + bool(enc.get('dragao')), 'vê', 'veem')} o grupo {_em(E, sid)}"), mais=mais)
    return dict(fase='encontro', encontro=enc, texto='\n'.join(L + le_encontro(E, pid)))


def le_encontro(E, pid):
    """o que o grupo lê com alguém à frente: quem é (a ameaça), quem viu primeiro, e as escolhas"""
    p = E['gente'][pid]; d = descida(p)
    if not d or d.get('fase') != 'encontro': return []
    enc = d['encontro']; arma, armadura = caca._veste(E, pid); n = enc['n']; L = []
    quem = _diz_bando(n, enc.get('chefe') and {'qual': enc['chefe']}, enc.get('dragao') and {'nome': enc['dragao']})
    if enc.get('ouviu'):
        L.append("NO ESCURO, O GRUPO OUVE GENTE À FRENTE: há quem more aqui, e não se sabe quantos. Eles não sabem do grupo.")
    else:
        L.append(('O GRUPO VÊ PRIMEIRO: ' if enc['viu'] == 'grupo' else 'APARECEM: ' if not enc.get('vem') else 'CHEGAM: ') + quem + '.'
                 + (' Eles não viram o grupo.' if enc['viu'] == 'grupo' else ' ELES PEGAM O GRUPO DESPREVENIDO: o grupo perde o primeiro turno.' if enc.get('surpresa') == 'A' else ' Ninguém foi pego desprevenido.')
                 + ('' if _luz_de(E, pid, d) else ' Está ESCURO: a luta terá −4 no golpe e −8 no tiro (para quem não vê no escuro).'))
        for e, q in n.items(): L.append(bichos.ameaca(e, n=q, arma=arma, armadura=armadura))
        if enc.get('chefe'): L.append(f"{_cap(_chefe_nome(enc['chefe']))} é quem manda aqui (o Mestre lê o que se sabe dele).")
        if enc.get('dragao') and _dragoes():
            dr = _dragao(E, enc['sala'])
            if dr:
                try: L.append(_dragoes().ameaca(dr['tipo'], dr['idade'], arma=arma, armadura=armadura))
                except (Exception, SystemExit): pass
    ant = d.get('anterior'); corr = ant in E['lugares'] and E['lugares'][ant].get('largura')
    if enc['viu'] == 'grupo':
        inis = ['perto', 'colado'] + (['longe'] if _sala(E, enc['sala']).get('largura') is None else [])
        L.append(f"ESCOLHA: `masmorra.py atacar [inicio={'|'.join(inis)}]" + (' [passagem]' if corr else '') + "` (eles perdem o primeiro turno" + (f"; `passagem`: o grupo espera na boca {_de(E, ant)} ({_largura_diz(E['lugares'][ant])}) e eles vêm um a um" if corr else '') + ")"
                 + f" · `masmorra.py esperar` ({_lances(K.CUSTO['esperar'])}, escondido) · `masmorra.py recuar` (volta sem ser visto)")
    else:
        pas = corr and enc.get('surpresa') != 'A' and enc.get('onde', enc['sala']) == d['sala'] and _sala(E, enc['sala']).get('largura') != 1
        L.append(f"ESCOLHA: `masmorra.py atacar" + (" [passagem]" if pas else '') + f"` (a luta começa {enc.get('inicio', 'perto')}" + (f"; `passagem`: o grupo recua à boca {_de(E, ant)} ({_largura_diz(E['lugares'][ant])}) e eles vêm um a um" if pas else '') + ") · `masmorra.py recuar` (volta à sala de onde veio; " + ('os mortos lentos não saem da sala deles' if all(_sem_vida(e) for e in n) and not enc.get('dragao') else 'eles podem vir atrás') + ')')
    return [_txt(x) for x in L]


def _ve_quem(E, pid, sid, L, escondido=False, porta_fechada=False):
    """o grupo entra numa sala com gente: quem vê primeiro (o escondido do mais barulhento; a atenção de quem vai na frente). Devolve o encontro, ou None"""
    if not ocupada(E, sid): return None
    p = E['gente'][pid]; d = descida(p); g = _grupo(E, pid, d); mh = _manha()
    n = bichos_de(E, sid); ch = _chefe_vivo(E, sid); dr = _dragao(E, sid); D = _dragoes()
    per, agi, at = _vigia(E, pid, d, sid)
    luz = _luz_de(E, pid, d) and not _sala(E, sid).get('acesa')
    viu, surp, ouviu = 'eles', None, False
    ini = K.INICIO['porta'] if porta_fechada else K.INICIO['notou']
    if escondido and not porta_fechada:
        q, mais = mh.mais_barulhento(E, g, luz=luz)
        contra = K.ESCONDIDO + per + K.ATENTO.get(at, 0)
        if dr and D:
            v = D.vigilia(E, sid)
            if v is not None: contra = v
        r = mh.testa(E, q, 'escondido', contra=contra, o_que=f"andar escondido {_em(E, sid)}", oculto=True, mais=mais)
        if r.get('efeitos'): estado.aplica(E, EVENTO, r['efeitos'], onde=sid, quem=[q], texto=f"{_pn(E, q)} percebe que tem um dom")
        L.append(teste.diz(E, r))
        if r['passou']:
            viu = 'grupo'; ouviu = not _alguem_ve(E, pid, d)
            ini = K.INICIO['aberta'] if _sala(E, sid).get('largura') is None else K.INICIO['viu']
    if viu == 'eles' and (at >= 1 or any(e in K.EMBOSCA for e in n)): surp = _atencao(E, pid, d, sid, L)
    return dict(sala=sid, onde=sid, n=n, chefe=ch['qual'] if ch else None, dragao=dr['nome'] if dr else None, viu=viu, surpresa=surp, inicio=ini, ouviu=ouviu)


# ---------- as armadilhas ----------
def _tronco_cat(F): return F['partes']['tronco']['cat'] if 'tronco' in F.get('partes', {}) else None


def golpe(F, tipo, cat, r, esquiva=None):
    """UM DISPARO contra a ficha F (pessoas.ficha): (dano, parte, crítico, escapou). A armadilha bate como uma arma da categoria dela: o dano é o da luta, dado × 4 ×
    o valor da categoria ÷ a proteção da parte que pega (o material contra o golpe; a parte nua conta um terço). O dardo e a lâmina rolam o acerto (2d20 + 6 + o bônus
    da categoria, contra a Defesa sem escudo); a runa, contra a Firmeza, e o dano dela (e o do gás) é pela guarda (o amuleto, ou 0,6 da armadura do tronco).
    O fosso e a pedra: Agilidade contra 20 + 6 por categoria (passou, escapa); o gás: Vigor (passou, a metade).
    r: random.Random dos dados da armadilha (o dado do mundo); esquiva(atributo, contra) → passou? (o teste de quem pega; sem ele, rola com r)"""
    a = K.ARMADILHAS[tipo]
    if not a.get('dado'): return 0, None, False, True
    def d20x():
        t = [r.randint(1, 20)]
        while t[-1] == 20: t.append(r.randint(1, 20))
        return t
    def rola(dado, vezes=1):
        n, f = map(int, dado.split('d')); return sum(r.randint(1, f) for _ in range(n * vezes))
    g, crit = a['golpe'], False
    if a['escapa'] in ('acerto', 'Firmeza'):
        d1, d2 = d20x(), d20x(); tot = sum(d1) + sum(d2) + K.ARMADILHA_ACERTO + T.BON[cat]
        crit = max(d1[0], d2[0]) == 20 and min(d1[0], d2[0]) >= T.CRIT_OUTRO
        contra = F.get('firmeza') or 22 + F['atributos']['Vontade'] // 20 if a['escapa'] == 'Firmeza' else F['def_fixa']
        if (d1[0], d2[0]) == (1, 1) or (tot < contra and not crit): return 0, None, False, True
        if g == 'guarda':
            gd = T.guarda(F.get('amuleto_cat'), _tronco_cat(F))
            return int(rola(a['dado'], 2 if crit else 1) * T.K_DANO * T.MULT[cat] / (gd / (2 if crit else 1))), 'tronco', crit, False
        parte = T.ONDE[r.randint(1, 10)]
    else:
        contra = K.ESQUIVA[0] + K.ESQUIVA[1] * cat
        passou = esquiva(a['escapa'], contra) if esquiva else sum(d20x()) + sum(d20x()) + F['atributos'][a['escapa']] // 10 >= contra
        if g == 'guarda':
            gd = T.guarda(F.get('amuleto_cat'), _tronco_cat(F)); dn = int(rola(a['dado']) * T.K_DANO * T.MULT[cat] / gd)
            return (dn // 2 if passou and a.get('metade') else dn), 'tronco', False, passou
        if passou: return 0, None, False, True
        parte = a.get('parte') or ('cabeça' if r.random() < a.get('cabeca', 0.3) else 'tronco')
        if tipo == 'fosso' and cat >= a.get('estacas_desde', 99): g = 'ponta'
    pc = F['partes'].get(parte)
    prot = (pc['rd'] * T.MATRIZ[g][pc['material']] / (2 if crit else 1)) if pc else T.NU
    return int(rola(a['dado'], 2 if crit else 1) * T.K_DANO * T.MULT[cat] / prot), parte, crit, False


def _fere(E, pid, dano, parte, crit):
    """o dano da armadilha no estado (a regra da luta): a zero de PV, morre se o golpe tirou mais da metade do PV máximo; senão cai e fica com 1. A ferida pela fração."""
    p = E['gente'][pid]; mx = estado.pv_max(p)
    if dano <= 0: return [], ''
    if dano >= p['pv'] and dano > mx * T.FERIDA_GRAVE: return [['pessoa', pid, 'estado', 'poe', 'morto']], 'MORRE'
    ef = [['pessoa', pid, 'pv', 'soma', -min(dano, p['pv'] - 1)]]; diz = f"PV {max(1, p['pv'] - dano)}/{mx}"
    if dano >= p['pv']: diz = f"CAI (fica com 1 de PV)"
    if dano >= mx * T.FERIDA_GRAVE: ef.append(['ferida', pid, 'abre', parte, True]); diz += ', ferida grave'
    elif dano >= mx * T.FERIDA or (crit and dano >= mx * T.FERIDA_MIN): ef.append(['ferida', pid, 'abre', parte, False]); diz += ', ferida'
    return ef, diz


def _arm_nome(a): return f"{'o' if a['tipo'] in ('dardo', 'fosso', 'gás', 'alarme') else 'a'} {a['tipo']} {(T.CATS if a['tipo'] in ('dardo', 'fosso', 'gás', 'alarme') else caca.FEM)[a['cat']]}"


def _arm_onde(E, sid, a):
    o = a.get('onde', 'chão')
    if o == 'chão': return 'no chão'
    if o == 'guardado': return f"n{(_sala(E, sid).get('guardado') or {}).get('nome', 'o guardado')}"
    return f"na porta ({o[6:]})" if o[6:] in E['lugares'] else 'numa porta'


def _dispara(E, pid, sid, i, alvos, L, porque='dispara'):
    """a armadilha i da sala dispara: em quem (alvos), o golpe pela conta do aço, o barulho. Um evento só. Devolve se alguém do grupo morreu"""
    from pessoas import ficha
    d = descida(E['gente'][pid]); arms = json.loads(json.dumps(_sala(E, sid).get('armadilhas') or [])); a = arms[i]; A = K.ARMADILHAS[a['tipo']]
    arms[i] = dict(a, feita='disparada'); mid = _mid(E, sid)
    ef = [['lugar', sid, 'armadilhas', 'poe', arms]] + _alarme_ef(E, mid, A.get('barulho', 0)); linhas = []; mortos = []
    rs = estado.sorte(E, f"masmorra|{sid}|armadilha|{i}")
    pega = _grupo(E, pid, d) if A['pega'] == 'todos' else alvos[:1] if A['pega'] == 'um' else []
    for q in pega:
        F = ficha(estado.lutador(E, q)); qn = _pn(E, q)
        def esquiva(at, contra, q=q, qn=qn):
            r = teste.rola(E, f"escapar d{'o' if a['tipo'] in ('dardo', 'fosso', 'gás') else 'a'} {a['tipo']}", at, contra, quem=q); linhas.append(teste.diz(E, r)); return r['passou']
        dano, parte, crit, escapou = golpe(F, a['tipo'], a['cat'], rs, esquiva)
        if dano <= 0: linhas.append(f"{qn} escapa." if escapou else f"{qn}: o golpe não passa."); continue
        e2, diz = _fere(E, q, dano, parte, crit); ef += e2
        linhas.append(f"{qn}: {dano} {caca.NA_PARTE.get(parte, 'no corpo') if parte else ''}{' (CRÍTICO)' if crit else ''}: {diz}.")
        if diz == 'MORRE': mortos.append(q)
        if a['tipo'] == 'runa' and a['cat'] >= A.get('amaldicoa_desde', 99) and diz != 'MORRE':
            try:
                import maldicao
                mo = maldicao.molde(K.RUNA_MALDICAO['nome'], a['cat'], K.RUNA_MALDICAO['tipo'], dict(tipo='sair', lugar=sid))
                ef += maldicao.poe(E, q, mo, 'lugar', fonte=sid, condicao=dict(tipo='sair', lugar=sid, visto=E['relogio']['dia'])); linhas.append(f"{qn} sente a runa grudar nele: uma maldição.")
            except (ImportError, SystemExit): pass
    if a['tipo'] == 'fosso' and pega and not mortos: linhas.append(f"{_pn(E, pega[0])} fica no fundo do fosso: tirá-lo custa {_lances(K.CUSTO['fosso'])}.")
    if A.get('barulho') and d: d2 = json.loads(json.dumps(d)); d2['barulho'] = True; ef.append(['pessoa', pid, 'marca.masmorra', 'poe', d2])
    txt = f"{_cap(_arm_nome(a))} {_arm_onde(E, sid, a)} {_em(E, sid)} {porque}" + (f" em {_e(_pn(E, q) for q in pega)}" if pega else '') + (f" ({A['diz']})" if A.get('diz') else '')
    estado.aplica(E, EVENTO, ef, onde=sid, quem=pega or [pid], texto=_txt(txt))
    L.append(_txt(f"A ARMADILHA DISPARA: {txt}. " + ' '.join(linhas) + (f" O barulho sobe o alarme." if A.get('barulho') else '')))
    return bool(mortos), (K.CUSTO['fosso'] if a['tipo'] == 'fosso' and pega and not mortos else 0)


def _achadas(E, sid, d=None):
    """as armadilhas achadas e não resolvidas desta sala: [(número à mesa, índice, armadilha)]"""
    return [(k + 1, i, a) for k, (i, a) in enumerate((i, a) for i, a in enumerate(_sala(E, sid).get('armadilhas') or []) if a.get('achada') is not None and a.get('feita') is None)]


def _de_passagem(E, pid, d, sid, onde, L):
    """quem vai na frente olha, de graça, ao entrar na sala (o chão) ou ao chegar à porta (6 mais difícil; oculta). Devolve [(índice, armadilha)] das achadas agora"""
    f = _frente(E, pid, d); mh = _manha(); achou = []; arms = json.loads(json.dumps(_sala(E, sid).get('armadilhas') or []))
    if not _ve(E, pid, d, f): return []
    for i, a in enumerate(arms):
        if a.get('achada') is not None or a.get('feita') is not None or a.get('onde', 'chão') != onde: continue
        r = mh.testa(E, f, 'achar', cat=a['cat'], o_que=f"ver de passagem o que há {_em(E, sid)}", oculto=True, mais=K.PASSAGEM, pedra=a['tipo'] == 'pedra')
        L.append(teste.diz(E, r))
        if r['passou']: arms[i]['achada'] = E['relogio']['dia']; achou.append((i, arms[i]))
    if achou:
        estado.aplica(E, EVENTO, [['lugar', sid, 'armadilhas', 'poe', arms]] + _mapa_ef(E, pid, d, armadilhas=[f"{sid}#{i}" for i, _ in achou]), onde=sid, quem=[f],
                      texto=_txt(f"{_pn(E, f)} vê {_e(_arm_nome(a) + ' ' + _arm_onde(E, sid, a) for _, a in achou)} {_em(E, sid)}"))
    return achou


# ---------- descer ----------
def descer(E, pid, mid=None, com=(), ordem=None, luz=None, quem_luz=None):
    """a ida: o grupo sai de casa para a masmorra vizinha (os blocos de caminho) e chega à entrada"""
    p = estado.presente(E, pid, 'descer'); aqui = p['lugar']
    if (p.get('marca') or {}).get('masmorra') is not None: sys.exit(f"{p['nome']} já está numa descida")
    if isinstance((p.get('marca') or {}).get('caca'), dict): sys.exit(f"{p['nome']} tem uma saída ao ermo aberta: feche-a antes (`caca.py volta`)")
    ms = masmorras(E, aqui)
    if mid is None:
        if len(ms) != 1: sys.exit(f"diga a que masmorra ({', '.join(ms)})" if ms else f"{_nm(E, aqui)} não tem masmorra vizinha")
        mid = ms[0]
    elif mid not in ms: sys.exit(f'"{mid}" não é uma masmorra vizinha de {_nm(E, aqui)}' + (f" (as que há: {', '.join(ms)})" if ms else ''))
    com = list(dict.fromkeys(c for c in com if c != pid))
    for c in com:
        q = E['gente'].get(c) or sys.exit(f'não há a pessoa "{c}"')
        if q['estado'] != 'vivo' or q['lugar'] != aqui or (q.get('marca') or {}).get('masmorra') is not None or isinstance((q.get('marca') or {}).get('caca'), dict) or estado.fora(E, c):
            sys.exit(f"{q['nome']} não pode ir junto (só vai quem vive, está {_em(E, aqui)} e não tem saída nem descida aberta)")
    g = [pid] + com
    o = list(dict.fromkeys(ordem or g))
    if set(o) != set(g): sys.exit(f"a ordem de marcha tem de ter o grupo inteiro, cada um uma vez ({', '.join(g)})")
    lz = _luz_escolhe(E, g, luz, quem_luz)
    m = E['lugares'][mid]; ent = m.get('entrada')
    if ent not in E['lugares']: sys.exit(f"{m['nome']} não tem entrada (o estado está torto: `estado.py valida`)")
    estado.sem_luta(E)
    for c in g: estado.em_cena(E, c)
    cansados = [x for x in (caca.nao_inteiro(E, c) for c in com) if x]
    d = dict(masmorra=mid, sala=ent, casa=aqui, com=com, ordem=o, lances=0, blocos=0, luz=lz, fase='anda', luta=None, lutas=0, caminho=[ent], encontro=None, armadilha=None,
             dia=E['relogio']['dia'], treino=[], barulho=False, anterior=None)
    txt = f"{p['nome']} desce {_a(E, mid)}" + (f", com {_e(_pn(E, c) for c in com)}" if com else '') + (f"; a luz: {_luz_diz(E, lz)}" if lz.get('tipo') else '; sem luz')
    estado.aplica(E, EVENTO, [['pessoa', pid, 'marca.masmorra', 'poe', d]] + [['pessoa', c, 'marca.masmorra', 'poe', dict(de=pid)] for c in com], onde=ent, quem=g, texto=_txt(txt))
    ida = _longe(E, mid); antes = corpo.faixas(E['gente'][pid])
    ato.passa(E, pid, ida, EVENTO, esforco=K.ESFORCO_IDA, para=False, texto=_txt(f"{p['nome']} vai {_a(E, mid, 'a')}"), com=com)
    L = [_txt(f"{txt}. A ida: {caca._bl(ida)}.")]
    if cansados: L.append('ATENÇÃO, quem vai junto não vai inteiro: ' + '; '.join(cansados) + '.')
    caca.merenda(E, com, L)
    if E['gente'][pid]['estado'] == 'vivo' and corpo.cruzou(E['gente'][pid], antes): L.append(f"No caminho: {corpo.cruzou(E['gente'][pid], antes)}.")
    if E['gente'][pid]['estado'] != 'vivo': return _morreu(E, pid, L)
    d = json.loads(json.dumps(descida(E['gente'][pid]))); mp = _mapa_ef(E, pid, d, salas_=[ent])
    if mp: estado.aplica(E, EVENTO, mp, onde=ent, quem=g, texto=_txt(f"o grupo chega {_em(E, ent)}, {_de(E, mid)}"))
    return _entra(E, pid, ent, L)


def _a(E, mid, prep='a'):
    """'à Cripta da Cova Velha' / 'ao Poço' (a preposição com o artigo do nome)"""
    n = E['lugares'][mid]['nome']; art, _, resto = n.partition(' ')
    return ({'a': 'à ', 'o': 'ao ', 'as': 'às ', 'os': 'aos '}[art] + resto) if art in ('a', 'o', 'as', 'os') and resto else 'a ' + n


def _luz_diz(E, lz):
    if not lz or not lz.get('tipo'): return 'nenhuma'
    q = E['gente'].get(lz.get('quem')) or {}
    return f"a tocha de {q.get('nome', '?')} ({(q.get('carga') or {}).get('tocha', 0)} na carga)" if lz['tipo'] == 'tocha' else f"o feitiço luz de {q.get('nome', '?')} (Mana {estado.mana(q, True) if q else 0})"


def _sabe_luz(p): return K.LUZ_FEITICO in (p.get('feiticos') or [])


def _luz_escolhe(E, g, luz, quem):
    """a luz do grupo: a tocha de quem leva uma, o feitiço de quem o sabe, ou nada. Sem dizer: a tocha, se alguém tem; senão o feitiço; senão nada"""
    tem_t = [c for c in g if (E['gente'][c].get('carga') or {}).get('tocha', 0) >= 1]
    sabe = [c for c in g if _sabe_luz(E['gente'][c]) and estado.mana(E['gente'][c]) >= K.LUZ_MANA_BLOCO]
    if luz is None: luz = 'tocha' if tem_t else 'feitiço' if sabe else 'nada'
    if luz in ('nada', 'nenhuma', None): return dict(tipo=None, quem=None)
    if luz == 'tocha':
        q = quem or (tem_t[0] if tem_t else None)
        if q not in g or q not in tem_t: sys.exit(f"{'ninguém do grupo leva tocha' if not tem_t else _pn(E, q) + ' não leva tocha' if q in E['gente'] else 'quem leva a luz é do grupo'} (a loja vende: 1 de prata)")
        return dict(tipo='tocha', quem=q)
    if luz in ('feitiço', 'feitico'):
        q = quem or (sabe[0] if sabe else None)
        if q not in g or q not in sabe: sys.exit(f"ninguém do grupo sustenta o feitiço luz (é preciso sabê-lo e ter {K.LUZ_MANA_BLOCO} de Mana)" if not sabe else f"{_pn(E, q)} não sustenta o feitiço luz")
        return dict(tipo='feitiço', quem=q)
    sys.exit(f'luz desconhecida: "{luz}" (tocha, feitiço ou nada)')


# ---------- entrar numa sala, andar ----------
def _entra(E, pid, sid, L, escondido=False, porta_fechada=False):
    """o grupo chegou à sala: a armadilha do chão (quem vai na frente olha de passagem; não achada, dispara no primeiro da fila), e quem mora ali"""
    d = descida(E['gente'][pid])
    achou = _de_passagem(E, pid, d, sid, 'chão', L)
    if achou:
        d = json.loads(json.dumps(descida(E['gente'][pid]))); d.update(fase='armadilha', armadilha=dict(sala=sid, escondido=escondido, porta=False))
        _marca(E, pid, d, f"o grupo para {_em(E, sid)}: há armadilha achada no chão")
        L.append(f"PAROU: {_pn(E, _frente(E, pid, d))} viu {_e(_arm_nome(a) + ' ' + _arm_onde(E, sid, a) for _, a in achou)}. `masmorra.py desarmar` (a gazua), `contornar` ({_lances(K.CUSTO['contornar'])}), `disparar` de longe ({_lances(K.CUSTO['disparar'])}), ou `voltar`.")
        return dict(fase='armadilha', texto='\n'.join(_txt(x) for x in L))
    return _depois_do_chao(E, pid, sid, L, escondido, porta_fechada)


def _depois_do_chao(E, pid, sid, L, escondido=False, porta_fechada=False):
    d = descida(E['gente'][pid])
    for i, a in enumerate(_sala(E, sid).get('armadilhas') or []):
        if a.get('onde', 'chão') == 'chão' and a.get('achada') is None and a.get('feita') is None:
            morreu, extra = _dispara(E, pid, sid, i, [_frente(E, pid, d)], L, 'dispara no primeiro da fila')
            if E['gente'][pid]['estado'] != 'vivo': return _morreu(E, pid, L)
            if extra: _soma_lances(E, pid, extra)
            d = descida(E['gente'][pid])
    enc = _ve_quem(E, pid, sid, L, escondido, porta_fechada)
    R = _fecha_blocos(E, pid, L)
    if R: return R
    if enc: return _encontro(E, pid, enc, L)
    return dict(fase='anda', texto='\n'.join(_txt(x) for x in L + _aqui(E, pid)))


def _soma_lances(E, pid, n, barulho=False, mais=(), texto=None):
    d = json.loads(json.dumps(descida(E['gente'][pid]))); d['lances'] = d.get('lances', 0) + n
    if barulho: d['barulho'] = True
    _marca(E, pid, d, texto or f"o grupo gasta {_lances(n)} {_em(E, d['sala'])}", mais=mais)


def ir(E, pid, sala, escondido=False):
    """anda à sala vizinha pela passagem (1 lance; escondido 2; no escuro, sem quem veja nele, o dobro). A porta fechada abre-se ao passar (e quem está do outro lado ouve);
    a trancada e a emperrada pedem `abrir`. A armadilha da porta e a do chão, quem vai na frente vê de passagem; quem mora na sala nova vê o grupo, ou é visto primeiro."""
    p, d = _minha(E, pid, fases=('anda', 'armadilha')); estado.sem_luta(E); sid = d['sala']
    if sala not in E['lugares'] or sala not in _viz(E, sid): sys.exit(f'"{sala}" não é uma sala vizinha {_de(E, sid)} (as passagens daqui: ' + (', '.join(_passagem_diz(E, pid, d, sid, v) for v in _viz(E, sid)) or 'nenhuma') + ')')
    if d['fase'] == 'armadilha' and sala != d.get('anterior'): sys.exit(f"há armadilha achada {_em(E, sid)}: `masmorra.py desarmar`, `contornar` ou `disparar` antes de seguir (ou volte por onde veio: `ir {d.get('anterior')}`)")
    pt = porta(E, sid, sala); g = _grupo(E, pid, d)
    if pt and pt.get('miudos') and any(estado.corpo_de(E['gente'][c]) != 'miúdo' for c in g): sys.exit(f"{_cap(_porta_diz(E, sid, sala, pid))} só dá para gente miúda")
    if pt and pt.get('estado') in ('trancada', 'emperrada'): sys.exit(f"{_cap(_porta_diz(E, sid, sala, pid))} está {pt['estado']}: `masmorra.py abrir {sala} " + ('gazua|chave|força' if pt['estado'] == 'trancada' else 'força') + '`')
    L = []; fechada = bool(pt and pt.get('estado') == 'fechada')
    if fechada:
        ach = _arm_porta(E, sid, sala)
        if ach is not None and ach[1].get('achada') is None:
            novas = _de_passagem(E, pid, d, sid, f'porta:{sala}', L)
            if novas: return dict(fase='anda', texto='\n'.join(_txt(x) for x in L + [f"PAROU: há {_arm_nome(novas[0][1])} {_em_nome(_porta_diz(E, sid, sala, pid))}. `masmorra.py desarmar`, `disparar` (de longe), ou abra assim mesmo (ela dispara em quem abre)."]))
    custo = (K.CUSTO['escondido'] if escondido else K.CUSTO['ir']) * (2 if not _ve(E, pid, d) else 1)
    d2 = json.loads(json.dumps(d)); d2.update(sala=sala, fase='anda', armadilha=None, encontro=None, anterior=sid, lances=d.get('lances', 0) + custo)
    cam = list(d['caminho']); d2['caminho'] = cam[:cam.index(sala) + 1] if sala in cam else cam + [sala]
    if escondido: _treina(d2, g)
    ef = _mapa_ef(E, pid, d2, salas_=[sala])
    if fechada: ef.append(['lugar', d['masmorra'], f'portas.{_pk(sid, sala)}', 'poe', dict(pt, estado='aberta')])
    _marca(E, pid, d2, f"o grupo passa {_a_nome(_nm(E, sala))}" + (', escondido' if escondido else '') + (' (abre a porta)' if fechada else ''), mais=ef)
    if fechada:
        a = _arm_porta(E, sid, sala)
        if a is not None and a[1].get('feita') is None:
            _dispara(E, pid, sid, a[0], [_frente(E, pid, d2)], L, 'dispara em quem abre a porta')
            if E['gente'][pid]['estado'] != 'vivo': return _morreu(E, pid, L)
    L.insert(0, _txt(f"O grupo passa {_a_nome(_nm(E, sala))} ({_lances(custo)}{', escondido' if escondido else ''}{'; no escuro, o dobro' if not _ve(E, pid, d) else ''}). {_cap(_sala(E, sala).get('sobre') or '')}".strip()))
    return _entra(E, pid, sala, L, escondido=escondido, porta_fechada=fechada)


def _arm_porta(E, sid, outra):
    """a armadilha não resolvida da porta para `outra`, nesta sala ou na outra (a da porta mora na lista da sala de onde se abre): (índice, armadilha, sala) ou None"""
    for s, o in ((sid, outra), (outra, sid)):
        for i, a in enumerate(_sala(E, s).get('armadilhas') or []):
            if a.get('onde') == f'porta:{o}' and a.get('feita') is None: return (i, a, s) if s == sid else None
    return None


def _vistas(E, pid, d):
    """as salas que o grupo viu desta masmorra (o mapa de quem comanda)"""
    return set(((E['gente'][pid].get('marca') or {}).get('mapa') or {}).get(d['masmorra'], {}).get('salas') or []) | set(d.get('caminho') or [])


def _porta_diz(E, sid, v, pid=None):
    """a porta (ou a passagem) da sala sid para v, como o grupo a conhece: "a porta de ferro", "a porta de madeira para o ossário" (o nome da sala só se o grupo já a viu)"""
    pt = porta(E, sid, v); d = descida(E['gente'][pid]) if pid else None
    para = f" para {_nm(E, v)}" if d and v in _vistas(E, pid, d) else f" ({v})"
    return (f"a porta de {pt.get('material', 'madeira')}" if pt else 'a passagem') + para


def _passagem_diz(E, pid, d, sid, v):
    """a passagem para v, como o grupo a conhece: o nome da sala, se já a viu; senão, só a passagem (e a porta)"""
    pt = porta(E, sid, v)
    return f"{v} ({_nm(E, v) if v in _vistas(E, pid, d) else 'uma passagem'}" + (f", porta {pt['estado']}" if pt else '') + ')'


def _aqui(E, pid):
    """o que se vê na sala, numa linha ou duas (o que há para pegar, as passagens)"""
    d = descida(E['gente'][pid])
    if not d: return []
    sid = d['sala']; l = _sala(E, sid); L = []
    gd = l.get('guardado')
    if isinstance(gd, dict) and not gd.get('aberto'): L.append(f"Aqui há {gd['nome']}, fechad{'a' if gd['nome'].startswith('a ') else 'o'}" + (' (com fechadura)' if gd.get('fechadura') is not None else '') + f": `masmorra.py abrir guardado`.")
    else:
        tem = _tesouro(E, sid)
        if tem: L.append(f"Aqui há o que pegar: {tem} (`masmorra.py pegar`).")
    mortos = [it for it in E['itens']['itens'].values() if it.get('onde') == sid and estado.de_morto(it)]
    if mortos: L.append(f"No chão, junto de um corpo: {_e(it['nome'] for it in mortos)} (não muda de mão sozinho).")
    viz = _viz(E, sid)
    L.append('Passagens: ' + (', '.join(_passagem_diz(E, pid, d, sid, v) for v in viz) or 'nenhuma') + '.')
    ach = _achadas(E, sid)
    if ach: L.append('Armadilhas achadas aqui: ' + ' · '.join(f"{k}) {_arm_nome(a)} {_arm_onde(E, sid, a)}" for k, _, a in ach) + '.')
    return [_txt(x) for x in L]


def _tesouro(E, sid):
    """o que está à vista para pegar: a prata e os bens do estoque, as peças guardadas e as soltas (não as de um morto)"""
    est = {b: q for b, q in _num(_sala(E, sid).get('estoque')).items() if q > 0}
    its = [it for it in E['itens']['itens'].values() if it.get('onde') == sid and not it.get('dono') and not estado.de_morto(it)]
    return _e([f"{int(q)} de {'prata' if b == 'prata' else estado.nome_bem(b)}" for b, q in est.items()] + [it['nome'] for it in its])


# ---------- olhar e mexer na sala ----------
def escutar(E, pid, sala, quem=None):
    """escuta à porta da passagem (1 lance; rolagem oculta): silêncio, algo se mexe, vozes de poucos ou de muitos. Nunca o número."""
    p, d = _minha(E, pid, fases=('anda',)); estado.sem_luta(E); sid = d['sala']; g = _grupo(E, pid, d); q = quem or _frente(E, pid, d)
    if q not in g: sys.exit(f'"{q}" não está no grupo')
    if sala not in _viz(E, sid): sys.exit(f'"{sala}" não é uma sala vizinha {_de(E, sid)}')
    pt = porta(E, sid, sala); mat = (pt or {}).get('material', 'madeira'); n = bichos_de(E, sala); ch = _chefe_vivo(E, sala); dr = _dragao(E, sala)
    mortos = (n or ch) and not dr and all(_sem_vida(e) for e in n)
    contra = TMH.ESCUTAR.get(mat, TMH.ESCUTAR['madeira']) + (TMH.ESCUTAR.get('mortos', 0) if mortos else 0)
    r = _manha().testa(E, q, 'escutar', contra=contra, o_que=f"escutar {_a_nome(_porta_diz(E, sid, sala, pid))}", oculto=True)
    tot = sum(n.values()) + bool(ch) + bool(dr)
    if not r['passou'] or not tot: ouve = 'silêncio'
    elif mortos: ouve = 'algo se mexe do outro lado, devagar, sem fôlego'
    else: ouve = f"vozes ou bichos do outro lado, de {K.ESCUTA[1] if tot <= K.ESCUTA[0] else K.ESCUTA[2]}"
    d['lances'] = d.get('lances', 0) + K.CUSTO['escutar']; _treina(d, [q])
    _marca(E, pid, d, f"{_pn(E, q)} escuta {_a_nome(_porta_diz(E, sid, sala, pid))}", mais=list(r.get('efeitos') or []))
    L = [teste.diz(E, r), f"{_pn(E, q)} escuta ({_lances(K.CUSTO['escutar'])}): {ouve}."]
    R = _fecha_blocos(E, pid, L)
    return R or dict(fase='anda', texto='\n'.join(_txt(x) for x in L))


def procurar(E, pid, quem=None):
    """procura na sala (2 lances): cada armadilha não achada e cada passagem escondida, uma rolagem oculta. Achada a passagem, ela vira passagem como as outras."""
    p, d = _minha(E, pid, fases=('anda',)); estado.sem_luta(E); sid = d['sala']; g = _grupo(E, pid, d); mh = _manha()
    q = quem or max(g, key=lambda c: (E['gente'][c]['atributos']['Percepção'] // 10 + mh.grau(E['gente'][c]), c == pid))
    if q not in g: sys.exit(f'"{q}" não está no grupo')
    if not _ve(E, pid, d, q): sys.exit(f"no escuro, {_pn(E, q)} não procura nada (é preciso luz, ou ver no escuro)")
    l = _sala(E, sid); arms = json.loads(json.dumps(l.get('armadilhas') or [])); segs = json.loads(json.dumps(l.get('segredos') or [])); L = []; achou = []; ef = []
    for i, a in enumerate(arms):
        if a.get('achada') is not None or a.get('feita') is not None: continue
        r = mh.testa(E, q, 'achar', cat=a['cat'], o_que=f"procurar {_em(E, sid)}", oculto=True, pedra=a['tipo'] == 'pedra'); L.append(teste.diz(E, r)); ef += list(r.get('efeitos') or [])
        if r['passou']: arms[i]['achada'] = E['relogio']['dia']; achou.append(f"{_arm_nome(a)} {_arm_onde(E, sid, a)}")
    novas = []
    for x in list(segs):
        r = mh.testa(E, q, 'achar', cat=x['cat'], o_que=f"procurar {_em(E, sid)}", oculto=True, pedra=True); L.append(teste.diz(E, r)); ef += list(r.get('efeitos') or [])
        if r['passou'] and x.get('para') in E['lugares']: segs.remove(x); novas.append(x['para']); achou.append(f"uma passagem escondida ({x['para']})")
    if arms != (l.get('armadilhas') or []): ef.append(['lugar', sid, 'armadilhas', 'poe', arms])
    if segs != (l.get('segredos') or []): ef.append(['lugar', sid, 'segredos', 'poe', segs])
    for o in novas:
        ef.append(['lugar', sid, 'vizinhos', 'poe', list(dict.fromkeys(_viz(E, sid) + [o]))]); ef.append(['lugar', o, 'vizinhos', 'poe', list(dict.fromkeys(_viz(E, o) + [sid]))])
    d['lances'] = d.get('lances', 0) + K.CUSTO['procurar']; _treina(d, [q])
    ef += _mapa_ef(E, pid, d, salas_=novas, armadilhas=[f"{sid}#{i}" for i, a in enumerate(arms) if a.get('achada') is not None])
    _marca(E, pid, d, f"{_pn(E, q)} procura {_em(E, sid)}" + (f": acha {_e(achou)}" if achou else ''), mais=ef)
    L.append(f"{_pn(E, q)} procura ({_lances(K.CUSTO['procurar'])}): " + (f"ACHA {_e(achou)}." if achou else 'não acha nada.'))
    R = _fecha_blocos(E, pid, L)
    return R or dict(fase='anda', texto='\n'.join(_txt(x) for x in L + _aqui(E, pid)))


def _chave_de(E, g, alvo):
    for it in E['itens']['itens'].values():
        if it.get('tipo') == 'chave' and it.get('abre') == alvo and it.get('dono') in g: return it
    return None


def abrir(E, pid, alvo, como=None, quem=None):
    """abre a porta da passagem para a sala ALVO, ou o que a sala guarda (alvo=guardado): a chave (sem teste), a gazua (a conta da fechadura) ou a força (arrombar:
    soma 1 no alarme). 1 lance por tentativa. A armadilha da porta (ou do guardado) que não foi desarmada dispara em quem abre."""
    p, d = _minha(E, pid, fases=('anda',)); estado.sem_luta(E); sid = d['sala']; g = _grupo(E, pid, d); mh = _manha(); mid = d['masmorra']
    q = quem or _frente(E, pid, d)
    if q not in g: sys.exit(f'"{q}" não está no grupo')
    if alvo == 'guardado':
        gd = _sala(E, sid).get('guardado')
        if not isinstance(gd, dict): sys.exit(f"{_cap(_nm(E, sid))} não guarda nada que se abra")
        if gd.get('aberto'): sys.exit(f"{_cap(gd['nome'])} já está abert{'a' if gd['nome'].startswith('a ') else 'o'}")
        if ocupada(E, sid): sys.exit("há quem more aqui, de pé: não se abre nada com eles olhando (a luta primeiro)")
        fech, cat, chave_alvo, nome = gd.get('fechadura'), gd.get('fechadura') or 0, sid, gd['nome']
        estado_p = 'trancada' if fech is not None else 'fechada'
    else:
        if alvo not in _viz(E, sid): sys.exit(f'"{alvo}" não é uma sala vizinha {_de(E, sid)}, nem "guardado"')
        pt = porta(E, sid, alvo)
        if not pt or pt.get('estado') in ('aberta', 'arrombada'): sys.exit(f"{_cap(_porta_diz(E, sid, alvo, pid))} não tem porta fechada: `masmorra.py ir {alvo}`")
        fech, cat, chave_alvo, nome, estado_p = pt.get('fechadura'), pt.get('cat', 0), _pk(sid, alvo), _porta_diz(E, sid, alvo, pid), pt['estado']
        ach = _arm_porta(E, sid, alvo)
        if ach is not None and ach[1].get('achada') is None:
            L0 = []; novas = _de_passagem(E, pid, d, sid, f'porta:{alvo}', L0)
            if novas: return dict(fase='anda', texto='\n'.join(_txt(x) for x in L0 + [f"PAROU: há {_arm_nome(novas[0][1])} {_em_nome(_porta_diz(E, sid, alvo, pid))}. `masmorra.py desarmar`, `disparar` (de longe), ou abra assim mesmo (ela dispara em quem abre)."]))
            d = json.loads(json.dumps(descida(E['gente'][pid])))
    ch = _chave_de(E, g, chave_alvo)
    if como is None: como = 'chave' if ch else 'gazua' if estado_p == 'trancada' and mh.gazua_de(E, q) else 'grampo' if estado_p == 'trancada' else 'força' if estado_p == 'emperrada' else 'mão'
    if estado_p == 'fechada': como = 'mão'
    if estado_p == 'emperrada' and como != 'força': sys.exit(f"{nome} está emperrada: só a força a abre (`masmorra.py abrir {alvo} força`)")
    if como == 'chave' and not ch: sys.exit(f"ninguém do grupo leva a chave d{'e' if alvo == 'guardado' else 'a porta'} ({nome})")
    if como == 'gazua' and not _ve(E, pid, d, q): sys.exit(f"no escuro, {_pn(E, q)} não abre fechadura (é preciso luz, ou ver no escuro; arrombar, sim)")
    if como == 'gazua' and not mh.gazua_de(E, q): sys.exit(f"{_pn(E, q)} não leva gazua: com o grampo (a ponta da faca) a conta é um degrau abaixo do Comum (`masmorra.py abrir {alvo} grampo`), ou a força")
    if como == 'grampo' and not _ve(E, pid, d, q): sys.exit(f"no escuro, {_pn(E, q)} não abre fechadura (é preciso luz, ou ver no escuro; arrombar, sim)")
    if como not in ('chave', 'gazua', 'grampo', 'força', 'mão'): sys.exit(f'abre-se com: chave, gazua, grampo ou força (veio "{como}")')
    L = []; ef = []; abriu = False; barulho = False
    if como in ('chave', 'mão'): abriu = True; L.append(f"{_pn(E, q)} abre {nome}" + (f" com {ch['nome']}" if como == 'chave' else '') + '.')
    elif como in ('gazua', 'grampo'):
        r = mh.testa(E, q, 'gazua', cat=cat, o_que=f"abrir a fechadura d{'e' if alvo == 'guardado' else 'a porta'} ({nome})"); L.append(teste.diz(E, r)); ef += list(r.get('efeitos') or []); _treina(d, [q])
        abriu = r['passou']
        if r.get('falhou_feio') and r.get('ferramenta'): ef.append(['item', r['ferramenta'], 'dur', 'soma', -1]); L.append('A gazua entorta (perde 1).')
        if abriu: ef += list(mh.feito(E, q, cat) or [])
    else:
        r = mh.testa(E, q, 'arrombar', cat=cat, o_que=f"arrombar {nome}"); L.append(teste.diz(E, r)); ef += list(r.get('efeitos') or []) + _alarme_ef(E, mid, K.ALARME['arrombar']); barulho = True
        abriu = r['passou']
        if r.get('falhou_feio') and r.get('ferramenta'): ef.append(['item', r['ferramenta'], 'dur', 'soma', -1]); L.append('A arma de arrombar sente o golpe (perde 1).')
    if abriu:
        if alvo == 'guardado': ef.append(['lugar', sid, 'guardado', 'poe', dict(_sala(E, sid)['guardado'], aberto=True)])
        else: ef.append(['lugar', mid, f'portas.{chave_alvo}', 'poe', dict(porta(E, sid, alvo), estado='arrombada' if como == 'força' else 'aberta')])
    elif como != 'força': L.append(f"{_pn(E, q)} não abre {nome}.")
    else: L.append(f"{_cap(nome)} aguenta.")
    d['lances'] = d.get('lances', 0) + K.CUSTO['tenta']
    if barulho: d['barulho'] = True
    _marca(E, pid, d, f"{_pn(E, q)} " + (f"abre {nome}" if abriu else f"tenta abrir {nome}") + {'chave': ' com a chave', 'gazua': ' com a gazua', 'grampo': ' com o grampo', 'força': ' na força', 'mão': ''}[como], mais=ef)
    if abriu:
        a = None
        if alvo == 'guardado':
            a = next(((i, x) for i, x in enumerate(_sala(E, sid).get('armadilhas') or []) if x.get('onde') == 'guardado' and x.get('feita') is None), None)
        else:
            x = _arm_porta(E, sid, alvo); a = (x[0], x[1]) if x else None
        if a: _dispara(E, pid, sid, a[0], [q], L, f"dispara em quem abre")
        if E['gente'][pid]['estado'] != 'vivo': return _morreu(E, pid, L)
        if alvo == 'guardado':
            tem = _tesouro(E, sid); L.append(f"Dentro: {tem}." if tem else 'Dentro não há nada.')
    R = _fecha_blocos(E, pid, L)
    return R or dict(fase='anda', texto='\n'.join(_txt(x) for x in L))


def _escolhe_arm(E, pid, d, n, onde_ok=None):
    sid = (d.get('armadilha') or {}).get('sala') or d['sala']; ach = _achadas(E, sid)
    if onde_ok: ach = [x for x in ach if onde_ok(x[2])]
    if not ach: sys.exit(f"não há armadilha achada {_em(E, sid)} para isso (procurar acha: `masmorra.py procurar`)")
    if n is None:
        if len(ach) > 1: sys.exit('diga qual: ' + ' · '.join(f"{k}) {_arm_nome(a)} {_arm_onde(E, sid, a)}" for k, _, a in ach))
        return sid, ach[0][1], ach[0][2]
    x = next((x for x in ach if x[0] == int(n)), None) or sys.exit('não há essa armadilha: ' + ' · '.join(f"{k}) {_arm_nome(a)} {_arm_onde(E, sid, a)}" for k, _, a in ach))
    return sid, x[1], x[2]


def _resolve(E, pid, L):
    """a armadilha do chão que parou o grupo foi resolvida: segue a entrada na sala"""
    d = descida(E['gente'][pid])
    feitas = set((d.get('armadilha') or {}).get('contornadas') or [])
    if d.get('fase') == 'armadilha' and not any(a.get('onde', 'chão') == 'chão' and a.get('feita') is None and a.get('achada') is not None and i not in feitas for i, a in enumerate(_sala(E, d['sala']).get('armadilhas') or [])):
        info = d.get('armadilha') or {}; d2 = json.loads(json.dumps(d)); d2.update(fase='anda', armadilha=None)
        _marca(E, pid, d2, f"o grupo segue {_em(E, d['sala'])}")
        return _depois_do_chao(E, pid, d['sala'], L, info.get('escondido', False), info.get('porta', False))
    R = _fecha_blocos(E, pid, L)
    return R or dict(fase=d.get('fase', 'anda'), texto='\n'.join(_txt(x) for x in L + _aqui(E, pid)))


def desarmar(E, pid, n=None, quem=None):
    """desarma a armadilha achada (a conta da gazua contra a categoria dela; 1 lance). Falhar por 5 ou mais a dispara em quem desarmava."""
    p, d = _minha(E, pid, fases=('anda', 'armadilha')); estado.sem_luta(E); g = _grupo(E, pid, d); mh = _manha()
    sid, i, a = _escolhe_arm(E, pid, d, n)
    q = quem or max(g, key=lambda c: (E['gente'][c]['atributos']['Agilidade'] // 10 + mh.grau(E['gente'][c]) + (mh.gazua_de(E, c) or {}).get('cat', -1) * 8, c == pid))
    if q not in g: sys.exit(f'"{q}" não está no grupo')
    if not _ve(E, pid, d, q): sys.exit(f"no escuro, {_pn(E, q)} não desarma nada (é preciso luz, ou ver no escuro)")
    r = mh.testa(E, q, 'desarmar', cat=a['cat'], o_que=f"desarmar {_arm_nome(a)} {_arm_onde(E, sid, a)}"); L = [teste.diz(E, r)]; ef = list(r.get('efeitos') or [])
    arms = json.loads(json.dumps(_sala(E, sid).get('armadilhas') or []))
    if r['passou']: arms[i]['feita'] = 'desarmada'; ef += [['lugar', sid, 'armadilhas', 'poe', arms]] + list(mh.feito(E, q, a['cat']) or []); L.append(f"{_pn(E, q)} desarma {_arm_nome(a)}.")
    if r.get('falhou_feio') and r.get('ferramenta'): ef.append(['item', r['ferramenta'], 'dur', 'soma', -1])
    d['lances'] = d.get('lances', 0) + K.CUSTO['tenta']; _treina(d, [q])
    _marca(E, pid, d, f"{_pn(E, q)} " + (f"desarma {_arm_nome(a)}" if r['passou'] else f"tenta desarmar {_arm_nome(a)}") + f" {_em(E, sid)}", mais=ef)
    if not r['passou']:
        if r.get('falhou_feio'):
            _dispara(E, pid, sid, i, [q], L, 'dispara na mão de quem a desarmava')
            if E['gente'][pid]['estado'] != 'vivo': return _morreu(E, pid, L)
        else: L.append(f"{_pn(E, q)} não consegue, e ela segue armada.")
    return _resolve(E, pid, L)


def contornar(E, pid, n=None):
    """passa ao largo da armadilha achada do chão (1 lance, sem teste). O fosso num corredor de um pede pular: Agilidade contra 20 + 6 por categoria, cada um."""
    p, d = _minha(E, pid, fases=('anda', 'armadilha')); estado.sem_luta(E); g = _grupo(E, pid, d)
    sid, i, a = _escolhe_arm(E, pid, d, n, lambda a: a.get('onde', 'chão') == 'chão')
    L = []; caiu = []
    if a['tipo'] == 'fosso' and _sala(E, sid).get('largura') == 1:
        for c in g:
            r = teste.rola(E, f"pular o fosso {_em(E, sid)}", 'Agilidade', K.ESQUIVA[0] + K.ESQUIVA[1] * a['cat'], quem=c); L.append(teste.diz(E, r))
            if not r['passou']: caiu.append(c)
    d['lances'] = d.get('lances', 0) + K.CUSTO['contornar']
    if isinstance(d.get('armadilha'), dict): d['armadilha']['contornadas'] = list(dict.fromkeys(list(d['armadilha'].get('contornadas') or []) + [i]))
    _marca(E, pid, d, f"o grupo contorna {_arm_nome(a)} {_em(E, sid)}")
    if caiu:
        _dispara(E, pid, sid, i, caiu, L, 'pega quem errou o pulo')
        if E['gente'][pid]['estado'] != 'vivo': return _morreu(E, pid, L)
    L.append(f"O grupo contorna {_arm_nome(a)} ({_lances(K.CUSTO['contornar'])}).")
    return _resolve(E, pid, L)


def disparar(E, pid, n=None):
    """dispara de longe a armadilha achada do chão ou da porta (1 lance; ninguém se fere, e faz o barulho dela)"""
    p, d = _minha(E, pid, fases=('anda', 'armadilha')); estado.sem_luta(E)
    sid, i, a = _escolhe_arm(E, pid, d, n, lambda a: a.get('onde', 'chão') != 'guardado')
    arms = json.loads(json.dumps(_sala(E, sid).get('armadilhas') or [])); arms[i]['feita'] = 'disparada'; A = K.ARMADILHAS[a['tipo']]
    d['lances'] = d.get('lances', 0) + K.CUSTO['disparar']
    if A.get('barulho'): d['barulho'] = True
    _marca(E, pid, d, f"o grupo dispara de longe {_arm_nome(a)} {_em(E, sid)}", mais=[['lugar', sid, 'armadilhas', 'poe', arms]] + _alarme_ef(E, d['masmorra'], A.get('barulho', 0)))
    return _resolve(E, pid, [f"O grupo dispara {_arm_nome(a)} de longe ({_lances(K.CUSTO['disparar'])})" + ('; o barulho sobe o alarme.' if A.get('barulho') else '; ninguém se fere.')])


# ---------- o encontro: atacar, esperar, recuar ----------
def atacar(E, pid, inicio=None, passagem=False):
    """ataca quem está à frente: monta o cenário e abre a luta (a do ato.py luta)"""
    p, d = _minha(E, pid, fases=('encontro',)); enc = d['encontro']
    if enc['viu'] == 'grupo':
        inis = ['perto', 'colado'] + (['longe'] if _sala(E, enc['sala']).get('largura') is None else [])
        ini = inicio or enc.get('inicio') or 'perto'
        if ini not in inis: sys.exit(f'esta luta começa {caca._ou(inis)} (veio "{ini}")')
        surp = 'B'
    else:
        ini = enc.get('inicio') or 'perto'; surp = enc.get('surpresa')
        if inicio and inicio != ini: sys.exit(f"eles viram o grupo: a luta começa {ini}")
        if passagem and surp == 'A': sys.exit('o grupo foi pego desprevenido: não escolhe onde a luta começa')
    onde = enc.get('onde', enc['sala'])
    if passagem:
        ant = d.get('anterior')
        if not (ant in E['lugares'] and E['lugares'][ant].get('largura')): sys.exit('não há passagem estreita atrás do grupo para esperar neles')
        onde = ant; ini = 'perto'
    return _luta_abre(E, pid, ini, surp, onde, [])


def _luta_abre(E, pid, ini, surp, onde, L):
    """monta o cenário (o grupo na ordem de marcha; o outro lado: o dragão, o chefe e quem mora na sala, da contagem real) e chama o ato.luta_nova"""
    import criaturas
    p = E['gente'][pid]; d = json.loads(json.dumps(descida(p))); enc = dict(d['encontro']); sid = enc['sala']; mid = d['masmorra']
    if not ocupada(E, sid):
        d.update(fase='anda', encontro=None); _marca(E, pid, d, 'não há mais ninguém ali'); return dict(fase='anda', texto='\n'.join(L + ['Não há mais ninguém ali.']))
    k = d.get('lutas', 0) + 1; B = []; chefe_nome = None; dragao_nome = None
    dr = _dragao(E, sid); D = _dragoes()
    if dr and D:
        mt = D.monta(E, sid)
        if mt: B.append(mt[0]); dragao_nome = mt[0].get('nome')
    chefe_p, bs = _bando(E, pid, sid, k, para_luta=True)
    if chefe_p:
        B.append(chefe_p if chefe_p.get('bicho') and _chefe_vivo(E, sid)['qual'] in TB.ESPECIES else criaturas.no_cenario(chefe_p)); chefe_nome = chefe_p['nome']
        import tabelas_criaturas as TC
        gq = (TC.CHEFES.get(_chefe_vivo(E, sid)['qual']) or {}).get('guarda', 0)
        for x in bs[:gq]: x['guarda'] = chefe_nome; x['linha'] = 'trás'
    for b in bs:
        esp = (b.get('povo') or {}).get('especie') if isinstance(b.get('povo'), dict) else (b.get('bicho') or {}).get('especie') if isinstance(b.get('bicho'), dict) else None
        B.append(b if esp in TB.ESPECIES else criaturas.no_cenario(b))
    A = [dict(id=x, **({'controla': True} if x == pid else {}), **({'linha': 'trás'} if _de_tras(E, x) else {})) for x in _ordem(E, pid, d)]
    lugar = {}; larg = E['lugares'][onde].get('largura')
    if larg: lugar['largura'] = larg
    if dr and E['lugares'][mid].get('molde') == 'covil': lugar['sem_saida'] = 'B'          # no covil o dragão luta até morrer (E3 a)
    luz = _luz_de(E, pid, d) or bool(_sala(E, onde).get('acesa'))
    pasta = os.path.join(estado.pasta(), 'lutas'); os.makedirs(pasta, exist_ok=True); base = os.path.join(pasta, f"masm_{pid}_d{E['relogio']['dia']}b{E['relogio']['bloco']}_{k}")
    json.dump(dict(inicio=ini, lugar=lugar, surpresa=surp, tempo=[] if luz else ['escuro'], luz=luz, ermo=sid, A=A, B=B), open(base + '_cenario.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    quadro = ato.luta_nova(E, base + '_cenario.json', base + '_luta.json')
    enc.update(inicio=ini, surpresa=surp, onde=onde, chefe_nome=chefe_nome, dragao_nome=dragao_nome)
    d.update(fase='luta', luta=estado.arq_guarda(base + '_luta.json'), lutas=k, encontro=enc)
    quem = _diz_bando(enc['n'], enc.get('chefe') and {'qual': enc['chefe']}, dr)
    _marca(E, pid, d, f"o grupo luta com {quem} {_em(E, onde)} (começa {ini}" + ({'A': ', e o grupo perde o primeiro turno', 'B': ', eles surpreendidos'}.get(surp, '') or '') + ')')
    L = L + [_txt(f"A LUTA ABRE {_em(E, onde)} ({_largura_diz(E['lugares'][onde])}{'' if luz else ', no ESCURO'}), começando {ini}" + ({'A': ': o grupo perde o primeiro turno', 'B': ': eles foram surpreendidos (perdem o primeiro turno)'}.get(surp, '') or '') + '.'),
             quadro, f'Siga com `masmorra.py luta "{p["nome"]}: atacar"` (ou `ato.py luta roda {d["luta"]} "{p["nome"]}: ordem"`); acabada a luta, as contas saem sozinhas.']
    return dict(fase='luta', luta=estado.arq_abre(d['luta']), encontro=enc, texto='\n'.join(L))


def esperar(E, pid):
    """espera escondido (1 lance): a sala segue como está, e o grupo escolhe de novo"""
    p, d = _minha(E, pid, fases=('encontro',)); enc = d['encontro']
    if enc['viu'] != 'grupo': sys.exit('eles viram o grupo: não há como esperar escondido (`masmorra.py atacar` ou `recuar`)')
    d['lances'] = d.get('lances', 0) + K.CUSTO['esperar']
    _marca(E, pid, d, f"o grupo espera, escondido, {_em(E, enc['sala'])}")
    L = [f"O grupo espera, escondido ({_lances(K.CUSTO['esperar'])})."]
    R = _fecha_blocos(E, pid, L)
    return R or dict(fase='encontro', texto='\n'.join(L + le_encontro(E, pid)))


def recuar(E, pid):
    """volta à sala de onde veio. Sem ser visto, ninguém vem atrás. Visto: as feras e o povo vêm atrás pela índole da espécie (o morto lento não sai da sala dele):
    quem vem chega na sala de trás, e a luta abre ali"""
    p, d = _minha(E, pid, fases=('encontro', 'armadilha')); enc = d.get('encontro') or {}; sid = d['sala']; ant = d.get('anterior')
    if ant not in E['lugares']: sys.exit('não há sala atrás do grupo (é a entrada: `masmorra.py sair`)')
    d2 = json.loads(json.dumps(d)); d2.update(sala=ant, fase='anda', encontro=None, armadilha=None, lances=d.get('lances', 0) + K.CUSTO['ir'])
    cam = list(d['caminho']); d2['caminho'] = cam[:cam.index(ant) + 1] if ant in cam else [ant]
    d2['anterior'] = d2['caminho'][-2] if len(d2['caminho']) > 1 else None
    _marca(E, pid, d2, f"o grupo recua {_a_nome(_nm(E, ant))}")
    L = [_txt(f"O grupo recua {_a_nome(_nm(E, ant))} ({_lances(K.CUSTO['ir'])}).")]
    if enc and enc.get('viu') == 'eles':
        R = _persegue(E, pid, enc, ant, L)
        if R: return R
    R = _fecha_blocos(E, pid, L)
    return R or dict(fase='anda', texto='\n'.join(_txt(x) for x in L + _aqui(E, pid)))


def _persegue(E, pid, enc, para, L):
    """quem viu o grupo ir embora vem atrás? Pela índole da espécie (a tabela da caça); o morto lento não sai da sala dele"""
    sid = enc['sala']; n = bichos_de(E, sid)
    andam = {e: q for e, q in n.items() if not _sem_vida(e) or e in ('espectro', 'alma-penada')}
    if not andam or not ocupada(E, sid): return None
    esp = max(andam, key=lambda e: andam[e]); ind = caca.K.indole(esp)[1]
    rs = estado.sorte(E, f"masmorra|{pid}|persegue|{sid}|{descida(E['gente'][pid]).get('lutas', 0)}")
    if rs.random() >= min(1.0, ind + caca.K.INVESTE_FUGA): L.append(f"{_cap(_diz_bando(n))} não {_s(sum(n.values()), 'vem', 'vêm')} atrás."); return None
    L.append(f"{_cap(_diz_bando(andam))} {_s(sum(andam.values()), 'VEM', 'VÊM')} ATRÁS.")
    e2 = dict(sala=sid, onde=para, n=n, chefe=None, dragao=None, viu='eles', surpresa=None, inicio=K.INICIO['vem'], ouviu=False, vem=True)
    return _encontro(E, pid, e2, L)


def luta_roda(E, pid, ordens=()):
    """roda a luta aberta da descida até a próxima parada (é o ato.luta_roda); acabada, faz as contas"""
    p, d = _minha(E, pid, vivo=False)
    if d.get('fase') != 'luta': sys.exit(f"{p['nome']} não tem luta aberta na descida")
    if _le_luta(d)['fim']: return acerta(E, pid)
    out = ato.luta_roda(E, estado.arq_abre(d['luta']), list(ordens))
    if _le_luta(d)['fim']: R = acerta(E, pid); R['texto'] = out + '\n\n' + R['texto']; return R
    return dict(fase='luta', luta=estado.arq_abre(d['luta']), texto=out)


def _le_luta(d):
    a = estado.arq_abre(d['luta'])
    if not os.path.exists(a): sys.exit(f"o arquivo da luta desta descida não está em {a}: sem ele não há contas. `masmorra.py larga \"por quê\"` fecha a descida sem elas (SÓ O MESTRE)")
    return json.load(open(a, encoding='utf-8'))


def _esp_de(f):
    x = f.get('povo') if isinstance(f.get('povo'), str) else f.get('bicho')
    return x if isinstance(x, str) and estado.especie(x) else None


def acerta(E, pid):
    """A LUTA ACABOU: as contas, num evento só. Quem morreu sai da contagem da sala (o caído é rematado por quem ficou com o campo; o povo rendido sai como o morto);
    o despojo de cada morto, na categoria dele, reparte-se entre quem lutou até o fim; o chefe morto deixa a sala (e o núcleo, do Épico para cima); o chefe do fundo
    morto pela primeira vez é a primeira limpeza. A luta soma no alarme. Quem perdeu o campo recua à sala de trás (e quem viu pode vir atrás)."""
    import criaturas, itens
    p, d = _minha(E, pid, vivo=False)
    if d.get('fase') != 'luta': sys.exit(f"{p['nome']} não tem luta para acertar")
    S = _le_luta(d)
    if not S['fim']: sys.exit(f'a luta ainda não acabou: siga com `masmorra.py luta "{p["nome"]}: atacar"`')
    if any(l['arq'] == d['luta'] and not l['fim'] for l in E['turno']['lutas']): ato.luta_fecha(E, S, estado.arq_abre(d['luta']))
    p = E['gente'][pid]; enc = d['encontro']; sid = enc['sala']; onde = enc.get('onde', sid); mid = d['masmorra']; campo = S['fim'] == 'A'
    chn, drn = enc.get('chefe_nome'), enc.get('dragao_nome')
    bs = [f for f in S['L'] if f['lado'] == 'B' and f['nome'] not in (chn, drn) and ', morto que anda' not in f['nome']]
    sai = lambda f: f['estado'] == 'morto' or (campo and f['estado'] == 'caido') or (campo and f['estado'] == 'rendido' and f.get('povo'))
    ficaram = [f['id'] for f in sorted((f for f in S['L'] if f['lado'] == 'A' and f['estado'] in FICOU and E['gente'].get(f.get('id'), {}).get('estado') == 'vivo'), key=lambda f: f['id'] != pid)] if campo else []
    leva = ficaram[0] if ficaram else None; ef = []; bens = {}; L = []; mortos = {}
    cont = bichos_de(E, sid)
    for i, f in enumerate(bs):
        esp = _esp_de(f)
        if not esp or not sai(f) or mortos.get(esp, 0) >= cont.get(esp, 0): continue
        mortos[esp] = mortos.get(esp, 0) + 1
        b, nuc = bichos.despojo(esp, estado.sorte(E, f"masmorra|{pid}|despojo|{d.get('lutas', 0)}|{i}"), cat=f.get('cat_corpo') if isinstance(f.get('cat_corpo'), int) else None)
        if leva:
            for k2, q in b.items(): bens[k2] = bens.get(k2, 0) + q
        if nuc: ef.append(['item', 'nasce', dict(nuc, dono=leva, onde=None if leva else onde, **({} if leva else dict(solto=True)), historia=[f"Dia {E['relogio']['dia']}: tirado {_em(E, sid)}"])])
    for esp, q in mortos.items(): ef.append(['lugar', sid, f'bichos.{esp}', 'soma', -q])
    fugiram = {}
    for f in bs:                                            # quem fugiu da luta some no escuro: sai da sala e passa a vaguear pela masmorra
        esp = _esp_de(f)
        if esp and f['estado'] == 'fugiu' and fugiram.get(esp, 0) + mortos.get(esp, 0) < cont.get(esp, 0): fugiram[esp] = fugiram.get(esp, 0) + 1
    for esp, q in fugiram.items(): ef += [['lugar', sid, f'bichos.{esp}', 'soma', -q], ['lugar', mid, f'vagantes.{esp}', 'soma', q]]
    if fugiram: L.append(f"{_cap(_diz_bando(fugiram))} {_s(sum(fugiram.values()), 'fugiu', 'fugiram')} para o escuro: {_s(sum(fugiram.values()), 'vagueia', 'vagueiam')} pela masmorra agora.")
    ch = _chefe_vivo(E, sid); chefe_caiu = False
    if ch and chn:
        fc = next((f for f in S['L'] if f['nome'] == chn), None)
        if fc and (fc['estado'] == 'morto' or (campo and fc['estado'] in ('caido', 'rendido'))):
            chefe_caiu = True; ef.append(['lugar', sid, 'chefe', 'poe', dict(ch, vivo=False)]); cc = _chefe_cat(ch['qual'])
            import tabelas_criaturas as TC
            C = TC.CHEFES.get(ch['qual']); rsd = estado.sorte(E, f"masmorra|{pid}|despojo_chefe|{d.get('lutas', 0)}")
            if C is None:
                b, nuc = bichos.despojo(ch['qual'], rsd, cat=cc)
                if leva:
                    for k2, q in b.items(): bens[k2] = bens.get(k2, 0) + q
                if nuc: ef.append(['item', 'nasce', dict(nuc, dono=leva, onde=None if leva else onde, **({} if leva else dict(solto=True)), historia=[f"Dia {E['relogio']['dia']}: tirado {_em(E, sid)}"])])
            base = (C or {}).get('povo') or (C or {}).get('especie')
            if C is not None and leva and base in TC.ESPECIES:
                b, _ = criaturas.despojo(base, rsd, cat=cc)
                for k2, q in b.items(): bens[k2] = bens.get(k2, 0) + q
            if C is not None and cc >= TB.NUCLEO_DESDE:
                ef.append(['item', 'nasce', itens.item('nucleo', cc, f"núcleo d{'a' if chn.startswith('a ') else 'o'} {chn.split(' ', 1)[-1]}", de=ch['qual'], dono=leva, onde=None if leva else onde,
                                                       **({} if leva else dict(solto=True)), historia=[f"Dia {E['relogio']['dia']}: tirado d{'a' if chn.startswith('a ') else 'o'} {chn.split(' ', 1)[-1]} {_em(E, sid)}"])])
            L.append(f"{_cap(chn)} caiu.")
    dr_ef, dr_partes, dr_L = [], {}, []
    if drn and _dragoes() and _dragao(E, sid):
        try: dr_ef, dr_partes, dr_L = _dragoes().depois_da_luta(E, sid, S, campo, ficaram)
        except (Exception, SystemExit) as x: dr_L = [f"(as contas do dragão não saíram: {x})"]
        ef += list(dr_ef); L += list(dr_L)
    caiu_fundo = (chefe_caiu or (drn and any(f['nome'] == drn and f['estado'] == 'morto' for f in S['L']))) and fundo(E, mid) == sid
    if campo and caiu_fundo and not E['lugares'][mid].get('limpa'):
        ef.append(['lugar', mid, 'limpa', 'poe', dict(dia=E['relogio']['dia'], quem=list(ficaram), chefe=chn or drn)])
        L.append(_txt(f"{_cap(E['lugares'][mid]['nome'])} foi limpa pela primeira vez, por {_e(_pn(E, c) for c in ficaram)}."))
    partes = {c: {} for c in ficaram}
    if leva:
        vez = 0
        for k2, v in bens.items():
            cada, resto = divmod(v, len(ficaram))
            for j, c in enumerate(ficaram):
                q = cada + (1 if (j - vez) % len(ficaram) < resto else 0)
                if q: partes[c][k2] = q
            vez = (vez + resto) % len(ficaram)
        ef += [['pessoa', c, 'carga.' + k2, 'soma', v] for c in ficaram for k2, v in partes[c].items()]
        tot = sum(mortos.values())
        if tot: ef.append(['pessoa', leva, 'marca.abates', 'soma', tot])
    ef += _alarme_ef(E, mid, K.ALARME['luta'])
    if sum(mortos.values()): L.insert(0, f"{_cap(_diz_bando(mortos))} {_s(sum(mortos.values()), 'sai', 'saem')} da contagem {_em(E, sid)}.")
    if leva and bens: L.append(('DESPOJO: ' + _e(f"{q} de {estado.nome_bem(b)}" for b, q in bens.items()) + f" (com {_pn(E, leva)})") if len(ficaram) == 1 else
                               'DESPOJO, em partes iguais entre quem lutou até o fim: ' + ' · '.join(f"{_pn(E, c)}: {_e(f'{q} de {estado.nome_bem(b)}' for b, q in partes[c].items()) or 'nada'}" for c in ficaram) + '.')
    for m_ in [pid] + list(d.get('com') or []):
        if E['gente'].get(m_, {}).get('estado') == 'morto' and (E['gente'][m_].get('morte') or {}).get('dia') == E['relogio']['dia']:
            L.append(f"{_pn(E, m_)} morreu {_em(E, onde)}: o que levava fica ali, com o corpo.")
    vivo = p['estado'] == 'vivo'
    d2 = json.loads(json.dumps(d)) if vivo else None
    if vivo:
        d2.update(fase='anda', encontro=None, luta=None, barulho=True, lances=d.get('lances', 0) + K.CUSTO['luta'])
        if not campo and d.get('anterior') in E['lugares'] and d['sala'] == sid:
            ant = d['anterior']; cam = list(d['caminho']); d2.update(sala=ant, caminho=cam[:cam.index(ant) + 1] if ant in cam else [ant]); d2['anterior'] = d2['caminho'][-2] if len(d2['caminho']) > 1 else None
    txt = (f"{_e(_pn(E, c) for c in ficaram)} {_s(len(ficaram), 'fica', 'ficam')} com o campo {_em(E, onde)}" if campo and ficaram else f"o grupo perde o campo {_em(E, onde)}") + (f": {_diz_bando(mortos)} a menos" if mortos else '')
    estado.aplica(E, EVENTO, ef + [['pessoa', pid, 'marca.masmorra', 'poe', d2]] + (_solta(E, d) if d2 is None else []), onde=onde, quem=[pid] + [c for c in d.get('com') or [] if c in E['gente']], texto=_txt(txt))
    if mortos and campo:
        try:
            import maldicao
            for q in [pid] + [c for c in d.get('com') or [] if c in E['gente']]: L += maldicao.confere(E, q)
        except ImportError: pass
    R = dict(fim=S['fim'], campo=campo, mortos=dict(mortos), leva=leva, bens=bens, partes=partes, chefe=chefe_caiu, rodadas=S['r'])
    if not vivo: R.update(fase='morto', texto='\n'.join(_txt(x) for x in L + [f"{p['nome']} morreu {_em(E, onde)}. A descida acaba aqui (quem ia junto sai sozinho: cena do Mestre)."])); return R
    if not campo:
        L.append(f"O grupo larga o campo e recua {_a_nome(_nm(E, descida(E['gente'][pid])['sala']))}.")
        if ocupada(E, sid) and enc.get('viu') != 'grupo':
            R2 = _persegue(E, pid, enc, descida(E['gente'][pid])['sala'], L)
            if R2: R.update(fase=R2['fase'], texto=R2['texto']); return R
    R2 = _fecha_blocos(E, pid, L)
    if R2: R.update(fase=R2['fase'], texto=R2['texto']); return R
    if campo and (E['lugares'][mid].get('alarme', 0) or 0) >= K.ALARME['vem']:
        R2 = _vem(E, pid, L)
        if R2: R.update(fase=R2['fase'], texto=R2['texto']); return R
    R.update(fase='anda', texto='\n'.join(_txt(x) for x in L + _aqui(E, pid))); return R


def _vem(E, pid, L):
    """o alarme em 4: quem está numa sala vizinha (sem chefe) vem ver o barulho, e chega logo depois da luta"""
    d = descida(E['gente'][pid]); sid = d['sala']
    for v in _viz(E, sid):
        n = bichos_de(E, v)
        if not n or _chefe_vivo(E, v) or _dragao(E, v): continue
        ef = [x for e, q in n.items() for x in (['lugar', v, f'bichos.{e}', 'soma', -q], ['lugar', sid, f'bichos.{e}', 'soma', q])] + [['lugar', sid, 'atento', 'poe', 1]]
        estado.aplica(E, EVENTO, ef, onde=sid, quem=_grupo(E, pid, d), texto=_txt(f"o barulho chama {_diz_bando(n)}, {_de(E, v)}"))
        L.append(_txt(f"O BARULHO CHAMOU QUEM ESTAVA PERTO: {_diz_bando(n)} {_s(sum(n.values()), 'chega', 'chegam')}, vindo {_de(E, v)}."))
        surp = _atencao(E, pid, d, sid, L)
        return _encontro(E, pid, dict(sala=sid, onde=sid, n=bichos_de(E, sid), chefe=None, dragao=None, viu='eles', surpresa=surp, inicio=K.INICIO['vem'], ouviu=False, vem=True), L)
    return None


# ---------- pegar, descansar, a ordem, a luz ----------
def pegar(E, pid, o_que='tudo', quem=None):
    """pega o que a sala guarda (1 lance): a prata e os bens repartem-se em partes iguais entre quem está na descida; a peça fica com quem a pega (quem comanda, sem dizer)"""
    p, d = _minha(E, pid, fases=('anda',)); estado.sem_luta(E); sid = d['sala']; g = _grupo(E, pid, d); q = quem or pid
    if q not in g: sys.exit(f'"{q}" não está no grupo')
    if ocupada(E, sid): sys.exit(f"há quem more aqui, de pé ({_diz_bando(bichos_de(E, sid), _chefe_vivo(E, sid), _dragao(E, sid))}): não se pega nada com eles olhando")
    gd = _sala(E, sid).get('guardado')
    if isinstance(gd, dict) and not gd.get('aberto'): sys.exit(f"{_cap(gd['nome'])} está fechad{'a' if gd['nome'].startswith('a ') else 'o'}: `masmorra.py abrir guardado`")
    est = {b: int(v) for b, v in _num(_sala(E, sid).get('estoque')).items() if v >= 1}
    its = [it for it in E['itens']['itens'].values() if it.get('onde') == sid and not it.get('dono') and not estado.de_morto(it)]
    if o_que == 'prata': est = {b: v for b, v in est.items() if b == 'prata'}; its = []
    elif o_que not in ('tudo', None):
        its = [it for it in its if it['id'] == o_que]; est = {}
        if not its: sys.exit(f'não há a peça "{o_que}" aqui para pegar' + (f" (há: {', '.join(it['id'] + ' ' + it['nome'] for it in E['itens']['itens'].values() if it.get('onde') == sid and not it.get('dono') and not estado.de_morto(it))})"))
    if not est and not its: sys.exit(f"não há o que pegar {_em(E, sid)}")
    ef = []; partes = {c: {} for c in g}; vez = 0
    for b, v in est.items():
        cada, resto = divmod(v, len(g)); ef.append(['estoque', sid, b, 'soma', -v])
        for j, c in enumerate(g):
            n = cada + (1 if (j - vez) % len(g) < resto else 0)
            if n: partes[c][b] = n; ef.append(['pessoa', c, 'moedas' if b == 'prata' else f'carga.{b}', 'soma', n])
        vez = (vez + resto) % len(g)
    for it in its: ef += [['item', it['id'], 'dono', 'poe', q], ['item', it['id'], 'historia', 'junta', f"Dia {E['relogio']['dia']}: {_pn(E, q)} achou esta peça {_em(E, sid)}"]]
    d['lances'] = d.get('lances', 0) + K.CUSTO['pegar']
    diz = [f"{_pn(E, c)}: {_e(f'{n} de ' + ('prata' if b == 'prata' else estado.nome_bem(b)) for b, n in partes[c].items())}" for c in g if partes[c]]
    txt = f"o grupo pega o que há {_em(E, sid)}" + (f": {_e(f'{v} de ' + ('prata' if b == 'prata' else estado.nome_bem(b)) for b, v in est.items())}" if est else '') + (f"; {_pn(E, q)} fica com {_e(it['nome'] for it in its)}" if its else '')
    _marca(E, pid, d, txt, mais=ef)
    L = [_txt(f"{_cap(txt)} ({_lances(K.CUSTO['pegar'])})." + (f" Em partes iguais: {' · '.join(diz)}." if diz and len(g) > 1 else ''))]
    R = _fecha_blocos(E, pid, L)
    return R or dict(fase='anda', texto='\n'.join(L), partes=partes, itens=[it['id'] for it in its])


def descansar(E, pid, n, vigia=None):
    """dorme N blocos no chão, ali (o bloco aberto fecha antes). Cada bloco o mundo rola o que vagueia: com quem vigia (vigia=ID, que não dorme), o grupo não é
    surpreendido; sem vigia, é. O sono e o cansaço baixam como no chão; o PV volta pouco: para sarar, a vila."""
    p, d = _minha(E, pid, fases=('anda',)); estado.sem_luta(E); g = _grupo(E, pid, d)
    try: n = int(n)
    except (TypeError, ValueError): n = 0
    if not 1 <= n <= M.BLOCOS_DIA: sys.exit(f'descansa-se de 1 a {M.BLOCOS_DIA} blocos (veio "{n}")')
    if vigia is not None and vigia not in g: sys.exit(f'"{vigia}" não está no grupo')
    if vigia is not None and len(g) < 2: sys.exit('quem está sozinho não vigia o próprio sono')
    if ocupada(E, d['sala']): sys.exit('há quem more aqui, de pé: não se dorme com eles olhando')
    L = []
    if d.get('lances', 0) > 0:
        R = _bloco(E, pid, L, inteiro=True)
        if R: return R
    for i in range(n):
        if E['gente'][pid]['estado'] != 'vivo': return _morreu(E, pid, L)
        R = _bloco(E, pid, L, dorme='chao', vigia=vigia)
        if R: return R
    L.append(f"O grupo descansou {caca._bl(n)}" + (f", com {_pn(E, vigia)} de vigia" if vigia else ', sem vigia') + '.')
    return dict(fase='anda', texto='\n'.join(_txt(x) for x in L))


def ordem(E, pid, ids):
    """a ordem de marcha (sem lance): o primeiro pisa primeiro, olha primeiro e fica na frente na luta"""
    p, d = _minha(E, pid); g = _grupo(E, pid, d); o = list(dict.fromkeys(ids))
    if set(o) != set(g): sys.exit(f"a ordem tem de ter o grupo inteiro, cada um uma vez ({', '.join(g)})")
    if d.get('fase') == 'luta': sys.exit('com a luta aberta, a ordem é a da luta (`masmorra.py luta "Nome: ordem"`)')
    d['ordem'] = o; _marca(E, pid, d, f"a ordem de marcha: {_e(_pn(E, c) for c in o)}")
    return dict(fase=d['fase'], texto=f"A ordem de marcha: {_e(_pn(E, c) for c in o)}.")


def luz(E, pid, tipo, quem=None):
    """acende ou apaga a luz (sem lance): a tocha de quem leva uma, o feitiço luz de quem o sabe, ou nada"""
    p, d = _minha(E, pid)
    if d.get('fase') == 'luta': sys.exit('com a luta aberta, a luz só muda pelo feitiço (a regra da luta)')
    d['luz'] = _luz_escolhe(E, _grupo(E, pid, d), tipo, quem)
    _marca(E, pid, d, f"a luz do grupo: {_luz_diz(E, d['luz'])}")
    return dict(fase=d['fase'], texto=_txt(f"A luz do grupo: {_luz_diz(E, d['luz'])}."))


# ---------- voltar, sair ----------
def voltar(E, pid):
    """volta pelas salas andadas até a entrada (1 lance por sala). Nas salas limpas, nada; na que tem gente de novo, o encontro."""
    p, d = _minha(E, pid, fases=('anda', 'armadilha')); estado.sem_luta(E); L = []
    rota = _rota(E, pid, d)
    if rota is None: sys.exit(f"não há caminho conhecido {_de(E, d['sala'])} até a entrada (uma porta trancada no meio?): ande sala a sala com `masmorra.py ir`")
    for para in rota:
        d = json.loads(json.dumps(descida(E['gente'][pid]))); de_ = d['sala']; cam = list(d['caminho'])
        d.update(sala=para, caminho=cam[:cam.index(para) + 1] if para in cam else cam + [para], fase='anda', armadilha=None, anterior=de_, lances=d.get('lances', 0) + K.CUSTO['voltar'])
        pt = porta(E, de_, para); ef = []
        if pt and pt.get('estado') == 'fechada': ef.append(['lugar', d['masmorra'], f'portas.{_pk(de_, para)}', 'poe', dict(pt, estado='aberta')])
        _marca(E, pid, d, f"o grupo volta {_a_nome(_nm(E, para))}", mais=ef)
        L.append(_txt(f"O grupo volta {_a_nome(_nm(E, para))} ({_lances(K.CUSTO['voltar'])})."))
        R = _fecha_blocos(E, pid, L)
        if R: return R
        if ocupada(E, para):
            enc = _ve_quem(E, pid, para, L)
            if enc: return _encontro(E, pid, enc, L)
    d = descida(E['gente'][pid])
    L.append(_txt(f"O grupo está {_em(E, d['sala'])}, a entrada: `masmorra.py sair` volta para casa."))
    return dict(fase='anda', texto='\n'.join(L))


def _rota(E, pid, d):
    """o caminho mais curto da sala do grupo até a entrada, pelas salas que o grupo viu e pelas passagens que dá para passar (porta aberta, fechada ou arrombada): a lista
    das salas a andar (sem a de agora), [] se já está lá, ou None se não há"""
    ent = E['lugares'][d['masmorra']].get('entrada'); vistas = set(((E['gente'][pid].get('marca') or {}).get('mapa') or {}).get(d['masmorra'], {}).get('salas') or []) | set(d.get('caminho') or [])
    de_ = {d['sala']: None}; fila = [d['sala']]
    while fila:
        s = fila.pop(0)
        if s == ent:
            out = []
            while de_[s] is not None: out.append(s); s = de_[s]
            return out[::-1]
        for v in _viz(E, s):
            pt = porta(E, s, v)
            if v in de_ or v not in vistas or (pt and pt.get('estado') in ('trancada', 'emperrada')): continue
            de_[v] = s; fila.append(v)
    return None


def sair(E, pid):
    """sai pela entrada e volta para casa: fecha o bloco aberto (o resto conta como bloco inteiro) e faz a volta. Quem comanda e morreu: a descida fecha (e, com a luta
    acabada, as contas antes)."""
    p, d = _minha(E, pid, vivo=False); L = []
    if d.get('fase') == 'luta':
        R = acerta(E, pid)
        if R['fase'] not in ('anda',): return R
        L.append(R['texto'].rsplit('\n', 1)[0]); d = descida(E['gente'][pid])
    if p['estado'] != 'vivo': return _morreu(E, pid, L)
    if d.get('fase') == 'encontro': sys.exit('há gente à frente: `masmorra.py atacar` ou `recuar` (recuar é o jeito de sair dali)')
    if d['sala'] != E['lugares'][d['masmorra']].get('entrada'):
        R = voltar(E, pid); L.append(R['texto'])
        if R['fase'] != 'anda': R['texto'] = '\n'.join(L); return R
    d = descida(E['gente'][pid])
    if d.get('lances', 0) > 0:
        R = _bloco(E, pid, L, inteiro=True)
        if R: return R
    d = descida(E['gente'][pid]); g = _grupo(E, pid, d); com = [c for c in g if c != pid]; n = _longe(E, d['masmorra']); antes = corpo.faixas(E['gente'][pid])
    ato.passa(E, pid, n, EVENTO, esforco=K.ESFORCO_IDA, para=False, texto=_txt(f"{p['nome']} volta {_de(E, d['masmorra'])}"), com=com,
              mais=lambda i: ([['pessoa', pid, 'marca.masmorra', 'poe', None]] + _solta(E, d)) if i == n - 1 else [])
    p = E['gente'][pid]
    if p['estado'] != 'vivo': return _morreu(E, pid, L, d)
    if descida(p): _marca(E, pid, None, f"{p['nome']} chega de volta")
    caca.merenda(E, com, L)
    L.append(_txt(f"O grupo sai {_de(E, d['masmorra'])} e volta ({caca._bl(n)}): {p['nome']} chega {_em(E, p['lugar'])} depois de {caca._bl(d.get('blocos', 0))} lá dentro."))
    if corpo.cruzou(p, antes): L.append(f"No caminho: {corpo.cruzou(p, antes)}.")
    return dict(fase='fim', texto='\n'.join(L))


def _morreu(E, pid, L, d=None):
    """quem comanda morreu no meio da descida: ela fecha (quem ia junto sai sozinho: cena do Mestre); o que ele levava fica na sala"""
    p = E['gente'][pid]; d = descida(p) or d
    if descida(p): _marca(E, pid, None, f"a descida de {p['nome']} acaba", quem=[pid])
    return dict(fase='morto', texto='\n'.join(_txt(x) for x in list(L) + [f"{p['nome']} {estado.morte_diz(E, p)}: o que levava fica ali, com o corpo. A descida acaba aqui."]))


def larga(E, pid, porque):
    """SÓ O MESTRE: fecha a descida SEM as contas (o arquivo da luta se perdeu, a cena mudou). O que o Mestre decidir entra por evento "mestre"."""
    p = E['gente'].get(pid) or sys.exit(f'não há a pessoa "{pid}"'); d = (p.get('marca') or {}).get('masmorra')
    if d is None: sys.exit(f"{p['nome']} não tem descida aberta")
    if not (porque or '').strip(): sys.exit('diga por que a descida é largada: `masmorra.py larga "por quê"`')
    d = d if isinstance(d, dict) else {}
    for l in E['turno']['lutas']:
        if d.get('luta') and l['arq'] == d['luta'] and not l['fim']: l['fim'] = 'largada'
    soltos = [c for c in (d.get('com') if isinstance(d.get('com'), list) else []) if c in E['gente'] and (E['gente'][c].get('marca') or {}).get('masmorra') is not None]
    estado.aplica(E, 'mestre', [['pessoa', q, 'marca.masmorra', 'poe', None] for q in [pid] + soltos], onde=d.get('sala') if d.get('sala') in E['lugares'] else None, quem=[pid] + soltos,
                  texto=f"a descida de {p['nome']} é largada sem as contas: {porque}")
    return dict(fase='fim', texto=f"A descida de {p['nome']} foi largada sem as contas ({porque}). O que houve nela entra por `estado.py mestre`.")


# ---------- olhar ----------
def _agora(E, pid):
    p = E['gente'][pid]; d = descida(p)
    if vai_com(p): return f"foi junto na descida de {E['gente'].get(vai_com(p), {}).get('nome', vai_com(p))}, {_em(E, estado.fora(E, pid) or p['lugar'])}: quem decide é quem comanda"
    if not d: return 'sem descida aberta'
    base = (f"{_em(E, d['sala'])} ({_largura_diz(_sala(E, d['sala']))}), {_de(E, d['masmorra'])}, desde o Dia {d.get('dia')}; {caca._bl(d.get('blocos', 0))} lá dentro; "
            f"{_lances(d.get('lances', 0))} andados: {_s(K.LANCES_BLOCO - d.get('lances', 0), 'falta', 'faltam')} {K.LANCES_BLOCO - d.get('lances', 0)} para o bloco fechar")
    f = d.get('fase')
    if f == 'encontro': return base + '; HÁ GENTE À FRENTE: `masmorra.py atacar`, `esperar` ou `recuar`'
    if f == 'luta': return base + f"; EM LUTA: `masmorra.py luta \"{p['nome']}: atacar\"`"
    if f == 'armadilha': return base + '; PARADO diante de armadilha achada: `desarmar`, `contornar` ou `disparar`'
    return base


def _mapa_diz(E, pid, d):
    """o mapa que o grupo viu: as salas, as passagens e as portas, as armadilhas achadas"""
    mid = d['masmorra']; mp = ((E['gente'][pid].get('marca') or {}).get('mapa') or {}).get(mid) or {}; vistas = [s for s in mp.get('salas') or [] if s in E['lugares']]; L = []
    for s in vistas:
        l = _sala(E, s); ps = []
        for v in _viz(E, s):
            pt = porta(E, s, v); ps.append((_nm(E, v) if v in vistas else 'uma passagem') + (f" (porta {pt['estado']})" if pt else ''))
        arms = [f"{_arm_nome(a)} {_arm_onde(E, s, a)}" + (f" ({a['feita']})" if a.get('feita') else '') for i, a in enumerate(l.get('armadilhas') or []) if f"{s}#{i}" in (mp.get('armadilhas') or [])]
        L.append(f"[{s}] {l['nome']}" + (' (aqui)' if s == d['sala'] else '') + f": {', '.join(ps) or 'sem saída'}" + (f"; armadilha: {', '.join(arms)}" if arms else ''))
    return L


def ver(E, pid):
    """as linhas da masmorra para esta pessoa: a descida aberta (onde, a luz, o tempo, o alarme, o grupo, o mapa visto, o que se faz daqui), ou as masmorras vizinhas"""
    p = E['gente'][pid]; L = []
    if vai_com(p): return [f"**DESCIDA ABERTA:** {_agora(E, pid)}"]
    d = descida(p)
    if d:
        L.append(f"**DESCIDA ABERTA:** {p['nome']} {_agora(E, pid)}.")
        l = _sala(E, d['sala'])
        if l.get('sobre'): L.append(f"O que se vê aqui: {l['sobre']}")
        lz = d.get('luz') or {}
        L.append(f"A luz: {_luz_diz(E, lz)}." if lz.get('tipo') else 'Sem luz: ESCURO' + (' (a sala tem fogo aceso)' if l.get('acesa') else '') + '.')
        L.append(_alarme_diz(E, d['masmorra']) + '.')
        L.append('O grupo, na ordem de marcha: ' + ', '.join(f"{_pn(E, c)} (PV {E['gente'][c]['pv']}/{estado.pv_max(E['gente'][c])}" + (', atrás na luta' if _de_tras(E, c) else '') + ')' for c in _ordem(E, pid, d)) + '.')
        mp = _mapa_diz(E, pid, d)
        if mp: L.append('O mapa que o grupo viu: ' + ' · '.join(mp))
        L += _aqui(E, pid)
        L += le_encontro(E, pid)
        if d.get('fase') == 'anda':
            L.append(f"Daqui: `ir SALA [escondido]` ({K.CUSTO['ir']}; escondido {K.CUSTO['escondido']}; no escuro, o dobro) · `escutar SALA` ({K.CUSTO['escutar']}) · `procurar` ({K.CUSTO['procurar']}) · `abrir SALA|guardado` ({K.CUSTO['tenta']} por tentativa) · "
                     f"`desarmar` · `contornar` · `disparar` ({K.CUSTO['tenta']}) · `pegar` ({K.CUSTO['pegar']}) · `descansar N` · `voltar` ({K.CUSTO['voltar']} por sala) · `sair`")
        return [_txt(x) for x in L]
    for mid in masmorras(E, p['lugar']):
        m = E['lugares'][mid]; mp = ((p.get('marca') or {}).get('mapa') or {}).get(mid) or {}
        L.append(f"**{m['nome']}**, a {caca._bl(_longe(E, mid))} [`{mid}`]" + (f": {m['sobre']}" if m.get('sobre') else '') + (f" (o grupo já viu {estado.tantos(len(mp.get('salas') or []), 'sala')} dela)" if mp.get('salas') else '')
                 + (f" Contam que foi limpa no Dia {m['limpa']['dia']}." if isinstance(m.get('limpa'), dict) else ''))
    if L: L.append("`masmorra.py descer [MASMORRA] [com=ID,ID] [ordem=ID,ID] [luz=tocha|feitiço|nada] [quem_luz=ID]` (a tocha arde um bloco; a loja a vende)")
    return [_txt(x) for x in L]


def mapa(E, mid):
    """SÓ O MESTRE: o mapa inteiro, sala por sala (quem mora, quantos, se dormem; as armadilhas, achadas ou não; as portas e as fechaduras; o tesouro; os segredos; o chefe)"""
    m = E['lugares'].get(mid) or sys.exit(f'não há o lugar "{mid}"')
    if m.get('tipo') != 'masmorra': sys.exit(f'"{mid}" não é masmorra')
    L = [f"{m['nome']} [{mid}] · {m.get('molde')} · alarme {m.get('alarme', 0)} · o que vagueia: {_e(_nome(e, int(q)) for e, q in _num(m.get('vagantes')).items() if q >= 1) or 'ninguém'} (chance por bloco {chance_vaga(E, mid):.0%})"
         + (f" · limpa no Dia {m['limpa']['dia']}" if isinstance(m.get('limpa'), dict) else '')]
    for nv in m.get('niveis') or []:
        L.append(f"nível {nv['n']} ({T.CATS[nv['cat']]}):")
        for s in nv.get('salas') or []:
            if s not in E['lugares']: continue
            l = E['lugares'][s]; n = bichos_de(E, s); ch = l.get('chefe'); dr = _dragao(E, s); x = []
            if n: x.append(_diz_bando(n) + {-1: ' (dormindo)', 1: ' (alertas)'}.get(l.get('atento', 0), ''))
            if isinstance(ch, dict): x.append(f"o chefe: {_chefe_nome(ch['qual'])}" + ('' if ch.get('vivo', True) else ' (morto)'))
            if dr: x.append(f"o dragão {dr['nome']}")
            if l.get('teto'): x.append('ninho: ' + ', '.join(f"{e} até {q:g}" for e, q in _num(l['teto']).items()))
            for i, a in enumerate(l.get('armadilhas') or []): x.append(f"{_arm_nome(a)} {_arm_onde(E, s, a)}" + (f" ({a['feita']})" if a.get('feita') else ' (achada)' if a.get('achada') is not None else ' (escondida)'))
            gd = l.get('guardado')
            if isinstance(gd, dict): x.append(f"{gd['nome']}" + (f", fechadura {T.CATS[gd['fechadura']]}" if gd.get('fechadura') is not None else '') + (' (aberto)' if gd.get('aberto') else ''))
            tes = _tesouro(E, s)
            if tes: x.append(f"tesouro: {tes}")
            for sg in l.get('segredos') or []: x.append(f"passagem escondida para {sg['para']} ({T.CATS[sg['cat']]})")
            ps = [v + (f" (porta {porta(E, s, v)['estado']}, {porta(E, s, v).get('material', 'madeira')}" + (f", fechadura {T.CATS[porta(E, s, v)['fechadura']]}" if porta(E, s, v).get('fechadura') is not None else '') + ')' if porta(E, s, v) else '') for v in _viz(E, s)]
            L.append(f"  [{s}] {l['nome']} ({_largura_diz(l)}{', acesa' if l.get('acesa') else ''}): " + ' · '.join(x + [f"passagens: {', '.join(ps) or 'nenhuma'}"]))
    chaves = [f"{it['nome']} ({it['id']}) abre {it.get('abre')}, " + (f"com {E['gente'][it['dono']]['nome']}" if it.get('dono') in E['gente'] else f"em {it.get('onde')}") for it in E['itens']['itens'].values() if it.get('tipo') == 'chave' and isinstance(it.get('abre'), str) and it['abre'].split('|')[0] in salas(E, mid)]
    if chaves: L.append('as chaves: ' + ' · '.join(chaves))
    return [_txt(x) for x in L]


# ---------- os ganchos do mundo ----------
def _de_quem(E):
    """o personagem e a descida em que ele está (a dele, ou a de quem ele segue): (quem comanda, descida) ou (None, None)"""
    pid = estado.eu(E)
    if not pid or E['gente'][pid]['estado'] != 'vivo': return None, None
    k = estado.quem_desce(E, pid)
    return (k, descida(E['gente'][k])) if k else (None, None)


def voce(E): return []


def mesa(E):
    """a seção da masmorra na MESA: só com a descida aberta"""
    k, d = _de_quem(E)
    if not d: return []
    return ['## A masmorra'] + ['- ' + x for x in ver(E, k)]


def so_mestre(E):
    """o SÓ O MESTRE: com a descida aberta, o mapa inteiro da masmorra; sem ela, uma linha por masmorra vizinha"""
    k, d = _de_quem(E)
    if d: return [f"a masmorra (o mapa inteiro; `masmorra.py mapa {d['masmorra']}`): "] + ['  ' + x for x in mapa(E, d['masmorra'])]
    pid = estado.eu(E)
    if not pid: return []
    aqui = E['gente'][pid].get('lugar') if E['gente'][pid]['estado'] == 'vivo' else None
    L = []
    for mid in (masmorras(E, aqui) if aqui in E['lugares'] else []):
        m = E['lugares'][mid]; vivos = sum(sum(bichos_de(E, s).values()) for s in salas(E, mid)); f = fundo(E, mid)
        chv = bool(f and _chefe_vivo(E, f)) or bool(f and _dragao(E, f))
        ouro = sum(int(_num(E['lugares'][s].get('estoque')).get('prata', 0)) for s in salas(E, mid))
        L.append(f"{m['nome']} [{mid}]: {vivos} morando nas salas, o chefe do fundo {'vivo' if chv else 'morto'}, {ouro} de prata nas salas, alarme {m.get('alarme', 0)} (`masmorra.py mapa {mid}`)")
    return [_txt(x) for x in L]


def retomar(E):
    """a linha da masmorra para o RETOMAR.md: a descida que ficou aberta no fim do turno"""
    pid = estado.eu(E)
    if not pid or E['gente'][pid]['estado'] != 'vivo': return []
    p = E['gente'][pid]
    if not (descida(p) or vai_com(p)): return []
    return [_txt(f"**Descida aberta:** {p['nome'] + ' ' if descida(p) else ''}{_agora(E, pid)}")]


def recusa_fecha(E): return []


def virada(E):
    """O DIA VIROU, NA MASMORRA (evento masmorra_vida, o mundo sozinho): o alarme volta a 0; o chefe vivo ergue um morto a cada 10 dias, até o que a sala tinha;
    o nível que ficou sem quem mande (sem chefe vivo e sem morador que não seja bicho que cria) espera 120 dias por um bando de fora (sem tesouro)."""
    import criaturas
    dia = E['relogio']['dia']
    for mid, m in list(E['lugares'].items()):
        if not isinstance(m, dict) or m.get('tipo') != 'masmorra': continue
        ef = []; txt = []
        if m.get('alarme'): ef.append(['lugar', mid, 'alarme', 'poe', 0])
        for s in salas(E, mid):
            ch = E['lugares'][s].get('chefe')
            if not (isinstance(ch, dict) and ch.get('vivo', True) and isinstance(ch.get('ergue'), dict)): continue
            if dia - (ch.get('ergueu') or 0) < K.MEMORIA['ergue']: continue
            for s2, quer in ch['ergue'].items():
                if s2 not in E['lugares']: continue
                tem = bichos_de(E, s2); e = next((e for e, q in _num(quer).items() if estado.especie(e) and tem.get(e, 0) < q), None)
                if e: ef += [['lugar', s2, f'bichos.{e}', 'soma', 1], ['lugar', s, 'chefe', 'poe', dict(ch, ergueu=dia)]]; txt.append(f"{_chefe_nome(ch['qual'])} ergue {_nome(e)} {_em(E, s2)}"); break
        niveis = json.loads(json.dumps(m.get('niveis') or [])); mudou = False
        for nv in niveis:
            ss = [s for s in nv.get('salas') or [] if s in E['lugares']]
            vazio = not any(_chefe_vivo(E, s) or _dragao(E, s) or any(not _fera(e) for e in bichos_de(E, s)) for s in ss)
            if not vazio:
                if 'vazio' in nv: nv.pop('vazio'); mudou = True
                continue
            if 'vazio' not in nv: nv['vazio'] = dia; mudou = True; continue
            fora = (K.MOLDES.get(m.get('molde')) or {}).get('fora') or []
            if fora and dia - nv['vazio'] >= K.MEMORIA['vem_de_fora']:
                rs = estado.sorte(E, f'masmorra|{mid}|fora|{nv["n"]}'); esp = fora[rs.randrange(len(fora))]
                ocupadas = {estado.descida(E, k)['sala'] for k in E['gente'] if estado.descida(E, k)}
                cand = [s for s in ss if s not in ocupadas and E['lugares'][s].get('largura') != 1] or [s for s in ss if s not in ocupadas]
                if cand:
                    s = cand[rs.randrange(len(cand))]; q = len(criaturas.bando(esp, rs))
                    ef.append(['lugar', s, f'bichos.{esp}', 'soma', q]); txt.append(f"um bando de fora ({_nome(esp, q)}) acha {_nm(E, s)} vazio e fica"); nv.pop('vazio'); mudou = True
        if mudou: ef.append(['lugar', mid, 'niveis', 'poe', niveis])
        if ef: estado.aplica(E, 'masmorra_vida', ef, onde=mid, texto=_txt(f"{m['nome']}: " + ('; '.join(txt) or 'o dia passa')))


# ---------- pôr a masmorra: à mão (a planta) e pelo gerador ----------
def poe(E, planta):
    """os efeitos da masmorra feita à mão (evento gera: segredo). A planta: {id, nome, em, molde, longe, vizinho, alarme, vagantes, origem, sobre, entrada,
    niveis: [{n, cat, salas}], salas: {SALA: {nome, ..., bichos, teto, estoque, chefe, guardado, armadilhas, segredos}}, passagens: [(A, B)], portas: {"A|B": porta},
    itens: [registros do itens.item com onde=SALA]}. A ordem que o gravador pede: nasce a masmorra, nascem as salas, e só então os vizinhos."""
    mid = planta['id']; viz = planta.get('vizinho')
    if mid in E['lugares']: sys.exit(f'já há o lugar "{mid}"')
    if viz not in E['lugares']: sys.exit(f'não há o lugar vizinho "{viz}"')
    m = dict(nome=planta['nome'], em=planta.get('em') or _em_nome(planta['nome']), tipo='masmorra', molde=planta['molde'], niveis=json.loads(json.dumps(planta['niveis'])), entrada=planta['entrada'],
             portas={}, alarme=planta.get('alarme', 0), vagantes=dict(planta.get('vagantes') or {}), longe=planta.get('longe', 1), vizinhos=[viz], limpa=None, origem=planta.get('origem', ''), estoque={})
    if planta.get('sobre'): m['sobre'] = planta['sobre']
    ef = [['lugar', 'nasce', mid, m]]
    nivel = {s: nv['n'] for nv in planta['niveis'] for s in nv['salas']}
    for s, r in planta['salas'].items():
        reg = {k: json.loads(json.dumps(v)) for k, v in r.items()}
        reg.update(tipo='sala', masmorra=mid, nivel=nivel[s]); reg.setdefault('em', _em_nome(reg['nome']))
        reg.setdefault('estoque', {})
        ef.append(['lugar', 'nasce', s, reg])
    vz = {s: [] for s in planta['salas']}
    for a, b in planta.get('passagens') or []: vz[a].append(b); vz[b].append(a)
    ef += [['lugar', s, 'vizinhos', 'poe', v] for s, v in vz.items() if v]
    for k, pt in (planta.get('portas') or {}).items(): ef.append(['lugar', mid, f'portas.{k}', 'poe', pt])
    ef.append(['lugar', viz, 'vizinhos', 'poe', list(dict.fromkeys(list(E['lugares'][viz].get('vizinhos') or []) + [mid]))])
    ef += [['item', 'nasce', it] for it in planta.get('itens') or []]
    return ef


def _ergue_de(salas_):
    """o que o chefe vivo ergue de novo: os mortos que andam de cada sala, como o gerador os pôs"""
    return {s: {e: q for e, q in (r.get('bichos') or {}).items() if _sem_vida(e)} for s, r in salas_.items() if any(_sem_vida(e) for e in (r.get('bichos') or {}))}


def cripta(E, vila='vila'):
    """A CRIPTA DA COVA VELHA (a vila de teste): 7 salas num nível só, Comum, sob o mausoléu quebrado da Cova Velha, com o guardião no fundo (projeto A, seção 7)"""
    import itens
    s = {k: f'cripta_{k}' for k in range(1, 8)}
    salas_ = {
        s[1]: dict(nome='a escada', em='na escada', largura=1, sobre='degraus de pedra que descem do mausoléu quebrado para o escuro; embaixo, uma porta de madeira'),
        s[2]: dict(nome='o corredor dos nichos', em='no corredor dos nichos', largura=1, cat=0, atento=0, bichos={'corpo-seco': 2},
                   armadilhas=[dict(tipo='dardo', cat=0, onde='chão', achada=None, feita=None)], sobre='um corredor estreito, de um só, com nichos dos dois lados; nos nichos, ossos e panos podres'),
        s[3]: dict(nome='o ossário', em='no ossário', cat=0, atento=0, bichos={'esqueleto': 3}, estoque={'prata': 10}, sobre='uma sala larga de ossos empilhados até o teto; no meio, a tigela das oferendas'),
        s[4]: dict(nome='a capela', em='na capela', largura=2, cat=0, atento=-1, bichos={'ratazana': 4}, teto={'ratazana': 4}, estoque={'prata': 25, 'cura:0': 1},
                   guardado=dict(nome='o baú das oferendas', fechadura=0, aberto=False), armadilhas=[dict(tipo='dardo', cat=0, onde='guardado', achada=None, feita=None)],
                   sobre='a capela velha, de altar quebrado; no canto, um ninho de ratos; junto do altar, o baú das oferendas'),
        s[5]: dict(nome='os degraus', em='nos degraus', largura=1, armadilhas=[dict(tipo='runa', cat=0, onde='chão', achada=None, feita=None)],
                   sobre='degraus que descem estreitos até uma porta de ferro'),
        s[6]: dict(nome='a câmara do guardião', em='na câmara do guardião', largura=2, cat=0, atento=0, bichos={'esqueleto': 2}, estoque={'prata': 30},
                   chefe=dict(qual='guardião da cripta', vivo=True), guardado=dict(nome='o sarcófago', fechadura=0, aberto=False), segredos=[dict(para=s[7], cat=1)],
                   sobre='uma câmara funda, de colunas; no meio, um sarcófago de pedra lavrada'),
        s[7]: dict(nome='o nicho escondido', em='no nicho escondido', largura=1, estoque={'prata': 15}, sobre='um vão apertado atrás da parede, com o que alguém escondeu ali'),
    }
    salas_[s[6]]['chefe']['ergue'] = _ergue_de(salas_); salas_[s[6]]['chefe']['ergueu'] = E['relogio']['dia']
    return dict(id='cripta', nome='a Cripta da Cova Velha', em='na Cripta da Cova Velha', molde='cripta', longe=1, vizinho=vila, alarme=0, vagantes={'corpo-seco': 1, 'ratazana': 3},
                origem='os mortos da Cova Velha subiam daqui: sob o mausoléu quebrado, a cripta do cavaleiro que guardava o cemitério', sobre='dizem que os mortos da Cova Velha subiam de uma escada, debaixo do mausoléu quebrado',
                niveis=[dict(n=1, cat=0, salas=[s[k] for k in range(1, 8)])], entrada=s[1], salas=salas_,
                passagens=[(s[1], s[2]), (s[2], s[3]), (s[2], s[4]), (s[3], s[5]), (s[4], s[5]), (s[5], s[6])],
                portas={_pk(s[1], s[2]): dict(estado='fechada', material='madeira', cat=0, fechadura=None), _pk(s[5], s[6]): dict(estado='trancada', material='ferro', cat=1, fechadura=1)},
                itens=[itens.item('arma', 0, familia='maça', onde=s[4]), itens.item('chave', 0, 'a chave de ferro', abre=_pk(s[5], s[6]), onde=s[4]),
                       itens.item('escudo', 1, 'o escudo do guardião', onde=s[6]), itens.item('gazua', 1, onde=s[7])])


def na_vila(E, vila='vila'):
    """A CRIPTA DA COVA VELHA na vila de teste (um evento do gerador: segredo). Recusa antes de pôr qualquer coisa se já foi posta, ou se a vila não tem a Cova Velha."""
    if vila not in E['lugares']: sys.exit(f'não há a vila "{vila}"')
    if 'cripta' in E['lugares'] or any(E['lugares'][v].get('nome') == 'a Cripta da Cova Velha' for v in masmorras(E, vila)): sys.exit('a vila de teste já tem a Cripta da Cova Velha: não se põe duas vezes')
    if 'cova' not in E['lugares']: sys.exit('a Cripta da Cova Velha fica sob a Cova Velha: esta vila ainda não tem a etapa da magia (`vila_teste.py magia`)')
    pl = cripta(E, vila); ef = poe(E, pl)
    estado.aplica(E, 'gera', ef, onde=pl['id'], texto="a Cripta da Cova Velha, sob o mausoléu quebrado: 7 salas, o guardião no fundo")
    prata = sum(int((r.get('estoque') or {}).get('prata', 0)) for r in pl['salas'].values())
    return [f"{_cap(pl['nome'])}: {len(pl['salas'])} salas sob a Cova Velha, a {pl['longe']} bloco de {E['lugares'][vila]['nome']} ({prata} de prata nas salas; o guardião no fundo). O povo diz: {pl['sobre']}."]


def _id(E, nome):
    base = re.sub(r'[^a-z0-9]+', '_', ''.join(c for c in unicodedata.normalize('NFD', nome.lower()) if unicodedata.category(c) != 'Mn')).strip('_')
    base = re.sub(r'^(a|o|as|os)_', '', base) or 'masmorra'; k, x = 1, base
    while x in E['lugares']: k += 1; x = f'{base}_{k}'
    return x


def _peca(rs, cat, onde):
    import itens
    t = rs.choice(('arma', 'arma', 'armadura', 'escudo'))
    if t == 'arma': return itens.item('arma', cat, familia=rs.choice(sorted(T.FAMILIAS)), onde=onde)
    if t == 'armadura': return itens.item('armadura', cat, material=rs.choice(('couro', 'malha', 'placa')), onde=onde)
    return itens.item('escudo', cat, onde=onde)


def gera(E, molde, nome, vizinho, niveis=None, cat=None, longe=None, origem=''):
    """OS EFEITOS QUE CRIAM UMA MASMORRA pelo dado do mundo (evento gera: segredo). A forma: a entrada; um caminho até a escada (no último nível, até o chefe); de 1 a 3 salas
    de lado; no primeiro nível (e a cada 3), uma sala escondida. Cada nível uma categoria acima. Quem mora, as armadilhas, as portas e o tesouro saem do molde
    (tabelas_masmorra); a prata nasce aqui, uma vez."""
    import itens
    if molde not in K.MOLDES: sys.exit(f'molde desconhecido: "{molde}" (os que há: {", ".join(K.MOLDES)})')
    if vizinho not in E['lugares']: sys.exit(f'não há o lugar vizinho "{vizinho}"')
    if (E['lugares'][vizinho].get('tipo') or '') in ('sala', 'masmorra'): sys.exit('a masmorra é vizinha de uma vila ou de um ermo, não de outra masmorra')
    Md = K.MOLDES[molde]; mid = _id(E, nome); rs = estado.sorte(E, f'masmorra|gera|{mid}'); Nm = K.NOMES_SALA[molde]
    nn = int(niveis) if niveis else rs.randint(*Md['niveis']); c0 = int(cat) if cat is not None else 0
    if not 1 <= nn <= 9 or not 0 <= c0 + nn - 1 < len(T.CATS): sys.exit('os níveis vão de 1 a 9, e a categoria do último cabe na tabela')
    salas_, pas, portas_, itens_, nvs, k = {}, [], {}, [], [], 0
    usados = set(); fim_ant = None; seq = E['itens']['seq']; fk = None
    def novo_id():
        nonlocal k
        k += 1; return f"{mid}_{k}"
    def nome_sala(tipo):
        if tipo != 'salas': return Nm[tipo]
        livres = [x for x in Nm['salas'] if x not in usados] or Nm['salas']; x = rs.choice(livres); usados.add(x); return x
    def mora(c):
        lst = list(Md.get('mora') or []) + list(Md.get('covil') or [])
        ok = [e for e in lst if estado.especie(e) and _esp(e)['cat'] <= c] or sorted((e for e in lst if estado.especie(e)), key=lambda e: _esp(e)['cat'])[:1]
        return ok
    vag = {}
    for n in range(1, nn + 1):
        c = c0 + n - 1; tot = rs.randint(*Md['salas']); seg = (n - 1) % K.SEGREDO_CADA == 0; lado = min(rs.randint(*K.LADO), max(0, tot - 3 - seg))
        caminho_n = max(2, tot - lado - seg); ids = [novo_id() for _ in range(caminho_n)]; ultimo = n == nn
        for j, s in enumerate(ids):
            tipo = 'boca' if j == 0 and n == 1 else 'escada' if j == 0 else 'fundo' if j == len(ids) - 1 and ultimo else 'salas'
            larg = 1 if rs.random() < Md['corredor'] and tipo not in ('fundo',) else rs.choice((2, None))
            if tipo == 'salas' and larg == 1 and Nm['corredor'] not in usados: nm_ = Nm['corredor']; usados.add(nm_)
            else: nm_ = nome_sala(tipo)
            salas_[s] = dict(nome=nm_, cat=c, atento=0)
            if larg: salas_[s]['largura'] = larg
            if j: pas.append((ids[j - 1], s))
        if fim_ant: pas.append((fim_ant, ids[0]))
        lados = []
        for _ in range(lado):
            s = novo_id(); salas_[s] = dict(nome=nome_sala('salas'), cat=c, atento=0); dono = rs.choice(ids[:-1] if len(ids) > 1 else ids); pas.append((dono, s)); lados.append(s)
        esc = None
        if seg:
            esc = novo_id(); salas_[esc] = dict(nome=Nm['segredo'], cat=c, largura=1); dono = rs.choice(ids)
            salas_[dono].setdefault('segredos', []).append(dict(para=esc, cat=min(c + 1, len(T.CATS) - 1)))
        todas = ids + lados + ([esc] if esc else [])
        nvs.append(dict(n=n, cat=c, salas=todas))
        ms = mora(c)
        for s in ids[1:] + lados:
            if s == ids[-1] and ultimo: continue
            if not ms: break
            if Md.get('ninho') and rs.random() < K.NINHO:
                e = Md['ninho'][0]; q = len(bichos.bando(e, rs)); salas_[s].update(bichos={e: q}, teto={e: q}, atento=-1); continue
            if rs.random() < K.MORA:
                e = rs.choice(ms); q = len(bichos.bando(e, rs)); salas_[s]['bichos'] = {e: q}; salas_[s]['atento'] = rs.choice((-1, 0, 0, 1)) if not _sem_vida(e) else 0
        if ultimo:
            f = ids[-1]; chs = Md['chefe']; kk = max([x for x in chs if x <= c] or [min(chs)]); qual = chs[kk]
            if estado.especie(qual) and not _esp(qual).get('chefe'): qual = None
            if qual:
                import tabelas_criaturas as TC
                if qual in TC.CHEFES or estado.especie(qual): salas_[f]['chefe'] = dict(qual=qual, vivo=True)
            if ms: e = rs.choice(ms); salas_[f]['bichos'] = {e: K.GUARDA_CHEFE}
        else: fim_ant = ids[-1]
        # as portas do caminho; a do fundo é de ferro e trancada
        for a, b in [x for x in pas if x[0] in ids and x[1] in ids]:
            fundo_ = ultimo and b == ids[-1]
            if fundo_ or rs.random() < K.PORTA['chance']:
                x = rs.random(); est = 'trancada' if fundo_ else 'fechada' if x < K.PORTA['fechada'] else 'trancada' if x < K.PORTA['fechada'] + K.PORTA['trancada'] else 'emperrada'
                portas_[_pk(a, b)] = dict(estado=est, material='ferro' if fundo_ or rs.random() < K.PORTA['ferro'] else 'madeira', cat=c, fechadura=c if est == 'trancada' else None)
                if fundo_: fk = _pk(a, b)
        # as armadilhas
        tipos = list(M.ARMADILHAS) if Md['armadilhas'] == 'todas' else list(Md['armadilhas'])
        for _ in range(len(todas) // K.ARMADILHA_CADA if tipos else 0):
            s = rs.choice(ids[1:] + lados) if len(ids) > 1 else ids[0]; t = rs.choice(tipos)
            salas_[s].setdefault('armadilhas', []).append(dict(tipo=t, cat=c, onde='chão', achada=None, feita=None))
        # o tesouro: as salas de tesouro (a prata), as peças, as poções
        cand = lados + ([esc] if esc else []) + ids[1:]; nt = min(len(cand), rs.randint(*K.TESOURO['salas']))
        tes = list(dict.fromkeys(([esc] if esc else []) + lados + rs.sample(ids[1:] or ids, min(len(ids[1:] or ids), nt))))[:max(nt, 1)]
        if ultimo and ids[-1] not in tes: tes.append(ids[-1])
        for s in tes:
            salas_[s].setdefault('estoque', {})['prata'] = salas_[s].get('estoque', {}).get('prata', 0) + K.TESOURO['prata'][0] * K.TESOURO['prata'][1] ** c
            if s != esc and rs.random() < K.TESOURO['guardado'] and 'guardado' not in salas_[s]:
                salas_[s]['guardado'] = dict(nome=rs.choice(K.GUARDADOS), fechadura=c, aberto=False)
        npecas = max(1, len(todas) // K.TESOURO['pecas_cada'])
        for j in range(npecas):
            s = tes[j % len(tes)]; pc = min(len(T.CATS) - 1, c + (1 if s == esc or (ultimo and s == ids[-1]) else 0))
            it = _peca(rs, pc, s)
            if rs.random() < K.TESOURO['maldita']:
                try:
                    import maldicao
                    seq_ = seq + len(itens_) + 1; it['maldita'] = maldicao.molde(f"a praga {estado.de_nome(nome)}", pc, rs.choice(M.MALDICAO_TIPOS), dict(tipo='devolver', item=f"i{seq_:04d}", onde=s))
                except (ImportError, SystemExit): pass
            itens_.append(it)
        for j in range(rs.randint(*K.TESOURO['pocoes'])):
            s = rs.choice(tes); salas_[s].setdefault('estoque', {})[f'cura:{min(c, M.MATERIA_ATE)}'] = salas_[s].get('estoque', {}).get(f'cura:{min(c, M.MATERIA_ATE)}', 0) + 1
        if ms: e = rs.choice(ms); vag[e] = vag.get(e, 0) + rs.randint(1, 3)
    # a chave da porta do fundo, num baú de um nível de antes (se houver), ou em nenhum lugar (abre-se na gazua ou na força)
    com_bau = [s for s, r in salas_.items() if 'guardado' in r]
    if fk and com_bau and rs.random() < 0.5: itens_.append(itens.item('chave', 0, 'uma chave velha', abre=fk, onde=rs.choice(com_bau)))
    for s, r in salas_.items():
        if r.get('chefe'): r['chefe']['ergue'] = _ergue_de(salas_); r['chefe']['ergueu'] = E['relogio']['dia']
    pl = dict(id=mid, nome=nome, molde=molde, longe=int(longe) if longe else 1, vizinho=vizinho, alarme=0, vagantes=vag, origem=origem, entrada=nvs[0]['salas'][0], niveis=nvs,
              salas=salas_, passagens=pas, portas=portas_, itens=itens_)
    return poe(E, pl)


# ---------- a linha de comando ----------
def main(a=None):
    a = sys.argv[1:] if a is None else list(a)
    if not a: print(__doc__); return
    def eh_op(x): k = x.split('=', 1)[0]; return '=' in x and ':' not in k and ' ' not in k
    op = dict(x.split('=', 1) for x in a if eh_op(x)); pos = [x for x in a if not eh_op(x)]
    cmds = ('ver', 'descer', 'ir', 'escutar', 'procurar', 'abrir', 'desarmar', 'contornar', 'disparar', 'atacar', 'esperar', 'recuar', 'luta', 'pegar', 'descansar', 'ordem', 'luz',
            'voltar', 'sair', 'larga', 'mapa', 'gera')
    if not pos or pos[0] not in cmds: print(__doc__); return
    E = estado.carrega(); pid = op.get('quem') or estado.eu(E)
    if pid in E['gente'] and vai_com(E['gente'][pid]) and pos[0] not in ('ver',): op.setdefault('por', pid); pid = vai_com(E['gente'][pid])       # quem=ID de quem foi junto: é ele quem faz, na descida de quem comanda
    if pos[0] == 'mapa':
        mid = pos[1] if len(pos) > 1 else (descida(E['gente'][pid]) or {}).get('masmorra') or next(iter(masmorras(E, E['gente'][pid]['lugar'])), None)
        if not mid: sys.exit('diga a masmorra: `masmorra.py mapa MASMORRA`')
        print('\n'.join(mapa(E, mid))); return
    if pos[0] == 'gera':
        if len(pos) < 3: sys.exit(f'diga o molde e o nome: `masmorra.py gera MOLDE "Nome" [vizinho=LUGAR] [niveis=N] [cat=K] [longe=N]` (os moldes: {", ".join(K.MOLDES)})')
        viz = op.get('vizinho') or (E['gente'][pid]['lugar'] if pid in E['gente'] else None)
        ef = gera(E, pos[1], pos[2], viz, niveis=op.get('niveis'), cat=op.get('cat'), longe=op.get('longe'), origem=op.get('origem', ''))
        estado.aplica(E, 'gera', ef, onde=viz, texto=f"{pos[2]}, uma masmorra ({pos[1]}) vizinha {_de(E, viz)}")
        P = estado.valida(E)
        if P: sys.exit('A MASMORRA NASCEU TORTA (não foi gravada):\n  ' + '\n  '.join(P))
        estado.grava(E); print(f"{pos[2]} ({pos[1]}) nasceu, vizinha {_de(E, viz)}: o mapa é do Mestre (`masmorra.py mapa {ef[0][2]}`)."); return
    if pid not in E['gente']: sys.exit(f'não há a pessoa "{pid}"')
    if pos[0] == 'ver': print('\n'.join(ver(E, pid) or [f"{E['gente'][pid]['nome']} não tem masmorra vizinha nem descida aberta."])); return
    arg = pos[1] if len(pos) > 1 else None
    if pos[0] == 'descer': R = descer(E, pid, arg, com=[c for c in op.get('com', '').split(',') if c], ordem=[c for c in op.get('ordem', '').split(',') if c] or None, luz=op.get('luz'), quem_luz=op.get('quem_luz'))
    elif pos[0] == 'ir':
        if not arg: sys.exit('diga a sala: `masmorra.py ir SALA [escondido]`')
        R = ir(E, pid, arg, escondido='escondido' in pos[2:])
    elif pos[0] == 'escutar':
        if not arg: sys.exit('diga a sala: `masmorra.py escutar SALA`')
        R = escutar(E, pid, arg, quem=op.get('por'))
    elif pos[0] == 'procurar': R = procurar(E, pid, quem=op.get('por'))
    elif pos[0] == 'abrir':
        if not arg: sys.exit('diga o quê: `masmorra.py abrir SALA|guardado [gazua|chave|força]`')
        R = abrir(E, pid, arg, como=pos[2] if len(pos) > 2 else None, quem=op.get('por'))
    elif pos[0] == 'desarmar': R = desarmar(E, pid, arg, quem=op.get('por'))
    elif pos[0] == 'contornar': R = contornar(E, pid, arg)
    elif pos[0] == 'disparar': R = disparar(E, pid, arg)
    elif pos[0] == 'atacar': R = atacar(E, pid, inicio=op.get('inicio'), passagem='passagem' in pos[1:])
    elif pos[0] == 'esperar': R = esperar(E, pid)
    elif pos[0] == 'recuar': R = recuar(E, pid)
    elif pos[0] == 'luta': R = luta_roda(E, pid, pos[1:])
    elif pos[0] == 'pegar': R = pegar(E, pid, arg or 'tudo', quem=op.get('por'))
    elif pos[0] == 'descansar': R = descansar(E, pid, arg, vigia=op.get('vigia'))
    elif pos[0] == 'ordem': R = ordem(E, pid, [c for c in (arg or '').split(',') if c])
    elif pos[0] == 'luz': R = luz(E, pid, arg or 'nada', quem=op.get('por') or op.get('quem_luz'))
    elif pos[0] == 'voltar': R = voltar(E, pid)
    elif pos[0] == 'larga': R = larga(E, pid, arg or '')
    else: R = sair(E, pid)
    estado.grava(E)                                         # grava ANTES de falar: a saída cortada não perde o que o dado rolou
    print(_txt(R['texto']))
    print(ato.ultima_linha(E, pid))


if __name__ == '__main__':
    import signal; hasattr(signal, 'SIGPIPE') and signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    main()
