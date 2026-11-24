#!/usr/bin/env python3
"""caca.py — MOTOR 10: A CAÇA E A COLETA. O ermo tem bichos contados e matéria contada. O que se tira, sai. O que nasce, nasce devagar.
Tudo por evento (`cacar`, `coletar`, `despojo`, `ninhada`); os números moram no tabelas_caca.py; os bichos, no bichos.py e no tabelas_bichos.py.

  A SAÍDA é um ato só: a ida ao ermo vizinho, os blocos de procura (ou de coleta) e a volta. A pessoa segue morando no lugar dela.
    A saída aberta fica escrita na pessoa (marca.caca) até a volta: sobrevive a fechar e abrir o estado. Quem vai junto (com=) fica marcado na saída de quem
    comanda, e o corpo dele passa os mesmos blocos. ENQUANTO A SAÍDA ESTÁ ABERTA, A PESSOA ESTÁ NO ERMO: os atos da vila (dormir, trabalhar, comprar, forjar)
    são recusados (estado.presente); só come da própria carga.
    QUEM VAI JUNTO CUIDA DE SI: ao entrar na saída, o tempo que ele passou em casa é acertado antes de mais nada (estado.em_cena: passados 3 blocos ou mais do último
    bloco em cena, dois inteiros em casa, a fome, o sono e o cansaço voltam a zero; a cada 6, uma noite de cura). Se mesmo assim não vai inteiro (ferida aberta, PV abaixo de 90%, o corpo cobrando),
    a mesa diz. No ermo, quem vai junto e tem comida na carga come quando a fome cobra.
  O RASTRO: um teste por bloco de procura, 2d20 + Percepção ÷ 10 + maestria de caça (+ a pena do corpo), contra a FARTURA do ermo:
    20, mais o arisco da espécie, mais até 12 pelo que falta dela (contagem ÷ teto). De noite, −4.
  O QUE APARECE SAI DA CONTAGEM REAL: um bicho, um bando (nunca mais do que há), ou nada. No bloco em que o rastro falha, pode
    aparecer o que não se procurava (o acaso do mundo), e esse VIU o caçador.
  ANTES DA LUTA O CAÇADOR LÊ A AMEAÇA (bichos.ameaca) e escolhe: atacar, deixar, fugir.
    Quem viu primeiro ataca com o bicho surpreendido, de longe ou de perto, e a margem do rastro dá o terreno (alto, cerco, estreito, cobertura).
    O bicho que viu o caçador pode investir em quem o deixa, e vir atrás de quem corre (Agilidade contra a dele; alcançado, luta colado e surpreendido).
  A LUTA É A DO `ato.py luta`, com paradas e ordens: este script só monta o cenário e, no fim, faz as contas.
    Bicho morto sai da contagem. Se a casa ficou com o campo, o despojo entra na carga e o núcleo do chefe entra no Livro de Itens.
    O DESPOJO É DE QUEM LUTOU ATÉ O FIM: reparte-se em partes iguais entre os da casa que acabaram a luta de pé no campo, ou caídos nele e vivos.
    Quem saiu da luta antes do fim (recuou para fora dela, fugiu, rendeu-se) não leva nada. O núcleo fica com quem comanda, se ele ficou; senão, com o primeiro que ficou.
    Quem perde o campo deixa a carcaça no mato. O bicho que fugiu segue no ermo.
    QUEM MORRE NO ERMO fica lá (a regra da morte é do estado.py): as peças e os núcleos dele caem SOLTOS ali, e a carga e a prata ficam no chão (o estoque do ermo).
    Quem passa num rastro ali ACHA o que está solto: o núcleo da carcaça que ninguém abriu e a peça largada passam a ser dele. Só o que está SOLTO: a prateleira de uma loja não é achado.
    O QUE ERA DE UM MORTO NÃO MUDA DE MÃO SOZINHO: quem passa num rastro acha o CORPO e lê o que ficou com ele (as peças, a carga, a prata), e nada mais.
    Quem fica com o quê é decisão de cena: o Mestre registra por evento (`itens.py dono ITEM PESSOA`, `estado.py mestre`). O herdeiro é da etapa 6.
  A PRESA FERIDA: o bicho que fugiu com ferida aberta deixa SANGUE. Quem ficou com o campo pode segui-lo na hora, sem gastar bloco: o rastro fica mais fácil,
    e quem passa acha o mesmo bicho, com o PV e as feridas com que fugiu. Cada nova perseguição no mesmo bloco é mais difícil. Quem segue a procura, larga-o.
  A COLETA (minério, madeira, erva): um teste por bloco, 2d20 + Força ou Percepção ÷ 10 + maestria de coleta, contra 20, mais 8 por categoria, mais o que rareou.
    O bloco que passa rende o da tabela, e só isso; o que falha não rende nada. O que se tira sai do `coleta` do ermo e entra na carga, no mesmo evento.
    A MATÉRIA PEDE MÃO: a Comum, qualquer um tira; a Incomum pede Iniciante em coleta; a Rara, Treinado. Sem a mão, o comando recusa antes de gastar a saída.
    A borda de um ermo só dá matéria Comum: a Incomum e a Rara só há do interior para cima.
  A VIRADA: os bichos criam devagar até o teto; a espécie caçada até o fim some por muito tempo; o chefe demora a nascer; a matéria volta devagar.
  AS CRIATURAS (etapa da magia: criaturas.py) contam no ermo como os bichos (lugar.bichos): o goblin, o esqueleto, o fogo-fátuo... Aparecem no rastro e no acaso,
    lê-se a ameaça antes, e a luta é a mesma. O POVO (gente que veste) pode render-se: quem fica com o campo o leva, e ele sai da contagem como o morto. O despojo do
    povo é a sucata das peças (a peça dele é gasta e malfeita). As criaturas que não são fera não criam na virada: o bando de um covil cria pela vida do covil (criaturas.virada).
  A TOCA: o ermo que tem covil (lugar.covil) esconde a toca do bando. `caca.py sair ERMO alvo=toca` procura a toca (o rastro é mais difícil, e a rolagem é oculta:
    ninguém sabe de graça se há toca); achada, a luta é com quem está lá dentro (o chefe e a guarda dele, o líder, e o resto). Quem fica com o campo NA TOCA leva
    o tesouro dela (a prata e a comida que o bando juntou: o estoque do ermo), repartido entre quem lutou até o fim. O que cai no chão de um ermo com toca, o bando junta.

Uso (o personagem do jogador, ou quem=ID):
  python3 caca.py ver                                   os ermos vizinhos (o que se sabe), a sua mão, a saída aberta
  python3 caca.py sair [ERMO] [alvo=ESPECIE|toca] [blocos=N] [com=ID,ID]      sai para caçar: a ida, e a procura até aparecer alguma coisa (sem alvo: o que aparecer; alvo=toca: a toca do covil).
                                                        O bicho comum que aquele ermo não tem é recusado antes de sair; do chefe ninguém sabe: a saída segue
  python3 caca.py atacar [inicio=longe|perto|colado] [vantagem=alto,cerco]    ataca o que apareceu: monta a luta e mostra o quadro
  python3 caca.py luta ["Nome: ordem"] ["grupo: ordem"]  roda a luta aberta até a próxima parada (é o `ato.py luta roda`); no fim, faz as contas do despojo
  python3 caca.py sangue                                segue o rastro de sangue da presa que fugiu ferida (sem gastar bloco: é agora ou nunca)
  python3 caca.py deixar                                deixa o bicho e segue a procura (o que viu você pode investir)
  python3 caca.py fugir                                 larga a caçada e volta (do bicho que viu você: Agilidade contra a dele)
  python3 caca.py segue                                 segue a procura (ou a coleta) com os blocos que restam
  python3 caca.py volta                                 volta para casa: fecha a saída (com a luta acabada, faz antes as contas dela)
  python3 caca.py larga "por quê"                       SÓ O MESTRE: fecha a saída SEM as contas (o arquivo da luta se perdeu, a cena mudou); o resto entra por evento
  python3 caca.py coletar BEM [ERMO] [blocos=N]         sai para tirar matéria: metal:0 madeira:0 erva:1 ... (0 Comum; 1 Incomum, pede Iniciante; 2 Raro, pede Treinado); N de 1 a 4
  python3 caca.py conta [ERMO]                          SÓ O MESTRE: a contagem de verdade, o número do rastro e a chance do acaso
  python3 caca.py povoa ERMO HABITAT [perigo=1] [vizinho=LUGAR] [longe=N] ["como foi"]     o Mestre povoa um lugar que já existe (bichos e matéria no teto)
HABITAT: floresta campo brejo serra caverna ruína · perigo: 1 (a borda), 2 (o interior), 3 (o coração)
"""
import json, math, os, sys
import tabelas as T
import tabelas_mundo as M
import tabelas_bichos as TB
import tabelas_caca as K
import estado, ato, corpo, teste, bichos, talento
TOCA = 'toca'               # o alvo que procura a toca do covil do ermo (etapa da magia: criaturas.py)

FEM = ['Comum', 'Incomum', 'Rara', 'Épica', 'Única', 'Lendária', 'Mítica', 'Primordial']       # a categoria, quando o nome que vem antes é feminino
FICOU = ('pe', 'caido')     # como acaba a luta quem LUTOU ATÉ O FIM (de pé no campo, ou caído nele): só esses têm parte no despojo. Quem saiu, fugiu ou se rendeu, não
EVENTO = {'caça': 'cacar', 'coleta': 'coletar'}
OFICIO = {'caça': 'caça', 'coleta': 'coleta'}


# ---------- dizer ----------
def _em(E, lid): l = E['lugares'][lid]; return l.get('em', 'em ' + l['nome'])
def _bem(chave): return estado.nome_bem(chave)       # o nome do bem à mesa: "couro Comum", "poção de cura Comum" (e não a chave "cura:0")
def _lista(d): return ', '.join(f'{q} de {_bem(b)}' for b, q in d.items()) or 'nada'
def _plural(nome):
    """o plural do nome de uma espécie: lobos, corças, dragões, aranhas-de-toca"""
    a, h, resto = nome.partition('-')
    return (a[:-2] + 'ões' if a.endswith('ão') else a + 's') + h + resto
def _E(esp): return estado.especie(esp) or sys.exit(f'espécie desconhecida: "{esp}"')            # o registro de um bicho ou de uma criatura (etapa da magia)
def _nome(esp, n=1):
    e = _E(esp); return f"{e['artigo']} {e['nome']}" if n == 1 else f"{n} {e.get('plural') or _plural(e['nome'])}"
def _s(n, um, muitos): return um if n == 1 else muitos
def _bl(n): return f"{n:g} {_s(n, 'bloco', 'blocos')}"          # "1 bloco", "2 blocos"
def _ou(L): return L[0] if len(L) == 1 else ', '.join(L[:-1]) + ' ou ' + L[-1]
def _e(L): L = list(L); return ''.join(L) if len(L) <= 1 else ', '.join(L[:-1]) + ' e ' + L[-1]        # "Rute", "Rute e Tomé", "Cira, Rute e Tomé"
def _resta(n, de=''):
    """o que resta da saída, numa frase: "Restam 2 blocos de procura: `caca.py segue` ou `caca.py volta`."; sem bloco nenhum, só há a volta"""
    return f"{_s(n, 'Resta', 'Restam')} {_bl(n)}{de}: `caca.py segue` ou `caca.py volta`." if n > 0 else f"Não resta bloco{de}: `caca.py volta`."
def _cap(x): return x[:1].upper() + x[1:]                        # a primeira letra maiúscula, sem mexer no resto ("a Mata do Corvo" abre a frase como "A Mata do Corvo")


NA_PARTE = {'cabeça': 'na cabeça', 'braços': 'nos braços', 'tronco': 'no tronco', 'pernas': 'nas pernas'}


def nao_inteiro(E, c):
    """o estado de quem vai junto, numa frase, SE ELE NÃO ESTÁ INTEIRO: PV abaixo de 90% (tabelas_mundo.INTEIRO_PV), ferida aberta, ou o corpo cobrando (pena ou fôlego a menos).
    Inteiro, None."""
    q = E['gente'][c]; L = []
    if q['pv'] < estado.pv_max(q) * M.INTEIRO_PV: L.append(f"PV {q['pv']}/{estado.pv_max(q)}")
    L += [f"ferida{' grave' if f['grave'] else ''} {NA_PARTE.get(f['parte'], f['parte'])} ({estado.num(f['repouso'])} de {M.FERIDA_DIAS[1 if f['grave'] else 0]} dias de repouso)" for f in q['feridas']]
    if corpo.pena(q, estado.agora(E)) or corpo.folego_menos(q):
        em_casa = max(0, corpo.fora_de_cena(E, c) - 1)       # os blocos inteiros em casa: o descanso conta do último bloco em cena, e esse não é de casa
        L.append(corpo.diz(q) + f" (em casa há {_bl(em_casa)}: com {M.CASA_ZERA - 1} ou mais, teria comido e dormido por conta própria)")
    return f"{q['nome']}: " + ' · '.join(L) if L else None


