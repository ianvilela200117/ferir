#!/usr/bin/env python3
"""npc.py — a ficha curta de quem está em cena (MOTOR 6). Lê e mexe no npcs.json sem o Mestre abrir o arquivo.

O npcs.json tem mais de 200 mil letras, e quatro quintos disso são diários velhos de cada NPC. O protocolo antigo
mandava ler o arquivo inteiro. Agora o Mestre pede só as fichas de quem entra na cena.

Uso:
  python3 npc.py cena NOME [NOME...]         as fichas curtas (nível, classe, ocupação, o que quer, as últimas 10 notas inteiras)
  python3 npc.py ver NOME [tudo]             uma ficha (com "tudo": o diário inteiro, incluindo o arquivado)
  python3 npc.py busca TERMO                 quem tem esse termo no nome, na classe, na ocupação ou nas notas
  python3 npc.py lista [N]                   uma linha por NPC, do nível mais alto para baixo
  python3 npc.py nota NOME "o que houve"     uma nota datada no diário do NPC
  python3 npc.py ocupa NOME "ocupação nova"  muda a ocupação (o que ele faz na semana)
  python3 npc.py estado NOME "MORTO no 382"  muda o estado (MORTO tira da semana e das faíscas)
  python3 npc.py nivel NOME N "motivo"       dá nível a uma ficha sem nível (ou corrige)
  python3 npc.py novo NOME NIVEL "classe" "ocupação"
  python3 npc.py lealdade NOME +N|-N "motivo"  a LEALDADE à casa, de 0 a 10 (começa em 6 na primeira vez). 3 ou menos: em risco de partir ou trair
  python3 npc.py lealdades                   quem tem lealdade marcada, do mais frio ao mais firme
  python3 npc.py arquiva [manter=8]          passa as notas velhas de cada NPC para npcs_arquivo.json (nada se apaga)
  python3 npc.py vida NOME [NOME...]|todos  MOTOR 9.1 (438): o que falta de DESEJO, AMBIÇÃO, MEDO, SEGREDO e LINHA VERMELHA: primeiro tira do texto
                                           da ficha (e dos Lendários do mundo_vivo); o que ainda faltar sai no dado (as listas do gerador.py; selo, OCULTO)
O nome pode vir sem acento, em minúscula ou pela metade.
"""
import sys
from nucleo import carrega, grava, dia_atual, acha_nome

ARQ = 'npcs.json'
VELHO = 'npcs_arquivo.json'


def acha(db, nome):
    k, sug = acha_nome(nome, db.keys())
    if not k:
        sys.exit(f'NPC não achado: "{nome}".' + (f' Parecidos: {", ".join(sug)}.' if sug else '') + ' (npc.py busca TERMO procura nas notas)')
    return k


