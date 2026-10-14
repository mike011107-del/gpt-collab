import numpy as np
from PIL import Image
def to_lin(a):
    a=a/255.0; return np.where(a<=0.04045,a/12.92,((a+0.055)/1.055)**2.4)
def to_srgb(l):
    l=np.clip(l,0,1); return np.where(l<=0.0031308,12.92*l,1.055*l**(1/2.4)-0.055)*255
def hexlin(h): return to_lin(np.array([int(h[i:i+2],16) for i in (1,3,5)],float))
def recolor(img,old,new,boxes,ang=0.12,lumr=(0.25,2.2)):
    a=np.asarray(img.convert('RGB')).astype(float); L=to_lin(a)
    o=hexlin(old); n=hexlin(new)
    on=o/np.linalg.norm(o)
    norm=np.linalg.norm(L,axis=2,keepdims=True)+1e-9
    cos=(L/norm*on).sum(axis=2)
    Yp=(L*np.array([0.2126,0.7152,0.0722])).sum(axis=2); Yo=(o*np.array([0.2126,0.7152,0.0722])).sum()
    k=Yp/Yo
    m=(cos>np.cos(ang))&(k>lumr[0])&(k<lumr[1])
    box=np.zeros(m.shape,bool)
    for x0,y0,x1,y1 in boxes: box[y0:y1,x0:x1]=True
    m&=box
    out=L.copy(); out[m]=n[None,:]*k[m][:,None]
    res=a.copy(); res[m]=to_srgb(out[m])
    return Image.fromarray(res.astype(np.uint8)),m
