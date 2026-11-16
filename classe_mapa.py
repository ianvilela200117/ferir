#!/usr/bin/env python3
"""classe_mapa.py — MOTOR 9 (438, 4e): todo NPC com CLASSE DO LIVRO.

Para cada NPC do npcs.json sem `classe_livro`: escolhe uma classe do Livro (capítulo Classes e Livro Nove) pelo que a
ficha dele diz (a classe antiga e a ocupação) e pela raridade que o nível dele alcança
(até 19 Comum · 20-49 Incomum · 50-99 Raro · 100-149 Épico · 150+ Único). A classe antiga FICA em `classe` (é a descrição).
Quem não dá pista nenhuma recebe uma classe de gente comum no dado (d6), anotada.
Também tira do texto da ficha o desejo, a ambição, o medo e a linha vermelha (quando estão escritos) e, onde faltam,
gera pelo gerador (marcado em `gerado_438`). Segredo NÃO se gera aqui: nasce em cena.
Depois: `python3 classe.py migra` grava as assinaturas e a fraqueza.

Uso: python3 classe_mapa.py [ver]      (com "ver", só mostra; sem nada, grava)
"""
import re, sys
from nucleo import d, carrega, grava, anota, sem_acento
import gerador as G
import classe as CL

T = lambda nv: 0 if (nv or 0) < 20 else 1 if nv < 50 else 2 if nv < 100 else 3 if nv < 150 else 4
SOLD = ['Soldado', 'Guarda-Costas', 'Duelista', 'Campeão', 'Senhor da Guerra']
REGRAS = [
 (r'intendente|notario|guarda-livros|escrevente|burocrata|copista|agrimensor|alfandega', ['Burocrata', 'Burocrata', 'Banqueiro', 'Senhor da Moeda', 'Senhor da Moeda']),
 (r'\bmae d|\bpai d|carroceir|gente comum|lavrador', ['Camponês'] * 5),
 (r'sargento|capuz do graur', SOLD),
 (r'mag[ao] de elo|selador', ['Selador', 'Selador', 'Caçador de Elo', 'Quebrador de Correntes', 'Guardião do Elo']),
 (r'runist', ['Aprendiz de Mago', 'Mago', 'Runomante', 'Elementalista', 'Conjurador do Vazio']),
 (r'\bmag[oa]\b|arquimago', ['Aprendiz de Mago', 'Mago', 'Mago de Batalha', 'Elementalista', 'Conjurador do Vazio']),
 (r'curandeir|fisic[oa]\b|enfermari', ['Curandeiro', 'Clérigo', 'Físico de Campanha', 'Guardião da Fé', 'Mártir']),
 (r'sacerdot|templo|lumine', ['Noviço', 'Sacerdote', 'Orador Sagrado', 'Guardião da Fé', 'Mártir']),
 (r'alquimi|remedio', ['Alquimista', 'Alquimista', 'Alquimista', 'Mestre Alquimista', 'Mestre Alquimista']),
 (r'plantas|herbal', ['Camponês', 'Herbalista', 'Druida', 'Guardião da Mata', 'Praguicultor']),
 (r'metais e forja', ['Artífice'] * 5),
 (r'pesquisador|ruinas|monstros e nucleos', ['Caçador de Achados', 'Caçador de Achados', 'Inspetor', 'Inspetor', 'Inspetor']),
 (r'mineir', ['Carpinteiro', 'Artífice', 'Construtor', 'Construtor', 'Construtor']),
 (r'ferreir|fundidor|forjador|bigorna|\bforja\b', ['Ferreiro', 'Armeiro', 'Ferreiro de Guerra', 'Mestre Forjador', 'Forjador de Alma']),
 (r'assassin|\bfaca\b|lamina de aluguel|venen', ['Ladino', 'Larápio', 'Assassino', 'Mestre das Sombras', 'Sombra do Trono']),
 (r'estivador-chefe|podesta|emissari|embaixador|diplomat|enviado|jurado|anciao|herdeiro|senhora de|voz do povo|quer a guerra', ['Arauto', 'Diplomata', 'Orador', 'Porta-Estandarte', 'Voz do Reino']),
 (r'espi|agente|fonte e canal|contraband', ['Ladino', 'Espião', 'Caçador de Recompensas', 'Mestre das Sombras', 'Sombra do Trono']),
 (r'barqueir|salineir|canais|mascate|mercador', ['Mascate', 'Mascate', 'Mestre de Caravana', 'Contrabandista de Rotas', 'Mercador Lendário']),
 (r'batedor|cacador|\bguia\b', ['Caçador', 'Batedor de Mata', 'Batedor de Mata', 'Guardião da Mata', 'Guardião da Mata']),
 (r'capita|campea|marechal', ['Soldado', 'Soldado', 'Capitão', 'Campeão', 'Senhor da Guerra']),
 (r'lanceir', ['Lanceiro', 'Lanceiro', 'Cavaleiro', 'Campeão', 'Senhor da Guerra']),
 (r'bandid|desertor|mercenari|da liga|na liga', ['Mercenário', 'Espadachim', 'Duelista', 'Mestre de Armas', 'Senhor da Guerra']),
 (r'guarda|soldad|remador|carregador|carcereir|chamado|\(aco', SOLD),
]
MAO = {'Leliel': 'Rei sem Coroa', 'Tilde': 'Ferreiro', 'Graur': 'Ferreiro de Guerra', 'Ceduion': 'Arquimago', 'Tuald': 'Ferreiro', 'Brara': 'Ferreiro de Guerra', 'Mie': 'Campeão', 'Girendino': 'Arauto', 'Tolvane': 'Diplomata'}
FORA = ('Tuir', 'Zyza')
COMUNS = ['Camponês', 'Mascate', 'Soldado', 'Carpinteiro', 'Menestrel', 'Andarilho']


