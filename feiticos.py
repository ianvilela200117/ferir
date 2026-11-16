#!/usr/bin/env python3
"""GRIMÓRIO DO MUNDO (regra da casa, Dia 200): feitiços de amostra das 12 escolas, do 1º ao 4º círculo.
Dano base (X.8): 1º-3º = 2d6 × círculo num alvo · 4º-6º = 4d6 × círculo.
MAGIA MAIS FORTE (regra da casa, Dia 200): o dano e a cura do feitiço são multiplicados pelo FOCO de quem lança
(Comum ×1 · Incomum ×1,25 · Raro ×1,5 · Épico ×2 · Único ×3 · Lendário ×5 · Mítico ×10 · Primordial ×20, casa 356); em ÁREA, metade do multiplicador (mín. ×1).
Feitiço preso numa peça (encantamento ou efeito de magia do Único) usa a categoria da PEÇA como foco.
Saber um feitiço = poder lançar (Magia) e poder IMBUIR (Encantamento: o feitiço conhecido conta como receita de encantamento).
Uso: python3 feiticos.py lista [ESCOLA]   ·   python3 feiticos.py sorteia [circ_max] [escola]
"""
import sys, secrets
G = [
 # Chama (Int)
 ('Chama',1,'Faísca','2d6 de fogo num alvo a 9 m','ataque'),
 ('Chama',1,'Alma de Brasa','a peça guarda fogo: 1x por cena +1d6 de fogo no golpe ou acende qualquer coisa','arma'),
 ('Chama',2,'Dardo Arcano','4d6, ignora armadura leve','ataque'),
 ('Chama',2,'Calor de Forja','um metal à mão fica em brasa por 1 minuto (molda sem fornalha; quem segura sem luva solta)','utilidade'),
 ('Chama',3,'Flor de Brasa','bola de fogo de 3 m de raio, 6d6 (área)','ataque'),
 ('Chama',4,'Chuva de Brasas','9 m, 8d6 de fogo, o chão queima 2 rodadas (área)','ataque'),
 # Gelo (Int)
 ('Gelo',1,'Frio de Mão','congela água, conserva comida um mês, ou 2d6 de frio no toque','utilidade'),
 ('Gelo',2,'Névoa Fria','esconde uma área de 9 m por 1 cena','utilidade'),
 ('Gelo',2,'Ponte de Gelo','uma passarela de gelo de 10 m sobre água ou abismo, por 1 hora','utilidade'),
 ('Gelo',3,'Geada de Lâmina','o golpe congela: −4 de Defesa e Lento 1 rodada','arma'),
 ('Gelo',3,'Muralha de Gelo','bloqueia uma passagem (RD 12, 60 PV)','defesa'),
 ('Gelo',4,'Inverno Breve','16d6 de frio num alvo, que fica preso no gelo 1 rodada','ataque'),
 # Pedra (Int)
 ('Pedra',1,'Mão de Pedra','o punho ou a arma vira pedra: +2 de dano, não quebra','arma'),
 ('Pedra',2,'Pele de Pedra','+4 de Defesa por 3 rodadas','defesa'),
 ('Pedra',2,'Abrir a Rocha','abre uma passagem de 1 m em rocha ou muro de pedra (1 minuto)','utilidade'),
 ('Pedra',3,'Raiz de Pedra','o alvo não pode ser derrubado, empurrado nem arrastado por 1 cena','defesa'),
 ('Pedra',3,'Muro Erguido','ergue um muro de pedra de 6 m × 3 m (permanente)','defesa'),
 ('Pedra',4,'Tremor','quem está a 12 m cai (Agilidade CD 25) e leva 4d6','ataque'),
 # Vento (Int)
 ('Vento',1,'Empurrão','empurra 2 m, ou apaga fogo pequeno','utilidade'),
 ('Vento',1,'Passo de Vento','+6 m de movimento e salto triplo por 1 rodada','defesa'),
 ('Vento',2,'Voz no Vento','a voz chega a 1 km, ou uma conversa longe é ouvida','utilidade'),
 ('Vento',3,'Escudo de Vento','projéteis erram com 1-10 no d20 por 1 cena','defesa'),
 ('Vento',3,'Lâmina de Vento','6d6 num alvo a 18 m, atravessa cobertura leve','ataque'),
 ('Vento',4,'Tempestade Local','3 rodadas de vento e raio, 4d6 por rodada em 9 m (área)','ataque'),
 # Luz (Sab)
 ('Luz',1,'Luz Menor','luz de tocha por 1 hora, ou cega 1 rodada com 18-20','utilidade'),
 ('Luz',2,'Cura Menor','cura 4d6','cura'),
 ('Luz',2,'Ver o Escondido','revela invisível e ilusão a 9 m por 1 cena','utilidade'),
 ('Luz',3,'Purificar','remove maldição, veneno ou doença de um','cura'),
 ('Luz',3,'Clarão','cega todos a 9 m por 1 rodada (Vontade)','defesa'),
 ('Luz',4,'Lança do Sol','16d6 de luz, dobrado contra mortos e sombra','ataque'),
 # Sombra (Von)
 ('Sombra',1,'Passo Mudo','não faz som por 1 cena','utilidade'),
 ('Sombra',2,'Manto de Sombra','invisível no escuro por 1 cena, ou até atacar','defesa'),
 ('Sombra',2,'Olho da Sombra','vê pelos olhos de uma sombra a 30 m','utilidade'),
 ('Sombra',3,'Medo','o alvo foge 1d4 rodadas (Vontade)','ataque'),
 ('Sombra',3,'Porta de Sombra','salta de uma sombra a outra a até 30 m','utilidade'),
 ('Sombra',4,'Noite Fechada','apaga toda luz em 18 m por 1 cena','defesa'),
 # Sangue (Afi) — cobra sempre (X.8)
 ('Sangue',1,'Sangue Quente','+4 contra frio, veneno e doença por 1 dia (custa 1d6 de PV)','defesa'),
 ('Sangue',2,'Fechar Ferida','para o Sangrando e cura 2d6 de outro, com o próprio sangue','cura'),
 ('Sangue',2,'Rastro de Sangue','segue quem sangrou num raio de 1 km por 1 dia','utilidade'),
 ('Sangue',3,'Frenesi','+4 de Força e −3 de Defesa por 3 rodadas','arma'),
 ('Sangue',3,'Laço de Sangue','dois que dividem sangue sabem a dor e o lugar um do outro por 1 mês','utilidade'),
 ('Sangue',4,'Corrente de Sangue','drena 16d6 e devolve metade a quem lança','ataque'),
 # Osso (Von) — cobra sempre
 ('Osso',1,'Ler o Osso','sabe como morreu quem deixou o osso','utilidade'),
 ('Osso',2,'Mão do Morto','uma mão de esqueleto obedece por 1 hora (carrega, abre, segura)','utilidade'),
 ('Osso',3,'Falar com Morto','três perguntas a um morto','utilidade'),
 ('Osso',3,'Armadura de Osso','RD +4 por 1 cena','defesa'),
 ('Osso',4,'Quebra-Ossos','16d6 e o alvo perde 1 ataque por rodada por 1 cena','ataque'),
 ('Osso',4,'Servo de Osso','ergue um esqueleto (soldado comum) por 1 dia','utilidade'),
 # Vazio (Von)
 ('Vazio',1,'Calar','um som ou uma runa de 1º círculo some','utilidade'),
 ('Vazio',2,'Bolso Vazio','guarda um objeto de até 5 kg num lugar que não existe (1 dia)','utilidade'),
 ('Vazio',3,'Desfazer','apaga um feitiço de até 3º círculo','defesa'),
 ('Vazio',3,'Peso do Nada','um alvo fica sem peso ou com peso dobrado por 3 rodadas','utilidade'),
 ('Vazio',4,'Sono do Ferro','no toque, apaga uma magia ou um encantamento por 1 cena','defesa'),
 ('Vazio',4,'Selo de Silêncio','anula magia numa área de 9 m por 1 cena','defesa'),
 # Elo (Afi)
 ('Elo',1,'Nó de Chamada','a peça volta à mão do dono a até 30 m','utilidade'),
 ('Elo',2,'Fio de Elo','prende um alvo a 9 m (Vontade CD 20)','ataque'),
 ('Elo',2,'Elo de Guarda','sabe quando o objeto ou a pessoa ligada é tocada, a até 1 km','utilidade'),
 ('Elo',3,'Corrente de Ferro','prende até 3 alvos a 9 m por 2 rodadas','ataque'),
 ('Elo',3,'Partilhar a Dor','metade do dano que um aliado levaria vem para o portador','defesa'),
 ('Elo',4,'Elo de Juramento','dois juram e o mundo cobra a quebra','utilidade'),
 # Tempo (Int)
 ('Tempo',1,'Instante','+4 na Iniciativa ou rerrola um teste de Agilidade','defesa'),
 ('Tempo',2,'Pressa','uma ação a mais nesta rodada (1x por cena)','arma'),
 ('Tempo',2,'Envelhecer','uma corda apodrece, um metal enferruja, uma comida estraga em segundos','utilidade'),
 ('Tempo',3,'Voltar um Passo','desfaz o último golpe recebido (1x por dia)','defesa'),
 ('Tempo',3,'Ler o Ontem','vê o que aconteceu num lugar há até 1 dia','utilidade'),
 ('Tempo',4,'Visão do Tempo','vê uma hora à frente (1x por dia)','utilidade'),
 # Mente (Von)
 ('Mente',1,'Sussurro','mensagem de 20 palavras a quem conhece, a 10 km','utilidade'),
 ('Mente',2,'Detectar Mentira','sabe se uma frase é mentira','utilidade'),
 ('Mente',2,'Calma','tira medo e raiva de até 4 aliados','defesa'),
 ('Mente',3,'Sono','até 3 alvos dormem (Vontade)','ataque'),
 ('Mente',3,'Ler a Superfície','ouve o que o alvo pensa agora','utilidade'),
 ('Mente',4,'Comando','o alvo obedece uma ordem de uma palavra (Vontade CD 25)','ataque'),
]
try:
    from grimorio_completo import ADD as _ADD  # grimório fechado (Dia 356): 13 escolas, 1º ao 9º
    G += _ADD
