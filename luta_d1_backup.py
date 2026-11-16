#!/usr/bin/env python3
"""LEI DA FERA v2 + LEI DAS AÇÕES — combate de um contra muitos (regra da casa, Dia 203, pedido do jogador).
Dia 202: "o monstro tem uma rodada e nós temos cinco". Dia 203: "uma Lendária contra 10 nível 30 batendo 1 cada e ela 1 também é injusto;
e o monstro ficar mais forte porque mais gente luta contra ele não é justo, a não ser que seja poder dele".

O QUE VALE (para TODOS: gente e monstro, dos dois lados):
 1. AÇÕES POR RODADA = 1 + nível ÷ 60 (máx. 8): 1-59 → 1 · 60-119 → 2 · 120-179 → 3 · 180-239 → 4 · 240-299 → 5 · 300-359 → 6 · 360-419 → 7 · 420+ → 8.
    MONSTRO soma o CORPO da categoria (poder dele, não do grupo): Raro +1 · Épico +2 · Único +2 · Lendário +3 · Mítico +4 · Primordial +5.
    O número de inimigos NÃO dá ação a ninguém. (Só um PODER do próprio monstro pode: "furia_bando": +1 ação a cada 3 inimigos além do 1º, máx. +2.)
 2. SEM FÔLEGO DE GRUPO: o PV não cresce porque o grupo é grande (só com o poder "folego_bando").
 3. GOLPE QUE VARRE: quando um golpe derruba (0 PV) alguém com METADE do nível de quem bateu ou menos, o golpe segue
    no próximo ao alcance (1 vez por ação). O grande atravessa a fila de pequenos.
 4. REAÇÃO (contra-golpe em quem acerta um golpe forte (10% do PV máximo) ou crítico):
    monstro pela categoria (Raro 1 · Épico 2 · Único 2 · Lendário 3 · Mítico 4 · Primordial 5);
    gente pelo nível (120+ → 1 · 240+ → 2 · 360+ → 3).
 5. COURO do monstro: RD mínima pela categoria (Raro 5 · Épico 10 · Único 15 · Lendário 25 · Mítico 40 · Primordial 60).
 6. PODER do monstro: Raro a cada 2 rodadas, Épico ou mais toda rodada (gasta 1 ação). FÚRIA abaixo de 50% (+1 ação, o poder recarrega).
    MORAL abaixo de 25% (1-3 foge).
 7. GENTE: recua com PV a 40% (heróis 25%), 1-4 no d6. 0 PV (motor X.6): desacordado, teste de morte d20 vs 12 (3 falhas morre,
    3 sucessos estável); DANO MACIÇO (mais da metade do PV máximo num golpe) mata; depois da luta, estancar = Medicina CD 15.
 7b. MÃO DA EXPERIÊNCIA: todo golpe de arma ou garra soma NÍVEL ÷ 5 ao dano (o veterano sabe onde bater). Feitiço não (o foco já multiplica).
 8. O 20 MORDE (acerta sempre, dados dobrados, RD pela metade, +1 dado por 20 extra). O 1 erra.
 8b. CERCO (Dia 205, pedido do jogador): a guarda de cada um cobre por rodada tantos golpes quanto as AÇÕES dele; cada golpe a mais
    que ele recebe na mesma rodada acha uma brecha: −1 na Defesa, acumulando, até −7. Vale para os dois lados.
 9. NOME: gritar o nome (gasta 1 ação de quem grita) tira do monstro 1 ação e o poder na rodada. FRAQUEZA: dano × 2 e corta regeneração.
Uso: python3 luta.py ARQUIVO.json [sim=N]
ARQUIVO: {"monstro":{nome,cat,nivel,pv,pv_atual?,df,rd,at,dado,mult,b?,poder?,veneno?,fraqueza?,inteligente?,moral?,gente?,furia_bando?,folego_bando?},
          "grupo":[{nome,nivel,at,dado,mult,b,df,rd,pv,essencia?,chega?,grita?,magia?,so20?,heroi?,vigor?,agi?,medicina?,imune_empurrao?}]}
"""
import sys, json, secrets, random
RDCAT={'Comum':0,'Incomum':2,'Raro':5,'Épico':10,'Único':15,'Lendário':25,'Mítico':40,'Primordial':60}
ACAT={'Comum':0,'Incomum':0,'Raro':1,'Épico':2,'Único':2,'Lendário':3,'Mítico':4,'Primordial':5}
REACAT={'Comum':0,'Incomum':0,'Raro':1,'Épico':2,'Único':2,'Lendário':3,'Mítico':4,'Primordial':5}
SIM=False
CERCO=(1,7)   # Dia 205: −1 na Defesa por golpe além das ações do alvo na rodada, até −7
def d(n): return random.randint(1,n) if SIM else secrets.randbelow(n)+1
def ex():
    ch=[d(20)]
    while ch[-1]==20: ch.append(d(20))
    return ch
