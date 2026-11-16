#!/usr/bin/env python3
"""cancao.py — G28, AS CANÇÕES DE FEITO (Livro Nove 11; MOTOR 9.1, Dia 438): um feito grande só vira poder quando o mundo o canta.

  O QUE CONTA (tipo=): lendario (matar um Lendário ou acima) · guerra (vencer uma guerra) · primordial (forjar uma peça Primordial) ·
                       masmorra (limpar PRIMEIRO uma masmorra Única ou acima) · cidade (salvar ou perder uma cidade)
  QUEM CANTA: um bardo da casa (classe VOZ: cantor=NOME) ou um contratado (cantor=contratado: 500 do cofre). O Cantor de Feitos soma +5.
  O DADO (d20 + Fama do rei, pelo selo, declarado antes):
     até 5    a canção não pega
     6 a 15   pega na região: reputação +5 nas cidades dela (padrão: as cidades do reino)
     16 a 19  CORRE O MUNDO: Fama +1 e +1 PERMANENTE num atributo ligado ao feito (o jogador escolhe entre os DOIS que o Mestre oferece: oferece=A,B)
     20+      tudo isso e um TÍTULO COM EFEITO (G22: o Mestre escreve o título pela ficção e grava com habilidades.py titulo)
  LIMITE: uma canção por lua. PREÇO (Lei 6): cada canção que corre o mundo anda 1 no relógio de um rival ou inimigo que também a ouviu
          (o script declara no selo a lista dos que podem ouvir e rola quem).
  A FAMA (0 a 7, Motor VIII.2 e XII.7): a canção sobe até 5 (além do reino); a 6 (lenda viva) e a 7 (mito) só pelas condições do Motor XII.7
          (feito que muda o mundo; um Lendário morto pela mão dele): o Mestre sobe à mão com ficha.py set fama N.

Uso:
  python3 cancao.py ver
  python3 cancao.py canta "O FEITO" tipo=lendario|guerra|primordial|masmorra|cidade cantor=NOME|contratado oferece=Atr1,Atr2 [cidades="Ireviel (a cidade),Levis (a cidade)"] [mais=N "motivo"]
  python3 cancao.py atributo NOME_DO_ATRIBUTO      o jogador escolheu (um dos dois oferecidos): +1 permanente
"""
import subprocess, sys
from nucleo import carrega, grava, anota, dia_atual, calendario, sem_acento, P

ARQ = 'cancoes.json'
TIPOS = {'lendario': 'matar um Lendário ou acima', 'guerra': 'vencer uma guerra', 'primordial': 'forjar uma peça Primordial',
         'masmorra': 'limpar primeiro uma masmorra Única ou acima', 'cidade': 'salvar ou perder uma cidade'}


def roda(script, *args):
    r = subprocess.run([sys.executable, P(script)] + [str(x) for x in args], capture_output=True, text=True)
    out = (r.stdout + r.stderr).strip()
    if out: print('    ' + out.replace('\n', '\n    '))
    return out


def opt(a, k, padrao=None):
    return next((x[len(k) + 1:] for x in a if x.startswith(k + '=')), padrao)


def lua_de(dia):
    c = calendario(dia); return f"{c['ano']}-{c['lua']}"


def rivais():
    """quem pode ouvir a canção e andar 1: os relógios vivos e visíveis do relogios.json e as OBRAS dos Lendários com quem a casa está mal (reputação −25 ou pior)"""
    out = []
    for r in carrega('relogios.json', {'relogios': []})['relogios']:
        if r.get('estado') == 'vivo' and not r.get('oculto'): out.append(('relogio', r['nome'], f"o relógio {r['nome']} ({r['valor']}/{r['max']})"))
    M = carrega('mundo_vivo.json', {}); rep = M.get('reputacao', {})
    for i, l in enumerate(M.get('lendarios', [])):
        if 'MORT' in str(l.get('estado', '')).upper(): continue
        n = sem_acento(l['nome'].split(',')[0])
        v = next((x['valor'] for k, x in rep.items() if n.split()[0] in sem_acento(k)), 0)
        if v <= -25: out.append(('lendario', i, f"{l['nome']}: a obra '{l.get('obra', '?')}' ({l['relogio'][0]}/{l['relogio'][1]})"))
    return out


