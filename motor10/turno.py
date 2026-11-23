#!/usr/bin/env python3
"""turno.py — MOTOR 10: O TURNO EM DOIS COMANDOS. `abre` gera a página do Mestre a partir do estado; `fecha` recusa fechar se algo ficou solto.

  python3 turno.py abre                         só lê. Gera e mostra a MESA.md: o relógio, o corpo, o lugar, o que dá para fazer, as perguntas abertas, e o SÓ O MESTRE.
  python3 turno.py responde "1a.2b"             confere os códigos do jogador contra as perguntas abertas e diz o que cada um quer dizer
  python3 turno.py pergunta "texto" "a=..." "b=..." ["c=..."]     abre uma pergunta para o fim do turno
  python3 turno.py nota "o que só o Mestre sabe"                  uma nota oculta (vai para o RETOMAR, na parte do Mestre)
  python3 turno.py fecha "o que houve" [parado] [git]             fecha o turno. `parado`: o turno foi só conversa, o relógio não andou. `git`: guarda no git e envia.

`fecha` RECUSA se: há luta aberta · há menos de 2 perguntas abertas
· o relógio não andou (e não foi dito `parado`) · o estado quebrou um invariante (moeda negativa, peça com dono que não existe, morto com peça, saída torta...).
MORTO o personagem, a MESA e o RETOMAR abrem com isso, sem a lista de atos; o turno fecha (o herdeiro é da etapa 6: até lá, as perguntas do turno são do Mestre).
No meio do turno usa-se: ato.py (o que a pessoa faz), teste.py (o dado), ato.py luta (a luta), mercado.py, oficio.py, caca.py.
"""
import json, os, subprocess, sys
import tabelas_mundo as M
import estado, corpo, pessoas, teste


def _eventos_desde(n):
    arq = os.path.join(estado.pasta(), 'eventos.jsonl')
    if not os.path.exists(arq): return []
    return [e for e in map(json.loads, open(arq, encoding='utf-8').read().splitlines()) if e['id'] > n]


def _carga_diz(p):
    def nome(b):
        n, c = M.le_materia(b); return b if c is None else f"{n} {pessoas.T.CATS[c] if not n.endswith('a') else ['Comum', 'Incomum', 'Rara'][min(c, 2)]}"
    return ', '.join(f'{q:g} de {nome(b)}' for b, q in (p.get('carga') or {}).items() if q)


def _voce(E):
    import ato
    pid = estado.eu(E); p = E['gente'][pid]; f = estado.fora(E, pid)
    if p['estado'] != 'vivo':
        return [f"**{p['nome']} ESTÁ MORTO:** {estado.morte_diz(E, p)}. Morto não age: nenhum ato dele vale.",
                'O que era dele caiu onde morreu (as peças, soltas; a carga e a prata, no estoque do lugar). O herdeiro e o recomeço são decisão do jogador (etapa 6 do projeto).']
    L = [f"**{p['nome']}**, nível {p['nivel']} · PV {p['pv']}/{estado.pv_max(p)} · {p['moedas']} de prata · " + (f"FORA, {estado.em(E, f)} (mora {estado.em(E, p['lugar'])})" if f else estado.em(E, p['lugar'])), f"Corpo: {corpo.diz(p)}"]
    for fe in p['feridas']: L.append(f"Ferida{' GRAVE' if fe['grave'] else ''}: {fe['parte']} (Dia {fe['dia']}; {fe['repouso']} de {M.FERIDA_DIAS[1 if fe['grave'] else 0]} dias de repouso)")
    L.append('```'); L.append(pessoas.linha(pessoas.ficha(estado.lutador(E, pid)))); L.append('```')
    pecas = ato.diz_pecas(E, pid)
    L.append('Peças (`ato.py vestir ITEM` · `ato.py tirar ITEM`): ' + ' · '.join(pecas[:10]) + (f' · e mais {len(pecas) - 10}' if len(pecas) > 10 else ''))
    if _carga_diz(p): L.append('Carga: ' + _carga_diz(p) + (' (`ato.py comer carga` come da sua comida)' if (p.get('carga') or {}).get('comida', 0) >= 1 else ''))
    tr = [f"{a}: {b} blocos" + (f" ({pessoas.T.MAESTRIAS[p.get('maestria', {}).get(a, 0)]})") for a, b in p.get('treino', {}).items()]
    if tr: L.append('Treino: ' + ' · '.join(tr))
    return L


