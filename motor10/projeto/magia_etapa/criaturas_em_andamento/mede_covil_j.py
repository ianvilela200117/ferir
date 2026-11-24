#!/usr/bin/env python3
"""mede_covil_j.py — o COVIL de goblins contado no ermo, contra o mundo de HOJE (a vila de teste de verdade, na memória: nada é gravado) e a luta do rascunho (luta_j, com o goblin da tabela).
  1  o covil sozinho, 365 dias: quantos ficam, o que comem da fauna contada, o que roubam da vila, quanto junta o tesouro, e se a prata do mundo fecha
  2  o robô LIMPADOR: Maro, Tomé e Rute assaltam a toca sempre que vale; o despojo passa pela loja de verdade
  3  a primeira limpeza, por tamanho do covil (a toca de começo e a toca com o xamã)
Uso: python3 mede_covil_j.py [1] [2] [3]"""
import sys, os, io, contextlib, random, statistics
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI); import criaturas as CR                    # (põe base/ na frente: as cópias de hoje da luta, dos itens e dos bichos)
sys.path.append('/home/user/ferir/motor10')                          # o mundo de verdade: estado, ato, mercado, caca, vila_teste (só leitura; tudo na memória)
import tabelas as T, tabelas_mundo as M, tabelas_bichos as TB, tabelas_mercado as CM
import tabelas_criaturas as TC, chefes as C, luta_j as LJ
import estado, ato, mercado, caca, vila_teste
from itens import item
from pessoas import padrao, veste

def quieto(f, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()): return f(*a, **k)

# ---------- a tabela do covil de goblins (iria para o tabelas_povos.py) ----------
G = dict(come=0.3, presa=('corça', 'javali', 'ratazana'), carne={'corça': 6, 'javali': 6, 'ratazana': 1},
         cria=0.025, teto=16, rouba_cada=7, rouba_chance=20, rouba_comida=2, rouba_prata=0.25, definha=9, tesouro0=20, cabecas0=9,
         xama_desde=12, xama_dias=30, esconde=30, vem_de_fora=120, novo_bando=6)
DESPOJO = {'metal:0': 1, 'couro:0': 1}

def um_dia(E):
    estado.aplica(E, 'tempo', [['relogio', M.BLOCOS_DIA]], texto='um dia sem ninguém'); ato._mundo_vira(E)
    if '_novos' in E: E['_novos'].clear()

def covil_novo(cabecas=None, tesouro=None):
    return dict(cabecas=G['cabecas0'] if cabecas is None else cabecas, fome=0, celeiro=0.0, prata=G['tesouro0'] if tesouro is None else tesouro, ult_roubo=-99, chefe=True, espada=True, sem_chefe=0,
                xama=False, talisma=True, dias_cheio=0, comeu={}, roubou_comida=0, roubou_prata=0, roubos=0, fora=0, esconde=0)

