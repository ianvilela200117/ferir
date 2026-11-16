#!/usr/bin/env python3
"""OBRA ABERTA (regra da casa, Dia 199, pedido do jogador): sem alvo escolhido.
O teto vem da capacidade real (maestria, melhor material, oficina; Lendário+ pede Receita Mestra e condição).
Rolam-se os 4 testes (d20 + todos os bônus). A peça sai NA MELHOR categoria que os dados alcançam
(regra do motor: 4 sucessos = a categoria; 3 = uma abaixo; 2 = duas abaixo; 0-1 = perde), até o teto.
Os dados mandam no resto:
  - cada 20 natural que passou: +1 efeito; dois 20 com 4 sucessos: obra-prima (1d6: 1-3 sobe uma categoria se o teto deixar, senão efeitos)
  - três 20: obra-prima + MARCA DO MUNDO (um efeito da tabela de maravilhas)
  - quatro 20: LENDA: a peça acorda (nome próprio, maravilha, o mundo fica sabendo)
  - SOBRA: o que os 4 testes passaram da CD da categoria final (somado); se a peça bateu no teto:
      sobra 40+ = +1 efeito · 60+ = +2 · 80+ = +3 e uma maravilha
  - 1 natural: complicação (1d6: 1 a peça se perde · 2-3 cai uma categoria · 4-6 menor), depois de contar
  - todo 20 ou 1 natural rola uma PECULIARIDADE (surpresa: boa, estranha ou defeito); e 1 em 10 obras ganha uma de graça
  - os EFEITOS saem sorteados da tabela do tipo da peça (d20), sem repetir; Único+ tem 1 encaixe de magia
Uso: python3 obra_aberta.py "Nome" TIPO materia processo tecnica quarto teto=CAT [alma=N] [fortuna=N] [protegida]
     python3 obra_aberta.py recalc "Nome" TIPO t1 t2 t3 t4 teto=CAT   (refaz com totais já rolados; d20 opcional: t1:20)
TIPO: arma armadura ferramenta objeto foco
"""
import sys, secrets
CAT = ['Comum','Incomum','Raro','Epico','Unico','Lendario','Mitico','Primordial']
NOME = ['Comum','Incomum','Rara','Épica','Única','Lendária','Mítica','Primordial']
CD = [15,20,25,30,35,40,45,50]
NEF = [0,1,1,2,3,4,6,8]   # efeitos por categoria (X.2); Único+ inclui 1 encaixe de magia
d = lambda n: secrets.randbelow(n)+1
def norm(s): return s.lower().replace('é','e').replace('ú','u').replace('í','i')
KEY = [norm(c) for c in CAT]

