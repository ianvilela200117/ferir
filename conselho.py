#!/usr/bin/env python3
"""conselho.py — O CONSELHO VOTA, cadeira por cadeira (MOTOR 6.1). "O reino não é autocracia: o conselho vota, e tudo
passa pela Intendente." Antes o conselho era uma tabela só de d20. Agora cada conselheiro presente vota: rola d20 para
cada opção e soma a INCLINAÇÃO que o Mestre declara pelo que aquela pessoa é e quer; fica com a maior. Vence a opção
com mais votos; no empate, decide a Intendente. Quem perde fica anotado (voto vencido vira atrito, favor ou rancor).
A declaração (opções, inclinações, quem falta) é gravada no envelope ANTES dos dados, como no selo.

Uso:
  python3 conselho.py ID "pergunta" "A: entregar a carta" "B: abrir e ler" "C: usar de isca" [inclinações] [fora=Nome,Nome] [oculto]
  inclinação:  Sira=B+4   Eliane=A+2,C-3   (sem inclinação, a cadeira vota pelo dado puro)
  Quem está fora da cidade não vota: fora=Tolvane
As cadeiras vêm do reino.json (conselho_real). A Nouliel tem duas cadeiras e um voto só.
"""
import re, sys
from nucleo import d, carrega, grava, anota, agora, dia_atual, acha_nome


