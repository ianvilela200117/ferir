#!/usr/bin/env python3
"""turno.py — MOTOR 10: O TURNO EM DOIS COMANDOS. `abre` gera a página do Mestre a partir do estado; `fecha` recusa fechar se algo ficou solto.

  python3 turno.py abre                         só lê. Gera e mostra a MESA.md: o relógio, o corpo, o lugar, o que dá para fazer, as perguntas abertas, e o SÓ O MESTRE.
  python3 turno.py responde "1a.2b"             confere os códigos do jogador contra as perguntas abertas e diz o que cada um quer dizer
                                                (cada pergunta guarda o número com que foi aberta até o turno fechar; a já respondida recusa segunda resposta;
                                                 vale como o jogador escreve: "1c.2 a", "1c, 2a", "1c 2a")
  python3 turno.py pergunta "texto" "a=..." "b=..." ["c=..."]     abre uma pergunta para o fim do turno, e diz o número que ela terá na lista do RETOMAR (o do código)
  python3 turno.py nota "o que só o Mestre sabe"                  uma nota oculta (vai para o RETOMAR, na parte do Mestre)
  python3 turno.py fecha "o que houve" [parado] [git]             fecha o turno. `parado`: o turno foi só conversa, o relógio não andou. `git`: guarda no git e envia.

`fecha` RECUSA se: há luta aberta · há menos de 2 perguntas abertas
· o relógio não andou (e não foi dito `parado`) · o estado quebrou um invariante (moeda negativa, peça com dono que não existe, peça de quem morreu, saída torta...)
· um módulo do mundo recusa (recusa_fecha: a maldição do personagem no passo 4 sem pergunta aberta sobre ela, etapa da magia).
O RETOMAR NUNCA CORTA CALADO: o que se repete todo dia (comer, dormir, a cama, esperar) vira uma linha por dia; se os fatos ainda passam do teto, a primeira linha
diz quantos ficaram de fora e como lê-los (`estado.py eventos N`).
Se o personagem MORREU, a MESA e o RETOMAR abrem com isso, sem a lista de atos; o turno fecha (o herdeiro é da etapa 6: até lá, as perguntas do turno são do Mestre).
No meio do turno usa-se: ato.py (o que a pessoa faz), teste.py (o dado), ato.py luta (a luta), mercado.py, oficio.py, caca.py.
"""
import json, os, subprocess, sys
import tabelas_mundo as M
import estado, corpo, pessoas, teste


def _eventos_desde(n): return estado.eventos(desde=n)          # o registro gravado depois do evento n (a estação aberta e, se o turno passou de uma estação, as que acabaram)


def _mil(n): return f'{int(n):,}'.replace(',', '.')          # 18.279


def _carga_diz(p):
    return ', '.join(f'{q:g} de {estado.nome_bem(b)}' for b, q in (p.get('carga') or {}).items() if q)       # a matéria e as poções com a categoria por extenso


def _voce(E):
    import ato
    pid = estado.eu(E); p = E['gente'][pid]; f = estado.fora(E, pid)
    if p['estado'] != 'vivo':
        return [f"**{p['nome']} MORREU** ({estado.morte_diz(E, p).replace('morreu no', 'no').replace('já morreu', 'antes deste turno')}). Quem morreu não age: nenhum ato em nome de {p['nome']} vale.",
                _do_morto(E, pid) + ' O herdeiro e o recomeço são decisão do jogador (etapa 6 do projeto).']
    L = [f"**{p['nome']}**, nível {p['nivel']} · PV {p['pv']}/{estado.pv_max(p)} · {p['moedas']} de prata · " + (f"FORA, {estado.em(E, f)} (mora {estado.em(E, p['lugar'])})" if f else estado.em(E, p['lugar'])), f"Corpo: {corpo.diz(p)}"]
    for fe in p['feridas']: L.append(f"Ferida{' GRAVE' if fe['grave'] else ''}: {fe['parte']} (Dia {fe['dia']}; {estado.num(fe['repouso'])} de {M.FERIDA_DIAS[1 if fe['grave'] else 0]} dias de repouso)")
    L.append('```'); L.append(pessoas.linha(pessoas.ficha(estado.lutador(E, pid, visivel=True)))); L.append('```')       # a ficha que vai à mesa: só o dom que a pessoa já viu
    pecas = ato.diz_pecas(E, pid)
    L.append('Peças (`ato.py vestir ITEM` · `ato.py tirar ITEM`): ' + ' · '.join(pecas[:10]) + (f' · e mais {len(pecas) - 10}' if len(pecas) > 10 else ''))
    if _carga_diz(p): L.append('Carga: ' + _carga_diz(p) + (' (`ato.py comer carga` come da sua comida)' if (p.get('carga') or {}).get('comida', 0) >= 1 else ''))
    conta = lambda a, b: estado.tantos(b, 'dia de negócio', 'dias de negócio') if a == 'comércio' else estado.tantos(b, 'bloco')        # o comércio conta dias de negócio; o resto, blocos
    tr = [f"{a}: {conta(a, b)}" + (f" ({pessoas.T.MAESTRIAS[p.get('maestria', {}).get(a, 0)]})") for a, b in p.get('treino', {}).items()]
    if tr: L.append('Treino: ' + ' · '.join(tr))
    return L


