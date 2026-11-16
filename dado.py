#!/usr/bin/env python3
"""Rolador do Mestre. Aleatoriedade real do sistema (secrets).
Uso:
  python3 dado.py 1d20+7 cd=25        teste contra CD
  python3 dado.py 1d20+7 van cd=25    vantagem (desv = desvantagem)
  python3 dado.py 3d8+2               dano
  python3 dado.py 1d6 x5              cinco rolagens separadas (dias, encontros)
  python3 dado.py lista "a" "b" "c"   sorteia um item de uma lista
"""
import re, secrets, sys, datetime

def d(lados):
    return secrets.randbelow(lados) + 1

def hora():
    return datetime.datetime.now().strftime('%H:%M:%S')

def rolar(expr, args):
    m = re.fullmatch(r'(\d*)d(\d+)([+-]\d+)?', expr.replace(' ', ''))
    if not m:
        sys.exit('expressão inválida: use NdL+M, por exemplo 1d20+5')
    n = int(m.group(1) or 1); lados = int(m.group(2)); mod = int(m.group(3) or 0)
    cd = next((int(a[3:]) for a in args if a.startswith('cd=')), None)
    modo = 'van' if 'van' in args else 'desv' if 'desv' in args else None
    if modo and lados == 20 and n == 1:
        a, b = d(20), d(20)
        nat = max(a, b) if modo == 'van' else min(a, b)
        detalhe = f'2d20 [{a}, {b}] -> {"maior" if modo == "van" else "menor"} {nat}'
        dados = [nat]
    else:
        dados = [d(lados) for _ in range(n)]
        nat = dados[0] if n == 1 else None
        detalhe = f'{n}d{lados} {dados}'
    total = sum(dados) + mod
    linha = f'{detalhe} {"+" if mod >= 0 else "-"} {abs(mod)} = {total}'
    if lados == 20 and n == 1:
        if nat == 20:
            linha += ' | 20 NATURAL'
        elif nat == 1:
            linha += ' | 1 NATURAL'
    if cd is not None:
        if lados == 20 and n == 1:
            if nat == 1:
                ok = False
            elif nat == 20:
                ok = total >= cd - 5     # 20 natural vence se o total chegou a 5 da CD
            else:
                ok = total >= cd
        else:
            ok = total >= cd
        linha += f' vs CD {cd} -> {"SUCESSO" if ok else "FALHA"}'
    return linha

def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    if args[0] == 'lista':
        itens = args[1:]
        i = secrets.randbelow(len(itens))
        print(f'[{hora()}] lista de {len(itens)} -> [{i + 1}] {itens[i]}')
        return
    vezes = next((int(a[1:]) for a in args if re.fullmatch(r'x\d+', a)), 1)
    for k in range(vezes):
        pref = f' #{k + 1}' if vezes > 1 else ''
        print(f'[{hora()}]{pref} {rolar(args[0], args[1:])}')

if __name__ == '__main__':
    main()
