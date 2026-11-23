#!/usr/bin/env python3
"""itens.py — MOTOR 10: O LIVRO DE ITENS. Uma peça que não está aqui não existe.

Toda arma, armadura e escudo é um registro em dados/itens.json: o que é, de que categoria, quanto aguenta, o que faz,
de quem é, quem fez e o que viveu. A ficha de luta de quem veste sai DAQUI (pessoas.py): ninguém digita ataque e dano.

Uso:
  python3 itens.py nova arma FAMILIA CATEGORIA "Nome" [dono=Nome] [feito=Nome] [dia=N] [efeito=chave[:valor]]... [sob=Dono:grau]
  python3 itens.py nova armadura MATERIAL CATEGORIA "Nome" [cobre=tronco,braços,pernas] ...   (elmo: cobre=cabeça)
  python3 itens.py nova escudo CATEGORIA "Nome" ...
  python3 itens.py nova nucleo CATEGORIA "Nome" [de=ESPECIE] [dono=Nome]     o núcleo de um chefe (o que a obra Épica ou maior pede)
  python3 itens.py ver [dono=Nome]          a lista
  python3 itens.py janela ID                a janela do item (a que aparece na cena)
  python3 itens.py dono ID "Nome" ["o que houve"]     a peça muda de mão (entra na história dela)
  python3 itens.py conserta ID [N]          devolve N de durabilidade (sem N: toda)
FAMILIA: punho adaga espada maça machado martelo lança montante alabarda malho arco besta · MATERIAL: couro malha placa
CATEGORIA: Comum Incomum Raro Épico Único Lendário Mítico Primordial
"""
import json, os, sys
import tabelas as T
from tabelas import CATS, MULT, RD, BON, DUR, FAMILIAS, MATERIAIS, PARTES, PEDE_PESO, DUAS_MAOS

AQUI = os.path.dirname(os.path.abspath(__file__))
ARQ = os.path.join(AQUI, 'dados', 'itens.json')

# os efeitos que a luta sabe rodar, e em que tipo de peça cada um vale. Efeito que não está aqui não entra numa peça.
EFEITOS = {
    'sangra':     ('a ferida que ela abre sangra mais (cinco rodadas)', ('arma',)),
    'critico_19': ('o 19 também é crítico', ('arma',)),
    'derruba':    ('uma vez por luta, o golpe que fere derruba', ('arma',)),
    'devolve':    ('quem golpeia o dono corpo a corpo leva {valor}', ('armadura',)),
    'firme':      ('o dono não é derrubado', ('armadura', 'escudo')),
    'leve':       ('pede 20 a menos de atributo', ('arma', 'armadura', 'escudo')),
    'pesa':       ('pede 20 a mais de atributo', ('arma', 'armadura', 'escudo')),
    'nao_quebra': ('não perde durabilidade', ('arma', 'armadura', 'escudo')),
}


def cat_i(c):
    """'Raro' ou 2 → 2"""
    if isinstance(c, int):
        if not 0 <= c < len(CATS): sys.exit(f'categoria fora da tabela: {c} (vai de 0, Comum, a 7, Primordial)')
        return c
    n = c.strip().lower().replace('epico', 'épico').replace('unico', 'único').replace('lendario', 'lendário').replace('mitico', 'mítico')
    for i, x in enumerate(CATS):
        if x.lower() == n: return i
    sys.exit(f'categoria desconhecida: "{c}" (use: {", ".join(CATS)})')


