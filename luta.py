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
ARQUIVO: {"monstro":{nome,cat,nivel,pv,pv_atual?,df,rd,at,dado,mult,b?,poder?,veneno?,fraqueza?,inteligente?,moral?,gente?,furia_bando?,folego_bando?,reflete? (425: magia volta no 18-20), covil? {nome,dano,cd,efeito}, grito? {cd} (437: o GRITO QUE DÁ MEDO, G16 AMEDRONTADO; no grupo: vontade_medo? N) e lendarias? N (G13, 433: o covil age no começo da rodada; Lendário 1, Mítico 2, Primordial 3 ações lendárias por padrão)},
          "grupo":[{nome,nivel,at,dado,mult,b,df,rd,pv,essencia?,chega?,grita?,magia?,so20?,heroi?,vigor?,agi?,medicina?,imune_empurrao?}]}
MOTOR 9.1 (Dia 438, pedido do jogador: "o luta.py rolar sozinho os traços novos, as fases, o olhar e os efeitos das Artes"):
  "tracos": [...] no monstro: o texto do gerador ou a chave curta (python3 luta.py tracos). O script roda sozinho:
     os 16 do Livro Nove 8.1 (pele que devolve · enxame · agarra e arrasta · teia · sangue que queima · casca que racha · duas vidas · sombra própria
     ("luz": "escuro"|"forte" no arquivo) · rouba o fôlego · cria no ventre · ouve o nome · come magia · faro de ferida · dono de território · velho demais ·
     carrega um tesouro) e, dos velhos, couraça · regenera · veneno · OLHAR PARALISANTE · muitas cabeças · grito · sentido sísmico · imune a armas ("arma_cat"
     em cada um) · invoca crias · reflete · devora metal · carrega doença. O que fica À MÃO (voa, camuflagem, escava, muda de forma, fala e mente) é avisado no topo.
  O OLHAR: 1 alvo por rodada (quem o feriu por último), sem gastar ação: Vontade (2d20 + nível ÷ 10 + "vontade") contra CD 10 + nível ÷ 10 (+14);
     falha: PARALISADO: perde a próxima vez e fica com −4 na Defesa até lá.
  A 2ª FASE (Livro Nove 8.3): chefe Único ou acima, aos 50%: d6 (troca de Essência · chama crias · o covil muda · foge para outra sala · troca de fraqueza ·
     FALA: a luta PARA e grava ARQ_continua.json). "fase": false desliga; "fase": {"rolado": N} usa o dado que já saiu do selo.
  RESISTÊNCIA LENDÁRIA (8.2): Lendário 1 · Mítico 2 · Primordial 3 por dia ("res_lendaria": N muda): vira em sucesso a falha contra queda, prisão, atordoamento.
  CRIAS (cria no ventre, invoca crias, a fase [2]): d6 crias, um degrau abaixo, UM QUARTO do nível do pai, 1 golpe cada ("cria": {nivel,pv,df,at,rd,dado,mult}
     muda os números). Quem tem "crias": 1 na ficha bate nelas primeiro; feitiço com "area": true pega todas. A última cria do ventre, sozinha e ferida,
     fica VIVA E RENDIDA ("captura": 0 desliga): o jogador decide depois se a leva (G25).
  AS ARTES DE ARMA (G30): "arte": "chave" no item de "magias" (python3 luta.py artes). O dano e o multiplicador continuam na ficha; o script põe o EFEITO
     quando a Arte pega em cheio: dois golpes · ignora RD · −2 de Defesa · CAÍDO · PRESO · ATORDOADO · SANGRANDO · dados dobrados (a Bigorna em quem está no chão
     ou preso) · crítico 17-20 · Reações (Ponta que Espera, Guarda de Dois, Muralha de Um Homem). ENCADEAR: "encadeia": {outra Arte} (o REMATE: uma lista de duas).
     "estamina" e "mana" na ficha e "custo" na técnica: sem recurso ela não sai (e o rouba o fôlego tira dali).
  OS DONS (G26, Livro Nove 4): "doms" na ficha (despertar.py põe sozinho): Segundo Coração (1x por dia fica com 1 PV ao cair) · Voz de Mando (+1 no
     ataque dos aliados) · Passo Certo (+2 na Iniciativa) · Pele do Mundo ("pele_essencia": RD +5 contra ela; +1 dado do golpe da oposta) · Fôlego Sem Fundo.
  Lei 7: o INIMIGO também: "magias": [...] no monstro (feitiço ou Arte na rodada marcada; "area": true pega todos; "efeito" e "cd" ou a "arte").
