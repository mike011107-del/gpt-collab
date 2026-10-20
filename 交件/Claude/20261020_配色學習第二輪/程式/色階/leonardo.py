"""Adobe Leonardo「以對比值找顏色」的 Python 改寫（只做 LAB 與 RGB 內插、WCAG2、單一背景）。
依據：adobe/leonardo 提交 eb6481d packages/contrast-colors/lib/utils.js
  createScale()：白、色鍵、黑排成一條，色鍵位置 = 3000 - 3000 * (CIECAM02 J / 100)
  searchColors()：在 3000 格的色條上二分搜尋，找對比最接近目標的位置
  getContrast()：亮底時比底色深者為正值
chroma.js（gka/chroma.js 提交 14e2b8a）src/io/lab 常數：D65、kE、kK。
CIECAM02 參數照 lib/chroma-plus.js：La=40、Yb=20、average、不打折。
"""
import math

Xn, Yn, Zn = 0.95047, 1.0, 1.08883
kE, kK, kKE = 216.0 / 24389.0, 24389.0 / 27.0, 8.0
M = [[0.4124564390896922, 0.357576077643909, 0.18043748326639894],
     [0.21267285140562253, 0.715152155287818, 0.07217499330655958],
     [0.0193338955823293, 0.11919202588130297, 0.9503040785363679]]
MI = [[3.2404541621141045, -1.5371385127977166, -0.498531409556016],
      [-0.9692660305051868, 1.8760108454466942, 0.041556017530349834],
      [0.055643430959114726, -0.2040259135167538, 1.0572251882231791]]


def mm(A, v):
    return [A[i][0] * v[0] + A[i][1] * v[1] + A[i][2] * v[2] for i in range(3)]


def lin(c):
    s = math.copysign(1, c); c = abs(c)
    return s * (c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)


def comp(c):
    s = math.copysign(1, c); c = abs(c)
    return s * (c * 12.92 if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055)


def hex2rgb(h):
    h = h.lstrip('#'); return [int(h[i:i + 2], 16) for i in (0, 2, 4)]


def rgb2hex(rgb):
    return '#' + ''.join('%02x' % v for v in rgb)


def rgb2lab(rgb):
    x, y, z = mm(M, [lin(c / 255) for c in rgb])
    f = [r ** (1 / 3) if r > kE else (kK * r + 16) / 116 for r in (x / Xn, y / Yn, z / Zn)]
    return [116 * f[1] - 16, 500 * (f[0] - f[1]), 200 * (f[1] - f[2])]


def lab2rgb_float(lab):
    L, a, b = lab
    fy = (L + 16) / 116; fx = 0.002 * a + fy; fz = fy - 0.005 * b
    xr = fx ** 3 if fx ** 3 > kE else (116 * fx - 16) / kK
    yr = ((L + 16) / 116) ** 3 if L > kKE else L / kK
    zr = fz ** 3 if fz ** 3 > kE else (116 * fz - 16) / kK
    r = mm(MI, [xr * Xn, yr * Yn, zr * Zn])
    return [comp(c) * 255 for c in r]


def clip_round(rgbf):
    return [int(round(min(255, max(0, c)))) for c in rgbf]


# ---- CIECAM02 J（只算 J，用來決定色鍵在色條上的位置）----
CAT02 = [[0.7328, 0.4296, -0.1624], [-0.7036, 1.6975, 0.0061], [0.0030, 0.0136, 0.9834]]
CAT02I = [[1.096124, -0.278869, 0.182745], [0.454369, 0.473533, 0.072098], [-0.009628, -0.005698, 1.015326]]
HPE = [[0.38971, 0.68898, -0.07868], [-0.22981, 1.18340, 0.04641], [0.0, 0.0, 1.0]]
WP = [95.047, 100.0, 108.883]
La, Yb, F, c_, Nc = 40.0, 20.0, 1.0, 0.69, 1.0
k = 1 / (5 * La + 1)
FL = 0.2 * k ** 4 * (5 * La) + 0.1 * (1 - k ** 4) ** 2 * (5 * La) ** (1 / 3)
n = Yb / WP[1]; Nbb = 0.725 * n ** -0.2; z = 1.48 + math.sqrt(n)
D = F * (1 - (1 / 3.6) * math.exp((-La - 42) / 92))
RGBw = mm(CAT02, WP)


