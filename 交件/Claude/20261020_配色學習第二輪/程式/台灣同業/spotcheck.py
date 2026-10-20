# 抽查 measure.py：不用去邊，直接數非白像素的明度、彩度分布，對照舊結果
import sys, json, numpy as np
sys.path.insert(0,'/tmp/claude-0/r2/tw/work')
from measure import load, oklab_arr, hexof
cfg={v['vid']:v for v in json.load(open('/tmp/claude-0/r2/tw/work/logos.json'))}
for vid in sys.argv[1:]:
    v=cfg[vid]; rgb,a=load(v['file'],v.get('crop'))
    ok=oklab_arr(rgb); L=ok[...,0]; C=np.hypot(ok[...,1],ok[...,2]); h=np.degrees(np.arctan2(ok[...,2],ok[...,1]))%360
    fg=(a>=250)&~((L>=0.93)&(C<0.04)); n=fg.sum()
    neu=fg&(C<0.04); chm=fg&(C>=0.04)
    print(vid,'前景',n,'無彩',round(neu.sum()/n,3),'彩色',round(chm.sum()/n,3))
    # 無彩依明度
    for a0,b0 in [(0,.3),(.3,.55),(.55,.8),(.8,.93)]:
        m=neu&(L>=a0)&(L<b0)
        if m.sum(): print('  無彩L',a0,b0,round(m.sum()/n,3),hexof(np.median(rgb[m],axis=0)))
    hb=(h//30).astype(int)
    for k in range(12):
        m=chm&(hb==k)
        if m.sum()/n>0.01: print('  色相',k*30,'-',k*30+30,round(m.sum()/n,3),hexof(np.median(rgb[m],axis=0)),'C中位',round(float(np.median(C[m])),3))
