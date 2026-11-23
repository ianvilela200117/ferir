#!/usr/bin/env python3
"""ato.py — MOTOR 10: O QUE A PESSOA FAZ, COM O TEMPO QUE CUSTA. Todo ato anda o relógio e mexe no corpo, por evento.

O ato longo PARA quando o corpo cruza um limiar (fome, sono, cansaço), e diz por quê. Quem cai no sono dorme ali mesmo, no chão.
MORTO NÃO AGE, e quem saiu para o ermo (a saída de caça ou de coleta aberta) não age na vila: o ato é recusado antes de cobrar qualquer coisa.

Uso (o personagem do jogador, ou quem=ID):
  python3 ato.py comer [carga]            uma refeição do lugar (1 de prata; fome −3; não gasta bloco). `carga`: come 1 de comida da própria carga, sem pagar
                                          (quem está no ermo só come da carga)
  python3 ato.py dormir N [chao]          N blocos de sono (a cama custa 2 de prata ao deitar; no chão é de graça e rende menos)
  python3 ato.py trabalhar N              N blocos no ofício da pessoa (o lugar paga por bloco, até a jornada: 2 blocos pagos por dia)
  python3 ato.py treinar N ARMA           N blocos de treino pesado com a arma (a maestria sobe pelos blocos)
  python3 ato.py descansar N              N blocos parado (o cansaço desce 1 por bloco)
  python3 ato.py esperar N                N blocos sem fazer nada
  python3 ato.py pecas                    as suas peças: o que está em uso e o que está guardado
  python3 ato.py vestir ITEM [arma|arma2|escudo]    empunha ou veste uma peça sua (não gasta bloco); a que estava no lugar dela vai para a guarda
  python3 ato.py tirar ITEM               guarda uma peça que estava em uso
  python3 ato.py luta nova CENARIO.json ARQ.json      monta uma luta com gente do mundo ({"id": "..."} no cenário) e a hora do dia
  python3 ato.py luta roda ARQ.json ["Nome: ordem"]...  roda até a próxima parada; no fim, a luta volta ao estado (PV, feridas, peças)
  python3 ato.py luta larga ARQ.json "por quê"        SÓ O MESTRE: dá por encerrada uma luta aberta cujo arquivo se perdeu (nada volta ao estado)
"""
import json, math, os, sys
import tabelas as T
import tabelas_mundo as M
import estado, corpo


def _vivo(E, pid):
    p = E['gente'].get(pid) or sys.exit(f'não há a pessoa "{pid}"')
    if p['estado'] != 'vivo': sys.exit(f"{p['nome']} não está vivo ({estado.morte_diz(E, p)})")
    return p


