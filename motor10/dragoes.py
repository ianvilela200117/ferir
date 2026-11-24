#!/usr/bin/env python3
"""dragoes.py — MOTOR 10, ETAPA 4b: OS DRAGÕES (capítulo 20; os números no tabelas_dragoes.py; o contrato: projeto/ETAPA_4B.md, seções 2, 9 e 12).

  TRÊS TIPOS, pelo lugar onde vivem (nada de cor): o DRAGÃO DA SERRA (voa e sopra fogo), o VERME DO BREJO (sem asas; o golpe envenena; luta na água) e o DRAGÃO DAS
  GRUTAS (sem asas; o escuro não lhe tira nada; prende quem está colado). CINCO IDADES: o filhote (grau D, Incomum), o jovem (C, Raro), o adulto (B, Épico), o velho
  (A, Único) e o ancião (S, Lendário). O dragão é um bicho: a luta o roda com os traços que já tem (sopro, voa, apavora, couraça, resiste, veneno, agarra, noturno).
  O FILHOTE testa a coragem e foge ferido, como bicho. Do JOVEM para cima é chefe: a moral é firme, e só a FASE o tira da luta. A fase, abaixo de uma fração do PV:
  o da serra, no covil, desce ao chão em fúria (deixa de voar; quem o golpeia de perto se queima) e, FORA DO COVIL, FOGE PELO AR (E3 a): volta ao covil com o PV que
  tinha, dorme até sarar e lembra de quem o feriu; o do brejo enrosca na lama (prende); o das grutas bebe o sangue de quem prende. NO COVIL (quem monta a luta põe
  sem_saida do lado dele) luta até morrer, defendendo o ouro. MORTO, dá o corpo (couro e osso; a peçonha do verme) e, do adulto para cima, o CORAÇÃO: o núcleo da
  categoria dele, com o nome dele. O dragão morto não volta, e o dragão não cria (não há ovo nesta etapa).
  O COVIL é uma sala de masmorra de molde covil (ou um ermo) com o registro `dragao`. O TESOURO é o estoque do lugar e as peças guardadas nele: prata que já existe,
  posta pelo gerador (nada novo cria prata). Quem fica com o campo leva o tesouro: a prata e os bens em partes iguais, as peças com quem comanda.
  A VIDA DO DRAGÃO (evento "dragão", todo dia, o mundo sozinho): dorme semanas, e o ferido sara dormindo; acordado, o jovem ataca a vila dele de noite (o gado, um
  pouco de prata para o tesouro, às vezes um morto) e volta a dormir; do adulto para cima cobra o tributo da estação, e só ataca quem não paga. O filhote caça no ermo.
  O ROUBO DE QUEM DORME: cada punhado (a sexta parte da prata que havia quando ele adormeceu; acabada a prata, uma peça) é um teste de andar escondido (o do ladino)
  contra a VIGÍLIA dele: 20 + Percepção ÷ 10 + 2 (dorme leve sobre o ouro), e mais 2 a cada punhado já tirado no mesmo sono. Falhou: ele acorda, e não é surpreendido.
  O QUE SE CONTA: a gente de um lugar sabe dos dragões que a fama dela alcança (o boato do último ataque, sem número). O registro inteiro é do SÓ O MESTRE.

Uso em código (o que as outras frentes chamam; nada grava sozinho, a não ser virada, na_vila e o comando):
  especie(tipo, idade) · dragao(tipo, idade, nome=None, **mais) · de(E, lid) · pv(E, lid) · pv_max(tipo, idade) · covis(E) · guardadas(E, lid)
  idade_da_cat(cat) · tipo_do_lugar(habitat) · tesouro_teto(E, idade)      (para quem gera o covil: a idade da categoria, o tipo do lugar, o teto do tesouro)
  monta(E, lid) → ({"bicho", "nome", "pv", "lider"}, dorme) · acordado(E, lid) · vigilia(E, lid) · punhado(E, lid, pid) → (efeitos, texto) · acorda(E, lid) → efeitos
  depois_da_luta(E, lid, S, campo, quem) → (efeitos, {pessoa: {bem: quanto}}, linhas) · poe(E, lid, tipo, idade, nome, vila=None, tesouro=0, dorme=0) → efeitos
  ameaca(tipo, idade, arma=None, armadura=None) · cena_em_casa(tipo, covil=True) (o tempo da casa e o sem saída do covil, para o cenário) · homem(...) · mede(...)
  virada(E) · mesa(E) · so_mestre(E) · na_vila(E, vila='vila')
Uso de linha de comando (o que só olha não rola dado de jogo nem mexe em save):
  python3 dragoes.py lista                                  os 15 dragões (os 3 tipos nas 5 idades)
  python3 dragoes.py ver TIPO IDADE                         a ficha de luta, o despojo, o núcleo e a ameaça
  python3 dragoes.py ameaca TIPO IDADE [arma=CAT] [armadura=CAT]       a frase que o Mestre lê quando a cena põe o dragão à frente
  python3 dragoes.py mede TIPO IDADE NIVEL CATEGORIA [homens=4] [lutas=200] [covil=sim|nao] [dorme=sim] [arma=CAT] [armadura=CAT]
                                                            a régua: lutas de ensaio (dado de mentira, nada é guardado) contra homens de espada, malha e escudo
  python3 dragoes.py covil [LUGAR]                          SÓ O MESTRE: o dragão, o sono, o PV, o tesouro, a vila, a vigília
  python3 dragoes.py covil poe LUGAR TIPO IDADE "Nome" [vila=LUGAR] [tesouro=N] [dorme=DIAS]       o Mestre funda um covil (evento "mestre": segredo)
  (TIPO: serra, brejo, grutas · IDADE: filhote, jovem, adulto, velho, ancião)
No cenário da luta: {"bicho": "dragão-da-serra-jovem", "nome": "o Tição", "pv": 350, "lider": true} (o que o monta devolve), e no covil o lugar {"sem_saida": "B"}.
"""
import math, random, sys
import tabelas as T
import tabelas_bichos as TB
import tabelas_dragoes as TD
import tabelas_mundo as M
import estado

