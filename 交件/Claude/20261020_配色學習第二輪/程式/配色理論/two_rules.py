# Color Nerd「兩條規則」練習（不要兩色同彩度、不要等距色相）拿來檢查同業：多色 logo 裡兩個彩色的彩度差，跟同業顏色打亂重配比
import sys, json, itertools
sys.path.insert(0, '/home/user/gpt-collab/.claude/skills/colour-tool/scripts')
import numpy as np
import colourtool as ct
peers = json.load(open('/tmp/claude-0/work/peer_schemes.json'))
C = lambda h: ct.lch(h)[1]
real, pool = [], []
for p in peers:
    cs = [c for c in p['cols'] if ct.oklch(c)[1] >= 0.04]
    pool += cs
    for a, b in itertools.combinations(cs, 2):
        real.append(abs(C(a) - C(b)))
rng = np.random.default_rng(9)
sims = []
for _ in range(4000):
    idx = rng.integers(0, len(pool), (len(real), 2))
    d = np.array([abs(C(pool[i]) - C(pool[j])) for i, j in idx if pool[i] != pool[j]])
    sims.append(((d < 5).mean(), np.median(d)))
sims = np.array(sims); real = np.array(real)
out = {'n_pairs_within_logo': len(real), 'share_dC_lt5_real': round(float((real < 5).mean()), 3), 'share_dC_lt5_shuffled_median': round(float(np.median(sims[:, 0])), 3),
       'p_share_lower': round(float((sims[:, 0] <= (real < 5).mean()).mean()), 3),
       'median_dC_real': round(float(np.median(real)), 1), 'median_dC_shuffled': round(float(np.median(sims[:, 1])), 1),
       'note': 'C* 用 CIELAB；「同彩度」定義為 C* 差 < 5（自訂）。打亂：同業全部彩色隨機兩兩配，配對數同真實。'}
json.dump(out, open('/tmp/claude-0/r2/theory/two_rules.json', 'w'), ensure_ascii=False, indent=1)
print(out)