EFEITOS = {
 'arma': ["o fio não cega nem lasca (durabilidade dobrada)","fere o que não tem corpo (espíritos, sombras)","volta à mão de quem a lança (até 9 m)",
  "1x por cena, o golpe derruba (Vigor CD 15+categoria)","sangra: o ferido perde 1d6 por rodada até ser tratado","+2 no ataque contra quem já feriu o portador nesta luta",
  "a arma avisa: vibra quando há inimigo escondido a 9 m","atravessa escudo: ignora a Defesa do escudo","1x por dia, um golpe que erraria acerta",
  "corta magia: o golpe desfaz um feitiço de 1º círculo no alvo","não pode ser tirada da mão (desarmar falha)","o golpe empurra 2 m",
  "pesa quase nada: +2 na Iniciativa","guarda o calor: +1d6 de fogo no primeiro golpe da cena","dano dobrado contra monstros de uma Essência (1d12 decide qual)",
  "brilha fraco no escuro (luz de vela) quando o portador quer","o portador não pode ser surpreendido enquanto a segura","crítico com 19 ou 20",
  "a arma bebe o golpe: cura o portador em 1d6 quando fere","o som da lâmina dá medo: quem a ouve pela primeira vez faz Vontade CD 15 ou recua"],
 'armadura': ["RD +2 contra lâminas","RD +3 contra fogo","não range: veste em silêncio, sem −2 de Furtividade","1x por cena, um crítico vira golpe normal",
  "veste e tira sozinho em meio minuto","+2 de Defesa contra projéteis","não enferruja nem apodrece (sal, chuva, lama)","esquenta o corpo: sem teste de frio até a neve funda",
  "1x por dia, devolve 1d8 a quem acertar o portador","o portador não pode ser derrubado nem empurrado","leve: sem penalidade de cansaço na marcha",
  "a armadura avisa veneno: o metal escurece perto dele","1x por cena, +4 de Defesa por 1 rodada","RD +2 contra magia (escolas de dano)",
  "o portador respira mesmo com fumaça densa","cura 1 PV por hora enquanto vestida","flutua: o portador não afunda na água",
  "+2 em Vontade contra medo","esconde: parece roupa comum a quem não tem Olho do Material","quem a veste ouve o próprio coração: nunca dorme em vigia"],
 'ferramenta': ["não cansa: o dono trabalha o dia inteiro sem cansaço","não escorrega com suor, óleo ou frio","+2 na Técnica de quem a usa",
  "o aprendiz que a usa conta prática em dobro","fala: soa diferente quando a peça tem falha (+2 na Matéria)","a obra feita com ela sai em 3/4 do tempo",
  "aguenta fogo de forja sem perder têmpera","gasta metade do material miúdo (rebite, carvão, óleo)","1x por obra, um 1 natural vira 2",
  "+2 no Processo (segura o calor certo)","pesa a metade","a ferramenta acha a veia do metal: +2 em Olho do Material e Coleta",
  "corta e molda pedra como se fosse madeira","não pode ser roubada: volta ao dono em 1 dia","marca o que faz: quem vê a peça sabe de quem é a mão",
  "trabalha no escuro como de dia","nunca precisa de reparo","acalma: quem trabalha com ela não se irrita (+2 em ensinar)",
  "+2 no Acaso das obras","o material fala com ela: +1 efeito extra numa obra por semana (1d6: 6)"],
 'objeto': ["não abre sem a chave certa: Ladinagem CD 40","quem força ganha um choque (2d6, Vontade CD 20 para não soltar)","não queima nem racha no fogo",
  "toca um sino baixo quando tocada por mão estranha","esconde o que guarda da magia de procura","pesa o dobro para quem não é dono",
  "tranca sozinha quando fechada","a fechadura troca de segredo uma vez por lua","não enferruja nem apodrece","guarda o frio ou o calor de dentro por um mês",
  "quem a abre sem direito esquece o que viu (Vontade CD 25)","aguenta golpe de aríete (RD 12 na peça)","a chave pode ser escondida em qualquer anel ou fita",
  "range alto se aberta à noite","dentro, papel e couro não estragam","duas chaves: uma abre, a outra só mostra que está tudo lá",
  "sela com cera de runa: mostra se alguém tentou","não pode ser tirada do lugar onde foi posta sem a chave","quem dorme perto dela não sonha mal",
  "esconde-se: quem não sabe que está ali não a acha (Percepção CD 30)"],
 'foco': ["+2 nos feitiços de uma escola (1d12 decide qual)","a runa gravada com ela dura o dobro","não devolve: quem lança não sofre o retorno de feitiço mal feito",
  "+2 em Magia ao gravar ou riscar","1x por dia, um feitiço de 1º círculo sem gastar Mana","duas runas no tempo de uma","o feitiço vai 3 m mais longe",
  "guarda 1 ponto de Mana por noite (até 5)","acende sozinha quando há magia hostil por perto","+2 na RM do portador",
  "quem toca sem ser dono sente frio e solta","grava em metal duro sem lascar","1x por cena, repete o último feitiço de 1º círculo",
  "o foco aprende: cada feitiço lançado 10 vezes com ele ganha +1","escreve sozinho o que o dono dita (Sussurro de papel)",
  "não pode ser apagado pelo vaduar por uma rodada","dá +1 efeito a um encantamento por semana","brilha com a cor da Essência do feitiço",
  "+2 em Afinidade para escolas de Elo e Sangue","o foco sonha: às vezes mostra ao dono uma runa que ele não conhecia (1d20 por semana: 20)"],
}
PECULIAR = ["canta baixinho quando o dono está triste","esquenta quando alguém mente perto dela","tem vontade própria: às vezes pesa quando o dono vai fazer bobagem",
 "atrai gatos","escurece com sangue e não limpa mais","o primeiro que a tocar depois do dono vai sonhar com a forja","guarda uma lembrança: quem a segura ouve o último golpe",
 "não gosta de água: chia molhada (sem dano)","marca de nascença: um desenho que ninguém gravou apareceu no metal","é pesada para crianças e leve para velhos",
 "DEFEITO: range quando o dono tem medo","DEFEITO: perde o efeito mais fraco em noite sem lua","DEFEITO: a Cobiça rola por ela como se fosse uma categoria acima",
 "aponta o norte se posta numa água parada","quem a usa por um mês fica com o cheiro da Fornalha","um animal da casa passa a segui-la",
 "SURPRESA: a peça reconhece outra peça de rei (vibra perto da Matriz, da tenaz ou do martelo do rei)","SURPRESA: algum morto da forja (a mestra?) parece ter posto a mão: +1 efeito",
 "SURPRESA: um material ficou mais nobre na têmpera: a próxima obra com ele tem +2 na Matéria","SURPRESA: a peça tem Essência própria nova (1d12 decide qual) e um efeito dela"]
