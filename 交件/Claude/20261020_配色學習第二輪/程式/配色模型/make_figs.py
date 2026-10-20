# 預覽圖（PIL）。給報告串參考；正式圖可用 data/fig_*.json 重畫。
import json
from PIL import Image, ImageDraw, ImageFont

D = '/tmp/claude-0/r2/models/data/'
FONT = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
f14 = ImageFont.truetype(FONT, 14)
f12 = ImageFont.truetype(FONT, 12)
f18 = ImageFont.truetype(FONT, 18)


def axes(dr, box, xr, yr, xt, yt, xlabel, ylabel):
    x0, y0, x1, y1 = box
    dr.rectangle(box, outline='#888888')
    for v in xt:
        X = x0 + (v - xr[0]) / (xr[1] - xr[0]) * (x1 - x0)
        dr.line([X, y1, X, y1 + 5], fill='#555555'); dr.text((X - 10, y1 + 8), str(v), font=f12, fill='#333333')
        dr.line([X, y0, X, y1], fill='#EEEEEE')
    for v in yt:
        Y = y1 - (v - yr[0]) / (yr[1] - yr[0]) * (y1 - y0)
        dr.line([x0 - 5, Y, x0, Y], fill='#555555'); dr.text((x0 - 40, Y - 7), str(v), font=f12, fill='#333333')
        dr.line([x0, Y, x1, Y], fill='#EEEEEE')
    dr.text(((x0 + x1) / 2 - 60, y1 + 28), xlabel, font=f14, fill='#222222')
    dr.text((x0 - 50, y0 - 28), ylabel, font=f14, fill='#222222')

    def P(x, y):
        return (x0 + (x - xr[0]) / (xr[1] - xr[0]) * (x1 - x0), y1 - (y - yr[0]) / (yr[1] - yr[0]) * (y1 - y0))
    return P


# 圖 1：Ou 冷暖 × L*
d = json.load(open(D + 'fig_single_wc_L.json'))
im = Image.new('RGB', (900, 680), 'white'); dr = ImageDraw.Draw(im)
dr.text((60, 14), '單色位置：Ou 冷暖公式（橫軸，>0 偏暖）× 明度 L*（縱軸）', font=f18, fill='#111111')
box = (90, 80, 860, 560)
P = axes(dr, box, (-2, 2.5), (0, 100), [-2, -1, 0, 1, 2], [0, 20, 40, 60, 80, 100], 'Ou 冷暖值 WC', 'L*')
X0 = P(0, 0)[0]; dr.line([X0, box[1], X0, box[3]], fill='#BBBBBB', width=2)
for p in d['points']:
    x, y = P(p['x'], p['y'])
    tgt = p['group'] == '崧淳候選／已定'
    r = 9 if tgt else 6
    dr.ellipse([x - r, y - r, x + r, y + r], fill=p['hex'], outline='#000000' if tgt else '#666666', width=2 if tgt else 1)
    if tgt:
        ox = -42 if p['name'] == '深青' else 11
        oy = 4 if p['name'] == '深青' else -14
        dr.text((x + ox, y + oy), p['name'], font=f14, fill='#000000')
dr.text((95, 615), '小圓：48 家國外同業中有彩色的 42 家主色；大圓黑框：深青、靛藍、工程黃、白。', font=f12, fill='#444444')
dr.text((95, 635), '公式取自 Material Color Utilities 的 Ou 等人 2004 冷暖實作；Ou 原文未取得，受試者與條件未讀到。', font=f12, fill='#444444')
im.save(D + 'fig_single_wc_L.png')

# 圖 2：ΔL* × 兩色偏好
d = json.load(open(D + 'fig_pair_dL_pp.json'))
im = Image.new('RGB', (900, 690), 'white'); dr = ImageDraw.Draw(im)
dr.text((60, 14), '兩色：明度差 ΔL*（橫軸）× Colorgorical 兩色偏好分數（縱軸，程式原樣）', font=f18, fill='#111111')
box = (90, 80, 860, 560)
P = axes(dr, box, (0, 95), (-100, 110), [0, 20, 40, 60, 80], [-100, -50, 0, 50, 100], '明度差 ΔL*', '兩色偏好 PP')
for p in d['random']:
    x, y = P(p['x'], p['y']); dr.ellipse([x - 2, y - 2, x + 2, y + 2], fill='#CCCCCC')
