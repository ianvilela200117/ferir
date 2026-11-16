#!/usr/bin/env python3
"""classe.py — MOTOR 7: AS ASSINATURAS DA CLASSE NA FICHA DE CADA NPC (tiradas do Livro, compendio/04_classes.md).

A classe deixa de ser só um nome: a ficha passa a guardar as 3 assinaturas e a fraqueza, e o Mestre as vê
no cartão de cena (tracos.py cena). Nada é inventado: o que não está no Livro fica listado para o Mestre gerar.

Uso:
  python3 classe.py livro [FAMÍLIA]      as classes do Livro (família, raridade)
  python3 classe.py ver NOME_DA_CLASSE   assinaturas e fraqueza de uma classe
  python3 classe.py npc NOME             o que a classe do NPC faz
  python3 classe.py migra                grava assinaturas e fraqueza em npcs.json para quem tem classe do Livro
  python3 classe.py faltam               NPCs cuja classe não está no Livro (gerar ou corrigir)
MOTOR 9.1 (438, pedido do jogador: "as fichas dos NPCs fora do Livro"):
  python3 classe.py liga NOME "Classe do Livro" ["motivo"]   o texto da ficha é sinônimo de uma classe do Livro (leitura do Mestre, anotada)
  python3 classe.py gera NOME [FAMÍLIA]                      sem classe escrita: o dado escolhe (a família no d11 se não vier; a classe no dN
                                                             da família, sem as Lendárias, que pedem Trilha 20); pelo selo, OCULTO
"""
import re, sys
from nucleo import carrega, grava, ler, sem_acento


def livro():
    """{chave: {'nome','familia','raridade','assinaturas':[...],'fraqueza'}} lido do compêndio."""
    L, fam, rar, cur = {}, '', '', None
    for ln in ler('compendio/04_classes.md').split('\n'):
        m = re.match(r'^###? Classes d[aeo]s? (.+)$', ln.strip())
        if m: fam = m.group(1).strip(); cur = None; continue
        m = re.match(r'^\*\*(Comum|Incomum|Raro|Épico|Único|Lendário):?\*\*', ln.strip())   # 438: o leitor só pegava "**Comum:**" e marcava tudo como a 1ª raridade
        if m: rar = m.group(1).strip(); cur = None; continue
        m = re.match(r'^- \*\*([^*]+)\*\*\s*$', ln)
        if m and fam:
            cur = {'nome': m.group(1).strip(), 'familia': fam, 'raridade': rar, 'assinaturas': [], 'fraqueza': ''}
            L[sem_acento(cur['nome']).lower()] = cur; continue
        if cur is None: continue
        m = re.match(r'^\s+- \*\*([^*]+)\*\*\s*(\([^)]*\))?:?\s*(.*)$', ln)
        if m: cur['assinaturas'].append(f'{m.group(1).strip()} {m.group(2) or ""}: {m.group(3).strip()}'.replace('  ', ' ')); continue
        m = re.match(r'^\s+- \*Fraqueza:\*\s*(.*)$', ln)
        if m: cur['fraqueza'] = m.group(1).strip(); continue
        if ln.startswith('## ') or ln.startswith('---'): cur = None
    return L


def classe_do_npc(v, L):
    if v.get('classe_livro') and sem_acento(v['classe_livro']).lower() in L: return L[sem_acento(v['classe_livro']).lower()]   # 438: a ligação gravada vale
    txt = sem_acento(str(v.get('classe', ''))).lower()
    cab = re.split(r'[(·,]', txt)[0].strip()
    if cab in L: return L[cab]
    p = cab.split(' ')   # a ficha diz "Cavaleira", "Assassina", "Maga de Elo"; o Livro diz no masculino
    for troca in ((r'eira$', 'eiro'), (r'ora$', 'or'), (r'a$', 'o'), (r'a$', ''), (r'esa$', 'es')):
        v1 = ' '.join([re.sub(troca[0], troca[1], p[0])] + p[1:]) if p and p[0] else cab
        if v1 in L: return L[v1]
    achados = [c for k, c in L.items() if re.search(r'\b' + re.escape(k) + r'\b', txt)]
    return max(achados, key=lambda c: len(c['nome'])) if achados else None


def mostra(c):
    print(f'{c["nome"]} ({c["familia"]}, {c["raridade"]})')
    for s in c['assinaturas']: print('  · ' + s)
    if c['fraqueza']: print('  FRAQUEZA: ' + c['fraqueza'])


