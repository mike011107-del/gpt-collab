# 驗證：拿作者給的測試值與常數，檢查我改寫的程式。結果寫進 data/validation.json
import json, math, sys, time
import numpy as np
sys.path.insert(0, '/tmp/claude-0/r2/models')
import models_lib as M

out = {}

# 1. MCU temperature_cache_test.ts 的 rawTemperature 測試值（Ou 冷暖）
exp = {'#0000FF': -1.393, '#FF0000': 2.351, '#00FF00': -0.267, '#FFFFFF': -0.5, '#000000': -0.5}
r = {}
for h, e in exp.items():
    v = M.ou_warm_cool(M.lab_from_hex(h))
    r[h] = dict(expected=e, got=round(v, 4), ok=abs(v - e) < 5e-4)
out['mcu_rawTemperature'] = r

# 2. MCU hct_test.ts 的 CAM16 測試值
exp = {'#FF0000': (27.408, 113.358, 46.445), '#00FF00': (142.140, 108.410, 79.332),
       '#0000FF': (282.788, 87.231, 25.466), '#FFFFFF': (209.492, 2.869, 100.0)}
r = {}
for h, (eh, ec, ej) in exp.items():
    c = M.cam16_from_hex(h)
    ok = abs(c['hue'] - eh) < 5e-3 and abs(c['chroma'] - ec) < 5e-3 and abs(c['j'] - ej) < 5e-3
    r[h] = dict(expected=[eh, ec, ej], got=[round(c['hue'], 4), round(c['chroma'], 4), round(c['j'], 4)], ok=ok)
out['mcu_cam16'] = r

# 3. MCU dislike_analyzer_test.ts
liked = ['#F6EDE4', '#F3E7DB', '#F7EAD0', '#EADABA', '#D7BD96', '#A07E56', '#825C43', '#604134', '#3A312A', '#292420']
disliked = ['#95884B', '#716B40', '#B08E00', '#4C4308', '#464521']
out['mcu_dislike'] = dict(
    liked_all_false=all(not M.mcu_is_disliked(h) for h in liked),
    disliked_all_true=all(M.mcu_is_disliked(h) for h in disliked))

# 4. CIEDE2000：Sharma 2005 測試資料（抄自 colourtool.py SHARMA 表）
sharma = [(50.0, 2.6772, -79.7751, 50.0, 0.0, -82.7485, 2.0425),
          (50.0, 0.0, 0.0, 50.0, -1.0, 2.0, 2.3669),
          (50.0, 2.5, 0.0, 73.0, 25.0, -18.0, 27.1492),
          (60.2574, -34.0099, 36.2677, 60.4626, -34.1751, 39.4387, 1.2644),
          (2.0776, 0.0795, -1.1350, 0.9033, -0.0636, -0.5514, 0.9082)]
r = []
for t in sharma:
    v = M.ciede2000(t[:3], t[3:6])
    vv = float(M.ciede2000_vec(*[np.array([x]) for x in t[:6]])[0])
    r.append(dict(expected=t[6], got=round(v, 4), got_vec=round(vv, 4), ok=abs(v - t[6]) < 1e-4 and abs(vv - t[6]) < 1e-4))
out['ciede2000_sharma'] = r

# 5. Colorgorical：model.py 寫的「從 8325 色預先算好」的上下限
CG = M.Colorgorical('/tmp/claude-0/r2/models/data/colorgorical_tables.npz')
G = CG.grid
n = len(G)
t0 = time.time()
demax, demin = -1, 1e9
for i in range(n - 1):
    d = M.ciede2000_vec(G[i, 0], G[i, 1], G[i, 2], G[i + 1:, 0], G[i + 1:, 1], G[i + 1:, 2])
    demax = max(demax, float(d.max())); demin = min(demin, float(d.min()))
out['colorgorical_de_bounds'] = dict(expected_max=CG.DE_MAX, expected_min=CG.DE_MIN, got_max=demax, got_min=demin,
                                    ok=abs(demax - CG.DE_MAX) < 1e-4 and abs(demin - CG.DE_MIN) < 1e-4)

