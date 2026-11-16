#!/usr/bin/env python3
"""artes.py — MOTOR 9 (G30): as ARTES DE ARMA e a AURA de cada um, pela arma e pelo nível.

A maestria de Luta de quem vive da arma e não a tem escrita vai pela faixa de nível (declarado no 438):
até 49 Treinado (1 técnica, até o 2º círculo) · 50 a 149 Mestre (2, até o 4º) · 150 ou mais Lendário (3, até o 6º);
+1 técnica a cada 50 níveis. Primeiro a escada da arma (2º, 4º, 6º), depois a da segunda arma, depois Auras.
A Arte que fere entra na ficha de combate como feitiço da peça: (1 + 2 × círculo)d6 com METADE do multiplicador
de foco da categoria que a arma RENDE, uma por rodada, 1x por cena, com o efeito que o luta.py roda.

Uso:
  python3 artes.py ver [NOME]            as Artes de quem tem ficha de combate
  python3 artes.py aplica [NOME]         escolhe e grava nas fichas (menos o rei: as dele o jogador escolhe); anota no envelope
  python3 artes.py lista ARMA NIVEL [mult=N]   as entradas prontas para um inimigo ou NPC sem ficha (espada lança maça machado arco punho)
"""
import json, re, sys
from nucleo import carrega, grava, anota

ESCADA = {
 'espada': [('FIO DUPLO', 2, {}), ('CORTE CORRIDO', 4, {'area': True}), ('CORTE DO HORIZONTE', 6, {'ignora_rd': 0.5})],
 'lança': [('PONTA QUE ESPERA', 2, {}), ('CHUVA DE PONTAS', 4, {'area': True}), ('LANÇA QUE NÃO DOBRA', 6, {'ignora_rd': 1.0})],
 'maça': [('QUEBRA-GUARDA', 2, {'efeito': 'quebra_guarda'}), ('TREMOR DE FERRO', 4, {'efeito': 'derruba', 'cd_efeito': 25, 'area': True}), ('BIGORNA', 6, {'efeito': 'dobra_se_caido'})],
 'machado': [('RACHAR', 2, {'efeito': 'sangra'}), ('RODA DE LÂMINA', 4, {'area': True}), ('DERRUBAR O TRONCO', 6, {'efeito': 'derruba', 'cd_efeito': 30})],
 'arco': [('TIRO DUPLO', 2, {}), ('FLECHA QUE PREGA', 4, {'efeito': 'derruba', 'cd_efeito': 25}), ('FLECHA QUE NÃO CAI', 6, {})],
 'punho': [('MÃO ABERTA', 2, {'efeito': 'derruba', 'cd_efeito': 20}), ('PASSO QUE SOME', 4, {}), ('GOLPE NO SOPRO', 6, {'efeito': 'derruba', 'cd_efeito': 35})],
}
CHAVES = [('espada', ('ESPADA', 'LÂMINA', 'SABRE', 'ADAGA', 'FACA', 'PUNHAL', 'ESTOQUE')), ('lança', ('LANÇA', 'ALABARDA', 'TRIDENTE', 'ARPÃO', 'PIQUE')),
          ('maça', ('MAÇA', 'MARTELO', 'MANGUAL')), ('machado', ('MACHADO',)), ('arco', ('ARCO', 'BESTA'))]
AURAS = ['Pele de Pedra', 'Raiz de Pedra menor', 'Passo de Vento', 'Instante', 'Fôlego de Ferro', 'Calma', 'Mão de Pedra', 'Sangue Quente', 'Luz no Escudo', 'Nó de Chamada']
FOCO = {'comum': 1, 'incomum': 1.25, 'rar': 1.5, 'épic': 2, 'únic': 3, 'lendári': 5, 'mític': 10, 'primordial': 20}
ARQ = 'fichas_combate.json'


def maestria(nv): return ('Treinado', 1, 2) if nv < 50 else ('Mestre', 2, 4) if nv < 150 else ('Lendário', 3, 6)


def armas_de(f):
    if f.get('arma'): return f['arma'] if isinstance(f['arma'], list) else [f['arma']]   # a arma dita na ficha vale
    txt = (f.get('pecas') or '').upper(); achou = []
    for pedaco in re.split(r' · ', txt):
        for fam, ks in CHAVES:
            if any(pedaco.strip().startswith(k) or f'{k} ' in pedaco.split('(')[0] for k in ks) and fam not in achou: achou.append(fam)
    return achou or ['punho']


def foco_de(f):
    txt = ' '.join(m.get('nome', '') for m in f.get('magias', []) if '(Arte de' not in m.get('nome', '')) + ' ' + (f.get('pecas') or '').split(' · ')[0]
    r = re.search(r'rende (\w+)', txt, re.I); alvo = (r.group(1) if r else txt).lower()
    for k in ('primordial', 'mític', 'lendári', 'únic', 'épic', 'rar', 'incomum', 'comum'):
        if k in alvo: return FOCO[k]
    return 1


