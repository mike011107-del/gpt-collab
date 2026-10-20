# 各色彩系統的換算（只用 numpy），每個都附驗證用的已知值
import sys, json, math
sys.path.insert(0, '/tmp/claude-0/r2/theory')
sys.path.insert(0, '/home/user/gpt-collab/.claude/skills/colour-tool/scripts')
import numpy as np
import colourtool as ct  # WCAG、CIELAB、CIEDE2000、OKLCH、APCA（專案工具）
from munsell_conv import Inverter, load, hex2xyY_C, fmt, hue_name, M_RGB2XYZ, dec

_INV = None


def munsell(h):
    global _INV
    if _INV is None:
        _INV = Inverter(load('all'))
    x, y, Y = hex2xyY_C(h)
    m = _INV.xyY_to_munsell(x, y, Y)
    m['text'] = fmt(m)
    return m


# ---------- PCCS：Kobayashi & Yosiki 2001 公式，照 PyPI pccs 0.2a3 改寫 ----------
PCCS_TONES = {'p': (2, 8.6), 'p+': (3, 8.2), 'ltg': (2, 7.1), 'g': (2, 4.1), 'dkg': (2, 2.1),
              'lt': (5, 7.8), 'lt+': (6, 7.3), 'sf': (5, 6.3), 'd': (5, 4.8), 'dk': (5, 3.0),
              'b': (8, 6.6), 's': (8, 5.2), 'dp': (8, 4.1), 'v': (9, 5.5)}
PCCS_HUES = ['pR', 'R', 'yR', 'rO', 'O', 'yO', 'rY', 'Y', 'gY', 'YG', 'yG', 'G', 'bG', 'BG', 'BG', 'gB', 'B', 'B',
             'pB', 'V', 'bP', 'P', 'rP', 'RP']


def tilde_C(h, variant):
    if variant == 'as_written':  # 套件原樣：sin((h + 2.2 / 12 * pi))，運算順序疑似寫錯
        return 12 + 1.7 * math.sin(h + 2.2 / 12 * math.pi)
    return 12 + 1.7 * math.sin((h + 2.2) / 12 * math.pi)  # 補上括號的版本


def tilde_lambda(h):
    return 0.81 - 0.24 * math.sin((h - 2.6) / 12 * math.pi)


def pccs_to_munsellH_V_C(h, l, s, variant='as_written'):
    x = (h - 1) / 12 * math.pi
    H = (100 / (2 * math.pi) * x - 1.0 + 0.12 * math.cos(x) + 0.34 * math.cos(2 * x) + 0.40 * math.cos(3 * x)
         - 2.7 * math.sin(x) + 1.5 * math.sin(2 * x) - 0.40 * math.sin(3 * x))
    C = tilde_C(h, variant) * (0.077 * s + 0.0040 * s ** 2) * (1 - math.exp(-tilde_lambda(h) * l))
    return H % 100, l, C


def munsell_to_pccs(H, V, C, variant='as_written'):
    if H is None or C < 0.3:
        return {'h': None, 'l': V, 's': 0.0, 'tone': 'N'}
    y = H / 50 * math.pi
    h = (24 / (2 * math.pi) * y + 1.24 + 0.020 * math.cos(y) - 0.10 * math.cos(2 * y) - 0.11 * math.cos(3 * y)
         + 0.68 * math.sin(y) - 0.30 * math.sin(2 * y) + 0.013 * math.sin(3 * y))
    h = ((h - 1) % 24) + 1
    K = C / (tilde_C(h, variant) * (1 - math.exp(-tilde_lambda(h) * V)))
    s = (-0.077 + math.sqrt(0.077 ** 2 + 4 * 0.004 * K)) / (2 * 0.004)
    return {'h': h, 'l': V, 's': s, 'tone': pccs_tone(h, V, s), 'tone_raw_code': pccs_tone_buggy(h, V, s)}


def _t(h, l, s):
    return l - (0.25 - 0.34 * math.sqrt(max(0.0, 1 - math.sin((h - 2) / 12 * math.pi)))) * s


def pccs_tone(h, l, s):  # 歐氏距離（修正套件的距離式）
    t = _t(h, l, s)
    return min(PCCS_TONES, key=lambda k: (PCCS_TONES[k][0] - s) ** 2 + (PCCS_TONES[k][1] - t) ** 2)


def pccs_tone_buggy(h, l, s):  # 套件原樣：((s0-s)**2 + (t0-t))**2
    t = _t(h, l, s)
    return min(PCCS_TONES, key=lambda k: ((PCCS_TONES[k][0] - s) ** 2 + (PCCS_TONES[k][1] - t)) ** 2)


def pccs_hue_label(h):
    if h is None:
        return 'n'
    k = int(round(h))
    k = ((k - 1) % 24) + 1
    return f'{k}:{PCCS_HUES[k - 1]}'


