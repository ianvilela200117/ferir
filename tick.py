#!/usr/bin/env python3
"""Motor de Mundo v5. O Tick (Parte XVII), lendo e gravando estado.json.   ·   MOTOR 6 (Dia 379)
Uso:
  python3 tick.py dia [estrada|segura]        passa um dia e mostra TUDO (como sempre)
  python3 tick.py bloco N [estrada|segura]    passa N dias de uma vez, com a saída INTEIRA de cada dia (o padrão: detalhe primeiro)
  python3 tick.py bloco N resumo              o mesmo, mostrando só o que toca a casa (o resto fica em tick_N.txt)
  python3 tick.py ate DIA [estrada|segura]    idem, até o dia DIA
  python3 tick.py status                      mostra a linha do RELÓGIO sem rolar nada
  python3 tick.py pula DIA "motivo"           acerta o relógio sem rolar (um dia já narrado à mão)
Por dia: +1 de Pressão · evento local 1d20 ou, na estrada, encontro · avistamento de monstro ·
evento de mundo quando a Pressão chega ao limiar · Fortuna volta · mundo.py e mundo_vivo.py.
A cada 7 dias: o CHECKLIST SEMANAL inteiro (nada fica de fora; XVII.2).
Os dados são aleatórios de verdade (secrets) e saem crus, com horário. O Mestre interpreta; o script só conta.

O QUE O MOTOR 6 MUDOU AQUI (as regras do dado são as mesmas):
  · a saída inteira de cada dia é gravada sozinha em tick_N.txt (o noticias.py e o conferidor leem de lá)
  · BLOCO: vários dias numa chamada. Padrão: saída inteira (motor.json "detalhe": "completo"); com "resumo", só o que toca a casa
  · 6.1: a data do calendário, a lua e os Dias Mudos em cada dia · o CLIMA de cada cidade e o nível do rio (clima.py)
  · 6.1: na semana, o clima pesa nos pilares antes do dado do reino, e as FACÇÕES têm o turno delas (faccoes.py)
  · 6.1: a notícia que chega traz COMO chega (fiel, exagerada, incompleta ou falsa)
  · o bloco PARA sozinho: item da agenda marcado "para", relógio que encheu, cofre negativo
  · a SEMANA faz sozinha o que era feito à mão: o reino (reino.py), os relógios de facção (relogio.py),
    a rotina de dados da semana (rotina.json, pelo selo) e o livro-caixa (ficha.py)
  · a AGENDA do dia aparece no tick: marcos e notícias que chegam hoje
"""
import json, os, re, subprocess, sys
import nucleo
from nucleo import d, agora, carrega, grava, P, toca_a_casa, agenda_do_dia

ARQ = 'estado.json'
# Dia 204 (pedido do jogador): os eventos rolam d20, não d6, para ter mais variedade
EVENTO = ['Guerra', 'Praga', 'Colapso econômico', 'Morte de figura importante', 'Descoberta', 'Evento mágico',
          'Revolta ou greve', 'Golpe ou sucessão', 'Casamento ou aliança de casas', 'Fome ou colheita perdida', 'Monstro grande desce',
          'Cisma religioso ou milagre', 'Caravana ou frota perdida', 'Invenção ou receita nova circula', 'Terremoto, enchente ou incêndio',
          'Traição dentro de uma facção', 'Um Lendário aparece em público', 'A coberta afina (algo do Silêncio)', 'Fronteira muda (terra tomada ou perdida)',
          'SURPRESA (gerador novidade)']
ENCADEIA = ['Escalada', 'Reação', 'Oportunidade', 'Refugiado', 'Preço', 'Silêncio', 'Vingança', 'Aliança inesperada', 'Boato errado', 'Herói local',
            'Mercado reage', 'Fé reage', 'A Liga reage', 'Um monstro aproveita', 'Alguém lucra', 'Alguém some', 'Pedido de ajuda a Ireviel',
            'O eco chega à casa (liga a um fio ativo)', 'Nada por enquanto (volta em 1d6 dias)', 'SURPRESA (gerador novidade)']
LOCAL = ['nada'] * 7 + ['briga na feira', 'um estrangeiro pergunta pela fundição', 'um roubo pequeno no cais', 'uma criança doente na enfermaria piora ou sara',
         'um barqueiro traz boato do rio', 'uma encomenda nova chega à forja', 'um vizinho reclama do barulho ou da fumaça', 'um animal estranho nos lodaçais',
         'uma festa ou casamento no bairro', 'falta algo no mercado (preço sobe)', 'um pedinte com algo valioso para vender', 'um NPC da casa tem um momento (laço ou atrito)',
         'SURPRESA (gerador novidade)']

