"""第二十輪文件應用示意：拿掉無功能裝飾、字幕條改放主色深、新增白底內頁（管段檢視紀錄）。"""
import json,sys
S=json.load(open('system.json'))
def G(fs,base,hi): return f'<span class="gong kai" style="font-size:{fs}px"><span style="color:{base}">崧</span><span class="g1" style="color:{hi}">崧</span></span>'
CSS='''*{box-sizing:border-box}html,body{margin:0}
body{width:1000px;height:930px;background:#E9E8E4;font-family:'Noto Sans TC',sans-serif;position:relative;overflow:hidden;color:var(--ink)}
.kai{font-family:'LXGW WenKai TC',serif;font-weight:700}
.lab{position:absolute;font-size:13px;color:#55554F;letter-spacing:.05em}
.sh{box-shadow:0 2px 6px rgba(0,0,0,.18)}
.fence{position:absolute;left:24px;top:30px;width:610px;height:236px;background:var(--m);overflow:hidden}
.posts{position:absolute;inset:0;background:repeating-linear-gradient(90deg,transparent 0 150px,rgba(0,0,0,.08) 150px 152px)}
.fence .nm{position:absolute;left:28px;top:34px;font-size:34px;letter-spacing:3px;color:var(--om);white-space:nowrap}
.fence .sub{position:absolute;left:30px;top:92px;font-size:20px;color:var(--om);letter-spacing:2px;opacity:.92}
.fence .yb{position:absolute;left:0;right:0;bottom:0;height:60px;background:var(--y)}
.fence .yt{position:absolute;left:30px;bottom:15px;font-size:22px;font-weight:700;color:var(--oy);letter-spacing:1px}
.card{position:absolute;width:290px;height:174px;overflow:hidden}
.c1{left:24px;top:300px;background:var(--paper)}
.c1 .bar{position:absolute;left:0;top:0;bottom:0;width:16px;background:var(--m)}
.c1 .ybar{position:absolute;left:16px;top:0;bottom:0;width:7px;background:var(--y)}
.c1 .nm{position:absolute;left:40px;top:24px;font-size:19px;letter-spacing:1px}
.c1 .p{position:absolute;left:40px;top:62px;font-size:24px}
.c1 .tx{position:absolute;left:40px;top:106px;font-size:13px;color:var(--sub)}
.c1 .ct{position:absolute;left:40px;bottom:20px;font-size:12px;color:var(--sub);letter-spacing:.02em}
.c2{left:344px;top:300px;background:var(--m)}
.c2 .nm{position:absolute;left:0;right:0;top:36px;text-align:center;font-size:46px;letter-spacing:8px;color:var(--om);line-height:1}
.c2 .yb{position:absolute;left:0;right:0;bottom:0;height:36px;background:var(--y)}
.c2 .yt{position:absolute;left:0;right:0;bottom:9px;text-align:center;font-size:13px;font-weight:700;color:var(--oy);letter-spacing:2px}
.rep{position:absolute;left:660px;top:30px;width:316px;height:444px;background:var(--paper);overflow:hidden}
.rep .top{position:absolute;left:0;right:0;top:0;height:140px;background:var(--m)}
.rep .yb{position:absolute;left:0;right:0;top:140px;height:12px;background:var(--y)}
.rep .k{position:absolute;left:22px;top:18px;font-size:13px;color:var(--om);letter-spacing:.1em;opacity:.9}
.rep .h{position:absolute;left:22px;top:42px;font-size:27px;line-height:1.3;color:var(--om)}
.cctv{position:absolute;left:22px;top:170px;width:272px;height:156px;overflow:hidden;
 background:radial-gradient(ellipse 60% 62% at 50% 50%,#0b0b0b 0 20%,#3c372e 34%,#7d7768 50%,#4a453b 64%,#1a1a1a 80%)}
.cctv .b{position:absolute;left:0;right:0;height:20px;background:var(--deep);color:var(--y);font:700 10.5px/20px 'Noto Sans TC';padding-left:6px;letter-spacing:.03em;white-space:nowrap}
.rep .row{position:absolute;left:22px;right:22px;font-size:14px;border-bottom:1px solid var(--line);padding:6px 0;display:flex;justify-content:space-between}
.rep .row span:first-child{color:var(--sub)}
.rep .ft{position:absolute;left:22px;bottom:14px;font-size:14px;letter-spacing:1px;color:var(--sub)}
.pg{position:absolute;left:24px;top:510px;width:610px;height:396px;background:var(--paper);overflow:hidden}
.pg .hd{position:absolute;left:0;right:0;top:0;height:46px;border-bottom:3px solid var(--y);display:flex;align-items:center;padding:0 22px;justify-content:space-between}
.pg .hd b{font-size:16px;letter-spacing:1px}.pg .hd i{font-style:normal;font-size:12px;color:var(--sub)}
.pg .mk{width:10px;height:22px;background:var(--m);display:inline-block;margin-right:10px;vertical-align:-5px}
.pg table{position:absolute;left:22px;right:22px;top:66px;width:566px;border-collapse:collapse;font-size:13px}
.pg th{background:var(--zone);text-align:left;font-weight:700;padding:8px 8px;color:var(--ink);border-bottom:1px solid var(--line)}
.pg td{padding:8px 8px;border-bottom:1px solid var(--line);font-variant-numeric:tabular-nums}
.pg tr:nth-child(even) td{background:var(--zone2)}
.pg td.n{text-align:right}
.st{display:inline-block;padding:1px 8px;border-radius:3px;font-weight:700;font-size:12px}
.pg .note{position:absolute;left:22px;right:22px;bottom:58px;font-size:12px;color:var(--sub);line-height:1.6}
.pg .sig{position:absolute;left:22px;right:22px;bottom:16px;display:flex;gap:14px;font-size:12px;color:var(--sub)}
.pg .sig span{flex:1;border-top:1px solid var(--line);padding-top:5px}
.vest{position:absolute;left:676px;top:520px}
.gong{position:relative;display:inline-block;line-height:1;letter-spacing:0;margin-right:8px}.gong .g1{position:absolute;left:0;top:0;clip-path:inset(47% 0 0 47%)}
'''
def HEAD(root): return '<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=LXGW+WenKai+TC:wght@700&family=Noto+Sans+TC:wght@400;700&display=block" rel="stylesheet"><style>body{'+root+'}'+CSS+'</style></head><body>'
def status(g,T,kind):
    if g=='3A' and kind=='bad': return f'<span class="st" style="background:{S["third"]["3A"]["hex"]};color:#111">▲ 缺陷</span>'
    if g=='3B' and kind=='ok': return f'<span class="st" style="background:{S["third"]["3B"]["hex"]};color:#111">✓ 合格</span>'
    if kind=='bad': return f'<span class="st" style="background:var(--y);color:var(--oy)">▲ 缺陷</span>'
    return f'<span class="st" style="color:var(--m2);border:1px solid var(--line)">✓ 合格</span>'
