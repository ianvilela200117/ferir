#!/usr/bin/env python3
"""nomes.py — MOTOR 10: OS NOMES DO MUNDO (gente, casa, lugar), pelo acaso do mundo. Nenhum nome sai de livro ou de jogo: as sílabas são do motor,
e o que bate num nome famoso da fantasia (a lista FAMOSOS) é trocado antes de ir à mesa.

  python3 nomes.py gente POVO N [semente=S]     N nomes de gente do povo (humano, anão, elfo, meio-orc, pequenino, gnomo)
  python3 nomes.py casa N [semente=S]            N nomes de casa nobre e de família
  python3 nomes.py lugar N [semente=S]           N nomes de lugar

Uso no motor: `Nomes(rng)` guarda os nomes já dados (não repete no mesmo mundo); `.gente(povo)`, `.casa(nobre)`, `.lugar(tipo)`.
"""
import random, sys, unicodedata

# ---------- a gente: o humano tem nomes da terra (comuns, de toda parte); os outros povos, sílabas do motor ----------
HUMANO_DADO = ['Aldo', 'Bento', 'Caio', 'Dimas', 'Elias', 'Fausto', 'Gil', 'Heitor', 'Ivo', 'Jonas', 'Lauro', 'Mauro', 'Nuno', 'Otávio', 'Paio', 'Quirino',
               'Rui', 'Simão', 'Tomé', 'Urbano', 'Vasco', 'Zeno', 'Abel', 'Brás', 'Celso', 'Davi', 'Ernesto', 'Fábio', 'Gaspar', 'Hugo', 'Inácio', 'Joaquim',
               'Lino', 'Mateus', 'Nelo', 'Orlando', 'Pedro', 'Raul', 'Sancho', 'Tito', 'Valter', 'Afonso', 'Bernardo', 'Cosme', 'Damião', 'Estêvão', 'Fernão',
               'Garcia', 'Henrique', 'Jordão', 'Leandro', 'Martim', 'Nicolau', 'Pascoal', 'Roque', 'Sebastião', 'Teodoro', 'Vicente', 'Amaro', 'Baltasar', 'Crispim',
               'Duarte', 'Eloi', 'Félix', 'Gervásio', 'Isidoro', 'Lourenço', 'Mendo', 'Onofre', 'Policarpo', 'Rodrigo', 'Salvador', 'Tristão', 'Urias', 'Vidal',
               'Alba', 'Beatriz', 'Clara', 'Dalva', 'Elvira', 'Flora', 'Graça', 'Helena', 'Inês', 'Joana', 'Laura', 'Mafalda', 'Nara', 'Olga', 'Paula', 'Quitéria',
               'Rute', 'Sara', 'Teresa', 'Úrsula', 'Vera', 'Zélia', 'Aurora', 'Branca', 'Cecília', 'Dora', 'Estela', 'Filipa', 'Glória', 'Hilda', 'Irene', 'Júlia',
               'Leonor', 'Marta', 'Noémia', 'Odete', 'Prisca', 'Rosa', 'Sílvia', 'Tânia', 'Violeta', 'Adelaide', 'Benedita', 'Constança', 'Domingas', 'Eulália',
               'Fernanda', 'Genoveva', 'Isabel', 'Josefa', 'Lucinda', 'Madalena', 'Natália', 'Ofélia', 'Paulina', 'Rafaela', 'Serafina', 'Tomásia', 'Valentina',
               'Águeda', 'Brites', 'Catarina', 'Dulce', 'Ermelinda', 'Felícia', 'Guiomar', 'Iria', 'Justa', 'Lia', 'Mécia', 'Olímpia', 'Petronila', 'Sancha', 'Urraca']