def dados(s,crit=False,plus=0):
    n,f=map(int,s.split('d')); n=n*(2 if crit else 1)+plus
    return [d(f) for _ in range(n)]
def P(*a):
    if not SIM: print(*a)
def fraco(g,M): return bool(g.get('essencia')) and g.get('essencia')==M.get('fraqueza')   # Dia 205: sem Essência não dobra (erro achado)
def acoes(nivel): return max(1,min(8,1+nivel//60))
def reac_gente(nivel): return 3 if nivel>=360 else 2 if nivel>=240 else 1 if nivel>=120 else 0

def luta(F):
    M=dict(F['monstro']); G=[dict(g) for g in F['grupo']]
    for g in G:
        g.setdefault('vivo',True); g.setdefault('fora',0); g['pvmax']=g.get('pvmax_real',g['pv']); g.setdefault('nivel',20)   # Dia 205: o máximo VERDADEIRO (luta retomada no meio)
        g['ac']=g.get('acoes',acoes(g['nivel']))
    nini=len(G); gente=M.get('gente',False)
    mult=min(1.5,1+0.10*(nini-1)) if M.get('folego_bando') else 1.0
    pvmax=int(M['pv']*mult); frac=M.get('pv_atual',M['pv'])/M['pv']; M['pvm']=pvmax; M['pva']=int(pvmax*frac)
    if not gente: M['rd']=max(M.get('rd',0),RDCAT.get(M.get('cat','Comum'),0))
    base_ac=M.get('acoes',acoes(M['nivel'])+(0 if gente else ACAT.get(M.get('cat','Comum'),0)))+(min(2,(nini-1)//3) if M.get('furia_bando') else 0)
    reac_max=reac_gente(M['nivel']) if gente else REACAT.get(M.get('cat','Comum'),0)
    P(f"LEI DAS AÇÕES: {M['nome']} (nível {M['nivel']}) contra {nini} · PV {M['pva']}/{pvmax} · RD {M['rd']} · {base_ac} ações · reação {reac_max} · grupo: "+', '.join(f"{g['nome']} {g['ac']}" for g in G))
    furia=False; recarga=False; rnd=0; ultimo=None; moral_feito=False; morreu=[]
    while M['pva']>0 and rnd<F.get('ate',40):
        rnd+=1; P(f'--- RODADA {rnd} · {M["nome"]} {M["pva"]}/{pvmax}')
        reac=reac_max; M['golpes']=0
        for g in G: g['reac']=reac_gente(g['nivel']); g['golpes']=0
        for g in G:
            if g['vivo'] and g.get('veneno',0)>0:
                x=sum(dados(M['veneno']['dado'])); g['pv']-=x; g['veneno']-=1; P(f'  veneno em {g["nome"]}: −{x} ({g["pv"]})')
                if g['pv']<=0: cai(g,0,morreu)
        for g in G:
            if not g['vivo'] or g.get('chega',1)>rnd or M['pva']<=0: continue
            if g['fora']>0: g['fora']-=1; P(f'  {g["nome"]} volta'); continue
            for k in range(g['ac']):
                if not g['vivo'] or M['pva']<=0: break
                if k==0 and g.get('grita'):
                    M['calado']=True; P(f'  {g["nome"]} GRITA O NOME: "{M["nome"].upper()}!"'); continue
                mg=g.get('magia')
                if k==0 and mg and mg.get('rodada')==rnd:
                    dm=int(sum(dados(mg['dano']))*mg.get('mult',1)); sv=sum(ex())+M['at']; dd=max((dm//2 if sv>=mg['cd'] else dm)-M['rd'],0)
                    if fraco(g,M): dd*=2
                    M['pva']-=dd; ultimo=g; P(f'  {g["nome"]} lança: {dm}; resiste {sv} vs {mg["cd"]} → {dd} ({M["pva"]})'); continue
                ch=ex(); t=sum(ch)+g['at']; crit=ch[0]==20
                M['golpes']+=1; brecha=min(CERCO[1],CERCO[0]*max(0,M['golpes']-base_ac)); dfM=M['df']-brecha
                if ch[0]==1 or (t<dfM and not crit) or (g.get('so20') and not crit): P(f'  {g["nome"]}: {ch}+{g["at"]}={t} vs {dfM} erra'); continue
                dd_=dados(g['dado'],crit=crit,plus=(len(ch)-1 if crit else 0)); br=int(sum(dd_)*g['mult'])+g['b']+g['nivel']//5
                rd=M['rd']//2 if crit else M['rd']; liq=max(br-rd,0)
                if fraco(g,M): liq*=2
                M['pva']-=liq; ultimo=g
                P(f'  {g["nome"]}: {ch}+{g["at"]}={t} ACERTA{" CRÍTICO" if crit else ""} {dd_}×{g["mult"]}+{g["b"]}+{g['nivel']//5}={br} − RD {rd}{" ×2" if fraco(g,M) else ""} = {liq} ({M["pva"]})')
                if M['pva']>0 and reac>0 and (liq>=pvmax*0.10 or crit):
                    reac-=1; P('  REAÇÃO:'); ataque(M,g,G,morreu,rnd)
        if M['pva']<=0: P(f'  {M["nome"]} CAI'); break
        if not gente and not furia and M['pva']<pvmax*0.5: furia=True; recarga=True; P('  FÚRIA: +1 ação, o poder recarrega')
        if M.get('moral',True) and not moral_feito and M['pva']<pvmax*0.25:
            moral_feito=True; m=d(6); P(f'  MORAL d6 [{m}] → '+('FOGE' if m<=3 else 'luta até cair'))
            if m<=3:
                gu=[g for g in G if g['vivo'] and g.get('guarda_fuga')]
                if gu and M.get('fuga'):
                    a=sum(ex())+M['fuga']; b=sum(ex())+gu[0]['guarda_fuga']; P(f'  FUGA: {M["nome"]} {a} × {gu[0]["nome"]} na saída {b}')
                    if b>=a: P('  FUGA BARRADA: luta até cair'); m=6
                if m<=3: fim_caidos(G,morreu); return dict(res='fugiu',rnd=rnd,mortos=morreu,pv=M['pva'],pvm=pvmax,G=G)
        ac=base_ac+(1 if furia else 0)
        calado=M.pop('calado',False)
        if calado: ac-=1
        poder=M.get('poder'); per=1 if REACAT.get(M.get('cat','Comum'),0)>=2 else 2
        if poder and not calado and (per==1 or rnd%2==1 or recarga):
            recarga=False; ac-=1; area(M,G,rnd,morreu)
        for _ in range(max(ac,0)):
            V=vivos(G,rnd)
            if not V: break
            ataque(M,alvo_de(M,V,ultimo),G,morreu,rnd,varre=True)
        testes_morte(G,morreu)
        if not [g for g in G if g['vivo']]: P('  O GRUPO CAI'); fim_caidos(G,morreu); return dict(res='grupo caiu',rnd=rnd,mortos=morreu,pv=M['pva'],pvm=pvmax,G=G)
    if M['pva']<=0 or not F.get('ate'): fim_caidos(G,morreu)   # Dia 205: rodada a rodada ('ate') não estanca de graça no fim
    return dict(res='morto' if M['pva']<=0 else 'empate',rnd=rnd,mortos=morreu,pv=M['pva'],pvm=pvmax,G=G)

def vivos(G,rnd): return [g for g in G if g['vivo'] and g.get('chega',1)<=rnd and g['fora']==0]
def alvo_de(M,V,ultimo):
    r=d(6)
    if M.get('inteligente'): return min(V,key=lambda g:g['pv'])
    if r<=3 and ultimo in V: return ultimo
    if r==6: return min(V,key=lambda g:g['pvmax'])
    return V[d(len(V))-1]

def cai(g,liq,morreu):
    g['vivo']=False
    if liq>g['pvmax']/2: morreu.append(g['nome']); P(f'    {g["nome"]} MORRE (dano maciço)')
    else: g['caido']=True; g['falhas']=0; g['suc']=0; P(f'    {g["nome"]} CAI DESACORDADO')

def testes_morte(G,morreu):
    for g in G:
        if not g.get('caido') or g.get('estavel') or g['nome'] in morreu: continue
        r=d(20)
        if r>=12: g['suc']+=1
        else: g['falhas']+=1
        P(f'  teste de morte de {g["nome"]}: [{r}] vs 12 ({g["suc"]} sucessos, {g["falhas"]} falhas)')
        if g['falhas']>=3: morreu.append(g['nome']); P(f'  {g["nome"]} MORRE')
        elif g['suc']>=3: g['estavel']=True; P(f'  {g["nome"]} fica ESTÁVEL')

def fim_caidos(G,morreu):
    for _ in range(6):
        pend=[g for g in G if g.get('caido') and not g.get('estavel') and g['nome'] not in morreu]
        if not pend: return
        med=[g for g in G if (g['vivo'] or g.get('recuou')) and g['pv']>0]
        for c in pend:
            if med:
                h=max(med,key=lambda x:x.get('medicina',0)); r=d(20)+h.get('medicina',0)
                if r>=15: c['estavel']=True; P(f'  {h["nome"]} estanca {c["nome"]} (Medicina {r} vs 15): ESTÁVEL'); continue
                P(f'  {h["nome"]} tenta estancar {c["nome"]} (Medicina {r} vs 15): não')
        testes_morte(G,morreu)

def ataque(M,g,G,morreu,rnd,varre=False):
    ch=ex(); t=sum(ch)+M['at']; crit=ch[0]==20; g['golpes']=g.get('golpes',0)+1
    df=g['df']+(g.get('aura_def',[0,0])[0] if g.get('aura_def') else 0)-min(CERCO[1],CERCO[0]*max(0,g['golpes']-g['ac']))
    if ch[0]==1 or (t<df and not crit): P(f'    ataque em {g["nome"]}: {ch}+{M["at"]}={t} vs {df} erra'); return
    dd_=dados(M['dado'],crit=crit,plus=(len(ch)-1 if crit else 0)); br=int(sum(dd_)*M['mult'])+M.get('b',0)+M['nivel']//5; rd=g['rd']//2 if crit else g['rd']; liq=max(br-rd,0)
    g['pv']-=liq; s=f'    ataque em {g["nome"]}: {ch}+{M["at"]}={t} vs {df} ACERTA{" CRÍTICO" if crit else ""} {dd_}×{M["mult"]}+{M.get("b",0)}+{M['nivel']//5}={br} − RD {rd} = {liq} ({g["pv"]})'
    if M.get('veneno') and g['pv']>0:
        vg=sum(ex())+g.get('vigor',10)
        if vg<M['veneno']['cd']: g['veneno']=M['veneno']['rodadas']; s+=f' · VENENO (Vigor {vg})'
    P(s)
    if g['pv']<=0:
        cai(g,liq,morreu)
        if varre and g['nivel']*2<=M['nivel']:
            V=vivos(G,rnd)
            if V: P('    GOLPE QUE VARRE: segue no próximo'); ataque(M,V[d(len(V))-1],G,morreu,rnd,varre=False)
        return
    # contra-golpe de gente de nível alto
    if g.get('reac',0)>0 and (liq>=g['pvmax']*0.10 or crit) and M['pva']>0:
        g['reac']-=1; c2=ex(); t2=sum(c2)+g['at']; cr2=c2[0]==20
        if c2[0]!=1 and (t2>=M['df'] or cr2):
            dd2=dados(g['dado'],crit=cr2); br2=int(sum(dd2)*g['mult'])+g['b']+g['nivel']//5; l2=max(br2-(M['rd']//2 if cr2 else M['rd']),0)
            if fraco(g,M): l2*=2
            M['pva']-=l2; P(f'    CONTRA-GOLPE de {g["nome"]}: {c2} → {l2} ({M["pva"]})')
    lim=0.25 if g.get('heroi') else 0.40
    if g['pv']<=g['pvmax']*lim and not g.get('fica'):
        r=d(6)
        if r<=4: g['vivo']=False; g['recuou']=True; P(f'    {g["nome"]} RECUA ferido (d6 [{r}])')

def area(M,G,rnd,morreu):
    p=M['poder']; P(f'  PODER: {p.get("nome","poder")}')
    for g in G:
        if not g['vivo'] or g.get('chega',1)>rnd or g['fora']>0: continue
        if d(6)>3: continue
        if p['tipo']=='area_empurra':
            if g.get('imune_empurrao'): P(f'    {g["nome"]}: não se mexe'); continue
            a=sum(ex())+g.get('agi',6)
            if a<p['cd']:
                q=d(6)+d(6); g['pv']-=q; g['fora']=1; P(f'    {g["nome"]}: Agilidade {a} vs {p["cd"]} → CAI (−{q}, {g["pv"]})')
                if g['pv']<=0: cai(g,q,morreu)
            else: P(f'    {g["nome"]}: segura ({a})')
        else:
            dm=sum(dados(p['dano'])); a=sum(ex())+g.get('agi',6); dm=dm//2 if a>=p['cd'] else dm; g['pv']-=dm
            P(f'    {g["nome"]}: {dm} ({g["pv"]})')
            if g['pv']<=0: cai(g,dm,morreu)

if __name__=='__main__':
    F=json.load(open(sys.argv[1])); n=next((int(x[4:]) for x in sys.argv[2:] if x.startswith('sim=')),0)
    if n:
        SIM=True; from collections import Counter; c=Counter(); mortes=Counter(); rs=[]
        for _ in range(n):
            r=luta(F); c[r['res']]+=1; rs.append(r['rnd'])
            for m in r['mortos']: mortes[m]+=1
        print(f'SIMULAÇÃO {n} lutas (sem valor de jogo):', {k:f'{100*v/n:.0f}%' for k,v in c.items()}, '· rodadas médias', round(sum(rs)/n,1))
        print('  chance de cada um morrer:', {k:f'{100*v/n:.0f}%' for k,v in mortes.most_common()})
    else:
        r=luta(F); print('FIM:', r['res'], '· rodadas', r['rnd'], '· mortos', r['mortos'], '· PV', f"{r['pv']}/{r['pvm']}", '· grupo', {g['nome']:g['pv'] for g in r['G']})
