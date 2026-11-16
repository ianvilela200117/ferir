#!/usr/bin/env python3
"""guildas.py — G12, AS GUILDAS DO MUNDO (Dia 433, pedido do jogador; aprovada como proposta).

Seis guildas grandes fora do reino, cada uma com sede, ofício, CHEFE com nome e nível, dois membros fortes,
FORÇA (1 a 6), COFRE, FAMA, um OBJETIVO com relógio de 8 e uma POSTURA para a casa (−2 inimiga … +2 aliada).
Elas ficam em mundo_vivo.json ("guildas"); a Guilda dos Aventureiros de Ireviel ("guilda_da_casa") entra só no
RANKING DE FAMA: ela age pela G1.

Toda semana (o tick semanal chama), cada guilda viva rola d20:
  1      RACHA: perde gente (força −1) e um membro forte vai embora (a 0, se desfaz)
  2-5    CONTRATOS: cofre +1d6×100, fama +1
  6-7    RECRUTA: força +1 (teto 6), cofre −300
  8-10   AGE PELO OBJETIVO: relógio +1
  11-12  CAÇA UM MONSTRO do bestiário vivo (até 1,3 × o nível do chefe; primeiro o da terra dela; o do objetivo
         quando o relógio passa de 4): d20 + força×2 + chefe÷25 contra d20 + 5 + nível÷15 (+4 Lendário, +6 Mítico,
         +10 Primordial). Vence: o bicho MORRE, o núcleo (Épico ou maior) é dela, fama +3 (o do objetivo: relógio +3).
         Perde: 1d6: 1-2 um membro forte morre · 3-4 feridos (força −1) · 5-6 recua sem perda
  13     EXPLORA um lugar novo que guarda NÚCLEO (lugares_novos; Ithium, ...): d20 + força×2 contra 18: leva o que ele guarda
  14     GUERRA DE GUILDA: contra a rival do objetivo (ou uma ao acaso): d20 + força de cada lado; quem perde, força −1;
         quem ganha, relógio +1 (se a rival é o objetivo) ou fama +2
  15     PERDE TERRENO: relógio −1
  16     COMPRA no mercado do mundo (cofre de 3.000 para cima): −2.000; 1d6: 6 um núcleo Épico · o resto material raro (fama +1)
  17     PROCURA A CASA: amiga oferece contrato · neutra propõe negócio (compra de peça da forja, um contrato) · hostil ameaça
         ou sabota (o enviado chega em 1d6+2 dias: agenda)
  18     O CHEFE SOBE 1d6 níveis
  19     GESTO PÚBLICO (torneio, festa, desafio): fama +2, notícia certa
  20     SURPRESA: gerador de novidade ligado a ela (o Mestre roda gerador.py novidade)
  Hostil ou inimiga NÃO DORME (como a G8-D): no 2-7, 1d6: 1-3 força +1 · 4-6 relógio +1.
  Relógio 8/8: OBJETIVO CUMPRIDO (o mundo muda; o Mestre mostra); a guilda para de rolar o objetivo até ganhar outro.
A notícia de cada movimento segue a G8-B (chega pelo dado, com atraso, ou não chega sozinha); a do que toca o reino chega mais fácil.

Uso:
  python3 guildas.py ver [tudo]        o painel (com "tudo": os segredos dos chefes, só para o Mestre)
  python3 guildas.py ranking           o RANKING DE FAMA (com a Guilda dos Aventureiros de Ireviel)
  python3 guildas.py semana DIA        o turno da semana (o tick semanal chama)
  python3 guildas.py fama ID +N "motivo"   |   forca ID N "motivo"   |   postura ID N "motivo"   |   objetivo ID "novo"
"""
import sys
from nucleo import d, carrega, grava, anota, dia_atual, agenda_add, toca_a_casa

POST = {-2: 'INIMIGA', -1: 'hostil', 0: 'neutra', 1: 'amiga', 2: 'ALIADA'}
CATB = {'Lendário': 4, 'Lendario': 4, 'Mítico': 6, 'Mitico': 6, 'Primordial': 10}
COM_NUCLEO = ('Épico', 'Epico', 'Único', 'Unico', 'Lendário', 'Lendario', 'Mítico', 'Mitico', 'Primordial')


def chega(dia, texto, toca):
    r = d(20) - (4 if toca else 0)
    if r <= 4:
        q, s = dia, 'chega hoje'
    elif r <= 10:
        x = d(3); q, s = dia + x, f'chega no dia {dia + x}'
    elif r <= 17:
        x = d(6); q, s = dia + x, f'chega no dia {dia + x}'
    else:
        return f'notícia d20 [{r}] não chega sozinha'
    agenda_add(q, texto, tipo='noticia', origem=f'guildas.py, tick {dia}', toca=toca)
    return f'notícia {s}'