CHECKLIST = [
    'RELÓGIOS: facções (relogio.py, rolados abaixo), Lendários, ambições de NPC e cultos',
    'AGENDAS E AMBIÇÕES: até 6 NPCs relevantes dão um passo (primeiro os dos fios ativos); um DILEMA chega a quem tem ambição em 3/4',
    'XP E NÍVEL DOS NPCs: somar o que cada um fez na semana (XVI.4) no cresce.py (lutas: nível × 10; ajudante 1/4; missões); a CLASSE de cada um pesa no que fez',
    'ECONOMIA DA CASA: o livro da semana é lançado abaixo (ficha.py); compras e vendas avulsas: ficha.py cofre',
    'COMIDA: porções da semana = pessoas × 7; falta de comida aplica a Fome (XIX)',
    'MATERIAL: estoque de cada material depois do que a forja gastou (XI.5): ficha.py mat',
    'MERCADOS: o que foi vendido pesa na saturação; o que sobrou de estoque regional',
    'VÍNCULOS: 2 vínculos entre NPCs se movem (Módulo 1): os d20 acima dizem a direção; a rotina abaixo diz quais',
    'LAÇOS ÍNTIMOS: o par e a família (Módulo 9): 1 momento ou 1 atrito da semana (rotina abaixo); e PERGUNTAR ao jogador o que Ferir sente',
    'COBIÇA: cada peça Mítica ou Lendária conhecida rola (Módulo 10): os d20 acima',
    'FIOS: cada fio ativo avança um passo (agenda.py fios mostra os parados)',
    'NOVIDADE E MEMÓRIA: algo novo entra (gerador.py novidade) e algo antigo volta (XXI.6)',
]
A_MAO = 'À MÃO nesta semana: agendas e ambições (até 6 NPCs) · comida · mercados · cobiça e vínculos (ler os d20) · cada fio anda um passo · 1 novidade e 1 memória · perguntar o que Ferir sente'


def seg(txt):
    a, b = txt.split('/')
    return int(a), int(b)


def relogios(e, dia):
    linhas = []
    for grupo, chave in (('relogios_faccao', 'seg'), ('lendarios', 'relogio'), ('ambicoes', 'seg'), ('cultos', 'seg')):
        for r in e.get(grupo, []):
            if not isinstance(r, dict) or chave not in r:
                continue
            try:
                atual, total = seg(r[chave].split(',')[0].strip())
            except ValueError:
                continue
            m = re.search(r'(\d+)', r.get('ritmo', r[chave].split(',')[1] if ',' in r[chave] else '14'))
            passo = int(m.group(1)) if m else 14
            prox = r.setdefault('proximo', dia + passo)
            while prox <= dia and atual < total:
                atual += 1; prox += passo
                linhas.append(f"{r.get('faccao', r.get('nome', '?'))} avança para {atual}/{total}" + (' -> COMPLETO: muda o mundo' if atual == total else ''))
            r['proximo'] = prox
            resto = r[chave].split(',', 1)[1] if ',' in r[chave] else ''
            r[chave] = f'{atual}/{total}' + (f',{resto}' if resto else '')
    return linhas


def roda(script, *args):
    """roda um script do motor e devolve (linhas normais, linhas de resumo, erro)"""
    env = dict(os.environ, MOTOR_RESUMO='1')
    r = subprocess.run([sys.executable, P(script)] + [str(x) for x in args], capture_output=True, text=True, env=env)
    linhas = r.stdout.rstrip('\n').split('\n') if r.stdout.strip() else []
    res = [l[6:] for l in linhas if l.startswith('::R:: ')]
    norm = [l for l in linhas if not l.startswith('::R:: ')]
    erro = r.stderr.strip()[-400:] if r.returncode != 0 or (not linhas and r.stderr.strip()) else ''
    if erro:                 # MOTOR 6: script que cai no meio não passa mais calado
        ult = erro.splitlines()[-1]
        norm.append(f'⚠ {script} CAIU NO MEIO: {ult}')
        res.append(f'⚠ {script} CAIU NO MEIO: {ult} (o resto não rodou; consertar e avisar o jogador)')
    return norm, res, erro


