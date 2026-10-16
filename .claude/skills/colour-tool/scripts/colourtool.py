#!/usr/bin/env python3
"""色彩計算與取色工具（只用標準函式庫；image 子命令另需 Pillow）。

用法：
  python3 colourtool.py selftest
  python3 colourtool.py info '#FACA30' '#14A5B3'
  python3 colourtool.py pair '#FACA30' '#14A5B3'      # 前景 背景
  python3 colourtool.py peak [--step 10]
  python3 colourtool.py image 圖檔.png [--k 8]
加 --json 輸出機器可讀結果。

色彩數學沿用 交件/Claude/20261014_第十五輪雲端重跑/check.py（已用 Sharma 2005 測試資料驗過）。
限制：只處理不透明 sRGB 螢幕色；不代表印刷、油漆或實物色。
"""
import json
import math
import sys

# ---------- sRGB ----------
def rgb(h):
    raw = h
    h = h.strip().lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    if len(h) != 6 or any(c not in '0123456789abcdefABCDEF' for c in h):
        raise ValueError(f'不是 HEX 色碼（要 #RRGGBB 或 #RGB）：{raw!r}')
    return [int(h[i:i + 2], 16) for i in (0, 2, 4)]

def hx(c):
    return '#%02X%02X%02X' % tuple(max(0, min(255, round(v))) for v in c)

def dec(v):  # IEC 61966-2-1 解碼；WCAG 2.2 也用 0.04045
    v /= 255
    return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4

def enc(v):
    v = max(0.0, min(1.0, v))
    return 255 * (12.92 * v if v <= 0.0031308 else 1.055 * v ** (1 / 2.4) - 0.055)

def lin3(h):
    return [dec(v) for v in rgb(h)]

def from_lin(c):
    return hx([enc(v) for v in c])

def lum(h):
    r, g, b = lin3(h)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contrast(a, b):  # WCAG 2.x
    x, y = sorted([lum(a), lum(b)], reverse=True)
    return (x + 0.05) / (y + 0.05)

# ---------- CIELAB（D65）----------
M = [[0.4124564, 0.3575761, 0.1804375], [0.2126729, 0.7151522, 0.0721750], [0.0193339, 0.1191920, 0.9503041]]
WHITE = [sum(r) for r in M]
EPS, KAP = 216 / 24389, 24389 / 27

def lab_from_lin(c):
    X, Y, Z = [sum(M[i][j] * c[j] for j in range(3)) / WHITE[i] for i in range(3)]
    f = lambda t: t ** (1 / 3) if t > EPS else (KAP * t + 16) / 116
    return (116 * f(Y) - 16, 500 * (f(X) - f(Y)), 200 * (f(Y) - f(Z)))

def lab(h):
    return lab_from_lin(lin3(h))

def lch(h):
    L, a, b = lab(h)
    return L, math.hypot(a, b), math.degrees(math.atan2(b, a)) % 360

# ---------- OKLab（Ottosson 2020）----------
def oklch(h):
    r, g, b = lin3(h)
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l, m, s = (math.copysign(abs(v) ** (1 / 3), v) for v in (l, m, s))
    L = 0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s
    a = 1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s
    bb = 0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s
    return L, math.hypot(a, bb), math.degrees(math.atan2(bb, a)) % 360

# ---------- CIEDE2000（Sharma, Wu, Dalal 2005）----------
def de2000_lab(l1, l2):
    L1, a1, b1 = l1; L2, a2, b2 = l2
    C1 = math.hypot(a1, b1); C2 = math.hypot(a2, b2); Cb = (C1 + C2) / 2
    G = 0.5 * (1 - math.sqrt(Cb ** 7 / (Cb ** 7 + 25 ** 7)))
    a1p, a2p = (1 + G) * a1, (1 + G) * a2
    C1p, C2p = math.hypot(a1p, b1), math.hypot(a2p, b2)
    h1p = math.degrees(math.atan2(b1, a1p)) % 360 if (a1p or b1) else 0.0
    h2p = math.degrees(math.atan2(b2, a2p)) % 360 if (a2p or b2) else 0.0
    dL = L2 - L1; dC = C2p - C1p
    if C1p * C2p == 0:
        dh = 0
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
    T = (1 - 0.17 * math.cos(math.radians(hb - 30)) + 0.24 * math.cos(math.radians(2 * hb))
         + 0.32 * math.cos(math.radians(3 * hb + 6)) - 0.20 * math.cos(math.radians(4 * hb - 63)))
    dth = 30 * math.exp(-((hb - 275) / 25) ** 2); RC = 2 * math.sqrt(Cbp ** 7 / (Cbp ** 7 + 25 ** 7))
    SL = 1 + 0.015 * (Lb - 50) ** 2 / math.sqrt(20 + (Lb - 50) ** 2); SC = 1 + 0.045 * Cbp
    SH = 1 + 0.015 * Cbp * T; RT = -math.sin(math.radians(2 * dth)) * RC
    return math.sqrt((dL / SL) ** 2 + (dC / SC) ** 2 + (dH / SH) ** 2 + RT * (dC / SC) * (dH / SH))

