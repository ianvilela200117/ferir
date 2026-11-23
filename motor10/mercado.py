#!/usr/bin/env python3
"""mercado.py — MOTOR 10: O MERCADO. O preço sai do estoque, e toda compra mexe nele, a do jogador também.
O lugar tem prata contada: loja sem prata não compra. Tudo por evento (`compra`, `venda`, `producao`, `consumo`); os números moram no tabelas_mercado.py.

  O PREÇO de um bem: base × √(alvo ÷ estoque), entre 0,4 e 3 vezes a base. O alvo são tantos dias de consumo do povo do lugar.
    Um lote é pago unidade a unidade (cada uma já mexe no preço da seguinte): o preço do lote é o mesmo de uma vez ou aos poucos. O troco, não:
    quem compra ou vende aos poucos paga o arredondamento a cada vez.
    Comprar custa 10% a mais. A loja paga 60% do preço, e 5 pontos a mais por grau de comércio de quem vende (até 80%).
    A prata é inteira: a compra arredonda para cima, a venda para baixo (a cesta de vários bens arredonda uma vez só). Comprar e vender de volta sempre perde.
  A PRATA NÃO NASCE NEM SOME: passa do bolso da pessoa (moedas) para o estoque do lugar (estoque.prata) e de volta. Loja sem prata recusa a compra.
  AS PEÇAS DA LOJA são itens do Livro de Itens com "onde" no lugar, sem dono e que não estão SOLTOS (caídos no chão), até o Épico. Valem o preço da categoria
    (30 a Comum, vezes 6 por categoria; a armadura, na proporção do que cobre: o elmo vale um quarto) menos o conserto que pedem (2% por ponto gasto);
    quebrada, a sucata (10%); sob medida, uma categoria abaixo.
    A loja pede o valor; paga a parte dela (60 a 80%), e 20% a menos por cada peça igual (tipo, família ou material, categoria) que já tem na prateleira.
    A peça que está EM USO não se vende: guarda-se antes (`ato.py tirar ITEM`).
  A VIRADA DO DIA, em cada lugar com povo: o lugar produz (tudo acompanha o preço: falta, produz mais; sobra, menos; e a colheita, além disso, segue a estação)
    e o povo consome. A prata não mexe.
  LUGAR SEM POVO (sem o campo `pop`) NÃO TEM MERCADO: ali não se compra, não se vende, e a virada não faz nada.
  Negociar não gasta bloco (como comer).

Uso (o personagem do jogador, ou quem=ID):
  python3 mercado.py ver                          os preços daqui, a prateleira, o que você carrega e quanto a loja paga
  python3 mercado.py preco BEM [N]                quanto custam N e quanto a loja paga por N, sem negociar nada
  python3 mercado.py comprar BEM N                compra N de um bem (comida, lenha, sal, metal:0, couro:1 ...)
  python3 mercado.py vender BEM N|tudo            vende N de um bem que você carrega
  python3 mercado.py vender tudo                  vende, num negócio só, tudo o que você carrega e a loja negocia (a prata arredonda uma vez)
  python3 mercado.py comprar ITEM                 compra uma peça da prateleira (o id dela no Livro de Itens: i0007)
  python3 mercado.py vender ITEM                  vende uma peça sua à loja
  python3 mercado.py funda POVO ["como foi"]      o Mestre abre um mercado onde a pessoa está: o povo, a produção, o estoque no alvo, a prateleira e a prata
BEM: comida lenha carvão sal pano remédio ferramenta · a matéria, com a categoria: metal:0 couro:1 osso:2 madeira:0 erva:1 (0 Comum, 1 Incomum, 2 Raro)
"""
import math, sys
import tabelas as T
import tabelas_mundo as M
import tabelas_mercado as C
import estado, corpo
from itens import item

PECAS = ('arma', 'armadura', 'escudo')
FEM = ['Comum', 'Incomum', 'Rara', 'Épica', 'Única', 'Lendária', 'Mítica', 'Primordial']       # a categoria, quando o nome que vem antes é feminino


# ---------- dizer ----------
def _n(x, casas=2): return f'{x:.{casas}f}'.replace('.', ',')           # 1,17
def _m(n): return f'{n:,}'.replace(',', '.') if isinstance(n, int) else _n(n, 1)        # 26.400
def _em(E, lid): l = E['lugares'][lid]; return l.get('em', 'em ' + l['nome'])


def nome_bem(bem):
    """o nome de um bem para a mesa: 'metal:1' → 'metal Incomum'; 'madeira:2' → 'madeira Rara'; 'comida' → 'comida'"""
    n, c = M.le_materia(bem)
    return bem if c is None or not 0 <= c < len(T.CATS) else f"{n} {(FEM if n.endswith('a') else T.CATS)[c]}"


