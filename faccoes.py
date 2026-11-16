#!/usr/bin/env python3
"""faccoes.py — o TURNO SEMANAL DAS FACÇÕES (MOTOR 6.1). As 28 facções do mundo_vivo.json eram só texto
(nome, onde, o que querem): nasciam de um evento e nunca mais se mexiam. Agora cada uma tem FORÇA (1 a 6),
um RELÓGIO do objetivo (0 a 6) e uma POSTURA para a casa (−2 inimiga … +2 aliada), e age toda semana.

Por semana, cada facção viva rola d20:
  1      RACHA: perde 1 de força (a 0, se desfaz)
  2-8    quieta
  9-10   JUNTA GENTE OU RECURSO: força +1 (teto 6)
  11-12  AGE PELO OBJETIVO: relógio +1
  13-14  BATE DE FRENTE com outra facção da mesma terra: d20 + força de cada lado; quem perde, −1 de força; quem ganha, relógio +1
  15-16  PERDE TERRENO (a guarda, a lei, um rival ou a própria casa aperta): relógio −1
  17     PROCURA A CASA: aliada oferece, neutra pede audiência, inimiga ameaça ou sabota (entra na agenda)
  18     GANHA UM PATRONO (um poder maior passa a pagar ou proteger): força +1; o Mestre escolhe quem, pelo fio mais perto
  19     GESTO PÚBLICO (marcha, greve, procissão, pichação): notícia certa
  20     SURPRESA: gerador de novidade ligado a ela
(Faixas acertadas na auditoria do Dia 379, 20 mil facções simuladas por um ano: na primeira versão 95% cumpriam o objetivo;
 agora, em um ano, 3 em 10 cumprem, 2 em 10 se desfazem e metade segue na luta.)
Relógio 6/6: OBJETIVO CUMPRIDO: muda a terra dela; para de rolar até ganhar objetivo novo.
A notícia de cada movimento segue a regra de sempre (mundo_vivo.chega) e entra na agenda.

Uso:
  python3 faccoes.py ver [tudo]                    o painel (padrão: as das terras do reino)
  python3 faccoes.py semana DIA                    o turno (o tick semanal chama sozinho)
  python3 faccoes.py semear                        dá força, relógio e postura a quem não tem (força 1d4+1, anotada no envelope)
  python3 faccoes.py postura "NOME" N "motivo"     −2 inimiga · −1 hostil · 0 neutra · +1 amiga · +2 aliada
  python3 faccoes.py forca "NOME" N "motivo"   |   relogio "NOME" +N "motivo"   |   objetivo "NOME" "objetivo novo"   |   fim "NOME" "o que houve"
"""
import re, sys
from nucleo import d, carrega, grava, anota, dia_atual, agenda_add, acha_nome, toca_a_casa, sem_acento

TERRAS = ['ireviel', 'marasar', 'farenta', 'levis', 'delta', 'steunn', 'telosus', 'zisrir', 'rio', 'leve']
POST = {-2: 'INIMIGA', -1: 'hostil', 0: 'neutra', 1: 'amiga', 2: 'ALIADA'}


def terras(f):
    t = sem_acento(f.get('onde', ''))
    return {x for x in TERRAS if x in t}


def chega(dia, texto, toca):
    r = d(20)
    if r <= 4:
        q, s = dia, 'chega hoje'
    elif r <= 10:
        x = d(3); q, s = dia + x, f'chega no dia {dia + x}'
    elif r <= 17:
        x = d(6); q, s = dia + x, f'chega no dia {dia + x}'
    else:
        return f'notícia d20 [{r}] não chega sozinha'
    agenda_add(q, texto, tipo='noticia', origem=f'faccoes.py, tick {dia}', toca=toca)
    return f'notícia d20 [{r}] {s}'


def semear(M, dia):
    novas = []
    for f in M.get('faccoes', []):
        if 'forca' in f:
            continue
        r = d(4) + 1
        f['forca'] = r
        f['relogio'] = [0, 6]
        txt = sem_acento(f.get('o_que', '') + ' ' + f.get('nome', ''))
        f['postura'] = -2 if 'contra a casa' in txt else -1 if re.search(r'(?<![a-z])culto', txt) else 0
        f['estado'] = 'viva'
        novas.append(f"{f['nome']} [{r}]" + (f" postura {POST[f['postura']]}" if f['postura'] else ''))
    if novas:
        anota(f"- FACÇÕES [Dia {dia}] camada nova do MOTOR 6.1: força de partida 1d4+1 de cada facção sem ficha (relógio 0/6; postura neutra, salvo 'contra a casa' = inimiga e culto = hostil; o Mestre ajusta com faccoes.py postura/forca): " + ' · '.join(novas))
    return novas


