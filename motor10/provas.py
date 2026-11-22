#!/usr/bin/env python3
"""provas.py — MOTOR 10: O BANCO DE PROVAS. As metas de equilíbrio, escritas e medidas.

Toda mudança no tabelas.py ou no luta.py roda isto. Meta que falha: a mudança não entra (ou a meta muda, com a palavra do jogador).
As metas dizem em números o que o jogador pediu no Dia 507:
  "a arma decide muito quem vence" · "uma arma dá chance de um nível 50 vencer um nível 500" · "sem restrição de nível para usar a peça".
Três blocos: O EQUILÍBRIO (quem vence) · A DURAÇÃO (quanto dura) · OS MÓDULOS (cada coisa que interfere, interfere mesmo).

Uso: python3 provas.py [N]        N = lutas por meta (padrão 600)
"""
import sys
import luta
from itens import item
from pessoas import ficha, padrao, veste

C = dict(comum=0, incomum=1, raro=2, epico=3, unico=4, lendario=5, mitico=6, primordial=7)
R = C['raro']


def um(nivel, arma, arm, esc=None, familia='espada', material='malha', nome=None, **kw):
    """um lado com um combatente: nível, categoria da arma, categoria da armadura (e do escudo; sem dizer, igual à armadura)"""
    e = arm if esc is None else esc
    return lambda: [veste(padrao(nome or f'n{nivel}-{arma}{arm}', nivel, **kw), arma=(familia, arma), armadura=(material, arm), escudo=e)]


def varios(k, nivel, arma, arm, pre='s', **kw):
    return lambda: [veste(padrao(f'{pre}{i + 1}', nivel, **kw), arma=('espada', arma), armadura=('malha', arm), escudo=arm) for i in range(k)]


def gente(nome, nivel, arma, armadura=None, escudo=None, arma2=None, **kw):
    """um lado com um combatente vestido peça por peça"""
    return lambda: [veste(padrao(nome, nivel, **kw), arma=arma, armadura=armadura, escudo=escudo, arma2=arma2)]


# (o que se mede · lado A · lado B · faixa de vitória de A em % · opções)
METAS = [
    ('SIMETRIA: iguais em tudo (nível 50, Raro)',                      um(50, R, R, nome='a'), um(50, R, R, nome='b'), (44, 56), {}),
    ('A ARMA: mesmo nível, só a ARMA uma categoria acima',             um(50, R + 1, R), um(50, R, R), (85, 100), {}),
    ('O CONJUNTO: mesmo nível, tudo uma categoria acima',              um(50, R + 1, R + 1), um(50, R, R), (88, 100), {}),
    ('O NÍVEL AJUDA DEVAGAR: mesma arma, 50 contra 75',                um(75, R, R), um(50, R, R), (50, 65), {}),
    ('O NÍVEL CONTA: mesma arma, 50 contra 150',                       um(150, R, R), um(50, R, R), (85, 100), {}),
    ('UMA categoria na arma vence 100 níveis (50 × 150)',              um(50, R + 1, R), um(150, R, R), (55, 80), {}),
    ('A CHANCE PEQUENA: uma arma UMA acima, nível 50 × nível 500',     um(50, R + 1, R), um(500, R, R), (2, 20), {}),
    ('DUAS categorias na arma vencem 150 níveis (50 × 200)',           um(50, R + 2, R), um(200, R, R), (85, 100), {}),
    ('A ARMA DECIDE: uma arma DUAS acima, nível 50 × nível 500',       um(50, R + 2, R), um(500, R, R), (45, 75), {}),
    ('uma arma TRÊS acima, nível 50 × nível 500',                      um(50, R + 3, R), um(500, R, R), (80, 100), {}),
    ('O CONJUNTO duas acima, nível 50 × nível 500',                    um(50, R + 2, R + 2), um(500, R, R), (95, 100), {}),
    ('A GUILDA: um nível 90 de conjunto Mítico × dez de nível 275 de Raro', um(90, C['mitico'], C['mitico'], moral='firme'), varios(10, 275, R, R), (90, 100), dict(n=120)),
    ('SÓ A ARMA NÃO BASTA contra dez: o mesmo, com armadura Rara',     um(90, C['mitico'], R, moral='firme'), varios(10, 275, R, R), (0, 40), dict(n=120)),
    ('O NÚMERO CONTA: um nível 120 de Lendário × dez de nível 60 de Único', um(120, C['lendario'], C['lendario'], moral='firme'), varios(10, 60, C['unico'], C['unico']), (0, 25), dict(n=120)),
    ('SOLDADOS COMUNS não derrubam o Lendário: um nível 120 × dez de nível 15', um(120, C['lendario'], C['lendario'], moral='firme'), varios(10, 15, 0, 0), (97, 100), dict(n=120)),
]
# (o que se mede · lado A · lado B · faixa da MEDIANA de rodadas)
DURACAO = [
    ('duelo entre iguais (nível 50, Raro)',            um(50, R, R, nome='a'), um(50, R, R, nome='b'), (4, 9)),
    ('duelo entre iguais (nível 150, Lendário)',       um(150, 5, 5, nome='a'), um(150, 5, 5, nome='b'), (4, 9)),
    ('cinco contra cinco (nível 40, Incomum)',         varios(5, 40, 1, 1, pre='a'), varios(5, 40, 1, 1, pre='b'), (4, 12)),
]


