import math
def _f_inv(x): return ((x+0.055)/1.055)**2.4 if x>=0.04045 else x/12.92
def _f_fwd(x): return 1.055*x**(1/2.4)-0.055 if x>=0.0031308 else 12.92*x
def rgb(h): h=h.lstrip('#'); return [int(h[i:i+2],16) for i in (0,2,4)]
def hx(c): return '#%02X%02X%02X'%tuple(max(0,min(255,round(v))) for v in c)
def lin3(h): return [_f_inv(v/255) for v in rgb(h)]
def lum(h): r,g,b=lin3(h); return 0.2126*r+0.7152*g+0.0722*b
def cr(a,b):
    x,y=sorted([lum(a),lum(b)],reverse=True); return (x+0.05)/(y+0.05)
def oklab_lin(r,g,b):
    l=0.4122214708*r+0.5363325363*g+0.0514459929*b
    m=0.2119034982*r+0.6806995451*g+0.1073969566*b
    s=0.0883024619*r+0.2817188376*g+0.6299787005*b
    l,m,s=[math.copysign(abs(v)**(1/3),v) for v in (l,m,s)]
    return (0.2104542553*l+0.7936177850*m-0.0040720468*s,1.9779984951*l-2.4285922050*m+0.4505937099*s,0.0259040371*l+0.7827717662*m-0.8086757660*s)
def lab2lin(L,a,b):
    l=L+0.3963377774*a+0.2158037573*b; m=L-0.1055613458*a-0.0638541728*b; s=L-0.0894841775*a-1.2914855480*b
    l,m,s=l**3,m**3,s**3
    return (4.0767416621*l-3.3077115913*m+0.2309699292*s,-1.2684380046*l+2.6097574011*m-0.3413193965*s,-0.0041960863*l-0.7034186147*m+1.7076147010*s)
def oklch(h):
    L,a,b=oklab_lin(*lin3(h)); return L,math.hypot(a,b),math.degrees(math.atan2(b,a))%360
def ingamut(c,eps=1e-6): return all(-eps<=v<=1+eps for v in c)
def from_oklch(L,C,H,clip=True):
    hr=math.radians(H)
    c=lab2lin(L,C*math.cos(hr),C*math.sin(hr))
    if not ingamut(c):
        if not clip: return None
        lo,hi=0,C
        for _ in range(30):
            mid=(lo+hi)/2; c2=lab2lin(L,mid*math.cos(hr),mid*math.sin(hr))
            if ingamut(c2): lo=mid
            else: hi=mid
        c=lab2lin(L,lo*math.cos(hr),lo*math.sin(hr))
    return hx([255*_f_fwd(max(0,min(1,v))) for v in c])
def maxC(L,H):
    lo,hi=0,0.4; hr=math.radians(H)
    for _ in range(30):
        mid=(lo+hi)/2
        if ingamut(lab2lin(L,mid*math.cos(hr),mid*math.sin(hr))): lo=mid
        else: hi=mid
    return lo
