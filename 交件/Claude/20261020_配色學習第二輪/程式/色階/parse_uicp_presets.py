"""讀 UI Color Palette 外掛的色階預設（a-ng-d/ui-ui-color-palette 提交 c212430 src/stores/presets.ts）。
這些是外掛作者對各設計系統的近似設定（階數、明度上下限、分布），不是各系統官方資料。"""
import re, json, sys
src = open(sys.argv[1], encoding='utf-8').read()
out = []
for m in re.finditer(r"\{\s*name: locales\('([^']+)'\),\s*stops: \[([^\]]*)\],\s*min: (\d+),\s*max: (\d+),(.*?)id: '([^']+)'", src, re.S):
    body = m.group(5)
    ease = re.search(r"easing: '([^']+)'", body)
    stops = [s.strip() for s in m.group(2).split(',') if s.strip()]
    out.append({'id': m.group(6), 'stops': stops, 'n_stops': len(stops), 'lightness_min': int(m.group(3)),
                'lightness_max': int(m.group(4)), 'easing': ease.group(1) if ease else None})
json.dump(out, open('/tmp/claude-0/r2/scales/uicp_presets.json', 'w'), indent=1)
for o in out:
    print(o['id'], o['n_stops'], o['lightness_min'], o['lightness_max'], o['easing'], ' '.join(o['stops']))