def build(g,docname=None):
    s=S['system'][g]; T=s['tokens']; d=g[0]; th=S['third'][g]['hex']
    m=T['主色']; v=dict(m=m,y=T['工程黃'],om=T['主色上的字'],oy=T['黃上的字'],deep=T['主色深'],paper=T['紙'],zone=T['分區'],
        zone2=T['分區'] if g not in('2B',) else T['黃淺'],line=T['邊線'],sub=T['次要字'],ink=T['正文'],m2=m if d!='4' else T['主色深'],t=th)
    if g=='2B': v['zone2']=S['third']['2B']['hex']+'33'
    root=';'.join(f'--{k}:{x}' for k,x in v.items())
    extra=''
    fence_extra=''; c2=f'<div class="nm kai">崧淳</div><div class="yb"></div><div class="yt">清淤　CCTV管線檢視</div>'
    lower=''
    if d=='1':
        hi=T['工程黃']  # 1B 的印泥紅對松針綠只有 1.26，不放在綠底上
        fence_extra=f'<div style="position:absolute;right:30px;top:24px">{G(96,v["om"],hi)}</div>'
        c2=f'<div class="nm kai">{G(46,v["om"],hi)}<span style="font-size:46px">淳</span></div><div class="yb"></div><div class="yt">清淤　CCTV管線檢視</div>'
    if d=='2':
        lower=f'<div style="position:absolute;left:0;right:0;bottom:60px;height:10px;background:{T["主色深"] if g=="2B" else th}"></div>'
    if d=='3':
        fence_extra='<div style="position:absolute;left:0;right:0;top:132px;height:34px;background:rgba(0,0,0,.35);color:var(--y);font:700 15px/34px Noto Sans TC;padding-left:30px;letter-spacing:.06em">管段 A12 → A13　Ø400　檢視中</div>'
        c2='<div class="nm kai" style="color:var(--y)">崧淳</div><div class="yb"></div><div class="yt">清淤　CCTV管線檢視</div>'
    if g=='4B':
        lower=f'<div style="position:absolute;left:0;right:0;bottom:60px;height:10px;background:{th}"></div>'
    cctv_extra=''
    if d=='3':
        cctv_extra=f'<div style="position:absolute;left:150px;top:62px;width:46px;height:42px;border:3px solid {th}"></div><div style="position:absolute;left:200px;top:66px;background:{th};color:#111;font:700 11px/18px Noto Sans TC;padding:0 5px">{"裂縫 12.4m" if g=="3A" else "✓ 管段合格"}</div>'
    sh=S['share'][d]; nm=S['dirs'][d]['main_name']; tn=S['third'][g]['name']
    cols=[(m,sh[0],nm),(T['工程黃'],sh[1],'工程黃'),(th,sh[2],tn)]
    bar=''.join(f'<div style="flex:{p};background:{c}"></div>' for c,p,_ in cols)
    legend='　'.join(f'{n} {p}%' for c,p,n in cols)+'<br>紙、正文、邊線屬中性色系，不計入比例'
    rows=[('A12 → A13','400','RCP','38.6','bad','12.4 m 縱向裂縫'),('A13 → A14','400','RCP','41.2','ok',''),('A14 → A15','300','PVC','27.9','ok',''),('A15 → A16','300','PVC','33.5','bad','接頭錯位'),('A16 → A17','300','PVC','30.1','ok','')]
    trs=''.join(f'<tr><td>{a}</td><td class="n">Ø{b}</td><td>{c}</td><td class="n">{e} m</td><td>{status(g,T,k)}</td><td>{n}</td></tr>' for a,b,c,e,k,n in rows)
    if g=='1B':
        extra='<style>.c1 .nm{border-bottom:2px solid var(--t);padding-bottom:4px}.pg .mk{background:var(--t)}</style>'
    body=extra+f'''<div class="lab" style="left:26px;top:8px">工地圍籬</div>
<div class="fence sh"><div class="posts"></div>{fence_extra}<div class="nm kai">崧淳環保科技股份有限公司</div><div class="sub">污水下水道清淤及CCTV檢視工程</div>{lower}<div class="yb"></div><div class="yt">施工中　人孔作業　請小心通行</div></div>
<div class="lab" style="left:26px;top:280px">名片　正面／背面</div>
<div class="card c1 sh"><div class="bar"></div><div class="ybar"></div><div class="nm kai">崧淳環保科技股份有限公司</div><div class="p kai">姓名　工地主任</div><div class="tx">污水下水道清淤及CCTV檢視工程</div><div class="ct">電話　·　地址（待提供）</div></div>
<div class="card c2 sh">{c2}</div>
<div class="lab" style="left:662px;top:8px">CCTV 檢視報告　封面</div>
<div class="rep sh"><div class="top"></div><div class="yb"></div><div class="k">崧淳環保科技股份有限公司</div><div class="h kai">污水下水道<br>CCTV 管線檢視報告</div>
<div class="cctv"><div class="b" style="top:0">2026-10-14　A12 → A13　順流</div>{cctv_extra}<div class="b" style="bottom:0">Ø400　RCP　12.4 / 38.6 m</div></div>
<div class="row" style="top:338px"><span>管段</span><span>A12 → A13　Ø400</span></div><div class="row" style="top:370px"><span>檢視長度</span><span>38.6 m</span></div>
<div class="ft">崧淳環保科技股份有限公司</div></div>
<div class="lab" style="left:26px;top:490px">報告內頁　管段檢視紀錄（數值為示意）</div>
<div class="pg sh"><div class="hd"><b><span class="mk"></span>管段檢視紀錄</b><i>崧淳環保科技股份有限公司　第 3 頁</i></div>
<table><tr><th>管段</th><th>管徑</th><th>管材</th><th>長度</th><th>判讀</th><th>備註</th></tr>{trs}</table>
<div class="note">判讀依委託單位指定之分級標準；顏色只輔助辨識，判讀結果一律以文字記載。</div>
<div class="sig"><span>檢視人員</span><span>複核</span><span>日期</span></div></div>
<svg class="vest" width="300" height="200" viewBox="0 0 300 200"><text x="0" y="-4" font-size="13" fill="#55554F"></text>
<path d="M30 14 L74 2 L90 34 L130 34 L146 2 L190 14 L204 186 L16 186 Z" fill="{v['y']}" stroke="rgba(0,0,0,.25)"/>
<rect x="20" y="122" width="180" height="12" fill="#C9CCCF"/><rect x="18" y="152" width="184" height="12" fill="#C9CCCF"/>
<rect x="44" y="52" width="132" height="44" fill="{v['m']}"/>
<text x="110" y="83" text-anchor="middle" font-family="LXGW WenKai TC" font-weight="700" font-size="28" letter-spacing="5" fill="{v['om']}">崧淳</text></svg>
<div class="lab" style="left:676px;top:494px">背心背面</div>
<div class="lab" style="left:676px;top:742px">面積比例（車身與大型應用）</div>
<div style="position:absolute;left:676px;top:766px;width:300px;height:34px;display:flex" class="sh">{bar}</div>
<div style="position:absolute;left:676px;top:808px;width:300px;font-size:12px;color:#55554F;line-height:1.7">{legend}</div>
'''
    html=HEAD(root)+body+'</body></html>'
    p=f'out/{g}_docs.html'; open(p,'w').write(html); return p
if __name__=='__main__':
    for g in S['third']: print(build(g))