# ---------- ler: o povo, o alvo, o preço ----------
def _vivo(E, pid): return estado.presente(E, pid, 'negociar na vila')        # vivo e no lugar onde mora: quem saiu para o ermo não compra nem vende


def povo(E, lid):
    """quanta gente o lugar tem (lugar.pop), ou 0: lugar sem povo não tem mercado"""
    v = E['lugares'][lid].get('pop')
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) and v > 0 else 0


def tem_mercado(E, lid): return povo(E, lid) > 0
def mao(p): m = p.get('maestria'); return m.get('comércio', 0) if isinstance(m, dict) else 0              # a maestria de comércio (0 a 8)
def parte(p): return C.parte(mao(p))                                                                       # a fração do preço que a loja paga a esta pessoa
def caixa(E, lid): return E['lugares'][lid]['estoque'].get('prata', 0)                                    # a prata do lugar
def prata_do_mundo(E): return sum(p['moedas'] for p in E['gente'].values()) + sum((l.get('estoque') or {}).get('prata', 0) for l in E['lugares'].values())      # gente mais lugares: a conta que tem de fechar


def _loja(E, lid):
    l = E['lugares'][lid]
    if not tem_mercado(E, lid): sys.exit(f"{l['nome']} não tem mercado (lugar sem povo contado): aqui não se compra nem se vende")
    return l


def _base(bem):
    b = C.base(bem)
    if b is None: sys.exit(f'a loja não negocia "{bem}" (negocia: {", ".join(C.BASE)}; e a matéria com a categoria, de 0 a {M.MATERIA_ATE}: {", ".join(n + ":0" for n in C.BASE_MATERIA)})')
    return b


def alvo(E, lid, bem):
    """o estoque que o lugar quer ter deste bem: tantos dias do consumo do povo dele"""
    return max(C.ALVO_MIN, C.alvo_dias(bem) * povo(E, lid) * C.consumo(bem))


def fator_de(alvo_, estoque):
    """√(alvo ÷ estoque), entre 0,4 e 3: quantas vezes a base o bem vale"""
    if estoque <= 0: return C.FATOR_MAX
    return max(C.FATOR_MIN, min(C.FATOR_MAX, math.sqrt(alvo_ / estoque)))


def fator(E, lid, bem): return fator_de(alvo(E, lid, bem), E['lugares'][lid]['estoque'].get(bem, 0))
def preco(E, lid, bem):
    """o preço do dia de UMA unidade (sem os 10% da compra nem o desconto da venda), ou None se a loja não negocia isto"""
    b = C.base(bem); return None if b is None else b * fator(E, lid, bem)


def refeicao(E, lid):
    """o que valeria UMA refeição servida no lugar, hoje: o preço do dia da comida, em prata inteira (a mais perto; nunca menos que 1). Lugar sem mercado: o preço fixo.
    NINGUÉM USA AINDA: o `ato.py comer` cobra o preço fixo (tabelas_mundo.REFEICAO_PRECO). Está aqui para o dia em que a taverna seguir o celeiro."""
    if not tem_mercado(E, lid): return M.REFEICAO_PRECO
    return max(1, math.floor(preco(E, lid, 'comida') + 0.5))


def lote(E, lid, bem, n, compra=True):
    """a soma dos preços de n unidades, uma a uma. Cada unidade vale o preço com o estoque no MEIO do passo dela: por isso a ida e a volta passam pelos mesmos preços."""
    b = C.base(bem); a = alvo(E, lid, bem); s = E['lugares'][lid]['estoque'].get(bem, 0); sinal = -1 if compra else 1
    return b * sum(fator_de(a, s + sinal * (k + 0.5)) for k in range(int(n)))


def custa(E, lid, bem, n):
    """quanta prata custa comprar n unidades aqui, agora (inteira, arredondada para cima)"""
    return max(1, math.ceil(round(C.COMPRA * lote(E, lid, bem, n, compra=True), 6)))


def paga(E, pid, bem, n, lid=None):
    """quanta prata a loja paga a esta pessoa por n unidades, agora (inteira, arredondada para baixo)"""
    p = E['gente'][pid]; return math.floor(round(parte(p) * lote(E, lid or p['lugar'], bem, n, compra=False), 6))


def cabe(E, pid, bem, lid=None):
    """quantas unidades deste bem a loja consegue pagar agora a esta pessoa (no máximo, o que ela carrega)"""
    p = E['gente'][pid]; lid = lid or p['lugar']; b = C.base(bem); tem = int(p.get('carga', {}).get(bem, 0))
    if b is None or not tem_mercado(E, lid): return 0
    a = alvo(E, lid, bem); s = E['lugares'][lid]['estoque'].get(bem, 0); pct = parte(p); cx = caixa(E, lid); soma = 0.0
    for k in range(tem):
        soma += b * fator_de(a, s + k + 0.5)
        if math.floor(round(pct * soma, 6)) > cx: return k
    return tem


