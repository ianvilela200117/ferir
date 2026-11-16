#!/usr/bin/env python3
"""cria.py — G25, CRIAS E MONTARIAS (Livro Nove 8.5; MOTOR 9.1, Dia 438).

Uma cria vem do traço "cria no ventre" (o luta.py avisa quando uma fica VIVA E RENDIDA), de um ninho de covil, de compra
rara ou do feitiço Chamar a Matilha (só Comuns). O script guarda as crias da casa (crias.json) e faz as contas do Livro:
  · CRESCE em UMA LUA POR DEGRAU do bicho (Comum 1 · Incomum 2 · Raro 3 · Épico 4 · Único 5 · Lendário 6 · Mítico 7);
    com o talento Criador de Feras do dono, um quarto mais rápido
  · COME por semana degrau × 20 de ouro em carne (entra na despesa fixa da semana: ficha.py fixo)
  · SEM LAÇO, ao crescer rola d6 (pelo selo): 1-3 foge ou ataca · 4-6 fica
  · ADULTA tem METADE do nível do bicho que a pôs e sobe com XP, como um NPC da casa, até o nível do pai
  · TETO: uma cria por 100 níveis do dono (mínimo 1); o Dom Mão que Doma soma 1; a Ninhada (Senhor de Feras) dobra
  · FERA EM CIDADE: solta, Ordem −2 naquela semana; presa e mostrada, +5 de reputação na cidade, uma vez

Uso:
  python3 cria.py ver
  python3 cria.py nova NOME "PAI" CATEGORIA NIVEL_DO_PAI ESSENCIA [dono=Ferir] [tamanho=cavalo] [traco="..."] [poder="..."] [laco="..."] [de="de onde veio"] [teto=N]
  python3 cria.py laco NOME "Elo de Montaria renovado | Laço de Servo | Domar | classe Domador..."   (laco "" tira)
  python3 cria.py xp NOME QTD "motivo"          XP da adulta (100 × nível por nível, como os NPCs)
  python3 cria.py ficha NOME                     a ficha de combate dela (para o combate.py nova / fichas_combate.json)
  python3 cria.py mostra NOME "Cidade (a cidade)"   presa e mostrada: +5 de reputação, uma vez por cria
  python3 cria.py solta NOME CIDADE              andou solta na cidade: Ordem −2 nesta semana
  python3 cria.py estado NOME morta|fugiu|vendida "motivo"
  python3 cria.py semana DIA                     o tick semanal chama sozinho: quem cresce, quem foge, quanto comem
CATEGORIA sem acento: Comum Incomum Raro Epico Unico Lendario Mitico. NOME novo passa pelo nomes.py livre.
"""
import subprocess, sys
from nucleo import carrega, grava, anota, dia_atual, sem_acento, P

ARQ = 'crias.json'
CATS = ['Comum', 'Incomum', 'Raro', 'Epico', 'Unico', 'Lendario', 'Mitico', 'Primordial']
NOME_CAT = dict(zip(CATS, ['Comum', 'Incomum', 'Raro', 'Épico', 'Único', 'Lendário', 'Mítico', 'Primordial']))
PVMULT = {'Comum': 5, 'Incomum': 6, 'Raro': 8, 'Epico': 15, 'Unico': 20, 'Lendario': 25, 'Mitico': 100, 'Primordial': 300}
MULT = {'Comum': 1, 'Incomum': 1.5, 'Raro': 2.5, 'Epico': 5, 'Unico': 10, 'Lendario': 25, 'Mitico': 100, 'Primordial': 500}
BONUS = {'Comum': 2, 'Incomum': 4, 'Raro': 6, 'Epico': 10, 'Unico': 15, 'Lendario': 20, 'Mitico': 30, 'Primordial': 50}
RD = {'Comum': 0, 'Incomum': 1, 'Raro': 3, 'Epico': 6, 'Unico': 12, 'Lendario': 25, 'Mitico': 50, 'Primordial': 100}
DADO = {'homem': '1d8', 'cavalo': '1d10', 'casa': '1d12', 'torre': '2d10', 'colina': '3d10', 'montanha': '4d12'}
MONTA = ('cavalo', 'casa', 'torre', 'colina', 'montanha')


