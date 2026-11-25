#!/usr/bin/env python3
"""m3_ano_da_regiao.py — MEDIDA (projeto A, etapa 3): a região nasce em volta de uma CÓPIA do ensaio/ e vive um ano sem o personagem (ele só espera e come em Pedra Rasa).
Mede: o tempo por dia, os eventos e os bytes do registro, o tamanho do estado; a prata do mundo (fecha?), a prata de cada povoado (caixa e bolsa), o preço da comida
em cada um ao longo do ano, a freguesia e a forja do povo, a caça do povo e a contagem dos ermos, o bicho que sai, a fome, a migração, o bando, o perigo das rotas.

Roda de dentro de motor10/:  PYTHONDONTWRITEBYTECODE=1 python3 projeto/etapa3/projeto_a/medidas/m3_ano_da_regiao.py COPIA_DO_ENSAIO [dias=364] [sementes=1,2,3] [gravador=toque|hoje]
COPIA_DO_ENSAIO: uma cópia do ensaio/ no rascunho (só é lida; o mundo anda em memória e nada é gravado).
"""
import copy, json, os, sys, time
sys.path.insert(0, os.getcwd()); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
a = sys.argv[1:]
if not a: print(__doc__); sys.exit()
os.environ['MOTOR10_MUNDO'] = os.path.abspath(a[0]); op = dict(x.split('=', 1) for x in a[1:] if '=' in x)
DIAS = int(op.get('dias', 364)); EU = op.get('eu', 'espera'); SEMS = [int(x) for x in op.get('sementes', '1,2,3').split(',')]; GRAV = op.get('gravador', 'toque')
import estado, ato, mercado, caca
import tabelas_mundo as M, tabelas_mercado as C
import proto_aplica, proto_regiao as R

R.instala()
for k, v in op.items():         # (medida) tab.CHAVE=valor muda um número da página do protótipo: tab.SAFRA_REGIAO=0.65,0.7
    if k.startswith('tab.'): x = [float(y) for y in v.split(',')]; R.TAB[k[4:]] = tuple(x) if len(x) > 1 else x[0]
if GRAV == 'hoje':      # o gravador de hoje, com o verbo 'rota' por fora (o protótipo só para medir o custo da cópia inteira)
    _velho_um = estado._um
    def _um(E, ef): return R._rota_um(E, ef) if ef and ef[0] == 'rota' else _velho_um(E, ef)
    estado._um = _um; proto_aplica.desinstala()


class _Mod: pass
REG = _Mod(); REG.__name__ = 'proto_regiao'; REG.virada = R.virada