def ver(M, tudo):
    fs = [f for f in M.get('faccoes', []) if f.get('estado', 'viva') == 'viva' and 'forca' in f and (tudo or toca_a_casa(f.get('onde', '') + ' ' + f['nome']))]
    print('FACÇÕES' + ('' if tudo else ' NAS TERRAS DO REINO') + f' ({len(fs)})')
    for f in sorted(fs, key=lambda f: -f['forca']):
        print(f"  {'■' * f['forca']}{'□' * (6 - f['forca'])} {f['nome']} ({f.get('onde', '?')}) · objetivo {f['relogio'][0]}/6 · {POST[f.get('postura', 0)]} · {f.get('objetivo') or f.get('o_que', '')[:110]}")


def semana(M, dia):
    semear(M, dia)
    vivas = [f for f in M['faccoes'] if f.get('estado', 'viva') == 'viva']
    print('  AS FACÇÕES (turno da semana):')
    for f in vivas:
        if f.get('estado', 'viva') != 'viva':
            continue
        r = d(20)
        toca = toca_a_casa(f.get('onde', '') + ' ' + f['nome'])
        marca = ' ◆' if toca else ''
        cab = f"   {f['nome']} (força {f['forca']}, {f['relogio'][0]}/6, {POST[f.get('postura', 0)]}; {f.get('onde', '?')}){marca} d20 [{r}]"
        nt = None
        if r == 1:
            f['forca'] -= 1
            if f['forca'] <= 0:
                f['estado'] = 'desfeita'
                res = 'RACHA e SE DESFAZ: os que sobram vão para casa ou para outra bandeira'
            else:
                res = f"RACHA: perde gente → força {f['forca']}"
            nt = res
        elif r <= 8 and f.get('postura', 0) <= -1:
            # G8-D (Dia 422): a inimiga e a hostil NÃO DORMEM: no 2-8, 1d6: 1-3 junta gente (força +1) · 4-6 age pelo objetivo
            x = d(6)
            if x <= 3:
                f['forca'] = min(6, f['forca'] + 1)
                res = f"NÃO DORME (G8-D) 1d6 [{x}]: junta gente → força {f['forca']}"
            else:
                f['relogio'][0] = min(6, f['relogio'][0] + 1)
                res = f"NÃO DORME (G8-D) 1d6 [{x}]: AGE PELO OBJETIVO → {f['relogio'][0]}/6"
                nt = 'dá um passo no que quer'
        elif r <= 8:
            res = 'quieta'
        elif r <= 10:
            f['forca'] = min(6, f['forca'] + 1)
            res = f"junta gente ou recurso → força {f['forca']}"
        elif r <= 12:
            f['relogio'][0] = min(6, f['relogio'][0] + 1)
            res = f"AGE PELO OBJETIVO → {f['relogio'][0]}/6"
            nt = 'dá um passo no que quer'
        elif r <= 14:
            outras = [o for o in vivas if o is not f and o.get('estado', 'viva') == 'viva' and terras(o) & terras(f)]
            if not outras:
                f['relogio'][0] = min(6, f['relogio'][0] + 1)
                res = f"não acha rival na terra: age pelo objetivo → {f['relogio'][0]}/6"
            else:
                o = outras[d(len(outras)) - 1]
                ff, fo = f['forca'], o['forca']
                a, b = d(20), d(20)
                while a + f['forca'] == b + o['forca']:
                    a, b = d(20), d(20)
                ganha, perde = (f, o) if a + f['forca'] > b + o['forca'] else (o, f)
                perde['forca'] -= 1
                ganha['relogio'][0] = min(6, ganha['relogio'][0] + 1)
                if perde['forca'] <= 0:
                    perde['estado'] = 'desfeita'
                res = (f"BATE DE FRENTE com {o['nome']}: [{a}]+{ff} × [{b}]+{fo}"
                       f" → vence {ganha['nome']} ({ganha['relogio'][0]}/6); {perde['nome']} cai a força {perde['forca']}" + (' e SE DESFAZ' if perde['forca'] <= 0 else ''))
                nt = f"briga com {o['nome']}; vence {ganha['nome']}"
        elif r <= 16:
            f['relogio'][0] = max(0, f['relogio'][0] - 1)
            res = f"PERDE TERRENO (a guarda, a lei ou um rival aperta) → {f['relogio'][0]}/6"
        elif r == 17:
            p = f.get('postura', 0)
            oque = 'OFERECE ajuda ou aliança à casa' if p >= 1 else 'PEDE AUDIÊNCIA ao conselho' if p == 0 else 'AMEAÇA ou SABOTA a casa (pequeno, mas visível)'
            res = f'PROCURA A CASA: {oque}'
            agenda_add(dia + 1, f"FACÇÃO — {f['nome']} ({f.get('onde', '?')}) {oque.lower()}. O que querem: {f.get('objetivo') or f.get('o_que', '')[:160]}", tipo='marco', origem='faccoes.py', toca=True)
        elif r == 18:
            f['forca'] = min(6, f['forca'] + 1)
            res = f"GANHA UM PATRONO (o Mestre escolhe quem, pelo fio mais perto) → força {f['forca']}"
            nt = 'alguém grande passou a pagar ou proteger'
        elif r == 19:
            res = 'GESTO PÚBLICO (marcha, greve, procissão ou pichação): todo mundo vê'
            if toca:
                agenda_add(dia, f"{f['nome']} ({f.get('onde', '?')}): gesto público", tipo='noticia', origem='faccoes.py', toca=True)
            else:
                nt = 'gesto público'
        else:
            res = 'SURPRESA: gerador de novidade ligado a ela (python3 gerador.py novidade)'
        if f['relogio'][0] >= 6 and f.get('estado', 'viva') == 'viva':
            f['estado'] = 'cumpriu'
            res += ' → OBJETIVO CUMPRIDO: a terra dela muda (o Mestre mostra); para até ganhar objetivo novo'
            agenda_add(dia, f"FACÇÃO CUMPRIU O OBJETIVO — {f['nome']} ({f.get('onde', '?')}): {f.get('objetivo') or f.get('o_que', '')[:160]}", tipo='marco', para=toca, origem='faccoes.py', toca=toca)
            nt = 'conseguiu o que queria'
        f.setdefault('log', []).append(f'{dia}: [{r}] {res[:90]}')
        f['log'] = f['log'][-10:]
        print(cab + ' ' + res + (' · ' + chega(dia, f"{f['nome']} ({f.get('onde', '?')}): {nt}", toca) if nt else ''))
    grava('mundo_vivo.json', M)