def passa(E, pid, blocos, tipo, esforco='nada', dorme=None, texto='', mais=None, para=True, com=()):
    """anda o mundo `blocos` blocos com a pessoa fazendo isto: um evento por bloco. Devolve (blocos feitos, por que parou ou None).
    com: quem vai junto (a saída ao ermo): passa os mesmos blocos, com o mesmo esforço, no mesmo evento.
    Com `para`, o ato para quando o corpo cruza um limiar; e quem cai no sono (sono 8 ou mais, Vontade falhada) dorme ali mesmo, no chão, até o sono baixar do primeiro limiar."""
    feitos = 0; porque = None
    for i in range(blocos):
        p = E['gente'][pid]
        if p['estado'] != 'vivo': porque = f"{p['nome']} não está vivo"; break
        junto = [c for c in com if c != pid and E['gente'].get(c, {}).get('estado') == 'vivo']
        antes = corpo.faixas(p); ultimo = E['relogio']['bloco'] == M.BLOCOS_DIA - 1; lid = estado.onde(E, pid)
        ef = corpo.bloco(E, pid, esforco, dorme)
        for c in junto: ef += corpo.bloco(E, c, esforco, dorme)
        ef += (mais(i) if mais else [])
        if not ultimo: estado.aplica(E, tipo, ef + [['relogio', 1]], onde=lid, quem=[pid] + junto, texto=texto)
        else:                                               # o último bloco do dia: o bloco, e depois a virada (com o relógio)
            if ef: estado.aplica(E, tipo, ef, onde=lid, quem=[pid] + junto, texto=texto)
            vir = corpo.virada(E, pid)
            for c in junto: vir += corpo.virada(E, c)
            estado.aplica(E, 'virada', vir + [['relogio', 1]], onde=lid, quem=[pid] + junto, texto='o dia vira')
            _mundo_vira(E)
        feitos += 1
        for q in [pid] + junto:
            x = E['gente'][q]
            if x['estado'] == 'vivo' and x['pv'] <= 0:
                estado.aplica(E, 'virada', [['pessoa', q, 'estado', 'poe', 'morto']], onde=estado.onde(E, q), quem=[q], texto=f"a fome leva {x['nome']}")
        p = E['gente'][pid]
        if p['estado'] != 'vivo': porque = f"{p['nome']} morreu de fome"; break
        porque = corpo.cruzou(p, antes)
        if dorme and p['corpo']['sono'] == 0 and p['corpo']['cansaco'] == 0 and p['pv'] >= estado.pv_max(p): porque = porque or f"{p['nome']} acorda descansado"
        if not dorme and p['corpo']['sono'] >= M.SONO_CAI[0]:
            r = estado.sorte(E, f'sono|{pid}'); t = r.randint(1, 20) + r.randint(1, 20) + p['atributos']['Vontade'] // 10
            if t < M.SONO_CAI[1] and para:
                n = math.ceil((p['corpo']['sono'] - (M.LIMIARES['sono'][0] - 1)) / -M.SONO_CHAO)
                k, _ = passa(E, pid, n, 'dormir', dorme='chao', texto=f"{p['nome']} cai no sono e dorme no chão", para=False, com=com)
                porque = f"{p['nome']} cai no sono onde está (Vontade {t} contra {M.SONO_CAI[1]}) e dorme {k} bloco(s) no chão"; break
        if porque and para: break
    return feitos, porque


def _mundo_vira(E):
    """o dia virou: cada módulo do mundo que tiver virada(E) roda a sua parte (o mercado produz e consome, os bichos criam...)"""
    import importlib
    for nome in M.MODULOS:
        try: mod = importlib.import_module(nome)
        except ModuleNotFoundError as e:
            if e.name != nome: raise
            continue
        if hasattr(mod, 'virada'): mod.virada(E)


def comer(E, pid, da_carga=False):
    """uma refeição: a do lugar (paga, sai do celeiro dele), ou 1 de comida da própria carga (sem pagar). Quem está no ermo só come da carga."""
    p = _vivo(E, pid); f = estado.fora(E, pid)
    if da_carga or f:
        if p.get('carga', {}).get('comida', 0) < 1: sys.exit(f"{p['nome']} não carrega comida" + (f" (e {estado.em(E, f)} não há quem sirva)" if f else ' (a refeição do lugar: `ato.py comer`)'))
        estado.aplica(E, 'comer', [['pessoa', pid, 'carga.comida', 'soma', -1], ['pessoa', pid, 'fome', 'soma', M.REFEICAO]], onde=estado.onde(E, pid), quem=[pid], texto=f"{p['nome']} come da própria carga")
        q = E['gente'][pid]; return f"{p['nome']} come da própria carga (fome {q['corpo']['fome']}; resta {q.get('carga', {}).get('comida', 0):g} de comida)"
    l = E['lugares'][p['lugar']]
    if l['estoque'].get('comida', 0) < 1: sys.exit(f"não há comida {estado.em(E, p['lugar'])}: ninguém serve refeição" + (' (você carrega comida: `ato.py comer carga`)' if p.get('carga', {}).get('comida', 0) >= 1 else ''))
    if p['moedas'] < M.REFEICAO_PRECO: sys.exit(f"a refeição custa {M.REFEICAO_PRECO} de prata; {p['nome']} tem {p['moedas']}" + (' (você carrega comida: `ato.py comer carga`)' if p.get('carga', {}).get('comida', 0) >= 1 else ''))
    estado.aplica(E, 'comer', [['pessoa', pid, 'moedas', 'soma', -M.REFEICAO_PRECO], ['estoque', p['lugar'], 'comida', 'soma', -1], ['estoque', p['lugar'], 'prata', 'soma', M.REFEICAO_PRECO],
                               ['pessoa', pid, 'fome', 'soma', M.REFEICAO]], onde=p['lugar'], quem=[pid], texto=f"{p['nome']} come {estado.em(E, p['lugar'])}")
    return f"{p['nome']} come (fome {E['gente'][pid]['corpo']['fome']}; {E['gente'][pid]['moedas']} de prata)"