def um_ano(sem):
    E = estado.carrega(); E['rotas'] = {}; E['relogio']['semente'] = 1000 + sem; R.MEDE.pop('safra', None)      # (medida) cada semente, outro dado do mundo
    if GRAV == 'hoje' and 'rotas' not in estado.ARQS: estado.ARQS = tuple(estado.ARQS) + ('rotas',)
    estado.aplica(E, 'mestre', [['pessoa', 'eu', 'moedas', 'soma', 2000]], quem=['eu'], texto='(medida) o personagem ganha com que comer o ano todo')
    t = time.perf_counter(); info = R.gera(E, sem); t_gera = time.perf_counter() - t
    estado.modulos()
    if REG not in estado._MODS: estado._MODS.append(REG)
    tam0 = {k: len(json.dumps(E[k], ensure_ascii=False)) for k in tuple(estado.ARQS) + ('rotas',) if k in E}; R.MEDE['razoes'].clear(); R.MEDE['carreto'] = 0
    eu0 = E['gente']['eu']['moedas']; p0 = R.prata_do_mundo(E); povs = [k for k, l in E['lugares'].items() if mercado.tem_mercado(E, k) and k != 'fora']
    S = {k: dict(pop0=E['lugares'][k]['pop'], caixa0=E['lugares'][k]['estoque'].get('prata', 0), bolsa0=E['lugares'][k].get('bolsa', 0), fmin=9, fmax=0, cmin=10 ** 9, cmax=0, fome=0) for k in povs}
    ermos = [k for k, l in E['lugares'].items() if l.get('tipo') == 'ermo' and caca.tem_caca(E, k)]
    E0 = {k: dict(caca.bichos_de(E, k)) for k in ermos}; Emin = copy.deepcopy(E0)
    perigo0 = {rid: R.perigo_rota(E, rt) for rid, rt in E['rotas'].items()}
    eu = 'eu'; nev = 0; bytes_ev = 0; liq = {}; bytes_liq = 0; tipos_ev = {}; fregues = 0; refaz = 0; sai = 0; t = time.perf_counter(); fomes = []; txt_sem = []
    for d in range(DIAS):
        for _ in range(6):
            if E['gente'][eu]['corpo']['fome'] >= 3:
                try: ato.comer(E, eu)
                except SystemExit: pass
            b_ = E['relogio']['bloco']
            if EU == 'trabalha' and b_ in (0, 1):
                try: ato.dormir(E, eu, 1, para=False)
                except SystemExit: ato.passa(E, eu, 1, 'esperar', texto='espera', para=False)
            elif EU == 'trabalha' and b_ in (2, 3) and ato.jornada(E, eu) < 2:
                try: ato.trabalhar(E, eu, 1)
                except SystemExit: ato.passa(E, eu, 1, 'esperar', texto='espera', para=False)
            else: ato.passa(E, eu, 1, 'esperar', texto='espera', para=False)
            for ev in E['_novos']:
                nev += 1; b = len(json.dumps(ev, ensure_ascii=False)); bytes_ev += b
                if ev['tipo'] in ('producao', 'consumo'):
                    k_ = (ev['dia'], ev['onde']); d_ = liq.setdefault(k_, {})
                    for x in ev['efeitos']: d_[x[2]] = d_.get(x[2], 0) + x[4]
                else: bytes_liq += b
                tipos_ev[ev['tipo']] = tipos_ev.get(ev['tipo'], [0, 0]); tipos_ev[ev['tipo']][0] += 1; tipos_ev[ev['tipo']][1] += b
                if ev['tipo'] == 'regiao':
                    fregues += sum(1 for x in ev['efeitos'] if x[0] == 'item' and x[2] == 'some'); refaz += sum(1 for x in ev['efeitos'] if x[0] == 'item' and x[1] == 'nasce')
                    if ev['texto'].startswith('a semana'): txt_sem.append(f"Dia {ev['dia']}: {ev['texto'][19:]}")
            E['_novos'] = []
        for k in povs:
            l = E['lugares'][k]; f = mercado.fator(E, k, 'comida'); s = S[k]; s['fmin'] = min(s['fmin'], f); s['fmax'] = max(s['fmax'], f)
            cx = l['estoque'].get('prata', 0) + int(l.get('bolsa') or 0); s['cmin'] = min(s['cmin'], cx); s['cmax'] = max(s['cmax'], cx)
            if l['estoque'].get('comida', 0) / max(1, l['pop']) < R.TAB['FOME_DIAS']: s['fome'] += 1
        for k in ermos:
            for e, q in caca.bichos_de(E, k).items(): Emin[k][e] = min(Emin[k].get(e, q), q)
            for e in E0[k]:
                if e not in caca.bichos_de(E, k): Emin[k][e] = 0
    dt = time.perf_counter() - t
    for (dia_, onde_), d_ in liq.items():
        bytes_liq += len(json.dumps(dict(id=99999, dia=dia_, bloco=0, tipo='mercado', onde=onde_, quem=[], efeitos=[['estoque', onde_, k, 'soma', v] for k, v in d_.items() if v], texto=f'o dia do mercado'), ensure_ascii=False))
    tam1 = {k: len(json.dumps(E[k], ensure_ascii=False)) for k in tuple(estado.ARQS) + ('rotas',) if k in E}
    P = estado.valida(E); p1 = R.prata_do_mundo(E)
    return dict(E=E, info=info, t_gera=t_gera, dt=dt, nev=nev, bytes_ev=bytes_ev, tipos=tipos_ev, tam0=tam0, tam1=tam1, p0=p0, p1=p1, S=S, povs=povs, E0=E0, Emin=Emin, ermos=ermos,
                fregues=fregues, refaz=refaz, eu0=eu0, bytes_liq=bytes_liq, razoes=list(R.MEDE['razoes']), carreto=R.MEDE['carreto'], perigo0=perigo0, valida=P, txt_sem=txt_sem)


def _n(x, c=2): return f'{x:.{c}f}'.replace('.', ',')


