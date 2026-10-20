# 用 48 家國外同業 logo 的實際顏色，挑出能代表 Itten 七種對比的組合（只用已存在的同業色）。
# 判斷用我自訂的可量化條件（寫在 criteria），不是 Itten 原書的定義；Itten 原書沒有數字門檻。
import sys, json, math, itertools
sys.path.insert(0, '/home/user/gpt-collab/.claude/skills/colour-tool/scripts')
import colourtool as ct

peers = json.load(open('/tmp/claude-0/work/peer_schemes.json'))
CHROMA_MIN = 0.04  # OKLCH C 低於此視為無彩


def info(h):
    L, C, H = ct.oklch(h); lab = ct.lab(h)
    return {'hex': h.upper(), 'L': round(lab[0], 1), 'C': round(math.hypot(lab[1], lab[2]), 1), 'okC': round(C, 3), 'okh': round(H, 1), 'chromatic': C >= CHROMA_MIN}


def dh(a, b):
    d = abs(a - b) % 360
    return min(d, 360 - d)


def warmth(h):  # 自訂：OKLCH 色相 0–110 或 340 以上算暖（紅橘黃），160–290 算冷（綠青藍）
    if h < 110 or h >= 340: return 'warm'
    if 160 <= h < 290: return 'cool'
    return 'mid'


pairs = []
for p in peers:
    cs = [info(c) for c in p['cols']] + [dict(info(c), neutral_listed=True) for c in p['neutral']]
    for a, b in itertools.combinations(cs, 2):
        both = a['chromatic'] and b['chromatic']
        pairs.append({'peer': p['name'], 'a': a, 'b': b, 'both_chromatic': both,
                      'dh': round(dh(a['okh'], b['okh']), 1) if both else None,
                      'dL': round(abs(a['L'] - b['L']), 1), 'dC': round(abs(a['C'] - b['C']), 1),
                      'dE2000': round(ct.de(a['hex'], b['hex']), 1),
                      'warm_cool': sorted([warmth(a['okh']) if a['chromatic'] else 'neutral', warmth(b['okh']) if b['chromatic'] else 'neutral'])})

res = {'criteria': {}, 'examples': {}}
# 1 色相對比：同一個 logo 裡不同色相的數目（色相相差 30° 以內併成一群）
hue_counts = []
for p in peers:
    hs = sorted(info(c)['okh'] for c in p['cols'] if info(c)['chromatic'])
    if not hs: continue
    groups = 1
    for x, y in zip(hs, hs[1:]):
        if y - x >= 30: groups += 1
    if len(hs) > 1 and (hs[0] + 360 - hs[-1]) < 30 and groups > 1: groups -= 1
    hue_counts.append({'peer': p['name'], 'n_hues': groups, 'cols': p['cols'], 'okh': hs})
