#!/usr/bin/env python3
"""vila_teste.py — MOTOR 10: A VILA DE TESTE. Um mundo pequeno, FORA DO CÂNONE, para o jogador experimentar a luta, a caça, a forja e o custo de viver.

  python3 vila_teste.py PASTA [comeco=ferreiro|cacador|guerreiro] [nome=NOME] [semente=N]

Cria, numa pasta NOVA (recusa escrever por cima de qualquer coisa), tudo por eventos "gera":
  PEDRA RASA, uma vila de 400 pessoas: pousada, mercado (os bens no ponto do ano, 15 peças Comuns e Incomuns na prateleira, 2.000 de prata contada)
    e a forja da vila (oficina 1; o fogo e a bigorna servem até o Incomum);
  A MATA DO CORVO, o ermo vizinho, a 1 bloco: corça, javali, lobo e urso; UMA pantera (o bicho raro: dá matéria Rara) e UMA serpe (o chefe: dá núcleo Épico);
    madeira, erva e minério para tirar (o Raro, contado: 4 de minério e 2 de erva);
  OITO PESSOAS com nome e ficha de luta (o ferreiro, a taverneira, a caçadora, o guarda, o lenhador, a curandeira, o mercador, o aprendiz);
  e O PERSONAGEM do começo escolhido: nível 5, a mão de Iniciante no ofício dele, peças Comuns, 30 de prata.
Depois: MOTOR10_MUNDO=PASTA python3 turno.py abre      (o guia está no GUIA_VILA.md)
"""
import os, sys
import tabelas as T
import tabelas_mundo as M
import tabelas_bichos as TB
import estado, mercado, turno
from itens import item
from pessoas import padrao

VILA = dict(id='vila', nome='Pedra Rasa', em='em Pedra Rasa', pop=400, oficina=1, fogo=1, bigorna=1)
ERMO = dict(id='mata', nome='a Mata do Corvo', em='na Mata do Corvo', habitat='floresta', perigo=1, longe=1,
            bichos={'corça': 80, 'javali': 40, 'lobo': 12, 'urso': 3, 'pantera': 1, 'serpe': 1},                              # a pantera é o bicho raro; a serpe, o chefe (dá núcleo Épico)
            coleta={'madeira:0': 200, 'erva:0': 60, 'metal:0': 60, 'madeira:1': 20, 'erva:1': 10, 'metal:1': 8, 'metal:2': 4, 'erva:2': 2})        # o minério Raro é pouco e quase não volta
# quem tem nome: (id, nome, o que é, nível, molde, grau de ofício, maestria, prata, as peças: (tipo, família ou material, categoria, cobre, uso))
GENTE = [
    ('bento', 'Bento', 'o ferreiro da vila; conserta e vende o que forja', 28, 'guerreiro', 'oficial', {'forja': 4, 'martelo': 2}, 60,
     [('arma', 'martelo', 0, None, 'arma'), ('armadura', 'couro', 0, None, 'veste')]),
    ('dalva', 'Dalva', 'a taverneira da pousada; sabe de tudo o que se conta', 12, 'comum', 'oficial', {'comércio': 2, 'adaga': 2}, 80,
     [('arma', 'adaga', 0, None, 'arma')]),
    ('rute', 'Rute', 'a caçadora; conhece a Mata do Corvo', 22, 'arqueiro', 'aprendiz', {'arco': 4, 'caça': 4, 'adaga': 2}, 25,
     [('arma', 'arco', 1, None, 'arma'), ('arma', 'adaga', 0, None, 'arma2'), ('armadura', 'couro', 0, None, 'veste')]),
    ('tome', 'Tomé', 'o guarda da vila', 30, 'guerreiro', 'oficial', {'lança': 4, 'espada': 2}, 40,
     [('arma', 'lança', 1, None, 'arma'), ('escudo', None, 0, None, 'escudo'), ('armadura', 'malha', 0, None, 'veste'), ('armadura', 'malha', 0, ['cabeça'], 'veste')]),
    ('ivo', 'Ivo', 'o lenhador; tira madeira na borda da mata', 14, 'guerreiro', 'diarista', {'machado': 2, 'coleta': 2}, 12,
     [('arma', 'machado', 0, None, 'arma')]),
    ('nara', 'Nara', 'a curandeira; colhe erva e trata ferida', 16, 'comum', 'aprendiz', {'cura': 2, 'coleta': 2}, 30,
     [('arma', 'adaga', 0, None, 'arma')]),
    ('lino', 'Lino', 'o mercador da loja', 10, 'comum', 'oficial', {'comércio': 4}, 150, []),
    ('zeca', 'Zeca', 'o aprendiz da forja; novo, quer aprender', 3, 'comum', 'aprendiz', {}, 5, []),
]
# os começos: os atributos (a soma é a mesma: 340), a mão de Iniciante, o treino que a explica, o grau de ofício, as peças Comuns e a carga
COMECOS = dict(
    ferreiro=dict(sobre='ferreiro novo, com a mão de Iniciante na forja', atributos=dict(Força=65, Agilidade=50, Vigor=65, Vontade=50, Percepção=45, Afinidade=65), grau_oficio='aprendiz',
                  maestria={'forja': 2, 'martelo': 2}, treino={'forja': 50, 'martelo': 40}, marca={'prep_receita': 0}, carga={'metal:0': 4, 'madeira:0': 2},
                  pecas=[('arma', 'martelo', 0, None, 'arma'), ('armadura', 'couro', 0, None, 'veste')]),
    cacador=dict(sobre='caçador novo, com a mão de Iniciante no rastro e no arco', atributos=dict(Força=55, Agilidade=70, Vigor=60, Vontade=45, Percepção=70, Afinidade=40), grau_oficio='diarista',
                 maestria={'caça': 2, 'arco': 2}, treino={'caça': 40, 'arco': 40}, marca={}, carga={'comida': 2},
                 pecas=[('arma', 'arco', 0, None, 'arma'), ('arma', 'adaga', 0, None, 'arma2'), ('armadura', 'couro', 0, None, 'veste')]),
    guerreiro=dict(sobre='guerreiro novo, com a mão de Iniciante na espada', atributos=dict(Força=70, Agilidade=60, Vigor=70, Vontade=50, Percepção=50, Afinidade=40), grau_oficio='diarista',
                   maestria={'espada': 2}, treino={'espada': 40}, marca={}, carga={},
                   pecas=[('arma', 'espada', 0, None, 'arma'), ('escudo', None, 0, None, 'escudo'), ('armadura', 'malha', 0, None, 'veste')]),
)
NIVEL = 5
PRATA = 30
NOMES = dict(ferreiro='Aldo', cacador='Cira', guerreiro='Maro')


