#!/usr/bin/env python3
"""bichos.py — MOTOR 10: OS BICHOS. Um bicho é uma ficha de luta como qualquer outra.

O corpo é a ARMA (garra, presa, chifre, cauda, casco, ferrão) e a ARMADURA (pelo, escama, carapaça), com CATEGORIA, e a regra de
ouro vale igual: conta a diferença entre a arma de quem bate e a armadura de quem apanha. O corpo NÃO É PEÇA: não está no Livro de
Itens, não tem dono, não quebra, não ocupa sintonia. O TAMANHO mexe no PV, no alcance, no cerco, no corredor e na Defesa. Os TRAÇOS
são uma lista fechada que a luta roda. O bicho comum FOGE ferido; o encurralado e o chefe, não. O DESPOJO sai da tabela.
As regras estão no projeto/regras_bichos.md; os números, no tabelas_bichos.py; as provas, no provas.py (bloco OS BICHOS).

Uso em código (a caça usa isto):
  tabelas_bichos.ESPECIES[especie]         nome, cat, grau, tamanho, bando, despojo, nucleo, habitat (e o resto da ficha)
  bicho(especie, nome=None, **mais)        a pessoa pronta para o luta.nova (e para a lista "B" do cenário do ato.py luta)
  bando(especie, sorte, n=None)            a lista: quantos andam juntos sai da sorte (o acaso do mundo: estado.sorte(E, chave)); a espécie de alfa traz o líder
  despojo(especie, sorte)                  ({bem: quantidade}, o registro do núcleo ou None)
  ameaca(especie, n=None, arma=None, armadura=None)     a frase que o caçador lê ANTES da luta
  resumo(especie, n=None)                  a espécie numa linha curta · mesa(E): as linhas dos bichos para a MESA.md (sem contagem e sem chefes)
Uso de linha de comando (só olha: não rola dado de jogo nem mexe em save):
  python3 bichos.py lista                  as espécies, do grau F ao S
  python3 bichos.py ver ESPECIE            a ficha de luta, o despojo e a ameaça
  python3 bichos.py ameaca ESPECIE [N] [arma=CATEGORIA] [armadura=CATEGORIA]
  python3 bichos.py tracos                 os traços que a luta roda, e os tamanhos
  python3 bichos.py mede ESPECIE NIVEL CATEGORIA [N] [lutas=200] [arma=espada] [armadura=malha] [homens=1] [inicio=perto] [surpresa=bicho|homem]
                                           a régua: N bichos contra um homem daquele nível e conjunto, em lutas de ensaio
No cenário da luta (luta.py nova, ato.py luta nova), um bicho é {"nome": "lobo 1", "nivel": 0, "bicho": "lobo"} (a espécie
inteira sai da tabela), ou a pessoa que o bicho() devolve, tal qual.
"""
import math, random, sys
import tabelas as T
import tabelas_bichos as TB
from itens import item, cat_i

CORPO = ('cat', 'armas', 'couro', 'tamanho', 'tracos', 'coragem')        # o que é do corpo; o resto do que se passa em `mais` é da pessoa


def especie(e):
    if e not in TB.ESPECIES: sys.exit(f'espécie desconhecida: "{e}" (as que existem: {", ".join(TB.ESPECIES)})')
    return TB.ESPECIES[e]


def bicho(esp, nome=None, **mais):
    """a pessoa pronta para o luta.nova. `mais` muda o corpo (cat, armas, couro, tamanho, tracos, coragem) ou a pessoa
    (nivel, atributos, instinto, lider, moral, linha, pv, feridas...): serve ao Mestre para o bicho fora do comum, e às provas."""
    e = especie(esp)
    corpo = dict(especie=esp, cat=e['cat'], armas=list(e['armas']), couro=e['couro'], tamanho=e['tamanho'], tracos=list(e['tracos']), coragem=e['coragem'])
    for k in CORPO:
        if k in mais: corpo[k] = mais.pop(k)
    corpo['cat'] = cat_i(corpo['cat'])
    at = dict(e['atributos']); at.update(mais.pop('atributos', None) or {})
    p = dict(nome=nome or f"{e['artigo']} {e['nome']}", nivel=mais.pop('nivel', e['nivel']), atributos=at, maestria=mais.pop('instinto', e['instinto']), equip={}, moral=e['moral'], bicho=corpo)
    p.update(mais)
    return p


