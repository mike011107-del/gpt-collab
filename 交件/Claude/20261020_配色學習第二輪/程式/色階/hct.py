"""HCT (Material Color Utilities) 的 Python 改寫。
依據：material-foundation/material-color-utilities 提交 dd62982
  typescript/hct/viewing_conditions.ts、cam16.ts、utils/color_utils.ts、palettes/tonal_palette.ts
HCT -> sRGB 用二分法（固定 hue、tone，找 J；超出色域就把 chroma 二分到邊界），
不是原庫的 HctSolver 解析解，所以個別色碼可能差 1。selftest() 拿原庫測試值核對。
"""
import math

SRGB_TO_XYZ = [[0.41233895, 0.35762064, 0.18051042],
               [0.2126, 0.7152, 0.0722],
               [0.01932141, 0.11916382, 0.95034478]]
XYZ_TO_SRGB = [[3.2413774792388685, -1.5376652402851851, -0.49885366846268053],
               [-0.9691452513005321, 1.8758853451067872, 0.04156585616912061],
               [0.05562093689691305, -0.20395524564742123, 1.0571799111220335]]
WP = [95.047, 100.0, 108.883]


def lab_f(t):
    e = 216.0 / 24389.0; k = 24389.0 / 27.0
    return t ** (1 / 3) if t > e else (k * t + 16) / 116


def lab_invf(ft):
    e = 216.0 / 24389.0; k = 24389.0 / 27.0
    f3 = ft ** 3
    return f3 if f3 > e else (116 * ft - 16) / k


def y_from_lstar(l):
    return 100.0 * lab_invf((l + 16.0) / 116.0)


def lstar_from_y(y):
    return lab_f(y / 100.0) * 116.0 - 16.0


def linearized(c):
    n = c / 255.0
    return n / 12.92 * 100.0 if n <= 0.040449936 else ((n + 0.055) / 1.055) ** 2.4 * 100.0


def delinearized_f(c):
    n = c / 100.0
    d = n * 12.92 if n <= 0.0031308 else 1.055 * (n ** (1 / 2.4)) - 0.055
    return d * 255.0


def lerp(a, b, t):
    return a + (b - a) * t


class VC:
    def __init__(self):
        wp = WP
        al = (200.0 / math.pi) * y_from_lstar(50.0) / 100.0
        bl = 50.0; surround = 2.0
        rW = wp[0] * 0.401288 + wp[1] * 0.650173 + wp[2] * -0.051461
        gW = wp[0] * -0.250268 + wp[1] * 1.204414 + wp[2] * 0.045854
        bW = wp[0] * -0.002079 + wp[1] * 0.048952 + wp[2] * 0.953127
        f = 0.8 + surround / 10.0
        c = lerp(0.59, 0.69, (f - 0.9) * 10.0) if f >= 0.9 else lerp(0.525, 0.59, (f - 0.8) * 10.0)
        d = f * (1.0 - (1.0 / 3.6) * math.exp((-al - 42.0) / 92.0))
        d = max(0.0, min(1.0, d))
        self.nc = f
        self.rgbD = [d * (100.0 / rW) + 1.0 - d, d * (100.0 / gW) + 1.0 - d, d * (100.0 / bW) + 1.0 - d]
        k = 1.0 / (5.0 * al + 1.0); k4 = k ** 4; k4F = 1.0 - k4
        self.fl = k4 * al + 0.1 * k4F * k4F * ((5.0 * al) ** (1 / 3))
        self.n = y_from_lstar(bl) / wp[1]
        self.z = 1.48 + math.sqrt(self.n)
        self.nbb = 0.725 / (self.n ** 0.2); self.ncb = self.nbb
        fs = [((self.fl * self.rgbD[i] * w) / 100.0) ** 0.42 for i, w in enumerate([rW, gW, bW])]
        rgbA = [400.0 * x / (x + 27.13) for x in fs]
        self.aw = (2.0 * rgbA[0] + rgbA[1] + 0.05 * rgbA[2]) * self.nbb
        self.c = c
        self.fLRoot = self.fl ** 0.25


V = VC()


def sgn(x):
    return (x > 0) - (x < 0)


