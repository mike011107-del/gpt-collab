"""Audit shared records and four existing images; never fetch or change inputs.

Run: python 交件/GPT/20261024_同業配色比較查核/audit.py
Requires numpy and Pillow. Output JSON/CSV and a chart containing data rectangles
only. Pixel shares describe this mask and these files, not brand standards.
"""
from pathlib import Path
import collections
import csv
import hashlib
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
DATA = ROOT / '交件/Claude/20261020_配色學習第二輪/數據/台灣同業'
IMAGES = ROOT / '研究/同業圖片/logo與車輛_20261011'
BASE = '4fc2c93edf186988e96b9006f561fa3899bf63e4'

def read(name):
    return json.loads((DATA / name).read_text())

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def lab(rgb):
    v = np.asarray(rgb, dtype=float) / 255
    v = np.where(v <= .04045, v / 12.92, ((v + .055) / 1.055) ** 2.4)
    lms = v @ np.array([[.4122214708, .5363325363, .0514459929],
                       [.2119034982, .6806995451, .1073969566],
                       [.0883024619, .2817188376, .6299787005]]).T
    return np.cbrt(lms) @ np.array([[.2104542553, .7936177850, -.0040720468],
                                   [1.9779984951, -2.4285922050, .4505937099],
                                   [.0259040371, .7827717662, -.8086757660]]).T

def rgb(h):
    return [int(h[i:i+2], 16) for i in (1, 3, 5)]

peers = read('tw_peers.json')
versions = read('measure_final.json')
inventory = read('inventory.json')
source_files = [DATA / n for n in ('tw_peers.json', 'measure_final.json',
    'inventory.json', 'share_sensitivity.json', 'corrections.md', 'comparison.json')]
rows = []
for p in peers:
    colors = (p.get('cols') or []) + (p.get('neutral') or [])
    known = [c for c in colors if c.get('share') is not None]
    largest = max(known, key=lambda c: c['share'], default=None)
    rows.append(dict(company=p['company'], version=p['vid'], source_tier=p['tier'],
        source_reference=p['source'], recorded_main=p.get('main'),
        largest_recorded_component=largest['hex'] if largest else None,
        largest_recorded_share=largest['share'] if largest else None,
        listed_share_sum=round(sum(c['share'] for c in known), 4),
        n_chromatic=p.get('n_chromatic'), gradient=p['gradient'],
        alternate_versions=p['alt'], source_note=p['note'],
        direct_sewer_cctv_scope_verified_this_round=False,
        current_website_verified_this_round=False))

checks = []
for company, filename in [
    ('源昌', '07_源昌工程環保科技.png'),
    ('逸居管必潔', '09_逸居管必潔.png'),
    ('宏隆', '12_宏隆環保.png'),
    ('日技', '11_日技管清工程.gif'),
]:
    p = next(x for x in peers if x['company'] == company)
    path = IMAGES / filename
    source_files.append(path)
    im = Image.open(path).convert('RGBA')  # GIF: first frame only
    a = np.asarray(im)
    ok = lab(a[..., :3])
    mask = (a[..., 3] >= 250) & ~((ok[..., 0] >= .93) &
                                      (np.hypot(ok[..., 1], ok[..., 2]) < .04))
    pixels = ok[mask]
    colors = (p.get('cols') or []) + (p.get('neutral') or [])
    seeds = [c['hex'] for c in colors if c.get('share') is not None]
    seed_ok = lab([rgb(h) for h in seeds])
    # Nearest existing seed, no erosion, no new color candidates.
    nearest = np.argmin(np.sum((pixels[:, None, :] - seed_ok[None, :, :]) ** 2, axis=2), axis=1)
    counts = np.bincount(nearest, minlength=len(seeds))
    shares = counts / len(pixels)
    exact = {h: int(np.all(a[..., :3][mask] == rgb(h), axis=1).sum()) for h in seeds}
    checks.append(dict(company=company, version=p['vid'],
        image_path=path.relative_to(ROOT).as_posix(), sha256=digest(path),
        size=list(im.size), visible_nonwhite_pixel_count=int(mask.sum()),
        alpha_valid_pixel_count=int((a[..., 3] >= 250).sum()),
        seeds=seeds, source_shares=[c['share'] for c in colors if c.get('share') is not None],
        source_method=p['share_method'], unfiltered_nearest_seed_counts=counts.tolist(),
        unfiltered_nearest_seed_shares=shares.tolist(), exact_seed_pixel_counts=exact,
        max_absolute_share_change=float(max(abs(shares[i]-colors[i]['share']) for i in range(len(seeds)))),
        new_measurement_method='alpha>=250; remove OKLab L>=0.93 and C<0.04; no erosion; nearest listed seed in Euclidean OKLab',
        limitation='All retained pixels assigned to existing seeds; omitted colors cannot be discovered; denominator excludes white and transparency.'))

