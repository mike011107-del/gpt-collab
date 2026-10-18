# 用 FOGRA39L（銅版）與 FOGRA47L（非塗佈）實測特性資料（colord 收錄，CC0）推算 sRGB 色在印刷上的最佳重現
import re, sys, json, math
import numpy as np
sys.path.insert(0,'/tmp/claude-0/work')
PROF='/tmp/claude-0/src/colord/data/profiles/'
def load_ti3(name):
    s=open(PROF+name+'.iccprofile.xml',encoding='utf-8').read()
    tl=float(re.search(r'<tlimit>([\d.]+)</tlimit>',s).group(1))
    fmt=re.search(r'BEGIN_DATA_FORMAT\s*(.*?)\s*END_DATA_FORMAT',s,re.S).group(1).split()
    body=re.search(r'BEGIN_DATA\s*(.*?)\s*END_DATA\b',s.split('END_DATA_FORMAT',1)[1],re.S).group(1)
    rows=[l.split() for l in body.strip().splitlines() if l.strip()]
    A=np.array([[float(x) for x in r] for r in rows])
    ix={k:i for i,k in enumerate(fmt)}
    cmyk=A[:,[ix['CMYK_C'],ix['CMYK_M'],ix['CMYK_Y'],ix['CMYK_K']]]
    xyz=A[:,[ix['XYZ_X'],ix['XYZ_Y'],ix['XYZ_Z']]]/100.0
    return cmyk, xyz, tl
D50=np.array([0.9642,1.0,0.8249])
def xyz2lab(xyz,wn=D50):
    t=np.asarray(xyz)/wn; f=np.where(t>(6/29)**3,np.cbrt(t),t/(3*(6/29)**2)+4/29)
    return np.stack([116*f[...,1]-16,500*(f[...,0]-f[...,1]),200*(f[...,1]-f[...,2])],-1)
def lab2xyz(lab,wn=D50):
    L,a,b=lab[...,0],lab[...,1],lab[...,2]; fy=(L+16)/116; fx=fy+a/500; fz=fy-b/200
    def finv(f): return np.where(f>6/29, f**3, 3*(6/29)**2*(f-4/29))
    return np.stack([finv(fx),finv(fy),finv(fz)],-1)*wn
# sRGB -> XYZ D50 (Bradford-adapted, ICC sRGB)
M50=np.array([[0.4360747,0.3850649,0.1430804],[0.2225045,0.7168786,0.0606169],[0.0139322,0.0971045,0.7141733]])
def hex2rgb(h): h=h.lstrip('#'); return np.array([int(h[i:i+2],16) for i in (0,2,4)])/255.0
def lin(c): return np.where(c<=0.04045,c/12.92,((c+0.055)/1.055)**2.4)
def enc(c): c=np.clip(c,0,1); return np.where(c<=0.0031308,12.92*c,1.055*c**(1/2.4)-0.055)
def srgb2lab50(h): return xyz2lab(M50@lin(hex2rgb(h)))
def lab502hex(lab):
    rgb=enc(np.linalg.solve(M50, lab2xyz(np.asarray(lab))))
    return '#%02X%02X%02X'%tuple(int(round(v*255)) for v in rgb), bool(np.all((np.linalg.solve(M50, lab2xyz(np.asarray(lab)))>=-0.002)&(np.linalg.solve(M50, lab2xyz(np.asarray(lab)))<=1.002)))
