#!/usr/bin/env python3
"""oficio.py — MOTOR 10: O OFÍCIO. Forjar é uma obra de vários dias, com matéria contada, que pode falhar e custa caro.
Consertar é o pão do ferreiro. Ajustar faz a peça servir a um dono. Tudo por evento; os números moram no tabelas_oficio.py.

  A FAIXA (a parte 2, fase 1a; projeto/etapa_efeitos/DESENHO.md, seção 5): a categoria sai como sempre; os EFEITOS saem de quanto faltou para a CD de cima (a régua:
    faltou 1 ou 2, 4 efeitos; 3 a 5, 3; 6 a 8, 2; 9 a 16, 1; 17 ou mais, nenhum; na categoria do teto, no máximo 2), mais 1 por cada 20, até o teto de efeitos (Comum 2, Incomum
    e Rara 4, Épica e Única 5, Lendária e Mítica 6, Primordial 7); o que passa vira CHEIO. Os doze efeitos de ferramenta (o prumo, a têmpera, o lastro...). REGRAS 7.3, 7.6, 7.14 a 7.16.
  FORJAR, NA FORJA E NO COURO: A LEI DO VALOR (decisão do jogador, Dia 30 do mundo novo). A CATEGORIA dita no comando é a da OBRA, o que entra nela (a matéria da
    categoria; do Épico para cima, a matéria Rara e um NÚCLEO da categoria), e dá os blocos (3^k, PESADOS, numa oficina). A categoria da PEÇA sai da soma, uma vez,
    no último bloco: 2d20 explosivos + maestria + Afinidade ÷ 10 + a oficina + o preparo + a obra (matéria Comum 0, Incomum 15, Rara 30; núcleo +15 por categoria
    acima) + o martelo de forja + a tenaz. A peça sai na maior categoria cuja CD o total alcança (Comum 22, Incomum 55, Rara 80, Épica 105, Única 130, Lendária 155),
    até o TETO (com núcleo, a categoria dele; sem núcleo, uma acima da matéria e nunca acima da Rara; subir acima da matéria pede mão de Treinado: a PORTA DO
    DEGRAU); abaixo de 22, a matéria se perde. OS DADOS: cada 20 dá +1 efeito; os dois em 20, a peça sobe; um em 1, cai uma (a faixa fica); os dois em 1, perde (REGRAS 7.3 e 7.6).
  O ENCANTO (o foco e o amuleto) segue com a categoria escolhida: UM teste contra 28 + 6 × k; falhar por menos de 5, uma categoria abaixo; por 5 ou mais, a matéria some.
  A OBRA FICA ABERTA entre um dia e outro: a matéria entra quando ela abre, os blocos somam, o ato para quando o corpo pede, o teste só sai quando os blocos fecham.
  O PREPARO tem alcance: receita e ajudante (da pessoa), fogo e bigorna (do lugar), +2 cada um, só na obra da categoria que ele alcança.
  A MAESTRIA do ofício (forja; couro, para a armadura de couro) sobe por blocos de bancada; de Mestre para cima pede um feito (uma obra nascida).
  CONSERTAR: você na bancada (tempo e um pouco de matéria; pede a mão da categoria), ou pago à oficina do lugar (2% do preço por ponto).
  AJUSTAR (sob medida): grava o dono na peça; o grau (1 a 4) sai da mão de quem ajusta; custa blocos e um teste.
  A BANCADA SERVE A TODO OFÍCIO (etapa da magia): a forja e o couro na oficina; o ENCANTO na mesa de runas (o foco e o amuleto se forjam ali, com a mão de encanto,
    e a gravação de um feitiço numa peça é obra dele: encanto.py); a ALQUIMIA na botica (a leva: alquimia.py); o jornal também no santuário (fé). A obra é uma só:
    abre com a matéria, soma blocos, e o teste sai quando os blocos fecham; quem remata a leva e a gravação é o módulo dela.

Uso (o personagem do jogador, ou quem=ID):
  python3 oficio.py ver                                   a oficina daqui, a sua mão, o preparo, as obras abertas, a matéria que você carrega
  python3 oficio.py pede arma FAMILIA CATEGORIA           o que a obra pede (matéria, núcleo, blocos) e a sua conta no teste, sem abrir nada
  python3 oficio.py pede armadura MATERIAL CATEGORIA [cobre=cabeça]   ·   python3 oficio.py pede escudo CATEGORIA
  python3 oficio.py forjar arma FAMILIA CATEGORIA ["Nome"] [blocos=N] [nucleo=ID]    abre a obra (a matéria entra) e trabalha N blocos
  python3 oficio.py forjar armadura MATERIAL CATEGORIA ["Nome"] [cobre=tronco,braços,pernas] [blocos=N] [nucleo=ID]    (elmo: cobre=cabeça)
  python3 oficio.py forjar escudo CATEGORIA ["Nome"] [blocos=N] [nucleo=ID]
  python3 oficio.py forjar foco FORMA CATEGORIA ["Nome"] · forjar amuleto CATEGORIA ["Nome"]    (etapa da magia) no ofício do encanto, na mesa de runas (o mesmo que encanto.py fazer)
  python3 oficio.py forjar gazua CATEGORIA ["Nome"] [blocos=N]       (etapa 4b) a ferramenta do ladino, como a adaga: 1 de metal da categoria
  python3 oficio.py forjar armadura MATERIAL CATEGORIA ... talhe=miúdo     (etapa 4b) a armadura do corpo miúdo (o pequenino, o gnomo): a mesma matéria, o mesmo teste
                                                          (ou para=ID: a armadura sai no corpo dessa pessoa, miúda ou de gente)
  python3 oficio.py continua [OBRA] [blocos=N]            mais N blocos na obra aberta (sem N: até fechar, ou até o corpo parar)
  python3 oficio.py larga OBRA                            abandona a obra (a matéria que já foi ao fogo se perde; o núcleo fica)
  python3 oficio.py consertar ITEM [pontos=N] [pago]      devolve durabilidade: você na bancada, ou `pago` à oficina do lugar
  python3 oficio.py ajustar ITEM [para=ID] [blocos=N]     sob medida para alguém que está aqui (sem para: para você)
  python3 oficio.py jornal N [oficio=forja|couro|alquimia|encanto|fé]    N blocos de bancada a serviço do lugar (a oficina, a botica, a mesa de runas ou o santuário;
                                                          ele paga o seu salário por bloco, até a jornada:
                                                          2 blocos pagos por dia, contados junto com o `ato.py trabalhar`; depois disso a bancada é sua, sem paga)
  python3 oficio.py pede|forjar ferramenta martelo|tenaz CATEGORIA ["Nome"]     as FERRAMENTAS (a Lei do Valor): o martelo de forja (2 de metal, 1 de madeira) e a tenaz
                                                          (1 de metal, 1 de madeira), cada um +1, +3, +5, +7, +9, +11 do Comum ao Lendário; `ferramenta forja|couro CAT`, o jogo
                                                          (os dois de uma vez); a afinada +1; os poderes da Rara para cima (REGRAS 7.14)
  python3 oficio.py efeito ITEM [CHAVE|auto] [cheio] [emprestado]    (a parte 2, fase 1a) escolhe UM dos efeitos por escolher da peça (cada escolha, um evento): sem CHAVE,
                                                          a lista do que cabe (a porta pela força, o número, o cheio, o que vale); `auto`, pela sua receita; `cheio`, o número da
                                                          categoria de cima num efeito de número. NA FASE 1a SÓ A FERRAMENTA ESCOLHE: a arma, a armadura e o resto guardam os efeitos
                                                          ("efeitos por escolher: N (o catálogo de luta chega na próxima fase)")
  python3 oficio.py receita [TIPO chave,chave|nada]      a SUA RECEITA, uma ordem que vale sempre (TIPO: martelo, tenaz, jogo, ou ferramenta para todas): a ferramenta que nasce com efeitos
                                                          escolhe por ela, na hora, e a mesa só relata (`oficio.py receita tenaz prumo,afinada,fagulha`); sem nada, mostra as suas
  python3 oficio.py forjar ... molde=CHAVE                (com o MOLDE DE MESTRE de uma ferramenta Lendária em uso) o efeito dito ao abrir: a peça que sai na categoria da obra ou acima nasce com ele
  python3 oficio.py preparo receita|ajudante|fogo|bigorna CATEGORIA|nada "como foi ganho" [oficio=alquimia|encanto]     o Mestre registra um preparo ganho no mundo
                                                          (a alquimia: receita, ajudante, fogo, vidraria; o encanto: receita, ajudante, tinta, pedra)
  python3 oficio.py oficina NIVEL|nada "como foi"         o Mestre registra a oficina do lugar onde a pessoa está (0 a 4; nada: o lugar fica sem)
FAMILIA: adaga espada maça machado martelo lança montante alabarda malho arco besta · MATERIAL: couro malha placa · e a gazua (sem família): forjar gazua CATEGORIA
CATEGORIA: Comum Incomum Raro Épico Único Lendário
"""
import math, sys
import tabelas as T
import tabelas_mundo as M
import tabelas_oficio as O
import estado, ato, corpo, teste, talento
from itens import item, cat_i, rotulo, tem as item_tem, EFEITOS, ESCOLHE_NAO

PECAS = ('arma', 'armadura', 'escudo')
FORJA = PECAS + O.PECAS_ENCANTO + O.PECAS_LADINO + O.PECAS_FERRAMENTA      # o que se forja (o foco e o amuleto, no ofício do encanto; a gazua e a ferramenta, na oficina)
SEM_FAMILIA = ('escudo', 'amuleto', 'gazua')                # o que se forja sem família, forma nem material: só a categoria
FEM = ['Comum', 'Incomum', 'Rara', 'Épica', 'Única', 'Lendária', 'Mítica', 'Primordial']       # a categoria, quando o nome que vem antes é feminino (a peça, a obra)


# ---------- o dado, contado (para dizer a chance antes de abrir a obra) ----------
def _somas():
    """a distribuição de 2d20 em que cada 20 rola de novo e soma (como o teste.py rola)"""
    um = {}
    for k in range(5):
        for x in range(1, 20): um[20 * k + x] = 0.05 ** (k + 1)
    dois = {}
    for a, pa in um.items():
        for b, pb in um.items(): dois[a + b] = dois.get(a + b, 0) + pa * pb
    return dois
_SOMAS = _somas()


def chance_de(precisa):
    """a chance de 2d20 (com o 20 que rola de novo) dar `precisa` ou mais"""
    return min(1.0, sum(p for s, p in _SOMAS.items() if s >= precisa))


def chances(soma, contra):
    """(acerta, sai uma abaixo, perde tudo) para quem soma `soma` ao 2d20 contra `contra`"""
    acerta = chance_de(contra - soma); pouco = chance_de(contra - soma - (O.POR_POUCO - 1)) - acerta
    return acerta, pouco, max(0.0, 1 - acerta - pouco)


# ---------- ler: a oficina, a mão, o preparo, a conta ----------
def _vivo(E, pid): return estado.presente(E, pid, 'trabalhar na bancada')        # vivo e no lugar onde mora: quem saiu para o ermo não forja nem conserta


def oficina(E, lid):
    """o nível da oficina do lugar (0 a 4), ou None se o lugar não tem oficina"""
    v = E['lugares'][lid].get('oficina')
    if v is None or v is False or not isinstance(v, (int, float)): return None
    return max(0, min(len(O.OFICINAS) - 1, int(v)))


def nome_oficina(v): return f'{O.OFICINAS[v]} (+{v})'


def banca(E, lid, oficio='forja'):
    """o nível da bancada do ofício no lugar (0 a 4): a oficina (forja, couro), a mesa de runas (encanto), a botica (alquimia), o santuário (fé); None se o lugar não a tem"""
    if O.BANCA.get(oficio, 'oficina') == 'oficina': return oficina(E, lid)
    v = E['lugares'][lid].get(O.BANCA[oficio])
    return None if not isinstance(v, int) or isinstance(v, bool) else max(0, min(M.BANCADA_MAX, v))


def nomes_banca(oficio):
    import tabelas_magia_mundo as W
    return dict(encanto=W.RUNAS, alquimia=W.BOTICAS, fé=['altar', 'capela', 'santuário', 'templo', 'grande templo']).get(oficio, O.OFICINAS)
def nome_banca(oficio, v): return f'{nomes_banca(oficio)[v]} (+{v})'
def evento_de(oficio, tipo='forjar'): return O.EVENTO_OFICIO.get(oficio, tipo if tipo in ('forjar', 'ajustar') else 'forjar')        # o tipo de evento do trabalho na bancada deste ofício
def _sem_banca(E, lid, oficio):
    nome = dict(encanto='mesa de runas', alquimia='botica', fé='santuário').get(oficio, 'oficina')
    return f"{E['lugares'][lid]['nome']} não tem {nome}"
def _fam(x): return x.get('forma') if x.get('tipo') == 'foco' else O.chave_ferramenta(x.get('forma') or 'jogo', x.get('oficio')) if x.get('tipo') == 'ferramenta' else x.get('familia')        # o foco leva a forma, e a ferramenta a forma ou o ofício do jogo, onde a arma leva a família
def mao(p, oficio='forja'): m = p.get('maestria'); return m.get(oficio, 0) if isinstance(m, dict) else 0             # a maestria no ofício (0 a 8)
def bancada(p, oficio='forja'): t = p.get('treino'); return t.get(oficio, 0) if isinstance(t, dict) else 0         # os blocos de bancada já feitos


def tabela_preparos(oficio='forja'):
    """os quatro preparos do ofício: a forja e o couro (receita, ajudante, fogo, bigorna); a alquimia (receita, ajudante, fogo, vidraria); o encanto (receita, ajudante, tinta, pedra)"""
    import tabelas_magia_mundo as W
    return dict(alquimia=W.PREPAROS_ALQUIMIA, encanto=W.PREPAROS_ENCANTO).get(oficio, O.PREPAROS)


