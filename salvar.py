#!/usr/bin/env python3
"""salvar.py — fim de sessão (MOTOR 6): confere o motor, refaz o BRIEFING.md e gera o zip do save.
Uso: python3 salvar.py [sem_zip]
"""
import os, sys, zipfile, subprocess
from nucleo import carrega, P, AQUI, envelope_atual

def main():
    dia = carrega('estado.json').get('tempo', {}).get('dia', 0)
    av = []
    S = carrega('selos.json', {'ordem': [], 'selos': {}})
    ab = [i for i in S['ordem'] if S['selos'].get(i, {}).get('estado') == 'declarado']
    if ab: av.append(f"selos declarados e NÃO rolados: {', '.join(ab)} (selo.py rola ID)")
    for r in carrega('relogios.json', {'relogios': []})['relogios']:
        if r['estado'] == 'vivo' and r['valor'] >= r['max']: av.append(f"relógio CHEIO sem desfecho: {r['nome']}")
    A = carrega('agenda.json', {'itens': []})
    at = [f"#{i['id']} (Dia {i['dia']})" for i in A['itens'] if not i['feito'] and i['tipo'] != 'noticia' and i['dia'] < dia]
    if at: av.append('agenda ATRASADA: ' + ', '.join(at) + ' (agenda.py feito ID ou muda ID DIA)')
    F = carrega('ficha.json')
    if F and F.get('cofre', 0) < 0: av.append(f"cofre negativo: {F['cofre']}")
    kb = os.path.getsize(envelope_atual()) // 1024
    if kb > 400: av.append(f"o envelope atual tem {kb} KB: comece um novo (crie o próximo envelope_sessao2?.md com uma linha de título; o motor passa a escrever nele)")
    print('CONFERÊNCIA DO MOTOR: ' + ('tudo em ordem.' if not av else ''))
    for a in av: print('  ⚠ ' + a)
    if 'sem_teste' not in sys.argv: subprocess.run([sys.executable, P('teste_motor.py'), 'rapido'])
    subprocess.run([sys.executable, P('contexto.py'), 'quieto'])
    subprocess.run([sys.executable, P('painel.py'), 'quieto']); subprocess.run([sys.executable, P('cronica.py'), 'quieto'])
    if 'sem_zip' in sys.argv: return
    destino = os.path.join(os.path.dirname(AQUI), f'save_ferir_dia{dia}_motor6.zip')
    raiz = os.path.basename(AQUI)
    with zipfile.ZipFile(destino, 'w', zipfile.ZIP_DEFLATED) as z:
        for pasta, _, arqs in os.walk(AQUI):
            if '__pycache__' in pasta: continue
            for a in arqs:
                if a.endswith(('.tmp', '.pyc')): continue
                cam = os.path.join(pasta, a)
                z.write(cam, os.path.join(raiz, os.path.relpath(cam, AQUI)))
    print(f'SAVE: {destino} ({os.path.getsize(destino) // 1024} KB)')

if __name__ == '__main__':
    main()
