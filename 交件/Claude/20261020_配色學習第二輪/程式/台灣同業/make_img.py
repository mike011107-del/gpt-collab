# 每個 logo 版本：依 logos.json 裁切 → 去掉四周空白 → 白底（純白 logo 改深灰底）→ 等高 160px
# 輸出 img/<vid>.png；另出檢視用的拼圖 sheets/
import json, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
W='/tmp/claude-0/r2/tw/'
cfg=json.load(open(W+'work/logos.json'))
DARK={'lvyi','haoyuan_white'}   # 只有白色的版本
H=160; PAD=12
font=ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',18)
def prep(v):
    im=Image.open(v['file']).convert('RGBA')
    if v.get('crop'): im=im.crop(tuple(v['crop']))
    a=np.asarray(im).astype(int)
    if v['vid'] in DARK: m=a[...,3]>=40
    else: m=(a[...,3]>=40)&(a[...,:3].min(axis=2)<235)
    ys,xs=np.where(m)
    if len(ys): im=im.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1))
    bgc=(60,60,60,255) if v['vid'] in DARK else (255,255,255,255)
    bg=Image.new('RGBA',(im.width+2*PAD,im.height+2*PAD),bgc); bg.alpha_composite(im,(PAD,PAD))
    s=H/bg.height
    out=bg.resize((max(1,round(bg.width*s)),H),Image.LANCZOS).convert('RGB')
    return out, s
if __name__=='__main__':
    tiles=[]
    for v in cfg:
        out,s=prep(v); out.save(W+f"img/{v['vid']}.png"); tiles.append((v,out))
        print(v['vid'],out.size,'放大' if s>1 else '縮小',round(s,2))
    # 檢視用拼圖：每張 6 個，加標籤
    for k in range(0,len(tiles),6):
        grp=tiles[k:k+6]; wmax=min(900,max(t.width for _,t in grp))
        rows=[]
        for v,t in grp:
            if t.width>wmax: t=t.resize((wmax,round(t.height*wmax/t.width)),Image.LANCZOS)
            r=Image.new('RGB',(wmax+10,t.height+30),(200,200,200)); r.paste(t,(5,26))
            ImageDraw.Draw(r).text((5,3),f"{v['vid']} {v['company']} {v['version'][:22]}",fill=(0,0,0),font=font)
            rows.append(r)
        sh=Image.new('RGB',(max(r.width for r in rows),sum(r.height for r in rows)),(200,200,200))
        y=0
        for r in rows: sh.paste(r,(0,y)); y+=r.height
        sh.save(W+f'sheets/check_{k//6+1}.png'); print('sheet',k//6+1,sh.size)
