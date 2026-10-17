import sys, numpy as np
sys.path.insert(0,'/tmp/claude-0/work')
from scielab import *
from PIL import Image, ImageDraw, ImageFont
def hx(h): h=h.lstrip('#'); return np.array([int(h[i:i+2],16) for i in (0,2,4)],float)
BGS=[('深青 #0C424A','#0C424A'),('靛藍 #333D66','#333D66'),('石油青 #009999（Siemens）','#009999'),('中藍 #2071B5（Vattenfall）','#2071B5')]
AMB='#D68702'
# 測試圖：背景上 3 條工程黃線＋1 條白線，線寬 8px，間距 8px
H,W=96,160
def make(bg):
    a=np.tile(hx(bg),(H,W,1))
    for i,x0 in enumerate([24,48,72]):
        a[16:80,x0:x0+8]=hx(AMB)
    a[16:80,112:120]=255
    return a
# spd：每度幾個像素。線寬 8px → 0.5°、0.1°、0.04°
SCALES=[(16,'0.5°'),(80,'0.1°'),(200,'0.04°')]
import json; stats={}
tiles=[]
for name,bg in BGS:
    row=[make(bg).astype(np.uint8)]
    st={}
    for spd,lab in SCALES:
        img,xyz=scielab_render(make(bg),spd); row.append(img)
        # 線中央與背景的亮度比（S-CIELAB 濾波後）
        Yl=xyz[48,52,1]; Yb=xyz[48,8,1]; Yw=xyz[48,116,1]
        st[lab]=dict(黃線對背景亮度比=round((max(Yl,Yb)+0.05)/(min(Yl,Yb)+0.05),2), 白線對背景=round((max(Yw,Yb)+0.05)/(min(Yw,Yb)+0.05),2), 黃線看起來=('#%02X%02X%02X'%tuple(img[48,52])))
    stats[name]=st; tiles.append((name,row))
json.dump(stats,open('/tmp/claude-0/work/distance_stats.json','w'),ensure_ascii=False,indent=1)
print(json.dumps(stats,ensure_ascii=False,indent=1))
# 版面
FONT='/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
import os
if not os.path.exists(FONT):
    import glob; c=glob.glob('/usr/share/fonts/**/*CJK*',recursive=True)+glob.glob('/usr/share/fonts/**/*Noto*Sans*TC*',recursive=True); FONT=c[0] if c else None
print('font',FONT)
S=2; tw,th=W*S,H*S; pad=24; left=300; top=110
canvas=Image.new('RGB',(left+4*(tw+pad)+pad, top+len(tiles)*(th+pad)+60),(255,255,255))
d=ImageDraw.Draw(canvas)
f=ImageFont.truetype(FONT,22) if FONT else None; fs=ImageFont.truetype(FONT,17) if FONT else None
d.text((pad,20),'同一條工程黃線，越遠越看不出顏色：只剩明暗差撐得住（S-CIELAB 模擬）',fill=(20,20,20),font=f)
heads=['原圖（近看）','線寬 0.5°','線寬 0.1°','線寬 0.04°']
subs=['','約 1 cm 線在 1.1 m','約 1 cm 線在 5.7 m','約 1 cm 線在 14 m']
for j,hd in enumerate(heads):
    x=left+j*(tw+pad); d.text((x,58),hd,fill=(20,20,20),font=fs); d.text((x,80),subs[j],fill=(110,110,110),font=fs)
for i,(name,row) in enumerate(tiles):
    y=top+i*(th+pad)
    d.text((pad,y+th//2-24),name,fill=(20,20,20),font=fs)
    st=stats[name]['0.04°']; d.text((pad,y+th//2+2),f"0.04° 時黃線對底 {st['黃線對背景亮度比']}:1",fill=(110,110,110),font=fs)
    for j,img in enumerate(row):
        canvas.paste(Image.fromarray(img).resize((tw,th),Image.NEAREST),(left+j*(tw+pad),y))
d.text((pad,canvas.height-40),'每格右邊那條是白線。模擬用 Zhang & Wandell 的空間濾波，參數用 1996 原始發表值（ISETCam 收錄）；螢幕色，不代表實物。',fill=(110,110,110),font=fs)
canvas.save('/tmp/claude-0/work/fig_distance.png'); print(canvas.size)
