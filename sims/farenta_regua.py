import random, statistics as st
d=lambda n: random.randint(1,n)
def batalha(mamiltia=False):
    far=1000; coal_baixas=0
    # F2 muralha: trebuchete; o mago e as pedras param 1 dia com 1-4 (só atrasa)
    # F3 assalto: até 3 trocas
    pedra = d(6)  # cinza saciado anula: 1-3 a névoa · 4-6 a Lança do Moreth
    nevoa_ok = pedra>3; moreth_ok = pedra<=3
    eiag = 2
    for troca in range(3):
        if mamiltia:
            far -= far  # um exército
            break
        a=d(20)+18; b=d(20)+13+3
        m=a-b
        if m>=5: far -= (m//5)*100
        elif m<=-5: coal_baixas += ((-m)//5)*100
        far -= d(6)*20  # Skotha
        far -= d(6)*20  # Teraseth
        if troca==0 and nevoa_ok: far -= d(6)*100
        if troca==0 and moreth_ok: far -= d(6)*20
        if eiag>0: far -= d(6)*20; eiag-=1
        coal_baixas += d(6)*20//2 + d(6)*10   # a Leliel (÷2 na hoste de Épicas) e o mago
        if far<=200: break
        perdidos=1000-far
        if perdidos>=300 and d(6)>=4: break
    return far, coal_baixas
for mam in (False, True):
    R=[batalha(mam) for _ in range(20000)]
    vit=sum(1 for f,c in R if f<=200 or (1000-f)>=300)/len(R)
    cb=[c for f,c in R]
    print('COM a Mamiltia' if mam else 'SEM a Mamiltia', '· Farenta cai ou se rende:', f'{vit:.0%}', '· baixas da coalizão: média', round(st.mean(cb)), '· pior 5%:', sorted(cb)[int(0.95*len(cb))])
