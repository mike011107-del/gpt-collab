# 車輛與工作照片拼圖（目視用）
import sys
from PIL import Image, ImageDraw, ImageFont
U='/mnt/user-data/uploads/崧淳環保科技股份有限公司/崧淳同業logo/'
P='/tmp/claude-0/r2/tw/pdfimg/'
L=[('華通(插畫)',U+'01_華通清淤工程_車輛.jpg'),('邦盛',U+'03_邦盛企業_車輛.jpg'),('天福',U+'04_天福環保_車輛.jpg'),
   ('大亞',U+'05_大亞環保_車輛.jpg'),('逸居',U+'09_逸居管必潔_車輛.jpg'),('日技',U+'11_日技管清工程_車輛.jpg'),
   ('宏隆',U+'12_宏隆環保_車輛.jpg'),('康立',U+'13_康立衛生清潔工程_車輛.jpg'),('一元',U+'14_一元環保_車輛.jpg'),
   ('全基 PDF',P+'p05_016.png'),('華通 PDF',P+'p05_017.png'),('宏隆 PDF',P+'p06_019.png'),('派浦 PDF',P+'p06_020.png')]
font=ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',20)
TW=440
def tile(nm,f):
    im=Image.open(f).convert('RGB'); s=TW/im.width; im=im.resize((TW,round(im.height*s)),Image.LANCZOS)
    if im.height>330: im=im.crop((0,0,TW,330))
    t=Image.new('RGB',(TW,im.height+26),(230,230,230)); t.paste(im,(0,26)); ImageDraw.Draw(t).text((4,2),nm+f' {Image.open(f).size}',fill=(0,0,0),font=font); return t
for k,grp in enumerate([L[:6],L[6:]]):
    ts=[tile(*x) for x in grp]; rows=[ts[i:i+2] for i in range(0,len(ts),2)]
    H=sum(max(t.height for t in r) for r in rows); sh=Image.new('RGB',(2*TW+10,H),(255,255,255)); y=0
    for r in rows:
        for j,t in enumerate(r): sh.paste(t,(j*(TW+10),y))
        y+=max(t.height for t in r)
    sh.save(f'/tmp/claude-0/r2/tw/sheets/vehicles_{k+1}.png'); print(sh.size)
