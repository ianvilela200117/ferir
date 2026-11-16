#!/usr/bin/env python3
"""clima.py — o TEMPO de cada cidade do reino, dia a dia, pela estação do calendário (MOTOR 6.1): clima.json.

Antes o clima era uma frase parada no estado.json ("frio, neblina no rio", escrita no inverno e ainda lá no verão).
Agora cada cidade tem céu e vento rolados por dia, pela estação (Inverno, Degelo, Sol, Colheita), com PERSISTÊNCIA:
o tempo de hoje tende a repetir o de ontem (d6: 1-3 fica; 4-6 muda, d20 na tabela da estação). O RIO tem nível:
sobe com chuva e degelo, desce com sol. Na semana, o clima pesa na COMIDA e no COMÉRCIO de cada cidade
(modificador de uma semana no reino.json, que vence sozinho).

Uso:
  python3 clima.py dia DIA        rola o dia (o tick chama sozinho)
  python3 clima.py semana DIA     o peso do clima da semana nos pilares (o tick semanal chama, antes do reino)
  python3 clima.py ver            o tempo de hoje e os últimos 7 dias
  python3 clima.py previsao       o que os barqueiros e os velhos esperam para amanhã (um palpite, não um dado)
"""
import sys
from nucleo import d, carrega, grava, calendario

ARQ = 'clima.json'
CIDADES = ['Ireviel', 'o Porto de Marasar', 'Levis', 'Farenta']
# d20 por estação: (até, céu)
CEU = {
 'Inverno':  [(4, 'limpo e gelado'), (8, 'nublado'), (11, 'neblina'), (14, 'chuva fria'), (17, 'neve'), (19, 'geada forte'), (20, 'tempestade')],
 'Degelo':   [(4, 'limpo'), (8, 'nublado'), (11, 'neblina'), (16, 'chuva'), (18, 'chuva forte'), (19, 'geada tardia'), (20, 'tempestade')],
 'Sol':      [(8, 'limpo'), (12, 'calor forte'), (15, 'nublado'), (17, 'chuva de verão'), (18, 'neblina'), (20, 'tempestade')],
 'Colheita': [(5, 'limpo'), (10, 'nublado'), (13, 'neblina'), (17, 'chuva'), (18, 'chuva forte'), (19, 'geada cedo'), (20, 'tempestade')],
}
CEU['Dias Mudos'] = CEU['Inverno']
VENTO = ['calmo', 'calmo', 'brisa', 'brisa', 'vento firme', 'vento forte']
EFEITO = {
 'neblina': 'vê-se a 30 passos: emboscada e fuga ficam fáceis, tiro longo fica difícil, barca grande anda devagar',
 'chuva': 'estrada de lama (viagem mais lenta), arco molhado, rastro some em horas',
 'chuva fria': 'estrada de lama, frio que cansa quem dorme ao relento',
 'chuva de verão': 'pancada curta: refresca, apaga rastro, enche as cisternas',
 'chuva forte': 'estrada cortada em trechos, o rio sobe, fogo ao ar livre não pega',
 'tempestade': 'BARCO NÃO SAI, estrada perigosa, telhado e andaime em risco, raio (o fogo e o Ar ficam imprevisíveis)',
 'neve': 'estrada fechada para carroça, rastro fica dias, frio que mata quem não tem abrigo',
 'geada forte': 'o rio pode prender barca rasa, ferro quebradiço ao ar livre, planta nova morre',
 'geada tardia': 'PERIGO PARA A SEMENTE: broto queimado',
 'geada cedo': 'PERIGO PARA A COLHEITA que ainda está no campo',
 'calor forte': 'cansaço dobrado em armadura e na forja grande, água vale ouro, capim seco (fogo corre)',
}
AGUA = {'chuva': 1, 'chuva fria': 1, 'chuva de verão': 1, 'chuva forte': 2, 'tempestade': 2}
NIVEL = [(15, 'SECO (barca grande encalha; vau a pé em vários pontos)'), (35, 'baixo'), (65, 'normal'), (85, 'cheio (correnteza forte: subir o rio custa o dobro)'), (101, 'CHEIA (alaga os lodaçais e a cidade baixa; barca não desce)')]
BASE = {'Inverno': 1.5, 'Degelo': 0.9, 'Sol': -0.6, 'Colheita': 0.2, 'Dias Mudos': 1.5}
RUIM_COMIDA = ('tempestade', 'geada tardia', 'geada cedo', 'geada forte', 'calor forte', 'chuva forte')


def nivel(a):
    return next(t for lim, t in NIVEL if a < lim)


def load():
    return carrega(ARQ, {'agua': 50, 'hoje': {}, 'historia': []})