def _do_morto(E, pid):
    """o que ficou de quem morreu, com as palavras certas: as peças, soltas junto do corpo; a carga e a prata, com o povo do lugar (num lugar com povo: entram no estoque e
    no caixa dele) ou no chão, junto do corpo (no ermo). O que era de um morto não muda de mão sozinho."""
    p = E['gente'][pid]; m = p.get('morte') or {}; lid = m.get('onde') if m.get('onde') in E['lugares'] else None
    if not lid: return f"O que {p['nome']} tinha caiu onde a morte veio."
    l = E['lugares'][lid]; pecas = [f"{it['nome']} ({i})" for i, it in E['itens']['itens'].items() if it.get('corpo') == pid and it.get('solto') and it.get('onde') == lid]
    carga = ', '.join(f'{q:g} de {estado.nome_bem(b)}' for b, q in (m.get('carga') or {}).items())
    if 'prata' in m: partes = ([f'a carga ({carga})'] if carga else []) + ([f"a prata ({_mil(m['prata'])})"] if m.get('prata') else [])
    else: partes = ['a carga', 'a prata']                    # o save de antes desta regra não guardou quanto ele deixou
    L = [f"Com o corpo, {estado.em(E, lid)}, ficaram soltas: " + (', '.join(pecas) if pecas else 'nenhuma peça') + '.']
    um = len(partes) == 1; o_que = ' e '.join(partes)
    if not partes: L.append(f"{p['nome']} não tinha carga nem prata.")
    elif l.get('pop'): L.append(f"{o_que[0].upper() + o_que[1:]} {'ficou' if um else 'ficaram'} com o povo do lugar: {'entrou' if um else 'entraram'} no estoque e no caixa {estado.de(E, lid)}.")
    else: L.append(f"{o_que[0].upper() + o_que[1:]} {'ficou' if um else 'ficaram'} no chão, junto do corpo.")
    L.append('O que era de um morto não muda de mão sozinho: quem fica com o quê é decisão de cena, e o Mestre registra por evento (`itens.py dono ITEM PESSOA`, `estado.py mestre`).')
    return ' '.join(L)


def _aqui(E):
    import ato
    pid = estado.eu(E); p = E['gente'][pid]; l = E['lugares'][p['lugar']]; of = p.get('grau_oficio', 'diarista'); f = estado.fora(E, pid)
    if f and estado.quem_viaja(E, pid):
        v = estado.viagem(E, pid)
        return [f"**{p['nome']} está na estrada, de {E['lugares'][v['origem']]['nome']} para {E['lugares'][v['destino']]['nome']}** ({estado.tantos(v.get('feito', 0), 'bloco')} de {v.get('blocos')}). Enquanto a viagem estiver aberta, os atos da vila não valem (comer da carga vale: `ato.py comer carga`). O que há à frente está em \"A viagem\"."]
    if f and estado.quem_desce(E, pid): return [f"**{p['nome']} está {estado.em(E, f)}, na descida.** Enquanto a descida estiver aberta, os atos da vila não valem (comer da carga vale: `ato.py comer carga`). O que há à frente está em \"A masmorra\"."]
    if f: return [f"**{p['nome']} está fora, {estado.em(E, f)}.** Enquanto a saída estiver aberta, os atos da vila não valem (comer da carga vale: `ato.py comer carga`). O que há à frente está em \"A caça e a coleta\"."]
    L = [f"**{l['nome']}** · comida no lugar: {_mil(l['estoque'].get('comida', 0))} · {'há cama' if l.get('cama') else 'não há cama: dorme-se no chão'}"]
    outros = [q['nome'] + (f" ({q['sobre']})" if q.get('sobre') else '') for k, q in E['gente'].items() if k != pid and q['lugar'] == p['lugar'] and q['estado'] == 'vivo' and not estado.fora(E, k)]
    if outros: L.append('Quem está aqui: ' + ', '.join(outros[:QUEM_AQUI]) + (f' e mais {len(outros) - QUEM_AQUI}' if len(outros) > QUEM_AQUI else ''))
    L += _perto(E, pid)
    feito = ato.jornada(E, pid); cama = ato.cama_diz(E, pid)
    L += ['', '**O que dá para fazer, e o que custa** (1 bloco = 4 horas):',
          f"- comer: {M.REFEICAO_PRECO} de prata, fome −{-M.REFEICAO} (`ato.py comer`; da sua carga, sem pagar: `ato.py comer carga`)",
          f"- dormir: {f'cama por {M.CAMA_PRECO} de prata, ' + ('e a sua está ' + cama + '; ' if cama else f'que vale {M.CAMA_VALE} blocos (um dia) a contar de quando se paga; ') if l.get('cama') else ''}"
          f"cada bloco tira {-M.SONO_CAMA} de sono e de cansaço (no chão, {-M.SONO_CHAO}) e devolve PV (`ato.py dormir N`)",
          f"- trabalhar ({of}): {M.SALARIO[of]} de prata por bloco, esforço {M.ESFORCO_OFICIO[of]}; a jornada são {M.JORNADA} blocos pagos por dia (hoje: {feito} de {M.JORNADA}) (`ato.py trabalhar N`)",
          f"- treinar com uma arma: esforço pesado; a maestria sobe aos {', '.join(_mil(v) for v in M.MAESTRIA_BLOCOS.values())} blocos (`ato.py treinar N ARMA`)",
          "- descansar, esperar (`ato.py descansar N`, `ato.py esperar N`) · lutar (`ato.py luta nova CENARIO ARQ`) · testar (`teste.py`)"]
    return L