def de(h1, h2):
    return de2000_lab(lab(h1), lab(h2))

# ---------- 色弱模擬（Machado 2009，severity 1.0，線性 RGB）----------
MACH = {'protan': [[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048116, 1.051998]],
        'deutan': [[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]],
        'tritan': [[1.255528, -0.076749, -0.178779], [-0.078411, 0.930809, 0.147602], [0.004733, 0.691367, 0.303900]]}

def cvd(h, kind):
    c = lin3(h); m = MACH[kind]
    return from_lin([sum(m[i][j] * c[j] for j in range(3)) for i in range(3)])

# ---------- APCA 0.1.9（apca-w3 常數）----------
def apca(text, bg):
    def Y(h):
        r, g, b = [v / 255 for v in rgb(h)]
        return 0.2126729 * r ** 2.4 + 0.7151522 * g ** 2.4 + 0.0721750 * b ** 2.4
    t, b = Y(text), Y(bg)
    t = t if t > 0.022 else t + (0.022 - t) ** 1.414
    b = b if b > 0.022 else b + (0.022 - b) ** 1.414
    if abs(b - t) < 0.0005:
        return 0.0
    if b > t:
        s = (b ** 0.56 - t ** 0.57) * 1.14; out = 0 if s < 0.1 else s - 0.027
    else:
        s = (b ** 0.65 - t ** 0.62) * 1.14; out = 0 if s > -0.1 else s + 0.027
    return out * 100

# ---------- USWDS 明度級（uswds-site overview.md 的亮度表）----------
GRADES = [(0, 1.0, 1.0), (5, .85, .93), (10, .75, .82), (20, .5, .65), (30, .35, .45), (40, .225, .3),
          (50, .175, .183), (60, .1, .125), (70, .05, .07), (80, .02, .04), (90, .005, .015), (100, 0.0, 0.0)]

def uswds_grade(h):
    """回傳 (落在哪一級, 是否在該級範圍內)。不在任何一級範圍內時，回傳亮度最接近的一級與 False。"""
    y = lum(h)
    for g, lo, hi in GRADES:
        if lo <= y <= hi:
            return g, True
    g = min(GRADES, key=lambda t: min(abs(y - t[1]), abs(y - t[2])))[0]
    return g, False

# ---------- 子命令 ----------
SHARMA = [
    (50.0000, 2.6772, -79.7751, 50.0000, 0.0000, -82.7485, 2.0425),
    (50.0000, 0.0000, 0.0000, 50.0000, -1.0000, 2.0000, 2.3669),
    (50.0000, 2.5000, 0.0000, 73.0000, 25.0000, -18.0000, 27.1492),
    (60.2574, -34.0099, 36.2677, 60.4626, -34.1751, 39.4387, 1.2644),
    (2.0776, 0.0795, -1.1350, 0.9033, -0.0636, -0.5514, 0.9082),
]

def cmd_selftest(args):
    errs, notes = [], []
    for t in SHARMA:
        got = de2000_lab(t[0:3], t[3:6])
        if abs(got - t[6]) > 1e-4:
            errs.append(f'CIEDE2000 {t} 得 {got:.4f}')
    if abs(contrast('#000000', '#FFFFFF') - 21) > 1e-9:
        errs.append('WCAG 黑白對比不是 21')
    L, a, b = lab('#FFFFFF')
    if abs(L - 100) > 1e-6 or abs(a) > 1e-6 or abs(b) > 1e-6:
        errs.append('白色 Lab 不是 (100,0,0)')
    Lok, Cok, _ = oklch('#FFFFFF')
    if abs(Lok - 1) > 1e-3 or Cok > 1e-3:
        errs.append(f'白色 OKLCH 不是 (1,0)：{Lok},{Cok}')
    for k in MACH:
        for row in MACH[k]:
            if abs(sum(row) - 1) > 1e-3:
                errs.append(f'{k} 矩陣列和 {sum(row)}')
    # 用另一套獨立實作交叉驗算（有裝 coloraide 才跑）
    try:
        from coloraide import Color
        samples = ['#FACA30', '#14A5B3', '#086A74', '#081C2F', '#FFFFFF', '#000000', '#7F7F7F']
        worst = {'wcag': 0, 'lab': 0, 'oklch_L': 0, 'de2000': 0}
        for i, h in enumerate(samples):
            c = Color(h)
            worst['wcag'] = max(worst['wcag'], abs(contrast(h, '#FFFFFF') - c.contrast('#FFFFFF', method='wcag21')))
            lc = c.convert('lab-d65').coords()
            worst['lab'] = max(worst['lab'], max(abs(x - y) for x, y in zip(lab(h), lc)))
            worst['oklch_L'] = max(worst['oklch_L'], abs(oklch(h)[0] - c.convert('oklch').coords()[0]))
            j = samples[(i + 1) % len(samples)]
            worst['de2000'] = max(worst['de2000'], abs(de(h, j) - Color(h).delta_e(j, method='2000')))
        notes.append('與 coloraide 交叉驗算最大差：' + json.dumps({k: float(f'{v:.2e}') for k, v in worst.items()}))
        # WCAG：本工具照 WCAG 原文用四位小數係數 0.2126/0.7152/0.0722，coloraide 用完整矩陣，差約 2e-4 屬定義差
        if worst['wcag'] > 1e-3 or worst['oklch_L'] > 1e-4:
            errs.append(f'與 coloraide 差異過大：{worst}')
        # Lab 與 ΔE2000：coloraide 的 lab-d65 白點常數與本工具不同，只作參考，差 0.05 以內視為一致
        if worst['lab'] > 0.05 or worst['de2000'] > 0.05:
            errs.append(f'Lab／ΔE2000 與 coloraide 差異超過 0.05：{worst}')
    except ImportError:
        notes.append('沒有安裝 coloraide，跳過獨立實作交叉驗算')
    return {'通過': not errs, '錯誤': errs, '附註': notes}

