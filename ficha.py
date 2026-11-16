#!/usr/bin/env python3
"""ficha.py — a ficha de Ferir e o cofre num lugar só (MOTOR 6): ficha.json.

Antes o XP, o nível, os atributos e o cofre viviam em frases do estado_vivo.md e do envelope, e o Mestre
fazia a conta de cabeça (o conferidor já pegou cofre diferente nos dois). Agora a conta é do script:
o XP sobe o nível sozinho, os atributos acompanham e o cofre tem livro-caixa.

Uso:
  python3 ficha.py ver                         a ficha curta (para o 📊 ESTADO)
  python3 ficha.py xp QTD "motivo"             soma XP; se passar do limiar, SOBE e mostra a tabela
  python3 ficha.py cofre +N|-N "motivo"        mexe no cofre e lança no livro
  python3 ficha.py mat NOME +KG|-KG "motivo"   material (kg); cria o material se não existir
  python3 ficha.py pv -N | mana -N | fortuna -1 | reves +1      (ou "cheio" para voltar ao máximo)
  python3 ficha.py set CAMPO VALOR "motivo"    conserto à mão (ex.: set atributos.Sorte 96)
  python3 ficha.py livro                       as últimas linhas do livro-caixa
  python3 ficha.py semana DIA [cidades=N]      lança a semana: renda da casa + cidades − despesa (o tick chama sozinho)
  python3 ficha.py fixo renda_casa|despesa N "motivo"    muda o valor fixo da semana
  python3 ficha.py recurso "NOME" MAX [dia|cena|semana]   cria um recurso contado (a Visão do Tempo 2 por dia; os usos de uma peça)
  python3 ficha.py usa "NOME" [N]                         gasta (recusa se não há); os de "dia" voltam sozinhos no tick
  python3 ficha.py volta "NOME"                           enche de novo (fim de cena)

Regras que o script segue (tiradas do save, não inventadas):
  o nível N+1 chega em 50 × N × (N+1) + 100 de XP total (o 77 em 292.700; o 144 em 1.029.700)
  cada nível: Inteligência +1 · Afinidade +1 · PV +2 · Mana +1 (visto do 105 ao 143) · Foco +1 a cada 5 níveis
  ações por rodada = 1 + nível ÷ 60 · ponto de habilidade a cada 3 níveis · talento a cada 10
"""
import sys
from nucleo import carrega, grava, dia_atual, anota, agora

ARQ = 'ficha.json'


def limiar(n):
    """XP total para chegar ao nível n+1"""
    return 50 * n * (n + 1) + 100


def br(n):
    return f'{int(n):,}'.replace(',', '.')


def load():
    F = carrega(ARQ)
    if not F:
        sys.exit('ficha.json não existe.')
    return F


