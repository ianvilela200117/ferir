#!/usr/bin/env python3
"""LEI DO VALOR (regra da casa, Dia 201, pedido do jogador). Substitui obra_dado.py.
Sem teto, sem receita obrigatória: TUDO É VALOR QUE SOMA AO DADO. O dado continua soberano (2d20 explosivos).

TOTAL = 2d20 EXPLOSIVOS (cada 20 rola outro d20 e soma, sem limite)
      + MÃO (maestria + atributo do ofício ÷ 10 + Sorte ÷ 20 + nível ÷ 10 + talentos)
      + MATERIAL (o melhor que for pelo menos 1/5 da massa; + afinidade/propriedades)
      + FERRAMENTAS (martelo + bigorna + 1 de apoio pela metade; e os efeitos delas)
      + OFICINA + RECEITA (bônus, nunca exigida) + AJUDANTES (máx. +6) + EXTRAS (anel, broche, bênção, pressa...)
      + PORCENTAGEM (efeitos Lendários: +10% dos valores) · CD − X (efeitos que baixam a dificuldade)
A peça sai na MAIOR categoria cuja CD o total alcança. CDs (iguais para todos):
  Comum 15 · Incomum 26 · Raro 42 · Épico 55 · Único 68 · Lendário 84 · Mítico 102 · Primordial 125. Abaixo de 15: material perdido.
OS DADOS: cada 20 = +1 efeito e uma peculiaridade · os dois abrindo em 20 = OBRA-PRIMA (1d6: 1-3 sobe uma categoria; 4-6 +1 efeito)
  · três 20+ = MARAVILHA · cinco+ = LENDA · QUASE (o total ficou a 3 ou menos da CD seguinte) = +1 efeito (a peça quis subir)
  · um dado em 1 = complicação 1d6 (1 a peça se perde · 2-3 cai uma categoria · 4-6 menor) · os dois em 1 = a peça se perde · 1 em 10 obras: peculiaridade.
REQUISITO DE NÍVEL para usar inteira: Comum 1 · Incomum 5 · Raro 20 · Épico 40 · Único 70 · Lendário 110 · Mítico 180 · Primordial 260.

Uso:
  python3 obra_valor.py obra "Nome" TIPO quem=ferir mat=raro [opções]
  python3 obra_valor.py encantar "Feitiço" CIRCULO CAT_DO_ITEM quem=ferir_enc cond=raro [opções]
  python3 obra_valor.py reforja "Nome" TIPO CAT_ATUAL quem=ferir [mat=CAT] [opções]
  python3 obra_valor.py conserto "Nome" CAT quem=ferir [opções]
  python3 obra_valor.py sim quem=ferir mat=raro [opções]        (só a chance, sem valor de jogo)
  python3 obra_valor.py fichas                                  (mostra as fichas de valor guardadas)
Opções: mao=N (no lugar da ficha) · mat=CAT · matx=N · martelo=CAT · bigorna=CAT · apoio=CAT · ofic=NOME|N · rec=GRAU · condicao=1
        ajud=N (soma dos ajudantes) · extra=N · pct=N · cdmenos=N · alma=N · fortuna=N · x19=1 (o 19 também explode)
TIPO: arma armadura ferramenta objeto foco

MOTOR 6 (Dia 379): as fichas de Ferir (quem=ferir, quem=ferir_enc) leem o NÍVEL e os ATRIBUTOS de ficha.json. Antes os
números iam escritos à mão dentro deste arquivo ("nível 142 ÷ 10", "Inteligência 171") e ficavam velhos a cada subida.
As ferramentas com categoria acima do que o nível deixa usar rendem pela regra do requisito (Sob Medida: −30):
no 150 a Tenaz, o Buril, o Fole e o Martelo de Zeieth passam a render como Míticos sozinhos; no 230 o Martelo rende Primordial.
Depois de uma obra de Ferir que dá XP, o script mostra a linha pronta para lançar (ficha.py xp).
"""
import sys, secrets, os, re, json, copy
from obra_aberta import EFEITOS, PECULIAR, MARAVILHA, ensure
from feiticos import G as GRIMORIO