SILABAS = {      # (começos, meios, fins): o nome é começo + (meio) + fim
    'humano':    (['Al', 'Ber', 'Cel', 'Dan', 'Er', 'Fer', 'Gil', 'Her', 'Ir', 'Jor', 'Lou', 'Mar', 'Nor', 'Os', 'Per', 'Ros', 'Sel', 'Ter', 'Val', 'Ves'],
                  ['', '', 'an', 'el', 'in', 'or', 'ar'], ['o', 'a', 'eu', 'ão', 'ia', 'ino', 'ina', 'ado', 'ada']),
    'anão':      (['Ta', 'Du', 'Bra', 'Ko', 'Gru', 'Ha', 'Ro', 'Vo', 'Ma', 'U', 'Bo', 'Dra', 'Kre', 'To', 'Gu', 'Ba', 'Hu'],
                  ['rn', 'rv', 'lk', 'sk', 'nd', 'rd', 'gr', 'mb', 'rk', 'ld', 'rg', 'st'], ['o', 'a', 'u', 'ek', 'um', 'ar', 'in', 'ur', 'ok', 'ia']),
    'elfo':      (['I', 'E', 'A', 'Ae', 'Si', 'Le', 'Ve', 'Na', 'Ce', 'Mi', 'Sae', 'Ny', 'Ili', 'Ela', 'Ora'],
                  ['l', 'lv', 'n', 'r', 's', 'ss', 'nw', 'lr', 'm'], ['ena', 'ara', 'ine', 'eli', 'ane', 'oril', 'ael', 'issa', 'ion', 'ys']),
    'meio-orc':  (['Bra', 'Gru', 'Ka', 'U', 'Dro', 'Ga', 'Mu', 'Zo', 'Ra', 'Tu', 'Bo', 'Vru'],
                  ['sc', 'sk', 'zz', 'gg', 'rk', 'sh', 'kt', 'rg'], ['o', 'a', 'u', 'ag', 'ok', 'ul', 'ash']),
    'pequenino': (['Ne', 'Bi', 'Lu', 'Pi', 'Mo', 'Ti', 'Fu', 'Do', 'Ca', 'Ma', 'Be', 'Ro'],
                  ['n', 'l', 'p', 't', 'm', 'ss', 'nd', 'rr'], ['a', 'o', 'i', 'inho', 'ita', 'ico', 'ela', 'ito']),
    'gnomo':     (['Fi', 'Zo', 'Pe', 'Ni', 'Bo', 'Ru', 'Ti', 'Qui', 'Za', 'Fe', 'Lo', 'Bi'],
                  ['zz', 'b', 'dd', 'ck', 'p', 'm', 'nk', 'lb'], ['el', 'ino', 'o', 'a', 'ana', 'olo', 'eta', 'ulo']),
}
# ---------- as casas: a nobre tem nome de linhagem; a comum, do ofício, do lugar ou de alcunha ----------
CASA_NOBRE = (['Val', 'Alb', 'Ter', 'Mon', 'Cas', 'Bel', 'Dor', 'Fal', 'Gal', 'Lor', 'Mir', 'Nav', 'Or', 'Ros', 'Sar', 'Tav', 'Ul', 'Var', 'Ver', 'Ast'],
              ['', 'a', 'e', 'i', 'o'], ['mor', 'rena', 'sal', 'dano', 'cor', 'ves', 'lan', 'mira', 'roz', 'tel', 'gar', 'del', 'vira', 'nor', 'quim', 'ena'])
CASA_COMUM = ['Ferreira', 'Moleiro', 'Pastor', 'Carvalho', 'Pereira', 'Lobo', 'Raposo', 'Cordeiro', 'Ribeiro', 'Souto', 'Barreiro', 'Pinheiro', 'Teixeira',
              'Salgueiro', 'Cabral', 'Coelho', 'Gago', 'Ruivo', 'Moreno', 'Calvo', 'Franco', 'Amado', 'Bravo', 'Leal', 'Pardo', 'Seixas', 'Mota', 'Vilar',
              'Fontes', 'Lagos', 'Rocha', 'Serra', 'Valente', 'Matos', 'Prado', 'Brandão', 'Couto', 'Faria', 'Godinho', 'Junqueira', 'Lemos', 'Neiva',
              'Outeiro', 'Paiva', 'Quintas', 'Rego', 'Sampaio', 'Tavares', 'Veloso', 'Antunes', 'Bastos', 'Caldas', 'Dorneles', 'Esteves', 'Freitas']
# ---------- os lugares ----------
LUGAR_NOME = [('Pedra', 'a'), ('Vau', 'o'), ('Serra', 'a'), ('Ponte', 'a'), ('Fonte', 'a'), ('Porto', 'o'), ('Campo', 'o'), ('Vale', 'o'), ('Monte', 'o'),
              ('Torre', 'a'), ('Lagoa', 'a'), ('Cruz', 'a'), ('Ribeira', 'a'), ('Outeiro', 'o'), ('Penha', 'a'), ('Moinho', 'o'), ('Atalaia', 'a'),
              ('Castro', 'o'), ('Souto', 'o'), ('Freixo', 'o'), ('Pinhal', 'o'), ('Barca', 'a'), ('Poço', 'o'), ('Várzea', 'a'), ('Coval', 'o'), ('Ermida', 'a')]