def covil_dia(E, cv, r, ermo='mata', vila='vila'):
    """a virada de UM covil: come (do celeiro, depois da caça contada do ermo), a fome anda, rouba, cria, definha; o capataz e o xamã sobem"""
    n = cv['cabecas']
    if n <= 0:
        if cv['fora'] > 0:
            cv['fora'] -= 1
            if cv['fora'] == 0: cv.update(cabecas=G['novo_bando'], fome=0, chefe=True, espada=False, xama=False, talisma=False, dias_cheio=0)       # vem um bando de fora: seis, com um capataz sem peça e sem tesouro
        return
    precisa = n * G['come']; do_cel = min(cv['celeiro'], precisa); cv['celeiro'] -= do_cel; precisa -= do_cel
    B = caca.bichos_de(E, ermo); Tt = caca.teto_de(E, ermo); presas = {e: B.get(e, 0) for e in G['presa'] if B.get(e, 0) > 0}
    fartura = sum(presas.values()) / max(1, sum(Tt.get(e, 0) for e in G['presa'] if e in Tt)); ef = {}
    while precisa > 1e-9 and presas:
        if r.random() >= fartura: break
        esp = r.choices(list(presas), weights=list(presas.values()))[0]; carne = G['carne'][esp]
        if precisa < carne and r.random() > precisa / carne: precisa = 0; break
        presas[esp] -= 1; ef[esp] = ef.get(esp, 0) + 1; precisa = max(0, precisa - carne)
        if presas[esp] <= 0: del presas[esp]
    if ef:
        estado.aplica(E, 'mestre', [['lugar', ermo, f'bichos.{e}', 'soma', -q] for e, q in ef.items()], onde=ermo, texto='o bando caça')
        for e, q in ef.items(): cv['comeu'][e] = cv['comeu'].get(e, 0) + q
    cv['fome'] = max(0, cv['fome'] - 1) if precisa <= 1e-9 else min(10, cv['fome'] + 1)
    dia = E['relogio']['dia']
    if cv['esconde'] > 0: cv['esconde'] -= 1
    if dia - cv['ult_roubo'] >= G['rouba_cada'] and cv['esconde'] <= 0:
        cv['ult_roubo'] = dia
        q = min(int(n * G['rouba_comida']), int(E['lugares'][vila]['estoque'].get('comida', 0))) if r.random() < n / G['rouba_chance'] + 0.1 * cv['fome'] else 0
        if q > 0:
            efs = [['estoque', vila, 'comida', 'soma', -q]]; pr = 0
            if r.random() < G['rouba_prata']:
                pr = min(r.randint(1, 6) + n // 4, E['lugares'][vila]['estoque'].get('prata', 0))
                if pr > 0: efs.append(['estoque', vila, 'prata', 'soma', -pr])
            estado.aplica(E, 'mestre', efs, onde=vila, texto='o bando rouba de noite')
            cv['celeiro'] += q; cv['prata'] += pr; cv['roubou_comida'] += q; cv['roubou_prata'] += pr; cv['roubos'] += 1
    if cv['fome'] < 4 and n < G['teto']:
        x = n * G['cria'] * (1 - n / G['teto']); cv['cabecas'] += int(x) + (1 if r.random() < x - int(x) else 0)
    if cv['fome'] >= G['definha']: cv['cabecas'] = max(0, cv['cabecas'] - 1)
    if not cv['chefe'] and cv['cabecas'] > 0:
        cv['sem_chefe'] += 1
        if cv['sem_chefe'] >= 7: cv['chefe'] = True; cv['sem_chefe'] = 0       # em sete dias sobe outro capataz (sem peça: a espada foi com o morto)
    cv['dias_cheio'] = cv['dias_cheio'] + 1 if cv['cabecas'] >= G['xama_desde'] else 0
    if not cv['xama'] and cv['dias_cheio'] >= G['xama_dias']: cv['xama'] = True                                    # o covil que ninguém incomoda ganha um xamã

def parte1(sementes=10, dias=365):
    print(f'1 — O COVIL SOZINHO na Mata do Corvo ({sementes} mundos, {dias} dias; começa com {G["cabecas0"]} cabeças e {G["tesouro0"]} de prata no tesouro; o teto é {G["teto"]})')
    H = []; marcos = (30, 60, 120, 240, 365)
    for s in range(1, sementes + 1):
        E = quieto(vila_teste.cria, 'guerreiro', None, s); cv = covil_novo(); r = random.Random(1000 + s); p0 = mercado.prata_do_mundo(E) + cv['prata']; hist = []; xama_dia = None
        for d in range(dias):
            um_dia(E); covil_dia(E, cv, r)
            if cv['xama'] and xama_dia is None: xama_dia = d + 1
            if d + 1 in marcos: hist.append((cv['cabecas'], caca.bichos_de(E, 'mata').get('corça', 0), caca.bichos_de(E, 'mata').get('javali', 0), cv['fome'], cv['prata']))
        H.append(dict(cv=cv, hist=hist, fecha=mercado.prata_do_mundo(E) + cv['prata'] == p0, xama=xama_dia))
    for k, d in enumerate(marcos):
        cab = [h['hist'][k][0] for h in H]; cor = [h['hist'][k][1] for h in H]; jav = [h['hist'][k][2] for h in H]; pr = [h['hist'][k][4] for h in H]
        print(f"  Dia {d:>3}: cabeças {statistics.mean(cab):4.1f} (de {min(cab)} a {max(cab)}) · corça {statistics.mean(cor):4.1f} de 80 · javali {statistics.mean(jav):4.1f} de 40 · tesouro {statistics.mean(pr):5.1f} de prata (de {min(pr)} a {max(pr)})")
    rc = [h['cv']['roubou_comida'] for h in H]; rp = [h['cv']['roubou_prata'] for h in H]; rb = [h['cv']['roubos'] for h in H]
    cc = [h['cv']['comeu'].get('corça', 0) for h in H]; cj = [h['cv']['comeu'].get('javali', 0) for h in H]; xs = [h['xama'] for h in H if h['xama']]
    print(f"  no ano: comeu {statistics.mean(cc):.0f} corças e {statistics.mean(cj):.0f} javalis · roubou {statistics.mean(rb):.1f} vezes: {statistics.mean(rc):.0f} de comida (a vila come 400 por dia: {100 * statistics.mean(rc) / (400 * dias):.1f}% do ano) e {statistics.mean(rp):.0f} de prata (de {min(rp)} a {max(rp)}; a vila tem 2.000)")
    print(f"  o xamã sobe (30 dias seguidos com {G['xama_desde']} cabeças ou mais) no Dia {statistics.mean(xs):.0f}, em média (de {min(xs)} a {max(xs)}), em {len(xs)} de {len(H)} mundos · a prata do mundo, com o tesouro, fecha em {sum(h['fecha'] for h in H)} de {len(H)}")

# ---------- a casa (as fichas do vila_teste.py) ----------
def maro():
    p = dict(nome='Maro', nivel=5, atributos=dict(Força=70, Agilidade=60, Vigor=70, Vontade=50, Percepção=50, Afinidade=40), maestria={'espada': 2}, equip={}, controla=True)
    return veste(p, arma=('espada', 0), armadura=('malha', 0), escudo=0, elmo=False)
def tome(): return veste(padrao('Tomé', 30, molde='guerreiro', maestria={'lança': 4, 'espada': 2}), arma=('lança', 1), armadura=('malha', 0), escudo=0)
def rute(): return veste(padrao('Rute', 22, molde='arqueiro', maestria={'arco': 4, 'adaga': 2}, linha='trás'), arma=('arco', 1), arma2=('adaga', 0), armadura=('couro', 0), elmo=False)
def bento(): return veste(padrao('Bento', 28, molde='guerreiro', maestria={'martelo': 2}), arma=('martelo', 0), armadura=('couro', 0), elmo=False)
CASAS = {3: lambda: [maro(), tome(), rute()], 4: lambda: [maro(), tome(), rute(), bento()]}

def bando(cv):
    """quem está na toca, pela contagem (chefes.covil): o xamã e 2 guardas (se há xamã), o capataz (com a espada Incomum, se o covil ainda a tem), um quarto de arco, um quarto de lança, o resto de faca"""
    return C.covil(cv['cabecas'], capataz=cv['chefe'], espada=1 if cv['espada'] else None, xama=cv['xama'])()

def assalto(cv, r, surpresa=True, casa=3, **kw):
    """a luta: a casa contra quem está na toca. Devolve (venceu, mortos da casa, ficaram no campo, o capataz ficou, o xamã ficou, feridos da casa, Maro morreu)"""
    LJ.semente(r.randint(1, 10 ** 9)); B = bando(cv)
    if not B: return True, 0, 0, False, False, 0, False
    S = LJ.nova(CASAS[casa](), B, quieto=True, surpresa='B' if surpresa else None, **kw); LJ.corre(S)
    As = [f for f in S['L'] if f['lado'] == 'A']; Bs = [f for f in S['L'] if f['lado'] == 'B']; venceu = S['fim'] == 'A'
    campo = [f for f in Bs if f['estado'] in ('morto', 'caido')] if venceu else [f for f in Bs if f['estado'] == 'morto']
    feridos = sum(len(f['feridas']) > f['feridas_antes'] or f['estado'] in ('morto', 'caido') for f in As)
    mortos = sum(f['estado'] == 'morto' for f in As) + (0 if venceu else sum(f['estado'] == 'caido' for f in As))
    return venceu, mortos, len(campo), any(f['nome'] == 'o capataz goblin' for f in campo), any(f['nome'] == 'o xamã' for f in campo), feridos, As[0]['estado'] == 'morto' or (not venceu and As[0]['estado'] == 'caido')

def vende(E, bens, pecas):
    """vende à loja de verdade (60% pelos bens, 40% pelas peças, a loja farta). Devolve a prata que entrou."""
    p0 = E['gente']['eu']['moedas']
    ef = [['pessoa', 'eu', 'carga.' + b, 'soma', q] for b, q in bens.items() if q >= 1]
    if ef:
        estado.aplica(E, 'mestre', ef, onde='vila', quem=['eu'], texto='o despojo')
        try: quieto(mercado.vender_cesta, E, 'eu')
        except SystemExit: pass
    for tipo, qual, cat, dur in pecas:
        antes = set(E['itens']['itens']); it = item(tipo, cat, None, familia=qual, dono='eu'); it['dur'][0] = dur
        estado.aplica(E, 'gera', [['item', 'nasce', it]], onde='vila', quem=['eu'], texto='a peça do chefe'); iid = next(i for i in E['itens']['itens'] if i not in antes)
        try: quieto(mercado.vender_peca, E, 'eu', iid)
        except SystemExit: pass
    return E['gente']['eu']['moedas'] - p0

def colhe(E, cv, campo, cap, xam):
    """o que a casa leva para a loja depois de ficar com o campo: a sucata de cada cabeça (de metade ao inteiro: aqui o inteiro, o teto), o celeiro, o tesouro, a espada do capataz, o talismã do xamã"""
    bens = {k: v * campo for k, v in DESPOJO.items()}
    if cv['celeiro'] >= 1: bens['comida'] = int(cv['celeiro'])
    pecas = []
    if cap and cv['espada']: pecas.append(('arma', 'espada', 1, 14)); cv['espada'] = False
    if xam and cv['talisma']: pecas.append(('arma', 'maça', 1, 16)); cv['talisma'] = False        # o talismã Incomum vale o preço de tabela (180), como a maça: entra na loja como peça Incomum
    ganho = vende(E, bens, pecas) + cv['prata']; cv['prata'] = 0; cv['celeiro'] = 0
    return ganho

def parte2(sementes=40, dias=120, minimo=6, surpresa=True, repouso=9, casa=3):
    print(f"2 — O ROBÔ LIMPADOR ({sementes} vidas de {dias} dias; a casa: {'Maro, Tomé e Rute' if casa == 3 else 'Maro, Tomé, Rute e Bento'}): assalta {'de madrugada (o bando surpreendido)' if surpresa else 'de dia (ninguém surpreendido)'} sempre que há {minimo} cabeças ou mais; ferido alguém, repousa {repouso} dias")
    R = []
    for s in range(1, sementes + 1):
        E = quieto(vila_teste.cria, 'guerreiro', None, s); cv = covil_novo(); r = random.Random(5000 + s); prata = 0; assaltos = 0; morreu = None; maro_m = False; proximo = 2; primeira = None; depois = []; mortos_g = 0; ganhos = []
        for d in range(1, dias + 1):
            um_dia(E); covil_dia(E, cv, r)
            if morreu or d < proximo or cv['cabecas'] < minimo: continue
            antes = cv['cabecas']; venceu, mortos, campo, cap, xam, feridos, mm = assalto(cv, r, surpresa, casa); assaltos += 1; cv['cabecas'] -= campo; mortos_g += campo
            if cap: cv['chefe'] = False; cv['sem_chefe'] = 0
            if xam: cv['xama'] = False; cv['dias_cheio'] = 0
            ganho = 0
            if venceu:
                ganho = colhe(E, cv, campo, cap, xam)
                if cv['cabecas'] <= 0: cv['fora'] = int(r.expovariate(1 / (G['vem_de_fora'] - 20))) + 20; cv['cabecas'] = 0
                elif cv['cabecas'] <= antes / 2: cv['esconde'] = G['esconde']
            prata += ganho; ganhos.append((d, antes, campo, ganho))
            if primeira is None: primeira = ganho
            else: depois.append(ganho)
            if mortos or not venceu: morreu = d; maro_m = mm
            proximo = d + (repouso if feridos else 2)
        R.append(dict(prata=prata, assaltos=assaltos, morreu=morreu, maro=maro_m, primeira=primeira or 0, depois=depois, mortos_g=mortos_g, dias=morreu or dias, ganhos=ganhos, fim=cv['cabecas']))
    vivos = [x for x in R if not x['morreu']]; dep = [g for x in R for g in x['depois']]
    print(f"  alguém da casa morreu (ou a casa perdeu o campo) em {sum(1 for x in R if x['morreu'])} de {len(R)} vidas (Maro, em {sum(x['maro'] for x in R)}) · assaltos por vida: {statistics.mean(x['assaltos'] for x in R):.1f} · goblins que ficaram no campo por vida: {statistics.mean(x['mortos_g'] for x in R):.1f}")
    print(f"  a PRIMEIRA limpeza rende {statistics.mean(x['primeira'] for x in R):.0f} de prata para a casa inteira (de {min(x['primeira'] for x in R)} a {max(x['primeira'] for x in R)}) · cada limpeza seguinte: "
          + (f"{statistics.mean(dep):.0f} (de {min(dep)} a {max(dep)}; {len(dep)} limpezas)" if dep else 'nenhuma'))
    if vivos:
        m = statistics.mean(x['prata'] for x in vivos)
        print(f"  nas {len(vivos)} vidas em que ninguém morreu: {m:.0f} de prata em {dias} dias = {m / dias / casa:.2f} de prata por dia e por cabeça ({m / dias / casa / 4:.2f} diária) · a que mais rendeu: {max(x['prata'] for x in R)} · o bando no fim: {statistics.mean(x['fim'] for x in R):.1f} cabeças")
    print(f"  uma vida de exemplo (dia, cabeças antes, ficaram no campo, prata): {R[2]['ganhos']}")
    return R

def parte3(n=300):
    print(f'3 — A PRIMEIRA LIMPEZA, por tamanho do covil ({n} assaltos por linha; a prata é a da casa inteira, com o despojo vendido na loja de Pedra Rasa)')
    for nome, cab, tes, xama, casa, surp, kw in (
            ('a toca de começo (9 cabeças, 20 de prata), Maro, Tomé e Rute, de madrugada', 9, 20, False, 3, True, {}),
            ('a mesma, de dia, sem surpresa', 9, 20, False, 3, False, {}),
            ('a toca crescida (13 cabeças, 45 de prata), de madrugada', 13, 45, False, 3, True, {}),
            ('a toca cheia com o xamã (16 cabeças, 100 de prata), Maro, Tomé e Rute, de madrugada', 16, 100, True, 3, True, {}),
            ('a mesma, com Bento (quatro), de madrugada', 16, 100, True, 4, True, {}),
            ('a mesma, com Bento, de dia, sem surpresa', 16, 100, True, 4, False, {})):
        r = random.Random(77); G_ = []; v = m = mm = 0; campo_t = 0
        for i in range(n):
            E = quieto(vila_teste.cria, 'guerreiro', None, 1 + i % 5) if i % 25 == 0 else E
            cv = covil_novo(cab, tes); cv['xama'] = xama; cv['celeiro'] = cab * 2
            venceu, mortos, campo, cap, xam, feridos, maro_m = assalto(cv, r, surp, casa, **kw); v += venceu; m += bool(mortos); mm += maro_m; campo_t += campo
            if venceu:
                E2 = quieto(vila_teste.cria, 'guerreiro', None, 1 + i % 5); G_.append(colhe(E2, cv, campo, cap, xam))
        print(f"  {nome:<86} vence {100 * v / n:3.0f}% · alguém da casa morre {100 * m / n:3.0f}% (Maro: {100 * mm / n:3.0f}%) · ficam no campo {campo_t / n:.1f} · quando vence, leva {statistics.mean(G_):.0f} de prata (de {min(G_)} a {max(G_)}) = {statistics.mean(G_) / 4:.0f} diárias; por cabeça, {statistics.mean(G_) / casa:.0f} de prata")

if __name__ == '__main__':
    qual = [a for a in sys.argv[1:]] or ['1', '2', '3']
    if '1' in qual: parte1(); print()
    if '2' in qual: parte2(); print(); parte2(surpresa=False); print(); parte2(casa=4, minimo=9); print()
    if '3' in qual: parte3()
