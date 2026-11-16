#!/usr/bin/env python3
"""edito.py — G27, O CÓDIGO DE IREVIEL (Livro Nove 10.2; MOTOR 9.1, Dia 438): os éditos do rei saem do papel.

O rei PROPÕE, o conselho VOTA (conselho.py; tudo passa pela Intendente) e o édito VALE a partir do tick semanal seguinte.
O script guarda quem está em vigor (editos.json), confere o TETO (2 + Legitimidade ÷ 3; +1 com o talento Legislador), põe os
modificadores nos pilares (reino.py mod), soma o preço na despesa fixa da semana (ficha.py fixo), mexe na reputação, na
Legitimidade e no prestígio, e lembra o Mestre, toda semana, do que fica à mão.

Uso:
  python3 edito.py ver                         os éditos em vigor, o teto e o preço por semana
  python3 edito.py catalogo                    os 16 do Livro, com o efeito e o preço
  python3 edito.py propoe CHAVE [cidade=X] [fe="a Vigília"]   prepara o voto: imprime o tracos.py inclina e o conselho.py para rodar
  python3 edito.py aprova CHAVE [por_cima]     depois do voto: entra na fila e VALE no próximo tick semanal (por_cima: o rei passou por cima: Legitimidade −1)
  python3 edito.py recusa CHAVE                o conselho recusou e o rei aceitou: sai da fila
  python3 edito.py revoga CHAVE                tira o édito (antes de uma lua: Legitimidade −1; com Legislador: −2)
  python3 edito.py semana DIA                  o tick semanal chama sozinho: ativa os aprovados e lembra os que valem
CHAVE: feira · grao · ronda · oficio · caca · osso · mao · sal · chamado · colegio · moeda · fisico · estrada · fe · carta · juizo
"""
import subprocess, sys
from nucleo import carrega, grava, anota, dia_atual, calendario, sem_acento, P

