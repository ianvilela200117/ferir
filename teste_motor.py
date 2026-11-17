#!/usr/bin/env python3
"""teste_motor.py — TESTE DO MOTOR antes da sessão (MOTOR 6.3). Copia o save para uma pasta temporária, roda cada script lá
(inclusive um bloco de 8 dias, que passa por um tick semanal inteiro) e confere se nenhum cai e se todo JSON abre.
NÃO mexe no save de verdade. Uso: python3 teste_motor.py [rapido]   (rapido: sem o bloco de 8 dias). O salvar.py roda o rápido.
"""
import os, sys, json, glob, shutil, subprocess, tempfile
AQUI = os.path.dirname(os.path.abspath(__file__))
CMDS = [['habilidades.py', 'mao'], ['artes.py', 'ver'], ['despertar.py', 'ver'], ['edito.py', 'ver'], ['cria.py', 'ver'], ['cancao.py', 'ver'], ['coleta.py', 'ver'], ['festas.py', 'ver'], ['atlas.py', 'ver'], ['classe_mapa.py', 'ver'], ['bicho.py', 'obras/zythir_sala9_guardiao.txt', 'sims/_teste_bicho.json', 'fase=nao'],
        ['tick.py', 'status'], ['ficha.py', 'ver'], ['agenda.py', 'ver'], ['agenda.py', 'fios'], ['relogio.py', 'ver'], ['faccoes.py', 'ver'], ['clima.py', 'ver'],
        ['mercado.py', 'ver'], ['combate.py', 'ver'], ['feridos.py', 'ver'], ['cerco.py', 'lista'], ['npc.py', 'lista', '3'], ['reino.py', 'estado'], ['obra_valor.py', 'fichas'],
        ['viagem.py', 'lista'], ['motor.py'], ['rotina.py', 'ver'], ['nomes.py', 'arcaica', '2', 'livre'], ['selo.py', 'dr', 'TESTE1', 'teste', 'd20', '1-10: a | 11-20: b'],
        ['conselho.py', 'TESTE2', 'teste', 'A: sim', 'B: não'], ['luta.py', 'sims/caca_6_lobo-cinzento.json', 'sim=30'], ['aberto.py', '2d20+10', 'cd=20'],
        ['contexto.py', 'quieto'], ['conferidor.py', '999'], ['julgamento.py', 'ver'], ['tratados.py', 'ver'], ['onde.py', 'ver'], ['batalha.py', 'modelo', 'sim=50'], ['painel.py', 'quieto'], ['cronica.py', 'quieto']]
LENTO = [['tick.py', 'bloco', '8', 'resumo'], ['contexto.py', 'quieto']]

def main():
    tmp = tempfile.mkdtemp(prefix='teste_motor_'); dst = os.path.join(tmp, 'save')
    shutil.copytree(AQUI, dst, ignore=shutil.ignore_patterns('*.zip', '__pycache__', 'tick_1*.txt', 'tick_2*.txt'))
    falhas = []; cmds = CMDS + ([] if 'rapido' in sys.argv else LENTO)
    for c in cmds:
        r = subprocess.run([sys.executable, os.path.join(dst, c[0])] + c[1:], capture_output=True, text=True, cwd=dst)
        ruim = r.returncode != 0 or 'Traceback' in r.stderr or 'CAIU NO MEIO' in r.stdout
        if ruim: falhas.append((' '.join(c), (r.stderr.strip().splitlines() or r.stdout.strip().splitlines() or ['?'])[-1][:200]))
    for f in glob.glob(os.path.join(dst, '*.json')) + glob.glob(os.path.join(dst, 'cercos', '*.json')):
        try: json.load(open(f, encoding='utf-8'))
        except Exception as e: falhas.append((os.path.basename(f), f'JSON quebrado: {e}'))
    shutil.rmtree(tmp, ignore_errors=True)
    print(f'TESTE DO MOTOR: {len(cmds) - len([f for f in falhas if not f[0].endswith(".json")])} de {len(cmds)} comandos passaram' + (' · todos os JSON abrem' if not any(f[0].endswith('.json') for f in falhas) else ''))
    for c, e in falhas: print(f'  ✗ {c}: {e}')
    sys.exit(1 if falhas else 0)

if __name__ == '__main__':
    main()
