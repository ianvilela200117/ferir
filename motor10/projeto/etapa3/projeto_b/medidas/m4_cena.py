#!/usr/bin/env python3
"""m4_cena.py — MEDIDA (projeto B, etapa 3): a MESA com a região, e uma cena para o PROJETO.md.

Roda de dentro de motor10/:  PYTHONDONTWRITEBYTECODE=1 python3 projeto/etapa3/projeto_b/medidas/m4_cena.py RASCUNHO [dias=40]
Cria a vila de teste do ferreiro com a região (o arremedo), anda o mundo com o robô atento até haver dois itens na caixa (ou até DIAS), e mostra:
(1) o tamanho da MESA.md de hoje (turno.abre) com 144 nomeados na região, seção por seção; (2) as seções do projeto B (proto_b.mesa_b) naquele momento;
(3) o preço que a gente de Pedra Rasa pede para ir junto (a regra de quem vai junto do projeto B), contra cada bicho e lugar.
"""
import os, sys, shutil, contextlib, io, math
sys.path.insert(0, os.getcwd()); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    a = sys.argv[1:]; op = dict(x.split('=', 1) for x in a if '=' in x); pos = [x for x in a if '=' not in x]
    rasc = pos[0]; dias = int(op.get('dias', 40)); pasta = os.path.join(rasc, 'm4'); shutil.rmtree(pasta, ignore_errors=True); os.environ['MOTOR10_MUNDO'] = pasta
    import vila_teste, estado, ato, oficio, mercado, turno, cow, bichos
    import proto_b as P, tab_b as G
    cow.instala()
    with contextlib.redirect_stdout(io.StringIO()):
        vila_teste.main([pasta, 'comeco=ferreiro', 'inclinacao=forja', 'inclinacao2=encanto']); vila_teste.main(['magia', pasta]); vila_teste.main(['fantasia', pasta])
    E = estado.carrega(); B = P.B_novo(); P.regiao(E); P.povoa(E, B)
    ultimo = None; fim = E['relogio']['dia'] + dias
    while E['relogio']['dia'] < fim:
        if E['relogio']['dia'] != ultimo:
            ultimo = E['relogio']['dia']; P.gente_dia_tudo(E, B)
            if len(B['caixa']['abertos']) >= 2 and E['relogio']['dia'] > 10: break
        for _ in range(3):
            if E['gente']['eu']['corpo']['fome'] >= 2:
                try: ato.comer(E, 'eu')
                except SystemExit: pass
        try: oficio.jornal(E, 'eu', 2); ato.dormir(E, 'eu', 2); ato.esperar(E, 'eu', 2)
        except SystemExit: pass
        tb = (E['gente']['eu'].get('treino') or {}).get('forja', 0); P.fama_bancada(E, B, tb - 2)
    txt = turno.mesa(E); partes = txt.split('\n## ')
    print(f'== a MESA.md de hoje (turno.mesa), no Dia {E["relogio"]["dia"]}, com {len(P.nomeados(E, B))} nomeados na região: {len(txt.encode()) / 1024:.1f} KB')
    for pt in partes: print(f'   {pt.splitlines()[0][:40]:40s} {len(pt.encode()) / 1024:5.1f} KB')
    mb = '\n'.join(P.mesa_b(E, B)); print(f'\n== as seções do projeto B (proto_b.mesa_b): {len(mb.encode()) / 1024:.1f} KB\n'); print(mb)
    print('\n== quem vai junto (a regra do projeto B): o teto de cada um, e o que pede contra cada perigo (a opinião de hoje)')
    graus = dict(corça='F', javali='E', lobo='D', urso='D', goblin='F', esqueleto='E', **{'corpo-seco': 'E'})
    perigos = [('corça', 0), ('javali', 1), ('lobo (bando)', 2), ('a toca dos goblins', 2), ('a cripta (o guardião)', 3)]
    for k in ('rute', 'tome', 'ivo', 'durva', 'brasco', 'ilvena', 'quim'):
        if k not in E['gente']: continue
        t = P.teto(E, k); op_ = P.opiniao(E, B, k); dia = M_diaria(E, k); L = []
        for nome, g in perigos:
            d = g - t
            if op_ <= G.NAO_PEDE or d >= 2: L.append(f'{nome}: recusa'); continue
            if d >= 1 and op_ < 2: L.append(f'{nome}: recusa (só com opinião +2)'); continue
            vezes = G.COMPANHIA[max(-1, min(1, d))]; desc = next((x for o, x in G.COMPANHIA_OPINIAO if op_ >= o), 1.0)
            L.append(f'{nome}: ' + ('vai pela parte' if vezes * desc == 0 else f'{math.ceil(dia * vezes * desc)} de prata e a parte'))
        print(f'- {E["gente"][k]["nome"]} (teto {G.GRAUS[t]}, diária {dia}, opinião {op_:+d}): ' + ' · '.join(L))


def M_diaria(E, k):
    import tabelas_mundo as M
    return M.SALARIO[E['gente'][k]['grau_oficio']] * M.JORNADA


if __name__ == '__main__': main()
