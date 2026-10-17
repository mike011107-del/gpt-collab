import json, numpy as np
from PIL import Image, ImageFilter, ImageDraw
def depthmap(mask):  # mask: bool array, returns erosion depth
    img=Image.fromarray((mask*255).astype(np.uint8)); d=np.zeros(mask.shape,np.int32); k=0
    while True:
        a=np.asarray(img)>0
        if not a.any() or k>60: break
        d[a]+=1; img=img.filter(ImageFilter.MinFilter(3)); k+=1
    return d
def ridge_cv(d):
    if d.max()==0: return None
    p=np.pad(d,1); nb=np.stack([p[1+dy:1+dy+d.shape[0],1+dx:1+dx+d.shape[1]] for dy in(-1,0,1) for dx in(-1,0,1) if (dy,dx)!=(0,0)])
    r=(d>0)&(d>=nb.max(0)); v=d[r].astype(float)
    return float(v.std()/v.mean()) if len(v)>3 else None
def measure(gray):  # PIL L 128x128, ink dark
    a=np.asarray(gray)<128
    ink=ridge_cv(depthmap(a))
    # inner gaps: background not connected to border
    bg=Image.fromarray(((~a)*255).astype(np.uint8)); pad=Image.new('L',(130,130),255); pad.paste(bg,(1,1))
    ImageDraw.floodfill(pad,(0,0),0); inner=np.asarray(pad)[1:-1,1:-1]>0
    gap=ridge_cv(depthmap(inner)) if inner.sum()>20 else None
    return ink,gap
if __name__=='__main__':
    names=json.load(open('names.json')); met=json.load(open('si_metrics.json'))
    sp=Image.open('sprite128.png').convert('L'); out={}
    for i,n in enumerate(names):
        if not (0.8<=met[n]['aspect']<=1.25): continue
        r,c=divmod(i,59); out[n]=measure(sp.crop((c*128,r*128,(c+1)*128,(r+1)*128)))
    json.dump(out,open('stroke.json','w'))
    v=np.array([x[0] for x in out.values() if x[0] is not None]); print('ink cv pct',np.percentile(v,[10,25,50,75,90]).round(3), len(v))
