#!/usr/bin/env python3
"""ato.py — MOTOR 10: O QUE A PESSOA FAZ, COM O TEMPO QUE CUSTA. Todo ato anda o relógio e mexe no corpo, por evento.

O ato longo PARA quando o corpo cruza um limiar (fome, sono, cansaço), e diz por quê. Quem cai no sono dorme ali mesmo, no chão.
O TEMPO PASSA PARA O PERSONAGEM, AJA QUEM AGIR: quando o relógio anda por ato de outra pessoa (quem=ID), o corpo do personagem passa os mesmos blocos, no mesmo evento,
como quem espera (a fome e o sono sobem); se ele cruza um limiar, o ato do outro para, e a mesa diz por quê. Não dobra quando ele já está no ato (vai junto na saída).
QUEM NÃO É O PERSONAGEM CUIDA DE SI QUANDO NÃO ESTÁ EM CENA: ao voltar a agir, o tempo que passou em casa é acertado antes de mais nada (estado.em_cena; corpo.casa).
QUEM MORREU NÃO AGE, e quem saiu para o ermo (a saída de caça ou de coleta aberta) não age na vila: o ato é recusado antes de cobrar qualquer coisa.
COM UMA LUTA ABERTA O MUNDO NÃO ANDA: até ela acabar (ou o Mestre a soltar), todo ato é recusado, de qualquer pessoa, fora os da própria luta.
DA ETAPA DA MAGIA: a maestria das armas sobe pelos blocos vezes o TALENTO, até o teto dele (talento.py); o foco e o amuleto se vestem (foco, pescoço);
cada bloco passa também pelos módulos que têm bloco() (a volta da Mana); vestir passa pelos que têm vestiu() (a peça maldita); a luta que volta ao estado leva
também a Mana, as poções e as doses gastas, os elixires, os encantos soltos, as maldições postas e as marcas.

Uso (o personagem do jogador, ou quem=ID):
  python3 ato.py comer [carga]            uma refeição do lugar (1 de prata; fome −3; não gasta bloco). `carga`: come 1 de comida da própria carga, sem pagar
                                          (quem está no ermo só come da carga; sem fome nenhuma, a refeição é recusada e nada é cobrado)
  python3 ato.py dormir N [chao]          N blocos de sono (a cama custa 2 de prata e vale um dia inteiro, 6 blocos, a contar do bloco em que se pagou, naquele lugar:
                                          dormir de novo nesse prazo não cobra; no chão é de graça e rende menos)
  python3 ato.py trabalhar N              N blocos no ofício da pessoa (o lugar paga por bloco, até a jornada: 2 blocos pagos por dia)
  python3 ato.py treinar N ARMA           N blocos de treino pesado com a arma (a maestria sobe pelos blocos)
  python3 ato.py descansar N              N blocos parado (o cansaço desce 1 por bloco)
  python3 ato.py esperar N                N blocos sem fazer nada
  python3 ato.py pecas                    as suas peças: o que está em uso e o que está na guarda
  python3 ato.py vestir ITEM [arma|arma2|escudo]    empunha ou veste uma peça sua (não gasta bloco); a que estava no lugar dela vai para a guarda
  python3 ato.py tirar ITEM               guarda uma peça que estava em uso
  python3 ato.py luta nova CENARIO.json ARQ.json      monta uma luta com gente do mundo ({"id": "..."} no cenário) e a hora do dia
                                          (ARQ.json só com o nome, sem pasta, fica na pasta do save, em lutas/: vai junto se o save mudar de lugar)
  python3 ato.py luta roda ARQ.json ["Nome: ordem"]...  roda até a próxima parada; no fim, a luta volta ao estado (PV, feridas, peças)
  python3 ato.py luta larga ARQ.json "por quê"        SÓ O MESTRE: dá por encerrada uma luta aberta cujo arquivo se perdeu (nada volta ao estado)
"""
import json, math, os, sys
import tabelas as T
import tabelas_mundo as M
import estado, corpo, talento
from itens import rotulo


def _vivo(E, pid):
    """a pessoa, se existe e vive, e se não há luta aberta no mundo; senão, a recusa com a frase"""
    p = E['gente'].get(pid) or sys.exit(f'não há a pessoa "{pid}"')
    if p['estado'] != 'vivo': sys.exit(f"{p['nome']} não age: {estado.morte_diz(E, p)}")
    estado.sem_luta(E)
    estado.em_cena(E, pid)                                  # quem não é o personagem e volta a agir: antes de mais nada, o descanso em casa
    return E['gente'][pid]


def espera(E, pid, com=()):
    """o personagem do jogador, se o ato é de OUTRA pessoa, ele não está nesse ato (nem age, nem vai junto) e está vivo: o tempo passa para ele também, como quem espera.
    Senão (o ato é dele, ele vai junto, ou morreu), None."""
    eu = estado.eu(E)
    return eu if eu and eu != pid and eu not in com and E['gente'][eu]['estado'] == 'vivo' else None


