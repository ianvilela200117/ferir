#!/usr/bin/env python3
"""luta.py — MOTOR 10: A LUTA. Grupo contra grupo, numa linha de casas (1 casa ≈ 3 m), turno a turno.

O que entra na conta (as regras estão no REGRAS.md; os números, no tabelas.py):
  1 distância e alcance · 2 o lugar (estreito, alto, cobertura, sem saída) · 3 o tempo (escuro, chuva, lama, neblina, vento, calor, água)
  4 fôlego · 5 golpe contra armadura · 6 parte do corpo e ferida · 7 durabilidade · 8 moral · 9 grupo contra grupo
  10 A LUTA PARA E PERGUNTA: quando algo muda, o turno acaba e o script devolve o quadro; a ordem do jogador volta por `ordem`.
     O que a luta diz de GENTE não depende de gênero (a luta não sabe o gênero de ninguém): CAIU, MORREU, FRAQUEJA, "levou uma ferida". Do bicho, a espécie diz o gênero.
  11 OS BICHOS (bichos.py; os números, no tabelas_bichos.py): o corpo é a arma e a armadura, com categoria, e não é peça (não quebra);
     o tamanho mexe no PV, no alcance, no cerco, no corredor e na Defesa; os traços (lista fechada); a moral do bicho (foge ferido, não se rende).
  12 A MAGIA (magia.py; os números, no tabelas_magia.py; capítulo 11): lançar (a Conjuração contra a Defesa, a área ou a Firmeza; a Mana que volta 1 por turno;
     o feitiço longo e a concentração; o retrochoque; lançar no osso), os estados com prazo, o calejo, o campo, a cura, beber na luta, a peça encantada,
     os nove traços novos e as fases do chefe. Só numa luta em que alguém traz magia: a luta sem magia é a de sempre, dado por dado.
  13 A ETAPA 4b (o contrato: projeto/ETAPA_4B.md, seção 9): os traços do povo (vê no escuro: no golpe o escuro tira a metade, no tiro pesa inteiro; resiste a veneno: o veneno pela metade; a coragem
     do povo no teste de coragem), o GOLPE PELAS COSTAS de quem tem a manha de Treinado, e a fase "foge" do chefe que voa (magia.fase). Só para quem tem o traço, a manha
     ou a fase: a luta de quem não tem é a de sempre, dado por dado.
  14 A PARTE 2, FASE 1b (o contrato: projeto/etapa_efeitos/DESENHO.md, seções 3 e 4; o capítulo 28; os números, no tabelas_efeitos.py): os efeitos de item (os 21 de
     número, cujo valor sai da categoria que a peça rende, e os 26 de regra), pela PILHA (o dano é uma conta só, no fim, com o teto de 7 vezes o golpe de hoje, os dados
     no máximo 4 vezes, os fixos até +8, a couraça em curva até 75%), a CARGA (uma barra por família: cabeça, pernas, mana; a cabeça firme; o calejo; ninguém perde mais
     de 1 turno em 3), os FILETES de sangue e de fogo (até 3; a ordem `atar`), o exposto e o amolecido, o Imortal (um salvamento por dia) e A ESCADA DO MEDO (o acuado;
     as fontes novas testam juntas). A escada é a única mudança que toca toda luta de gente; fora ela, a luta sem efeito novo é a de antes, dado por dado (a meta B0).
  15 A PARTE 2, FASE 2 (DESENHO 6; o capítulo 29; habilidade.py): AS HABILIDADES na luta, só numa luta em que alguém traz habilidade (S['hab']): a ordem `fazer`, a Roda do
     Malho (as batidas, o fecho, o abrir, as figuras), a Sanha, os Trunfos (a ordem com condição), as declaradas (o Tranco dentro da regra de 1 turno em 3, o Corte Fundo, a
     Rasteira), as reações (a Riposta, o Manter à Distância, a Vigília), o Brado, o Rito de Veia, a Guarda de Bigorna (a postura `bigorna`) e as outras. A luta sem habilidade
     é a de sempre, dado por dado.

Uso em código:
  S = nova(lado_a, lado_b, inicio='perto', lugar={...}, tempo=[...])     (listas de pessoas do pessoas.py; o lado A é o do jogador)
  corre(S, interativo=True)      roda até uma PARADA ou o fim · ordem(S, 'Nome: atacar Alvo agressiva')
  resultado(S)                   quem venceu, mortos, caídos, presos, feridas, peças quebradas
Uso de linha de comando (a luta de verdade: dado de verdade, o estado guardado num arquivo entre uma ordem e outra):
  python3 luta.py nova CENARIO.json lutas/NOME.json                       monta a luta e mostra o quadro
  python3 luta.py roda lutas/NOME.json ["Nome: ordem"] ["grupo: ordem"]   roda até a próxima PARADA (ou o fim) com as ordens dadas
       ordem: atacar [alvo] · segurar · avancar · recuar · folego · guardar NOME · atar [ALIADO] · animar, e no fim a postura (firme, agressiva, defensiva)
              · lancar FEITICO [em ALVO | casa N] [sempre] [osso] · beber POCAO [em ALIADO] · usar [PECA] [em ALVO | casa N]   (a magia: só quem o jogador comanda recebe)
              · fazer HABILIDADE [em ALVO] [opções] [sempre] [postura] · trunfo=USO [se CONDIÇÃO, senão USO] · sem riposta · a postura bigorna   (as habilidades: habilidade.py)
              (a ordem `folego` acaba quando o fôlego enche: daí a pessoa segura, e a luta para e pergunta)
              (a ordem `recuar` é a retirada: a pessoa anda para trás enquanto houver inimigo de pé a menos de 8 casas; a 8 casas de todos, no fim da rodada, sai da luta.
               SEM INIMIGO DE PÉ NÃO HÁ RETIRADA: a luta acabou, e quem recuava ficou com o campo como os outros)
       ordem do grupo: atacar · segurar · recuar
  python3 luta.py demo           uma luta de exemplo num corredor, com as paradas
"""
import json, math, random, re, secrets, sys
if __name__ == '__main__': sys.modules.setdefault('luta', sys.modules[__name__])       # rodando como comando: o magia.py fala com ESTE módulo (e não com uma segunda cópia dele)
import tabelas as T
import tabelas_bichos as TB
import tabelas_magia as TM
import tabelas_povos as TP
import tabelas_efeitos as TE
import magia
import habilidade
from pessoas import ficha, maior

ESCADA = True               # A ESCADA DO MEDO (DESENHO 3.6; a única mudança da fase 1b que toca toda luta de gente): o abalado que falha por menos de 5 fica ACUADO.
                            # Só o banco a desliga (a meta B0: com ela desligada, a luta sem nada novo é a de antes, dado por dado)


class Dados:
    def __init__(s, semente=None): s.r = random.Random(semente) if semente is not None else None
    def d(s, n): return s.r.randint(1, n) if s.r else secrets.randbelow(n) + 1
D = Dados()


def semente(n):
    """só para o simulador: dados que se repetem"""
    global D
    D = Dados(n)


def d20x():
    t = [D.d(20)]
    while t[-1] == 20: t.append(D.d(20))
    return t


def jogada(bonus, faixa=(20, T.CRIT_OUTRO)):
    """o dado do golpe: 2d20 que explodem. O CRÍTICO (fase 1b) é uma FAIXA: a face alta e o mínimo do outro dado (o de antes: 20/11; o critico_19, 19/11; o Crítico, pela categoria)"""
    a, b = d20x(), d20x(); n = (a[0], b[0])
    return dict(total=sum(a) + sum(b) + bonus, falha=n == (1, 1), crit=(max(n) >= faixa[0] and min(n) >= faixa[1]))


def chance(falta):
    """a chance de 2d20 dar pelo menos `falta` (sem contar o 20 que explode; o crítico acerta sempre)"""
    n = math.ceil(falta)
    if n <= 2: return 1.0
    return max(0.05, sum(min(s - 1, 41 - s) for s in range(n, 41)) / 400)


def rola(dado, vezes=1):
    n, f = map(int, dado.split('d'))
    return sum(D.d(f) for _ in range(n * vezes))


# ---------- montar a luta ----------
SINONIMOS = {'colada': 'colado', 'água pela cintura': 'água', 'agua': 'água', 'tras': 'trás'}


def _confere(lado_a, lado_b, inicio, lugar, tempo, surpresa):
    """o cenário é conferido ANTES de qualquer dado: erro de digitação não derruba a luta no meio"""
    E = []
    if not (inicio in T.INICIO or (isinstance(inicio, int) and inicio >= 1)): E.append(f'início desconhecido: "{inicio}" (use: {", ".join(T.INICIO)}, ou um número de casas)')
    for t in tempo:
        if t not in T.TEMPO: E.append(f'tempo desconhecido: "{t}" (use: {", ".join(T.TEMPO)})')
    for k, v in lugar.items():
        if k not in ('largura', 'alto', 'cobertura', 'sem_saida'): E.append(f'chave de lugar desconhecida: "{k}" (use: largura, alto, cobertura, sem_saida)')
        elif k == 'largura' and not (v is None or (isinstance(v, int) and v >= 1)): E.append('a largura é um número de 1 para cima')
        elif k != 'largura' and v not in (None, 'A', 'B'): E.append(f'"{k}" diz de que lado: "A" ou "B" (veio "{v}")')
    if surpresa not in (None, 'A', 'B'): E.append(f'a surpresa diz o lado surpreendido: "A" ou "B" (veio "{surpresa}")')
    if not lado_a or not lado_b: E.append('cada lado precisa de pelo menos uma pessoa')
    nomes = [p['nome'] for p in lado_a + lado_b]
    if any(n.lower() == 'grupo' or ':' in n for n in nomes): E.append('ninguém pode se chamar "grupo" nem ter dois-pontos no nome (a ordem usa os dois)')
    for n in sorted(set(x for x in nomes if nomes.count(x) > 1)): E.append(f'nome repetido: "{n}" (cada um na luta tem um nome só dele)')
    for lado in (lado_a, lado_b):
        for p in lado:
            if p.get('linha') not in (None, 'frente', 'trás'): E.append(f'{p["nome"]}: a linha é "frente" ou "trás" (veio "{p.get("linha")}")')
            if p.get('moral') not in (None, 'testa', 'firme'): E.append(f'{p["nome"]}: a moral é "testa" ou "firme" (veio "{p.get("moral")}")')
            if p.get('papel') not in (None, 'frente', 'guarda'): E.append(f'{p["nome"]}: o papel é "frente" ou "guarda" (veio "{p.get("papel")}")')
            if p.get('guarda') and p['guarda'] not in [q['nome'] for q in lado if q is not p]: E.append(f'{p["nome"]} guarda "{p["guarda"]}", que não está do mesmo lado')
            for k in p.get('feiticos') or []:
                if k not in T.FEITICOS: E.append(f'{p["nome"]}: feitiço desconhecido: "{k}" (os que há: {", ".join(T.FEITICOS)})')
    if E: sys.exit('O cenário tem problema. Nenhum dado foi rolado.\n  - ' + '\n  - '.join(E))


def nova(lado_a, lado_b, inicio='perto', lugar=None, tempo=None, surpresa=None, quieto=False, ermo=None):
    inicio = SINONIMOS.get(inicio, inicio); tempo = [SINONIMOS.get(t, t) for t in (tempo or [])]; lugar = dict(lugar or {})
    for p in lado_a + lado_b:
        if p.get('linha') in SINONIMOS: p['linha'] = SINONIMOS[p['linha']]
    _confere(lado_a, lado_b, inicio, lugar, tempo, surpresa)
    S = dict(r=0, L=[], itens={}, lugar=lugar, tempo=tempo, log=[], paradas=['a luta vai começar'], fim=None, ordens={}, surpresa=surpresa, quieto=quieto,
             fila=[], comecou=False, usadas=[], sem_dano=0, sem_parada=0, dano_r=0, houve_parada=False, fechada=0, avisos=[])
    sep = T.INICIO[inicio] if isinstance(inicio, str) else inicio
    for lado, gente, x0, tras in (('A', lado_a, 0, -1), ('B', lado_b, sep, 1)):
        larg = lugar.get('largura') or 99; cheio = {}
        for p in sorted(gente, key=lambda p: p.get('linha') == 'trás'):
            f = ficha(p); f['lado'] = lado; oc = f.get('ocupa', 1)       # o que cada um toma do corredor: gente 1; o bicho, pelo tamanho
            x = x0 + (tras if p.get('linha') == 'trás' else 0)
            while cheio.get(x, 0) and cheio[x] + oc > larg: x += tras
            cheio[x] = cheio.get(x, 0) + oc
            f.update(x=x, estado='pe', feridas=[], sangra=None, atordoado=0, chao=False, preso=False, abalado=False, reac=f['reacoes'], postura='firme',
                     usou=[], testou=[], morte=[0, 0], agressor=None, recarga=0, sem_arma=False, resguardo=False, fugiu=False, golpeado=[], ini=0, pv_visto=f['pv'],
                     veneno=None, agarrado=None, encurralado=False, golpes=0, andou_t=0, feriu_t=[], sopro_r=0)
            f.setdefault('moral', 'testa'); f.setdefault('papel', 'guarda' if f.get('guarda') else 'frente'); _campos_1b(f)
            f['feridas'] = f.pop('feridas0'); f['feridas_antes'] = len(f['feridas'])
            for parte, grave in f['feridas']:               # a ferida que a pessoa já traz entra na luta com ela
                if parte == 'tronco': f['fol'] = max(0, f['fol'] - T.FERIDAS['tronco'][1 if grave else 0])
                if parte == 'pernas' and grave: f['preso'] = True
            for w in [f['arma'], f['arma2'], f['punho']] + f.get('armas_corpo', []) + [f.get('sopro')]:
                if w: w['item'] = _guarda_item(S, w['item'])
            for pc in f['partes'].values(): pc['item'] = _guarda_item(S, pc['item'])
            for src in f['fontes']: src['item'] = _guarda_item(S, src['item'])
            if f['escudo']: f['escudo']['item'] = _guarda_item(S, f['escudo']['item'])
            _guarda_magia(S, f)
            if f['fol_rodada'] + f['arma']['folego'] > f['folmax']: S['avisos'].append(f"{f['nome']} veste mais peso do que o fôlego aguenta: vai lutar sem fôlego")
            if f['nuas'] and f['partes']: S['avisos'].append(f"{f['nome']} está sem proteção em: {', '.join(f['nuas'])}")
            if oc > larg: S['avisos'].append(f"{f['nome']} é maior que o corredor: luta sem espaço")
            S['L'].append(f)
    if ermo: S['ermo'] = list(ermo)                         # as espécies do ermo onde se luta (o feitiço "chamar" só vale nele)
    if habilidade.tem_hab(S):                               # (fase 2) A LUTA DE HABILIDADE: alguém traz habilidade (a luta sem habilidade é a de sempre, dado por dado)
        S['hab'] = True
        for f in S['L']: habilidade.prepara(S, f)
    _marca_1b(S)
    if any(magia.tem_magia(f) for f in S['L']):             # A LUTA DE MAGIA: alguém traz feitiço, foco, amuleto, encanto, poção, traço novo ou fases
        S['magia'] = True
        for f in S['L']: magia.prepara(S, f)
    return S


def _guarda_magia(S, f):
    """o foco, o amuleto e as peças encantadas entram no S['itens'], como as outras peças: o desgaste deles volta ao estado"""
    if f.get('foco'): f['foco'] = _guarda_item(S, f['foco'])
    if f.get('amuleto'): f['amuleto'] = _guarda_item(S, f['amuleto'])
    for e in f.get('encantos') or []: e['item'] = _guarda_item(S, e['item'])


def _entra(S, f, lado, x):
    """alguém entra na luta já começada (o bicho chamado, o morto erguido): a ficha pronta, com o que cada lutador tem no começo"""
    f['lado'] = lado
    f.update(x=x, estado='pe', sangra=None, atordoado=0, chao=False, preso=False, abalado=False, reac=f['reacoes'], postura='firme', usou=[], testou=[], morte=[0, 0],
             agressor=None, recarga=0, sem_arma=False, resguardo=False, fugiu=False, golpeado=[], ini=0, pv_visto=f['pv'], veneno=None, agarrado=None, encurralado=False,
             golpes=0, andou_t=0, feriu_t=[], sopro_r=0)
    f.setdefault('moral', 'testa'); f.setdefault('papel', 'frente'); _campos_1b(f)
    if 'feridas0' in f: f['feridas'] = f.pop('feridas0')
    f.setdefault('feridas', []); f['feridas_antes'] = len(f['feridas'])
    for w in [f['arma'], f['arma2'], f['punho']] + f.get('armas_corpo', []) + [f.get('sopro')]:
        if w and not isinstance(w['item'], str): w['item'] = _guarda_item(S, w['item'])
    for pc in f['partes'].values():
        if not isinstance(pc['item'], str): pc['item'] = _guarda_item(S, pc['item'])
    for src in f['fontes']:
        if not isinstance(src['item'], str): src['item'] = _guarda_item(S, src['item'])
    if f['escudo'] and not isinstance(f['escudo']['item'], str): f['escudo']['item'] = _guarda_item(S, f['escudo']['item'])
    if not isinstance(f.get('foco') or '', str) or not isinstance(f.get('amuleto') or '', str) or any(not isinstance(e['item'], str) for e in f.get('encantos') or []): _guarda_magia(S, f)
    S['L'].append(f)
    if S.get('magia'): magia.prepara(S, f)
    if S.get('hab') or f.get('hab'):
        if not S.get('hab'):
            S['hab'] = True
            for o in S['L']: habilidade.prepara(S, o)
        else: habilidade.prepara(S, f)
    _marca_1b(S)
    return f


