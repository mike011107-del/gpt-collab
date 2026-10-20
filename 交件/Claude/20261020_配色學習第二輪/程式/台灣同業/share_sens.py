# 多色 logo 第二色占比的敏感度：定案值（measure_final）對照「不去邊、每個不透明非白像素分給最近的種子色（OKLab）」
# 種子＝tw_peers 的彩色＋黑白灰（含併掉的漸層端色）。輸出 data/share_sensitivity.json
# 用法：python3 -I /tmp/claude-0/r2/tw/work/share_sens.py
import sys, json, numpy as np
sys.path.insert(0,'/tmp/claude-0/r2/tw/work')
from measure import load, oklab_arr
W='/tmp/claude-0/r2/tw/'
cfg={v['vid']:v for v in json.load(open(W+'work/logos.json'))}
TW=json.load(open(W+'tw_peers.json'))
def rgbh(h): return np.array([[int(h[1:3],16),int(h[3:5],16),int(h[5:7],16)]],float)
out={}
for t in TW:
    if not t['cols'] or len(t['cols'])<2: continue
    v=cfg[t['vid']]; rgb,a=load(v['file'],v.get('crop')); ok=oklab_arr(rgb); L=ok[...,0]; C=np.hypot(ok[...,1],ok[...,2])
    fg=(a>=250)&~((L>=0.93)&(C<0.04)); px=ok[fg]
    seeds=[(c['hex'],'彩',i) for i,c in enumerate(t['cols'])]+[(c['merged'],'彩',i) for i,c in enumerate(t['cols']) if c.get('merged')]
    seeds+=[(n['hex'],'無彩',None) for n in t['neutral'] if n['hex']!='#FFFFFF']
    S=np.array([oklab_arr(rgbh(h))[0] for h,_,_ in seeds])
    nn=np.linalg.norm(px[:,None,:]-S[None],axis=2).argmin(1)
    sh=[0.0]*len(t['cols'])
    for j,(h,k,i) in enumerate(seeds):
        if k=='彩': sh[i]+=float((nn==j).mean())
    fin=[c['share'] for c in t['cols']]
    o=np.argsort(fin)[::-1]
    out[t['company']]=dict(vid=t['vid'],method=t['share_method'],hex=[t['cols'][i]['hex'] for i in o],
        定案占比=[round(fin[i],4) for i in o],不去邊最近色占比=[round(sh[i],4) for i in o],
        第二色_定案=round(fin[o[1]],4),第二色_不去邊=round(sh[o[1]],4))
    print(t['company'],out[t['company']]['hex'],out[t['company']]['定案占比'],out[t['company']]['不去邊最近色占比'])
json.dump(out,open(W+'data/share_sensitivity.json','w'),ensure_ascii=False,indent=1)