def passa(E, pid, blocos, tipo, esforco='nada', dorme=None, texto='', mais=None, para=True, com=()):
    """anda o mundo `blocos` blocos com a pessoa fazendo isto: um evento por bloco. Devolve (blocos feitos, por que parou ou None).
    com: quem vai junto (a saída ao ermo): passa os mesmos blocos, com o mesmo esforço, no mesmo evento.
    O TEMPO PASSA PARA O PERSONAGEM, AJA QUEM AGIR: se o ato é de outra pessoa e o personagem não está nele, o corpo dele passa os mesmos blocos, no mesmo evento, como quem
    espera (esforço `nada`); as paradas do corpo valem para ele também.
    Com `para`, o ato para quando o corpo cruza um limiar; e quem cai no sono (sono 8 ou mais, Vontade falhada) dorme ali mesmo, no chão, até o sono baixar do primeiro limiar."""
    feitos = 0; porque = None
    if blocos > 0:
        estado.sem_luta(E)                                  # com uma luta aberta, o relógio não anda
        for q in [pid] + [c for c in com if c != pid]: estado.em_cena(E, q)      # quem não é o personagem e volta a agir: antes de mais nada, o descanso em casa
    for i in range(blocos):
        p = E['gente'][pid]
        if p['estado'] != 'vivo': porque = f"{p['nome']} morreu"; break
        junto = [c for c in com if c != pid and E['gente'].get(c, {}).get('estado') == 'vivo']
        ve = espera(E, pid, junto); todos = [pid] + junto + ([ve] if ve else [])     # ve: o personagem, que espera enquanto outro age
        antes = corpo.faixas(p); antes_ve = corpo.faixas(E['gente'][ve]) if ve else None
        ultimo = E['relogio']['bloco'] == M.BLOCOS_DIA - 1; lid = estado.onde(E, pid)
        ef = corpo.bloco(E, pid, esforco, dorme) + _bloco_dos_modulos(E, pid, esforco, dorme)
        for c in junto: ef += corpo.bloco(E, c, esforco, dorme) + _bloco_dos_modulos(E, c, esforco, dorme)
        if ve: ef += corpo.bloco(E, ve, 'nada') + _bloco_dos_modulos(E, ve, 'nada', None)
        ef += (mais(i) if mais else [])
        if not ultimo: estado.aplica(E, tipo, ef + [['relogio', 1]], onde=lid, quem=[pid] + junto, texto=texto)
        else:                                               # o último bloco do dia: o bloco, e depois a virada (com o relógio)
            if ef: estado.aplica(E, tipo, ef, onde=lid, quem=[pid] + junto, texto=texto)
            vir = []
            for c in todos: vir += corpo.virada(E, c)
            estado.aplica(E, 'virada', vir + [['relogio', 1]], onde=lid, quem=[pid] + junto, texto='o dia vira')
            _mundo_vira(E)
        feitos += 1
        for q in todos:
            x = E['gente'][q]
            if x['estado'] == 'vivo' and x['pv'] <= 0:
                estado.aplica(E, 'virada', [['pessoa', q, 'estado', 'poe', 'morto']], onde=estado.onde(E, q), quem=[q], texto=f"a fome leva {x['nome']}")
        p = E['gente'][pid]
        if p['estado'] != 'vivo': porque = f"{p['nome']} morreu de fome"; break
        porque = corpo.cruzou(p, antes)
        if dorme and p['corpo']['sono'] == 0 and p['corpo']['cansaco'] == 0 and p['pv'] >= estado.pv_max(p): porque = porque or f"{p['nome']} acorda com o sono em dia"
        if not dorme and p['corpo']['sono'] >= M.SONO_CAI[0]:
            r = estado.sorte(E, f'sono|{pid}'); t = r.randint(1, 20) + r.randint(1, 20) + p['atributos']['Vontade'] // 10
            if t < M.SONO_CAI[1] and para:
                n = math.ceil((p['corpo']['sono'] - (M.LIMIARES['sono'][0] - 1)) / -M.SONO_CHAO)
                k, _ = passa(E, pid, n, 'dormir', dorme='chao', texto=f"{p['nome']} cai no sono e dorme no chão", para=False, com=com)
                porque = f"{p['nome']} cai no sono onde está (Vontade {t} contra {M.SONO_CAI[1]}) e dorme {estado.tantos(k, 'bloco')} no chão"; break
        if ve:                                              # quem espera: o corpo dele cobra igual, e o ato do outro para
            x = E['gente'][ve]; pq = None
            if x['estado'] != 'vivo': pq = f"{x['nome']}, que esperava, morreu de fome"
            else:
                c = corpo.cruzou(x, antes_ve)
                if c: pq = f"{c} (esperava: o tempo passa também para quem espera)"
                if para and x['corpo']['sono'] >= M.SONO_CAI[0]:
                    r = estado.sorte(E, f'sono|{ve}'); t = r.randint(1, 20) + r.randint(1, 20) + x['atributos']['Vontade'] // 10
                    if t < M.SONO_CAI[1]:
                        n = math.ceil((x['corpo']['sono'] - (M.LIMIARES['sono'][0] - 1)) / -M.SONO_CHAO)
                        k, _ = passa(E, ve, n, 'dormir', dorme='chao', texto=f"{x['nome']} cai no sono e dorme no chão", para=False)
                        porque = ' · '.join(y for y in (porque, f"{x['nome']}, que esperava, cai no sono onde está (Vontade {t} contra {M.SONO_CAI[1]}) e dorme {estado.tantos(k, 'bloco')} no chão") if y); break
            if pq: porque = ' · '.join(y for y in (porque, pq) if y)
        if porque and para: break
    return feitos, porque


def _bloco_dos_modulos(E, pid, esforco, dorme):
    """os efeitos de UM bloco que os módulos do mundo põem em quem age, vai junto ou espera (a volta da Mana fora da luta: a frente do mundo da magia)"""
    return [x for mod in estado.modulos('bloco') for x in (mod.bloco(E, pid, esforco, dorme) or [])]


def _mundo_vira(E):
    """o dia virou: cada módulo do mundo que tiver virada(E) roda a sua parte (o mercado produz e consome, os bichos criam, a maldição anda...)"""
    for mod in estado.modulos('virada'): mod.virada(E)


def comer(E, pid, da_carga=False):
    """uma refeição: a do lugar (paga, sai do celeiro dele), ou 1 de comida da própria carga (sem pagar). Quem está no ermo só come da carga."""
    p = _vivo(E, pid); f = estado.fora(E, pid)
    if p['corpo']['fome'] <= 0: sys.exit(f"{p['nome']} não tem fome (fome 0): a refeição não mudaria nada. Nada foi cobrado.")
    if da_carga or f:
        if p.get('carga', {}).get('comida', 0) < 1: sys.exit(f"{p['nome']} não carrega comida" + (f" (e {estado.em(E, f)} não há quem sirva)" if f else ' (a refeição do lugar: `ato.py comer`)'))
        estado.aplica(E, 'comer', [['pessoa', pid, 'carga.comida', 'soma', -1], ['pessoa', pid, 'fome', 'soma', M.REFEICAO]], onde=estado.onde(E, pid), quem=[pid], texto=f"{p['nome']} come da própria carga")
        q = E['gente'][pid]; sobra = q.get('carga', {}).get('comida', 0)
        return f"{p['nome']} come da própria carga (fome {q['corpo']['fome']}; {'resta' if sobra == 1 else 'restam'} {sobra:g} de comida)"
    l = E['lugares'][p['lugar']]
    if l['estoque'].get('comida', 0) < 1: sys.exit(f"não há comida {estado.em(E, p['lugar'])}: ninguém serve refeição" + (' (você carrega comida: `ato.py comer carga`)' if p.get('carga', {}).get('comida', 0) >= 1 else ''))
    if p['moedas'] < M.REFEICAO_PRECO: sys.exit(f"a refeição custa {M.REFEICAO_PRECO} de prata; {p['nome']} tem {p['moedas']}" + (' (você carrega comida: `ato.py comer carga`)' if p.get('carga', {}).get('comida', 0) >= 1 else ''))
    estado.aplica(E, 'comer', [['pessoa', pid, 'moedas', 'soma', -M.REFEICAO_PRECO], ['estoque', p['lugar'], 'comida', 'soma', -1], ['estoque', p['lugar'], 'prata', 'soma', M.REFEICAO_PRECO],
                               ['pessoa', pid, 'fome', 'soma', M.REFEICAO]], onde=p['lugar'], quem=[pid], texto=f"{p['nome']} come {estado.em(E, p['lugar'])}")
    return f"{p['nome']} come (fome {E['gente'][pid]['corpo']['fome']}; {E['gente'][pid]['moedas']} de prata)"


