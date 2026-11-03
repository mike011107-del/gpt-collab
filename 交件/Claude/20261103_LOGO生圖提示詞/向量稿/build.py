"""G1、G2、G3 向量草稿：輸出 SVG（白底、深藍底反白、橘黃車身黑色）。
用法：python3 -I build.py 輸出資料夾
色號：主色 #194764、工程黃 #F39D16、朱紅 #D73626、淺冷灰 #E2E9EF（梁特助 11-03 12:02 指定）；車身 #D68702 是照片取色。
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from glyphs import SONG, CHUN, glyph_svg

NAVY, YELLOW, RED, WHITE, BLACK, TRUCK = "#194764", "#F39D16", "#D73626", "#FFFFFF", "#000000", "#D68702"

def rect(x, y, w, h, c):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{c}"/>'

def wordmark(x, y, C, c):
    gap = 0.06 * C
    return glyph_svg(SONG, x, y, C, colour=c) + glyph_svg(CHUN, x + C + gap, y, C, colour=c), 2 * C + gap

def shan(x, base_bottom, w, gap, outer, middle, c):
    """山：三根豎條＋底橫。base_bottom 是底橫下緣。"""
    parts = [rect(x, base_bottom - w, 3 * w + 2 * gap, w, c)]
    for i, h in enumerate([outer, middle, outer]):
        parts.append(rect(x + i * (w + gap), base_bottom - h, w, h, c))
    return "".join(parts)

def g1(fg, mark, bg):
    w, gap, outer, middle, C = 30, 48, 150, 230, 300
    pad = 60
    base = pad + 300
    s = shan(pad, base, w, gap, outer, middle, fg)
    s += rect(pad + w + gap, base - middle - 18 - w, w, w, mark)       # 中間豎條上方一格
    wm, ww = wordmark(pad + 3 * w + 2 * gap + 70, base - C + 0.035 * C, C, fg)
    W = pad + 3 * w + 2 * gap + 70 + ww + pad
    return W, base + pad, s + wm

def g2(fg, mark, bg):
    w, gap, C, pad = 30, 48, 260, 60
    bar_top = pad + 24 + C + 24
    middle = 24 + C + w      # 山中豎頂到字頂
    outer = int(middle * 0.6)
    base = bar_top + w
    s = shan(pad, base, w, gap, outer, middle, fg)
    x0 = pad + 3 * w + 2 * gap + 56
    wm, ww = wordmark(x0, bar_top - 24 - C + 0.035 * C, C, fg)
    bar_end = x0 + ww + 24
    s += rect(pad, bar_top, bar_end - pad, w, fg)
    s += rect(bar_end + 20, bar_top, w, w, mark)
    W = bar_end + 20 + w + pad
    return W, base + pad, s + wm

def g3(fg_box, fg_text, bg):
    C, m, gap, pad = 300, 46, 26, 60
    bw, bh = C + 2 * m, 2 * C + gap + 2 * m
    s = rect(pad, pad, bw, bh, fg_box)
    s += glyph_svg(SONG, pad + m, pad + m, C, colour=fg_text) + glyph_svg(CHUN, pad + m, pad + m + C + gap, C, colour=fg_text)
    return bw + 2 * pad, bh + 2 * pad, s

VERSIONS = {
    "G1": [("白底", lambda: g1(NAVY, RED, WHITE), WHITE), ("深藍底反白", lambda: g1(WHITE, YELLOW, NAVY), NAVY), ("車身黑色", lambda: g1(BLACK, BLACK, TRUCK), TRUCK)],
    "G2": [("白底", lambda: g2(NAVY, RED, WHITE), WHITE), ("深藍底反白", lambda: g2(WHITE, YELLOW, NAVY), NAVY), ("車身黑色", lambda: g2(BLACK, BLACK, TRUCK), TRUCK)],
    "G3": [("白底", lambda: g3(NAVY, WHITE, WHITE), WHITE), ("深藍底反白", lambda: g3(WHITE, NAVY, NAVY), NAVY), ("車身黑色", lambda: g3(BLACK, TRUCK, TRUCK), TRUCK)],
}

if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for g, vs in VERSIONS.items():
        for name, fn, bg in vs:
            W, H, body = fn()
            svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" viewBox="0 0 {W:.0f} {H:.0f}">{rect(0, 0, W, H, bg)}{body}</svg>'
            p = os.path.join(out, f"{g}_{name}.svg")
            open(p, "w", encoding="utf-8").write(svg)
            print(p)
