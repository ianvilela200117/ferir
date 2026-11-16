#!/usr/bin/env python3
"""Gera nomes por sonoridade. Uso: python3 nomes.py SONORIDADE [quantidade] [livre]
MOTOR 6.2: com "livre", só saem nomes cujas 3 primeiras letras não batem com nenhum nome do cânone, do estado, dos NPCs, do mundo nem do Livro (compendio/).
Antes eram dois passos (nomes.py e depois prefixo.py), e o prefixo.py não olhava o Livro."""
import sys, secrets
S = {
 'aspera':     (['Kr', 'Dr', 'Gr', 'Th', 'Br', 'Sk', 'Vr', 'Hr'], ['a', 'o', 'u', 'e'], ['g', 'k', 'rn', 'th', 'dd', 'sk', 'rk', 'n'], ['', 'a', 'ur', 'ek', 'os']),
 'liquida':    (['L', 'M', 'N', 'Ir', 'El', 'Y', 'Ael', 'S'], ['ia', 'e', 'i', 'ae', 'ou', 'a'], ['l', 'n', 'r', 'v', 'll', 'nn', 's'], ['a', 'iel', 'is', 'ane', 'or', 'e']),
 'arcaica':    (['Va', 'Or', 'Ce', 'Al', 'Ma', 'Te', 'Qu', 'Ser'], ['ra', 'lo', 'mi', 'the', 'du', 'ne'], ['s', 'x', 'mn', 'rv', 'lt', 'c'], ['us', 'ia', 'ion', 'ar', 'eth', 'a']),
 'mercante':   (['Pe', 'Bo', 'Fa', 'Lu', 'Ca', 'Ro', 'Gi', 'Do'], ['re', 'ni', 'la', 'to', 'ci', 'ba'], ['nt', 'll', 'cc', 'rz', 'nd', 'ss'], ['o', 'i', 'a', 'ino', 'etta', 'one']),
 'sibilante':  (['S', 'Z', 'Ss', 'Xa', 'Is', 'Sh', 'Ze', 'As'], ['a', 'i', 'e', 'y'], ['sh', 'z', 'ss', 'th', 'sr', 'zh'], ['', 'a', 'ir', 'ess', 'eth', 'is']),
 'montanhesa': (['H', 'Bj', 'Ul', 'St', 'Ei', 'G', 'R', 'T'], ['a', 'o', 'i', 'u', 'e'], ['rv', 'nd', 'lg', 'st', 'rk', 'gr'], ['', 'a', 'ir', 'ald', 'unn', 'e']),
}
pick = lambda xs: xs[secrets.randbelow(len(xs))]
def nome(som):
    if som not in S:
        print(f'sonoridade desconhecida: {som}. Use uma destas: ' + ', '.join(S)); sys.exit(1)
    a, v, c, f = S[som]
    partes = [pick(a), pick(v)]
    if secrets.randbelow(3): partes.append(pick(c))
    partes.append(pick(f))
    return ''.join(partes).capitalize()
if __name__ == '__main__' and 'livre' not in sys.argv:
    if len(sys.argv) < 2 or sys.argv[1] not in S:
        sys.exit(__doc__)
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    print(', '.join(nome(sys.argv[1]) for _ in range(n)))


def _usados():
    import re, glob, os
    aqui = os.path.dirname(os.path.abspath(__file__)); txt = ''
    for f in ['npcs.json', 'mundo_vivo.json', 'canone.md', 'estado_vivo.md', 'mundo.json', 'reino.json', 'agenda.json'] + [os.path.basename(x) for x in glob.glob(os.path.join(aqui, 'envelope_sessao*.md'))] + ['compendio/' + os.path.basename(x) for x in glob.glob(os.path.join(aqui, 'compendio', '*.md'))]:
        try: txt += open(os.path.join(aqui, f), encoding='utf-8').read()
        except OSError: pass
    nomes = {w[:3].lower() for w in re.findall(r"\b[A-ZÁÉÍÓÚ][A-Za-záéíóúãõâêôç]{3,}\b", txt)}
    # 435: os materiais do Livro ficam em minúscula, em negrito ("**yiis**", "**zaess**"): também entram
    nomes |= {w[:3].lower() for w in re.findall(r"\*\*([a-záéíóúãõâêôç]{3,})\*\*", txt)}
    return nomes

if __name__ == '__main__' and 'livre' in sys.argv:
    som = sys.argv[1]; q = next((int(x) for x in sys.argv[2:] if x.isdigit()), 6); us = _usados(); out = []; t = 0
    while len(out) < q and t < 4000:
        t += 1; n = nome(som)
        if n[:3].lower() not in us and n not in out: out.append(n)
    print(', '.join(out) if out else 'nenhum nome livre nessa sonoridade; tente outra')
    sys.exit(0)
