#!/usr/bin/env python3
"""encanto.py — MOTOR 10: O ENCANTO (etapa da magia, capítulo 12). Os números moram no tabelas_magia_mundo.py; a obra é a do oficio.py.

  O OFÍCIO DO ENCANTO trabalha na MESA DE RUNAS do lugar (o campo `runas`, 0 a 4), com a maestria de encanto (sobe pela tabela da forja: 50, 150, 375, 1.000).
  FAZ O FOCO E O AMULETO como a forja faz a adaga: a matéria da peça (a varinha, 2 de madeira e 1 de osso; o cajado, 4 e 1; o símbolo, 3 de metal; o talismã, 2 de osso
    e 1 de couro; o amuleto, 1 de osso; do Épico para cima, matéria Rara e um NÚCLEO), 3^k blocos pesados e o teste da forja (falhar por pouco: uma categoria abaixo; por 5
    ou mais, a matéria some).
  GRAVA UM FEITIÇO numa arma, armadura ou escudo: quem grava sabe o feitiço (ou tem ao lado quem sabe); a ESSÊNCIA da categoria da peça (até o Raro, 4 de osso e 2 de erva;
    do Épico para cima, um núcleo); um terço dos blocos da forja (Comum e Incomum 1, Raro 3, Épico 9); e o teste da forja contra 28 + 6 por categoria da peça.
    Falhou por 1 a 4: grava um grau abaixo. Por 5 ou mais: a essência some (o núcleo também) e a peça perde 5 de durabilidade. POR 10 OU MAIS A PEÇA SAI MALDITA
    (é de onde vêm as peças malditas do mundo): quem a puser em uso pega a maldição, e ela só quebra devolvendo a peça à mesa de runas onde se gravou.
  Uma peça leva um encanto; do Único para cima, dois. Na luta, o dono solta o feitiço uma vez (a peça vale foco um degrau abaixo) e ela volta a carregar 1 bloco depois.

Uso (o personagem do jogador, ou quem=ID):
  python3 encanto.py ver                                       a mesa de runas daqui, a sua mão, as obras abertas
  python3 encanto.py pede foco FORMA CATEGORIA | amuleto CATEGORIA       o que a peça pede e a chance, sem abrir nada
  python3 encanto.py fazer foco FORMA CATEGORIA ["Nome"] [blocos=N] [nucleo=ID] · fazer amuleto CATEGORIA ["Nome"] ...
  python3 encanto.py gravar ITEM FEITICO [para=DONO] [com=QUEM_SABE] [blocos=N] [nucleo=ID]    grava um feitiço numa peça (sua, ou de quem está aqui)
  python3 encanto.py continua [OBRA] [blocos=N] · python3 encanto.py larga OBRA
  python3 encanto.py jornal N                                  N blocos a serviço da mesa de runas do lugar (o salário da sua mão, até a jornada)
  python3 encanto.py runas NIVEL|nada "como foi"               o Mestre registra a mesa de runas do lugar (0 a 4)
FORMA: varinha cajado símbolo talismã · CATEGORIA: Comum Incomum Raro Épico Único Lendário
"""
import sys
import tabelas as T
import tabelas_mundo as M
import tabelas_oficio as O
import tabelas_magia_mundo as W
import estado, ato, teste, talento, oficio
from itens import rotulo

FEM = oficio.FEM
tantos = estado.tantos
def _nf(f): return T.nome_feitico(f)


def essencia(cat):
    """a essência de gravar numa peça desta categoria: {chave: quanto} até o Raro; do Épico para cima, nada (vai um núcleo)"""
    return {} if O.pede_nucleo(cat) else {M.materia(k, cat): n for k, n in W.ESSENCIA.items()}


def _quem_sabe(E, pid, f, com):
    """quem sabe o feitiço para a gravação: quem grava, ou quem está ao lado dele (com=). Devolve o id."""
    p = E['gente'][pid]
    if f in (p.get('feiticos') or []): return pid
    if com:
        q = E['gente'].get(com) or sys.exit(f'não há a pessoa "{com}"')
        if q['estado'] != 'vivo' or q['lugar'] != p['lugar'] or estado.fora(E, com): sys.exit(f"{q['nome']} não está aqui")
        if f not in (q.get('feiticos') or []): sys.exit(f"{q['nome']} não sabe {_nf(f)}")
        return com
    sys.exit(f"{p['nome']} não sabe {_nf(f)}: grave com quem saiba ao lado (com=PESSOA)")


