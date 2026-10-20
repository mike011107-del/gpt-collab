# make_figs.py（/tmp/claude-0/r2/theory/）的副本（v3）：只重畫 fig_simul_contrast、fig_munsell_vc、fig_wada 三張，
# 讓 A5 報告裡每個字印出來至少 2.2mm（約 6pt）。數據、色碼、色塊與點的位置、統計結果都不變，只改字級、版面、標籤位置。
# Itten 那張（fig_itten_peers）不在這次範圍，已移除，避免誤跑覆寫原圖；輸出一律寫到 report2/img/*_v3.png。
# 最小字身 px = ceil(2.2mm × 圖寬 px ÷ 顯示寬 mm)。
import json, math
from PIL import Image, ImageDraw, ImageFont
D = '/tmp/claude-0/r2/theory/'
O = '/tmp/claude-0/report2/img/'
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
f = lambda s: ImageFont.truetype(F, s)
INK, SUB = (30, 30, 30), (110, 110, 110)
def minpx(P, Wmm): return math.ceil(2.2 * P / Wmm)

# 記錄每段字的外框，畫完檢查：字級、重疊、出界
LOG = []
def T(d, xy, s, size, fill, anchor='la', fig=''):
    d.text(xy, s, font=f(size), fill=fill, anchor=anchor)
    LOG.append((fig, 'text', d.textbbox(xy, s, font=f(size), anchor=anchor), size, s))
def M(box, fig, name='mark'):
    LOG.append((fig, name, tuple(box), 0, ''))

# 圖 1：同時對比（顯示寬 126mm）
S = json.load(open(D + 'simul_contrast.json'))
W = 5 * 240 + 40; FS = minpx(W, 126)          # 1240px → 22px
H = 524
im = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(im); g = 'simul'
T(d, (20, 14), '同一個工程黃 #D68702 放在五種底上（示意，不是配色提案）', 26, INK, fig=g)
for i, r in enumerate(S['rows']):
    x = 20 + i * 240; y = 60
    d.rectangle([x, y, x + 220, y + 220], fill=r['bg'], outline=(200, 200, 200))
    d.rectangle([x + 75, y + 75, x + 145, y + 145], fill=r['fg'])
    M([x, y, x + 220, y + 220], g, 'swatch')
    T(d, (x, y + 232), f"{r['bg_name']}  {r['bg']}", FS, INK, fig=g)
    T(d, (x, y + 262), f"亮度比 {r['wcag']}:1", FS, INK, fig=g)
    T(d, (x, y + 292), f"色差 ΔE2000 {r['dE2000']}", FS, INK, fig=g)
    T(d, (x, y + 322), f"明度差 ΔL* {r['dL']:+}", FS, INK, fig=g)
    T(d, (x, y + 352), f"模型明度 J {r['cam02_J_of_yellow']}", FS, SUB, fig=g)
T(d, (20, 454), 'J：CIECAM02 依底色亮度預測黃看起來多亮（白底 46、黑底 61）。模型不預測色相偏移。', FS, SUB, fig=g)
bf = S['black_bg_J_by_Yb_floor']
T(d, (20, 484), f"黑底的背景亮度 Y_b=0 模型算不了，這裡自訂下限 Y_b=1；取 0.5 或 2 時黑底 J 是 {bf['0.5']} 或 {bf['2.0']}。", FS, SUB, fig=g)
im.save(O + 'fig_simul_contrast_v3.png')

# 圖 3：Munsell 明度×彩度（同業主色＋崧淳三色）（顯示寬 114mm）
Sy = json.load(open(D + 'systems_colors.json'))
W, H = 1180, 652; FS = minpx(W, 114)          # 1180px → 23px
im = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(im); g = 'munsell'
T(d, (20, 12), 'Munsell 明度 × 彩度：42 家同業主色（圓點）與三個崧淳色（方塊）', 26, INK, fig=g)
X0, Y0, Wd, Ht = 90, 560, 1040, 480  # C 0–24, V 0–10（座標框與原圖相同，點的位置不變）
for c in range(0, 25, 4):
    x = X0 + c / 24 * Wd; d.line([x, Y0, x, Y0 - Ht], fill=(232, 232, 232))
    T(d, (x, Y0 + 10), str(c), FS, SUB, anchor='ma', fig=g)
for v in range(0, 11, 2):
    y = Y0 - v / 10 * Ht; d.line([X0, y, X0 + Wd, y], fill=(232, 232, 232))
    T(d, (X0 - 10, y), str(v), FS, SUB, anchor='rm', fig=g)
T(d, (X0 + Wd / 2, Y0 + 46), 'Munsell 彩度 C', 24, INK, anchor='ma', fig=g)
T(d, (X0 + 8, 50), '明度 V', 24, INK, fig=g)
for p in Sy['peers']:
    if not p['cols']: continue
    c = p['cols'][0]; x = X0 + min(c['munsell_C'], 24) / 24 * Wd; y = Y0 - c['munsell_V'] / 10 * Ht
    d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=c['hex'], outline=(160, 160, 160)); M([x - 9, y - 9, x + 9, y + 9], g, 'dot')
