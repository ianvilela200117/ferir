#!/usr/bin/env python3
"""motor.py — a configuração do MOTOR 6 (motor.json) e a cola dos comandos.

Uso:
  python3 motor.py                 a cola: todos os comandos do motor numa tela
  python3 motor.py vigia           a lista do que TOCA A CASA (o resumo do tick mostra inteiro só o que cita uma delas)
  python3 motor.py vigia +Nome     passa a vigiar (um nome novo de inimigo, cidade, monstro)
  python3 motor.py vigia -Nome     deixa de vigiar
  python3 motor.py regra "texto"   acrescenta uma REGRA DO JOGADOR (aparece em todo BRIEFING)
"""
import sys
from nucleo import carrega, grava, sem_acento

COLA = """MOTOR 6.4 — A COLA DO MESTRE
COMEÇAR UMA SESSÃO     python3 contexto.py            → escreve e mostra o BRIEFING.md (o painel); ler também MESTRE.md, canone, regras e estado_vivo
CORRER OS DIAS         python3 tick.py bloco N        → N dias de uma vez, saída INTEIRA; PARA sozinho em parada (com "resumo": só o que toca a casa)
                       python3 tick.py ate DIA        → idem, até o dia
                       python3 tick.py dia [segura]   → um dia, saída inteira (como antes)
DADO COM TABELA        python3 selo.py dr ID "título" d20 "1-10: x | 11-19: y | 20n: SURPRESA"
VÁRIOS DADOS           python3 selo.py lote -   (uma linha por dado:  ID ;; título ;; d20+2 ;; tabela)
O CONSELHO VOTA        python3 conselho.py ID "pergunta" "A: ..." "B: ..." Sira=B+4 Eliane=A+2 fora=Tolvane   (voto por cadeira)
  (o jeito rápido)     python3 selo.py conselho ID "pergunta" "opção A:6" "opção B:9" "opção C:4"
CLIMA E CALENDÁRIO     python3 clima.py ver · previsao      (o tick rola o tempo de cada cidade e o nível do rio)
VIAGEM E RECADO        python3 viagem.py vai "quem" DESTINO [de=ORIGEM] [volta] [para]   (dias do Livro; a chegada entra na agenda)
CERCO DE LONGE         python3 cerco.py NOME dia DIA · visao · entra QUEM · ver
FICHAS DE COMBATE      python3 combate.py ver · monta SAIDA base=sims/ARQ.json Nome Nome   (o grupo com o nível de hoje)
FERIDOS                python3 feridos.py ver · rola NOME [caiu] [medicina]   (o luta.py chama sozinho)
MERCADO                python3 mercado.py ver · choque CIDADE COISA +N "motivo"
LEGITIMIDADE           python3 reino.py legit -1 "passou por cima do voto" · prest +1 "vitória"
LEALDADE               python3 npc.py lealdade NOME -1 "motivo" · lealdades
RECURSOS DO DIA        python3 ficha.py usa "Visão" · recurso "NOME" MAX dia|cena
JULGAMENTO             python3 julgamento.py abre ID "caso" acusador=.. reu=.. lei=.. · prova · testemunha · sentenca
TRATADOS               python3 tratados.py ver · novo · clausula · estado ID vigente   (a semana cobra sozinha)
BATALHA DE EXÉRCITOS   python3 batalha.py NOME [sim=2000] · modelo
ONDE ESTÁ CADA UM      python3 onde.py ver · poe "Nome" LUGAR · viagem.py ... leva=Nome,Nome
PAINEL E CRÔNICA       python3 painel.py (painel.html, só o que Ferir sabe) · python3 cronica.py (cronica.md, lua a lua)
TESTE DO MOTOR         python3 teste_motor.py   (numa cópia; não mexe no save)
FACÇÕES                python3 faccoes.py ver [tudo] · semear · postura "NOME" N · objetivo "NOME" "novo"
GUILDAS DO MUNDO (G12) python3 guildas.py ver [tudo] · ranking · fama ID|casa +N "motivo" · forca|postura ID N · objetivo ID "novo"   (o tick semanal roda a semana)
MASMORRA (G14)         python3 masmorra.py gera NOME CAT "o que guarda" · ver NOME [tudo] · entra NOME SALA
REPUTAÇÃO (G21)        python3 reputacao.py ver · muda "QUEM" +N "motivo"
HABILIDADES À MÃO (G24) python3 habilidades.py mao   (a linha 🛠️ do turno) · usa "Nome" · carga "Nome" -1|cheio
LIVRO NOVE (MOTOR 9)   compendio/08_livro_nove.md: G25 crias · G26 Despertar · G27 éditos · G28 canções · G29 bênçãos · G30 Artes de arma · G31 magia · G32 itens · G33 monstros ("tracos": [...] no monstro; o luta.py roda sozinho) · G34 masmorra
ÉDITOS (G27)           python3 edito.py ver · catalogo · propoe CHAVE · aprova CHAVE [por_cima] · recusa · revoga   (o tick semanal põe em vigor)
CRIAS (G25)            python3 cria.py ver · nova NOME "PAI" CAT NIVEL ESSENCIA [laco=..] · laco · xp · ficha · mostra · solta   (o tick semanal faz crescer)
CANÇÕES (G28)          python3 cancao.py ver · canta "FEITO" tipo=.. cantor=..|contratado oferece=A,B · atributo NOME
DESPERTAR (G26)        python3 despertar.py ver · devidos · rola todos|casa|NOME · dom NOME "Dom" · nome NOME "nome"
ARTES DE ARMA (G30)    python3 artes.py ver · da NOME arma=lanca|?.. [cat=..] [oculto] · ficha NOME   (python3 luta.py artes|tracos: as listas)
FICHAS DOS NPCs        python3 classe.py liga NOME "Classe" · gera NOME [FAMÍLIA] · npc.py vida NOME|todos
COLETA (G35)           python3 coleta.py ver · reserva "LUGAR" MAT CAT [tamanho=..] · vai NOME OFICIO "LUGAR" [dias=N] [para=casa] · esfola · grau
FESTAS (G36)           python3 festas.py ver · proximas [N]   (o tick diário aplica no dia)
ATLAS (G37)            python3 masmorra.py atlas · degrau NOME · estado NOME "texto" · extra ...
COVIL E LENDÁRIAS (G13) na ficha do bicho: "covil": {nome,dano,cd,efeito} · "lendarias": N (o luta.py faz o resto)
ANOTAR NO ENVELOPE     python3 selo.py nota "LEITURA: ..."
TESTE DE PERÍCIA       python3 aberto.py 2d20+N cd=X [oposto=M] [nivel=N]
FORJA E ENCANTO        python3 obra_valor.py obra|encantar|reforja|conserto|sim|fichas ...
LUTA                   python3 luta.py sims/X.json            (uma luta de verdade)
RÉGUA ESCONDIDA        python3 luta.py sims/X.json regua=2000 (simula, mostra a distribuição e grava no envelope como OCULTO)
XP, COFRE, MATERIAL    python3 ficha.py xp N "motivo" · cofre -N "motivo" · mat zeieth -0.2 "motivo" · ver
AGENDA E FIOS          python3 agenda.py ver · add DIA "texto" [oculto] [para] · feito ID · fios · fio "texto" · toca ID
RELÓGIOS               python3 relogio.py ver · novo ... · anda "NOME" +1 "motivo" · fecha "NOME" "desfecho"
NPC EM CENA            python3 npc.py cena Eliane Sira Moreth   (fichas curtas; não abrir npcs.json)
XP DE NPC              python3 cresce.py xp NOME QTD "motivo"
REINO                  python3 reino.py estado · projeto · mod · pilar · rel  (a semana roda dentro do tick semanal)
NOME NOVO              python3 nomes.py SONORIDADE 6 livre   (já sai conferido contra o cânone e o Livro)
FATO ANTIGO            python3 confere.py TERMO               (antes de narrar o que não está no BRIEFING)
FIM DE SESSÃO          python3 salvar.py              → conferidor + BRIEFING novo + zip do save
ARRUMAR OS NPCs        python3 npc.py arquiva         → notas velhas vão para npcs_arquivo.json (nada se apaga)
"""


def main():
    a = sys.argv[1:]
    M = carrega('motor.json', {})
    if not a:
        print(COLA)
        return
    if a[0] == 'vigia':
        if len(a) == 1:
            print('O QUE TOCA A CASA: ' + ' · '.join(M.get('vigia', [])))
            return
        for x in a[1:]:
            if x.startswith('+'):
                if not any(sem_acento(v) == sem_acento(x[1:]) for v in M['vigia']):
                    M['vigia'].append(x[1:])
                print('vigiando:', x[1:])
            elif x.startswith('-'):
                M['vigia'] = [v for v in M['vigia'] if sem_acento(v) != sem_acento(x[1:])]
                print('deixou de vigiar:', x[1:])
            else:
                sys.exit('use +Nome para vigiar e -Nome para tirar')
        grava('motor.json', M)
    elif a[0] == 'regra' and len(a) > 1:
        M.setdefault('regras_do_jogador', []).append(a[1])
        grava('motor.json', M)
        print('regra do jogador guardada (entra em todo BRIEFING).')
    else:
        print(__doc__)


if __name__ == '__main__':
    main()
