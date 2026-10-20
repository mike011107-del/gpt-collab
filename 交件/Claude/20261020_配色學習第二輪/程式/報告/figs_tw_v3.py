# figs.py 的副本（v3）：台灣同業的 5 張圖（logo 拼圖、分組比較、主色色相環、ΔL* 點圖、候選色距離），
# 重排字級與標籤位置，讓 A5 報告裡每個字印出來 ≥ 2.2mm（約 6pt）。
# 數據、色碼、點的位置、統計結果都不變：資料一樣讀 tw_peers.json、comparison.json；色相環的圓心、半徑、點的排法照舊。
# 其他圖（色塊、車身）的函式已移除，輸出一律寫到 report2/img/*_v3.png，不覆寫原圖。
import json, math, sys
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0,'/tmp/claude-0/r2/tw/work')
from ct import oklch, de
W='/tmp/claude-0/r2/tw/'; O='/tmp/claude-0/report2/img/'
FT='/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
f=lambda s:ImageFont.truetype(FT,s)
INK=(34,34,34); MUTED=(110,110,110); GRID=(225,225,225); TWC=(40,72,104); FRC=(168,180,192)
TW=json.load(open(W+'tw_peers.json')); R=json.load(open(W+'comparison.json'))
def rgb(h): h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))
TIER={'官網logo檔':'官網 logo','官網banner字標':'官網 banner 字卡','智財局商標圖樣':'智財局商標','第三方頁':'第三方頁面'}

# ---- 共用：畫字並記錄字框，最後檢查字級、重疊、出界、缺字 ----
class Fig:
    def __init__(s,size,wmm,bg='white'):
        s.im=Image.new('RGB',size,bg); s.d=ImageDraw.Draw(s.im); s.wmm=wmm
        s.req=math.ceil(2.2*size[0]/wmm)          # 最小字身 px：2.2mm × 圖寬 px ÷ 顯示寬 mm
        s.boxes=[]; s.sizes=[]
    def text(s,xy,txt,fs,fill=INK,anchor='la',bg=None):
        assert fs>=s.req,(txt,fs,s.req)
        ft=f(fs); bb=s.d.textbbox(xy,txt,font=ft,anchor=anchor)
        if bg: s.d.rectangle((bb[0]-3,bb[1]-3,bb[2]+3,bb[3]+3),fill=bg)
        s.d.text(xy,txt,fill=fill,font=ft,anchor=anchor); s.boxes.append((bb,txt)); s.sizes.append(fs); return bb
    def check(s):
        Wd,Ht=s.im.size; prob=[]
        for i,(a,ta) in enumerate(s.boxes):
            if a[0]<0 or a[1]<0 or a[2]>Wd or a[3]>Ht: prob.append(('出界',ta,a))
            for b,tb in s.boxes[i+1:]:
                if a[0]<b[2] and b[0]<a[2] and a[1]<b[3] and b[1]<a[3]: prob.append(('重疊',ta,tb))
        miss=missing_glyphs(''.join(t for _,t in s.boxes))
        if miss: prob.append(('缺字',miss))
        return {'size':s.im.size,'min_px':min(s.sizes),'min_pt':round(min(s.sizes)*s.wmm/Wd/25.4*72,2),
                'req_px':s.req,'h_mm':round(s.wmm*Ht/Wd,1),'problems':prob}
_ND=None
def missing_glyphs(txt):
    global _ND
    ft=f(40)
    if _ND is None: _ND=bytes(ft.getmask('\U0010FFFD'))
    return sorted({c for c in txt if not c.isspace() and bytes(ft.getmask(c))==_ND})

