#!/usr/bin/env python3
"""Monta o LIVRO DO MUNDO (uma página HTML com abas, busca e o mapa do continente) a partir dos .md do compendio."""
import markdown, json, re, html, os
D = os.path.dirname(os.path.abspath(__file__))
ABAS = [('mapa','Mapa',None),('mundo','O Mundo','01_mundo.md'),('classes','Classes','04_classes.md'),
        ('grimorio','Grimório','03_grimorio.md'),('talentos','Talentos','05_talentos.md'),
        ('materiais','Essências e Materiais','06_essencias_materiais.md'),('bestiario','Bestiário','07_bestiario.md'),
        ('nove','Livro Nove','08_livro_nove.md')]
md = markdown.Markdown(extensions=['tables','toc','sane_lists'])
corpo = {}
def prep(t):
    """GFM -> Python-Markdown: linha em branco antes de lista e tabela; sublistas com 4 espaços."""
    out=[]; prev=''
    for l in t.split('\n'):
        m=re.match(r'^( *)([-*] |\d+\. )',l)
        if m:
            n=len(m.group(1)); l=' '*(n*2)+l[n:]
            if prev.strip() and not re.match(r'^ *([-*] |\d+\. )',prev): out.append('')
        elif l.startswith('|') and prev.strip() and not prev.startswith('|'): out.append('')
        out.append(l); prev=l
    return '\n'.join(out)
for k,_,f in ABAS:
    if f:
        md.reset(); corpo[k] = md.convert(prep(open(os.path.join(D,f)).read()))

