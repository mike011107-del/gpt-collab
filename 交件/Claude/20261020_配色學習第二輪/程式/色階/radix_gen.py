"""Radix 自訂色階產生器的 Python 改寫（只做亮色模式、實色 12 階，不做透明版與 P3 字串）。
依據：radix-ui/website 提交 402e749 components/generate-radix-colors.tsx
  色彩換算常數照 colorjs.io 0.5.2（npm 原始碼，website 鎖定這版）：oklab.js、srgb-linear.js、
  p3-linear.js、adapt.js（Bradford）、lab.js、toGamut.js（CSS 色域映射）、contrast/APCA.js
  bezier-easing 2.1.0 的曲線求值改用二分法。
Radix 原始 12 階：radix-ui/colors 提交 dbdb854 src/light.ts（P3 與 sRGB hex 兩套）。
"""
import math
import re
import sys

LIGHT_TS = '/tmp/claude-0/r2/src/radix-colors/repo/src/light.ts'

GRAY_NAMES = ['gray', 'mauve', 'slate', 'sage', 'olive', 'sand']
SCALE_NAMES = GRAY_NAMES + ['tomato', 'red', 'ruby', 'crimson', 'pink', 'plum', 'purple', 'violet', 'iris',
                            'indigo', 'blue', 'cyan', 'teal', 'jade', 'green', 'grass', 'brown', 'orange',
                            'sky', 'mint', 'lime', 'yellow', 'amber']
ALL_HEX_NAMES = SCALE_NAMES + ['gold', 'bronze']  # gold、bronze 不在產生器名單，但 light.ts 有

XYZ2LMS = [[0.8190224379967030, 0.3619062600528904, -0.1288737815209879],
           [0.0329836539323885, 0.9292868615863434, 0.0361446663506424],
           [0.0481771893596242, 0.2642395317527308, 0.6335478284694309]]
LMS2XYZ = [[1.2268798758459243, -0.5578149944602171, 0.2813910456659647],
           [-0.0405757452148008, 1.1122868032803170, -0.0717110580655164],
           [-0.0763729366746601, -0.4214933324022432, 1.5869240198367816]]
LMS2LAB = [[0.2104542683093140, 0.7936177747023054, -0.0040720430116193],
           [1.9779985324311684, -2.4285922420485799, 0.4505937096174110],
           [0.0259040424655478, 0.7827717124575296, -0.8086757549230774]]
LAB2LMS = [[1.0, 0.3963377773761749, 0.2158037573099136],
           [1.0, -0.1055613458156586, -0.0638541728258133],
           [1.0, -0.0894841775298119, -1.2914855480194092]]
SRGB2XYZ = [[0.41239079926595934, 0.357584339383878, 0.1804807884018343],
            [0.21263900587151027, 0.715168678767756, 0.07219231536073371],
            [0.01933081871559182, 0.11919477979462598, 0.9505321522496607]]
XYZ2SRGB = [[3.2409699419045226, -1.537383177570094, -0.4986107602930034],
            [-0.9692436362808796, 1.8759675015077202, 0.04155505740717559],
            [0.05563007969699366, -0.20397695888897652, 1.0569715142428786]]
P32XYZ = [[0.4865709486482162, 0.26566769316909306, 0.1982172852343625],
          [0.2289745640697488, 0.6917385218365064, 0.079286914093745],
          [0.0, 0.04511338185890264, 1.043944368900976]]
D65_TO_D50 = [[1.0479297925449969, 0.022946870601609652, -0.05019226628920524],
              [0.02962780877005599, 0.9904344267538799, -0.017073799063418826],
              [-0.009243040646204504, 0.015055191490298152, 0.7518742814281371]]
D50_TO_D65 = [[0.955473421488075, -0.02309845494876471, 0.06325924320057072],
              [-0.0283697093338637, 1.0099953980813041, 0.021041441191917323],
              [0.012314014864481998, -0.020507649298898964, 1.330365926242124]]
WD50 = [0.3457 / 0.3585, 1.0, (1.0 - 0.3457 - 0.3585) / 0.3585]


