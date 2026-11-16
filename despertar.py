#!/usr/bin/env python3
"""despertar.py — G26, O DESPERTAR (Livro Nove 4; MOTOR 9.1, Dia 438): os Dons dos níveis 100, 200 e 300 para todos.

  Nos níveis 100, 200 e 300 a pessoa desperta e toma UM DOM (não troca mais). No 200 pode tomar outro ou o SEGUNDO GRAU do mesmo
  (o número dobra; o preço também). No 300 o Dom ganha NOME PRÓPRIO e entra nas canções (o Mestre dá o nome na primeira cena).
  O REI escolhe (o jogador). NPC recebe NO DADO (d12, declarado no envelope pelo selo; o de fora da casa vai OCULTO).
  Leitura do Mestre para o dado (438): saiu um Dom que a pessoa já tem → o SEGUNDO GRAU dele; já no segundo grau → o seguinte da lista.
  O que os Dons fazem na luta, o luta.py lê de "doms" na ficha de combate (Segundo Coração, Voz de Mando, Passo Certo, Pele do Mundo,
  Fôlego Sem Fundo); o resto o Mestre aplica na cena.

Uso:
  python3 despertar.py ver [NOME]            os Dons de quem já despertou
  python3 despertar.py devidos               quem passou do 100, 200 ou 300 e ainda não tem o Dom
  python3 despertar.py rola todos|casa|NOME,NOME   rola no selo os Dons devidos (um selo por pessoa; d12 por marco)
  python3 despertar.py dom NOME "Dom" [marco=100] [essencia=X]   grava um Dom escolhido (o rei, ou um NPC que escolheu em cena)
  python3 despertar.py nome NOME "o nome próprio"                o Dom do 300 ganha nome (cena)
"""
import json, sys
from nucleo import carrega, grava, anota, dia_atual, sem_acento

ARQ = 'despertares.json'
DONS = [   # Livro Nove 4, na ordem do d12
 ('Segundo Coração', '1x por dia, ao cair a 0 PV fica com 1 e age na vez dele', 'depois da cena fica Exausto até dormir'),
 ('Mão do Mundo', '+2 em toda obra de ofício', 'a marca é cobiçada: +1 na Cobiça de toda peça Épica ou acima que fizer'),
 ('Olho Aberto', 'vê magia ativa e sente mentira grossa sem teste', 'não descansa direito: recupera um quarto a menos de PV por noite'),
 ('Sangue Grosso', 'Sangue e Osso cobram a metade do PV', 'cura de Luz rende a metade nele'),
 ('Voz de Mando', 'aliados a 30 m têm +1 no ataque e +2 na moral', 'se ele cai, a tropa testa moral com −4'),
 ('Pele do Mundo', 'RD +5 contra uma Essência escolhida', 'o dano da Essência oposta soma +1 dado contra ele'),
 ('Fôlego Sem Fundo', 'Estamina e Mana máximas +25%', 'come por dois: sem ração dobrada, perde o Dom naquele dia'),
 ('Sorte Velha', 'Fortuna máxima +1', 'o Limiar de Revés cai 1'),
 ('Nome que Anda', 'a reputação começa em +10 em todo lugar novo', 'os inimigos também ouviram: um rival a mais no mundo'),
 ('Mão que Doma', '+1 no teto de servos e de crias; os laços com eles duram o dobro', 'sente a morte de cada um deles (Atordoado 1 rodada quando um cai)'),
 ('Passo Certo', 'nunca é surpreendido; +2 na Iniciativa', 'dorme leve: qualquer barulho o acorda (não recupera Estamina inteira em acampamento)'),
 ('Memória de Rei', 'um talento a mais, agora', 'o próximo talento por nível atrasa 10 níveis'),
]
NOMES = [x[0] for x in DONS]
ESS = ['Fogo', 'Gelo', 'Vento', 'Terra', 'Água', 'Raio', 'Vida', 'Podridão', 'Sangue', 'Sombra', 'Luz', 'Som', 'Silêncio', 'Mente', 'Tempo', 'Peso', 'Sal', 'Força', 'Veneno', 'Sorte', 'Elo', 'Metal', 'Fome', 'Espinho']
CASA_EXTRA = {'Fabaino'}   # gente da casa sem ficha de combate