def _aqui(E):
    import ato
    pid = estado.eu(E); p = E['gente'][pid]; l = E['lugares'][p['lugar']]; of = p.get('grau_oficio', 'diarista'); f = estado.fora(E, pid)
    if f: return [f"**{p['nome']} está fora, {estado.em(E, f)}.** Enquanto a saída estiver aberta, os atos da vila não valem (comer da carga vale: `ato.py comer carga`). O que há à frente está em \"A caça e a coleta\"."]
    L = [f"**{l['nome']}** · comida no lugar: {l['estoque'].get('comida', 0):g} · {'há cama' if l.get('cama') else 'não há cama: dorme-se no chão'}"]
    outros = [q['nome'] + (f" ({q['sobre']})" if q.get('sobre') else '') for k, q in E['gente'].items() if k != pid and q['lugar'] == p['lugar'] and q['estado'] == 'vivo' and not estado.fora(E, k)]
    if outros: L.append('Quem está aqui: ' + ', '.join(outros[:12]) + (f' e mais {len(outros) - 12}' if len(outros) > 12 else ''))
    feito = ato.jornada(E, pid)
    L += ['', '**O que dá para fazer, e o que custa** (1 bloco = 4 horas):',
          f"- comer: {M.REFEICAO_PRECO} de prata, fome {M.REFEICAO} (`ato.py comer`; da sua carga, sem pagar: `ato.py comer carga`)",
          f"- dormir: {'cama por ' + str(M.CAMA_PRECO) + ' de prata; ' if l.get('cama') else ''}cada bloco tira {-M.SONO_CAMA} de sono e de cansaço (no chão, {-M.SONO_CHAO}) e devolve PV (`ato.py dormir N`)",
          f"- trabalhar ({of}): {M.SALARIO[of]} de prata por bloco, esforço {M.ESFORCO_OFICIO[of]}; a jornada são {M.JORNADA} blocos pagos por dia (hoje: {feito} de {M.JORNADA}) (`ato.py trabalhar N`)",
          f"- treinar com uma arma: esforço pesado; a maestria sobe aos {', '.join(str(v) for v in M.MAESTRIA_BLOCOS.values())} blocos (`ato.py treinar N ARMA`)",
          "- descansar, esperar (`ato.py descansar N`, `ato.py esperar N`) · lutar (`ato.py luta nova CENARIO ARQ`) · testar (`teste.py`)"]
    return L


def _modulos(E, gancho):
    """as linhas que cada módulo do mundo põe na página (mesa) ou no resumo do turno (retomar)"""
    import importlib
    L = []
    for nome in M.MODULOS:
        try: mod = importlib.import_module(nome)
        except ModuleNotFoundError as e:
            if e.name != nome: raise
            continue
        if hasattr(mod, gancho): L.append(list(getattr(mod, gancho)(E)))
    return [x for x in L if x]


def mesa(E):
    t = E['turno']; pid = estado.eu(E); vivo = E['gente'][pid]['estado'] == 'vivo'
    L = [f"# MESA · turno {t['n']} · {estado.quando(E)}", '', '## Você'] + _voce(E)
    if vivo:
        L += ['', '## Aqui'] + _aqui(E)
        for linhas in _modulos(E, 'mesa'): L += [''] + linhas      # cada módulo do mundo põe na mesa a sua parte (o mercado, a oficina, a caça)
    L += ['', '## Perguntas abertas']
    L += [f"{i + 1}. {q['texto']}  " + ' · '.join(f"**{k})** {v}" for k, v in q['opcoes'].items()) for i, q in enumerate(t['perguntas'])] or ['(nenhuma: o turno precisa abrir pelo menos duas antes de fechar)']
    if t['respondidas']: L += ['', '**Respondido neste turno (cumprir antes de fechar):** ' + ' · '.join(f"{r['texto']} → {r['cod']}) {r['opcao']}" for r in t['respondidas'])]
    L += ['', '## SÓ O MESTRE']
    L += [f"- {teste.diz(E, r, mestre=True)}" for r in t['dados'] if r['oculto']] + [f"- nota: {n}" for n in t['notas']]
    L += [f"- LUTA ABERTA: {l['arq']} (`ato.py luta roda {l['arq']} \"Nome: ordem\"`)" for l in t['lutas'] if not l['fim']]
    aqui = estado.onde(E, pid); soltos = [f"{i} {it['nome']}" for i, it in E['itens']['itens'].items() if it.get('onde') == aqui and it.get('solto')]
    if soltos: L.append(f"- no chão {estado.em(E, aqui)} (soltas; quem fica com elas entra por evento): " + ' · '.join(soltos[:8]) + (f' · e mais {len(soltos) - 8}' if len(soltos) > 8 else ''))
    P = estado.valida(E); L += [f"- ESTADO QUEBRADO: {x}" for x in P] or ['- o estado está inteiro.']
    return '\n'.join(L) + '\n'


def abre(E):
    txt = mesa(E); open(os.path.join(estado.pasta(), 'MESA.md'), 'w', encoding='utf-8').write(txt); return txt


def pergunta(E, texto, opcoes):
    ops = dict(o.split('=', 1) for o in opcoes if '=' in o)
    if len(ops) < 2 or any(len(k) != 1 or not k.isalpha() for k in ops): sys.exit('a pergunta pede pelo menos duas opções, cada uma com uma letra: "a=..." "b=..."')
    E['turno']['perguntas'].append(dict(texto=texto, opcoes=ops)); return f"pergunta {len(E['turno']['perguntas'])} aberta."


