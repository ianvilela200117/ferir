#!/usr/bin/env python3
"""encadeia.py — G39, OS ENCADEAMENTOS (Dia 502, pedido do jogador: "faz um jeito de você parar de esquecer alguma
informação ou ficar algo para trás: toda vez que uma luta finalizar, ver quem ajudou e distribuir XP; sempre que o NPC
fizer algo, ativar o XP dele; e outras coisas que dependem uma da outra: se ativar uma, ative a outra").

Uma coisa puxa a outra, sozinha. O que cada script chama aqui:
  luta.py (luta de verdade, sem régua)  → xp_luta: o XP vai para cada um que lutou e não morreu (o rei no ficha.py,
                                           os outros no cresce.py); o despojo do bicho é lembrado.
  cresce.py tick (alguém subiu)         → subiu: o PV da ficha de combate sobe junto (o Motor: nível × 2; o ataque e a
                                           defesa não sobem com o nível) · a CLASSE sobe de faixa com a Prova (d6, 3-6) ·
                                           o DESPERTAR no 100, 200 e 300 · as ARTES DE ARMA na faixa nova.
  tick.py (todo dia)                    → pendencias: os PRAZOS da casa nos próximos 7 dias, os ATRASADOS que tocam a
                                           casa, as ESCOLHAS do jogador por fazer, quem passou do 100 sem Dom, as fichas
                                           de combate fora do nível.
Uso à mão:
  python3 encadeia.py pendencias [DIAS]    o que está para trás ou vence nos próximos DIAS (padrão 7)
  python3 encadeia.py sincroniza           acerta o PV de toda ficha de combate pelo nível de hoje (uma vez; anota)
"""
import sys, os, json, secrets, subprocess, re
from nucleo import P, carrega, grava, anota, dia_atual, sem_acento

d = lambda n: secrets.randbelow(n) + 1
FAIXAS = [(0, 'Comum'), (20, 'Incomum'), (50, 'Raro'), (100, 'Épico'), (150, 'Único')]   # a mesma do classe_mapa.py (438)
ORDEM_RAR = ['Comum', 'Incomum', 'Raro', 'Épico', 'Único', 'Lendário']
GRANDES = ('Lendário', 'Lendario', 'Mítico', 'Mitico', 'Primordial')


def faixa(nivel):
    r = 'Comum'
    for n, nome in FAIXAS:
        if nivel >= n: r = nome
    return r


def roda(script, *args):
    p = subprocess.run([sys.executable, P(script)] + [str(x) for x in args], capture_output=True, text=True)
    return (p.stdout or '') + (p.stderr or '')