ARQ = 'editos.json'
# nome · escopo · mods (pilar, valor, onde: 'todas' | 'capital' | 'cidade') · custo por semana (fixo, por cidade) · uma vez (lista de ações) · lembrete semanal · eixos do voto
CAT = {
 'feira':   dict(nome='da Feira Franca', cidade=True, mods=[('Comércio', 1, 'cidade')], efeito='Comércio +1 na cidade; mercadores de fora chegam (uma novidade de mercado por lua)',
                 preco='a portagem dessa cidade cai à metade', lembra='FEIRA FRANCA: a portagem da cidade pela metade (descontar da renda dela); 1 novidade de mercado por lua (mercado.py choque ou gerador material)',
                 eixos=('gasto,povo,novidade', 'poupar,tradicao')),
 'grao':    dict(nome='do Grão Guardado', mods=[('Comida', 1, 'todas')], inverno=True, custo=100, efeito='celeiros do reino: Comida +1 em toda cidade no INVERNO e em cerco',
                 preco='100 por semana', lembra='GRÃO GUARDADO: em CERCO, Comida +1 na cidade cercada (reino.py mod à mão)', eixos=('cautela,povo', 'poupar')),
 'ronda':   dict(nome='da Ronda', mods=[('Ordem', 1, 'todas')], custo_cidade=140, efeito='Ordem +1 em toda cidade', preco='140 por semana por cidade', eixos=('rigor,gasto', 'poupar,misericordia')),
 'oficio':  dict(nome='do Ofício Livre', efeito='qualquer um abre oficina sem pedir à guilda: um pedido a mais por semana no Fundo dos Ofícios', preco='reputação −10 com as guildas de ofício',
                 lembra='OFÍCIO LIVRE: um pedido A MAIS no Fundo dos Ofícios nesta semana; as guildas de ofício (a Guilda de Levis, a Bigorna Livre, os Mineiros) com −10 (à mão, no que cada uma é)',
                 eixos=('novidade,povo', 'tradicao')),
 'caca':    dict(nome='da Caça Paga', custo=200, efeito='o reino paga por parte de monstro: as guildas caçam os bichos do reino com +2 no dado delas, e o rei tem a primeira compra de todo núcleo',
                 preco='200 por semana em prêmios', lembra='CAÇA PAGA: +2 no dado das guildas contra bicho DO REINO (guildas.py) e a PRIMEIRA COMPRA de todo núcleo é do rei', eixos=('gasto,guerra', 'poupar')),
 'osso':    dict(nome='do Osso', efeito='os servos do rei andam dentro da lei: a perda de reputação da G23 (−5 por cidade) não acontece no reino',
                 preco='reputação −10 com a Mão Queimada e com o Templo do Rio; a Vigília manda um observador', rep=[('a Mão Queimada', -10), ('o Templo do Rio', -10)],
                 lembra='ÉDITO DO OSSO: servo armado visto em cidade DO REINO não tira reputação; o OBSERVADOR DA VIGÍLIA está na corte (gerar na 1ª cena)', eixos=('rei,novidade', 'fe,tradicao')),
 'mao':     dict(nome='da Mão Livre', efeito='acaba o trabalho forçado: Legitimidade +1 e reputação +10 em toda cidade', preco='perde o desconto das obras (G6); os forçados soltos escolhem ficar ou ir (dado)',
                 legit=1, rep_cidades=10, lembra='MÃO LIVRE: a G6 (obra a quatro quintos) NÃO vale; na 1ª semana, rolar no selo quantos forçados ficam', eixos=('misericordia,povo', 'rigor,poupar')),
 'sal':     dict(nome='do Sal', mods=[('Dinheiro', 1, 'capital')], efeito='o sal é do rei: Dinheiro +1 na capital', preco='o contrabando sobe (um evento de contrabando por lua); reputação −10 no Delta',
                 rep=[('os Do Junco (o Delta)', -10), ('a Lurentetta (o Delta)', -10)], lembra='ÉDITO DO SAL: 1 evento de CONTRABANDO por lua (declarar no selo)', eixos=('rei,rigor', 'povo,paz')),
 'chamado': dict(nome='do Chamado', mods=[('Ordem', -1, 'todas'), ('Comida', -1, 'todas')], efeito='20 lanças novas por lua, sem pedir peça', preco='Ordem −1 e Comida −1 enquanto valer',
                 lembra='ÉDITO DO CHAMADO: +20 lanças a cada lua (o soldo delas entra na despesa: ficha.py fixo)', eixos=('guerra,rei', 'paz,povo')),
 'colegio': dict(nome='do Colégio', custo=150, efeito='toda criança com dom vai ao Colégio: um aprendiz de mago por estação entra na casa', preco='150 por semana; as famílias que perdem braços reclamam (reputação −5 no campo)',
                 rep_cidades=-5, lembra='ÉDITO DO COLÉGIO: 1 APRENDIZ DE MAGO por estação (gerar no começo de cada estação)', eixos=('saber,novidade', 'povo,poupar')),
 'moeda':   dict(nome='da Moeda', prest=1, efeito='Ireviel cunha moeda: prestígio +1, e o Dinheiro da capital não recua por evento de fora', preco='a oficina de cunho (obra de 2.000: reino.py projeto) e um mestre; moeda falsa vira crime de traição',
                 lembra='ÉDITO DA MOEDA: o Dinheiro da capital NÃO recua por evento de fora (se o dado do reino mandar recuar por isso, não recua)', eixos=('rei,gasto,novidade', 'poupar,cautela')),
 'fisico':  dict(nome='do Físico', mods=[('Saúde', 1, 'todas')], custo_cidade=120, efeito='casas de cura: Saúde +1 em toda cidade; os feridos da casa tratados nelas têm −3 no dado do ferimento',
                 preco='120 por semana por cidade', lembra='ÉDITO DO FÍSICO: ferido da casa tratado numa cidade do reino: "medicina" no feridos.py (−3)', eixos=('misericordia,gasto,povo', 'poupar')),
 'estrada': dict(nome='da Estrada', custo=100, efeito='patrulha e marco: viagem da casa dentro do reino um quarto mais rápida; menos assalto', preco='100 por semana; pedágio (o Comércio não avança por dado na primeira lua)',
                 lembra='ÉDITO DA ESTRADA: viagem.py dentro do reino: tirar um quarto dos dias; encontro de estrada com −2', lua1='o Comércio NÃO avança por dado (se o dado do reino mandar avançar, fica)', eixos=('rigor,gasto', 'poupar,povo')),
 'fe':      dict(nome='da Fé do Reino', fe=True, efeito='uma fé vira a do reino: a bênção dela (Livro Nove 12) vale para a casa sem o voto pessoal', preco='reputação −10 com todas as outras fés',
                 lembra='FÉ DO REINO: a bênção da fé escolhida vale para a casa; as OUTRAS fés com −10 (à mão, cada uma no que é)', eixos=('fe,tradicao', 'paz,novidade')),
 'carta':   dict(nome='da Carta às Guildas', efeito='toda guilda no reino se registra: reputação +5 com as registradas e o rei sabe a força de cada uma', preco='as que recusam viram hostis; aventureiro sem registro é preso',
                 lembra='CARTA ÀS GUILDAS: na 1ª semana, d6 por guilda do reino (1 recusa e vira hostil · 2-6 registra: +5)', eixos=('rigor,rei', 'paz,povo')),
 'juizo':   dict(nome='do Juízo', efeito='um tribunal fixo julga sem o rei: Legitimidade +1 por estação sem execução sumária', preco='o rei não perdoa nem condena sozinho enquanto valer',
                 lembra='ÉDITO DO JUÍZO: no começo de cada ESTAÇÃO sem execução sumária, reino.py legit +1; o rei NÃO julga sozinho', eixos=('honra,rigor,povo', 'rei')),
}


