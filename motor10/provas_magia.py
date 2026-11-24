#!/usr/bin/env python3
"""provas_magia.py — MOTOR 10: O BANCO DE PROVAS DO MUNDO DA MAGIA (etapa da magia, frente do mundo: a alquimia, o encanto, a maldição, o estudo, as tradições, os serviços).

O provas_mundo.py chama este banco (provas(n)); sozinho: `python3 provas_magia.py [N]`. As provas rodam em pastas de rascunho (nunca num save de verdade).
As metas de dinheiro usam a MESMA FAIXA do ferreiro de loja (provas_mercado: dada de fora, não se mexe): nada novo cria prata, e toda renda nova tem meta aqui.
"""
import contextlib, io, json, math, os, random, shutil, sys, tempfile
import tabelas as T
import tabelas_mundo as M
import tabelas_mercado as C
import tabelas_oficio as O
import tabelas_magia_mundo as W
import estado, ato, teste, talento, mercado, oficio, corpo, turno
import alquimia, encanto, maldicao, magia_mundo as MM
import provas_mundo as PM
import provas_mercado as PMk
from itens import item

MINA_DIAS, MINA_COMECO, MINA_DEPOIS, MINA_SEMENTES = PMk.MINA_DIAS, PMk.MINA_COMECO, PMk.MINA_DEPOIS, PMk.MINA_SEMENTES      # a faixa do ferreiro de loja (não se mexe)
MEUS = ('magia_mundo', 'alquimia', 'encanto', 'maldicao')


# ---------- montar ----------
def vila(semente=1, botica=1, santuario=1, runas=1, prata=30, caixa=None):
    """a vila de prova do mercado (400 de povo, o estoque no alvo, a prateleira), com a botica, o santuário e a mesa de runas, e a magia no mercado aberta"""
    E = PMk.vila(semente, prata=prata, caixa=caixa)
    ef = [['lugar', 'vila', k, 'poe', v] for k, v in (('botica', botica), ('santuario', santuario), ('runas', runas)) if v is not None]
    if ef: estado.aplica(E, 'gera', ef, onde='vila', texto='a magia da vila de prova')
    mercado.funda_magia(E, 'vila'); E['_novos'].clear()
    return E


def gente(E, pid, nome, at=None, nivel=10, lugar='vila', **mais):
    """o gerador põe alguém no mundo, por evento "gera" (os campos da magia entram ao nascer)"""
    r = dict(nome=nome, nivel=nivel, atributos=dict(at or dict(Força=50, Agilidade=50, Vigor=60, Vontade=50, Percepção=50, Afinidade=60)), lugar=lugar, moedas=mais.pop('moedas', 50), grau_oficio=mais.pop('grau', 'oficial'))
    r.update(mais); estado.aplica(E, 'gera', [['pessoa', 'nasce', pid, r]], onde=lugar, quem=[pid], texto=f'{nome} nasce para a prova')
    return pid


def da(E, pid='eu', prata=0, **carga):
    ef = [['pessoa', pid, 'carga.' + k.replace('_', ':').replace('agua:benta', 'água benta'), 'soma', n] for k, n in carga.items()] + ([['pessoa', pid, 'moedas', 'soma', prata]] if prata else [])
    estado.aplica(E, 'gera', ef, texto='os bens de prova')


def veste(E, pid, *its):
    s0 = E['itens']['seq']; estado.aplica(E, 'gera', [['item', 'nasce', dict(it, dono=pid)] for it, _ in its], texto='as peças de prova')
    ids = [f'i{s0 + k + 1:04d}' for k in range(len(its))]
    usos = [['item', i, 'uso', 'poe', u] for i, (_, u) in zip(ids, its) if u]
    if usos: estado.aplica(E, 'gera', usos, texto='veste')
    return ids


def recusa(f): return PM.recusa(f)
def retrato(E): return json.dumps({k: E[k] for k in estado.ARQS}, sort_keys=True, ensure_ascii=False)
def prata(E): return mercado.prata_do_mundo(E)
def pc(x, casas=0): return f'{100 * x:.{casas}f}%'.replace('.', ',')
def vz(x, casas=2): return f'{x:.{casas}f}'.replace('.', ',').replace('-', '−')
def mais(x, casas=2): return ('+' if x > 0 else '') + vz(x, casas)


@contextlib.contextmanager
def dado_posto(margens):
    """o dado de verdade é rolado, mas o total é posto à mão (contra + margem): para conferir cada saída"""
    real = teste.rola; fila = list(margens)
    def posto(E, o_que, atributo, contra, mais=0, quem=None, oculto=False, dom=0, **kw):
        r = real(E, o_que, atributo, contra, mais=mais, quem=quem, oculto=oculto, dom=dom, **kw); m = fila.pop(0); r['total'] = contra + m; r['passou'] = m >= 0
        if dom: r['fez'] = r['total'] >= contra and r['total'] - dom < contra
        return r
    teste.rola = posto
    try: yield
    finally: teste.rola = real


@contextlib.contextmanager
def pasta():
    d = tempfile.mkdtemp(prefix='m10_mag_'); antes = os.environ.get('MOTOR10_MUNDO'); os.environ['MOTOR10_MUNDO'] = d
    try: yield d
    finally:
        if antes is None: os.environ.pop('MOTOR10_MUNDO', None)
        else: os.environ['MOTOR10_MUNDO'] = antes
        shutil.rmtree(d, ignore_errors=True)


def termina(E, pid, R):
    """leva até o fim a obra que a primeira chamada abriu (a obra longa para quando o corpo pede: aqui o corpo de cada bloco volta ao zero, que a prova é da bancada)"""
    while not R.get('fim') and oficio.obras_de(E, pid):
        E['gente'][pid]['corpo'].update(fome=0, sono=0, cansaco=0); R = oficio.continua(E, pid, next(iter(oficio.obras_de(E, pid))))
    return R


def materia(E): return sum(q for k, q in oficio.materia_do_mundo(E).items() if M.le_materia(k)[0] in M.MATERIAS)      # a matéria do mundo (sem as poções, que também têm categoria)


# ---------- 1. a pessoa comum ----------
def _comum(n):
    """MG1 A PESSOA COMUM NÃO MUDA: dez dias de rotina numa vila de prova, com os módulos do mundo da magia ligados e desligados, dão o mesmo mundo (o estado e os eventos)"""
    def roda(com):
        estado.modulos(); guarda = estado._MODS
        if not com: estado._MODS = [m for m in guarda if m.__name__ not in MEUS]
        try:
            E = PM.vila(); E['relogio']['bloco'] = 0; E['turno']['aberto']['bloco'] = 0; evs = []
            for _ in range(10): PM.dia_de_rotina(E); evs += [(e['tipo'], e['efeitos']) for e in E['_novos']]; E['_novos'].clear()
            return retrato(E), json.dumps(evs, ensure_ascii=False)
        finally: estado._MODS = guarda
    a, b = roda(True), roda(False)
    return ('MG1 A PESSOA COMUM NÃO MUDA: dez dias de rotina (dormir, comer, trabalhar) dão o mesmo mundo com os módulos da magia ligados e desligados (o estado e cada evento)',
            f"o estado: {'igual' if a[0] == b[0] else 'DIFERENTE'}; os eventos: {'iguais' if a[1] == b[1] else 'DIFERENTES'} ({len(json.loads(a[1]))} eventos)", a == b)


# ---------- 2. estudar ----------
def _estudo(n):
    """MG2 ESTUDAR: o feitiço de grau 1 pede 6 blocos ao Comum e 3 ao Prodígio; o mestre ensina só dentro da jornada dele e cobra o salário; o escrito ensina de graça;
    sem fonte, de outra tradição ou da fé sem voto, recusa; os blocos viram treino da tradição; a prata fecha"""
    E = vila(prata=200); gente(E, 'anselmo', 'Anselmo', feiticos=['seta', 'luz', 'prender'], tradicao='arcano', maestria={'arcano': 4}, treino={'arcano': 160}, moedas=10)
    descansa = lambda: [E['gente'][q]['corpo'].update(fome=0, sono=0, cansaco=0) for q in ('eu', 'anselmo')]      # o corpo de cada dia volta ao zero (a prova é do estudo, não do sono)
    E['relogio']['bloco'] = 2; p0 = prata(E); R = MM.estudar(E, 'eu', 'seta', {'com': 'anselmo'}); dia1 = (R['feitos'], E['gente']['eu']['moedas'], E['gente']['anselmo']['moedas'])
    ato.passa(E, 'eu', 4, 'esperar', para=False); descansa()
    R2 = MM.estudar(E, 'eu', 'seta', {'com': 'anselmo'}); ato.passa(E, 'eu', 4, 'esperar', para=False); descansa()
    R3 = MM.estudar(E, 'eu', 'seta', {'com': 'anselmo'}); p = E['gente']['eu']
    sabe = 'seta' in (p.get('feiticos') or []); tr = (p.get('treino') or {}).get('arcano', 0); tradicao = p.get('tradicao')
    # o prodígio, por um escrito (sem custo): metade dos blocos
    F = vila(prata=50); estado.aplica(F, 'mestre', [['pessoa', 'eu', 'talento', 'poe', {'arcano': 2}]], texto='prodígio'); esc = veste(F, 'eu', (item('escrito', 0, 'Cartilha', feiticos=['seta', 'luz']), None))[0]
    m0 = F['gente']['eu']['moedas']; RP = MM.estudar(F, 'eu', 'seta', {'escrito': esc}); pr = (RP['feitos'], RP['aprendeu'], F['gente']['eu']['moedas'] == m0)
    G = vila(); recs = [recusa(lambda: MM.estudar(G, 'eu', 'seta', None)), recusa(lambda: MM.estudar(G, 'eu', 'cura', 'santuario')),
                        recusa(lambda: MM.estudar(G, 'eu', 'raízes', 'ermo')), recusa(lambda: MM.estudar(E, 'eu', 'cura', 'santuario'))]       # sem fonte; a fé sem voto; o verde sem laço; o mago na fé
    certo = dia1[0] == 2 and R2['feitos'] == 2 and sabe and R3['aprendeu'] and tr == 6 and tradicao == 'arcano' and pr == (3, True, True) and all(recs) and prata(E) == p0 and not estado.valida(E)
    return ('MG2 ESTUDAR: o feitiço de grau 1 pede 6 blocos (o Prodígio, 3); quem ensina só ensina dentro da jornada dele (2 blocos pagos por dia) e cobra o salário por bloco; '
            'o escrito ensina de graça; sem fonte, a fé sem voto, o verde sem laço e a tradição alheia recusam; os blocos viram treino da tradição; a prata fecha',
            f"com o mestre: {dia1[0]} blocos no primeiro dia (pagou {200 - dia1[1]} de prata), {R2['feitos']} no segundo, aprendeu no terceiro: {'sim' if sabe else 'NÃO'}; treino do arcano {tr}; "
            f"a tradição: {tradicao}; o Prodígio pelo escrito: {pr[0]} blocos, aprendeu: {'sim' if pr[1] else 'NÃO'}, de graça: {'sim' if pr[2] else 'NÃO'}; "
            f"recusas: {sum(1 for x in recs if x)} de {len(recs)}; prata {'fecha' if prata(E) == p0 else 'NÃO FECHA'}", certo)


