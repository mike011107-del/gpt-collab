# 用 PIL 畫給報告用的圖（色塊為主）。資料都從本資料夾的 JSON 讀。
import json, math
from PIL import Image, ImageDraw, ImageFont
import sys
sys.path.insert(0, '/home/user/gpt-collab/.claude/skills/colour-tool/scripts')
import colourtool as ct
D = '/tmp/claude-0/r2/theory/'
F = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
f = lambda s: ImageFont.truetype(F, s)
INK, SUB = (30, 30, 30), (110, 110, 110)

def lum_txt(hx):
    r, g, b = (int(hx[i:i + 2], 16) for i in (1, 3, 5))
    return (255, 255, 255) if (0.299 * r + 0.587 * g + 0.114 * b) < 140 else INK

# 圖 1：同時對比
S = json.load(open(D + 'simul_contrast.json'))
W = 5 * 240 + 40; im = Image.new('RGB', (W, 500), 'white'); d = ImageDraw.Draw(im)
d.text((20, 14), '同一個工程黃 #D68702 放在五種底上（示意，不是配色提案）', font=f(24), fill=INK)
for i, r in enumerate(S['rows']):
    x = 20 + i * 240; y = 60
    d.rectangle([x, y, x + 220, y + 220], fill=r['bg'], outline=(200, 200, 200))
    d.rectangle([x + 75, y + 75, x + 145, y + 145], fill=r['fg'])
    d.text((x, y + 232), f"{r['bg_name']}  {r['bg']}", font=f(18), fill=INK)
    d.text((x, y + 260), f"亮度比 {r['wcag']}:1", font=f(18), fill=INK)
    d.text((x, y + 286), f"色差 ΔE2000 {r['dE2000']}", font=f(18), fill=INK)
    d.text((x, y + 312), f"明度差 ΔL* {r['dL']:+}", font=f(18), fill=INK)
    d.text((x, y + 338), f"模型明度 J {r['cam02_J_of_yellow']}", font=f(18), fill=SUB)
d.text((20, 435), 'J：CIECAM02 依底色亮度預測黃看起來多亮（白底 46、黑底 61）。模型不預測色相偏移。', font=f(16), fill=SUB)
bf = S['black_bg_J_by_Yb_floor']
d.text((20, 462), f"黑底的背景亮度 Y_b=0 模型算不了，這裡自訂下限 Y_b=1；取 0.5 或 2 時黑底 J 是 {bf['0.5']} 或 {bf['2.0']}。", font=f(16), fill=SUB)
im.save(D + 'fig_simul_contrast.png')

# 圖 2：Itten 對比的同業例子
I = json.load(open(D + 'itten_examples.json'))['examples']
def dh_exact(a, b):
    x = abs(ct.oklch(a)[2] - ct.oklch(b)[2]) % 360; return min(x, 360 - x)
wc = I['冷暖對比'][0]; kr = I['補色對比'][0]; sz = I['補色對比'][1]
rows = [('色相對比', 'Watercare 四色、三群色相', I['色相對比'][0]['cols'], '', False),
        ('明暗對比', 'Insituform 同色相，只差深淺', [I['明暗對比'][1]['a']['hex'], I['明暗對比'][1]['b']['hex']], f"ΔL* {I['明暗對比'][1]['dL']}　色相差 {I['明暗對比'][1]['dh']}°", False),
        ('冷暖對比', 'Watercare 紅＋藍，幾乎一樣亮', [wc['a']['hex'], wc['b']['hex']], f"ΔL* {wc['dL']}　色相差 {dh_exact(wc['a']['hex'], wc['b']['hex']):.1f}°", False),
        ('補色對比', 'Kier 紅＋藍綠，色相接近相對', [kr['a']['hex'], kr['b']['hex']], f"色相差 {dh_exact(kr['a']['hex'], kr['b']['hex']):.1f}°　ΔL* {kr['dL']}　轉黑白會糊", False),
        ('彩度對比', 'Tideway 青綠＋灰，亮度相近', [I['彩度對比'][0]['a']['hex'], I['彩度對比'][0]['b']['hex']], f"C* 差 {I['彩度對比'][0]['dC']}　ΔL* {I['彩度對比'][0]['dL']}", False),
        ('彩度對比【跨公司】', 'Uisce Éireann 藍 對 KAISER 藍', [I['彩度對比_跨公司'][0]['a']['hex'], I['彩度對比_跨公司'][0]['b']['hex']], f"C* 差 {I['彩度對比_跨公司'][0]['dC']}　ΔL* {I['彩度對比_跨公司'][0]['dL']}", True)]
TAG = (176, 70, 0)
im = Image.new('RGB', (1180, 80 + 130 * len(rows) + 330), 'white'); d = ImageDraw.Draw(im)
d.text((20, 14), 'Itten 對比：國外同業 logo 的實際顏色（五種有單一 logo 內的實例）', font=f(26), fill=INK)
for k, (t, sub, cols, m, flag) in enumerate(rows):
    y = 70 + k * 130
    d.text((20, y + 20), t, font=f(22), fill=TAG if flag else INK); d.text((20, y + 54), sub, font=f(15), fill=TAG if flag else SUB); d.text((20, y + 80), m, font=f(16), fill=SUB)
    if flag: d.text((20, y + 104), '兩家拼的，不是同一個 logo', font=f(15), fill=TAG)
    for j, c in enumerate(cols):
        x = 400 + j * 190
        d.rectangle([x, y, x + 180, y + 110], fill=c); d.text((x + 8, y + 82), c, font=f(16), fill=lum_txt(c))