def roda(script, *args):
    r = subprocess.run([sys.executable, P(script)] + [str(x) for x in args], capture_output=True, text=True)
    out = (r.stdout + r.stderr).strip()
    if out: print('    ' + out.replace('\n', '\n    '))


def acha(ch):
    k = sem_acento(ch).replace('do ', '').replace('da ', '').strip()
    c = [x for x in CAT if x == k] or [x for x in CAT if x.startswith(k) or k in sem_acento(CAT[x]['nome'])]
    if len(c) != 1: sys.exit(f'édito não achado (ou ambíguo): "{ch}" · chaves: {", ".join(CAT)}')
    return c[0]


def teto():
    leg = carrega('reino.json')['reino'].get('legitimidade', 10)
    tal = any(sem_acento(t.get('nome', '')) == 'legislador' for t in carrega('habilidades.json', {}).get('talentos', []))
    return 2 + leg // 3 + (1 if tal else 0), leg, tal


def cidades():
    return [c['nome'] for c in carrega('reino.json')['cidades']]


def custo(e):
    c = CAT[e['chave']]
    return c.get('custo', 0) + c.get('custo_cidade', 0) * len(cidades())


def onde(e, alvo):
    cs = cidades()
    return cs if alvo == 'todas' else [cs[0]] if alvo == 'capital' else [e.get('cidade') or cs[0]]


def poe_mods(e, liga):
    c = CAT[e['chave']]
    for pilar, v, alvo in c.get('mods', []):
        for cid in onde(e, alvo):
            roda('reino.py', 'mod', cid, pilar, v if liga else 0, f"ÉDITO {c['nome']}")


def ver(S):
    t, leg, tal = teto(); vig = [e for e in S['editos'] if e['estado'] == 'vigente']; fila = [e for e in S['editos'] if e['estado'] in ('proposto', 'aprovado')]
    print(f"O CÓDIGO DE IREVIEL (G27) · em vigor {len(vig)} de {t} (2 + Legitimidade {leg} ÷ 3" + (' + 1 do Legislador' if tal else '') + f") · preço por semana: {sum(custo(e) for e in vig)}")
    for e in vig:
        c = CAT[e['chave']]
        print(f"  ● o Édito {c['nome']}" + (f" ({e['cidade']})" if e.get('cidade') else '') + (f" ({e['fe']})" if e.get('fe') else '') + f" · desde o {e['desde']} · {c['efeito']} · PREÇO: {c['preco']}")
    for e in fila:
        print(f"  ○ o Édito {CAT[e['chave']]['nome']}: {e['estado'].upper()}" + (f" (vale no tick semanal do {e['vale_de']})" if e.get('vale_de') else ' (falta o voto do conselho)'))
    if not vig and not fila: print('  nenhum édito ainda. (edito.py catalogo · edito.py propoe CHAVE)')


