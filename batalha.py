#!/usr/bin/env python3
"""batalha.py — BATALHA DE EXÉRCITOS (MOTOR 6.4; regra nova). Hoste contra hoste, uma rodada por hora de luta.
Cada batalha é um arquivo em batalhas/NOME.json com o terreno e os dois lados (comando, unidades e heróis).

FORÇA de uma unidade = homens × QUALIDADE (1 recruta · 2 milícia · 3 soldado · 4 veterano · 5 guarda de elite · 6 lenda) × o tipo no terreno:
   infantaria ×1 · arqueiros ×1,5 atrás de muralha ou em navio, ×1 no resto · cavalaria ×1,5 em campo, ×0,5 em rua ou muralha · magos ×2 · navio ×1 (só luta na água)
HERÓI: vale (nível ÷ 10)² homens de qualidade 3. Um nível 230 pesa como 529 soldados; o grande atravessa a fila, como na luta.
DEFENSOR: atrás de MURALHA, força ×2 · atrás de RIO ou em rua estreita, ×1,5.
CADA RODADA: os dois comandantes rolam 2d20 + comando. Cada lado perde 8% dos homens × raiz(força do outro ÷ a sua),
   mais ou menos 2,5% por ponto de diferença no dado (quem rola melhor perde menos e tira mais), entre 2% e 25%.
MORAL: o lado que perdeu mais de 15% na rodada, ou que está abaixo da metade dos homens do começo, testa cada unidade: d6 acima da moral, a unidade QUEBRA e foge
   (metade some: mortos, presos, desertores). HERÓI do lado que perdeu a rodada: d20 = 1, sai FERIDO (feridos.py).
FIM: um lado sem unidades (derrota), ou 12 rodadas (a noite separa).
Uso:
  python3 batalha.py modelo                 escreve batalhas/modelo.json para copiar
  python3 batalha.py NOME                   a batalha de verdade (dado verdadeiro; grava no envelope)
  python3 batalha.py NOME sim=2000          a régua (sem valor de jogo; não mostrar ao jogador sem a Visão do Tempo)
"""
import sys, os, json, secrets, random, copy
from nucleo import P, anota, dia_atual
SIM = False
def d(n): return random.randint(1, n) if SIM else secrets.randbelow(n) + 1
TIPO = {'infantaria': {}, 'arqueiros': {'muralha': 1.5, 'navio': 1.5}, 'cavalaria': {'campo': 1.5, 'rua': 0.5, 'muralha': 0.5}, 'magos': {'*': 2.0}, 'navio': {}}


def forca(lado, terreno, defende):
    f = 0
    for u in lado['unidades']:
        m = TIPO.get(u.get('tipo', 'infantaria'), {})
        f += u['homens'] * u['qualidade'] * m.get(terreno, m.get('*', 1.0))
    f += sum((h['nivel'] / 10) ** 2 * 3 for h in lado.get('herois', []) if not h.get('fora'))
    if defende: f *= 2.0 if terreno == 'muralha' else 1.5 if terreno in ('rio', 'rua') else 1.0
    return max(f, 1)


def homens(lado): return sum(u['homens'] for u in lado['unidades'])


def batalha(B, falar=True):
    B = copy.deepcopy(B); A_, B_ = B['lados']['A'], B['lados']['B']; ini = {k: homens(v) for k, v in B['lados'].items()}; L = []; fer = []
    for rod in range(1, 13):
        fa, fb = forca(A_, B['terreno'], A_.get('defende')), forca(B_, B['terreno'], B_.get('defende'))
        ra, rb = d(20) + d(20) + A_.get('comando', 0) + (A_.get('surpresa', 0) if rod == 1 else 0), d(20) + d(20) + B_.get('comando', 0) + (B_.get('surpresa', 0) if rod == 1 else 0); D = ra - rb   # 400: 'surpresa' = bônus de comando só na 1ª rodada (emboscada)
        pa = max(0.02, min(0.25, 0.08 * (fb / fa) ** 0.5 * (1 - D / 40))); pb = max(0.02, min(0.25, 0.08 * (fa / fb) ** 0.5 * (1 + D / 40)))
        txt = f"rodada {rod}: {A_['nome']} [{ra}] × {B_['nome']} [{rb}] · força {fa:.0f} × {fb:.0f}"
        for lado, p in ((A_, pa), (B_, pb)):
            antes = homens(lado)
            for u in lado['unidades']: u['homens'] = max(0, int(round(u['homens'] * (1 - p))))
            txt += f" · {lado['nome']} perde {antes - homens(lado)} ({100 * p:.0f}%)"
        for k, lado, p, perdeu in (('A', A_, pa, D < 0), ('B', B_, pb, D > 0)):
            if p > 0.15 or homens(lado) < ini[k] / 2:
                for u in list(lado['unidades']):
                    r = d(6)
                    if r > u.get('moral', 3):
                        txt += f" · {u['nome']} QUEBRA (d6 [{r}] contra moral {u.get('moral', 3)})"; lado['unidades'].remove(u)
            if perdeu:
                for h in lado.get('herois', []):
                    if not h.get('fora') and d(20) == 1: h['fora'] = True; fer.append(h['nome']); txt += f" · {h['nome']} sai FERIDO"
            lado['unidades'] = [u for u in lado['unidades'] if u['homens'] > 0]
        L.append(txt)
        if not A_['unidades'] or not B_['unidades']: break
    venc = 'A' if not B_['unidades'] and A_['unidades'] else 'B' if not A_['unidades'] and B_['unidades'] else None
    res = {'vencedor': venc, 'rodadas': rod, 'resta': {k: homens(v) for k, v in B['lados'].items()}, 'ini': ini, 'feridos': fer, 'linhas': L}
    return res