def merenda(E, com, L):
    """NO ERMO, QUEM VAI JUNTO COME DA PRÓPRIA CARGA quando a fome cobra (o primeiro limiar): ninguém manda nele, e ninguém passa fome com comida no alforje.
    Não vale para o personagem (esse come quando o jogador manda). Uma linha na mesa por pessoa."""
    if estado.luta_aberta(E): return
    for c in com:
        q = E['gente'].get(c); n = 0
        if not q or q.get('jogador') or q['estado'] != 'vivo': continue
        while E['gente'][c]['corpo']['fome'] >= M.LIMIARES['fome'][0] and (E['gente'][c].get('carga') or {}).get('comida', 0) >= 1:
            estado.aplica(E, 'comer', [['pessoa', c, 'carga.comida', 'soma', -1], ['pessoa', c, 'fome', 'soma', M.REFEICAO]], onde=estado.onde(E, c), quem=[c], texto=f"{q['nome']} come da própria carga"); n += 1
        if n:
            q = E['gente'][c]; sobra = (q.get('carga') or {}).get('comida', 0)
            L.append(f"{q['nome']} come da própria carga ({estado.tantos(n, 'refeição', 'refeições')}; fome {q['corpo']['fome']}; {_s(sobra, 'resta', 'restam')} {sobra:g} de comida).")


# ---------- ler ----------
def _vivo(E, pid):
    p = E['gente'].get(pid) or sys.exit(f'não há a pessoa "{pid}"')
    if p['estado'] != 'vivo': sys.exit(f"{p['nome']} não age: {estado.morte_diz(E, p)}")
    return p


def _num(d): return {k: v for k, v in d.items() if isinstance(v, (int, float)) and not isinstance(v, bool)} if isinstance(d, dict) else {}
def mao(p, oficio='caça'): m = p.get('maestria'); return m.get(oficio, 0) if isinstance(m, dict) else 0             # a maestria no ofício (0 a 8)
def saida(p): s = (p.get('marca') or {}).get('caca'); return s if isinstance(s, dict) and not s.get('de') else None    # a saída aberta que esta pessoa COMANDA, ou None
def vai_com(p): s = (p.get('marca') or {}).get('caca'); return s.get('de') if isinstance(s, dict) else None             # de quem é a saída em que esta pessoa foi junto, ou None
def _arq(s): return estado.arq_abre(s['luta'])                                                                          # o arquivo da luta da saída (o save guarda o caminho relativo à pasta dele)
def bichos_de(E, lid): return {e: int(q) for e, q in _num(E['lugares'][lid].get('bichos')).items() if estado.especie(e) and q >= 1}      # a contagem real: {espécie: quantos} (bichos e criaturas)
def teto_de(E, lid): return {e: q for e, q in _num(E['lugares'][lid].get('teto')).items() if estado.especie(e) and q > 0}
def covil_de(E, lid):
    """o covil do ermo (etapa da magia: criaturas.py), se há, com as cabeças contadas; ou None"""
    cv = E['lugares'][lid].get('covil'); return cv if isinstance(cv, dict) and estado.especie(cv.get('especie')) else None
def coleta_de(E, lid): return {b: q for b, q in _num(E['lugares'][lid].get('coleta')).items() if M.le_materia(b)[0] in K.COLETA}
def coleta_teto(E, lid): return {b: q for b, q in _num(E['lugares'][lid].get('coleta_teto')).items() if M.le_materia(b)[0] in K.COLETA and q > 0}
def tem_caca(E, lid): return bool(teto_de(E, lid) or bichos_de(E, lid))
def e_ermo(E, lid): return tem_caca(E, lid) or bool(coleta_teto(E, lid))
def ermos(E, lid): return [v for v in (E['lugares'][lid].get('vizinhos') or []) if v in E['lugares'] and e_ermo(E, v)]         # os ermos vizinhos de um lugar
def longe(E, lid): v = E['lugares'][lid].get('longe'); return v if isinstance(v, int) and not isinstance(v, bool) and v >= 1 else K.IDA      # os blocos de ida (a volta custa o mesmo)


def falta(tem, teto):
    """o que falta para o teto, de 0 (cheio) a 1 (sumiu)"""
    return (0.0 if tem > 0 else 1.0) if teto <= 0 else max(0.0, 1 - tem / teto)


def rastro_contra(E, lid, alvo=None):
    """o número do rastro neste ermo, hoje: a base, o arisco da espécie e o que falta dela. Sem alvo: a base e o que falta do ermo inteiro."""
    B = bichos_de(E, lid); Tt = teto_de(E, lid)
    if alvo: return K.RASTRO_BASE + K.arisco(alvo) + round(K.RASTRO_FALTA * falta(B.get(alvo, 0), Tt.get(alvo, 0)))
    return K.RASTRO_BASE + round(K.RASTRO_FALTA * falta(sum(B.values()), sum(Tt.values())))


def acaso(E, lid):
    """a chance, por bloco, de aparecer o que não se procurava: a soma de contagem × ousadia, dividida pela tabela"""
    return min(K.ACASO_MAX, sum(q * K.indole(e)[0] for e, q in bichos_de(E, lid).items()) / K.ACASO_CADA)


def coleta_contra(E, lid, bem):
    """o número da coleta desta matéria neste ermo, hoje"""
    _, cat = M.le_materia(bem); ha = coleta_de(E, lid).get(bem, 0)
    return K.COLETA_BASE + K.COLETA_CAT * (cat or 0) + round(K.COLETA_FALTA * falta(ha, coleta_teto(E, lid).get(bem, 0)))


def _somas():
    """a conta exata do 2d20 (cada 20 rola de novo e soma): {soma: chance}"""
    um = {}
    def rola(soma, p, vezes):
        for f in range(1, 21):
            if f == 20 and vezes < 6: rola(soma + 20, p / 20, vezes + 1)
            else: um[soma + f] = um.get(soma + f, 0) + p / 20
    rola(0, 1.0, 0); dois = {}
    for a, pa in um.items():
        for b, pb in um.items(): dois[a + b] = dois.get(a + b, 0) + pa * pb
    return dois
_SOMAS = _somas()
def chance(precisa): return min(1.0, sum(p for s, p in _SOMAS.items() if s >= precisa))       # a chance de 2d20 (com o 20 que rola de novo) dar `precisa` ou mais


def coleta_rende(bem, margem, ha):
    """quantas unidades um bloco de coleta rende, dada a margem do teste (o total menos o número) e o que há no ermo: passou, o da tabela (e só isso); falhou, nada"""
    return min(int(ha), K.COLETA[M.le_materia(bem)[0]]['rende']) if margem >= 0 else 0


def coleta_pede(p, bem):
    """a mão que esta matéria pede e esta pessoa NÃO tem (a maestria de coleta que falta), ou None se a mão dela basta"""
    pede = K.coleta_mao(M.le_materia(bem)[1] or 0)
    return pede if mao(p, 'coleta') < pede else None


def coleta_conta(E, pid, lid, bem):
    """a conta exata de UM bloco de coleta desta matéria, para esta pessoa, hoje: (a chance de o teste passar, as unidades que o bloco rende em média).
    Quem não tem a mão que a matéria pede não tira: (0, 0)."""
    p = E['gente'][pid]; nome, _ = M.le_materia(bem); contra = coleta_contra(E, lid, bem); ha = int(coleta_de(E, lid).get(bem, 0))
    if coleta_pede(p, bem) is not None: return 0.0, 0.0
    soma = p['atributos'][K.COLETA[nome]['atributo']] // 10 + mao(p, 'coleta') + corpo.pena(p, estado.agora(E))
    return chance(contra - soma), sum(pr * coleta_rende(bem, s + soma - contra, ha) for s, pr in _SOMAS.items())