# 崧淳三色：標籤放到旁邊沒有點的空白處，工程黃用細線連回方塊
LAB = {'深青': ((-24, 22), None), '靛藍': ((16, -54), None), '工程黃': ((60, -96), 'line')}
for nm, c in Sy['songchun'].items():
    x = X0 + c['munsell_C'] / 24 * Wd; y = Y0 - c['munsell_V'] / 10 * Ht
    (ox, oy), ln = LAB[nm]
    if ln:
        d.line([x + 10, y - 10, x + ox - 4, y + oy + 26], fill=(90, 90, 90), width=2)
    d.rectangle([x - 13, y - 13, x + 13, y + 13], fill=c['hex'], outline=INK, width=2); M([x - 13, y - 13, x + 13, y + 13], g, 'square')
    T(d, (x + ox, y + oy), f"{nm} {c['munsell']}", FS, INK, fig=g)
im.save(O + 'fig_munsell_vc_v3.png')

# 圖 4：和田三造兩色組 vs 同盒隨機（10-19 修正：每次重新抽樣，兩個種子各 2 萬次）（顯示寬 111mm）
Wd_ = json.load(open(D + 'wada_stats.json')); t = Wd_['test_vs_weighted_random_fresh_123x20000x2seeds']; pt = Wd_['pccs_same_tone_test']
items = [('明度差 < 10', t['dL_lt10_share']), ('明度差 ≥ 26', t['dL_ge26_share']), ('色相差 < 30°', t['dh_lt30_share']), ('色相差 ≥ 150°', t['dh_ge150_share'])]
W, H = 1000, 462; FS = minpx(W, 111)          # 1000px → 20px
im = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(im); g = 'wada'
T(d, (20, 14), '和田三造《配色總鑑》123 組兩色配色 vs 同一盒色隨機配（每次重抽，2 萬次 × 2）', 24, INK, fig=g)
for k, (lab, v) in enumerate(items + [('同一 PCCS 色調', {'wada': pt['wada_same_tone_share'], 'sim_median': pt['random_same_tone_share_median'], 'two_sided_p': pt['p_same']})]):
    y = 70 + k * 64
    pr = v.get('p_range'); ptxt = f"p≈{v['two_sided_p']:.2f}"
    edge = lab == '色相差 < 30°'
    T(d, (20, y + 24), lab, 22, INK, anchor='lm', fig=g)
    d.rectangle([220, y, 220 + v['wada'] * 900, y + 22], fill=(60, 60, 60)); M([220, y, 220 + v['wada'] * 900, y + 22], g, 'bar')
    T(d, (230 + v['wada'] * 900, y + 11), f"和田 {v['wada']:.0%}", FS, INK, anchor='lm', fig=g)
    d.rectangle([220, y + 26, 220 + v['sim_median'] * 900, y + 48], fill=(180, 180, 180)); M([220, y + 26, 220 + v['sim_median'] * 900, y + 48], g, 'bar')
    T(d, (230 + v['sim_median'] * 900, y + 37), f"隨機 {v['sim_median']:.0%}　{ptxt}" + ('　邊界' if edge else ''), FS, INK if edge else SUB, anchor='lm', fig=g)
T(d, (20, 396), '色相差 < 30° 在邊界：和田的同色相配對偏少，方向跟刻意拉開色相一致，但未達一般顯著水準。', FS, SUB, fig=g)
T(d, (20, 426), '其他四項沒有測到差別。只有 123 組，檢定力有限，不顯著不等於沒有差別。hex 是 CMYK 直接換算。', FS, SUB, fig=g)
im.save(O + 'fig_wada_v3.png')

# 檢查：最小字、字與字／字與標記重疊、出界、缺字
SIZES = {'simul': (1240, 524), 'munsell': (1180, 652), 'wada': (1000, 462)}
def hit(a, b, pad=2):
    return not (a[2] + pad <= b[0] or b[2] + pad <= a[0] or a[3] + pad <= b[1] or b[3] + pad <= a[1])
fnt = f(22)
def glyph(ch):
    gi = Image.new('L', (44, 44)); ImageDraw.Draw(gi).text((6, 6), ch, font=fnt, fill=255); return gi.tobytes()
notdef = glyph(chr(0x2212))  # 這個字型沒有 U+2212，用它的方框當缺字樣本
for g, (Wp, Hp) in SIZES.items():
    tx = [e for e in LOG if e[0] == g and e[1] == 'text']; mk = [e for e in LOG if e[0] == g and e[1] in ('dot', 'square')]
    print(g, 'min font', min(e[3] for e in tx))
    for i in range(len(tx)):
        b = tx[i][2]
        if b[0] < 4 or b[1] < 4 or b[2] > Wp - 4 or b[3] > Hp - 4: print('  OUT', b, tx[i][4])
        for j in range(i + 1, len(tx)):
            if hit(b, tx[j][2]): print('  TEXT×TEXT', tx[i][4], '|', tx[j][4])
        for m in mk:
            if hit(b, m[2]): print('  TEXT×MARK', tx[i][4], m[2])
        miss = {ch for ch in tx[i][4] if not ch.isspace() and glyph(ch) == notdef}
        if miss: print('  MISSING', miss, tx[i][4])
print('ok')
