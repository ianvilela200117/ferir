#!/usr/bin/env python3
"""tracos.py — MOTOR 7: PERSONALIDADE QUE PESA (traços em número, opinião sobre o rei, resistência social, voz).

Os traços saem do texto da ficha e viram lista. Cada traço empurra EIXOS (misericordia, rigor, risco, cautela,
gasto, poupar, honra, segredo, guerra, paz, tradicao, novidade, rei, povo, fe, saber). O Mestre marca os eixos
de cada opção e o script devolve as inclinações prontas para o conselho.py. Ninguém digita inclinação à mão.

Uso:
  python3 tracos.py migra                      tira os traços do texto de classe/ocupação e grava em npcs.json
  python3 tracos.py completa [N]               quem não tem traço ganha 2 pelo dado (anotado no envelope); N = quantos NPCs
  python3 tracos.py ver [NOME]                 traços, opinião e voz (sem nome: todos os que têm traço)
  python3 tracos.py cena NOME NOME ...         cartão denso para narrar: traços, opinião, voz, assinaturas da classe
  python3 tracos.py inclina A=misericordia,risco B=rigor,cautela [fora=Nome,Nome] [quem=Nome,Nome]
                                               devolve as inclinações do conselho para colar no conselho.py
  python3 tracos.py opiniao NOME +10 "motivo" [dias=60]     soma opinião sobre o rei (vence sozinha; sem dias, fica)
  python3 tracos.py opinioes                   a opinião de todos, da pior para a melhor
  python3 tracos.py resiste NOME EIXO          a resistência do NPC a um pedido nesse eixo (CD do teste social)
  python3 tracos.py traco NOME +TEIMOSO | -TEIMOSO "motivo"  traço ganho ou perdido pelo que o NPC viveu
  python3 tracos.py voz NOME "como ele fala"   a voz do NPC (o Mestre lê antes de pôr fala na boca dele)
  python3 tracos.py catalogo                   os traços e o que cada um empurra
"""
import re, sys
from nucleo import carrega, grava, anota, d, dia_atual, sem_acento

EIXOS = ['misericordia', 'rigor', 'risco', 'cautela', 'gasto', 'poupar', 'honra', 'segredo', 'guerra', 'paz',
         'tradicao', 'novidade', 'rei', 'povo', 'fe', 'saber']
CAT = {
 'LEAL': {'rei': 3, 'honra': 1}, 'ORGULHOSO': {'honra': 2, 'paz': -1, 'misericordia': -1},
 'JUSTO': {'rigor': 2, 'honra': 2, 'segredo': -2}, 'HONESTO': {'segredo': -3, 'honra': 1, 'rigor': 1},
 'AVARENTO': {'poupar': 3, 'gasto': -3}, 'DILIGENTE': {'cautela': 1, 'tradicao': 1},
 'DISCIPLINADO': {'rigor': 2, 'tradicao': 1, 'risco': -1}, 'CRUEL': {'misericordia': -3, 'rigor': 1, 'guerra': 1},
 'TEIMOSO': {'tradicao': 2, 'novidade': -2}, 'PACIENTE': {'cautela': 2, 'risco': -2},
 'FRIO': {'misericordia': -1, 'cautela': 1, 'segredo': 1}, 'CURIOSO': {'novidade': 2, 'saber': 2},
 'AMBICIOSO': {'risco': 2, 'novidade': 1, 'gasto': 1}, 'VINGATIVO': {'guerra': 2, 'misericordia': -2, 'paz': -2},
 'RELIGIOSO': {'fe': 3, 'tradicao': 1}, 'CORAJOSO': {'risco': 2, 'guerra': 1},
 'COVARDE': {'cautela': 3, 'guerra': -2, 'risco': -2}, 'GENEROSO': {'gasto': 2, 'misericordia': 2, 'povo': 1},
 'CINICO': {'fe': -2, 'segredo': 1}, 'DESCONFIADO': {'segredo': 2, 'cautela': 1, 'novidade': -1},
 'IMPULSIVO': {'risco': 3, 'cautela': -2}, 'CALCULISTA': {'cautela': 2, 'poupar': 1, 'segredo': 1},
 'SABIO': {'saber': 2, 'cautela': 1, 'misericordia': 1}, 'MISERICORDIOSO': {'misericordia': 3, 'rigor': -1},
 'GANANCIOSO': {'poupar': 1, 'risco': 1, 'povo': -1}, 'HUMILDE': {'povo': 2, 'honra': -1},
 'VAIDOSO': {'honra': 1, 'gasto': 1}, 'PREGUICOSO': {'novidade': -1, 'tradicao': 1},
}
OPOSTOS = [('CORAJOSO', 'COVARDE'), ('GENEROSO', 'AVARENTO'), ('IMPULSIVO', 'PACIENTE'), ('CRUEL', 'MISERICORDIOSO'),
           ('HONESTO', 'CINICO'), ('HUMILDE', 'ORGULHOSO'), ('HUMILDE', 'VAIDOSO'), ('DILIGENTE', 'PREGUICOSO')]


