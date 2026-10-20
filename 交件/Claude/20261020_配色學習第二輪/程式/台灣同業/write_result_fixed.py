# 第三次修正：讀 result.json，照 verify/verdict.json 與自己重算的結果改寫有問題的 claims、摘要、圖說，輸出 result_fixed.json
# 用法：python3 -I /tmp/claude-0/r2/tw/work/write_result_fixed.py
import json, copy
W='/tmp/claude-0/r2/tw/'
R=json.load(open(W+'result.json')); F=copy.deepcopy(R)
E=json.load(open(W+'data/extra.json')); C=json.load(open(W+'comparison.json')); S=json.load(open(W+'data/share_sensitivity.json'))
TW={t['company']:t for t in json.load(open(W+'tw_peers.json'))}
two=E['兩色logo第二色占比']
assert two['第二色小於10']==['大亞','日技','升野'] and two['藍綠配紅橘且紅橘小於10']==['大亞','日技']
assert C['字型_目視']=={'黑體':11,'書法毛筆':4,'無字':4,'明體或楷體':2} or dict(C['字型_目視'])==dict({'黑體':11,'書法毛筆':4,'無字':4,'明體或楷體':2})
assert E['彩色面積占比']['低於三成']==['源昌'] and E['彩色面積占比']['中位']==0.997
MAIN='/mnt/user-data/uploads/崧淳環保科技股份有限公司/Taiwan_Sewer_CCTV_Competitor_Intelligence_With_Logo_CIS_20261013.pdf'
SUPP='/mnt/user-data/uploads/崧淳環保科技股份有限公司/Taiwan_Sewer_CCTV_Logo_CIS_Supplement_20261013.pdf'
MD='/mnt/user-data/uploads/崧淳環保科技股份有限公司/崧淳同業logo/同業色彩整理.md'
pct=lambda x:f"{x*100:.1f}%"
hd=S['華通']; dy=S['大亞']; rj=S['日技']; hl=S['宏隆']; sy=S['升野']; jd=S['積德']
upd={
'tw01':dict(text_zh="主 PDF 登記總表 25 家（p5 列 01–13、p6 列 14–25）中，11 家有 logo 或商標圖（全基、升野、積德、華通衛生行、九升、宏隆、浩源、久大、派浦崴洱、龍祥、順捷），14 家未取得（銘源、力士通、晨佳、力賀、昭揚、浚富、瑞碁、三福、程堡、廣村、盛泰、鼎宸、辰福、鎮海）；這個 11／14 的分法出自補充 PDF 首頁（主 PDF p28 附錄是同一頁）。資料夾是同業色彩整理.md 的 14 家，銘源沒有 logo 圖，有圖 13 家；兩邊重疊華通、久大、宏隆，合計 21 家有圖。",
  source=MAIN+" p5–6 登記總表、p28（補充 PDF 首頁的同一頁）（pdftotext → "+W+"pdf/main.txt）；"+SUPP+" p1（"+W+"pdf/supp.txt）；"+W+"data/inventory.json",
  check_how="打開主 PDF p5–6 與補充 PDF p1 對照；python3 -I "+W+"work/inventory.py"),
'tw03':dict(text_zh="量色規則：略過 alpha<250、OKLab L≥0.93 且 C<0.04 的白；OKLCH C≥0.04 算彩色；色群占 1.5% 以下當雜色。不透明像素只有 1–3 個純色、沒有反鋸齒的 4 張圖（華通清淤、華通衛生行、逸居、浩源藍版）逐像素直接計數。其他圖用去邊：8 鄰點中至少 4 點是同色前景才留（白點不算鄰點）。去邊在小圖細字會刪很多像素（華通 33%、逸居 82%、日技 58%），所以日技紅字、一元灰字改用不去邊的值，多色 logo 的第二色另外附不去邊、分給最近色的占比當範圍。",
  source=W+"work/diag_pure.py（判斷純色）、"+W+"work/purecount.py → "+W+"data/measure_final.json；"+W+"work/measure.py → data/measure_raw.json；"+W+"work/share_sens.py → "+W+"data/share_sensitivity.json",
  check_how="python3 -I "+W+"work/diag_pure.py；python3 -I "+W+"work/purecount.py；python3 -I "+W+"work/share_sens.py"),
'tw08':dict(text_zh=f"台灣 6 家兩色 logo 裡有 5 家是藍或綠配紅、橘（華通 綠＋紅褐、大亞 藍＋紅、日技 藍＋紅、宏隆 綠＋橘、積德 綠＋紅），另一家升野是黃＋藍。第二色占 logo 非白像素 10% 以下的有 3 家，像點綴：大亞紅 {pct(dy['第二色_定案'])}（不去邊 {pct(dy['第二色_不去邊'])}）、日技紅約 3%（2.6–4.2%，看分法）、升野藍 {pct(sy['第二色_定案'])}（不去邊 {pct(sy['第二色_不去邊'])}）。另外 3 家不是點綴：華通紅褐副標 {pct(hd['第二色_定案'])}（純色圖逐像素直接計數）、積德紅 {pct(jd['第二色_定案'])}（不去邊 {pct(jd['第二色_不去邊'])}）、宏隆橘 {pct(hl['第二色_定案'])}（不去邊 {pct(hl['第二色_不去邊'])}）。",
  source=W+"data/extra.json（多色組合、兩色logo第二色占比）；"+W+"data/share_sensitivity.json；"+W+"tw_peers.json",
  check_how="python3 -I "+W+"work/purecount.py；python3 -I "+W+"work/tw_decide.py；python3 -I "+W+"work/share_sens.py；python3 -I "+W+"work/extra.py"),
'tw13':dict(text_zh="字型（目視）：黑體 11、書法毛筆 4（源昌、宏隆、康立、一元）、無字純圖形 4（全基、積德、派浦崴洱、順捷）、明體或楷體 2（逸居公司名是明體，橫細直粗、橫筆末端有三角襯線，副標是黑體；九升小圖不確定）。升野中文名筆畫很粗、筆畫末端帶毛筆頓筆，補充 PDF 也寫「筆畫較厚、帶書寫感」，這裡算黑體但有爭議；改算毛筆就是黑體 10、毛筆 5。",
  source=W+"tw_peers.json（font、font_cls、font_disputed）；"+W+"view3/yiju_x4.png、"+W+"view3/shengye_name.png；"+SUPP+"（升野字體描述）",
  check_how="python3 -I "+W+"work/view_fix.py 後看 view3/ 放大圖；python3 -I "+W+"work/analyze.py 看 字型_目視"),
'tw20':dict(text_zh="彩色面積占比（logo 非白像素中彩色的比例；純色圖逐像素直接計數，其他用去邊後的像素）中位 0.997，多數台灣 logo 整個是彩色。低於三成的只有源昌（4.5%，不去邊 6.2%；主體是深灰 #414951）。大亞約三成（去邊 32%、不去邊 30%，黑占 41–45%）。逸居管必潔原圖逐像素是藍 44%、黑 56%，不低於三成。",
  source=W+"data/extra.json（彩色面積占比）；"+W+"data/measure_final.json",
  check_how="python3 -I "+W+"work/purecount.py；python3 -I "+W+"work/extra.py"),
'tw21':dict(text_zh=f"同業色彩整理.md 觀察段寫「橘紅只當點綴（宏隆、源昌、大亞、邦盛）…沒有一家拿暖色當主色」，成不成立要看主色怎麼定。在 md 的 14 家裡：宏隆橘帶占 logo {pct(hl['第二色_定案'])}–{pct(hl['第二色_不去邊'])}，已經不是點綴，但按「占比最大的彩色」定主色，宏隆主色仍是綠（去邊 {pct(hl['定案占比'][0])}）。源昌唯一的彩色是橘，按這條規則算暖色主色，但只占 logo 4.5%（主體深灰），按面積仍像點綴。md 表上有記華通紅褐 #713E3E，點綴名單沒列它；它占華通 logo {pct(hd['第二色_定案'])}。升野主色是黃 #FCCB26，但升野不在 md 的 14 家裡，不能拿來反駁 md。",
  source=MD+" 觀察段與總表；"+W+"tw_peers.json；"+W+"data/share_sensitivity.json",
  check_how="對照 md 第 64 行與 tw_peers.json 的 main、cols；python3 -I "+W+"work/share_sens.py"),
}
for c in F['claims']:
    if c['id'] in upd: c.update(upd[c['id']])