# ---------- o resumo ----------
def resumo_mundo(linhas):
    """mundo.py: blocos separados por '——'. Fica o que TOCA A CASA; o resto vira contagem."""
    out, longe, bloco = [], 0, []

    def fecha(b):
        nonlocal longe
        if not b:
            return
        txt = '\n'.join(b)
        if 'TERRA ALÉM DO MAPA' in txt:
            if 'ABRE-SE' in txt:
                out.append('  ◆ ' + ' '.join(x.strip() for x in b)[:300])
            return
        m1 = re.search(r'd20 \[\d+\] (.+)', txt)
        m2 = re.search(r'ONDE: d\d+ \[\d+\] ([^\n◆]+)', txt)
        m3 = re.search(r'A NOTÍCIA: (.+)', txt)
        if not m1:
            return
        if '◆ TOCA A CASA' in txt:
            ler_ = re.search(r'LEITURA DO DADO: (.+)', txt)
            nome = re.search(r'\n\s*nome: (.+)', txt)
            o_que = re.sub(r'\s*\([^)]*\)', '', m1.group(1).split(' · 1d6')[0])
            out.append(f"  ◆ O MUNDO, perto: {o_que}" + (f": {ler_.group(1)}" if ler_ else '') + f" — {m2.group(1).strip() if m2 else '?'}"
                       + (f" ({nome.group(1).strip()})" if nome else '') + f" · notícia {m3.group(1) if m3 else '?'}")
        else:
            longe += 1

    for l in linhas:
        if l.strip() in ('——', '————————————————————————————————————————'):
            if l.strip() == '——':
                fecha(bloco); bloco = []
            continue
        if l.startswith('O MUNDO SE MOVE'):
            continue
        if 'TERRA ALÉM DO MAPA' in l:
            fecha(bloco); bloco = [l]
            continue
        bloco.append(l)
    fecha(bloco)
    return out, longe


def resumo_vivo(linhas, semanal, nfaisca):
    out, sec, longe, pai = [], '', {}, False
    faiscas = []
    SEMPRE = ('CHOQUE DE RIVAIS', 'OBRA COMPLETA', 'ACORDA', 'EXPLODE', 'ESQUENTA MUITO', 'IDENTIFICADO', 'PISTA (', 'FALHA FEIA', 'SEGREDO', 'RUMOR VERDADEIRO',
              'ENTRA e descobre', 'PEGA:', 'a célula cresce', 'OBRAS PRONTAS E PARADAS', 'PLANOS CUMPRIDOS', 'o chefe CAI', 'UM GESTO GRANDE', 'TRAMA NOVA')
    for l in linhas:
        s = l.strip()
        if not s or s.startswith('O MUNDO VIVO'):
            continue
        if s.startswith('FAÍSCA:'):
            faiscas.append(s)
            continue
        cab = next((c for c in ('OS LENDÁRIOS', 'MONSTROS GRANDES', 'POVOS-MONSTRO', 'TRAMAS', 'ESPIONAGEM DA CASA', 'FAÍSCAS DO MESTRE', 'REDES INIMIGAS') if s.startswith(c)), None)
        if cab:
            sec = cab
            continue
        if l.startswith('     ') and not s.startswith(('CONTRA-', 'REDES')) and sec in ('MONSTROS GRANDES', 'POVOS-MONSTRO'):   # continuação (migra para / +N níveis / chefe)
            if pai or toca_a_casa(s) or 'o chefe CAI' in s:
                out.append('      ' + s)
            continue
        fica = any(k in s for k in SEMPRE)
        if sec == 'ESPIONAGEM DA CASA':
            fica = not s.startswith('CD de ') and 'nada de novo' not in s and 'célula caída' not in s
        elif sec == 'REDES INIMIGAS':
            fica = 'barrada' not in s
        elif s.startswith('CONTRA-ESPIONAGEM'):
            fica = 'não visto' not in s
        elif s.startswith('trama do dia'):
            fica = 'nada visível' not in s
        elif s.startswith('Lendários: d20'):
            fica = False
            pai = False
            continue
        elif not fica:
            fica = toca_a_casa(s) and not re.search(r'\(próximo passo no dia \d+\)$', s)
            if sec == 'TRAMAS' and ' segue · ' in s and not any(k in s for k in SEMPRE):
                fica = False
        pai = fica
        if fica:
            out.append('  ' + enxuga(s))
        else:
            longe[sec or 'dia'] = longe.get(sec or 'dia', 0) + 1
    perto = [f for f in faiscas if toca_a_casa(f)]
    escolhidas = (perto + [f for f in faiscas if f not in perto])[:nfaisca]
    out += ['  ' + f for f in escolhidas]
    return out, sum(longe.values())


