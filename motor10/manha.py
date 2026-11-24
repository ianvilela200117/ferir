#!/usr/bin/env python3
"""manha.py — MOTOR 10, ETAPA 4b: O LADINO (capítulo 18; os números no tabelas_manha.py; o contrato: projeto/ETAPA_4B.md, seção 12).

  A MANHA é o 17º caminho, o ofício do ladino: andar escondido, escutar, achar e desarmar armadilha, abrir fechadura (e o furto, que fica escrito para a etapa 3).
  Sobe por blocos como as armas (40, 160, 500, 1.500, vezes o talento), com feito de Mestre para cima. Todo teste do ladino é o dado do jogador (teste.rola: declarado
  e rolado uma vez): 2d20 + o atributo ÷ 10 + a mão de manha + o dom escondido + o +2 do povo, contra um número. A GAZUA é a arma, a fechadura é a armadura.

  ESQUELETO DO ALICERCE (onda 1): as funções do contrato, com a conta do projeto A (seção 4), o dom e o povo. A frente L (o ladino) enche o resto (o treino, o feito,
  a gazua na forja e na loja, o Quim, o comando) sem mudar a assinatura nem o que cada função devolve.

Uso em código (o que as outras frentes chamam):
  grau(p) · gazua_de(E, pid) · contra(E, pid, teste, cat) · testa(E, pid, teste, contra=None, cat=None, o_que=None, oculto=False, mais=0, pedra=False)
  mais_barulhento(E, ids, luz=False) · treino(E, pid, blocos=1) · feito(E, pid, cat) · na_vila(E, vila='vila') · voce(E) · so_mestre(E)
Uso de linha de comando:
  python3 manha.py ver [ID]           a mão do ladino (sem ID: o personagem)
"""
import sys
import tabelas as T
import tabelas_manha as TM


def grau(p):
    """a mão de manha da pessoa (0 Leigo, 2 Iniciante, 4 Treinado, 6 Mestre, 8 Lendário)"""
    m = p.get('maestria') if isinstance(p, dict) else None
    return int(m.get('manha', 0)) if isinstance(m, dict) else 0


def gazua_de(E, pid):
    """a melhor gazua inteira que a pessoa leva (o registro, com o id), ou None"""
    gs = [it for it in E['itens']['itens'].values() if it.get('dono') == pid and it.get('tipo') == 'gazua' and it['dur'][0] > 0]
    return max(gs, key=lambda it: (it['cat'], it['dur'][0]), default=None)


def _arma_de_impacto(E, pid):
    import estado
    w = estado.pecas(E, pid)['arma']
    return w if w and w.get('familia') in TM.ARROMBAR_ARMAS and w['dur'][0] > 0 else None


def contra(E, pid, teste, cat):
    """(o número contra o qual se rola, a ferramenta): achar contra 20 + 6 por categoria; abrir e desarmar contra 24 + 8 × (a categoria − a da gazua; sem gazua, −1);
    arrombar contra 24 + 8 × (a categoria da porta − a da arma de impacto em uso; o ombro, −1). Outro teste: None (o número é de quem chama)"""
    if teste == 'achar': return TM.ACHAR[0] + TM.ACHAR[1] * cat, None
    if teste in ('gazua', 'desarmar'):
        g = gazua_de(E, pid); return TM.GAZUA[0] + TM.GAZUA[1] * (cat - (g['cat'] if g else TM.SEM_GAZUA)), (g['id'] if g else None)
    if teste == 'arrombar':
        w = _arma_de_impacto(E, pid); return TM.ARROMBAR[0] + TM.ARROMBAR[1] * (cat - (w['cat'] if w else TM.SEM_GAZUA)), (w['id'] if w else None)
    return None


_contra = contra          # (o nome da função; dentro do testa, `contra` é o número)