def de2000(l1,l2):
    L1,a1,b1=l1; L2,a2,b2=l2
    C1=math.hypot(a1,b1); C2=math.hypot(a2,b2); Cb=(C1+C2)/2
    G=0.5*(1-math.sqrt(Cb**7/(Cb**7+25**7)))
    a1p=(1+G)*a1; a2p=(1+G)*a2; C1p=math.hypot(a1p,b1); C2p=math.hypot(a2p,b2)
    h1p=math.degrees(math.atan2(b1,a1p))%360 if C1p else 0; h2p=math.degrees(math.atan2(b2,a2p))%360 if C2p else 0
    dLp=L2-L1; dCp=C2p-C1p
    if C1p*C2p==0: dhp=0
    else:
        dhp=h2p-h1p
        if dhp>180: dhp-=360
        elif dhp<-180: dhp+=360
    dHp=2*math.sqrt(C1p*C2p)*math.sin(math.radians(dhp/2))
    Lbp=(L1+L2)/2; Cbp=(C1p+C2p)/2
    if C1p*C2p==0: hbp=h1p+h2p
    elif abs(h1p-h2p)<=180: hbp=(h1p+h2p)/2
    elif h1p+h2p<360: hbp=(h1p+h2p+360)/2
    else: hbp=(h1p+h2p-360)/2
    Tt=1-0.17*math.cos(math.radians(hbp-30))+0.24*math.cos(math.radians(2*hbp))+0.32*math.cos(math.radians(3*hbp+6))-0.20*math.cos(math.radians(4*hbp-63))
    dth=30*math.exp(-((hbp-275)/25)**2); Rc=2*math.sqrt(Cbp**7/(Cbp**7+25**7))
    Sl=1+0.015*(Lbp-50)**2/math.sqrt(20+(Lbp-50)**2); Sc=1+0.045*Cbp; Sh=1+0.015*Cbp*Tt; Rt=-math.sin(math.radians(2*dth))*Rc
    return math.sqrt((dLp/Sl)**2+(dCp/Sc)**2+(dHp/Sh)**2+Rt*(dCp/Sc)*(dHp/Sh))

class Printer:
    def __init__(self,name):
        cmyk,xyz,tl=load_ti3(name); self.name=name; self.tl=tl
        white=xyz[np.argmin(cmyk.sum(1))]; self.paper_abs=xyz2lab(white)
        rel=xyz*(D50/white)              # 媒材相對（ICC 相對色度）
        self.cmyk=cmyk; self.lab=xyz2lab(rel); self.lab_abs=xyz2lab(xyz)
    def forward(self,c,k=12,absolute=False):
        c=np.asarray(c,float); d=np.linalg.norm(self.cmyk-c,axis=1); idx=np.argsort(d)[:k]
        X=np.hstack([self.cmyk[idx],np.ones((k,1))]); w=1/(d[idx]+1.0)
        Y=(self.lab_abs if absolute else self.lab)[idx]
        W=np.diag(w); beta=np.linalg.lstsq(W@X,W@Y,rcond=None)[0]
        return np.append(c,1)@beta
    def best(self,target_lab):
        # 起點：與目標最接近的實測色塊
        de=np.array([de2000(target_lab,l) for l in self.lab]); order=np.argsort(de)[:6]
        best=(1e9,None)
        for o in order:
            x=self.cmyk[o].copy(); step=8.0; f=de2000(target_lab,self.forward(x))
            while step>0.05:
                improved=False
                for i in range(4):
                    for s in (step,-step):
                        y=x.copy(); y[i]=min(100,max(0,y[i]+s))
                        if y.sum()>self.tl: continue
                        fy=de2000(target_lab,self.forward(y))
                        if fy<f-1e-6: x,f,improved=y,fy,True
                if not improved: step/=2
            if f<best[0]: best=(f,x)
        f,x=best; return dict(cmyk=[round(v,1) for v in x], de=round(f,2), lab_rel=[round(v,2) for v in self.forward(x)], lab_abs=[round(v,2) for v in self.forward(x,absolute=True)])
if __name__=='__main__':
    P={'coated':Printer('FOGRA39L_coated'),'uncoated':Printer('FOGRA47L_uncoated')}
    for k,p in P.items(): print(k,'TAC',p.tl,'paper Lab(abs D50)',np.round(p.paper_abs,2), 'patches',len(p.cmyk))
    out={}
    for name,h in [('深青','#0C424A'),('靛藍','#333D66'),('工程黃','#D68702'),('冷灰','#788284'),('淺灰藍','#B6C5DF'),('霧白','#F4F7F8'),('華通衛生行','#005959'),('Siemens石油青','#009999'),('Vattenfall藍','#2071B5'),('黑字墨灰','#222B2C')]:
        t=srgb2lab50(h); row=dict(hex=h, lab50=[round(v,2) for v in t])
        for k,p in P.items(): row[k]=p.best(t); row[k]['view_hex']=lab502hex(np.array(row[k]['lab_rel']))[0]
        out[name]=row
        print(name,h,'Lab',row['lab50'],'| 銅版 ΔE',row['coated']['de'],row['coated']['cmyk'],row['coated']['view_hex'],'| 非塗佈 ΔE',row['uncoated']['de'],row['uncoated']['cmyk'],row['uncoated']['view_hex'])
    json.dump(out,open('/tmp/claude-0/work/print_results.json','w'),ensure_ascii=False,indent=1)
