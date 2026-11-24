#!/usr/bin/env python3
"""manha.py, MOTOR 10, ETAPA 4b: O LADINO (capítulo 18; os números no tabelas_manha.py; o contrato: projeto/ETAPA_4B.md, seção 12).

  A MANHA é o 17º caminho, o ofício do ladino: andar escondido, escutar, achar e desarmar armadilha, abrir fechadura (e o furto, que fica escrito para a etapa 3).
  Um caminho só para tudo isso, porque é uma mão só. Sobe por blocos como as armas (40, 160, 500, 1.500, vezes o talento); de Mestre para cima pede um FEITO:
  abrir uma fechadura ou desarmar uma armadilha Rara de verdade (o Lendário, uma Épica), não no treino.
  TODO TESTE DO LADINO é o dado do jogador (teste.rola: declarado e rolado uma vez): 2d20 + o atributo ÷ 10 + a mão de manha (Iniciante +2 ... Lendário +8)
  + o dom escondido ("a mão leve") + o +2 do povo (com teto), contra um número. A GAZUA É A ARMA, A FECHADURA É A ARMADURA: abrir e desarmar contam
  24 + 8 × (a categoria da fechadura − a da gazua); sem gazua, um degrau abaixo do Comum. Achar é o olho: 20 + 6 por categoria. Arrombar é a Força e a arma de impacto
  em uso (a mão não soma). Falhar por 5 ou mais entorta a gazua (ou gasta a arma de arrombar), e dispara a armadilha em quem desarmava.
  COMO SE APRENDE: na masmorra, cada bloco que fecha lá dentro em que a pessoa andou escondida, escutou, procurou, abriu ou desarmou soma 1 bloco de treino
  (no máximo 1 por bloco: quem conta é a masmorra, pelo `treino`); em casa, `manha.py treinar N`, com uma gazua (a fechadura velha, o passo macio no pátio): bloco pesado.
  O FURTO fica escrito (tabelas_manha.FURTO) e entra na etapa 3, com a gente que lembra e a vila com justiça: hoje o comando recusa.

Uso em código (o que as outras frentes chamam; nenhuma grava sozinha, a não ser na_vila, treinar, sobe e o main: devolvem efeitos, e quem chama os põe no evento dele):
  grau(p) · gazua_de(E, pid) · contra(E, pid, teste, cat) · testa(E, pid, teste, contra=None, cat=None, o_que=None, oculto=False, mais=0, pedra=False)
  mais_barulhento(E, ids, luz=False) · treino(E, pid, blocos=1) · feito(E, pid, cat) · na_vila(E, vila='vila') · voce(E) · so_mestre(E)
  e mais: gasta(r) (o desgaste da ferramenta depois de um teste) · chance(E, pid, teste, ...) (a conta exata, sem rolar) · contra_escutar(material, mortos)
  · sobe(E, pid) (a mão que sobe, gravada) · treinar(E, pid, blocos) (o treino em casa, gravado) · ver(E, pid) (as linhas da mesa do ladino)
Uso de linha de comando (o personagem do jogador, ou quem=ID):
  python3 manha.py ver [ID]                  a mão do ladino: o grau, os blocos, o feito, a gazua, e a chance de cada teste hoje (só olha)
  python3 manha.py chance TESTE CATEGORIA    (só olha) a chance de achar, abrir (gazua), desarmar ou arrombar contra a categoria, com a ferramenta que você leva
  python3 manha.py treinar N                 N blocos de treino em casa, com uma gazua (bloco pesado; a mão sobe quando os blocos chegam)
  python3 manha.py furtar ALVO               o furto fica escrito para a etapa 3: hoje recusa
TESTE: achar gazua desarmar arrombar · CATEGORIA: Comum Incomum Raro Épico Único Lendário (ou 0 a 7)
"""
import sys
import tabelas as T
import tabelas_mundo as M
import tabelas_manha as TM

