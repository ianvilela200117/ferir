#!/usr/bin/env python3
"""povos.py — MOTOR 10, ETAPA 4b: OS POVOS DO PERSONAGEM (capítulo 19; os números no tabelas_povos.py; o contrato: projeto/ETAPA_4B.md, seções 1, 8 e 12).

  Seis povos: o humano (a medida de todos: é a pessoa de hoje), o anão, o elfo, o meio-orc, o pequenino e o gnomo. O povo mexe nos atributos com a soma igual, dá
  de nenhum a dois traços (vê no escuro, resiste a veneno), uma coragem, um corpo (gente ou miúdo: a armadura é feita para o corpo), uma tendência nos talentos, a vida
  longa e um +2 num teste do ladino. Quem não tem o campo `povo` é humano. O povo não se troca depois de nascer.
  O NÚCLEO (o gravador, o lutador, o talento, a luta) lê a página tabelas_povos direto; este módulo é o que as outras frentes chamam, o que vai à mesa e o que põe a gente
  de outros povos na vila de teste. A lei, medida no banco (provas_povos.py): nenhum povo pesa mais que o Grande Dom, em condição nenhuma.

Uso em código (o que as outras frentes chamam; nada aqui grava, a não ser o na_vila):
  de(p) · tracos(p) (também traços) · ve_no_escuro(p) · coragem(p) · corpo(p) · serve(it, p) · manha(p, teste, pedra=False) · frase(povo)
  nasce(E, pid, registro, povo) · talhe(povo) · gerado(nome, nivel, povo, molde='guerreiro')
  ganchos: pode_vestir(E, pid, iid) · voce(E) · mesa(E) · so_mestre(E) · na_vila(E, vila='vila')
Uso de linha de comando (só olha):
  python3 povos.py lista              os povos, para o jogador escolher
  python3 povos.py ver POVO           os atributos, os traços, o corpo, a tendência, a vida, o teste do ladino
"""
import sys
import tabelas_povos as TP


def _desconhecido(povo): sys.exit(f'povo desconhecido: "{povo}" (os que há: {", ".join(TP.POVOS)})')


# ---------- ler a pessoa ----------
def de(p):
    """o nome do povo da pessoa ("humano" se ela não tem o campo)"""
    v = p.get('povo') if isinstance(p, dict) else None
    return v if isinstance(v, str) and v in TP.POVOS else TP.HUMANO


def _reg(p): return TP.POVOS[de(p)]
def tracos(p): return list(_reg(p).get('tracos') or [])          # os traços do povo (a lista fechada: tabelas.TRACOS_POVO)
traços = tracos
def ve_no_escuro(p): return 'vê no escuro' in tracos(p)          # fora da luta: anda, procura, abre e desarma sem luz (a regra da masmorra)
def coragem(p): return int(_reg(p).get('coragem') or 0)
def corpo(p): return _reg(p).get('corpo') or 'gente'


def serve(it, p):
    """a peça serve no corpo desta pessoa? (só a armadura tem corpo; a mesma conta do estado.serve)"""
    import estado
    return estado.serve(it, p)


def manha(p, teste, pedra=False):
    """o bônus do povo num teste do ladino (tabelas_manha.TESTES; no achar em lugar de pedra também conta o achar_pedra), de 0 a MANHA_TETO"""
    m = TP.MANHA.get(de(p)) or {}
    b = m.get(teste, 0) + (m.get('achar_pedra', 0) if teste == 'achar' and pedra else 0)
    return max(0, min(TP.MANHA_TETO, b))


def frase(povo):
    """a linha que o jogador lê para escolher o povo"""
    r = TP.POVOS.get(povo) or _desconhecido(povo)
    return f"{povo}: {r.get('frase', '')}"


def talhe(povo):
    """o talhe da armadura que serve neste povo: "miúdo" para o corpo miúdo, None para o de gente (as peças do começo do personagem miúdo nascem miúdas)"""
    r = TP.POVOS.get(povo) or _desconhecido(povo)
    return 'miúdo' if r.get('corpo') == 'miúdo' else None


