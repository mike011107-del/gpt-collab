import json,sys
sys.argv=['x']
import check as C
from cl import wx,FAV,VW
A=json.load(open('同業色_A_原程式53色.json'))['colors']
Y='#FACA30'; DK='#111417'; WH='#FFFFFF'
def fate(h):
    w=wx(h); return sum(VW[k]*sum(s*FAV[k][e] for e,s in w.items()) for k in VW)
def fate30(pairs):
    tot=sum(p for _,p in pairs); f=sum(fate(h)*p for h,p in pairs)/tot; return round((f+1)/1.88*30,1)
UNIQ={'1':10,'2':9,'3':5,'4':4}
def score(k,m,t,share):
    g={'colors':[{'hex':m,'share':share[0]},{'hex':Y,'share':share[1]},{'hex':t,'share':share[2]}]}
    o=C.evaluate(g,Y,A,'std',DK,WH)
    mk=o['同行']+o['誤認']+o['遠看']+o['色弱']+UNIQ[k[0]]
    f=fate30([(m,share[0]),(Y,share[1]),(t,share[2])])
    return dict(fate=f,market=round(mk,1),total=round(f+mk,1),detail={x:o[x] for x in ('同行','誤認','遠看','色弱','誤認扣分','同行最近')})