def tira(txt, v):
    """desejo, ambição, medo e linha vermelha que já estão escritos na classe antiga"""
    for ped in [p.strip() for p in str(txt).split(' · ')]:
        m = re.match(r'desejo:\s*(.+)', ped, re.I)
        if m and not v.get('desejo'): v['desejo'] = m.group(1).strip()
        m = re.match(r'ambi[çc][ãa]o(?: \(\d+\))?:\s*(.+)', ped, re.I)
        if m and not v.get('ambicao'): v['ambicao'] = m.group(1).strip()
        m = re.match(r'medo(?::| d[oae]s?)\s*(.+)', ped, re.I)
        if m and not v.get('medo'): v['medo'] = m.group(1).strip()
        if re.match(r'nunca ', ped, re.I) and not v.get('linha_vermelha'): v['linha_vermelha'] = ped


def main():
    so_ver = 'ver' in sys.argv; N = carrega('npcs.json'); L = CL.livro(); linhas = []; dados = []; n_ger = 0
    for nome, v in N.items():
        tira(v.get('classe', ''), v)
        if nome not in FORA and (v.get('classe') or v.get('ocupacao')):
            ger = [k for k, lst in (('desejo', G.DESEJO), ('ambicao', G.AMBICAO), ('medo', G.MEDO), ('linha_vermelha', G.LINHA)) if not v.get(k)]
            if ger and not so_ver:
                for k, lst in (('desejo', G.DESEJO), ('ambicao', G.AMBICAO), ('medo', G.MEDO), ('linha_vermelha', G.LINHA)):
                    if k in ger: v[k] = G.esc(lst)
                v['gerado_438'] = ger; n_ger += 1
        if v.get('classe_livro') or nome in FORA: continue
        txt = sem_acento(f"{v.get('classe') or ''} {v.get('ocupacao') or ''}").lower()
        if not txt.strip() or txt.strip() in ('(sem ficha antiga no livro)',): continue
        tc = sem_acento(str(v.get('classe') or '')).lower(); to = sem_acento(str(v.get('ocupacao') or '')).lower()   # primeiro a classe antiga; só depois a ocupação
        alvo = MAO.get(nome) or next((lad[T(v.get('nivel'))] for rx, lad in REGRAS if re.search(rx, tc)), None) or next((lad[T(v.get('nivel'))] for rx, lad in REGRAS if re.search(rx, to)), None)
        if not alvo:
            r = d(6) if not so_ver else 0; alvo = COMUNS[r - 1] if r else '(d6 de gente comum)'; dados.append(f'{nome} d6 [{r}] {alvo}')
        if not so_ver and sem_acento(alvo).lower() not in L: sys.exit(f'classe fora do Livro no mapa: {alvo} ({nome})')
        if not so_ver: v['classe_livro'] = alvo; v['classe_mapeada_438'] = True
        linhas.append(f"{nome} ({v.get('nivel')}): {alvo}")
    print(f'{len(linhas)} NPC(s) ganham classe do Livro' + (' (só mostrando)' if so_ver else '') + ':')
    for i in range(0, len(linhas), 4): print('  ' + ' · '.join(linhas[i:i + 4]))
    if not so_ver:
        grava('npcs.json', N)
        anota(f"- (OCULTO) CLASSE_MAPA (438, 4e): {len(linhas)} NPCs com classe do Livro pela ficha e pelo nível: " + ' · '.join(linhas) + (f" · no dado (sem pista na ficha): {' | '.join(dados)}" if dados else '') + f" · desejo, ambição, medo e linha vermelha gerados onde faltavam em {n_ger} fichas (campo gerado_438); segredo não se gera")
        print(f'desejo, ambição, medo e linha vermelha: tirados do texto ou gerados em {n_ger} ficha(s). Agora: python3 classe.py migra')


if __name__ == '__main__':
    main()
