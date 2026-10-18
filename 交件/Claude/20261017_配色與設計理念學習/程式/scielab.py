# S-CIELAB（Zhang & Wandell 1996；濾波參數取 ISETCam scGaussianParameters 'distribution' 版）
import numpy as np
M=np.array([[0.4124564,0.3575761,0.1804375],[0.2126729,0.7151522,0.0721750],[0.0193339,0.1191920,0.9503041]])
XYZ2OPP=np.array([[278.7336,721.8031,-106.5520],[-448.7736,289.8056,77.1569],[85.9513,-589.9859,501.1089]])/1000
PAR_DIST={0:[(0.05,1.00327),(0.225,0.114416),(7.0,-0.117686)],1:[(0.0685,0.616725),(0.826,0.383275)],2:[(0.0920,0.567885),(0.6451,0.432115)]}
# 1996 原始發表值（擴散約為上面一半，模擬較保守）
PAR_ORIG={0:[(0.0283,0.921),(0.133,0.105),(4.336,-0.1080)],1:[(0.0392,0.531),(0.494,0.33)],2:[(0.0536,0.488),(0.386,0.371)]}
PAR=PAR_ORIG
def lin(c): return np.where(c<=0.04045,c/12.92,((c+0.055)/1.055)**2.4)
def enc(c): c=np.clip(c,0,1); return np.where(c<=0.0031308,12.92*c,1.055*c**(1/2.4)-0.055)
def kernel1d(hwhm_px,n):
    x=np.arange(n)-n//2; sd=hwhm_px/np.sqrt(2*np.log(2)); g=np.exp(-0.5*(x/sd)**2); return g/g.sum()
def filt(img,ch,spd):
    H,W=img.shape; out=np.zeros_like(img); tot=0
    # 用 FFT 做分離式卷積，邊界用反射延伸
    for hw,w in PAR[ch]:
        hp=hw*spd; n=int(min(max(8*hp,3),4*max(H,W)))|1
        k=kernel1d(hp,n)
        pad=n//2
        a=np.pad(img,((pad,pad),(pad,pad)),mode='reflect' if pad<min(H,W) else 'edge')
        a=np.apply_along_axis(lambda r: np.convolve(r,k,mode='same'),1,a)
        a=np.apply_along_axis(lambda r: np.convolve(r,k,mode='same'),0,a)
        out+=w*a[pad:pad+H,pad:pad+W]; tot+=w
    return out/tot
def scielab_render(rgb8,spd):
    rgb=lin(rgb8/255.0); xyz=rgb@M.T; opp=xyz@XYZ2OPP.T
    f=np.stack([filt(opp[...,i],i,spd) for i in range(3)],-1)
    xyz2=f@np.linalg.inv(XYZ2OPP).T; rgb2=xyz2@np.linalg.inv(M).T
    return (enc(rgb2)*255).round().astype(np.uint8), xyz2