def enxuga(s):
    """encurta a linha de Lendário, monstro ou povo para o resumo (a linha inteira fica no tick_N.txt)"""
    s = re.sub(r' · notícia d20 \[\d+\] chega hoje', ' · notícia HOJE', s)
    s = re.sub(r' · notícia d20 \[\d+\] chega no dia (\d+)', r' · notícia no \1', s)
    s = re.sub(r' · notícia d20 \[\d+\] não chega sozinha \([^)]*\)', ' · sem notícia', s)
    m = re.match(r'(.+?) \((.*)\) d20 \[(\d+)\] (.*)$', s)
    if m and len(m.group(2)) > 60:
        dentro = m.group(2)
        corte = dentro.find(' (')
        if 0 < corte:
            dentro = dentro[:corte]
        s = f'{m.group(1)} ({dentro[:70]}) d20 [{m.group(3)}] {m.group(4)}'
    return s if len(s) <= 330 else s[:327] + '…'


def agenda_linhas(dia, max_outras):
    itens = agenda_do_dia(dia)
    out, paradas = [], []
    marcos = [i for i in itens if i['tipo'] != 'noticia']
    for i in sorted(marcos, key=lambda i: i['dia']):
        atras = f' (era do Dia {i["dia"]})' if i['dia'] < dia else ''
        out.append(f"  ▶ AGENDA #{i['id']}{atras}: {'[OCULTO] ' if i['oculto'] else ''}{i['texto']}")
        if i.get('para') and i['dia'] == dia:
            paradas.append(f"agenda #{i['id']}: {i['texto'][:110]}")
    nots = [i for i in itens if i['tipo'] == 'noticia']
    perto = [i for i in nots if i.get('toca')]
    longe = [i for i in nots if not i.get('toca')]
    def bo(i):
        b = i.get('boato')
        return f" · COMO CHEGA: d20 [{b[0]}] {b[1]}" if b else ''
    for i in perto:
        out.append(f"  ✉ NOTÍCIA QUE CHEGA HOJE: {i['texto']}{bo(i)}")
    if longe:
        if nucleo.motor().get('detalhe', 'completo') == 'completo':
            for i in longe:
                out.append(f"  ✉ notícia de longe que chega hoje: {i['texto']}{bo(i)}")
        else:
            curtas = [i['texto'][:70] for i in longe[:max_outras]]
            out.append(f"  ✉ outras notícias de longe hoje ({len(longe)}): " + ' ‖ '.join(curtas) + (' …' if len(longe) > max_outras else ''))
    return out, paradas


