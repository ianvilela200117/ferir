"""proto_b.py — PROTÓTIPO DE MEDIDA do projeto B (etapa 3): a gente que responde. NÃO é o motor: é o rascunho das regras, para medir custo, KB e equilíbrio.

O que já existe (a prata, o estoque, as peças, a forja, o relógio) passa pelo motor de hoje (estado.aplica, mercado, oficio, ato).
O que é do projeto B (o papel, a memória, o querer, os laços, a fama, a notícia, a caixa, a missão) mora num ARMAZÉM À PARTE (B), com um gravador pequeno
que aplica efeitos com a forma do projeto (['memoria', pid, 'junta', fato], ['noticia', id, 'chega', lugar, saltos], ['caixa', 'abre', reg]...) e escreve o
registro deles em eventos_b.jsonl. No motor de verdade, tudo isto entra pelo estado.aplica, num evento só.
A REGIÃO EM VOLTA (16 lugares, 24 rotas) é um ARREMEDO da metade A, só para a notícia andar e a gente morar: os nomes, as distâncias e o perigo são de rascunho.
"""
import copy, json, math, os, sys
import estado, mercado, talento, oficio
import tabelas as T
import tabelas_mundo as M
from itens import item
from pessoas import padrao
import tab_b as G

AQUI_RASC = None

# ====================================================================== o arremedo da metade A: os lugares e as rotas
LUGARES = [   # id, nome, tipo, povo, oficina, runas  (a vila de teste já tem 'vila' = Pedra Rasa e 'vau' = Vau Seco)
    ('torre', 'Torre Alta', 'capital', 4000, 3, 2), ('bomporto', 'Bom Porto', 'cidade', 1500, 2, 1), ('cruzeiro', 'Cruzeiro', 'cidade', 1500, 2, 1),
    ('ribeira', 'Ribeira', 'vila', 400, 1, None), ('moinhos', 'Moinhos', 'vila', 400, 1, None), ('lagoa', 'Lagoa Funda', 'vila', 400, 1, None), ('campo', 'Campo Largo', 'vila', 400, 1, None),
    ('pinhal', 'Pinhal', 'aldeia', 120, None, None), ('barreiro', 'Barreiro', 'aldeia', 120, None, None), ('fonte', 'Fonte Fria', 'aldeia', 120, None, None),
    ('outeiro', 'Outeiro', 'aldeia', 120, None, None), ('cancela', 'Cancela', 'aldeia', 120, None, None), ('passo', 'Passo Estreito', 'aldeia', 120, None, None), ('ermida', 'Ermida', 'aldeia', 120, None, None),
]
ROTAS = [('torre', 'bomporto', 4, 1), ('torre', 'cruzeiro', 5, 1), ('torre', 'moinhos', 3, 1), ('torre', 'campo', 3, 1), ('bomporto', 'vila', 4, 1), ('bomporto', 'ribeira', 2, 1),
         ('bomporto', 'barreiro', 2, 1), ('cruzeiro', 'lagoa', 3, 1), ('cruzeiro', 'fonte', 2, 2), ('cruzeiro', 'outeiro', 3, 1), ('vila', 'ribeira', 3, 1), ('vila', 'cancela', 2, 1),
         ('ribeira', 'pinhal', 2, 2), ('pinhal', 'vau', 4, 3), ('vau', 'passo', 3, 3), ('passo', 'cruzeiro', 5, 2), ('moinhos', 'ermida', 2, 1), ('campo', 'ermida', 3, 2),
         ('lagoa', 'outeiro', 2, 1), ('barreiro', 'ribeira', 3, 1), ('campo', 'bomporto', 4, 1), ('cancela', 'moinhos', 4, 2), ('fonte', 'passo', 4, 3), ('lagoa', 'torre', 6, 2)]    # (a, b, blocos, perigo)
NOMES = ['Abel', 'Aurora', 'Bárbara', 'Benedito', 'Brígida', 'Caetano', 'Cândida', 'Celso', 'Clara', 'Custódio', 'Damião', 'Dinis', 'Doroteia', 'Elias', 'Emília', 'Estêvão', 'Fausto',
         'Filipa', 'Firmino', 'Gaspar', 'Glória', 'Gonçalo', 'Graça', 'Hélio', 'Honório', 'Inês', 'Irene', 'Jacinto', 'Joaquina', 'Jordão', 'Júlia', 'Leandro', 'Leonor', 'Lourenço',
         'Luzia', 'Marcelo', 'Marta', 'Matias', 'Miguel', 'Mónica', 'Nuno', 'Olavo', 'Olímpia', 'Otávio', 'Paulina', 'Pedro', 'Quitéria', 'Rafael', 'Raimundo', 'Regina', 'Rosa',
         'Salvador', 'Severino', 'Sílvia', 'Simão', 'Teodoro', 'Teresa', 'Tibério', 'Úrsula', 'Valentim', 'Vicente', 'Violante', 'Xavier', 'Zacarias', 'Zélia']
APELIDOS = ['do Moinho', 'da Ponte', 'Ferraz', 'Correia', 'do Vale', 'Seixas', 'Cardoso', 'Lobo', 'Pires', 'Rocha', 'Vidal', 'Barros', 'Couto', 'Neves', 'Prado', 'Teles']
PAPEIS_VILA = dict(bento='ferreiro', dalva='taverneiro', rute='cacador', tome='guarda', ivo='lenhador', nara='curandeiro', lino='mercador', zeca='aprendiz', anselmo='mago',
                   lucia='sacerdote', joana='bruxa', durva='ferreiro', brasco='caravaneiro', ilvena='cacador', nena='lavrador', quim='ladino')


def vizinhos(E, lid):
    """as rotas de um lugar: {vizinho: (blocos, perigo)} (arremedo da metade A)"""
    return {k: tuple(v) for k, v in (E['lugares'][lid].get('rotas') or {}).items()}


def regiao(E):
    """o arremedo da metade A em volta da vila de teste: 14 lugares novos (Pedra Rasa e Vau Seco já existem), as 24 rotas, o mercado de cada um, a forja e a mesa de runas,
    e um lugar de custódia (a prata das missões guardada: no motor de verdade, o campo `guarda` da missão, contado na soma da prata)"""
    ef = [['lugar', 'nasce', lid, dict(nome=n, em='em ' + n, tipo=t, cama=True, estoque={})] for lid, n, t, pop, of, ru in LUGARES]
    ef.append(['lugar', 'nasce', 'custodia', dict(nome='a custódia das missões', em='na custódia', tipo='custodia', estoque={})])
    estado.aplica(E, 'gera', ef, texto='o arremedo da região (medida)')
    for lid, n, t, pop, of, ru in LUGARES:
        mercado.funda(E, lid, pop, como='o mercado do arremedo')
        x = [['lugar', lid, 'oficina', 'poe', of]] if of is not None else []
        if of: x += [['lugar', lid, 'preparo.fogo', 'poe', of], ['lugar', lid, 'preparo.bigorna', 'poe', of]]
        if ru is not None: x.append(['lugar', lid, 'runas', 'poe', ru])
        if x: estado.aplica(E, 'gera', x, onde=lid, texto='a forja e as runas do arremedo')
    rot = {}
    for a, b, bl, pe in ROTAS:
        rot.setdefault(a, {})[b] = [bl, pe]; rot.setdefault(b, {})[a] = [bl, pe]
    estado.aplica(E, 'gera', [['lugar', k, 'rotas', 'poe', v] for k, v in rot.items()], texto='as rotas do arremedo')


def _nome(E, B, r):
    usados = {p['nome'] for p in E['gente'].values()}
    for _ in range(200):
        n = f"{r.choice(NOMES)} {r.choice(APELIDOS)}"
        if n not in usados: return n
    return f"{r.choice(NOMES)} {len(usados)}"


def nasce_nomeado(E, B, lid, papel, r, pid=None):
    """o gerador de gente: um nomeado do papel, no lugar, com o nível, a mão, as peças e a bolsa do papel (e os talentos pelo dado do mundo)"""
    rot, grau, molde, (n0, n1), maestria, pecas, _, _ = G.PAPEIS[papel]
    nivel = r.randint(n0, n1); nome = _nome(E, B, r); pid = pid or f"n{len(B['gente_b']) + 1:03d}"
    while pid in E['gente']: pid += 'x'
    import vila_teste
    bolsa = alvo_bolsa_papel(papel, grau)
    reg = dict(nome=nome, nivel=nivel, atributos=padrao(nome, nivel, molde=molde)['atributos'], lugar=lid, grau_oficio=grau, maestria=dict(maestria),
               treino=vila_teste.treino_da_mao(maestria), moedas=int(bolsa), sobre=papel)
    estado.aplica(E, 'gera', [['pessoa', 'nasce', pid, talento.nasce(E, pid, reg)]], onde=lid, quem=[pid], texto=f'{nome}, {papel}')
    if pecas:
        s0 = E['itens']['seq']
        estado.aplica(E, 'gera', [['item', 'nasce', vila_teste._peca(t, q, c, cb, nome, pid)] for t, q, c, cb, _ in pecas], onde=lid, quem=[pid], texto=f'as peças de {nome}')
        estado.aplica(E, 'gera', [['item', f'i{s0 + k + 1:04d}', 'uso', 'poe', uso] for k, (_, _, _, _, uso) in enumerate(pecas) if uso], onde=lid, quem=[pid], texto=f'{nome} se veste')
    bgrava(E, B, 'gera', [['papel', pid, 'poe', papel]])
    return pid