def _peca(tipo, qual, cat, cobre, de, dono):
    nome = dict(arma=qual, escudo='escudo').get(tipo) or ('elmo de ' + qual if cobre == ['cabeça'] else 'armadura de ' + qual)
    return item(tipo, cat, f"{nome.capitalize()} de {de}", familia=qual if tipo == 'arma' else None, material=qual if tipo == 'armadura' else None, cobre=cobre, dono=dono)


def _veste(E, pid, nome, pecas):
    """as peças de alguém nascem (um evento) e são postas em uso (outro)"""
    if not pecas: return
    s0 = E['itens']['seq']
    estado.aplica(E, 'gera', [['item', 'nasce', _peca(t, q, c, cb, nome, pid)] for t, q, c, cb, _ in pecas], onde=VILA['id'], quem=[pid], texto=f'as peças de {nome}')
    estado.aplica(E, 'gera', [['item', f'i{s0 + k + 1:04d}', 'uso', 'poe', uso] for k, (_, _, _, _, uso) in enumerate(pecas) if uso], onde=VILA['id'], quem=[pid], texto=f'{nome} se veste')


def cria(comeco='guerreiro', nome=None, semente=1):
    """o mundo da vila de teste, inteiro, por eventos "gera". Devolve o estado (quem chama grava)."""
    if comeco not in COMECOS: sys.exit(f'começo desconhecido: "{comeco}" (os que há: {", ".join(COMECOS)})')
    c = COMECOS[comeco]; nome = nome or NOMES[comeco]; E = estado.novo(semente); v, e = VILA, ERMO
    estado.aplica(E, 'gera', [['lugar', 'nasce', v['id'], dict(nome=v['nome'], em=v['em'], tipo='vila', cama=True, estoque={})],
                              ['lugar', 'nasce', e['id'], dict(nome=e['nome'], em=e['em'], tipo='ermo', habitat=e['habitat'], perigo=e['perigo'], longe=e['longe'], estoque={}, vizinhos=[v['id']],
                                                               teto=dict(e['bichos']), bichos=dict(e['bichos']), coleta_teto=dict(e['coleta']), coleta=dict(e['coleta']))],
                              ['lugar', v['id'], 'vizinhos', 'poe', [e['id']]]], texto=f"nascem {v['nome']} e {e['nome']} (a vila de teste, fora do cânone)")
    mercado.funda(E, v['id'], v['pop'], como='a feira e a loja da vila de teste')
    estado.aplica(E, 'gera', [['lugar', v['id'], 'oficina', 'poe', v['oficina']], ['lugar', v['id'], 'preparo.fogo', 'poe', v['fogo']], ['lugar', v['id'], 'preparo.bigorna', 'poe', v['bigorna']]],
                  onde=v['id'], texto=f"a forja de {v['nome']}: oficina {v['oficina']}; o fogo e a bigorna servem até o {T.CATS[v['fogo']]}")
    for pid, n, sobre, nivel, molde, grau, maestria, prata, pecas in GENTE:
        estado.aplica(E, 'gera', [['pessoa', 'nasce', pid, dict(nome=n, nivel=nivel, atributos=padrao(n, nivel, molde=molde)['atributos'], lugar=v['id'], grau_oficio=grau, maestria=dict(maestria), moedas=prata, sobre=sobre)]],
                      onde=v['id'], quem=[pid], texto=f'{n}, {sobre}')
        _veste(E, pid, n, pecas)
    estado.aplica(E, 'gera', [['pessoa', 'nasce', 'eu', dict(nome=nome, nivel=NIVEL, atributos=dict(c['atributos']), lugar=v['id'], grau_oficio=c['grau_oficio'], maestria=dict(c['maestria']), treino=dict(c['treino']),
                                                              marca=dict(c['marca']), carga=dict(c['carga']), moedas=PRATA, jogador=True, sobre=c['sobre'])]], onde=v['id'], quem=['eu'], texto=f"{nome}, {c['sobre']}: o personagem")
    _veste(E, 'eu', nome, c['pecas'])
    P = estado.valida(E)
    if P: sys.exit('A VILA DE TESTE NASCEU QUEBRADA (não foi gravada):\n  ' + '\n  '.join(P))
    return E