def cama_paga(E, pid):
    """até que bloco (contado desde o começo do mundo, como o estado.agora) a cama desta pessoa está paga NO LUGAR ONDE ELA ESTÁ; 0 se não está paga, ou se o prazo venceu"""
    p = E['gente'][pid]; c = (p.get('marca') or {}).get('cama')
    return c['ate'] if isinstance(c, dict) and c.get('onde') == p['lugar'] and isinstance(c.get('ate'), int) and c['ate'] > estado.agora(E) else 0


def cama_diz(E, pid):
    """até quando a cama está paga, em palavras ("paga até o Dia 2, manhã (8h)"), ou None"""
    ate = cama_paga(E, pid)
    return f"paga até o Dia {ate // M.BLOCOS_DIA + 1}, {M.BLOCOS[ate % M.BLOCOS_DIA]} ({ate % M.BLOCOS_DIA * M.BLOCO_HORAS}h)" if ate else None


def dormir(E, pid, blocos, chao=False, para=True):
    """N blocos de sono. NA CAMA PAGA-SE A NOITE, não a deitada: a cama paga vale CAMA_VALE blocos (um dia inteiro) a contar do bloco em que se pagou, no lugar onde
    se pagou. Dormir de novo nesse prazo não cobra; o sono que passa do prazo paga outra noite, e sem prata para ela o sono para ali."""
    p = estado.presente(E, pid, 'dormir na vila'); lid = p['lugar']; l = E['lugares'][lid]
    if chao or not l.get('cama'):
        n, pq = passa(E, pid, blocos, 'dormir', dorme='chao', texto=f"{p['nome']} dorme (no chão)", para=para)
        return f"{p['nome']} dorme {estado.tantos(n, 'bloco')} no chão" + (f'. PAROU: {pq}' if pq else '')
    feitos = 0; pq = None; pagou = 0
    while feitos < blocos:
        p = E['gente'][pid]
        if not cama_paga(E, pid):
            if p['moedas'] < M.CAMA_PRECO:
                if not feitos: sys.exit(f"a cama custa {M.CAMA_PRECO} de prata; {p['nome']} tem {p['moedas']}. No chão é de graça: `ato.py dormir N chao`")
                pq = f"a cama paga venceu, e {p['nome']} não tem {M.CAMA_PRECO} de prata para outra noite (no chão é de graça: `ato.py dormir N chao`)"; break
            estado.aplica(E, 'dormir', [['pessoa', pid, 'moedas', 'soma', -M.CAMA_PRECO], ['estoque', lid, 'prata', 'soma', M.CAMA_PRECO],
                                        ['pessoa', pid, 'marca.cama', 'poe', dict(ate=estado.agora(E) + M.CAMA_VALE, onde=lid)]], onde=lid, quem=[pid], texto=f"{p['nome']} paga a cama")
            pagou += M.CAMA_PRECO
        pede = min(blocos - feitos, cama_paga(E, pid) - estado.agora(E))
        n, pq = passa(E, pid, pede, 'dormir', dorme='cama', texto=f"{p['nome']} dorme (na cama)", para=para)
        feitos += n
        if n < pede or (pq and para) or E['gente'][pid]['estado'] != 'vivo': break
    c = cama_diz(E, pid) if E['gente'][pid]['estado'] == 'vivo' else None
    cama = (f"pagou {pagou} de prata pela cama" + (f', {c}' if c else '')) if pagou else ('a cama já estava ' + (c or 'paga'))
    return f"{p['nome']} dorme {estado.tantos(feitos, 'bloco')} na cama ({cama})" + (f'. PAROU: {pq}' if pq else '')


def jornada(E, pid):
    """quantos blocos de serviço PAGO a pessoa já fez hoje (trabalhar e o jornal da oficina contam juntos; o teto é tabelas_mundo.JORNADA)"""
    m = E['gente'][pid].get('marca') or {}
    return m.get('jornada', 0) if m.get('jornada_dia') == E['relogio']['dia'] else 0


def paga_bloco(E, pid, lid, paga):
    """os efeitos de UM bloco de serviço pago pelo lugar: a prata passa do lugar para a pessoa, e o bloco conta na jornada do dia"""
    return [['estoque', lid, 'prata', 'soma', -paga], ['pessoa', pid, 'moedas', 'soma', paga],
            ['pessoa', pid, 'marca.jornada_dia', 'poe', E['relogio']['dia']], ['pessoa', pid, 'marca.jornada', 'poe', jornada(E, pid) + 1]]