# ---------- 3. a Mana fora da luta ----------
def _mana(n):
    """MG3 A MANA FORA DA LUTA, por bloco: dormindo um quarto da máxima, descansando um oitavo, leve 1, pesado nada; o clérigo só pela prece (no santuário enche,
    fora metade); o druida em dobro no ermo; a bruxa sozinha só até a metade, e paga o resto; a maldição do passo 4 trava"""
    E = vila(); at = dict(Força=40, Agilidade=50, Vigor=60, Vontade=60, Percepção=60, Afinidade=60)
    gente(E, 'mago', 'Mago', at, tradicao='arcano', maestria={'arcano': 4}, feiticos=['seta'], mana=0)
    gente(E, 'clerigo', 'Clérigo', at, tradicao='fé', maestria={'fé': 4}, feiticos=['cura'], voto=dict(qual='socorro', santuario='vila', dia=1), mana=0)
    gente(E, 'bruxa', 'Bruxa', at, tradicao='pacto', maestria={'pacto': 4}, feiticos=['ler'], mana=0)
    mx = estado.mana_max(E['gente']['mago'])
    def um(pid, esforco, dorme=None):
        ef = MM.bloco(E, pid, esforco, dorme); return next((x[4] for x in ef if x[2] == 'mana'), 0)
    v = dict(dorme=um('mago', 'nada', 'cama'), descanso=um('mago', 'descanso'), leve=um('mago', 'leve'), pesado=um('mago', 'pesado'), clerigo=um('clerigo', 'nada', 'cama'))
    E['gente']['bruxa']['mana'] = int(mx * W.PACTO_SOZINHA) - 1; v['bruxa_meio'] = um('bruxa', 'nada', 'cama'); E['gente']['bruxa']['mana'] = int(mx * W.PACTO_SOZINHA); v['bruxa_cheia'] = um('bruxa', 'nada', 'cama')
    estado.aplica(E, 'mestre', [['maldicao', 'mago', 'poe', maldicao.registro(dict(nome='x', cat=0, tipo='míngua', condicao=dict(tipo='cumprir')), 'feitiço', passo=4)]], texto='a maldição de prova')
    v['passo4'] = um('mago', 'nada', 'cama')
    t0 = estado.agora(E); E['relogio']['bloco'] = 2
    pr = MM.prece(E, 'clerigo'); cheia = estado.mana(E['gente']['clerigo']) == estado.mana_max(E['gente']['clerigo'])
    r2 = recusa(lambda: MM.prece(E, 'clerigo'))
    F = vila(santuario=None); gente(F, 'c2', 'Clériga', at, tradicao='fé', maestria={'fé': 4}, feiticos=['cura'], voto=dict(qual='socorro', santuario='vila', dia=1), mana=0)
    MM.prece(F, 'c2'); meio = estado.mana(F['gente']['c2']); mx2 = estado.mana_max(F['gente']['c2'])
    pg = MM.paga(E, 'bruxa', 4, 'divida'); dv = E['gente']['bruxa'].get('divida')
    # o druida no ermo: em dobro
    D = vila(); D['lugares']['mata'] = dict(nome='a Mata', em='na Mata', tipo='ermo', estoque={}, vizinhos=['vila']); D['lugares']['vila']['vizinhos'] = ['mata']
    gente(D, 'dru', 'Druida', at, tradicao='verde', maestria={'verde': 4}, feiticos=['raízes'], laco=dict(ermo='mata', dia=1), mana=0, lugar='mata')
    druida = next((x[4] for x in MM.bloco(D, 'dru', 'leve', None) if x[2] == 'mana'), 0)
    casa = _casa(at)
    certo = (v['dorme'] == round(mx / 4) and v['descanso'] == max(1, math.floor(mx / 8 + 0.5)) and v['leve'] == 1 and v['pesado'] == 0 and v['clerigo'] == 0 and v['bruxa_meio'] == 1 and v['bruxa_cheia'] == 0
             and v['passo4'] == 0 and cheia and r2 and meio == int(mx2 * W.PRECE_FORA) and dv == 1 and druida == 2 and casa['certo'])
    return ('MG3 A MANA FORA DA LUTA: por bloco, dormindo um quarto da máxima, descansando um oitavo, leve 1, pesado nada; o clérigo só pela prece (uma por dia: no santuário enche, '
            'fora dele metade); o druida em dobro no ermo; a bruxa sozinha só até a metade (o resto, pago: 4 de Mana por 1 de dívida); a maldição do passo 4 trava; e QUEM VOLTA À CENA '
            f'(quem não é o personagem, um dia em casa) recobra a Mana pela mesma regra ({W.CASA_SONO} blocos dormidos e o resto parado; o clérigo, a prece do dia em casa), uma vez só',
            f"o mago de Mana máxima {mx}: dormindo {v['dorme']}, descansando {v['descanso']}, leve {v['leve']}, pesado {v['pesado']}; o clérigo pelo bloco {v['clerigo']}, a prece no santuário "
            f"{'enche' if cheia else 'NÃO ENCHE'}, a segunda prece {'recusada' if r2 else 'ACEITA'}, longe dele {meio} de {mx2}; a bruxa abaixo da metade {v['bruxa_meio']}, na metade {v['bruxa_cheia']}, "
            f"pagando 4 de Mana a dívida vai a {dv}; o druida no ermo, leve: {druida}; com a maldição no passo 4: {v['passo4']}; " + casa['diz'], certo)


def _casa(at):
    """quem não é o personagem volta à cena depois de um dia em casa (9 blocos fora de cena: uma noite contada), de Mana 0: o mago, a clériga (com santuário e sem), a bruxa;
    a pessoa comum não ganha Mana; gastar a Mana é estar em cena (a mesma noite não enche duas vezes)"""
    mg = dict(mago=dict(tradicao='arcano', maestria={'arcano': 4}, feiticos=['seta']), clerigo=dict(tradicao='fé', maestria={'fé': 4}, feiticos=['cura'], voto=dict(qual='socorro', santuario='vila', dia=1)),
              bruxa=dict(tradicao='pacto', maestria={'pacto': 4}, feiticos=['ler']))
    H = vila(); F = vila(santuario=None); v = {}
    for E, quem in ((H, ('mago', 'clerigo', 'bruxa', 'comum')), (F, ('clerigo',))):
        for k in quem: gente(E, k, k.capitalize(), at, **(dict(mg[k], mana=0) if k in mg else {}))
        estado.aplica(E, 'mestre', [['pessoa', k, 'marca.cena', 'poe', estado.agora(E)] for k in quem], texto='em cena agora'); E['relogio']['dia'] += 1; E['relogio']['bloco'] += 3
        for k in quem:
            ev = estado.em_cena(E, k); v[(E is F, k)] = (estado.mana(E['gente'][k]), estado.mana_max(E['gente'][k]), any(x[2] == 'mana' for x in (ev or {}).get('efeitos', [])))
    mx = v[(False, 'mago')][1]; q = max(1, math.floor(mx * W.MANA_DORME + 0.5)); quer = min(mx, W.CASA_SONO * q + (M.CASA_NOITE - W.CASA_SONO) * W.MANA_ACORDADO[W.CASA_ESFORCO])
    estado.aplica(H, 'lancar', [['pessoa', 'mago', 'mana', 'soma', -2]], quem=['mago'], texto='o mago gasta 2 de Mana'); de_novo = estado.em_cena(H, 'mago'); depois = estado.mana(H['gente']['mago'])
    certo = (v[(False, 'mago')][0] == quer and v[(False, 'clerigo')][0] == v[(False, 'clerigo')][1] and v[(True, 'clerigo')][0] == int(v[(True, 'clerigo')][1] * W.PRECE_FORA)
             and v[(False, 'bruxa')][0] == int(v[(False, 'bruxa')][1] * W.PACTO_SOZINHA) and not v[(False, 'comum')][2] and H['gente']['comum'].get('mana') is None and de_novo is None and depois == quer - 2)
    diz = (f"quem volta à cena depois de um dia em casa, de Mana 0: o mago {v[(False, 'mago')][0]} de {mx} (a regra dá {quer}), a clériga com santuário {v[(False, 'clerigo')][0]} de {v[(False, 'clerigo')][1]}, "
           f"sem santuário {v[(True, 'clerigo')][0]} de {v[(True, 'clerigo')][1]}, a bruxa {v[(False, 'bruxa')][0]} de {v[(False, 'bruxa')][1]}; a pessoa comum {'sem Mana' if not v[(False, 'comum')][2] else 'GANHOU MANA'}; "
           f"o mago gasta 2 e volta à cena: {depois} ({'a noite não conta de novo' if de_novo is None and depois == quer - 2 else 'ENCHEU DE NOVO' if depois > quer - 2 else 'ERRADO: a regra dá ' + str(quer - 2)})")
    return dict(certo=certo, diz=diz)