def _A(xyz):
    rgb = mm(CAT02, xyz)
    rgbc = [(D * WP[1] / w + 1 - D) * v for v, w in zip(rgb, RGBw)]
    rgbp = mm(HPE, mm(CAT02I, rgbc))
    ra = []
    for v in rgbp:
        t = (FL * abs(v) / 100) ** 0.42
        ra.append(math.copysign(400 * t / (27.13 + t), v) + 0.1)
    return (2 * ra[0] + ra[1] + ra[2] / 20 - 0.305) * Nbb


Aw = _A(WP)


def cam02_J(hexs):
    xyz = [v * 100 for v in mm(M, [lin(c / 255) for c in hex2rgb(hexs)])]
    A = _A(xyz)
    return 100 * (max(A, 0) / Aw) ** (c_ * z)


def lum(rgb):
    r = [lin(c / 255) for c in rgb]
    return 0.2126 * r[0] + 0.7152 * r[1] + 0.0722 * r[2]


def get_contrast(rgb, base, light_theme=True):
    cl, bl = lum(rgb), lum(base)
    cr1 = (cl + 0.05) / (bl + 0.05); cr2 = (bl + 0.05) / (cl + 0.05)
    if not light_theme:
        return cr1 if cr1 >= 1 else -cr2
    if cr1 < 1:
        return cr2
    if cr1 == 1:
        return cr1
    return -cr1


SW = 3000


def make_scale(keys, space='LAB'):
    """回傳 f(i), i 在 0..3000：白 -> 色鍵（依 J 排）-> 黑，分段線性內插。"""
    doms = sorted(SW - SW * (cam02_J(k) / 100) for k in keys) + [SW]
    doms = [0] + doms
    keys_sorted = sorted(keys, key=lambda k: -rgb2lab(hex2rgb(k))[0])  # 原程式用 HSLuv L 排；單一色鍵時無差別
    cols = ['#ffffff'] + keys_sorted + ['#000000']
    if space == 'LAB':
        pts = [rgb2lab(hex2rgb(c)) for c in cols]
        conv = lab2rgb_float
    else:
        pts = [hex2rgb(c) for c in cols]
        conv = lambda v: v

    def f(i):
        i = max(doms[0], min(doms[-1], i))
        for s in range(len(doms) - 1):
            if doms[s] <= i <= doms[s + 1]:
                span = doms[s + 1] - doms[s]
                t = 0 if span == 0 else (i - doms[s]) / span
                v = [a + (b - a) * t for a, b in zip(pts[s], pts[s + 1])]
                return clip_round(conv(v))
    return f


def search(keys, ratios, bg='#ffffff', space='LAB'):
    f = make_scale(keys, space)
    base = hex2rgb(bg)
    light = True  # 只做亮底
    cache = {}

    def gc(i):
        if i not in cache:
            cache[i] = get_contrast(f(i), base, light)
        return cache[i]
    out = []
    for x in ratios:
        first, last = gc(0), gc(SW)
        d = 1 if first < last else -1
        x = x + 0.005 * math.copysign(1, x)
        step = SW / 2; dot = step; val = gc(dot); cnt = 100
        while abs(val - x) > 0.01 and cnt:
            cnt -= 1; step /= 2
            dot = dot + step * d if val < x else dot - step * d
            val = gc(dot)
        rgb = f(round(dot, 3))
        out.append({'ratio_target': x - 0.005 * math.copysign(1, x), 'hex': rgb2hex(rgb),
                    'ratio_got': round(get_contrast(rgb, base, light), 2)})
    return out


def selftest():
    # searchColors.test.js：#0000ff、LAB、白底
    r1 = search(['#0000ff'], [3.12])
    r2 = search(['#0000ff'], [3, 4.5])
    exp1 = [[163, 121, 255]]; exp2 = [[167, 124, 255], [129, 84, 255]]
    got1 = [hex2rgb(x['hex']) for x in r1]; got2 = [hex2rgb(x['hex']) for x in r2]
    return [('3.12', got1, exp1, got1 == exp1), ('3,4.5', got2, exp2, got2 == exp2)]


if __name__ == '__main__':
    for t in selftest():
        print(t)
