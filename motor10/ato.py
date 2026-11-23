#!/usr/bin/env python3
"""ato.py — MOTOR 10: O QUE A PESSOA FAZ, COM O TEMPO QUE CUSTA. Todo ato anda o relógio e mexe no corpo, por evento.

O ato longo PARA quando o corpo cruza um limiar (fome, sono, cansaço), e diz por quê.

Uso (o personagem do jogador, ou quem=ID):
  python3 ato.py comer                    uma refeição do lugar (1 de prata; fome −3; não gasta bloco)
  python3 ato.py dormir N [chao]          N blocos de sono (a cama custa 2 de prata ao deitar; no chão é de graça e rende menos)
  python3 ato.py trabalhar N              N blocos no ofício da pessoa (o lugar paga por bloco)
  python3 ato.py treinar N ARMA           N blocos de treino pesado com a arma (a maestria sobe pelos blocos)
  python3 ato.py descansar N              N blocos parado (o cansaço desce 1 por bloco)
  python3 ato.py esperar N                N blocos sem fazer nada
  python3 ato.py luta nova CENARIO.json ARQ.json      monta uma luta com gente do mundo ({"id": "..."} no cenário) e a hora do dia
  python3 ato.py luta roda ARQ.json ["Nome: ordem"]...  roda até a próxima parada; no fim, a luta volta ao estado (PV, feridas, peças)
"""
import json, os, sys
import tabelas as T
import tabelas_mundo as M
import estado, corpo


def _para_por(p, antes):
    """o porquê de parar: um medidor cruzou um limiar para cima"""
    nomes = dict(fome=['', 'está com fome', 'está faminto'], sono=['', 'está com sono', 'está caindo de sono'], cansaco=['', 'está exausto'])
    for m in M.MEDIDORES:
        if corpo.faixa(p, m) > antes[m]: return f"{p['nome']} {nomes[m][corpo.faixa(p, m)]}"
    return None


def passa(E, pid, blocos, tipo, esforco='nada', dorme=None, texto='', mais=None, para=True):
    """anda o mundo `blocos` blocos com a pessoa fazendo isto: um evento por bloco. Devolve (blocos feitos, por que parou ou None)."""
    feitos = 0; porque = None
    for i in range(blocos):
        p = E['gente'][pid]
        if p['estado'] != 'vivo': porque = f"{p['nome']} não está vivo"; break
        antes = {m: corpo.faixa(p, m) for m in M.MEDIDORES}; ultimo = E['relogio']['bloco'] == M.BLOCOS_DIA - 1
        ef = corpo.bloco(E, pid, esforco, dorme) + (mais(i) if mais else [])
        if not ultimo: estado.aplica(E, tipo, ef + [['relogio', 1]], onde=p['lugar'], quem=[pid], texto=texto)
        else:                                               # o último bloco do dia: o bloco, e depois a virada (com o relógio)
            if ef: estado.aplica(E, tipo, ef, onde=p['lugar'], quem=[pid], texto=texto)
            estado.aplica(E, 'virada', corpo.virada(E, pid) + [['relogio', 1]], onde=p['lugar'], quem=[pid], texto='o dia vira')
            _mundo_vira(E)
        feitos += 1; p = E['gente'][pid]
        if p['pv'] <= 0:
            estado.aplica(E, 'virada', [['pessoa', pid, 'estado', 'poe', 'morto']], onde=p['lugar'], quem=[pid], texto='a fome leva'); porque = f"{p['nome']} morreu de fome"; break
        porque = _para_por(p, antes)
        if dorme and p['corpo']['sono'] == 0 and p['corpo']['cansaco'] == 0 and p['pv'] >= estado.pv_max(p): porque = porque or f"{p['nome']} acorda descansado"
        if not dorme and p['corpo']['sono'] >= M.SONO_CAI[0]:
            r = estado.sorte(E, f'sono|{pid}'); t = r.randint(1, 20) + r.randint(1, 20) + p['atributos']['Vontade'] // 10
            if t < M.SONO_CAI[1]: porque = f"{p['nome']} cai no sono onde está (Vontade {t} contra {M.SONO_CAI[1]})"
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