def canon(p):
    """ORGULHOSA → ORGULHOSO; SÁBIA → SABIO. Devolve None se não é traço do catálogo."""
    w = sem_acento(p).upper()
    if w in CAT: return w
    if w.endswith('A') and w[:-1] + 'O' in CAT: return w[:-1] + 'O'
    return None


def acha(N, nome):
    alvo = sem_acento(nome).lower()
    for k in N:
        if sem_acento(k).lower() == alvo: return k
    c = [k for k in N if alvo in sem_acento(k).lower()]
    if len(c) == 1: return c[0]
    sys.exit(f'NPC não achado (ou ambíguo): "{nome}" · candidatos: {", ".join(c) or "nenhum"}')


def tracos_de(v):
    return list(v.get('tracos', []))


def opiniao_de(v, dia=None):
    dia = dia or dia_atual()
    return sum(o['v'] for o in v.get('opiniao', []) if o.get('ate') is None or o['ate'] >= dia)


def migra(N):
    n = 0
    for k, v in N.items():
        achados = []
        for campo in ('classe', 'ocupacao'):
            for p in re.findall(r'[A-ZÁÉÍÓÚÂÊÔÃÕÇ]{4,}', str(v.get(campo, ''))):
                t = canon(p)
                if t and t not in achados: achados.append(t)
        novos = [t for t in achados if t not in v.get('tracos', [])]
        if novos:
            v['tracos'] = v.get('tracos', []) + novos; n += 1
    grava('npcs.json', N)
    print(f'migra: {n} fichas ganharam a lista de traços · com traço agora: {sum(1 for v in N.values() if v.get("tracos"))} de {len(N)}')


def completa(N, quantos):
    falta = [k for k, v in N.items() if not v.get('tracos')][:quantos]
    nomes = sorted(CAT)
    linhas = []
    for k in falta:
        tr = []
        while len(tr) < 2:
            t = nomes[d(len(nomes)) - 1]
            if t in tr or any((t == a and b in tr) or (t == b and a in tr) for a, b in OPOSTOS): continue
            tr.append(t)
        N[k]['tracos'] = tr; linhas.append(f'{k}: {", ".join(tr)}')
    grava('npcs.json', N)
    if linhas: anota('(OCULTO) TRAÇOS ROLADOS (tracos.py completa; 2 por NPC sem traço, 1d%d cada): ' % len(nomes) + ' · '.join(linhas))
    print(f'completa: {len(linhas)} NPCs ganharam 2 traços pelo dado (no envelope) · ainda sem traço: {sum(1 for v in N.values() if not v.get("tracos"))}')


def inclina(N, args):
    R = carrega('reino.json', {}).get('reino', {})
    cadeiras = []
    for dono in R.get('conselho_real', {}).values():   # "Nouliel (também Tesoureira)" → Nouliel; duas cadeiras, um voto
        nome = str(dono).split(' (')[0].strip()
        if nome and nome not in cadeiras: cadeiras.append(nome)
    ops, fora = {}, []
    for a in args:
        if a.startswith('fora='): fora = [x.strip() for x in a[5:].split(',') if x.strip()]
        elif a.startswith('quem='): cadeiras = [x.strip() for x in a[5:].split(',') if x.strip()]
        elif re.match(r'^[A-Z]=', a): ops[a[0]] = [sem_acento(x).lower() for x in a[2:].split(',') if x.strip()]
    ruins = [e for es in ops.values() for e in es if e not in EIXOS]
    if ruins: sys.exit(f'eixo que não existe: {", ".join(ruins)} · eixos: {", ".join(EIXOS)}')
    if not cadeiras: sys.exit('não achei as cadeiras em reino.json: passe quem=Nome,Nome')
    saida, conta = [], []
    for c in cadeiras:
        if not c or any(sem_acento(f).lower() == sem_acento(c).lower() for f in fora): continue
        k = acha(N, c); v = N[k]; tr = tracos_de(v); op = opiniao_de(v); partes = []
        for letra, eixos in ops.items():
            s = sum(CAT.get(t, {}).get(e, 0) for t in tr for e in eixos)
            if 'rei' in eixos: s += round(op / 20)
            s = max(-5, min(5, s))
            if s: partes.append(f'{letra}{s:+d}')
        conta.append(f'  {k}: {", ".join(tr) or "sem traço"} · opinião {op:+d} → {", ".join(partes) or "dado puro"}')
        if partes: saida.append(f'{k}={",".join(partes)}')
    print('INCLINAÇÕES PELOS TRAÇOS (declare no conselho.py antes do dado):')
    print('\n'.join(conta)); print('COLAR: ' + ' '.join(saida) + (f' fora={",".join(fora)}' if fora else ''))


