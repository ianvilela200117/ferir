#!/usr/bin/env python3
"""itens.py — MOTOR 10: O LIVRO DE ITENS. Uma peça que não está aqui não existe.

Toda arma, armadura, escudo e núcleo é um registro: o que é, de que categoria, quanto aguenta, o que faz, de quem é, quem fez e o que viveu.
A ficha de luta de quem veste sai DAQUI (pessoas.py): ninguém digita ataque e dano.
  HAVENDO UM MUNDO (a pasta de MOTOR10_MUNDO, ou `mundo/`), o Livro é o do mundo (itens.json do save): `ver` e `janela` leem dele, e `nova`, `dono` e
  `conserta` entram por um evento "mestre" (o gravador é um só). Sem mundo, vale o Livro solto (dados/itens.json), que só serve à luta fora do mundo.

Uso:
  python3 itens.py nova arma FAMILIA CATEGORIA "Nome" [dono=ID] [onde=LUGAR] [feito=Nome] [dia=N] [efeito=chave[:valor]]... [sob=Dono:grau]
  python3 itens.py nova armadura MATERIAL CATEGORIA "Nome" [cobre=tronco,braços,pernas] ...   (elmo: cobre=cabeça)
  python3 itens.py nova escudo CATEGORIA "Nome" ...
  python3 itens.py nova nucleo CATEGORIA "Nome" [de=ESPECIE] [dono=ID] [onde=LUGAR]     o núcleo de um chefe (o que a obra Épica ou maior pede)
  python3 itens.py nova foco FORMA CATEGORIA "Nome" ...     (etapa da magia) o foco de quem lança: varinha, cajado, símbolo, talismã
  python3 itens.py nova amuleto CATEGORIA "Nome" ...        o amuleto: a armadura contra a magia (no pescoço; um só)
  python3 itens.py nova elixir POCAO CATEGORIA "Nome" ...   a poção do Épico para cima (abaixo disso, a poção é bem: cura:0)
  python3 itens.py nova escrito CATEGORIA "Nome" feiticos=seta,luz ...     o escrito que ensina feitiços
  python3 itens.py nova gazua CATEGORIA ["Nome"] ...       (etapa 4b) a ferramenta do ladino (não se veste: o teste usa a melhor que a pessoa leva)
  python3 itens.py nova chave ["Nome"] abre=SALA_A|SALA_B ...    a chave de uma porta (ou abre=SALA: o guardado da sala); abre sem teste
  python3 itens.py nova armadura MATERIAL CATEGORIA ["Nome"] talhe=miúdo ...    a armadura de talhe miúdo (o pequenino, o gnomo)
  python3 itens.py ver [dono=ID]            a lista
  python3 itens.py janela ID                a janela do item (a que aparece na cena)
  python3 itens.py dono ID PESSOA ["o que houve"]     a peça muda de mão (entra na história dela)
  python3 itens.py conserta ID [N]          devolve N de durabilidade (sem N: toda)
FAMILIA: punho adaga espada maça machado martelo lança montante alabarda malho arco besta · MATERIAL: couro malha placa
CATEGORIA: Comum Incomum Raro Épico Único Lendário Mítico Primordial
"""
import json, os, sys
import tabelas as T
import tabelas_mundo as M
from tabelas import CATS, MULT, RD, BON, DUR, FAMILIAS, MATERIAIS, PARTES, PEDE_PESO, DUAS_MAOS

AQUI = os.path.dirname(os.path.abspath(__file__))
ARQ = os.path.join(AQUI, 'dados', 'itens.json')

# OS EFEITOS (a parte 2): o catálogo de luta (fase 1b) mora no tabelas_efeitos.EFEITOS (os 21 de número e os 26 de regra, com a força, a porta, os 8 valores e a frase);
# os doze de ferramenta (fase 1a), no tabelas_oficio.FERRAMENTA_EFEITOS. Aqui entram todos, com a frase e os tipos de peça. Efeito que não está aqui não entra numa peça.
# Os de antes (o `critico_19`, o `sangra`) ficam só na peça que já os tem (a resposta 2a): o critico_19 para sempre; o sangra (a Sangria Comum de antes) também, acima da Comum,
# e na peça Comum até o evento de entrada da 1b, que o converte na chave `sangria` (igual). Nenhuma peça nova os ganha.
def _efeitos_do_catalogo():
    import tabelas_efeitos as TE, tabelas_oficio as O
    d = {k: (v['faz'].replace('{v}', '{valor}').replace('{contra}', 'o tipo escolhido'), tuple(v['pecas'])) for k, v in TE.EFEITOS.items()}
    d.update({k: (v['faz'], tuple(v['pecas'])) for k, v in TE.LEGADO.items()})
    d.update({k: (v[3], ('ferramenta',)) for k, v in O.FERRAMENTA_EFEITOS.items()})
    return d
EFEITOS = _efeitos_do_catalogo()
ESCOLHE_NAO = ('pesa', 'critico_19', 'sangra')      # o que não se escolhe: o defeito (pesa) e os de antes (o que nasceu, nasceu)


NOME_EFEITO = dict(mao_de_medida='mão de medida', poupa_ferro='poupa-ferro', tempera='têmpera', molde='molde de mestre', degrau='degrau emprestado')       # o nome à mesa