def nivel(m):
    try:
        return int(str(m.get('nivel') or 0).split()[0])
    except ValueError:
        return 0


def vivo(m):
    e = str(m.get('estado', 'ativo')).upper()
    return 'MORT' not in e and 'DESFEIT' not in e


def acha(G, gid):
    for g in G:
        if g['id'] == gid or g['nome'] == gid:
            return g
    sys.exit(f'guilda não achada: {gid} (ids: {", ".join(g["id"] for g in G)})')


def rival_do_objetivo(g, G):
    o = g.get('objetivo', '').upper()
    for h in G:
        if h is not g and h.get('estado') == 'viva' and h['nome'].upper().replace('O ', '', 1).replace('A ', '', 1) in o:
            return h
    for h in G:
        if h is not g and h.get('estado') == 'viva' and h['nome'].split(' ', 1)[-1].upper() in o:
            return h
    return None


def alvo_de_caca(g, M):
    teto = int(g['chefe']['nivel'] * 1.3)
    vivos = [m for m in M.get('monstros', []) if vivo(m) and 0 < nivel(m) <= teto]
    if not vivos:
        return None
    if g['relogio'][0] >= 4:
        for m in vivos:
            if m['nome'].split(',')[0].upper() in g.get('objetivo', '').upper():
                return m
    da_terra = [m for m in vivos if g['sede'].lower() in str(m.get('regiao', '')).lower()]
    pool = da_terra or vivos
    return pool[d(len(pool)) - 1]