def dormir(E, pid, blocos, chao=False, para=True):
    p = estado.presente(E, pid, 'dormir na vila'); l = E['lugares'][p['lugar']]; modo = 'chao' if chao or not l.get('cama') else 'cama'
    if modo == 'cama':
        if p['moedas'] < M.CAMA_PRECO: sys.exit(f"a cama custa {M.CAMA_PRECO} de prata; {p['nome']} tem {p['moedas']}. No chão é de graça: `ato.py dormir N chao`")
        estado.aplica(E, 'dormir', [['pessoa', pid, 'moedas', 'soma', -M.CAMA_PRECO], ['estoque', p['lugar'], 'prata', 'soma', M.CAMA_PRECO]], onde=p['lugar'], quem=[pid], texto=f"{p['nome']} paga a cama")
    n, pq = passa(E, pid, blocos, 'dormir', dorme=modo, texto=f"{p['nome']} dorme ({'na cama' if modo == 'cama' else 'no chão'})", para=para)
    return f"{p['nome']} dorme {n} bloco(s) {'na cama' if modo == 'cama' else 'no chão'}" + (f'. PAROU: {pq}' if pq else '')


def jornada(E, pid):
    """quantos blocos de serviço PAGO a pessoa já fez hoje (trabalhar e o jornal da oficina contam juntos; o teto é tabelas_mundo.JORNADA)"""
    m = E['gente'][pid].get('marca') or {}
    return m.get('jornada', 0) if m.get('jornada_dia') == E['relogio']['dia'] else 0


def paga_bloco(E, pid, lid, paga):
    """os efeitos de UM bloco de serviço pago pelo lugar: a prata passa do lugar para a pessoa, e o bloco conta na jornada do dia"""
    return [['estoque', lid, 'prata', 'soma', -paga], ['pessoa', pid, 'moedas', 'soma', paga],
            ['pessoa', pid, 'marca.jornada_dia', 'poe', E['relogio']['dia']], ['pessoa', pid, 'marca.jornada', 'poe', jornada(E, pid) + 1]]


def trabalhar(E, pid, blocos):
    """N blocos no ofício da pessoa. O lugar paga por bloco, até a JORNADA do dia (2 blocos pagos por pessoa, por dia); sem prata, o lugar não tem com que pagar."""
    p = estado.presente(E, pid, 'trabalhar na vila'); lid = p['lugar']; of = p.get('grau_oficio', 'diarista'); paga = M.SALARIO[of]; feitos = 0; pq = None
    for _ in range(blocos):
        if jornada(E, pid) >= M.JORNADA: pq = f"a jornada de hoje acabou ({M.JORNADA} blocos pagos por dia): {E['lugares'][lid]['nome']} não tem mais serviço para {p['nome']} hoje"
        elif E['lugares'][lid]['estoque'].get('prata', 0) < paga: pq = f"{E['lugares'][lid]['nome']} não tem prata para pagar o serviço ({paga} por bloco; tem {E['lugares'][lid]['estoque'].get('prata', 0)})"
        if pq: break
        n, pq = passa(E, pid, 1, 'trabalhar', esforco=M.ESFORCO_OFICIO[of], mais=lambda i: paga_bloco(E, pid, lid, paga), texto=f"{p['nome']} trabalha ({of})")
        feitos += n
        if pq: break
    if not feitos and pq: sys.exit(pq[0].upper() + pq[1:] + '.')
    return f"{p['nome']} trabalha {feitos} bloco(s) e recebe {feitos * paga} de prata" + (f'. PAROU: {pq}' if pq else '')


def treinar(E, pid, blocos, arma):
    if arma not in T.FAMILIAS: sys.exit(f'arma desconhecida: "{arma}" (use: {", ".join(T.FAMILIAS)})')
    p = estado.presente(E, pid, 'treinar na vila')
    n, pq = passa(E, pid, blocos, 'treinar', esforco='pesado', mais=lambda i: [['pessoa', pid, 'treino.' + arma, 'soma', 1]], texto=f"{p['nome']} treina com {arma}")
    return f"{p['nome']} treina {n} bloco(s) com {arma}" + _sobe_maestria(E, pid, arma) + (f'. PAROU: {pq}' if pq else '')


