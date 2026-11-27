#!/usr/bin/env python3
"""estado.py — MOTOR 10: O ESTADO DO MUNDO E O ÚNICO GRAVADOR.

O save é uma pasta (`mundo/`, ou a que estiver em MOTOR10_MUNDO) com: relogio.json · lugares.json · gente.json · itens.json
· turno.json · eventos.jsonl (o único histórico; o diário sai dele).
  CADA FATO NUM LUGAR SÓ: o dono de uma peça e onde ela está vestida moram só no itens.json; onde a pessoa está, só na ficha dela.
  SÓ `aplica()` MUDA O ESTADO. Um evento é {dia, bloco, tipo, onde, quem, efeitos, texto}; sem efeito, é recusado; o que não muda nada não entra no registro.
  Um efeito é uma operação tipada de uma lista fechada:
    ['relogio', blocos]                              o tempo anda
    ['pessoa', id, campo, 'soma'|'poe', valor]       moedas · pv · fome · sono · cansaco · lugar · estado · nivel · grau_oficio · treino.X · maestria.X (X: arma ou ofício) · marca.X
                                                     · carga.BEM (o que a pessoa carrega: só 'soma', nunca abaixo de zero)
    ['pessoa', 'nasce', id, registro]                uma pessoa nova (nome, nivel, atributos, lugar; o resto tem padrão). Só em evento "gera" ou "mestre"
    ['lugar', id, campo ou campo.sub, 'soma'|'poe', valor]   um número ou uma marca do lugar (bichos.lobo, coleta.metal:0, oficina, pop); 'soma' nunca abaixo de zero;
                                                     o que é conta (bichos, teto, coleta, coleta_teto, produz, pop, oficina, preparo) só aceita número, na faixa dele
    ['lugar', 'nasce', id, registro]                 um lugar novo (nome; o resto tem padrão). Só em evento "gera" ou "mestre"
    ['ferida', id, 'abre', parte, grave]  ·  ['ferida', id, 'repousa', n]  ·  ['ferida', id, 'sara', indice]
    ['estoque', lugar, bem, 'soma', valor]
    ['item', id, campo, 'poe'|'soma', valor]         dono · uso · dur
    ['item', 'nasce', registro]                      uma peça nova entra no Livro de Itens (o id sai da sequência); também núcleos (tipo 'nucleo')
    ['item', id, 'onde', 'poe', lugar]  ·  ['item', id, 'solto', 'poe', True|None]  ·  ['item', id, 'sob_medida', 'poe', {dono, grau}]
    ['item', id, 'historia', 'junta', 'texto']  ·  ['item', id, 'some']
    ['item', id, 'efeito', 'junta', {chave, cheio?, emprestado?}]  ·  ['item', id, 'efeitos_livres'|'cheios_livres', 'poe'|'soma', n]      (a parte 2, fase 1a: os efeitos de
                                                     ferramenta pela porta da força e o teto de efeitos; os campos novos do item: teto_efeitos, cheios_livres, sinete, degrau;
                                                     a obra aceita o molde: ['obra', 'abre', {..., molde}]. O save de antes passa como está: a peça sem teto_efeitos usa o da categoria)
    ['obra', 'abre', registro]  ·  ['obra', id, campo, 'soma'|'poe', valor]  ·  ['obra', id, 'fecha']      a obra em andamento (forja de vários dias; a leva da alquimia; a gravação)
  OS DA ETAPA DA MAGIA (a forma exata e o porquê de cada um: projeto/ETAPA_MAGIA.md, seção 7):
    ['pessoa', id, 'talento'|'dom', 'poe', {caminho: grau}] (só em gera, mestre ou talento) · ['pessoa', id, 'inclinacao', 'poe', caminho]
    · ['pessoa', id, 'mana', 'soma'|'poe', n] · ['pessoa', id, 'feitico', 'aprende'|'esquece', nome] · ['pessoa', id, 'tradicao', 'poe', t]
    · ['pessoa', id, 'voto', 'poe', {qual, santuario, dia}] · ['pessoa', id, 'voto', 'quebra', 'como'] · ['pessoa', id, 'laco', 'poe', {ermo, dia}]
    · ['pessoa', id, 'divida', 'soma', n] · ['pessoa', id, 'funda', 'poe', categoria]
    ['maldicao', id, 'poe', registro]  ·  ['maldicao', id, MID, 'passo'|'quebra'|'sabe'|'suspensa'|'condicao', valor]
    ['item', id, 'encanto', 'grava', registro] · ['item', id, 'encanto', 'gasta'|'apaga', indice] · ['item', id, 'maldita'|'benta'|'veneno', 'poe', valor]
    (os tipos novos de item: foco, amuleto, elixir, escrito; os usos novos: foco, pescoco; no lugar: botica, runas, santuario, maldito, covil)
  OS DA ETAPA 4b (as masmorras e o mundo de fantasia; a forma exata: projeto/ETAPA_4B.md, seção 6):
    ['pessoa', id, 'povo'|'idade', 'poe', valor] (só em gera ou mestre) · ['pessoa', id, 'inclinacao2', 'poe', caminho] (só em gera, mestre ou talento)
    · ['pessoa', id, 'marca.masmorra', 'poe', {...}] (a descida aberta) · ['item', id, 'talhe', 'poe', 'miúdo' | None] (só armadura: o corpo para que foi feita)
    (os tipos novos de item: gazua, chave; o bem novo: tocha; no lugar: a masmorra e a sala (molde, niveis, entrada, portas, alarme, vagantes, limpa, origem; masmorra, nivel,
    largura, acesa, cat, atento, armadilhas, guardado, segredos, chefe, do_morto), a gente (povos) e o dragão (dragao))
  OS DA ETAPA FINAL (a região, a gente, a corrida, o medo, a história; a forma exata: projeto/ETAPA_FINAL.md, seções 1 a 3):
    ['mundo', SECAO, ID, 'poe', registro|None] · ['mundo', SECAO, ID, 'CAMPO', 'poe'|'soma'|'junta', valor] · ['mundo', SECAO, 'junta', valor] (cronica, janela)
    · ['mundo', SECAO, 'CAMPO', 'poe'|'soma', valor] (meta, ranking, leilao, torneio, oculto, seq): o arquivo novo do save, mundo.json (ausente: o mundo vazio)
    ['pessoa', id, 'casa'|'pais'|'papel'|'rival', 'poe', valor] (só em gera, mestre; a casa também em heranca) · ['pessoa', id, 'lacos.OUTRO', 'poe', tipo|None]
    · ['pessoa', id, 'memoria', 'junta', {dia, de, o_que, peso}] · ['pessoa', id, 'fama', 'soma', n] · ['pessoa', id, 'querer'|'guilda', 'poe', valor]
    · ['pessoa', id, 'herdeiro', 'poe', PID] (herdeiro, mestre) · ['pessoa', id, 'jogador', 'poe', True|None] (só em heranca: o herdeiro assume)
    (o lugar novo: a estrada, tipo "estrada", com ponta, longe, perigo, bando, passa, fechada; quem viaja leva marca.viagem e está FORA, na estrada)
  QUEM ESTÁ NUMA DESCIDA (marca.masmorra) também está FORA: `fora()` diz a sala onde o grupo está. A morte lá dentro deixa tudo na sala; quem comanda e morre solta quem ia junto.
  A ARMADURA É FEITA PARA UM CORPO (o `talhe`: sem ele, de gente; "miúdo"): a que não serve no corpo do dono não entra em uso. (O `corpo` de uma peça solta é outra coisa: de quem era o morto.)
  A PEÇA MALDITA NÃO SAI: enquanto o dono tem uma maldição andando que veio dela, a peça não sai de uso nem muda de dono. O morto não tem maldição andando
    (elas vão para a morte dele). A ferida funda some quando o PV enche.
  O ITEM SEM DONO está num lugar (`onde`). Ali ele é da LOJA (a prateleira), a não ser que esteja SOLTO (`solto`): caído no chão, de quem achar.
  A MORTE é uma regra só, dentro do efeito ['pessoa', id, 'estado', 'poe', 'morto']: o morto não fica com nada. As peças dele (vestidas ou guardadas, e os núcleos)
    caem SOLTAS onde ele morreu, com a marca `corpo` (de quem eram); as obras dele se desfazem (a matéria se perde; o núcleo cai com o resto); a carga e a prata
    ficam no estoque desse lugar (num lugar com povo, o povo fica com elas; no ermo, ficam no chão, junto do corpo; na sala de uma masmorra, onde o estoque é também o
    tesouro, a parte do morto fica escrita à parte, em `do_morto`: não se pega, e o estoque não desce abaixo dela sem o Mestre soltá-la no mesmo evento).
    O QUE ERA DE UM MORTO NÃO MUDA DE MÃO SOZINHO: quem passa ali acha o corpo, mas quem fica com o quê é decisão de cena, por evento "mestre" (o herdeiro é da etapa 6).
  QUEM SAIU para o ermo (a saída de caça ou de coleta, escrita em marca.caca) está FORA: `fora()` diz onde, e `presente()` recusa o ato da vila.
  COM UMA LUTA ABERTA (no caderno do turno) O MUNDO NÃO ANDA: `aplica()` só aceita a luta que volta ao estado (evento "luta"), a mão do Mestre (evento "mestre")
    e a nota da saída de caça que diz que ela está naquela luta. O resto é recusado, de qualquer pessoa, com a frase que diz como acabar ou soltar a luta.
  O que o Mestre inventa em cena entra por um evento "mestre", com os mesmos efeitos. Fora disso, não aconteceu.
  QUEM NÃO É O PERSONAGEM CUIDA DE SI QUANDO NÃO ESTÁ EM CENA (o descanso em casa). O gravador guarda, em cada pessoa que não é o personagem, o bloco em que o corpo dela
    (a fome, o sono, o cansaço, o PV, as feridas) foi mexido pela última vez: `marca.cena` (o último bloco em que esteve em cena). Quando ela volta a agir (um ato com quem=,
    entrar numa saída ou numa luta), `em_cena()` acerta ANTES, num evento "casa", o tempo que passou desde esse bloco: 3 blocos ou mais, o corpo volta a zero; a cada 6, uma noite
    de cura e um dia de repouso (corpo.casa). Quem volta do ermo no bloco da noite e é chamado às 8h passou 3 blocos (dois inteiros em casa): descansou.
    O personagem nunca ganha descanso de graça. Save de antes desta regra: quem não tem a marca conta como descansado, sem noite de cura.

Uso (para olhar): python3 estado.py valida | python3 estado.py eventos [N] | python3 estado.py pessoa ID | python3 estado.py lugar ID
     (o Mestre): python3 estado.py mestre '[["pessoa","eu","moedas","soma",5]]' "achou cinco moedas na estrada"      um evento "mestre", com os efeitos em JSON
"""
import copy, hashlib, json, os, random, sys
import tabelas as T
import tabelas_mundo as M
import tabelas_bichos as TB
import tabelas_talento as TT

AQUI = os.path.dirname(os.path.abspath(__file__))
ARQS = ('relogio', 'lugares', 'gente', 'itens', 'turno', 'mundo')        # mundo: o arquivo da etapa final (ausente no save antigo: o mundo vazio)
PARTES_VESTE = ('arma', 'arma2', 'escudo', 'veste', 'foco', 'pescoco')
TIPOS_ITEM = ('arma', 'armadura', 'escudo', 'nucleo', 'foco', 'amuleto', 'elixir', 'escrito', 'gazua', 'chave', 'ferramenta')      # os tipos do Livro de Itens (foco a escrito: etapa da magia; gazua e chave: etapa 4b)
USO_DO_TIPO = dict(arma='arma', arma2='arma', escudo='escudo', veste='armadura', foco='foco', pescoco='amuleto')     # onde cada uso pede que tipo de peça
COM_ENCANTO = ('arma', 'armadura', 'escudo')        # as peças que levam encanto (o foco e o amuleto já são magia)
TALENTO_EVENTOS = ('gera', 'mestre', 'talento')     # só nestes eventos se grava o talento e o dom (o talento já rolado, só em "mestre")


def pasta(): return os.environ.get('MOTOR10_MUNDO') or os.path.join(AQUI, 'mundo')


# ---------- ler e gravar ----------
def carrega():
    p = pasta()
    if not os.path.exists(os.path.join(p, 'relogio.json')): sys.exit(f'não há mundo em {p} (falta o relogio.json)')
    E = {k: json.load(open(os.path.join(p, k + '.json'), encoding='utf-8')) for k in ARQS if k != 'mundo' or os.path.exists(os.path.join(p, k + '.json'))}
    E.setdefault('mundo', {})                               # o save de antes da etapa final não tem o mundo.json: o mundo vazio
    E['_novos'] = []
    return E


