"""m7: o despojo e o tesouro do dragão vendidos na loja de Pedra Rasa (o mercado de verdade do motor; o mundo é a vila de teste de rascunho, carregado e NUNCA gravado).
Mede quanto a loja paga, quanto a prata dela aguenta e quanto sobra, para o jovem e para o adulto."""
import sys, io, contextlib, copy
sys.path.insert(0, '/tmp/claude-0/-home-user-ferir/2caa978a-1aa4-5b05-88b7-11bcda935cb0/scratchpad/masmorras/projeto_b/medidas')
from base_b import *
import estado, mercado
from itens import item

DESPOJO = {   # o corpo (a tabela proposta, o inteiro: o pior caso para a loja) e as peças do tesouro
    'jovem':  dict(carga={'couro:2': 5, 'osso:2': 4}, pecas=[('arma', 2, 'espada'), ('escudo', 2, None), ('armadura', 1, 'couro')], prata=400),
    'adulto': dict(carga={'couro:2': 8, 'osso:2': 6}, pecas=[('armadura', 3, 'malha'), ('arma', 2, 'machado'), ('arma', 2, 'lança'), ('arma', 1, 'espada'), ('armadura', 1, 'malha')], prata=1500),
}


def mede(qual):
    E = estado.carrega(); E['_novos'] = []
    d = DESPOJO[qual]; ef = [['pessoa', 'eu', 'carga.' + b, 'soma', q] for b, q in d['carga'].items()]
    for tipo, c, f in d['pecas']:
        it = item(tipo, c, f'peça {tipo} {T.CATS[c]} do tesouro', familia=f if tipo == 'arma' else None, material=f if tipo == 'armadura' else None, dono='eu')
        ef.append(['item', 'nasce', it])
    ef.append(['pessoa', 'eu', 'moedas', 'soma', d['prata']])
    estado.aplica(E, 'mestre', ef, onde='vila', quem=['eu'], texto=f'o despojo do dragão {qual} (medida de rascunho)')
    p0 = E['gente']['eu']['moedas']; caixa0 = mercado.caixa(E, 'vila'); mundo0 = mercado.prata_do_mundo(E)
    L = []
    for b, q in d['carga'].items():
        for _ in range(q):
            antes = E['gente']['eu']['moedas']
            try:
                with contextlib.redirect_stdout(io.StringIO()): mercado.vender(E, 'eu', b, 1)
                L.append(f"{b}: {E['gente']['eu']['moedas'] - antes}")
            except SystemExit as x: L.append(f'{b}: recusa ({str(x)[:70]})'); break
    for iid, it in list(E['itens']['itens'].items()):
        if it.get('dono') == 'eu' and 'do tesouro' in it['nome']:
            antes = E['gente']['eu']['moedas']
            try:
                with contextlib.redirect_stdout(io.StringIO()): mercado.vender_peca(E, 'eu', iid)
                L.append(f"{it['nome']}: {E['gente']['eu']['moedas'] - antes}")
            except SystemExit as x: L.append(f"{it['nome']}: recusa ({str(x)[:90]})")
    ganho = E['gente']['eu']['moedas'] - p0
    print(f"\nO DRAGÃO {qual.upper()}: o tesouro tem {d['prata']} de prata (que já é prata: não passa pela loja); o resto, vendido em Pedra Rasa:")
    for x in L: print('   ' + x)
    print(f"  a loja pagou {ganho} de prata no total; a caixa dela foi de {caixa0} para {mercado.caixa(E, 'vila')}; a prata do mundo antes e depois da venda: {mundo0} e {mercado.prata_do_mundo(E)}")
    print(f"  o preço do couro Raro na vila depois: {mercado.preco(E, 'vila', 'couro:2'):.0f} (a base é 72)")


for q in DESPOJO: mede(q)
