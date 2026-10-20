# 能算的配色模型（第二輪 models 工作串）
# 每個函式都寫出公式取自哪個檔、哪個提交。不從記憶補公式。
#
# 來源：
#  MCU  = google/material-color-utilities，/tmp/claude-0/r2/src/mcu/repo，提交 dd62982dfdefdfc9232ce8d76e122fb1c6d188ae
#         typescript/utils/color_utils.ts（sRGB→XYZ→Lab）、hct/viewing_conditions.ts、hct/cam16.ts、
#         temperature/temperature_cache.ts（rawTemperature = Ou 等人 2004 冷暖）、dislike/dislike_analyzer.ts
#  CG   = connorgr/colorgorical，/tmp/claude-0/r2/src/colorgorical/repo，提交 90649656a57ce9743b00390473adce51a821cadc
#         src/model/c/scores/*.c、src/model/c/util/*.c、src/model/c/numpyColorgorical.c、src/model/model.py
import math
import numpy as np

# ---------- 色彩轉換（MCU color_utils.ts） ----------
SRGB_TO_XYZ = np.array([
    [0.41233895, 0.35762064, 0.18051042],
    [0.2126, 0.7152, 0.0722],
    [0.01932141, 0.11916382, 0.95034478]])
WHITE_D65 = np.array([95.047, 100.0, 108.883])


def hex2rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def linearized(c):
    n = c / 255.0
    return n / 12.92 * 100.0 if n <= 0.040449936 else ((n + 0.055) / 1.055) ** 2.4 * 100.0


def xyz_from_hex(h):
    r, g, b = hex2rgb(h)
    lin = np.array([linearized(r), linearized(g), linearized(b)])
    return SRGB_TO_XYZ @ lin


def _labf(t):
    e = 216.0 / 24389.0
    k = 24389.0 / 27.0
    return t ** (1.0 / 3.0) if t > e else (k * t + 16) / 116


def lab_from_xyz(xyz):
    fx, fy, fz = (_labf(xyz[i] / WHITE_D65[i]) for i in range(3))
    return np.array([116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)])


def lab_from_hex(h):
    return lab_from_xyz(xyz_from_hex(h))


def lch(lab):
    L, a, b = lab
    C = math.hypot(a, b)
    hdeg = math.degrees(math.atan2(b, a)) % 360
    return L, C, hdeg


# ---------- CIEDE2000（Sharma 等 2005；CG ciede2000.c 同一算法） ----------
def ciede2000(lab1, lab2):
    L1, a1, b1 = lab1
    L2, a2, b2 = lab2
    C1 = math.hypot(a1, b1); C2 = math.hypot(a2, b2)
    Cm = (C1 + C2) / 2
    G = 0.5 * (1 - math.sqrt(Cm ** 7 / (Cm ** 7 + 25.0 ** 7)))
    a1p = (1 + G) * a1; a2p = (1 + G) * a2
    C1p = math.hypot(a1p, b1); C2p = math.hypot(a2p, b2)
    h1p = math.degrees(math.atan2(b1, a1p)) % 360 if C1p else 0.0
    h2p = math.degrees(math.atan2(b2, a2p)) % 360 if C2p else 0.0
    dLp = L2 - L1
    dCp = C2p - C1p
    if C1p * C2p == 0:
        dhp = 0.0
    else:
        dhp = h2p - h1p
        if dhp > 180: dhp -= 360
        elif dhp < -180: dhp += 360
    dHp = 2 * math.sqrt(C1p * C2p) * math.sin(math.radians(dhp / 2))
    Lpm = (L1 + L2) / 2
    Cpm = (C1p + C2p) / 2
    if C1p * C2p == 0:
        hpm = h1p + h2p
    elif abs(h1p - h2p) <= 180:
        hpm = (h1p + h2p) / 2
    elif h1p + h2p < 360:
        hpm = (h1p + h2p + 360) / 2
    else:
        hpm = (h1p + h2p - 360) / 2
    T = (1 - 0.17 * math.cos(math.radians(hpm - 30)) + 0.24 * math.cos(math.radians(2 * hpm))
         + 0.32 * math.cos(math.radians(3 * hpm + 6)) - 0.20 * math.cos(math.radians(4 * hpm - 63)))
    dtheta = 30 * math.exp(-((hpm - 275) / 25) ** 2)
    Rc = 2 * math.sqrt(Cpm ** 7 / (Cpm ** 7 + 25.0 ** 7))
    Sl = 1 + 0.015 * (Lpm - 50) ** 2 / math.sqrt(20 + (Lpm - 50) ** 2)
    Sc = 1 + 0.045 * Cpm
    Sh = 1 + 0.015 * Cpm * T
    Rt = -math.sin(math.radians(2 * dtheta)) * Rc
    return math.sqrt((dLp / Sl) ** 2 + (dCp / Sc) ** 2 + (dHp / Sh) ** 2 + Rt * (dCp / Sc) * (dHp / Sh))