def trabalhar(E, pid, blocos):
    """N blocos no ofício da pessoa. O lugar paga por bloco, até a JORNADA do dia (2 blocos pagos por pessoa, por dia); sem prata, o lugar não tem com que pagar."""
    p = estado.presente(E, pid, 'trabalhar na vila'); lid = p['lugar']; of = p.get('grau_oficio', 'diarista'); paga = M.SALARIO[of]; feitos = 0; pq = None
    for _ in range(blocos):
        if jornada(E, pid) >= M.JORNADA: pq = f"a jornada de hoje acabou ({M.JORNADA} blocos pagos por dia): {E['lugares'][lid]['nome']} não tem mais serviço para {p['nome']} hoje"
        elif E['lugares'][lid]['estoque'].get('prata', 0) < paga: pq = f"{E['lugares'][lid]['nome']} não tem prata para pagar o serviço ({paga} por bloco; tem {E['lugares'][lid]['estoque'].get('prata', 0)})"
        if pq: break
        n, pq = passa(E, pid, 1, 'trabalhar', esforco=M.ESFORCO_OFICIO[of], mais=lambda i: paga_bloco(E, pid, lid, paga), texto=f"{p['nome']} trabalha ({of})")
        feitos += n
        if pq: break
    if not feitos and pq: sys.exit(pq[0].upper() + pq[1:] + '.')
    return f"{p['nome']} trabalha {estado.tantos(feitos, 'bloco')} e recebe {feitos * paga} de prata" + (f'. PAROU: {pq}' if pq else '')


def treinar(E, pid, blocos, arma):
    if arma not in T.FAMILIAS: sys.exit(f'arma desconhecida: "{arma}" (use: {", ".join(T.FAMILIAS)})')
    p = estado.presente(E, pid, 'treinar na vila')
    n, pq = passa(E, pid, blocos, 'treinar', esforco='pesado', mais=lambda i: [['pessoa', pid, 'treino.' + arma, 'soma', 1]], texto=f"{p['nome']} treina com {arma}")
    return f"{p['nome']} treina {estado.tantos(n, 'bloco')} com {arma}" + _sobe_maestria(E, pid, arma) + (f'. PAROU: {pq}' if pq else '')


def _sobe_maestria(E, pid, arma):
    """a maestria sobe quando os blocos chegam; de Mestre para cima, só com um FEITO registrado (marca.feito_ARMA)"""
    p = E['gente'][pid]; tem = p.get('maestria', {}).get(arma, 0); blocos = p.get('treino', {}).get(arma, 0); txt = ''
    for grau in sorted(M.MAESTRIA_BLOCOS):
        pede = talento.pede(p, arma, M.MAESTRIA_BLOCOS, grau)                # os blocos vezes o talento da mão desta arma
        if grau <= tem: continue
        if pede is None:
            if blocos >= M.MAESTRIA_BLOCOS[grau]: txt = f' (a mão não sobe mais em {arma}: o talento para em {T.MAESTRIAS[talento.teto(p, arma)]})'
            break
        if blocos < pede: continue
        if grau >= M.MAESTRIA_FEITO and p.get('marca', {}).get(f'feito_{arma}', 0) < grau: txt = f' (tem os blocos para {T.MAESTRIAS[grau]}; falta o feito)'; break
        estado.aplica(E, 'treinar', [['pessoa', pid, 'maestria.' + arma, 'poe', grau]], onde=p['lugar'], quem=[pid], texto=f"{p['nome']} chega a {T.MAESTRIAS[grau]} em {arma}")
        tem = grau; txt = f'. MAESTRIA: {T.MAESTRIAS[grau]} em {arma}'
    return txt


def descansar(E, pid, blocos):
    estado.presente(E, pid, 'descansar na vila')
    n, pq = passa(E, pid, blocos, 'descansar', esforco='descanso', texto=f"{E['gente'][pid]['nome']} descansa"); return f"{E['gente'][pid]['nome']} descansa {estado.tantos(n, 'bloco')}" + (f'. PAROU: {pq}' if pq else '')


def esperar(E, pid, blocos):
    estado.presente(E, pid, 'esperar na vila')
    n, pq = passa(E, pid, blocos, 'esperar', texto=f"{E['gente'][pid]['nome']} espera"); return f"{E['gente'][pid]['nome']} espera {estado.tantos(n, 'bloco')}" + (f'. PAROU: {pq}' if pq else '')


# ---------- vestir, empunhar, guardar ----------
USO_DO_TIPO = dict(arma='arma', escudo='escudo', armadura='veste', foco='foco', amuleto='pescoco')
USO_DIZ = dict(arma='na mão', arma2='de reserva', escudo='no braço', veste='no corpo', foco='na mão, para lançar', pescoco='no pescoço')       # o nome da peça pode ser masculino ou feminino: estas palavras servem aos dois


def uso_diz(it, uso=None):
    """onde a peça está em uso, em palavras: na mão, de reserva, no braço, no corpo; o elmo (a armadura que só cobre a cabeça), na cabeça"""
    uso = uso or it.get('uso')
    return 'na cabeça' if uso == 'veste' and list(it.get('cobre') or []) == ['cabeça'] else USO_DIZ.get(uso, uso)


def diz_pecas(E, pid):
    """as peças da pessoa, uma linha cada: o que está em uso (e onde) e o que está guardado; e os núcleos"""
    L = []
    for i, it in E['itens']['itens'].items():
        if it.get('dono') != pid: continue
        if it['tipo'] == 'nucleo': L.append(f"{i} {rotulo(it)} · núcleo, na guarda"); continue
        import itens as _IT
        efs = [_IT.EFEITOS[e['chave']][0].format(valor=e.get('valor', '')) for e in it.get('efeitos') or [] if isinstance(e, dict) and e.get('chave') in _IT.EFEITOS]      # (a etapa dos efeitos) o que a peça faz
        livre = f"OBRA-PRIMA: {it['efeitos_livres']} efeito{'s' if it['efeitos_livres'] > 1 else ''} por escolher (`oficio.py efeito {i} CHAVE`)" if it.get('efeitos_livres') else ''
        onde = 'ferramenta, na carga' if it['tipo'] == 'ferramenta' else ('EM USO, ' + uso_diz(it) if it.get('uso') else 'na guarda')
        L.append(f"{i} {rotulo(it, str(it['dur'][0]) + '/' + str(it['dur'][1]), 'QUEBROU' if it['dur'][0] <= 0 else '')} · {onde}" + ''.join(f' · {x}' for x in efs) + (f' · {livre}' if livre else ''))
    return L or ['(nenhuma peça)']


def presa_diz(E, pid, it):
    """a peça maldita não sai de uso enquanto a maldição que veio dela anda no dono (estado._presa): a frase simples que vai à mesa, ou None (a peça sai)"""
    if not estado._presa(E, it): return None
    p = E['gente'][pid]
    return (f"A mão de {p['nome']} não larga {it['nome']}" if it.get('uso') in ('arma', 'foco') else f"{p['nome']} não consegue tirar {it['nome']}") + ': há algo de errado nessa peça.'