def frase_efeito(e, cat, nome=True):
    """a frase de um efeito da peça, com o número da categoria que ela rende (o de luta: tabelas_efeitos.valor; o de ferramenta: tabelas_oficio.valor_ferramenta; cheio, o da
    categoria de cima; o `devolve N` de antes, que a entrada da 1b converte, o número gravado), e as marcas: (cheio), (degrau emprestado). nome: o de ferramenta começa pelo nome dele"""
    import tabelas_oficio as O, tabelas_efeitos as TE
    k = e.get('chave')
    if k in TE.EFEITOS:
        if k == 'devolve' and e.get('valor') is not None: txt = f"Devolve: quem golpeia o dono corpo a corpo leva {e['valor']} (o devolve de antes; a entrada da 1b o converte no {TE.diz_valor(k, TE.valor(k, cat))} da categoria)"
        else: txt = TE.frase(k, cat, bool(e.get('cheio')), TE_contra(e.get('contra')))
        txt = txt if nome else txt.split(': ', 1)[-1]
    else:
        txt = EFEITOS[k][0] if k in EFEITOS else k
        v = O.valor_ferramenta(k, cat, bool(e.get('cheio'))) if k in O.FERRAMENTA_EFEITOS else e.get('valor', '')
        txt = txt.format(valor=v if v is not None else '')
        if k in O.FERRAMENTA_EFEITOS and nome: txt = f"{NOME_EFEITO.get(k, k)}: {txt}"
    return txt + (' (cheio: o número da categoria de cima)' if e.get('cheio') else '') + (' (do degrau emprestado)' if e.get('emprestado') else '')


def TE_contra(c): return {'bicho': 'o bicho', 'morto': 'o morto (quem não tem vida)', 'povo': 'o povo (goblin, orc...)', 'gente': 'a gente', 'dragão': 'o dragão'}.get(c, c)


def curta_efeito(e, cat):
    """o efeito em poucas palavras, para a linha das peças na MESA: "prumo 2 (cheio)", "afinada", "remendo 8"; os de luta: "gume +15%", "crítico 20/7 (cheio)", "Escancara" """
    import tabelas_oficio as O, tabelas_efeitos as TE
    k = e.get('chave')
    if k in TE.EFEITOS:
        x = TE.EFEITOS[k]; v = TE.valor(k, cat, bool(e.get('cheio')))
        if x['tipo'] == 'regra': base = x['nome']
        elif k == 'sangria': base = 'Sangria ' + ('5 rodadas na ferida' if v == 'ferida' else f"{'1/3' if abs(v[0] - 1 / 3) < 1e-9 else '1/4' if v[0] == 0.25 else '1/5'} por {v[1]}")
        elif k == 'robusta': base = f"Robusta +{v[0]}"
        elif k in ('aturdir',): base = f"Aturdir {v}"
        elif k in ('medo', 'temivel'): base = f"{x['nome']} {v}"
        elif k == 'segundo_golpe': base = f"Segundo Golpe ×{v}"
        else: base = f"{x['nome']} {'+' if k in ('gume', 'certeira', 'cacadora', 'chama', 'foco_certeiro', 'guarda', 'firmeza', 'coragem') else ''}{TE.diz_valor(k, v)}"
        if k == 'cacadora' and e.get('contra'): base += f" contra {e['contra']}"
        return base + (' (cheio)' if e.get('cheio') else '') + (' (emprestado)' if e.get('emprestado') else '')
    if k not in O.FERRAMENTA_EFEITOS: return frase_efeito(e, cat)
    v = O.valor_ferramenta(k, cat, bool(e.get('cheio'))); v = O.REMENDO_BLOCO if k == 'remendo' else v
    return NOME_EFEITO.get(k, k) + (f' {v}' if v is not None else '') + (' (cheio)' if e.get('cheio') else '') + (' (emprestado)' if e.get('emprestado') else '')


