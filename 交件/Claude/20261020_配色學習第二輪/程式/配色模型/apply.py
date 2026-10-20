# 套用：單色、兩色、基準。只算事實，不評好壞。輸出 data/apply.json 與畫圖資料 data/fig_*.json
import json, math, sys, itertools
import numpy as np
sys.path.insert(0, '/tmp/claude-0/r2/models')
import models_lib as M

SEED = 20261019
CG = M.Colorgorical('/tmp/claude-0/r2/models/data/colorgorical_tables.npz')
TERMS = json.load(open('/tmp/claude-0/src/c3/data/xkcd/c3_data.json'))['terms']
peers = json.load(open('/tmp/claude-0/work/peer_schemes.json'))

TARGETS = {'深青': '#0C424A', '靛藍': '#333D66', '工程黃': '#D68702', '白': '#FFFFFF'}


def r(x, n=3):
    return None if x is None or (isinstance(x, float) and math.isnan(x)) else round(float(x), n)


def single(hx):
    lab = M.lab_from_hex(hx)
    L, C, h = M.lch(lab)
    hh, hc, ht = M.hct_from_hex(hx)
    g, sd = CG.snap(lab)
    achrom = (g[1] == 0 and g[2] == 0)
    d = dict(hex=hx, L=r(L, 2), C=r(C, 2), h=r(h, 1),
             ou_warm_cool=r(M.ou_warm_cool(lab)),
             hct=[r(hh, 1), r(hc, 1), r(ht, 1)], mcu_disliked=bool(M.mcu_is_disliked(hx)),
             cg_grid=list(g), cg_snap_dist=r(sd, 2), cg_achromatic=achrom,
             cg_coolness=None if achrom else r(CG.coolness(g), 2),
             cg_name_uniqueness=r(CG.name_uniqueness(g)),
             cg_top_terms=CG.top_terms(g, TERMS, 3),
             cg_penalty=CG.penalty(g), cg_ugly_filtered=bool(CG.is_ugly_filtered(g)))
    return d


def pair(h1, h2):
    l1 = M.lab_from_hex(h1); l2 = M.lab_from_hex(h2)
    g1, _ = CG.snap(l1); g2, _ = CG.snap(l2)
    pp, parts = CG.pair_preference(g1, g2, parts=True)
    ppw = CG.pair_preference(g1, g2, wrap_hue=True)
    de = M.ciede2000(l1, l2)
    return dict(a=h1, b=h2, dE2000=r(de, 2), dL=r(abs(l1[0] - l2[0]), 2),
                pp_code=r(pp, 2), pp_wrapped=r(ppw, 2), pp_norm_code=r(CG.pp_norm(pp)),
                pp_parts=parts, name_diff=r(CG.name_difference(g1, g2)),
                de_norm=r(CG.de_norm(de)),
                wc_a=r(M.ou_warm_cool(l1)), wc_b=r(M.ou_warm_cool(l2)))


def stats(vals):
    v = np.array([x for x in vals if x is not None and not (isinstance(x, float) and math.isnan(x))], float)
    if v.size == 0:
        return dict(n=0)
    q1, med, q3 = np.percentile(v, [25, 50, 75])
    return dict(n=int(v.size), median=r(med, 3), q1=r(q1, 3), q3=r(q3, 3), min=r(v.min(), 3), max=r(v.max(), 3))


def pct_rank(x, vals):
    v = np.array([y for y in vals if y is not None], float)
    if x is None or v.size == 0:
        return None
    return r(100.0 * ((v < x).sum() + 0.5 * (v == x).sum()) / v.size, 1)


out = {'seed': SEED}

# ---------------- 單色 ----------------
out['targets_single'] = {k: single(v) for k, v in TARGETS.items()}
peer_main = []
peer_allcol = []
for p in peers:
    if p['cols']:
        s = single(p['cols'][0]); s['name'] = p['name']; s['group'] = p['t']
        peer_main.append(s)
        for c in p['cols']:
            t = single(c); t['name'] = p['name']; t['group'] = p['t']
            peer_allcol.append(t)
