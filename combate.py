#!/usr/bin/env python3
"""combate.py — as FICHAS DE COMBATE num lugar só (MOTOR 6.3): fichas_combate.json.
Antes cada arquivo de luta em sims/ carregava a sua cópia das fichas, e elas ficavam velhas (num deles o Ferir ainda é nível 82).
Uso:
  python3 combate.py ver                                     as fichas, com o nível de hoje e o aviso de ficha velha
  python3 combate.py monta SAIDA.json base=ARQ.json NOME...  cria sims/SAIDA.json: o monstro vem do arquivo base, o grupo vem daqui
  python3 combate.py poe NOME campo=valor ...                acerta a ficha (at, df, rd, pv, dado, mult, b) e marca o nível de hoje
  python3 combate.py nova NOME nivel at df rd pv dado mult b
MOTOR 9.1 (438): a conferência mostra as ARTES DE ARMA de cada um (a chave "arte" no feitiço da ficha faz o luta.py rodar o efeito) e o base=
pode trazer "tracos" no monstro (o texto do gerador): o luta.py roda os traços, a 2ª fase e o olhar sozinho.
O nível vem de ficha.json (Ferir) e de npcs.json (os outros). O PV de Ferir vem da ficha viva. Ferido (feridos.py) é avisado; ferimento
LEVE entra com −2 no ataque e na defesa; SÉRIO para cima não entra.
"""
import sys, json, os
from nucleo import carrega, grava, P, acha_nome
ARQ = 'fichas_combate.json'

def nivel_hoje(nome):
    F = carrega('ficha.json')
    if F and nome == F.get('nome'): return F['nivel'], F['pv'][1]
    db = carrega('npcs.json'); k, _ = acha_nome(nome, db)
    return (db[k].get('nivel'), None) if k else (None, None)

def _livros_sobre(nome, n=3):
    """426 (G9): trechos do estado vivo e do cânone com o nome e uma palavra de peça ou feitiço."""
    import re as _re
    chaves = ('TOQUE', 'LANÇA DO SOL', 'CHUVA', 'ERGUER', 'GORJAL', 'ENCANT', 'guarda o', 'MÍTIC', 'PRIMORDIAL', 'LENDÁRI', 'feitiço')
    achou = []
    for arq in ('estado_vivo.md', 'canone.md'):
        try: txt = open(P(arq), encoding='utf-8').read()
        except Exception: continue
        for frase in _re.split(r'(?<=[.·])\s', txt):
            if nome.upper() in frase.upper() and any(c.upper() in frase.upper() for c in chaves):
                f = frase.strip()[:170]
                if f not in achou: achou.append(f)
            if len(achou) >= n: return achou
    return achou