CAT  = ['comum','incomum','raro','epico','unico','lendario','mitico','primordial']
NAOTREME=0
NOME = ['Comum','Incomum','Rara','Épica','Única','Lendária','Mítica','Primordial']
CD   = [15,26,42,55,68,84,102,125]
NEF  = [0,1,1,2,3,4,6,8]
XP   = [5,20,80,300,800,2500,10000,50000]
V_MAT  = {'sucata':-3,'comum':0,'incomum':2,'raro':4,'epico':7,'unico':10,'lendario':14,'mitico':18,'primordial':24}
V_FERR = {'improvisada':-2,'nenhuma':0,'comum':0,'incomum':1,'raro':2,'epico':3,'unico':5,'lendario':7,'mitico':10,'primordial':14}
V_OFIC = {'campo':-4,'improvisada':-2,'comum':0,'boa':2,'grande':3,'mestra':4,'lendaria':6,'mitica':8,'primordial':12}
V_REC  = {'nenhuma':0,'fragmento':1,'esboco':2,'receita':4,'mestra':5}
CIRC_AJ = {1:-10,2:-5,3:0,4:5,5:10,6:15,7:20}

# FICHAS DE VALOR (o que cada um soma; mudar aqui quando subir de nível, maestria ou equipamento)
FICHAS = {
 'ferir': dict(desc='Ferir, Forja (Lendário)', mao=[('Maestria Forja Lendário',12),('Inteligência 171 ÷ 10 (teto 10)',10),('Sorte 95 ÷ 20',4),('nível 142 ÷ 10',14),
               ('Mão de Mestre (Técnica, Matéria e Processo; talentos do 80 e do 90)',6),('Olho do Material',1),('Fole Firme 2',1),('Alma no Aço 2',1),('Mão que Não Treme 3',3)],
               martelo='lendario', martelo_nome='O MARTELO DE ZEIETH (Primordial, 352; rende Lendário até o 150, Mítico até o 230, com o nome dele)', martelo_x=[('martelo de zeieth: fala, soa diferente na falha (+2 na Matéria)',2)], bigorna='lendario', bigorna_nome='A MATRIZ',
               apoio='lendario', apoio_nome='TENAZ DE EIURVO (Mítica, 229; Lendária desde o 80, Mítica no 150)', apoio_x=[('FOLE DE ARVEL (Mítico, 267; 3ª ferramenta pela metade: Lendário desde o 80)',3),('fole: o arvel como ferramenta (+3 em toda obra de forja)',3),('fole: segura o calor certo (+2 no Processo)',2)], ofic='lendaria', ofic_nome='Fornalha que Não Apaga', alma=1, naotreme=1),
 'ferir_enc': dict(desc='Ferir, Encantamento (Mestre)', mao=[('Maestria Encantamento Mestre',9),('(Int 171 + Afinidade 157) ÷ 20 (teto 10)',10),('Sorte 95 ÷ 20',4),
               ('nível 142 ÷ 10',14),('Mão de Mestre (Processo, Técnica, Matéria)',3),('Mão que Não Treme 3 (toda obra)',3),('Mão que Encanta 5 (ramo Processo; pontos do 111 e do 153)',10),('Mão que Sela 4 (ramo Técnica, pontos do 78, 81, 84 e 114; proposta do Mestre)',8),('Olho do Encanto 4 (ramo Matéria, pontos do 87, 90, 93 e 102)',8),('Bancada do Encanto 4 (ramo Oficina, pontos do 96, 99, 105 e 117; proposta do Mestre)',8),('Condutor Fiel 4 (grau 4, ponto do 108; proposta do Mestre)',2),('Assinatura do Encanto 4: Selo do Rei, Duas Vozes, Peso da Mão, Alma Gravada (pontos do 120, 123, 126 e 129; proposta do Mestre; +2 a mais no 4º círculo para cima)',5),('Mão que Escuta 4 (ramo Matéria; ponto do 138, proposta do Mestre)',2),('Alma no Aço 5 (ramo Assinatura; pontos do 141, do 147 e do 150; só peça que ele mesmo forjou)',4),('Olho do Material (+2 em Matéria, toda obra)',1)],
               martelo='lendario', martelo_nome='BURIL DE HAMIR (Mítico, 230; Lendário desde o 80, Mítico no 150)', martelo_x=[('buril: o Hamir como ferramenta (+8 em Infusão e Encantamento)',8)], bigorna='mitico', bigorna_nome='O BERÇO DE SELO (Mítico, 407: vorthil, o coração do Vorthen e veyine; a bigorna do encantador)', bigorna_x=[('berço: Gelo com Gelo, B 5 (+5 em Técnica: o selo não empena)',5),('berço: o veyine como ferramenta (+2 em Infusão e Encantamento)',2),('berço: fala, soa diferente quando a peça tem falha (+2 na Matéria)',2)], apoio='lendario', apoio_nome='LUVAS DO ENCANTADOR (Lendárias de veyine, 218; Lendárias desde o 80)',
               apoio_x=[('luvas: o veyine como ferramenta (+2 em Infusão e Encantamento)',2)], ofic='lendaria', ofic_nome='Fornalha que Não Apaga', alma=1),
 'herkald': dict(desc='Herkald, Forja (Mestre), nível 70', mao=[('Maestria Forja Mestre',9),('Inteligência ~50 ÷ 10',5),('Sorte ~40 ÷ 20',2),('nível 76 ÷ 10',7),('mão velha',2)],
               martelo='unico', martelo_nome='o MARTELO dele (Único)', bigorna='raro', apoio='comum', ofic='lendaria', ofic_nome='Fornalha'),
 'skedda': dict(desc='Skedda, Runas/Encantamento (Treinado), nível 21', mao=[('Maestria Treinado',6),('(Int+Afinidade) ÷ 20',5),('Sorte ÷ 20',2),('nível 21 ÷ 10',2)],
               martelo='unico', martelo_nome='o BURIL dela (Único; rende Épico até o 70)', bigorna='nenhuma', apoio='comum', ofic='lendaria'),
 'aprendiz': dict(desc='aprendiz (Iniciante, nível 5)', mao=[('Maestria Iniciante',3),('Inteligência 30 ÷ 10',3),('Sorte 40 ÷ 20',2)],
               martelo='comum', bigorna='comum', apoio='comum', ofic='comum'),
}