QUEM_AQUI = 16          # quantos nomes o "Quem está aqui" diz (a vila de teste com a etapa 4b tem 16 pessoas além do personagem: o Quim tem de aparecer)


def _perto(E, pid):
    """a masmorra vizinha do lugar, com o que o povo diz dela (etapa 4b: masmorra.perto). Sem masmorra vizinha (ou sem o módulo), nada: a MESA de hoje sai igual"""
    try: import masmorra
    except ModuleNotFoundError as x:
        if x.name != 'masmorra': raise
        return []
    return list(getattr(masmorra, 'perto', lambda E, pid: [])(E, pid))


def _modulos(E, gancho):
    """as linhas que cada módulo do mundo põe na página (voce, mesa, so_mestre), no resumo do turno (retomar) ou na recusa de fechar (recusa_fecha).
    A MESA (etapa 3): as seções dos módulos da etapa 3 vêm primeiro (tabelas_mundo.MESA_ORDEM); com a viagem aberta, só os da estrada põem seção (MESA_NA_ESTRADA);
    e o SÓ O MESTRE dos módulos que falam de pessoas (MESA_SO_CENA) só vê quem está em cena (estado.na_cena): o resto sai no `talento.py mestre`."""
    ms = estado.modulos(gancho)
    if gancho == 'mesa':
        ordem = {n: i for i, n in enumerate(M.MESA_ORDEM)}; ms = sorted(ms, key=lambda m: ordem.get(m.__name__, len(ordem)))
        pid = estado.eu(E)
        if pid and E['gente'][pid]['estado'] == 'vivo' and estado.quem_viaja(E, pid): ms = [m for m in ms if m.__name__ in M.MESA_NA_ESTRADA]
    cena = None
    if gancho == 'so_mestre' and any(m.__name__ in M.MESA_SO_CENA for m in ms):
        ids = set(estado.na_cena(E)); cena = dict(E, gente={k: p for k, p in E['gente'].items() if k in ids})        # a vista do estado com a gente que está em cena (só lê)
    L = [list(getattr(mod, gancho)(cena if cena is not None and mod.__name__ in M.MESA_SO_CENA else E) or []) for mod in ms]
    return [x for x in L if x]


def orcamento(txt):
    """O ORÇAMENTO DA MESA (etapa 3): o tamanho de cada parte (em KB de 1.000 letras do arquivo), pelas seções (o título "## ..."), e o teto dela (tabelas_mundo.MESA_TETO).
    Devolve [(a parte, os KB, o teto ou None)], na ordem em que aparecem, e o total no fim ("total")."""
    partes = {}; atual = 'voce'
    for linha in txt.splitlines(keepends=True):
        if linha.startswith('## '):
            t = linha[3:]; atual = next((k for pre, k in M.MESA_SECOES if t.startswith(pre)), 'outros')
        partes[atual] = partes.get(atual, 0) + len(linha.encode('utf-8'))
    out = [(k, v / 1000, M.MESA_TETO.get(k)) for k, v in partes.items()]
    return out + [('total', len(txt.encode('utf-8')) / 1000, M.MESA_TOTAL)]


