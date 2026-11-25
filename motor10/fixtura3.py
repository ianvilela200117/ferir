#!/usr/bin/env python3
"""fixtura3.py — MOTOR 10, etapa 3: A REGIÃO PEQUENA DE PROVA (para as quatro frentes testarem antes de o gerador de A1 existir).

Em volta da vila de teste com a magia e a 4b (Pedra Rasa, a Mata do Corvo, a Cova Velha e a cripta, Vau Seco, a Serra Fria e o Tição), só por eventos "gera":
  3 povoados novos: Telhal Alto (cidade, 1.500: a forja de cidade, a mesa de runas, a botica e o santuário), Ribanceira (vila, 400) e Cerro Manso (aldeia, 120);
  1 ermo novo: o Charco do Cerro (brejo, a borda), vizinho de Cerro Manso;
  3 rotas: Pedra Rasa a Telhal Alto (estrada, 3 blocos, passa perto da Mata do Corvo), Pedra Rasa a Cerro Manso (caminho, 2 blocos, cruza o Charco),
           Telhal Alto a Ribanceira (caminho, 4 blocos, campo aberto);
  a bolsa do povo (5 de prata por pessoa) em Pedra Rasa e nos três povoados novos; a posição de cada um no mapa;
  6 pessoas de papel: Bento (ferreiro), Dalva (taverneiro) e Tomé (guarda), de Pedra Rasa; e três novas, Ilmara Tojal (encantador, em Telhal Alto),
  Belmiro Sarça (mercador, em Ribanceira) e Odília Penedo (alcaide, em Cerro Manso).
A prata nova (a dos povoados, das bolsas e da gente nova) nasce nos eventos do gerador; depois só muda de mão. O relógio não anda. Recusa rodar duas vezes.
Não é o gerador da região (que é da frente A1): é uma planta fixa, pequena, para o banco.

  python3 fixtura3.py PASTA [semente=N]       cria a vila de teste com a região pequena numa pasta nova (fora do ensaio/)
  import fixtura3; E = fixtura3.cria(semente)  o mesmo, em memória (o banco); fixtura3.poe(E) põe a região num mundo que já tem a vila de teste
"""
import os, sys
import estado, vila_teste, mercado, caca

LUGARES = [   # id, nome, em, tipo, povo, posição, bancadas
    ('telhal', 'Telhal Alto', 'em Telhal Alto', 'cidade', 1500, [34, 40], dict(oficina=2, runas=1, botica=1, santuario=1, preparo=dict(fogo=2, bigorna=2))),
    ('ribanceira', 'Ribanceira', 'na Ribanceira', 'vila', 400, [52, 22], dict(oficina=1, botica=1, preparo=dict(fogo=1, bigorna=1))),
    ('cerro', 'Cerro Manso', 'em Cerro Manso', 'aldeia', 120, [12, 58], dict(oficina=0)),
]
POS_VILA = [14, 40]
ERMO = ('charco', 'o Charco do Cerro', 'no Charco do Cerro', 'brejo', [10, 66], 'cerro')
ROTAS = [   # id, a, b, blocos, tipo, ermo, expoe
    ('r_vila_telhal', 'vila', 'telhal', 3, 'estrada', 'mata', 0.3),
    ('r_vila_cerro', 'vila', 'cerro', 2, 'caminho', 'charco', 1),
    ('r_telhal_ribanceira', 'telhal', 'ribanceira', 4, 'caminho', None, 1),
]
PAPEL_VILA = dict(bento='ferreiro', dalva='taverneiro', tome='guarda')
GENTE = [   # id, nome, onde, papel, grau, nível, prata, atributos
    ('ilmara', 'Ilmara Tojal', 'telhal', 'encantador', 'oficial', 8, 60, dict(Força=40, Agilidade=50, Vigor=45, Vontade=65, Percepção=55, Afinidade=70)),
    ('belmiro', 'Belmiro Sarça', 'ribanceira', 'mercador', 'oficial', 6, 150, dict(Força=45, Agilidade=50, Vigor=50, Vontade=55, Percepção=60, Afinidade=40)),
    ('odilia', 'Odília Penedo', 'cerro', 'alcaide', 'aprendiz', 7, 30, dict(Força=55, Agilidade=50, Vigor=60, Vontade=60, Percepção=50, Afinidade=35)),
]
BOLSA_CABECA = 5


def ja_tem(E): return bool(E.get('rotas')) or any(l in E['lugares'] for l, *_ in LUGARES)


