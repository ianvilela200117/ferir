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
 8c. DOIS DADOS (Dia 207, pedido do jogador): o ataque é 2d20 + ataque (cada 20 explode à parte) contra a DEFESA + 14
    (o +14 guarda o valor da guarda do veterano: com +10 o enxame de fracos passava a ganhar tudo; simulado 10 mil lutas).
    O 20 MORDE (crítico, acerta sempre, RD pela metade) só se o OUTRO dado der 11+; cada 20 da jogada soma +1 dado no crítico.
    DOIS 1: erra sempre. Testes de resistência na luta (veneno, área, magia, fuga, Medicina): 2d20, CD +14 (Medicina +10: 25).
    O teste de morte continua 1 d20 contra 12 (a vida por um fio não muda). 'um_dado' na linha de comando roda a regra velha.
 8d. INICIATIVA (Dia 379, revisão de combate): no começo, cada lado rola 2d20 + nível ÷ 10 (o grupo usa a média). Quem ganha age primeiro
    na rodada 1. Antes o grupo agia sempre primeiro, e em fichas iguais isso dava 55% a 61% de vitória só pela ordem. Surpresa segue valendo
    (quem é surpreendido não age na rodada 1 e não rola). 'ini=nao' na linha de comando desliga.
 8e. MAGIA DISPUTADA (Dia 379, revisão de combate): o feitiço de dano joga como golpe: 2d20 + ataque do lançador contra a Defesa + 14 do alvo.
    Pega em cheio: dano inteiro · o alvo resiste: metade · 20 que morde: dados dobrados · dois 1: o feitiço se desfaz. Depois a RD e a fraqueza.
    Antes o ALVO resistia com 2d20 + o ataque dele contra CD 30 + 14, igual para todo lançador: monstro de nível 155 para cima resistia SEMPRE
    e bicho pequeno NUNCA, fosse o lançador um aprendiz ou a Mamiltia. 'magia=velha' roda a regra antiga.
 9. NOME: gritar o nome (gasta 1 ação de quem grita) tira do monstro 1 ação e o poder na rodada. FRAQUEZA: dano × 2 e corta regeneração.
Uso: python3 luta.py ARQUIVO.json [sim=N]   ("surpresa":1 no arquivo: o monstro não age na rodada 1)
MOTOR 6 (Dia 379; as regras da luta são as mesmas):
  python3 luta.py ARQ sim=2000 [seed=7]   a régua agora mostra a DISTRIBUIÇÃO: desfechos, duração, quanto sobra do bicho, quem morre,
                                          quem cai ou recua, e o veredito pela LEI DAS CAÇADAS (2% de morte). seed= repete a mesma régua.
  python3 luta.py ARQ regua=2000          o mesmo, e grava a régua no envelope como OCULTO (o Mestre não copia à mão).
  Arquivo com campo faltando avisa qual campo falta antes de rolar qualquer dado.
ARQUIVO: {"monstro":{nome,cat,nivel,pv,pv_atual?,df,rd,at,dado,mult,b?,poder?,veneno?,fraqueza?,inteligente?,moral?,gente?,furia_bando?,folego_bando?,reflete? (425: magia volta no 18-20), covil? {nome,dano,cd,efeito}, MOTOR 9 (438): regenera? N por rodada (a fraqueza corta) · prende? [{nome,cd,teste}] (olhar, teia: 1 alvo por rodada perde a vez) · fase? {tipo 1-6, fraqueza?, covil?} aos 50% · devolve? 0.25 · sangue_queima? 'NdL' · enxame? · casca? · duas_vidas? · come_magia? · faro_ferida? · dono_territorio? · cria_ventre? · agarra? · devora_metal? · essencia? (a do golpe dele) · no grupo: veneno_golpe? {dado,rodadas,cd}, servo?, segundo_coracao? N, rd_ess? {Essência: N}, voz_mando?, vontade?, forca? · na magia/Arte: area?, efeito? (quebra_guarda|derruba|sangra|dobra_se_caido), ignora_rd? 0.5, cd_efeito? · grito? {cd} (437: o GRITO QUE DÁ MEDO, G16 AMEDRONTADO; no grupo: vontade_medo? N) e lendarias? N (G13, 433: o covil age no começo da rodada; Lendário 1, Mítico 2, Primordial 3 ações lendárias por padrão)},
          "grupo":[{nome,nivel,at,dado,mult,b,df,rd,pv,essencia?,chega?,grita?,magia?,so20?,heroi?,vigor?,agi?,medicina?,imune_empurrao?}]}
