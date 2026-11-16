#!/usr/bin/env python3
"""bicho.py — MOTOR 9 (Dia 438, G9 e G33): a FICHA DE LUTA do bicho sai da saída do gerador, sem montar à mão.

Lê o arquivo que o `gerador.py monstro ... > obras/x.txt` escreveu (a saída INTEIRA) e escreve a base da luta
(sims/x_base.json) com tudo o que o luta.py roda: números, ações (a lei + as cabeças), traços, poder, veneno,
fraqueza, covil pelo degrau (G13) e a SEGUNDA FASE dos chefes Únicos ou acima (G33: d6 rolado aqui, UMA vez,
anotado no envelope como OCULTO). O que o luta.py NÃO roda fica listado em "nao_roda": o Mestre declara antes.

Uso:
  python3 bicho.py obras/x.txt sims/x_base.json [nome=NovoNome] [covil="nome do covil"] [volta] [surpresa] [fase=N|nao]
     nome=      o nome trocado (quando o do gerador bate no cânone)
     covil=     o bicho luta NA TOCA: entra o covil pelo degrau dele (Épico 4d6 CD 21 · Único 6d6 CD 23 · ...)
     volta      G14: a casa saiu e voltou: +2 no ataque e na Defesa
     surpresa   a casa o pega de surpresa (não age na 1ª rodada)
     fase=      força o tipo da fase (já rolado antes) ou "nao" (sem fase)
Depois: python3 combate.py monta x.json base=sims/x_base.json NOMES... (conferir) e de novo com conferido=1.
"""
import json, re, sys
from nucleo import d, anota

DEG = {'Comum': 0, 'Incomum': 1, 'Raro': 2, 'Épico': 3, 'Único': 4, 'Lendário': 5, 'Mítico': 6, 'Primordial': 7}
DANO = ['1d6', '2d6', '3d6', '4d6', '6d6', '8d6', '12d6', '20d6']
ACAT = {'Comum': 0, 'Incomum': 0, 'Raro': 1, 'Épico': 2, 'Único': 2, 'Lendário': 3, 'Mítico': 4, 'Primordial': 5}
FASES = {1: 'troca de Essência', 2: 'chama crias', 3: 'o covil muda', 4: 'foge para outra sala e a luta recomeça lá',
         5: 'perde a fraqueza conhecida e ganha outra', 6: 'fala: oferece um trato (Lei 15)'}


def le(arq):
    R = {'traços': []}; chave = None
    for l in open(arq, encoding='utf-8'):
        l = l.rstrip('\n')
        if l.startswith('  · ') and chave: R[chave].append(l[4:]); continue
        m = re.match(r'^([^:(]+?)(?: \([^)]*\))?:\s*(.*)$', l)
        if m and not l.startswith(' '):
            chave = m.group(1).strip()
            if m.group(2): R[chave] = m.group(2); chave = None if chave not in ('traços', 'drops') else chave
            else: R[chave] = []
    return R


