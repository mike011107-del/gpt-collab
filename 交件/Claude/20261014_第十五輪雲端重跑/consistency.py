#!/usr/bin/env python3
"""第十五輪交付一致性檢查：輸入檔、原分數 JSON、check.py 結果、手機頁、八張合成圖。

用法（在本資料夾，先跑過 check.py）：python3 consistency.py
需要 Pillow（只用來讀圖取色）。輸出：結果/一致性.json、結果/一致性.md。退出碼：0＝全部一致；3＝有不一致（細節見輸出）。
"""
import json, os, re, sys, statistics
from check import de, contrast

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', '20261014_全部成果同步', '01_第十五輪配色')
P = json.load(open(os.path.join(HERE, '輸入', '八組.json'), encoding='utf-8'))
O = json.load(open(os.path.join(HERE, '輸入', '原報告值_分數.json'), encoding='utf-8'))
R = json.load(open(os.path.join(HERE, '結果', '結果.json'), encoding='utf-8'))
page = open(os.path.join(SRC, '手機頁.html'), encoding='utf-8').read()
Y = P['工程黃']['hex']; DK = P['文字色']['深']; WH = P['文字色']['白']

# 原程式 livery20.py SPEC 與 docs20.py 的字色設定（逐字轉錄，見 圖說.md）
TANK_TEXT = {'1A': WH, '1B': WH, '2A': WH, '2B': WH, '3A': Y, '3B': Y, '4A': DK, '4B': 'third'}
# docs20.py 各組額外的字（逐字轉錄色碼；3 方向圍籬疊字條是主色上加 38% 黑）
def over(h, a=0.38):
    from check import lin3, from_lin
    return from_lin([v*(1-a) for v in lin3(h)])
EXTRA = {
 '1A': [('「崧」字裡的公（黃）', Y, '#395848'), ('報告封底「山」字', '#FFFFFF', '#909586'), ('報告封底「木」字', '#FFFFFF', '#395848'), ('報告封底「公」字', '#1B1E21', Y)],
 '1B': [('「崧」字裡的公（黃）', Y, '#395848'), ('印章字', '#F6F1E6', '#B8283A')],
 '2A': [('名片背面「崧」字（黃）', Y, '#086A74')], '2B': [('名片背面「崧」字（黃）', Y, '#086A74')],
 '3A': [('名片背面「崧淳」（黃）', Y, '#081C2F'), ('圍籬疊字條（黃字）', Y, over('#081C2F')), ('CCTV 缺陷標籤', '#111111', '#F05A6E')],
 '3B': [('名片背面「崧淳」（黃）', Y, '#081C2F'), ('圍籬疊字條（黃字）', Y, over('#081C2F')), ('CCTV 合格標籤', '#111111', '#3CCB7F')],
}
issues = []; out = {}
try:
    from PIL import Image
except ImportError:
    Image = None
    issues.append('沒有 Pillow，略過圖片取色')

def patch(im, x, y, r=4):
    px = [im.getpixel((i, j)) for i in range(x-r, x+r+1) for j in range(y-r, y+r+1)]
    return '#%02X%02X%02X' % tuple(int(statistics.median(p[k] for p in px)) for k in range(3))

