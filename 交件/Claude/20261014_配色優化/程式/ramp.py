from ok import *
STEPS=[50,100,200,300,400,500,600,700,800,900,950]
LT=[0.975,0.945,0.895,0.83,0.745,0.655,0.565,0.475,0.385,0.30,0.225]   # 跨色相對齊的明度（Huetone/Stripe 做法）
def ramp(key,hue_light=None,hue_dark=None,cmin=0.12,cdark=0.65,lock=True):
    L0,C0,H0=oklch(key)
    i0=min(range(len(LT)),key=lambda i:abs(LT[i]-L0))
    hl=H0 if hue_light is None else hue_light; hd=H0 if hue_dark is None else hue_dark
    out=[]
    for i,(s,L) in enumerate(zip(STEPS,LT)):
        if i<=i0:
            t=i/i0 if i0 else 1; H=hl+(H0-hl)*t; C=C0*(cmin+(1-cmin)*t**1.3)
        else:
            t=(i-i0)/(len(LT)-1-i0); H=H0+(hd-H0)*t; C=C0*(1-(1-cdark)*t)
        h=from_oklch(L,C,H)
        out.append([s,h])
    if lock: out[i0][1]=key.upper()
    return out,STEPS[i0]
def neutral(hue,c=0.012,cl=0.004):
    out=[]
    for s,L in zip(STEPS,LT):
        t=(0.975-L)/(0.975-0.225); C=cl+(c-cl)*min(1,t*1.6)
        out.append([s,from_oklch(L,C,hue)])
    return out
