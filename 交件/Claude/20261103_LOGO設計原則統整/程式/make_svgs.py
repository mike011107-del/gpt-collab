import os, re, sys
W=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(W,'lib'))
import build
from build import g1,g2,g3,NAVY,RED,YELLOW,WHITE,BLACK,rect
from glyphs import SONG,CHUN,glyph_svg
out=os.path.join(W,'img')
def svg(Wd,H,body,bg):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{Wd:.0f}" height="{H:.0f}" viewBox="0 0 {Wd:.0f} {H:.0f}">{rect(0,0,Wd,H,bg)}{body}</svg>'
def save(name,s): open(os.path.join(out,name),'w',encoding='utf-8').write(s)
for g,fn in [('G1',g1),('G2',g2)]:
    Wd,H,b=fn(NAVY,RED,WHITE); save(f'{g}_white.svg',svg(Wd,H,b,WHITE))
    Wd,H,b=fn(WHITE,YELLOW,NAVY); save(f'{g}_navy.svg',svg(Wd,H,b,NAVY))
Wd,H,b=g3(NAVY,WHITE,WHITE); save('G3_white.svg',svg(Wd,H,b,WHITE))
# G3 tight crop (no padding) for small-size test
C,m,gap=300,46,26; bw,bh=C+2*m,2*C+gap+2*m
save('G3_tight.svg',f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="60 60 {bw} {bh}" width="{bw}" height="{bh}">{b}</svg>')
# G1 annotated: boxes around 山 symbol and the 山 part of 崧, labels under each element
Wd,H,b=g1(NAVY,RED,WHITE)
H2=H+70
ann=''
ann+='<rect x="48" y="70" width="210" height="302" fill="none" stroke="#B3261E" stroke-width="5" stroke-dasharray="14 9"/>'
ann+='<rect x="372" y="70" width="188" height="118" fill="none" stroke="#B3261E" stroke-width="5" stroke-dasharray="14 9"/>'
for x,t in [(153,'山'),(466,'崧'),(784,'淳')]:
    ann+=f'<text x="{x}" y="{H+40}" font-family="Noto Sans TC" font-weight="700" font-size="44" fill="#B3261E" text-anchor="middle">{t}</text>'
save('G1_annot.svg',svg(Wd,H2,b+ann,WHITE))
# G1 symbol only + 'i' comparison
sym=''
w,gap,outer,middle=30,48,150,230
base=330; x=40
sym+=build.shan(x,base,w,gap,outer,middle,NAVY)
sym+=rect(x+w+gap,base-middle-18-w,w,w,RED)
sym+=f'<text x="400" y="{base}" font-family="Noto Sans TC" font-weight="700" font-size="330" fill="{NAVY}" text-anchor="middle">i</text>'
save('G1_idot.svg',svg(520,380,sym,WHITE))
# glyph-only wordmark for comparison (size 300)
gw=glyph_svg(SONG,20,20,300,colour=NAVY)+glyph_svg(CHUN,20+300+18,20,300,colour=NAVY)
save('G_glyphs.svg',svg(20+618+20,340,gw,WHITE))
print('ok')