def bando(esp, sorte=None, n=None, primeiro=1, **mais):
    """os bichos que andam juntos, com nome cada um. Quantos: da sorte (um random.Random; o do mundo é o estado.sorte), ou n.
    Na espécie que segue um alfa, o primeiro é o líder: caído ele, o bando testa a coragem.
    primeiro: de que número os nomes partem (um segundo bando da mesma espécie na mesma luta parte de onde o outro parou, e não traz outro alfa)."""
    e = especie(esp); lo, hi = e['bando']
    if n is None: n = lo if lo == hi else (sorte or random.SystemRandom()).randint(lo, hi)
    if n == 1 and primeiro == 1: return [bicho(esp, **mais)]
    out = [bicho(esp, nome=f"{e['nome']} {i + primeiro}", **mais) for i in range(n)]
    if e['alfa'] and primeiro == 1: out[0]['nome'] = f"{e['artigo']} {e['nome']} alfa"; out[0]['lider'] = True
    return out


def despojo(esp, sorte=None):
    """o que o bicho morto rende: ({bem: quantidade}, o núcleo). A luta estraga: de cada bem sai de metade ao inteiro da tabela.
    O núcleo (só o chefe dá, sempre) é o registro pronto para o ['item', 'nasce', registro]: falta pôr o dono ou o lugar."""
    e = especie(esp); r = sorte or random.SystemRandom(); bens = {}
    for bem, q in e['despojo'].items():
        lo = max(1, math.ceil(q * TB.DESPOJO_MIN)); bens[bem] = lo if lo >= q else r.randint(lo, q)
    nucleo = item('nucleo', e['cat'], f"núcleo de {e['nome']}", de=esp) if e['nucleo'] else None
    return bens, nucleo


# ---------- a ameaça: o que o caçador lê antes da luta ----------
VEZES = {0: 'passa inteiro', 1: 'vale o triplo', 2: 'vale nove vezes', -1: 'vale um terço', -2: 'vale um nono'}
NO_COURO = dict(pelo='no pelo', escama='na escama', carapaça='na carapaça')


def _vezes(d): return VEZES.get(d, 'vale vinte e sete vezes ou mais' if d > 0 else 'quase não passa')
def _menos(x): return f'{x:+d}'.replace('-', '−')


def _tamanho_diz(t, fem):
    tam = TB.TAMANHOS[t]; m = TB.TAMANHOS['médio']; L = []; nele = 'nela' if fem else 'nele'
    if tam['defesa'] > 0: L.append(f"difícil de acertar: {_menos(tam['defesa'])} na Defesa")
    if tam['defesa'] < 0: L.append(f"fácil de acertar: {_menos(tam['defesa'])} na Defesa")
    if tam['alcance'] > 1: L.append(f"alcança {tam['alcance']} casas e bate primeiro em quem chega com arma mais curta")
    if tam['cerco'] != m['cerco']: L.append(f"{tam['cerco'][0]} batem {nele} de perto na mesma rodada")
    if tam['ocupa'] < 1: L.append('cabem dois numa vaga de corredor')
    if tam['ocupa'] > 1: L.append(f"toma {tam['ocupa']} vagas de um corredor; em lugar mais estreito, luta apertado")
    return (t[:-1] + 'a' if fem and t.endswith('o') else t) + (f" ({'; '.join(L)})" if L else '')


