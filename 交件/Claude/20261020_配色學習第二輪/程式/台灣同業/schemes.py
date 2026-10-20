# 配色方式分組：沿用上一輪規則
#  0 個彩色 → 只有黑白灰；1 個 → 一個彩色加黑白灰；4 個以上 → 四色以上
#  2–3 個 → 看兩兩 OKLCH 色相差的最大值：≤45 同色系、45–90 相鄰、>90 對比
import sys, json, itertools
sys.path.insert(0,'/tmp/claude-0/r2/tw/work')
from ct import oklch, hue_diff, lab
def max_hue_diff(cols):
    hs=[oklch(c)[2] for c in cols]
    return max(hue_diff(a,b) for a,b in itertools.combinations(hs,2))
def scheme(cols, rule='maxpair'):
    n=len(cols)
    if n==0: return '只有黑白灰'
    if n==1: return '一個彩色'
    if n>=4: return '四色以上'
    if rule=='maxpair': d=max_hue_diff(cols)
    elif rule=='first2':  d=hue_diff(oklch(cols[0])[2],oklch(cols[1])[2])
    elif rule=='minspan':  # 色相在色環上最小涵蓋弧長
        hs=sorted(oklch(c)[2] for c in cols); gaps=[(hs[(i+1)%n]-hs[i])%360 for i in range(n)]
        d=360-max(gaps)
    if d<=45: return '同色系'
    if d<=90: return '相鄰'
    return '對比'
ORDER=['一個彩色','同色系','相鄰','對比','四色以上','只有黑白灰']
if __name__=='__main__':
    d=json.load(open('/tmp/claude-0/work/peer_schemes.json'))
    import collections
    for rule in ['maxpair','first2','minspan']:
        cnt=collections.Counter(scheme(x['cols'],rule) for x in d)
        print(rule,[ (k,cnt[k]) for k in ORDER])
    print()
    for x in d:
        if len(x['cols'])>=2:
            hs=[round(oklch(c)[2]) for c in x['cols']]
            print(f"{x['name'][:18]:18s} 原標:{x['t']:6s} 色相{hs} 最大差{max_hue_diff(x['cols']):.0f} → {scheme(x['cols'])}")
