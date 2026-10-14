"""第二版文件與現場示意（1000x600）：圍籬、名片正反、CCTV 報告封面、背心。
修正：圍籬柱線在字下面、拿掉電話信箱佔位字、每份報告都有 CCTV 畫面、標題用楷書、背心名牌放大。"""
import sys; sys.path.insert(0,'.')
from combos import combos
from sets import Y,text_on
OUT='/tmp/claude-0/-home-claude/f822ab78-49b8-5e2f-8fbe-8111b065c404/scratchpad/r19/out20'
DK='#111417'; WH='#FFFFFF'
HEAD='''<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=LXGW+WenKai+TC:wght@700&family=Noto+Sans+TC:wght@400;700&display=block" rel="stylesheet">
<style>
*{box-sizing:border-box}html,body{margin:0}
body{width:1000px;height:600px;background:#E9E8E4;font-family:'Noto Sans TC',sans-serif;position:relative;overflow:hidden;
 --m:%(m)s;--y:%(y)s;--t:%(t)s;--om:%(om)s;--oy:%(oy)s;--ot:%(ot)s;--paper:#F6F6F3;--ink:#1B1E21}
.kai{font-family:'LXGW WenKai TC',serif;font-weight:700}
.lab{position:absolute;font-size:13px;color:#55554F;letter-spacing:.05em}
.fence{position:absolute;left:24px;top:30px;width:610px;height:236px;background:var(--m);overflow:hidden;box-shadow:0 2px 6px rgba(0,0,0,.18)}
.posts{position:absolute;inset:0;background:repeating-linear-gradient(90deg,transparent 0 150px,rgba(0,0,0,.08) 150px 152px);z-index:1}
.fence .nm{position:absolute;left:28px;top:30px;font-size:34px;letter-spacing:3px;color:var(--om);white-space:nowrap;z-index:3}
.fence .sub{position:absolute;left:30px;top:88px;font-size:20px;color:var(--om);letter-spacing:2px;z-index:3}
.fence .yb{position:absolute;left:0;right:0;bottom:0;height:60px;background:var(--y);z-index:2}
.fence .yt{position:absolute;left:30px;bottom:15px;font-size:22px;font-weight:700;color:var(--oy);letter-spacing:1px;z-index:3}
.card{position:absolute;width:290px;height:174px;box-shadow:0 2px 6px rgba(0,0,0,.2);overflow:hidden}
.c1{left:24px;top:318px;background:var(--paper)}
.c1 .bar{position:absolute;left:0;top:0;bottom:0;width:16px;background:var(--m)}
.c1 .ybar{position:absolute;left:16px;top:0;bottom:0;width:7px;background:var(--y)}
.c1 .nm{position:absolute;left:40px;top:24px;font-size:19px;color:var(--ink);letter-spacing:1px}
.c1 .p{position:absolute;left:40px;top:62px;font-size:24px;color:var(--ink)}
.c1 .tx{position:absolute;left:40px;top:106px;font-size:13px;color:var(--ink);opacity:.85}
.c1 .tl{position:absolute;left:40px;right:24px;bottom:22px;height:5px;background:var(--t)}
.c2{left:330px;top:318px;background:var(--m)}
.c2 .nm{position:absolute;left:0;right:0;top:34px;text-align:center;font-size:46px;letter-spacing:8px;color:var(--om);line-height:1}
.c2 .yb{position:absolute;left:0;right:0;bottom:0;height:36px;background:var(--y)}
.c2 .yt{position:absolute;left:0;right:0;bottom:9px;text-align:center;font-size:13px;font-weight:700;color:var(--oy);letter-spacing:2px}
.rep{position:absolute;left:660px;top:30px;width:316px;height:446px;background:var(--paper);box-shadow:0 2px 8px rgba(0,0,0,.22);overflow:hidden}
.rep .top{position:absolute;left:0;right:0;top:0;height:140px;background:var(--m)}
.rep .yb{position:absolute;left:0;right:0;top:140px;height:16px;background:var(--y)}
.rep .k{position:absolute;left:22px;top:18px;font-size:13px;color:var(--om);letter-spacing:.1em;opacity:.9}
.rep .h{position:absolute;left:22px;top:42px;font-size:27px;line-height:1.3;color:var(--om)}
.cctv{position:absolute;left:22px;top:172px;width:272px;height:150px;overflow:hidden;
 background:radial-gradient(ellipse 60%% 62%% at 50%% 50%%,#0b0b0b 0 20%%,#3c372e 34%%,#7d7768 50%%,#4a453b 64%%,#1a1a1a 80%%)}
.cctv .b1,.cctv .b2{position:absolute;left:0;right:0;height:20px;background:var(--m);color:var(--y);font:700 10.5px/20px 'Noto Sans TC';padding-left:6px;letter-spacing:.03em;white-space:nowrap}
.cctv .b1{top:0}.cctv .b2{bottom:0}
.rep .row{position:absolute;left:22px;right:22px;font-size:14px;color:var(--ink);border-bottom:1px solid rgba(0,0,0,.15);padding:6px 0;display:flex;justify-content:space-between}
.rep .ft{position:absolute;left:22px;bottom:14px;font-size:15px;color:var(--ink);letter-spacing:1px}
.vest{position:absolute;left:636px;top:484px}
.gong{position:relative;display:inline-block;line-height:1;letter-spacing:0;margin-right:8px}.gong .g1{position:absolute;left:0;top:0;clip-path:inset(47%% 0 0 47%%)}
%(css)s
</style></head><body>'''
BODY='''<div class="lab" style="left:26px;top:8px">工地圍籬（縣市規定允許自訂時）</div>
<div class="fence"><div class="posts"></div>%(fence_extra)s<div class="nm kai">崧淳環保科技股份有限公司</div>
<div class="sub">污水下水道清淤及CCTV檢視工程</div>%(fence_y)s</div>
<div class="lab" style="left:26px;top:296px">名片　正面／背面</div>
<div class="card c1"><div class="bar"></div><div class="ybar"></div>%(c1_extra)s
<div class="nm kai">崧淳環保科技股份有限公司</div><div class="p kai">姓名　工地主任</div>
<div class="tx">污水下水道清淤及CCTV檢視工程</div><div class="tl"></div></div>
<div class="card c2">%(c2)s</div>
<div class="lab" style="left:662px;top:8px">CCTV 檢視報告封面</div>
<div class="rep"><div class="top"></div><div class="yb"></div>%(rep_extra)s
<div class="k">崧淳環保科技股份有限公司</div><div class="h kai">污水下水道<br>CCTV 管線檢視報告</div>
<div class="cctv"><div class="b1">2026-10-14　A12 → A13　順流</div>%(cctv_extra)s<div class="b2">Ø400　RCP　12.4 / 38.6 m</div></div>
<div class="row" style="top:334px"><span>管段</span><span>A12 → A13　Ø400</span></div>
<div class="row" style="top:366px"><span>檢視長度</span><span>38.6 m</span></div>
<div class="ft kai">崧淳環保科技股份有限公司</div></div>
<svg class="vest" width="350" height="116" viewBox="0 0 350 116"><g transform="translate(0,2)">
<path d="M20 8 L54 0 L66 22 L94 22 L106 0 L140 8 L150 110 L10 110 Z" fill="%(y)s" stroke="rgba(0,0,0,.25)"/>
<rect x="12" y="70" width="136" height="9" fill="#C9CCCF"/><rect x="11" y="90" width="138" height="9" fill="#C9CCCF"/>
<rect x="30" y="30" width="100" height="32" fill="%(m)s"/>%(vest_extra)s
<text x="80" y="54" text-anchor="middle" font-family="LXGW WenKai TC" font-weight="700" font-size="22" letter-spacing="4" fill="%(om)s">崧淳</text></g>
<text x="170" y="44" font-family="Noto Sans TC" font-size="13" fill="#55554F">背心背面：工程黃底</text>
<text x="170" y="64" font-family="Noto Sans TC" font-size="13" fill="#55554F">反光條＋主色名牌</text></svg>
</body></html>'''
def G(fs,base,hi): return f'<span class="gong kai" style="font-size:{fs}px"><span style="color:{base}">崧</span><span class="g1" style="color:{hi}">崧</span></span>'
def build(c):
    k=c['k']; d0=c['dir']; m=c['main'][1]; t=c['third'][1]; om=text_on(m)
    d=dict(m=m,y=Y,t=t,om=om,oy=DK,ot=text_on(t),css='',fence_extra='',c1_extra='',rep_extra='',cctv_extra='',vest_extra='',
           fence_y='<div class="yb"></div><div class="yt">施工中　人孔作業　請小心通行</div>',
           c2='<div class="nm kai">崧淳</div><div class="yb"></div><div class="yt">清淤　CCTV管線檢視</div>')
    if d0=='d1':
        d['fence_extra']=f'<div style="position:absolute;right:30px;top:22px;z-index:3">{G(96,om,Y)}</div>'
        d['c2']=f'<div class="nm kai">{G(46,om,Y)}<span style="font-size:46px">淳</span></div><div class="yb"></div><div class="yt">崧＝山＋松　松裡有公</div>'
        if k=='d1a':
            d['css']='.fence .gb{position:absolute;left:0;right:0;bottom:60px;height:14px;background:var(--t);z-index:2}.chips{position:absolute;left:22px;top:404px;display:flex;gap:6px;align-items:center;font-size:15px;color:var(--ink)}.chips b{display:inline-block;padding:1px 7px;border-radius:3px}.rep .ft{display:none}'
            d['fence_y']='<div class="gb"></div>'+d['fence_y']
            d['rep_extra']=f'<div class="chips kai"><b style="background:var(--t);color:#fff">山</b>＋<b style="background:var(--m);color:#fff">木</b>＋<b style="background:var(--y)">公</b>＝崧</div>'
        else:
            d['css']='.seal{position:absolute;width:58px;height:58px;background:var(--t);border-radius:5px;box-shadow:inset 0 0 0 3px var(--t),inset 0 0 0 5px #F6F1E6;color:#F6F1E6;display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:21px;line-height:1.05;transform:rotate(-4deg)}'
            d['rep_extra']='<div class="seal kai" style="right:22px;bottom:12px"><span>崧</span><span>淳</span></div>'
            d['c1_extra']='<div class="seal kai" style="right:16px;top:58px;width:44px;height:44px;font-size:15px"><span>崧</span><span>淳</span></div>'
    if d0=='d2':
        d['css']='.fence .y0{position:absolute;left:0;right:0;top:0;height:20px;background:var(--y);z-index:2}.fence .nm{top:40px}.fence .sub{top:96px}.c2 .y0{position:absolute;left:0;right:0;top:0;height:12px;background:var(--y)}.rep .y0{position:absolute;left:0;right:0;top:0;height:16px;background:var(--y);z-index:2}.rep .k{top:30px}.rep .h{top:52px}.tline{position:absolute;left:0;right:0;z-index:2;background:var(--t)}'
        d['fence_extra']='<div class="y0"></div>'
        d['rep_extra']='<div class="y0"></div><div class="tline" style="top:132px;height:8px"></div>'
        d['fence_y']='<div class="tline" style="bottom:60px;height:12px"></div>'+d['fence_y']
        d['c2']='<div class="y0"></div><div class="nm kai"><span style="color:var(--y)">崧</span><span style="color:#fff">淳</span></div><div class="tline" style="bottom:36px;height:6px"></div><div class="yb"></div><div class="yt">崧有山　淳有水</div>'
    if d0=='d3':
        d['css']='.fence .ov{position:absolute;left:0;right:0;top:128px;height:36px;background:rgba(0,0,0,.38);color:var(--y);font:700 16px/34px "Noto Sans TC";padding-left:30px;z-index:3;letter-spacing:.06em;border-bottom:2px solid var(--y)}.cctv{top:166px;height:166px}.rep .row:first-of-type{display:none}'
        d['fence_extra']='<div class="ov">管段 A12 → A13　Ø400　檢視中</div>'
        d['c2']='<div class="nm kai" style="color:var(--y)">崧淳</div><div style="position:absolute;left:0;right:0;bottom:36px;height:6px;background:var(--t)"></div><div class="yb"></div><div class="yt">清淤　CCTV管線檢視</div>'
        if k=='d3a':
            d['cctv_extra']='<div style="position:absolute;left:150px;top:60px;width:46px;height:42px;border:3px solid var(--t)"></div><div style="position:absolute;left:200px;top:64px;background:var(--t);color:#111;font:700 11px/18px Noto Sans TC;padding:0 5px">裂縫 12.4m</div>'
        else:
            d['cctv_extra']='<div style="position:absolute;right:8px;top:28px;background:var(--t);color:#111;font:700 12px/20px Noto Sans TC;padding:0 7px">✓ 管段合格</div>'
    if d0=='d4':
        if k=='d4a':
            d['css']='.fence .sb{position:absolute;left:0;right:0;bottom:60px;height:18px;background:var(--t);z-index:2}.rep .sb{position:absolute;left:0;right:0;top:132px;height:8px;background:var(--t)}'
            d['fence_y']='<div class="sb"></div>'+d['fence_y']; d['rep_extra']='<div class="sb"></div>'
            d['c2']='<div class="nm kai">崧淳</div><div style="position:absolute;left:0;right:0;bottom:36px;height:8px;background:var(--t)"></div><div class="yb"></div><div class="yt">清淤　CCTV管線檢視</div>'
        else:
            d['om']=t
            d['css']='.fence .db{position:absolute;left:0;right:0;bottom:0;height:22px;background:var(--t);z-index:2}.fence .yb{bottom:22px;height:54px}.fence .yt{bottom:32px}.rep .db{position:absolute;left:0;right:0;bottom:0;height:10px;background:var(--t)}.rep .ft{bottom:22px}'
            d['fence_y']='<div class="yb"></div><div class="db"></div><div class="yt">施工中　人孔作業　請小心通行</div>'; d['rep_extra']='<div class="db"></div>'
    html=HEAD%d+BODY%d
    p=f'{OUT}/{k}_docs.html'; open(p,'w').write(html); return p
if __name__=='__main__':
    for c in combos(): print(build(c))
