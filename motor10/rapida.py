#!/usr/bin/env python3
"""rapida.py — MOTOR 10, etapa 3: A CONTA RÁPIDA PROVISÓRIA DE QUEM NÃO É O PERSONAGEM (uma tabela só, que as duas metades da etapa chamam).

Quem não é o personagem e está fora da cena não luta pelo luta.py: o nomeado que viaja e dá com um bicho na estrada (viagem.anda_npc, frente A2) e o nomeado que pega
uma missão do quadro (missoes.py, frente B2) resolvem tudo pela mesma conta, pelo TETO dele (o grau de perigo que ele enfrenta sem medo) MENOS o GRAU do perigo:
  o teto: (a mão na arma em uso ÷ 2 + 3 × a categoria da arma + a categoria da armadura) ÷ 2, para baixo: 0 é F, 1 é E, 2 é D... (projeto B, 2.11)
  a linha da tabela (tabelas_mundo.RAPIDA): de −2 para baixo, a de −2; de 1 para cima, a de 1. A missão cumpre ou falha (e morre em parte das falhas acima do teto);
  o encontro vence ou não (e morre), com a companhia pela metade (RAPIDA_COMPANHIA).
O dado é o do mundo (estado.sorte, com a chave de quem chama): mesma semente, mesmo mundo. Não grava nada: devolve o que deu, e quem chama põe os efeitos no evento dele.
A ETAPA 5 TROCA ESTA PEÇA pela conta calibrada contra o luta.py (os mesmos nomes de função; a tabela muda).

  python3 rapida.py                 esta ajuda e a tabela
  python3 rapida.py teto ID         o teto de alguém do save (MOTOR10_MUNDO)
"""
import sys
import tabelas_mundo as M
import estado


def teto(E, pid):
    """o teto da pessoa (0 = F, 1 = E, 2 = D...): (a mão na arma em uso ÷ 2 + 3 × a categoria dela + a categoria da armadura) ÷ 2, para baixo; sem arma, a mão nas mãos"""
    p = E['gente'][pid]; eq = estado.pecas(E, pid); ar = eq['arma']; ma = p.get('maestria') or {}
    mao = (ma.get(ar.get('familia'), 0) if ar else ma.get('punho', 0)) if isinstance(ma, dict) else 0
    cat_arma = ar['cat'] if ar else 0
    cat_arm = max([it['cat'] for it in eq['veste'] if it.get('tipo') == 'armadura'] + [0])
    return max(0, min(len(M.GRAUS) - 1, (mao // 2 + 3 * cat_arma + cat_arm) // 2))


def grau(letra_ou_n):
    """o grau como número (0 = F ... 6 = S), de uma letra ('D') ou de um número"""
    return M.GRAUS.index(letra_ou_n) if isinstance(letra_ou_n, str) else int(letra_ou_n)


def letra(n): return M.GRAUS[max(0, min(len(M.GRAUS) - 1, n))]


def linha(dif):
    """a linha da tabela para o teto menos o grau"""
    return M.RAPIDA[max(min(M.RAPIDA), min(max(M.RAPIDA), dif))]


def missao(E, pid, grau_, chave):
    """o nomeado cumpre a missão de grau `grau_`? Devolve {cumpre, morre, dias, linha}: morre só na falha acima do teto. O dado do mundo, com a chave dada."""
    d = teto(E, pid) - grau(grau_); L = linha(d); r = estado.sorte(E, f'rapida|missao|{pid}|{chave}')
    cumpre = r.random() < L['cumpre']; morre = (not cumpre) and d < 0 and r.random() < L['morre_falha']
    return dict(cumpre=cumpre, morre=morre, dias=r.randint(*M.RAPIDA_DIAS), gasta=M.RAPIDA_GASTA, linha=d)


def encontro(E, pid, grau_, chave, com=0):
    """o nomeado que viaja dá com um perigo de grau `grau_` (o bicho, o bando): {vence, morre, linha}. Com companhia (com > 0), a chance de morrer cai pela metade."""
    d = teto(E, pid) - grau(grau_); L = linha(d); r = estado.sorte(E, f'rapida|encontro|{pid}|{chave}')
    vence = r.random() < L['vence']; morre = (not vence) and r.random() < L['morre'] * (M.RAPIDA_COMPANHIA if com else 1) / max(1e-9, 1 - L['vence'])
    return dict(vence=vence, morre=morre, linha=d)


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[:1] == ['teto'] and len(a) == 2:
        E = estado.carrega(); p = E['gente'].get(a[1]) or sys.exit(f'não há a pessoa "{a[1]}"')
        print(f"{p['nome']}: teto {letra(teto(E, a[1]))}"); sys.exit()
    print(__doc__)
    for k in sorted(M.RAPIDA, reverse=True): print(f"  teto − grau {k:+d}: " + ' · '.join(f'{c} {v:g}' for c, v in M.RAPIDA[k].items()))
