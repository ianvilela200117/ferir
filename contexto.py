#!/usr/bin/env python3
"""contexto.py — o BRIEFING do Mestre (MOTOR 6): tudo o que é preciso para retomar, numa página.

O protocolo antigo mandava ler, a cada conversa nova, o estado_vivo.md (111 mil letras), o fim do envelope
(680 mil), o npcs.json (210 mil), o cânone e as regras. Isso custa caro em qualquer modelo e ainda deixa passar
coisa. Este script monta o BRIEFING.md a partir dos arquivos de estado (ficha, reino, agenda, relógios, fios,
selos, mundo vivo) e do último trecho do envelope. O Mestre lê SÓ o briefing; o resto ele consulta por comando
(confere.py TERMO, npc.py cena NOME) quando a cena pedir.

Uso:
  python3 contexto.py            escreve BRIEFING.md e mostra na tela
  python3 contexto.py quieto     só escreve o arquivo
  python3 contexto.py jogador    a versão SEM o que é oculto (para mostrar ao jogador, se ele pedir)
"""
import re, sys, os
from nucleo import carrega, ler, P, envelope_atual, motor, toca_a_casa

PILARES = ['Comida', 'Comércio', 'Dinheiro', 'Saúde', 'Ordem', 'Defesa']


def br(n):
    return f'{int(n):,}'.replace(',', '.')


def corta(t, n):
    t = ' '.join(t.split())
    return t if len(t) <= n else t[:n - 1].rsplit(' ', 1)[0] + '…'