# ---------- o mapa ----------
REG = [  # nome, cor, x, y, rx, ry, info
 ('Reino de Ireviel','casa',588,585,48,128,['O rei Ferir e o conselho real. Capital Ireviel (~14.000).','Levis (Brara), o Porto de Marasar, a Forquilha e Farenta (tomada no 356).']),
 ('Marasar','skotha',665,738,34,22,['A Doge Skotha Graskur (Lendária). Aliada +5.','O cais é de Ireviel.']),
 ('O Delta e o Brejo','delta',480,730,70,32,['Ninguém manda sozinho: os Do Junco, a Guilda do Sal, a Altheltia, a Lurentetta.','No brejo: Ninnane e Dragal (canção de coveiro).']),
 ('As Montanhas Hegre','cla',560,295,100,48,['O Clã Hegre (o Hrotgar). Gogrunn, as Fundas, Vrogur, Ululge, Braron.','O Kredun toma terra do Clã. Relação +1.']),
 ('Steunn','livre',705,330,42,34,['Cidade livre de pedra, os mestres do bronze. O Borecci (Mítico).','Relação +2.']),
 ('Kremir e Zisrir','neutro',350,380,80,58,['Clãs das colinas e o vale de ruínas. O Maneus; o Adurel; os Sem-Torre.']),
 ('Telosus e o Oeste','fe',265,535,72,52,['O Colégio (Ceduion) e a fé da Mamiltia (Primordial).','Zieth (a Vigília), Zaivil, Kasron.']),
 ('O Deserto de Sal','neutro',830,545,105,72,['Yaelane (Clã Eloulane, o veio-mãe), Shizess (as caravanas), Mordun, Brathen.','O Thargos (Mítico), o Fenron.']),
 ('As Montanhas de Fogo','perigo',945,420,40,90,['Pedra preta e vapor. Uma só passagem: o Passo da Cinza.','O Ithvil (Mítico) dorme fundo.']),
 ('O Sul da Areia','neutro',905,745,85,40,['As tribos da areia. Syzh, o oásis; Ulek, o templo caído.','A Guardiã da Tenaz (Lendária).']),
 ('O Norte','liga',620,160,140,60,['A coroa da Leliel (Lendária), fugida de Farenta. Corte em Eiest.','EM GUERRA com o reino.']),
 ('Kasra, a Marca dos Fortes','kasra',150,230,95,75,['Os fortes do reino de cavaleiros caído há 200 anos. Os mortos de guarda.','A Ordem do Sino, em Dreska.']),
 ('Zaitor, as Estepes','zaitor',905,160,120,70,['Os khanatos dos cavaleiros e o Khan. Stind, o acampamento; Geunn, a travessia.','Vendem cavalos ao Norte.']),
 ('Qulosus, a Costa do Cobre','qulosus',140,665,85,60,['A República dos Bancos (doze banqueiros). Roreetta e Ginirza.','Cobre e estanho; a dívida é lei.']),
 ('Quramnar, o Reino do Leste','quramnar',1070,480,70,140,['O Trono de Quramnar, a rainha e as Nove Casas. Iriavis (~60.000), Boninda, Serrarva.','O culto da Agulha (o Tecelão).']),
 ('Ulra, as Ilhas do Sul','ulra',720,862,95,30,['As Capitanias e o Conselho das Velas. Ragra, o porto franco; Naane; Yaniel.']),
]
CID = [  # nome, x, y, tamanho (3 capital grande, 2 cidade, 1 lugar), cor
 ('Ireviel',590,690,3,'casa'),('a Forquilha',586,662,1,'casa'),('Levis',575,470,2,'casa'),('Farenta',760,712,2,'casa'),
 ('Marasar',662,740,2,'skotha'),('Salinas Velhas',505,748,1,'delta'),('Ninnane',462,705,1,'delta'),('Dragal?',440,725,1,'perigo'),
 ('Brassa',548,720,1,'perigo'),('Hassa',612,784,1,'perigo'),('Haol',690,768,1,'perigo'),('Costa Quebrada',430,770,1,'perigo'),
 ('Lumgal',515,470,1,'neutro'),('Lumade',465,482,1,'neutro'),('Mata de Elais',520,585,1,'neutro'),('Ulnar',580,430,1,'neutro'),
 ('Gogrunn',535,320,2,'cla'),('as Fundas',605,300,2,'cla'),('Vrogur',585,262,1,'cla'),('Braron',650,300,1,'perigo'),
 ('Steunn',705,330,2,'livre'),('Kremir',385,420,2,'neutro'),('Zisrir',315,335,1,'neutro'),('Telosus',250,520,2,'fe'),
 ('Zieth',300,565,1,'fe'),('Zaivil',360,560,1,'perigo'),('Kasron?',430,590,1,'perigo'),
 ('Shizess',770,520,2,'neutro'),('Yaelane',865,585,2,'neutro'),('Mordun',830,470,1,'perigo'),('Brathen',735,600,1,'perigo'),
 ('Syzh',905,760,1,'neutro'),('Ulek',965,725,1,'perigo'),('Eiest',620,160,2,'liga'),('Dreska',140,230,2,'kasra'),('Ralgir',205,300,1,'perigo'),
 ('Stind',905,140,2,'zaitor'),('Geunn',820,195,1,'zaitor'),('Roreetta',115,690,2,'qulosus'),('Ginirza',185,620,1,'qulosus'),
 ('Iriavis',1060,470,3,'quramnar'),('Boninda',1100,570,2,'quramnar'),('Serrarva',1010,375,1,'quramnar'),
 ('Ragra',720,855,2,'ulra'),('Naane',640,872,1,'ulra'),('Yaniel',800,878,1,'ulra'),
]
GRANDES = [  # nome, tier, x, y, cor
 ('MAMILTIA','Primordial',265,500,'fe'),('CELOCUS','Mítico',470,500,'neutro'),('LURENTETTA','Mítica',490,760,'delta'),('BORECCI','Mítico',725,345,'livre'),
 ('Skotha','Lendária',680,725,'skotha'),('Teraseth','Lendário',600,640,'casa'),('Leliel','Lendária',650,170,'liga'),('Altheltia','Lendária',475,745,'delta'),
 ('Adurel','Lendário',330,320,'neutro'),('Ceduion','Lendário',235,540,'fe'),('Eiandald','Lendário',880,595,'neutro'),('Garkunn','Lendário',845,460,'perigo'),
 ('Guardiã da Tenaz','Lendária',930,770,'neutro'),('Qunemneth','Lendário',648,752,'skotha'),('Almision','Lendária',420,640,'neutro'),
]
FERAS = [ ('Mãe Branca (Primordial, dorme)',600,235),('Kredun (Mítico)',640,280),('Elaeva (Mítico)',390,470),('Thargos (Mítico)',815,455),
 ('Ithvil (Mítico)',955,400),('Maneus',370,400),('Vathexa',725,315),('Varogh',540,600),('Kervos',570,520),('Eloune',555,760),('Husgarn',800,740),('Laennor',505,765)]
