#!/usr/bin/env python3
"""m2_ano.py — MEDIDA (projeto B, etapa 3): um ano da gente que responde, em volta da vila de teste, com o motor de hoje e o protótipo do projeto B.

Roda de dentro de motor10/:
  PYTHONDONTWRITEBYTECODE=1 python3 projeto/etapa3/projeto_b/medidas/m2_ano.py RASCUNHO DIAS atento|mudo [cow] [semente=N]
Cria em RASCUNHO/m2_MODO_N a vila de teste (ferreiro, com a magia e a 4b), o arremedo da região (16 lugares, 24 rotas), uns 150 nomeados com papel, laços e bolsa,
e o personagem vive DIAS dias: come, serve o jornal da forja (2 blocos), dorme 2. O ATENTO responde a caixa (aceita a encomenda que a forja dele faz, pega a missão
de levar, paga a cobrança, aceita a oferta), forja e entrega; o MUDO nunca responde. `cow`: o gravador que só copia o que toca (cow.py) no lugar do de hoje.
Mede: o tempo por dia, o peso do save, a caixa (quantos, quantos vencem, o máximo aberto), a opinião média, a fama, a renda, as encomendas, as missões, as notícias,
a prata do mundo (tem de fechar) e o tamanho das seções do projeto B na MESA.
"""
import os, sys, time, shutil, json, contextlib, io
sys.path.insert(0, os.getcwd()); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    a = sys.argv[1:]; op = dict(x.split('=', 1) for x in a if '=' in x); pos = [x for x in a if '=' not in x]
    rasc, dias, modo = pos[0], int(pos[1]), pos[2]; usa_cow = 'cow' in pos; sem = int(op.get('semente', 1)); preco = float(op.get('preco', 1.0))
    pasta = os.path.join(rasc, f'm2_{modo}_{sem}_{preco:g}_{op.get("demanda", "")}{op.get("fama", "")}{op.get("dados", "")}' + ('_cow' if usa_cow else '')); shutil.rmtree(pasta, ignore_errors=True)
    os.environ['MOTOR10_MUNDO'] = pasta
    import vila_teste, estado, ato, oficio, mercado, cow
    import proto_b as P, tab_b as G
    if usa_cow: cow.instala()
    if op.get('dados'):                                   # o dado do jogador com semente (só para conferir que os dois gravadores dão o mesmo mundo)
        import random, teste
        rr = random.Random(int(op['dados']))
        def d20x():
            t = [rr.randint(1, 20)]
            while t[-1] == 20: t.append(rr.randint(1, 20))
            return t
        teste.d20x = d20x
    with contextlib.redirect_stdout(io.StringIO()):
        vila_teste.main([pasta, 'comeco=ferreiro', 'inclinacao=forja', 'inclinacao2=encanto', f'semente={sem}'])
        vila_teste.main(['magia', pasta]); vila_teste.main(['fantasia', pasta])
    E = estado.carrega(); B = P.B_novo(); P.AQUI_RASC = pasta
    t0 = time.time(); P.regiao(E); P.povoa(E, B); t_gera = time.time() - t0
    if preco != 1.0: P.gb(B, 'eu')['preco'] = preco
    if op.get('demanda') == 'alta': G.QUEBRA = 0.3; G.GASTA = 0.4; G.MISSAO_GASTA = 5
    if op.get('fama'): G.FAMA_ESFRIA = 10 ** 6; P.bgrava(E, B, 'mestre', [['fama', 'eu', k, 'ofício', 'soma', int(op['fama'])] for k, l in E['lugares'].items() if l.get('pop')])
    prata0 = mercado.prata_do_mundo(E); lug0 = {k: l['estoque'].get('prata', 0) for k, l in E['lugares'].items() if l.get('pop')}; vila0 = E['lugares']['vila']['estoque'].get('prata', 0); eu0 = E['gente']['eu']['moedas']
    ev0 = E['relogio']['eventos']; n_nom = len(P.nomeados(E, B))
    estado.grava(E); P.B_grava(B, pasta)
    tam0 = {k: os.path.getsize(os.path.join(pasta, k)) for k in os.listdir(pasta) if k.endswith('.json') or k.endswith('.jsonl')}
    R = dict(jornal=0, levar=0, forjas=0, forja_ok=0, materia=0, vendeu=0, caixa_max=0, caixa_soma=0, recusas=0)
    ultimo = None; t1 = time.time(); dia_fim = E['relogio']['dia'] + dias; tb = (E['gente']['eu'].get('treino') or {}).get('forja', 0)

    def tenta(f, *x, **k):
        try: return f(*x, **k)
        except SystemExit as e: R['recusas'] += 1; return None

    while E['relogio']['dia'] < dia_fim:
        if E['relogio']['dia'] != ultimo:
            ultimo = E['relogio']['dia']; tg = time.time()
            if 'sem_b' not in pos: P.gente_dia_tudo(E, B)
            R['t_b'] = R.get('t_b', 0) + time.time() - tg
            n = len(B['caixa']['abertos']); R['caixa_max'] = max(R['caixa_max'], n); R['caixa_soma'] += n
        eu = E['gente']['eu']
        if eu['estado'] != 'vivo': break
        if modo == 'atento':
            for cid, c in sorted(B['caixa']['abertos'].items()):
                if c['m'] == 'encomenda':
                    pc = c['peca']; ok = pc['cat'] <= 1 and oficio.oficio_de(pc) == 'forja' and oficio.conta(E, 'eu', pc['cat'])['acerta'] >= 0.25
                    P.responde(E, B, cid, 'a' if ok else 'c')
                elif c['m'] == 'loja':
                    import math as _m
                    pc = c['peca']; molde = oficio.molde(pc['tipo'], 0, familia=pc.get('familia')); mat = oficio.materia_de(molde); antes = E['gente']['eu']['moedas']
                    for k, n in mat.items():
                        falta = n - (E['gente']['eu'].get('carga') or {}).get(k, 0)
                        if falta > 0: tenta(mercado.comprar, E, 'eu', k, falta)
                    R['materia_loja'] = R.get('materia_loja', 0) + antes - E['gente']['eu']['moedas']
                    Rf = tenta(oficio.forjar, E, 'eu', molde)
                    P.bgrava(E, B, 'caixa', [['caixa', cid, 'fecha', 'feitos']])
                    if Rf and Rf.get('fim') == 'acertou': P.entrega_loja(E, B, c, Rf['item'])
                elif c['m'] == 'conserto':
                    it = E['itens']['itens'].get(c['item']); P.responde(E, B, cid, 'a' if it and it['cat'] <= 1 else 'b')
                elif c['m'] == 'missao':
                    m = B['missoes']['itens'][c['missao']]; P.responde(E, B, cid, 'a' if m['tipo'] == 'levar' else 'b')
                else: P.responde(E, B, cid, 'a')
        for _ in range(3):
            if E['gente']['eu']['corpo']['fome'] >= 2: tenta(ato.comer, E, 'eu')
        pend = [(k, m) for k, m in sorted(B['missoes']['itens'].items()) if m['estado'] == 'pega' and m.get('quem') == 'eu']
        obra = oficio.obras_de(E, 'eu'); fez = False
        if obra: tenta(oficio.continua, E, 'eu'); fez = True
        elif pend and pend[0][1]['tipo'] == 'encomenda':
            mid, m = pend[0]; pc = m['peca']
            molde = oficio.molde(pc['tipo'], pc['cat'], familia=pc.get('familia'), material=pc.get('material'))
            mat = oficio.materia_de(molde); antes = eu['moedas']
            for k, n in mat.items():
                falta = n - (eu.get('carga') or {}).get(k, 0)
                if falta > 0: tenta(mercado.comprar, E, 'eu', k, falta)
            R['materia'] += antes - E['gente']['eu']['moedas']
            Rf = tenta(oficio.forjar, E, 'eu', molde); fez = True
            if Rf and Rf.get('fim'):
                R['forjas'] += 1
                it = E['itens']['itens'].get(Rf['item']) if Rf.get('item') else None
                if it and it['cat'] >= pc['cat'] and Rf['fim'] == 'acertou': P.entrega(E, B, mid, Rf['item']); R['forja_ok'] += 1
                elif it:
                    x = E['gente']['eu']['moedas']; tenta(mercado.vender_peca, E, 'eu', Rf['item']); R['vendeu'] += E['gente']['eu']['moedas'] - x
        elif pend and pend[0][1]['tipo'] == 'levar':
            mid, m = pend[0]; tenta(ato.esperar, E, 'eu', 2 * m.get('blocos', 2)); P.missao_fecha(E, B, mid, 'cumprida'); R['levar'] += m['paga']; fez = True
        x = E['gente']['eu']['moedas']; tenta(oficio.jornal, E, 'eu', 2); R['jornal'] += E['gente']['eu']['moedas'] - x
        P.fama_bancada(E, B, tb); tb = (E['gente']['eu'].get('treino') or {}).get('forja', 0)
        tenta(ato.dormir, E, 'eu', 2)
        if not fez: tenta(ato.esperar, E, 'eu', 2)
    t2 = time.time()
    estado.grava(E); P.B_grava(B, pasta)
    tam = {k: os.path.getsize(os.path.join(pasta, k)) for k in os.listdir(pasta) if k.endswith('.json') or k.endswith('.jsonl')}
    nd = E['relogio']['dia'] - (dia_fim - dias)
    prata1 = mercado.prata_do_mundo(E)
    vila = P.nomeados(E, B, 'vila'); todos = P.nomeados(E, B)
    opv = [P.opiniao(E, B, k) for k in vila]; opt = [P.opiniao(E, B, k) for k in todos]
    com_mem = sum(1 for k in todos if any(f[3] == 'eu' for f in P.gb(B, k)['mem']))
    mem_tam = [len(P.gb(B, k)['mem']) for k in todos]
    C = B['caixa']; S = P.STATS
    mesa = '\n'.join(P.mesa_b(E, B)); open(os.path.join(pasta, 'MESA_B.md'), 'w').write(mesa + '\n')
    print(f'== {modo}{" (cow)" if usa_cow else ""}, semente {sem}, o preço do personagem × {preco:g} {op.get("demanda", "")} {("fama " + op["fama"]) if op.get("fama") else ""}: {nd} dias, {n_nom} nomeados (a gente nasceu em {t_gera:.1f} s)')
    print(f'o dia da gente (proto_b.gente_dia_tudo, com as compras, as forjas fora de cena e os eventos do motor que ele faz): {R.get("t_b", 0) / max(1, nd) * 1000:.1f} ms por dia')
    print(f'tempo: {t2 - t1:.1f} s ({(t2 - t1) / max(1, nd) * 1000:.0f} ms por dia; o gravador B: {B["_conta"]["segundos"]:.2f} s em {B["_conta"]["eventos"]} eventos) · eventos do motor: {E["relogio"]["eventos"] - ev0} ({(E["relogio"]["eventos"] - ev0) / max(1, nd):.0f} por dia) · recusas do robô: {R["recusas"]}')
    print('o save no fim (KB): ' + ' · '.join(f"{k} {v / 1024:.0f}" for k, v in sorted(tam.items())) + f" · TOTAL {sum(tam.values()) / 1024:.0f} (no começo {sum(tam0.values()) / 1024:.0f})")
    print(f'a caixa: {C["seq"]} itens no ano ({C["seq"] / max(1, nd) * 7:.1f} por semana) · respondidos {C.get("feitos", 0)} · vencidos {C.get("vencidos", 0)} · forçados pelo oitavo {C.get("forcados", 0)} · aberta no fim {len(C["abertos"])} · no máximo {R["caixa_max"]} · em média {R["caixa_soma"] / max(1, nd):.1f}')
    print(f'a opinião sobre o personagem: em Pedra Rasa, média {sum(opv) / max(1, len(opv)):+.2f} ({len(opv)} nomeados; de {min(opv)} a {max(opv)}) · na região, média {sum(opt) / len(opt):+.2f} · {com_mem} de {len(todos)} lembram algo dele · memória: média {sum(mem_tam) / len(mem_tam):.1f} fatos, no máximo {max(mem_tam)}')
    fv = {e: P.fama_de(E, B, 'eu', 'vila', e) for e in ('ofício', 'feito', 'crime')}
    print(f'a fama em Pedra Rasa: {fv} · em Bom Porto: {dict((e, P.fama_de(E, B, "eu", "bomporto", e)) for e in ("ofício", "feito", "crime"))} · em Torre Alta: {dict((e, P.fama_de(E, B, "eu", "torre", e)) for e in ("ofício", "feito", "crime"))}')
    ganho = E['gente']['eu']['moedas'] - eu0
    print(f'a prata do personagem: {eu0} → {E["gente"]["eu"]["moedas"]} ({ganho / max(1, nd):+.2f} por dia) · jornal {R["jornal"]} ({R["jornal"] / max(1, nd):.2f}/dia) · sinais {S.get("sinal", 0)} + resto {S.get("enc_resto", 0)} − matéria {R["materia"]} + peça abaixo vendida {R["vendeu"]} = encomenda líquida {(S.get("sinal", 0) + S.get("enc_resto", 0) - R["materia"] + R["vendeu"]) / max(1, nd):+.2f}/dia · levar {R["levar"]} · cobranças pagas {S.get("cobrancas_pagas", 0)} · ofertas {S.get("ofertas", 0)}')
    print(f'a loja: o povo levou {S.get("freguesia", 0)} peças da prateleira (arremedo) · a loja pediu ao personagem {S.get("loja_eu", 0)} (pagou {S.get("loja_paga", 0)}; a matéria custou {R.get("materia_loja", 0)}) · a outros ferreiros {S.get("loja_npc", 0)}')
    print(f'os consertos pedidos ao personagem: {S.get("cons_eu", 0)} (pagaram {S.get("cons_paga", 0)}, a matéria custou {S.get("cons_materia", 0)})')
    print(f'as encomendas: ao personagem {S["enc_eu"]} (aceitas {S.get("enc_aceitas", 0)}, entregues {S.get("enc_entregues", 0)}, falhadas {S.get("enc_falhas", 0)}; forjas {R["forjas"]}, certas {R["forja_ok"]}) · aos ferreiros de nome {S["enc_npc"]} (feitas {S["enc_npc_ok"]}) · consertos {S["consertos"]}')
    print(f'as missões: {S["missoes"]} nasceram · nomeados cumpriram/falharam {S["missoes_npc"]} · morreram nelas {S["mortes_missao"]} · furtos de nomeados {S["furtos_npc"]} (pegos {S["furtos_npc_pegos"]}) · laços que viraram notícia {S["laco_noticia"]}')
    print(f'as notícias: {B["noticias"]["seq"]} nasceram ({B["noticias"]["seq"] / max(1, nd):.1f} por dia) · ativas no fim {len(B["noticias"]["ativas"])}')
    print(f'os quereres: {dict(sorted(S["querer"].items()))}')
    print(f'a prata do mundo: {prata0} → {prata1} ({"FECHA" if prata0 == prata1 else "NÃO FECHA"}) · Pedra Rasa: {vila0} → {E["lugares"]["vila"]["estoque"].get("prata", 0)} · a custódia: {E["lugares"]["custodia"]["estoque"].get("prata", 0)}')
    print('a prata dos lugares (começo → fim): ' + ' · '.join(f"{E['lugares'][k]['nome']} {v} → {E['lugares'][k]['estoque'].get('prata', 0)}" for k, v in lug0.items()))
    print(f'as seções do projeto B na MESA: {len(mesa.encode()) / 1024:.1f} KB ({pasta}/MESA_B.md)')
    P_ = estado.valida(E); print('o estado: ' + ('inteiro' if not P_ else 'QUEBRADO: ' + '; '.join(P_[:3])))


if __name__ == '__main__': main()
