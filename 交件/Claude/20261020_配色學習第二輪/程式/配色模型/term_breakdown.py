# 兩色偏好三項（明度差、色相差、冷度和）在同業實際配對、同業打亂、隨機之間的中位數比較 → data/term_breakdown.json
import json, sys, itertools
import numpy as np
sys.path.insert(0, '/tmp/claude-0/r2/models')
import models_lib as M
CG = M.Colorgorical('/tmp/claude-0/r2/models/data/colorgorical_tables.npz')
peers = json.load(open('/tmp/claude-0/work/peer_schemes.json'))
def parts(a, b):
    g1, _ = CG.snap(M.lab_from_hex(a)); g2, _ = CG.snap(M.lab_from_hex(b))
    pp, p = CG.pair_preference(g1, g2, parts=True)
    return p if p['path'] == 'chromatic' else None
actual = [parts(a, b) for p in peers if len(p['cols']) >= 2 for a, b in itertools.combinations(p['cols'], 2)]
pool = [(p['name'], c) for p in peers for c in p['cols']]
shuf = [parts(a[1], b[1]) for a, b in itertools.combinations(pool, 2) if a[0] != b[0]]
rng = np.random.default_rng(20261019 + 1)
rnd = []
for _ in range(5000):
    a = '#%02X%02X%02X' % tuple(rng.integers(0, 256, 3)); b = '#%02X%02X%02X' % tuple(rng.integers(0, 256, 3))
    rnd.append(parts(a, b))
out = {}
for name, L in [('peer_actual', actual), ('peer_shuffled', shuf), ('random_sRGB', rnd)]:
    L = [x for x in L if x]
    out[name] = dict(n=len(L), **{k: round(float(np.median([x[k] for x in L])), 2) for k in ['term_lightness', 'term_hue', 'term_coolness', 'dH_illC', 'dL_illC']},
                     median_coolness_sum=round(float(np.median([sum(x['coolness']) for x in L])), 2))
json.dump(out, open('/tmp/claude-0/r2/models/data/term_breakdown.json', 'w'), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False))
