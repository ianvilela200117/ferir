"""m2_armadilhas.py: a armadilha que dispara (o golpe dela, pela conta do aço) contra o Maro de hoje e contra quem veste melhor; e a conta exata dos testes do ladino
(achar, desarmar, abrir, arrombar, andar escondido, escutar), pelo 2d20 que explode no 20."""
import sys, random
from med_comum import *
from pessoas import ficha

N = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
R = random.Random(11)
def d20x():
    t = [R.randint(1, 20)]
    while t[-1] == 20: t.append(R.randint(1, 20))
    return t
def rola(dado, vezes=1):
    n, f = map(int, dado.split('d')); return sum(R.randint(1, f) for _ in range(n * vezes))

# ---------- a proposta: as armadilhas (os números iriam ao tabelas_masmorra.py) ----------
ARMADILHAS = {
    'dardo':  dict(dado='1d6',  golpe='ponta',   acerto=6),                 # o dardo da parede: 2d20 + 6 + o bônus da categoria contra a Defesa sem escudo e sem aparo
    'lâmina': dict(dado='1d10', golpe='corte',   acerto=6),                 # a lâmina que varre: o mesmo
    'fosso':  dict(dado='2d6',  golpe='impacto', esquiva='Agilidade', parte='pernas'),     # o chão cede: Agilidade contra 20 + 6 por categoria; falhou, cai (nas pernas)
    'pedra':  dict(dado='2d8',  golpe='impacto', esquiva='Agilidade', parte=None),         # a pedra que cai: Agilidade; falhou, leva (cabeça 3 em 10, tronco 7 em 10)
    'gás':    dict(dado='1d6',  golpe='veneno',  esquiva='Vigor', todos=True),             # o gás passa a armadura: Vigor contra 20 + 6 por categoria; passou, a metade. Pega todos na sala
    'gás com guarda': dict(dado='1d6', golpe='veneno', esquiva='Vigor', todos=True, guarda=True),   # a proposta: o gás divide pela guarda (o amuleto, ou 0,6 da armadura do tronco), como a magia
    'runa':   dict(dado='1d8',  golpe='magia', acerto=6, guarda=True),                     # a runa: contra a Firmeza, o dano pela guarda
}
ESQUIVA = (20, 6)                                                            # o teste de esquiva: contra 20 + 6 por categoria

