"""核對 chroma.js 文件 scale.mode 一節的說法：RGB 內插中段變灰、變暗；Lab 較好；HSL/Lch 太鮮。
用文件自己的例子 yellow→navy、#f00→#0f0，取中點。"""
import sys, math
sys.path.insert(0, '/tmp/claude-0/r2/scales')
sys.path.insert(0, '/home/user/gpt-collab/.claude/skills/colour-tool/scripts')
import leonardo as L
import colourtool as T
def mid_rgb(a, b):
    A, B = L.hex2rgb(a), L.hex2rgb(b); return L.rgb2hex(L.clip_round([(x + y) / 2 for x, y in zip(A, B)]))
def mid_lrgb(a, b):
    A, B = L.hex2rgb(a), L.hex2rgb(b)
    return L.rgb2hex(L.clip_round([math.sqrt((x * x + y * y) / 2) for x, y in zip(A, B)]))
def mid_lab(a, b):
    A, B = L.rgb2lab(L.hex2rgb(a)), L.rgb2lab(L.hex2rgb(b)); return L.rgb2hex(L.clip_round(L.lab2rgb_float([(x + y) / 2 for x, y in zip(A, B)])))
def mid_lch(a, b):
    A, B = L.rgb2lab(L.hex2rgb(a)), L.rgb2lab(L.hex2rgb(b))
    ca, cb = math.hypot(A[1], A[2]), math.hypot(B[1], B[2])
    ha, hb = math.degrees(math.atan2(A[2], A[1])) % 360, math.degrees(math.atan2(B[2], B[1])) % 360
    dh = ((hb - ha + 180) % 360) - 180; h = ha + dh / 2; c = (ca + cb) / 2; l = (A[0] + B[0]) / 2
    return L.rgb2hex(L.clip_round(L.lab2rgb_float([l, c * math.cos(math.radians(h)), c * math.sin(math.radians(h))])))
def desc(h):
    l = T.lch(h); return {'hex': h, 'L*': round(l[0], 1), 'C*': round(l[1], 1)}
for a, b in [('#ffff00', '#000080'), ('#ff0000', '#00ff00')]:
    print(a, b, 'ends', desc(a), desc(b))
    for name, f in [('rgb', mid_rgb), ('lrgb', mid_lrgb), ('lab', mid_lab), ('lch', mid_lch)]:
        print('  mid', name, desc(f(a, b)))
