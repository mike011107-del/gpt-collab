import sys, json, numpy as np
from PIL import Image
im = np.asarray(Image.open(sys.argv[1]).convert('L'), dtype=np.float32)/255.0
names = [l.strip().rsplit('/',1)[-1][:-4] for l in open(sys.argv[2])]
cell = int(sys.argv[3]); cols = int(sys.argv[4])
out = {}
def resize(a, s, mode):
    return np.asarray(Image.fromarray((a*255).astype(np.uint8)).resize((s,s), mode), dtype=np.float32)/255.0
for i,n in enumerate(names):
    r, c = divmod(i, cols)
    a = 1.0 - im[r*cell:(r+1)*cell, c*cell:(c+1)*cell]   # ink = 1
    if a.sum() < 1: continue
    sst = ((a - a.mean())**2).sum()
    res = {}
    for s in (16, 24, 32):
        small = resize(a, s, Image.BOX)
        back = resize(small, cell, Image.BILINEAR)
        res[f'r2_{s}'] = float(1 - ((a-back)**2).sum()/sst)
    b = a > 0.5
    ys, xs = np.nonzero(b)
    h = ys.max()-ys.min()+1; w = xs.max()-xs.min()+1
    # perimeter: count edge transitions
    per = (b[1:,:]!=b[:-1,:]).sum() + (b[:,1:]!=b[:,:-1]).sum()
    area = b.sum()
    res.update(ink=float(area/(h*w)), aspect=float(w/h), compact=float(per**2/(4*np.pi*area)) if area else 0)
    out[n] = res
json.dump(out, open(sys.argv[5],'w'))
print(len(out))