def avisos(txt):
    """o aviso das partes da MESA que passam do teto delas (e do total): [linhas]; vazio, a MESA cabe"""
    return [f"a parte \"{k}\" da MESA tem {estado.num(round(kb, 1))} KB (o teto é {estado.num(t)})" for k, kb, t in orcamento(txt) if t is not None and kb > t + 1e-9]


def mesa(E):
    t = E['turno']; pid = estado.eu(E); vivo = E['gente'][pid]['estado'] == 'vivo'
    L = [f"# MESA · turno {t['n']} · {estado.quando(E)}"]
    if estado.luta_aberta(E): L += ['', f"**LUTA ABERTA.** {estado.luta_diz(E)[0].upper() + estado.luta_diz(E)[1:]}"]
    L += ['', '## Você'] + _voce(E)
    if vivo:
        for linhas in _modulos(E, 'voce'): L += linhas            # o que cada módulo põe no "Você" (o talento que apareceu, a Mana, os feitiços, a maldição até onde se sabe)
        L += ['', '## Aqui'] + _aqui(E)
        for linhas in _modulos(E, 'mesa'): L += [''] + linhas      # cada módulo do mundo põe na mesa a sua parte (o mercado, a oficina, a caça)
    L += ['', '## Perguntas abertas']
    L += lista_perguntas(t) + [f"- (da caixa, vence em um dia: entra sozinha nas perguntas ao fechar) {c['id']}: {c['pede']}" for c in caixa_pendentes(E)] or ['(nenhuma: o turno precisa abrir pelo menos duas antes de fechar)']
    if t['respondidas']: L += ['', '**Respondido neste turno (cumprir antes de fechar):** ' + ' · '.join(f"{r['texto']} → {r['cod']}) {r['opcao']}" for r in t['respondidas'])]
    L += ['', '## SÓ O MESTRE']
    L += [f"- {teste.diz(E, r, mestre=True)}" for r in t['dados'] if r['oculto']] + [f"- nota: {n}" for n in t['notas']]
    L += [f"- LUTA ABERTA: {l['arq']} (`ato.py luta roda {l['arq']} \"Nome: ordem\"`)" for l in t['lutas'] if not l['fim']]
    for linhas in _modulos(E, 'so_mestre'): L += [x if x.startswith('- ') else '- ' + x for x in linhas]       # o que cada módulo do mundo só mostra ao Mestre (a contagem do ermo, o que os mortos deixaram lá...): a função so_mestre(E) do módulo; vale também com o personagem morto
    aqui = estado.onde(E, pid) if vivo else ((E['gente'][pid].get('morte') or {}).get('onde') if (E['gente'][pid].get('morte') or {}).get('onde') in E['lugares'] else estado.onde(E, pid)); soltos = [f"{i} {it['nome']}" for i, it in E['itens']['itens'].items() if it.get('onde') == aqui and it.get('solto')]
    if soltos: L.append(f"- no chão {estado.em(E, aqui)} (soltas; quem fica com elas entra por evento): " + ' · '.join(soltos[:8]) + (f' · e mais {len(soltos) - 8}' if len(soltos) > 8 else ''))
    P = estado.valida(E); L += [f"- ESTADO QUEBRADO: {x}" for x in P] or ['- o estado está inteiro.']
    return '\n'.join(L) + '\n'


def abre(E):
    txt = mesa(E); open(os.path.join(estado.pasta(), 'MESA.md'), 'w', encoding='utf-8').write(txt); return txt


# ---------- a caixa vira pergunta sozinha (etapa 3) ----------
def caixa_pendentes(E):
    """os pedidos da caixa do personagem que vencem em até um dia (tabelas_mundo.CAIXA_PERGUNTA blocos) e ainda não estão nas perguntas abertas: [registro]"""
    pid = estado.eu(E); C = (E.get('caixa') or {}).get('abertos') or {}; ja = {q.get('caixa') for q in E['turno'].get('perguntas', [])}
    return sorted((c for c in C.values() if isinstance(c, dict) and c.get('para') == pid and _int(c.get('prazo')) and c['prazo'] - estado.agora(E) <= M.CAIXA_PERGUNTA and c.get('id') not in ja),
                  key=lambda c: (c['prazo'], c['id']))


def _int(v): return isinstance(v, int) and not isinstance(v, bool)