# 1 logo 拼圖（第三方圖）v3：格子加高到 210px，公司名 26px、出處｜配色 24px；logo 縮放框不變
def fig_logos(wmm=104):
    cw,ch,cols=370,210,3; n=len(TW); rows=math.ceil(n/cols); top=56
    F=Fig((cols*cw+20,top+rows*ch+4),wmm); im,d=F.im,F.d
    F.text((10,10),'台灣同業 logo（21 家，每家主版本；白底等比縮放）',30)
    for i,t in enumerate(TW):
        x=10+(i%cols)*cw; y=top+(i//cols)*ch
        lg=Image.open(t['img']); s=min(340/lg.width,118/lg.height); lg=lg.resize((max(1,round(lg.width*s)),max(1,round(lg.height*s))),Image.LANCZOS)
        d.rectangle((x,y,x+cw-12,y+ch-10),outline=GRID)
        im.paste(lg,(x+(cw-12-lg.width)//2,y+8+(118-lg.height)//2))
        F.text((x+8,y+132),t['company'],26)
        F.text((x+8,y+166),f"{TIER[t['tier']]}｜{t['scheme']}",24,fill=MUTED)
    im.save(O+'fig_tw_logo_grid_v3.png'); return F.check()

# 3 分組比較 v3：字級放大；長條、比例尺、數據不變；格線字置中
def fig_scheme(wmm=126):
    ORDER=['一個彩色','同色系','相鄰','對比','四色以上','只有黑白灰']
    a=R['分組']['台灣全部']; b=R['分組']['國外']
    F=Fig((900,520),wmm); d=F.d
    F.text((20,12),'配色方式占比：台灣 20 家 vs 國外 48 家',26)
    F.text((20,48),'同一規則：OKLCH 色相兩兩最大差 ≤45° 同色系、45–90° 相鄰、>90° 對比',17,fill=MUTED)
    d.rectangle((560,80,578,98),fill=TWC); F.text((584,89),'台灣 (n=20)',18,anchor='lm')
    d.rectangle((710,80,728,98),fill=FRC); F.text((734,89),'國外 (n=48)',18,anchor='lm')
    x0=150; sc=1000
    for k in range(0,61,20):
        xx=x0+k/100*sc; d.line((xx,110,xx,490),fill=GRID); F.text((xx,495),f'{k}%',17,fill=MUTED,anchor='mt')
    for i,k in enumerate(ORDER):
        y=120+i*62; F.text((20,y+22),k,19,anchor='lm')
        for j,(v,c) in enumerate([(a[k],TWC),(b[k],FRC)]):
            yy=y+j*24; w=v[1]*sc
            if w>0: d.rounded_rectangle((x0,yy,x0+w,yy+20),radius=4,fill=c)
            F.text((x0+w+6,yy+10),f'{v[0]} 家（{v[1]*100:.0f}%）',17,anchor='lm',bg='white')
    F.im.save(O+'fig_scheme_compare_v3.png'); return F.check()

# 4 主色色相環 v3：圓的半徑、點的大小與排法完全照舊，整組圖只往下平移 24px（圓心 y 370→394）讓出標題空間；
#   分格字 30px 置中放在格子中線上（字底白框蓋住其下的分格線）；底下說明分兩行
def fig_hue(wmm=108):
    F=Fig((1400,850),wmm); d=F.d
    F.text((20,8),'logo 主色的 OKLCH 色相：左國外 42 家，右台灣 17 家（點＝實際主色）',31)
    SEC=[('紅',345,40),('橘',40,70),('黃',70,110),('綠',110,170),('青',170,225),('藍',225,285),('紫',285,345)]
    LR={'紅':100,'橘':112,'黃':104,'綠':100,'青':100,'藍':100,'紫':100}   # 分格字距圓心半徑（只動字的位置）
    def panel(cx,cy,items,title):
        F.text((cx,58),title,29,anchor='mt')
        d.ellipse((cx-150,cy-150,cx+150,cy+150),outline=GRID,width=2)
        for nm,a0,a1 in SEC:
            t=math.radians(a0); d.line((cx+60*math.cos(t),cy-60*math.sin(t),cx+300*math.cos(t),cy-300*math.sin(t)),fill=GRID)
        for nm,a0,a1 in SEC:
            cnt=sum(1 for it in items if (it['h']-a0)%360<(a1-a0)%360)
            mid=math.radians((a0+((a1-a0)%360)/2)%360); r=LR[nm]
            F.text((cx+r*math.cos(mid),cy-r*math.sin(mid)),f'{nm}{cnt}',30,fill=MUTED,anchor='mm',bg='white')
        used=[]
        for it in sorted(items,key=lambda z:z['h']):
            t=math.radians(it['h']); r=162
            while any(abs(((it['h']-h0+180)%360)-180)<7 and abs(r-r1)<1 for h0,r1 in used): r+=22
            used.append((it['h'],r)); x=cx+r*math.cos(t); y=cy-r*math.sin(t)
            d.ellipse((x-10,y-10,x+10,y+10),fill=rgb(it['hex']),outline='white',width=2)
    panel(360,394,R['主色逐家']['國外'],'國外 48 家中有彩色的 42 家')
    panel(1040,394,R['主色逐家']['台灣'],'台灣 20 家中有彩色的 17 家')
    F.text((20,754),'色相用 OKLCH h，0° 在右邊、逆時針增加；',29,fill=MUTED)
    F.text((20,798),'分格：紅 345–40、橘 40–70、黃 70–110、綠 110–170、青 170–225、藍 225–285、紫 285–345。',29,fill=MUTED)
    F.im.save(O+'fig_hue_ring_v3.png'); return F.check()

# 5 ΔL* 點圖 v3：點的位置、比例尺不變；台灣中位字移到中位線左邊（原本壓在隨機中位虛線上），隨機中位字上移避開刻度字
def fig_dL(wmm=109):
    m=R['明度差ΔL*']; F=Fig((900,350),wmm); d=F.d
    F.text((20,10),'多色 logo 的明度差 ΔL*（各彩色 CIELAB L* 最大減最小）',24)
    x0,sc=150,11
    for k in range(0,61,10):
        xx=x0+k*sc; d.line((xx,70,xx,280),fill=GRID); F.text((xx,286),str(k),19,fill=MUTED,anchor='mt')
    rows=[('台灣 n=7',m['台灣']['值'],TWC,m['台灣']['中位'],'rt'),('國外 n=19',m['國外']['值'],FRC,m['國外']['中位'],'lt')]
    labs=[]
    for i,(nm,vals,c,md,anc) in enumerate(rows):
        y=110+i*80; F.text((20,y),nm,20,anchor='lm')
        seen={}
        for v in sorted(vals):
            k=round(v/2); off=seen.get(k,0); seen[k]=off+1
            x=x0+v*sc; yy=y-off*14
            d.ellipse((x-6,yy-6,x+6,yy+6),fill=c,outline='white')
        x=x0+md*sc; d.line((x,y-34,x,y+16),fill=INK,width=2)
        labs.append(((x-5 if anc=='rt' else x+5,y+16),f'中位 {md}',anc))
    rm=m['隨機兩彩色']['中位']; x=x0+rm*sc
    for yy in range(70,280,8): d.line((x,yy,x,yy+4),fill=(200,90,60),width=2)
    for xy,s,anc in labs: F.text(xy,s,19,anchor=anc,bg='white')
    F.text((x+6,244),f'隨機兩彩色中位 {rm}',19,fill=(170,70,40),bg='white')
    F.text((20,318),'台灣與國外中位差 12.4，置換檢定單尾 p=0.137；台灣只有 7 家，差距可能是樣本小造成。',19,fill=MUTED)
    F.im.save(O+'fig_dL_v3.png'); return F.check()

# 6 候選色與台灣同業主色的 CIEDE2000（只列事實）v3：字級放大；兩列間距 170→175；底下第一條註分兩行
def fig_cand(wmm=126):
    C=R['候選色距離']; F=Fig((900,530),wmm); d=F.d
    F.text((20,12),'主色候選與台灣同業主色的色差（CIEDE2000，最近三家）',23)
    for i,(nm,v) in enumerate(C.items()):
        y=60+i*175; hx=nm.split()[-1]
        d.rectangle((20,y,140,y+90),fill=rgb(hx)); F.text((20,y+98),nm,18)
        for j,r in enumerate(v['主色最近三家']):
            x=200+j*230; d.rectangle((x,y,x+120,y+90),fill=rgb(r['hex']))
            F.text((x,y+98),f"{r['company']} {r['hex']}",17); F.text((x,y+122),f"ΔE2000 = {r['dE']}",17)
            if r['company']=='大亞': F.text((x,y+146),'＊槽體漸層的深端',16,fill=(170,70,40))
    y0=414
    F.text((20,y0),'＊大亞 #243952 是槽體由深藍漸到灰青 #83A9A7 的深端；',16,fill=MUTED)
    F.text((36,y0+26),'大亞 logo 面積最大的是黑 #060606（約 41–45%），藍色槽體約 24–28%。',16,fill=MUTED)
    F.text((20,y0+52),'華通另一站（嘉佳／華通衛生行）的青 #005959 跟深青差 9.3，但那不是華通清淤主版本的主色。',16,fill=MUTED)
    F.text((20,y0+78),'只列色差事實，不代表推薦或排序。',16,fill=MUTED)
    F.im.save(O+'fig_candidates_dE_v3.png'); return F.check()

if __name__=='__main__':
    names=sys.argv[1:] or ['fig_logos','fig_scheme','fig_hue','fig_dL','fig_cand']
    for nm in names: print(nm,globals()[nm]())
