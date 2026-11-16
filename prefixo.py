import re,sys,glob
txt=''
for f in ['npcs.json','mundo_vivo.json','canone.md','estado_vivo.md','mundo.json','reino.json']+glob.glob('envelope_sessao2m.md'):
    txt+=open(f).read()
pal=set(w for w in re.findall(r"\b[A-ZÁÉÍÓÚ][a-záéíóúãõâêôç]{3,}\b",txt))
pal|=set(w.capitalize() for w in re.findall(r"\b[A-ZÁÉÍÓÚ]{4,}\b",txt))
for n in sys.argv[1:]:
    p=n[:3].lower()
    hits=sorted(w for w in pal if w.lower().startswith(p) and w.lower()!=n.lower())
    print(n, '→', hits[:8] if hits else 'LIVRE')
