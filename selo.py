#!/usr/bin/env python3
"""selo.py — DECLARAR ANTES DE ROLAR, agora garantido pelo script (MOTOR 6).

A regra da mesa: todo dado sai de script, com a tabela escrita no envelope ANTES de rolar.
Antes isso dependia da memória do Mestre. Agora o selo escreve a tabela no envelope, guarda
em selos.json e só então rola. Não dá para rolar sem declarar, nem rolar duas vezes.
O Mestre NÃO precisa abrir o envelope: o selo escreve as linhas DECLARADO e ROLADO sozinho.

Uso:
  python3 selo.py dr ID "título" DADO "TABELA" [oculto] [x=N] [nomes="a,b,c"]
        declara e rola na mesma chamada (a declaração é gravada antes do dado)
  python3 selo.py declara ID "título" DADO "TABELA" [oculto] [x=N] [nomes=...]
  python3 selo.py rola ID
  python3 selo.py conselho ID "pergunta" "opção A:peso" "opção B:peso" ... [oculto]
        o conselho decide no d20: os pesos viram faixas de 1 a 19 e o 20 natural é SURPRESA
  python3 selo.py lote ARQUIVO|-        várias de uma vez (uma por linha:  ID ;; título ;; DADO ;; TABELA ;; opções)
        declara TODAS e depois rola TODAS: um bloco inteiro numa chamada só
  python3 selo.py nota "texto"          uma linha livre no envelope (LEITURA, RESPOSTAS, PARADA)
  python3 selo.py lista [abertos]       os últimos selos (ou só os declarados e não rolados)
  python3 selo.py ver ID

ID: uma etiqueta curta (Z3, 380a). Use "-" para o script dar a próxima do dia.
DADO: d20 · d6 · 2d6 · d100 · d20+3 · d20-2
TABELA: faixas separadas por "|":   "1-4: perdem o rastro | 5-10: perdem na foz | 11-19: acham | 20n: SURPRESA"
   1-4 faixa · 7 um número · 15+ daí para cima · 20n o 20 NATURAL (vale por cima do total) · 1n o 1 natural · resto: o que sobrar
   A tabela tem de cobrir o dado inteiro; se sobrar buraco, o selo recusa.
"""
import re, sys
from nucleo import d, agora, carrega, grava, anota, dia_atual, faixa_txt

ARQ = 'selos.json'
GUARDA = 400   # quantos selos ficam no json (os velhos continuam no envelope)


def load():
    return carrega(ARQ, {'ordem': [], 'selos': {}})


def save(S):
    while len(S['ordem']) > GUARDA:
        velho = S['ordem'].pop(0)
        if S['selos'].get(velho, {}).get('estado') == 'rolado':
            S['selos'].pop(velho, None)
        else:
            S['ordem'].insert(0, velho)
            break
    grava(ARQ, S)


def dado_de(txt):
    m = re.fullmatch(r'(\d*)d(\d+)([+-]\d+)?', txt.replace(' ', '').replace('−', '-'))
    if not m:
        sys.exit(f'dado inválido: "{txt}" (use d20, 2d6, d20+3, d20-2)')
    return int(m.group(1) or 1), int(m.group(2)), int(m.group(3) or 0)


def tabela_de(txt):
    linhas = []
    for parte in [p.strip() for p in txt.split('|') if p.strip()]:
        if ':' not in parte:
            sys.exit(f'faixa sem ":" → "{parte}"')
        chave, res = [x.strip() for x in parte.split(':', 1)]
        chave = chave.replace('–', '-').replace('−', '-')
        if chave.lower() == 'resto':
            linhas.append({'tipo': 'resto', 'res': res})
        elif re.fullmatch(r'\d+n', chave):
            linhas.append({'tipo': 'nat', 'a': int(chave[:-1]), 'res': res})
        elif re.fullmatch(r'\d+\+', chave):
            linhas.append({'tipo': 'num', 'a': int(chave[:-1]), 'b': 10 ** 6, 'res': res})
        elif re.fullmatch(r'\d+-\d+', chave):
            a, b = map(int, chave.split('-'))
            linhas.append({'tipo': 'num', 'a': min(a, b), 'b': max(a, b), 'res': res})
        elif re.fullmatch(r'\d+', chave):
            linhas.append({'tipo': 'num', 'a': int(chave), 'b': int(chave), 'res': res})
        else:
            sys.exit(f'faixa que não entendi: "{chave}" (use 1-4, 7, 15+, 20n ou resto)')
    return linhas