def _sobe_maestria(E, pid, arma):
    """a maestria sobe quando os blocos chegam; de Mestre para cima, só com um FEITO registrado (marca.feito_ARMA)"""
    p = E['gente'][pid]; tem = p.get('maestria', {}).get(arma, 0); blocos = p.get('treino', {}).get(arma, 0); txt = ''
    for grau, pede in sorted(M.MAESTRIA_BLOCOS.items()):
        if grau <= tem or blocos < pede: continue
        if grau >= M.MAESTRIA_FEITO and p.get('marca', {}).get(f'feito_{arma}', 0) < grau: txt = f' (tem os blocos para {T.MAESTRIAS[grau]}; falta o feito)'; break
        estado.aplica(E, 'treinar', [['pessoa', pid, 'maestria.' + arma, 'poe', grau]], onde=p['lugar'], quem=[pid], texto=f"{p['nome']} chega a {T.MAESTRIAS[grau]} em {arma}")
        tem = grau; txt = f'. MAESTRIA: {T.MAESTRIAS[grau]} em {arma}'
    return txt


def descansar(E, pid, blocos):
    estado.presente(E, pid, 'descansar na vila')
    n, pq = passa(E, pid, blocos, 'descansar', esforco='descanso', texto='descansa'); return f"{E['gente'][pid]['nome']} descansa {n} bloco(s)" + (f'. PAROU: {pq}' if pq else '')


def esperar(E, pid, blocos):
    estado.presente(E, pid, 'esperar na vila')
    n, pq = passa(E, pid, blocos, 'esperar', texto='espera'); return f"{E['gente'][pid]['nome']} espera {n} bloco(s)" + (f'. PAROU: {pq}' if pq else '')


# ---------- vestir, empunhar, guardar ----------
USO_DO_TIPO = dict(arma='arma', escudo='escudo', armadura='veste')
USO_DIZ = dict(arma='na mão', arma2='de reserva', escudo='no braço', veste='vestida')


def diz_pecas(E, pid):
    """as peças da pessoa, uma linha cada: o que está em uso (e onde) e o que está guardado; e os núcleos"""
    L = []
    for i, it in E['itens']['itens'].items():
        if it.get('dono') != pid: continue
        cat = T.CATS[it['cat']]
        if it['tipo'] == 'nucleo': L.append(f"{i} {it['nome']} ({cat}) · núcleo, guardado"); continue
        L.append(f"{i} {it['nome']} ({cat}, {it['dur'][0]}/{it['dur'][1]}" + (', QUEBRADA' if it['dur'][0] <= 0 else '') + f") · {'EM USO, ' + USO_DIZ[it['uso']] if it.get('uso') else 'guardada'}")
    return L or ['(nenhuma peça)']


def _sem_luta(E, pid):
    if any(not l['fim'] for l in E['turno']['lutas']): sys.exit('há uma luta aberta: não se troca de peça no meio dela (acabe-a primeiro)')