def vestir(E, pid, iid, uso=None):
    """empunha ou veste uma peça da pessoa (não gasta bloco). A que estava no mesmo lugar (a outra arma, o outro escudo, a armadura que cobre a mesma parte) vai para a guarda."""
    p = _vivo(E, pid); it = E['itens']['itens'].get(iid) or sys.exit(f'não há o item "{iid}" no Livro de Itens')
    if it.get('dono') != pid: sys.exit(f"{it['nome']} ({iid}) não é de {p['nome']}")
    if it['tipo'] not in USO_DO_TIPO: sys.exit(f"{it['nome']} não se veste nem se empunha")
    uso = uso or USO_DO_TIPO[it['tipo']]
    if uso not in estado.PARTES_VESTE or estado.USO_DO_TIPO[uso] != it['tipo']:
        sys.exit(f"{it['nome']} é {it['tipo']}: vai em " + ('arma (na mão) ou arma2 (de reserva)' if it['tipo'] == 'arma' else USO_DO_TIPO[it['tipo']]) + f' (veio "{uso}")')
    if it.get('uso') == uso: sys.exit(f"{it['nome']} já está em uso ({uso_diz(it, uso)})")
    eq = estado.pecas(E, pid); saem = []
    if uso != 'veste' and eq[uso] and eq[uso]['id'] != iid: saem.append(eq[uso])
    if uso == 'veste': saem += [o for o in eq['veste'] if o['id'] != iid and set(o.get('cobre') or []) & set(it.get('cobre') or [])]
    for o in ([it] if it.get('uso') else []) + saem:         # a peça maldita presa não muda de lugar nem dá lugar a outra (antes de montar o evento, em palavras simples)
        if presa_diz(E, pid, o): sys.exit(presa_diz(E, pid, o) + ('' if o is it else f" {it['nome']} não entra no lugar dela."))
    for mod in estado.modulos('pode_vestir'):              # ANTES de montar o evento (etapa 4b): o que os módulos recusam (a armadura de outro corpo), em palavras simples
        t = mod.pode_vestir(E, pid, iid)
        if t: sys.exit(t)
    ef = [['item', o['id'], 'uso', 'poe', None] for o in saem] + [['item', iid, 'uso', 'poe', uso]]
    verbo = 'veste' if uso == 'veste' else 'põe' if uso == 'pescoco' else 'empunha'
    estado.aplica(E, 'vestir', ef, onde=estado.onde(E, pid), quem=[pid], texto=f"{p['nome']} {verbo} {it['nome']}" + (f" (guarda {', '.join(o['nome'] for o in saem)})" if saem else ''))
    aviso = ''
    arma = estado.pecas(E, pid)['arma']
    if arma and T.FAMILIAS[arma['familia']]['maos'] == 2 and estado.pecas(E, pid)['escudo']: aviso = f"\nAVISO: {arma['nome']} pede as duas mãos: o escudo não entra na conta enquanto ela estiver na mão."
    for mod in estado.modulos('vestiu'):                    # depois de pôr a peça em uso: o que os módulos do mundo fazem com isso (a peça maldita)
        t = mod.vestiu(E, pid, iid)
        if t: aviso += '\n' + t
    return f"{p['nome']} {verbo} {it['nome']} ({uso_diz(it, uso)})" + (f"; vai para a guarda: {', '.join(o['nome'] for o in saem)}" if saem else '') + '.' + aviso + '\n' + _ficha(E, pid)


def tirar(E, pid, iid):
    """guarda uma peça que estava em uso (não gasta bloco)"""
    p = _vivo(E, pid); it = E['itens']['itens'].get(iid) or sys.exit(f'não há o item "{iid}" no Livro de Itens')
    if it.get('dono') != pid: sys.exit(f"{it['nome']} ({iid}) não é de {p['nome']}")
    if not it.get('uso'): sys.exit(f"{it['nome']} já está na guarda")
    if presa_diz(E, pid, it): sys.exit(presa_diz(E, pid, it))
    estado.aplica(E, 'vestir', [['item', iid, 'uso', 'poe', None]], onde=estado.onde(E, pid), quem=[pid], texto=f"{p['nome']} guarda {it['nome']}")
    return f"{p['nome']} guarda {it['nome']}.\n" + _ficha(E, pid)


def _ficha(E, pid):
    import pessoas
    return pessoas.linha(pessoas.ficha(estado.lutador(E, pid, visivel=True)))       # a ficha que vai à mesa: só o dom que a pessoa já viu


# ---------- a luta dentro do mundo ----------
def _arq_luta(arq):
    """o caminho de verdade de um arquivo de luta: como veio, ou dentro da pasta do save (é assim que o save o guarda), ou em lutas/ dentro dela (onde fica a luta aberta só com o nome)"""
    achados = [c for c in dict.fromkeys([arq, estado.arq_abre(arq)] + ([os.path.join(estado.pasta(), 'lutas', arq)] if not os.path.dirname(arq) else [])) if os.path.exists(c)]
    for c in achados:                                       # o primeiro que É uma luta (um cenário com o mesmo nome, na pasta do save, não é)
        try: S = json.load(open(c, encoding='utf-8'))
        except (ValueError, OSError): continue
        if isinstance(S, dict) and 'fim' in S and 'L' in S: return c
    if achados: sys.exit(f'"{arq}" não é um arquivo de luta (é o cenário? A luta aberta fica em lutas/, na pasta do save: {", ".join(l["arq"] for l in estado.carrega()["turno"]["lutas"] if not l["fim"]) or "nenhuma aberta"})')
    sys.exit(f'não há o arquivo de luta "{arq}" (nem na pasta do save, {estado.pasta()}). Se ele se perdeu: `ato.py luta larga {arq} "por quê"`')


