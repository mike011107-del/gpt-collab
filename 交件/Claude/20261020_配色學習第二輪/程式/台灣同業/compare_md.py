# 對照「同業色彩整理.md」（10-11 別的串）記的 logo 色，跟這輪 measure.py 量到的色，算 CIEDE2000
import sys, json
sys.path.insert(0,'/tmp/claude-0/r2/tw/work')
from ct import de
W='/tmp/claude-0/r2/tw/'
# (公司, md 記的色, 這輪對應色, 這輪出處說明)
P=[('華通','#2D661F','#2D661F','logo 綠'),('華通','#713E3E','#713E3E','副標紅褐'),
   ('邦盛','#D3151C','#D7060B','md 當 logo 色；這輪判定是標語「專人為您服務」'),
   ('天福','#2267AC','#2368AD','藍'),('天福','#21AC68','#22AD69','綠'),('天福','#A4D49C','#A6D49D','淺綠'),('天福','#5DC4F1','#5EC5F2','天藍'),
   ('大亞','#213750','#243952','深藍（槽體漸層深端）'),('大亞','#AD3822','#AD3922','紅 T.Y.'),
   ('久大','#0A6BB6','#2298D3','md 站台圖示藍深端；這輪取補充 PDF 全版 logo 眾數'),('久大','#029FDC','#2298D3','md 站台圖示藍淺端'),
   ('源昌','#FE6500','#FF6600','橘圈'),('森淨家','#89C5DF','#89C5DF','淺藍'),('逸居管必潔','#2D6EB1','#2D6EB1','副標藍'),
   ('日技','#0070C0','#0070C0','圓徽藍'),('日技','#87BBE1',None,'md 記淺藍；這輪判定為圓徽白帶的淺色，不另計'),
   ('日技',None,'#EC1D24','md 沒記；這輪找到 JPN-TEK 小紅字 2.9%'),
   ('宏隆','#186504','#186504','綠'),('宏隆','#F55903','#F55802','橘'),('康立','#566A1E','#566A1F','底塊橄欖綠'),('一元','#255093','#255092','藍')]
out=[]
for co,a,b,why in P:
    d=round(de(a,b),2) if a and b else None
    out.append(dict(company=co,md_hex=a,this_hex=b,dE2000=d,note=why)); print(co,a,b,d,why)
same=[r for r in out if r['dE2000'] is not None and r['dE2000']<2]
print('ΔE<2 的筆數',len(same),'/',sum(r['dE2000'] is not None for r in out))
json.dump(dict(說明='md＝/mnt/user-data/uploads/崧淳環保科技股份有限公司/崧淳同業logo/同業色彩整理.md 總表「logo 主色」欄；this＝data/measure_raw.json（tw_decide.py 定案）',
  rows=out,dE小於2筆數=len(same),可比筆數=sum(r['dE2000'] is not None for r in out)),open(W+'data/md_check.json','w'),ensure_ascii=False,indent=1)