def main():
    a = sys.argv[1:]; S = carrega(ARQ, {'nota': 'G27: os éditos do rei (edito.py). estado: proposto → aprovado → vigente → revogado.', 'editos': []})
    dia = dia_atual()
    if not a or a[0] == 'ver':
        if not a: print(__doc__)
        ver(S); return
    if a[0] == 'catalogo':
        for k, c in CAT.items(): print(f"  {k:8s} o Édito {c['nome']}" + (' (numa cidade)' if c.get('cidade') else '') + f": {c['efeito']} · PREÇO: {c['preco']}")
        return
    if a[0] == 'semana':
        dia = int(a[1]) if len(a) > 1 else dia; cal = calendario(dia); mudou = False
        for e in S['editos']:
            c = CAT[e['chave']]
            if e['estado'] == 'aprovado' and e.get('vale_de', 0) <= dia:
                e['estado'] = 'vigente'; e['desde'] = dia; mudou = True
                print(f"  ÉDITO {c['nome']} ENTRA EM VIGOR: {c['efeito']} · PREÇO: {c['preco']}")
                if not c.get('inverno'): poe_mods(e, True)
                if custo(e):
                    F = carrega('ficha.json'); roda('ficha.py', 'fixo', 'despesa', F['livro']['despesa'] + custo(e), f"o Édito {c['nome']} (+{custo(e)} por semana)")
                for quem, n in c.get('rep', []): roda('reputacao.py', 'muda', quem, n, f"o Édito {c['nome']}")
                if c.get('rep_cidades'):
                    for quem in carrega('mundo_vivo.json').get('reputacao', {}):
                        if '(a cidade)' in quem: roda('reputacao.py', 'muda', quem, c['rep_cidades'], f"o Édito {c['nome']}")
                if c.get('legit'): roda('reino.py', 'legit', f"{c['legit']:+d}", f"o Édito {c['nome']}")
                if c.get('prest'): roda('reino.py', 'prest', f"{c['prest']:+d}", f"o Édito {c['nome']}")
                anota(f"- ÉDITO (G27) [Dia {dia}]: o Édito {c['nome']} entra em vigor" + (f" ({e.get('cidade')})" if e.get('cidade') else ''))
            if e['estado'] == 'vigente':
                if c.get('inverno'):   # o Grão Guardado só pesa no inverno (e em cerco, à mão)
                    quer = cal['estacao'] == 'Inverno'
                    if quer != bool(e.get('mods_ligados')): poe_mods(e, quer); e['mods_ligados'] = quer; mudou = True; print(f"  ÉDITO {c['nome']}: " + ('é INVERNO: Comida +1 em toda cidade' if quer else 'o inverno passou: o +1 de Comida sai'))
                if c.get('lembra'): print('  À MÃO · ' + c['lembra'])
                if c.get('lua1') and dia - e['desde'] < 30: print(f"  À MÃO · ÉDITO {c['nome']} (1ª lua): {c['lua1']}")
        vig = [e for e in S['editos'] if e['estado'] == 'vigente']
        print(f"  éditos em vigor: {len(vig)} de {teto()[0]}" + (' · ' + ', '.join(CAT[e['chave']]['nome'] for e in vig) if vig else ''))
        if mudou: grava(ARQ, S)
        return
    if len(a) < 2: sys.exit(__doc__)
    k = acha(a[1]); c = CAT[k]; vivo = next((e for e in S['editos'] if e['chave'] == k and e['estado'] != 'revogado'), None)
    if a[0] == 'propoe':
        if vivo: sys.exit(f"o Édito {c['nome']} já está {vivo['estado']}.")
        cid = next((x[7:] for x in a[2:] if x.startswith('cidade=')), None); fe = next((x[3:] for x in a[2:] if x.startswith('fe=')), None)
        if c.get('cidade') and not cid: sys.exit('este édito vale NUMA cidade: cidade=Ireviel (ou Levis, Farenta, "o Porto de Marasar")')
        if c.get('fe') and not fe: sys.exit('diga a fé: fe="a Vigília" (as dez estão no Livro Nove 12)')
        t, leg, _ = teto(); n = len([e for e in S['editos'] if e['estado'] in ('vigente', 'aprovado')])
        if n >= t: print(f'⚠ TETO: já há {n} éditos e o teto é {t}. O conselho pode votar, mas o édito só entra se outro sair (edito.py revoga).')
        S['editos'].append({'chave': k, 'estado': 'proposto', 'proposto': dia, 'cidade': cid, 'fe': fe}); grava(ARQ, S)
        anota(f"- ÉDITO (G27) [Dia {dia}]: o rei PROPÕE o Édito {c['nome']}" + (f' ({cid})' if cid else '') + (f' ({fe})' if fe else '') + f": {c['efeito']} · PREÇO: {c['preco']} · falta o voto do conselho")
        print(f"PROPOSTO: o Édito {c['nome']}: {c['efeito']} · PREÇO: {c['preco']}")
        print('O VOTO (G27; a inclinação sai dos traços, não da cabeça):')
        print(f"  python3 tracos.py inclina A={c['eixos'][0]} B={c['eixos'][1]} [fora=Nome,Nome]")
        print(f"  python3 conselho.py ED{dia}{k} \"o Édito {c['nome']}: {c['efeito']} (preço: {c['preco']})\" \"A: aprovar\" \"B: recusar\" <COLAR as inclinações>")
        print(f"  depois: python3 edito.py aprova {k}   (ou: aprova {k} por_cima · recusa {k})")
        return
    if a[0] in ('aprova', 'recusa'):
        if not vivo or vivo['estado'] != 'proposto': sys.exit(f"o Édito {c['nome']} não está proposto (edito.py propoe {k}).")
        if a[0] == 'recusa':
            vivo['estado'] = 'revogado'; vivo['recusado'] = dia; grava(ARQ, S); anota(f"- ÉDITO (G27) [Dia {dia}]: o conselho RECUSOU o Édito {c['nome']}; o rei aceitou"); print('recusado; sai da fila.'); return
        t, leg, _ = teto(); n = len([e for e in S['editos'] if e['estado'] in ('vigente', 'aprovado')])
        if n >= t: sys.exit(f'TETO: {n} éditos de {t}. Revogue um antes (edito.py revoga CHAVE). Nada mudou.')
        vale = carrega('estado.json').get('tempo', {}).get('primeiro_tick_semanal', dia + 7)
        vivo['estado'] = 'aprovado'; vivo['vale_de'] = vale; vivo['por_cima'] = 'por_cima' in a; grava(ARQ, S)
        if vivo['por_cima']: roda('reino.py', 'legit', '-1', f"o rei passou por cima do voto: o Édito {c['nome']}")
        anota(f"- ÉDITO (G27) [Dia {dia}]: o Édito {c['nome']} APROVADO" + (' (o rei PASSOU POR CIMA do voto: Legitimidade −1)' if vivo['por_cima'] else ' pelo conselho') + f"; vale no tick semanal do {vale}")
        print(f"APROVADO: o Édito {c['nome']} vale a partir do tick semanal do Dia {vale}." + (f" Preço por semana: {custo(vivo)}." if custo(vivo) else '')); return
    if a[0] == 'revoga':
        if not vivo: sys.exit(f"o Édito {c['nome']} não está em vigor nem na fila.")
        if vivo['estado'] == 'vigente':
            poe_mods(vivo, False)
            if custo(vivo): F = carrega('ficha.json'); roda('ficha.py', 'fixo', 'despesa', F['livro']['despesa'] - custo(vivo), f"o Édito {c['nome']} revogado (−{custo(vivo)} por semana)")
            if dia - vivo.get('desde', dia) < 30:
                roda('reino.py', 'legit', '-2' if teto()[2] else '-1', f"o Édito {c['nome']} revogado antes de uma lua")
        vivo['estado'] = 'revogado'; vivo['revogado'] = dia; grava(ARQ, S)
        anota(f"- ÉDITO (G27) [Dia {dia}]: o Édito {c['nome']} REVOGADO"); print(f"REVOGADO: o Édito {c['nome']}. (A reputação que ele custou não volta sozinha.)"); return
    sys.exit(__doc__)


if __name__ == '__main__':
    main()
