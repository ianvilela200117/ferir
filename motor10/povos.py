#!/usr/bin/env python3
"""povos.py — MOTOR 10, ETAPA 4b: OS POVOS DO PERSONAGEM (capítulo 19; os números no tabelas_povos.py; o contrato: projeto/ETAPA_4B.md, seções 1, 8 e 12).

  Seis povos: o humano (a medida de todos: é a pessoa de hoje), o anão, o elfo, o meio-orc, o pequenino e o gnomo. O povo mexe nos atributos com a soma igual, dá
  de nenhum a dois traços (vê no escuro, resiste a veneno), uma coragem, um corpo (gente ou miúdo: a armadura é feita para o corpo), uma tendência nos talentos, a vida
  longa e um +2 num teste do ladino. Quem não tem o campo `povo` é humano. O povo não se troca depois de nascer.
  O NÚCLEO (o gravador, o lutador, o talento, a luta) lê a página tabelas_povos direto; este módulo é o que as frentes chamam e o que vai à mesa.

  ESQUELETO DO ALICERCE (onda 1): as funções do contrato, com a conta simples da página. A frente P (os povos) enche o resto (a mesa, a gente de outros povos na vila de
  teste, o comando) sem mudar a assinatura nem o que cada função devolve.

Uso em código (o que as outras frentes chamam):
  de(p) · tracos(p) (também traços) · ve_no_escuro(p) · coragem(p) · corpo(p) · serve(it, p) · manha(p, teste, pedra=False) · frase(povo) · nasce(E, pid, registro, povo)
  pode_vestir(E, pid, iid) · voce(E) · mesa(E) · so_mestre(E) · na_vila(E, vila='vila')
Uso de linha de comando (só olha):
  python3 povos.py lista              os povos, para o jogador escolher
  python3 povos.py ver POVO           os atributos, os traços, o corpo, a tendência, a vida, o teste do ladino
"""
import sys
import tabelas as T
import tabelas_povos as TP


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
    r = TP.POVOS.get(povo) or sys.exit(f'povo desconhecido: "{povo}" (os que há: {", ".join(TP.POVOS)})')
    return f"{povo}: {r.get('frase', '')}"


def nasce(E, pid, registro, povo):
    """o registro de quem nasce com este povo: os atributos mais os do povo (a soma não muda), o "povo" e a "idade" (a de adulto do povo mais um d10, pelo dado do mundo)"""
    import estado
    r = TP.POVOS.get(povo) or sys.exit(f'povo desconhecido: "{povo}" (os que há: {", ".join(TP.POVOS)})')
    reg = dict(registro); at = dict(reg['atributos'])
    for k, v in (r.get('mods') or {}).items(): at[k] = at[k] + v
    reg['atributos'] = at; reg['povo'] = povo
    reg['idade'] = r['vida'][0] + estado.sorte(E, f'idade|{pid}').randint(1, 10)
    return reg


# ---------- os ganchos ----------
def pode_vestir(E, pid, iid):
    """antes de pôr uma peça em uso (o ato.vestir chama): '' se pode; senão, a frase da recusa (a armadura de outro corpo não serve até ser ajustada)"""
    import estado
    p = E['gente'].get(pid); it = E['itens']['itens'].get(iid)
    if not isinstance(p, dict) or not isinstance(it, dict) or estado.serve(it, p): return ''
    de_quem = 'gente miúda' if it.get('talhe') == 'miúdo' else 'gente grande'
    return f"{it['nome'][0].upper() + it['nome'][1:]} é de {de_quem}: não serve no corpo de {p['nome']}. Um ferreiro a ajusta (`oficio.py ajustar {iid} para={pid}`)."


def voce(E): return []          # (frente P) o povo do personagem numa linha, só se não for humano (a MESA de hoje sai igual)
def mesa(E): return []          # (frente P) quem está aqui, com o povo de quem não é humano
def so_mestre(E): return []


def na_vila(E, vila='vila'):
    """(frente P) a gente de outros povos na vila de teste, o `povos` de Pedra Rasa, as armaduras miúdas na loja: aplica os eventos dela (gera) e devolve as linhas.
    O esqueleto não põe nada."""
    return []


# ---------- o comando ----------
def main(a=None):
    a = sys.argv[1:] if a is None else a
    if a[:1] == ['lista']:
        for k in TP.POVOS: print(frase(k))
    elif a[:1] == ['ver'] and len(a) > 1:
        r = TP.POVOS.get(a[1]) or sys.exit(f'povo desconhecido: "{a[1]}" (os que há: {", ".join(TP.POVOS)})')
        mods = ', '.join(f"{k} {v:+d}" for k, v in (r.get('mods') or {}).items()) or 'nada'
        print(frase(a[1])); print(f"  atributos: {mods} · traços: {', '.join(r['tracos']) or 'nenhum'} · coragem {r['coragem']:+d} · corpo {r['corpo']}"
                                  f" · a favor: {r.get('a_favor') or 'nada'} · contra: {r.get('contra') or 'nada'} · adulto aos {r['vida'][0]}, vive até {r['vida'][2]}")
    else: print(__doc__)


if __name__ == '__main__':
    main()
