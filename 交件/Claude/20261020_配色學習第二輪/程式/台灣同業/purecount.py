# 修正量色占比：只有少數純色、沒有反鋸齒的圖（不透明非白像素 ≤4 個相異 RGB、涵蓋 ≥99.9%）改用逐像素直接計數；
# 其他圖（有反鋸齒、JPEG 雜色、漸層淡出）沿用 measure.py 去邊結果。輸出 data/measure_final.json（格式同 measure_raw.json，加 method 欄）。
# 另外對多色 logo 算「不去邊、像素分給最近種子色」的占比，當去邊結果的敏感度參考 → data/share_sensitivity.json
# 用法：python3 -I /tmp/claude-0/r2/tw/work/purecount.py
import sys, json, copy, numpy as np
sys.path.insert(0,'/tmp/claude-0/r2/tw/work')
from measure import load, oklab_arr, hexof
W='/tmp/claude-0/r2/tw/'
cfg={v['vid']:v for v in json.load(open(W+'work/logos.json'))}
raw=json.load(open(W+'data/measure_raw.json'))
MAXU=4; COV=0.999
out=[]; log=[]
for r in raw:
    v=cfg[r['vid']]; rgb,a=load(v['file'],v.get('crop')); ok=oklab_arr(rgb); L=ok[...,0]; C=np.hypot(ok[...,1],ok[...,2])
    fg=(a>=250)&~((L>=0.93)&(C<0.04)); n=int(fg.sum())
    r2=copy.deepcopy(r); r2['method']='去邊（measure.py）'
    if n:
        px=rgb[fg].astype(int); keys=px[:,0]*65536+px[:,1]*256+px[:,2]
        u,c=np.unique(keys,return_counts=True); o=np.argsort(-c); u=u[o]; c=c[o]
        k=min(MAXU,len(u))
        if len(u)<=MAXU or c[:k].sum()/n>=COV:
            chrom=[]; neut=[]; nch=0
            for i in range(k):
                hx='#%06X'%u[i]; rr=np.array([[u[i]>>16,(u[i]>>8)&255,u[i]&255]],float); o2=oklab_arr(rr)[0]
                Li=o2[0]; Ci=float(np.hypot(o2[1],o2[2])); sh=round(c[i]/n,4)
                if Ci>=0.04:
                    nch+=c[i]; chrom.append(dict(hex=hx,median_hex=hx,share=sh,n=int(c[i]),okL_p5=round(float(Li),3),okL_p95=round(float(Li),3),okL_spread=0.0,dark_end=hx,light_end=hx))
                else:
                    nm=[x for x,a0,b0 in [('黑',0,.3),('深灰',.3,.55),('灰',.55,.8),('淺灰',.8,.93)] if a0<=Li<b0][0]
                    neut.append(dict(name=nm,hex=hx,share=sh))
            r2.update(method='逐像素直接計數（純色、無反鋸齒）',n_direct=n,chromatic=chrom,neutral=neut,chromatic_share=round(nch/n,4),
                      old_edge_removed_shares=dict(chromatic=[(g['hex'],g['share']) for g in r['chromatic']],neutral=[(g['name'],g['hex'],g['share']) for g in r['neutral']],chromatic_share=r['chromatic_share']))
            log.append(f"{r['vid']}: 去邊 {[(g['hex'],g['share']) for g in r['chromatic']]}+{[(g['hex'],g['share']) for g in r['neutral']]} → 直接 {[(g['hex'],g['share']) for g in chrom]}+{[(g['hex'],g['share']) for g in neut]}")
    out.append(r2)
json.dump(out,open(W+'data/measure_final.json','w'),ensure_ascii=False,indent=1)
print('\n'.join(log))
