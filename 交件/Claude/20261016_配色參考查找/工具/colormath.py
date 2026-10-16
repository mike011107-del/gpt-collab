"""色彩數學（只用標準函式庫）。
- OKLab／OKLCH：照 Björn Ottosson 公開公式，沿用 交件/Claude/20261014_配色優化/程式/ok.py。
- CIELAB、CIEDE2000、WCAG 對比、Machado 色弱模擬：沿用 交件/Claude/20261014_第十五輪雲端重跑/check.py。
"""
import math


def rgb(h):
    h = h.lstrip('#'); return [int(h[i:i + 2], 16) for i in (0, 2, 4)]


def hx(c):
    return '#%02X%02X%02X' % tuple(max(0, min(255, round(v))) for v in c)


def dec(v):
    v /= 255; return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4


def enc(v):
    v = max(0.0, min(1.0, v)); return 255 * (12.92 * v if v <= 0.0031308 else 1.055 * v ** (1 / 2.4) - 0.055)


def lin3(h): return [dec(v) for v in rgb(h)]
def from_lin(c): return hx([enc(v) for v in c])


def lum(h):
    r, g, b = lin3(h); return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    x, y = sorted([lum(a), lum(b)], reverse=True); return (x + 0.05) / (y + 0.05)


# ---------- OKLab / OKLCH ----------
def oklab(h):
    r, g, b = lin3(h)
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l, m, s = [math.copysign(abs(v) ** (1 / 3), v) for v in (l, m, s)]
    return (0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
            1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
            0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s)


def oklch(h):
    L, a, b = oklab(h); return L, math.hypot(a, b), math.degrees(math.atan2(b, a)) % 360


# ---------- CIELAB（D65）與 CIEDE2000 ----------
M = [[0.4124564, 0.3575761, 0.1804375], [0.2126729, 0.7151522, 0.0721750], [0.0193339, 0.1191920, 0.9503041]]
WHITE = [sum(r) for r in M]
EPS, KAP = 216 / 24389, 24389 / 27


def lab(h):
    c = lin3(h); X, Y, Z = [sum(M[i][j] * c[j] for j in range(3)) / WHITE[i] for i in range(3)]
    f = lambda t: t ** (1 / 3) if t > EPS else (KAP * t + 16) / 116
    return (116 * f(Y) - 16, 500 * (f(X) - f(Y)), 200 * (f(Y) - f(Z)))


def de2000_lab(l1, l2):  # Sharma, Wu, Dalal (2005)
    L1, a1, b1 = l1; L2, a2, b2 = l2
    C1 = math.hypot(a1, b1); C2 = math.hypot(a2, b2); Cb = (C1 + C2) / 2
    G = 0.5 * (1 - math.sqrt(Cb ** 7 / (Cb ** 7 + 25 ** 7)))
    a1p, a2p = (1 + G) * a1, (1 + G) * a2; C1p, C2p = math.hypot(a1p, b1), math.hypot(a2p, b2)
    h1p = math.degrees(math.atan2(b1, a1p)) % 360 if (a1p or b1) else 0.0
    h2p = math.degrees(math.atan2(b2, a2p)) % 360 if (a2p or b2) else 0.0
    dL = L2 - L1; dC = C2p - C1p
    if C1p * C2p == 0: dh = 0
    else:
        dh = h2p - h1p
        if dh > 180: dh -= 360
        elif dh < -180: dh += 360
    dH = 2 * math.sqrt(C1p * C2p) * math.sin(math.radians(dh / 2))
    Lb = (L1 + L2) / 2; Cbp = (C1p + C2p) / 2
    if C1p * C2p == 0: hb = h1p + h2p
    elif abs(h1p - h2p) <= 180: hb = (h1p + h2p) / 2
    elif h1p + h2p < 360: hb = (h1p + h2p + 360) / 2
    else: hb = (h1p + h2p - 360) / 2
    T = 1 - 0.17 * math.cos(math.radians(hb - 30)) + 0.24 * math.cos(math.radians(2 * hb)) + 0.32 * math.cos(math.radians(3 * hb + 6)) - 0.20 * math.cos(math.radians(4 * hb - 63))
    dth = 30 * math.exp(-((hb - 275) / 25) ** 2); RC = 2 * math.sqrt(Cbp ** 7 / (Cbp ** 7 + 25 ** 7))
    SL = 1 + 0.015 * (Lb - 50) ** 2 / math.sqrt(20 + (Lb - 50) ** 2); SC = 1 + 0.045 * Cbp; SH = 1 + 0.015 * Cbp * T; RT = -math.sin(math.radians(2 * dth)) * RC
    return math.sqrt((dL / SL) ** 2 + (dC / SC) ** 2 + (dH / SH) ** 2 + RT * (dC / SC) * (dH / SH))