# ---------- nascer ----------
def nasce(E, pid, registro, povo):
    """o registro de quem nasce com este povo: os atributos mais os do povo (a soma não muda), o "povo" e a "idade" (a de adulto do povo mais um d10, pelo dado do mundo).
    Para o personagem: povos.nasce primeiro, depois talento.nasce (a tendência do povo já está no registro)."""
    import estado
    r = TP.POVOS.get(povo) or _desconhecido(povo)
    reg = dict(registro); at = dict(reg['atributos'])
    for k, v in (r.get('mods') or {}).items(): at[k] = at[k] + v
    reg['atributos'] = at; reg['povo'] = povo
    reg['idade'] = r['vida'][0] + estado.sorte(E, f'idade|{pid}').randint(1, TP.IDADE_DADO)
    return reg


def gerado(nome, nivel, povo=TP.HUMANO, molde='guerreiro', **mais):
    """a pessoa GERADA daquele nível e povo, pronta para vestir e lutar (o pessoas.padrao com os atributos do povo, os traços e a coragem dele): a mesma que o
    estado.lutador dá de quem nasceu com o povo. O humano é o pessoas.padrao de hoje, sem tirar nem pôr."""
    import pessoas
    r = TP.POVOS.get(povo) or _desconhecido(povo)
    p = pessoas.padrao(nome, nivel, molde=molde, **mais)
    for k, v in (r.get('mods') or {}).items(): p['atributos'][k] += v
    if r.get('tracos'): p['tracos'] = list(p.get('tracos') or []) + [t for t in r['tracos'] if t not in (p.get('tracos') or [])]
    if r.get('coragem'): p['coragem'] = r['coragem']
    return p


# ---------- o que se diz de um povo ----------
def _sinal(v): return f"+{v}" if v > 0 else f"−{-v}"


def diz(povo):
    """as linhas que contam um povo ao jogador (o `ver`), em português simples"""
    r = TP.POVOS.get(povo) or _desconhecido(povo)
    L = [f"{povo.upper()}: {r.get('frase', '')}."]
    mods = ', '.join(f"{k} {_sinal(v)}" for k, v in (r.get('mods') or {}).items() if v)
    L.append(f"  Atributos (a soma é a mesma do humano): {mods}." if mods else '  Atributos: os de quem nasce, sem tirar nem pôr.')
    if r.get('tracos'): L.append('  Traços: ' + ' · '.join(f"{t}: {TP.TRACOS[t]}" for t in r['tracos']) + '.')
    if r.get('coragem'): L.append(f"  Coragem {_sinal(r['coragem'])} no teste de coragem (o pavor do dragão, o susto).")
    L.append('  Corpo: ' + ('miúdo. Veste a armadura miúda; a de gente grande só serve depois que um ferreiro a ajusta (1 bloco). A arma e o escudo servem em todo corpo.'
                            if r.get('corpo') == 'miúdo' else 'de gente. Veste a armadura de gente; a miúda só serve depois que um ferreiro a ajusta.'))
    if r.get('a_favor') or r.get('contra'):
        import tabelas_talento as TT
        nome = lambda c: TT.O_QUE.get(c, c).split(' (')[0]
        L.append('  Ao nascer: ' + '; '.join(x for x in (f"mais jeito para {nome(r['a_favor'])} (o dado do talento rola duas vezes e vale o melhor)" if r.get('a_favor') else '',
                                                          f"menos para {nome(r['contra'])} (duas vezes, vale o pior)" if r.get('contra') else '') if x) + '.')
    a, v, m = r['vida']; L.append(f"  Vida: adulto aos {a}, velho aos {v}, vive até {m} anos.")
    mh = TP.MANHA.get(povo) or {}
    if mh: L.append('  No ofício do ladino: ' + '; '.join(f"{_sinal(q)} em {TP.MANHA_DIZ.get(t, t)}" for t, q in mh.items()) + '.')
    return L


