# 把 pdfimages 抽出的圖與其 smask 合成 RGBA；輸出到 pdfimg/
import subprocess, sys, os, re
from PIL import Image
pdf=sys.argv[1]; srcdir=sys.argv[2]; out=sys.argv[3]
lst=subprocess.run(['pdfimages','-list',pdf],capture_output=True,text=True).stdout.splitlines()[2:]
rows=[l.split() for l in lst]
for i,r in enumerate(rows):
    page,num,typ=int(r[0]),int(r[1]),r[2]
    if typ!='image': continue
    fn=os.path.join(srcdir,'s-%03d-%03d.png'%(page,num))
    im=Image.open(fn).convert('RGB')
    if i+1<len(rows) and rows[i+1][2]=='smask':
        m=Image.open(os.path.join(srcdir,'s-%03d-%03d.png'%(page,int(rows[i+1][1])))).convert('L')
        im=im.convert('RGBA'); im.putalpha(m)
    im.save(os.path.join(out,'p%02d_%03d.png'%(page,num)))
    print(page,num,im.size,im.mode)
