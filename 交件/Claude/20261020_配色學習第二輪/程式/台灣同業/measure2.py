# 補量：不去邊的色相分布（30°一格，C>=0.06）與深色無彩（L<0.8）
# 用途：找出 measure.py 去邊時被刪掉的細小字或細線（小圖最常見），再逐張目視確認
import sys, json, numpy as np
sys.path.insert(0,'/tmp/claude-0/r2/tw/work')
from measure import load, oklab_arr, hexof
from ct import oklch, hue_diff
W='/tmp/claude-0/r2/tw/'
cfg=json.load(open(W+'work/logos.json')); raw={r['vid']:r for r in json.load(open(W+'data/measure_raw.json'))}
out={}
for v in cfg:
    rgb,a=load(v['file'],v.get('crop')); ok=oklab_arr(rgb); L=ok[...,0]; C=np.hypot(ok[...,1],ok[...,2])
    h=np.degrees(np.arctan2(ok[...,2],ok[...,1]))%360
    fg=(a>=250)&~((L>=0.93)&(C<0.04)); n=int(fg.sum())
    if n==0: out[v['vid']]=dict(n=0); continue
    bins=[]
    for k in range(12):
        m=fg&(C>=0.06)&((h//30).astype(int)==k); s=m.sum()/n
        if s>=0.02: bins.append(dict(hue=f'{k*30}-{k*30+30}',share=round(float(s),3),hex=hexof(np.median(rgb[m],axis=0))))
    neu=[]
    for nm,a0,b0 in [('黑',0,.3),('深灰',.3,.55),('灰',.55,.8)]:
        m=fg&(C<0.04)&(L>=a0)&(L<b0); s=m.sum()/n
        if s>=0.02: neu.append(dict(name=nm,share=round(float(s),3),hex=hexof(np.median(rgb[m],axis=0))))
    # 跟去邊結果比：有哪個色相格在去邊結果裡沒有對應色（色相差>30°）
    fh=[oklch(g['hex'])[2] for g in raw[v['vid']]['chromatic']]
    miss=[b for b in bins if all(hue_diff(oklch(b['hex'])[2],x)>30 for x in fh)]
    fn=[g['name'] for g in raw[v['vid']]['neutral']]
    missn=[x for x in neu if not fn]
    out[v['vid']]=dict(n=n,raw_hue_bins=bins,raw_dark_neutral=neu,missed_hue=miss,missed_neutral=missn)
    if miss or missn: print(v['vid'],'漏彩:',[(b['hue'],b['share'],b['hex']) for b in miss],'漏無彩:',[(x['name'],x['share'],x['hex']) for x in missn])
json.dump(out,open(W+'data/measure_unfiltered.json','w'),ensure_ascii=False,indent=1)