def alvo_bolsa_papel(papel, grau): return G.BOLSA[grau] * G.BOLSA_PAPEL.get(papel, 1)


def povoa(E, B):
    """a gente da região: os da vila de teste ganham o papel; cada lugar novo, os do tipo dele (tab_b.POVOAR); Vau Seco, os de aldeia; e os laços (família e amizade)"""
    r = estado.sorte(E, 'povoa')
    for pid, papel in PAPEIS_VILA.items():
        if pid in E['gente']: bgrava(E, B, 'gera', [['papel', pid, 'poe', papel]])
    for lid, n, t, pop, of, ru in LUGARES + [('vau', 'Vau Seco', 'aldeia', 120, None, None)]:
        for papel in G.POVOAR[t]: nasce_nomeado(E, B, lid, papel, r)
    gente = [k for k in B['gente_b'] if E['gente'][k].get('estado') == 'vivo']
    por_lugar = {}
    for k in gente: por_lugar.setdefault(E['gente'][k]['lugar'], []).append(k)
    ef = []
    for lid, ks in por_lugar.items():        # cada um, um ou dois laços no lugar dele; um em cada cinco, um parente noutro lugar vizinho
        for k in ks:
            for _ in range(r.randint(1, 2)):
                o = r.choice(ks)
                if o != k: ef += [['laco', k, o, 'soma', r.randint(2, 6)], ['laco', o, k, 'soma', r.randint(2, 6)]]
            if r.random() < 0.2 and vizinhos(E, lid):
                vl = r.choice(sorted(vizinhos(E, lid))); outros = por_lugar.get(vl) or []
                if outros: o = r.choice(outros); ef += [['laco', k, o, 'soma', 7], ['laco', o, k, 'soma', 7]]
    bgrava(E, B, 'gera', ef)


# ====================================================================== o armazém B e o gravador pequeno
def B_novo(): return dict(gente_b={}, noticias=dict(seq=0, ativas={}), caixa=dict(seq=0, abertos={}, feitos=0, vencidos=0, forcados=0), missoes=dict(seq=0, itens={}), _log=[], _conta=dict(eventos=0, segundos=0.0))


