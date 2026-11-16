#!/usr/bin/env python3
"""relogio.py — os relógios de facção, vilão e ameaça com o TOTAL guardado (MOTOR 6): relogios.json.

O problema que isto resolve: os relógios "Leliel → forquilha" e "Descalços → Matriz" eram rolados toda
semana no envelope ("[19] −3 = 16 → +1"), mas o TOTAL nunca ficava escrito em lugar nenhum. Ninguém sabia
em quanto estavam, e um deles passou do fim sem disparar. Agora cada relógio tem valor, tamanho, regra de
dado e o que acontece quando enche; o tick semanal rola todos sozinho e o bloco PARA quando um enche.

Uso:
  python3 relogio.py ver [tudo]                      o painel (com os Lendários perto do fim da obra)
  python3 relogio.py novo "NOME" MAX "o que acontece ao encher" [oculto] [dado=d20] [mod=-3] [sobe="15-20:1"] [inicio=N]
  python3 relogio.py anda "NOME" +N|-N "motivo"     a ficção mexeu no relógio
  python3 relogio.py mod "NOME" N "motivo"          muda o modificador da rolagem semanal
  python3 relogio.py para "NOME" "motivo"  |  retoma "NOME"
  python3 relogio.py fecha "NOME" "o que houve"     o relógio acabou (disparou ou perdeu o sentido)
  python3 relogio.py semana DIA                      rola os relógios vivos (o tick semanal chama sozinho)

REGRA "sobe": faixas do total do dado e quanto anda. Ex.: "15-20:1" (15 ou mais anda 1) · "11-17:1,18-30:2".
O 20 natural sempre conta como a faixa mais alta; o 1 natural nunca anda.
"""
import re, sys
from nucleo import carrega, grava, d, anota, dia_atual, agenda_add, acha_nome

ARQ = 'relogios.json'


def load():
    return carrega(ARQ, {'relogios': []})


def acha(R, nome):
    nomes = [r['nome'] for r in R['relogios']]
    k, sug = acha_nome(nome, nomes)
    if not k:
        sys.exit(f'relógio não achado: "{nome}".' + (f' Parecidos: {", ".join(sug)}' if sug else f' Existem: {", ".join(nomes)}'))
    return next(r for r in R['relogios'] if r['nome'] == k)


def barra(v, m):
    return '●' * min(v, m) + '○' * max(m - v, 0)


def sobe_de(txt):
    out = []
    for p in txt.split(','):
        fx, q = p.split(':')
        a, b = (fx.split('-') + [fx])[:2] if '-' in fx else (fx.rstrip('+'), '99')
        out.append([int(a), int(b), int(q)])
    return sorted(out)


def ver(tudo=False):
    R = load()
    print('RELÓGIOS DA CAMPANHA')
    vivos = [r for r in R['relogios'] if r['estado'] != 'fechado']
    for r in vivos:
        reg = r['regra']
        extra = ' · PARADO' if r['estado'] == 'parado' else ''
        cheio = ' · ⚠ CHEIO: ' + r['ao_encher'] if r['valor'] >= r['max'] else ''
        print(f"  {barra(r['valor'], r['max'])} {r['valor']}/{r['max']} {'[OCULTO] ' if r['oculto'] else ''}{r['nome']}"
              f" · semana: {reg['dado']}{reg['mod']:+d}, {', '.join(f'{a}+ anda {q}' if b >= 30 else f'{a}-{b} anda {q}' for a, b, q in reg['sobe'])}{extra}{cheio}")
        if r.get('conferir'):
            print(f"      ⚠ CONFERIR: {r['conferir']}")
        if tudo:
            for l in r.get('log', [])[-4:]:
                print('      ' + l)
    if not vivos:
        print('  nenhum relógio vivo.')
    M = carrega('mundo_vivo.json')
    perto = [l for l in M.get('lendarios', []) if l.get('estado') != 'morto' and l['relogio'][1] - l['relogio'][0] <= (8 if tudo else 1)]
    if perto:
        print('OBRAS DOS LENDÁRIOS' + ('' if tudo else ' a um passo do fim (ou prontas)') + ':')
        for l in perto:
            print(f"  {barra(l['relogio'][0], l['relogio'][1])} {l['relogio'][0]}/{l['relogio'][1]} {l['nome']} ({l.get('regiao', '?')}): {l['obra'][:90]}")
    povos = [p for p in M.get('povos', []) if p['relogio'][0] >= 5]
    for p in povos:
        print(f"  {barra(p['relogio'][0], 6)} {p['relogio'][0]}/6 o plano dos {p['nome']} ({p['regiao']})")


def enche(r, dia):
    it = agenda_add(dia, f"RELÓGIO CHEIO — {r['nome']}: {r['ao_encher']}", tipo='relogio', oculto=r['oculto'], para=True, origem='relogio', toca=True)
    return f"   ⚠ {r['nome']} ENCHEU ({r['valor']}/{r['max']}): {r['ao_encher']} [agenda #{it['id']}; o bloco PARA]"