EVENTO = 'dragão'
_num = lambda v: isinstance(v, (int, float)) and not isinstance(v, bool)
_int = lambda v: isinstance(v, int) and not isinstance(v, bool)


# ---------- a espécie ----------
def especie(tipo, idade):
    """a chave da espécie de um dragão: 'dragão-da-serra-jovem', 'verme-do-brejo-filhote'..."""
    if tipo not in TD.TIPOS or idade not in TD.IDADES: sys.exit(f'dragão desconhecido: "{tipo} {idade}" (os tipos: {", ".join(TD.TIPOS)}; as idades: {", ".join(TD.IDADES)})')
    return TD.chave(tipo, idade)


def dragao(tipo, idade, nome=None, **mais):
    """o lutador pronto para o luta.nova (como bichos.bicho): o corpo da tabela, com o nome que vier"""
    import bichos
    return bichos.bicho(especie(tipo, idade), nome=nome, **mais)


def pv_max(tipo, idade):
    """o PV cheio do dragão daquela espécie (a conta da ficha de bicho: o PV do Vigor e do nível, vezes o tamanho)"""
    e = TD.ESPECIES[especie(tipo, idade)]
    return int(T.pv_max(e['atributos']['Vigor'], e['nivel']) * TB.TAMANHOS[e['tamanho']]['pv'])


def _esp(d):
    """o registro da espécie do dragão de um lugar, ou None"""
    if not isinstance(d, dict) or d.get('tipo') not in TD.TIPOS or d.get('idade') not in TD.IDADES: return None
    return TD.ESPECIES.get(TD.chave(d['tipo'], d['idade']))


def de(E, lid):
    """o registro do dragão que mora no lugar, ou None"""
    d = (E['lugares'].get(lid) or {}).get('dragao') if isinstance(lid, str) else None
    return d if isinstance(d, dict) else None


def pv(E, lid):
    """o PV de agora do dragão do lugar (sem o campo: cheio), ou None"""
    d = de(E, lid)
    if not _esp(d): return None
    mx = pv_max(d['tipo'], d['idade'])
    return min(d['pv'], mx) if _int(d.get('pv')) else mx


def idade_da_cat(cat):
    """a idade do dragão de uma categoria (o covil de uma masmorra daquela categoria): 1 o filhote, 2 o jovem, 3 o adulto, 4 o velho, 5 o ancião; None fora disso"""
    return next((i for i, x in TD.IDADES.items() if x['cat'] == cat), None)


def tipo_do_lugar(habitat):
    """o tipo de dragão que vive num lugar (o habitat do ermo): serra, brejo ou grutas; o fundo da masmorra (sem habitat que case) é das grutas"""
    return next((t for t, x in TD.TIPOS.items() if habitat in x['habitat']), 'grutas')


def tesouro_teto(E, idade):
    """o teto da prata do tesouro de um dragão daquela idade, na conta da prata do mundo de agora (tabelas_dragoes.TESOURO); o filhote não junta tesouro"""
    import mercado
    t = TD.TESOURO.get(idade)
    return int(t[0] * mercado.prata_do_mundo(E)) if t else 0


def covis(E):
    """[(lugar, registro do dragão)] de todos os dragões do mundo, na ordem dos lugares"""
    return [(lid, l['dragao']) for lid, l in sorted(E['lugares'].items()) if isinstance(l, dict) and _esp(l.get('dragao'))]


def _diz(d):
    """'o Tição, dragão jovem da serra'"""
    e = _esp(d); return f"{d['nome']}, {e['nome']}" if e else d.get('nome', 'o dragão')


def _e(xs):
    xs = [str(x) for x in xs if x]; return ' e '.join(xs) if len(xs) < 3 else ', '.join(xs[:-1]) + ' e ' + xs[-1]


def _prata(E, lid):
    v = (E['lugares'][lid].get('estoque') or {}).get('prata', 0)
    return int(v) if _num(v) else 0


def guardadas(E, lid):
    """as peças do tesouro: no lugar, sem dono e não soltas (a peça solta é de quem achar; a de um morto fica com o corpo)"""
    return sorted((it for it in E['itens']['itens'].values() if it.get('onde') == lid and not it.get('dono') and not it.get('solto')), key=lambda it: it['id'])


# ---------- o sono e a luta ----------
def acordado(E, lid):
    """o dragão do lugar está acordado? (sem dragão: não)"""
    d = de(E, lid)
    return bool(d) and not (_int(d.get('dorme_ate')) and d['dorme_ate'] > E['relogio']['dia'])


def monta(E, lid):
    """(a pessoa em forma curta para o cenário da luta, dorme) do dragão do lugar: {"bicho": CHAVE, "nome": ..., "pv": ..., "lider": true}; ou None se não há dragão.
    O PV é o de agora (o ferido entra ferido). A moral é a da espécie: o filhote testa a coragem; do jovem para cima, firme (só a fase o tira da luta)."""
    d = de(E, lid)
    if not _esp(d): return None
    p = dict(bicho=TD.chave(d['tipo'], d['idade']), nome=d['nome'], lider=True)
    if _int(d.get('pv')) and d['pv'] < pv_max(d['tipo'], d['idade']): p['pv'] = d['pv']
    return p, not acordado(E, lid)


def vigilia(E, lid):
    """o número contra o qual o ladrão anda escondido na câmara do dragão que dorme: 20 + Percepção ÷ 10 + 2 (dorme leve sobre o ouro), mais 2 a cada punhado tirado
    no mesmo sono. None se não há dragão ou se ele está acordado (acordado, ninguém rouba: o ladrão é visto)."""
    d = de(E, lid); e = _esp(d)
    if not e or acordado(E, lid): return None
    V = TD.VIGILIA
    return V['base'] + e['atributos']['Percepção'] // 10 + V['leve'] + V['sobe'] * max(0, int(d.get('punhados') or 0))