s=R['summary_zh']
reps=[("逐張看圖、用像素量色（彩色門檻 OKLCH C≥0.04，略過白、透明、反鋸齒）","逐張看圖、用像素量色（彩色門檻 OKLCH C≥0.04，略過白、透明；只有幾個純色、沒反鋸齒的圖逐像素直接計數，其他去掉反鋸齒邊）"),
("台灣的多色組合大多是藍或綠配紅、橘一小塊。","台灣 6 家兩色 logo 有 5 家是藍或綠配紅、橘，但紅橘只占一小塊（<10%）的只有大亞、日技；華通紅褐 28%、積德紅 21–27%、宏隆橘約一半。"),
("書法毛筆字 4/21 家。","書法毛筆字 4/21 家（升野粗筆帶書寫感，算黑體有爭議）。"),
("深青 #0C424A 最近的台灣主色是大亞 #243952（ΔE 14.0）","深青 #0C424A 最近的台灣主色是大亞 #243952（槽體漸層的深端，大亞 logo 面積最大的是黑；ΔE 14.0）")]
for a,b in reps:
    assert s.count(a)==1,a; s=s.replace(a,b)
F['summary_zh']=s
nv=R['new_vs_round1']
assert nv[0].startswith('上輪台灣只有 17 筆主色（抄自同業色彩整理.md）')
nv[0]="上輪台灣只有 17 筆主色（14 筆來自同業色彩整理.md，華通衛生行 #005959、積德 #1F532F、浩源 #0086BE 3 筆來自補充 PDF），這輪實際量了 21 家 31 個版本的色、占比、黑白灰、漸層、字型、圖形。"
assert nv[4].startswith('台灣多色 logo 明度差中位 19.7')
nv[4]="台灣多色 logo 明度差中位 19.7，接近隨機 20.0，國外 32.1；華通、日技的第二色是副標或小字，ΔL* 只有 5.6、4.3。"
nv.insert(5,"量色占比更正（查核後）：華通 01 紅褐 9.7%→28.3%、逸居藍 20%→44%（純色圖改逐像素直接計數）；兩色 logo 第二色 <10% 由 4 家改為 3 家（大亞、日技、升野），彩色占比低於三成只剩源昌。配色方式、主色、ΔL*、檢定都沒變。")
F['new_vs_round1']=nv
for fg in F['figures']:
    if fg['path'].endswith('fig_tw_swatches.png'):
        fg['caption_zh']="每家一條 100% 長條：色塊寬＝占 logo 非白像素比例，彩色與黑白灰同一比例尺、不放大小比例，太窄的在下一行標數字；＊是純色圖逐像素直接計數。右欄配色方式、彩色數、漸層。"
    if fg['path'].endswith('fig_candidates_dE.png'):
        fg['caption_zh']="深青、靛藍跟最近三家台灣主色的 CIEDE2000（只列事實）。大亞 #243952 是槽體漸層的深端，大亞 logo 面積最大的是黑 #060606（41–45%）。"
add=[W+"corrections.md",W+"result_fixed.json",W+"data/measure_final.json",W+"data/share_sensitivity.json",W+"work/diag_pure.py",W+"work/purecount.py",W+"work/share_sens.py",W+"work/view_fix.py",W+"work/write_result_fixed.py",W+"view3/",W+"data/tw_peers_v1.json",W+"data/comparison_v1.json",W+"data/extra_v1.json"]
F['files']=[x for x in R['files'] if x!=W+'result.json']+[W+'result.json（修正前）']+add
F['gaps']=R['gaps']+["有反鋸齒的圖仍用去邊規則，細字、細線的占比會偏低；多色 logo 第二色已附不去邊範圍（data/share_sensitivity.json），單色 logo 的黑白灰占比沒有逐家附範圍。","升野字型歸黑體或毛筆有爭議；九升小圖看不清。"]
json.dump(F,open(W+'result_fixed.json','w'),ensure_ascii=False,indent=1)
print('ok',len(F['claims']))