def confere_tabela(tab, n, lados, mod):
    """a tabela cobre tudo o que o dado pode dar? devolve a lista de buracos"""
    nums = sorted([l for l in tab if l['tipo'] == 'num'], key=lambda l: l['a'])
    for x, y in zip(nums, nums[1:]):
        if y['a'] <= x['b']:
            sys.exit(f'faixas que se cruzam: {faixa_txt(x["a"], x["b"])} e {faixa_txt(y["a"], y["b"])}')
    if any(l['tipo'] == 'resto' for l in tab):
        return []
    if not nums:
        return ['a tabela não tem faixa numérica']
    # naturais cobrem as pontas (20n cobre o 20 de um dado só)
    nat = {l['a'] for l in tab if l['tipo'] == 'nat'} if n == 1 else set()
    lo, hi = n + mod, n * lados + mod
    buracos = []
    for v in range(max(lo, nums[0]['a']), min(hi, nums[-1]['b']) + 1):   # abaixo e acima das pontas, a ponta vale
        if not any(l['a'] <= v <= l['b'] for l in nums) and (v - mod) not in nat:
            buracos.append(str(v))
    return buracos


def resolve(tab, nat, total, um_dado):
    if um_dado:
        for l in tab:
            if l['tipo'] == 'nat' and l['a'] == nat:
                return l['res'], f'{nat} NATURAL'
    nums = sorted([l for l in tab if l['tipo'] == 'num'], key=lambda l: l['a'])
    for l in nums:
        if l['a'] <= total <= l['b']:
            return l['res'], ''
    resto = next((l for l in tab if l['tipo'] == 'resto'), None)
    if resto:
        return resto['res'], ''
    if nums and total < nums[0]['a']:
        return nums[0]['res'], 'abaixo da tabela: vale a primeira faixa'
    if nums:
        return nums[-1]['res'], 'acima da tabela: vale a última faixa'
    return '(sem resultado)', ''


def tabela_txt(tab):
    out = []
    for l in tab:
        if l['tipo'] == 'resto':
            out.append(f"resto {l['res']}")
        elif l['tipo'] == 'nat':
            out.append(f"{l['a']} natural {l['res']}")
        elif l['b'] >= 10 ** 6:
            out.append(f"{l['a']}+ {l['res']}")
        else:
            out.append(f"{faixa_txt(l['a'], l['b'])} {l['res']}")
    return ' · '.join(out)


def novo_id(S, dia):
    k = 0
    while True:
        s, x = '', k
        while True:
            s = chr(ord('a') + x % 26) + s
            x = x // 26 - 1
            if x < 0:
                break
        cand = f'{dia}{s}'
        if cand not in S['selos']:
            return cand
        k += 1


def opcoes(args):
    o = {'oculto': False, 'x': 1, 'nomes': []}
    for a in args:
        if a == 'oculto':
            o['oculto'] = True
        elif a.startswith('x='):
            o['x'] = max(1, int(a[2:]))
        elif a.startswith('nomes='):
            o['nomes'] = [n.strip() for n in a[6:].split(',') if n.strip()]
            o['x'] = max(o['x'], len(o['nomes']))
        elif a.strip():
            sys.exit(f'opção que não entendi: "{a}"')
    return o


