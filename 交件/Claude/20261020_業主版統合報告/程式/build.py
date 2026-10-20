import json
P = json.load(open('palette_both.json'))
FOOT = '崧淳環保科技｜企業識別主視覺色 研究與候選報告｜2026-10-20'
pages = []

def page(body, n=True):
    pages.append(body)

def foot(i):
    return f'<div class="foot"><span>{FOOT}</span><span>{i}</span></div>'

LBL = {'primary': '主色', 'deep': '深階', 'mid': '中階', 'light': '淺階', 'ink': '墨色（文字）', 'grey': '冷灰', 'pale': '淺灰', 'mist': '霧白（大面積底）'}

def spec_rows(d, keys, lbl):
    out = []
    for k in keys:
        v = d[k]
        c = '/'.join(str(x) for x in v['cmyk'])
        r = ','.join(str(x) for x in v['rgb'])
        out.append(f'<tr><td><span class="sw" style="background:{v["hex"]}"></span>{lbl[k]}</td><td class="mono">{v["hex"]}</td><td class="mono">{r}</td><td class="mono">{c}</td><td>{v["pantone"][0]}<br><span class="note">ΔE {v["pantone"][1]}</span></td><td>{v["ral"][0]}<br><span class="note">ΔE {v["ral"][2]}</span></td><td class="n">{v["white"]:.2f}</td></tr>')
    return '\n'.join(out)

def spec_table(name):
    d = P[name]
    s = P['shared']
    rows = spec_rows(d, ['primary', 'deep', 'mid', 'light', 'ink', 'grey', 'pale', 'mist'], LBL)
    rows += '\n' + spec_rows(s, ['yellow', 'ylight', 'white'], {'yellow': '工程黃（車身，已定）', 'ylight': '黃淺', 'white': '白'})
    return f'''<table><tr><th>用途</th><th>HEX</th><th>RGB</th><th>CMYK（參考）</th><th>Pantone 最近</th><th>RAL 最近</th><th class="n">對白底<br>亮度比</th></tr>
{rows}</table>'''

def scale(name):
    d = P[name]
    ks = ['deep', 'primary', 'mid', 'light', 'mist']
    cells = []
    for k in ks:
        h = d[k]['hex']
        fg = '#fff' if d[k]['white'] > 4.5 else '#1a1a1a'
        cells.append(f'<div style="background:{h};color:{fg}">{LBL[k].split("（")[0]}<br>{h}</div>')
    return '<div class="scale">' + ''.join(cells) + '</div>'

exec(open('pages.py').read())

html = '<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><title>崧淳主視覺色報告</title><link rel="stylesheet" href="r.css"></head><body>\n'
for i, b in enumerate(pages, 1):
    html += (f'<section class="page">{b}</section>\n' if i == 1 else f'<section class="page"><div class="inner">{b}</div>{foot(i)}</section>\n')
html += '</body></html>'
open('report.html', 'w').write(html)
print(len(pages), 'pages')
