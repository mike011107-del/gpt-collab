# 台灣同業每家定案：設計色（彩色）、黑白灰、漸層、字型、圖形（後三項目視）
# 數字來源：data/measure_final.json（純色無反鋸齒的 4 張圖逐像素直接計數，其餘去邊版；work/purecount.py）、data/measure_unfiltered.json（不去邊，補細字）
# 第三次修正：原本讀 measure_raw.json，去邊規則把小圖細字刪掉，華通紅褐、逸居藍占比被壓低；舊版留在 work/tw_decide_v1.py
# 併色規則（逐筆寫理由）：同一漸層的深淺端併成一色；JPEG 光暈、反鋸齒色不算；其餘 ≥1.5% 的獨立色塊都算
import json, sys
sys.path.insert(0,'/tmp/claude-0/r2/tw/work')
from ct import oklch, lab
W='/tmp/claude-0/r2/tw/'
raw={r['vid']:r for r in json.load(open(W+'data/measure_final.json'))}
unf=json.load(open(W+'data/measure_unfiltered.json'))
cfg={v['vid']:v for v in json.load(open(W+'work/logos.json'))}
def g(vid,i): x=raw[vid]['chromatic'][i]; return dict(hex=x['hex'],share=x['share'])
def merge(vid,i,j,why):  # 把 j 併進 i
    a=raw[vid]['chromatic'][i]; b=raw[vid]['chromatic'][j]
    return dict(hex=a['hex'],share=round(a['share']+b['share'],4),merged=b['hex'],why=why)