hue_counts.sort(key=lambda r: -r['n_hues'])
res['criteria']['色相對比'] = '一個 logo 裡有幾群色相（OKLCH 色相差 30° 以內算同一群）；取群數最多的'
res['examples']['色相對比'] = hue_counts[:4]
# 2 明暗對比：同色相（dh<30）或一邊無彩，取 L* 差最大
c2 = [x for x in pairs if (x['both_chromatic'] and x['dh'] < 30)]
c2.sort(key=lambda x: -x['dL'])
res['criteria']['明暗對比'] = '兩色色相差 < 30°（同一色相只差深淺），取 L* 差最大'
res['examples']['明暗對比'] = c2[:4]
# 3 冷暖對比：一暖一冷，L* 差越小越純（只剩冷暖在對比）
c3 = [x for x in pairs if x['warm_cool'] == ['cool', 'warm']]
c3.sort(key=lambda x: x['dL'])
res['criteria']['冷暖對比'] = '一色 OKLCH 色相 0–110° 或 ≥340°（暖），一色 160–290°（冷）；取 L* 差最小（只剩冷暖在對比）'
res['examples']['冷暖對比'] = c3[:4]
res['examples']['冷暖對比_同時明暗差大'] = sorted(c3, key=lambda x: -x['dL'])[:3]
# 4 補色對比：色相差最接近 180°，兩色都夠鮮（OKLCH C ≥ 0.08）
c4 = [x for x in pairs if x['both_chromatic'] and x['a']['okC'] >= 0.08 and x['b']['okC'] >= 0.08]
c4.sort(key=lambda x: abs(180 - x['dh']))
res['criteria']['補色對比'] = '兩色 OKLCH C 都 ≥ 0.08，色相差最接近 180°'
res['examples']['補色對比'] = c4[:4]
# 5 彩度對比：同色相或一邊無彩、L* 差 < 8，取 C* 差最大
c5 = [x for x in pairs if x['dL'] < 8 and ((x['both_chromatic'] and x['dh'] < 30) or not x['both_chromatic'])]
c5.sort(key=lambda x: -x['dC'])
res['criteria']['彩度對比'] = '同色相（差 < 30°）或一邊是灰，L* 差 < 8（不靠明暗），取 C* 差最大'
res['examples']['彩度對比'] = c5[:4]
# 跨公司的彩度對比（同 logo 內不夠時）：同業任兩色，同色相、L* 差 < 5、C* 差最大
allc = [(p['name'], info(c)) for p in peers for c in p['cols']]
cross = []
for (n1, a), (n2, b) in itertools.combinations(allc, 2):
    if n1 == n2 or not (a['chromatic'] and b['chromatic']): continue
    if dh(a['okh'], b['okh']) < 15 and abs(a['L'] - b['L']) < 5:
        cross.append({'peers': [n1, n2], 'a': a, 'b': b, 'dC': round(abs(a['C'] - b['C']), 1), 'dL': round(abs(a['L'] - b['L']), 1), 'dh': round(dh(a['okh'], b['okh']), 1)})
cross.sort(key=lambda x: -x['dC'])
res['examples']['彩度對比_跨公司'] = cross[:3]
# 6 同時對比（示意，非實際用法）：同業 logo 裡的中灰，放在兩個明度接近灰、色相相反的同業主色上
grays = [(p['name'], info(c)) for p in peers for c in p['neutral'] if 35 <= info(c)['L'] <= 70]
mains = [(p['name'], info(p['cols'][0])) for p in peers if p['cols']]
best = None
for gn, g in grays:
    cand = [(n, m) for n, m in mains if abs(m['L'] - g['L']) < 12 and m['okC'] >= 0.08]
    for (n1, a), (n2, b) in itertools.combinations(cand, 2):
        score = dh(a['okh'], b['okh'])
        if best is None or score > best[0]:
            best = (score, gn, g, n1, a, n2, b)
s, gn, g, n1, a, n2, b = best
res['criteria']['同時對比'] = '示意：取同業 logo 裡的一個中灰，放在兩個跟灰明度相近（L* 差 < 12）、色相差最大的同業主色上；理論預測灰會往底色的補色方向偏'
res['examples']['同時對比'] = {'gray_from': gn, 'gray': g, 'bg1_from': n1, 'bg1': a, 'bg2_from': n2, 'bg2': b, 'bg_dh': round(s, 1),
                               'predicted_tint_on_bg1_okh': round((a['okh'] + 180) % 360, 1), 'predicted_tint_on_bg2_okh': round((b['okh'] + 180) % 360, 1)}
res['criteria']['面積對比'] = '同業資料沒有各色面積，不能挑；見 area_balance.json 的公式示意'
json.dump(res, open('/tmp/claude-0/r2/theory/itten_examples.json', 'w'), ensure_ascii=False, indent=1)


def short(x):
    if 'peer' in x and 'a' in x:
        return f"{x['peer']}: {x['a']['hex']}(L{x['a']['L']},C{x['a']['C']},h{x['a']['okh']}) + {x['b']['hex']}(L{x['b']['L']},C{x['b']['C']},h{x['b']['okh']}) dh={x['dh']} dL={x['dL']} dC={x['dC']} dE={x['dE2000']}"
    return str(x)[:300]


for k, v in res['examples'].items():
    print('==', k)
    for x in (v if isinstance(v, list) else [v]):
        print('  ', short(x))