REQ = [1,5,20,40,70,110,180,260]   # requisito de nível para usar inteira (o mesmo do cabeçalho)
# a categoria VERDADEIRA de cada ferramenta de Ferir (o que ela rende hoje sai do nível)
REAL = {'ferir': {'martelo':'primordial', 'apoio':'mitico', 'fole':'mitico'}, 'ferir_enc': {'martelo':'mitico'}}

NPC_FICHA = {'herkald': 'Herkald', 'skedda': 'Skedda'}

def ficha_viva():
    try:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'ficha.json'),encoding='utf-8') as fh: return json.load(fh)
    except Exception: return None

def rende(real, nivel, desconto):
    """a maior categoria, até a verdadeira, que o nível deixa usar inteira (requisito − desconto do Sob Medida)"""
    i = CAT.index(real)
    while i > 0 and REQ[i]-desconto > nivel: i -= 1
    return CAT[i]

def viva(chave, f):
    """devolve a ficha com nível, atributos e ferramentas recalculados de ficha.json (só as de Ferir)"""
    if chave in NPC_FICHA:   # ajudante com ficha própria: o nível vem do livro dos NPCs
        try:
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'npcs.json'),encoding='utf-8') as fh: nv = json.load(fh)[NPC_FICHA[chave]]['nivel']
        except Exception: return f
        f = copy.deepcopy(f)
        f['mao'] = [((f'nível {nv} ÷ 10', nv//10) if re.match(r'^nível \d+ ÷ 10', r) else (r, v)) for r, v in f.get('mao', [])]
        return f
    F = ficha_viva()
    if not F or chave not in REAL: return f
    f = copy.deepcopy(f); n = F['nivel']; A = F['atributos']; desc = F.get('sob_medida_desconto', 30)
    herdeiro = F.get('classe_lendaria') == 'Herdeiro do Rei-Ferreiro'
    if herdeiro:   # 478 (a classe HERDEIRO DO REI-FERREIRO, compendio/04_classes.md): MÃO DE REI e MARTELO E BIGORNA
        n = max(n, F.get('nivel_maximo', n))   # a Mão conta o maior nível que ele já teve
        desc = 999                             # as peças que ele mesmo forjou rendem inteiras na mão dele (sem requisito)
        if chave == 'ferir':                   # o Martelo do Rei é o martelo da obra; com a Matriz, cada um soma +14
            f['martelo'] = 'lendario'; f['martelo_nome'] = 'O MARTELO DO REI (Ferramenta de Rei, de Dragal)'
            f['martelo_x'] = [('Martelo e Bigorna (Herdeiro): o Martelo do Rei soma o dobro', 7)]
            f['bigorna_x'] = [('Martelo e Bigorna (Herdeiro): a Matriz soma o dobro', 7)]
            REAL[chave] = {k: v for k, v in REAL[chave].items() if k != 'martelo'}
    I, S, Af = A['Inteligência'], A['Sorte'], A['Afinidade']
    troca = [(r'^Inteligência \d+ ÷ 10 \(teto 10\)', f'Inteligência {I} ÷ 10 (teto 10)', min(10, I//10)),
             (r'^\(Int \d+ \+ Afinidade \d+\) ÷ 20 \(teto 10\)', f'(Int {I} + Afinidade {Af}) ÷ 20 (teto 10)', min(10, (I+Af)//20)),
             (r'^Sorte \d+ ÷ 20', f'Sorte {S} ÷ 20', S//20),
             (r'^nível \d+ ÷ 10', f'nível {n} ÷ 10', n//10)]
    mao = []
    for rot, v in f.get('mao', []):
        for rx, novo, val in troca:
            if re.match(rx, rot): rot, v = novo, val
        mao.append((rot, v))
    f['mao'] = mao
    for slot, real in REAL[chave].items():
        if slot == 'fole':
            f['apoio_x'] = [((r, V_FERR[rende(real, n, desc)]//2) if r.startswith('FOLE DE ARVEL') else (r, v)) for r, v in f.get('apoio_x', [])]
        else:
            f[slot] = rende(real, n, desc)
    return f

d = lambda n: secrets.randbelow(n)+1
def norm(s): return s.lower().replace('é','e').replace('ú','u').replace('í','i').replace('ê','e').replace('ç','c').replace('á','a').replace('ó','o')
def opt(a,k,default=None):
    for x in a:
        if x.startswith(k+'='): return x[len(k)+1:]
    return default
def die(x19=False):
    ch=[d(20)]
    while ch[-1]==20 or (x19 and len(ch)==1 and ch[0]==19): ch.append(d(20))
    return ch

def valores(a, modo='obra'):
    """monta a lista de (rótulo, valor) a partir da ficha e das opções; devolve (linhas, soma, cdmenos, x19, alma)"""
    quem = opt(a,'quem','') or ''
    f = viva(quem, FICHAS.get(quem, {}))
    L=[]
    if opt(a,'mao') is not None: L.append(('MÃO (dada)', int(opt(a,'mao'))))
    else: L += [('MÃO · '+r,v) for r,v in f.get('mao',[])]
    if modo in ('obra','sim','reforja'):
        m=norm(opt(a,'mat','comum')); L.append((f'MATERIAL {m}', V_MAT[m]))
    if modo=='encantar':
        c=norm(opt(a,'cond','comum')); L.append((f'CONDUTOR {c}', V_MAT[c]))
    if modo=='conserto':
        L.append(('MATERIAL (o mesmo da peça)',0))
    if opt(a,'matx'): L.append(('material: afinidade/propriedades', int(opt(a,'matx'))))
    for slot,meia in (('martelo',False),('bigorna',False),('apoio',True)):
        c=norm(opt(a,slot, f.get(slot,'nenhuma')))
        v=V_FERR[c]//2 if meia and V_FERR[c]>0 else V_FERR[c]
        nome=f.get(slot+'_nome',slot)
        if v or c!='nenhuma': L.append((f'FERRAMENTA {nome} ({c}{", metade" if meia else ""})', v))
        for r,x in f.get(slot+'_x',[]): L.append(('FERRAMENTA · '+r,x))
    o=opt(a,'ofic', f.get('ofic','comum'))
    try: ov=int(o); onome='oficina'
    except ValueError: ov=V_OFIC[norm(o)]; onome=f.get('ofic_nome',o)
    L.append((f'OFICINA {onome}', ov))
    r=norm(opt(a,'rec','nenhuma'));
    if V_REC[r]: L.append((f'RECEITA ({r})', V_REC[r]))
    if opt(a,'condicao')=='1': L.append(('RECEITA: condição cumprida',3))
    aj=min(int(opt(a,'ajud',0)),6)
    if aj: L.append(('AJUDANTES (máx. +6)',aj))
    if opt(a,'extra'): L.append(('EXTRAS', int(opt(a,'extra'))))
    s=sum(v for _,v in L)
    p=int(opt(a,'pct',0))
    if p: add=s*p//100; L.append((f'+{p}% dos valores',add)); s+=add
    global NAOTREME
    NAOTREME=int(opt(a,'naotreme', f.get('naotreme',0)))
    return L, s, int(opt(a,'cdmenos',0)), opt(a,'x19')=='1', int(opt(a,'alma', f.get('alma',0))), int(opt(a,'fortuna',0))

def mostra(L,s,cdm):
    for r,v in L: print(f'    {v:+3d}  {r}')
    print(f'    ---- SOMA DOS VALORES: {s}' + (f' · CD −{cdm}' if cdm else ''))

def rola(s, alma, fort, x19, need, naotreme=0):
    A=die(x19); B=die(x19); log=[f'dados de saída: {A} + {B} = {s+sum(A)+sum(B)}']; rev=0
    for X in (A,B):
        if naotreme and X[0]==1: X[0]=2; naotreme=0; log.append('MÃO QUE NÃO TREME (1x por dia): o 1 natural vira 2')
    tot=lambda: s+sum(A)+sum(B)
    for nome,n,custo in (('ALMA OUVIDA (sem Revés)',alma,0),('Fortuna (+1 Revés)',fort,1)):
        for _ in range(n):
            if not need(tot(),A,B): break
            low = A if (A[0]==1 or (sum(A)<=sum(B) and B[0]!=1)) else B
            old=list(low); low[:]=die(x19); log.append(f'{nome}: {old} → {low} (total {tot()})'); rev+=custo
    return A,B,tot(),log,rev

def cat_de(T,cdm,atual=None):
    r=-1
    for c in range(8):
        extra=10*max(0,c-atual-1) if atual is not None and atual>=0 else 0   # Dia 204: na REFORJA, cada categoria além da primeira pede +10
        if T>=CD[c]-cdm+extra: r=c
    return r

def efeitos(nomep,tipo,f,extra,marav,npec,de=0):
    nef=max(NEF[f]-NEF[de],0) if de else NEF[f]
    mag = 1 if (f>=4 and de<4) else 0
    pool=list(EFEITOS[tipo]); n=max(nef-mag,0)+extra
    for j in range(min(n,len(pool))): print(f'    efeito novo {j+1}: {ensure(pool.pop(secrets.randbelow(len(pool))))}')
    if mag:
        pm=[g for g in GRIMORIO if g[1]<=(3 if f==4 else 6)]; e_,c_,n_,ef_,t_=pm[d(len(pm))-1]
        print(f'    efeito de magia (d{len(pm)} do grimório): {n_} ({e_} {c_}º): {ef_} — 1x por cena, sem saber magia (se não couber na peça, rerrolar)')
    p2=list(MARAVILHA)
    for _ in range(marav): print(f'    MARAVILHA: {ensure(p2.pop(secrets.randbelow(len(p2))))}')
    p3=list(PECULIAR)
    for _ in range(npec): print(f'    PECULIARIDADE: {ensure(p3.pop(secrets.randbelow(len(p3))))}')

def obra(a, reforja=False):
    if reforja: nomep,tipo,atual=a[1],a[2],CAT.index(norm(a[3]))
    else: nomep,tipo=a[1],a[2]; atual=-1
    L,s,cdm,x19,alma,fort=valores(a,'reforja' if reforja else 'obra')
    if reforja:
        mv=V_MAT[norm(opt(a,'mat','comum'))]; pv=V_MAT[CAT[atual]]
        L=[x for x in L if not x[0].startswith('MATERIAL')]
        L.insert(0,(f'MATERIAL: a própria peça ({NOME[atual]}) ou o material novo, o melhor' ,max(mv,pv)))
        L.insert(1,('REFORJA: o aço já conhece a forma',2)); s=sum(v for _,v in L)
    print(('REFORJA' if reforja else 'OBRA')+f' "{nomep}" ({tipo})' + (f' · hoje {NOME[atual]}' if reforja else ''))
    mostra(L,s,cdm)
    print('    CDs: '+' · '.join(f'{NOME[c]} {CD[c]-cdm+(10*max(0,c-atual-1) if reforja else 0)}' for c in range(8)) + ('  (reforja: +10 por categoria além da primeira)' if reforja else ''))
    quer=opt(a,'quer')
    if reforja: need=lambda T,A,B: cat_de(T,cdm,atual)<=atual or A[0]==1 or B[0]==1
    elif quer: need=lambda T,A,B: cat_de(T,cdm)<CAT.index(norm(quer)) or A[0]==1 or B[0]==1
    else: need=lambda T,A,B: A[0]==1 or B[0]==1 or min(sum(A),sum(B))<=7   # política declarada: rerrola o dado ruim (1 a 7)
    A,B,T,log,rev=rola(s,alma,fort,x19,need,NAOTREME)
    print(f'  dados finais: {A} + {B} → TOTAL {T}')
    for l in log: print('  '+l)
    if rev: print(f'  Revés +{rev}')
    if A[0]==1 and B[0]==1:
        if reforja: print(f'  OS DOIS EM 1: a peça cai a {NOME[max(atual-1,0)]} e perde o efeito mais fraco (não se perde inteira: respeito pelo trabalho)')
        else: print('  OS DOIS EM 1: A PEÇA SE PERDE (e o material)')
        return
    f=cat_de(T,cdm,atual if reforja else None)
    if reforja and f<=atual:
        print(f'  RESULTADO: não sobe (precisava de {CD[atual+1]-cdm}). A peça fica {NOME[atual]}, inteira; o material novo se gasta.')
        if A[0]==1 or B[0]==1: print('  um 1 natural: a peça RACHA (precisa de conserto antes de nova reforja)')
        return
    if f<0: print('  RESULTADO: abaixo de 15: MATERIAL PERDIDO'); return
    notas=[]; extra=0; marav=0; tw=sum(x==20 for x in A+B); extra+=tw
    if A[0]==20 and B[0]==20:
        r=d(6)
        if r<=3 and f<7: f+=1; notas.append(f'OBRA-PRIMA (os dois abriram em 20) 1d6 [{r}] → sobe a {NOME[f]}')
        else: extra+=1; notas.append(f'OBRA-PRIMA 1d6 [{r}] → +1 efeito')
    if tw>=3: marav+=1; notas.append(f'{tw} VINTES: MARAVILHA')
    if tw>=5: marav+=1; notas.append('LENDA: a peça acorda (nome próprio; o mundo fica sabendo)')
    if f<7 and CD[f+1]-cdm-T<=3: extra+=1; notas.append(f'QUASE: ficou a {CD[f+1]-cdm-T} da CD {NOME[f+1]} → +1 efeito (a peça quis subir)')
    ones=[x for x in (A[0],B[0]) if x==1]
    for _ in ones:
        r=d(6)
        if r==1 and not reforja: notas.append('UM 1: complicação [1] → A PEÇA SE PERDE'); print('\n'.join('  '+n for n in notas)); return
        if r<=3 and f>max(atual,0): f-=1; notas.append(f'UM 1: complicação [{r}] → cai a {NOME[f]}')
        else: notas.append(f'UM 1: complicação [{r}] → menor (o tempo dobra ou a ferramenta perde 1)')
    for n in notas: print('  '+n)
    if reforja and f<=atual: print(f'  RESULTADO: a complicação segurou a peça em {NOME[atual]}.'); return
    xp = XP[f]-(XP[atual] if reforja else 0)
    print(f'  RESULTADO: {nomep} — {NOME[f].upper()} · XP {xp}' + (f' (diferença {NOME[atual]} → {NOME[f]}; mantém todos os efeitos e o encantamento)' if reforja else ''))
    if (opt(a,'quem','') or '').startswith('ferir') and xp>0: print(f'  → lançar: python3 ficha.py xp {xp} "{nomep} ({NOME[f]})"   (ajudantes: 1/4 cada, no cresce.py)')
    npec=tw+len(ones)+(1 if d(10)==1 else 0)
    efeitos(nomep,tipo,f,extra,marav,npec,de=atual if reforja else 0)

def encantar(a):
    feit,circ,cat=a[1],int(a[2]),CAT.index(norm(a[3]))
    L,s,cdm,x19,alma,fort=valores(a,'encantar')
    lim=CD[cat]+CIRC_AJ.get(circ,0)-cdm
    print(f'ENCANTAMENTO "{feit}" ({circ}º círculo) numa peça {NOME[cat]} · LIMIAR {lim} (CD {CD[cat]} {CIRC_AJ.get(circ,0):+d} pelo círculo{f" −{cdm}" if cdm else ""})')
    mostra(L,s,cdm)
    A,B,T,log,rev=rola(s,alma,fort,x19,lambda T,A,B: T<lim or A[0]==1 or B[0]==1)
    print(f'  dados finais: {A} + {B} → TOTAL {T}')
    for l in log: print('  '+l)
    if rev: print(f'  Revés +{rev}')
    if A[0]==1 and B[0]==1: print('  OS DOIS EM 1: o condutor se perde E A PEÇA RACHA (conserto)'); return
    g='INTEIRO' if T>=lim else 'UMA VEZ MAIS FRACO' if T>=lim-10 else 'DUAS VEZES MAIS FRACO' if T>=lim-20 else 'FALHA: o condutor se perde'
    tw=sum(x==20 for x in A+B)
    print(f'  RESULTADO: {g}'+(f' · {tw} vinte(s): o feitiço sai mais forte (+1 uso por dia ou +2d6, pela ficção)' if tw and 'FALHA' not in g else ''))
    if (A[0]==1 or B[0]==1) and 'FALHA' not in g:
        r=d(6); print(f'  um 1 natural: complicação 1d6 [{r}] → '+('a peça perde 1 de durabilidade' if r>1 else 'o condutor se perde (não pega)'))
    if 'FALHA' not in g: print(f'  XP: {XP[cat]}')
    if 'FALHA' not in g and (opt(a,'quem','') or '').startswith('ferir'): print(f'  → lançar: python3 ficha.py xp {XP[cat]} "encanto {feit} ({NOME[cat]})"')
    print('  (REFORÇO: um encantamento mais fraco pode ser refeito 1x por semana com meio condutor; se não chegar ao inteiro, fica como está)')

def conserto(a):
    nomep,cat=a[1],CAT.index(norm(a[2]))
    L,s,cdm,x19,alma,fort=valores(a,'conserto'); lim=max(CD[cat]-20,10)-cdm
    print(f'CONSERTO "{nomep}" ({NOME[cat]}) · CD {lim} (CD da categoria − 20) · material 1/10 da massa'); mostra(L,s,cdm)
    A,B,T,log,rev=rola(s,alma,fort,x19,lambda T,A,B: T<lim or A[0]==1)
    print(f'  dados finais: {A} + {B} → TOTAL {T}')
    for l in log: print('  '+l)
    if A[0]==1 and B[0]==1: print('  OS DOIS EM 1: o conserto tira o efeito mais fraco da peça'); return
    if T>=lim+20: print('  RESULTADO: CONSERTADA e MELHOR: ganha uma marca do ferreiro (+1 de durabilidade ou um detalhe)')
    elif T>=lim: print('  RESULTADO: CONSERTADA, inteira como antes')
    else: print('  RESULTADO: não fechou; tentar de novo amanhã (o material gasto fica)')
    print('  XP: 1/4 do XP da categoria' if T>=lim else '')

def sim(a, N=100000):
    import random
    L,s,cdm,x19,_,_=valores(a,'obra'); mostra(L,s,cdm)
    def dd():
        t=0
        while True:
            r=random.randint(1,20); t+=r
            if r!=20: return t
    c=[0]*8
    for _ in range(N):
        T=s+dd()+dd()
        for i in range(8):
            if T>=CD[i]-cdm: c[i]+=1
    print('  chance de chegar a (simulação, sem valor de jogo): '+' · '.join(f'{NOME[i]} {100*c[i]/N:.1f}%' for i in range(8)))

def main():
    a=sys.argv[1:]
    if not a: sys.exit(__doc__)
    if a[0]=='fichas':
        for k,f in FICHAS.items():
            L,s,*_=valores(['quem='+k]+(['cond=comum'] if k.endswith('enc') else []),'encantar' if k.endswith('enc') else 'obra'); print(f'[{k}] {f["desc"]}' + (' · lida de ficha.json' if k in REAL and ficha_viva() else '')); mostra(L,s,0)
        return
    {'obra':lambda: obra(a),'reforja':lambda: obra(a,True),'encantar':lambda: encantar(a),'conserto':lambda: conserto(a),'sim':lambda: sim(a)}[a[0]]()
if __name__=='__main__': main()
