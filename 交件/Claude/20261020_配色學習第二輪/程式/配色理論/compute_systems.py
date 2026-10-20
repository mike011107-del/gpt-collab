# 崧淳三色 + 48 家國外同業 logo 色 → Munsell、PCCS 色調、ISCC-NBS 最近名、CIECAM02 色相組成（類 NCS）、OSA-UCS、OKLCH
# 並算隨機 sRGB 基準（PCCS 色調分布、Munsell 明度彩度）。用 python3 -I 執行。
import sys, json, math
sys.path.insert(0, '/tmp/claude-0/r2/theory')
sys.path.insert(0, '/home/user/gpt-collab/.claude/skills/colour-tool/scripts')
import numpy as np
import colourtool as ct
from systems_lib import munsell, munsell_to_pccs, pccs_hue_label, osa_ucs, iscc_nbs_nearest, ciecam02, hex2XYZ65
from munsell_conv import HUES
from collections import Counter

SC = {'深青': '#0C424A', '靛藍': '#333D66', '工程黃': '#D68702'}
peers = json.load(open('/tmp/claude-0/work/peer_schemes.json'))

# CIECAM02 sRGB 標準觀看條件（colour-science CAM_KWARGS_CIECAM02_sRGB：L_A=64/π*0.2, Y_b=20, 一般環境）
XYZ_W = hex2XYZ65('#FFFFFF')
L_A = 64 / math.pi * 0.2
h_i = [20.14, 90.00, 164.25, 237.53, 380.14]; e_i = [0.8, 0.7, 1.0, 1.2, 0.8]; H_i = [0, 100, 200, 300, 400]
UNI = ['R', 'Y', 'G', 'B', 'R']


def hue_quad(h):  # CIE 159:2004
    hp = h + 360 if h < h_i[0] else h
    i = max(k for k in range(4) if h_i[k] <= hp)
    a = (hp - h_i[i]) / e_i[i]; b = (h_i[i + 1] - hp) / e_i[i + 1]
    return H_i[i] + 100 * a / (a + b)


def hue_comp(H):  # 例：H=150 -> Y50G（黃 50%、綠 50%）
    i = int(H // 100) % 4; f = H - 100 * (H // 100)
    if f < 0.5: return UNI[i]
    if f > 99.5: return UNI[i + 1]
    return f'{UNI[i]}{round(f):d}{UNI[i + 1]}'


def describe(hx):
    m = munsell(hx)
    p = munsell_to_pccs(m['H'], m['V'], m['C']) if m['H'] is not None else {'h': None, 'l': m['V'], 's': 0, 'tone': 'N'}
    p2 = munsell_to_pccs(m['H'], m['V'], m['C'], variant='fixed') if m['H'] is not None else p
    cam = ciecam02(hex2XYZ65(hx), XYZ_W, L_A, 20.0)
    Hq = hue_quad(cam['h'])
    L, j, g = osa_ucs(hx)
    ok = ct.oklch(hx); lab = ct.lab(hx)
    return {'hex': hx.upper(), 'munsell': m['text'], 'munsell_H': None if m['H'] is None else round(m['H'], 2),
            'munsell_V': round(m['V'], 2), 'munsell_C': round(m['C'], 2),
            'pccs_hue': pccs_hue_label(p['h']), 'pccs_s': round(p['s'], 1), 'pccs_tone': p['tone'], 'pccs_tone_fixed_variant': p2['tone'],
            'iscc_nbs': iscc_nbs_nearest(hx, 2), 'cam02_J': round(cam['J'], 1), 'cam02_C': round(cam['C'], 1), 'cam02_h': round(cam['h'], 1),
            'cam02_hue_comp': hue_comp(Hq) if cam['C'] > 5 else 'N', 'osa_Ljg': [round(L, 2), round(j, 2), round(g, 2)],
            'oklch': [round(v, 3) for v in ok], 'lab_L': round(lab[0], 1)}


out = {'note': 'Munsell 用 colour-science renotation（commit 248121e）反查；PCCS 用 pccs 0.2a3 公式（Kobayashi & Yosiki 2001）；ISCC-NBS 是 267 中心色 ΔE2000 最近，不是官方區塊判定；CIECAM02 色相組成以紅黃綠藍獨特色相為基準，跟 NCS 色相同一種想法，但不是 NCS 編號；OSA-UCS 用 2° 近似（定義是 10°）。',
       'songchun': {k: describe(v) for k, v in SC.items()}, 'peers': []}
for p in peers:
    out['peers'].append({'name': p['name'], 'group': p['t'], 'cols': [describe(c) for c in p['cols']],
                         'neutral': [describe(c) for c in p['neutral']]})

# 統計：同業主色（cols[0]）
main = [p['cols'][0] for p in out['peers'] if p['cols']]
fam = Counter()
for c in main:
    if c['munsell_H'] is None or c['munsell_C'] < 1.5: fam['N'] += 1; continue
    H = c['munsell_H'] % 100; i = (int(math.ceil(H / 10.0)) - 1) % 10 if H > 0 else 9
    fam[HUES[i]] += 1
allc = [c for p in out['peers'] for c in p['cols']]
st = lambda a: {'n': len(a), 'median': round(float(np.median(a)), 2), 'p25': round(float(np.percentile(a, 25)), 2), 'p75': round(float(np.percentile(a, 75)), 2)}
out['stats_main'] = {'n': len(main), 'munsell_family': dict(fam.most_common()), 'V': st([c['munsell_V'] for c in main]), 'C': st([c['munsell_C'] for c in main]),
                     'pccs_tone': dict(Counter(c['pccs_tone'] for c in main).most_common())}
out['stats_allcols'] = {'n': len(allc), 'pccs_tone': dict(Counter(c['pccs_tone'] for c in allc).most_common()),
                        'V': st([c['munsell_V'] for c in allc]), 'C': st([c['munsell_C'] for c in allc])}

# 隨機基準：均勻 sRGB 立方體 2000 色，去掉 Munsell 彩度 < 1.5 的近灰色
rng = np.random.default_rng(7)
rt, rV, rC = Counter(), [], []
for _ in range(2000):
    hx = '#' + ''.join(f'{v:02X}' for v in rng.integers(0, 256, 3))
    m = munsell(hx)
    if m['H'] is None or m['C'] < 1.5: continue
    p = munsell_to_pccs(m['H'], m['V'], m['C'])
    rt[p['tone']] += 1; rV.append(m['V']); rC.append(m['C'])
n = sum(rt.values())
out['baseline_random_srgb'] = {'n': n, 'pccs_tone_share': {k: round(v / n, 3) for k, v in rt.most_common()}, 'V': st(rV), 'C': st(rC)}
json.dump(out, open('/tmp/claude-0/r2/theory/systems_colors.json', 'w'), ensure_ascii=False, indent=1)
print(json.dumps(out['songchun'], ensure_ascii=False)[:3000])
print(json.dumps({k: out[k] for k in ('stats_main', 'stats_allcols', 'baseline_random_srgb')}, ensure_ascii=False))
