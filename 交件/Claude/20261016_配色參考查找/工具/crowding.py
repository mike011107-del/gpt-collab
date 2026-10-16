"""全球品牌主色在冷色區的擁擠度（simple-icons 16.35.0，3466 個品牌，CC0）。
格子：OKLCH 色相每 15° 一格（140°–275°，綠到藍），明度每 0.1 一格；只算彩度 ≥0.03 的顏色。
另把台灣同業 14 家的 logo／網站色放進同一張表，方便對照。
用法：python3 crowding.py   → ../資料/全球品牌冷色擁擠度.json
限制：simple-icons 以科技、媒體、交通品牌為主，工程與水務品牌很少；這是「大眾看過的品牌」的粗略分布，不是同業分布。
"""
import json, os, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from colormath import oklch

HUES = list(range(140, 275, 15))  # 每格起點
LS = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7]


def cell(h):
    L, C, H = oklch(h)
    if C < 0.03 or not (140 <= H < 275) or not (0.2 <= L < 0.8): return None
    return (int((H - 140) // 15) * 15 + 140, round(int(L * 10) / 10, 1))


def main():
    si = json.load(open(os.path.join(HERE, '..', '資料', '原始', 'simple_icons_16.35.0_title_hex.json')))
    refs = json.load(open(os.path.join(HERE, '參照庫.json')))
    g = collections.defaultdict(list); tw = collections.defaultdict(list)
    for b in si:
        c = cell(b['hex'])
        if c: g[c].append(b['title'])
    for b in refs['brands']:
        if b['group'] == '台灣同業':
            c = cell(b['hex'])
            if c and b['name'] not in tw[c]: tw[c].append(b['name'])
    grid = []
    for L in LS:
        for Hs in HUES:
            k = (Hs, L)
            grid.append({'hue_from': Hs, 'hue_to': Hs + 15, 'L_from': L, 'L_to': round(L + 0.1, 1),
                         'global_count': len(g[k]), 'global_examples': g[k][:8], 'taiwan_peers': tw[k]})
    out = {'source': 'simple-icons 16.35.0（npm，CC0），品牌數 %d' % len(si), 'grid': grid,
           'note': '色相 140–175 綠、175–200 青綠、200–230 青、230–275 藍；明度 L 是 OKLCH（0 黑、1 白）。'}
    json.dump(out, open(os.path.join(HERE, '..', '資料', '全球品牌冷色擁擠度.json'), 'w'), ensure_ascii=False, indent=1)
    print('L\\H ' + ' '.join(f'{h:>4}' for h in HUES))
    for L in LS:
        print(f'{L:.1f} ' + ' '.join(f"{len(g[(h, L)]):4d}" for h in HUES))


if __name__ == '__main__':
    main()
