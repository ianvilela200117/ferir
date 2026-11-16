#!/usr/bin/env python3
"""livro_sync.py — MOTOR 9: o LIVRO acompanha o jogo.

Escreve, entre marcas, no fim do capítulo de MATERIAIS os que a casa achou e o Livro não trazia (ficha.json),
e no fim do BESTIÁRIO os bichos que a casa enfrentou ou viu (mundo_vivo.json: monstros_novos).
Só entra o que a casa SABE: pedaço de nota com "OCULTO" ou "a descobrir" fica de fora.
Depois refaz o livro_do_mundo.html (se o módulo markdown estiver instalado).

Uso: python3 livro_sync.py        (rodar quando entrar bicho ou material novo; pode rodar sempre)
"""
import os, re, subprocess, sys
from nucleo import carrega, P

INI, FIM = '<!-- SYNC:INICIO (livro_sync.py; não editar à mão) -->', '<!-- SYNC:FIM -->'


def troca(arq, bloco):
    t = open(arq, encoding='utf-8').read()
    if INI in t: t = t[:t.index(INI)].rstrip('\n') + '\n'
    open(arq, 'w', encoding='utf-8').write(t.rstrip('\n') + '\n\n' + INI + '\n' + bloco.rstrip('\n') + '\n' + FIM + '\n')


def limpa(nota):
    ped = [p.strip() for p in re.split(r'[;·]', nota or '') if p.strip()]
    ped = [p for p in ped if not re.search(r'oculto|a descobrir|bicho\.py|gerador monstro|obras/|nomes\.py|trocad', p, re.I)]
    return '; '.join(ped)[:260]


def main():
    F = carrega('ficha.json'); M = carrega('mundo_vivo.json')
    arq6 = P('compendio', '06_essencias_materiais.md'); arq7 = P('compendio', '07_bestiario.md')
    base6 = open(arq6, encoding='utf-8').read().split(INI)[0].lower()
    lin = []
    for nome, m in sorted(F.get('materiais', {}).items()):
        if re.search(r'\b' + re.escape(nome.lower()) + r'\b', base6) or nome.startswith('núcleo'): continue
        log = (m.get('log') or [''])[0]; sabe = re.sub(r'^Dia \d+: [+-][\d.,]+ (?:\d+: )?', '', log)
        lin.append(f"| **{nome}** | ~{m.get('kg', 0):g} | {limpa(sabe) or '—'} |")
    nuc = [f"{n} ×{m.get('kg', 0):g}" for n, m in sorted(F.get('materiais', {}).items()) if n.startswith('núcleo') and m.get('kg', 0) > 0]
    b6 = ('### Achados da casa que o Livro não trazia\n\nSaem do `ficha.json` a cada vez que o `livro_sync.py` roda. São drops de bichos e achados de tesouro.\n\n'
          '| Material | A casa tem | O que se sabe |\n| --- | --- | --- |\n' + '\n'.join(lin) + '\n'
          + (f"\n**Núcleos na mão do rei:** {' · '.join(nuc)}.\n" if nuc else ''))
    troca(arq6, b6)
    lb = []
    for x in M.get('monstros_novos', []):
        nota = x.get('nota', ''); estado = 'morto' if re.match(r'\s*MORT', nota) else 'vivo'
        lb.append(f"| **{x.get('nome')}** | {x.get('cat', '')} | {x.get('nivel', '')} | {x.get('essencia', '')} | {x.get('onde', x.get('regiao', ''))} | {estado} | {limpa(nota) or '—'} |")
    b7 = ('## 5. Bichos que a casa enfrentou ou viu\n\nSaem do jogo (`mundo_vivo.json`) a cada vez que o `livro_sync.py` roda. Só o que a casa sabe.\n\n'
          '| Bicho | Categoria | Nível | Essência | Onde | Estado | O que a casa sabe |\n| --- | --- | --- | --- | --- | --- | --- |\n' + '\n'.join(lb) + '\n\n'
          'Os traços novos, as fases dos chefes, os nomeados e as crias estão no **Livro Nove**, seção 8.\n')
    troca(arq7, b7)
    print(f'Livro sincronizado: {len(lin)} material(is) novo(s) no capítulo 6; {len(lb)} bicho(s) no capítulo 7.')
    try:
        import markdown  # noqa
        r = subprocess.run([sys.executable, 'build_livro.py'], cwd=P('compendio'), capture_output=True, text=True)
        print('livro_do_mundo.html refeito.' if r.returncode == 0 else f'(o HTML não foi refeito: {r.stderr[-120:]})')
    except ImportError:
        print('(sem o módulo markdown: o HTML não foi refeito; `pip install markdown` e rodar compendio/build_livro.py)')


if __name__ == '__main__':
    main()
