import sys; sys.path.insert(0,'.')
from wm import *
from shapely.geometry import box, Point, Polygon, LineString
from shapely.ops import unary_union
F='../fontsrc/'
SANS=F+'NotoSansTC-Black.otf'; SANSB=F+'NotoSansTC-Bold.otf'; SERIF=F+'NotoSerifTC-Bold.otf'; KAI=F+'LXGWWenKaiTC-Medium.ttf'

def polys(g): return list(g.geoms) if g.geom_type=='MultiPolygon' else [g]
def chamfer(g,r): return g.buffer(-r,join_style='mitre').buffer(r,join_style='bevel')

def interval_at(g,y,x0,x1):
    """g 在高度 y、x0..x1 範圍內的黑色區間。"""
    inter=g.intersection(LineString([(x0,y),(x1,y)]))
    segs=[inter] if inter.geom_type=='LineString' else list(getattr(inter,'geoms',[]))
    return [tuple(sorted((s.coords[0][0],s.coords[-1][0]))) for s in segs if not s.is_empty]

def shan_high(g, ext, probe_dy=30, half=130):
    """崧：山的中豎往上多一截（保留原本的筆端形狀，整段往上搬）。"""
    minx,_,maxx,top=g.bounds; mid=(minx+maxx)/2
    t=None
    y=top
    while y>top-260:
        iv=interval_at(g,y,mid-half,mid+half)
        iv=[i for i in iv if i[1]-i[0]>20]
        if iv:
            t=y; break
        y-=2
    # 筆端往下 probe_dy 處量筆寬
    ivs=interval_at(g,t-probe_dy,mid-half,mid+half)
    iv=min(ivs,key=lambda i:abs((i[0]+i[1])/2-mid))
    pad=40
    cap=g.intersection(box(iv[0]-pad,t-probe_dy,iv[1]+pad,t+10))
    # 只留跟中豎相連的那塊
    cap=unary_union([p for p in polys(cap) if p.intersects(box(iv[0],t-probe_dy,iv[1],t-probe_dy+4))])
    moved=affinity.translate(cap,0,ext)
    body=g.difference(cap.buffer(0.5))
    return unary_union([body,moved,box(iv[0],t-probe_dy-1,iv[1],t-probe_dy+ext+1)]).buffer(0.3).buffer(-0.3), (iv,t)

def pill_counter(g):
    """淳：口的內框改成兩頭全圓（管）。"""
    out=[]
    for p in polys(g):
        if not p.interiors: out.append(p); continue
        keep=[]
        for i in p.interiors:
            hp=Polygon(i); a,b,c,d=hp.bounds
            if a>420:  # 口在右半
                h=d-b; r=h/2
                pill=box(a+r,b,c-r,d).union(Point(a+r,b+r).buffer(r,64)).union(Point(c-r,b+r).buffer(r,64))
                out.append(Polygon(p.exterior).difference(pill).difference(unary_union([Polygon(j) for j in p.interiors if j is not i])))
                break
        else:
            out.append(p)
    return unary_union(out)

def word(chars, gap):
    out=[];x=0
    for g in chars:
        minx,miny,maxx,maxy=g.bounds
        out.append(affinity.translate(g,x-minx,0)); x+=(maxx-minx)+gap
    return unary_union(out), x-gap

def W1(rev=False):
    s,_=glyph(SANS,'崧'); c,_=glyph(SANS,'淳')
    s,_iv=shan_high(s,62)
    r=24
    s=chamfer(s,r); c=chamfer(c,r)
    w,W=word([s,c],46)
    if rev: w=w.buffer(-5,join_style='mitre')
    return w,W
def W2(rev=False):
    s,_=glyph(SERIF,'崧'); c,_=glyph(SERIF,'淳')
    s,_iv=shan_high(s,64,probe_dy=110)
    w,W=word([s,c],30)
    if rev: w=w.buffer(-4)
    return w,W
def W3(rev=False):
    s,_=glyph(KAI,'崧'); c,_=glyph(KAI,'淳')
    s=s.buffer(18,join_style='mitre',mitre_limit=1.6); c=c.buffer(18,join_style='mitre',mitre_limit=1.6)
    s,_iv=shan_high(s,60,probe_dy=100)
    w,W=word([s,c],0)
    if rev: w=w.buffer(-6)
    return w,W
def PLAIN(path):
    s,_=glyph(path,'崧'); c,_=glyph(path,'淳'); return word([s,c],0)

if __name__=='__main__':
    html='<html><body style="margin:0;background:#fff;font-family:sans-serif">'
    for lab,(g,w) in [('W1',W1()),('W2',W2()),('W3',W3()),('sans plain',PLAIN(SANS)),('serif plain',PLAIN(SERIF)),('kai plain',PLAIN(KAI))]:
        s=svg([(to_path(g),None)],(-30,-960,w+60,1100))
        html+=f'<div style="display:inline-block;margin:10px;text-align:center">{s.replace("<svg ","<svg style=\"height:260px\" ",1)}<div>{lab}</div></div>'
    open('d1.html','w').write(html+'</body></html>')