def mm(M, v):
    return [M[i][0] * v[0] + M[i][1] * v[1] + M[i][2] * v[2] for i in range(3)]


def cbrt(x):
    return math.copysign(abs(x) ** (1 / 3), x)


def dec(c):  # sRGB / P3 共用的轉換曲線（colorjs srgb.js）
    s = math.copysign(1, c); a = abs(c)
    return s * (a / 12.92 if a <= 0.04045 else ((a + 0.055) / 1.055) ** 2.4)


def enc(c):
    s = math.copysign(1, c); a = abs(c)
    return s * (1.055 * a ** (1 / 2.4) - 0.055 if a > 0.0031308 else 12.92 * a)


# ---- OKLCH 物件用 [L, C, H] list；H 可能是 nan ----
def oklab_from_xyz(xyz):
    lms = [cbrt(x) for x in mm(XYZ2LMS, xyz)]
    return mm(LMS2LAB, lms)


def xyz_from_oklab(lab):
    lms = [x ** 3 for x in mm(LAB2LMS, lab)]
    return mm(LMS2XYZ, lms)


def oklch_from_oklab(lab):
    L, a, b = lab
    if abs(a) < 0.0002 and abs(b) < 0.0002:
        h = float('nan')
    else:
        h = math.degrees(math.atan2(b, a)) % 360
    return [L, math.hypot(a, b), h]


def oklab_from_oklch(c):
    L, C, H = c
    if math.isnan(H):
        H = 0.0
    return [L, C * math.cos(math.radians(H)), C * math.sin(math.radians(H))]


def oklch_from_hex(h):
    h = h.lstrip('#')
    rgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return oklch_from_oklab(oklab_from_xyz(mm(SRGB2XYZ, [dec(c) for c in rgb])))


def oklch_from_p3(r, g, b):
    return oklch_from_oklab(oklab_from_xyz(mm(P32XYZ, [dec(r), dec(g), dec(b)])))


def srgb_from_oklch(c):
    return [enc(x) for x in mm(XYZ2SRGB, xyz_from_oklab(oklab_from_oklch(c)))]


def lab_from_oklch(c):  # CIELab D50（colorjs 'lab'）
    xyz = mm(D65_TO_D50, xyz_from_oklab(oklab_from_oklch(c)))
    e = 216 / 24389; k = 24389 / 27
    f = [cbrt(v / w) if v / w > e else (k * v / w + 16) / 116 for v, w in zip(xyz, WD50)]
    return [116 * f[1] - 16, 500 * (f[0] - f[1]), 200 * (f[1] - f[2])]


def oklch_from_lab(lab):
    e = 216 / 24389; k = 24389 / 27; e3 = 24 / 116
    f1 = (lab[0] + 16) / 116; f0 = lab[1] / 500 + f1; f2 = f1 - lab[2] / 200
    xyz = [f0 ** 3 if f0 > e3 else (116 * f0 - 16) / k,
           ((lab[0] + 16) / 116) ** 3 if lab[0] > k * e else lab[0] / k,
           f2 ** 3 if f2 > e3 else (116 * f2 - 16) / k]
    xyz = [v * w for v, w in zip(xyz, WD50)]
    return oklch_from_oklab(oklab_from_xyz(mm(D50_TO_D65, xyz)))


def mix_lab(a, b, p):
    la, lb = lab_from_oklch(a), lab_from_oklch(b)
    return oklch_from_lab([x + (y - x) * p for x, y in zip(la, lb)])


def deltaEOK(a, b):
    A, B = oklab_from_oklch(a), oklab_from_oklch(b)
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(A, B)))


def in_srgb(rgb, eps=0.0):
    return all(-eps <= c <= 1 + eps for c in rgb)


