#!/usr/bin/env python3
"""atlas.py — MOTOR 9 (G37): O ATLAS DE MASMORRAS do mundo (Livro Nove 16).

O mundo tem lugares fechados que esperam: ruínas, tumbas, torres, minas. O atlas guarda todos; a casa só vê os que
CONHECE (por ter entrado, por carta, por boato). Toda semana, d20: com 18 ou mais um BOATO de um lugar que a casa
não conhecia chega a uma cidade do reino (com o nome, a região e o que se diz que guarda; o degrau, só indo lá).
O mapa de salas (masmorra.py gera) só nasce quando a casa entra ou manda olhos.

Uso:
  python3 atlas.py ver [tudo]          o que a casa conhece (com "tudo": também os ocultos; só o Mestre)
  python3 atlas.py nova [N]            gera N lugares novos, ocultos (gerador lugar; nome livre; degrau e região no dado)
  python3 atlas.py conhece "NOME" "como soube"
  python3 atlas.py semana DIA          o tick semanal chama: o dado do boato
"""
import os, sys
from nucleo import d, carrega, grava, anota, P

ARQ = 'atlas.json'
REG = ['o Delta e o Brejo', 'as Montanhas Hegre', 'a Mata de Elais', 'o Deserto de Sal', 'as Montanhas de Fogo', 'o Sul da Areia', 'o Norte', 'os Picos Brancos',
       'Kremir e Zisrir', 'Telosus e o Oeste', 'o Vale do Leve de cima', 'Steunn']
CATS = ['Raro', 'Raro', 'Épico', 'Épico', 'Épico', 'Único', 'Único', 'Lendário']   # d8


def semeia():
    M = carrega('mundo_vivo.json'); L = []
    for x in M.get('lugares_novos', []):
        limpo = lambda s: str(s or '').split(' (OCULTO')[0]
        L.append({'nome': x['nome'], 'onde': limpo(x.get('onde')), 'era': x.get('o_que_era'), 'caiu': x.get('por_que_caiu'), 'guarda': limpo(x.get('guarda')), 'habita': limpo(x.get('habita')),
                  'entrar': limpo(x.get('entrar')), 'degrau': 'Único' if x['nome'] == 'Zythir' else '?', 'conhecida': True, 'como': 'lugar do mundo vivo (mundo_vivo.json)'})
    L += [{'nome': 'Alnesar', 'onde': 'as colinas a leste de Ireviel, a 2 dias', 'era': '?', 'caiu': '?', 'guarda': 'numa metade, um NÚCLEO e nada mora lá; na outra, bandidos guardam um segredo de facção', 'habita': 'bandidos numa metade',
           'entrar': 'uma luta de um lado; uma chave do outro', 'degrau': '?', 'conhecida': True, 'como': 'a Tessal e a Lile acharam nos papéis (427)'},
          {'nome': 'Quoium', 'onde': 'a escada afundada onde mora o Laennor', 'era': '?', 'caiu': '?', 'guarda': '?', 'habita': 'o Laennor, o Redemoinho, mora por cima', 'entrar': 'passar pelo Laennor', 'degrau': '?', 'conhecida': True, 'como': 'cânone'},
          {'nome': 'Iroule', 'onde': '?', 'era': '?', 'caiu': '?', 'guarda': '?', 'habita': '?', 'entrar': 'uma senha: estava nos papéis do velho, na letra do pai do rei', 'degrau': '?', 'conhecida': True, 'como': 'cânone'}]
    return L


def main():
    a = sys.argv[1:]
    if not os.path.exists(P(ARQ)): grava(ARQ, {'nota': 'o atlas de masmorras (G37). conhecida: a casa sabe que existe.', 'lugares': semeia()})
    S = carrega(ARQ); L = S['lugares']
    if not a or a[0] == 'ver':
        if not a: print(__doc__)
        vis = [x for x in L if x['conhecida'] or 'tudo' in a]
        print(f"O ATLAS DE MASMORRAS (G37): a casa conhece {len([x for x in L if x['conhecida']])} de {len(L) if 'tudo' in a else '?'}")
        for x in vis:
            mapa = os.path.exists(P('masmorras', x['nome'].lower().replace(' ', '_') + '.json'))
            print(f"  {'' if x['conhecida'] else '(OCULTO) '}{x['nome']} · {x['onde']} · degrau {x['degrau'] if (x['conhecida'] and x['degrau'] != '?') or 'tudo' in a else '?'}"
                  + f" · era {x['era']}; caiu por {x['caiu']} · guarda: {x['guarda']} · habita: {x['habita']} · entrar: {x['entrar']}" + (' · MAPA DE SALAS GERADO' if mapa else '') + f" · ({x.get('como', '')})")
        return
    if a[0] == 'nova':
        import gerador as G, subprocess
        n = int(a[1]) if len(a) > 1 else 1; novos = []
        for _ in range(n):
            g = G.lugar(); r = subprocess.run([sys.executable, P('nomes.py'), ['arcaica', 'aspera', 'sibilante', 'liquida', 'mercante', 'montanhesa'][d(6) - 1], '1', 'livre'], capture_output=True, text=True)
            nome = r.stdout.strip().split(',')[0].strip() if r.stdout.strip() and 'nenhum' not in r.stdout else g['nome']
            x = {'nome': nome, 'onde': REG[d(12) - 1], 'era': g['o que era'], 'caiu': g['por que caiu'], 'guarda': g['o que guarda'], 'habita': g['o que habita'], 'entrar': g['custo de entrar'],
                 'degrau': CATS[d(8) - 1], 'conhecida': False, 'como': ''}
            L.append(x); novos.append(f"{x['nome']} ({x['degrau']}; {x['onde']}): era {x['era']}, caiu por {x['caiu']}; guarda {x['guarda']}; habita {x['habita']}; entrar: {x['entrar']}")
        grava(ARQ, S); anota('- (OCULTO) ATLAS (G37): lugares novos no mundo, que a casa não conhece: ' + ' | '.join(novos)); print(f'{n} lugar(es) novo(s) no atlas (OCULTO, no envelope)'); return
    if a[0] == 'conhece' and len(a) >= 3:
        x = next((y for y in L if y['nome'].lower() == a[1].lower()), None) or sys.exit('lugar não achado no atlas')
        x['conhecida'] = True; x['como'] = a[2]; grava(ARQ, S); anota(f"- ATLAS: a casa passa a conhecer {x['nome']} ({x['onde']}): {a[2]}"); print(f"{x['nome']}: conhecida ({a[2]})"); return
    if a[0] == 'semana' and len(a) >= 2:
        oc = [x for x in L if not x['conhecida']]; r = d(20)
        if r >= 18 and oc:
            x = oc[d(len(oc)) - 1]; x['conhecida'] = True; x['como'] = f'boato que chegou no {a[1]}'
            grava(ARQ, S); t = f"BOATO DE MASMORRA (d20 [{r}]): fala-se de {x['nome'].upper()}, em {x['onde']}: era {x['era']}, caiu por {x['caiu']}; dizem que guarda {x['guarda']} (o degrau, só indo lá)"
            anota('- ATLAS (G37): ' + t); print('  ' + t)
        else: print(f'  o dado do boato de masmorra: d20 [{r}]: nada novo' + ('' if oc else ' (não há lugar oculto: atlas.py nova)'))
        return
    sys.exit(__doc__)


if __name__ == '__main__':
    main()