# PP 全配對（向量化，照 pairPreference.c）
cool = np.array([CG.coolness(tuple(int(v) for v in g)) for g in G])
illC = np.array([CG.d65_to_illC(*g) for g in G])
Hc = np.degrees(np.arctan2(illC[:, 2], illC[:, 1])); Hc = np.where(Hc < 0, Hc + 360, Hc)
Lc = illC[:, 0]
achrom = (G[:, 1] == 0) & (G[:, 2] == 0)
chrom_idx = np.where(~achrom)[0]
print('coolness 範圍（彩色格點）', cool[chrom_idx].min(), cool[chrom_idx].max(), '無定義數', int((cool[chrom_idx] < 0).sum()))
nrm = lambda d, hi, lo: (d - lo) / (hi - lo)
ppmax, ppmin = -1e9, 1e9
ppmax_w, ppmin_w = -1e9, 1e9
valid = CG.valid
ppmax_v, ppmin_v = -1e9, 1e9
for k, i in enumerate(chrom_idx[:-1]):
    j = chrom_idx[k + 1:]
    dL = np.abs(Lc[i] - Lc[j]); dH = np.abs(Hc[i] - Hc[j]); sC = cool[i] + cool[j]
    pp = CG.WL * nrm(dL, CG.LMAX, CG.LMIN) + CG.WH * nrm(dH, CG.HMAX, CG.HMIN) + CG.WC * nrm(sC, CG.CMAX, CG.CMIN)
    ppmax = max(ppmax, float(pp.max())); ppmin = min(ppmin, float(pp.min()))
    vm = valid[i] & valid[j]
    if vm.any():
        ppmax_v = max(ppmax_v, float(pp[vm].max())); ppmin_v = min(ppmin_v, float(pp[vm].min()))
    dHw = np.where(dH > 180, 360 - dH, dH)
    ppw = CG.WL * nrm(dL, CG.LMAX, CG.LMIN) + CG.WH * nrm(dHw, CG.HMAX, CG.HMIN) + CG.WC * nrm(sC, CG.CMAX, CG.CMIN)
    ppmax_w = max(ppmax_w, float(ppw.max())); ppmin_w = min(ppmin_w, float(ppw.min()))
out['colorgorical_pp_bounds'] = dict(
    expected_max=CG.PP_MAX, expected_min=CG.PP_MIN,
    got_all_chromatic=[round(ppmax, 3), round(ppmin, 3)],
    got_rgb_valid_only=[round(ppmax_v, 3), round(ppmin_v, 3)],
    got_wrapped_hue_variant=[round(ppmax_w, 3), round(ppmin_w, 3)],
    n_chromatic_grid=int(len(chrom_idx)), n_valid_rgb=int(valid.sum()))

# NU：程式寫死最小熵 -4.5
ents = []
for g in G:
    ents.append(1 - CG.name_uniqueness(tuple(int(v) for v in g)))  # 回推正規化熵
ents = np.array(ents) * 4.5 - 4.5
out['colorgorical_nu_entropy'] = dict(hardcoded_min=-4.5, got_min=round(float(ents.min()), 3), got_max=round(float(ents.max()), 3))

# 6. Lab 與 colourtool 交叉檢查（幾個色）
sys.path.insert(0, '/home/user/gpt-collab/.claude/skills/colour-tool/scripts')
import colourtool as CT
r = {}
for h in ['#0C424A', '#333D66', '#D68702', '#FFFFFF']:
    a = M.lab_from_hex(h); b = CT.lab(h)
    r[h] = dict(mine=[round(x, 3) for x in a], colourtool=[round(x, 3) for x in b])
r['dE_teal_yellow'] = dict(mine=round(M.ciede2000(M.lab_from_hex('#0C424A'), M.lab_from_hex('#D68702')), 4),
                           colourtool=round(CT.de('#0C424A', '#D68702'), 4))
out['lab_crosscheck'] = r
out['seconds'] = round(time.time() - t0, 1)

json.dump(out, open('/tmp/claude-0/r2/models/data/validation.json', 'w'), ensure_ascii=False, indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))
print(json.dumps(out, ensure_ascii=False, indent=1))
