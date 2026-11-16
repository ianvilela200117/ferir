#!/usr/bin/env python3
"""cria.py — MOTOR 9 (G25): CRIAS E MONTARIAS (Livro Nove 8.5).

Uma cria leva UMA LUA POR DEGRAU do bicho para ficar adulta (Comum 1 ... Épico 4, Único 5), come por semana
degrau × 20 de ouro em carne, e SEM LAÇO, ao crescer, foge ou ataca (d6 1-3). Adulta: metade do nível do pai,
e daí sobe com XP como um NPC da casa (cresce.py), até o nível do pai. Teto: uma cria por 100 níveis do dono
(mínimo 1), mais o Dom Mão que Doma e a Ninhada.

Uso:
  python3 cria.py ver
  python3 cria.py nova "NOME" "o bicho que a pôs" CATEGORIA NIVEL_DO_PAI [dono=Ferir] [laco="Elo de Montaria"] [essencia=X] [montaria]
  python3 cria.py laco "NOME" "o laço" | python3 cria.py morre "NOME" "como"
  python3 cria.py semana DIA             o tick semanal chama: a comida (ficha.py cofre) e quem ficou adulta
"""
import subprocess, sys
from nucleo import d, carrega, grava, anota, dia_atual, P

ARQ = 'crias.json'
DEG = {'comum': 0, 'incomum': 1, 'raro': 2, 'epico': 3, 'unico': 4, 'lendario': 5, 'mitico': 6, 'primordial': 7}
sem = lambda s: s.lower().replace('é', 'e').replace('ú', 'u').replace('í', 'i').replace('á', 'a')


def teto(dono):
    nv = carrega('ficha.json').get('nivel', 0) if dono == 'Ferir' else (carrega('npcs.json').get(dono) or {}).get('nivel') or 0
    extra = 0
    if dono == 'Ferir':
        H = carrega('habilidades.json', {})
        extra = sum(1 for t in H.get('talentos', []) if 'Mão que Doma' in t.get('nome', ''))
    return max(1, nv // 100) + extra


def main():
    a = sys.argv[1:]; S = carrega(ARQ, {'crias': []}); C = S['crias']
    if not a or a[0] == 'ver':
        if not a: print(__doc__)
        print(f'CRIAS E MONTARIAS (G25): {len([c for c in C if c["estado"] in ("filhote", "adulta")])} de pé')
        for c in C:
            print(f"  {c['nome']} ({c['cat']}, cria de {c['pai']}) · {c['estado']}" + (f" · adulta no Dia {c['adulta_em']}" if c['estado'] == 'filhote' else f" · nível {c.get('nivel', '?')}")
                  + f" · dono: {c['dono']} · laço: {c.get('laco') or 'NENHUM'}" + (' · montaria' if c.get('montaria') else '') + f" · come {c['come']} por semana")
        return
    if a[0] == 'nova' and len(a) >= 5:
        op = {x.split('=')[0]: x.split('=', 1)[1] for x in a[5:] if '=' in x}; g = DEG[sem(a[3])]; dono = op.get('dono', 'Ferir')
        vivas = [c for c in C if c['dono'] == dono and c['estado'] in ('filhote', 'adulta')]
        if len(vivas) >= teto(dono): sys.exit(f'TETO: {dono} já tem {len(vivas)} cria(s) de {teto(dono)}.')
        dia = dia_atual(); c = {'nome': a[1], 'pai': a[2], 'cat': a[3], 'degrau': g, 'nivel_pai': int(a[4]), 'dono': dono, 'laco': op.get('laco'), 'essencia': op.get('essencia', ''),
                               'montaria': 'montaria' in a, 'nasceu': dia, 'adulta_em': dia + 30 * (g + 1), 'estado': 'filhote', 'come': max(1, g) * 20}
        C.append(c); grava(ARQ, S)
        t = f"CRIA NOVA (G25): {c['nome']}, cria de {c['pai']} ({c['cat']}), de {dono}: adulta no Dia {c['adulta_em']} com nível {c['nivel_pai'] // 2}; come {c['come']} por semana; laço: {c['laco'] or 'NENHUM (ao crescer, d6 1-3 foge ou ataca)'}"
        anota('- ' + t); print(t); return
    if a[0] in ('laco', 'morre') and len(a) >= 3:
        c = next((x for x in C if x['nome'].lower() == a[1].lower()), None) or sys.exit('cria não achada')
        if a[0] == 'laco': c['laco'] = a[2]
        else: c['estado'] = 'morta'; c['fim'] = a[2]
        grava(ARQ, S); anota(f"- CRIA {c['nome']}: {a[0]}: {a[2]}"); print(f"{c['nome']}: {a[0]}: {a[2]}"); return
    if a[0] == 'semana' and len(a) >= 2:
        dia = int(a[1]); out = []; conta = 0
        for c in C:
            if c['estado'] not in ('filhote', 'adulta'): continue
            conta += c['come']
            if c['estado'] == 'filhote' and dia >= c['adulta_em']:
                if not c.get('laco'):
                    r = d(6)
                    if r <= 3: c['estado'] = 'fugiu'; out.append(f"  ⚠ {c['nome']} cresceu SEM LAÇO: d6 [{r}] → FOGE OU ATACA (o Mestre decide pela cena; a cria deixa a casa)"); continue
                    out.append(f"  {c['nome']} cresceu sem laço: d6 [{r}] → fica (por ora)")
                c['estado'] = 'adulta'; c['nivel'] = c['nivel_pai'] // 2
                out.append(f"  ★ {c['nome']} ficou ADULTA: nível {c['nivel']} (sobe com XP até {c['nivel_pai']}); dar ficha em npcs.json e em fichas_combate.json")
        if conta:
            r = subprocess.run([sys.executable, P('ficha.py'), 'cofre', f'-{conta}', f'{dia}: a carne das crias (G25)'], capture_output=True, text=True)
            out.insert(0, f'  a carne das crias: −{conta} · ' + (r.stdout.strip().split('\n') or [''])[-1])
        grava(ARQ, S)
        if out: anota('- CRIAS (semana do ' + str(dia) + '): ' + ' · '.join(x.strip() for x in out))
        print('\n'.join(out) if out else '  (nenhuma cria na casa)'); return
    sys.exit(__doc__)


if __name__ == '__main__':
    main()