def efeito_erro(it, e, novo=False, legado=True):
    """(a parte 2, fase 1b; DESENHO 9.5) o que um efeito de LUTA pede para estar nesta peça (None: certo): o tipo de peça e a arma certa, a porta pela força (com o degrau
    emprestado, uma acima: só com o direito que a peça trouxe ao nascer, e em peça de até 4 efeitos), a Caçadora com `contra`, o cheio só em efeito de número; um apelão de regra
    por peça; uma porta adiantada por peça (o degrau emprestado; o vidro e a Sede chegam na fase 5; o cheio não conta). Os de antes: o `critico_19` sempre (a resposta 2a: o que
    nasceu, nasceu), o `sangra` na peça acima da Comum (a Sangria Comum de antes: a entrada só converte o da Comum, que vira a Sangria igual), e, enquanto `legado` (até o
    evento de entrada da 1b), o `sangra` da Comum e o `devolve N` fixo (de 1 ao teto da categoria). Nenhum de antes ENTRA em peça (`novo`), antes ou depois da entrada: as peças
    novas seguem o catálogo (a resposta 2a). O Crítico não entra na peça que tem o critico_19 (um efeito só). `novo`: o efeito está entrando."""
    import tabelas_efeitos as TE, tabelas_oficio as O
    k = e.get('chave'); cat = it['cat'] if isinstance(it.get('cat'), int) and not isinstance(it.get('cat'), bool) else 0; tipo = it.get('tipo')
    if k in TE.LEGADO:
        if tipo not in TE.LEGADO[k]['pecas']: return f'o efeito "{k}" não vale em {tipo}'
        if set(e) - {'chave'}: return f'o efeito de antes "{k}" não leva nada além da chave'
        if k == 'sangra' and not legado and cat == 0: return 'o `sangra` de antes, na peça Comum, virou a Sangria Comum na entrada da fase 1b: a peça leva {"chave": "sangria"}'
        if novo: return f'"{k}" é o efeito de antes: fica só na peça que já o tem, e as peças novas seguem o catálogo de luta (o Crítico pela categoria; a Sangria)'
        return None
    if k not in TE.EFEITOS: return None
    x = TE.EFEITOS[k]
    if k == 'critico' and any(isinstance(o, dict) and o.get('chave') == 'critico_19' for o in it.get('efeitos') or []):
        return 'a peça já tem o crítico de antes (19/11): o Crítico e o critico_19 são um efeito só (P5: vale a melhor faixa), e o lugar se perderia'
    if k == 'devolve' and e.get('valor') is not None:
        if not legado: return 'o devolve fixo de antes virou % na entrada da fase 1b: a peça leva {"chave": "devolve"} (o número sai da categoria)'
        if not (isinstance(e['valor'], int) and not isinstance(e['valor'], bool) and 1 <= e['valor'] <= TE.devolve_fixo_max(cat)): return f'"devolve" (o de antes) numa peça {T.CATS[cat]} vai de 1 a {TE.devolve_fixo_max(cat)}'
        if novo: return 'o devolve de antes (com valor) não entra em peça: o de agora é {"chave": "devolve"}, o % da categoria'
        sobra = set(e) - {'chave', 'valor'}
        return f'o devolve de antes é {{chave, valor}} (veio também: {", ".join(sorted(sobra))})' if sobra else None
    sobra = set(e) - {'chave', 'cheio', 'emprestado', 'contra', 'gasto'}
    if sobra: return f'o efeito de luta "{k}" é {{chave, cheio?, emprestado?, contra?}} (veio também: {", ".join(sorted(sobra))}): o número nunca se guarda, sai da categoria'
    emp = bool(e.get('emprestado'))
    erro = TE.cabe(k, tipo, cat, it.get('familia'), emp)
    if erro: return erro
    if e.get('cheio') is not None and e['cheio'] is not True: return 'o cheio é True, ou não vem'
    if e.get('emprestado') is not None and e['emprestado'] is not True: return 'o emprestado é True, ou não vem'
    if e.get('cheio') and x['tipo'] != 'numero': return f'{x["nome"]} é de regra: o cheio só vale em efeito de número'
    if k == 'cacadora' and e.get('contra') not in TE.CONTRA: return f'a Caçadora pede contra quem (contra: {", ".join(TE.CONTRA)})'
    if k != 'cacadora' and e.get('contra') is not None: return f'só a Caçadora leva `contra`'
    if e.get('gasto') is not None and not (isinstance(e['gasto'], dict) and isinstance(e['gasto'].get('dia'), int) and isinstance(e['gasto'].get('n'), int) and e['gasto']['n'] >= 1): return 'o gasto é {dia, n}'
    if e.get('gasto') is not None and x.get('usos') != 'dia': return f'{x["nome"]} não tem uso do dia para gastar'
    if emp:
        if not it.get('degrau'): return f'{x["nome"]} emprestado pede o degrau emprestado, que a peça traz ao nascer (a ferramenta que o dá em uso na forja)'
        if TE.cabe(k, tipo, cat, it.get('familia')) is None: return f'{x["nome"]} já cabe na porta da peça: não é do degrau emprestado'
        if any(isinstance(o, dict) and o.get('emprestado') and o is not e for o in it.get('efeitos') or []): return 'a peça já tem um efeito do degrau emprestado: a porta adiantada é uma só'
        livres = it.get('efeitos_livres') or 0
        if len(it.get('efeitos') or []) + (max(livres, 1) if novo else livres) > O.DEGRAU_ATE: return f'o degrau emprestado só entra em peça de até {O.DEGRAU_ATE} efeitos'
    if TE.apelao_de_regra(k) and any(isinstance(o, dict) and o is not e and o.get('chave') != k and TE.apelao_de_regra(o.get('chave')) for o in it.get('efeitos') or []):
        return f'{x["nome"]} é apelão de regra, e a peça já leva um: um apelão de regra por peça'
    return None


FORMAS_FEM = ('varinha',)   # as formas de foco de nome feminino (a categoria concorda: "varinha Rara", "cajado Raro")


# a língua da mesa: a categoria concorda com o nome da peça ("espada Rara", "arco Raro"), e não se diz duas vezes ("espada Rara", e não "espada Rara (Raro)")
FEM = ['Comum', 'Incomum', 'Rara', 'Épica', 'Única', 'Lendária', 'Mítica', 'Primordial']       # a categoria, quando o nome que vem antes é feminino
FEMININAS = ('adaga', 'espada', 'maça', 'lança', 'alabarda', 'besta')                          # as armas de nome feminino (a armadura também é; o elmo, o escudo e o núcleo, não)


def rotulo(it, *mais):
    """o nome de uma peça com a categoria entre parênteses, e o que mais vier ("Adaga da Cira (Comum, 10/10)"). Se o nome já diz a categoria, ela não se repete ("espada Rara (30/30)")."""
    c = it['cat']; partes = ([] if str(it['nome']).endswith((CATS[c], FEM[c])) else [CATS[c]]) + [str(x) for x in mais if x]
    return it['nome'] + (f" ({', '.join(partes)})" if partes else '')


def cat_i(c):
    """'Raro' ou 2 → 2"""
    if isinstance(c, int):
        if not 0 <= c < len(CATS): sys.exit(f'categoria fora da tabela: {c} (vai de 0, Comum, a 7, Primordial)')
        return c
    n = c.strip().lower().replace('epico', 'épico').replace('unico', 'único').replace('lendario', 'lendário').replace('mitico', 'mítico')
    for i, x in enumerate(CATS):
        if x.lower() == n: return i
    sys.exit(f'categoria desconhecida: "{c}" (use: {", ".join(CATS)})')


