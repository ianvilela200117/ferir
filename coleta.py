#!/usr/bin/env python3
"""coleta.py — MOTOR 9 (G35): OS OFÍCIOS DE COLETA, com grau que sobe pelo uso (Livro Nove 14).

Ofícios: mineracao · ervas · pesca · esfola · lenha. Graus (como as habilidades): 1 Iniciante (0 usos) · 2 Aprendiz (10)
· 3 Adepto (30) · 4 Perito (80) · 5 Mestre (200) · 6 Grão-Mestre (500).
Um dia de coleta: d20 + grau × 2 + ferramenta. Até 5 nada · 6-12 material Comum do lugar (1d6 kg) · 13-17 o MATERIAL do
lugar (1d6 kg) · 18-22 o dobro · 23+ o dobro e um ACHADO (1 kg um degrau acima, ou o lugar rende +2 por uma lua).
O grau limita a categoria que a mão colhe: 1-2 até Incomum · 3 Raro · 4 Épico · 5 Único · 6 qualquer.
1 natural: ACIDENTE (um ferido leve, ou o bicho do lugar aparece: o Mestre rola a cena).
ESFOLA: quem esfola um bicho morto soma 10% de despojo por grau acima do 1 (arredonda para baixo).
EQUIPE: gente da casa que colhe num lugar toda semana (50 por semana): uma rolagem por semana, o grau é o da equipe.

Uso:
  python3 coleta.py ver
  python3 coleta.py rola "QUEM" OFICIO "LUGAR" MATERIAL CATEGORIA [ferramenta=N] [comum=ferro]
  python3 coleta.py esfola "QUEM" QTD           diz quanto despojo a mais (e conta o uso)
  python3 coleta.py equipe "NOME" OFICIO "LUGAR" MATERIAL CATEGORIA [comum=ferro] [grau=N]
  python3 coleta.py semana DIA                  o tick semanal chama: as equipes colhem e o custo sai do cofre
"""
import subprocess, sys
from nucleo import d, carrega, grava, anota, P

ARQ = 'oficios.json'; MARCAS = [0, 10, 30, 80, 200, 500]; NOMES = ['Iniciante', 'Aprendiz', 'Adepto', 'Perito', 'Mestre', 'Grão-Mestre']
DEG = {'comum': 0, 'incomum': 1, 'raro': 2, 'epico': 3, 'unico': 4, 'lendario': 5, 'mitico': 6, 'primordial': 7}
TETO = {1: 1, 2: 1, 3: 2, 4: 3, 5: 4, 6: 7}
sem = lambda s: s.lower().replace('é', 'e').replace('ú', 'u').replace('í', 'i').replace('á', 'a').replace('ç', 'c').replace('ã', 'a')
grau = lambda u: max(i + 1 for i, m in enumerate(MARCAS) if u >= m)


def sh(*a):
    r = subprocess.run([sys.executable, P(a[0])] + [str(x) for x in a[1:]], capture_output=True, text=True)
    return (r.stdout.strip().split('\n') or [''])[-1]


def colhe(quem, usos, oficio, lugar, mat, cat, ferr, comum, dia=None):
    g = grau(usos); r = d(20); t = r + g * 2 + ferr; out = []
    if DEG[sem(cat)] > TETO[g]: mat_ok = False
    else: mat_ok = True
    base = f"COLETA (G35): {quem} ({oficio}, grau {g} {NOMES[g - 1]}) em {lugar}: d20 [{r}] + {g * 2}" + (f' + {ferr}' if ferr else '') + f' = {t} → '
    if r == 1: return base + 'ACIDENTE (1 natural): um ferido leve ou o bicho do lugar aparece; nada colhido', []
    if t <= 5: return base + 'nada', []
    kg = d(6)
    if t <= 12 or not mat_ok:
        out.append((comum, kg)); txt = f'{kg} kg de {comum} (Comum)' + ('' if mat_ok else f' · a mão ainda não colhe {cat} (grau {g})')
    else:
        if t >= 18: kg *= 2
        out.append((mat, kg)); txt = f'{kg} kg de {mat} ({cat})' + (' · e um ACHADO: 1 kg um degrau acima, ou o lugar rende +2 por uma lua (o Mestre escolhe pela cena)' if t >= 23 else '')
    return base + txt, out


