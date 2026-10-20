# 文字版附錄：台灣 21 家色表、多色 logo、Itten 實例、色名、面積示意的數據
import json
tw = json.load(open('/tmp/claude-0/r2/tw/tw_peers.json'))
itt = json.load(open('/tmp/claude-0/r2/theory/itten_examples.json'))
ap = json.load(open('/tmp/claude-0/r2/models/data/apply.json'))
L = ['## 附錄：PDF 色塊圖的數據', '', '### A. 台灣 21 家 logo 的顏色與佔比（佔 logo 非白部分）', '',
     '| 公司 | 彩色（色碼 佔比） | 黑灰 | 配色方式 | 漸層 | 字 |', '|---|---|---|---|---|---|']
for p in tw:
    cols = '、'.join(f"{c['hex']} {round(100*c['share'])}%" for c in (p.get('cols') or []) if c.get('share'))
    neu = '、'.join(f"{n['hex']} {round(100*n['share'])}%" for n in (p.get('neutral') or []) if n.get('share') and n['hex'].upper() != '#FFFFFF')
    sch = p.get('scheme') or ('只有白色反白版，不計色' if p.get('white_only') else '墨色商標，不計色')
    if p.get('white_only'): sch = '只有白色反白版，不計色'
    if p.get('cols') is None: sch = '墨色商標，不計色'
    L.append(f"| {p['company']} | {cols or '—'} | {neu or '—'} | {sch} | {'有' if p.get('gradient') else '—'} | {p.get('font_cls') or '—'} |")
I = itt['examples']
L += ['', '### B. 第 19 頁 Itten 對比的國外同業實例（色碼）', '',
      f"- 色相對比：Watercare 四色 {'、'.join(I['色相對比'][0]['cols'])}",
      f"- 明暗對比：Insituform {I['明暗對比'][1]['a']['hex']}、{I['明暗對比'][1]['b']['hex']}（明度差 {I['明暗對比'][1]['dL']}）",
      f"- 冷暖對比：Watercare {I['冷暖對比'][0]['a']['hex']}、{I['冷暖對比'][0]['b']['hex']}（明度差 {I['冷暖對比'][0]['dL']}）",
      f"- 補色對比：Kier {I['補色對比'][0]['a']['hex']}、{I['補色對比'][0]['b']['hex']}（色相差 179.5°，明度差 0.6）",
      f"- 彩度對比：Tideway {I['彩度對比'][0]['a']['hex']}、{I['彩度對比'][0]['b']['hex']}（明度差 {I['彩度對比'][0]['dL']}）",
      f"- 同時對比（示意，三家拼的）：灰 {I['同時對比']['gray']['hex']} 放在 {I['同時對比']['bg1']['hex']}、{I['同時對比']['bg2']['hex']} 上"]
L += ['', '### C. 第 17 頁英文色名（xkcd 153 色名，Colorgorical 內建）', '']
T = ap['targets_single']
T['靛藍']['cg_top_terms'] = [['navyblue', 0.237], ['blue', 49 / 228], ['darkblue', 0.184]]
for k in ('深青', '靛藍', '工程黃'):
    L.append(f"- {k} {T[k]['hex']}：" + '、'.join(f"{a} {round(b*100)}%" for a, b in T[k]['cg_top_terms']))
L += ['', '### D. 第 23 頁面積示意（不是建議比例）', '',
      '- 配深青 #0C424A：面積跟 L* 成反比 → 黃 28.5%；Munsell 式 → 黃 11.3%',
      '- 配靛藍 #333D66：面積跟 L* 成反比 → 黃 29.8%；Munsell 式 → 黃 17.2%', '',
      '### E. 第 26 頁原色與最近 Radix 階', '',
      '- 深青 #0C424A → cyan 12 #0d3c48（ΔE2000 3.53）',
      '- 靛藍 #333D66 → indigo 12 #1f2d5c（5.32）',
      '- 工程黃 #D68702 → amber 8 #e2a336（8.12）', '']
open('out/appendix.md', 'w').write('\n'.join(L))
print('\n'.join(L)[:3000])