def item(tipo, cat, nome=None, familia=None, material=None, cobre=None, efeitos=None, sob=None, **mais):
    """monta um registro de item (sem gravar). É o que os testes e o `nova` usam.
    Etapa 4b: a GAZUA (`item('gazua', cat)`), a CHAVE (`item('chave', 0, nome, abre='SALA_A|SALA_B')`) e o TALHE da armadura (o corpo para que foi feita: `talhe='miúdo'`; sem ele, de gente)."""
    c = cat_i(cat)
    if tipo in ('gazua', 'chave'): return _ladino(tipo, c, nome, efeitos, sob, familia, material, cobre, mais)
    talhe = mais.pop('talhe', None)
    if talhe not in (None, 'gente', 'miúdo'): sys.exit(f'talhe desconhecido: "{talhe}" (a armadura é de gente, ou miúda: talhe=miúdo)')
    if talhe == 'miúdo' and tipo != 'armadura': sys.exit('só a armadura tem talhe (a arma e o escudo servem em todo corpo)')
    if tipo == 'nucleo':                                    # o NÚCLEO: não se veste, não gasta, não leva efeito. É contado no mundo, com dono e lugar.
        if efeitos or sob or familia or material or cobre: sys.exit('o núcleo não leva efeito, sob medida, família nem material: só a categoria, o nome e de que bicho veio (de=)')
        it = dict(tipo='nucleo', cat=c, nome=nome or f'núcleo {CATS[c]}', dur=[T.NUCLEO_DUR, T.NUCLEO_DUR], dono=None, onde=None, de=mais.pop('de', None), historia=[])
        it.update(mais)
        return it
    if tipo in ('foco', 'amuleto', 'elixir', 'escrito'): return _magia(tipo, c, nome, efeitos, sob, familia, material, cobre, mais)
    if tipo == 'ferramenta': return _ferramenta(c, nome, efeitos, sob, familia, material, cobre, mais)
    it = dict(tipo=tipo, cat=c, nome=nome, dur=[DUR[c], DUR[c]], efeitos=list(efeitos or []), sob_medida=sob, historia=[], dono=None, onde=None)
    if tipo == 'arma':
        if familia not in FAMILIAS: sys.exit(f'família de arma desconhecida: "{familia}" (use: {", ".join(FAMILIAS)})')
        it['familia'] = familia; it['nome'] = nome or f'{familia} {(FEM if familia in FEMININAS else CATS)[c]}'
    elif tipo == 'armadura':
        if material not in MATERIAIS: sys.exit(f'material desconhecido: "{material}" (use: {", ".join(MATERIAIS)})')
        it['material'] = material; it['cobre'] = list(cobre or ['tronco', 'braços', 'pernas'])
        for p in it['cobre']:
            if p not in PARTES: sys.exit(f'parte desconhecida: "{p}" (use: {", ".join(PARTES)})')
        it['nome'] = nome or ((f'elmo miúdo de {material} {CATS[c]}' if it['cobre'] == ['cabeça'] else f'armadura de {material} miúda {FEM[c]}') if talhe == 'miúdo' else
                              (f'elmo de {material} {CATS[c]}' if it['cobre'] == ['cabeça'] else f'armadura de {material} {FEM[c]}'))
        if talhe == 'miúdo': it['talhe'] = 'miúdo'
    elif tipo == 'escudo':
        it['nome'] = nome or f'escudo {CATS[c]}'
    else:
        sys.exit(f'tipo desconhecido: "{tipo}" (arma, armadura, escudo, nucleo, foco, amuleto, elixir, escrito, gazua, chave)')
    if sob and not T.SOB_MEDIDA_GRAUS[0] <= sob.get('grau', 1) <= T.SOB_MEDIDA_GRAUS[1]:
        sys.exit(f'o grau do sob medida vai de {T.SOB_MEDIDA_GRAUS[0]} a {T.SOB_MEDIDA_GRAUS[1]} (veio {sob.get("grau")})')
    it.update(mais)
    _confere_efeitos(it)
    return it


def _ladino(tipo, c, nome, efeitos, sob, familia, material, cobre, mais):
    """os tipos da etapa 4b: a GAZUA (a ferramenta do ladino, com categoria e durabilidade; vale pela matéria, a da adaga) e a CHAVE (abre sem teste a porta ou o guardado
    que diz em `abre`; não gasta; a loja não a compra nem a vende)"""
    if efeitos or sob or familia or material or cobre: sys.exit(f'a {tipo} não leva efeito, sob medida, família, material nem cobertura')
    base = dict(cat=c, historia=[], dono=None, onde=None)
    if tipo == 'gazua': it = dict(tipo='gazua', nome=nome or f'gazua {FEM[c]}', dur=[DUR[c], DUR[c]], efeitos=[], **base)
    else:
        abre = mais.pop('abre', None)
        if not isinstance(abre, str) or not abre: sys.exit('a chave diz o que abre: abre="SALA_A|SALA_B" (a porta de uma passagem) ou abre="SALA" (o guardado da sala)')
        it = dict(tipo='chave', nome=nome or 'chave', abre=abre, dur=[1, 1], **base)
    it.update(mais)
    return it


def cat_escrito(feiticos): return max([0] + [T.FEITICOS[f]['grau'] - 1 for f in feiticos if f in T.FEITICOS])      # a categoria do escrito: o maior grau que ensina, menos 1 (o de grau 1 é Comum)


def _ferramenta(c, nome, efeitos, sob, familia, material, cobre, mais):
    """(a etapa dos efeitos, parte 1) a FERRAMENTA do ofício: o jogo de forja (martelo de forja e tenaz) ou o jogo de couro (faca e sovela). Não se veste:
    quem a tem soma o bônus dela no teste do ofício (tabelas_oficio.bonus_ferramenta). O ofício vem em oficio=."""
    import tabelas_oficio as O
    if sob or familia or material or cobre: sys.exit('a ferramenta não leva sob medida, família, material nem cobertura: só o ofício (oficio=forja ou couro), a categoria e o nome')
    of = mais.pop('oficio', None); forma = mais.pop('forma', None) or 'jogo'
    if forma in ('martelo', 'tenaz'): of = of or 'forja'
    if of not in O.FERRAMENTA_OFICIOS: sys.exit(f'a ferramenta é de um ofício: oficio={" ou ".join(O.FERRAMENTA_OFICIOS)} (veio "{of}")')
    if forma not in O.FERRAMENTA_FORMAS or (forma != 'jogo' and of != 'forja'): sys.exit(f'a ferramenta da forja é o martelo de forja, a tenaz ou o jogo (os dois); a do couro, o jogo (veio "{forma}" de {of})')
    k = O.chave_ferramenta(forma, of)
    it = dict(tipo='ferramenta', oficio=of, forma=forma, cat=c, nome=nome or f'{O.NOME_FERRAMENTA[k]} {(FEM if forma == "tenaz" else CATS)[c]}', dur=[DUR[c], DUR[c]], efeitos=list(efeitos or []), historia=[], dono=None, onde=None)
    for e in it['efeitos']:
        if e['chave'] not in EFEITOS: sys.exit(f'efeito desconhecido: "{e["chave"]}" (os que há: {", ".join(EFEITOS)})')
        if 'ferramenta' not in EFEITOS[e['chave']][1]: sys.exit(f'o efeito "{e["chave"]}" não vale em ferramenta (vale em: {", ".join(EFEITOS[e["chave"]][1])})')
    it.update(mais)
    return it


