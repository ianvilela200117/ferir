#!/usr/bin/env python3
"""OBRA DO DADO (regra da casa, Dia 200; substitui a obra_aberta.py do Dia 199, que dava efeito demais).
CDs FIXAS do mundo (as mesmas para todos): Comum 15 · Incomum 25 · Raro 35 · Épico 45 · Único 55 · Lendário 70 · Mítico 85 · Primordial 100.
ROLAGEM: 2d20 EXPLOSIVOS (cada 20 rola de novo e soma, sem limite) + BASE.
BASE = média dos 4 bônus da Obra (Matéria, Processo, Técnica, Acaso) + nível ÷ 10 + 2 por ajudante (máx. +6).
TETO DURO (o material ruim não faz milagre): o menor entre
  - melhor material (≥1/5 da massa) + 1 categoria; - oficina (improvisada Incomum · comum Raro · boa Épico · mestra Lendário · lendária Mítico);
  - RECEITA (Lei 13 da casa, Dia 200): só LENDÁRIO para cima pede Receita Mestra + condição (Mítico + núcleo). Épico e Único não pedem receita.
REQUISITO DE NÍVEL para usar inteira (casa, Dia 200): Comum 1 · Incomum 5 · Raro 20 · Épico 40 · Único 70 · Lendário 110 · Mítico 180 · Primordial 260 (abaixo: rende uma categoria abaixo).
MAESTRIA (teto mole): acima da categoria natural dela, −10 por categoria (Leigo Comum · Iniciante Incomum · Treinado Raro · Mestre Único · Lendário: nenhum).
RESULTADO: a melhor categoria até o teto cujo limiar (CD + penalidade) o total alcança. Abaixo de 15: material perdido.
OS DADOS: cada 20 (também os que explodem) = +1 efeito e uma peculiaridade · os dois dados abrindo em 20 = obra-prima (1d6: 1-3 sobe uma categoria se o teto deixar; senão +1 efeito)
  · três 20 ou mais = MARAVILHA · cinco ou mais = LENDA · SOBRA no teto: +1 efeito a cada 10 acima do limiar (máx. +3; 30+ também maravilha)
  · um dado em 1 = complicação 1d6 (1 perde · 2-3 cai uma categoria · 4-6 menor) · os dois em 1 = a peça se perde · 1 em 10 obras ganha uma peculiaridade.
Uso: python3 obra_dado.py "Nome" TIPO m p t a teto=CAT nat=CAT [nivel=N] [ajud=N] [alma=1] [fortuna=N]
     python3 obra_dado.py encantar "Feitiço" CAT_DO_ITEM m p t a [nivel=N] [ajud=N] [alma=1] [fortuna=N] [nat=CAT]
TIPO: arma armadura ferramenta objeto foco
"""
import sys, secrets
sys.argv_backup = list(sys.argv)
from obra_aberta import EFEITOS, PECULIAR, MARAVILHA, ensure  # tabelas d20
from feiticos import G as GRIMORIO
CAT = ['comum','incomum','raro','epico','unico','lendario','mitico','primordial']
NOME = ['Comum','Incomum','Rara','Épica','Única','Lendária','Mítica','Primordial']
CD = [15,25,35,45,55,70,85,100]
NEF = [0,1,1,2,3,4,6,8]
XP = [5,20,80,300,800,2500,10000,50000]
MAGIA = ["Alma de Brasa (1º): a peça guarda fogo, 1x por cena +1d6","Faca Acesa (1º)","Pele de Pedra (2º): 1x por cena +4 Defesa 3 rodadas",
 "Fio de Elo (2º): 1x por dia prende um alvo","Geada de Lâmina (3º)","Sussurro (1º): 1x por dia, 20 palavras a quem o dono conhece",
 "Faísca (1º)","Flor de Brasa fraca (3º, 1x por dia)","uma magia de escola nova (1d12) de 1º círculo, sem receita: a peça a inventou"]