def main():
    a = sys.argv[1:]
    M = carrega('mundo_vivo.json')
    dia = dia_atual()
    if not a or a[0] == 'ver':
        ver(M, 'tudo' in a)
        return
    if a[0] == 'semana':
        semana(M, int(a[1]) if len(a) > 1 else dia)
        return
    if a[0] == 'semear':
        n = semear(M, dia)
        grava('mundo_vivo.json', M)
        print(f'{len(n)} facções ganharam ficha: ' + ' · '.join(n) if n else 'todas já têm ficha.')
        return
    if len(a) < 3:
        sys.exit(__doc__)
    k, sug = acha_nome(a[1], [f['nome'] for f in M['faccoes']])
    if not k:
        sys.exit(f'facção não achada: {a[1]}. ' + (f'Parecidas: {", ".join(sug)}' if sug else ''))
    f = next(x for x in M['faccoes'] if x['nome'] == k)
    motivo = a[3] if len(a) > 3 else ''
    if a[0] == 'postura':
        f['postura'] = max(-2, min(2, int(a[2]))); txt = f"postura → {POST[f['postura']]}"
    elif a[0] == 'forca':
        f['forca'] = max(0, min(6, int(a[2]))); txt = f"força → {f['forca']}"
    elif a[0] == 'relogio':
        f['relogio'][0] = max(0, min(6, f['relogio'][0] + int(a[2].replace('+', '')))); txt = f"relógio → {f['relogio'][0]}/6"
    elif a[0] == 'objetivo':
        f['objetivo'] = a[2]; f['relogio'] = [0, 6]; f['estado'] = 'viva'; txt = f'objetivo novo: {a[2]}'; motivo = ''
    elif a[0] == 'fim':
        f['estado'] = 'desfeita'; txt = f'ACABOU: {a[2]}'; motivo = ''
    else:
        sys.exit(__doc__)
    grava('mundo_vivo.json', M)
    print(f'{k}: {txt}' + (f' ({motivo})' if motivo else ''))
    anota(f"- FACÇÃO [Dia {dia}] {k}: {txt}" + (f' ({motivo})' if motivo else ''))


if __name__ == '__main__':
    main()
