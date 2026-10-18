import json, numpy as np
from PIL import Image
sp=np.asarray(Image.open('sprite128.png').convert('L'),dtype=np.float32)/255
names=json.load(open('names.json')); crowd=json.load(open('crowd.json')); met=json.load(open('si_metrics.json'))
cell,cols=128,59
yy,xx=np.mgrid[0:cell,0:cell]; cx=cy=(cell-1)/2; rr=np.hypot(yy-cy,xx-cx)
out={}
for i,n in enumerate(names):
    r,c=divmod(i,cols); a=(1-sp[r*cell:(r+1)*cell,c*cell:(c+1)*cell])>0.5
    if met[n]['aspect']<0.9 or met[n]['aspect']>1.11: continue
    ring_c=(rr>58)&(rr<62.5); circ=a[ring_c].mean()
    b=np.zeros_like(a); b[1:4,:]=b[-4:-1,:]=b[:,1:4]=b[:,-4:-1]=True
    # rounded corners: ignore 12px corners
    k=14; b[:k,:k]=b[:k,-k:]=b[-k:,:k]=b[-k:,-k:]=False
    sq=a[b].mean()
    out[n]=dict(circle=float(circ),square=float(sq),container=bool(max(circ,sq)>0.9),
                crowd=crowd[n][1],r16=met[n]['r2_16'])
json.dump(out,open('container.json','w'))
C=[v for v in out.values() if v['container']]; N=[v for v in out.values() if not v['container']]
f=lambda L,k: np.percentile([v[k] for v in L],[25,50,75]).round(3)
print('square-ish n',len(out),'container',len(C),'none',len(N))
print('crowd  container',f(C,'crowd'),' none',f(N,'crowd'))
print('r2_16  container',f(C,'r16'),' none',f(N,'r16'))
# bootstrap CI for median difference
rng=np.random.default_rng(0); a=np.array([v['crowd'] for v in C]); b=np.array([v['crowd'] for v in N])
d=[np.median(rng.choice(a,len(a)))-np.median(rng.choice(b,len(b))) for _ in range(2000)]
print('crowd median diff 95%CI',np.percentile(d,[2.5,97.5]).round(3))
a=np.array([v['r16'] for v in C]); b=np.array([v['r16'] for v in N])
d=[np.median(rng.choice(a,len(a)))-np.median(rng.choice(b,len(b))) for _ in range(2000)]
print('r16 median diff 95%CI',np.percentile(d,[2.5,97.5]).round(3))
for n in ['chase','deutschebank','mitsubishi','target','lufthansa','shell','apple','mcdonalds','deutschetelekom','volvo','bmw','starbucks','uniqlo']:
    if n in out: print(n,{k:(round(v,2) if isinstance(v,float) else v) for k,v in out[n].items()})
