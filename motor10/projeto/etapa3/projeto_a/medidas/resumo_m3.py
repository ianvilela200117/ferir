# resumo_m3.py: uma linha por semente da saída do m3 (a fome, o povo, a prata dos povoados, Pedra Rasa, a comida, o mundo de fora, o tempo)
# python3 projeto/etapa3/projeto_a/medidas/resumo_m3.py SAIDA_DO_M3.txt
import re, sys
t=open(sys.argv[1]).read()
for bloco in t.split('===== SEMENTE')[1:]:
    sem=bloco.split()[0]
    fomes=[int(x) for x in re.findall(r'fome (\d+) dias', bloco)]
    pr=re.findall(r'(\S+)\s+(capital|cidade|vila|aldeia)\s+povo\s+(\d+) →\s+(\d+) · prata\s+(\d+) →\s+(\d+) \(menor (\d+)', bloco)
    mins=[int(m[6])/int(m[4]) for m in pr]; fins=[int(m[5])/int(m[4]) for m in pr]
    pops=sum(int(m[3]) for m in pr)-sum(int(m[2]) for m in pr)
    pedra=[(int(m[4]),int(m[5]),int(m[6])) for m in pr if m[0]=='Rasa'][0]
    fora=re.search(r'fora: (\d+)', bloco).group(1)
    fc=re.findall(r'comida × ([\d,]+) a × ([\d,]+)', bloco); fmax=max(float(b.replace(',','.')) for a,b in fc); fmin=min(float(a.replace(',','.')) for a,b in fc)
    tm=re.search(r'TEMPO: .*?: ([\d,]+) ms por dia', bloco).group(1)
    print(f'semente {sem}: com fome {sum(1 for f in fomes if f>0)} povoados (o pior {max(fomes)} dias) · povo {pops:+d} · a prata do povoado no fim: de {min(fins):.2f} a {max(fins):.2f} da inicial (a menor do ano {min(mins):.2f}) · Pedra Rasa {pedra[0]}→{pedra[1]} (menor {pedra[2]}) · a comida de × {fmin:.2f} a × {fmax:.2f} · fora {fora} · {tm} ms/dia')