def modulos(n):
    """cada módulo da luta tem de mexer no resultado para o lado certo. Devolve [(o que se mede, o que deu, passou?)]."""
    out = []; v = lambda a, b, **kw: luta.duelos(a, b, n=n, **kw)[0]
    lan = lambda: [veste(padrao(f'lança {i}', 50), arma=('lança', R), armadura=('couro', R)) for i in (1, 2)]
    esp = lambda: [veste(padrao(f'espada {i}', 50), arma=('espada', R), armadura=('couro', R)) for i in (1, 2)]
    x = v(lan, esp, inicio='perto', lugar=dict(largura=1)); y = v(lan, esp, inicio='perto')
    out.append(('1 ALCANCE: duas lanças vencem duas espadas (couro dos dois lados), num corredor de um e em campo aberto', f'{x}% e {y}%', x >= 60 and y >= 55))
    arq = gente('arqueira', 50, ('arco', R), ('couro', R), arma2=('adaga', R)); inf = gente('infante', 50, ('espada', R), ('malha', R), R)
    lo, co = v(arq, inf, inicio='longe'), v(arq, inf, inicio='colado')
    out.append(('1 DISTÂNCIA: a arqueira começa longe ou começa colada', f'{lo}% contra {co}%', lo - co >= 15))
    es = v(arq, inf, inicio='longe', tempo=['escuro']); out.append(('3 O TEMPO: a mesma arqueira, no escuro', f'{es}% contra {lo}%', lo - es >= 8))
    so = gente('sozinho', 150, ('espada', R), ('malha', R), R, moral='firme'); tres = varios(4, 50, R, R, pre='t')
    ab, cr = v(so, tres, inicio='perto'), v(so, tres, inicio='perto', lugar=dict(largura=1))
    out.append(('2 O LUGAR: um contra quatro, em campo aberto ou num corredor de um', f'{ab}% contra {cr}%', cr - ab >= 10))
    placa = gente('de placa', 50, ('espada', R), ('placa', R), R)
    ma, mo = v(gente('malho', 50, ('malho', R), ('malha', R)), placa), v(gente('montante', 50, ('montante', R), ('malha', R)), placa)
    out.append(('5 GOLPE CONTRA ARMADURA: o malho e o montante contra a placa', f'{ma}% contra {mo}%', ma - mo >= 10))
    fraco = ficha(veste(padrao('fraco', 50, atributos={'Força': 60}), arma=('espada', R), armadura=('placa', R)))
    forte = ficha(veste(padrao('forte', 50, atributos={'Força': 85}), arma=('espada', R), armadura=('placa', R)))
    out.append(('4 FÔLEGO E REQUISITO: a placa em quem não tem Força para ela', f"Defesa {fraco['defesa']:g} contra {forte['defesa']:g}; fôlego por rodada {fraco['fol_rodada']} contra {forte['fol_rodada']}",
                fraco['defesa'] < forte['defesa'] and fraco['fol_rodada'] > forte['fol_rodada']))
    sob = lambda dono: item('arma', 5, 'a espada do Aldric', familia='montante', sob=dict(dono=dono, grau=3))
    dele = ficha(veste(padrao('Aldric', 30, atributos={'Força': 60}), arma=sob('Aldric'))); de_outro = ficha(veste(padrao('Bera', 30, atributos={'Força': 60}), arma=sob('Aldric')))
    out.append(('SOB MEDIDA: a mesma peça na mão do dono e na mão de outro', f"acerto +{dele['arma']['acerto']:g} e × {dele['arma']['mult']:g} contra +{de_outro['arma']['acerto']:g} e × {de_outro['arma']['mult']:g}",
                dele['arma']['mult'] > de_outro['arma']['mult'] and dele['arma']['acerto'] > de_outro['arma']['acerto']))
    ef = [dict(chave='sangra')]
    muitas = veste(padrao('carregado', 50, atributos={'Vontade': 25}), arma=item('arma', 4, familia='espada', efeitos=ef), escudo=item('escudo', 3, efeitos=[dict(chave='firme')]))
    f = ficha(muitas); out.append(('SINTONIA: duas peças despertas em quem só sustenta uma', f"dormem: {', '.join(f['dormem']) or 'nenhuma'}", len(f['dormem']) == 1 and f['arma']['efeitos'] == {'sangra': True}))
    q = 0
    for _ in range(n // 3):
        S = luta.nova(gente('mal armado', 50, ('espada', 0), ('malha', 3), 3)(), gente('bem vestido', 50, ('espada', 0), ('malha', 3), 3)(), inicio='colado', quieto=True); luta.corre(S)
        q += bool(luta.resultado(S)['quebradas'])
    q = round(100 * q / (n // 3)); out.append(('7 DURABILIDADE: espada Comum batendo em armadura Épica quebra', f'em {q}% das lutas', q >= 25))
    m = 0
    for _ in range(n // 3):
        S = luta.nova(um(120, 4, 4, moral='firme')(), varios(6, 30, 1, 1, pre='b')(), inicio='colado', quieto=True); luta.corre(S); r = luta.resultado(S)
        m += bool(r['fugiram'] or r['presos'])
    m = round(100 * m / (n // 3)); out.append(('8 MORAL: seis contra um muito mais forte: alguém foge ou se rende', f'em {m}% das lutas', m >= 40))
    S = luta.nova(gente('o rei', 40, ('lança', 3), ('couro', 2), controla=True)(), varios(2, 40, 1, 1, pre='b')(), inicio='colado', quieto=True)
    p1 = luta.corre(S, interativo=True); S['ordens']['o rei'] = dict(acao='recuar'); S['paradas'] = []; x0 = S['L'][0]['x']; S['L'][0]['ini'] = 99; luta.rodada(S)
    out.append(('10 PARA E PERGUNTA: a luta para antes da 1ª rodada, e a ordem de recuar é cumprida', f"{p1}; o rei foi da casa {x0} para a {S['L'][0]['x']}", p1 == 'parada' and S['L'][0]['x'] < x0))
    return out


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 600
    luta.semente(10); ok = 0; tot = 0
    print(f'BANCO DE PROVAS DO MOTOR 10 · {n} lutas por meta\n')
    print(f"{'O EQUILÍBRIO (vitória do primeiro)':<74}{'faixa':>10}{'medido':>9}")
    for nome, a, b, (lo, hi), kw in METAS:
        v, r = luta.duelos(a, b, n=kw.get('n', n), inicio='colado'); passa = lo <= v <= hi; ok += passa; tot += 1
        print(f"{nome:<74}{f'{lo}-{hi}%':>10}{f'{v}%':>8}  {'passa' if passa else 'FALHA'}  ({r} rodadas)")
    print(f"\n{'A DURAÇÃO (mediana de rodadas)':<74}{'faixa':>10}{'medido':>9}")
    for nome, a, b, (lo, hi) in DURACAO:
        v, r = luta.duelos(a, b, n=max(200, n // 3), inicio='colado'); passa = lo <= r <= hi; ok += passa; tot += 1
        print(f"{nome:<74}{f'{lo}-{hi} r':>10}{f'{r} r':>8}  {'passa' if passa else 'FALHA'}")
    print('\nOS MÓDULOS (cada coisa que interfere, interfere para o lado certo)')
    for nome, deu, passa in modulos(max(300, n // 2)):
        ok += passa; tot += 1
        print(f"  {'passa' if passa else 'FALHA'}  {nome}: {deu}")
    print(f'\n{ok} de {tot} metas passam.')
    return ok == tot


if __name__ == '__main__':
    sys.exit(0 if main() else 1)
