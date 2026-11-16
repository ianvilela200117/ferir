#!/usr/bin/env python3
"""Motor de Mundo v5. Uma Obra (forja, alquimia, costura, engenharia, joalheria, culinária, encantamento).
Uso: python3 obra.py "Nome" alvo materia processo tecnica quarto [fortuna=N] [teto=CATEGORIA] [protegida] [cd=N] [van=TESTE] [desv=TESTE]
  alvo: Comum Incomum Raro Epico Unico Lendario Mitico Primordial
  materia/processo/tecnica: bônus totais desses testes (atributo ÷ 5 + maestria + ferramenta + oficina + material; sem teto, v5)
  quarto: bônus do 4º teste (Acaso = Sorte ÷ 5 + metade da maestria; ou Paciência = Vontade ÷ 5 + metade da maestria, com tempo dobrado)
  fortuna=N: pontos de Fortuna que o jogador aceita gastar nesta obra (máximo 1 por teste)
  teto=CATEGORIA: o teto que material, maestria e oficina permitem (padrão: o próprio alvo)
  protegida: a complicação do 1 natural nunca destrói a peça (técnica de campanha); o 1 no d6 vira "cai uma categoria"
  cd=N: CD usada nos três primeiros testes, quando uma regra da campanha muda a CD (o quarto teste usa N - 10); a Forja de Alma, por exemplo, usa a CD de três categorias abaixo
  van=TESTE / desv=TESTE: vantagem ou desvantagem num teste (materia, processo, tecnica ou quarto); separe vários com vírgula
Exemplo: python3 obra.py "Espada do vau" Raro 24 23 25 15 teto=Epico
"""
import sys, secrets, datetime

CAT = ['Comum', 'Incomum', 'Raro', 'Épico', 'Único', 'Lendário', 'Mítico', 'Primordial']
CHAVE = ['comum', 'incomum', 'raro', 'epico', 'unico', 'lendario', 'mitico', 'primordial']
d = lambda n: secrets.randbelow(n) + 1
norm = lambda x: x.lower().replace('é', 'e').replace('ú', 'u').replace('í', 'i')

def teste(bonus, cd, modo=None):
    if modo:
        a, b = d(20), d(20)
        r = max(a, b) if modo == 'van' else min(a, b)
        par = f'2d20 [{a}, {b}] -> '
    else:
        r = d(20); par = ''
    t = r + bonus
    if r == 1: ok = False
    elif r == 20: ok = t >= cd - 5
    else: ok = t >= cd
    return r, t, ok, par

def main():
    a = sys.argv[1:]
    if len(a) < 6:
        sys.exit(__doc__)
    nome = a[0]
    alvo = CHAVE.index(norm(a[1]))
    bonus = list(map(int, a[2:6]))
    fortuna = next((int(x[8:]) for x in a if x.startswith('fortuna=')), 0)
    teto = next((CHAVE.index(norm(x[5:])) for x in a if x.startswith('teto=')), alvo)
    protegida = 'protegida' in a
    cd = next((int(x[3:]) for x in a if x.startswith('cd=')), 15 + 5 * alvo)
    cds = [cd, cd, cd, cd - 10]
    TES = ['materia', 'processo', 'tecnica', 'quarto']
    modos = [None] * 4
    for x in a:
        for m in ('van', 'desv'):
            if x.startswith(m + '='):
                for k in x[len(m) + 1:].split(','):
                    modos[TES.index(norm(k).replace('ã', 'a'))] = m
    nomes = ['Matéria', 'Processo', 'Técnica', 'Acaso ou Paciência']
    if alvo >= 6:
        print('  LEMBRETE: Mítico pede NÚCLEO (coração Épico+, relíquia ou 1 ano de vida); Primordial pede núcleo Lendário ou Mítico')
    print(f'[{datetime.datetime.now().strftime("%H:%M:%S")}] OBRA "{nome}" | alvo {CAT[alvo]} | CD {cd} (Acaso ou Paciência: CD {cd - 10})')
    suc = n20 = n1 = gastos = 0
    for lab, b, c, m in zip(nomes, bonus, cds, modos):
        r, t, ok, par = teste(b, c, m)
        linha = f'  {lab}: {par}[{r}] + {b} = {t} vs {c} -> {"SUCESSO" if ok else "FALHA"}'
        if not ok and gastos < fortuna:
            gastos += 1
            r, t, ok, par = teste(b, c, m)
            linha += f' | Fortuna: {par}[{r}] + {b} = {t} -> {"SUCESSO" if ok else "FALHA"}'
        print(linha)
        suc += ok
        n20 += (r == 20 and ok)   # só o 20 natural que deu sucesso vale efeito
        n1 += (r == 1)
    if gastos:
        print(f'  Fortuna gasta: {gastos} (+{gastos} de Revés)')
    if suc <= 1:
        print('  RESULTADO: material perdido')
        return
    cat = alvo - (4 - suc)
    efeitos = n20
    if suc == 4 and n20 >= 2:
        if alvo + 1 <= teto:
            cat += 1; efeitos = 0
            print('  Dois 20 naturais com quatro sucessos: OBRA-PRIMA, +1 categoria')
        else:
            print('  Dois 20 naturais com quatro sucessos: OBRA-PRIMA, mas o teto não permite subir; vira efeitos extras')
    if n1:
        c = d(6)
        if c == 1 and not protegida:
            print(f'  1 natural -> complicação 1d6 [{c}]: a peça se perde')
            print('  RESULTADO: material perdido')
            return
        if c <= 3:
            cat -= 1
            extra_p = ' (protegida: não se perde)' if c == 1 else ''
            print(f'  1 natural -> complicação 1d6 [{c}]: cai uma categoria{extra_p}')
        else:
            print(f'  1 natural -> complicação 1d6 [{c}]: complicação menor (tempo dobrado ou a ferramenta perde 1 de durabilidade)')
    cat = max(0, min(cat, 7))
    extra = f' com {efeitos} efeito(s) extra(s) dos 20 naturais' if efeitos else ''
    print(f'  RESULTADO: {CAT[cat]}{extra}')

if __name__ == '__main__':
    main()