def main():
    global SIM
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    if a[0] == 'modelo' and len(a) == 1:
        M = {'nome': 'modelo: copie e troque', 'terreno': 'campo', 'nota': 'terreno: campo, muralha, rio, rua, navio. "defende": true dá o bônus do terreno a esse lado.',
             'lados': {'A': {'nome': 'a hoste do rei', 'comando': 9, 'unidades': [{'nome': 'os lanceiros de Ireviel', 'homens': 300, 'qualidade': 3, 'moral': 4, 'tipo': 'infantaria'}, {'nome': 'os arqueiros do Graur', 'homens': 80, 'qualidade': 3, 'moral': 3, 'tipo': 'arqueiros'}], 'herois': [{'nome': 'Eliane', 'nivel': 94}]},
                       'B': {'nome': 'as casas da Liga', 'comando': 6, 'defende': True, 'unidades': [{'nome': 'a guarda das casas', 'homens': 250, 'qualidade': 3, 'moral': 3, 'tipo': 'infantaria'}, {'nome': 'os mercenários do norte', 'homens': 120, 'qualidade': 4, 'moral': 2, 'tipo': 'infantaria'}], 'herois': []}}}
        json.dump(M, open(P('batalhas', 'modelo.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1); print('escrito: batalhas/modelo.json (os números do modelo são só exemplo; ponha os da ficção)'); return
    f = P('batalhas', a[0] if a[0].endswith('.json') else a[0] + '.json')
    if not os.path.exists(f): sys.exit(f'não achei {f} (python3 batalha.py modelo)')
    B = json.load(open(f, encoding='utf-8')); n = next((int(x[4:]) for x in a[1:] if x.startswith('sim=')), 0)
    if n:
        SIM = True; va = vb = 0; ra = []; rb = []; fer = {}
        for _ in range(n):
            r = batalha(B); va += r['vencedor'] == 'A'; vb += r['vencedor'] == 'B'; ra.append(r['resta']['A'] / r['ini']['A']); rb.append(r['resta']['B'] / r['ini']['B'])
            for x in r['feridos']: fer[x] = fer.get(x, 0) + 1
        ra.sort(); rb.sort(); A_, B_ = B['lados']['A']['nome'], B['lados']['B']['nome']
        print(f"RÉGUA de {n} batalhas (sem valor de jogo): {A_} vence {100 * va / n:.0f}% · {B_} vence {100 * vb / n:.0f}% · a noite separa {100 * (n - va - vb) / n:.0f}%")
        print(f"  {A_} sai com {100 * ra[n // 2]:.0f}% dos homens (de {100 * ra[n // 10]:.0f}% a {100 * ra[9 * n // 10]:.0f}%) · {B_} com {100 * rb[n // 2]:.0f}% (de {100 * rb[n // 10]:.0f}% a {100 * rb[9 * n // 10]:.0f}%)")
        if fer: print('  herói ferido: ' + ' · '.join(f'{k} {100 * v / n:.0f}%' for k, v in fer.items()))
        return
    r = batalha(B); print(f"BATALHA: {B['nome']} ({B['terreno']})")
    for l in r['linhas']: print('  ' + l)
    v = r['vencedor']; fim = f"VENCE {B['lados'][v]['nome']}" if v else 'A NOITE SEPARA os dois lados'
    print(f"  FIM em {r['rodadas']} rodadas: {fim} · restam " + ' · '.join(f"{B['lados'][k]['nome']} {r['resta'][k]} de {r['ini'][k]}" for k in 'AB') + (f" · feridos: {', '.join(r['feridos'])} (python3 feridos.py rola NOME)" if r['feridos'] else ''))
    anota(f"- BATALHA [Dia {dia_atual()}] {B['nome']}: " + ' ‖ '.join(r['linhas']) + f" ‖ {fim}")


if __name__ == '__main__':
    main()
