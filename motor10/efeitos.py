#!/usr/bin/env python3
"""efeitos.py — MOTOR 10, A PARTE 2, FASE 1b: OS EFEITOS DE UMA PEÇA, EM PALAVRAS (o catálogo: tabelas_efeitos.py; o contrato: projeto/etapa_efeitos/DESENHO.md, seção 4).

A peça nunca guarda o número do efeito: ele sai da categoria que ela rende agora PARA O DONO QUE A USA (a ficha dele: a sob medida na mão de outro rende uma abaixo; a que dorme
na sintonia tem os efeitos dormindo; o apelão de regra que não é o acordado dorme sozinho; a quebrada não tem efeito). Este comando só olha: diz cada efeito com o número de hoje, a força, o cheio, os usos gastos, e "no seu nível, perto de +X pontos de vitória"
(a tabela do banco por nível: 10, 20, 50 e 150; no nível baixo os % rendem menos, e o crítico rende o mesmo).

Uso:
  python3 efeitos.py ver ITEM [nivel=N]        os efeitos da peça (do Livro de Itens do mundo, ou do solto), com o número da categoria dela e o que valem no nível do dono
  python3 efeitos.py lista [TIPO] [CATEGORIA]  o catálogo de luta (TIPO: arma, armadura, escudo, foco, amuleto), com os números de cada categoria (ou só os da CATEGORIA)
(Na fase 5: `efeitos.py semente ITEM`, o que a semente dá às peças da história; só olha.)
"""
import os, sys
import tabelas as T
import tabelas_efeitos as TE
import tabelas_oficio as O


def _cat(it):
    return it['cat'] if isinstance(it.get('cat'), int) and not isinstance(it.get('cat'), bool) else 0


def rende_de(E, it):
    """o que a peça RENDE agora para o dono que a usa (pessoas.ficha: a categoria, se dorme na sintonia, se o apelão de regra dela dorme), ou None se ninguém vivo a usa"""
    import estado
    from pessoas import ficha
    dono = it.get('dono')
    if not it.get('uso') or not dono or (E['gente'].get(dono) or {}).get('estado') != 'vivo': return None
    try: return ficha(estado.lutador(E, dono)).get('rende', {}).get(it.get('id'))
    except (SystemExit, Exception): return None              # (sem a ficha, o número é o da categoria da peça)


def linhas(it, nivel=None, dono=None, rende=None):
    """as linhas dos efeitos de uma peça: a frase com o número da categoria que ela RENDE para o dono (rende: o que a ficha dele diz; sem ele, a categoria da peça; o cheio, o da
    de cima), a força, os usos gastos e o que vale no nível do dono; a que dorme na sintonia e o apelão que dorme (um acordado por pessoa) aparecem como dormindo"""
    import itens as IT
    c0 = _cat(it); c = rende['cat'] if rende and not rende.get('quebrada') and not rende.get('dorme') else c0; L = []
    if it.get('dur') and it['dur'][0] <= 0: L.append('(a peça está quebrada: nenhum efeito vale até ela ser consertada)')
    elif rende and rende.get('dorme'): L.append(f'(a peça DORME na sintonia do dono: rende uma categoria abaixo, e os efeitos dela dormem; os números abaixo são os da peça {TE.FEM[c0]} acordada)')
    elif rende and c != c0: L.append(f'(na mão do dono, a peça rende uma categoria abaixo: os números abaixo são os da peça {TE.FEM[c]})')
    for e in it.get('efeitos') or []:
        k = e.get('chave')
        if k in TE.EFEITOS:
            x = TE.EFEITOS[k]; v = TE.pontos(k, c, nivel or 50, bool(e.get('cheio')))
            s = f"- {IT.frase_efeito(e, c)} [{TE.forca(k, c + (1 if e.get('cheio') else 0)) if x['tipo'] == 'numero' else x['forca']}"
            s += (f"; o cheio se mede na faixa da categoria de cima ({T.CATS[min(c + 1, len(T.CATS) - 1)]})" if e.get('cheio') else '') + ']'
            if x.get('usos') == 'dia' and isinstance(e.get('gasto'), dict): s += f" (gasto no Dia {e['gasto'].get('dia')})"
            if v is not None: s += f" · no seu nível, perto de {v:+.1f} pontos de vitória".replace('.', ',')
            if TE.apelao_de_regra(k):
                s += ' · apelão de regra: a peça ocupa 2 lugares na sintonia, e só um apelão de regra fica acordado por pessoa'
                if rende and rende.get('apelao_dorme'): s += ' · ESTE DORME: o apelão acordado do dono é o de outra peça (a de categoria maior; no empate, a arma, o escudo, a armadura, o foco, o amuleto); a peça ocupa 1 lugar e o resto dela vale'
        elif k in TE.LEGADO: s = f"- {IT.frase_efeito(e, c)} [" + ('fica na peça que já o tem: a resposta 2a do jogador; nenhuma peça nova o ganha' if k == 'critico_19'
                                                              else 'a Sangria Comum de antes: fica na peça que já o tem (na peça Comum, a entrada da fase 1b o troca pela Sangria, igual); nenhuma peça nova o ganha') + ']'
        elif k in O.FERRAMENTA_EFEITOS: s = f"- {IT.frase_efeito(e, c)} [efeito de ferramenta: {O.FERRAMENTA_EFEITOS[k][0]}]"
        else: s = f"- {k} (fora do catálogo)"
        L.append(s)
    if it.get('efeitos_livres'): L.append(f"- e {it['efeitos_livres']} por escolher" + (f" ({it['cheios_livres']} cheio(s))" if it.get('cheios_livres') else '') + f" (`oficio.py efeito {it.get('id', 'ITEM')}` mostra o que cabe)")
    if not L: L.append('(nenhum efeito)')
    return L


