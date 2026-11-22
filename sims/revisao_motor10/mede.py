# Medição para a revisão do motor: quanto pesa o NÍVEL e quanto pesa o EQUIPAMENTO no luta.py de hoje.
# Só simulador (luta.SIM=True): nada é gravado, nada tem valor de jogo.
import sys, random, pathlib
RAIZ = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
import luta
luta.SIM = True
random.seed(507)
N = 4000

def duelo(a, b, n=N):
    """a e b são fichas de gente; devolve % de vitória de a, duração mediana. Alterna quem é 'monstro' para tirar o viés do papel."""
    va = 0; rs = []
    for i in range(n):
        if i % 2 == 0: M, g, a_e_grupo = dict(b, gente=True, moral=False), dict(a), True
        else:          M, g, a_e_grupo = dict(a, gente=True, moral=False), dict(b), False
        r = luta.luta({'monstro': M, 'grupo': [dict(g, heroi=True)], 'ate': 60})
        grupo_venceu = r['res'] == 'morto'
        if grupo_venceu == a_e_grupo and r['res'] in ('morto', 'grupo caiu'): va += 1
        elif r['res'] not in ('morto', 'grupo caiu'): va += 0.5   # empate ou recuo: meio a meio
        rs.append(r['rnd'])
    rs.sort()
    return round(100 * va / n), rs[len(rs) // 2]

def ficha(nome, nivel, at, df, rd, pv, dado, mult, b): return dict(nome=nome, nivel=nivel, at=at, df=df, rd=rd, pv=pv, dado=dado, mult=mult, b=b)

print('=== 1. SENSIBILIDADE: o mesmo guerreiro (a ficha típica do save no nível 95: +24, Defesa 32, RD 6, PV 230, 1d10 × 2,5 + 8) contra ele mesmo, mudando UMA coisa ===')
base = ficha('base', 95, 24, 32, 6, 230, '1d10', 2.5, 8)
casos = [
 ('nada (controle)',                                        dict()),
 ('SÓ o número do nível: 95 → 275 (ataque, Defesa, PV e arma iguais)', dict(nivel=275)),
 ('SÓ o número do nível: 95 → 180',                         dict(nivel=180)),
 ('a arma como as fichas do save tratam o MÍTICO: × 2,5 → × 3', dict(mult=3)),
 ('a armadura como as fichas tratam o MÍTICO: RD 6 → 8',    dict(rd=8)),
 ('arma E armadura Míticas pelas fichas (× 3, RD 8, +4 ataque, +2 Defesa)', dict(mult=3, rd=8, at=28, df=34)),
 ('a arma LENDÁRIA pela tabela do Livro: × 25',             dict(mult=25)),
 ('a armadura LENDÁRIA pela tabela do Livro: RD 25',        dict(rd=25)),
]
for nome, mud in casos:
    v, r = duelo(dict(base, **mud), base)
    print(f'  {nome:<78} vence {v:>3}% · {r} rodada(s)')

print()
print('=== 2. O DUELO DO OVERGEARED: nível 60 MUITO BEM ARMADO contra nível 275 MAL ARMADO ===')
# PV pela curva do save (~2,6 por nível): 60 → 170 · 275 → 720
# (a) COMO AS FICHAS DO SAVE SÃO MONTADAS (a prática: multiplicador 1 a 3, RD 0 a 8)
p60  = ficha('nível 60, Mítico (ficha do save)', 60, 22, 30, 8, 170, '1d10', 3, 6)
p275 = ficha('nível 275, Comum (ficha do save)', 275, 32, 36, 2, 720, '1d10', 1, 15)
v, r = duelo(p60, p275); print(f'  (a) pelas fichas como o save as monta:            o nível 60 bem armado vence {v:>3}% · {r} rodada(s)')
# (b) PELA TABELA DO LIVRO (X.2), com a regra "abaixo do requisito rende uma categoria abaixo": o Mítico no nível 60 rende LENDÁRIO (× 25, +20, RD 25)
#     ataque = atributo ÷ 10 + maestria + bônus da arma · Defesa = 10 + Agilidade ÷ 10 + armadura
l60  = ficha('nível 60, Mítico rendendo Lendário (Livro)', 60, 7 + 6 + 20, 10 + 7 + 20, 25, 170, '1d10', 25, 7)
l275 = ficha('nível 275, Comum (Livro)', 275, 20 + 8 + 2, 10 + 20 + 2, 0, 720, '1d10', 1, 20)
v, r = duelo(l60, l275); print(f'  (b) pela tabela do Livro, no luta.py de hoje:      o nível 60 bem armado vence {v:>3}% · {r} rodada(s)')
# (c) o mesmo, sem as três coisas que a casa deu ao nível (ações 1 + nível ÷ 60, nível ÷ 5 no dano): ações do Livro (1 + nível ÷ 100)
ac = luta.acoes
luta.acoes = lambda nv: max(1, min(8, 1 + nv // 100))
l60c, l275c = dict(l60, nivel=60), dict(l275, nivel=275)
v, r = duelo(l60c, l275c); print(f'  (c) idem, com as ações do Livro (1 + nível ÷ 100): o nível 60 bem armado vence {v:>3}% · {r} rodada(s)')
luta.acoes = ac

print()
print('=== 3. UMA GUILDA: dez de nível 275 mal armados (fichas do save) contra UM nível 90 com Mítico ===')
def um_contra_muitos(um, muitos, k, n=1500):
    v = 0; rs = []
    for i in range(n):
        r = luta.luta({'monstro': dict(um, gente=True, moral=False), 'grupo': [dict(muitos, nome=f'{muitos["nome"]} {j+1}') for j in range(k)], 'ate': 60})
        v += r['res'] == 'grupo caiu'; rs.append(r['rnd'])
    rs.sort(); return round(100 * v / n), rs[len(rs) // 2]
p90 = ficha('nível 90, Mítico (ficha do save)', 90, 26, 34, 8, 240, '1d10', 3, 9)
l90 = ficha('nível 90, Mítico rendendo Lendário (Livro)', 90, 9 + 6 + 20, 10 + 9 + 20, 25, 240, '1d10', 25, 9)
for k in (1, 3, 10):
    v, r = um_contra_muitos(p90, p275, k); print(f'  pelas fichas do save · contra {k:>2}: o bem armado vence {v:>3}% · {r} rodada(s)')
for k in (1, 3, 10):
    v, r = um_contra_muitos(l90, l275, k); print(f'  pela tabela do Livro · contra {k:>2}: o bem armado vence {v:>3}% · {r} rodada(s)')
