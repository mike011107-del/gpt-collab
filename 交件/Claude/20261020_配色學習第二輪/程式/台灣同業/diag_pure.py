# 診斷每個 logo 版本是不是「少數純色、無反鋸齒」：數不透明非白像素的相異 RGB 個數、前幾色涵蓋率、半透明像素比例
# 用法：python3 -I /tmp/claude-0/r2/tw/work/diag_pure.py
import sys, json, numpy as np
sys.path.insert(0,'/tmp/claude-0/r2/tw/work')
from measure import load, oklab_arr, hexof
W='/tmp/claude-0/r2/tw/'
cfg=json.load(open(W+'work/logos.json'))
for v in cfg:
    rgb,a=load(v['file'],v.get('crop')); ok=oklab_arr(rgb); L=ok[...,0]; C=np.hypot(ok[...,1],ok[...,2])
    white=(L>=0.93)&(C<0.04)
    fg=(a>=250)&~white
    semi=((a>0)&(a<250)).sum()
    px=rgb[fg].astype(int); n=len(px)
    if n==0: print(v['vid'],'n=0'); continue
    keys=px[:,0]*65536+px[:,1]*256+px[:,2]
    u,c=np.unique(keys,return_counts=True); o=np.argsort(-c); c=c[o]; u=u[o]
    cum=np.cumsum(c)/n
    top=[('#%06X'%u[i],round(c[i]/n,3)) for i in range(min(5,len(u)))]
    k99=int(np.searchsorted(cum,0.99)+1)
    print(f"{v['vid']:15s} n={n:7d} uniq={len(u):6d} k99={k99:4d} top3cov={cum[min(2,len(u)-1)]:.3f} semi_alpha={semi} top={top}")