for p in d['peer']:
    x, y = P(p['x'], p['y'])
    dr.ellipse([x - 7, y - 7, x, y + 7], fill=p['a'], outline='#444444')
    dr.ellipse([x, y - 7, x + 7, y + 7], fill=p['b'], outline='#444444')
for p in d['targets']:
    x, y = P(p['x'], p['y'])
    dr.ellipse([x - 10, y - 10, x, y + 10], fill=p['a'], outline='#000000', width=2)
    dr.ellipse([x, y - 10, x + 10, y + 10], fill=p['b'], outline='#000000', width=2)
    off = {'工程黃×白': (-95, -9), '靛藍×工程黃': (13, 2)}.get(p['name'], (13, -9))
    dr.text((x + off[0], y + off[1]), p['name'], font=f14, fill='#000000')
    if p['y_wrapped'] != p['y']:
        x2, y2 = P(p['x'], p['y_wrapped'])
        dr.line([x + 12, y, x + 12, y2], fill='#000000', width=1)
        dr.ellipse([x + 9, y2 - 3, x + 15, y2 + 3], outline='#000000')
        dr.text((x + 18, y2 - 16), '靛藍×工程黃 色相差取補角時', font=f12, fill='#000000')
dr.text((95, 625), '灰點：隨機 sRGB 兩色（固定種子，取 800 組）；半圓對：同業 logo 實際配對 30 對；大半圓黑框：崧淳候選配對。', font=f12, fill='#444444')
dr.text((95, 645), '分數只代表 Schloss & Palmer 2011 柏克萊 48 人螢幕實驗的迴歸預測（經 Colorgorical 改寫到 CIELAB），不等於好看。', font=f12, fill='#444444')
im.save(D + 'fig_pair_dL_pp.png')

# 圖 3：冷度曲線 + Ou 冷暖曲線
cc = json.load(open(D + 'fig_coolness_curve.json'))
wc = json.load(open(D + 'fig_ou_wc_curve.json'))
im = Image.new('RGB', (900, 680), 'white'); dr = ImageDraw.Draw(im)
dr.text((60, 14), '同一個色相，兩個模型怎麼看冷暖', font=f18, fill='#111111')
box = (90, 70, 860, 290)
P = axes(dr, box, (0, 360), (0, 19), [0, 60, 120, 180, 240, 300, 360], [0, 6, 12, 18], 'Lab 色相角 h', '冷度')
for p in cc['points']:
    import colorsys
    x, y = P(p['h'], p['coolness'])
    dr.ellipse([x - 3, y - 3, x + 3, y + 3], fill='#336699')
dr.text((95, 343), '上：Colorgorical 冷度表（Schloss & Palmer 冷度，L*=50、C* 30–45 格點）。越高越冷。', font=f12, fill='#444444')
box = (90, 405, 860, 590)
P = axes(dr, box, (0, 360), (-2, 2), [0, 60, 120, 180, 240, 300, 360], [-2, -1, 0, 1, 2], 'Lab 色相角 h', 'Ou 冷暖')
cols = {'20': '#99BBDD', '40': '#3377AA', '70': '#113355'}
for C, vals in wc['wc'].items():
    pts = [P(h, v) for h, v in zip(wc['hue'], vals)]
    dr.line(pts, fill=cols[C], width=2)
    dr.text((pts[10][0], pts[10][1] - 16), 'C*=' + C, font=f12, fill=cols[C])
y0 = P(0, 0)[1]; dr.line([box[0], y0, box[2], y0], fill='#BBBBBB')
dr.text((95, 645), '下：Ou 冷暖公式（越高越暖，0 以上算暖）。兩個模型方向相反：冷度高＝Ou 值低。', font=f12, fill='#444444')
im.save(D + 'fig_coolness_ou_curves.png')
print('ok')