CORES = {'casa':'#b3412e','skotha':'#c9772b','liga':'#7a4e9c','cla':'#3f7a4a','livre':'#2e6f8f','delta':'#4f8a7b','fe':'#a8861c',
         'neutro':'#8a7a5e','perigo':'#2b2b2b','kasra':'#56616e','zaitor':'#8c5a2b','qulosus':'#b8683a','quramnar':'#8e2f5e','ulra':'#2f8a8a'}
NOMES = {'casa':'Reino de Ireviel','skotha':'A Doge Skotha','liga':'A Leliel (em guerra)','cla':'O Clã Hegre','livre':'Cidade livre','delta':'O Delta',
         'fe':'Telosus e a fé','neutro':'Sem dono / neutro','perigo':'Perigo ou ruína','kasra':'Kasra','zaitor':'Zaitor','qulosus':'Qulosus','quramnar':'Quramnar','ulra':'Ulra'}
DADOS = json.dumps(dict(REG=REG,CID=CID,GRANDES=GRANDES,FERAS=FERAS,C=CORES,N=NOMES),ensure_ascii=False)

MAPA = """
<div class="mapwrap">
 <div class="mapbox">
  <svg id="mapa" viewBox="0 0 1200 920" role="img" aria-label="Mapa de Ortheia">
   <defs>
    <pattern id="areia" width="8" height="8" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="#c9b27e"/><circle cx="6" cy="6" r=".8" fill="#c9b27e"/></pattern>
    <pattern id="mata" width="14" height="14" patternUnits="userSpaceOnUse"><circle cx="7" cy="7" r="3" fill="#6f8f5a" fill-opacity=".35"/></pattern>
    <filter id="sombra" x="-5%" y="-5%" width="110%" height="110%"><feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity=".18"/></filter>
   </defs>
   <rect width="1200" height="920" fill="#cfe0e3"/>
   <path id="costa" filter="url(#sombra)" fill="#efe3c6" stroke="#8a7350" stroke-width="2" d="M70,140 L160,90 L300,70 L450,60 L600,70 L760,60 L900,70 L1020,110 L1100,190 L1140,300 L1150,420 L1140,540 L1110,620 L1050,660 L985,700 L980,760 L930,792 L850,792 L780,772 L720,760 L680,756 L640,772 L600,770 L560,762 L520,772 L470,778 L420,768 L360,772 L280,762 L200,742 L130,722 L80,682 L50,600 L40,500 L45,380 L40,260 Z"/>
   <g fill="#efe3c6" stroke="#8a7350" stroke-width="1.5"><ellipse cx="720" cy="852" rx="34" ry="14"/><ellipse cx="640" cy="872" rx="20" ry="9"/><ellipse cx="800" cy="878" rx="24" ry="10"/><ellipse cx="612" cy="786" rx="9" ry="5"/></g>
   <ellipse cx="830" cy="545" rx="110" ry="74" fill="url(#areia)"/><ellipse cx="905" cy="745" rx="85" ry="38" fill="url(#areia)"/>
   <ellipse cx="520" cy="585" rx="55" ry="38" fill="url(#mata)"/><ellipse cx="1070" cy="540" rx="55" ry="70" fill="url(#mata)"/><ellipse cx="620" cy="165" rx="130" ry="45" fill="url(#mata)"/>
   <g id="regioes"></g>
   <g id="montes" fill="#8a7350" fill-opacity=".55"></g>
   <g fill="none" stroke="#4f86a6" stroke-width="3" stroke-linecap="round">
    <path d="M592,250 C585,330 568,400 575,470 S592,600 586,662"/><path d="M586,662 Q560,702 515,745"/><path d="M586,662 Q622,702 662,742"/>
    <path d="M1030,330 C1050,400 1070,470 1100,570" stroke-width="2.4"/><path d="M880,110 C860,150 840,180 820,195" stroke-width="2"/>
   </g>
   <g id="rotas" fill="none" stroke="#7a5c3a" stroke-width="1.6" stroke-dasharray="5 5"></g>
   <g id="mares" fill="#4f7487" font-style="italic" font-size="17" text-anchor="middle">
    <text x="420" y="880">o mar do Sul</text><text x="1170" y="760" transform="rotate(-90 1170 760)">o mar do Leste</text><text x="75" y="800">o mar do Oeste</text>
   </g>
   <g id="cidades"></g><g id="grandes"></g><g id="feras"></g>
   <g transform="translate(40,880)"><rect width="125" height="5" fill="#3b2f22"/><rect width="62" height="5" fill="#efe3c6" stroke="#3b2f22"/><text y="-6" font-size="12" fill="#3b2f22">~5 dias de estrada</text></g>
  </svg>
 </div>
 <aside class="painel" id="painel">
  <h3>Ortheia</h3>
  <p>Toque numa região ou numa cidade. As distâncias de verdade estão na tabela d'<a href="#mundo">O Mundo</a> (o mapa não está em escala exata nas montanhas).</p>
  <div class="camadas">
   <label><input type="checkbox" data-c="regioes" checked> regiões</label>
   <label><input type="checkbox" data-c="cidades" checked> cidades</label>
   <label><input type="checkbox" data-c="rotas" checked> estradas e rotas</label>
   <label><input type="checkbox" data-c="grandes"> os grandes</label>
   <label><input type="checkbox" data-c="feras"> monstros grandes</label>
  </div>
  <div id="legenda"></div>
 </aside>
</div>
"""