def main():
    a = sys.argv[1:]
    if len(a) < 4:
        sys.exit(__doc__)
    sid, pergunta = a[0], a[1]
    ops = {}
    incl = {}
    fora = []
    oculto = False
    R = carrega('reino.json')['reino']
    cadeiras = {}
    for cargo, quem in R.get('conselho_real', {}).items():
        nome = quem.split(' (')[0].strip()
        cadeiras.setdefault(nome, []).append(cargo.split(' (')[0])
    for x in a[2:]:
        m = re.match(r'^([A-Z]):\s*(.+)$', x)
        if m:
            ops[m.group(1)] = m.group(2)
        elif x.startswith('fora='):
            fora = [acha_nome(n.strip(), cadeiras)[0] or n.strip() for n in x[5:].split(',')]
        elif x == 'oculto':
            oculto = True
        elif '=' in x:
            nome, resto = x.split('=', 1)
            k, sug = acha_nome(nome, cadeiras)
            if not k:
                sys.exit(f'"{nome}" não tem cadeira no conselho. Cadeiras: {", ".join(cadeiras)}. Nada foi rolado.')
            for p in resto.split(','):
                mm = re.match(r'^([A-Z])([+-]\d+)$', p.strip().replace('−', '-'))
                if not mm:
                    sys.exit(f'inclinação que não entendi: "{p}" (use Nome=B+4 ou Nome=A+2,C-3). Nada foi rolado.')
                incl.setdefault(k, {})[mm.group(1)] = int(mm.group(2))
        else:
            sys.exit(f'não entendi: "{x}". Nada foi rolado.')
    if len(ops) < 2:
        sys.exit('preciso de pelo menos duas opções ("A: ..." "B: ...").')
    S = carrega('selos.json', {'ordem': [], 'selos': {}})
    if sid in S['selos']:
        sys.exit(f'a etiqueta {sid} já foi usada. Use outra.')
    presentes = [n for n in cadeiras if n not in fora]
    dia = dia_atual()
    tag = '(OCULTO) ' if oculto else ''
    decl = (f"- DECLARADO ({sid}) [Dia {dia}, {agora()[:5]}] {tag}O CONSELHO VOTA: {pergunta} · " + ' · '.join(f'{k}) {v}' for k, v in ops.items())
            + ' · cada cadeira: d20 por opção + inclinação, fica com a maior; maioria vence; empate: a Intendente · votam: ' + ', '.join(presentes)
            + (' · fora: ' + ', '.join(fora) if fora else '')
            + (' · inclinações: ' + '; '.join(f"{n} " + ','.join(f'{o}{v:+d}' for o, v in iv.items()) for n, iv in incl.items()) if incl else ' · sem inclinações'))
    S['selos'][sid] = {'id': sid, 'dia': dia, 'hora': agora(), 'titulo': 'O CONSELHO VOTA: ' + pergunta, 'dado': [1, 20, 0], 'tabela': [], 'oculto': oculto, 'x': 1, 'nomes': [], 'estado': 'declarado', 'rolagens': []}
    S['ordem'].append(sid)
    grava('selos.json', S)
    anota(decl)
    print(decl[2:])
    votos = {k: [] for k in ops}
    linhas = []
    for n in presentes:
        while True:
            rol = {k: d(20) for k in ops}
            tot = {k: rol[k] + incl.get(n, {}).get(k, 0) for k in ops}
            top = max(tot.values())
            lideres = [k for k in ops if tot[k] == top]
            if len(lideres) == 1:
                break
        esc = lideres[0]
        votos[esc].append(n)
        linhas.append(f"{n} ({' e '.join(cadeiras[n])}): " + ' '.join(f"{k}[{rol[k]}]{incl.get(n, {}).get(k, 0):+d}" if incl.get(n, {}).get(k) else f'{k}[{rol[k]}]' for k in ops) + f' → {esc}')
    maior = max(len(v) for v in votos.values())
    lideres = [k for k in ops if len(votos[k]) == maior]
    intendente = next((n for n, cs in cadeiras.items() if 'Intendente' in cs), None)
    desempate = ''
    if len(lideres) > 1:
        vi = next((k for k in lideres if intendente in votos[k]), None)
        if vi:
            venc = vi
            desempate = f' (EMPATE em {maior} votos: decide a Intendente, {intendente})'
        else:
            venc = lideres[d(len(lideres)) - 1]
            desempate = f' (EMPATE em {maior} votos e a Intendente votou em outra: ela desempata no dado entre {", ".join(lideres)})'
    else:
        venc = lideres[0]
    placar = ' · '.join(f'{k} {len(votos[k])}' for k in ops)
    vencidos = [n for k in ops if k != venc for n in votos[k]]
    for l in linhas:
        print('  ' + l)
    res = f"VENCE {venc}) {ops[venc]} · placar {placar}{desempate}" + (f" · VOTO VENCIDO: {', '.join(vencidos)}" if vencidos else ' · unânime')
    print('  ' + res)
    anota(f"- ROLADO ({sid}) [{agora()[:5]}] {tag}O CONSELHO: " + ' ‖ '.join(linhas) + ' ‖ ' + res)
    S = carrega('selos.json')
    S['selos'][sid]['estado'] = 'rolado'
    S['selos'][sid]['rolagens'] = [{'dados': [], 'total': 0, 'res': res, 'txt': res}]
    grava('selos.json', S)
    db = carrega('npcs.json')
    # MOTOR 7.1 (Dia 397): a mágoa conta votos vencidos SEGUIDOS (zera quando a cadeira vence), como o texto sempre disse.
    # Antes a conta era pelo total e nunca zerava: toda cadeira perdia lealdade com o tempo, por mais que vencesse.
    for n in votos[venc]:
        k, _ = acha_nome(n, db)
        if k:
            db[k]['votos_seguidos'] = 0
    for n in vencidos:
        k, _ = acha_nome(n, db)
        if k:
            db[k]['votos_vencidos'] = db[k].get('votos_vencidos', 0) + 1
            db[k]['votos_seguidos'] = db[k].get('votos_seguidos', 0) + 1
            if db[k]['votos_seguidos'] >= 3:
                db[k]['votos_seguidos'] = 0
                db[k]['lealdade'] = max(0, (6 if db[k].get('lealdade') is None else db[k]['lealdade']) - 1); print(f"  {k}: terceiro voto vencido seguido de mágoa: lealdade → {db[k]['lealdade']}/10")
            db[k].setdefault('log', []).append(f"Dia {dia}: VOTO VENCIDO no conselho ({pergunta[:60]}): queria {next(o for o in ops if n in votos[o])}) {ops[next(o for o in ops if n in votos[o])][:50]}")
    grava('npcs.json', db)



if __name__ == '__main__':
    main()