def monta(jogador=False):
    L = []
    e = carrega('estado.json')
    t = e.get('tempo', {})
    dia = t.get('dia', 0)
    F = carrega('ficha.json')
    R = carrega('reino.json')
    A = carrega('agenda.json', {'itens': [], 'fios': []})
    RL = carrega('relogios.json', {'relogios': []})
    S = carrega('selos.json', {'ordem': [], 'selos': {}})
    M = carrega('mundo_vivo.json')
    est = ler('estado_vivo.md')
    oc = lambda x: not (jogador and x)

    L.append(f"# BRIEFING DO MESTRE — relógio no Dia {dia}" + (' (versão do jogador, sem ocultos)' if jogador else ''))
    L.append('')
    if not jogador:
        L.append('> **Este é o PAINEL do Mestre: os números e as datas certas, tirados dos arquivos de estado.** Ele não substitui a leitura de fundo: para narrar com o detalhe que o jogador pede, leia também o `MESTRE.md`, o `canone.md`, as `regras_da_casa_dia199.md`, o `estado_vivo.md` e o último bloco do diário. O que pode ficar sem ler, sem perda nenhuma: os envelopes antigos e os `tick_N.txt` velhos (dados já resolvidos; `confere.py TERMO` acha qualquer coisa neles). O que está marcado [OCULTO] o jogador não sabe.')
        L.append('')
    # 1. relógio
    L.append('## 1. O relógio')
    from nucleo import calendario
    cal = calendario(dia)
    L.append(f"- Dia **{dia}** = **{cal['txt']}**" + (f" · {cal['nota']}" if cal['nota'] else '') + f" · {t.get('hora', '?')} · {t.get('local', '?')} · Pressão {t.get('pressao', 0)}/{t.get('limiar_pressao', 10)}")
    CL = carrega('clima.json', {})
    if CL.get('hoje'):
        L.append('- O tempo hoje: ' + ' · '.join(f"{k}: {v['ceu']}, {v['vento']}" for k, v in CL['hoje'].items()) + f" · o rio: {CL.get('agua', '?')}/100")
    else:
        L.append(f"- O tempo: ainda não rolado pela camada de clima (começa no próximo tick; a frase velha do estado era \"{t.get('clima', '?')}\")")
    prox_lua = next(x for x in range(dia + 1, dia + 31) if calendario(x)['dia_lua'] == 1 or calendario(x)['mudo'])
    L.append(f"- Próxima lua nova: Dia {prox_lua} ({calendario(prox_lua)['txt']}) · Dias Mudos de {cal['ano']}: Dias {190 + 365 * (cal['ano'] - 1013) + 360} a {190 + 365 * (cal['ano'] - 1013) + 364}")
    L.append(f"- Próximo tick semanal: **Dia {t.get('primeiro_tick_semanal', '?')}** · próxima auditoria: Dia {t.get('proxima_auditoria', '?')}")
    m = re.search(r'atualizado:[^\n]*?Dia (\d+)', est.split('\n', 1)[0])
    if m and int(m.group(1)) > dia and not jogador:
        n = int(m.group(1))
        L.append(f"- ⚠ **O relógio do tick está no Dia {dia}, mas a história já foi narrada até o Dia {n}.** O tick do {n} nunca foi rolado. Escolha uma vez: `python3 tick.py dia` (rola agora o amanhecer do {n}) ou `python3 tick.py pula {n} \"já narrado\"` (acerta o relógio sem dados). Depois disso o próximo dia é o {n + 1}.")
    L.append('')
    # 2. Ferir
    if F:
        a = F['atributos']
        lim = 50 * F['nivel'] * (F['nivel'] + 1) + 100
        L.append('## 2. Ferir')
        L.append(f"- **Nível {F['nivel']}** · XP {br(F['xp'])} / {br(lim)} (faltam {br(lim - F['xp'])}) · Int {a['Inteligência']} · Afinidade {a['Afinidade']} · PV {F['pv'][0]}/{F['pv'][1]} · Mana {F['mana'][0]}/{F['mana'][1]} · Foco {F['foco']} · {max(1, min(8, 1 + F['nivel'] // 60))} ações · Fortuna {F['fortuna'][0]}/{F['fortuna'][1]} · Revés {F['reves'][0]}/{F['reves'][1]}")
        L.append(f"- **Cofre {br(F['cofre'])}** · semana fixa: +{br(F['livro']['renda_casa'])} da casa + cidades − {br(F['livro']['despesa'])} · material contado: " + (' · '.join(f"{k} ~{v['kg']:g} kg" for k, v in F.get('materiais', {}).items()) or '—'))
        prox = [mm for mm in F.get('marcos_de_nivel', []) if mm['nivel'] > F['nivel']][:1]
        pont = next(n for n in range(F['nivel'] + 1, F['nivel'] + 4) if n % 3 == 0)
        L.append(f"- Próximos marcos: ponto de habilidade no {pont} · talento no {(F['nivel'] // 10 + 1) * 10}" + (f" · no {prox[0]['nivel']}: {corta(prox[0]['texto'], 150)}" if prox else ''))
        L.append('- Somas de forja e encanto: `python3 obra_valor.py fichas` (já leem o nível desta ficha). Talentos, peças e receitas: `confere.py TERMO` ou a seção "Ferir" do `estado_vivo.md`.')
        L.append('')
    # 3. reino
    if R:
        r = R['reino']
        L.append('## 3. O reino')
        L.append(f"- {r['nome']} · prestígio {r['prestigio']}/10 · legitimidade {r['legitimidade']}/10 · o conselho vota e tudo passa pela Intendente (a Nouliel)")
        for c in R['cidades']:
            p = c['pilares']
            fracos = [k for k in PILARES if p[k] <= 1]
            obras = '; '.join(f"OBRA {o['nome']} (pronta no {o['pronta']})" for o in c.get('obras', []))
            vence = []
            for k, lst in c.get('mods', {}).items():
                for v, mot in lst:
                    mm = re.search(r'até o (\d+)', mot)
                    if mm and int(mm.group(1)) <= dia + 7:
                        vence.append(f'{k} {v:+d} vence no {mm.group(1)}')
            L.append(f"- **{c['nome']}** (~{br(c['gente'])}): " + ' · '.join(f'{k} {p[k]}' for k in PILARES)
                     + (f" · ⚠ EM PERIGO: {', '.join(fracos)}" if fracos else '') + (f' · {obras}' if obras else '') + (f" · {'; '.join(vence)}" if vence else ''))
        L.append('- Relações: ' + ' · '.join(f'{k} {v:+d}' for k, v in r['relacoes'].items()))
        L.append('- Conselho real: ' + ' · '.join(f'{k}: {v.split(" (")[0]}' for k, v in r.get('conselho_real', {}).items()))
        L.append('')
    # 4. agenda
    L.append('## 4. O que vem (agenda, 21 dias)')
    itens = sorted([i for i in A.get('itens', []) if not i['feito'] and i['dia'] <= dia + 21 and oc(i.get('oculto'))], key=lambda i: i['dia'])
    marcos = [i for i in itens if i['tipo'] != 'noticia']
    for i in marcos:
        tags = ''.join(x for x, ok in ((' [OCULTO]', i.get('oculto')), (' [o bloco PARA aqui]', i.get('para')), (' [data aproximada]', i.get('aprox'))) if ok)
        L.append(f"- **Dia {i['dia']}**{' ⏰ ATRASADO' if i['dia'] < dia else ''} — {i['texto']}{tags}")
    if not marcos:
        L.append('- nada marcado.')
    nots = [i for i in itens if i['tipo'] == 'noticia' and i['dia'] >= dia and i.get('toca')]
    if nots:
        L.append('- Notícias a caminho que tocam a casa: ' + ' ‖ '.join(f"Dia {i['dia']}: {corta(i['texto'], 110)}" for i in nots[:8]))
    L.append('')
    # 5. relógios
    L.append('## 5. Relógios')
    vivos = [x for x in RL.get('relogios', []) if x['estado'] != 'fechado' and oc(x.get('oculto'))]
    for x in vivos:
        reg = x['regra']
        L.append(f"- **{x['valor']}/{x['max']}** {'[OCULTO] ' if x['oculto'] else ''}{x['nome']} (semana: {reg['dado']}{reg['mod']:+d}) → ao encher: {x['ao_encher']}"
                 + (' · **CHEIO, sem desfecho ainda**' if x['valor'] >= x['max'] else '') + (' · PARADO' if x['estado'] == 'parado' else ''))
        if x.get('conferir') and not jogador:
            L.append(f"  - ⚠ conferir: {corta(x['conferir'], 330)}")
    if not jogador:
        perto = [l for l in M.get('lendarios', []) if l.get('estado') != 'morto' and l['relogio'][1] - l['relogio'][0] <= 1]
        if perto:
            L.append('- Obras de Lendários no fim: ' + ' · '.join(f"{l['nome']} {l['relogio'][0]}/{l['relogio'][1]} ({corta(l['obra'], 50)})" for l in perto))
            parados = [l['nome'] for l in perto if l['relogio'][0] >= l['relogio'][1]]
            if parados:
                L.append(f"  - ⚠ com a obra PRONTA e sem obra nova (o mundo deles parou): {', '.join(parados)} → `python3 mundo_vivo.py nova_obra \"NOME\"`")
        pp = [p['nome'] for p in M.get('povos', []) if p['relogio'][0] >= 6]
        if pp:
            L.append(f"  - ⚠ povos com o plano cumprido e parado: {', '.join(pp)} → `python3 mundo_vivo.py novo_plano \"NOME\"`")
    L.append('')
    # 6. fios
    L.append('## 6. Fios abertos (o 🧵; no máximo 7 na resposta)')
    fios = sorted([f for f in A.get('fios', []) if not f['fechado'] and oc(False)], key=lambda f: f['tocado'])
    for f in fios:
        txt = f['texto']
        if jogador:
            txt = re.sub(r'\s*\(OCULTO:[^)]*\)', '', txt)
        par = dia - f['tocado']
        L.append(f"- F{f['id']} {txt}" + (f' · parado há {par} dias' if par >= 7 else ''))
    L.append('')
    # 7. perigos perto
    if M:
        terras = [c['nome'].split()[-1] for c in R.get('cidades', [])] + ['Delta', 'salinas', 'o rio', 'costa']
        perto = [m for m in M.get('monstros', []) if m.get('estado') not in ('morto',) and any(tt.lower() in m.get('regiao', '').lower() for tt in terras)]
        L.append('## 7. Monstros grandes nas terras do reino')
        L.append('- ' + (' · '.join(f"{m['nome']} ({m['cat']} {m.get('nivel', '?')}, {m['regiao'].split(' (')[0]}{', dormindo' if m.get('estado') == 'dormindo' else ''})" for m in perto) or 'nenhum'))
        E = M.get('espionagem', {})
        if E and not jogador:
            cel = ' · '.join(f"{k} força {v['forca']}" for k, v in E.get('celulas', {}).items())
            soltos = [i['nome'] for i in M.get('infiltrados', []) if i.get('estado') == 'solto']
            L.append(f"- Espionagem: chefe {E.get('chefe')} (+{E.get('chefe_bonus')}) · células: {cel} · contra-espionagem +{E.get('contra_bonus')}" + (f" · [OCULTO] infiltrado solto em Ireviel: {', '.join(soltos)}" if soltos else ''))
        L.append('')
    # 7b. facções e vilões
    if M and not jogador:
        fs = [f for f in M.get('faccoes', []) if f.get('estado', 'viva') == 'viva' and toca_a_casa(f.get('onde', '') + ' ' + f['nome'])]
        L.append('## 7b. Facções nas terras do reino e vilões')
        if fs and 'forca' in fs[0]:
            POST = {-2: 'INIMIGA', -1: 'hostil', 0: 'neutra', 1: 'amiga', 2: 'ALIADA'}
            for f in sorted(fs, key=lambda f: -f.get('forca', 0)):
                L.append(f"- {f['nome']} ({f.get('onde', '?')}): força {f.get('forca', '?')}/6 · objetivo {f.get('relogio', [0, 6])[0]}/6 · {POST.get(f.get('postura', 0))} · {corta(f.get('objetivo') or f.get('o_que', ''), 150)}")
        else:
            L.append(f"- {len(fs)} facções nas terras do reino ainda SEM FICHA de força (ganham no primeiro tick semanal, ou agora: `python3 faccoes.py semear`). Antes do primeiro turno, acerte a postura de cada uma para a casa: `python3 faccoes.py postura \"NOME\" N`. Lista: " + ' · '.join(f['nome'] for f in fs))
        for v in M.get('viloes', []):
            L.append(f"- [OCULTO] VILÃO {v['nome']} (nível {v.get('nivel', '?')}, {v.get('onde') or v.get('regiao', '?')}): {v.get('obra', '?')} pelo método {v.get('metodo', '?')}" + (f" · {corta(v.get('plano') or v.get('nota', ''), 140)}" if v.get('plano') or v.get('nota') else ''))
        cob = carrega('estado.json').get('cobica', {}).get('pecas_conhecidas', [])
        if cob:
            L.append('- Peças que o mundo cobiça (rolam toda semana): ' + ' · '.join(cob))
        L.append('')
    # 8. o último bloco
    L.append('## 8. Onde a história parou')
    pend = est.split('## Pendentes que Ferir conhece', 1)
    if len(pend) > 1:
        bul = [b for b in pend[1].split('\n') if b.startswith('- ')][:4]
        for b in bul:
            L.append('- ' + corta(b[2:], 2500))
    lac = re.search(r'## Laços\n(.+)', est)
    if lac:
        L.append('- Laços: ' + corta(lac.group(1), 260))
    if not jogador:
        env = ler(envelope_atual())
        paradas = [l for l in env.split('\n') if 'PARADA' in l[:60]]
        if paradas:
            L.append(f"- Última PARADA no envelope ({os.path.basename(envelope_atual())}): " + corta(paradas[-1].lstrip('- '), 900))
    L.append('')
    # 9. selos abertos
    abertos = [S['selos'][i] for i in S.get('ordem', []) if i in S['selos'] and S['selos'][i]['estado'] == 'declarado']
    if abertos and not jogador:
        L.append('## 9. Selos declarados à espera do dado')
        for s in abertos:
            L.append(f"- ({s['id']}) Dia {s['dia']}: {s['titulo']} → `python3 selo.py rola {s['id']}`")
        L.append('')
    # 10. regras do jogador
    L.append('## 10. As regras do jogador (valem sempre)')
    for x in motor().get('regras_do_jogador', []):
        L.append('- ' + x)
    L.append('')
    if not jogador:
        L.append('## 11. Um turno')
        L.append('1. `python3 tick.py bloco N` (ou `ate DIA`): corre os dias com a saída INTEIRA e PARA sozinho em parada. Ler tudo: o clima, o mundo, as facções e os NPCs são matéria de cena.')
        L.append('2. `python3 selo.py lote -` para as tabelas do bloco; `python3 conselho.py ...` quando o jogador responder "conselho" (voto por cadeira).')
        L.append('3. `python3 npc.py cena A B C` para quem entra em cena; `python3 confere.py TERMO` para fato antigo; `python3 clima.py ver`, `python3 faccoes.py ver`, `python3 relogio.py ver`.')
        L.append('4. `python3 ficha.py xp|cofre|mat`, `python3 cresce.py xp`, `python3 npc.py nota`, `python3 agenda.py add|feito|toca`, `python3 relogio.py anda`, `python3 faccoes.py postura|relogio`: o que a cena mudou.')
        L.append('5. Responder no formato (⏳ 🕰️ 🎲 🎭 👁️ 🧵 🎯 📊 📜), com cena longa e sensorial, e registrar o bloco no diário e no topo dos Pendentes do `estado_vivo.md`.')
        L.append('- A cola completa: `python3 motor.py`. Fim de sessão: `python3 salvar.py`.')
    return '\n'.join(L) + '\n'


def main():
    a = sys.argv[1:]
    jog = 'jogador' in a
    txt = monta(jog)
    nome = 'BRIEFING_JOGADOR.md' if jog else 'BRIEFING.md'
    with open(P(nome), 'w', encoding='utf-8') as fh:
        fh.write(txt)
    if 'quieto' not in a:
        print(txt)
    print(f'[{nome}: {len(txt)} letras, cerca de {len(txt) // 3} tokens]', file=sys.stderr)


if __name__ == '__main__':
    main()