JS = r"""
const DATA=__DADOS__;
const NS='http://www.w3.org/2000/svg';
function el(t,a,txt){const e=document.createElementNS(NS,t);for(const k in a)e.setAttribute(k,a[k]);if(txt!==undefined)e.textContent=txt;return e;}
const painel=document.getElementById('painel');
const base=painel.innerHTML;
function mostra(titulo,cor,linhas){
  painel.innerHTML='<h3 style="border-left:6px solid '+cor+';padding-left:8px">'+titulo+'</h3>'+linhas.map(l=>'<p>'+l+'</p>').join('')+'<p><a href="#" id="voltar">voltar à legenda</a></p>';
  document.getElementById('voltar').onclick=(ev)=>{ev.preventDefault();painel.innerHTML=base;liga();};
}
const gr=document.getElementById('regioes');
DATA.REG.forEach(([n,c,x,y,rx,ry,info])=>{
  const g=el('g',{class:'reg',tabindex:0});
  g.appendChild(el('ellipse',{cx:x,cy:y,rx:rx,ry:ry,fill:DATA.C[c],'fill-opacity':.16,stroke:DATA.C[c],'stroke-width':1.6,'stroke-dasharray':c==='casa'?'':'4 3'}));
  if(rx>=45) g.appendChild(el('text',{x:x,y:y-ry-5,'text-anchor':'middle',class:'rlab',fill:DATA.C[c]},n.toUpperCase()));
  g.onclick=()=>mostra(n,DATA.C[c],info); g.onkeydown=(e)=>{if(e.key==='Enter')mostra(n,DATA.C[c],info)};
  gr.appendChild(g);
});
const gm=document.getElementById('montes');
function serra(x0,y0,x1,y1,n,h){for(let i=0;i<n;i++){const t=n>1?i/(n-1):0;const x=x0+(x1-x0)*t,y=y0+(y1-y0)*t;gm.appendChild(el('path',{d:`M${x-h*0.7},${y+h*0.5} L${x},${y-h*0.6} L${x+h*0.7},${y+h*0.5} Z`}));}}
serra(470,300,690,285,12,16);serra(560,245,640,240,4,20);serra(925,345,960,500,9,18);serra(90,190,240,260,7,12);serra(150,610,90,650,4,12);serra(1010,330,1040,400,4,13);serra(300,330,380,360,4,10);
const gro=document.getElementById('rotas');
[[575,470,770,520,865,585],[590,690,500,640,300,565,250,520],[250,520,205,300,140,230],[250,520,185,620,115,690],[575,470,585,262,620,160],[620,160,820,195,905,140],[770,520,930,440,1060,470],[575,470,705,330],[590,690,760,712,905,760]].forEach(p=>{
  let d='M'+p[0]+','+p[1];for(let i=2;i<p.length;i+=2)d+=' L'+p[i]+','+p[i+1];gro.appendChild(el('path',{d:d}));});
[[662,742,720,852],[662,742,900,800,1050,700,1100,570],[515,745,300,790,115,690]].forEach(p=>{let d='M'+p[0]+','+p[1];for(let i=2;i<p.length;i+=2)d+=' L'+p[i]+','+p[i+1];gro.appendChild(el('path',{d:d,stroke:'#3c6f86','stroke-dasharray':'2 6','stroke-width':2}));});
const gc=document.getElementById('cidades');
DATA.CID.forEach(([n,x,y,s,c])=>{
  const g=el('g',{class:'cid'});const r=s===3?7:s===2?5:3;
  g.appendChild(el('circle',{cx:x,cy:y,r:r,fill:s>1?DATA.C[c]:'#fff',stroke:DATA.C[c],'stroke-width':s>1?1.4:2}));
  g.appendChild(el('text',{x:x+r+3,y:y+4,class:s>1?'clab':'clab peq'},n));
  g.onclick=(e)=>{e.stopPropagation();const reg=DATA.REG.find(R=>Math.hypot((x-R[2])/R[4],(y-R[3])/R[5])<=1.05);mostra(n,DATA.C[c],[(reg?'Região: '+reg[0]+'. ':'')+DATA.N[c]+'.','Leia a ficha da região em <a href="#mundo">O Mundo</a>.'])};
  gc.appendChild(g);
});
function estrela(cx,cy,R){const r=R*0.45;let d='';for(let k=0;k<10;k++){const a=-Math.PI/2+k*Math.PI/5;const rr=k%2?r:R;d+=(k?'L':'M')+(cx+rr*Math.cos(a)).toFixed(1)+' '+(cy+rr*Math.sin(a)).toFixed(1);}return d+'Z';}
const gg=document.getElementById('grandes');
DATA.GRANDES.forEach(([n,t,x,y,c])=>{const R=t==='Primordial'?12:t.startsWith('Mític')?9:6;const g=el('g',{});
  g.appendChild(el('path',{d:estrela(x,y,R),fill:DATA.C[c],stroke:'#fff','stroke-width':1}));g.appendChild(el('text',{x:x+R+2,y:y+4,class:'glab'},n+' · '+t));gg.appendChild(g);});
const gf=document.getElementById('feras');
DATA.FERAS.forEach(([n,x,y])=>{const g=el('g',{});g.appendChild(el('path',{d:`M${x},${y-7} L${x+6},${y+5} L${x-6},${y+5} Z`,fill:'#2b2b2b'}));g.appendChild(el('text',{x:x+8,y:y+4,class:'flab'},n));gf.appendChild(g);});
function liga(){
  painel.querySelectorAll('input[data-c]').forEach(i=>{i.checked=document.getElementById(i.dataset.c).style.display!=='none';i.onchange=()=>{document.getElementById(i.dataset.c).style.display=i.checked?'':'none';};});
  const L=document.getElementById('legenda');L.innerHTML='';Object.keys(DATA.N).forEach(k=>{L.insertAdjacentHTML('beforeend','<div class="leg"><span style="background:'+DATA.C[k]+'"></span>'+DATA.N[k]+'</div>')});
}
document.getElementById('grandes').style.display='none';document.getElementById('feras').style.display='none';liga();

// ---------- abas e busca ----------
const abas=[...document.querySelectorAll('nav button')];
function abre(id){if(!document.getElementById('aba-'+id))id='mapa';abas.forEach(b=>b.classList.toggle('on',b.dataset.a===id));document.querySelectorAll('section.aba').forEach(s=>s.hidden=s.id!=='aba-'+id);filtra();}
abas.forEach(b=>b.onclick=()=>{location.hash=b.dataset.a;});
window.addEventListener('hashchange',()=>abre(location.hash.slice(1)));
const q=document.getElementById('q');
function norm(s){return s.normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase();}
function filtra(){
  const t=norm(q.value.trim());
  document.querySelectorAll('section.aba').forEach(sec=>{
    let n=0;
    sec.querySelectorAll('.texto tr, .texto p').forEach(e=>{
      if(e.closest('thead')||e.closest('li'))return;
      const hit=!t||norm(e.textContent).includes(t); e.style.display=hit?'':'none'; if(t&&hit)n++;
    });
    const lis=[...sec.querySelectorAll('.texto li')];
    lis.forEach(li=>{const hit=!t||norm(li.textContent).includes(t); li.style.display=hit?'':'none'; if(t&&hit&&!li.querySelector('li'))n++;});
    if(t) lis.forEach(li=>{ if(!li.querySelector('ul,ol'))return; const c=li.cloneNode(true); c.querySelectorAll('ul,ol').forEach(u=>u.remove());
      if(norm(c.textContent).includes(t)) li.querySelectorAll('li').forEach(x=>x.style.display=''); });
    const tx=sec.querySelector('.texto'); if(tx){ const kids=[...tx.children];
      if(!t){ kids.forEach(k=>k.style.display=''); }
      else {
        kids.forEach(k=>{ if(k.tagName==='TABLE'){k.style.display=[...k.querySelectorAll('tbody tr')].some(r=>r.style.display!=='none')?'':'none';}
          else if(k.tagName==='UL'||k.tagName==='OL'){k.style.display=[...k.children].some(li=>li.style.display!=='none')?'':'none';}
          else if(k.tagName==='HR'){k.style.display='none';} });
        const H=/^H[1-6]$/;
        kids.forEach((h,i)=>{ if(!H.test(h.tagName))return; const lv=+h.tagName[1]; let vis=false;
          for(let j=i+1;j<kids.length;j++){const k=kids[j]; if(H.test(k.tagName)){ if(+k.tagName[1]<=lv)break; else continue;} if(k.style.display!=='none'){vis=true;break;}}
          h.style.display=vis?'':'none'; });
      } }
    const b=document.querySelector('nav button[data-a="'+sec.id.slice(4)+'"] .n'); if(b) b.textContent=(t&&tx)?(' '+n):'';
  });
}
q.addEventListener('input',filtra);
document.getElementById('limpa').onclick=()=>{q.value='';filtra();q.focus();};
abre(location.hash.slice(1)||'mapa');
"""