def item(tipo, cat, nome=None, familia=None, material=None, cobre=None, efeitos=None, sob=None, **mais):
    """monta um registro de item (sem gravar). É o que os testes e o `nova` usam."""
    c = cat_i(cat)
    if tipo == 'nucleo':                                    # o NÚCLEO: não se veste, não gasta, não leva efeito. É contado no mundo, com dono e lugar.
        if efeitos or sob or familia or material or cobre: sys.exit('o núcleo não leva efeito, sob medida, família nem material: só a categoria, o nome e de que bicho veio (de=)')
        it = dict(tipo='nucleo', cat=c, nome=nome or f'núcleo {CATS[c]}', dur=[T.NUCLEO_DUR, T.NUCLEO_DUR], dono=None, onde=None, de=mais.pop('de', None), historia=[])
        it.update(mais)
        return it
    it = dict(tipo=tipo, cat=c, nome=nome, dur=[DUR[c], DUR[c]], efeitos=list(efeitos or []), sob_medida=sob, historia=[], dono=None, onde=None)
    if tipo == 'arma':
        if familia not in FAMILIAS: sys.exit(f'família de arma desconhecida: "{familia}" (use: {", ".join(FAMILIAS)})')
        it['familia'] = familia; it['nome'] = nome or f'{familia} {CATS[c]}'
    elif tipo == 'armadura':
        if material not in MATERIAIS: sys.exit(f'material desconhecido: "{material}" (use: {", ".join(MATERIAIS)})')
        it['material'] = material; it['cobre'] = list(cobre or ['tronco', 'braços', 'pernas'])
        for p in it['cobre']:
            if p not in PARTES: sys.exit(f'parte desconhecida: "{p}" (use: {", ".join(PARTES)})')
        it['nome'] = nome or (f'elmo de {material}' if it['cobre'] == ['cabeça'] else f'armadura de {material}') + f' {CATS[c]}'
    elif tipo == 'escudo':
        it['nome'] = nome or f'escudo {CATS[c]}'
    else:
        sys.exit(f'tipo desconhecido: "{tipo}" (arma, armadura, escudo, nucleo)')
    for e in it['efeitos']:
        if e['chave'] not in EFEITOS: sys.exit(f'efeito desconhecido: "{e["chave"]}" (os que a luta roda: {", ".join(EFEITOS)})')
        if tipo not in EFEITOS[e['chave']][1]: sys.exit(f'o efeito "{e["chave"]}" não vale em {tipo} (vale em: {", ".join(EFEITOS[e["chave"]][1])})')
        if e['chave'] == 'devolve' and not 1 <= e.get('valor', 0) <= T.devolve_max(c):
            sys.exit(f'"devolve" numa peça {CATS[c]} vai de 1 a {T.devolve_max(c)} (veio {e.get("valor")})')
    if sob and not T.SOB_MEDIDA_GRAUS[0] <= sob.get('grau', 1) <= T.SOB_MEDIDA_GRAUS[1]:
        sys.exit(f'o grau do sob medida vai de {T.SOB_MEDIDA_GRAUS[0]} a {T.SOB_MEDIDA_GRAUS[1]} (veio {sob.get("grau")})')
    it.update(mais)
    return it


def tem(it, chave):
    """o valor do efeito na peça (True se não tem valor), ou None"""
    for e in it.get('efeitos', []):
        if e['chave'] == chave: return e.get('valor', True)
    return None


def pede(it, dorme=False):
    """(atributo, quanto) que a peça pede. O requisito vem do PESO da peça, nunca da categoria nem do nível.
    Peça que dorme (sintonia) não tem efeito nenhum: nem o "leve"."""
    if it['tipo'] == 'nucleo': return 'Força', 0            # o núcleo não se empunha
    aj = 0 if dorme else (T.AJUSTE_PESO if tem(it, 'pesa') else 0) - (T.AJUSTE_PESO if tem(it, 'leve') else 0)
    if it['tipo'] == 'arma':
        f = FAMILIAS[it['familia']]
        return f.get('atributo', 'Força'), PEDE_PESO[f['peso']] + aj
    if it['tipo'] == 'armadura': return 'Força', MATERIAIS[it['material']]['pede'] + aj
    return 'Força', PEDE_PESO['media'] + aj


def janela(it):
    """a janela do item, como aparece na cena"""
    c = it['cat']; L = [f"[ {it['nome']} ]"]
    if it['tipo'] == 'nucleo':
        L.append(f"Categoria: {CATS[c]}      Núcleo" + (f" de {it['de']}" if it.get('de') else ''))
        L.append(f"Serve para: uma obra {CATS[c]} (do Épico para cima, a forja pede um núcleo da categoria da peça). Não se veste e não gasta.")
        if it.get('dono'): L.append(f"Dono: {it['dono']}")
        if it.get('onde'): L.append(f"Está em: {it['onde']}")
        for h in it.get('historia', [])[-3:]: L.append(f'  · {h}')
        return '\n'.join(L)
    L.append(f"Categoria: {CATS[c]}      Durabilidade: {it['dur'][0]}/{it['dur'][1]}")
    if it['tipo'] == 'arma':
        f = FAMILIAS[it['familia']]; m = MULT[c] * (DUAS_MAOS if f['maos'] == 2 else 1)
        L.append(f"Ataque: {f['dado']} × {m:g} ({f['golpe']})      Acerto: +{BON[c]}      Alcance: {'à distância' if f.get('distancia') else str(f['alcance']) + ' casa(s)'}")
    elif it['tipo'] == 'armadura':
        mat = MATERIAIS[it['material']]
        L.append(f"Proteção: {RD[c] * mat['rd']:g} ({it['material']})      Cobre: {', '.join(it['cobre'])}" + (f"      Defesa: {mat['defesa']:+d}" if 'tronco' in it['cobre'] and mat['defesa'] else ''))
    else:
        L.append(f"Defesa: +{T.ESCUDO_BASE + BON[c]:g}")
    a, q = pede(it); L.append(f"Pede: {a} {q}")
    if it['efeitos']: L.append('Efeitos: ' + ' · '.join(EFEITOS[e['chave']][0].format(valor=e.get('valor', '')) for e in it['efeitos']))
    if it.get('sob_medida'): L.append(f"Sob medida para: {it['sob_medida']['dono']} (grau {it['sob_medida']['grau']})")
    if it.get('dono'): L.append(f"Dono: {it['dono']}")
    if it.get('feito_por'): L.append(f"Feita por: {it['feito_por']}" + (f", Dia {it['dia']}" if it.get('dia') else ''))
    for h in it.get('historia', [])[-3:]: L.append(f'  · {h}')
    return '\n'.join(L)


