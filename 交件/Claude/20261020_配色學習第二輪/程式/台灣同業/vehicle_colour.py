# 車身取色：在照片上框一塊車身，取中位色，跟該家 logo 色比 ΔE2000（框位置目視定，另存裁切圖核對）
import sys, json, numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0,'/tmp/claude-0/r2/tw/work')
from ct import de, oklch
U='/mnt/user-data/uploads/崧淳環保科技股份有限公司/崧淳同業logo/'; P='/tmp/claude-0/r2/tw/pdfimg/'
J=[('華通','槽體綠',P+'p05_017.png',(720,60,900,160),['#2D661F','#005959']),
   ('宏隆','槽體黃',U+'12_宏隆環保_車輛.jpg',(60,100,200,220),['#186504','#F55802']),
   ('一元','車身黃',U+'14_一元環保_車輛.jpg',(60,300,380,370),['#255092']),
   ('康立','車側布條藍',U+'13_康立衛生清潔工程_車輛.jpg',(120,60,500,140),['#566A1F']),
   ('大亞','車頭藍',U+'05_大亞環保_車輛.jpg',(600,420,760,560),['#243952','#AD3922']),
   ('派浦崴洱','槽體橘黃',P+'p06_020.png',(760,40,860,120),[]),
   ('日技','槽車黃',U+'11_日技管清工程_車輛.jpg',(110,150,170,175),['#0070C0','#EC1D24'])]
font=ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',16)
out=[]; strip=Image.new('RGB',(len(J)*170,190),(255,255,255)); d=ImageDraw.Draw(strip)
for i,(co,part,f,box,logo) in enumerate(J):
    im=Image.open(f).convert('RGB').crop(box); a=np.asarray(im).reshape(-1,3).astype(float)
    med='#%02X%02X%02X'%tuple(int(v) for v in np.median(a,axis=0))
    from measure import oklab_arr
    ok=oklab_arr(a); C=np.hypot(ok[:,1],ok[:,2]); m=C>=0.05
    q=np.floor(ok[m]/0.03).astype(int); u,inv,cn=np.unique(q,axis=0,return_inverse=True,return_counts=True)
    top=np.argmax(cn); mode='#%02X%02X%02X'%tuple(int(v) for v in a[m][inv.ravel()==top].mean(axis=0))
    chrom_share=round(float(m.mean()),3)
    r=dict(company=co,part=part,file=f,box=box,median=med,mode=mode,chrom_share=chrom_share,oklch_mode=[round(v,3) for v in oklch(mode)],
           dE_mode_to_logo={h:round(de(mode,h),1) for h in logo},dE_mode_to_D68702=round(de(mode,'#D68702'),1),D68702_oklch=[round(v,3) for v in oklch('#D68702')])
    out.append(r); print(r)
    t=im.resize((160,round(160*im.height/im.width))); strip.paste(t,(i*170,20)); d.text((i*170,0),co+part,fill=(0,0,0),font=font)
    d.rectangle((i*170,150,i*170+80,185),fill=med); d.rectangle((i*170+80,150,i*170+160,185),fill=mode)
strip.save('/tmp/claude-0/r2/tw/sheets/vehicle_crops.png')
json.dump(out,open('/tmp/claude-0/r2/tw/data/vehicle_colours.json','w'),ensure_ascii=False,indent=1)
