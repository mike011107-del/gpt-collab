"""配色比對：輸入一組顏色，查它跟同業、街頭、全球品牌、名家與人氣配色的距離，並算對比、灰階、色弱。
用法：
  python3 palette_check.py "#主色" "#工程黃" "#第三色" [更多色] [--name 名稱] [--json 輸出.json] [--html 輸出.html]
順序約定：第 1 色＝主色，第 2 色＝工程黃，其餘＝第三色或中性色。
只用標準函式庫。先跑過 build_refs.py 產生 參照庫.json。
距離用 CIEDE2000（ΔE00）。經驗值：<5 幾乎同色、5–10 很像、10–20 同一家族、>20 明顯不同。這是螢幕色，不代表烤漆或印刷。
"""
import json, os, sys, collections, html as H
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from colormath import oklch, de, contrast, cvd, gray, lum, selftest
from classify import is_cool, is_yellow, family, cool_sub

ROLE = lambda i: '主色' if i == 0 else ('工程黃' if i == 1 else f'第{i + 1}色')


def load():
    return json.load(open(os.path.join(HERE, '參照庫.json')))


def nearest(h, items, k=3):
    return sorted(((de(h, it['hex']), it) for it in items), key=lambda x: x[0])[:k]


def palette_dist(inp, pal):
    """輸入每一色到該配色最近一色的 ΔE00 平均（看「這組裡有沒有我的每一色」）。"""
    return sum(min(de(h, p) for p in pal) for h in inp) / len(inp)


def check(cols, refs, name=''):
    out = {'name': name, 'colors': [], 'pairs': [], 'neighbours': {}, 'structure': {}}
    groups = collections.defaultdict(list)
    for b in refs['brands']:
        groups[b['group']].append(b)
    for i, h in enumerate(cols):
        L, C, Hh = oklch(h)
        row = {'role': ROLE(i), 'hex': h, 'oklch': [round(L, 3), round(C, 3), round(Hh, 1)],
               'family': ('冷深色·' + cool_sub(h)) if is_cool(h) else ('工程黃' if is_yellow(h) else family(h)),
               'near': {}}
        for g, items in groups.items():
            row['near'][g] = [{'name': it['name'], 'hex': it['hex'], 'de': round(d, 1), 'grade': it['grade']} for d, it in nearest(h, items, 2)]
        gl = [(de(h, b['hex']), b) for b in refs['global']]
        close = sorted([x for x in gl if x[0] < 8], key=lambda x: x[0])
        row['global_within_8'] = len(close)
        row['global_examples'] = [{'name': b['name'], 'hex': b['hex'], 'de': round(d, 1)} for d, b in close[:6]]
        out['colors'].append(row)
    # 名家／人氣近親
    for src in ('和田三造《配色事典》', 'COLOURlovers 人氣'):
        pals = [p for p in refs['palettes'] if p['src'] == src]
        best = sorted(((palette_dist(cols, p['colors']), p) for p in pals), key=lambda x: x[0])[:5]
        out['neighbours'][src] = [{'id': p['id'], 'colors': p['colors'], 'avg_de': round(d, 1)} for d, p in best]
    # 結構：在名家與人氣配色中，有「冷深色＋工程黃」的組合裡，第三色家族出現比例
    if len(cols) >= 3 and is_cool(cols[0]) and is_yellow(cols[1]):
        hit = [p for p in refs['palettes'] if any(is_cool(x) for x in p['colors']) and any(is_yellow(x) for x in p['colors'])]
        fams = collections.Counter()
        for p in hit:
            fams.update(set(family(x) for x in p['colors'] if not is_cool(x) and not is_yellow(x)))
        mine = [family(x) for x in cols[2:]]
        out['structure'] = {'combos_with_cool_dark_and_yellow': len(hit),
                            'your_third_families': mine,
                            'share': {f: f'{fams[f]}/{len(hit)}' for f in sorted(set(mine))},
                            'top_families': fams.most_common(6)}
    # 兩兩對比、灰階、色弱
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            a, b = cols[i], cols[j]
            out['pairs'].append({'a': ROLE(i), 'b': ROLE(j), 'wcag': round(contrast(a, b), 2),
                                 'gray_dL': round(abs(oklch(gray(a))[0] - oklch(gray(b))[0]) * 100, 1),
                                 **{k: round(de(cvd(a, k), cvd(b, k)), 1) for k in ('紅色弱', '綠色弱', '藍色弱')}})
    for i, h in enumerate(cols):
        out['colors'][i]['on_white'] = round(contrast(h, '#FFFFFF'), 2)
        out['colors'][i]['on_black'] = round(contrast(h, '#000000'), 2)
    return out


