# 面積與比例：
# (a) Goethe／Schopenhauer 明度權重（Hirschler 演講逐字稿引述：紫 1/4、藍 1/3、綠 1/2、紅 1/2、橘 2/3）對照 Munsell renotation real.py 各色相最高彩度點的明度
#     10-19 修正：real.py 是 1943 renotation 裡落在 MacAdam 極限內的理論點（docstring：within MacAdam limits），不是實體色票；
#     5P 最高彩度 32 在 V3、V4 並列，5G 的 28 在 V5、V6 並列，兩種取法都列。
# (b) 兩條「平衡面積」公式套在已定的工程黃與候選色上（示意，不是比例建議）：
#     L* 倒數式：面積 ∝ 1 / CIELAB L*（仿 Goethe/Itten 的明度倒數想法，但不是 Goethe 的權重表，10-19 改名）；Munsell（逐字稿引述的例子 5/10 紅 對 5/5 藍綠 要兩倍面積）：面積 × 明度 × 彩度 相等
import sys, json
sys.path.insert(0, '/tmp/claude-0/r2/theory')
sys.path.insert(0, '/home/user/gpt-collab/.claude/skills/colour-tool/scripts')
import colourtool as ct
from systems_lib import munsell
from munsell_conv import load, xyYC2hex

real = load('real')
GOETHE = {'P': 1 / 4, 'PB': 1 / 3, 'G': 1 / 2, 'R': 1 / 2, 'YR': 2 / 3}
a = {}
for fam in ['Y', 'YR', 'R', 'P', 'PB', 'G']:
    page = [r for r in real if r[1] == fam and r[0] == 5.0]
    cmax = max(r[3] for r in page)
    tops = sorted([r for r in page if r[3] == cmax], key=lambda r: r[2])  # 最高彩度可能在幾個明度並列
    pts = []
    for s_, f, V, C, x, y, Y in tops:
        hx, oog = xyYC2hex(x, y, Y * 0.975)
        pts.append({'point': f'5{fam} {V:g}/{C:g}', 'V_over_10': V / 10, 'srgb_approx': hx, 'out_of_srgb': oog})
    a[fam] = {'max_chroma': cmax, 'tied_points': pts, 'V_over_10_options': [q['V_over_10'] for q in pts], 'goethe_weight': GOETHE.get(fam),
              'what_it_is': 'real.py 理論點（MacAdam 極限內），不是實體色票'}
# Itten 面積比（逐字稿）：黃:紫 = 1:3、橘:藍 = 1:2、紅:綠 = 1:1；用 real.py 最高彩度點的 V 重算同樣的倒數比；並列時兩種取法都列
def ratios(f1, f2):
    return sorted({round(v1 / v2, 2) for v1 in a[f1]['V_over_10_options'] for v2 in a[f2]['V_over_10_options']}, reverse=True)
itten = {k: {'itten': it, 'munsell_V_based_options': [f'1:{r:g}' for r in ratios(f1, f2)]}
         for k, it, f1, f2 in [('黃:紫', '1:3', 'Y', 'P'), ('橘:藍', '1:2', 'YR', 'PB'), ('紅:綠', '1:1', 'R', 'G')]}
itten['_reading'] = '紫、綠取較低明度（5P 3/32、5G 5/28）時是 1:3.0、1:1.75、1:1.0，跟 Itten 很接近；取較高明度（5P 4/32、5G 6/28）時黃:紫 1:2.25、紅:綠 1:0.83（綠比紅亮，綠的面積反而較小；換個寫法是紅 1.2 倍於綠）。接不接近看取法而定。'


def balance(fg, bg):
    mf, mb = munsell(fg), munsell(bg)
    Lf, Lb = ct.lab(fg)[0], ct.lab(bg)[0]
    g = Lf / Lb  # 背景面積 / 前景面積（面積與 L* 成反比）
    m = (mf['V'] * mf['C']) / (mb['V'] * max(mb['C'], 0.5))
    sg, sm = 1 / (1 + g), 1 / (1 + m)
    return {'fg': fg, 'bg': bg, 'fg_munsell': mf['text'], 'bg_munsell': mb['text'],
            'inverse_Lstar_bg_per_fg': round(g, 2), 'inverse_Lstar_fg_share': round(sg, 3),
            'munsell_VC_bg_per_fg': round(m, 2), 'munsell_fg_share': round(sm, 3),
            'share_ratio_inverseL_over_VC': round(sg / sm, 2)}


SC = [('工程黃 對 深青', '#D68702', '#0C424A'), ('工程黃 對 靛藍', '#D68702', '#333D66')]
peers = json.load(open('/tmp/claude-0/work/peer_schemes.json'))
pick = {p['name']: p for p in peers}
PEER = [('Kier 紅 對 藍綠', pick['Kier']['cols'][0], pick['Kier']['cols'][1]),
        ('SUEZ 綠 對 深藍', pick['SUEZ']['cols'][0], pick['SUEZ']['cols'][1]),
        ('Metro Rod 綠 對 深紫藍', '#2EA836', '#2E1D67'),
        ('Roto-Rooter 紅 對 深紫藍', '#DA291C', '#2A1768')]
out = {'a_goethe_vs_munsell': a, 'itten_area_ratios': itten,
       'b_formula_demo_songchun': [dict(balance(f, b), label=l) for l, f, b in SC],
       'b_formula_demo_peers': [dict(balance(f, b), label=l) for l, f, b in PEER],
       'rule_60_30_10_accent_share': 0.10,
       'notes': ['「L* 倒數式」是面積與 CIELAB L* 成反比，原本叫 Goethe 式，但不是 Goethe 的權重表，10-19 改名。兩式對工程黃配深青差 2.5 倍、配靛藍差 1.7 倍。',
                 '兩條公式都只說「看起來力量平衡」的面積，沒有說平衡就好看；Hirschler 演講也說這種平衡的美感價值可疑。',
                 'Goethe 數字是 1810 年代對顏料的估計，逐字稿是自動字幕，紫 1/4、藍 1/3 等是演講者口述引用。',
                 'Munsell 規則（面積×明度×彩度）只從逐字稿的一個例子得知，未讀到 A Grammar of Color 原文。',
                 '同業 logo 沒有量各色面積，公式算出的比例無法跟實際對照。']}
json.dump(out, open('/tmp/claude-0/r2/theory/area_balance.json', 'w'), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=0)[:3500])