def arq_da_luta_nova(arq):
    """onde fica guardado o arquivo de uma luta nova. Só o nome, sem pasta: na pasta do save, em lutas/ (criada se faltar), como as lutas da caça; assim a luta vai junto se o save
    mudar de lugar. Com pasta: é o caminho que veio, e a pasta tem de existir (senão, a recusa é uma frase, antes de qualquer dado)."""
    if not os.path.dirname(arq):
        d = os.path.join(estado.pasta(), 'lutas'); os.makedirs(d, exist_ok=True); return os.path.join(d, arq)
    if not os.path.isdir(os.path.dirname(os.path.abspath(arq))):
        sys.exit(f'a pasta "{os.path.dirname(arq)}" não existe: a luta não foi aberta. Diga só o nome do arquivo (`ato.py luta nova CENARIO.json {os.path.basename(arq)}`) e ele fica na pasta do save, em lutas/.')
    return arq


def luta_nova(E, arq_cenario, arq_luta):
    """monta a luta: quem tem "id" no cenário vem do estado (o que veste hoje, o PV, as feridas, a pena do corpo); de noite, fica escuro"""
    import luta
    from pessoas import padrao, veste
    from itens import cat_i
    estado.sem_luta(E)                                      # uma luta de cada vez: com uma aberta, não se abre outra
    if not os.path.exists(arq_cenario): sys.exit(f'não há o cenário "{arq_cenario}"')
    arq_luta = arq_da_luta_nova(arq_luta)
    try: C = json.load(open(arq_cenario, encoding='utf-8'))
    except ValueError as x: sys.exit(f'o cenário "{arq_cenario}" não é JSON: {x}')
    if not isinstance(C, dict) or not isinstance(C.get('A'), list) or not isinstance(C.get('B'), list) or not C['A'] or not C['B']: sys.exit('o cenário pede os dois lados: "A": [...] e "B": [...], cada um com alguém')
    def peca(x, tipo):
        if x is None or x is False: return x
        return cat_i(x) if tipo == 'escudo' else (x[0], cat_i(x[1]))
    def pessoa(d):
        if not isinstance(d, dict): sys.exit(f'cada lutador do cenário é um registro {{...}} (veio {json.dumps(d, ensure_ascii=False)})')
        d = dict(d)
        if 'id' in d:
            pid = d.pop('id')
            if pid not in E['gente']: sys.exit(f'não há a pessoa "{pid}" no mundo')
            if E['gente'][pid]['estado'] != 'vivo': sys.exit(f'{E["gente"][pid]["nome"]} não entra na luta: {estado.morte_diz(E, E["gente"][pid])}')
            estado.em_cena(E, pid)                          # quem não é o personagem e entra numa luta: antes de mais nada, o descanso em casa
            return estado.lutador(E, pid, **d)
        if isinstance(d.get('bicho'), str):                 # o atalho do bicho: a espécie inteira sai da tabela (o nível, se vier, não conta)
            import bichos
            esp = d.pop('bicho'); d.pop('nivel', None); return bichos.bicho(esp, **d)
        if 'nome' not in d or 'nivel' not in d: sys.exit(f'quem não vem do mundo ("id") nem é bicho ("bicho") pede "nome" e "nivel" (veio {json.dumps(d, ensure_ascii=False)[:80]})')
        v = d.pop('veste', {})
        if not isinstance(v, dict): sys.exit(f'{d.get("nome")}: "veste" é um registro {{"arma": ..., "armadura": ...}}')
        ruins = [k for k in v if k not in ('arma', 'arma2', 'armadura', 'elmo', 'escudo', 'foco', 'amuleto')]
        if ruins: sys.exit(f'{d.get("nome")}: não sei vestir "{ruins[0]}" (use: arma, arma2, armadura, elmo, escudo, foco, amuleto)')
        p = padrao(d.pop('nome'), d.pop('nivel'), molde=d.pop('molde', 'guerreiro'), maestria=d.pop('maestria', None), atributos=d.pop('atributos', None), **d)
        return veste(p, arma=peca(v.get('arma'), 'arma'), arma2=peca(v.get('arma2'), 'arma'), armadura=peca(v.get('armadura'), 'armadura'), elmo=peca(v.get('elmo'), 'armadura'), escudo=peca(v.get('escudo'), 'escudo'),
                     foco=peca(v.get('foco'), 'foco'), amuleto=peca(v.get('amuleto'), 'escudo'))      # o foco: ["cajado", "Raro"]; o amuleto: "Raro"
    tempo = list(C.get('tempo') or [])
    if E['relogio']['bloco'] in M.ESCUROS and not C.get('luz') and 'escuro' not in tempo: tempo.append('escuro')
    S = luta.nova([pessoa(x) for x in C['A']], [pessoa(x) for x in C['B']], inicio=C.get('inicio', 'perto'), lugar=C.get('lugar'), tempo=tempo, surpresa=C.get('surpresa'), ermo=_ermo_da_luta(E, C))
    S['mundo'] = True; S['comecou'] = True; luta.salva(S, arq_luta)
    E['turno']['lutas'].append(dict(arq=estado.arq_guarda(arq_luta), fim=None)); estado.grava(E)
    return luta.situacao(S)


def _ermo_da_luta(E, C):
    """as espécies do ermo onde a luta é (o feitiço "chamar" só vale num ermo contado): o "ermo" do cenário, ou o lugar de quem vem do mundo, se for um ermo com bichos"""
    lid = C.get('ermo') or next((E['gente'][x['id']]['lugar'] for x in C['A'] + C['B'] if isinstance(x, dict) and x.get('id') in E['gente']), None)
    l = E['lugares'].get(lid) if isinstance(lid, str) else None
    if not isinstance(l, dict) or not isinstance(l.get('bichos'), dict): return None
    return sorted(e for e, q in l['bichos'].items() if isinstance(q, (int, float)) and q >= 1 and estado.especie(e)) or None


def luta_roda(E, arq_luta, ordens):
    import luta
    arq_luta = _arq_luta(arq_luta); S = json.load(open(arq_luta, encoding='utf-8'))
    if S['fim']:
        if any(l['arq'] == estado.arq_guarda(arq_luta) and not l['fim'] for l in E['turno']['lutas']):       # acabou no arquivo e ainda não voltou ao estado (o comando foi cortado no meio): volta agora
            return 'Esta luta já tinha acabado: ' + luta.resultado_diz(S) + '\n' + luta_fecha(E, S, arq_luta)
        sys.exit('esta luta já acabou.')
    for o in ordens: luta.ordem(S, o)
    S['log'] = []; fim = luta.corre(S, interativo=True); luta.salva(S, arq_luta)
    out = '\n'.join(S['log']) + '\n\n' + luta.situacao(S)
    if fim == 'fim': out += '\n\nFIM: ' + luta.resultado_diz(S) + '\n' + luta_fecha(E, S, arq_luta)
    return out