def declara(S, sid, titulo, dado, tabtxt, o, quieto=False):
    dia = dia_atual()
    if sid in ('-', ''):
        sid = novo_id(S, dia)
    if sid in S['selos']:
        sys.exit(f'o selo {sid} já existe ({S["selos"][sid]["estado"]}): {S["selos"][sid]["titulo"]}. Use outra etiqueta.')
    n, lados, mod = dado_de(dado)
    tab = tabela_de(tabtxt)
    bur = confere_tabela(tab, n, lados, mod)
    if bur:
        sys.exit(f'TABELA COM BURACO no selo {sid} ({dado}): falta cobrir {", ".join(bur[:12])}. Nada foi declarado.')
    selo = {'id': sid, 'dia': dia, 'hora': agora(), 'titulo': titulo, 'dado': [n, lados, mod], 'tabela': tab,
            'oculto': o['oculto'], 'x': o['x'], 'nomes': o['nomes'], 'estado': 'declarado', 'rolagens': []}
    S['selos'][sid] = selo
    S['ordem'].append(sid)
    save(S)                                   # gravado ANTES de qualquer dado
    dtxt = f"{n if n > 1 else ''}d{lados}" + (f' {mod:+d}' if mod else '')
    vezes = f' × {o["x"]}' + (f' ({", ".join(o["nomes"])})' if o['nomes'] else '') if o['x'] > 1 else ''
    linha = f"- DECLARADO ({sid}) [Dia {dia}, {selo['hora'][:5]}] {'(OCULTO) ' if o['oculto'] else ''}{titulo}, {dtxt}{vezes}: {tabela_txt(tab)}"
    anota(linha)
    if not quieto:
        print(linha[2:])
    return sid


def rola(S, sid, quieto=False):
    if sid not in S['selos']:
        sys.exit(f'o selo {sid} NÃO FOI DECLARADO. Declarar antes de rolar: selo.py declara {sid} ...')
    s = S['selos'][sid]
    if s['estado'] == 'rolado':
        print(f'o selo {sid} JÁ FOI ROLADO (não se rola duas vezes): ' + ' · '.join(r['txt'] for r in s['rolagens']))
        return s
    n, lados, mod = s['dado']
    partes = []
    for k in range(s['x']):
        dados = [d(lados) for _ in range(n)]
        total = sum(dados) + mod
        res, obs = resolve(s['tabela'], dados[0], total, n == 1)
        quem = (s['nomes'][k] + ' ') if k < len(s['nomes']) else (f'#{k + 1} ' if s['x'] > 1 else '')
        conta = f'{dados}' + (f' {mod:+d} = {total}' if mod or n > 1 else '')
        txt = f'{quem}{conta} → {res}' + (f' ({obs})' if obs else '')
        s['rolagens'].append({'dados': dados, 'total': total, 'res': res, 'txt': txt})
        partes.append(txt)
    s['estado'] = 'rolado'
    s['hora_rolado'] = agora()
    save(S)
    linha = f"- ROLADO ({sid}) [{s['hora_rolado'][:5]}] {'(OCULTO) ' if s['oculto'] else ''}{s['titulo']}: " + ' · '.join(partes)
    anota(linha)
    if not quieto:
        print(linha[2:])
    return s


def pesos_para_tabela(opcs):
    """["A:6","B:8"] -> faixas de 1 a 19 proporcionais aos pesos; 20 natural = SURPRESA"""
    itens = []
    for o in opcs:
        if ':' not in o:
            sys.exit(f'opção sem peso: "{o}" (use "texto:peso")')
        t, p = o.rsplit(':', 1)
        itens.append((t.strip(), float(p)))
    tot = sum(p for _, p in itens)
    if tot <= 0 or len(itens) > 19:
        sys.exit('pesos inválidos (de 1 a 19 opções, peso maior que zero)')
    cotas = [p * 19 / tot for _, p in itens]
    faces = [max(1, int(c)) for c in cotas]
    while sum(faces) > 19:
        i = max(range(len(faces)), key=lambda j: (faces[j] - cotas[j], faces[j]))
        faces[i] -= 1
    while sum(faces) < 19:
        i = max(range(len(faces)), key=lambda j: cotas[j] - faces[j])
        faces[i] += 1
    partes, ini = [], 1
    for (t, _), f in zip(itens, faces):
        partes.append(f'{faixa_txt(ini, ini + f - 1)}: {t}')
        ini += f
    partes.append('20n: SURPRESA (gerador novidade)')
    return ' | '.join(partes)