def vestir(E, pid, iid, uso=None):
    """empunha ou veste uma peça da pessoa (não gasta bloco). A que estava no mesmo lugar (a outra arma, o outro escudo, a armadura que cobre a mesma parte) vai para a guarda."""
    p = _vivo(E, pid); _sem_luta(E, pid); it = E['itens']['itens'].get(iid) or sys.exit(f'não há o item "{iid}" no Livro de Itens')
    if it.get('dono') != pid: sys.exit(f"{it['nome']} ({iid}) não é de {p['nome']}")
    if it['tipo'] not in USO_DO_TIPO: sys.exit(f"{it['nome']} não se veste nem se empunha")
    uso = uso or USO_DO_TIPO[it['tipo']]
    if uso not in estado.PARTES_VESTE or (it['tipo'] == 'arma') != (uso in ('arma', 'arma2')) or (uso == 'escudo') != (it['tipo'] == 'escudo'):
        sys.exit(f"{it['nome']} é {it['tipo']}: vai em " + ('arma (na mão) ou arma2 (de reserva)' if it['tipo'] == 'arma' else USO_DO_TIPO[it['tipo']]) + f' (veio "{uso}")')
    if it.get('uso') == uso: sys.exit(f"{it['nome']} já está em uso ({USO_DIZ[uso]})")
    eq = estado.pecas(E, pid); saem = []
    if uso != 'veste' and eq[uso] and eq[uso]['id'] != iid: saem.append(eq[uso])
    if uso == 'veste': saem += [o for o in eq['veste'] if o['id'] != iid and set(o.get('cobre') or []) & set(it.get('cobre') or [])]
    ef = [['item', o['id'], 'uso', 'poe', None] for o in saem] + [['item', iid, 'uso', 'poe', uso]]
    estado.aplica(E, 'vestir', ef, onde=estado.onde(E, pid), quem=[pid], texto=f"{p['nome']} {'veste' if uso == 'veste' else 'empunha'} {it['nome']}" + (f" (guarda {', '.join(o['nome'] for o in saem)})" if saem else ''))
    aviso = ''
    arma = estado.pecas(E, pid)['arma']
    if arma and T.FAMILIAS[arma['familia']]['maos'] == 2 and estado.pecas(E, pid)['escudo']: aviso = f"\nAVISO: {arma['nome']} pede as duas mãos: o escudo não entra na conta enquanto ela estiver na mão."
    return f"{p['nome']} {'veste' if uso == 'veste' else 'empunha'} {it['nome']} ({USO_DIZ[uso]})" + (f"; vai para a guarda: {', '.join(o['nome'] for o in saem)}" if saem else '') + '.' + aviso + '\n' + _ficha(E, pid)


def tirar(E, pid, iid):
    """guarda uma peça que estava em uso (não gasta bloco)"""
    p = _vivo(E, pid); _sem_luta(E, pid); it = E['itens']['itens'].get(iid) or sys.exit(f'não há o item "{iid}" no Livro de Itens')
    if it.get('dono') != pid: sys.exit(f"{it['nome']} ({iid}) não é de {p['nome']}")
    if not it.get('uso'): sys.exit(f"{it['nome']} já está guardada")
    estado.aplica(E, 'vestir', [['item', iid, 'uso', 'poe', None]], onde=estado.onde(E, pid), quem=[pid], texto=f"{p['nome']} guarda {it['nome']}")
    return f"{p['nome']} guarda {it['nome']}.\n" + _ficha(E, pid)


def _ficha(E, pid):
    import pessoas
    return pessoas.linha(pessoas.ficha(estado.lutador(E, pid)))


# ---------- a luta dentro do mundo ----------
def _arq_luta(arq):
    """o caminho de verdade de um arquivo de luta: como veio, ou dentro da pasta do save (é assim que o save o guarda)"""
    if os.path.exists(arq): return arq
    if os.path.exists(estado.arq_abre(arq)): return estado.arq_abre(arq)
    sys.exit(f'não há o arquivo de luta "{arq}" (nem na pasta do save, {estado.pasta()}). Se ele se perdeu: `ato.py luta larga {arq} "por quê"`')