"""
import sys, json, secrets, random
RDCAT={'Comum':0,'Incomum':2,'Raro':5,'Épico':10,'Único':15,'Lendário':25,'Mítico':40,'Primordial':60}
ACAT={'Comum':0,'Incomum':0,'Raro':1,'Épico':2,'Único':2,'Lendário':3,'Mítico':4,'Primordial':5}
REACAT={'Comum':0,'Incomum':0,'Raro':1,'Épico':2,'Único':2,'Lendário':3,'Mítico':4,'Primordial':5}
SIM=False
CERCO=(1,7)   # Dia 205: −1 na Defesa por golpe além das ações do alvo na rodada, até −7
DOIS=True     # Dia 207 (pedido do jogador): DOIS DADOS. Todo d20 de teste vira 2d20 (cada 20 explode à parte); todo alvo fixo (Defesa, CD) +OFF
OFF=14
CRITMODO='20e11'
MAGIA='disputada'   # Dia 379: 'velha' = o alvo resistia com 2d20 + ataque dele contra CD + 14 (sempre ou nunca)
INICIATIVA=True     # Dia 379: os dois lados rolam quem age primeiro
FUMMODO='11'
def d(n): return random.randint(1,n) if SIM else secrets.randbelow(n)+1
def ex1():
    ch=[d(20)]
    while ch[-1]==20: ch.append(d(20))
    return ch
def ex():   # a soma da jogada (lista achatada): 2 dados explosivos (ou 1, no modo velho)
    return ex1()+ex1() if DOIS else ex1()
def jog():
    A=ex1(); B=ex1() if DOIS else None
    t=sum(A)+(sum(B) if B else 0); n20=A.count(20)+(B.count(20) if B else 0)
    if not DOIS: return dict(t=t,ch=A,crit=A[0]==20,fum=A[0]==1,extra=n20)
    nat=(A[0],B[0])
    if CRITMODO=='um20': crit=20 in nat
    elif CRITMODO=='20e11': crit=(nat[0]==20 and nat[1]>=11) or (nat[1]==20 and nat[0]>=11)
    else: crit=nat==(20,20)
    fum=(nat[0]==1 and nat[1]<=10) or (nat[1]==1 and nat[0]<=10) if FUMMODO=='1e10' else nat==(1,1)
    return dict(t=t,ch=[A,B],crit=crit,fum=fum,extra=n20)
def dados(s,crit=False,plus=0):
    n,f=map(int,s.split('d')); n=n*(2 if crit else 1)+plus
    return [d(f) for _ in range(n)]
def P(*a):
    if not SIM: print(*a)
def _sa(s):   # MOTOR 9: 'Podridao' (o gerador) e 'Podridão' (as fichas) são a mesma Essência
    import unicodedata
    return ''.join(c for c in unicodedata.normalize('NFD',str(s or '')) if unicodedata.category(c)!='Mn').lower()
def fraco(g,M): return bool(g.get('essencia')) and _sa(g.get('essencia'))==_sa(M.get('fraqueza'))   # Dia 205: sem Essência não dobra (erro achado)
def acoes(nivel): return max(1,min(8,1+nivel//60))
def reac_gente(nivel): return 3 if nivel>=360 else 2 if nivel>=240 else 1 if nivel>=120 else 0

LENDCAT={'Lendário':1,'Lendario':1,'Mítico':2,'Mitico':2,'Primordial':3}   # G13 (Dia 433, pedido do jogador)

def luta(F):
    M=dict(F['monstro']); G=[dict(g) for g in F['grupo']]
    for g in G:
        g.setdefault('vivo',True); g.setdefault('fora',0); g['pvmax']=g.get('pvmax_real',g['pv']); g.setdefault('nivel',20)   # Dia 205: o máximo VERDADEIRO (luta retomada no meio)
        g['ac']=g.get('acoes',acoes(g['nivel']))
    nini=len(G); gente=M.get('gente',False)
    if any(g.get('voz_mando') for g in G):   # MOTOR 9 (Dom Voz de Mando): os aliados de quem manda têm +1 no ataque
        for g in G:
            if not g.get('voz_mando'): g['at']=g['at']+1
    mult=min(1.5,1+0.10*(nini-1)) if M.get('folego_bando') else 1.0
    pvmax=int(M['pv']*mult); frac=M.get('pv_atual',M['pv'])/M['pv']; M['pvm']=pvmax; M['pva']=int(pvmax*frac)
    if not gente: M['rd']=max(M.get('rd',0),RDCAT.get(M.get('cat','Comum'),0))
    base_ac=M.get('acoes',acoes(M['nivel'])+(0 if gente else ACAT.get(M.get('cat','Comum'),0)))+(min(2,(nini-1)//3) if M.get('furia_bando') else 0)
    reac_max=reac_gente(M['nivel']) if gente else REACAT.get(M.get('cat','Comum'),0)
    P(f"LEI DAS AÇÕES: {M['nome']} (nível {M['nivel']}) contra {nini} · PV {M['pva']}/{pvmax} · RD {M['rd']} · {base_ac} ações · reação {reac_max} · grupo: "+', '.join(f"{g['nome']} {g['ac']}" for g in G))
    furia=False; recarga=False; rnd=0; ultimo=None; moral_feito=False; morreu=[]
    primeiro_m=False
    if INICIATIVA and F.get('iniciativa',True) and not F.get('surpresa') and G:   # INICIATIVA (Dia 379): antes o grupo agia sempre primeiro
        bm=M.get('ini',M['nivel']//10); bg=int(sum(g.get('ini',g['nivel']//10) for g in G)/len(G))
        while True:
            im=sum(ex())+bm; ig=sum(ex())+bg
            if im!=ig: break
        primeiro_m=im>ig
        P(f"INICIATIVA: {M['nome']} 2d20+{bm} = {im} × o grupo 2d20+{bg} (média) = {ig} → "+(f"{M['nome']} AGE PRIMEIRO" if primeiro_m else 'o grupo age primeiro'))
    while M['pva']>0 and rnd<F.get('ate',40):
        rnd+=1; P(f'--- RODADA {rnd} · {M["nome"]} {M["pva"]}/{pvmax}')
        reac=reac_max; M['golpes']=0
        for g in G: g['reac']=reac_gente(g['nivel']); g['golpes']=0
        for g in G:
            if g['vivo'] and g.get('veneno',0)>0:
                x=sum(dados(M['veneno']['dado'])); g['pv']-=x; g['veneno']-=1; P(f'  veneno em {g["nome"]}: −{x} ({g["pv"]})')
                if g['pv']<=0: cai(g,0,morreu)
        gr=M.get('grito')   # 437: o GRITO QUE DÁ MEDO (traço do gerador; G16 AMEDRONTADO: não avança contra o que teme, −2 no ataque; Vontade a cada rodada para sair)
        if gr and M['pva']>0:
            cdg=gr.get('cd',15)+(OFF if DOIS else 0)
            for g in vivos(G,rnd):
                if g.get('medo'):
                    sv=sum(ex())+g['nivel']//10+g.get('vontade_medo',0)
                    if sv>=cdg: g['medo']=False; P(f"  {g['nome']} sacode o medo (Vontade {sv} vs {cdg})")
            if not M.get('_gritou') and not (F.get('surpresa') and rnd==1):
                M['_gritou']=True; P(f"  GRITO de {M['nome']}: Vontade contra {cdg}")
                for g in vivos(G,rnd):
                    sv=sum(ex())+g['nivel']//10+g.get('vontade_medo',0)
                    if sv<cdg: g['medo']=True
                    P(f"    {g['nome']}: {sv} → "+('AMEDRONTADO (só feitiço de longe; −2 no ataque)' if g.get('medo') else 'firme'))
        if M.get('_qg') and rnd>M['_qg']: M['df']+=2; M.pop('_qg')   # MOTOR 9: a Quebra-Guarda dura 1 rodada
        if M.get('_sangra',0)>0 and M['pva']>0:
            x=max(2,int(pvmax*0.02)); M['pva']-=x; M['_sangra']-=1; P(f"  {M['nome']} sangra: −{x} ({M['pva']})")
        if M.get('_veneno',[0])[0]>0 and M['pva']>0:
            x=sum(dados(M['_veneno'][1])); M['pva']-=x; M['_veneno'][0]-=1; P(f"  veneno em {M['nome']}: −{x} ({M['pva']})")
        if M.get('regenera') and 0<M['pva']<pvmax and M.get('_fraco_r')!=rnd-1 and rnd>1:   # MOTOR 9: o traço 'regenera' existia no gerador e não rodava; a fraqueza corta
            x=min(M['regenera'],pvmax-M['pva']); M['pva']+=x; P(f"  {M['nome']} regenera: +{x} ({M['pva']})")
        for pr in M.get('prende',[]):   # MOTOR 9 (438): o OLHAR que paralisa e a TEIA que prende: um alvo por rodada; falhou, perde a vez (e segue sendo alvo)
            V=vivos(G,rnd)
            if M['pva']<=0 or not V or (F.get('surpresa') and rnd==1): break
            g=alvo_de(M,V,ultimo); cdp=pr.get('cd',20)+(OFF if DOIS else 0)
            sv=sum(ex())+g['nivel']//10+g.get('forca' if pr.get('teste')=='forca' else 'vontade',0)
            if sv<cdp: g['preso_r']=1
            P(f"  {pr.get('nome','o olhar').upper()} em {g['nome']}: {sv} vs {cdp} → "+('PRESO: perde a vez' if sv<cdp else 'resiste'))
        for _ in range(2 if M.get('dono_territorio') else 1): covil_age(M,G,rnd,morreu)
        for g in G:
            if not g['vivo'] or g.get('chega',1)>rnd or M['pva']<=0 or (rnd==1 and primeiro_m): continue
            if g['fora']>0: g['fora']-=1; P(f'  {g["nome"]} volta'); continue
            if g.get('preso_r'): g['preso_r']=0; P(f'  {g["nome"]} está PRESO: perde a vez'); continue
            for k in range(g['ac']):
                if not g['vivo'] or M['pva']<=0: break
                if k==0 and g.get('agarrado'):   # MOTOR 9: AGARRADO: a 1ª ação é tentar sair
                    sv=sum(ex())+g['nivel']//10+g.get('forca',0); cda=10+M['nivel']//10+(OFF if DOIS else 0)
                    if sv>=cda: g['agarrado']=False; g['df']+=2
                    P(f'  {g["nome"]} tenta se soltar: {sv} vs {cda} → '+('SOLTO' if sv>=cda else 'segue agarrado')); continue
                if k==0 and g.get('grita'):
                    M['calado']=True; P(f'  {g["nome"]} GRITA O NOME: "{M["nome"].upper()}!"'); continue
                mg=None   # 426 (G9): a ficha pode ter VÁRIOS feitiços ('magias'); vale o primeiro que tem esta rodada
                for _m in (g.get('magias') or ([g['magia']] if g.get('magia') else [])):
                    _rr=_m.get('rodada'); _rr=_rr if isinstance(_rr,list) else [_rr]
                    if rnd in _rr: mg=_m; break
                if g.get('medo') and not (k==0 and mg): continue   # 437: AMEDRONTADO não avança contra o que teme (o feitiço de longe vale)
                if k==0 and mg and rnd in (mg.get('rodada') if isinstance(mg.get('rodada'),list) else [mg.get('rodada')]):   # Dia 299: 'rodada' pode ser lista (a Maça lança 2x por cena; antes contava 1: erro achado)
                    if MAGIA=='velha':
                        dm=int(sum(dados(mg['dano']))*mg.get('mult',1)); sv=sum(ex())+M['at']; dd=max((dm//2 if sv>=mg['cd']+(OFF if DOIS else 0) else dm)-M['rd'],0); txt_m=f'resiste {sv} vs {mg["cd"]}'
                    else:   # MAGIA DISPUTADA (Dia 379): o lançador joga 2d20 + ataque contra a Defesa + 14 do alvo, como um golpe
                        Jm=jog(); tm=Jm['t']+mg.get('at',g['at'])-(2 if g.get('medo') else 0); dfm=M['df']+(OFF if DOIS else 0)
                        if Jm['fum']: dm=0; txt_m=f'{Jm["ch"]} DOIS 1: o feitiço se desfaz'
                        elif Jm['crit']: dm=int(sum(dados(mg['dano'],crit=True))*mg.get('mult',1)); txt_m=f'{Jm["ch"]}+{mg.get("at",g["at"])}={tm} CRÍTICO (dados dobrados)'
                        elif tm>=dfm: dm=int(sum(dados(mg['dano']))*mg.get('mult',1)); txt_m=f'{Jm["ch"]}+{mg.get("at",g["at"])}={tm} vs {dfm} pega em cheio'
                        else: dm=int(sum(dados(mg['dano']))*mg.get('mult',1))//2; txt_m=f'{Jm["ch"]}+{mg.get("at",g["at"])}={tm} vs {dfm} o alvo resiste: metade'
                        cheio=dm>0 and ('cheio' in txt_m or 'CRÍTICO' in txt_m)
                        if cheio and mg.get('efeito')=='dobra_se_caido' and (M.get('calado') or M.get('_caido')==rnd): dm*=2; txt_m+=' · o alvo no chão: dobra'
                        dd=max(dm-int(M['rd']*(1-mg.get('ignora_rd',0))),0)
                        if cheio and mg.get('efeito'):   # MOTOR 9 (G30): o efeito da Arte só vale quando pega em cheio
                            ef=mg['efeito']
                            if ef=='quebra_guarda' and not M.get('_qg'): M['df']-=2; M['_qg']=rnd+1; txt_m+=' · QUEBRA-GUARDA (−2 de Defesa por 1 rodada)'
                            elif ef=='sangra': M['_sangra']=3; txt_m+=' · SANGRANDO (3 rodadas)'
                            elif ef=='derruba':
                                svm=sum(ex())+M['nivel']//10; cde=mg.get('cd_efeito',25)+(OFF if DOIS else 0)
                                if svm<cde: M['calado']=True; M['_caido']=rnd; txt_m+=f' · DERRUBADO ({svm} vs {cde}): perde 1 ação e o poder'
                                else: txt_m+=f' · firma o pé ({svm} vs {cde})'
                    if M.get('enxame'): dd=dd*2 if mg.get('area') else dd//2
                    if fraco({'essencia': mg.get('essencia', g.get('essencia'))},M): dd*=2; M['_fraco_r']=rnd
                    elif M.get('come_magia') and M.get('_comeu')!=rnd and dd>0:
                        M['_comeu']=rnd; M['pva']=min(pvmax,M['pva']+dd); P(f'  {g["nome"]} lança: {dm}; {txt_m} → COME A MAGIA: +{dd} ({M["pva"]})'); continue   # 407: a magia pode declarar a Essência dela ("" = nenhuma); sem declarar, vale a do lançador, como antes
                    if M.get('reflete') and dd>0:   # 425: o traço "reflete magia com 18 a 20" existia nas fichas e não rodava (achado ao montar o Morek)
                        rf=d(20)
                        if rf>=18:
                            g['pv']-=dd; P(f'  {g["nome"]} lança: {dm}; {txt_m} → REFLETIDA (d20 [{rf}]): {dd} voltam em {g["nome"]} ({g["pv"]})')
                            if g['pv']<=0: cai(g,dd,morreu)
                            continue
                    M['pva']-=dd; ultimo=g; P(f'  {g["nome"]} lança{(" " + mg["nome"]) if mg.get("nome") else ""}: {dm}; {txt_m} → {dd} ({M["pva"]})'); continue
                J=jog(); ch=J['ch']; t=J['t']+g['at']; crit=J['crit']
                M['golpes']+=1; brecha=min(CERCO[1],CERCO[0]*max(0,M['golpes']-base_ac)); dfM=M['df']+(OFF if DOIS else 0)-brecha
                if J['fum'] or (t<dfM and not crit) or (g.get('so20') and not crit):
                    P(f'  {g["nome"]}: {ch}+{g["at"]}={t} vs {dfM} erra'+(' · DEVORA METAL: a arma perde 1 categoria' if J['fum'] and M.get('devora_metal') else '')); continue
                dd_=dados(g['dado'],crit=crit,plus=(J['extra'] if crit else 0)); br=int(sum(dd_)*g['mult'])+g['b']+g['nivel']//5
                rd=M['rd']//2 if crit else M['rd']; liq=max(br-rd,0)
                if fraco(g,M): liq*=2; M['_fraco_r']=rnd
                if M.get('enxame'): liq//=2
                M['pva']-=liq; ultimo=g
                P(f'  {g["nome"]}: {ch}+{g["at"]}={t} ACERTA{" CRÍTICO" if crit else ""} {dd_}×{g["mult"]}+{g["b"]}+{g['nivel']//5}={br} − RD {rd}{" ×2" if fraco(g,M) else ""} = {liq} ({M["pva"]})')
                if liq>0 and g.get('veneno_golpe') and M['pva']>0 and not M.get('_veneno',[0])[0]:   # MOTOR 9: o veneno do golpe de um aliado (o Zyza)
                    vg=g['veneno_golpe']; svm=sum(ex())+M['nivel']//10
                    if svm<vg.get('cd',16)+(OFF if DOIS else 0): M['_veneno']=[vg.get('rodadas',3),vg.get('dado','2d6')]; P(f'    o veneno de {g["nome"]} pega ({svm})')
                if liq>0 and (M.get('devolve') or M.get('sangue_queima')):   # MOTOR 9: pele que devolve / sangue que queima
                    x=int(liq*M.get('devolve',0))+(sum(dados(M['sangue_queima'])) if M.get('sangue_queima') else 0)
                    if x>0:
                        g['pv']-=x; P(f'    {g["nome"]} leva {x} de volta ({g["pv"]})')
                        if g['pv']<=0: cai(g,x,morreu); break
                if M['pva']>0 and reac>0 and (liq>=pvmax*0.10 or crit):
                    reac-=1; P('  REAÇÃO:'); ataque(M,g,G,morreu,rnd)
        if M['pva']<=0 and M.get('duas_vidas') and not M.get('_viveu'):   # MOTOR 9: DUAS VIDAS
            M['_viveu']=True; M['pva']=pvmax//4; M['fraqueza']=M['duas_vidas'] if isinstance(M['duas_vidas'],str) else None
            P(f"  {M['nome']} CAI... e LEVANTA com {M['pva']} (duas vidas; outra Essência)")
        if M['pva']<=0: P(f'  {M["nome"]} CAI'); break
        nl=M.get('lendarias', 0 if gente else LENDCAT.get(M.get('cat','Comum'),0))   # G13: AÇÕES LENDÁRIAS: golpes fora da vez, em quem o feriu por último
        for _ in range(nl):
            V=vivos(G,rnd)
            if not V: break
            P('  AÇÃO LENDÁRIA:'); ataque(M,ultimo if ultimo in V else V[d(len(V))-1],G,morreu,rnd)
        if not gente and not furia and M['pva']<pvmax*0.5: furia=True; recarga=True; P('  FÚRIA: +1 ação, o poder recarrega')
        if M.get('casca') and not M.get('_rachou') and M['pva']<pvmax*0.5: M['_rachou']=True; M['rd']//=2; base_ac+=1; P(f"  A CASCA RACHA: RD {M['rd']} e +1 ação")
        fs=M.get('fase')   # MOTOR 9 (G33): a SEGUNDA FASE dos chefes aos 50%
        if fs and not M.get('_fase') and M['pva']<pvmax*0.5:
            M['_fase']=True; tp=fs.get('tipo')
            if tp in (1,5): M['fraqueza']=fs.get('fraqueza'); P(f"  SEGUNDA FASE: troca de Essência (a fraqueza agora: {M['fraqueza'] or 'nenhuma conhecida'})")
            elif tp==2: base_ac+=1; P('  SEGUNDA FASE: chama crias (+1 ação)')
            elif tp==3: M['covil']=fs.get('covil',M.get('covil')); P('  SEGUNDA FASE: o covil muda')
            elif tp in (4,6):
                P('  SEGUNDA FASE: '+('foge para outra sala do covil: a luta recomeça lá' if tp==4 else 'FALA: oferece um trato (Lei 15)'))
                fim_caidos(G,morreu); return dict(res='fase',rnd=rnd,mortos=morreu,pv=M['pva'],pvm=pvmax,G=G)
        if M.get('moral',True) and not moral_feito and M['pva']<pvmax*0.25:
            moral_feito=True; m=d(6); P(f'  MORAL d6 [{m}] → '+('FOGE' if m<=3 else 'luta até cair'))
            if m<=3:
                gu=[g for g in G if g['vivo'] and g.get('guarda_fuga')]
                if gu and M.get('fuga'):
                    a=sum(ex())+M['fuga']; b=sum(ex())+gu[0]['guarda_fuga']; P(f'  FUGA: {M["nome"]} {a} × {gu[0]["nome"]} na saída {b}')
                    if b>=a: P('  FUGA BARRADA: luta até cair'); m=6
                if m<=3: fim_caidos(G,morreu); return dict(res='fugiu',rnd=rnd,mortos=morreu,pv=M['pva'],pvm=pvmax,G=G)
        if F.get('surpresa') and rnd==1: P('  SURPRESA: ele não age nesta rodada'); continue   # Dia 208: a casa pegou de surpresa (teste aberto antes)
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
    if M['pva']<=0 and M.get('cria_ventre'): P(f"  CRIA NO VENTRE: {d(6)} cria(s) saem do corpo (um degrau abaixo; uma pode ser levada viva: G25)")
    if M['pva']<=0 or not F.get('ate'): fim_caidos(G,morreu)   # Dia 205: rodada a rodada ('ate') não estanca de graça no fim
    return dict(res='morto' if M['pva']<=0 else 'empate',rnd=rnd,mortos=morreu,pv=M['pva'],pvm=pvmax,G=G)

def covil_age(M,G,rnd,morreu):
    cv=M.get('covil')   # G13 (Dia 433): o COVIL age no começo da rodada (d6: 1-2 respira · 3-5 um alvo · 6 todos, metade)
    if cv and M['pva']>0:
        rc=d(6); V=vivos(G,rnd)
        alvos=[] if rc<=2 or not V else ([V[d(len(V))-1]] if rc<=5 else V)
        P(f"  COVIL ({cv.get('nome','o covil')}) d6 [{rc}]: "+('respira' if not alvos else ('um alvo' if rc<=5 else 'TODOS (metade)')))
        for g in alvos:
            sv=d(20)+g['nivel']//10; dm=sum(dados(cv.get('dano','4d6')))
            if rc==6: dm//=2
            liq=0 if sv>=cv.get('cd',20) and rc==6 else (dm//2 if sv>=cv.get('cd',20) else dm)
            liq=max(liq-g['rd']//2,0); g['pv']-=liq
            P(f"    {g['nome']}: resiste [{sv}] vs {cv.get('cd',20)} → {liq}"+(f" · {cv['efeito']}" if cv.get('efeito') and sv<cv.get('cd',20) else '')+f" ({g['pv']})")
            if g['pv']<=0: cai(g,liq,morreu)

def vivos(G,rnd): return [g for g in G if g['vivo'] and g.get('chega',1)<=rnd and g['fora']==0]
def alvo_de(M,V,ultimo):
    r=d(6)
    if M.get('inteligente') or M.get('faro_ferida'): return min(V,key=lambda g:g['pv'])
    if r<=3 and ultimo in V: return ultimo
    if r==6: return min(V,key=lambda g:g['pvmax'])
    return V[d(len(V))-1]

def cai(g,liq,morreu):
    if g.get('segundo_coracao',0)>0:   # MOTOR 9 (Dom): 1x por dia, a 0 PV fica com 1 e segue
        g['segundo_coracao']-=1; g['pv']=1; P(f'    {g["nome"]} cai... e fica de pé com 1 (SEGUNDO CORAÇÃO)'); return
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
                h=max(med,key=lambda x:x.get('medicina',0)); r=(d(20)+d(20) if DOIS else d(20))+h.get('medicina',0)
                if r>=15+(10 if DOIS else 0): c['estavel']=True; P(f'  {h["nome"]} estanca {c["nome"]} (Medicina {r} vs 15): ESTÁVEL'); continue
                P(f'  {h["nome"]} tenta estancar {c["nome"]} (Medicina {r} vs 15): não')
        testes_morte(G,morreu)

def ataque(M,g,G,morreu,rnd,varre=False):
    J=jog(); ch=J['ch']; t=J['t']+M['at']+(2 if M.get('faro_ferida') and g['pv']<g['pvmax']*0.5 else 0); crit=J['crit']; g['golpes']=g.get('golpes',0)+1
    df=g['df']+(OFF if DOIS else 0)+(g.get('aura_def',[0,0])[0] if g.get('aura_def') else 0)-min(CERCO[1],CERCO[0]*max(0,g['golpes']-g['ac']))
    if J['fum'] or (t<df and not crit): P(f'    ataque em {g["nome"]}: {ch}+{M["at"]}={t} vs {df} erra'); return
    dd_=dados(M['dado'],crit=crit,plus=(J['extra'] if crit else 0)); br=int(sum(dd_)*M['mult'])+M.get('b',0)+M['nivel']//5; rd=g['rd']//2 if crit else g['rd']; rd+=sum(v for k,v in g.get('rd_ess',{}).items() if _sa(k)==_sa(M.get('essencia'))); liq=max(br-rd,0)
    if g.get('desfaz',0)>0 and liq>0 and (crit or liq>=g['pvmax']*0.2):   # 436 (G9): a peça que 'desfaz um golpe por dia' (o Gibão do rei) desfaz o golpe grande
        g['desfaz']-=1; P(f'    ataque em {g["nome"]}: {ch}+{M["at"]}={t} vs {df} ACERTA{" CRÍTICO" if crit else ""} {liq} → DESFEITO ({g.get("desfaz_nome","a peça")}, 1x por dia)'); return
    g['pv']-=liq; s=f'    ataque em {g["nome"]}: {ch}+{M["at"]}={t} vs {df} ACERTA{" CRÍTICO" if crit else ""} {dd_}×{M["mult"]}+{M.get("b",0)}+{M['nivel']//5}={br} − RD {rd} = {liq} ({g["pv"]})'
    if M.get('veneno') and g['pv']>0:
        vg=sum(ex())+g.get('vigor',10)
        if vg<M['veneno']['cd']+(OFF if DOIS else 0): g['veneno']=M['veneno']['rodadas']; s+=f' · VENENO (Vigor {vg})'
    if M.get('agarra') and g['pv']>0 and not g.get('agarrado'): g['agarrado']=True; g['df']-=2; s+=' · AGARRADO (−2 de Defesa)'
    P(s)
    if g['pv']<=0:
        cai(g,liq,morreu)
        if varre and g['nivel']*2<=M['nivel']:
            V=vivos(G,rnd)
            if V: P('    GOLPE QUE VARRE: segue no próximo'); ataque(M,V[d(len(V))-1],G,morreu,rnd,varre=False)
        return
    # contra-golpe de gente de nível alto
    if g.get('reac',0)>0 and (liq>=g['pvmax']*0.10 or crit) and M['pva']>0:
        g['reac']-=1; J2=jog(); c2=J2['ch']; t2=J2['t']+g['at']; cr2=J2['crit']
        if not J2['fum'] and (t2>=M['df']+(OFF if DOIS else 0) or cr2):
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
            if a<p['cd']+(OFF if DOIS else 0):
                q=d(6)+d(6); g['pv']-=q; g['fora']=1; P(f'    {g["nome"]}: Agilidade {a} vs {p["cd"]} → CAI (−{q}, {g["pv"]})')
                if g['pv']<=0: cai(g,q,morreu)
            else: P(f'    {g["nome"]}: segura ({a})')
        else:
            dm=sum(dados(p['dano'])); a=sum(ex())+g.get('agi',6); dm=dm//2 if a>=p['cd']+(OFF if DOIS else 0) else dm; g['pv']-=dm
            P(f'    {g["nome"]}: {dm} ({g["pv"]})')
            if p.get('rompe_servo') and g.get('servo') and g['pv']>0:   # MOTOR 9: o golpe que corta laços pode romper a palavra do servo
                rr=d(6)
                if rr<=2: g['vivo']=False; g['desfeito']=True; morreu.append(g['nome']); P(f'    A PALAVRA DE {g["nome"].upper()} SE ROMPE (d6 [{rr}]): desfeito'); continue
            if g['pv']<=0: cai(g,dm,morreu)

def confere_arquivo(F, nome):
    """MOTOR 6: arquivo de luta com campo faltando avisa QUAL campo, em vez de cair no meio da luta"""
    erros=[]
    if 'monstro' not in F or 'grupo' not in F: sys.exit(f'{nome}: o arquivo precisa de "monstro" e "grupo".')
    for k in ('nome','nivel','pv','df','at','dado','mult'):
        if k not in F['monstro']: erros.append(f'monstro: falta "{k}"')
    if not F['monstro'].get('gente') and F['monstro'].get('cat','Comum') not in RDCAT: erros.append(f'monstro: categoria desconhecida "{F["monstro"].get("cat")}" (use {", ".join(RDCAT)})')
    if not F['grupo']: erros.append('grupo vazio')
    for n,g in enumerate(F['grupo'],1):
        for k in ('nome','at','dado','mult','b','df','rd','pv'):
            if k not in g: erros.append(f'grupo #{n} ({g.get("nome","sem nome")}): falta "{k}"')
        for mg in (g.get('magias') or ([g['magia']] if g.get('magia') else [])):
            if not all(k in mg for k in ('dano','cd','rodada')): erros.append(f'grupo #{n} ({g.get("nome")}): a magia precisa de dano, cd e rodada')
    for dd_ in [F['monstro'].get('dado','1d6')]+[g.get('dado','1d6') for g in F['grupo']]:
        if not re.fullmatch(r'\d+d\d+', str(dd_)): erros.append(f'dado inválido: "{dd_}" (use NdL, por exemplo 3d10)')
    if erros: sys.exit(f'{nome}: arquivo de luta com problema. Nada foi rolado.\n  - '+'\n  - '.join(erros))

def pct(v,n): return f'{100*v/n:.0f}%' if (v==0 or 100*v/n>=1) else '<1%'
def quantil(xs,q):
    xs=sorted(xs); return xs[min(len(xs)-1,int(q*len(xs)))]

def simula(F, n, nome, grava_regua=False):
    """MOTOR 6: a régua com DISTRIBUIÇÃO (não só a média): quem morre, quem cai, quanto dura, quanto sobra do bicho"""
    global SIM
    SIM=True
    from collections import Counter
    c=Counter(); mortes=Counter(); cai_=Counter(); recua=Counter(); rs=[]; sobra=[]
    for _ in range(n):
        r=luta(F); c[r['res']]+=1; rs.append(r['rnd'])
        if r['res']!='morto': sobra.append(max(r['pv'],0)/r['pvm'])
        for m in set(r['mortos']): mortes[m]+=1
        for g in r['G']:
            if g.get('caido') or g['nome'] in r['mortos']: cai_[g['nome']]+=1
            elif g.get('recuou'): recua[g['nome']]+=1
    SIM=False
    M=F['monstro']; L=[]
    L.append(f"RÉGUA de {n} lutas simuladas (sem valor de jogo; margem de ±{196*(0.25/n)**0.5:.0f} pontos) · {M['nome']} ({M.get('cat','gente')} {M['nivel']}) contra {len(F['grupo'])}")
    ordem=[('morto',f"{M['nome']} MORRE"),('fugiu',f"{M['nome']} foge"),('grupo caiu','O GRUPO CAI'),('fase','a luta PARA na segunda fase (foge de sala ou propõe trato)'),('empate','sem desfecho no tempo')]
    L.append('  desfecho: '+' · '.join(f'{rot} {pct(c[k],n)}' for k,rot in ordem if c[k]))
    L.append(f'  duração: mediana {quantil(rs,0.5)} rodadas (de {quantil(rs,0.1)} a {quantil(rs,0.9)} em 8 de cada 10 lutas)')
    if sobra: L.append(f'  quando o bicho NÃO morre, sai com {100*quantil(sobra,0.5):.0f}% do PV (entre {100*quantil(sobra,0.1):.0f}% e {100*quantil(sobra,0.9):.0f}%)')
    nomes=[g['nome'] for g in F['grupo']]
    risco=sorted(nomes,key=lambda x:-mortes[x])
    L.append('  MORRE: '+(' · '.join(f'{x} {pct(mortes[x],n)}' for x in risco if mortes[x]) or 'ninguém, em nenhuma simulação'))
    L.append('  cai ou recua ferido: '+(' · '.join(f'{x} {pct(cai_[x]+recua[x],n)}' for x in sorted(nomes,key=lambda x:-(cai_[x]+recua[x])) if cai_[x]+recua[x]) or 'ninguém'))
    pior=max((mortes[x]/n for x in nomes),default=0)
    L.append(f"  LEI DAS CAÇADAS (339, limite de 2% de morte para qualquer um dos nossos): o pior risco é {100*pior:.1f}% → "+('DENTRO da lei' if pior<=0.02 else 'ACIMA: não vai sem o rei'))
    for l in L: print(l)
    if grava_regua:
        try:
            from nucleo import anota, dia_atual
            anota(f"- (OCULTO) RÉGUA [Dia {dia_atual()}] {os.path.basename(nome)}: "+' ‖ '.join(x.strip() for x in L[1:]))
            print('  (régua gravada no envelope como OCULTO; não mostrar ao jogador sem a Visão do Tempo)')
        except ImportError: print('  (sem nucleo.py: a régua não foi gravada no envelope)')

if __name__=='__main__':
    import re, os
    if len(sys.argv)<2: sys.exit(__doc__)
    try: F=json.load(open(sys.argv[1],encoding='utf-8'))
    except FileNotFoundError: sys.exit(f'não achei o arquivo de luta: {sys.argv[1]} (os arquivos ficam em sims/)')
    except json.JSONDecodeError as e: sys.exit(f'{sys.argv[1]}: o JSON está quebrado ({e}). Nada foi rolado.')
    confere_arquivo(F, sys.argv[1])
    n=next((int(x[4:]) for x in sys.argv[2:] if x.startswith('sim=')),0)
    regua=next((int(x[6:]) for x in sys.argv[2:] if x.startswith('regua=')),0)
    for x in sys.argv[2:]:
        if x=='um_dado': DOIS=False
        if x.startswith('off='): OFF=int(x[4:])
        if x.startswith('crit='): CRITMODO=x[5:]
        if x.startswith('fum='): FUMMODO=x[4:]
        if x.startswith('cerco='): a_,b_=x[6:].split(','); CERCO=(int(a_),int(b_))
        if x.startswith('seed='): random.seed(int(x[5:]))
        if x=='magia=velha': MAGIA='velha'
        if x in ('ini=nao','ini=não'): INICIATIVA=False   # MOTOR 6: a mesma semente repete a mesma régua (para comparar planos)
    if n or regua:
        simula(F, n or regua, sys.argv[1], grava_regua=bool(regua))
    else:
        r=luta(F)
        try:   # MOTOR 6.3: ferimento que dura, para quem caiu e viveu ou recuou ferido
            import feridos, nucleo
            if nucleo.camada('ferimentos'):
                med=any(g.get('medicina') for g in r['G'] if g['vivo'] or g.get('recuou'))
                for g in r['G']:
                    if g['nome'] in r['mortos'] or g['nome'].startswith('hoste'): continue
                    if g.get('caido') or g.get('recuou'): feridos.rola(g['nome'], caiu=bool(g.get('caido')), medicina=med, causa=F['monstro']['nome'])
        except ImportError: pass
        print('FIM:', r['res'], '· rodadas', r['rnd'], '· mortos', r['mortos'], '· PV', f"{r['pv']}/{r['pvm']}", '· grupo', {g['nome']:g['pv'] for g in r['G']})
        if 'sem_xp' not in sys.argv:   # 502 (G39, pedido do jogador): o XP da luta vai sozinho para quem lutou
            try:
                import encadeia; F['_arquivo']=sys.argv[1]; encadeia.xp_luta(F, r)
            except Exception as e: print('⚠ G39: o XP da luta NÃO foi lançado:', e)
        caidos=[g['nome'] for g in r['G'] if g['pv']<=0]
        if r['mortos'] or caidos:   # 426 (G9): a trava que faltou na forquilha
            print('⛔ G9: PARAR AQUI, DENTRO DA HORA. Mortos:', r['mortos'] or 'nenhum', '· caídos:', caidos or 'nenhum')
            print('   antes de o tempo andar, o jogador decide: ERGUER O CAÍDO (Luz 6º, o rei sabe: até 1 hora; 30 de Mana; 1 PV e −1 para sempre num atributo) · o SERVO ARMADO (a Receita Mestra do rei) · Medicina nos caídos · onde estão os corpos')
