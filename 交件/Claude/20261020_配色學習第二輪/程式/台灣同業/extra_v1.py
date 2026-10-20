# 補充數字：紅色主色檢定、華通車槽與 logo 綠色相、彩色面積占比、多色組合
import json, sys, statistics as st
sys.path.insert(0,'/tmp/claude-0/r2/tw/work')
from ct import oklch
from analyze import fisher   # 會重跑 analyze（不寫新東西以外的檔）
W='/tmp/claude-0/r2/tw/'
R=json.load(open(W+'comparison.json')); TW=json.load(open(W+'tw_peers.json'))
raw={r['vid']:r for r in json.load(open(W+'data/measure_raw.json'))}
hT=R['主色色相']['台灣']; hF=R['主色色相']['國外']; nT=R['主色色相']['台灣有彩色家數']; nF=R['主色色相']['國外有彩色家數']
E={}
E['紅主色']=dict(台灣=f"{hT['紅']}/{nT}",國外=f"{hF['紅']}/{nF}",fisher_p=fisher(hT['紅'],nT-hT['紅'],hF['紅'],nF-hF['紅']))
E['暖色主色_紅橘黃']=dict(台灣=f"{hT['紅']+hT['橘']+hT['黃']}/{nT}",國外=f"{hF['紅']+hF['橘']+hF['黃']}/{nF}")
E['華通車槽對logo綠色相']=dict(logo綠=[round(v,3) for v in oklch('#2D661F')],車槽=[round(v,3) for v in oklch('#98C268')])
cs={t['company']:raw[t['vid']]['chromatic_share'] for t in TW if t['cols']}
E['彩色面積占比']=dict(定義='measure_raw chromatic_share：去邊後 logo 像素中 C≥0.04 的比例（banner 字卡與白字版不準）',
  逐家=cs,中位=round(st.median(cs.values()),3),低於三成=[k for k,v in cs.items() if v<0.3])
pairs=[]
for t in TW:
    if t['cols'] and len(t['cols'])>=2:
        pairs.append(dict(company=t['company'],bins=[c['hue_bin'] for c in t['cols']],second_share=sorted(c['share'] for c in t['cols'])[-2]))
E['多色組合']=pairs
json.dump(E,open(W+'data/extra.json','w'),ensure_ascii=False,indent=1)
print(json.dumps(E,ensure_ascii=False))