def preparos(E, pid, lid=None, oficio='forja'):
    """{os quatro preparos do ofício: o índice da categoria que ele alcança, ou None se não há}"""
    p = E['gente'][pid]; l = E['lugares'][lid or p['lugar']]; out = {}; do_lugar = l.get('preparo') if isinstance(l.get('preparo'), dict) else {}
    for nome, (de, chave) in tabela_preparos(oficio).items():
        v = p.get('marca', {}).get(chave) if de == 'pessoa' else do_lugar.get(chave)
        out[nome] = int(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else None
    return out


def preparo(E, pid, cat, lid=None, oficio='forja'):
    """o preparo que vale numa obra de categoria `cat`: +2 por preparo que a alcança, até +8"""
    return min(O.PREPARO_MAX, O.PREPARO_CADA * sum(1 for v in preparos(E, pid, lid, oficio).values() if v is not None and v >= cat))


def ferramentas(E, pid, oficio='forja'):
    """(a Lei do Valor) as ferramentas deste ofício que a pessoa tem, inteiras: a melhor no lugar do MARTELO DE FORJA e a melhor no lugar da TENAZ (o jogo, da parte 1,
    serve nos dois lugares). Devolve {martelo: (id, item) | None, tenaz: (id, item) | None}"""
    out = dict(martelo=None, tenaz=None)
    if oficio not in O.FERRAMENTA_OFICIOS: return out
    boas = [(k, it) for k, it in E['itens']['itens'].items() if it.get('tipo') == 'ferramenta' and it.get('oficio') == oficio and it.get('dono') == pid and it['dur'][0] > 0]
    chave = lambda x: (x[1]['cat'], len(x[1].get('efeitos') or []), bool(item_tem(x[1], 'afinada')), x[0])     # a de maior categoria; no empate, a de mais efeitos (fase 1a), depois a afinada
    for lugar in ('martelo', 'tenaz'):
        cabem = [x for x in boas if (x[1].get('forma') or 'jogo') in (lugar, 'jogo')]
        if cabem: out[lugar] = max(cabem, key=chave)
    return out


def efeitos_em_uso(E, pid, oficio='forja'):
    """(a parte 2, fase 1a) os EFEITOS DAS FERRAMENTAS EM USO (a do lugar do martelo e a do lugar da tenaz; o jogo que está nos dois vale uma vez): o mesmo efeito em duas
    não soma (vale o maior), menos o PRUMO, que soma até PRUMO_MAX. Devolve {prumo, tempera, remendo (os de número), e cada um dos outros: True/False; de: {chave: [ids]}}"""
    fx = dict(prumo=0, tempera=0, remendo=0, de={})
    usadas = {x[0]: x[1] for x in ferramentas(E, pid, oficio).values() if x}
    for iid, it in usadas.items():
        for e in it.get('efeitos') or []:
            k = e.get('chave') if isinstance(e, dict) else None
            if k not in O.FERRAMENTA_EFEITOS: continue
            fx['de'].setdefault(k, []).append(iid)
            v = O.valor_ferramenta(k, it['cat'], bool(e.get('cheio')))
            if k == 'prumo': fx['prumo'] += v
            elif k == 'tempera': fx['tempera'] = max(fx['tempera'], v)
            elif k == 'remendo': fx['remendo'] = O.REMENDO_BLOCO
            else: fx[k] = True
    fx['prumo'] = min(O.PRUMO_MAX, fx['prumo'])
    return fx


def valor_ferramentas(E, pid, oficio='forja'):
    """o que as ferramentas somam (a Lei do Valor): o martelo de forja e a tenaz, cada um pela categoria dele, e a afinada (obra-prima) mais VALOR_AFINADA uma vez.
    Devolve (martelo, tenaz, a maior categoria entre as duas ou None)"""
    f = ferramentas(E, pid, oficio); vm = vt = 0; cats = []
    if f['martelo']: it = f['martelo'][1]; vm = O.VALOR_MARTELO[min(it['cat'], len(O.VALOR_MARTELO) - 1)]; cats.append(it['cat'])
    if f['tenaz']: it = f['tenaz'][1]; vt = O.VALOR_TENAZ[min(it['cat'], len(O.VALOR_TENAZ) - 1)]; cats.append(it['cat'])
    if any(x and item_tem(x[1], 'afinada') for x in f.values()): vm += O.VALOR_AFINADA
    return vm, vt, (max(cats) if cats else None)


def conta(E, pid, cat, oficio='forja', lid=None, contra=None):
    """a conta do teste desta pessoa, hoje, numa obra desta categoria: o que soma, contra quanto, e as três chances"""
    p = E['gente'][pid]; lid = lid or p['lugar']; v = banca(E, lid, oficio) or 0; prep = preparo(E, pid, cat, lid, oficio)
    # O DOM da bancada (etapa da magia) é um preparo que nasce com a pessoa: preparo e dom juntos não passam de +8. O dom que a pessoa ainda não viu não entra na conta
    # que vai à mesa: vai escondido no dado (c['oculto'], o dom= do teste.rola)
    c = dict(maestria=mao(p, oficio), afinidade=p['atributos']['Afinidade'] // 10, oficina=v, preparo=min(O.PREPARO_MAX, prep + talento.dom_visto(p, oficio)), pena=corpo.pena(p, estado.agora(E)), contra=O.contra(cat) if contra is None else contra)
    c['oculto'] = min(O.PREPARO_MAX, prep + talento.dom(p, oficio)) - c['preparo']
    vm, vt, fc = valor_ferramentas(E, pid, oficio); c['ferramenta'] = vm + vt; c['ferramenta_cat'] = fc       # o martelo de forja e a tenaz somam também no teste de passar (o ajuste)
    c['mais'] = c['maestria'] + c['oficina'] + c['preparo'] + c['ferramenta']      # o que entra como "mais" no teste.rola (a Afinidade e a pena, ele mesmo soma)
    c['soma'] = c['mais'] + c['afinidade'] + c['pena']
    c['acerta'], c['pouco'], c['perde'] = chances(c['soma'], c['contra'])
    return c


# ---------- A LEI DO VALOR (a forja e o couro: a soma decide a categoria) ----------
def _um_d20x(prof=4):
    """a distribuição de UM d20 que rola de novo no 20 e soma (cortada em `prof` voltas: o resto da massa fica no último 20)"""
    d = {}
    def rec(acc, p, k):
        for x in range(1, 21):
            q = p / 20
            if x == 20 and k < prof: rec(acc + 20, q, k + 1)
            else: d[acc + x] = d.get(acc + x, 0) + q
    rec(0, 1.0, 0); return d
_UM = _um_d20x()


def _resolve(total, a0, b0, teto, fc, prumo=0, lastro=False):
    """o que sai de uma obra pela Lei do Valor, dado o total e as duas faces de partida (a0, b0): uma lista com UMA saída [(1.0, saída)] (a forma de lista fica para a conta exata),
    em que a saída é {cat: a categoria ou None (perde), tosca, sobe, mais_efeito, quase, salva, k, falta, faixa, como}. fc: a maior categoria das ferramentas (ou -1). Os dados
    (sem 1d6): os dois abrindo em 1, perde (só a ferramenta Épica segura); um abrindo em 1, a peça sai uma categoria abaixo do que o total deu (a Comum, tosca); os dois abrindo
    em 20, a OBRA-PRIMA (sobe uma categoria se o teto deixa; no teto, +1 efeito). Os poderes: a ferramenta Rara segura a matéria até VALOR_SEGURA abaixo da CD do Comum; a Épica
    nunca a perde; a Única dá o QUASE.
    A FAIXA (a parte 2, fase 1a): k é a categoria que o TOTAL deu (antes dos dados especiais); falta, o que faltou para a CD de cima; faixa, os efeitos da régua (com o prumo e o
    lastro; na categoria do teto, no máximo 2). A CATEGORIA SAI COMO ANTES, linha por linha: o prumo e o lastro só mexem nos efeitos. O 1 tira a categoria e deixa a faixa; a
    obra-prima sobe e deixa a faixa; a peça salva pela ferramenta sai sem efeito (salva). O QUASE vale com ou sem dado especial, só abaixo do teto (a CD de cima alcançável)."""
    k = O.cat_do_total(total, teto)
    nf, falta = O.faixa(total, k, teto, prumo, lastro)
    x = dict(cat=k, k=k, tosca=False, sobe=False, mais_efeito=0, quase=False, salva=False, falta=falta, faixa=nf, como='')
    if a0 == 1 and b0 == 1:
        x.update(cat=None, faixa=0, como='os dois dados abrindo em 1: a matéria se perde')
        if fc >= O.NADA_SE_PERDE: x.update(cat=0, tosca=True, salva=True, como=x['como'] + '; a ferramenta Épica a segura: a peça sai Comum, tosca, sem efeito')
        return [(1.0, x)]
    if a0 == 1 or b0 == 1:
        if k is not None:
            if k > 0: x.update(cat=k - 1, como='um dado abrindo em 1: a peça sai uma categoria abaixo (a faixa fica)')
            else: x.update(tosca=True, como='um dado abrindo em 1: a peça Comum sai tosca (a faixa fica)')
    elif a0 == 20 and b0 == 20 and k is not None:
        if k < teto: x.update(cat=k + 1, sobe=True, como='OBRA-PRIMA, os dois dados abrindo em 20: a peça sobe uma categoria (a faixa fica)')
        else: x.update(mais_efeito=1, como='OBRA-PRIMA, os dois dados abrindo em 20: no teto, +1 efeito')
    if k is not None and fc >= O.OBRA_PRIMA_FACIL and k < teto and falta <= O.QUASE_JANELA:
        x.update(quase=True, como=(x['como'] + '; ' if x['como'] else '') + f'QUASE (o poder da ferramenta Única): faltaram {falta} para a CD de cima, +1 efeito')
    if x['cat'] is None and (fc >= O.NADA_SE_PERDE or (fc >= 2 and total >= O.VALOR_CD[0] - O.VALOR_SEGURA)):
        x.update(cat=0, tosca=True, salva=True, faixa=0, como=(x['como'] + '; ' if x['como'] else '') + f"a ferramenta {'Épica' if fc >= O.NADA_SE_PERDE else 'Rara'} segura a matéria: a peça sai Comum, tosca, sem efeito")
    if x['cat'] is None and not x['como']: x['como'] = f'a soma ficou abaixo da CD do Comum ({O.VALOR_CD[0]}): a matéria se perde'
    return [(1.0, x)]


def conta_efeitos(x, n20=0, n19=0, fagulha=False, tempera=0, molde=False):
    """(a parte 2, fase 1a: a conta em ordem do contrato, 5.4) os efeitos de uma obra já resolvida: n = os da faixa + 1 por cada 20 + as fagulhas (os 19 que abrem, com a
    fagulha) + o quase; efeitos = o mínimo entre o teto de efeitos da categoria FINAL e n, mais a obra-prima no teto; o que passa do teto (e a têmpera) vira CHEIO
    (cheios = mínimo entre os efeitos e a sobra + a têmpera). O MOLDE (se a peça sai na categoria da obra ou acima: quem chama decide) é +1 fora do teto, já escolhido.
    A peça perdida ou salva pela ferramenta sai sem efeito. Devolve {n, faixa, vintes, fagulhas, quase, livres, cheios, molde, efeitos, teto, sobra}."""
    if x['cat'] is None or x.get('salva'):
        return dict(n=0, faixa=0, vintes=0, fagulhas=0, quase=0, livres=0, cheios=0, molde=0, efeitos=0, teto=O.efeitos_max(x['cat'] or 0), sobra=0)
    cap = O.efeitos_max(x['cat']); fag = n19 if fagulha else 0; q = 1 if x.get('quase') else 0
    n = x['faixa'] + n20 + fag + q
    livres = min(cap, n) + x.get('mais_efeito', 0)
    cheios = min(livres, max(0, n - cap) + tempera)
    m = 1 if molde else 0
    return dict(n=n, faixa=x['faixa'], vintes=n20, fagulhas=fag, quase=q, livres=livres, cheios=cheios, molde=m, efeitos=livres + m, teto=cap + x.get('mais_efeito', 0) + m, sobra=max(0, n - cap))


def dist_valor(soma, teto, fc=-1):
    """a chance de cada categoria (e de perder: None) pela Lei do Valor, para quem soma `soma` ao 2d20 explosivo, com o teto e os dados especiais"""
    res = {}
    for a0 in range(1, 21):
        da = {a0: 1.0} if a0 < 20 else {20 + x: q for x, q in _UM.items()}
        for b0 in range(1, 21):
            db = {b0: 1.0} if b0 < 20 else {20 + x: q for x, q in _UM.items()}
            for va, pa in da.items():
                for vb, pb in db.items():
                    p = pa * pb / 400
                    for q, x in _resolve(va + vb + soma, a0, b0, teto, fc): res[x['cat']] = res.get(x['cat'], 0) + p * q
    return res


def _um_d20xn(prof=4):
    """o mesmo dado do _UM (um d20 que rola de novo no 20, cortado em `prof` voltas), contando os 20 da cadeia: {(soma, quantos 20): chance}"""
    d = {}
    def rec(acc, p, k):
        for x in range(1, 21):
            q = p / 20
            if x == 20 and k < prof: rec(acc + 20, q, k + 1)
            else: d[(acc + x, k + (x == 20))] = d.get((acc + x, k + (x == 20)), 0) + q
    rec(0, 1.0, 0); return d
_UMN = _um_d20xn()
_DADOS = None


def _dados():
    """(a conta exata dos efeitos) o 2d20 explosivo do dist_valor, juntado pelo que a regra lê: (quantos abrem em 1, os dois abrem em 20, quantos abrem em 19, quantos 20 na
    cadeia, a soma dos dados) → chance. A mesma massa do dist_valor, só agrupada (a categoria bate com ele a 1e−12: a meta B2)."""
    global _DADOS
    if _DADOS is None:
        d = {}
        for a0 in range(1, 21):
            da = {(a0, 0): 1.0} if a0 < 20 else {(20 + x, 1 + n): q for (x, n), q in _UMN.items()}
            for b0 in range(1, 21):
                db = {(b0, 0): 1.0} if b0 < 20 else {(20 + x, 1 + n): q for (x, n), q in _UMN.items()}
                chave = ((a0 == 1) + (b0 == 1), a0 == 20 and b0 == 20, (a0 == 19) + (b0 == 19))
                for (va, na), pa in da.items():
                    for (vb, nb), pb in db.items():
                        k = chave + (na + nb, va + vb); d[k] = d.get(k, 0) + pa * pb / 400
        _DADOS = sorted(d.items())
    return _DADOS
_FACE = {(2, False): (1, 1), (1, False): (1, 9), (0, True): (20, 20), (0, False): (9, 9)}     # as faces que o _resolve lê (os 1, os dois 20), postas por quem representa o grupo


def dist_efeitos(soma, teto, fc=-1, prumo=0, lastro=False, fagulha=False, tempera=0, molde_cat=None, detalhe=False):
    """(a parte 2, fase 1a) a conta exata da obra inteira: {(categoria ou None, efeitos, cheios): chance} para quem soma `soma` ao 2d20 explosivo, com o teto, a ferramenta
    (fc: o poder; prumo, lastro, fagulha, têmpera: os efeitos dela) e o molde (a categoria da obra: o molde vale na peça que sai nela ou acima). A categoria é a do dist_valor.
    detalhe: as chaves levam também os efeitos da faixa e se foram os dois 1 ((cat, efeitos, cheios, faixa, dois_1)), para a conta da peça colada."""
    res = {}
    for (uns, vinte2, n19, n20, td), p in _dados():
        a0, b0 = _FACE[(uns, vinte2)]
        x = _resolve(td + soma, a0, b0, teto, fc, prumo, lastro)[0][1]
        c = conta_efeitos(x, n20, n19, fagulha, tempera, molde=molde_cat is not None and x['cat'] is not None and not x['salva'] and x['cat'] >= molde_cat)
        k = (x['cat'], c['efeitos'], c['cheios']) + ((x['faixa'], uns == 2) if detalhe else ())
        res[k] = res.get(k, 0) + p
    return res


def resumo_efeitos(d):
    """o que a mesa e o banco leem da conta exata: efeitos e cheios por obra, os pontos de feitio (efeitos + metade dos cheios), a obra com efeito, a com 3 ou mais, e por categoria"""
    ef = sum(k[1] * q for k, q in d.items() if k[0] is not None); ch = sum(k[2] * q for k, q in d.items() if k[0] is not None)
    out = dict(efeitos=ef, cheios=ch, feitio=ef + ch / 2, com=sum(q for k, q in d.items() if k[0] is not None and k[1] >= 1),
               tres=sum(q for k, q in d.items() if k[0] is not None and k[1] >= 3), perde=sum(q for k, q in d.items() if k[0] is None), cat={})
    for k, q in d.items():
        if k[0] is None: continue
        c = out['cat'].setdefault(k[0], dict(chance=0.0, ef={}, cheios=0.0)); c['chance'] += q; c['ef'][k[1]] = c['ef'].get(k[1], 0) + q; c['cheios'] += k[2] * q
    feitas = 1 - out['perde']; out['com_peca'] = out['com'] / feitas if feitas else 0
    if d and len(next(iter(d))) == 5:          # o detalhe: a COLADA (3 ou 4 efeitos só da faixa), entre as peças feitas (fora a dos dois 1, que a ferramenta Épica salva)
        f = sum(q for k, q in d.items() if k[0] is not None and not k[4]); out['colada'] = sum(q for k, q in d.items() if k[0] is not None and not k[4] and k[3] >= 3) / f if f else 0
    return out


def regua(teto, prumo=0, lastro=False):
    """a régua de cada faixa até o teto, em totais: [(categoria, [(efeitos da faixa, de, até ou None: em diante)])]; o prumo desloca os degraus, o lastro tira o zero"""
    out = []
    for k in range(min(teto, len(O.VALOR_CD) - 1) + 1):
        degraus = []; top = O.cd_de_cima(k); fim = top + 40 if k >= teto else top - 1
        for t in range(O.VALOR_CD[k], fim + 1):
            n = O.faixa(t, k, teto, prumo, lastro)[0]
            if degraus and degraus[-1][0] == n: degraus[-1][2] = t
            else: degraus.append([n, t, t])
        if k >= teto: degraus[-1][2] = None                                       # no teto, o último degrau não acaba: passar da CD trancada dá o mesmo
        out.append((k, [tuple(x) for x in degraus]))
    return out


def diz_regua(teto, prumo=0, lastro=False, fc=-1):
    """a régua em uma linha, para a mesa: o que faltou para a CD de cima dá efeitos, até o teto da obra"""
    partes = []
    for k, degraus in regua(teto, prumo, lastro):
        cab = f"{FEM[k]}" + (f' (o teto desta obra: a régua para em {O.TETO_FAIXA})' if k >= teto else '')
        partes.append(cab + ' ' + ' · '.join(f"{de}–{ate}: {n}" if ate is not None and ate != de else f"{de}: {n}" if ate is not None else f"{de} em diante: {n}" for n, de, ate in degraus))
    extra = ['mais 1 por cada 20 dos dados'] + (['o quase: +1 quando faltam 6 ou menos para a CD de cima, abaixo do teto'] if fc >= O.OBRA_PRIMA_FACIL else [])
    if prumo: extra.insert(0, f'com o prumo {prumo} (a falta conta {prumo} a menos)')
    if lastro: extra.insert(0, 'com o lastro (a faixa dá pelo menos 1)')
    tetos = ', '.join(f"{FEM[k]} {O.efeitos_max(k)}" for k in range(min(teto, len(O.VALOR_CD) - 1) + 1))
    return 'a RÉGUA DA FAIXA (o que faltou para a CD de cima dá efeitos): ' + ' | '.join(partes) + f"; {'; '.join(extra)}; até o teto de efeitos ({tetos}), e o que passa vira CHEIO"


def valor(E, pid, cat, oficio='forja', lid=None):
    """a conta da LEI DO VALOR desta pessoa, hoje, numa obra cuja matéria (ou núcleo) é da categoria `cat`: o que soma, o teto, e a chance de cada categoria"""
    p = E['gente'][pid]; lid = lid or p['lugar']; v = banca(E, lid, oficio) or 0; prep = preparo(E, pid, cat, lid, oficio); vm, vt, fc = valor_ferramentas(E, pid, oficio)
    c = dict(maestria=mao(p, oficio), afinidade=p['atributos']['Afinidade'] // 10, oficina=v, preparo=min(O.PREPARO_MAX, prep + talento.dom_visto(p, oficio)),
             materia=O.VALOR_MATERIA[min(cat, M.MATERIA_ATE)], nucleo=O.VALOR_NUCLEO.get(cat, 0), martelo=vm, tenaz=vt, ferramenta_cat=fc,
             pena=corpo.pena(p, estado.agora(E)), teto=O.teto(cat, mao(p, oficio), fc), cat=cat, contra=O.VALOR_CD[min(cat, len(O.VALOR_CD) - 1)])
    c['porta'] = cat <= M.MATERIA_ATE and c['maestria'] < O.PORTA_DEGRAU             # a porta do degrau: sem a mão de Treinado, a peça não passa da matéria
    c['oculto'] = min(O.PREPARO_MAX, prep + talento.dom(p, oficio)) - c['preparo']
    c['mais'] = c['maestria'] + c['oficina'] + c['preparo'] + c['materia'] + c['nucleo'] + c['martelo'] + c['tenaz']
    c['soma'] = c['mais'] + c['afinidade'] + c['pena']; c['ferramenta'] = vm + vt
    c['chances'] = dist_valor(c['soma'], c['teto'], -1 if fc is None else fc)
    c['fx'] = efeitos_em_uso(E, pid, oficio)                                          # (fase 1a) os efeitos das ferramentas em uso: o prumo, o lastro, a fagulha, a têmpera...
    return c


def efeitos_de(c, molde_cat=None):
    """(fase 1a) a conta exata dos efeitos desta conta da Lei do Valor (o valor() não a faz sozinho: é a conta mais pesada, e só a mesa a pede)"""
    fx = c.get('fx') or {}; fc = -1 if c.get('ferramenta_cat') is None else c['ferramenta_cat']
    d = dist_efeitos(c['soma'], c['teto'], fc, fx.get('prumo', 0), bool(fx.get('lastro')), bool(fx.get('fagulha')), fx.get('tempera', 0), molde_cat, detalhe=True)
    c['efeitos'] = resumo_efeitos(d); return c['efeitos']


def diz_efeitos(c):
    """os efeitos em uma linha: por obra, a peça com efeito, a colada; e a categoria de baixo colada na de cima (a Incomum de 3 ou 4)"""
    r = c.get('efeitos') or efeitos_de(c)
    col = {k: sum(q for e, q in v['ef'].items() if e >= 3) for k, v in r['cat'].items()}
    alto = ' · '.join(f"{FEM[k]} com 3 ou mais {col[k]:.1%}" for k in sorted(col) if col[k] >= 0.0005)
    return (f"os efeitos, pela conta exata: {r['efeitos']:.2f} efeito por obra ({r['cheios']:.2f} cheio), obra com efeito {r['com']:.0%}, peça colada (3 ou 4 só da faixa) {r.get('colada', 0):.0%}"
            + (f"; {alto}" if alto else ''))


def diz_valor(c):
    """a conta da Lei do Valor em uma linha, a chance de cada categoria, e a régua da faixa (fase 1a)"""
    partes = (f"maestria {c['maestria']} + Afinidade {c['afinidade']} + matéria {c['materia']}" + (f" + núcleo {c['nucleo']}" if c['nucleo'] else '')
              + (f" + martelo de forja {c['martelo']}" if c['martelo'] else '') + (f" + tenaz {c['tenaz']}" if c['tenaz'] else '') + f" + oficina {c['oficina']} + preparo {c['preparo']}"
              + (f" − {-c['pena']} do corpo" if c['pena'] else ''))
    ch = c['chances']; cats = [k for k in range(c['teto'] + 1) if ch.get(k, 0) >= 0.0005]
    tab = ' · '.join(f"{T.CATS[k]} {ch.get(k, 0):.0%}" for k in cats) + f" · perde {ch.get(None, 0):.0%}"
    cds = ' · '.join(f"{T.CATS[k]} {O.VALOR_CD[k]}" for k in range(min(c['teto'], len(O.VALOR_CD) - 1) + 1))
    porta = f" (a porta do degrau: sem a mão de Treinado, a peça não passa da matéria)" if c.get('porta') else ''
    fx = c.get('fx') or {}; fc = -1 if c.get('ferramenta_cat') is None else c['ferramenta_cat']
    return (f"2d20 + {c['soma']} ({partes}) · a peça sai na maior categoria que o total alcança ({cds}; o teto desta obra: {T.CATS[c['teto']]}{porta}): {tab}"
            + f" · {diz_regua(c['teto'], fx.get('prumo', 0), bool(fx.get('lastro')), fc)}")


def diz_conta(c, pouco='sai uma abaixo', perde='perde tudo', banca='oficina'):
    partes = f"maestria {c['maestria']} + Afinidade {c['afinidade']} + {banca} {c['oficina']} + preparo {c['preparo']}" + (f" + ferramenta {c['ferramenta']}" if c.get('ferramenta') else '') + (f" − {-c['pena']} do corpo" if c['pena'] else '')
    return f"2d20 + {c['soma']} ({partes}) contra {c['contra']}: acerta {c['acerta']:.0%} · {pouco} {c['pouco']:.0%} · {perde} {c['perde']:.0%}"


def _em(E, lid): l = E['lugares'][lid]; return l.get('em', 'em ' + l['nome'])
def _peca(x): return rotulo(x)                                                 # "Adaga da Cira (Comum)"; "espada Rara" (o nome que já diz a categoria não a repete)
tantos = estado.tantos
def obras_de(E, pid): return {k: o for k, o in E['itens'].get('obras', {}).items() if o.get('quem') == pid}
def _mat(chave): n, c = M.le_materia(chave); return f"{n} {(FEM if n.endswith('a') else T.CATS)[c]}" if c is not None else chave        # "metal Raro", "madeira Rara"
def _lista(d): return ', '.join(f'{n} de {_mat(k)}' for k, n in d.items())


def materia_do_mundo(E):
    """toda a matéria com categoria que existe: nas cargas, nos estoques e dentro das obras abertas (para as provas: a conta tem de fechar)"""
    tot = {}
    def junta(d):
        for k, n in (d or {}).items():
            if M.le_materia(k)[1] is not None: tot[k] = tot.get(k, 0) + n
    for p in E['gente'].values(): junta(p.get('carga'))
    for l in E['lugares'].values(): junta(l.get('estoque'))
    for o in E['itens'].get('obras', {}).values(): junta(o.get('materia'))
    return tot


def prata_do_mundo(E): return sum(p['moedas'] for p in E['gente'].values()) + sum(l['estoque'].get('prata', 0) for l in E['lugares'].values())


# ---------- a peça que se quer ----------
def molde(tipo, cat, nome=None, familia=None, material=None, cobre=None, forma=None, talhe=None, oficio=None):
    """o que se vai forjar, conferido ANTES de qualquer coisa mudar: {tipo, cat, nome, familia | material e cobre (e o talhe da armadura miúda) | forma (o foco)}"""
    if tipo not in FORJA: sys.exit(f'não se forja "{tipo}" (forja-se: {", ".join(FORJA)})')
    c = cat_i(cat)
    if c > O.FORJA_ATE: sys.exit(f'ninguém forja acima do {T.CATS[O.FORJA_ATE]} (veio {T.CATS[c]})')
    if tipo == 'arma' and familia not in O.MATERIA_ARMA: sys.exit(f'não se forja a arma "{familia}" (forja-se: {", ".join(O.MATERIA_ARMA)})')
    if tipo == 'foco' and forma not in M.MATERIA_FOCO: sys.exit(f'não se faz o foco "{forma}" (faz-se: {", ".join(M.MATERIA_FOCO)})')
    if talhe not in O.TALHES + ('gente',): sys.exit(f'talhe desconhecido: "{talhe}" (a armadura é de gente, ou miúda: talhe=miúdo)')
    if talhe == 'miúdo' and tipo != 'armadura': sys.exit('só a armadura se forja para o corpo miúdo (a arma, o escudo e a gazua servem em todo corpo)')
    if tipo == 'ferramenta':                                # (a etapa dos efeitos, parte 1) a ferramenta do ofício: o jogo de forja ou o jogo de couro
        if oficio in ('martelo', 'tenaz'): forma, of = oficio, 'forja'
        elif oficio in O.FERRAMENTA_OFICIOS: forma, of = 'jogo', oficio
        else: sys.exit(f'a ferramenta: forjar ferramenta martelo|tenaz CATEGORIA (o martelo de forja, a tenaz) ou ferramenta forja|couro CATEGORIA (o jogo, os dois de uma vez) (veio "{oficio}")')
        it = item('ferramenta', c, nome, oficio=of, forma=forma); return dict(tipo='ferramenta', cat=c, nome=it['nome'], oficio=of, forma=forma)
    it = item(tipo, c, nome, **({'forma': forma} if tipo == 'foco' else {} if tipo in ('amuleto', 'gazua') else dict(familia=familia, material=material, cobre=cobre, talhe=None if talhe == 'gente' else talhe)))        # confere o material e as partes, e dá o nome padrão
    d = dict(tipo=tipo, cat=c, nome=it['nome'])
    if tipo == 'foco': d['forma'] = forma
    if tipo == 'arma': d['familia'] = familia
    if tipo == 'armadura':
        d['material'] = material; d['cobre'] = it['cobre']
        if it.get('talhe'): d['talhe'] = it['talhe']            # a armadura miúda (etapa 4b): a peça nasce com o talhe
    return d


def _materia_conserto(it):
    """a chave da matéria que o conserto desta peça gasta, ou None se a tabela não sabe de que ela é feita"""
    try: return O.materia_conserto(it['tipo'], it['cat'], _fam(it), it.get('material'), it.get('cobre'))
    except KeyError: return None
def oficio_de(x): return O.oficio_da(x['tipo'], x.get('material'))
def materia_de(x, cat=None): return O.materia(x['tipo'], x['cat'] if cat is None else cat, _fam(x), x.get('material'), x.get('cobre'))


def _nucleo(E, pid, cat, nid=None):
    """o núcleo que entra na obra: da categoria da obra, na mão de quem forja, e fora de outra obra aberta"""
    ocupados = {o.get('nucleo') for o in E['itens'].get('obras', {}).values()}; L = E['itens']['itens']
    if nid:
        it = L.get(nid) or sys.exit(f'não há o item "{nid}" no Livro de Itens')
        if it['tipo'] != 'nucleo': sys.exit(f"{it['nome']} ({nid}) não é um núcleo")
        if it['cat'] != cat: sys.exit(f"{it['nome']} é um núcleo {T.CATS[it['cat']]}: a obra {FEM[cat]} pede um núcleo {T.CATS[cat]}")
        if it.get('dono') != pid: sys.exit(f"{it['nome']} não está na mão de quem forja")
        if nid in ocupados: sys.exit(f"{it['nome']} já está dentro de outra obra aberta")
        return nid
    for iid, it in L.items():
        if it['tipo'] == 'nucleo' and it['cat'] == cat and it.get('dono') == pid and iid not in ocupados: return iid
    sys.exit(f'uma obra {FEM[cat]} pede um núcleo {T.CATS[cat]} na mão de quem forja (item do Livro de Itens, tipo "nucleo"). Não há nenhum livre.')


def materia_da_obra(E, pid, peca):
    """a matéria que a obra gasta: a da peça, e (fase 1a) com o POUPA-FERRO de uma ferramenta em uso, 1 de metal a menos, se o metal é a matéria principal da peça e ela leva
    3 ou mais dele (a espada com 2 de metal; o arco e a armadura de couro, não: é o ferro que ele poupa)"""
    mat = dict(materia_de(peca)); of = oficio_de(peca)
    if of in O.VALOR_OFICIOS and efeitos_em_uso(E, pid, of).get('poupa_ferro'):
        k = max(mat, key=lambda x: mat[x])
        if mat[k] >= 3 and M.le_materia(k)[0] == 'metal': mat[k] -= 1
    return mat


def pede(E, pid, peca):
    """o que a obra pede e a conta de hoje, sem abrir nada"""
    p = _vivo(E, pid); cat = peca['cat']; of = oficio_de(peca); v = banca(E, p['lugar'], of); mat = materia_da_obra(E, pid, peca); carga = p.get('carga', {})
    poupa = mat != materia_de(peca)
    L = [f"{_peca(peca)} · ofício: {of} · {tantos(O.blocos(cat), 'bloco pesado', 'blocos pesados')} de bancada",
         'Matéria: ' + ', '.join(f"{n} de {_mat(k)} (você tem {carga.get(k, 0)})" for k, n in mat.items())
         + (' (o poupa-ferro da sua ferramenta tira 1 do metal)' if poupa else '') + (f' · e um núcleo {T.CATS[cat]}' if O.pede_nucleo(cat) else '')]
    if v is None: L.append(_sem_banca(E, p['lugar'], of) + ': a obra não abre.')
    elif of in O.VALOR_OFICIOS:
        c = valor(E, pid, cat, of); L.append('A soma, hoje e aqui (a Lei do Valor): ' + diz_valor(c))
        L.append('E ' + diz_efeitos(c) + (f" · {diz_quem_escolhe(peca)}"))
    else: L.append('O teste final, hoje e aqui: ' + diz_conta(conta(E, pid, cat, of), pouco='sai uma abaixo' if cat else 'sai tosca', banca='runas' if of == 'encanto' else 'oficina'))
    if mao(p, of) < O.MAO_DA_OBRA[cat]:
        L.append(f"AVISO: a obra {FEM[cat]} pede mão de {T.MAESTRIAS[O.MAO_DA_OBRA[cat]]}; a sua é de {T.MAESTRIAS[mao(p, of)]}. Pode tentar; o que entra na obra não volta.")
    return '\n'.join(L)


# ---------- a maestria ----------
def sobe(E, pid, oficio='forja'):
    """a maestria do ofício sobe quando os blocos de bancada chegam; de Mestre para cima, só com o FEITO (marca.feito_OFICIO)"""
    p = E['gente'][pid]; tem = mao(p, oficio); bl = bancada(p, oficio); txt = ''
    for grau in sorted(O.OFICIO_BLOCOS):
        quer = talento.pede(p, oficio, O.OFICIO_BLOCOS, grau)             # os blocos vezes o talento (etapa da magia), até o teto dele
        if grau <= tem: continue
        if quer is None:
            if bl >= O.OFICIO_BLOCOS[grau]: txt = f" (a mão não sobe mais em {oficio}: o talento para em {T.MAESTRIAS[talento.teto(p, oficio)]})"
            break
        if bl < quer: continue
        if grau in O.FEITO_OBRA and p.get('marca', {}).get(f'feito_{oficio}', 0) < grau:
            txt = f" (tem os blocos para {T.MAESTRIAS[grau]} em {oficio}; falta o feito: uma obra {FEM[O.FEITO_OBRA[grau]]}, ou melhor, nascida da sua mão)"; break
        estado.aplica(E, 'treinar', [['pessoa', pid, 'maestria.' + oficio, 'poe', grau]], onde=p['lugar'], quem=[pid], texto=f"{p['nome']} chega a {T.MAESTRIAS[grau]} em {oficio}")
        p = E['gente'][pid]; tem = grau; txt = f'. MAESTRIA: {T.MAESTRIAS[grau]} em {oficio}'
    return txt


# ---------- forjar ----------
def escolhe_agora(it):
    """(a regra da fase 1a) a peça escolhe os efeitos agora? Só a FERRAMENTA (os efeitos de ferramenta estão no catálogo); a arma, a armadura e o resto guardam os seus em
    efeitos_livres e cheios_livres até o catálogo de luta chegar (a fase 1b)"""
    return it.get('tipo') == 'ferramenta'


def diz_quem_escolhe(peca):
    return ('na ferramenta, quem forjou escolhe os efeitos (`oficio.py efeito ITEM CHAVE [cheio]`), ou a sua receita os escolhe sozinha (`oficio.py receita TIPO chave,chave`)'
            if escolhe_agora(peca) else 'os efeitos desta peça ficam por escolher: o catálogo de luta chega na próxima fase')


def _molde_ok(E, pid, peca, chave):
    """o MOLDE DE MESTRE dito ao abrir a obra (molde=CHAVE): pede uma ferramenta com o molde em uso; o efeito tem de caber na peça (na fase 1a, só na ferramenta) e na porta que
    a obra abre (a categoria da obra). Devolve a chave do catálogo, ou sai com a frase."""
    k = O.chave_efeito(chave); of = oficio_de(peca)
    if of not in O.VALOR_OFICIOS: sys.exit('o molde de mestre é da forja e do couro (a Lei do Valor)')
    if not efeitos_em_uso(E, pid, of).get('molde'): sys.exit('o molde (molde=CHAVE) pede uma ferramenta com o MOLDE DE MESTRE em uso (o efeito apelão, da ferramenta Lendária)')
    if not escolhe_agora(peca): sys.exit('na fase 1a só a ferramenta escolhe efeitos: o molde de uma arma, armadura ou escudo espera o catálogo de luta (a próxima fase)')
    if k not in O.FERRAMENTA_EFEITOS or k in ESCOLHE_NAO: sys.exit(f'"{chave}" não é efeito de ferramenta (os que há: {", ".join(O.FERRAMENTA_EFEITOS)})')
    if not O.cabe_forca(O.FERRAMENTA_EFEITOS[k][0], peca['cat']): sys.exit(f'o molde "{k}" é {O.FERRAMENTA_EFEITOS[k][0]}: a obra {FEM[peca["cat"]]} não abre essa porta (fraco na Comum, normal na Incomum, forte na Épica, apelão na Lendária)')
    return k


def forjar(E, pid, peca, blocos=None, nucleo=None, molde=None):
    """abre a obra (a matéria sai da carga e entra nela) e trabalha `blocos` blocos (None: até fechar, ou até o corpo parar; 0: só abre).
    (fase 1a) Com o POUPA-FERRO de uma ferramenta em uso, a obra gasta 1 a menos da matéria principal (se a peça leva 3 ou mais dela); com o MOLDE DE MESTRE, molde=CHAVE."""
    p = _vivo(E, pid); lid = p['lugar']; cat = peca['cat']; of = oficio_de(peca)
    if banca(E, lid, of) is None: sys.exit(_sem_banca(E, lid, of) + ': a obra não abre')
    mat = materia_da_obra(E, pid, peca); carga = p.get('carga', {}); falta = {k: n - carga.get(k, 0) for k, n in mat.items() if carga.get(k, 0) < n}
    if falta: sys.exit(f"falta matéria para {_peca(peca)}: {_lista(falta)} (a obra pede {_lista(mat)})")
    km = _molde_ok(E, pid, peca, molde) if molde else None
    nid = _nucleo(E, pid, cat, nucleo) if O.pede_nucleo(cat) else None
    if nucleo and not nid: sys.exit(f'uma obra {FEM[cat]} não leva núcleo (só do {T.CATS[M.MATERIA_ATE + 1]} para cima)')
    reg = dict(quem=pid, lugar=lid, tipo='forjar', oficio=of, peca=dict(peca), cat=cat, blocos=0, pede=O.blocos(cat), materia=mat, nucleo=nid)
    if km: reg['molde'] = km
    ef = [['pessoa', pid, 'carga.' + k, 'soma', -n] for k, n in mat.items()] + [['obra', 'abre', reg]]
    if nid: ef.append(['item', nid, 'historia', 'junta', f"Dia {E['relogio']['dia']}: entrou na obra de {peca['nome']}"])
    poupa = ' (o poupa-ferro poupou 1 de metal)' if mat != materia_de(peca) else ''; diz_molde = f'; o molde: {km}' if km else ''
    estado.aplica(E, evento_de(of), ef, onde=lid, quem=[pid], texto=f"{p['nome']} abre a obra: {_peca(peca)}; entram {_lista(mat)}" + (f" e {E['itens']['itens'][nid]['nome']}" if nid else '') + poupa + diz_molde)
    oid = f"o{E['itens']['oseq']:04d}"
    R = continua(E, pid, oid, blocos)
    R['texto'] = f"Obra {oid} aberta: {_peca(peca)}. Entraram {_lista(mat)}" + (f" e o núcleo {nid}" if nid else '') + poupa + (f". O MOLDE DE MESTRE: se a peça sair {FEM[cat]} ou acima, nasce com {km}, fora do teto" if km else '') + '.\n' + R['texto']
    return R


def _obra(E, pid, oid=None):
    minhas = obras_de(E, pid)
    if oid:
        if oid not in minhas: sys.exit(f'não há a obra "{oid}" aberta em nome de {E["gente"][pid]["nome"]}' + (f' (abertas: {", ".join(minhas)})' if minhas else ''))
        return minhas[oid]
    if len(minhas) == 1: return next(iter(minhas.values()))
    sys.exit('não há obra aberta.' if not minhas else f'há mais de uma obra aberta: diga qual ({", ".join(minhas)})')


def _nome_obra(E, o):
    if o['tipo'] == 'forjar': return _peca(o['peca'])
    if o['tipo'] in ('leva', 'gravar'): return o.get('nome') or o['tipo']                   # a leva e a gravação guardam o nome delas ao abrir
    it = E['itens']['itens'].get(o['item']); return f"o ajuste de {it['nome'] if it else o['item']}"


def continua(E, pid, oid=None, blocos=None):
    """trabalha na obra aberta. Para quando os blocos fecham (e aí sai o teste), quando acabam os blocos pedidos, ou quando o corpo cruza um limiar."""
    p = _vivo(E, pid); o = _obra(E, pid, oid); oid = o['id']; of = o['oficio']
    if p['lugar'] != o['lugar']: sys.exit(f"a obra {oid} está {_em(E, o['lugar'])}: é lá que se trabalha nela")
    if banca(E, o['lugar'], of) is None: sys.exit(_sem_banca(E, o['lugar'], of) + f": a obra {oid} não anda")
    if o.get('nucleo') and E['itens']['itens'].get(o['nucleo'], {}).get('dono') != pid: sys.exit(f"o núcleo da obra {oid} não está mais na mão de quem forja: a obra não anda (largue-a com `larga`)")
    if o['tipo'] in ('ajustar', 'gravar') and _ajuste_solto(E, o): sys.exit(f"{_ajuste_solto(E, o)}: a obra {oid} não anda (largue-a com `larga`)")       # a gravação, como o ajuste, trabalha na peça de alguém que está ali
    falta = max(0, o['pede'] - o['blocos']); n = falta if blocos is None else max(0, min(int(blocos), falta)); nome = _nome_obra(E, o)
    feitos, pq = ato.passa(E, pid, n, evento_de(of, o['tipo']), esforco='pesado', texto=f"{p['nome']} trabalha na obra: {nome}",
                           mais=lambda i: [['obra', oid, 'blocos', 'soma', 1], ['pessoa', pid, 'treino.' + of, 'soma', 1]])
    o = E['itens']['obras'][oid]; p = E['gente'][pid]
    R = dict(obra=oid, feitos=feitos, parou=pq, fim=None, item=None, rolagem=None)
    R['texto'] = f"{p['nome']} trabalha {tantos(feitos, 'bloco')} na obra {oid}, {nome}: {o['blocos']} de {o['pede']}" + (sobe(E, pid, of) if feitos else '') + (f'. PAROU: {pq}' if pq else '')
    if o['blocos'] >= o['pede'] and E['gente'][pid]['estado'] == 'vivo':
        F = remata(E, oid); R.update(fim=F['fim'], item=F['item'], rolagem=F['rolagem'], cat=o['cat'], sai=F.get('sai')); R['texto'] += '\n' + F['texto']
    return R


def remata(E, oid):
    """os blocos fecharam: sai o teste final (dado de verdade, uma vez) e a obra fecha"""
    o = E['itens'].get('obras', {}).get(oid) or sys.exit(f'não há a obra "{oid}"')
    if o['blocos'] < o['pede']: sys.exit(f"a obra {oid} tem {o['blocos']} de {o['pede']} blocos: o teste só sai quando os blocos fecham")
    _vivo(E, o['quem'])
    if o['tipo'] == 'leva': import alquimia; return alquimia.remata(E, o)          # a leva da alquimia e a gravação do encanto: quem remata é o módulo delas
    if o['tipo'] == 'gravar': import encanto; return encanto.remata(E, o)
    return _remata_forja(E, o) if o['tipo'] == 'forjar' else _remata_ajuste(E, o)


def _remata_valor(E, o):
    """(a LEI DO VALOR) os blocos fecharam: sai o teste (2d20 explosivos, uma vez; as faces de partida decidem os dados especiais), e a soma decide a categoria da peça"""
    oid = o['id']; pid = o['quem']; p = E['gente'][pid]; cat = o['cat']; peca = o['peca']; lid = o['lugar']; of = o['oficio']; nid = o.get('nucleo'); L = E['itens']['itens']
    if nid and nid not in L: sys.exit(f'o núcleo da obra {oid} não está mais no Livro de Itens: a obra não fecha (largue-a com `larga`)')
    c = valor(E, pid, cat, of, lid); nuc = L[nid]['nome'] if nid else None; dia = E['relogio']['dia']; fam = _fam(peca); fc = -1 if c['ferramenta_cat'] is None else c['ferramenta_cat']
    fx = c['fx']; prumo = fx['prumo']; lastro = bool(fx.get('lastro')); fagulha = bool(fx.get('fagulha')); tempera = fx['tempera']; km = o.get('molde')
    r = teste.rola(E, f"forjar {_peca(peca)}", 'Afinidade', c['contra'], mais=c['mais'], quem=pid, **({'dom': c['oculto']} if c['oculto'] else {}))
    a0, b0 = r['dados'][0][0], r['dados'][1][0]
    if r.get('posto_a_mao'): a0 = b0 = 10                    # o dado posto à mão (só na prova): sem dado especial
    n20 = 0 if r.get('posto_a_mao') else sum(1 for d in r['dados'] for f in d if f == 20)
    n19 = (a0 == 19) + (b0 == 19)                            # os dados que ABREM em 19 (a fagulha os conta como um 20)
    def saida(total):
        x_ = _resolve(total, a0, b0, c['teto'], fc, prumo, lastro)[0][1]
        return x_, conta_efeitos(x_, n20, n19, fagulha, tempera, molde=bool(km) and x_['cat'] is not None and not x_['salva'] and x_['cat'] >= cat)
    x, ce = saida(r['total'])
    if c['oculto']:                                          # o dom escondido FEZ a diferença se, sem ele, a peça sairia noutra categoria (ou se perderia), ou (fase 1a) com outro número de efeitos
        xs, cs = saida(r['total'] - c['oculto'])
        r['fez'] = (True if xs['cat'] is None else 'faixa') if xs['cat'] != x['cat'] else 'efeitos' if cs['efeitos'] != ce['efeitos'] else False
    sai = x['cat']; ef = []; it = None; molde_vale = bool(ce['molde'])
    fim = 'perdeu' if sai is None else 'acertou' if sai >= cat else 'abaixo'
    if sai is not None:
        padrao = molde(peca['tipo'], cat, familia=peca.get('familia'), material=peca.get('material'), cobre=peca.get('cobre'), forma=peca.get('forma') if peca['tipo'] == 'foco' else None, talhe=peca.get('talhe'), oficio=(peca.get('forma') if peca.get('forma') in ('martelo', 'tenaz') else peca.get('oficio')) if peca['tipo'] == 'ferramenta' else None)['nome']
        nome = None if sai != cat and peca['nome'] == padrao else peca['nome']           # a peça sem nome próprio ganha o nome da categoria em que nasceu
        forma = {'oficio': peca.get('oficio'), 'forma': peca.get('forma') or 'jogo'} if peca['tipo'] == 'ferramenta' else {} if peca['tipo'] in ('amuleto', 'gazua') else dict(familia=peca.get('familia'), material=peca.get('material'), cobre=peca.get('cobre'), **({'talhe': peca['talhe']} if peca.get('talhe') else {}))
        it = item(peca['tipo'], sai, nome, dono=pid, feito_por=pid, dia=dia, **forma)
        como = f"Dia {dia}: {p['nome']} forjou {_em(E, lid)}" + (f', com {nuc}' if nuc else '') + f" (a soma: {teste.total_visto(r)}; a obra era de matéria {FEM[min(cat, M.MATERIA_ATE)]}" + (f" e núcleo {T.CATS[cat]}" if cat > M.MATERIA_ATE else '') + ')'
        if x['tosca']: it['dur'][0] = max(1, int(it['dur'][1] * O.TOSCA)); como += '; a peça saiu tosca'
        it['teto_efeitos'] = ce['teto']                      # (fase 1a) o teto de efeitos, gravado ao nascer: o da categoria, mais a obra-prima no teto e o molde
        cheios = ce['cheios']
        if molde_vale:                                       # o MOLDE DE MESTRE: a peça nasce com o efeito dito ao abrir, fora do teto (e, se é de número e há cheio, cheio)
            m = {'chave': km}
            if O.de_numero(km) and cheios: m['cheio'] = True; cheios -= 1
            it['efeitos'].append(m)
        if ce['livres']: it['efeitos_livres'] = ce['livres']
        perdidos = 0
        if escolhe_agora(it): perdidos = max(0, cheios - cheios_possiveis(it)); cheios -= perdidos      # o cheio sem efeito de número onde cair se perde (a ferramenta Comum não tem nenhum)
        if cheios: it['cheios_livres'] = cheios
        if fx.get('sinete'): it['sinete'] = pid              # o SINETE: a peça leva o nome de quem a forjou
        if fx.get('degrau'): it['degrau'] = True             # o DEGRAU EMPRESTADO: um efeito dela pode ser da força de cima (só em peça de até 4 efeitos)
        faixa_txt = _diz_faixa(x, ce, c['teto'], prumo, it) + (f" ({tantos(perdidos, 'cheio se perde', 'cheios se perdem')}: não há efeito de número onde cair numa ferramenta {FEM[sai]})" if perdidos else '')
        if faixa_txt: como += f"; {faixa_txt}"
        if x['como']: como += f"; {x['como']}"
        if nid and L[nid].get('de'): it['nucleo_de'] = L[nid]['de']
        it['historia'].append(como); ef.append(['item', 'nasce', it])
        for grau, quer in sorted(O.FEITO_OBRA.items()):                     # o feito: uma obra nascida da categoria certa (ou melhor)
            if it['cat'] >= quer and p.get('marca', {}).get(f'feito_{of}', 0) < grau: ef.append(['pessoa', pid, f'marca.feito_{of}', 'poe', grau])
    volta = {k: n // 2 for k, n in (o.get('materia') or {}).items() if n // 2} if sai is None and fx.get('recobro') else {}       # o RECOBRO: a obra perdida devolve metade da matéria
    ef += [['pessoa', pid, 'carga.' + k, 'soma', n] for k, n in volta.items()]
    if nid: ef.append(['item', nid, 'some'])
    ef.append(['obra', oid, 'fecha'])
    if talento.decidiu(r): ef += talento.mostra(E, pid)
    conta_txt = f"soma {teste.total_visto(r)}"
    if sai is None: txt = (f"a obra de {_peca(peca)} se perde ({conta_txt}" + (f"; {x['como']}" if x['como'] else f", abaixo da CD do Comum, {O.VALOR_CD[0]}") + f"): some a matéria ({_lista(o['materia'])})" + (f' e some {nuc}' if nuc else '')
                           + (f"; o recobro devolve {_lista(volta)}" if volta else '; o recobro não devolve nada (metade, para baixo, de cada matéria)' if fx.get('recobro') else ''))
    else:
        txt = f"{p['nome']} forja {peca['nome'] if nome else _peca(it)}: {conta_txt}, a peça sai {FEM[sai]}" + (' (tosca)' if x['tosca'] else '')
        txt += (f"; {faixa_txt}" if faixa_txt else '') + (f"; {x['como']}" if x['como'] else '')
        if it.get('sinete'): txt += '; leva o seu sinete'
    estado.aplica(E, evento_de(of), ef, onde=lid, quem=[pid], texto=txt)
    iid = f"i{E['itens']['seq']:04d}" if it else None
    escolhas = _escolhe_ao_nascer(E, pid, iid) if iid else ''          # (fase 1a) a ferramenta escolhe na hora: pela receita do jogador, ou sozinha (quem não é o jogador)
    out = (teste.diz(E, r) + f"\n  (o +{c['mais']}: maestria {c['maestria']}, matéria {c['materia']}" + (f", núcleo {c['nucleo']}" if c['nucleo'] else '') + (f", martelo de forja {c['martelo']}" if c['martelo'] else '')
           + (f", tenaz {c['tenaz']}" if c['tenaz'] else '') + f", oficina {c['oficina']}, preparo {c['preparo']}) · as CDs: " + ' · '.join(f"{T.CATS[k]} {O.VALOR_CD[k]}" for k in range(min(c['teto'], len(O.VALOR_CD) - 1) + 1))
           + f" (o teto: {T.CATS[c['teto']]}" + (', a porta do degrau' if c.get('porta') else '') + ')' + (f" · {_diz_fx(fx)}" if _diz_fx(fx) else '') + '\n' + txt
           + (f'. Entrou no Livro de Itens: {iid}' if iid else '') + (f'. {escolhas}' if escolhas else '') + _diz_dom(E, pid, r) + sobe(E, pid, of))
    return dict(obra=oid, fim=fim, item=iid, rolagem=r, texto=out, sai=sai, cat=cat, efeitos=ce)


def _diz_fx(fx):
    """os efeitos das ferramentas em uso que mexem na obra, em palavras (ou '')"""
    P = []
    if fx.get('prumo'): P.append(f"prumo {fx['prumo']}")
    if fx.get('lastro'): P.append('lastro')
    if fx.get('fagulha'): P.append('fagulha')
    if fx.get('tempera'): P.append(f"têmpera {fx['tempera']}")
    if fx.get('recobro'): P.append('recobro')
    if fx.get('sinete'): P.append('sinete')
    if fx.get('poupa_ferro'): P.append('poupa-ferro')
    if fx.get('molde'): P.append('molde de mestre')
    if fx.get('degrau'): P.append('degrau emprestado')
    return ('os efeitos das suas ferramentas: ' + ', '.join(P)) if P else ''


def _diz_faixa(x, ce, teto, prumo=0, it=None):
    """A FAIXA EM PALAVRAS (fase 1a), para o remate e a história da peça: "faltaram 2 para a Rara (80): no fio, 4 da faixa, 1 dos 20: 4 efeitos por escolher (o teto da Incomum)
    e 1 cheio". '' se a peça se perdeu ou foi salva pela ferramenta (sai sem efeito)."""
    k = x.get('k')
    if k is None or x['cat'] is None or x.get('salva'): return ''
    cima = O.cd_de_cima(k); nome_cima = FEM[k + 1] if k + 1 < len(FEM) else 'Mítica'
    conta_prumo = f" (com o prumo {prumo}, contam {x['falta'] - prumo})" if prumo and x['falta'] > 0 else ''
    if k >= teto and x['falta'] <= 0: inicio = f"a {FEM[k]} é o teto desta obra e a soma passou da CD trancada ({nome_cima} {cima}): {ce['faixa']} da faixa"
    elif k >= teto: inicio = f"a {FEM[k]} é o teto desta obra (a régua para em {O.TETO_FAIXA}): faltaram {x['falta']} para a {nome_cima} ({cima}){conta_prumo}: {ce['faixa']} da faixa"
    else:
        cru = O.da_regua(x['falta'] - prumo)
        inicio = f"faltaram {x['falta']} para a {nome_cima} ({cima}){conta_prumo}: {O.FAIXA_NOME[cru]}, {ce['faixa']} da faixa" + (' (o lastro dá 1)' if ce['faixa'] > cru else '')
    partes = [f"{ce['vintes']} dos 20"] + ([f"{ce['fagulhas']} da fagulha"] if ce['fagulhas'] else []) + (['1 do quase'] if ce['quase'] else []) + (['1 da obra-prima no teto'] if x.get('mais_efeito') else [])
    cap = O.efeitos_max(x['cat']); n = ce['livres']; total = ce['n'] + x.get('mais_efeito', 0)
    if not n and not ce['molde']: fim = 'nenhum efeito'
    else:
        fim = (f"{tantos(n, 'efeito por escolher', 'efeitos por escolher')}" if n else '') + (f" (o teto da {FEM[x['cat']]}: {cap})" if ce['sobra'] else '')
        if ce['cheios']: fim += f", e {tantos(ce['cheios'], 'cheio', 'cheios')} (o número da categoria de cima num efeito de número" + (', com a têmpera' if ce['cheios'] > ce['sobra'] else '') + ')'
        if ce['molde']: fim = (fim + ', e ' if n else '') + 'o efeito do molde, fora do teto'
        if it is not None and n and not escolhe_agora(it): fim += ' (o catálogo de luta chega na próxima fase)'
    return f"{inicio}, {', '.join(partes)} = {total}: {fim}"


def _remata_forja(E, o):
    if o.get('oficio') in O.VALOR_OFICIOS: return _remata_valor(E, o)       # a forja e o couro: a Lei do Valor (o encanto segue com a categoria escolhida)
    oid = o['id']; pid = o['quem']; p = E['gente'][pid]; cat = o['cat']; peca = o['peca']; lid = o['lugar']; of = o['oficio']; nid = o.get('nucleo'); L = E['itens']['itens']
    if nid and nid not in L: sys.exit(f'o núcleo da obra {oid} não está mais no Livro de Itens: a obra não fecha (largue-a com `larga`)')
    c = conta(E, pid, cat, of, lid); nuc = L[nid]['nome'] if nid else None; dia = E['relogio']['dia']; fam = _fam(peca)
    r = teste.rola(E, f"forjar {_peca(peca)}", 'Afinidade', c['contra'], mais=c['mais'], quem=pid, **({'dom': c['oculto']} if c['oculto'] else {}))
    margem = r['total'] - r['contra']; fc = c.get('ferramenta_cat'); fc = -1 if fc is None else fc        # o poder da ferramenta que a pessoa tem (a categoria dela)
    por_pouco = O.POR_POUCO_RARA if fc >= 2 else O.POR_POUCO
    sai = cat if margem >= 0 else cat - 1 if (margem > -por_pouco or fc >= O.NADA_SE_PERDE) else None; ef = []; it = None
    acima = margem >= O.ACIMA_MARGEM and fc >= O.ACIMA_DO_FERRO and cat < O.FORJA_ATE      # a ferramenta Lendária: a peça que passa muito nasce uma categoria acima
    if acima: sai = cat + 1
    _faixa_do_dom(r, c, margem)
    fim = 'acertou' if margem >= 0 else 'abaixo' if sai is not None else 'perdeu'
    if sai is not None:
        padrao = molde(peca['tipo'], cat, familia=peca.get('familia'), material=peca.get('material'), cobre=peca.get('cobre'), forma=peca.get('forma') if peca['tipo'] == 'foco' else None, talhe=peca.get('talhe'), oficio=(peca.get('forma') if peca.get('forma') in ('martelo', 'tenaz') else peca.get('oficio')) if peca['tipo'] == 'ferramenta' else None)['nome']       # o nome que a obra ganha quando não se dá nome: diz a categoria DA OBRA
        nome = None if max(0, sai) != cat and peca['nome'] == padrao else peca['nome']      # a peça sem nome próprio que sai uma categoria abaixo ganha o nome da categoria em que saiu ("arco Incomum", e não "arco Raro")
        forma = {'forma': fam} if peca['tipo'] == 'foco' else {'oficio': peca.get('oficio'), 'forma': peca.get('forma') or 'jogo'} if peca['tipo'] == 'ferramenta' else {} if peca['tipo'] in ('amuleto', 'gazua') else dict(familia=peca.get('familia'), material=peca.get('material'), cobre=peca.get('cobre'), **({'talhe': peca['talhe']} if peca.get('talhe') else {}))
        it = item(peca['tipo'], max(0, sai), nome, dono=pid, feito_por=pid, dia=dia, **forma)
        como = f"Dia {dia}: {p['nome']} forjou {_em(E, lid)}" + (f', com {nuc}' if nuc else '')
        if sai < 0: it['dur'][0] = max(1, int(it['dur'][1] * O.TOSCA)); como += '; a peça saiu tosca'
        elif sai < cat: como += f'; a obra era {FEM[cat]} e a peça saiu {FEM[sai]}'
        elif acima: como += f'; a obra era {FEM[cat]} e a ferramenta Lendária a fez nascer {FEM[sai]}'
        livres = O.efeitos_da_obra(margem, it['cat'], facil=fc >= O.OBRA_PRIMA_FACIL) if margem >= 0 else 0
        if livres: it['efeitos_livres'] = livres; como += f'; OBRA-PRIMA: passou por {margem}, {livres} efeito{"s" if livres > 1 else ""} por escolher' + ('' if escolhe_agora(it) else ' (o catálogo de luta chega na próxima fase)')
        if nid and L[nid].get('de'): it['nucleo_de'] = L[nid]['de']
        it['historia'].append(como); ef.append(['item', 'nasce', it])
        for grau, quer in sorted(O.FEITO_OBRA.items()):                     # o feito: uma obra nascida da categoria certa (ou melhor)
            if it['cat'] >= quer and p.get('marca', {}).get(f'feito_{of}', 0) < grau: ef.append(['pessoa', pid, f'marca.feito_{of}', 'poe', grau])
    if nid: ef.append(['item', nid, 'some'])
    ef.append(['obra', oid, 'fecha'])
    if talento.decidiu(r): ef += talento.mostra(E, pid)                    # o dom escondido fez a diferença: a pessoa vê que tem
    conta_txt = f"{teste.total_visto(r)} contra {r['contra']}"
    if fim == 'acertou': txt = f"{p['nome']} forja {_peca(peca)}: {conta_txt}" + (f"; a ferramenta Lendária a fez nascer {FEM[sai]}" if acima else '') + (f"; OBRA-PRIMA: {it['efeitos_livres']} efeito{'s' if it['efeitos_livres'] > 1 else ''} por escolher" + ('' if escolhe_agora(it) else ' (o catálogo de luta chega na próxima fase)') if it and it.get('efeitos_livres') else '')
    elif fim == 'abaixo': txt = f"{p['nome']} erra por pouco ({conta_txt}): {peca['nome']} sai " + (f'{FEM[sai]}, uma categoria abaixo' if sai >= 0 else 'Comum e tosca') + (f'; {nuc} se gasta nela' if nuc else '')
    else: txt = f"a obra de {_peca(peca)} se perde ({conta_txt}): some a matéria ({_lista(o['materia'])})" + (f' e some {nuc}' if nuc else '')
    estado.aplica(E, evento_de(of), ef, onde=lid, quem=[pid], texto=txt)
    iid = f"i{E['itens']['seq']:04d}" if it else None
    out = teste.diz(E, r) + f"\n  (o +{c['mais']}: maestria {c['maestria']}, {'runas' if of == 'encanto' else 'oficina'} {c['oficina']}, preparo {c['preparo']}" + (f", ferramenta {c['ferramenta']}" if c.get('ferramenta') else '') + ")\n" + txt + (f'. Entrou no Livro de Itens: {iid}' if iid else '') + _diz_dom(E, pid, r) + sobe(E, pid, of)
    return dict(obra=oid, fim=fim, item=iid, rolagem=r, texto=out)


def _faixa_do_dom(r, c, margem):
    """o teste da bancada tem três faixas (acerta, sai uma abaixo, perde tudo): o dom escondido FEZ a diferença se mudou a faixa (r['fez'], que o teste.diz e o talento.decidiu leem)"""
    if not c.get('oculto'): return
    faixa = lambda m: 0 if m >= 0 else 1 if m > -O.POR_POUCO else 2
    sem = margem - c['oculto']
    r['fez'] = (True if margem >= 0 else 'faixa') if faixa(sem) != faixa(margem) else False


def _diz_poder(fc):
    """o poder das ferramentas pela maior categoria delas, em palavras (a Lei do Valor)"""
    P = []
    if fc >= 2: P.append(f'a matéria só se perde {O.VALOR_SEGURA} abaixo da CD do Comum (a peça sai Comum, tosca)' if fc < O.NADA_SE_PERDE else 'a matéria nunca se perde, nem nos dois 1 (a peça sai, no pior, Comum e tosca)')
    if fc >= O.OBRA_PRIMA_FACIL: P.append(f'o QUASE: +1 efeito quando a soma fica a {O.QUASE_JANELA} ou menos da CD seguinte')
    if fc >= O.ACIMA_DO_FERRO: P.append('ACIMA DO FERRO: na obra com núcleo, o teto sobe uma categoria')
    return (' · poder: ' + '; '.join(P)) if P else ''


def _diz_dom(E, pid, r):
    return f" Foi o dom que fez a diferença: há alguma coisa nas mãos de {E['gente'][pid]['nome']}." if talento.decidiu(r) else ''


def larga(E, pid, oid):
    """abandona a obra. A matéria que já foi ao fogo se perde (com zero blocos, volta à carga); o núcleo fica com o dono: só o teste o gasta."""
    p = _vivo(E, pid); o = _obra(E, pid, oid); ef = [['obra', o['id'], 'fecha']]; leva_materia = o['tipo'] in ('forjar', 'leva', 'gravar'); volta = leva_materia and o['blocos'] == 0
    if volta: ef += [['pessoa', pid, 'carga.' + k, 'soma', n] for k, n in o['materia'].items()]
    txt = f"{p['nome']} larga a obra: {_nome_obra(E, o)}" + ('' if not leva_materia else f" (a matéria volta: {_lista(o['materia'])})" if volta else f" (a matéria se perde: {_lista(o['materia'])})")
    estado.aplica(E, evento_de(o.get('oficio', 'forja'), o['tipo']), ef, onde=p['lugar'], quem=[pid], texto=txt)
    return dict(obra=o['id'], fim='largada', item=None, rolagem=None, texto=txt + '.')


# ---------- consertar ----------
def consertar(E, pid, iid, pontos=None, pago=False):
    """devolve durabilidade a uma peça da pessoa: ela mesma na bancada (blocos pesados e um pouco de matéria), ou paga à oficina do lugar (2% do preço por ponto)"""
    p = _vivo(E, pid); lid = p['lugar']; l = E['lugares'][lid]; it = E['itens']['itens'].get(iid) or sys.exit(f'não há o item "{iid}" no Livro de Itens')
    if it['tipo'] not in FORJA: sys.exit(f"{it['nome']} não é peça que se conserte")
    if it.get('dono') != pid: sys.exit(f"{it['nome']} não é de {p['nome']}")
    of = oficio_de(it); v = banca(E, lid, of); nb = nomes_banca(of)
    if v is None: sys.exit(_sem_banca(E, lid, of) + ': não se conserta aqui')
    gasto = it['dur'][1] - it['dur'][0]
    if gasto <= 0: sys.exit(f"{it['nome']} não precisa de conserto ({it['dur'][0]}/{it['dur'][1]})")
    q = gasto if pontos is None else min(int(pontos), gasto)
    if q < 1: sys.exit('diga quantos pontos consertar (1 ou mais)')
    cat = it['cat']; sobra = f" Pediu {pontos}; a peça só tinha {tantos(gasto, 'ponto gasto', 'pontos gastos')}." if pontos is not None and int(pontos) > gasto else ''
    if pago:
        if cat > v + O.OFICINA_CONSERTA: sys.exit(f"a {nb[v]} {estado.de(E, lid)} só conserta até o {T.CATS[min(v + O.OFICINA_CONSERTA, len(T.CATS) - 1)]}; {it['nome']} é {T.CATS[cat]}")
        custo = O.conserto_pago(cat, q, M.peso_do_item(it))
        if p['moedas'] < custo: sys.exit(f"consertar {tantos(q, 'ponto')} de {_peca(it)} custa {custo} de prata; {p['nome']} tem {p['moedas']}")
        estado.aplica(E, 'consertar', [['pessoa', pid, 'moedas', 'soma', -custo], ['estoque', lid, 'prata', 'soma', custo], ['item', iid, 'dur', 'soma', q]], onde=lid, quem=[pid],
                      texto=f"{p['nome']} paga {custo} de prata à {nb[v]} pelo conserto de {it['nome']} ({tantos(q, 'ponto')})")
        n, pq = ato.passa(E, pid, math.ceil(q / O.PAGO_BLOCO), 'consertar', esforco='nada', texto=f"{p['nome']} espera o conserto", para=False)
        it = E['itens']['itens'][iid]
        return dict(pontos=q, custo=custo, feitos=n, parou=pq, texto=f"A {nb[v]} conserta {it['nome']}: {tantos(q, 'ponto')} por {custo} de prata, em {tantos(n, 'bloco')}. Durabilidade {it['dur'][0]}/{it['dur'][1]}.{sobra}")
    pede_mao = O.MAO_DA_OBRA[cat] if cat < len(O.MAO_DA_OBRA) else None
    if pede_mao is None or mao(p, of) < pede_mao:
        sys.exit(f"consertar uma peça {FEM[cat]} pede mão de {T.MAESTRIAS[pede_mao] if pede_mao is not None else 'quem ainda não existe'} em {of}; a de {p['nome']} é de {T.MAESTRIAS[mao(p, of)]}. Pago à oficina: {O.conserto_pago(cat, q, M.peso_do_item(it))} de prata.")
    chave = _materia_conserto(it) or sys.exit(f"{it['nome']} não é peça que a bancada saiba consertar"); unidades = math.ceil(q / O.CONSERTO_MATERIA)
    if p.get('carga', {}).get(chave, 0) < unidades: sys.exit(f"consertar {tantos(q, 'ponto')} de {it['nome']} gasta {unidades} de {_mat(chave)}; {p['nome']} carrega {p.get('carga', {}).get(chave, 0)}")
    pb = conserto_bloco(E, pid, of)                         # (fase 1a) o REMENDO de uma ferramenta em uso: 8 por bloco, não 5
    def mais(i):
        antes = i * pb; agora = min(pb, q - antes); un = math.ceil((antes + agora) / O.CONSERTO_MATERIA) - math.ceil(antes / O.CONSERTO_MATERIA)
        return [['item', iid, 'dur', 'soma', agora], ['pessoa', pid, 'treino.' + of, 'soma', 1]] + ([['pessoa', pid, 'carga.' + chave, 'soma', -un]] if un else [])
    antes = it['dur'][0]; tinha = p.get('carga', {}).get(chave, 0)
    n, pq = ato.passa(E, pid, math.ceil(q / pb), 'consertar', esforco='pesado', mais=mais, texto=f"{p['nome']} conserta {it['nome']}")
    it = E['itens']['itens'][iid]; p = E['gente'][pid]; feito = it['dur'][0] - antes
    return dict(pontos=feito, custo=0, feitos=n, parou=pq, texto=f"{p['nome']} conserta {it['nome']}: {tantos(feito, 'ponto')} em {tantos(n, 'bloco')}, com {tinha - p.get('carga', {}).get(chave, 0)} de {_mat(chave)}" + (f" (o remendo: {pb} por bloco)" if pb != O.CONSERTO_BLOCO else '') + f". Durabilidade {it['dur'][0]}/{it['dur'][1]}"
                + sobe(E, pid, of) + (f'. PAROU: {pq}' if pq else '.') + sobra)


def conserto_bloco(E, pid, oficio='forja'):
    """os pontos que um bloco de conserto na bancada devolve: 5; com o REMENDO de uma ferramenta em uso do ofício da peça (fase 1a), 8 (vale a melhor fonte)"""
    return max(O.CONSERTO_BLOCO, efeitos_em_uso(E, pid, oficio).get('remendo') or 0)


def ajuste_blocos(E, pid, cat, oficio='forja'):
    """os blocos do ajuste sob medida: um por degrau da categoria; com a MÃO DE MEDIDA de uma ferramenta em uso (fase 1a), a metade, para cima"""
    b = O.ajuste_blocos(cat); return math.ceil(b / 2) if efeitos_em_uso(E, pid, oficio).get('mao_de_medida') else b


# ---------- ajustar (sob medida) ----------
def _ajuste_solto(E, o):
    """por que o ajuste não pode seguir (ou None): a peça saiu do Livro ou mudou de mão, ou o dono dela foi embora"""
    it = E['itens']['itens'].get(o['item']); a = E['gente'].get(o['para'])
    if not it: return 'a peça não está mais no Livro de Itens'
    if it.get('dono') not in (o['quem'], o['para']): return f"{it['nome']} mudou de mão"
    if not a or a['estado'] != 'vivo' or a['lugar'] != o['lugar']: return 'quem ia receber a peça não está mais aqui'
    return None


def ajustar(E, pid, iid, para=None, blocos=None):
    """sob medida: abre o ajuste de uma peça para alguém que está aqui (sem `para`: para quem ajusta) e trabalha nele; no fim, um teste"""
    p = _vivo(E, pid); lid = p['lugar']; alvo = para or pid; a = _vivo(E, alvo); it = E['itens']['itens'].get(iid) or sys.exit(f'não há o item "{iid}" no Livro de Itens')
    if it['tipo'] not in PECAS: sys.exit(f"{it['nome']} não é peça que se ajuste")
    if oficina(E, lid) is None: sys.exit(f"{E['lugares'][lid]['nome']} não tem oficina: não se ajusta aqui")
    if a['lugar'] != lid: sys.exit(f"{a['nome']} não está aqui: o ajuste pede o corpo de quem vai usar a peça")
    if it.get('dono') not in (pid, alvo): sys.exit(f"{it['nome']} não é de {p['nome']}" + (f" nem de {a['nome']}" if alvo != pid else ''))
    of = oficio_de(it)
    if O.ajuste_grau(mao(p, of)) < T.SOB_MEDIDA_GRAUS[0]: sys.exit(f"ajustar pede pelo menos mão de {T.MAESTRIAS[2]} em {of}; a de {p['nome']} é de {T.MAESTRIAS[mao(p, of)]}")
    if any(o['tipo'] == 'ajustar' and o['item'] == iid for o in E['itens'].get('obras', {}).values()): sys.exit(f"{it['nome']} já está num ajuste aberto")
    reg = dict(quem=pid, lugar=lid, tipo='ajustar', oficio=of, item=iid, para=alvo, cat=it['cat'], blocos=0, pede=ajuste_blocos(E, pid, it['cat'], of))
    estado.aplica(E, 'ajustar', [['obra', 'abre', reg]], onde=lid, quem=[pid, alvo] if alvo != pid else [pid], texto=f"{p['nome']} abre o ajuste de {it['nome']} para {a['nome']}")
    oid = f"o{E['itens']['oseq']:04d}"
    R = continua(E, pid, oid, blocos); R['texto'] = f"Ajuste {oid} aberto: {_peca(it)} para {a['nome']}.\n" + R['texto']
    return R


def _remata_ajuste(E, o):
    oid = o['id']; pid = o['quem']; p = E['gente'][pid]; lid = o['lugar']; of = o['oficio']
    solto = _ajuste_solto(E, o)
    if solto:
        estado.aplica(E, 'ajustar', [['obra', oid, 'fecha']], onde=lid, quem=[pid], texto=f"o ajuste {oid} se desfaz: {solto}")
        return dict(obra=oid, fim='desfeito', item=o['item'], rolagem=None, texto=f"O ajuste {oid} se desfaz: {solto}.")
    it = E['itens']['itens'][o['item']]; a = E['gente'][o['para']]; cat = it['cat']; grau = O.ajuste_grau(mao(p, of)); c = conta(E, pid, cat, of, lid, contra=O.ajuste_contra(cat))
    medida = O.MEDIDA_TESTE if efeitos_em_uso(E, pid, of).get('mao_de_medida') else 0       # (fase 1a) a MÃO DE MEDIDA: +2 no teste do ajuste
    if medida: c['mais'] += medida; c['soma'] += medida
    r = teste.rola(E, f"ajustar {it['nome']} para {a['nome']}", 'Afinidade', c['contra'], mais=c['mais'], quem=pid, **({'dom': c['oculto']} if c['oculto'] else {}))
    margem = r['total'] - r['contra']; ef = [['obra', oid, 'fecha']]; _faixa_do_dom(r, c, margem); conta_txt = f"{teste.total_visto(r)} contra {r['contra']}"
    if talento.decidiu(r): ef += talento.mostra(E, pid)
    if margem >= 0 and grau >= T.SOB_MEDIDA_GRAUS[0]:
        fim = 'acertou'; txt = f"{p['nome']} ajusta {it['nome']} para {a['nome']}, grau {grau} ({conta_txt})"
        ef += [['item', o['item'], 'sob_medida', 'poe', dict(dono=a['nome'], grau=grau, id=o['para'])], ['item', o['item'], 'historia', 'junta', f"Dia {E['relogio']['dia']}: {p['nome']} ajustou para {a['nome']} (grau {grau})"]]
        corpo = estado.corpo_de(a)                          # O AJUSTE RECORTA A PEÇA (etapa 4b): a armadura passa a servir no corpo de quem a pede (tirada de uso antes, se preciso)
        if it['tipo'] == 'armadura' and (it.get('talhe') or 'gente') != corpo:
            if it.get('uso'): ef.append(['item', o['item'], 'uso', 'poe', None])
            ef.append(['item', o['item'], 'talhe', 'poe', None if corpo == 'gente' else corpo]); txt += f" (recortada para o corpo {'miúdo' if corpo == 'miúdo' else 'de gente'})"
    elif margem > -O.POR_POUCO: fim = 'falhou'; txt = f"o ajuste de {it['nome']} não assenta ({conta_txt}): fica como estava"
    else:
        fim = 'estragou'; txt = f"o ajuste de {it['nome']} sai errado ({conta_txt}): a peça perde {O.AJUSTE_ESTRAGO} de durabilidade"
        ef.append(['item', o['item'], 'dur', 'soma', -O.AJUSTE_ESTRAGO])
    estado.aplica(E, 'ajustar', ef, onde=lid, quem=[pid], texto=txt)
    return dict(obra=oid, fim=fim, item=o['item'], rolagem=r, texto=teste.diz(E, r) + f"\n  (o +{c['mais']}: maestria {c['maestria']}, oficina {c['oficina']}, preparo {c['preparo']}" + (f", ferramenta {c['ferramenta']}" if c.get('ferramenta') else '') + (f", mão de medida {medida}" if medida else '') + ")\n" + txt + '.' + _diz_dom(E, pid, r))


# ---------- o jornal: a bancada a serviço da oficina do lugar ----------
def jornal(E, pid, blocos, oficio='forja'):
    """N blocos de bancada no serviço miúdo da oficina (a ferramenta do povo): o lugar paga o salário do grau de ofício da pessoa, e os blocos contam como bancada.
    A paga segue a JORNADA (tabelas_mundo: 2 blocos pagos por dia, junto com o `ato.py trabalhar`); passado isso, ou sem prata na oficina, o bloco é só bancada."""
    p = _vivo(E, pid); lid = p['lugar']
    if oficio not in O.BANCA: sys.exit(f'o jornal é de {", ".join(O.BANCA)} (veio "{oficio}")')
    if banca(E, lid, oficio) is None: sys.exit(_sem_banca(E, lid, oficio) + ': não há onde servir')
    grau = O.jornal_grau(mao(p, oficio), p.get('grau_oficio', 'diarista')); paga = M.SALARIO[grau]; tinha = p['moedas']
    def mais(i):
        ef = [['pessoa', pid, 'treino.' + oficio, 'soma', 1]]
        if ato.jornada(E, pid) < M.JORNADA and E['lugares'][lid]['estoque'].get('prata', 0) >= paga: ef += ato.paga_bloco(E, pid, lid, paga)      # depois da jornada, e sem prata, a oficina não paga
        return ef
    onde_serve = dict(encanto='na mesa de runas', alquimia='na botica', fé='no santuário').get(oficio, 'na bancada da oficina')
    n, pq = ato.passa(E, pid, int(blocos), 'trabalhar', esforco=O.JORNAL_ESFORCO if oficio in ('forja', 'couro') else 'leve', mais=mais, texto=f"{p['nome']} serve {onde_serve} ({grau})")
    ganhou = E['gente'][pid]['moedas'] - tinha
    sobe_txt = sobe(E, pid, oficio) if oficio in ('forja', 'couro', 'alquimia', 'encanto') else __import__('magia_mundo').sobe(E, pid, oficio)       # a fé sobe pela tabela das armas (magia_mundo)
    return dict(feitos=n, parou=pq, ganhou=ganhou, texto=f"{p['nome']} serve {tantos(n, 'bloco')} {onde_serve} e recebe {ganhou} de prata" + ('' if ganhou == n * paga else f' (o lugar paga {M.JORNADA} blocos por dia a cada um, e só enquanto tem prata; o resto é serviço sem paga)')
                + sobe_txt + (f'. PAROU: {pq}' if pq else '.'))


# ---------- escolher os efeitos (a parte 2, fase 1a: o contrato, 5.7; só a FERRAMENTA escolhe agora) ----------
def teto_de(it):
    """o teto de efeitos da peça: o gravado ao nascer (a categoria, a obra-prima no teto, o molde); a peça antiga sem o campo, o da categoria"""
    t = it.get('teto_efeitos'); return t if isinstance(t, int) and not isinstance(t, bool) else O.efeitos_max(it['cat'])


def _tem_emprestado(it): return any(isinstance(e, dict) and e.get('emprestado') for e in it.get('efeitos') or [])


def efeitos_que_cabem(it, emprestado=False):
    """os efeitos que cabem nesta peça agora: na FERRAMENTA, os de ferramenta cuja porta a categoria dela abre (com o degrau emprestado, a força de cima), que ela ainda não
    tem. Na arma, na armadura e no resto, nenhum na fase 1a: os efeitos delas ficam por escolher até o catálogo de luta (a fase 1b)."""
    if not escolhe_agora(it): return []
    tem_ja = {e.get('chave') for e in it.get('efeitos') or [] if isinstance(e, dict)}
    return [k for k, v in O.FERRAMENTA_EFEITOS.items() if k not in tem_ja and k not in ESCOLHE_NAO and O.cabe_forca(v[0], it['cat'], emprestado)]


def cheios_possiveis(it):
    """quantos cheios a peça ainda pode usar: um por efeito de número que ainda cabe nela (na ferramenta, o prumo e a têmpera); na peça que não escolhe agora, os por escolher"""
    if not escolhe_agora(it): return it.get('efeitos_livres') or 0
    return min(it.get('efeitos_livres') or 0, sum(1 for k in efeitos_que_cabem(it) if O.de_numero(k)))


def _sorte_fixa(E, chave):
    """o acaso do mundo que NÃO muda com o dia (o jeito de uma pessoa, a ordem de uma peça): sai da semente e da chave. Mesma semente, mesma escolha."""
    import hashlib, random
    return random.Random(int.from_bytes(hashlib.sha256(f"{E['relogio']['semente']}|{chave}".encode()).digest()[:8], 'big'))


def jeito(E, quem):
    """o JEITO de um ferreiro (ou de uma loja: quem é o id do lugar), sorteado pela semente e pelo id: do gume, da guarda, do fôlego ou do tranco"""
    return O.JEITOS[_sorte_fixa(E, f'jeito|{quem}').randrange(len(O.JEITOS))]


def receita_do_jeito(E, jt, iid):
    """a receita do jeito, numa ferramenta: os efeitos de NÚMERO primeiro (para o cheio ter onde cair), depois os do jeito, e o resto na ordem da semente (o empate)"""
    numero = [k for k in O.FERRAMENTA_EFEITOS if O.de_numero(k)]; dele = [k for k in O.JEITO_FERRAMENTA[jt] if k not in numero]
    resto = [k for k in O.FERRAMENTA_EFEITOS if k not in numero and k not in dele]; _sorte_fixa(E, f'efeito|{iid}').shuffle(resto)
    return numero + dele + resto


def receita_de(E, pid, it):
    """a receita do jogador para esta peça (a ordem que vale sempre: marca.receita), ou None. Na ferramenta: a da forma (martelo, tenaz, jogo), ou a de toda ferramenta."""
    rc = (E['gente'][pid].get('marca') or {}).get('receita')
    if not isinstance(rc, dict) or not escolhe_agora(it): return None
    return rc.get(it.get('forma') or 'jogo') or rc.get('ferramenta')


def _diz_um(k, cat, cheio=False, emprestado=False):
    import itens as IT
    return IT.frase_efeito({'chave': k, 'cheio': cheio, 'emprestado': emprestado}, cat)
def IT_frase(k, cat): import itens as IT; return IT.frase_efeito({'chave': k}, cat, nome=False)


def _escolhe(E, iid, k, cheio=False, emprestado=False, quem=None, como=''):
    """UMA escolha, UM evento: o efeito entra na peça, sai um dos por escolher (e um cheio, se cheio); o cheio que não tem mais onde cair se perde. Sem conferir quem é o dono
    (quem chama confere: o comando, a receita, o ferreiro do mundo, a loja)."""
    it = E['itens']['itens'][iid]; reg = {'chave': k}
    if cheio: reg['cheio'] = True
    if emprestado: reg['emprestado'] = True
    livres = (it.get('efeitos_livres') or 0) - 1; cheios = (it.get('cheios_livres') or 0) - (1 if cheio else 0)
    depois = dict(it, efeitos=list(it.get('efeitos') or []) + [reg], efeitos_livres=livres)
    cheios = min(cheios, cheios_possiveis(depois)) if livres else 0                    # o cheio sem efeito de número para encher se perde
    ef = [['item', iid, 'efeito', 'junta', reg], ['item', iid, 'cheios_livres', 'poe', max(0, cheios)], ['item', iid, 'efeitos_livres', 'soma', -1]]
    frase = _diz_um(k, it['cat'], cheio, emprestado); nome = E['gente'][quem]['nome'] if quem in E['gente'] else (E['lugares'][quem]['nome'] if quem in E['lugares'] else 'o mundo')
    ef.append(['item', iid, 'historia', 'junta', f"Dia {E['relogio']['dia']}: {nome} deu à peça o efeito: {frase}" + (f" ({como})" if como else '')])
    estado.aplica(E, 'forjar', ef, onde=E['gente'][quem]['lugar'] if quem in E['gente'] else quem if quem in E['lugares'] else None, quem=[quem] if quem in E['gente'] else [],
                  texto=f"{nome} escolhe o efeito de {it['nome']}: {frase}" + (f" ({como})" if como else ''))
    return frase


def aplica_receita(E, iid, receita, quem=None, como='pela receita'):
    """escolhe pela receita, um evento por escolha: desce a lista e põe cada efeito que cabe (a porta, o tipo, o repetido), até acabarem os por escolher; o de número leva o
    cheio enquanto houver. Devolve (os escolhidos em palavras, os que não couberam)."""
    feitos = []; fora = []
    for k in [O.chave_efeito(x) for x in receita]:
        it = E['itens']['itens'][iid]
        if not it.get('efeitos_livres'): break
        if k not in efeitos_que_cabem(it):
            if k not in {e.get('chave') for e in it.get('efeitos') or []}: fora.append(k)
            continue
        feitos.append(_escolhe(E, iid, k, cheio=O.de_numero(k) and (it.get('cheios_livres') or 0) > 0, quem=quem, como=como))
    return feitos, fora


def escolhe_sozinho(E, iid, quem=None, jt=None):
    """O MUNDO ESCOLHE SOZINHO quando a peça nasce (ou a loja, ao comprar: quem é o id do lugar): pelo jeito de quem escolhe, sorteado pela semente (mesma semente, mesma
    escolha). Na fase 1a, só na ferramenta. Devolve (o jeito, os escolhidos)."""
    it = E['itens']['itens'][iid]
    if not escolhe_agora(it) or not it.get('efeitos_livres'): return None, []
    quem = quem or it.get('dono') or it.get('feito_por'); jt = jt or jeito(E, quem)
    return jt, aplica_receita(E, iid, receita_do_jeito(E, jt, iid), quem=quem, como=f'o jeito {O.JEITO_DIZ[jt]}')[0]


def _escolhe_ao_nascer(E, pid, iid):
    """a ferramenta que nasce com efeitos escolhe na hora: a do jogador, pela receita dele (a mesa só relata; pergunta quando a receita não cabe); a de quem não é o jogador,
    sozinha, pelo jeito. A arma, a armadura e o resto guardam os efeitos (a fase 1b). Devolve a frase para a mesa (ou '')."""
    it = E['itens']['itens'][iid]; n = it.get('efeitos_livres') or 0
    if not n: return ''
    if not escolhe_agora(it): return f"Efeitos por escolher: {n} (o catálogo de luta chega na próxima fase)" + (f", e {tantos(it['cheios_livres'], 'cheio')}" if it.get('cheios_livres') else '')
    if not E['gente'][pid].get('jogador'):
        jt, feitos = escolhe_sozinho(E, iid, pid)
        return f"{E['gente'][pid]['nome']} escolhe pelo jeito {O.JEITO_DIZ[jt]}: " + (' e '.join(feitos) if feitos else 'nada coube')
    rc = receita_de(E, pid, it); txt = ''
    if rc:
        feitos, fora = aplica_receita(E, iid, rc, quem=pid, como='pela sua receita')
        txt = ('Pela sua receita: ' + ' e '.join(feitos)) if feitos else 'A sua receita não coube nesta peça'
        if fora: txt += f" (não couberam: {', '.join(fora)}: a porta da {FEM[it['cat']]} ou o tipo da peça)"
    it = E['itens']['itens'][iid]; resta = it.get('efeitos_livres') or 0
    if resta: txt += ('. ' if txt else '') + f"{tantos(resta, 'efeito', 'efeitos')} por escolher" + (f" ({tantos(it['cheios_livres'], 'cheio')})" if it.get('cheios_livres') else '') + f": `oficio.py efeito {iid}` mostra o que cabe"
    return txt


def diz_cabem(E, pid, it, iid=None):
    """sem CHAVE: a lista do que cabe na peça, com o número na categoria dela, o número cheio e o que vale (pontos de feitio por obra, medidos no banco)"""
    L = []
    for k in efeitos_que_cabem(it):
        forca, _porta, nums, _faz, vale = O.FERRAMENTA_EFEITOS[k]
        L.append(f"- {k} ({forca}): {IT_frase(k, it['cat'])}" + (f"; cheio, {O.valor_ferramenta(k, it['cat'], True)}" if nums else '') + f" · vale: {vale}")
    if it.get('degrau') and not _tem_emprestado(it):
        mais = [k for k in efeitos_que_cabem(it, emprestado=True) if k not in efeitos_que_cabem(it)]
        if mais: L.append('- com o DEGRAU EMPRESTADO (`emprestado`; só um, e só em peça de até 4 efeitos): ' + ', '.join(mais))
    cab = (f"{it['nome']} ({FEM[it['cat']]}): {tantos(it.get('efeitos_livres') or 0, 'efeito', 'efeitos')} por escolher" + (f", {tantos(it['cheios_livres'], 'cheio')} (só em efeito de número: diga `cheio`)" if it.get('cheios_livres') else '')
           + f"; o teto de efeitos dela: {teto_de(it)}. Cabem (a porta da {FEM[it['cat']]}: {O.forca_da_cat(it['cat'])}; `oficio.py efeito {iid or 'ITEM'} CHAVE [cheio]`, ou `auto`, pela receita):")
    return '\n'.join([cab] + (L or ['- nada (a peça já tem tudo o que a porta dela abre)']))


def efeito(E, pid, iid, chave=None, cheio=False, emprestado=False, valor=None):
    """quem tem a peça escolhe UM dos efeitos por escolher (cada escolha, um evento). Na fase 1a, SÓ A FERRAMENTA escolhe: a arma, a armadura e o resto guardam os efeitos
    até o catálogo de luta. Sem chave: a lista do que cabe. chave 'auto': pela receita do jogador (ou, sem ela, pela receita da guarda)."""
    p = E['gente'][pid]; it = E['itens']['itens'].get(iid) or sys.exit(f'não há o item "{iid}" no Livro de Itens')
    if it.get('dono') != pid: sys.exit(f"{it['nome']} não é de {p['nome']}: escolhe os efeitos quem tem a peça")
    n = it.get('efeitos_livres') or 0
    if not escolhe_agora(it):
        sys.exit(f"{it['nome']}: efeitos por escolher: {n} (o catálogo de luta chega na próxima fase)" if n else f"{it['nome']} não tem efeito por escolher (e, na fase 1a, só a ferramenta escolhe)")
    if not n: sys.exit(f"{it['nome']} não tem efeito por escolher (os efeitos nascem da faixa da forja: `oficio.py pede` mostra a régua)")
    if chave is None: return diz_cabem(E, pid, it, iid)
    if chave == 'auto':
        rc = receita_de(E, pid, it); jt = None if rc else O.RECEITA_AUTO['ferramenta']
        feitos, fora = aplica_receita(E, iid, rc or receita_do_jeito(E, jt, iid), quem=pid, como='pela sua receita' if rc else f'pela receita {O.JEITO_DIZ[jt]}')
        it = E['itens']['itens'][iid]; resta = it.get('efeitos_livres') or 0
        return (f"{it['nome']}, " + ('pela sua receita' if rc else f'pela receita {O.JEITO_DIZ[jt]}') + ': ' + (' e '.join(feitos) if feitos else 'nada coube')
                + (f" (não couberam: {', '.join(fora)})" if fora else '') + '.' + (f" Ainda há {resta} por escolher." if resta else ''))
    k = O.chave_efeito(chave)
    if k not in O.FERRAMENTA_EFEITOS: sys.exit(f'"{chave}" não é efeito de ferramenta. ' + diz_cabem(E, pid, it, iid))
    if k in {e.get('chave') for e in it.get('efeitos') or []}: sys.exit(f"{it['nome']} já tem {k}: o mesmo efeito não se repete na peça")
    forca = O.FERRAMENTA_EFEITOS[k][0]
    if emprestado:
        if not it.get('degrau'): sys.exit(f"{it['nome']} não nasceu com o degrau emprestado (a ferramenta Lendária que o dá estava em uso quando ela foi forjada?)")
        if _tem_emprestado(it): sys.exit(f"{it['nome']} já tem um efeito do degrau emprestado: é a porta adiantada dela, uma só")
        if O.cabe_forca(forca, it['cat']): sys.exit(f"{k} já cabe na porta da {FEM[it['cat']]}: não precisa do degrau emprestado")
        if len(it.get('efeitos') or []) + n > O.DEGRAU_ATE: sys.exit(f"o degrau emprestado só entra em peça de até {O.DEGRAU_ATE} efeitos; {it['nome']} terá {len(it.get('efeitos') or []) + n}")
    if not O.cabe_forca(forca, it['cat'], emprestado): sys.exit(f"{k} é {forca}: a porta da {FEM[it['cat']]} não abre essa força (fraco na Comum, normal na Incomum, forte na Épica, apelão na Lendária)")
    if cheio and not O.de_numero(k): sys.exit(f"{k} não tem número: o cheio só vale em efeito de número (o prumo, a têmpera)")
    if cheio and not it.get('cheios_livres'): sys.exit(f"{it['nome']} não tem cheio por escolher (o cheio nasce do que passa do teto de efeitos, e da têmpera)")
    frase = _escolhe(E, iid, k, cheio=cheio, emprestado=emprestado, quem=pid)
    it = E['itens']['itens'][iid]; resta = it.get('efeitos_livres') or 0
    return f"{it['nome']} ganha o efeito: {frase}." + (f" Ainda há {resta} por escolher" + (f" ({tantos(it['cheios_livres'], 'cheio')})" if it.get('cheios_livres') else '') + '.' if resta else '')


def receita(E, pid, tipo=None, chaves=None):
    """A RECEITA DO JOGADOR: uma ordem que vale sempre, por tipo de peça (na fase 1a, as ferramentas: martelo, tenaz, jogo, ou ferramenta para todas); a obra que nasce com efeitos
    escolhe por ela, e a mesa só relata. Sem tipo: mostra as receitas. chaves 'nada': apaga a do tipo."""
    p = E['gente'][pid]; rc = dict((p.get('marca') or {}).get('receita') or {})
    if tipo is None: return 'As suas receitas: ' + (' · '.join(f"{t}: {', '.join(v)}" for t, v in rc.items()) if rc else 'nenhuma (`oficio.py receita tenaz prumo,afinada,fagulha`)')
    if tipo not in ('martelo', 'tenaz', 'jogo', 'ferramenta'):
        sys.exit(f'a receita é por tipo de peça; na fase 1a só a ferramenta escolhe: martelo, tenaz, jogo ou ferramenta (todas). A da arma e da armadura chega com o catálogo de luta (veio "{tipo}")')
    if chaves in (None, ''): sys.exit(f'diga a ordem: `oficio.py receita {tipo} prumo,afinada,fagulha` (ou `nada`, para apagar)')
    if chaves == 'nada': rc.pop(tipo, None); novo = None
    else:
        novo = [O.chave_efeito(x) for x in chaves.split(',') if x.strip()]
        ruins = [x for x in novo if x not in O.FERRAMENTA_EFEITOS]
        if ruins: sys.exit(f'não são efeitos de ferramenta: {", ".join(ruins)} (os que há: {", ".join(O.FERRAMENTA_EFEITOS)})')
        if len(set(novo)) != len(novo): sys.exit('a receita não repete efeito')
        rc[tipo] = novo
    if not estado.aplica(E, 'forjar', [['pessoa', pid, 'marca.receita', 'poe', rc or None]], onde=p['lugar'], quem=[pid],
                         texto=f"{p['nome']} " + (f"apaga a receita de {tipo}" if novo is None else f"põe a receita de {tipo}: {', '.join(novo)}")): return 'A receita já era essa: nada mudou.'
    return (f"Receita de {tipo}: {', '.join(novo)}. A {tipo if tipo != 'ferramenta' else 'ferramenta'} que nascer com efeitos escolhe por ela, na hora; o que não couber (a porta, o repetido) fica para você."
            if novo else f"Receita de {tipo} apagada.")


# ---------- o preparo ganho no mundo (o Mestre registra) ----------
def ganha_preparo(E, qual, cat, pid=None, lid=None, como='', oficio='forja'):
    """registra um preparo do ofício: os da pessoa (receita, ajudante) vão para ela; os do lugar (fogo e bigorna; a vidraria da botica; a tinta e a pedra das runas), para o lugar
    onde ela está. `cat`: a categoria que ele alcança (None: perde-se)"""
    tab = tabela_preparos(oficio)
    if qual not in tab: sys.exit(f'preparo desconhecido no ofício {oficio}: "{qual}" (os que existem: {", ".join(tab)})')
    c = None if cat is None else cat_i(cat); de, chave = tab[qual]; alcance = 'nada' if c is None else f'até o {T.CATS[c]}'
    if de == 'pessoa':
        p = _vivo(E, pid); txt = f"{p['nome']} ganha o preparo: {qual} ({alcance})" + (f': {como}' if como else '')
        if not estado.aplica(E, 'mestre', [['pessoa', pid, 'marca.' + chave, 'poe', c]], onde=p['lugar'], quem=[pid], texto=txt): return f"{p['nome']} já tinha esse preparo: nada mudou."
    else:
        lid = lid or _vivo(E, pid)['lugar']; l = E['lugares'].get(lid) or sys.exit(f'não há o lugar "{lid}"')
        txt = f"{l['nome']} ganha o preparo: {qual} ({alcance})" + (f': {como}' if como else '')
        if not estado.aplica(E, 'mestre', [['lugar', lid, 'preparo.' + chave, 'poe', c]], onde=lid, texto=txt): return f"{l['nome']} já tinha esse preparo: nada mudou."
    return txt + '.'


def poe_oficina(E, lid, nivel, como=''):
    """o Mestre registra a oficina de um lugar (0 a 4), ou tira (None)"""
    l = E['lugares'].get(lid) or sys.exit(f'não há o lugar "{lid}"')
    if nivel is not None and not 0 <= nivel < len(O.OFICINAS): sys.exit(f'a oficina vai de 0 ({O.OFICINAS[0]}) a {len(O.OFICINAS) - 1} ({O.OFICINAS[-1]}); veio {nivel}')
    txt = f"{l['nome']} " + ('fica sem oficina' if nivel is None else f'tem agora uma {nome_oficina(nivel)}') + (f': {como}' if como else '')
    if not estado.aplica(E, 'mestre', [['lugar', lid, 'oficina', 'poe', nivel]], onde=lid, texto=txt): return f"{l['nome']} já estava assim: nada mudou."
    return txt + '.'


# ---------- a virada do dia ----------
def virada(E):
    """o dia virou: a obra sem dono vivo se desfaz. (A regra da morte, no estado.py, já desfaz as obras de quem morre, na hora: a matéria que estava nelas se perde,
    e o núcleo cai solto com o resto do que era dele. Isto aqui é só a rede: a obra que ficou órfã por outro caminho.)"""
    for oid, o in list(E['itens'].get('obras', {}).items()):
        q = E['gente'].get(o.get('quem'))
        if q and q['estado'] == 'vivo': continue
        estado.aplica(E, evento_de(o.get('oficio', 'forja'), o.get('tipo')), [['obra', oid, 'fecha']], onde=o.get('lugar'), quem=[o['quem']] if q else [],
                      texto=f"a obra {oid} se desfaz: {q['nome'] if q else 'quem a fazia'} morreu")


# ---------- a mesa ----------
def _diz_preparos(E, pid): return ' · '.join(f"{k}: {'não há' if v is None else 'até o ' + T.CATS[min(v, len(T.CATS) - 1)]}" for k, v in preparos(E, pid).items())


def ver(E, pid):
    """as linhas da oficina para esta pessoa: o lugar, a mão, o preparo, as obras, a matéria, o que dá para fazer e o que custa"""
    p = E['gente'][pid]; l = E['lugares'][p['lugar']]; v = oficina(E, p['lugar']); L = []; itens = E['itens']['itens']
    if estado.fora(E, pid): return [f"**{p['nome']} está fora, {_em(E, estado.fora(E, pid))}:** lá não há bancada."]
    L.append(f"**{l['nome']}:** " + ('não há oficina (não se forja, não se conserta, não se ajusta aqui).' if v is None else f"{nome_oficina(v)} · conserta, pago, até o {T.CATS[min(v + O.OFICINA_CONSERTA, len(T.CATS) - 1)]}"))
    maos = []
    for of in ('forja', 'couro'):
        if not (mao(p, of) or bancada(p, of)) and of != 'forja': continue
        prox = next((f'{T.MAESTRIAS[g]} aos {q}' + (f' e uma obra {FEM[O.FEITO_OBRA[g]]}' if g in O.FEITO_OBRA else '') for g, q in sorted(O.OFICIO_BLOCOS.items()) if g > mao(p, of)), 'o topo')
        maos.append(f"{of} {T.MAESTRIAS[mao(p, of)]} ({tantos(bancada(p, of), 'bloco')} de bancada; {prox})")
    L.append('Mão: ' + ' · '.join(maos)); L.append('Preparo (+2 cada, na obra que ele alcança): ' + _diz_preparos(E, pid))
    f = ferramentas(E, pid, 'forja'); vm, vt, fc = valor_ferramentas(E, pid, 'forja')
    lugar = lambda k, nome: (f"{f[k][0]} {_peca(f[k][1])}" + (' (o jogo: martelo e tenaz)' if (f[k][1].get('forma') or 'jogo') == 'jogo' else '') if f[k] else f"nenhum{'a' if k == 'tenaz' else ''} ({nome})")
    L.append(f"Ferramentas (somam na Lei do Valor): martelo de forja: {lugar('martelo', 'forjar ferramenta martelo CATEGORIA')}, +{vm} · tenaz: {lugar('tenaz', 'forjar ferramenta tenaz CATEGORIA')}, +{vt}" + (_diz_poder(fc) if fc is not None else ''))
    fx = efeitos_em_uso(E, pid, 'forja')
    if _diz_fx(fx): L.append(f"Os efeitos das ferramentas em uso (o mesmo efeito em duas vale o maior; o prumo soma, até {O.PRUMO_MAX}): " + _diz_fx(fx).split(': ', 1)[1])
    rc = (p.get('marca') or {}).get('receita')
    if rc: L.append('A sua receita (a ferramenta que nasce com efeitos escolhe por ela, na hora): ' + ' · '.join(f"{t}: {', '.join(v)}" for t, v in rc.items()))
    por_escolher = [(i, it) for i, it in itens.items() if it.get('dono') == pid and it.get('efeitos_livres')]
    for i, it in por_escolher[:4]:
        L.append(f"Efeitos por escolher em {i} {_peca(it)}: {it['efeitos_livres']}" + ((f" ({tantos(it['cheios_livres'], 'cheio')})" if it.get('cheios_livres') else '') + f" (`oficio.py efeito {i}` mostra o que cabe)" if escolhe_agora(it)
                 else ' (o catálogo de luta chega na próxima fase)' + (f", e {tantos(it['cheios_livres'], 'cheio')}" if it.get('cheios_livres') else '')))
    for oid, o in obras_de(E, pid).items():
        L.append(f"Obra aberta {oid}: {_nome_obra(E, o)}, {o['blocos']} de {o['pede']} blocos, {_em(E, o['lugar'])} (`oficio.py continua {oid}`)")
    mat = {k: n for k, n in p.get('carga', {}).items() if M.le_materia(k)[1] is not None}; nuc = [f"{i} {it['nome']} ({T.CATS[it['cat']]})" for i, it in itens.items() if it['tipo'] == 'nucleo' and it.get('dono') == pid]
    if mat or nuc: L.append('Matéria na carga: ' + (_lista(mat) if mat else 'nenhuma') + (' · núcleos: ' + ', '.join(nuc) if nuc else ''))
    if v is None: return L
    L += ['', '**Na bancada** (bloco pesado; `oficio.py pede ...` diz a matéria e a chance antes de abrir):',
          '- forjar (a LEI DO VALOR: a soma decide a categoria): escolhe-se a peça e a matéria que entra; os blocos vêm da matéria (' + ', '.join(f'{T.CATS[c]} {O.blocos(c)}' for c in range(M.MATERIA_ATE + 1))
          + f'); do {T.CATS[M.MATERIA_ATE + 1]} para cima, a matéria Rara e um núcleo (' + ', '.join(f'{T.CATS[c]} {O.blocos(c)}' for c in range(M.MATERIA_ATE + 1, O.FORJA_ATE + 1)) + ' blocos). '
          + 'A peça sai na maior categoria cuja CD a soma alcança (' + ' · '.join(f'{T.CATS[c]} {O.VALOR_CD[c]}' for c in range(len(O.VALOR_CD))) + f'), até o teto (sem núcleo, uma acima da matéria e nunca acima do {T.CATS[M.MATERIA_ATE]}); abaixo da CD do Comum, a matéria se perde. `oficio.py pede ...` diz a chance de cada categoria.']
    gastas = [(i, it) for i, it in itens.items() if it.get('dono') == pid and it['tipo'] in PECAS + O.PECAS_LADINO and it['dur'][0] < it['dur'][1]]
    for i, it in gastas[:4]:
        q = it['dur'][1] - it['dur'][0]; of = oficio_de(it); chave = _materia_conserto(it); pode = chave and it['cat'] < len(O.MAO_DA_OBRA) and mao(p, of) >= O.MAO_DA_OBRA[it['cat']]
        pb = conserto_bloco(E, pid, of); eu_txt = f"você, {tantos(math.ceil(q / pb), 'bloco')} e {math.ceil(q / O.CONSERTO_MATERIA)} de {_mat(chave)}" + (' (o remendo: 8 por bloco)' if pb != O.CONSERTO_BLOCO else '') if pode else 'você não tem a mão'
        pago = f"pago, {O.conserto_pago(it['cat'], q, M.peso_do_item(it))} de prata e {tantos(math.ceil(q / O.PAGO_BLOCO), 'bloco')} de espera" if it['cat'] <= v + O.OFICINA_CONSERTA else 'esta oficina não conserta'
        L.append(f"- consertar {it['nome']} ({i}, {it['dur'][0]}/{it['dur'][1]}): {eu_txt}; {pago}")
    if len(gastas) > 4: L.append(f"- ... e mais {tantos(len(gastas) - 4, 'peça gasta', 'peças gastas')}")
    L.append(f"- o conserto pago (`oficio.py consertar ITEM pago`): {100 * M.CONSERTO_PONTO:g}% do preço da peça por ponto, em prata inteira (arredonda para cima: um ponto de uma espada Comum custa {O.conserto_pago(0, 1)} de prata), "
             f"e um bloco de espera por peça (a cada {O.PAGO_BLOCO} pontos ou parte): mandar consertar quatro peças leva quatro blocos")
    g = O.ajuste_grau(mao(p))
    L.append('- ajustar (sob medida): ' + (f'grau {g}; de {O.ajuste_blocos(0)} (Comum) a {O.ajuste_blocos(O.FORJA_ATE)} blocos ({T.CATS[O.FORJA_ATE]}) e um teste contra {O.AJUSTE_BASE} + {O.TESTE_CAT} por categoria' if g else f'pede mão de {T.MAESTRIAS[2]}'))
    L.append(f"- jornal: {M.SALARIO[O.jornal_grau(mao(p), p.get('grau_oficio', 'diarista'))]} de prata por bloco de bancada a serviço da oficina (paga-se pelo que a mão vale: {O.jornal_grau(mao(p), p.get('grau_oficio', 'diarista'))}), até a jornada ({M.JORNADA} blocos pagos por dia; hoje: {ato.jornada(E, pid)}) (`oficio.py jornal N`)")
    return L


def mesa(E):
    """as linhas do ofício para a MESA.md"""
    pid = estado.eu(E)
    if not pid: return []
    if estado.fora(E, pid): return []                        # quem está no ermo não tem bancada à frente: a MESA não a mostra
    return ['## A oficina'] + ver(E, pid)


# ---------- a linha de comando ----------
def main(a=None):
    a = sys.argv[1:] if a is None else list(a)
    if not a: print(__doc__); return
    op = dict(x.split('=', 1) for x in a if '=' in x); pos = [x for x in a if '=' not in x]
    cmds = ('ver', 'pede', 'forjar', 'continua', 'larga', 'consertar', 'ajustar', 'jornal', 'preparo', 'oficina', 'efeito', 'receita')
    if not pos or pos[0] not in cmds: print(__doc__); return
    if pos[0] == 'jornal' and (len(pos) < 2 or not pos[1].isdigit() or int(pos[1]) < 1):       # uma frase por erro, em vez do uso inteiro
        sys.exit("diga quantos blocos de jornal, em número inteiro (1 ou mais): `python3 oficio.py jornal 2`" + (f' (veio "{pos[1]}")' if len(pos) > 1 else '') + '. Um bloco são 4 horas.')
    E = estado.carrega(); pid = op.get('quem') or estado.eu(E)
    if pid not in E['gente']: sys.exit(f'não há a pessoa "{pid}"')
    inteiro = lambda k: int(op[k]) if op.get(k, '').isdigit() else sys.exit(f'{k}= pede um número inteiro, de zero para cima (veio "{op[k]}")') if k in op else None
    def peca(i):
        tipo = pos[i] if len(pos) > i else sys.exit('diga o que forjar: arma FAMILIA CATEGORIA, armadura MATERIAL CATEGORIA, escudo CATEGORIA ou gazua CATEGORIA. Veja o uso: python3 oficio.py')
        if tipo in SEM_FAMILIA: fam = None; resto = pos[i + 1:]
        else: fam = pos[i + 1] if len(pos) > i + 1 else None; resto = pos[i + 2:]
        if tipo in FORJA and not resto: sys.exit('falta a categoria da peça. Veja o uso: python3 oficio.py')
        resto = resto or [0]
        return molde(tipo, resto[0], resto[1] if len(resto) > 1 else None, familia=fam if tipo == 'arma' else None, material=fam if tipo == 'armadura' else None,
                     cobre=op['cobre'].split(',') if op.get('cobre') else None, forma=fam if tipo == 'foco' else None, talhe=talhe_de(tipo), oficio=fam if tipo == 'ferramenta' else None)
    def talhe_de(tipo):
        """o talhe da armadura que se forja: o dito (talhe=miúdo), ou o do corpo de quem vai vesti-la (para=ID; etapa 4b)"""
        if 'para' not in op or tipo != 'armadura': return op.get('talhe')
        q = E['gente'].get(op['para']) or sys.exit(f'não há a pessoa "{op["para"]}" (para= diz para quem é a armadura)')
        c = estado.corpo_de(q); return None if c == 'gente' else c
    falta = lambda o_que, exemplo: sys.exit(f'{o_que}: `python3 oficio.py {exemplo}`')
    if pos[0] == 'ver': print('\n'.join(ver(E, pid))); return
    if pos[0] == 'pede': print(pede(E, pid, peca(1))); return
    if pos[0] == 'forjar': out = forjar(E, pid, peca(1), blocos=inteiro('blocos'), nucleo=op.get('nucleo'), molde=op.get('molde'))['texto']
    elif pos[0] == 'continua': out = continua(E, pid, pos[1] if len(pos) > 1 else None, blocos=inteiro('blocos'))['texto']
    elif pos[0] == 'larga': out = larga(E, pid, pos[1] if len(pos) > 1 else falta('diga qual obra largar (o id dela: `oficio.py ver` mostra)', 'larga o0001'))['texto']
    elif pos[0] == 'consertar': out = consertar(E, pid, pos[1] if len(pos) > 1 else falta('diga qual peça consertar (o id dela)', 'consertar i0007 pago'), pontos=inteiro('pontos'), pago='pago' in pos[2:])['texto']
    elif pos[0] == 'ajustar': out = ajustar(E, pid, pos[1] if len(pos) > 1 else falta('diga qual peça ajustar (o id dela)', 'ajustar i0007'), para=op.get('para'), blocos=inteiro('blocos'))['texto']
    elif pos[0] == 'jornal': out = jornal(E, pid, int(pos[1]), oficio=op.get('oficio', 'forja'))['texto']
    elif pos[0] == 'efeito':
        if len(pos) < 2: falta('diga a peça (e o efeito; sem efeito, a lista do que cabe)', 'efeito i0007 prumo cheio')
        resto = [x for x in pos[2:] if x not in ('cheio', 'emprestado')]
        if len(pos) < 3 or not resto: print(efeito(E, pid, pos[1])); return            # a lista do que cabe: só olha, não grava
        out = efeito(E, pid, pos[1], resto[0], cheio='cheio' in pos[2:], emprestado='emprestado' in pos[2:], valor=inteiro('valor'))
    elif pos[0] == 'receita':
        if len(pos) < 2: print(receita(E, pid)); return                                 # mostra as receitas: só olha
        out = receita(E, pid, pos[1], pos[2] if len(pos) > 2 else None)
    elif pos[0] == 'preparo':
        if len(pos) < 3: falta('diga qual preparo (receita, ajudante, fogo ou bigorna) e até que categoria ele serve (ou "nada")', 'preparo fogo Raro "como foi ganho"')
        out = ganha_preparo(E, pos[1], None if pos[2] == 'nada' else pos[2], pid=pid, como=pos[3] if len(pos) > 3 else '', oficio=op.get('oficio', 'forja'))
    else:                                                   # oficina
        if len(pos) < 2 or not (pos[1] == 'nada' or pos[1].isdigit()): falta(f'diga o nível da oficina, de 0 ({O.OFICINAS[0]}) a {len(O.OFICINAS) - 1} ({O.OFICINAS[-1]}), ou "nada"', 'oficina 1 "como foi"')
        out = poe_oficina(E, E['gente'][pid]['lugar'], None if pos[1] == 'nada' else int(pos[1]), como=pos[2] if len(pos) > 2 else '')
    estado.grava(E)                                         # grava ANTES de falar: a saída cortada não perde o que o dado rolou
    print(out)
    print(ato.ultima_linha(E, pid))


if __name__ == '__main__':
    import signal; hasattr(signal, 'SIGPIPE') and signal.signal(signal.SIGPIPE, signal.SIG_DFL)      # a saída cortada (`| head`) acaba o comando calada, sem erro de programa: tudo já foi gravado antes de falar
    main()
