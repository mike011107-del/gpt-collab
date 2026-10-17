import json, sys, numpy as np
from PIL import Image, ImageFilter
S=48
def prep(gray):  # gray: PIL L image of a mark on white, any size
    a = 255 - np.asarray(gray, dtype=np.float32)
    ys,xs = np.nonzero(a>20)
    gray = gray.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1))
    w,h = gray.size; m=max(w,h)
    can = Image.new('L',(m,m),255); can.paste(gray,((m-w)//2,(m-h)//2))
    g = np.asarray(can.resize((S,S),Image.BOX),dtype=np.float32)/255
    gx = np.zeros_like(g); gy=np.zeros_like(g)
    gx[:,1:-1]=g[:,2:]-g[:,:-2]; gy[1:-1,:]=g[2:,:]-g[:-2,:]
    e = np.hypot(gx,gy)
    e = np.asarray(Image.fromarray((e/e.max()*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2)),dtype=np.float32)
    e -= e.mean(); n=np.linalg.norm(e); return (e/n).ravel() if n else e.ravel()
im = Image.open('sprite128.png').convert('L')
names=[l.strip().rsplit('/',1)[-1][:-4] for l in open('all.txt')]
cell,cols=128,59
V=[]
for i,n in enumerate(names):
    r,c=divmod(i,cols); V.append(prep(im.crop((c*cell,r*cell,(c+1)*cell,(r+1)*cell))))
V=np.stack(V); np.save('V.npy',V); json.dump(names,open('names.json','w'))
sim=V@V.T; np.fill_diagonal(sim,-1)
top10=np.sort(sim,axis=1)[:,-10:].mean(1); top1=sim.max(1)
json.dump({n:[float(a),float(b)] for n,a,b in zip(names,top1,top10)},open('crowd.json','w'))
print('top1 pct',np.percentile(top1,[10,25,50,75,90]).round(3)); print('top10 pct',np.percentile(top10,[10,25,50,75,90]).round(3))