def _diz_pessoa(p):
    """o que o povo põe na linha de quem é de outro povo (a mesa: o Você)"""
    pv = de(p); r = TP.POVOS[pv]; partes = []
    if r.get('corpo') == 'miúdo': partes.append('corpo miúdo (a armadura de gente grande não serve até um ferreiro ajustar)')
    if 'vê no escuro' in (r.get('tracos') or []): partes.append('vê na penumbra (de perto, o escuro pesa a metade; anda, procura, abre e desarma sem luz)')
    if 'resiste a veneno' in (r.get('tracos') or []): partes.append('o veneno pega pela metade')
    if r.get('coragem'): partes.append(f"coragem {_sinal(r['coragem'])} diante do que apavora")
    partes += [f"{_sinal(q)} em {TP.MANHA_DIZ.get(t, t)}" for t, q in (TP.MANHA.get(pv) or {}).items()]
    return partes


# ---------- os ganchos ----------
def pode_vestir(E, pid, iid):
    """antes de pôr uma peça em uso (o ato.vestir chama): '' se pode; senão, a frase da recusa (a armadura de outro corpo não serve até ser ajustada)"""
    import estado
    p = E['gente'].get(pid); it = E['itens']['itens'].get(iid)
    if not isinstance(p, dict) or not isinstance(it, dict) or estado.serve(it, p): return ''
    de_quem = 'gente miúda' if it.get('talhe') == 'miúdo' else 'gente grande'
    return f"{it['nome'][0].upper() + it['nome'][1:]} é de {de_quem}: não serve no corpo de {p['nome']}. Um ferreiro a ajusta (`oficio.py ajustar {iid} para={pid}`)."


def voce(E):
    """o povo do personagem numa linha (no "Você"), só para quem tem algo de novo: o de outro povo, ou o que nasceu com a idade escrita. O humano de hoje: nada (a MESA sai igual)"""
    import estado
    pid = estado.eu(E); p = E['gente'].get(pid) if pid else None
    if not isinstance(p, dict) or p.get('estado') != 'vivo': return []
    pv = de(p); idade = p.get('idade'); anos = f", {idade} anos" if isinstance(idade, int) else ''
    if pv == TP.HUMANO: return [f"Do povo dos humanos{anos}: a medida de todos."] if anos else []
    return [f"Do povo dos {TP.PLURAL[pv]}{anos}: " + '; '.join(_diz_pessoa(p)) + '.']


def mesa(E):
    """quem está aqui e é de outro povo, numa linha (o "Quem está aqui" corta a lista em 12 nomes: esta linha diz todos os de outro povo). Sem ninguém assim aqui: nada"""
    import estado
    pid = estado.eu(E); p = E['gente'].get(pid) if pid else None
    if not isinstance(p, dict) or estado.fora(E, pid): return []
    xs = []
    for k, q in E['gente'].items():
        if k == pid or q.get('estado') != 'vivo' or q.get('lugar') != p['lugar'] or estado.fora(E, k) or de(q) == TP.HUMANO: continue
        pv = de(q); s = (q.get('sobre') or '').split(';')[0].split(',')[0].strip().lower()
        xs.append(f"{q['nome']} ({s if s in TP.FORMAS.get(pv, ()) else 'do povo dos ' + TP.PLURAL[pv]})")      # o "sobre" que começa pelo povo diz se é ele ou ela
    return [f"De outros povos, aqui: {', '.join(xs)}."] if xs else []


def so_mestre(E): return []          # o povo não tem segredo: o que ele dá está na mesa e no `povos.py ver`


# ---------- a vila de teste ----------
def _peca(tipo, qual, cat, cobre, de_quem, dono):
    from itens import item
    nome = dict(arma=qual, escudo='escudo').get(tipo) or ('elmo de ' + qual if cobre == ['cabeça'] else 'armadura de ' + qual)
    return item(tipo, cat, f"{nome.capitalize()} de {de_quem}", familia=qual if tipo == 'arma' else None, material=qual if tipo == 'armadura' else None, cobre=cobre, dono=dono)