def luta_nova(E, arq_cenario, arq_luta):
    """monta a luta: quem tem "id" no cenário vem do estado (o que veste hoje, o PV, as feridas, a pena do corpo); de noite, fica escuro"""
    import luta
    from pessoas import padrao, veste
    from itens import cat_i
    if not os.path.exists(arq_cenario): sys.exit(f'não há o cenário "{arq_cenario}"')
    try: C = json.load(open(arq_cenario, encoding='utf-8'))
    except ValueError as x: sys.exit(f'o cenário "{arq_cenario}" não é JSON: {x}')
    if not isinstance(C, dict) or not isinstance(C.get('A'), list) or not isinstance(C.get('B'), list) or not C['A'] or not C['B']: sys.exit('o cenário pede os dois lados: "A": [...] e "B": [...], cada um com alguém')
    def peca(x, tipo):
        if x is None or x is False: return x
        return cat_i(x) if tipo == 'escudo' else (x[0], cat_i(x[1]))
    def pessoa(d):
        if not isinstance(d, dict): sys.exit(f'cada lutador do cenário é um registro {{...}} (veio {json.dumps(d, ensure_ascii=False)})')
        d = dict(d)
        if 'id' in d:
            pid = d.pop('id')
            if pid not in E['gente']: sys.exit(f'não há a pessoa "{pid}" no mundo')
            if E['gente'][pid]['estado'] != 'vivo': sys.exit(f'{E["gente"][pid]["nome"]} não está vivo')
            return estado.lutador(E, pid, **d)
        if isinstance(d.get('bicho'), str):                 # o atalho do bicho: a espécie inteira sai da tabela (o nível, se vier, não conta)
            import bichos
            esp = d.pop('bicho'); d.pop('nivel', None); return bichos.bicho(esp, **d)
        if 'nome' not in d or 'nivel' not in d: sys.exit(f'quem não vem do mundo ("id") nem é bicho ("bicho") pede "nome" e "nivel" (veio {json.dumps(d, ensure_ascii=False)[:80]})')
        v = d.pop('veste', {})
        p = padrao(d.pop('nome'), d.pop('nivel'), molde=d.pop('molde', 'guerreiro'), maestria=d.pop('maestria', None), atributos=d.pop('atributos', None), **d)
        return veste(p, arma=peca(v.get('arma'), 'arma'), arma2=peca(v.get('arma2'), 'arma'), armadura=peca(v.get('armadura'), 'armadura'), elmo=peca(v.get('elmo'), 'armadura'), escudo=peca(v.get('escudo'), 'escudo'))
    tempo = list(C.get('tempo') or [])
    if E['relogio']['bloco'] in M.ESCUROS and not C.get('luz') and 'escuro' not in tempo: tempo.append('escuro')
    S = luta.nova([pessoa(x) for x in C['A']], [pessoa(x) for x in C['B']], inicio=C.get('inicio', 'perto'), lugar=C.get('lugar'), tempo=tempo, surpresa=C.get('surpresa'))
    S['mundo'] = True; S['comecou'] = True; luta.salva(S, arq_luta)
    E['turno']['lutas'].append(dict(arq=estado.arq_guarda(arq_luta), fim=None)); estado.grava(E)
    return luta.situacao(S)


def luta_roda(E, arq_luta, ordens):
    import luta
    arq_luta = _arq_luta(arq_luta); S = json.load(open(arq_luta, encoding='utf-8'))
    if S['fim']: sys.exit('esta luta já acabou.')
    for o in ordens: luta.ordem(S, o)
    S['log'] = []; fim = luta.corre(S, interativo=True); luta.salva(S, arq_luta)
    out = '\n'.join(S['log']) + '\n\n' + luta.situacao(S)
    if fim == 'fim': out += '\n\nFIM: ' + luta.resultado_diz(S) + '\n' + luta_fecha(E, S, arq_luta)
    return out


def luta_fecha(E, S, arq_luta=None):
    """a luta acabada volta ao estado, num evento só: PV, feridas novas, mortes, o cansaço, a durabilidade das peças"""
    ef = []; quem = []; linhas = []
    for f in S['L']:
        pid = f.get('id')
        if not pid or pid not in E['gente']: continue
        p = E['gente'][pid]; quem.append(pid); morto = f['estado'] == 'morto'
        pv = 0 if morto else max(1, f['pv'])               # quem caiu e foi estancado fica com 1
        if pv != p['pv']: ef.append(['pessoa', pid, 'pv', 'soma', pv - p['pv']])
        for parte, grave in f['feridas'][f['feridas_antes']:]: ef.append(['ferida', pid, 'abre', parte, grave])
        if morto: ef.append(['pessoa', pid, 'estado', 'poe', 'morto'])
        else: ef.append(['pessoa', pid, 'cansaco', 'soma', M.LUTA_CANSA])
        linhas.append(f"  {p['nome']}: {'MORTO' if morto else f'PV {pv}'}" + (f", {len(f['feridas']) - f['feridas_antes']} ferida(s) nova(s)" if len(f['feridas']) > f['feridas_antes'] else ''))
    for it in S['itens'].values():
        iid = it.get('id')
        if iid in E['itens']['itens'] and it['dur'][0] != E['itens']['itens'][iid]['dur'][0]:
            ef.append(['item', iid, 'dur', 'soma', it['dur'][0] - E['itens']['itens'][iid]['dur'][0]])
            if it['dur'][0] <= 0: linhas.append(f"  {it['nome']} QUEBROU")
    antes = {pid: corpo.faixas(E['gente'][pid]) for pid in quem}
    import luta
    if ef: estado.aplica(E, 'luta', ef, onde=estado.onde(E, quem[0]) if quem else None, quem=quem, texto='luta: ' + luta.resultado_diz(S).split(' · feridas')[0])
    for pid in quem:
        c = corpo.cruzou(E['gente'][pid], antes[pid]) if E['gente'][pid]['estado'] == 'vivo' else None
        if c: linhas.append(f"  {c} (a luta cansa)")
    for l in E['turno']['lutas']:
        if arq_luta and l['arq'] == estado.arq_guarda(arq_luta): l['fim'] = S['fim']
    return 'A LUTA VOLTOU AO ESTADO:\n' + '\n'.join(linhas)