def main():
    a = sys.argv[1:]
    if len(a) < 2: sys.exit(__doc__)
    op = {x.split('=')[0]: x.split('=', 1)[1] for x in a[2:] if '=' in x}; flags = [x for x in a[2:] if '=' not in x]
    R = le(a[0]); cat = R['categoria']; g = DEG[cat]; nv = int(R['nível']); num = R['números']
    n = lambda rx: int(re.search(rx, num).group(1))
    dado, mult = re.search(r'dano (\d+d\d+) × ([\d.,]+)', num).groups()
    M = {'nome': op.get('nome', R['nome']), 'cat': cat, 'nivel': nv, 'pv': n(r'PV (\d+)'), 'df': n(r'Defesa (\d+)'), 'rd': n(r'RD (\d+)'),
         'at': n(r'ataque \+(\d+)'), 'dado': dado, 'mult': float(mult.replace(',', '.')), 'moral': True, 'essencia': R.get('essência', '')}
    if M['mult'] == int(M['mult']): M['mult'] = int(M['mult'])
    acoes = 1 + nv // 60 + ACAT[cat]; nao_roda = []; notas = []
    for tr in R.get('traços', []):
        s = tr.lower()
        if s.startswith('couraça'): M['rd'] += g * 3
        elif s.startswith('regenera'): M['regenera'] = nv // 2
        elif s.startswith('veneno'): M['veneno'] = {'cd': 16, 'rodadas': 3, 'dado': '2d6'}
        elif s.startswith('olhar'): M.setdefault('prende', []).append({'nome': 'o olhar que paralisa', 'cd': 10 + nv // 10, 'teste': 'vontade'})
        elif s.startswith('cospe teia'): M.setdefault('prende', []).append({'nome': 'a teia', 'cd': 10 + nv // 10, 'teste': 'forca'})
        elif s.startswith('muitas cabeças'): acoes += 1
        elif s.startswith('grito'): M['grito'] = {'cd': 15}
        elif s.startswith('reflete'): M['reflete'] = True
        elif s.startswith('devora metal'): M['devora_metal'] = True
        elif s.startswith('fala e mente'): M['inteligente'] = True
        elif s.startswith('pele que devolve'): M['devolve'] = 0.25
        elif s.startswith('enxame'): M['enxame'] = True
        elif s.startswith('agarra'): M['agarra'] = True
        elif s.startswith('sangue que queima'): M['sangue_queima'] = f'{max(g, 1)}d6'
        elif s.startswith('casca que racha'): M['casca'] = True
        elif s.startswith('duas vidas'): M['duas_vidas'] = True
        elif s.startswith('cria no ventre'): M['cria_ventre'] = True
        elif s.startswith('come magia'): M['come_magia'] = True
        elif s.startswith('faro de ferida'): M['faro_ferida'] = True
        elif s.startswith('dono de território'): M['dono_territorio'] = True
        elif s.startswith(('velho demais', 'sentido sísmico')): notas.append(tr + ' → a surpresa não vale contra ele'); flags = [f for f in flags if f != 'surpresa']
        else: nao_roda.append(tr)
    M['acoes'] = acoes
    pod = R.get('poder assinatura', '')
    if pod:
        cd = re.search(r'CD (\d+)', pod); prende = any(x in pod for x in ('prende', 'empurra', 'derruba', 'joga longe'))
        M['poder'] = {'nome': pod.split(', em área')[0], 'tipo': 'area_empurra' if prende else 'area', 'cd': int(cd.group(1)) if cd else 10 + nv // 10}
        if not prende: M['poder']['dano'] = DANO[g]
        if 'corta laços' in pod: M['poder']['rompe_servo'] = True
        if ('infecciona' in pod or 'veneno' in pod) and 'veneno' not in M: M['veneno'] = {'cd': int(cd.group(1)) if cd else 16, 'rodadas': 3, 'dado': '2d6'}
    fq = re.search(r'a Essência (\w+)', R.get('fraqueza', ''))
    if fq: M['fraqueza'] = fq.group(1)
    comp = R.get('comportamento', '')
    if comp.startswith(('caçador', 'servo')) or 'escolhe a presa' in comp: M['inteligente'] = True
    if comp.startswith(('guarda', 'territorial')) or 'covil' in op: M['moral'] = False
    if 'covil' in op and g >= 3: M['covil'] = {'nome': op['covil'], 'dano': DANO[g], 'cd': 15 + g * 2, 'efeito': op.get('efeito', '')}
    if 'volta' in flags: M['at'] += 2; M['df'] += 2; notas.append('+2 no ataque e na Defesa (G14: a casa voltou)')
    if g >= 4 and op.get('fase') != 'nao':
        tp = int(op['fase']) if op.get('fase') else d(6)
        M['fase'] = {'tipo': tp, 'nome': FASES[tp]}
        if not op.get('fase'): anota(f"- (OCULTO) BICHO.PY: a SEGUNDA FASE de {M['nome']} ({cat} {nv}) aos 50% (G33), d6 [{tp}]: {FASES[tp]}")
    M['nota'] = f"bicho.py ({a[0]}): {R.get('corpo', '')}, {R.get('tamanho', '')}, {R.get('essência', '')}; {comp}; fraqueza: {R.get('fraqueza', '')}" + (' · ' + ' · '.join(notas) if notas else '')
    if nao_roda: M['nao_roda'] = nao_roda
    F = {'monstro': M, 'grupo': []}
    if 'surpresa' in flags: F['surpresa'] = True
    json.dump(F, open(a[1], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"{M['nome']} ({cat} {nv}): PV {M['pv']} · Defesa {M['df']} · RD {M['rd']} · ataque +{M['at']} · {M['dado']} × {M['mult']} · {acoes} ações")
    print('  roda sozinho: ' + ', '.join(k for k in ('regenera', 'veneno', 'prende', 'grito', 'reflete', 'devora_metal', 'devolve', 'enxame', 'agarra', 'sangue_queima', 'casca', 'duas_vidas', 'cria_ventre', 'come_magia', 'faro_ferida', 'dono_territorio', 'poder', 'covil', 'fase', 'fraqueza') if k in M))
    if nao_roda: print('  ⚠ NÃO RODA no luta.py (declarar antes como aplica, G33): ' + ' | '.join(nao_roda))
    for x in notas: print('  nota: ' + x)
    print(f'  escrito: {a[1]}')


if __name__ == '__main__':
    main()
