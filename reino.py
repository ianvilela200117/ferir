#!/usr/bin/env python3
"""reino.py — gerenciamento das cidades e do reino (Dia 290).

Uso:
  python3 reino.py estado                      o painel do reino e das cidades
  python3 reino.py semana N                    o tick do reino (rodar junto do tick semanal)
  python3 reino.py projeto CIDADE "NOME" CUSTO DIAS "EFEITO"   começa uma obra pública
  python3 reino.py mod CIDADE PILAR VALOR "MOTIVO"             modificador fixo num pilar (VALOR 0 apaga)
  python3 reino.py pilar CIDADE PILAR NIVEL "MOTIVO"           muda um pilar à mão (a ficção mandou)
  python3 reino.py rel "QUEM" DELTA "MOTIVO"                   muda uma relação do reino (−5 a +5)
  python3 reino.py valor CAMPO DELTA "MOTIVO"                  prestigio ou legitimidade (0 a 10)

Regras (declaradas no envelope do Dia 290):
  PILARES (6 por cidade: Comida, Comércio, Dinheiro, Saúde, Ordem, Defesa; 0 a 4):
    d6 + modificadores: 5 ou mais AVANÇA 1 · 1 natural RECUA 1 e traz um PROBLEMA (d6) · o resto fica.
  EVENTO DA CIDADE, d20 por cidade por semana (tabela EVENTOS).
  RELAÇÕES, d20 por vizinho: 1-4 piora 1 · 5-16 fica · 17-20 melhora 1 (o humor do mundo; a ficção manda mais).
  RENDA da cidade nova (Ireviel segue no livro da casa): base + 150 × Comércio + 100 × Dinheiro − custo.
  OBRAS PÚBLICAS: custam ouro na hora e ficam prontas em N dias; o efeito entra quando ficam prontas.

MOTOR 6 (Dia 379):
  · a semana roda DENTRO do tick semanal (tick.py); rodar de novo o mesmo dia é recusado (não rola duas vezes)
  · dado verdadeiro (secrets), como o resto do motor (antes era o gerador comum do Python)
  · modificador com prazo escrito no motivo ("até o 381") VENCE SOZINHO depois do dia (antes ficava somando para sempre)
  · SOCORRO DE COMIDA: cidade fora da capital que começa a semana com Comida abaixo de 2 custa 400 (regra do 332), já descontado
  · EQUILÍBRIO (Dia 379, escolha do jogador): o 1 natural só gera PROBLEMA em pilar 2 ou menos; pilar em 3 ou 4 só recua (eram 4 problemas por semana no reino)
  · LEGITIMIDADE E PRESTÍGIO como moeda (6.3): python3 reino.py legit +N|-N "motivo" · python3 reino.py prest +N|-N "motivo"
    Guia: passar por cima de um voto do conselho −1 · julgamento justo em praça +1 · quebrar a própria lei −2 · vitória grande ou obra pública +1 de prestígio.
    Legitimidade 5 ou menos: Ordem −1 na capital toda semana · 3 ou menos: Ordem −1 em todas as cidades.
  · o dia do reino vem do relógio do jogo (estado.json): a obra pública não nasce mais com data velha
"""
import json, os, re, secrets, sys
try:
    from nucleo import dia_atual
except ImportError:
    dia_atual = lambda: 0
RES = os.environ.get('MOTOR_RESUMO') == '1'   # o tick pede as linhas de resumo
SOCORRO = 400


def resumo(txt):
    if RES:
        print('::R:: ' + txt)

AQUI = os.path.dirname(os.path.abspath(__file__))
ARQ = os.path.join(AQUI, 'reino.json')
PILARES = ['Comida', 'Comércio', 'Dinheiro', 'Saúde', 'Ordem', 'Defesa']
PROBLEMAS = {1: 'fome', 2: 'furto ou roubo grande', 3: 'briga ou motim', 4: 'surto de doença',
             5: 'fuga de comerciante ou de gente', 6: 'SURPRESA (gerador novidade)'}