FEM = ['Comum', 'Incomum', 'Rara', 'Épica', 'Única', 'Lendária', 'Mítica', 'Primordial']       # a categoria, quando o nome que vem antes é feminino (a fechadura, a armadilha)


# ---------- ler a pessoa ----------
def grau(p):
    """a mão de manha da pessoa (0 Leigo, 2 Iniciante, 4 Treinado, 6 Mestre, 8 Lendário)"""
    m = p.get('maestria') if isinstance(p, dict) else None
    return int(m.get('manha', 0)) if isinstance(m, dict) else 0


def blocos_de(p):
    """os blocos de treino de manha da pessoa"""
    t = p.get('treino') if isinstance(p, dict) else None
    return int(t.get('manha', 0)) if isinstance(t, dict) else 0


def feito_de(p):
    """a maior categoria que a pessoa já abriu ou desarmou de verdade (marca.feito_manha), ou −1 se nenhuma"""
    m = p.get('marca') if isinstance(p, dict) else None
    v = m.get('feito_manha') if isinstance(m, dict) else None
    return v if isinstance(v, int) and not isinstance(v, bool) else -1


def gazua_de(E, pid):
    """a melhor gazua inteira que a pessoa leva (o registro, com o id), ou None"""
    gs = [it for it in E['itens']['itens'].values() if it.get('dono') == pid and it.get('tipo') == 'gazua' and it['dur'][0] > 0]
    return max(gs, key=lambda it: (it['cat'], it['dur'][0]), default=None)


def _arma_de_impacto(E, pid):
    import estado
    w = estado.pecas(E, pid)['arma']
    return w if w and w.get('familia') in TM.ARROMBAR_ARMAS and w['dur'][0] > 0 else None


# ---------- a conta ----------
def _povo(p, teste, pedra=False):
    """o +2 do povo no teste do ladino (povos.manha), com o teto por teste (tabelas_povos.MANHA_TETO: o mesmo do Grande Dom), conferido aqui também"""
    import povos
    try: import tabelas_povos as TP; teto = getattr(TP, 'MANHA_TETO', 2)
    except ModuleNotFoundError: teto = 2
    return max(0, min(teto, povos.manha(p, teste, pedra)))


def contra(E, pid, teste, cat):
    """(o número contra o qual se rola, a ferramenta): achar contra 20 + 6 por categoria; abrir e desarmar contra 24 + 8 × (a categoria − a da gazua; sem gazua, −1);
    arrombar contra 24 + 8 × (a categoria da porta − a da arma de impacto em uso; o ombro, −1). Outro teste: None (o número é de quem chama)"""
    if teste == 'achar': return TM.ACHAR[0] + TM.ACHAR[1] * cat, None
    if teste in ('gazua', 'desarmar'):
        g = gazua_de(E, pid); return TM.GAZUA[0] + TM.GAZUA[1] * (cat - (g['cat'] if g else TM.SEM_GAZUA)), (g['id'] if g else None)
    if teste == 'arrombar':
        w = _arma_de_impacto(E, pid); return TM.ARROMBAR[0] + TM.ARROMBAR[1] * (cat - (w['cat'] if w else TM.OMBRO)), (w['id'] if w else None)
    return None


_contra = contra          # (o nome da função; dentro do testa, `contra` é o número)


def contra_escutar(material='madeira', mortos=False):
    """o número de escutar à porta: pelo material dela (o ferro e a pedra, 4 mais difícil), e mais 6 se quem está do outro lado são mortos (não respiram)"""
    return TM.ESCUTAR.get(material, TM.ESCUTAR['madeira']) + (TM.ESCUTAR['mortos'] if mortos else 0)