out['peer_main_single'] = peer_main
keys = ['ou_warm_cool', 'L', 'C', 'cg_coolness', 'cg_name_uniqueness']
out['peer_main_stats'] = {k: stats([s[k] for s in peer_main]) for k in keys}
out['peer_allcol_stats'] = {k: stats([s[k] for s in peer_allcol]) for k in keys}
out['peer_counts'] = dict(n_peers=len(peers), n_with_colour=len(peer_main), n_all_chromatic_cols=len(peer_allcol),
                          main_warm=sum(1 for s in peer_main if s['ou_warm_cool'] > 0),
                          main_cool=sum(1 for s in peer_main if s['ou_warm_cool'] < 0),
                          main_mcu_disliked=[s['name'] for s in peer_main if s['mcu_disliked']],
                          allcol_mcu_disliked=[(s['name'], s['hex']) for s in peer_allcol if s['mcu_disliked']],
                          main_cg_penalised=[(s['name'], s['hex'], s['cg_penalty']) for s in peer_main if s['cg_penalty'] < 1],
                          allcol_cg_penalised=[(s['name'], s['hex'], s['cg_penalty']) for s in peer_allcol if s['cg_penalty'] < 1])
out['targets_pct_in_peer_main'] = {k: {m: pct_rank(out['targets_single'][k][m], [s[m] for s in peer_main]) for m in keys}
                                   for k in ['深青', '靛藍', '工程黃']}

# 隨機單色基準（均勻 sRGB）
rng = np.random.default_rng(SEED)
rand_cols = ['#%02X%02X%02X' % tuple(rng.integers(0, 256, 3)) for _ in range(3000)]
rs = [single(h) for h in rand_cols]
out['random_single_stats'] = {k: stats([s[k] for s in rs]) for k in keys}
out['random_single_stats']['share_warm'] = r(sum(1 for s in rs if s['ou_warm_cool'] > 0) / len(rs), 3)
out['random_single_stats']['share_mcu_disliked'] = r(sum(1 for s in rs if s['mcu_disliked']) / len(rs), 3)
out['random_single_stats']['share_cg_penalised'] = r(sum(1 for s in rs if s['cg_penalty'] < 1) / len(rs), 3)

# ---------------- 兩色 ----------------
tp = {'深青×工程黃': ('#0C424A', '#D68702'), '靛藍×工程黃': ('#333D66', '#D68702'),
      '深青×白': ('#0C424A', '#FFFFFF'), '靛藍×白': ('#333D66', '#FFFFFF'), '工程黃×白': ('#D68702', '#FFFFFF')}
out['targets_pair'] = {k: pair(*v) for k, v in tp.items()}

# 同業多色 logo 的實際配對（同一家 logo 裡的彩色兩兩配）
peer_pairs = []
for p in peers:
    if len(p['cols']) >= 2:
        for a, b in itertools.combinations(p['cols'], 2):
            d = pair(a, b); d['name'] = p['name']; d['group'] = p['t']
            peer_pairs.append(d)
out['peer_pairs'] = peer_pairs

# 同業主色 × 白
peer_white = []
for s in peer_main:
    d = pair(s['hex'], '#FFFFFF'); d['name'] = s['name']
    peer_white.append(d)
out['peer_main_x_white'] = peer_white

# 同業彩色打亂重配（不同家之間的所有配對，不用亂數）
pool = [(p['name'], c) for p in peers for c in p['cols']]
shuf = [pair(a[1], b[1]) for a, b in itertools.combinations(pool, 2) if a[0] != b[0]]

# 隨機兩色（均勻 sRGB，5000 組）與隨機色 × 白（2000）
rng2 = np.random.default_rng(SEED + 1)
rp = []
for _ in range(5000):
    a = '#%02X%02X%02X' % tuple(rng2.integers(0, 256, 3)); b = '#%02X%02X%02X' % tuple(rng2.integers(0, 256, 3))
    rp.append(pair(a, b))
rng3 = np.random.default_rng(SEED + 2)
rw = [pair('#%02X%02X%02X' % tuple(rng3.integers(0, 256, 3)), '#FFFFFF') for _ in range(2000)]

pk = ['dE2000', 'dL', 'pp_code', 'pp_wrapped', 'name_diff']
out['baseline_pair_stats'] = dict(
    random_sRGB_5000={k: stats([d[k] for d in rp]) for k in pk},
    peer_shuffled={k: stats([d[k] for d in shuf]) for k in pk},
    peer_actual_pairs={k: stats([d[k] for d in peer_pairs]) for k in pk},
    random_x_white_2000={k: stats([d[k] for d in rw]) for k in pk},
    peer_main_x_white={k: stats([d[k] for d in peer_white]) for k in pk})