EVENTOS = {1: 'DESASTRE (incêndio, enchente ou desabamento)', 2: 'CRIME GRANDE (alguém importante roubado ou morto)',
           3: 'GREVE ou briga de ofícios', 4: 'DOENÇA numa rua', 5: 'FOME LOCAL (um carregamento não veio)',
           15: 'IMIGRANTES chegam (gente nova, braços e bocas)', 16: 'FESTA ou FEIRA (Comércio +1 na próxima rolagem)',
           17: 'ACHADO (ouro, material ou ruína debaixo da cidade)', 18: 'UM TALENTO aparece (gerador npc)',
           19: 'UMA PETIÇÃO AO REI (o povo pede uma coisa)', 20: 'SURPRESA (gerador novidade)'}


def d(n):
    return secrets.randbelow(n) + 1


def load():
    with open(ARQ, encoding='utf-8') as f:
        return json.load(f)


def save(R):
    tmp = ARQ + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(R, f, ensure_ascii=False, indent=1)
    os.replace(tmp, ARQ)


def vence_mods(c, dia):
    """tira os modificadores cujo motivo traz prazo ("até o N") já passado; devolve as linhas do que venceu"""
    out = []
    for p, lst in c.get('mods', {}).items():
        for v, motivo in list(lst):
            m = re.search(r'até o (\d+)', motivo)
            if m and dia > int(m.group(1)):
                lst.remove([v, motivo])
                out.append(f"{p} {v:+d} VENCEU ({motivo})")
    return out


def cidade(R, nome):
    for c in R['cidades']:
        if c['nome'].lower().startswith(nome.lower()) or nome.lower() in c['nome'].lower():
            return c
    sys.exit(f'cidade não achada: {nome}')


def barra(n):
    return '■' * n + '□' * (4 - n)


def estado(R):
    r = R['reino']
    print(f"{r['nome'].upper()} · {('rei: ' + r['rei']) if r.get('rei') else 'sem coroa ainda'} · "
          f"prestígio {r['prestigio']}/10 · legitimidade {r['legitimidade']}/10")
    if r.get('conselho_real'):
        print('  CONSELHO REAL: ' + ' · '.join(f"{k}: {v}" for k, v in r['conselho_real'].items()))
    print('  RELAÇÕES: ' + ' · '.join(f"{k} {v:+d}" for k, v in r['relacoes'].items()))
    if r.get('leis'):
        print('  LEIS: ' + ' · '.join(r['leis']))
    for c in R['cidades']:
        mods = c.get('mods', {})
        print(f"\n  {c['nome']} ({c['tipo']}) · gente ~" + f"{c['gente']:,}".replace(',', '.'))
        for p in PILARES:
            m = sum(v for v, _ in mods.get(p, []))
            print(f"    {p:9} {barra(c['pilares'][p])} {c['pilares'][p]}/4" + (f"  (mod {m:+d})" if m else ''))
        if c.get('renda'):
            rr = c['renda']
            print(f"    renda: base {rr['base']} + 150×Comércio + 100×Dinheiro − custo {rr['custo']}"
                  if not rr.get('no_livro') else '    renda: no LIVRO DA CASA (o cofre)')
        for o in c.get('obras', []):
            print(f"    OBRA: {o['nome']} · pronta no dia {o['pronta']} · {o['efeito']}")