def _soma(E, pid, teste, mais=0, pedra=False, vista=True):
    """o que se soma ao 2d20 neste teste, sem rolar: o atributo ÷ 10, a pena do corpo, a mão (se o teste a leva), o dom (o que a pessoa já viu; ou o de verdade), o povo e o resto"""
    import estado, corpo, talento
    p = E['gente'][pid]; atr, soma_mao = TM.TESTES[teste]
    dm = (talento.dom_visto(p, 'manha') if vista else talento.dom(p, 'manha')) if soma_mao else 0
    return p['atributos'][atr] // 10 + corpo.pena(p, estado.agora(E)) + (grau(p) if soma_mao else 0) + dm + _povo(p, teste, pedra) + mais


def chance(E, pid, teste, cat=None, contra=None, mais=0, pedra=False, vista=True):
    """(a chance de passar, o número, a ferramenta), sem rolar nada: a conta exata do 2d20 que rola de novo no 20 (a da forja). `vista`: a conta que vai à mesa
    (sem o dom que a pessoa ainda não viu); sem ela, a de verdade"""
    import oficio
    if teste not in TM.TESTES: sys.exit(f'teste do ladino desconhecido: "{teste}" (os que há: {", ".join(TM.TESTES)})')
    ferr = None
    if contra is None:
        c = _contra(E, pid, teste, cat) if cat is not None else None
        if c is None: sys.exit(f'o teste "{teste}" pede o número (contra=)' + ('' if cat is not None else ' ou a categoria (cat=)'))
        contra, ferr = c
    return oficio.chance_de(contra - _soma(E, pid, teste, mais, pedra, vista)), contra, ferr


def testa(E, pid, teste, contra=None, cat=None, o_que=None, oculto=False, mais=0, pedra=False):
    """O DADO DO LADINO (o do jogador: teste.rola, rolado uma vez e escrito no turno). Dê `cat` (achar, gazua, desarmar, arrombar: a conta sai do contra()) ou `contra`
    (escondido, escutar, atencao: o número de quem vigia, que quem chama faz). Soma a mão (se o teste a leva), o dom escondido da manha e o +2 do povo; `mais` é o resto
    (a armadura e a luz no andar escondido). Devolve o r do teste.rola, com: teste, margem, falhou_feio, ferramenta e efeitos (o que entra no evento de quem chamou:
    o dom que se mostrou). Não grava nada. O desgaste da ferramenta (falhar por 5 ou mais) é o gasta(r)."""
    import estado, teste as dado, talento
    if teste not in TM.TESTES: sys.exit(f'teste do ladino desconhecido: "{teste}" (os que há: {", ".join(TM.TESTES)})')
    p = E['gente'].get(pid) or sys.exit(f'não há a pessoa "{pid}"')
    ferr = None
    if contra is None:
        if cat is None: sys.exit(f'o teste "{teste}" pede o número (contra=) ou a categoria (cat=)')
        c = _contra(E, pid, teste, cat)
        if c is None: sys.exit(f'o teste "{teste}" pede o número (contra=): a conta é de quem chama')
        contra, ferr = c
    atr, soma_mao = TM.TESTES[teste]
    vis = (grau(p) if soma_mao else 0) + _povo(p, teste, pedra) + mais
    r = dado.rola(E, o_que or TM.NOMES.get(teste, teste), atr, contra, mais=vis + (talento.dom_visto(p, 'manha') if soma_mao else 0), quem=pid, oculto=oculto, **(talento.kw(p, 'manha') if soma_mao else {}))
    r.update(teste=teste, margem=r['total'] - r['contra'], falhou_feio=r['total'] - r['contra'] <= -TM.FALHA, ferramenta=ferr,
             efeitos=talento.mostra(E, pid) if talento.decidiu(r) else [])
    return r


def gasta(r):
    """os efeitos do desgaste da ferramenta depois de um teste (o r do testa): abrir, desarmar ou arrombar que falha por FALHA ou mais tira 1 de durabilidade da gazua
    (ou da arma de arrombar); a zero, ela quebra e não conta mais. Quem chama põe no evento dele, junto do resto ([] se não gasta nada)"""
    if r.get('teste') in ('gazua', 'desarmar', 'arrombar') and r.get('falhou_feio') and r.get('ferramenta'): return [['item', r['ferramenta'], 'dur', 'soma', -1]]
    return []


