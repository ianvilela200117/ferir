#!/usr/bin/env python3
"""O MUNDO VIVO (regra da casa, Dia 201, pedido do jogador: "cadê os Lendários, os monstros grandes, os bandos, as tramas,
a espionagem? cria um sistema para eu não ter de lembrar e para o Mestre ter ideias sozinho").
Estado em mundo_vivo.json. Roda sozinho no tick.py (dia e semana). Tudo por dado (secrets); nada escolhido antes.

  python3 mundo_vivo.py dia N        1 Lendário pode agir (1-7 no d20) · 1 trama mexe · contra-espionagem contra infiltrados · 3 FAÍSCAS
  python3 mundo_vivo.py semana N     os 8 Lendários (relógios, choques entre rivais) · monstros grandes · povos-monstro · tramas (todas)
                                     · espionagem (relatório de cada célula) e redes inimigas · 1 trama nova · 5 FAÍSCAS
  python3 mundo_vivo.py faisca N     ideias do Mestre, juntando o que já existe (o Mestre usa pelo menos 1 por resposta)
  python3 mundo_vivo.py ver          resumo
  python3 mundo_vivo.py espiao CIDADE  operação da esquadra numa cidade agora (1 rolagem)
A NOTÍCIA de tudo o que acontece longe chega pela regra do mundo.py (Dia 204, d20: 1-4 hoje · 5-10 em 1d3 · 11-17 em 1d6 · 18-20 só se alguém for atrás).
"""
import sys, json, os, secrets
AQUI=os.path.dirname(os.path.abspath(__file__)); ARQ=os.path.join(AQUI,'mundo_vivo.json')
d=lambda n: secrets.randbelow(n)+1
pick=lambda xs: xs[secrets.randbelow(len(xs))]
def ex():
    ch=[d(20)]
    while ch[-1]==20: ch.append(d(20))
    return ch
def chega(dia):   # Dia 204: d20
    r=d(20)
    if r<=4: return f'd20 [{r}] chega hoje'
    if r<=10: x=d(3); return f'd20 [{r}] chega no dia {dia+x}'
    if r<=17: x=d(6); return f'd20 [{r}] chega no dia {dia+x}'
    return f'd20 [{r}] não chega sozinha (só a espionagem ou quem for atrás)'

ACAO_LENDARIO=["um gesto público grande (discurso, decreto, desafio) que todo mundo comenta","compra, toma ou destrói algo de valor ligado à Obra",
 "recruta: gente, uma facção ou um monstro passa para o lado dele","ataca ou sabota a obra do RIVAL lendário","viaja: aparece num lugar onde não era esperado",
 "manda um enviado (pode vir a Ireviel se a Obra tocar a casa: 1-3 no d20)","um segredo dele vaza (boato ou espionagem)","sofre um revés (ferida, perda, traição de um próximo)",
 "faz uma OBRA ligada à frente (uma peça, uma lei, uma batalha, um ritual)","procura um ferreiro, um mago ou um objeto (1-3 no d20: procura Ferir ou a Matriz)",
 "o desejo dele pesa: faz algo pessoal, fora da Obra (amor, vingança, saudade)",
 "o MEDO dele aparece: foge, se esconde ou faz algo desesperado","oferece um acordo a um rival (paz, casamento, troca)","perde uma peça ou um aliado para alguém",
 "funda ou compra algo (uma casa, uma ordem, uma cidade pequena)","um discípulo ou herdeiro dele aparece no mundo","desafia alguém em público (duelo, debate, prova)",
 "a ambição dele avança fora da Obra (um passo no que ele quer para si)","manda caçar alguém (um nome, uma peça, um monstro)",
 "SURPRESA: gerador de novidade ligado a ele"]
ACAO_MONSTRO=["dorme / quieto","caça perto do habitat (gado ou gente some)","migra 1 região (rola para onde)","ataca uma aldeia ou caravana (notícia certa)",
 "cria: aparecem crias (1d6) perto do habitat","marca território: o sinal dele aparece mais perto de gente","é caçado por alguém (uma companhia, um Lendário, um culto)",
 "come algo que o muda (sobe 1d6 níveis)","alguém o viu e sobreviveu: um rumor exato (fraqueza, lugar ou drop)",
 "dorme fundo (some por 1d4 semanas)","briga com outro monstro grande (um sai ferido)","deixa cair um drop onde gente acha (material à venda)","um culto ou bando passa a adorá-lo",
 "fica ferido (alguém o caçou e quase conseguiu)","muda de comportamento (fica mais manso ou mais faminto)","persegue uma caravana ou barca por dias",
 "destrói uma ponte, estrada ou mina (o comércio sente)","atrai monstros menores ao redor (o lugar fica perigoso)","aparece de dia, à vista de muitos (pânico e notícia certa)","SURPRESA: gerador de novidade ligado a ele"]