def main():
    a = sys.argv[1:]; S = carrega(ARQ, {'gente': {}, 'equipes': []})
    if not a or a[0] == 'ver':
        if not a: print(__doc__)
        print('OFÍCIOS DE COLETA (G35)')
        for q, of in S['gente'].items(): print(f"  {q}: " + ' · '.join(f'{o} grau {grau(u)} ({u} usos)' for o, u in of.items()))
        for e in S['equipes']: print(f"  EQUIPE {e['nome']}: {e['oficio']} em {e['lugar']} ({e['material']}, {e['cat']}) · grau {grau(e['usos'])} ({e['usos']} usos) · 50 por semana")
        return
    op = {x.split('=')[0]: x.split('=', 1)[1] for x in a if '=' in x}
    if a[0] == 'rola' and len(a) >= 6:
        of = S['gente'].setdefault(a[1], {}); u = of.get(sem(a[2]), 0)
        txt, ganho = colhe(a[1], u, sem(a[2]), a[3], a[4], a[5], int(op.get('ferramenta', 0)), op.get('comum', 'ferro'))
        of[sem(a[2])] = u + 1; grava(ARQ, S)
        for m, kg in ganho: txt += ' · ' + sh('ficha.py', 'mat', m, f'+{kg}', f'coleta de {a[1]} em {a[3]}')[:60]
        if grau(u + 1) > grau(u): txt += f' · ★ {a[1]} sobe em {a[2]}: grau {grau(u + 1)} {NOMES[grau(u + 1) - 1]}'
        anota('- ' + txt); print(txt); return
    if a[0] == 'esfola' and len(a) >= 3:
        of = S['gente'].setdefault(a[1], {}); u = of.get('esfola', 0); g = grau(u); q = int(a[2]); extra = q * (g - 1) // 10
        of['esfola'] = u + 1; grava(ARQ, S)
        print(f'ESFOLA (G35): {a[1]}, grau {g} {NOMES[g - 1]}: de {q} partes, +{extra} (10% por grau acima do 1)' + (f' · ★ sobe: grau {grau(u + 1)}' if grau(u + 1) > g else '')); return
    if a[0] == 'equipe' and len(a) >= 6:
        S['equipes'].append({'nome': a[1], 'oficio': sem(a[2]), 'lugar': a[3], 'material': a[4], 'cat': a[5], 'comum': op.get('comum', 'ferro'), 'usos': MARCAS[int(op.get('grau', 1)) - 1]})
        grava(ARQ, S); t = f"EQUIPE DE COLETA (G35): {a[1]}: {a[2]} em {a[3]} ({a[4]}, {a[5]}); 50 por semana"; anota('- ' + t); print(t); return
    if a[0] == 'semana' and len(a) >= 2:
        out = []
        for e in S['equipes']:
            txt, ganho = colhe(e['nome'], e['usos'], e['oficio'], e['lugar'], e['material'], e['cat'], 0, e.get('comum', 'ferro'))
            e['usos'] += 1
            for m, kg in ganho: sh('ficha.py', 'mat', m, f'+{kg}', f"{a[1]}: a equipe {e['nome']}")
            out.append('  ' + txt.replace('COLETA (G35): ', ''))
        if S['equipes']:
            out.append('  ' + sh('ficha.py', 'cofre', f"-{50 * len(S['equipes'])}", f"{a[1]}: as equipes de coleta (G35)"))
            grava(ARQ, S); anota(f'- COLETA (semana do {a[1]}): ' + ' · '.join(x.strip() for x in out))
        print('\n'.join(out) if out else '  (nenhuma equipe de coleta)'); return
    sys.exit(__doc__)


if __name__ == '__main__':
    main()
