# 台灣對國外比較：分組占比、彩色數量、多色 ΔL*、漸層、主色色相、深青／靛藍 ΔE2000
# 國外 48 家與台灣用同一支 scheme()（OKLCH 最大色相差）
import json, sys, math, random, statistics as st, collections, itertools
import numpy as np
sys.path.insert(0,'/tmp/claude-0/r2/tw/work')
from ct import oklch, lab, de, hue_diff
from schemes import scheme, ORDER
from tw_decide import hue_bin
W='/tmp/claude-0/r2/tw/'
F=json.load(open('/tmp/claude-0/work/peer_schemes.json'))
TW=json.load(open(W+'tw_peers.json'))
TWc=[t for t in TW if t['cols'] is not None]            # 20 家（去掉墨色商標）
TWo=[t for t in TWc if t['own_logo']]                    # 官網 logo 檔 14 家
def dist(items,getcols):
    c=collections.Counter(scheme(getcols(x)) for x in items); n=len(items)
    return {k:[c[k],round(c[k]/n,3)] for k in ORDER}
def ncount(items,getcols):
    c=collections.Counter(min(len(getcols(x)),4) for x in items); return {('4+' if k==4 else str(k)):c[k] for k in range(5)}
def dLs(items,getcols):
    return [max(lab(h)[0] for h in getcols(x))-min(lab(h)[0] for h in getcols(x)) for x in items if len(getcols(x))>=2]
fc=lambda x:x['cols']; tc=lambda t:[c['hex'] for c in t['cols']]
R={}
R['樣本']=dict(國外=len(F),台灣全部可計色=len(TWc),台灣官網logo檔=len(TWo),
  說明='台灣 21 家有圖；順捷只有智財局墨色商標，不計色。官網 logo 檔＝排除 banner 字卡（邦盛、康立）、智財局圖樣（積德）、第三方頁（九升、派浦崴洱、龍祥）。')
R['分組']=dict(國外=dist(F,fc),台灣全部=dist(TWc,tc),台灣官網=dist(TWo,tc))
R['分組_前兩色規則']=dict(國外={k:v for k,v in collections.Counter(scheme(x['cols'],'first2') for x in F).items()},
                    台灣全部={k:v for k,v in collections.Counter(scheme(tc(t),'first2') for t in TWc).items()})
R['彩色數量']=dict(國外=ncount(F,fc),台灣全部=ncount(TWc,tc),台灣官網=ncount(TWo,tc))
# Fisher 精確檢定（雙尾）：「一個彩色」比例、「多色裡對比」比例
def fisher(a,b,c,d):
    n=a+b+c+d; r1=a+b; c1=a+c
    def p(x): return math.comb(r1,x)*math.comb(n-r1,c1-x)/math.comb(n,c1)
    p0=p(a); return round(sum(p(x) for x in range(max(0,c1-(n-r1)),min(r1,c1)+1) if p(x)<=p0*(1+1e-9)),3)
def cnt(items,getcols,k): return sum(scheme(getcols(x))==k for x in items)
a=cnt(TWc,tc,'一個彩色'); c_=cnt(F,fc,'一個彩色')
R['檢定_一個彩色']=dict(台灣=f'{a}/{len(TWc)}',國外=f'{c_}/{len(F)}',fisher_p=fisher(a,len(TWc)-a,c_,len(F)-c_))
mt=[t for t in TWc if len(t['cols'])>=2]; mf=[x for x in F if len(x['cols'])>=2]
a=sum(scheme(tc(t))=='對比' for t in mt); c_=sum(scheme(x['cols'])=='對比' for x in mf)
R['檢定_多色裡對比']=dict(台灣=f'{a}/{len(mt)}',國外=f'{c_}/{len(mf)}',fisher_p=fisher(a,len(mt)-a,c_,len(mf)-c_))
# ΔL*
dT=dLs(TWc,tc); dF=dLs(F,fc)
rng=random.Random(20261018)
def rand_chrom():
    while True:
        h='#%02X%02X%02X'%tuple(rng.randint(0,255) for _ in range(3))
        if oklch(h)[1]>=0.04: return h