def punhado(E, lid, pid):
    """(efeitos, texto): o punhado que a pessoa tira do tesouro do dragão que dorme (quem chama já passou o teste contra a vigília). É a sexta parte da prata que havia
    quando ele adormeceu (no máximo o que resta); acabada a prata, uma peça guardada (a que a mão alcança: o acaso do mundo). O punhado conta no sono (a vigília sobe)."""
    d = de(E, lid)
    if not _esp(d): return [], ''
    nome = (E['gente'].get(pid) or {}).get('nome', pid); dia = E['relogio']['dia']
    base = d.get('prata_sono') if _int(d.get('prata_sono')) and d['prata_sono'] >= 0 else _prata(E, lid)
    q = min(_prata(E, lid), math.ceil(base / TD.PUNHADO)) if base > 0 else 0
    n = max(0, int(d.get('punhados') or 0)) + 1; conta = ['lugar', lid, 'dragao.punhados', 'poe', n]
    if q >= 1:
        return [conta, ['estoque', lid, 'prata', 'soma', -q], ['pessoa', pid, 'moedas', 'soma', q]], f"{nome} pega um punhado do tesouro: {q} de prata. {d['nome'].capitalize()} segue dormindo."
    gs = guardadas(E, lid)
    if gs:
        it = gs[0] if len(gs) == 1 else estado.sorte(E, f'dragão|{lid}|punhado|{n}').choice(gs)
        return [conta, ['item', it['id'], 'dono', 'poe', pid], ['item', it['id'], 'historia', 'junta', f"Dia {dia}: tirada do tesouro {estado.de_nome(d['nome'])} por {nome}, com ele dormindo"]], \
            f"{nome} pega {it['nome']} do tesouro. {d['nome'].capitalize()} segue dormindo."
    return [], 'O tesouro está vazio: não há o que pegar.'


def acorda(E, lid):
    """os efeitos de acordar o dragão (o ladrão falhou, ou o barulho): acordado, os punhados do sono não contam mais"""
    d = de(E, lid)
    if not _esp(d) or acordado(E, lid): return []
    novo = {k: v for k, v in d.items() if k != 'prata_sono'}; novo.update(dorme_ate=None, punhados=0)
    return [['lugar', lid, 'dragao', 'poe', novo]]


def _dorme(d, dias, prata, dia):
    """o registro de quem vai dormir: até quando, a prata do tesouro ao adormecer (a conta do punhado), os punhados zerados"""
    novo = dict(d); novo.update(dorme_ate=dia + max(1, int(dias)), punhados=0, prata_sono=max(0, int(prata)))
    return novo


def _sarar(pv_, mx):
    """os dias de sono para sarar do PV de agora ao cheio (SARA_DORMINDO do PV por dia)"""
    return max(TD.SARA_MIN, math.ceil((mx - pv_) / max(1, math.ceil(mx * TD.SARA_DORMINDO))))