CSS = """
:root{--p:#3b2f22;--m:#7a6a55;--bg:#f7f1e3;--card:#fffaf0;--b:#dccfb4;--a:#9c3a2a}
*{box-sizing:border-box}html,body{margin:0}body{background:var(--bg);color:var(--p);font:16px/1.55 'EB Garamond',Georgia,serif}
header{position:sticky;top:0;z-index:5;background:#efe3c6;border-bottom:1px solid var(--b);padding:10px 16px 0}
h1{font:600 26px/1.1 'Cinzel','EB Garamond',serif;margin:0 0 4px;letter-spacing:.04em}
.sub{color:var(--m);font-size:14px;margin:0 0 8px}
.busca{display:flex;gap:6px;margin-bottom:8px;max-width:560px}
.busca input{flex:1;padding:7px 10px;border:1px solid var(--b);border-radius:8px;background:#fffdf7;font:inherit;font-size:15px}
.busca button{border:1px solid var(--b);background:#fffdf7;border-radius:8px;padding:0 10px;cursor:pointer;font:inherit}
nav{display:flex;gap:2px;overflow-x:auto;scrollbar-width:thin}
nav button{border:1px solid var(--b);border-bottom:none;background:#e6d8b8;color:var(--p);padding:7px 12px;border-radius:8px 8px 0 0;font:600 14px 'EB Garamond',serif;cursor:pointer;white-space:nowrap}
nav button.on{background:var(--bg)}nav .n{color:var(--a)}
main{padding:16px;max-width:1180px;margin:0 auto}
.texto h1{font:600 28px 'Cinzel',serif;margin:6px 0 10px}.texto h2{font:600 21px 'Cinzel',serif;margin:28px 0 8px;border-bottom:1px solid var(--b);padding-bottom:4px}
.texto h3{font-size:19px;margin:22px 0 6px}.texto h4{font-size:17px;margin:18px 0 4px;color:var(--a)}
.texto table{border-collapse:collapse;width:100%;margin:8px 0 16px;background:var(--card);font-size:14.5px;display:block;overflow-x:auto}
.texto th,.texto td{border:1px solid var(--b);padding:5px 8px;vertical-align:top;text-align:left}.texto th{background:#efe3c6}
.texto ul{padding-left:22px}.texto li{margin:2px 0}.texto hr{border:none;border-top:1px dashed var(--b);margin:24px 0}
.texto a{color:var(--a)}
.mapwrap{display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:14px}
@media (max-width:860px){.mapwrap{grid-template-columns:1fr}}
.mapbox{background:var(--card);border:1px solid var(--b);border-radius:12px;overflow:hidden}
#mapa{width:100%;height:auto;display:block}
.painel{background:var(--card);border:1px solid var(--b);border-radius:12px;padding:12px 14px;font-size:15px;align-self:start}
.painel h3{margin:2px 0 8px;font:600 18px 'Cinzel',serif}.painel p{margin:6px 0}
.camadas{display:grid;gap:3px;margin:10px 0;font-size:14px}.leg{display:flex;align-items:center;gap:6px;font-size:13px;margin:2px 0}
.leg span{width:14px;height:14px;border-radius:3px;display:inline-block;opacity:.85}
.reg{cursor:pointer}.reg:hover ellipse,.reg:focus ellipse{fill-opacity:.3}
.rlab{font:700 12px 'Cinzel',serif;letter-spacing:.06em;paint-order:stroke;stroke:#efe3c6;stroke-width:3px}
.cid{cursor:pointer}.clab{font:600 12.5px 'EB Garamond',serif;fill:#2e241a;paint-order:stroke;stroke:#efe3c6;stroke-width:3px}.clab.peq{font-weight:400;font-size:11px}
.glab{font:700 11px 'EB Garamond',serif;fill:#3b2f22;paint-order:stroke;stroke:#fff;stroke-width:3px}.flab{font:italic 11px 'EB Garamond',serif;fill:#111;paint-order:stroke;stroke:#efe3c6;stroke-width:3px}
"""

secs = []
for k,t,f in ABAS:
    inner = MAPA if k=='mapa' else '<div class="texto">'+corpo[k]+'</div>'
    secs.append(f'<section class="aba" id="aba-{k}" hidden>{inner}</section>')
navs = ''.join(f'<button data-a="{k}">{t}<span class="n"></span></button>' for k,t,_ in ABAS)
page = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Livro do Mundo — Ortheia</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=EB+Garamond:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
<header><h1>Livro do Mundo · Ortheia</h1><p class="sub">O mundo e as regras fechados (Dia 356). O Mestre consulta este livro e não inventa fora dele.</p>
<div class="busca"><input id="q" type="search" placeholder="Buscar (feitiço, classe, lugar, material, fera...)" aria-label="Buscar"><button id="limpa" type="button">limpar</button></div>
<nav>{navs}</nav></header>
<main>{''.join(secs)}</main>
<script>{JS.replace('__DADOS__',DADOS)}</script></body></html>"""
open(os.path.join(D,'..','livro_do_mundo.html'),'w').write(page)
print('ok', len(page))