# ---------- a maestria de comércio ----------
def _treino(E, pid, prata):
    """os efeitos de um negócio na mão de quem negocia: o dia de negócio (um por dia) e o feito (um negócio grande)"""
    p = E['gente'][pid]; m = p.get('marca', {}); ef = []
    if prata >= C.NEGOCIO_MIN and m.get('negocio_dia') != E['relogio']['dia']:
        ef += [['pessoa', pid, 'treino.comércio', 'soma', 1], ['pessoa', pid, 'marca.negocio_dia', 'poe', E['relogio']['dia']]]
    for grau, quer in sorted(C.FEITO_NEGOCIO.items()):
        if prata >= quer and m.get('feito_comércio', 0) < grau: ef.append(['pessoa', pid, 'marca.feito_comércio', 'poe', grau])
    return ef


def sobe(E, pid):
    """a maestria de comércio sobe quando os dias de negócio chegam; de Mestre para cima, só com o FEITO (um negócio grande)"""
    p = E['gente'][pid]; tem = mao(p); dias = (p.get('treino') or {}).get('comércio', 0); txt = ''
    for grau, quer in sorted(C.COMERCIO_DIAS.items()):
        if grau <= tem or dias < quer: continue
        if grau in C.FEITO_NEGOCIO and p.get('marca', {}).get('feito_comércio', 0) < grau:
            txt = f" (tem os dias para {T.MAESTRIAS[grau]} em comércio; falta o feito: um negócio só de {_m(C.FEITO_NEGOCIO[grau])} de prata ou mais)"; break
        estado.aplica(E, 'treinar', [['pessoa', pid, 'maestria.comércio', 'poe', grau]], onde=p['lugar'], quem=[pid], texto=f"{p['nome']} chega a {T.MAESTRIAS[grau]} em comércio")
        p = E['gente'][pid]; tem = grau; txt = f'. MAESTRIA: {T.MAESTRIAS[grau]} em comércio'
    return txt


# ---------- comprar e vender um bem ----------
def _quantos(n):
    try: q = int(str(n).strip())
    except ValueError: q = 0
    if q < 1: sys.exit(f'diga quantas unidades, em número inteiro (1 ou mais); veio "{n}"')
    return q


def comprar(E, pid, bem, n):
    """a pessoa compra n unidades de um bem da loja do lugar onde está: a prata vai para o lugar, o bem sai do estoque e entra na carga"""
    p = _vivo(E, pid); lid = p['lugar']; l = _loja(E, lid); _base(bem); n = _quantos(n); tem = l['estoque'].get(bem, 0)
    if tem < n: sys.exit(f"{l['nome']} só tem {_m(tem)} de {nome_bem(bem)} (pediu {_m(n)})")
    prata = custa(E, lid, bem, n); antes = preco(E, lid, bem)
    if p['moedas'] < prata: sys.exit(f"{_m(n)} de {nome_bem(bem)} custam {_m(prata)} de prata {_em(E, lid)}; {p['nome']} tem {_m(p['moedas'])}")
    ef = [['pessoa', pid, 'moedas', 'soma', -prata], ['estoque', lid, 'prata', 'soma', prata], ['estoque', lid, bem, 'soma', -n], ['pessoa', pid, 'carga.' + bem, 'soma', n]] + _treino(E, pid, prata)
    txt = f"{p['nome']} compra {_m(n)} de {nome_bem(bem)} por {_m(prata)} de prata {_em(E, lid)}"
    estado.aplica(E, 'compra', ef, onde=lid, quem=[pid], texto=txt); depois = preco(E, lid, bem)
    return dict(bem=bem, n=n, prata=prata, antes=antes, depois=depois, texto=f"{txt}. O preço do dia: {_n(antes)} → {_n(depois)}" + (sobe(E, pid) or '.'))