def caixa_perguntas(E):
    """O PEDIDO QUE VENCE EM UM DIA VIRA PERGUNTA SOZINHO: abre, para cada um, a pergunta do turno com as opções dele, ligada a `caixa.py responde ID LETRA`. Devolve quantas abriu."""
    k = 0
    for c in caixa_pendentes(E):
        de = E['gente'].get(c.get('de'), {}).get('nome', c.get('de')); calado = c['opcoes'].get(c['padrao'], c['padrao'])
        pergunta(E, f"{de} pede: {c['pede']} (a caixa, {c['id']}: vence em um dia; calado, vale \"{calado}\"; cumpra com `caixa.py responde {c['id']} LETRA`)", [f'{l}={v}' for l, v in c['opcoes'].items()])
        E['turno']['perguntas'][-1]['caixa'] = c['id']; k += 1
    return k


def numera(t):
    """cada pergunta aberta GUARDA O NÚMERO com que foi aberta (o que o jogador leu no RETOMAR.md) até o turno fechar: responder uma não muda o número das outras.
    Pergunta de save antigo, sem número, ganha um aqui: o primeiro livre, na ordem em que estão. Devolve as perguntas abertas."""
    usados = {q['n'] for q in t['perguntas'] if isinstance(q.get('n'), int)} | {r['n'] for r in t.get('respondidas', []) if isinstance(r.get('n'), int)}
    for q in t['perguntas']:
        if not isinstance(q.get('n'), int):
            q['n'] = next(k for k in range(1, len(usados) + 2) if k not in usados); usados.add(q['n'])
    return t['perguntas']


def lista_perguntas(t): return [f"{q['n']}. {q['texto']}  " + ' · '.join(f"**{k})** {v}" for k, v in q['opcoes'].items()) for q in numera(t)]        # as perguntas abertas, cada uma com o número dela


def pergunta(E, texto, opcoes):
    ops = dict(o.split('=', 1) for o in opcoes if '=' in o); t = E['turno']
    if len(ops) < 2 or any(len(k) != 1 or not k.isalpha() for k in ops): sys.exit('a pergunta pede pelo menos duas opções, cada uma com uma letra: "a=..." "b=..."')
    n = max([q['n'] for q in numera(t)] + [r['n'] for r in t.get('respondidas', []) if isinstance(r.get('n'), int)] + [0]) + 1      # o número seguinte ao maior já usado neste turno (aberto ou respondido)
    t['perguntas'].append(dict(n=n, texto=texto, opcoes=ops)); lista = len(t['perguntas'])
    # o número que vale para o jogador é o da LISTA do RETOMAR (no fechar, as que ficam são numeradas de novo, de 1 em diante): é com ele que o código da resposta vem ("1a")
    if lista == n: return f"pergunta {n} aberta."
    return f"pergunta {lista} aberta: é o número dela na lista do RETOMAR, e é com ele que o jogador responde ({lista}{next(iter(ops))}, {lista}{list(ops)[1]}...). Até este turno fechar, o caderno a guarda como {n}."


def responde(E, codigos):
    """'1a.2b': cada código tem de bater numa pergunta aberta (pelo NÚMERO com que ela foi aberta) e numa opção dela. A pergunta já respondida neste turno recusa segunda resposta.
    Nada é executado: o Mestre cumpre com os comandos."""
    t = E['turno']; pares = []; abertas = {q['n']: q for q in numera(t)}; feitas = {r['n']: r for r in t.get('respondidas', []) if isinstance(r.get('n'), int)}
    import re
    cods = re.findall(r'(\d+)\s*([^\W\d_]*)', codigos); resto = re.sub(r'\d+\s*[^\W\d_]*', '', codigos)       # "1c.2 a", "1c, 2a", "1c 2a": o jogador escreve assim (espaço entre o número e a letra; vírgula, ponto ou espaço entre os códigos)
    if not cods or re.sub(r'[\s.,;]', '', resto): sys.exit(f'não entendi "{codigos}": cada código é o número da pergunta e a letra da opção ("1a.2b", "1a, 2b" ou "1 a 2 b"). Nada foi marcado.')
    for num, letra in cods:
        c = num + letra; letra = letra.lower()
        if num and int(num) in feitas and int(num) not in abertas:
            sys.exit(f'a pergunta {int(num)} já foi respondida neste turno ("{feitas[int(num)]["texto"]}" → {feitas[int(num)]["cod"]}) {feitas[int(num)]["opcao"]}): não aceita segunda resposta. Nada foi marcado.')
        if not num or int(num) not in abertas:
            sys.exit(f'o código "{c}" não bate em nenhuma pergunta aberta (' + (f"as abertas: {', '.join(str(k) for k in sorted(abertas))}" if abertas else 'não há nenhuma') + '). Nada foi marcado.')
        q = abertas[int(num)]
        if not letra: sys.exit(f'falta a letra da opção no código "{c}" (a pergunta {int(num)} tem: {", ".join(q["opcoes"])}). Nada foi marcado.')
        if letra not in q['opcoes']: sys.exit(f'a pergunta {int(num)} não tem a opção "{letra}" (tem: {", ".join(q["opcoes"])}). Nada foi marcado.')
        pares.append((int(num), letra))
    if len({n for n, _ in pares}) != len(pares): sys.exit('a mesma pergunta foi respondida duas vezes. Nada foi marcado.')
    out = []
    for n, letra in pares:
        q = abertas[n]; t['respondidas'].append(dict(n=n, texto=q['texto'], cod=letra, opcao=q['opcoes'][letra], **({'caixa': q['caixa']} if q.get('caixa') else {})))
        out.append(f"{n}{letra}: {q['texto']} → {q['opcoes'][letra]}" + (f" (cumpra: `caixa.py responde {q['caixa']} {letra}`)" if q.get('caixa') else ''))
    t['perguntas'] = [q for q in t['perguntas'] if q['n'] not in {n for n, _ in pares}]
    return '\n'.join(out) + (f"\nFicam abertas: {', '.join(str(q['n']) for q in t['perguntas'])}." if t['perguntas'] else '')