def mais_barulhento(E, ids, luz=False):
    """(pid, mais): quem do grupo anda pior escondido (o grupo anda no passo do mais barulhento), e o `mais` dele para o testa(..., 'escondido'): a armadura do tronco
    e a luz (se o grupo leva luz e o lugar está escuro)"""
    import estado
    ids = [k for k in ids if k in E['gente']]
    if not ids: sys.exit('o andar escondido pede um grupo de gente que existe')
    def conta(pid):
        p = E['gente'][pid]; mais = TM.ESCONDIDO_LUZ if luz else 0
        tronco = [it for it in estado.pecas(E, pid)['veste'] if 'tronco' in (it.get('cobre') or [])]
        if tronco: mais += min(TM.ESCONDIDO_ARMADURA.get(it.get('material'), 0) for it in tronco)
        return p['atributos']['Agilidade'] // 10 + grau(p) + _povo(p, 'escondido') + mais, mais
    pid = min(ids, key=lambda k: conta(k)[0])
    return pid, conta(pid)[1]


# ---------- a mão: o treino e o feito ----------
def _chega(p, blocos, feito_cat):
    """o grau de manha a que a pessoa chega com estes blocos e este feito (a escada das armas vezes o talento, até o teto dele; de Mestre para cima, o feito),
    e por que não passa dali ('' se não há nada a dizer)"""
    import talento
    tem = grau(p); txt = ''
    for g in sorted(M.MAESTRIA_BLOCOS):
        if g <= tem: continue
        quer = talento.pede(p, 'manha', M.MAESTRIA_BLOCOS, g)
        if quer is None:
            if blocos >= M.MAESTRIA_BLOCOS[g]: txt = f" (a mão não sobe mais em manha: o talento para em {T.MAESTRIAS[talento.teto(p, 'manha')]})"
            break
        if blocos < quer: break
        if g in TM.FEITO and feito_cat < TM.FEITO[g]:
            txt = f" (tem os blocos para {T.MAESTRIAS[g]} em manha; falta o feito: abrir uma fechadura ou desarmar uma armadilha {FEM[TM.FEITO[g]]}, ou melhor, de verdade)"; break
        tem = g
    return tem, txt


def treino(E, pid, blocos=1):
    """os efeitos de `blocos` blocos de treino de manha: o treino.manha e a mão que sobe (pelo talento e pelo feito que a pessoa já tem). Não grava nada.
    Na masmorra, quem chama dá no máximo TREINO_BLOCO por bloco que fecha lá dentro (só a quem andou escondido, escutou, procurou, abriu ou desarmou)"""
    p = E['gente'][pid]; n = int(blocos)
    if n <= 0: return []
    ef = [['pessoa', pid, 'treino.manha', 'soma', n]]
    g, _ = _chega(p, blocos_de(p) + n, feito_de(p))
    if g > grau(p): ef.append(['pessoa', pid, 'maestria.manha', 'poe', g])
    return ef


def feito(E, pid, cat):
    """os efeitos do FEITO: se `cat` passa da maior categoria que a pessoa já abriu ou desarmou de verdade (não no treino), a marca.feito_manha sobe, e a mão sobe junto
    se os blocos já estavam lá esperando o feito. [] se não passa. Não grava nada"""
    p = E['gente'][pid]
    if cat is None or not isinstance(cat, int) or cat <= feito_de(p): return []
    ef = [['pessoa', pid, 'marca.feito_manha', 'poe', cat]]
    g, _ = _chega(p, blocos_de(p), cat)
    if g > grau(p): ef.append(['pessoa', pid, 'maestria.manha', 'poe', g])
    return ef