def vender(E, pid, bem, n):
    """a pessoa vende à loja n unidades de um bem que carrega (ou 'tudo'): o bem entra no estoque, a prata sai do lugar. Loja sem prata recusa."""
    p = _vivo(E, pid); lid = p['lugar']; l = _loja(E, lid); _base(bem); tem = p.get('carga', {}).get(bem, 0)
    if n == 'tudo': n = int(tem) or sys.exit(f"{p['nome']} não carrega {nome_bem(bem)}")
    n = _quantos(n)
    if tem < n: sys.exit(f"{p['nome']} carrega {_m(tem)} de {nome_bem(bem)} (quis vender {_m(n)})")
    prata = paga(E, pid, bem, n); antes = preco(E, lid, bem); cx = caixa(E, lid)
    if prata < 1: sys.exit(f"{_m(n)} de {nome_bem(bem)} não valem uma moeda de prata {_em(E, lid)}: junte mais para vender")
    if cx < prata:
        k = cabe(E, pid, bem); sys.exit(f"a loja de {l['nome']} tem {_m(cx)} de prata e não paga {_m(prata)} por {_m(n)} de {nome_bem(bem)}" + (f': hoje ela compra até {_m(k)}' if k and paga(E, pid, bem, k) >= 1 else ': hoje ela não compra'))
    ef = [['estoque', lid, 'prata', 'soma', -prata], ['pessoa', pid, 'moedas', 'soma', prata], ['pessoa', pid, 'carga.' + bem, 'soma', -n], ['estoque', lid, bem, 'soma', n]] + _treino(E, pid, prata)
    txt = f"{p['nome']} vende {_m(n)} de {nome_bem(bem)} por {_m(prata)} de prata {_em(E, lid)}"
    estado.aplica(E, 'venda', ef, onde=lid, quem=[pid], texto=txt); depois = preco(E, lid, bem)
    return dict(bem=bem, n=n, prata=prata, antes=antes, depois=depois, texto=f"{txt}. O preço do dia: {_n(antes)} → {_n(depois)}" + (sobe(E, pid) or '.'))


def vender_cesta(E, pid, cesta=None):
    """a pessoa vende vários bens num negócio só ({bem: quanto}; sem cesta: tudo o que carrega e a loja negocia). A prata é arredondada UMA vez, na soma:
    quem junta a venda do dia perde menos no troco. Loja sem prata para a cesta inteira recusa a cesta inteira."""
    p = _vivo(E, pid); lid = p['lugar']; l = _loja(E, lid); carga = p.get('carga', {})
    if cesta is None: cesta = {b: int(q) for b, q in carga.items() if C.base(b) is not None and q >= 1}
    if not cesta: sys.exit(f"{p['nome']} não carrega nada que a loja negocie")
    cesta = {b: _quantos(q) for b, q in cesta.items()}
    for b, q in cesta.items():
        _base(b)
        if carga.get(b, 0) < q: sys.exit(f"{p['nome']} carrega {_m(carga.get(b, 0))} de {nome_bem(b)} (quis vender {_m(q)})")
    prata = math.floor(round(parte(p) * sum(lote(E, lid, b, q, compra=False) for b, q in cesta.items()), 6)); cx = caixa(E, lid); lista = ', '.join(f'{_m(q)} de {nome_bem(b)}' for b, q in cesta.items())
    if prata < 1: sys.exit(f"{lista}: isso não vale uma moeda de prata {_em(E, lid)}: junte mais para vender")
    if cx < prata: sys.exit(f"a loja de {l['nome']} tem {_m(cx)} de prata e não paga {_m(prata)} pela cesta ({lista}): venda aos poucos (`mercado.py preco BEM N` diz quanto ela paga)")
    ef = [['estoque', lid, 'prata', 'soma', -prata], ['pessoa', pid, 'moedas', 'soma', prata]]
    for b, q in cesta.items(): ef += [['pessoa', pid, 'carga.' + b, 'soma', -q], ['estoque', lid, b, 'soma', q]]
    txt = f"{p['nome']} vende {lista} por {_m(prata)} de prata {_em(E, lid)}"
    estado.aplica(E, 'venda', ef + _treino(E, pid, prata), onde=lid, quem=[pid], texto=txt)
    return dict(cesta=cesta, prata=prata, texto=txt + (sobe(E, pid) or '.'))


# ---------- as peças da loja ----------
def valor(it):
    """o valor de uma peça do Livro de Itens (antes de arredondar): a categoria, menos o desgaste; quebrada, a sucata; sob medida, uma categoria abaixo"""
    return C.valor_peca(it['cat'], it['dur'][0], it['dur'][1], sob_medida=bool(it.get('sob_medida')), peso=M.peso_da_peca(it['tipo'], it.get('cobre')))


def preco_peca(it): return max(1, math.ceil(round(valor(it), 6)))                                         # o que a loja pede por ela
def _e_peca(it): return it.get('tipo') in PECAS and it['cat'] <= M.PECA_LOJA_ATE
def _feitio(it): return (it['tipo'], it['cat'], it.get('familia'), it.get('material'))      # o que faz duas peças serem "iguais" para a loja (o recorte da armadura não conta)


def prateleira(E, lid):
    """{id: item} das peças da loja deste lugar: no Livro de Itens, com "onde" aqui, sem dono, até o Épico. O que está SOLTO (caído no chão: de quem morreu ali) não é da loja."""
    return {i: it for i, it in E['itens']['itens'].items() if it.get('onde') == lid and not it.get('dono') and not it.get('solto') and _e_peca(it)}


