import secrets
d=lambda n: secrets.randbelow(n)+1
def dd(n,s): return [d(s) for _ in range(n)]
T=102; DEF_AGUA=22; DEF_PEDRA=18; RD=1
print('O PLANO DA ELIANE: ganchos cravados (seguram no gelo), todos amarrados; o BREN grita o nome; 4 arpões; puxar para a pedra; depois martelo e lanças.')
# rodada 0: o nome
print('RODADA 1: o BREN grita "TISTIR!" (fraqueza: o nome: ele vem direto a quem chamou, sai da espuma até a pedra da margem; nesta rodada não empurra).')
a=d(20); x=a+8; print(f'  Tistir ataca o Bren: [{a}]+8={x} vs Def 16 -> '+(f'ACERTA {int(sum(dd(2 if a==20 else 1,10))*1.5)}' if (x>=16 and a!=1) or a==20 else 'erra (o escudo do Bren)'))
fis=0
for nome,b in (('Sira',10),('cavaleiro 1',8),('cavaleiro 2',8),('Ferir',22)):
    r=d(20); ok=(r+b>=DEF_PEDRA and r!=1) or r==20
    if ok: fis+=1
    print(f'  arpão de {nome}: [{r}]+{b}={r+b} vs {DEF_PEDRA} -> '+('FISGA' if ok else 'erra'))
print(f'  arpões presos: {fis}')
na_pedra=False
if fis>=2:
    p=d(20)+8+2*fis; t=d(20)+8
    na_pedra=p>t
    print(f'  PUXAR (ancorados, +8 +2 por arpão = +{8+2*fis}): {p} vs Tistir {t} -> '+('NA PEDRA: fora da água' if na_pedra else 'ele segura na espuma'))
def golpe(nome,b,dfs,dado,mult,soma,rd=True):
    global T
    r=d(20)
    if r==1 or (r+b<dfs and r!=20): print(f'    {nome}: [{r}]+{b}={r+b} vs {dfs} -> erra'); return
    n=2 if r==20 else 1; x=int(sum(dd(n,dado))*mult)+soma-(RD if rd else 0); T-=x
    print(f'    {nome}: [{r}]+{b}={r+b} vs {dfs} -> {x}'+(' CRÍTICO' if r==20 else '')+f' (Tistir {T})')
rod=1
while T>0 and rod<=6:
    dfs=DEF_PEDRA if na_pedra else DEF_AGUA
    print(f'RODADA {rod} {"(na pedra)" if na_pedra else "(na espuma, +4 Def)"}:')
    golpe('Eliane (Épica, ignora RD)',28,dfs,10,3,10,rd=False)
    if T>0: golpe('Ferir ("Brasa")',22,dfs,8,2.5,4)
    if T>0:
        for i in range(1,6):
            if T<=0: break
            golpe(f'cavaleiro {i} (lança)',9,dfs,8,1,5)
    if T>0:
        a=d(20); x=a+8
        if rod%3==0:
            print(f'  Tistir EMPURRA (área 6 m): os amarrados nos ganchos não caem; um cavaleiro sem amarra? não: todos amarrados -> ninguém no rio')
        tgt=['Ferir','Eliane','Bren','Sira'][d(4)-1]; dfs2={'Ferir':30,'Eliane':34,'Bren':16,'Sira':14}[tgt]
        if (x>=dfs2 and a!=1) or a==20:
            print(f'  Tistir golpeia {tgt}: [{a}]+8={x} vs {dfs2} -> ACERTA {int(sum(dd(2 if a==20 else 1,10))*1.5)} (RD do alvo à parte)')
        else: print(f'  Tistir golpeia {tgt}: [{a}]+8={x} vs {dfs2} -> erra')
        if not na_pedra and fis>=1:
            p=d(20)+8+2*fis; t=d(20)+8; na_pedra=p>t; print(f'  puxar de novo: {p} vs {t} -> '+('NA PEDRA' if na_pedra else 'segura na espuma'))
    rod+=1
print('FIM: Tistir '+('MORTO' if T<=0 else f'ainda com {T} PV'))