def pessoas():
    """todo mundo de nível 100 para cima que é GENTE: os NPCs vivos, os Lendários e acima, os chefes e membros das guildas e os vilões"""
    P = {}; N = carrega('npcs.json', {}); V = carrega('mundo_vivo.json', {}); F = carrega('ficha.json', {})
    casa = set(carrega('fichas_combate.json', {'fichas': {}})['fichas']) | CASA_EXTRA
    for k, v in N.items():
        if 'MORT' in str(v.get('estado', '')).upper() or not isinstance(v.get('nivel'), int): continue
        if k in ('Zyza',) or 'servo armado' in str(v.get('classe', '')): continue   # monstro erguido: não desperta
        if v['nivel'] >= 100: P[k] = dict(nivel=v['nivel'], de='npcs', casa=k in casa)
    for l in V.get('lendarios', []):
        n = l['nome'].split(',')[0]
        if 'MORT' in str(l.get('estado', '')).upper(): continue
        if n not in P and isinstance(l.get('nivel'), int): P[n] = dict(nivel=l['nivel'], de='lendarios', casa=False)
    for g in V.get('guildas', []):
        for p in [g['chefe']] + g.get('membros', []):
            if isinstance(p.get('nivel'), int) and p['nivel'] >= 100 and p['nome'] not in P: P[p['nome']] = dict(nivel=p['nivel'], de='guilda: ' + g['nome'], casa=False)
    for v in V.get('viloes', []):
        if isinstance(v.get('nivel'), int) and v['nivel'] >= 100 and v['nome'] not in P and 'MORT' not in str(v.get('estado', '')).upper(): P[v['nome']] = dict(nivel=v['nivel'], de='vilões', casa=False)
    if F: P[F['nome']] = dict(nivel=F['nivel'], de='o rei', casa=True, rei=True)
    return P


def marcos(nv): return [m for m in (100, 200, 300) if nv >= m]


def devidos(S, P):
    out = {}
    for k, p in P.items():
        tem = [d['marco'] for d in S.get(k, {}).get('doms', [])]
        falta = [m for m in marcos(p['nivel']) if m not in tem]
        if falta: out[k] = falta
    return out


def aplica(S, k, nv, marco, idx, essencia=None, oculto=False, como='dado'):
    e = S.setdefault(k, {'nivel': nv, 'doms': [], 'oculto': oculto}); e['nivel'] = nv
    ja = {d['dom']: d for d in e['doms']}
    nome = NOMES[idx]; nota = ''
    while nome in ja and ja[nome]['grau'] >= 2:   # leitura do Mestre: no segundo grau, vale o seguinte da lista
        idx = (idx + 1) % 12; nome = NOMES[idx]; nota = ' (o que saiu já estava no 2º grau: vale o seguinte)'
    if nome in ja and como == 'dado':
        ja[nome]['grau'] = 2; ja[nome]['marco2'] = marco; ja[nome].setdefault('marcos', [ja[nome]['marco']]).append(marco)
        e['doms'].append({'dom': nome, 'grau': 2, 'marco': marco, 'repete': True})
        return f"{nome} (2º GRAU: o número dobra, o preço também){nota}"
    d = {'dom': nome, 'grau': 1, 'marco': marco, 'efeito': DONS[idx][1], 'preco': DONS[idx][2]}
    if nome == 'Pele do Mundo': d['essencia'] = essencia
    if marco == 300: d['nome_proprio'] = 'a dar na primeira cena (Livro Nove 4: no 300 o Dom ganha nome)'
    e['doms'].append(d)
    return nome + (f" (contra {essencia})" if essencia else '') + nota


def resumo(e):
    vis = {}
    for d in e['doms']:
        if d.get('repete'): continue
        vis[d['dom']] = d
    out = []
    for d in vis.values():
        g = max([x['grau'] for x in e['doms'] if x['dom'] == d['dom']])
        out.append(d['dom'] + (' (2º grau)' if g >= 2 else '') + (f" [{d['essencia']}]" if d.get('essencia') else '') + (f" «{d['nome_proprio']}»" if d.get('nome_proprio') and not d['nome_proprio'].startswith('a dar') else ''))
    return ' · '.join(out)


def poe_na_ficha(k, e):
    """os Dons que o luta.py lê vão para a ficha de combate (G9)"""
    R = carrega('fichas_combate.json', {'fichas': {}})
    if k not in R['fichas']: return
    f = R['fichas'][k]; f['doms'] = sorted({d['dom'] for d in e['doms']})
    pe = next((d.get('essencia') for d in e['doms'] if d['dom'] == 'Pele do Mundo' and d.get('essencia')), None)
    if pe: f['pele_essencia'] = pe
    g2 = [d['dom'] for d in e['doms'] if d.get('repete')]
    if g2: f['doms_grau2'] = sorted(set(g2))
    grava('fichas_combate.json', R)


