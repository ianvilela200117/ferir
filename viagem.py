#!/usr/bin/env python3
"""viagem.py — viagens e recados com a DISTÂNCIA do Livro do Mundo (MOTOR 6.3). A tabela vem de compendio/01_mundo.md
(tempos a partir de Ireviel). O script soma os dias, olha o tempo na saída e põe a chegada na AGENDA.

Uso:
  python3 viagem.py lista                                 a tabela de distâncias do Livro
  python3 viagem.py vai "QUEM OU O QUÊ" DESTINO [de=ORIGEM] [saida=DIA] [dias=N] [volta] [para] [oculto]
        de=    de onde sai (padrão: Ireviel). Entre dois lugares que não são Ireviel, soma os dois trechos.
        dias=  força o tempo (um atalho, um navio, uma barca rápida)
        volta  marca também a chegada de volta à origem
        leva=Nome,Nome   quem vai junto: o onde.py passa a mostrar essa gente em viagem e, na chegada, no destino
        para   o bloco PARA no dia da chegada
Tempestade na saída (clima.py): o barco não sai, +1 dia. Rio SECO ou em CHEIA: +1 dia nos caminhos de rio.
"""
import re, sys
from nucleo import ler, carrega, dia_atual, agenda_add, acha_nome, anota


def tabela():
    T = {}
    for l in ler('compendio/01_mundo.md').split('\n'):
        m = re.match(r'^\| ([^|]+?) \| ([^|]*\d[^|]*|meia manhã[^|]*) \| ([^|]+?) \|$', l)
        if not m or 'dia' not in m.group(2) and 'manhã' not in m.group(2):
            continue
        nome, tempo, via = m.group(1).strip(' *'), m.group(2), m.group(3)
        fx = re.search(r'(\d+) a (\d+)', tempo)
        nums = re.findall(r'\d+', tempo)
        dias = int(fx.group(2)) if fx else int(nums[0]) if nums else 0
        T[nome] = {'dias': dias, 'tempo': tempo, 'via': via}
    return T


def acha(T, nome):
    if nome.lower() == 'ireviel':
        return 'Ireviel'
    k, sug = acha_nome(nome, T)
    if not k:
        sys.exit(f'lugar não achado na tabela do Livro: "{nome}".' + (f' Parecidos: {", ".join(sug)}.' if sug else '') + ' (viagem.py lista; ou use dias=N)')
    return k


def main():
    a = sys.argv[1:]
    T = tabela()
    if not a or a[0] == 'lista':
        print('DISTÂNCIAS A PARTIR DE IREVIEL (Livro do Mundo):')
        for n, v in T.items():
            print(f"  {n}: {v['tempo']} · {v['via']}")
        return
    if a[0] != 'vai' or len(a) < 3:
        sys.exit(__doc__)
    quem, destino = a[1], acha(T, a[2])
    op = {x.split('=')[0]: x.split('=', 1)[1] for x in a[3:] if '=' in x}
    origem = acha(T, op.get('de', 'Ireviel'))
    saida = int(op.get('saida', dia_atual()))
    if origem == destino:
        sys.exit('origem e destino são o mesmo lugar.')
    if 'dias' in op:
        dias, como = int(op['dias']), f"{op['dias']} dias (dito pelo Mestre)"
    else:
        trechos = [x for x in (origem, destino) if x != 'Ireviel']
        dias = sum(T[x]['dias'] for x in trechos)
        como = ' + '.join(f"{x} {T[x]['tempo']}" for x in trechos)
        for a_, b_ in ((origem, destino), (destino, origem)):   # 437: o Livro diz 'Levis + 4 dias a oeste': o trecho direto vale, sem passar por Ireviel (erro achado: Levis → Lumade dava 16)
            mm = re.search(re.escape(a_) + r'\s*\+\s*(\d+)\s*dias?', T[b_].get('via', '')) if a_ != 'Ireviel' else None
            if mm: dias, como = int(mm.group(1)), f"{b_}: {T[b_]['via']} (o trecho direto do Livro)"; break
    extra = []
    C = carrega('clima.json', {})
    ceu = next((v['ceu'] for k, v in C.get('hoje', {}).items() if k.split()[-1].lower() in origem.lower()), None)
    if ceu == 'tempestade':
        dias += 1; extra.append('tempestade na saída: +1 dia')
    vias = ' '.join(T[x]['via'] for x in (origem, destino) if x in T)
    if 'rio' in vias and (C.get('agua', 50) < 15 or C.get('agua', 50) >= 85):
        dias += 1; extra.append('rio seco ou em cheia: +1 dia')
    chega = saida + max(dias, 0)
    it = agenda_add(chega, f"CHEGA a {destino}: {quem} (saiu de {origem} no {saida})", tipo='marco', oculto='oculto' in a, para='para' in a, origem='viagem.py', toca=True)
    txt = f"VIAGEM: {quem} · {origem} → {destino} · sai no {saida}, {dias} dias ({como}{'; ' + '; '.join(extra) if extra else ''}) → chega no Dia {chega} [agenda #{it['id']}]"
    if 'volta' in a:
        it2 = agenda_add(chega + dias, f"VOLTA a {origem}: {quem} (de {destino})", tipo='marco', oculto='oculto' in a, para='para' in a, origem='viagem.py', toca=True)
        txt += f" · de volta a {origem} no Dia {chega + dias} [agenda #{it2['id']}]"
    if 'leva' in op:
        O = carrega('onde.json', {})
        for n in [x.strip() for x in op['leva'].split(',') if x.strip()]:
            if destino == 'Ireviel': O[n] = {'lugar': 'Ireviel', 'chega': chega, 'desde': saida, 'motivo': ''}
            else: O[n] = {'lugar': destino, 'chega': chega, 'desde': saida, 'motivo': ''}
        from nucleo import grava
        grava('onde.json', O); txt += f" · leva: {op['leva']}"
    print(txt)
    anota('- ' + ('(OCULTO) ' if 'oculto' in a else '') + txt)


if __name__ == '__main__':
    main()