def luta_fecha(E, S, arq_luta=None):
    """a luta acabada volta ao estado, num evento só: PV, feridas novas, mortes, o cansaço, a durabilidade das peças"""
    ef = []; quem = []; linhas = []
    for f in S['L']:
        pid = f.get('id')
        if not pid or pid not in E['gente']: continue
        p = E['gente'][pid]; quem.append(pid); morto = f['estado'] == 'morto'
        pv = 0 if morto else max(1, f['pv'])               # quem caiu e foi estancado fica com 1
        if pv != p['pv']: ef.append(['pessoa', pid, 'pv', 'soma', pv - p['pv']])
        for parte, grave in f['feridas'][f['feridas_antes']:]: ef.append(['ferida', pid, 'abre', parte, grave])
        mg = _magia_volta(E, pid, p, f, pv); ef += mg                 # a etapa da magia: a Mana, as poções, os elixires, os encantos, as maldições postas, as marcas (antes da morte)
        if morto: ef.append(['pessoa', pid, 'estado', 'poe', 'morto'])
        else: ef += [['pessoa', pid, 'cansaco', 'soma', M.LUTA_CANSA], ['pessoa', pid, 'marca.luta_dia', 'poe', E['relogio']['dia']]]       # o dia em que a pessoa lutou não é dia de repouso (corpo.repousou)
        novas = len(f['feridas']) - f['feridas_antes']
        mana_txt = next((f", Mana {min(x[4], estado.mana_max(p, True))} de {estado.mana_max(p, True)}" for x in mg if x[:3] == ['pessoa', pid, 'mana']), '') if not morto else ''       # a conta que vai à mesa: sem o dom que a pessoa não viu
        linhas.append(f"  {p['nome']}: {'MORREU' if morto else f'PV {pv}'}" + (f", {estado.tantos(novas, 'ferida nova', 'feridas novas')}" if novas > 0 else '') + mana_txt)
    for it in S['itens'].values():
        iid = it.get('id')
        if iid in E['itens']['itens'] and it['dur'][0] != E['itens']['itens'][iid]['dur'][0]:
            ef.append(['item', iid, 'dur', 'soma', it['dur'][0] - E['itens']['itens'][iid]['dur'][0]])
            if it['dur'][0] <= 0: linhas.append(f"  {it['nome']} QUEBROU")
    antes = {pid: corpo.faixas(E['gente'][pid]) for pid in quem}
    import luta
    if ef: estado.aplica(E, 'luta', ef, onde=estado.onde(E, quem[0]) if quem else None, quem=quem, texto='luta: ' + luta.resultado_diz(S).split(' · feridas')[0])
    for pid in quem:
        c = corpo.cruzou(E['gente'][pid], antes[pid]) if E['gente'][pid]['estado'] == 'vivo' else None
        if c: linhas.append(f"  {c} (a luta cansa)")
    for l in E['turno']['lutas']:
        if arq_luta and l['arq'] == estado.arq_guarda(arq_luta): l['fim'] = S['fim']
    return 'A LUTA VOLTOU AO ESTADO:\n' + '\n'.join(linhas)


def _magia_volta(E, pid, p, f, pv):
    """o que a luta de magia devolve ao estado de quem tem id no mundo (o contrato, seção 10). O que não mudou não gera efeito: a luta sem magia volta igual a hoje."""
    ef = []; L = E['itens']['itens']
    if f.get('mana') is not None and f.get('mana_max') is not None:
        m = max(0, min(estado.mana_max(p), int(round(f['mana']))))
        if m != estado.mana(p): ef.append(['pessoa', pid, 'mana', 'poe', m])
    for b, n in (f.get('gastou') or {}).items():                         # a poção bebida, a dose de veneno: sai da carga
        if n: ef.append(['pessoa', pid, 'carga.' + b, 'soma', -int(n)])
    ef += [['item', i, 'some'] for i in f.get('elixires_gastos') or [] if L.get(i, {}).get('dono') == pid and L[i].get('tipo') == 'elixir']
    ef += [['item', i, 'veneno', 'poe', None] for i in f.get('venenos_gastos') or [] if L.get(i, {}).get('veneno')]
    ef += [['item', i, 'encanto', 'gasta', k] for i, k in f.get('encantos_gastos') or [] if i in L]
    ef += [['maldicao', pid, 'poe', r] for r in f.get('maldicoes_postas') or []]
    ef += [['pessoa', pid, 'marca.' + k, 'poe', v] for k, v in (f.get('marcas') or {}).items()]
    if f.get('divida'): ef.append(['pessoa', pid, 'divida', 'soma', int(f['divida'])])          # o feitiço de pacto lançado na luta soma dívida (a bruxa)
    if (f.get('est') or {}).get('enjoo') and f['estado'] != 'morto':                            # quem enjoou na luta segue enjoado até o fim do bloco, como fora dela
        import tabelas_magia_mundo as W
        ef.append(['pessoa', pid, 'marca.enjoo', 'poe', dict(ate=estado.agora(E) + W.ENJOO_DURA)])
    if f.get('dom_fez'): ef += talento.mostra(E, pid)                    # o dom decidiu um golpe: a pessoa viu que tem
    if f.get('funda') is not None and pv < estado.pv_max(p) and f['funda'] != p.get('funda'): ef.append(['pessoa', pid, 'funda', 'poe', f['funda']])
    for k in ('doses', 'curado'):                                        # os totais do dia: as poções bebidas, o PV devolvido por cura
        n = f.get(k)
        if n is not None and n != estado.hoje(E, p, k): ef.append(['pessoa', pid, f'marca.{k}', 'poe', dict(dia=E['relogio']['dia'], n=n)])
    return ef


