import sys,json; sys.path.insert(0,'.')
from sets import *
DIRS={
 'd1':dict(name='崧裡有公',main=('松針綠','#395848')),
 'd2':dict(name='山管住水',main=('水青','#086A74')),
 'd3':dict(name='CCTV 字幕條',main=('監看墨藍','#081C2F')),
 'd4':dict(name='路上沒人用的青',main=('空位青','#14A5B3')),
}
THIRDS={
 'd1a':('山岩灰','#909586','穩重'),'d1b':('印泥紅','#B8283A','命格'),
 'd2a':('岩炭','#2E3236','穩重'),'d2b':('杏','#F2A07B','命格'),
 'd3a':('缺陷紅','#F05A6E','命格'),'d3b':('合格綠','#3CCB7F','清爽'),
 'd4a':('反光銀','#CED2D3','清爽'),'d4b':('深墨','#1B2A30','穩重'),
}
SHARE={'d1':(60,28,12),'d2':(50,40,10),'d3':(62,30,8),'d4':(58,32,10)}
UNIQ={'d1':10,'d2':9,'d3':5,'d4':4}
def combos():
    out=[]
    for k,(tn,th,mood) in THIRDS.items():
        d=k[:2]; D=DIRS[d]
        out.append(dict(k=k,dir=d,name=D['name'],main=D['main'],third=(tn,th),mood=mood,share=SHARE[d]))
    return out
def score(c):
    m=c['main'][1]; t=c['third'][1]; sh=c['share']
    f30,f=fate30([(m,sh[0]),(Y,sh[1]),(t,sh[2])]); mk=market(c)
    sub=mk['同行']+mk['誤認']+mk['遠看']+mk['色弱']
    return dict(fate30=round(f30),market70=round(sub+UNIQ[c['dir']]),detail=mk)
if __name__=='__main__':
    res={}
    for c in combos():
        s=score(c); res[c['k']]=dict(c,**s,ral_main=nearest_ral(c['main'][1])[0][1:3],ral_third=nearest_ral(c['third'][1])[0][1:3])
        print(c['k'],c['name'],c['third'][0],'命格',s['fate30'],'市場',s['market70'],'合計',s['fate30']+s['market70'],{k:v for k,v in s['detail'].items() if k in('同行','誤認','誤認扣分','遠看','色弱')})
    json.dump(res,open('combos.json','w'),ensure_ascii=False,indent=1)