def iguais(E, lid, it):
    """quantas peças iguais a esta (tipo, família ou material, categoria) a loja do lugar já tem na prateleira"""
    return sum(1 for i, x in prateleira(E, lid).items() if i != it.get('id') and _feitio(x) == _feitio(it))


def paga_peca(E, pid, it, lid=None):
    """o que a loja paga por esta peça a esta pessoa: a parte dela no valor, e 20% a menos por cada peça igual que a prateleira já tem"""
    p = E['gente'][pid]; return math.floor(round(parte(p) * valor(it) * C.FARTA ** iguais(E, lid or p['lugar'], it), 6))


def _diz_peca(it): return f"{it['nome']} ({T.CATS[it['cat']]}, {it['dur'][0]}/{it['dur'][1]}" + (', QUEBRADA' if it['dur'][0] <= 0 else '') + (f", sob medida para {it['sob_medida'].get('dono')}" if it.get('sob_medida') else '') + ')'


def comprar_peca(E, pid, iid):
    """a pessoa compra uma peça da prateleira do lugar onde está: a prata vai para o lugar e o dono entra no Livro de Itens"""
    p = _vivo(E, pid); lid = p['lugar']; l = _loja(E, lid); it = E['itens']['itens'].get(iid) or sys.exit(f'não há o item "{iid}" no Livro de Itens')
    if iid not in prateleira(E, lid):
        sys.exit(f"{it['nome']} ({iid}) não está na prateleira de {l['nome']}" + (f": é de {E['gente'][it['dono']]['nome']}" if it.get('dono') in E['gente']
                 else ': está caída no chão, não é da loja (quem fica com ela entra por evento do Mestre)' if it.get('onde') == lid and it.get('solto')
                 else f": a loja só negocia arma, armadura e escudo, até o {T.CATS[M.PECA_LOJA_ATE]}" if it.get('onde') == lid else ''))
    prata = preco_peca(it)
    if p['moedas'] < prata: sys.exit(f"{_diz_peca(it)} custa {_m(prata)} de prata; {p['nome']} tem {_m(p['moedas'])}")
    ef = [['pessoa', pid, 'moedas', 'soma', -prata], ['estoque', lid, 'prata', 'soma', prata], ['item', iid, 'dono', 'poe', pid],
          ['item', iid, 'historia', 'junta', f"Dia {E['relogio']['dia']}: comprada por {p['nome']} {_em(E, lid)}, por {_m(prata)} de prata"]] + _treino(E, pid, prata)
    txt = f"{p['nome']} compra {_diz_peca(it)} por {_m(prata)} de prata {_em(E, lid)}"
    estado.aplica(E, 'compra', ef, onde=lid, quem=[pid], texto=txt)
    return dict(item=iid, prata=prata, texto=txt + (sobe(E, pid) or '.'))


def vender_peca(E, pid, iid):
    """a pessoa vende à loja uma peça sua: a peça fica sem dono, com "onde" no lugar (vai para a prateleira), e a prata sai do lugar. Loja sem prata recusa."""
    p = _vivo(E, pid); lid = p['lugar']; l = _loja(E, lid); it = E['itens']['itens'].get(iid) or sys.exit(f'não há o item "{iid}" no Livro de Itens')
    if it.get('dono') != pid: sys.exit(f"{it['nome']} ({iid}) não é de {p['nome']}")
    if it.get('tipo') not in PECAS: sys.exit(f"{it['nome']} não é peça que a loja negocie (núcleo não se vende em loja: é coisa de leilão ou de encomenda)")
    if it['cat'] > M.PECA_LOJA_ATE: sys.exit(f"{it['nome']} é {T.CATS[it['cat']]}: a loja só negocia peça até o {T.CATS[M.PECA_LOJA_ATE]} (daí para cima, leilão ou encomenda)")
    if any(o.get('item') == iid for o in E['itens'].get('obras', {}).values()): sys.exit(f"{it['nome']} está num ajuste aberto: feche ou largue a obra antes de vender")
    if it.get('uso'): sys.exit(f"{it['nome']} está em uso: guarde antes de vender (`ato.py tirar {iid}`)")
    prata = paga_peca(E, pid, it); cx = caixa(E, lid); k = iguais(E, lid, it)
    if prata < 1: sys.exit(f"{_diz_peca(it)} não vale uma moeda de prata {_em(E, lid)}" + (f': a loja já tem {k} igual(is) na prateleira' if k else ''))
    if cx < prata: sys.exit(f"a loja de {l['nome']} tem {_m(cx)} de prata e não paga {_m(prata)} por {_diz_peca(it)}")
    ef = [['estoque', lid, 'prata', 'soma', -prata], ['pessoa', pid, 'moedas', 'soma', prata], ['item', iid, 'dono', 'poe', None], ['item', iid, 'onde', 'poe', lid],
          ['item', iid, 'historia', 'junta', f"Dia {E['relogio']['dia']}: vendida por {p['nome']} à loja de {l['nome']}, por {_m(prata)} de prata"]] + _treino(E, pid, prata)
    txt = f"{p['nome']} vende {_diz_peca(it)} por {_m(prata)} de prata {_em(E, lid)}"
    estado.aplica(E, 'venda', ef, onde=lid, quem=[pid], texto=txt)
    return dict(item=iid, prata=prata, iguais=k, texto=txt + (f' (a loja já tinha {k} igual(is): pagou menos)' if k and C.FARTA < 1 else '') + (sobe(E, pid) or '.'))