"""
import sys, json, secrets, random, re, os, unicodedata
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
def jog(crit17=False):
    A=ex1(); B=ex1() if DOIS else None
    t=sum(A)+(sum(B) if B else 0); n20=A.count(20)+(B.count(20) if B else 0)
    if not DOIS: return dict(t=t,ch=A,crit=A[0]==20 or (crit17 and A[0]>=17),fum=A[0]==1,extra=n20)
    nat=(A[0],B[0]); lim=17 if crit17 else 20   # MOTOR 9.1: a Flecha que Não Cai faz crítico com 17-20 (o outro dado 11+, como sempre)
    if CRITMODO=='um20': crit=max(nat)>=lim
    elif CRITMODO=='20e11': crit=(nat[0]>=lim and nat[1]>=11) or (nat[1]>=lim and nat[0]>=11)
    else: crit=nat==(20,20)
    fum=(nat[0]==1 and nat[1]<=10) or (nat[1]==1 and nat[0]<=10) if FUMMODO=='1e10' else nat==(1,1)
    return dict(t=t,ch=[A,B],crit=crit,fum=fum,extra=n20)
def dados(s,crit=False,plus=0,dobra=False):
    n,f=map(int,s.split('d')); n=n*(2 if crit else 1)*(2 if dobra else 1)+plus
    return [d(f) for _ in range(n)]
def P(*a):
    if not SIM: print(*a)
def fraco(g,M): return bool(g.get('essencia')) and g.get('essencia')==M.get('fraqueza')   # Dia 205: sem Essência não dobra (erro achado)
def acoes(nivel): return max(1,min(8,1+nivel//60))
def reac_gente(nivel): return 3 if nivel>=360 else 2 if nivel>=240 else 1 if nivel>=120 else 0
def liso(s): return ''.join(c for c in unicodedata.normalize('NFD',str(s)) if unicodedata.category(c)!='Mn').lower().strip()

LENDCAT={'Lendário':1,'Lendario':1,'Mítico':2,'Mitico':2,'Primordial':3}   # G13 (Dia 433, pedido do jogador)

# ---------- MOTOR 9.1 (Dia 438, pedido do jogador: "o luta.py rolar sozinho os traços novos, as fases, o olhar e os efeitos das Artes") ----------
DEGRAU={'Comum':0,'Incomum':1,'Raro':2,'Épico':3,'Único':4,'Lendário':5,'Mítico':6,'Primordial':7}
CATS=list(DEGRAU)
RESLEND={'Lendário':1,'Mítico':2,'Primordial':3}                      # Livro Nove 8.2: Resistência Lendária por dia
MAGCAT={'Comum':(0,'1d4'),'Incomum':(1,'1d4'),'Raro':(2,'1d6'),'Épico':(3,'2d6'),'Único':(5,'3d6'),'Lendário':(8,'5d6'),'Mítico':(12,'10d6'),'Primordial':(20,'20d6')}   # B e D do gerador
PVMULT_C={'Comum':5,'Incomum':6,'Raro':8,'Épico':15,'Único':20,'Lendário':25,'Mítico':100,'Primordial':300}
MULT_C={'Comum':1,'Incomum':1.5,'Raro':2.5,'Épico':5,'Único':10,'Lendário':25,'Mítico':100,'Primordial':500}
BONUS_C={'Comum':2,'Incomum':4,'Raro':6,'Épico':10,'Único':15,'Lendário':20,'Mítico':30,'Primordial':50}
RD_C={'Comum':0,'Incomum':1,'Raro':3,'Épico':6,'Único':12,'Lendário':25,'Mítico':50,'Primordial':100}
OPOSTA={'Fogo':'Gelo','Gelo':'Fogo','Vento':'Terra','Terra':'Vento','Água':'Raio','Raio':'Água','Vida':'Podridão','Podridão':'Vida','Sangue':'Luz',
        'Sombra':'Luz','Luz':'Sombra','Som':'Silêncio','Silêncio':'Som','Mente':'Fome','Tempo':'Sorte','Peso':'Vento','Sal':'Água','Força':'Fome',
        'Veneno':'Vida','Sorte':'Tempo','Elo':'Fome','Metal':'Podridão','Fome':'Vida','Espinho':'Fogo'}
# os traços do gerador (os 18 velhos e os 16 do Livro Nove 8.1): (chave curta, começo do texto do gerador)
TRACOS=[('couraca','couraca'),('regenera','regenera'),('voa','voa'),('veneno','veneno no golpe'),('olhar','olhar paralisante'),('cabecas','muitas cabecas'),
        ('camuflagem','camuflagem'),('grito','grito que causa medo'),('sopro','sopro em cone'),('escava','escava ou nada'),('sismico','sentido sismico'),
        ('imune_armas','imune a armas'),('doenca','carrega doenca'),('invoca_crias','invoca crias'),('reflete','reflete magia'),('devora_metal','devora metal'),
        ('muda_forma','muda de forma'),('fala_mente','fala e mente'),
        ('pele_devolve','pele que devolve'),('enxame','enxame'),('agarra','agarra e arrasta'),('teia','cospe teia'),('sangue_queima','sangue que queima'),
        ('casca_racha','casca que racha'),('duas_vidas','duas vidas'),('sombra_propria','sombra propria'),('rouba_folego','rouba o folego'),
        ('cria_ventre','cria no ventre'),('ouve_nome','ouve o nome'),('come_magia','come magia'),('faro_ferida','faro de ferida'),
        ('dono_territorio','dono de territorio'),('velho_demais','velho demais'),('carrega_tesouro','carrega um tesouro')]
A_MAO={'voa':'voa (só o alcança quem tem arma de longe, feitiço ou asa: o Mestre tira da linha quem não alcança)','camuflagem':'camuflagem (o teste de achar antes da luta)',
       'escava':'escava ou nada (a fuga dele pelo chão ou pela água: o Mestre declara)','muda_forma':'muda de forma (cena)','fala_mente':'fala e mente (cena)',
       'sopro':'sopro em cone (é o "poder" da ficha)'}
# as Artes de arma (Livro Nove 3.3): o que cada uma faz ALÉM do dano (o dano continua vindo de "dano" e "mult" da ficha)
ARTES={
 'fio_duplo':dict(circ=2,golpes=2), 'tiro_duplo':dict(circ=2,golpes=2,longe=True),
 'corte_corrido':dict(circ=4,varios=True), 'corte_do_horizonte':dict(circ=6,rd='metade',longe=True),
 'ponta_que_espera':dict(circ=2,reacao='ponta'), 'chuva_de_pontas':dict(circ=4,varios=True,max_alvos=3),
 'lanca_que_nao_dobra':dict(circ=6,rd='zero'), 'quebra_guarda':dict(circ=2,quebra=2),
 'tremor_de_ferro':dict(circ=4,varios=True,efeito=('derrubado',25)), 'bigorna':dict(circ=6,dobra_se=('derrubado','preso','agarrado','paralisado')),
 'rachar':dict(circ=2,rd=3,efeito=('sangrando',0)), 'roda_de_lamina':dict(circ=4,varios=True),
 'derrubar_o_tronco':dict(circ=6,tronco=True), 'flecha_que_prega':dict(circ=4,efeito=('preso',25),longe=True),
 'flecha_que_nao_cai':dict(circ=6,crit17=True,longe=True), 'empurrar_a_parede':dict(circ=2,efeito=('derrubado',20)),
 'guarda_de_dois':dict(circ=4,reacao='guarda'), 'muralha_de_um_homem':dict(circ=6,reacao='muralha'),
 'mao_aberta':dict(circ=2,efeito=('derrubado',20)), 'passo_que_some':dict(circ=4,at=2), 'golpe_no_sopro':dict(circ=6,efeito=('atordoado',35)),
}
COND_COVIL=['ENVENENADO','AGARRADO','CAÍDO','AMEDRONTADO','CEGO','ATORDOADO']

def chave_arte(x): return liso(x).replace('-',' ').replace(' ','_')
def le_tracos(M):
    T=set(); fora=[]
    for t in M.get('tracos') or []:
        n=liso(t); k=next((c for c,ini in TRACOS if n==c or n==c.replace('_',' ') or n.startswith(ini)),None)
        if k: T.add(k)
        else: fora.append(t)
    return T,fora
def magias_de(g): return g.get('magias') or ([g['magia']] if g.get('magia') else [])
def reacao_livre(m): return bool(m.get('arte')) and ARTES.get(chave_arte(m['arte']),{}).get('reacao') in ('ponta','guarda')
def na_rodada(m,rnd):
    r=m.get('rodada'); return rnd in (r if isinstance(r,list) else [r])
def mod_df(x,rnd,corpo=True):
    """o que as condições tiram da Defesa de quem é golpeado (gente ou bicho)"""
    m=0
    if x.get('quebra_ate',0)>=rnd: m-=2                                  # Quebra-Guarda: −2 por 1 rodada
    if corpo and (x.get('derrubado') or x.get('paralisado',0)>0 or x.get('atordoado')): m-=4   # G16 CAÍDO: −4 contra corpo a corpo (o paralisado e o atordoado não se guardam)
    if x.get('agarrado') or x.get('preso'): m-=2                         # G16 AGARRADO: −2 (o Preso não sai do lugar: o mesmo −2)
    return m
def teste(x,cd,attr=None):
    """resistência de gente na luta: 2d20 + nível ÷ 10 + o bônus declarado na ficha (forca, vontade...) contra a CD + 14"""
    sv=sum(ex())+x['nivel']//10+(x.get(attr,0) if attr else 0)
    return sv, cd+(OFF if DOIS else 0)
def resiste_M(M,cd,nome):
    """a resistência do bicho a um efeito de Arte (queda, prisão, atordoamento). A RESISTÊNCIA LENDÁRIA (Livro Nove 8.2) vira a falha em sucesso."""
    if nome=='o atordoamento' and M.get('cat') in RESLEND and not M.get('gente'): cd=cd//2   # Golpe no Sopro: Lendário ou acima resiste com metade da CD
    sv,alvo=teste(M,cd)
    if sv>=alvo: P(f'    {M["nome"]} resiste a {nome} ({sv} vs {alvo})'); return True
    if M.get('resl',0)>0:
        M['resl']-=1; P(f'    {M["nome"]} falha em {nome} ({sv} vs {alvo}) → RESISTÊNCIA LENDÁRIA: vira sucesso (restam {M["resl"]} hoje)'); return True
    P(f'    {M["nome"]} NÃO resiste a {nome} ({sv} vs {alvo})'); return False
def nova_cria(M,i):
    """a cria recém-solta (Livro Nove 8.1 e 8.5; a leitura do 438): um degrau abaixo, UM QUARTO do nível do pai (a adulta tem a metade), 1 ação"""
    c=M.get('cria') or {}; cc=CATS[max(DEGRAU.get(M.get('cat','Comum'),0)-1,0)]; nv=c.get('nivel',max(1,M['nivel']//4)); pv=c.get('pv',nv*PVMULT_C[cc])
    return dict(nome=f"cria {i} de {M['nome']}",cat=cc,nivel=nv,pva=pv,pvm=pv,df=c.get('df',10+nv//4+BONUS_C[cc]),rd=c.get('rd',RD_C[cc]),at=c.get('at',nv//4+BONUS_C[cc]),
                dado=c.get('dado','1d8'),mult=c.get('mult',MULT_C[cc]),b=0,golpes=0,bac=1,T=set(),cria=True,fraqueza=M.get('fraqueza'))
def solta_crias(M,motivo):
    n=d(6); ja=len(M['crias']); M['crias']+=[nova_cria(M,ja+i+1) for i in range(n)]; c=M['crias'][-1]; M['n_crias']=M.get('n_crias',0)+n
    P(f"  {motivo}: d6 [{n}] CRIAS ({c['cat']} {c['nivel']} · PV {c['pvm']} · Defesa {c['df']} · RD {c['rd']} · +{c['at']} · {c['dado']}×{c['mult']:g} · 1 golpe cada)")
def crias_vivas(M): return [c for c in M.get('crias',[]) if c['pva']>0 and not c.get('rendida')]
def rende_ultima(M):
    """Livro Nove 8.1 (cria no ventre): uma cria pode ser levada VIVA: a última, sozinha e abaixo da metade, se rende (salvo "captura": 0 no arquivo)"""
    cv=crias_vivas(M)
    if M.get('_morto') and M.get('_captura') and 'cria_ventre' in M.get('T',()) and len(cv)==1 and cv[0]['pva']<cv[0]['pvm']*0.5:
        cv[0]['rendida']=True; P(f"    a última cria ({cv[0]['nome']}) está sozinha e ferida: RENDIDA E VIVA ({cv[0]['pva']}/{cv[0]['pvm']})")
def troca_essencia(M,motivo):
    velha=M.get('essencia'); pool=[e for e in OPOSTA if e!=velha]; nova=pool[d(len(pool))-1]; M['essencia']=nova; M['fraqueza']=OPOSTA[nova]
    P(f"  {motivo}: a Essência dele vira {nova.upper()} (d{len(pool)}); a fraqueza passa a ser {OPOSTA[nova].upper()}")
def aplica_cond(x,cond,cd,quem,G=None,morreu=None,attr='forca'):
    """um efeito de Arte ou de feitiço em GENTE do grupo (vindo de inimigo com Artes, Lei 7)"""
    if cond=='sangrando': x['sangrando']=True; P(f'    {x["nome"]} fica SANGRANDO (2% do PV por rodada)'); return
    sv,alvo=teste(x,cd,'vigor_b' if cond=='atordoado' else attr)
    if sv>=alvo: P(f'    {x["nome"]} resiste ({sv} vs {alvo})'); return
    if cond=='atordoado': x['paralisado']=1
    else: x[cond]=True
    P(f'    {x["nome"]} ({sv} vs {alvo}) → {cond.upper()}')

def luta(F):
    M=dict(F['monstro']); G=[dict(g) for g in F['grupo']]
    for g in G:
        g.setdefault('vivo',True); g.setdefault('fora',0); g['pvmax']=g.get('pvmax_real',g['pv']); g.setdefault('nivel',20)   # Dia 205: o máximo VERDADEIRO (luta retomada no meio)
        g['ac']=g.get('acoes',acoes(g['nivel']))
    nini=len(G); gente=M.get('gente',False); cat=M.get('cat','Comum'); deg=DEGRAU.get(cat,0)
    doms(G,M)   # MOTOR 9.1 (438, G26): os Dons do Despertar que mudam a luta
    T,_=le_tracos(M); M['T']=T; M['crias']=[]; M['_captura']=F.get('captura',1)
    mult=min(1.5,1+0.10*(nini-1)) if M.get('folego_bando') else 1.0
    pvmax=int(M['pv']*mult); frac=M.get('pv_atual',M['pv'])/M['pv']; M['pvm']=pvmax; M['pva']=int(pvmax*frac)
    if not gente: M['rd']=max(M.get('rd',0),RDCAT.get(cat,0))
    # MOTOR 9.1: o que os traços do gerador põem na ficha sozinhos (só quando o arquivo traz "tracos"; chave escrita à mão no arquivo ganha do traço)
    if 'couraca' in T: M['rd']+=max(deg-1,0)*3                                   # couraça: RD +3 por degrau acima de Incomum (o precedente da Eloune, EL23b: Épico +6)
    if 'grito' in T and not M.get('grito'): M['grito']={'cd':15}                    # G16: Vontade CD 15
    if 'olhar' in T and not M.get('olhar'): M['olhar']={'cd':10+M['nivel']//10}     # o gerador: Vontade contra CD 10 + nível ÷ 10
    if 'veneno' in T and not M.get('veneno'): M['veneno']={'dado':MAGCAT[cat][1],'cd':10+2*MAGCAT[cat][0],'rodadas':3}   # o precedente da Zatha: D e 10 + 2B da categoria, 3 rodadas
    if 'reflete' in T: M['reflete']=True
    luz=liso(F.get('luz','')); sem_surpresa=bool({'sismico','velho_demais'}&T)
    surpresa=bool(F.get('surpresa')) and not sem_surpresa
    M['bac']=M.get('acoes',acoes(M['nivel'])+(0 if gente else ACAT.get(cat,0))+(1 if 'cabecas' in T else 0))+(min(2,(nini-1)//3) if M.get('furia_bando') else 0)
    if 'sombra_propria' in T:
        if luz=='escuro': M['bac']*=2
        elif luz=='forte': M['bac']=max(1,M['bac']-1)
    M['resl']=M.get('res_lendaria',0 if gente else RESLEND.get(cat,0))
    reac_max=reac_gente(M['nivel']) if gente else REACAT.get(cat,0)
    tem_fase=M.get('fase',(not gente) and deg>=4)   # Livro Nove 8.3: todo chefe Único ou acima; "fase": false desliga; "fase": {"rolado": N} usa o d6 que já saiu do selo
    P(f"LEI DAS AÇÕES: {M['nome']} (nível {M['nivel']}) contra {nini} · PV {M['pva']}/{pvmax} · RD {M['rd']} · {M['bac']} ações · reação {reac_max} · grupo: "+', '.join(f"{g['nome']} {g['ac']}" for g in G))
    if T or M['resl'] or tem_fase:
        roda=[c for c,_ in TRACOS if c in T and c not in A_MAO]
        P('TRAÇOS QUE O SCRIPT RODA: '+(', '.join(x.replace('_',' ') for x in roda) or 'nenhum')+(f' · Resistência Lendária {M["resl"]}' if M['resl'] else '')+(' · 2ª FASE aos 50%' if tem_fase else ''))
        for k in sorted(T&set(A_MAO)): P('  À MÃO (declarar no envelope antes, G33): '+A_MAO[k])
        if 'imune_armas' in T and not all(g.get('arma_cat') for g in G): P('  ⚠ imune a armas duas categorias abaixo: ponha "arma_cat" em cada um do grupo (sem ela o golpe passa)')
        if surpresa is False and F.get('surpresa'): P('  nunca é surpreendido (sentido sísmico ou velho demais): a SURPRESA não vale')
    furia=False; recarga=False; rnd=F.get('rodada0',0); ultimo=None; moral_feito=bool(F.get('moral_feito')); morreu=[]; fase_feita=bool(F.get('fase_feita')); trato=False
    if F.get('furia_feita'): furia=True
    primeiro_m=False
    def inicia():
        bm=M.get('ini',M['nivel']//10); bg=int(sum(g.get('ini',g['nivel']//10) for g in G)/len(G))
        while True:
            im=sum(ex())+bm; ig=sum(ex())+bg
            if im!=ig: break
        P(f"INICIATIVA: {M['nome']} 2d20+{bm} = {im} × o grupo 2d20+{bg} (média) = {ig} → "+(f"{M['nome']} AGE PRIMEIRO" if im>ig else 'o grupo age primeiro'))
        return im>ig
    if INICIATIVA and F.get('iniciativa',True) and not surpresa and G and not F.get('rodada0'):   # INICIATIVA (Dia 379): antes o grupo agia sempre primeiro
        primeiro_m=inicia()
    rnd_ini=rnd+1; rnd1=rnd+1; pula_m=0
    def queda():
        """o chefe chegou a 0 (na vez do grupo, por contra-golpe ou sangrando): DUAS VIDAS, CRIA NO VENTRE ou o fim. Devolve True se a luta acabou."""
        if M['pva']>0 or M.get('_morto'): return bool(M.get('_morto')) and not crias_vivas(M)
        if 'duas_vidas' in T and not M.get('_segunda'):   # Livro Nove 8.1: levanta 1x com um quarto do PV e outra Essência
            M['_segunda']=True; M['pva']=pvmax//4
            for k_ in ('derrubado','preso','atordoado','sangrando'): M.pop(k_,None)
            P(f'  {M["nome"]} CAI… e LEVANTA (DUAS VIDAS): {M["pva"]}/{pvmax}'); troca_essencia(M,'  a segunda vida'); return False
        M['_morto']=True; P(f'  {M["nome"]} CAI')
        for g in G: g.pop('medo',None); g.pop('agarrado',None)
        if 'cria_ventre' in T: solta_crias(M,'CRIA NO VENTRE (ao morrer)')
        return not crias_vivas(M)
    while rnd<F.get('ate',40)+F.get('rodada0',0):
        if queda(): break
        rnd+=1; P(f'--- RODADA {rnd} · {M["nome"]} {max(M["pva"],0)}/{pvmax}'+(f' · {len(crias_vivas(M))} cria(s)' if crias_vivas(M) else ''))
        reac=reac_max; M['golpes']=0; M.pop('alvo_fixo',None); M['_comeu']=False
        for c in M['crias']: c['golpes']=0
        for g in G: g['reac']=reac_gente(g['nivel']); g['golpes']=0
        for g in G:
            if g['vivo'] and g.get('veneno',0)>0:
                x=sum(dados(M['veneno']['dado'])); g['pv']-=x; g['veneno']-=1; P(f'  veneno em {g["nome"]}: −{x} ({g["pv"]})')
                if g['pv']<=0: cai(g,0,morreu)
            if g['vivo'] and g.get('sangrando'):
                x=max(2,g['pvmax']*2//100); g['pv']-=x; P(f'  {g["nome"]} sangra: −{x} ({g["pv"]})')
                if g['pv']<=0: cai(g,0,morreu)
        if M['pva']>0:
            if M.get('sangrando'):
                x=max(2,pvmax*2//100); M['pva']-=x; P(f'  {M["nome"]} sangra: −{x} ({M["pva"]})')
            if 'regenera' in T and M['pva']>0 and M['pva']<pvmax:
                if M.pop('_ferido_fraqueza',False): P(f'  {M["nome"]} não regenera (ferido pela fraqueza)')
                else: x=min(M['nivel']//2,pvmax-M['pva']); M['pva']+=x; P(f'  {M["nome"]} REGENERA +{x} ({M["pva"]})')
        gr=M.get('grito')   # 437: o GRITO QUE DÁ MEDO (traço do gerador; G16 AMEDRONTADO: não avança contra o que teme, −2 no ataque; Vontade a cada rodada para sair)
        if gr and M['pva']>0:
            cdg=gr.get('cd',15)+(OFF if DOIS else 0)
            for g in vivos(G,rnd):
                if g.get('medo'):
                    sv=sum(ex())+g['nivel']//10+g.get('vontade_medo',0)
                    if sv>=cdg: g['medo']=False; P(f"  {g['nome']} sacode o medo (Vontade {sv} vs {cdg})")
            if not M.get('_gritou') and not (surpresa and rnd==rnd1):
                M['_gritou']=True; P(f"  GRITO de {M['nome']}: Vontade contra {cdg}")
                for g in vivos(G,rnd):
                    sv=sum(ex())+g['nivel']//10+g.get('vontade_medo',0)
                    if sv<cdg: g['medo']=True
                    P(f"    {g['nome']}: {sv} → "+('AMEDRONTADO (só feitiço de longe; −2 no ataque)' if g.get('medo') else 'firme'))
        cv=M.get('covil')   # G13 (Dia 433): o COVIL age no começo da rodada (d6: 1-2 respira · 3-5 um alvo · 6 todos, metade)
        for _vez in range((2 if 'dono_territorio' in T else 1) if cv and M['pva']>0 else 0):   # Livro Nove 8.1: dono de território: o covil age duas vezes
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
        # ---------- a vez do grupo ----------
        for g in G:
            if not g['vivo'] or g.get('chega',1)>rnd or not (M['pva']>0 or crias_vivas(M)) or (rnd==rnd_ini and primeiro_m): continue
            if g['fora']>0: g['fora']-=1; P(f'  {g["nome"]} volta'); continue
            if g.get('paralisado',0)>0: g['paralisado']-=1; P(f'  {g["nome"]} PARALISADO: perde a vez'); continue
            for _m in magias_de(g):   # as Artes que são REAÇÃO (Ponta que Espera, Guarda de Dois) se armam sem gastar a ação
                if reacao_livre(_m) and na_rodada(_m,rnd) and pode_pagar(g,_m) and M['pva']>0: paga(g,_m); arte(g,_m,M,G,morreu,rnd)
            for k in range(g['ac']):
                if not g['vivo'] or not (M['pva']>0 or crias_vivas(M)): break
                if k==0 and g.get('grita') and M['pva']>0:
                    if 'ouve_nome' in T:   # Livro Nove 8.1: quem diz o nome vira o alvo; só o nome VERDADEIRO o cala
                        M['alvo_fixo']=g; P(f'  {g["nome"]} GRITA O NOME: "{M["nome"].upper()}!" → ele OUVE: {g["nome"]} vira o alvo'+(' · é o nome VERDADEIRO: ele se cala' if g.get('grita')=='verdadeiro' else ''))
                        if g.get('grita')=='verdadeiro': M['calado']=True
                    else: M['calado']=True; P(f'  {g["nome"]} GRITA O NOME: "{M["nome"].upper()}!"')
                    continue
                mg=None   # 426 (G9): a ficha pode ter VÁRIOS feitiços ('magias'); vale o primeiro que tem esta rodada
                for _m in magias_de(g):
                    if na_rodada(_m,rnd) and pode_pagar(g,_m) and not reacao_livre(_m): mg=_m; break
                if g.get('derrubado') and not (k==0 and mg): g['derrubado']=False; P(f'  {g["nome"]} se levanta (1 ação)'); continue
                if (g.get('agarrado') or g.get('preso')) and not (k==0 and mg):   # G16 AGARRADO e o Preso da teia: a ação vai no teste para sair
                    oq='agarrado' if g.get('agarrado') else 'preso'; sv,alvo=teste(g,10+M['nivel']//10,'forca')
                    if sv>=alvo: g[oq]=False; P(f'  {g["nome"]} se solta ({oq}; Força ou Agilidade {sv} vs {alvo})')
                    else: P(f'  {g["nome"]} não se solta ({oq}; {sv} vs {alvo})')
                    continue
                if g.get('medo') and not (k==0 and mg): continue   # 437: AMEDRONTADO não avança contra o que teme (o feitiço de longe vale)
                if k==0 and mg:   # Dia 299: 'rodada' pode ser lista (a Maça lança 2x por cena; antes contava 1: erro achado)
                    paga(g,mg)
                    if mg.get('arte'):
                        if arte(g,mg,M,G,morreu,rnd): ultimo=g
                        continue
                    if M['pva']<=0:   # o chefe caiu e sobram crias: o feitiço vai nelas
                        feitico_nas_crias(g,mg,M,None,None,so_crias=True); continue
                    if MAGIA=='velha':
                        dm=int(sum(dados(mg['dano']))*mg.get('mult',1)); sv=sum(ex())+M['at']; dd=max((dm//2 if sv>=mg['cd']+(OFF if DOIS else 0) else dm)-M['rd'],0); txt_m=f'resiste {sv} vs {mg["cd"]}'; Jm=None; tm=None
                    else:   # MAGIA DISPUTADA (Dia 379): o lançador joga 2d20 + ataque contra a Defesa + 14 do alvo, como um golpe
                        Jm=jog(); tm=Jm['t']+mg.get('at',g['at'])-(2 if g.get('medo') else 0); dfm=M['df']+(OFF if DOIS else 0)+mod_df(M,rnd,corpo=False)
                        if Jm['fum']: dm=0; txt_m=f'{Jm["ch"]} DOIS 1: o feitiço se desfaz'
                        elif Jm['crit']: dm=int(sum(dados(mg['dano'],crit=True))*mg.get('mult',1)); txt_m=f'{Jm["ch"]}+{mg.get("at",g["at"])}={tm} CRÍTICO (dados dobrados)'
                        elif tm>=dfm: dm=int(sum(dados(mg['dano']))*mg.get('mult',1)); txt_m=f'{Jm["ch"]}+{mg.get("at",g["at"])}={tm} vs {dfm} pega em cheio'
                        else: dm=int(sum(dados(mg['dano']))*mg.get('mult',1))//2; txt_m=f'{Jm["ch"]}+{mg.get("at",g["at"])}={tm} vs {dfm} o alvo resiste: metade'
                        dd=max(dm-M['rd'],0)
                    essm=mg.get('essencia', g.get('essencia')); fr=fraco({'essencia': essm},M)
                    if fr: dd*=2   # 407: a magia pode declarar a Essência dela ("" = nenhuma); sem declarar, vale a do lançador, como antes
                    if 'enxame' in T: dd=dd*2 if mg.get('area') else dd//2; txt_m+=' · ENXAME: '+('área, o dobro' if mg.get('area') else 'um alvo só, metade')
                    if mg.get('area') and crias_vivas(M): feitico_nas_crias(g,mg,M,Jm,tm)
                    if M.get('reflete') and dd>0:   # 425: o traço "reflete magia com 18 a 20" existia nas fichas e não rodava (achado ao montar o Morek)
                        rf=d(20)
                        if rf>=18:
                            g['pv']-=dd; P(f'  {g["nome"]} lança: {dm}; {txt_m} → REFLETIDA (d20 [{rf}]): {dd} voltam em {g["nome"]} ({g["pv"]})')
                            if g['pv']<=0: cai(g,dd,morreu)
                            continue
                    if 'come_magia' in T and dd>0 and not M['_comeu'] and not fr:   # Livro Nove 8.1: o 1º feitiço de cada rodada o cura (salvo o da fraqueza)
                        M['_comeu']=True; cura=min(dd,pvmax-M['pva']); M['pva']+=cura
                        P(f'  {g["nome"]} lança{(" " + mg["nome"]) if mg.get("nome") else ""}: {dm}; {txt_m} → ELE COME A MAGIA: +{cura} ({M["pva"]})'); continue
                    if fr and dd>0: M['_ferido_fraqueza']=True
                    M['pva']-=dd; ultimo=g; P(f'  {g["nome"]} lança{(" " + mg["nome"]) if mg.get("nome") else ""}: {dm}; {txt_m} → {dd} ({M["pva"]})'); continue
                # ---------- o golpe de arma ----------
                cv_=crias_vivas(M)
                if cv_ and (M['pva']<=0 or g.get('crias')):   # quem a ficha manda limpar as crias ("crias": 1), ou todos depois que o chefe cai
                    golpe_cria(g,cv_[0],M,G,morreu,rnd); continue
                if M['pva']<=0: break
                J=jog(); ch=J['ch']; t=J['t']+g['at']-(2 if g.get('agarrado') else 0); crit=J['crit']
                M['golpes']+=1; brecha=min(CERCO[1],CERCO[0]*max(0,M['golpes']-M['bac'])); dfM=M['df']+(OFF if DOIS else 0)-brecha+mod_df(M,rnd,corpo=not g.get('longe'))
                if J['fum'] and 'devora_metal' in T: M.setdefault('_roidas',[]).append(g['nome']); P(f'  ⚠ DEVORA METAL: dois 1 de {g["nome"]}: a arma dele PERDE 1 CATEGORIA (acertar a ficha depois da luta)')
                if J['fum'] or (t<dfM and not crit) or (g.get('so20') and not crit): P(f'  {g["nome"]}: {ch}+{g["at"]}={t} vs {dfM} erra'); continue
                dd_=dados(g['dado'],crit=crit,plus=(J['extra'] if crit else 0)); br=int(sum(dd_)*g['mult'])+g['b']+g['nivel']//5
                rd=M['rd']//2 if crit else M['rd']; liq=max(br-rd,0); nota=''
                if fraco(g,M): liq*=2
                if 'imune_armas' in T and g.get('arma_cat') and DEGRAU.get(g['arma_cat'],9)<=deg-2: liq=0; nota+=f' · IMUNE (arma {g["arma_cat"]}, duas categorias abaixo)'
                if 'enxame' in T: liq//=2; nota+=' · ENXAME: metade'
                if fraco(g,M) and liq>0: M['_ferido_fraqueza']=True
                M['pva']-=liq; ultimo=g
                P(f'  {g["nome"]}: {ch}+{g["at"]}={t} ACERTA{" CRÍTICO" if crit else ""} {dd_}×{g["mult"]}+{g["b"]}+{g["nivel"]//5}={br} − RD {rd}{" ×2" if fraco(g,M) else ""} = {liq} ({M["pva"]}){nota}')
                devolve(M,g,liq,morreu)
                if M['pva']>0 and reac>0 and (liq>=pvmax*0.10 or crit) and g['vivo']:
                    reac-=1; P('  REAÇÃO:'); ataque(M,g,G,morreu,rnd)
        # ---------- o chefe cai? ----------
        if queda(): break
        if M['pva']>0:
            nl=0 if M.get('atordoado') else M.get('lendarias', 0 if gente else LENDCAT.get(cat,0))   # G13: AÇÕES LENDÁRIAS: golpes fora da vez, em quem o feriu por último
            for _ in range(nl):
                V=vivos(G,rnd)
                if not V: break
                P('  AÇÃO LENDÁRIA:'); ataque(M,ultimo if ultimo in V else V[d(len(V))-1],G,morreu,rnd)
            if 'casca_racha' in T and not M.get('_rachou') and M['pva']<pvmax*0.5:   # Livro Nove 8.1: perde a couraça (RD à metade) e ganha +1 ação
                M['_rachou']=True; M['rd']//=2; M['bac']+=1; P(f'  A CASCA RACHA: RD {M["rd"]} e +1 ação')
            if not gente and not furia and M['pva']<pvmax*0.5: furia=True; recarga=True; P('  FÚRIA: +1 ação, o poder recarrega')
            if tem_fase and not fase_feita and M['pva']<pvmax*0.5:   # Livro Nove 8.3: a SEGUNDA FASE dos chefes Únicos ou acima
                fase_feita=True; rf=tem_fase.get('rolado') if isinstance(tem_fase,dict) else None; pre=bool(rf); rf=rf or d(6)
                P(f'  2ª FASE (Livro Nove 8.3) d6 [{rf}]'+(' (já rolado no selo)' if pre else '')+': '+['troca de Essência','chama crias','o covil muda','foge para outra sala do covil','perde a fraqueza conhecida e ganha outra','FALA: oferece um trato (Lei 15)'][rf-1])
                if gente and not furia: furia=True; recarga=True; P('  FÚRIA: +1 ação, o poder recarrega')
                if rf==1: troca_essencia(M,'  a fase')
                elif rf==2: solta_crias(M,'  ele CHAMA AS CRIAS')
                elif rf==3:
                    if cv: novo=[c for c in COND_COVIL if c not in str(cv.get('efeito',''))]; cv=dict(cv); cv['efeito']=novo[d(len(novo))-1]+' (G16)'; M['covil']=cv; P(f"    o covil agora dá {cv['efeito']}")
                    else: P('    ele não luta no covil: nada muda')
                elif rf==4:
                    if M.get('preso') or M.get('derrubado'): P('    preso ou no chão: não consegue sair; fica só a Fúria')
                    else:
                        for k_ in ('sangrando','quebra_ate'): M.pop(k_,None)
                        for g in G:
                            for k_ in ('agarrado',): g.pop(k_,None)
                        P('    ele some para OUTRA SALA do covil: a luta recomeça lá (quem está caído fica; nova iniciativa)')
                        primeiro_m=inicia(); rnd_ini=rnd+1; pula_m=1
                elif rf==5:
                    pool=[e for e in OPOSTA if e not in (M.get('fraqueza'),M.get('essencia'))]; M['fraqueza']=pool[d(len(pool))-1]
                    P(f"    a fraqueza conhecida não vale mais; a nova (a descobrir) é {M['fraqueza'].upper()} (d{len(pool)})")
                elif rf==6:
                    trato=True
                    if not SIM:
                        P('  ⏸ LEI 15: ELE FALA E OFERECE UM TRATO. A luta PARA aqui; a oferta vai à mesa (declarar no selo o que ele quer e o que dá).')
                        fim_caidos(G,morreu); return dict(res='trato',rnd=rnd,mortos=morreu,pv=M['pva'],pvm=pvmax,G=G,M=M,trato=True,furia=furia)
            if M.get('moral',True) and not moral_feito and M['pva']<pvmax*0.25:
                moral_feito=True; m=d(6); P(f'  MORAL d6 [{m}] → '+('FOGE' if m<=3 else 'luta até cair'))
                if m<=3 and M.get('preso'): P('  PRESO: não consegue fugir; luta até cair'); m=6
                if m<=3:
                    gu=[g for g in G if g['vivo'] and g.get('guarda_fuga')]
                    if gu and M.get('fuga'):
                        a=sum(ex())+M['fuga']; b=sum(ex())+gu[0]['guarda_fuga']; P(f'  FUGA: {M["nome"]} {a} × {gu[0]["nome"]} na saída {b}')
                        if b>=a: P('  FUGA BARRADA: luta até cair'); m=6
                    if m<=3: fim_caidos(G,morreu); return dict(res='fugiu',rnd=rnd,mortos=morreu,pv=M['pva'],pvm=pvmax,G=G,M=M,trato=trato)
        if surpresa and rnd==rnd1: P('  SURPRESA: ele não age nesta rodada'); continue   # Dia 208: a casa pegou de surpresa (teste aberto antes)
        if pula_m: pula_m=0; continue
        # ---------- a vez do bicho ----------
        if M['pva']>0:
            ac=M['bac']+(1 if furia else 0)
            calado=M.pop('calado',False)
            if calado: ac-=1
            if M.get('atordoado'): M['atordoado']=False; ac=0; P(f'  {M["nome"]} ATORDOADO: perde a rodada')
            else:
                if M.get('derrubado'): M['derrubado']=False; ac-=1; P(f'  {M["nome"]} se levanta (1 ação)')
                if M.get('preso'):
                    ac-=1
                    if resiste_M(M,25,'a prisão'): M['preso']=False
                if 'invoca_crias' in T and not M.get('_invocou'): M['_invocou']=True; solta_crias(M,'INVOCA CRIAS')
                ol=M.get('olhar')   # MOTOR 9.1: o OLHAR PARALISANTE: 1 alvo por rodada, sem gastar ação; falha: perde a próxima vez e fica sem guarda (−4)
                if ol and not calado:
                    V=[g for g in vivos(G,rnd) if not g.get('paralisado') and not g.get('cego') and g.get('_olhado',0)<rnd]   # quem acabou de perder a vez pelo olhar não é preso de novo na rodada seguinte
                    if V:
                        g=ultimo if ultimo in V else V[d(len(V))-1]; sv,alvo=teste(g,ol.get('cd',10+M['nivel']//10),'vontade' if 'vontade' in g else 'vontade_medo')
                        if sv<alvo: g['paralisado']=1; g['_olhado']=rnd+1
                        P(f'  OLHAR de {M["nome"]} em {g["nome"]}: Vontade {sv} vs {alvo} → '+('PARALISADO (perde a próxima vez; −4 na Defesa)' if sv<alvo else 'desvia os olhos'))
                if 'teia' in T:   # Livro Nove 8.1: 1x por rodada prende um alvo a 18 m (Força CD 10 + nível ÷ 10)
                    V=[g for g in vivos(G,rnd) if not g.get('preso')]
                    if V:
                        g=V[d(len(V))-1]; sv,alvo=teste(g,10+M['nivel']//10,'forca')
                        if sv<alvo: g['preso']=True
                        P(f'  TEIA de {M["nome"]} em {g["nome"]}: Força {sv} vs {alvo} → '+('PRESO (a ação vai em se soltar; −2 na Defesa)' if sv<alvo else 'rasga a teia'))
                poder=M.get('poder'); per=1 if REACAT.get(cat,0)>=2 else 2
                if poder and not calado and ac>0 and (per==1 or rnd%2==1 or recarga):
                    recarga=False; ac-=1; area(M,G,rnd,morreu)
                for mm in M.get('magias') or []:   # Lei 7: o inimigo com feitiço ou Arte de arma lança na rodada marcada (1 ação)
                    if ac>0 and na_rodada(mm,rnd) and vivos(G,rnd): ac-=1; magia_M(M,mm,G,morreu,rnd,ultimo); break
                for _ in range(max(ac,0)):
                    V=vivos(G,rnd)
                    if not V: break
                    ataque(M,escolhe(M,V,ultimo,rnd),G,morreu,rnd,varre=True)
        for c in crias_vivas(M):   # cada cria viva dá 1 golpe
            V=vivos(G,rnd)
            if not V: break
            ataque(c,V[d(len(V))-1],G,morreu,rnd)
        testes_morte(G,morreu)
        if not [g for g in G if g['vivo']]: P('  O GRUPO CAI'); fim_caidos(G,morreu); return dict(res='grupo caiu',rnd=rnd,mortos=morreu,pv=M['pva'],pvm=pvmax,G=G,M=M,trato=trato)
        rende_ultima(M)
    venceu=M['pva']<=0 and not crias_vivas(M)
    if venceu or not F.get('ate'): fim_caidos(G,morreu)   # Dia 205: rodada a rodada ('ate') não estanca de graça no fim
    return dict(res='morto' if venceu else 'empate',rnd=rnd,mortos=morreu,pv=M['pva'],pvm=pvmax,G=G,M=M,trato=trato)

def doms(G,M):
    """G26 (Livro Nove 4): o que os Dons fazem na luta. "doms": [...] e "doms_grau2": [...] na ficha; "pele_essencia" para a Pele do Mundo"""
    for g in G:
        D=g.get('doms') or []; g2=g.get('doms_grau2') or []; x=lambda d: 2 if d in g2 else 1
        if 'Passo Certo' in D: g['ini']=g.get('ini',g['nivel']//10)+2*x('Passo Certo')
        if 'Fôlego Sem Fundo' in D:
            for r in ('estamina','mana'):
                if r in g: g[r]=int(g[r]*(1+0.25*x('Fôlego Sem Fundo')))
        pe=g.get('pele_essencia')
        if 'Pele do Mundo' in D and pe and M.get('essencia')==pe: g['rd']+=5*x('Pele do Mundo'); P(f"DOM: a PELE DO MUNDO de {g['nome']} contra {pe}: RD +{5*x('Pele do Mundo')}")
        if 'Pele do Mundo' in D and pe and M.get('essencia')==OPOSTA.get(pe): g['_pele_oposta']=True; P(f"DOM: a PELE DO MUNDO de {g['nome']} (contra {pe}) paga o preço: o golpe de {OPOSTA[pe]} soma +1 dado nele")
        if 'Voz de Mando' in D:
            for h in G:
                if h is not g: h['at']+=x('Voz de Mando')
            P(f"DOM: a VOZ DE MANDO de {g['nome']}: os aliados com +{x('Voz de Mando')} no ataque")
def vivos(G,rnd): return [g for g in G if g['vivo'] and g.get('chega',1)<=rnd and g['fora']==0]
def alvo_de(M,V,ultimo):
    r=d(6)
    if M.get('inteligente') or 'faro_ferida' in M.get('T',()): return min(V,key=lambda g:g['pv'])   # Livro Nove 8.1: faro de ferida: escolhe sempre quem tem menos PV
    if r<=3 and ultimo in V: return ultimo
    if r==6: return min(V,key=lambda g:g['pvmax'])
    return V[d(len(V))-1]
def escolhe(M,V,ultimo,rnd):
    if M.get('alvo_fixo') in V: return M['alvo_fixo']                                  # ouve o nome: quem disse o nome vira o alvo
    mu=[g for g in V if g.get('muralha_ate',0)>=rnd]
    if mu: return mu[0]                                                                # Muralha de Um Homem: ninguém golpeia quem está atrás dele
    ag=[g for g in V if g.get('agarrado')]
    if ag and d(6)<=3: return ag[0]                                                    # quem ele segura está à mão
    return alvo_de(M,V,ultimo)

def pode_pagar(g,mg):
    """MOTOR 9.1: com "estamina" ou "mana" na ficha, a técnica e o feitiço com "custo" só saem se houver (o rouba o fôlego tira daí)"""
    c=mg.get('custo'); rec=mg.get('recurso','estamina' if mg.get('arte') else 'mana')
    return not c or rec not in g or g[rec]>=c
def paga(g,mg):
    c=mg.get('custo'); rec=mg.get('recurso','estamina' if mg.get('arte') else 'mana')
    if c and rec in g: g[rec]-=c

def devolve(M,g,liq,morreu,corpo=True):
    """o que o corpo do bicho devolve a quem o fere de perto (Livro Nove 8.1)"""
    T=M.get('T',())
    if liq<=0 or not g['vivo'] or g.get('longe') or not corpo: return
    if 'pele_devolve' in T:
        x=liq//4; g['pv']-=x; P(f'    PELE QUE DEVOLVE: {g["nome"]} leva {x} ({g["pv"]})')
        if g['pv']<=0: cai(g,x,morreu); return
    if 'sangue_queima' in T and g.get('corte',True):
        x=d(6)*max(DEGRAU.get(M.get('cat','Comum'),0),1); g['pv']-=x; P(f'    SANGUE QUE QUEIMA: espirra em {g["nome"]}: {x} ({g["pv"]})')
        if g['pv']<=0: cai(g,x,morreu)

def golpe_cria(g,c,M,G,morreu,rnd,varre=True):
    J=jog(); ch=J['ch']; t=J['t']+g['at']; crit=J['crit']; c['golpes']+=1; dfc=c['df']+(OFF if DOIS else 0)-min(CERCO[1],CERCO[0]*max(0,c['golpes']-1))
    if J['fum'] or (t<dfc and not crit) or (g.get('so20') and not crit): P(f'  {g["nome"]} na {c["nome"]}: {ch}+{g["at"]}={t} vs {dfc} erra'); return
    dd_=dados(g['dado'],crit=crit,plus=(J['extra'] if crit else 0)); br=int(sum(dd_)*g['mult'])+g['b']+g['nivel']//5; liq=max(br-(c['rd']//2 if crit else c['rd']),0)
    if fraco(g,c): liq*=2
    c['pva']-=liq; P(f'  {g["nome"]} na {c["nome"]}: {ch}+{g["at"]}={t} ACERTA{" CRÍTICO" if crit else ""} = {liq} ({c["pva"]})'+(' → MORTA' if c['pva']<=0 else ''))
    rende_ultima(M)
    if varre and c['pva']<=0 and g['nivel']>=c['nivel']*2 and crias_vivas(M):   # o GOLPE QUE VARRE vale para os dois lados (regra 3)
        P('    GOLPE QUE VARRE: segue na próxima cria'); golpe_cria(g,crias_vivas(M)[0],M,G,morreu,rnd,varre=False)

def feitico_nas_crias(g,mg,M,Jm,tm,so_crias=False,dobra=False):
    """feitiço ou Arte em ÁREA pega também as crias (uma jogada só; cada cria compara com a Defesa dela). Sem área, vai na primeira cria."""
    C=crias_vivas(M)
    if not C: return
    if Jm is None: Jm=jog(); tm=Jm['t']+mg.get('at',g['at'])
    if not (mg.get('area') or ARTES.get(chave_arte(mg.get('arte','')),{}).get('varios')): C=C[:1]
    C=C[:ARTES.get(chave_arte(mg.get('arte','')),{}).get('max_alvos',99)]
    for c in C:
        if Jm['fum']: dm=0
        else:
            dm=int(sum(dados(mg['dano'],crit=Jm['crit'],dobra=dobra))*mg.get('mult',1))
            if not Jm['crit'] and tm<c['df']+(OFF if DOIS else 0): dm//=2
        dd=max(dm-c['rd'],0)
        if fraco({'essencia':mg.get('essencia',g.get('essencia'))},c): dd*=2
        c['pva']-=dd; P(f'    {"" if not so_crias else g["nome"]+" lança: "}{c["nome"]}: {dd} ({c["pva"]})'+(' → MORTA' if c['pva']<=0 else ''))
    rende_ultima(M)

def arte(g,mg,M,G,morreu,rnd,dobra=False,elo=False):
    """MOTOR 9.1 (G30, Livro Nove 3): a ARTE DE ARMA com o efeito dela. Joga como feitiço da peça (2d20 + ataque contra a Defesa + 14: em cheio, metade ou
    crítico); o EFEITO só entra quando pega em cheio. Devolve True se feriu o chefe."""
    k=chave_arte(mg['arte']); A=ARTES.get(k,{}); nome=mg.get('nome') or mg['arte'].upper(); T=M.get('T',())
    enc=mg.get('encadeia') if not elo else None
    if enc:   # Livro Nove 3.4: ENCADEAR: Luta (2d20 + ataque) contra CD 15 + a soma dos círculos (+14); falha: perde a Estamina e a Ação
        lista=enc if isinstance(enc,list) else [enc]; soma=A.get('circ',2)+sum(ARTES.get(chave_arte(e['arte']),{}).get('circ',2) for e in lista)
        Jt=jog(); tt=Jt['t']+g['at']; alvo=15+soma+(OFF if DOIS else 0)
        if Jt['fum'] or tt<alvo: P(f'  {g["nome"]} tenta ENCADEAR ({nome} + {len(lista)}): Luta {tt} vs {alvo}: FALHA; perde a Estamina e a ação'); return False
        P(f'  {g["nome"]} ENCADEIA{" o REMATE" if len(lista)>1 else ""} (Luta {tt} vs {alvo}):')
        f1=arte(g,mg,M,G,morreu,rnd,elo=True); fs=[arte(g,e,M,G,morreu,rnd,dobra=(i==len(lista)-1),elo=True) for i,e in enumerate(lista)]
        return f1 or any(fs)
    if A.get('reacao')=='ponta': g['ponta']=(rnd,mg); P(f'  {g["nome"]} arma {nome}: a ponta espera quem entrar'); return False
    if A.get('reacao')=='guarda': g['guarda2']=rnd; P(f'  {g["nome"]} arma {nome}: vai anular um golpe num aliado ao lado'); return False
    if A.get('reacao')=='muralha': g['muralha_ate']=rnd+2; P(f'  {g["nome"]} ergue {nome}: por 3 rodadas ninguém passa por ele nem golpeia quem está atrás'); return False
    if M['pva']<=0: feitico_nas_crias(g,mg,M,None,None,so_crias=True,dobra=dobra); return False
    dob=dobra or any(M.get(c) for c in A.get('dobra_se',())); feriu=False; total=0
    for n in range(A.get('golpes',1)):
        if M['pva']<=0: break
        J=jog(crit17=A.get('crit17',False)); at=mg.get('at',g['at'])+A.get('at',0)-(2 if n else 0)-(2 if g.get('medo') or g.get('agarrado') else 0); t=J['t']+at
        dfm=M['df']+(OFF if DOIS else 0)+mod_df(M,rnd,corpo=not (A.get('longe') or g.get('longe')))
        cheio=False
        if J['fum']: dm=0; txt=f'{J["ch"]} DOIS 1: o golpe se perde'
        elif J['crit']: dm=int(sum(dados(mg['dano'],crit=True,dobra=dob))*mg.get('mult',1)); txt=f'{J["ch"]}+{at}={t} CRÍTICO'; cheio=True
        elif t>=dfm: dm=int(sum(dados(mg['dano'],dobra=dob))*mg.get('mult',1)); txt=f'{J["ch"]}+{at}={t} vs {dfm} pega em cheio'; cheio=True
        else: dm=int(sum(dados(mg['dano'],dobra=dob))*mg.get('mult',1))//2; txt=f'{J["ch"]}+{at}={t} vs {dfm} resistido: metade'
        rd=M['rd']; r_=A.get('rd')
        rd=0 if r_=='zero' else rd//2 if r_=='metade' else max(rd-r_,0) if isinstance(r_,int) else rd
        dd=max(dm-rd,0); fr=fraco({'essencia':mg.get('essencia',g.get('essencia'))},M)
        if fr: dd*=2
        if 'enxame' in T: dd=dd*2 if A.get('varios') else dd//2
        if fr and dd>0: M['_ferido_fraqueza']=True
        M['pva']-=dd; total+=dd; feriu=feriu or dd>0
        P(f'  {g["nome"]} · {nome}{" (dados dobrados)" if dob else ""}{" (2º golpe)" if n else ""}: {dm}; {txt} − RD {rd}{" ×2" if fr else ""} → {dd} ({M["pva"]})')
        if A.get('varios') and crias_vivas(M): feitico_nas_crias(g,mg,M,J,t,dobra=dob)
        devolve(M,g,dd,morreu,corpo=not A.get('longe'))
        if not cheio or M['pva']<=0: continue
        if A.get('quebra'): M['quebra_ate']=rnd+1; P(f'    QUEBRA-GUARDA: {M["nome"]} com −2 na Defesa até o fim da próxima rodada'+(' e sem escudo' if M.get('escudo') else ''))
        ef=A.get('efeito')
        if ef:
            cond,cd=ef
            if cond=='sangrando': M['sangrando']=True; P(f'    {M["nome"]} fica SANGRANDO (2% do PV por rodada)')
            elif cond=='derrubado' and not resiste_M(M,cd,'a queda'): M['derrubado']=True; P('    CAÍDO: −4 na Defesa contra corpo a corpo; levantar gasta 1 ação')
            elif cond=='preso' and not resiste_M(M,cd,'a prisão'): M['preso']=True; P('    PRESO: −2 na Defesa; não foge; 1 ação por rodada para se soltar')
            elif cond=='atordoado' and not resiste_M(M,cd,'o atordoamento'): M['atordoado']=True; P('    ATORDOADO: perde a próxima rodada')
        if A.get('tronco') and not M.get('_tronco') and not M.get('gente'):
            M['_tronco']=True; M['bac']=max(1,M['bac']-1); P(f'    DERRUBAR O TRONCO: {M["nome"]} perde 1 ataque por rodada até o fim da cena ({M["bac"]} ações)')
        if k=='bigorna' and dob: P(f'    BIGORNA: a armadura ou a casca de {M["nome"]} perde 1d6 [{d(6)}] de durabilidade')
    return feriu

def magia_M(M,mm,G,morreu,rnd,ultimo):
    """Lei 7: o INIMIGO lança feitiço ou Arte de arma: 2d20 + ataque contra a Defesa + 14 de cada alvo (em cheio, metade, crítico)"""
    A=ARTES.get(chave_arte(mm.get('arte','')),{}); nome=mm.get('nome') or mm.get('arte','feitiço'); V=vivos(G,rnd)
    alvos=V if (mm.get('area') or A.get('varios')) else [escolhe(M,V,ultimo,rnd)]
    alvos=alvos[:A.get('max_alvos',99)]; P(f'  {M["nome"]} · {nome}:')
    ef=mm.get('efeito') and (mm['efeito'],mm.get('cd',20)) or A.get('efeito')
    for g in alvos:
        for n in range(A.get('golpes',1)):
            if not g['vivo']: break
            J=jog(crit17=A.get('crit17',False)); at=mm.get('at',M['at'])+A.get('at',0)-(2 if n else 0); t=J['t']+at; df=g['df']+(OFF if DOIS else 0)+mod_df(g,rnd,corpo=not A.get('longe'))
            cheio=J['crit'] or (t>=df and not J['fum'])
            dm=0 if J['fum'] else int(sum(dados(mm['dano'],crit=J['crit']))*mm.get('mult',1))//(1 if cheio else 2)
            r_=A.get('rd'); rd=g['rd']; rd=0 if r_=='zero' else rd//2 if r_=='metade' else max(rd-r_,0) if isinstance(r_,int) else rd
            dd=max(dm-rd,0); g['pv']-=dd
            P(f'    em {g["nome"]}: {J["ch"]}+{at}={t} vs {df} '+('DOIS 1: nada' if J['fum'] else 'CRÍTICO' if J['crit'] else 'em cheio' if cheio else 'resiste: metade')+f' → {dd} ({g["pv"]})')
            if g['pv']<=0: cai(g,dd,morreu); break
            if cheio and A.get('quebra'): g['quebra_ate']=rnd+1; P(f'    {g["nome"]} com −2 na Defesa até o fim da próxima rodada')
            if cheio and ef: aplica_cond(g,ef[0],ef[1],M)

def cai(g,liq,morreu):
    if 'Segundo Coração' in g.get('doms',()) and g.get('_sc',0)<(2 if 'Segundo Coração' in g.get('doms_grau2',()) else 1):   # G26: ao cair a 0 fica com 1 e age na vez dele
        g['_sc']=g.get('_sc',0)+1; g['pv']=1; g['vivo']=True; P(f'    {g["nome"]} cai… e o SEGUNDO CORAÇÃO bate: fica com 1 PV e segue (depois da cena, Exausto até dormir)'); return
    g['vivo']=False
    if 'Voz de Mando' in g.get('doms',()): P(f'    a VOZ DE MANDO cala: a tropa de {g["nome"]} testa moral com −4 (à mão, se houver tropa)')
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
    T=M.get('T',())
    if g.get('ponta') and g['ponta'][0]==rnd and g['vivo']:   # PONTA QUE ESPERA (Arte de lança, 2º): Reação contra quem entra no alcance; se acerta, ele para
        mg=g['ponta'][1]; g['ponta']=None; J0=jog(); t0=J0['t']+mg.get('at',g['at']); df0=M['df']+(OFF if DOIS else 0)
        if not J0['fum'] and (t0>=df0 or J0['crit']):
            dm=int(sum(dados(mg['dano'],crit=J0['crit']))*mg.get('mult',1)); dd=max(dm-M['rd'],0)
            if fraco({'essencia':mg.get('essencia',g.get('essencia'))},M): dd*=2
            M['pva']-=dd; P(f'    PONTA QUE ESPERA de {g["nome"]}: {J0["ch"]}+{mg.get("at",g["at"])}={t0} vs {df0} ACERTA: {dd} ({M["pva"]}) → {M["nome"]} PARA: o golpe não sai'); return
        P(f'    PONTA QUE ESPERA de {g["nome"]}: {t0} vs {df0} erra; o golpe vem')
    J=jog(); ch=J['ch']; faro=2 if 'faro_ferida' in T and g['pv']<g['pvmax'] else 0; t=J['t']+M['at']+faro; crit=J['crit']; g['golpes']=g.get('golpes',0)+1
    df=g['df']+(OFF if DOIS else 0)+(g.get('aura_def',[0,0])[0] if g.get('aura_def') else 0)-min(CERCO[1],CERCO[0]*max(0,g['golpes']-g['ac']))+mod_df(g,rnd)
    if J['fum'] or (t<df and not crit): P(f'    ataque em {g["nome"]}: {ch}+{M["at"]+faro}={t} vs {df} erra'); return
    dd_=dados(M['dado'],crit=crit,plus=(J['extra'] if crit else 0)+(1 if g.get('_pele_oposta') else 0)); br=int(sum(dd_)*M['mult'])+M.get('b',0)+M['nivel']//5; rd=g['rd']//2 if crit else g['rd']; liq=max(br-rd,0)
    if g.get('desfaz',0)>0 and liq>0 and (crit or liq>=g['pvmax']*0.2):   # 436 (G9): a peça que 'desfaz um golpe por dia' (o Gibão do rei) desfaz o golpe grande
        g['desfaz']-=1; P(f'    ataque em {g["nome"]}: {ch}+{M["at"]+faro}={t} vs {df} ACERTA{" CRÍTICO" if crit else ""} {liq} → DESFEITO ({g.get("desfaz_nome","a peça")}, 1x por dia)'); return
    gd=[x for x in G if x is not g and x['vivo'] and x['fora']==0 and x.get('guarda2')==rnd] if liq>0 else []
    if gd:   # GUARDA DE DOIS (Arte de escudo, 4º): Reação: anula um golpe num aliado ao lado
        gd[0]['guarda2']=None; P(f'    ataque em {g["nome"]}: {ch}+{M["at"]+faro}={t} vs {df} ACERTA {liq} → ANULADO pela GUARDA DE DOIS de {gd[0]["nome"]}'); return
    g['pv']-=liq; s=f'    ataque em {g["nome"]}: {ch}+{M["at"]+faro}={t} vs {df} ACERTA{" CRÍTICO" if crit else ""} {dd_}×{M["mult"]}+{M.get("b",0)}+{M["nivel"]//5}={br} − RD {rd} = {liq} ({g["pv"]})'
    if M.get('veneno') and g['pv']>0:
        vg=sum(ex())+g.get('vigor',10)
        if vg<M['veneno']['cd']+(OFF if DOIS else 0): g['veneno']=M['veneno']['rodadas']; s+=f' · VENENO (Vigor {vg})'
    if 'agarra' in T and g['pv']>0 and liq>0 and not g.get('agarrado'): g['agarrado']=True; s+=' · AGARRADO (−2 na Defesa e no ataque; a ação vai em se soltar)'
    if 'rouba_folego' in T and liq>0:
        g['folego_roubado']=g.get('folego_roubado',0)+2; s+=' · rouba 2 de fôlego'
        for rec in ('estamina','mana'):
            if g.get(rec,0)>0: g[rec]=max(0,g[rec]-2); break
    P(s)
    if g['pv']<=0:
        cai(g,liq,morreu)
        if varre and g['nivel']*2<=M['nivel']:
            V=vivos(G,rnd)
            if V: P('    GOLPE QUE VARRE: segue no próximo'); ataque(M,V[d(len(V))-1],G,morreu,rnd,varre=False)
        return
    # contra-golpe de gente de nível alto
    if g.get('reac',0)>0 and (liq>=g['pvmax']*0.10 or crit) and M['pva']>0 and not g.get('paralisado'):
        g['reac']-=1; J2=jog(); c2=J2['ch']; t2=J2['t']+g['at']; cr2=J2['crit']
        if not J2['fum'] and (t2>=M['df']+(OFF if DOIS else 0) or cr2):
            dd2=dados(g['dado'],crit=cr2); br2=int(sum(dd2)*g['mult'])+g['b']+g['nivel']//5; l2=max(br2-(M['rd']//2 if cr2 else M['rd']),0)
            if fraco(g,M): l2*=2
            if 'enxame' in T: l2//=2
            M['pva']-=l2; P(f'    CONTRA-GOLPE de {g["nome"]}: {c2} → {l2} ({M["pva"]})'); devolve(M,g,l2,morreu)
    lim=0.25 if g.get('heroi') else 0.40
    if g['vivo'] and g['pv']<=g['pvmax']*lim and not g.get('fica') and not g.get('agarrado') and not g.get('preso'):
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
            if g['pv']<=0: cai(g,dm,morreu)

def confere_arquivo(F, nome):
    """MOTOR 6: arquivo de luta com campo faltando avisa QUAL campo, em vez de cair no meio da luta"""
    erros=[]
    if 'monstro' not in F or 'grupo' not in F: sys.exit(f'{nome}: o arquivo precisa de "monstro" e "grupo".')
    for k in ('nome','nivel','pv','df','at','dado','mult'):
        if k not in F['monstro']: erros.append(f'monstro: falta "{k}"')
    if not F['monstro'].get('gente') and F['monstro'].get('cat','Comum') not in RDCAT: erros.append(f'monstro: categoria desconhecida "{F["monstro"].get("cat")}" (use {", ".join(RDCAT)})')
    _,fora=le_tracos(F['monstro'])   # MOTOR 9.1: traço que o script não conhece para ANTES do dado
    for t in fora: erros.append(f'monstro: traço que o luta.py não conhece: "{t}" (python3 luta.py tracos mostra a lista)')
    if liso(F.get('luz','')) not in ('','escuro','forte','normal'): erros.append('"luz" tem de ser "escuro", "forte" ou "normal"')
    for mm in F['monstro'].get('magias') or []:
        if not all(k in mm for k in ('dano','rodada')): erros.append('monstro: cada item de "magias" precisa de dano e rodada')
        if mm.get('arte') and chave_arte(mm['arte']) not in ARTES: erros.append(f'monstro: Arte desconhecida "{mm["arte"]}"')
    if not F['grupo']: erros.append('grupo vazio')
    for n,g in enumerate(F['grupo'],1):
        for k in ('nome','at','dado','mult','b','df','rd','pv'):
            if k not in g: erros.append(f'grupo #{n} ({g.get("nome","sem nome")}): falta "{k}"')
        for mg in magias_de(g):
            lista=[mg]+(mg['encadeia'] if isinstance(mg.get('encadeia'),list) else [mg['encadeia']] if mg.get('encadeia') else [])
            for i,x in enumerate(lista):
                reac=ARTES.get(chave_arte(x.get('arte','')),{}).get('reacao') in ('guarda','muralha')
                falta=[k for k in (('rodada',) if reac else ('dano','cd','rodada') if i==0 else ('dano',)) if k not in x]
                if falta: erros.append(f'grupo #{n} ({g.get("nome")}): a magia precisa de dano, cd e rodada')
                if x.get('arte') and chave_arte(x['arte']) not in ARTES: erros.append(f'grupo #{n} ({g.get("nome")}): Arte desconhecida "{x["arte"]}" (python3 luta.py artes)')
                if i and not x.get('arte'): erros.append(f'grupo #{n} ({g.get("nome")}): só se encadeia Arte com Arte')
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
    c=Counter(); mortes=Counter(); cai_=Counter(); recua=Counter(); rs=[]; sobra=[]; tratos=0; chefe=0; com_crias=0
    for _ in range(n):
        r=luta(F); c[r['res']]+=1; rs.append(r['rnd']); tratos+=bool(r.get('trato')); chefe+=r['pv']<=0; com_crias+=bool(r['M'].get('n_crias'))
        if r['res']!='morto': sobra.append(max(r['pv'],0)/r['pvm'])
        for m in set(r['mortos']): mortes[m]+=1
        for g in r['G']:
            if g.get('caido') or g['nome'] in r['mortos']: cai_[g['nome']]+=1
            elif g.get('recuou'): recua[g['nome']]+=1
    SIM=False
    M=F['monstro']; L=[]
    L.append(f"RÉGUA de {n} lutas simuladas (sem valor de jogo; margem de ±{196*(0.25/n)**0.5:.0f} pontos) · {M['nome']} ({M.get('cat','gente')} {M['nivel']}) contra {len(F['grupo'])}")
    ordem=[('morto',f"{M['nome']} MORRE"),('fugiu',f"{M['nome']} foge"),('grupo caiu','O GRUPO CAI'),('empate','sem desfecho no tempo')]
    L.append('  desfecho: '+' · '.join(f'{rot} {pct(c[k],n)}' for k,rot in ordem if c[k]))
    L.append(f'  duração: mediana {quantil(rs,0.5)} rodadas (de {quantil(rs,0.1)} a {quantil(rs,0.9)} em 8 de cada 10 lutas)')
    if sobra: L.append(f'  quando o bicho NÃO morre, sai com {100*quantil(sobra,0.5):.0f}% do PV (entre {100*quantil(sobra,0.1):.0f}% e {100*quantil(sobra,0.9):.0f}%)')
    if com_crias: L.append(f'  CRIAS em {pct(com_crias,n)} das lutas · o chefe cai em {pct(chefe,n)} (o resto é das crias)')
    if tratos: L.append(f'  2ª fase [6]: ele OFERECE UM TRATO em {pct(tratos,n)} das lutas (a régua segue como se a casa recusasse)')
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

def continua(F,r,nome):
    """2ª fase [6], o TRATO: grava o ponto em que a luta parou (se a casa recusar, a luta segue deste arquivo, sem rolar de novo o que já saiu)"""
    N=json.loads(json.dumps(F)); N['monstro']['pv_atual']=r['pv']; N['monstro']['fase']=False; N['rodada0']=r['rnd']; N['iniciativa']=False
    N['fase_feita']=True; N['furia_feita']=bool(r.get('furia')); N['surpresa']=0; N['grupo']=[]
    for g0,g in zip(F['grupo'],r['G']):
        if g['nome'] in r['mortos'] or g['pv']<=0 or g.get('recuou'): continue
        x=dict(g0); x['pv']=g['pv']; x['pvmax_real']=g['pvmax']
        for k in ('desfaz','estamina','mana'):
            if k in g: x[k]=g[k]
        N['grupo'].append(x)
    for k in ('essencia','fraqueza','covil','rd'):
        if k in r['M']: N['monstro'][k]=r['M'][k]
    saida=re.sub(r'\.json$','',nome)+'_continua.json'; json.dump(N,open(saida,'w',encoding='utf-8'),ensure_ascii=False,indent=1); return saida

if __name__=='__main__':
    if len(sys.argv)<2: sys.exit(__doc__)
    if sys.argv[1]=='tracos':
        print('TRAÇOS que o luta.py lê em "tracos" (o texto do gerador ou a chave curta):')
        for c,ini in TRACOS: print(f'  {c:16s} {ini}'+('   [à mão: '+A_MAO[c]+']' if c in A_MAO else ''))
        sys.exit(0)
    if sys.argv[1]=='artes':
        print('ARTES DE ARMA (Livro Nove 3.3) que o luta.py roda: ponha "arte": "chave" no item de "magias" (o dano e o multiplicador continuam na ficha)')
        for k,a in ARTES.items(): print(f'  {k:22s} {a["circ"]}º · '+', '.join(f'{x}={v}' for x,v in a.items() if x!='circ'))
        sys.exit(0)
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
        Mf=r['M']; Tf=Mf.get('T',())   # MOTOR 9.1: o que os traços deixam para depois da luta
        if r['res']=='trato':
            print('⏸ TRATO (2ª fase [6], Lei 15): o ponto da luta ficou em', continua(F,r,sys.argv[1]), '· se a casa recusar: python3 luta.py nesse arquivo (não rola de novo o que já saiu)')
        if Mf.get('n_crias'):
            viva=[c for c in Mf['crias'] if c.get('rendida')]
            print(f"CRIAS: {Mf['n_crias']} saíram" + (f" · UMA ESTÁ VIVA E RENDIDA ({viva[0]['cat']} {viva[0]['nivel']}): o jogador decide se a leva (G25: python3 cria.py nova) ou se a mata" if viva else ''))
        rb={g['nome']:g['folego_roubado'] for g in r['G'] if g.get('folego_roubado')}
        if rb: print('ROUBA O FÔLEGO: tirar da Estamina ou da Mana de cada um:', rb)
        if Mf.get('_roidas'): print('DEVORA METAL: a arma perde 1 categoria:', Mf['_roidas'])
        if r['res']=='morto' and 'carrega_tesouro' in Tf: print('CARREGA UM TESOURO: o tesouro do covil (G17) rola DUAS vezes')
        if 'doenca' in Tf: print('CARREGA DOENÇA: quem foi ferido por ele testa Vigor (declarar no selo, como nas outras vezes)')
        caidos=[g['nome'] for g in r['G'] if g['pv']<=0]
        if r['mortos'] or caidos:   # 426 (G9): a trava que faltou na forquilha
            print('⛔ G9: PARAR AQUI, DENTRO DA HORA. Mortos:', r['mortos'] or 'nenhum', '· caídos:', caidos or 'nenhum')
            print('   antes de o tempo andar, o jogador decide: ERGUER O CAÍDO (Luz 6º, o rei sabe: até 1 hora; 30 de Mana; 1 PV e −1 para sempre num atributo) · o SERVO ARMADO (a Receita Mestra do rei) · Medicina nos caídos · onde estão os corpos')
