#!/usr/bin/env python3
"""saber.py — G10 (Dia 427, pedido do jogador): a PERGUNTA DENTRO DO JOGO passa pela cabeça de quem responde.

Quando o jogador pergunta algo que o rei (ou um conselheiro) teria de SABER, LER ou PERCEBER no mundo,
o Mestre rola o saber dessa pessoa. A resposta sai do tamanho da margem:
  FALHA FEIA  -> o que a pessoa ACREDITA, e está errado (o Mestre anota a verdade no envelope; à mesa: "o rei acha que...")
  FALHA       -> não sabe; só o óbvio
  SUCESSO     -> o essencial, certo
  GANHO       -> o essencial e um detalhe útil
  EXTRAORD.   -> tudo, e uma pista nova
Pergunta de REGRA, de CÓDIGO ou de como o jogo funciona: fora do jogo, resposta inteira, sem dado.

Uso:
  python3 saber.py DOMINIO DIFICULDADE "a pergunta" [quem=Nome] [mais=N]
  DOMINIO: forja · magia · mundo · guerra · gente · dinheiro · terra · notar
  DIFICULDADE: facil · media · dificil · obscura   (CD 10 · 15 · 20 · 25; o aberto.py soma +10)
  quem=Nome: um conselheiro ou NPC (o bônus vem do nível e do cargo dele; sem quem=, é o rei)
  mais=N: apoio declarado (um livro, a biblioteca do Colégio, a Visão, uma fonte)
"""
import sys, json, subprocess, os
from nucleo import carrega, P

CD = {'facil': 10, 'media': 15, 'dificil': 20, 'obscura': 25}

# O REI: atributo ÷ 10 + perícia (estado_vivo, linha das perícias; ERUDITO: Int 150 vale como Saber Mestre +6)
def bonus_rei(dom):
    F = carrega('ficha.json'); a = F['atributos']
    at = lambda k: a.get(k, 40) // 10
    tab = {
        'forja':    (at('Inteligência') + 8, 'Int ÷10 + Forja LENDÁRIO +8'),
        'magia':    (at('Inteligência') + 6, 'Int ÷10 + Magia MESTRE +6'),
        'mundo':    (at('Inteligência') + 6, 'Int ÷10 + ERUDITO (Saber MESTRE +6)'),
        'guerra':   (at('Astúcia') + 4, 'Astúcia ÷10 + Luta TREINADO +4'),
        'gente':    (at('Empatia') + 2, 'Empatia ÷10 + Intuição +2'),
        'dinheiro': (at('Astúcia') + 2, 'Astúcia ÷10 + Negócio INICIANTE +2'),
        'terra':    (at('Sabedoria') + 2, 'Sabedoria ÷10 + Coleta +2'),
        'notar':    (at('Percepção') + 2, 'Percepção ÷10 + Intuição +2'),
    }
    return tab[dom][0], tab[dom][1], F['nivel']

# O CONSELHO: cada cadeira sabe mais do que é dela (+6 no próprio ofício, +2 perto dele, 0 fora)
OFICIO = {
    'Nouliel': {'dinheiro': 6, 'gente': 2}, 'Eliane': {'guerra': 6, 'notar': 2}, 'Graur': {'guerra': 4, 'notar': 2},
    'Sira': {'gente': 6, 'notar': 6, 'mundo': 2}, 'Isolda': {'notar': 4, 'gente': 2}, 'Herkald': {'forja': 6, 'dinheiro': 2},
    'Thuron': {'magia': 6, 'mundo': 4}, 'Tolvane': {'gente': 4, 'terra': 2}, 'Fabaino': {'dinheiro': 4, 'mundo': 2},
    'Starkald': {'notar': 6, 'terra': 4, 'guerra': 2}, 'Moreth': {'guerra': 6}, 'Bjorvunn': {'mundo': 6, 'magia': 2},
}

def bonus_npc(nome, dom):
    N = carrega('npcs.json', {}); v = N.get(nome)
    if not v: sys.exit(f'sem ficha para "{nome}" (npc.py ver)')
    nv = int(str(v.get('nivel') or 10).split()[0])
    of = OFICIO.get(nome, {}).get(dom, 0)
    return of, f'{nome}: ofício {"+" + str(of) if of else "0"} em {dom}', nv

def main():
    a = sys.argv[1:]
    if len(a) < 3 or a[0] not in ('forja','magia','mundo','guerra','gente','dinheiro','terra','notar') or a[1] not in CD:
        sys.exit(__doc__)
    dom, dif, perg = a[0], a[1], a[2]
    quem = next((x[5:] for x in a[3:] if x.startswith('quem=')), None)
    mais = int(next((x[5:] for x in a[3:] if x.startswith('mais=')), 0))
    b, txt, nv = bonus_npc(quem, dom) if quem else bonus_rei(dom)
    b += mais
    cmd = [sys.executable, P('aberto.py'), f'1d20+{b}', f'cd={CD[dif]}', f'nivel={nv}']
    nota = (f'DECLARADO (G10) PERGUNTA DO JOGADOR, pelo saber de {quem or "Ferir"}: "{perg}" · domínio {dom} · {dif} (CD {CD[dif]}, o aberto soma +10) · '
            f'bônus {b} ({txt}{" + apoio " + str(mais) if mais else ""}; nível {nv}) · falha feia: crença errada (verdade no envelope) · falha: não sabe · '
            f'sucesso: o essencial · ganho: e um detalhe · extraordinário: tudo e uma pista')
    subprocess.run([sys.executable, P('selo.py'), 'nota', nota], stdout=subprocess.DEVNULL)
    r = subprocess.run(cmd, capture_output=True, text=True).stdout
    print(nota); print(r.strip())
    subprocess.run([sys.executable, P('selo.py'), 'nota', 'ROLADO (G10) ' + ' · '.join(l.strip() for l in r.strip().splitlines()[-3:])], stdout=subprocess.DEVNULL)

if __name__ == '__main__':
    main()