# ---------- a virada do dia ----------
def _inteiro(E, x, chave):
    """x em unidades inteiras: a parte quebrada vira a chance de mais uma (o acaso do mundo: mesma semente, mesmo mundo)"""
    n = math.floor(x); resto = x - n
    return n + (1 if resto > 1e-9 and estado.sorte(E, chave).random() < resto else 0)


def virada(E):
    """o dia virou: em cada lugar com povo, o lugar produz (tudo acompanha o preço; a colheita, além disso, segue a estação do dia que acabou) e o povo consome.
    A prata não mexe. Lugar sem povo: nada acontece."""
    ontem = max(1, E['relogio']['dia'] - 1); est = ((ontem - 1) % M.ANO) // M.ESTACAO
    for lid in list(E['lugares']):
        pop = povo(E, lid)
        if not pop: continue
        l = E['lugares'][lid]; ef = []
        for bem, q in (l.get('produz') if isinstance(l.get('produz'), dict) else {}).items():
            if bem == 'prata' or not isinstance(q, (int, float)) or isinstance(q, bool) or q <= 0: continue        # prata não se produz: só nasce em evento "gera" ou "mestre"
            vezes = 1 if C.base(bem) is None else max(C.RESPOSTA[0], min(C.RESPOSTA[1], fator(E, lid, bem)))       # a produção acompanha o preço: falta, produz mais; sobra, menos
            if bem in C.SAFRA: vezes *= M.COLHEITA[est]                                                             # ... e a colheita, além disso, segue a estação
            n = _inteiro(E, q * vezes, f'mercado|{lid}|{bem}|produz')
            if n: ef.append(['estoque', lid, bem, 'soma', n])
        if ef: estado.aplica(E, 'producao', ef, onde=lid)
        l = E['lugares'][lid]; ef = []
        for bem, tem in l['estoque'].items():
            c = C.consumo(bem)
            if bem == 'prata' or not c or tem <= 0: continue
            n = min(tem, _inteiro(E, pop * c * C.CONSUMO_ESTACAO.get(bem, [1] * len(M.ESTACOES))[est], f'mercado|{lid}|{bem}|consome'))
            if n: ef.append(['estoque', lid, bem, 'soma', -n])
        if ef: estado.aplica(E, 'consumo', ef, onde=lid)


# ---------- o gerador: abrir um mercado ----------
def funda(E, lid, pop, prata=None, prateleira_=True, como=''):
    """o gerador (ou o Mestre) abre um mercado EQUILIBRADO num lugar, por um evento "gera": o povo; a produção (o que esse povo consome: preço de equilíbrio na base);
    o estoque no alvo (a comida, no ponto do ano em que o mundo está); a prateleira do tipo do lugar; e a prata (se o lugar não tem nenhuma: 5 por pessoa).
    `prata`: a prata que o lugar passa a ter (None: fica a que tem; sem nenhuma, a de tabela)."""
    l = E['lugares'].get(lid) or sys.exit(f'não há o lugar "{lid}"')
    if not isinstance(pop, (int, float)) or isinstance(pop, bool) or pop < 1: sys.exit(f'o povo de um mercado é 1 ou mais (veio {pop})')
    if tem_mercado(E, lid): sys.exit(f"{l['nome']} já tem mercado ({_m(povo(E, lid))} de povo): não se abre outro por cima")
    ef = [['lugar', lid, 'pop', 'poe', pop]]
    for bem in C.bens():
        c = pop * C.consumo(bem); _, cat = M.le_materia(bem); feito = cat is None or cat <= C.PRODUZ_ATE
        if not feito: continue                                                                             # o que o povo não tira (a matéria Rara) fica como está: nem produção, nem estoque posto
        ef.append(['lugar', lid, 'produz.' + bem, 'poe', round(c, 4)])
        quer = round((C.celeiro_dias(E['relogio']['dia']) if bem in C.SAFRA else C.alvo_dias(bem)) * c)
        if quer != l['estoque'].get(bem, 0): ef.append(['estoque', lid, bem, 'soma', quer - l['estoque'].get(bem, 0)])
    tem = l['estoque'].get('prata', 0); quer = tem or round(pop * C.PRATA_CABECA) if prata is None else prata
    if quer != tem: ef.append(['estoque', lid, 'prata', 'soma', quer - tem])
    if prateleira_:
        for tipo, qual, cat, cobre in C.PRATELEIRA.get(l.get('tipo'), C.PRATELEIRA['vila']):
            ef.append(['item', 'nasce', item(tipo, cat, familia=qual if tipo == 'arma' else None, material=qual if tipo == 'armadura' else None, cobre=cobre, onde=lid)])
    txt = f"{l['nome']} abre o mercado: {_m(pop)} de povo, {_m(quer)} de prata" + (f': {como}' if como else '')
    estado.aplica(E, 'gera', ef, onde=lid, texto=txt)
    return txt + '.'


