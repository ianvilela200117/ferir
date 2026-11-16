#!/usr/bin/env python3
"""TESTE ABERTO (regra da casa, Dia 199): todo teste lê a MARGEM, não só passa/falha.
Uso: python3 aberto.py 1d20+N cd=X [oposto=M] [nivel=N] [nivel_op=N]   (d20 EXPLOSIVO: cada 20 rola de novo e soma; + nível ÷ 10; oposto: o outro lado rola igual)
Graus: falha por 10+ = FALHA FEIA (complicação) · falha = falha · passa = sucesso ·
       passa por 10+ = SUCESSO COM GANHO (algo a mais) · passa por 20+ = EXTRAORDINÁRIO (ganho + surpresa)
LEI DO VALOR (Dia 201): o bônus é a SOMA DE VALORES (atributo, perícia, equipamento, encantos, talentos, apoio), e o dado manda.
20 NATURAL — "O 20 MORDE": o d20 explode (rola outro e soma, sem limite) e, se mesmo assim não chegar, o 20 garante o SUCESSO MÍNIMO
  (consegue o essencial, nada além). NO ATAQUE: o 20 acerta sempre, o dano é de crítico (os dados da arma dobram) e a RD do alvo conta
  só a METADE; cada 20 a mais na cadeia: +1 dado de dano. Um fraco com 20 fere um forte: arranha, não mata.
1 NATURAL: falha sempre. A SURPRESA RUIM só vem se nem com o 1 o bônus chegava (quem é muito melhor erra sem desastre).
A SURPRESA sai da tabela abaixo (d20) e o Mestre a liga à cena; não é escolhida antes.
"""
import sys, secrets, re
d=lambda n: secrets.randbelow(n)+1
BOA=["alguém de fora viu e conta (Fama local +1)","acha uma coisa a mais no lugar (1d6: 1-2 ouro, 3-4 material, 5-6 pista)",
 "o outro lado deixa escapar um segredo que não era o pedido","ganha um aliado inesperado na cena","o tempo rende: a ação gasta metade do tempo",
 "abre uma porta nova (um lugar, uma pessoa, uma oferta)","um NPC muda de opinião sobre Ferir para melhor (+1 Memória)","o mundo responde: um rumor novo chega (gerador)",
 "o feito ensina: +1 dia de prática na perícia","a sorte vira: a próxima rolagem da cena tem +2","um inimigo comete um erro e se expõe",
 "aparece um item ou material que não estava em lista nenhuma (gerador material)","quem estava contra vira neutro","um velho fio esquecido volta a favor",
 "um animal, um espírito ou uma coisa estranha ajuda","alguém deve um favor a Ferir depois disso","o lugar guarda uma memória antiga e mostra",
 "ganha tempo: o relógio de uma facção contrária atrasa um passo","um laço se aproxima (momento verdadeiro)","SURPRESA GRANDE: rolar o gerador de novidade"]
RUIM=["quebra ou perde algo pequeno","alguém de fora viu e conta errado (boato)","o outro lado fica desconfiado (−1 Memória)","machuca-se: 1d6 PV",
 "chega alguém na hora errada","o tempo vai embora: a ação gasta o dobro","um rival fica sabendo","o barulho atrai algo","uma pista falsa parece verdadeira",
 "um aliado se ofende","o material estraga um pouco","uma dívida antiga é lembrada","o relógio de uma facção contrária anda um passo","um laço sofre (atrito)",
 "a próxima rolagem da cena tem −2","perde um recurso (ouro 1d6×10)","um segredo pequeno de Ferir escapa","o clima piora","um animal ou coisa estranha atrapalha",
 "SURPRESA RUIM GRANDE: rolar o gerador de novidade (e o Mestre a liga ao erro)"]
a=sys.argv[1:]
m=re.match(r'1d20([+-]\d+)?',a[0]); bon=int(m.group(1) or 0)
cd=next((int(x[3:]) for x in a if x.startswith('cd=')),None)
op=next((int(x[7:]) for x in a if x.startswith('oposto=')),None)
def ex():
    ch=[d(20)]
    while ch[-1]==20: ch.append(d(20))
    return ch
nv=next((int(x[6:]) for x in a if x.startswith('nivel=')),0)//10
nvo=next((int(x[9:]) for x in a if x.startswith('nivel_op=')),0)//10
ch=ex(); r=ch[0]; tot=sum(ch)+bon+nv
if op is not None:
    cho=ex(); cd=sum(cho)+op+nvo; print(f'oposto: {cho} + {op} + nível {nvo} = {cd}')
mg=tot-cd
print(f'teste: {ch} + {bon} + nível {nv} = {tot} vs {cd} (margem {mg:+d})')
ok = (mg>0 if op is not None else mg>=0)
if r==1: ok=False
if not ok and r==20: grau='O 20 MORDE: SUCESSO MÍNIMO (no ataque: acerta, dano de crítico, RD pela metade, +%d dado(s) extra)' % (ch.count(20)-1)
elif not ok: grau='FALHA FEIA (complicação)' if (mg<=-10 and r!=1) else 'falha'
else: grau='EXTRAORDINÁRIO' if mg>=20 else 'SUCESSO COM GANHO' if mg>=10 else 'sucesso'
if ok and r==20 and ch.count(20)>1: grau+=f' · cadeia de {ch.count(20)} vintes (no ataque: crítico com +{ch.count(20)-1} dado(s))'
print('grau:',grau)
if r==20 or grau=='EXTRAORDINÁRIO': print('  SURPRESA BOA (d20):',BOA[d(20)-1])
if (r==1 and 1+bon+nv<cd) or grau=='FALHA FEIA (complicação)': print('  SURPRESA RUIM (d20):',RUIM[d(20)-1])
elif r==1: print('  1 natural de quem é muito melhor: erra, sem desastre')
