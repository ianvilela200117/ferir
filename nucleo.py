#!/usr/bin/env python3
"""nucleo.py — o que todos os scripts do motor dividem (MOTOR 6, Dia 379).

Não se roda sozinho. Dá aos outros scripts:
  d(n)                 o dado verdadeiro (secrets), o mesmo de sempre
  carrega / grava      JSON com gravação ATÔMICA (um script que cai no meio não estraga o arquivo)
  dia_atual()          o dia do relógio (estado.json)
  anota(texto)         escreve uma linha no fim do ENVELOPE atual, sem o Mestre abrir o arquivo
  toca_a_casa(texto)   o texto fala de algo que o reino vigia? (lista em motor.json -> vigia)
  agenda_add(...)      marca um dia futuro (agenda.json)
  acha_nome(...)       acha um nome mesmo com acento, caixa ou pedaço errado
"""
import json, os, re, secrets, datetime, glob, unicodedata, difflib

AQUI = os.path.dirname(os.path.abspath(__file__))


def P(*a):
    return os.path.join(AQUI, *a)


def d(n):
    return secrets.randbelow(n) + 1


def agora():
    return datetime.datetime.now().strftime('%H:%M:%S')


def carrega(nome, padrao=None):
    f = P(nome)
    if not os.path.exists(f):
        return {} if padrao is None else padrao
    with open(f, encoding='utf-8') as fh:
        return json.load(fh)


def grava(nome, obj):
    f = P(nome)
    tmp = f + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=1)
    os.replace(tmp, f)


def ler(nome):
    f = nome if os.path.isabs(nome) else P(nome)
    if not os.path.exists(f):
        return ''
    with open(f, encoding='utf-8', errors='replace') as fh:
        return fh.read()


def sem_acento(s):
    return ''.join(c for c in unicodedata.normalize('NFD', str(s)) if unicodedata.category(c) != 'Mn').lower()


def dia_atual():
    return carrega('estado.json').get('tempo', {}).get('dia', 0)


# ---------- o envelope ----------
def envelopes():
    return sorted(glob.glob(P('envelope_sessao*.md')))


def envelope_atual():
    xs = envelopes()
    return xs[-1] if xs else P('envelope_sessao2.md')


def anota(texto, arquivo=None):
    """acrescenta uma linha (ou várias) ao fim do envelope atual"""
    f = arquivo or envelope_atual()
    precisa_nl = False
    if os.path.exists(f) and os.path.getsize(f):
        with open(f, 'rb') as fh:
            fh.seek(-1, 2)
            precisa_nl = fh.read(1) != b'\n'
    with open(f, 'a', encoding='utf-8') as fh:
        fh.write(('\n' if precisa_nl else '') + texto.rstrip('\n') + '\n')


# ---------- o que a casa vigia ----------
_MOTOR = None


def motor():
    global _MOTOR
    if _MOTOR is None:
        _MOTOR = carrega('motor.json', {})
    return _MOTOR


_VIGIA = None


def toca_a_casa(texto):
    """o texto cita, como palavra inteira, algo da lista 'vigia' do motor.json?"""
    global _VIGIA
    if _VIGIA is None:
        ps = [re.escape(sem_acento(p)) for p in motor().get('vigia', []) if p.strip()]
        _VIGIA = re.compile(r'(?<![a-z0-9])(?:' + '|'.join(ps) + r')(?![a-z0-9])') if ps else False
    return bool(_VIGIA and _VIGIA.search(sem_acento(texto)))


# ---------- o calendário (Livro do Mundo, 01_mundo.md, seção 6) ----------
LUAS = ['do Gelo', 'do Lobo', 'da Cinza', 'do Degelo', 'da Semente', 'das Barcas', 'do Sal', 'da Forja', 'da Seca', 'do Grão', 'do Vinho', 'das Velas']
ESTACOES = ['Inverno', 'Degelo', 'Sol', 'Colheita']


