#!/usr/bin/env python3
"""gera.py — MOTOR 10, ETAPA FINAL: O MUNDO NOVO, inteiro, por eventos "gera", numa pasta nova (recusa escrever por cima de qualquer coisa).

  python3 gera.py PASTA [semente=N]

O que nasce (os números: tabelas_regiao.py; o contrato: projeto/ETAPA_FINAL.md, seção 6):
  O MAPA: 16 lugares de povo (a capital, 2 cidades, 5 vilas, 5 aldeias, 3 postos), com mercado, oficina, pousada, santuário, botica e runas pelo tamanho;
  as 24 ESTRADAS (lugares tipo "estrada": o grafo é conexo), com o perigo e o bando; os 6 ERMOS (bichos e matéria contados); as 8 MASMORRAS (com a origem
  na história), o covil da calamidade (o dragão ancião dorme sobre a peça Mítica), o dragão jovem que ataca, os covis de criatura.
  A HISTÓRIA (historia.py): de 400 a 1.000 anos; as casas, os reinos, a crônica, a origem das ruínas, a cadeia de donos de cada peça alta.
  A GENTE: uns 150 nomeados (com papel, casa, família, talento e dom, peças), e os 40 RIVAIS em 6 guildas (as 3 Lendas vivas com as Lendárias).
  O RARO CONTADO: as peças altas da história vão a quem a conta pede (as Lendas, os veteranos, as casas, o fundo das masmorras, os dragões).
  As FRENTES, as MISSÕES e as NOTÍCIAS do Dia 1 (frentes.py, missoes.py, noticias.py).
O personagem ainda não existe: depois, `MOTOR10_MUNDO=PASTA python3 turno.py abre` mostra a criação, e `cria.py` faz o personagem.
"""
import math, os, random, re, sys, unicodedata
import tabelas as T
import tabelas_mundo as M
import tabelas_regiao as R
import tabelas_povos as TP
import estado, mercado, caca, masmorra, talento, historia
import nomes as NM
from itens import item


def slug(nome, usados):
    base = re.sub(r'[^a-z0-9]+', '_', ''.join(c for c in unicodedata.normalize('NFD', nome.lower()) if unicodedata.category(c) != 'Mn')).strip('_')
    base = re.sub(r'^(a|o|as|os)_', '', base) or 'x'; k, x = 1, base
    while x in usados or x == 'eu': k += 1; x = f'{base}_{k}'
    return x


def de_nome(n): return estado.de_nome(n)
def a_nome(n):
    art, _, resto = n.partition(' ')
    return {'a': 'à ', 'o': 'ao ', 'as': 'às ', 'os': 'aos '}[art] + resto if art in ('a', 'o', 'as', 'os') and resto else 'a ' + n
def cap(x): return x[:1].upper() + x[1:]