def _campos_1b(f):
    """(a parte 2, fase 1b; DESENHO 9.4) os campos de luta da base nova, em todo lutador, zerados: a barra de carga por família e os calejos (o de arma e o que o feitiço de
    controle dá na resistência), a cabeça firme, o turno perdido pela carga e os últimos turnos (ninguém perde mais de 1 em cada 3), os filetes de sangue dos efeitos, o exposto,
    o amolecido e o aberto (a rodada em que vencem: nascem vencidos, −1, para o quadro da rodada 0 não mostrar ninguém exposto), o acuado e o susto, as fontes novas de medo da
    rodada, os usos dos efeitos, a desforra, e o que volta ao estado"""
    f.update(barra={k: 0 for k in TE.FAMILIAS}, calejo_f={k: 0 for k in TE.CALEJOS}, calejo_m={k: 0 for k in TE.FAMILIAS}, firme_cabeca=0, perde_turno=False, perdidos=[],
             filetes=[], exposto=-1, amolecido=-1, aberto=-1, prazo_r={}, acuado=False, susto_r=0, medo_fontes={}, fx_usos={}, desforra={}, turnos_n=0, efeitos_gastos=[], guardia_r=[0, 0])


def _marca_1b(S):
    """a luta em que alguém traz CARGA DE CABEÇA (o Aturdir; na fase 2, o Tranco e o fecho tranco): só nela a ferida grave na cabeça conta como turno perdido e dá a cabeça
    firme (3.5). A luta sem nada novo segue a de antes, dado por dado."""
    S['carga_cabeca'] = any(w and (w.get('efeitos') or {}).get('aturdir') for f in S['L'] for w in [f.get('arma'), f.get('arma2')] + list(f.get('armas_corpo') or [])) or bool(S.get('hab') and habilidade.traz_cabeca(S))


def _guarda_item(S, it):
    for k, v in S['itens'].items():
        if v is it: return k
    k = f"p{len(S['itens']) + 1}"; S['itens'][k] = it
    return k


# ---------- olhar o campo ----------
def diz(S, txt):
    if not S['quieto']: S['log'].append(TB.contrai(txt))
def _n(x): return f'{x:g}'.replace('.', ',')                 # 23,5
def _oa(f): return 'A' if f.get('bicho') and TB.ESPECIES.get(f['bicho'], {}).get('artigo') == 'a' else 'O'       # ENCURRALADA: o gênero do BICHO, que a espécie diz. De gente a luta não sabe o gênero: as frases de gente não dependem dele
def _acoes(n): return f"{n} {'ação' if n == 1 else 'ações'}"
def _parte(e, parte): return TB.PARTES_BICHO.get(parte, parte) if e.get('bicho') else parte                       # bicho não tem braços
SUSTOS = dict(lider_caiu='o líder caiu', metade_caiu='metade dos seus caiu', golpe_terrivel='o golpe terrível', ferido_grave='por um fio', ferido='a ferida', pavor='o pavor', medo='o medo',
              medo_peca='o medo das peças')
def de_pe(S, lado=None): return [f for f in S['L'] if f['estado'] == 'pe' and (lado is None or f['lado'] == lado)]
def outro(lado): return 'B' if lado == 'A' else 'A'
def inimigos(S, f): return de_pe(S, outro(f['lado']))
def dist(a, b): return abs(a['x'] - b['x'])
def frente(f): return 1 if f['lado'] == 'A' else -1
def entre(S, a, b): return any(min(a['x'], b['x']) < o['x'] < max(a['x'], b['x']) for o in de_pe(S) if o is not a and o is not b)
def lider(S, lado): return next((f for f in S['L'] if f['lado'] == lado and f.get('lider')), None)
def por_nome(S, nome): return next((f for f in S['L'] if f['nome'] == nome), None)
def inteiro(S, chave): return S['itens'][chave]['dur'][0] > 0
def tem(f, traco): return traco in f.get('tracos', ())          # o traço de bicho (lista fechada do tabelas_bichos)


def _agarrado(S, f):
    """quem agarra este lutador agora (ou None). O bicho que cai, foge ou se afasta solta: só se agarra quem está colado."""
    if not f.get('agarrado'): return None
    g = por_nome(S, f['agarrado'])
    if g and g['estado'] == 'pe' and dist(g, f) <= 1: return g
    f['agarrado'] = None
    return None


def _nao_anda(S, f): return bool(f['preso'] or _agarrado(S, f) or (S.get('magia') and (f.get('est') or {}).get('preso')))      # a perna presa, o bicho que agarra, o feitiço que prende
def _no_ar(S, f): return tem(f, 'voa') and not f['chao'] and not f['preso'] and not S['lugar'].get('largura') and not _agarrado(S, f)
def _derruba(S, a, e): return e['estado'] == 'pe' and not efeito(S, e, 'firme') and e.get('ocupa', 1) <= a.get('ocupa', 1) and not (S.get('magia') and tem(e, 'imaterial')) and not (S.get('hab') and habilidade.firme(S, e))      # ninguém derruba quem é maior que ele (nem o imaterial)


def _apertado(S, f):
    """o bicho maior que o corredor luta apertado"""
    larg = S['lugar'].get('largura')
    return TB.APERTADO * math.ceil(f['ocupa'] - larg) if larg and f.get('ocupa', 1) > larg else 0


def arma_de(S, f):
    """a arma em uso agora: a principal; a segunda (ou as mãos) se a principal caiu, ou se é de tiro e há inimigo colado"""
    if f.get('bicho'): return f['armas_corpo'][f['golpes'] % len(f['armas_corpo'])]      # o bicho alterna as armas do corpo, golpe a golpe
    w = f['arma']
    if f['sem_arma'] or (w['distancia'] and any(dist(f, e) <= 1 for e in inimigos(S, f))): return f['arma2'] or f['punho']
    return w


def guarda_de(S, f):
    """(o bônus, a peça) do que apara os golpes agora: o escudo (arma de uma mão, escudo inteiro) ou a própria arma, o que for melhor"""
    w = arma_de(S, f); esc = f['escudo']
    if esc and w['maos'] == 1 and inteiro(S, esc['item']) and esc['bonus'] >= w['aparo']: return esc['bonus'], esc
    return w['aparo'], w


def defesa_de(S, f): return f['def_fixa'] + guarda_de(S, f)[0]


def _vale(S, f, src):
    """a fonte vale agora? A peça inteira; e o escudo só com a arma de uma mão em uso (como a Guarda e o aparo de hoje: com a arma de duas mãos, o escudo vestido não guarda)"""
    return inteiro(S, src['item']) and not (src.get('escudo') and arma_de(S, f)['maos'] != 1)


def efeito(S, f, chave):
    """o efeito de armadura, escudo, amuleto ou foco que está valendo agora (a peça desfeita não tem efeito; o escudo, só com a arma de uma mão; o mesmo efeito de duas fontes
    vale o maior: P5)"""
    return maior([src for src in f['fontes'] if _vale(S, f, src)], chave)


def _fonte(S, f, chave):
    """a fonte inteira de onde vem o efeito (para gastar o uso dele), ou None"""
    vs = [src for src in f['fontes'] if chave in src['efeitos'] and _vale(S, f, src)]
    return max(vs, key=lambda s_: TE.ordem_valor(chave, s_['efeitos'][chave])) if vs else None


