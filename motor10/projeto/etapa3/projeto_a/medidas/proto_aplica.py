#!/usr/bin/env python3
"""proto_aplica.py — PROTÓTIPO (projeto A, etapa 3): o gravador que copia só o que o evento toca ("cópia por toque").

Hoje o estado.aplica faz deepcopy do estado INTEIRO a cada evento (e compara o estado inteiro): com a vila de teste (32 KB) são ~9 ms por evento,
e 97% do tempo de um dia de mundo. Com a região (16 lugares, 150 nomeados, ~400 peças) o estado passa de 300 KB e o ano não roda em 2 minutos.
Aqui o ensaio é RASO: cada arquivo do estado é um dicionário novo que aponta para os registros de antes, e só o registro que um efeito pode mexer
(a pessoa, o lugar, o item, a obra, a rota) é copiado, uma vez por evento, antes do efeito. A morte (que mexe em peças, lugar e gente) copia tudo, como hoje.
As regras de recusa são as MESMAS do estado.aplica (este protótipo chama o mesmo _um). Nada daqui é motor: é medida.

  instala()      troca o estado.aplica por este (em memória, só neste processo)
  desinstala()   volta ao de antes
"""
import copy, sys
import estado, tabelas_mundo as M

_ORIGINAL = estado.aplica
EXTRA = []          # arquivos novos do estado (o protótipo da região põe 'rotas' aqui)


def _arqs(): return tuple(estado.ARQS) + tuple(EXTRA)


def _raso(E):
    """o ensaio raso: um dicionário novo por arquivo, com os registros de antes dentro (nada copiado ainda)"""
    S = {}
    for k in _arqs():
        v = E.setdefault(k, {}) if k in EXTRA else E[k]          # o arquivo novo que o save antigo não tem nasce vazio (o valor padrão)
        if k == 'itens': S[k] = dict(v, itens=dict(v['itens']), obras=dict(v.get('obras', {})))
        elif k in ('lugares', 'gente') or k in EXTRA: S[k] = dict(v)
        else: S[k] = copy.deepcopy(v)          # o relógio e o turno são pequenos
    return S


def _toca(S, E, toc, ef):
    """copia (uma vez por evento) o registro que este efeito pode mexer; devolve False se o efeito pede a cópia inteira"""
    if not isinstance(ef, (list, tuple)) or not ef: return True
    v = ef[0]
    def um(arq, k, sub=None):
        chave = (arq, sub, k)
        if chave in toc: return
        src = (E[arq][sub] if sub else E[arq]); dst = (S[arq][sub] if sub else S[arq])
        if k in src: dst[k] = copy.deepcopy(src[k])
        toc.add(chave)
    if v == 'relogio': return True
    if v in ('pessoa', 'ferida', 'maldicao'):
        if len(ef) > 1 and ef[1] == 'nasce': return True
        if v == 'pessoa' and len(ef) == 5 and ef[2] == 'estado' and ef[4] == 'morto': return False      # a morte mexe em peças, lugar e gente: copia tudo
        if len(ef) > 1 and isinstance(ef[1], str): um('gente', ef[1])
        return True
    if v in ('lugar', 'estoque'):
        if len(ef) > 1 and ef[1] == 'nasce': return True
        if len(ef) > 1 and isinstance(ef[1], str): um('lugares', ef[1])
        return True
    if v == 'item':
        if len(ef) > 1 and ef[1] == 'nasce': return True
        if len(ef) > 1 and isinstance(ef[1], str): um('itens', ef[1], 'itens')
        return True
    if v == 'obra':
        if len(ef) > 1 and ef[1] == 'abre': return True
        if len(ef) > 1 and isinstance(ef[1], str): um('itens', ef[1], 'obras')
        return True
    if v in EXTRA_VERBOS:
        arq = EXTRA_VERBOS[v]
        if len(ef) > 1 and ef[1] != 'nasce' and isinstance(ef[1], str): um(arq, ef[1])
        return True
    return False


EXTRA_VERBOS = {}   # verbo novo -> arquivo dele (o protótipo da região: 'rota' -> 'rotas')
UM_EXTRA = {}       # verbo novo -> função (E, ef) -> erro ou None


def _um(E, ef):
    if isinstance(ef, (list, tuple)) and ef and ef[0] in UM_EXTRA: return UM_EXTRA[ef[0]](E, ef)
    return estado._um(E, ef)


