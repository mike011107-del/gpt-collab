import json, math, sys, collections
import numpy as np
sys.argv=['x']
exec(open('/tmp/claude-0/work/naming.py').read().split("if __name__=='__main__':")[0])
# 中文色族完整分布
def zh_full(h,k=60):
    p=oklab(hex2rgb(h)); dd=np.linalg.norm(UWP['zh']-p,axis=1); idx=np.argsort(dd)[:k]
    cnt=collections.Counter(zh_family(UWN['zh'][i]) for i in idx); n=sum(cnt.values())
    names=collections.Counter(UWN['zh'][i] for i in idx)
    return {w:v/n for w,v in cnt.most_common()}, [(w,v/k) for w,v in names.most_common(3)]
# 英文色族（c3）
src=open('/tmp/claude-0/work/naming_baseline.py').read()
i=src.index('FAM_EN'); j=src.index('def c3_family')
exec(src[i:j])
def en_fam(h):
    c,_=c3_index(h); row=T[c]; n=sum(row.values()); out=collections.Counter()
    for w,v in row.items():
        out[fam_en(terms[w])]+=v/n
    return dict(out.most_common())
cols=[('深青','#0C424A','崧淳候選'),('靛藍','#333D66','崧淳候選'),('工程黃（車身實測）','#D68702','崧淳輔色'),
      ('華通衛生行字樣','#005959','台灣同業'),('Ventia','#004127','國外同業'),('Siemens 石油青','#009999','長年單色'),
      ('Tiffany 藍','#81D8D0','長年單色'),('Vattenfall 藍','#2071B5','長年單色'),('Kanal-Türpe 橘','#FA8D02','國外同業'),
      ('Caterpillar 黃','#FFCD11','長年單色'),('Lanes 粉紅','#E40571','國外同業'),('Biffa 紅','#E42313','國外同業')]
out=[]
for nm,h,g in cols:
    z,zn=zh_full(h); e=en_fam(h)
    out.append(dict(name=nm,hex=h,group=g,zh=z,zh_names=zn,en=e))
    print(nm,h,{k:round(v,2) for k,v in list(z.items())[:4]},zn,{k:round(v,2) for k,v in list(e.items())[:3]})
json.dump(out,open('/tmp/claude-0/report/naming_fig.json','w'),ensure_ascii=False,indent=1)