SEGREDO = {('pessoa', 'talento'), ('pessoa', 'dom'), ('item', 'maldita'), ('lugar', 'maldito'), ('lugar', 'covil'),      # o que o Mestre (ou o gerador) põe e a gente do mundo não sabe
           ('lugar', 'dragao'), ('lugar', 'armadilhas'), ('lugar', 'segredos'), ('lugar', 'guardado'), ('lugar', 'portas'), ('lugar', 'vagantes'), ('lugar', 'chefe'),      # etapa 4b: o dragão e o mapa da masmorra
           ('lugar', 'bando'), ('pessoa', 'querer')}      # etapa 3: o bando que o gerador põe num ermo; o querer escondido de alguém


def secreto(e):
    """o evento do Mestre ou do gerador que só o Mestre sabe (o talento e o dom de alguém, a peça ou o lugar maldito, o covil, a maldição que a pessoa ainda não sente):
    não vai aos fatos do turno, vai ao SÓ O MESTRE do RETOMAR"""
    if e.get('tipo') not in ('gera', 'mestre'): return False
    for x in e.get('efeitos') or []:
        if not isinstance(x, list) or len(x) < 4: continue
        if x[0] == 'lugar' and x[1] == 'nasce' and isinstance(x[3], dict) and x[3].get('tipo') in ('masmorra', 'sala'): return True      # a masmorra que nasce (etapa 4b): o mapa que ninguém viu
        if x[0] == 'maldicao' and x[2] == 'poe' and isinstance(x[3], dict) and (x[3].get('sabe') or 0) < 2: return True
        if x[0] in ('pessoa', 'item', 'lugar') and (x[0], str(x[2]).split('.')[0]) in SEGREDO: return True
    return False


