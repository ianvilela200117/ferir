#!/usr/bin/env python3
"""turno.py — MOTOR 10: O TURNO EM DOIS COMANDOS. `abre` gera a página do Mestre a partir do estado; `fecha` recusa fechar se algo ficou solto.

  python3 turno.py abre                         só lê. Gera e mostra a MESA.md: o relógio, o corpo, o lugar, o que dá para fazer, as perguntas abertas, e o SÓ O MESTRE.
  python3 turno.py responde "1a.2b"             confere os códigos do jogador contra as perguntas abertas e diz o que cada um quer dizer
  python3 turno.py pergunta "texto" "a=..." "b=..." ["c=..."]     abre uma pergunta para o fim do turno
  python3 turno.py nota "o que só o Mestre sabe"                  uma nota oculta (vai para o RETOMAR, na parte do Mestre)
  python3 turno.py fecha "o que houve" [parado] [git]             fecha o turno. `parado`: o turno foi só conversa, o relógio não andou. `git`: guarda no git e envia.

`fecha` RECUSA se: há luta aberta · há menos de 2 perguntas abertas
· o relógio não andou (e não foi dito `parado`) · o estado quebrou um invariante (moeda negativa, peça com dono que não existe, morto vestido...).
No meio do turno usa-se: ato.py (o que a pessoa faz), teste.py (o dado), ato.py luta (a luta).
"""
import json, os, subprocess, sys
import tabelas_mundo as M
import estado, corpo, pessoas, teste


def _eventos_desde(n):
    arq = os.path.join(estado.pasta(), 'eventos.jsonl')
    if not os.path.exists(arq): return []
    return [e for e in map(json.loads, open(arq, encoding='utf-8').read().splitlines()) if e['id'] > n]


def _voce(E):
    pid = estado.eu(E); p = E['gente'][pid]; l = E['lugares'][p['lugar']]
    L = [f"**{p['nome']}**, nível {p['nivel']} · PV {p['pv']}/{estado.pv_max(p)} · {p['moedas']} de prata · {l.get('em', 'em ' + l['nome'])}", f"Corpo: {corpo.diz(p)}"]
    for f in p['feridas']: L.append(f"Ferida{' GRAVE' if f['grave'] else ''}: {f['parte']} (Dia {f['dia']}; {f['repouso']} de {M.FERIDA_DIAS[1 if f['grave'] else 0]} dias de repouso)")
    L.append('```'); L.append(pessoas.linha(pessoas.ficha(estado.lutador(E, pid)))); L.append('```')
    tr = [f"{a}: {b} blocos" + (f" ({pessoas.T.MAESTRIAS[p.get('maestria', {}).get(a, 0)]})") for a, b in p.get('treino', {}).items()]
    if tr: L.append('Treino: ' + ' · '.join(tr))
    return L


def _aqui(E):
    pid = estado.eu(E); p = E['gente'][pid]; l = E['lugares'][p['lugar']]; of = p.get('grau_oficio', 'diarista')
    L = [f"**{l['nome']}** · comida no lugar: {l['estoque'].get('comida', 0)} · {'há cama' if l.get('cama') else 'não há cama: dorme-se no chão'}"]
    outros = [q['nome'] for k, q in E['gente'].items() if k != pid and q['lugar'] == p['lugar'] and q['estado'] == 'vivo']
    if outros: L.append('Quem está aqui: ' + ', '.join(outros))
    L += ['', '**O que dá para fazer, e o que custa** (1 bloco = 4 horas):',
          f"- comer: {M.REFEICAO_PRECO} de prata, fome {M.REFEICAO} (`ato.py comer`)",
          f"- dormir: {'cama por ' + str(M.CAMA_PRECO) + ' de prata; ' if l.get('cama') else ''}cada bloco tira {-M.SONO_CAMA} de sono e de cansaço (no chão, {-M.SONO_CHAO}) e devolve PV (`ato.py dormir N`)",
          f"- trabalhar ({of}): {M.SALARIO[of]} de prata por bloco, esforço {M.ESFORCO_OFICIO[of]} (`ato.py trabalhar N`)",
          f"- treinar com uma arma: esforço pesado; a maestria sobe aos {', '.join(str(v) for v in M.MAESTRIA_BLOCOS.values())} blocos (`ato.py treinar N ARMA`)",
          "- descansar, esperar (`ato.py descansar N`, `ato.py esperar N`) · lutar (`ato.py luta nova CENARIO ARQ`) · testar (`teste.py`)"]
    return L


def mesa(E):
    t = E['turno']; L = [f"# MESA · turno {t['n']} · {estado.quando(E)}", '', '## Você'] + _voce(E) + ['', '## Aqui'] + _aqui(E)
    L += ['', '## Perguntas abertas']
    L += [f"{i + 1}. {q['texto']}  " + ' · '.join(f"**{k})** {v}" for k, v in q['opcoes'].items()) for i, q in enumerate(t['perguntas'])] or ['(nenhuma: o turno precisa abrir pelo menos duas antes de fechar)']
    if t['respondidas']: L += ['', '**Respondido neste turno (cumprir antes de fechar):** ' + ' · '.join(f"{r['texto']} → {r['cod']}) {r['opcao']}" for r in t['respondidas'])]
    L += ['', '## SÓ O MESTRE']
    L += [f"- {teste.diz(E, r, mestre=True)}" for r in t['dados'] if r['oculto']] + [f"- nota: {n}" for n in t['notas']]
    L += [f"- LUTA ABERTA: {l['arq']}" for l in t['lutas'] if not l['fim']]
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
    R += [f"há uma luta aberta: {l['arq']} (acabe-a com `ato.py luta roda`)" for l in t['lutas'] if not l['fim']]
    if len(t['perguntas']) < 2: R.append(f"há {len(t['perguntas'])} pergunta(s) aberta(s): o turno fecha com pelo menos duas (`turno.py pergunta`)")
    if estado.agora(E) == (t['aberto']['dia'] - 1) * M.BLOCOS_DIA + t['aberto']['bloco'] and not parado: R.append('o relógio não andou neste turno. Todo ato custa tempo; se foi só conversa, feche com `parado`')
    R += [f'o estado quebrou: {x}' for x in estado.valida(E)]
    if not resumo.strip(): R.append('falta dizer o que houve no turno')
    if R: sys.exit('O TURNO NÃO FECHA:\n  - ' + '\n  - '.join(R))
    p = E['gente'][estado.eu(E)]; evs = _eventos_desde(t.get('evento0', 0)) + E['_novos']
    L = [f"# RETOMAR · depois do turno {t['n']}", '', f"**Agora:** {estado.quando(E)} · {p['nome']} {E['lugares'][p['lugar']].get('em', 'em ' + E['lugares'][p['lugar']]['nome'])} · PV {p['pv']}/{estado.pv_max(p)} · {corpo.diz(p)} · {p['moedas']} de prata",
         '', f"**O que houve no turno {t['n']}:** {resumo}"]
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