def posicao(enc):
    """o que o encontro dá a quem ataca: (os começos possíveis, quantas vantagens de terreno, o lado surpreendido)"""
    if enc['viu'] == 'caçador':
        m = enc['margem']; return list(K.INICIOS_RASTRO) + (['colado'] if m >= K.COLADO else []), max(0, min(K.POSICAO_MAX, m // K.POSICAO_CADA)), 'B'
    if enc['viu'] == 'alcançado': return [K.INICIO_ALCANCADO], 0, 'A'
    return [K.INICIO_ACASO], 0, None


def _especie(x):
    """a espécie pelo nome da tabela ou pelo nome que vai à mesa ("aranha" ou "aranha-de-toca"); a criatura também (etapa da magia); "toca" (ou "covil"): a toca do covil"""
    if x in (TOCA, 'covil'): return TOCA
    k = next((k for k, d in TB.ESPECIES.items() if x in (k, d['nome'])), None) or bichos._chave(x)
    return k if estado.especie(k) else sys.exit(f'espécie desconhecida: "{x}" (as que existem: {", ".join(TB.ESPECIES)}; e as criaturas: criaturas.py lista)')


def _veste(E, pid):
    """(a categoria da arma, a da armadura do tronco) de quem lê a ameaça, ou None"""
    eq = estado.pecas(E, pid); tronco = [it['cat'] for it in eq['veste'] if 'tronco' in it.get('cobre', []) and it['dur'][0] > 0]
    return (eq['arma']['cat'] if eq['arma'] and eq['arma']['dur'][0] > 0 else None), (max(tronco) if tronco else None)


def _inteiro(E, x, chave):
    """x em unidades inteiras: a parte quebrada vira a chance de mais uma (o acaso do mundo: mesma semente, mesmo mundo)"""
    n = math.floor(x); resto = x - n
    return n + (1 if resto > 1e-9 and estado.sorte(E, chave).random() < resto else 0)


def _sorteia(pesos, r):
    """uma chave ao acaso, com a chance do peso dela (None se não há peso nenhum)"""
    tot = sum(pesos.values())
    if tot <= 0: return None
    x = r.random() * tot; ult = None
    for k in sorted(pesos):
        if pesos[k] <= 0: continue
        ult = k; x -= pesos[k]
        if x < 0: return k
    return ult


def _soltam(E, s):
    """os efeitos que tiram da saída quem foi junto (a saída fechou)"""
    return [['pessoa', c, 'marca.caca', 'poe', None] for c in (s or {}).get('com', []) if c in E['gente'] and (E['gente'][c].get('marca') or {}).get('caca') is not None]


def _marca(E, pid, s, texto, mais=(), tipo=None):
    """a saída aberta (ou None: fechada, e quem foi junto fica solto) fica escrita na pessoa, por evento"""
    p = E['gente'][pid]; ant = saida(p) or s or {}
    estado.aplica(E, tipo or EVENTO[ant.get('quer', 'caça')], [['pessoa', pid, 'marca.caca', 'poe', s]] + (_soltam(E, ant) if s is None else []) + list(mais),
                  onde=ant.get('ermo'), quem=[pid], texto=TB.contrai(texto))


def _minha(E, pid, vivo=True):
    """a pessoa e a saída que ela comanda; recusa, com a frase, quem não tem saída ou só foi junto na de outro"""
    p = _vivo(E, pid) if vivo else (E['gente'].get(pid) or sys.exit(f'não há a pessoa "{pid}"'))
    if vai_com(p): sys.exit(f"{p['nome']} foi junto na saída de {E['gente'].get(vai_com(p), {}).get('nome', vai_com(p))}: quem decide é quem comanda (`quem={vai_com(p)}`)")
    s = saida(p)
    if not s and p['estado'] != 'vivo': sys.exit(f"{p['nome']} não age: {estado.morte_diz(E, p)}. Não há saída aberta para fechar.")
    if not s: sys.exit(f"{p['nome']} não tem saída aberta (`caca.py sair`)")
    if s.get('ermo') not in E['lugares'] or s.get('fase') not in ('procura', 'encontro', 'luta') or not isinstance(s.get('restam'), int) or not isinstance(s.get('com', []), list):
        sys.exit(f"a saída de {p['nome']} está torta (o estado não a descreve direito: `estado.py valida`). SÓ O MESTRE: `caca.py larga \"por quê\"` a fecha sem as contas")
    s.setdefault('com', []); s.setdefault('lutas', 0)
    return p, s


# ---------- a maestria ----------
def _dom_mostra(E, pid, r, ermo):
    """o dom escondido fez passar o teste (etapa da magia): a pessoa vê que tem (um evento só, antes de seguir)"""
    if talento.decidiu(r) and talento.mostra(E, pid):
        estado.aplica(E, 'cacar', talento.mostra(E, pid), onde=ermo, quem=[pid], texto=f"{E['gente'][pid]['nome']} percebe que tem um dom")


def sobe(E, pid, oficio='caça'):
    """a maestria de caça (ou de coleta) sobe quando os blocos chegam; de Mestre para cima, só com o FEITO (marca.feito_OFICIO: a categoria mais alta que a mão já tirou)"""
    p = E['gente'][pid]; tem = mao(p, oficio); bl = (p.get('treino') or {}).get(oficio, 0); txt = ''
    tab, feito = (K.CACA_BLOCOS, K.FEITO_CACA) if oficio == 'caça' else (K.COLETA_BLOCOS, K.FEITO_COLETA)
    for grau in sorted(tab):
        quer = talento.pede(p, oficio, tab, grau)                         # os blocos vezes o talento (etapa da magia), até o teto dele
        if grau <= tem: continue
        if quer is None:
            if bl >= tab[grau]: txt = f" (a mão não sobe mais em {oficio}: o talento para em {T.MAESTRIAS[talento.teto(p, oficio)]})"
            break
        if bl < quer: continue
        if grau in feito and p.get('marca', {}).get(f'feito_{oficio}', -1) < feito[grau]:
            o_que = f"ficar com a carcaça de um bicho {T.CATS[feito[grau]]} ou maior" if oficio == 'caça' else f"tirar matéria {FEM[feito[grau]]} com a própria mão"
            txt = f" (tem os blocos para {T.MAESTRIAS[grau]} em {oficio}; falta o feito: {o_que})"; break
        estado.aplica(E, 'treinar', [['pessoa', pid, 'maestria.' + oficio, 'poe', grau]], onde=p['lugar'], quem=[pid], texto=f"{p['nome']} chega a {T.MAESTRIAS[grau]} em {oficio}")
        p = E['gente'][pid]; tem = grau; txt = f'. MAESTRIA: {T.MAESTRIAS[grau]} em {oficio}'
    return txt


# ---------- a saída ----------
def _abre(E, pid, quer, ermo, alvo, blocos, com=()):
    p = _vivo(E, pid); aqui = p['lugar']
    if vai_com(p): sys.exit(f"{p['nome']} foi junto na saída de {E['gente'].get(vai_com(p), {}).get('nome', vai_com(p))}: não abre outra")
    if saida(p): sys.exit(f"{p['nome']} já tem uma saída aberta ({_agora(E, pid)}). Feche-a antes: `caca.py volta`")
    viz = ermos(E, aqui)
    if ermo is None:
        if len(viz) != 1: sys.exit(f"diga a que ermo ({', '.join(viz)})" if viz else f"{E['lugares'][aqui]['nome']} não tem ermo vizinho: não há aonde sair")
        ermo = viz[0]
    elif ermo not in viz: sys.exit(f'"{ermo}" não é um ermo vizinho de {E["lugares"][aqui]["nome"]}' + (f" (os que há: {', '.join(viz)})" if viz else ' (não há nenhum)'))
    l = E['lugares'][ermo]
    aviso = None
    if quer == 'caça':
        if alvo is not None: alvo = _especie(alvo)
        if not tem_caca(E, ermo): sys.exit(f"{_cap(l['nome'])} não tem caça")
        if alvo is not None: aviso = _nao_vive(E, ermo, alvo)
    else:
        nome, cat = M.le_materia(alvo or '')
        if nome not in K.COLETA or cat is None or cat > M.MATERIA_ATE: sys.exit(f'não se coleta "{alvo}" (coleta-se: {", ".join(n + ":0" for n in K.COLETA)}; o número é a categoria, de 0 a {M.MATERIA_ATE})')
        if alvo not in coleta_teto(E, ermo): sys.exit(f"{_cap(l['nome'])} não dá {_bem(alvo)}" + (f" (dá: {', '.join(_bem(b) for b in coleta_teto(E, ermo))})" if coleta_teto(E, ermo) else ''))
        if coleta_pede(p, alvo) is not None:
            pede = K.COLETA_BLOCOS[coleta_pede(p, alvo)]; tem = (p.get('treino') or {}).get('coleta', 0)
            sys.exit(f"{p['nome']} não tem mão para tirar {_bem(alvo)}: pede {T.MAESTRIAS[coleta_pede(p, alvo)]} em coleta ({pede} blocos de coleta" + (f"; {p['nome']} tem {tem:g}: {_s(pede - tem, 'falta', 'faltam')} {pede - tem:g}" if tem < pede else '')
                     + f"); a mão de {p['nome']} é de {T.MAESTRIAS.get(mao(p, 'coleta'), mao(p, 'coleta'))}")
    try: n = K.PROCURA if blocos is None else int(blocos)
    except ValueError: n = 0
    teto = K.PROCURA_MAX if quer == 'caça' else K.COLETA_MAX
    if not 1 <= n <= teto: sys.exit(f'os blocos de {"procura" if quer == "caça" else "coleta"} de uma saída vão de 1 a {teto} (veio "{blocos}"). Um bloco são 4 horas.')
    com = list(dict.fromkeys(com))
    for c in com:
        q = E['gente'].get(c) or sys.exit(f'não há a pessoa "{c}"')
        if c == pid or q['estado'] != 'vivo' or q['lugar'] != aqui or (q.get('marca') or {}).get('caca'): sys.exit(f"{q['nome']} não pode ir junto (só vai quem vive, está {_em(E, aqui)} e não tem saída aberta)")
    estado.sem_luta(E)
    for c in [pid] + com: estado.em_cena(E, c)                 # quem não é o personagem volta à cena: ANTES de mais nada, o tempo que passou em casa (comeu, dormiu, sarou)
    p = E['gente'][pid]; cansados = [x for x in (nao_inteiro(E, c) for c in com) if x]
    ida = longe(E, ermo); o_que = _o_que(alvo) if quer == 'caça' else _bem(alvo)
    s = dict(ermo=ermo, casa=aqui, quer=quer, alvo=alvo, restam=n, com=com, dia=E['relogio']['dia'], fase='procura', encontro=None, luta=None, lutas=0, parou=None, sangue=None)
    txt = f"{p['nome']} sai para {'caçar' if quer == 'caça' else 'tirar'} {o_que} {_em(E, ermo)}" + (f", com {_e(E['gente'][c]['nome'] for c in com)}" if com else '')
    estado.aplica(E, EVENTO[quer], [['pessoa', pid, 'marca.caca', 'poe', s]] + [['pessoa', c, 'marca.caca', 'poe', dict(de=pid, ermo=ermo)] for c in com], onde=ermo, quem=[pid] + com, texto=txt)
    antes = corpo.faixas(E['gente'][pid])
    ato.passa(E, pid, ida, EVENTO[quer], esforco=K.ESFORCO['ida'], para=False, texto=f"{p['nome']} vai ao ermo ({l['nome']})", com=com)
    L = ([aviso] if aviso else []) + [f"{txt}: {_bl(ida)} de ida, {n} de {'procura' if quer == 'caça' else 'coleta'}, {ida} de volta."]
    if cansados: L.append(f"ATENÇÃO, quem vai junto não vai {_s(len(cansados), 'inteiro', 'inteiros')}: " + '; '.join(cansados) + '.')
    merenda(E, com, L)
    if E['gente'][pid]['estado'] == 'vivo' and corpo.cruzou(E['gente'][pid], antes): L.append(f"No caminho: {corpo.cruzou(E['gente'][pid], antes)}.")
    dv = _devolve_aqui(E, pid, ermo)
    if dv: return _pausa(E, pid, f"{E['gente'][pid]['nome']} chegou {_em(E, ermo)} com {dv['nome']}, que é daqui", L, mais=f"`maldicao.py devolver {dv['id']}` deixa a peça no lugar dela; `caca.py segue` segue a procura")
    return _anda(E, pid, L)


def _devolve_aqui(E, pid, ermo):
    """a peça maldita que a pessoa leva e que é DESTE ermo, quando ela sabe que devolvê-la quebra a maldição (alguém leu): a saída para na chegada, para dar tempo de devolver"""
    try: import maldicao
    except ImportError: return None
    L_ = E['itens']['itens']
    for m in maldicao.minhas(E['gente'][pid]):
        c = m.get('condicao') or {}
        if m.get('de') == 'peça' and c.get('tipo') == 'devolver' and c.get('onde') == ermo and maldicao.degrau(m) == 2 and L_.get(c.get('item'), {}).get('dono') == pid: return L_[c['item']]
    return None


def _o_que(alvo): return 'a toca de um bando' if alvo == TOCA else _E(alvo)['nome'] if alvo else 'o que aparecer'


def _nao_vive(E, ermo, alvo):
    """o alvo que não vive ali. Do bicho que não é chefe, o povo sabe o que cada ermo tem: se ali nunca houve, a saída é RECUSADA antes de gastar um bloco.
    Do chefe ninguém sabe de graça (acha-se no rastro): a saída segue, e só se AVISA quando a espécie não é bicho daquele tipo de ermo. O aviso sai do tipo
    do ermo e da espécie, nunca da contagem: é o mesmo, haja ou não um chefe ali."""
    if alvo == TOCA: return None                            # da toca ninguém sabe de graça (acha-se no rastro): a saída segue
    e = _E(alvo); l = E['lugares'][ermo]; hab = l.get('habitat')
    if not e['chefe']:
        if alvo in teto_de(E, ermo) or alvo in bichos_de(E, ermo): return None
        ha = sorted({x for x in set(teto_de(E, ermo)) | set(bichos_de(E, ermo)) if not _E(x)['chefe']}, key=lambda x: (_E(x)['cat'], x))
        sys.exit(f"{_cap(l['nome'])} não tem {e['nome']}: todo mundo sabe o que vive ali" + (f" ({', '.join(_E(x)['nome'] for x in ha)})" if ha else '') + ". Sem `alvo=`, procura-se o que aparecer.")
    if hab in K.HABITATS and hab not in e['habitat']:
        return f"AVISO: {_nome(alvo)} é bicho de {_ou(e['habitat'])}, e {l['nome']} é {hab}. Não é lugar onde se espere achar rastro {'dela' if e['artigo'] == 'a' else 'dele'}: a procura pode ser em vão."
    return None


def sair(E, pid, ermo=None, alvo=None, blocos=None, com=()):
    """sai para caçar no ermo vizinho: a ida, e a procura bloco a bloco até aparecer alguma coisa (aí PARA, e o caçador lê a ameaça), até o corpo pedir,
    ou até os blocos acabarem (aí volta sozinho). alvo: a espécie que se procura (None: o que aparecer). com: quem vai junto (entra na luta)."""
    return _abre(E, pid, 'caça', ermo, alvo, blocos, com)


def coletar(E, pid, bem, ermo=None, blocos=None, com=()):
    """sai para tirar matéria (\"metal:0\", \"madeira:1\", \"erva:0\") do ermo vizinho: a ida, os blocos de coleta (um teste cada), a volta"""
    return _abre(E, pid, 'coleta', ermo, bem, blocos, com)


def _anda(E, pid, L):
    """a procura (ou a coleta) segue, bloco a bloco: até aparecer alguma coisa, o corpo pedir, ou os blocos acabarem (aí a volta sai sozinha)"""
    while True:
        p = E['gente'][pid]; s = saida(p)
        if p['estado'] != 'vivo': return _morreu(E, pid, L)
        if s['restam'] <= 0: return volta(E, pid, L)
        R = (_bloco_caca if s['quer'] == 'caça' else _bloco_coleta)(E, pid, L)
        if R: return R


def _quantos(E, lid, esp, chave):
    """quantos aparecem: o bando da espécie (o acaso do mundo), nunca mais do que a contagem real"""
    return min(bichos_de(E, lid).get(esp, 0), len(bichos.bando(esp, estado.sorte(E, chave))))


def _bloco_caca(E, pid, L):
    """um bloco de procura: o tempo passa, e sai o teste do rastro. Devolve o que parou a procura, ou None."""
    p = E['gente'][pid]; s = dict(saida(p)); ermo = s['ermo']; alvo = s['alvo']; escuro = E['relogio']['bloco'] in M.ESCUROS
    s.update(restam=s['restam'] - 1, parou=None, sangue=None)
    _, pq = ato.passa(E, pid, 1, 'cacar', esforco=K.ESFORCO['procura'], texto=f"{p['nome']} procura rastro {_em(E, ermo)}", com=s['com'],
                      mais=lambda i: [['pessoa', pid, 'treino.caça', 'soma', 1], ['pessoa', pid, 'marca.caca', 'poe', s]])
    p = E['gente'][pid]
    if p['estado'] != 'vivo': return None
    merenda(E, s['com'], L); p = E['gente'][pid]
    if pq and ato_caiu(pq, p): return _pausa(E, pid, pq, L) if s['restam'] > 0 else L.append(f'PAROU: {pq}.')        # caiu no sono no meio do bloco: não há rastro a ler
    cv = covil_de(E, ermo); toca = alvo == TOCA
    contra = (rastro_contra(E, ermo, cv['especie']) if cv else K.RASTRO_BASE) + _tc_toca() if toca else rastro_contra(E, ermo, alvo)
    o_que = _o_que(alvo); B = bichos_de(E, ermo); enc = None
    # ATRÁS DE CHEFE (OU DA TOCA) A ROLAGEM É OCULTA: o número do rastro muda com a contagem (há um, não há), e do chefe ninguém sabe de graça. À mesa sai só "rolagem oculta"; o número fica com o Mestre
    r = teste.rola(E, f"rastrear {o_que} {_em(E, ermo)}" + (', no escuro' if escuro else ''), 'Percepção', contra, mais=mao(p) + talento.dom_visto(p, 'caça') + (K.RASTRO_ESCURO if escuro else 0), quem=pid, oculto=bool(toca or (alvo and _E(alvo)['chefe'])), **talento.kw(p, 'caça'))
    _dom_mostra(E, pid, r, ermo); L.append(teste.diz(E, r))
    if r['passou']:
        _acha(E, pid, ermo, L)
        if toca:
            n = B.get(cv['especie'], 0) if cv else 0
            if n >= 1: enc = dict(especie=cv['especie'], n=n, viu='caçador', margem=int(r['total'] - contra), escuro=escuro, toca=True)
            else: L.append('Nenhuma toca: você procurou bem, e aqui não há bando morando.' if not cv else 'A toca está vazia: o bando foi embora, ou morreu.')
        else:
            esp = alvo or _sorteia(B, estado.sorte(E, f'caca|{pid}|aparece'))
            if esp and B.get(esp, 0) >= 1: enc = dict(especie=esp, n=_quantos(E, ermo, esp, f'caca|{pid}|bando'), viu='caçador', margem=int(r['total'] - contra), escuro=escuro)
            elif alvo and alvo not in teto_de(E, ermo): L.append(f"Nenhum sinal de {_E(alvo)['nome']}: você procurou bem, e aqui não há.")
            else: L.append('O rastro é velho: não há nada no fim dele.')
    else:
        rs = estado.sorte(E, f'caca|{pid}|acaso')
        if rs.random() < acaso(E, ermo):
            esp = _sorteia({e: q * K.indole(e)[0] for e, q in B.items()}, rs)
            if esp: enc = dict(especie=esp, n=_quantos(E, ermo, esp, f'caca|{pid}|bando'), viu='bicho', margem=0, escuro=escuro)
        if not enc: L.append('Nenhum rastro neste bloco.')
    if enc:
        if pq: L.append(f'O corpo: {pq}.')
        return _encontro(E, pid, enc, L)
    if pq and s['restam'] > 0: return _pausa(E, pid, pq, L)
    return None


def _tc_toca():
    import tabelas_criaturas as TC
    return TC.RASTRO_TOCA


def _nomes_chefes():
    """os nomes dos chefes das criaturas (o chefe da toca não sai da contagem do ermo: mora no registro do covil)"""
    try: import tabelas_criaturas as TC
    except ModuleNotFoundError: return set()
    return {C['nome'] for C in TC.CHEFES.values() if C.get('nome')}


def ato_caiu(pq, p): return (pq or '').startswith(f"{p['nome']} cai no sono")         # o ato parou porque QUEM AGIA caiu no sono (e já dormiu ali, no chão: ato.passa); o personagem que esperava e caiu no sono não conta aqui


def do_morto(E, ermo):
    """o que os mortos deixaram neste ermo: (os ids das peças soltas que ficaram com um corpo, o que ficou no chão: a carga e a prata, os nomes dos mortos)"""
    l = E['lugares'][ermo]; pecas = [i for i, it in E['itens']['itens'].items() if it.get('onde') == ermo and estado.de_morto(it)]
    chao = {} if l.get('pop') or covil_de(E, ermo) else {b: q for b, q in _num(l.get('estoque')).items() if q > 0}     # num lugar com povo, o povo fica com a carga e a prata do morto; num ermo com toca, o bando junta
    quem = list(dict.fromkeys(c for c in (E['itens']['itens'][i].get('corpo') for i in pecas) if c in E['gente']))
    if chao or not quem: quem = list(dict.fromkeys(quem + [k for k, q in E['gente'].items() if q['estado'] == 'morto' and (q.get('morte') or {}).get('onde') == ermo]))
    return pecas, chao, [E['gente'][k]['nome'] for k in quem]


def _acha(E, pid, ermo, L):
    """quem passa num rastro acha o que está SOLTO no chão do ermo (no Livro de Itens, com `onde` ali, sem dono e com a marca `solto`).
    O núcleo da carcaça que ninguém abriu e a peça largada passam a ser dele (as peças vão guardadas, não vestidas). O que não está solto é de uma loja: não se acha.
    O QUE ERA DE UM MORTO (as peças que ficaram com o corpo; a carga e a prata, no chão) NÃO MUDA DE MÃO SOZINHO: ele acha o corpo e lê o que há ali, uma vez por saída.
    Quem fica com o quê é decisão de cena, e entra por evento do Mestre."""
    p = E['gente'][pid]
    for iid, it in list(E['itens']['itens'].items()):
        if it.get('onde') == ermo and not it.get('dono') and it.get('solto') and not estado.de_morto(it):
            de_que = 'numa carcaça velha' if it.get('tipo') == 'nucleo' else 'no chão'          # palavras que servem a nome masculino e feminino ("a Espada", "o núcleo")
            estado.aplica(E, 'despojo', [['item', iid, 'dono', 'poe', pid], ['item', iid, 'historia', 'junta', f"Dia {E['relogio']['dia']}: {p['nome']} achou {'este núcleo' if it.get('tipo') == 'nucleo' else 'esta peça'} {de_que}, {_em(E, ermo)}"]],
                          onde=ermo, quem=[pid], texto=f"{p['nome']} acha {it['nome']} {de_que}, {_em(E, ermo)}")
            L.append(f"  ACHADO {de_que}: {it['nome']} ({iid}, {T.CATS[it['cat']]}). Agora é de {p['nome']}.")
    pecas, chao, nomes = do_morto(E, ermo); s = saida(p)
    if not (pecas or chao) or not s: return
    visto = [len(pecas), sum(chao.values())]
    if s.get('corpo') == visto: return                      # já viu, nesta saída, o que há ali: não se repete a cada rastro
    de_quem = (('o corpo de ' if len(nomes) == 1 else 'os corpos de ') + _e(nomes)) if nomes else 'o que um morto deixou'
    _marca(E, pid, dict(s, corpo=visto), f"{p['nome']} acha {de_quem} {_em(E, ermo)}")
    junto = [f"{E['itens']['itens'][i]['nome']} ({i}, {T.CATS[E['itens']['itens'][i]['cat']]})" for i in pecas]
    no_chao = [f"{q:g} de {'prata' if b == 'prata' else _bem(b)}" for b, q in chao.items()]
    L.append(f"  ACHADO: {de_quem}." + (f" Ali ficaram: {', '.join(junto)}." if junto else '') + (f" No chão: {_e(no_chao)}." if no_chao else ''))
    L.append("  O que era de um morto não muda de mão sozinho: quem fica com o quê é decisão de cena, e o Mestre registra (`itens.py dono ITEM PESSOA`, `estado.py mestre`).")


def _bloco_coleta(E, pid, L):
    """um bloco de coleta: o tempo passa, sai o teste, e o que se tira sai do ermo e entra na carga no mesmo evento. Pode aparecer bicho."""
    p = E['gente'][pid]; s = dict(saida(p)); ermo = s['ermo']; bem = s['alvo']; nome, cat = M.le_materia(bem); tab = K.COLETA[nome]; escuro = E['relogio']['bloco'] in M.ESCUROS
    s.update(restam=s['restam'] - 1, parou=None, sangue=None)
    _, pq = ato.passa(E, pid, 1, 'coletar', esforco=K.ESFORCO['coleta'], texto=f"{p['nome']} tira {tab['nome']} {_em(E, ermo)}", com=s['com'],
                      mais=lambda i: [['pessoa', pid, 'treino.coleta', 'soma', 1], ['pessoa', pid, 'marca.caca', 'poe', s]])
    p = E['gente'][pid]
    if p['estado'] != 'vivo': return None
    merenda(E, s['com'], L); p = E['gente'][pid]
    if pq and ato_caiu(pq, p): return _pausa(E, pid, pq, L) if s['restam'] > 0 else L.append(f'PAROU: {pq}.')        # caiu no sono no meio do bloco: não tirou nada
    contra = coleta_contra(E, ermo, bem); ha = int(coleta_de(E, ermo).get(bem, 0))
    r = teste.rola(E, f"tirar {_bem(bem)} {_em(E, ermo)}", tab['atributo'], contra, mais=mao(p, 'coleta') + talento.dom_visto(p, 'coleta'), quem=pid, **talento.kw(p, 'coleta')); m = r['total'] - contra
    _dom_mostra(E, pid, r, ermo); L.append(teste.diz(E, r))
    q = coleta_rende(bem, m, ha)
    if q > 0:
        ef = [['lugar', ermo, 'coleta.' + bem, 'soma', -q], ['pessoa', pid, 'carga.' + bem, 'soma', q]]
        if p.get('marca', {}).get('feito_coleta', -1) < cat: ef.append(['pessoa', pid, 'marca.feito_coleta', 'poe', cat])
        estado.aplica(E, 'coletar', ef, onde=ermo, quem=[pid], texto=f"{p['nome']} tira {q} de {_bem(bem)} {_em(E, ermo)}")
        L.append(f"  Tirou {q} de {_bem(bem)}.")
    else: L.append('  Não rendeu nada.' if ha else f"  Não há mais {_bem(bem)} aqui: esgotou.")
    rs = estado.sorte(E, f'caca|{pid}|acaso'); B = bichos_de(E, ermo)
    if rs.random() < acaso(E, ermo):
        esp = _sorteia({e: n * K.indole(e)[0] for e, n in B.items()}, rs)
        if esp: return _encontro(E, pid, dict(especie=esp, n=_quantos(E, ermo, esp, f'caca|{pid}|bando'), viu='bicho', margem=0, escuro=escuro), L + ([f'O corpo: {pq}.'] if pq else []))
    if pq and s['restam'] > 0: return _pausa(E, pid, pq, L)
    return None


def _pausa(E, pid, pq, L, mais=''):
    """o corpo pediu (ou a peça maldita chegou em casa): a procura para, e o caçador escolhe seguir ou voltar. O fato (o registro, o RETOMAR) é a frase; o que dá para fazer
    (`mais`, os comandos) só vai à saída do comando"""
    s = dict(saida(E['gente'][pid]), parou=pq); _marca(E, pid, s, f"a {'coleta' if s.get('quer') == 'coleta' else 'procura'} para: {pq}")
    L.append(f"PAROU: {pq}." + (f" {mais}." if mais else '') + f" {_resta(s['restam'])}")
    return dict(fase='procura', parou=pq, texto='\n'.join(L))


def _le_encontro(E, pid, enc, restam):
    """o que o caçador lê quando o bicho aparece: a ameaça (com a conta do que ele veste), o que a posição dá, e as escolhas"""
    esp = enc['especie']; n = enc['n']; arma, armadura = _veste(E, pid); inis, nv, _ = posicao(enc)
    if enc.get('toca'):
        import criaturas
        s0 = saida(E['gente'][pid]); L = ['ACHOU A TOCA' + ('. Está ESCURO: a luta terá −4 no golpe e −8 no tiro (o bando vê no escuro).' if enc.get('escuro') else '.'), criaturas.ameaca_toca(E, s0['ermo'], arma=arma, armadura=armadura)]
    else:
        L = [('A PRESA FERIDA, no fim do sangue: ' if enc.get('feridos') else _s(n, 'APARECE: ', 'APARECEM: ') if enc['viu'] == 'caçador' else _s(n, 'APARECE, E VIU VOCÊ: ', 'APARECEM, E VIRAM VOCÊ: ')) + _nome(esp, n) + (' (PV ' + ', '.join(str(f['pv']) for f in enc['feridos']) + ')' if enc.get('feridos') else '') + ('. Está ESCURO: a luta terá −4 no golpe e −8 no tiro.' if enc.get('escuro') else '.'), bichos.ameaca(esp, n=n, arma=arma, armadura=armadura)]
    if enc['viu'] == 'caçador':
        L.append(f"VOCÊ VIU PRIMEIRO (o rastro passou por {enc['margem']}): se atacar, {_s(n, 'o bicho perde', 'os bichos perdem')} o primeiro turno, e a luta começa {_ou(inis)}."
                 + (f" Terreno: {nv} {_s(nv, 'vantagem', 'vantagens')} à escolha: " + ' · '.join(f'{k} ({v})' for k, v in K.VANTAGEM_DIZ.items()) + '.' if nv else ' Sem vantagem de terreno.'))
        L.append(f"ESCOLHA: `caca.py atacar [inicio={'|'.join(inis)}]" + (f" [vantagem={'|'.join(K.VANTAGENS)}]" + (' (até duas, com vírgula)' if nv > 1 else '') if nv else '') + f"` · `caca.py deixar` ({'segue a procura: ' + _s(restam, 'resta', 'restam') + ' ' + _bl(restam) if restam > 0 else _s(n, 'deixa o bicho ir', 'deixa os bichos irem') + '; não resta bloco de procura: é a volta'}) · `caca.py fugir` (larga a caçada e volta)")
    else:
        agil = _E(esp)['atributos']['Agilidade'] // 10
        L.append(f"ESCOLHA: `caca.py atacar` (a luta começa {K.INICIO_ACASO}; ninguém é surpreendido) · `caca.py deixar` (fica onde está: {_s(n, 'ele pode', 'eles podem')} investir, e aí a luta é a mesma) · "
                 f"`caca.py fugir` (larga a caçada; se {_s(n, 'ele vier', 'eles vierem')} atrás, Agilidade contra {K.FUGA_BASE + agil}: se {_s(n, 'ele alcançar', 'eles alcançarem')} você, a luta começa {K.INICIO_ALCANCADO} e você perde o primeiro turno)")
    return L


def _encontro(E, pid, enc, L):
    s0 = saida(E['gente'][pid]); enc = dict(enc)
    if enc['viu'] == 'bicho':                               # o acaso do mundo decide AGORA, no bloco em que o bicho aparece, e fica escrito: passar tempo não rola de novo
        ind = K.indole(enc['especie'])[1]
        enc['investe'] = estado.sorte(E, f"caca|{pid}|investe|{s0['restam']}|{s0['lutas']}").random() < ind
        enc['persegue'] = estado.sorte(E, f"caca|{pid}|persegue|{s0['restam']}|{s0['lutas']}").random() < min(1.0, ind + K.INVESTE_FUGA)
    s = dict(s0, fase='encontro', encontro=enc, parou=None)
    _marca(E, pid, s, (f"{E['gente'][pid]['nome']} acha a toca {_em(E, s['ermo'])}" if enc.get('toca') else f"{_s(enc['n'], 'aparece', 'aparecem')} {_nome(enc['especie'], enc['n'])} {_em(E, s['ermo'])}") + (_s(enc['n'], ' (viu o caçador)', ' (viram o caçador)') if enc['viu'] == 'bicho' else ''))
    return dict(fase='encontro', encontro=dict(enc), texto='\n'.join(L + _le_encontro(E, pid, enc, s['restam'])))


def _no_encontro(E, pid):
    p, s = _minha(E, pid)
    if s['fase'] != 'encontro': sys.exit(f"não há bicho à frente de {p['nome']} agora ({_agora(E, pid)})")
    return p, s, s['encontro']


def atacar(E, pid, inicio=None, vantagens=()):
    """ataca o que apareceu: confere o que a posição dá, monta o cenário e abre a luta (a do ato.py luta). Devolve o quadro."""
    p, s, enc = _no_encontro(E, pid); inis, nv, surp = posicao(enc); vs = list(dict.fromkeys(vantagens))
    ini = inicio or (K.INICIO_PADRAO if K.INICIO_PADRAO in inis else inis[0])
    if ini not in inis: sys.exit(f'esta luta não começa "{ini}": começa {_ou(inis)}' + ('' if enc['viu'] == 'caçador' else ' (o bicho viu você)'))
    ruins = [v for v in vs if v not in K.VANTAGENS]
    if ruins: sys.exit(f'vantagem desconhecida: "{ruins[0]}" (as que há: {", ".join(K.VANTAGENS)})')
    if len(vs) > nv: sys.exit(f"a posição dá {nv} {_s(nv, 'vantagem', 'vantagens')} de terreno (uma a cada {K.POSICAO_CADA} pontos de margem no rastro, até {K.POSICAO_MAX}); vieram {len(vs)}")
    return _luta_abre(E, pid, ini, {K.VANTAGENS[v][0]: K.VANTAGENS[v][1] for v in vs}, surp, vs, [])


def _luta_abre(E, pid, ini, lugar, surp, vs, L):
    """monta o cenário (a casa: o caçador e quem veio junto; o outro lado: os bichos, tirados da contagem real) e chama o ato.luta_nova"""
    p = E['gente'][pid]; s = dict(saida(p)); enc = dict(s['encontro']); esp = enc['especie']; n = min(enc['n'], bichos_de(E, s['ermo']).get(esp, 0))
    if n < 1:                                               # não há mais nenhum (o Mestre mexeu na contagem no meio da saída): o encontro se desfaz
        s.update(fase='procura', encontro=None); _marca(E, pid, s, 'o bicho não está mais lá'); return _anda(E, pid, L + ['Não há mais nada ali.'])
    k = s['lutas'] + 1
    if enc.get('toca'):                                     # a toca: o chefe e a guarda, o líder e o resto (criaturas.toca), em forma curta (o luta.cenario os refaz)
        import criaturas
        B = [criaturas.no_cenario(b) for b in criaturas.toca(E, s['ermo'], n)]
    else: B = bichos.bando(esp, estado.sorte(E, f'caca|{pid}|luta|{k}'), n=n)
    if not enc.get('toca') and esp not in TB.ESPECIES:      # a criatura de povo vai em forma curta ({"bicho": ESPECIE, "posto": ...}): o luta.cenario a refaz pelo bichos.bicho
        import criaturas
        B = [criaturas.no_cenario(b) for b in B]
    for b, fd in zip(B, enc.get('feridos') or []): b['pv'] = fd['pv']; b['feridas'] = [list(x) for x in fd['feridas']]       # a presa que fugiu ferida volta com o PV e as feridas com que fugiu
    A = [dict(id=pid, controla=True)] + [dict(id=c) for c in s['com'] if E['gente'].get(c, {}).get('estado') == 'vivo']
    pasta = os.path.join(estado.pasta(), 'lutas'); os.makedirs(pasta, exist_ok=True); base = os.path.join(pasta, f"caca_{pid}_d{E['relogio']['dia']}b{E['relogio']['bloco']}_{k}")
    escuro = bool(enc.get('escuro'))                           # a luz é a do bloco em que o bicho apareceu (o relógio já andou até o fim dele)
    json.dump(dict(inicio=ini, lugar=lugar, surpresa=surp, tempo=['escuro'] if escuro else [], luz=not escuro, ermo=s['ermo'], A=A, B=B), open(base + '_cenario.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)      # o ermo: o "chamar" do druida vale nele
    quadro = ato.luta_nova(E, base + '_cenario.json', base + '_luta.json')
    enc.update(n=n, inicio=ini, vantagens=vs, surpresa=surp); s.update(fase='luta', luta=estado.arq_guarda(base + '_luta.json'), lutas=k, encontro=enc)
    _marca(E, pid, s, f"{p['nome']} luta com {_nome(esp, n)} {_em(E, s['ermo'])} (começa {ini}" + (f", {', '.join(vs)}" if vs else '') + ({'A': ', e perde o primeiro turno', 'B': _s(n, ', o bicho surpreendido', ', os bichos surpreendidos')}.get(surp, '')) + ')')
    L = L + [f"A LUTA ABRE: {p['nome']} contra {_nome(esp, n)}, começando {ini}" + (f"; terreno: {', '.join(vs)}" if vs else '') + ({'A': _s(n, '; a surpresa é do bicho', '; a surpresa é dos bichos') + ': VOCÊ perde o primeiro turno', 'B': _s(n, '; o bicho foi surpreendido (perde o primeiro turno)', '; os bichos foram surpreendidos (perdem o primeiro turno)')}.get(surp, '')) + '.',
             quadro, f'Siga com `caca.py luta "{p["nome"]}: atacar"` (ou `ato.py luta roda {s["luta"]} "{p["nome"]}: ordem"`); acabada a luta, `caca.py segue` ou `caca.py volta`.']
    return dict(fase='luta', luta=_arq(s), encontro=enc, texto='\n'.join(L))


def deixar(E, pid):
    """deixa o bicho. O que não viu o caçador segue o caminho dele; o que viu pode investir (o acaso do mundo, pela índole da espécie). Depois, a procura segue."""
    p, s, enc = _no_encontro(E, pid); esp = enc['especie']; n = enc['n']; L = []
    if enc['viu'] != 'caçador':
        if enc.get('investe', False):
            return _luta_abre(E, pid, K.INICIO_ACASO, {}, None, [], [f"{_nome(esp, n).capitalize()} não {_s(n, 'deixa', 'deixam')}: {_s(n, 'INVESTE', 'INVESTEM')}."])
        L.append(f"{_nome(esp, n).capitalize()} {_s(n, 'olha e vai', 'olham e vão')} embora.")
    else: L.append(f"{p['nome']} deixa {_nome(esp, n)} ir.")
    s = dict(s, fase='procura', encontro=None); _marca(E, pid, s, f"{p['nome']} deixa {_nome(esp, n)}")
    return _anda(E, pid, L)


def fugir(E, pid):
    """larga a caçada e volta. Do bicho que não viu o caçador, sem teste. Do que viu: ele pode vir atrás (a índole, mais o que a corrida chama); aí é Agilidade
    contra a dele: quem passa, escapa; quem falha é alcançado, e luta colado e surpreendido."""
    p, s, enc = _no_encontro(E, pid); esp = enc['especie']; n = enc['n']; L = []
    if enc['viu'] != 'caçador':
        if enc.get('persegue', False):
            contra = K.FUGA_BASE + _E(esp)['atributos']['Agilidade'] // 10
            r = teste.rola(E, TB.contrai(f"fugir de {_nome(esp, n)}"), 'Agilidade', contra, quem=pid); L += [f"{_nome(esp, n).capitalize()} {_s(n, 'vem', 'vêm')} atrás.", teste.diz(E, r)]
            if not r['passou']:
                s = dict(s, encontro=dict(enc, viu='alcançado')); _marca(E, pid, s, f"{_nome(esp, n)} {_s(n, 'alcança', 'alcançam')} {p['nome']}")
                return _luta_abre(E, pid, K.INICIO_ALCANCADO, {}, 'A', [], L + [f"{_nome(esp, n).capitalize()} {_s(n, 'ALCANÇA', 'ALCANÇAM')} {p['nome']}."])
            L.append(f"{p['nome']} escapa.")
        else: L.append(f"{_nome(esp, n).capitalize()} não {_s(n, 'vem', 'vêm')} atrás.")
    else: L.append(f"{p['nome']} recua sem que {_s(n, 'o bicho dê', 'os bichos deem')} por isso.")
    s = dict(s, fase='procura', encontro=None); _marca(E, pid, s, f"{p['nome']} larga a caçada")
    return volta(E, pid, L)


def luta_roda(E, pid, ordens=()):
    """roda a luta aberta da saída até a próxima parada, com as ordens dadas: é o ato.luta_roda. Acabada a luta, faz as contas (acerta)."""
    p, s = _minha(E, pid, vivo=False)
    if s['fase'] != 'luta': sys.exit(f"{p['nome']} não tem luta de caça aberta")
    if _le_luta(s)['fim']: return acerta(E, pid)                                                  # a luta já acabou (rodada pelo `ato.py luta roda`): faltam só as contas
    out = ato.luta_roda(E, _arq(s), list(ordens))
    if _le_luta(s)['fim']: R = acerta(E, pid); R['texto'] = out + '\n\n' + R['texto']; return R
    return dict(fase='luta', luta=_arq(s), texto=out)


def _le_luta(s):
    """o arquivo da luta da saída, lido; se ele se perdeu, recusa com a frase (e diz como soltar a saída)"""
    if not os.path.exists(_arq(s)): sys.exit(f"o arquivo da luta desta saída não está em {_arq(s)}: sem ele não há contas. `caca.py larga \"por quê\"` fecha a saída sem elas (SÓ O MESTRE)")
    return json.load(open(_arq(s), encoding='utf-8'))


def acerta(E, pid):
    """A LUTA ACABOU: as contas, num evento só. Bicho morto sai da contagem (o caído é rematado por quem ficou com o campo). Se a casa ficou com o campo,
    o despojo de cada carcaça (bichos.despojo) entra na carga e o núcleo do chefe entra no Livro de Itens, com dono; se não ficou, a carcaça fica no mato,
    e o núcleo fica no ermo (no Livro, com `onde`). Quem perdeu o campo e vive volta na hora; quem ficou com ele pode seguir a procura.
    O DESPOJO É DE QUEM LUTOU ATÉ O FIM: reparte-se em partes iguais entre os da casa que acabaram a luta de pé no campo, ou caídos nele e vivos (o que sobra da divisão
    vai, uma unidade a cada um, em roda, a começar por quem comanda). Quem saiu da luta antes do fim (recuou para fora dela, fugiu, rendeu-se) não leva nada.
    O núcleo, os abates e o feito ficam com quem comanda, se ele ficou; senão, com o primeiro que ficou."""
    p, s = _minha(E, pid, vivo=False)
    if s['fase'] != 'luta': sys.exit(f"{p['nome']} não tem luta de caça para acertar")
    S = _le_luta(s)
    if not S['fim']: sys.exit(f'a luta ainda não acabou: siga com `caca.py luta "{p["nome"]}: atacar"`')
    if any(l['arq'] == s['luta'] and not l['fim'] for l in E['turno']['lutas']): ato.luta_fecha(E, S, _arq(s))       # a luta acabou no arquivo e ainda não voltou ao estado
    p = E['gente'][pid]; ermo = s['ermo']; enc = s['encontro']; esp = enc['especie']; e = _E(esp); campo = S['fim'] == 'A'
    chefes = _nomes_chefes() if enc.get('toca') else set()
    bs = [f for f in S['L'] if f['lado'] == 'B' and f['nome'] not in chefes and ', morto que anda' not in f['nome']]       # o chefe da toca não é da contagem (mora no registro do covil); o morto erguido na luta, também não
    mortos = sum(f['estado'] == 'morto' for f in bs); caidos = sum(f['estado'] == 'caido' for f in bs); fugiram = sum(f['estado'] == 'fugiu' for f in bs)
    rendidos = sum(f['estado'] == 'rendido' for f in bs) if campo and e.get('povo') else 0      # o povo que se rende a quem fica com o campo sai da contagem (vai preso, ou é rematado: a cena decide)
    saem = min(mortos + (caidos if campo else 0) + rendidos, bichos_de(E, ermo).get(esp, 0)); ef = []; bens = {}; nucleos = 0; L = []
    ficaram = [f['id'] for f in sorted((f for f in S['L'] if f['lado'] == 'A' and f['estado'] in FICOU and E['gente'].get(f.get('id'), {}).get('estado') == 'vivo'), key=lambda f: f['id'] != pid)] if campo else []
    leva = ficaram[0] if ficaram else None; partes = {q: {} for q in ficaram}                    # quem lutou até o fim (quem comanda primeiro), e a parte de cada um
    if saem: ef.append(['lugar', ermo, f'bichos.{esp}', 'soma', -saem])
    for i in range(saem):
        b, nuc = bichos.despojo(esp, estado.sorte(E, f"caca|{pid}|despojo|{s['lutas']}|{i}"))
        if leva:
            for k, q in b.items(): bens[k] = bens.get(k, 0) + q
        if nuc:
            como = TB.contrai(f"tirado de {_nome(esp)} por {E['gente'][leva]['nome']}" if leva else f"ficou na carcaça de {_nome(esp)}")
            ef.append(['item', 'nasce', dict(nuc, dono=leva, onde=None if leva else ermo, **({} if leva else dict(solto=True)), historia=[f"Dia {E['relogio']['dia']}: {como} {_em(E, ermo)}"])]); nucleos += 1
    if leva:
        vez = 0                                             # a vez de quem recebe o que sobra da divisão: roda de um bem para o outro, a começar por quem comanda
        for k, v in bens.items():
            cada, resto = divmod(v, len(ficaram))
            for i, c in enumerate(ficaram):
                n = cada + (1 if (i - vez) % len(ficaram) < resto else 0)
                if n: partes[c][k] = n
            vez = (vez + resto) % len(ficaram)
        q = E['gente'][leva]; ef += [['pessoa', c, 'carga.' + k, 'soma', v] for c in ficaram for k, v in partes[c].items()]
        if saem:
            ef.append(['pessoa', leva, 'marca.abates', 'soma', saem])
            if q.get('marca', {}).get('feito_caça', -1) < e['cat']: ef.append(['pessoa', leva, 'marca.feito_caça', 'poe', e['cat']])
    if saem: L.append(f"{_nome(esp, saem).capitalize()} {_s(saem, 'morreu', 'morreram') if not rendidos else _s(saem, 'ficou', 'ficaram') + ' no campo (' + str(rendidos) + ' ' + _s(rendidos, 'rendido', 'rendidos') + ')'}: {_s(saem, 'sai', 'saem')} da contagem {_em(E, ermo)}.")
    if enc.get('toca'):                                     # A TOCA: o líder ou o chefe que caiu muda o covil; quem ficou com o campo leva o tesouro (o estoque do ermo)
        import criaturas
        ef2, tes, L2 = criaturas.depois_da_luta(E, ermo, S, campo, ficaram); ef += ef2; L += L2
    if fugiram: L.append(f"{_nome(esp, fugiram).capitalize()} {_s(fugiram, 'fugiu', 'fugiram')}: {_s(fugiram, 'segue', 'seguem')} no ermo.")
    nuc_diz = f"{nucleos} {_s(nucleos, 'núcleo', 'núcleos')} {T.CATS[e['cat']]} (no Livro de Itens)" if nucleos else ''
    if leva and saem and len(ficaram) == 1: L.append(f"DESPOJO ({E['gente'][leva]['nome']}): {_lista(bens)}" + (f", e {nuc_diz}" if nucleos else '') + '.')
    elif leva and saem: L.append(f"DESPOJO, em partes iguais entre quem lutou até o fim: " + ' · '.join(f"{E['gente'][c]['nome']}: {_lista(partes[c])}" for c in ficaram) + (f". E {nuc_diz}, com {E['gente'][leva]['nome']}" if nucleos else '') + '.')
    elif saem: L.append('A casa não ficou com o campo: a carcaça ficou no mato.' + (f" O núcleo ficou com ela (no Livro de Itens, {_em(E, ermo)})." if nucleos else ''))
    for m in [pid] + list(s['com']):                           # quem morreu no ermo fica lá, com tudo o que era dele (a regra da morte é do estado.py)
        if E['gente'].get(m, {}).get('estado') == 'morto': L.append(f"{E['gente'][m]['nome']} morreu {_em(E, ermo)}: o que levava fica lá, com o corpo (as peças, soltas; a carga e a prata, no chão).")
    vivo = p['estado'] == 'vivo'; meu = next((f for f in S['L'] if f.get('id') == pid), {}); segue = vivo and S['fim'] in ('A', 'impasse', 'empate')
    fora_da_parte = [E['gente'][f['id']]['nome'] for f in S['L'] if f['lado'] == 'A' and f.get('id') in E['gente'] and f['id'] not in ficaram and E['gente'][f['id']]['estado'] == 'vivo'] if leva and saem else []
    if fora_da_parte: L.append(f"{_e(fora_da_parte)} {_s(len(fora_da_parte), 'saiu', 'saíram')} da luta antes do fim: não {_s(len(fora_da_parte), 'leva', 'levam')} parte do despojo.")
    feridos = [dict(pv=f['pv'], feridas=f['feridas']) for f in bs if f['estado'] == 'fugiu' and f['feridas'] and f['pv'] > 0] if campo else []
    sg = dict(especie=esp, feridos=feridos, vezes=(enc.get('perseguiu') or 0), escuro=bool(enc.get('escuro')), quando=estado.agora(E)) if feridos else None
    s2 = dict(s, fase='procura', encontro=None, luta=None, sangue=sg) if vivo else None
    quem_ficou = _e(E['gente'][c]['nome'] for c in ficaram)
    txt = (f"{quem_ficou} {_s(len(ficaram), 'fica', 'ficam')} com o campo {_em(E, ermo)}" if campo and ficaram else f"{p['nome']} " + (f"fica com o campo {_em(E, ermo)}" if campo else f"perde o campo {_em(E, ermo)}")) \
        + (f": {saem} {e['nome'] if saem == 1 else _plural(e['nome'])} a menos" if saem else '') + (f"; {_s(len(ficaram), 'leva', 'repartem')} {_lista(bens)}" if bens else '')
    estado.aplica(E, 'despojo' if saem else 'cacar', ef + [['pessoa', pid, 'marca.caca', 'poe', s2]] + (_soltam(E, s) if s2 is None else []), onde=ermo, quem=[pid] + [c for c in s['com'] if c in E['gente']], texto=TB.contrai(txt))
    if saem and campo:                                      # a maldição cuja condição é matar este bicho quebra na hora (etapa da magia), não na virada do dia
        try: import maldicao
        except ImportError: maldicao = None
        for q in ([pid] + [c for c in s['com'] if c in E['gente']]) if maldicao else []: L += maldicao.confere(E, q)
    R = dict(fim=S['fim'], campo=campo, especie=esp, eram=len(bs), mortos=saem, fugiram=fugiram, leva=leva, bens=bens, partes=partes, nucleos=nucleos, meu=meu.get('estado'), rodadas=S['r'],
             ids_nucleos=[f"i{E['itens']['seq'] - k:04d}" for k in reversed(range(nucleos))])
    if not vivo: R.update(fase='morto', texto='\n'.join(L + [f"{p['nome']} morreu {_em(E, ermo)}. A saída acaba aqui."])); return R
    R['sangue'] = len(feridos) if segue else 0
    if segue:
        if feridos: L.append(f"SANGUE: {_nome(esp, len(feridos))} {_s(len(feridos), 'fugiu ferida' if e['artigo'] == 'a' else 'fugiu ferido', 'fugiram com ferida aberta')}. `caca.py sangue` segue o rastro AGORA, sem gastar bloco "
                             f"(Percepção contra {sangue_contra(E, ermo, sg)}); seguir a procura ou voltar é largar a presa.")
        L.append(_resta(s2['restam'], ' de procura' if s['quer'] == 'caça' else ' de coleta')); R.update(fase='procura', texto='\n'.join(L)); return R
    caiu = meu.get('estado') == 'caido'
    L.append(f"{p['nome']} " + ('caiu, e o bicho largou o corpo por morto: volta arrastando-se.' if caiu else 'larga o campo e volta.'))
    V = volta(E, pid, L, arrasta=caiu); R.update(fase=V['fase'], texto=V['texto']); return R


def sangue_contra(E, lid, sg):
    """o número do rastro de sangue: o do rastro da espécie, mais fácil pelo sangue, e mais difícil a cada perseguição no mesmo bloco"""
    return rastro_contra(E, lid, sg['especie']) - K.SANGUE + K.SANGUE_ESFRIA * sg['vezes']


def sangue(E, pid):
    """segue o rastro de sangue da presa que fugiu ferida, na hora (não gasta bloco). Passou: acha o mesmo bicho, com o PV e as feridas com que fugiu,
    e viu primeiro. Falhou: perdeu-o (ele segue no ermo). Cada nova perseguição no mesmo bloco é mais difícil."""
    p, s = _minha(E, pid)
    if s['fase'] == 'luta':                                 # a luta acabou no arquivo e as contas ainda não saíram: saem agora
        R = acerta(E, pid)
        if R['fase'] != 'procura' or not R.get('sangue'): return R
        p = E['gente'][pid]; s = saida(p)
    if not s or s['fase'] != 'procura' or not s.get('sangue'): sys.exit(f"não há rastro de sangue para {p['nome']} seguir" + (f" ({_agora(E, pid)})" if s else ''))
    sg = s['sangue']; esp = sg['especie']; ermo = s['ermo']; fer = sg['feridos'][:bichos_de(E, ermo).get(esp, 0)]; contra = sangue_contra(E, ermo, sg)
    if sg.get('quando') is not None and sg['quando'] != estado.agora(E):          # o sangue é agora ou nunca: se o relógio andou, a presa ganhou o mato
        s = dict(s, sangue=None); _marca(E, pid, s, f"o rastro de sangue esfriou")
        return dict(fase='procura', texto=f"O rastro de sangue esfriou: o tempo andou, e {_nome(esp, len(sg['feridos']))} ganhou o mato. {_resta(s['restam'])}")
    r = teste.rola(E, TB.contrai(f"seguir o sangue de {_nome(esp, len(sg['feridos']))} {_em(E, ermo)}"), 'Percepção', contra, mais=mao(p) + talento.dom_visto(p, 'caça') + (K.RASTRO_ESCURO if sg['escuro'] else 0), quem=pid, **talento.kw(p, 'caça'))
    _dom_mostra(E, pid, r, ermo); L = [teste.diz(E, r)]
    if r['passou'] and fer:
        s = dict(s, sangue=None); _marca(E, pid, s, f"{p['nome']} segue o sangue")
        return _encontro(E, pid, dict(especie=esp, n=len(fer), viu='caçador', margem=int(r['total'] - contra), escuro=sg['escuro'], feridos=fer, perseguiu=sg['vezes'] + 1), L)
    s = dict(s, sangue=None); _marca(E, pid, s, f"{p['nome']} perde o rastro de sangue")
    L.append(f"O sangue some no mato: {_nome(esp, len(sg['feridos']))} {_s(len(sg['feridos']), 'escapou', 'escaparam')}. {_resta(s['restam'])}")
    return dict(fase='procura', texto='\n'.join(L))


def segue(E, pid):
    """segue a procura (ou a coleta) com os blocos que restam (depois de uma luta ganha, ou de o corpo ter pedido). Sem blocos, volta."""
    p, s = _minha(E, pid)
    if s['fase'] == 'luta': R = acerta(E, pid); return R if R['fase'] != 'procura' else _anda(E, pid, [R['texto'].rsplit('\n', 1)[0]])
    if s['fase'] == 'encontro': sys.exit('há um bicho à sua frente: `caca.py atacar`, `caca.py deixar` ou `caca.py fugir`')
    return _anda(E, pid, [])


def volta(E, pid, L=None, arrasta=False):
    """volta para casa: os blocos de volta (mais os de quem se arrasta), e a saída fecha"""
    p, s = _minha(E, pid, vivo=False); L = list(L or [])
    if s['fase'] == 'luta':                                 # a luta acabou (talvez pelo `ato.py luta roda`): PRIMEIRO as contas dela, vivo ou morto quem comanda
        R = acerta(E, pid)
        if R['fase'] != 'procura': return R
        L.append(R['texto'].rsplit('\n', 1)[0]); s = saida(E['gente'][pid])
    if p['estado'] != 'vivo': return _morreu(E, pid, L)
    if s['fase'] == 'encontro': sys.exit('há um bicho à sua frente: `caca.py atacar`, `caca.py deixar` ou `caca.py fugir` (fugir é o jeito de voltar agora)')
    n = longe(E, s['ermo']) + (K.ARRASTA if arrasta else 0); of = OFICIO[s['quer']]; antes = corpo.faixas(p)
    ato.passa(E, pid, n, EVENTO[s['quer']], esforco=K.ESFORCO['volta'], para=False, texto=f"{p['nome']} volta do ermo" + (' arrastando-se' if arrasta else ''), com=s['com'],
              mais=lambda i: [['pessoa', pid, 'marca.caca', 'poe', None]] + _soltam(E, s) if i == n - 1 else [])
    p = E['gente'][pid]
    if p['estado'] != 'vivo': return _morreu(E, pid, L, s)
    if saida(p): _marca(E, pid, None, f"{p['nome']} chega do ermo")
    merenda(E, s['com'], L); p = E['gente'][pid]
    carga = {b: q for b, q in p.get('carga', {}).items() if q}
    L.append(f"{p['nome']} volta ({_bl(n)}) e chega {_em(E, p['lugar'])}. Carrega: {_lista(carga)}" + (sobe(E, pid, of) or '.'))
    if corpo.cruzou(p, antes): L.append(f"No caminho: {corpo.cruzou(p, antes)}.")
    return dict(fase='fim', texto='\n'.join(L))


def _morreu(E, pid, L, s=None):
    """quem morre no meio da saída (de fome, no caminho) fica onde caiu, com tudo o que era dele (a regra da morte é do estado.py); a saída fecha, e quem foi junto fica solto"""
    p = E['gente'][pid]; s = saida(p) or s
    if saida(p): _marca(E, pid, None, f"{p['nome']} não volta do ermo")
    elif s and _soltam(E, s): estado.aplica(E, 'cacar', _soltam(E, s), onde=s.get('ermo'), quem=[pid], texto=f"{p['nome']} não volta do ermo")
    return dict(fase='morto', texto='\n'.join(list(L) + [f"{p['nome']} {estado.morte_diz(E, p)}: o que levava fica lá, com o corpo. A saída acaba aqui."]))


def larga(E, pid, porque):
    """SÓ O MESTRE: fecha a saída SEM as contas (o arquivo da luta se perdeu, a cena mudou de rumo). Nada sai da contagem e nada entra na carga: o que o Mestre
    decidir entra por evento "mestre". A luta aberta da saída, se houver, é dada por largada no caderno do turno."""
    p = E['gente'].get(pid) or sys.exit(f'não há a pessoa "{pid}"'); s = (p.get('marca') or {}).get('caca')
    if s is None: sys.exit(f"{p['nome']} não tem saída aberta")
    if not (porque or '').strip(): sys.exit('diga por que a saída é largada: `caca.py larga "por quê"`')
    s = s if isinstance(s, dict) else {}                    # a saída pode estar torta: larga-se assim mesmo
    for l in E['turno']['lutas']:
        if s.get('luta') and l['arq'] == s['luta'] and not l['fim']: l['fim'] = 'largada'
    soltos = [c for c in (s.get('com') if isinstance(s.get('com'), list) else []) if c in E['gente'] and (E['gente'][c].get('marca') or {}).get('caca') is not None]
    estado.aplica(E, 'mestre', [['pessoa', q, 'marca.caca', 'poe', None] for q in [pid] + soltos], onde=s.get('ermo') if s.get('ermo') in E['lugares'] else None, quem=[pid] + soltos,
                  texto=f"a saída de {p['nome']} é largada sem as contas: {porque}")
    return dict(fase='fim', texto=f"A saída de {p['nome']} foi largada sem as contas ({porque}). O que houve nela entra por `estado.py mestre`.")


def _agora(E, pid):
    """a saída aberta, numa frase: onde está e o que falta decidir"""
    p = E['gente'][pid]; s = saida(p)
    if vai_com(p): return f"foi junto na saída de {E['gente'].get(vai_com(p), {}).get('nome', vai_com(p))} {_em(E, estado.fora(E, pid) or p['lugar'])}: quem decide é quem comanda"
    if not s: return 'sem saída aberta'
    o_que = _o_que(s['alvo']) if s['quer'] == 'caça' else _bem(s['alvo'])
    base = f"{'caçando' if s['quer'] == 'caça' else 'tirando'} {o_que} {_em(E, s['ermo'])} desde o Dia {s['dia']}; {_s(s['restam'], 'resta', 'restam') + ' ' + _bl(s['restam']) if s['restam'] > 0 else 'não resta bloco'}"
    if s['fase'] == 'encontro': return base + f"; À FRENTE: {_nome(s['encontro']['especie'], s['encontro']['n'])}: `caca.py atacar`, `deixar` ou `fugir` (a ameaça e o que a posição dá: `caca.py ver`)"
    if s['fase'] == 'luta': return base + f"; EM LUTA com {_nome(s['encontro']['especie'], s['encontro']['n'])}: `caca.py luta \"{p['nome']}: atacar\"`"
    return base + (f"; parou ({s['parou']})" if s.get('parou') else '') + (f"; há SANGUE de {_nome(s['sangue']['especie'], len(s['sangue']['feridos']))}: `caca.py sangue`" if s.get('sangue') else '') + (': `caca.py segue` ou `caca.py volta`' if s['restam'] > 0 else ': `caca.py volta`')


# ---------- a virada do dia ----------
def virada(E):
    """o dia virou: em cada lugar com teto de bichos ou de matéria, os bichos criam devagar (até o teto), o chefe pode nascer, e a matéria volta devagar.
    Por dia, de cada espécie nascem contagem × cria × (1 − contagem ÷ teto). Com menos de dois, a espécie não cria: espera um casal de fora."""
    for lid in list(E['lugares']):
        B = bichos_de(E, lid); ef = []
        for esp, teto in sorted(teto_de(E, lid).items()):
            e = _E(esp); c = B.get(esp, 0)
            if c >= teto or not e.get('fera', True): continue           # a criatura que não é fera (o povo, o morto, o ser de magia) não cria aqui: o covil cria pela vida dele (criaturas.virada)
            if e['chefe']: dias = K.CHEFE_NASCE.get(e['cat'], 0); n = 1 if dias and estado.sorte(E, f'caca|{lid}|{esp}|chefe').random() < 1 / dias else 0
            elif c >= K.CRIA_MIN: n = _inteiro(E, c * K.cria(e['cat']) * (1 - c / teto), f'caca|{lid}|{esp}|cria')
            else: n = 2 if estado.sorte(E, f'caca|{lid}|{esp}|fora').random() < 1 / K.vem_de_fora(e['cat']) else 0
            n = min(n, math.ceil(teto - c))
            if n > 0: ef.append(['lugar', lid, f'bichos.{esp}', 'soma', n])
        ha = coleta_de(E, lid)
        for bem, teto in sorted(coleta_teto(E, lid).items()):
            c = ha.get(bem, 0)
            if c >= teto: continue
            n = min(_inteiro(E, teto * K.COLETA[M.le_materia(bem)[0]]['volta'], f'caca|{lid}|{bem}|volta'), math.ceil(teto - c))
            if n > 0: ef.append(['lugar', lid, f'coleta.{bem}', 'soma', n])
        if ef: estado.aplica(E, 'ninhada', ef, onde=lid, texto=f"{E['lugares'][lid].get('nome', lid)} se refaz")


# ---------- o gerador: povoar um ermo ----------
def povoa(E, lid, habitat, perigo=1, vizinho=None, longe_=None, cheio=1.0, como=''):
    """o gerador (ou o Mestre) povoa um lugar QUE JÁ EXISTE, por um evento "gera": o habitat, o perigo, o teto e a contagem de cada espécie que vive ali,
    e o teto e o que há de cada matéria (tabelas_caca.fauna e materia). vizinho: o lugar de onde se sai para ele (os dois passam a ser vizinhos).
    cheio: a fração do teto com que o ermo começa (1: cheio)."""
    l = E['lugares'].get(lid) or sys.exit(f'não há o lugar "{lid}" (criar lugar é do gerador do mundo; este comando povoa um que já existe)')
    if habitat not in K.HABITATS: sys.exit(f'habitat desconhecido: "{habitat}" (os que há: {", ".join(K.HABITATS)})')
    if not isinstance(perigo, int) or not 1 <= perigo <= len(K.PERIGOS): sys.exit(f'o perigo vai de 1 a {len(K.PERIGOS)} ({", ".join(K.PERIGOS)})')
    if e_ermo(E, lid): sys.exit(f"{l['nome']} já tem bichos ou matéria contados: não se povoa por cima")
    if vizinho is not None and (vizinho not in E['lugares'] or vizinho == lid): sys.exit(f'não há o lugar vizinho "{vizinho}"')
    fa = K.fauna(habitat, perigo); ma = K.materia(habitat, perigo); cheio = max(0.0, min(1.0, cheio))
    ef = [['lugar', lid, 'habitat', 'poe', habitat], ['lugar', lid, 'perigo', 'poe', perigo], ['lugar', lid, 'teto', 'poe', dict(fa)], ['lugar', lid, 'bichos', 'poe', {e: round(t * cheio) for e, t in fa.items()}],
          ['lugar', lid, 'coleta_teto', 'poe', dict(ma)], ['lugar', lid, 'coleta', 'poe', {b: round(t * cheio) for b, t in ma.items()}]]
    if longe_ is not None:
        if not isinstance(longe_, int) or longe_ < 1: sys.exit('os blocos de ida são 1 ou mais')
        ef.append(['lugar', lid, 'longe', 'poe', longe_])
    if vizinho is not None:
        for a, b in ((lid, vizinho), (vizinho, lid)):
            v = list(E['lugares'][a].get('vizinhos') or [])
            if b not in v: ef.append(['lugar', a, 'vizinhos', 'poe', v + [b]])
    txt = f"{l['nome']} passa a ter bichos e matéria contados ({habitat}, {K.PERIGOS[perigo - 1]}): {len(fa)} {_s(len(fa), 'espécie', 'espécies')}, {len(ma)} {_s(len(ma), 'matéria', 'matérias')}" + (f': {como}' if como else '')
    estado.aplica(E, 'gera', ef, onde=lid, texto=txt)
    return txt + '.'


# ---------- olhar ----------
def _sabe(E, lid, p=None):
    """o que todo mundo sabe de um ermo: a fartura de cada espécie (sem os chefes) e de cada matéria, em palavras (e, para a pessoa `p`, a mão que a matéria pede e ela não tem).
    A contagem é do Mestre."""
    B = bichos_de(E, lid); Tt = teto_de(E, lid); ha = coleta_de(E, lid)
    bi = [f"{_E(e)['nome']} ({K.fartura_diz(B.get(e, 0), Tt.get(e, 0)) if Tt.get(e) else 'há' if B.get(e) else 'sumiu'})" for e in sorted(set(B) | set(Tt), key=lambda e: (_E(e)['cat'], e)) if not _E(e)['chefe']]
    ma = [f"{_bem(b)} ({K.fartura_materia(ha.get(b, 0), t)}" + (f"; pede mão de {T.MAESTRIAS[coleta_pede(p, b)]}" if p and coleta_pede(p, b) is not None else '') + ')' for b, t in coleta_teto(E, lid).items()]
    return bi, ma


def ver(E, pid):
    """as linhas da caça para esta pessoa: os ermos vizinhos e o que se sabe deles, a mão dela, a saída aberta"""
    p = E['gente'][pid]; aqui = p['lugar']; viz = ermos(E, aqui); L = []
    if saida(p) or vai_com(p): L.append(f"**SAÍDA ABERTA:** {_agora(E, pid)}")
    junto = [E['gente'][c] for c in (saida(p) or {}).get('com', []) if E['gente'].get(c, {}).get('estado') == 'vivo']
    if junto: L.append('Vai junto: ' + '; '.join(f"{q['nome']} (PV {q['pv']}/{estado.pv_max(q)} · {corpo.diz(q)}" + (f" · {estado.tantos(len(q['feridas']), 'ferida aberta', 'feridas abertas')}" if q['feridas'] else '') + ')' for q in junto))
    if not viz: return L + [f"{E['lugares'][aqui]['nome']} não tem ermo vizinho: daqui não se sai para caçar nem para coletar."]
    for lid in viz:
        l = E['lugares'][lid]; bi, ma = _sabe(E, lid, p); n = longe(E, lid)
        L.append(f"**{l['nome']}**" + (f" ({l['habitat']}, {K.PERIGOS[l['perigo'] - 1]})" if l.get('habitat') in K.HABITATS and l.get('perigo') in (1, 2, 3) else '') + f", a {_bl(n)} [`{lid}`]"
                 + (' · caça: ' + ', '.join(bi) if bi else '') + (' · tira-se: ' + ', '.join(ma) if ma else ''))
    tr = p.get('treino') or {}
    L.append(f"A sua mão: caça {T.MAESTRIAS.get(mao(p), mao(p))} ({_bl(tr.get('caça', 0))}), coleta {T.MAESTRIAS.get(mao(p, 'coleta'), mao(p, 'coleta'))} ({_bl(tr.get('coleta', 0))}). "
             f"O rastro: 2d20 + {p['atributos']['Percepção'] // 10 + mao(p) + talento.dom_visto(p, 'caça') + corpo.pena(p, estado.agora(E))} contra {K.RASTRO_BASE} ou mais (o bicho arisco e o que rareou pedem mais; de noite, {K.RASTRO_ESCURO}). "
             f"A coleta: 2d20 + {p['atributos']['Força'] // 10 + mao(p, 'coleta') + talento.dom_visto(p, 'coleta') + corpo.pena(p, estado.agora(E))} (minério, madeira) ou + {p['atributos']['Percepção'] // 10 + mao(p, 'coleta') + talento.dom_visto(p, 'coleta') + corpo.pena(p, estado.agora(E))} (erva) contra {K.COLETA_BASE}, "
             f"mais {K.COLETA_CAT} por categoria, e o que rareou pede mais; o bloco que passa rende {_ou([str(t['rende']) + ' de ' + t['nome'] for t in K.COLETA.values()])}, e o que falha não rende.".replace('-', '−'))
    L.append(f"`caca.py sair [ERMO] [alvo=ESPECIE] [blocos=N]` (ida, N de procura, volta; N de 1 a {K.PROCURA_MAX}, {K.PROCURA} se não disser) · `caca.py coletar BEM [ERMO] [blocos=N]` (N de 1 a {K.COLETA_MAX})")
    return L


def conta(E, lid=None, pid=None):
    """SÓ O MESTRE: a contagem de verdade de um ermo (ou dos vizinhos de quem pergunta), o número do rastro de cada espécie e a chance do acaso"""
    lids = [lid] if lid else ermos(E, E['gente'][pid]['lugar']) if pid else [k for k in E['lugares'] if e_ermo(E, k)]; L = []
    for k in lids:
        if k not in E['lugares']: sys.exit(f'não há o lugar "{k}"')
        B = bichos_de(E, k); Tt = teto_de(E, k); ha = coleta_de(E, k); ct = coleta_teto(E, k)
        L.append(f"{E['lugares'][k]['nome']} [{k}] · acaso por bloco: {f'{acaso(E, k):.1%}'.replace('.', ',')} · rastro sem alvo: contra {rastro_contra(E, k)}")
        L += [f"  {_E(e)['nome']:<16} {B.get(e, 0):>3} de {Tt.get(e, 0):<4g} · rastro contra {rastro_contra(E, k, e)}" + (' · CHEFE' if _E(e)['chefe'] else '') for e in sorted(set(B) | set(Tt), key=lambda e: (_E(e)['cat'], e))]
        if covil_de(E, k): L.append(f"  a toca ({covil_de(E, k).get('nome', 'o covil')}): rastro contra {rastro_contra(E, k, covil_de(E, k)['especie']) + _tc_toca()} · `criaturas.py covil {k}`")
        L += [f"  {_bem(b):<16} {ha.get(b, 0):>3g} de {t:<4g} · coleta contra {coleta_contra(E, k, b)}" + (f" · pede mão de {T.MAESTRIAS[K.coleta_mao(M.le_materia(b)[1] or 0)]}" if K.coleta_mao(M.le_materia(b)[1] or 0) else '') for b, t in ct.items()]
        L += [f"  no chão ({'junto de um corpo: não muda de mão sozinho' if estado.de_morto(it) else 'solto: de quem passar num rastro'}): {it['nome']} ({i})" for i, it in E['itens']['itens'].items() if it.get('onde') == k and not it.get('dono') and it.get('solto')]
        chao = {b: q for b, q in _num(E['lugares'][k].get('estoque')).items() if q > 0}
        if chao and covil_de(E, k): L.append('  o tesouro da toca (o estoque do ermo: o que o bando juntou): ' + ', '.join(f"{q:g} de {'prata' if b == 'prata' else _bem(b)}" for b, q in chao.items()))
        elif chao and not E['lugares'][k].get('pop'): L.append('  no chão (de quem morreu ali: não muda de mão sozinho): ' + ', '.join(f"{q:g} de {'prata' if b == 'prata' else _bem(b)}" for b, q in chao.items()))
    return L or ['não há ermo contado.']


def le(E, pid):
    """o que o caçador lê agora, com o bicho à frente (a ameaça, a posição, as escolhas): para repetir à mesa depois de fechar e abrir o estado"""
    s = saida(E['gente'][pid])
    return _le_encontro(E, pid, s['encontro'], s['restam']) if s and s['fase'] == 'encontro' else []


def mesa(E):
    """as linhas da caça e da coleta para a parte PÚBLICA da MESA.md: os ermos vizinhos (o que se sabe), a saída aberta, as espécies (bichos.mesa). A contagem não sai aqui: é do Mestre (so_mestre)"""
    pid = estado.eu(E)
    if not pid: return []
    p = E['gente'][pid]; viz = ermos(E, p['lugar'])
    if not viz and not saida(p) and not vai_com(p): return []
    L = ['## A caça e a coleta'] + ['- ' + x for x in ver(E, pid)]
    return [TB.contrai(x) for x in L] + [''] + list(bichos.mesa(E))


def so_mestre(E):
    """as linhas da caça para a seção SÓ O MESTRE da MESA.md (o turno.py as põe lá): a contagem de cada ermo vizinho, com os chefes, a chance do acaso, e o que os mortos deixaram ali"""
    pid = estado.eu(E)
    if not pid: return []
    L = []
    for lid in ermos(E, E['gente'][pid]['lugar']):
        B = bichos_de(E, lid); Tt = teto_de(E, lid); pecas, chao, nomes = do_morto(E, lid)
        L.append(f"a contagem {_em(E, lid)}: " + ' · '.join(f"{_E(e)['nome']} {B.get(e, 0)}/{Tt.get(e, 0):g}" for e in sorted(set(B) | set(Tt), key=lambda e: (_E(e)['cat'], e))) + f" · acaso {acaso(E, lid):.0%} por bloco")
        if pecas or chao:
            L.append(f"junto {'do corpo' if len(nomes) == 1 else 'dos corpos'}{' de ' + _e(nomes) if nomes else ''} {_em(E, lid)} (não muda de mão sozinho: quem fica com o quê entra por evento): "
                     + _e([f"{E['itens']['itens'][i]['nome']} ({i})" for i in pecas] + [f"{q:g} de {'prata' if b == 'prata' else _bem(b)}" for b, q in chao.items()]))
    return [TB.contrai(x) for x in L]


def retomar(E):
    """a linha da caça para o RETOMAR.md: a saída que ficou aberta no fim do turno (quem a comanda, ou quem foi junto)"""
    pid = estado.eu(E)
    if not pid or E['gente'][pid]['estado'] != 'vivo' or not (saida(E['gente'][pid]) or vai_com(E['gente'][pid])): return []
    return [TB.contrai(f"**Saída aberta:** {_agora(E, pid)}")]


# ---------- a linha de comando ----------
def main(a=None):
    a = sys.argv[1:] if a is None else list(a)
    if not a: print(__doc__); return
    op = dict(x.split('=', 1) for x in a if '=' in x and ':' not in x.split('=', 1)[0] and ' ' not in x.split('=', 1)[0]); pos = [x for x in a if not ('=' in x and ':' not in x.split('=', 1)[0] and ' ' not in x.split('=', 1)[0])]
    cmds = ('ver', 'sair', 'atacar', 'luta', 'sangue', 'deixar', 'fugir', 'segue', 'volta', 'larga', 'coletar', 'conta', 'povoa')
    if not pos or pos[0] not in cmds: print(__doc__); return
    if pos[0] == 'coletar' and len(pos) < 2: sys.exit(f"diga o que tirar, com a categoria: `python3 caca.py coletar madeira:0 blocos=2` (coleta-se: {', '.join(n + ':0' for n in K.COLETA)}; 0 é Comum, 1 Incomum, 2 Rara). `caca.py ver` diz o que cada ermo dá.")
    if pos[0] == 'povoa' and len(pos) < 3: sys.exit(f"diga o lugar e o habitat: `python3 caca.py povoa ERMO HABITAT [perigo=1] [vizinho=LUGAR]` (os habitats: {', '.join(K.HABITATS)})")
    E = estado.carrega(); pid = op.get('quem') or estado.eu(E)
    if pos[0] == 'conta': print('\n'.join(conta(E, pos[1] if len(pos) > 1 else None, pid if pid in E['gente'] else None))); return
    if pos[0] == 'povoa':
        num = lambda k, pad: pad if k not in op else int(op[k]) if op[k].isdigit() else sys.exit(f'"{k}" é um número (veio "{op[k]}")')
        txt = povoa(E, pos[1], pos[2], perigo=num('perigo', 1), vizinho=op.get('vizinho'), longe_=num('longe', None), como=pos[3] if len(pos) > 3 else ''); estado.grava(E); print(txt); return
    if pid not in E['gente']: sys.exit(f'não há a pessoa "{pid}"')
    if pos[0] == 'ver': print(TB.contrai('\n'.join(ver(E, pid) + le(E, pid)))); return
    com = [c for c in op.get('com', '').split(',') if c]
    if pos[0] == 'sair': R = sair(E, pid, pos[1] if len(pos) > 1 else None, alvo=op.get('alvo'), blocos=op.get('blocos'), com=com)
    elif pos[0] == 'coletar': R = coletar(E, pid, pos[1], pos[2] if len(pos) > 2 else None, blocos=op.get('blocos'), com=com)
    elif pos[0] == 'atacar': R = atacar(E, pid, inicio=op.get('inicio'), vantagens=[v for v in op.get('vantagem', '').split(',') if v])
    elif pos[0] == 'luta': R = luta_roda(E, pid, pos[1:])
    elif pos[0] == 'sangue': R = sangue(E, pid)
    elif pos[0] == 'deixar': R = deixar(E, pid)
    elif pos[0] == 'fugir': R = fugir(E, pid)
    elif pos[0] == 'segue': R = segue(E, pid)
    elif pos[0] == 'larga': R = larga(E, pid, pos[1] if len(pos) > 1 else '')
    else: R = volta(E, pid)
    estado.grava(E)                                         # grava ANTES de falar: a saída cortada não perde o que o dado rolou
    print(TB.contrai(R['texto']))
    print(ato.ultima_linha(E, pid))                         # com a luta aberta, só a hora e que vale o quadro; de quem morreu, só a hora e a morte


if __name__ == '__main__':
    import signal; hasattr(signal, 'SIGPIPE') and signal.signal(signal.SIGPIPE, signal.SIG_DFL)      # a saída cortada (`| head`) acaba o comando calada, sem erro de programa: tudo já foi gravado antes de falar
    main()