def main():
    a = sys.argv[1:]
    if not a: print(__doc__); return
    N = carrega('npcs.json', {})
    c = a[0]
    if c == 'migra': migra(N)
    elif c == 'completa': completa(N, int(a[1]) if len(a) > 1 else 999)
    elif c == 'catalogo':
        for t in sorted(CAT): print(f'  {t}: ' + ' · '.join(f'{e} {v:+d}' for e, v in CAT[t].items()))
    elif c in ('ver', 'cena'):
        nomes = [acha(N, x) for x in a[1:]] or [k for k, v in N.items() if v.get('tracos')]
        for k in nomes:
            v = N[k]; print(f'{k} (nível {v.get("nivel", "?")}) · traços: {", ".join(tracos_de(v)) or "nenhum"} · opinião sobre o rei: {opiniao_de(v):+d}')
            if c == 'cena' or len(a) > 1:
                for o in v.get('opiniao', [])[-4:]: print(f'    {o["v"]:+d} {o["motivo"]} (Dia {o["dia"]}{", até " + str(o["ate"]) if o.get("ate") else ""})')
                if v.get('voz'): print(f'    VOZ: {v["voz"]}')
                if v.get('assinaturas'): print('    CLASSE: ' + ' · '.join(v['assinaturas']) + (f' · FRAQUEZA: {v["fraqueza"]}' if v.get('fraqueza') else ''))
                for campo in ('desejo', 'medo', 'linha_vermelha'):
                    if v.get(campo): print(f'    {campo}: {v[campo]}')
    elif c == 'inclina': inclina(N, a[1:])
    elif c == 'opiniao' and len(a) >= 4:
        k = acha(N, a[1]); val = int(a[2].replace('−', '-')); dias = next((int(x[5:]) for x in a[4:] if x.startswith('dias=')), None)
        hoje = dia_atual(); N[k].setdefault('opiniao', []).append({'v': val, 'motivo': a[3], 'dia': hoje, 'ate': hoje + dias if dias else None})
        grava('npcs.json', N); anota(f'OPINIÃO: {k} {val:+d} ({a[3]}) → {opiniao_de(N[k]):+d}')
        print(f'{k}: opinião {val:+d} ({a[3]}) → agora {opiniao_de(N[k]):+d}')
    elif c == 'opinioes':
        for k, v in sorted(N.items(), key=lambda kv: opiniao_de(kv[1])):
            if v.get('opiniao'): print(f'  {opiniao_de(v):+4d}  {k}')
    elif c == 'resiste' and len(a) >= 3:
        k = acha(N, a[1]); e = sem_acento(a[2]).lower(); v = N[k]
        if e not in EIXOS: sys.exit(f'eixos: {", ".join(EIXOS)}')
        base = 10 + int(v.get('nivel', 1)) // 10; tr = sum(-CAT.get(t, {}).get(e, 0) for t in tracos_de(v)); teima = 3 if 'TEIMOSO' in tracos_de(v) else 0
        op = -round(opiniao_de(v) / 10)
        print(f'RESISTÊNCIA de {k} a um pedido de "{e}": CD {base + tr + teima + op} = 10 + nível÷10 ({int(v.get("nivel", 1)) // 10}) + traços contra o eixo ({tr:+d}) + teimosia ({teima:+d}) + opinião ({op:+d}). Contra NPC importante o Mestre ainda soma o contexto.')
    elif c == 'traco' and len(a) >= 3:
        k = acha(N, a[1]); t = canon(a[2].lstrip('+-'))
        if not t: sys.exit('traço fora do catálogo (tracos.py catalogo)')
        tr = N[k].setdefault('tracos', [])
        if a[2].startswith('-'): tr[:] = [x for x in tr if x != t]
        elif t not in tr: tr.append(t)
        grava('npcs.json', N); anota(f'TRAÇO: {k} {a[2][0]}{t} ({a[3] if len(a) > 3 else "sem motivo dito"}) → {", ".join(tr)}'); print(f'{k}: {", ".join(tr)}')
    elif c == 'voz' and len(a) >= 3:
        k = acha(N, a[1]); N[k]['voz'] = a[2]; grava('npcs.json', N); print(f'{k}: voz gravada')
    else: print(__doc__)


if __name__ == '__main__':
    main()