def sobe(E, pid):
    """a mão de manha sobe, num evento "treinar", se os blocos e o feito já chegaram (o que ficou para trás). Devolve o texto para a mesa ('' se nada mudou)"""
    import estado
    p = E['gente'][pid]; g, txt = _chega(p, blocos_de(p), feito_de(p))
    if g > grau(p):
        estado.aplica(E, 'treinar', [['pessoa', pid, 'maestria.manha', 'poe', g]], onde=estado.onde(E, pid), quem=[pid], texto=f"{p['nome']} chega a {T.MAESTRIAS[g]} em manha")
        return f'. MAESTRIA: {T.MAESTRIAS[g]} em manha'
    return txt


def treinar(E, pid, blocos):
    """o treino da manha EM CASA: com uma gazua (a fechadura velha, o passo macio no pátio), bloco pesado, como o treino de arma; cada bloco soma 1 de treino. Grava"""
    import estado, ato
    p = estado.presente(E, pid, 'treinar a manha')
    try: n = int(blocos)
    except (TypeError, ValueError): n = 0
    if n < 1: sys.exit(f'diga quantos blocos de treino, em número inteiro (1 ou mais): `python3 manha.py treinar 2` (veio "{blocos}"). Um bloco são 4 horas.')
    if TM.TREINO_PEDE_GAZUA and not gazua_de(E, pid):
        sys.exit(f"{p['nome']} não leva gazua inteira: o treino da manha em casa pede uma (a fechadura velha, o passo macio no pátio). A loja vende; a forja faz (`oficio.py forjar gazua Comum`).")
    feitos, pq = ato.passa(E, pid, n, 'treinar', esforco=TM.TREINO_ESFORCO, mais=lambda i: [['pessoa', pid, 'treino.manha', 'soma', 1]], texto=f"{p['nome']} treina a manha")
    return f"{p['nome']} treina a manha {estado.tantos(feitos, 'bloco')}" + sobe(E, pid) + (f'. PAROU: {pq}' if pq else '')


# ---------- a vila de teste: o Quim, a tocha e a gazua na loja ----------
def na_vila(E, vila='vila'):
    """O LADINO DA VILA (o Quim, sobrinho do Lino), a TOCHA na loja (o povo a gasta: a produção no consumo, o estoque no alvo) e UMA GAZUA na prateleira.
    Aplica os eventos (gera) e devolve as linhas que contam o que pôs. Recusa com a frase ANTES de mudar qualquer coisa se já foi posto, ou se a vila não tem loja."""
    import estado, talento, mercado
    from itens import item
    from pessoas import padrao
    q = TM.QUIM
    l = E['lugares'].get(vila) or sys.exit(f'não há o lugar "{vila}": o ladino mora numa vila que existe')
    if q['id'] in E['gente']: sys.exit(f"{E['gente'][q['id']]['nome']} já está no mundo: o ladino da vila não se põe duas vezes")
    if l.get('feira_masmorra'): sys.exit(f"a loja {estado.de(E, vila)} já tem a tocha e a gazua (desde o Dia {l['feira_masmorra']}): não se põem duas vezes")
    if not mercado.tem_mercado(E, vila): sys.exit(f"{l['nome']} não tem mercado: o ladino e a loja da tocha vão a uma vila com povo")
    estado.sem_luta(E)
    r = dict(nome=q['nome'], nivel=q['nivel'], atributos=padrao(q['nome'], q['nivel'], molde=q['molde'])['atributos'], lugar=vila, grau_oficio=q['grau_oficio'],
             maestria=dict(q['maestria']), treino={k: M.MAESTRIA_BLOCOS[g] for k, g in q['maestria'].items() if g in M.MAESTRIA_BLOCOS}, moedas=q['moedas'], sobre=q['sobre'])
    estado.aplica(E, 'gera', [['pessoa', 'nasce', q['id'], talento.nasce(E, q['id'], r)]], onde=vila, quem=[q['id']], texto=f"{q['nome']}, {q['sobre']}")
    s0 = E['itens']['seq']; nome = lambda t, f: (f.capitalize() if t == 'arma' else f'Armadura de {f}' if t == 'armadura' else 'Gazua') + f" de {q['nome']}"      # "Adaga de Quim", como a gente da vila
    its = [item(t, c, nome(t, f), **({} if t == 'gazua' else dict(familia=f) if t == 'arma' else dict(material=f)), dono=q['id']) for t, f, c, _ in q['pecas']]
    estado.aplica(E, 'gera', [['item', 'nasce', it] for it in its], onde=vila, quem=[q['id']], texto=f"as peças de {q['nome']}")
    usos = [['item', f'i{s0 + k + 1:04d}', 'uso', 'poe', uso] for k, (_, _, _, uso) in enumerate(q['pecas']) if uso]
    if usos: estado.aplica(E, 'gera', usos, onde=vila, quem=[q['id']], texto=f"{q['nome']} se veste")
    loja = mercado.funda_masmorra(E, vila, como='o Lino vende a tocha e a gazua')
    return [f"{q['nome']}, {q['sobre']}: nível {q['nivel']}, manha de {T.MAESTRIAS[q['maestria']['manha']]}, " + ', '.join(it['nome'] for it in its) + f", {q['moedas']} de prata "
            f"(o talento e o dom rolados: só o Mestre sabe).", loja]


