#!/usr/bin/env python3
"""O MUNDO CRESCE (XVI.4 / XXIII.22): livro de XP e nível dos NPCs.
Custo do nível: 100 × nível atual (para passar de N a N+1). No máximo 1 nível por Tick semanal (Lendários: 1 por mês).
Uso:
  python3 cresce.py ver [N]                     mostra todos (ou os N de nível mais alto)
  python3 cresce.py xp NOME QTD "motivo"        soma XP (fica guardado até o Tick)
  python3 cresce.py xp "A,B,C" QTD "motivo"     o mesmo XP para vários de uma vez (uma luta, uma missão)
  python3 cresce.py tick DIA                    aplica: quem tem XP para subir, sobe 1 nível (o resto fica)
Tabela (XVI.4): passo de agenda/ambição 500 · agenda ou ambição inteira 1.000 · conflito sério 500 (ou nível do inimigo × 10 se lutou)
· obra/descoberta/feito pela Parte IX (Comum 5 · Incomum 20 · Raro 80 · Épico 300 · Único 800 · Lendário 2.500; feito menor 500, grande 1.000; missão pela letra).

MOTOR 6 (Dia 379): o nome pode vir sem acento, em minúscula ou pela metade (antes um nome errado derrubava o script);
vários nomes numa chamada; a regra "Lendários: 1 nível por mês", que estava escrita mas nunca rodava (o Lendário
não subia nunca), agora roda: 28 dias entre uma subida e outra; gravação atômica.
EQUILÍBRIO (Dia 379): com XP guardado para 4 níveis ou mais, sobe 2 por semana; para 10 ou mais, sobe 3. Lendários, 1 por mês.
"""
import sys, json, os, difflib, unicodedata
F=os.path.join(os.path.dirname(os.path.abspath(__file__)),'npcs.json')
db=json.load(open(F,encoding='utf-8'))
RES=os.environ.get('MOTOR_RESUMO')=='1'
def save():
    tmp=F+'.tmp'; json.dump(db,open(tmp,'w',encoding='utf-8'),ensure_ascii=False,indent=1); os.replace(tmp,F)
def liso(s): return ''.join(c for c in unicodedata.normalize('NFD',s) if unicodedata.category(c)!='Mn').lower()
def acha(nome):
    if nome in db: return nome
    n=liso(nome)
    for teste in (lambda k: liso(k)==n, lambda k: liso(k).startswith(n), lambda k: n in liso(k)):
        xs=[k for k in db if teste(k)]
        if len(xs)==1: return xs[0]
        if len(xs)>1: sys.exit(f'"{nome}" serve para mais de um: {", ".join(xs[:8])}. Diga o nome inteiro. Nada foi lançado.')
    sug=difflib.get_close_matches(nome,list(db),n=5,cutoff=0.6)
    sys.exit(f'NPC não achado: "{nome}".'+(f' Parecidos: {", ".join(sug)}.' if sug else '')+' Nada foi lançado. (Ficha nova: python3 npc.py novo NOME NIVEL "classe" "ocupação")')
a=sys.argv[1:]
if not a or a[0]=='ver':
    lim=int(a[1]) if len(a)>1 and a[1].isdigit() else None
    for n,v in sorted(db.items(), key=lambda x:-(x[1].get('nivel') or 0))[:lim]:
        print(f"{n:10s} nível {(v.get('nivel') or 0):3d} · XP {v.get('xp',0):6d}/{100*(v.get('nivel') or 0):6d}" + (" (Lendário: 1/mês)" if v.get('lendario') else '') + (' · MORTO' if 'MORTO' in v.get('estado','') else ''))
elif a[0]=='xp':
    if len(a)<3: sys.exit('uso: cresce.py xp NOME QTD "motivo"')
    nomes=[acha(x.strip()) for x in a[1].split(',') if x.strip()]; q=int(a[2]); m=a[3] if len(a)>3 else ''
    for n in nomes:
        db[n]['xp']+=q; db[n].setdefault('log',[]).append(f"+{q} {m}"); print(f"{n}: +{q} ({m}) → {db[n]['xp']}/{100*db[n]['nivel']}")
    save()
elif a[0]=='tick':
    dia=a[1]; ndia=int(dia) if dia.isdigit() else 0; sobem=[]; subidas=[]
    for n,v in db.items():
        if 'MORTO' in v.get('estado',''): continue   # auditoria 203
        if not v.get('nivel'): continue   # Dia 245: sem ficha (nível 0) não sobe sozinho; gerar o nível quando entrar em cena
        custo=100*v['nivel']
        if v['xp']<custo: continue
        if v.get('lendario') and ndia and ndia-v.get('ultima_subida',0)<28: continue   # MOTOR 6: Lendários, 1 nível por mês
        # Dia 379 (equilíbrio): quem tem XP guardado para MUITOS níveis sobe mais de 1 por semana (até 3). Antes a Tilde, com 105 mil
        # de XP no nível 32, levaria 8 meses na fila. Lendários seguem em 1 por mês.
        lim=1 if v.get('lendario') else 3 if v['xp']>=10*custo else 2 if v['xp']>=4*custo else 1; de=v['nivel']
        while lim>0 and v['xp']>=100*v['nivel']:
            v['xp']-=100*v['nivel']; v['nivel']+=1; lim-=1
        v['ultima_subida']=ndia; v.setdefault('log',[]).append(f"Tick {dia}: SOBE a {v['nivel']}" + (f" (de {de}: fila de XP)" if v['nivel']-de>1 else ''))
        print(f"{n}: SOBE a {v['nivel']}" + (f" (de {de}, fila de XP)" if v['nivel']-de>1 else '') + f" (sobra {v['xp']}/{100*v['nivel']})"); sobem.append(f"{n} {v['nivel']}")
        subidas.append((n, de, v['nivel']))
    save()
    # 502 (G39, pedido do jogador): o nível destrava o resto, sozinho: o PV da ficha de combate, a classe da faixa nova (a Prova),
    # o Despertar no 100/200/300 e as Artes. Depois do save(), porque o encadeia.py grava no npcs.json por conta própria.
    try:
        import encadeia
        for n, de, para in subidas:
            for l in encadeia.subiu(n, de, para, dia): print(l)
    except Exception as e: print('⚠ G39: o encadeamento da subida falhou:', e)
    if RES and sobem: print('::R:: SOBEM DE NÍVEL: '+' · '.join(sobem))
else: sys.exit(__doc__)