def roda(script, *args):
    r = subprocess.run([sys.executable, P(script)] + [str(x) for x in args], capture_output=True, text=True)
    out = (r.stdout + r.stderr).strip()
    if out: print('    ' + out.replace('\n', '\n    '))


def opt(a, k, padrao=None):
    return next((x[len(k) + 1:] for x in a if x.startswith(k + '=')), padrao)


def cat_de(txt):
    k = sem_acento(txt).capitalize()
    if k not in CATS: sys.exit(f'categoria que não conheço: "{txt}" (use {", ".join(CATS[:7])})')
    return k


def acha(S, nome):
    n = sem_acento(nome)
    c = [x for x in S['crias'] if sem_acento(x['nome']) == n] or [x for x in S['crias'] if n in sem_acento(x['nome'])]
    if len(c) != 1: sys.exit(f'cria não achada (ou ambígua): "{nome}" · ' + (', '.join(x['nome'] for x in S['crias']) or 'a casa não tem cria'))
    return c[0]


def teto_de(dono):
    """uma por 100 níveis do dono (mínimo 1); Mão que Doma +1; Ninhada (Senhor de Feras) dobra"""
    F = carrega('ficha.json', {}); H = carrega('habilidades.json', {}); N = carrega('npcs.json', {})
    if dono == F.get('nome'):
        nv = F.get('nivel', 1); tal = ' '.join(t.get('nome', '') for t in H.get('talentos', [])); classe = F.get('titulo', '')
        dom = 'Mão que Doma' in tal; criador = 'Criador de Feras' in tal
    else:
        v = N.get(dono, {}); nv = v.get('nivel') or 1; classe = str(v.get('classe', '')) + ' ' + str(v.get('classe_livro', ''))
        dom = 'Mão que Doma' in str(v.get('despertar', '')); criador = 'Criador de Feras' in str(v.get('talentos', ''))
    t = max(1, nv // 100) + (1 if dom else 0)
    if 'Senhor de Feras' in classe: t *= 2
    return t, criador, dom


def vivas(S, dono=None):
    return [c for c in S['crias'] if c['estado'] in ('filhote', 'adulta') and (dono is None or c['dono'] == dono)]


def linha(c, dia):
    grau = CATS.index(c['cat']) + 1
    base = f"{c['nome']} · cria de {c['pai']} ({NOME_CAT[c['cat']]}, {c['essencia']}) · dono: {c['dono']} · "
    if c['estado'] == 'filhote': base += f"FILHOTE: adulta no Dia {c['adulta_em']} (faltam {max(0, c['adulta_em'] - dia)} dias) · come {grau * 20} por semana"
    elif c['estado'] == 'adulta': base += f"ADULTA nível {c['nivel']} de {c['nivel_pai']} (XP {c.get('xp', 0)}/{100 * c['nivel']}) · come {grau * 20} por semana" + (' · MONTARIA' if c.get('tamanho') in MONTA else '')
    else: base += c['estado'].upper()
    return base + (f" · laço: {c['laco']}" if c.get('laco') else ' · ⚠ SEM LAÇO (ao crescer: d6 1-3 foge ou ataca)' if c['estado'] == 'filhote' else '') + (f" · traço: {c['traco']}" if c.get('traco') else '')


def ficha_combate(c):
    cat = c['cat']; nv = c['nivel'] if c['estado'] == 'adulta' else max(1, c['nivel_pai'] // 4)
    return dict(nome=c['nome'], nivel=nv, nivel_ref=nv, at=nv // 4 + BONUS[cat], df=10 + nv // 4 + BONUS[cat], rd=RD[cat], pv=nv * PVMULT[cat], dado=DADO.get(c.get('tamanho', 'cavalo'), '1d10'),
                mult=MULT[cat], b=0, essencia=c['essencia'], fica=True, pecas=f"CRIA de {c['pai']} ({NOME_CAT[cat]}, {c['essencia']}; G25)" + (f"; traço: {c['traco']}" if c.get('traco') else '') + (f"; poder: {c['poder']}" if c.get('poder') else ''))


def main():
    a = sys.argv[1:]; S = carrega(ARQ, {'nota': 'G25: as crias e montarias da casa (cria.py). estado: filhote → adulta (ou fugiu, morta, vendida).', 'crias': []})
    dia = dia_atual()
    if not a or a[0] == 'ver':
        if not a: print(__doc__)
        vs = vivas(S); print(f'CRIAS E MONTARIAS DA CASA (G25): {len(vs)}')
        for dono in sorted({c['dono'] for c in vs}): print(f'  teto de {dono}: {len(vivas(S, dono))} de {teto_de(dono)[0]}')
        for c in S['crias']: print('  ' + linha(c, dia))
        return
    cmd = a[0]
    if cmd == 'nova' and len(a) >= 6:
        nome, pai, cat, nvp, ess = a[1], a[2], cat_de(a[3]), int(a[4]), a[5]; dono = opt(a, 'dono', carrega('ficha.json', {}).get('nome', 'Ferir'))
        if any(sem_acento(c['nome']) == sem_acento(nome) for c in S['crias']): sys.exit(f'já existe uma cria chamada {nome}.')
        t, criador, _ = teto_de(dono); t = int(opt(a, 'teto', t)); tem = len(vivas(S, dono))
        if tem >= t: sys.exit(f'TETO: {dono} já tem {tem} cria(s) e o teto é {t} (uma por 100 níveis; Mão que Doma +1; Ninhada dobra). Nada foi criado.')
        grau = CATS.index(cat) + 1; dias = grau * 30
        if criador: dias = dias * 3 // 4
        c = {'nome': nome, 'pai': pai, 'cat': cat, 'nivel_pai': nvp, 'essencia': ess, 'dono': dono, 'tamanho': opt(a, 'tamanho', 'cavalo'), 'traco': opt(a, 'traco'), 'poder': opt(a, 'poder'),
             'laco': opt(a, 'laco'), 'de': opt(a, 'de', ''), 'nasceu': dia, 'adulta_em': dia + dias, 'estado': 'filhote', 'nivel': None, 'xp': 0, 'come': grau * 20}
        S['crias'].append(c); grava(ARQ, S)
        F = carrega('ficha.json'); roda('ficha.py', 'fixo', 'despesa', F['livro']['despesa'] + c['come'], f"a carne da cria {nome} (+{c['come']} por semana, G25)")
        anota(f"- CRIA (G25) [Dia {dia}]: {nome}, cria de {pai} ({NOME_CAT[cat]} {nvp}, {ess})" + (f", {c['de']}" if c['de'] else '') + f" · dono {dono} ({tem + 1} de {t}) · adulta no Dia {c['adulta_em']} (nível {nvp // 2}) · come {c['come']} por semana · laço: {c['laco'] or 'NENHUM AINDA'}")
        print('CRIA NOVA: ' + linha(c, dia))
        if not c['laco']: print('  ⚠ sem laço: até o Dia ' + str(c['adulta_em']) + ' o dono precisa de um (Elo de Montaria renovado, Laço de Servo, Domar, ou a classe Domador, Senhor de Feras, Cavaleiro de Elo): cria.py laco')
        return
    if cmd == 'semana':
        dia = int(a[1]) if len(a) > 1 else dia; mudou = False
        for c in vivas(S):
            if c['estado'] == 'filhote' and dia >= c['adulta_em']:
                mudou = True
                if not c.get('laco'):   # sem laço, foge ou ataca ao crescer (d6 1-3): pelo selo, declarado antes
                    import selo
                    Z = selo.load(); sid = selo.declara(Z, f"CR{dia}{sem_acento(c['nome'])[:6]}", f"A CRIA {c['nome'].upper()} CRESCE SEM LAÇO (G25)", 'd6', '1-3: FOGE OU ATACA (o Mestre lê pela cena) | 4-6: fica com o dono', selo.opcoes([]))
                    r = selo.rola(Z, sid)['rolagens'][-1]
                    if r['total'] <= 3:
                        c['estado'] = 'fugiu'; F = carrega('ficha.json'); roda('ficha.py', 'fixo', 'despesa', F['livro']['despesa'] - c['come'], f"a cria {c['nome']} fugiu (−{c['come']} por semana)")
                        print(f"  ⚠ CRIA {c['nome']}: cresceu SEM LAÇO e d6 [{r['total']}]: FOGE OU ATACA (cena)"); continue
                c['estado'] = 'adulta'; c['nivel'] = max(1, c['nivel_pai'] // 2)
                anota(f"- CRIA (G25) [Dia {dia}]: {c['nome']} está ADULTA: nível {c['nivel']} (metade de {c['nivel_pai']}); sobe com XP até {c['nivel_pai']}")
                print(f"  ★ CRIA {c['nome']} está ADULTA: nível {c['nivel']}" + (' · já carrega o dono (MONTARIA)' if c.get('tamanho') in MONTA else '') + ' · python3 cria.py ficha ' + c['nome'])
            elif c['estado'] == 'adulta':
                subiu = False
                while c['nivel'] < c['nivel_pai'] and c.get('xp', 0) >= 100 * c['nivel']: c['xp'] -= 100 * c['nivel']; c['nivel'] += 1; subiu = True; mudou = True
                if subiu: print(f"  CRIA {c['nome']} SOBE a {c['nivel']}")
        vs = vivas(S)
        if vs: print(f"  crias da casa: {len(vs)} · comem {sum(c['come'] for c in vs)} por semana (já na despesa fixa) · " + ' · '.join(f"{c['nome']} ({'adulta ' + str(c['nivel']) if c['estado'] == 'adulta' else 'filhote, adulta no ' + str(c['adulta_em'])}{'' if c.get('laco') else ', SEM LAÇO'})" for c in vs))
        else: print('  a casa não tem cria.')
        if mudou: grava(ARQ, S)
        return
    if len(a) < 2: sys.exit(__doc__)
    c = acha(S, a[1])
    if cmd == 'laco' and len(a) >= 3:
        c['laco'] = a[2] or None; grava(ARQ, S); anota(f"- CRIA (G25) [Dia {dia}]: {c['nome']}: laço: {a[2] or 'NENHUM'}"); print(linha(c, dia))
    elif cmd == 'xp' and len(a) >= 3:
        if c['estado'] != 'adulta': sys.exit('só a adulta ganha XP.')
        c['xp'] = c.get('xp', 0) + int(a[2]); grava(ARQ, S); print(f"{c['nome']}: +{a[2]} ({a[3] if len(a) > 3 else ''}) → {c['xp']}/{100 * c['nivel']} (sobe no tick semanal, até o nível {c['nivel_pai']})")
    elif cmd == 'ficha':
        import json
        f = ficha_combate(c); print(json.dumps({c['nome']: f}, ensure_ascii=False, indent=1))
        print(f"para pôr nas fichas: python3 combate.py nova {c['nome']} {f['nivel']} {f['at']} {f['df']} {f['rd']} {f['pv']} {f['dado']} {f['mult']} {f['b']}   (em luta entra como aliado; \"fica\": não recua)")
    elif cmd == 'mostra' and len(a) >= 3:
        if c.get('mostrada'): sys.exit(f"{c['nome']} já foi mostrada em {c['mostrada']} (vale uma vez).")
        c['mostrada'] = a[2]; grava(ARQ, S); roda('reputacao.py', 'muda', a[2], 5, f"a cria {c['nome']}, presa e mostrada: orgulho da cidade (G25)")
    elif cmd == 'solta' and len(a) >= 3:
        roda('reino.py', 'mod', a[2], 'Ordem', -2, f"a cria {c['nome']} andou solta na cidade (G25; até o {dia + 6})")
    elif cmd == 'estado' and len(a) >= 3:
        if c['estado'] in ('filhote', 'adulta'):
            F = carrega('ficha.json'); roda('ficha.py', 'fixo', 'despesa', F['livro']['despesa'] - c['come'], f"a cria {c['nome']}: {a[2]} (−{c['come']} por semana)")
        c['estado'] = a[2]; grava(ARQ, S); anota(f"- CRIA (G25) [Dia {dia}]: {c['nome']}: {a[2]} ({a[3] if len(a) > 3 else ''})"); print(linha(c, dia))
    else: sys.exit(__doc__)


if __name__ == '__main__':
    main()