def golpe(F, arm, cat):
    """um disparo contra a ficha F: devolve o dano (0 se não pegou), a parte, se foi crítico"""
    a = ARMADILHAS[arm]; crit = False
    if 'acerto' in a:
        d1, d2 = d20x(), d20x(); tot = sum(d1) + sum(d2) + a['acerto'] + T.BON[cat]; crit = max(d1[0], d2[0]) == 20 and min(d1[0], d2[0]) >= T.CRIT_OUTRO
        contra = F['def_fixa'] if a['golpe'] != 'magia' else F.get('firmeza', 22 + (F['atributos']['Vontade'] // 10) / 2)
        if (d1[0], d2[0]) == (1, 1) or (tot < contra and not crit): return 0, None, False
        if a['golpe'] == 'magia':
            g = T.guarda(None, F['partes']['tronco']['cat'] if 'tronco' in F['partes'] else None)
            return int(rola(a['dado'], 2 if crit else 1) * T.K_DANO * T.MULT[cat] / (g / (2 if crit else 1))), 'o corpo', crit
        parte = T.ONDE[R.randint(1, 10)]
    else:
        at = F['atributos'][a['esquiva']] // 10; tot = sum(d20x()) + sum(d20x()) + at
        passou = tot >= ESQUIVA[0] + ESQUIVA[1] * cat
        if a['golpe'] != 'veneno' and passou: return 0, None, False
        parte = a.get('parte') or ('cabeça' if R.randint(1, 10) <= 3 else 'tronco')
        if a['golpe'] == 'veneno':
            g = T.guarda(None, F['partes']['tronco']['cat'] if 'tronco' in F['partes'] else None) if a.get('guarda') else 1
            d = int(rola(a['dado']) * T.K_DANO * T.MULT[cat] / g)
            return (d // 2 if passou else d), 'todo o corpo', False
    pc = F['partes'].get(parte)
    prot = (pc['rd'] * T.MATRIZ[a['golpe']][pc['material']] / (2 if crit else 1)) if pc else T.NU
    return int(rola(a['dado'], 2 if crit else 1) * T.K_DANO * T.MULT[cat] / prot), parte, crit

def mede(F, arm, cat, nome):
    pv = F['pvmax']; pega = fer = grave = cai = morre = 0; soma = 0
    for _ in range(N):
        d, parte, crit = golpe(F, arm, cat)
        if d <= 0: continue
        pega += 1; soma += d
        if d >= pv: cai += 1; morre += d > pv * T.FERIDA_GRAVE        # a zero de PV cai; o golpe que tirou mais da metade do PV máximo mata na hora
        elif d >= pv * T.FERIDA_GRAVE: grave += 1
        elif d >= pv * T.FERIDA or (crit and d >= pv * T.FERIDA_MIN): fer += 1
    return f"{nome}: {arm} {T.CATS[cat]}: pega {pega / N:.0%} · tira em média {soma / max(1, pega):.0f} de {pv} quando pega · ferida {fer / N:.0%} · grave {grave / N:.0%} · cai {cai / N:.1%} (morre na hora {morre / N:.1%})"

L = []
def p(x): L.append(x); print(x, flush=True)
quem = [('Maro (malha e elmo Comuns, PV 141)', ficha(cheio('eu'))), ('Tomé (malha e elmo Comuns, PV 161)', ficha(cheio('tome'))), ('Rute (couro Comum, sem elmo, PV 133)', ficha(cheio('rute'))),
        ('o nível 50 de malha Rara', ficha(veste(padrao('x', 50), arma=('espada', 2), armadura=('malha', 2), escudo=2)))]
p('== A ARMADILHA QUE DISPARA (o golpe dela pela conta do aço: dado × 4 × o valor da categoria ÷ a proteção da parte) ==')
for nome, F in quem:
    p(f"-- {nome}: Defesa sem escudo {F['def_fixa']:g}")
    for arm in ARMADILHAS:
        for cat in (0, 1, 2):
            if nome.startswith('o nível 50') and cat == 0: continue
            p(mede(F, arm, cat, nome.split(' (')[0]))

# ---------- a conta exata dos testes ----------
p('\n== OS TESTES DO LADINO (a conta exata do 2d20 que explode no 20) ==')
def t(bonus, contra): return chance(contra - bonus)
gente_ = [('Maro (Agilidade 60, Percepção 50, Leigo)', 6, 5, 0), ('Rute (Agilidade 82, Percepção 68, Leiga)', 8, 6, 0), ('o ladino Iniciante (Agilidade 70, Percepção 60)', 7, 6, 2),
          ('o ladino Treinado (Agilidade 80, Percepção 60)', 8, 6, 4), ('o ladino Mestre (Agilidade 90, Percepção 70)', 9, 7, 6), ('o ladino Lendário (Agilidade 100, Percepção 80)', 10, 8, 8)]
p('ACHAR (procurar: 2 lances): 2d20 + Percepção ÷ 10 + manha, contra 20 + 6 por categoria · de passagem (quem vai na frente, sem procurar): 6 mais difícil')
for nome, ag, pe, ma in gente_:
    p(f"  {nome}: " + ' · '.join(f"{T.CATS[c]} {pct(t(pe + ma, 20 + 6 * c))}" for c in range(5)) + f" · de passagem, Comum {pct(t(pe + ma, 26))}, Incomum {pct(t(pe + ma, 32))}")
p('DESARMAR e ABRIR com a gazua (1 lance por tentativa): 2d20 + Agilidade ÷ 10 + manha, contra 24 + 8 × (a categoria da armadilha ou da fechadura − a da gazua); sem gazua, ela conta um degrau abaixo do Comum')
for nome, ag, pe, ma in gente_:
    p(f"  {nome}: gazua da mesma categoria {pct(t(ag + ma, 24))} · uma abaixo {pct(t(ag + ma, 32))} · duas abaixo {pct(t(ag + ma, 40))} · três abaixo {pct(t(ag + ma, 48))}"
      + f" · (falha por 5 ou mais, na mesma: {pct(1 - t(ag + ma, 24 - 4))}; uma abaixo: {pct(1 - t(ag + ma, 32 - 4))})")
p('ARROMBAR (1 lance e barulho por tentativa): 2d20 + Força ÷ 10 contra 24 + 8 × (a categoria da porta − a da arma de impacto em uso; sem ela, o ombro conta um degrau abaixo do Comum)')
for nome, fo in (('Maro (Força 70)', 7), ('Tomé (Força 79)', 7), ('o bruto (Força 100)', 10)):
    p(f"  {nome}: porta Comum com maça Comum {pct(t(fo, 24))} · porta Comum no ombro {pct(t(fo, 32))} · porta Incomum com maça Comum {pct(t(fo, 32))} · porta Incomum no ombro {pct(t(fo, 40))} · porta Rara com maça Comum {pct(t(fo, 40))}")
p('ANDAR ESCONDIDO: o grupo anda no passo do mais barulhento: 2d20 + Agilidade ÷ 10 + manha − a armadura (couro 0, malha −3, placa −6) − a luz (−6) contra 20 + Percepção ÷ 10 do melhor vigia (alerta +4; dormindo −6)')
vig = [('esqueletos (Percepção 41)', 4), ('goblins (Percepção 61)', 6), ('o guardião (Percepção 54)', 5)]
for nome, b in (('Maro (malha: +6 −3)', 3), ('Rute (couro: +8)', 8), ('o ladino Iniciante (couro: +7 +2)', 9), ('o ladino Treinado (couro: +8 +4)', 12), ('quem veste placa (Agilidade 60: +6 −6)', 0)):
    p(f"  {nome}: " + ' · '.join(f"{vn}: no escuro {pct(t(b, 20 + vb))}, com luz {pct(t(b - 6, 20 + vb))}, alerta e com luz {pct(t(b - 6, 24 + vb))}" for vn, vb in vig[:2]))
p('ESCUTAR à porta (1 lance; rolagem oculta): 2d20 + Percepção ÷ 10 + manha contra 22 (porta de madeira) ou 26 (de ferro ou de pedra); os mortos não respiram: 6 mais difícil')
for nome, ag, pe, ma in gente_[:4]:
    p(f"  {nome}: madeira {pct(t(pe + ma, 22))} · ferro {pct(t(pe + ma, 26))} · mortos atrás da madeira {pct(t(pe + ma, 28))}")
open('m2_saida.txt', 'w').write('\n'.join(L) + '\n')