def comer(E, pid):
    p = E['gente'][pid]; l = E['lugares'][p['lugar']]
    estado.aplica(E, 'comer', [['pessoa', pid, 'moedas', 'soma', -M.REFEICAO_PRECO], ['estoque', p['lugar'], 'comida', 'soma', -1], ['estoque', p['lugar'], 'prata', 'soma', M.REFEICAO_PRECO],
                               ['pessoa', pid, 'fome', 'soma', M.REFEICAO]], onde=p['lugar'], quem=[pid], texto=f"{p['nome']} come {l.get('em', 'em ' + l['nome'])}")
    return f"{p['nome']} come (fome {E['gente'][pid]['corpo']['fome']}; {E['gente'][pid]['moedas']} de prata)"


def dormir(E, pid, blocos, chao=False, para=True):
    p = E['gente'][pid]; l = E['lugares'][p['lugar']]; modo = 'chao' if chao or not l.get('cama') else 'cama'
    if modo == 'cama':
        estado.aplica(E, 'dormir', [['pessoa', pid, 'moedas', 'soma', -M.CAMA_PRECO], ['estoque', p['lugar'], 'prata', 'soma', M.CAMA_PRECO]], onde=p['lugar'], quem=[pid], texto=f"{p['nome']} paga a cama")
    n, pq = passa(E, pid, blocos, 'dormir', dorme=modo, texto=f"{p['nome']} dorme ({'na cama' if modo == 'cama' else 'no chão'})", para=para)
    return f"{p['nome']} dorme {n} bloco(s) {'na cama' if modo == 'cama' else 'no chão'}" + (f'. PAROU: {pq}' if pq else '')


def trabalhar(E, pid, blocos):
    p = E['gente'][pid]; of = p.get('grau_oficio', 'diarista'); paga = M.SALARIO[of]
    mais = lambda i: [['estoque', p['lugar'], 'prata', 'soma', -paga], ['pessoa', pid, 'moedas', 'soma', paga]]
    n, pq = passa(E, pid, blocos, 'trabalhar', esforco=M.ESFORCO_OFICIO[of], mais=mais, texto=f"{p['nome']} trabalha ({of})")
    return f"{p['nome']} trabalha {n} bloco(s) e recebe {n * paga} de prata" + (f'. PAROU: {pq}' if pq else '')


def treinar(E, pid, blocos, arma):
    if arma not in T.FAMILIAS: sys.exit(f'arma desconhecida: "{arma}" (use: {", ".join(T.FAMILIAS)})')
    p = E['gente'][pid]
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
    n, pq = passa(E, pid, blocos, 'descansar', esforco='descanso', texto='descansa'); return f"{E['gente'][pid]['nome']} descansa {n} bloco(s)" + (f'. PAROU: {pq}' if pq else '')


def esperar(E, pid, blocos):
    n, pq = passa(E, pid, blocos, 'esperar', texto='espera'); return f"{E['gente'][pid]['nome']} espera {n} bloco(s)" + (f'. PAROU: {pq}' if pq else '')


