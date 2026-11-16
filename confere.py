#!/usr/bin/env python3
"""confere.py — antes de narrar um FATO ANTIGO, procurar o que está escrito.

Uso:  python3 confere.py TERMO [TERMO2 ...] [max=6]
Procura cada termo (sem diferença de maiúsculas) no CÂNONE FIXO, no ATLAS
(secreto: só o Mestre lê), no estado, nos diários, nos envelopes, nos NPCs e
no mundo vivo, e mostra as linhas (cortadas) por arquivo, na ordem de
autoridade. Se o termo NÃO aparece em lugar nenhum, o fato NÃO EXISTE ainda:
declarar uma tabela antes de inventar.
"""
import sys, glob, os, re, json

AQUI = os.path.dirname(os.path.abspath(__file__))
def _acha(*nomes):
    import os
    base = os.path.dirname(os.path.abspath(__file__))
    for n in nomes:
        for c in (os.path.join(base, '..', 'pacote', 'arquivo_dia159', n), os.path.join(base, 'arquivo_dia159', n), os.path.join(base, n)):
            if os.path.exists(c): return c
    return os.path.join(base, 'arquivo_dia159', nomes[0])

ORDEM = [
    ('CÂNONE FIXO', [os.path.join(AQUI, 'canone.md')]),
    ('ATLAS (secreto)', [_acha('atlas.md')]),
    ('ESTADO', [os.path.join(AQUI, 'estado_vivo.md')]),
    ('REGRAS DA CASA', glob.glob(os.path.join(AQUI, 'regras_da_casa*.md'))),
    ('DIÁRIOS', sorted(glob.glob(os.path.join(AQUI, 'diario_sessao*.md')), reverse=True)),
    ('ENVELOPES', sorted(glob.glob(os.path.join(AQUI, 'envelope_sessao*.md')), reverse=True)
                  + [_acha('envelope.md')]),
    ('NPCS', [os.path.join(AQUI, 'npcs.json')]),
    ('MUNDO VIVO', [os.path.join(AQUI, 'mundo_vivo.json')]),
]

def trecho(linha, termo, largura=260):
    i = linha.lower().find(termo.lower())
    ini = max(0, i - largura // 2)
    t = linha[ini:ini + largura].strip()
    return ('…' if ini > 0 else '') + t + ('…' if ini + largura < len(linha) else '')

def main():
    args = sys.argv[1:]
    mx = 6
    termos = []
    for a in args:
        if a.startswith('max='): mx = int(a[4:])
        else: termos.append(a)
    if not termos:
        print(__doc__); return
    for termo in termos:
        print(f'===== "{termo}" =====')
        achou = 0
        for rotulo, arquivos in ORDEM:
            for arq in arquivos:
                if not os.path.exists(arq): continue
                linhas = open(arq, encoding='utf-8', errors='replace').read().splitlines()
                hits = [(n + 1, l) for n, l in enumerate(linhas) if termo.lower() in l.lower()]
                if not hits: continue
                achou += len(hits)
                print(f'-- {rotulo}: {os.path.basename(arq)} ({len(hits)} linhas)')
                for n, l in hits[:mx]:
                    print(f'   {n}: {trecho(l, termo)}')
                if len(hits) > mx: print(f'   … mais {len(hits) - mx}')
        if not achou:
            print('   NADA ESCRITO. O fato não existe ainda: DECLARAR TABELA antes de narrar.')
        print()

if __name__ == '__main__':
    main()
