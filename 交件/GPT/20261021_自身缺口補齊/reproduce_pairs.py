"""Read numeric source tables; independently evaluate published pair formula.
No upstream program is imported or executed. No total score for three-colour logos.
"""
from pathlib import Path
import math,json,re,hashlib,sys
import numpy as np

ROOT=Path(__file__).resolve().parent
SRC=ROOT/'sources'/'src'/'model'/'c'
def array(path,name):
 t=path.read_text(encoding='utf-8')
 m=re.search(re.escape(name)+r'\s*\[\s*\d*\s*\]\s*=\s*\{([^}]+)\}',t,re.S)
 if not m: raise ValueError(name)
 return np.array([float(v) for v in m.group(1).replace('NAN','nan').split(',') if v.strip()])
GRID=array(SRC/'util'/'labList.c','COLORGORICAL_LAB').reshape(-1,3)
COOL=array(SRC/'util'/'labToCoolness.c','COLORGORICAL_LAB_TO_COOLNESS')
assert len(GRID)==8325 and len(COOL)==33516
def lin(v):
 x=v/255
 return x/12.92 if x<=.040449936 else ((x+.055)/1.055)**2.4
def lab(h):
 r,g,b=(lin(int(h[i:i+2],16))*100 for i in (1,3,5))
 xyz=[.41233895*r+.35762064*g+.18051042*b,.2126*r+.7152*g+.0722*b,.01932141*r+.11916382*g+.95034478*b]
 def f(x):return x**(1/3) if x>216/24389 else ((24389/27)*x+16)/116
 x,y,z=[f(v/w) for v,w in zip(xyz,[95.047,100,108.883])]
 return (116*y-16,500*(x-y),200*(y-z))
def snap(h):
 p=np.array(lab(h));i=int(np.argmin(np.sum((GRID-p)**2,axis=1)))
 return tuple(int(v) for v in GRID[i])
def ill_c(p):
 l,a,b=p
 def inv(t):return t**3 if t>6/29 else 3*(6/29)**2*(t-4/29)
 def f(t):return t**(1/3) if t>(6/29)**3 else (29/6)**2*t/3+4/29
 x=95.047*inv((l+16)/116+a/500);y=100*inv((l+16)/116);z=108.883*inv((l+16)/116-b/200)
 fy=f(y/100)
 return (116*fy-16,500*(f(x/98.074)-fy),200*(fy-f(z/118.232)))
def index(p):
 l,a,b=p
 return (l//5)*38*42+((a+85)//5)*42+((b+110)//5)
def contrast(a,b):
 def luminance(h):return sum(lin(int(h[i:i+2],16))*w for i,w in zip((1,3,5),(.2126,.7152,.0722)))
 x,y=sorted([luminance(a),luminance(b)]);return (y+.05)/(x+.05)
def hue_delta(a,b,wrapped):
 d=abs(a-b)
 return min(d,360-d) if wrapped else d
def pair(a,b,wrapped=False):
 ga,gb=snap(a),snap(b)
 if (ga[1:]==(0,0)) or (gb[1:]==(0,0)):raise ValueError('achromatic table intentionally not implemented')
 x,y=ill_c(ga),ill_c(gb)
 hs=[math.degrees(math.atan2(p[2],p[1]))%360 for p in (x,y)]
 dl=abs(x[0]-y[0]);dh=hue_delta(*hs,wrapped)
 c=[float(COOL[index(g)]) for g in (ga,gb)]
 terms=[47.6133*dl/63.3673,-46.4222*(dh-.033547949)/(179.266981384-.033547949),75.1481*(sum(c)-4)/32]
 return {'value':sum(terms),'grids':[ga,gb],'hue_difference':dh,'terms':terms,'coolness':c}

def main():
 source=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'reference_pairs.json'
 old=json.loads(source.read_text(encoding='utf-8'))
 rows=[]
 candidates=list(old['targets_pair'].items())+[(r['name']+f'_{i}',r) for i,r in enumerate(old['peer_pairs'])]
 for name,r in candidates:
  if r['pp_parts']['path']!='chromatic':continue
  a,b=r['a'],r['b'];x=pair(a,b);w=pair(a,b,True)
  rows.append({'id':name,'a':a,'b':b,'original':x,'wrapped_comparison':w,'claude_original':r['pp_code'],'claude_wrapped':r['pp_wrapped'],'error_original':x['value']-r['pp_code'],'error_wrapped':w['value']-r['pp_wrapped'],'contrast':contrast(a,b)})
 checks={
  'all_reported_scores_match_2_decimals':all(abs(r['error_original'])<=.0051 and abs(r['error_wrapped'])<=.0051 for r in rows),
  'all_scores_finite':all(math.isfinite(r['original']['value']) for r in rows),
  'pair_order_symmetry':all(abs(pair(r['a'],r['b'])['value']-pair(r['b'],r['a'])['value'])<1e-10 for r in rows),
  'wrapped_never_exceeds_180':all(r['wrapped_comparison']['hue_difference']<=180 for r in rows),
  'wrap_boundary_350_10_is_20':hue_delta(350,10,True)==20,
  'original_boundary_350_10_is_340':hue_delta(350,10,False)==340,
  'contrast_black_white_21':abs(contrast('#000000','#FFFFFF')-21)<1e-12,
  'contrast_same_is_1':contrast('#0C424A','#0C424A')==1,
  'achromatic_pair_rejected_instead_of_fabricated':False,
 }
 try:pair('#FFFFFF','#0C424A')
 except ValueError:checks['achromatic_pair_rejected_instead_of_fabricated']=True
 assert all(checks.values()),checks
 result={'method':'independent arithmetic from pinned numeric source tables; chromatic pairs only','upstream':'connorgr/colorgorical@90649656a57ce9743b00390473adce51a821cadc','source_json_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'pairs_recomputed':len(rows),'checks':checks,'targets':rows[:2],'peer_pairs':rows[2:],'limitations':['No achromatic lookup or preference normalization reproduced','Wrapped hue is a comparison variant, not certified author correction','No three-colour aggregate, audience acceptance, beauty or recognition score']}
 (ROOT/'pair_reproduction.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({'pairs_recomputed':len(rows),'checks':checks,'targets':[{k:r[k] for k in ['id','error_original','error_wrapped','contrast']} for r in rows[:2]]},ensure_ascii=False))
if __name__=='__main__':main()