def testa(E, pid, teste, contra=None, cat=None, o_que=None, oculto=False, mais=0, pedra=False):
    """O DADO DO LADINO (o do jogador: teste.rola, rolado uma vez e escrito no turno). Dê `cat` (achar, gazua, desarmar, arrombar: a conta sai do contra()) ou `contra`
    (escondido, escutar, atencao: o número de quem vigia, que quem chama faz). Soma a mão (se o teste a leva), o dom escondido da manha e o +2 do povo; `mais` é o resto
    (a armadura e a luz no andar escondido). Devolve o r do teste.rola, com: teste, margem, falhou_feio, ferramenta e efeitos (o que entra no evento de quem chamou:
    o dom que se mostrou). Não grava nada."""
    import estado, teste as dado, talento, povos
    if teste not in TM.TESTES: sys.exit(f'teste do ladino desconhecido: "{teste}" (os que há: {", ".join(TM.TESTES)})')
    p = E['gente'].get(pid) or sys.exit(f'não há a pessoa "{pid}"')
    ferr = None
    if contra is None:
        if cat is None: sys.exit(f'o teste "{teste}" pede o número (contra=) ou a categoria (cat=)')
        c = _contra(E, pid, teste, cat)
        if c is None: sys.exit(f'o teste "{teste}" pede o número (contra=): a conta é de quem chama')
        contra, ferr = c
    atr, soma_mao = TM.TESTES[teste]
    vis = (grau(p) if soma_mao else 0) + povos.manha(p, teste, pedra) + mais
    r = dado.rola(E, o_que or teste, atr, contra, mais=vis + (talento.dom_visto(p, 'manha') if soma_mao else 0), quem=pid, oculto=oculto, **(talento.kw(p, 'manha') if soma_mao else {}))
    r.update(teste=teste, margem=r['total'] - r['contra'], falhou_feio=r['total'] - r['contra'] <= -TM.FALHA, ferramenta=ferr,
             efeitos=talento.mostra(E, pid) if talento.decidiu(r) else [])
    return r


def mais_barulhento(E, ids, luz=False):
    """(pid, mais): quem do grupo anda pior escondido (o grupo anda no passo do mais barulhento), e o `mais` dele para o testa(..., 'escondido'): a armadura do tronco
    e a luz (se o grupo leva luz e o lugar está escuro)"""
    import estado, povos
    def conta(pid):
        p = E['gente'][pid]; mais = TM.ESCONDIDO_LUZ if luz else 0
        tronco = [it for it in estado.pecas(E, pid)['veste'] if 'tronco' in (it.get('cobre') or [])]
        if tronco: mais += min(TM.ESCONDIDO_ARMADURA.get(it.get('material'), 0) for it in tronco)
        return p['atributos']['Agilidade'] // 10 + grau(p) + povos.manha(p, 'escondido') + mais, mais
    pid = min(ids, key=lambda k: conta(k)[0])
    return pid, conta(pid)[1]


def treino(E, pid, blocos=1):
    """(frente L) os efeitos do treino de manha (o treino.manha e a mão que sobe, pelo talento.pede e o feito). O esqueleto não treina: []"""
    return []


def feito(E, pid, cat):
    """(frente L) os efeitos do feito (marca.feito_manha), se `cat` passa do que a pessoa já abriu ou desarmou de verdade. O esqueleto: []"""
    return []


def na_vila(E, vila='vila'):
    """(frente L) o Quim, o ladino da vila; a tocha e a gazua na loja: aplica os eventos dele (gera) e devolve as linhas. O esqueleto não põe nada."""
    return []


def voce(E): return []          # (frente L) a mão do ladino do personagem, só se ele tem manha (a MESA de hoje sai igual)
def so_mestre(E): return []


def main(a=None):
    a = sys.argv[1:] if a is None else a
    if a[:1] == ['ver']:
        import estado
        E = estado.carrega(); pid = a[1] if len(a) > 1 else estado.eu(E)
        p = E['gente'].get(pid) or sys.exit(f'não há a pessoa "{pid}"'); g = gazua_de(E, pid)
        print(f"{p['nome']}: manha de {T.MAESTRIAS.get(grau(p), grau(p))} · gazua: {g['nome'] if g else 'nenhuma'}")
    else: print(__doc__)


if __name__ == '__main__':
    main()
