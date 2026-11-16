#!/usr/bin/env python3
"""conferidor.py — a CONFERÊNCIA DE 5 EM 5 DIAS (pedido do jogador, Dia 248).

Uso:  python3 conferidor.py DIA
Roda nos dias de AUDITORIA do tick (de 5 em 5 dias) e no começo de cada sessão.
Procura sozinho os erros que já aconteceram nesta campanha:
  1. tick semanal sem os PILARES rolados (XXIII.24)
  2. a TRAMA DO JOGADOR rolada pelo tick
  3. NOMES REPETIDOS ou parecidos demais (Kassa/Kasssa, Ithvil)
  4. NOMES NOVOS no estado e no diário que não foram declarados no envelope,
     nem estão nos NPCs, no atlas, no cânone ou no mundo (fato inventado?)
  5. fichas de NPC sem nível
  6. o COFRE: o último número do estado bate com o do envelope?
  7. fatos do CÂNONE contrariados por linhas novas (lista de frases proibidas)
Tudo que aparece com ⚠ é para o Mestre olhar e anotar no envelope (regra 14).
"""
import sys, os, re, json, glob, unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
P = lambda *a: os.path.join(AQUI, *a)
ler = lambda f: open(f, encoding='utf-8', errors='replace').read() if os.path.exists(f) else ''

ENVS = sorted(glob.glob(P('envelope_sessao2*.md')))
ENV_ATUAL = ENVS[-1] if ENVS else ''
DIARIOS = sorted(glob.glob(P('diario_sessao*.md')))
def _acha(*nomes):
    import os
    base = os.path.dirname(os.path.abspath(__file__))
    for n in nomes:
        for c in (os.path.join(base, '..', 'pacote', 'arquivo_dia159', n), os.path.join(base, 'arquivo_dia159', n), os.path.join(base, n)):
            if os.path.exists(c): return c
    return os.path.join(base, 'arquivo_dia159', nomes[0])
ATLAS = _acha('atlas.md')
ENV_VELHO = _acha('envelope.md')

# frases que JÁ FORAM ERRO e não podem voltar (cânone)
PROIBIDAS = [
    (r'(bate|trabalha)[a-z]* (o )?vaduar (a )?quente', 'a casa bate o vaduar A FRIO'),
    (r'febre[^.]{0,40}(obra|culpa|feita) d[oe] M[ée]dico Cinzento', 'a febre é o pó do vaduar aquecido, não obra do Médico Cinzento'),
    (r'Carea[^.]{0,30}(em|de) Ireviel', 'a Carea mora em LEVIS'),
    (r'Graur[^.]{0,60}(vaduar quente|batendo vaduar)', 'o Graur pegou a febre do Kreium, na cela'),
]

def sem_acento(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn').lower()

def lev(a, b):
    if abs(len(a) - len(b)) > 1: return 9
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]