def rola_dia(dia):
    C = load()
    if C['historia'] and C['historia'][-1]['dia'] >= dia:
        print(f'o clima do Dia {dia} já foi rolado.')
        return
    cal = calendario(dia)
    est = cal['estacao']
    hoje = {}
    linhas = []
    pontos = 0
    for c in CIDADES:
        ontem = C['hoje'].get(c, {}).get('ceu')
        p = d(6)
        if ontem and p <= 3 and any(ontem == x for _, x in CEU[est]):
            ceu, como = ontem, f'd6 [{p}] fica'
        else:
            r = d(20)
            ceu = next(x for lim, x in CEU[est] if r <= lim)
            como = f'd6 [{p}] muda, d20 [{r}]'
        v = d(6)
        vento = 'VENTANIA' if ceu == 'tempestade' else VENTO[v - 1]
        hoje[c] = {'ceu': ceu, 'vento': vento}
        pontos += AGUA.get(ceu, 0)
        ef = EFEITO.get(ceu, '')
        linhas.append(f"   {c}: {ceu}, {vento} ({como} · vento d6 [{v}])" + (f' → {ef}' if ef else ''))
    seca = sum(1 for c in CIDADES if hoje[c]['ceu'] == 'calor forte')
    antes = nivel(C['agua'])
    # o rio volta devagar ao normal da estação (baixo no Sol, cheio no Degelo); chuva empurra para cima, calor para baixo
    C['agua'] = max(0, min(100, round(C['agua'] + pontos * 3 + BASE.get(est, 0.5) - 0.1 * C['agua'] - seca)))
    agora = nivel(C['agua'])
    C['hoje'] = hoje
    C['historia'].append({'dia': dia, 'tempo': {c: hoje[c]['ceu'] for c in CIDADES}, 'agua': C['agua']})
    C['historia'] = C['historia'][-40:]
    grava(ARQ, C)
    e = carrega('estado.json')
    if e:
        e['tempo']['clima'] = f"{hoje['Ireviel']['ceu']}, {hoje['Ireviel']['vento']}; rio {agora.split(' (')[0]}"
        grava('estado.json', e)
    print(f"  O TEMPO ({cal['txt']})" + (f" · {cal['nota']}" if cal['nota'] else ''))
    for l in linhas:
        print(l)
    print(f"   O RIO: {agora} [{C['agua']}/100]" + (f' · MUDOU: era {antes.split(" (")[0]}' if antes != agora else ''))


def semana(dia):
    C = load()
    R = carrega('reino.json')
    if not R:
        return
    ult = [h for h in C['historia'] if dia - 7 < h['dia'] <= dia]
    est = calendario(dia)['estacao']
    print(f'  O CLIMA DA SEMANA NOS PILARES (vale até o Dia {dia + 6}):')
    mud = 0
    for c in R['cidades']:
        nome = next((x for x in CIDADES if x.split()[-1] in c['nome']), None)
        if not nome:
            continue
        dias = [h['tempo'].get(nome, '') for h in ult]
        ruins = [x for x in dias if x in RUIM_COMIDA]
        chuva_boa = [x for x in dias if x in ('chuva', 'chuva de verão')]
        mods = c.setdefault('mods', {})
        # EQUILÍBRIO (auditoria do Dia 379, 6.000 semanas simuladas por estação): calor forte sozinho só pesa a partir de 5 dias (seca);
        # geada, tempestade e chuva forte pesam a partir de 3. Assim a semana ruim fica perto de 1 em 7, e a boa também.
        duros = [x for x in ruins if x != 'calor forte']
        limpos = [x for x in dias if x in ('limpo', 'limpo e gelado')]
        if len(duros) >= 3 or len(ruins) >= 5:
            mods.setdefault('Comida', []).append([-1, f"clima: {len(ruins)} dias de {', '.join(sorted(set(ruins)))} (até o {dia + 6})"])
            print(f"   {c['nome']}: Comida −1 ({len(ruins)} dias ruins para o campo: {', '.join(sorted(set(ruins)))})"); mud += 1
        elif est == 'Colheita' and not duros and len(limpos) >= 3:
            mods.setdefault('Comida', []).append([1, f"clima: colheita em tempo seco, {len(limpos)} dias limpos (até o {dia + 6})"])
            print(f"   {c['nome']}: Comida +1 (colheita em tempo seco)"); mud += 1
        elif not duros and len(ruins) <= 2 and len(chuva_boa) >= (3 if est == 'Degelo' else 2) and est in ('Degelo', 'Sol'):
            mods.setdefault('Comida', []).append([1, f"clima: semana boa para o campo, {len(chuva_boa)} dias de chuva mansa (até o {dia + 6})"])
            print(f"   {c['nome']}: Comida +1 (chuva mansa na hora certa)"); mud += 1
        temp = sum(1 for x in dias if x == 'tempestade')
        if nome in ('Ireviel', 'o Porto de Marasar') and (C['agua'] < 15 or C['agua'] >= 85 or temp >= 2):
            porque = 'o rio seco' if C['agua'] < 15 else 'a cheia do rio' if C['agua'] >= 85 else f'{temp} dias de tempestade (barco parado)'
            mods.setdefault('Comércio', []).append([-1, f"clima: {porque} (até o {dia + 6})"])
            print(f"   {c['nome']}: Comércio −1 ({porque})"); mud += 1
    if not mud:
        print('   nada: o tempo não pesou em nenhum pilar.')
    grava('reino.json', R)


def main():
    a = sys.argv[1:]
    if a and a[0] == 'dia' and len(a) > 1:
        rola_dia(int(a[1]))
    elif a and a[0] == 'semana' and len(a) > 1:
        semana(int(a[1]))
    elif a and a[0] == 'previsao':
        C = load()
        for c, v in C['hoje'].items():
            print(f"{c}: hoje {v['ceu']}; amanhã, metade de chance de seguir igual (os velhos dizem que {'segura' if v['ceu'] in ('limpo', 'nublado') else 'vira'})")
    else:
        C = load()
        if not C['historia']:
            print('o clima ainda não foi rolado (começa no próximo tick).')
            return
        print(f"O TEMPO HOJE (Dia {C['historia'][-1]['dia']}, {calendario(C['historia'][-1]['dia'])['txt']}) · rio: {nivel(C['agua'])}")
        for c, v in C['hoje'].items():
            print(f"  {c}: {v['ceu']}, {v['vento']}")
        print('ÚLTIMOS DIAS (Ireviel · Porto · Levis · Farenta):')
        for h in C['historia'][-7:]:
            print(f"  Dia {h['dia']}: " + ' · '.join(h['tempo'].values()))


if __name__ == '__main__':
    main()
