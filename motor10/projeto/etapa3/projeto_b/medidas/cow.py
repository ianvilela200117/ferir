"""cow.py — MEDIDA (projeto B, etapa 3): o gravador que só copia o que o evento toca (a proposta para o alicerce comum).

O `estado.aplica` de hoje ensaia o evento numa CÓPIA INTEIRA do estado (copy.deepcopy de gente, lugares, itens, turno e relógio) e depois compara tudo.
Com 150 nomeados com memória e 16 lugares com estoque, essa cópia é o custo do mundo. Aqui está o mesmo `aplica`, com as mesmas recusas e o mesmo
resultado, mas a cópia de ensaio é RASA: só se copia de verdade a pessoa, o lugar, o item ou a obra que o efeito nomeia; o efeito que mexe em muita coisa
de uma vez (a morte, o nascer de uma peça, a obra, a maldição, o verbo que este arquivo não conhece) copia o arquivo inteiro, como hoje.
`instala()` troca o estado.aplica por este (só no processo da medida); `confere()` roda o mesmo caminho com os dois e diz se o estado final é igual, byte a byte.
"""
import copy, sys
import estado
import tabelas_mundo as M

_ORIGINAL = estado.aplica


def _toca(E, ef):
    """o que o efeito pode mudar: uma lista de (arquivo, chave) — chave None é o arquivo inteiro"""
    if not isinstance(ef, (list, tuple)) or not ef: return [(k, None) for k in estado.ARQS]
    v = ef[0]
    if v == 'relogio': return [('relogio', None)]
    if v == 'pessoa':
        if len(ef) > 1 and ef[1] == 'nasce': return [('gente', '+')]
        if len(ef) == 5 and ef[2] == 'estado' and ef[4] == 'morto': return [('gente', None), ('itens', None), ('lugares', None)]
        if len(ef) == 5 and isinstance(ef[2], str) and ef[2].split('.')[0] in ('talento', 'dom', 'inclinacao', 'inclinacao2', 'povo', 'idade', 'marca', 'carga', 'treino', 'maestria',
                                                                                 'moedas', 'pv', 'fome', 'sono', 'cansaco', 'nivel', 'lugar', 'grau_oficio', 'mana'):
            return [('gente', ef[1])]
        return [('gente', None), ('itens', None)]
    if v == 'ferida': return [('gente', ef[1] if len(ef) > 1 else None)]
    if v == 'estoque': return [('lugares', ef[1] if len(ef) > 1 else None)]
    if v == 'lugar':
        if len(ef) > 1 and ef[1] == 'nasce': return [('lugares', '+')]
        return [('lugares', ef[1] if len(ef) > 1 else None)]
    if v == 'item':
        if len(ef) == 3 and ef[1] == 'nasce': return [('itens', '+item')]
        if len(ef) == 3 and ef[2] == 'some': return [('itens', '-item')]
        if len(ef) == 5 and ef[2] in ('dur', 'historia', 'nome', 'uso', 'onde', 'solto', 'sob_medida', 'dono'): return [('itens', ('item', ef[1]))]
        return [('itens', None)]
    return [(k, None) for k in estado.ARQS]          # a obra, a maldição e o resto: o arquivo inteiro, como hoje


def _ensaio(E, efeitos):
    """a cópia de ensaio: rasa, com cópia de verdade só do que os efeitos tocam"""
    ens = {k: E[k] for k in estado.ARQS}; feito = set()
    for ef in efeitos:
        for arq, ch in _toca(E, ef):
            if (arq, None) in feito: continue
            if ch is None:
                ens[arq] = copy.deepcopy(E[arq]); feito.add((arq, None)); continue
            if (arq, 'raso') not in feito:
                ens[arq] = dict(E[arq]) if arq != 'itens' else dict(E[arq], itens=dict(E[arq]['itens'])); feito.add((arq, 'raso'))
            if arq == 'itens':
                if ch in ('+item', '-item'): continue
                iid = ch[1]
                if (arq, iid) not in feito and iid in ens['itens']['itens']: ens['itens']['itens'][iid] = copy.deepcopy(E['itens']['itens'][iid]); feito.add((arq, iid))
                continue
            if ch == '+': continue
            if (arq, ch) not in feito and ch in ens[arq]: ens[arq][ch] = copy.deepcopy(E[arq][ch]); feito.add((arq, ch))
    return ens


def aplica(E, tipo, efeitos, onde=None, quem=(), texto=''):
    """o estado.aplica, com a cópia de ensaio rasa (as mesmas recusas, o mesmo resultado)"""
    if tipo not in M.EVENTOS: sys.exit(f'evento desconhecido: "{tipo}"')
    if not efeitos: sys.exit(f'evento "{tipo}" sem efeito: recusado. O que não muda número não aconteceu.')
    if tipo not in M.NA_LUTA and estado.luta_aberta(E) and not estado._nota_da_luta(E, efeitos): sys.exit(estado.luta_diz(E))
    ens = _ensaio(E, efeitos)
    for ef in efeitos:
        if isinstance(ef, (list, tuple)) and len(ef) == 5 and ef[0] == 'pessoa' and ef[2] in ('talento', 'dom'):
            if tipo not in estado.TALENTO_EVENTOS: sys.exit(f'evento "{tipo}" recusado (talento)')
        if tipo not in M.NASCE and isinstance(ef, (list, tuple)) and len(ef) > 1 and ef[0] in ('pessoa', 'lugar') and ef[1] == 'nasce':
            sys.exit(f'evento "{tipo}" recusado, nada mudou (nasce fora do gera)')
        try: e = estado._um(ens, ef)
        except (TypeError, KeyError, IndexError, AttributeError, ValueError) as x: e = estado._erro(ef, f'efeito malformado ({type(x).__name__})')
        if e: sys.exit(f'evento "{tipo}" recusado, nada mudou. {e}')
    if all(ens[k] is E[k] or ens[k] == E[k] for k in estado.ARQS): return None
    for pid, p in ens['gente'].items() if tipo != 'casa' else ():
        a = E['gente'].get(pid)
        if a is p: continue                                # a pessoa que o evento não tocou é o mesmo objeto: não mudou
        if isinstance(a, dict) and isinstance(p, dict) and not p.get('jogador') and p.get('estado') == 'vivo' and any(a.get(k) != p.get(k) for k in ('corpo', 'pv', 'feridas', 'mana')):
            if not isinstance(p.get('marca'), dict): p['marca'] = {}
            p['marca']['cena'] = estado.agora(E)
    ev = dict(id=E['relogio']['eventos'] + 1, dia=E['relogio']['dia'], bloco=E['relogio']['bloco'], tipo=tipo, onde=onde, quem=list(quem), efeitos=[list(x) for x in efeitos], texto=texto)
    for k in estado.ARQS: E[k] = ens[k]
    E['relogio']['eventos'] = ev['id']; E['_novos'].append(ev)
    return ev


def instala():
    estado.aplica = aplica


def desinstala(): estado.aplica = _ORIGINAL