ACAO_POVO=["fica no covil (rotina)","assalta uma estrada ou aldeia (roubo, mortos)","guerra contra outro povo ou bicho","negocia: vende ou troca com humanos (oportunidade)",
 "cresce: +1d6×10 de número; o chefe ganha prestígio","o chefe é desafiado (1d6: 1-3 cai, novo chefe)","acha algo nas ruínas ou minas (material, núcleo, relíquia)",
 "um Lendário, culto ou facção os contrata ou escraviza","descem para perto das cidades (fome, frio, medo de algo maior)",
 "fazem um ritual (o xamã ou o sacerdote ganha poder)","racham em dois bandos (um sai com outro chefe)","pegam prisioneiros humanos (resgate ou escravos)",
 "mandam um emissário a uma cidade (paz, troca, ameaça)","são caçados por uma companhia (perdem 1d6×5)","acham um líder de fora (um humano, um monstro grande)",
 "atacam outro povo-monstro (guerra de bandos)","constroem algo (forte, ponte, templo)","um deles vira herói ou traidor (rumor com nome)","pedem armas ou abrigo a uma cidade humana (oportunidade ou perigo)","SURPRESA: gerador de novidade ligado a eles"]
TRAMA_TIPO=['ÓDIO','AMOR','RESSENTIMENTO','DÍVIDA','RIVALIDADE','INVEJA','DESEJO SECRETO','LEALDADE CEGA','MEDO','TRAIÇÃO PENDENTE','VINGANÇA JURADA','PAIXÃO PROIBIDA']
TRAMA_CAUSA=['uma morte antiga','um amor recusado','uma promessa quebrada','ouro devido','uma humilhação pública','um segredo descoberto','um filho ou uma filha',
 'um cargo ou título','uma peça (arma, joia, bigorna)','uma terra ou casa','uma fé diferente','um salvamento que não se pagou']
FAISCA_VERBO=['quer casar com','quer matar','deve a vida a','rouba de','descobre o segredo de','foge de','oferece aliança a','vai trair','ama em segredo','inveja',
 'procura','vende algo a','pede ajuda a','acusa em público','encomenda uma peça para','esconde um filho de','sonha com','chantageia','salva','desafia para duelo']
FAISCA_POR=['a Matriz','vaduar','um núcleo de monstro','uma receita perdida','um herdeiro dos Steunn','uma dívida antiga','um mapa','a coberta do mundo','sal','um título',
 'a Fornalha que Não Apaga','uma criança','uma terra além do mapa','um feitiço proibido','uma peça Lendária roubada','o perdão','vingança','fome','uma profecia','dinheiro da Liga']
POVOS=[('goblins','tocas e minas velhas'),('hobgoblins','fortes caídos'),('orcs','montanhas e passos'),('kobolds','galerias fundas'),('gnolls','planícies e estradas'),
 ('homens-lagarto','brejos e Delta'),('trolls','pontes e gargantas'),('ogros','florestas e colinas'),('homens-rato','esgotos e cisternas das cidades'),
 ('harpias','penhascos da costa'),('homens-peixe','costa e lodaçais'),('gigantes de pedra','picos e pedreiras')]
CHEFE=['chefe-guerreiro (AÇO)','xamã (MAGIA: Sangue ou Osso)','bruxa (MAGIA: Mente ou Sombra)','rei-bandido (OURO)','sacerdote de um deus morto (FÉ)','montador de fera (AÇO/RAIZ)']
REL_POVO=['GUERRA aberta com os humanos','SAQUEIA quem passa','DESCONFIA (fica longe)','COMERCIA (troca peles e minério por ferro)','VASSALO de alguém (rolar quem)','ALIANÇA SECRETA com uma facção humana']
PLANO_POVO=['tomar um forte ou mina','achar um novo covil longe de algo que os caça','vingar um chefe morto por humanos','ter armas de ferro boas (procuram ferreiro)',
 'unir as tribos sob um só chefe','servir a um Lendário ou monstro grande','fugir do frio que desce das Fundas','acordar algo que dorme sob o covil','ser aceitos numa cidade','juntar ouro para um resgate']
