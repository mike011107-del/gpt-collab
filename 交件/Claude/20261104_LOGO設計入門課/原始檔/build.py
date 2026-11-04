"""組裝 LOGO 設計教學課程 HTML。用法：python3 -I build.py <build 資料夾> <fontsource package 資料夾>"""
import base64, os, re, sys
W, FONTS = sys.argv[1], sys.argv[2]
sys.path.insert(0, W)
import figs

def read(p):
    return open(os.path.join(W, p), encoding='utf-8').read()

body = read('body1.html') + read('body2.html') + read('body3.html')
for k, f in figs.ALL.items():
    body = body.replace(f'<!--F:{k}-->', f())

def b64(p):
    return 'data:image/png;base64,' + base64.b64encode(open(os.path.join(W, 'px', p), 'rb').read()).decode()

def pxgrid(rows):
    h = '<div class="pxgrid"><div></div><div class="hd">64 px</div><div class="hd">32 px</div><div class="hd">16 px</div>'
    for name, lab in rows:
        h += f'<div>{lab}</div>' + ''.join(f'<div><img src="{b64(f"{name}_{s}_big.png")}"></div>' for s in (64, 32, 16))
    return h + '</div>'

body = body.replace('<!--PX:four-->', pxgrid([('four04', '縫 4%'), ('four16', '縫 16%')]))
body = body.replace('<!--PX:mark-->', pxgrid([('thin', '細線版'), ('bold', '粗線版')]))

# 字面圖：直接嵌入量測用的同一張 600×600 渲染圖，紅框由同一張圖的像素算出，保證對齊
from PIL import Image, ImageOps
def glyph_png(ch):
    return os.path.join(W, 'meas', format(ord(ch), 'x') + '.png')
def bbox_of(ch):
    im = Image.open(glyph_png(ch)).convert('L')
    return ImageOps.invert(im).point(lambda v: 255 if v > 60 else 0).getbbox()  # (x0, y0, x1, y1)，x1/y1 不含
BB = {c: bbox_of(c) for c in '上國小口'}
SC = 0.11339  # 18mm / 600px
def gbox(ch, eq):
    x0, y0, x1, y1 = BB[ch]
    if eq:
        k = 470 / max(x1 - x0, y1 - y0)
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        tx, ty = 300 - k * cx, 300 - k * cy
    else:
        k, tx, ty = 1, 0, 0
    nx0, ny0, nx1, ny1 = k * x0 + tx, k * y0 + ty, k * x1 + tx, k * y1 + ty
    pad = 10  # 紅框畫在筆畫外側一點，不壓到筆畫
    nx0, ny0, nx1, ny1 = nx0 - pad, ny0 - pad, nx1 + pad, ny1 + pad
    src = 'data:image/png;base64,' + base64.b64encode(open(glyph_png(ch), 'rb').read()).decode()
    return (f'<div class="gbox"><div class="gin" style="transform:scale({SC})">'
            f'<img class="gch" src="{src}" style="transform:translate({tx:.1f}px,{ty:.1f}px) scale({k:.4f})">'
            f'<div class="gbb" style="left:{nx0:.1f}px;top:{ny0:.1f}px;width:{nx1-nx0:.1f}px;height:{ny1-ny0:.1f}px"></div></div></div>')
glyph = ''
for eq, lab in ((False, '字型原本'), (True, '紅框拉成一樣大')):
    glyph += '<div class="glyphs" style="margin-bottom:2mm"><div class="glab">' + lab + '</div>' + ''.join(gbox(c, eq) for c in '上國小口') + '</div>'
body = body.replace('<!--GLYPH-->', glyph)

# 對比表
def lum(h):
    v = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    v = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in v]
    return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]
def cr(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)
FG = [('白', '#FFFFFF'), ('深藍灰', figs.B), ('工程黃', figs.Y), ('紅', figs.R), ('黑', '#000000')]
BG = [('白', '#FFFFFF'), ('淺冷灰', figs.G), ('深藍灰', figs.B), ('工程黃', figs.Y), ('紅', figs.R)]
cm = '<table class="cm"><tr><th>字＼底</th>' + ''.join(f'<th>{n}</th>' for n, _ in BG) + '</tr>'
for fn, fc in FG:
    cm += f'<tr><th>{fn}</th>'
    for bn, bc in BG:
        if fc == bc:
            cm += f'<td style="background:{bc};color:#999;border:0.6pt solid #ddd">—</td>'; continue
        r = cr(fc, bc)
        m = '◎' if r >= 4.5 else ('○' if r >= 3 else '✕')
        cm += f'<td style="background:{bc};color:{fc};border:0.6pt solid #ddd"><b style="font-size:11pt">崧</b><br><span style="font-size:7.8pt">{m} {r:.2f}</span></td>'
    cm += '</tr>'
cm += '</table>'
body = body.replace('<!--CM-->', cm)

left = re.findall(r'<!--(F|PX):[a-z0-9]+-->|<!--GLYPH-->|<!--CM-->', body)
assert not left, left
css = read('style.css')
html = (f'<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><title>LOGO 設計入門課</title>'
        f'<link rel="stylesheet" href="file://{FONTS}/400.css"><link rel="stylesheet" href="file://{FONTS}/700.css"><link rel="stylesheet" href="file://{FONTS}/900.css">'
        f'<style>{css}</style></head><body>{body}</body></html>')
open(os.path.join(W, 'course.html'), 'w', encoding='utf-8').write(html)
print('ok', len(html))