def depois_da_luta(E, lid, S, campo, quem):
    """as contas da luta com o dragão do lugar (quem chama põe os efeitos no evento dele), como o criaturas.depois_da_luta. Devolve (efeitos, {pessoa: {bem: quanto}}, linhas).
    MORTO (ou caído e quem lutou ficou com o campo): sai do registro; o corpo (o despojo pela categoria dele) e o tesouro (a prata e os bens do estoque) vão em partes
    iguais para quem ficou com o campo (`quem`, quem comanda primeiro), as peças guardadas e o coração (o núcleo, do adulto para cima) com quem comanda; sem ninguém
    com o campo, o coração fica no chão, solto. FUGIU (a fase do que voa, fora do covil): o PV de agora volta ao registro, ele dorme até sarar e lembra de quem o
    feriu. VIVO (o grupo largou o campo): o PV volta ao registro, e ele fica acordado."""
    import bichos
    from itens import item
    d = de(E, lid); e = _esp(d)
    if not e: return [], {}, []
    k = TD.chave(d['tipo'], d['idade'])
    f = next((x for x in S['L'] if x['lado'] == 'B' and x['nome'] == d['nome']), None) or next((x for x in S['L'] if x['lado'] == 'B' and k in (x.get('bicho'), x.get('povo'))), None)
    if f is None: return [], {}, []
    dia = E['relogio']['dia']; mx = pv_max(d['tipo'], d['idade']); quem = [c for c in (quem or []) if c in E['gente'] and E['gente'][c].get('estado') == 'vivo']
    ef = []; partes = {}; L = []; nome = d['nome']; Nome = nome[:1].upper() + nome[1:]
    feriu = list(dict.fromkeys(list(d.get('feriu') or []) + [x['id'] for x in S['L'] if x['lado'] == 'A' and x.get('id') in E['gente']]))[-TD.FERIU_MAX:]
    if f['estado'] == 'morto' or (campo and f['estado'] in ('caido', 'rendido')):
        ef.append(['lugar', lid, 'dragao', 'poe', None]); c = f.get('cat_corpo') if _int(f.get('cat_corpo')) else e['cat']
        leva = quem[0] if campo and quem else None
        bens, _ = bichos.despojo(k, estado.sorte(E, f'dragão|{lid}|corpo'), cat=c)
        est = {b: int(q) for b, q in (E['lugares'][lid].get('estoque') or {}).items() if _num(q) and q >= 1} if leva else {}
        for b, q in est.items(): ef.append(['estoque', lid, b, 'soma', -q])
        tudo = {}
        for b, q in sorted(list(est.items()) + list(bens.items()), key=lambda x: x[0] != 'prata'): tudo[b] = tudo.get(b, 0) + q
        if leva:
            vez = 0
            for b, q in tudo.items():
                cada, resto = divmod(q, len(quem))
                for j, cc in enumerate(quem):
                    n = cada + (1 if (j - vez) % len(quem) < resto else 0)
                    if n: partes.setdefault(cc, {})[b] = partes.get(cc, {}).get(b, 0) + n
                vez = (vez + resto) % len(quem)
            ef += [['pessoa', cc, 'moedas' if b == 'prata' else f'carga.{b}', 'soma', n] for cc, x in partes.items() for b, n in x.items()]
            for it in guardadas(E, lid):
                ef += [['item', it['id'], 'dono', 'poe', leva], ['item', it['id'], 'historia', 'junta', f"Dia {dia}: tirada do tesouro {estado.de_nome(nome)}, morto {estado.em(E, lid)}"]]
        L.append(f"{Nome} morreu {estado.em(E, lid)}.")
        if c >= TD.NUCLEO_DESDE and e['nucleo']:
            nuc = item('nucleo', c, f"o coração {estado.de_nome(nome)}", de=k, historia=[f"Dia {dia}: tirado {estado.de_nome(nome)}, morto {estado.em(E, lid)}"])
            nuc.update(dict(dono=leva) if leva else dict(onde=lid, solto=True))
            ef.append(['item', 'nasce', nuc])
            L.append(f"O coração {estado.de_nome(nome)} (um núcleo {T.CATS[c]}) " + (f"fica com {E['gente'][leva]['nome']}." if leva else 'fica no chão, junto do corpo.'))
        if leva:
            pec = [it['nome'] for it in guardadas(E, lid)]
            L.append('O CORPO E O TESOURO' + (', em partes iguais entre quem lutou até o fim' if len(quem) > 1 else '') + ': '
                     + _e(f"{q} de {'prata' if b == 'prata' else estado.nome_bem(b)}" for b, q in tudo.items()) + '.'
                     + (f" As peças do tesouro ficam com {E['gente'][leva]['nome']}: {_e(pec)}." if pec else ''))
        return ef, partes, L
    agora = max(1, min(mx, int(f['pv']))); novo = dict(d); novo.pop('pv', None)
    if agora < mx: novo['pv'] = agora
    if agora < mx: novo['feriu'] = feriu
    if f['estado'] == 'fugiu':
        novo = _dorme(novo, _sarar(agora, mx), _prata(E, lid), dia); novo['fugiu'] = dia
        L.append(f"{Nome} fugiu pelo ar, ferido ({agora} de {mx}): volta ao covil, dorme até sarar e lembra de quem o feriu.")
    else:
        novo.update(dorme_ate=None, punhados=0); novo.pop('prata_sono', None)
        if agora < mx: L.append(f"{Nome} fica {estado.em(E, lid)}, ferido ({agora} de {mx}), e lembra de quem o feriu.")
    if novo != d: ef.append(['lugar', lid, 'dragao', 'poe', novo])
    return ef, partes, L


# ---------- pôr o dragão (o gerador ou o Mestre) ----------
def poe(E, lid, tipo, idade, nome, vila=None, tesouro=0, dorme=0, **mais):
    """os efeitos que põem o dragão e o tesouro num lugar (o evento é gera ou mestre: vai ao SÓ O MESTRE). O tesouro é a prata posta agora no estoque do lugar (a prata
    que o gerador tirou do mundo em séculos); as peças, quem chama as põe ali, guardadas. `dorme`: os dias de sono que faltam (0: acordado). `mais`: campos do
    registro (anos, fama, ult_ataque, ataques...). A fama (os lugares cuja gente sabe dele) é, sem dizer, a vila que ele ataca."""
    especie(tipo, idade)
    if lid not in E['lugares']: sys.exit(f'não há o lugar "{lid}"')
    l = E['lugares'][lid]
    if l.get('tipo') not in ('ermo', 'sala'): sys.exit(f"{l.get('nome', lid)} não é covil: o dragão mora num ermo ou numa sala de masmorra")
    if de(E, lid): sys.exit(f"{l.get('nome', lid)} já tem um dragão ({de(E, lid)['nome']}): um covil, um dragão")
    if not isinstance(nome, str) or not nome.strip(): sys.exit('o dragão tem nome')
    if any(x['nome'] == nome for _, x in covis(E)): sys.exit(f'já há um dragão chamado {nome}: o nome é de um só')
    if vila is not None and vila not in E['lugares']: sys.exit(f'não há o lugar "{vila}" (a vila do dragão)')
    if not _int(tesouro) or tesouro < 0 or not _int(dorme) or dorme < 0: sys.exit('o tesouro e os dias de sono são inteiros de zero para cima')
    dia = E['relogio']['dia']
    reg = dict(nome=nome, tipo=tipo, idade=idade, dorme_ate=None, punhados=0, vila=vila, desde=dia, ataques=0, fama=[vila] if vila else [])
    reg.update(mais)
    if dorme: reg = _dorme(reg, dorme, _prata(E, lid) + tesouro, dia)
    return [['lugar', lid, 'dragao', 'poe', reg]] + ([['estoque', lid, 'prata', 'soma', tesouro]] if tesouro else [])


