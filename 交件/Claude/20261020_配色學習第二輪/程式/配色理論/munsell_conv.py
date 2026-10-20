# sRGB -> Munsell 近似換算（只用 numpy）
# 資料：colour-science/colour 的 Munsell renotation 資料檔（all.py、real.py），只當文字讀，不 import。
# 流程：sRGB(D65) -> XYZ -> Bradford 轉到 Illuminant C -> xyY
#       明度 V：ASTM D1535 五次式反解（colour-science colorimetry/luminance.py 的係數）
#       色相、彩度：在相鄰兩個明度平面上，用 (色相, 彩度) 格點雙線性內插出 xy，細格搜尋最接近的點，再按 V 線性內插
# 用 python3 -I 執行。
import re, json, sys, os
import numpy as np

SRC = '/tmp/claude-0/r2/src/colour-science/colour'
HUES = ['R', 'YR', 'Y', 'GY', 'G', 'BG', 'B', 'PB', 'P', 'RP']  # 線性色相 0..100：10RP=0=100, 2.5R=2.5 ...
XY_C = np.array([0.31006, 0.31616])  # colour-science chromaticity_coordinates.py 第 117 行 Illuminant C (CIE 1931 2°)

ROW = re.compile(r'\(\("([0-9.]+)([A-Z]+)", ([0-9.]+), ([0-9.]+)\), \[([0-9.]+), ([0-9.]+), ([0-9.]+)\]\)')


def load(name):
    t = open(f'{SRC}/notation/datasets/munsell/{name}.py').read()
    out = []
    for s, fam, v, c, x, y, Y in ROW.findall(t):
        out.append((float(s), fam, float(v), float(c), float(x), float(y), float(Y)))
    return out


def lin_hue(step, fam):
    # 2.5R -> 2.5, 10R -> 10, 2.5YR -> 12.5 ... 10RP -> 100 -> 0
    return (HUES.index(fam) * 10 + step) % 100


def hue_name(H):
    H = H % 100
    if H == 0:
        H = 100
    i = int(np.ceil(H / 10.0)) - 1
    step = H - i * 10
    if step < 1e-9:
        i -= 1; step = 10
    return f'{step:.1f}{HUES[i % 10]}'


def astm_Y(V):
    return 1.1914 * V - 0.22533 * V**2 + 0.23352 * V**3 - 0.020484 * V**4 + 0.00081939 * V**5


_VV = np.arange(0, 10.0001, 0.0005)
_YY = astm_Y(_VV)


def astm_V(Y):  # Y: 0..100
    return float(np.interp(Y, _YY, _VV))


def dec(v):
    return np.where(v <= 0.04045, v / 12.92, ((v + 0.055) / 1.055) ** 2.4)


M_RGB2XYZ = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
BRAD = np.array([[0.8951, 0.2664, -0.1614], [-0.7502, 1.7135, 0.0367], [0.0389, -0.0685, 1.0296]])


def xy2XYZ(x, y, Y=1.0):
    return np.array([x * Y / y, Y, (1 - x - y) * Y / y])


W65 = M_RGB2XYZ.sum(axis=1)
WC = xy2XYZ(*XY_C)
CAT = np.linalg.inv(BRAD) @ np.diag((BRAD @ WC) / (BRAD @ W65)) @ BRAD
CAT_INV = np.linalg.inv(CAT)


def hex2xyY_C(h):
    h = h.lstrip('#')
    rgb = np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)])
    XYZ = M_RGB2XYZ @ dec(rgb)
    XYZc = CAT @ XYZ
    s = XYZc.sum()
    return np.array([XYZc[0] / s, XYZc[1] / s, XYZc[1] * 100])


def xyYC2hex(x, y, Y):
    XYZc = xy2XYZ(x, y, Y / 100)
    XYZ = CAT_INV @ XYZc
    lin = np.linalg.inv(M_RGB2XYZ) @ XYZ
    oog = bool((lin < -1e-4).any() or (lin > 1 + 1e-4).any())
    lin = np.clip(lin, 0, 1)
    enc = np.where(lin <= 0.0031308, lin * 12.92, 1.055 * lin ** (1 / 2.4) - 0.055)
    return '#' + ''.join(f'{int(round(c * 255)):02X}' for c in enc), oog


