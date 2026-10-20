import sys
from PIL import Image
src,dst,s=sys.argv[1],sys.argv[2],int(sys.argv[3])
im=Image.open(src).convert('RGBA')
bg=Image.new('RGBA',im.size,(255,255,255,255)); bg.alpha_composite(im)
bg=bg.resize((im.size[0]*s,im.size[1]*s),Image.LANCZOS)
bg.convert('RGB').save(dst); print(im.size)