class Gerador:
    def __init__(self, semente):
        self.s = semente; self.r = random.Random(f'gera|{semente}'); self.N = NM.Nomes(self.r)
        self.E = estado.novo(semente); self.L = []; self.mapa = None; self.H = None; self.casa_de = {}

    def ap(self, ef, texto, onde=None, quem=()):
        if ef: estado.aplica(self.E, 'gera', ef, onde=onde, quem=list(quem), texto=texto)

    # ---------- 1. o mapa: os lugares de povo, onde ficam ----------
    def lugares(self):
        r = self.r; pts = []
        for tipo, (n, pop, ofi, cama, bot, run, san, res, gua, dist) in R.LUGARES.items():
            for _ in range(n):
                for _t in range(400):
                    d = r.uniform(*dist) if dist[1] else 0.0; a = r.uniform(0, 2 * math.pi); x, y = round(d * math.cos(a), 2), round(d * math.sin(a), 2)
                    if all(math.hypot(x - p['x'], y - p['y']) >= 2.2 for p in pts): break
                pts.append(dict(tipo=tipo, x=x, y=y, pop=r.randint(*pop), oficina=ofi, cama=cama, botica=bot, runas=run, santuario=san, resiste=res, guarda=gua))
        usados = set()
        for p in pts:
            p['nome'] = self.N.lugar(p['tipo']); p['id'] = slug(p['nome'], usados); usados.add(p['id'])
        self.pts = pts; regiao = self.N.casa(True); self.regiao = regiao
        ef = []
        for p in pts:
            ef.append(['lugar', 'nasce', p['id'], dict(nome=p['nome'], em=NM.em(p['nome']), tipo=p['tipo'], cama=p['cama'], estoque={}, x=p['x'], y=p['y'], resiste=p['resiste'], guarda=p['guarda'])])
        self.ap(ef, f"nasce a região de {regiao}: {len(pts)} lugares de povo")
        self.L.append(f"A região de {regiao}: {len(pts)} lugares de povo (" + ', '.join(f"{sum(1 for p in pts if p['tipo'] == t)} {t}" for t in R.LUGARES) + ').')

    # ---------- 2. as estradas: a árvore mais curta e as mais curtas que faltam ----------
    def estradas(self):
        P = self.pts; n = len(P); pares = sorted((math.hypot(P[i]['x'] - P[j]['x'], P[i]['y'] - P[j]['y']), i, j) for i in range(n) for j in range(i + 1, n))
        pai = list(range(n))
        def raiz(i):
            while pai[i] != i: pai[i] = pai[pai[i]]; i = pai[i]
            return i
        arestas = []
        for d, i, j in pares:
            if raiz(i) != raiz(j): pai[raiz(i)] = raiz(j); arestas.append((d, i, j))
        grau = [0] * n
        for _, i, j in arestas: grau[i] += 1; grau[j] += 1
        for d, i, j in pares:
            if len(arestas) >= R.ESTRADAS: break
            if (d, i, j) in arestas or grau[i] >= 4 or grau[j] >= 4: continue
            arestas.append((d, i, j)); grau[i] += 1; grau[j] += 1
        self.arestas = arestas
        return arestas

    def poe_estradas(self):
        ef = []; usados = set(self.E['lugares']); self.ids_estrada = []
        for d, i, j in self.arestas:
            a, b = self.pts[i], self.pts[j]; longe = max(M.ESTRADA_LONGE[0], min(M.ESTRADA_LONGE[1], round(d / R.LEGUA_BLOCOS)))
            meio = ((a['x'] + b['x']) / 2, (a['y'] + b['y']) / 2); centro = math.hypot(*meio)
            perigo = 1 if centro < 4 else 2 if centro < 8 else 3
            passa = min(self.ermos_pts, key=lambda e: math.hypot(e['x'] - meio[0], e['y'] - meio[1])) if getattr(self, 'ermos_pts', None) else None
            passa = passa['id'] if passa and math.hypot(passa['x'] - meio[0], passa['y'] - meio[1]) < 3.0 else None
            bando = self.r.randint(*R.BANDO_INICIO) + (1 if passa else 0) + (1 if longe >= 4 else 0)
            nome = f"a estrada {de_nome(a['nome'])} {a_nome(b['nome'])}"; eid = slug('estrada ' + a['id'] + ' ' + b['id'], usados); usados.add(eid)
            ef.append(['lugar', 'nasce', eid, dict(nome=nome, em='na ' + nome[2:], tipo='estrada', ponta=[a['id'], b['id']], longe=longe, perigo=perigo, bando=bando, passa=passa, estoque={})])
            self.ids_estrada.append(eid)
        self.ap(ef, f"as {len(ef)} estradas da região")
        ls = [e[3]['longe'] for e in ef]; self.L.append(f"{len(ef)} estradas: de {min(ls)} a {max(ls)} blocos; {sum(e[3]['bando'] for e in ef)} salteadores nelas.")

    # ---------- 3. os ermos ----------
    def ermos(self):
        r = self.r; self.ermos_pts = []
        for k, (hab, per) in enumerate(R.ERMOS):
            base = r.choice([p for p in self.pts if p['tipo'] != 'capital'])
            x, y = round(base['x'] + r.uniform(-2, 2), 2), round(base['y'] + r.uniform(-2, 2), 2)
            nome = self.N.ermo(hab); eid = slug(nome, set(self.E['lugares']))
            self.ap([['lugar', 'nasce', eid, dict(nome=nome, em=NM.em(nome), tipo='ermo', estoque={}, x=x, y=y)]], f"nasce {nome}")
            viz = sorted(self.pts, key=lambda p: math.hypot(p['x'] - x, p['y'] - y))[:r.randint(*R.ERMO_VIZINHOS)]
            caca.povoa(self.E, eid, hab, per, vizinho=viz[0]['id'], longe_=r.randint(*R.ERMO_LONGE), como='o gerador da região')
            ef = []
            for v in viz[1:]:
                for a, b in ((eid, v['id']), (v['id'], eid)):
                    lv = list(self.E['lugares'][a].get('vizinhos') or [])
                    if b not in lv: ef.append(['lugar', a, 'vizinhos', 'poe', lv + [b]])
            self.ap(ef, f"{nome} dá para {len(viz)} lugares")
            self.ermos_pts.append(dict(id=eid, nome=nome, habitat=hab, perigo=per, x=x, y=y, viz=[v['id'] for v in viz]))
        self.L.append('Os ermos: ' + '; '.join(f"{e['nome']} ({e['habitat']}, {caca.K.PERIGOS[e['perigo'] - 1]})" for e in self.ermos_pts) + '.')

    # ---------- 4. a história ----------
    def historia(self):
        mapa = dict(regiao=self.regiao, lugares=[dict(tag=p['id'], nome=p['nome'], tipo=p['tipo']) for p in self.pts],
                    ermos=[dict(tag=e['id'], nome=e['nome'], habitat=e['habitat']) for e in self.ermos_pts], masmorras=self.masm_plano)
        H = historia.gera(self.s, mapa); self.H = H
        for c in H['casas'].values():
            if c['viva']: self.N.usados.add(NM._sem_acento(c['ramo'][-1]['nome']))
        for v in H['vivas']: self.N.usados.add(NM._sem_acento(v['nome']))
        ef = [['mundo', 'meta', 'nome', 'poe', self.regiao], ['mundo', 'meta', 'ano0', 'poe', H['ano0']], ['mundo', 'meta', 'anos', 'poe', H['anos']],
              ['mundo', 'meta', 'semente_historia', 'poe', self.s], ['mundo', 'meta', 'reino', 'poe', 'r_hoje']]
        for k, rr in enumerate(H['reinos']):
            ef.append(['mundo', 'reinos', 'r_hoje' if rr['caiu'] is None else f'r_{k}', 'poe', dict(nome=rr['nome'], fundado=rr['fundado'], caiu=rr['caiu'], casa=rr['casa'])])
        for cid, c in H['casas'].items():
            ef.append(['mundo', 'casas', cid, 'poe', dict(nome=c['nome'], tipo='nobre', sede=c['sede'], fundada=c['fundada'], viva=c['viva'], caiu=c['caiu'],
                                                          ramo=[dict(nome=x['nome'], assume=x['assume'], morre=x['morre'], como=x['como']) for x in c['ramo']])])
        for x in H['cronica']: ef.append(['mundo', 'cronica', 'junta', dict(ano=x['ano'], texto=x['texto'], onde=x['onde'], tags=x['tags'])])
        self.ap(ef, f"a história de {self.regiao}: {H['anos']} anos, até o ano {H['ano0']}")
        for p in self.pts:                                  # quem manda em cada lugar: a casa sediada nele, ou a do rei
            dono = next((cid for cid, c in H['casas'].items() if c['viva'] and c['sede'] == p['id']), H['rei'])
            self.ap([['lugar', p['id'], 'casa', 'poe', dono], ['lugar', p['id'], 'reino', 'poe', 'r_hoje']], f"{p['nome']} é dos {H['casas'][dono]['nome'][3:]}")
        self.L.append(f"A história: {H['anos']} anos, do ano {H['inicio']} ao {H['ano0']}; {len(H['casas'])} casas nobres ({sum(not c['viva'] for c in H['casas'].values())} caíram), "
                      f"{estado.tantos(len(H['reinos']), 'reino')}, {estado.tantos(len(H['guerras']), 'guerra')}, {estado.tantos(len(H['lendas']), 'lenda morta', 'lendas mortas')}; {len(H['cronica'])} linhas de crônica.")

    # ---------- 5. as masmorras ----------
    def plano_masmorras(self):
        r = self.r; plano = []
        perto_hab = {'mina': ('serra', 'caverna'), 'toca': ('floresta', 'brejo', 'campo'), 'covil': ('serra',), 'ruína': ('campo', 'floresta', 'brejo', 'caverna')}
        for k, (molde, cat, niv, perto) in enumerate(R.MASMORRAS):
            if perto == 'ermo':
                cands = [e for e in self.ermos_pts if e['habitat'] in perto_hab.get(molde, ())] or self.ermos_pts
                viz = r.choice(cands)['id']
            else: viz = r.choice([p for p in self.pts if p['tipo'] in ('vila', 'cidade', 'aldeia')])['id']
            de = self.N.de(); casa = self.N.casa(True)
            nome = {'cripta': f"a Cripta dos {casa}", 'mina': f"a Mina {de}", 'ruína': f"as Ruínas {de}", 'toca': f"a Toca {de}", 'covil': f"o Covil {de}"}[molde]
            plano.append(dict(tag=f'M{k}', nome=nome, molde=molde, cat=cat, niveis=niv, viz=viz))
        self.masm_plano = plano

    def masmorras(self):
        self.masm_id = {}; altos = 0
        for m in self.masm_plano:
            ef = masmorra.gera(self.E, m['molde'], m['nome'], m['viz'], niveis=m['niveis'], cat=m['cat'], origem=self.H['ruinas'].get(m['tag'], ''))
            mid = next(x[2] for x in ef if x[:2] == ['lugar', 'nasce'] and isinstance(x[3], dict) and x[3].get('tipo') == 'masmorra')
            fora = [x for x in ef if x[:2] == ['item', 'nasce'] and isinstance(x[2], dict) and x[2].get('cat', 0) >= 3 and x[2].get('tipo') != 'chave']
            altos += len(fora); ef = [x for x in ef if x not in fora]       # O RARO É CONTADO: do Épico para cima, só as peças da história (vão depois, ao fundo)
            self.ap(ef, f"{m['nome']}: a masmorra ({m['molde']})", onde=mid)
            self.masm_id[m['tag']] = mid; m['id'] = mid
        self.L.append('As masmorras: ' + '; '.join(f"{m['nome']} ({m['molde']}, {len(self.E['lugares'][m['id']]['niveis'])} nível(is))" for m in self.masm_plano) + '.')

    def fundo(self, mid):
        """a sala do fundo de uma masmorra: a do chefe, ou a do dragão, ou a última do último nível"""
        m = self.E['lugares'][mid]; ult = m['niveis'][-1]['salas']
        return next((s for s in ult if self.E['lugares'][s].get('chefe') or self.E['lugares'][s].get('dragao')), ult[-1])

    # ---------- 6. os mercados e as casas de ofício ----------
    def mercados(self):
        for p in self.pts:
            lid = p['id']
            mercado.funda(self.E, lid, p['pop'], como='o gerador da região')
            ef = [['lugar', lid, 'oficina', 'poe', p['oficina']]]
            if p['oficina']: ef += [['lugar', lid, 'preparo.fogo', 'poe', min(p['oficina'], 2)], ['lugar', lid, 'preparo.bigorna', 'poe', min(p['oficina'], 2)]]
            for k in ('botica', 'runas', 'santuario'):
                if p[k] is not None: ef.append(['lugar', lid, k, 'poe', p[k]])
            pv = {k: v for k, v in R.POVOS_LUGAR.get(p['tipo'], {}).items()}
            if pv: ef.append(['lugar', lid, 'povos', 'poe', pv])
            self.ap(ef, f"as casas de ofício {de_nome(p['nome'])}", onde=lid)
            if p['botica'] is not None or p['santuario'] is not None: mercado.funda_magia(self.E, lid, como='o gerador da região')
            if any(lid in (self.E['lugares'][m['id']].get('vizinhos') or []) for m in self.masm_plano) or p['tipo'] in ('capital', 'cidade'): mercado.funda_masmorra(self.E, lid, como='o gerador da região')

    # ---------- 7. a gente com nome ----------
    def _idade(self, povo, crianca=False):
        v = TP.POVOS[povo]['vida']
        return self.r.randint(5, v[0] - 1) if crianca else self.r.randint(v[0], max(v[0] + 1, (v[0] + v[1]) // 2 + (v[1] - v[0]) // 4))

    def _povo_de(self, lid):
        pv = self.E['lugares'][lid].get('povos') or {}; x = self.r.random(); soma = 0
        for k, f in pv.items():
            soma += f
            if x < soma: return k
        return 'humano'

    def _registro(self, pid, nome, papel, lid, povo, nivel=None, idade=None, casa=None, extra=None):
        nv, molde, grau, ma, prata, pecas, mag = R.PAPEL[papel]
        nivel = nivel or self.r.randint(*nv); ma = dict(ma)
        import pessoas, vila_teste
        at = pessoas.padrao(nome, nivel, molde=molde)['atributos']
        for k, v in (TP.POVOS[povo].get('mods') or {}).items(): at[k] += v
        lug = self.E['lugares'][lid]; sobre = R.SOBRE.get(papel, papel).format(lugar=lug['nome'], casa=(self.E['mundo']['casas'][casa]['nome'][3:] if casa else ''))
        reg = dict(nome=nome, nivel=nivel, atributos=at, lugar=lid, grau_oficio=grau, maestria=ma, treino=vila_teste.treino_da_mao(ma), moedas=self.r.randint(*prata),
                   sobre=sobre, papel=papel, casa=casa)
        if povo != 'humano': reg['povo'] = povo
        reg['idade'] = idade if idade is not None else self._idade(povo, papel == 'criança')
        if mag: reg.update(tradicao=mag['tradicao'], feiticos=list(mag['feiticos']))
        reg.update(extra or {})
        return talento.nasce(self.E, pid, reg), pecas

    def _pecas(self, pid, nome, povo, pecas, cats=None):
        ef = []; s0 = self.E['itens']['seq']; usos = []; miudo = TP.POVOS[povo]['corpo'] == 'miúdo'
        for k, (tipo, qual, cr, cobre, uso) in enumerate(pecas):
            c = self.r.randint(*cr) if cats is None else cats[k]
            de = nome
            if tipo == 'arma': it = item('arma', c, f"{cap(qual)} de {de}", familia=qual, dono=pid)
            elif tipo == 'armadura': it = item('armadura', c, f"{'Elmo' if cobre == ['cabeça'] else 'Armadura'} de {qual} de {de}", material=qual, cobre=cobre, dono=pid, **({'talhe': 'miúdo'} if miudo else {}))
            elif tipo == 'escudo': it = item('escudo', c, f"Escudo de {de}", dono=pid)
            elif tipo == 'foco': it = item('foco', c, f"{cap(qual)} de {de}", forma=qual, dono=pid)
            elif tipo == 'amuleto': it = item('amuleto', c, f"Amuleto de {de}", dono=pid)
            elif tipo == 'gazua': it = item('gazua', c, dono=pid)
            else: continue
            ef.append(['item', 'nasce', it]); usos.append(uso)
        for k, uso in enumerate(usos):
            if uso: ef.append(['item', f"i{s0 + k + 1:04d}", 'uso', 'poe', uso])
        return ef

    def _nasce(self, pid, reg, pecas, lacos=None, mais_ef=(), cats=None):
        if lacos: reg['lacos'] = {k: v for k, v in lacos.items()}
        ef = [['pessoa', 'nasce', pid, reg]] + list(mais_ef) + self._pecas(pid, reg['nome'], reg.get('povo', 'humano'), pecas, cats)
        self.ap(ef, f"{reg['nome']}, {reg['sobre']}", onde=reg['lugar'], quem=[pid])

    def _pid(self, nome):
        return slug(nome.split()[0], set(self.E['gente']))

    def gente(self):
        H = self.H; ef_casas = []
        nobres = {cid: c for cid, c in H['casas'].items() if c['viva']}
        for p in self.pts:
            lid = p['id']; papeis = [x for x in R.GENTE[p['tipo']]]
            sede = next((cid for cid, c in nobres.items() if c['sede'] == lid), None)
            if sede and not any(pp == 'senhor' for pp, _ in papeis): papeis = [('senhor', 1)] + papeis
            hab = next((e['habitat'] for e in self.ermos_pts if lid in e['viz']), 'campo')
            for papel, q in papeis:
                for _ in range(q):
                    pp = R.ALDEIA_OFICIO.get(hab, 'lavrador') if papel == 'lavrador' else papel
                    if pp == 'senhor' and sede:               # o senhor: o chefe de hoje da casa nobre (o nome e a idade vêm da história); o herdeiro nasce junto
                        x = H['casas'][sede]['ramo'][-1]; nome = x['nome']; pid = self._pid(nome); idade = H['ano0'] - x['nasce']
                        reg, pecas = self._registro(pid, nome, 'senhor', lid, 'humano', idade=min(idade, 85), casa=sede); self._nasce(pid, reg, pecas)
                        self.casa_de[pid] = sede
                        hn = self.N.gente('humano'); hid = self._pid(hn); filho = self.r.random() < 0.7
                        regh, ph = self._registro(hid, hn, 'nobre', lid, 'humano', idade=max(16, min(idade - 18, 40)) if filho else self._idade('humano'), casa=sede,
                                                  extra=dict(pais=[pid]) if filho else None)
                        self._nasce(hid, regh, ph, lacos={pid: 'pai' if filho else 'irmão'}, mais_ef=[['pessoa', pid, f'lacos.{hid}', 'poe', 'filho' if filho else 'irmão']])
                        continue
                    if pp == 'senhor':                        # lugar sem casa sediada: quem manda é um capitão do rei
                        pp = 'capitão'
                    povo = self._povo_de(lid); nome = self.N.gente(povo); pid = self._pid(nome)
                    usados_aqui = {c['nome'] for c in (self.E['mundo'].get('casas') or {}).values() if c.get('sede') == lid}
                    fam = next((x for x in (self.r.choice(NM.CASA_COMUM) for _ in range(30)) if f'os {x}' not in usados_aqui), self.r.choice(NM.CASA_COMUM))      # o sobrenome se repete pela região, não no mesmo lugar
                    cid = slug('c ' + fam + ' ' + lid, set(self.E['mundo'].get('casas') or {}))
                    self.ap([['mundo', 'casas', cid, 'poe', dict(nome=f'os {fam}', tipo='comum', sede=lid, fundada=H['ano0'] - self.r.randint(20, 200), viva=True)]], f"a família dos {fam} {de_nome(p['nome'])}")
                    extra = dict(maestria={'forja': 6, 'martelo': 2}, grau_oficio='mestre', sobre='o mestre ferreiro da capital; faz a peça de núcleo para quem traz') if pp == 'ferreiro' and p['tipo'] == 'capital' and not any(
                        g.get('papel') == 'ferreiro' and g['lugar'] == lid for g in self.E['gente'].values()) else None
                    reg, pecas = self._registro(pid, nome, pp, lid, povo, casa=cid, extra=extra)
                    if extra: import vila_teste; reg['treino'] = vila_teste.treino_da_mao(reg['maestria'])
                    self._nasce(pid, reg, pecas)
                    self._familia(pid, reg, lid, cid, povo)
        n = sum(1 for g in self.E['gente'].values() if not g.get('rival'))
        self.L.append(f"A gente com nome: {n} pessoas, em {len(self.E['mundo']['casas'])} casas e famílias.")

    def _familia(self, pid, reg, lid, cid, povo):
        r = self.r; F = R.FAMILIA
        if reg['papel'] in ('criança', 'aprendiz'): return
        if r.random() < F['conjuge']:
            nm = self.N.gente(povo); c = self._pid(nm); pp = r.choice(['lavrador', 'curandeiro', 'taverneiro', 'aprendiz']) if reg['papel'] != 'lavrador' else 'lavrador'
            rc, pc = self._registro(c, nm, pp, lid, povo, casa=cid); self._nasce(c, rc, pc, lacos={pid: 'cônjuge'}, mais_ef=[['pessoa', pid, f'lacos.{c}', 'poe', 'cônjuge']])
        if r.random() < F['filho']:
            nm = self.N.gente(povo); c = self._pid(nm); adulto = r.random() < 0.5
            rc, pc = self._registro(c, nm, 'aprendiz' if adulto else 'criança', lid, povo, casa=cid, extra=dict(pais=[pid]))
            rc['idade'] = max(rc['idade'], TP.POVOS[povo]['vida'][0]) if adulto else rc['idade']
            self._nasce(c, rc, pc, lacos={pid: 'pai'}, mais_ef=[['pessoa', pid, f'lacos.{c}', 'poe', 'filho']])
        if r.random() < F['irmao']:
            nm = self.N.gente(povo); c = self._pid(nm); pp = r.choice(['lavrador', 'guarda', 'caçador', 'aprendiz'])
            rc, pc = self._registro(c, nm, pp, lid, povo, casa=cid); self._nasce(c, rc, pc, lacos={pid: 'irmão'}, mais_ef=[['pessoa', pid, f'lacos.{c}', 'poe', 'irmão']])

    # ---------- 8. os rivais e as guildas ----------
    def rivais(self):
        r = self.r; H = self.H; sedes = [p['id'] for p in self.pts if p['tipo'] == 'capital'] * 3 + [p['id'] for p in self.pts if p['tipo'] == 'cidade'] * 2
        gs = []; pre = r.sample(R.GUILDA_NOMES[0], R.GUILDAS); suf = r.sample(R.GUILDA_NOMES[1], R.GUILDAS)      # nenhuma parte do nome se repete entre as guildas
        for k in range(R.GUILDAS):
            nm = f"{pre[k]} {suf[k]}"
            gid = slug('g ' + nm, set(self.E['mundo'].get('guildas') or {})); sede = sedes[k % len(sedes)]
            self.ap([['mundo', 'guildas', gid, 'poe', dict(nome=nm, sede=sede, lider=None, fama=0)]], f"{nm}, a guilda de {self.E['lugares'][sede]['nome']}"); gs.append(gid)
        faixas = []
        for q, nv, ca, cr, diz in R.RIVAIS: faixas += [(nv, ca, cr, diz)] * q
        lend = [it for it in H['itens'] if it['hoje'].startswith('lenda:')]; self.rival_ids = []; lendas_ids = []
        vagas = {g: r.randint(*R.GUILDA_TAMANHO) for g in gs}; ordem = list(range(len(faixas))); r.shuffle(ordem)
        for idx, (nv, ca, cr, diz) in enumerate(faixas):
            lenda = diz == 'Lenda'; li = len(lendas_ids) if lenda else None
            if lenda:
                v = H['vivas'][li]; nome, povo, idade = v['nome'], v['povo'], v['idade']
                minha = next((it for it in lend if it['hoje'] == f'lenda:{li}' and it['cat'] == 5), None)
                arq = self._arquetipo_da(minha)
            else:
                povo = r.choices(['humano', 'anão', 'elfo', 'meio-orc', 'pequenino', 'gnomo'], [62, 12, 10, 8, 5, 3])[0]; nome = self.N.gente(povo); idade = None; arq = r.choice(R.ARQUETIPOS)
            molde, mae, fam, escudo, mat, mag = arq
            nivel = r.randint(*nv); pid = self._pid(nome)
            livres = [g for g in gs if vagas[g] > 0]; guilda = r.choice(livres) if livres and r.random() < 0.78 else None
            if guilda: vagas[guilda] -= 1
            lugar = self.E['mundo']['guildas'][guilda]['sede'] if guilda else r.choice([p['id'] for p in self.pts if p['tipo'] in ('capital', 'cidade', 'vila', 'posto')])
            import pessoas, vila_teste
            at = pessoas.padrao(nome, nivel, molde=molde)['atributos']
            for k2, v2 in (TP.POVOS[povo].get('mods') or {}).items(): at[k2] += v2
            mt = T.maestria_tipica(nivel); ma = {mae: max(2, mt)} if mae else {}
            if mag and mae != mag.get('tradicao'): ma[mag['tradicao']] = max(2, mt)
            if mae == 'adaga': ma['manha'] = max(2, mt)
            fama = {'novato': r.randint(0, 6), 'oficial': r.randint(10, 45), 'veterano': r.randint(60, 160), 'Lenda': r.randint(290, 300)}[diz]
            reg = dict(nome=nome, nivel=nivel, atributos=at, lugar=lugar, grau_oficio='oficial', maestria=ma, treino=vila_teste.treino_da_mao(ma), moedas=r.randint(10, 40) * (1 + nivel // 10),
                       sobre=f"aventureiro{'' if diz == 'novato' else ' ' + ('veterano' if diz == 'veterano' else 'de ofício' if diz == 'oficial' else 'de lenda')}" + (f", {self.E['mundo']['guildas'][guilda]['nome']}" if guilda else ', anda sozinho'),
                       papel='aventureiro', rival=True, fama=fama, guilda=guilda)
            if povo != 'humano': reg['povo'] = povo
            reg['idade'] = idade if idade is not None else self._idade(povo)
            if mag: reg.update(tradicao=mag['tradicao'], feiticos=list(mag['feiticos']))
            reg = talento.nasce(self.E, pid, reg)
            pecas = []; cats = []
            if fam: pecas.append(('arma', fam, ca, None, 'arma')); cats.append(r.randint(*ca))
            if mag: pecas.append(('foco', 'cajado' if mag['tradicao'] == 'arcano' else 'símbolo', ca, None, 'foco')); cats.append(r.randint(*ca))
            pecas.append(('armadura', mat, cr, None, 'veste')); cats.append(r.randint(*cr))
            if escudo: pecas.append(('escudo', None, cr, None, 'escudo')); cats.append(max(0, r.randint(*cr) - 1))
            if mae == 'adaga': pecas.append(('gazua', None, (0, 1), None, None)); cats.append(min(2, max(0, r.randint(*ca))))
            if lenda and minha:                                 # a Lenda leva a Lendária no lugar da peça do mesmo tipo
                tp = {'arma': 'arma', 'armadura': 'armadura', 'escudo': 'escudo', 'foco': 'foco', 'amuleto': 'amuleto'}[minha['tipo']]
                fora = next((k3 for k3, x in enumerate(pecas) if x[0] == tp), None)
                if fora is not None: pecas.pop(fora); cats.pop(fora)
            self._nasce(pid, reg, pecas, cats=cats)
            self.rival_ids.append(pid)
            if lenda: lendas_ids.append(pid)
        for g in gs:                                            # o líder da guilda é o de maior nível dela; a fama da guilda, a soma
            mem = [k for k in self.rival_ids if self.E['gente'][k].get('guilda') == g]
            if mem:
                lid_ = max(mem, key=lambda k: self.E['gente'][k]['nivel'])
                self.ap([['mundo', 'guildas', g, 'lider', 'poe', lid_], ['mundo', 'guildas', g, 'fama', 'poe', sum(self.E['gente'][k].get('fama', 0) for k in mem)]], 'o líder da guilda')
        self.lendas_ids = lendas_ids
        self.L.append(f"Os rivais: {len(self.rival_ids)} aventureiros, {len(gs)} guildas (" + ', '.join(self.E['mundo']['guildas'][g]['nome'] for g in gs) + f"); as Lendas vivas: " + ', '.join(self.E['gente'][k]['nome'] for k in lendas_ids) + '.')

    def _arquetipo_da(self, it):
        if not it: return R.ARQUETIPOS[0]
        if it['tipo'] == 'arma': return ('arqueiro' if it['qual'] == 'arco' else 'guerreiro', it['qual'], it['qual'], it['qual'] not in ('arco', 'montante', 'malho', 'alabarda'), 'malha', None)
        if it['tipo'] == 'foco': return R.ARQUETIPOS[6]
        if it['tipo'] == 'amuleto': return R.ARQUETIPOS[7]
        return R.ARQUETIPOS[0]

    # ---------- 9. os dragões, os covis, e as peças altas da história ----------
    def feras(self):
        import dragoes, criaturas
        r = self.r; serra = next((e for e in self.ermos_pts if e['habitat'] == 'serra'), self.ermos_pts[0])
        alvo = min((p for p in self.pts if p['tipo'] in ('vila', 'aldeia', 'posto')), key=lambda p: math.hypot(p['x'] - serra['x'], p['y'] - serra['y']))
        nome_j = r.choice(['o Brasa', 'o Ferrugem', 'a Fornalha', 'o Carvão Vivo', 'o Rubro', 'o Fumo Velho', 'a Cinzenta'])
        self.ap(dragoes.poe(self.E, serra['id'], R.DRAGAO_JOVEM['tipo'], R.DRAGAO_JOVEM['idade'], nome_j, vila=alvo['id'], tesouro=r.randint(*R.DRAGAO_JOVEM['tesouro'])), f"{nome_j}, o dragão jovem da serra", onde=serra['id'])
        self.dragao_jovem = (serra['id'], nome_j, alvo['id'])
        cov = next(m for m in self.masm_plano if m['molde'] == 'covil'); sala = self.fundo(cov['id']); d = dict(self.E['lugares'][sala].get('dragao') or {})
        if d:
            d['dorme_ate'] = r.randint(*R.CALAMIDADE['dorme']); d['nome'] = r.choice(['a Montanha que Dorme', 'o Sono da Serra', 'a Fome da Serra', 'o Pai das Cinzas'])
            self.ap([['lugar', sala, 'dragao', 'poe', d]], 'o dragão ancião dorme no covil')
        self.calamidade = (cov['id'], sala, d.get('nome'))
        for esp, hab, cab in R.COVIS:
            e = next((x for x in self.ermos_pts if x['habitat'] == hab), None)
            if e and not self.E['lugares'][e['id']].get('covil'): criaturas.poe_covil(self.E, e['id'], esp, cabecas_=cab, tesouro=r.randint(15, 40), tipo='gera', como='um covil do Dia 1')
        self.L.append(f"Os dragões: {nome_j} (jovem) {NM.em(serra['nome'])}, cobra de {alvo['nome']}; {d.get('nome', '?')} (ancião) dorme {NM.em(cov['nome'])}.")

    def pecas_altas(self):
        H = self.H; r = self.r; vets = [k for k in self.rival_ids if 50 <= self.E['gente'][k]['nivel'] <= 100]; vi = 0; postos = []
        for it in H['itens']:
            hoje = it['hoje']; dono = onde = None
            if hoje.startswith('lenda:'): dono = self.lendas_ids[int(hoje.split(':')[1]) % len(self.lendas_ids)]
            elif hoje == 'veterano' and vets: dono = vets[vi % len(vets)]; vi += 1
            elif hoje.startswith('casa:'):
                cid = hoje.split(':', 1)[1]; dono = next((k for k, g in self.E['gente'].items() if g.get('casa') == cid and g.get('papel') == 'senhor'), None)
            elif hoje.startswith('masmorra:'):
                tag = hoje.split(':', 1)[1]; mid = self.masm_id.get(tag) or self.masm_id[r.choice(list(self.masm_id))]; onde = self.fundo(mid)
            elif hoje == 'dragao': onde = self.dragao_jovem[0]
            elif hoje == 'calamidade': onde = self.calamidade[1]
            if dono is None and onde is None: onde = self.fundo(self.masm_id[r.choice(list(self.masm_id))])
            hist = [f"Ano {d['ano']}: " + (f"{d['quem']} " if d['quem'] else '') + d['como'] for d in it['donos']]
            ult_ano = it['donos'][-1]['ano']; depois = lambda a: max(ult_ano, min(H['ano0'], a))       # a última linha nunca vem antes da que já está escrita
            if dono:
                g = self.E['gente'][dono]; ult = it['donos'][-1]
                hist.append(f"Ano {depois(H['ano0'] - r.randint(1, 15))}: {g['nome']} " + ('a achou' if ult['quem'] is None else r.choice(['a herdou', 'a comprou', 'a tomou de quem a tinha', 'a ganhou'])) + ', e a tem hoje')
            elif hoje == 'dragao': hist.append(f"Ano {depois(H['ano0'] - r.randint(1, 30))}: foi parar no tesouro {de_nome(self.dragao_jovem[1])}")
            elif hoje == 'calamidade': hist.append(f"Ano {depois(H['ano0'] - r.randint(100, 300))}: jaz sob {self.calamidade[2] or 'o dragão'}, que dorme sobre o tesouro")
            elif it['donos'][-1]['quem'] is not None: hist.append(f"Ano {depois(H['ano0'] - r.randint(5, 40))}: perdeu-se {NM.em(self.E['lugares'][self.E['lugares'][onde].get('masmorra', onde)]['nome'])}, com quem a levava")
            kw = dict(familia=it['qual']) if it['tipo'] == 'arma' else dict(material=it['qual']) if it['tipo'] == 'armadura' else dict(forma=it['qual']) if it['tipo'] == 'foco' else {}
            reg = item(it['tipo'], it['cat'], it['nome'][0].upper() + it['nome'][1:], dono=dono, onde=None if dono else onde, historia=hist, **kw)
            if dono and reg['tipo'] == 'armadura' and TP.POVOS[estado.povo(self.E['gente'][dono])]['corpo'] == 'miúdo': reg['talhe'] = 'miúdo'
            s0 = self.E['itens']['seq']; ef = [['item', 'nasce', reg]]
            if dono:                                            # quem tem a peça alta a usa (no lugar da que vestia ali)
                uso = {'arma': 'arma', 'armadura': 'veste', 'escudo': 'escudo', 'foco': 'foco', 'amuleto': 'pescoco'}[it['tipo']]
                for iid, x in self.E['itens']['itens'].items():
                    if x.get('dono') == dono and x.get('uso') == uso and (uso != 'veste' or 'tronco' in (x.get('cobre') or ['tronco'])): ef.append(['item', iid, 'uso', 'poe', None])
                ef.append(['item', f"i{s0 + 1:04d}", 'uso', 'poe', uso])
            self.ap(ef, f"{reg['nome']} ({T.CATS[it['cat']]}): a peça da história", onde=onde or self.E['gente'][dono]['lugar'], quem=[dono] if dono else ())
            postos.append((reg['nome'], it['cat'], self.E['gente'][dono]['nome'] if dono else self.E['lugares'][onde]['nome']))
        self.L.append(f"As peças altas da história: {len(postos)} (" + ', '.join(f"{T.CATS[c]} {sum(1 for _, x, _ in postos if x == c)}" for c in sorted({c for _, c, _ in postos})) + ').')

    # ---------- 10. as frentes, as missões e as notícias do Dia 1 (dos módulos que existirem) ----------
    def habilidades(self):
        """(a parte 2, fase 2) a gente nasce com as habilidades que a mão e a vida explicam, pela função da semente (habilidade.da_vida; o acaso do gerador não anda)"""
        import habilidade
        ef = []
        for pid in sorted(self.E['gente']): ef += habilidade.efeitos_da_vida(self.E, pid)
        if ef: self.ap(ef, f"a gente nasce com as habilidades que a mão e a vida explicam ({len(ef)})")
        n = len({x[1] for x in ef}); self.L.append(f"As habilidades: {n} pessoas nascem com {len(ef)} habilidades (a mão e a vida, pela semente).")

    def comeco(self):
        import importlib
        for nome in ('frentes', 'missoes', 'noticias', 'rivais', 'gente'):
            try: mod = importlib.import_module(nome)
            except ModuleNotFoundError as x:
                if x.name != nome: raise
                continue
            f = getattr(mod, 'gera', None)
            if callable(f):
                linhas = f(self.E, self.r) or []
                self.L += list(linhas)

    def tudo(self):
        self.lugares(); self.ermos(); self.estradas(); self.poe_estradas(); self.plano_masmorras(); self.historia(); self.masmorras(); self.mercados()
        self.gente(); self.rivais(); self.habilidades(); self.feras(); self.pecas_altas(); self.comeco()
        P = estado.valida(self.E)
        if P: sys.exit('O MUNDO NASCEU QUEBRADO (não foi gravado):\n  ' + '\n  '.join(P[:30]))
        conta = {}
        for it in self.E['itens']['itens'].values(): conta[it['cat']] = conta.get(it['cat'], 0) + 1
        self.L.append('O raro contado no Dia 1: ' + ', '.join(f"{T.CATS[c]} {conta[c]}" for c in sorted(conta) if c >= 2) + '.')
        prata = mercado.prata_do_mundo(self.E)
        self.L.append(f"A prata do mundo: {prata:,}".replace(',', '.') + f"; {len(self.E['gente'])} pessoas com ficha; {len(self.E['lugares'])} lugares (com estradas, ermos e salas); {self.E['relogio']['eventos']} eventos do gerador.")
        return self.E


def mundo(semente=1):
    """o mundo novo inteiro, em memória (quem chama grava). Devolve (E, linhas do resumo)"""
    G = Gerador(semente); E = G.tudo(); return E, G.L


def main(a=None):
    a = sys.argv[1:] if a is None else list(a)
    op = dict(x.split('=', 1) for x in a if '=' in x); pos = [x for x in a if '=' not in x]
    if len(pos) != 1 or any(k != 'semente' for k in op): print(__doc__); return
    pasta = os.path.abspath(pos[0])
    if os.path.exists(pasta) and (not os.path.isdir(pasta) or os.listdir(pasta)): sys.exit(f'{pasta} já existe e não está vazia: não escrevo por cima. Escolha uma pasta nova.')
    if not op.get('semente', '1').isdigit(): sys.exit(f'semente= pede um número (veio "{op["semente"]}")')
    E, L = mundo(int(op.get('semente', 1)))
    os.makedirs(pasta, exist_ok=True); os.environ['MOTOR10_MUNDO'] = pasta; estado.grava(E)
    try:
        import turno; turno.abre(E)
    except SystemExit: pass
    open(os.path.join(pasta, 'LEIA.md'), 'w', encoding='utf-8').write(f"# O MUNDO NOVO: {E['mundo']['meta']['nome']}\n\nGerado pelo `gera.py` do Motor 10 (semente {E['relogio']['semente']}).\n\n" + '\n'.join('- ' + x for x in L) + '\n')
    print(f'O MUNDO NOVO nasceu em {pasta}.\n'); print('\n'.join(L))


if __name__ == '__main__':
    import signal; hasattr(signal, 'SIGPIPE') and signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    main()
