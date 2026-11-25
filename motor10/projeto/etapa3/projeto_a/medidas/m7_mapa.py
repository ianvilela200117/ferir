# m7_mapa.py: os fatos do mapa em três sementes (de Pedra Rasa a cada povoado, em blocos; as bancadas; as rotas; as masmorras)
# roda de dentro de motor10/: PYTHONDONTWRITEBYTECODE=1 python3 projeto/etapa3/projeto_a/medidas/m7_mapa.py COPIA_DO_ENSAIO
import os, sys, heapq, json
sys.path.insert(0, os.getcwd()); sys.path.insert(0, 'projeto/etapa3/projeto_a/medidas')
os.environ['MOTOR10_MUNDO'] = sys.argv[1]
import estado, mercado, proto_regiao as R
R.instala()
for sem in (1, 2, 3):
    E = R.monta(sem); Ls = E['lugares']; G = {}
    for rid, rt in E['rotas'].items():
        G.setdefault(rt['a'], []).append((rt['blocos'], rt['b'], rid)); G.setdefault(rt['b'], []).append((rt['blocos'], rt['a'], rid))
    d = {'vila': 0}; h = [(0, 'vila')]
    while h:
        x, u = heapq.heappop(h)
        if x > d.get(u, 99): continue
        for w, v, _ in G.get(u, []):
            if x + w < d.get(v, 99): d[v] = x + w; heapq.heappush(h, (x + w, v))
    tipos = {k: l.get('tipo') for k, l in Ls.items()}
    of = {k: (l.get('oficina'), l.get('runas'), l.get('botica'), l.get('santuario')) for k, l in Ls.items() if mercado.tem_mercado(E, k) and k != 'fora'}
    print(f'semente {sem}: de Pedra Rasa, em blocos: ' + ', '.join(f"{Ls[k]['nome']} ({tipos[k]}{', runas ' + str(of[k][1]) if of.get(k, (None, None))[1] is not None else ''}{', oficina ' + str(of[k][0]) if of.get(k) and of[k][0] is not None else ''}) {v}" for k, v in sorted(d.items(), key=lambda kv: kv[1]) if k in of))
    graus = {k: len(G.get(k, [])) for k in of}; print('   rotas por povoado:', sorted(graus.values()), '· tipos de rota:', {t: sum(1 for r in E['rotas'].values() if r['tipo'] == t) for t in ('estrada', 'caminho', 'trilha', 'fora')})
    nucl = [(Ls[s].get('nome'), Ls[s].get('chefe')) for s in Ls if Ls[s].get('tipo') == 'sala' and Ls[s].get('chefe')]
    print('   chefes nas masmorras:', [(n, c.get('qual')) for n, c in nucl])
    cats = {k: [nv['cat'] for nv in l['niveis']] for k, l in Ls.items() if l.get('tipo') == 'masmorra'}; print('   masmorras (categorias dos níveis):', {Ls[k]['nome']: v for k, v in cats.items()})
    print('   salas:', sum(1 for l in Ls.values() if l.get('tipo') == 'sala'), '· peças no Livro:', len(E['itens']['itens']), '· prata nas masmorras:', sum(int(l['estoque'].get('prata', 0)) for l in Ls.values() if l.get('tipo') == 'sala'))
    chefes_ermo = [(Ls[k]['nome'], e) for k, l in Ls.items() if l.get('tipo') == 'ermo' for e in (l.get('bichos') or {}) if (estado.especie(e) or {}).get('chefe')]
    print('   chefes nos ermos:', chefes_ermo)