for sem in SEMS:
    X = um_ano(sem); E = X['E']; Ls = E['lugares']
    print(f"\n===== SEMENTE {sem} (gravador {GRAV}; o personagem {EU}) =====")
    print(f"O PERSONAGEM: {E['gente']['eu']['moedas']} de prata no fim (começou com {X['eu0']})")
    print(f"a região: {X['info']} · nasceu em {_n(X['t_gera'])} s")
    print(f"TEMPO: {DIAS} dias em {_n(X['dt'], 1)} s: {_n(1000 * X['dt'] / DIAS, 1)} ms por dia (um ano: {_n(364 * X['dt'] / DIAS, 1)} s) · {X['nev']} eventos ({_n(X['nev'] / DIAS, 1)} por dia)")
    print(f"O REGISTRO: {_n(X['bytes_ev'] / 1024, 0)} KB no ano ({_n(X['bytes_ev'] / DIAS / 1024, 1)} KB por dia); por tipo (eventos, KB): " + ', '.join(f"{k} {v[0]} {_n(v[1] / 1024, 0)}" for k, v in sorted(X['tipos'].items(), key=lambda kv: -kv[1][1])))
    print(f"  com o dia do mercado (a produção e o consumo de cada lugar num evento só, com o que mudou): {_n(X['bytes_liq'] / 1024, 0)} KB ({_n(X['bytes_liq'] / DIAS / 1024, 1)} KB por dia)")
    print(f"O ESTADO (json compacto, KB): ao nascer " + ', '.join(f"{k} {_n(v / 1024, 0)}" for k, v in X['tam0'].items()) + f" (total {_n(sum(X['tam0'].values()) / 1024, 0)}) · no fim " + ', '.join(f"{k} {_n(v / 1024, 0)}" for k, v in X['tam1'].items()) + f" (total {_n(sum(X['tam1'].values()) / 1024, 0)})")
    rz = sorted(X['razoes']); n_ = len(rz) or 1
    print(f"O ATRAVESSADOR (a razão do preço de loja entre dois vizinhos, antes do carreto do dia; {len(rz)} pares bem-rota-dia): a mediana {_n(rz[len(rz) // 2] if rz else 0)}, o 99º centésimo {_n(rz[int(0.99 * n_)] if rz else 0)}, o maior {_n(rz[-1] if rz else 0)} · passa de 1,83 (o Leigo empata) em {_n(100 * sum(1 for x in rz if x > 1.83) / n_, 3)}%; de 1,375 (o Lendário em comércio empata) em {_n(100 * sum(1 for x in rz if x > 1.375) / n_, 3)}%")
    print(f"O CARRETO DO POVO moveu {X['carreto']} de prata no ano entre os povoados (e fora)")
    print(f"A PRATA DO MUNDO (gente, caixas, bolsas, fora): {X['p0']} → {X['p1']} ({'FECHA' if X['p0'] == X['p1'] else 'NÃO FECHA'}) · fora: {Ls['fora']['estoque'].get('prata', 0)} (era {R.TAB['FORA']['caixa']})")
    print(f"o estado: {'inteiro' if not X['valida'] else 'QUEBRADO: ' + '; '.join(X['valida'][:5])}")
    print('OS POVOADOS (povo do começo → do fim · caixa+bolsa: começo → fim, menor, maior · a comida: o menor e o maior fator do ano · dias de fome):')
    for k in sorted(X['povs'], key=lambda k: -X['S'][k]['pop0']):
        s = X['S'][k]; l = Ls[k]
        print(f"  {l['nome']:22} {l.get('tipo', ''):8} povo {s['pop0']:>5} → {l['pop']:>5} · prata {s['caixa0'] + s['bolsa0']:>6} → {l['estoque'].get('prata', 0) + int(l.get('bolsa') or 0):>6} (menor {s['cmin']}, maior {s['cmax']}; caixa {l['estoque'].get('prata', 0)}, bolsa {int(l.get('bolsa') or 0)})"
              f" · comida × {_n(s['fmin'])} a × {_n(s['fmax'])} · fome {s['fome']} dias · prateleira {len(mercado.prateleira(E, k))}")
    print('A SAFRA DO ANO: ' + ', '.join(f"{Ls[k]['nome']} {_n(v)}" for k, v in sorted(R.MEDE.get('safra', {}).items())[:6]) + ' ...')
    print(f"A FREGUESIA comprou {X['fregues']} peças no ano; a forja do povo fez {X['refaz']}")
    print('OS ERMOS (a contagem do começo → o menor do ano → o fim):')
    for k in X['ermos']:
        fim = caca.bichos_de(E, k)
        print(f"  {Ls[k]['nome']:22} " + ' · '.join(f"{e} {q}→{X['Emin'][k].get(e, 0)}→{fim.get(e, 0)}" for e, q in sorted(X['E0'][k].items())) + (f" · bando {Ls[k].get('bando')}" if Ls[k].get('bando') is not None else ''))
    print('AS ROTAS (blocos, tipo, ermo; o encontro por bloco: bicho, bando; no começo → no fim):')
    for rid, rt in sorted(E['rotas'].items()):
        a0, b0 = X['perigo0'][rid]; a1, b1 = R.perigo_rota(E, rt)
        print(f"  {rid} {Ls[rt['a']]['nome']} — {Ls[rt['b']]['nome']}: {rt['blocos']} blocos, {rt['tipo']}, {Ls[rt['ermo']]['nome'] if rt.get('ermo') else 'campo aberto'} · {_n(100 * a0)}% e {_n(100 * b0)}% → {_n(100 * a1)}% e {_n(100 * b1)}%")
    print('A SEMANA DA REGIÃO (as primeiras 25 linhas):'); print('  ' + '\n  '.join(X['txt_sem'][:25]))
