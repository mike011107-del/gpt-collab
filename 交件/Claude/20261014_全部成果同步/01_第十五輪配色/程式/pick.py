import sys,json; sys.path.insert(0,'.')
from refs import *
PEER=[(n,h) for n,h in COMP]; OLDL=OLD
def ok_dist(h,old_min,peer_min,site_min,ban_min,extra=[]):
    o=min(de2000(h,r) for n,r in OLDL); p=min(de2000(h,r) for n,r in PEER)
    s=min(de2000(h,r) for n,r in SITE); b=min(de2000(h,r) for n,r in BAN)
    e=min([de2000(h,r) for r in extra] or [99])
    return o>=old_min and p>=peer_min and s>=site_min and b>=ban_min and e>=14, (o,p,s,b,e)
def pick(target,old_min=7,peer_min=8,site_min=8,ban_min=8,extra=[]):
    L0,C0,H0=target; best=None
    for dL in range(-12,13):
      for dC in range(-6,7):
        for dH in range(-20,21,2):
          L=L0+dL/100; C=max(0.004,C0+dC/200); H=H0+dH
          h,ok=oklch_hex(L,C,H)
          if not ok: continue
          good,ds=ok_dist(h,old_min,peer_min,site_min,ban_min,extra)
          if not good: continue
          cost=(dL/100)**2*4+(dC/200)**2*30+(dH/180)**2
          if best is None or cost<best[0]: best=(cost,h,round(L,2),round(C,3),H,[round(x,1) for x in ds])
    return best
if __name__=='__main__':
    T={'1松墨':(.38,.06,170),'2冰水':(.90,.035,215),'3監看墨藍':(.30,.045,240),'5灰藍':(.62,.045,240),
       '6鋼灰':(.68,.015,220),'7水青':(.48,.085,212),'8翡翠':(.70,.10,163)}
    chosen=['#14A5B3']
    for k,t in T.items():
        b=pick(t,extra=chosen)
        if b is None: b=pick(t,old_min=5,peer_min=7,site_min=7,extra=chosen); k+='(放寬)'
        print(k,b); 
        if b: chosen.append(b[1])
