# Matsuda 色相模板（經 Cohen-Or 等 2006 的實作轉述）：tartarskunk/ColorHarmonization commit b789279 color_harmonization.py 第 10–18 行
# 模板 = 色相環上的扇形（中心、寬度，以一圈為 1）。問：48 家同業 logo 的色相落在哪幾種模板裡？隨機色相又有多少能放進去？
import sys, json, colorsys, math
sys.path.insert(0, '/home/user/gpt-collab/.claude/skills/colour-tool/scripts')
import numpy as np
import colourtool as ct

T = {"i": [(0.00, 0.05)], "V": [(0.00, 0.26)], "L": [(0.00, 0.05), (0.25, 0.22)], "mirror_L": [(0.00, 0.05), (-0.25, 0.22)],
     "I": [(0.00, 0.05), (0.50, 0.05)], "T": [(0.25, 0.50)], "Y": [(0.00, 0.26), (0.50, 0.05)], "X": [(0.00, 0.26), (0.50, 0.26)]}


def fits(hues, sectors):  # hues 以一圈為 1
    # 10-19 修正：原本試 720 個旋轉角（0.5° 步長），會漏掉色相差接近 180° 時 T 型（半圈）剛好放得進的情形。
    # 改成精確判定：可行的旋轉若存在，必有一個是「某個色相正好落在某個扇形邊上」，所以只要試這些候選角。
    cands = [h - c + sgn * w / 2 for h in hues for c, w in sectors for sgn in (-1, 1)]
    for r in cands:
        if all(any(abs(((h - (c + r)) + 0.5) % 1 - 0.5) <= w / 2 + 1e-9 for c, w in sectors) for h in hues):
            return True
    return False


def hsv_h(hx):
    # 10-19 修正：ct.rgb 回傳 0–255 整數，原本寫 r/255 if r>1，會把通道值 1（例 PUB #0172BB 的 R=1）當成滿值 1.0。
    r, g, b = ct.rgb(hx)
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    return h, s


peers = json.load(open('/tmp/claude-0/work/peer_schemes.json'))
rows = []
for p in peers:
    hs = [hsv_h(c)[0] for c in p['cols'] if ct.oklch(c)[1] >= 0.04]
    if len(hs) < 2: continue
    hok = [ct.oklch(c)[2] / 360 for c in p['cols'] if ct.oklch(c)[1] >= 0.04]
    rows.append({'peer': p['name'], 'n_chromatic': len(hs), 'cols': p['cols'],
                 'fits_hsv': [k for k, s in T.items() if fits(hs, s)], 'fits_oklch': [k for k, s in T.items() if fits(hok, s)]})
# 隨機基準：同樣色彩數的隨機色相
rng = np.random.default_rng(5); base = {}
for n in (2, 3, 4):
    cnt = {k: 0 for k in T}; N = 2000
    for _ in range(N):
        hs = list(rng.random(n))
        for k, s in T.items():
            if fits(hs, s): cnt[k] += 1
    base[n] = {k: round(v / N, 3) for k, v in cnt.items()}
out = {'source': 'github.com/tartarskunk/ColorHarmonization commit b78927988c0c66dc022abffd9fe3c3fd69050757（Cohen-Or 2006 實作；模板源自 Matsuda，原著未取得）',
       'templates': T, 'peers': rows, 'random_hues_fit_share': base,
       'note': '色相用 HSV（跟實作一樣）另附 OKLCH；近灰（OKLCH C<0.04）不算。T 型是 180° 半圈，任兩個色相的最短弧都 ≤180°，一定放得進（幾何上 100%）；X 型兩個 93.6° 扇形相對，任兩色也一定放得進。10-19 修正：旋轉改精確判定、hsv_h 通道值修正、隨機基準改 2000 組。'}
json.dump(out, open('/tmp/claude-0/r2/theory/matsuda_templates.json', 'w'), ensure_ascii=False, indent=1)
for r in rows: print(r['peer'], r['n_chromatic'], r['fits_hsv'], '| ok:', r['fits_oklch'])
print(base)
