# 色名可說性：英文用 Heer & Stone c3 (XKCD) 模型；中文、英文另用 uwdata 多語色名原始資料做近鄰統計
import json, math, csv, collections, sys
import numpy as np
C3='/tmp/claude-0/src/c3/data/xkcd/c3_data.json'
UW='/tmp/claude-0/src/cn-lang/model/cleaned_color_names.csv'

def srgb2lin(c):
    c=c/255.0
    return np.where(c<=0.04045, c/12.92, ((c+0.055)/1.055)**2.4)
def hex2rgb(h): h=h.lstrip('#'); return np.array([int(h[i:i+2],16) for i in (0,2,4)],float)
M=np.array([[0.4124564,0.3575761,0.1804375],[0.2126729,0.7151522,0.0721750],[0.0193339,0.1191920,0.9503041]])
def lab(rgb):
    xyz=M@srgb2lin(np.asarray(rgb,float))
    wn=np.array([0.950470,1.0,1.088830]); t=xyz/wn
    f=np.where(t>(6/29)**3, np.cbrt(t), t/(3*(6/29)**2)+4/29)
    return np.array([116*f[1]-16, 500*(f[0]-f[1]), 200*(f[1]-f[2])])
def oklab(rgb):
    l=srgb2lin(np.asarray(rgb,float))
    M1=np.array([[0.4122214708,0.5363325363,0.0514459929],[0.2119034982,0.6806995451,0.1073969566],[0.0883024619,0.2817188376,0.6299787005]])
    M2=np.array([[0.2104542553,0.7936177850,-0.0040720468],[1.9779984951,-2.4285922050,0.4505937099],[0.0259040371,0.7827717662,-0.8086757660]])
    lms=np.cbrt(M1@l); return M2@lms

# ---- c3 ----
d=json.load(open(C3)); terms=d['terms']; W=len(terms)
cols=np.array(d['color']).reshape(-1,3)
T=collections.defaultdict(dict)
for i in range(0,len(d['T']),2):
    idx=d['T'][i]; v=d['T'][i+1]; T[idx//W][idx%W]=v
key={tuple(c):i for i,c in enumerate(cols.tolist())}
def c3_index(h):
    L,a,b=lab(hex2rgb(h)); k=(5*round(L/5),5*round(a/5),5*round(b/5))
    if k in key and key[k] in T: return key[k], 0.0
    # nearest bin with data
    dd=np.linalg.norm(cols-np.array([L,a,b]),axis=1)
    for i in np.argsort(dd):
        if i in T: return int(i), float(dd[i])
def c3_name(h, top=3):
    c,dist=c3_index(h); row=T[c]; n=sum(row.values())
    H=sum((v/n)*math.log2(v/n) for v in row.values())
    sal=(H+4.5)/4.5
    tt=sorted(row.items(), key=lambda x:-x[1])[:top]
    return dict(n=n, H=-H, saliency=sal, top=[(terms[w], v/n) for w,v in tt], bin_dist=dist)

# ---- uwdata ----
T2S=str.maketrans('綠藍紅淺黃鮮螢寶磚銀鐵銅葉軍鴨蘋檸欖薑灣濃艷豔棗紺翡鈷鐵灰','绿蓝红浅黄鲜荧宝砖银铁铜叶军鸭苹柠榄姜湾浓艳艳枣绀翡钴铁灰')
uw={'zh':[], 'en':[]}
with open(UW,encoding='utf-8') as f:
    for r in csv.DictReader(f):
        lg=r['langAbv']
        if lg in uw and r['rgbSet']=='full' and r['colorSpace']=='rgb':
            nm=r['standardized_entered_name'].strip()
            if lg=='zh': nm=nm.translate(T2S)
            uw[lg].append((nm, oklab(np.array([float(r['r']),float(r['g']),float(r['b'])]))))
UWP={lg:np.array([p for _,p in v]) for lg,v in uw.items()}
UWN={lg:[n for n,_ in v] for lg,v in uw.items()}
def uw_name(h, lg, k=40, top=4):
    p=oklab(hex2rgb(h)); dd=np.linalg.norm(UWP[lg]-p,axis=1); idx=np.argsort(dd)[:k]
    cnt=collections.Counter(UWN[lg][i] for i in idx); n=sum(cnt.values())
    H=-sum((v/n)*math.log2(v/n) for v in cnt.values())
    return dict(k=k, radius=float(dd[idx[-1]]), H=H, top=[(w,v/n) for w,v in cnt.most_common(top)])

# 中文主色族
def zh_family(nm):
    s=nm
    if any(x in s for x in ['黑']): return '黑'
    if '灰' in s and not any(x in s for x in ['蓝','绿','紫','青']): return '灰'
    if any(x in s for x in ['蓝绿','青绿','湖绿','孔雀','碧','翡','松石','绿松']): return '蓝绿'
    if '青' in s and not any(x in s for x in ['藏青','青蓝','靛青']): return '青'
    if any(x in s for x in ['藏青','海军','靛','蓝','湛']): return '蓝'
    if any(x in s for x in ['绿','翠','橄榄','军']): return '绿'
    if any(x in s for x in ['紫']): return '紫'
    if any(x in s for x in ['橙','橘','杏']): return '橙'
    if any(x in s for x in ['黄','金','姜','土']): return '黄'
    if any(x in s for x in ['棕','褐','咖啡','茶','巧克力','赭']): return '棕'
    if any(x in s for x in ['红','粉','玫','桃','品']): return '红粉'
    return '其他'
def zh_fam_dist(h,k=60):
    p=oklab(hex2rgb(h)); dd=np.linalg.norm(UWP['zh']-p,axis=1); idx=np.argsort(dd)[:k]
    cnt=collections.Counter(zh_family(UWN['zh'][i]) for i in idx); n=sum(cnt.values())
    return [(w,v/n) for w,v in cnt.most_common(3)], float(dd[idx[-1]])

if __name__=='__main__':
    for h in sys.argv[1:]:
        print(h, c3_name(h), uw_name(h,'zh'), zh_fam_dist(h), uw_name(h,'en',k=200))
