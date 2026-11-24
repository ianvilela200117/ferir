#!/usr/bin/env python3
"""estado.py — MOTOR 10: O ESTADO DO MUNDO E O ÚNICO GRAVADOR.

O save é uma pasta (`mundo/`, ou a que estiver em MOTOR10_MUNDO) com: relogio.json · lugares.json · gente.json · itens.json
· turno.json · eventos.jsonl (o único histórico; o diário sai dele).
  CADA FATO NUM LUGAR SÓ: o dono de uma peça e onde ela está vestida moram só no itens.json; onde a pessoa está, só na ficha dela.
  SÓ `aplica()` MUDA O ESTADO. Um evento é {dia, bloco, tipo, onde, quem, efeitos, texto}; sem efeito, é recusado; o que não muda nada não entra no registro.
  Um efeito é uma operação tipada de uma lista fechada:
    ['relogio', blocos]                              o tempo anda
    ['pessoa', id, campo, 'soma'|'poe', valor]       moedas · pv · fome · sono · cansaco · lugar · estado · nivel · grau_oficio · treino.X · maestria.X (X: arma ou ofício) · marca.X
                                                     · carga.BEM (o que a pessoa carrega: só 'soma', nunca abaixo de zero)
    ['pessoa', 'nasce', id, registro]                uma pessoa nova (nome, nivel, atributos, lugar; o resto tem padrão). Só em evento "gera" ou "mestre"
    ['lugar', id, campo ou campo.sub, 'soma'|'poe', valor]   um número ou uma marca do lugar (bichos.lobo, coleta.metal:0, oficina, pop); 'soma' nunca abaixo de zero;
                                                     o que é conta (bichos, teto, coleta, coleta_teto, produz, pop, oficina, preparo) só aceita número, na faixa dele
    ['lugar', 'nasce', id, registro]                 um lugar novo (nome; o resto tem padrão). Só em evento "gera" ou "mestre"
    ['ferida', id, 'abre', parte, grave]  ·  ['ferida', id, 'repousa', n]  ·  ['ferida', id, 'sara', indice]
    ['estoque', lugar, bem, 'soma', valor]
    ['item', id, campo, 'poe'|'soma', valor]         dono · uso · dur
    ['item', 'nasce', registro]                      uma peça nova entra no Livro de Itens (o id sai da sequência); também núcleos (tipo 'nucleo')
    ['item', id, 'onde', 'poe', lugar]  ·  ['item', id, 'solto', 'poe', True|None]  ·  ['item', id, 'sob_medida', 'poe', {dono, grau}]
    ['item', id, 'historia', 'junta', 'texto']  ·  ['item', id, 'some']
    ['obra', 'abre', registro]  ·  ['obra', id, campo, 'soma'|'poe', valor]  ·  ['obra', id, 'fecha']      a obra em andamento (forja de vários dias)
  O ITEM SEM DONO está num lugar (`onde`). Ali ele é da LOJA (a prateleira), a não ser que esteja SOLTO (`solto`): caído no chão, de quem achar.
  A MORTE é uma regra só, dentro do efeito ['pessoa', id, 'estado', 'poe', 'morto']: o morto não fica com nada. As peças dele (vestidas ou guardadas, e os núcleos)
    caem SOLTAS onde ele morreu, com a marca `corpo` (de quem eram); as obras dele se desfazem (a matéria se perde; o núcleo cai com o resto); a carga e a prata
    ficam no estoque desse lugar (num lugar com povo, o povo fica com elas; no ermo, ficam no chão, junto do corpo).
    O QUE ERA DE UM MORTO NÃO MUDA DE MÃO SOZINHO: quem passa ali acha o corpo, mas quem fica com o quê é decisão de cena, por evento "mestre" (o herdeiro é da etapa 6).
  QUEM SAIU para o ermo (a saída de caça ou de coleta, escrita em marca.caca) está FORA: `fora()` diz onde, e `presente()` recusa o ato da vila.
  COM UMA LUTA ABERTA (no caderno do turno) O MUNDO NÃO ANDA: `aplica()` só aceita a luta que volta ao estado (evento "luta"), a mão do Mestre (evento "mestre")
    e a nota da saída de caça que diz que ela está naquela luta. O resto é recusado, de qualquer pessoa, com a frase que diz como acabar ou soltar a luta.
  O que o Mestre inventa em cena entra por um evento "mestre", com os mesmos efeitos. Fora disso, não aconteceu.

Uso (para olhar): python3 estado.py valida | python3 estado.py eventos [N] | python3 estado.py pessoa ID | python3 estado.py lugar ID
     (o Mestre): python3 estado.py mestre '[["pessoa","eu","moedas","soma",5]]' "achou cinco moedas na estrada"      um evento "mestre", com os efeitos em JSON
"""
import copy, hashlib, json, os, random, sys
import tabelas as T
import tabelas_mundo as M
import tabelas_bichos as TB

AQUI = os.path.dirname(os.path.abspath(__file__))
ARQS = ('relogio', 'lugares', 'gente', 'itens', 'turno')
PARTES_VESTE = ('arma', 'arma2', 'escudo', 'veste')


def pasta(): return os.environ.get('MOTOR10_MUNDO') or os.path.join(AQUI, 'mundo')


# ---------- ler e gravar ----------
def carrega():
    p = pasta()
    if not os.path.exists(os.path.join(p, 'relogio.json')): sys.exit(f'não há mundo em {p} (falta o relogio.json)')
    E = {k: json.load(open(os.path.join(p, k + '.json'), encoding='utf-8')) for k in ARQS}
    E['_novos'] = []
    return E