out['baseline_pair_stats']['random_sRGB_5000']['pp_nan_count'] = sum(1 for d in rp if d['pp_code'] is None)
out['baseline_pair_stats']['random_x_white_2000']['pp_nan_count'] = sum(1 for d in rw if d['pp_code'] is None)
out['baseline_pair_stats']['peer_shuffled']['n_pairs'] = len(shuf)
# 色相差超過 180（程式原樣與取補角結果不同）的比例
out['hue_wrap_share'] = dict(
    random=r(sum(1 for d in rp if d['pp_parts'].get('dH_illC', 0) > 180) / len(rp), 3),
    peer_actual=r(sum(1 for d in peer_pairs if d['pp_parts'].get('dH_illC', 0) > 180) / len(peer_pairs), 3))

# 目標配對在各基準中的百分位
pct = {}
for k, d in out['targets_pair'].items():
    base = rw if '白' in k else rp
    pb = peer_white if '白' in k else peer_pairs
    pct[k] = {m: dict(vs_random=pct_rank(d[m], [x[m] for x in base]), vs_peer=pct_rank(d[m], [x[m] for x in pb]))
              for m in pk}
    if '白' not in k:
        for m in pk:
            pct[k][m]['vs_peer_shuffled'] = pct_rank(d[m], [x[m] for x in shuf])
out['targets_pair_percentiles'] = pct

# 各指標之間的相關（隨機 5000 組），看分數彼此是否重疊
arr = np.array([[d['dE2000'], d['dL'], d['pp_code'], d['name_diff']] for d in rp if d['pp_code'] is not None], float)
cm = np.corrcoef(arr.T)
out['random_corr'] = dict(order=['dE2000', 'dL', 'pp_code', 'name_diff'], matrix=[[r(x, 3) for x in row] for row in cm])

json.dump(out, open('/tmp/claude-0/r2/models/data/apply.json', 'w'), ensure_ascii=False, indent=1)

# ---------- 畫圖資料 ----------
fig1 = dict(desc='單色位置：x=Ou 冷暖（>0 暖），y=L*；同業主色 + 目標色',
            points=[dict(name=s['name'], group=s['group'], hex=s['hex'], x=s['ou_warm_cool'], y=s['L'],
                         coolness=s['cg_coolness'], nu=s['cg_name_uniqueness']) for s in peer_main]
            + [dict(name=k, group='崧淳候選／已定', hex=v['hex'], x=v['ou_warm_cool'], y=v['L'],
                    coolness=v['cg_coolness'], nu=v['cg_name_uniqueness']) for k, v in out['targets_single'].items()])
json.dump(fig1, open('/tmp/claude-0/r2/models/data/fig_single_wc_L.json', 'w'), ensure_ascii=False, indent=1)
rs_sample = rp[:800]
fig2 = dict(desc='兩色：x=明度差 ΔL*，y=Colorgorical 兩色偏好（程式原樣）；隨機取前 800 組、同業實際配對、目標配對',
            random=[dict(a=d['a'], b=d['b'], x=d['dL'], y=d['pp_code'], nd=d['name_diff'], de=d['dE2000']) for d in rs_sample],
            peer=[dict(name=d['name'], a=d['a'], b=d['b'], x=d['dL'], y=d['pp_code'], y_wrapped=d['pp_wrapped'], nd=d['name_diff'], de=d['dE2000']) for d in peer_pairs],
            targets=[dict(name=k, a=d['a'], b=d['b'], x=d['dL'], y=d['pp_code'], y_wrapped=d['pp_wrapped'], nd=d['name_diff'], de=d['dE2000']) for k, d in out['targets_pair'].items()])
json.dump(fig2, open('/tmp/claude-0/r2/models/data/fig_pair_dL_pp.json', 'w'), ensure_ascii=False, indent=1)
print(json.dumps({k: out[k] for k in ['targets_single', 'peer_main_stats', 'peer_counts', 'targets_pct_in_peer_main', 'random_single_stats']}, ensure_ascii=False)[:6000])