def luta_larga(E, arq_luta, porque):
    """SÓ O MESTRE: dá por encerrada uma luta aberta (o arquivo se perdeu, a cena mudou). Nada volta ao estado: o que o Mestre decidir entra por evento "mestre"."""
    g = estado.arq_guarda(arq_luta); abertas = [l for l in E['turno']['lutas'] if not l['fim'] and (l['arq'] == g or l['arq'] == arq_luta or os.path.basename(l['arq']) == os.path.basename(arq_luta))]
    if not abertas: sys.exit(f'não há luta aberta com o arquivo "{arq_luta}"' + (f" (abertas: {', '.join(l['arq'] for l in E['turno']['lutas'] if not l['fim'])})" if any(not l['fim'] for l in E['turno']['lutas']) else ''))
    if not porque.strip(): sys.exit('diga por quê a luta é largada')
    for l in abertas: l['fim'] = 'largada'
    E['turno']['notas'].append(f"luta largada ({abertas[0]['arq']}): {porque}")
    return f"luta largada: {abertas[0]['arq']} ({porque}). Nada voltou ao estado: o que houve nela entra por `estado.py mestre`."


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: print(__doc__); sys.exit()
    op = dict(x.split('=', 1) for x in a if '=' in x and ':' not in x); pos = [x for x in a if '=' not in x or ':' in x]
    cmds = ('comer', 'dormir', 'trabalhar', 'treinar', 'descansar', 'esperar', 'pecas', 'vestir', 'tirar', 'luta')
    if not pos or pos[0] not in cmds: print(__doc__); sys.exit()
    E = estado.carrega(); pid = op.get('quem') or estado.eu(E)
    if pid not in E['gente']: sys.exit(f'não há a pessoa "{pid}"')
    n = lambda i: int(pos[i]) if len(pos) > i and pos[i].isdigit() and int(pos[i]) >= 1 else sys.exit('diga quantos blocos (1 ou mais). Um bloco são 4 horas.')
    if pos[0] == 'pecas': print('\n'.join(diz_pecas(E, pid))); sys.exit()
    if pos[0] == 'comer': out = comer(E, pid, da_carga='carga' in pos[1:])
    elif pos[0] == 'dormir': out = dormir(E, pid, n(1), chao='chao' in pos)
    elif pos[0] == 'trabalhar': out = trabalhar(E, pid, n(1))
    elif pos[0] == 'treinar' and len(pos) > 2: out = treinar(E, pid, n(1), pos[2])
    elif pos[0] == 'descansar': out = descansar(E, pid, n(1))
    elif pos[0] == 'esperar': out = esperar(E, pid, n(1))
    elif pos[0] == 'vestir' and len(pos) in (2, 3): out = vestir(E, pid, pos[1], pos[2] if len(pos) > 2 else None)
    elif pos[0] == 'tirar' and len(pos) == 2: out = tirar(E, pid, pos[1])
    elif pos[:2] == ['luta', 'nova'] and len(pos) == 4: print(luta_nova(E, pos[2], pos[3])); sys.exit()
    elif pos[:2] == ['luta', 'roda'] and len(pos) >= 3: out = luta_roda(E, pos[2], pos[3:])
    elif pos[:2] == ['luta', 'larga'] and len(pos) == 4: out = luta_larga(E, pos[2], pos[3])
    else: print(__doc__); sys.exit()
    estado.grava(E); p = E['gente'][pid]                    # grava ANTES de falar: a saída cortada não perde o que o dado rolou
    print(out)
    print(f"{estado.quando(E)} · PV {p['pv']}/{estado.pv_max(p)} · {corpo.diz(p)} · {p['moedas']} de prata")