def lista(tipo=None, cat=None):
    """o catálogo de luta: cada efeito, a força (a porta), as peças e os números de cada categoria (ou de uma)"""
    L = []
    for k, x in TE.EFEITOS.items():
        if tipo and tipo not in x['pecas']: continue
        if x['tipo'] == 'numero':
            nums = [TE.diz_valor(k, v) if v is not None else '—' for v in x['valores']]
            corpo = (f"{T.CATS[cat]}: {nums[cat]}" if cat is not None else ' · '.join(f"{T.CATS[i][:3]} {n}" for i, n in enumerate(nums)))
            L.append(f"{x['nome']} (`{k}`, número; {', '.join(x['pecas'])}): {x['faz'].format(v='N', contra='o tipo escolhido')} — {corpo} · medida: {x['medida']}")
        else:
            L.append(f"{x['nome']} (`{k}`, {x['forca']}, porta: a peça {TE.FEM[TE.FORCA_PORTA[x['forca']]]}; {', '.join(x['pecas'])}): {x['faz']} · medida: {x['medida']}")
    return L


def main(a=None):
    a = sys.argv[1:] if a is None else list(a)
    if not a: print(__doc__); return
    op = dict(x.split('=', 1) for x in a if '=' in x); pos = [x for x in a if '=' not in x]
    if pos[0] == 'lista':
        from itens import cat_i
        tipo = pos[1] if len(pos) > 1 and pos[1] in TE.PECAS_LUTA else None
        cat = cat_i(pos[-1]) if len(pos) > 1 and pos[-1] not in TE.PECAS_LUTA else None
        print('\n'.join(lista(tipo, cat))); return
    if pos[0] == 'ver' and len(pos) > 1:
        import itens, estado
        mundo = os.path.exists(os.path.join(estado.pasta(), 'relogio.json'))
        rende = None
        if mundo:
            E = estado.carrega(); it = E['itens']['itens'].get(pos[1]) or sys.exit(f'não há o item "{pos[1]}" no Livro de Itens do mundo (itens.py ver)')
            dono = E['gente'].get(it.get('dono')) if it.get('dono') else None; rende = rende_de(E, it)
        else:
            it = itens.carrega()['itens'].get(pos[1]) or sys.exit(f'não há o item "{pos[1]}" no Livro de Itens solto (itens.py ver)'); dono = None
        nv = int(op['nivel']) if op.get('nivel', '').isdigit() else (dono or {}).get('nivel', 50)
        print(f"{itens.rotulo(it)} · a porta: {TE.forca_da_cat(_cat(it))}; o teto de efeitos: {it.get('teto_efeitos') or O.efeitos_max(_cat(it))}"
              + (f" · de {dono['nome']}, nível {nv}" if dono else f" · no nível {nv}") + ('' if not dono or rende else ' (fora de uso: os números são os da categoria da peça)'))
        print('\n'.join(linhas(it, nv, dono, rende))); return
    print(__doc__)


if __name__ == '__main__':
    import signal; hasattr(signal, 'SIGPIPE') and signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    main()