def to_gamut_css(c):
    """colorjs toGamutCSS，目標 sRGB。輸入輸出 oklch。"""
    L = c[0]
    if L >= 1:
        return [1, 0, float('nan')]
    if L <= 0:
        return [0, 0, float('nan')]
    if in_srgb(srgb_from_oklch(c)):
        return c

    def clip(cc):
        rgb = [min(1, max(0, x)) for x in srgb_from_oklch(cc)]
        return oklch_from_oklab(oklab_from_xyz(mm(SRGB2XYZ, [dec(x) for x in rgb])))
    JND = 0.02; eps = 0.0001
    lo, hi = 0.0, c[1]; lo_in = True
    cur = list(c); clipped = clip(cur)
    E = deltaEOK(clipped, cur)
    if E < JND:
        return clipped
    while hi - lo > eps:
        ch = (lo + hi) / 2; cur[1] = ch
        if lo_in and in_srgb(srgb_from_oklch(cur)):
            lo = ch
        else:
            clipped = clip(cur); E = deltaEOK(clipped, cur)
            if E < JND:
                if JND - E < eps:
                    break
                lo_in = False; lo = ch
            else:
                hi = ch
    return clipped


def to_hex(c):
    rgb = srgb_from_oklch(c)
    if not in_srgb(rgb, 0.000075):
        rgb = srgb_from_oklch(to_gamut_css(c))
        rgb = [min(1, max(0, x)) for x in rgb]
    return '#' + ''.join('%02x' % round(min(1, max(0, x)) * 255) for x in rgb)


def apca(bg_c, fg_c):
    """colorjs contrastAPCA(background, foreground)，APCA 0.0.98G。"""
    def Y(c):
        rgb = srgb_from_oklch(c)
        lin = [math.copysign(abs(x) ** 2.4, x) for x in rgb]
        return lin[0] * 0.2126729 + lin[1] * 0.7151522 + lin[2] * 0.0721750
    def clamp(y):
        return y if y >= 0.022 else y + (0.022 - y) ** 1.414
    yb, yt = clamp(Y(bg_c)), clamp(Y(fg_c))
    if abs(yb - yt) < 0.0005:
        return 0.0
    if yb > yt:
        s = (yb ** 0.56 - yt ** 0.57) * 1.14
        out = 0 if s < 0.1 else s - 0.027
    else:
        s = (yb ** 0.65 - yt ** 0.62) * 1.14
        out = 0 if s > -0.1 else s + 0.027
    return out * 100


def bezier(x1, y1, x2, y2):
    if x1 == y1 and x2 == y2:
        return lambda x: x
    def bz(t, a1, a2):
        return ((1 - 3 * a2 + 3 * a1) * t + (3 * a2 - 6 * a1)) * t * t + 3 * a1 * t
    def f(x):
        if x == 0 or x == 1:
            return x
        lo, hi = 0.0, 1.0
        for _ in range(80):
            m = (lo + hi) / 2
            if bz(m, x1, x2) > x:
                hi = m
            else:
                lo = m
        return bz((lo + hi) / 2, y1, y2)
    return f


LIGHT_EASE = (0, 2, 0, 2)


def transpose_start(to, arr, curve):
    fn = bezier(*curve); last = len(arr) - 1; diff = arr[0] - to
    return [n - diff * fn(1 - i / last) for i, n in enumerate(arr)]


def load_light_ts(path=LIGHT_TS):
    txt = open(path, encoding='utf-8').read()
    p3, hexes = {}, {}
    for m in re.finditer(r'export const (\w+) = \{(.*?)\};', txt, re.S):
        name, body = m.group(1), m.group(2)
        if name.endswith('P3') and not name.endswith('P3A'):
            base = name[:-2]
            vals = re.findall(r'color\(display-p3 ([\d.]+) ([\d.]+) ([\d.]+)\)', body)
            if len(vals) == 12:
                p3[base] = [tuple(float(x) for x in v) for v in vals]
        elif re.fullmatch(r'[a-z]+', name):
            vals = re.findall(r'"(#[0-9a-fA-F]{6})"', body)
            if len(vals) == 12:
                hexes[name] = vals
    return p3, hexes


P3, HEX = load_light_ts()
LIGHT = {n: [oklch_from_p3(*v) for v in P3[n]] for n in SCALE_NAMES}
LIGHT_GRAY = {n: LIGHT[n] for n in GRAY_NAMES}