def main():
    a = sys.argv[1:]; R = carrega(ARQ, {'fichas': {}}); fer = {x['nome']: x for x in carrega('feridos.json', {'feridos': []})['feridos']}
    if not a or a[0] == 'ver':
        for n, g in R['fichas'].items():
            nv, _ = nivel_hoje(n); velha = nv and g.get('nivel_ref') and abs(nv - g['nivel_ref']) >= 5
            print(f"{n}: nível {nv or g.get('nivel')} · ataque {g['at']} · defesa {g['df']} · RD {g['rd']} · PV {g['pv']} · {g['dado']}×{g['mult']}+{g['b']}" + (' · magia ' + str(g['magia']) if g.get('magia') else '')
                  + (f" · ⚠ FICHA DO NÍVEL {g['nivel_ref']}: rever ataque e defesa (combate.py poe)" if velha else '') + (f" · FERIDO ({fer[n]['grau']}) até o {fer[n]['ate']}" if n in fer else ''))
        return
    if a[0] == 'monta' and len(a) > 3:
        base = next((x[5:] for x in a[2:] if x.startswith('base=')), None); nomes = [x for x in a[2:] if '=' not in x]
        if not base: sys.exit('falta base=ARQ.json (de onde vem o monstro)')
        F = json.load(open(P(base) if not os.path.isabs(base) else base, encoding='utf-8')); grupo = []; CONF = []
        for n in nomes:
            k, sug = acha_nome(n, R['fichas'])
            if not k: sys.exit(f'sem ficha de combate para "{n}".' + (f' Parecidos: {", ".join(sug)}.' if sug else '') + ' (combate.py nova)')
            g = dict(R['fichas'][k]); nv, pv = nivel_hoje(k)
            if nv: g['nivel'] = nv
            if pv: g['pv'] = pv
            if g.get('nivel_ref') and nv and abs(nv - g['nivel_ref']) >= 5: print(f"⚠ {k}: a ficha é do nível {g['nivel_ref']}; hoje é {nv}. Ataque e defesa podem estar baixos.")
            # 426 (G9): a CONFERÊNCIA que faltou na forquilha: o que a ficha tem e o que os livros dizem que a pessoa carrega
            mgs = g.get('magias') or ([g['magia']] if g.get('magia') else [])
            CONF.append(f"  {k} (nível {nv or g.get('nivel')}): ficha com {len(mgs)} feitiço(s): " + ('; '.join(m.get('nome', m.get('dano','?')) for m in mgs) or 'NENHUM') + f" · peças na ficha: {g.get('pecas','⚠ NÃO ANOTADAS')}")
            # MOTOR 9.1 (438): as ARTES DE ARMA com efeito (a chave "arte" faz o luta.py rodar o efeito; sem ela só sai o dano)
            try:
                from luta import ARTES, chave_arte
                com = [m['arte'] for m in mgs if m.get('arte')]
                sem = [m.get('nome', '?')[:30] for m in mgs if not m.get('arte') and any(chave_arte(m.get('nome', '')).startswith(a_) for a_ in ARTES)]
                if com: CONF.append('      Artes de arma com efeito no script: ' + ', '.join(com) + ''.join(f" (encadeia {m['encadeia']['arte'] if isinstance(m['encadeia'], dict) else '+'.join(x['arte'] for x in m['encadeia'])})" for m in mgs if m.get('encadeia')))
                if sem: CONF.append('      ⚠ Arte SEM a chave "arte" (só o dano roda; python3 luta.py artes): ' + '; '.join(sem))
                ruins = [m['arte'] for m in mgs if m.get('arte') and chave_arte(m['arte']) not in ARTES]
                if ruins: CONF.append('      ⚠ Arte desconhecida: ' + ', '.join(ruins))
            except ImportError: pass
            for lv in _livros_sobre(k): CONF.append('      livro: ' + lv)
            if k in fer:
                if fer[k]['grau'] == 'LEVE': g['at'] -= 2; g['df'] -= 2; print(f'⚠ {k} luta ferido (LEVE): −2 no ataque e na defesa.')
                else: print(f"⚠ {k} está FERIDO ({fer[k]['grau']}) até o Dia {fer[k]['ate']}: NÃO ENTRA na luta."); continue
            g.pop('nivel_ref', None); grupo.append(g)
        print('CONFERÊNCIA DAS FICHAS (G9, 426): confira cada peça e cada feitiço com os livros antes de lutar')
        for c in CONF: print(c)
        if 'conferido=1' not in a:
            sys.exit('⛔ G9: nada foi montado. Acerte as fichas (combate.py poe ou o json) e rode de novo com conferido=1.')
        F['grupo'] = grupo; saida = P('sims', a[1] if a[1].endswith('.json') else a[1] + '.json')
        json.dump(F, open(saida, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(f"montado: sims/{os.path.basename(saida)} · {F['monstro']['nome']} contra {', '.join(g['nome'] for g in grupo)}  → python3 luta.py sims/{os.path.basename(saida)} regua=2000")
        return
    if a[0] == 'poe' and len(a) > 2:
        k, _ = acha_nome(a[1], R['fichas'])
        if not k: sys.exit('ficha não achada.')
        for x in a[2:]:
            c, v = x.split('=', 1); R['fichas'][k][c] = v if c == 'dado' else float(v) if '.' in v else int(v)
        nv, _ = nivel_hoje(k); R['fichas'][k]['nivel_ref'] = nv or R['fichas'][k].get('nivel_ref'); grava(ARQ, R); print(f'{k}: ficha acertada (nível de referência {R["fichas"][k]["nivel_ref"]}).'); return
    if a[0] == 'nova' and len(a) > 9:
        R['fichas'][a[1]] = dict(nome=a[1], nivel=int(a[2]), nivel_ref=int(a[2]), at=int(a[3]), df=int(a[4]), rd=int(a[5]), pv=int(a[6]), dado=a[7], mult=float(a[8]), b=int(a[9])); grava(ARQ, R); print(f'{a[1]}: ficha criada.'); return
    print(__doc__)

if __name__ == '__main__':
    main()