def semana(M, dia):
    G = M.get('guildas', [])
    vivas = [g for g in G if g.get('estado') == 'viva']
    print('  AS GUILDAS DO MUNDO (G12, turno da semana):')
    for g in vivas:
        r = d(20)
        p = g.get('postura', 0)
        cab = f"   {g['nome']} ({g['sede']}; força {g['forca']}, {g['relogio'][0]}/8, fama {g['fama']}, {POST[p]}) d20 [{r}]"
        nt, toca = None, 'IREVIEL' in g.get('objetivo', '').upper() or g.get('postura', 0) != 0
        if r == 1:
            g['forca'] -= 1
            saiu = g['membros'].pop(0)['nome'] if g.get('membros') else None
            res = 'RACHA: perde gente' + (f'; {saiu} vai embora' if saiu else '') + f" → força {g['forca']}"
            if g['forca'] <= 0:
                g['estado'] = 'desfeita'; res += ' e SE DESFAZ'
            nt = res.lower()
        elif r <= 7 and p <= -1:
            x = d(6)
            if x <= 3:
                g['forca'] = min(6, g['forca'] + 1); res = f"NÃO DORME 1d6 [{x}]: junta gente → força {g['forca']}"
            else:
                g['relogio'][0] = min(8, g['relogio'][0] + 1); res = f"NÃO DORME 1d6 [{x}]: AGE PELO OBJETIVO → {g['relogio'][0]}/8"
                nt = 'dá um passo no que quer'
        elif r <= 5:
            x = d(6); g['cofre'] += x * 100; g['fama'] += 1
            res = f"CONTRATOS: cofre +{x * 100} → {g['cofre']} · fama {g['fama']}"
        elif r <= 7:
            g['forca'] = min(6, g['forca'] + 1); g['cofre'] = max(0, g['cofre'] - 300)
            res = f"RECRUTA → força {g['forca']}"
        elif r <= 10:
            g['relogio'][0] = min(8, g['relogio'][0] + 1)
            res = f"AGE PELO OBJETIVO ({g['objetivo']}) → {g['relogio'][0]}/8"
            nt = f"dá um passo: {g['objetivo']}"
        elif r <= 12:
            m = alvo_de_caca(g, M)
            if not m:
                res = 'sai à caça e não acha bicho à altura'
            else:
                nm, nv = m['nome'], nivel(m)
                a = d(20) + g['forca'] * 2 + g['chefe']['nivel'] // 25
                b = d(20) + 5 + nv // 15 + CATB.get(m.get('cat') or '', 0)
                tm = toca_a_casa(str(m.get('regiao', '')))
                toca = toca or tm
                if a > b:
                    m['estado'] = f"MORTO ({dia}, pela guilda: {g['nome']})"
                    g['fama'] += 3
                    nuc = (m.get('cat') or '') in COM_NUCLEO
                    if nuc:
                        g['nucleos'].append(f"núcleo {m.get('cat')} de {nm} ({dia})")
                    obj = nm.split(',')[0].upper() in g.get('objetivo', '').upper()
                    if obj:
                        g['relogio'][0] = min(8, g['relogio'][0] + 3)
                    res = (f"CAÇA {nm} ({m.get('cat') or '?'} {nv}, {m.get('regiao', '?')}): {a} × {b} → MATA" +
                           (' e fica com o NÚCLEO' if nuc else '') + (f" (o do objetivo: {g['relogio'][0]}/8)" if obj else '') + f" · fama {g['fama']}")
                    nt = f"matou {nm}" + (' e levou o núcleo' if nuc else '')
                else:
                    x = d(6)
                    if x <= 2 and g.get('membros'):
                        morto = g['membros'].pop(d(len(g['membros'])) - 1)
                        res = f"CAÇA {nm} ({nv}): {a} × {b} → PERDE: {morto['nome']} ({morto['nivel']}) MORRE"
                    elif x <= 4:
                        g['forca'] = max(1, g['forca'] - 1)
                        res = f"CAÇA {nm} ({nv}): {a} × {b} → PERDE: feridos → força {g['forca']}"
                    else:
                        res = f"CAÇA {nm} ({nv}): {a} × {b} → recua sem perda"
                    nt = f"caçou {nm} e perdeu"
        elif r == 13:
            L = [l for l in M.get('lugares_novos', []) if 'NÚCLEO' in str(l.get('guarda', '')).upper() and not l.get('tomado_por')]
            if not L:
                res = 'EXPLORA: não acha lugar que valha'
            else:
                l = L[d(len(L)) - 1]; a = d(20) + g['forca'] * 2
                if a >= 18:
                    l['tomado_por'] = f"{g['nome']} ({dia})"; g['nucleos'].append(f"o que {l['nome']} guardava ({dia})"); g['fama'] += 2
                    res = f"EXPLORA {l['nome']} ({l.get('onde', '?')}): {a} contra 18 → LEVA o que ele guardava"
                    nt = f"entrou em {l['nome']} e levou o que ele guardava"
                    toca = toca or toca_a_casa(str(l.get('onde', '')))
                else:
                    res = f"EXPLORA {l['nome']} ({l.get('onde', '?')}): {a} contra 18 → volta sem nada"
        elif r == 14:
            o = rival_do_objetivo(g, G) or (lambda xs: xs[d(len(xs)) - 1] if xs else None)([h for h in vivas if h is not g and h.get('estado') == 'viva'])
            if not o:
                res = 'GUERRA: não acha rival'
            else:
                a, b = d(20), d(20)
                while a + g['forca'] == b + o['forca']:
                    a, b = d(20), d(20)
                ganha, perde = (g, o) if a + g['forca'] > b + o['forca'] else (o, g)
                perde['forca'] -= 1
                if perde['forca'] <= 0:
                    perde['estado'] = 'desfeita'
                if ganha is g and rival_do_objetivo(g, G) is o:
                    g['relogio'][0] = min(8, g['relogio'][0] + 1)
                else:
                    ganha['fama'] += 2
                res = (f"GUERRA DE GUILDA contra {o['nome']}: [{a}]+{g['forca'] + (1 if perde is g else 0)} × [{b}]+{o['forca'] + (1 if perde is o else 0)} → vence {ganha['nome']}; "
                       f"{perde['nome']} cai a força {perde['forca']}" + (' e SE DESFAZ' if perde.get('estado') == 'desfeita' else ''))
                nt = f"guerra contra {o['nome']}; vence {ganha['nome']}"
        elif r == 15:
            g['relogio'][0] = max(0, g['relogio'][0] - 1)
            res = f"PERDE TERRENO → {g['relogio'][0]}/8"
        elif r == 16:
            if g['cofre'] >= 3000:
                g['cofre'] -= 2000; x = d(6)
                if x == 6:
                    g['nucleos'].append(f"núcleo Épico comprado ({dia})"); res = f"COMPRA 1d6 [{x}]: um NÚCLEO ÉPICO no mercado do mundo"
                    nt = 'comprou um núcleo'
                else:
                    g['fama'] += 1; res = f"COMPRA 1d6 [{x}]: material raro"
            else:
                res = f"quer comprar e não tem cofre ({g['cofre']})"
        elif r == 17:
            oque = 'OFERECE um contrato à casa' if p >= 1 else 'PROPÕE um negócio à casa (uma peça da forja, um contrato)' if p == 0 else 'AMEAÇA ou SABOTA a casa'
            q = dia + d(6) + 2
            agenda_add(q, f"GUILDA — {g['nome']} ({g['sede']}; chefe {g['chefe']['nome']}, {g['chefe']['nivel']}) {oque.lower()}. O que quer: {g['objetivo']}",
                       tipo='marco', origem='guildas.py', toca=True)
            res = f"PROCURA A CASA: {oque} (o enviado chega no {q})"
        elif r == 18:
            x = d(6); g['chefe']['nivel'] += x
            res = f"O CHEFE {g['chefe']['nome']} SOBE {x} → nível {g['chefe']['nivel']}"
        elif r == 19:
            g['fama'] += 2; res = f"GESTO PÚBLICO (torneio, festa ou desafio): fama {g['fama']}"
            nt = 'gesto público (todo mundo vê)'
        else:
            res = 'SURPRESA: gerador de novidade ligado a ela (python3 gerador.py novidade)'
        if g['relogio'][0] >= 8 and g.get('estado') == 'viva' and not g.get('cumpriu'):
            g['cumpriu'] = dia
            res += f" → OBJETIVO CUMPRIDO: {g['objetivo']}"
            agenda_add(dia, f"GUILDA CUMPRIU O OBJETIVO — {g['nome']} ({g['sede']}): {g['objetivo']}", tipo='marco', para=True, origem='guildas.py', toca=True)
            nt = f"cumpriu o objetivo: {g['objetivo']}"
        g.setdefault('log', []).append(f'{dia}: [{r}] {res[:110]}')
        g['log'] = g['log'][-12:]
        marca = ' ◆' if toca else ''
        print(cab + marca + ' ' + res + (' · ' + chega(dia, f"{g['nome']} ({g['sede']}): {nt}", toca) if nt else ''))
    grava('mundo_vivo.json', M)