def luta_larga(E, arq_luta, porque):
    """SÓ O MESTRE: dá por encerrada uma luta aberta (o arquivo se perdeu, a cena mudou). Nada volta ao estado: o que o Mestre decidir entra por evento "mestre"."""
    g = estado.arq_guarda(arq_luta); abertas = [l for l in E['turno']['lutas'] if not l['fim'] and (l['arq'] == g or l['arq'] == arq_luta or os.path.basename(l['arq']) == os.path.basename(arq_luta))]
    if not abertas: sys.exit(f'não há luta aberta com o arquivo "{arq_luta}"' + (f" (abertas: {', '.join(l['arq'] for l in E['turno']['lutas'] if not l['fim'])})" if any(not l['fim'] for l in E['turno']['lutas']) else ''))
    if not porque.strip(): sys.exit('diga por que a luta é largada: `ato.py luta larga LUTA.json "por quê"`')
    for l in abertas: l['fim'] = 'largada'
    E['turno']['notas'].append(f"luta largada ({abertas[0]['arq']}): {porque}")
    return f"luta largada: {abertas[0]['arq']} ({porque}). Nada voltou ao estado: o que houve nela entra por `estado.py mestre`."


def ultima_linha(E, pid, prata=None):
    """A ÚLTIMA LINHA de todo comando que mexe no mundo: a hora, e como ficou quem agiu. COM UMA LUTA ABERTA diz só a hora e que vale o quadro da luta (o PV do save é o de
    antes dela: o da luta só volta ao estado quando ela acaba). De quem MORREU, só a hora e a morte. Se quem agiu não é o personagem, uma segunda linha diz como ficou o
    personagem, que esperava: o tempo passa para ele também."""
    p = E['gente'][pid]; eu = estado.eu(E); mil = prata or (lambda n: f'{n}')
    if estado.luta_aberta(E): return f"{estado.quando(E)} · LUTA ABERTA: o PV, o fôlego e as feridas que valem agora são os do quadro da luta"
    diz = lambda x: f"PV {x['pv']}/{estado.pv_max(x)} · {corpo.diz(x)} · {mil(x['moedas'])} de prata"
    L = [f"{estado.quando(E)} · " + (f"{p['nome']} {estado.morte_diz(E, p)}" if p['estado'] != 'vivo' else diz(p))]
    if eu and eu != pid and E['gente'][eu]['estado'] == 'vivo': L.append(f"{E['gente'][eu]['nome']}, que esperava: {diz(E['gente'][eu])}")
    return '\n'.join(L)


if __name__ == '__main__':
    import signal; hasattr(signal, 'SIGPIPE') and signal.signal(signal.SIGPIPE, signal.SIG_DFL)      # a saída cortada (`| head`) acaba o comando calada, sem erro de programa: tudo já foi gravado antes de falar
    a = sys.argv[1:]
    if not a: print(__doc__); sys.exit()
    op = dict(x.split('=', 1) for x in a if '=' in x and ':' not in x); pos = [x for x in a if '=' not in x or ':' in x]
    cmds = ('comer', 'dormir', 'trabalhar', 'treinar', 'descansar', 'esperar', 'pecas', 'vestir', 'tirar', 'luta')
    if not pos or pos[0] not in cmds: print(__doc__); sys.exit()
    E = estado.carrega(); pid = op.get('quem') or estado.eu(E)
    if pid not in E['gente']: sys.exit(f'não há a pessoa "{pid}"')
    n = lambda i: int(pos[i]) if len(pos) > i and pos[i].isdigit() and int(pos[i]) >= 1 else sys.exit(f'diga quantos blocos, em número inteiro (1 ou mais): `ato.py {pos[0]} 2`. Um bloco são 4 horas.')
    falta = lambda o_que, exemplo: sys.exit(f'{o_que}: `python3 ato.py {exemplo}`')       # uma frase por erro, em vez do uso inteiro
    if pos[0] == 'pecas': print('\n'.join(diz_pecas(E, pid))); sys.exit()
    if pos[0] == 'comer': out = comer(E, pid, da_carga='carga' in pos[1:])
    elif pos[0] == 'dormir': out = dormir(E, pid, n(1), chao='chao' in pos)
    elif pos[0] == 'trabalhar': out = trabalhar(E, pid, n(1))
    elif pos[0] == 'treinar': out = treinar(E, pid, n(1), pos[2] if len(pos) > 2 else falta(f"diga com que arma treinar ({', '.join(T.FAMILIAS)})", 'treinar 2 espada'))
    elif pos[0] == 'descansar': out = descansar(E, pid, n(1))
    elif pos[0] == 'esperar': out = esperar(E, pid, n(1))
    elif pos[0] == 'vestir': out = vestir(E, pid, pos[1], pos[2] if len(pos) > 2 else None) if len(pos) in (2, 3) else falta('diga qual peça vestir (o id dela: `ato.py pecas` mostra) e, se quiser, onde (arma, arma2 ou escudo)', 'vestir i0007')
    elif pos[0] == 'tirar': out = tirar(E, pid, pos[1]) if len(pos) == 2 else falta('diga qual peça guardar (o id dela: `ato.py pecas` mostra)', 'tirar i0007')
    elif pos[:2] == ['luta', 'nova']:
        if len(pos) != 4: falta('diga o arquivo do cenário e o arquivo onde a luta fica guardada', 'luta nova CENARIO.json LUTA.json')
        quadro = luta_nova(E, pos[2], pos[3]); g = E['turno']['lutas'][-1]['arq']; print(quadro)
        print(f'\nA luta ficou guardada em {g}' + (' (na pasta do save)' if not os.path.isabs(g) else '') + f'. Siga com `python3 ato.py luta roda {g} "Nome: ordem"`.')
        if os.path.isabs(g): print(f'AVISO: esse arquivo está FORA da pasta do save ({estado.pasta()}): se o save mudar de lugar, a luta não vai junto. Só com o nome (sem pasta), ela fica em lutas/, dentro do save.')
        sys.exit()
    elif pos[:2] == ['luta', 'roda']: out = luta_roda(E, pos[2], pos[3:]) if len(pos) >= 3 else falta('diga o arquivo da luta e, se quiser, as ordens', 'luta roda LUTA.json "Nome: atacar"')
    elif pos[:2] == ['luta', 'larga']: out = luta_larga(E, pos[2], pos[3]) if len(pos) == 4 else falta('diga o arquivo da luta e por quê ela é largada', 'luta larga LUTA.json "por quê"')
    else: falta('a luta tem três comandos: nova, roda e larga', 'luta roda LUTA.json "Nome: atacar"')
    estado.grava(E)                                         # grava ANTES de falar: a saída cortada não perde o que o dado rolou
    print(out)
    print(ultima_linha(E, pid))
