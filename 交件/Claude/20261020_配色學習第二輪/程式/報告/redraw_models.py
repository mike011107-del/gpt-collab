# 重畫配色模型兩張圖（查核指出標籤擠、年份來源不明）。資料取自 models/data/fig_*.json。
import json
from PIL import Image, ImageDraw, ImageFont

D = '/tmp/claude-0/r2/models/data/'
OUT = '/tmp/claude-0/report2/img/'
FONT = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
S = 2
F = lambda n: ImageFont.truetype(FONT, n * S)
f12, f13, f14, f16 = F(12), F(13), F(14), F(16)


def axes(dr, box, xr, yr, xt, yt, xlabel, ylabel):
    x0, y0, x1, y1 = [v * S for v in box]
    dr.rectangle([x0, y0, x1, y1], outline='#888888', width=S)
    for v in xt:
        X = x0 + (v - xr[0]) / (xr[1] - xr[0]) * (x1 - x0)
        dr.line([X, y0, X, y1], fill='#EEEEEE', width=S)
        dr.line([X, y1, X, y1 + 5 * S], fill='#555555', width=S)
        dr.text((X, y1 + 8 * S), str(v), font=f12, fill='#333333', anchor='ma')
    for v in yt:
        Y = y1 - (v - yr[0]) / (yr[1] - yr[0]) * (y1 - y0)
        dr.line([x0, Y, x1, Y], fill='#EEEEEE', width=S)
        dr.line([x0 - 5 * S, Y, x0, Y], fill='#555555', width=S)
        dr.text((x0 - 8 * S, Y), str(v), font=f12, fill='#333333', anchor='rm')
    dr.text(((x0 + x1) / 2, y1 + 28 * S), xlabel, font=f14, fill='#222222', anchor='ma')
    dr.text((x0, y0 - 10 * S), ylabel, font=f14, fill='#222222', anchor='ld')

    def P(x, y):
        return (x0 + (x - xr[0]) / (xr[1] - xr[0]) * (x1 - x0), y1 - (y - yr[0]) / (yr[1] - yr[0]) * (y1 - y0))
    return P


def callout(dr, frm, to, text, font=f14, anchor='lm'):
    dr.line([frm, to], fill='#000000', width=S)
    bb = dr.textbbox(to, text, font=font, anchor=anchor)
    pad = 3 * S
    dr.rectangle([bb[0] - pad, bb[1] - pad, bb[2] + pad, bb[3] + pad], fill='#FFFFFF', outline='#000000', width=S)
    dr.text(to, text, font=font, fill='#000000', anchor=anchor)


# 圖 1：Ou 冷暖 × L*
d = json.load(open(D + 'fig_single_wc_L.json'))
im = Image.new('RGB', (900 * S, 690 * S), 'white'); dr = ImageDraw.Draw(im)
dr.text((60 * S, 14 * S), '單色位置：Ou 冷暖值（橫軸，0 以上偏暖）× 明度 L*（縱軸）', font=f16, fill='#111111')
box = (90, 80, 860, 560)
P = axes(dr, box, (-2.2, 2.5), (0, 100), [-2, -1, 0, 1, 2], [0, 20, 40, 60, 80, 100], 'Ou 冷暖值', 'L*')
X0 = P(0, 0)[0]
dr.line([X0, box[1] * S, X0, box[3] * S], fill='#BBBBBB', width=2 * S)
dr.text((X0, box[3] * S - 8 * S), '← 偏冷　偏暖 →', font=f12, fill='#666666', anchor='md')
tg = {}
for p in d['points']:
    x, y = P(p['x'], p['y'])
    if p['group'] == '崧淳候選／已定':
        tg[p['name']] = (x, y, p); continue
    r = 6 * S
    dr.ellipse([x - r, y - r, x + r, y + r], fill=p['hex'], outline='#666666', width=S)
for name, (x, y, p) in tg.items():
    r = 9 * S
    dr.ellipse([x - r, y - r, x + r, y + r], fill=p['hex'], outline='#000000', width=2 * S)