def ver(M, tudo):
    print('AS GUILDAS DO MUNDO (G12)')
    for g in M.get('guildas', []):
        c = g['chefe']
        print(f"  {'■' * max(g['forca'], 0)}{'□' * (6 - max(g['forca'], 0))} {g['nome']} · {g['sede']} · {g['oficio']} · {g.get('estado')} · fama {g['fama']} · {POST[g.get('postura', 0)]}")
        print(f"      chefe {c['nome']} ({c['nivel']}, {c['classe']}; {c['tracos']}) · membros: " + ', '.join(f"{m['nome']} ({m['nivel']})" for m in g.get('membros', [])))
        print(f"      objetivo: {g['objetivo']} · {g['relogio'][0]}/8 · cofre {g['cofre']}" + (f" · núcleos: {', '.join(g['nucleos'])}" if g.get('nucleos') else ''))
        if tudo:
            print(f"      (OCULTO) desejo {c['desejo']} · ambição {c['ambicao']} · medo {c['medo']} · {c['segredo']} · linha vermelha: {c['linha_vermelha']}")


def ranking(M):
    L = [(g['fama'], g['nome'], g['sede'], g.get('estado')) for g in M.get('guildas', [])]
    c = M.get('guilda_da_casa')
    if c:
        L.append((c['fama'], c['nome'] + ' (A DA CASA)', c['sede'], 'viva'))
    print('O RANKING DE FAMA DAS GUILDAS')
    for i, (f, n, s, e) in enumerate(sorted(L, reverse=True), 1):
        print(f"  {i}. {n} ({s}) · fama {f}" + ('' if e == 'viva' else f' · {e}'))


def main():
    a = sys.argv[1:]
    M = carrega('mundo_vivo.json')
    if not a or a[0] == 'ver':
        ver(M, 'tudo' in a); return
    if a[0] == 'ranking':
        ranking(M); return
    if a[0] == 'semana':
        semana(M, int(a[1]) if len(a) > 1 else dia_atual()); return
    if a[0] in ('fama', 'forca', 'postura', 'objetivo') and len(a) >= 3:
        if a[1] == 'casa' and a[0] == 'fama':
            c = M['guilda_da_casa']; c['fama'] += int(a[2])
            print(f"{c['nome']}: fama {c['fama']} ({a[3] if len(a) > 3 else ''})"); grava('mundo_vivo.json', M); return
        g = acha(M.get('guildas', []), a[1])
        if a[0] == 'objetivo':
            g['objetivo'] = a[2]; g['relogio'] = [0, 8]; g.pop('cumpriu', None)
        elif a[0] == 'fama':
            g['fama'] += int(a[2])
        else:
            g[a[0]] = int(a[2])
        motivo = a[3] if len(a) > 3 else ''
        g.setdefault('log', []).append(f'{dia_atual()}: {a[0]} {a[2]} ({motivo})')
        anota(f"- GUILDA {g['nome']}: {a[0]} {a[2]} ({motivo})")
        grava('mundo_vivo.json', M); print(f"{g['nome']}: {a[0]} → {g.get(a[0]) if a[0] != 'objetivo' else g['objetivo']}")
        return
    print(__doc__)


if __name__ == '__main__':
    main()
