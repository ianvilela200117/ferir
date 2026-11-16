#!/usr/bin/env python3
"""edito.py — MOTOR 9 (G27): O CÓDIGO DE IREVIEL. Os 16 éditos do Livro Nove (10.2), com o teto e os efeitos.

O rei propõe, o conselho vota (conselho.py, pelo Mestre) e o édito entra AQUI. Teto: 2 + Legitimidade ÷ 3.
O script põe os modificadores nos pilares (reino.json), soma o custo na despesa fixa da semana (ficha.py fixo),
mexe em Legitimidade e prestígio, lança a reputação de quem tem ficha (reputacao.py) e escreve a lei no reino.
O que é ficção (uma novidade de mercado, um aprendiz por estação) fica na nota do édito para o Mestre cumprir.

Uso:
  python3 edito.py ver                          os 16, o teto e os que estão em vigor
  python3 edito.py decreta "NOME" [cidade=X] [fe="a fé"] [porcima]    porcima: o rei passou por cima do voto (Legitimidade −1)
  python3 edito.py revoga "NOME"
"""
import subprocess, sys
from nucleo import carrega, grava, anota, dia_atual, P

E = {
 'da Feira Franca': dict(cidade=True, mods=[('Comércio', 1)], custo=100, nota='uma novidade de mercado por lua na cidade; a portagem dela cai à metade (os 100 por semana)'),
 'do Grão Guardado': dict(custo=100, nota='celeiros: Comida +1 em toda cidade NO INVERNO e EM CERCO (o Mestre põe e tira o modificador nessas horas)'),
 'da Ronda': dict(mods=[('Ordem', 1)], custo=140, por_cidade=True, nota='ronda em toda cidade'),
 'do Ofício Livre': dict(rep=[('as guildas de ofício', -10)], nota='um pedido a mais por semana no Fundo dos Ofícios (P1)'),
 'da Caça Paga': dict(custo=200, nota='as guildas caçam os bichos do reino com +2 no dado delas (G12); o rei tem a primeira compra de todo núcleo'),
 'do Osso': dict(rep=[('a Mamiltia', -10), ('o Templo do Rio', -10)], nota='os servos do rei andam dentro da lei: a perda de reputação da G23 não acontece no reino; a Vigília manda um observador'),
 'da Mão Livre': dict(legit=1, rep=[('Ireviel (a cidade)', 10), ('Levis (a cidade)', 10), ('o Porto de Marasar (a cidade)', 10), ('Farenta (a cidade)', 10)], nota='acaba o trabalho forçado: PERDE o desconto das obras (G6); os forçados soltos escolhem ficar ou ir (dado)'),
 'do Sal': dict(capital=True, mods=[('Dinheiro', 1)], rep=[('os Do Junco (o Delta)', -10)], nota='o sal é do rei; um evento de contrabando por lua'),
 'do Chamado': dict(mods=[('Ordem', -1), ('Comida', -1)], nota='20 lanças novas por lua, sem pedir peça'),
 'do Colégio': dict(custo=150, rep=[('o campo', -5)], nota='um aprendiz de mago por estação entra na casa'),
 'da Moeda': dict(prestigio=1, nota='PEDE a oficina de cunho (obra de 2.000) e um mestre; o Dinheiro da capital não recua por evento de fora; moeda falsa é traição'),
 'do Físico': dict(mods=[('Saúde', 1)], custo=120, por_cidade=True, nota='os feridos da casa tratados nas casas de cura têm −3 no dado do ferimento'),
 'da Estrada': dict(custo=100, nota='viagem da casa dentro do reino um quarto mais rápida; menos assalto; o Comércio não avança por dado na lua em que entra'),
 'da Fé do Reino': dict(nota='a bênção da fé escolhida vale para a casa sem o voto pessoal; reputação −10 com TODAS as outras fés (o Mestre lança)'),
 'da Carta às Guildas': dict(nota='reputação +5 com as guildas que se registram; as que recusam viram hostis; aventureiro sem registro é preso (o Mestre lança pelo guildas.py)'),
 'do Juízo': dict(nota='um tribunal fixo: Legitimidade +1 por estação sem execução sumária; o rei não perdoa nem condena sozinho'),
}


def acha(nome):
    c = [k for k in E if k.lower() == nome.lower()] or [k for k in E if nome.lower().replace('édito ', '').strip() in k.lower()]
    if len(c) != 1: sys.exit(f'édito não achado (ou ambíguo): "{nome}" · ' + ', '.join(E))
    return c[0]


def sh(*a):
    r = subprocess.run([sys.executable, P(a[0])] + [str(x) for x in a[1:]], capture_output=True, text=True)
    return (r.stdout.strip().split('\n') or [''])[-1]


def teto(R): return 2 + R['reino'].get('legitimidade', 0) // 3 + R['reino'].get('editos_extra', 0)


def cidades_de(R, e, v):
    if e.get('cidade'): return [c for c in R['cidades'] if v.get('cidade', '').lower() in c['nome'].lower()]
    if e.get('capital'): return R['cidades'][:1]
    return R['cidades']


