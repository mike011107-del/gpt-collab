# 報告用圖：logo 拼圖、每家色塊、分組比較、主色色相環、ΔL* 點圖、候選色距離、車身
import json, math, sys
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0,'/tmp/claude-0/r2/tw/work')
from ct import oklch, de
W='/tmp/claude-0/r2/tw/'; O=W+'img/'
FT='/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
f=lambda s:ImageFont.truetype(FT,s)
INK=(34,34,34); MUTED=(110,110,110); GRID=(225,225,225); TWC=(40,72,104); FRC=(168,180,192)
TW=json.load(open(W+'tw_peers.json')); R=json.load(open(W+'comparison.json'))
def rgb(h): h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))
def outline(d,box,h):  # 淺色塊加細框
    d.rectangle(box,fill=rgb(h),outline=(190,190,190) if oklch(h)[0]>0.85 else None)
TIER={'官網logo檔':'官網 logo','官網banner字標':'官網 banner 字卡','智財局商標圖樣':'智財局商標','第三方頁':'第三方頁面'}
# 1 logo 拼圖（第三方圖）
def fig_logos():
    cw,ch,cols=370,190,3; n=len(TW); rows=math.ceil(n/cols)
    im=Image.new('RGB',(cols*cw+20,rows*ch+60),'white'); d=ImageDraw.Draw(im)
    d.text((10,12),'台灣同業 logo（21 家，每家主版本；白底等比縮放）',fill=INK,font=f(22))
    for i,t in enumerate(TW):
        x=10+(i%cols)*cw; y=50+(i//cols)*ch
        lg=Image.open(t['img']); s=min(340/lg.width,118/lg.height); lg=lg.resize((max(1,round(lg.width*s)),max(1,round(lg.height*s))),Image.LANCZOS)
        d.rectangle((x,y,x+cw-12,y+ch-10),outline=GRID)
        im.paste(lg,(x+(cw-12-lg.width)//2,y+8+(118-lg.height)//2))
        d.text((x+8,y+132),t['company'],fill=INK,font=f(18))
        d.text((x+8,y+156),f"{TIER[t['tier']]}｜{t['scheme']}",fill=MUTED,font=f(14))
    im.save(O+'fig_tw_logo_grid.png'); return im.size
# 2 每家色塊：一條 100% 長條，彩色與黑白灰同一比例尺，寬度＝占 logo 非白像素比例（第三次修正：原本兩欄比例尺不同、最小寬 64px）
def fig_swatch():
    BAR=760; x0=180; rh=84; top=104
    im=Image.new('RGB',(1440,top+rh*len(TW)+60),'white'); d=ImageDraw.Draw(im)
    d.text((10,12),'台灣同業 logo 量到的顏色：色塊寬＝占 logo 非白像素比例（彩色與黑白灰同一比例尺，整條框＝100%）',fill=INK,font=f(19))
    d.text((10,40),'先排彩色（OKLCH C≥0.04）再排黑白灰；框內空白＝未歸類像素（1.5% 以下雜色、反鋸齒、漸層淡出）。太窄的色塊在下一行標數字。＊＝純色圖逐像素直接計數，其餘為去邊後像素。',fill=MUTED,font=f(13))
    d.text((10,74),'公司',fill=MUTED,font=f(14)); d.text((x0,74),'0%',fill=MUTED,font=f(12)); d.text((x0+BAR//2-12,74),'50%',fill=MUTED,font=f(12)); d.text((x0+BAR-30,74),'100%',fill=MUTED,font=f(12))
    d.text((1080,74),'配色方式｜彩色數｜漸層',fill=MUTED,font=f(14))
    for i,t in enumerate(TW):
        y=top+i*rh; d.line((10,y+rh-4,1430,y+rh-4),fill=GRID)
        star='＊' if (t.get('share_method') or '').startswith('逐像素') else ''
        d.text((10,y+4),t['company']+star,fill=INK,font=f(17)); d.text((10,y+26),TIER[t['tier']],fill=MUTED,font=f(12))
        segs=[(c['hex'],c['share']) for c in (t['cols'] or [])]+[(n['hex'],n['share']) for n in t['neutral'] if n['hex'].upper()!='#FFFFFF' and n['share']]
        whitetext=any(n['hex'].upper()=='#FFFFFF' for n in t['neutral'])
        if t.get('white_only'):
            d.text((x0,y+8),'只取得白色反白版，無法量色占比',fill=MUTED,font=f(14))
        else:
            d.rectangle((x0,y+4,x0+BAR,y+30),outline=(200,200,200))
            x=float(x0); row2=x0-8
            for hx,sh in segs:
                w=BAR*sh; x1=x+w
                d.rectangle((round(x),y+4,max(round(x),round(x1)-1),y+30),fill=rgb(hx))
                lab=f"{hx} {sh*100:.1f}%"; lw=d.textlength(lab,font=f(12))
                if w>=lw+6: d.text((round(x)+2,y+34),lab,fill=INK,font=f(12))
                else:
                    cx=x+w/2; lx=max(cx-4,row2+10); d.line((cx,y+31,cx,y+52),fill=MUTED); d.line((cx,y+52,lx+2,y+52),fill=MUTED)
                    d.text((lx+2,y+54),lab,fill=INK,font=f(12)); row2=lx+2+lw
                x=x1
            if t['cols'] is None: d.text((x0+BAR+8,y+8),'墨色商標，不計色',fill=MUTED,font=f(12))
            elif whitetext: d.text((x0+BAR+8,y+8),'＋白字（未計面積）',fill=MUTED,font=f(12))
        g={True:'有',False:'無',None:'—'}[t['gradient']]
        d.text((1080,y+8),f"{t['scheme']}｜{t['n_chromatic'] if t['n_chromatic'] is not None else '—'}｜{g}",fill=INK,font=f(16))
    d.text((10,top+rh*len(TW)+10),'占比來源：tw_peers.json（data/measure_final.json）。日技紅 2.9% 取自不去邊色相格；一元藍 97%、灰 3% 用不去邊最近色分法；漸層的深淺端併成一色。',fill=MUTED,font=f(13))
    im.save(O+'fig_tw_swatches.png'); return im.size
# 3 分組比較（百分比，台灣 20 家 vs 國外 48 家）
def fig_scheme():
    ORDER=['一個彩色','同色系','相鄰','對比','四色以上','只有黑白灰']
    a=R['分組']['台灣全部']; b=R['分組']['國外']
    im=Image.new('RGB',(900,520),'white'); d=ImageDraw.Draw(im)
    d.text((20,14),'配色方式占比：台灣 20 家 vs 國外 48 家',fill=INK,font=f(22))
    d.text((20,46),'同一規則：OKLCH 色相兩兩最大差 ≤45° 同色系、45–90° 相鄰、>90° 對比',fill=MUTED,font=f(14))
    d.rectangle((560,78,576,94),fill=TWC); d.text((582,76),'台灣 (n=20)',fill=INK,font=f(15))
    d.rectangle((700,78,716,94),fill=FRC); d.text((722,76),'國外 (n=48)',fill=INK,font=f(15))
    x0=150; sc=1000
    for k in range(0,61,20):
        xx=x0+k/100*sc; d.line((xx,110,xx,490),fill=GRID); d.text((xx-10,494),f'{k}%',fill=MUTED,font=f(12))
    for i,k in enumerate(ORDER):
        y=120+i*62; d.text((20,y+12),k,fill=INK,font=f(17))
        for j,(v,c) in enumerate([(a[k],TWC),(b[k],FRC)]):
            yy=y+j*24; w=v[1]*sc
            if w>0: d.rounded_rectangle((x0,yy,x0+w,yy+20),radius=4,fill=c)
            d.text((x0+w+6,yy+2),f'{v[0]} 家（{v[1]*100:.0f}%）',fill=INK,font=f(13))
    im.save(O+'fig_scheme_compare.png'); return im.size
# 4 主色色相環：左國外 42 家、右台灣 17 家，點用實際主色，同一角度附近的點往外排
def fig_hue():
    im=Image.new('RGB',(1400,850),'white'); d=ImageDraw.Draw(im)
    d.text((20,14),'logo 主色的 OKLCH 色相：左國外 42 家，右台灣 17 家（點＝實際主色）',fill=INK,font=f(22))
    SEC=[('紅',345,40),('橘',40,70),('黃',70,110),('綠',110,170),('青',170,225),('藍',225,285),('紫',285,345)]
    def panel(cx,cy,items,title):
        d.text((cx-110,52),title,fill=INK,font=f(18))
        d.ellipse((cx-150,cy-150,cx+150,cy+150),outline=GRID,width=2)
        for nm,a0,a1 in SEC:
            t=math.radians(a0); d.line((cx+60*math.cos(t),cy-60*math.sin(t),cx+300*math.cos(t),cy-300*math.sin(t)),fill=GRID)
            cnt=sum(1 for it in items if (it['h']-a0)%360<(a1-a0)%360)
            mid=math.radians((a0+((a1-a0)%360)/2)%360)
            d.text((cx+100*math.cos(mid)-14,cy-100*math.sin(mid)-10),f'{nm}{cnt}',fill=MUTED,font=f(15))
        used=[]
        for it in sorted(items,key=lambda z:z['h']):
            t=math.radians(it['h']); r=162
            while any(abs(((it['h']-h0+180)%360)-180)<7 and abs(r-r1)<1 for h0,r1 in used): r+=22
            used.append((it['h'],r)); x=cx+r*math.cos(t); y=cy-r*math.sin(t)
            d.ellipse((x-10,y-10,x+10,y+10),fill=rgb(it['hex']),outline='white',width=2)
    panel(360,370,R['主色逐家']['國外'],'國外 48 家中有彩色的 42 家')
    panel(1040,370,R['主色逐家']['台灣'],'台灣 20 家中有彩色的 17 家')
    d.text((20,822),'色相用 OKLCH h，0° 在右邊、逆時針增加；分格：紅 345–40、橘 40–70、黃 70–110、綠 110–170、青 170–225、藍 225–285、紫 285–345。',fill=MUTED,font=f(13))
    im.save(O+'fig_hue_ring.png'); return im.size
# 5 ΔL* 點圖
def fig_dL():
    m=R['明度差ΔL*']; im=Image.new('RGB',(900,330),'white'); d=ImageDraw.Draw(im)
    d.text((20,14),'多色 logo 的明度差 ΔL*（各彩色 CIELAB L* 最大減最小）',fill=INK,font=f(20))
    x0,sc=150,11
    for k in range(0,61,10):
        xx=x0+k*sc; d.line((xx,70,xx,280),fill=GRID); d.text((xx-8,284),str(k),fill=MUTED,font=f(12))
    rows=[('台灣 n=7',m['台灣']['值'],TWC,m['台灣']['中位']),('國外 n=19',m['國外']['值'],FRC,m['國外']['中位'])]
    for i,(nm,vals,c,md) in enumerate(rows):
        y=110+i*80; d.text((20,y-8),nm,fill=INK,font=f(16))
        seen={}
        for v in sorted(vals):
            k=round(v/2); off=seen.get(k,0); seen[k]=off+1
            x=x0+v*sc; yy=y-off*14
            d.ellipse((x-6,yy-6,x+6,yy+6),fill=c,outline='white')
        x=x0+md*sc; d.line((x,y-34,x,y+16),fill=INK,width=2); d.text((x+4,y+14),f'中位 {md}',fill=INK,font=f(13))
    rm=m['隨機兩彩色']['中位']; x=x0+rm*sc
    for yy in range(70,280,8): d.line((x,yy,x,yy+4),fill=(200,90,60),width=2)
    d.text((x+4,262),f'隨機兩彩色中位 {rm}',fill=(170,70,40),font=f(13))
    d.text((20,306),'台灣與國外中位差 12.4，置換檢定單尾 p=0.137；台灣只有 7 家，差距可能是樣本小造成。',fill=MUTED,font=f(13))
    im.save(O+'fig_dL.png'); return im.size
# 6 候選色與台灣同業主色的 CIEDE2000（只列事實）；第三次修正：註明大亞 #243952 是槽體漸層深端、大亞面積最大是黑
def fig_cand():
    C=R['候選色距離']; im=Image.new('RGB',(900,470),'white'); d=ImageDraw.Draw(im)
    d.text((20,14),'主色候選與台灣同業主色的色差（CIEDE2000，最近三家）',fill=INK,font=f(20))
    for i,(nm,v) in enumerate(C.items()):
        y=60+i*170; hx=nm.split()[-1]
        d.rectangle((20,y,140,y+90),fill=rgb(hx)); d.text((20,y+96),nm,fill=INK,font=f(15))
        for j,r in enumerate(v['主色最近三家']):
            x=200+j*230; d.rectangle((x,y,x+120,y+90),fill=rgb(r['hex']))
            d.text((x,y+96),f"{r['company']} {r['hex']}",fill=INK,font=f(14)); d.text((x,y+118),f"ΔE2000 = {r['dE']}",fill=INK,font=f(14))
            if r['company']=='大亞': d.text((x,y+140),'＊槽體漸層的深端',fill=(170,70,40),font=f(13))
    d.text((20,396),'＊大亞 #243952 是槽體由深藍漸到灰青 #83A9A7 的深端；大亞 logo 面積最大的是黑 #060606（約 41–45%），藍色槽體約 24–28%。',fill=MUTED,font=f(13))
    d.text((20,418),'華通另一站（嘉佳／華通衛生行）的青 #005959 跟深青差 9.3，但那不是華通清淤主版本的主色。',fill=MUTED,font=f(13))
    d.text((20,440),'只列色差事實，不代表推薦或排序。',fill=MUTED,font=f(13))
    im.save(O+'fig_candidates_dE.png'); return im.size
# 7 車身色（第三方照片裁切）
def fig_vehicle():
    V=json.load(open(W+'data/vehicle_colours.json')); cw=200
    im=Image.new('RGB',(cw*len(V)+20,330),'white'); d=ImageDraw.Draw(im)
    d.text((10,10),'車身取色（照片裁切中位與眾數）對 logo 主色、車身工程黃 #D68702',fill=INK,font=f(18))
    for i,v in enumerate(V):
        x=10+i*cw; ph=Image.open(v['file']).convert('RGB').crop(tuple(v['box'])); s=min(180/ph.width,110/ph.height)
        ph=ph.resize((round(ph.width*s),round(ph.height*s))); im.paste(ph,(x,44))
        d.text((x,160),f"{v['company']} {v['part']}",fill=INK,font=f(14))
        d.rectangle((x,184,x+85,224),fill=rgb(v['mode'])); d.text((x,228),'車身 '+v['mode'],fill=INK,font=f(12))
        lg=list(v['dE_mode_to_logo'].items())
        if lg:
            h,dv=min(lg,key=lambda z:z[1]); d.rectangle((x+92,184,x+177,224),fill=rgb(h)); d.text((x+92,228),'logo '+h,fill=INK,font=f(12))
            d.text((x,250),f'對最近 logo 色 ΔE {dv}',fill=INK,font=f(12))
        d.text((x,270),f"對 #D68702 ΔE {v['dE_mode_to_D68702']}",fill=INK,font=f(12))
    d.text((10,304),'照片受光線與相機影響，車身色只是近似值。',fill=MUTED,font=f(12))
    im.save(O+'fig_vehicle_colours.png'); return im.size
if __name__=='__main__':
    import sys as _s
    names=_s.argv[1:] or ['fig_logos','fig_swatch','fig_scheme','fig_hue','fig_dL','fig_cand','fig_vehicle']
    for nm in names: print(nm,globals()[nm]())