def ameaca(esp, n=None, arma=None, armadura=None):
    """a frase que o caçador lê ANTES da luta: o grau, o tamanho, o corpo, o que se sabe, se foge. Com n, quantos são;
    com a categoria da arma e da armadura de quem lê, a conta da regra de ouro já feita."""
    e = especie(esp); c = e['cat']; C = T.CATS[c]; lo, hi = e['bando']; fem = e['artigo'] == 'a'; dele = 'dela' if fem else 'dele'; so = 'sozinha' if fem else 'sozinho'; tam = TB.TAMANHOS[e['tamanho']]
    quantos = f'são {n}' if n and n > 1 else f'está {so}' if n == 1 else f'anda {so}' if hi == 1 else f'anda em bando de {lo} a {hi}' if lo > 1 else f'anda {so} ou em {hi}'
    if e['alfa'] and (n is None or n > 1): quantos += ', atrás de um alfa'
    L = [f"{e['nome'].upper()} · grau {e['grau']} ({C}): {TB.GRAU_DIZ[e['grau']]} · {_tamanho_diz(e['tamanho'], fem)} · {quantos}."]
    armas = e['armas'][0] if len(e['armas']) == 1 else ', '.join(e['armas'][:-1]) + ' e ' + e['armas'][-1]
    L.append(f"O corpo: {armas} de categoria {C}; {e['couro']} {C}, que vale como {TB.COUROS[e['couro']]}.")
    if e['tracos']: L.append('Traços: ' + '. '.join(f'{t.capitalize()}: {TB.TRACOS[t]}' for t in e['tracos']) + '.')
    if tam['ocupa'] < 1 and any(t in TB.PEDE_TAMANHO for t in e['tracos']):       # ninguém derruba nem agarra quem é maior que ele: o traço do bicho pequeno não pega gente
        L.append(f"Por ser pequen{'a' if fem else 'o'}, não derruba nem agarra gente: só quem é do tamanho {dele}.")
    if (n or hi) > 1:                                       # o bando: o grau fala de um só, e o cerco e o flanco são os de toda luta (tabelas.py)
        vaga = int(1 / tam['ocupa']); chegam = 'só um chega' if vaga <= 1 else f'só {vaga} chegam'
        L.append(f"Em bando: o grau é o de {'uma' if fem else 'um'} só. Até {T.CERCO} batem em você de perto na mesma rodada, e cada um que já bateu tira {T.FLANCO} da sua Defesa "
                 f"para o próximo (até {_menos(-T.FLANCO * T.FLANCO_MAX)}); num corredor de um, {chegam} de cada vez.")
    L.append(f"Sabe-se: {e['sabe']}.")
    if e['chefe']: L.append(f"É chefe: não foge, e {'morta' if fem else 'morto'} dá um núcleo {C}.")
    else: L.append(f"Ferid{'a' if fem else 'o'}, testa a coragem ({_menos(e['coragem'])}) e pode fugir; encurralad{'a' if fem else 'o'}, luta até o fim.")
    if arma is None and armadura is None:
        if c == 0: L.append(f"A conta: é Comum. Qualquer arma passa inteira {NO_COURO[e['couro']]} {dele}; o golpe {dele} passa inteiro em armadura Comum, vale um terço na Incomum, e o triplo em parte do corpo sem armadura.")
        else: L.append(f"A conta: arma abaixo de {C} {_vezes(-1)} {NO_COURO[e['couro']]} {dele} (duas abaixo, {_vezes(-2).replace('vale ', '')}); em armadura abaixo de {C}, o golpe {dele} {_vezes(1)}.")
    else:
        if arma is not None: a = cat_i(arma); L.append(f"A sua arma ({T.CATS[a]}) {NO_COURO[e['couro']]} {dele} ({C}): o golpe {_vezes(a - c)}.")
        if armadura is not None: a = cat_i(armadura); L.append(f"O golpe {dele} ({C}) na sua armadura ({T.CATS[a]}): {_vezes(c - a)}.")
    return ' '.join(L)


def _ordem(esp): e = TB.ESPECIES[esp]; return (e['cat'], TB.GRAUS.index(e['grau']), e['nivel'], esp)


def resumo(esp, n=None):
    """a espécie numa linha curta (para a MESA.md e para listas): o grau, a categoria, o tamanho, quantos andam juntos e os traços"""
    e = especie(esp); lo, hi = e['bando']; fem = e['artigo'] == 'a'; t = e['tamanho']
    quantos = f'{n}' if n else ('sozinha' if fem else 'sozinho') if hi == 1 else f'bando de {lo} a {hi}' if lo > 1 else f'de 1 a {hi}'
    return f"{e['nome']} (grau {e['grau']}, {T.CATS[e['cat']]}, {t[:-1] + 'a' if fem and t.endswith('o') else t}, {quantos}" + (': ' + ', '.join(e['tracos']) if e['tracos'] else '') + ')'


def mesa(E):
    """as linhas dos bichos para a MESA.md (que tem teto de tamanho): uma linha por lugar, o do personagem e os vizinhos, com o resumo de
    cada espécie contada ali. Sem a contagem (é do Mestre) e sem os CHEFES (onde há um núcleo não se sabe de graça: acha-se no rastro).
    A frase inteira de cada espécie é a ameaca(): o caçador a lê quando o bicho aparece."""
    import estado
    pid = estado.eu(E)
    if not pid: return []
    aqui = E['gente'][pid]['lugar']; L = []
    for lid in [aqui] + list(E['lugares'][aqui].get('vizinhos', [])):
        l = E['lugares'].get(lid) or {}
        esps = sorted((esp for esp, q in (l.get('bichos') or {}).items() if q > 0 and esp in TB.ESPECIES and not TB.ESPECIES[esp]['chefe']), key=_ordem)
        if esps: L.append(f"- **{l.get('nome', lid)}:** " + ' · '.join(resumo(esp) for esp in esps))
    return ['## Os bichos daqui (o que todo mundo sabe; a frase inteira: `bichos.py ameaca ESPECIE`)'] + L if L else []


