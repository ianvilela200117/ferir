#!/usr/bin/env python3
"""m3_furto.py — MEDIDA (projeto B, etapa 3): o furto do capítulo 18.13, ligado com a memória, a vigia e a recusa de negócio. O robô ladino vive 30 dias em Pedra Rasa.

Roda de dentro de motor10/:  PYTHONDONTWRITEBYTECODE=1 python3 projeto/etapa3/projeto_b/medidas/m3_furto.py RASCUNHO [vidas=30] [dias=30] [mao=2] [agi=60] [sem_memoria]
O robô: come na taverna (se a taverneira ainda o serve; senão compra comida na loja, se o mercador o atende; senão passa fome), dorme na cama, e de manhã, de tarde e ao
entardecer vai ao ponto público onde está a bolsa mais gorda que ele ainda não tentou hoje e tenta o furto (um alvo por bloco; uma tentativa por alvo por dia).
O dado é o do jogador (2d20, o 20 rola de novo), com semente por vida. As regras do projeto B: a vítima que não viu dá pela falta na virada (60%) e desconfia de quem estava
no ponto; quem é pego paga o triplo ao caixa (sem prata, 3 dias preso); a vítima e quem estava ali lembram; a notícia sobe a fama de crime; cada falta descoberta põe +2 na
vigia do lugar por 28 dias (até +8); a fama de crime soma no número; quem tem opinião −6 ou pior não negocia com ele.
`sem_memoria`: a regra do 18.13 sozinha (o furto escrito e desligado), para comparar.
"""
import os, sys, time, shutil, contextlib, io, random, math
sys.path.insert(0, os.getcwd()); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    a = sys.argv[1:]; op = dict(x.split('=', 1) for x in a if '=' in x); pos = [x for x in a if '=' not in x]
    rasc = pos[0]; vidas = int(op.get('vidas', 30)); dias = int(op.get('dias', 30)); mao = int(op.get('mao', 2)); agi = int(op.get('agi', 60)); memoria = 'sem_memoria' not in pos
    jeito = op.get('jeito', 'guloso')        # guloso: furta sempre; prudente: para quando é pego ou quando a fama de crime chega a 10, e volta à jornada; diarista: nunca furta
    import vila_teste, estado, ato, mercado, cow
    import proto_b as P, tab_b as G
    cow.instala()
    tot = dict(leva=0, multa=0, preso=0, pegos=0, tentativas=0, certos=0, recusado=0, fome=0, morreu=0, d5=0)
    por_vida = []
    for v in range(vidas):
        pasta = os.path.join(rasc, f'm3_{v}'); shutil.rmtree(pasta, ignore_errors=True); os.environ['MOTOR10_MUNDO'] = pasta
        with contextlib.redirect_stdout(io.StringIO()):
            vila_teste.main([pasta, 'comeco=guerreiro', f'semente={v + 1}']); vila_teste.main(['magia', pasta]); vila_teste.main(['fantasia', pasta])
        E = estado.carrega(); B = P.B_novo(); P.STATS.clear(); P.STATS.update(enc_eu=0, enc_npc=0, enc_npc_ok=0, querer={}, missoes=0, missoes_npc=0, mortes_missao=0, furtos_npc=0, furtos_npc_pegos=0, noticias=0, consertos=0, laco_noticia=0)
        P.regiao(E); P.povoa(E, B)
        at = dict(E['gente']['eu']['atributos']); at['Agilidade'] = agi
        estado.aplica(E, 'mestre', [['pessoa', 'eu', 'maestria.manha', 'poe', mao], ['pessoa', 'eu', 'treino.manha', 'soma', {2: 40, 4: 160, 6: 500}.get(mao, 0)]], texto='medida: o ladino')
        E['gente']['eu']['atributos'] = at
        r = random.Random(1000 + v); eu0 = E['gente']['eu']['moedas']; ultimo = None; dia_fim = E['relogio']['dia'] + dias; preso_ate = -1
        leva = multa = preso = pegos = tent = certos = recusado = fome = 0; leva5 = 0; pendentes = []
        while E['relogio']['dia'] < dia_fim and E['gente']['eu']['estado'] == 'vivo':
            if E['relogio']['dia'] != ultimo:
                ultimo = E['relogio']['dia']
                # a virada da gente (a bolsa, o querer, as notícias); e quem foi furtado e não viu dá pela falta
                for (vit, bl, sp, nome_v) in pendentes:
                    rr = estado.sorte(E, f'falta|{vit}')
                    if memoria and rr.random() < G.DA_FALTA:
                        lid = 'vila'; presentes = [k for k in P.nomeados(E, B, lid) if k != vit and P.ponto(E, B, k, bl)[0] == sp] + ['eu']
                        x = min(0.9, (1 + P.fama_de(E, B, 'eu', lid, 'crime') / 10) / len(presentes) * (1.5 if P.opiniao(E, B, vit) < 0 else 1))
                        estado.aplica(E, 'mestre', [['lugar', lid, 'vigia', 'poe', (E['lugares'][lid].get('vigia') or [])[-3:] + [E['relogio']['dia']]]], onde=lid, texto='a vila fica de olho')
                        efb = P.noticia(E, B, lid, 'suspeita', None, f'sumiu prata da bolsa de {nome_v}', alcance=1)
                        if rr.random() < x: efb += P.lembra(E, B, vit, 'suspeita') + [['fama', 'eu', lid, 'crime', 'soma', G.FATOS['suspeita'][2]]]
                        P.bgrava(E, B, 'furto', efb)
                pendentes = []
                P.gente_dia_tudo(E, B)
            eu = E['gente']['eu']; d0 = E['relogio']['dia']
            if d0 <= preso_ate:
                try: ato.esperar(E, 'eu', 6)
                except SystemExit: pass
                preso += 0; continue
            # comer: a taverna, ou a loja, ou nada
            taver = next((k for k in P.nomeados(E, B, 'vila') if P.papel(B, k) == 'taverneiro'), None); merc = next((k for k in P.nomeados(E, B, 'vila') if P.papel(B, k) == 'mercador'), None)
            if eu['corpo']['fome'] >= 2:
                if not memoria or taver is None or P.opiniao(E, B, taver) > G.RECUSA_NEGOCIO:
                    try: ato.comer(E, 'eu')
                    except SystemExit: pass
                elif merc is None or P.opiniao(E, B, merc) > G.RECUSA_NEGOCIO:
                    recusado += 1
                    try: mercado.comprar(E, 'eu', 'comida', 1); ato.comer(E, 'eu', da_carga=True)
                    except SystemExit: pass
                else: recusado += 1; fome += 1
            tentados = set()
            parou = jeito == 'diarista' or (jeito == 'prudente' and (pegos or P.fama_de(E, B, 'eu', 'vila', 'crime') >= 10))
            alc = next((k for k in P.nomeados(E, B, 'vila') if P.papel(B, k) == 'alcaide'), None)
            if parou:
                if E['relogio']['bloco'] != 2:
                    try: ato.esperar(E, 'eu', (2 - E['relogio']['bloco']) % 6)
                    except SystemExit: pass
                if alc is None or P.opiniao(E, B, alc) > G.RECUSA_NEGOCIO:
                    x = E['gente']['eu']['moedas']
                    try: ato.trabalhar(E, 'eu', 2)
                    except SystemExit: pass
                    tot['jornal'] = tot.get('jornal', 0) + E['gente']['eu']['moedas'] - x
                else: recusado += 1
            for bl in ((2, 3, 4) if not parou else ()):
                if E['relogio']['bloco'] != bl:
                    try: ato.esperar(E, 'eu', (bl - E['relogio']['bloco']) % 6)
                    except SystemExit: pass
                if E['relogio']['bloco'] != bl or E['relogio']['dia'] != d0: break
                alvos = [k for k in P.nomeados(E, B, 'vila') if k not in tentados and P.ponto(E, B, k, bl)[0] not in ('casa', 'santuário', 'ermo', 'estrada') and E['gente'][k]['moedas'] > 0
                         and (not memoria or P.opiniao(E, B, k) > G.RECUSA_NEGOCIO)]
                if not alvos: continue
                vit = max(alvos, key=lambda k: E['gente'][k]['moedas'] / (1 + P.contra_furto(E, B, 'eu', k, bl) - 20)); tentados.add(vit); tent += 1
                c = P.contra_furto(E, B, 'eu', vit, bl) if memoria else (G.FURTO_CONTRA + E['gente'][vit]['atributos']['Percepção'] // 10 + (G.FURTO_GUARDA if P.papel(B, vit) in ('guarda', 'capitao', 'mercador') else 0))
                t = P.d2(r) + agi // 10 + mao
                n = min(E['gente'][vit]['moedas'], r.randint(1, 6) * (1 + mao // 2)); sp = P.ponto(E, B, vit, bl)[0]
                if t >= c:
                    certos += 1; leva += n; leva5 += n if d0 - (dia_fim - dias) < 5 else 0
                    estado.aplica(E, 'mestre', [['pessoa', vit, 'moedas', 'soma', -n], ['pessoa', 'eu', 'moedas', 'soma', n]], onde='vila', quem=['eu', vit], texto='furto')
                    pendentes.append((vit, bl, sp, E['gente'][vit]['nome']))
                elif c - t >= 5:
                    pegos += 1; m = 3 * n; tem = E['gente']['eu']['moedas']
                    if tem >= m: estado.aplica(E, 'mestre', [['pessoa', 'eu', 'moedas', 'soma', -m], ['estoque', 'vila', 'prata', 'soma', m]], onde='vila', quem=['eu'], texto='a multa do furto'); multa += m
                    else:
                        if tem: estado.aplica(E, 'mestre', [['pessoa', 'eu', 'moedas', 'soma', -tem], ['estoque', 'vila', 'prata', 'soma', tem]], onde='vila', quem=['eu'], texto='a multa do furto (o que tinha)'); multa += tem
                        preso_ate = E['relogio']['dia'] + G.FURTO_PRESO; preso += G.FURTO_PRESO
                    if memoria:
                        testem = [k for k in P.nomeados(E, B, 'vila') if k != vit and P.ponto(E, B, k, bl)[0] == sp][:4]
                        efb = P.lembra(E, B, vit, 'roubou') + [x for k in testem for x in P.lembra(E, B, k, 'viu_roubar')]
                        efb += P.noticia(E, B, 'vila', 'roubou', 'eu', f"pegaram o forasteiro com a mão na bolsa de {E['gente'][vit]['nome']}", 'crime', G.FATOS['roubou'][2], peso=-2)
                        estado.aplica(E, 'mestre', [['lugar', 'vila', 'vigia', 'poe', (E['lugares']['vila'].get('vigia') or [])[-3:] + [E['relogio']['dia']]]], onde='vila', texto='a vila fica de olho')
                        P.bgrava(E, B, 'furto', efb + [['fama', 'eu', 'vila', 'crime', 'soma', G.FATOS['roubou'][2]]])
                    if preso_ate >= E['relogio']['dia']: break
            try:
                if E['relogio']['dia'] == d0 and E['relogio']['bloco'] < 5: ato.esperar(E, 'eu', 5 - E['relogio']['bloco'])
                ato.dormir(E, 'eu', 2)
            except SystemExit:
                try: ato.dormir(E, 'eu', 2, chao=True)
                except SystemExit: pass
        morreu = E['gente']['eu']['estado'] != 'vivo'
        tot['leva'] += leva; tot['multa'] += multa; tot['preso'] += preso; tot['pegos'] += pegos; tot['tentativas'] += tent; tot['certos'] += certos; tot['recusado'] += recusado; tot['fome'] += fome; tot['morreu'] += morreu; tot['d5'] += leva5
        por_vida.append((leva - multa) / dias); tot['bolsa'] = tot.get('bolsa', 0) + E['gente']['eu']['moedas'] - eu0
        print(f'vida {v + 1}: levou {leva} em {certos} de {tent} tentativas; pego {pegos} vezes; multa {multa}; preso {preso} dias; recusado {recusado} vezes, com fome {fome} · fama de crime {P.fama_de(E, B, "eu", "vila", "crime")} · vigia +{P.vigia(E, B, "vila")} · {(leva - multa) / dias:+.2f} por dia' + (' · MORREU' if morreu else ''))
    n = vidas * dias
    print(f'\n== {vidas} vidas de {dias} dias · o {jeito} · mão {mao}, Agilidade {agi} · {"com a memória e a vigia (o projeto B)" if memoria else "SEM a memória (o 18.13 sozinho)"}')
    print(f'a bolsa do robô anda {tot.get("bolsa", 0) / n:+.2f} por dia (vida inteira: comida, cama, multa, jornada quando há) · a jornada rendeu {tot.get("jornal", 0) / n:.2f} por dia')
    print(f'o furto rende {(tot["leva"] - tot["multa"]) / n:+.2f} de prata por dia (levou {tot["leva"] / n:.2f}, multas {tot["multa"] / n:.2f}); nos 5 primeiros dias, {tot["d5"] / (vidas * 5):.2f} por dia; contando os dias presos como diária perdida (4): {(tot["leva"] - tot["multa"] - 4 * tot["preso"]) / n:+.2f}')
    por_vida.sort(); print(f'por vida: a pior {por_vida[0]:+.2f}, a mediana {por_vida[len(por_vida) // 2]:+.2f}, a melhor {por_vida[-1]:+.2f} · tentativas {tot["tentativas"]}, certas {tot["certos"]}, pego {tot["pegos"]} · preso {tot["preso"]} dias · recusado {tot["recusado"]} vezes · morreu {tot["morreu"]}')


if __name__ == '__main__': main()