rp=[abs(lab(rand_chrom())[0]-lab(rand_chrom())[0]) for _ in range(5000)]
poolT=[h for t in mt for h in tc(t)]; poolF=[h for x in mf for h in x['cols']]
def shuf(pool,k=5000):
    out=[]
    for _ in range(k):
        a,b=rng.sample(pool,2); out.append(abs(lab(a)[0]-lab(b)[0]))
    return out
sT=shuf(poolT); sF=shuf(poolF)
# 置換檢定：台灣與國外 ΔL* 中位數差
allv=dT+dF; obs=st.median(dF)-st.median(dT); k=0; NP=20000
for _ in range(NP):
    rng.shuffle(allv)
    if st.median(allv[len(dT):])-st.median(allv[:len(dT)])>=obs: k+=1
pc=lambda v:round(sum(x>=26 for x in v)/len(v),3)
R['明度差ΔL*']=dict(定義='同一 logo 各彩色 CIELAB L* 的最大減最小（重現上輪 19 家中位 32.1、13 家 ≥26）',
  台灣=dict(n=len(dT),中位=round(st.median(dT),1),值=[round(v,1) for v in dT],至少26比例=pc(dT)),
  國外=dict(n=len(dF),中位=round(st.median(dF),1),至少26比例=pc(dF),值=[round(v,1) for v in dF],家=[x['name'] for x in F if len(x['cols'])>=2]),
  隨機兩彩色=dict(n=len(rp),中位=round(st.median(rp),1),至少26比例=pc(rp),種子=20261018),
  台灣色打亂重配=dict(中位=round(st.median(sT),1),至少26比例=pc(sT)),
  國外色打亂重配=dict(中位=round(st.median(sF),1),至少26比例=pc(sF)),
  置換檢定_國外中位減台灣中位=dict(差=round(obs,1),單尾p=round(k/NP,3),次數=NP))
# 敏感度：去掉積德（商標圖樣）、只看官網 logo 檔
dTo=dLs(TWo,tc)
R['明度差ΔL*']['台灣官網']=dict(n=len(dTo),中位=round(st.median(dTo),1) if dTo else None,值=[round(v,1) for v in dTo])
R['明度差ΔL*']['台灣家名']=[t['company'] for t in TWc if len(t['cols'])>=2]
# 漸層
gT=[t['company'] for t in TWc if t['gradient']]; gTo=[t['company'] for t in TWo if t['gradient']]
R['漸層']=dict(台灣全部=dict(n=len(gT),共=len(TWc),比例=round(len(gT)/len(TWc),3),家=gT),
  台灣官網=dict(n=len(gTo),共=len(TWo),比例=round(len(gTo)/len(TWo),3),家=gTo),
  國外=dict(n=4,共=48,比例=round(4/48,3),家=['Scottish Water','Uisce Éireann','日本水工設計','Mini-Cam'],
    說明='上輪 peers.json 文字有寫「漸層」的家數；上輪沒有逐家記漸層，只能當下限。國外 logo 原圖不在雲端，這輪沒重看。'))
R['漸層']['檢定_台灣全部對國外下限']=dict(fisher_p=fisher(len(gT),len(TWc)-len(gT),4,44),說明='國外 4/48 只是下限，p 值只當參考')
R['漸層']['檢定_台灣官網對國外下限']=dict(fisher_p=fisher(len(gTo),len(TWo)-len(gTo),4,44))
# 主色色相
hbT=collections.Counter(hue_bin(oklch(t['main'])[2]) for t in TWc if t['main'])
hbF=collections.Counter(hue_bin(oklch(x['cols'][0])[2]) for x in F if x['cols'])
order=['紅','橘','黃','綠','青','藍','紫']
R['主色色相']=dict(分格='OKLCH h：紅 345–40、橘 40–70、黃 70–110、綠 110–170、青 170–225、藍 225–285、紫 285–345；台灣主色＝占比最大的彩色，國外＝peer_schemes 第一色',
  台灣={k:hbT[k] for k in order},台灣有彩色家數=sum(hbT.values()),國外={k:hbF[k] for k in order},國外有彩色家數=sum(hbF.values()))
