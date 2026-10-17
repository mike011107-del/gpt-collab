import json, numpy as np
from PIL import Image
P="/mnt/user-data/uploads/崧淳環保科技股份有限公司/國外同業CIS素材_20261017/_報告原始檔/v3/photos/"
def lin(c): return np.where(c<=0.04045,c/12.92,((c+0.055)/1.055)**2.4)
def enc(c): c=np.clip(c,0,1); return np.where(c<=0.0031308,12.92*c,1.055*c**(1/2.4)-0.055)
M1=np.array([[0.4122214708,0.5363325363,0.0514459929],[0.2119034982,0.6806995451,0.1073969566],[0.0883024619,0.2817188376,0.6299787005]])
M2=np.array([[0.2104542553,0.7936177850,-0.0040720468],[1.9779984951,-2.4285922050,0.4505937099],[0.0259040371,0.7827717662,-0.8086757660]])
def oklch(rgb):
    lab=(M2@np.cbrt(M1@lin(rgb/255.0).T)).T
    L=lab[:,0]; C=np.hypot(lab[:,1],lab[:,2]); H=np.degrees(np.arctan2(lab[:,2],lab[:,1]))%360
    return L,C,H
out={}
for f,kind in [('Biffa_c01','o'),('SUEZ_c01','o'),('Metro_Rod_c16','o'),('Clancy_c31','o'),('Ventia_c03','o'),('Aarsleff_c14','o'),('Kier_c08','y'),('Lanes_Group_c01','y'),('Hydromax_USA_c16','y'),('IBAK_c20','y')]:
    im=np.asarray(Image.open(P+f+'.jpg').convert('RGB')).reshape(-1,3).astype(float)
    L,C,H=oklch(im)
    if kind=='o': m=(H>35)&(H<70)&(C>0.14)&(L>0.55)
    else: m=(H>100)&(H<125)&(C>0.14)&(L>0.75)
    sel=im[m]
    med=np.median(sel,axis=0) if len(sel) else None
    hx='#%02X%02X%02X'%tuple(int(round(x)) for x in med)
    Lm,Cm,Hm=oklch(med[None,:])
    out[f]=dict(kind=kind,hex=hx,share=float(m.mean()),oklch=[round(float(Lm[0]),3),round(float(Cm[0]),3),round(float(Hm[0]),1)])
    print(f,kind,hx,round(m.mean(),3),out[f]['oklch'])
L,C,H=oklch(np.array([[0xD6,0x87,0x02]],float)); print('工程黃',round(L[0],3),round(C[0],3),round(H[0],1))
json.dump(out,open('/tmp/claude-0/report/hivis.json','w'),ensure_ascii=False,indent=1)