def ciede2000_vec(L1, a1, b1, L2, a2, b2):
    """numpy 向量版，給 8325 色全配對驗證用。"""
    C1 = np.hypot(a1, b1); C2 = np.hypot(a2, b2)
    Cm = (C1 + C2) / 2
    G = 0.5 * (1 - np.sqrt(Cm ** 7 / (Cm ** 7 + 25.0 ** 7)))
    a1p = (1 + G) * a1; a2p = (1 + G) * a2
    C1p = np.hypot(a1p, b1); C2p = np.hypot(a2p, b2)
    h1p = np.where(C1p == 0, 0.0, np.degrees(np.arctan2(b1, a1p)) % 360)
    h2p = np.where(C2p == 0, 0.0, np.degrees(np.arctan2(b2, a2p)) % 360)
    dLp = L2 - L1
    dCp = C2p - C1p
    dhp = h2p - h1p
    dhp = np.where(dhp > 180, dhp - 360, np.where(dhp < -180, dhp + 360, dhp))
    dhp = np.where(C1p * C2p == 0, 0.0, dhp)
    dHp = 2 * np.sqrt(C1p * C2p) * np.sin(np.radians(dhp / 2))
    Lpm = (L1 + L2) / 2
    Cpm = (C1p + C2p) / 2
    s = h1p + h2p
    hpm = np.where(np.abs(h1p - h2p) <= 180, s / 2, np.where(s < 360, (s + 360) / 2, (s - 360) / 2))
    hpm = np.where(C1p * C2p == 0, s, hpm)
    T = (1 - 0.17 * np.cos(np.radians(hpm - 30)) + 0.24 * np.cos(np.radians(2 * hpm))
         + 0.32 * np.cos(np.radians(3 * hpm + 6)) - 0.20 * np.cos(np.radians(4 * hpm - 63)))
    dtheta = 30 * np.exp(-((hpm - 275) / 25) ** 2)
    Rc = 2 * np.sqrt(Cpm ** 7 / (Cpm ** 7 + 25.0 ** 7))
    Sl = 1 + 0.015 * (Lpm - 50) ** 2 / np.sqrt(20 + (Lpm - 50) ** 2)
    Sc = 1 + 0.045 * Cpm
    Sh = 1 + 0.015 * Cpm * T
    Rt = -np.sin(np.radians(2 * dtheta)) * Rc
    return np.sqrt((dLp / Sl) ** 2 + (dCp / Sc) ** 2 + (dHp / Sh) ** 2 + Rt * (dCp / Sc) * (dHp / Sh))


# ---------- Ou 等人 2004 冷暖（經 MCU temperature_cache.ts rawTemperature） ----------
def ou_warm_cool(lab):
    """-0.5 + 0.02 * C^1.07 * cos(h - 50°)，L*a*b*（D65）。大於 0 偏暖，小於 0 偏冷。"""
    L, C, h = lch(lab)
    return -0.5 + 0.02 * C ** 1.07 * math.cos(math.radians((h - 50.0) % 360))


# ---------- CAM16 / HCT（MCU viewing_conditions.ts、cam16.ts） ----------
def _y_from_lstar(l):
    ft = (l + 16.0) / 116.0
    ft3 = ft ** 3
    return 100.0 * (ft3 if ft3 > 216.0 / 24389.0 else (116 * ft - 16) / (24389.0 / 27.0))