def grava(E):
    """escreve o estado inteiro (cada arquivo de uma vez, por troca) e junta os eventos novos ao histórico"""
    p = pasta(); os.makedirs(p, exist_ok=True); E.setdefault('mundo', {})
    for k in ARQS:
        if k == 'mundo' and not E['mundo'] and not os.path.exists(os.path.join(p, 'mundo.json')): continue      # o save antigo segue sem o arquivo novo enquanto o mundo estiver vazio
        tmp = os.path.join(p, k + '.json.tmp')
        json.dump(E[k], open(tmp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        os.replace(tmp, os.path.join(p, k + '.json'))
    if E['_novos']:
        with open(os.path.join(p, 'eventos.jsonl'), 'a', encoding='utf-8') as f:
            for ev in E['_novos']: f.write(json.dumps(ev, ensure_ascii=False) + '\n')
        E['_novos'] = []


def novo(semente=1):
    """um estado vazio (o gerador e as provas partem daqui)"""
    return dict(relogio=dict(semente=semente, dia=1, bloco=2, eventos=0), lugares={}, gente={}, itens=dict(seq=0, itens={}, oseq=0, obras={}),
                turno=dict(n=1, aberto=dict(dia=1, bloco=2), dados=[], lutas=[], perguntas=[], respondidas=[], notas=[]), mundo={}, _novos=[])


# ---------- o tempo e o acaso do mundo ----------
def agora(E): return (E['relogio']['dia'] - 1) * M.BLOCOS_DIA + E['relogio']['bloco']        # blocos desde o começo do mundo
def estacao(E): return M.ESTACOES[((E['relogio']['dia'] - 1) % M.ANO) // M.ESTACAO]
def quando(E):
    r = E['relogio']; return f"Dia {r['dia']}, {M.BLOCOS[r['bloco']]} ({r['bloco'] * M.BLOCO_HORAS}h) · {estacao(E)}"


def sorte(E, chave):
    """o acaso do MUNDO (não o dado do jogador): sai da semente, do dia, do bloco e de uma chave. Mesma semente, mesmo mundo; nunca se rola de novo."""
    r = E['relogio']; h = hashlib.sha256(f"{r['semente']}|{r['dia']}|{r['bloco']}|{chave}".encode()).digest()
    return random.Random(int.from_bytes(h[:8], 'big'))


def eu(E):
    """o id do personagem do jogador"""
    return next((k for k, p in E['gente'].items() if p.get('jogador')), None)


# ---------- onde a pessoa está, e o arquivo de uma luta ----------
def fora(E, pid):
    """o lugar onde a pessoa está, se SAIU do lugar onde mora: o ermo da saída de caça ou de coleta (marca.caca), ou a sala da descida aberta (marca.masmorra,
    etapa 4b: a sala de quem comanda); senão None"""
    s = (E['gente'][pid].get('marca') or {}).get('caca')
    if isinstance(s, dict) and s.get('ermo') in E['lugares']: return s['ermo']
    d = descida(E, pid)
    if d: return d['sala']
    v = viagem(E, pid)
    return v['estrada'] if v else None


def viajante(E, pid):
    """o id de quem comanda a viagem aberta em que a pessoa está (ela mesma, se comanda), ou None (etapa final: marca.viagem; quem vai junto tem {"de": quem comanda})"""
    p = E['gente'].get(pid) if isinstance(pid, str) else None
    v = (p.get('marca') or {}).get('viagem') if isinstance(p, dict) and isinstance(p.get('marca'), dict) else None
    if not isinstance(v, dict): return None
    if v.get('de') is None: return pid if isinstance(E['lugares'].get(v.get('estrada')), dict) else None
    q = E['gente'].get(v['de']) if isinstance(v['de'], str) else None
    vq = (q.get('marca') or {}).get('viagem') if isinstance(q, dict) and isinstance(q.get('marca'), dict) else None
    return v['de'] if isinstance(vq, dict) and vq.get('de') is None and isinstance(E['lugares'].get(vq.get('estrada')), dict) else None


def viagem(E, pid):
    """a viagem aberta em que a pessoa está: o registro de quem comanda (marca.viagem: "estrada", "sai", "para", "feitos", "longe", "com", "fase"...), ou None"""
    k = viajante(E, pid)
    return E['gente'][k]['marca']['viagem'] if k else None


def quem_desce(E, pid):
    """o id de quem comanda a descida aberta em que a pessoa está (ela mesma, se comanda), ou None (etapa 4b: marca.masmorra; quem vai junto tem {"de": quem comanda})"""
    p = E['gente'].get(pid) if isinstance(pid, str) else None
    d = (p.get('marca') or {}).get('masmorra') if isinstance(p, dict) and isinstance(p.get('marca'), dict) else None
    if not isinstance(d, dict): return None
    if d.get('de') is None: return pid if d.get('sala') in E['lugares'] else None
    q = E['gente'].get(d['de']) if isinstance(d['de'], str) else None
    dq = (q.get('marca') or {}).get('masmorra') if isinstance(q, dict) and isinstance(q.get('marca'), dict) else None
    return d['de'] if isinstance(dq, dict) and dq.get('de') is None and dq.get('sala') in E['lugares'] else None


def descida(E, pid):
    """a descida aberta em que a pessoa está: o registro de quem comanda (marca.masmorra: "masmorra", "sala", "com", "ordem", "lances", "luz", "fase", "luta"...), ou None"""
    k = quem_desce(E, pid)
    return E['gente'][k]['marca']['masmorra'] if k else None


def onde(E, pid): return fora(E, pid) or E['gente'][pid]['lugar']          # onde o corpo está agora: no ermo da saída, ou no lugar onde mora
def em(E, lid): l = E['lugares'][lid]; return l.get('em', 'em ' + l['nome'])
def de(E, lid):
    """o lugar depois de "de", com a contração do artigo do nome: "da Vila de Prova", "do Mato", "de Pedra Rasa\""""
    return de_nome(E['lugares'][lid]['nome'])


def de_nome(n):
    """um nome depois de "de", com a contração do artigo, se ele vem com artigo: "da Espada do Guardião", "do Mato", "de Pedra Rasa", "de amuleto Comum\""""
    art, _, resto = n.partition(' ')
    return {'a': 'da ', 'o': 'do ', 'as': 'das ', 'os': 'dos '}[art] + resto if art in ('a', 'o', 'as', 'os') and resto else 'de ' + n


def morte_diz(E, p):
    m = p.get('morte') or {}
    return f"morreu no Dia {m['dia']}, {em(E, m['onde'])}" if m.get('onde') in E['lugares'] else 'já morreu'


def de_morto(it):
    """esta peça solta ficou com o corpo de alguém que morreu? Devolve o id do morto (a marca `corpo`), True se só a história o diz (save antigo), ou None"""
    if not it.get('solto') or it.get('dono'): return None
    return it.get('corpo') or (True if 'ficou com o corpo de' in ''.join((it.get('historia') or [])[-1:]) else None)


def junto(E, lid):
    """A PARTE DO ESTOQUE QUE FICOU JUNTO DO CORPO de quem morreu numa sala de masmorra (`do_morto`): {bem: quanto}. Está no estoque (a prata do mundo a conta),
    mas não é tesouro: não muda de mão sozinha (cena do Mestre). Fora da sala, nada (no ermo o estoque inteiro é o chão; na vila, o povo fica com ela)"""
    l = E['lugares'].get(lid) or {}; est = l.get('estoque') or {}
    return {b: min(q, est.get(b, 0)) for b, q in (l.get('do_morto') or {}).items() if _num(q) and q > 0 and _num(est.get(b, 0)) and est.get(b, 0) > 0}


def livre(E, lid):
    """o estoque do lugar sem a parte que ficou junto do corpo de um morto (junto): {bem: quanto}, só o que é mais que zero. É o que se pega"""
    est = (E['lugares'].get(lid) or {}).get('estoque') or {}; j = junto(E, lid)
    return {b: q - j.get(b, 0) for b, q in est.items() if _num(q) and q - j.get(b, 0) > 0}


def nome_bem(b):
    """o nome de um bem como vai à mesa: a matéria com a categoria por extenso ("couro Comum", "madeira Rara", e não a chave "couro:0"); os outros bens, como são"""
    from itens import FEM
    n, c = M.le_materia(b)
    if c is None or not 0 <= c < len(T.CATS): return b
    if n in M.POCOES: nm = M.POCOES[n]; return f"{nm} {(FEM if nm.split()[0].endswith(('a', 'ção')) else T.CATS)[c]}"      # "poção de cura Comum", "antídoto Raro"
    return f"{n} {(FEM if n.endswith('a') else T.CATS)[c]}"


def num(n): return f'{n:g}'.replace('.', ',')       # o número à mesa: sem casa decimal à toa, com vírgula (1,5 dia de repouso)


def tantos(n, um, muitos=None):
    """o número com a palavra no singular ou no plural: "1 bloco", "3 blocos", "2 ações" (tantos(2, 'ação', 'ações'))"""
    return f"{n:g} {um if n == 1 else (muitos or um + 's')}"


# ---------- a luta aberta tranca o mundo ----------
def luta_aberta(E):
    """o arquivo (como o save o guarda) da luta que está aberta no caderno do turno, ou None"""
    return next((l['arq'] for l in E['turno'].get('lutas', []) if not l.get('fim')), None)


def luta_diz(E):
    """a frase da tranca (ou None, se não há luta aberta): há uma luta aberta, o mundo não anda, e é assim que ela acaba ou se solta"""
    arq = luta_aberta(E)
    if not arq: return None
    dono = next((k for k, p in E['gente'].items() if isinstance(p, dict) and isinstance((p.get('marca') or {}).get('caca'), dict) and p['marca']['caca'].get('luta') == arq), None)
    desce = None if dono else next((k for k, p in E['gente'].items() if isinstance(p, dict) and isinstance((p.get('marca') or {}).get('masmorra'), dict) and p['marca']['masmorra'].get('luta') == arq), None)
    anda = None if dono or desce else next((k for k, p in E['gente'].items() if isinstance(p, dict) and isinstance((p.get('marca') or {}).get('viagem'), dict) and p['marca']['viagem'].get('luta') == arq), None)
    quem = f' quem={dono or desce or anda}' if (dono or desce or anda) and (dono or desce or anda) != eu(E) else ''
    if anda: acaba, solta = f'`viagem.py luta "Nome: ordem"{quem}`', f'`viagem.py larga "por quê"{quem}`'
    elif desce: acaba, solta = f'`masmorra.py luta "Nome: ordem"{quem}`', f'`masmorra.py larga "por quê"{quem}`'
    elif dono: acaba, solta = f'`caca.py luta "Nome: ordem"{quem}`', f'`caca.py larga "por quê"{quem}`'
    else: acaba, solta = f'`ato.py luta roda {arq} "Nome: ordem"`', f'`ato.py luta larga {arq} "por quê"`'
    return f"há uma luta aberta ({arq}): enquanto ela não acabar, nada mais anda no mundo. Para seguir a luta: {acaba}. Se o arquivo se perdeu ou a cena mudou, o Mestre a solta: {solta}."


def sem_luta(E):
    """recusa, com a frase, se há luta aberta no mundo: todo ato que grava chama isto ANTES de cobrar ou rolar qualquer coisa"""
    t = luta_diz(E)
    if t: sys.exit(t)


def _nota_da_luta(E, efeitos):
    """os efeitos são só a nota da saída de caça (ou da descida, etapa 4b) dizendo que ela está NAQUELA luta aberta? (é o que se escreve logo ao abrir a luta: não mexe em tempo, prata nem peça)"""
    abertas = [l['arq'] for l in E['turno'].get('lutas', []) if not l.get('fim')]
    return bool(efeitos) and all(isinstance(ef, (list, tuple)) and len(ef) == 5 and ef[0] == 'pessoa' and ef[2] in ('marca.caca', 'marca.masmorra', 'marca.viagem') and ef[3] == 'poe' and isinstance(ef[4], dict)
                                 and ef[4].get('fase') == 'luta' and ef[4].get('luta') in abertas for ef in efeitos)


def presente(E, pid, o_que='agir aqui'):
    """a condição de todo ato da vila: a pessoa existe, está viva, está NO LUGAR ONDE MORA (sem saída aberta) e não há luta aberta no mundo. Senão, recusa com a frase. Devolve a pessoa."""
    p = E['gente'].get(pid) or sys.exit(f'não há a pessoa "{pid}"')
    if p['estado'] != 'vivo': sys.exit(f"{p['nome']} não age: {morte_diz(E, p)}")
    sem_luta(E)
    f = fora(E, pid)
    if f and viajante(E, pid): sys.exit(f"{p['nome']} está {em(E, f)}, na viagem (a viagem está aberta): não pode {o_que}. `viagem.py ver` diz o que há à frente; `viagem.py segue` continua o caminho.")
    if f and quem_desce(E, pid): sys.exit(f"{p['nome']} está {em(E, f)}, na descida (a descida está aberta): não pode {o_que}. `masmorra.py ver` diz onde o grupo está; `masmorra.py sair` volta para casa.")
    if f: sys.exit(f"{p['nome']} está fora, {em(E, f)} (a saída está aberta): não pode {o_que}. `caca.py ver` diz o que há à frente; `caca.py volta` fecha a saída.")
    em_cena(E, pid)
    return E['gente'][pid]


def em_cena(E, pid):
    """QUEM NÃO É O PERSONAGEM VOLTA À CENA: antes de mais nada, acerta num evento só ("casa") o tempo que a pessoa passou fora de cena (corpo.casa: o descanso em casa).
    Não vale para o personagem (ele nunca descansa de graça), para quem morreu, para quem está fora (no ermo, numa saída aberta: lá não é casa), nem com uma luta aberta
    (o mundo está parado). Chamar de novo não muda nada: o acerto conta do bloco em que o corpo foi mexido pela última vez. Devolve o evento, ou None."""
    import corpo
    p = E['gente'].get(pid) if isinstance(pid, str) else None
    if not isinstance(p, dict) or p.get('jogador') or p.get('estado') != 'vivo' or fora(E, pid) or luta_aberta(E): return None
    ef = corpo.casa(E, pid)
    return aplica(E, 'casa', ef, onde=p['lugar'], quem=[pid], texto=f"{p['nome']} descansou em casa") if ef else None


def arq_guarda(arq):
    """o caminho de um arquivo como fica escrito no save: relativo à pasta do save se está dentro dela (a pasta pode mudar de lugar), senão inteiro"""
    a = os.path.abspath(arq); p = os.path.abspath(pasta())
    return os.path.relpath(a, p) if a == p or a.startswith(p + os.sep) else a


def arq_abre(guardado): return guardado if os.path.isabs(guardado) else os.path.join(pasta(), guardado)       # o caminho de verdade do que o save guardou


# ---------- o gravador ----------
CAMPOS = dict(moedas='soma', pv='soma', fome='soma', sono='soma', cansaco='soma', nivel='soma', lugar='poe', estado='poe', grau_oficio='poe')
CONTAS = ('bichos', 'teto', 'coleta', 'coleta_teto', 'produz')          # os campos do lugar que são {nome: número de zero para cima}


def _erro(ef, porque): return f'efeito {json.dumps(ef, ensure_ascii=False)}: {porque}'
def _num(v): return isinstance(v, (int, float)) and not isinstance(v, bool)
def _int(v): return isinstance(v, int) and not isinstance(v, bool)


def bem_conhecido(b):
    """o que se carrega e se guarda em estoque: os bens da tabela, a matéria com categoria e as poções do Comum ao Raro (tabelas_mundo: BENS, MATERIAS, MATERIA_ATE,
    POCOES, POCAO_ATE); a prata é à parte"""
    if b in M.BENS: return True
    n, c = M.le_materia(b)
    return c is not None and ((n in M.MATERIAS and c <= M.MATERIA_ATE) or (n in M.POCOES and c <= M.POCAO_ATE))


def e_pocao(b): n, c = M.le_materia(b); return n in M.POCOES and c is not None and c <= M.POCAO_ATE       # o bem é uma poção (ou a dose de veneno)?


_TC = 0
def especie(k):
    """o registro da espécie que a contagem do ermo e o encontro da caça aceitam: a dos bichos (tabelas_bichos.ESPECIES), a das criaturas (tabelas_criaturas.ESPECIES,
    se a página existir; etapa da magia) ou a dos dragões (tabelas_dragoes.ESPECIES, etapa 4b); None se não há"""
    if k in TB.ESPECIES: return TB.ESPECIES[k]
    mais = getattr(_tc(), 'ESPECIES', None)
    if isinstance(mais, dict) and isinstance(k, str) and k in mais: return mais[k]
    dr = getattr(_td(), 'ESPECIES', None)
    return dr.get(k) if isinstance(dr, dict) and isinstance(k, str) else None


_PAGINAS = {}
def _pagina(nome):
    """uma página de números da etapa 4b (tabelas_povos, tabelas_dragoes), importada uma vez só, ou None se ainda não existe"""
    if nome not in _PAGINAS:
        import importlib
        try: _PAGINAS[nome] = importlib.import_module(nome)
        except ModuleNotFoundError as e:
            if e.name != nome: raise
            _PAGINAS[nome] = None
    return _PAGINAS[nome]
def _tc():
    """a página das criaturas (etapa da magia), ou None"""
    global _TC
    if _TC == 0: _TC = _pagina('tabelas_criaturas')
    return _TC
def _tp(): return _pagina('tabelas_povos')
def _td(): return _pagina('tabelas_dragoes')


# ---------- a etapa 4b: o povo e o corpo da pessoa (leia sempre por aqui; os números: tabelas_povos) ----------
def povo(p):
    """o povo da pessoa: o nome; "humano" se ela não tem o campo (o save antigo, a gente de hoje)"""
    v = p.get('povo') if isinstance(p, dict) else None
    return v if isinstance(v, str) and v else 'humano'


def _povo_reg(p):
    """o registro do povo da pessoa (tabelas_povos.POVOS), ou {} (o humano, ou sem a página)"""
    TP = _tp(); r = TP.POVOS.get(povo(p)) if TP else None
    return r if isinstance(r, dict) else {}


def corpo_de(p):
    """o corpo da pessoa: "gente" ou "miúdo" (o do povo dela)"""
    return _povo_reg(p).get('corpo') or 'gente'


def serve(it, p):
    """a peça serve no corpo desta pessoa? Só a armadura tem corpo (sem o campo: de gente); a arma, o escudo e o resto servem em todo corpo"""
    return not isinstance(it, dict) or it.get('tipo') != 'armadura' or (it.get('talhe') or 'gente') == corpo_de(p)


_MODS = None
def modulos(gancho=None):
    """os módulos do mundo (tabelas_mundo.MODULOS) que existem, importados uma vez só: o que ainda não existe fica de fora, sem quebrar nada.
    Com `gancho`, só os que têm essa função (virada, bloco, casa, vestiu, voce, mesa, so_mestre, retomar, recusa_fecha)."""
    global _MODS
    if _MODS is None:
        import importlib; ms = []
        for nome in M.MODULOS:
            try: ms.append(importlib.import_module(nome))
            except ModuleNotFoundError as e:
                if e.name != nome: raise
        _MODS = ms
    return [m for m in _MODS if gancho is None or callable(getattr(m, gancho, None))]


def _conta_erro(raiz, k, v):
    """o que uma conta do lugar aceita: (o texto do erro, ou None)"""
    if not _num(v) or v < 0: return f'"{raiz}.{k}" é um número de zero para cima (veio {json.dumps(v, ensure_ascii=False)})'
    if raiz in ('bichos', 'teto') and not especie(k): return f'espécie desconhecida: "{k}"'
    if raiz == 'bichos' and int(v) != v: return f'a contagem de "{k}" é um número inteiro'
    if raiz in ('coleta', 'coleta_teto'):
        n, c = M.le_materia(k)
        if n not in M.MATERIAS or c is None or c > M.MATERIA_ATE: return f'matéria desconhecida: "{k}" (use nome:categoria, de 0 a {M.MATERIA_ATE}: metal:0, erva:1)'
    if raiz == 'produz' and k == 'prata': return 'prata não se produz: só nasce em evento "gera" ou "mestre"'
    return None


def _lugar_erro(E, raiz, sub, val):
    """o que um campo do lugar aceita num 'poe' (None: aceita)"""
    if raiz in CONTAS:
        d = {sub: val} if sub else val
        if not isinstance(d, dict): return f'"{raiz}" é uma conta: {{nome: quanto}}'
        return next((e for e in (_conta_erro(raiz, k, v) for k, v in d.items()) if e), None)
    if sub and raiz == 'preparo': return None if val is None or (_int(val) and 0 <= val < len(T.CATS)) else 'o preparo alcança uma categoria (0, Comum, em diante), ou nada'
    if raiz == 'alvo_pecas':                               # o alvo de peças da loja (mercado.py): {categoria: quantas peças ela quer ter na prateleira}
        d = {sub: val} if sub else val
        return None if isinstance(d, dict) and all(isinstance(k, str) and k.isdigit() and int(k) < len(T.CATS) and _int(v) and v >= 0 for k, v in d.items()) else 'o alvo de peças da loja é {categoria ("0", Comum, em diante): quantas peças ela quer ter na prateleira, de zero para cima}'
    if raiz == 'covil':                                     # o covil (etapa da magia, frente das criaturas): um registro livre; não guarda prata (o tesouro é o estoque do ermo)
        d = {sub: val} if sub else val
        if d is None: return None
        if not isinstance(d, dict): return 'o covil é um registro {...}, ou nada'
        if 'prata' in d: return 'o covil não guarda prata: o tesouro do covil é a prata do estoque do ermo'
        if 'cabecas' in d and not (_int(d['cabecas']) and d['cabecas'] >= 0): return 'as cabeças do covil são um número inteiro de zero para cima'
        return None
    if raiz in CAMPOS_4B: return _lugar4b_erro(E, raiz, sub, val)
    if sub: return None
    if raiz in ('botica', 'runas', 'santuario'): return None if val is None or (_int(val) and 0 <= val <= M.BANCADA_MAX) else f'"{raiz}" vai de 0 a {M.BANCADA_MAX}, ou nada'
    if raiz == 'maldito': return None if val is None else _molde_erro(val)
    if raiz == 'pop': return None if val is None or (_num(val) and val >= 0) else 'o povo é um número de zero para cima'
    if raiz == 'oficina': return None if val is None or (_int(val) and 0 <= val <= M.OFICINA_MAX) else f'a oficina vai de 0 a {M.OFICINA_MAX}, ou nada'
    if raiz == 'preparo': return None if isinstance(val, dict) and all(v is None or (_int(v) and 0 <= v < len(T.CATS)) for v in val.values()) else 'o preparo é {fogo, bigorna: a categoria que alcança}'
    if raiz == 'longe': return None if _int(val) and val >= 1 else 'os blocos de ida são 1 ou mais'
    if raiz == 'perigo': return None if _int(val) and 1 <= val <= M.PERIGO_MAX else f'o perigo vai de 1 a {M.PERIGO_MAX}'
    if raiz == 'vizinhos': return None if isinstance(val, list) and all(v in E['lugares'] for v in val) else 'os vizinhos são uma lista de lugares que existem'
    if raiz == 'cama': return None if isinstance(val, bool) else 'a cama é sim ou não'
    if raiz == 'ponta': return None if isinstance(val, list) and len(val) == 2 and val[0] != val[1] and all(v in E['lugares'] for v in val) else 'a ponta da estrada são dois lugares que existem, diferentes'
    if raiz == 'bando': return None if _int(val) and val >= 0 else 'o bando da estrada é um número inteiro de zero para cima'
    if raiz == 'passa': return None if val is None or val in E['lugares'] else 'a estrada passa por um lugar que existe (um ermo), ou nada'
    if raiz == 'fechada': return None if val is None or (isinstance(val, dict) and isinstance(val.get('por'), str)) else 'a estrada fechada diz {por: quem ou o quê, dia}, ou nada'
    return None


# ---------- a etapa 4b no lugar: a masmorra, a sala, a gente e o dragão (a forma de cada campo; as ligações entre lugares são do valida) ----------
CAMPOS_MASMORRA = ('molde', 'niveis', 'entrada', 'portas', 'alarme', 'vagantes', 'limpa', 'origem')
CAMPOS_SALA = ('masmorra', 'nivel', 'largura', 'acesa', 'cat', 'atento', 'armadilhas', 'guardado', 'segredos', 'chefe', 'do_morto')
CAMPOS_4B = CAMPOS_MASMORRA + CAMPOS_SALA + ('povos', 'dragao')


def _cat_ok(c): return _int(c) and 0 <= c < len(T.CATS)


def _chefe_ok(q):
    """um chefe que a tabela conhece: um dos tabelas_criaturas.CHEFES, ou uma espécie (bicho, criatura) que é chefe. O dragão não: a sala dele leva `dragao`"""
    if not isinstance(q, str) or not q: return False
    ch = getattr(_tc(), 'CHEFES', None)
    return (isinstance(ch, dict) and q in ch) or bool((especie(q) or {}).get('chefe'))


def _porta_erro(k, v):
    a, sep, b = k.partition('|') if isinstance(k, str) else ('', '', '')
    if not (sep and a and b and a < b): return f'a porta "{k}" se chama pelas duas salas, em ordem alfabética: "SALA_A|SALA_B"'
    if not isinstance(v, dict) or v.get('estado') not in M.PORTAS: return f'a porta é {{estado: {" | ".join(M.PORTAS)}, material, cat, fechadura}}'
    if v.get('material', 'madeira') not in M.PORTA_MATERIAL: return f'o material da porta é um de: {", ".join(M.PORTA_MATERIAL)}'
    if not _cat_ok(v.get('cat', 0)) or not (v.get('fechadura') is None or _cat_ok(v['fechadura'])): return 'a categoria da porta e a da fechadura vão de 0 a 7 (a fechadura pode ser nada)'
    if not isinstance(v.get('miudos', False), bool): return '"miudos" (só passa o corpo miúdo) é sim ou não'
    return None


def _armadilha_erro(a):
    if not isinstance(a, dict) or a.get('tipo') not in M.ARMADILHAS or not _cat_ok(a.get('cat')): return f'cada armadilha é {{tipo: um de {", ".join(M.ARMADILHAS)}, cat: 0 a 7, onde, achada, feita}}'
    o = a.get('onde', 'chão')
    if not (o in M.ARMADILHA_ONDE or (isinstance(o, str) and o.startswith('porta:') and len(o) > 6)): return 'a armadilha fica no "chão", no "guardado" ou na "porta:SALA"'
    if not (a.get('achada') is None or _int(a['achada'])) or a.get('feita') not in (None,) + M.ARMADILHA_FEITA: return f'"achada" é um dia (ou nada) e "feita" é {" ou ".join(M.ARMADILHA_FEITA)} (ou nada)'
    return None


def _dragao_erro(E, d):
    """o registro do dragão de um lugar (frente D): a forma que o gravador confere"""
    TD = _td()
    if TD is None: return 'não há a página dos dragões (tabelas_dragoes)'
    if not isinstance(d, dict) or not isinstance(d.get('nome'), str) or not d['nome']: return 'o dragão é um registro {nome, tipo, idade, pv, dorme_ate, punhados, vila, ...}, ou nada'
    if 'prata' in d: return 'o dragão não guarda prata: o tesouro é o estoque do lugar e as peças guardadas nele'
    if d.get('tipo') not in TD.TIPOS or d.get('idade') not in TD.IDADES: return f'o dragão tem um tipo ({", ".join(TD.TIPOS)}) e uma idade ({", ".join(TD.IDADES)})'
    if 'pv' in d and not (_int(d['pv']) and d['pv'] >= 1): return 'o PV do dragão é um número inteiro de 1 para cima (sem o campo: cheio)'
    if not (d.get('dorme_ate') is None or _int(d['dorme_ate'])) or not (_int(d.get('punhados', 0)) and d.get('punhados', 0) >= 0): return '"dorme_ate" é um dia (ou nada) e "punhados" um inteiro de zero para cima'
    if d.get('vila') is not None and d['vila'] not in E['lugares']: return f'não há o lugar "{d["vila"]}" (a vila do dragão)'
    return None


def _lugar4b_erro(E, raiz, sub, val):
    """o que um campo da etapa 4b no lugar aceita (None: aceita); com `sub`, a parte (portas.SALA_A|SALA_B, vagantes.ESPECIE, povos.POVO, dragao.CAMPO)"""
    if raiz == 'portas':
        d = {sub: val} if sub else val
        if not isinstance(d, dict): return 'as portas são {"SALA_A|SALA_B": porta}'
        return next((e for e in (_porta_erro(k, v) for k, v in d.items()) if e), None)
    if raiz == 'vagantes':
        d = {sub: val} if sub else val
        if not isinstance(d, dict): return 'os que vagueiam são {espécie: quantos}'
        return next((f'espécie desconhecida: "{k}"' if not especie(k) else f'"vagantes.{k}" é um inteiro de zero para cima' for k, v in d.items() if not especie(k) or not (_int(v) and v >= 0)), None)
    if raiz == 'povos':
        d = {sub: val} if sub else val
        TP = _tp()
        if not isinstance(d, dict) or any(TP is None or k not in TP.POVOS or not _num(v) or not 0 <= v <= 1 for k, v in d.items()): return 'a gente do lugar é {povo: fração de 0 a 1}, com os povos da tabela (tabelas_povos.POVOS)'
        if not sub and sum(d.values()) > 1 + 1e-9: return f'as frações da gente do lugar somam até 1 (somam {sum(d.values()):g})'
        return None
    if raiz == 'do_morto':                                  # a parte do estoque da sala que ficou junto do corpo de quem morreu ali (não é tesouro: cena do Mestre)
        d = {sub: val} if sub else val
        if not isinstance(d, dict): return 'o que ficou junto do corpo é {bem: quanto} (a parte do estoque da sala que é de um morto)'
        for k, v in d.items():
            if k != 'prata' and not bem_conhecido(k): return f'bem desconhecido junto do corpo: "{k}"'
            if not _num(v) or v < 0 or (k == 'prata' and not _int(v)): return f'"do_morto.{k}" é um número de zero para cima (a prata, inteira)'
        return None
    if raiz == 'dragao':
        if sub == 'pv': return None if _int(val) and val >= 1 else 'o PV do dragão é um número inteiro de 1 para cima'
        if sub == 'punhados': return None if _int(val) and val >= 0 else 'os punhados são um inteiro de zero para cima'
        if sub: return None
        return None if val is None else _dragao_erro(E, val)
    if sub: return None
    if raiz == 'molde': return None if val in M.MOLDES else f'o molde da masmorra é um de: {", ".join(M.MOLDES)}'
    if raiz == 'niveis':
        if not isinstance(val, list) or not val: return 'os níveis são [{n: 1, cat: 0, salas: [ids]}, ...]'
        for i, x in enumerate(val, 1):
            if not isinstance(x, dict) or x.get('n') != i or not _cat_ok(x.get('cat')) or not isinstance(x.get('salas'), list) or not all(isinstance(s, str) for s in x['salas']):
                return 'os níveis são [{n: 1, cat: 0, salas: [ids]}, {n: 2, ...}], em ordem, com a categoria de 0 a 7'
        return None
    if raiz in ('entrada', 'masmorra'): return None if isinstance(val, str) and val else f'"{raiz}" é o id de um lugar'
    if raiz == 'alarme': return None if _int(val) and 0 <= val <= M.ALARME_MAX else f'o alarme vai de 0 a {M.ALARME_MAX}'
    if raiz == 'limpa': return None if val is None or (isinstance(val, dict) and _int(val.get('dia')) and isinstance(val.get('quem', []), list)) else 'a primeira limpeza é {dia, quem: [ids], chefe}, ou nada'
    if raiz == 'origem': return None if isinstance(val, str) else 'a origem é texto'
    if raiz == 'nivel': return None if _int(val) and val >= 1 else 'o nível da sala é um inteiro de 1 para cima'
    if raiz == 'largura': return None if val is None or (_int(val) and val >= 1) else 'a largura é um inteiro de 1 para cima (1: corredor), ou nada (sala aberta)'
    if raiz == 'acesa': return None if isinstance(val, bool) else '"acesa" é sim ou não'
    if raiz == 'cat': return None if _cat_ok(val) else 'a categoria da sala vai de 0 a 7'
    if raiz == 'atento': return None if val in M.ATENTOS and _int(val) else 'quem mora na sala está −1 (dormindo), 0 (à toa) ou 1 (alerta)'
    if raiz == 'armadilhas':
        if not isinstance(val, list): return 'as armadilhas são uma lista'
        return next((e for e in (_armadilha_erro(a) for a in val) if e), None)
    if raiz == 'guardado':
        if val is None: return None
        if not isinstance(val, dict) or not isinstance(val.get('nome'), str) or not val['nome'] or not (val.get('fechadura') is None or _cat_ok(val['fechadura'])) or not isinstance(val.get('aberto', False), bool):
            return 'o guardado é {nome, fechadura: categoria ou nada, aberto: sim ou não} (o que tem dentro é o estoque e as peças guardadas da sala: não se lista)'
        return None
    if raiz == 'segredos':
        if not isinstance(val, list) or any(not isinstance(x, dict) or not isinstance(x.get('para'), str) or not _cat_ok(x.get('cat')) for x in val): return 'os segredos são [{para: SALA, cat: 0 a 7}]'
        return None
    if raiz == 'chefe':
        if val is None: return None
        if not isinstance(val, dict) or not _chefe_ok(val.get('qual')) or not isinstance(val.get('vivo', True), bool): return 'o chefe da sala é {qual: um chefe que a tabela conhece, vivo: sim ou não} (o dragão não: a sala dele leva "dragao")'
        return None
    return None


def _morre(E, pid):
    """A MORTE, numa regra só: o morto não fica com nada. As peças e os núcleos dele caem SOLTOS onde ele morreu; as obras se desfazem; a carga e a prata ficam no
    estoque desse lugar. Quem foi junto na saída de outro deixa de estar nela; a saída de quem a comandava fica escrita, para a caça fazer as contas."""
    p = E['gente'][pid]; lid = onde(E, pid); l = E['lugares'][lid]; dia = E['relogio']['dia']
    p['morte'] = dict(dia=dia, bloco=E['relogio']['bloco'], onde=lid, prata=p['moedas'] if _int(p.get('moedas')) and p['moedas'] > 0 else 0,
                      carga={b: q for b, q in (p.get('carga') or {}).items() if _num(q) and q > 0})       # o que ele deixou (a MESA de quem morreu diz); save antigo: sem estes dois campos, não se diz quanto
    vestia = [i for i, it in E['itens']['itens'].items() if it.get('dono') == pid and it.get('uso')]
    if vestia and (E.get('mundo') or {}).get('meta'): p['morte']['vestia'] = vestia      # o que estava em uso (etapa final, só no mundo com região: o nêmesis fica com isto)
    if p.get('maldicoes'): p['morte']['maldicoes'] = p['maldicoes']; p['maldicoes'] = []       # o morto não tem maldição andando: ficam escritas na morte dele
    for oid in [k for k, o in E['itens'].get('obras', {}).items() if o.get('quem') == pid]: del E['itens']['obras'][oid]
    for it in E['itens']['itens'].values():
        if it.get('dono') == pid:
            it['dono'] = None; it['uso'] = None; it['onde'] = lid; it['solto'] = True; it['corpo'] = pid      # solta, junto do corpo: `corpo` diz de quem era (sai quando a peça ganha dono ou vai para a prateleira)
            it.setdefault('historia', []).append(f"Dia {dia}: ficou com o corpo de {p['nome']} {em(E, lid)}")
    est = l.setdefault('estoque', {})
    dm = l.setdefault('do_morto', {}) if l.get('tipo') == 'sala' else {}     # NA SALA DA MASMORRA o estoque é também o tesouro: a parte do morto fica escrita à parte (junto do corpo), e não se pega
    for b, q in (p.get('carga') or {}).items():
        if _num(q) and q > 0: est[b] = est.get(b, 0) + q; dm[b] = dm.get(b, 0) + q
    p['carga'] = {}
    if p['moedas'] > 0: est['prata'] = est.get('prata', 0) + p['moedas']; dm['prata'] = dm.get('prata', 0) + p['moedas']; p['moedas'] = 0
    if l.get('tipo') == 'sala' and not l['do_morto']: del l['do_morto']
    s = (p.get('marca') or {}).get('caca')
    if isinstance(s, dict) and s.get('de'): p['marca'].pop('caca')
    d = (p.get('marca') or {}).get('masmorra')                 # A DESCIDA (etapa 4b): quem ia junto e morre sai dela; quem comanda e morre solta quem ia junto (saem sozinhos:
    if isinstance(d, dict) and d.get('de') is not None: p['marca'].pop('masmorra')       # é cena do Mestre); a descida de quem comandava fica escrita, para a masmorra fazer as contas
    elif isinstance(d, dict):
        for q in E['gente'].values():
            dq = (q.get('marca') or {}).get('masmorra') if isinstance(q, dict) and isinstance(q.get('marca'), dict) else None
            if isinstance(dq, dict) and dq.get('de') == pid: q['marca'].pop('masmorra')
    v = (p.get('marca') or {}).get('viagem')                 # A VIAGEM (etapa final): quem ia junto e morre sai dela; quem comanda e morre solta quem ia junto (cena do Mestre);
    if isinstance(v, dict) and v.get('de') is not None: p['marca'].pop('viagem')        # a viagem de quem comandava fica escrita, para a viagem.py fazer as contas
    elif isinstance(v, dict):
        for q in E['gente'].values():
            vq = (q.get('marca') or {}).get('viagem') if isinstance(q, dict) and isinstance(q.get('marca'), dict) else None
            if isinstance(vq, dict) and vq.get('de') == pid: q['marca'].pop('viagem')


def _nasce_pessoa(E, ef):
    if len(ef) != 4 or not isinstance(ef[2], str) or not isinstance(ef[3], dict): return _erro(ef, "use ['pessoa', 'nasce', id, registro]")
    pid, r = ef[2], ef[3]
    if not pid or pid == 'nasce' or pid in E['gente']: return _erro(ef, f'já há a pessoa "{pid}" (ou o id não serve)')
    if not r.get('nome') or not isinstance(r['nome'], str): return _erro(ef, 'a pessoa pede um nome')
    if not _int(r.get('nivel')) or r['nivel'] < 1: return _erro(ef, 'a pessoa pede um nível (1 ou mais)')
    at = r.get('atributos')
    if not isinstance(at, dict) or set(at) != set(T.ATRIBUTOS) or not all(_num(v) and v > 0 for v in at.values()): return _erro(ef, f'a pessoa pede os seis atributos ({", ".join(T.ATRIBUTOS)})')
    if r.get('lugar') not in E['lugares']: return _erro(ef, f'não há o lugar "{r.get("lugar")}"')
    of = r.get('grau_oficio', 'diarista')
    if of not in M.SALARIO: return _erro(ef, f'grau de ofício desconhecido: "{of}" (os que há: {", ".join(M.SALARIO)})')
    ma = r.get('maestria') or {}; tr = r.get('treino') or {}; ca = r.get('carga') or {}; mo = r.get('moedas', 0)
    if not isinstance(ma, dict) or any((k not in T.FAMILIAS and k not in M.OFICIOS) or v not in T.MAESTRIAS for k, v in ma.items()): return _erro(ef, 'maestria fora da tabela (arma ou ofício: 0, 2, 4, 6 ou 8)')
    if not isinstance(tr, dict) or any((k not in T.FAMILIAS and k not in M.OFICIOS) or not _num(v) or v < 0 for k, v in tr.items()): return _erro(ef, 'treino fora da tabela (arma ou ofício: blocos)')
    if not isinstance(ca, dict) or any(not _num(v) or v <= 0 for v in ca.values()): return _erro(ef, 'a carga é {bem: quanto}, acima de zero')
    if not _int(mo) or mo < 0: return _erro(ef, 'a prata é um número inteiro de zero para cima')
    if r.get('jogador') and any(q.get('jogador') for q in E['gente'].values()): return _erro(ef, 'já há um personagem do jogador')
    ruins = [k for k in r if k not in ('nome', 'nivel', 'atributos', 'lugar', 'grau_oficio', 'maestria', 'treino', 'carga', 'moedas', 'jogador', 'marca', 'sobre', 'lacos') + NASCE_MAGIA + PESSOA_4B + NASCE_REGIAO]
    if ruins: return _erro(ef, f'a pessoa não tem o campo "{ruins[0]}"')
    p = dict(nome=r['nome'], lugar=r['lugar'], grau_oficio=of, nivel=r['nivel'], atributos={a: at[a] for a in T.ATRIBUTOS}, maestria=dict(ma), treino=dict(tr), moedas=mo,
             corpo={m: 0 for m in M.MEDIDORES}, pv=0, feridas=[], estado='vivo', marca=copy.deepcopy(r.get('marca') or {}), carga=dict(ca))
    p['pv'] = pv_max(p)
    if r.get('jogador'): p['jogador'] = True
    for k in NASCE_MAGIA:                                   # a etapa da magia: o talento, o dom, a inclinação, os feitiços, a tradição, o voto, o laço, a dívida, a Mana
        if k in r:
            e = _magia_erro(E, p, 'feiticos' if k == 'feiticos' else k, r[k])
            if e: return _erro(ef, e)
            p[k] = copy.deepcopy(r[k]) if k != 'talento' or r[k] is None else {c: g for c, g in r[k].items() if g}
    for k in PESSOA_4B:                                     # a etapa 4b: o povo, a idade, a segunda inclinação (o povo primeiro: a idade e a inclinação dependem dele)
        if r.get(k) is not None:
            e = _pessoa4b_erro(E, p, k, r[k])
            if e: return _erro(ef, e)
            p[k] = r[k]
    if r.get('sobre'): p['sobre'] = str(r['sobre'])
    for k in NASCE_REGIAO:                                  # a etapa final: a casa, os pais, o papel, a guilda, o rival, a fama, a memória
        if r.get(k) is not None:
            e = _regiao_erro(E, pid, p, k, r[k])
            if e: return _erro(ef, e)
            p[k] = copy.deepcopy(r[k])
    if r.get('lacos'):
        if not isinstance(r['lacos'], dict) or any(k not in E['gente'] or v not in M.LACOS for k, v in r['lacos'].items()): return _erro(ef, f'os laços são {{pessoa que existe: um de {", ".join(M.LACOS)}}}')
        p['lacos'] = dict(r['lacos'])
    E['gente'][pid] = p


def _nasce_lugar(E, ef):
    if len(ef) != 4 or not isinstance(ef[2], str) or not isinstance(ef[3], dict): return _erro(ef, "use ['lugar', 'nasce', id, registro]")
    lid, r = ef[2], copy.deepcopy(ef[3])
    if not lid or lid == 'nasce' or lid in E['lugares']: return _erro(ef, f'já há o lugar "{lid}" (ou o id não serve)')
    if not r.get('nome') or not isinstance(r['nome'], str): return _erro(ef, 'o lugar pede um nome')
    est = r.setdefault('estoque', {})
    if not isinstance(est, dict) or any(not _num(v) or v < 0 for v in est.values()): return _erro(ef, 'o estoque é {bem: quanto}, de zero para cima')
    r.setdefault('tipo', 'ermo')
    for k, v in r.items():
        if k in ('nome', 'em', 'tipo', 'habitat', 'sobre'):
            if not isinstance(v, str): return _erro(ef, f'"{k}" é texto')
        elif k != 'estoque':
            e = _lugar_erro(E, k, None, v)
            if e: return _erro(ef, e)
    E['lugares'][lid] = r


def _um(E, ef):
    """aplica UM efeito em E (que pode ser uma cópia de ensaio). Devolve None, ou o texto do erro."""
    if not isinstance(ef, (list, tuple)) or not ef: return _erro(ef, 'efeito vazio')
    v = ef[0]
    if v == 'relogio':
        if len(ef) != 2 or not _int(ef[1]) or ef[1] < 1: return _erro(ef, 'o tempo anda 1 bloco ou mais')
        t = agora(E) + ef[1]; E['relogio']['dia'], E['relogio']['bloco'] = t // M.BLOCOS_DIA + 1, t % M.BLOCOS_DIA; return
    if v == 'pessoa' and len(ef) > 1 and ef[1] == 'nasce': return _nasce_pessoa(E, ef)
    if v == 'pessoa':
        if len(ef) != 5: return _erro(ef, "use ['pessoa', id, campo, 'soma'|'poe', valor]")
        _, pid, campo, op, val = ef; p = E['gente'].get(pid) if isinstance(pid, str) else None
        if not p: return _erro(ef, f'não há a pessoa "{pid}"')
        if not isinstance(campo, str): return _erro(ef, 'o campo é um nome')
        raiz, _, sub = campo.partition('.')
        if campo in PESSOA_REGIAO or raiz == 'lacos': return _pessoa_regiao(E, pid, p, campo, raiz, sub, op, val, ef)
        if campo in PESSOA_MAGIA: return _pessoa_magia(E, pid, p, campo, op, val, ef)
        if campo in PESSOA_4B:
            if op != 'poe': return _erro(ef, f'"{campo}" só aceita "poe"')
            e = _pessoa4b_erro(E, p, campo, val) if val is not None else None
            if e: return _erro(ef, e)
            if val is None: p.pop(campo, None)
            else: p[campo] = val
            return
        if raiz == 'carga':
            if not sub or op != 'soma' or not _int(val): return _erro(ef, "a carga muda por ['pessoa', id, 'carga.BEM', 'soma', número inteiro]")
            if not bem_conhecido(sub): return _erro(ef, f'não se carrega "{sub}" (carregam-se: {", ".join(M.BENS)}; e a matéria com a categoria, de 0 a {M.MATERIA_ATE}: metal:0, couro:1...)')
            if val > 0 and p['estado'] == 'morto': return _erro(ef, f'{p["nome"]} morreu: não recebe carga (quem morre não fica com nada)')
            d = p.setdefault('carga', {}); q = d.get(sub, 0) + val
            if q < 0: return _erro(ef, f'{p["nome"]} só carrega {d.get(sub, 0)} de {sub}')
            if q: d[sub] = q
            else: d.pop(sub, None)
            return
        if raiz in ('treino', 'maestria', 'marca'):
            if not sub: return _erro(ef, f'"{raiz}" pede o nome depois do ponto (treino.espada)')
            if raiz == 'marca' and sub in ('caca', 'masmorra', 'viagem') and op == 'poe' and val is not None:      # UMA SAÍDA, UMA DESCIDA E UMA VIAGEM NÃO ANDAM JUNTAS (etapas 4b e final)
                for outra in [x for x in ('caca', 'masmorra', 'viagem') if x != sub]:
                    if isinstance((p.get('marca') or {}).get(outra), dict): return _erro(ef, f"{p['nome']} já está n{dict(masmorra='a descida', caca='uma saída ao ermo', viagem='a viagem')[outra]} aberta: feche-a antes")
                if sub == 'masmorra':
                    e = _descida_erro(E, val, pid)
                    if e: return _erro(ef, f'a descida (marca.masmorra) {e}')
                if sub == 'viagem':
                    e = _viagem_erro(E, val, pid)
                    if e: return _erro(ef, f'a viagem (marca.viagem) {e}')
            if raiz != 'marca' and sub not in T.FAMILIAS and sub not in M.OFICIOS: return _erro(ef, f'arma ou ofício desconhecido: "{sub}"')
            if raiz != 'marca' and not _num(val): return _erro(ef, f'"{campo}" é um número')
            d = p.setdefault(raiz, {})
            if op == 'soma':
                if not _num(val) or not _num(d.get(sub, 0)): return _erro(ef, f'"{campo}" não é número: não se soma')
                d[sub] = d.get(sub, 0) + val
            elif op == 'poe': d[sub] = val
            else: return _erro(ef, 'a operação é "soma" ou "poe"')
            if raiz == 'maestria' and d[sub] not in T.MAESTRIAS: return _erro(ef, f'maestria fora da tabela: {d[sub]}')
            return
        if campo not in CAMPOS: return _erro(ef, f'campo desconhecido: "{campo}" (os que existem: {", ".join(CAMPOS)}, treino.ARMA, maestria.ARMA, marca.X, carga.BEM)')
        if op != CAMPOS[campo]: return _erro(ef, f'"{campo}" só aceita "{CAMPOS[campo]}"')
        if CAMPOS[campo] == 'soma' and not _num(val): return _erro(ef, f'"{campo}" soma um número')
        if campo == 'lugar':
            if val not in E['lugares']: return _erro(ef, f'não há o lugar "{val}"')
            p['lugar'] = val
        elif campo == 'estado':
            if val not in M.ESTADOS: return _erro(ef, f'estado desconhecido: "{val}"')
            if val == 'morto' and p['estado'] != 'morto': _morre(E, pid)
            if val == 'vivo': p.pop('morte', None)
            p['estado'] = val
        elif campo == 'grau_oficio':
            if val not in M.SALARIO: return _erro(ef, f'grau de ofício desconhecido: "{val}" (os que há: {", ".join(M.SALARIO)})')
            p['grau_oficio'] = val
        elif campo in M.MEDIDORES: p['corpo'][campo] = max(0, min(M.MED_MAX, p['corpo'][campo] + val))
        elif campo == 'pv':
            p['pv'] = max(0, min(pv_max(p), p['pv'] + val))
            if p['pv'] >= pv_max(p): p.pop('funda', None)        # a ferida funda some quando o PV enche
        elif campo == 'moedas':
            if not _int(val): return _erro(ef, 'a prata é inteira')
            if val > 0 and p['estado'] == 'morto': return _erro(ef, f'{p["nome"]} morreu: não recebe prata (quem morre não fica com nada)')
            if p['moedas'] + val < 0: return _erro(ef, f'{p["nome"]} tem {p["moedas"]} de prata e não paga {-val}')
            p['moedas'] += val
        else: p[campo] += val
        return
    if v == 'ferida':
        p = E['gente'].get(ef[1]) if len(ef) > 2 and isinstance(ef[1], str) else None
        if not p: return _erro(ef, 'não há essa pessoa')
        if ef[2] == 'abre' and len(ef) == 5:
            if ef[3] not in T.PARTES: return _erro(ef, f'parte desconhecida: "{ef[3]}"')
            p['feridas'].append(dict(parte=ef[3], grave=bool(ef[4]), dia=E['relogio']['dia'], repouso=0)); return
        if ef[2] == 'repousa' and len(ef) == 4 and _num(ef[3]):
            for f in p['feridas']: f['repouso'] += ef[3]
            return
        if ef[2] == 'sara' and len(ef) == 4:
            if not _int(ef[3]) or not 0 <= ef[3] < len(p['feridas']): return _erro(ef, 'não há essa ferida')
            p['feridas'].pop(ef[3]); return
        return _erro(ef, "use ['ferida', id, 'abre', parte, grave], ['ferida', id, 'repousa', n] ou ['ferida', id, 'sara', indice]")
    if v == 'maldicao': return _maldicao(E, ef)
    if v == 'lugar' and len(ef) > 1 and ef[1] == 'nasce': return _nasce_lugar(E, ef)
    if v == 'lugar':
        if len(ef) != 5 or ef[3] not in ('soma', 'poe') or not isinstance(ef[2], str): return _erro(ef, "use ['lugar', id, campo ou campo.sub, 'soma'|'poe', valor]")
        l = E['lugares'].get(ef[1]) if isinstance(ef[1], str) else None
        if not l: return _erro(ef, f'não há o lugar "{ef[1]}"')
        raiz, _, sub = ef[2].partition('.')
        if raiz in ('estoque', 'nome'): return _erro(ef, f'"{raiz}" não se muda por aqui (o estoque tem o verbo dele)')
        if sub and not isinstance(l.get(raiz, {}), dict): return _erro(ef, f'"{raiz}" não tem partes')
        d = l.setdefault(raiz, {}) if sub else l; k = sub or raiz
        if ef[3] == 'poe':
            e = _lugar_erro(E, raiz, sub, ef[4])
            if e: return _erro(ef, e)
            d[k] = copy.deepcopy(ef[4])
        else:
            if not _num(d.get(k, 0)) or not _num(ef[4]): return _erro(ef, f'"{ef[2]}" não é número')
            q = d.get(k, 0) + ef[4]
            if q < 0: return _erro(ef, f'{l["nome"]} só tem {d.get(k, 0)} de {ef[2]}')
            e = _lugar_erro(E, raiz, sub, q)
            if e: return _erro(ef, e)
            d[k] = q
        return
    if v == 'obra':
        O = E['itens'].setdefault('obras', {})
        if len(ef) == 3 and ef[1] == 'abre':
            o = copy.deepcopy(ef[2])
            if not isinstance(o, dict) or o.get('quem') not in E['gente']: return _erro(ef, 'a obra pede um registro com "quem" (uma pessoa que existe)')
            if o.get('lugar') not in E['lugares']: return _erro(ef, 'a obra pede o "lugar" onde está a bancada (um lugar que existe)')
            if not _num(o.get('pede')) or o['pede'] < 1 or not _num(o.get('blocos', 0)) or not 0 <= o.get('blocos', 0) <= o['pede']: return _erro(ef, 'a obra pede "pede" (blocos, 1 ou mais) e "blocos" entre zero e isso')
            if o.get('molde') is not None and not _molde_obra_ok(o['molde']): return _erro(ef, 'o molde da obra (a parte 2, fase 1a) é a chave de um efeito do catálogo (o molde de mestre: molde=CHAVE)')
            E['itens']['oseq'] = E['itens'].get('oseq', 0) + 1; o['id'] = f"o{E['itens']['oseq']:04d}"; o.setdefault('blocos', 0); o.setdefault('dia', E['relogio']['dia']); O[o['id']] = o; return
        o = O.get(ef[1]) if len(ef) > 2 and isinstance(ef[1], str) else None
        if not o: return _erro(ef, 'não há essa obra')
        if len(ef) == 3 and ef[2] == 'fecha': del O[ef[1]]; return
        if len(ef) == 5 and ef[3] in ('soma', 'poe') and ef[2] in ('blocos', 'pede'):
            q = o.get(ef[2], 0) + ef[4] if ef[3] == 'soma' and _num(ef[4]) else ef[4]
            if not _num(q) or q < 0 or (ef[2] == 'blocos' and q > o.get('pede', q)) or (ef[2] == 'pede' and (q < 1 or q < o.get('blocos', 0))): return _erro(ef, 'os blocos da obra ficam entre zero e o que ela pede')
            o[ef[2]] = q; return
        if len(ef) == 5 and ef[3] == 'poe' and ef[2] in ('id', 'quem', 'lugar', 'tipo', 'materia', 'nucleo', 'item', 'para'):
            c, x = ef[2], ef[4]
            certo = (c == 'lugar' and x in E['lugares']) or (c == 'materia' and isinstance(x, dict) and all(bem_conhecido(k) and _num(q) and q >= 0 for k, q in x.items())) \
                or (c == 'nucleo' and (x is None or E['itens']['itens'].get(x, {}).get('tipo') == 'nucleo')) or (c == 'item' and x in E['itens']['itens']) or (c == 'para' and x in E['gente'])
            if not certo: return _erro(ef, f'a obra não aceita "{c}" = {json.dumps(x, ensure_ascii=False)} (o lugar, a matéria, o núcleo, a peça e a pessoa têm de existir; quem a faz e o tipo dela não mudam)')
            o[c] = copy.deepcopy(x); return
        if len(ef) == 5 and ef[3] == 'soma' and _num(ef[4]) and _num(o.get(ef[2], 0)): o[ef[2]] = o.get(ef[2], 0) + ef[4]; return
        if len(ef) == 5 and ef[3] == 'poe': o[ef[2]] = ef[4]; return
        return _erro(ef, "use ['obra', 'abre', registro], ['obra', id, campo, 'soma'|'poe', valor] ou ['obra', id, 'fecha']")
    if v == 'estoque':
        if len(ef) != 5 or ef[3] != 'soma' or not _num(ef[4]) or not isinstance(ef[2], str): return _erro(ef, "use ['estoque', lugar, bem, 'soma', número]")
        l = E['lugares'].get(ef[1]) if isinstance(ef[1], str) else None
        if not l: return _erro(ef, f'não há o lugar "{ef[1]}"')
        if ef[2] == 'prata' and not _int(ef[4]): return _erro(ef, 'a prata é inteira')
        q = l['estoque'].get(ef[2], 0) + ef[4]
        if q < 0: return _erro(ef, f'{l["nome"]} só tem {l["estoque"].get(ef[2], 0)} de {ef[2]}')
        dm = (l.get('do_morto') or {}).get(ef[2], 0)
        if ef[4] < 0 and _num(dm) and q < dm:                    # a parte que ficou junto do corpo de um morto não sai do estoque sozinha: o Mestre a solta antes, no mesmo evento
            return _erro(ef, f'{dm:g} de {ef[2]} {de(E, ef[1])} ficaram junto do corpo de quem morreu ali: não mudam de mão sozinhos (o Mestre, no mesmo evento e antes disto: '
                             f"['lugar', '{ef[1]}', 'do_morto.{ef[2]}', 'soma', -N])")
        l['estoque'][ef[2]] = q; return
    if v == 'item' and len(ef) == 3 and ef[1] == 'nasce':
        it = copy.deepcopy(ef[2])
        if not isinstance(it, dict) or it.get('tipo') not in TIPOS_ITEM or 'dur' not in it or 'cat' not in it or not it.get('nome'): return _erro(ef, 'o registro tem de sair do itens.item() (ou ser um núcleo: tipo, cat, nome, dur)')
        if not _int(it['cat']) or not 0 <= it['cat'] < len(T.CATS): return _erro(ef, f'categoria fora da tabela: {it["cat"]} (vai de 0, Comum, a {len(T.CATS) - 1})')
        e = _item_magia_erro(it) or _item4b_erro(it)
        if e: return _erro(ef, e)
        if not (isinstance(it['dur'], list) and len(it['dur']) == 2 and all(_int(x) for x in it['dur']) and 0 <= it['dur'][0] <= it['dur'][1]): return _erro(ef, 'a durabilidade é [quanto tem, quanto cabe]')
        if it.get('dono') is not None and it['dono'] not in E['gente']: return _erro(ef, f'não há a pessoa "{it["dono"]}"')
        if it.get('dono') is not None and E['gente'][it['dono']]['estado'] != 'vivo': return _erro(ef, f'{E["gente"][it["dono"]]["nome"]} morreu: não recebe peça')
        if it.get('onde') is not None and it['onde'] not in E['lugares']: return _erro(ef, f'não há o lugar "{it["onde"]}"')
        if it.get('dono') is not None and it.get('onde') is not None: return _erro(ef, 'a peça nasce com dono OU num lugar, não os dois')
        if it.get('dono') is None and it.get('onde') is None: return _erro(ef, 'a peça nasce com dono (dono=) ou num lugar (onde=): solta no nada, não existe')
        if it.get('solto') and it.get('dono') is not None: return _erro(ef, 'peça com dono não está solta')
        if not it.get('solto'): it.pop('solto', None)
        E['itens']['seq'] += 1; it['id'] = f"i{E['itens']['seq']:04d}"; it['uso'] = None; E['itens']['itens'][it['id']] = it; return
    if v == 'item' and len(ef) == 3 and ef[2] == 'some':
        if ef[1] not in E['itens']['itens']: return _erro(ef, f'não há o item "{ef[1]}" no Livro de Itens')
        del E['itens']['itens'][ef[1]]; return
    if v == 'item':
        if len(ef) != 5: return _erro(ef, "use ['item', id, campo, 'poe'|'soma', valor], ['item', 'nasce', registro] ou ['item', id, 'some']")
        it = E['itens']['itens'].get(ef[1]) if isinstance(ef[1], str) else None
        if not it: return _erro(ef, f'não há o item "{ef[1]}" no Livro de Itens')
        _, _, campo, op, val = ef
        if campo in ('dono', 'uso') and op == 'poe' and it.get(campo) and val != it.get(campo) and _presa(E, it):
            return _erro(ef, f'a mão não larga {it["nome"]}: a maldição que veio dela anda em {E["gente"][it["dono"]]["nome"]} (quebre-a antes, no mesmo evento)')
        if campo == 'encanto': return _encanto(E, it, op, val, ef)
        if campo in ('maldita', 'benta', 'veneno') and op == 'poe':
            if val is None: it.pop(campo, None); return
            x = dict(it); x[campo] = val; e = _item_magia_erro(x)
            if e: return _erro(ef, e)
            it[campo] = copy.deepcopy(val); return
        if campo == 'dono' and op == 'poe':
            if val is not None and val not in E['gente']: return _erro(ef, f'não há a pessoa "{val}"')
            if val is not None and E['gente'][val]['estado'] != 'vivo': return _erro(ef, f'{E["gente"][val]["nome"]} morreu: não recebe peça')
            it['dono'] = val; it['uso'] = None
            if val is not None: it['onde'] = None; it.pop('solto', None); it.pop('corpo', None)
            return
        if campo == 'onde' and op == 'poe':
            if val is not None and val not in E['lugares']: return _erro(ef, f'não há o lugar "{val}"')
            if val is not None and it.get('dono'): return _erro(ef, 'peça com dono não fica largada num lugar: tire o dono antes')
            it['onde'] = val
            if val is None: it.pop('solto', None); it.pop('corpo', None)
            return
        if campo == 'solto' and op == 'poe':
            if val and (it.get('dono') or it.get('onde') is None): return _erro(ef, 'só fica solta (caída no chão) a peça sem dono que está num lugar')
            if val: it['solto'] = True
            else: it.pop('solto', None); it.pop('corpo', None)
            return
        if campo == 'sob_medida' and op == 'poe':
            if val is not None and not (isinstance(val, dict) and val.get('dono') and _num(val.get('grau', 0)) and T.SOB_MEDIDA_GRAUS[0] <= val.get('grau', 0) <= T.SOB_MEDIDA_GRAUS[1]): return _erro(ef, 'o sob medida é {dono, grau de 1 a 4}, ou nada')
            if it['tipo'] == 'nucleo': return _erro(ef, 'núcleo não se ajusta')
            it['sob_medida'] = val; return
        if campo == 'talhe' and op == 'poe':                # O TALHE DA ARMADURA (etapa 4b): o corpo para que foi feita; sem o campo, de gente; "miúdo", do pequenino e do gnomo
            if it['tipo'] != 'armadura': return _erro(ef, 'só a armadura tem talhe (a arma e o escudo servem em todo corpo)')
            if val not in (None, 'miúdo'): return _erro(ef, 'o talhe da armadura é "miúdo", ou nada (de gente)')
            d = E['gente'].get(it.get('dono')) if it.get('dono') else None
            if it.get('uso') and isinstance(d, dict) and (val or 'gente') != corpo_de(d): return _erro(ef, f'{it["nome"]} está em uso e deixaria de servir em {d["nome"]}: tire-a de uso antes, no mesmo evento')
            if val is None: it.pop('talhe', None)
            else: it['talhe'] = val
            return
        if campo == 'historia' and op == 'junta': it.setdefault('historia', []).append(str(val)); return
        if campo == 'efeito' and op == 'junta':              # (a etapa dos efeitos) um efeito novo na peça: {chave, cheio?, emprestado?} (de ferramenta) ou {chave, valor?} (os de luta de hoje)
            import itens as IT
            if not isinstance(val, dict) or val.get('chave') not in IT.EFEITOS: return _erro(ef, f'o efeito é {{chave, cheio?, emprestado?}}, com a chave de um dos que há ({", ".join(IT.EFEITOS)})')
            if it['tipo'] not in IT.EFEITOS[val['chave']][1]: return _erro(ef, f'o efeito "{val["chave"]}" não vale em {it["tipo"]} (vale em: {", ".join(IT.EFEITOS[val["chave"]][1])})')
            if any(isinstance(e, dict) and e.get('chave') == val['chave'] for e in it.get('efeitos') or []): return _erro(ef, f'{it["nome"]} já tem o efeito "{val["chave"]}"')
            e = _efeito_erro(it, val, novo=True)
            if e: return _erro(ef, e)
            it.setdefault('efeitos', []).append(copy.deepcopy(val)); return
        if campo == 'efeitos_livres' and op in ('poe', 'soma'):     # os efeitos que a faixa (ou a obra-prima) ainda deixa escolher
            q = (val if op == 'poe' else (it.get('efeitos_livres') or 0) + val) if _int(val) else None
            if q is None or q < 0: return _erro(ef, 'os efeitos por escolher são um número inteiro, de zero para cima')
            if q < (it.get('cheios_livres') or 0): return _erro(ef, f'{it["nome"]} ficaria com mais cheios ({it.get("cheios_livres")}) do que efeitos por escolher ({q}): tire os cheios antes, no mesmo evento')
            if (len(it.get('efeitos') or []) + q) > _teto_ef(it): return _erro(ef, f'{it["nome"]} passaria do teto de efeitos dela ({_teto_ef(it)})')
            if q: it['efeitos_livres'] = q
            else: it.pop('efeitos_livres', None)
            return
        if campo == 'cheios_livres' and op in ('poe', 'soma'):      # (a parte 2, fase 1a) quantos dos efeitos por escolher podem ser cheios (o número da categoria de cima)
            q = (val if op == 'poe' else (it.get('cheios_livres') or 0) + val) if _int(val) else None
            if q is None or q < 0: return _erro(ef, 'os cheios por escolher são um número inteiro, de zero para cima')
            if q > (it.get('efeitos_livres') or 0): return _erro(ef, f'{it["nome"]} não tem tantos efeitos por escolher para encher ({it.get("efeitos_livres") or 0}): um cheio por efeito')
            if q: it['cheios_livres'] = q
            else: it.pop('cheios_livres', None)
            return
        if campo == 'nome' and op == 'poe' and val: it['nome'] = str(val); return
        if campo == 'uso' and op == 'poe':
            if val not in (None,) + PARTES_VESTE: return _erro(ef, f'uso desconhecido: "{val}" (arma, arma2, escudo, veste, foco, pescoco ou nada)')
            if val and not it.get('dono'): return _erro(ef, 'peça sem dono não se veste')
            if val and it['tipo'] != USO_DO_TIPO[val]: return _erro(ef, f'{it["nome"]} é {it["tipo"]}: não vai em "{val}"')
            if val == 'veste' and not serve(it, E['gente'][it['dono']]):
                d = E['gente'][it['dono']]
                return _erro(ef, f'{it["nome"]} é de {"gente miúda" if it.get("talhe") == "miúdo" else "gente grande"}: não serve no corpo de {d["nome"]}. Um ferreiro a ajusta (`oficio.py ajustar {it.get("id", "ITEM")} para={it["dono"]}`)')
            it['uso'] = val; return
        if campo == 'dur' and op == 'soma' and _num(val):
            if it['tipo'] in ('nucleo', 'elixir', 'escrito', 'chave'): return _erro(ef, f'{it["tipo"]} não gasta nem se conserta')
            it['dur'][0] = max(0, min(it['dur'][1], it['dur'][0] + int(val))); return
        return _erro(ef, 'no item muda-se: dono, uso, onde, solto, sob_medida, nome, maldita, benta, veneno, talhe (poe) · dur (soma) · historia, efeito (junta) · efeitos_livres, cheios_livres (poe, soma) · encanto (grava, gasta, apaga)')
    if v == 'mundo': return _mundo(E, ef)
    return _erro(ef, f'verbo desconhecido: "{v}" (os que existem: relogio, pessoa, ferida, estoque, lugar, item, obra, maldicao, mundo)')


# ---------- a etapa final no gravador (as formas: projeto/ETAPA_FINAL.md, seções 1 a 3) ----------
PESSOA_REGIAO = ('casa', 'pais', 'memoria', 'fama', 'querer', 'papel', 'guilda', 'rival', 'herdeiro', 'jogador')
NASCE_REGIAO = ('casa', 'pais', 'memoria', 'fama', 'querer', 'papel', 'guilda', 'rival')       # o que a pessoa pode trazer ao nascer (os laços, à parte)
REGIAO_EVENTOS = dict(casa=('gera', 'mestre', 'heranca'), pais=('gera', 'mestre'), papel=('gera', 'mestre'), rival=('gera', 'mestre'),
                      herdeiro=('herdeiro', 'mestre', 'heranca'), jogador=('heranca',))      # os campos que só entram em certos eventos (os outros: em todos)


def _secao(E, nome):
    """uma seção do mundo.json (o dicionário ou a lista; ausente: vazia)"""
    W = E.get('mundo') or {}
    return W.get(nome) or ([] if nome in M.SECOES_LISTA else {})


def _memoria_ok(x):
    return isinstance(x, dict) and _int(x.get('dia')) and isinstance(x.get('o_que'), str) and x['o_que'] and _int(x.get('peso')) and -M.MEMORIA_PESO <= x['peso'] <= M.MEMORIA_PESO \
        and (x.get('de') is None or isinstance(x['de'], str))


def _regiao_erro(E, pid, p, campo, v):
    """o que um campo da etapa final aceita na pessoa (None: aceita). Serve ao gravador, ao nascer e aos invariantes."""
    if campo == 'casa': return None if v is None or v in _secao(E, 'casas') else f'não há a casa "{v}" (mundo.casas)'
    if campo == 'pais': return None if isinstance(v, list) and len(v) <= 2 and all(isinstance(x, str) and x for x in v) else 'os pais são uma lista de até dois ids'
    if campo == 'memoria': return None if isinstance(v, list) and len(v) <= M.MEMORIA_MAX and all(_memoria_ok(x) for x in v) else f'a memória é uma lista de até {M.MEMORIA_MAX} fatos {{dia, de, o_que, peso de −{M.MEMORIA_PESO} a {M.MEMORIA_PESO}}}'
    if campo == 'fama': return None if _num(v) else 'a fama é um número'
    if campo == 'querer': return None if v is None or (isinstance(v, dict) and isinstance(v.get('o_que'), str) and v['o_que']) else 'o querer é {o_que, alvo, ate}, ou nada'
    if campo == 'papel': return None if v is None or v in M.PAPEIS else f'o papel é um de: {", ".join(M.PAPEIS)}'
    if campo == 'guilda': return None if v is None or v in _secao(E, 'guildas') else f'não há a guilda "{v}" (mundo.guildas)'
    if campo in ('rival', 'jogador'): return None if v in (None, True, False) else f'"{campo}" é sim (True) ou nada'
    if campo == 'herdeiro':
        if v is None: return None
        if not p.get('jogador'): return 'só o personagem do jogador nomeia herdeiro'
        q = E['gente'].get(v) if isinstance(v, str) else None
        if not isinstance(q, dict) or v == pid: return f'o herdeiro é outra pessoa que existe (veio "{v}")'
        if q.get('estado') != 'vivo': return f'{q["nome"]} morreu: não herda'
        return None
    return None


def _pessoa_regiao(E, pid, p, campo, raiz, sub, op, val, ef):
    """os verbos da etapa final na pessoa: os laços, a memória (junta), a fama (soma), o resto (poe)"""
    if raiz == 'lacos':
        if not sub or op != 'poe': return _erro(ef, "os laços mudam por ['pessoa', id, 'lacos.OUTRO', 'poe', tipo ou None]")
        if sub not in E['gente'] or sub == pid: return _erro(ef, f'o laço é com outra pessoa que existe (veio "{sub}")')
        if val is not None and val not in M.LACOS: return _erro(ef, f'o laço é um de: {", ".join(M.LACOS)}')
        d = p.setdefault('lacos', {})
        if val is None: d.pop(sub, None)
        else: d[sub] = val
        if not d: p.pop('lacos', None)
        return
    if campo == 'memoria' and op == 'junta':
        if not _memoria_ok(val): return _erro(ef, f'o fato da memória é {{dia, de, o_que, peso de −{M.MEMORIA_PESO} a {M.MEMORIA_PESO}}}')
        L = list(p.get('memoria') or []) + [copy.deepcopy(val)]
        while len(L) > M.MEMORIA_MAX: L.pop(min(range(len(L)), key=lambda i: (abs(L[i]['peso']), L[i]['dia'])))      # sai o de menor peso; entre iguais, o mais velho
        p['memoria'] = L; return
    if campo == 'fama' and op == 'soma':
        if not _num(val): return _erro(ef, 'a fama soma um número')
        p['fama'] = (p.get('fama') or 0) + val; return
    if op != 'poe': return _erro(ef, f'"{campo}" só aceita "poe"' + (' (e "junta")' if campo == 'memoria' else ' (e "soma")' if campo == 'fama' else ''))
    if campo == 'jogador' and val:
        if any(q.get('jogador') and q.get('estado') == 'vivo' for k, q in E['gente'].items() if k != pid and isinstance(q, dict)): return _erro(ef, 'o personagem do jogador está vivo: ninguém assume no lugar dele')
        if p.get('estado') != 'vivo': return _erro(ef, f'{p["nome"]} morreu: não assume')
    e = _regiao_erro(E, pid, p, campo, val)
    if e: return _erro(ef, e)
    if val is None: p.pop(campo, None)
    else: p[campo] = copy.deepcopy(val)


def _viagem_erro(E, v, pid=None):
    """a forma da viagem aberta (marca.viagem): o texto do erro, ou None"""
    if not isinstance(v, dict): return 'é um registro {estrada, sai, para, feitos, longe, com, fase...} (em quem vai junto: {de: quem comanda})'
    if v.get('de') is not None: return None if v['de'] in E['gente'] and v['de'] != pid else f'diz que foi junto com quem não há: "{v["de"]}"'
    s = E['lugares'].get(v.get('estrada')) if isinstance(v.get('estrada'), str) else None
    if not isinstance(s, dict) or s.get('tipo') != 'estrada': return f'não diz uma estrada que existe ("{v.get("estrada")}")'
    pt = s.get('ponta') or []
    if v.get('sai') not in pt or v.get('para') not in pt or v.get('sai') == v.get('para'): return 'não sai de uma ponta da estrada para a outra'
    if not (_int(v.get('longe')) and v['longe'] >= 1 and _int(v.get('feitos', 0)) and 0 <= v.get('feitos', 0) <= v['longe']): return 'tem os blocos fora da conta (feitos de zero até o longe)'
    if not isinstance(v.get('com', []), list) or any(c not in E['gente'] for c in v.get('com', [])): return 'tem em "com" quem não existe'
    if v.get('fase', 'anda') not in ('anda', 'encontro', 'luta'): return 'tem a fase torta (anda, encontro ou luta)'
    if v.get('fase') == 'luta' and not isinstance(v.get('luta'), str): return 'está em luta sem o arquivo dela'
    return None


def _mundo_forma(E, sec, rid, r):
    """a forma de um registro de uma seção do mundo.json (None: certo). As ligações com o resto do mundo são do valida."""
    Ls = E['lugares']
    if sec in M.SECOES_LISTA:
        if sec == 'cronica': return None if isinstance(r, dict) and _int(r.get('ano')) and isinstance(r.get('texto'), str) and r['texto'] else 'a crônica junta {ano, texto, onde, tags}'
        return None if isinstance(r, dict) and _int(r.get('dia')) and isinstance(r.get('texto'), str) and r['texto'] else 'a janela junta {dia, texto}'
    if not isinstance(r, dict): return f'o registro de "{sec}" é um dicionário'
    if sec in ('casas', 'reinos', 'guildas') and not (isinstance(r.get('nome'), str) and r['nome']): return f'o registro de "{sec}" pede um nome'
    if sec == 'casas' and r.get('tipo', 'comum') not in ('nobre', 'comum'): return 'a casa é nobre ou comum'
    if sec == 'guildas' and r.get('sede') not in Ls: return 'a guilda tem sede num lugar que existe'
    if sec == 'frentes':
        if r.get('tipo') not in M.FRENTE_TIPOS: return f'a frente é de um tipo: {", ".join(M.FRENTE_TIPOS)}'
        if not (_int(r.get('passo')) and 0 <= r['passo'] <= M.FRENTE_PASSOS): return f'o passo da frente vai de 0 a {M.FRENTE_PASSOS}'
        if not (isinstance(r.get('nome'), str) and r['nome']): return 'a frente pede um nome'
        if r.get('fim') not in (None,) + M.FRENTE_FINS: return 'o fim da frente é desfecho ou barrada, ou nada'
        if r.get('onde') is not None and r['onde'] not in Ls: return 'a frente acontece num lugar que existe'
        ps = r.get('passos')
        if not (isinstance(ps, list) and len(ps) == M.FRENTE_PASSOS and all(isinstance(x, str) for x in ps)): return f'a frente traz os {M.FRENTE_PASSOS} passos (textos)'
        return None
    if sec == 'missoes':
        if r.get('tipo') not in M.MISSAO_TIPOS: return f'a missão é de um tipo: {", ".join(M.MISSAO_TIPOS)}'
        if r.get('estado') not in M.MISSAO_ESTADOS: return f'o estado da missão é um de: {", ".join(M.MISSAO_ESTADOS)}'
        if r.get('onde') not in Ls: return 'a missão está num quadro de um lugar que existe'
        if not (_int(r.get('paga')) and r['paga'] >= 0 and _int(r.get('prazo'))): return 'a missão tem paga (prata, inteira) e prazo (o dia)'
        return None
    if sec == 'caixa':
        op = r.get('opcoes')
        if not (isinstance(r.get('pede'), str) and r['pede'] and _int(r.get('prazo'))): return 'o pedido da caixa tem o que pede e o prazo (o dia)'
        if not (isinstance(op, dict) and len(op) >= 2 and all(isinstance(k, str) and len(k) == 1 and k.isalpha() and isinstance(t, str) for k, t in op.items())): return 'o pedido tem pelo menos duas opções, cada uma com uma letra'
        if r.get('padrao') not in op: return 'o padrão do pedido é uma das opções dele'
        ef = r.get('efeitos') or {}
        if not (isinstance(ef, dict) and all(k in op and isinstance(v, list) for k, v in ef.items())): return 'os efeitos do pedido são {letra: [efeitos]}'
        if r.get('fim') is not None and r['fim'] not in op: return 'o pedido resolvido diz a letra que valeu'
        return None
    if sec == 'noticias':
        if not (_int(r.get('dia')) and r.get('onde') in Ls and isinstance(r.get('texto'), str) and r['texto']): return 'a notícia é {dia, onde (um lugar que existe), texto, peso, chegou}'
        ch = r.get('chegou') or {}
        if not (isinstance(ch, dict) and all(k in Ls and isinstance(x, list) and len(x) == 2 and all(_int(y) for y in x) for k, x in ch.items())): return 'a notícia diz onde chegou: {lugar: [dia, saltos]}'
        return None
    return None


def _mundo(E, ef):
    """o verbo do mundo.json (a forma: projeto/ETAPA_FINAL.md, seção 1)"""
    W = E.setdefault('mundo', {})
    if len(ef) < 4 or ef[1] not in M.SECOES_MUNDO: return _erro(ef, f'a seção do mundo é uma de: {", ".join(M.SECOES_MUNDO)}')
    sec = ef[1]
    if sec in M.SECOES_LISTA:
        if len(ef) != 4 or ef[2] != 'junta': return _erro(ef, f"use ['mundo', '{sec}', 'junta', registro]")
        e = _mundo_forma(E, sec, None, ef[3])
        if e: return _erro(ef, e)
        W[sec] = list(W.get(sec) or []) + [copy.deepcopy(ef[3])]; return
    if sec in M.SECOES_UNICAS:
        if len(ef) != 5 or not isinstance(ef[2], str) or not ef[2] or ef[3] not in ('poe', 'soma'): return _erro(ef, f"use ['mundo', '{sec}', 'CAMPO', 'poe'|'soma', valor]")
        d = W.setdefault(sec, {}); raiz, _, sub = ef[2].partition('.')
        if sub and not isinstance(d.get(raiz, {}), dict): return _erro(ef, f'"{raiz}" não tem partes')
        alvo = d.setdefault(raiz, {}) if sub else d; k = sub or raiz
        if ef[3] == 'soma':
            if not _num(ef[4]) or not _num(alvo.get(k, 0)): return _erro(ef, f'"{ef[2]}" não é número: não se soma')
            alvo[k] = alvo.get(k, 0) + ef[4]
        elif ef[4] is None: alvo.pop(k, None)
        else: alvo[k] = copy.deepcopy(ef[4])
        return
    D = W.setdefault(sec, {})
    if len(ef) == 5:
        _, _, rid, op, reg = ef
        if op != 'poe' or not isinstance(rid, str) or not rid: return _erro(ef, f"use ['mundo', '{sec}', ID, 'poe', registro ou None]")
        if reg is None: D.pop(rid, None); return
        e = _mundo_forma(E, sec, rid, reg)
        if e: return _erro(ef, e)
        D[rid] = copy.deepcopy(reg); return
    if len(ef) == 6:
        _, _, rid, campo, op, val = ef
        r = D.get(rid) if isinstance(rid, str) else None
        if not isinstance(r, dict): return _erro(ef, f'não há "{rid}" em mundo.{sec}')
        if not isinstance(campo, str) or not campo or op not in ('poe', 'soma', 'junta'): return _erro(ef, f"use ['mundo', '{sec}', ID, 'CAMPO', 'poe'|'soma'|'junta', valor]")
        novo = copy.deepcopy(r); raiz, _, sub = campo.partition('.')
        if sub and not isinstance(novo.get(raiz, {}), dict): return _erro(ef, f'"{raiz}" não tem partes')
        alvo = novo.setdefault(raiz, {}) if sub else novo; k = sub or raiz
        if op == 'soma':
            if not _num(val) or not _num(alvo.get(k, 0)): return _erro(ef, f'"{campo}" não é número: não se soma')
            alvo[k] = alvo.get(k, 0) + val
        elif op == 'junta':
            if not isinstance(alvo.get(k, []), list): return _erro(ef, f'"{campo}" não é lista: não se junta')
            alvo[k] = list(alvo.get(k) or []) + [copy.deepcopy(val)]
        elif val is None: alvo.pop(k, None)
        else: alvo[k] = copy.deepcopy(val)
        e = _mundo_forma(E, sec, rid, novo)
        if e: return _erro(ef, e)
        D[rid] = novo; return
    return _erro(ef, f"use ['mundo', '{sec}', ID, 'poe', registro] ou ['mundo', '{sec}', ID, 'CAMPO', 'poe'|'soma'|'junta', valor]")


# ---------- a etapa da magia no gravador (as formas: projeto/ETAPA_MAGIA.md, seções 1 a 7) ----------
PESSOA_MAGIA = ('talento', 'dom', 'inclinacao', 'mana', 'feitico', 'tradicao', 'voto', 'laco', 'divida', 'funda')
NASCE_MAGIA = ('talento', 'dom', 'inclinacao', 'feiticos', 'tradicao', 'voto', 'laco', 'divida', 'mana')     # o que a pessoa pode trazer ao nascer (a Mana por último: o máximo depende do resto)


def _magia_erro(E, p, campo, v):
    """o que um campo da magia aceita (None: aceita). Serve ao gravador, ao nascer e aos invariantes."""
    if campo == 'talento':
        if v is None: return None
        return None if isinstance(v, dict) and all(k in TT.CAMINHOS and _int(g) and g in TT.TALENTO for k, g in v.items()) else f'o talento é {{caminho: grau de −2 a 2}} (os caminhos: {", ".join(TT.CAMINHOS)})'
    if campo == 'dom': return None if isinstance(v, dict) and len(v) <= 1 and all(k in TT.CAMINHOS and _int(g) and g in TT.DOM for k, g in v.items()) else 'o dom é {caminho: 1 ou 2}, num caminho só ({}: sem dom)'
    if campo == 'inclinacao':
        if v is not None and v not in TT.CAMINHOS: return f'a inclinação é um caminho ({", ".join(TT.CAMINHOS)})'
        return None if v is None or p.get('jogador') or p.get('estado') == 'morto' else 'só o personagem do jogador tem inclinação'      # o personagem que morreu (e passou a vez ao herdeiro) guarda a dele
    if campo == 'mana': return None if _num(v) and 0 <= v <= mana_max(p) else f'a Mana vai de 0 a {mana_max(p)}'
    if campo == 'feiticos': return None if isinstance(v, list) and all(x in T.FEITICOS for x in v) and len(set(v)) == len(v) else 'os feitiços sabidos são uma lista de nomes da tabela (tabelas.FEITICOS), sem repetir'
    if campo == 'tradicao': return None if v is None or v in T.TRADICOES else f'a tradição é uma de: {", ".join(T.TRADICOES)}'
    if campo == 'voto':
        return None if v is None or (isinstance(v, dict) and v.get('qual') in M.VOTOS and v.get('santuario') in E['lugares'] and _int(v.get('dia', 0))) else f'o voto é {{qual: {" | ".join(M.VOTOS)}, santuario: um lugar que existe, dia}}'
    if campo == 'laco': return None if v is None or (isinstance(v, dict) and v.get('ermo') in E['lugares'] and _int(v.get('dia', 0))) else 'o laço é {ermo: um lugar que existe, dia}'
    if campo == 'divida': return None if _num(v) and v >= 0 else 'a dívida é um número de zero para cima'
    if campo == 'funda': return None if v is None or (_int(v) and 0 <= v < len(T.CATS)) else 'a ferida funda é uma categoria (0 a 7), ou nada'
    return None


def _pessoa_magia(E, pid, p, campo, op, val, ef):
    """os verbos da magia na pessoa (seção 7 do contrato)"""
    if campo == 'feitico':
        if op not in ('aprende', 'esquece') or val not in T.FEITICOS: return _erro(ef, f'use ["pessoa", id, "feitico", "aprende"|"esquece", NOME] (os feitiços: {", ".join(T.FEITICOS)})')
        L = p.setdefault('feiticos', [])
        if op == 'aprende' and val not in L: L.append(val)
        if op == 'esquece' and val in L: L.remove(val)
        return
    if campo == 'voto' and op == 'quebra':
        v = p.get('voto')
        if not isinstance(v, dict): return _erro(ef, f'{p["nome"]} não tem voto para quebrar')
        if v.get('quebrado') is None: v['quebrado'] = E['relogio']['dia']; v['como'] = str(val)
        return
    if campo in ('mana', 'divida') and op == 'soma':
        if not _num(val): return _erro(ef, f'"{campo}" soma um número')
        if campo == 'mana': p['mana'] = max(0, min(mana_max(p), mana(p) + val)); return
        q = (p.get('divida') or 0) + val
        if q < 0: return _erro(ef, f'{p["nome"]} só deve {p.get("divida") or 0}')
        p['divida'] = q; return
    if op != 'poe': return _erro(ef, f'"{campo}" só aceita "poe"' + (' (e "soma")' if campo in ('mana', 'divida') else ' (e "quebra")' if campo == 'voto' else ''))
    if campo in ('talento', 'divida') and val is None: return _erro(ef, f'"{campo}" não se põe em nada')
    e = _magia_erro(E, p, campo, val)
    if e: return _erro(ef, e)
    if campo == 'talento': p['talento'] = {k: g for k, g in val.items() if g}
    elif val is None and campo in ('funda',): p.pop(campo, None)
    else: p[campo] = copy.deepcopy(val)


# ---------- a etapa 4b na pessoa e no item (as formas: projeto/ETAPA_4B.md, seções 1, 3 e 6) ----------
PESSOA_4B = ('povo', 'idade', 'inclinacao2')     # o povo primeiro: a idade e a segunda inclinação dependem dele
POVO_EVENTOS = ('gera', 'mestre')               # só nestes eventos se grava o povo e a idade (a segunda inclinação: os do talento)


def _pessoa4b_erro(E, p, campo, v):
    """o que o povo, a idade e a segunda inclinação aceitam (None: aceita). Serve ao gravador, ao nascer e aos invariantes."""
    if campo == 'povo':
        TP = _tp()
        return None if TP is not None and v in TP.POVOS else 'o povo é um da tabela (' + (', '.join(TP.POVOS) if TP else 'não há a página dos povos') + ')'
    if campo == 'idade':
        if not _int(v) or v < 0: return 'a idade é um número inteiro de anos, de zero para cima'
        vida = _povo_reg(p).get('vida'); mx = vida[2] if isinstance(vida, (list, tuple)) and len(vida) > 2 else None
        return None if mx is None or v <= mx else f'{p.get("nome", "?")} não vive {v} anos: o povo {povo(p)} vive até {mx}'
    if campo == 'inclinacao2':
        if v not in TT.CAMINHOS: return f'a segunda inclinação é um caminho ({", ".join(TT.CAMINHOS)})'
        if not p.get('jogador') and p.get('estado') != 'morto': return 'só o personagem do jogador tem inclinação'
        if povo(p) != 'humano': return 'a segunda inclinação é só do personagem humano (E2 b)'
        if v == p.get('inclinacao'): return 'a segunda inclinação é outro caminho, não o da primeira'
    return None


def _descida_erro(E, d, pid=None):
    """a forma da descida aberta (marca.masmorra; a frente M guarda o resto dos campos): o texto do erro, ou None"""
    if not isinstance(d, dict): return 'é um registro {masmorra, sala, com, ordem, lances, luz, fase, luta...} (em quem vai junto: {de: quem comanda})'
    if d.get('de') is not None: return None if d['de'] in E['gente'] and d['de'] != pid else f'diz que foi junto com quem não há: "{d["de"]}"'
    m = E['lugares'].get(d.get('masmorra')) if isinstance(d.get('masmorra'), str) else None
    if not isinstance(m, dict) or m.get('tipo') != 'masmorra': return f'não diz uma masmorra que existe ("{d.get("masmorra")}")'
    s = E['lugares'].get(d.get('sala')) if isinstance(d.get('sala'), str) else None
    if not isinstance(s, dict) or s.get('tipo') != 'sala' or s.get('masmorra') != d['masmorra']: return f'não diz uma sala daquela masmorra ("{d.get("sala")}")'
    if not isinstance(d.get('com', []), list) or any(c not in E['gente'] for c in d.get('com', [])): return 'tem em "com" quem não existe'
    if not (_int(d.get('lances', 0)) and d.get('lances', 0) >= 0): return 'tem os lances fora da conta (um inteiro de zero para cima)'
    if not isinstance(d.get('fase', ''), str): return 'tem a fase torta (é texto)'
    if d.get('fase') == 'luta' and not isinstance(d.get('luta'), str): return 'está em luta sem o arquivo dela'
    return None


def _item4b_erro(it):
    """o que a gazua, a chave e o talhe da armadura pedem (None: certo)"""
    if it.get('talhe') is not None and (it.get('tipo') != 'armadura' or it['talhe'] != 'miúdo'): return 'o talhe só existe em armadura, e é "miúdo" (sem o campo: de gente)'
    if it.get('tipo') == 'chave' and (not isinstance(it.get('abre'), str) or not it['abre']): return 'a chave diz o que abre: a porta ("SALA_A|SALA_B") ou o guardado de uma sala ("SALA")'
    return None


def _abre_ok(E, a):
    """a chave abre uma porta que existe (das portas da masmorra das duas salas) ou o guardado de uma sala que existe?"""
    if not isinstance(a, str) or not a: return False
    if '|' in a:
        s = E['lugares'].get(a.split('|', 1)[0])
        return isinstance(s, dict) and s.get('tipo') == 'sala' and a in ((E['lugares'].get(s.get('masmorra')) or {}).get('portas') or {})
    s = E['lugares'].get(a)
    return isinstance(s, dict) and isinstance(s.get('guardado'), dict)


def _so_acrescenta(p, novo):
    """o talento novo só ACRESCENTA os caminhos que faltam à pessoa (talento.falta), sem mexer nos outros? (o caminho novo de quem já nasceu entra em gera ou talento)"""
    import talento
    falta = talento.falta(p)
    if not falta or not isinstance(novo, dict) or any(k not in TT.CAMINHOS for k in novo): return False
    velho = p.get('talento') or {}
    return all(novo.get(c, 0) == velho.get(c, 0) for c in TT.CAMINHOS if c not in falta)


def _molde_erro(m):
    """o MOLDE de uma maldição (o que mora numa peça maldita ou num lugar maldito): {nome, cat, tipo, condicao}. None: certo."""
    if not isinstance(m, dict): return 'o molde da maldição é {nome, cat, tipo, condicao}'
    if not isinstance(m.get('nome'), str) or not m['nome']: return 'a maldição pede um nome'
    if not _int(m.get('cat')) or not 0 <= m['cat'] < len(T.CATS): return 'a categoria da maldição vai de 0 a 7'
    if m.get('tipo') not in M.MALDICAO_TIPOS: return f'o tipo da maldição é um de: {", ".join(M.MALDICAO_TIPOS)}'
    c = m.get('condicao')
    if not isinstance(c, dict) or c.get('tipo') not in M.MALDICAO_CONDICOES: return f'a condição é {{tipo: {" | ".join(M.MALDICAO_CONDICOES)}, ...}}'
    return None


def _maldicao_erro(E, r):
    """o REGISTRO de uma maldição que anda numa pessoa (seção 6 do contrato). None: certo."""
    e = _molde_erro(r)
    if e: return e
    if not isinstance(r.get('id'), str) or not r['id']: return 'a maldição pede um id'
    if not _int(r.get('passo')) or not 1 <= r['passo'] <= len(M.MALDICAO_PASSOS): return f'o passo vai de 1 a {len(M.MALDICAO_PASSOS)}'
    if r.get('de') not in M.MALDICAO_ORIGENS: return f'a origem é uma de: {", ".join(M.MALDICAO_ORIGENS)}'
    if r.get('quem') is not None and r['quem'] not in E['gente']: return f'não há a pessoa "{r["quem"]}" (quem rogou)'
    if not _int(r.get('sabe', 0)) or not 0 <= r.get('sabe', 0) <= M.MALDICAO_SABE: return f'o saber vai de 0 a {M.MALDICAO_SABE}'
    if r.get('suspensa') is not None and not _int(r['suspensa']): return '"suspensa" é um dia, ou nada'
    if r.get('desde') is not None and not _int(r['desde']): return '"desde" é um dia'
    return None


def _maldicao(E, ef):
    """o verbo maldicao: ['maldicao', pessoa, 'poe', registro] ou ['maldicao', pessoa, MID, campo, valor]"""
    p = E['gente'].get(ef[1]) if len(ef) > 2 and isinstance(ef[1], str) else None
    if not p: return _erro(ef, 'não há essa pessoa')
    if len(ef) == 4 and ef[2] == 'poe':
        if p['estado'] != 'vivo': return _erro(ef, f'{p["nome"]} morreu: não pega maldição')
        r = copy.deepcopy(ef[3])
        if not isinstance(r, dict) or 'id' in r: return _erro(ef, 'o registro da maldição vem sem "id" (o gravador dá)')
        E['itens']['mseq'] = E['itens'].get('mseq', 0) + 1; r['id'] = f"m{E['itens']['mseq']:04d}"
        for k, v in (('passo', 1), ('desde', E['relogio']['dia']), ('sabe', 0), ('suspensa', None), ('quem', None), ('fonte', None)): r.setdefault(k, v)
        e = _maldicao_erro(E, r)
        if e: return _erro(ef, e)
        p.setdefault('maldicoes', []).append(r); return
    if len(ef) != 5: return _erro(ef, "use ['maldicao', id, 'poe', registro] ou ['maldicao', id, MID, 'passo'|'quebra'|'sabe'|'suspensa'|'condicao', valor]")
    _, _, mid, campo, val = ef; L = p.get('maldicoes') or []
    i = next((k for k, m in enumerate(L) if isinstance(m, dict) and m.get('id') == mid), None)
    if i is None: return _erro(ef, f'{p["nome"]} não tem a maldição "{mid}"')
    m = L[i]
    if campo == 'passo':
        if not _int(val) or not val: return _erro(ef, 'o relógio anda um número inteiro de passos (+1; a poção: −2)')
        m['passo'] = max(1, min(len(M.MALDICAO_PASSOS), m['passo'] + val)); return
    if campo == 'quebra': L.pop(i); return
    if campo == 'sabe':
        if not _int(val) or not 0 <= val <= M.MALDICAO_SABE: return _erro(ef, f'o saber é de 0 a {M.MALDICAO_SABE}')
        if val < m.get('sabe', 0): return _erro(ef, 'o saber só sobe')
        m['sabe'] = val; return
    if campo == 'suspensa':
        if val is not None and not _int(val): return _erro(ef, '"suspensa" é um dia, ou nada')
        m['suspensa'] = val; return
    if campo == 'condicao':
        if not isinstance(val, dict) or val.get('tipo') not in M.MALDICAO_CONDICOES: return _erro(ef, f'a condição é {{tipo: {" | ".join(M.MALDICAO_CONDICOES)}, ...}}')
        m['condicao'] = copy.deepcopy(val); return
    return _erro(ef, 'na maldição muda-se: passo, quebra, sabe, suspensa, condicao')


def _encanto_erro(x): return not (isinstance(x, dict) and x.get('feitico') in T.FEITICOS and _int(x.get('grau')) and 0 <= x['grau'] <= 4 and (x.get('gasto') is None or _int(x['gasto'])))


def _item_magia_erro(it):
    """o que os tipos e os campos novos de item pedem (None: certo)"""
    t = it.get('tipo')
    if t == 'foco' and it.get('forma') not in T.FOCOS: return f'o foco pede a forma ({", ".join(T.FOCOS)})'
    if t == 'elixir' and (it.get('pocao') not in M.POCOES or not _int(it.get('cat')) or it['cat'] <= M.POCAO_ATE): return 'o elixir é uma poção da tabela, do Épico para cima (abaixo disso a poção é bem, na carga)'
    if t == 'escrito' and (not isinstance(it.get('feiticos'), list) or not it['feiticos'] or any(x not in T.FEITICOS for x in it['feiticos'])): return 'o escrito ensina feitiços da tabela (uma lista com pelo menos um)'
    enc = it.get('encantos')
    if enc is not None:
        if t not in COM_ENCANTO: return 'só arma, armadura e escudo levam encanto (o foco e o amuleto já são magia)'
        mx = M.encantos_max(it['cat']) if _int(it.get('cat')) else 1
        if not isinstance(enc, list) or len(enc) > mx or any(_encanto_erro(x) for x in enc): return f'os encantos de uma peça são uma lista de até {mx}, cada um {{feitico, grau de 0 a 4, feito_por, dia, gasto}}'
    if it.get('maldita') is not None:
        e = _molde_erro(it['maldita'])
        if e: return 'a peça maldita leva um molde de maldição: ' + e
    if t == 'ferramenta':                                    # (a etapa dos efeitos, parte 1) a ferramenta do ofício
        import tabelas_oficio as TO
        if it.get('oficio') not in TO.FERRAMENTA_OFICIOS: return f'a ferramenta é de um ofício ({", ".join(TO.FERRAMENTA_OFICIOS)})'
        if it.get('forma') is not None and it['forma'] not in TO.FERRAMENTA_FORMAS: return f'a forma da ferramenta é uma de: {", ".join(TO.FERRAMENTA_FORMAS)}'
    el = it.get('efeitos_livres')
    if el is not None and (not _int(el) or el < 0): return 'os efeitos por escolher são um número inteiro, de zero para cima'
    e = _campos_faixa_erro(it)                               # (a parte 2, fase 1a) o teto de efeitos, os cheios, o sinete, o degrau, e cada efeito na porta dele
    if e: return e
    if it.get('benta') is not None and (t != 'arma' or not _int(it['benta'])): return 'só a arma fica benta (até um bloco)'
    v = it.get('veneno')
    if v is not None and (t != 'arma' or not isinstance(v, dict) or not _int(v.get('cat')) or not 0 <= v['cat'] <= M.POCAO_ATE or not _int(v.get('ate'))): return f'o veneno na lâmina é {{cat: de 0 a {M.POCAO_ATE}, ate: um bloco}}, só em arma'
    return None


def _molde_obra_ok(k):
    import itens as IT
    return isinstance(k, str) and k in IT.EFEITOS and k not in IT.ESCOLHE_NAO


def _teto_ef(it):
    """(a parte 2, fase 1a) o teto de efeitos da peça: o gravado ao nascer; a peça antiga sem o campo, o da categoria (tabelas_oficio.EFEITOS_MAX)"""
    import tabelas_oficio as TO
    t = it.get('teto_efeitos'); return t if _int(t) else TO.efeitos_max(it['cat'] if _int(it.get('cat')) else 0)


def _efeito_erro(it, val, novo=False):
    """(a parte 2, fase 1a) o que um efeito pede para estar nesta peça (None: certo). O de FERRAMENTA: a porta pela força (com o degrau emprestado, uma acima: só com o direito
    que a peça trouxe ao nascer, um só, e em peça de até 4 efeitos); o cheio só em efeito de número. Os de luta de hoje seguem a regra de hoje (o devolve de 1 ao teto da
    categoria; nenhum leva cheio nem emprestado) até o evento de entrada da fase 1b. `novo`: o efeito está entrando (conta ele no teto de efeitos)."""
    import tabelas_oficio as TO
    k = val.get('chave'); cat = it['cat'] if _int(it.get('cat')) else 0
    if k in TO.FERRAMENTA_EFEITOS:
        sobra = set(val) - {'chave', 'cheio', 'emprestado'}
        if sobra: return f'o efeito de ferramenta "{k}" é {{chave, cheio?, emprestado?}} (veio também: {", ".join(sorted(sobra))}): o número nunca se guarda, sai da categoria'
        forca = TO.FERRAMENTA_EFEITOS[k][0]; emp = bool(val.get('emprestado'))
        if not TO.cabe_forca(forca, cat, emp): return f'"{k}" é {forca}: a porta da peça {T.CATS[cat]} não abre essa força' + (' (nem com o degrau emprestado)' if emp else ' (fraco na Comum, normal na Incomum, forte na Épica, apelão na Lendária)')
        if emp:
            if not it.get('degrau'): return f'"{k}" emprestado pede o degrau emprestado, que a peça traz ao nascer (a ferramenta que o dá em uso na forja)'
            if TO.cabe_forca(forca, cat): return f'"{k}" já cabe na porta da peça: não é do degrau emprestado'
            outros = [e for e in it.get('efeitos') or [] if isinstance(e, dict) and e.get('emprestado') and e is not val]
            if outros: return 'a peça já tem um efeito do degrau emprestado: a porta adiantada é uma só'
            livres = it.get('efeitos_livres') or 0
            if len(it.get('efeitos') or []) + (max(livres, 1) if novo else livres) > TO.DEGRAU_ATE: return f'o degrau emprestado só entra em peça de até {TO.DEGRAU_ATE} efeitos'      # (o que entra está entre os por escolher; o gravado, entre os efeitos)
        if val.get('cheio') is not None and val['cheio'] is not True: return 'o cheio é True, ou não vem'
        if val.get('cheio') and not TO.de_numero(k): return f'"{k}" não tem número: o cheio só vale em efeito de número (o prumo, a têmpera)'
    else:
        if val.get('cheio') or val.get('emprestado'): return f'o efeito "{k}" é de luta: o cheio e o degrau emprestado chegam com o catálogo de luta (a fase 1b)'
        if k == 'devolve' and not (_int(val.get('valor')) and 1 <= val['valor'] <= T.devolve_max(cat)): return f'"devolve" numa peça {T.CATS[cat]} vai de 1 a {T.devolve_max(cat)}'
        if k != 'devolve' and 'valor' in val: return f'o efeito "{k}" não leva valor'
    if novo and len(it.get('efeitos') or []) + 1 > _teto_ef(it): return f'a peça já tem os efeitos que o teto dela deixa ({_teto_ef(it)})'
    return None


def _campos_faixa_erro(it):
    """(a parte 2, fase 1a) os campos novos do item: teto_efeitos (de o da categoria a ele mais 2: a obra-prima no teto e o molde), cheios_livres (até os por escolher), sinete,
    degrau; os efeitos (escolhidos e por escolher) até o teto; cada efeito de ferramenta na porta dele. O save de antes (sem os campos) passa como está."""
    import tabelas_oficio as TO
    cat = it['cat'] if _int(it.get('cat')) else 0; te = it.get('teto_efeitos')
    if te is not None and not (_int(te) and TO.efeitos_max(cat) <= te <= TO.efeitos_max(cat) + 2): return f'o teto de efeitos de uma peça {T.CATS[cat]} vai de {TO.efeitos_max(cat)} a {TO.efeitos_max(cat) + 2} (a obra-prima no teto e o molde)'
    ch = it.get('cheios_livres')
    if ch is not None and (not _int(ch) or ch < 0 or ch > (it.get('efeitos_livres') or 0)): return 'os cheios por escolher são um número inteiro, de zero até os efeitos por escolher'
    if it.get('sinete') is not None and not (isinstance(it['sinete'], str) and it['sinete']): return 'o sinete é o id de quem forjou a peça'
    if it.get('degrau') is not None and it['degrau'] is not True: return 'o degrau emprestado da peça é True, ou não vem'
    efs = it.get('efeitos')
    if efs is None: return None
    if not isinstance(efs, list) or not all(isinstance(e, dict) for e in efs): return 'os efeitos da peça são uma lista de {chave, ...}'
    if len(efs) + (it.get('efeitos_livres') or 0) > _teto_ef(it): return f'a peça tem mais efeitos (escolhidos e por escolher: {len(efs) + (it.get("efeitos_livres") or 0)}) do que o teto dela ({_teto_ef(it)})'
    if sum(1 for e in efs if e.get('emprestado')) > 1: return 'a peça tem mais de um efeito do degrau emprestado'
    for e in efs:
        if e.get('chave') in TO.FERRAMENTA_EFEITOS:
            if it.get('tipo') != 'ferramenta': return f'o efeito "{e["chave"]}" é de ferramenta'
            x = _efeito_erro(it, e)
            if x: return x
    return None


def _presa(E, it):
    """o dono desta peça tem uma maldição andando que veio dela? (a peça maldita não sai de uso nem muda de dono enquanto a maldição dura)"""
    d = E['gente'].get(it.get('dono')) if it.get('dono') else None
    return isinstance(d, dict) and any(isinstance(m, dict) and m.get('de') == 'peça' and m.get('fonte') == it.get('id') for m in d.get('maldicoes') or [])


def _encanto(E, it, op, val, ef):
    """['item', id, 'encanto', 'grava', registro] · ['item', id, 'encanto', 'gasta'|'apaga', indice]"""
    if it['tipo'] not in COM_ENCANTO: return _erro(ef, f'{it["nome"]} não leva encanto (só arma, armadura e escudo: o foco e o amuleto já são magia)')
    L = it.get('encantos') or []
    if op == 'grava':
        x = copy.deepcopy(val)
        if not isinstance(x, dict): return _erro(ef, 'o encanto é {feitico, grau, feito_por, dia}')
        x.setdefault('feito_por', None); x.setdefault('dia', E['relogio']['dia']); x['gasto'] = None
        if _encanto_erro(x): return _erro(ef, 'o encanto é {feitico: um da tabela, grau: de 0 a 4, feito_por, dia}')
        if len(L) >= M.encantos_max(it['cat']): return _erro(ef, f'{it["nome"]} já tem os encantos que cabem numa peça {T.CATS[it["cat"]]} ({M.encantos_max(it["cat"])})')
        it['encantos'] = L + [x]; return
    if op in ('gasta', 'apaga'):
        if not _int(val) or not 0 <= val < len(L): return _erro(ef, f'{it["nome"]} não tem esse encanto')
        if op == 'gasta': L[val]['gasto'] = agora(E)
        else:
            L.pop(val)
            if not L: it.pop('encantos', None)
        return
    return _erro(ef, "use ['item', id, 'encanto', 'grava', registro] ou ['item', id, 'encanto', 'gasta'|'apaga', indice]")


# O ENSAIO COPIA SÓ O QUE O EVENTO MEXE (etapa final: o mundo grande). Cada efeito diz o que pode tocar; o registro que nenhum efeito toca segue sendo o mesmo objeto,
# só lido (ninguém o muda em lugar: quem muda, muda a cópia). O efeito que pode mexer em mais coisas (a morte, a maldição, o encanto...) copia tudo, como antes.
_ITEM_LEVE = ('dono', 'uso', 'onde', 'solto', 'dur', 'historia', 'nome', 'sob_medida', 'talhe', 'maldita', 'benta', 'veneno', 'efeito', 'efeitos_livres', 'cheios_livres')


def _toca(ef):
    """o que um efeito pode mexer: [(arquivo, chave)] (chave None: o arquivo inteiro; '+': só a lista do arquivo, para nascer ou sumir alguém), ou None (copia tudo)"""
    if not isinstance(ef, (list, tuple)) or not ef: return None
    v = ef[0]; n = len(ef)
    if v == 'relogio': return [('relogio', None)]
    if v == 'estoque' and n == 5 and isinstance(ef[1], str): return [('lugares', ef[1])]
    if v == 'lugar' and n >= 3: return [('lugares', '+')] if ef[1] == 'nasce' else [('lugares', ef[1])] if isinstance(ef[1], str) else None
    if v == 'pessoa' and n >= 3:
        if ef[1] == 'nasce': return [('gente', '+')]
        if n == 5 and isinstance(ef[1], str) and isinstance(ef[2], str) and ef[2] != 'estado': return [('gente', ef[1])]
        return None
    if v == 'ferida' and n >= 3 and isinstance(ef[1], str): return [('gente', ef[1])]
    if v == 'item' and n >= 3:
        if ef[1] == 'nasce' or (n == 3 and ef[2] == 'some'): return [('itens', '+')]
        if n == 5 and isinstance(ef[1], str) and ef[2] in _ITEM_LEVE: return [('itens', ef[1])]
        return None
    if v == 'obra': return [('itens', 'obras')]
    if v == 'mundo' and n >= 4 and isinstance(ef[1], str):
        return [('mundo', (ef[1], ef[2] if n in (5, 6) and ef[1] not in M.SECOES_UNICAS and ef[1] not in M.SECOES_LISTA and isinstance(ef[2], str) else None))]
    return None


def _ensaio(E, efeitos):
    """a cópia de ensaio do estado: só o que os efeitos podem mexer é copiado a fundo; o resto é o mesmo objeto (só se lê)"""
    alvo = {}
    for ef in efeitos:
        t = _toca(ef)
        if t is None: return {k: copy.deepcopy(E[k]) for k in ARQS}
        for arq, chave in t: alvo.setdefault(arq, set()).add(chave)
    ens = {k: E[k] for k in ARQS}
    for arq, chaves in alvo.items():
        if None in chaves and arq != 'mundo': ens[arq] = copy.deepcopy(E[arq]); continue
        if arq == 'itens':
            d = dict(E['itens'])
            if 'obras' in chaves: d['obras'] = copy.deepcopy(E['itens'].get('obras', {}))
            resto = chaves - {'obras'}
            if resto:
                d['itens'] = dict(E['itens']['itens'])
                for k in resto - {'+'}:
                    if k in d['itens']: d['itens'][k] = copy.deepcopy(d['itens'][k])
            ens['itens'] = d
        elif arq == 'mundo':
            d = dict(E['mundo'])
            for sec, rid in chaves:
                velho = E['mundo'].get(sec)
                if rid is None: d[sec] = copy.deepcopy(velho) if velho is not None and sec not in M.SECOES_LISTA else (list(velho) if velho is not None else velho)
                else:
                    if d.get(sec) is velho: d[sec] = dict(velho) if isinstance(velho, dict) else velho
                    if isinstance(d.get(sec), dict) and rid in d[sec]: d[sec][rid] = copy.deepcopy(d[sec][rid])
                if d.get(sec) is None: d.pop(sec, None)
            ens['mundo'] = d
        else:
            d = dict(E[arq])
            for k in chaves - {'+'}:
                if k in d: d[k] = copy.deepcopy(d[k])
            ens[arq] = d
    return ens


def aplica(E, tipo, efeitos, onde=None, quem=(), texto=''):
    """A ÚNICA PORTA. Ensaia todos os efeitos numa cópia; se um falha, NADA muda e o erro sai com o motivo.
    O evento cujos efeitos não mudam nada (somar no que já está no teto, pôr o que já está posto) não aconteceu: não entra no registro, e devolve None.
    COM UMA LUTA ABERTA no mundo, só entram a luta que volta ao estado, a mão do Mestre e a nota da saída de caça que está naquela luta (tabelas_mundo.NA_LUTA)."""
    if tipo not in M.EVENTOS: sys.exit(f'evento desconhecido: "{tipo}" (os que existem: {", ".join(M.EVENTOS)})')
    if not efeitos: sys.exit(f'evento "{tipo}" sem efeito: recusado. O que não muda número não aconteceu.')
    if tipo not in M.NA_LUTA and luta_aberta(E) and not _nota_da_luta(E, efeitos): sys.exit(luta_diz(E))
    E.setdefault('mundo', {})
    ensaio = _ensaio(E, efeitos)
    for ef in efeitos:
        if isinstance(ef, (list, tuple)) and len(ef) == 5 and ef[0] == 'pessoa' and ef[2] in REGIAO_EVENTOS and tipo not in REGIAO_EVENTOS[ef[2]]:
            sys.exit(f'evento "{tipo}" recusado, nada mudou. {_erro(ef, "este campo só se grava em evento " + " ou ".join(REGIAO_EVENTOS[ef[2]]))}')
        if isinstance(ef, (list, tuple)) and len(ef) >= 4 and ef[0] == 'mundo' and tipo not in M.NASCE and (ef[1] in M.SECOES_GERA or (ef[1] == 'meta' and str(ef[2]).split('.')[0] in ('ano0', 'anos', 'nome'))):
            sys.exit(f'evento "{tipo}" recusado, nada mudou. {_erro(ef, "a história (as casas, os reinos, a crônica, o ano) só se escreve em evento " + " ou ".join(M.NASCE))}')
        if isinstance(ef, (list, tuple)) and len(ef) == 5 and ef[0] == 'pessoa' and ef[2] in ('talento', 'dom'):
            if tipo not in TALENTO_EVENTOS: sys.exit(f'evento "{tipo}" recusado, nada mudou. {_erro(ef, "o talento e o dom só se gravam em evento " + ", ".join(TALENTO_EVENTOS))}')
            q = E['gente'].get(ef[1]) if isinstance(ef[1], str) else None
            if ef[2] == 'talento' and isinstance(q, dict) and q.get('talento') is not None and tipo != 'mestre' and not _so_acrescenta(q, ef[4]):
                sys.exit(f'evento "{tipo}" recusado, nada mudou. {_erro(ef, q["nome"] + " já tem o talento rolado: só o Mestre o troca (o caminho novo que falta entra pelo talento.rola_caminho)")}')
        if isinstance(ef, (list, tuple)) and len(ef) == 5 and ef[0] == 'pessoa' and ef[2] in PESSOA_4B and tipo not in (TALENTO_EVENTOS if ef[2] == 'inclinacao2' else POVO_EVENTOS):
            sys.exit(f'evento "{tipo}" recusado, nada mudou. {_erro(ef, "este campo só se grava em evento " + " ou ".join(TALENTO_EVENTOS if ef[2] == "inclinacao2" else POVO_EVENTOS))}')
        if tipo not in M.NASCE and isinstance(ef, (list, tuple)) and len(ef) > 1 and ef[0] in ('pessoa', 'lugar') and ef[1] == 'nasce':
            sys.exit(f'evento "{tipo}" recusado, nada mudou. {_erro(ef, "gente e lugar só nascem em evento " + " ou ".join(M.NASCE))}')
        try: e = _um(ensaio, ef)
        except (TypeError, KeyError, IndexError, AttributeError, ValueError) as x: e = _erro(ef, f'efeito malformado ({type(x).__name__})')
        if e: sys.exit(f'evento "{tipo}" recusado, nada mudou. {e}')
    if all(ensaio[k] == E[k] for k in ARQS): return None
    if sum(1 for p in ensaio['gente'].values() if isinstance(p, dict) and p.get('jogador')) > 1 and tipo == 'heranca': sys.exit(f'evento "{tipo}" recusado, nada mudou: ficariam dois personagens do jogador (tire o do morto no mesmo evento)')
    for pid, p in ensaio['gente'].items() if tipo != 'casa' else ():       # quem não é o personagem guarda O BLOCO EM QUE o corpo foi mexido pela última vez (o bloco deste evento: o relógio de antes de ele andar): o descanso em casa conta daí (em_cena).
        a = E['gente'].get(pid)                             # O próprio acerto do descanso (evento "casa") não é "estar em cena": ele não marca o bloco (as noites já contadas, o corpo.casa desconta à parte)
        if a is p: continue                                 # o registro que o evento não tocou é o mesmo objeto (o ensaio só copia o que muda)
        if isinstance(a, dict) and isinstance(p, dict) and not p.get('jogador') and p.get('estado') == 'vivo' and any(a.get(k) != p.get(k) for k in ('corpo', 'pv', 'feridas', 'mana')):      # a Mana gasta também é estar em cena: as noites de antes não voltam a encher
            if not isinstance(p.get('marca'), dict): p['marca'] = {}
            p['marca']['cena'] = agora(E)
    ev = dict(id=E['relogio']['eventos'] + 1, dia=E['relogio']['dia'], bloco=E['relogio']['bloco'], tipo=tipo, onde=onde, quem=list(quem), efeitos=[list(x) for x in efeitos], texto=texto)
    for k in ARQS: E[k] = ensaio[k]
    E['relogio']['eventos'] = ev['id']; E['_novos'].append(ev)
    return ev


# ---------- ler o estado (ninguém guarda cópia: tudo sai daqui) ----------
def pv_max(p): return T.pv_max(p['atributos']['Vigor'], p['nivel'])


def mana_max(p, visivel=False):
    """a Mana máxima da pessoa: (Afinidade + Vontade) ÷ 10, mais a melhor tradição dela (a maestria e o dom nela).
    `visivel`: só o dom que a pessoa já viu (a conta que vai à mesa); sem ele, o dom de verdade (a regra)."""
    import talento
    at = p['atributos']; ma = p.get('maestria') or {}; dm = talento.doms_vistos(p) if visivel else talento.doms(p)
    melhor = max([(ma.get(t, 0) if isinstance(ma, dict) else 0) + dm.get(t, 0) for t in T.TRADICOES] + [0])
    return T.mana_max(at['Afinidade'], at['Vontade'], melhor)


def mana(p, visivel=False):
    """a Mana de agora (a que não está escrita vale a cheia). `visivel`: como a pessoa a vê (nunca acima da máxima que ela conhece)"""
    v = p.get('mana'); mx = mana_max(p)
    m = mx if not _num(v) else max(0, min(mx, v))
    return min(m, mana_max(p, True)) if visivel else m


def firmeza(E, pid, visivel=False):
    """A FIRMEZA da pessoa fora da luta (contra a maldição e o lugar maldito; a base comum, tabelas.firmeza): a Vontade, a maior maestria, o dom de tradição, o amuleto que
    veste (sem amuleto, metade do bônus da armadura do tronco), com a poção de guarda valendo amuleto da categoria dela enquanto dura. A CONTA ÚNICA: o maldicao.firmeza
    é esta. `visivel`: só o dom que a pessoa já viu (a conta que vai à mesa). A luta soma o calejo por cima."""
    import talento
    p = E['gente'][pid]; eq = pecas(E, pid); ma = p.get('maestria') or {}
    maior = max([v for v in ma.values() if _num(v)] + [0]) if isinstance(ma, dict) else (ma if _num(ma) else 0)
    amu = eq['pescoco']['cat'] if eq['pescoco'] and eq['pescoco']['dur'][0] > 0 else None
    g = (p.get('marca') or {}).get('guarda')                # a poção de guarda bebida: amuleto da categoria dela até o bloco que marca
    if isinstance(g, dict) and _int(g.get('ate')) and g['ate'] > agora(E) and _int(g.get('cat')): amu = max(g['cat'], amu if amu is not None else -1)
    tronco = max((it['cat'] for it in eq['veste'] if 'tronco' in (it.get('cobre') or []) and it['dur'][0] > 0), default=None)
    dm = talento.doms_vistos(p) if visivel else talento.doms(p)
    return T.firmeza(p['atributos']['Vontade'], maior, amu, tronco, max([dm.get(t, 0) for t in T.TRADICOES] + [0]))


def hoje(E, p, chave):
    """o contador de hoje de uma marca {dia, n} (as poções bebidas: 'doses'; o PV devolvido por cura: 'curado'); de outro dia, zero"""
    m = (p.get('marca') or {}).get(chave)
    return m.get('n', 0) if isinstance(m, dict) and m.get('dia') == E['relogio']['dia'] and _num(m.get('n')) else 0


def encanto_carregado(E, enc):
    """o encanto está carregado? (solto, volta a carregar ENCANTO_VOLTA blocos depois, fora da luta)"""
    g = enc.get('gasto') if isinstance(enc, dict) else None
    return not _num(g) or agora(E) - g >= M.ENCANTO_VOLTA


def pecas(E, pid):
    """{'arma': item, 'arma2': item, 'escudo': item, 'veste': [itens]} do que a pessoa veste agora (sai do Livro de Itens)"""
    out = dict(arma=None, arma2=None, escudo=None, veste=[], foco=None, pescoco=None)
    for it in E['itens']['itens'].values():
        if it.get('dono') == pid and it.get('uso'):
            if it['uso'] == 'veste': out['veste'].append(it)
            else: out[it['uso']] = it
    return out


def lutador(E, pid, visivel=False, **mais):
    """a pessoa pronta para o pessoas.ficha e o luta.nova: quem é, o que veste hoje, o PV, as feridas e a pena do corpo (com a da maldição).
    Da etapa da magia: os feitiços, a Mana, a tradição, o dom, a pena da maldição, as maldições, a ferida funda, as poções de hoje, a carga de poções e os elixires;
    no equip, o foco e o amuleto. As cópias das peças vêm sem o que venceu (a bênção, o veneno da lâmina) e com cada encanto dizendo se está carregado.
    O que foi feito antes da luta e ainda vale: a bênção (marca.bencao: benzido), a poção de guarda (marca.guarda: guarda_p, amuleto da categoria dela), e o laço do druida
    com o ermo caçado até o fim (pena_laco, na Conjuração do verde).
    `visivel`: só o dom que a pessoa já viu (a ficha que vai à MESA; também a Mana máxima); sem ele, o dom de verdade (a luta), e `mana_vista` para a mesa da luta."""
    import corpo, talento
    p = E['gente'][pid]; eq = pecas(E, pid); t = agora(E)
    def copia(it):                                          # cópia: a luta não mexe no Livro
        if it is None: return None
        c = copy.deepcopy(it)
        if _num(c.get('benta')) and c['benta'] < t: c.pop('benta')
        if 'veneno' in c and not (isinstance(c['veneno'], dict) and _num(c['veneno'].get('ate')) and c['veneno']['ate'] >= t): c.pop('veneno')
        for enc in c.get('encantos') or []: enc['carregado'] = encanto_carregado(E, enc)
        return c
    d = dict(id=pid, nome=p['nome'], nivel=p['nivel'], atributos=dict(p['atributos']), maestria=dict(p.get('maestria', {})), pv=p['pv'],
             feridas=[[f['parte'], f['grave']] for f in p['feridas']], pena=corpo.pena(p, t), fol_menos=corpo.folego_menos(p),
             equip=dict(arma=copia(eq['arma']), arma2=copia(eq['arma2']), escudo=copia(eq['escudo']), armaduras=[copia(x) for x in eq['veste']], foco=copia(eq['foco']), amuleto=copia(eq['pescoco'])))
    d.update(feiticos=list(p.get('feiticos') or []), mana=mana(p, visivel), mana_max=mana_max(p, visivel), tradicao=p.get('tradicao'), dom=dict(talento.doms_vistos(p) if visivel else talento.doms(p)),
             pena_magia=corpo.pena_maldicao(p), maldicoes=copy.deepcopy(p.get('maldicoes') or []), funda=p.get('funda'), doses=hoje(E, p, 'doses'), curado=hoje(E, p, 'curado'),
             carga={b: q for b, q in (p.get('carga') or {}).items() if e_pocao(b) and _num(q) and q > 0},
             elixires=[dict(id=i, pocao=it.get('pocao'), cat=it['cat'], nome=it['nome']) for i, it in E['itens']['itens'].items() if it.get('dono') == pid and it.get('tipo') == 'elixir'])
    m = p.get('marca') or {}; bz = m.get('bencao'); gd = m.get('guarda')
    if isinstance(bz, dict) and _num(bz.get('ate')) and bz['ate'] >= t: d['benzido'] = True                      # a bênção dada antes da luta (vale do bloco em que foi dada ao seguinte)
    if isinstance(gd, dict) and _num(gd.get('ate')) and gd['ate'] > t and _int(gd.get('cat')): d['guarda_p'] = gd['cat']      # a poção de guarda: amuleto da categoria dela enquanto dura
    if not visivel and mana_max(p, True) != d['mana_max']: d['mana_vista'] = mana_max(p, True)                # o dom de tradição escondido: a luta usa a Mana de verdade, a mesa mostra a que a pessoa conhece
    pl = sum(m.pena_laco(E, pid) for m in modulos('pena_laco'))
    if pl: d['pena_laco'] = pl                                                              # o laço do druida com o ermo caçado até o fim tira da Conjuração dele
    rp = _povo_reg(p)                                       # O POVO (etapa 4b): os traços e a coragem dele vão à luta (o nome não: o "povo" do lutador é o corpo das criaturas)
    if rp.get('tracos'): d['tracos'] = list(rp['tracos'])
    if rp.get('coragem'): d['coragem'] = rp['coragem']
    d.update(mais)
    return d


def valida(E):
    """os invariantes: o que nunca pode ser verdade. Devolve a lista dos problemas (vazia: tudo certo). Nunca quebra: o que tem o tipo errado é um problema da lista."""
    P = []
    def tenta(nome, f):
        try: f()
        except Exception as x: P.append(f'{nome}: registro torto, não dá para conferir ({type(x).__name__}: {x})')
    def relogio():
        r = E['relogio']
        if not (r['dia'] >= 1 and 0 <= r['bloco'] < M.BLOCOS_DIA): P.append(f'relógio fora: dia {r["dia"]}, bloco {r["bloco"]}')
    tenta('o relógio', relogio)
    if sum(1 for p in E['gente'].values() if isinstance(p, dict) and p.get('jogador')) > 1: P.append('há mais de um personagem do jogador')
    L = E['itens']['itens']; O = E['itens'].get('obras', {})
    def pessoa(pid, p):
        n = p.get('nome', pid)
        if p['lugar'] not in E['lugares']: P.append(f'{n} está num lugar que não existe: {p["lugar"]}')
        if not _int(p['moedas']) or p['moedas'] < 0: P.append(f'{n} tem prata errada: {p["moedas"]}')
        if p['estado'] not in M.ESTADOS: P.append(f'{n} tem estado desconhecido: {p["estado"]}')
        if not 0 <= p['pv'] <= pv_max(p): P.append(f'{n} tem PV fora da faixa: {p["pv"]} de {pv_max(p)}')
        if p['estado'] == 'vivo' and p['pv'] <= 0: P.append(f'{n} consta entre os vivos com PV zero')
        for m in M.MEDIDORES:
            if not 0 <= p['corpo'][m] <= M.MED_MAX: P.append(f'{n} tem {m} fora da faixa: {p["corpo"][m]}')
        for b, q in (p.get('carga') or {}).items():
            if not _int(q) or q < 0: P.append(f'{n} carrega quantidade errada de {b}: {q}')
            if not bem_conhecido(b): P.append(f'{n} carrega o que não existe: "{b}"')
        if p.get('grau_oficio', 'diarista') not in M.SALARIO: P.append(f'{n} tem grau de ofício desconhecido: {p.get("grau_oficio")}')
        for k, v in (p.get('maestria') or {}).items():
            if v not in T.MAESTRIAS: P.append(f'{n} tem maestria fora da tabela em {k}: {v}')
        for k in ('talento', 'dom', 'inclinacao', 'tradicao', 'voto', 'laco', 'divida', 'funda', 'feiticos'):       # a etapa da magia
            if p.get(k) is not None:
                e = _magia_erro(E, p, k, p[k])
                if e: P.append(f'{n}: {e}')
        if p.get('mana') is not None and not (_num(p['mana']) and 0 <= p['mana'] <= mana_max(p)): P.append(f'{n} tem Mana fora da faixa: {p["mana"]} de {mana_max(p)}')
        mal = p.get('maldicoes') or []
        if not isinstance(mal, list): P.append(f'{n} tem as maldições tortas (não é uma lista)'); mal = []
        for m in mal:
            e = _maldicao_erro(E, m) if isinstance(m, dict) else 'o registro não é um dicionário'
            if e: P.append(f'{n} tem uma maldição torta ({m.get("id", "?") if isinstance(m, dict) else m}): {e}')
        if len({m.get('id') for m in mal if isinstance(m, dict)}) != len(mal): P.append(f'{n} tem duas maldições com o mesmo id')
        if p['estado'] == 'morto' and mal: P.append(f'{n} morreu e ainda tem maldição andando (elas vão para a morte dele)')
        usos = [it.get('uso') for it in L.values() if isinstance(it, dict) and it.get('dono') == pid and it.get('uso') in ('arma', 'arma2', 'escudo', 'foco', 'pescoco')]
        for u in set(usos):
            if usos.count(u) > 1: P.append(f'{n} tem duas peças em "{u}"')
        for k in PESSOA_4B:                                 # a etapa 4b: o povo, a idade, a segunda inclinação
            if p.get(k) is not None:
                e = _pessoa4b_erro(E, p, k, p[k])
                if e: P.append(f'{n}: {e}')
        mm = (p.get('marca') or {}).get('masmorra')         # A DESCIDA (etapa 4b)
        if mm is not None:
            if isinstance((p.get('marca') or {}).get('caca'), dict): P.append(f'{n} tem saída ao ermo e descida abertas ao mesmo tempo')
            e = _descida_erro(E, mm, pid)
            if e: P.append(f'{n} tem a descida (marca.masmorra) torta: {e}')
            elif mm.get('de') is not None:
                d = E['gente'].get(mm['de']); dd = (d.get('marca') or {}).get('masmorra') if isinstance(d, dict) else None
                if p['estado'] == 'morto' or not isinstance(dd, dict) or dd.get('de') is not None or pid not in (dd.get('com') or []) or d.get('estado') != 'vivo':
                    P.append(f'{n} foi junto numa descida que não existe mais (marca.masmorra)')
            elif p['estado'] == 'morto': P.append(f'{n} morreu com a descida aberta: `masmorra.py sair quem={pid}` faz as contas e fecha (ou `masmorra.py larga "por quê" quem={pid}`)')
        s = (p.get('marca') or {}).get('caca')
        if p['estado'] == 'morto':
            if p['moedas'] or p.get('carga'): P.append(f'{n} morreu e ainda tem prata ou carga (quem morre não fica com nada)')
            if s is not None: P.append(f'{n} morreu com a saída aberta: `caca.py volta quem={pid}` faz as contas e fecha (ou `caca.py larga quem={pid}`)')
        if s is not None:
            if not isinstance(s, dict) or s.get('ermo') not in E['lugares']: P.append(f'{n} tem a saída (marca.caca) torta: não diz um ermo que existe'); return
            if s.get('de') is not None:
                d = E['gente'].get(s['de']); sd = (d.get('marca') or {}).get('caca') if isinstance(d, dict) else None
                if not isinstance(sd, dict) or pid not in (sd.get('com') or []): P.append(f'{n} foi junto numa saída que não existe mais (marca.caca)')
            else:
                if s.get('fase') not in ('procura', 'encontro', 'luta') or not _int(s.get('restam')) or s['restam'] < 0 or s.get('casa') not in E['lugares'] or not isinstance(s.get('com', []), list):
                    P.append(f'{n} tem a saída (marca.caca) torta')
                elif s['fase'] == 'encontro' and not (isinstance(s.get('encontro'), dict) and especie(s['encontro'].get('especie')) and _int(s['encontro'].get('n')) and s['encontro']['n'] >= 1):
                    P.append(f'{n} tem um bicho à frente que a saída não descreve (marca.caca)')
                elif s['fase'] == 'luta' and not isinstance(s.get('luta'), str): P.append(f'{n} está em luta de caça sem o arquivo dela (marca.caca)')
    for pid, p in E['gente'].items(): tenta(f'a pessoa {pid}', lambda: pessoa(pid, p))
    def item_(iid, it):
        n = f'{it.get("nome", "?")} ({iid})'; dono = it.get('dono')
        if it.get('tipo') not in TIPOS_ITEM: P.append(f'{n} tem tipo desconhecido: {it.get("tipo")}')
        e = _item_magia_erro(it) if it.get('tipo') in TIPOS_ITEM else None
        if e: P.append(f'{n}: {e}')
        if it.get('uso') in USO_DO_TIPO and it.get('tipo') != USO_DO_TIPO[it['uso']]: P.append(f'{n} é {it.get("tipo")} e está em "{it["uso"]}"')
        if not _int(it['cat']) or not 0 <= it['cat'] < len(T.CATS): P.append(f'{n} tem categoria fora da tabela: {it["cat"]}')
        if dono is not None and dono not in E['gente']: P.append(f'{n} tem dono que não existe: {dono}')
        if it.get('uso') and not dono: P.append(f'{n} está em uso sem dono')
        if dono in E['gente'] and E['gente'][dono]['estado'] == 'morto': P.append(f'{n} ' + ('está em uso com alguém que morreu' if it.get('uso') else 'é de alguém que morreu (quem morre não fica com nada)'))
        if not 0 <= it['dur'][0] <= it['dur'][1]: P.append(f'{n} tem durabilidade fora da faixa')
        if it.get('onde') is not None and it['onde'] not in E['lugares']: P.append(f'{n} está num lugar que não existe: {it["onde"]}')
        if it.get('onde') is not None and dono: P.append(f'{n} tem dono e está largada num lugar ao mesmo tempo')
        if it.get('onde') is None and dono is None: P.append(f'{n} não tem dono nem lugar: não está em parte nenhuma')
        if it.get('solto') and (dono or it.get('onde') is None): P.append(f'{n} consta no chão (sem dono) e tem dono, ou não tem lugar')
        if it.get('uso') and it.get('uso') not in PARTES_VESTE: P.append(f'{n} tem uso desconhecido: {it["uso"]}')
        if it.get('tipo') == 'nucleo' and (it['dur'][0] != it['dur'][1] or it.get('uso')): P.append(f'{n} é núcleo e está gasto ou em uso')
        e = _item4b_erro(it)                                # a etapa 4b: a gazua, a chave, o talhe da armadura
        if e: P.append(f'{n}: {e}')
        if it.get('tipo') == 'chave' and not _abre_ok(E, it.get('abre')): P.append(f'{n} abre o que não existe: "{it.get("abre")}" (uma porta das portas da masmorra, ou o guardado de uma sala)')
        if it.get('uso') == 'veste' and dono in E['gente'] and not serve(it, E['gente'][dono]): P.append(f'{n} está em uso e não serve no corpo de {E["gente"][dono]["nome"]} ({corpo_de(E["gente"][dono])})')
    for iid, it in L.items(): tenta(f'o item {iid}', lambda: item_(iid, it))
    def obra(oid, o):
        if o.get('quem') not in E['gente'] or E['gente'][o['quem']]['estado'] == 'morto': P.append(f'a obra {oid} é de alguém que não existe ou morreu')
        if o.get('lugar') not in E['lugares']: P.append(f'a obra {oid} está num lugar que não existe: {o.get("lugar")}')
        if not _num(o.get('pede')) or o['pede'] < 1 or not _num(o.get('blocos')) or not 0 <= o['blocos'] <= o['pede']: P.append(f'a obra {oid} tem os blocos fora da conta: {o.get("blocos")} de {o.get("pede")}')
        if o.get('tipo') not in M.OBRAS: P.append(f'a obra {oid} tem tipo desconhecido: {o.get("tipo")}')
        if o.get('nucleo') is not None:
            nu = L.get(o['nucleo'])
            if not isinstance(nu, dict) or nu.get('tipo') != 'nucleo': P.append(f'a obra {oid} pede um núcleo que não está no Livro de Itens: {o["nucleo"]}')
            elif nu.get('dono') != o.get('quem'): P.append(f'o núcleo da obra {oid} não está na mão de quem forja')
        if o.get('tipo') == 'ajustar' and o.get('item') not in L: P.append(f'o ajuste {oid} é de uma peça que não está no Livro de Itens')
        if o.get('molde') is not None and not _molde_obra_ok(o['molde']): P.append(f'a obra {oid} tem um molde que não é efeito do catálogo: {o["molde"]}')
        for b, q in (o.get('materia') or {}).items():
            if not _num(q) or q < 0: P.append(f'a obra {oid} tem matéria errada: {q} de {b}')
    for oid, o in O.items(): tenta(f'a obra {oid}', lambda: obra(oid, o))
    def lugar(lid, l):
        n = l.get('nome', lid)
        for b, q in l['estoque'].items():
            if not _num(q) or q < 0: P.append(f'{n} tem estoque errado de {b}: {q}')
        for campo, teto in (('bichos', 'teto'), ('coleta', 'coleta_teto')):
            for b, q in (l.get(campo) or {}).items():
                e = _conta_erro(campo, b, q)
                if e: P.append(f'{n}: {e}'); continue
                t = (l.get(teto) or {}).get(b)
                if _num(t) and q > t: P.append(f'{n} tem mais {b} do que cabe: {q:g} de {t:g}')
            for b, q in (l.get(teto) or {}).items():
                e = _conta_erro(teto, b, q)
                if e: P.append(f'{n}: {e}')
        for campo in ('pop', 'oficina', 'preparo', 'longe', 'perigo', 'vizinhos', 'produz', 'alvo_pecas', 'botica', 'runas', 'santuario', 'maldito', 'covil') + CAMPOS_4B:
            if campo in l:
                e = _lugar_erro(E, campo, None, l[campo])
                if e: P.append(f'{n}: "{campo}" errado ({json.dumps(l[campo], ensure_ascii=False)[:60]}): {e}')
        lugar4b(lid, l, n)
    def lugar4b(lid, l, n):                                 # A ETAPA 4b: as ligações da masmorra e das salas; nenhuma sala é vizinha do que não é sala; o dragão
        Ls = E['lugares']; t = l.get('tipo'); viz = [v for v in (l.get('vizinhos') or []) if v in Ls]
        if t != 'sala':
            for v in viz:
                if Ls[v].get('tipo') == 'sala': P.append(f'{n} tem uma sala por vizinha ({v}): só as salas da mesma masmorra se ligam (a mesa da caça nunca lista uma sala)')
        if t == 'masmorra':
            if l.get('molde') not in M.MOLDES: P.append(f'{n} é masmorra e não diz o molde')
            if any(l.get(k) for k in ('bichos', 'teto', 'coleta', 'coleta_teto')): P.append(f'{n} é masmorra e tem bichos ou coleta: quem mora está nas salas (a caça a listaria como ermo)')
            minhas = {k for k, x in Ls.items() if isinstance(x, dict) and x.get('tipo') == 'sala' and x.get('masmorra') == lid}; vistas = []
            for nv in l.get('niveis') or []:
                for s in nv.get('salas') or []:
                    x = Ls.get(s); vistas.append(s)
                    if not isinstance(x, dict) or x.get('tipo') != 'sala' or x.get('masmorra') != lid or x.get('nivel') != nv.get('n'): P.append(f'{n}: a sala {s} do nível {nv.get("n")} não existe, não é dela ou está noutro nível')
            for s in sorted(minhas - set(vistas)): P.append(f'{n}: a sala {s} é dela e não está em nível nenhum')
            for s in sorted({s for s in vistas if vistas.count(s) > 1}): P.append(f'{n}: a sala {s} está em dois níveis')
            nv1 = ((l.get('niveis') or [{}])[0] or {}).get('salas') or []
            if l.get('entrada') not in nv1: P.append(f'{n}: a entrada ({l.get("entrada")}) não é uma sala do nível 1')
            for k in (l.get('portas') or {}):
                a, _, b = k.partition('|'); xa, xb = Ls.get(a), Ls.get(b)
                if not (isinstance(xa, dict) and isinstance(xb, dict) and a in minhas and b in minhas): P.append(f'{n}: a porta {k} não é de duas salas dela'); continue
                liga = (b in (xa.get('vizinhos') or []) and a in (xb.get('vizinhos') or [])) or any(isinstance(x, dict) and x.get('para') == o for s, o in ((xa, b), (xb, a)) for x in (s.get('segredos') or []))
                if not liga: P.append(f'{n}: a porta {k} não é de uma passagem (nem de um segredo) que existe')
        if t == 'sala':
            m = Ls.get(l.get('masmorra'))
            if not isinstance(m, dict) or m.get('tipo') != 'masmorra': P.append(f'{n} é sala de uma masmorra que não existe ({l.get("masmorra")})')
            elif not any(isinstance(nv, dict) and nv.get('n') == l.get('nivel') and lid in (nv.get('salas') or []) for nv in m.get('niveis') or []): P.append(f'{n} não está no nível que diz ({l.get("nivel")})')
            for v in viz:
                x = Ls[v]
                if x.get('tipo') != 'sala' or x.get('masmorra') != l.get('masmorra'): P.append(f'{n} tem por vizinha {v}, que não é sala da mesma masmorra (a entrada liga ao lado de fora pela masmorra)')
                elif lid not in (x.get('vizinhos') or []): P.append(f'{n} passa a {v}, e {v} não passa a ela (a passagem vale para os dois lados)')
            for x in l.get('segredos') or []:
                o = Ls.get(x.get('para')) if isinstance(x, dict) else None
                if not isinstance(o, dict) or o.get('tipo') != 'sala' or o.get('masmorra') != l.get('masmorra'): P.append(f'{n} tem um segredo para o que não é sala da mesma masmorra ({x})')
            portas = [x['onde'][6:] for x in l.get('armadilhas') or [] if isinstance(x, dict) and isinstance(x.get('onde'), str) and x['onde'].startswith('porta:')]
            for o in portas:
                if o not in (l.get('vizinhos') or []) and not any(isinstance(x, dict) and x.get('para') == o for x in l.get('segredos') or []): P.append(f'{n} tem uma armadilha na porta para {o}, que não é passagem dela')
            if l.get('guardado') is None and any(isinstance(x, dict) and x.get('onde') == 'guardado' for x in l.get('armadilhas') or []): P.append(f'{n} tem uma armadilha no guardado e não guarda nada')
            for b, q in (l.get('do_morto') or {}).items():
                if _num(q) and q > (l.get('estoque') or {}).get(b, 0): P.append(f'{n}: o que ficou junto do corpo ({q:g} de {b}) passa do que o estoque tem ({(l.get("estoque") or {}).get(b, 0):g})')
        elif l.get('do_morto'): P.append(f'{n} não é sala de masmorra e diz o que ficou junto de um corpo (do_morto): fora da sala, a carga e a prata do morto são o estoque do lugar')
        if isinstance(l.get('povos'), dict) and all(_num(v) for v in l['povos'].values()) and sum(l['povos'].values()) > 1 + 1e-9: P.append(f'{n}: as frações da gente (povos) somam mais que 1')
        dr = l.get('dragao')
        if isinstance(dr, dict) and _td() and dr.get('tipo') in _td().TIPOS and dr.get('idade') in _td().IDADES:
            esp = especie(_td().chave(dr['tipo'], dr['idade']))
            if isinstance(esp, dict) and _int(dr.get('pv')):
                mx = int(T.pv_max(esp['atributos']['Vigor'], esp['nivel']) * TB.TAMANHOS[esp['tamanho']]['pv'])
                if dr['pv'] > mx: P.append(f'{n}: o dragão {dr["nome"]} tem PV {dr["pv"]}, acima do máximo dele ({mx})')
    for lid, l in E['lugares'].items(): tenta(f'o lugar {lid}', lambda: lugar(lid, l))
    nomes = [x['dragao']['nome'] for x in E['lugares'].values() if isinstance(x, dict) and isinstance(x.get('dragao'), dict) and isinstance(x['dragao'].get('nome'), str)]
    for nm in sorted({x for x in nomes if nomes.count(x) > 1}): P.append(f'o dragão {nm} mora em dois lugares')
    tenta('a região', lambda: _valida_regiao(E, P))
    return P


def _valida_regiao(E, P):
    """OS INVARIANTES DA ETAPA FINAL: a estrada, a viagem, os campos novos da pessoa e o mundo.json (projeto/ETAPA_FINAL.md). O mundo sem região não tem nada disto."""
    Ls = E['lugares']; G = E['gente']; W = E.get('mundo') or {}
    pares = {}
    for lid, l in Ls.items():
        if not isinstance(l, dict): continue
        n = l.get('nome', lid)
        for v in l.get('vizinhos') or []:
            if isinstance(Ls.get(v), dict) and Ls[v].get('tipo') == 'estrada': P.append(f'{n} tem uma estrada por vizinha ({v}): a estrada liga pela ponta dela, não pelos vizinhos (a caça nunca a lista)')
        if l.get('tipo') != 'estrada': continue
        pt = l.get('ponta')
        if not (isinstance(pt, list) and len(pt) == 2 and pt[0] != pt[1] and all(isinstance(Ls.get(x), dict) and Ls[x].get('tipo') in M.POVOADOS for x in pt)):
            P.append(f'{n} é estrada e a ponta dela não são dois lugares de povo ({", ".join(M.POVOADOS)})'); continue
        k = '|'.join(sorted(pt))
        if k in pares: P.append(f'{n} e {Ls[pares[k]]["nome"]} ligam os mesmos dois lugares'); 
        pares[k] = lid
        if any(l.get(c) for c in ('vizinhos', 'bichos', 'teto', 'coleta', 'coleta_teto')): P.append(f'{n} é estrada e tem vizinhos, bichos ou coleta (a caça a listaria como ermo)')
        if not (_int(l.get('longe')) and M.ESTRADA_LONGE[0] <= l['longe'] <= M.ESTRADA_LONGE[1]): P.append(f'{n} tem os blocos fora da faixa ({M.ESTRADA_LONGE[0]} a {M.ESTRADA_LONGE[1]})')
        if not (_int(l.get('bando', 0)) and l.get('bando', 0) >= 0): P.append(f'{n} tem o bando torto')
        if l.get('passa') is not None and l['passa'] not in Ls: P.append(f'{n} passa por um lugar que não existe: {l["passa"]}')
    casas = W.get('casas') or {}; guildas = W.get('guildas') or {}
    for pid, p in G.items():
        if not isinstance(p, dict): continue
        n = p.get('nome', pid)
        for k in PESSOA_REGIAO:
            if p.get(k) is not None and k != 'herdeiro':
                e = _regiao_erro(E, pid, p, k, p[k])
                if e: P.append(f'{n}: {e}')
        for o, t in (p.get('lacos') or {}).items():
            if o not in G or t not in M.LACOS: P.append(f'{n} tem um laço torto: {o} ({t})')
        h = p.get('herdeiro')
        if h is not None and (h not in G or h == pid or not p.get('jogador')): P.append(f'{n} tem um herdeiro que não serve: {h}')
        v = (p.get('marca') or {}).get('viagem')
        if v is None: continue
        if isinstance((p.get('marca') or {}).get('caca'), dict) or isinstance((p.get('marca') or {}).get('masmorra'), dict): P.append(f'{n} tem viagem e saída (ou descida) abertas ao mesmo tempo')
        e = _viagem_erro(E, v, pid)
        if e: P.append(f'{n} tem a viagem (marca.viagem) torta: {e}')
        elif v.get('de') is not None:
            d = G.get(v['de']); dv = (d.get('marca') or {}).get('viagem') if isinstance(d, dict) else None
            if p['estado'] == 'morto' or not isinstance(dv, dict) or dv.get('de') is not None or pid not in (dv.get('com') or []) or d.get('estado') != 'vivo':
                P.append(f'{n} foi junto numa viagem que não existe mais (marca.viagem)')
        elif p['estado'] == 'morto': P.append(f'{n} morreu com a viagem aberta: `viagem.py larga "por quê" quem={pid}` fecha (as contas da estrada)')
    for cid, c in casas.items():
        if isinstance(c, dict) and c.get('sede') is not None and c['sede'] not in Ls: P.append(f'a casa {c.get("nome", cid)} tem sede num lugar que não existe')
    for gid, g in guildas.items():
        if isinstance(g, dict) and g.get('lider') is not None and g['lider'] not in G: P.append(f'a guilda {g.get("nome", gid)} tem um líder que não existe')
    for fid, f in (W.get('frentes') or {}).items():
        e = _mundo_forma(E, 'frentes', fid, f)
        if e: P.append(f'a frente {fid}: {e}')
    for mid, m in (W.get('missoes') or {}).items():
        e = _mundo_forma(E, 'missoes', mid, m)
        if e: P.append(f'a missão {mid}: {e}')
        elif m.get('quem') is not None and m['quem'] not in G: P.append(f'a missão {mid} foi tomada por quem não existe: {m["quem"]}')
    abertos = 0
    for xid, x in (W.get('caixa') or {}).items():
        e = _mundo_forma(E, 'caixa', xid, x)
        if e: P.append(f'o pedido {xid} da caixa: {e}')
        elif x.get('fim') is None: abertos += 1
    if abertos > M.CAIXA_MAX: P.append(f'a caixa tem {abertos} pedidos abertos (cabem {M.CAIXA_MAX})')
    for nid, x in (W.get('noticias') or {}).items():
        e = _mundo_forma(E, 'noticias', nid, x)
        if e: P.append(f'a notícia {nid}: {e}')


if __name__ == '__main__':
    import signal; hasattr(signal, 'SIGPIPE') and signal.signal(signal.SIGPIPE, signal.SIG_DFL)      # a saída cortada (`| head`) acaba o comando calada, sem erro de programa: tudo já foi gravado antes de falar
    a = sys.argv[1:]
    if a[:1] == ['valida']:
        P = valida(carrega()); print('\n'.join(P) if P else 'o estado está inteiro.'); sys.exit(1 if P else 0)
    elif a[:1] == ['eventos']:
        arq = os.path.join(pasta(), 'eventos.jsonl'); n = int(a[1]) if len(a) > 1 and a[1].isdigit() else 15
        for l in (open(arq, encoding='utf-8').read().splitlines()[-n:] if os.path.exists(arq) else []):
            ev = json.loads(l); print(f"#{ev['id']} Dia {ev['dia']}, {M.BLOCOS[ev['bloco']]} · {ev['tipo']}" + (f" · {ev['texto']}" if ev['texto'] else '') + f" · {tantos(len(ev['efeitos']), 'efeito')}")
    elif a[:1] == ['pessoa'] and len(a) > 1:
        E = carrega(); p = E['gente'].get(a[1]) or sys.exit(f'não há a pessoa "{a[1]}"')
        import pessoas, corpo
        from itens import rotulo
        if p['estado'] != 'vivo':                           # do morto só se diz que morreu (e onde): não tem ficha de luta, nem fome, nem forças, nem peça
            print(f"{p['nome']}, nível {p['nivel']}: {morte_diz(E, p)}. Quem morreu não fica com nada: o que era de {p['nome']} caiu ali."); sys.exit()
        casa = em_cena(E, a[1]); p = E['gente'][a[1]]         # quem não é o personagem aparece como VOLTA À CENA agora (o descanso em casa); este comando só olha: nada é gravado
        print(pessoas.linha(pessoas.ficha(lutador(E, a[1]))))
        feridas = ', '.join(f"{f['parte']}{' (grave)' if f['grave'] else ''}, do Dia {f['dia']}" for f in p['feridas']) or 'nenhuma'
        print(f"  corpo: {corpo.diz(p)} · feridas: {feridas} · prata: {p['moedas']} · {em(E, onde(E, a[1]))}")
        if casa: print(f"  ({p['nome']} descansou em casa desde a última vez em cena: é assim que volta a agir)")
        if p.get('carga'): print('  carga: ' + ', '.join(f'{q:g} de {nome_bem(b)}' for b, q in p['carga'].items()))
        usos = dict(arma='na mão', arma2='de reserva', escudo='no braço', veste='no corpo', foco='na mão, para lançar', pescoco='no pescoço')      # as mesmas palavras do ato.uso_diz
        for i, it in E['itens']['itens'].items():
            if it.get('dono') == a[1]: print(f"  {i} {rotulo(it, str(it['dur'][0]) + '/' + str(it['dur'][1]))}" + (f" · em uso, {'na cabeça' if it['uso'] == 'veste' and list(it.get('cobre') or []) == ['cabeça'] else usos.get(it['uso'], it['uso'])}" if it.get('uso') else ' · na guarda'))
    elif a[:1] == ['lugar'] and len(a) > 1:
        E = carrega(); l = E['lugares'].get(a[1]) or sys.exit(f'não há o lugar "{a[1]}" (os que há: {", ".join(E["lugares"])})')
        from itens import FEM, rotulo
        bem = nome_bem
        mil = lambda x: f'{int(x):,}'.replace(',', '.') if float(x).is_integer() else f'{x:g}'.replace('.', ',')
        conta = lambda d, teto=None, nome=str: ' · '.join(f"{nome(k)} {mil(v)}" + (f"/{mil(teto[k])}" if teto and k in teto else '') for k, v in d.items()) or 'nada'
        print(f"{l['nome']} [{a[1]}] · {l.get('tipo', 'lugar')}" + (f" · {l['habitat']}" if l.get('habitat') else '') + (f" · perigo {l['perigo']}" if l.get('perigo') else '') + (f" · a {tantos(l['longe'], 'bloco')} dos vizinhos" if l.get('longe') else '')
              + (f" · {mil(l['pop'])} de povo" if l.get('pop') else '') + (' · há cama' if l.get('cama') else '') + (f" · oficina {l['oficina']}" if l.get('oficina') is not None else ''))
        if l.get('sobre'): print(f"  {l['sobre']}")
        if l.get('vizinhos'): print('  vizinhos: ' + ', '.join(f"{E['lugares'][v]['nome']} [{v}]" if v in E['lugares'] else v for v in l['vizinhos']))
        if isinstance(l.get('preparo'), dict) and l['preparo']: print('  preparo da forja: ' + ' · '.join(f"{k} até o {T.CATS[v]}" for k, v in l['preparo'].items() if _int(v) and 0 <= v < len(T.CATS)))
        print('  estoque: ' + conta({k: v for k, v in l['estoque'].items() if v}, nome=bem))
        if isinstance(l.get('produz'), dict) and l['produz']: print('  produz por dia (antes de o preço e a estação mexerem): ' + conta(l['produz'], nome=bem))
        if isinstance(l.get('bichos'), dict) or isinstance(l.get('teto'), dict): print('  SÓ O MESTRE, os bichos (há/cabem): ' + conta(l.get('bichos') or {}, l.get('teto') or {}))
        if isinstance(l.get('coleta'), dict) or isinstance(l.get('coleta_teto'), dict): print('  SÓ O MESTRE, a matéria para tirar (há/cabe): ' + conta(l.get('coleta') or {}, l.get('coleta_teto') or {}, nome=bem))
        if isinstance(l.get('alvo_pecas'), dict) and l['alvo_pecas']: print('  a loja quer ter na prateleira: ' + ' · '.join(f"{tantos(v, 'peça ' + FEM[int(k)], 'peças ' + (FEM[int(k)][:-1] + 'ns' if FEM[int(k)].endswith('m') else FEM[int(k)] + 's'))}" for k, v in sorted(l['alvo_pecas'].items()) if k.isdigit() and int(k) < len(FEM)) + ' (acima disso, paga menos)')
        outros = {k: v for k, v in l.items() if k not in ('nome', 'em', 'tipo', 'habitat', 'perigo', 'longe', 'pop', 'cama', 'oficina', 'sobre', 'vizinhos', 'preparo', 'estoque', 'produz', 'bichos', 'teto', 'coleta', 'coleta_teto', 'alvo_pecas')}
        if outros: print('  e mais: ' + ' · '.join(f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in outros.items()))
        for i, it in E['itens']['itens'].items():
            if it.get('onde') == a[1]: print(f"  {i} {rotulo(it)}" + ((' · NO CHÃO, junto de um corpo (quem fica com ela é decisão de cena)' if de_morto(it) else ' · NO CHÃO, de quem achar') if it.get('solto') else ' · na prateleira'))
    elif a[:1] == ['mestre'] and len(a) in (2, 3):
        E = carrega()
        try: ef = json.loads(a[1])
        except ValueError as x: sys.exit(f'os efeitos vêm em JSON: uma lista de efeitos, cada um uma lista ({x}). Veja os verbos: python3 estado.py')
        if not isinstance(ef, list) or not ef or not all(isinstance(x, list) for x in ef): sys.exit('os efeitos são uma lista de listas: \'[["pessoa","eu","moedas","soma",5]]\'')
        if len(a) < 3 or not a[2].strip(): sys.exit('diga o que houve, entre aspas: o evento do Mestre vai para o registro e para o RETOMAR com esse texto (`python3 estado.py mestre \'[["pessoa","eu","moedas","soma",5]]\' "achou cinco moedas"`)')
        ev = aplica(E, 'mestre', ef, quem=[x[1] for x in ef if x[:1] == ['pessoa'] and len(x) > 1 and x[1] in E['gente']][:1], texto=a[2])
        if not ev: print('nada mudou: os efeitos já eram verdade. Nenhum evento foi registrado.'); sys.exit()
        grava(E); print(f"evento #{ev['id']} (mestre): {ev['texto']} · {tantos(len(ev['efeitos']), 'efeito')}"); P = valida(E)
        if P: print('ATENÇÃO, o estado ficou com problema:\n  ' + '\n  '.join(P))
    else: print(__doc__)