def _magia(tipo, c, nome, efeitos, sob, familia, material, cobre, mais):
    """os tipos da etapa da magia: o FOCO (com a forma), o AMULETO, o ELIXIR (a poção do Épico para cima) e o ESCRITO (ensina feitiços). O preço é o da regra de hoje
    (tabelas_mundo.peso_da_peca: a matéria que levam; o amuleto Comum, 10)."""
    if sob or familia or material or cobre: sys.exit(f'o {tipo} não leva sob medida, família, material nem cobertura')
    base = dict(cat=c, historia=[], dono=None, onde=None)
    if tipo == 'foco':
        forma = mais.pop('forma', None)
        if forma not in T.FOCOS: sys.exit(f'forma de foco desconhecida: "{forma}" (use: {", ".join(T.FOCOS)})')
        it = dict(tipo='foco', forma=forma, nome=nome or f"{forma} {(FEM if forma in FORMAS_FEM else CATS)[c]}", dur=[DUR[c], DUR[c]], efeitos=list(efeitos or []), **base)
    elif tipo == 'amuleto': it = dict(tipo='amuleto', nome=nome or f'amuleto {CATS[c]}', dur=[DUR[c], DUR[c]], efeitos=list(efeitos or []), **base)
    else:
        if efeitos: sys.exit(f'o {tipo} não leva efeito')
        if tipo == 'elixir':
            pocao = mais.pop('pocao', None)
            if pocao not in M.POCOES: sys.exit(f'poção desconhecida: "{pocao}" (use: {", ".join(M.POCOES)})')
            if c <= M.POCAO_ATE: sys.exit(f'do Comum ao {CATS[M.POCAO_ATE]} a poção é um bem, na carga ({pocao}:{c}); elixir é do {CATS[M.POCAO_ATE + 1]} para cima')
            it = dict(tipo='elixir', pocao=pocao, nome=nome or f'elixir de {pocao} {CATS[c]}', dur=[1, 1], **base)
        else:
            fs = list(mais.pop('feiticos', None) or [])
            if not fs or any(f not in T.FEITICOS for f in fs): sys.exit(f'o escrito ensina feitiços da tabela (feiticos=seta,luz; os que há: {", ".join(T.FEITICOS)})')
            it = dict(tipo='escrito', feiticos=fs, nome=nome or f"escrito de {', '.join(T.nome_feitico(f) for f in fs)}", dur=[1, 1], **base)
    it.update(mais)
    if 'efeitos' in it: _confere_efeitos(it)
    return it


def _confere_efeitos(it):
    """(fase 1b) os efeitos de uma peça montada fora do mundo (os testes, o cenário, o `nova`): a chave, o tipo de peça, a porta, o cheio, a Caçadora, sem repetir, um apelão de
    regra, e até o teto de efeitos dela mais os dois de fora do teto (a obra-prima e o molde). No mundo, o gravador confere o resto (o teto gravado, a entrada da 1b)."""
    import tabelas_oficio as O
    vistos = set(); teto = it.get('teto_efeitos') if isinstance(it.get('teto_efeitos'), int) else O.efeitos_max(it['cat']) + 2
    for e in it['efeitos']:
        k = e.get('chave')
        if k not in EFEITOS: sys.exit(f'efeito desconhecido: "{k}" (os que há: {", ".join(EFEITOS)})')
        if it['tipo'] not in EFEITOS[k][1]: sys.exit(f'o efeito "{k}" não vale em {it["tipo"]} (vale em: {", ".join(EFEITOS[k][1])})')
        if k in vistos: sys.exit(f'o efeito "{k}" se repete na peça')
        vistos.add(k)
        x = efeito_erro(it, e)
        if x: sys.exit(f'{it.get("nome") or it["tipo"]}: {x}')
    if len(it['efeitos']) > teto: sys.exit(f'{it.get("nome") or it["tipo"]} leva {len(it["efeitos"])} efeitos: o teto dela é {teto}')


def tem(it, chave):
    """o valor do efeito na peça (True se não tem valor), ou None"""
    for e in it.get('efeitos', []):
        if e['chave'] == chave: return e.get('valor', True)
    return None


def pede(it, dorme=False):
    """(atributo, quanto) que a peça pede. O requisito vem do PESO da peça, nunca da categoria nem do nível.
    Peça que dorme (sintonia) não tem efeito nenhum: nem o "leve"."""
    if it['tipo'] in ('nucleo', 'amuleto', 'elixir', 'escrito', 'gazua', 'chave', 'ferramenta'): return 'Força', 0       # o núcleo não se empunha; o amuleto não pede nada; o elixir, o escrito, a gazua, a chave e a ferramenta não se vestem
    aj = 0 if dorme else (T.AJUSTE_PESO if tem(it, 'pesa') else 0) - (T.AJUSTE_PESO if tem(it, 'leve') else 0)
    if it['tipo'] == 'foco': a, q = T.FOCOS[it['forma']]['pede']; return a, q + aj      # o foco pede Afinidade ou Vontade (a forma diz)
    if it['tipo'] == 'arma':
        f = FAMILIAS[it['familia']]
        return f.get('atributo', 'Força'), PEDE_PESO[f['peso']] + aj
    if it['tipo'] == 'armadura': return 'Força', MATERIAIS[it['material']]['pede'] + aj
    return 'Força', PEDE_PESO['media'] + aj