def responde(E, codigos):
    """'1a.2b': cada código tem de bater numa pergunta aberta e numa opção dela. Nada é executado: o Mestre cumpre com os comandos."""
    t = E['turno']; pares = []
    for c in [x for x in codigos.replace(',', '.').replace(' ', '.').split('.') if x]:
        num = ''.join(ch for ch in c if ch.isdigit()); letra = c[len(num):].lower()
        if not num or not 1 <= int(num) <= len(t['perguntas']): sys.exit(f'o código "{c}" não bate em nenhuma pergunta aberta (há {len(t["perguntas"])}). Nada foi marcado.')
        q = t['perguntas'][int(num) - 1]
        if letra not in q['opcoes']: sys.exit(f'a pergunta {num} não tem a opção "{letra}" (tem: {", ".join(q["opcoes"])}). Nada foi marcado.')
        pares.append((int(num) - 1, letra))
    if len({i for i, _ in pares}) != len(pares): sys.exit('a mesma pergunta foi respondida duas vezes. Nada foi marcado.')
    out = []
    for i, letra in pares:
        q = t['perguntas'][i]; t['respondidas'].append(dict(texto=q['texto'], cod=letra, opcao=q['opcoes'][letra])); out.append(f"{i + 1}{letra}: {q['texto']} → {q['opcoes'][letra]}")
    t['perguntas'] = [q for i, q in enumerate(t['perguntas']) if i not in {i for i, _ in pares}]
    return '\n'.join(out) + (f"\nFicam abertas: {len(t['perguntas'])}." if t['perguntas'] else '')


def fecha(E, resumo, parado=False, git=False):
    t = E['turno']; R = []
    R += [f"há uma luta aberta: {l['arq']} (acabe-a com `ato.py luta roda {l['arq']}`; se o arquivo se perdeu, `ato.py luta larga`)" for l in t['lutas'] if not l['fim']]
    if len(t['perguntas']) < 2: R.append(f"há {len(t['perguntas'])} pergunta(s) aberta(s): o turno fecha com pelo menos duas (`turno.py pergunta`)")
    if estado.agora(E) == (t['aberto']['dia'] - 1) * M.BLOCOS_DIA + t['aberto']['bloco'] and not parado: R.append('o relógio não andou neste turno. Todo ato custa tempo; se foi só conversa, feche com `parado`')
    R += [f'o estado quebrou: {x}' for x in estado.valida(E)]
    if not resumo.strip(): R.append('falta dizer o que houve no turno')
    if R: sys.exit('O TURNO NÃO FECHA:\n  - ' + '\n  - '.join(R))
    pid = estado.eu(E); p = E['gente'][pid]; evs = _eventos_desde(t.get('evento0', 0)) + E['_novos']; f = estado.fora(E, pid)
    if p['estado'] != 'vivo': agora = f"**{p['nome']} ESTÁ MORTO:** {estado.morte_diz(E, p)}"
    else: agora = f"{p['nome']} " + (f"FORA, {estado.em(E, f)} (a saída está aberta)" if f else estado.em(E, p['lugar'])) + f" · PV {p['pv']}/{estado.pv_max(p)} · {corpo.diz(p)} · {p['moedas']} de prata"
    L = [f"# RETOMAR · depois do turno {t['n']}", '', f"**Agora:** {estado.quando(E)} · {agora}", '', f"**O que houve no turno {t['n']}:** {resumo}"]
    for linhas in _modulos(E, 'retomar'): L += [''] + linhas
    if t['respondidas']: L += ['', '**Respondido:** ' + ' · '.join(f"{r['texto']} → {r['opcao']}" for r in t['respondidas'])]
    vistos = [f"- Dia {e['dia']}, {M.BLOCOS[e['bloco']]}: {e['texto']}" for e in evs if e['texto'] and e['tipo'] not in ('virada',)]
    resum = []
    for x in vistos:                                        # atos repetidos (oito blocos de sono) viram uma linha só
        if resum and resum[-1][0].split(': ', 1)[1] == x.split(': ', 1)[1]: resum[-1][1] += 1
        else: resum.append([x, 1])
    L += ['', '**Os fatos do turno** (do registro de eventos):'] + [x + (f' (× {k})' if k > 1 else '') for x, k in resum[-25:]]
    L += ['', '## PERGUNTAS ABERTAS'] + [f"{i + 1}. {q['texto']}  " + ' · '.join(f"**{k})** {v}" for k, v in q['opcoes'].items()) for i, q in enumerate(t['perguntas'])]
    ocultas = [f"- {teste.diz(E, r, mestre=True)}" for r in t['dados'] if r['oculto']] + [f"- {n}" for n in t['notas']]
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
    a = sys.argv[1:]
    if not a: print(__doc__); sys.exit()
    E = estado.carrega()
    if a[0] == 'abre': print(abre(E)); sys.exit()
    if a[0] == 'pergunta' and len(a) >= 4: print(pergunta(E, a[1], a[2:])); estado.grava(E)
    elif a[0] == 'responde' and len(a) == 2: print(responde(E, a[1])); estado.grava(E)
    elif a[0] == 'nota' and len(a) == 2: E['turno']['notas'].append(a[1]); estado.grava(E); print('nota guardada (só o Mestre vê).')
    elif a[0] == 'fecha' and len(a) >= 2: print(fecha(E, a[1], parado='parado' in a[2:], git='git' in a[2:]))
    else: print(__doc__)