# ---------- um dia ----------
def um_dia(estrada, limite):
    """roda um dia. devolve dict(dia, cru=[...], resumo=[...], paradas=[...])"""
    e = carrega(ARQ)
    t = e['tempo']
    L = t.get('limiar_pressao', 10)
    cfg = nucleo.motor()
    t['dia'] += 1; t['hora'] = 'amanhecer'; dia = t['dia']
    t['pressao'] += 1
    grava(ARQ, e)            # o dia novo já vale para os scripts chamados (selo, ficha, agenda)
    C, R, paradas = [], [], []
    loc = d(20)
    txt = f"[{agora()}] Dia {dia} · Pressão {t['pressao']}/{L} · {'encontro de estrada' if estrada else 'evento local'} 1d20 [{loc}]"
    if estrada:
        achou = loc <= limite * 3 + 1
        txt += ' -> encontro na estrada' if achou else ' -> nada'
        local_txt = 'ENCONTRO NA ESTRADA' if achou else ''
    else:
        txt += f' -> {LOCAL[loc - 1]}'
        local_txt = '' if LOCAL[loc - 1] == 'nada' else LOCAL[loc - 1]
    C.append(txt)
    cal = nucleo.calendario(dia)
    clima_res = ''
    if nucleo.camada('clima'):
        nc, _, _ = roda('clima.py', 'dia', dia)
        C += nc
        ir = next((l.strip() for l in nc if l.strip().startswith('Ireviel:')), '')
        rio = next((l.strip() for l in nc if l.strip().startswith('O RIO:')), '')
        clima_res = ' · ' + ir.split(' (')[0] + (' · ' + rio.split(' [')[0] if rio else '')
        extremos = [l.strip() for l in nc if any(k in l for k in ('tempestade', 'geada', 'neve', 'MUDOU', 'CHEIA', 'SECO')) and not l.strip().startswith('Ireviel:')]
    else:
        C.append(f"  ({cal['txt']})" + (f" · {cal['nota']}" if cal['nota'] else ''))
        extremos = []
    av = d(20)
    tab = e.get('bestiario', {}).get('avistamento')
    linha = f'  avistamento de monstro 1d20 [{av}]'
    visto = ''
    if av <= 7:
        q = d(len(tab)) if isinstance(tab, list) and tab else d(6)
        visto = tab[q - 1] if isinstance(tab, list) and len(tab) >= q else f'[{q}]'
        linha += f' -> alguém vê um · tabela 1d{len(tab) if tab else 6} [{q}]' + (f' {visto}' if isinstance(tab, list) and len(tab) >= q else '')
    else:
        linha += ' -> nenhum'
    C.append(linha)
    cab = f"Dia {dia} · Pressão {t['pressao']}/{L}" + (f' · local: {local_txt}' if local_txt else '') + (f' · avistamento: {visto}' if visto else '')
    R.append(cab.replace(f'Dia {dia} ·', f"Dia {dia} ({cal['txt']}){clima_res} ·", 1))
    if cal['nota']:
        R.append('  ☾ ' + cal['nota'])
    if os.path.exists(P('festas.py')):   # MOTOR 9.1 (438, G36): as FESTAS DO CALENDÁRIO, no dia delas
        _nfe, _, _ = roda('festas.py', 'dia', dia)
        C += _nfe; R += [l for l in _nfe if 'FESTA' in l or 'À MÃO' in l]
    R += ['  ☁ ' + x for x in extremos]
    if t['pressao'] >= L:
        # G8-A (Dia 423, pedido do jogador): a PRESSÃO cheia rola TRÊS eventos de mundo: 1 LONGE, 1 PERTO, 1 ALEATÓRIO
        import importlib.util
        _sp = importlib.util.spec_from_file_location('mundo_g8', P('mundo.py')); _mg = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(_mg)
        _M = _mg.load()
        for alvo, rot in (('longe', 'LONGE'), ('perto', 'PERTO'), (None, 'ALEATÓRIO')):
            ev, en = d(20), d(20); od, onome = _mg.onde_de(_M, alvo)
            C.append(f'  EVENTO DE MUNDO ({rot}) 1d20 [{ev}] {EVENTO[ev - 1]} · encadeamento 1d20 [{en}] {ENCADEIA[en - 1]} · ONDE: {od}')
            R.append(f'  ★ EVENTO DE MUNDO ({rot}) [{ev}] {EVENTO[ev - 1]} · encadeamento [{en}] {ENCADEIA[en - 1]} · ONDE: {od}' + ('  ◆ TOCA A CASA' if toca_a_casa(onome) else ''))
        C.append('  Pressão zera')
        t['pressao'] = 0
    C.append('  Fortuna volta ao máximo')
    _sv = carrega('servos.json', {'servos': []}).get('servos', [])   # MOTOR 9 (438, G23): a palavra dos servos armados cobra sangue a cada aurora
    for _s in [x for x in _sv if x.get('de_pe')]:
        C.append(f"  ☠ SERVO ARMADO {_s['nome']} (nível {_s.get('nivel', '?')}): a PALAVRA cobra do rei {_s.get('palavra', '1d6 × 2')} de PV nesta aurora (rolar no selo.py e lançar em ficha.py pv)"
                 + (f" · {_s['preco']}" + (' ⚠ O PRAZO PASSOU' if _s.get('prazo') and dia > _s['prazo'] else '') if _s.get('preco') else '')
                 + (f" · lua nova no {_s['lua_nova']}: o nome e a gota de sangue" if _s.get('lua_nova') else ''))
    F = carrega('ficha.json')
    if F:
        F['fortuna'][0] = F['fortuna'][1]
        for rec in F.get('recursos', {}).values():   # 6.3: o que volta por dia, volta
            if rec.get('renova') == 'dia' or (rec.get('renova') == 'semana' and dia >= t['primeiro_tick_semanal']):
                rec['tem'] = rec['max']
        grava('ficha.json', F)
    if nucleo.camada('ferimentos'):
        nfe, _, _ = roda('feridos.py', 'dia', dia)
        C += nfe
        R += nfe
    semanal = dia >= t['primeiro_tick_semanal']
    modo = 'semana' if semanal else 'dia'
    nm, _, err = roda('mundo.py', modo, dia)
    C += ['  ' + l for l in nm] or [f'  o mundo: (falhou) {err}']
    rm, longe_m = resumo_mundo(nm)
    R += rm + ['  ' + l for l in nm if l.startswith('⚠')]
    nv, _, err = roda('mundo_vivo.py', modo, dia)
    C += ['  ' + l for l in nv] or [f'  o mundo vivo: (falhou) {err}']
    rs = cfg.get('resumo', {})
    rv, longe_v = resumo_vivo(nv, semanal, rs.get('faiscas_na_semana', 3) if semanal else rs.get('faiscas_no_dia', 1))
    if semanal:
        R.append(f'  ═══ TICK SEMANAL (Dia {dia}) ═══')
    R += rv + ['  ' + l for l in nv if l.startswith('⚠')]
    if longe_m + longe_v:
        R.append(f'  (longe da casa: {longe_m + longe_v} movimentos do mundo que não tocam o reino; estão no tick_{dia}.txt)')
    if semanal:
        C.append(f'  TICK SEMANAL (Dia {dia}) — checklist completo:')
        for l in relogios(e, dia):
            C.append('   · ' + l)
        v = [d(20) for _ in range(2)]
        pecas = e.get('cobica', {}).get('pecas_conhecidas', [])
        c = [d(20) for _ in range(max(1, len(pecas) or 1))]
        C.append(f'   · vínculos 1d20 {v} (1-9 desce, 10-11 fica, 12-20 sobe; 1 e 20 rompem ou selam) · cobiça 1d20 {c} (1-3 alguém age pela peça; 1 é alguém grande)')
        def dirv(x):
            return 'ROMPE' if x == 1 else 'SELA' if x == 20 else 'desce' if x <= 9 else 'fica' if x <= 11 else 'sobe'
        R.append(f"  vínculos {v}: {dirv(v[0])} e {dirv(v[1])}")
        cob = [f"{pecas[i] if i < len(pecas) else '?'} [{x}]" + (' ALGUÉM GRANDE' if x == 1 else '') for i, x in enumerate(c) if x <= 3]
        R.append('  cobiça: ' + (' · '.join(cob) + ' → alguém age pela peça' if cob else 'ninguém age esta semana'))
        for i, item in enumerate(CHECKLIST, 1):
            C.append(f'   [{i:2d}] {item}')
        C.append('   [13a] A SEMANA DOS NPCs (regra da casa, Dia 200: ocupação, missões, ouro e XP):')
        n0, r0, err = roda('semana_npc.py', dia)
        C += ['      ' + l for l in n0] or ['      ninguém' + (f' (falhou: {err})' if err else '')]
        R.append('  A SEMANA DOS NPCs:')
        R += ['    ' + l for l in r0]
        C.append('   [13] O MUNDO CRESCE (obrigatório, regra da casa do Dia 199): lançar no cresce.py o XP da semana de cada NPC ANTES; agora o livro sobe quem tem XP:')
        n1, r1, err = roda('cresce.py', 'tick', dia)
        C += ['      ' + l for l in n1] or ['      ninguém sobe nesta semana' + (f' (falhou: {err})' if err else '')]
        R += ['    ' + l for l in r1]
        # --- MOTOR 6: o reino, os relógios, a rotina e o livro, sem chamada à mão ---
        if nucleo.camada('clima'):
            C.append('   [14a] O CLIMA DA SEMANA (clima.py semana; pesa na Comida e no Comércio antes do dado do reino):')
            ncl, _, err = roda('clima.py', 'semana', dia)
            C += ['    ' + l for l in ncl]
            R += [l for l in ncl]
        if nucleo.camada('mercado'):
            C.append('   [14b] O MERCADO (mercado.py semana):')
            nme, _, err = roda('mercado.py', 'semana', dia)
            C += ['    ' + l for l in nme]
            R += nme
        C.append('   [14] O REINO (reino.py semana):')
        n2, r2, err = roda('reino.py', 'semana', dia)
        C += ['      ' + l for l in n2] or [f'      (falhou: {err})']
        R.append('  O REINO:')
        R += ['    ' + l for l in r2]
        cidades = 0
        for l in n2:
            m = re.search(r'RENDA DAS CIDADES FORA DO LIVRO: ([+-]?\d+)', l)
            if m:
                cidades = int(m.group(1))
        C.append('   [15] OS RELÓGIOS DE FACÇÃO (relogio.py semana):')
        n3, _, err = roda('relogio.py', 'semana', dia)
        C += ['    ' + l for l in n3] or [f'      (falhou: {err})']
        R += n3
        if nucleo.camada('faccoes'):
            C.append('   [15a] O TURNO DAS FACÇÕES (faccoes.py semana):')
            nf, _, err = roda('faccoes.py', 'semana', dia)
            C += ['    ' + l for l in nf]
            perto_f = [l for l in nf if '◆' in l or 'OBJETIVO CUMPRIDO' in l or 'SE DESFAZ' in l or l.startswith('⚠')]
            R.append('  AS FACÇÕES (as que tocam a casa):')
            R += [enxuga(l) if len(l) < 330 else l[:330] for l in perto_f] or ['   nenhuma se mexeu perto da casa.']
            if len(nf) - 1 - len(perto_f) > 0:
                R.append(f'   (+{len(nf) - 1 - len(perto_f)} facções de longe; no tick_{dia}.txt)')
        if nucleo.camada('guildas') and os.path.exists(P('guildas.py')):
            # G12 (Dia 433, pedido do jogador): as seis guildas do mundo, com chefe, agem toda semana
            C.append('   [15c] AS GUILDAS DO MUNDO (guildas.py semana, G12):')
            ng, _, err = roda('guildas.py', 'semana', dia)
            C += ['    ' + l for l in ng] or [f'      (falhou: {err})']
            R.append('  AS GUILDAS DO MUNDO (G12):')
            R += [l if len(l) < 330 else l[:330] for l in ng[1:]] or [f'   (falhou: {err})']
        # MOTOR 9.1 (438, pedido do jogador): os ÉDITOS (G27) e as CRIAS (G25) andam sozinhos na semana
        for _scr, _rot in (('edito.py', '[15d] O CÓDIGO DE IREVIEL (edito.py semana, G27):'), ('cria.py', '[15e] AS CRIAS E MONTARIAS (cria.py semana, G25):')):
            if os.path.exists(P(_scr)):
                C.append('   ' + _rot)
                _n, _, err = roda(_scr, 'semana', dia)
                C += ['    ' + l for l in _n] or [f'      (falhou: {err})']
                R += ['  ' + l for l in _n if l.strip().startswith(('ÉDITO', '★', '⚠', 'À MÃO', 'CRIA'))]
        if os.path.exists(P('tratados.json')):
            C.append('   [15b] OS TRATADOS (tratados.py semana):')
            ntr, _, err = roda('tratados.py', 'semana', dia)
            C += ['    ' + l for l in ntr]
            R += ntr
        if os.path.exists(P('rotina.json')):
            C.append('   [16] A ROTINA DE DADOS DA SEMANA (rotina.json, pelo selo: declarada e rolada):')
            n4, _, err = roda('rotina.py', 'semana', dia)
            C += ['      ' + l for l in n4] or [f'      (falhou: {err})']
            R.append('  A ROTINA DA SEMANA:')
            R += ['    ' + l for l in n4 if l.startswith('ROLADO')] or [f'    (falhou: {err})']
        C.append('   [17] O LIVRO DA SEMANA (ficha.py semana):')
        n5, _, err = roda('ficha.py', 'semana', dia, f'cidades={cidades}')
        C += ['      ' + l for l in n5] or [f'      (falhou: {err})']
        R += ['  ' + l for l in n5]
        R.append('  ' + A_MAO)
        t['primeiro_tick_semanal'] = dia + 7
    pa = t.setdefault('proxima_auditoria', dia + 5)
    if dia >= pa:
        C.append(f'  AUDITORIA (XXIII.23, Dia {dia}): relógios de facção/vilão/culto · ambições · comida e soldo · material · cobiça · pendentes do Envelope · prática · Revés e Fortuna · o que ficou para trás')
        C.append('  AUDITORIA — CONFERIR SOZINHO (regra da casa do Dia 199): toda Obra dos últimos 5 dias (LEI DO VALOR: a soma de valores e os dados anotados? obra_valor.py) · XP de Ferir somado de novo do zero · npcs.json (todos lançados?) · estado_vivo.md bate com o diário? · relógios e pendentes · erro achado = corrigir e anotar (regra 14)')
        n6, _, err = roda('conferidor.py', dia)
        C += ['    ' + l for l in n6]
        avisos = [l for l in n6 if l.startswith('⚠')]
        R.append(f'  AUDITORIA do Dia {dia}: ' + (f'{len(avisos)} avisos novos do conferidor' if avisos else 'o conferidor não achou nada novo') + ' · no REGISTRO: 1 coisa esquecida e 1 sistema ajustado')
        R += ['    ' + l for l in avisos[:8]]
        t['proxima_auditoria'] = dia + 5
    ag, par = agenda_linhas(dia, rs.get('outras_noticias_max', 8))
    C += ag
    R += ag
    pcfg = cfg.get('paradas', {})
    if pcfg.get('agenda', True):
        paradas += par
    F = carrega('ficha.json')
    if F and F.get('cofre', 0) < 0 and pcfg.get('cofre_negativo', True):
        paradas.append(f"o cofre está negativo ({F['cofre']})")
    grava(ARQ, e)
    # a saída inteira fica em tick_N.txt (a não ser que alguém já esteja mandando a saída para um arquivo)
    try:
        import stat
        redir = stat.S_ISREG(os.fstat(sys.stdout.fileno()).st_mode)
    except Exception:
        redir = False
    if not redir:
        with open(P(f'tick_{dia}.txt'), 'w', encoding='utf-8') as fh:
            fh.write('\n'.join(C) + '\n')
    return dict(dia=dia, cru=C, resumo=R, paradas=paradas, semanal=semanal)


