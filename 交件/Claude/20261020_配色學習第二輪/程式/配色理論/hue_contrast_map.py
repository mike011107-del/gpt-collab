# (1) 「幾個色相 × 多大對比」：把 48 家同業 logo 放上兩軸（色相群數、最大 L* 差、最大 ΔE2000）
# (2) 相對彩度：每個顏色的 OKLCH 彩度 ÷ 同明度同色相在 sRGB 能到的最大彩度（看是「深而飽和」還是「暗而灰」）
# (3) 各色相最鮮豔點的明度（每個色相面的形狀不同）
import sys, json, math, itertools
sys.path.insert(0, '/home/user/gpt-collab/.claude/skills/colour-tool/scripts')
import numpy as np
import colourtool as ct

M1 = np.array([[1.0, 0.3963377774, 0.2158037573], [1.0, -0.1055613458, -0.0638541728], [1.0, -0.0894841775, -1.2914855480]])
M2 = np.array([[4.0767416621, -3.3077115913, 0.2309699292], [-1.2684380046, 2.6097574011, -0.3413193965], [-0.0041960863, -0.7034186147, 1.7076147010]])


def oklch_to_lin(L, C, h):
    a, b = C * math.cos(math.radians(h)), C * math.sin(math.radians(h))
    lms = (M1 @ np.array([L, a, b])) ** 3
    return M2 @ lms


def max_chroma(L, h):
    lo, hi = 0.0, 0.5
    for _ in range(40):
        mid = (lo + hi) / 2
        rgb = oklch_to_lin(L, mid, h)
        if (rgb >= -1e-6).all() and (rgb <= 1 + 1e-6).all(): lo = mid
        else: hi = mid
    return lo


def rel_chroma(hx):
    L, C, h = ct.oklch(hx)
    m = max_chroma(L, h)
    return round(C / m, 3) if m > 1e-4 else 0.0, round(m, 3)


# 驗證 oklch_to_lin：拿幾個 hex 來回
chk = []
for hx in ['#D68702', '#0C424A', '#333D66', '#FF0000', '#00FF00', '#0000FF', '#777777']:
    L, C, h = ct.oklch(hx)
    lin = oklch_to_lin(L, C, h)
    chk.append(round(float(np.abs(lin - np.array(ct.lin3(hx))).max()), 6))

peers = json.load(open('/tmp/claude-0/work/peer_schemes.json'))
pts = []
for p in peers:
    cols = p['cols']; allc = cols + p['neutral']
    hs = sorted(ct.oklch(c)[2] for c in cols if ct.oklch(c)[1] >= 0.04)
    g = 0
    if hs:
        g = 1
        for x, y in zip(hs, hs[1:]):
            if y - x >= 30: g += 1
        if len(hs) > 1 and (hs[0] + 360 - hs[-1]) < 30 and g > 1: g -= 1
    dLs = [abs(ct.lab(a)[0] - ct.lab(b)[0]) for a, b in itertools.combinations(allc, 2)]
    dEs = [ct.de(a, b) for a, b in itertools.combinations(allc, 2)]
    # 加白底：logo 多半放在白底上
    dLw = [100 - ct.lab(c)[0] for c in allc]
    pts.append({'peer': p['name'], 'group': p['t'], 'n_hues': g, 'n_colours_listed': len(allc),
                'max_dL_within': round(max(dLs), 1) if dLs else 0.0, 'max_dE_within': round(max(dEs), 1) if dEs else 0.0,
                'max_dL_vs_white': round(max(dLw), 1) if dLw else 0.0,
                'rel_chroma_main': rel_chroma(cols[0])[0] if cols else None, 'main': cols[0] if cols else (p['neutral'][0] if p['neutral'] else None)})

from collections import Counter
cnt = Counter(r['n_hues'] for r in pts)
by = {}
for k in sorted(cnt):
    sub = [r['max_dL_within'] for r in pts if r['n_hues'] == k and r['n_colours_listed'] > 1]
    by[k] = {'n_peers': cnt[k], 'n_with_2plus_colours': len(sub), 'median_max_dL_within': round(float(np.median(sub)), 1) if sub else None}

rel = {k: dict(zip(['rel_chroma', 'max_okC_at_same_L_h'], rel_chroma(v))) for k, v in {'深青': '#0C424A', '靛藍': '#333D66', '工程黃': '#D68702'}.items()}
main_rel = [r['rel_chroma_main'] for r in pts if r['rel_chroma_main'] is not None]
# 隨機基準：均勻 sRGB 色的相對彩度（去掉 OKLCH C < 0.04）
rng = np.random.default_rng(3); rr = []
for _ in range(3000):
    hx = '#' + ''.join(f'{v:02X}' for v in rng.integers(0, 256, 3))
    if ct.oklch(hx)[1] >= 0.04: rr.append(rel_chroma(hx)[0])
