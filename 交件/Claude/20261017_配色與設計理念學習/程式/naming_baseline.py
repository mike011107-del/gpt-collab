import json, sys, random, math, collections
import numpy as np
sys.path.insert(0,'/tmp/claude-0/work')
from naming import *
FAM_EN=[('teal',['teal','turquoise','cyan','aqua','bluegreen','greenblue','seafoam']),('blue',['navy','blue','periwinkle','cerulean','cobalt','royal','denim']),
 ('green',['green','olive','lime','forest','mint','sage','chartreuse','emerald']),('purple',['purple','violet','lavender','indigo','plum','lilac','mauve','eggplant']),
 ('pink',['pink','magenta','fuchsia','salmon','rose','hotpink']),('red',['red','maroon','crimson','burgundy','wine','scarlet']),('orange',['orange','peach','rust','tangerine','pumpkin']),
 ('yellow',['yellow','mustard','gold','lemon']),('brown',['brown','tan','khaki','beige','chocolate','coffee','taupe','mud']),('grey',['grey','gray','slate','silver','charcoal']),('black',['black']),('white',['white','cream'])]
def fam_en(t):
    for f,ks in FAM_EN:
        if any(k in t for k in ks): return f
    return 'other'
def c3_family(h):
    c,_=c3_index(h); row=T[c]; n=sum(row.values()); cnt=collections.Counter()
    for w,v in row.items(): cnt[fam_en(terms[w])]+=v
    return [(f,v/n) for f,v in cnt.most_common(3)]
def summary(h):
    a=c3_name(h); f=c3_family(h); z=uw_name(h,'zh'); zf,_=zh_fam_dist(h)
    return dict(hex=h, en_sal=round(a['saliency'],3), en_top=a['top'][0], en_fam=f[0], en_fam2=f[1] if len(f)>1 else None, zh_top=z['top'][0], zh_fam=zf[0], zh_fam2=zf[1] if len(zf)>1 else None, zh_H=round(z['H'],2))
peers=json.load(open('/tmp/claude-0/work/peers.json'))['C']
groups={}
groups['國外48家logo主色']=[(c['key'],c['logo'][0]) for c in peers if c['logo']]
tw=json.load(open('/mnt/project-files/崧淳CI/_工作資料/選色/02_決選三組與同業色票.json'))['competitors']
seen=set(); twl=[]
for c in tw:
    r=hex2rgb(c['hex']); L,a,b=lab(r); C=math.hypot(a,b)
    if c['firm'] in seen or C<15: continue
    seen.add(c['firm']); twl.append((c['firm'],c['hex']))
twl+= [('華通衛生行字樣','#005959'),('積德','#1F532F'),('浩源','#0086BE')]
groups['台灣同業主色']=twl
groups['長年單色品牌']=[('Caterpillar','#FFCD11'),('John Deere','#367C2B'),('DHL','#FFCC00'),('Tiffany','#81D8D0'),('Lanes','#E40571'),('Kanal-Türpe','#FA8D02'),('Veolia','#E52028'),('Vattenfall藍','#2071B5'),('Siemens石油青','#009999'),('IKEA藍','#0058A3'),('Biffa','#E42313'),('Wise','#9FE870')]
groups['崧淳候選與舊色']=[('深青','#0C424A'),('靛藍','#333D66'),('工程黃(實車)','#D68702'),('冷灰','#788284'),('淺灰藍','#B6C5DF'),('舊水青','#086A74'),('舊空位青','#14A5B3'),('舊墨藍','#081C2F'),('舊松針綠','#395848'),('RAL1018螢幕值','#FACA30')]
out={}
for g,lst in groups.items():
    rows=[]
    for name,h in lst:
        s=summary(h); s['name']=name; rows.append(s)
    out[g]=rows
# random baselines
random.seed(7)
def rand_hex(): return '#%02X%02X%02X'%tuple(random.randint(0,255) for _ in range(3))
allr=[];dark=[]
while len(allr)<2000 or len(dark)<600:
    h=rand_hex(); r=hex2rgb(h); L,a,b=lab(r); C=math.hypot(a,b)
    s=c3_name(h)['saliency']; f=c3_family(h)[0][1]
    if len(allr)<2000: allr.append((s,f))
    if 25<=L<=45 and C>=15 and len(dark)<600: dark.append((s,f,h))
def stats(v): v=np.array(v); return dict(n=len(v), p25=round(float(np.percentile(v,25)),3), median=round(float(np.median(v)),3), p75=round(float(np.percentile(v,75)),3))
out['_基準']=dict(sRGB隨機_英文命名一致度=stats([x[0] for x in allr]), sRGB隨機_英文同色族比例=stats([x[1] for x in allr]),
  深色彩色_L25到45_C15以上_命名一致度=stats([x[0] for x in dark]), 深色彩色_同色族比例=stats([x[1] for x in dark]))
# zh baseline for dark chroma colours (subset 200 for speed)
zf=[zh_fam_dist(x[2])[0][0][1] for x in dark[:200]]
out['_基準']['深色彩色_中文同色族比例']=stats(zf)
zall=[zh_fam_dist(rand_hex())[0][0][1] for _ in range(300)]
out['_基準']['sRGB隨機_中文同色族比例']=stats(zall)
json.dump(out,open('/tmp/claude-0/work/naming_results.json','w'),ensure_ascii=False,indent=1)
for g,rows in out.items():
    print('==',g)
    if g=='_基準': print(json.dumps(rows,ensure_ascii=False,indent=0)); continue
    for s in rows:
        print(f"{s['name'][:16]:16s} {s['hex']} 英一致{s['en_sal']:.2f} 英族{s['en_fam'][0]}{s['en_fam'][1]:.0%} 次{(s['en_fam2'] or ('-',0))[0]}{(s['en_fam2'] or ('-',0))[1]:.0%} | 中:{s['zh_top'][0]}{s['zh_top'][1]:.0%} 族{s['zh_fam'][0]}{s['zh_fam'][1]:.0%} 次{(s['zh_fam2'] or ('-',0))[0]}{(s['zh_fam2'] or ('-',0))[1]:.0%}")