# ---------- a mesa ----------
def _linha_bem(E, pid, lid, bem):
    p = E['gente'][pid]; tem = E['lugares'][lid]['estoque'].get(bem, 0); b = C.base(bem); un = 1 if b >= 5 else 10; carrega = p.get('carga', {}).get(bem, 0)
    k = min(un, int(tem)); compra = f'{k} por {_m(custa(E, lid, bem, k))}' if k else 'não há'
    q = paga(E, pid, bem, un); return f"| {nome_bem(bem)} | {_m(tem)} | {_n(preco(E, lid, bem))} (× {_n(fator(E, lid, bem))}) | {compra} | {_m(q)} por {un} | {_m(carrega) if carrega else ''} |"


def ver(E, pid):
    """as linhas do mercado para esta pessoa: os preços do lugar ONDE ELA ESTÁ, a prateleira, o que ela carrega e o que a loja paga"""
    p = E['gente'][pid]; lid = p['lugar']; l = E['lugares'][lid]; pop = povo(E, lid)
    if estado.fora(E, pid): return [f"**{p['nome']} está fora, {_em(E, estado.fora(E, pid))}:** lá não há mercado. Vende-se o despojo na volta."]
    if not pop: return [f"**{l['nome']}:** não há mercado aqui (lugar sem povo contado: não se compra nem se vende)."]
    carga = p.get('carga', {}); itens = E['itens']['itens']
    L = [f"**{l['nome']}** · {_m(pop)} de povo · a loja tem {_m(caixa(E, lid))} de prata (sem prata, ela não compra) · comprar custa {C.COMPRA - 1:.0%} a mais · "
         f"a loja paga {parte(p):.0%} do preço (a sua mão em comércio: {T.MAESTRIAS.get(mao(p), mao(p))})"]
    tem = [b for b in C.bens() if l['estoque'].get(b, 0) > 0 or carga.get(b, 0) > 0]; falta = [nome_bem(b) for b in C.bens() if b not in tem and C.consumo(b) and M.le_materia(b)[1] in (None, 0)]
    if tem: L += ['', '| bem | no lugar | preço do dia (× a base) | comprar | a loja paga | você carrega |', '| --- | --- | --- | --- | --- | --- |'] + [_linha_bem(E, pid, lid, b) for b in tem]
    if falta: L.append(f"Em falta aqui (preço no teto, × {C.FATOR_MAX:g}): {', '.join(falta)}.")
    outros = [f'{_m(q)} de {b}' for b, q in carga.items() if C.base(b) is None]
    if outros: L.append('A loja não negocia: ' + ', '.join(outros) + '.')
    loja = prateleira(E, lid)
    if loja:
        L += ['', '**A prateleira** (peças do Livro de Itens; o preço é o de tabela, menos o desgaste):']; novas = {}; outras = []
        for i, it in loja.items():
            if it['dur'][0] == it['dur'][1] and not it.get('sob_medida'): novas.setdefault((it['cat'], preco_peca(it)), []).append(f"{i} {it['nome']}")
            else: outras.append(f"- {i} {_diz_peca(it)}: {_m(preco_peca(it))} de prata")
        L += [f"- novas, a {_m(pr)} de prata cada ({T.CATS[cat]}): " + ' · '.join(v[:14]) + (f' · e mais {len(v) - 14}' if len(v) > 14 else '') for (cat, pr), v in sorted(novas.items())]
        L += outras[:8] + ([f'- ... e mais {len(outras) - 8} peça(s) gasta(s)'] if len(outras) > 8 else [])
    minhas = [(i, it) for i, it in itens.items() if it.get('dono') == pid and _e_peca(it)]
    if minhas: L += ['', f'**As suas peças** (o que a loja paga; {1 - C.FARTA:.0%} a menos por peça igual que ela já tem; a que está em uso não se vende sem guardar): '
                     + ' · '.join(f"{i} {_diz_peca(it)}{' EM USO' if it.get('uso') else ''}: {_m(paga_peca(E, pid, it))}" for i, it in minhas[:8]) + (f' · e mais {len(minhas) - 8}' if len(minhas) > 8 else '')]
    L += ['', 'Negociar não gasta bloco: `mercado.py comprar BEM N` · `mercado.py vender BEM N|tudo` · `mercado.py vender tudo` (a cesta: um troco só) · `mercado.py comprar ITEM` · `mercado.py vender ITEM` · `mercado.py preco BEM N` (só olha)']
    return L


