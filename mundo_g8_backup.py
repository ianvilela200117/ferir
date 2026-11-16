#!/usr/bin/env python3
"""O MUNDO SE MOVE (regra da casa, Dia 201, pedido do jogador: "o mundo parou de expandir").
Todo DIA o mundo rola 1 novidade longe de Ferir; todo TICK SEMANAL rola 3 e tem 1 em 6 de abrir uma TERRA ALÉM DO MAPA.
Nada é escolhido: o dado diz O QUÊ (d20), ONDE (dN das regiões conhecidas + as que o mundo abriu) e QUANDO A NOTÍCIA CHEGA
a Ireviel (1d6: 1 hoje · 2-3 em 1d3 dias · 4-5 em 1d6 dias · 6 não chega sozinha: só se alguém for atrás).
Tudo entra no cânone (mundo.json). Uso: python3 mundo.py dia N   |   python3 mundo.py semana N   |   python3 mundo.py ver
MOTOR 6 (Dia 379): o sub-dado já sai LIDO ("→ LEITURA DO DADO: febre"), a notícia com dia marcado entra sozinha na AGENDA
(agenda.json; o tick avisa no dia em que chega) e o que cai numa terra do reino sai marcado "TOCA A CASA".
"""
import sys, json, secrets, subprocess, os, re
try:
    from nucleo import agenda_add, toca_a_casa, grava as _grava
except ImportError:   # o script segue rodando sozinho, sem o MOTOR 6
    agenda_add = None; toca_a_casa = lambda t: False; _grava = None
d=lambda n: secrets.randbelow(n)+1
AQUI=os.path.dirname(os.path.abspath(__file__)); ARQ=os.path.join(AQUI,'mundo.json')
REGIOES=['Ireviel e o rio','Levis e Levis-baixa','Lumade','Marasar (a Liga e o Doge)','Farenta','Gogrunn (as minas)','Kremir',
 'Telosus (o Colégio)','Shizess (as caravanas)','o Delta e as salinas','Mordun (a Boca com Fome)','as Fundas do Norte (o Clã Hegre)',
 'a Mata de Elais','o brejo do oeste (a Torre Afogada)','o sul, onde a areia come a pedra','as Montanhas de Fogo','os Picos Brancos','a costa (Ireviel–Marasar)',
 'Yaelane','Steunn','Zisrir']
TAB=[("GUERRA OU ESCARAMUÇA entre dois poderes (1d6: 1-2 a Liga contra alguém · 3 dois clãs · 4 uma cidade se rebela · 5 bandidos viram exército · 6 monstros contra homens)",None),
 ("NASCE UMA FACÇÃO nova (companhia, guilda, ordem, bando)",'npc'),
 ("UM LENDÁRIO AGE (1d6: 1 morre · 2 aparece um novo · 3 ataca · 4 desaparece · 5 procura um ferreiro · 6 funda algo)",None),
 ("DESCOBERTA DE MATERIAL (um veio, uma árvore, uma fera nova)",'material'),
 ("MONSTRO NOVO OU MIGRAÇÃO",'monstro'),
 ("FENÔMENO MÁGICO: a coberta afina (1d6: 1 estrela cai · 2 magia selvagem · 3 os mortos se mexem · 4 um rio muda · 5 um portal · 6 o céu sangra)",None),
 ("ROTA DE COMÉRCIO abre ou fecha (1d6: 1-3 abre · 4-6 fecha), mudando preços",None),
 ("PESTE OU DESASTRE (1d6: 1 febre · 2 fome · 3 enchente · 4 incêndio · 5 terremoto · 6 praga nos animais)",None),
 ("INVENÇÃO OU TÉCNICA NOVA (oficina, magia, guerra, plantio): alguém aprendeu algo que pode ser comprado ou roubado",None),
 ("UMA RUÍNA SE ABRE (masmorra, cripta, cidade afundada)",'lugar'),
 ("UM CULTO CRESCE ou nasce",'culto'),
 ("UM VILÃO NOVO entra no mundo",'vilao'),
 ("EMBAIXADA OU VISITA de terra distante (quer comprar, aliar-se ou espiar)",'npc'),
 ("FESTIVAL, TORNEIO OU FEIRA GRANDE (oportunidade de fama, ouro e material)",None),
 ("OFERTA PÚBLICA: alguém paga por um serviço",'missao'),
 ("MUDANÇA POLÍTICA (1d6: 1 morre um governante · 2 golpe · 3 casamento · 4 herdeiro · 5 lei nova · 6 um traidor exposto)",None),
 ("CLIMA ESTRANHO (inverno que não acaba, neve vermelha, seca, tempestade de cinza)",None),
 ("LUGAR NOVO DESCOBERTO",'lugar'),
 ("UMA PESSOA IMPORTANTE VIAJA (pode cruzar com Ferir)",'npc'),
 ("SURPRESA: o gerador de novidade",'novidade')]
