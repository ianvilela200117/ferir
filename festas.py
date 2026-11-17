#!/usr/bin/env python3
"""festas.py — MOTOR 9 (G36): AS FESTAS DO CALENDÁRIO, com efeito (Livro Nove 15).

Cada lua tem uma festa. Na semana dela, o efeito vale onde a festa se faz. O rei que PAGA a festa (o custo ao lado)
garante o efeito bom e ganha a reputação escrita; sem pagar, a festa acontece menor e só o efeito de base vale.

Uso:
  python3 festas.py ver                o ano inteiro, com os dias de cada festa a partir de hoje
  python3 festas.py hoje [DIA]         a festa de hoje e as dos próximos 7 dias (o tick diário chama)
"""
import sys
from nucleo import calendario, dia_atual, LUAS

F = [  # (lua, dia, nome, efeito de base, se o rei paga: custo, ganho)
 (1, 15, 'a Noite do Fogo Guardado', 'cada casa guarda uma brasa: Ordem +1 na semana em toda cidade', 50, 'o rei acende a brasa da praça: reputação +2 na capital'),
 (2, 10, 'a Caçada do Lobo', 'os caçadores saem: as guildas e as caçadas do reino têm +2 no dado da semana; o avistamento de monstro rola duas vezes', 100, 'prêmio do rei ao melhor caçador: reputação +2 com a Guilda dos Aventureiros'),
 (3, 20, 'o Dia das Cinzas', 'o reino lembra os mortos: Falar com Morto cobra metade do sangue hoje; servo de osso à vista ofende (reputação −5 a mais)', 50, 'o rei paga as velas: reputação +2 com o templo da cidade'),
 (4, 5, 'a Abertura do Rio', 'as barcas voltam: Comércio +1 na semana nas cidades do rio; viagem de barca um quarto mais rápida', 100, 'a primeira barca leva a bandeira do rei: reputação +2 com os barqueiros'),
 (5, 12, 'a Bênção da Semente', 'o dado da Comida da semana rola com +1; casamento feito hoje dá Laço +1 aos dois', 100, 'o rei dá a semente: Comida não recua por evento nesta lua'),
 (6, 27, 'o Dia do Primeiro Martelo', 'a casa de Ferir faz anos (o Dia 1 foi um 27 da Lua das Barcas): obra de forja feita em praça hoje tem +2', 200, 'a forja aberta ao povo: reputação +5 na capital (uma vez por ano)'),
 (7, 1, 'a Feira do Sal', 'mercadores do Delta sobem o rio: uma novidade de mercado em cada cidade do rio; material 10% mais barato na semana', 150, 'banca do rei na feira: a renda da semana +10%'),
 (8, 8, 'a Noite das Forjas', 'toda forja acesa: +1 em toda obra de forja na semana; o fogo corre: d20, com 1 um bairro pega fogo', 100, 'a ronda do fogo paga: o incêndio não acontece'),
 (9, 15, 'a Procissão da Água', 'as fés saem às ruas: o dado da Saúde da semana rola com +1', 50, 'o rei anda na procissão: reputação +2 com a fé da cidade em que ele estiver'),
 (10, 10, 'a Colheita', 'Comida +1 na semana em toda cidade', 200, 'a mesa do rei na praça: a renda da semana +10% e reputação +2 em toda cidade'),
 (11, 1, 'a Vindima e os Jogos das Cidades', 'sete dias de trégua; o chamado de recrutas rola com +3; os Jogos (Livro Nove 13) se alguém os pagar', 2000, 'o rei chama os Jogos: quatro provas, títulos e a praça cheia de enviados'),
 (12, 30, 'a Noite das Velas', 'véspera dos Dias Mudos: morto-vivo Comum não anda esta noite; juramento feito nela vale em dobro (Elo)', 50, 'uma vela por morto da casa: os servos do rei não assustam ninguém nesta noite'),
]
MUDOS = 'OS DIAS MUDOS (cinco, no fim do ano): não se acende forja grande, não se faz magia de 4º círculo para cima e não se casa. Quem quebra o silêncio: reputação −5 na cidade e Revés +1'


def dia_de(lua, dl, hoje):
    doy = (lua - 1) * 30 + dl; base = (hoje - 190) // 365 * 365 + 190 + doy - 1
    return base if base >= hoje else base + 365


def main():
    a = sys.argv[1:]; hoje = int(a[1]) if len(a) > 1 else dia_atual()
    if not a or a[0] == 'ver':
        if not a: print(__doc__)
        print(f'AS FESTAS DO ANO (G36) · hoje é o Dia {hoje}: {calendario(hoje)["txt"]}')
        for lua, dl, nome, ef, custo, ganho in sorted(F, key=lambda x: dia_de(x[0], x[1], hoje)):
            print(f"  Dia {dia_de(lua, dl, hoje)} ({dl} da Lua {LUAS[lua - 1]}): {nome.upper()} · {ef} · se o rei paga ({custo}): {ganho}")
        print('  ' + MUDOS); return
    if a[0] == 'hoje':
        c = calendario(hoje)
        if c.get('mudo'): print('  ◈ ' + MUDOS)
        for lua, dl, nome, ef, custo, ganho in F:
            dd = dia_de(lua, dl, hoje) - hoje
            if dd == 0: print(f"  ◈ FESTA HOJE: {nome.upper()} · {ef} · se o rei paga ({custo}): {ganho}")
            elif dd <= 7: print(f"  ◈ festa em {dd} dia(s) (Dia {hoje + dd}): {nome} · se o rei paga ({custo}): {ganho}")
        return
    sys.exit(__doc__)


if __name__ == '__main__':
    main()