except ImportError: pass
TECNICAS_DE_AURA = [  # para guerreiros (regra da casa, Dia 200): Luta Treinado 1 · Mestre 2 · Lendário 3; 1º-2º círculo; custa Estamina = círculo; 1x por cena
 'Pele de Pedra (Pedra 2º): +4 de Defesa por 3 rodadas','Raiz de Pedra menor (Pedra): não é derrubado por 1 rodada','Passo de Vento (Vento 1º)',
 'Sangue Quente (Sangue 1º, sem custo de PV na aura)','Fôlego de Ferro (Sangue 2º): ignora Exausto por 1 cena','Mão de Pedra (Pedra 1º)',
 'Instante (Tempo 1º)','Calma (Mente 2º): tira medo dos que estão a 6 m','Luz no Escudo (Luz 1º): cega 1 rodada quem bate no escudo com 19-20','Nó de Chamada (Elo 1º): a arma volta à mão']
d=lambda n: secrets.randbelow(n)+1
if __name__=='__main__':
    a=sys.argv[1:]
    if not a or a[0]=='lista':
        esc=a[1] if len(a)>1 else None
        for e,c,n,ef,t in G:
            if not esc or e.lower()==esc.lower(): print(f'{e:6s} {c}º  {n}: {ef} [{t}]')
        if not esc: print('\nTÉCNICAS DE AURA (guerreiros):'); [print(' · '+x) for x in TECNICAS_DE_AURA]
    elif a[0]=='sorteia':
        cm=int(a[1]) if len(a)>1 else 3; esc=a[2] if len(a)>2 else None
        pool=[g for g in G if g[1]<=cm and (not esc or g[0].lower()==esc.lower())]
        e,c,n,ef,t=pool[d(len(pool))-1]; print(f'[d{len(pool)}] {e} {c}º — {n}: {ef} [{t}]')