ADJ = [('Rasa', 'Raso'), ('Seca', 'Seco'), ('Fria', 'Frio'), ('Alta', 'Alto'), ('Velha', 'Velho'), ('Nova', 'Novo'), ('Negra', 'Negro'), ('Branca', 'Branco'),
       ('Funda', 'Fundo'), ('Larga', 'Largo'), ('Verde', 'Verde'), ('Queimada', 'Queimado'), ('Partida', 'Partido'), ('Torta', 'Torto'), ('Brava', 'Bravo'),
       ('Mansa', 'Manso'), ('Grande', 'Grande'), ('Escura', 'Escuro'), ('Clara', 'Claro'), ('Real', 'Real'), ('Cinzenta', 'Cinzento'), ('Doce', 'Doce')]
DE = ['do Corvo', 'da Lua', 'do Lobo', 'das Pedras', 'do Freixo', 'dos Mortos', 'da Bruma', 'do Sal', 'do Ferro', 'das Cinzas', 'do Carvalho', 'da Garça',
      'do Urso', 'das Águas', 'do Vento', 'da Cruz', 'dos Sinos', 'do Gamo', 'da Névoa', 'das Rosas', 'do Touro', 'da Lebre', 'do Junco', 'dos Ossos']
ERMO_NOME = {'floresta': ['a Mata', 'o Bosque', 'a Floresta', 'o Souto'], 'campo': ['o Campo', 'a Charneca', 'os Ermos', 'a Planura'],
             'brejo': ['o Brejo', 'o Pântano', 'o Lameiro', 'a Turfeira'], 'serra': ['a Serra', 'os Penhascos', 'a Cordilheira', 'o Alto'],
             'caverna': ['as Grutas', 'a Lapa', 'as Furnas', 'o Fojo'], 'ruína': ['as Ruínas', 'o Campo Velho', 'os Escombros', 'a Cidade Morta']}
# os nomes que não podem sair (os famosos da fantasia de livro e de jogo): o gerador troca o que bater, inteiro ou nas quatro primeiras letras
FAMOSOS = ['Gimli', 'Thorin', 'Legolas', 'Elrond', 'Drizzt', 'Bilbo', 'Frodo', 'Samwise', 'Gandalf', 'Aragorn', 'Galadriel', 'Balin', 'Dwalin', 'Durin', 'Thrain',
           'Dain', 'Gloin', 'Bombur', 'Bifur', 'Bofur', 'Fili', 'Kili', 'Elendil', 'Arwen', 'Eowyn', 'Boromir', 'Faramir', 'Smaug', 'Sauron', 'Saruman',
           'Tauriel', 'Thranduil', 'Celeborn', 'Glorfindel', 'Haldir', 'Raistlin', 'Tasslehoff', 'Elminster', 'Mordenkainen', 'Vecna', 'Strahd', 'Tiamat',
           'Bahamut', 'Lolth', 'Gruumsh', 'Moradin', 'Corellon', 'Yondalla', 'Bruenor', 'Wulfgar', 'Regis', 'Jarlaxle', 'Minsc', 'Volo', 'Borin', 'Gollum',
           'Sméagol', 'Pippin', 'Merry', 'Gorbag', 'Shagrat', 'Ugluk', 'Azog', 'Bolg', 'Grishnakh', 'Lurtz', 'Geralt', 'Ciri', 'Yennefer', 'Triss', 'Dandelion',
           'Conan', 'Elric', 'Fafhrd', 'Ged', 'Kvothe', 'Rand', 'Moiraine', 'Arya', 'Sansa', 'Tyrion', 'Daenerys', 'Jaime', 'Cersei', 'Brienne', 'Eragon', 'Saphira',
           'Dumbo', 'Bambi', 'Mandela', 'Gandhi', 'Napoleão', 'César', 'Hitler', 'Stalin', 'Shrek', 'Zelda', 'Ganon', 'Link', 'Mario', 'Luigi', 'Sonic', 'Kratos', 'Merlin', 'Arthur', 'Lancelot', 'Morgana']
# o que não pode ser nome de jeito nenhum (o palavrão e a ofensa, na língua do jogador): o nome que é, ou começa por, uma destas sai
FEIOS = ['bixa', 'bicha', 'puta', 'caralh', 'merda', 'porra', 'buceta', 'viado', 'corno', 'bosta', 'foda', 'piroca', 'xota', 'cacete', 'punhet', 'vagabund',
         'otari', 'idiot', 'burr', 'coco', 'cuzao', 'rola', 'pica', 'pinto', 'peido', 'mijo', 'tesao', 'safad', 'traveco', 'macaco', 'negao', 'retardad']