MARAVILHA = ["um efeito da categoria ACIMA, mesmo passando do teto","a peça cresce com o dono: a cada 10 níveis dele, +1 efeito até a categoria acima",
 "a peça não pode ser destruída por nada abaixo de Lendário","um feitiço de 4º círculo preso, 1x por dia, sem saber magia","fala com o dono (uma frase por dia, verdadeira)",
 "dá ao portador um título enquanto a usa (+2 numa situação, à escolha dos dados)","quem a forjou ganha +1 permanente na perícia dela (a obra ensinou)","a peça escolhe o dono: rende como uma categoria acima nas mãos dele",
 "toda a cidade fica sabendo: Fama +1 (e a Cobiça de quem ouvir)","uma ESSÊNCIA rara acordou nela (Tempo, Vazio ou Sangue: 1d3): um efeito dela"]
ESC = ['Chama','Gelo','Pedra','Vento','Luz','Sombra','Sangue','Osso','Vazio','Elo','Tempo','Mente']

def ensure(txt):
    if '1d12' in txt: txt += f" [1d12 → {ESC[d(12)-1]}]"
    if '1d3' in txt and 'Tempo, Vazio' in txt: txt += f" [1d3 → {['Tempo','Vazio','Sangue'][d(3)-1]}]"
    return txt

def resolve(nomep, tipo, tests, teto, recalc=False):
    # tests: list of (die, total) ; index 3 is Acaso/Paciência (CD-10)
    best=-1; succ_best=0; cat_used=None
    for c in range(teto+1):
        s=sum(1 for i,(dd,t) in enumerate(tests) if t >= (CD[c]-10 if i==3 else CD[c]))
        res = c-(4-s) if s>=2 else -1
        if res>best or (res==best and c<(cat_used or 99)): best, succ_best, cat_used = res, s, c
    out=[]
    if best<0:
        out.append("RESULTADO: MATERIAL PERDIDO (0-1 sucesso em qualquer categoria)"); return out, None
    final=max(best,0)
    out.append(f"Melhor leitura dos dados: {succ_best} sucessos contra a CD {CD[cat_used]} ({NOME[cat_used]}) → {NOME[final]}")
    twenties=[i for i,(dd,t) in enumerate(tests) if dd==20 and t >= (CD[final]-10 if i==3 else CD[final])]
    ones=[i for i,(dd,t) in enumerate(tests) if dd==1]
    extra=len(twenties); notas=[]; marav=0; lenda=False
    if len(twenties)>=2 and succ_best==4:
        r=d(6)
        if r<=3 and final+1<=teto: final+=1; extra-=0; notas.append(f"OBRA-PRIMA 1d6 [{r}] → sobe a {NOME[final]}")
        else: extra+=1; notas.append(f"OBRA-PRIMA 1d6 [{r}] → +1 efeito (teto ou dado)")
    if len(twenties)>=3: marav+=1; notas.append("TRÊS 20: MARCA DO MUNDO (maravilha)")
    if len(twenties)>=4: lenda=True; marav+=1; notas.append("QUATRO 20: LENDA — a peça acorda (nome próprio; o mundo fica sabendo)")
    sobra=sum(t-(CD[final]-10 if i==3 else CD[final]) for i,(dd,t) in enumerate(tests) if t >= (CD[final]-10 if i==3 else CD[final]))
    if final>=teto:
        add = 3 if sobra>=80 else 2 if sobra>=60 else 1 if sobra>=40 else 0
        if add: extra+=add; notas.append(f"SOBRA {sobra} no teto → +{add} efeito(s)")
        if sobra>=80: marav+=1; notas.append("SOBRA 80+: uma maravilha")
        if not add: notas.append(f"sobra {sobra} (no teto; abaixo de 40, nada a mais)")
    else: notas.append(f"sobra {sobra} (abaixo do teto: a peça já subiu o que os dados deram)")
    for i in ones:
        r=d(6)
        if r==1: notas.append(f"1 NATURAL no teste {i+1}: complicação [1] → a peça SE PERDE"); out+=notas; out.append("RESULTADO: PERDIDA"); return out, None
        elif r<=3: final=max(final-1,0); notas.append(f"1 NATURAL no teste {i+1}: complicação [{r}] → cai a {NOME[final]}")
        else: notas.append(f"1 NATURAL no teste {i+1}: complicação [{r}] → menor (tempo dobra ou a ferramenta perde 1 de durabilidade)")
    npec = len([1 for i,(dd,t) in enumerate(tests) if dd in (1,20)]) + (1 if d(10)==1 else 0)
    out+=notas
    nef = NEF[final]; enc = 1 if final>=4 else 0
    total_ef = max(nef-enc,0)+extra
    pool=list(EFEITOS[tipo]); efs=[]
    for _ in range(min(total_ef,len(pool))):
        k=secrets.randbelow(len(pool)); efs.append(ensure(pool.pop(k)))
    out.append(f"RESULTADO: {nomep} — {NOME[final].upper()}")
    for j,e in enumerate(efs,1): out.append(f"  efeito {j} (d20 da tabela '{tipo}'): {e}")
    if enc: out.append("  + 1 ENCAIXE DE MAGIA (1º ao 3º círculo; para o Encantamento)" if final==4 else f"  + 1 ENCAIXE DE MAGIA ({'4º ao 6º' if final==5 else '7º ou 8º'} círculo)")
    pool2=list(MARAVILHA)
    for _ in range(marav): out.append(f"  MARAVILHA: {ensure(pool2.pop(secrets.randbelow(len(pool2))))}")
    pool3=list(PECULIAR)
    for _ in range(npec): out.append(f"  PECULIARIDADE: {ensure(pool3.pop(secrets.randbelow(len(pool3))))}")
    return out, final

