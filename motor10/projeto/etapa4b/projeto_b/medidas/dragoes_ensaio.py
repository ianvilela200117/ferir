"""dragoes_ensaio.py: os dragões de verdade, montados com o bichos.bicho() de hoje (categoria, tamanho, nível, atributos, instinto, armas, traços, fases), sem mexer no motor.
As idades e os tipos são a proposta do projeto B (rascunho: os números são os que se medem aqui)."""
import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-ferir/2caa978a-1aa4-5b05-88b7-11bcda935cb0/scratchpad/masmorras/projeto_b/medidas')
from base_b import *

# a idade: (grau, categoria, tamanho, nível, instinto, (Força, Agilidade, Vigor, Vontade, Percepção, Afinidade), armas, traços da idade)
IDADES = {
    'filhote': dict(cat=1, tamanho='médio',  nivel=30,  instinto=2, at=(70, 80, 70, 50, 70, 40),     armas=['garra', 'presa'],             tracos=['sopro']),
    'jovem':   dict(cat=2, tamanho='grande', nivel=80,  instinto=6, at=(120, 70, 150, 60, 75, 45),   armas=['garra', 'bocarra', 'cauda'],  tracos=['sopro', 'apavora']),
    'adulto':  dict(cat=3, tamanho='enorme', nivel=110, instinto=6, at=(140, 70, 150, 80, 85, 50),   armas=['garra', 'bocarra', 'cauda'],  tracos=['sopro', 'apavora', 'couraça']),
    'velho':   dict(cat=4, tamanho='enorme', nivel=160, instinto=6, at=(160, 70, 200, 90, 90, 55),   armas=['garra', 'bocarra', 'cauda'],  tracos=['sopro', 'apavora', 'couraça']),
    'ancião':  dict(cat=5, tamanho='enorme', nivel=220, instinto=8, at=(180, 70, 240, 100, 90, 60),  armas=['garra', 'bocarra', 'cauda'],  tracos=['sopro', 'apavora', 'couraça']),
}
# o tipo: o que muda do lugar onde vive (traços a mais e a menos)
TIPOS = {
    'serra':  dict(mais=['voa'], menos=[]),              # o das alturas: voa e sopra fogo
    'brejo':  dict(mais=['veneno'], menos=[]),           # o verme do brejo: não voa; o bafo e a cauda envenenam
    'grutas': dict(mais=['noturno', 'agarra'], menos=[]),  # o de baixo: não voa; vê no escuro e enrosca
}


def dragao(tipo='serra', idade='jovem', nome=None, fases=None, **mais):
    i = IDADES[idade]; t = TIPOS[tipo]
    tr = [x for x in i['tracos'] + t['mais'] if x not in t['menos']]
    at = dict(zip(T.ATRIBUTOS, i['at']))
    p = bichos.bicho('dragão', nome=nome or f'o dragão {idade}', cat=i['cat'], tamanho=i['tamanho'], nivel=i['nivel'], instinto=i['instinto'], atributos=at, armas=list(i['armas']), tracos=tr, **mais)
    if fases: p['fases'] = [dict(x) for x in fases]
    return p


REF = {0: 10, 1: 30, 2: 50, 3: 90, 4: 120, 5: 150}      # o homem do degrau (tabelas_criaturas.REF)


def grupo(k, nivel, arma, arm, familia='espada', pre='h', misto=False, **kw):
    """k homens; misto: dois de espada e escudo, um de lança e escudo, um de arco (com adaga de reserva), o resto de espada"""
    def um(i):
        if misto and i == 2: return homem(f'{pre}{i + 1}', nivel, arma=arma, arm=arm, familia='lança', **kw)
        if misto and i == 3:
            p = padrao(f'{pre}{i + 1}', nivel, molde='arqueiro', **kw); veste(p, arma=('arco', arma), armadura=('couro', arm), arma2=('adaga', arma)); p['linha'] = 'trás'; return p
        return homem(f'{pre}{i + 1}', nivel, arma=arma, arm=arm, familia=familia, **kw)
    return lambda: [um(i) for i in range(k)]
