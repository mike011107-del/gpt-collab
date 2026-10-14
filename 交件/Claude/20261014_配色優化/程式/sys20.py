"""第二十輪：配色優化成 CIS 色彩系統。
方法來源（GitHub 原文已讀）：
- Material Color Utilities：用明度（tone）差控制對比，色相、彩度另外處理。
- Lyft coloralgorithm（ColorBox）：色階不是只改明度，色相與彩度沿明暗走曲線。
- Huetone（受 Stripe 2019 啟發）：不同色相的同一階要有同樣明度，對比才可預測。
- Tailwind v4 OKLCH 色階：黃色變深時色相往橙褐走（102°→54°），不會變成髒黃。
"""
import json
from ok import *
from ramp import ramp, neutral, STEPS
Y='#FACA30'
DIRS={
 '1':dict(name='崧裡有公',main_name='松針綠',orig='#395848',main='#1E5D46',hl=150,hd=172,nh=140),
 '2':dict(name='山管住水',main_name='水青',orig='#086A74',main='#086A74',hl=198,hd=214,nh=230),
 '3':dict(name='CCTV 字幕條',main_name='監看墨藍',orig='#081C2F',main='#081C2F',hl=240,hd=None,nh=250),
 '4':dict(name='路上沒人用的青',main_name='空位青',orig='#14A5B3',main='#14A5B3',hl=198,hd=214,nh=214),
}
THIRD={
 '1A':dict(name='山岩灰',hex='#909586',role='中性色系的一階（不另當第三色）：分隔線、次要字的底色系'),
 '1B':dict(name='印泥紅',hex='#B8283A',role='點綴，面積 5% 以內：只用在「公」字或細線；不做仿印章、不單獨表示意思'),
 '2A':dict(name='岩炭',hex='#2E3236',role='深色系：正文、車身下緣、字幕條'),
 '2B':dict(name='杏',hex='#F2A07B',role='淺色點綴：文件重點列底色，上面一律深字'),
 '3A':dict(name='缺陷紅',hex='#F05A6E',role='只做 CCTV 判讀狀態：缺陷標記，一律加文字'),
 '3B':dict(name='合格綠',hex='#3CCB7F',role='只做 CCTV 判讀狀態：合格標記，一律加文字'),
 '4A':dict(name='反光銀',hex='#CED2D3',role='中性色系的一階（淺）：分區底色；不叫「反光」，印刷不會反光'),
 '4B':dict(name='深墨',hex='#1B2A30',role='深色系：正文、字幕條、車身下緣'),
}
SHARE={'1':(60,28,12),'2':(50,40,10),'3':(62,30,8),'4':(58,32,10)}
NLOCK={'1A':'#909586','4A':'#CED2D3'}
def build(d,g=None):
    D=DIRS[d]
    mr,mstep=ramp(D['main'],hue_light=D['hl'],hue_dark=D['hd'])
    yr,ystep=ramp(Y,hue_light=102,hue_dark=58,cdark=0.75)
    nr=neutral(D['nh'])
    if g in NLOCK: nr,_=ramp(NLOCK[g],cmin=0.5,cdark=0.9)
    M=dict(mr); YY=dict(yr); N=dict(nr)
    # 角色
    ink=N[950]; paper=N[50]
    on_main='#FFFFFF' if cr('#FFFFFF',D['main'])>=4.5 else M[950]
    deep=M[800] if cr(Y,M[800])>=4.5 else M[900]
    if d=='3': deep=D['main']
    if g=='4B': deep=THIRD['4B']['hex']
    T=dict(
      主色=D['main'], 主色深=deep, 主色淺=M[100], 主色上的字=on_main,
      工程黃=Y, 黃上的字=M[950] if cr(M[950],Y)>=7 else ink, 黃淺=YY[100], 黃深_白底小字=YY[700] if cr(YY[700],paper)>=4.5 else YY[800],
      紙=paper, 分區=N[100], 邊線=N[300], 次要字=N[600] if cr(N[600],paper)>=4.5 else N[700], 正文=ink)
    return dict(main_ramp=mr,main_step=mstep,yellow_ramp=yr,yellow_step=ystep,neutral=nr,tokens=T)
def pairs(T):
    P=[('主色上的字','主色',4.5),('工程黃','主色深',4.5),('黃上的字','工程黃',7),('正文','紙',7),('次要字','紙',4.5),('黃深_白底小字','紙',4.5),('正文','分區',7),('正文','黃淺',7),('正文','主色淺',7)]
    return [dict(字=a,底=b,字色=T[a],底色=T[b],比值=round(cr(T[a],T[b]),2),門檻=th,過=cr(T[a],T[b])>=th) for a,b,th in P]
if __name__=='__main__':
    out={}
    for g in THIRD:
        d=g[0]; s=build(d,g); s['pairs']=pairs(s['tokens']); out[g]=s
        print(g,DIRS[d]['name'],'主色在',s['main_step'],'階');
        for k,v in s['tokens'].items(): print('  ',k,v)
        for p in s['pairs']: print('   ',p['字'],'/',p['底'],p['比值'],'✓' if p['過'] else '✗')
    json.dump(dict(dirs=DIRS,third=THIRD,share=SHARE,system=out),open('system.json','w'),ensure_ascii=False,indent=1)