def cmd_info(args):
    out = []
    for h in args:
        L, C, H = lch(h); Lo, Co, Ho = oklch(h); g, ok = uswds_grade(h)
        out.append({'hex': hx(rgb(h)), '相對亮度Y': round(lum(h), 4), 'L*': round(L, 1), 'C*': round(C, 1),
                    'h°': round(H), 'OKLCH': [round(Lo, 3), round(Co, 3), round(Ho)],
                    'USWDS級': g, '在該級範圍內': ok,
                    '對白': round(contrast(h, '#FFFFFF'), 2), '對黑': round(contrast(h, '#000000'), 2)})
    return out

def cmd_pair(args):
    if len(args) != 2:
        raise SystemExit('pair 需要兩個色碼：前景 背景')
    fg, bg = args
    r = {'前景': hx(rgb(fg)), '背景': hx(rgb(bg)), 'WCAG對比': round(contrast(fg, bg), 3),
         'APCA_Lc': round(apca(fg, bg), 1), 'ΔE2000': round(de(fg, bg), 2),
         'L*差': round(abs(lab(fg)[0] - lab(bg)[0]), 1),
         'USWDS級差': abs(uswds_grade(fg)[0] - uswds_grade(bg)[0]), '色弱模擬': {}}
    for k in MACH:
        a, b = cvd(fg, k), cvd(bg, k)
        r['色弱模擬'][k] = {'前景': a, '背景': b, 'WCAG對比': round(contrast(a, b), 3), 'ΔE2000': round(de(a, b), 2)}
    r['門檻參考'] = 'WCAG 一般文字 4.5、大字 3；只是螢幕不透明色對，不代表字形、字級、實物'
    return r

def cmd_peak(args):
    step = 10
    if '--step' in args:
        step = int(args[args.index('--step') + 1])
    N = 48
    best = {}
    for i in range(N + 1):
        for j in range(N + 1):
            for k in range(N + 1):
                c = [dec(v * 255 / N) for v in (i, j, k)]
                L, a, b = lab_from_lin(c)
                C = math.hypot(a, b); Hh = math.degrees(math.atan2(b, a)) % 360
                key = int(Hh // step) * step
                if C > best.get(key, (0,))[0]:
                    best[key] = (C, L, hx([v * 255 / N for v in (i, j, k)]))
    return [{'h範圍': f'{k}-{k + step - 1}', '最鮮豔時L*': round(v[1], 1), 'C*': round(v[0], 1), '色碼': v[2]}
            for k, v in sorted(best.items())]

def cmd_image(args):
    from PIL import Image
    path = args[0]; k = 8
    if '--k' in args:
        k = int(args[args.index('--k') + 1])
    im = Image.open(path).convert('RGB')
    w, h = im.size
    small = im.copy(); small.thumbnail((400, 400))
    q = small.quantize(colors=k, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()[:3 * k]
    counts = sorted(q.getcolors(), reverse=True)
    total = sum(c for c, _ in counts)
    rows = []
    for c, idx in counts:
        hexc = hx(pal[3 * idx:3 * idx + 3]); L, C, H = lch(hexc)
        rows.append({'色碼': hexc, '面積%': round(100 * c / total, 1), 'L*': round(L, 1), 'C*': round(C, 1), 'h°': round(H)})
    return {'檔案': path, '尺寸': [w, h], '取色數': k,
            '附註': '中位切割量化的近似代表色；壓縮、光線、陰影都會影響，不等於品牌標準色', '代表色': rows}

CMDS = {'selftest': cmd_selftest, 'info': cmd_info, 'pair': cmd_pair, 'peak': cmd_peak, 'image': cmd_image}

def main(argv):
    if not argv or argv[0] not in CMDS:
        print(__doc__); return 2
    as_json = '--json' in argv
    args = [a for a in argv[1:] if a != '--json']
    res = CMDS[argv[0]](args)
    if as_json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
    else:
        rows = res if isinstance(res, list) else [res]
        for r in rows:
            print(json.dumps(r, ensure_ascii=False))
    if argv[0] == 'selftest' and not res['通過']:
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