def main():
    dia = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else None
    avisos = []
    env_txt = '\n'.join(ler(f) for f in ENVS)
    npcs = json.load(open(P('npcs.json'))) if os.path.exists(P('npcs.json')) else {}
    mundo = json.load(open(P('mundo_vivo.json'))) if os.path.exists(P('mundo_vivo.json')) else {}

    # 1. pilares em cada tick semanal do envelope atual
    semanais = sorted(set(int(x) for x in re.findall(r'TICK SEMANAL (\d+)', ler(ENV_ATUAL))))
    for d in semanais:
        trecho = ' '.join(l for l in ler(ENV_ATUAL).splitlines() if f'SEMANAL {d}' in l or f'PILARES {d}' in l or f'pilares do {d}' in l.lower())
        if 'PILARES' not in trecho.upper():
            avisos.append(f'PILARES: o tick semanal {d} não tem os pilares rolados (XXIII.24).')

    # 2. trama do jogador rolada
    for f in sorted(glob.glob(P('tick_*.txt'))):
        for l in ler(f).splitlines():
            if re.search(r'trama do dia: Ferir', l) or (re.search(r'^\s*Ferir → ', l) and 'JOGADOR' not in l):
                avisos.append(f'TRAMA DO JOGADOR rolada em {os.path.basename(f)}: {l.strip()[:120]}')

    # 3. nomes parecidos
    nomes = set(npcs.keys())
    for k in ('lendarios', 'monstros', 'lugares', 'viajantes', 'presos', 'monstros_novos'):
        for x in mundo.get(k, []):
            if isinstance(x, dict) and x.get('nome'): nomes.add(x['nome'].split(',')[0].strip())
    base = {}
    for n in nomes:
        if not n[:1].isupper(): continue   # descrições ('agente da Lumine') não são nomes
        s = sem_acento(n.split()[0]) if n.split() else ''
        if len(s) >= 4: base.setdefault(s, set()).add(n)
    chaves = sorted(base)
    vistos = set()
    for i, a in enumerate(chaves):
        for b in chaves[i + 1:]:
            if (a == b or lev(a, b) <= 1) and (a, b) not in vistos and len(a) >= 5:
                vistos.add((a, b))
                avisos.append(f'NOMES PARECIDOS: {sorted(base[a])} × {sorted(base[b])}')

    # 4. nomes em CAIXA ALTA no último bloco do estado e do diário sem declaração
    referencia = sem_acento(env_txt + ler(ATLAS) + ler(ENV_VELHO) + ler(P('canone.md')) + json.dumps(npcs, ensure_ascii=False) + json.dumps(mundo, ensure_ascii=False))
    est = ler(P('estado_vivo.md'))
    m = re.search(r'- \*\*DIA [^\n]*', est)
    ultimo = m.group(0) if m else ''
    comuns = set('DIA BLOCO FERIR SÉRIE SAÚDE COFRE CASA LIGA HOSTE MAGIA MESTRE ÉPICAS ÉPICA NÃO GANHO SUCESSO FALHA CONTA NADA TODOS NOVO NOVA LEU PRAÇA'.split())
    for w in sorted(set(re.findall(r'\b[A-ZÁÉÍÓÚÂÊÔÃÕÇ]{4,}\b', ultimo))):
        if w in comuns: continue
        if sem_acento(w) not in referencia:
            avisos.append(f'NOME SEM DECLARAÇÃO no último bloco do estado: {w}')

    # 4b. o chefe da espionagem no estado bate com o mundo_vivo? (erro do 228, achado no 253)
    ch = mundo.get('espionagem', {}).get('chefe', '')
    m2 = re.search(r'CHEFE DA ESPIONAGEM: (?:o |a )?([A-ZÁÉÍÓÚÂÊÔÃÕÇ]+)', est)
    if ch and m2 and sem_acento(m2.group(1)) != sem_acento(ch):
        avisos.append(f'CHEFE DA ESPIONAGEM: o estado diz {m2.group(1)}, o mundo_vivo diz {ch}.')

    # 5. fichas sem nível
    sem = [n for n, v in npcs.items() if not v.get('nivel')]
    if sem: avisos.append(f'FICHAS SEM NÍVEL (gerar quando entrarem em cena): {", ".join(sem)}')

    # 6. cofre
    NUM = r'(\d{1,3}(?:\.\d{3})+|\d{4,6})'
    def cofre_estado(txt):   # o estado tem o mais novo em cima: vale a linha do LIVRO (primeira)
        m = re.search(r'COFRE\**\s*' + NUM, txt)
        return m.group(1) if m else None
    def cofre_envelope(txt):  # o envelope tem o mais novo embaixo: o último trecho, o último número depois de "→"
        trechos = re.findall(r'COFRE\**\s+\d[^·\n]{0,60}', txt)
        if not trechos: return None
        nums = re.findall(NUM, trechos[-1])
        return nums[-1] if nums else None
    c_est, c_env = cofre_estado(est), cofre_envelope(ler(ENV_ATUAL))
    if c_est and c_env and c_est != c_env:
        avisos.append(f'COFRE: estado diz {c_est}, envelope diz {c_env}.')

    # 7. frases proibidas em qualquer registro vivo
    vivos = [P('estado_vivo.md'), P('npcs.json'), P('mundo_vivo.json')] + DIARIOS[-1:] + [ENV_ATUAL]
    for f in vivos:
        for n, l in enumerate(ler(f).splitlines(), 1):
            if 'CORRIG' in l.upper() or 'ERRAD' in l.upper() or 'ERRO' in l.upper(): continue
            for rx, certo in PROIBIDAS:
                mm = re.search(rx, l, re.I)
                if mm and not re.search(r'\bn[ãa]o\b', l[max(0, mm.start() - 40):mm.start()], re.I):
                    avisos.append(f'CÂNONE CONTRARIADO em {os.path.basename(f)}:{n} — o certo: {certo}')

    # avisos já vistos e anotados no envelope (conferidor_visto.txt) não repetem
    visto = [l.strip() for l in ler(P('conferidor_visto.txt')).splitlines() if l.strip() and not l.startswith('#')]
    novos = [a for a in avisos if not any(a.startswith(v) for v in visto)]
    print(f'=== CONFERIDOR' + (f' · Dia {dia}' if dia else '') + ' ===')
    if not novos:
        print('nada novo achado.')
    for a in novos:
        print('⚠', a)
    print(f'({len(novos)} avisos novos · {len(avisos) - len(novos)} já vistos e anotados. Reler o canone.md antes de narrar.)')

if __name__ == '__main__':
    main()