FRENTES=['combate','ofício','influência','magia','ameaça','fé']
OBRAS=['unificar os clãs do norte sob uma coroa','forjar uma arma que muda a guerra','fundar uma fé nova','quebrar a Liga de Marasar','abrir uma passagem para o que dorme',
 'acabar com a magia','fechar a coberta do mundo de novo','criar uma escola de magia sem limites','comprar todas as dívidas da costa','domar um monstro Mítico',
 'achar as três ferramentas dos reis','ressuscitar um morto amado']

def load(): return json.load(open(ARQ))
def save(M): json.dump(M,open(ARQ,'w'),ensure_ascii=False,indent=1)
def nomes_canon(M):
    xs=[l['nome'] for l in M['lendarios'] if l['estado']!='morto']+[p['chefe'] for p in M['povos']]+M.get('gente',[])
    return xs

def faisca(M,n,dia):
    out=[]
    for _ in range(n):
        a=pick(nomes_canon(M)); b=pick([x for x in nomes_canon(M)+['Ferir','a casa da fundição'] if x!=a])
        out.append(f'FAÍSCA: {a} {pick(FAISCA_VERBO)} {b}, por causa de {pick(FAISCA_POR)}')
    return out

def lendario_age(l,dia,M,forcado=False):
    r=d(20); txt=ACAO_LENDARIO[r-1]; extra=''
    if r in (6,10): extra=f' · 1d20 [{d(20)}]'
    l['log'].append(f'{dia}: [{r}] {txt}')
    return f"  {l['nome']} ({l['frente']}, {l['regiao']}) d20 [{r}] {txt}{extra} · notícia {chega(dia)}"

def semana(dia):
    M=load(); print(f'O MUNDO VIVO — semana (Dia {dia})')
    print(' OS LENDÁRIOS:')
    avan=[]
    for l in M['lendarios']:
        if l['estado']=='morto': continue
        l['prox']=l.get('prox',dia)
        if dia>=l['prox'] and l['relogio'][0]<l['relogio'][1]:
            l['relogio'][0]+=1; l['prox']=dia+l['ritmo']; avan.append(l)
            done=' (chegou ao fim: confere depois dos choques)' if l['relogio'][0]>=l['relogio'][1] else ''
            print(f"  {l['nome']} relógio {l['relogio'][0]}/{l['relogio'][1]} ({l['obra']}){done}")
            print(lendario_age(l,dia,M))
        else: print(f"  {l['nome']} {l['relogio'][0]}/{l['relogio'][1]} (próximo passo no dia {l['prox']})")
    for l in avan:
        rv=next((x for x in M['lendarios'] if x['nome']==l.get('rival') and x['estado']!='morto'),None)
        if rv and rv in avan:
            a=sum(ex())+l['regua']; b=sum(ex())+rv['regua']; w,lo=(l,rv) if a>=b else (rv,l)
            lo['relogio'][0]=max(0,lo['relogio'][0]-2)
            print(f"  CHOQUE DE RIVAIS: {l['nome']} {a} × {rv['nome']} {b} → {lo['nome']} recua 2 ({lo['relogio'][0]}/8)")
    for l in avan:   # auditoria 203: a OBRA só se completa DEPOIS dos choques
        if l['relogio'][0]>=l['relogio'][1]: print(f"  {l['nome']}: OBRA COMPLETA ({l['obra']}): muda o mundo (Registro), e começa outra obra")
    print(' MONSTROS GRANDES (Épico para cima):')
    for m in M['monstros']:
        if m['estado'] in ('morto',): continue
        if m['estado']=='dormindo':
            r=d(20); print(f"  {m['nome']} ({m['cat']}, dormindo, {m['regiao']}) d20 [{r}] " + ('ACORDA' if r==20 else 'dorme'));
            if r==20: m['estado']='ativo'
            continue
        r=d(20); print(f"  {m['nome']} ({m['cat']} {m['nivel']}, {m['regiao']}) d20 [{r}] {ACAO_MONSTRO[r-1]} · notícia {chega(dia)}")
        if r==3: m['regiao']=pick(REGIOES); print(f"     migra para: {m['regiao']}")
        if r==8: x=d(6); m['nivel']+=x; print(f'     +{x} níveis → {m["nivel"]}')
    print(' POVOS-MONSTRO (bandos):')
    for p in M['povos']:
        r=d(20); print(f"  {p['nome']} ({p['povo']}, {p['numero']}, {p['regiao']}; chefe {p['chefe']} nível {p['chefe_nivel']}) d20 [{r}] {ACAO_POVO[r-1]} · plano {p['relogio'][0]}/6 · notícia {chega(dia)}")
        if r in (2,5,7,9) and p['relogio'][0]<6: p['relogio'][0]+=1
        if r==5: p['numero']+=d(6)*10
        if r==6:
            q=d(6)
            if q<=3: from nomes import nome; p['chefe']=nome('aspera'); p['chefe_nivel']=p['chefe_nivel']+d(10)-3; print(f"     [{q}] o chefe CAI: novo chefe {p['chefe']} ({p['chefe_nivel']})")
            else: print(f'     [{q}] o chefe aguenta')
    print(' TRAMAS (amor, ódio, ressentimento):')
    for t in M['tramas']:
        if t['estado']!='viva': continue
        r=d(20); mv=-1 if r<=3 else 2 if r==20 else 1 if r>=14 else 0; t['int']=max(0,min(4,t['int']+mv))   # Dia 204: d20 (1-3 esfria · 14-19 esquenta · 20 esquenta 2)
        s=f"  {t['a']} → {t['b']}: {t['tipo']} ({t['causa']}) d20 [{r}] " + ('esfria' if mv<0 else 'ESQUENTA MUITO (um gesto grande)' if mv==2 else 'ESQUENTA' if mv>0 else 'segue') + f" · {t['int']}/4"
        if t['int']>=4: s+=' → EXPLODE: vira cena ou evento esta semana (o Mestre mostra)'; t['estado']='explodiu'
        if t['int']==0: s+=' → apagou'; t['estado']='apagou'
        print(s)
    nt=nova_trama(M,dia); print('  TRAMA NOVA: '+nt)
    print(' ESPIONAGEM DA CASA:')
    espionagem_semana(M,dia)
    print(' FAÍSCAS DO MESTRE (usar pelo menos 1):')
    for f in faisca(M,5,dia): print('  '+f)
    save(M)