def xyz_from_rgb255(r, g, b):
    lin = [linearized(r), linearized(g), linearized(b)]
    return [sum(SRGB_TO_XYZ[i][j] * lin[j] for j in range(3)) for i in range(3)]


def cam16_from_xyz(x, y, z, v=V):
    rC = 0.401288 * x + 0.650173 * y - 0.051461 * z
    gC = -0.250268 * x + 1.204414 * y + 0.045854 * z
    bC = -0.002079 * x + 0.048952 * y + 0.953127 * z
    rD, gD, bD = v.rgbD[0] * rC, v.rgbD[1] * gC, v.rgbD[2] * bC
    af = [(v.fl * abs(q) / 100.0) ** 0.42 for q in (rD, gD, bD)]
    rA, gA, bA = [sgn(q) * 400.0 * f / (f + 27.13) for q, f in zip((rD, gD, bD), af)]
    a = (11.0 * rA - 12.0 * gA + bA) / 11.0
    b = (rA + gA - 2.0 * bA) / 9.0
    u = (20.0 * rA + 20.0 * gA + 21.0 * bA) / 20.0
    p2 = (40.0 * rA + 20.0 * gA + bA) / 20.0
    hue = math.degrees(math.atan2(b, a)) % 360.0
    ac = p2 * v.nbb
    J = 100.0 * (ac / v.aw) ** (v.c * v.z)
    hp = hue + 360 if hue < 20.14 else hue
    eHue = 0.25 * (math.cos(math.radians(hp) + 2.0) + 3.8)
    p1 = 50000.0 / 13.0 * eHue * v.nc * v.ncb
    t = p1 * math.sqrt(a * a + b * b) / (u + 0.305)
    alpha = (t ** 0.9) * ((1.64 - 0.29 ** v.n) ** 0.73)
    C = alpha * math.sqrt(J / 100.0)
    return hue, C, J


def xyz_from_cam16(J, C, hue, v=V):
    alpha = 0.0 if (C == 0.0 or J == 0.0) else C / math.sqrt(J / 100.0)
    t = (alpha / ((1.64 - 0.29 ** v.n) ** 0.73)) ** (1.0 / 0.9)
    hR = math.radians(hue)
    eHue = 0.25 * (math.cos(hR + 2.0) + 3.8)
    ac = v.aw * (J / 100.0) ** (1.0 / v.c / v.z)
    p1 = eHue * (50000.0 / 13.0) * v.nc * v.ncb
    p2 = ac / v.nbb
    hs, hc = math.sin(hR), math.cos(hR)
    gamma = 23.0 * (p2 + 0.305) * t / (23.0 * p1 + 11 * t * hc + 108.0 * t * hs)
    a, b = gamma * hc, gamma * hs
    rA = (460.0 * p2 + 451.0 * a + 288.0 * b) / 1403.0
    gA = (460.0 * p2 - 891.0 * a - 261.0 * b) / 1403.0
    bA = (460.0 * p2 - 220.0 * a - 6300.0 * b) / 1403.0
    out = []
    for q, d in zip((rA, gA, bA), v.rgbD):
        base = max(0, (27.13 * abs(q)) / (400.0 - abs(q)))
        out.append(sgn(q) * (100.0 / v.fl) * base ** (1.0 / 0.42) / d)
    rF, gF, bF = out
    x = 1.86206786 * rF - 1.01125463 * gF + 0.14918677 * bF
    y = 0.38752654 * rF + 0.62144744 * gF - 0.00897398 * bF
    z = -0.01584150 * rF - 0.03412294 * gF + 1.04996444 * bF
    return [x, y, z]


def hex2rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb2hex(rgb):
    return '#' + ''.join('%02x' % int(c) for c in rgb)


def hct_from_hex(h):
    x, y, z = xyz_from_rgb255(*hex2rgb(h))
    hue, C, J = cam16_from_xyz(x, y, z)
    return hue, C, lstar_from_y(y)


def _lin_rgb_for(J, C, hue):
    xyz = xyz_from_cam16(J, C, hue)
    return [sum(XYZ_TO_SRGB[i][j] * xyz[j] for j in range(3)) for i in range(3)], xyz[1]