def status():
    t = carrega(ARQ)['tempo']
    L = t.get('limiar_pressao', 10)
    print(f"Dia {t['dia']}, {t['hora']} · Pressão {t['pressao']}/{L} · próximo Tick semanal: Dia {t['primeiro_tick_semanal']} · próxima auditoria: Dia {t.get('proxima_auditoria', '?')}")


def main():
    a = sys.argv[1:]
    if not a or a[0] == 'status':
        status()
        return
    estrada = 'estrada' in a or 'segura' in a
    limite = 3 if 'estrada' in a else 2
    if a[0] == 'dia':
        r = um_dia(estrada, limite)
        print('\n'.join(r['cru']))
        for p in r['paradas']:
            print(f'  ■ PARADA: {p}')
    elif a[0] in ('bloco', 'ate'):
        if len(a) < 2 or not a[1].isdigit():
            sys.exit('uso: tick.py bloco N   ou   tick.py ate DIA')
        hoje = carrega(ARQ)['tempo']['dia']
        n = int(a[1]) if a[0] == 'bloco' else int(a[1]) - hoje
        if n <= 0:
            sys.exit(f'nada a rodar: o relógio já está no Dia {hoje}.')
        if n > 60:
            sys.exit('bloco grande demais (máximo 60 dias por chamada).')
        feitos = 0
        for _ in range(n):
            r = um_dia(estrada, limite)
            feitos += 1
            curto = 'resumo' in a or (nucleo.motor().get('detalhe', 'completo') == 'resumo' and 'completo' not in a)
            print('\n'.join(r['resumo'] if curto else r['cru']))
            if r['paradas']:
                print(f"■ PARADA NO DIA {r['dia']} (rodados {feitos} de {n} dias):")
                for p in r['paradas']:
                    print('   ' + p)
                break
        else:
            print(f'— bloco inteiro: {feitos} dias, sem parada. O relógio está no Dia {hoje + feitos}. —')
        print(f'(a saída inteira de cada dia está em tick_N.txt; próxima semana: Dia {carrega(ARQ)["tempo"]["primeiro_tick_semanal"]})')
    elif a[0] == 'pula':
        if len(a) < 2 or not a[1].isdigit():
            sys.exit('uso: tick.py pula DIA "motivo"')
        e = carrega(ARQ)
        t = e['tempo']
        alvo = int(a[1])
        if alvo <= t['dia']:
            sys.exit(f"o relógio já está no Dia {t['dia']}.")
        if alvo >= t['primeiro_tick_semanal']:
            sys.exit(f"não pulo por cima do tick semanal (Dia {t['primeiro_tick_semanal']}): rode os dias.")
        pulados = alvo - t['dia']
        t['pressao'] = min(t['pressao'] + pulados, t.get('limiar_pressao', 10) - 1)
        t['dia'] = alvo
        grava(ARQ, e)
        motivo = a[2] if len(a) > 2 else 'dia narrado à mão'
        nucleo.anota(f'- RELÓGIO ACERTADO SEM ROLAR [{agora()[:5]}]: o tick pulou para o Dia {alvo} ({motivo}); {pulados} dia(s) sem dados de mundo.')
        print(f'relógio no Dia {alvo}, sem rolar ({motivo}). Anotado no envelope.')
    else:
        sys.exit(__doc__)


if __name__ == '__main__':
    main()
