"""每組合成一張 1080 寬直圖：側面車、車隊現場、文件示意；另出縮圖。"""
from PIL import Image
O='/tmp/claude-0/-home-claude/f822ab78-49b8-5e2f-8fbe-8111b065c404/scratchpad/r19/out20'
P='/tmp/claude-0/-home-claude/f822ab78-49b8-5e2f-8fbe-8111b065c404/scratchpad/r19/page20'
W=1080
def fit(im): return im.resize((W,round(im.size[1]*W/im.size[0])),Image.LANCZOS)
for k in ['d1a','d1b','d2a','d2b','d3a','d3b','d4a','d4b']:
    a=fit(Image.open(f'{O}/{k}_side.jpg')); b=fit(Image.open(f'{O}/{k}_fleet.jpg')); c=fit(Image.open(f'{O}/{k}_docs.png').convert('RGB'))
    g=8; H=a.size[1]+b.size[1]+c.size[1]+2*g
    im=Image.new('RGB',(W,H),'#FFFFFF'); y=0
    for x in (a,b,c): im.paste(x,(0,y)); y+=x.size[1]+g
    im.save(f'{P}/{k}.jpg',quality=82,optimize=True,progressive=True)
    t=Image.open(f'{O}/{k}_side.jpg').crop((40,40,1100,440)); t=t.resize((540,round(t.size[1]*540/t.size[0])),Image.LANCZOS)
    t.save(f'{P}/{k}_t.jpg',quality=80,optimize=True)
    print(k,im.size,t.size)