def poe(E):
    """a região pequena, por eventos "gera", em volta da vila de teste que já existe (com a magia e a 4b). Devolve as linhas que contam o que pôs. Recusa rodar duas vezes."""
    if ja_tem(E): sys.exit('a região pequena já está neste mundo (ou ele já tem rotas): não se põe por cima')
    if 'vila' not in E['lugares'] or 'mata' not in E['lugares']: sys.exit('a região pequena nasce em volta da vila de teste (Pedra Rasa e a Mata do Corvo)')
    estado.sem_luta(E); L = []; estado.padroes(E)
    ef = [['lugar', 'nasce', lid, dict(nome=nome, em=em, tipo=tipo, cama=tipo != 'aldeia', pos=pos, **banc)] for lid, nome, em, tipo, pop, pos, banc in LUGARES]
    ef.append(['lugar', 'nasce', ERMO[0], dict(nome=ERMO[1], em=ERMO[2], tipo='ermo', pos=ERMO[4])])
    estado.aplica(E, 'gera', ef, texto='a região pequena de prova: os povoados e o ermo nascem')
    for lid, nome, em, tipo, pop, pos, banc in LUGARES:
        mercado.funda(E, lid, pop, prateleira_=tipo != 'aldeia', como='a região pequena de prova')
    caca.povoa(E, ERMO[0], ERMO[3], 1, vizinho=ERMO[5], como='a região pequena de prova')
    ef = [['lugar', 'vila', 'pos', 'poe', POS_VILA], ['lugar', 'vila', 'bolsa', 'poe', round((E['lugares']['vila'].get('pop') or 0) * BOLSA_CABECA)]]
    ef += [['lugar', lid, 'bolsa', 'poe', pop * BOLSA_CABECA] for lid, nome, em, tipo, pop, pos, banc in LUGARES]
    ef += [['rota', 'nasce', rid, dict(a=a, b=b, blocos=bl, tipo=t, ermo=er, expoe=ex)] for rid, a, b, bl, t, er, ex in ROTAS]
    estado.aplica(E, 'gera', ef, texto='a região pequena de prova: as rotas, as bolsas do povo e o mapa')
    ef = [['pessoa', k, 'papel', 'poe', v] for k, v in PAPEL_VILA.items() if k in E['gente']]
    ef += [['pessoa', 'nasce', pid, dict(nome=nome, nivel=nv, atributos=at, lugar=onde, mora=onde, papel=papel, grau_oficio=grau, moedas=prata)] for pid, nome, onde, papel, grau, nv, prata, at in GENTE]
    estado.aplica(E, 'gera', ef, texto='a região pequena de prova: a gente de papel')
    L.append(f"a região pequena: {', '.join(n for _, n, *_ in LUGARES)} e {ERMO[1]}; {len(ROTAS)} rotas; a bolsa do povo em Pedra Rasa e nos povoados novos; "
             f"{len(PAPEL_VILA) + len(GENTE)} pessoas de papel ({', '.join(E['gente'][k]['nome'] for k in list(PAPEL_VILA) + [g[0] for g in GENTE] if k in E['gente'])})")
    return L


def cria(semente=3, inclinacao='forja', inclinacao2='encanto'):
    """a vila de teste do ferreiro (com a magia e a 4b) e a região pequena em volta, em memória (nada gravado)"""
    E = vila_teste.cria('ferreiro', semente=semente, talentos=True, inclinacao=inclinacao, inclinacao2=inclinacao2)
    vila_teste.magia(E); vila_teste.fantasia(E); poe(E)
    return E


if __name__ == '__main__':
    a = [x for x in sys.argv[1:] if '=' not in x]; op = dict(x.split('=', 1) for x in sys.argv[1:] if '=' in x)
    if len(a) != 1: print(__doc__); sys.exit()
    os.environ['MOTOR10_MUNDO'] = os.path.abspath(a[0])
    if os.path.basename(os.path.normpath(a[0])) == 'ensaio': sys.exit('a pasta ensaio/ é o save do jogador: a região pequena nasce numa pasta nova')
    if os.path.exists(os.path.join(estado.pasta(), 'relogio.json')): sys.exit(f'já há um mundo em {estado.pasta()}: não escrevo por cima.')
    E = vila_teste.cria('ferreiro', semente=int(op.get('semente', 3)), talentos=True, inclinacao='forja', inclinacao2='encanto')
    vila_teste.magia(E); vila_teste.fantasia(E); L = poe(E); estado.grava(E)
    print(f'a vila de teste com a região pequena nasceu em {estado.pasta()}: ' + ' '.join(L))