def _mudou(S, E, toc, cheio):
    if cheio: return any(S[k] != E[k] for k in _arqs())
    for k in _arqs():
        a, b = S[k], E[k]
        if k == 'itens':
            if {x: y for x, y in a.items() if x not in ('itens', 'obras')} != {x: y for x, y in b.items() if x not in ('itens', 'obras')}: return True
            for sub in ('itens', 'obras'):
                A, B = a[sub], b.get(sub, {})
                if A.keys() != B.keys(): return True
                if any(A[x] != B[x] for (arq, s, x) in toc if arq == 'itens' and s == sub and x in A): return True
        elif k in ('lugares', 'gente') or k in EXTRA:
            if a.keys() != b.keys(): return True
            if any(a[x] != b[x] for (arq, s, x) in toc if arq == k and x in a): return True
        elif a != b: return True
    return False


def aplica(E, tipo, efeitos, onde=None, quem=(), texto=''):
    """a mesma porta, com o ensaio raso (as mesmas recusas do estado.aplica)"""
    if tipo not in M.EVENTOS: sys.exit(f'evento desconhecido: "{tipo}"')
    if not efeitos: sys.exit(f'evento "{tipo}" sem efeito: recusado. O que não muda número não aconteceu.')
    if tipo not in M.NA_LUTA and estado.luta_aberta(E) and not estado._nota_da_luta(E, efeitos): sys.exit(estado.luta_diz(E))
    cheio = False; toc = set()
    S = _raso(E)
    for ef in efeitos:
        if isinstance(ef, (list, tuple)) and len(ef) == 5 and ef[0] == 'pessoa' and ef[2] in ('talento', 'dom'):
            if tipo not in estado.TALENTO_EVENTOS: sys.exit(f'evento "{tipo}" recusado (talento fora do evento certo)')
            q = E['gente'].get(ef[1]) if isinstance(ef[1], str) else None
            if ef[2] == 'talento' and isinstance(q, dict) and q.get('talento') is not None and tipo != 'mestre' and not estado._so_acrescenta(q, ef[4]): sys.exit(f'evento "{tipo}" recusado (talento já rolado)')
        if isinstance(ef, (list, tuple)) and len(ef) == 5 and ef[0] == 'pessoa' and ef[2] in estado.PESSOA_4B and tipo not in (estado.TALENTO_EVENTOS if ef[2] == 'inclinacao2' else estado.POVO_EVENTOS):
            sys.exit(f'evento "{tipo}" recusado (campo da 4b fora do evento certo)')
        if tipo not in M.NASCE and isinstance(ef, (list, tuple)) and len(ef) > 1 and ef[0] in ('pessoa', 'lugar') and ef[1] == 'nasce': sys.exit(f'evento "{tipo}" recusado (nasce fora de gera/mestre)')
        if not cheio and not _toca(S, E, toc, ef):
            cheio = True; base = S; S = {k: copy.deepcopy(E.get(k, {})) for k in _arqs()}
            # refaz, na cópia inteira, os efeitos que já tinham entrado no ensaio raso
            for ef0 in efeitos[:efeitos.index(ef)]:
                e = _um(S, ef0)
                if e: sys.exit(f'evento "{tipo}" recusado, nada mudou. {e}')
        try: e = _um(S, ef)
        except (TypeError, KeyError, IndexError, AttributeError, ValueError) as x: e = estado._erro(ef, f'efeito malformado ({type(x).__name__})')
        if e: sys.exit(f'evento "{tipo}" recusado, nada mudou. {e}')
    if not _mudou(S, E, toc, cheio): return None
    gente = S['gente'].items() if cheio else ((pid, S['gente'][pid]) for (arq, s, pid) in toc if arq == 'gente' and pid in S['gente'])
    for pid, p in (gente if tipo != 'casa' else ()):
        a = E['gente'].get(pid)
        if isinstance(a, dict) and isinstance(p, dict) and not p.get('jogador') and p.get('estado') == 'vivo' and any(a.get(k) != p.get(k) for k in ('corpo', 'pv', 'feridas', 'mana')):
            if not isinstance(p.get('marca'), dict): p['marca'] = {}
            p['marca']['cena'] = estado.agora(E)
    ev = dict(id=E['relogio']['eventos'] + 1, dia=E['relogio']['dia'], bloco=E['relogio']['bloco'], tipo=tipo, onde=onde, quem=list(quem), efeitos=[list(x) for x in efeitos], texto=texto)
    for k in _arqs(): E[k] = S[k]
    E['relogio']['eventos'] = ev['id']; E['_novos'].append(ev)
    return ev


def instala(): estado.aplica = aplica
def desinstala(): estado.aplica = _ORIGINAL