def main():
    a=sys.argv[1:]
    if not a: sys.exit(__doc__)
    teto=next((KEY.index(norm(x[5:])) for x in a if x.startswith('teto=')), None)
    if teto is None: sys.exit('falta teto=CATEGORIA (a capacidade real: maestria, material, oficina)')
    if a[0]=='recalc':
        nomep,tipo=a[1],a[2]; tests=[]
        for x in a[3:7]:
            if ':' in x: t,dd=x.split(':'); tests.append((int(dd),int(t)))
            else: tests.append((0,int(x)))
        print(f'RECÁLCULO "{nomep}" ({tipo}) | teto {NOME[teto]} | totais {[t for _,t in tests]}')
        out,_=resolve(nomep,tipo,tests,teto,True); print('\n'.join('  '+o for o in out)); return
    nomep,tipo=a[0],a[1]; b=[int(x) for x in a[2:6]]
    alma=next((int(x[5:]) for x in a if x.startswith('alma=')),0)
    fort=next((int(x[8:]) for x in a if x.startswith('fortuna=')),0)
    rol=[[d(20),b[i]] for i in range(4)]
    print(f'OBRA ABERTA "{nomep}" ({tipo}) | teto {NOME[teto]} (CD {CD[teto]}) | bônus {b}')
    for i,nm in enumerate(['Matéria','Processo','Técnica','Acaso/Paciência']):
        print(f'  {nm}: [{rol[i][0]}] + {b[i]} = {rol[i][0]+b[i]}')
    # rerrolagens: a que mais limita (menor margem contra a CD do teto); Alma Ouvida primeiro (grátis), depois Fortuna (+1 Revés)
    def cur():
        tests=[(r[0],r[0]+r[1]) for r in rol]
        best=-1
        for c in range(teto+1):
            s=sum(1 for i,(dd,t) in enumerate(tests) if t >= (CD[c]-10 if i==3 else CD[c]))
            best=max(best, c-(4-s) if s>=2 else -1)
        return best
    reves=0
    for tipo_r,n in (('ALMA OUVIDA (sem Revés)',alma),('Fortuna (+1 Revés)',fort)):
        for _ in range(n):
            base=cur()
            if base>=teto and all(r[0]!=1 for r in rol): break
            # pior teste relativo ao teto
            i=min(range(4), key=lambda k:(rol[k][0]!=1, rol[k][0]+rol[k][1]-(CD[teto]-10 if k==3 else CD[teto])))
            old=rol[i][0]; new=d(20); rol[i][0]=new
            print(f'  {tipo_r}: teste {i+1} [{old}] → rerrola [{new}] = {new+rol[i][1]}')
            if 'Fortuna' in tipo_r: reves+=1
    if reves: print(f'  Revés +{reves}')
    tests=[(r[0],r[0]+r[1]) for r in rol]
    out,_=resolve(nomep,tipo,tests,teto); print('\n'.join('  '+o for o in out))
if __name__=='__main__': main()
