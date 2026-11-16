#!/usr/bin/env python3
"""Régua dos barcos contra a Elaeva (Dia 361; sem valor de jogo). A regra de magia do luta.py: o monstro resiste com 2d20+at
contra a CD+14 (metade se passar); depois a RD. Uma cena por dia. A Elaveva não alcança os barcos (30 m; o espinheiro vai a 18 m)."""
import random, statistics as st
d=lambda n: random.randint(1,n)
def dados(q,f): return sum(d(f) for _ in range(q))
def ex():  # d20 que explode no 20
    t=0
    while True:
        r=d(20); t+=r
        if r!=20: return t
PV=37000; RD=50; AT=122; DF=132
# MOTOR 6.1 (Dia 379): MAGIA DISPUTADA. O atirador joga 2d20 + ataque contra a Defesa + 14 (146): em cheio = inteiro; resiste = metade; 20 que morde = dobra.
ATQ={'Mamiltia':134,'Moreth':44,'Eiagrir':36,'Ferir':34,'Arpão':34}
import sys
EXTRA=[]   # tiros a mais (ex.: uma peça nova): python3 sims/elaeva_barcos.py "Arpão,2,12,10"
for a in sys.argv[1:]:
    n_,v_,q_,m_=a.split(','); EXTRA.append((n_,int(v_),int(q_),float(m_),30))
TIRO=[('Mamiltia',2,8,20,30),('Moreth',2,16,10,30),('Eiagrir',2,16,5,30),('Ferir',7,8,5,30)]
def cerco():
    pv=PV; dias=0; dano_por={k[0]:0 for k in TIRO+EXTRA}
    for dia in range(20):
        frac=pv/PV
        if frac<0.25 and d(6)<=4: return pv,'foi embora (abaixo de 25%)',dia,dano_por
        if frac<0.50 and d(6)<=2: return pv,'foi embora (abaixo de 50%)',dia,dano_por
        if d(6)<=2: continue          # longe da costa hoje
        for nome,vezes,q,mult,cd in TIRO+EXTRA:
            for _ in range(vezes):
                a1=d(20); a2=d(20); t=a1+a2+ATQ.get(nome,34)
                crit=(a1==20 and a2>=11) or (a2==20 and a1>=11)
                dm=int(dados(q*(2 if crit else 1),6)*mult)
                if not crit and t<DF+14: dm//=2
                if a1==1 and a2==1: dm=0
                liq=max(dm-RD,0); pv-=liq; dano_por[nome]+=liq
                if pv<=0: return 0,'MORTA',dia,dano_por
    return pv,'ficou (20 dias)',20,dano_por
N=5000; R=[cerco() for _ in range(N)]
mort=sum(1 for r in R if r[1]=='MORTA')/N
fim={}
for r in R: fim[r[1]]=fim.get(r[1],0)+1
perda=[1-r[0]/PV for r in R]
print(f'{N} cercos · a Elaeva MORRE {mort:.1%} · fim: '+' · '.join(f'{k} {v/N:.0%}' for k,v in fim.items()))
print(f'dano que ela leva: média {st.mean(perda):.0%} do PV · pior 5% (o mais dano) {sorted(perda)[int(0.95*N)]:.0%} · dias de cerco, média {st.mean(r[2] for r in R):.1f}')
tot={k:st.mean(r[3][k] for r in R) for k in R[0][3]}
print('dano médio por atirador no cerco inteiro: '+' · '.join(f'{k} {int(v)}' for k,v in tot.items()))
print('mortes dos nossos: 0 (os barcos ficam fora do alcance; o risco é o barco chegar perto: não modelado)')
