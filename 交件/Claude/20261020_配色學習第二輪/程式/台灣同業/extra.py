# 補充數字：紅色主色檢定、華通車槽與 logo 綠色相、彩色面積占比、多色組合
import json, sys, statistics as st
sys.path.insert(0,'/tmp/claude-0/r2/tw/work')
from ct import oklch
from analyze import fisher   # 會重跑 analyze（不寫新東西以外的檔）
W='/tmp/claude-0/r2/tw/'
R=json.load(open(W+'comparison.json')); TW=json.load(open(W+'tw_peers.json'))
raw={r['vid']:r for r in json.load(open(W+'data/measure_final.json'))}   # 第三次修正：原讀 measure_raw.json（去邊壓低細字），舊版 work/extra_v1.py
SENS=json.load(open(W+'data/share_sensitivity.json'))
hT=R['主色色相']['台灣']; hF=R['主色色相']['國外']; nT=R['主色色相']['台灣有彩色家數']; nF=R['主色色相']['國外有彩色家數']
E={}
E['紅主色']=dict(台灣=f"{hT['紅']}/{nT}",國外=f"{hF['紅']}/{nF}",fisher_p=fisher(hT['紅'],nT-hT['紅'],hF['紅'],nF-hF['紅']))
E['暖色主色_紅橘黃']=dict(台灣=f"{hT['紅']+hT['橘']+hT['黃']}/{nT}",國外=f"{hF['紅']+hF['橘']+hF['黃']}/{nF}")
E['華通車槽對logo綠色相']=dict(logo綠=[round(v,3) for v in oklch('#2D661F')],車槽=[round(v,3) for v in oklch('#98C268')])
cs={t['company']:raw[t['vid']]['chromatic_share'] for t in TW if t['cols']}
E['彩色面積占比']=dict(定義='measure_final chromatic_share：logo 非白像素中 C≥0.04 的比例；華通、逸居、浩源等純色無反鋸齒的圖逐像素直接計數，其餘用去邊後像素（banner 字卡與白字版不準）',
  逐家=cs,中位=round(st.median(cs.values()),3),低於三成=[k for k,v in cs.items() if v<0.3])
pairs=[]
for t in TW:
    if t['cols'] and len(t['cols'])>=2:
        cs=sorted(t['cols'],key=lambda c:-c['share']); sv=SENS[t['company']]
        pairs.append(dict(company=t['company'],bins=[c['hue_bin'] for c in cs],hex=[c['hex'] for c in cs],share=[c['share'] for c in cs],
            second_share=cs[1]['share'],second_share_unfiltered=sv['第二色_不去邊'],share_method=t['share_method'],
            second_lt_10pct=max(cs[1]['share'],sv['第二色_不去邊'])<0.10))
E['多色組合']=pairs
two=[p for p in pairs if len(p['bins'])==2]
cool={'藍','綠','青'}; warm={'紅','橘'}
bgw=[p for p in two if (set(p['bins'])&cool) and (set(p['bins'])&warm)]
E['兩色logo第二色占比']=dict(說明='第二色占 logo 非白像素比例；second_share 是定案值，second_share_unfiltered 是不去邊最近色分法，兩種都 <10% 才算「<10%」',
  兩色家數=len(two),第二色小於10=[p['company'] for p in two if p['second_lt_10pct']],第二色至少10=[p['company'] for p in two if not p['second_lt_10pct']],
  藍綠配紅橘=[p['company'] for p in bgw],藍綠配紅橘且紅橘小於10=[p['company'] for p in bgw if p['second_lt_10pct'] and p['bins'][1] in warm],
  藍綠配紅橘且紅橘至少10=[p['company'] for p in bgw if not (p['second_lt_10pct'] and p['bins'][1] in warm)])
json.dump(E,open(W+'data/extra.json','w'),ensure_ascii=False,indent=1)
print(json.dumps(E,ensure_ascii=False))