def main():
    a = sys.argv[1:]
    if not a: print(__doc__); return
    L = livro(); N = carrega('npcs.json', {})
    if a[0] == 'livro':
        f = sem_acento(a[1]).lower() if len(a) > 1 else ''
        for c in L.values():
            if f in sem_acento(c['familia']).lower(): print(f'  {c["nome"]} ({c["familia"]}, {c["raridade"]}) · {len(c["assinaturas"])} assinaturas')
        print(f'{len(L)} classes no Livro')
    elif a[0] == 'ver' and len(a) > 1:
        c = L.get(sem_acento(' '.join(a[1:])).lower()) or sys.exit('classe fora do Livro (classe.py livro)')
        mostra(c)
    elif a[0] == 'npc' and len(a) > 1:
        alvo = sem_acento(a[1]).lower(); k = next((k for k in N if sem_acento(k).lower() == alvo), None) or sys.exit('NPC não achado')
        c = classe_do_npc(N[k], L)
        print(f'{k}: {N[k].get("classe")}'); mostra(c) if c else print('  (classe fora do Livro: gerar ou corrigir)')
    elif a[0] in ('migra', 'faltam'):
        ok, falta = 0, []
        for k, v in N.items():
            c = classe_do_npc(v, L)
            if not c: falta.append(f'{k} [{str(v.get("classe"))[:40]}]'); continue
            ok += 1
            if a[0] == 'migra':
                v['classe_livro'] = c['nome']; v['assinaturas'] = [s.split(':')[0].strip() for s in c['assinaturas']]; v['fraqueza'] = c['fraqueza']
        if a[0] == 'migra': grava('npcs.json', N)
        print(f'{a[0]}: {ok} de {len(N)} NPCs com classe do Livro · fora do Livro: {len(falta)}')
        if a[0] == 'faltam' or falta: print('  ' + ' · '.join(falta[:60]))
    elif a[0] in ('liga', 'gera') and len(a) > 1:
        from nucleo import anota, dia_atual
        alvo = sem_acento(a[1]).lower(); k = next((k for k in N if sem_acento(k).lower() == alvo), None) or sys.exit('NPC não achado')
        if a[0] == 'liga':
            c = L.get(sem_acento(a[2]).lower()) if len(a) > 2 else None
            if not c: sys.exit('classe fora do Livro (classe.py livro)')
            mot = a[3] if len(a) > 3 else 'o texto da ficha é sinônimo dela'
        else:
            import selo
            fams = []
            for x in L.values():
                if x['familia'] not in fams: fams.append(x['familia'])
            fam = a[2] if len(a) > 2 else None
            Z = selo.load()
            if not fam:
                sid = selo.declara(Z, '-', f'A FAMÍLIA DA CLASSE DE {k} (sem classe escrita)', f'd{len(fams)}', ' | '.join(f'{i + 1}: {f}' for i, f in enumerate(fams)), selo.opcoes(['oculto']), quieto=True)
                fam = fams[selo.rola(Z, sid, quieto=True)['rolagens'][-1]['total'] - 1]
            fam = next((f for f in fams if sem_acento(f).lower().startswith(sem_acento(fam).lower()[:4])), None) or sys.exit(f'família que não conheço: {fam} ({", ".join(fams)})')
            pool = [x for x in L.values() if x['familia'] == fam and x['raridade'] != 'Lendário']
            sid = selo.declara(Z, '-', f'A CLASSE DE {k} NA FAMÍLIA {fam} (sem as Lendárias)', f'd{len(pool)}', ' | '.join(f'{i + 1}: {x["nome"]}' for i, x in enumerate(pool)), selo.opcoes(['oculto']), quieto=True)
            c = pool[selo.rola(Z, sid, quieto=True)['rolagens'][-1]['total'] - 1]; mot = f'pelo dado (família {fam})'
        v = N[k]; v['classe_livro'] = c['nome']; v['assinaturas'] = [s_.split(':')[0].strip() for s_ in c['assinaturas']]; v['fraqueza'] = c['fraqueza']
        v.setdefault('log', []).append(f"Dia {dia_atual()}: classe do Livro: {c['nome']} ({c['familia']}, {c['raridade']}) · {mot}")
        grava('npcs.json', N); anota(f"- CLASSE (438, MOTOR 9.1) {k}: {c['nome']} ({c['familia']}, {c['raridade']}) · {mot}")
        print(f"{k}: {c['nome']} ({c['familia']}, {c['raridade']}) · {mot}")
    else: print(__doc__)


if __name__ == '__main__':
    main()