def main():
    a = sys.argv[1:]
    R = carrega('reino.json'); V = R['reino'].setdefault('editos', [])
    if not a or a[0] == 'ver':
        print(f"O CÓDIGO DE IREVIEL (G27) · em vigor {len(V)} de {teto(R)} (2 + Legitimidade {R['reino'].get('legitimidade')} ÷ 3)")
        for k, e in E.items():
            v = next((x for x in V if x['nome'] == k), None)
            custo = (f" · {e['custo']} por semana" + (' por cidade' if e.get('por_cidade') else '')) if e.get('custo') else ''
            mods = ' · ' + ', '.join(f'{p} {n:+d}' for p, n in e['mods']) if e.get('mods') else ''
            print(f"  {'✔' if v else '·'} Édito {k}" + (f" (desde o {v['dia']}" + (f", {v['cidade']}" if v.get('cidade') else '') + ')' if v else '') + mods + custo + f" · {e['nota']}")
        return
    if a[0] == 'decreta' and len(a) >= 2:
        k = acha(a[1]); e = E[k]; op = {x.split('=')[0]: x.split('=', 1)[1] for x in a[2:] if '=' in x}
        if any(x['nome'] == k for x in V): sys.exit(f'o Édito {k} já está em vigor.')
        if len(V) >= teto(R): sys.exit(f'TETO: {len(V)} éditos em vigor de {teto(R)}. Revogar um antes, ou subir a Legitimidade.')
        if e.get('cidade') and not op.get('cidade'): sys.exit('este édito vale NUMA cidade: diga cidade=NOME')
        v = {'nome': k, 'dia': dia_atual(), **({'cidade': op['cidade']} if op.get('cidade') else {}), **({'fe': op['fe']} if op.get('fe') else {})}
        cs = cidades_de(R, e, v)
        if e.get('cidade') and len(cs) != 1: sys.exit(f"cidade não achada: {op.get('cidade')}")
        for c in cs:
            for p, n in e.get('mods', []): c.setdefault('mods', {}).setdefault(p, []).append([n, f'Édito {k}'])
        custo = e.get('custo', 0) * (len(R['cidades']) if e.get('por_cidade') else 1); v['custo_semana'] = custo
        V.append(v); R['reino'].setdefault('leis', []).append(f"ÉDITO {k.upper()} ({v['dia']}" + (f"; {v['cidade']}" if v.get('cidade') else '') + f"): {e['nota']}")
        grava('reino.json', R); out = [f"ÉDITO {k.upper()} em vigor (Dia {v['dia']}): " + (', '.join(f'{p} {n:+d}' for p, n in e.get('mods', [])) + f" em {', '.join(c['nome'] for c in cs)}" if e.get('mods') else 'sem modificador de pilar')]
        if custo:
            F = carrega('ficha.json'); out.append(sh('ficha.py', 'fixo', 'despesa', F['livro']['despesa'] + custo, f'Édito {k}: +{custo} por semana'))
        if e.get('legit'): out.append(sh('reino.py', 'valor', 'legitimidade', e['legit'], f'Édito {k}'))
        if e.get('prestigio'): out.append(sh('reino.py', 'valor', 'prestigio', e['prestigio'], f'Édito {k}'))
        if 'porcima' in a: out.append(sh('reino.py', 'valor', 'legitimidade', -1, f'o rei passou por cima do voto do conselho (Édito {k})'))
        rep = carrega('mundo_vivo.json').get('reputacao', {})
        for quem, n in e.get('rep', []):
            out.append(sh('reputacao.py', 'muda', quem, f'{n:+d}', f'Édito {k}') if quem in rep else f'  REPUTAÇÃO a lançar pelo Mestre: {quem} {n:+d} (sem ficha de reputação com esse nome)')
        out.append(f"  o que o Mestre cumpre: {e['nota']}")
        anota('- ' + ' · '.join(x.strip() for x in out if x)); print('\n'.join(out)); return
    if a[0] == 'revoga' and len(a) >= 2:
        k = acha(a[1]); v = next((x for x in V if x['nome'] == k), None) or sys.exit(f'o Édito {k} não está em vigor.')
        e = E[k]
        for c in R['cidades']:
            for p, n in e.get('mods', []): c.get('mods', {}).get(p, [])[:] = [x for x in c.get('mods', {}).get(p, []) if x[1] != f'Édito {k}']
        V.remove(v); R['reino']['leis'] = [l for l in R['reino'].get('leis', []) if not l.startswith(f'ÉDITO {k.upper()} (')]
        grava('reino.json', R); out = [f'ÉDITO {k.upper()} REVOGADO (valia desde o {v["dia"]})']
        if v.get('custo_semana'):
            F = carrega('ficha.json'); out.append(sh('ficha.py', 'fixo', 'despesa', F['livro']['despesa'] - v['custo_semana'], f'Édito {k} revogado: −{v["custo_semana"]} por semana'))
        if dia_atual() - v['dia'] < 30: out.append(sh('reino.py', 'valor', 'legitimidade', -1, f'Édito {k} revogado antes de uma lua'))
        anota('- ' + ' · '.join(x.strip() for x in out if x)); print('\n'.join(out)); return
    sys.exit(__doc__)


if __name__ == '__main__':
    main()