def semana(dia):
    R = load()
    linhas, partes = [], []
    for r in R['relogios']:
        if r['estado'] != 'vivo' or r['valor'] >= r['max']:
            continue
        reg = r['regra']
        lados = int(reg['dado'].lstrip('d'))
        nat = d(lados)
        tot = nat + reg['mod']
        anda = 0
        if nat != 1:
            for a, b, q in reg['sobe']:
                if a <= tot <= b:
                    anda = q
            if nat == lados and lados == 20:
                anda = max(anda, max(q for _, _, q in reg['sobe']))
        antes = r['valor']
        r['valor'] = min(r['max'], r['valor'] + anda)
        conta = f"[{nat}]" + (f" {reg['mod']:+d} = {tot}" if reg['mod'] else '')
        res = f"anda {anda} → {r['valor']}/{r['max']}" if anda else f"nada ({antes}/{r['max']})"
        r.setdefault('log', []).append(f'{dia}: {conta} {res}')
        r['log'] = r['log'][-20:]
        linhas.append(f"   {'(OCULTO) ' if r['oculto'] else ''}{r['nome']}: {reg['dado']} {conta} → {res}")
        partes.append(f"{'(OCULTO) ' if r['oculto'] else ''}{r['nome']} {conta} → {res}")
        if r['valor'] >= r['max'] and antes < r['max']:
            linhas.append(enche(r, dia))
    grava(ARQ, R)
    if partes:
        anota(f"- RELÓGIOS {dia} (regra fixa em relogios.json): " + ' · '.join(partes))
    print('  RELÓGIOS DE FACÇÃO:')
    print('\n'.join(linhas) if linhas else '   nenhum relógio vivo para rolar.')
    for r in R['relogios']:
        if r['estado'] == 'vivo' and r['valor'] >= r['max']:
            print(f"   ⚠ {'(OCULTO) ' if r['oculto'] else ''}{r['nome']} está CHEIO e sem desfecho: {r['ao_encher']} (resolver em cena e: relogio.py fecha)")


def main():
    a = sys.argv[1:]
    if not a or a[0] == 'ver':
        ver('tudo' in a)
        return
    c = a[0]
    R = load()
    dia = dia_atual()
    if c == 'semana':
        semana(int(a[1]) if len(a) > 1 else dia)
        return
    if c == 'novo':
        if len(a) < 4:
            sys.exit('uso: relogio.py novo "NOME" MAX "o que acontece ao encher" [oculto] [dado=d20] [mod=-3] [sobe="15-20:1"] [inicio=N]')
        op = {x.split('=')[0]: x.split('=', 1)[1] for x in a[4:] if '=' in x}
        r = {'nome': a[1], 'valor': int(op.get('inicio', 0)), 'max': int(a[2]), 'ao_encher': a[3], 'oculto': 'oculto' in a[4:],
             'estado': 'vivo', 'regra': {'dado': op.get('dado', 'd20'), 'mod': int(op.get('mod', 0)), 'sobe': sobe_de(op.get('sobe', '15-99:1'))},
             'log': [f'{dia}: criado em {op.get("inicio", 0)}/{a[2]}']}
        if any(x['nome'] == r['nome'] for x in R['relogios']):
            sys.exit('já existe um relógio com esse nome.')
        R['relogios'].append(r)
        grava(ARQ, R)
        anota(f"- RELÓGIO NOVO [Dia {dia}] {'(OCULTO) ' if r['oculto'] else ''}{r['nome']} {r['valor']}/{r['max']} · semana {r['regra']['dado']}{r['regra']['mod']:+d} · ao encher: {r['ao_encher']}")
        print(f"relógio criado: {r['nome']} {r['valor']}/{r['max']}")
        return
    r = acha(R, a[1])
    if c == 'anda':
        q = int(a[2].replace('+', ''))
        antes = r['valor']
        r['valor'] = max(0, min(r['max'], r['valor'] + q))
        r.setdefault('log', []).append(f"{dia}: {q:+d} à mão ({a[3] if len(a) > 3 else ''}) → {r['valor']}/{r['max']}")
        r.pop('conferir', None)
        print(f"{r['nome']}: {antes} → {r['valor']}/{r['max']}")
        anota(f"- RELÓGIO [Dia {dia}] {'(OCULTO) ' if r['oculto'] else ''}{r['nome']}: {q:+d} ({a[3] if len(a) > 3 else ''}) → {r['valor']}/{r['max']}")
        if r['valor'] >= r['max'] and antes < r['max']:
            print(enche(r, dia))
    elif c == 'mod':
        velho = r['regra']['mod']
        r['regra']['mod'] = int(a[2])
        r.setdefault('log', []).append(f"{dia}: mod {velho:+d} → {int(a[2]):+d} ({a[3] if len(a) > 3 else ''})")
        print(f"{r['nome']}: modificador {velho:+d} → {int(a[2]):+d}")
        anota(f"- RELÓGIO [Dia {dia}] {r['nome']}: modificador {velho:+d} → {int(a[2]):+d} ({a[3] if len(a) > 3 else ''})")
    elif c in ('para', 'retoma', 'fecha'):
        r['estado'] = {'para': 'parado', 'retoma': 'vivo', 'fecha': 'fechado'}[c]
        r.setdefault('log', []).append(f"{dia}: {r['estado']} ({a[2] if len(a) > 2 else ''})")
        r.pop('conferir', None)
        print(f"{r['nome']}: {r['estado']}")
        anota(f"- RELÓGIO [Dia {dia}] {'(OCULTO) ' if r['oculto'] else ''}{r['nome']}: {r['estado'].upper()} ({a[2] if len(a) > 2 else ''})")
    else:
        sys.exit(__doc__)
    grava(ARQ, R)


if __name__ == '__main__':
    main()
