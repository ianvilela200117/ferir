# m8_cena.py: os números da cena jogada (o que cada loja paga pelo escudo Incomum, o perigo das rotas de Pedra Rasa e da capital) e quanto o registro comprime
# roda de dentro de motor10/: PYTHONDONTWRITEBYTECODE=1 python3 projeto/etapa3/projeto_a/medidas/m8_cena.py COPIA_DO_ENSAIO
import os, sys, json, gzip
sys.path.insert(0, os.getcwd()); sys.path.insert(0, 'projeto/etapa3/projeto_a/medidas')
os.environ['MOTOR10_MUNDO'] = sys.argv[1]
import estado, ato, mercado, itens, proto_regiao as R
R.instala(); R.moeda_na_loja()
E = R.monta(1)
evs = []
for d in range(60):
    for _ in range(6):
        if E['gente']['eu']['corpo']['fome'] >= 3:
            try: ato.comer(E, 'eu')
            except SystemExit: pass
        ato.passa(E, 'eu', 1, 'esperar', para=False)
    evs += E['_novos']; E['_novos'] = []
raw = '\n'.join(json.dumps(e, ensure_ascii=False) for e in evs).encode()
print('60 dias de registro:', len(raw) // 1024, 'KB; comprimido (gzip):', len(gzip.compress(raw)) // 1024, 'KB')
Ls = E['lugares']; cid = [k for k, l in Ls.items() if l.get('tipo') == 'cidade']; cap = [k for k, l in Ls.items() if l.get('tipo') == 'capital'][0]
esc = itens.item('escudo', 1, dono='eu'); arm = itens.item('armadura', 1, material='couro', dono='eu')
for lid in ['vila', cap] + cid:
    print(Ls[lid]['nome'], Ls[lid]['tipo'], '· o escudo Incomum: a loja paga', mercado.paga_peca(E, 'eu', esc, lid=lid), '· a armadura de couro Incomum:', mercado.paga_peca(E, 'eu', arm, lid=lid),
          '· 10 de couro Comum pagam', mercado.paga(E, 'eu', 'couro:0', 10, lid=lid), '· o metal Incomum custa', mercado.custa(E, lid, 'metal:1', 3), 'por 3 · comida × %.2f' % mercado.fator(E, lid, 'comida'), '· moeda %.2f' % R.moeda(E, lid),
          '· prateleira', len(mercado.prateleira(E, lid)), 'alvo', mercado.alvo_pecas(E, lid))
for rid, rt in sorted(E['rotas'].items()):
    if 'vila' in (rt['a'], rt['b']) or cap in (rt['a'], rt['b']):
        a, b = R.perigo_rota(E, rt); print(rid, Ls[rt['a']]['nome'], '—', Ls[rt['b']]['nome'], rt['blocos'], rt['tipo'], Ls[rt['ermo']]['nome'] if rt.get('ermo') else '-', 'bicho %.2f%% bando %.2f%%' % (100 * a, 100 * b))
print('dia', E['relogio']['dia'], estado.estacao(E))