# ---------- OSA-UCS：colour-science models/osa_ucs.py（Moroney 2003、Schlömer 2019 係數） ----------
M_OSA = np.array([[0.799, 0.4194, -0.1648], [-0.4493, 1.3265, 0.0927], [-0.1149, 0.3394, 0.717]])
VJ = np.array([1.7, 8.0, -9.7]); VG = np.array([-13.7, 17.7, -4.0])


def osa_ucs_XYZ(XYZ):
    XYZ = np.asarray(XYZ, float)
    s = XYZ.sum(); x, y, Y = XYZ[0] / s, XYZ[1] / s, XYZ[1]
    Y0 = Y * (4.4934 * x ** 2 + 4.3034 * y ** 2 - 4.276 * x * y - 1.3744 * x - 2.5643 * y + 1.8103)
    Y0es = np.cbrt(Y0) - 2 / 3
    Lam = 5.9 * (Y0es + 0.042 * np.cbrt(Y0 - 30))
    RGB3 = np.cbrt(M_OSA @ XYZ)
    C = Lam / (5.9 * Y0es)
    return float((Lam - 14.4) / math.sqrt(2)), float(C * RGB3 @ VJ), float(C * RGB3 @ VG)


def hex2XYZ65(h):
    h = h.lstrip('#')
    rgb = np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)])
    return (M_RGB2XYZ @ dec(rgb)) * 100


def osa_ucs(h):  # 注意：OSA-UCS 定義用 10° 觀察者，這裡用 sRGB 的 2° XYZ 近似
    return osa_ucs_XYZ(hex2XYZ65(h))


# ---------- CIECAM02：colour-science appearance/ciecam02.py、hunt.py、adaptation/datasets/cat.py ----------
CAT02 = np.array([[0.7328, 0.4296, -0.1624], [-0.7036, 1.6975, 0.0061], [0.0030, 0.0136, 0.9834]])
HPE = np.array([[0.38971, 0.68898, -0.07868], [-0.22981, 1.18340, 0.04641], [0.0, 0.0, 1.0]])


def ciecam02(XYZ, XYZ_w, L_A, Y_b, F=1.0, c=0.69, N_c=1.0):
    XYZ = np.asarray(XYZ, float); XYZ_w = np.asarray(XYZ_w, float)
    Y_w = XYZ_w[1]
    n = Y_b / Y_w
    k = 1 / (5 * L_A + 1); k4 = k ** 4
    F_L = 0.2 * k4 * (5 * L_A) + 0.1 * (1 - k4) ** 2 * (5 * L_A) ** (1 / 3)
    N_bb = N_cb = 0.725 * (1 / n) ** 0.2
    z = 1.48 + math.sqrt(n)
    D = F * (1 - (1 / 3.6) * math.exp((-L_A - 42) / 92))
    RGB = CAT02 @ XYZ; RGB_w = CAT02 @ XYZ_w
    RGB_c = (Y_w * D / RGB_w + 1 - D) * RGB
    RGB_wc = (Y_w * D / RGB_w + 1 - D) * RGB_w
    Mx = HPE @ np.linalg.inv(CAT02)
    def comp(v):
        p = Mx @ v
        f = (F_L * np.abs(p) / 100) ** 0.42
        return 400 * np.sign(p) * f / (27.13 + f) + 0.1
    Ra, Ga, Ba = comp(RGB_c); Rw, Gw, Bw = comp(RGB_wc)
    a = Ra - 12 * Ga / 11 + Ba / 11; b = (Ra + Ga - 2 * Ba) / 9
    h = math.degrees(math.atan2(b, a)) % 360
    e_t = 0.25 * (math.cos(2 + math.radians(h)) + 3.8)
    A = (2 * Ra + Ga + Ba / 20 - 0.305) * N_bb
    A_w = (2 * Rw + Gw + Bw / 20 - 0.305) * N_bb
    J = 100 * (A / A_w) ** (c * z)
    t = (50000 / 13) * N_c * N_cb * e_t * math.sqrt(a * a + b * b) / (Ra + Ga + 21 * Ba / 20)
    C = t ** 0.9 * math.sqrt(J / 100) * (1.64 - 0.29 ** n) ** 0.73
    return {'J': J, 'C': C, 'h': h}


# ---------- ISCC-NBS：color-name-lists 3.34.0 的 nbs-iscc.json（267 個中心色，CC0）----------
_NBS = None


def iscc_nbs_nearest(h, k=1):
    global _NBS
    if _NBS is None:
        _NBS = json.load(open('/tmp/claude-0/r2/src/npm-color-name-lists/x/package/lib/colors/nbs-iscc.json'))
    d = sorted(((ct.de(h, e['hex']), e['name'], e['hex'].upper()) for e in _NBS))
    return [{'name': n, 'hex': x, 'dE2000': round(v, 1)} for v, n, x in d[:k]]