def main():
    a = sys.argv[1:]; S = carrega(ARQ, {'nota': 'G28: as canções de feito da casa (cancao.py).', 'cancoes': [], 'pendente': None}); dia = dia_atual(); F = carrega('ficha.json')
    if not a or a[0] == 'ver':
        if not a: print(__doc__)
        print(f"AS CANÇÕES DE FEITO (G28) · Fama do rei {F.get('fama', '?')}/7 · canção desta lua: " + ('JÁ CANTADA' if any(c['lua'] == lua_de(dia) for c in S['cancoes']) else 'livre'))
        for c in S['cancoes']: print(f"  Dia {c['dia']}: \"{c['feito']}\" ({c['cantor']}) d20 {c['total']} → {c['grau']}")
        if S.get('pendente'): print(f"  ⚠ FALTA O JOGADOR ESCOLHER o atributo: {' ou '.join(S['pendente']['oferece'])} (cancao.py atributo NOME)")
        return
    if a[0] == 'atributo' and len(a) > 1:
        pe = S.get('pendente') or sys.exit('não há atributo para escolher.')
        at = next((x for x in pe['oferece'] if sem_acento(x) == sem_acento(a[1])), None) or sys.exit(f"tem de ser um dos dois oferecidos: {' ou '.join(pe['oferece'])}")
        k = next((x for x in F['atributos'] if sem_acento(x) == sem_acento(at)), None) or sys.exit(f'atributo que a ficha não tem: {at}')
        roda('ficha.py', 'set', f'atributos.{k}', F['atributos'][k] + 1, f"+1 PERMANENTE: a canção \"{pe['feito']}\" correu o mundo (G28)")
        S['pendente'] = None; grava(ARQ, S); return
    if a[0] != 'canta' or len(a) < 2: sys.exit(__doc__)
    feito = a[1]; tipo = sem_acento(opt(a, 'tipo', '')); cantor = opt(a, 'cantor'); ofe = [x.strip() for x in (opt(a, 'oferece') or '').split(',') if x.strip()]
    if tipo not in TIPOS: sys.exit('tipo= tem de ser um destes (o que conta, Livro Nove 11): ' + ' · '.join(f'{k} ({v})' for k, v in TIPOS.items()))
    if not cantor: sys.exit('cantor=NOME (um bardo da casa, classe VOZ) ou cantor=contratado (500)')
    if len(ofe) != 2: sys.exit('oferece=Atr1,Atr2: os DOIS atributos ligados ao feito, entre os quais o jogador escolhe se a canção correr o mundo (declarados ANTES do dado)')
    if any(c['lua'] == lua_de(dia) for c in S['cancoes']): sys.exit(f"LIMITE: já houve uma canção nesta lua ({calendario(dia)['txt']}). Nada foi rolado.")
    if S.get('pendente'): sys.exit('a canção anterior ainda espera o jogador escolher o atributo (cancao.py atributo NOME).')
    bonus = int(F.get('fama', 0)); txt_b = [f"Fama {bonus}"]
    if sem_acento(cantor) == 'contratado':
        if F['cofre'] < 500: sys.exit('o cofre não tem os 500 do cantor contratado.')
        roda('ficha.py', 'cofre', '-500', f'o cantor contratado da canção "{feito}" (G28)')
    else:
        N = carrega('npcs.json', {}); k = next((x for x in N if sem_acento(x) == sem_acento(cantor)), None) or sys.exit(f'{cantor} não está no livro dos NPCs (npc.py busca)')
        cl = sem_acento(str(N[k].get('classe', '')) + ' ' + str(N[k].get('classe_livro', '')))
        if 'cantor de feitos' in cl: bonus += 5; txt_b.append('Cantor de Feitos +5')
        elif 'voz' not in cl and not any(x in cl for x in ('bardo', 'menestrel', 'arauto', 'orador')): sys.exit(f'{k} não é da família VOZ (classe: {N[k].get("classe")}). Use um bardo ou cantor=contratado.')
        cantor = k
    mais = int(opt(a, 'mais', 0) or 0)
    if mais: bonus += mais; txt_b.append(f'apoio {mais:+d}')
    R = rivais()
    import selo
    Z = selo.load(); base = f"CF{dia}"
    tab = ' | '.join(['1-5: a canção não pega', '6-15: pega na REGIÃO: reputação +5 nas cidades dela', '16-19: CORRE O MUNDO: Fama +1 e +1 permanente em ' + ' ou '.join(ofe) + ' (o jogador escolhe); um rival a ouve',
                      '20+: CORRE O MUNDO e um TÍTULO COM EFEITO (G22); um rival a ouve'])
    sid = selo.declara(Z, base if base not in Z['selos'] else '-', f'A CANÇÃO DE FEITO "{feito}" ({TIPOS[tipo]}; cantor: {cantor}; ' + ' · '.join(txt_b) + ')', f'd20+{bonus}', tab, selo.opcoes([]))
    sr = None
    if R:   # o preço da Lei 6 também é declarado ANTES do dado da canção
        sr = selo.declara(Z, '-', f'SE A CANÇÃO \"{feito}\" CORRER O MUNDO, QUEM A OUVE E ANDA 1 (Lei 6)', f'd{len(R)}', ' | '.join(f'{i + 1}: {r[2]}' for i, r in enumerate(R)), selo.opcoes([]))
    rr = selo.rola(Z, sid)['rolagens'][-1]; t = rr['total']
    grau = 'não pega' if t <= 5 else 'REGIÃO' if t <= 15 else 'CORRE O MUNDO' if t <= 19 else 'CORRE O MUNDO E UM TÍTULO'
    S['cancoes'].append({'dia': dia, 'lua': lua_de(dia), 'feito': feito, 'tipo': tipo, 'cantor': cantor, 'total': t, 'grau': grau})
    if 6 <= t <= 15:
        cids = [x.strip() for x in (opt(a, 'cidades') or '').split(',') if x.strip()] or [k for k in carrega('mundo_vivo.json', {}).get('reputacao', {}) if '(a cidade)' in k]
        for c in cids: roda('reputacao.py', 'muda', c, 5, f'a canção "{feito}" pegou na região (G28)')
    if t >= 16:
        fa = int(F.get('fama', 0))
        if fa < 5: roda('ficha.py', 'set', 'fama', fa + 1, f'a canção "{feito}" correu o mundo (G28)')
        else: print(f'  FAMA {fa}: a canção não passa de 5; a 6 e a 7 só pelas condições do Motor XII.7 (o Mestre decide: ficha.py set fama N)')
        S['pendente'] = {'feito': feito, 'oferece': ofe, 'dia': dia}
        print(f"  ★ +1 PERMANENTE: o JOGADOR escolhe entre {ofe[0]} e {ofe[1]} → python3 cancao.py atributo NOME")
        if sr:
            r2 = selo.rola(Z, sr)['rolagens'][-1]['total']; tp, ref, txt = R[r2 - 1]
            if tp == 'relogio': roda('relogio.py', 'anda', ref, '+1', f'ouviu a canção "{feito}" (G28, Lei 6)')
            else:
                M = carrega('mundo_vivo.json'); L = M['lendarios'][ref]; L['relogio'][0] = min(L['relogio'][1], L['relogio'][0] + 1); grava('mundo_vivo.json', M)
                anota(f"- CANÇÃO (G28): {L['nome']} ouviu \"{feito}\": a obra anda 1 → {L['relogio'][0]}/{L['relogio'][1]}"); print(f"    {L['nome']}: a obra anda 1 → {L['relogio'][0]}/{L['relogio'][1]}")
        if t >= 20: print('  ★ TÍTULO COM EFEITO (G22): o Mestre escreve o título pela ficção (efeito pequeno e estreito) → python3 habilidades.py titulo "Nome" "efeito" "a canção"; e guildas.py fama casa +1')
    if sr and t < 16:   # a canção não correu o mundo: ninguém ouviu; o selo do rival fecha sem dado
        Z = selo.load(); Z['selos'][sr]['estado'] = 'nao_usado'; selo.save(Z); anota(f"- SELO ({sr}) sem dado: a canção não correu o mundo; nenhum rival a ouviu")
    grava(ARQ, S)
    anota(f"- CANÇÃO DE FEITO (G28) [Dia {dia}]: \"{feito}\" ({cantor}) → {grau}")


if __name__ == '__main__':
    main()