# ─────────────────────────── 1. O XP DA LUTA (o luta.py chama) ───────────────────────────
def xp_luta(F, r, dia=None):
    """F: o arquivo da luta; r: o resultado do luta.py. Devolve as linhas que mostrou."""
    dia = dia or dia_atual()
    M = F['monstro']; nivel = int(M.get('nivel') or 0); cat = str(M.get('cat', 'Comum'))
    quantos = int(M.get('quantos', 1) or 1)
    pv_un = M.get('pv_un') or (M['pv'] / quantos)
    out = []
    if r['res'] == 'morto':
        caidos = quantos
    else:
        dano = max(0, r['pvm'] - max(0, r['pv']))
        caidos = int(dano // pv_un) if quantos > 1 else 0
    if M.get('enxame') and quantos == 1:
        out.append("⚠ G39: enxame sem 'quantos' no arquivo da luta: o XP conta um só (pôr 'quantos' e 'pv_un' na base)")
    try:   # 507 (G39, erro achado no G9 do coração): o PV do rei no fim da luta vai à ficha sozinho (antes ficava cheio no ficha.json)
        g = next((x for x in r.get('G', []) if x.get('nome') == 'Ferir'), None)
        if g is not None and 'sim=' not in ' '.join(sys.argv):
            Fi = carrega('ficha.json'); pv_fim = max(0, int(g.get('pva', g.get('pv', Fi['pv'][0]))))
            if pv_fim != Fi['pv'][0]:
                out.append(f"G39 · o PV do rei no fim da luta vai à ficha: {Fi['pv'][0]} → {pv_fim}/{Fi['pv'][1]}"); Fi['pv'][0] = min(pv_fim, Fi['pv'][1]); grava('ficha.json', Fi)
    except Exception as ex:
        out.append(f'⚠ G39: o PV do rei não foi à ficha: {ex}')
    mult = 10 if cat in GRANDES else (5 if M.get('chefe') else 1)
    cada = nivel * 10 * caidos * mult
    vivos = [g for g in r['G'] if g['nome'] not in r['mortos'] and not g['nome'].startswith('hoste')]
    if cada <= 0:
        out.append(f"G39 · XP da luta: nenhum caído do lado de lá ({M['nome']} {r['res']}): sem XP")
        for l in out: print(l)
        return out
    motivo = f"{dia}: {M['nome']} ({cat} {nivel}; {caidos} caído(s)" + (f", × {mult}" if mult > 1 else '') + ')'
    out.append(f"G39 · XP DA LUTA, sozinho: {cada} a cada um que lutou ({nivel} × 10 × {caidos}" + (f" × {mult}" if mult > 1 else '') + f"): {', '.join(g['nome'] for g in vivos)}")
    npcs = []
    for g in vivos:
        if g['nome'] == 'Ferir':
            lin = [l for l in roda('ficha.py', 'xp', cada, motivo).split('\n') if l.strip() and not l.startswith('  |')]
            out += ['   ' + l for l in lin]
        else:
            npcs.append(g['nome'])
    if npcs:
        lin = [l for l in roda('cresce.py', 'xp', ','.join(npcs), cada, motivo).split('\n') if l.strip()]
        out += ['   ' + l for l in lin]
    if M.get('drops'):
        out.append(f"   G39 · o DESPOJO: {M['drops']} → lançar com ficha.py mat")
    elif r['res'] == 'morto':
        out.append("   G39 · o DESPOJO: o bicho deixa corpo: ver os drops do gerador e lançar com ficha.py mat")
    anota(f"- G39 [Dia {dia}] XP DA LUTA ({os.path.basename(F.get('_arquivo', 'luta'))}): {cada} a {', '.join(g['nome'] for g in vivos)} · {motivo}")
    for l in out: print(l)
    return out


# ─────────────────────────── 2. O NÍVEL DESTRAVA O RESTO (o cresce.py chama) ───────────────────────────
def _classes_do_livro():
    try:
        import classe
        return classe.livro()
    except Exception:
        return {}


def subiu(nome, de, para, dia=None):
    """Alguém subiu de 'de' para 'para'. Faz tudo o que depende disso e devolve as linhas."""
    dia = dia or dia_atual(); out = []
    FC = carrega('fichas_combate.json', {'fichas': {}})
    if nome in FC.get('fichas', {}):   # (a) o PV da ficha de combate (o Motor IV: nível × 2)
        g = FC['fichas'][nome]; dv = para - de
        g['pv'] = int(g.get('pv', 0)) + 2 * dv; g['nivel'] = para; g['nivel_ref'] = para
        out.append(f"   G39 · {nome}: a ficha de combate sobe junto: PV +{2 * dv} → {g['pv']} (o ataque e a defesa não sobem com o nível)")
        grava('fichas_combate.json', FC)
    N = carrega('npcs.json', {}); v = N.get(nome, {})
    fx_antes, fx_agora = faixa(de), faixa(para)   # (b) a CLASSE na faixa nova: a Prova (d6, 3-6 passa; 1-2 tenta no próximo tick)
    cl = v.get('classe_livro')
    pend = v.get('prova_pendente')
    L = _classes_do_livro() if cl else {}
    atual = L.get(sem_acento(cl or '').lower())
    norm = lambda s: sem_acento(s or '').lower()[:4]
    rar_i = next((i for i, x in enumerate(ORDEM_RAR) if norm(x) == norm((atual or {}).get('raridade'))), -1)
    if cl and atual and (fx_agora != fx_antes or pend) and ORDEM_RAR.index(fx_agora) > rar_i:
        fam = atual.get('familia')
        opcoes = [c for c in L.values() if c.get('familia') == fam and sem_acento(c.get('raridade', '')).lower().startswith(sem_acento(fx_agora).lower()[:4])]
        r = d(6)
        if r <= 2:
            v['prova_pendente'] = fx_agora
            out.append(f"   G39 · {nome}: a faixa {fx_agora} pede a PROVA da classe: d6 [{r}] → ainda não (tenta de novo no próximo tick)")
        elif not opcoes:
            v['prova_pendente'] = fx_agora
            out.append(f"   G39 · {nome}: d6 [{r}] passou a Prova, mas o Livro não tem classe {fx_agora} na família {fam or '?'}: o Mestre gera (classe.py faltam)")
        else:
            nova = opcoes[d(len(opcoes)) - 1]
            v.setdefault('assinaturas_antigas', []).extend(v.get('assinaturas', []))
            v['classe_livro'] = nova['nome']; v['classe_raridade'] = fx_agora; v['assinaturas'] = nova.get('assinaturas', [])
            v['fraqueza'] = nova.get('fraqueza', v.get('fraqueza', '')); v.pop('prova_pendente', None)
            v.setdefault('log', []).append(f"Dia {dia}: G39: a PROVA da faixa {fx_agora} (d6 [{r}]): a classe sobe de {cl} para {nova['nome']}; as assinaturas antigas ficam")
            out.append(f"   G39 · {nome}: d6 [{r}] PASSA A PROVA: a classe sobe de {cl} para {nova['nome']} ({fx_agora}, {fam}); as assinaturas antigas ficam")
            anota(f"- G39 [Dia {dia}] {nome}: a classe sobe de {cl} para {nova['nome']} ({fx_agora}) pela Prova (d6 [{r}])")
        N[nome] = v; grava('npcs.json', N)
    if any(de < m <= para for m in (100, 200, 300)):   # (c) o DESPERTAR
        lin = [l for l in roda('despertar.py', 'rola').split('\n') if l.strip()]
        out += ['   G39 · o DESPERTAR: ' + l for l in lin] or [f'   G39 · {nome}: o Despertar já estava rolado']
    if nome in FC.get('fichas', {}) and any(de < m <= para for m in (50, 150, 200, 250, 300)):   # (d) as ARTES DE ARMA
        lin = [l for l in roda('artes.py', 'aplica', nome).split('\n') if l.strip()]
        out += ['   G39 · as ARTES: ' + l for l in lin[:4]]
    return out


# ─────────────────────────── 3. AS PENDÊNCIAS (o tick.py chama todo dia) ───────────────────────────
def pendencias(dias=7, dia=None):
    dia = int(dia or dia_atual() or 0); out = []
    A = carrega('agenda.json', {'itens': []})
    for it in A.get('itens', []):
        if it.get('feito'): continue
        t = it.get('texto', ''); di = it.get('dia') or 0
        if it.get('oculto') or t.startswith('(OCULTO'): t = '(OCULTO: o texto está na agenda e no envelope; não vai à mesa)'   # 508 (erro achado): o resumo do tick vai à mesa
        casa = it.get('para') or 'PRAZO' in t.upper() or it.get('tipo') in ('marco', 'fio')
        if not casa or it.get('tipo') == 'noticia': continue
        if dia <= di <= dia + dias:
            out.append(f"⚠ PRAZO em {di - dia} dia(s) (#{it['id']}, Dia {di}): {t[:160]}")
        elif di < dia and ('PRAZO' in t.upper() or it.get('para')):
            out.append(f"⚠ PRAZO VENCIDO há {dia - di} dia(s) (#{it['id']}, Dia {di}): {t[:160]}")
    F = carrega('ficha.json', {})
    for e in F.get('escolhas_pendentes', []):
        out.append(f"⚠ ESCOLHA DO JOGADOR por fazer: {e}")
    N = carrega('npcs.json', {})
    FC = carrega('fichas_combate.json', {'fichas': {}}).get('fichas', {})
    for n, v in N.items():
        if __import__('nucleo').morto(v): continue
        nv = v.get('nivel') or 0
        precisa = sum(1 for m in (100, 200, 300) if nv >= m)
        if precisa > len(v.get('dons', [])) and n in FC:
            out.append(f"⚠ {n} ({nv}) tem {len(v.get('dons', []))} Dom de {precisa}: o Despertar falta (despertar.py rola)")
        if n in FC and FC[n].get('nivel_ref') and nv and nv != FC[n]['nivel_ref']:
            out.append(f"⚠ a ficha de combate de {n} é do nível {FC[n]['nivel_ref']}; o nível de hoje é {nv} (encadeia.py sincroniza)")
        if v.get('prova_pendente'):
            out.append(f"⚠ {n}: a Prova da faixa {v['prova_pendente']} ainda por passar (o próximo tick tenta)")
    Fr = carrega('ficha.json', {}); fr = FC.get('Ferir')   # 507 (G9): o PV de combate do rei contra o da ficha
    if Fr and fr and fr.get('pv') != Fr.get('pv', [0, 0])[1]:
        out.append(f"⚠ a ficha de combate do rei tem PV {fr.get('pv')}; a ficha diz {Fr['pv'][1]} (encadeia.py sincroniza)")
    R = carrega('reino.json', {'cidades': []})   # 502 (erro achado): mod com chave fora dos pilares ou prazo sem data nunca vence nem conta
    for c in R.get('cidades', []):
        for pl, lst in c.get('mods', {}).items():
            for v, m in lst:
                if pl not in c.get('pilares', {}):
                    out.append(f"⚠ {c['nome']}: o modificador '{m[:60]}' está na chave '{pl}', fora dos pilares (não conta)")
                elif not re.search(r'até o \d+', m) and re.search(r'\bsemanas?\b|\bdias\b|\blua\b', m) and 'enquanto' not in m and 'de vez' not in m:
                    out.append(f"⚠ {c['nome']} {pl} {v:+d}: '{m[:60]}' tem prazo sem 'até o N' (nunca vence)")
    fz = carrega('estado.json', {}).get('forcados')   # 503 (G41): o desconto da G6 acaba abaixo de 44
    if fz and fz.get('n', 0) < 50:
        out.append(f"⚠ G6/G41: os forçados são {fz['n']}; com menos de 44 o desconto das obras do reino acaba")
    return out


def sincroniza():
    N = carrega('npcs.json', {}); FC = carrega('fichas_combate.json', {'fichas': {}}); out = []
    for n, g in FC.get('fichas', {}).items():
        nv = (N.get(n) or {}).get('nivel')
        if n == 'Ferir' or not nv or not g.get('nivel_ref') or nv == g['nivel_ref']: continue
        dv = nv - g['nivel_ref']; g['pv'] = int(g['pv']) + 2 * dv; out.append(f"{n}: nível {g['nivel_ref']} → {nv}: PV {'+' if dv >= 0 else ''}{2 * dv} → {g['pv']}")
        g['nivel_ref'] = nv; g['nivel'] = nv
    grava('fichas_combate.json', FC)
    if out: anota(f"- G39 [Dia {dia_atual()}] SINCRONIA DAS FICHAS DE COMBATE (o PV pelo nível de hoje): " + ' · '.join(out))
    try:   # 507 (G9, erro achado): o rei não está no npcs.json; o PV de combate dele segue o ficha.json
        F = carrega('ficha.json', {}); FCx = carrega('fichas_combate.json', {'fichas': {}})
        fr = FCx['fichas'].get('Ferir')
        if F and fr and (fr.get('pv') != F['pv'][1] or fr.get('nivel_ref') != F['nivel'] or fr.get('nivel') != F['nivel']):
            out.append(f"Ferir: PV de combate {fr.get('pv')} → {F['pv'][1]} (nível {F['nivel']})"); fr['pv'] = F['pv'][1]; fr['nivel_ref'] = F['nivel']; fr['nivel'] = F['nivel']; grava('fichas_combate.json', FCx)
    except Exception as ex:
        out.append(f'⚠ a ficha de combate do rei não sincronizou: {ex}')
    return out


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    if a[0] == 'pendencias':
        L = pendencias(int(a[1]) if len(a) > 1 else 7)
        print('\n'.join(L) if L else 'nada para trás nem vencendo nos próximos dias.')
    elif a[0] == 'sincroniza':
        L = sincroniza(); print('\n'.join(L) if L else 'todas as fichas já estão no nível de hoje.')
    else:
        sys.exit(__doc__)