def semana(R, dia):
    r = R['reino']
    if r.get('ultima_semana') == dia:
        print(f"O REINO — a semana do Dia {dia} JÁ FOI ROLADA (não se rola duas vezes). Painel: reino.py estado")
        return False
    print(f"O REINO — semana (Dia {dia}) · {r['nome']}")
    total = 0
    if r.get('legitimidade', 10) <= 5:
        for c in R['cidades']:
            if r['legitimidade'] <= 3 or c is R['cidades'][0]:
                c.setdefault('mods', {}).setdefault('Ordem', []).append([-1, f"legitimidade do rei em {r['legitimidade']}/10 (até o {dia + 6})"])
        print(f"  LEGITIMIDADE {r['legitimidade']}/10: Ordem −1 " + ('em todas as cidades' if r['legitimidade'] <= 3 else 'na capital') + ' nesta semana')
        resumo(f"legitimidade {r['legitimidade']}/10 pesa na Ordem")
    for c in R['cidades']:
        print(f"  {c['nome'].upper()}:")
        nota = []
        for l in vence_mods(c, dia):
            print('    MODIFICADOR ' + l)
            nota.append(l.split(' (')[0])
        mods = c.get('mods', {})
        rr = c.get('renda')
        fome = bool(rr and not rr.get('no_livro') and c['pilares']['Comida'] < 2)
        for p in PILARES:
            m = sum(v for v, _ in mods.get(p, []))
            x = d(6)
            antes = c['pilares'][p]
            if x == 1 and antes >= 3:   # Dia 379 (equilíbrio, escolha 6b do jogador): pilar firme só recua; o PROBLEMA nasce em pilar 2 ou menos
                c['pilares'][p] = antes - 1
                res = f"1 NATURAL → RECUA {antes}/4 → {c['pilares'][p]}/4 (sem problema: o pilar estava firme)"
                nota.append(f"{p} {antes}→{c['pilares'][p]} (1 natural)")
            elif x == 1:
                c['pilares'][p] = max(0, antes - 1)
                pr = d(6)
                res = f"1 NATURAL → RECUA {antes}/4 → {c['pilares'][p]}/4 + PROBLEMA [{pr}] {PROBLEMAS[pr]}"
                nota.append(f"{p} {antes}→{c['pilares'][p]} (1 natural; PROBLEMA: {PROBLEMAS[pr]})")
            elif x + m >= 5:
                c['pilares'][p] = min(4, antes + 1)
                res = f"AVANÇA {antes}/4 → {c['pilares'][p]}/4" if antes < 4 else 'fica 4/4 (cheio)'
                if antes < 4:
                    nota.append(f"{p} {antes}→{c['pilares'][p]}")
            else:
                res = f"fica {antes}/4"
            print(f"    {p:9} d6 [{x}]{m:+d} = {x + m} → {res}")
        e = d(20)
        print(f"    EVENTO d20 [{e}] → {EVENTOS.get(e, 'nada de especial')}")
        if e in EVENTOS:
            nota.append('EVENTO: ' + EVENTOS[e])
        for o in list(c.get('obras', [])):
            if dia >= o['pronta']:
                curto = c['nome'].split()[-1]
                print(f"    OBRA PRONTA: {o['nome']} → {o['efeito']}  (aplicar: python3 reino.py mod {curto} PILAR VALOR \"obra: {o['nome']}\"  ou  reino.py pilar ...)")
                nota.append(f"OBRA PRONTA: {o['nome']} → {o['efeito']} (aplicar com reino.py mod/pilar)")
                c.setdefault('obras_feitas', []).append(o)
                c['obras'].remove(o)
        if rr and not rr.get('no_livro'):
            v = rr['base'] + 150 * c['pilares']['Comércio'] + 100 * c['pilares']['Dinheiro'] - rr['custo']
            total += v
            print(f"    RENDA: {rr['base']} + 150×{c['pilares']['Comércio']} + 100×{c['pilares']['Dinheiro']} − {rr['custo']} = {v:+d}")
            if fome:
                total -= SOCORRO
                print(f"    SOCORRO DE COMIDA: −{SOCORRO} (começou a semana com Comida abaixo de 2; regra do 332)")
                nota.append(f'socorro de comida −{SOCORRO}')
        baixos = [f"{p} {c['pilares'][p]}/4" for p in PILARES if c['pilares'][p] <= 1]
        if baixos:
            nota.append('EM PERIGO: ' + ', '.join(baixos))
        resumo(f"{c['nome']}: " + (' · '.join(nota) if nota else 'sem mudança'))
        c.setdefault('log', []).append(f"{dia}: " + ' · '.join(f"{p} {c['pilares'][p]}" for p in PILARES) + f" · evento [{e}]")
        c['log'] = c['log'][-40:]
    print('  RELAÇÕES DO REINO:')
    mud = []
    for k in r['relacoes']:
        x = d(20)
        antes = r['relacoes'][k]
        if x <= 4:
            r['relacoes'][k] = max(-5, antes - 1); res = f"PIORA {antes:+d} → {r['relacoes'][k]:+d}"
        elif x >= 17:
            r['relacoes'][k] = min(5, antes + 1); res = f"MELHORA {antes:+d} → {r['relacoes'][k]:+d}"
        else:
            res = f"fica {antes:+d}"
        if r['relacoes'][k] != antes:
            mud.append(f"{k} {antes:+d}→{r['relacoes'][k]:+d}")
        print(f"    {k}: d20 [{x}] → {res}")
    resumo('relações: ' + (' · '.join(mud) if mud else 'sem mudança'))
    print(f"  RENDA DAS CIDADES FORA DO LIVRO: {total:+d} (o tick lança no cofre: ficha.py semana)")
    r.setdefault('log', []).append(f"{dia}: semana do reino; renda de fora do livro {total:+d}")
    r['log'] = r['log'][-80:]
    r['ultima_semana'] = dia
    r['dia'] = dia
    return True


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__); return
    R = load()
    if a[0] == 'estado':
        estado(R); return
    if a[0] in ('legit', 'prest') and len(a) > 1:
        k = 'legitimidade' if a[0] == 'legit' else 'prestigio'; antes = R['reino'][k]
        R['reino'][k] = max(0, min(10, antes + int(a[1].replace('+', ''))))
        R['reino'].setdefault('log', []).append(f"{dia_atual()}: {k} {antes} → {R['reino'][k]} ({a[2] if len(a) > 2 else ''})")
        save(R); print(f"{k.upper()}: {antes}/10 → {R['reino'][k]}/10" + (f' ({a[2]})' if len(a) > 2 else ''))
        try:
            from nucleo import anota
            anota(f"- REINO [Dia {dia_atual()}]: {k} {antes} → {R['reino'][k]}" + (f' ({a[2]})' if len(a) > 2 else ''))
        except ImportError: pass
        return
    if a[0] == 'semana':
        if not semana(R, int(a[1])):
            return
    elif a[0] == 'projeto':
        c = cidade(R, a[1]); dias = int(a[4])
        hoje = dia_atual() or R['reino'].get('dia', 0)
        c.setdefault('obras', []).append({'nome': a[2], 'custo': int(a[3]), 'pronta': hoje + dias, 'efeito': a[5]})
        print(f"OBRA começada em {c['nome']}: {a[2]} · custo {a[3]} · pronta no dia {hoje + dias} · {a[5]}")
    elif a[0] == 'mod':
        c = cidade(R, a[1]); p = a[2]; v = int(a[3])
        lst = c.setdefault('mods', {}).setdefault(p, [])
        lst[:] = [x for x in lst if x[1] != a[4]]
        if v: lst.append([v, a[4]])
        print(f"{c['nome']} · {p}: modificador {v:+d} ({a[4]})")
    elif a[0] == 'pilar':
        c = cidade(R, a[1]); c['pilares'][a[2]] = max(0, min(4, int(a[3])))
        c.setdefault('log', []).append(f"pilar {a[2]} → {a[3]} ({a[4]})")
        print(f"{c['nome']} · {a[2]} → {a[3]}/4 ({a[4]})")
    elif a[0] == 'rel':
        r = R['reino']['relacoes']; r[a[1]] = max(-5, min(5, r.get(a[1], 0) + int(a[2])))
        print(f"relação com {a[1]}: {r[a[1]]:+d} ({a[3]})")
    elif a[0] == 'valor':
        r = R['reino']; r[a[1]] = max(0, min(10, r[a[1]] + int(a[2])))
        print(f"{a[1]}: {r[a[1]]}/10 ({a[3]})")
    elif a[0] == 'dia':
        R['reino']['dia'] = int(a[1]); print('dia do reino:', a[1])
    save(R)


if __name__ == '__main__':
    main()