def resumo(E):
    v = E['lugares'][VILA['id']]; e = E['lugares'][ERMO['id']]; p = E['gente']['eu']; raro = [TB.ESPECIES[x]['nome'] for x in e['bichos'] if TB.ESPECIES[x]['cat'] >= 2 and not TB.ESPECIES[x]['chefe']]
    chefe = [TB.ESPECIES[x]['nome'] for x in e['bichos'] if TB.ESPECIES[x]['chefe']]
    return [f"{v['nome']}: {v['pop']} de povo, {v['estoque'].get('prata', 0)} de prata, {len(mercado.prateleira(E, VILA['id']))} peças na prateleira, pousada, forja (oficina {v['oficina']}).",
            f"{e['nome']}, a {e['longe']} bloco: " + ', '.join(f"{TB.ESPECIES[x]['nome']} {q}" for x, q in e['bichos'].items()) + f" (o raro: {', '.join(raro)}; o chefe: {', '.join(chefe)}); tira-se: " + ', '.join(e['coleta']) + '.',
            'Gente com nome: ' + ', '.join(f"{q['nome']} ({q['sobre'].split(';')[0]})" for k, q in E['gente'].items() if k != 'eu') + '.',
            f"O personagem: {p['nome']}, nível {p['nivel']}, {p['sobre']}; {p['moedas']} de prata; " + ', '.join(it['nome'] for it in E['itens']['itens'].values() if it.get('dono') == 'eu') + '.']


def main(a=None):
    a = sys.argv[1:] if a is None else list(a)
    op = dict(x.split('=', 1) for x in a if '=' in x); pos = [x for x in a if '=' not in x]
    if len(pos) != 1 or any(k not in ('comeco', 'nome', 'semente') for k in op): print(__doc__); return
    pasta = os.path.abspath(pos[0])
    if os.path.exists(pasta) and (not os.path.isdir(pasta) or os.listdir(pasta)): sys.exit(f'{pasta} já existe e não está vazia: não escrevo por cima. Escolha uma pasta nova.')
    if not op.get('semente', '1').isdigit(): sys.exit(f'semente= pede um número (veio "{op["semente"]}")')
    E = cria(op.get('comeco', 'guerreiro'), op.get('nome'), int(op.get('semente', 1)))
    os.makedirs(pasta, exist_ok=True); os.environ['MOTOR10_MUNDO'] = pasta
    estado.grava(E); turno.abre(E)
    open(os.path.join(pasta, 'LEIA.md'), 'w', encoding='utf-8').write(
        '# VILA DE TESTE (fora do cânone)\n\nEste save é um mundo pequeno, feito pelo `vila_teste.py` do Motor 10 para experimentar a luta, a caça, a forja e o custo de viver.\n'
        'Nada daqui vale para jogo nenhum. O guia está em `motor10/GUIA_VILA.md`.\n\n' + '\n'.join('- ' + x for x in resumo(E)) + '\n')
    print(f'A VILA DE TESTE nasceu em {pasta} (fora do cânone; {E["relogio"]["eventos"]} eventos "gera").\n')
    print('\n'.join(resumo(E)))
    print(f'\nPara jogar (de dentro de motor10/):\n  export MOTOR10_MUNDO={pasta}\n  python3 turno.py abre\nO guia: GUIA_VILA.md')


if __name__ == '__main__':
    main()