def grava(E):
    """escreve o estado inteiro (cada arquivo de uma vez, por troca) e junta os eventos novos ao histórico"""
    p = pasta(); os.makedirs(p, exist_ok=True)
    for k in ARQS:
        tmp = os.path.join(p, k + '.json.tmp')
        json.dump(E[k], open(tmp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        os.replace(tmp, os.path.join(p, k + '.json'))
    if E['_novos']:
        with open(os.path.join(p, 'eventos.jsonl'), 'a', encoding='utf-8') as f:
            for ev in E['_novos']: f.write(json.dumps(ev, ensure_ascii=False) + '\n')
        E['_novos'] = []


def novo(semente=1):
    """um estado vazio (o gerador e as provas partem daqui)"""
    return dict(relogio=dict(semente=semente, dia=1, bloco=2, eventos=0), lugares={}, gente={}, itens=dict(seq=0, itens={}, oseq=0, obras={}),
                turno=dict(n=1, aberto=dict(dia=1, bloco=2), dados=[], lutas=[], perguntas=[], respondidas=[], notas=[]), _novos=[])


# ---------- o tempo e o acaso do mundo ----------
def agora(E): return (E['relogio']['dia'] - 1) * M.BLOCOS_DIA + E['relogio']['bloco']        # blocos desde o começo do mundo
def estacao(E): return M.ESTACOES[((E['relogio']['dia'] - 1) % M.ANO) // M.ESTACAO]
def quando(E):
    r = E['relogio']; return f"Dia {r['dia']}, {M.BLOCOS[r['bloco']]} ({r['bloco'] * M.BLOCO_HORAS}h) · {estacao(E)}"


def sorte(E, chave):
    """o acaso do MUNDO (não o dado do jogador): sai da semente, do dia, do bloco e de uma chave. Mesma semente, mesmo mundo; nunca se rola de novo."""
    r = E['relogio']; h = hashlib.sha256(f"{r['semente']}|{r['dia']}|{r['bloco']}|{chave}".encode()).digest()
    return random.Random(int.from_bytes(h[:8], 'big'))


def eu(E):
    """o id do personagem do jogador"""
    return next((k for k, p in E['gente'].items() if p.get('jogador')), None)


# ---------- onde a pessoa está, e o arquivo de uma luta ----------
def fora(E, pid):
    """o id do ermo onde a pessoa está, se SAIU do lugar onde mora (a saída de caça ou de coleta, escrita em marca.caca); senão None"""
    s = (E['gente'][pid].get('marca') or {}).get('caca')
    return s['ermo'] if isinstance(s, dict) and s.get('ermo') in E['lugares'] else None


def onde(E, pid): return fora(E, pid) or E['gente'][pid]['lugar']          # onde o corpo está agora: no ermo da saída, ou no lugar onde mora
def em(E, lid): l = E['lugares'][lid]; return l.get('em', 'em ' + l['nome'])
def de(E, lid):
    """o lugar depois de "de", com a contração do artigo do nome: "da Vila de Prova", "do Mato", "de Pedra Rasa"""
    n = E['lugares'][lid]['nome']; art, _, resto = n.partition(' ')
    return {'a': 'da ', 'o': 'do ', 'as': 'das ', 'os': 'dos '}[art] + resto if art in ('a', 'o', 'as', 'os') and resto else 'de ' + n


def morte_diz(E, p):
    m = p.get('morte') or {}
    return f"morreu no Dia {m['dia']}, {em(E, m['onde'])}" if m.get('onde') in E['lugares'] else 'já morreu'


def de_morto(it):
    """esta peça solta ficou com o corpo de alguém que morreu? Devolve o id do morto (a marca `corpo`), True se só a história o diz (save antigo), ou None"""
    if not it.get('solto') or it.get('dono'): return None
    return it.get('corpo') or (True if 'ficou com o corpo de' in ''.join((it.get('historia') or [])[-1:]) else None)


def tantos(n, um, muitos=None):
    """o número com a palavra no singular ou no plural: "1 bloco", "3 blocos", "2 ações" (tantos(2, 'ação', 'ações'))"""
    return f"{n:g} {um if n == 1 else (muitos or um + 's')}"


# ---------- a luta aberta tranca o mundo ----------
def luta_aberta(E):
    """o arquivo (como o save o guarda) da luta que está aberta no caderno do turno, ou None"""
    return next((l['arq'] for l in E['turno'].get('lutas', []) if not l.get('fim')), None)


def luta_diz(E):
    """a frase da tranca (ou None, se não há luta aberta): há uma luta aberta, o mundo não anda, e é assim que ela acaba ou se solta"""
    arq = luta_aberta(E)
    if not arq: return None
    dono = next((k for k, p in E['gente'].items() if isinstance(p, dict) and isinstance((p.get('marca') or {}).get('caca'), dict) and p['marca']['caca'].get('luta') == arq), None)
    quem = f' quem={dono}' if dono and dono != eu(E) else ''
    if dono: acaba, solta = f'`caca.py luta "Nome: ordem"{quem}`', f'`caca.py larga "por quê"{quem}`'
    else: acaba, solta = f'`ato.py luta roda {arq} "Nome: ordem"`', f'`ato.py luta larga {arq} "por quê"`'
    return f"há uma luta aberta ({arq}): enquanto ela não acabar, nada mais anda no mundo. Para seguir a luta: {acaba}. Se o arquivo se perdeu ou a cena mudou, o Mestre a solta: {solta}."


def sem_luta(E):
    """recusa, com a frase, se há luta aberta no mundo: todo ato que grava chama isto ANTES de cobrar ou rolar qualquer coisa"""
    t = luta_diz(E)
    if t: sys.exit(t)


def _nota_da_luta(E, efeitos):
    """os efeitos são só a nota da saída de caça dizendo que ela está NAQUELA luta aberta? (é o que a caça escreve logo ao abrir a luta: não mexe em tempo, prata nem peça)"""
    abertas = [l['arq'] for l in E['turno'].get('lutas', []) if not l.get('fim')]
    return bool(efeitos) and all(isinstance(ef, (list, tuple)) and len(ef) == 5 and ef[0] == 'pessoa' and ef[2] == 'marca.caca' and ef[3] == 'poe' and isinstance(ef[4], dict)
                                 and ef[4].get('fase') == 'luta' and ef[4].get('luta') in abertas for ef in efeitos)


def presente(E, pid, o_que='agir aqui'):
    """a condição de todo ato da vila: a pessoa existe, está viva, está NO LUGAR ONDE MORA (sem saída aberta) e não há luta aberta no mundo. Senão, recusa com a frase. Devolve a pessoa."""
    p = E['gente'].get(pid) or sys.exit(f'não há a pessoa "{pid}"')
    if p['estado'] != 'vivo': sys.exit(f"{p['nome']} não age: {morte_diz(E, p)}")
    sem_luta(E)
    f = fora(E, pid)
    if f: sys.exit(f"{p['nome']} está fora, {em(E, f)} (a saída está aberta): não pode {o_que}. `caca.py ver` diz o que há à frente; `caca.py volta` fecha a saída.")
    return p


def arq_guarda(arq):
    """o caminho de um arquivo como fica escrito no save: relativo à pasta do save se está dentro dela (a pasta pode mudar de lugar), senão inteiro"""
    a = os.path.abspath(arq); p = os.path.abspath(pasta())
    return os.path.relpath(a, p) if a == p or a.startswith(p + os.sep) else a


def arq_abre(guardado): return guardado if os.path.isabs(guardado) else os.path.join(pasta(), guardado)       # o caminho de verdade do que o save guardou


# ---------- o gravador ----------
CAMPOS = dict(moedas='soma', pv='soma', fome='soma', sono='soma', cansaco='soma', nivel='soma', lugar='poe', estado='poe', grau_oficio='poe')
CONTAS = ('bichos', 'teto', 'coleta', 'coleta_teto', 'produz')          # os campos do lugar que são {nome: número de zero para cima}


def _erro(ef, porque): return f'efeito {json.dumps(ef, ensure_ascii=False)}: {porque}'
def _num(v): return isinstance(v, (int, float)) and not isinstance(v, bool)
def _int(v): return isinstance(v, int) and not isinstance(v, bool)


def bem_conhecido(b):
    """o que se carrega e se guarda em estoque: os bens da tabela e a matéria com categoria (tabelas_mundo: BENS, MATERIAS, MATERIA_ATE); a prata é à parte"""
    if b in M.BENS: return True
    n, c = M.le_materia(b)
    return n in M.MATERIAS and c is not None and c <= M.MATERIA_ATE


def _conta_erro(raiz, k, v):
    """o que uma conta do lugar aceita: (o texto do erro, ou None)"""
    if not _num(v) or v < 0: return f'"{raiz}.{k}" é um número de zero para cima (veio {json.dumps(v, ensure_ascii=False)})'
    if raiz in ('bichos', 'teto') and k not in TB.ESPECIES: return f'espécie desconhecida: "{k}"'
    if raiz == 'bichos' and int(v) != v: return f'a contagem de "{k}" é um número inteiro'
    if raiz in ('coleta', 'coleta_teto'):
        n, c = M.le_materia(k)
        if n not in M.MATERIAS or c is None or c > M.MATERIA_ATE: return f'matéria desconhecida: "{k}" (use nome:categoria, de 0 a {M.MATERIA_ATE}: metal:0, erva:1)'
    if raiz == 'produz' and k == 'prata': return 'prata não se produz: só nasce em evento "gera" ou "mestre"'
    return None


def _lugar_erro(E, raiz, sub, val):
    """o que um campo do lugar aceita num 'poe' (None: aceita)"""
    if raiz in CONTAS:
        d = {sub: val} if sub else val
        if not isinstance(d, dict): return f'"{raiz}" é uma conta: {{nome: quanto}}'
        return next((e for e in (_conta_erro(raiz, k, v) for k, v in d.items()) if e), None)
    if sub and raiz == 'preparo': return None if val is None or (_int(val) and 0 <= val < len(T.CATS)) else 'o preparo alcança uma categoria (0, Comum, em diante), ou nada'
    if raiz == 'alvo_pecas':                               # o alvo de peças da loja (mercado.py): {categoria: quantas peças ela quer ter na prateleira}
        d = {sub: val} if sub else val
        return None if isinstance(d, dict) and all(isinstance(k, str) and k.isdigit() and int(k) < len(T.CATS) and _int(v) and v >= 0 for k, v in d.items()) else 'o alvo de peças da loja é {categoria ("0", Comum, em diante): quantas peças ela quer ter na prateleira, de zero para cima}'
    if sub: return None
    if raiz == 'pop': return None if val is None or (_num(val) and val >= 0) else 'o povo é um número de zero para cima'
    if raiz == 'oficina': return None if val is None or (_int(val) and 0 <= val <= M.OFICINA_MAX) else f'a oficina vai de 0 a {M.OFICINA_MAX}, ou nada'
    if raiz == 'preparo': return None if isinstance(val, dict) and all(v is None or (_int(v) and 0 <= v < len(T.CATS)) for v in val.values()) else 'o preparo é {fogo, bigorna: a categoria que alcança}'
    if raiz == 'longe': return None if _int(val) and val >= 1 else 'os blocos de ida são 1 ou mais'
    if raiz == 'perigo': return None if _int(val) and 1 <= val <= M.PERIGO_MAX else f'o perigo vai de 1 a {M.PERIGO_MAX}'
    if raiz == 'vizinhos': return None if isinstance(val, list) and all(v in E['lugares'] for v in val) else 'os vizinhos são uma lista de lugares que existem'
    if raiz == 'cama': return None if isinstance(val, bool) else 'a cama é sim ou não'
    return None


def _morre(E, pid):
    """A MORTE, numa regra só: o morto não fica com nada. As peças e os núcleos dele caem SOLTOS onde ele morreu; as obras se desfazem; a carga e a prata ficam no
    estoque desse lugar. Quem foi junto na saída de outro deixa de estar nela; a saída de quem a comandava fica escrita, para a caça fazer as contas."""
    p = E['gente'][pid]; lid = onde(E, pid); l = E['lugares'][lid]; dia = E['relogio']['dia']
    p['morte'] = dict(dia=dia, bloco=E['relogio']['bloco'], onde=lid)
    for oid in [k for k, o in E['itens'].get('obras', {}).items() if o.get('quem') == pid]: del E['itens']['obras'][oid]
    for it in E['itens']['itens'].values():
        if it.get('dono') == pid:
            it['dono'] = None; it['uso'] = None; it['onde'] = lid; it['solto'] = True; it['corpo'] = pid      # solta, junto do corpo: `corpo` diz de quem era (sai quando a peça ganha dono ou vai para a prateleira)
            it.setdefault('historia', []).append(f"Dia {dia}: ficou com o corpo de {p['nome']} {em(E, lid)}")
    est = l.setdefault('estoque', {})
    for b, q in (p.get('carga') or {}).items():
        if _num(q) and q > 0: est[b] = est.get(b, 0) + q
    p['carga'] = {}
    if p['moedas'] > 0: est['prata'] = est.get('prata', 0) + p['moedas']; p['moedas'] = 0
    s = (p.get('marca') or {}).get('caca')
    if isinstance(s, dict) and s.get('de'): p['marca'].pop('caca')


def _nasce_pessoa(E, ef):
    if len(ef) != 4 or not isinstance(ef[2], str) or not isinstance(ef[3], dict): return _erro(ef, "use ['pessoa', 'nasce', id, registro]")
    pid, r = ef[2], ef[3]
    if not pid or pid == 'nasce' or pid in E['gente']: return _erro(ef, f'já há a pessoa "{pid}" (ou o id não serve)')
    if not r.get('nome') or not isinstance(r['nome'], str): return _erro(ef, 'a pessoa pede um nome')
    if not _int(r.get('nivel')) or r['nivel'] < 1: return _erro(ef, 'a pessoa pede um nível (1 ou mais)')
    at = r.get('atributos')
    if not isinstance(at, dict) or set(at) != set(T.ATRIBUTOS) or not all(_num(v) and v > 0 for v in at.values()): return _erro(ef, f'a pessoa pede os seis atributos ({", ".join(T.ATRIBUTOS)})')
    if r.get('lugar') not in E['lugares']: return _erro(ef, f'não há o lugar "{r.get("lugar")}"')
    of = r.get('grau_oficio', 'diarista')
    if of not in M.SALARIO: return _erro(ef, f'grau de ofício desconhecido: "{of}" (os que há: {", ".join(M.SALARIO)})')
    ma = r.get('maestria') or {}; tr = r.get('treino') or {}; ca = r.get('carga') or {}; mo = r.get('moedas', 0)
    if not isinstance(ma, dict) or any((k not in T.FAMILIAS and k not in M.OFICIOS) or v not in T.MAESTRIAS for k, v in ma.items()): return _erro(ef, 'maestria fora da tabela (arma ou ofício: 0, 2, 4, 6 ou 8)')
    if not isinstance(tr, dict) or any((k not in T.FAMILIAS and k not in M.OFICIOS) or not _num(v) or v < 0 for k, v in tr.items()): return _erro(ef, 'treino fora da tabela (arma ou ofício: blocos)')
    if not isinstance(ca, dict) or any(not _num(v) or v <= 0 for v in ca.values()): return _erro(ef, 'a carga é {bem: quanto}, acima de zero')
    if not _int(mo) or mo < 0: return _erro(ef, 'a prata é um número inteiro de zero para cima')
    if r.get('jogador') and any(q.get('jogador') for q in E['gente'].values()): return _erro(ef, 'já há um personagem do jogador')
    ruins = [k for k in r if k not in ('nome', 'nivel', 'atributos', 'lugar', 'grau_oficio', 'maestria', 'treino', 'carga', 'moedas', 'jogador', 'marca', 'sobre')]
    if ruins: return _erro(ef, f'a pessoa não tem o campo "{ruins[0]}"')
    p = dict(nome=r['nome'], lugar=r['lugar'], grau_oficio=of, nivel=r['nivel'], atributos={a: at[a] for a in T.ATRIBUTOS}, maestria=dict(ma), treino=dict(tr), moedas=mo,
             corpo={m: 0 for m in M.MEDIDORES}, pv=0, feridas=[], estado='vivo', marca=copy.deepcopy(r.get('marca') or {}), carga=dict(ca))
    p['pv'] = pv_max(p)
    if r.get('jogador'): p['jogador'] = True
    if r.get('sobre'): p['sobre'] = str(r['sobre'])
    E['gente'][pid] = p


def _nasce_lugar(E, ef):
    if len(ef) != 4 or not isinstance(ef[2], str) or not isinstance(ef[3], dict): return _erro(ef, "use ['lugar', 'nasce', id, registro]")
    lid, r = ef[2], copy.deepcopy(ef[3])
    if not lid or lid == 'nasce' or lid in E['lugares']: return _erro(ef, f'já há o lugar "{lid}" (ou o id não serve)')
    if not r.get('nome') or not isinstance(r['nome'], str): return _erro(ef, 'o lugar pede um nome')
    est = r.setdefault('estoque', {})
    if not isinstance(est, dict) or any(not _num(v) or v < 0 for v in est.values()): return _erro(ef, 'o estoque é {bem: quanto}, de zero para cima')
    r.setdefault('tipo', 'ermo')
    for k, v in r.items():
        if k in ('nome', 'em', 'tipo', 'habitat', 'sobre'):
            if not isinstance(v, str): return _erro(ef, f'"{k}" é texto')
        elif k != 'estoque':
            e = _lugar_erro(E, k, None, v)
            if e: return _erro(ef, e)
    E['lugares'][lid] = r


def _um(E, ef):
    """aplica UM efeito em E (que pode ser uma cópia de ensaio). Devolve None, ou o texto do erro."""
    if not isinstance(ef, (list, tuple)) or not ef: return _erro(ef, 'efeito vazio')
    v = ef[0]
    if v == 'relogio':
        if len(ef) != 2 or not _int(ef[1]) or ef[1] < 1: return _erro(ef, 'o tempo anda 1 bloco ou mais')
        t = agora(E) + ef[1]; E['relogio']['dia'], E['relogio']['bloco'] = t // M.BLOCOS_DIA + 1, t % M.BLOCOS_DIA; return
    if v == 'pessoa' and len(ef) > 1 and ef[1] == 'nasce': return _nasce_pessoa(E, ef)
    if v == 'pessoa':
        if len(ef) != 5: return _erro(ef, "use ['pessoa', id, campo, 'soma'|'poe', valor]")
        _, pid, campo, op, val = ef; p = E['gente'].get(pid) if isinstance(pid, str) else None
        if not p: return _erro(ef, f'não há a pessoa "{pid}"')
        if not isinstance(campo, str): return _erro(ef, 'o campo é um nome')
        raiz, _, sub = campo.partition('.')
        if raiz == 'carga':
            if not sub or op != 'soma' or not _int(val): return _erro(ef, "a carga muda por ['pessoa', id, 'carga.BEM', 'soma', número inteiro]")
            if not bem_conhecido(sub): return _erro(ef, f'não se carrega "{sub}" (carregam-se: {", ".join(M.BENS)}; e a matéria com a categoria, de 0 a {M.MATERIA_ATE}: metal:0, couro:1...)')
            d = p.setdefault('carga', {}); q = d.get(sub, 0) + val
            if q < 0: return _erro(ef, f'{p["nome"]} só carrega {d.get(sub, 0)} de {sub}')
            if q: d[sub] = q
            else: d.pop(sub, None)
            return
        if raiz in ('treino', 'maestria', 'marca'):
            if not sub: return _erro(ef, f'"{raiz}" pede o nome depois do ponto (treino.espada)')
            if raiz != 'marca' and sub not in T.FAMILIAS and sub not in M.OFICIOS: return _erro(ef, f'arma ou ofício desconhecido: "{sub}"')
            if raiz != 'marca' and not _num(val): return _erro(ef, f'"{campo}" é um número')
            d = p.setdefault(raiz, {})
            if op == 'soma':
                if not _num(val) or not _num(d.get(sub, 0)): return _erro(ef, f'"{campo}" não é número: não se soma')
                d[sub] = d.get(sub, 0) + val
            elif op == 'poe': d[sub] = val
            else: return _erro(ef, 'a operação é "soma" ou "poe"')
            if raiz == 'maestria' and d[sub] not in T.MAESTRIAS: return _erro(ef, f'maestria fora da tabela: {d[sub]}')
            return
        if campo not in CAMPOS: return _erro(ef, f'campo desconhecido: "{campo}" (os que existem: {", ".join(CAMPOS)}, treino.ARMA, maestria.ARMA, marca.X, carga.BEM)')
        if op != CAMPOS[campo]: return _erro(ef, f'"{campo}" só aceita "{CAMPOS[campo]}"')
        if CAMPOS[campo] == 'soma' and not _num(val): return _erro(ef, f'"{campo}" soma um número')
        if campo == 'lugar':
            if val not in E['lugares']: return _erro(ef, f'não há o lugar "{val}"')
            p['lugar'] = val
        elif campo == 'estado':
            if val not in M.ESTADOS: return _erro(ef, f'estado desconhecido: "{val}"')
            if val == 'morto' and p['estado'] != 'morto': _morre(E, pid)
            if val == 'vivo': p.pop('morte', None)
            p['estado'] = val
        elif campo == 'grau_oficio':
            if val not in M.SALARIO: return _erro(ef, f'grau de ofício desconhecido: "{val}" (os que há: {", ".join(M.SALARIO)})')
            p['grau_oficio'] = val
        elif campo in M.MEDIDORES: p['corpo'][campo] = max(0, min(M.MED_MAX, p['corpo'][campo] + val))
        elif campo == 'pv': p['pv'] = max(0, min(pv_max(p), p['pv'] + val))
        elif campo == 'moedas':
            if not _int(val): return _erro(ef, 'a prata é inteira')
            if p['moedas'] + val < 0: return _erro(ef, f'{p["nome"]} tem {p["moedas"]} de prata e não paga {-val}')
            p['moedas'] += val
        else: p[campo] += val
        return
    if v == 'ferida':
        p = E['gente'].get(ef[1]) if len(ef) > 2 and isinstance(ef[1], str) else None
        if not p: return _erro(ef, 'não há essa pessoa')
        if ef[2] == 'abre' and len(ef) == 5:
            if ef[3] not in T.PARTES: return _erro(ef, f'parte desconhecida: "{ef[3]}"')
            p['feridas'].append(dict(parte=ef[3], grave=bool(ef[4]), dia=E['relogio']['dia'], repouso=0)); return
        if ef[2] == 'repousa' and len(ef) == 4 and _num(ef[3]):
            for f in p['feridas']: f['repouso'] += ef[3]
            return
        if ef[2] == 'sara' and len(ef) == 4:
            if not _int(ef[3]) or not 0 <= ef[3] < len(p['feridas']): return _erro(ef, 'não há essa ferida')
            p['feridas'].pop(ef[3]); return
        return _erro(ef, "use ['ferida', id, 'abre', parte, grave], ['ferida', id, 'repousa', n] ou ['ferida', id, 'sara', indice]")
    if v == 'lugar' and len(ef) > 1 and ef[1] == 'nasce': return _nasce_lugar(E, ef)
    if v == 'lugar':
        if len(ef) != 5 or ef[3] not in ('soma', 'poe') or not isinstance(ef[2], str): return _erro(ef, "use ['lugar', id, campo ou campo.sub, 'soma'|'poe', valor]")
        l = E['lugares'].get(ef[1]) if isinstance(ef[1], str) else None
        if not l: return _erro(ef, f'não há o lugar "{ef[1]}"')
        raiz, _, sub = ef[2].partition('.')
        if raiz in ('estoque', 'nome'): return _erro(ef, f'"{raiz}" não se muda por aqui (o estoque tem o verbo dele)')
        if sub and not isinstance(l.get(raiz, {}), dict): return _erro(ef, f'"{raiz}" não tem partes')
        d = l.setdefault(raiz, {}) if sub else l; k = sub or raiz
        if ef[3] == 'poe':
            e = _lugar_erro(E, raiz, sub, ef[4])
            if e: return _erro(ef, e)
            d[k] = copy.deepcopy(ef[4])
        else:
            if not _num(d.get(k, 0)) or not _num(ef[4]): return _erro(ef, f'"{ef[2]}" não é número')
            q = d.get(k, 0) + ef[4]
            if q < 0: return _erro(ef, f'{l["nome"]} só tem {d.get(k, 0)} de {ef[2]}')
            e = _lugar_erro(E, raiz, sub, q)
            if e: return _erro(ef, e)
            d[k] = q
        return
    if v == 'obra':
        O = E['itens'].setdefault('obras', {})
        if len(ef) == 3 and ef[1] == 'abre':
            o = copy.deepcopy(ef[2])
            if not isinstance(o, dict) or o.get('quem') not in E['gente']: return _erro(ef, 'a obra pede um registro com "quem" (uma pessoa que existe)')
            if o.get('lugar') not in E['lugares']: return _erro(ef, 'a obra pede o "lugar" onde está a bancada (um lugar que existe)')
            if not _num(o.get('pede')) or o['pede'] < 1 or not _num(o.get('blocos', 0)) or not 0 <= o.get('blocos', 0) <= o['pede']: return _erro(ef, 'a obra pede "pede" (blocos, 1 ou mais) e "blocos" entre zero e isso')
            E['itens']['oseq'] = E['itens'].get('oseq', 0) + 1; o['id'] = f"o{E['itens']['oseq']:04d}"; o.setdefault('blocos', 0); o.setdefault('dia', E['relogio']['dia']); O[o['id']] = o; return
        o = O.get(ef[1]) if len(ef) > 2 and isinstance(ef[1], str) else None
        if not o: return _erro(ef, 'não há essa obra')
        if len(ef) == 3 and ef[2] == 'fecha': del O[ef[1]]; return
        if len(ef) == 5 and ef[3] in ('soma', 'poe') and ef[2] in ('blocos', 'pede'):
            q = o.get(ef[2], 0) + ef[4] if ef[3] == 'soma' and _num(ef[4]) else ef[4]
            if not _num(q) or q < 0 or (ef[2] == 'blocos' and q > o.get('pede', q)) or (ef[2] == 'pede' and (q < 1 or q < o.get('blocos', 0))): return _erro(ef, 'os blocos da obra ficam entre zero e o que ela pede')
            o[ef[2]] = q; return
        if len(ef) == 5 and ef[3] == 'poe' and ef[2] in ('id', 'quem', 'lugar', 'tipo', 'materia', 'nucleo', 'item', 'para'):
            c, x = ef[2], ef[4]
            certo = (c == 'lugar' and x in E['lugares']) or (c == 'materia' and isinstance(x, dict) and all(bem_conhecido(k) and _num(q) and q >= 0 for k, q in x.items())) \
                or (c == 'nucleo' and (x is None or E['itens']['itens'].get(x, {}).get('tipo') == 'nucleo')) or (c == 'item' and x in E['itens']['itens']) or (c == 'para' and x in E['gente'])
            if not certo: return _erro(ef, f'a obra não aceita "{c}" = {json.dumps(x, ensure_ascii=False)} (o lugar, a matéria, o núcleo, a peça e a pessoa têm de existir; quem a faz e o tipo dela não mudam)')
            o[c] = copy.deepcopy(x); return
        if len(ef) == 5 and ef[3] == 'soma' and _num(ef[4]) and _num(o.get(ef[2], 0)): o[ef[2]] = o.get(ef[2], 0) + ef[4]; return
        if len(ef) == 5 and ef[3] == 'poe': o[ef[2]] = ef[4]; return
        return _erro(ef, "use ['obra', 'abre', registro], ['obra', id, campo, 'soma'|'poe', valor] ou ['obra', id, 'fecha']")
    if v == 'estoque':
        if len(ef) != 5 or ef[3] != 'soma' or not _num(ef[4]) or not isinstance(ef[2], str): return _erro(ef, "use ['estoque', lugar, bem, 'soma', número]")
        l = E['lugares'].get(ef[1]) if isinstance(ef[1], str) else None
        if not l: return _erro(ef, f'não há o lugar "{ef[1]}"')
        if ef[2] == 'prata' and not _int(ef[4]): return _erro(ef, 'a prata é inteira')
        q = l['estoque'].get(ef[2], 0) + ef[4]
        if q < 0: return _erro(ef, f'{l["nome"]} só tem {l["estoque"].get(ef[2], 0)} de {ef[2]}')
        l['estoque'][ef[2]] = q; return
    if v == 'item' and len(ef) == 3 and ef[1] == 'nasce':
        it = copy.deepcopy(ef[2])
        if not isinstance(it, dict) or it.get('tipo') not in ('arma', 'armadura', 'escudo', 'nucleo') or 'dur' not in it or 'cat' not in it or not it.get('nome'): return _erro(ef, 'o registro tem de sair do itens.item() (ou ser um núcleo: tipo, cat, nome, dur)')
        if not _int(it['cat']) or not 0 <= it['cat'] < len(T.CATS): return _erro(ef, f'categoria fora da tabela: {it["cat"]} (vai de 0, Comum, a {len(T.CATS) - 1})')
        if not (isinstance(it['dur'], list) and len(it['dur']) == 2 and all(_int(x) for x in it['dur']) and 0 <= it['dur'][0] <= it['dur'][1]): return _erro(ef, 'a durabilidade é [quanto tem, quanto cabe]')
        if it.get('dono') is not None and it['dono'] not in E['gente']: return _erro(ef, f'não há a pessoa "{it["dono"]}"')
        if it.get('dono') is not None and E['gente'][it['dono']]['estado'] != 'vivo': return _erro(ef, f'{E["gente"][it["dono"]]["nome"]} morreu: não recebe peça')
        if it.get('onde') is not None and it['onde'] not in E['lugares']: return _erro(ef, f'não há o lugar "{it["onde"]}"')
        if it.get('dono') is not None and it.get('onde') is not None: return _erro(ef, 'a peça nasce com dono OU num lugar, não os dois')
        if it.get('dono') is None and it.get('onde') is None: return _erro(ef, 'a peça nasce com dono (dono=) ou num lugar (onde=): solta no nada, não existe')
        if it.get('solto') and it.get('dono') is not None: return _erro(ef, 'peça com dono não está solta')
        if not it.get('solto'): it.pop('solto', None)
        E['itens']['seq'] += 1; it['id'] = f"i{E['itens']['seq']:04d}"; it['uso'] = None; E['itens']['itens'][it['id']] = it; return
    if v == 'item' and len(ef) == 3 and ef[2] == 'some':
        if ef[1] not in E['itens']['itens']: return _erro(ef, f'não há o item "{ef[1]}" no Livro de Itens')
        del E['itens']['itens'][ef[1]]; return
    if v == 'item':
        if len(ef) != 5: return _erro(ef, "use ['item', id, campo, 'poe'|'soma', valor], ['item', 'nasce', registro] ou ['item', id, 'some']")
        it = E['itens']['itens'].get(ef[1]) if isinstance(ef[1], str) else None
        if not it: return _erro(ef, f'não há o item "{ef[1]}" no Livro de Itens')
        _, _, campo, op, val = ef
        if campo == 'dono' and op == 'poe':
            if val is not None and val not in E['gente']: return _erro(ef, f'não há a pessoa "{val}"')
            if val is not None and E['gente'][val]['estado'] != 'vivo': return _erro(ef, f'{E["gente"][val]["nome"]} morreu: não recebe peça')
            it['dono'] = val; it['uso'] = None
            if val is not None: it['onde'] = None; it.pop('solto', None); it.pop('corpo', None)
            return
        if campo == 'onde' and op == 'poe':
            if val is not None and val not in E['lugares']: return _erro(ef, f'não há o lugar "{val}"')
            if val is not None and it.get('dono'): return _erro(ef, 'peça com dono não fica largada num lugar: tire o dono antes')
            it['onde'] = val
            if val is None: it.pop('solto', None); it.pop('corpo', None)
            return
        if campo == 'solto' and op == 'poe':
            if val and (it.get('dono') or it.get('onde') is None): return _erro(ef, 'só fica solta (caída no chão) a peça sem dono que está num lugar')
            if val: it['solto'] = True
            else: it.pop('solto', None); it.pop('corpo', None)
            return
        if campo == 'sob_medida' and op == 'poe':
            if val is not None and not (isinstance(val, dict) and val.get('dono') and _num(val.get('grau', 0)) and T.SOB_MEDIDA_GRAUS[0] <= val.get('grau', 0) <= T.SOB_MEDIDA_GRAUS[1]): return _erro(ef, 'o sob medida é {dono, grau de 1 a 4}, ou nada')
            if it['tipo'] == 'nucleo': return _erro(ef, 'núcleo não se ajusta')
            it['sob_medida'] = val; return
        if campo == 'historia' and op == 'junta': it.setdefault('historia', []).append(str(val)); return
        if campo == 'nome' and op == 'poe' and val: it['nome'] = str(val); return
        if campo == 'uso' and op == 'poe':
            if val not in (None,) + PARTES_VESTE: return _erro(ef, f'uso desconhecido: "{val}" (arma, arma2, escudo, veste ou nada)')
            if val and not it.get('dono'): return _erro(ef, 'peça sem dono não se veste')
            tipo_certo = dict(arma='arma', arma2='arma', escudo='escudo', veste='armadura')
            if val and it['tipo'] != tipo_certo[val]: return _erro(ef, f'{it["nome"]} é {it["tipo"]}: não vai em "{val}"')
            it['uso'] = val; return
        if campo == 'dur' and op == 'soma' and _num(val):
            if it['tipo'] == 'nucleo': return _erro(ef, 'núcleo não gasta nem se conserta')
            it['dur'][0] = max(0, min(it['dur'][1], it['dur'][0] + int(val))); return
        return _erro(ef, 'no item muda-se: dono, uso, onde, solto, sob_medida, nome (poe) · dur (soma) · historia (junta)')
    return _erro(ef, f'verbo desconhecido: "{v}" (os que existem: relogio, pessoa, ferida, estoque, lugar, item, obra)')


def aplica(E, tipo, efeitos, onde=None, quem=(), texto=''):
    """A ÚNICA PORTA. Ensaia todos os efeitos numa cópia; se um falha, NADA muda e o erro sai com o motivo.
    O evento cujos efeitos não mudam nada (somar no que já está no teto, pôr o que já está posto) não aconteceu: não entra no registro, e devolve None.
    COM UMA LUTA ABERTA no mundo, só entram a luta que volta ao estado, a mão do Mestre e a nota da saída de caça que está naquela luta (tabelas_mundo.NA_LUTA)."""
    if tipo not in M.EVENTOS: sys.exit(f'evento desconhecido: "{tipo}" (os que existem: {", ".join(M.EVENTOS)})')
    if not efeitos: sys.exit(f'evento "{tipo}" sem efeito: recusado. O que não muda número não aconteceu.')
    if tipo not in M.NA_LUTA and luta_aberta(E) and not _nota_da_luta(E, efeitos): sys.exit(luta_diz(E))
    ensaio = {k: copy.deepcopy(E[k]) for k in ARQS}
    for ef in efeitos:
        if tipo not in M.NASCE and isinstance(ef, (list, tuple)) and len(ef) > 1 and ef[0] in ('pessoa', 'lugar') and ef[1] == 'nasce':
            sys.exit(f'evento "{tipo}" recusado, nada mudou. {_erro(ef, "gente e lugar só nascem em evento " + " ou ".join(M.NASCE))}')
        try: e = _um(ensaio, ef)
        except (TypeError, KeyError, IndexError, AttributeError, ValueError) as x: e = _erro(ef, f'efeito malformado ({type(x).__name__})')
        if e: sys.exit(f'evento "{tipo}" recusado, nada mudou. {e}')
    if all(ensaio[k] == E[k] for k in ARQS): return None
    ev = dict(id=E['relogio']['eventos'] + 1, dia=E['relogio']['dia'], bloco=E['relogio']['bloco'], tipo=tipo, onde=onde, quem=list(quem), efeitos=[list(x) for x in efeitos], texto=texto)
    for k in ARQS: E[k] = ensaio[k]
    E['relogio']['eventos'] = ev['id']; E['_novos'].append(ev)
    return ev


# ---------- ler o estado (ninguém guarda cópia: tudo sai daqui) ----------
def pv_max(p): return T.pv_max(p['atributos']['Vigor'], p['nivel'])


def pecas(E, pid):
    """{'arma': item, 'arma2': item, 'escudo': item, 'veste': [itens]} do que a pessoa veste agora (sai do Livro de Itens)"""
    out = dict(arma=None, arma2=None, escudo=None, veste=[])
    for it in E['itens']['itens'].values():
        if it.get('dono') == pid and it.get('uso'):
            if it['uso'] == 'veste': out['veste'].append(it)
            else: out[it['uso']] = it
    return out


def lutador(E, pid, **mais):
    """a pessoa pronta para o pessoas.ficha e o luta.nova: quem é, o que veste hoje, o PV, as feridas e a pena do corpo"""
    import corpo
    p = E['gente'][pid]; eq = pecas(E, pid)
    d = dict(id=pid, nome=p['nome'], nivel=p['nivel'], atributos=dict(p['atributos']), maestria=dict(p.get('maestria', {})), pv=p['pv'],
             feridas=[[f['parte'], f['grave']] for f in p['feridas']], pena=corpo.pena(p), fol_menos=corpo.folego_menos(p),
             equip=copy.deepcopy(dict(arma=eq['arma'], arma2=eq['arma2'], escudo=eq['escudo'], armaduras=eq['veste'])))    # cópia: a luta não mexe no Livro
    d.update(mais)
    return d


def valida(E):
    """os invariantes: o que nunca pode ser verdade. Devolve a lista dos problemas (vazia: tudo certo). Nunca quebra: o que tem o tipo errado é um problema da lista."""
    P = []
    def tenta(nome, f):
        try: f()
        except Exception as x: P.append(f'{nome}: registro torto, não dá para conferir ({type(x).__name__}: {x})')
    def relogio():
        r = E['relogio']
        if not (r['dia'] >= 1 and 0 <= r['bloco'] < M.BLOCOS_DIA): P.append(f'relógio fora: dia {r["dia"]}, bloco {r["bloco"]}')
    tenta('o relógio', relogio)
    if sum(1 for p in E['gente'].values() if isinstance(p, dict) and p.get('jogador')) > 1: P.append('há mais de um personagem do jogador')
    L = E['itens']['itens']; O = E['itens'].get('obras', {})
    def pessoa(pid, p):
        n = p.get('nome', pid)
        if p['lugar'] not in E['lugares']: P.append(f'{n} está num lugar que não existe: {p["lugar"]}')
        if not _int(p['moedas']) or p['moedas'] < 0: P.append(f'{n} tem prata errada: {p["moedas"]}')
        if p['estado'] not in M.ESTADOS: P.append(f'{n} tem estado desconhecido: {p["estado"]}')
        if not 0 <= p['pv'] <= pv_max(p): P.append(f'{n} tem PV fora da faixa: {p["pv"]} de {pv_max(p)}')
        if p['estado'] == 'vivo' and p['pv'] <= 0: P.append(f'{n} consta entre os vivos com PV zero')
        for m in M.MEDIDORES:
            if not 0 <= p['corpo'][m] <= M.MED_MAX: P.append(f'{n} tem {m} fora da faixa: {p["corpo"][m]}')
        for b, q in (p.get('carga') or {}).items():
            if not _int(q) or q < 0: P.append(f'{n} carrega quantidade errada de {b}: {q}')
            if not bem_conhecido(b): P.append(f'{n} carrega o que não existe: "{b}"')
        if p.get('grau_oficio', 'diarista') not in M.SALARIO: P.append(f'{n} tem grau de ofício desconhecido: {p.get("grau_oficio")}')
        for k, v in (p.get('maestria') or {}).items():
            if v not in T.MAESTRIAS: P.append(f'{n} tem maestria fora da tabela em {k}: {v}')
        usos = [it.get('uso') for it in L.values() if isinstance(it, dict) and it.get('dono') == pid and it.get('uso') in ('arma', 'arma2', 'escudo')]
        for u in set(usos):
            if usos.count(u) > 1: P.append(f'{n} tem duas peças em "{u}"')
        s = (p.get('marca') or {}).get('caca')
        if p['estado'] == 'morto':
            if p['moedas'] or p.get('carga'): P.append(f'{n} morreu e ainda tem prata ou carga (quem morre não fica com nada)')
            if s is not None: P.append(f'{n} morreu com a saída aberta: `caca.py volta quem={pid}` faz as contas e fecha (ou `caca.py larga quem={pid}`)')
        if s is not None:
            if not isinstance(s, dict) or s.get('ermo') not in E['lugares']: P.append(f'{n} tem a saída (marca.caca) torta: não diz um ermo que existe'); return
            if s.get('de') is not None:
                d = E['gente'].get(s['de']); sd = (d.get('marca') or {}).get('caca') if isinstance(d, dict) else None
                if not isinstance(sd, dict) or pid not in (sd.get('com') or []): P.append(f'{n} foi junto numa saída que não existe mais (marca.caca)')
            else:
                if s.get('fase') not in ('procura', 'encontro', 'luta') or not _int(s.get('restam')) or s['restam'] < 0 or s.get('casa') not in E['lugares'] or not isinstance(s.get('com', []), list):
                    P.append(f'{n} tem a saída (marca.caca) torta')
                elif s['fase'] == 'encontro' and not (isinstance(s.get('encontro'), dict) and s['encontro'].get('especie') in TB.ESPECIES and _int(s['encontro'].get('n')) and s['encontro']['n'] >= 1):
                    P.append(f'{n} tem um bicho à frente que a saída não descreve (marca.caca)')
                elif s['fase'] == 'luta' and not isinstance(s.get('luta'), str): P.append(f'{n} está em luta de caça sem o arquivo dela (marca.caca)')
    for pid, p in E['gente'].items(): tenta(f'a pessoa {pid}', lambda: pessoa(pid, p))
    def item_(iid, it):
        n = f'{it.get("nome", "?")} ({iid})'; dono = it.get('dono')
        if it.get('tipo') not in ('arma', 'armadura', 'escudo', 'nucleo'): P.append(f'{n} tem tipo desconhecido: {it.get("tipo")}')
        if not _int(it['cat']) or not 0 <= it['cat'] < len(T.CATS): P.append(f'{n} tem categoria fora da tabela: {it["cat"]}')
        if dono is not None and dono not in E['gente']: P.append(f'{n} tem dono que não existe: {dono}')
        if it.get('uso') and not dono: P.append(f'{n} está em uso sem dono')
        if dono in E['gente'] and E['gente'][dono]['estado'] == 'morto': P.append(f'{n} ' + ('está em uso com alguém que morreu' if it.get('uso') else 'é de alguém que morreu (quem morre não fica com nada)'))
        if not 0 <= it['dur'][0] <= it['dur'][1]: P.append(f'{n} tem durabilidade fora da faixa')
        if it.get('onde') is not None and it['onde'] not in E['lugares']: P.append(f'{n} está num lugar que não existe: {it["onde"]}')
        if it.get('onde') is not None and dono: P.append(f'{n} tem dono e está largada num lugar ao mesmo tempo')
        if it.get('onde') is None and dono is None: P.append(f'{n} não tem dono nem lugar: não está em parte nenhuma')
        if it.get('solto') and (dono or it.get('onde') is None): P.append(f'{n} consta no chão (sem dono) e tem dono, ou não tem lugar')
        if it.get('uso') and it.get('uso') not in PARTES_VESTE: P.append(f'{n} tem uso desconhecido: {it["uso"]}')
        if it.get('tipo') == 'nucleo' and (it['dur'][0] != it['dur'][1] or it.get('uso')): P.append(f'{n} é núcleo e está gasto ou em uso')
    for iid, it in L.items(): tenta(f'o item {iid}', lambda: item_(iid, it))
    def obra(oid, o):
        if o.get('quem') not in E['gente'] or E['gente'][o['quem']]['estado'] == 'morto': P.append(f'a obra {oid} é de alguém que não existe ou morreu')
        if o.get('lugar') not in E['lugares']: P.append(f'a obra {oid} está num lugar que não existe: {o.get("lugar")}')
        if not _num(o.get('pede')) or o['pede'] < 1 or not _num(o.get('blocos')) or not 0 <= o['blocos'] <= o['pede']: P.append(f'a obra {oid} tem os blocos fora da conta: {o.get("blocos")} de {o.get("pede")}')
        if o.get('tipo') not in ('forjar', 'ajustar'): P.append(f'a obra {oid} tem tipo desconhecido: {o.get("tipo")}')
        if o.get('nucleo') is not None:
            nu = L.get(o['nucleo'])
            if not isinstance(nu, dict) or nu.get('tipo') != 'nucleo': P.append(f'a obra {oid} pede um núcleo que não está no Livro de Itens: {o["nucleo"]}')
            elif nu.get('dono') != o.get('quem'): P.append(f'o núcleo da obra {oid} não está na mão de quem forja')
        if o.get('tipo') == 'ajustar' and o.get('item') not in L: P.append(f'o ajuste {oid} é de uma peça que não está no Livro de Itens')
        for b, q in (o.get('materia') or {}).items():
            if not _num(q) or q < 0: P.append(f'a obra {oid} tem matéria errada: {q} de {b}')
    for oid, o in O.items(): tenta(f'a obra {oid}', lambda: obra(oid, o))
    def lugar(lid, l):
        n = l.get('nome', lid)
        for b, q in l['estoque'].items():
            if not _num(q) or q < 0: P.append(f'{n} tem estoque errado de {b}: {q}')
        for campo, teto in (('bichos', 'teto'), ('coleta', 'coleta_teto')):
            for b, q in (l.get(campo) or {}).items():
                e = _conta_erro(campo, b, q)
                if e: P.append(f'{n}: {e}'); continue
                t = (l.get(teto) or {}).get(b)
                if _num(t) and q > t: P.append(f'{n} tem mais {b} do que cabe: {q:g} de {t:g}')
            for b, q in (l.get(teto) or {}).items():
                e = _conta_erro(teto, b, q)
                if e: P.append(f'{n}: {e}')
        for campo in ('pop', 'oficina', 'preparo', 'longe', 'perigo', 'vizinhos', 'produz', 'alvo_pecas'):
            if campo in l:
                e = _lugar_erro(E, campo, None, l[campo])
                if e: P.append(f'{n}: "{campo}" errado ({json.dumps(l[campo], ensure_ascii=False)[:60]}): {e}')
    for lid, l in E['lugares'].items(): tenta(f'o lugar {lid}', lambda: lugar(lid, l))
    return P


if __name__ == '__main__':
    import signal; hasattr(signal, 'SIGPIPE') and signal.signal(signal.SIGPIPE, signal.SIG_DFL)      # a saída cortada (`| head`) acaba o comando calada, sem erro de programa: tudo já foi gravado antes de falar
    a = sys.argv[1:]
    if a[:1] == ['valida']:
        P = valida(carrega()); print('\n'.join(P) if P else 'o estado está inteiro.'); sys.exit(1 if P else 0)
    elif a[:1] == ['eventos']:
        arq = os.path.join(pasta(), 'eventos.jsonl'); n = int(a[1]) if len(a) > 1 and a[1].isdigit() else 15
        for l in (open(arq, encoding='utf-8').read().splitlines()[-n:] if os.path.exists(arq) else []):
            ev = json.loads(l); print(f"#{ev['id']} Dia {ev['dia']}, {M.BLOCOS[ev['bloco']]} · {ev['tipo']}" + (f" · {ev['texto']}" if ev['texto'] else '') + f" · {tantos(len(ev['efeitos']), 'efeito')}")
    elif a[:1] == ['pessoa'] and len(a) > 1:
        E = carrega(); p = E['gente'].get(a[1]) or sys.exit(f'não há a pessoa "{a[1]}"')
        import pessoas, corpo
        from itens import rotulo
        if p['estado'] != 'vivo':                           # do morto só se diz que morreu (e onde): não tem ficha de luta, nem fome, nem forças, nem peça
            print(f"{p['nome']}, nível {p['nivel']}: {morte_diz(E, p)}. Quem morreu não fica com nada: o que era de {p['nome']} caiu ali."); sys.exit()
        print(pessoas.linha(pessoas.ficha(lutador(E, a[1]))))
        feridas = ', '.join(f"{f['parte']}{' (grave)' if f['grave'] else ''}, do Dia {f['dia']}" for f in p['feridas']) or 'nenhuma'
        print(f"  corpo: {corpo.diz(p)} · feridas: {feridas} · prata: {p['moedas']} · {em(E, onde(E, a[1]))}")
        if p.get('carga'): print('  carga: ' + ', '.join(f'{q:g} de {b}' for b, q in p['carga'].items()))
        usos = dict(arma='na mão', arma2='de reserva', escudo='no braço', veste='no corpo')
        for i, it in E['itens']['itens'].items():
            if it.get('dono') == a[1]: print(f"  {i} {rotulo(it, str(it['dur'][0]) + '/' + str(it['dur'][1]))}" + (f" · em uso, {usos.get(it['uso'], it['uso'])}" if it.get('uso') else ' · na guarda'))
    elif a[:1] == ['lugar'] and len(a) > 1:
        E = carrega(); l = E['lugares'].get(a[1]) or sys.exit(f'não há o lugar "{a[1]}" (os que há: {", ".join(E["lugares"])})')
        from itens import FEM, rotulo
        def bem(b): n, c = M.le_materia(b); return b if c is None or not 0 <= c < len(T.CATS) else f"{n} {(FEM if n.endswith('a') else T.CATS)[c]}"
        mil = lambda x: f'{int(x):,}'.replace(',', '.') if float(x).is_integer() else f'{x:g}'.replace('.', ',')
        conta = lambda d, teto=None, nome=str: ' · '.join(f"{nome(k)} {mil(v)}" + (f"/{mil(teto[k])}" if teto and k in teto else '') for k, v in d.items()) or 'nada'
        print(f"{l['nome']} [{a[1]}] · {l.get('tipo', 'lugar')}" + (f" · {l['habitat']}" if l.get('habitat') else '') + (f" · perigo {l['perigo']}" if l.get('perigo') else '') + (f" · a {tantos(l['longe'], 'bloco')} dos vizinhos" if l.get('longe') else '')
              + (f" · {mil(l['pop'])} de povo" if l.get('pop') else '') + (' · há cama' if l.get('cama') else '') + (f" · oficina {l['oficina']}" if l.get('oficina') is not None else ''))
        if l.get('sobre'): print(f"  {l['sobre']}")
        if l.get('vizinhos'): print('  vizinhos: ' + ', '.join(f"{E['lugares'][v]['nome']} [{v}]" if v in E['lugares'] else v for v in l['vizinhos']))
        if isinstance(l.get('preparo'), dict) and l['preparo']: print('  preparo da forja: ' + ' · '.join(f"{k} até o {T.CATS[v]}" for k, v in l['preparo'].items() if _int(v) and 0 <= v < len(T.CATS)))
        print('  estoque: ' + conta({k: v for k, v in l['estoque'].items() if v}, nome=bem))
        if isinstance(l.get('produz'), dict) and l['produz']: print('  produz por dia (antes de o preço e a estação mexerem): ' + conta(l['produz'], nome=bem))
        if isinstance(l.get('bichos'), dict) or isinstance(l.get('teto'), dict): print('  SÓ O MESTRE, os bichos (há/cabem): ' + conta(l.get('bichos') or {}, l.get('teto') or {}))
        if isinstance(l.get('coleta'), dict) or isinstance(l.get('coleta_teto'), dict): print('  SÓ O MESTRE, a matéria para tirar (há/cabe): ' + conta(l.get('coleta') or {}, l.get('coleta_teto') or {}, nome=bem))
        if isinstance(l.get('alvo_pecas'), dict) and l['alvo_pecas']: print('  a loja quer ter na prateleira: ' + ' · '.join(f"{tantos(v, 'peça ' + FEM[int(k)], 'peças ' + (FEM[int(k)][:-1] + 'ns' if FEM[int(k)].endswith('m') else FEM[int(k)] + 's'))}" for k, v in sorted(l['alvo_pecas'].items()) if k.isdigit() and int(k) < len(FEM)) + ' (acima disso, paga menos)')
        outros = {k: v for k, v in l.items() if k not in ('nome', 'em', 'tipo', 'habitat', 'perigo', 'longe', 'pop', 'cama', 'oficina', 'sobre', 'vizinhos', 'preparo', 'estoque', 'produz', 'bichos', 'teto', 'coleta', 'coleta_teto', 'alvo_pecas')}
        if outros: print('  e mais: ' + ' · '.join(f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in outros.items()))
        for i, it in E['itens']['itens'].items():
            if it.get('onde') == a[1]: print(f"  {i} {rotulo(it)}" + ((' · NO CHÃO, junto de um corpo (quem fica com ela é decisão de cena)' if de_morto(it) else ' · NO CHÃO, de quem achar') if it.get('solto') else ' · na prateleira'))
    elif a[:1] == ['mestre'] and len(a) in (2, 3):
        E = carrega()
        try: ef = json.loads(a[1])
        except ValueError as x: sys.exit(f'os efeitos vêm em JSON: uma lista de efeitos, cada um uma lista ({x}). Veja os verbos: python3 estado.py')
        if not isinstance(ef, list) or not ef or not all(isinstance(x, list) for x in ef): sys.exit('os efeitos são uma lista de listas: \'[["pessoa","eu","moedas","soma",5]]\'')
        if len(a) < 3 or not a[2].strip(): sys.exit('diga o que houve, entre aspas: o evento do Mestre vai para o registro e para o RETOMAR com esse texto (`python3 estado.py mestre \'[["pessoa","eu","moedas","soma",5]]\' "achou cinco moedas"`)')
        ev = aplica(E, 'mestre', ef, quem=[x[1] for x in ef if x[:1] == ['pessoa'] and len(x) > 1 and x[1] in E['gente']][:1], texto=a[2])
        if not ev: print('nada mudou: os efeitos já eram verdade. Nenhum evento foi registrado.'); sys.exit()
        grava(E); print(f"evento #{ev['id']} (mestre): {ev['texto']} · {tantos(len(ev['efeitos']), 'efeito')}"); P = valida(E)
        if P: print('ATENÇÃO, o estado ficou com problema:\n  ' + '\n  '.join(P))
    else: print(__doc__)