def janela(it):
    """a janela do item, como aparece na cena"""
    c = it['cat']; L = [f"[ {it['nome']} ]"]
    if it['tipo'] == 'nucleo':
        L.append(f"Categoria: {CATS[c]}      Núcleo" + (f" de {it['de']}" if it.get('de') else ''))
        L.append(f"Serve para: uma obra {FEM[c]} (do Épico para cima, a forja pede um núcleo da categoria da peça). Não se veste e não gasta.")
        if it.get('dono'): L.append(f"Dono: {it['dono']}")
        if it.get('onde'): L.append(f"Está em: {it['onde']}")
        for h in it.get('historia', [])[-3:]: L.append(f'  · {h}')
        return '\n'.join(L)
    if it['tipo'] in ('gazua', 'chave'):
        L.append(f"Categoria: {CATS[c]}      " + (f"Gazua (a ferramenta do ladino): durabilidade {it['dur'][0]}/{it['dur'][1]}; abre a fechadura da categoria dela (uma acima, a custo)" if it['tipo'] == 'gazua' else 'Chave: abre sem teste o que foi feita para abrir'))
        if it.get('dono'): L.append(f"Dono: {it['dono']}")
        for h in it.get('historia', [])[-3:]: L.append(f'  · {h}')
        return '\n'.join(L)
    if it['tipo'] in ('elixir', 'escrito'):
        L.append(f"Categoria: {CATS[c]}      " + (f"Elixir: {M.POCOES[it['pocao']]}, uma dose (bebida, some)" if it['tipo'] == 'elixir' else 'Escrito: ensina ' + ', '.join(T.nome_feitico(f) for f in it['feiticos'])))
        if it.get('dono'): L.append(f"Dono: {it['dono']}")
        for h in it.get('historia', [])[-3:]: L.append(f'  · {h}')
        return '\n'.join(L)
    L.append(f"Categoria: {CATS[c]}      Durabilidade: {it['dur'][0]}/{it['dur'][1]}")
    if it['tipo'] == 'foco':
        f = T.FOCOS[it['forma']]
        L.append(f"Foco ({it['forma']}, {'duas mãos' if f['maos'] == 2 else 'uma mão'}): vale {MULT[c] * f['vezes']:g} · de {', '.join(f['de'])}".replace('.', ',') + (f" · apara {BON[c]} e bate {f['dado']} ({f['golpe']})" if f.get('apara') else ''))
    elif it['tipo'] == 'amuleto':
        L.append(f"Guarda contra a magia: {MULT[c]:g} (no pescoço; um só)")
    elif it['tipo'] == 'arma':
        f = FAMILIAS[it['familia']]; m = MULT[c] * (DUAS_MAOS if f['maos'] == 2 and not f.get('distancia') else 1)       # o arco e a besta não ganham o das duas mãos (2.4)
        L.append(f"Ataque: {f['dado']} × {str(round(m, 2)).rstrip('0').rstrip('.').replace('.', ',')} ({f['golpe']})      Acerto: +{BON[c]}      Alcance: {'à distância' if f.get('distancia') else str(f['alcance']) + (' casa' if f['alcance'] == 1 else ' casas')}")
    elif it['tipo'] == 'armadura':
        mat = MATERIAIS[it['material']]; prot = f"{RD[c] * mat['rd']:g}".replace('.', ',')        # a vírgula da mesa: 0,7
        L.append(f"Proteção: {prot} ({it['material']})      Cobre: {', '.join(it['cobre'])}" + (f"      Defesa: {mat['defesa']:+d}" if 'tronco' in it['cobre'] and mat['defesa'] else '') + ('      Talhe: miúdo (não serve em gente grande)' if it.get('talhe') == 'miúdo' else ''))
    elif it['tipo'] == 'ferramenta':                        # (a parte 2, fase 1a) a ferramenta do ofício: o que soma na Lei do Valor, e em que lugar
        import tabelas_oficio as O
        forma = it.get('forma') or 'jogo'; v = O.VALOR_MARTELO[min(c, len(O.VALOR_MARTELO) - 1)]
        L.append(f"Ferramenta de {it.get('oficio', 'forja')}: " + ('o martelo de forja' if forma == 'martelo' else 'a tenaz' if forma == 'tenaz' else 'o jogo (vale no lugar do martelo e no da tenaz)')
                 + f"; soma +{v} na Lei do Valor" + (' em cada lugar' if forma == 'jogo' else '') + f" · teto de efeitos: {it['teto_efeitos'] if isinstance(it.get('teto_efeitos'), int) else O.efeitos_max(c)}")
    else:
        L.append(f"Defesa: +{T.ESCUDO_BASE + BON[c]:g}")
    a, q = pede(it); L.append(f"Pede: {a} {q}" if q else 'Pede: nada')
    for e in it.get('encantos') or []: L.append(f"Encanto: {T.nome_feitico(e['feitico'])} (grau {e['grau']})" + (f", gravado por {e['feito_por']}" if e.get('feito_por') else '') + (f", Dia {e['dia']}" if e.get('dia') else ''))
    if it.get('benta') is not None: L.append('Benta: conta inteira contra o que não tem corpo (por uns dias)')
    if it.get('veneno'): L.append(f"Veneno na lâmina: uma dose {FEM[it['veneno']['cat']]} (a primeira ferida envenena; seca em um dia)")
    mo = it.get('maldita')                                  # a peça maldita parece uma peça comum: só quem a leu (o rito de ler) sabe
    if isinstance(mo, dict) and mo.get('lida'): L.append(f"MALDITA (lida): {mo.get('nome')} ({FEM[mo['cat']] if isinstance(mo.get('cat'), int) else '?'}, {mo.get('tipo')}): quem a puser em uso pega a maldição, e a mão não a larga")
    if it.get('efeitos'): L.append('Efeitos: ' + ' · '.join(frase_efeito(e, c) for e in it['efeitos']))
    if it.get('efeitos_livres'):                            # (fases 1a e 1b) os efeitos que a faixa deu e ainda não foram escolhidos: a ferramenta e (da 1b) a peça de luta escolhem pelo catálogo
        L.append(f"Efeitos por escolher: {it['efeitos_livres']}" + (f" (cheios: {it['cheios_livres']})" if it.get('cheios_livres') else '') + ' (`oficio.py efeito ID` mostra o que cabe)')
    if it.get('sinete'): L.append(f"Sinete: {it['sinete']} (a peça leva o nome de quem a forjou)")
    if it.get('sob_medida'): L.append(f"Sob medida para: {it['sob_medida']['dono']} (grau {it['sob_medida']['grau']})")
    if it.get('dono'): L.append(f"Dono: {it['dono']}")
    if it.get('feito_por'): L.append(f"Quem fez: {it['feito_por']}" + (f", Dia {it['dia']}" if it.get('dia') else ''))
    hs = it.get('historia', [])                             # (fase 1a) a primeira linha (o nascimento: a soma e a faixa) fica sempre, e as três últimas (as escolhas)
    for h in (hs if len(hs) <= 4 else hs[:1] + ['...'] + hs[-3:]): L.append(f'  · {h}')
    return '\n'.join(L)