d = lambda n: secrets.randbelow(n)+1
def norm(s): return s.lower().replace('é','e').replace('ú','u').replace('í','i').replace('ê','e')
def die():
    ch=[d(20)]
    while ch[-1]==20: ch.append(d(20))
    return ch
def opt(a,k,default):
    for x in a:
        if x.startswith(k+'='): return x[len(k)+1:]
    return default

def roll2(base, alma, fort, need_fn):
    A=die(); B=die(); log=[f'dados de saída: {A} + {B} = {base+sum(A)+sum(B)}']; rev=0
    def tot(): return base+sum(A)+sum(B)
    for nome,n,custo in (('ALMA OUVIDA (sem Revés)',alma,0),('Fortuna (+1 Revés)',fort,1)):
        for _ in range(n):
            if not need_fn(tot(),A,B): break
            low = A if (A[0]==1 or (sum(A)<=sum(B) and B[0]!=1)) else B
            old=list(low); low[:] = die()
            log.append(f"{nome}: dado {old} → {low} (total {tot()})"); rev+=custo
    return A,B,tot(),log,rev

def main():
    a=sys.argv[1:]
    if not a: sys.exit(__doc__)
    if a[0]=='encantar':
        feit, cat = a[1], CAT.index(norm(a[2])); m,p,t,q = map(int,a[3:7])
        niv=int(opt(a,'nivel',0)); aj=min(int(opt(a,'ajud',0)),3); alma=int(opt(a,'alma',0)); fort=int(opt(a,'fortuna',0))
        nat=CAT.index(norm(opt(a,'nat','unico'))); pen=10*max(0,cat-nat)
        base=round((m+p+t+q)/4)+niv//10+2*aj; lim=CD[cat]+pen
        A,B,T,log,rev=roll2(base,alma,fort,lambda T,A,B: T<lim or A[0]==1 or B[0]==1)
        print(f'ENCANTAMENTO "{feit}" numa peça {NOME[cat]} | limiar {lim} (CD {CD[cat]}{" +"+str(pen) if pen else ""}) | base {base} (média {round((m+p+t+q)/4)} + nível {niv//10} + ajud {2*aj})')
        print(f'  dados finais: {A} + {B} → total {T}')
        for l in log: print('  '+l)
        if A[0]==1 and B[0]==1: print('  OS DOIS EM 1: o condutor se perde E A PEÇA SE QUEBRA'); return
        if T>=lim: g='INTEIRO'
        elif T>=lim-10: g='UMA VEZ MAIS FRACO (XXIII.14)'
        elif T>=lim-20: g='DUAS VEZES MAIS FRACO'
        else: g='FALHA: o condutor se perde'
        tw=sum(x==20 for x in A+B)
        print(f'  RESULTADO: {g}' + (f' · {tw} vinte(s): o feitiço sai +{tw} mais forte (um uso a mais por dia ou +2d6, pela ficção)' if tw and 'FALHA' not in g else ''))
        if (A[0]==1 or B[0]==1) and 'FALHA' not in g:
            r=d(6); print(f'  um 1 natural: complicação 1d6 [{r}] → ' + ('a peça perde 1 de durabilidade' if r>1 else 'o condutor se perde (o feitiço não pega)'))
        if rev: print(f'  Revés +{rev}')
        print(f'  XP: {XP[cat]} (Obra de encantamento {NOME[cat]})'); return
    nomep,tipo=a[0],a[1]; m,p,t,q=map(int,a[2:6])
    teto=CAT.index(norm(opt(a,'teto','raro'))); nat=CAT.index(norm(opt(a,'nat','raro')))
    niv=int(opt(a,'nivel',0)); aj=min(int(opt(a,'ajud',0)),3); alma=int(opt(a,'alma',0)); fort=int(opt(a,'fortuna',0))
    base=round((m+p+t+q)/4)+niv//10+2*aj
    lim=lambda c: CD[c]+10*max(0,c-nat)
    def cat_of(T):
        r=-1
        for c in range(teto+1):
            if T>=lim(c): r=c
        return r
    A,B,T,log,rev=roll2(base,alma,fort,lambda T,A,B: cat_of(T)<teto or A[0]==1 or B[0]==1)
    print(f'OBRA DO DADO "{nomep}" ({tipo}) | teto {NOME[teto]} | maestria natural {NOME[nat]} | base {base} (média {round((m+p+t+q)/4)} + nível {niv//10} + ajud {2*aj})')
    print('  limiares: ' + ' · '.join(f'{NOME[c]} {lim(c)}' for c in range(teto+1)))
    print(f'  dados finais: {A} + {B} → total {T}')
    for l in log: print('  '+l)
    if rev: print(f'  Revés +{rev}')
    if A[0]==1 and B[0]==1: print('  OS DOIS DADOS EM 1: A PEÇA SE PERDE (e o material)'); return
    f=cat_of(T)
    if f<0: print('  RESULTADO: abaixo de 15: MATERIAL PERDIDO'); return
    notas=[]; extra=0; marav=0
    tw=sum(x==20 for x in A+B); extra+=tw
    if A[0]==20 and B[0]==20:
        r=d(6)
        if r<=3 and f<teto: f+=1; notas.append(f'OBRA-PRIMA (os dois abriram em 20) 1d6 [{r}] → sobe a {NOME[f]}')
        else: extra+=1; notas.append(f'OBRA-PRIMA 1d6 [{r}] → +1 efeito')
    if tw>=3: marav+=1; notas.append(f'{tw} VINTES: MARAVILHA')
    if tw>=5: marav+=1; notas.append('LENDA: a peça acorda (nome próprio; o mundo fica sabendo)')
    if f==teto:
        s=T-lim(f); add=min(s//10,3)
        if add: extra+=add; notas.append(f'SOBRA {s} no teto → +{add} efeito(s)')
        if s>=30: marav+=1; notas.append('SOBRA 30+: maravilha')
        if not add: notas.append(f'sobra {s} no teto (menos de 10: nada a mais)')
    ones=[x for x in (A[0],B[0]) if x==1]
    for _ in ones:
        r=d(6)
        if r==1: notas.append('UM 1: complicação [1] → A PEÇA SE PERDE'); print('\n'.join('  '+n for n in notas)); return
        if r<=3: f=max(f-1,0); notas.append(f'UM 1: complicação [{r}] → cai a {NOME[f]}')
        else: notas.append(f'UM 1: complicação [{r}] → menor (o tempo dobra ou a ferramenta perde 1)')
    for n in notas: print('  '+n)
    nef=NEF[f]; mag=1 if f>=4 else 0
    pool=list(EFEITOS[tipo]); efs=[ensure(pool.pop(secrets.randbelow(len(pool)))) for _ in range(min(nef-mag+extra,len(pool)))]
    print(f'  RESULTADO: {nomep} — {NOME[f].upper()} · XP {XP[f]}')
    for j,e in enumerate(efs,1): print(f'    efeito {j}: {e}')
    if mag:
        pool_m=[g for g in GRIMORIO if g[1]<=(3 if f==4 else 6)]
        e_,c_,n_,ef_,t_=pool_m[d(len(pool_m))-1]
        print(f'    efeito de magia (X.2; d{len(pool_m)} do grimório): {n_} ({e_} {c_}º): {ef_} — 1x por cena, sem saber magia')
    p2=list(MARAVILHA)
    for _ in range(marav): print(f'    MARAVILHA: {ensure(p2.pop(secrets.randbelow(len(p2))))}')
    p3=list(PECULIAR); npec=tw+len(ones)+(1 if d(10)==1 else 0)
    for _ in range(npec): print(f'    PECULIARIDADE: {ensure(p3.pop(secrets.randbelow(len(p3))))}')
main()