def _fixo(S, f, qual, w=None, alvo=None):
    """P3: o NÚMERO FIXO novo (acerto, Defesa, coragem, resistência à carga), somado de tudo o que é novo, com o teto (+8; a resistência, +16). O de hoje (a mão, o corpo, o
    líder, a matilha, o benzido) fica fora da conta."""
    if qual == 'acerto':
        ef = (w or {}).get('efeitos') or {}; v = ef.get('certeira') or 0
        if ef.get('desforra') and alvo is not None and f['desforra'].get(alvo['nome']): v += TE.DESFORRA
        if S.get('hab'): v += habilidade.acerto_mais(S, f)                 # (fase 2) as batidas, a Sanha, a Teima, a Mira Firme, o Manter à Distância
        return min(TE.FIXO_TETO, v)
    if qual == 'defesa':
        es = f.get('escudo'); v = 0
        if es and inteiro(S, es['item']) and arma_de(S, f)['maos'] == 1: v = next((src['efeitos'].get('guarda') or 0 for src in f['fontes'] if src['item'] == es['item']), 0)
        if S.get('hab'): v += habilidade.defesa_mais(S, f)                 # (fase 2) a Guarda de Bigorna
        return min(TE.FIXO_TETO, v)
    if qual == 'coragem':
        rb = efeito(S, f, 'robusta'); return min(TE.FIXO_TETO, (efeito(S, f, 'coragem') or 0) + (rb[0] // 2 if rb else 0) + f.get('coragem_escudo', 0) + (habilidade.coragem(S, f) if S.get('hab') else 0))
    if qual == 'resistencia':
        rb = efeito(S, f, 'robusta'); return min(TE.RESIST_TETO, rb[0] if rb else 0)
    return 0


def tipo_alvo(f):
    """o tipo do alvo para a Caçadora: o dragão, o morto (quem não tem vida), o povo (goblin, orc...), o bicho ou a gente"""
    b = f.get('bicho')
    if b and (b == 'dragão' or str(b).startswith(('dragão-', 'verme-do-'))): return 'dragão'      # o dragão da tabela dos bichos e os dos dragões (tabelas_dragoes: dragão-da-serra-..., verme-do-brejo-...)
    if 'sem vida' in (f.get('tracos') or ()): return 'morto'
    if f.get('povo'): return 'povo'
    return 'bicho' if b else 'gente'


def _vaga(S, f, e, w):
    """o CERCO: em campo aberto só tantos batem corpo a corpo no mesmo alvo na mesma rodada (em volta do bicho, pelo tamanho dele)"""
    if S['lugar'].get('largura'): return True
    longe = w['haste'] and dist(f, e) == 2
    if any(n == f['nome'] for n, _ in e['golpeado']): return True
    perto, haste = e.get('cerco') or (T.CERCO, T.CERCO_HASTE)
    return sum(1 for _, l in e['golpeado'] if l == longe) < (haste if longe else perto)


def alvos(S, f, w, cerco=True):
    """[(inimigo, penalidade)] que esta arma alcança agora"""
    out = []
    for e in inimigos(S, f):
        dd = dist(f, e)
        if w['distancia']:
            if dd < 2 or dd > w['alcance']: continue
            if any(dd > T.TEMPO[k]['sem_tiro_longe'] for k in S['tempo'] if 'sem_tiro_longe' in T.TEMPO[k]): continue
        else:
            if dd > max(1, w['alcance']): continue
            if cerco and not _vaga(S, f, e, w): continue
        pen = T.ENTRE if entre(S, f, e) and S['lugar'].get('alto') != f['lado'] else 0
        if w['haste'] and dd <= 1: pen += T.HASTE_COLADO
        out.append((e, pen))
    return out


# ---------- o golpe ----------
def golpe(S, a, e, w, livre='', extra=None):
    """o golpe (ou o tiro) de a em e com a arma w. (Fase 1b) O golpe EXTRA (o segundo golpe, a ceifadora, a varredura, a tempestade; e o golpe livre de hoje) não puxa
    outro golpe extra e põe metade da carga (P8); extra='meio' tira metade do dano (a varredura). O golpe de verdade, que acertou, puxa os extras da arma."""
    r = _golpe(S, a, e, w, livre, extra)
    if r and not livre and not extra and a['estado'] == 'pe' and not S['fim']:
        _extras(S, a, w, r)
        if S.get('hab'): habilidade.extras(S, a, w, r)      # (fase 2) a Varrida
    return r


def _medo_acerto(f): return TE.ACUADO if f.get('acuado') else T.ABALADO if f['abalado'] else 0      # a escada do medo no acerto: o abalado −2, o acuado −4 (não somam)


def _luz(S, f, w):
    """o dono tem uma peça com Luz (a arma na mão, ou uma fonte inteira)? O escuro não pesa no golpe dele (no tiro, metade)"""
    return bool((w.get('efeitos') or {}).get('luz') or efeito(S, f, 'luz'))


def _guardia(S, g):
    """a Guardiã: guardar um aliado colado não gasta a reação, uma vez por rodada (o escudo inteiro)"""
    gr = g.get('guardia_r') or [0, 0]
    if not isinstance(gr, list): gr = [gr, 1]
    return bool(efeito(S, g, 'guardia')) and (gr[0] != S['r'] or gr[1] < TE.GUARDIA_RODADA)


def faixa_critico(w):
    """P6: a faixa do crítico desta arma, a melhor entre as fontes (a de antes 20/11; o critico_19, 19/11; o Crítico, pela categoria; o Golpe do Fim, 17/11), nunca melhor que 17/7"""
    ef = w.get('efeitos') or {}; fx = [(20, T.CRIT_OUTRO)]
    if ef.get('critico_19'): fx.append(TE.LEGADO['critico_19']['critico'])
    if ef.get('critico'): fx.append(tuple(ef['critico']))
    if ef.get('golpe_do_fim'): fx.append(TE.GOLPE_DO_FIM['critico'])
    return fx[0] if len(fx) == 1 else TE.melhor_critico(*fx)


def _pilha(S, a, e, w, extra):
    """P1: a conta da pilha no fim: (1 + PEÇAS) × (1 + TÉCNICA) × (1 + DOM) × ESTADOS × (1 − COURAÇA). Na fase 1b, PEÇAS (o Gume e a Caçadora contra o tipo dela, até +100%),
    os ESTADOS (o alvo exposto ×1,5; quem bate amolecido ×0,75) e a COURAÇA do alvo (em curva, até 75%); a TÉCNICA e o DOM chegam nas fases 2 e 3. A varredura: metade."""
    ef = w.get('efeitos') or {}; pc = ef.get('gume') or 0; cz = ef.get('cacadora')
    if cz and cz[1] == tipo_alvo(e): pc += cz[0]
    m = 1 + min(TE.PILHA['pecas'], pc)
    if S.get('hab'): m *= 1 + min(TE.PILHA['tecnica'], habilidade.tecnica(S, a, e, w))      # (fase 2) o grupo TÉCNICA: as batidas, a Sanha, o Golpe de Voto (até +40%)
    if e['exposto'] >= S['r']: m *= TE.EXPOSTO
    if a['amolecido'] >= S['r']: m *= TE.AMOLECIDO
    cou = efeito(S, e, 'couraca')
    if cou: m *= 1 - TE.curva(cou)
    if extra == 'meio': m *= 0.5
    return m


def _golpe(S, a, e, w, livre='', extra=None):
    g = None if w.get('area') else next((x for x in de_pe(S, e['lado']) if x.get('guarda') == e['nome'] and x is not e and dist(x, e) <= 1 and (x['reac'] > 0 or _guardia(S, x))), None)
    if g:
        if _guardia(S, g):
            gr = g.get('guardia_r') if isinstance(g.get('guardia_r'), list) else [0, 0]
            g['guardia_r'] = [S['r'], (gr[1] + 1) if gr[0] == S['r'] else 1]; diz(S, f"  {g['nome']} se põe na frente de {e['nome']} (a Guardiã: sem gastar a reação)")
        else: g['reac'] -= 1; diz(S, f"  {g['nome']} se põe na frente de {e['nome']}")
        e = g
    tiro = w['distancia']; pa, pd = T.POSTURAS.get(a['postura']) or T.POSTURAS['firme'], T.POSTURAS.get(e['postura']) or T.POSTURAS['firme']      # (a postura nova `bigorna` vale pela habilidade)
    hb = S.get('hab')
    if hb: habilidade.golpe_antes(S, a, e, w, livre, extra)             # (fase 2) a Roda, o fecho, a declarada, a Riposta, o Manter à Distância: o que a habilidade põe antes do dado
    if not tiro and not livre and not any(n == a['nome'] for n, _ in e['golpeado']): e['golpeado'].append([a['nome'], bool(w['haste'] and dist(a, e) == 2)])
    bon = w['acerto'] + pa[0] - (T.SEM_FOLEGO if a['fol'] <= 0 else 0) + _medo_acerto(a)
    bon += sum(T.FERIDAS['braços'][1 if gr else 0] for p, gr in a['feridas'] if p == 'braços')
    bon += sum(T.TEMPO[k].get('tiro' if tiro else 'acerto', 0) for k in S['tempo'])
    if 'escuro' in S['tempo'] and _luz(S, a, w): bon -= T.TEMPO['escuro']['tiro' if tiro else 'acerto'] * TE.LUZ[1 if tiro else 0]     # (fase 1b) a Luz: tira do golpe do dono a parte do escuro dela (TE.LUZ)
    elif 'escuro' in S['tempo'] and tem(a, 'vê no escuro'): bon -= T.TEMPO['escuro']['tiro' if tiro else 'acerto'] * (1 - (TP.ESCURO_TIRO if tiro else TP.ESCURO))      # quem vê no escuro (o povo, etapa 4b): no golpe o escuro tira só a metade; no tiro, inteiro (ESCURO_TIRO)
    if S['lugar'].get('alto') == a['lado']: bon += T.ALTO['tiro' if tiro else 'acerto']
    if tiro and S['lugar'].get('cobertura') == e['lado']: bon += T.COBERTURA
    if entre(S, a, e) and S['lugar'].get('alto') != a['lado'] and not w.get('area'): bon += T.ENTRE
    if w['haste'] and dist(a, e) <= 1: bon += T.HASTE_COLADO
    if tiro and a['fugiu']: bon += T.TIRO_FUGINDO
    esp = _golpe_especial(S, a, w, livre); mb, md = _dos_bichos(S, a, e, w, esp); bon += mb      # o bote e a investida; o que os traços e o tamanho mexem
    bon += _fixo(S, a, 'acerto', w, e)                                                               # (fase 1b) a Certeira e a Desforra (P3: até +8)
    if hb: bon += habilidade.acerto_pena(S, a)                                                       # (fase 2) o acerto a menos: a declarada, a Riposta, a bigorna
    df = md + (e['def_fixa'] if w.get('area') else defesa_de(S, e)) + pd[1] - (T.SEM_FOLEGO if e['fol'] <= 0 else 0) + (T.CHAO if e['chao'] else 0) + (T.PRESO if e['preso'] else 0) + (T.RESGUARDO if e['resguardo'] else 0)
    if not w.get('area'): df += _fixo(S, e, 'defesa')                                                # (fase 1b) a Guarda do escudo (P3: até +8)
    pn = TE.ABERTO if e['aberto'] >= S['r'] else 0                                                   # (fase 1b) o aberto do atordoado (as penas novas de Defesa no alvo: vale a pior)
    if hb: pn = min(pn, habilidade.abrir(S, a, e)); df += habilidade.defesa_pena(S, a, e)           # (fase 2) o ABRIR da Roda (não soma com o aberto); o preço da Sanha
    df += pn
    df += sum(T.TEMPO[k].get('defesa', 0) for k in S['tempo'])
    df -= T.FLANCO * min(T.FLANCO_MAX, sum(1 for n, _ in e['golpeado'] if n != a['nome']))       # cercado: cada um que já bateu nele abre a guarda para o próximo
    if S.get('magia'): mb, md = magia.no_golpe(S, a, e, w); bon += mb; df += md                 # a bênção, o escudo, o mau-olhado, a fúria, o escuro de quem é noturno...
    tr = e['partes'].get('tronco'); perf = (w.get('efeitos') or {}).get('perfura')                # mirar a fresta: só contra armadura melhor que a arma, e só quando compensa
    # (fase 1b) a escolha de mirar é a de hoje, com ou sem a Perfura: a Perfura só muda a proteção (com a mira, vale o maior; nunca abaixo de um terço), e assim nunca piora o golpe.
    # Com a escolha refeita pela Perfura (mirar renderia menos), o robô de hoje, que pesa a mira sem contar o crítico, deixava de mirar no nível 150 e a Perfura Comum TIRAVA 15 pontos
    ganho = T.MIRA_PROT; fr = habilidade.fresta(S, a, w) if hb else None; ma = fr or T.MIRA_ACERTO      # (fase 2) a Mira Firme do Perito: a fresta pede −5 no tiro
    mira = bool(tr and inteiro(S, tr['item']) and tr['cat'] > w['cat'] and not tem(e, 'couraça') and not w.get('area') and chance(df - bon - ma) * ganho > chance(df - bon))
    if mira:
        bon += ma
        if fr: habilidade.mirou(a)
    if w['item'] not in S['usadas']: S['usadas'].append(w['item'])
    for pc in list(e['partes'].values()) + ([e['escudo']] if e['escudo'] else []):
        if pc['item'] not in S['usadas']: S['usadas'].append(pc['item'])
    j = jogada(bon, faixa_critico(w))
    cab = f"  {a['nome']} {'sopra em' if w.get('area') else 'atira em' if tiro else 'golpeia'} {e['nome']}" + (f' ({livre})' if livre and not w.get('area') else '') + (f" ({esp['nome']})" if esp else '') + (' mirando a fresta' if mira else '') + (' (no ar)' if not tiro and w['alcance'] < 2 and _no_ar(S, e) else '')
    if a.get('bicho') and not w.get('area'): a['golpes'] += 1; a['andou_t'] = 0
    if j['falha']:
        diz(S, f"{cab}: dois 1, erra feio"); _gasta(S, a, w, 1)
        if hb: habilidade.errou(S, a, e, w, j, df)
        return None
    ponta = ''
    if j['total'] < df and not j['crit']:
        if (w.get('efeitos') or {}).get('ponta_certa') and 'ponta_certa' not in a['usou'] and df - j['total'] <= TE.PONTA_CERTA:     # (fase 1b) a Ponta Certa: uma vez por luta, o golpe que errou por 5 ou menos acerta
            a['usou'].append('ponta_certa'); ponta = ' (a Ponta Certa: errava por pouco, e acerta)'
        else:
            gb, gp = guarda_de(S, e); aparado = not tiro and gb > 0 and df - j['total'] <= gb
            diz(S, f"{cab}: {_n(j['total'])} contra {_n(df)}, {'aparado' if aparado else 'erra'}")
            if aparado and _aparadora(S, e, gp) and not (TE.APARADORA_RODADA == 'rodada' and e.get('aparou_r') == S['r']) and not (TE.APARADORA_RODADA == 'luta' and e.get('aparou_r')):
                a['fol'] -= 1; e['aparou_r'] = S['r']; diz(S, f"    a Aparadora de {e['nome']}: {a['nome']} perde 1 de fôlego")
            if aparado and gp['cat'] != w['cat']:                # dois aços se encontram: o pior gasta
                if gp['cat'] > w['cat']: _gasta(S, a, w, 1)
                elif gp is e['escudo']: _gasta_armadura(S, e, gp['nome'], gp['item'], 1)
                else: _gasta(S, e, gp, 1)
            if hb: habilidade.errou(S, a, e, w, j, df)                    # (fase 2) a batida que errou; a RIPOSTA de quem apara
            return None
    if w.get('dom') and not j['crit'] and j['total'] - w['dom'] < df and not ponta:       # O DOM (etapa da magia): este golpe só passou por causa dele (não rola nada a mais: a luta de quem não tem dom é a de sempre)
        if a.get('controla') and not a.get('dom_fez'): diz(S, f"    ({a['nome']} acerta por pouco: sem o dom, errava)")
        a['dom_fez'] = True                                 # a luta que volta ao estado faz disto a marca.dom_visto
    parte = T.ONDE[D.d(10)]; pc = e['partes'].get(parte); vestida = bool(pc and inteiro(S, pc['item']))
    prot = pc['rd'] * (1 if w.get('area') else T.MATRIZ[w['golpe']][pc['material']]) / (2 if j['crit'] and not tem(e, 'couraça') else 1) if vestida else T.NU
    prot_novo = prot
    if hb:                                                  # (fase 2) o GOLPE DE QUEBRA: o mesmo efeito da Perfura (vale o maior: P5); custa 1 de fôlego no golpe em que vale
        qb = habilidade.quebra(S, a, w, pc, vestida)
        if qb: perf = min(perf, qb) if perf else qb; a['fol'] -= 1
    if mira and vestida and pc['cat'] > w['cat']: prot /= T.MIRA_PROT
    if perf and vestida and pc['cat'] > w['cat']: prot_novo = prot_novo * max(TE.PERFURA_PISO, min(1 / T.MIRA_PROT if mira else 1.0, perf))      # (fase 1b) a Perfura: vale o maior com a mira, nunca abaixo de um terço
    else: prot_novo = prot
    # OS DADOS (P2): o maior entre o crítico (2), o golpe especial de hoje e o Golpe do Fim (4), nunca mais de 4; a regra de hoje, com os mesmos dados, é a medida do teto
    vh = max(2 if j['crit'] else 1, esp['dados'] if esp else 1); vz = vh
    if j['crit'] and (w.get('efeitos') or {}).get('golpe_do_fim'): vz = min(max(vz, TE.GOLPE_DO_FIM['dados']), max(TE.DADOS_MAX, vh))
    if hb: vz = max(vz, min(max(TE.DADOS_MAX, vh), habilidade.dados_vezes(S, a, a.get('_hg'))))      # (fase 2) o FECHO FUNDO: o maior com o crítico e o Golpe do Fim, nunca mais de 4
    nd, fd = map(int, w['dado'].split('d')); rolos = [D.d(fd) for _ in range(nd * vz)]
    soma_x = habilidade.dado_extra(S, a, e, w, j, a['_hg']) if hb else 0     # (fase 2) O DADO SOMADO (o trunfo no dano, o Rito de Veia): uma vez, sem dobrar no crítico
    hoje = int(sum(rolos[:nd * vh]) * T.K_DANO * w['mult'] / prot * w['fmult'])
    mult = _pilha(S, a, e, w, extra); teto_txt = ''
    if mult != 1 or vz != vh or prot_novo != prot or soma_x:          # (fase 1b) A PILHA, para baixo uma vez; e O TETO DA PILHA: nunca mais que 7 vezes o golpe de hoje, com os mesmos dados
        dano = int((sum(rolos) + soma_x) * T.K_DANO * w['mult'] / prot_novo * w['fmult'] * mult); bruto = dano
        if dano > TE.TETO_PILHA * hoje: dano = TE.TETO_PILHA * hoje; teto_txt = ' (o teto da pilha segura o golpe)'
    else: dano = bruto = hoje
    if S.get('mede') is not None: S['mede'].append(dict(novo=bruto, final=dano, hoje=hoje, vezes=vz, crit=j['crit'], faixa=faixa_critico(w), couraca=TE.curva(efeito(S, e, 'couraca') or 0), mult=mult))
    if S.get('magia') and e.get('tracos'): dano = magia.dano_aco(S, a, e, w, dano)              # o osso (corte e ponta pela metade) e o imaterial (a arma comum, uma categoria abaixo)
    # o aço gasta o aço
    if dano == 0: _gasta(S, a, w, 1)
    if vestida and (w['cat'] > pc['cat'] or j['crit']): _gasta_armadura(S, e, pc['nome'], pc['item'], 2 if w['cat'] >= pc['cat'] + 2 else 1)
    esc = e['escudo']
    if j['crit'] and esc and inteiro(S, esc['item']) and arma_de(S, e)['maos'] == 1: _gasta_armadura(S, e, esc['nome'], esc['item'], 1)
    pv0 = e['pv']; e['pv'] -= dano; e['agressor'] = a['nome']; exp = e['exposto'] >= S['r']
    diz(S, f"{cab}: {_n(j['total'])} contra {_n(df)}{ponta}{', CRÍTICO' + (' (a couraça não abre)' if tem(e, 'couraça') else '') if j['crit'] else ''}, {_parte(e, parte)}: {dano} ({max(e['pv'], 0)}/{e['pvmax']})" + (' · o aço não passa' if dano == 0 else '') + (' · exposto' if exp and dano else '') + teto_txt)
    q = _devolve(S, a, e, w, dano, pv0) if not tiro and not w.get('area') and a['estado'] == 'pe' else 0      # (fase 1b) o Devolve: o % do dano levado (decisão 2), só em quem golpeia de perto
    if q > 0:
        a['pv'] -= q; diz(S, f"    a armadura de {e['nome']} devolve {q} em {a['nome']} ({max(a['pv'], 0)}/{a['pvmax']})"); S['dano_r'] += q / a['pvmax']
        if a['pv'] <= 0: _cai(S, a, 0)
    if S.get('magia') and tem(e, 'ardente'): magia.fogo_de_volta(S, a, e, w)                     # quem golpeia de perto o corpo que arde leva o fogo de volta
    if dano <= 0:
        if hb: habilidade.acertou(S, a, e, w, j, 0, pv0, pc, vestida, extra or livre)
        return dict(e=e, acertou=True, dano=0, caiu=False)
    S['dano_r'] += dano / e['pvmax']
    if e.get('funda') is None or e['funda'] < w['cat']: e['funda'] = w['cat']                   # A FERIDA FUNDA: a maior categoria que tirou PV desde o PV cheio (a cura segue a lei ao contrário)
    terrivel = dano >= e['pvmax'] * T.FERIDA_GRAVE; abertas = len(e['feridas'])
    if any(((x or {}).get('efeitos') or {}).get('desforra') for x in (e.get('arma'), e.get('arma2'))): e['desforra'][a['nome']] = e['turnos_n'] + 1     # (fase 1b) a Desforra de quem foi ferido
    if e['pv'] <= 0: _cai(S, e, dano, manso=bool((w.get('efeitos') or {}).get('fio_manso')) and pv0 < e['pvmax'] * TE.FIO_MANSO)
    elif dano >= e['pvmax'] * T.FERIDA or (j['crit'] and dano >= e['pvmax'] * T.FERIDA_MIN): _ferida(S, e, parte, terrivel, w, dano)
    _depois_1b(S, a, e, w, dano, pv0, pc, vestida, extra or livre)
    if hb: habilidade.acertou(S, a, e, w, j, dano, pv0, pc, vestida, extra or livre)      # (fase 2) a batida e o fecho, o abrir, a Sanha, o trunfo de efeito, a declarada
    if w['efeitos'].get('derruba') and 'derruba' not in a['usou'] and _derruba(S, a, e):
        a['usou'].append('derruba'); e['chao'] = True; e['calejo_f']['pernas'] += 1; diz(S, f"    {e['nome']} vai ao chão")      # (fase 1b) o derruba de hoje entra no calejo de pernas
    if a.get('bicho') or e.get('bicho'): _depois_do_golpe(S, a, e, w, dano, esp, len(e['feridas']) > abertas)
    if terrivel:
        for o in de_pe(S, e['lado']):
            if o is not e and dist(o, e) <= 2: _moral(S, o, 'golpe_terrivel')
    if e['estado'] == 'pe' and e['pv'] < e['pvmax'] * 0.25: _moral(S, e, 'ferido_grave')
    if S.get('magia'): magia.feriu(S, a, e, w, dano, len(e['feridas']) > abertas)                # a dose da lâmina, o dreno, a maldição, a concentração de quem canaliza, a fase do chefe
    return dict(e=e, acertou=True, dano=dano, caiu=e['estado'] in ('caido', 'morto'))


def _devolve(S, a, e, w, dano, pv0):
    """(fase 1b) O DEVOLVE: parte do DANO LEVADO volta em quem golpeia de perto. O dano levado é o que o alvo perdeu de PV: o golpe que passa do PV que ele tinha não leva mais que
    isso (como a Vampira, que cura do que tirou). Sem esse teto, o golpe enorme na cabeça sem elmo (o ×27 da regra de ouro) voltava inteiro em quem bateu e o derrubava: a
    armadura de baixo com Devolve desfazia o item que decide (o banco, B3: a arma duas acima vencia 78%, e a meta é 85%; com o teto, 99%)."""
    src = _fonte(S, e, 'devolve')
    return int(min(dano, max(pv0, 0)) * src['efeitos']['devolve']) if src else 0


def _aparadora(S, e, gp):
    """a peça que aparou (o escudo ou a arma de e) tem a Aparadora? Quem teve o golpe aparado perde 1 de fôlego"""
    if gp is e.get('escudo'): return bool(next((src['efeitos'].get('aparadora') for src in e['fontes'] if src['item'] == gp['item']), False))
    return bool((gp.get('efeitos') or {}).get('aparadora'))


def _depois_1b(S, a, e, w, dano, pv0, pc, vestida, extra):
    """(fase 1b) o golpe tirou PV: a Vampira cura quem bate (no teto da cura do dia); a Sangria e a Brasa abrem filetes; o Aturdir e o Atar enchem a barra da família; o Expõe,
    a Escancara e o Amolece põem o estado; o Medo da peça conta como fonte de medo da rodada (testa no fim dela, junto das outras). Nada disto rola dado."""
    ef = w.get('efeitos') or {}
    if not ef: return
    vp = ef.get('vampira')
    if vp and a['estado'] == 'pe' and a['pv'] < a['pvmax']:
        teto = max(0, int(a['pvmax'] * T.CURA_TETO) - a.get('curado', 0)); g = min(a['pvmax'] - a['pv'], teto, int(min(dano, max(pv0, 0)) * vp))
        if g > 0: a['pv'] += g; a['curado'] = a.get('curado', 0) + g; S['dano_r'] -= g / a['pvmax']; diz(S, f"    a Vampira de {a['nome']} bebe do golpe (+{g}: {a['pv']}/{a['pvmax']})"); _conta(S, 'vampira', g)
    if e['estado'] != 'pe': return
    sg = ef.get('sangria')
    if sg and sg != 'ferida' and not tem(e, 'sem vida'): _filete(S, e, max(1, int(dano * sg[0])), sg[1], f"sangria:{a['nome']}", soma=sg[2], sem_atar=sg[3])
    if ef.get('brasa'): _filete(S, e, max(1, int(dano * TE.BRASA[0])), TE.BRASA[1], 'fogo', soma=True)
    if ef.get('aturdir'): _carga(S, e, w, 'cabeca', ef['aturdir'], pc, vestida, extra)
    if ef.get('atar') and S.get('magia') and (e.get('mana_max') or 0) > 0: _carga(S, e, w, 'mana', TE.ATAR_CARGA, pc, vestida, extra)      # (o Atar só ata quem tem Mana a atar)
    if e['estado'] != 'pe': return
    if ef.get('escancara'): _prazo(S, e, 'exposto', TE.ESCANCARA_RODADAS)
    elif ef.get('expoe'): _prazo(S, e, 'exposto', TE.EXPOE_RODADAS)
    if ef.get('amolece'): _prazo(S, e, 'amolecido', TE.AMOLECE_RODADAS)
    if ef.get('medo'): e['medo_fontes'][f"medo:{a['nome']}"] = max(e['medo_fontes'].get(f"medo:{a['nome']}", 0), ef['medo'])


def _conta(S, k, v=1): c = S.setdefault('conta', {}); c[k] = c.get(k, 0) + v           # os contadores que o banco lê (S['conta'], como na magia)


def _prazo(S, e, campo, dur):
    """P9: o estado tem potência fixa e prazo que soma, até 3 rodadas (contando a de agora); o campo guarda a rodada em que ele vence. APLICAR DE NOVO é de novo numa rodada
    nova: o segundo golpe que fere na mesma rodada não soma mais prazo (o mesmo estado, no mesmo alvo, soma uma vez por rodada). Somando a cada golpe, quem bate 3 ou 4 vezes
    por turno deixava o alvo exposto o tempo todo: o Expõe (normal: até 10) dava +12,0; somando uma vez por rodada, +7,6, o medido do contrato (+7,1; a Escancara, +17,2)"""
    r = S['r']; pr = e.setdefault('prazo_r', {})
    if pr.get(campo) == r: return
    pr[campo] = r; x = e[campo]; e[campo] = min(r + TE.PRAZO_MAX - 1, (x if x >= r else r - 1) + dur)
    _conta(S, campo)


def _filete(S, e, q, rodadas, fonte, soma=True, sem_atar=False):
    """um FILETE de sangue (ou de fogo): cada fonte é um filete, com o seu tanto por rodada e o seu prazo; até 3 contando o da ferida (o quarto toma o lugar do mais fraco).
    A Sangria da Incomum e da Rara não soma: o filete dela se renova (o maior tanto e o maior prazo); da Épica para cima, e o fogo, somam."""
    if not soma:
        velho = next((x for x in e['filetes'] if x[2] == fonte), None)
        if velho: velho[0] = max(velho[0], q); velho[1] = max(velho[1], rodadas); return
    e['filetes'].append([q, rodadas, fonte, bool(sem_atar)])
    while len(e['filetes']) > 1 and len(e['filetes']) + (1 if e['sangra'] else 0) > TE.FILETES_MAX:
        e['filetes'].remove(min(e['filetes'][:-1], key=lambda x: (x[0], x[1])))
    _conta(S, 'filetes')


def _chefe(f):
    """chefe e bicho grande começam com +4 na resistência à carga (3.4; 3.5, freio 4): o bicho chefe da tabela, o grande e o enorme, o chefe com fases; e, entre a gente, o CHEFE
    é o de moral firme (3.6: "contra moral firme (o chefe)") ou o das fases. O líder de um bando não é chefe por ser líder. (O +4 de saída vale só na resistência à carga, e não
    como calejo na Firmeza: o chefe com +4 na Firmeza contra o prender e o nó mudaria a luta de magia de hoje, que a fase 1b não toca: 3.7.7.)"""
    if f.get('bicho'):
        esp = TB.ESPECIES.get(f['bicho']) or {}
        return bool(esp.get('chefe')) or f.get('tamanho') in ('grande', 'enorme') or bool(f.get('fases'))
    return f.get('moral') == 'firme' or bool(f.get('fases'))


def resistencia(S, e, fam):
    """3.4: RESISTÊNCIA = 6 + bônus de Vigor ÷ 2 + 4 por calejo da família (o de arma e o que o feitiço de controle deu) + 4 no chefe e no bicho grande + a Robusta (até +16)"""
    return TE.resistencia((e.get('atributos') or {}).get('Vigor', 50), e['calejo_f'][fam] + e['calejo_m'][fam], _chefe(e), _fixo(S, e, 'resistencia'))


def _pode_perder(f):
    """ninguém perde mais de 1 turno em cada 3 seguidos (3.5, freio 5): nem um perdido nos dois últimos turnos, nem um já para perder"""
    return not f['perde_turno'] and not any(f['perdidos'][-(TE.JANELA_TURNOS - 1):])


def _carga(S, e, w, fam, q, pc, vestida, extra):
    """3.4: o golpe que tira PV soma a carga do efeito na barra da família, no alvo (contra armadura de categoria maior que a arma, pela metade; na parte nua, em dobro; o golpe
    extra, metade, no mínimo 1). A barra cheia (a resistência): o estado pega, a barra zera, e o alvo ganha um calejo daquela família. Na cabeça firme não soma carga de cabeça."""
    if e['estado'] != 'pe' or not q: return
    mc = S.get('mede_carga') if fam == 'cabeca' else None
    if mc is not None: mc.setdefault(e['nome'], [[0, 0]])[-1][0] += 1      # (o banco, EF6) os golpes que tiram PV até cada atordoar: todos...
    if fam == 'cabeca' and (e['firme_cabeca'] > 0 or e['perde_turno']): return
    if vestida and pc['cat'] > w['cat']: q //= 2
    elif not vestida: q *= 2
    if extra: q = max(1, q // 2)
    if q <= 0: return
    if mc is not None: mc[e['nome']][-1][1] += 1                          # ... e só os que enchem a barra (os da cabeça firme não enchem: o calejo sozinho)
    res = resistencia(S, e, fam); antes = e['barra'][fam]
    if fam == 'cabeca' and not _pode_perder(e):           # ninguém perde mais de 1 turno em cada 3: o estado não pega agora; a barra fica cheia (sem calejo: ele vem quando o estado pega)
        e['barra'][fam] = min(antes + q, res)
        if e['barra'][fam] >= res > antes: diz(S, f"    a carga de cabeça de {e['nome']} está cheia, mas ninguém perde mais de 1 turno em cada 3: atordoa no próximo golpe que puder")
        return
    e['barra'][fam] = antes + q
    if e['barra'][fam] < res: return
    e['barra'][fam] = 0; e['calejo_f'][fam] += 1; _conta(S, 'carga_' + fam)
    if fam == 'cabeca':
        e['perde_turno'] = True; e['aberto'] = S['r'] + 1; _conta(S, 'atordoa')
        if mc is not None: mc[e['nome']].append([0, 0])
        diz(S, f"    {e['nome']} fica ATORDOADO: perde o próximo turno e fica aberto (−4 na Defesa) até o fim da rodada seguinte")
        _para(S, e, f"{e['nome']} ficou atordoado (perde o próximo turno)", so_controlado=True)
    elif fam == 'pernas':                                   # (fase 2) a carga de pernas cheia (a Rasteira, o trunfo de rasteira): ao chão
        if not e['chao'] and not efeito(S, e, 'firme') and not (S.get('hab') and habilidade.firme(S, e)) and not (S.get('magia') and tem(e, 'imaterial')):
            e['chao'] = True; diz(S, f"    {e['nome']} vai ao chão (a carga de pernas)"); _para(S, e, f"{e['nome']} foi ao chão", so_controlado=True)
    elif fam == 'mana':
        st = e.setdefault('est', {}); st['no'] = max(st.get('no') or 0, TE.ATADO_TURNOS)
        diz(S, f"    {e['nome']} fica ATADO: a Mana não volta e cada feitiço custa 1 a mais, por {TE.ATADO_TURNOS} turnos")


def _extras(S, a, w, r):
    """(fase 1b) os golpes EXTRAS que o golpe que acertou puxa (P8: nenhum puxa outro, e põem metade da carga): o SEGUNDO GOLPE (vezes por luta, no mesmo alvo), a VARREDURA
    (um outro inimigo colado, metade do dano) ou a TEMPESTADE (o dano inteiro), e a CEIFADORA (quem derrubou golpeia outro que alcança). De graça: sem ação nem fôlego."""
    ef = w.get('efeitos') or {}; e = r['e']
    if not ef: return
    sg = ef.get('segundo_golpe')
    if sg and a['fx_usos'].get('segundo_golpe', 0) < sg and e['estado'] == 'pe' and a['estado'] == 'pe' and not S['fim'] and dist(a, e) <= max(1, w['alcance']):
        a['fx_usos']['segundo_golpe'] = a['fx_usos'].get('segundo_golpe', 0) + 1; _conta(S, 'segundo_golpe')
        golpe(S, a, e, w, livre='o segundo golpe', extra=True)
    vt = 'tempestade' if ef.get('tempestade') else 'varredura' if ef.get('varredura') else None
    if vt and not w['distancia'] and a['estado'] == 'pe' and not S['fim']:
        outros = [o for o in inimigos(S, a) if o is not e and dist(a, o) <= 1]
        if outros:
            o = min(outros, key=lambda x: (x['pv'] / x['pvmax'], x['nome'])); _conta(S, vt)
            golpe(S, a, o, w, livre='a tempestade' if vt == 'tempestade' else 'a varredura', extra=True if vt == 'tempestade' else 'meio')
    if ef.get('ceifadora') and r['caiu'] and a['estado'] == 'pe' and not S['fim']:
        al = [x[0] for x in alvos(S, a, w, cerco=False)]
        if al:
            o = min(al, key=lambda x: (x['pv'] / x['pvmax'], x['nome'])); _conta(S, 'ceifadora')
            golpe(S, a, o, w, livre='a ceifadora', extra=True)


def _golpe_especial(S, a, w, livre):
    """o BOTE (o primeiro golpe do bicho na luta) e a INVESTIDA (o golpe depois de correr): acertam mais, rolam os dados mais vezes e derrubam.
    E O GOLPE PELAS COSTAS (etapa 4b, E1 a): quem tem a manha de Treinado ou mais, na primeira rodada, contra o lado surpreendido, dá o primeiro golpe de corpo a corpo
    com mais acerto e os dados rolados mais vezes (tabelas.COSTAS). Não derruba."""
    if not a.get('bicho') and (a.get('manha') or 0) >= T.COSTAS['desde'] and not w['distancia'] and not livre and 'costas' not in a['usou'] and S['r'] == 1 and S.get('surpresa') and S['surpresa'] != a['lado']:
        a['usou'].append('costas'); return dict(nome='pelas costas', acerto=T.COSTAS['acerto'], dados=T.COSTAS['dados'])
    if not a.get('bicho') or w['distancia'] or livre: return None
    if tem(a, 'bote') and 'bote' not in a['usou']:
        a['usou'].append('bote'); return dict(nome='bote', acerto=TB.BOTE['acerto'], dados=TB.BOTE['dados'])
    if tem(a, 'investida') and a['andou_t'] >= TB.INVESTIDA['casas']: return dict(nome='investida', acerto=TB.INVESTIDA['acerto'], dados=TB.INVESTIDA['dados'])
    return None


def _dos_bichos(S, a, e, w, esp):
    """o que os traços, o tamanho e a moral dos bichos mexem neste golpe: (no acerto de quem bate, na Defesa de quem apanha). Entre gente, (0, 0)."""
    bon = esp['acerto'] if esp else 0; df = 0
    if a.get('veneno'): bon += TB.VENENO['acerto']
    if _agarrado(S, a): bon += TB.AGARRADO['acerto']
    if _agarrado(S, e): df += TB.AGARRADO['defesa']
    if S['lugar'].get('largura'): bon += _apertado(S, a); df += _apertado(S, e)
    if a.get('encurralado'): bon += TB.ENCURRALADO
    if not w['distancia'] and w['alcance'] < 2 and _no_ar(S, e): bon += TB.VOA
    return bon, df


def _depois_do_golpe(S, a, e, w, dano, esp, abriu):
    """o golpe feriu, e um dos dois é bicho: o bote, a investida e a matilha derrubam, o veneno entra, o que agarra segura, e o bicho ferido testa a coragem"""
    if esp and esp['nome'] == 'pelas costas': esp = None             # o golpe pelas costas (etapa 4b) não derruba
    if not e['chao'] and _derruba(S, a, e) and (esp or (tem(a, 'matilha') and w.get('corpo') and sum(1 for n, _ in e['golpeado'] if n != a['nome'] and tem(por_nome(S, n), 'matilha')) >= TB.MATILHA)):
        e['chao'] = True; diz(S, f"    {e['nome']} vai ao chão" + ('' if esp else ' (a matilha derruba)'))
        if esp and esp['nome'] == 'bote': e['atordoado'] = max(e['atordoado'], TB.BOTE['atordoa'])           # pego de surpresa
    if w.get('corpo') and not w.get('area') and e['estado'] == 'pe':
        if tem(a, 'veneno') and not (S.get('magia') and tem(e, 'sem vida')):
            q = max(1, int(dano * TB.VENENO['fracao'] * TP.VENENO)) if tem(e, 'resiste a veneno') else max(1, int(dano * TB.VENENO['fracao'])); ant = e['veneno'] or [0, 0]      # quem resiste a veneno (o povo): a metade
            e['veneno'] = [max(q, ant[0]), TB.VENENO['rodadas']]; diz(S, f"    o veneno entra em {e['nome']} ({e['veneno'][0]} por rodada)")
            if S.get('magia'): e['veneno_cat'] = max(e.get('veneno_cat', 0), w['cat'])        # a categoria do veneno (o antídoto tira até a dele)
        if tem(a, 'agarra') and a['estado'] == 'pe' and dist(a, e) <= 1 and e.get('ocupa', 1) <= a['ocupa'] and not any(o is not e and o['estado'] == 'pe' and _agarrado(S, o) is a for o in S['L']) \
                and not (S.get('magia') and tem(e, 'imaterial')):
            if e.get('agarrado') != a['nome']:
                e['agarrado'] = a['nome']; diz(S, f"    {a['nome']} AGARRA {e['nome']}"); _para(S, e, f"{a['nome']} agarrou {e['nome']}", so_controlado=True)
            if e['nome'] not in a['feriu_t']: a['feriu_t'].append(e['nome'])
    if abriu and e.get('bicho') and e['estado'] == 'pe': _moral(S, e, 'ferido')


def _gasta(S, a, w, n):
    it = S['itens'][w['item']]
    if w['efeitos'].get('nao_quebra') or it['dur'][0] <= 0: return
    it['dur'][0] = max(0, it['dur'][0] - n)
    if it['dur'][0] == 0:
        diz(S, f"    ✖ {w['nome']} de {a['nome']} QUEBRA"); _para(S, a, f"{w['nome']} de {a['nome']} quebrou")
        w.update(acerto=w['acerto'] - T.BON[w['cat']] + T.QUEBRADA, mult=T.MULT[0] * (T.DUAS_MAOS if w['maos'] == 2 and not w['distancia'] else 1), cat=0, efeitos={}, aparo=0, nome=w['nome'] + ' (quebrou)')


def _gasta_armadura(S, e, nome, chave, n):
    it = S['itens'][chave]
    if it['dur'][0] <= 0 or any(src['item'] == chave and src['efeitos'].get('nao_quebra') for src in e['fontes']): return
    it['dur'][0] = max(0, it['dur'][0] - n)
    if it['dur'][0] == 0:
        diz(S, f"    ✖ {nome} de {e['nome']} se desfaz"); _para(S, e, f"{nome} de {e['nome']} quebrou")
        if e.get('robusta_fol'):                             # (fase 1b) a Robusta que se desfaz leva o fôlego máximo a mais que dava (fica o da outra fonte, se houver)
            rb = efeito(S, e, 'robusta'); novo = rb[1] if rb else 0
            if novo < e['robusta_fol']: e['folmax'] -= e['robusta_fol'] - novo; e['robusta_fol'] = novo; e['fol'] = min(e['fol'], e['folmax'])


def _ferida(S, e, parte, grave, w, dano):
    sangria5 = bool(w['efeitos'].get('sangra')) or w['efeitos'].get('sangria') == 'ferida'      # o `sangra` de antes, e a Sangria Comum (fase 1b): a ferida sangra 5 rodadas
    e['feridas'].append([parte, grave]); g = 1 if grave else 0; txt = f"    FERIDA{' GRAVE' if grave else ''} em {e['nome']}, {_parte(e, parte)}: "; sangra = grave or sangria5 or bool(w.get('queima'))
    if parte == 'cabeça':
        perde = T.FERIDAS['cabeça'][g]
        if grave and S.get('carga_cabeca'):                 # (fase 1b) numa luta com carga de cabeça, a grave conta como turno perdido (dá a cabeça firme); na cabeça firme, tira só 1 ação, como a leve
            if e['firme_cabeca'] > 0 or not _pode_perder(e): perde = T.FERIDAS['cabeça'][0]
            else: e['turno_cabeca'] = True
        if S.get('hab') and not grave and habilidade.sanha_cabeca(e): perde = 0; txt += 'a Sanha segura a cabeça (não atordoa)'
        e['atordoado'] = max(e['atordoado'], perde)
        if perde: txt += f"a cabeça roda (perde {_acoes(e['atordoado'])})"
    elif parte == 'braços':
        txt += f"{T.FERIDAS['braços'][g]:+d} no acerto".replace('-', '−')
        if grave and not e['sem_arma'] and not e.get('bicho'): e['sem_arma'] = True; txt += ' e larga a arma'
    elif parte == 'tronco': e['fol'] = max(0, e['fol'] - T.FERIDAS['tronco'][g]); sangra = True; txt += 'perde o fôlego'
    else:
        firme = bool(efeito(S, e, 'firme')) or bool(S.get('magia') and tem(e, 'imaterial')) or bool(S.get('hab') and habilidade.firme(S, e))      # (o imaterial não tem pernas que cedam; a bigorna do Adepto)
        if not firme: e['chao'] = True
        e['preso'] = e['preso'] or grave                    # a perna presa: a pessoa ainda se levanta, mas não sai mais do lugar
        txt += ('a perna cede, mas a peça firme segura de pé' if firme else 'vai ao chão') + ('; com a perna presa, não sai mais do lugar (levantar-se, pode)' if grave else '')
    if sangra and S.get('magia') and tem(e, 'sem vida'): sangra = False; txt += ' (não sangra: não tem vida)'
    if sangra:
        n = T.SANGRA_RODADAS[1 if grave or sangria5 or w.get('queima') else 0]; q = max(1, int(dano * T.SANGRA)); ant = e['sangra'] or [0, 0]
        e['sangra'] = [max(q, ant[0]), max(n, ant[1])]; txt += f' · {"queima" if w.get("queima") else "sangra"} {e["sangra"][0]} por {e["sangra"][1]} rodadas'
        while len(e['filetes']) + 1 > TE.FILETES_MAX: e['filetes'].remove(min(e['filetes'], key=lambda x: (x[0], x[1])))      # (fase 1b) até 3 filetes, contando o da ferida: o quarto toma o lugar do mais fraco
        if w.get('queima'): e['queimando'] = True              # (o fim da rodada diz "queima", não "sangra")
    diz(S, txt); _para(S, e, f"{e['nome']} levou uma ferida ({_parte(e, parte)}{', grave' if grave else ''})", so_controlado=True)


def _salva(S, e):
    """(fase 1b) O IMORTAL: uma vez por dia, o dono fica com 1 PV em vez de cair (e não morre do golpe). O salvamento de 1 PV é um só por dia, venha de onde vier (P5): a ficha
    já o tira quando foi gasto hoje (estado.lutador: salvo_dia), e o uso gasto volta ao estado num evento (ato.luta_fecha: ['item', id, 'efeito', 'gasta', 'imortal'])."""
    if e['estado'] != 'pe' or e['fx_usos'].get('imortal'): return False
    src = _fonte(S, e, 'imortal')
    if not src: return False
    e['fx_usos']['imortal'] = 1; e['pv'] = 1; it = S['itens'][src['item']]; _conta(S, 'imortal')
    if it.get('id'): e['efeitos_gastos'].append([it['id'], 'imortal'])
    diz(S, f"    ✦ {e['nome']} não cai: o Imortal de {it['nome']} o segura de pé, com 1 PV (uma vez por dia)")
    _para(S, e, f"o Imortal segurou {e['nome']} de pé (1 PV; uma vez por dia)")
    return True


def _cai(S, e, dano, manso=False):
    if _salva(S, e): return
    desfaz = bool(S.get('magia') and tem(e, 'sem vida'))     # quem não tem vida não fica caído: a zero de PV se desfaz
    macico = (dano > e['pvmax'] * 0.5 and not manso) or desfaz          # (fase 1b) o Fio Manso: o golpe que mataria quem já estava abaixo de 1/4 do PV o deixa caído, vivo
    e['estado'] = 'morto' if macico else 'caido'; e['pv'] = min(e['pv'], 0)
    if manso and not macico: e['morte'][0] = 3; diz(S, f"    o Fio Manso deixa {e['nome']} caído e vivo (para fazer preso)")
    if S.get('magia') and e.get('canaliza'): magia.perde(S, e, 'sem teste')      # quem cai perde o feitiço que canalizava
    diz(S, f"    ☠ {e['nome']} SE DESFAZ" if desfaz else f"    ☠ {e['nome']} MORRE" if macico else f"    ▼ {e['nome']} CAI")
    _para(S, e, f"{e['nome']} {'morreu' if macico else 'caiu'}" + (magia.cura_ao_alcance(S, e) if S.get('magia') and not macico else ''))
    if S.get('hab'): habilidade.caiu(S, e)                    # (fase 2) a Vigília de um aliado; a marca da queda (o Sopro de Volta)
    aliados = de_pe(S, e['lado'])
    if e.get('lider'):
        for o in aliados: _moral(S, o, 'lider_caiu')
    if len(aliados) * 2 <= len([f for f in S['L'] if f['lado'] == e['lado']]):
        for o in aliados: _moral(S, o, 'metade_caiu')
    _fim(S)


def _moral(S, f, motivo, cd=None, cd_pavor=None):
    """o teste de coragem (3.14), com A ESCADA DO MEDO (fase 1b, DESENHO 3.6): firme, ABALADO (−2 no acerto), ACUADO (−4; não avança), QUEBRA (foge ou se rende). O firme que
    falha por menos de 10 fica abalado (por 10 ou mais, quebra); o abalado que falha por menos de 5 fica acuado (por 5 ou mais, quebra); o acuado que falha quebra. Quem o jogador
    comanda para no abalado; o bicho foge, como hoje. `cd`: a FONTE NOVA de medo (o Medo e o Temível das peças), que testa uma vez por rodada, junta, com o calejo de ânimo."""
    nova = cd is not None
    if f['moral'] == 'firme' or f['estado'] != 'pe': return
    if not nova and ((motivo in f['testou'] and motivo not in ('golpe_terrivel', 'medo')) or f.get('moral_r') == [S['r'], motivo]): return
    if not inimigos(S, f): return                           # sem inimigo de pé não há de quem fugir nem a quem se render: quem ficou com o campo não testa a coragem
    bicho = f.get('bicho') and not f.get('controla')
    if bicho and f['chao'] and not f['preso'] and S['lugar'].get('sem_saida') != f['lado']: return       # o bicho no chão não tem como correr agora: o susto fica para quando ele se levantar
    if nova and (tem(f, 'sem vida') or (f.get('controla') and f['abalado'])): return                     # o sem vida não sente medo; quem o jogador comanda, já abalado, não testa mais as fontes novas
    if not nova: f['testou'].append(motivo); f['moral_r'] = [S['r'], motivo]
    f['susto_r'] = S['r']
    meus, deles = len(de_pe(S, f['lado'])), len(de_pe(S, outro(f['lado'])))
    ld = lider(S, f['lado']); bon = f['vontade_b'] + f.get('coragem', 0) + (T.MORAL_LIDER if ld and ld['estado'] == 'pe' and ld is not f else 0)
    if S.get('magia') and (f.get('est') or {}).get('benzido'): bon += TM.ESTADOS['benzido']['coragem']          # o benzido tem coragem a mais
    if tem(f, 'matilha') and any(o is not f and tem(o, 'matilha') for o in de_pe(S, f['lado'])): bon += TB.MATILHA_CORAGEM       # a matilha dá coragem
    bon += T.MORAL_MAIS if meus > deles else T.MORAL_MENOS if deles >= 2 * meus else 0
    bon += _fixo(S, f, 'coragem')                            # (fase 1b) a Coragem do amuleto, metade da Robusta e o Escudo que Conta (P3: até +8)
    if nova: bon += TE.CALEJO_ANIMO * f['calejo_f']['animo']                                           # o calejo de ânimo: +4 por degrau que uma fonte nova já fez pegar
    t = sum(d20x()) + sum(d20x()) + bon; que = SUSTOS.get(motivo, motivo.replace('_', ' '))
    if not nova: cd = T.MORAL[motivo] if motivo in T.MORAL else (cd_pavor or TB.PAVOR) if motivo == 'pavor' else TM.MEDO if motivo == 'medo' else TB.MORAL[motivo]
    if nova: _conta(S, 'medo_testes')
    if t >= cd: return
    if nova: _conta(S, 'medo_falhas')
    if bicho:       # o BICHO não fica abalado nem se rende: foge. Encurralado (sem saída, ou sem pernas para correr), luta até o fim
        if S['lugar'].get('sem_saida') == f['lado'] or f['preso'] or (S.get('magia') and (f.get('est') or {}).get('preso')):
            if not f.get('encurralado'): f['encurralado'] = True; diz(S, f"    {f['nome']} está ENCURRALAD{_oa(f)}: não tem {'para onde' if not f['preso'] else 'pernas para'} fugir ({que}: {t} contra {cd})")
            return
        f['estado'] = 'fugiu'; diz(S, f"    {f['nome']} FOGE ({que}: {t} contra {cd})"); _para(S, f, f"{f['nome']} fugiu")
        if not _no_ar(S, f): _golpe_livre(S, f, 'pelas costas')      # quem voa sai por cima
        if _nao_saiu(S, f): return
        if f.get('lider'):
            for o in de_pe(S, f['lado']): _moral(S, o, 'lider_caiu')
        _fim(S); return
    if f.get('controla'):       # quem o jogador comanda não foge nem se rende pelo dado: fica abalado, e a escolha é do jogador
        if nova and not f['abalado']: f['calejo_f']['animo'] += 1
        f['abalado'] = True; diz(S, f"    {f['nome']} FRAQUEJA ({que}: {t} contra {cd})"); _para(S, f, f"{f['nome']} fraquejou ({que}): seguir lutando assim, recuar ou render-se é escolha sua"); return
    if t > cd - T.MORAL_QUEBRA and not f['abalado']:
        if nova: f['calejo_f']['animo'] += 1
        f['abalado'] = True; diz(S, f"    {f['nome']} FRAQUEJA ({que}: {t} contra {cd})"); return
    if ESCADA and f['abalado'] and not f.get('acuado') and t > cd - TE.QUEBRA_ABALADO:          # (fase 1b) A ESCADA: o abalado que falha por pouco fica ACUADO (não avança; −4 no acerto)
        if nova: f['calejo_f']['animo'] += 1
        f['acuado'] = True; _conta(S, 'acuado'); diz(S, f"    {f['nome']} fica ACUADO ({que}: {t} contra {cd}): não avança contra quem o assusta"); return
    rende = f['pv'] < f['pvmax'] * 0.25 or S['lugar'].get('sem_saida') == f['lado']
    if rende and inimigos(S, f) and all(o.get('bicho') for o in inimigos(S, f)):       # ninguém se rende a um bicho: foge, se tem por onde
        if S['lugar'].get('sem_saida') == f['lado']:
            f['abalado'] = True; diz(S, f"    {f['nome']} não tem a quem se render nem por onde fugir ({que}: {t} contra {cd})"); return
        rende = False
    f['estado'] = 'rendido' if rende else 'fugiu'
    diz(S, f"    {f['nome']} {'SE RENDE' if rende else 'FOGE'} ({que}: {t} contra {cd})")
    _para(S, f, f"{f['nome']} {'se rendeu' if rende else 'fugiu'}")
    if not rende: _golpe_livre(S, f, 'pelas costas')
    if not rende and _nao_saiu(S, f): return
    if f.get('lider'):
        for o in de_pe(S, f['lado']): _moral(S, o, 'lider_caiu')
    _fim(S)


def _nao_saiu(S, f):
    """quem fugia e levou, de costas, o golpe que o pôs no chão (ou lhe prendeu a perna) NÃO SAIU: segue na luta, onde caiu. Devolve True se foi assim."""
    if f['estado'] != 'fugiu' or not (f['chao'] or f['preso']): return False
    f['estado'] = 'pe'; txt = f"{f['nome']} fugiu"
    if txt in S['paradas']: S['paradas'].remove(txt)
    if f['preso'] and f.get('bicho') and not f.get('controla'): f['encurralado'] = True
    diz(S, f"    {f['nome']} NÃO SAI: o golpe {'prendeu-lhe a perna' if f['preso'] else 'pôs no chão quem fugia'}" + (f" (ENCURRALAD{_oa(f)}: luta até o fim)" if f.get('encurralado') else ''))
    return True


def _golpe_livre(S, f, porque, quem=None, vinha_de=None):
    """UM golpe livre em f, de um inimigo com reação e arma de corpo a corpo que o alcance (o de arma mais longa primeiro).
    quem: só estes podem dar · vinha_de: só de quem tem arma mais longa que a de f, e só se f acabou de ENTRAR no alcance dele"""
    meu = arma_de(S, f)['alcance']
    for e in sorted(quem if quem is not None else inimigos(S, f), key=lambda e: -arma_de(S, e)['alcance']):
        w = arma_de(S, e); alc = max(1, w['alcance'])
        if e['estado'] != 'pe' or e['reac'] <= 0 or w['distancia'] or dist(e, f) > alc: continue
        if vinha_de is not None and (w['alcance'] <= meu or abs(vinha_de - e['x']) <= alc): continue
        e['reac'] -= 1; return e, golpe(S, e, f, w, livre=porque)
    return None


def _para(S, f, txt, so_controlado=False):
    """uma PARADA: o que faz a luta parar e perguntar. Vale o que toca o lado do jogador (A), o líder do outro, e toda rendição."""
    if so_controlado and not f.get('controla'): return
    if f['lado'] == 'A' or f.get('lider') or 'rendeu' in txt:
        if txt not in S['paradas']: S['paradas'].append(txt)
        S['houve_parada'] = True


# ---------- o turno de cada um ----------
def _passo(S, f=None):
    if f is not None and _no_ar(S, f): return T.PASSO          # quem voa não pisa na lama nem na água
    return min([T.PASSO] + [T.TEMPO[k]['passo'] for k in S['tempo'] if 'passo' in T.TEMPO[k]])


def _ordem_de(S, a):
    """a ordem que vale para este lutador agora (a dele, se o jogador o comanda; a do grupo, se é do lado A e não guarda ninguém)"""
    if a.get('controla'): return (S['ordens'].get(a['nome']) or {}).get('acao')
    return S['ordens'].get('grupo') if a['lado'] == 'A' and a['papel'] != 'guarda' else None


def _fica(S, a):
    """este aliado não vai para a frente: num corredor, quem vem atrás pode trocar de lugar com ele"""
    if a['chao'] or _nao_anda(S, a) or a['fol'] <= 0 or arma_de(S, a)['distancia']: return True
    o = _ordem_de(S, a)
    if o in ('recuar', 'folego'): return True
    if alvos(S, a, arma_de(S, a), cerco=False): return False
    g = por_nome(S, a.get('guarda') or '')
    return o == 'segurar' or bool(g and g['estado'] == 'pe' and dist(a, g) <= 1)


def _livre(S, f, nx, avanca):
    """dá para entrar na casa nx? 'sim' · 'troca' (corredor cheio: troca de lugar com um aliado) · 'contorna' (campo aberto:
    passa pela casa do inimigo que os outros seguram) · '' (não dá)"""
    larg = S['lugar'].get('largura'); la = [e for e in inimigos(S, f) if e['x'] == nx]
    if la:
        if larg or not avanca: return ''
        if _no_ar(S, f): return 'contorna'                      # quem voa passa por cima da linha
        colados = [a for a in de_pe(S, f['lado']) if a is not f and any(dist(a, e) <= 1 for e in la)]
        return 'contorna' if len(colados) >= T.SEGURA * len(la) else ''
    if larg:
        meus = [a for a in de_pe(S, f['lado']) if a['x'] == nx and a is not f]      # a casa está cheia? (cada um toma o seu tanto; o bicho grande demais cabe sozinho, apertado)
        if meus and sum(a.get('ocupa', 1) for a in meus) + f.get('ocupa', 1) > larg: return 'troca' if any(_troca(S, f, a, avanca) for a in meus) else ''
    return 'sim'


def _troca(S, f, a, avanca):
    """f pode trocar de lugar com o aliado a? (a não vai para onde f vai, os dois tomam o mesmo tanto do corredor, e ninguém tira do lugar quem o bicho agarrou)"""
    return _fica(S, a) == avanca and a.get('ocupa', 1) == f.get('ocupa', 1) and not _agarrado(S, a) and not (S.get('magia') and (a.get('est') or {}).get('preso'))      # (o preso do feitiço não troca de lugar)


def _rumo(S, f, w, alvo=None):
    """para que lado da linha andar (+1 ou −1) para chegar em quem a arma não alcança; 0 se não há para onde ir"""
    perto = [x[0] for x in alvos(S, f, w, cerco=False)]
    cand = [alvo] if alvo else [e for e in inimigos(S, f) if not any(e is p for p in perto)]
    cand = [e for e in cand if e['x'] != f['x']]
    if not cand: return 0
    e = min(cand, key=lambda e: dist(f, e))
    return 1 if e['x'] > f['x'] else -1


def _anda(S, f, dx, recuo=False, ate=None):
    """anda até PASSO casas para o lado dx da linha. Devolve as casas andadas.
    Quem se afasta de um inimigo colado leva o golpe livre dele (no avanço, só de quem não está seguro por dois dos seus)."""
    avanca = not recuo; passo = _passo(S, f)
    if avanca and dx == frente(f) and S['lugar'].get('alto') == outro(f['lado']) and not _no_ar(S, f): passo = 1       # subindo
    if recuo and S.get('hab') and passo >= T.PASSO: passo = max(passo, habilidade.recuo(S, f))          # (fase 2) o PÉ DE LEBRE: mais casas no recuo
    if not _livre(S, f, f['x'] + dx, avanca): return 0
    colados = [e for e in inimigos(S, f) if dist(f, e) <= 1 and abs(e['x'] - (f['x'] + dx)) > dist(f, e)]
    if avanca: colados = [e for e in colados if len([a for a in de_pe(S, f['lado']) if a is not f and dist(a, e) <= 1]) < T.SEGURA]
    if colados and not _no_ar(S, f):                            # quem voa sai por cima: não dá as costas a ninguém
        if recuo: f['fugiu'] = True
        _golpe_livre(S, f, 'no recuo' if recuo else 'pelo flanco', quem=colados)
    andou = 0
    for _ in range(passo):
        if f['estado'] != 'pe' or f['chao'] or _nao_anda(S, f): break      # o golpe que o pegou no caminho o parou
        nx = f['x'] + dx; como = _livre(S, f, nx, avanca)
        if not como: break
        al = alvos(S, f, arma_de(S, f))
        if avanca and como == 'sim' and (any(x[0] is ate for x in al) if ate else al): break    # já alcança: para aqui
        if como == 'troca':
            o = next(a for a in de_pe(S, f['lado']) if a['x'] == nx and a is not f and _troca(S, f, a, avanca))
            o['x'] = f['x']; diz(S, f"  {f['nome']} troca de lugar com {o['nome']}")
        elif como == 'contorna': diz(S, f"  {f['nome']} contorna a linha")
        de = f['x']; f['x'] = nx; andou += 1
        if avanca:
            gl = _golpe_livre(S, f, 'o alcance bate primeiro', vinha_de=de)
            if gl and S.get('hab') and f['estado'] == 'pe' and habilidade.segura(S, gl[0], gl[1]):      # (fase 2) o MANTER À DISTÂNCIA do Perito: ferido, não entra
                f['x'] = de; andou -= 1; diz(S, f"    {gl[0]['nome']} mantém {f['nome']} à distância"); break
        if como != 'sim': break
    return andou


def _viva(S, f):
    """a ordem que vale nesta ação para quem o jogador comanda: a do `fazer ... sempre` que não age agora (a mira já feita, o ferro sem sangue a estancar) cede à de antes (fase 2)"""
    o = S['ordens'].get(f['nome']) or {}
    return (o.get('antes') or {}) if o.get('acao') == 'fazer' else o


def _decide(S, f, pagou):
    """o que este lutador faz com a ação: ('golpe', alvo) · ('anda', lado, recuo?, até quem) · ('folego',) · ('levanta',) · ('pega',) · ('recarrega',) · ('espera',) · ('sopro',)"""
    w = arma_de(S, f); o = S['ordens'].get(f['nome']) or {}
    if not f.get('controla'): o = dict(acao=_ordem_de(S, f)) if _ordem_de(S, f) else {}
    acao = o.get('acao', 'atacar'); f['postura'] = o.get('postura', f['postura'] if f.get('controla') else 'firme')
    if S.get('hab'):                                        # (fase 2) a postura nova (a bigorna); a ação de habilidade (o Brado, o Rito, a Mira, o Ferro, o Sopro, a atadura que cura)
        habilidade.postura(S, f, o)
        r = habilidade.decide(S, f, o, pagou)
        if r: return r
        if f.get('controla'): o = _viva(S, f); acao = o.get('acao', 'atacar')
    if S.get('magia'):                                      # A MAGIA: a ordem de lançar, beber ou usar (de quem o jogador comanda) e a regra curta dos outros (magia.escolhe)
        r = magia.decide(S, f, o, pagou)
        if r: return r
        if f.get('controla'): o = _viva(S, f); acao = o.get('acao', 'atacar')
    custo = w['folego'] + (0 if pagou else _peso(S, f))
    if acao == 'folego' and f['fol'] >= f['folmax']:        # A ORDEM DE TOMAR FÔLEGO ACABA QUANDO O FÔLEGO ENCHE: daí em diante segura (bate em quem chega), e a luta para e pergunta
        acao = 'segurar'; (S['ordens'].get(f['nome']) or {}).update(acao='segurar')
        _para(S, f, f"{f['nome']} recuperou o fôlego ({f['fol']}/{f['folmax']}): a ordem de tomar fôlego acabou, e agora segura até nova ordem", so_controlado=True)
    if acao in ('atar', 'animar') and f.get('controla'):     # (fase 1b) as ordens de uma vez: atar [ALIADO] e animar (o Escudo que Conta); depois, volta a ordem de antes
        ant = o.get('antes')
        if ant: S['ordens'][f['nome']] = ant
        else: S['ordens'].pop(f['nome'], None)
        return ('atar', o.get('alvo')) if acao == 'atar' else ('animar',)
    if acao == 'folego' or f['fol'] < min(custo, f['folmax']): return ('folego',)
    if f['chao']: return ('levanta',)
    colado = any(dist(f, e) <= 1 for e in inimigos(S, f))
    if not f.get('controla') and f['filetes'] and not colado and _ataveis_rodada(f) >= f['pvmax'] * TE.ATAR_SOZINHO: return ('atar', None)      # (fase 1b) quem o jogador não comanda ata a si (só o que se ata conta)
    if not f.get('controla') and efeito(S, f, 'escudo_que_conta') and 'escudo_que_conta' not in f['usou'] and any(dist(f, o) <= TE.ESCUDO_CONTA['casas'] and (o['abalado'] or o.get('acuado')) for o in de_pe(S, f['lado'])):
        return ('animar',)
    if f['sem_arma'] and not colado: return ('pega',)
    preso = _nao_anda(S, f)                                     # a perna que não anda mais, ou o bicho que o agarra
    tras = -frente(f); pode_recuar = not preso and bool(_livre(S, f, f['x'] + tras, False))
    if acao == 'recuar':                                    # A RETIRADA: quem recua ANDA PARA TRÁS enquanto houver inimigo de pé a menos de RETIRADA casas (a 8 de todos, no fim da rodada, saiu da luta)
        rt = habilidade.retirada(S, f) if S.get('hab') else T.RETIRADA
        if min([dist(f, e) for e in inimigos(S, f)] or [rt]) < rt and pode_recuar: return ('anda', tras, True, None)
        acao = 'atacar' if colado else 'segurar'            # longe o bastante, segura; encurralado, luta
    if w['distancia'] and f['recarga'] > 0: return ('recarrega',)
    if not f.get('controla') and f['arma']['distancia'] and not f['sem_arma'] and colado and pode_recuar and not f['fugiu']: return ('anda', tras, True, None)   # o atirador se afasta de quem colou
    al = alvos(S, f, w); nome = o.get('alvo'); pref = next((x for x in inimigos(S, f) if x['nome'] == nome), None) if nome else None
    if nome and not pref:
        if f.get('controla'): _para(S, f, f"o alvo de {f['nome']} ({nome}) não está mais de pé")
        o['alvo'] = None
    if f.get('bicho') and not pref: pref = next((x[0] for x in al if _agarrado(S, x[0]) is f), None)      # o bicho não larga quem agarrou
    if f.get('sopro') and f['sopro_r'] <= 0 and f['fol'] >= f['sopro']['folego']:              # o SOPRO: quando pega dois ou mais, ou quando não alcança ninguém de outro jeito
        n = len(_no_sopro(S, f))
        if n >= 2 or (n == 1 and not al): return ('sopro',)
    if pref and not any(x[0] is pref for x in al) and not preso and not f.get('acuado'):      # o alvo da ordem está fora de alcance: vai até ele (o acuado não avança)
        dx = _rumo(S, f, w, pref)
        if dx and _livre(S, f, f['x'] + dx, True): return ('anda', dx, False, pref)
    if al:
        e = next((x for x in al if x[0] is pref), None)
        if not e:
            limpos = [x for x in al if x[1] == 0] or al
            ag = next((x for x in limpos if x[0]['nome'] == f['agressor']), None)
            e = ag if ag and D.d(10) <= 6 else min(limpos, key=lambda x: x[0]['pv'] / x[0]['pvmax'])
        return ('golpe', e[0])
    gd = next((x for x in de_pe(S, f['lado']) if x['nome'] == f.get('guarda')), None)
    if gd:
        if dist(f, gd) <= 1: return ('espera',)
        s = 1 if gd['x'] > f['x'] else -1
        if not preso and _livre(S, f, f['x'] + s, True): return ('anda', s, False, None)     # sem caminho até o guardado, luta como soldado
    if preso: return ('espera',)
    if acao == 'segurar':
        apanha = any(arma_de(S, e)['distancia'] or dist(e, f) <= max(1, arma_de(S, e)['alcance']) for e in inimigos(S, f))
        if not apanha: return ('espera',)
        if f.get('controla'):
            _para(S, f, f"{f['nome']} está ao alcance deles e não alcança ninguém: segurar assim é só apanhar"); return ('espera',)
    if f.get('acuado'): return ('espera',)                  # (fase 1b) o ACUADO não avança contra quem o assustou: só segura, guarda, toma fôlego ou recua
    dx = _rumo(S, f, w)
    return ('anda', dx, False, None) if dx else ('espera',)


def _peso(S, f):
    """o fôlego que a armadura cobra numa rodada em que a pessoa se mexe (o couro do bicho é o corpo dele: não pesa nem esquenta)"""
    return f['fol_rodada'] + sum(T.TEMPO[k].get('folego', 0) for k in S['tempo']) + (sum(T.TEMPO[k].get('folego_armadura', 0) for k in S['tempo']) if not f.get('bicho') and any(p['material'] != 'couro' for p in f['partes'].values()) else 0)


def _no_sopro(S, f):
    """os inimigos de pé que o sopro deste bicho pega agora"""
    alc = min([f['sopro']['alcance']] + [T.TEMPO[k]['sem_tiro_longe'] for k in S['tempo'] if 'sem_tiro_longe' in T.TEMPO[k]])       # o tempo vale como num tiro
    return [e for e in inimigos(S, f) if dist(f, e) <= alc]


def _turno_do_bicho(S, f, fim=False):
    """o que só o bicho faz no começo e no fim do turno dele: a carne que fecha, o sopro que volta, a presa que ele solta"""
    if fim:
        for v in S['L']:
            if v.get('agarrado') == f['nome'] and v['nome'] not in f['feriu_t']: v['agarrado'] = None; diz(S, f"  {f['nome']} solta {v['nome']}")
        return
    f['feriu_t'] = []
    if f['sopro_r'] > 0: f['sopro_r'] -= 1
    if tem(f, 'regenera') and f['pv'] < f['pvmax']:
        g = min(f['pvmax'] - f['pv'], max(1, int(f['pvmax'] * TB.REGENERA))); f['pv'] += g; S['dano_r'] -= g / f['pvmax']
        diz(S, f"  {f['nome']} regenera (+{g}: {f['pv']}/{f['pvmax']})")


def _diz_passo(S, txt, i0):
    """a linha do passo entra no registro ANTES do golpe que o alcance deu no caminho (o passo veio primeiro, e foi ao entrar no alcance que ele apanhou):
    assim ninguém aparece avançando depois de cair ou de morrer. Só a ordem das linhas muda; nenhum dado é rolado aqui."""
    if S['quieto']: return
    pos = next((i for i in range(i0, len(S['log'])) if '(o alcance bate primeiro)' in S['log'][i]), len(S['log']))
    S['log'].insert(pos, TB.contrai(txt))


def _turno(S, f):
    f['resguardo'] = False; f['reac'] = f['reacoes']; f['fugiu'] = False; f['turnos_n'] += 1
    mg = S.get('magia'); sv = bool(mg and tem(f, 'sem vida'))
    if sv: f['fol'] = f['folmax']                           # quem não tem vida não cansa
    zerado = f['fol'] <= 0                                     # começou o turno sem fôlego: uma ação só
    f['fol'] = min(f['folmax'], f['fol'] + 1 + (T.POSTURAS.get(f['postura']) or T.POSTURAS['firme'])[2])
    custos = [1] if zerado else [1] * T.ACOES + ([] if sv else list(f['esforcos']))      # (nem faz a ação a mais)
    base = T.ACOES
    if S['r'] == 1 and not zerado and _arrancada(S, f): custos = [1] + custos; base += 1; diz(S, f"  {f['nome']} sai na arrancada (uma ação a mais)")      # (fase 1b) a Arrancada
    if f.get('bicho'): _turno_do_bicho(S, f)
    if mg: magia.comeco(S, f)                                  # a Mana volta, o campo se paga, o feitiço longo sai (ou se perde)
    if S.get('hab'): habilidade.comeco(S, f)                   # (fase 2) a Sanha soma, o Rito conta, a declarada fica pronta, o robô acende e declara
    perdeu = False
    if f['perde_turno']:                                       # (fase 1b) ATORDOADO PELA CARGA: perde o turno inteiro; daí, a cabeça firme até o fim do segundo turno em que volta a agir
        f['perde_turno'] = False; f['atordoado'] = 0; custos = []; perdeu = True; f['firme_cabeca'] = TE.FIRME_TURNOS; f.pop('turno_cabeca', None)
        diz(S, f"  {f['nome']} está atordoado: perde o turno"); _conta(S, 'turnos_perdidos')
    elif f['atordoado']:
        perde = min(len(custos), f['atordoado']); custos = custos[perde:]; f['atordoado'] = 0; diz(S, f"  {f['nome']} ainda sente o golpe: perde {_acoes(perde)}")
        if f.pop('turno_cabeca', False): perdeu = True; f['firme_cabeca'] = TE.FIRME_TURNOS; _conta(S, 'turnos_perdidos')      # a grave na cabeça, numa luta com carga de cabeça
    pagou = False; feitas = 0
    for mult in custos:
        if f['estado'] != 'pe' or S['fim']: break
        if mg: f['_restam'] = max(0, T.ACOES - feitas)
        ac = _decide(S, f, pagou); w = arma_de(S, f)
        if feitas >= base:                                     # a ação A MAIS (o esforço): só para golpear, e guardando um terço do fôlego (a postura agressiva gasta tudo)
            if ac[0] != 'golpe' or f['postura'] == 'defensiva': break
            if f['fol'] - w['folego'] * mult < (0 if f['postura'] == 'agressiva' else f['folmax'] // 3): break
        if S.get('hab'): habilidade.acao(S, f, ac)            # (fase 2) a outra ação zera a Roda; o fôlego e o recuo apagam a Sanha (só a ação que acontece: a decidida e largada no freio acima não mexe)
        feitas += 1
        if ac[0] in ('golpe', 'anda', 'sopro', 'lanca', 'hab') and not pagou: pagou = True; f['fol'] -= _peso(S, f)      # a armadura cobra o fôlego dela também na rodada em que se lança
        if ac[0] == 'folego':
            g = rola(T.TOMA_FOLEGO[0]) + T.TOMA_FOLEGO[1]; tinha = max(f['fol'], 0); f['fol'] = min(f['folmax'], tinha + g); f['resguardo'] = True
            diz(S, f"  {f['nome']} toma fôlego (+{f['fol'] - tinha}: {f['fol']}/{f['folmax']})" if f['fol'] > tinha else f"  {f['nome']} se resguarda (o fôlego já está cheio: {f['fol']}/{f['folmax']})")
        elif ac[0] == 'levanta': f['chao'] = False; diz(S, f"  {f['nome']} se levanta" + (' (com a perna presa: não sai do lugar)' if f['preso'] else ''))
        elif ac[0] == 'pega': f['sem_arma'] = False; diz(S, f"  {f['nome']} apanha a arma")
        elif ac[0] == 'recarrega': f['recarga'] -= 1
        elif ac[0] == 'espera': f['resguardo'] = True; break
        elif ac[0] == 'anda':
            i0 = len(S['log']); k = _anda(S, f, ac[1], recuo=ac[2], ate=ac[3])
            if not k: f['resguardo'] = True; break
            f['fol'] -= mult; _diz_passo(S, f"  {f['nome']} {'recua' if ac[2] else 'avança'} ({k} casa{'s' if k > 1 else ''})", i0)
            if f.get('bicho') and not ac[2]: f['andou_t'] += k               # a investida conta as casas corridas desde o último golpe
        elif ac[0] == 'golpe':
            golpe(S, f, ac[1], w); f['fol'] -= w['folego'] * mult; f['recarga'] = w['recarga'] if w['distancia'] else 0
        elif ac[0] == 'sopro':
            ws = f['sopro']; f['fol'] -= ws['folego'] * mult; f['sopro_r'] = TB.SOPRO['recarga']; diz(S, f"  {f['nome']} SOPRA")
            for e in _no_sopro(S, f):
                if f['estado'] == 'pe' and e['estado'] == 'pe': golpe(S, f, e, ws, livre='o sopro')
        elif ac[0] in ('lanca', 'bebe'):                        # A MAGIA: lançar (1 ação, 2, ou começar o longo), soltar o encanto, beber
            feitas += magia.acoes(ac) - 1; magia.faz(S, f, ac)
            if f.get('canaliza'): _fim(S); break               # quem começou a canalizar não faz mais nada neste turno
        elif ac[0] == 'atar': _ata(S, f, ac[1])                 # (fase 1b) atar: corta o filete mais forte (em si ou num aliado colado)
        elif ac[0] == 'animar': _anima(S, f)                   # (fase 1b) o Escudo que Conta
        elif ac[0] == 'hab': habilidade.faz(S, f, ac)          # (fase 2) o Brado, o Rito de Veia, a Mira Firme, o Ferro em Brasa, o Sopro de Volta
        _fim(S)
    if f['perdidos'] is not None:                             # (fase 1b) os últimos turnos (ninguém perde mais de 1 em cada 3) e a cabeça firme, que conta os turnos em que ele age
        f['perdidos'] = (f['perdidos'] + [perdeu])[-(TE.JANELA_TURNOS - 1):]
        if S.get('mede_turnos') is not None: S['mede_turnos'].setdefault(f['nome'], []).append(perdeu)
        if not perdeu and f['firme_cabeca'] > 0: f['firme_cabeca'] -= 1
        if f['desforra']: f['desforra'] = {k: v for k, v in f['desforra'].items() if v > f['turnos_n']}
    if mg: magia.fim_turno(S, f)
    if f.get('bicho'): _turno_do_bicho(S, f, fim=True)
    if f['fol'] > 0: f['avisou_fol'] = False
    elif f['estado'] == 'pe' and f.get('controla') and not f.get('avisou_fol'): f['avisou_fol'] = True; _para(S, f, f"{f['nome']} está sem fôlego")


def _arrancada(S, f):
    """a Arrancada (na arma em uso ou numa fonte inteira): uma ação a mais na primeira rodada"""
    return bool((arma_de(S, f).get('efeitos') or {}).get('arrancada') or efeito(S, f, 'arrancada'))


def _filetes_rodada(f): return sum(x[0] for x in f['filetes']) + (f['sangra'][0] if f['sangra'] else 0)
def _ataveis_rodada(f):
    """o sangue por rodada que atar pode cortar: a ferida e os filetes que se atam (os da Sangria Lendária para cima não se atam). Contando os que não se atam, quem o jogador não
    comanda escolhia atar sem ter o que atar, ação após ação, e ficava parado enquanto o filete durasse"""
    return sum(x[0] for x in f['filetes'] if not x[3]) + (f['sangra'][0] if f['sangra'] else 0)


def _ata(S, f, nome):
    """ATAR (3.3; a ordem `atar [ALIADO]`): 1 ação, em si ou num aliado colado: corta o filete mais forte (o da ferida, ou um dos efeitos; o da Sangria Lendária não se ata)"""
    if S.get('hab') and habilidade.tem(f, 'estanca'): habilidade.ata(S, f, nome); return      # (fase 2) a MÃO QUE ESTANCA: corta mais filetes e cura (do Mestre, firma o caído colado)
    o = por_nome(S, nome) if nome else f
    if not o or o['estado'] != 'pe' or o['lado'] != f['lado'] or dist(f, o) > 1: o = f
    cands = [('ferida', f_) for f_ in ([o['sangra']] if o['sangra'] else [])] + [('efeito', x) for x in o['filetes'] if not x[3]]
    if not cands: diz(S, f"  {f['nome']} {'se ata' if o is f else 'ata ' + o['nome']}, mas não há filete que se ate"); return
    qual, x = max(cands, key=lambda c: c[1][0]); _conta(S, 'atar')
    if qual == 'ferida': o['sangra'] = None; o.pop('queimando', None)
    else: o['filetes'].remove(x)
    diz(S, f"  {f['nome']} {'se ata' if o is f else 'ata ' + o['nome']}: corta o filete de {x[0]} por rodada" + (f" ({_filetes_rodada(o)} ainda por rodada)" if _filetes_rodada(o) else ''))


def _anima(S, f):
    """o ESCUDO QUE CONTA (1 ação, uma vez por luta; a ordem `animar`): os aliados a 2 casas descem um degrau do medo e ganham +2 na coragem até o fim da luta"""
    if not efeito(S, f, 'escudo_que_conta') or 'escudo_que_conta' in f['usou']: diz(S, f"  {f['nome']} ergue o escudo, mas ele já contou nesta luta"); return
    f['usou'].append('escudo_que_conta'); toca = []
    for o in de_pe(S, f['lado']):
        if dist(f, o) > TE.ESCUDO_CONTA['casas']: continue
        o['coragem_escudo'] = TE.ESCUDO_CONTA['coragem']
        if o.get('acuado'): o['acuado'] = False; toca.append(f"{o['nome']} sai do acuado")
        elif o['abalado']: o['abalado'] = False; toca.append(f"{o['nome']} se firma")
    _conta(S, 'escudo_que_conta')
    diz(S, f"  {f['nome']} ergue o escudo que conta: +{TE.ESCUDO_CONTA['coragem']} na coragem dos seus a {TE.ESCUDO_CONTA['casas']} casas" + (f" ({'; '.join(toca)})" if toca else ''))


def _fim(S):
    if S['fim']: return
    a, b = de_pe(S, 'A'), de_pe(S, 'B')
    if not a and not b: S['fim'] = 'ninguém'
    elif not a: S['fim'] = 'B'
    elif not b: S['fim'] = 'A'


def _abre_rodada(S):
    S['r'] += 1; S['dano_r'] = 0; S['houve_parada'] = False; diz(S, f"— RODADA {S['r']} —")
    if S['r'] == 1:                                         # o que APAVORA: quem começa a luta contra ele testa a coragem
        for lado in 'AB':
            ap = [b for b in de_pe(S, lado) if tem(b, 'apavora')]
            if ap:
                cd = max(b.get('pavor') or TB.PAVOR for b in ap)       # o pavor do dragão jovem é mais alto que o dos outros (tabelas_dragoes.PAVOR)
                for o in de_pe(S, outro(lado)): _moral(S, o, 'pavor', cd_pavor=cd)
        for d in de_pe(S):                                  # (fase 1b) o TEMÍVEL: quem começa a luta contra o dono testa a coragem (uma fonte nova de medo: testa no fim da rodada, junto das outras)
            tv = efeito(S, d, 'temivel')
            if tv:
                for o in inimigos(S, d): o['medo_fontes'][f"temivel:{d['nome']}"] = tv
    vivos = de_pe(S)
    for f in S['L']: f['golpeado'] = []
    for f in vivos: f['ini'] = sum(d20x()) + sum(d20x()) + f['percep_b'] + f['agil_b'] + f['ini_mod'] + (TB.BOTE['ini'] if S['r'] == 1 and tem(f, 'bote') else 0)
    S['fila'] = [f['nome'] for f in sorted(vivos, key=lambda f: -f['ini'])]


def _fecha_rodada(S):
    if S['fechada'] == S['r']: return
    S['fechada'] = S['r']
    for f in S['L']:                                        # o sangue e a vida por um fio
        if f['estado'] == 'pe' and f['sangra']:
            q = f['sangra'][0]; f['pv'] -= q; f['sangra'][1] -= 1; S['dano_r'] += q / f['pvmax']
            if f.get('funda') is None: f['funda'] = 0           # o sangue conta como ferida Comum
            if f['sangra'][1] <= 0: f['sangra'] = None
            qu = 'queima' if f.get('queimando') else 'sangra'
            if not f['sangra']: f.pop('queimando', None)
            diz(S, f"  {f['nome']} {qu} {q} ({max(f['pv'], 0)}/{f['pvmax']})")       # o que o sangue tira fica escrito: a conta dos golpes fecha com o quadro
            if f['pv'] <= 0 and not _salva(S, f): diz(S, f"  {f['nome']} {qu} até cair"); _cai(S, f, 0)
        elif f['estado'] == 'caido' and max(f['morte']) < 3:
            ok = D.d(20) >= T.MORTE_CD; f['morte'][0 if ok else 1] += 1
            if f['morte'][1] >= 3: f['estado'] = 'morto'; diz(S, f"  ☠ {f['nome']} morre no chão"); _para(S, f, f"{f['nome']} morreu no chão")
    for f in S['L']:                                        # (fase 1b) OS FILETES dos efeitos (a Sangria, a Brasa): cada um tira o seu tanto por rodada, pelo seu prazo; a água apaga o fogo
        if f['estado'] != 'pe' or not f['filetes']: continue
        if 'água' in S['tempo'] and any(x[2] == 'fogo' for x in f['filetes']): f['filetes'] = [x for x in f['filetes'] if x[2] != 'fogo']; diz(S, f"  a água apaga o fogo em {f['nome']}")
        if not f['filetes']: continue
        q = sum(x[0] for x in f['filetes']); fogo = all(x[2] == 'fogo' for x in f['filetes'])
        for x in f['filetes']: x[1] -= 1
        f['filetes'] = [x for x in f['filetes'] if x[1] > 0]; f['pv'] -= q; S['dano_r'] += q / f['pvmax']
        if f.get('funda') is None: f['funda'] = 0
        diz(S, f"  {f['nome']} {'queima' if fogo else 'sangra'} {q} pelos filetes ({max(f['pv'], 0)}/{f['pvmax']})"); _conta(S, 'filetes_pv', q)
        if f['pv'] <= 0 and not _salva(S, f): diz(S, f"  {f['nome']} {'queima' if fogo else 'sangra'} até cair"); _cai(S, f, 0)
    for f in S['L']:                                        # o veneno
        if f['estado'] == 'pe' and f.get('veneno'):
            q = f['veneno'][0]; f['pv'] -= q; f['veneno'][1] -= 1; S['dano_r'] += q / f['pvmax']
            if f.get('funda') is None: f['funda'] = 0           # o veneno também
            if f['veneno'][1] <= 0: f['veneno'] = None
            diz(S, f"  {f['nome']} perde {q} para o veneno ({max(f['pv'], 0)}/{f['pvmax']})")      # como o sangue: o que o veneno tira fica escrito
            if f['pv'] <= 0 and not _salva(S, f): diz(S, f"  {f['nome']} cai pelo veneno"); _cai(S, f, 0)
    for f in de_pe(S):                                      # (fase 1b) a REGENERA: do PV máximo por rodada, no teto da cura do dia
        rg = efeito(S, f, 'regenera')
        if rg and f['pv'] < f['pvmax']:
            teto = max(0, int(f['pvmax'] * T.CURA_TETO) - f.get('curado', 0)); g = min(f['pvmax'] - f['pv'], teto, max(1, int(f['pvmax'] * rg)))
            if g > 0: f['pv'] += g; f['curado'] = f.get('curado', 0) + g; S['dano_r'] -= g / f['pvmax']; diz(S, f"  {f['nome']} se refaz (a Regenera: +{g}: {f['pv']}/{f['pvmax']})"); _conta(S, 'regenera', g)
    if S.get('magia'): magia.fecha_rodada(S)                # a seiva, os prazos que contam em rodadas, o campo de quem caiu, a fase do chefe
    if S.get('hab'): habilidade.fecha_rodada(S)              # (fase 2) a Sanha sem sangue perde metade; a pilha da Mão que Estanca quebra
    for f in S['L']:                                        # (fase 1b) AS FONTES NOVAS DE MEDO testam juntas: um teste por alvo por rodada, contra a maior CD, +1 por fonte a mais (até +2)
        fs = f['medo_fontes']
        if not fs: continue
        f['medo_fontes'] = {}
        if f['estado'] != 'pe': continue
        cds = sorted(fs.values(), reverse=True); _moral(S, f, 'medo_peca', cd=cds[0] + min(TE.MEDO_MAIS_MAX, TE.MEDO_MAIS * (len(cds) - 1)))
    for f in de_pe(S):                                      # (fase 1b) o acuado desce a abalado depois de 2 rodadas sem susto novo
        if f.get('acuado') and S['r'] - f['susto_r'] >= TE.ACUADO_DESCE: f['acuado'] = False; diz(S, f"  {f['nome']} se recompõe um pouco: de acuado a abalado")
    for f in de_pe(S):                                      # a retirada: quem recua e ficou longe de todo inimigo de pé saiu da luta
        ini = inimigos(S, f)                                # SEM INIMIGO DE PÉ NÃO HÁ RETIRADA: a luta acabou, e quem recuava ficou com o campo como os outros
        if _ordem_de(S, f) == 'recuar' and ini and not S['fim'] and all(dist(f, e) >= (habilidade.retirada(S, f) if S.get('hab') else T.RETIRADA) for e in ini):
            f['estado'] = 'saiu'; diz(S, f"  {f['nome']} SAI DA LUTA"); _para(S, f, f"{f['nome']} saiu da luta")
    _fim(S)
    S['sem_dano'] = 0 if S['dano_r'] >= T.IMPASSE_MIN else S['sem_dano'] + 1
    if S['sem_dano'] >= T.IMPASSE and not S['fim']:
        S['fim'] = 'impasse'; diz(S, f"  IMPASSE: {T.IMPASSE} rodadas em que ninguém feriu ninguém de verdade. Os dois lados se separam.")
    S['sem_parada'] = 0 if S['houve_parada'] else S['sem_parada'] + 1
    if S['sem_parada'] >= 3 and not S['fim']: S['paradas'].append('três rodadas sem novidade'); S['sem_parada'] = 0


def passo(S):
    """o turno de UM lutador (abre a rodada se for o caso, e a fecha depois do último)"""
    if not S['fila']: _abre_rodada(S)
    f = por_nome(S, S['fila'].pop(0))
    if f['estado'] == 'pe' and not S['fim'] and not (S['r'] == 1 and S['surpresa'] == f['lado']):
        _turno(S, f)
        for c in S['L']:                                    # quem o jogador comanda passou de metade ou de um quarto do PV?
            if c.get('controla') and c['estado'] == 'pe':
                for lim in (0.5, 0.25):
                    if c['pv_visto'] >= c['pvmax'] * lim > c['pv']: _para(S, c, f"{c['nome']} está abaixo de {int(lim * 100)}% do PV")
                c['pv_visto'] = c['pv']
    if not S['fila'] or S['fim']: S['fila'] = []; _fecha_rodada(S)


def rodada(S):
    """uma rodada inteira, sem parar (o simulador e as provas usam)"""
    passo(S)
    while S['fila']: passo(S)


def _fecha_luta(S):
    """o fim: quem caiu do lado que ficou com o campo é estancado pelos seus; os outros rolam até o fim"""
    if S.get('luta_fechada'): return
    S['luta_fechada'] = True
    if S.get('magia'): magia.fecha_luta(S)
    for k in S['usadas']:                                   # o uso: toda peça que entrou na luta perde 1 (menos a que não quebra e a que já quebrou)
        it = S['itens'][k]
        if it['dur'][0] > 0 and not any(x.get('chave') == 'nao_quebra' for x in it.get('efeitos', [])): it['dur'][0] -= 1
    for f in S['L']:
        if f['estado'] == 'pe' and f.get('veneno'):         # o veneno que sobra corre depois da luta: deixa por um fio, mas sozinho não mata
            q = min(f['pv'] - 1, f['veneno'][0] * f['veneno'][1]); f['veneno'] = None
            if q > 0: f['pv'] -= q; diz(S, f"  {f['nome']} ainda perde {q} para o veneno depois da luta ({f['pv']}/{f['pvmax']})")
        if f['estado'] != 'caido': continue
        if f['lado'] == S['fim']: f['estavel'] = True; continue
        while max(f['morte']) < 3: f['morte'][0 if D.d(20) >= T.MORTE_CD else 1] += 1
        if f['morte'][1] >= 3: f['estado'] = 'morto'; diz(S, f"  ☠ {f['nome']} não resiste aos ferimentos")
        else: f['estavel'] = True


def corre(S, interativo=False, maximo=T.MAX_RODADAS):
    """roda até acabar. Com interativo, devolve 'parada' antes da 1ª rodada e sempre que houver o que perguntar; a ordem volta por ordem()."""
    if interativo and not S['comecou']: S['comecou'] = True; return 'parada'
    S['comecou'] = True; S['paradas'] = []
    while not S['fim']:
        if not S['fila'] and S['r'] >= maximo: break
        passo(S)
        if interativo and S['paradas'] and not S['fim']: return 'parada'
    if not S['fim']: S['fim'] = 'empate'
    _fecha_luta(S)
    return 'fim'


def resultado(S):
    q = lambda est: [f['nome'] for f in S['L'] if f['estado'] == est]
    return dict(vencedor=S['fim'], rodadas=S['r'], mortos=q('morto'), caidos=q('caido'), fugiram=q('fugiu'), sairam=q('saiu'), presos=q('rendido'),
                feridas={f['nome']: f['feridas'][f.get('feridas_antes', 0):] for f in S['L'] if f['feridas'][f.get('feridas_antes', 0):]},      # só as feridas abertas NESTA luta (a que a pessoa já trazia não é notícia do fim)
                quebradas=[it.get('nome', k) for k, it in S['itens'].items() if it['dur'][0] <= 0 and it.get('nome') != 'as mãos'])


def resultado_diz(S):
    """o fim da luta numa linha, para a mesa (o resultado() é o mesmo, em registro, para os scripts)"""
    R = resultado(S); quem = dict(A='a casa fica com o campo', B='o outro lado fica com o campo', impasse='impasse: os dois lados se separam', empate='empate: ninguém fica com o campo').get(R['vencedor'], str(R['vencedor']))
    L = [f"{quem}, em {R['rodadas']} rodada{'s' if R['rodadas'] != 1 else ''}"]
    for k, nome in (('mortos', 'morreram'), ('caidos', 'caíram'), ('fugiram', 'fugiram'), ('sairam', 'saíram da luta'), ('presos', 'renderam-se')):
        if R[k]: L.append(f"{nome}: {', '.join(R[k])}")
    if R['feridas']: L.append('feridas: ' + '; '.join(f"{n} ({' e '.join(_parte(por_nome(S, n) or {}, p) + (', grave' if g else '') for p, g in fs)})" for n, fs in R['feridas'].items()))
    if R['quebradas']: L.append('peças quebradas: ' + ', '.join(R['quebradas']))
    return ' · '.join(L)


def linha_1b(S, f):
    """(fase 1b) o que a base nova põe na linha do lutador no quadro: o acuado, a barra de carga de cada família (a mesa vê a do inimigo: "carga de cabeça 6/10"), o atordoado,
    a cabeça firme, o aberto, os filetes, o exposto, o amolecido e o Imortal já gasto. Quem não tem nada disso, nada (a linha de hoje sai igual)."""
    L_ = []
    if f.get('acuado'): L_.append('ACUADO (não avança)')
    for k in TE.FAMILIAS:
        if f['barra'][k]: L_.append(f"carga de {TE.FAMILIA_DIZ[k]} {f['barra'][k]}/{resistencia(S, f, k):g}".replace('.', ','))
    if f['perde_turno']: L_.append('ATORDOADO: perde o próximo turno')
    if f['firme_cabeca'] > 0 and S.get('carga_cabeca'): L_.append(f"cabeça firme ({f['firme_cabeca']} turno{'s' if f['firme_cabeca'] > 1 else ''})")
    if f['aberto'] >= S['r']: L_.append('aberto (−4 na Defesa)')
    if f['filetes']: L_.append(f"filetes ({len(f['filetes'])}: {sum(x[0] for x in f['filetes'])} por rodada)")
    if f['exposto'] >= S['r']: L_.append('exposto (+50% no dano que leva)')
    if f['amolecido'] >= S['r']: L_.append('amolecido (−25% no dano que faz)')
    if f['fx_usos'].get('imortal'): L_.append('o Imortal já segurou hoje')
    return ''.join(' · ' + x for x in L_)


def situacao(S):
    """o quadro que o jogador vê quando a luta para"""
    lado = dict(A='a casa', B='o outro lado'); lg = S['lugar'] or {}
    lugar = [x for x in ([f"corredor de {lg['largura']}" if lg.get('largura') else ''] + [f"{lado.get(lg[k], lg[k])} {txt}" for k, txt in (('alto', 'no alto'), ('cobertura', 'com cobertura'), ('sem_saida', 'sem saída')) if lg.get(k)]) if x]
    lugar += [f'{k}: {v}' for k, v in lg.items() if k not in ('largura', 'alto', 'cobertura', 'sem_saida')]
    L = [f"RODADA {S['r']} · " + ' · '.join(S['tempo'] or ['tempo limpo']) + (f" · lugar: {', '.join(lugar)}" if lugar else '')]
    for lado, nome in (('A', 'A CASA'), ('B', 'O OUTRO LADO')):
        L.append(nome + ':')
        for f in S['L']:
            if f['lado'] != lado: continue
            oa = _oa(f); est = dict(pe='no chão' if f['chao'] else 'de pé', caido='CAIU', morto='MORREU', fugiu='fugiu', rendido='rendeu-se', saiu='saiu')[f['estado']]
            fer = ', '.join(_parte(f, p) + (' (grave)' if g else '') for p, g in f['feridas'])
            L.append(f"  {f['nome']:<22} {est:<8} PV {max(f['pv'], 0):>4}/{f['pvmax']:<4} fôlego {max(f['fol'], 0):>2}/{f['folmax']:<2} casa {f['x']:>3}"
                     + (f" · feridas: {fer}" if fer else '') + (f" · sangrando ({f['sangra'][0]} por rodada)" if f['sangra'] and f['estado'] == 'pe' else '')
                     + (' · fraquejou' if f['abalado'] else '') + (' · no chão' if f['chao'] and f['estado'] != 'pe' else '') + (' · sem a arma' if f['sem_arma'] else '') + (' · perna presa: não sai do lugar' if f['preso'] and f['estado'] == 'pe' else '')
                     + (f" · com veneno ({f['veneno'][0]} por rodada)" if f.get('veneno') and f['estado'] == 'pe' else '') + (f" · {f['agarrado']} não solta" if f['estado'] == 'pe' and _agarrado(S, f) else '')
                     + (f" · bicho {f['tamanho']}" + (', no ar' if f['estado'] == 'pe' and _no_ar(S, f) else '') + (', encurralad' + oa.lower() if f.get('encurralado') else '') if f.get('bicho') else '')
                     + (linha_1b(S, f) if f['estado'] == 'pe' else '') + (magia.linha(S, f) if S.get('magia') else '') + (habilidade.linha(S, f) if S.get('hab') else ''))
    if S.get('magia') and magia.campo(S): L.append(magia.campo(S))
    if S['r'] == 0 and S['avisos']: L.append('AVISOS: ' + ' · '.join(S['avisos']))
    if S['paradas']: L.append('PAROU PORQUE: ' + ' · '.join(S['paradas']))
    return '\n'.join(L)


# ---------- o simulador (o banco de provas usa) ----------
def duelos(faz_a, faz_b, n=1000, **kw):
    """n lutas entre os lados que faz_a() e faz_b() montam. Devolve (% de vitória de A, mediana de rodadas)."""
    va = 0; rs = []
    for _ in range(n):
        S = nova(faz_a(), faz_b(), quieto=True, **kw); corre(S)
        va += 1 if S['fim'] == 'A' else 0 if S['fim'] == 'B' else 0.5; rs.append(S['r'])
    rs.sort()
    return round(100 * va / n), rs[len(rs) // 2]


# ---------- a luta de verdade: o cenário, o arquivo da luta e as ordens ----------
def cenario(arq):
    """monta a luta de um arquivo de cenário: {"inicio","lugar","tempo","surpresa","A":[pessoa...],"B":[pessoa...]}
    pessoa = {"nome","nivel", "molde"?, "maestria"?, "atributos"?, "controla"?, "lider"?, "guarda"?, "moral"?, "linha"?, "feiticos"?, "tradicao"?, "tracos"?, "fases"?, "carga"?,
              "veste": {"arma", "arma2", "armadura", "elmo", "escudo", "pecas": [...], "foco", "amuleto"}}
    bicho  = {"bicho": "lobo", "nome"?: "lobo 1", "lider"?, "linha"?}     (a espécie inteira sai do tabelas_bichos.py; ou a pessoa que o bichos.bicho devolve)
    cada peça é o id de um item do Livro de Itens, ou o atalho ["espada","Raro"] (armadura: ["malha","Raro"] veste corpo e elmo; escudo: "Raro")."""
    from pessoas import padrao, veste
    from itens import carrega, cat_i
    C = json.load(open(arq, encoding='utf-8')); B = carrega()['itens']
    def peca(x, tipo):
        if x is None or x is False: return x
        if isinstance(x, str) and x in B: return B[x]
        if isinstance(x, str) and tipo != 'escudo': sys.exit(f'não há o item "{x}" no Livro de Itens (itens.py ver)')
        return cat_i(x) if tipo == 'escudo' else (x[0], cat_i(x[1]))
    def pessoa(d):
        d = dict(d)
        if isinstance(d.get('bicho'), str):
            import bichos
            esp = d.pop('bicho'); d.pop('nivel', None); return bichos.bicho(esp, **d)
        v = d.pop('veste', {})
        ruins = [k for k in v if k not in ('arma', 'arma2', 'armadura', 'elmo', 'escudo', 'pecas', 'foco', 'amuleto')]
        if ruins: sys.exit(f'{d.get("nome")}: não sei vestir "{ruins[0]}" (use: arma, arma2, armadura, elmo, escudo, pecas, foco, amuleto)')
        p = padrao(d.pop('nome'), d.pop('nivel'), molde=d.pop('molde', 'guerreiro'), maestria=d.pop('maestria', None), atributos=d.pop('atributos', None), **d)
        return veste(p, arma=peca(v.get('arma'), 'arma'), arma2=peca(v.get('arma2'), 'arma'), armadura=peca(v.get('armadura'), 'armadura'), elmo=peca(v.get('elmo'), 'armadura'),
                     escudo=peca(v.get('escudo'), 'escudo'), pecas=[peca(x, 'armadura') for x in v.get('pecas', [])],
                     foco=peca(v.get('foco'), 'foco'), amuleto=peca(v.get('amuleto'), 'escudo'))      # o foco: ["cajado", "Raro"] ou o id; o amuleto: "Raro" ou o id
    return nova([pessoa(x) for x in C['A']], [pessoa(x) for x in C['B']], inicio=C.get('inicio', 'perto'), lugar=C.get('lugar'), tempo=C.get('tempo'), surpresa=C.get('surpresa'))


def salva(S, arq):
    """guarda a luta no arquivo e devolve ao Livro de Itens a durabilidade gasta até aqui"""
    json.dump(S, open(arq, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    if S.get('mundo'): return                               # luta do mundo: a durabilidade volta por evento, no ato.py (o gravador é um só)
    from itens import carrega, grava
    B = carrega(); mudou = False
    for it in S['itens'].values():
        if it.get('id') in B['itens'] and B['itens'][it['id']]['dur'] != it['dur']: B['itens'][it['id']]['dur'] = it['dur']; mudou = True
    if mudou: grava(B)


def ordem(S, txt):
    """'Nome: atacar [alvo] [postura]' · ação: atacar, segurar, avancar, recuar, folego, guardar NOME · lancar FEITICO [em ALVO | casa N] [sempre] [osso]
    · beber POCAO [em ALIADO] · usar [PECA] [em ALVO | casa N] · 'grupo: atacar|segurar|recuar'.
    Só o lado A recebe ordem. Nome que não existe é recusado, com a lista de quem está de pé."""
    quem, _, resto = txt.partition(':'); quem = quem.strip(); pal = resto.split()
    if not pal: sys.exit(f'ordem vazia: "{txt}"')
    if quem.lower() == 'grupo':
        if len(pal) != 1 or pal[0] not in ('atacar', 'segurar', 'recuar'): sys.exit(f'a ordem do grupo é uma palavra só: atacar, segurar ou recuar (veio "{resto.strip()}")')
        S['ordens']['grupo'] = pal[0]; return
    acha = lambda nome, gente: next((x for x in gente if x['nome'].lower() == nome.lower()), None)
    meus, deles = de_pe(S, 'A'), de_pe(S, 'B')
    f = acha(quem, meus)
    if not f: sys.exit(f'não há "{quem}" de pé do seu lado. De pé: {", ".join(x["nome"] for x in meus)}')
    palavras = pal[0] == 'fazer' or bool(re.search(r'\btrunfo\s*=', resto)) or bool(re.search(r'\b(sem|com) (riposta|voto)\b', resto)) or pal[-1] == 'bigorna'
    sanha = S.get('hab') and f.get('hab') and (f.get('acesa') == 'sanha' or f.get('sanha_arma'))
    if palavras or (sanha and (pal[0] in ('recuar', 'guardar', 'lancar') or pal[-1] in ('defensiva', 'bigorna'))):      # (fase 2) as palavras das habilidades (e a ordem que apaga a Sanha, ou que ela recusa)
        if not S.get('hab') or not f.get('hab'): sys.exit(f'{f["nome"]} não tem habilidade de luta')
        f['controla'] = True; resto2 = habilidade.ordem(S, f, resto.strip())
        if resto2 is None: return
        pal = resto2.split()
        if not pal: return
    post = pal.pop() if pal[-1] in T.POSTURAS or (pal[-1] == 'bigorna' and S.get('hab') and habilidade.tem(f, 'bigorna')) else None
    if not pal: pal = ['atacar']
    acao = pal[0]; resto = ' '.join(pal[1:]) or None
    if acao in ('lancar', 'beber', 'usar'):                 # A MAGIA: a ordem é conferida inteira aqui (o feitiço que a pessoa sabe, o alvo, a poção que leva, o encanto carregado)
        if not S.get('magia'): sys.exit(f'{f["nome"]} não tem magia nesta luta: nem feitiço, nem poção, nem encanto')
        o = magia.ordem(S, f, acao, pal[1:]); o.update({'postura': post} if post else {})
        f['controla'] = True; f['acuado'] = False; S['ordens'][f['nome']] = o; return
    if acao in ('atar', 'animar'):                           # (fase 1b) atar [ALIADO]: corta o filete mais forte, em si ou num aliado colado · animar: o Escudo que Conta
        if acao == 'animar' and (not efeito(S, f, 'escudo_que_conta') or 'escudo_que_conta' in f['usou']): sys.exit(f'{f["nome"]} não tem o Escudo que Conta pronto (o escudo com ele, inteiro, uma vez por luta)')
        alvo = None
        if acao == 'atar' and resto:
            caidos = habilidade.caidos_ataveis(S, f) if S.get('hab') and f.get('hab') else []      # (fase 2) a Mão que Estanca do Mestre: o caído colado (firmar; no Grão-Mestre, levantar)
            g = acha(resto, meus) or acha(resto, caidos)
            if not g or dist(f, g) > 1: sys.exit(f'atar quem? Em si, ou num aliado colado: {", ".join(x["nome"] for x in meus + caidos if dist(f, x) <= 1)}')
            alvo = g['nome']
        elif acao == 'animar' and resto: sys.exit('"animar" não leva nome (o escudo conta para os seus a 2 casas)')
        antes = S['ordens'].get(f['nome']); antes = antes.get('antes') if antes and antes.get('acao') in ('atar', 'animar') else antes
        f['controla'] = True; f['acuado'] = False; S['ordens'][f['nome']] = dict(acao=acao, alvo=alvo, antes=antes, **({'postura': post} if post else {})); return
    if acao not in ('atacar', 'segurar', 'avancar', 'recuar', 'folego', 'guardar'): sys.exit(f'ação desconhecida: "{acao}" (use: atacar, segurar, avancar, recuar, folego, guardar, atar, animar, lancar, beber, usar)')
    alvo = None
    if acao == 'guardar':
        g = acha(resto or '', [x for x in meus if x is not f])
        if not g: sys.exit(f'guardar quem? Do seu lado, de pé: {", ".join(x["nome"] for x in meus if x is not f)}')
        f['guarda'] = g['nome']
    elif resto:
        if acao != 'atacar': sys.exit(f'"{acao}" não leva nome (veio "{resto}")')
        e = acha(resto, deles)
        if not e: sys.exit(f'não há "{resto}" de pé do outro lado. De pé: {", ".join(x["nome"] for x in deles)}')
        alvo = e['nome']
    if acao in ('atacar', 'avancar'): f['guarda'] = None
    f['controla'] = True; f['acuado'] = False                 # (fase 1b) quem o jogador passa a comandar para no abalado (a escada: o acuado é de quem ele não comanda)
    S['ordens'][f['nome']] = dict(acao='atacar' if acao in ('avancar', 'guardar') else acao, alvo=alvo, **({'postura': post} if post else {}))


def _demo():
    from pessoas import padrao, veste
    from itens import item
    semente(7)
    rei = veste(padrao('o ferreiro', 40, controla=True, linha='trás'), arma=('lança', 3), armadura=('couro', 2))
    a = [veste(padrao('Moreth', 120, moral='firme', lider=True), arma=item('arma', 4, 'a Maça do Rio', familia='maça', efeitos=[dict(chave='derruba')]), armadura=('malha', 4), escudo=3),
         veste(padrao('Gonde', 32, guarda='o ferreiro', moral='firme'), arma=('espada', 2), armadura=('malha', 2), escudo=2), rei]
    b = [veste(padrao('Nutoccone', 90, lider=True), arma=('espada', 3), armadura=('malha', 2), escudo=2)] + \
        [veste(padrao(f'herdeiro {i}', 30 + 5 * i), arma=('lança' if i % 2 else 'machado', 1), armadura=('couro', 1)) for i in range(1, 7)]
    S = nova(a, b, inicio='perto', lugar=dict(largura=2, sem_saida='B'), tempo=['escuro'])
    ordem(S, 'o ferreiro: segurar defensiva')
    while corre(S, interativo=True) == 'parada':
        print('\n'.join(S['log'])); S['log'] = []; print(); print(situacao(S)); print()
        if any('abaixo de 50%' in p for p in S['paradas']): ordem(S, 'o ferreiro: recuar defensiva'); print('>>> ordem: o ferreiro recua\n')
    print('\n'.join(S['log'])); print(); print(situacao(S)); print(); print('FIM:', resultado_diz(S))


if __name__ == '__main__':
    import signal; hasattr(signal, 'SIGPIPE') and signal.signal(signal.SIGPIPE, signal.SIG_DFL)      # a saída cortada (`| head`) acaba o comando calada, sem erro de programa: tudo já foi gravado antes de falar
    a = sys.argv[1:]
    if a[:1] == ['demo']: _demo()
    elif a[:1] == ['nova'] and len(a) >= 3:
        try: S = cenario(a[1])
        except OSError: sys.exit(f'não há o cenário "{a[1]}"')
        except (ValueError, KeyError, TypeError) as x: sys.exit(f'o cenário "{a[1]}" não se lê ({type(x).__name__}: {x}). Veja o exemplo: dados/cenario_exemplo.json')
        S['comecou'] = True; salva(S, a[2]); print(situacao(S))
        print(f'\nA luta está em {a[2]}. As ordens: python3 luta.py roda {a[2]} "Nome: atacar Alvo agressiva" "grupo: segurar"')
    elif a[:1] == ['roda'] and len(a) >= 2:
        try: S = json.load(open(a[1], encoding='utf-8'))
        except (OSError, ValueError): sys.exit(f'não há a luta "{a[1]}" (ou o arquivo não se lê). Uma luta nova: python3 luta.py nova CENARIO.json {a[1]}')
        if S['fim']: sys.exit('esta luta já acabou.')
        for o in a[2:]: ordem(S, o)
        S['log'] = []; fim = corre(S, interativo=True)
        salva(S, a[1])                                      # grava ANTES de falar: a saída cortada não perde o que o dado rolou
        print('\n'.join(S['log'])); print(); print(situacao(S))
        if fim == 'fim': print(); print('FIM:', resultado_diz(S))
    elif a[:1] in (['nova'], ['roda']): sys.exit('diga os arquivos: `python3 luta.py nova CENARIO.json LUTA.json` · `python3 luta.py roda LUTA.json "Nome: atacar"`')
    else: print(__doc__)
