# 驗證 munsell_conv.py：
# (a) colour-science 文件範例 xyY -> 4.2YR 8.1/5.3
# (b) colour-science 單元測試表 MUNSELL_SPECIFICATIONS（他們的演算法算出的 xyY 與 Munsell 對照）
# (c) 留一法：拿掉 V=5 平面，用 V=4、6 內插去猜 real.py 的 V=5 色票；只留 5、10 色相去猜 2.5、7.5 色相
import sys, re, json
sys.path.insert(0, '/tmp/claude-0/r2/theory')
import numpy as np
from munsell_conv import *

out = {}
inv = Inverter(load('all'))

# (a)
m = inv.xyY_to_munsell(0.38736945, 0.35751656, 59.362)
out['a_doctest'] = {'expect': '4.2YR 8.1/5.3', 'got': fmt(m)}
print('a', out['a_doctest'])

# (b)
t = open(f'{SRC}/notation/munsell/tests/test_centore2014.py').read()
blk = t[t.index('MUNSELL_SPECIFICATIONS: NDArrayFloat'):]
blk = blk[:blk.index('\n)\n')]
pairs = re.findall(r'\[\s*\[([-0-9.e, ]+)\],\s*\[([-0-9.e, ]+)\],?\s*\]', blk)
dH, dV, dC = [], [], []
for s, xyY in pairs:
    step, V, C, code = [float(v) for v in s.split(',')]
    x, y, Y = [float(v) for v in xyY.split(',')]
    r = inv.xyY_to_munsell(x, y, Y * 100)
    Href = spec_to_linear(step, code)
    if r['H'] is None:
        continue
    dH.append(abs(hue_diff(r['H'], Href))); dV.append(abs(r['V'] - V)); dC.append(abs(r['C'] - C))
dH, dV, dC = map(np.array, (dH, dV, dC))
def st(a):
    return {'median': round(float(np.median(a)), 3), 'p90': round(float(np.percentile(a, 90)), 3), 'max': round(float(a.max()), 3)}
out['b_colour_science_table'] = {'n': int(len(dH)), 'hue_steps': st(dH), 'value': st(dV), 'chroma': st(dC)}
print('b', out['b_colour_science_table'])
# 只看 V 2-9、C<=16（跟我們的顏色範圍接近）
real = load('real')

# (c1) 拿掉 V=5
inv_noV5 = Inverter(load('all'), drop_value=5.0)
dH, dC, dV = [], [], []
for s, fam, v, c, x, y, Y in real:
    if v != 5.0:
        continue
    r = inv_noV5.xyY_to_munsell(x, y, Y * 0.975)
    dH.append(abs(hue_diff(r['H'], lin_hue(s, fam)))); dC.append(abs(r['C'] - c)); dV.append(abs(r['V'] - v))
out['c1_drop_V5'] = {'n': len(dH), 'hue_steps': st(np.array(dH)), 'chroma': st(np.array(dC)), 'value': st(np.array(dV))}
print('c1', out['c1_drop_V5'])

# (c2) 只用 5、10 色相
inv_h5 = Inverter(load('all'), hue_subset=5)
dH, dC = [], []
for s, fam, v, c, x, y, Y in real:
    if s not in (2.5, 7.5) or v not in (3.0, 4.0, 5.0, 6.0):
        continue
    r = inv_h5.xyY_to_munsell(x, y, Y * 0.975)
    dH.append(abs(hue_diff(r['H'], lin_hue(s, fam)))); dC.append(abs(r['C'] - c))
out['c2_hue_subset5'] = {'n': len(dH), 'hue_steps': st(np.array(dH)), 'chroma': st(np.array(dC))}
print('c2', out['c2_hue_subset5'])

# (d) 自身重建：real.py 色票直接丟回去（應該接近 0，只檢查程式沒寫錯）
dH, dC = [], []
for s, fam, v, c, x, y, Y in real[::7]:
    r = inv.xyY_to_munsell(x, y, Y * 0.975)
    dH.append(abs(hue_diff(r['H'], lin_hue(s, fam)))); dC.append(abs(r['C'] - c))
out['d_self'] = {'n': len(dH), 'hue_steps': st(np.array(dH)), 'chroma': st(np.array(dC))}
print('d', out['d_self'])
json.dump(out, open('/tmp/claude-0/r2/theory/munsell_validation.json', 'w'), ensure_ascii=False, indent=1)
