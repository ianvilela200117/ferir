#!/usr/bin/env python3
"""A SEMANA DOS NPCs (regra da casa, Dia 200): todo NPC do livro (npcs.json) com ocupação vive a semana dele.
Rola no Tick semanal, ANTES do cresce.py. Cada um, d10 (+1 se nível 50+, +1 se a ocupação é missão de fora):
 1  PROBLEMA: um revés na ocupação (o Mestre liga à ficção; surpresa ruim) · 0 XP
 2-3 ROTINA: a semana passa · 0 XP
 4-7 PASSO: a ocupação anda um passo · +500 XP
 8-9 MISSÃO OU FEITO: cumpre algo que conta (missão da casa, encomenda, caçada pequena) · +1.000 XP e ouro (nível × 1d6 × 5)
 10+ SURPRESA: o gerador decide (novidade ligada a ele) · +500 XP
Presos, longe sem notícia e Lendários não rolam aqui (os Lendários andam pelo relógio).
O XP vai direto para o livro (cresce.py); o ouro é do NPC (não da casa), salvo se a ocupação é da casa: aí vai para o livro da Nouliel.
Uso: python3 semana_npc.py DIA

MOTOR 6 (Dia 379): as regras são as mesmas. Mudou só a máquina: o XP é lançado direto no npcs.json (antes abria um
processo por NPC, ~90 por semana), a gravação é atômica, e o tick recebe um RESUMO (quem teve PROBLEMA, MISSÃO ou
SURPRESA; os de rotina e de passo viram contagem). A lista inteira continua saindo aqui e no tick_N.txt.
"""
import sys, json, os, secrets
d=lambda n: secrets.randbelow(n)+1
P=os.path.dirname(os.path.abspath(__file__)); F=os.path.join(P,'npcs.json')
RES=os.environ.get('MOTOR_RESUMO')=='1'
db=json.load(open(F,encoding='utf-8'))
dia=sys.argv[1] if len(sys.argv)>1 else '?'
conta={'rotina':0,'PASSO':0}; destaque=[]; sem_nivel=[]
# MOTOR 6.1 (camada detalhe_npc): o PROBLEMA e o FEITO já saem com o que foi, para o Mestre ligar à ficção
PROB=['adoece ou se fere no ofício','dívida ou aperto de dinheiro','briga com um colega ou vizinho','erro no trabalho (perde material ou prazo)','ferramenta, carga ou animal perdido','coração (ciúme, recusa, saudade)','um rival o passa para trás','problema de família (doença, morte, herança)','encrenca com a guarda ou com a lei','é roubado ou enganado','um segredo dele quase vem à tona','cansaço fundo: fala em largar o posto']
FEITO=['cumpre a tarefa com folga e ganha nome','acha algo de valor no caminho','faz um contato novo e útil','salva alguém ou evita um desastre pequeno','fecha um bom negócio','ensina ou aprende um pedaço de ofício','resolve uma pendência velha','traz uma informação que a casa não tinha']
try:
    DET=bool(json.load(open(os.path.join(P,'motor.json'),encoding='utf-8')).get('camadas',{}).get('detalhe_npc',True))
except Exception: DET=True
for n,v in db.items():
    if 'MORT' in str(v.get('estado') or '').upper(): continue   # auditoria 203: morto não vive a semana (441: sem olhar maiúscula; o Pelaccino e o Quthemnus passavam)
    oc=v.get('ocupacao','')
    if not oc or 'presa' in oc.lower() or 'preso' in oc.lower() or v.get('lendario'): continue
    if not v.get('nivel'):   # MOTOR 6: ficha sem nível derrubava o script no meio (desde ~336, os 8 últimos NPCs do livro não viviam a semana)
        print(f'{n}: SEM NÍVEL, não rola (gerar a ficha quando entrar em cena: npc.py nivel {n} N) · ({oc})'); sem_nivel.append(n); continue
    r=d(10); mod=(1 if v['nivel']>=50 else 0)+(1 if 'fora' in oc else 0); t=r+mod
    if r==1: res,xp,ouro='PROBLEMA',0,0
    elif t<=3: res,xp,ouro='rotina',0,0
    elif t<=7: res,xp,ouro='PASSO',500,0
    elif t<=9: res,xp,ouro='MISSÃO/FEITO',1000,v['nivel']*d(6)*5
    else: res,xp,ouro='SURPRESA (gerador)',500,0
    det=''
    if DET and res=='PROBLEMA': q=d(12); det=f' · O QUÊ d12 [{q}]: {PROB[q-1]}'
    elif DET and res=='MISSÃO/FEITO': q=d(8); det=f' · O QUÊ d8 [{q}]: {FEITO[q-1]}'
    linha=f'{n}: d10 [{r}]{"+"+str(mod) if mod else ""} → {res}{det}' + (f' · +{xp} XP' if xp else '') + (f' · ouro {ouro}' if ouro else '') + f' · ({oc})'
    print(linha)
    if xp:
        v['xp']+=xp; v.setdefault('log',[]).append(f'+{xp} Tick {dia}: {res} ({oc})')
    if res in conta: conta[res]+=1
    else: destaque.append(f'{n}: {res}{det}' + (f' (ouro {ouro})' if ouro else '') + f' — {oc[:70]}')
tmp=F+'.tmp'; json.dump(db,open(tmp,'w',encoding='utf-8'),ensure_ascii=False,indent=1); os.replace(tmp,F)
if RES:
    for l in destaque: print('::R:: '+l)
    print(f"::R:: (os outros: {conta['PASSO']} deram um PASSO, {conta['rotina']} ficaram na rotina)")
    if sem_nivel: print('::R:: ⚠ SEM NÍVEL, fora da semana: '+', '.join(sem_nivel)+' (npc.py nivel NOME N)')