# ---------- olhar ----------
def _lista():
    L = [f"{'espécie':<12}{'grau':<6}{'categoria':<11}{'tamanho':<9}{'bando':<8}{'traços':<34}onde vive"]
    for k, e in sorted(TB.ESPECIES.items(), key=lambda x: _ordem(x[0])):
        L.append(f"{k:<12}{e['grau']:<6}{T.CATS[e['cat']]:<11}{e['tamanho']:<9}{('%d' % e['bando'][0] if e['bando'][0] == e['bando'][1] else '%d a %d' % e['bando']):<8}{(', '.join(e['tracos']) or '—'):<34}{', '.join(e['habitat'])}"
                 + (' · CHEFE (dá núcleo)' if e['chefe'] else ''))
    return '\n'.join(L)


def _ver(esp):
    from pessoas import ficha, linha
    e = especie(esp)
    return '\n'.join([linha(ficha(bicho(esp))), '  despojo (o bicho inteiro): ' + ' · '.join(f'{q} de {b}' for b, q in e['despojo'].items()) + (f" · e um núcleo {T.CATS[e['cat']]}" if e['nucleo'] else ''),
                      '  onde vive: ' + ', '.join(e['habitat']), '', ameaca(esp)])


def _tracos():
    L = ['OS TRAÇOS (a lista é fechada: só entra o que a luta roda)'] + [f'  {k:<10} {v}' for k, v in TB.TRACOS.items()]
    L += ['', 'OS TAMANHOS'] + [f"  {k:<8} PV × {t['pv']:g} · alcança {t['alcance']} casa(s) · cerco {t['cerco'][0]} de perto e {t['cerco'][1]} de haste · toma {t['ocupa']:g} de um corredor · Defesa {_menos(t['defesa'])}" for k, t in TB.TAMANHOS.items()]
    L += ['', 'O CORPO: A ARMA'] + [f"  {k:<8} {a['dado']} ({a['golpe']}), {a['folego']} de fôlego por golpe" for k, a in TB.ARMAS_CORPO.items()]
    L += ['', 'O CORPO: A ARMADURA'] + [f'  {k:<9} vale como {v}' for k, v in TB.COUROS.items()]
    return '\n'.join(L)


def _inicio(x):
    """o começo da luta para a régua: longe, perto ou colado"""
    if x not in T.INICIO: sys.exit(f'início desconhecido: "{x}" (use: {", ".join(T.INICIO)})')
    return x