lab = {'深青': ((-1.95, 9), 'lm'), '靛藍': ((-0.3, 13), 'lm'), '工程黃': ((0.15, 60), 'lm'), '白': ((-0.2, 97), 'lm')}
for name, (x, y, p) in tg.items():
    (lx, ly), an = lab[name]
    callout(dr, (x, y), P(lx, ly), f"{name} {p['x']:+.2f}", anchor=an)
dr.text((95 * S, 612 * S), '小圓：48 家國外同業裡有彩色的 42 家主色。黑框大圓：深青、靛藍、工程黃、白。', font=f12, fill='#444444')
dr.text((95 * S, 632 * S), '公式取自 Google Material Color Utilities 程式（註明 Ou、Woodcock、Wright；程式沒寫年份）。', font=f12, fill='#444444')
dr.text((95 * S, 652 * S), 'Ou 原論文未取得，受試者與實驗條件沒讀到。', font=f12, fill='#444444')
im.save(OUT + 'fig_single_wc_L_v2.png')

# 圖 2：ΔL* × 兩色偏好
d = json.load(open(D + 'fig_pair_dL_pp.json'))
im = Image.new('RGB', (900 * S, 700 * S), 'white'); dr = ImageDraw.Draw(im)
dr.text((60 * S, 14 * S), '兩色：明度差 ΔL*（橫軸）× Colorgorical 兩色偏好分數（縱軸）', font=f16, fill='#111111')
box = (90, 80, 860, 560)
P = axes(dr, box, (0, 95), (-100, 110), [0, 20, 40, 60, 80], [-100, -50, 0, 50, 100], '明度差 ΔL*', '兩色偏好分數')
for p in d['random']:
    x, y = P(p['x'], p['y']); r = 2 * S
    dr.ellipse([x - r, y - r, x + r, y + r], fill='#D4D4D4')
for p in d['peer']:
    x, y = P(p['x'], p['y']); r = 7 * S
    dr.ellipse([x - r, y - r, x + r, y + r], fill=p['a'], outline='#555555', width=S)
    dr.pieslice([x - r, y - r, x + r, y + r], -90, 90, fill=p['b'])
    dr.ellipse([x - r, y - r, x + r, y + r], outline='#555555', width=S)
T = {p['name']: p for p in d['targets']}
for name, p in T.items():
    x, y = P(p['x'], p['y']); r = 10 * S
    dr.ellipse([x - r, y - r, x + r, y + r], fill=p['a'])
    dr.pieslice([x - r, y - r, x + r, y + r], -90, 90, fill=p['b'])
    dr.ellipse([x - r, y - r, x + r, y + r], outline='#000000', width=2 * S)
fmt = lambda v: f'{v:.1f}'
callout(dr, P(37.87, 27.39), P(52, 100), f'深青×工程黃 {fmt(27.39)}')
callout(dr, P(36.3, -2.58), P(48, -55), f'靛藍×工程黃 {fmt(-2.58)}（照程式；照原意 {fmt(14.23)}）')
callout(dr, P(36.97, 12.02), P(28, -62), f'工程黃×白 {fmt(12.02)}', anchor='rm')
callout(dr, P(74.83, 56.23), P(66, 86), f'深青×白 {fmt(56.23)}', anchor='lm')
callout(dr, P(73.26, 29.27), P(76, 4), f'靛藍×白 {fmt(29.27)}', anchor='lm')
dr.text((95 * S, 618 * S), '灰點：隨機 sRGB 兩色 800 組（固定種子）。小雙色圓：國外同業 logo 實際配對 30 對。黑框大雙色圓：本報告比較的配對。', font=f12, fill='#444444')
dr.text((95 * S, 638 * S), '分數是 Schloss & Palmer 2011 柏克萊 48 人看螢幕色塊的迴歸預測（Colorgorical 改寫到 CIELAB），不等於好看。', font=f12, fill='#444444')
dr.text((95 * S, 658 * S), 'Colorgorical 程式算色相差沒有繞回 360°，跨過紅色的配對分數會偏低。靛藍×工程黃照原意改算是 14.2，會落在工程黃×白旁邊。', font=f12, fill='#444444')
im.save(OUT + 'fig_pair_dL_pp_v2.png')
print('ok')