def ficha(n, v, notas=10, tudo=False):
    xp = f"XP {v['xp']}/{100 * v['nivel']}" if v.get('nivel') else 'SEM NÍVEL (gerar: npc.py nivel)'
    print(f"{n.upper()} · nível {v.get('nivel') or '?'} · {xp}" + (' · LENDÁRIO' if v.get('lendario') else '') + (f" · {v['estado']}" if v.get('estado') else ''))
    try:
        from onde import lugar_de
        lg = lugar_de(n)
        if lg != 'Ireviel': print(f'  ⚠ ONDE: {lg} (não está em Ireviel)')
    except ImportError: pass
    print(f"  classe: {v.get('classe') or '—'}" + (f" · CLASSE DO LIVRO: {v['classe_livro']}" + (f" ({' · '.join(v['assinaturas'])}; fraqueza: {v.get('fraqueza', '')})" if v.get('assinaturas') else '') if v.get('classe_livro') and v['classe_livro'].lower() not in str(v.get('classe', '')).lower() else ''))
    print(f"  ocupação: {v.get('ocupacao') or '—'}")
    if v.get('lealdade') is not None:
        print(f"  lealdade à casa: {v['lealdade']}/10" + (' ⚠ EM RISCO' if v['lealdade'] <= 3 else '') + (f" · votos vencidos no conselho: {v['votos_vencidos']}" if v.get('votos_vencidos') else ''))
    quer = [f"{rot} {v[k]}" for k, rot in (('desejo', 'quer'), ('ambicao', 'ambição:'), ('medo', 'teme'), ('linha_vermelha', 'linha vermelha:')) if v.get(k)]
    if quer:
        print('  ' + ' · '.join(quer))
    if v.get('segredo'):
        print(f"  [OCULTO] segredo: {v['segredo']}")
    log = v.get('log', [])
    if tudo:
        velho = carrega(VELHO, {}).get(n, [])
        for l in velho + log:
            print('   · ' + l)
    else:
        for l in log[-notas:]:
            print('   · ' + l)
        if len(log) > notas:
            print(f'   (+{len(log) - notas} notas mais antigas: npc.py ver {n} tudo)')


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        return
    db = carrega(ARQ)
    c = a[0]
    dia = dia_atual()
    if c in ('cena', 'ver'):
        tudo = c == 'ver' and 'tudo' in a[2:]
        for nome in [x for x in a[1:] if x != 'tudo']:
            k, sug = acha_nome(nome, db.keys())
            if not k:   # um nome que falta não derruba a cena inteira
                print(f'{nome.upper()} · não está no livro dos NPCs.' + (f' Parecidos: {", ".join(sug)}.' if sug else '') + f' (python3 confere.py {nome}  ·  ficha nova: npc.py novo)')
                continue
            ficha(k, db[k], tudo=tudo)
    elif c == 'busca':
        t = a[1].lower()
        achou = 0
        for n, v in db.items():
            campos = [n, v.get('classe') or '', v.get('ocupacao') or ''] + v.get('log', [])[-12:]
            hits = [x for x in campos if t in x.lower()]
            if hits:
                achou += 1
                print(f"{n} (nível {v.get('nivel') or '?'}): {hits[-1][:170]}")
        if not achou:
            print('ninguém no livro dos NPCs. (Fato antigo: python3 confere.py TERMO)')
    elif c == 'lista':
        lim = int(a[1]) if len(a) > 1 and a[1].isdigit() else None
        for n, v in sorted(db.items(), key=lambda x: -(x[1].get('nivel') or 0))[:lim]:
            print(f"{n} {v.get('nivel') or '?'} · {(v.get('classe') or '—')[:40]} · {(v.get('ocupacao') or '—')[:70]}" + (f" · {v['estado'][:30]}" if v.get('estado') else ''))
    elif c in ('nota', 'ocupa', 'estado') and len(a) > 2:
        k = acha(db, a[1])
        if c == 'nota':
            db[k].setdefault('log', []).append(f'Dia {dia}: {a[2]}')
        elif c == 'ocupa':
            db[k].setdefault('log', []).append(f"Dia {dia}: ocupação nova (antes: {db[k].get('ocupacao', '')})")
            db[k]['ocupacao'] = a[2]
        else:
            db[k]['estado'] = a[2]
            db[k].setdefault('log', []).append(f'Dia {dia}: estado → {a[2]}')
        grava(ARQ, db)
        print(f'{k}: anotado ({c}).')
    elif c == 'nivel' and len(a) > 2:
        k = acha(db, a[1])
        velho = db[k].get('nivel')
        db[k]['nivel'] = int(a[2])
        db[k].setdefault('log', []).append(f"Dia {dia}: nível {velho} → {a[2]} ({a[3] if len(a) > 3 else 'ficha gerada'})")
        grava(ARQ, db)
        print(f'{k}: nível {velho} → {a[2]}')
    elif c == 'novo' and len(a) > 4:
        if a[1] in db:
            sys.exit(f'{a[1]} já está no livro.')
        db[a[1]] = {'nivel': int(a[2]), 'xp': 0, 'log': [f'Dia {dia}: entra no livro (nível {a[2]})'], 'classe': a[3], 'ocupacao': a[4]}
        grava(ARQ, db)
        print(f'{a[1]} entrou no livro: nível {a[2]}, {a[3]}. (O nome passou pelo nomes.py livre?)')
    elif c == 'lealdade' and len(a) > 2:
        k = acha(db, a[1]); antes = db[k].get('lealdade'); base = 6 if antes is None else antes
        db[k]['lealdade'] = max(0, min(10, base + int(a[2].replace('+', ''))))
        db[k].setdefault('log', []).append(f"Dia {dia}: lealdade {base} → {db[k]['lealdade']} ({a[3] if len(a) > 3 else ''})")
        grava(ARQ, db); print(f"{k}: lealdade {base} → {db[k]['lealdade']}/10" + (' ⚠ EM RISCO: pode partir, calar ou trair (o Mestre declara a tabela quando a hora chegar)' if db[k]['lealdade'] <= 3 else ''))
    elif c == 'lealdades':
        for nn, v in sorted([(x, y) for x, y in db.items() if y.get('lealdade') is not None], key=lambda x: x[1]['lealdade']):
            print(f"{nn}: {v['lealdade']}/10" + (' ⚠' if v['lealdade'] <= 3 else '') + (f" · votos vencidos {v['votos_vencidos']}" if v.get('votos_vencidos') else ''))
    elif c == 'arquiva':
        manter = next((int(x[7:]) for x in a[1:] if x.startswith('manter=')), 8)
        velho = carrega(VELHO, {})
        movidas = 0
        for n, v in db.items():
            log = v.get('log', [])
            if len(log) > manter:
                velho.setdefault(n, []).extend(log[:-manter])
                movidas += len(log) - manter
                v['log'] = log[-manter:]
        grava(VELHO, velho)
        grava(ARQ, db)
        print(f'{movidas} notas velhas foram para {VELHO}; cada NPC ficou com as últimas {manter}. Nada foi apagado.')
    elif c == 'vida' and len(a) > 1:
        vida(db, a[1:], dia)
    else:
        print(__doc__)