# ---------- a mesa ----------
def _degraus(p):
    """a escada da manha como a pessoa a conhece: com o talento, se ele já apareceu; senão, a de tabela"""
    import talento
    sabe = talento.aparece(p, 'manha')
    return {g: (talento.pede(p, 'manha', M.MAESTRIA_BLOCOS, g) if sabe else q) for g, q in M.MAESTRIA_BLOCOS.items()}


def _pc(x): return f'{100 * x:.0f}%'


def _linha_chance(E, pid, teste, cats=TM.CHANCE_CATS):
    return ' · '.join(f"{FEM[c]} {_pc(chance(E, pid, teste, cat=c)[0])}" for c in cats)


def ver(E, pid):
    """as linhas da mesa do ladino para esta pessoa: a mão, os blocos, o feito, a gazua, e a chance de cada teste hoje (a conta que a mesa faz: sem o dom que ela não viu)"""
    import estado
    p = E['gente'][pid]; g = grau(p); bl = blocos_de(p); fe = feito_de(p); dg = _degraus(p)
    prox = next(((k, q) for k, q in sorted(dg.items()) if k > g and q is not None), None)
    L = [f"**{p['nome']}**: manha de {T.MAESTRIAS[g]} · {estado.tantos(bl, 'bloco')} de treino" + (f" ({T.MAESTRIAS[prox[0]]} aos {prox[1]}" + (f" e o feito: abrir ou desarmar uma {FEM[TM.FEITO[prox[0]]]} de verdade" if prox[0] in TM.FEITO else '') + ')' if prox else '')
         + (f" · o feito: já abriu ou desarmou uma {FEM[fe]}" if fe >= 0 else '')]
    gs = sorted((it for it in E['itens']['itens'].values() if it.get('dono') == pid and it.get('tipo') == 'gazua'), key=lambda it: -it['cat'])
    a = _arma_de_impacto(E, pid)
    L.append('Gazua: ' + (' · '.join(f"{it['nome']} ({T.CATS[it['cat']]}, {it['dur'][0]}/{it['dur'][1]}" + (', QUEBRADA' if it['dur'][0] <= 0 else '') + ')' for it in gs) if gs else 'nenhuma (sem ela, o grampo conta um degrau abaixo do Comum)')
             + ' · para arrombar: ' + (f"{a['nome']} em uso" if a else 'o ombro (nenhuma maça, martelo ou malho em uso)'))
    L.append(f"A chance hoje (contra a categoria): abrir a fechadura e desarmar a armadilha: {_linha_chance(E, pid, 'gazua')} · achar o escondido: {_linha_chance(E, pid, 'achar')}"
             f" · arrombar: {_linha_chance(E, pid, 'arrombar')}. Falhar por {TM.FALHA} ou mais entorta a gazua e dispara a armadilha em quem desarmava.")
    return L


