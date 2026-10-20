# 和田三造《配色總鑑》第一冊數位版（color-name-lists 3.34.0 的 sanzo-wada-I.json：159 色、348 組配色）
# 問：設計師挑的配色，明度差、色相差跟「同一盒 159 色隨機配」比起來有什麼不同？
# 注意：hex 是從 CMYK 直接換算（先驗證），不是實際印刷色；只看相對關係。
import sys, json, math, itertools
sys.path.insert(0, '/home/user/gpt-collab/.claude/skills/colour-tool/scripts')
import numpy as np
import colourtool as ct
from collections import defaultdict, Counter

D = json.load(open('/tmp/claude-0/r2/src/npm-color-name-lists/x/package/lib/colors/sanzo-wada-I.json'))
# 驗證 hex = 255×(1−C)(1−K) 這種直接換算；不符的記下來，資料錯誤（例：Citrine 寫成 #000000）改用 CMYK 直接換算
naive, fixed = 0, []
for c in D:
    C, M, Y, K = [v / 100 for v in c['cmyk_array']]
    pred = [min(255, max(0, round(255 * (1 - v) * (1 - K)))) for v in (C, M, Y)]  # 資料裡有 M=106 這種超過 100 的值，截到 0–255
    got = [int(c['hex'][i:i + 2], 16) for i in (1, 3, 5)]
    if max(abs(a - b) for a, b in zip(pred, got)) <= 1:
        naive += 1
    else:
        fixed.append({'name': c['name'], 'hex_in_data': c['hex'], 'cmyk': c['cmyk_array'], 'hex_used': '#' + ''.join(f'{v:02X}' for v in pred)})
        c['hex'] = fixed[-1]['hex_used']
combos = defaultdict(list)
for c in D:
    for k in c['combinations']:
        combos[k].append(c['hex'])
sizes = Counter(len(v) for v in combos.values())


def okh(h): return ct.oklch(h)
def dh(a, b):
    d = abs(a - b) % 360; return min(d, 360 - d)


def pair_stats(a, b):
    La, Ca, ha = okh(a); Lb, Cb, hb = okh(b)
    both = Ca >= 0.04 and Cb >= 0.04
    return abs(ct.lab(a)[0] - ct.lab(b)[0]), (dh(ha, hb) if both else None), ct.de(a, b)


def summarize(pairs):
    dL = np.array([p[0] for p in pairs]); dH = np.array([p[1] for p in pairs if p[1] is not None]); dE = np.array([p[2] for p in pairs])
    return {'n': len(pairs), 'dL_median': round(float(np.median(dL)), 1), 'dL_ge26_share': round(float((dL >= 26).mean()), 3),
            'dL_lt10_share': round(float((dL < 10).mean()), 3),
            'dh_median': round(float(np.median(dH)), 1), 'dh_lt30_share': round(float((dH < 30).mean()), 3),
            'dh_30_90_share': round(float(((dH >= 30) & (dH < 90)).mean()), 3), 'dh_ge150_share': round(float((dH >= 150).mean()), 3),
            'dE_median': round(float(np.median(dE)), 1)}


two = [v for v in combos.values() if len(v) == 2]
wada2 = summarize([pair_stats(*v) for v in two])
# 3、4 色組：組內所有兩兩配對
multi_pairs = [pair_stats(a, b) for v in combos.values() if len(v) >= 3 for a, b in itertools.combinations(v, 2)]
wada_multi = summarize(multi_pairs)
# 3、4 色組：組內最大明度差
maxdL = [max(abs(ct.lab(a)[0] - ct.lab(b)[0]) for a, b in itertools.combinations(v, 2)) for v in combos.values() if len(v) >= 3]
# 基準：159 色任兩色全部配對
allhex = [c['hex'] for c in D]
base = summarize([pair_stats(a, b) for a, b in itertools.combinations(allhex, 2)])
# 基準：只從「有被用在兩色組」的顏色裡，依使用次數加權抽 20000 對
rng = np.random.default_rng(11)
used = [h for v in two for h in v]
bp = []
for _ in range(20000):
    a, b = rng.choice(used, 2, replace=False)
    if a != b: bp.append(pair_stats(a, b))
