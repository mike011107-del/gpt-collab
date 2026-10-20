import sys, json, re
sys.path.insert(0,'/home/user/gpt-collab/.claude/skills/colour-tool/scripts')
import colourtool as ct
exec(open('ok.py').read().split('amber=')[0])
from PIL import Image, ImageCms
D='dl/'
pc=json.load(open(D+'x_pantonr-0.1.0/package/dist/pantone_coated.json'))
txt=open(D+'x_ral-colors-1.0.1/package/RAL/classic.js').read()
ral={m[0]:m[2] for m in re.findall(r"(RAL\d{4}): \{ description: '([^']*)',\s*HEX:\s*'(#[0-9A-Fa-f]{6})'",txt)}
raln={m[0]:m[1] for m in re.findall(r"(RAL\d{4}): \{ description: '([^']*)'",txt)}
srgb=ImageCms.createProfile('sRGB'); cmyk=ImageCms.getOpenProfile(D+'icc/default_cmyk.icc')
tr=ImageCms.buildTransform(srgb,cmyk,'RGB','CMYK',renderingIntent=1)
def tocmyk(h):
    im=Image.new('RGB',(1,1),tuple(int(h[i:i+2],16) for i in (1,3,5)))
    return [round(v/2.55) for v in ImageCms.applyTransform(im,tr).getpixel((0,0))]
pcs={v['name']:v['hex'] for v in pc.values()}
def near(h,t): return sorted((round(ct.de(h,v),1),k) for k,v in t.items())[0]
A={'primary':'#0C424A','deep':'#04272C','mid':'#447B85','light':'#CEE2E6','ink':'#222B2C','grey':'#788284','pale':'#D5DCDE','mist':'#F4F7F8'}
B={'primary':'#333D66','deep':hexof(0.25,0.05,272),'mid':hexof(0.55,0.08,272),'light':'#B6C5DF','ink':'#1B1F29','grey':hexof(0.60,0.012,272),'pale':hexof(0.89,0.008,272),'mist':hexof(0.975,0.004,272)}
Y={'yellow':'#D68702','ylight':'#FBE9CA','white':'#FFFFFF'}
out={}
for name,P in (('teal',A),('indigo',B),('shared',Y)):
  out[name]={}
  for k,h in P.items():
    p=near(h,pcs); r=near(h,ral)
    out[name][k]=dict(hex=h,rgb=[int(h[i:i+2],16) for i in (1,3,5)],cmyk=tocmyk(h),pantone=[p[1].replace('PANTONE ',''),p[0]],ral=[r[1].replace('RAL','RAL '),raln[r[1]],r[0]],
      white=round(ct.contrast(h,'#FFFFFF'),2),yellow=round(ct.contrast(h,'#D68702'),2))
for nm,P in (('teal',A),('indigo',B)):
  ink=P['ink']
  out[nm+'_pairs']={'白字/主色':round(ct.contrast('#FFFFFF',P['primary']),2),'黃/主色':round(ct.contrast('#D68702',P['primary']),2),'黃/深階':round(ct.contrast('#D68702',P['deep']),2),'墨字/黃':round(ct.contrast(ink,'#D68702'),2),'墨字/白':round(ct.contrast(ink,'#FFFFFF'),2),'主色字/白':round(ct.contrast(P['primary'],'#FFFFFF'),2),'灰字/白':round(ct.contrast(P['grey'],'#FFFFFF'),2),'主色字/淺階':round(ct.contrast(P['primary'],P['light']),2)}
out['white/yellow']=round(ct.contrast('#FFFFFF','#D68702'),2)
out['teal_vs_indigo_dE']=round(ct.de('#0C424A','#333D66'),2)
json.dump(out,open('palette_both.json','w'),ensure_ascii=False,indent=1)
for k,v in out.items(): print(k, json.dumps(v,ensure_ascii=False)[:900])