def voce(E):
    """a mão do ladino do personagem, no "Você" da MESA: só se ele tem manha, treino de manha, feito ou uma gazua (a MESA de quem não tem nada disso sai igual)"""
    import estado
    pid = estado.eu(E); p = E['gente'].get(pid) if pid else None
    if not isinstance(p, dict) or p.get('estado') != 'vivo': return []
    tem_gazua = any(it.get('dono') == pid and it.get('tipo') == 'gazua' for it in E['itens']['itens'].values())
    if not (grau(p) or blocos_de(p) or feito_de(p) >= 0 or tem_gazua): return []
    L = ver(E, pid)
    return [f"**A manha** (o ladino; `manha.py ver` · `manha.py treinar N`): " + L[0].split(': ', 1)[1]] + L[1:]


def so_mestre(E):
    """o SÓ O MESTRE: a manha de quem está com o personagem (no mesmo lugar) e tem a mão ou uma gazua: quem é o ladino do grupo"""
    import estado
    pid = estado.eu(E)
    if not pid: return []
    aqui = estado.onde(E, pid); L = []
    for k, x in E['gente'].items():
        if k == pid or not isinstance(x, dict) or x.get('estado') != 'vivo' or estado.onde(E, k) != aqui or not grau(x): continue
        g = gazua_de(E, k)
        L.append(f"a manha de {x['nome']}: {T.MAESTRIAS[grau(x)]} ({estado.tantos(blocos_de(x), 'bloco')}); gazua: {g['nome'] + ' (' + T.CATS[g['cat']] + ')' if g else 'nenhuma'}")
    return L


# ---------- a linha de comando ----------
def _cat(x):
    from itens import cat_i
    return cat_i(int(x) if str(x).isdigit() else x)


def main(a=None):
    a = sys.argv[1:] if a is None else list(a)
    op = dict(x.split('=', 1) for x in a if '=' in x); pos = [x for x in a if '=' not in x]
    if not pos or pos[0] not in ('ver', 'chance', 'treinar', 'furtar'): print(__doc__); return
    if pos[0] == 'furtar':
        sys.exit('O furto fica escrito e entra na etapa 3, quando a gente lembrar de quem a roubou e a vila tiver quem vigie: hoje não se furta '
                 '(sem memória nem guarda, o ladino tiraria a bolsa da vila inteira). A regra está no capítulo 18.')
    import estado
    E = estado.carrega(); pid = op.get('quem') or (pos[1] if pos[0] == 'ver' and len(pos) > 1 else None) or estado.eu(E)
    if pid not in E['gente']: sys.exit(f'não há a pessoa "{pid}"')
    if pos[0] == 'ver': print('\n'.join(ver(E, pid))); return
    if pos[0] == 'chance':
        if len(pos) < 3 or pos[1] not in ('achar', 'gazua', 'desarmar', 'arrombar'):
            sys.exit('diga o teste (achar, gazua, desarmar ou arrombar) e a categoria: `python3 manha.py chance gazua Incomum`')
        c = _cat(pos[2]); ch, n, ferr = chance(E, pid, pos[1], cat=c)
        it = E['itens']['itens'].get(ferr) if ferr else None
        print(f"{E['gente'][pid]['nome']}, {TM.NOMES[pos[1]]} {FEM[c]}: contra {n}" + (f", com {it['nome']}" if it else ', sem ferramenta' if pos[1] != 'achar' else '') + f": {_pc(ch)} (só olha: nada foi rolado)")
        return
    out = treinar(E, pid, pos[1] if len(pos) > 1 else 0)
    estado.grava(E)                                         # grava ANTES de falar: a saída cortada não perde nada
    print(out)
    import ato
    print(ato.ultima_linha(E, pid))


if __name__ == '__main__':
    import signal; hasattr(signal, 'SIGPIPE') and signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    main()
