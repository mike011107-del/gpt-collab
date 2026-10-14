import json,sys
sys.argv=['x']
import check as C
from ok import cr,rgb
S=json.load(open('system.json')); R=json.load(open('RAL_wikipedia.json'))
def ral(h):
    L1=C.lab_std(h); d,k,n=min((C.de2000_lab(L1,tuple(v['lab'])),k,v['name']) for k,v in R.items()); return k,n,round(d,1)
def cmyk(h):
    r,g,b=[x/255 for x in rgb(h)]; k=1-max(r,g,b)
    if k>=1: return (0,0,0,100)
    return tuple(round(100*x) for x in ((1-r-k)/(1-k),(1-g-k)/(1-k),(1-b-k)/(1-k),k))
USE={'主色':'車身大面積、圍籬、名片背面、報告封面','主色深':'黃字的底（字幕條、深色資訊帶）','主色淺':'文件淺色底塊','主色上的字':'主色底上的字',
 '工程黃':'車頭、背心、告示帶、分隔帶','黃上的字':'黃底上的字（一律深字）','黃淺':'文件重點列底色','黃深_白底小字':'白底上要用黃色系的小字時',
 '紙':'文件底','分區':'表頭、交替列','邊線':'表格線、分隔線（不放字）','次要字':'欄名、註記','正文':'正文、數字'}
def sw(h,lab,key=False):
    tc='#FFFFFF' if cr('#FFFFFF',h)>cr('#111111',h) else '#111111'
    return f'<div class="s" style="background:{h};color:{tc}">{"●" if key else ""}<b>{lab}</b><i>{h}</i></div>'
def build(g):
    s=S['system'][g]; d=g[0]; D=S['dirs'][d]; T=s['tokens']; th=S['third'][g]
    mr=''.join(sw(h,st,st==s['main_step']) for st,h in s['main_ramp'])
    yr=''.join(sw(h,st,st==s['yellow_step']) for st,h in s['yellow_ramp'])
    nr=''.join(sw(h,st,h.upper()==th['hex'].upper()) for st,h in s['neutral'])
    tok=''.join(f'<div class="t"><span style="background:{v}"></span><div><b>{k.replace("_","・")}</b> {v}<br><i>{USE[k]}</i></div></div>' for k,v in T.items())
    pr=''.join(f'<li>{"✓" if p["過"] else "✗"} {p["字"].replace("_","・")} 在 {p["底"]} 上　<b>{p["比值"]}</b>（要 {p["門檻"]}）</li>' for p in s['pairs'])
    rows=''
    for nm,h in ((D['main_name'],D['main']),('工程黃',T['工程黃']),(th['name'],th['hex'])):
        k,n,de=ral(h); c=cmyk(h); r=rgb(h)
        rows+=f'<tr><td><span class="dot" style="background:{h}"></span>{nm}</td><td>{h}</td><td>{r[0]} {r[1]} {r[2]}</td><td>{c[0]} {c[1]} {c[2]} {c[3]}</td><td>RAL {k}<br><i>ΔE {de}</i></td></tr>'
    chg=f'原 {D["orig"]} → 提純 {D["main"]}' if D['orig']!=D['main'] else '主色不變'
    html=f'''<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;700&display=block" rel="stylesheet"><style>
*{{box-sizing:border-box}}body{{margin:0;width:1000px;background:#F4F3EF;font-family:'Noto Sans TC';color:#1B1E21;padding:28px 30px}}
h1{{font-size:24px;margin:0 0 4px}}h2{{font-size:15px;margin:22px 0 8px;color:#444}}.sub{{color:#555;font-size:14px}}
.r{{display:flex;gap:3px}}.s{{flex:1;height:74px;padding:6px;font-size:11px;display:flex;flex-direction:column;justify-content:flex-end;position:relative}}
.s b{{font-size:12px}}.s i{{font-style:normal;opacity:.85}}.rl{{font-size:12px;color:#555;margin:8px 0 3px}}
.tk{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px 14px}}.t{{display:flex;gap:8px;font-size:12.5px;line-height:1.45}}.t span{{width:34px;height:34px;flex:none;border:1px solid rgba(0,0,0,.12)}}.t i{{font-style:normal;color:#666}}
ul{{margin:0;padding:0;list-style:none;columns:2;font-size:13px;line-height:1.9}}
table{{border-collapse:collapse;width:100%;font-size:13px}}td,th{{border-bottom:1px solid #D5D3CC;padding:7px 6px;text-align:left;vertical-align:top}}th{{background:#E8E6E0}}td i{{font-style:normal;color:#666;font-size:12px}}
.dot{{display:inline-block;width:14px;height:14px;margin-right:6px;vertical-align:-2px;border:1px solid rgba(0,0,0,.15)}}.note{{font-size:12px;color:#666;margin-top:6px;line-height:1.6}}
</style></head><body>
<h1>{g}　{D['name']}｜{D['main_name']}＋工程黃＋{th['name']}</h1><div class="sub">{chg}。第三色角色：{th['role']}</div>
<h2>色階（● 為標準色所在的階；三條色階同一階明度相同）</h2>
<div class="rl">主色　{D['main_name']}</div><div class="r">{mr}</div>
<div class="rl">工程黃（變深時往赭褐走，不變成髒黃）</div><div class="r">{yr}</div>
<div class="rl">中性色（紙、分區、邊線、次要字、正文）{'　● 為 '+th['name'] if th['hex'].upper() in [h.upper() for _,h in s['neutral']] else ''}</div><div class="r">{nr}</div>
<h2>角色色（設計時只用這些）</h2><div class="tk">{tok}</div>
<h2>文字配對檢查（WCAG 2 對比，螢幕）</h2><ul>{pr}</ul>
<h2>規格（CMYK 是螢幕換算參考；RAL 是 Wikipedia 色表最近色號，ΔE 大於 2 就不算同色，烤漆要做實體色板）</h2>
<table><tr><th>顏色</th><th>HEX</th><th>RGB</th><th>CMYK 參考</th><th>最近 RAL</th></tr>{rows}</table>
</body></html>'''
    open(f'out/{g}_sheet.html','w').write(html)
for g in S['third']: build(g)