CAMPOS = [('desejo', 'DESEJO'), ('ambicao', 'AMBICAO'), ('medo', 'MEDO'), ('segredo', 'SEGREDO'), ('linha_vermelha', 'LINHA')]


def vida(db, nomes, dia):
    """MOTOR 9.1: desejo, ambição, medo, segredo e linha vermelha para quem não tem (do texto da ficha; senão, do dado)"""
    import re
    import gerador, selo
    from nucleo import anota, sem_acento
    lend = {sem_acento(l['nome'].split(',')[0]): l for l in carrega('mundo_vivo.json', {}).get('lendarios', [])}
    alvo = [k for k, v in db.items() if 'MORT' not in str(v.get('estado', '')).upper() and 'servo armado' not in str(v.get('classe', ''))] if nomes == ['todos'] else [acha(db, n) for n in nomes]
    tirou, falta = [], {c: [] for c, _ in CAMPOS}
    rx = {'desejo': r'desejo:?\s+([^·;]+)', 'ambicao': r'ambi[cç][aã]o(?:\s*\(4\))?:?\s+([^·;]+)', 'medo': r'medo:?\s+([^·;]+)', 'segredo': r'segredo:?\s+([^·;]+)', 'linha_vermelha': r'linha vermelha:?\s+([^·;]+)'}
    for k in alvo:
        v = db[k]; txt = f"{v.get('classe', '')} · {v.get('ocupacao', '')}"; L = lend.get(sem_acento(k))
        for c, _ in CAMPOS:
            if v.get(c): continue
            if L and L.get(c): v[c] = L[c]; tirou.append(f'{k}.{c} (mundo_vivo)'); continue
            m = re.search(rx[c], txt, re.I) or (re.search(r'(nunca [^·;]+)', txt, re.I) if c == 'linha_vermelha' else None)   # 441: a linha vermelha escrita sem rótulo
            if m and len(m.group(1).strip()) > 3: v[c] = m.group(1).strip().rstrip('.'); tirou.append(f'{k}.{c} (texto)'); continue
            falta[c].append(k)
    grava(ARQ, db)
    if tirou: anota(f"- VIDA DOS NPCs (438, MOTOR 9.1): tirado do que já estava escrito: {', '.join(tirou)}")
    Z = selo.load(); feitos = 0
    for c, lista in CAMPOS:
        nm = falta[c]
        if not nm: continue
        L_ = getattr(gerador, lista)
        sid = selo.declara(Z, '-', f'{c.upper().replace("_", " ")} DOS NPCs QUE NÃO TÊM (gerador.py, 1d{len(L_)} cada)', f'd{len(L_)}', ' | '.join(f'{i + 1}: {x}' for i, x in enumerate(L_)), selo.opcoes(['oculto', f'x={len(nm)}', 'nomes=' + ','.join(nm)]), quieto=True)
        db = carrega(ARQ)
        for k, r in zip(nm, selo.rola(Z, sid, quieto=True)['rolagens']):
            val = L_[r['total'] - 1]
            if c == 'linha_vermelha' and 'facção X' in val: val = val.replace('facção X', 'facção X (o Mestre declara qual quando a linha for posta à prova)')
            db[k][c] = val + (' (OCULTO)' if c == 'segredo' else ''); db[k].setdefault('log', []).append(f'Dia {dia}: {c.replace("_", " ")} pelo dado (438)'); feitos += 1
        grava(ARQ, db)
    print(f'vida: {len(tirou)} campos tirados do que já estava escrito · {feitos} rolados (selo, oculto) · ' + ' · '.join(f'{c}: {len(falta[c])}' for c, _ in CAMPOS))


if __name__ == '__main__':
    main()
