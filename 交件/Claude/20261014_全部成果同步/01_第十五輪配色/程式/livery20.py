"""第二版：4 個方向 × 2 種第三色，畫在真車照片上（側面 33e7029f、車隊 49f29896）。
所有組都保留黃色車頭（民眾已認得黃車），罐身寫法定全名。"""
import sys,json; S='/tmp/claude-0/-home-claude/f822ab78-49b8-5e2f-8fbe-8111b065c404/scratchpad'
sys.path.insert(0,S+'/r18'); sys.path.insert(0,S+'/r19')
import livery2 as L
from combos import combos
from sets import Y
C={c['k']:c for c in combos()}
def M(k): return C[k]['main'][1]
def T(k): return C[k]['third'][1]
CH='#2B2D2F'; WH='#FFFFFF'; DK='#111417'; O=S+'/r19/out20'
SPEC={
 # 方向一 崧裡有公：松針綠罐身、白字；車門貼「崧」字，公是黃色（A）或紅色印章（B）
 'd1a':dict(cab=Y,tower=M('d1a'),tank=M('d1a'),split=624,low=T('d1a'),rear=Y,text=WH,chassis=CH,
            decal=[O+'/d1a_decal.png',412,592,52],van=M('d1a'),vanlow=Y,vansplit=662,vantext=WH),
 'd1b':dict(cab=Y,tower=M('d1b'),tank=M('d1b'),split=632,low=Y,rear=Y,text=WH,chassis=CH,
            decal=[O+'/d1b_decal.png',414,592,50],van=M('d1b'),vanlow=Y,vansplit=662,vantext=WH),
 # 方向二 山管住水：黃色上下框住水青罐身
 'd2a':dict(cab=Y,tower=T('d2a'),tank=M('d2a'),rear=Y,bands=[[Y,497,526],[T('d2a'),624,638],[Y,638,662]],text=WH,chassis=T('d2a'),
            cabbands=[[T('d2a'),640,700]],van=M('d2a'),vanlow=Y,vansplit=662,vanbands=[[T('d2a'),656,662]],vantext=WH),
 'd2b':dict(cab=Y,tower=Y,tank=M('d2b'),rear=Y,bands=[[Y,497,526],[T('d2b'),526,534],[T('d2b'),624,638],[Y,638,662]],text=WH,chassis=CH,
            van=M('d2b'),vanlow=Y,vansplit=662,vanbands=[[T('d2b'),656,662]],vantext=WH),
 # 方向三 CCTV 字幕條：罐身像放大的字幕條，墨藍底黃字
 'd3a':dict(cab=Y,tower=M('d3a'),tank=M('d3a'),rear=M('d3a'),bands=[[T('d3a'),626,636]],text=Y,chassis=CH,
            van=M('d3a'),vanlow=Y,vansplit=664,vanbands=[[T('d3a'),658,664]],vantext=Y),
 'd3b':dict(cab=Y,tower=M('d3b'),tank=M('d3b'),rear=M('d3b'),bands=[[T('d3b'),626,636]],text=Y,chassis=CH,
            van=M('d3b'),vanlow=Y,vansplit=664,vanbands=[[T('d3b'),658,664]],vantext=Y),
 # 方向四 路上沒人用的青：深字
 'd4a':dict(cab=Y,tower=M('d4a'),tank=M('d4a'),rear=Y,bands=[[T('d4a'),622,636]],text=DK,chassis=CH,
            van=M('d4a'),vanlow=Y,vansplit=664,vanbands=[[T('d4a'),654,664]],vantext=DK),
 'd4b':dict(cab=Y,tower=M('d4b'),tank=M('d4b'),split=630,low=T('d4b'),rear=Y,text=T('d4b'),chassis=T('d4b'),
            cabbands=[[T('d4b'),640,700]],van=M('d4b'),vanlow=T('d4b'),vansplit=662,vantext=T('d4b')),
}
if __name__=='__main__':
    ks=sys.argv[1:] or list(SPEC)
    for k in ks:
        L.side(SPEC[k],f'{O}/{k}_side.jpg'); L.fleet(SPEC[k],f'{O}/{k}_fleet.jpg'); print(k)