# ---------- a ameaça: o que o Mestre lê quando a cena põe o dragão à frente ----------
def ameaca(tipo, idade, arma=None, armadura=None):
    """a frase do dragão: o grau, o tamanho, o corpo, os traços, a fase, o que dá morto e a conta da regra de ouro (com a arma e a armadura de quem lê, já feita)"""
    import bichos
    from itens import cat_i, FEM
    k = especie(tipo, idade); e = TD.ESPECIES[k]; c = e['cat']; C = T.CATS[c]; F = FEM[c]; t = TD.TIPOS[tipo]; fs = (e.get('fases') or [{}])[0]
    L = [f"{e['nome'].upper()} · grau {e['grau']} ({C}): {TB.GRAU_DIZ[e['grau']]} · {bichos._tamanho_diz(e['tamanho'], False)} · anda sozinho."]
    L.append(f"O corpo: {', '.join(e['armas'][:-1])} e {e['armas'][-1]} de categoria {F}; escama {F}, que vale como {TB.COUROS['escama']}.")
    L.append('Traços: ' + '. '.join(f'{x.capitalize()}: {bichos.frase(x)}' for x in e['tracos']) + '.')
    casa = {'água': 'luta na água (a água pesa para os dois lados)', 'escuro': 'luta no escuro, que não lhe tira nada'}
    if t['casa'].get('tempo'): L.append('Em casa, ' + ' e '.join(casa.get(x, x) for x in t['casa']['tempo']) + '.')
    if not e['chefe']:
        L.append('É um filhote: ferido, testa a coragem e pode fugir; encurralado, luta até o fim.')
    else:
        perde = ', '.join(fs.get('perde') or []); ganha = ', '.join(fs.get('ganha') or [])
        muda = f"{fs.get('diz', 'muda')}" + (f" (deixa de {'voar' if perde == 'voa' else perde}" if perde else ' (') + ('; ' if perde and ganha else '') + (f"ganha {ganha}: {bichos.frase(fs['ganha'][0])}" if ganha else '') + ')'
        L.append(f"É chefe: não foge pelo susto. Abaixo de {fs.get('abaixo', 0):.0%} do PV, " + (f"no covil {muda}; fora dele, foge pelo ar, sem golpe livre, volta ao covil para sarar e lembra de quem o feriu."
                                                                                              if fs.get('foge') else f"{muda}; luta até morrer."))
    corpo = 'couro, osso e peçonha' if t.get('peconha') else 'couro e osso'
    L.append(f"Morto, dá o corpo ({corpo}, de categoria {FEM[min(c, M.MATERIA_ATE)]})" + (f" e o coração, um núcleo {C}." if e['nucleo'] else ', e nenhum núcleo.'))
    if arma is None and armadura is None:
        L.append(f"A conta: arma abaixo de {F} {bichos._vezes(-1)} na escama dele (duas abaixo, {bichos._vezes(-2).replace('vale ', '')}); em armadura abaixo de {F}, o golpe dele {bichos._vezes(1)}.")
    else:
        if arma is not None: a = cat_i(arma); L.append(f"A sua arma ({T.CATS[a]}) na escama dele ({F}): o golpe {bichos._vezes(a - c)}.")
        if armadura is not None: a = cat_i(armadura); L.append(f"O golpe dele ({C}) na sua armadura ({T.CATS[a]}): {bichos._vezes(c - a)}.")
    return ' '.join(L)


# ---------- a régua: lutas de ensaio ----------
def homem(nome, nivel, cat, familia='espada', arma=None, armadura=None, vontade=None):
    """o homem do degrau (a régua das criaturas): gerado no nível, com a arma, a malha (corpo e elmo) e o escudo da categoria; arma= e armadura= mudam uma das duas
    (o escudo anda com a armadura); vontade= põe a Vontade (80 do Épico para cima: sem ela, a armadura grande dorme)"""
    from pessoas import padrao, veste
    from itens import cat_i
    Fm = T.FAMILIAS[familia]; ca = cat_i(cat if arma is None else arma); cr = cat_i(cat if armadura is None else armadura)
    p = padrao(nome, nivel, molde='guerreiro', atributos={'Vontade': vontade} if vontade else None)
    return veste(p, arma=(familia, ca), armadura=('malha', cr), escudo=cr if Fm['maos'] == 1 else None)


def cena_em_casa(tipo, covil=True):
    """(não se chama `casa`: esse é o nome de um gancho dos módulos) o lugar da luta em casa: o tempo do tipo (a água do brejo, o escuro das grutas) e, no covil, sem saída do lado do dragão"""
    kw = {k: list(v) for k, v in TD.TIPOS[tipo]['casa'].items()}
    if covil: kw['lugar'] = dict(sem_saida='B')
    return kw