def calendario(dia):
    """12 luas de 30 dias + 5 Dias Mudos = 365. Âncora do Livro: Dia 190 = 1 da Lua do Gelo de 1013 d.S."""
    doy = (dia - 190) % 365 + 1
    ano = 1013 + (dia - 190) // 365
    if doy > 360:
        return {'lua': 0, 'dia_lua': doy - 360, 'ano': ano, 'estacao': 'Dias Mudos', 'mudo': True,
                'txt': f'{doy - 360}º Dia Mudo de {ano} d.S.',
                'nota': 'DIA MUDO: não se acende forja grande, não se faz magia de 4º círculo para cima e não se casa'}
    lua = (doy - 1) // 30 + 1
    dl = (doy - 1) % 30 + 1
    nota = 'LUA NOVA (a do nome do servo)' if dl == 1 else 'lua cheia' if dl == 15 else ''
    if dl == 1 and lua in (1, 4, 7, 10):
        nota += f' · COMEÇA A ESTAÇÃO: {ESTACOES[(lua - 1) // 3]}'
    return {'lua': lua, 'dia_lua': dl, 'ano': ano, 'estacao': ESTACOES[(lua - 1) // 3], 'mudo': False,
            'txt': f'{dl} da Lua {LUAS[lua - 1]} de {ano} d.S., {ESTACOES[(lua - 1) // 3]}', 'nota': nota}


def camada(nome):
    """a camada de simulação está ligada? (motor.json -> camadas)"""
    return bool(motor().get('camadas', {}).get(nome, True))


# ---------- a agenda ----------
def agenda_add(dia, texto, tipo='marco', oculto=False, para=False, origem='', toca=None):
    A = carrega('agenda.json', {'prox_id': 1, 'itens': []})
    it = {'id': A['prox_id'], 'dia': int(dia), 'texto': texto, 'tipo': tipo, 'oculto': bool(oculto),
          'para': bool(para), 'origem': origem, 'feito': False,
          'toca': toca_a_casa(texto) if toca is None else bool(toca)}
    if tipo == 'noticia' and camada('boatos'):
        # BOATOS (camada nova): a notícia viaja de boca em boca. Onde a casa tem célula de espionagem viva, chega fiel.
        cel = carrega('mundo_vivo.json').get('espionagem', {}).get('celulas', {})
        tem_olho = any(v.get('forca', 0) > 0 and sem_acento(k.split()[-1]) in sem_acento(texto) for k, v in cel.items())
        r = d(20)
        it['boato'] = [r, 'FIEL (a célula da casa confirma)' if tem_olho else
                       'FALSA: chega trocada (outro lugar, outro culpado ou o contrário do que houve)' if r <= 2 else
                       'EXAGERADA: chega maior do que foi' if r <= 6 else
                       'INCOMPLETA: falta quem fez ou onde foi' if r <= 9 else 'FIEL']
    A['itens'].append(it)
    A['prox_id'] += 1
    grava('agenda.json', A)
    return it


def agenda_do_dia(dia, incluir_atrasados=True):
    A = carrega('agenda.json', {'prox_id': 1, 'itens': []})
    return [i for i in A['itens'] if not i['feito'] and (i['dia'] == dia or (incluir_atrasados and i['dia'] < dia and i['tipo'] != 'noticia'))]


# ---------- nomes ----------
def acha_nome(nome, chaves):
    """devolve (chave, sugestoes). chave é None se não achou um só."""
    chaves = list(chaves)
    if nome in chaves:
        return nome, []
    n = sem_acento(nome)
    iguais = [k for k in chaves if sem_acento(k) == n]
    if len(iguais) == 1:
        return iguais[0], []
    comeca = [k for k in chaves if sem_acento(k).startswith(n)]
    if len(comeca) == 1:
        return comeca[0], []
    dentro = [k for k in chaves if n in sem_acento(k)]
    if len(dentro) == 1:
        return dentro[0], []
    sug = (comeca or dentro) or difflib.get_close_matches(nome, chaves, n=5, cutoff=0.6)
    return None, sug[:8]


def faixa_txt(a, b):
    return str(a) if a == b else f'{a}-{b}'


def morto(v):
    """506 (erro achado): morto é quem tem MORTO ou MORTA no estado (em qualquer caixa) ou na frente da ocupação.
    Antes cada script procurava só 'MORTO' no estado, e a Mamiltia, a Carea, o Quthemnus e o Pelaccino viviam a semana."""
    import re as _re
    e = str(v.get('estado', '')).upper(); o = str(v.get('ocupacao', '')).upper().lstrip('( ')
    if e.lstrip('( ').startswith('VIVO'): return False   # 'vivo (morto pelo Morek no 425 e ERGUIDO...)': o Starkald e o Goir
    return bool(_re.search(r'\bMORT[OA]\b', e)) or o.startswith('MORTO') or o.startswith('MORTA')
