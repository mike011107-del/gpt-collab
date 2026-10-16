"""基準檢查：名家與人氣配色「兩個有彩色＋其餘灰白」的比例，對照冷深色＋工程黃的組合。
用法：python3 grey_baseline.py
"""
import json, sys, os, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from colormath import oklch
from classify import is_yellow, is_cool, family
D = os.path.join(HERE, '..', '資料', '原始')
NEUT = {'白／米白', '淺灰', '中灰', '炭黑'}
wc = json.load(open(os.path.join(D, 'wada_colors.json')))
combos = collections.defaultdict(list)
for c in wc:
    for cid in c['combinations']:
        combos[cid].append(c['hex'].upper())
wada = list(combos.values())
cl = [[h.upper() for h in p] for p in json.load(open(os.path.join(D, 'colourlovers_1000.json')))]

def neutral(h): return family(h) in NEUT if not (is_cool(h) or is_yellow(h)) else False

for name, pals in [('wada', wada), ('colourlovers', cl)]:
    by = collections.defaultdict(lambda: [0, 0, 0, 0])  # size -> [all, all_rest_neutral, hits, hits_rest_neutral]
    for p in pals:
        n = len(p)
        chrom = [h for h in p if not neutral(h)]
        by[n][0] += 1
        # baseline: 有 >=2 個有彩色時，「除了兩個有彩色，其餘全是灰白」
        if len(chrom) <= 2: by[n][1] += 1
        cools = [h for h in p if is_cool(h)]; ys = [h for h in p if is_yellow(h)]
        if cools and ys:
            by[n][2] += 1
            others = [h for h in p if h not in cools and h not in ys]
            if all(family(h) in NEUT for h in others): by[n][3] += 1
    print('==', name)
    ta = sum(v[0] for v in by.values()); tb = sum(v[1] for v in by.values())
    th = sum(v[2] for v in by.values()); tn = sum(v[3] for v in by.values())
    for n in sorted(by):
        a, b, h, hn = by[n]
        print(f' {n} 色：全部 {a} 組裡 {b} 組最多兩個有彩色（{b/a:.0%}）；冷深＋黃 {h} 組裡 {hn} 組其餘只有灰白或沒有（{(hn/h if h else 0):.0%}）')
    # 基準限定：至少兩個有彩色的配色
    a2 = sum(1 for p in pals if len([h for h in p if not neutral(h)]) >= 2)
    b2 = sum(1 for p in pals if len([h for h in p if not neutral(h)]) == 2)
    print(f' 合計：全部 {tb}/{ta}={tb/ta:.0%}；有兩個以上有彩色的 {a2} 組裡恰好兩個 {b2}={b2/a2:.0%}；冷深＋黃 {tn}/{th}={tn/th:.0%}')
