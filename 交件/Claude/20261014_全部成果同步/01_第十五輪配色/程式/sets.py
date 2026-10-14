import sys,json; sys.path.insert(0,'.')
from refs import *
Y='#FACA30'   # 工程黃 RAL 1018 鋅黃
SETS=[
 dict(k='s1',name='崧字裡的「公」',main=('松墨','#395848'),third=('青石灰','#C9D3D0'),share=(60,25,15)),
 dict(k='s2',name='鬆、沖、純',main=('冰水','#C5E5EC'),third=('淤墨','#25312B'),share=(55,25,20)),
 dict(k='s3',name='CCTV 字幕條',main=('監看墨藍','#081C2F'),third=('缺陷紅','#F05A6E'),share=(60,30,10)),
 dict(k='s4',name='工地上沒人用的顏色',main=('空位青','#14A5B3'),third=('反光銀','#CED2D3'),share=(60,30,10)),
 dict(k='s5',name='跟人孔蓋同一本色卡',main=('灰藍','#6E8A9F'),third=('人孔棕','#9A6B4B'),share=(60,25,15)),
 dict(k='s6',name='黃車照舊，冷色上名牌',main=('鋼灰','#96ADAE'),third=('吸污管綠','#2E9E4F'),share=(40,50,10)),
 dict(k='s7',name='山管住水',main=('水青','#086A74'),third=('岩炭','#2E3236'),share=(50,40,10)),
 dict(k='s8',name='木生火、火生土',main=('翡翠','#5EB28C'),third=('火紅','#F34465'),share=(55,30,15)),
]
PEER=[(n,h) for n,h in COMP]
DK='#111417'; WH='#FFFFFF'
def text_on(h): return DK if cr(DK,h)>=cr(WH,h) else WH
def nearest(h,L): return min((de2000(h,r),n,r) for n,r in L)
def clamp(x): return max(0,min(1,x))
def market(s):
    m=s['main'][1]; t=s['third'][1]
    out={}
    # A 不撞同行 15
    dm=nearest(m,PEER)[0]; n15=sum(1 for _,r in PEER if de2000(m,r)<15)
    out['同行']=round(15*(0.5*clamp((dm-3)/12)+0.5*clamp(1-n15/6)),1); out['同行近色家數']=n15
    # B 不被認錯 20
    pen=[]; Lm,Cm,Hm=lch(m)
    d_cht=de2000(m,'#0069AA'); 
    if d_cht<15: pen.append(('像中華電信黃車配藍',8))
    elif d_cht<25 and 230<=Hm<=290: pen.append(('偏中華電信藍',4))
    if min(de2000(m,'#005E83'),de2000(m,'#1E5B8A'))<12: pen.append(('像業主告示牌藍',6))
    if min(de2000(m,'#308446'),de2000(m,'#2E8B57'))<12: pen.append(('像圍籬綠或台南垃圾車',5))
    if Lm>85: pen.append(('大面積淺色，遠看可能像白色回收車',4))
    if s['share'][1]>=50: pen.append(('車身以黃為主，跟同行黃車、台電車、工程警示車同一路',7))
    if min(de2000(t,'#DA530A'),de2000(t,'#F82F22'))<12: pen.append(('第三色靠近交維橙',3))
    out['誤認']=round(max(0,20-sum(p for _,p in pen)),1); out['誤認扣分']=pen
    # C 遠看 15：主色與工程黃的亮度對比，含霧中
    tx=text_on(m)
    pairs=[(m,Y),(m,t),(Y,t),(m,tx)]
    best=max(pairs,key=lambda p:cr(*p)); r=cr(*best); rf=cr(fog(best[0]),fog(best[1])); rmy=cr(m,Y)
    out['遠看']=round(15*(0.4*clamp((rmy-1.2)/3.8)+0.4*clamp((r-1.5)/6)+0.2*clamp((rf-1.1)/1.9)),1); out['對比']=dict(主黃=round(rmy,2),最強一對=round(r,2),霧中=round(rf,2))
    # D 色弱 10：三色兩兩在紅色弱、綠色弱下的最小色差
    mins=[]
    for kind in ('protan','deutan'):
        a,b,c=cvd(m,kind),cvd(Y,kind),cvd(t,kind)
        mins.append(min(de2000(a,b),de2000(a,c),de2000(b,c)))
    out['色弱']=round(10*clamp((min(mins)-5)/20),1); out['色弱最小ΔE']=round(min(mins),1)
    return out
if __name__=='__main__':
    for s in SETS:
        m=s['main'][1]; t=s['third'][1]; sh=s['share']
        f30,f=fate30([(m,sh[0]),(Y,sh[1]),(t,sh[2])])
        mk=market(s); sub=mk['同行']+mk['誤認']+mk['遠看']+mk['色弱']
        print(f"{s['k']} {s['name']} {m}/{Y}/{t} 命格{f30}/30  市場(未含專屬10){sub:.1f}/60  {mk}")
        for lab_,h in (('主',m),('三',t)):
            print('   ',lab_,h,'同行',[round(x,1) if isinstance(x,float) else x for x in nearest(h,PEER)],'工地',[round(x,1) if isinstance(x,float) else x for x in nearest(h,SITE)][:2],'禁',[round(x,1) if isinstance(x,float) else x for x in nearest(h,BAN)][:2],'舊',[round(x,1) if isinstance(x,float) else x for x in nearest(h,OLD)],'RAL',nearest_ral(h)[0][:3])