def fatos(evs, teto=None, nasce=False):
    """as linhas dos fatos do turno, tiradas do registro de eventos, para o RETOMAR.md. NUNCA CORTA CALADO.
    O mundo andando sozinho (o dia que vira, o lugar que produz e consome, o ermo que se refaz) não é fato do turno, a não ser que alguém morra.
    Com `nasce` (o primeiro turno de um mundo), os eventos do gerador que abrem o registro (o mundo nascendo) também ficam de fora: não são coisa que alguém fez.
    O que se repete todo dia (comer, dormir, a cama, descansar, esperar) vira UMA linha por dia. O mesmo fato repetido SEGUIDO no mesmo dia vira uma linha, com a conta
    e as horas do primeiro ao último ("manhã a noite: ... (× 4)"). O que aconteceu depois de outro fato fica na linha e na hora dele: nada vai parar na hora do primeiro.
    O evento que foi gravado SEM TEXTO (e não é o mundo andando sozinho) entra assim mesmo, com o número e o tipo dele: nada do que alguém fez some calado.
    Se ainda assim passa do teto (tabelas_mundo.RETOMAR_FATOS), ficam as mais novas, e a primeira linha diz quantas ficaram de fora e como lê-las."""
    teto = teto or M.RETOMAR_FATOS; linhas = []; onde = {}; ultimo = None
    for e in evs:
        if nasce and e['tipo'] == 'gera': continue
        nasce = False
        morte = any(isinstance(x, list) and len(x) == 5 and x[0] == 'pessoa' and x[2:] == ['estado', 'poe', 'morto'] for x in e.get('efeitos', []))
        if e['tipo'] in M.MUNDO_SOZINHO and not morte: continue
        if secreto(e): continue                                                                 # o segredo do Mestre não é fato que o jogador lê (vai ao SÓ O MESTRE)
        if not e.get('texto'): e = dict(e, texto=f"(evento #{e.get('id', '?')}, {e['tipo']}, sem texto: `python3 estado.py eventos` mostra o que ele mudou)")      # o evento gravado sem texto não some calado: entra com o número dele
        if e['tipo'] in M.ROTINA and not morte:
            chave = ('rotina', e['dia'])
            if chave not in onde: onde[chave] = dict(dia=e['dia'], rotina={}); linhas.append(onde[chave])
            onde[chave]['rotina'][e['texto']] = onde[chave]['rotina'].get(e['texto'], 0) + 1
        else:
            if not (ultimo and ultimo['dia'] == e['dia'] and ultimo['texto'] == e['texto']):      # só se junta ao fato IGUAL que veio logo antes (a rotina e o mundo andando sozinho não contam como "entre os dois")
                ultimo = dict(dia=e['dia'], bloco=e['bloco'], texto=e['texto'], vezes=0); linhas.append(ultimo)
            ultimo['vezes'] += 1; ultimo['ate'] = e['bloco']
    vezes = lambda k: f' (× {k})' if k > 1 else ''
    def diz(x):
        if 'rotina' in x: return f"- Dia {x['dia']}, a rotina: " + ' · '.join(txt + vezes(k) for txt, k in x['rotina'].items())
        hora = M.BLOCOS[x['bloco']] + (f" a {M.BLOCOS[x['ate']]}" if x['ate'] != x['bloco'] else '')        # "manhã a noite": do primeiro ao último dos fatos juntados
        return f"- Dia {x['dia']}, {hora}: {x['texto']}{vezes(x['vezes'])}"
    if not linhas: return ['- (nenhum fato registrado neste turno)']
    if len(linhas) <= teto: return [diz(x) for x in linhas]
    fora = linhas[:len(linhas) - (teto - 1)]; ficam = linhas[len(fora):]; d0, d1 = fora[0]['dia'], fora[-1]['dia']
    aviso = (f"- (ficaram de fora {estado.tantos(len(fora), 'fato mais antigo', 'fatos mais antigos')}, " + (f'do Dia {d0}' if d0 == d1 else f'do Dia {d0} ao Dia {d1}')
             + f": o registro inteiro do turno sai com `python3 estado.py eventos {len(evs)}`)")
    return [aviso] + [diz(x) for x in ficam]


