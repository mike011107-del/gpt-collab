import json, numpy as np
from PIL import Image, ImageFilter
sp=Image.open('sprite128.png').convert('L'); names=json.load(open('names.json')); met=json.load(open('si_metrics.json'))
cell,cols=128,59
def fine(img,k=9):
    # ink=white for filters
    ink=img.point(lambda p:255 if p<128 else 0)
    opened=ink.filter(ImageFilter.MinFilter(k)).filter(ImageFilter.MaxFilter(k))
    closed=ink.filter(ImageFilter.MaxFilter(k)).filter(ImageFilter.MinFilter(k))
    a=np.asarray(ink)>0; o=np.asarray(opened)>0; c=np.asarray(closed)>0
    lost_ink=(a&~o).sum()/max(a.sum(),1); filled_gap=(c&~a).sum()/max(a.sum(),1)
    return float(lost_ink), float(filled_gap)
out={}
for i,n in enumerate(names):
    if not (0.8<=met[n]['aspect']<=1.25): continue
    r,c=divmod(i,cols); li,fg=fine(sp.crop((c*cell,r*cell,(c+1)*cell,(r+1)*cell)))
    out[n]=dict(lost=li,filled=fg,fine=li+fg,r16=met[n]['r2_16'])
json.dump(out,open('fine.json','w'))
f=np.array([v['fine'] for v in out.values()]); r=np.array([v['r16'] for v in out.values()])
from numpy import corrcoef
rank=lambda x: np.argsort(np.argsort(x))
print('n',len(out),'spearman fine vs r16', round(corrcoef(rank(f),rank(r))[0,1],3))
q=np.percentile(f,[25,50,75]); print('fine pct',q.round(3))
for lo,hi in [(0,0.05),(0.05,0.15),(0.15,0.3),(0.3,9)]:
    m=(f>=lo)&(f<hi); print(f'fine {lo}-{hi}: n={m.sum()} median r16={np.median(r[m]):.3f}')
for n in ['deutschebank','chase','mitsubishi','lufthansa','shell','target','apple']:
    print(n, {k:round(v,3) for k,v in out[n].items()})
# drafts
for L in 'ABC':
    im=Image.open(f'{L}_flat.png').convert('L'); g=im.point(lambda p:255 if p<245 else 0); b=g.getbbox(); im=im.crop(b)
    w,h=im.size; m=max(w,h); can=Image.new('L',(m,m),255); can.paste(im,((m-w)//2,(m-h)//2)); can=can.resize((128,128),Image.BOX)
    print('draft',L, [round(x,3) for x in fine(can)])
