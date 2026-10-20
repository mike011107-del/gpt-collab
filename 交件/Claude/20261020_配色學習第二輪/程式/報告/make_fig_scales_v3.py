"""把 scales.json 的色階畫成一張 HTML 色條圖（報告 A5 版 v3：只放大字級、調版面）。
原稿：/tmp/claude-0/r2/scales/make_fig.py。數據、色碼、框線位置不變。
圖寬 900px、報告顯示寬 105mm → 最小字 2.2*900/105=18.9px，這裡用 20px。
轉 PNG：NODE_PATH=$(npm root -g) node render.cjs fig_vattenfall_scales_v3.html ../img/fig_vattenfall_scales_v3.png 900 1
"""
import json
d = json.load(open('/tmp/claude-0/r2/scales/scales.json'))
c = json.load(open('/tmp/claude-0/r2/scales/scale_curves.json'))
rows = [
    ('Material Tonal Spot 主色板（chroma 36）', [x['hex'] for x in d['material']['tonal_spot_palettes']['primary']['tones']][::-1], [str(x['tone']) for x in d['material']['tonal_spot_palettes']['primary']['tones']][::-1]),
    ('Material Fidelity 主色板（原色 chroma）', [x['hex'] for x in d['material']['fidelity_primary_palette']['tones']][::-1], [str(x['tone']) for x in d['material']['fidelity_primary_palette']['tones']][::-1]),
    ('Radix 產生器（亮色）', [x['hex'] for x in d['radix']['accent_scale']], [str(i) for i in range(1, 13)]),
    ('Radix 官方 blue（對照）', [x['hex'] for x in d['radix']['official_blue_for_comparison']], [str(i) for i in range(1, 13)]),
    ('Leonardo（LAB，目標＝Radix blue 對比）', [x['hex'] for x in d['leonardo']['lab_interpolation']], [str(x['ratio_target']) for x in d['leonardo']['lab_interpolation']]),
    ('Tailwind 3 blue（對照）', c['tailwind3']['blue_hex'], [str(s) for s in c['tailwind3']['steps']]),
]
h = ['<!doctype html><meta charset="utf-8"><style>body{font-family:sans-serif;background:#fff;margin:12px 16px 14px;width:860px}.r{display:flex;margin:0 0 10px}.s{flex:1;box-sizing:border-box;height:46px;font-size:20px;line-height:1;display:flex;align-items:flex-end;justify-content:center;padding-bottom:6px}h4{margin:0 0 5px;font-size:20px;line-height:1.25}h4.t{font-size:21px;margin-bottom:8px}</style>',
     '<h4 class="t">例子：Vattenfall 藍 #2071B5（與崧淳無關）</h4>']
for title, cols, labs in rows:
    h.append('<h4>%s</h4><div class="r">' % title)
    for col, lab in zip(cols, labs):
        r, g, b = (int(col[i:i + 2], 16) for i in (1, 3, 5))
        y = 0.2126 * (r / 255) ** 2.2 + 0.7152 * (g / 255) ** 2.2 + 0.0722 * (b / 255) ** 2.2
        fg = '#000' if y > 0.25 else '#fff'
        mark = ' outline:3px solid #000' if col.lower() == '#2071b5' else ''
        h.append('<div class="s" style="background:%s;color:%s;%s">%s</div>' % (col, fg, mark, lab))
    h.append('</div>')
open('/tmp/claude-0/report2/figsrc/fig_vattenfall_scales_v3.html', 'w', encoding='utf-8').write('\n'.join(h))