def nova_trama(M,dia):
    xs=nomes_canon(M)+['Ferir','a casa da fundição']; a=pick(xs); b=pick([x for x in xs if x!=a])
    t={'a':a,'b':b,'tipo':pick(TRAMA_TIPO),'causa':pick(TRAMA_CAUSA),'int':d(2),'desde':dia,'estado':'viva'}
    M['tramas'].append(t); return f"{a} → {b}: {t['tipo']} ({t['causa']}), {t['int']}/4"

V_TAM={'aldeia':0,'vila':2,'cidade':5,'capital':10}
V_ORD={'nenhuma':0,'fraca':2,'guarda':5,'guarda forte':8}
V_RIQ={'pobre':0,'média':2,'rica':4}
def cd_cidade(M,nome):
    """Dia 204 (pedido do jogador): a CD da cidade é SOMA DE VALORES, como na forja. Cidade forte e organizada = difícil; cidade em crise = fácil.
    CD = 20 + tamanho + ordem + riqueza + (rede inimiga local ÷ 4) − problemas − amigos da casa ali."""
    c=M['espionagem']['celulas'][nome]; e=c.get('estado')
    if not e: return c['cd'],[]
    L=[('base',20),(f"tamanho ({e['tamanho']})",V_TAM[e['tamanho']]),(f"ordem ({e['ordem']})",V_ORD[e['ordem']]),(f"riqueza ({e['riqueza']})",V_RIQ[e['riqueza']])]
    if e.get('rede'): L.append((f"rede inimiga ({e['rede'][0]})",e['rede'][1]//4))
    for p,v in e.get('problemas',[]): L.append((p,-v))
    for a,v in e.get('amigos',[]): L.append((f'amigo da casa: {a}',-v))
    cd=sum(v for _,v in L); c['cd']=cd; return cd,L

def espionagem_semana(M,dia):
    E=M['espionagem']
    for c in E['celulas']:
        cd,L=cd_cidade(M,c)
        if L: print(f"  CD de {c} = {cd}: "+' · '.join(f'{r} {v:+d}' for r,v in L))
    for c,cel in E['celulas'].items():
        if cel['forca']<=0: print(f'  {c}: célula caída'); continue
        ch=ex(); tot=sum(ch)+E['chefe_bonus']+2*cel['forca']; cd=cel['cd']; mg=tot-cd
        if ch[0]==1 or mg<=-10: g='FALHA FEIA: um agente é pego; a célula perde 1; quem pegou sabe que a casa espiona'; cel['forca']-=1
        elif mg<0: g='nada de novo'
        elif mg<10: g='UM RUMOR VERDADEIRO da região (o Mestre tira do Envelope ou do mundo)'
        elif mg<20: g='UM SEGREDO (plano de facção, Lendário ou vilão da região)'
        else: g='SEGREDO GRANDE + uma oportunidade'
        if mg>=0 and d(6)==6 and cel['forca']<3: cel['forca']+=1; g+=' · a célula cresce (+1)'
        print(f"  {c} (força {cel['forca']}): {ch} + {E['chefe_bonus']} + {2*cel['forca']} = {tot} vs {cd} → {g}")
    print('  REDES INIMIGAS tentando entrar em Ireviel:')
    for r in M['redes_inimigas']:
        a=ex(); b=ex(); ta=sum(a)+r['forca']; tb=sum(b)+E['contra_bonus']
        g='ENTRA e descobre algo da casa (d6 da lista de segredos)' if ta>tb else 'barrada'
        if tb-ta>=10: g='PEGA: um agente deles cai na mão da contra-espionagem'
        print(f"   {r['nome']}: {a}+{r['forca']} = {ta} × contra {b}+{E['contra_bonus']} = {tb} → {g}" + (f" · segredo [{d(6)}]" if ta>tb else ''))
    if d(6)>=5 and E['contra_bonus']<E.get('contra_max',30): E['contra_bonus']+=1; print(f"  a contra-espionagem treina: +1 → {E['contra_bonus']}")

def dia(n):
    M=load(); print(f'O MUNDO VIVO — Dia {n}')
    r=d(20)
    if r<=7:
        vivos=[l for l in M['lendarios'] if l['estado']!='morto']; l=pick(vivos); print(f'  um Lendário age (d20 [{r}]):'); print(lendario_age(l,n,M))
    else: print(f'  Lendários: d20 [{r}] quietos hoje')
    vivas=[t for t in M['tramas'] if t['estado']=='viva']
    if vivas:
        t=pick(vivas); q=d(20); print(f"  trama do dia: {t['a']} → {t['b']} ({t['tipo']}) d20 [{q}] " + ('UM GESTO GRANDE em cena hoje' if q==20 else 'um gesto dela aparece em cena hoje' if q>=14 else 'nada visível'))
    E=M['espionagem']
    for i in M.get('infiltrados',[]):
        if i.get('estado')!='solto': continue
        a=ex(); b=ex(); ti=sum(a)+i['furt']; tc=sum(b)+E['contra_bonus']; mg=tc-ti
        g='IDENTIFICADO' if mg>=10 else 'PISTA (alguém estranho foi notado)' if mg>=0 else 'não visto'
        print(f"  CONTRA-ESPIONAGEM (oculto) vs {i['nome']}: contra {b}+{E['contra_bonus']} = {tc} × {a}+{i['furt']} = {ti} → {g}")
        if mg>=10: i['estado']='identificado'
    for f in faisca(M,3,n): print('  '+f)
    save(M)

def espiao(cidade):
    M=load(); E=M['espionagem']; cel=E['celulas'][cidade]; cd,L=cd_cidade(M,cidade)
    if L: print(f"  CD de {cidade} = {cd}: "+' · '.join(f'{r} {v:+d}' for r,v in L))
    ch=ex(); tot=sum(ch)+E['chefe_bonus']+2*cel['forca']
    print(f"OPERAÇÃO em {cidade}: {ch} + {E['chefe_bonus']} + {2*cel['forca']} = {tot} vs {cel['cd']} (margem {tot-cel['cd']:+d})")

REGIOES=['Ireviel e o rio','Levis','Lumade','Marasar','Farenta','Gogrunn','Kremir','Telosus','Shizess','o Delta','Mordun','as Fundas do Norte',
 'a Mata de Elais','o brejo do oeste','o sul da areia','as Montanhas de Fogo','os Picos Brancos','a costa','Yaelane','Steunn','Zisrir']

if __name__=='__main__':
    a=sys.argv[1:]
    if not a: sys.exit(__doc__)
    if a[0]=='semana': semana(int(a[1]))
    elif a[0]=='dia': dia(int(a[1]))
    elif a[0]=='faisca':
        M=load(); [print(f) for f in faisca(M,int(a[1]) if len(a)>1 else 3,0)]
    elif a[0]=='espiao': espiao(a[1])
    elif a[0]=='ver':
        M=load()
        for l in M['lendarios']: print('L', l['nome'], l['estado'], l['relogio'], l['obra'])
        for m in M['monstros']: print('M', m['nome'], m['cat'], m['estado'], m['regiao'])
        for p in M['povos']: print('P', p['nome'], p['povo'], p['regiao'], p['relogio'])
        for t in M['tramas']: print('T', t['a'],'→',t['b'],t['tipo'],t['int'],t['estado'])
        print('E', M['espionagem'])