# 各色相最鮮豔點的明度
cusp = []
for h in range(0, 360, 15):
    best = max(((max_chroma(L, h), L) for L in np.arange(0.2, 0.99, 0.005)))
    cusp.append({'okh': h, 'cusp_L': round(float(best[1]), 3), 'cusp_C': round(best[0], 3)})
# 10-19 修正：上面 15° 取樣會漏掉 110° 附近（sRGB 純黃 #FFFF00）的尖點。改用細取樣：
# sRGB 各色相最鮮點（尖點）一定在立方體「一個通道 1、一個通道 0」的六條邊上，沿邊取 2 萬點算 OKLCH，再內插到每 1°。
Minv1, Minv2 = np.linalg.inv(M1), np.linalg.inv(M2)
tt = np.linspace(0, 1, 20001); E = []
for one in range(3):
    for zero in range(3):
        if one == zero: continue
        var = 3 - one - zero; rgb = np.zeros((len(tt), 3)); rgb[:, one] = 1; rgb[:, var] = tt; E.append(rgb)
E = np.vstack(E)  # 線性 RGB（邊上 0/1 在線性與編碼空間相同，中間值取線性）
lab_ = (Minv1 @ np.cbrt(Minv2 @ E.T)).T
eh = np.degrees(np.arctan2(lab_[:, 2], lab_[:, 1])) % 360; eL = lab_[:, 0]; eC = np.hypot(lab_[:, 1], lab_[:, 2])
o = np.argsort(eh); eh, eL, eC = eh[o], eL[o], eC[o]
hh = np.arange(0, 360, 1.0)
cL = np.interp(hh, eh, eL, period=360); cC = np.interp(hh, eh, eC, period=360)
imax = int(np.argmax(eL)); jmax = int(np.argmax(cL))
cusp_fine = {'method': 'sRGB 立方體六條邊各 20001 點，OKLCH 內插到每 1°',
             'by_hue_1deg': [{'okh': int(a), 'cusp_L': round(float(b), 3), 'cusp_C': round(float(c), 3)} for a, b, c in zip(hh, cL, cC)],
             'highest_cusp': {'okh': round(float(eh[imax]), 1), 'cusp_L': round(float(eL[imax]), 3), 'cusp_C': round(float(eC[imax]), 3),
                              'srgb_hex_check': '#FFFF00', 'hex_oklch': [round(float(v), 3) for v in ct.oklch('#FFFF00')]},
             'check_15deg_vs_fine': {int(a): {'coarse': c['cusp_L'], 'fine': round(float(np.interp(a, eh, eL, period=360)), 3)} for a, c in zip(range(0, 360, 15), cusp)},
             'note': 'OKLCH 110° 附近是 sRGB 純黃，不是黃綠；105° 與 120° 約 0.94，原本 15° 取樣（明度步 0.005）只看到 0.935。'}
for nm, hx in {'深青': '#0C424A', '靛藍': '#333D66', '工程黃': '#D68702'}.items():
    L, C, h = ct.oklch(hx)
    best = max(((max_chroma(Lx, h), Lx) for Lx in np.arange(0.2, 0.99, 0.005)))
    rel[nm].update({'okL': round(L, 3), 'okh': round(h, 1), 'cusp_L_this_hue': round(float(best[1]), 3), 'cusp_C_this_hue': round(best[0], 3)})

out = {'roundtrip_check_max_abs_err_linear_rgb': max(chk), 'peers': pts, 'by_n_hues': by, 'songchun_rel_chroma': rel,
       'peer_main_rel_chroma': {'n': len(main_rel), 'median': round(float(np.median(main_rel)), 3), 'p25': round(float(np.percentile(main_rel, 25)), 3),
                                'min': round(min(main_rel), 3), 'n_below_0.5': sum(v < 0.5 for v in main_rel)},
       'random_srgb_rel_chroma': {'n': len(rr), 'median': round(float(np.median(rr)), 3), 'p25': round(float(np.percentile(rr, 25)), 3)},
       'cusp_by_hue': cusp, 'cusp_by_hue_note': '15° 取樣，只當粗略參考；細取樣看 cusp_fine。', 'cusp_fine': cusp_fine,
       'note': '色相群：OKLCH 色相差 30° 內算同一群；相對彩度 = 顏色 OKLCH C ÷ 同 L、同 h 在 sRGB 的最大 C；1 表示已經是螢幕上這個深淺能做到最鮮的。'}
json.dump(out, open('/tmp/claude-0/r2/theory/hue_contrast_map.json', 'w'), ensure_ascii=False, indent=1)
print(out['roundtrip_check_max_abs_err_linear_rgb'], by)
print(rel)
print(out['peer_main_rel_chroma'], out['random_srgb_rel_chroma'])
print(sorted([(r['rel_chroma_main'], r['peer']) for r in pts if r['rel_chroma_main'] is not None])[:6])
print([(c['okh'], c['cusp_L']) for c in cusp])