result = dict(date='2026-10-24', timezone='Asia/Taipei', base_commit=BASE,
    facts=dict(primary_records=len(peers), measured_versions=len(versions),
        color_statistics_records=sum(p.get('n_chromatic') is not None for p in peers),
        source_tiers=dict(collections.Counter(p['tier'] for p in peers)),
        measured_versions_with_source_url=sum('http://' in x['source'] or 'https://' in x['source'] for x in versions),
        primary_has_direct_service_verification_field=any('service_evidence' in p for p in peers),
        inventory_rows=len(inventory['rows'])),
    primary_records=rows,
    versions=[{k:v[k] for k in ('vid','company','version','source','tier','primary','method')} for v in versions],
    pixel_checks=checks,
    inputs=[dict(path=p.relative_to(ROOT).as_posix(), sha256=digest(p)) for p in source_files],
    scope='Repository snapshot audit and four image checks; not current-site, complete-CIS, market-recognition, or customer testing.')
(OUT / 'audit.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
with (OUT / '同行版本索引.csv').open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=list(result['versions'][0]), lineterminator='\n')
    writer.writeheader()
    writer.writerows(result['versions'])

# Data-only chart: retained source fractions are not renormalized to 100%.
fontfile = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
font = lambda n: ImageFont.truetype(fontfile, n)
im = Image.new('RGB', (1600, 1160), '#FFFFFF')
d = ImageDraw.Draw(im)
d.text((48,28), '同業用色：最大彩色 ≠ 畫面最大色塊', fill='#17212B', font=font(39))
d.text((48,92), '四個庫內原檔的數據核對｜不是崧淳候選色，也不是現行品牌標準', fill='#394856', font=font(25))
d.text((48,134), '長條均以非白前景為分母；白與透明已排除，不能當成整張圖面積。', fill='#394856', font=font(24))
for j,c in enumerate(checks):
    y = 196 + j*211
    d.text((48,y), c['company'], fill='#17212B', font=font(28))
    for k, (label, values) in enumerate([('原表',c['source_shares']),('本次不去邊',c['unfiltered_nearest_seed_shares'])]):
        yy=y+48+k*47
        d.text((48,yy),label,fill='#394856',font=font(22))
        d.rectangle((230,yy,1530,yy+32),fill='#E5E7EB')
        x=230
        for h,share in zip(c['seeds'],values):
            nx=x+1300*share
            if nx>x: d.rectangle((round(x),yy,round(nx)-1,yy+32),fill=h)
            x=nx
    desc='；'.join(f'{h}：{a*100:.2f}%→{b*100:.2f}%' for h,a,b in zip(c['seeds'][:2],c['source_shares'][:2],c['unfiltered_nearest_seed_shares'][:2]))
    d.text((230,y+144),desc,fill='#394856',font=font(21))
d.text((48,1054),'原表尾端灰底＝未列出的殘餘份量；本次將像素分給既有色碼，不用於找出漏列顏色。',fill='#394856',font=font(23))
d.text((48,1097),'來源與重跑：同目錄 audit.json / audit.py。2026-10-24｜GPT 資料查核，待 Claude 評閱。',fill='#394856',font=font(23))
im.save(OUT / '份量方法比較.png')
print(json.dumps(result['facts'],ensure_ascii=False))
for c in checks:
    print(c['company'], [(h,round(v*100,3)) for h,v in zip(c['seeds'],c['unfiltered_nearest_seed_shares'])])