def main():
    a = sys.argv[1:]
    if not a or a[0] in ('-h', '--help', 'ajuda'):
        print(__doc__)
        return
    S = load()
    c = a[0]
    if c in ('declara', 'dr'):
        if len(a) < 5:
            sys.exit('uso: selo.py ' + c + ' ID "título" DADO "TABELA" [oculto] [x=N] [nomes="a,b"]')
        sid = declara(S, a[1], a[2], a[3], a[4], opcoes(a[5:]))
        if c == 'dr':
            rola(S, sid)
    elif c == 'rola':
        if len(a) < 2:
            sys.exit('uso: selo.py rola ID')
        for sid in a[1:]:
            rola(S, sid)
    elif c == 'conselho':
        if len(a) < 4:
            sys.exit('uso: selo.py conselho ID "pergunta" "opção A:peso" "opção B:peso" ...')
        ops = [x for x in a[3:] if ':' in x]
        resto = [x for x in a[3:] if ':' not in x]
        sid = declara(S, a[1], 'O CONSELHO: ' + a[2], 'd20', pesos_para_tabela(ops), opcoes(resto))
        rola(S, sid)
    elif c == 'lote':
        if len(a) < 2:
            sys.exit('uso: selo.py lote ARQUIVO   (ou "-" para ler da entrada)')
        txt = sys.stdin.read() if a[1] == '-' else open(a[1], encoding='utf-8').read()
        ids = []
        for n, l in enumerate(txt.splitlines(), 1):
            l = l.strip()
            if not l or l.startswith('#'):
                continue
            campos = [x.strip() for x in l.split(';;')]
            if len(campos) < 4:
                sys.exit(f'linha {n} do lote: preciso de  ID ;; título ;; DADO ;; TABELA  (achei {len(campos)} campos). Nada foi rolado.')
            ids.append(declara(S, campos[0], campos[1], campos[2], campos[3], opcoes(campos[4].split() if len(campos) > 4 else [])))
        print('— todas declaradas; agora os dados —')
        for sid in ids:
            rola(S, sid)
    elif c == 'nota':
        if len(a) < 2:
            sys.exit('uso: selo.py nota "texto"')
        linha = f'- [Dia {dia_atual()}, {agora()[:5]}] ' + ' '.join(a[1:])
        anota(linha)
        print('anotado no envelope:', linha[2:])
    elif c == 'lista':
        so_abertos = len(a) > 1 and a[1].startswith('abert')
        ids = [i for i in S['ordem'] if i in S['selos'] and (not so_abertos or S['selos'][i]['estado'] == 'declarado')]
        for i in ids[-(200 if so_abertos else 15):]:
            s = S['selos'][i]
            fim = ' · '.join(r['txt'] for r in s['rolagens']) if s['rolagens'] else 'À ESPERA DO DADO'
            print(f"({i}) Dia {s['dia']} {'(OCULTO) ' if s['oculto'] else ''}{s['titulo']} → {fim}")
        if not ids:
            print('nenhum selo aberto.' if so_abertos else 'nenhum selo ainda.')
    elif c == 'ver':
        s = S['selos'].get(a[1]) if len(a) > 1 else None
        if not s:
            sys.exit('selo não achado')
        n, lados, mod = s['dado']
        print(f"({s['id']}) Dia {s['dia']} {s['hora']} · {s['titulo']} · {n}d{lados}{mod:+d} · {s['estado']}")
        print('  ' + tabela_txt(s['tabela']))
        for r in s['rolagens']:
            print('  → ' + r['txt'])
    else:
        sys.exit(f'comando que não conheço: {c}\n' + __doc__)


if __name__ == '__main__':
    main()