def ger(tipo):
    try: return subprocess.run([sys.executable,os.path.join(AQUI,'gerador.py'),tipo,'1'],capture_output=True,text=True,timeout=30).stdout.strip()
    except Exception as e: return f'(gerador falhou: {e})'
def load():
    if os.path.exists(ARQ): return json.load(open(ARQ))
    return {'regioes_novas':[], 'eventos':[]}
def chega(dia):
    r=d(6)
    if r==1: return dia, f'[{r}] hoje'
    if r<=3: x=d(3); return dia+x, f'[{r}] em 1d3 [{x}] dias'
    if r<=5: x=d(6); return dia+x, f'[{r}] em 1d6 [{x}] dias'
    return None, f'[{r}] não chega sozinha (só se alguém for atrás)'
def decodifica(txt, r):
    """lê o sub-dado: "(1d6: 1-2 a Liga contra alguém · 3 dois clãs ...)" com r=3 → "dois clãs" """
    m = re.search(r'\(1d6: ([^)]*)\)', txt)
    if not m: return ''
    for parte in m.group(1).split(' · '):
        mm = re.match(r'(\d)(?:-(\d))? (.+)', parte.strip())
        if mm and int(mm.group(1)) <= r <= int(mm.group(2) or mm.group(1)): return mm.group(3)
    return ''
def curto(txt):
    return re.sub(r'\s*\([^)]*\)', '', txt).strip(' :')
def evento(dia,M):
    regs=REGIOES+M['regioes_novas']; i=d(20); txt,g=TAB[i-1]; w=d(len(regs)); onde=regs[w-1]
    sub=''; leitura=''
    if '1d6' in txt: r6=d(6); sub=f' · 1d6 [{r6}]'; leitura=decodifica(txt,r6)
    det=ger(g) if g else ''
    quando,ql=chega(dia)
    e={'dia':dia,'d20':i,'o_que':txt+sub,'onde':f'd{len(regs)} [{w}] {onde}','detalhe':det,'noticia_chega':quando,'chegada':ql}
    if leitura: e['leitura']=leitura
    nome=next((l.split(':',1)[1].strip() for l in det.split('\n') if l.startswith('nome:')),'')
    e['resumo']=curto(txt)+(f': {leitura}' if leitura else '')+f' — {onde}'+(f' ({nome})' if nome else '')
    e['toca']=bool(toca_a_casa(onde+' '+det))
    if quando is not None and agenda_add:
        agenda_add(quando, e['resumo'], tipo='noticia', origem=f'mundo.py, tick {dia}', toca=e['toca'])
    M['eventos'].append(e); return e
def show(e):
    print(f"  d20 [{e['d20']}] {e['o_que']}\n  ONDE: {e['onde']}" + ('  ◆ TOCA A CASA' if e.get('toca') else '') + f"\n  A NOTÍCIA: {e['chegada']}")
    if e.get('leitura'): print(f"  → LEITURA DO DADO: {e['leitura']}")
    if e['detalhe']: print('  ' + e['detalhe'].replace('\n','\n  '))
def main():
    a=sys.argv[1:]
    if not a: sys.exit(__doc__)
    M=load()
    if a[0]=='ver':
        for e in M['eventos'][-15:]: print(e['dia'], e['o_que'][:70], '|', e['onde'], '| chega', e['noticia_chega'])
        print('regiões novas:', M['regioes_novas']); return
    dia=int(a[1]); n=1 if a[0]=='dia' else 3
    print(f'O MUNDO SE MOVE — Dia {dia} ({a[0]})')
    for _ in range(n): show(evento(dia,M)); print('  ——')
    if a[0]=='semana':
        r=d(6); print(f'  TERRA ALÉM DO MAPA 1d6 [{r}]' + (' → ABRE-SE UMA REGIÃO NOVA:' if r==6 else ' → nada'))
        if r==6:
            det=ger('lugar'); nome=det.split('\n')[0].replace('nome: ','').strip()
            M['regioes_novas'].append(nome+' (terra nova)'); print('  '+det.replace('\n','\n  '))
    if _grava: _grava('mundo.json',M)
    else: json.dump(M,open(ARQ,'w'),ensure_ascii=False,indent=1)
if __name__=='__main__': main()