def _solve_J(C, hue, ytarget):
    lo, hi = 0.0, 100.0
    for _ in range(60):
        mid = (lo + hi) / 2
        _, y = _lin_rgb_for(mid, C, hue)
        if y < ytarget:
            lo = mid
        else:
            hi = mid
    J = (lo + hi) / 2
    lin, _ = _lin_rgb_for(J, C, hue)
    return J, lin


def _in_gamut(lin, eps=1e-7):
    return all(-eps <= c <= 100.0 + eps for c in lin)


def hct_to_hex(hue, chroma, tone):
    if tone <= 0.0001:
        return '#000000'
    if tone >= 99.9999:
        return '#ffffff'
    ytarget = y_from_lstar(tone)
    if chroma < 0.0001:
        g = round(delinearized_f(ytarget))
        g = max(0, min(255, g))
        return rgb2hex((g, g, g))
    J, lin = _solve_J(chroma, hue % 360, ytarget)
    if not _in_gamut(lin):
        lo, hi = 0.0, chroma
        best = None
        for _ in range(50):
            mid = (lo + hi) / 2
            J, l2 = _solve_J(mid, hue % 360, ytarget)
            if _in_gamut(l2):
                lo = mid; best = l2
            else:
                hi = mid
        if best is None:
            g = max(0, min(255, round(delinearized_f(ytarget))))
            return rgb2hex((g, g, g))
        lin = best
    rgb = [max(0, min(255, round(delinearized_f(max(0.0, c))))) for c in lin]
    return rgb2hex(rgb)


def is_yellow(h):
    return 105 <= h < 125


TONES = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 99, 100]


def tonal_palette(hue, chroma, tones=TONES):
    out = {}
    for t in tones:
        if t == 99 and is_yellow(hue):
            a = hex2rgb(hct_to_hex(hue, chroma, 98)); b = hex2rgb(hct_to_hex(hue, chroma, 100))
            out[t] = rgb2hex([round((x + y) / 2) for x, y in zip(a, b)])
        else:
            out[t] = hct_to_hex(hue, chroma, t)
    return out


def selftest():
    """拿 MCU 原庫的測試值核對（hct_test.ts、palettes_test.ts、concepts/color_spaces.md）。"""
    res = []
    for hx, exp in [('#ff0000', (27.408, 113.358, 46.445)), ('#00ff00', (142.140, 108.410, 79.332)),
                    ('#0000ff', (282.788, 87.231, 25.466))]:
        x, y, z = xyz_from_rgb255(*hex2rgb(hx))
        h, C, J = cam16_from_xyz(x, y, z)
        res.append((hx, 'cam16 h C J', (round(h, 3), round(C, 3), round(J, 3)), exp,
                    max(abs(h - exp[0]), abs(C - exp[1]), abs(J - exp[2])) < 2e-3))
    h, C, T = hct_from_hex('#ff6600')
    res.append(('#ff6600', 'HCT', (round(h, 2), round(C, 2), round(T, 2)), (42.39, 79.39, 62.31),
                max(abs(h - 42.39), abs(C - 79.39), abs(T - 62.31)) < 0.01))
    # palettes_test.ts: TonalPalette.fromInt(0xff0000ff)
    h, C, T = hct_from_hex('#0000ff')
    exp = {100: '#ffffff', 95: '#f1efff', 90: '#e0e0ff', 80: '#bec2ff', 70: '#9da3ff', 60: '#7c84ff',
           50: '#5a64ff', 40: '#343dff', 30: '#0000ef', 20: '#0001ac', 10: '#00006e', 0: '#000000'}
    pal = tonal_palette(h, C, list(exp))
    for t, e in exp.items():
        got = pal[t]
        dmax = max(abs(a - b) for a, b in zip(hex2rgb(got), hex2rgb(e)))
        res.append(('blue tone %d' % t, 'hex', got, e, dmax <= 1))
    return res


if __name__ == '__main__':
    ok = True
    for r in selftest():
        print(r)
        ok &= r[-1]
    print('ALL OK' if ok else 'FAIL')