def mesa(E):
    """as linhas do mercado para a MESA.md: os preços do lugar onde o personagem está"""
    pid = estado.eu(E)
    if not pid: return []
    if estado.fora(E, pid): return []                        # quem está no ermo não tem mercado à frente: a MESA não o mostra
    return ['## O mercado'] + ver(E, pid)


def diz_preco(E, pid, bem, n=1):
    """quanto custam n e quanto a loja paga por n, aqui e agora, sem negociar nada"""
    p = _vivo(E, pid); lid = p['lugar']; l = _loja(E, lid); b = _base(bem); n = _quantos(n); tem = l['estoque'].get(bem, 0); k = min(n, int(tem))
    L = [f"{nome_bem(bem)} {_em(E, lid)}: base {_n(b)} · preço do dia {_n(preco(E, lid, bem))} (× {_n(fator(E, lid, bem))}) · no lugar {_m(tem)} (o alvo: {_m(round(alvo(E, lid, bem)))})"]
    L.append(f"Comprar {_m(k)}: {_m(custa(E, lid, bem, k))} de prata" + (f' (o lugar só tem {_m(tem)})' if k < n else '') if k else 'Comprar: não há no lugar.')
    q = paga(E, pid, bem, n); L.append(f"Vender {_m(n)}: a loja paga {_m(q)} de prata ({parte(p):.0%} do preço)" + (f"; ela tem {_m(caixa(E, lid))}" if caixa(E, lid) < q else '') + (f"; você carrega {_m(p.get('carga', {}).get(bem, 0))}" if p.get('carga', {}).get(bem, 0) < n else ''))
    return '\n'.join(L)


# ---------- a linha de comando ----------
def main(a=None):
    a = sys.argv[1:] if a is None else list(a)
    if not a: print(__doc__); return
    op = dict(x.split('=', 1) for x in a if '=' in x); pos = [x for x in a if '=' not in x]
    if not pos or pos[0] not in ('ver', 'preco', 'comprar', 'vender', 'funda') or (pos[0] != 'ver' and len(pos) < 2): print(__doc__); return
    E = estado.carrega(); pid = op.get('quem') or estado.eu(E)
    if pid not in E['gente']: sys.exit(f'não há a pessoa "{pid}"')
    if pos[0] == 'ver': print('\n'.join(ver(E, pid))); return
    if pos[0] == 'preco': print(diz_preco(E, pid, pos[1], pos[2] if len(pos) > 2 else 1)); return
    e_item = pos[1] in E['itens']['itens']
    if pos[0] == 'vender' and pos[1:] == ['tudo']: out = vender_cesta(E, pid)['texto']
    elif pos[0] == 'comprar' and e_item: out = comprar_peca(E, pid, pos[1])['texto']
    elif pos[0] == 'vender' and e_item: out = vender_peca(E, pid, pos[1])['texto']
    elif pos[0] == 'comprar' and len(pos) > 2: out = comprar(E, pid, pos[1], pos[2])['texto']
    elif pos[0] == 'vender' and len(pos) > 2: out = vender(E, pid, pos[1], pos[2])['texto']
    elif pos[0] == 'funda' and pos[1].isdigit(): out = funda(E, E['gente'][pid]['lugar'], int(pos[1]), como=pos[2] if len(pos) > 2 else '')
    elif pos[0] in ('comprar', 'vender'): sys.exit(f'diga quantas unidades de "{pos[1]}" (ou o id de uma peça do Livro de Itens: i0007). Veja o uso: python3 mercado.py')
    else: print(__doc__); return
    estado.grava(E); p = E['gente'][pid]                    # grava ANTES de falar
    print(out)
    print(f"{estado.quando(E)} · PV {p['pv']}/{estado.pv_max(p)} · {corpo.diz(p)} · {_m(p['moedas'])} de prata")


if __name__ == '__main__':
    main()
