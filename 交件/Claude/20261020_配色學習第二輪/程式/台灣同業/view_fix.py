# 放大看圖：華通 01、逸居（字型）、升野（字型），存 view3/
import sys
from PIL import Image
def flat(p,crop=None):
    im=Image.open(p).convert('RGBA')
    if crop: im=im.crop(crop)
    bg=Image.new('RGBA',im.size,(255,255,255,255)); bg.alpha_composite(im); return bg.convert('RGB')
U='/mnt/user-data/uploads/崧淳環保科技股份有限公司/崧淳同業logo/'
a=flat(U+'01_華通清淤工程.png'); print('huatong',a.size)
b=flat(U+'09_逸居管必潔.png'); print('yiju',b.size)
a.resize((a.width*3,a.height*3),Image.NEAREST).save('/tmp/claude-0/r2/tw/view3/huatong_x3.png')
b.resize((b.width*4,b.height*4),Image.NEAREST).save('/tmp/claude-0/r2/tw/view3/yiju_x4.png')
s=flat('/tmp/claude-0/r2/tw/pdfimg/p08_024.png',(345,208,1625,600)); print('shengye',s.size)
s.resize((s.width//2,s.height//2),Image.LANCZOS).save('/tmp/claude-0/r2/tw/view3/shengye_half.png')
