# 試幾種變化，看能不能重現 model.py 的 PP 上下限 107.909 / -101.423（查明而已，不改模型）
import sys, numpy as np
sys.path.insert(0, '/tmp/claude-0/r2/models')
import models_lib as M
CG = M.Colorgorical('/tmp/claude-0/r2/models/data/colorgorical_tables.npz')
G = CG.grid
cool = np.array([CG.coolness(tuple(int(v) for v in g)) for g in G])
illC = np.array([CG.d65_to_illC(*g) for g in G])
nrm = lambda d, hi, lo: (d - lo) / (hi - lo)
def run(Lx, Hx, mask, wrap=False):
    idx = np.where(mask)[0]
    mx, mn = -1e9, 1e9
    for k, i in enumerate(idx[:-1]):
        j = idx[k+1:]
        dL = np.abs(Lx[i]-Lx[j]); dH = np.abs(Hx[i]-Hx[j])
        if wrap: dH = np.where(dH > 180, 360-dH, dH)
        pp = CG.WL*nrm(dL,CG.LMAX,CG.LMIN)+CG.WH*nrm(dH,CG.HMAX,CG.HMIN)+CG.WC*nrm(cool[i]+cool[j],CG.CMAX,CG.CMIN)
        mx = max(mx, pp.max()); mn = min(mn, pp.min())
    return round(float(mx),3), round(float(mn),3)
chrom = ~((G[:,1]==0)&(G[:,2]==0))
HC = np.degrees(np.arctan2(illC[:,2], illC[:,1])) % 360
HD = np.degrees(np.arctan2(G[:,2], G[:,1])) % 360
Lrange = (G[:,0] >= 30) & (G[:,0] <= 85)
print('IllC, valid RGB, L30-85', run(illC[:,0], HC, chrom & CG.valid & Lrange))
print('D65 L,h, all chromatic', run(G[:,0], HD, chrom))
print('D65 L,h, valid RGB', run(G[:,0], HD, chrom & CG.valid))
print('IllC, valid RGB, L30-85, wrap', run(illC[:,0], HC, chrom & CG.valid & Lrange, True))
