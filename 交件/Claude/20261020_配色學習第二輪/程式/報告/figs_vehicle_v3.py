# figs.py 的副本（v3）：只留車身取色圖 fig_vehicle，重排版面讓 A5 版心 126mm 寬時每個字 ≥ 2.2mm（6pt）。數據、色碼、裁切框都不變；其他圖的函式已移除，避免誤跑覆寫原圖。
import json, math, sys
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0,'/tmp/claude-0/r2/tw/work')
from ct import oklch, de, contrast
W='/tmp/claude-0/r2/tw/'; O=W+'img/'
FT='/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
f=lambda s:ImageFont.truetype(FT,s)
INK=(34,34,34); MUTED=(110,110,110); GRID=(225,225,225); TWC=(40,72,104); FRC=(168,180,192)
TW=json.load(open(W+'tw_peers.json')); R=json.load(open(W+'comparison.json'))
def rgb(h): h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))
def outline(d,box,h):  # 淺色塊加細框
    d.rectangle(box,fill=rgb(h),outline=(190,190,190) if oklch(h)[0]>0.85 else None)
TIER={'官網logo檔':'官網 logo','官網banner字標':'官網 banner 字卡','智財局商標圖樣':'智財局商標','第三方頁':'第三方頁面'}
# 7 車身色（第三方照片裁切）v3：兩排（每排 4 格，第 8 格放照片附註）；色碼字寫在色塊內；照片在左、兩色塊上下疊在右
OUT='/tmp/claude-0/report2/img/fig_vehicle_colours_v3.png'
def fig_vehicle_v3(out=OUT):
    V=json.load(open(W+'data/vehicle_colours.json'))
    PW,WMM=1420,126; FS=max(25,math.ceil(2.2*PW/WMM))   # 最小字身 px：2.2mm × 圖寬 px ÷ 顯示寬 mm
    cols=4; cw=350; PAD=8                                # 每格 350px；色塊內字左右留 8px
    PHW,PHH=140,98; SWX=PHW+8; SWW=180; SWH=46            # 照片框、色塊位置與大小；格內內容寬 328px，格與格之間空 22px
    X0=(PW-((cols-1)*cw+SWX+SWW))//2                      # 左右邊界對稱
    top,rowh=58,226; rows=math.ceil((len(V)+1)/cols)
    H=top+(rows-1)*rowh+207+9
    def on(h): return INK if contrast(h,'#222222')>=contrast(h,'#FFFFFF') else (255,255,255)  # 色塊上的字取對比較高的深字或白字
    im=Image.new('RGB',(PW,H),'white'); d=ImageDraw.Draw(im)
    d.text((X0,10),'車身取色（照片裁切中位與眾數）對 logo 主色、車身工程黃 #D68702',fill=INK,font=f(29))
    for i,v in enumerate(V):
        x=X0+(i%cols)*cw; y=top+(i//cols)*rowh; sy=y+38
        d.text((x,y),f"{v['company']} {v['part']}",fill=INK,font=f(27))
        ph=Image.open(v['file']).convert('RGB').crop(tuple(v['box'])); s=min(PHW/ph.width,PHH/ph.height)
        ph=ph.resize((round(ph.width*s),round(ph.height*s))); im.paste(ph,(x,sy))
        d.rectangle((x+SWX,sy,x+SWX+SWW,sy+SWH),fill=rgb(v['mode']))
        d.text((x+SWX+PAD,sy+SWH//2),'車身 '+v['mode'],fill=on(v['mode']),font=f(FS),anchor='lm')
        lg=list(v['dE_mode_to_logo'].items())
        if lg:
            h,dv=min(lg,key=lambda z:z[1]); ly=sy+SWH+6
            d.rectangle((x+SWX,ly,x+SWX+SWW,ly+SWH),fill=rgb(h))
            d.text((x+SWX+PAD,ly+SWH//2),'logo '+h,fill=on(h),font=f(FS),anchor='lm')
            d.text((x,y+146),f'對最近 logo 色 ΔE {dv}',fill=INK,font=f(FS))
        d.text((x,y+178),f"對 #D68702 ΔE {v['dE_mode_to_D68702']}",fill=INK,font=f(FS))
    x=X0+(len(V)%cols)*cw; y=top+(len(V)//cols)*rowh      # 第 8 格：照片附註（原文分兩行）
    d.text((x,y+146),'照片受光線與相機影響，',fill=MUTED,font=f(FS)); d.text((x,y+178),'車身色只是近似值。',fill=MUTED,font=f(FS))
    im.save(out); return im.size, FS
if __name__=='__main__':
    print('fig_vehicle_v3',fig_vehicle_v3())