def B_grava(B, pasta):
    for k in ('gente_b', 'noticias', 'caixa', 'missoes'):
        json.dump(B[k], open(os.path.join(pasta, k + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    if B['_log']:
        with open(os.path.join(pasta, 'eventos_b.jsonl'), 'a', encoding='utf-8') as f:
            for ev in B['_log']: f.write(json.dumps(ev, ensure_ascii=False) + '\n')
        B['_log'] = []


def gb(B, pid):
    return B['gente_b'].setdefault(pid, dict(papel=None, mem=[], querer=None, lacos={}, fama={}))


def bgrava(E, B, tipo, efb, texto=''):
    """o gravador pequeno do armazém B: aplica os efeitos com a forma do projeto, e escreve o registro. (Só copia o que toca: aqui, aplica direto, depois de conferir.)"""
    import time
    if not efb: return None
    t0 = time.perf_counter(); dia = E['relogio']['dia']
    for ef in efb:
        v = ef[0]
        if v == 'papel': gb(B, ef[1])['papel'] = ef[3]
        elif v == 'memoria':
            g = gb(B, ef[1])
            if ef[2] == 'junta':                    # cheia, esquece o de menor peso de hoje (o mais velho primeiro): a regra mora no gravador
                if len(g['mem']) >= G.MEMORIA:
                    i = min(range(len(g['mem'])), key=lambda k: (abs(peso_atual(g['mem'][k], dia)), g['mem'][k][0])); g['mem'].pop(i)
                g['mem'].append(list(ef[3]))
            elif ef[2] == 'esquece': g['mem'].pop(ef[3])
            elif ef[2] == 'retribui': g.setdefault('ret', []).append(list(ef[3]))
        elif v == 'querer': gb(B, ef[1])['querer'] = copy.deepcopy(ef[3])
        elif v == 'laco':
            g = gb(B, ef[1]); g['lacos'][ef[2]] = max(-10, min(10, g['lacos'].get(ef[2], 0) + ef[4]))
        elif v == 'fama':
            g = gb(B, ef[1]); d = g['fama'].setdefault(ef[2], {}); atual = fama_de(E, B, ef[1], ef[2], ef[3]); d[ef[3]] = [max(0, min(100, atual + ef[5])), dia]
        elif v == 'viagem': gb(B, ef[1])['viagem'] = copy.deepcopy(ef[3])
        elif v == 'noticia':
            N = B['noticias']
            if ef[1] == 'nasce':
                N['seq'] += 1; n = dict(ef[2], id=f"n{N['seq']}", d=dia); N['ativas'][n['id']] = n
            elif ef[2] == 'chega': N['ativas'][ef[1]]['em'][ef[3]] = [dia, ef[4]]
            elif ef[2] == 'some': N['ativas'].pop(ef[1], None)
        elif v == 'caixa':
            C = B['caixa']
            if ef[1] == 'abre': C['seq'] += 1; c = dict(ef[2], id=f"c{C['seq']}"); C['abertos'][c['id']] = c
            elif ef[2] == 'fecha': C['abertos'].pop(ef[1]); C[ef[3]] = C.get(ef[3], 0) + 1
        elif v == 'missao':
            Q = B['missoes']
            if ef[1] == 'abre': Q['seq'] += 1; m = dict(ef[2], id=f"m{Q['seq']}"); Q['itens'][m['id']] = m
            elif ef[2] == 'fecha': Q['itens'][ef[1]]['estado'] = ef[3]
            else: Q['itens'][ef[1]][ef[2]] = copy.deepcopy(ef[4])
        else: raise ValueError(f'verbo do rascunho desconhecido: {v}')
    B['_conta']['eventos'] += 1; B['_conta']['segundos'] += time.perf_counter() - t0
    B['_log'].append(dict(dia=dia, bloco=E['relogio']['bloco'], tipo=tipo, efeitos=efb, texto=texto))
    if len(B['_log']) > 5000 and AQUI_RASC: B_grava(B, AQUI_RASC)


def ultimo_id(B, k): return f"{dict(noticias='n', caixa='c', missoes='m')[k]}{B[k]['seq']}"


# ====================================================================== ler: a rotina, a memória, a opinião, a fama, o teto
def papel(B, pid): return (B['gente_b'].get(pid) or {}).get('papel')
def vivo(E, pid): return E['gente'].get(pid, {}).get('estado') == 'vivo'
def nomeados(E, B, lid=None): return [k for k, g in B['gente_b'].items() if g.get('papel') and vivo(E, k) and (lid is None or E['gente'][k]['lugar'] == lid)]


def ponto(E, B, pid, bloco=None):
    """onde a pessoa está e o que faz neste bloco: sai da tabela da rotina (não grava nada). Quem viaja está na estrada."""
    g = B['gente_b'].get(pid) or {}
    if g.get('viagem'): return ('estrada', 'viaja')
    pa = g.get('papel'); bloco = E['relogio']['bloco'] if bloco is None else bloco
    if not pa: return ('praça', 'à toa')
    sp, at = G.ROTINAS[G.PAPEIS[pa][0]][bloco]
    return (G.PAPEIS[pa][7] if sp == 'oficio' else sp, at)


def peso_atual(f, hoje):
    """o peso de um fato hoje: ele esfria com o tempo (o de peso 8 ou mais nunca). A conta sai na hora de ler: não grava nada"""
    d, t, p = f[0], f[1], f[2]
    if abs(p) >= 8: return p
    ritmo = next((dd for teto, dd in G.ESFRIA if abs(p) <= teto), None)
    perde = (hoje - d) // ritmo
    return 0 if perde >= abs(p) else p - perde * (1 if p > 0 else -1)


def fama_de(E, B, sujeito, lid, eixo):
    v = ((gb(B, sujeito)['fama'].get(lid) or {}).get(eixo)) or [0, E['relogio']['dia']]
    return max(0, v[0] - (E['relogio']['dia'] - v[1]) // G.FAMA_ESFRIA)


def opiniao(E, B, pid, sobre='eu'):
    """a opinião de pid sobre o personagem: a soma dos pesos de hoje, mais o tom da fama do lugar dele (para quem não lembra nada), de −10 a 10"""
    hoje = E['relogio']['dia']; mem = [f for f in gb(B, pid)['mem'] if f[3] == sobre]
    s = sum(peso_atual(f, hoje) for f in mem) + tom(E, B, sobre, E['gente'][pid]['lugar'])
    return max(-10, min(10, s))


def tom(E, B, sobre, lid):
    """o pano de fundo: o que o lugar diz de quem tem fama ali (de −3 a +2), por baixo do que cada um lembra"""
    return max(G.TOM[0], min(G.TOM[1], (fama_de(E, B, sobre, lid, 'feito') + fama_de(E, B, sobre, lid, 'ofício')) // G.FAMA_TOM['feito']
                              - fama_de(E, B, sobre, lid, 'crime') // -G.FAMA_TOM['crime']))


def palavra(op): return next(w for teto, w in G.OPINIAO if op <= teto)


def lembra(E, B, pid, tipo, canal='viu', sobre='eu', peso=None, texto=None):
    """os efeitos de guardar um fato na memória de pid (cheia: esquece o de menor peso de hoje, o mais velho primeiro)"""
    p0 = G.FATOS[tipo][0] if peso is None else peso
    p = round(p0 * G.CANAL[canal]); p = p if p != 0 else (1 if p0 > 0 else -1 if p0 < 0 else 0)
    if p == 0: return []
    return [['memoria', pid, 'junta', [E['relogio']['dia'], tipo, p, sobre, canal] + ([texto] if texto else [])]]


def teto(E, pid):
    """o grau de perigo (0 = F ... 6 = S) que a pessoa enfrenta sem medo: pela mão na arma em uso e a categoria da arma e da armadura"""
    arma = arm = None
    for it in E['itens']['itens'].values():
        if it.get('dono') == pid and it.get('uso') == 'arma': arma = it
        if it.get('dono') == pid and it.get('uso') == 'veste' and 'tronco' in (it.get('cobre') or []): arm = it
    mao = (E['gente'][pid].get('maestria') or {}).get(arma['familia'], 0) if arma else 0
    return max(0, math.floor((mao / 2 + 3 * (arma['cat'] if arma else -1) + (arm['cat'] if arm else -1)) / 2))


def pecas_de(E, pid): return [it for it in E['itens']['itens'].values() if it.get('dono') == pid and it.get('tipo') in ('arma', 'armadura', 'escudo')]


# ====================================================================== a notícia
def noticia(E, B, lid, tipo, sujeito=None, texto='', eixo=None, pontos=0, alcance=None, peso=0):
    """os efeitos de uma notícia que nasce num lugar (e chega a ele no mesmo dia)"""
    a = G.FATOS[tipo][3] if alcance is None and tipo in G.FATOS else (alcance or 0)
    return [['noticia', 'nasce', dict(de=lid, s=sujeito, t=tipo, x=texto, e=eixo, f=pontos, a=a, p=peso, em={lid: [E['relogio']['dia'], 0]})]]


def chega(E, B, nid, lid, saltos):
    """a notícia chega a um lugar: a fama de quem ela fala, e a memória de até 3 nomeados de lá (os de laço com quem está nela; o do mesmo ofício; o taverneiro)"""
    n = B['noticias']['ativas'][nid]; efb = [['noticia', nid, 'chega', lid, saltos]]
    boato = saltos > G.BOATO; s = n.get('s')
    if s == 'eu':
        if n.get('e') and n.get('f'): efb.append(['fama', 'eu', lid, n['e'], 'soma', round(n['f'] * (0.5 if boato else 1))])
        if n.get('p'):
            ks = nomeados(E, B, lid); r = estado.sorte(E, f'ouve|{nid}|{lid}')
            quem = [k for k in ks if n.get('v') in gb(B, k)['lacos']] + [k for k in ks if papel(B, k) in ('taverneiro',)]
            quem += r.sample(ks, min(len(ks), G.OUVEM))
            vistos = []
            for k in quem:
                if k not in vistos and k != n.get('v'): vistos.append(k)
            for k in vistos[:G.OUVEM]: efb += lembra(E, B, k, 'ouviu', canal='boato' if boato else 'ouviu', peso=n['p'], texto=n['t'])
    return efb


def noticias_andam(E, B):
    """uma rota por dia: cada notícia que chegou ontem a um lugar, e ainda não passou do alcance, chega hoje aos vizinhos dele; a velha que não anda mais sai do arquivo"""
    hoje = E['relogio']['dia']; efb = []
    for nid, n in list(B['noticias']['ativas'].items()):
        anda = False
        for lid, (d, s) in list(n['em'].items()):
            if d == hoje - 1 and s < n['a'] and E['lugares'].get(lid, {}).get('rotas'):
                for v in vizinhos(E, lid):
                    if v not in n['em']: n2 = chega(E, B, nid, v, s + 1); efb += n2; n['em'][v] = [hoje, s + 1]; anda = True      # (marca já, para dois vizinhos não trazerem a mesma)
        if not anda and hoje - n['d'] > G.VIDA_NOTICIA: efb.append(['noticia', nid, 'some'])
    bgrava(E, B, 'noticias', efb, texto='as notícias andam')


# ====================================================================== a caixa
def caixa_abre(E, B, de, pede, molde, prazo, motivo, opcoes, padrao, custo, **mais):
    C = B['caixa']; ef = []
    if len(C['abertos']) >= G.CAIXA:            # cabem 7: o oitavo força o mais velho
        velho = min(C['abertos'].values(), key=lambda c: c['ab']); vence(E, B, velho['id'], forcado=True)
    bgrava(E, B, 'caixa', [['caixa', 'abre', dict(de=de, pede=pede, m=molde, ab=estado.agora(E), prazo=estado.agora(E) + prazo, mot=motivo, op=opcoes, pad=padrao, custo=custo, **mais)]],
           texto=f"{E['gente'][de]['nome']} pede: {pede}")
    return ultimo_id(B, 'caixa')


def vence(E, B, cid, forcado=False):
    """o prazo venceu (ou o oitavo item forçou o mais velho): vale o padrão, sempre com custo"""
    c = B['caixa']['abertos'][cid]; efb = [['caixa', cid, 'fecha', 'forcados' if forcado else 'vencidos']]
    de = c['de']; lid = E['gente'][de]['lugar']
    efb += lembra(E, B, de, 'calou')
    if c['m'] == 'encomenda':
        efb += [['fama', 'eu', lid, 'ofício', 'soma', -1]]
        bgrava(E, B, 'caixa', efb, texto='a caixa venceu'); encomenda_npc(E, B, de, c['peca'], sem='eu')
        return
    if c['m'] == 'missao':
        bgrava(E, B, 'caixa', efb + [['missao', c['missao'], 'dirigida', 'poe', None]], texto='a caixa venceu: a missão vai ao quadro'); return
    if c['m'] == 'cobranca':
        efb += [['fama', 'eu', lid, 'crime', 'soma', 5]] + noticia(E, B, lid, 'suspeita', 'eu', f"{E['gente'][de]['nome']} se queixa de você ao alcaide", 'crime', 3, peso=-2)
    bgrava(E, B, 'caixa', efb, texto='a caixa venceu')


def caixa_dia(E, B):
    for cid, c in list(B['caixa']['abertos'].items()):
        if c['prazo'] <= estado.agora(E): vence(E, B, cid)


# ====================================================================== a missão e a encomenda
def missao_abre(E, B, de, tipo, grau, paga, prazo, onde, alvo=None, dirigida=None, **mais):
    """a missão nasce com a paga guardada (sai da bolsa de quem pede, ou do caixa do lugar, para a custódia)"""
    q = E['gente'][de] if de in E['gente'] else None
    if q is not None and q['moedas'] < paga: return None
    ef = ([['pessoa', de, 'moedas', 'soma', -paga]] if q is not None else [['estoque', onde, 'prata', 'soma', -paga]]) + [['estoque', 'custodia', 'prata', 'soma', paga]]
    if q is None and E['lugares'][onde]['estoque'].get('prata', 0) < paga: return None
    estado.aplica(E, 'mestre', ef, onde=onde, texto=f'a paga da missão guardada')
    bgrava(E, B, 'missao', [['missao', 'abre', dict(de=de, tipo=tipo, grau=grau, paga=paga, caucao=round(paga * G.CAUCAO), prazo=E['relogio']['dia'] + prazo, onde=onde, alvo=alvo,
                                                     dirigida=dirigida, quem=None, estado='aberta', **mais)]])
    return ultimo_id(B, 'missoes')


def missao_fecha(E, B, mid, desfecho, quem=None):
    """paga quem cumpriu (a paga e a caução de volta), ou devolve a paga a quem pediu (e a caução de quem falhou vai a quem pediu)"""
    m = B['missoes']['itens'][mid]; de = m['de']; paga = m['paga']; cau = m['caucao'] if m.get('quem') else 0; ef = []
    para_de = (lambda n: ['pessoa', de, 'moedas', 'soma', n]) if de in E['gente'] and vivo(E, de) else (lambda n: ['estoque', m['onde'], 'prata', 'soma', n])
    if desfecho == 'cumprida': ef = [['estoque', 'custodia', 'prata', 'soma', -(paga + cau)], ['pessoa', m['quem'], 'moedas', 'soma', paga + cau]]
    elif desfecho == 'falhada': ef = [['estoque', 'custodia', 'prata', 'soma', -(paga + cau)], para_de(paga + cau)]
    else: ef = [['estoque', 'custodia', 'prata', 'soma', -(paga + cau)], para_de(paga + cau)]
    if paga + cau: estado.aplica(E, 'mestre', ef, onde=m['onde'], texto=f'a missão {desfecho}')
    efb = [['missao', mid, 'fecha', desfecho]]
    if m.get('quem') == 'eu':
        lid = m['onde']
        if desfecho == 'cumprida':
            efb += lembra(E, B, de, 'cumpriu') if de in E['gente'] else []
            efb += noticia(E, B, lid, 'cumpriu', 'eu', f"cumpriu a missão de {E['gente'][de]['nome'] if de in E['gente'] else 'o lugar'}", 'feito', 1 if m['tipo'] == 'levar' else 2 * G.GRAUS.index(m['grau']) + 2, peso=2)
        elif desfecho == 'falhada':
            efb += (lembra(E, B, de, 'falhou_missao') if de in E['gente'] else []) + noticia(E, B, lid, 'falhou_missao', 'eu', 'falhou numa missão', 'feito', 0, peso=-1)
    bgrava(E, B, 'missao', efb)


def preco_peca(peca):
    it = item(peca['tipo'], peca['cat'], familia=peca.get('familia'), material=peca.get('material'), cobre=peca.get('cobre'))
    return max(1, math.ceil(mercado.valor(dict(it, dur=[it['dur'][1], it['dur'][1]]))))


def ferreiros(E, B, lid, cat):
    """quem pode fazer a peça para um cliente deste lugar: os ferreiros de nome do lugar e dos vizinhos a até 4 blocos (com forja) e o personagem"""
    perto = [lid] + [v for v, (bl, pe) in vizinhos(E, lid).items() if bl <= 4]
    serve = lambda l: (E['lugares'][l].get('oficina') or 0) >= max(1, cat)          # a peça Rara pede a forja de cidade; a Épica, a grande forja
    c = [k for k in nomeados(E, B) if papel(B, k) in ('ferreiro', 'mestre_ferreiro') and E['gente'][k]['lugar'] in perto and serve(E['gente'][k]['lugar']) and not gb(B, k).get('viagem')]
    eu = E['gente'].get('eu')
    if eu and eu['estado'] == 'vivo' and eu['lugar'] in perto and serve(eu['lugar']) and (eu.get('maestria') or {}).get('forja', 0) >= 2: c.append('eu')
    return c


def peso_ferreiro(E, B, cli, f):
    lcli = E['gente'][cli]['lugar']; lf = E['gente'][f]['lugar']
    if f == 'eu':
        op = opiniao(E, B, cli)
        if op <= G.NAO_PEDE: return 0
        fam = fama_de(E, B, 'eu', lcli, 'ofício'); fator = (gb(B, 'eu').get('preco') or 1.0)
        w = (1 + fam / 10) * (1 + max(0, op) / 3) / fator ** 2
    else:
        fam = G.FAMA_FERREIRO[E['gente'][f]['grau_oficio']] if E['gente'][f]['grau_oficio'] in G.FAMA_FERREIRO else 10
        w = (1 + fam / 10) * (1 + max(0, gb(B, cli)['lacos'].get(f, 0)) / 3)
    return w * (1 if lf == lcli else 0.5)


def encomenda_npc(E, B, cli, peca, sem=None):
    """o cliente escolhe outro ferreiro (não o personagem): o ferreiro de nome faz a peça fora de cena, com o dado do mundo e a conta da forja dele"""
    fs = [f for f in ferreiros(E, B, E['gente'][cli]['lugar'], peca['cat']) if f != sem and f != 'eu']
    if not fs: return None
    r = estado.sorte(E, f'encomenda|{cli}'); ws = [peso_ferreiro(E, B, cli, f) for f in fs]
    f = r.choices(fs, ws)[0]; c = oficio.conta(E, f, peca['cat'], lid=E['gente'][f]['lugar']); preco = preco_peca(peca)
    if E['gente'][cli]['moedas'] < preco: return None
    mat = oficio.materia_de(dict(peca)); custo = sum(math.ceil(mercado._base(k)) * n for k, n in mat.items()); lf = E['gente'][f]['lugar']
    ok = r.random() < c['acerta'] + c['pouco'] * 0.0
    ef = [['estoque', lf, 'prata', 'soma', custo], ['pessoa', f, 'moedas', 'soma', -min(custo, E['gente'][f]['moedas'])]]
    if E['gente'][f]['moedas'] < custo: ef[0][4] = E['gente'][f]['moedas']
    if ok:
        it = item(peca['tipo'], peca['cat'], familia=peca.get('familia'), material=peca.get('material'), cobre=peca.get('cobre'), dono=cli, feito_por=f)
        ef += [['item', 'nasce', it], ['pessoa', cli, 'moedas', 'soma', -preco], ['pessoa', f, 'moedas', 'soma', preco]]
    if any(x[4] for x in ef if x[0] in ('estoque', 'pessoa')) or ok: estado.aplica(E, 'mestre', ef, onde=lf, quem=[cli, f], texto='encomenda fora de cena')
    if ok: troca_peca(E, B, cli, f"i{E['itens']['seq']:04d}", lf)
    STATS['enc_npc'] += 1; STATS['enc_npc_ok'] += ok
    return f


# ====================================================================== a semana de cada nomeado: a bolsa, o desgaste, o querer
STATS = dict(enc_eu=0, enc_npc=0, enc_npc_ok=0, querer={}, missoes=0, missoes_npc=0, mortes_missao=0, furtos_npc=0, furtos_npc_pegos=0, noticias=0, consertos=0, laco_noticia=0)


def semana(E, B, pid):
    """a semana de um nomeado (no dia da semana dele): a bolsa anda para o alvo (a prata vem do caixa do lugar ou volta a ele), a peça do ofício gasta, e o querer sai"""
    p = E['gente'][pid]; g = gb(B, pid); pa = g['papel']; lid = p['lugar']; r = estado.sorte(E, f'semana|{pid}')
    if g.get('viagem'): return
    grau = p['grau_oficio']; alvo = alvo_bolsa_papel(pa, grau) + ((g.get('querer') or {}).get('preco', 0) if (g.get('querer') or {}).get('t') == 'juntar' else 0)
    sobra = (M.SALARIO[grau] * M.JORNADA - G.VIVER_DIA) * 7; ef = []
    d = alvo - p['moedas']; caixa_l = E['lugares'][lid]['estoque'].get('prata', 0)
    if d > 0: d = int(min(d, sobra, caixa_l))
    else: d = int(d)
    if d: ef += [['pessoa', pid, 'moedas', 'soma', d], ['estoque', lid, 'prata', 'soma', -d]]
    gasto = G.PAPEIS[pa][6]
    if gasto:
        for it in pecas_de(E, pid):
            if it.get('uso') and it['dur'][0] > 0 and r.random() < gasto: ef.append(['item', it['id'], 'dur', 'soma', -1])
    if ef: estado.aplica(E, 'mestre', ef, onde=lid, quem=[pid], texto='a semana')
    querer(E, B, pid, r)


def precisa_peca(E, B, pid):
    """a peça do ofício que falta, quebrou ou está no fim (o motivo da encomenda), ou None; e a que gasta (o motivo do conserto)"""
    pa = papel(B, pid); quer = G.PAPEIS[pa][5]; tem = pecas_de(E, pid); nova = gasta = None
    for t, q, c, cb, uso in quer:
        x = next((it for it in tem if it.get('uso') and it['tipo'] == t and (t != 'arma' or it.get('familia') == q) and (t != 'armadura' or it.get('material') == q)), None)
        if x is None or x['dur'][0] <= x['dur'][1] * G.QUEBRA:
            nova = nova or dict(tipo=t, cat=c if x is None else x['cat'], **({'familia': q} if t == 'arma' else {'material': q} if t == 'armadura' else {}))
        elif x['dur'][0] < x['dur'][1] * G.GASTA: gasta = gasta or x
    return nova, gasta


def melhora(E, B, pid):
    """a arma do ofício uma categoria acima, se a bolsa tem MELHORA vezes o preço dela (o rico quer o melhor)"""
    p = E['gente'][pid]
    for it in pecas_de(E, pid):
        if it.get('uso') == 'arma' and it['cat'] < 2:
            peca = dict(tipo='arma', cat=it['cat'] + 1, familia=it['familia'])
            if p['moedas'] >= G.MELHORA * preco_peca(peca): return peca
    return None


def querer(E, B, pid, r):
    p = E['gente'][pid]; g = gb(B, pid); pa = g['papel']; lid = p['lugar']; q = g.get('querer') or {}
    if q.get('t') == 'juntar':          # quem junta para a peça: quando a bolsa chega, encomenda
        if p['moedas'] >= q['preco']: bgrava(E, B, 'querer', [['querer', pid, 'poe', None]]); return encomendar(E, B, pid, q['peca'])
        return
    nova, gasta = precisa_peca(E, B, pid); op = opiniao(E, B, pid); w = {}
    if nova: w['encomendar'] = G.QUERER['encomendar']
    melhor = melhora(E, B, pid)
    if melhor and not nova: w['melhorar'] = G.QUERER['melhorar']
    if gasta: w['consertar'] = G.QUERER['consertar']
    mem = g['mem']; hoje = E['relogio']['dia']
    if any(peso_atual(f, hoje) <= -5 for f in mem if f[3] == 'eu') and not any(c['de'] == pid for c in B['caixa']['abertos'].values()): w['cobrar'] = G.QUERER['cobrar']
    ret = [tuple(x) for x in g.get('ret', [])]
    if any(peso_atual(f, hoje) >= 6 and (f[0], f[1]) not in ret for f in mem if f[3] == 'eu'): w['retribuir'] = G.QUERER['retribuir']
    if abs(op) >= 4 and mem: w['falar'] = G.QUERER['falar']
    if pa == 'ladino' and p['moedas'] < alvo_bolsa_papel(pa, p['grau_oficio']): w['furtar'] = G.QUERER['furtar']
    if pa in ('mercador', 'caravaneiro') or any(E['gente'].get(k, {}).get('lugar') != lid for k in g['lacos'] if k in E['gente']): w['viajar'] = G.QUERER['viajar']
    w['laco'] = G.QUERER['laco']; w['nada'] = G.QUERER['nada']
    if pa == 'alcaide' or (pa == 'mercador' and vizinhos(E, lid)): w['missao'] = G.QUERER['missao']
    for k, x in G.QUERER_PAPEL.get(pa, {}).items():
        if k in w: w[k] *= x
    ks = sorted(w); t = r.choices(ks, [w[k] for k in ks])[0]
    STATS['querer'][t] = STATS['querer'].get(t, 0) + 1
    if t == 'melhorar': t = 'encomendar'; nova = melhor
    if t == 'encomendar':
        preco = preco_peca(nova)
        if p['moedas'] >= preco: return encomendar(E, B, pid, nova)
        bgrava(E, B, 'querer', [['querer', pid, 'poe', dict(t='juntar', peca=nova, preco=preco, desde=hoje)]], texto=f"{p['nome']} junta para {nova.get('familia') or nova.get('material') or 'escudo'}")
    elif t == 'consertar':
        pontos = gasta['dur'][1] - gasta['dur'][0]; custo = math.ceil(mercado.valor(dict(gasta, dur=[gasta['dur'][1]] * 2)) * M.CONSERTO_PONTO * pontos)
        fs = ferreiros(E, B, lid, gasta['cat']) if p['moedas'] >= custo else []
        ws = [peso_ferreiro(E, B, pid, f) for f in fs]
        if fs and any(ws):
            f = r.choices(fs, ws)[0]
            if f == 'eu':
                STATS['cons_eu'] = STATS.get('cons_eu', 0) + 1
                caixa_abre(E, B, pid, f"consertar {gasta['nome']} ({pontos} pontos), por {custo} de prata", 'conserto', G.PRAZO_RESPOSTA, dict(peca_gasta=gasta['id']), dict(a='aceitar', b='recusar'), 'b',
                           'ele leva a outro ferreiro e lembra que você calou', item=gasta['id'], pontos=pontos, valor=custo)
            else:
                estado.aplica(E, 'mestre', [['item', gasta['id'], 'dur', 'soma', pontos], ['pessoa', pid, 'moedas', 'soma', -custo], ['pessoa', f, 'moedas', 'soma', custo]], onde=lid, quem=[pid, f], texto='conserto')
                STATS['consertos'] += 1
    elif t == 'missao': pede_missao(E, B, pid, r)
    elif t == 'laco':
        meus = [k for k in nomeados(E, B, lid) if k != pid and ponto(E, B, k, 4)[0] == 'taverna']
        if meus:
            o = r.choice(meus); x = 2 if r.random() < 0.7 else -2; antes = g['lacos'].get(o, 0); efb = [['laco', pid, o, 'soma', x], ['laco', o, pid, 'soma', x]]
            if (antes < 6 <= antes + x) or (antes > -5 >= antes + x):
                efb += noticia(E, B, lid, 'laco', None, f"{p['nome']} e {E['gente'][o]['nome']} " + ('estão sempre juntos' if x > 0 else 'brigaram na taverna'), alcance=1); STATS['laco_noticia'] += 1
            bgrava(E, B, 'laco', efb)
    elif t == 'falar':
        efb = noticia(E, B, lid, 'ouviu', 'eu', f"{p['nome']} fala {'bem' if op > 0 else 'mal'} de você", alcance=0, peso=2 if op > 0 else -2)
        bgrava(E, B, 'falar', efb); nid = ultimo_id(B, 'noticias'); B['noticias']['ativas'][nid]['v'] = pid
        bgrava(E, B, 'falar', chega(E, B, nid, lid, 0)[1:])
    elif t == 'cobrar':
        f = min((f for f in mem if f[3] == 'eu'), key=lambda f: peso_atual(f, hoje)); n = 5 if f[1] != 'roubou' else 10
        caixa_abre(E, B, pid, f"que você pague {n} de prata pelo que fez ({G.FATOS[f[1]][4]})", 'cobranca', 18, dict(memoria=f[:2]), dict(a=f'pagar {n}', b='negar'), 'b',
                   'ele se queixa ao alcaide: a fama de crime sobe, e ele lembra', valor=n)
    elif t == 'retribuir':
        f = next(f for f in mem if f[3] == 'eu' and peso_atual(f, hoje) >= 6 and (f[0], f[1]) not in ret)
        bgrava(E, B, 'querer', [['memoria', pid, 'retribui', f[:2]]])
        dar = max(1, p['moedas'] // 5)
        caixa_abre(E, B, pid, f'dar-lhe {dar} de prata, pelo que você fez', 'oferta', 18, dict(memoria=f[:2]), dict(a='aceitar', b='recusar'), 'b', 'ele se sente desfeitado', valor=dar)
    elif t == 'furtar': furto_npc(E, B, pid, r)
    elif t == 'viajar':
        vs = vizinhos(E, lid)
        if vs:
            v = r.choice(sorted(vs)); bl, pe = vs[v]; dias = max(2, 2 * bl // 6 + 2)
            estado.aplica(E, 'mestre', [['pessoa', pid, 'lugar', 'poe', v]], onde=v, quem=[pid], texto=f"{p['nome']} viaja")
            bgrava(E, B, 'viagem', [['viagem', pid, 'poe', dict(casa=lid, volta=hoje + dias)]])


def pede_missao(E, B, pid, r):
    """o motivo da missão tem de estar no estado: o alcaide, pelo roubo do covil na semana ou pelo bicho do ermo; o mercador, pela escolta numa rota de perigo"""
    p = E['gente'][pid]; lid = p['lugar']; pa = papel(B, pid)
    if any(m['de'] == pid and m['estado'] in ('aberta', 'pega') for m in B['missoes']['itens'].values()): return
    if pa == 'mercador':
        vs = [(v, bl, pe) for v, (bl, pe) in vizinhos(E, lid).items() if pe >= 2]
        if not vs: vs = [(v, bl, pe) for v, (bl, pe) in vizinhos(E, lid).items()]
        v, bl, pe = r.choice(sorted(vs)); grau = G.GRAUS[min(6, pe - 1)]; paga = G.LEVAR[0] + G.LEVAR[1] * 2 * bl if pe <= 1 else G.PAGA_GRAU[pe - 1]
        tipo = 'levar' if pe <= 1 else 'escoltar'
        mid = missao_abre(E, B, pid, tipo, grau, paga, G.PRAZO_MISSAO, lid, alvo=v, blocos=bl)
    else:
        rob = LOG_COVIL.get(lid, 0) > 0
        if not rob and r.random() > 0.15: return
        grau = 'D' if rob else 'E'; paga = G.PAGA_GRAU[G.GRAUS.index(grau)]
        mid = missao_abre(E, B, pid, 'limpar' if rob else 'caçar', grau, paga, G.PRAZO_MISSAO, lid, alvo='toca' if rob else 'lobo')
        LOG_COVIL[lid] = 0
    if not mid: return
    STATS['missoes'] += 1
    m = B['missoes']['itens'][mid]
    if lid == E['gente']['eu']['lugar'] or lid in vizinhos(E, E['gente']['eu']['lugar']):
        op = opiniao(E, B, pid); fam = fama_de(E, B, 'eu', lid, 'feito')
        if op >= G.DIRIGE or fam >= 10 * (G.GRAUS.index(m['grau']) + 1):
            bgrava(E, B, 'missao', [['missao', mid, 'dirigida', 'poe', 'eu']])
            caixa_abre(E, B, pid, f"que você {m['tipo']} ({m['alvo']}), por {m['paga']} de prata (caução {m['caucao']})", 'missao', 12, dict(missao=mid), dict(a='pegar', b='recusar'), 'b',
                       'ele lembra que você calou; a missão vai ao quadro', missao=mid)


LOG_COVIL = {}


def missoes_dia(E, B):
    """a missão vencida devolve a paga; a do quadro, quem tem o teto para ela (o guarda, o caçador, o capitão), de lá ou de perto, pega; e cumpre (ou morre) em uns dias"""
    hoje = E['relogio']['dia']; r = estado.sorte(E, 'missoes_dia')
    for mid, m in list(B['missoes']['itens'].items()):
        if m['estado'] == 'aberta' and hoje > m['prazo']: missao_fecha(E, B, mid, 'vencida'); continue
        if m['estado'] == 'pega' and m['quem'] != 'eu' and hoje >= m.get('fim', hoje + 1):
            k = m['quem']; ok = r.random() < G.NOMEADO_FAZ.get(max(-1, min(1, teto(E, k) - G.GRAUS.index(m['grau']))), 0.25)
            if not ok and teto(E, k) < G.GRAUS.index(m['grau']) and r.random() < G.NOMEADO_MORRE:
                estado.aplica(E, 'mestre', [['pessoa', k, 'estado', 'poe', 'morto']], onde=E['gente'][k]['lugar'], texto='morre na missão'); STATS['mortes_missao'] += 1
                bgrava(E, B, 'morte', noticia(E, B, m['onde'], 'morreu_junto', None, f"{E['gente'][k]['nome']} morreu na missão", alcance=2))
            if vivo(E, k) and m['tipo'] in ('limpar', 'caçar', 'escoltar'):
                g_ = [['item', it['id'], 'dur', 'soma', -G.MISSAO_GASTA] for it in pecas_de(E, k) if it.get('uso') in ('arma', 'veste', 'escudo') and it['dur'][0] > 0]
                if g_: estado.aplica(E, 'mestre', g_, onde=E['gente'][k]['lugar'], quem=[k], texto='a luta gasta as peças')
            missao_fecha(E, B, mid, 'cumprida' if ok else 'falhada'); STATS['missoes_npc'] += 1
            if ok: bgrava(E, B, 'missao', noticia(E, B, m['onde'], 'cumpriu', None, f"{E['gente'][k]['nome']} cumpriu a missão de {E['gente'][m['de']]['nome'] if m['de'] in E['gente'] else m['onde']} ({m['tipo']}: {m['alvo']})", alcance=1))
        elif m['estado'] == 'aberta' and not m.get('dirigida') and m['tipo'] in ('limpar', 'caçar', 'escoltar'):
            perto = [m['onde']] + list(vizinhos(E, m['onde']))
            ks = [k for k in nomeados(E, B) if papel(B, k) in ('guarda', 'capitao', 'cacador', 'caravaneiro') and E['gente'][k]['lugar'] in perto and not gb(B, k).get('viagem')
                  and teto(E, k) >= G.GRAUS.index(m['grau']) - 1 and not any(x.get('quem') == k and x['estado'] == 'pega' for x in B['missoes']['itens'].values())
                  and E['gente'][k]['moedas'] >= m['caucao']]
            if ks and r.random() < 0.3:
                k = r.choice(ks)
                estado.aplica(E, 'mestre', [['pessoa', k, 'moedas', 'soma', -m['caucao']], ['estoque', 'custodia', 'prata', 'soma', m['caucao']]], onde=m['onde'], quem=[k], texto='pega a missão')
                bgrava(E, B, 'missao', [['missao', mid, 'quem', 'poe', k], ['missao', mid, 'estado', 'poe', 'pega'], ['missao', mid, 'fim', 'poe', hoje + r.randint(2, 5)]])


# ====================================================================== o furto
def d2(r):
    def d():
        s = 0
        while True:
            x = r.randint(1, 20); s += x
            if x < 20: return s
    return d() + d()


def vigia(E, B, lid):
    v = E['lugares'][lid].get('vigia') or []
    hoje = E['relogio']['dia']
    return min(G.VIGIA[2], G.VIGIA[0] * sum(1 for d in v if hoje - d <= G.VIGIA[1]))


def contra_furto(E, B, ladrao, vit, bloco):
    q = E['gente'][vit]; lid = q['lugar']; sp = ponto(E, B, vit, bloco)[0]
    c = G.FURTO_CONTRA + q['atributos']['Percepção'] // 10 + (G.FURTO_GUARDA if papel(B, vit) in ('guarda', 'capitao', 'mercador') else 0)
    if any(ponto(E, B, k, bloco) == (sp, 'vigia') for k in nomeados(E, B, lid) if k != vit): c += G.FURTO_GUARDA
    c += vigia(E, B, lid) + (fama_de(E, B, ladrao, lid, 'crime') // G.VIGIA_FAMA if ladrao == 'eu' else 0)
    return c


def furto_npc(E, B, pid, r):
    """o ladino de nome furta alguém que está no mesmo ponto que ele, pelo dado do mundo e a mesma conta do personagem"""
    p = E['gente'][pid]; lid = p['lugar']; bloco = 3; sp = ponto(E, B, pid, bloco)[0]
    alvos = [k for k in nomeados(E, B, lid) if k != pid and ponto(E, B, k, bloco)[0] == sp and E['gente'][k]['moedas'] > 0]
    if not alvos: return
    v = r.choice(alvos); c = contra_furto(E, B, pid, v, bloco)
    t = d2(r) + p['atributos']['Agilidade'] // 10 + (p.get('maestria') or {}).get('manha', 0)
    STATS['furtos_npc'] += 1
    if t >= c:
        n = min(E['gente'][v]['moedas'], r.randint(1, 6) * (1 + (p.get('maestria') or {}).get('manha', 0) // 2))
        estado.aplica(E, 'mestre', [['pessoa', v, 'moedas', 'soma', -n], ['pessoa', pid, 'moedas', 'soma', n]], onde=lid, quem=[pid, v], texto='furto (fora de cena)')
        if r.random() < G.DA_FALTA:
            estado.aplica(E, 'mestre', [['lugar', lid, 'vigia', 'poe', (E['lugares'][lid].get('vigia') or [])[-3:] + [E['relogio']['dia']]]], onde=lid, texto='a vila fica de olho')
            bgrava(E, B, 'furto', noticia(E, B, lid, 'suspeita', None, f"sumiu prata da bolsa de {E['gente'][v]['nome']}", alcance=1))
    elif c - t >= 5:
        STATS['furtos_npc_pegos'] += 1; multa = min(p['moedas'], 3 * r.randint(1, 6))
        if multa: estado.aplica(E, 'mestre', [['pessoa', pid, 'moedas', 'soma', -multa], ['estoque', lid, 'prata', 'soma', multa]], onde=lid, quem=[pid], texto='o ladrão paga a multa')
        bgrava(E, B, 'furto', [['laco', v, pid, 'soma', -6]] + noticia(E, B, lid, 'roubou', None, f"{p['nome']} foi pego com a mão na bolsa de {E['gente'][v]['nome']}", alcance=2))


# ====================================================================== o dia do mundo (o que roda na virada)
def gente_dia(E, B):
    hoje = E['relogio']['dia']
    for k in nomeados(E, B):                  # quem viajava volta
        v = gb(B, k).get('viagem')
        if v and hoje >= v['volta']:
            estado.aplica(E, 'mestre', [['pessoa', k, 'lugar', 'poe', v['casa']]], onde=v['casa'], quem=[k], texto='volta de viagem'); bgrava(E, B, 'viagem', [['viagem', k, 'poe', None]])
    noticias_andam(E, B)
    caixa_dia(E, B)
    missoes_dia(E, B)
    for k in nomeados(E, B):
        if sum(map(ord, k)) % 7 == hoje % 7: semana(E, B, k)


# ====================================================================== a encomenda ao personagem, a resposta da caixa, a entrega
def troca_peca(E, B, cli, iid, lid):
    """a peça nova vai ao uso; a velha do mesmo lugar do corpo (se havia) se derrete na forja de quem fez: sai do Livro, e a matéria dela entra no estoque do lugar"""
    nova = E['itens']['itens'][iid]; uso = 'arma' if nova['tipo'] == 'arma' else 'escudo' if nova['tipo'] == 'escudo' else 'veste'; ef = []
    for it in pecas_de(E, cli):
        if it['id'] != iid and it.get('uso') == uso and (uso != 'veste' or set(it.get('cobre') or []) & set(nova.get('cobre') or [])):
            mat = oficio._materia_conserto(it)
            ef += [['item', it['id'], 'uso', 'poe', None], ['item', it['id'], 'dono', 'poe', None], ['item', it['id'], 'some']] + ([['estoque', lid, mat, 'soma', 1]] if mat else [])
    ef.append(['item', iid, 'uso', 'poe', uso])
    estado.aplica(E, 'mestre', ef, onde=lid, quem=[cli], texto='a peça nova em uso; a velha vai ao fogo')


def encomendar(E, B, cli, peca):
    """o cliente que tem a prata escolhe o ferreiro (pela fama de ofício, pela opinião ou pelo laço, pelo preço, e perto): se é o personagem, a caixa; senão, fora de cena"""
    lid = E['gente'][cli]['lugar']; fs = ferreiros(E, B, lid, peca['cat'])
    if not fs: return None
    r = estado.sorte(E, f'escolhe|{cli}'); ws = [peso_ferreiro(E, B, cli, f) for f in fs]
    if not any(ws): return None
    f = r.choices(fs, ws)[0]
    if f != 'eu': return encomenda_npc(E, B, cli, peca, sem='eu')
    preco = round(preco_peca(peca) * (gb(B, 'eu').get('preco') or 1.0)); STATS['enc_eu'] += 1
    nome = peca.get('familia') or (f"armadura de {peca['material']}" if peca['tipo'] == 'armadura' else 'escudo')
    return caixa_abre(E, B, cli, f"{nome} {T.CATS[peca['cat']]} por {preco} de prata ({round(preco * G.SINAL)} de sinal; entrega em {oficio.O.blocos(peca['cat']) // 2 + G.PRAZO_OBRA} dias)",
                      'encomenda', G.PRAZO_RESPOSTA, dict(peca_do_oficio=papel(B, cli)), dict(a='aceitar', b='pedir 20% a mais', c='recusar'), 'c',
                      'ele vai a outro ferreiro e lembra que você calou', peca=peca, preco=preco)


def responde(E, B, cid, letra):
    """o personagem responde um item da caixa (no motor: `caixa.py responde ID LETRA`, ligado às perguntas do turno)"""
    c = B['caixa']['abertos'][cid]; de = c['de']; lid = E['gente'][de]['lugar']; hoje = E['relogio']['dia']; efb = [['caixa', cid, 'fecha', 'feitos']]
    if c['m'] == 'encomenda':
        if letra == 'c':
            bgrava(E, B, 'caixa', efb + lembra(E, B, de, 'recusou')); encomenda_npc(E, B, de, c['peca'], sem='eu'); return 'recusou'
        preco = c['preco'] if letra == 'a' else round(c['preco'] * 1.2)
        if letra == 'b' and opiniao(E, B, de) < 2:
            bgrava(E, B, 'caixa', efb + lembra(E, B, de, 'recusou')); encomenda_npc(E, B, de, c['peca'], sem='eu'); return 'o cliente não aceitou o preço'
        if E['gente'][de]['moedas'] < preco: bgrava(E, B, 'caixa', efb); return 'o cliente não tem a prata'
        sinal = round(preco * G.SINAL)
        estado.aplica(E, 'mestre', [['pessoa', de, 'moedas', 'soma', -preco], ['pessoa', 'eu', 'moedas', 'soma', sinal], ['estoque', 'custodia', 'prata', 'soma', preco - sinal]], onde=lid, quem=[de, 'eu'],
                      texto='a encomenda: o sinal vem, o resto fica guardado')
        bgrava(E, B, 'caixa', efb + [['missao', 'abre', dict(de=de, tipo='encomenda', grau='F', paga=preco - sinal, sinal=sinal, caucao=0, peca=c['peca'], prazo=hoje + oficio.O.blocos(c['peca']['cat']) // 2 + G.PRAZO_OBRA,
                                                                  onde=lid, quem='eu', estado='pega')]])
        STATS['enc_aceitas'] = STATS.get('enc_aceitas', 0) + 1; STATS['sinal'] = STATS.get('sinal', 0) + sinal
        return 'aceitou'
    if c['m'] == 'conserto':
        it = E['itens']['itens'].get(c['item'])
        if letra != 'a' or not it or it.get('dono') != de or E['gente'][de]['moedas'] < c['valor']: bgrava(E, B, 'caixa', efb + (lembra(E, B, de, 'recusou') if letra != 'a' else [])); return 'não'
        import ato
        mat = oficio._materia_conserto(it); n = math.ceil(c['pontos'] / 10); antes = E['gente']['eu']['moedas']
        try:
            if mat and (E['gente']['eu'].get('carga') or {}).get(mat, 0) < n: mercado.comprar(E, 'eu', mat, n - (E['gente']['eu'].get('carga') or {}).get(mat, 0))
            ato.passa(E, 'eu', math.ceil(c['pontos'] / 5), 'consertar', esforco='pesado', texto='conserta a peça de um cliente', mais=lambda i: [['pessoa', 'eu', 'treino.forja', 'soma', 1]])
        except SystemExit: bgrava(E, B, 'caixa', efb); return 'não deu'
        STATS['cons_materia'] = STATS.get('cons_materia', 0) + antes - E['gente']['eu']['moedas']
        estado.aplica(E, 'mestre', [['item', it['id'], 'dur', 'soma', c['pontos']], ['pessoa', de, 'moedas', 'soma', -c['valor']], ['pessoa', 'eu', 'moedas', 'soma', c['valor']]]
                      + ([['pessoa', 'eu', 'carga.' + mat, 'soma', -n]] if mat else []), onde=lid, quem=['eu', de], texto='o conserto do cliente')
        bgrava(E, B, 'caixa', efb + lembra(E, B, de, 'pagou'))
        STATS['cons_paga'] = STATS.get('cons_paga', 0) + c['valor']; return 'consertou'
    if c['m'] == 'missao':
        mid = c['missao']; m = B['missoes']['itens'][mid]
        if letra == 'a' and m['estado'] == 'aberta' and E['gente']['eu']['moedas'] >= m['caucao']:
            estado.aplica(E, 'mestre', [['pessoa', 'eu', 'moedas', 'soma', -m['caucao']], ['estoque', 'custodia', 'prata', 'soma', m['caucao']]], onde=m['onde'], quem=['eu'], texto='pega a missão (a caução)')
            bgrava(E, B, 'caixa', efb + [['missao', mid, 'quem', 'poe', 'eu'], ['missao', mid, 'estado', 'poe', 'pega']]); return 'pegou'
        bgrava(E, B, 'caixa', efb + lembra(E, B, de, 'recusou') + [['missao', mid, 'dirigida', 'poe', None]]); return 'recusou'
    if c['m'] == 'cobranca':
        if letra == 'a' and E['gente']['eu']['moedas'] >= c['valor']:
            estado.aplica(E, 'mestre', [['pessoa', 'eu', 'moedas', 'soma', -c['valor']], ['pessoa', de, 'moedas', 'soma', c['valor']]], onde=lid, quem=['eu', de], texto='paga a cobrança')
            i = next((k for k, f in enumerate(gb(B, de)['mem']) if f[:2] == c['mot']['memoria']), None)
            bgrava(E, B, 'caixa', efb + ([['memoria', de, 'esquece', i]] if i is not None else []) + lembra(E, B, de, 'pagou')); STATS['cobrancas_pagas'] = STATS.get('cobrancas_pagas', 0) + c['valor']; return 'pagou'
        bgrava(E, B, 'caixa', efb + lembra(E, B, de, 'calou') + [['fama', 'eu', lid, 'crime', 'soma', 5]]); return 'negou'
    if c['m'] == 'oferta':
        if letra == 'a' and E['gente'][de]['moedas'] >= c['valor']:
            estado.aplica(E, 'mestre', [['pessoa', de, 'moedas', 'soma', -c['valor']], ['pessoa', 'eu', 'moedas', 'soma', c['valor']]], onde=lid, quem=['eu', de], texto='aceita o presente')
            STATS['ofertas'] = STATS.get('ofertas', 0) + c['valor']
        bgrava(E, B, 'caixa', efb); return 'aceitou'


def entrega(E, B, mid, iid):
    """a encomenda entregue: a peça passa ao cliente; o resto guardado vem ao ferreiro (menos o atraso, que volta ao cliente); a memória e a notícia"""
    m = B['missoes']['itens'][mid]; de = m['de']; hoje = E['relogio']['dia']; atraso = max(0, hoje - m['prazo'])
    desc = round(m['paga'] * min(0.5, atraso * G.ATRASO)); lid = m['onde']
    ef = [['item', iid, 'dono', 'poe', de], ['estoque', 'custodia', 'prata', 'soma', -m['paga']], ['pessoa', 'eu', 'moedas', 'soma', m['paga'] - desc]]
    if desc: ef.append(['pessoa', de, 'moedas', 'soma', desc])
    estado.aplica(E, 'mestre', ef, onde=lid, quem=['eu', de], texto='a encomenda entregue')
    troca_peca(E, B, de, iid, E['gente']['eu']['lugar'])
    tipo = 'entregou' if not atraso else 'entregou_tarde'
    bgrava(E, B, 'missao', [['missao', mid, 'fecha', 'cumprida']] + lembra(E, B, de, tipo) +
           noticia(E, B, lid, tipo, 'eu', f"o ferreiro de {E['lugares'][E['gente']['eu']['lugar']]['nome']} fez a peça de {E['gente'][de]['nome']}", 'ofício', G.FATOS[tipo][2] * (1 + 2 * m['peca']['cat']), peso=1))
    STATS['enc_entregues'] = STATS.get('enc_entregues', 0) + 1; STATS['enc_resto'] = STATS.get('enc_resto', 0) + m['paga'] - desc


def falha_encomenda(E, B, mid):
    """passou uma semana do prazo sem a peça: o resto guardado volta ao cliente, e o ferreiro devolve o sinal em dobro (o que tiver)"""
    m = B['missoes']['itens'][mid]; de = m['de']; devolve = min(E['gente']['eu']['moedas'], 2 * m['sinal'])
    estado.aplica(E, 'mestre', [['estoque', 'custodia', 'prata', 'soma', -m['paga']], ['pessoa', de, 'moedas', 'soma', m['paga'] + devolve], ['pessoa', 'eu', 'moedas', 'soma', -devolve]], onde=m['onde'], quem=['eu', de], texto='a encomenda falhou')
    bgrava(E, B, 'missao', [['missao', mid, 'fecha', 'falhada']] + lembra(E, B, de, 'falhou_obra') + noticia(E, B, m['onde'], 'falhou_obra', 'eu', 'não entregou a peça prometida', 'ofício', -3, peso=-2))
    STATS['enc_falhas'] = STATS.get('enc_falhas', 0) + 1


def encomendas_dia(E, B):
    hoje = E['relogio']['dia']
    for mid, m in list(B['missoes']['itens'].items()):
        if m['tipo'] == 'encomenda' and m['estado'] == 'pega' and hoje > m['prazo'] + 7: falha_encomenda(E, B, mid)


_COVIL = {}
def covil_dia(E, B):
    """o arremedo do aviso: o bando da toca roubou a vila ontem (a comida do ermo subiu sem caça): o alcaide tem motivo para a missão, e a vila fala disso"""
    for lid, l in E['lugares'].items():
        if not l.get('covil'): continue
        tem = (l.get('estoque') or {}).get('comida', 0) + (l.get('estoque') or {}).get('prata', 0); antes = _COVIL.get(lid, tem); _COVIL[lid] = tem
        if tem > antes:
            for v in l.get('vizinhos') or []:
                if E['lugares'][v].get('pop'):
                    LOG_COVIL[v] = 1
                    bgrava(E, B, 'covil', noticia(E, B, v, 'ataque', None, f"os goblins da {l['nome']} levaram comida de {E['lugares'][v]['nome']}", alcance=1))


def loja_dia(E, B):
    """ARREMEDO da freguesia de A: o povo leva peças Comuns da prateleira; uma vez por semana, a loja que ficou abaixo do alvo pede ao ferreiro uma peça para repor
    (o mercador é quem pede; a paga sai do caixa do lugar, que é o da loja)"""
    hoje = E['relogio']['dia']
    for lid, l in E['lugares'].items():
        if not l.get('pop') or l.get('tipo') not in G.FREGUESIA: continue
        r = estado.sorte(E, f'freguesia|{lid}'); x = G.FREGUESIA[l['tipo']] / 7
        if r.random() < x:
            pr = [it for it in mercado.prateleira(E, lid).values() if it['cat'] == 0 and it.get('tipo') in ('arma', 'armadura', 'escudo')]
            if pr: it = r.choice(pr); estado.aplica(E, 'mestre', [['item', it['id'], 'onde', 'poe', None], ['item', it['id'], 'some']], onde=lid, texto='o povo leva uma peça da prateleira (arremedo)'); STATS['freguesia'] = STATS.get('freguesia', 0) + 1
        if hoje % 7 != (sum(map(ord, lid)) % 7): continue
        merc = next((k for k in nomeados(E, B, lid) if papel(B, k) == 'mercador'), None)
        alvo = (l.get('alvo_pecas') or {}).get('0', 0); tem = sum(1 for it in mercado.prateleira(E, lid).values() if it['cat'] == 0)
        if not merc or tem >= alvo or any(c['m'] == 'loja' and c['de'] == merc for c in B['caixa']['abertos'].values()): continue
        peca = r.choice([dict(tipo='arma', cat=0, familia=f) for f in ('espada', 'lança', 'machado', 'maça')] + [dict(tipo='escudo', cat=0)])
        preco = round(preco_peca(peca) * G.LOJA_PAGA); fs = [f for f in ferreiros(E, B, lid, 0)]
        if not fs or l['estoque'].get('prata', 0) < preco: continue
        ws = [peso_ferreiro(E, B, merc, f) for f in fs]; f = r.choices(fs, ws)[0]
        if f == 'eu':
            STATS['loja_eu'] = STATS.get('loja_eu', 0) + 1
            caixa_abre(E, B, merc, f"para a loja: {peca.get('familia') or 'escudo'} Comum, por {preco} de prata (a loja repõe a prateleira)", 'loja', G.PRAZO_RESPOSTA * 2, dict(prateleira=f'{tem} de {alvo}'),
                       dict(a='aceitar', b='recusar'), 'b', 'o mercador pede a outro', peca=peca, preco=preco)
        else:
            mat = oficio.materia_de(dict(peca)); custo = sum(math.ceil(mercado._base(k)) * n for k, n in mat.items()); lf = E['gente'][f]['lugar']
            it = item(peca['tipo'], 0, familia=peca.get('familia'), onde=lid, feito_por=f)
            estado.aplica(E, 'mestre', [['item', 'nasce', it], ['estoque', lid, 'prata', 'soma', -preco], ['pessoa', f, 'moedas', 'soma', preco - custo], ['estoque', lf, 'prata', 'soma', custo]], onde=lid, texto='a loja repõe (fora de cena)')
            STATS['loja_npc'] = STATS.get('loja_npc', 0) + 1


def entrega_loja(E, B, c, iid):
    lid = E['gente'][c['de']]['lugar']
    estado.aplica(E, 'mestre', [['item', iid, 'uso', 'poe', None], ['item', iid, 'dono', 'poe', None], ['item', iid, 'onde', 'poe', lid], ['estoque', lid, 'prata', 'soma', -c['preco']], ['pessoa', 'eu', 'moedas', 'soma', c['preco']]],
                  onde=lid, quem=['eu'], texto='a peça para a loja')
    bgrava(E, B, 'loja', lembra(E, B, c['de'], 'entregou') + [['fama', 'eu', lid, 'ofício', 'soma', 1]])
    STATS['loja_paga'] = STATS.get('loja_paga', 0) + c['preco']


def gente_dia_tudo(E, B):
    covil_dia(E, B); encomendas_dia(E, B); loja_dia(E, B); gente_dia(E, B)


def fama_bancada(E, B, antes):
    """quem serve na bancada fica conhecido: +1 de fama de ofício no lugar a cada FAMA_BANCADA blocos de bancada"""
    agora = (E['gente']['eu'].get('treino') or {}).get('forja', 0); n = agora // G.FAMA_BANCADA - antes // G.FAMA_BANCADA
    if n > 0: bgrava(E, B, 'fama', [['fama', 'eu', E['gente']['eu']['lugar'], 'ofício', 'soma', n]])


# ====================================================================== a MESA da gente (o rascunho das seções do projeto B)
def mesa_b(E, B, quantos=8):
    """as seções do projeto B na MESA: quem está aqui (o que faz, o que quer, o que lembra de você), a caixa por prazo, as missões do quadro, as notícias
    chegadas e dois fatos que não tocam você. Devolve as linhas."""
    eu = E['gente']['eu']; lid = eu['lugar']; hoje = E['relogio']['dia']; L = ['## Quem está aqui']
    ks = nomeados(E, B, lid)
    def chave(k):
        sp = ponto(E, B, k)[0]; op = opiniao(E, B, k)
        return (sp not in ('casa', 'santuário', 'pousada', 'ermo'), abs(op), len(gb(B, k)['mem']))
    ks.sort(key=chave, reverse=True)
    for k in ks[:quantos]:
        q = E['gente'][k]; sp, at = ponto(E, B, k); op = opiniao(E, B, k); g = gb(B, k)
        mem = sorted((f for f in g['mem'] if f[3] == 'eu'), key=lambda f: -abs(peso_atual(f, hoje)))[:2]
        pq = '; '.join(G.FATOS[f[1]][4] if f[1] != 'ouviu' else f"ouviu: {f[5] if len(f) > 5 else 'falar de você'}" for f in mem)
        qu = g.get('querer') or {}
        quer = f"; junta para {qu['peca'].get('familia') or qu['peca'].get('material') or 'escudo'}" if qu.get('t') == 'juntar' else ''
        L.append(f"- {q['nome']} ({g['papel']}), {at} ({sp}) · {palavra(op)} ({op:+d}" + (f": {pq})" if pq else ")") + quer)
    if len(ks) > quantos: L.append(f"- e mais {len(ks) - quantos} (`gente.py aqui`)")
    ab = sorted(B['caixa']['abertos'].values(), key=lambda c: c['prazo'])
    L += ['', f'## A caixa ({len(ab)} de {G.CAIXA})']
    for c in ab:
        falta = c['prazo'] - estado.agora(E)
        L.append(f"- {c['id']} · {E['gente'][c['de']]['nome']} quer {c['pede']} · prazo: {falta // 6} dias e {falta % 6} blocos · " + ' · '.join(f"{k}) {v}" for k, v in c['op'].items()) +
                 f" · calado: {c['op'][c['pad']]} ({c['custo']})")
    qd = [m for m in B['missoes']['itens'].values() if m['estado'] == 'aberta' and m['onde'] == lid][:4]
    if qd:
        L += ['', '## O quadro (missões daqui)'] + [f"- {m['id']} · {E['gente'][m['de']]['nome'] if m['de'] in E['gente'] else m['de']}: {m['tipo']} ({m['alvo']}), grau {m['grau']}, {m['paga']} de prata, caução {m['caucao']}, até o Dia {m['prazo']}" for m in qd]
    ch = sorted((n for n in B['noticias']['ativas'].values() if lid in n['em']), key=lambda n: -n['em'][lid][0])
    minhas = [n for n in ch if n.get('s') == 'eu'][:3]; outras = [n for n in ch if n.get('s') != 'eu'][:2]
    if minhas: L += ['', '## O que se diz de você'] + [f"- {'(boato) ' if n['em'][lid][1] > G.BOATO else ''}{n['x']} (Dia {n['d']}, {E['lugares'][n['de']]['nome']})" for n in minhas]
    if outras: L += ['', '## Dois fatos que não tocam você'] + [f"- {'(boato) ' if n['em'][lid][1] > G.BOATO else ''}{n['x']} (Dia {n['d']}, {E['lugares'][n['de']]['nome']})" for n in outras]
    return L
