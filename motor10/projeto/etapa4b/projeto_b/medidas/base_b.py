"""base_b.py: o arreio de medida do projeto B (dragões e povos). Só LÊ o motor10: importa os módulos e roda lutas de ensaio, sem gravar nada.
Rodar de dentro de /home/user/ferir/motor10 com PYTHONDONTWRITEBYTECODE=1 e MOTOR10_MUNDO numa pasta de rascunho."""
import os, sys, random, statistics
MOTOR = '/home/user/ferir/motor10'
if MOTOR not in sys.path: sys.path.insert(1, MOTOR)
import tabelas as T
import tabelas_bichos as TB
import luta
from pessoas import padrao, veste, ficha, linha, defesa
import bichos

R = 2


def homem(nome, nivel, arma=R, arm=R, esc='igual', familia='espada', material='malha', molde='guerreiro', mods=None, povo=None, tracos=None, **kw):
    """um combatente gerado, vestido; mods soma nos atributos (o povo); povo é o dict do corpo do povo (tamanho etc.)"""
    p = padrao(nome, nivel, molde=molde, **kw)
    for k, v in (mods or {}).items(): p['atributos'][k] += v
    e = arm if esc == 'igual' else esc
    if T.FAMILIAS[familia]['maos'] == 2: e = None
    veste(p, arma=(familia, arma), armadura=(material, arm), escudo=e)
    if povo: p['povo'] = dict(povo)
    if tracos: p['tracos'] = list(tracos)
    return p


def duelo(fa, fb, n=600, semente=7, **kw):
    """(vitória de A em %, mediana de rodadas, mortes de A em %, mortes de B em %)"""
    luta.semente(semente); va = 0; rs = []; ma = mb = 0
    for _ in range(n):
        S = luta.nova(fa(), fb(), quieto=True, **kw); luta.corre(S)
        va += 1 if S['fim'] == 'A' else 0 if S['fim'] == 'B' else 0.5; rs.append(S['r'])
        ma += sum(1 for f in S['L'] if f['lado'] == 'A' and f['estado'] == 'morto')
        mb += sum(1 for f in S['L'] if f['lado'] == 'B' and f['estado'] == 'morto')
    rs.sort()
    return round(100 * va / n, 1), rs[len(rs) // 2], round(ma / n, 2), round(mb / n, 2)


def grupo_contra(fa, fb, n=300, semente=11, **kw):
    """o grupo A contra B: vitória de A, mediana de rodadas, mortos de A por luta (média), lutas em que alguém de A morre (%), A inteiro de pé no fim (%)"""
    luta.semente(semente); va = 0; rs = []; mortos = 0; alguem = 0; caidos = 0
    for _ in range(n):
        S = luta.nova(fa(), fb(), quieto=True, **kw); luta.corre(S)
        va += 1 if S['fim'] == 'A' else 0 if S['fim'] == 'B' else 0.5; rs.append(S['r'])
        m = sum(1 for f in S['L'] if f['lado'] == 'A' and f['estado'] == 'morto'); mortos += m; alguem += m > 0
        caidos += sum(1 for f in S['L'] if f['lado'] == 'A' and f['estado'] in ('morto', 'caido'))
    rs.sort()
    return dict(vence=round(100 * va / n, 1), rodadas=rs[len(rs) // 2], mortos=round(mortos / n, 2), alguem_morre=round(100 * alguem / n, 1), caidos=round(caidos / n, 2))
