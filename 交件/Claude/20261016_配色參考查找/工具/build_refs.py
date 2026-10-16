"""把各來源整理成一份參照庫（工具/參照庫.json），給 palette_check.py 用。
用法（在 repo 根目錄或任何地方都可）：python3 -I build_refs.py
只用標準函式庫。資料來源與等級寫在每一筆的 src、grade。
"""
import json, os, re, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))  # repo 根目錄
DATA = os.path.join(HERE, '..', '資料')
RAW = os.path.join(DATA, '原始')


def rp(*p): return os.path.join(ROOT, *p)


HEX = re.compile(r'#[0-9A-Fa-f]{6}\b')
refs = {'brands': [], 'palettes': [], 'global': []}

# 1) 台灣同業 14 家（2026-10-11 梁特助電腦上取色；logo＋網站全部 HEX）
tw = json.load(open(rp('交件', 'Claude', '20261014_第十五輪雲端重跑', '輸入', '同業色_B_總表全量.json')))
for c in tw['colors']:
    refs['brands'].append({'group': '台灣同業', 'name': c['company'], 'where': c.get('where', ''), 'hex': c['hex'].upper(),
                           'src': '研究/同業圖片/logo與車輛_20261011/同業色彩整理.md', 'grade': '取色'})

# 2) 台灣街頭參照色（工地、交通、公部門；多為近似值）
site = json.load(open(rp('交件', 'Claude', '20261014_第十五輪雲端重跑', '輸入', '參照色_誤認規則.json')))
for c in site['site_colors']:
    refs['brands'].append({'group': '台灣街頭', 'name': c['name'], 'where': '', 'hex': c['hex'].upper(),
                           'src': '交件/Claude/20261014_第十五輪雲端重跑/輸入/參照色_誤認規則.json', 'grade': '近似'})

# 3) 國外同業 18 家（Brandfetch 擷取，2026-10-12）
for line in open(rp('交件', 'Claude', '20261014_全部成果同步', '04_定位與產業研究', '11_C_國外同業.md'), encoding='utf-8'):
    m = re.match(r'^\| (\d+) \| ([^|]+) \| ([^|]+) \| [^|]+ \| ([^|]+) \|', line)
    if not m: continue
    for h in HEX.findall(m.group(4)):
        refs['brands'].append({'group': '國外同業', 'name': m.group(2).strip(), 'where': m.group(3).strip(), 'hex': h.upper(),
                               'src': '交件/Claude/20261014_全部成果同步/04_定位與產業研究/11_C_國外同業.md', 'grade': 'C（Brandfetch）'})

# 4) 本次新查：國外冷色識別＋黃色車隊（A1）、台灣冷色＋黃（A2）
for fn, group in [('國外_冷色識別加黃色車隊.json', '國外冷色＋黃'), ('台灣_冷色加黃.json', '台灣冷色＋黃')]:
    p = os.path.join(DATA, fn)
    if not os.path.exists(p): continue
    for it in json.load(open(p)):
        slots = []
        for k in ('cool_primary', 'primary', 'yellow'):
            if isinstance(it.get(k), dict): slots.append((k, it[k]))
        for t in it.get('third_or_neutral', []) or it.get('third', []) or []:
            if isinstance(t, dict): slots.append(('third', t))
        for role, s in slots:
            for h in HEX.findall(str(s.get('hex', ''))):
                refs['brands'].append({'group': group, 'name': it['name'], 'where': role, 'hex': h.upper(),
                                       'src': s.get('source_url', ''), 'grade': s.get('grade', '')})

# 5) 名家與人氣配色
wada = json.load(open(os.path.join(RAW, 'wada_colors.json')))
combos = collections.defaultdict(list)
for c in wada:
    for cid in c['combinations']:
        combos[cid].append(c['hex'].upper())
for cid, hs in sorted(combos.items()):
    refs['palettes'].append({'src': '和田三造《配色事典》', 'id': cid, 'colors': hs})
for i, p in enumerate(json.load(open(os.path.join(RAW, 'colourlovers_1000.json')))):
    refs['palettes'].append({'src': 'COLOURlovers 人氣', 'id': i + 1, 'colors': [h.upper() for h in p]})

# 6) 全球品牌主色（simple-icons 16.35.0，CC0；以科技品牌居多）
for b in json.load(open(os.path.join(RAW, 'simple_icons_16.35.0_title_hex.json'))):
    refs['global'].append({'name': b['title'], 'hex': b['hex'].upper()})

out = os.path.join(HERE, '參照庫.json')
json.dump(refs, open(out, 'w'), ensure_ascii=False)
print('brands', len(refs['brands']), collections.Counter(b['group'] for b in refs['brands']))
print('palettes', len(refs['palettes']), 'global', len(refs['global']))
