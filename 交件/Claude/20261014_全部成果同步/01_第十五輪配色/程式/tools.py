"""崧淳配色檢查工具。演算法照 GitHub 與原作者公開資料自己實作，沒有安裝任何套件。
- sRGB 線性化、OKLab/OKLCH：Björn Ottosson, bottosson.github.io/posts/oklab
- 色弱模擬：Machado 2009 矩陣（severity 1.0），數值取自 DaltonLens/DaltonLens-Python 與 colour-science/colour，兩者一致；在線性 RGB 上套用
- APCA Lc：Myndex/apca-w3 0.1.9 src/apca-w3.js 的常數
- 明度差規則：material-color-utilities hct.ts「tone 差 50 保證 4.5:1、差 40 保證 3:1」，HCT 的 tone 就是 CIELAB L*
- 反推字色：adobe/leonardo contrast-colors 的做法（沿明度二分搜尋到剛好達標）
- RAL 最近色號：Wikipedia List of RAL colours 的 L*a*b* 欄（hex 欄不可靠，不用）
"""
import sys, json, math, os
S='/tmp/claude-0/-home-claude/f822ab78-49b8-5e2f-8fbe-8111b065c404/scratchpad'
sys.path.insert(0,S); _cwd=os.getcwd(); os.chdir(S)
from cl import rgb, lab, de2000, lch, cr, lum, wx, FAV, VW
os.chdir(_cwd)

def hx(c): return '#%02X%02X%02X'%tuple(max(0,min(255,round(v))) for v in c)
def f_inv(x): return ((x+0.055)/1.055)**2.4 if x>=0.04045 else x/12.92
def f_fwd(x): return 1.055*x**(1/2.4)-0.055 if x>=0.0031308 else 12.92*x
def lin3(h): return [f_inv(v/255) for v in rgb(h)]
def from_lin(c): return hx([255*f_fwd(max(0,min(1,v))) for v in c])

# OKLab (Ottosson)
def oklab(h):
    r,g,b=lin3(h)
    l=0.4122214708*r+0.5363325363*g+0.0514459929*b
    m=0.2119034982*r+0.6806995451*g+0.1073969566*b
    s=0.0883024619*r+0.2817188376*g+0.6299787005*b
    l,m,s=[math.copysign(abs(v)**(1/3),v) for v in (l,m,s)]
    return (0.2104542553*l+0.7936177850*m-0.0040720468*s,
            1.9779984951*l-2.4285922050*m+0.4505937099*s,
            0.0259040371*l+0.7827717662*m-0.8086757660*s)
def oklab_to_hex(L,a,b):
    l=L+0.3963377774*a+0.2158037573*b; m=L-0.1055613458*a-0.0638541728*b; s=L-0.0894841775*a-1.2914855480*b
    l,m,s=l**3,m**3,s**3
    r=4.0767416621*l-3.3077115913*m+0.2309699292*s
    g=-1.2684380046*l+2.6097574011*m-0.3413193965*s
    bb=-0.0041960863*l-0.7034186147*m+1.7076147010*s
    ok=all(-1e-4<=v<=1+1e-4 for v in (r,g,bb))
    return from_lin([r,g,bb]), ok
def oklch(h):
    L,a,b=oklab(h); return L, math.hypot(a,b), math.degrees(math.atan2(b,a))%360
def oklch_hex(L,C,H):
    return oklab_to_hex(L, C*math.cos(math.radians(H)), C*math.sin(math.radians(H)))
def deok(h1,h2):
    a=oklab(h1); b=oklab(h2); return 100*math.dist(a,b)

# Machado 2009, severity 1.0
MACH={'protan':[[0.152286,1.052583,-0.204868],[0.114503,0.786281,0.099216],[-0.003882,-0.048116,1.051998]],
      'deutan':[[0.367322,0.860646,-0.227968],[0.280085,0.672501,0.047413],[-0.011820,0.042940,0.968881]],
      'tritan':[[1.255528,-0.076749,-0.178779],[-0.078411,0.930809,0.147602],[0.004733,0.691367,0.303900]]}
def cvd(h,kind):
    c=lin3(h); M=MACH[kind]
    return from_lin([sum(M[i][j]*c[j] for j in range(3)) for i in range(3)])
def gray(h):
    y=lum(h); return from_lin([y,y,y])

# APCA 0.1.9 (text, background)
def _Y(h):
    r,g,b=[v/255 for v in rgb(h)]
    return 0.2126729*r**2.4+0.7151522*g**2.4+0.0721750*b**2.4
def apca(text,bg):
    t,b=_Y(text),_Y(bg)
    t=t if t>0.022 else t+(0.022-t)**1.414
    b=b if b>0.022 else b+(0.022-b)**1.414
    if abs(b-t)<0.0005: return 0.0
    if b>t:
        s=(b**0.56-t**0.57)*1.14; out=0 if s<0.1 else s-0.027
    else:
        s=(b**0.65-t**0.62)*1.14; out=0 if s>-0.1 else s+0.027
    return out*100

# 反推字色（Leonardo 式）：固定色相彩度，找最接近 base 明度且達到對比的字色
def text_for(bg, base, target=4.5):
    L,C,H=oklch(base)
    best=None
    for i in range(0,101):
        for Lx in (L+i/200, L-i/200):
            if not 0<=Lx<=1: continue
            hcol,ok=oklch_hex(Lx,C,H)
            if cr(hcol,bg)>=target: return hcol
    return None

RAL=json.load(open(os.path.join(S,'r19','ral.json')))
def lab2hex_dummy(): pass
def nearest_ral(h,n=1):
    L,a,b=lab(h)
    # Wikipedia L*a*b* 為 D50；cl.lab 為 D65。差異對最近鄰排序影響小，用 RGB 欄重算 D65 Lab 比較更一致
    out=[]
    for k,v in RAL.items():
        out.append((de2000(h,hx(v['rgb'])),k,v['name'],hx(v['rgb'])))
    out.sort(); return out[:n]

def fate(h):
    w=wx(h); return sum(VW[k]*sum(s*FAV[k][e] for e,s in w.items()) for k in VW)
def fate30(pairs):
    tot=sum(p for _,p in pairs); f=sum(fate(h)*p for h,p in pairs)/tot
    return round((f+1)/1.88*30,1), f

# 實景底色：白牆、柏油、泥地、霧、黃昏、夜間（夜間＝亮度乘 0.15 並偏暖）
SCENES={'白牆':'#E9E7E1','柏油':'#3E3F41','泥地':'#6B5A45','霧':'#C9CCCC','黃昏':'#8A6F5C'}
def fog(h,k=0.55,fogc='#C9CCCC'):
    a=lin3(h); b=lin3(fogc); return from_lin([a[i]*(1-k)+b[i]*k for i in range(3)])
def night(h):
    a=lin3(h); return from_lin([a[0]*0.18,a[1]*0.15,a[2]*0.11])