def na_vila(E, vila='vila'):
    """ACRESCENTA à vila de teste que já existe (só por eventos "gera"; nada se recria) a gente de outros povos (Durva, Brasco, Ilvena e Nena, com os talentos e os dons
    rolados com a tendência do povo), a gente do lugar (o `povos` de Pedra Rasa) e as armaduras miúdas na prateleira da loja. Recusa, com a frase e antes de gravar
    qualquer coisa, se já foi posto. Devolve as linhas que contam o que pôs."""
    import estado, talento
    from itens import item
    from pessoas import padrao
    from vila_teste import treino_da_mao
    V = TP.VILA; l = E['lugares'].get(vila)
    if not isinstance(l, dict) or l.get('tipo') != 'vila': sys.exit(f'não há a vila "{vila}" neste mundo: a gente de outros povos só se acrescenta à vila de teste')
    ja = [V_[1] for V_ in V['gente'] if V_[0] in E['gente']]
    if l.get('povos') is not None or ja:
        sys.exit(f"{l['nome']} já tem a gente de outros povos" + (f" ({', '.join(ja)})" if ja else '') + ': não se acrescenta duas vezes')
    estado.sem_luta(E); L = []
    # 1 a gente do lugar (as frações de cada povo)
    estado.aplica(E, 'gera', [['lugar', vila, 'povos', 'poe', dict(V['povos'])]], onde=vila, texto=f"a gente {estado.de(E, vila)}: a maioria humana, e alguns de outros povos")
    L.append(f"A gente {estado.de(E, vila)}: em cada 100, " + ', '.join(f"{round(100 * q)} {TP.PLURAL[pv] if round(100 * q) > 1 else pv}" for pv, q in V['povos'].items()) + '.')
    # 2 a gente de outros povos, com o que sabem e o que vestem
    nomes = []
    for pid, nome, pv, idade, sobre, nivel, molde, grau, maestria, prata, pecas in V['gente']:
        r = dict(nome=nome, nivel=nivel, atributos=padrao(nome, nivel, molde=molde)['atributos'], lugar=vila, grau_oficio=grau, maestria=dict(maestria),
                 treino=treino_da_mao(maestria), moedas=prata, sobre=sobre)
        r = nasce(E, pid, r, pv); r['idade'] = idade
        estado.aplica(E, 'gera', [['pessoa', 'nasce', pid, talento.nasce(E, pid, r)]], onde=vila, quem=[pid], texto=f'{nome}, {sobre}')
        if pecas:
            s0 = E['itens']['seq']
            estado.aplica(E, 'gera', [['item', 'nasce', _peca(t, q, c, cb, nome, pid)] for t, q, c, cb, _ in pecas], onde=vila, quem=[pid], texto=f'as peças de {nome}')
            estado.aplica(E, 'gera', [['item', f'i{s0 + k + 1:04d}', 'uso', 'poe', uso] for k, (_, _, _, _, uso) in enumerate(pecas) if uso], onde=vila, quem=[pid], texto=f'{nome} se veste')
        nomes.append(f"{nome} ({sobre.split(';')[0]}, {idade} anos)")
    L.append('Gente de outros povos: ' + ', '.join(nomes) + '.')
    # 3 a prateleira: as armaduras miúdas (só onde há loja: a vila de teste tem)
    if isinstance(l.get('alvo_pecas'), dict):
        evs = [item(t, c, material=m, cobre=cb, talhe='miúdo', onde=vila) for t, m, c, cb in V['loja']]
        estado.aplica(E, 'gera', [['item', 'nasce', x] for x in evs], onde=vila, texto='a loja põe na prateleira armaduras miúdas, para a gente pequena')
        L.append('Na prateleira da loja: ' + ', '.join(x['nome'] for x in evs) + ' (para o corpo miúdo).')
    P = estado.valida(E)
    if P: sys.exit('A GENTE DE OUTROS POVOS ENTROU TORTA NA VILA (não foi gravada):\n  ' + '\n  '.join(P))
    return L


# ---------- o comando ----------
def main(a=None):
    a = sys.argv[1:] if a is None else a
    if a[:1] == ['lista']:
        for k in TP.POVOS: print(frase(k))
        print('\nPara ver um povo inteiro: python3 povos.py ver POVO')
    elif a[:1] == ['ver'] and len(a) > 1: print('\n'.join(diz(a[1])))
    else: print(__doc__)


if __name__ == '__main__':
    main()