def escolhe(nv, armas):
    nome, base, teto = maestria(nv); n = base + nv // 50; lista = []
    for fam in armas:
        for a in ESCADA[fam]:
            if a[1] <= teto and len(lista) < n: lista.append((fam, a))
    auras = AURAS[:max(0, n - len(lista))]
    return nome, teto, lista, auras


def entradas(lista, mult, rodada0):
    ordem = sorted(lista, key=lambda x: (0 if x[1][2].get('efeito') == 'derruba' else 1, -x[1][1]))   # o que derruba vem antes do que dobra no caído
    out = []
    for i, (fam, (nome, circ, ex)) in enumerate(ordem):
        e = {'nome': f'{nome} (Arte de {fam}, {circ}º; G30: metade do multiplicador da arma, ×{mult:g}; 1x por cena)', 'dano': f'{1 + 2 * circ}d6', 'mult': mult, 'cd': 30, 'rodada': [rodada0 + i]}
        e.update(ex); out.append(e)
    return out


def aplica(F, nome):
    f = F['fichas'][nome]; nv = f.get('nivel_ref', f.get('nivel', 20))
    try:
        N = carrega('npcs.json', {}); nv = max(nv, (N.get(nome) or {}).get('nivel') or 0)
    except Exception: pass
    if f.get('sem_arte'):   # quem não luta com arma (a Mamiltia: fé e magia)
        f['magias'] = [m for m in f.get('magias', []) if '(Arte de' not in m.get('nome', '')]; f.pop('artes', None)
        f['pecas'] = (f.get('pecas') or '').split(' · ARTES DE ARMA')[0]
        return f'{nome}: não luta com arma (sem Arte)'
    armas = armas_de(f); mst, teto, lista, auras = escolhe(nv, armas); mult = max(1, foco_de(f) / 2)
    velhas = [m for m in f.get('magias', []) if '(Arte de' not in m.get('nome', '')]
    usadas = [r for m in velhas for r in (m['rodada'] if isinstance(m.get('rodada'), list) else [m.get('rodada')]) if isinstance(r, int) and r < 15]
    r0 = (max(usadas) + 1) if usadas else 1
    f['magias'] = velhas + entradas(lista, mult, r0)
    f['artes'] = {'maestria': mst, 'teto': teto, 'artes': [a[1][0].title() for a in lista], 'auras': auras, 'mult': mult}
    base = re.sub(r' · ARTES DE ARMA \(G30[^·]*(?: · [^·]*?(?=$))?', '', f.get('pecas') or '').split(' · ARTES DE ARMA')[0]
    f['pecas'] = base + f" · ARTES DE ARMA (G30): {', '.join(a[1][0].title() for a in lista) or 'nenhuma'}; auras: {', '.join(auras) or 'nenhuma'}"
    return f"{nome} ({nv}, Luta {mst}): {', '.join(a[1][0].title() + ' ' + str(a[1][1]) + 'º' for a in lista) or 'sem Arte'}" + (f" · auras: {', '.join(auras)}" if auras else '') + f' · ×{mult:g}'


def main():
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    if a[0] == 'lista' and len(a) >= 3:
        mult = float(next((x[5:] for x in a if x.startswith('mult=')), 1)); nv = int(a[2])
        mst, teto, lista, auras = escolhe(nv, [a[1]])
        print(f'Luta {mst}, até o {teto}º · auras: {", ".join(auras) or "nenhuma"}'); print(json.dumps(entradas(lista, mult, 1), ensure_ascii=False, indent=1)); return
    F = carrega(ARQ)
    nomes = [n for n in F['fichas'] if (len(a) < 2 or n.lower() == a[1].lower())]
    if a[0] == 'ver':
        for n in nomes:
            ar = F['fichas'][n].get('artes'); print(f"{n}: " + (f"Luta {ar['maestria']} · {', '.join(ar['artes']) or 'sem Arte'} · auras: {', '.join(ar['auras']) or 'nenhuma'}" if ar else 'sem Artes escolhidas'))
        return
    if a[0] == 'aplica':
        linhas = []
        for n in nomes:
            if n == 'Ferir' and len(a) < 2: print('Ferir: as Artes do rei o jogador escolhe (artes.py aplica Ferir, depois da palavra dele)'); continue
            if F['fichas'][n].get('servo') or not (F['fichas'][n].get('pecas') or '').strip(): 
                if F['fichas'][n].get('servo'): print(f'{n}: servo, luta com o corpo (sem Arte)'); continue
            l = aplica(F, n); linhas.append(l); print(l)
        grava(ARQ, F)
        if linhas: anota('- ARTES DE ARMA (G30; artes.py): ' + ' | '.join(linhas))
        return
    sys.exit(__doc__)


if __name__ == '__main__':
    main()
