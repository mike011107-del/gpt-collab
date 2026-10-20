import sys
from PIL import Image
src,dst=sys.argv[1],sys.argv[2]
im=Image.open(src).convert('RGBA')
bg=Image.new('RGBA',im.size,(60,60,60,255))
bg.alpha_composite(im)
w,h=bg.size
s=max(1,int(600/max(w,h))) if max(w,h)<300 else 1
bg=bg.resize((w*s,h*s),Image.NEAREST)
bg.convert('RGB').save(dst)
print(im.size, im.mode)