def text_report(r):
    p = []
    p.append(f"■ {r['name'] or '這組配色'}")
    for c in r['colors']:
        p.append(f"\n{c['role']} {c['hex']}（{c['family']}；OKLCH {c['oklch']}；白底對比 {c['on_white']}，黑底 {c['on_black']}）")
        for g, ns in c['near'].items():
            p.append(f"  最近{g}：" + '、'.join(f"{n['name']} {n['hex']} ΔE{n['de']}" for n in ns))
        p.append(f"  全球品牌 ΔE<8 有 {c['global_within_8']} 個：" + '、'.join(f"{n['name']}" for n in c['global_examples']))
    for src, ns in r['neighbours'].items():
        p.append(f"\n{src} 最像的 5 組（平均 ΔE）：")
        for n in ns:
            p.append(f"  #{n['id']} {' '.join(n['colors'])}  {n['avg_de']}")
    if r['structure']:
        s = r['structure']
        p.append(f"\n結構：名家＋人氣共 {s['combos_with_cool_dark_and_yellow']} 組有冷深色＋黃；你的第三色家族 {s['your_third_families']} 出現比例 {s['share']}；最常見 {s['top_families']}")
    p.append('\n兩兩對比（WCAG）、灰階明度差（OKLCH L×100）、色弱後 ΔE00：')
    for x in r['pairs']:
        p.append(f"  {x['a']}×{x['b']}：對比 {x['wcag']}；灰階差 {x['gray_dL']}；紅弱 {x['紅色弱']} 綠弱 {x['綠色弱']} 藍弱 {x['藍色弱']}")
    return '\n'.join(p)


def html_report(r):
    e = H.escape
    sw = lambda h, w=56: f'<span class="sw" style="background:{h};width:{w}px"></span>'
    rows = []
    for c in r['colors']:
        near = ''.join(f"<li>{e(g)}：{'、'.join(f'{sw(n['hex'],14)}{e(n['name'])} ΔE{n['de']}' for n in ns)}</li>" for g, ns in c['near'].items())
        rows.append(f"<section><h3>{sw(c['hex'])} {e(c['role'])} {c['hex']}</h3><p>{e(c['family'])}；白底對比 {c['on_white']}；全球品牌 ΔE&lt;8：{c['global_within_8']} 個</p><ul>{near}</ul></section>")
    nb = ''.join(f"<h3>{e(src)} 最像的組合</h3>" + ''.join(f"<div class='pal'>{''.join(sw(h, 36) for h in n['colors'])} <small>#{n['id']} 平均 ΔE {n['avg_de']}</small></div>" for n in ns) for src, ns in r['neighbours'].items())
    pr = ''.join(f"<tr><td>{e(x['a'])}×{e(x['b'])}</td><td>{x['wcag']}</td><td>{x['gray_dL']}</td><td>{x['紅色弱']}</td><td>{x['綠色弱']}</td><td>{x['藍色弱']}</td></tr>" for x in r['pairs'])
    return f"""<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>配色比對</title>
<style>body{{font:15px/1.6 system-ui,'Noto Sans TC',sans-serif;margin:16px;color:#1b1f23;background:#fff}}.sw{{display:inline-block;height:28px;vertical-align:middle;border-radius:3px;margin-right:4px}}ul{{padding-left:18px}}table{{border-collapse:collapse}}td,th{{border-bottom:1px solid #ddd;padding:4px 6px;text-align:right}}td:first-child{{text-align:left}}.pal{{margin:4px 0}}</style>
<h2>{e(r['name'] or '配色比對')}</h2><div>{''.join(sw(c['hex'], 72) for c in r['colors'])}</div>{''.join(rows)}{nb}
<h3>對比與色弱</h3><table><tr><th></th><th>對比</th><th>灰階差</th><th>紅弱</th><th>綠弱</th><th>藍弱</th></tr>{pr}</table>"""


def main(argv):
    errs = selftest()
    if errs:
        print('自我測試失敗：', errs); return 2
    cols, name, js, ht = [], '', None, None
    it = iter(argv)
    for a in it:
        if a == '--name': name = next(it)
        elif a == '--json': js = next(it)
        elif a == '--html': ht = next(it)
        else: cols.append('#' + a.lstrip('#').upper())
    if len(cols) < 2:
        print(__doc__); return 1
    r = check(cols, load(), name)
    print(text_report(r))
    if js: json.dump(r, open(js, 'w'), ensure_ascii=False, indent=1)
    if ht: open(ht, 'w').write(html_report(r))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
