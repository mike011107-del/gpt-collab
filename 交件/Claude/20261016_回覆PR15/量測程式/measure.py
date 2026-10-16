"""量測「崧」右緣到「淳」左緣的實際墨色空白。先跑 render.cjs 產生 k_<em>.png（2 倍）。
分界用 GPT JSON 的第二字字元框 left（CSS px）。"""
from PIL import Image
import numpy as np, json
L={'0':112.95,'0.025':114.975,'0.055':117.4125,'0.14':124.2875}
out={}
for em,s in L.items():
    a=np.array(Image.open(f'k_{em}.png').convert('L'))<128; c=a.any(0); x=int(round(s*2))
    r1=np.where(c[:x])[0].max(); l2=x+np.where(c[x:])[0].min()
    i1=np.where(c[:x])[0].min(); i2=x+np.where(c[x:])[0].max()
    g=(l2-r1-1)/2; out[em]={'兩字墨色空白_px':g,'兩字墨色空白_em':round(g/80.96,3),'墨色總寬_px':(i2-i1+1)/2}
print(json.dumps(out,ensure_ascii=False,indent=1))