def _viewing_conditions():
    wp = WHITE_D65
    La = (200.0 / math.pi) * _y_from_lstar(50.0) / 100.0
    bgL = 50.0; surround = 2.0
    rW = wp[0] * 0.401288 + wp[1] * 0.650173 + wp[2] * -0.051461
    gW = wp[0] * -0.250268 + wp[1] * 1.204414 + wp[2] * 0.045854
    bW = wp[0] * -0.002079 + wp[1] * 0.048952 + wp[2] * 0.953127
    f = 0.8 + surround / 10.0
    c = (0.59 + (0.69 - 0.59) * (f - 0.9) * 10.0) if f >= 0.9 else (0.525 + (0.59 - 0.525) * (f - 0.8) * 10.0)
    d = f * (1.0 - (1.0 / 3.6) * math.exp((-La - 42.0) / 92.0))
    d = min(1.0, max(0.0, d))
    nc = f
    rgbD = [d * (100.0 / rW) + 1.0 - d, d * (100.0 / gW) + 1.0 - d, d * (100.0 / bW) + 1.0 - d]
    k = 1.0 / (5.0 * La + 1.0)
    k4 = k ** 4
    k4F = 1.0 - k4
    fl = k4 * La + 0.1 * k4F * k4F * (5.0 * La) ** (1 / 3)
    n = _y_from_lstar(bgL) / wp[1]
    z = 1.48 + math.sqrt(n)
    nbb = 0.725 / n ** 0.2
    ncb = nbb
    rgbAF = [(fl * rgbD[0] * rW / 100.0) ** 0.42, (fl * rgbD[1] * gW / 100.0) ** 0.42, (fl * rgbD[2] * bW / 100.0) ** 0.42]
    rgbA = [400.0 * x / (x + 27.13) for x in rgbAF]
    aw = (2.0 * rgbA[0] + rgbA[1] + 0.05 * rgbA[2]) * nbb
    return dict(n=n, aw=aw, nbb=nbb, ncb=ncb, c=c, nc=nc, rgbD=rgbD, fl=fl, fLRoot=fl ** 0.25, z=z)


VC = _viewing_conditions()


def cam16_from_hex(hx):
    x, y, z = xyz_from_hex(hx)
    v = VC
    rC = 0.401288 * x + 0.650173 * y - 0.051461 * z
    gC = -0.250268 * x + 1.204414 * y + 0.045854 * z
    bC = -0.002079 * x + 0.048952 * y + 0.953127 * z
    rD, gD, bD = v['rgbD'][0] * rC, v['rgbD'][1] * gC, v['rgbD'][2] * bC

    def adapt(cD):
        af = (v['fl'] * abs(cD) / 100.0) ** 0.42
        return math.copysign(1, cD) * 400.0 * af / (af + 27.13) if cD != 0 else 0.0
    rA, gA, bA = adapt(rD), adapt(gD), adapt(bD)
    a = (11.0 * rA - 12.0 * gA + bA) / 11.0
    b = (rA + gA - 2.0 * bA) / 9.0
    u = (20.0 * rA + 20.0 * gA + 21.0 * bA) / 20.0
    p2 = (40.0 * rA + 20.0 * gA + bA) / 20.0
    hue = math.degrees(math.atan2(b, a)) % 360
    ac = p2 * v['nbb']
    J = 100.0 * (ac / v['aw']) ** (v['c'] * v['z'])
    Q = (4.0 / v['c']) * math.sqrt(J / 100.0) * (v['aw'] + 4.0) * v['fLRoot']
    huePrime = hue + 360 if hue < 20.14 else hue
    eHue = 0.25 * (math.cos(math.radians(huePrime) + 2.0) + 3.8)
    p1 = 50000.0 / 13.0 * eHue * v['nc'] * v['ncb']
    t = p1 * math.hypot(a, b) / (u + 0.305)
    alpha = t ** 0.9 * (1.64 - 0.29 ** v['n']) ** 0.73
    C = alpha * math.sqrt(J / 100.0)
    M = C * v['fLRoot']
    s = 50.0 * math.sqrt(alpha * v['c'] / (v['aw'] + 4.0))
    return dict(hue=hue, chroma=C, j=J, q=Q, m=M, s=s)