def fecha(E, resumo, parado=False, git=False):
    t = E['turno']; R = []; caixa_perguntas(E)              # o pedido da caixa que vence em um dia entra sozinho nas perguntas (etapa 3)
    if estado.luta_aberta(E): R.append(estado.luta_diz(E))
    if len(t['perguntas']) < 2: R.append(('não há pergunta aberta' if not t['perguntas'] else 'há uma pergunta aberta só') + ': o turno fecha com pelo menos duas (`turno.py pergunta`)')
    if estado.agora(E) == (t['aberto']['dia'] - 1) * M.BLOCOS_DIA + t['aberto']['bloco'] and not parado: R.append('o relógio não andou neste turno. Todo ato custa tempo; se foi só conversa, feche com `parado`')
    R += [f'o estado quebrou: {x}' for x in estado.valida(E)]
    R += [x for linhas in _modulos(E, 'recusa_fecha') for x in linhas]       # o que os módulos do mundo recusam (a maldição no passo 4 sem pergunta aberta)
    C = (E.get('caixa') or {}).get('abertos') or {}
    R += [f"o jogador respondeu o pedido {r['caixa']} da caixa ({r['cod']}: {r['opcao']}) e ele segue aberto: cumpra com `caixa.py responde {r['caixa']} {r['cod']}`" for r in t['respondidas'] if r.get('caixa') in C]
    R += [f"o pedido {c['id']} da caixa vence em um dia e não está nas perguntas abertas" for c in caixa_pendentes(E)]
    if not resumo.strip(): R.append('falta dizer o que houve no turno')
    if R: sys.exit('O TURNO NÃO FECHA:\n  - ' + '\n  - '.join(R))
    for i, q in enumerate(t['perguntas']): q['n'] = i + 1         # o turno fecha: as perguntas que ficam abertas são numeradas de novo, de 1 em diante. É com esse número que o jogador as lê no RETOMAR.md e responde
    pid = estado.eu(E); p = E['gente'][pid]; evs = _eventos_desde(t.get('evento0', 0)) + E['_novos']; f = estado.fora(E, pid)
    if p['estado'] != 'vivo': agora = f"**{p['nome']} MORREU** ({estado.morte_diz(E, p).replace('morreu no', 'no').replace('já morreu', 'antes deste turno')})"
    else: agora = f"{p['nome']} " + (f"FORA, {estado.em(E, f)} (a {'viagem' if estado.quem_viaja(E, pid) else 'descida' if estado.quem_desce(E, pid) else 'saída'} está aberta)" if f else estado.em(E, p['lugar'])) + f" · PV {p['pv']}/{estado.pv_max(p)} · {corpo.diz(p)} · {p['moedas']} de prata"
    L = [f"# RETOMAR · depois do turno {t['n']}", '', f"**Agora:** {estado.quando(E)} · {agora}", '', f"**O que houve no turno {t['n']}:** {resumo}"]
    for linhas in _modulos(E, 'retomar'): L += [''] + linhas
    if t['respondidas']: L += ['', '**Respondido:** ' + ' · '.join(f"{r['texto']} → {r['opcao']}" for r in t['respondidas'])]
    L += ['', '**Os fatos do turno** (do registro de eventos):'] + fatos(evs, nasce=not t.get('evento0'))
    L += ['', '## PERGUNTAS ABERTAS'] + lista_perguntas(t)
    ocultas = [f"- {teste.diz(E, r, mestre=True)}" for r in t['dados'] if r['oculto']] + [f"- {n}" for n in t['notas']]
    ocultas += [f"- Dia {e['dia']}, {M.BLOCOS[e['bloco']]}: {e.get('texto') or e['tipo']} (evento #{e.get('id', '?')}, do {'gerador' if e['tipo'] == 'gera' else 'Mestre'}: fora dos fatos)" for e in evs if secreto(e) and not (not t.get('evento0') and e['tipo'] == 'gera')]
    L += ['', '## SÓ O MESTRE'] + (ocultas or ['- nada oculto neste turno.'])
    txt = '\n'.join(L) + '\n'
    E['turno'] = dict(n=t['n'] + 1, aberto=dict(dia=E['relogio']['dia'], bloco=E['relogio']['bloco']), evento0=E['relogio']['eventos'], dados=[], lutas=[], perguntas=t['perguntas'], respondidas=[], notas=[])
    estado.grava(E); open(os.path.join(estado.pasta(), 'RETOMAR.md'), 'w', encoding='utf-8').write(txt); abre(E)
    out = f"Turno {t['n']} fechado. RETOMAR.md e MESA.md gerados."
    if git:
        raiz = estado.pasta(); cmds = [['git', 'add', '-A', '.'], ['git', 'commit', '-q', '-m', f"Dia {E['relogio']['dia']}: {resumo[:120]}"], ['git', 'push']]
        for c in cmds:
            r = subprocess.run(c, cwd=raiz, capture_output=True, text=True)
            if r.returncode != 0: out += f"\nATENÇÃO: `{' '.join(c[:2])}` falhou: {(r.stderr or r.stdout).strip()[:300]}. O save NÃO foi enviado; diga ao jogador."; break
        else: out += '\nGuardado no git e enviado.'
    return out


if __name__ == '__main__':
    import signal; hasattr(signal, 'SIGPIPE') and signal.signal(signal.SIGPIPE, signal.SIG_DFL)      # a saída cortada (`| head`) acaba o comando calada, sem erro de programa: tudo já foi gravado antes de falar
    a = sys.argv[1:]
    if not a or a[0] not in ('abre', 'pergunta', 'responde', 'nota', 'fecha'): print(__doc__); sys.exit()
    E = estado.carrega()
    if a[0] == 'abre':
        txt = abre(E); print(txt)
        av = avisos(txt)
        if av: print('AVISO, o orçamento da MESA (tabelas_mundo.MESA_TETO): ' + ' · '.join(av))
        sys.exit()
    if a[0] == 'pergunta':
        if len(a) < 2 or not a[1].strip(): sys.exit('diga a pergunta e as opções: `turno.py pergunta "O que fazer de manhã?" "a=trabalhar" "b=treinar"`')
        print(pergunta(E, a[1], a[2:])); estado.grava(E)
    elif a[0] == 'responde':
        if len(a) < 2: sys.exit('diga os códigos do jogador: `turno.py responde "1a.2b"` (vale também "1a, 2b" e "1 a 2 b")')
        print(responde(E, ' '.join(a[1:]))); estado.grava(E)
    elif a[0] == 'nota':
        if len(a) != 2 or not a[1].strip(): sys.exit('diga a nota, entre aspas: `turno.py nota "o que só o Mestre sabe"`')
        E['turno']['notas'].append(a[1]); estado.grava(E); print('nota guardada (só o Mestre vê).')
    else: print(fecha(E, a[1] if len(a) > 1 else '', parado='parado' in a[2:], git='git' in a[2:]))