# ---------- a luta dentro do mundo ----------
def luta_nova(E, arq_cenario, arq_luta):
    """monta a luta: quem tem "id" no cenário vem do estado (o que veste hoje, o PV, as feridas, a pena do corpo); de noite, fica escuro"""
    import luta
    from pessoas import padrao, veste
    from itens import cat_i
    C = json.load(open(arq_cenario, encoding='utf-8'))
    def peca(x, tipo):
        if x is None or x is False: return x
        return cat_i(x) if tipo == 'escudo' else (x[0], cat_i(x[1]))
    def pessoa(d):
        d = dict(d)
        if 'id' in d:
            pid = d.pop('id')
            if pid not in E['gente']: sys.exit(f'não há a pessoa "{pid}" no mundo')
            if E['gente'][pid]['estado'] != 'vivo': sys.exit(f'{E["gente"][pid]["nome"]} não está vivo')
            return estado.lutador(E, pid, **d)
        v = d.pop('veste', {})
        p = padrao(d.pop('nome'), d.pop('nivel'), molde=d.pop('molde', 'guerreiro'), maestria=d.pop('maestria', None), atributos=d.pop('atributos', None), **d)
        return veste(p, arma=peca(v.get('arma'), 'arma'), arma2=peca(v.get('arma2'), 'arma'), armadura=peca(v.get('armadura'), 'armadura'), elmo=peca(v.get('elmo'), 'armadura'), escudo=peca(v.get('escudo'), 'escudo'))
    tempo = list(C.get('tempo') or [])
    if E['relogio']['bloco'] in M.ESCUROS and not C.get('luz') and 'escuro' not in tempo: tempo.append('escuro')
    S = luta.nova([pessoa(x) for x in C['A']], [pessoa(x) for x in C['B']], inicio=C.get('inicio', 'perto'), lugar=C.get('lugar'), tempo=tempo, surpresa=C.get('surpresa'))
    S['mundo'] = True; S['comecou'] = True; luta.salva(S, arq_luta)
    E['turno']['lutas'].append(dict(arq=os.path.abspath(arq_luta), fim=None)); estado.grava(E)
    return luta.situacao(S)


def luta_roda(E, arq_luta, ordens):
    import luta
    S = json.load(open(arq_luta, encoding='utf-8'))
    if S['fim']: sys.exit('esta luta já acabou.')
    for o in ordens: luta.ordem(S, o)
    S['log'] = []; fim = luta.corre(S, interativo=True); luta.salva(S, arq_luta)
    out = '\n'.join(S['log']) + '\n\n' + luta.situacao(S)
    if fim == 'fim': out += '\n\nFIM: ' + json.dumps(luta.resultado(S), ensure_ascii=False) + '\n' + luta_fecha(E, S, arq_luta)
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
    if ef: estado.aplica(E, 'luta', ef, quem=quem, texto=f"luta: vence {S['fim']} em {S['r']} rodadas")
    for l in E['turno']['lutas']:
        if arq_luta and l['arq'] == os.path.abspath(arq_luta): l['fim'] = S['fim']
    return 'A LUTA VOLTOU AO ESTADO:\n' + '\n'.join(linhas)


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: print(__doc__); sys.exit()
    E = estado.carrega(); op = dict(x.split('=', 1) for x in a if '=' in x and ':' not in x); pos = [x for x in a if '=' not in x or ':' in x]
    pid = op.get('quem') or estado.eu(E)
    if pid not in E['gente']: sys.exit(f'não há a pessoa "{pid}"')
    n = lambda i: int(pos[i]) if len(pos) > i and pos[i].isdigit() and int(pos[i]) >= 1 else sys.exit('diga quantos blocos (1 ou mais). Um bloco são 4 horas.')
    if pos[0] == 'comer': print(comer(E, pid))
    elif pos[0] == 'dormir': print(dormir(E, pid, n(1), chao='chao' in pos))
    elif pos[0] == 'trabalhar': print(trabalhar(E, pid, n(1)))
    elif pos[0] == 'treinar' and len(pos) > 2: print(treinar(E, pid, n(1), pos[2]))
    elif pos[0] == 'descansar': print(descansar(E, pid, n(1)))
    elif pos[0] == 'esperar': print(esperar(E, pid, n(1)))
    elif pos[:2] == ['luta', 'nova'] and len(pos) == 4: print(luta_nova(E, pos[2], pos[3])); sys.exit()
    elif pos[:2] == ['luta', 'roda'] and len(pos) >= 3: print(luta_roda(E, pos[2], pos[3:]))
    else: print(__doc__); sys.exit()
    estado.grava(E); p = E['gente'][pid]
    print(f"{estado.quando(E)} · PV {p['pv']}/{estado.pv_max(p)} · {corpo.diz(p)} · {p['moedas']} de prata")
