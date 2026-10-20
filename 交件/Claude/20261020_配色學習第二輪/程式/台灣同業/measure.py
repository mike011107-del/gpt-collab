# 量 logo 像素：略過透明、白、反鋸齒邊緣；彩色門檻 OKLCH C>=0.04
# 用法：python3 -I measure.py（讀 logos.json 設定，輸出 ../data/measure_raw.json）
import sys, json, math
import numpy as np
from PIL import Image
sys.path.insert(0,'/tmp/claude-0/r2/tw/work')
from ct import oklch, lab as lab_hex

C_MIN=0.04        # 彩色門檻（OKLCH C）
WHITE_L=0.93      # OKLab L 以上且 C<0.04 當白底略過
ALPHA_MIN=250     # alpha 低於此值（透明、半透明邊）略過
NEI_D=0.05        # 鄰點 OKLab 距離小於此值算「同色」
NEI_K=4           # 8 鄰點中至少 4 個同色才留（去反鋸齒）
CELL=0.03         # 色空間格子大小
MIN_SHARE=0.015   # 色群占 logo 像素 1.5% 以下當雜色

M1=np.array([[0.4122214708,0.5363325363,0.0514459929],[0.2119034982,0.6806995451,0.1073969566],[0.0883024619,0.2817188376,0.6299787005]])
M2=np.array([[0.2104542553,0.7936177850,-0.0040720468],[1.9779984951,-2.4285922050,0.4505937099],[0.0259040371,0.7827717662,-0.8086757660]])
def oklab_arr(rgb):
    c=rgb/255.0; l=np.where(c<=0.04045,c/12.92,((c+0.055)/1.055)**2.4)
    lms=np.cbrt(l@M1.T); return lms@M2.T
def hexof(rgb): return '#%02X%02X%02X'%tuple(int(round(v)) for v in rgb)

def load(path,crop=None):
    im=Image.open(path).convert('RGBA')
    if crop: im=im.crop(tuple(crop))
    a=np.asarray(im).astype(float); return a[...,:3],a[...,3]

def measure(path,crop=None):
    rgb,alpha=load(path,crop); H,W=alpha.shape
    ok=oklab_arr(rgb); L=ok[...,0]; C=np.hypot(ok[...,1],ok[...,2])
    valid=alpha>=ALPHA_MIN
    white=(L>=WHITE_L)&(C<C_MIN)
    fg=valid&~white
    # 鄰點同色計數
    pad=np.pad(ok,((1,1),(1,1),(0,0)),mode='edge'); fpad=np.pad(fg,1)
    cnt=np.zeros((H,W),int)
    for dy in (-1,0,1):
        for dx in (-1,0,1):
            if dy==0 and dx==0: continue
            nb=pad[1+dy:1+dy+H,1+dx:1+dx+W]; nf=fpad[1+dy:1+dy+H,1+dx:1+dx+W]
            cnt+=((np.linalg.norm(nb-ok,axis=2)<NEI_D)&nf)
    core=fg&(cnt>=NEI_K)
    n_fg=int(fg.sum()); n_core=int(core.sum())
    out=dict(path=path,crop=crop,size=[W,H],n_fg=n_fg,n_core=n_core,
             edge_removed=round(1-n_core/n_fg,3) if n_fg else None)
    if n_core==0:
        out.update(chromatic=[],neutral=[],chromatic_share=0); return out
    chrom=core&(C>=C_MIN); neut=core&(C<C_MIN)
    # 彩色：格子直方圖→連通→色群
    P=ok[chrom]; R=rgb[chrom]
    groups=[]
    if len(P):
        q=np.floor(P/CELL).astype(int)
        keys,inv,counts=np.unique(q,axis=0,return_inverse=True,return_counts=True)
        inv=inv.ravel()
        keep=counts>=max(3,0.002*n_core)
        idx={tuple(k):i for i,k in enumerate(keys) if keep[i]}
        comp={}; cid=0
        for k in idx:
            if k in comp: continue
            stack=[k]; comp[k]=cid
            while stack:
                x=stack.pop()
                for d0 in (-1,0,1):
                    for d1 in (-1,0,1):
                        for d2 in (-1,0,1):
                            y=(x[0]+d0,x[1]+d1,x[2]+d2)
                            if y in idx and y not in comp: comp[y]=cid; stack.append(y)
            cid+=1
        lab_of_cell=np.full(len(keys),-1)
        for k,i in idx.items(): lab_of_cell[i]=comp[k]
        pix_comp=lab_of_cell[inv]
        for g in range(cid):
            m=pix_comp==g; n=int(m.sum())
            if n/n_core<MIN_SHARE: continue
            gp=P[m]; gr=R[m]
            # 眾數色：該色群內像素最多的格子
            cells=inv[m]; uc,cc=np.unique(cells,return_counts=True); top=uc[np.argmax(cc)]
            mode_rgb=R[inv==top].mean(axis=0)
            Ls=gp[:,0]; order=np.argsort(Ls)
            lo=gr[order[int(0.05*(n-1))]]; hi=gr[order[int(0.95*(n-1))]]
            groups.append(dict(hex=hexof(mode_rgb),median_hex=hexof(np.median(gr,axis=0)),
                share=round(n/n_core,4),n=n,
                okL_p5=round(float(np.percentile(Ls,5)),3),okL_p95=round(float(np.percentile(Ls,95)),3),
                okL_spread=round(float(np.percentile(Ls,95)-np.percentile(Ls,5)),3),
                dark_end=hexof(lo),light_end=hexof(hi)))
    groups.sort(key=lambda g:-g['share'])
    # 黑白灰：按明度分四段
    nl=[]
    if neut.any():
        Ln=L[neut]; Rn=rgb[neut]
        for name,a,b in [('黑',0,0.30),('深灰',0.30,0.55),('灰',0.55,0.80),('淺灰',0.80,WHITE_L)]:
            m=(Ln>=a)&(Ln<b); n=int(m.sum())
            if n/n_core<MIN_SHARE: continue
            nl.append(dict(name=name,hex=hexof(np.median(Rn[m],axis=0)),share=round(n/n_core,4)))
    out.update(chromatic=groups,neutral=nl,
               chromatic_share=round(float(chrom.sum())/n_core,4),
               white_share_of_valid=round(float((valid&white).sum())/max(1,valid.sum()),4))
    return out

if __name__=='__main__':
    cfg=json.load(open('/tmp/claude-0/r2/tw/work/logos.json'))
    res=[]
    for v in cfg:
        r=measure(v['file'],v.get('crop')); r.update({k:v[k] for k in v if k not in ('file','crop')})
        res.append(r)
        cs=' '.join(f"{g['hex']}({g['share']:.0%},Lsp{g['okL_spread']:.2f})" for g in r['chromatic'])
        ns=' '.join(f"{g['name']}{g['hex']}({g['share']:.0%})" for g in r['neutral'])
        print(f"{v['vid']:14s} 去邊{r['edge_removed']} 彩:{cs} | 無彩:{ns}")
    json.dump(res,open('/tmp/claude-0/r2/tw/data/measure_raw.json','w'),ensure_ascii=False,indent=1)