def main():
    a = sys.argv[1:]; S = carrega(ARQ, {}); P = pessoas()
    if not a or a[0] == 'ver':
        if not a: print(__doc__)
        alvo = a[1] if len(a) > 1 else None
        for k, e in sorted(S.items(), key=lambda kv: -kv[1].get('nivel', 0)):
            if k == '_nota' or (alvo and sem_acento(alvo) not in sem_acento(k)): continue
            print(f"  {k} ({e.get('nivel')}){' [OCULTO]' if e.get('oculto') else ''}: {resumo(e)}")
        if not S: print('  ninguém despertou ainda no livro.')
        return
    if a[0] == 'devidos':
        D = devidos(S, P)
        for k, f in sorted(D.items(), key=lambda kv: -P[kv[0]]['nivel']): print(f"  {k} ({P[k]['nivel']}, {P[k]['de']}){' · DA CASA' if P[k]['casa'] else ''}: falta o Dom do {', '.join(map(str, f))}")
        print(f'{len(D)} pessoas com Despertar devido.'); return
    if a[0] == 'rola' and len(a) > 1:
        D = devidos(S, P)
        if a[1] == 'todos': quem = [k for k in D if not P[k].get('rei')]
        elif a[1] == 'casa': quem = [k for k in D if P[k]['casa'] and not P[k].get('rei')]
        else: quem = [x.strip() for x in a[1].split(',') if x.strip()]
        quem = [k for k in quem if k in D]
        if not quem: sys.exit('ninguém com Despertar devido nessa lista. (despertar.py devidos)')
        if any(P[k].get('rei') for k in quem): sys.exit('o Dom do REI é escolha do jogador: despertar.py dom Ferir "Dom"')
        import selo
        Z = selo.load(); tab = ' | '.join(f'{i + 1}: {n}' for i, n in enumerate(NOMES)); lin = []
        for k in sorted(quem, key=lambda x: -P[x]['nivel']):
            p = P[k]; f = D[k]; oc = not p['casa']
            sid = selo.declara(Z, '-', f"O DESPERTAR (G26) de {k} ({p['nivel']}; {p['de']}): o Dom do " + ', do '.join(map(str, f)) + ' (repetido: 2º grau; repetido no 2º grau: o seguinte da lista)', 'd12', tab,
                               selo.opcoes((['oculto'] if oc else []) + ([f'x={len(f)}', 'nomes=' + ','.join(f'o {m}' for m in f)] if len(f) > 1 else [])), quieto=True)
            rs = selo.rola(Z, sid, quieto=True)['rolagens']; out = []
            for m, r in zip(f, rs):
                ess = None
                if NOMES[r['total'] - 1] == 'Pele do Mundo':
                    s2 = selo.declara(Z, '-', f"A PELE DO MUNDO de {k}: contra qual Essência", 'd24', ' | '.join(f'{i + 1}: {x}' for i, x in enumerate(ESS)), selo.opcoes(['oculto'] if oc else []), quieto=True)
                    ess = ESS[selo.rola(Z, s2, quieto=True)['rolagens'][-1]['total'] - 1]
                out.append(f"o {m}: [{r['total']}] " + aplica(S, k, p['nivel'], m, r['total'] - 1, ess, oc))
            lin.append(f"{k} ({p['nivel']}){' [OCULTO]' if oc else ''}: " + ' · '.join(out))
            if p['de'] == 'npcs':
                N = carrega('npcs.json'); N[k]['despertar'] = resumo(S[k]); grava('npcs.json', N)
            if p['casa']: poe_na_ficha(k, S[k])
        grava(ARQ, S)
        anota('- O DESPERTAR (G26) [Dia %d], %d pessoas (os selos acima): ' % (dia_atual(), len(lin)) + ' ‖ '.join(lin))
        for l in lin: print('  ' + l)
        return
    if a[0] == 'dom' and len(a) >= 3:
        k = a[1]; nm = next((n for n in NOMES if sem_acento(n) == sem_acento(a[2])), None) or sys.exit('Dom fora do Livro Nove 4: ' + ', '.join(NOMES))
        marco = int(next((x[6:] for x in a if x.startswith('marco=')), 100)); ess = next((x[9:] for x in a if x.startswith('essencia=')), None)
        p = P.get(k) or sys.exit(f'{k}: não achei (nível 100 ou mais).')
        txt = aplica(S, k, p['nivel'], marco, NOMES.index(nm), ess, oculto=not p['casa'], como='escolha'); grava(ARQ, S)
        if p['de'] == 'npcs': N = carrega('npcs.json'); N[k]['despertar'] = resumo(S[k]); grava('npcs.json', N)
        if p['casa']: poe_na_ficha(k, S[k])
        anota(f"- O DESPERTAR (G26) [Dia {dia_atual()}]: {k} toma {txt} (o Dom do {marco}; escolha)"); print(f'{k}: {txt}'); return
    if a[0] == 'nome' and len(a) >= 3:
        e = S.get(a[1]) or sys.exit('sem Despertar no livro.')
        d = next((x for x in e['doms'] if x['marco'] == 300 and not x.get('repete')), None) or next((x for x in e['doms'] if x['marco'] == 300), None) or sys.exit('ainda não tem o Dom do 300.')
        alvo = next(x for x in e['doms'] if x['dom'] == d['dom'] and not x.get('repete')); alvo['nome_proprio'] = a[2]; grava(ARQ, S)
        anota(f"- O DESPERTAR (G26): o Dom de {a[1]} ganha nome: «{a[2]}»"); print('gravado.'); return
    print(__doc__)


if __name__ == '__main__':
    main()