def get_scale_from_color(source, scales, bg):
    allc = []
    for name, sc in scales.items():
        for col in sc:
            allc.append((deltaEOK(source, col), name, col))
    allc.sort(key=lambda x: x[0])
    seen = set(); closest = []
    for d, n, c in allc:
        if n not in seen:
            seen.add(n); closest.append((d, n, c))
    all_gray = all(n in GRAY_NAMES for _, n, _ in closest)
    if not all_gray and closest[0][1] in GRAY_NAMES:
        while closest[1][1] in GRAY_NAMES:
            closest.pop(1)
    A, B = closest[0], closest[1]
    a, b = B[0], A[0]
    c = deltaEOK(A[2], B[2])
    try:
        cosA = (b ** 2 + c ** 2 - a ** 2) / (2 * b * c)
        cosB = (a ** 2 + c ** 2 - b ** 2) / (2 * a * c)
        radA = math.acos(cosA); radB = math.acos(cosB)
        tanC1 = cosA / math.sin(radA); tanC2 = cosB / math.sin(radB)
        ratio = max(0.0, tanC1 / tanC2) * 0.5
    except (ValueError, ZeroDivisionError):
        ratio = float('nan')
    scale = [mix_lab(scales[A[1]][i], scales[B[1]][i], ratio) for i in range(12)]
    base = sorted(scale, key=lambda x: deltaEOK(source, x))[0]
    ratioC = source[1] / base[1]
    for col in scale:
        col[1] = min(source[1] * 1.5, col[1] * ratioC)
        col[2] = source[2]
    info = {'closest_scale': A[1], 'closest_dist': A[0], 'second_scale': B[1], 'second_dist': B[0],
            'mix_ratio_of_second': ratio}
    if scale[0][0] > 0.5:
        ls = [col[0] for col in scale]
        bgL = max(0, min(1, bg[0]))
        new = transpose_start(bgL, [1] + ls, LIGHT_EASE)[1:]
        for col, l in zip(scale, new):
            col[0] = l
        return scale, info
    raise NotImplementedError('dark mode not ported')


def get_text_color(bgc):
    white = [1, 0, float('nan')]
    if abs(apca(white, bgc)) < 40:
        return [0.25, max(0.08 * bgc[1], 0.04), bgc[2]]
    return white


def button_hover(src, scales):
    L, C, H = src
    nL = L - 0.03 / (L + 0.1) if L > 0.4 else L + 0.03 / (L + 0.1)
    nC = C * 0.93 if (L > 0.4 and not math.isnan(H)) else C
    hv = [nL, nC, H]
    best, md = hv, float('inf')
    for sc in scales:
        for col in sc:
            d = deltaEOK(hv, col)
            if d < md:
                md, best = d, col
    hv[1], hv[2] = best[1], best[2]
    return hv


def generate(accent, gray='#8B8D98', background='#FFFFFF'):
    bg = oklch_from_hex(background)
    gray_scale, ginfo = get_scale_from_color(oklch_from_hex(gray), LIGHT_GRAY, bg)
    src = oklch_from_hex(accent)
    acc, info = get_scale_from_color(src, LIGHT, bg)
    if deltaEOK(src, acc[0]) * 100 < 25:
        s9, contrast = acc[8], get_text_color(acc[8])
    else:
        s9, contrast = src, get_text_color(src)
    acc[8] = list(s9)
    acc[9] = button_hover(s9, [acc])
    for i in (10, 11):
        acc[i][1] = min(max(acc[8][1], acc[7][1]), acc[i][1])
    return {'accent': [to_hex(c) for c in acc], 'accent_oklch': [[round(x, 4) if not math.isnan(x) else None for x in c] for c in acc],
            'contrast_text': to_hex(contrast), 'gray': [to_hex(c) for c in gray_scale],
            'match': info, 'gray_match': ginfo}


if __name__ == '__main__':
    for a in sys.argv[1:]:
        print(a, generate(a))