class Inverter:
    def __init__(self, rows, drop_value=None, hue_subset=None):
        self.planes = {}
        for s, fam, v, c, x, y, Y in rows:
            if drop_value is not None and abs(v - drop_value) < 1e-9:
                continue
            H = lin_hue(s, fam)
            if hue_subset is not None and (H % hue_subset) > 1e-9:
                continue
            self.planes.setdefault(v, {})[(H, c)] = (x, y)
        self.values = sorted(self.planes)
        self.cache = {}

    def plane_grid(self, v):
        if v in self.cache:
            return self.cache[v]
        P = self.planes[v]
        Hs = sorted(set(k[0] for k in P))
        step = Hs[1] - Hs[0]
        Hs = list(np.arange(0, 100, step))
        Cs = sorted(set(k[1] for k in P) | {0.0})
        nH, nC = len(Hs), len(Cs)
        gx = np.full((nH + 1, nC), np.nan); gy = np.full((nH + 1, nC), np.nan)
        for i, H in enumerate(Hs + [100.0]):
            for j, C in enumerate(Cs):
                if C == 0:
                    gx[i, j], gy[i, j] = XY_C
                else:
                    k = (H % 100, C)
                    if k in P:
                        gx[i, j], gy[i, j] = P[k]
        # 細格：每格切 20x20
        n = 20
        t = np.linspace(0, 1, n, endpoint=False)
        pts_H, pts_C, pts_x, pts_y = [], [], [], []
        Harr = np.array(Hs + [100.0]); Carr = np.array(Cs)
        for i in range(nH):
            for j in range(nC - 1):
                q = [gx[i, j], gx[i + 1, j], gx[i, j + 1], gx[i + 1, j + 1]]
                if np.isnan(q).any():
                    continue
                qy = [gy[i, j], gy[i + 1, j], gy[i, j + 1], gy[i + 1, j + 1]]
                a, b = np.meshgrid(t, np.append(t, 1.0) if j == nC - 2 else t, indexing='ij')
                xx = (1 - a) * (1 - b) * q[0] + a * (1 - b) * q[1] + (1 - a) * b * q[2] + a * b * q[3]
                yy = (1 - a) * (1 - b) * qy[0] + a * (1 - b) * qy[1] + (1 - a) * b * qy[2] + a * b * qy[3]
                pts_H.append((Harr[i] + a * (Harr[i + 1] - Harr[i])).ravel())
                pts_C.append((Carr[j] + b * (Carr[j + 1] - Carr[j])).ravel())
                pts_x.append(xx.ravel()); pts_y.append(yy.ravel())
        g = (np.concatenate(pts_H), np.concatenate(pts_C), np.concatenate(pts_x), np.concatenate(pts_y))
        self.cache[v] = g
        return g

    def invert_plane(self, v, x, y):
        H, C, gx, gy = self.plane_grid(v)
        d = (gx - x) ** 2 + (gy - y) ** 2
        k = int(np.argmin(d))
        return H[k] % 100, C[k], float(np.sqrt(d[k]))

    def xyY_to_munsell(self, x, y, Y):
        V = astm_V(Y)
        if np.hypot(x - XY_C[0], y - XY_C[1]) < 1e-4:
            return {'H': None, 'V': V, 'C': 0.0}
        vals = self.values
        lo = max([w for w in vals if w <= V], default=vals[0])
        hi = min([w for w in vals if w >= V], default=vals[-1])
        H0, C0, e0 = self.invert_plane(lo, x, y)
        if hi == lo:
            return {'H': H0, 'V': V, 'C': C0, 'fit': e0}
        H1, C1, e1 = self.invert_plane(hi, x, y)
        f = (V - lo) / (hi - lo)
        dH = ((H1 - H0 + 50) % 100) - 50
        H = (H0 + f * dH) % 100
        C = C0 + f * (C1 - C0)
        return {'H': H, 'V': V, 'C': C, 'fit': max(e0, e1)}


def fmt(m):
    if m['H'] is None or m['C'] < 0.5:
        return f"N {m['V']:.1f}"
    return f"{hue_name(m['H'])} {m['V']:.1f}/{m['C']:.1f}"


SPEC_CODE = {1: 'B', 2: 'BG', 3: 'G', 4: 'GY', 5: 'Y', 6: 'YR', 7: 'R', 8: 'RP', 9: 'P', 10: 'PB'}


def spec_to_linear(step, code):
    return lin_hue(step, SPEC_CODE[int(round(code))])


def hue_diff(a, b):
    return ((a - b + 50) % 100) - 50