# ---------- 4. a maldição mata na faixa ----------
def _vidas(n, cat, at, pecas, semente0=0, maestria=None):
    """n vidas de uma pessoa amaldiçoada no Dia 1, ninguém fazendo nada: em que dia (contado do Dia 1) a maldição a mata; o relógio da virada é o de verdade (maldicao.virada).
    Devolve (os dias, em ordem; a Firmeza dela pela conta de verdade, maldicao.firmeza, a que o relógio usa)"""
    dias = []; fir = None
    for s in range(n):
        E = estado.novo(semente0 * 100000 + s + 1); E['lugares']['vila'] = dict(nome='a Vila', em='na Vila', tipo='vila', estoque={})
        E['gente']['x'] = dict(nome='X', lugar='vila', grau_oficio='diarista', nivel=50, atributos=dict(at), maestria=dict(maestria or {}), treino={}, moedas=0, corpo=dict(fome=0, sono=0, cansaco=0),
                               pv=T.pv_max(at['Vigor'], 50), feridas=[], estado='vivo', marca={})
        if pecas: veste(E, 'x', *pecas)
        if fir is None: fir = maldicao.firmeza(E, 'x')
        estado.aplica(E, 'mestre', [['maldicao', 'x', 'poe', maldicao.registro(dict(nome='a Prova', cat=cat, tipo='míngua', condicao=dict(tipo='cumprir')), 'feitiço')]], texto='a maldição')
        E['_novos'].clear()
        for d in range(2, 120):
            E['relogio']['dia'] = d; maldicao.virada(E); E['_novos'].clear(); E['turno']['notas'].clear()
            if E['gente']['x']['estado'] == 'morto': dias.append(d - 1); break
        else: dias.append(999)
    dias.sort(); return dias, fir


AMULETO_COMPRA = 3          # a meta: o amuleto da categoria da maldição compra pelo menos tantos dias (a mediana com ele contra a mediana sem ele, o resto igual)