base_w = summarize(bp)
# 3 色以上組的「最大明度差」基準：隨機抽同樣大小的組
bm = []
for v in combos.values():
    if len(v) < 3: continue
    for _ in range(30):
        s = rng.choice(allhex, len(v), replace=False)
        bm.append(max(abs(ct.lab(a)[0] - ct.lab(b)[0]) for a, b in itertools.combinations(s, 2)))
# 每組有幾群色相（OKLCH 色相差 30° 內算一群；近灰不算）
def n_hues(v):
    hs = sorted(okh(h)[2] for h in v if okh(h)[1] >= 0.04)
    if not hs: return 0
    g = 1
    for x, y in zip(hs, hs[1:]):
        if y - x >= 30: g += 1
    if len(hs) > 1 and hs[0] + 360 - hs[-1] < 30 and g > 1: g -= 1
    return g
nh = Counter((len(v), n_hues(v)) for v in combos.values())
out = {'source': 'npm color-name-lists 3.34.0 lib/colors/sanzo-wada-I.json（來源標 sanzo-wada.dmbk.io）',
       'n_colours': len(D), 'n_combos': len(combos), 'combo_sizes': dict(sizes), 'hex_matches_naive_cmyk_conversion': f'{naive}/{len(D)}', 'hex_fixed': fixed,
       'wada_2colour': wada2, 'baseline_all_pairs_159': base, 'baseline_weighted_used_in_2colour': base_w,
       'wada_3plus_all_pairs': wada_multi,
       'wada_3plus_max_dL': {'n': len(maxdL), 'median': round(float(np.median(maxdL)), 1)},
       'baseline_3plus_max_dL_same_size_random': {'n': len(bm), 'median': round(float(np.median(bm)), 1)},
       'n_hues_by_size': {f'{k[0]}色組_{k[1]}群色相': v for k, v in sorted(nh.items())}}
json.dump(out, open('/tmp/claude-0/r2/theory/wada_stats.json', 'w'), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1))

# 抽樣檢定（10-19 修正）：每次重新依使用次數抽 123 對（兩色不同），兩個種子各 20000 次，看和田的數字落在哪裡。
# 原本是先抽一個固定 2 萬對的池再從池裡重抽，池本身的比例會帶進偏差（色相差 <30° 的池剛好偏低，p 變 0.128）。
U = sorted(set(used)); uidx = {h: i for i, h in enumerate(U)}
UL = np.array([ct.lab(h)[0] for h in U]); UO = np.array([okh(h) for h in U])
ui = np.array([uidx[h] for h in used])
wa = np.array([uidx[v[0]] for v in two]); wb = np.array([uidx[v[1]] for v in two])
def stats_idx(a, b):
    L = np.abs(UL[a] - UL[b]); ch = (UO[a, 1] >= 0.04) & (UO[b, 1] >= 0.04)
    d = np.abs(UO[a, 2] - UO[b, 2]) % 360; Hc = np.minimum(d, 360 - d)[ch]
    return np.array([np.median(L), (L < 10).mean(), (L >= 26).mean(), (Hc < 30).mean(), (Hc >= 150).mean(), np.median(Hc)])
def draw_pairs(rng, n):
    while True:
        a = ui[rng.integers(0, len(ui), 3 * n)]; b = ui[rng.integers(0, len(ui), 3 * n)]
        k = a != b
        if k.sum() >= n: return a[k][:n], b[k][:n]
obs = stats_idx(wa, wb)
SEEDS, NSIM = (11, 2027), 20000
names = ['dL_median', 'dL_lt10_share', 'dL_ge26_share', 'dh_lt30_share', 'dh_ge150_share', 'dh_median']
test = {n: {'wada': round(float(obs[i]), 3)} for i, n in enumerate(names)}
for sd in SEEDS:
    r2 = np.random.default_rng(sd)
    sims = np.array([stats_idx(*draw_pairs(r2, len(two))) for _ in range(NSIM)])
    for i, n in enumerate(names):
        lo = float((sims[:, i] <= obs[i]).mean()); hi = float((sims[:, i] >= obs[i]).mean())
        test[n][f'seed{sd}'] = {'sim_mean': round(float(sims[:, i].mean()), 3), 'sim_median': round(float(np.median(sims[:, i])), 3),
                                'two_sided_p': round(min(1.0, 2 * min(lo, hi)), 3)}