# ---------- o arquivo ----------
def carrega():
    if not os.path.exists(ARQ): return dict(seq=0, itens={})
    return json.load(open(ARQ, encoding='utf-8'))


def grava(B):
    os.makedirs(os.path.dirname(ARQ), exist_ok=True)
    json.dump(B, open(ARQ, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


def _mundo():
    """o módulo do estado, se HÁ UM MUNDO (a pasta de MOTOR10_MUNDO, ou `mundo/` ao lado): aí o Livro de Itens é o dele, e só o gravador o muda. Senão, None."""
    import estado
    return estado if os.path.exists(os.path.join(estado.pasta(), 'relogio.json')) else None


def _monta(a, op, pos):
    """o registro pedido na linha de comando (`nova ...`), sem dono nem id"""
    if len(pos) >= 3 and pos[1] == 'nucleo': return item('nucleo', pos[2], pos[3] if len(pos) > 3 else None, de=op.get('de'))
    if len(pos) >= 4 and pos[1] in ('foco', 'elixir'):
        return item(pos[1], pos[3], pos[4] if len(pos) > 4 else None, **({'forma': pos[2]} if pos[1] == 'foco' else {'pocao': pos[2]}))
    if len(pos) >= 3 and pos[1] == 'gazua': return item('gazua', pos[2], pos[3] if len(pos) > 3 else None)
    if len(pos) >= 2 and pos[1] == 'chave': return item('chave', 0, pos[2] if len(pos) > 2 else None, abre=op.get('abre'))
    if len(pos) >= 3 and pos[1] in ('amuleto', 'escrito'):
        return item(pos[1], pos[2], pos[3] if len(pos) > 3 else None, **({'feiticos': [x for x in op.get('feiticos', '').split(',') if x]} if pos[1] == 'escrito' else {}))
    if len(pos) < 3 or pos[1] not in ('arma', 'armadura', 'escudo') or (pos[1] != 'escudo' and len(pos) < 4): sys.exit(__doc__)
    ef = []
    for x in a:
        if x.startswith('efeito='):
            k, _, v = x[7:].partition(':'); ef.append(dict(chave=k, **({'valor': int(v)} if v.isdigit() else {})))
    sob = None
    if op.get('sob'):
        d, _, g = op['sob'].partition(':'); sob = dict(dono=d, grau=int(g) if g.isdigit() else 1)
    tipo = pos[1]
    if tipo == 'arma': it = item('arma', pos[3], pos[4] if len(pos) > 4 else None, familia=pos[2], efeitos=ef, sob=sob)
    elif tipo == 'armadura': it = item('armadura', pos[3], pos[4] if len(pos) > 4 else None, material=pos[2], cobre=op['cobre'].split(',') if op.get('cobre') else None, efeitos=ef, sob=sob, talhe=op.get('talhe'))
    else: it = item('escudo', pos[2], pos[3] if len(pos) > 3 else None, efeitos=ef, sob=sob)
    it['feito_por'] = op.get('feito'); it['dia'] = int(op['dia']) if op.get('dia', '').isdigit() else None
    return it


def _no_mundo(estado, a, op, pos):
    """a linha de comando quando há um mundo: olhar lê o Livro dele; o que muda entra por um evento "mestre" (o gravador é um só)"""
    E = estado.carrega(); L = E['itens']['itens']
    quem = lambda x: x if x in E['gente'] else next((k for k, p in E['gente'].items() if p['nome'] == x), None) or sys.exit(f'não há a pessoa "{x}" no mundo (use o id ou o nome: {", ".join(E["gente"])})')
    dono_diz = lambda it: (f" · de {E['gente'][it['dono']]['nome']}" + (' (em uso)' if it.get('uso') else '') if it.get('dono') in E['gente'] else f" · {estado.em(E, it['onde'])}" + (', no chão' if it.get('solto') else '') if it.get('onde') in E['lugares'] else '')
    if a[0] == 'ver':
        alvo = quem(op['dono']) if op.get('dono') else None
        for i, it in L.items():
            if alvo and it.get('dono') != alvo: continue
            print(f"  {i}  {it['nome']} · {CATS[it['cat']]} · {it['dur'][0]}/{it['dur'][1]}" + dono_diz(it))
        if not L: print('  (o Livro de Itens do mundo está vazio)')
        return
    if a[0] == 'nova':
        it = _monta(a, op, pos)
        if op.get('onde'):
            if op['onde'] not in E['lugares']: sys.exit(f'não há o lugar "{op["onde"]}" (os que há: {", ".join(E["lugares"])})')
            it['onde'] = op['onde']
        elif op.get('dono'): it['dono'] = quem(op['dono'])
        else: sys.exit('num mundo, a peça nasce com dono (dono=ID) ou num lugar (onde=LUGAR): solta no nada, não existe')
        ev = estado.aplica(E, 'mestre', [['item', 'nasce', it]], onde=it.get('onde'), quem=[it['dono']] if it.get('dono') else [], texto=f"o Mestre põe no mundo: {it['nome']}")
        iid = f"i{E['itens']['seq']:04d}"; estado.grava(E); print(f"{iid} entrou no Livro de Itens do mundo (evento #{ev['id']}).\n"); print(_janela_mundo(E, E['itens']['itens'][iid])); return
    if a[0] in ('janela', 'dono', 'conserta') and len(pos) > 1:
        it = L.get(pos[1]) or sys.exit(f'não há item "{pos[1]}" no Livro de Itens do mundo (itens.py ver)')
        if a[0] == 'dono':
            if len(pos) < 3: sys.exit('diga para quem: itens.py dono ID PESSOA ["o que houve"]')
            pid = quem(pos[2]); de = E['gente'][it['dono']]['nome'] if it.get('dono') in E['gente'] else 'ninguém'
            if pid != it.get('dono') and estado._presa(E, it): sys.exit(f"{it['nome']} não sai das mãos de {de}: a maldição que veio dela anda em quem a leva (só muda de mão depois de quebrada)")
            ev = estado.aplica(E, 'mestre', [['item', pos[1], 'dono', 'poe', pid], ['item', pos[1], 'historia', 'junta', f"Dia {E['relogio']['dia']}: de {de} para {E['gente'][pid]['nome']}" + (f': {pos[3]}' if len(pos) > 3 else '')]],
                               quem=[pid], texto=f"{it['nome']} passa de {de} para {E['gente'][pid]['nome']}")
            estado.grava(E)
        if a[0] == 'conserta':
            n = int(pos[2]) if len(pos) > 2 and pos[2].isdigit() else it['dur'][1] - it['dur'][0]
            if n < 1 or not estado.aplica(E, 'mestre', [['item', pos[1], 'dur', 'soma', n]], texto=f"o Mestre conserta {it['nome']} ({estado.tantos(n, 'ponto')})"): print('(não havia o que consertar: nada mudou)')
            estado.grava(E)
        print(_janela_mundo(E, E['itens']['itens'][pos[1]])); return
    print(__doc__)


def _janela_mundo(E, it):
    """a janela do item com os nomes de quem é e de quem fez (o Livro do mundo guarda os ids), e onde está"""
    v = dict(it); nome = lambda x: E['gente'][x]['nome'] if x in E['gente'] else x
    if v.get('dono'): v['dono'] = nome(v['dono']) + (' (em uso)' if it.get('uso') else ' (na guarda)' if it['tipo'] != 'nucleo' else '')
    if v.get('feito_por'): v['feito_por'] = nome(v['feito_por'])
    if v.get('sinete'): v['sinete'] = nome(v['sinete'])
    txt = janela(v)
    if it.get('onde') in E['lugares'] and it['tipo'] != 'nucleo': txt += f"\nEstá {E['lugares'][it['onde']].get('em', it['onde'])}" + ((', no chão, junto de um corpo: quem fica com ela é decisão de cena' if it.get('corpo') else ', no chão, de quem achar') if it.get('solto') else ', sem dono')
    return txt


def main():
    a = sys.argv[1:]
    if not a: print(__doc__); return
    op = {k: v for k, v in (x.split('=', 1) for x in a if '=' in x and not x.startswith('efeito='))}
    pos = [x for x in a if '=' not in x]
    estado = _mundo()
    if estado: return _no_mundo(estado, a, op, pos)
    B = carrega()                                           # sem mundo: o Livro solto (dados/itens.json), que só serve à luta fora do mundo (luta.py nova)
    if a[0] == 'nova':
        it = _monta(a, op, pos)
        B['seq'] += 1; it['id'] = f"i{B['seq']:04d}"; it['dono'] = op.get('dono')
        B['itens'][it['id']] = it; grava(B); print(f"{it['id']} entrou no Livro de Itens solto ({ARQ}): vale para a luta fora do mundo. Num mundo (MOTOR10_MUNDO), o mesmo comando grava nele, por evento.\n"); print(janela(it)); return
    if a[0] == 'ver':
        for i, it in B['itens'].items():
            if op.get('dono') and it.get('dono') != op['dono']: continue
            print(f"  {i}  {it['nome']} · {CATS[it['cat']]} · {it['dur'][0]}/{it['dur'][1]}" + (f" · de {it['dono']}" if it.get('dono') else ''))
        if not B['itens']: print('  (o Livro de Itens solto está vazio; não há mundo em MOTOR10_MUNDO)')
        return
    if a[0] in ('janela', 'dono', 'conserta') and len(pos) > 1:
        it = B['itens'].get(pos[1])
        if not it: sys.exit(f'não há item "{pos[1]}" (itens.py ver)')
        if a[0] == 'dono':
            if len(pos) < 3: sys.exit('diga para quem: itens.py dono ID "Nome" ["o que houve"]')
            it['historia'].append(f"de {it.get('dono') or 'ninguém'} para {pos[2]}" + (f': {pos[3]}' if len(pos) > 3 else '')); it['dono'] = pos[2]; grava(B)
        if a[0] == 'conserta':
            it['dur'][0] = min(it['dur'][1], it['dur'][0] + int(pos[2])) if len(pos) > 2 and pos[2].isdigit() else it['dur'][1]; grava(B)
        print(janela(it)); return
    print(__doc__)


if __name__ == '__main__':
    import signal; hasattr(signal, 'SIGPIPE') and signal.signal(signal.SIGPIPE, signal.SIG_DFL)      # a saída cortada (`| head`) acaba o comando calada, sem erro de programa: tudo já foi gravado antes de falar
    main()
