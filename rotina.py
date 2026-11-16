#!/usr/bin/env python3
"""rotina.py — a ROTINA DE DADOS DA SEMANA (MOTOR 6): rotina.json.

Toda semana o Mestre declarava de novo, à mão, as mesmas tabelas "de sempre" (o laço, o chamado, quais vínculos
se movem...) e depois rolava. Agora as tabelas fixas moram em rotina.json: o tick semanal declara e rola todas
pelo selo (ficam no envelope como DECLARADO e ROLADO, com a etiqueta DIA-nome).

Uso:
  python3 rotina.py ver                 as tabelas fixas da semana
  python3 rotina.py semana DIA          declara e rola todas as ativas (o tick semanal chama sozinho)
  python3 rotina.py liga NOME | desliga NOME
Para mudar uma tabela "de sempre" (um laço novo, um vínculo que acabou), edite rotina.json: cada item tem
nome, titulo, dado, tabela (no formato do selo.py), e pode ter x (quantas vezes), nomes e oculto.
"""
import sys
from nucleo import carrega, grava
import selo

ARQ = 'rotina.json'


def main():
    a = sys.argv[1:]
    R = carrega(ARQ, {'itens': []})
    if not a or a[0] == 'ver':
        for i in R['itens']:
            print(f"{'●' if i.get('ativo', True) else '○'} {i['nome']}: {i['titulo']} · {i['dado']}" + (f" × {i['x']}" if i.get('x', 1) > 1 else '') + f" · {i['tabela']}")
        return
    if a[0] in ('liga', 'desliga') and len(a) > 1:
        for i in R['itens']:
            if i['nome'] == a[1]:
                i['ativo'] = a[0] == 'liga'
                print(f"{i['nome']}: {'ligada' if i['ativo'] else 'desligada'}")
        grava(ARQ, R)
        return
    if a[0] == 'semana' and len(a) > 1:
        dia = a[1]
        S = selo.load()
        ids = []
        for i in R['itens']:
            if not i.get('ativo', True):
                continue
            sid = f"{dia}-{i['nome']}"
            if sid in S['selos']:
                print(f'({sid}) já rolado nesta semana.')
                continue
            o = {'oculto': bool(i.get('oculto')), 'x': max(int(i.get('x', 1)), len(i.get('nomes', []))), 'nomes': i.get('nomes', [])}
            ids.append(selo.declara(S, sid, i['titulo'], i['dado'], i['tabela'], o, quieto=True))
        for sid in ids:
            s = selo.rola(S, sid, quieto=True)
            print(f"ROLADO ({sid}) {'(OCULTO) ' if s['oculto'] else ''}{s['titulo']}: " + ' · '.join(r['txt'] for r in s['rolagens']))
        return
    print(__doc__)


if __name__ == '__main__':
    main()
