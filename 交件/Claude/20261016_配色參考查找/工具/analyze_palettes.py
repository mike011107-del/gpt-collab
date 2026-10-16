"""從兩個開源配色資料庫篩出「冷深色＋工程黃」的組合，統計第三色。
用法：python3 analyze_palettes.py   （讀 ../資料/原始/，寫 ../資料/冷深色加黃_名家與人氣配色.json）
"""
import json, sys, os, collections, statistics
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from colormath import oklch, contrast as cr
from classify import is_yellow, is_cool, cool_sub, family

HERE = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(HERE, '..', '資料', '原始')
out = os.path.join(HERE, '..', '資料', '冷深色加黃_名家與人氣配色.json')

# 和田三造《配色事典》348 組（2–4 色）
wada_colors = json.load(open(os.path.join(data_dir, 'wada_colors.json')))
combos = collections.defaultdict(list)
for c in wada_colors:
    for cid in c['combinations']:
        combos[cid].append({'hex': c['hex'].upper(), 'name': c['name']})
wada = [{'src': 'wada', 'id': k, 'colors': v} for k, v in sorted(combos.items())]

# COLOURlovers 人氣前 1000（實收 992 組，每組 5 色）
cl = json.load(open(os.path.join(data_dir, 'colourlovers_1000.json')))
cl = [{'src': 'colourlovers', 'id': i + 1, 'colors': [{'hex': h.upper()} for h in p]} for i, p in enumerate(cl)]


def analyse(pals, label):
    hits = []
    for p in pals:
        hexes = [c['hex'] for c in p['colors']]
        cools = [h for h in hexes if is_cool(h)]
        ys = [h for h in hexes if is_yellow(h)]
        if not cools or not ys:
            continue
        others = [h for h in hexes if h not in cools and h not in ys]
        fam = [family(h) for h in others]
        # 主冷色取最深的那個
        cool = min(cools, key=lambda h: oklch(h)[0])
        y = max(ys, key=lambda h: oklch(h)[1])
        Lc, Cc, Hc = oklch(cool)
        Ly, Cy, Hy = oklch(y)
        hits.append({**p, 'cool': cool, 'cool_sub': cool_sub(cool), 'yellow': y,
                     'others': others, 'other_families': fam,
                     'cool_L': round(Lc, 3), 'cool_C': round(Cc, 3), 'cool_H': round(Hc, 1),
                     'y_L': round(Ly, 3), 'y_C': round(Cy, 3), 'y_H': round(Hy, 1),
                     'contrast_cool_yellow': round(cr(cool, y), 2)})
    famc = collections.Counter()
    for h in hits:
        for f in set(h['other_families']):
            famc[f] += 1
    subc = collections.Counter(h['cool_sub'] for h in hits)
    def med(k):
        v = [h[k] for h in hits]
        return round(statistics.median(v), 3) if v else None
    def q(k):
        v = sorted(h[k] for h in hits)
        if len(v) < 4: return None
        n = len(v)
        return [round(v[n // 4], 3), round(v[(3 * n) // 4], 3)]
    # 基準：整個資料庫裡的冷深色（不論有沒有黃）
    allcool = [h for p in pals for h in [c['hex'] for c in p['colors']] if is_cool(h)]
    base_C = round(statistics.median([oklch(h)[1] for h in allcool]), 3) if allcool else None
    groups = {'暖紅系（紅、珊瑚、紅褐、橘、棕、粉）': {'紅', '珊瑚／橘紅', '紅褐', '橘', '棕／赭', '粉'},
              '淺中性（白、米白、淺灰、米黃）': {'白／米白', '淺灰', '淺黃／米黃'},
              '深中性（炭黑、中灰）': {'炭黑', '中灰'},
              '黃綠／橄欖': {'黃綠／橄欖'}}
    share = {g: f"{sum(1 for h in hits if fs & set(h['other_families']))}/{len(hits)}" for g, fs in groups.items()}
    return {
        'source': label, 'third_group_share': share, 'total': len(pals), 'hits': len(hits),
        'cool_subfamily': subc.most_common(),
        'third_family_palettes': famc.most_common(),
        'no_third': sum(1 for h in hits if not h['others']),
        'median': {k: med(k) for k in ['cool_L', 'cool_C', 'cool_H', 'y_L', 'y_C', 'y_H', 'contrast_cool_yellow']},
        'iqr': {k: q(k) for k in ['cool_L', 'cool_C', 'y_H', 'contrast_cool_yellow']},
        'baseline_all_cool_dark_median_C': base_C,
        'palettes': hits,
    }

res = {'wada': analyse(wada, '和田三造《配色事典》（npm dictionary-of-colour-combinations 1.0.2，MIT）'),
       'colourlovers': analyse(cl, 'COLOURlovers 人氣前 1000（npm nice-color-palettes 4.0.0，MIT；原作者 2018-10-14 擷取）')}
json.dump(res, open(out, 'w'), ensure_ascii=False, indent=1)
for k, r in res.items():
    print('==', k, r['hits'], '/', r['total'], 'no_third', r['no_third'])
    print(' cool sub', r['cool_subfamily'])
    print(' groups', r['third_group_share'])
    print(' third', r['third_family_palettes'])
    print(' median', r['median'], 'iqr', r['iqr'], 'baseline C', r['baseline_all_cool_dark_median_C'])