def gravar(E, pid, iid, f, para=None, com=None, blocos=None, nucleo=None):
    """abre a gravação (a essência sai da carga e entra na obra) e trabalha `blocos` blocos (None: até fechar)"""
    import magia_mundo
    if f not in T.FEITICOS: sys.exit(f'feitiço desconhecido: "{f}" (os que há: {", ".join(T.FEITICOS)})')
    p = oficio._vivo(E, pid); lid = p['lugar']
    if oficio.banca(E, lid, 'encanto') is None: sys.exit(f"{E['lugares'][lid]['nome']} não tem mesa de runas: não se grava aqui")
    it = E['itens']['itens'].get(iid) or sys.exit(f'não há o item "{iid}" no Livro de Itens')
    dono = it.get('dono')
    if dono != pid and dono != para: sys.exit(f"{it['nome']} não é de {p['nome']}" + (f" (é de {E['gente'][dono]['nome']}: grave com para={dono}, com o dono aqui)" if dono in E['gente'] else ''))
    if dono != pid:
        q = E['gente'][dono]
        if q['estado'] != 'vivo' or q['lugar'] != lid or estado.fora(E, dono): sys.exit(f"{q['nome']} não está aqui com a peça")
    if it['tipo'] not in estado.COM_ENCANTO: sys.exit(f"{it['nome']} não leva encanto (só arma, armadura e escudo: o foco e o amuleto já são magia)")
    if it['dur'][0] <= 0: sys.exit(f"{it['nome']} está quebrada: conserte antes")
    if len(it.get('encantos') or []) >= M.encantos_max(it['cat']): sys.exit(f"{it['nome']} já tem os encantos que cabem numa peça {T.CATS[it['cat']]} ({M.encantos_max(it['cat'])})")
    if any(o.get('item') == iid for o in E['itens'].get('obras', {}).values()): sys.exit(f"{it['nome']} já está numa obra aberta")
    sabe = _quem_sabe(E, pid, f, com); s = E['gente'][sabe]; grau = min(4, magia_mundo.mao(s, magia_mundo.trad_de(s, f)) // 2); cat = it['cat']
    mat = essencia(cat); carga = p.get('carga', {}); falta = {k: n - carga.get(k, 0) for k, n in mat.items() if carga.get(k, 0) < n}
    if falta: sys.exit(f"falta essência para gravar: {', '.join(f'{n} de {estado.nome_bem(k)}' for k, n in falta.items())} (pede {', '.join(f'{n} de {estado.nome_bem(k)}' for k, n in mat.items())})")
    nid = oficio._nucleo(E, pid, cat, nucleo) if O.pede_nucleo(cat) else None
    nome = f"a gravação de {_nf(f)} em {it['nome']}"
    reg = dict(quem=pid, lugar=lid, tipo='gravar', oficio='encanto', item=iid, para=dono, feitico=f, grau=grau, sabe=sabe, cat=cat, blocos=0, pede=W.blocos_gravar(cat), materia=mat, nucleo=nid, nome=nome)
    ef = [['pessoa', pid, 'carga.' + k, 'soma', -n] for k, n in mat.items()] + [['obra', 'abre', reg]]
    estado.aplica(E, 'encantar', ef, onde=lid, quem=[pid], texto=f"{p['nome']} abre {nome}")
    oid = f"o{E['itens']['oseq']:04d}"
    R = oficio.continua(E, pid, oid, blocos)
    R['texto'] = f"Obra {oid} aberta: {nome} (grau {grau}, de quem sabe o feitiço)." + (f" Entrou a essência: {', '.join(f'{n} de {estado.nome_bem(k)}' for k, n in mat.items())}." if mat else f" Entrou o núcleo {nid}.") + '\n' + R['texto']
    return R


encantar = gravar                                           # o nome que o contrato dá (projeto/ETAPA_MAGIA.md, seção 12)


def remata(E, o):
    """os blocos da gravação fecharam: sai o teste (o da forja, com a mão de encanto), e a obra fecha (oficio.remata chama isto)"""
    oid = o['id']; pid = o['quem']; p = E['gente'][pid]; cat = o['cat']; lid = o['lugar']; nid = o.get('nucleo'); L = E['itens']['itens']; iid = o['item']; dia = E['relogio']['dia']
    it = L.get(iid)
    if not it or it.get('dono') != o.get('para'): sys.exit(f"a peça da obra {oid} mudou de mão ou saiu do Livro: a gravação não fecha (largue-a com `larga`)")
    if nid and nid not in L: sys.exit(f'o núcleo da obra {oid} não está mais no Livro de Itens: a gravação não fecha (largue-a com `larga`)')
    k = oficio.conta(E, pid, cat, 'encanto', lid)
    r = teste.rola(E, o['nome'], 'Afinidade', k['contra'], mais=k['mais'], quem=pid, **({'dom': k['oculto']} if k['oculto'] else {}))
    margem = r['total'] - r['contra']; oficio._faixa_do_dom(r, k, margem); ef = []; f = o['feitico']
    if margem > -O.POR_POUCO:
        g = o['grau'] if margem >= 0 else max(0, o['grau'] - 1)
        ef.append(['item', iid, 'encanto', 'grava', dict(feitico=f, grau=g, feito_por=pid, dia=dia)])
        ef.append(['item', iid, 'historia', 'junta', f"Dia {dia}: {p['nome']} gravou {_nf(f)} nela {estado.em(E, lid)}"])
        for grau, quer in sorted(O.FEITO_OBRA.items()):
            if cat >= quer and (p.get('marca') or {}).get('feito_encanto', 0) < grau: ef.append(['pessoa', pid, 'marca.feito_encanto', 'poe', grau])
        fim = 'acertou' if margem >= 0 else 'abaixo'
        txt = f"{p['nome']} grava {_nf(f)} em {it['nome']} ({teste.total_visto(r)} contra {r['contra']})" + ('' if margem >= 0 else f": erra por pouco, e o encanto sai um grau abaixo (grau {g})")
    else:
        ef.append(['item', iid, 'dur', 'soma', -W.ESTRAGO]); fim = 'perdeu'
        txt = f"a gravação de {_nf(f)} falha ({teste.total_visto(r)} contra {r['contra']}): some a essência" + (f" e o núcleo" if nid else '') + f", e {it['nome']} perde {W.ESTRAGO} de durabilidade"
        if margem <= -W.MALDITA_FALHA:
            rr = estado.sorte(E, f'encanto|maldita|{iid}'); tipo = rr.choice(M.MALDICAO_TIPOS)
            ef.append(['item', iid, 'maldita', 'poe', dict(nome=W.NOMES[tipo], cat=cat, tipo=tipo, condicao=dict(tipo='devolver', item=iid, onde=lid))]); fim = 'maldita'
            txt += f". FALHOU POR {-margem}: a peça sai MALDITA (quem a puser em uso pega a maldição; quebra devolvendo-a {estado.em(E, lid)})"
    if nid: ef.append(['item', nid, 'some'])
    ef.append(['obra', oid, 'fecha'])
    if talento.decidiu(r): ef += talento.mostra(E, pid)
    estado.aplica(E, 'encantar', ef, onde=lid, quem=list(dict.fromkeys([pid, o.get('para') or pid])), texto=txt)
    out = teste.diz(E, r) + f"\n  (o +{k['mais']}: maestria {k['maestria']}, runas {k['oficina']}, preparo {k['preparo']})\n" + txt[0].upper() + txt[1:] + '.' + oficio._diz_dom(E, pid, r) + oficio.sobe(E, pid, 'encanto')
    return dict(obra=oid, fim=fim, item=iid, rolagem=r, texto=out)


def poe_runas(E, lid, nivel, como=''):
    """o Mestre (ou o gerador) registra a mesa de runas de um lugar (0 a 4), ou tira (None)"""
    l = E['lugares'].get(lid) or sys.exit(f'não há o lugar "{lid}"')
    if nivel is not None and not 0 <= nivel < len(W.RUNAS): sys.exit(f'a mesa de runas vai de 0 ({W.RUNAS[0]}) a {len(W.RUNAS) - 1} ({W.RUNAS[-1]}); veio {nivel}')
    txt = f"{l['nome']} " + ('fica sem mesa de runas' if nivel is None else f'tem agora uma {oficio.nome_banca("encanto", nivel)}') + (f': {como}' if como else '')
    if not estado.aplica(E, 'mestre', [['lugar', lid, 'runas', 'poe', nivel]], onde=lid, texto=txt): return f"{l['nome']} já estava assim: nada mudou."
    return txt + '.'


def ver(E, pid):
    p = E['gente'][pid]; lid = p['lugar']; v = oficio.banca(E, lid, 'encanto'); L = []
    if estado.fora(E, pid): return []
    if v is not None: L.append(f"**{E['lugares'][lid]['nome']}:** {oficio.nome_banca('encanto', v)} · faz-se foco e amuleto (`encanto.py pede amuleto Comum`) e grava-se feitiço em peça (`encanto.py gravar ITEM FEITICO`)")
    if oficio.mao(p, 'encanto') or oficio.bancada(p, 'encanto'): L.append(f"Mão de encanto: {T.MAESTRIAS[oficio.mao(p, 'encanto')]} ({tantos(oficio.bancada(p, 'encanto'), 'bloco')} de runas)")
    for oid, o in oficio.obras_de(E, pid).items():
        if o.get('oficio') == 'encanto': L.append(f"Obra aberta {oid}: {oficio._nome_obra(E, o)}, {o['blocos']} de {o['pede']} blocos (`encanto.py continua {oid}`)")
    return L


def mesa(E):
    pid = estado.eu(E)
    if not pid or E['gente'][pid]['estado'] != 'vivo': return []
    L = ver(E, pid)
    return ['## O encanto'] + L if L else []


def main(a=None):
    a = sys.argv[1:] if a is None else list(a)
    op = dict(x.split('=', 1) for x in a if '=' in x); pos = [x for x in a if '=' not in x]
    cmds = ('ver', 'pede', 'fazer', 'gravar', 'continua', 'larga', 'jornal', 'runas')
    if not pos or pos[0] not in cmds: print(__doc__); return
    falta = lambda o_que, exemplo: sys.exit(f'{o_que}: `python3 encanto.py {exemplo}`')
    E = estado.carrega(); pid = op.get('quem') or estado.eu(E)
    if pid not in E['gente']: sys.exit(f'não há a pessoa "{pid}"')
    num = lambda k: int(op[k]) if op.get(k, '').isdigit() else sys.exit(f'{k}= pede um número inteiro (veio "{op[k]}")') if k in op else None
    def peca(i):
        tipo = pos[i] if len(pos) > i else falta('diga a peça: foco FORMA CATEGORIA, ou amuleto CATEGORIA', 'pede amuleto Comum')
        if tipo == 'foco':
            if len(pos) < i + 3: falta('diga a forma e a categoria do foco', 'pede foco varinha Comum')
            return oficio.molde('foco', pos[i + 2], pos[i + 3] if len(pos) > i + 3 else None, forma=pos[i + 1])
        if tipo == 'amuleto':
            if len(pos) < i + 2: falta('diga a categoria do amuleto', 'pede amuleto Comum')
            return oficio.molde('amuleto', pos[i + 1], pos[i + 2] if len(pos) > i + 2 else None)
        sys.exit('o encanto faz foco e amuleto (a arma, a armadura e o escudo são da forja)')
    if pos[0] == 'ver': print('\n'.join(ver(E, pid)) or 'nada de mesa de runas aqui.'); return
    if pos[0] == 'pede': print(oficio.pede(E, pid, peca(1))); return
    if pos[0] == 'fazer': out = oficio.forjar(E, pid, peca(1), blocos=num('blocos'), nucleo=op.get('nucleo'))['texto']
    elif pos[0] == 'gravar':
        if len(pos) < 3: falta('diga a peça e o feitiço', 'gravar i0007 prender com=anselmo')
        out = gravar(E, pid, pos[1], pos[2], para=op.get('para'), com=op.get('com'), blocos=num('blocos'), nucleo=op.get('nucleo'))['texto']
    elif pos[0] == 'continua': out = oficio.continua(E, pid, pos[1] if len(pos) > 1 else None, blocos=num('blocos'))['texto']
    elif pos[0] == 'larga': out = oficio.larga(E, pid, pos[1] if len(pos) > 1 else falta('diga qual obra largar', 'larga o0001'))['texto']
    elif pos[0] == 'jornal':
        if len(pos) < 2 or not pos[1].isdigit() or int(pos[1]) < 1: falta('diga quantos blocos, em número inteiro', 'jornal 2')
        out = oficio.jornal(E, pid, int(pos[1]), oficio='encanto')['texto']
    else:
        if len(pos) < 2 or not (pos[1] == 'nada' or pos[1].isdigit()): falta(f'diga o nível da mesa de runas, de 0 a {len(W.RUNAS) - 1}, ou "nada"', 'runas 1 "como foi"')
        out = poe_runas(E, E['gente'][pid]['lugar'], None if pos[1] == 'nada' else int(pos[1]), como=pos[2] if len(pos) > 2 else '')
    estado.grava(E)
    print(out)
    print(ato.ultima_linha(E, pid))


if __name__ == '__main__':
    import signal; hasattr(signal, 'SIGPIPE') and signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    main()