def acoes(n):
    return max(1, min(8, 1 + n // 60))


def ver(F):
    a = F['atributos']
    print(f"FERIR · nível {F['nivel']} · XP {br(F['xp'])} / {br(limiar(F['nivel']))} (faltam {br(limiar(F['nivel']) - F['xp'])})")
    print(f"  Int {a['Inteligência']} · Afinidade {a['Afinidade']} · PV {F['pv'][0]}/{F['pv'][1]} · Mana {F['mana'][0]}/{F['mana'][1]} · "
          f"Foco {F['foco']} · {acoes(F['nivel'])} ações · Fortuna {F['fortuna'][0]}/{F['fortuna'][1]} · Revés {F['reves'][0]}/{F['reves'][1]}" + (f" · Fama {F['fama']}/7" if 'fama' in F else ''))
    print('  ' + ' · '.join(f'{k} {v}' for k, v in a.items() if k not in ('Inteligência', 'Afinidade')))
    print(f"  COFRE {br(F['cofre'])} · semana fixa: +{br(F['livro']['renda_casa'])} da casa − {br(F['livro']['despesa'])} de despesa (+ as cidades)")
    if F.get('materiais'):
        print('  MATERIAL: ' + ' · '.join(f"{k} ~{v['kg']:g} kg" for k, v in F['materiais'].items()))
    if F.get('recursos'):
        print('  RECURSOS: ' + ' · '.join(f"{k} {v['tem']}/{v['max']} (por {v['renova']})" for k, v in F['recursos'].items()))
    for av in F.get('avisos', []):
        print('  ⚠ ' + av)


def sobe(F, motivo):
    """aplica as subidas devidas; devolve as linhas da tabela"""
    out = []
    g = F['ganho_por_nivel']
    while F['xp'] >= limiar(F['nivel']):
        antes = dict(nivel=F['nivel'], Int=F['atributos']['Inteligência'], Afin=F['atributos']['Afinidade'],
                     pv=F['pv'][1], mana=F['mana'][1], foco=F['foco'], ac=acoes(F['nivel']))
        F['nivel'] += 1
        n = F['nivel']
        F['atributos']['Inteligência'] += g.get('Inteligência', 0)
        F['atributos']['Afinidade'] += g.get('Afinidade', 0)
        F['pv'] = [F['pv'][0] + g.get('pv', 0), F['pv'][1] + g.get('pv', 0)]
        F['mana'] = [F['mana'][0] + g.get('mana', 0), F['mana'][1] + g.get('mana', 0)]
        if n % 5 == 0:
            F['foco'] += 1
        out.append(f'⬆ SUBIU AO NÍVEL {n} ({motivo})')
        out.append('  | | antes | agora |')
        out.append('  |---|---|---|')
        out.append(f"  | Inteligência | {antes['Int']} | {F['atributos']['Inteligência']} |")
        out.append(f"  | Afinidade | {antes['Afin']} | {F['atributos']['Afinidade']} |")
        out.append(f"  | PV máximo | {antes['pv']} | {F['pv'][1]} |")
        out.append(f"  | Mana máxima | {antes['mana']} | {F['mana'][1]} |")
        if F['foco'] != antes['foco']:
            out.append(f"  | Foco | {antes['foco']} | {F['foco']} |")
        if acoes(n) != antes['ac']:
            out.append(f"  | Ações por rodada | {antes['ac']} | {acoes(n)} |")
        out.append(f'  próximo nível em {br(limiar(n))} XP')
        if n % 3 == 0:
            out.append(f'  ★ PONTO DE HABILIDADE do {n}: o jogador escolhe (ou o Mestre propõe)')
        if n % 10 == 0:
            out.append(f'  ★ TALENTO do {n}: o jogador escolhe')
        for marco in F.get('marcos_de_nivel', []):
            if marco['nivel'] == n:
                out.append(f"  ★ MARCO DO {n}: {marco['texto']}")
        F.setdefault('xp_log', []).append(f'Dia {dia_atual()}: SOBE ao {n}')
    return out


def campo(F, caminho):
    partes = caminho.split('.')
    alvo = F
    for p in partes[:-1]:
        alvo = alvo[p]
    return alvo, partes[-1]


def main():
    a = sys.argv[1:]
    F = load()
    if not a or a[0] == 'ver':
        ver(F)
        return
    c = a[0]
    dia = dia_atual()
    if c == 'xp':
        q = int(a[1].replace('.', ''))
        motivo = a[2] if len(a) > 2 else ''
        F['xp'] += q
        F.setdefault('xp_log', []).append(f'Dia {dia}: +{q} {motivo}'.strip())
        F['xp_log'] = F['xp_log'][-60:]
        linhas = sobe(F, motivo)
        grava(ARQ, F)
        print(f"XP +{br(q)} ({motivo}) → {br(F['xp'])} / {br(limiar(F['nivel']))}")
        for l in linhas:
            print(l)
        anota(f"- FERIR [Dia {dia}]: XP +{br(q)} ({motivo}) → {br(F['xp'])}" + (f" → NÍVEL {F['nivel']}" if linhas else ''))
    elif c == 'cofre':
        q = int(a[1].replace('.', '').replace('+', ''))
        motivo = a[2] if len(a) > 2 else ''
        antes = F['cofre']
        F['cofre'] += q
        F.setdefault('livro_log', []).append({'dia': dia, 'valor': q, 'motivo': motivo, 'saldo': F['cofre']})
        F['livro_log'] = F['livro_log'][-120:]
        grava(ARQ, F)
        print(f"COFRE {br(antes)} {q:+,d} ({motivo}) → {br(F['cofre'])}".replace(',', '.'))
        if F['cofre'] < 0:
            print('⚠ O COFRE FICOU NEGATIVO: a Intendente precisa saber (dívida, venda ou corte).')
        anota(f"- COFRE [Dia {dia}]: {br(antes)} {'+' if q >= 0 else '−'} {br(abs(q))} ({motivo}) → **{br(F['cofre'])}**")
    elif c == 'mat':
        nome = a[1].lower()
        q = float(a[2].replace(',', '.').replace('+', ''))
        motivo = a[3] if len(a) > 3 else ''
        m = F.setdefault('materiais', {}).setdefault(nome, {'kg': 0.0, 'log': []})
        if m['kg'] + q < -1e-9:
            sys.exit(f"NÃO HÁ {nome} que chegue: tem ~{m['kg']:g} kg e a obra pede {abs(q):g} kg. Nada mudou.")
        m['kg'] = round(m['kg'] + q, 3)
        m.setdefault('log', []).append(f'Dia {dia}: {q:+g} {motivo}'.strip())
        m['log'] = m['log'][-12:]
        grava(ARQ, F)
        print(f"{nome}: {q:+g} kg ({motivo}) → ~{m['kg']:g} kg")
        anota(f"- MATERIAL [Dia {dia}]: {nome} {q:+g} kg ({motivo}) → ~{m['kg']:g} kg")
    elif c in ('pv', 'mana', 'fortuna', 'reves'):
        par = F[c]
        if a[1] == 'cheio':
            par[0] = par[1] if c != 'reves' else 0
        else:
            par[0] = max(0, par[0] + int(a[1].replace('+', '')))
            if c != 'reves':
                par[0] = min(par[0], par[1])
        grava(ARQ, F)
        print(f'{c}: {par[0]}/{par[1]}')
        if c == 'pv' and par[0] == 0:
            print('⚠ PV 0: modo de morte REALISTA (teste de morte).')
        if c == 'reves' and par[0] >= par[1]:
            print('⚠ REVÉS NO LIMIAR: rolar a Tabela de Revés.')
    elif c == 'set':
        alvo, k = campo(F, a[1])
        velho = alvo.get(k)
        v = a[2]
        try:
            v = int(v)
        except ValueError:
            try:
                v = float(v)
            except ValueError:
                pass
        alvo[k] = v
        grava(ARQ, F)
        print(f'{a[1]}: {velho} → {v}' + (f' ({a[3]})' if len(a) > 3 else ''))
        anota(f"- FICHA [Dia {dia}]: {a[1]} {velho} → {v}" + (f' ({a[3]})' if len(a) > 3 else ''))
    elif c == 'livro':
        for l in F.get('livro_log', [])[-15:]:
            print(f"Dia {l['dia']}: {l['valor']:+d} {l['motivo']} → {br(l['saldo'])}")
        if not F.get('livro_log'):
            print('o livro-caixa ainda não tem lançamento (o cofre de partida veio do save do Dia 379).')
    elif c == 'semana':
        d = int(a[1])
        cid = next((int(x[8:]) for x in a[2:] if x.startswith('cidades=')), 0)
        if F['livro'].get('ultima_semana') == d:
            print(f'a semana do {d} já foi lançada no livro.')
            return
        L = F['livro']
        saldo = L['renda_casa'] + cid - L['despesa']
        antes = F['cofre']
        F['cofre'] += saldo
        L['ultima_semana'] = d
        F.setdefault('livro_log', []).append({'dia': d, 'valor': saldo, 'motivo': f"semana: casa {L['renda_casa']} + cidades {cid} − despesa {L['despesa']}", 'saldo': F['cofre']})
        grava(ARQ, F)
        print(f"LIVRO {d}: {br(L['renda_casa'])} + {br(cid)} − {br(L['despesa'])} = {saldo:+d} · COFRE {br(antes)} → {br(F['cofre'])}")
        if L.get('nota'):
            print('  lembrar: ' + L['nota'])
        if F['cofre'] < 0:
            print('  ⚠ O COFRE FICOU NEGATIVO.')
        elif saldo < 0 and F['cofre'] / -saldo < 12:
            print(f"  ⚠ neste passo o cofre dura {F['cofre'] // -saldo} semanas.")
        anota(f"- LIVRO {d}: {br(L['renda_casa'])} + {br(cid)} − {br(L['despesa'])} = {saldo:+d} · COFRE {br(antes)} → **{br(F['cofre'])}**")
    elif c == 'recurso' and len(a) > 2:
        F.setdefault('recursos', {})[a[1]] = {'tem': int(a[2]), 'max': int(a[2]), 'renova': a[3] if len(a) > 3 else 'dia'}
        grava(ARQ, F); print(f"recurso criado: {a[1]} {a[2]}/{a[2]} (por {F['recursos'][a[1]]['renova']})")
    elif c in ('usa', 'volta') and len(a) > 1:
        from nucleo import acha_nome
        k, sug = acha_nome(a[1], F.get('recursos', {}))
        if not k: sys.exit(f'recurso não achado: {a[1]}. Existem: {", ".join(F.get("recursos", {}))}')
        r = F['recursos'][k]
        if c == 'volta': r['tem'] = r['max']
        else:
            q = int(a[2]) if len(a) > 2 else 1
            if r['tem'] < q: sys.exit(f"NÃO HÁ: {k} está em {r['tem']}/{r['max']} (volta por {r['renova']}). Nada foi gasto.")
            r['tem'] -= q
        grava(ARQ, F); print(f"{k}: {r['tem']}/{r['max']}")
        if c == 'usa': anota(f"- RECURSO [Dia {dia}]: {k} usado → {r['tem']}/{r['max']}")
    elif c == 'fixo':
        if a[1] not in ('renda_casa', 'despesa'):
            sys.exit('uso: ficha.py fixo renda_casa|despesa N "motivo"')
        velho = F['livro'][a[1]]
        F['livro'][a[1]] = int(a[2].replace('.', ''))
        grava(ARQ, F)
        print(f"{a[1]} por semana: {br(velho)} → {br(F['livro'][a[1]])}" + (f' ({a[3]})' if len(a) > 3 else ''))
        anota(f"- LIVRO FIXO [Dia {dia}]: {a[1]} {br(velho)} → {br(F['livro'][a[1]])}" + (f' ({a[3]})' if len(a) > 3 else ''))
    else:
        sys.exit(__doc__)


if __name__ == '__main__':
    main()