nT=sum(hbT.values()); nF=sum(hbF.values())
R['主色色相']['綠青藍合計']=dict(台灣=f"{hbT['綠']+hbT['青']+hbT['藍']}/{nT}",國外=f"{hbF['綠']+hbF['青']+hbF['藍']}/{nF}",
  fisher_p=fisher(hbT['綠']+hbT['青']+hbT['藍'],nT-(hbT['綠']+hbT['青']+hbT['藍']),hbF['綠']+hbF['青']+hbF['藍'],nF-(hbF['綠']+hbF['青']+hbF['藍'])))
R['主色色相']['綠']=dict(台灣=f"{hbT['綠']}/{nT}",國外=f"{hbF['綠']}/{nF}",fisher_p=fisher(hbT['綠'],nT-hbT['綠'],hbF['綠'],nF-hbF['綠']))
# 主色 OKLCH 明度、彩度
LT=[oklch(t['main'])[0] for t in TWc if t['main']]; LF=[oklch(x['cols'][0])[0] for x in F if x['cols']]
CT=[oklch(t['main'])[1] for t in TWc if t['main']]; CF=[oklch(x['cols'][0])[1] for x in F if x['cols']]
R['主色明度彩度']=dict(台灣=dict(OKLCH_L中位=round(st.median(LT),3),C中位=round(st.median(CT),3)),國外=dict(OKLCH_L中位=round(st.median(LF),3),C中位=round(st.median(CF),3)))
# 字型、圖形（目視）
R['字型_目視']=dict(collections.Counter(t['font_cls'] for t in TW))
R['圖形題材_目視']=dict(collections.Counter(m for t in TW for m in t['motif_cls']))
# 深青、靛藍 ΔE2000
cand={'深青 #0C424A':'#0C424A','靛藍 #333D66':'#333D66'}
rows=[]
for t in TW:
    for vid_cols in ([(t['vid'],c['hex'],c['share']) for c in (t['cols'] or [])]):
        rows.append(dict(company=t['company'],vid=vid_cols[0],hex=vid_cols[1],share=vid_cols[2],is_main=(vid_cols[1]==t['main'])))
raw={r['vid']:r for r in json.load(open(W+'data/measure_raw.json'))}
for t in TW:
    for a in t['alt']:
        if a in ('bangsheng_slogan',): pass
        for gg in raw[a]['chromatic']:
            if gg['share']>=0.05: rows.append(dict(company=t['company'],vid=a,hex=gg['hex'],share=gg['share'],is_main=False,alt=True))
R['候選色距離']={}
for nm,hx in cand.items():
    mains=sorted([dict(company=t['company'],hex=t['main'],dE=round(de(hx,t['main']),1)) for t in TWc if t['main']],key=lambda r:r['dE'])
    allc=sorted([dict(r,dE=round(de(hx,r['hex']),1)) for r in rows],key=lambda r:r['dE'])
    R['候選色距離'][nm]=dict(主色最近三家=mains[:3],主色全部=mains,含其他版本與次色最近五筆=allc[:5],
        十以內家數_主色=sum(r['dE']<10 for r in mains))
# 主色色相逐家（給畫圖）
R['主色逐家']=dict(台灣=[dict(company=t['company'],hex=t['main'],h=round(oklch(t['main'])[2],1),L=round(oklch(t['main'])[0],3),C=round(oklch(t['main'])[1],3)) for t in TWc if t['main']],
  國外=[dict(name=x['name'],hex=x['cols'][0],h=round(oklch(x['cols'][0])[2],1),L=round(oklch(x['cols'][0])[0],3),C=round(oklch(x['cols'][0])[1],3)) for x in F if x['cols']])
json.dump(R,open(W+'comparison.json','w'),ensure_ascii=False,indent=1)
for k in ['分組','彩色數量','檢定_一個彩色','檢定_多色裡對比','明度差ΔL*','漸層','主色色相','主色明度彩度','字型_目視','圖形題材_目視']:
    print(k,json.dumps(R[k],ensure_ascii=False)[:900])
for nm in cand: print(nm,R['候選色距離'][nm]['主色最近三家'],R['候選色距離'][nm]['含其他版本與次色最近五筆'][:3])
