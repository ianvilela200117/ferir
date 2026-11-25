#!/usr/bin/env python3
"""m0_base.py — MEDIDA (projeto B, etapa 3): quanto custa HOJE um dia de mundo na vila de teste, sem nada da etapa 3.

Roda de dentro de motor10/:  PYTHONDONTWRITEBYTECODE=1 python3 projeto/etapa3/projeto_b/medidas/m0_base.py RASCUNHO DIAS
Cria uma vila nova com a magia e a 4b em RASCUNHO/m0 (apaga a de antes), e o personagem vive DIAS dias: come, trabalha 2 blocos, espera 2, dorme 2.
Mede: segundos por dia (o relógio de parede), eventos por dia, o tamanho do save (cada arquivo) no fim, e o tempo de um aplica() vazio (a cópia do estado).
Nada aqui escreve no repositório: o mundo fica no rascunho.
"""
import os, sys, time, shutil, json, contextlib, io
AQUI = os.getcwd()
sys.path.insert(0, AQUI)


def main():
    rasc, dias = sys.argv[1], int(sys.argv[2])
    pasta = os.path.join(rasc, 'm0'); shutil.rmtree(pasta, ignore_errors=True)
    os.environ['MOTOR10_MUNDO'] = pasta
    import vila_teste, estado, ato
    with contextlib.redirect_stdout(io.StringIO()):
        vila_teste.main([pasta, 'comeco=ferreiro'])
        vila_teste.main(['magia', pasta])
        vila_teste.main(['fantasia', pasta])
    E = estado.carrega()
    estado.aplica(E, 'mestre', [['pessoa', 'eu', 'moedas', 'soma', 5000]], texto='medida: prata para viver o ano')
    ev0 = E['relogio']['eventos']; t0 = time.time(); paradas = 0
    for d in range(dias):
        try:
            if E['gente']['eu']['corpo']['fome'] > 0: ato.comer(E, 'eu')
            ato.trabalhar(E, 'eu', 2)
            ato.esperar(E, 'eu', 2)
            ato.dormir(E, 'eu', 2)
        except SystemExit as x:
            paradas += 1
            ato.esperar(E, 'eu', 1)
    t1 = time.time()
    estado.grava(E)
    tam = {k: os.path.getsize(os.path.join(pasta, k + '.json')) for k in estado.ARQS}
    tam['eventos.jsonl'] = os.path.getsize(os.path.join(pasta, 'eventos.jsonl'))
    # o custo de UM aplica (a cópia do estado inteiro), medido 200 vezes
    t2 = time.time()
    for i in range(200): estado.aplica(E, 'mestre', [['pessoa', 'eu', 'moedas', 'soma', 1]], texto='medida')
    t3 = time.time()
    print(f'dias: {dias} · segundos: {t1 - t0:.2f} · por dia: {(t1 - t0) / dias * 1000:.1f} ms · eventos por dia: {(E["relogio"]["eventos"] - ev0 - 200) / dias:.1f} · recusas: {paradas}')
    print(f'um aplica (cópia do estado inteiro): {(t3 - t2) / 200 * 1000:.2f} ms · gente: {len(E["gente"])} pessoas · lugares: {len(E["lugares"])} · itens: {len(E["itens"]["itens"])}')
    print('tamanho do save no fim (KB): ' + ' · '.join(f'{k} {v / 1024:.1f}' for k, v in tam.items()))


if __name__ == '__main__': main()
