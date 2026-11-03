"""崧淳字標第一批：三個方向的 SVG、組合、反白、縮小圖，與 A5 比較頁 HTML。"""
import sys, os, io, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from design import *
from PIL import Image, ImageDraw
OUT = sys.argv[1] if len(sys.argv) > 1 else 'out'
FONTS = sys.argv[2]
os.makedirs(OUT, exist_ok=True)

FULL = '崧淳環保科技股份有限公司'
BIZ = '污水下水道清淤・CCTV檢視'

def line(fontpath, text, width, y_top, size, bold=0, track=None):
    """把一行字的輪廓排成指定寬度。中文字之間平均分配字距；連續英文字母當一組，組內只加一點字距。"""
    import re
    toks = re.findall(r'[A-Za-z0-9]+|.', text)
    sc = size / 1000
    groups = []
    for t in toks:
        x = 0; parts = []
        for i, ch in enumerate(t):
            g, adv = glyph(fontpath, ch)
            if bold: g = g.buffer(bold, join_style='mitre', mitre_limit=1.6)
            parts.append(affinity.translate(g, x, 0)); x += adv + (60 if len(t) > 1 else 0)
        if len(t) > 1: x -= 60
        groups.append((unary_union(parts), x))
    total = sum(a for _, a in groups) * sc
    tr = (width - total) / (len(groups) - 1) if track is None else track * sc
    x = 0; out = []
    for g, adv in groups:
        out.append(affinity.translate(affinity.scale(g, sc, sc, origin=(0, 0)), x, y_top))
        x += adv * sc + tr
    return unary_union(out)

def lockup(word_geom, W, fontpath, bizfont, bold=0):
    minx, miny, maxx, maxy = word_geom.bounds
    w = maxx - minx
    size1 = w / 13.2
    g1 = line(fontpath, FULL, w, miny - 70 - size1 * 0.88, size1, bold)
    size2 = size1 * 0.62
    g2 = line(bizfont, BIZ, w, miny - 70 - size1 * 1.25 - size2 * 0.9, size2, track=180)
    g1 = affinity.translate(g1, minx - g1.bounds[0], 0)
    g2 = affinity.translate(g2, minx - g2.bounds[0], 0)
    return unary_union([word_geom, g1, g2])

def vb(g, pad=40):
    a, b, c, d = g.bounds
    return (a - pad, -d - pad, c - a + 2 * pad, d - b + 2 * pad)

def write_svg(name, g, fill='#000', bg=None, pad=40):
    s = svg([(to_path(g), fill)], vb(g, pad), bg=bg)
    open(os.path.join(OUT, name), 'w').write(s)
    return s

def raster(g, hpx, ss=8):
    a, b, c, d = g.bounds
    sc = hpx * ss / (d - b)
    W = int((c - a) * sc) + 2 * ss; H = hpx * ss + 2 * ss
    im = Image.new('L', (W, H), 255); dr = ImageDraw.Draw(im)
    for p in polys(g):
        dr.polygon([((x - a) * sc + ss, (d - y) * sc + ss) for x, y in p.exterior.coords], fill=0)
        for r in p.interiors:
            dr.polygon([((x - a) * sc + ss, (d - y) * sc + ss) for x, y in r.coords], fill=255)
    im = im.resize((W // ss, H // ss), Image.LANCZOS)
    big = im.resize((im.width * 6, im.height * 6), Image.NEAREST) if hpx <= 24 else im.resize((im.width * 2, im.height * 2), Image.NEAREST)
    b_ = io.BytesIO(); big.save(b_, 'PNG')
    return 'data:image/png;base64,' + base64.b64encode(b_.getvalue()).decode()

DIRS = [
    ('W1', '黑體・切角', W1, SANS, SANSB, SANS, '思源黑體 Black（OFL）'),
    ('W2', '明體', W2, SERIF, SERIF, SERIF, '思源宋體 Bold（OFL）'),
    ('W3', '楷書・延續車身', W3, KAI, KAI, KAI, '霞鶩文楷 Medium 加粗（OFL）'),
]
res = {}
for key, name, fn, base, fullfont, plainfont, src in DIRS:
    g, W = fn(); gr, _ = fn(rev=True)
    plain, _ = PLAIN(plainfont)
    bd = 22 if key == 'W3' else 0
    lk = lockup(g, W, fullfont, SANSB, bd)
    lkr = lockup(gr, W, fullfont, SANSB, max(bd - 6, 0)).buffer(0)
    res[key] = dict(
        name=name, src=src,
        main=write_svg(f'{key}_字標.svg', g),
        plain=write_svg(f'{key}_原字型.svg', plain),
        lock=write_svg(f'{key}_組合.svg', lk),
        rev=svg([(to_path(lkr), '#fff')], vb(lkr, 60), bg='#000'),
        px=[(h, raster(g, h)) for h in (16, 24, 48)],
        geom=g)
    open(os.path.join(OUT, f'{key}_組合_反白.svg'), 'w').write(res[key]['rev'])
print('ok', OUT)
import pickle
pickle.dump({k: {kk: vv for kk, vv in v.items() if kk != 'geom'} for k, v in res.items()}, open(os.path.join(OUT, 'res.pkl'), 'wb'))
