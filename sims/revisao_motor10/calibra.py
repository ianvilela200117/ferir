# Calibração do protótipo "o item vence o nível" (só simulador; nada gravado). Fichas montadas SEMPRE pela mesma conta, a do Livro (X.2 e o resumo 4092).
import sys, random, pathlib
RAIZ = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import luta, prototipo
luta10 = prototipo.monta()
CATS = ['Comum', 'Incomum', 'Raro', 'Épico', 'Único', 'Lendário', 'Mítico', 'Primordial']
MULT = [1, 1.5, 2.5, 5, 10, 25, 100, 500]; BON = [2, 4, 6, 10, 15, 20, 30, 50]; RD = [0, 1, 3, 6, 12, 25, 50, 100]; REQ = [1, 5, 20, 40, 70, 110, 180, 260]   # o requisito DA CASA (regras_da_casa_dia199.md, seção 2); o do Livro é 1/10/30/70/110/150/250/350

def rende(cat, nivel, regra):
    """a categoria que a peça rende na mão de quem a usa"""
    if regra == 'inteira' or nivel >= REQ[cat]: return cat
    return max(cat - 1, 0)   # o Livro: abaixo do requisito, UMA categoria abaixo

def ficha(nome, nivel, arma, arm, regra='livro'):
    a = rende(arma, nivel, regra); d = rende(arm, nivel, regra)
    chave = 85 + int(nivel * 0.4); vig = 70 + int(nivel * 0.2)             # atributo-chave e Vigor (base de NPC do Livro + parte dos pontos por nível)
    mae = 8 if nivel >= 150 else 6 if nivel >= 50 else 4                   # Luta: Treinado, Mestre, Lendário
    return dict(nome=nome, nivel=nivel, at=chave // 10 + mae + BON[a], df=10 + (chave - 20) // 10 + BON[d], rd=RD[d], pv=(vig // 10) * 10 + nivel * 2,
                dado='1d10', mult=MULT[a], b=chave // 10, arma_cat=a, arm_cat=d)

def duelo(L, a, b, n=3000):
    L.SIM = True; va = 0; rs = []
    for i in range(n):
        if i % 2 == 0: M, g, ag = dict(b, gente=True, moral=False), dict(a), True
        else:          M, g, ag = dict(a, gente=True, moral=False), dict(b), False
        r = L.luta({'monstro': M, 'grupo': [dict(g, heroi=True, fica=True)], 'ate': 80})
        if r['res'] in ('morto', 'grupo caiu'): va += (r['res'] == 'morto') == ag
        else: va += 0.5
        rs.append(r['rnd'])
    rs.sort(); return round(100 * va / n), rs[len(rs) // 2]

def muitos(L, um, cada, k, n=1200):
    L.SIM = True; v = 0; rs = []
    for i in range(n):
        r = L.luta({'monstro': dict(um, gente=True, moral=False), 'grupo': [dict(cada, nome=f'v{j}', fica=True) for j in range(k)], 'ate': 80})
        v += r['res'] == 'grupo caiu'; rs.append(r['rnd'])
    rs.sort(); return round(100 * v / n), rs[len(rs) // 2]

random.seed(10)
f60 = ficha('60', 60, 6, 6); print('fichas pela conta do Livro:')
for x in (ficha('nível 60 com Mítico (rende Lendário)', 60, 6, 6), ficha('nível 60 com Mítico INTEIRO', 60, 6, 6, 'inteira'), ficha('nível 90 com Mítico (rende Lendário)', 90, 6, 6),
          ficha('nível 275 com Comum', 275, 0, 0), ficha('nível 275 com Raro', 275, 2, 2), ficha('nível 275 com Épico', 275, 3, 3), ficha('nível 275 com Único', 275, 4, 4), ficha('nível 275 com Lendário', 275, 5, 5)):
    print(f"  {x['nome']:<38} ataque +{x['at']} · Defesa {x['df']} · RD {x['rd']} · PV {x['pv']} · 1d10 × {x['mult']:g} + {x['b']}")
print()
print(f"{'DUELO (vitória do PRIMEIRO)':<62}{'motor de hoje':>16}{'protótipo':>14}")
linhas = [
 ('nível 60 Mítico × nível 275 COMUM', ficha('a', 60, 6, 6), ficha('b', 275, 0, 0)),
 ('nível 60 Mítico × nível 275 RARO', ficha('a', 60, 6, 6), ficha('b', 275, 2, 2)),
 ('nível 60 Mítico × nível 275 ÉPICO', ficha('a', 60, 6, 6), ficha('b', 275, 3, 3)),
 ('nível 60 Mítico × nível 275 ÚNICO', ficha('a', 60, 6, 6), ficha('b', 275, 4, 4)),
 ('nível 60 Mítico × nível 275 LENDÁRIO', ficha('a', 60, 6, 6), ficha('b', 275, 5, 5)),
 ('nível 60 Mítico INTEIRO (sob medida) × nível 275 ÚNICO', ficha('a', 60, 6, 6, 'inteira'), ficha('b', 275, 4, 4)),
 ('nível 60 Mítico INTEIRO (sob medida) × nível 275 LENDÁRIO', ficha('a', 60, 6, 6, 'inteira'), ficha('b', 275, 5, 5)),
 ('IGUAIS NA ARMA (Épico): nível 70 × nível 80', ficha('a', 70, 3, 3), ficha('b', 80, 3, 3)),
 ('IGUAIS NA ARMA (Épico): nível 70 × nível 95', ficha('a', 70, 3, 3), ficha('b', 95, 3, 3)),
 ('IGUAIS NA ARMA (Épico): nível 70 × nível 120', ficha('a', 70, 3, 3), ficha('b', 120, 3, 3)),
 ('UMA categoria: nível 60 Único × nível 120 Épico', ficha('a', 60, 4, 4, 'inteira'), ficha('b', 120, 3, 3)),
 ('DUAS categorias: nível 60 Único × nível 120 Raro', ficha('a', 60, 4, 4, 'inteira'), ficha('b', 120, 2, 2)),
]
for nome, a, b in linhas:
    v1, r1 = duelo(luta, a, b); v2, r2 = duelo(luta10, a, b)
    print(f'{nome:<62}{v1:>9}% ({r1:>2} r){v2:>8}% ({r2:>2} r)')
print()
print(f"{'UM CONTRA A GUILDA (vitória do sozinho)':<62}{'motor de hoje':>16}{'protótipo':>14}")
for nome, um, cada in [('nível 90 Mítico × nível 275 RARO', ficha('u', 90, 6, 6), ficha('c', 275, 2, 2)),
                       ('nível 90 Mítico INTEIRO × nível 275 RARO', ficha('u', 90, 6, 6, 'inteira'), ficha('c', 275, 2, 2)),
                       ('nível 90 Mítico INTEIRO × nível 275 ÉPICO', ficha('u', 90, 6, 6, 'inteira'), ficha('c', 275, 3, 3))]:
    for k in (3, 10):
        v1, r1 = muitos(luta, um, cada, k); v2, r2 = muitos(luta10, um, cada, k)
        print(f'{nome + f" (contra {k})":<62}{v1:>9}% ({r1:>2} r){v2:>8}% ({r2:>2} r)')