for g in P['groups']:
    k = g['group']; key = g['key']; m = g['colors'][0]['hex']; t = g['colors'][2]['hex']
    o = O[key]; rec = {}
    # 1. 輸入 vs 原分數 JSON
    rec['輸入=原JSON'] = (o['main'][1] == m and o['third'][1] == t and list(o['share']) == [c['share'] for c in g['colors']])
    if not rec['輸入=原JSON']: issues.append(f'{k} 輸入檔與原分數 JSON 的色碼或比例不同')
    # 2. 手機頁
    a = page.find(f'<article class="combo" id="{key}">'); b = page.find('</article>', a)
    sec = page[a:b] if a >= 0 else ''
    tot = re.search(r'class="tot">(\d+)', sec)
    sws = re.findall(r'<b>([^<]+)</b><span>(#[0-9A-F]{6})</span><span>RAL (\d{4})[^<]*</span><i>約 (\d+)%</i>', sec)
    rec['手機頁'] = {'找到': bool(sec), '總分': int(tot.group(1)) if tot else None, '色票': sws, '圖片': re.findall(r'src="([^"]+)"', sec)}
    if not sec: issues.append(f'{k} 手機頁找不到這組')
    if tot and int(tot.group(1)) != o['fate30']+o['market70']: issues.append(f'{k} 手機頁總分 {tot.group(1)} ≠ 原 JSON {o["fate30"]+o["market70"]}')
    exp = [(c['name'], c['hex'], c['share']) for c in g['colors']]
    got = [(n, h, int(p)) for n, h, _, p in sws]
    if got != exp: issues.append(f'{k} 手機頁色票 {got} ≠ 輸入 {exp}')
    ral_page = [r for _, _, r, _ in sws]
    ral_json = [o['ral_main'][0], '1018', o['ral_third'][0]]
    if ral_page != ral_json: issues.append(f'{k} 手機頁 RAL {ral_page} ≠ 原 JSON {ral_json}')
    pub = R['groups'][k]['public']['RAL最近']
    rec['RAL'] = {'手機頁': ral_page, '原JSON': ral_json, '重算_依RGB欄': [pub[r]['依RGB欄']['RAL'] for r in ('主色', '工程黃', '第三色')], '重算_依Lab欄': [pub[r]['依Lab欄']['RAL'] for r in ('主色', '工程黃', '第三色')]}
    # 3. 圖片取色（合成圖下方文件區是平塗色，可取樣）
    img = os.path.join(SRC, '圖', key + '.jpg')
    if Image and os.path.exists(img):
        im = Image.open(img).convert('RGB')
        smp = {'圍籬底（主色）': (patch(im, 108, 827), m), '圍籬黃帶（工程黃）': (patch(im, 626, 904), Y), '報告封面頂（主色）': (patch(im, 1037, 795), m)}
        rec['圖片取色'] = {n: {'取得': v[0], '應為': v[1], 'ΔE2000': round(de(v[0], v[1]), 2)} for n, v in smp.items()}
        for n, v in rec['圖片取色'].items():
            if v['ΔE2000'] > 3: issues.append(f'{k} 圖片 {n} 取色 {v["取得"]} 與 {v["應為"]} 差 {v["ΔE2000"]}')
        rec['圖片尺寸'] = im.size
    elif Image:
        issues.append(f'{k} 缺圖 {img}')
    # 4. 圖中文字配色對（依原程式設定）
    tt = t if TANK_TEXT[k] == 'third' else TANK_TEXT[k]
    om = DK if contrast(DK, m) >= contrast(WH, m) else WH
    oy = DK if contrast(DK, Y) >= contrast(WH, Y) else WH
    if k == '4B': om = t  # docs20.py：4B 主色上的字改用第三色
    pairs = [('罐身與廂型車公司全名', tt, m), ('圍籬、名片背面、報告封面字', om, m), ('黃帶上的字', oy, Y), ('CCTV 畫面字幕條', Y, m)]
    pairs += EXTRA.get(k, [])
    rec['文字配色'] = [{'位置': n, '字': f, '底': bg, 'WCAG對比': round(contrast(f, bg), 2), '達4.5': contrast(f, bg) >= 4.5, '達3': contrast(f, bg) >= 3} for n, f, bg in pairs]
    out[k] = rec

json.dump({'不一致': issues, 'groups': out}, open(os.path.join(HERE, '結果', '一致性.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
with open(os.path.join(HERE, '結果', '一致性.md'), 'w', encoding='utf-8') as f:
    f.write('# 交付一致性（自動產生）\n\n')
    f.write('## 不一致\n\n' + ('\n'.join(f'- {x}' for x in issues) if issues else '- 無') + '\n\n')
    f.write('## RAL 標示\n\n| 組 | 手機頁 | 原 JSON | 重算（依 RGB 欄） | 重算（依 Lab 欄） |\n|---|---|---|---|---|\n')
    for k, r in out.items(): f.write(f"| {k} | {'／'.join(r['RAL']['手機頁'])} | {'／'.join(r['RAL']['原JSON'])} | {'／'.join(r['RAL']['重算_依RGB欄'])} | {'／'.join(r['RAL']['重算_依Lab欄'])} |\n")
    f.write('\n## 圖片平塗區取色\n\n| 組 | 位置 | 取得 | 應為 | ΔE2000 |\n|---|---|---|---|---|\n')
    for k, r in out.items():
        for n, v in r.get('圖片取色', {}).items(): f.write(f"| {k} | {n} | {v['取得']} | {v['應為']} | {v['ΔE2000']} |\n")
    f.write('\n## 圖中文字配色對（WCAG 對比）\n\n| 組 | 位置 | 字 | 底 | 對比 | ≥4.5 | ≥3 |\n|---|---|---|---|---|---|---|\n')
    for k, r in out.items():
        for p in r['文字配色']: f.write(f"| {k} | {p['位置']} | {p['字']} | {p['底']} | {p['WCAG對比']} | {'是' if p['達4.5'] else '**否**'} | {'是' if p['達3'] else '**否**'} |\n")
print('不一致：', len(issues)); [print(' ', x) for x in issues]
sys.exit(3 if issues else 0)