N=lambda vid:[dict(name=x['name'],hex=x['hex'],share=x['share']) for x in raw[vid]['neutral']]
T=[
 dict(company='華通',full='華通清淤工程（另有嘉佳／華通衛生行站）',vid='huatong_dredge',
      alt=['huatong_wsh'],cols=[g('huatong_dredge',0),g('huatong_dredge',1)],neutral=N('huatong_dredge'),
      gradient=False,font='黑體（粗）；副標黑體',font_cls='黑體',motif='無，純字標',motif_cls=['純字標'],
      note='「華通清淤」綠、「工程」黑、副標「下水道維護施工經驗豐富」紅褐。原圖不透明像素只有這三個純色，逐像素直接計數：綠 58.8%、紅褐 28.3%、黑 12.8%（舊版去邊後紅褐只剩 9.7%，是細字被刪）。另一站「嘉佳／華通衛生行」只用青 #005959（91.8%）加深灰副標 #363636（8.2%），也是純色直接計數。補充 PDF 註明華通清淤與指定主體對應待確認。'),
 dict(company='邦盛',full='邦盛企業有限公司',vid='bangsheng',alt=['bangsheng_slogan'],cols=[],neutral=N('bangsheng'),
      gradient=False,font='粗黑體',font_cls='黑體',motif='無，banner 字卡',motif_cls=['純字標'],
      note='沒有獨立 logo 檔，公司名印在 banner 白卡上，只有黑字。同一張卡上有紅色標語「專人為您服務」#D7060B；若把標語算進去就變成「一個彩色」。上輪 17 筆主色用的紅 #D3151C 是這行標語。'),
 dict(company='天福',full='天福環保有限公司／天順環工有限公司',vid='tianfu',alt=[],
      cols=[g('tianfu',0),g('tianfu',1),g('tianfu',2),g('tianfu',3)],neutral=N('tianfu'),
      gradient=False,font='黑體（中文藍字）＋英文粗斜無襯線（綠）',font_cls='黑體',
      motif='圓形裡的藍綠波帶（像水和山）＋外圈兩支循環箭頭',motif_cls=['水','箭頭循環'],
      note='四個彩色都是平塗分色帶，沒有漸層。'),
 dict(company='大亞',full='大亞環保股份有限公司',vid='daya',alt=['daya_footer'],
      cols=[merge('daya',0,1,'#83A9A7 是槽體漸層的淺端，目視與深藍連成一條漸層'),g('daya',2)],neutral=N('daya'),
      gradient=True,font='黑體（中黑）＋英文無襯線；圖內 T.Y. 為襯線紅字',font_cls='黑體',
      motif='黑色圓框裡的槽體／塔形加波浪線',motif_cls=['水','設施'],
      note='槽體由深藍 #243952 漸到灰青 #83A9A7（去邊版明度跨度 0.13）。大片是黑 #060606（45%）。英文寫成 ENVIROINMENTAL（原圖如此）。頁首、頁尾兩版色相同、大小不同。'),
 dict(company='久大',full='久大管道工程',vid='jiuda_full',alt=['jiuda_word','jiuda_icon'],cols=[g('jiuda_full',0)],neutral=N('jiuda_full'),
      gradient=True,font='英文超粗寬黑體（展示用）＋中文粗黑體',font_cls='黑體',
      motif='四個灰色管件彎頭排成菱形，中間水滴裡有扳手；字標兩側也有扳手',motif_cls=['水','管','工具'],
      note='藍色從上淺到下深的漸層（明度跨度 0.25），補充 PDF 也記了漸層兩個觀察值 #2159A0、#269BD5。站台圖示（資料夾 06）是同一圖形。'),
 dict(company='源昌',full='源昌工程環保科技',vid='yuanchang',alt=[],cols=[g('yuanchang',0)],neutral=N('yuanchang'),
      gradient=False,font='圓潤手寫毛筆體',font_cls='書法毛筆',
      motif='橘色圓環裡四層灰色箭頭（≫），灰由淺到深分階',motif_cls=['箭頭循環'],
      note='唯一彩色是橘圈，只占 5%；字和箭頭是深灰 #414951（87%）。箭頭四階灰是分段，不是連續漸層。'),
 dict(company='森淨家',full='森淨家',vid='senjingjia',alt=[],cols=[g('senjingjia',0)],neutral=N('senjingjia'),
      gradient=False,font='細黑體（白字）',font_cls='黑體',motif='不規則圓潤色塊，像水漬或卵石',motif_cls=['水'],
      note='淺藍色塊上反白字，副標「水管清洗職人」。'),
 dict(company='逸居管必潔',full='逸居管必潔科技',vid='yiju',alt=[],cols=[g('yiju',0)],neutral=N('yiju'),
      gradient=False,font='公司名明體（橫細直粗、橫筆末端三角襯線）；副標黑體',font_cls='明體或楷體',motif='無，純字標',motif_cls=['純字標'],
      note='公司名黑 #222222（明體），副標「專業管路清洗」藍（黑體）。原圖只有這兩個純色，逐像素直接計數：藍 44.0%、黑 56.0%（舊版去邊後藍只剩 20%）。字型第三次放大 4 倍重看（view3/yiju_x4.png），舊版寫細黑體是錯的。'),
 dict(company='綠邑',full='綠邑環保科技有限公司',vid='lvyi',alt=[],cols=[],neutral=[dict(name='白',hex='#FFFFFF',share=1.0)],
      gradient=False,font='粗黑體＋英文細無襯線',font_cls='黑體',motif='幾何字母 GE（Greene）',motif_cls=['字母'],white_only=True,
      note='只取得白色反白版，放在網站深色頁首上用。上輪 17 筆主色裡的 #254529 是網站頁首色，不是 logo 色。'),
 dict(company='日技',full='日技管清工程股份有限公司',vid='riji',alt=[],
      cols=[g('riji',0),dict(hex='#EC1D24',share=0.029,why='圓徽中 JPN-TEK 小紅字；去邊時被刪，用不去邊色相格占比，色碼取紅字像素眾數')],
      neutral=N('riji'),gradient=False,font='黑體；圓徽內 JPN-TEK 為襯線',font_cls='黑體',
      motif='藍色圓徽，中間白帶寫 JPN-TEK',motif_cls=['字母'],
      note='圓徽白帶帶一點淺藍（#BBD9EE 左右，彩度 0.04 剛過門檻），算主藍的淺色，不另計。'),
 dict(company='宏隆',full='宏隆環保有限公司',vid='honglong',alt=[],cols=[g('honglong',0),g('honglong',1)],neutral=N('honglong'),
      gradient=True,font='書法（毛筆，綠）＋白色黑體「有限公司」',font_cls='書法毛筆',motif='無圖形；橘色底帶',motif_cls=['純字標'],
      note='橘色底帶兩端向白色淡出（目視；量測明度跨度 0，因淡出部分像素少被當雜色）。綠橘各約一半。'),
 dict(company='康立',full='康立衛生清潔工程',vid='kangli',alt=[],cols=[merge('kangli',0,1,'#829437 是綠色底塊漸層的亮端')],
      neutral=[dict(name='白',hex='#FFFFFF',share=None)],
      gradient=True,font='「康立」粗楷毛筆感＋「清潔工程」黑體＋英文無襯線',font_cls='書法毛筆',motif='右上角葉片',motif_cls=['葉片'],
      note='沒有獨立 logo 檔，取 banner 上的綠色底塊（白字）。底塊有深淺漸層（明度跨度 0.14）。'),
 dict(company='一元',full='一元環保工程社',vid='yiyuan',alt=[],cols=[dict(hex=g('yiyuan',0)['hex'],share=0.97,why='去邊版藍 100% 是因為灰色英文細字被刪；跟灰 3% 同一分母，用不去邊最近色分法：藍 97.0%、灰 3.0%（第三次修正，work/share_sens 同法）')],
      neutral=[dict(name='灰',hex='#7C7B7B',share=0.03,why='英文細襯線字，去邊時被刪，用不去邊值')],
      gradient=False,font='書法（毛筆）＋英文襯線',font_cls='書法毛筆',motif='毛筆圓圈裡寫書法「一元」',motif_cls=['書法圓'],
      note='全藍單色。'),
 dict(company='全基',full='全基企業有限公司',vid='quanji',alt=['quanji_fav'],cols=[g('quanji',0)],neutral=N('quanji'),
      gradient=False,font='無字（純圖形）',font_cls='無字',motif='圓點和長條排成箭頭狀（抽象；像管束或水流，推論）',motif_cls=['抽象'],
      note='#CCEFC8（7%）是 JPEG 圓點周圍的淡綠光暈，目視沒有獨立色塊，不計。官網小圖標同色同形。'),
 dict(company='升野',full='升野企業有限公司',vid='shengye',alt=['shengye_head'],cols=[g('shengye',0),g('shengye',1)],neutral=N('shengye'),
      gradient=False,font='中文名筆畫很粗、筆畫末端帶毛筆書寫感（介於粗黑體與毛筆字之間）＋英文粗襯線（SERN YUEH）',font_cls='黑體',font_disputed='歸黑體有爭議：筆畫末端有毛筆頓筆，補充 PDF 也寫「筆畫較厚、帶書寫感」；改算毛筆則黑體 10、毛筆 5（view3/shengye_name.png）',
      motif='黃色方塊裡：藍色管口圓環、箭頭、黑色管內攝影車照出光束',motif_cls=['管','箭頭循環','管內檢視'],
      note='光束是很淡的米色 #F4F3D4（1.7%，彩度 0.041），算淺色不另計；管口圓環偏青 #00A1DE（補充 PDF 值），線細，量測併在藍裡。黑占 33%。內頁頁首版是金色漸層底加白字陰影，屬網頁裝飾。'),
 dict(company='積德',full='積德工程股份有限公司',vid='jide',alt=[],cols=[g('jide',0),g('jide',1)],neutral=N('jide'),
      gradient=True,font='無字（純圖形）',font_cls='無字',motif='四支綠色箭頭繞圈，中間放射狀紅色圓',motif_cls=['箭頭循環'],
      note='智財局 2001 年彩色服務標章圖樣，不等於現行使用。綠、紅都有明顯漸層（明度跨度 0.53、0.31）。JPEG 掃描色差大。'),
 dict(company='九升',full='九升工程有限公司',vid='jiusheng',alt=[],cols=[g('jiusheng',0)],neutral=N('jiusheng'),
      gradient=False,font='白字「九升」偏楷／明體（小圖，目視不確定）＋英文小字',font_cls='明體或楷體',motif='圓形色塊',motif_cls=['無圖形色塊'],
      note='取自第三方合作廠商欄，現行版待核。色相 268°，是偏紫的藍。'),
 dict(company='浩源',full='浩源有限公司',vid='haoyuan_blue',alt=['haoyuan_white'],cols=[g('haoyuan_blue',0)],neutral=N('haoyuan_blue'),
      gradient=False,font='粗黑體＋英文粗圓潤無襯線',font_cls='黑體',motif='藍版無圖形；另一站白版有圓形裡的柱狀圖形',motif_cls=['純字標'],
      note='兩個網站兩個版本：hao-yuan 藍色純字標、pipe-clean 白色反白版加圖形。'),
 dict(company='派浦崴洱',full='派浦崴洱',vid='paipu',alt=['paipu_s'],cols=[],neutral=N('paipu'),
      gradient=False,font='無字（P 字形圖形）',font_cls='無字',motif='圓形 P 字，圓內有水波（像管內水流）',motif_cls=['水','管','字母'],
      note='只取得徵才平台上的低清黑白圖，不知道是否有彩色版。'),
 dict(company='龍祥',full='龍祥環保國際有限公司',vid='longxiang',alt=[],cols=[g('longxiang',0)],neutral=[dict(name='白',hex='#FFFFFF',share=None)],
      gradient=True,font='黑體（白字）',font_cls='黑體',motif='無，綠色橫幅上寫公司名',motif_cls=['純字標'],
      note='第三方企業專頁橫幅，不是 logo 檔。綠色上淺下深漸層（明度跨度 0.33）。'),
 dict(company='順捷',full='順捷營造',vid='shunjie',alt=['shunjie_man'],cols=None,neutral=N('shunjie'),
      gradient=None,font='無字（純圖形）',font_cls='無字',motif='黑灰層疊折塊排成樹／麥穗／向上箭頭形；另一件是戴安全帽的施工人物',motif_cls=['抽象'],
      note='兩件都是智財局墨色商標，墨色登記本來就不帶顏色，所以不計入配色統計。'),
]
OWN_TIERS={'官網logo檔'}
def hue_bin(h):
    for nm,a,b in [('紅',345,360),('紅',0,40),('橘',40,70),('黃',70,110),('綠',110,170),('青',170,225),('藍',225,285),('紫',285,345)]:
        if a<=h<b: return nm