def _maldicao_mata(n):
    """MG4 A MALDIÇÃO MATA NA FAIXA (M4 a): a da categoria da guarda (o guerreiro de amuleto Raro, maldição Rara) mata a metade das vidas em 10 a 25 dias; a Comum num aldeão sem
    amuleto, em 7 a 14; nenhuma mata antes de 5 dias; e o amuleto conta de verdade (compra pelo menos 3 dias). O dado do mundo, a regra de verdade (maldicao.virada)"""
    k = max(400, n * 2)
    aldeao = dict(Força=40, Agilidade=40, Vigor=50, Vontade=45, Percepção=40, Afinidade=40); guerreiro = dict(Força=80, Agilidade=60, Vigor=80, Vontade=50, Percepção=50, Afinidade=40)
    malha = (item('armadura', 2, 'Malha Rara', material='malha'), 'veste'); amuleto = (item('amuleto', 2, 'Amuleto Raro'), 'pescoco')
    (A, fa), (G, fg), (S, fs) = _vidas(k, 0, aldeao, (), 1), _vidas(k, 2, guerreiro, (malha, amuleto), 2, {'espada': 6}), _vidas(k, 2, guerreiro, (malha,), 3, {'espada': 6})       # o guerreiro é Mestre na espada (a conta D.3)
    med = lambda L: L[len(L) // 2]
    certo = 10 <= med(G) <= 25 and 7 <= med(A) <= 14 and min(A + G + S) >= 5 and med(G) - med(S) >= AMULETO_COMPRA
    return ('MG4 A MALDIÇÃO MATA NA FAIXA DO M4: da categoria da guarda (guerreiro de amuleto Raro e malha Rara, maldição Rara) a metade morre em 10 a 25 dias; a Comum num aldeão sem amuleto, '
            f'em 7 a 14; nenhuma antes de 5 dias (ninguém fazendo nada); e o amuleto compra pelo menos {AMULETO_COMPRA} dias (com ele contra só a malha)',
            f"{k} vidas por linha: guerreiro de amuleto Raro, maldição Rara: metade em {med(G)} dias (1 em 10 em {G[k // 10]}; 9 em 10 em {G[9 * k // 10]}); "
            f"o mesmo sem amuleto (só a malha): {med(S)} (o amuleto compra {med(G) - med(S)}); aldeão sem amuleto, maldição Comum: {med(A)} (1 em 10 em {A[k // 10]}); a mais curta de todas: {min(A + G + S)} dias "
            f"(a Firmeza pela conta que o relógio usa: guerreiro com amuleto {fg:g}, sem amuleto {fs:g}, aldeão {fa:g})".replace('.', ','), certo)


# ---------- 5. o clérigo quebra ----------
def _clerigo(n):
    """MG5 O CLÉRIGO QUEBRA DE 45 A 70% POR RITO: o clérigo Mestre de símbolo Raro, na maldição da categoria do foco, nos passos 1 e 2 (a conta exata, e ritos de verdade)"""
    conj = T.conjuracao(6, 80, 2)
    exata = {k: oficio.chance_de(math.ceil(W.QUEBRAR[0] + W.forca(2) + W.QUEBRAR[1] * (k - 1) - conj)) for k in (1, 2, 3)}
    acima = oficio.chance_de(math.ceil(W.QUEBRAR[0] + W.forca(3) - conj))
    k = max(150, n // 2); quebrou = 0; marca = 0
    for s in range(k):
        E = vila(semente=s + 1, prata=500); gente(E, 'cl', 'Clérigo', dict(Força=50, Agilidade=40, Vigor=60, Vontade=80, Percepção=50, Afinidade=40), tradicao='fé', maestria={'fé': 6},
                                                  feiticos=['quebrar-maldição'], voto=dict(qual='socorro', santuario='vila', dia=1))
        veste(E, 'cl', (item('foco', 2, forma='símbolo'), 'foco'))
        estado.aplica(E, 'mestre', [['maldicao', 'eu', 'poe', maldicao.registro(dict(nome='a Prova', cat=2, tipo='míngua', condicao=dict(tipo='cumprir')), 'feitiço')]], texto='a maldição')
        R = maldicao.rito(E, 'cl', 'eu'); quebrou += R['fim'] == 'quebrou'; marca += R['fim'] == 'marca'
    certo = all(0.45 <= exata[x] <= 0.70 for x in (1, 2)) and abs(quebrou / k - exata[1]) < 0.12
    return ('MG5 O CLÉRIGO QUEBRA DE 45 A 70% POR RITO: o clérigo Mestre (Vontade 80) de símbolo Raro, na maldição da categoria do foco (Rara), nos passos 1 e 2; a cada passo fica mais difícil',
            f"Conjuração {conj:g}; a conta exata: passo 1 {pc(exata[1])}, passo 2 {pc(exata[2])}, passo 3 {pc(exata[3])}; na maldição uma categoria acima (Épica), passo 1: {pc(acima)}; "
            f"{k} ritos de verdade no passo 1: quebrou {pc(quebrou / k)}, levou a marca {pc(marca / k)}", certo)


# ---------- 6. a poção e o golpe ----------
def _golpe_medio(forca=70):
    """o golpe médio de espada entre iguais (a mesma categoria na arma e na malha), pela conta da luta: o d8 vezes K vezes a força; o crítico (5%) rola dois dados e corta a armadura pela metade"""
    p_crit = 2 * (1 / 20) * ((20 - T.CRIT_OUTRO + 1) / 20) - (1 / 20) ** 2
    return T.K_DANO * T.forca_mult(forca) * ((1 - p_crit) * 4.5 + p_crit * 9 * 2)


def _pocao_golpe(n):
    """MG6 A POÇÃO DA CATEGORIA DESFAZ CERCA DE UM GOLPE, A DE BAIXO POUCO: a cura média da poção (o beber de verdade) contra o golpe médio de espada entre iguais"""
    E = vila(); gente(E, 'b', 'Bebedor', dict(Força=70, Agilidade=50, Vigor=200, Vontade=50, Percepção=50, Afinidade=40), nivel=50)
    k = max(200, n); soma = {0: 0, 1: 0}
    da(E, 'b', cura_1=2 * k)
    for funda, chave in ((1, 0), (2, 1)):           # a poção Incomum na ferida Incomum (a da categoria); na ferida Rara (uma acima da poção)
        for _ in range(k):
            b = E['gente']['b']; b['pv'] = 50; b['funda'] = funda; b['marca'].pop('doses', None); b['marca'].pop('curado', None)
            antes = b['pv']; alquimia.beber(E, 'b', 'cura:1'); soma[chave] += E['gente']['b']['pv'] - antes
            E['_novos'].clear()
    g = _golpe_medio(); cat, baixo = soma[0] / k, soma[1] / k
    certo = 0.7 <= cat / g <= 1.5 and baixo / g <= 0.5
    return ('MG6 A POÇÃO DA CATEGORIA DESFAZ CERCA DE UM GOLPE, A DE BAIXO POUCO: a cura média da poção na ferida da categoria dela fica entre 0,7 e 1,5 golpe médio de espada entre iguais; '
            'a poção uma categoria abaixo da ferida, no máximo meio golpe',
            f"o golpe médio entre iguais (Força 70): {vz(g, 1)}; {k} poções bebidas: na ferida da categoria, {vz(cat, 1)} ({vz(cat / g)} golpe); uma categoria abaixo, {vz(baixo, 1)} ({vz(baixo / g)} golpe)", certo)


# ---------- 7. o teto da cura e o limite do corpo ----------
def _teto(n):
    """MG7 O LIMITE DO CORPO E O TETO DA CURA: a poção além das do dia pede Vigor (falhou: não cura, gasta-se, e a pessoa enjoa); feitiço e poção somados nunca curam mais que
    metade do PV máximo por dia"""
    E = vila(); gente(E, 'b', 'Bebedor', dict(Força=50, Agilidade=50, Vigor=60, Vontade=50, Percepção=50, Afinidade=40), nivel=20)
    gente(E, 'cl', 'Clériga', tradicao='fé', maestria={'fé': 4}, feiticos=['cura'], voto=dict(qual='socorro', santuario='vila', dia=1))
    da(E, 'b', cura_2=6, prata=50); b = E['gente']['b']; mx = estado.pv_max(b); b['pv'] = 5; b['funda'] = 0
    for _ in range(T.doses_dia(60)): alquimia.beber(E, 'b', 'cura:2')
    curou = estado.hoje(E, E['gente']['b'], 'curado')
    with dado_posto([-1]): R = alquimia.beber(E, 'b', 'cura:2')
    b = E['gente']['b']; enjoo = isinstance((b.get('marca') or {}).get('enjoo'), dict); pv1 = b['pv']; gastou = (b.get('carga') or {}).get('cura:2', 0) == 6 - T.doses_dia(60) - 1
    teto = int(mx * T.CURA_TETO); pv2 = b['pv']; MM.lancar(E, 'cl', 'cura', alvo='b'); depois = estado.hoje(E, E['gente']['b'], 'curado')
    certo = curou <= teto and R['fim'] == 'enjoou' and enjoo and gastou and pv1 == 5 + curou and depois <= teto and E['gente']['b']['pv'] - pv2 == depois - curou
    return ('MG7 O LIMITE DO CORPO E O TETO DA CURA: Vigor ÷ 30 poções por dia; a seguinte pede Vigor (falhou: a poção se gasta, não cura, e a pessoa enjoa); feitiço e poção somados nunca curam '
            'mais que metade do PV máximo por dia',
            f"Vigor 60: {T.doses_dia(60)} poções Raras curaram {curou} de {mx} (o teto do dia: {teto}); a terceira com o Vigor falhado: {R['fim']}, enjoo {'marcado' if enjoo else 'NÃO'}, "
            f"gasta {'sim' if gastou else 'NÃO'}; o feitiço de cura depois: o dia fecha em {depois} de {teto}", certo)


# ---------- 8. comprar a erva e vender a poção ----------
def _erva_e_pocao(n):
    """MG8 QUEM COMPRA A ERVA E VENDE A POÇÃO NÃO GANHA: com a prateleira no alvo, nenhuma receita (do Comum e do Incomum) paga a matéria comprada na loja, mesmo acertando sempre;
    e a melhor mão de comércio que existe ganha no máximo o que diz a conta"""
    E = vila(prata=5000); L = []
    def conta(pocao, c, mao):
        if (E['gente']['eu'].get('maestria') or {}).get('comércio', 0) != mao: estado.aplica(E, 'mestre', [['pessoa', 'eu', 'maestria.comércio', 'poe', mao]], texto='a mão')
        mat = alquimia.materia_leva(pocao, c)
        if any(E['lugares']['vila']['estoque'].get(k, 0) < q for k, q in mat.items()): return None
        bem = 'remédio' if pocao == 'remédio' else M.materia(pocao, c); doses = 1 if pocao == 'remédio' else W.DOSES
        return mercado.paga(E, 'eu', bem, doses) - sum(mercado.custa(E, 'vila', k, q) for k, q in mat.items())
    for pocao in alquimia.RECEITAS:
        if pocao in C.CRIME: continue
        for c in ((0,) if pocao == 'remédio' else (0, 1)):
            x, y = conta(pocao, c, 0), conta(pocao, c, 8)
            if x is not None: L.append((pocao, c, x, y))
    pior = max(x for _, _, x, _ in L); melhor = max(y for _, _, _, y in L)
    certo = pior <= 0 and melhor <= MINA_COMECO[0]
    return ('MG8 QUEM COMPRA A ERVA E VENDE A POÇÃO NÃO GANHA: com a prateleira no alvo, nenhuma leva (Comum e Incomum, todas as receitas que a loja negocia) paga a matéria comprada na loja '
            f'a quem é Leigo em comércio, mesmo acertando; com a melhor mão que existe, a leva rende no máximo {MINA_COMECO[0]} (uma vez: depois o preço cede)',
            f"{len(L)} levas: a que mais rende ao Leigo dá {mais(pior, 0)} de prata; ao Lendário em comércio, {mais(melhor, 0)} (" + ', '.join(f"{alquimia.nome_pocao(a, c)} {mais(x, 0)}/{mais(y, 0)}" for a, c, x, y in sorted(L, key=lambda z: -z[3])[:4]) + ')', certo)


# ---------- 9 e 10. os robôs: o alquimista e o encantador de loja ----------
def _vida(semente, montar, bancada_):
    """a vida de um robô de loja (o molde do ferreiro de loja, provas_mercado): vive de verdade (come e paga, dorme na cama e paga) e é GANANCIOSO: em todo bloco de bancada que
    o corpo deixa, faz o que mais rende hoje e vende à loja na hora; quando nada paga a matéria, serve o jornal (é disso que come). Devolve o que rendeu por janela."""
    E = montar(semente); lid = 'vila'; p0 = prata(E); t0 = estado.agora(E); corte = t0 + MINA_DIAS[0] * M.BLOCOS_DIA; fim = t0 + MINA_DIAS[1] * M.BLOCOS_DIA
    V = dict(vendas=[0, 0], materia=[0, 0], jornal=[0, 0], obras=[0, 0], parado=None, olhou=0, pagava=0, abriu=0)
    w = lambda: 0 if estado.agora(E) < corte else 1
    while estado.agora(E) < fim and E['gente']['eu']['estado'] == 'vivo':
        b = E['relogio']['bloco']; p = E['gente']['eu']; c = p['corpo']
        if (c['fome'] >= 3 or (b in (0, 1, 5) and c['fome'] >= 2)) and p['moedas'] >= M.REFEICAO_PRECO and E['lugares'][lid]['estoque'].get('comida', 0) > 0:
            ato.comer(E, 'eu'); p = E['gente']['eu']; c = p['corpo']
        aguenta = c['cansaco'] + M.ESFORCO['pesado'] < M.LIMIARES['cansaco'][0] and c['sono'] + M.SONO_ACORDADO < M.LIMIARES['sono'][0]
        if b in (0, 1) or (b == 5 and not aguenta): ato.dormir(E, 'eu', (2 - b) if b < 2 else 3, chao=not ato.cama_paga(E, 'eu') and p['moedas'] < M.CAMA_PRECO, para=False)
        elif aguenta: bancada_(E, V, w)
        else: ato.descansar(E, 'eu', 1)
        E['_novos'].clear()
    eu = E['gente']['eu']; V['vivo'] = eu['estado'] == 'vivo'; V['prata'] = prata(E) == p0; V['inteiro'] = not estado.valida(E)
    V['rende'] = [(V['vendas'][i] - V['materia'][i]) / d for i, d in enumerate((MINA_DIAS[0], MINA_DIAS[1] - MINA_DIAS[0]))]
    return V


def _vende_tudo(E, V, w):
    """vende à loja as poções e o remédio que leva (o que ela paga, e tem prata para pagar)"""
    for b, q in list((E['gente']['eu'].get('carga') or {}).items()):
        if q > 0 and (C.de_beber(b) or b == 'remédio') and M.le_materia(b)[0] not in C.CRIME:
            pg = mercado.paga(E, 'eu', b, q)
            if 1 <= pg <= mercado.caixa(E, 'vila'): V['vendas'][w()] += mercado.vender(E, 'eu', b, q)['prata']


def _escolhe_leva(E, cats, teimosa=False):
    """a leva que MAIS RENDE hoje por bloco a quem compra a matéria e vende as doses à loja (pesada pela chance de acertar e de sair abaixo), ou None. A TEIMOSA leva a que
    menos perde, pague ou não (só precisa ter a prata da matéria): é ela que mede o que a produção de verdade rende na loja"""
    p = E['gente']['eu']; carga = p.get('carga', {}); est = E['lugares']['vila']['estoque']; melhor = None; reserva = M.CAMA_PRECO + M.REFEICAO_PRECO
    vale = lambda bem, q: mercado.paga(E, 'eu', bem, q) if q and C.base(bem) is not None and M.le_materia(bem)[0] not in C.CRIME else 0
    for pocao in alquimia.RECEITAS:
        for c in cats:
            if (pocao == 'remédio' and c) or pocao in C.CRIME: continue
            mat = alquimia.materia_leva(pocao, c); falta = {k: q - carga.get(k, 0) for k, q in mat.items() if carga.get(k, 0) < q}
            if any(est.get(k, 0) < q for k, q in falta.items()): continue
            custo = sum(mercado.custa(E, 'vila', k, q) for k, q in falta.items())
            if p['moedas'] < custo + reserva: continue
            meu = sum(mercado.parte(p) * mercado.lote(E, 'vila', k, min(q, carga.get(k, 0)), compra=False) for k, q in mat.items() if carga.get(k, 0) > 0)
            k = oficio.conta(E, 'eu', c, 'alquimia'); n = 1 if pocao == 'remédio' else W.DOSES; bem = lambda cc: 'remédio' if pocao == 'remédio' else M.materia(pocao, cc)
            rende = k['acerta'] * vale(bem(c), n) + k['pouco'] * (vale(bem(c - 1), n) if c else vale(bem(0), 1 if pocao == 'remédio' else W.AGUADA))
            lucro = (rende - custo - meu) / O.blocos(c)
            if (lucro > 0 or teimosa) and (melhor is None or lucro > melhor[0]): melhor = (lucro, pocao, c, falta)
    return melhor and melhor[1:]


def _melhor_leva(E, cats):
    """a conta da MG8 para a alquimista deste mundo, hoje: o que a melhor leva rende (o que a loja paga pelas doses, menos a matéria comprada na loja), acertando sempre"""
    est = E['lugares']['vila']['estoque']; L = []
    for pocao in alquimia.RECEITAS:
        for c in cats:
            if (pocao == 'remédio' and c) or pocao in C.CRIME: continue
            mat = alquimia.materia_leva(pocao, c)
            if any(est.get(k, 0) < q for k, q in mat.items()): continue
            bem = 'remédio' if pocao == 'remédio' else M.materia(pocao, c)
            L.append(mercado.paga(E, 'eu', bem, 1 if pocao == 'remédio' else W.DOSES) - sum(mercado.custa(E, 'vila', k, q) for k, q in mat.items()))
    return max(L) if L else None


def _alquimista(semente, cats, botica, teimosa=False):
    def montar(s):
        E = vila(s, botica=botica); p = E['gente']['eu']; p['atributos']['Afinidade'] = 65
        estado.aplica(E, 'gera', [['pessoa', 'eu', 'maestria.alquimia', 'poe', 2], ['pessoa', 'eu', 'treino.alquimia', 'soma', 50], ['pessoa', 'eu', 'marca.prep_alquimia', 'poe', 0]], texto='a alquimista de começo')
        if botica == 0: estado.aplica(E, 'gera', [['lugar', 'vila', 'produz.' + b, 'poe', 0] for b in list(E['lugares']['vila'].get('produz') or {}) if C.e_magia(b)] or [['lugar', 'vila', 'botica', 'poe', 0]], texto='sem botica que produza')
        E['_novos'].clear(); return E
    def bancada_(E, V, w):
        R = None
        if [o for o in oficio.obras_de(E, 'eu').values() if o['tipo'] == 'leva']: R = oficio.continua(E, 'eu', blocos=1)
        elif V['parado'] != E['relogio']['dia']:
            if V['olhou'] == 0: V['dia1'] = _melhor_leva(E, cats)        # a conta da MG8 neste mundo, no primeiro olhar: se ela diz que paga, o robô tem de fazer
            esc = _escolhe_leva(E, cats, teimosa); V['olhou'] += 1
            if esc:
                pocao, c, falta = esc; V['pagava'] += 1
                for k, q in falta.items(): V['materia'][w()] += mercado.comprar(E, 'eu', k, q)['prata']
                R = alquimia.fazer(E, 'eu', pocao, c, blocos=1); V['abriu'] += 1
            else: V['parado'] = E['relogio']['dia']
        if R is None: V['jornal'][w()] += oficio.jornal(E, 'eu', 1, 'alquimia')['ganhou']; return
        if R.get('fim'): V['obras'][w()] += 1; _vende_tudo(E, V, w)
    return _vida(semente, montar, bancada_)


def _escolhe_peca(E, cats):
    """o foco ou o amuleto que MAIS RENDE hoje por bloco a quem compra a matéria e vende a peça à loja, ou None"""
    p = E['gente']['eu']; carga = p.get('carga', {}); est = E['lugares']['vila']['estoque']; melhor = None; reserva = M.CAMA_PRECO + M.REFEICAO_PRECO
    def paga_se(peca, cat, tosca=False):
        it = item(peca['tipo'], cat, **({'forma': peca['forma']} if peca['tipo'] == 'foco' else {}), dono='eu')
        if tosca: it['dur'][0] = max(1, int(it['dur'][1] * O.TOSCA))
        return mercado.paga_peca(E, 'eu', it)
    for c in cats:
        for peca in [oficio.molde('foco', c, forma=f) for f in M.MATERIA_FOCO] + [oficio.molde('amuleto', c)]:
            mat = oficio.materia_de(peca); falta = {k: q - carga.get(k, 0) for k, q in mat.items() if carga.get(k, 0) < q}
            if any(est.get(k, 0) < q for k, q in falta.items()): continue
            custo = sum(mercado.custa(E, 'vila', k, q) for k, q in falta.items())
            if p['moedas'] < custo + reserva: continue
            meu = sum(mercado.parte(p) * mercado.lote(E, 'vila', k, min(q, carga.get(k, 0)), compra=False) for k, q in mat.items() if carga.get(k, 0) > 0)
            k = oficio.conta(E, 'eu', c, 'encanto')
            rende = k['acerta'] * paga_se(peca, c) + k['pouco'] * (paga_se(peca, c - 1) if c else paga_se(peca, 0, tosca=True))
            lucro = (rende - custo - meu) / O.blocos(c)
            if lucro > 0 and (melhor is None or lucro > melhor[0]): melhor = (lucro, peca, falta)
    return melhor and melhor[1:]


def _encantador(semente, cats):
    def montar(s):
        E = vila(s); p = E['gente']['eu']; p['atributos']['Afinidade'] = 65
        estado.aplica(E, 'gera', [['pessoa', 'eu', 'maestria.encanto', 'poe', 2], ['pessoa', 'eu', 'treino.encanto', 'soma', 50], ['pessoa', 'eu', 'marca.prep_encanto', 'poe', 0]], texto='o encantador de começo')
        E['_novos'].clear(); return E
    def bancada_(E, V, w):
        R = None
        if [o for o in oficio.obras_de(E, 'eu').values() if o.get('oficio') == 'encanto']: R = oficio.continua(E, 'eu', blocos=1)
        elif V['parado'] != E['relogio']['dia']:
            esc = _escolhe_peca(E, cats)
            if esc:
                peca, falta = esc
                for k, q in falta.items(): V['materia'][w()] += mercado.comprar(E, 'eu', k, q)['prata']
                R = oficio.forjar(E, 'eu', peca, blocos=1)
            else: V['parado'] = E['relogio']['dia']
        if R is None: V['jornal'][w()] += oficio.jornal(E, 'eu', 1, 'encanto')['ganhou']; return
        if R.get('fim'):
            V['obras'][w()] += 1
            if R['item']:
                pg = mercado.paga_peca(E, 'eu', E['itens']['itens'][R['item']])
                if 1 <= pg <= mercado.caixa(E, 'vila'): V['vendas'][w()] += mercado.vender_peca(E, 'eu', R['item'])['prata']
    return _vida(semente, montar, bancada_)


def _robo(titulo, vidas_por_escada):
    """julga as escadas de um robô de loja contra a faixa do ferreiro de loja"""
    media = lambda L: sum(L) / len(L)
    m5 = {k: media([V['rende'][0] for V in vs]) for k, vs in vidas_por_escada.items()}; p5 = {k: max(V['rende'][0] for V in vs) for k, vs in vidas_por_escada.items()}
    m30 = {k: media([V['rende'][1] for V in vs]) for k, vs in vidas_por_escada.items()}; todas = [V for vs in vidas_por_escada.values() for V in vs]
    fecha = all(V['prata'] and V['inteiro'] and V['vivo'] for V in todas); sementes = min(len(vs) for vs in vidas_por_escada.values())
    certo = sementes >= MINA_SEMENTES and max(m5.values()) <= MINA_COMECO[0] and max(p5.values()) <= MINA_COMECO[1] and max(m30.values()) <= MINA_DEPOIS and fecha
    diz = '. '.join(f"{k}: nos {MINA_DIAS[0]} primeiros dias {vz(m5[k])} de prata por dia (o pior caso {vz(p5[k])}), {vz(media([V['obras'][0] for V in vidas_por_escada[k]]), 1)} obras; "
                    f"do Dia {MINA_DIAS[0] + 1} ao {MINA_DIAS[1]}, {vz(m30[k])} por dia; o jornal deu {vz(media([V['jornal'][0] for V in vidas_por_escada[k]]) / MINA_DIAS[0])} por dia" for k in vidas_por_escada)
    return (titulo + f": o que rende (o que a loja paga, menos a matéria comprada) fica em média no máximo {MINA_COMECO[0]} de prata por dia nos {MINA_DIAS[0]} primeiros dias (o pior caso, {MINA_COMECO[1]}), "
            f"e no máximo {MINA_DEPOIS} por dia do Dia {MINA_DIAS[0] + 1} ao {MINA_DIAS[1]} (a faixa do ferreiro de loja)",
            f"{sementes} vilas por escada. {diz}. A prata {'fecha' if all(V['prata'] for V in todas) else 'NÃO FECHA'}; estado {'inteiro' if all(V['inteiro'] for V in todas) else 'QUEBRADO'}"
            + ('' if all(V['vivo'] for V in todas) else f"; MORRERAM {sum(not V['vivo'] for V in todas)}"), certo)


def _alquimista_de_loja(n):
    """MG9 O ALQUIMISTA DE LOJA NÃO É MINA (P5): a alquimista de começo (Iniciante, Afinidade 65, a receita Comum) compra a matéria na loja, faz a leva que mais rende e vende as doses;
    numa vila com botica (o povo produz as poções Comuns) e numa sem botica que produza (a prateleira só gasta); e A TEIMOSA, que faz a leva todo dia, pague ou não (é ela que
    mede a produção de verdade). O robô guloso olha todo dia e faz a leva sempre que ela paga: se a conta da MG8 diz que alguma paga, ele tem de ter feito"""
    k = max(MINA_SEMENTES, n // 10)
    linhas = {'com botica, Comum e Incomum': [_alquimista(s, (0, 1), 1) for s in range(1, k + 1)], 'sem botica que produza, Comum e Incomum': [_alquimista(s, (0, 1), 0) for s in range(1, k + 1)],
              'a teimosa, com botica (faz a leva todo dia, pague ou não)': [_alquimista(s, (0, 1), 1, teimosa=True) for s in range(1, k + 1)]}
    nome, deu, certo = _robo('MG9 O ALQUIMISTA DE LOJA NÃO É MINA', linhas)
    gulosos = [V for k_, vs in linhas.items() if 'teimosa' not in k_ for V in vs]; teimosa = linhas['a teimosa, com botica (faz a leva todo dia, pague ou não)']
    olhou = all(V['olhou'] > 0 for V in gulosos); coerente = all(V['abriu'] == V['pagava'] and (V.get('dia1') is None or V['dia1'] <= 0 or sum(V['obras']) > 0) for V in gulosos)
    fez = sum(sum(V['obras']) for V in teimosa) / len(teimosa)
    certo = certo and olhou and coerente and fez >= 1
    pagava = sum(1 for V in gulosos if V.get('dia1') is not None and V['dia1'] > 0)
    return (nome + '; o guloso olha todo dia e faz a leva sempre que ela paga; a teimosa produz de verdade',
            deu + f". O guloso olhou {sum(V['olhou'] for V in gulosos)} vezes ({'todas as vidas' if olhou else 'NÃO OLHOU em alguma'}), achou leva que pagava {sum(V['pagava'] for V in gulosos)} e abriu {sum(V['abriu'] for V in gulosos)}; "
            f"no primeiro olhar, a conta da MG8 dizia que alguma leva pagava em {pagava} de {len(gulosos)} vidas ({'coerente' if coerente else 'INCOERENTE: pagava e ele não fez'}); "
            f"a teimosa fez {vz(fez, 1)} obras por vida", certo)


def _encantador_de_loja(n):
    """MG10 FAZER FOCO E AMULETO PARA A LOJA NÃO É MINA (P7): o encantador de começo (Iniciante, Afinidade 65, a receita Comum), na mesa de runas, compra a matéria, faz a peça que mais rende
    e a vende à loja (a loja farta conta junto com as armas da mesma categoria)"""
    k = max(MINA_SEMENTES, n // 10)
    return _robo('MG10 FAZER FOCO E AMULETO PARA A LOJA NÃO É MINA', {'Comuns': [_encantador(s, (0,)) for s in range(1, k + 1)], 'Comuns e Incomuns': [_encantador(s, (0, 1)) for s in range(1, k + 1)]})


# ---------- 11. o serviço de magia ----------
def _servico(n):
    """MG11 O SERVIÇO DE MAGIA NÃO É MINA: o jornal da botica, do santuário e da mesa de runas entra na jornada (com o trabalhar, 2 blocos pagos por dia); a lição do mestre também; o serviço de
    pessoa a pessoa só muda a prata de mão; e ninguém compra serviço sozinho (a gente do mundo não procura clérigo nesta etapa)"""
    E = vila(prata=300); gente(E, 'nara', 'Nara', tradicao='fé', maestria={'fé': 4, 'cura': 2, 'alquimia': 2}, feiticos=['cura', 'quebrar-maldição', 'bênção', 'ler'][:3], voto=dict(qual='socorro', santuario='vila', dia=1), carga={'remédio': 2})
    gente(E, 'ans', 'Anselmo', tradicao='arcano', maestria={'arcano': 4, 'encanto': 2}, feiticos=['seta', 'luz'])
    p0 = prata(E); E['relogio']['bloco'] = 1; m0 = E['gente']['nara']['moedas']
    a = oficio.jornal(E, 'nara', 2, 'alquimia')['ganhou']; b = oficio.jornal(E, 'nara', 2, 'fé')['ganhou']; c = ato.trabalhar if False else None
    pagos = ato.jornada(E, 'nara'); ganhou = E['gente']['nara']['moedas'] - m0
    F = vila(prata=300); gente(F, 'ans', 'Anselmo', tradicao='arcano', maestria={'arcano': 4, 'encanto': 2}, feiticos=['seta', 'luz']); F['relogio']['bloco'] = 2
    oficio.jornal(F, 'ans', 1, 'encanto'); R = MM.estudar(F, 'eu', 'seta', {'com': 'ans'}); licao = R['feitos']
    E['gente']['eu']['pv'] -= 30; estado.aplica(E, 'mestre', [['ferida', 'eu', 'abre', 'braços', False]], texto='ferido')
    p1 = prata(E); MM.lancar(E, 'nara', 'cura', alvo='eu'); MM.tratar(E, 'nara', 'eu')
    gente(E, 'qui', 'Quitéria', tradicao='pacto', carga={'veneno:1': 2}, moedas=0); MM.compra(E, 'eu', 'veneno:1', 1, 'qui', preco=40); fecha = prata(E) == p1 == p0 and (E['gente']['eu'].get('carga') or {}).get('veneno:1') == 1
    torto = [recusa(lambda: MM.compra(E, 'eu', 'veneno:1', 1, 'qui', preco=x)) for x in (-20, 'abc')] + [recusa(lambda: MM.lancar(E, 'nara', 'bênção', alvo='eu', paga_=-5))]
    dias, nao_paga, fecha2 = _serve_o_povo()
    certo = (pagos == M.JORNADA and ganhou == a + b and a + b <= M.JORNADA * M.SALARIO['mestre'] and licao == 1 and fecha and not estado.valida(E) and all(torto)
             and all('preço' in x for x in torto) and max(dias) <= MINA_COMECO[1] and sum(dias) / len(dias) <= MINA_COMECO[0] and nao_paga == len(dias) and fecha2)
    return ('MG11 O SERVIÇO DE MAGIA NÃO É MINA: o jornal da botica, do santuário e da mesa de runas entra na jornada (2 blocos pagos por dia, com o trabalhar e a lição); o serviço de pessoa a '
            'pessoa (cura, tratar, ler, o rito, o veneno que a bruxa vende) só muda a prata de mão, e o preço torto (negativo, que não é número) é recusado; e ninguém compra serviço sozinho nesta etapa: '
            f'o personagem que serve a gente do mundo {MINA_DIAS[0]} dias seguidos não ganha mais de {MINA_COMECO[1]} de prata em dia nenhum (a gente do mundo não paga, nem com paga=)',
            f"Nara serve 2 blocos na botica e 2 no santuário: o lugar paga {pagos} blocos ({ganhou} de prata); Anselmo, depois de 1 bloco de jornal nas runas, ensina {licao} bloco pago; "
            f"a cura, o tratamento e o veneno comprado à bruxa: a prata do mundo {'fecha' if fecha else 'NÃO FECHA'}; o preço torto: {sum(1 for x in torto if x)} de {len(torto)} recusados; "
            f"o personagem clérigo benze, cura e lê a gente do mundo por {len(dias)} dias: ganha {', '.join(str(x) for x in dias)} de prata por dia, e o paga= de quem não é o personagem é recusado "
            f"{nao_paga} de {len(dias)} vezes; a prata do mundo {'fecha' if fecha2 else 'NÃO FECHA'}", certo)


def _serve_o_povo():
    """o personagem clérigo (voto do socorro, a bênção, a cura e a leitura) serve a gente do mundo por MINA_DIAS[0] dias, à vontade: a prece do dia no santuário, a bênção a todos
    até a Mana acabar, a cura em quem está ferido, a leitura do dom. Devolve (a prata que ganhou em cada dia, quantas vezes o paga= de outro foi recusado, a prata do mundo fecha)"""
    E = vila(prata=30)
    estado.aplica(E, 'gera', [['pessoa', 'eu', 'tradicao', 'poe', 'fé'], ['pessoa', 'eu', 'voto', 'poe', dict(qual='socorro', santuario='vila', dia=1)], ['pessoa', 'eu', 'maestria.fé', 'poe', 4],
                              ['pessoa', 'eu', 'feitico', 'aprende', 'bênção'], ['pessoa', 'eu', 'feitico', 'aprende', 'cura']], texto='o personagem clérigo')
    povo = [gente(E, f'p{i}', f'Povo {i}', moedas=60) for i in range(4)]; p0 = prata(E); dias = []; nao = 0
    for d in range(MINA_DIAS[0]):
        E['relogio']['dia'] = 1 + d; E['relogio']['bloco'] = 1; E['gente']['eu']['corpo'].update(fome=0, sono=0, cansaco=0); m0 = E['gente']['eu']['moedas']
        estado.aplica(E, 'mestre', [['pessoa', 'p0', 'pv', 'soma', -40]], texto='um do povo se fere')
        for f in (lambda: MM.prece(E, 'eu'), lambda: MM.ler(E, 'eu', 'dom', 'p1')): recusa(f)
        nao += 'não paga' in (recusa(lambda: MM.lancar(E, 'eu', 'bênção', alvo='p2', paga_=5)) or '')
        for q in povo * 3:
            for f in ('cura', 'bênção'): recusa(lambda: MM.lancar(E, 'eu', f, alvo=q))
        dias.append(E['gente']['eu']['moedas'] - m0); E['_novos'].clear()
    return dias, nao, prata(E) == p0 and not estado.valida(E)


# ---------- 12. a peça maldita e o lugar maldito ----------
def _peca_e_lugar(n):
    """MG12 A PEÇA MALDITA E O LUGAR MALDITO: pôr em uso põe a maldição (passo 1, a pessoa não sabe); a peça não sai de uso nem de mão; devolver no lugar errado recusa, no certo quebra e a peça
    fica no chão, ainda maldita; o lugar maldito pega a cada bloco (o dado do mundo), e a maldição dele quebra com 7 dias longe; o morto leva as maldições para a morte"""
    E = vila(); s0 = E['itens']['seq']; estado.aplica(E, 'gera', [['item', 'nasce', item('arma', 1, 'Adaga do Túmulo', familia='adaga', onde='vila', solto=True)]], texto='a adaga')
    iid = f"i{s0 + 1:04d}"; E['lugares']['cova'] = dict(nome='a Cova', em='na Cova', tipo='ermo', estoque={}, vizinhos=['vila'])
    maldicao.amaldicoa_peca(E, iid, 'a Mão Fria', 1, 'míngua', onde='cova')
    estado.aplica(E, 'mestre', [['item', iid, 'dono', 'poe', 'eu']], texto='pega a adaga'); ato.vestir(E, 'eu', iid)
    ms = maldicao.minhas(E['gente']['eu']); pegou = len(ms) == 1 and ms[0]['passo'] == 1 and ms[0].get('sabe') == 0 and not maldicao.voce(E)
    presa = [recusa(lambda: ato.tirar(E, 'eu', iid)), recusa(lambda: mercado.vender_peca(E, 'eu', iid)), recusa(lambda: estado.aplica(E, 'mestre', [['item', iid, 'dono', 'poe', None]], texto='x'))]
    errado = recusa(lambda: maldicao.devolver(E, 'eu', iid))
    E['gente']['eu']['marca']['caca'] = dict(ermo='cova', fase='procura', restam=4, casa='vila', com=[])       # está na cova (a saída aberta, à mão)
    maldicao.devolver(E, 'eu', iid); it = E['itens']['itens'][iid]; certo_dev = not maldicao.minhas(E['gente']['eu']) and it.get('solto') and it.get('onde') == 'cova' and isinstance(it.get('maldita'), dict)
    # o lugar maldito: muita gente passando um bloco, e a maldição quebra com 7 dias longe
    L = vila(); maldicao.amaldicoa_lugar(L, 'vila', 'o Ar Parado', 0, 'azar'); pegam = 0; k = max(60, n // 5)
    for i in range(k):
        pid = gente(L, f'p{i}', f'P{i}', dict(Força=40, Agilidade=40, Vigor=50, Vontade=40, Percepção=40, Afinidade=40))
        pegam += bool([x for x in MM.bloco(L, pid, 'nada', None) + maldicao.bloco(L, pid, 'nada', None) if x[0] == 'maldicao'])
    esperado = oficio.chance_de(math.ceil(T.firmeza(40, 0) - W.forca(0)))
    S = vila(); S['lugares']['cova'] = dict(nome='a Cova', em='na Cova', tipo='ermo', estoque={}, vizinhos=['vila'])
    estado.aplica(S, 'mestre', [['maldicao', 'eu', 'poe', maldicao.registro(dict(nome='o Ar Parado', cat=0, tipo='azar', condicao=dict(tipo='sair')), 'lugar', fonte='cova', condicao=dict(tipo='sair', lugar='cova', visto=1))]], texto='x')
    for d in range(2, 10): S['relogio']['dia'] = d; maldicao.virada(S)
    sai = not maldicao.minhas(S['gente']['eu'])
    Mo = vila(); estado.aplica(Mo, 'mestre', [['maldicao', 'eu', 'poe', maldicao.registro(dict(nome='a Prova', cat=0, tipo='míngua', condicao=dict(tipo='cumprir')), 'feitiço')]], texto='x')
    estado.aplica(Mo, 'mestre', [['pessoa', 'eu', 'estado', 'poe', 'morto']], texto='morre'); morto = not Mo['gente']['eu'].get('maldicoes') and Mo['gente']['eu']['morte'].get('maldicoes')
    certo = pegou and all(presa) and errado and certo_dev and abs(pegam / k - esperado) < 0.2 and sai and morto and not estado.valida(E) and not estado.valida(S)
    return ('MG12 A PEÇA MALDITA E O LUGAR MALDITO: pôr em uso põe a maldição (passo 1, a pessoa não sabe); a peça não sai de uso, não se vende, não muda de mão; devolver longe recusa, no lugar '
            'dela quebra e a peça fica no chão, ainda maldita; o lugar maldito pega pelo dado do mundo, e a maldição dele quebra com 7 dias longe; o morto leva as maldições para a morte',
            f"pegou no passo 1, escondida: {'sim' if pegou else 'NÃO'}; tirar, vender e dar: {sum(1 for x in presa if x)} de 3 recusados; devolver longe: {'recusado' if errado else 'ACEITO'}; "
            f"devolver na cova: {'quebra, a peça fica lá, maldita' if certo_dev else 'ERRADO'}; o lugar maldito pegou {pegam} de {k} num bloco (a conta: {pc(esperado)}); "
            f"7 dias longe: {'quebra' if sai else 'NÃO QUEBRA'}; o morto: {'a maldição foi para a morte' if morto else 'ERRADO'}", certo)


# ---------- 13. gravar custa o que diz ----------
def _gravar(n):
    """MG13 GRAVAR CUSTA O QUE DIZ (E4): acertar grava no grau de quem sabe; falhar por pouco, um grau abaixo; por 5 ou mais, a essência some e a peça perde 5; por 10 ou mais, a peça sai MALDITA;
    a peça Épica gasta o núcleo em qualquer saída; a chance é a da forja"""
    def uma(margem, cat=0):
        E = vila(); gente(E, 'ans', 'Anselmo', tradicao='arcano', maestria={'arcano': 4, 'encanto': 2}, feiticos=['prender'])
        it = veste(E, 'ans', (item('arma', cat, 'Lança de prova', familia='lança'), 'arma'))[0]
        if cat >= 3: estado.aplica(E, 'gera', [['item', 'nasce', dict(tipo='nucleo', cat=cat, nome='núcleo de prova', dur=[1, 1], dono='ans', historia=[])]], texto='o núcleo')
        else: da(E, 'ans', **{f'osso_{cat}': 4, f'erva_{cat}': 2})
        m0 = materia(E); n0 = sum(1 for x in E['itens']['itens'].values() if x['tipo'] == 'nucleo')
        with dado_posto([margem]): R = termina(E, 'ans', encanto.gravar(E, 'ans', it, 'prender'))
        x = E['itens']['itens'][it]; m1 = materia(E)
        return dict(fim=R['fim'], enc=[(e['feitico'], e['grau']) for e in x.get('encantos') or []], dur=x['dur'][0], maldita=isinstance(x.get('maldita'), dict),
                    essencia=m0 - m1, nucleo=n0 - sum(1 for y in E['itens']['itens'].values() if y['tipo'] == 'nucleo'), inteiro=not estado.valida(E), conta=oficio.conta(E, 'ans', cat, 'encanto'))
    a, b, c, d, e = uma(0), uma(-2), uma(-6), uma(-12), uma(-1, 3)
    dur0 = T.DUR[0]
    certo = (a['enc'] == [('prender', 2)] and b['enc'] == [('prender', 1)] and c['enc'] == [] and c['dur'] == dur0 - W.ESTRAGO and not c['maldita'] and d['maldita'] and d['dur'] == dur0 - W.ESTRAGO
             and a['essencia'] == b['essencia'] == c['essencia'] == 6 and e['nucleo'] == 1 and e['enc'] == [('prender', 1)] and all(x['inteiro'] for x in (a, b, c, d, e))
             and a['conta']['contra'] == O.contra(0))
    return ('MG13 GRAVAR CUSTA O QUE DIZ (E4): acertar grava no grau de quem sabe o feitiço; falhar por 1 a 4, um grau abaixo; por 5 ou mais, a essência some e a peça perde 5 de durabilidade; '
            'por 10 ou mais, a peça sai MALDITA; a peça Épica gasta o núcleo em qualquer saída; o teste é o da forja (contra 28 + 6 por categoria)',
            f"acertou: {a['enc']}; por pouco: {b['enc']}; por 6: encanto {c['enc']}, durabilidade {c['dur']} de {dur0}, maldita {'sim' if c['maldita'] else 'não'}; por 12: maldita {'SIM' if d['maldita'] else 'NÃO'}; "
            f"a essência gasta em cada saída: {a['essencia']}, {b['essencia']}, {c['essencia']}; a Épica por pouco: núcleo gasto {e['nucleo']}, encanto {e['enc']}", certo)


# ---------- 14. a mesa, o retomar e o fecha ----------
def _mesa(n):
    """MG14 A MESA, O RETOMAR E O FECHA (D6): a maldição do personagem não aparece no passo 1; do passo 2 a MESA diz o sinal (sem nome); depois de lida, tudo; o RETOMAR a leva; o `fecha` recusa
    com ela no passo 4 sem pergunta aberta sobre ela, e aceita com uma"""
    with pasta():
        E = vila(); gente(E, 'qui', 'Quitéria', tradicao='pacto', maestria={'pacto': 4}, feiticos=['ler'])
        estado.aplica(E, 'mestre', [['maldicao', 'eu', 'poe', maldicao.registro(dict(nome='a Mão Fria', cat=1, tipo='míngua', condicao=dict(tipo='cumprir')), 'feitiço')]], texto='x')
        mid = maldicao.minhas(E['gente']['eu'])[0]['id']; t1 = turno.mesa(E).split('## SÓ O MESTRE')[0]; a = 'Mão Fria' not in t1 and 'ALGO ESTÁ ERRADO' not in t1
        estado.aplica(E, 'mestre', [['maldicao', 'eu', mid, 'passo', 1]], texto='x'); t2 = turno.mesa(E); b = 'ALGO ESTÁ ERRADO' in t2 and 'Mão Fria' not in t2.split('## SÓ O MESTRE')[0]
        E['relogio']['bloco'] = 2; MM.ler(E, 'qui', 'maldicao', 'eu'); t3 = turno.mesa(E); c = 'MALDIÇÃO: a Mão Fria' in t3.split('## SÓ O MESTRE')[0]
        estado.aplica(E, 'mestre', [['maldicao', 'eu', mid, 'passo', 2]], texto='x')
        turno.pergunta(E, 'O que fazer na vila?', ['a=ficar', 'b=sair']); turno.pergunta(E, 'Comer agora?', ['a=sim', 'b=não'])
        r1 = recusa(lambda: turno.fecha(E, 'um dia'))
        turno.pergunta(E, 'A maldição aperta: o que fazer?', ['a=procurar a clériga', 'b=esperar'])
        r2 = recusa(lambda: turno.fecha(E, 'um dia')); ret = open(os.path.join(estado.pasta(), 'RETOMAR.md'), encoding='utf-8').read() if not r2 else ''
        d = 'MALDIÇÃO: a Mão Fria' in ret.split('## SÓ O MESTRE')[0]
    certo = a and b and c and bool(r1) and 'maldição' in (r1 or '') and r2 is None and d
    return ('MG14 A MESA, O RETOMAR E O FECHA (D6): no passo 1 a MESA não mostra a maldição; do passo 2, o sinal sem nome; lida, tudo; o RETOMAR a leva; o `fecha` recusa com ela no passo 4 sem '
            'pergunta aberta sobre ela, e aceita com uma',
            f"passo 1 escondido: {'sim' if a else 'NÃO'}; passo 2 o sinal: {'sim' if b else 'NÃO'}; lida, tudo: {'sim' if c else 'NÃO'}; o fecha no passo 4 sem pergunta: {'recusa' if r1 else 'ACEITA'}; "
            f"com a pergunta: {'fecha' if r2 is None else 'RECUSA: ' + r2[:80]}; o RETOMAR: {'leva' if d else 'NÃO LEVA'}", certo)


# ---------- 15. a prata e a matéria fecham ----------
def _fecha(n):
    """MG15 A PRATA E A MATÉRIA FECHAM (P8): levas que acertam, saem aguadas e se perdem, a Épica com núcleo, poções compradas e vendidas: a prata do mundo não muda; a matéria da leva perdida some
    (a conta do mundo cai exatamente o que ela levava); o núcleo da leva perdida sai do Livro"""
    E = vila(prata=2000); p = E['gente']['eu']; p['atributos']['Afinidade'] = 60; estado.aplica(E, 'gera', [['pessoa', 'eu', 'maestria.alquimia', 'poe', 6]], texto='a mão')
    da(E, erva_0=40, osso_0=8, erva_2=8); p0 = prata(E); fecha = True; L = []
    for margem in (0, -2, -7):
        m0 = materia(E)
        with dado_posto([margem]): R = termina(E, 'eu', alquimia.fazer(E, 'eu', 'cura', 0))
        L.append((R['fim'], m0 - materia(E), (E['gente']['eu'].get('carga') or {}).get('cura:0', 0)))
    estado.aplica(E, 'gera', [['item', 'nasce', dict(tipo='nucleo', cat=3, nome='núcleo Épico', dur=[1, 1], dono='eu', historia=[])]], texto='o núcleo')
    n0 = sum(1 for x in E['itens']['itens'].values() if x['tipo'] == 'nucleo')
    with dado_posto([-9]): R = termina(E, 'eu', alquimia.fazer(E, 'eu', 'cura', 3))
    nucleo_saiu = n0 - sum(1 for x in E['itens']['itens'].values() if x['tipo'] == 'nucleo') == 1 and R['fim'] == 'perdeu'
    estado.aplica(E, 'gera', [['item', 'nasce', dict(tipo='nucleo', cat=3, nome='núcleo Épico', dur=[1, 1], dono='eu', historia=[])]], texto='o núcleo')
    da(E, erva_2=4)
    with dado_posto([0]): R2 = termina(E, 'eu', alquimia.fazer(E, 'eu', 'cura', 3))
    elix = sum(1 for x in E['itens']['itens'].values() if x['tipo'] == 'elixir' and x.get('dono') == 'eu')
    c = mercado.comprar(E, 'eu', 'cura:0', 2); v = mercado.vender(E, 'eu', 'cura:0', 2); fecha = prata(E) == p0
    certo = L[0] == ('acertou', 4, 2) and L[1] == ('abaixo', 4, 3) and L[2] == ('perdeu', 4, 3) and nucleo_saiu and R2['fim'] == 'acertou' and elix == W.ELIXIRES and fecha and c['prata'] > v['prata'] and not estado.valida(E)
    return ('MG15 A PRATA E A MATÉRIA FECHAM (P8): a leva que acerta rende 2 doses, a que sai aguada 1, a que se perde some com a matéria (a conta do mundo cai o que ela levava); a Épica perdida tira o '
            'núcleo do Livro, e a que acerta rende 6 elixires; comprar e vender poção de volta sempre perde; a prata do mundo não muda',
            f"as levas Comuns (saída, matéria que saiu do mundo, doses na carga): {L}; a Épica perdida tira o núcleo: {'sim' if nucleo_saiu else 'NÃO'}; a Épica acertada: {elix} elixires; "
            f"comprar 2 e vender 2: {c['prata']} contra {v['prata']}; prata {'fecha' if fecha else 'NÃO FECHA'}", certo)


# ---------- 16. o voto, o laço e a dívida ----------
def _tradicoes(n):
    """MG16 O VOTO, O LAÇO E A DÍVIDA: o voto da lâmina se quebra ao pôr em uso uma espada (o voto fica quebrado, a Mana se apaga, fica a marca); o da pobreza leva ao santuário a prata acima de 50
    (a prata fecha); a dívida acima de Vontade ÷ 10 vira maldição na virada e quebra quando a dívida zera; o pacto só no escuro; o laço com ermo vizinho"""
    E = vila(prata=120); gente(E, 'cl', 'Clérigo', tradicao=None, maestria={'fé': 2}, moedas=20)
    E['relogio']['bloco'] = 2; MM.voto(E, 'cl', 'lâmina'); MM.voto if False else None
    esp = veste(E, 'cl', (item('arma', 0, 'Espada', familia='espada'), None))[0]; ato.vestir(E, 'cl', esp); c = E['gente']['cl']
    lamina = c['voto'].get('quebrado') is not None and estado.mana(c) == 0 and any(m.get('de') == 'juramento' for m in maldicao.minhas(c))
    P = vila(); gente(P, 'po', 'Pobre', voto=dict(qual='pobreza', santuario='vila', dia=1), tradicao='fé', moedas=90); p0 = prata(P); cx = P['lugares']['vila']['estoque']['prata']
    P['relogio']['dia'] = 2; MM.virada(P); pobreza = P['gente']['po']['moedas'] == W.VOTO_POBREZA and P['lugares']['vila']['estoque']['prata'] == cx + 40 and prata(P) == p0
    D = vila(); gente(D, 'bx', 'Bruxa', dict(Força=40, Agilidade=50, Vigor=60, Vontade=40, Percepção=50, Afinidade=60), tradicao='pacto', maestria={'pacto': 2}, divida=5)
    D['relogio']['dia'] = 2; MM.virada(D); conta = [m for m in maldicao.minhas(D['gente']['bx']) if (m.get('condicao') or {}).get('tipo') == 'divida']
    D['relogio']['bloco'] = 2; MM.paga_divida(D, 'bx', 5, 'pv'); zera = not D['gente']['bx'].get('divida') and not maldicao.minhas(D['gente']['bx'])
    Q = vila(); Q['relogio']['bloco'] = 2; claro = recusa(lambda: MM.pacto(Q, 'eu')); Q['relogio']['bloco'] = 5; MM.pacto(Q, 'eu'); escuro = Q['gente']['eu'].get('tradicao') == 'pacto' and Q['gente']['eu'].get('divida') == W.PACTO_ABRE
    V = vila(); V['lugares']['mata'] = dict(nome='a Mata', em='na Mata', tipo='ermo', estoque={}, vizinhos=['vila'], bichos={'lobo': 2}, teto={'lobo': 10}); V['lugares']['vila']['vizinhos'] = ['mata']
    V['lugares']['longe'] = dict(nome='o Longe', em='no Longe', tipo='ermo', estoque={}); V['relogio']['bloco'] = 2
    nv = recusa(lambda: MM.laco(V, 'eu', 'longe')); MM.laco(V, 'eu', 'mata'); laco = V['gente']['eu'].get('tradicao') == 'verde' and MM.pena_laco(V, 'eu') == -4 + 2 * (MM.fartura(V, 'mata') >= 0.1)
    certo = lamina and pobreza and len(conta) == 1 and zera and claro and escuro and nv and laco and not estado.valida(E)
    return ('MG16 O VOTO, O LAÇO E A DÍVIDA: pôr em uso uma espada quebra o voto da lâmina (o voto fica quebrado, a Mana se apaga, fica a marca do juramento); o voto da pobreza leva ao santuário a prata '
            'acima de 50; a dívida acima de Vontade ÷ 10 vira maldição na virada e quebra quando zera; o pacto só no escuro; o laço só com ermo vizinho, e a fartura dele pesa',
            f"lâmina: {'quebrou, Mana 0, marca' if lamina else 'ERRADO'}; pobreza: {'40 de prata ao santuário, a prata fecha' if pobreza else 'ERRADO'}; a dívida de 5 com Vontade 40: "
            f"{len(conta)} maldição; paga até zerar: {'quebra' if zera else 'NÃO QUEBRA'}; o pacto de dia: {'recusado' if claro else 'ACEITO'}, de noite: {'feito' if escuro else 'NÃO'}; "
            f"o laço com ermo longe: {'recusado' if nv else 'ACEITO'}; com a mata (fartura {pc(MM.fartura(V, 'mata'))}): a força cai {MM.pena_laco(V, 'eu')}", certo)


# ---------- 17. as recusas ----------
def _recusas(n):
    """MG17 AS RECUSAS: o que não pode não acontece, e nada muda pela metade"""
    E = vila(prata=200); da(E, antídoto_0=1, fúria_0=1, veneno_0=1, cura_0=2, remédio=1); gente(E, 'ans', 'Anselmo', tradicao='arcano', feiticos=['seta'])
    gente(E, 'cle', 'Clériga', tradicao='fé', maestria={'fé': 4}, feiticos=['cura', 'bênção'], voto=dict(qual='socorro', santuario='vila', dia=1))
    antes = retrato(E)
    R = [recusa(lambda: alquimia.beber(E, 'eu', 'antídoto:0')), recusa(lambda: alquimia.beber(E, 'eu', 'fúria:0')), recusa(lambda: alquimia.beber(E, 'eu', 'veneno:0')),
         recusa(lambda: alquimia.beber(E, 'eu', 'remédio')), recusa(lambda: alquimia.beber(E, 'eu', 'quebra-maldição:0')), recusa(lambda: mercado.vender(E, 'eu', 'veneno:0', 1)),
         recusa(lambda: mercado.comprar(E, 'eu', 'veneno:0', 1)), recusa(lambda: alquimia.fazer(E, 'eu', 'veneno', 3)), recusa(lambda: alquimia.fazer(E, 'eu', 'cura', 0)),
         recusa(lambda: alquimia.lamina(E, 'eu', 'i0002')), recusa(lambda: MM.lancar(E, 'eu', 'seta')), recusa(lambda: MM.lancar(E, 'ans', 'seta')), recusa(lambda: MM.ler(E, 'eu', 'maldicao', 'ans')),
         recusa(lambda: MM.praga(E, 'eu', 'ans')), recusa(lambda: maldicao.rito(E, 'ans', 'eu')), recusa(lambda: encanto.gravar(E, 'eu', 'i0001', 'seta')), recusa(lambda: MM.estudar(E, 'eu', 'seta', {'com': 'eu'})),
         recusa(lambda: MM.tratar(E, 'eu', 'ans')), recusa(lambda: alquimia.beber(E, 'eu', 'cura:0')), recusa(lambda: MM.lancar(E, 'cle', 'cura', alvo='eu')),
         recusa(lambda: MM.lancar(E, 'cle', 'bênção', alvo='ans', paga_=3)), recusa(lambda: MM.lancar(E, 'cle', 'bênção', alvo='eu', paga_=-1))]
    cesta = mercado.vender_cesta(E, 'eu') if False else None
    F = vila(prata=10); da(F, cura_0=2, erva_0=3); r = mercado.vender_cesta(F, 'eu'); fica = (F['gente']['eu'].get('carga') or {}).get('cura:0') == 2 and not (F['gente']['eu'].get('carga') or {}).get('erva:0')
    certo = all(R) and retrato(E) == antes and fica
    return ('MG17 AS RECUSAS: beber o antídoto e a fúria fora da luta, o veneno, o remédio, o quebra-maldição sem maldição; negociar o veneno na loja; o veneno Épico; a leva sem matéria; o veneno em arma '
            'de impacto; lançar o que não sabe e o que só vale na luta; ler e rogar sem saber; o rito sem o feitiço; gravar sem mesa de runas; estudar consigo; tratar sem a mão; a poção e o feitiço '
            'de cura com o PV cheio; a paga de quem não é o personagem e a paga negativa: tudo recusado, nada '
            'muda; e o "vender tudo" não leva as poções',
            f"{sum(1 for x in R if x)} de {len(R)} recusados; o estado {'intacto' if retrato(E) == antes else 'MUDOU'}; vender tudo: as poções {'ficam' if fica else 'FORAM VENDIDAS'}", certo)


def provas(n=300):
    out = []
    for f in (_comum, _estudo, _mana, _maldicao_mata, _clerigo, _pocao_golpe, _teto, _erva_e_pocao, _alquimista_de_loja, _encantador_de_loja, _servico, _peca_e_lugar, _gravar, _mesa, _fecha, _tradicoes, _recusas):
        try:
            with contextlib.redirect_stdout(io.StringIO()): out.append(f(n))
        except SystemExit as e: out.append((f.__doc__.split(':')[0].strip(), f'QUEBROU (recusa no meio da prova): {e}', False))
        except Exception as e: out.append((f.__doc__.split(':')[0].strip(), f'QUEBROU ({type(e).__name__}: {e})', False))      # a meta que quebra fica falhando às claras, sem derrubar o banco do mundo
    return out


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    print('BANCO DE PROVAS DO MUNDO DA MAGIA\n')
    with pasta():
        res = provas(n)
    for nome, deu, passa in res: print(f"  {'passa' if passa else 'FALHA'}  {nome}: {deu}")
    print(f'\n{sum(p for _, _, p in res)} de {len(res)} provas passam.')
    return all(p for _, _, p in res)


if __name__ == '__main__':
    sys.exit(0 if main() else 1)