_FAM = None


def _sem_acento(s): return ''.join(c for c in unicodedata.normalize('NFD', s.lower()) if unicodedata.category(c) != 'Mn')


def feio(nome):
    """o nome é (ou começa por) um palavrão ou uma ofensa?"""
    n = _sem_acento(nome).replace(' ', '')
    return any(n.startswith(f) for f in FEIOS) or n in ('cu', 'cus')


def famoso(nome):
    """o nome bate num famoso (inteiro; ou, nos famosos de cinco letras ou mais, começa com as quatro primeiras letras dele)?"""
    global _FAM
    if _FAM is None: _FAM = [_sem_acento(x) for x in FAMOSOS]
    n = _sem_acento(nome.split()[-1] if nome.split() else nome)
    return any(n == f or (len(f) >= 5 and len(n) >= 4 and n[:4] == f[:4]) for f in _FAM)


class Nomes:
    """os nomes de um mundo: não repete o que já deu (a gente, as casas, os lugares)"""
    def __init__(self, rng, usados=()):
        self.r = rng; self.usados = {_sem_acento(x) for x in usados}

    def _novo(self, faz, tentativas=200):
        for _ in range(tentativas):
            n = faz()
            k = _sem_acento(n)
            if k not in self.usados and not famoso(n) and not feio(n) and len(k.replace(' ', '')) >= 4: self.usados.add(k); return n
        n = faz() + ' ' + self.r.choice(['o Moço', 'o Velho', 'a Moça', 'a Velha', 'o Ruivo', 'a Ruiva'])      # esgotou: a alcunha separa
        self.usados.add(_sem_acento(n)); return n

    def silabas(self, povo):
        a, b, c = SILABAS.get(povo, SILABAS['humano'])
        return (self.r.choice(a) + self.r.choice(b) + self.r.choice(c)).capitalize()

    def gente(self, povo='humano'):
        if povo == 'humano': return self._novo(lambda: self.r.choice(HUMANO_DADO) if self.r.random() < 0.8 else self.silabas('humano'))
        return self._novo(lambda: self.silabas(povo))

    def casa(self, nobre=False):
        if nobre: return self._novo(lambda: (self.r.choice(CASA_NOBRE[0]) + self.r.choice(CASA_NOBRE[1]) + self.r.choice(CASA_NOBRE[2])).capitalize())
        return self._novo(lambda: self.r.choice(CASA_COMUM))

    def lugar(self, tipo='vila'):
        """o nome de um lugar de povo, com o artigo quando o tem ('Pedra Rasa', 'o Vau do Corvo')"""
        def faz():
            nm, g = self.r.choice(LUGAR_NOME)
            if self.r.random() < 0.55: a = self.r.choice(ADJ); return f"{nm} {a[0] if g == 'a' else a[1]}"
            d = self.r.choice([x for x in DE if nm.lower() not in x.lower()])
            return f"{nm} {d}"
        return self._novo(faz)

    def ermo(self, habitat):
        return self._novo(lambda: f"{self.r.choice(ERMO_NOME.get(habitat, ['o Ermo']))} {self.r.choice(DE)}")

    def de(self):
        return self.r.choice(DE)


def em(nome):
    """'em Pedra Rasa', 'na Mata do Corvo', 'no Vau Seco' (o lugar com artigo leva a contração)"""
    art, _, resto = nome.partition(' ')
    return {'a': 'na ', 'o': 'no ', 'as': 'nas ', 'os': 'nos '}[art] + resto if art in ('a', 'o', 'as', 'os') and resto else 'em ' + nome


if __name__ == '__main__':
    a = sys.argv[1:]; op = dict(x.split('=', 1) for x in a if '=' in x); pos = [x for x in a if '=' not in x]
    r = random.Random(int(op.get('semente', 1))); N = Nomes(r)
    if pos[:1] == ['gente'] and len(pos) == 3 and pos[2].isdigit(): print(', '.join(N.gente(pos[1]) for _ in range(int(pos[2]))))
    elif pos[:1] == ['casa'] and len(pos) == 2 and pos[1].isdigit(): print(', '.join(N.casa(i % 3 == 0) for i in range(int(pos[1]))))
    elif pos[:1] == ['lugar'] and len(pos) == 2 and pos[1].isdigit(): print(', '.join(N.lugar() for _ in range(int(pos[1]))))
    else: print(__doc__)