def mede(esp, nivel, cat, n=None, lutas=200, familia='espada', material='malha', quantos=1, **kw):
    """a régua: lutas de ENSAIO (dado de mentira, com semente; nada é guardado) de n bichos contra um homem daquele nível (ou `quantos`
    homens iguais), com a arma (espada, se não se disser outra), a armadura (malha) e o escudo (se a arma é de uma mão) da categoria.
    O arqueiro e o besteiro levam uma adaga de reserva. Devolve um dicionário: rodadas (a mediana) e, em % das lutas: vence · perde ·
    carcaca (venceu e ficou bicho morto ou caído no campo) · fugiu (venceu só porque todos fugiram) · ferido (o primeiro homem saiu
    com ferida nova, caído ou morto) · caiu (o primeiro homem caiu ou morreu)."""
    import luta
    from pessoas import padrao, veste
    if familia not in T.FAMILIAS or familia == 'punho': sys.exit(f'arma desconhecida: "{familia}" (use: {", ".join(f for f in T.FAMILIAS if f != "punho")})')
    if material not in T.MATERIAIS: sys.exit(f'armadura desconhecida: "{material}" (use: {", ".join(T.MATERIAIS)})')
    c = cat_i(cat); F = T.FAMILIAS[familia]; tiro = bool(F.get('distancia')); guarda = luta.D; luta.semente(1); rs = []; m = dict(vence=0, perde=0, carcaca=0, fugiu=0, ferido=0, caiu=0)
    homem = lambda k: veste(padrao('o caçador' if quantos == 1 else f'caçador {k + 1}', nivel, molde='arqueiro' if tiro else 'guerreiro'), arma=(familia, c), armadura=(material, c),
                            escudo=c if F['maos'] == 1 else None, arma2=('adaga', c) if tiro else None)
    try:
        for i in range(lutas):
            S = luta.nova([homem(k) for k in range(quantos)], bando(esp, random.Random(i), n=n), quieto=True, **kw); luta.corre(S); h = S['L'][0]; bs = [f for f in S['L'] if f['lado'] == 'B']
            m['vence'] += S['fim'] == 'A'; m['perde'] += S['fim'] == 'B'; rs.append(S['r'])
            m['carcaca'] += S['fim'] == 'A' and any(f['estado'] in ('morto', 'caido') for f in bs); m['fugiu'] += S['fim'] == 'A' and all(f['estado'] == 'fugiu' for f in bs)
            m['caiu'] += h['estado'] in ('morto', 'caido'); m['ferido'] += h['estado'] in ('morto', 'caido') or len(h['feridas']) > h['feridas_antes']
    finally: luta.D = guarda
    rs.sort(); m = {k: round(100 * v / lutas) for k, v in m.items()}; m['rodadas'] = rs[len(rs) // 2]
    return m


def _chave(x):
    """a espécie pelo nome da tabela ou pelo nome que vai à mesa ("aranha" ou "aranha-de-toca")"""
    return next((k for k, d in TB.ESPECIES.items() if x in (k, d['nome'])), x)


if __name__ == '__main__':
    a = sys.argv[1:]; op = dict(x.split('=', 1) for x in a if '=' in x); pos = [x for x in a if '=' not in x]
    if len(pos) > 1: pos[1] = _chave(pos[1])
    num = lambda x, que: int(x) if x.isdigit() and int(x) >= 1 else sys.exit(f'{que}: um número de 1 para cima (veio "{x}")')
    if pos == ['lista']: print(_lista())
    elif pos == ['tracos']: print(_tracos())
    elif pos[:1] == ['ver'] and len(pos) == 2: print(_ver(pos[1]))
    elif pos[:1] == ['ameaca'] and len(pos) in (2, 3): print(ameaca(pos[1], n=num(pos[2], 'quantos são') if len(pos) > 2 else None, arma=op.get('arma'), armadura=op.get('armadura')))
    elif pos[:1] == ['mede'] and len(pos) in (4, 5):
        especie(pos[1]); n = num(pos[4], 'quantos bichos') if len(pos) > 4 else None; fam = op.get('arma', 'espada'); mat = op.get('armadura', 'malha'); q = num(op.get('homens', '1'), 'quantos homens')
        sp = op.get('surpresa'); sp in (None, 'bicho', 'homem') or sys.exit(f'a surpresa diz quem foi surpreendido: bicho ou homem (veio "{sp}")')
        m = mede(pos[1], num(pos[2], 'o nível'), pos[3], n=n, lutas=num(op.get('lutas', '200'), 'quantas lutas'), familia=fam, material=mat, quantos=q, inicio=_inicio(op.get('inicio', 'perto')),
                 surpresa={'bicho': 'B', 'homem': 'A'}.get(sp))
        print(f"ENSAIO (não é a luta de verdade: dado de mentira, nada é guardado): {'um homem' if q == 1 else f'{q} homens'} de nível {pos[2]}, de {fam}, {mat}"
              f"{' e escudo' if T.FAMILIAS[fam]['maos'] == 1 else ''} {T.CATS[cat_i(pos[3])]}, contra {TB.ESPECIES[pos[1]]['nome']} ({f'{n} de uma vez' if n else 'quantos a sorte der, pelo bando da espécie'}), começando {op.get('inicio', 'perto')}{f', o {sp} surpreendido' if sp else ''}:\n"
              f"  vence {m['vence']}% (em {m['carcaca']}% fica bicho morto ou caído no campo; em {m['fugiu']}% todos fogem) · perde {m['perde']}% · mediana de {m['rodadas']} rodadas\n"
              f"  {'o homem' if q == 1 else 'o primeiro homem'} sai com ferida nova, caído ou morto em {m['ferido']}% das lutas (caído ou morto: {m['caiu']}%)")
    else: print(__doc__)