y = 70 + len(rows) * 130
s_ = I['同時對比']
d.text((20, y + 10), '同時對比【示意】', font=f(22), fill=TAG)
d.text((20, y + 44), f"三家拼的，不是實際用法：{s_['gray_from']} 的灰 {s_['gray']['hex']} 放在 {s_['bg1_from']} 橘、{s_['bg2_from']} 藍上", font=f(16), fill=TAG)
for j, bg in enumerate([s_['bg1'], s_['bg2']]):
    x = 400 + j * 300
    d.rectangle([x, y + 80, x + 280, y + 240], fill=bg['hex']); d.rectangle([x + 100, y + 120, x + 180, y + 200], fill=s_['gray']['hex'])
d.text((20, y + 80), '理論：灰在橘底偏藍、\n在藍底偏橘。', font=f(16), fill=SUB)
d.text((20, y + 262), f"面積對比：同業沒有各色面積資料，找不到例子。SUEZ 黃綠＋深藍色相差只有 {dh_exact(sz['a']['hex'], sz['b']['hex']):.1f}°，不當補色例子。", font=f(16), fill=SUB)
d.text((20, y + 288), '橘字標【跨公司】、【示意】的不是單一 logo 內的實例。', font=f(16), fill=SUB)
im.save(D + 'fig_itten_peers.png')

# 圖 3：Munsell 明度×彩度（同業主色＋崧淳三色）與相對彩度
Sy = json.load(open(D + 'systems_colors.json'))
im = Image.new('RGB', (1180, 640), 'white'); d = ImageDraw.Draw(im)
d.text((20, 14), 'Munsell 明度 × 彩度：42 家同業主色（圓點）與三個崧淳色（方塊）', font=f(24), fill=INK)
X0, Y0, Wd, Ht = 90, 560, 1040, 480  # C 0–24, V 0–10
for c in range(0, 25, 4):
    x = X0 + c / 24 * Wd; d.line([x, Y0, x, Y0 - Ht], fill=(232, 232, 232)); d.text((x - 8, Y0 + 8), str(c), font=f(16), fill=SUB)
for v in range(0, 11, 2):
    y = Y0 - v / 10 * Ht; d.line([X0, y, X0 + Wd, y], fill=(232, 232, 232)); d.text((X0 - 30, y - 9), str(v), font=f(16), fill=SUB)
d.text((X0 + Wd / 2 - 60, Y0 + 34), 'Munsell 彩度 C', font=f(18), fill=INK); d.text((20, 44), '明度 V', font=f(18), fill=INK)
for p in Sy['peers']:
    if not p['cols']: continue
    c = p['cols'][0]; x = X0 + min(c['munsell_C'], 24) / 24 * Wd; y = Y0 - c['munsell_V'] / 10 * Ht
    d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=c['hex'], outline=(160, 160, 160))
for nm, c in Sy['songchun'].items():
    x = X0 + c['munsell_C'] / 24 * Wd; y = Y0 - c['munsell_V'] / 10 * Ht
    d.rectangle([x - 13, y - 13, x + 13, y + 13], fill=c['hex'], outline=INK, width=2)
    off = {'深青': (-20, 18), '靛藍': (18, -40), '工程黃': (18, -12)}[nm]
    d.text((x + off[0], y + off[1]), f"{nm} {c['munsell']}", font=f(17), fill=INK)
im.save(D + 'fig_munsell_vc.png')

# 圖 4：和田三造兩色組 vs 同盒隨機（10-19 修正：每次重新抽樣，兩個種子各 2 萬次）
Wd_ = json.load(open(D + 'wada_stats.json')); t = Wd_['test_vs_weighted_random_fresh_123x20000x2seeds']; pt = Wd_['pccs_same_tone_test']
items = [('明度差 < 10', t['dL_lt10_share']), ('明度差 ≥ 26', t['dL_ge26_share']), ('色相差 < 30°', t['dh_lt30_share']), ('色相差 ≥ 150°', t['dh_ge150_share'])]
im = Image.new('RGB', (1000, 450), 'white'); d = ImageDraw.Draw(im)
d.text((20, 14), '和田三造《配色總鑑》123 組兩色配色 vs 同一盒色隨機配（每次重抽，2 萬次 × 2）', font=f(21), fill=INK)
for k, (lab, v) in enumerate(items + [('同一 PCCS 色調', {'wada': pt['wada_same_tone_share'], 'sim_median': pt['random_same_tone_share_median'], 'two_sided_p': pt['p_same']})]):
    y = 70 + k * 64
    pr = v.get('p_range'); ptxt = f"p≈{v['two_sided_p']:.2f}"
    edge = lab == '色相差 < 30°'
    d.text((20, y + 8), lab, font=f(18), fill=INK)
    d.rectangle([220, y, 220 + v['wada'] * 900, y + 22], fill=(60, 60, 60)); d.text((230 + v['wada'] * 900, y), f"和田 {v['wada']:.0%}", font=f(16), fill=INK)
    d.rectangle([220, y + 26, 220 + v['sim_median'] * 900, y + 48], fill=(180, 180, 180))
    d.text((230 + v['sim_median'] * 900, y + 28), f"隨機 {v['sim_median']:.0%}　{ptxt}" + ('　邊界' if edge else ''), font=f(16), fill=INK if edge else SUB)
d.text((20, 392), '色相差 < 30° 在邊界：和田的同色相配對偏少，方向跟刻意拉開色相一致，但未達一般顯著水準。', font=f(16), fill=SUB)
d.text((20, 416), '其他四項沒有測到差別。只有 123 組，檢定力有限，不顯著不等於沒有差別。hex 是 CMYK 直接換算。', font=f(16), fill=SUB)
im.save(D + 'fig_wada.png')
print('ok')
