# 補充：工程黃與 MCU「不喜歡」測試色的距離；Colorgorical 冷度曲線；Ou 冷暖曲線。輸出 data/extras.json、data/fig_*.json
import json, math, sys
import numpy as np
sys.path.insert(0, '/tmp/claude-0/r2/models')
import models_lib as M

CG = M.Colorgorical('/tmp/claude-0/r2/models/data/colorgorical_tables.npz')
out = {}

# 1. MCU dislike 測試色（dislike_analyzer_test.ts 裡判定為不喜歡的 5 色）跟工程黃
y = '#D68702'
ly = M.lab_from_hex(y)
hy = M.hct_from_hex(y)
rows = []
for h in ['#95884B', '#716B40', '#B08E00', '#4C4308', '#464521']:
    hh = M.hct_from_hex(h)
    rows.append(dict(hex=h, hct=[round(v, 1) for v in hh], dE2000_to_yellow=round(M.ciede2000(ly, M.lab_from_hex(h)), 2)))
out['yellow_vs_mcu_disliked_tests'] = dict(yellow_hct=[round(v, 1) for v in hy], tests=rows,
                                           zone='HCT 色相 90–111、彩度 >16、tone <65')
# 工程黃：保持 HCT 彩度與 tone，只轉色相，從幾度開始進入不喜歡區（用 Lab 判斷不了，要 HCT）
# 這裡只報色相差：90 - 目前色相
out['yellow_hue_gap_to_dislike_zone'] = round(90 - hy[0], 1)

# 2. Colorgorical 冷度表：L=50、C 介於 30 與 45 的格點，冷度對 Lab 色相
pts = []
for g in CG.grid:
    L, a, b = (int(v) for v in g)
    C = math.hypot(a, b)
    if L == 50 and 30 <= C <= 45:
        pts.append(dict(lab=[L, a, b], h=round(math.degrees(math.atan2(b, a)) % 360, 1), C=round(C, 1),
                        coolness=CG.coolness((L, a, b))))
pts.sort(key=lambda p: p['h'])
out['coolness_curve_L50'] = dict(n=len(pts), min=min(p['coolness'] for p in pts), max=max(p['coolness'] for p in pts),
                                 h_at_max=[p['h'] for p in pts if p['coolness'] == max(q['coolness'] for q in pts)][:5],
                                 h_at_min=[p['h'] for p in pts if p['coolness'] == min(q['coolness'] for q in pts)][:5])
json.dump(dict(desc='Colorgorical 冷度表（Schloss & Palmer 2011 冷度，Munsell 10R 起算的色相步數，經 Colorgorical 線性內插到 CIELAB）；L*=50、C* 30–45 的格點',
               points=pts), open('/tmp/claude-0/r2/models/data/fig_coolness_curve.json', 'w'), ensure_ascii=False, indent=1)

# 3. Ou 冷暖公式曲線：C* = 20、40、70，色相 0–359
curve = {}
for C in (20, 40, 70):
    curve[str(C)] = [round(-0.5 + 0.02 * C ** 1.07 * math.cos(math.radians(h - 50)), 3) for h in range(0, 360, 5)]
json.dump(dict(desc='Ou 等人 2004 冷暖公式（經 MCU）：WC = -0.5 + 0.02·C*^1.07·cos(h-50°)；h 每 5 度', hue=list(range(0, 360, 5)), wc=curve),
          open('/tmp/claude-0/r2/models/data/fig_ou_wc_curve.json', 'w'), ensure_ascii=False, indent=1)
# 冷暖為 0 的色相（C*=40）
c40 = 40
zeros = [h for h in np.arange(0, 360, 0.5) if abs(-0.5 + 0.02 * c40 ** 1.07 * math.cos(math.radians(h - 50))) < 0.01]
out['ou_wc_zero_hues_C40'] = [float(z) for z in zeros]

json.dump(out, open('/tmp/claude-0/r2/models/data/extras.json', 'w'), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False))