_LAB = {}


def de(h1, h2):
    a = _LAB.get(h1) or _LAB.setdefault(h1, lab(h1))
    b = _LAB.get(h2) or _LAB.setdefault(h2, lab(h2))
    return de2000_lab(a, b)


# ---------- 色弱模擬：Machado, Oliveira, Fernandes (2009) severity 1.0 ----------
MACH = {'紅色弱': [[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048116, 1.051998]],
        '綠色弱': [[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]],
        '藍色弱': [[1.255528, -0.076749, -0.178779], [-0.078411, 0.930809, 0.147602], [0.004733, 0.691367, 0.303900]]}


def cvd(h, kind):
    c = lin3(h); m = MACH[kind]; return from_lin([sum(m[i][j] * c[j] for j in range(3)) for i in range(3)])


def gray(h):
    """依相對亮度轉灰階（sRGB 編碼後的灰）。"""
    v = enc(lum(h)); return hx([v, v, v])


SHARMA = [
    (50.0000, 2.6772, -79.7751, 50.0000, 0.0000, -82.7485, 2.0425),
    (50.0000, 0.0000, 0.0000, 50.0000, -1.0000, 2.0000, 2.3669),
    (50.0000, 2.5000, 0.0000, 73.0000, 25.0000, -18.0000, 27.1492),
    (60.2574, -34.0099, 36.2677, 60.4626, -34.1751, 39.4387, 1.2644),
]


def selftest():
    errs = []
    for t in SHARMA:
        got = de2000_lab(t[0:3], t[3:6])
        if abs(got - t[6]) > 1e-4: errs.append(f'CIEDE2000 {t} 得 {got:.4f}')
    if abs(contrast('#000000', '#FFFFFF') - 21) > 1e-9: errs.append('黑白對比不是 21')
    L, C, H = oklch('#FFFFFF')
    if abs(L - 1) > 1e-3 or C > 1e-3: errs.append('白色 OKLCH 不是 L1 C0')
    return errs


# ---------- OKLCH → sRGB（畫色格用；超出色域時降彩度） ----------
def _lab2lin(L, a, b):
    l = L + 0.3963377774 * a + 0.2158037573 * b; m = L - 0.1055613458 * a - 0.0638541728 * b; s = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l ** 3, m ** 3, s ** 3
    return (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s, -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s, -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s)


def _ingamut(c, eps=1e-6): return all(-eps <= v <= 1 + eps for v in c)


def max_chroma(L, H):
    lo, hi = 0.0, 0.4; hr = math.radians(H)
    for _ in range(30):
        mid = (lo + hi) / 2
        if _ingamut(_lab2lin(L, mid * math.cos(hr), mid * math.sin(hr))): lo = mid
        else: hi = mid
    return lo


def from_oklch(L, C, H):
    C = min(C, max_chroma(L, H)); hr = math.radians(H)
    return from_lin([max(0.0, min(1.0, v)) for v in _lab2lin(L, C * math.cos(hr), C * math.sin(hr))])