# ---------- o arquivo ----------
def carrega():
    if not os.path.exists(ARQ): return dict(seq=0, itens={})
    return json.load(open(ARQ, encoding='utf-8'))


def grava(B):
    os.makedirs(os.path.dirname(ARQ), exist_ok=True)
    json.dump(B, open(ARQ, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


def main():
    a = sys.argv[1:]
    if not a: print(__doc__); return
    op = {k: v for k, v in (x.split('=', 1) for x in a if '=' in x and not x.startswith('efeito='))}
    pos = [x for x in a if '=' not in x]
    B = carrega()
    if a[0] == 'nova' and len(pos) >= 3 and pos[1] == 'nucleo':
        it = item('nucleo', pos[2], pos[3] if len(pos) > 3 else None, de=op.get('de'))
        B['seq'] += 1; it['id'] = f"i{B['seq']:04d}"; it['dono'] = op.get('dono')
        B['itens'][it['id']] = it; grava(B); print(f"{it['id']} entrou no Livro de Itens.\n"); print(janela(it)); return
    if a[0] == 'nova' and len(pos) >= 4:
        ef = []
        for x in a:
            if x.startswith('efeito='):
                k, _, v = x[7:].partition(':'); ef.append(dict(chave=k, **({'valor': int(v)} if v else {})))
        sob = None
        if op.get('sob'):
            d, _, g = op['sob'].partition(':'); sob = dict(dono=d, grau=int(g or 1))
        tipo = pos[1]
        if tipo == 'arma': it = item('arma', pos[3], pos[4] if len(pos) > 4 else None, familia=pos[2], efeitos=ef, sob=sob)
        elif tipo == 'armadura': it = item('armadura', pos[3], pos[4] if len(pos) > 4 else None, material=pos[2], cobre=op['cobre'].split(',') if op.get('cobre') else None, efeitos=ef, sob=sob)
        else: it = item('escudo', pos[2], pos[3] if len(pos) > 3 else None, efeitos=ef, sob=sob)
        B['seq'] += 1; it['id'] = f"i{B['seq']:04d}"; it['dono'] = op.get('dono'); it['feito_por'] = op.get('feito'); it['dia'] = int(op['dia']) if op.get('dia') else None
        B['itens'][it['id']] = it; grava(B); print(f"{it['id']} entrou no Livro de Itens.\n"); print(janela(it)); return
    if a[0] == 'ver':
        for i, it in B['itens'].items():
            if op.get('dono') and it.get('dono') != op['dono']: continue
            print(f"  {i}  {it['nome']} · {CATS[it['cat']]} · {it['dur'][0]}/{it['dur'][1]}" + (f" · de {it['dono']}" if it.get('dono') else ''))
        if not B['itens']: print('  (o Livro de Itens está vazio)')
        return
    if a[0] in ('janela', 'dono', 'conserta') and len(pos) > 1:
        it = B['itens'].get(pos[1])
        if not it: sys.exit(f'não há item "{pos[1]}" (itens.py ver)')
        if a[0] == 'dono':
            it['historia'].append(f"de {it.get('dono') or 'ninguém'} para {pos[2]}" + (f': {pos[3]}' if len(pos) > 3 else '')); it['dono'] = pos[2]; grava(B)
        if a[0] == 'conserta':
            it['dur'][0] = min(it['dur'][1], it['dur'][0] + int(pos[2])) if len(pos) > 2 else it['dur'][1]; grava(B)
        print(janela(it)); return
    print(__doc__)


if __name__ == '__main__':
    main()
