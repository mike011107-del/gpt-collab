# 抽查上一次留下的程式：OSA-UCS、CIECAM02 對 colour-science 文件範例；Munsell 用 sRGB 來回；PCCS 對套件原碼
import sys, json, re
sys.path.insert(0, '/tmp/claude-0/r2/theory')
import numpy as np
from systems_lib import *
from munsell_conv import Inverter, load, xyYC2hex, hex2xyY_C, lin_hue, hue_diff, fmt
out = {}
r = osa_ucs_XYZ(np.array([0.20654008, 0.12197225, 0.05136952]) * 100)
out['osa_doc'] = {'expect': [-3.0049979, 2.9971369, -9.6678423], 'got': [round(v, 7) for v in r]}
c = ciecam02([19.01, 20.00, 21.78], [95.05, 100.00, 108.88], 318.31, 20.0)
out['ciecam02_doc'] = {'expect': [41.7310911, 0.1047077, 219.0484326], 'got': [round(c['J'], 7), round(c['C'], 7), round(c['h'], 7)]}
# Munsell sRGB 來回：real.py 色票 -> sRGB hex（色域內）-> Munsell
inv = Inverter(load('all'))
rows = load('real')
rng = np.random.default_rng(1)
dH, dV, dC, n = [], [], [], 0
for k in rng.permutation(len(rows))[:400]:
    s, fam, v, cc, x, y, Y = rows[k]
    if v < 2 or cc < 2:
        continue
    hx, oog = xyYC2hex(x, y, Y * 0.975)
    if oog:
        continue
    m = munsell(hx)
    if m['H'] is None:
        continue
    dH.append(abs(hue_diff(m['H'], lin_hue(s, fam)))); dV.append(abs(m['V'] - v)); dC.append(abs(m['C'] - cc)); n += 1
q = lambda a: {'median': round(float(np.median(a)), 2), 'p90': round(float(np.percentile(a, 90)), 2)}
out['munsell_srgb_roundtrip'] = {'n': n, 'hue_steps': q(dH), 'value': q(dV), 'chroma': q(dC),
                                 'note': 'Y 乘 0.975 是 renotation 把 MgO 參考白換成理想白的比例（colour-science 慣例）；hex 量化到 8 bit 會帶進誤差'}
print(json.dumps(out, ensure_ascii=False, indent=1))
json.dump(out, open('/tmp/claude-0/r2/theory/spotcheck.json', 'w'), ensure_ascii=False, indent=1)
