#!/usr/bin/env python3
"""agenda.py — o calendário do Mestre (MOTOR 6): agenda.json.

Antes, "a Elaeva chega no 382" e "o Tolvane volta ~395" viviam em frases, e as notícias que chegam
a Ireviel eram pescadas dos tick_N.txt. Agora tudo o que tem DIA fica aqui, e o tick avisa sozinho
quando o dia chega (e PARA o bloco nos itens marcados "para").

Uso:
  python3 agenda.py ver [ATE_DIA] [tudo]       o que vem (padrão: 21 dias; "tudo" mostra também as notícias de longe)
  python3 agenda.py hoje                        o que vence hoje e o que está atrasado
  python3 agenda.py add DIA "texto" [oculto] [para] [aprox]
        oculto = só o Mestre sabe · para = o bloco PARA neste dia · aprox = data incerta (~)
  python3 agenda.py feito ID [ID...]            resolvido (sai da lista)
  python3 agenda.py muda ID DIA                 muda a data
  python3 agenda.py limpa                       apaga notícias de longe vencidas há mais de 14 dias

OS FIOS (a lista do 🧵, sem data): o que está aberto na história e quando foi mexido pela última vez.
  python3 agenda.py fios                        a lista (o mais parado em cima)
  python3 agenda.py fio "texto" [oculto]        abre um fio
  python3 agenda.py toca ID ["o que mudou"]     o fio andou hoje (zera a poeira; troca o texto se vier um novo)
  python3 agenda.py fecha ID                    o fio acabou

Tipos: marco (posto à mão) · noticia (posta pelo mundo.py e pelo mundo_vivo.py) · relogio (um relógio encheu) · obra.
"""
import sys
from nucleo import carrega, grava, dia_atual, agenda_add

ARQ = 'agenda.json'


def load():
    return carrega(ARQ, {'prox_id': 1, 'itens': []})


def linha(i, hoje):
    marca = ('⏰ ATRASADO ' if i['dia'] < hoje else '')
    tags = ''.join(t for t, ok in ((' [OCULTO]', i.get('oculto')), (' [PARA]', i.get('para')), (' [~]', i.get('aprox'))) if ok)
    return f"  #{i['id']:<4} Dia {i['dia']} {marca}{i['texto']}{tags}"


def ver(ate=None, tudo=False):
    A = load()
    hoje = dia_atual()
    ate = ate or hoje + 21
    itens = sorted([i for i in A['itens'] if not i['feito'] and i['dia'] <= ate], key=lambda i: (i['dia'], i['id']))
    marcos = [i for i in itens if i['tipo'] != 'noticia']
    nots = [i for i in itens if i['tipo'] == 'noticia' and i['dia'] >= hoje]
    print(f'AGENDA (hoje é o Dia {hoje}; até o {ate})')
    for i in marcos:
        print(linha(i, hoje))
    if not marcos:
        print('  nada marcado.')
    perto = [i for i in nots if i.get('toca')]
    longe = [i for i in nots if not i.get('toca')]
    if perto:
        print('NOTÍCIAS A CAMINHO que tocam a casa:')
        for i in perto:
            print(linha(i, hoje))
    if longe:
        if tudo:
            print('NOTÍCIAS DE LONGE:')
            for i in longe:
                print(linha(i, hoje))
        else:
            print(f'(+{len(longe)} notícias de longe a caminho; "agenda.py ver tudo" mostra)')


def main():
    a = sys.argv[1:]
    if not a or a[0] == 'ver':
        nums = [int(x) for x in a[1:] if x.isdigit()]
        ver(nums[0] if nums else None, 'tudo' in a)
        return
    A = load()
    c = a[0]
    if c == 'hoje':
        hoje = dia_atual()
        xs = [i for i in A['itens'] if not i['feito'] and i['dia'] <= hoje and (i['tipo'] != 'noticia' or i['dia'] == hoje)]
        for i in sorted(xs, key=lambda i: i['dia']):
            print(linha(i, hoje))
        if not xs:
            print('nada vence hoje.')
    elif c == 'add':
        if len(a) < 3:
            sys.exit('uso: agenda.py add DIA "texto" [oculto] [para] [aprox]')
        dia = int(a[1].replace('~', ''))
        it = agenda_add(dia, a[2], oculto='oculto' in a[3:], para='para' in a[3:], origem='mestre')
        if 'aprox' in a[3:] or a[1].startswith('~'):
            A = load()
            next(i for i in A['itens'] if i['id'] == it['id'])['aprox'] = True
            grava(ARQ, A)
        print(f"marcado #{it['id']}: Dia {dia} — {a[2]}")
    elif c == 'feito':
        ids = {int(x) for x in a[1:]}
        for i in A['itens']:
            if i['id'] in ids:
                i['feito'] = True
                print(f"feito #{i['id']}: {i['texto'][:80]}")
        grava(ARQ, A)
    elif c == 'muda':
        for i in A['itens']:
            if i['id'] == int(a[1]):
                i['dia'] = int(a[2])
                print(f"#{i['id']} agora é no Dia {a[2]}")
        grava(ARQ, A)
    elif c == 'limpa':
        hoje = dia_atual()
        antes = len(A['itens'])
        A['itens'] = [i for i in A['itens'] if not (i['tipo'] == 'noticia' and i['dia'] < hoje - 14) and not (i['feito'] and i['dia'] < hoje - 30)]
        grava(ARQ, A)
        print(f"agenda limpa: saíram {antes - len(A['itens'])} itens velhos.")
    elif c == 'fios':
        hoje = dia_atual()
        vivos = sorted([f for f in A.get('fios', []) if not f['fechado']], key=lambda f: f['tocado'])
        print(f'FIOS ABERTOS ({len(vivos)}; o mais parado em cima)')
        for f in vivos:
            parado = hoje - f['tocado']
            print(f"  F{f['id']:<3} {'[OCULTO] ' if f.get('oculto') else ''}{f['texto']}" + (f'  · parado há {parado} dias' if parado >= 7 else ''))
    elif c == 'fio':
        if len(a) < 2:
            sys.exit('uso: agenda.py fio "texto" [oculto]')
        fios = A.setdefault('fios', [])
        f = {'id': max([x['id'] for x in fios], default=0) + 1, 'texto': a[1], 'oculto': 'oculto' in a[2:], 'aberto': dia_atual(), 'tocado': dia_atual(), 'fechado': False}
        fios.append(f)
        grava(ARQ, A)
        print(f"fio F{f['id']} aberto: {a[1]}")
    elif c in ('toca', 'fecha'):
        f = next((x for x in A.get('fios', []) if x['id'] == int(a[1].lstrip('Ff'))), None)
        if not f:
            sys.exit('fio não achado (agenda.py fios)')
        f['tocado'] = dia_atual()
        if c == 'fecha':
            f['fechado'] = True
        elif len(a) > 2:
            f['texto'] = a[2]
        grava(ARQ, A)
        print(f"fio F{f['id']} {'FECHADO' if c == 'fecha' else 'tocado hoje'}: {f['texto'][:90]}")
    else:
        sys.exit(__doc__)


if __name__ == '__main__':
    main()