if __name__=='__main__':
    from schemes import scheme
    out=[]
    for t in T:
        v=cfg[t['vid']]; t['tier']=v['tier']; t['source']=v['source']; t['file']=v['file']; t['crop']=v.get('crop')
        t['img']=f"/tmp/claude-0/r2/tw/img/{t['vid']}.png"; t['alt_img']=[f"/tmp/claude-0/r2/tw/img/{a}.png" for a in t['alt']]
        t['own_logo']=v['tier'] in OWN_TIERS
        t['share_method']=raw[t['vid']].get('method')
        if t['cols'] is None:
            t.update(n_chromatic=None,scheme='不計（墨色商標）',scheme_first2=None,main=None)
        else:
            for c in t['cols']:
                L,C,h=oklch(c['hex']); c['oklch']=[round(L,3),round(C,3),round(h,1)]; c['lab_L']=round(lab(c['hex'])[0],1); c['hue_bin']=hue_bin(h)
            t['n_chromatic']=len(t['cols'])
            hx=[c['hex'] for c in t['cols']]
            t['scheme']=scheme(hx); t['scheme_first2']=scheme(hx,'first2')
            t['main']=max(t['cols'],key=lambda c:c['share'])['hex'] if t['cols'] else None
            t['dL']=round(max(c['lab_L'] for c in t['cols'])-min(c['lab_L'] for c in t['cols']),1) if len(t['cols'])>=2 else None
        out.append(t)
        print(f"{t['company']:6s} {t['tier']:10s} 彩{t['n_chromatic']} {t['scheme']:6s} 主{t['main']} 漸層{t['gradient']} ΔL*{t.get('dL')} {[c['hex'] for c in (t['cols'] or [])]}")
    json.dump(out,open(W+'tw_peers.json','w'),ensure_ascii=False,indent=1)