for n in names:
    ps = [test[n][f'seed{sd}']['two_sided_p'] for sd in SEEDS]
    test[n]['sim_median'] = test[n][f'seed{SEEDS[0]}']['sim_median']; test[n]['sim_mean'] = test[n][f'seed{SEEDS[0]}']['sim_mean']
    test[n]['two_sided_p'] = round(float(np.mean(ps)), 3); test[n]['p_range'] = [min(ps), max(ps)]
out.pop('test_vs_weighted_random_4000x123', None)
out['test_vs_weighted_random_fresh_123x20000x2seeds'] = test
# 檢定力參考：比例 0.17、n≈120 時的標準誤
nch = int((((UO[wa, 1] >= 0.04) & (UO[wb, 1] >= 0.04))).sum())
out['power_note'] = {'n_pairs': len(two), 'n_pairs_both_chromatic': nch, 'se_share_at_0.17': round(math.sqrt(0.17 * 0.83 / nch), 3),
                     'reading': '123 組（色相項只有 111 組兩色都有彩度）檢定力有限：色相差 <30° 和田 11.7% 對隨機約 17.7%，差 6 個百分點只約 1.7 個標準誤，p 約 0.09，在邊界；方向（同色相配對偏少）跟刻意拉開色相一致，但不顯著。不顯著不等於沒有差別。',
                     'pool_note': 'baseline_weighted_used_in_2colour 是一個固定 2 萬對的描述用池（色相差 <30° 0.172，剛好偏低）；檢定改用每次重新抽樣，不再從這個池重抽。'}
json.dump(out, open('/tmp/claude-0/r2/theory/wada_stats.json', 'w'), ensure_ascii=False, indent=1)
print(json.dumps(test, ensure_ascii=False))

# PCCS「同色調配色」檢驗：和田兩色組兩色同色調的比例，跟同一盒色加權隨機配對比。
# 色調用 pccs 0.2a3 公式；CMYK 直接換算會高估彩度，但隨機組用同一盒色，比較仍公平。
sys.path.insert(0, '/tmp/claude-0/r2/theory')
from systems_lib import munsell, munsell_to_pccs, PCCS_TONES, _t
tone_of, st_of = {}, {}
for c in D:
    m = munsell(c['hex'])
    if m['H'] is None or m['C'] < 1.0:
        tone_of[c['hex']] = 'N'; st_of[c['hex']] = None; continue
    p = munsell_to_pccs(m['H'], m['V'], m['C'])
    tone_of[c['hex']] = p['tone']; st_of[c['hex']] = (p['s'], _t(p['h'], p['l'], p['s']))
def tone_pair(a, b):
    same = tone_of[a] == tone_of[b]
    d = None if (st_of[a] is None or st_of[b] is None) else math.hypot(st_of[a][0] - st_of[b][0], st_of[a][1] - st_of[b][1])
    return same, d
w = [tone_pair(*v) for v in two]
wsame = np.mean([s for s, _ in w]); wd = np.median([d for _, d in w if d is not None])
Tu = [tone_pair(U[i], U[j]) for i in range(len(U)) for j in range(len(U))]  # 預先算好所有顏色對
SAME = np.array([t[0] for t in Tu]).reshape(len(U), len(U)); DIST = np.array([np.nan if t[1] is None else t[1] for t in Tu]).reshape(len(U), len(U))
sims_same, sims_d = [], []
for sd in SEEDS:
    r3 = np.random.default_rng(sd + 1)
    for _ in range(NSIM):
        a, b = draw_pairs(r3, len(two))
        sims_same.append(SAME[a, b].mean()); dd = DIST[a, b]; sims_d.append(np.median(dd[~np.isnan(dd)]))
sims_same, sims_d = np.array(sims_same), np.array(sims_d)
pv = lambda o, s: round(min(1.0, 2 * min((s <= o).mean(), (s >= o).mean())), 3)
out['pccs_same_tone_test'] = {'wada_same_tone_share': round(float(wsame), 3), 'random_same_tone_share_median': round(float(np.median(sims_same)), 3),
                              'p_same': pv(wsame, sims_same), 'wada_tone_distance_median': round(float(wd), 2),
                              'random_tone_distance_median': round(float(np.median(sims_d)), 2), 'p_dist': pv(wd, sims_d),
                              'palette_tone_counts': dict(Counter(tone_of.values()).most_common())}
json.dump(out, open('/tmp/claude-0/r2/theory/wada_stats.json', 'w'), ensure_ascii=False, indent=1)
print(json.dumps(out['pccs_same_tone_test'], ensure_ascii=False))