def hct_from_hex(hx):
    cam = cam16_from_hex(hx)
    tone = lab_from_hex(hx)[0]
    return cam['hue'], cam['chroma'], tone


def mcu_is_disliked(hx):
    """MCU DislikeAnalyzer.isDisliked：HCT 色相 90–111、彩度 >16、明度（tone）<65 都成立。"""
    h, c, t = hct_from_hex(hx)
    return (round(h) >= 90 and round(h) <= 111) and round(c) > 16 and round(t) < 65


# ---------- Colorgorical 分數（CG） ----------
class Colorgorical:
    # 來自 CG pairPreference.c
    WH, WL, WC = -46.4222, 47.6133, 75.1481
    CMAX, CMIN = 36.0, 4.0
    HMAX, HMIN = 179.266981384, 0.033547949
    LMAX, LMIN = 63.3673, 0.0
    # 來自 CG model.py（make()，正規化到 0–1 用；「從資料集 8325 色預先算好」）
    DE_MAX, DE_MIN = 122.48163103, 1.02043527056
    PP_MAX, PP_MIN = 107.909, -101.423

    def __init__(self, npz):
        d = np.load(npz)
        self.T = {k: d[k] for k in d.files}
        self.grid = self.T['LAB'].reshape(-1, 3).astype(float)  # 8325 × 3
        self.valid = self.T['LAB_IS_VALID_RGB'].astype(bool)

    @staticmethod
    def lab_index(L, a, b):
        # getIndex.c：L=[0,100]、a=[-85,100]、b=[-110,95]，每 5 一格（C 整數除法）
        L = int(L); a = int(a); b = int(b)
        return (L // 5) * 38 * 42 + ((a + 85) // 5) * 42 + ((b + 110) // 5)

    def color_index(self, L, a, b):
        return int(self.T['CIS'][self.lab_index(L, a, b)])

    def snap(self, lab):
        """把任意 Lab 放到 Colorgorical 的 5 單位格點（8325 色裡最近的一格）。"""
        dist = np.sqrt(((self.grid - np.asarray(lab)) ** 2).sum(1))
        i = int(np.argmin(dist))
        return tuple(int(v) for v in self.grid[i]), float(dist[i])

    # ---- 單色 ----
    def coolness(self, g):
        return float(self.T['COOLNESS'][self.lab_index(*g)])

    def lch_table(self, g):
        i = self.lab_index(*g) * 2
        return float(self.T['CH'][i]), float(self.T['CH'][i + 1])

    def penalty(self, g):
        # numpyColorgorical.c double_scorePenalty_ufunc
        C, hue = self.lch_table(g)
        L = g[0]
        if 70.0 <= hue <= 115.0:
            return 0.8 if L <= 75 else 0.85
        if 115.0 <= hue < 138.0 and L <= 45.0:
            return 0.75
        return 1.0

    def is_ugly_filtered(self, g):
        # model.py make()：色相 85–114 且 L 35–75 的色不進候選
        C, hue = self.lch_table(g)
        return (hue >= 85 and hue <= 114 and g[0] <= 75 and g[0] >= 35)

    def name_uniqueness(self, g):
        ci = self.color_index(*g)
        cnt = self.T['NAMES_T'][ci * 153:(ci + 1) * 153].astype(float)
        cnt[cnt == -1] = 0
        p = cnt / self.T['NAMES_CCOUNT'][ci]
        p = p[p > 0]
        H = float((p * np.log(p) / np.log(2)).sum())
        H = (H - (-4.5)) / (0 - (-4.5))
        return 1 - H

    def top_terms(self, g, terms=None, k=3):
        ci = self.color_index(*g)
        cnt = self.T['NAMES_T'][ci * 153:(ci + 1) * 153].astype(float)
        cnt[cnt == -1] = 0
        p = cnt / self.T['NAMES_CCOUNT'][ci]
        idx = np.argsort(-p)[:k]
        return [((terms[i] if terms else int(i)), round(float(p[i]), 3)) for i in idx if p[i] > 0]

    # ---- 兩色 ----
    def name_difference(self, g1, g2):
        ai = self.color_index(*g1); bi = self.color_index(*g2)
        z = math.sqrt(self.T['NAMES_CCOUNT'][ai] * self.T['NAMES_CCOUNT'][bi])
        pa = self.T['NAMES_T'][ai * 153:(ai + 1) * 153].astype(float); pa[pa == -1] = 0
        pb = self.T['NAMES_T'][bi * 153:(bi + 1) * 153].astype(float); pb[pb == -1] = 0
        bc = float(np.sqrt(pa * pb).sum())
        return math.sqrt(max(0.0, 1 - bc / z))

    @staticmethod
    def d65_to_illC(L, a, b):
        def lab2xyz_f(t):
            return t ** 3 if t > 6.0 / 29.0 else 3.0 * (6.0 / 29) ** 2 * (t - 4.0 / 29.0)

        def xyz2lab_f(t):
            return t ** (1 / 3) if t > (6.0 / 29.0) ** 3 else (1 / 3) * (29 / 6) ** 2 * t + 4 / 29
        X = 95.0470 * lab2xyz_f((L + 16) / 116 + a / 500)
        Y = 100.0 * lab2xyz_f((L + 16) / 116)
        Z = 108.8830 * lab2xyz_f((L + 16) / 116 - b / 200)
        fy = xyz2lab_f(Y / 100.0)
        return (116 * fy - 16, 500 * (xyz2lab_f(X / 98.074) - fy), 200 * (fy - xyz2lab_f(Z / 118.232)))

    def achromatic_pref(self, L, a, b, achL):
        # labToAchromaticPreference.c：C 的 (int)x/5 是向 0 截斷
        def tdiv(x):
            x = int(x)
            return int(x / 5)  # 向 0 截斷
        idx = tdiv(L) * 33516 + (tdiv(a) + 17) * 882 + (tdiv(b) + 22) * 21 + tdiv(achL)
        return float(self.T['ACHROMPREF'][idx])

    def pair_preference(self, g1, g2, wrap_hue=False, parts=False):
        """pairPreference.c。wrap_hue=False 為程式原樣（色相差直接相減取絕對值）；
        True 是我加的對照：色相差取 360 補角（≤180）。parts=True 另回傳三項分數與中間值。"""
        L1, a1, b1 = g1; L2, a2, b2 = g2
        ach = None
        if a1 == 0 and b1 == 0 and a2 == 0 and b2 == 0:
            ach = self.achromatic_pref(L1, a1, b1, L2)
        elif a1 == 0 and b1 == 0:
            ach = self.achromatic_pref(L2, a2, b2, L1)
        elif a2 == 0 and b2 == 0:
            ach = self.achromatic_pref(L1, a1, b1, L2)
        if ach is not None:
            return (ach, dict(path='achromatic_table')) if parts else ach
        k1 = self.coolness(g1); k2 = self.coolness(g2)
        c1 = self.d65_to_illC(*g1); c2 = self.d65_to_illC(*g2)
        H1 = math.degrees(math.atan2(c1[2], c1[1])); H1 = H1 + 360 if H1 < 0 else H1
        H2 = math.degrees(math.atan2(c2[2], c2[1])); H2 = H2 + 360 if H2 < 0 else H2
        dL = abs(c1[0] - c2[0])
        dH = abs(H1 - H2)
        if wrap_hue and dH > 180:
            dH = 360 - dH
        sC = k1 + k2
        norm = lambda d, hi, lo: (d - lo) / (hi - lo)
        tL = self.WL * norm(dL, self.LMAX, self.LMIN)
        tH = self.WH * norm(dH, self.HMAX, self.HMIN)
        tC = self.WC * norm(sC, self.CMAX, self.CMIN)
        pp = tL + tH + tC
        if parts:
            return pp, dict(path='chromatic', dL_illC=round(dL, 2), dH_illC=round(dH, 2), coolness=[k1, k2],
                            term_lightness=round(tL, 2), term_hue=round(tH, 2), term_coolness=round(tC, 2))
        return pp

    def pp_norm(self, pp):
        return (pp - self.PP_MIN) / (self.PP_MAX - self.PP_MIN)

    def de_norm(self, de):
        return (de - self.DE_MIN) / (self.DE_MAX - self.DE_MIN)
