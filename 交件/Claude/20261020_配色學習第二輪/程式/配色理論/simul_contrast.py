# 同時對比示意：同一個工程黃 #D68702 放在 深青、靛藍、白、中灰（L*50）、黑 上。
# 算：WCAG 亮度比、APCA、ΔE2000、ΔL*、CIECAM02 模型預測的明度 J 與視彩度 M（背景亮度 Y_b 改變）、色弱模擬後的亮度比。
# 這是示意，不是配色提案。用 python3 -I 執行。
import sys, json, math
sys.path.insert(0, '/tmp/claude-0/r2/theory')
sys.path.insert(0, '/home/user/gpt-collab/.claude/skills/colour-tool/scripts')
import colourtool as ct
from systems_lib import hex2XYZ65, ciecam02

Y = '#D68702'
BG = [('深青', '#0C424A'), ('靛藍', '#333D66'), ('白', '#FFFFFF'), ('中灰 L*50', '#777777'), ('黑', '#000000')]
XYZ_W = hex2XYZ65('#FFFFFF'); L_A = 64 / math.pi * 0.2
rows = []
for name, bg in BG:
    Yb = max(ct.lum(bg) * 100, 1.0)  # 黑底 Y=0 模型會除以零，下限取 1
    cam = ciecam02(hex2XYZ65(Y), XYZ_W, L_A, Yb)
    # 視彩度 M = C * F_L^0.25
    k = 1 / (5 * L_A + 1); FL = 0.2 * k ** 4 * 5 * L_A + 0.1 * (1 - k ** 4) ** 2 * (5 * L_A) ** (1 / 3)
    bl = ct.oklch(bg)
    r = {'bg_name': name, 'bg': bg, 'fg': Y, 'wcag': round(ct.contrast(Y, bg), 2), 'apca_Lc': round(ct.apca(Y, bg), 1),
         'dE2000': round(ct.de(Y, bg), 1), 'dL': round(ct.lab(Y)[0] - ct.lab(bg)[0], 1),
         'cam02_Yb_used': round(Yb, 1), 'cam02_J_of_yellow': round(cam['J'], 1), 'cam02_M_of_yellow': round(cam['C'] * FL ** 0.25, 1),
         'cam02_h_of_yellow': round(cam['h'], 1),
         'bg_oklch_h': None if bl[1] < 0.02 else round(bl[2], 1),
         'induced_direction_oklch_h': None if bl[1] < 0.02 else round((bl[2] + 180) % 360, 1)}
    for kind in ('protan', 'deutan', 'tritan'):
        try:
            r['wcag_' + kind] = round(ct.contrast(ct.cvd(Y, kind), ct.cvd(bg, kind)), 2)
        except Exception as e:
            r['wcag_' + kind] = str(e)[:40]
    rows.append(r)
J = [r['cam02_J_of_yellow'] for r in rows]
# 10-19 補：黑底 Y_b=0 模型算不了，下限 1 是自訂假設；列出下限 0.5、2 的敏感度
black_floor = {str(fl): round(ciecam02(hex2XYZ65(Y), XYZ_W, L_A, fl)['J'], 1) for fl in (0.5, 1.0, 2.0)}
out = {'what': '同一個工程黃放在五種底上（示意，不是配色提案）', 'rows': rows,
       'cam02_J_range': [min(J), max(J)], 'black_bg_J_by_Yb_floor': black_floor,
       'notes': ['CIECAM02 只用背景亮度 Y_b 一個數字模擬底色影響，只能預測「變亮、變暗」，不會預測色相往底色補色方向偏（Albers 圖例裡最明顯的那種）。',
                 '色相偏移方向欄（induced_direction）只是「底色 OKLCH 色相 +180°」，是同時對比理論的方向，不是模型算出的偏移量。',
                 '觀看條件用 colour-science 的 sRGB 預設：L_A = 64/π×0.2 cd/m²、一般環境；黑底 Y_b 下限取 1。']}
json.dump(out, open('/tmp/claude-0/r2/theory/simul_contrast.json', 'w'), ensure_ascii=False, indent=1)
for r in rows:
    print(r)
