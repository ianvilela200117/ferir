#!/usr/bin/env python3
"""painel.py — O PAINEL DO JOGADOR (MOTOR 6.4): escreve painel.html, uma página só, para abrir no navegador.
Mostra só o que Ferir sabe: nada marcado OCULTO entra. Data, tempo, Ferir, o reino com os pilares, a agenda, os fios, os relógios
conhecidos, o mercado, quem está fora de Ireviel, as distâncias. O salvar.py refaz a página a cada save.
Uso: python3 painel.py [quieto]
"""
import re, sys, html
from nucleo import carrega, P, calendario, ler

PIL = ['Comida', 'Comércio', 'Dinheiro', 'Saúde', 'Ordem', 'Defesa']
def e(x): return html.escape(str(x))
def limpa(t): return re.sub(r'\s*\(OCULTO[^)]*\)', '', t)
def br(n): return f'{int(n):,}'.replace(',', '.')

def main():
    est = carrega('estado.json').get('tempo', {}); dia = est.get('dia', 0); cal = calendario(dia)
    F = carrega('ficha.json'); R = carrega('reino.json'); A = carrega('agenda.json', {'itens': [], 'fios': []}); RL = carrega('relogios.json', {'relogios': []})
    C = carrega('clima.json', {}); M = carrega('mercado.json', {}); O = carrega('onde.json', {}); T = carrega('tratados.json', {'tratados': {}})
    H = []
    H.append(f"<header><h1>O reino de Ireviel</h1><p class='data'>Dia {dia} · {e(cal['txt'])}" + (f" · {e(cal['nota'])}" if cal['nota'] else '') + '</p></header>')
    if C.get('hoje'):
        H.append("<section><h2>O tempo</h2><div class='grade'>" + ''.join(f"<div class='cartao'><b>{e(k)}</b><br>{e(v['ceu'])}, {e(v['vento'])}</div>" for k, v in C['hoje'].items()) + f"<div class='cartao'><b>O rio</b><br>{C.get('agua', '?')}/100</div></div></section>")
    if F:
        a = F['atributos']; lim = 50 * F['nivel'] * (F['nivel'] + 1) + 100; ant = 50 * (F['nivel'] - 1) * F['nivel'] + 100; pct = max(0, min(100, 100 * (F['xp'] - ant) / (lim - ant)))
        H.append(f"<section><h2>Ferir</h2><p><b>Nível {F['nivel']}</b> · XP {br(F['xp'])} de {br(lim)}</p><div class='barra'><i style='width:{pct:.0f}%'></i></div>"
                 f"<p>PV {F['pv'][0]}/{F['pv'][1]} · Mana {F['mana'][0]}/{F['mana'][1]} · Foco {F['foco']} · Fortuna {F['fortuna'][0]}/{F['fortuna'][1]} · Revés {F['reves'][0]}/{F['reves'][1]}</p>"
                 f"<p>Inteligência {a['Inteligência']} · Afinidade {a['Afinidade']} · Percepção {a['Percepção']} · Sorte {a['Sorte']} · Agilidade {a['Agilidade']}</p>"
                 f"<p><b>Cofre {br(F['cofre'])}</b> · material: " + ' · '.join(f"{e(k)} ~{v['kg']:g} kg" for k, v in F.get('materiais', {}).items()) + '</p>'
                 + ('<p>' + ' · '.join(f"{e(k)} {v['tem']}/{v['max']}" for k, v in F.get('recursos', {}).items()) + '</p>' if F.get('recursos') else '') + '</section>')
    if R:
        r = R['reino']; H.append(f"<section><h2>O reino</h2><p>Prestígio {r['prestigio']}/10 · Legitimidade {r['legitimidade']}/10</p><div class='grade'>")
        for c in R['cidades']:
            H.append(f"<div class='cartao'><b>{e(c['nome'])}</b> <span class='fraco'>~{br(c['gente'])}</span>" + ''.join(f"<div class='pilar'><span>{k}</span><span class='pts n{c['pilares'][k]}'>{'●' * c['pilares'][k]}{'○' * (4 - c['pilares'][k])}</span></div>" for k in PIL)
                     + ''.join(f"<div class='fraco'>obra: {e(o['nome'])} (pronta no {o['pronta']})</div>" for o in c.get('obras', [])) + '</div>')
        H.append('</div><p class="fraco">Relações: ' + ' · '.join(f'{e(k)} {v:+d}' for k, v in r['relacoes'].items()) + '</p></section>')
    it = sorted([i for i in A['itens'] if not i['feito'] and not i.get('oculto') and i['tipo'] != 'noticia' and i['dia'] <= dia + 30], key=lambda i: i['dia'])
    H.append('<section><h2>O que vem</h2><ul>' + (''.join(f"<li><b>Dia {i['dia']}</b>{' (atrasado)' if i['dia'] < dia else ''} — {e(limpa(i['texto']))}</li>" for i in it) or '<li>nada marcado.</li>') + '</ul></section>')
    fios = [f for f in A.get('fios', []) if not f['fechado'] and not f.get('oculto')]
    H.append('<section><h2>Fios abertos</h2><ul>' + ''.join(f"<li>{e(limpa(f['texto']))}" + (f" <span class='fraco'>· parado há {dia - f['tocado']} dias</span>" if dia - f['tocado'] >= 7 else '') + '</li>' for f in sorted(fios, key=lambda f: f['tocado'])) + '</ul></section>')
    rl = [x for x in RL['relogios'] if not x['oculto'] and x['estado'] != 'fechado']
    if rl: H.append('<section><h2>Relógios</h2><ul>' + ''.join(f"<li><span class='pts'>{'●' * x['valor']}{'○' * (x['max'] - x['valor'])}</span> {e(x['nome'])}: {e(x['ao_encher'])}</li>" for x in rl) + '</ul></section>')
    tv = [t for t in T['tratados'].values() if t['estado'] in ('vigente', 'proposto')]
    if tv: H.append('<section><h2>Acordos</h2><ul>' + ''.join(f"<li><b>{e(t['com'])}</b> ({e(t['estado'])}): {e(limpa(t['texto']))}</li>" for t in tv) + '</ul></section>')
    if M.get('cidades'):
        H.append("<section><h2>O mercado <span class='fraco'>(100 = preço normal)</span></h2><table><tr><th></th>" + ''.join(f'<th>{e(k)}</th>' for k in next(iter(M['cidades'].values()))) + '</tr>'
                 + ''.join(f"<tr><td>{e(c)}</td>" + ''.join(f"<td class='{'caro' if x >= 130 else 'barato' if x <= 80 else ''}'>{x}</td>" for x in v.values()) + '</tr>' for c, v in M['cidades'].items()) + '</table></section>')
    if O:
        from onde import lugar_de
        H.append('<section><h2>Quem está fora de Ireviel</h2><ul>' + ''.join(f'<li><b>{e(n)}</b>: {e(lugar_de(n, O, dia))}</li>' for n in sorted(O)) + '</ul></section>')
    dist = re.findall(r'^\| ([^|]+?) \| ([^|]*\d[^|]*dias?[^|]*) \| ([^|]+?) \|$', ler('compendio/01_mundo.md'), re.M)[:18]
    if dist: H.append("<section><h2>Distâncias a partir de Ireviel</h2><table>" + ''.join(f'<tr><td>{e(a.strip(" *"))}</td><td>{e(b)}</td><td class="fraco">{e(c)}</td></tr>' for a, b, c in dist) + '</table></section>')
    css = """:root{--fundo:#f6f3ec;--carta:#fffdf8;--tinta:#2a2620;--fraco:#7a7164;--linha:#ddd5c5;--destaque:#8a3b12;--bom:#3d6b35;--ruim:#a3321f}
@media (prefers-color-scheme:dark){:root{--fundo:#1b1915;--carta:#25221d;--tinta:#ece5d8;--fraco:#9b917f;--linha:#3a352d;--destaque:#e09a5f;--bom:#8fc082;--ruim:#e58a78}}
*{box-sizing:border-box}body{margin:0;background:var(--fundo);color:var(--tinta);font:16px/1.5 Georgia,'Times New Roman',serif}
main{max-width:980px;margin:0 auto;padding:24px 18px 60px}header{border-bottom:2px solid var(--destaque);margin-bottom:18px}h1{margin:0;font-size:1.9rem;letter-spacing:.02em}
.data{margin:.2rem 0 .8rem;color:var(--fraco)}h2{font-size:1.15rem;margin:0 0 .5rem;color:var(--destaque)}section{background:var(--carta);border:1px solid var(--linha);border-radius:8px;padding:14px 16px;margin:0 0 14px}
.grade{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px}.cartao{border:1px solid var(--linha);border-radius:6px;padding:10px}.fraco{color:var(--fraco);font-size:.88rem}
.pilar{display:flex;justify-content:space-between;font-size:.93rem}.pts{letter-spacing:2px;color:var(--bom)}.pts.n0,.pts.n1{color:var(--ruim)}.pts.n2{color:var(--destaque)}
.barra{height:8px;background:var(--linha);border-radius:4px;overflow:hidden}.barra i{display:block;height:100%;background:var(--destaque)}
ul{margin:0;padding-left:1.1rem}li{margin:.25rem 0}table{border-collapse:collapse;width:100%;font-size:.93rem}td,th{padding:4px 8px;border-bottom:1px solid var(--linha);text-align:left}.caro{color:var(--ruim);font-weight:bold}.barato{color:var(--bom)}p{margin:.35rem 0}"""
    doc = f"<!DOCTYPE html><html lang='pt-BR'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>O reino de Ireviel — Dia {dia}</title><style>{css}</style></head><body><main>" + '\n'.join(H) + "<p class='fraco'>Só o que Ferir sabe. Gerado pelo motor a cada save.</p></main></body></html>"
    open(P('painel.html'), 'w', encoding='utf-8').write(doc)
    if 'quieto' not in sys.argv: print(f'painel.html escrito ({len(doc) // 1024} KB).')

if __name__ == '__main__':
    main()