def mede(tipo, idade, nivel, cat, homens=4, lutas=200, covil=True, dorme=False, arma=None, armadura=None, vontade=None, em_casa=True, largura=None, semente=11, interativo=False):
    """a régua: lutas de ENSAIO (dado de mentira, com semente; nada é guardado) de `homens` homens do degrau contra o dragão, em casa (o tempo do tipo) e, com covil,
    sem saída para ele. dorme: ele surpreendido (perde o primeiro turno). Devolve, em % das lutas: vence (o empate conta meio) · fugiu (ele fugiu pelo ar) · fase (a
    fase chegou) · para (a luta parou e perguntou na fase: só com interativo) · alguem (morreu alguém do grupo); e mortos (os do grupo, por luta) e rodadas (a mediana)."""
    import luta
    k = especie(tipo, idade); guarda = luta.D; luta.semente(semente); m = dict(vence=0, fugiu=0, fase=0, para=0, alguem=0, mortos=0); rs = []
    try:
        for _ in range(lutas):
            kw = cena_em_casa(tipo, covil) if em_casa else (dict(lugar=dict(sem_saida='B')) if covil else {})
            if largura: kw.setdefault('lugar', {})['largura'] = largura
            S = luta.nova([homem(f'h{j + 1}', nivel, cat, arma=arma, armadura=armadura, vontade=vontade) for j in range(homens)], [dragao(tipo, idade, lider=True)],
                          quieto=True, inicio='perto', surpresa='B' if dorme else None, **kw)
            if interativo:                                  # a luta que para e pergunta: cada parada da fase (mudou, fugiu) fica escrita, até a última
                parou = False
                while True:
                    fim = luta.corre(S, interativo=True); parou = parou or any(x.startswith(S['L'][-1]['nome']) and ('mudou' in x or 'fugiu' in x) for x in S['paradas'])
                    if fim != 'parada': break
                m['para'] += parou
            else: luta.corre(S)
            dr = S['L'][-1]; mortos = sum(1 for f in S['L'] if f['lado'] == 'A' and f['estado'] == 'morto')
            m['vence'] += 1 if S['fim'] == 'A' else 0.5 if S['fim'] == 'empate' else 0; m['fugiu'] += dr['estado'] == 'fugiu'; m['fase'] += dr.get('fase', 0) >= 1
            m['alguem'] += mortos > 0; m['mortos'] += mortos; rs.append(S['r'])
    finally: luta.D = guarda
    rs.sort(); out = {x: round(100 * v / lutas, 1) for x, v in m.items() if x != 'mortos'}; out['mortos'] = round(m['mortos'] / lutas, 2); out['rodadas'] = rs[len(rs) // 2]
    return out


# ---------- a vida do dragão (o mundo sozinho: evento "dragão", todo dia) ----------
def virada(E):
    """O DIA VIROU, NO COVIL: cada dragão vive o dia. DORMINDO (o dia antes de dorme_ate): o ferido sara SARA_DORMINDO do PV. ACORDADO: do adulto para cima, se a vila
    dele ainda não pagou a estação, paga o tributo (a prata vai do estoque dela para o do covil) e ele come no ermo; sem tributo (o jovem) ou sem prata para pagar,
    ATACA DE NOITE: o gado (a comida da vila) é comido, a prata vai para o tesouro, e morre gente do povo da vila. O filhote, e o dragão sem vila, caçam no ermo.
    Depois, dorme (os dias da tabela). O acaso é o do mundo (estado.sorte); a prata só muda de mão."""
    dia = E['relogio']['dia']
    for lid, d in covis(E):
        mx = pv_max(d['tipo'], d['idade']); agora = d['pv'] if _int(d.get('pv')) else mx; novo = dict(d); ef = []; txt = []
        if _int(d.get('dorme_ate')) and d['dorme_ate'] > dia:
            if agora >= mx: continue
            v = min(mx, agora + max(1, math.ceil(mx * TD.SARA_DORMINDO))); novo.pop('pv', None)
            if v < mx: novo['pv'] = v
            txt.append(f"dorme e sara ({v} de {mx})")
        else:
            V = TD.VIDA.get(d['idade']) or TD.VIDA['filhote']; r = estado.sorte(E, f'dragão|{lid}'); vila = d.get('vila') if d.get('vila') in E['lugares'] else None
            est = (dia - 1) // M.ESTACAO; leva = 0
            if not vila or not V['come']: txt.append('caça no ermo')
            elif V['tributo'] and d.get('tributo') == est: txt.append(f"come no ermo ({E['lugares'][vila]['nome']} já pagou a estação)")
            elif V['tributo'] and int(_prata(E, vila) * V['tributo']) > 0:
                leva = int(_prata(E, vila) * V['tributo']); novo['tributo'] = est
                ef += [['estoque', vila, 'prata', 'soma', -leva], ['estoque', lid, 'prata', 'soma', leva]]; txt.append(f"{E['lugares'][vila]['nome']} paga o tributo da estação: {leva} de prata")
            else:
                vl = E['lugares'][vila]; com = (vl.get('estoque') or {}).get('comida', 0); gado = min(V['come'], int(com) if _num(com) else 0)
                leva = min(r.randint(*V['prata']), _prata(E, vila)); pop = int(vl['pop']) if _num(vl.get('pop')) else 0; mata = min(r.randint(*V['mata']), pop)
                if gado: ef.append(['estoque', vila, 'comida', 'soma', -gado])
                if leva: ef += [['estoque', vila, 'prata', 'soma', -leva], ['estoque', lid, 'prata', 'soma', leva]]
                if mata: ef.append(['lugar', vila, 'pop', 'soma', -mata])
                novo.update(ataques=int(d.get('ataques') or 0) + 1, ult_ataque=dia, ult_mortos=mata)
                txt.append(f"ataca {vl['nome']} de noite: leva {gado} de gado e {leva} de prata" + (f"; morre{'m' if mata > 1 else ''} {mata} do povo" if mata else ''))
            novo = _dorme(novo, r.randint(*V['dorme']), _prata(E, lid) + leva, dia); txt.append(f"dorme até o Dia {novo['dorme_ate']}")
        ef.insert(0, ['lugar', lid, 'dragao', 'poe', novo])
        estado.aplica(E, EVENTO, ef, onde=lid, texto=f"{_diz(d)}: " + '; '.join(txt))


# ---------- a mesa ----------
def _conhece(E, d, lids):
    fama = d.get('fama') if isinstance(d.get('fama'), list) else ([d['vila']] if d.get('vila') else [])
    return any(x in fama for x in lids)


def mesa(E):
    """O QUE SE CONTA: de cada dragão que a gente daqui conhece (a fama dele alcança o lugar do personagem), o boato do último ataque. Sem número, sem tesouro."""
    pid = estado.eu(E)
    if not pid or pid not in E['gente']: return []
    p = E['gente'][pid]; lids = {p.get('lugar'), estado.onde(E, pid)}; aqui = p.get('lugar'); L = []; dia = E['relogio']['dia']
    for lid, d in covis(E):
        if not _conhece(E, d, lids): continue
        e = _esp(d); onde = E['lugares'][lid]['nome']; vila = d.get('vila') if d.get('vila') in E['lugares'] else None
        x = f"Conta-se que {d['nome']}, um {e['nome']}, mora {estado.em(E, lid)}"
        ua = d.get('ult_ataque')
        if vila and _int(ua) and 0 <= dia - ua <= TD.BOATO:
            ha = 'hoje' if dia == ua else 'ontem' if dia - ua == 1 else f"há {dia - ua} dias"
            x += f", e que {ha} levou gado {estado.de(E, vila)}" + (' e matou gente de lá' if d.get('ult_mortos') else '')
        elif vila and d.get('tributo') is not None and (dia - 1) // M.ESTACAO == d['tributo']: x += f", e que {E['lugares'][vila]['nome']} lhe paga tributo"
        x += '.'
        if vila and vila != aqui and vila not in (E['lugares'].get(aqui) or {}).get('vizinhos', []): x += f" {E['lugares'][vila]['nome']} fica longe daqui."
        L.append('- ' + x)
    return (['## O que se conta (os dragões de que a gente daqui sabe)'] + L) if L else []


def so_mestre(E):
    """SÓ O MESTRE: o registro de cada dragão do mundo (o PV, o sono, a vigília, o tesouro em prata e peças, a vila, o próximo ataque, quem ele lembra)"""
    L = []; dia = E['relogio']['dia']
    for lid, d in covis(E):
        e = _esp(d); mx = pv_max(d['tipo'], d['idade']); v = vigilia(E, lid); pec = guardadas(E, lid); vila = d.get('vila') if d.get('vila') in E['lugares'] else None
        sono = (f"dorme até o Dia {d['dorme_ate']} (vigília {v}, mais {TD.VIGILIA['sobe']} por punhado; {int(d.get('punhados') or 0)} tirados neste sono)" if v is not None else 'ACORDADO')
        L.append(f"{d['nome']} ({e['nome']}, grau {e['grau']}{', ' + str(d['anos']) + ' anos' if _int(d.get('anos')) else ''}) {estado.em(E, lid)}: PV {pv(E, lid)} de {mx} · {sono} · "
                 f"o tesouro: {_prata(E, lid)} de prata" + (f"; as peças: {_e(it['nome'] for it in pec)}" if pec else '') + ' · '
                 + (f"a vila: {E['lugares'][vila]['nome']} ({int(d.get('ataques') or 0)} ataque{'' if int(d.get('ataques') or 0) == 1 else 's'}" + (f", o último no Dia {d['ult_ataque']}" if _int(d.get('ult_ataque')) else '') + ')' if vila else 'sem vila (caça no ermo)')
                 + (f" · lembra de quem o feriu: {', '.join(E['gente'][x]['nome'] for x in d['feriu'] if x in E['gente'])}" if d.get('feriu') else '') + f" (`dragoes.py covil {lid}`)")
    return L


# ---------- a vila de teste (E4 a): o Tição, longe, em Vau Seco ----------
def na_vila(E, vila='vila'):
    """o dragão jovem longe (E4 a): VAU SECO (uma aldeia de 120, com mercado, longe: não é vizinha de Pedra Rasa), a SERRA FRIA (o ermo do covil, vizinho de Vau Seco)
    e O TIÇÃO, dragão jovem da serra, que dorme lá sobre o tesouro (prata e duas peças de quem o enfrentou) e ataca Vau Seco. A pousada da vila conta dele.
    Aplica os eventos (gera: o covil vai ao SÓ O MESTRE) e devolve as linhas. Recusa rodar duas vezes, antes de aplicar qualquer coisa."""
    import mercado
    from itens import item
    V = TD.VILA_TESTE; A, C, D = V['aldeia'], V['covil'], V['dragao']
    if vila not in E['lugares']: sys.exit(f'não há o lugar "{vila}" (a vila de teste)')
    if A['id'] in E['lugares'] or C['id'] in E['lugares'] or any(x['nome'] == D['nome'] for _, x in covis(E)):
        sys.exit(f"a vila de teste já tem {D['nome']} ({C['nome']}, {A['nome']}): não se acrescenta duas vezes")
    dia = E['relogio']['dia']
    estado.aplica(E, 'gera', [['lugar', 'nasce', A['id'], dict(nome=A['nome'], em=A['em'], tipo=A['tipo'], estoque={})]], onde=A['id'], texto=f"{A['nome']}, uma aldeia longe daqui, ao pé da serra")
    mercado.funda(E, A['id'], A['pop'], prateleira_=False, como='a aldeia que o dragão ataca')
    ef = [['lugar', 'nasce', C['id'], dict(nome=C['nome'], em=C['em'], tipo='ermo', habitat=C['habitat'], perigo=C['perigo'], longe=C['longe'], estoque={}, vizinhos=[A['id']], bichos={}, teto={})],
          ['lugar', A['id'], 'vizinhos', 'poe', list(E['lugares'][A['id']].get('vizinhos') or []) + [C['id']]]]
    E2 = dict(E, lugares=dict(E['lugares'], **{C['id']: dict(nome=C['nome'], tipo='ermo', estoque={})}))     # o ermo ainda não nasceu: o poe confere num retrato
    ef += poe(E2, C['id'], D['tipo'], D['idade'], D['nome'], vila=A['id'], tesouro=D['tesouro'], dorme=D['dorme'], anos=D['anos'], ataques=1,
              ult_ataque=dia - D['ult_ataque'], ult_mortos=0, fama=[A['id'], vila])
    for tipo, fam, cat, nm, hist in V['pecas']:
        ef.append(['item', 'nasce', dict(item(tipo, cat, nm, familia=fam), onde=C['id'], historia=[hist])])
    estado.aplica(E, 'gera', ef, onde=C['id'], texto=f"{C['nome']}: o covil {estado.de_nome(D['nome'])}, um dragão jovem da serra")
    P = estado.valida(E)
    if P: sys.exit('O DRAGÃO ENTROU TORTO NA VILA:\n  ' + '\n  '.join(P))
    d = de(E, C['id']); tes = _e([f"{_prata(E, C['id'])} de prata"] + [it['nome'] for it in guardadas(E, C['id'])])
    return [f"{A['nome']}, uma aldeia de {A['pop']} ao pé da serra, fica longe de {E['lugares'][vila]['nome']} (não há estrada daqui até lá). {D['nome'][:1].upper() + D['nome'][1:]}, "
            f"um dragão jovem da serra, mora {C['em']} e leva gado de lá de tempos em tempos: a pousada conta (o último ataque foi há {D['ult_ataque']} dias).",
            f"SÓ O MESTRE: {D['nome']} dorme até o Dia {d['dorme_ate']}, sobre {tes}."]


# ---------- olhar ----------
def _lista():
    L = [f"{'dragão':<28}{'grau':<6}{'categoria':<11}{'tamanho':<9}{'PV':>6}  {'traços':<52}o que dá morto"]
    for t in TD.TIPOS:
        for i in TD.IDADES:
            k = TD.chave(t, i); e = TD.ESPECIES[k]
            L.append(f"{k:<28}{e['grau']:<6}{T.CATS[e['cat']]:<11}{e['tamanho']:<9}{pv_max(t, i):>6}  {', '.join(e['tracos']):<52}"
                     + ' · '.join(f'{q} de {estado.nome_bem(b)}' for b, q in e['despojo'].items()) + (f" e o coração (núcleo {T.CATS[e['cat']]})" if e['nucleo'] else ''))
    return '\n'.join(L)


def _ver(tipo, idade):
    from pessoas import ficha, linha
    k = especie(tipo, idade); e = TD.ESPECIES[k]; i = TD.IDADES[idade]
    anos = f"de {i['anos'][0]} a {i['anos'][1]} anos" if i['anos'][1] else f"mais de {i['anos'][0]} anos"
    return '\n'.join([linha(ficha(dragao(tipo, idade))), f"  a idade: {anos} · onde vive: {', '.join(e['habitat'])}",
                      '  o corpo (inteiro): ' + ' · '.join(f'{q} de {estado.nome_bem(b)}' for b, q in e['despojo'].items()) + (f" · e o coração, um núcleo {T.CATS[e['cat']]}" if e['nucleo'] else ' · sem núcleo'),
                      '', ameaca(tipo, idade)])


def _covil(E, lid=None):
    if lid is None: return '\n'.join(so_mestre(E)) or 'não há dragão no mundo.'
    d = de(E, lid)
    if not d: return f'não há dragão em "{lid}".'
    return '\n'.join(x for x in so_mestre(E) if x.endswith(f'`dragoes.py covil {lid}`)'))


def main(a=None):
    a = sys.argv[1:] if a is None else list(a)
    op = dict(x.split('=', 1) for x in a if '=' in x); pos = [x for x in a if '=' not in x]
    num = lambda x, que: int(x) if str(x).isdigit() and int(x) >= 1 else sys.exit(f'{que}: um número de 1 para cima (veio "{x}")')
    sim = lambda k, pad: op.get(k, pad) in ('sim', 's', '1', 'true')
    if pos == ['lista']: print(_lista())
    elif pos[:1] == ['ver'] and len(pos) == 3: print(_ver(pos[1], pos[2]))
    elif pos[:1] == ['ameaca'] and len(pos) == 3: print(ameaca(pos[1], pos[2], arma=op.get('arma'), armadura=op.get('armadura')))
    elif pos[:1] == ['mede'] and len(pos) == 5:
        from itens import cat_i
        q = num(op.get('homens', '4'), 'quantos homens'); c = cat_i(pos[4]); nv = num(pos[3], 'o nível'); cov = sim('covil', 'sim'); dm = sim('dorme', 'nao')
        m = mede(pos[1], pos[2], nv, c, homens=q, lutas=num(op.get('lutas', '200'), 'quantas lutas'), covil=cov, dorme=dm, arma=op.get('arma'), armadura=op.get('armadura'),
                 vontade=80 if c >= 3 else None)
        print(f"ENSAIO (não é a luta de verdade: dado de mentira, nada é guardado): {'um homem' if q == 1 else f'{q} homens'} de nível {nv}, de espada, malha e escudo {T.CATS[c]}"
              f"{(', a arma ' + T.CATS[cat_i(op['arma'])]) if op.get('arma') else ''}{(', a armadura ' + T.CATS[cat_i(op['armadura'])]) if op.get('armadura') else ''}, "
              f"contra {TD.ESPECIES[especie(pos[1], pos[2])]['nome']} {'no covil (sem saída para ele)' if cov else 'fora do covil'}{', dormindo (surpreendido)' if dm else ''}:\n"
              f"  vence {m['vence']}% · morre alguém em {m['alguem']}% das lutas ({m['mortos']} mortos por luta) · ele fugiu em {m['fugiu']}% · a fase chegou em {m['fase']}% · mediana de {m['rodadas']} rodadas")
    elif pos[:1] == ['covil']:
        E = estado.carrega()
        if len(pos) >= 5 and pos[1] == 'poe':
            nome = pos[5] if len(pos) > 5 else None
            if not nome: sys.exit('o dragão tem nome: `dragoes.py covil poe LUGAR TIPO IDADE "Nome"`')
            ef = poe(E, pos[2], pos[3], pos[4], nome, vila=op.get('vila'), tesouro=int(op.get('tesouro', 0)) if str(op.get('tesouro', 0)).isdigit() else sys.exit('tesouro= é um número'),
                     dorme=int(op.get('dorme', 0)) if str(op.get('dorme', 0)).isdigit() else sys.exit('dorme= é um número de dias'))
            estado.aplica(E, 'mestre', ef, onde=pos[2], texto=f"o Mestre funda o covil {estado.de_nome(nome)} {estado.em(E, pos[2])}"); estado.grava(E)
            print(_covil(E, pos[2]))
        elif len(pos) <= 2: print(_covil(E, pos[1] if len(pos) == 2 else None))
        else: print(__doc__)
    else: print(__doc__)


if __name__ == '__main__':
    import signal; hasattr(signal, 'SIGPIPE') and signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    main()
