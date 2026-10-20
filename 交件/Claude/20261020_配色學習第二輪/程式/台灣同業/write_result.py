import json
W='/tmp/claude-0/r2/tw/'
U='/mnt/user-data/uploads/崧淳環保科技股份有限公司/'
MAIN=U+'Taiwan_Sewer_CCTV_Competitor_Intelligence_With_Logo_CIS_20261013.pdf'
SUPP=U+'Taiwan_Sewer_CCTV_Logo_CIS_Supplement_20261013.pdf'
FOLD=U+'崧淳同業logo/'
res=dict(
summary_zh=("台灣同業能拿到 logo 圖的有 21 家（31 個版本），主 PDF 的 25 家裡有 14 家查不到 logo。"
 "逐張看圖、用像素量色（彩色門檻 OKLCH C≥0.04，略過白、透明、反鋸齒），扣掉墨色商標的順捷，20 家可算色。"
 "同一支程式重算國外 48 家得 23/8/1/9/1/6，不是上輪的 23/7/3/8/1/6，差在 Sydney Water（色相差 44.2°，剛好在 45° 內）和 Uisce Éireann（三色兩兩最大差 105°）。"
 "台灣「一個彩色加黑白」10/20（50%），跟國外 23/48（48%）幾乎一樣。"
 "不同的是多色 logo：台灣 7 家裡 6 家是對比色、0 家同色系；國外 19 家是 9 家對比、8 家同色系（p=0.18，樣本小）。台灣的多色組合大多是藍或綠配紅、橘一小塊。"
 "台灣多色 logo 的明度差 ΔL* 中位 19.7，跟隨機兩色的 20.0 差不多；國外是 32.1（置換檢定 p=0.14）。"
 "台灣 17 家主色裡藍 9、綠 6、紅 0；國外 42 家紅 11（p=0.024，但這輪做了好幾個檢定，沒校正）。"
 "台灣 6/20 家用漸層，國外上輪文字記到的至少 4/48；書法毛筆字 4/21 家。"
 "車輛照片裡，宏隆、一元、派浦崴洱、日技的槽車是黃橘色（離 #D68702 的 ΔE 4.3–14.8），跟各自 logo 色無關；只有華通的綠槽跟 logo 綠同色相。"
 "深青 #0C424A 最近的台灣主色是大亞 #243952（ΔE 14.0）；靛藍 #333D66 最近也是大亞（7.0），其次一元 #255092（10.1）。"),
new_vs_round1=[
 "上輪台灣只有 17 筆主色（抄自同業色彩整理.md），這輪實際量了 21 家 31 個版本的色、占比、黑白灰、漸層、字型、圖形。",
 "更正上輪 17 筆：邦盛紅 #D3151C 是標語「專人為您服務」不是公司名；綠邑 #254529、銘源 #082066 是網站色不是 logo 色。",
 "重算國外 48 家得 23/8/1/9/1/6；上輪 23/7/3/8/1/6 的差異找到原因（Sydney Water 落在 45° 界線、Uisce Éireann 用前兩色算）。",
 "台灣多色 logo 6/7 是對比色、沒有同色系；國外同色系 8/19。",
 "台灣多色 logo 明度差中位 19.7，接近隨機 20.0，國外 32.1；台灣有兩家（華通、日技）第二色是小字，ΔL* 只有 5.6、4.3。",
 "台灣主色沒有紅（0/17），國外紅 11/42；台灣綠 6/17，國外 5/42。",
 "台灣用漸層 6/20（官網 logo 檔 3/14），書法毛筆字 4/21。",
 "車輛：7 筆車身量色，4 筆是黃橘槽車，跟 #D68702 差 4.3–14.8，跟 logo 色無關。",
 "同業色彩整理.md 的 logo 色重量：可比 19 筆有 16 筆 ΔE2000<2；久大藍差 17（md 用站台圖示深端）、日技漏記紅字。",
 "深青、靛藍跟每家台灣主色的 CIEDE2000 全表。"],
claims=[
 dict(id="tw01",text_zh="主 PDF 登記總表 25 家中，11 家有 logo 或商標圖（全基、升野、積德、華通衛生行、九升、宏隆、浩源、久大、派浦崴洱、龍祥、順捷），14 家未取得（銘源、力士通、晨佳、力賀、昭揚、浚富、瑞碁、三福、程堡、廣村、盛泰、鼎宸、辰福、鎮海）。加上資料夾 14 家，共 21 家有圖。",
   grade="原文已讀",source=MAIN+" p6–7 登記總表（pdftotext → "+W+"pdf/main.txt）；"+SUPP+"（"+W+"pdf/supp.txt）；"+W+"data/inventory.json",check_how="打開兩份 PDF 對照登記總表與附錄圖；python3 -I "+W+"work/inventory.py"),
 dict(id="tw02",text_zh="主 PDF 的 47 張內嵌圖跟補充 PDF 的 47 張逐張像素相同（md5），主 PDF 附錄就是補充 PDF p2–16。資料夾 01 華通清淤圖與補充 PDF p9 像素相同。",
   grade="資料與程式已跑",source=W+"pdfimg/（pdfimages 抽出）；"+W+"progress.md",check_how="pdfimages -png 兩份 PDF 後比 md5"),
 dict(id="tw03",text_zh="量色規則：略過 alpha<250、OKLab L≥0.93 且 C<0.04 的白；8 鄰點至少 4 點同色才留（去反鋸齒）；OKLCH C≥0.04 算彩色；色群占 1.5% 以下當雜色。小字被去邊刪掉的用不去邊版補回（華通衛生行副標、日技 JPN-TEK 紅字、一元英文灰）。",
   grade="資料與程式已跑",source=W+"work/measure.py、"+W+"work/measure2.py → "+W+"data/measure_raw.json、measure_unfiltered.json",check_how="python3 -I "+W+"work/measure.py；python3 -I "+W+"work/spotcheck.py tianfu honglong yuanchang 抽查"),
 dict(id="tw04",text_zh="同業色彩整理.md 記的 logo 色跟這輪量的，可比 19 筆有 16 筆 CIEDE2000<2；邦盛紅差 2.6（是標語）、久大藍 #0A6BB6 對 #2298D3 差 17.1（md 用站台圖示漸層深端，這輪用補充 PDF 全版眾數）；md 漏了日技 JPN-TEK 紅 #EC1D24。",
   grade="資料與程式已跑",source=FOLD+"同業色彩整理.md；"+W+"work/compare_md.py → "+W+"data/md_check.json",check_how="python3 -I "+W+"work/compare_md.py"),
 dict(id="tw05",text_zh="國外 48 家用 OKLCH 兩兩最大色相差規則重算，得一個彩色 23、同色系 8、相鄰 1、對比 9、四色以上 1、只有黑白灰 6。上輪 23/7/3/8/1/6 的相鄰 3 家是 Sydney Water（264°、220°，差 44.2°，本規則算同色系）、Uisce Éireann（前兩色差 87° 算相鄰，三色最大差 105° 算對比）、PUB（相鄰，兩邊一致）。",
   grade="資料與程式已跑",source="/tmp/claude-0/work/peer_schemes.json；"+W+"work/schemes.py",check_how="python3 -I "+W+"work/schemes.py"),
 dict(id="tw06",text_zh="台灣 20 家可算色：一個彩色 10（50%）、同色系 0、相鄰 0、對比 6（30%）、四色以上 1（天福）、只有黑白灰 3（邦盛、綠邑、派浦崴洱）。只看官網 logo 檔 14 家：7/0/0/5/1/1。",
   grade="資料與程式已跑",source=W+"work/tw_decide.py、analyze.py → "+W+"tw_peers.json、comparison.json",check_how="python3 -I "+W+"work/tw_decide.py；python3 -I "+W+"work/analyze.py"),
 dict(id="tw07",text_zh="「一個彩色」台灣 10/20 對國外 23/48，Fisher 雙尾 p=1.0，沒有差別。多色 logo 裡對比色台灣 6/7、國外 9/19，p=0.178。",
   grade="資料與程式已跑",source=W+"comparison.json（檢定_一個彩色、檢定_多色裡對比）",check_how="python3 -I "+W+"work/analyze.py"),
 dict(id="tw08",text_zh="台灣 6 家兩色 logo 有 5 家是藍或綠配紅、橘（華通 綠＋紅褐、大亞 藍＋紅、日技 藍＋紅、宏隆 綠＋橘、積德 綠＋紅），另一家升野是黃＋藍；第二色占比 4 家在 10% 以下（華通 9.7%、大亞 3.6%、日技 2.9%、升野 6.1%），像點綴。",
   grade="資料與程式已跑",source=W+"data/extra.json（多色組合）",check_how="python3 -I "+W+"work/extra.py"),
 dict(id="tw09",text_zh="多色 logo 明度差 ΔL*（CIELAB L* 最大減最小）：台灣 7 家中位 19.7（5.6、37.4、17.7、4.3、21.5、19.8、19.7），≥26 只有 1 家；國外 19 家中位 32.1，≥26 有 13 家；隨機兩彩色 5000 對中位 20.0；台灣色打亂重配中位 18.0。國外減台灣中位 12.4，置換檢定單尾 p=0.137。只看官網 6 家中位 18.7。",
   grade="資料與程式已跑",source=W+"comparison.json（明度差ΔL*），種子 20261018",check_how="python3 -I "+W+"work/analyze.py"),
 dict(id="tw10",text_zh="主色色相（OKLCH h 分格）：台灣 17 家藍 9、綠 6、橘 1（宏隆的綠橘各半，按占比算綠；源昌橘）、黃 1（升野）、紅 0；國外 42 家紅 11、橘 2、綠 5、青 1、藍 21、紫 2。紅主色 台灣 0/17 對國外 11/42，p=0.024；綠 6/17 對 5/42，p=0.062；綠青藍合計 15/17 對 27/42，p=0.111。這輪做了約 8 個檢定，沒有做多重比較校正。",
   grade="資料與程式已跑",source=W+"comparison.json（主色色相）、"+W+"data/extra.json（紅主色）",check_how="python3 -I "+W+"work/analyze.py；python3 -I "+W+"work/extra.py"),
 dict(id="tw11",text_zh="主色 OKLCH 明度中位 台灣 0.536、國外 0.564；彩度中位 台灣 0.129、國外 0.149。",
   grade="資料與程式已跑",source=W+"comparison.json（主色明度彩度）",check_how="python3 -I "+W+"work/analyze.py"),
 dict(id="tw12",text_zh="用漸層的：台灣 6/20（大亞、久大、宏隆、康立、積德、龍祥），官網 logo 檔 3/14；國外上輪文字記到的 4/48（Scottish Water、Uisce Éireann、日本水工設計、Mini-Cam）只是下限。台灣全部對國外下限 Fisher p=0.054。判斷漸層靠目視加量測明度跨度（例：久大藍 0.25、龍祥綠 0.33）。",
   grade="資料與程式已跑",source=W+"tw_peers.json（gradient、note）、"+W+"data/measure_raw.json（okL_spread）",check_how="看 "+W+"img/ 各圖；python3 -I "+W+"work/analyze.py"),
 dict(id="tw13",text_zh="字型（目視）：黑體 12、書法毛筆 4（源昌、宏隆、康立、一元）、無字純圖形 4（全基、積德、派浦崴洱、順捷）、楷明 1（九升，小圖不確定）。",
   grade="目視",source=W+"tw_peers.json（font、font_cls）；"+W+"img/fig_tw_logo_grid.png",check_how="看 "+W+"img/ 裡每家的圖"),
 dict(id="tw14",text_zh="圖形題材（目視，一家可多項）：純字標 6、水（水滴、水波、水漬）5、箭頭循環 4、管 3、字母 3、抽象 2，設施、工具、葉片、書法圓、管內檢視、無圖形色塊各 1。只有升野的圖形畫了管內攝影車。",
   grade="目視",source=W+"tw_peers.json（motif、motif_cls）",check_how="看 "+W+"img/fig_tw_logo_grid.png"),
 dict(id="tw15",text_zh="版本要分清：積德是智財局 2001 年彩色服務標章圖樣；順捷兩件是墨色商標（不計色）；九升、派浦崴洱、龍祥取自第三方頁面；邦盛、康立沒有獨立 logo 檔，取 banner 字卡；浩源兩站兩版（藍字標、白色加圖形）；綠邑只有白色反白版；升野另有網頁頁首金色漸層裝飾版。",
   grade="原文已讀",source=W+"work/logos.json（tier、source）；"+SUPP,check_how="看 "+W+"img/ 下 31 張版本圖與補充 PDF 對應頁"),
 dict(id="tw16",text_zh="車身取色（照片裁切眾數）：宏隆槽體 #C58829（h 73°）、一元 #CFAB7A（h 75°）、派浦崴洱 #A76C32（h 63°）、日技 #C38843（h 68°），跟 #D68702（h 69°）的 ΔE2000 分別 4.3、14.8、13.9、6.7；這四家 logo 主色是綠、藍、無彩、藍。華通綠槽 #98C268（h 130°）跟 logo 綠 #2D661F（h 140°）色相接近但亮很多（ΔE 33.5）；大亞車頭藍 #2D5087 跟 logo 深藍差 10.2，可能是原廠車色。康立白車上的藍色布條跟 logo 綠差 51。",
   grade="資料與程式已跑",source=W+"work/vehicle_colour.py → "+W+"data/vehicle_colours.json；照片 "+FOLD+"*_車輛.jpg、"+W+"pdfimg/p05_017.png、p06_020.png",check_how="python3 -I "+W+"work/vehicle_colour.py，看 "+W+"img/fig_vehicle_colours.png 的裁切位置"),
 dict(id="tw17",text_zh="車輛照片目視：天福白色槽車、逸居深藍車頭加白廂、邦盛 banner 裡白色與橘色卡車、全基團體照穿橘色反光背心；logo 色直接當車身大面積用的只看到華通（綠槽）。",
   grade="目視",source=W+"sheets/vehicles_1.png、vehicles_2.png",check_how="打開兩張拼圖對照原照片"),
 dict(id="tw18",text_zh="深青 #0C424A 跟台灣主色的 CIEDE2000 最近三家：大亞 #243952 14.0、一元 #255092 20.2、積德 #1E572D 21.9；主色在 10 以內 0 家。含其他版本與次色，最近的是華通另一站的青 #005959（9.3）。",
   grade="資料與程式已跑",source=W+"comparison.json（候選色距離）",check_how="python3 -I "+W+"work/analyze.py；或用 colour-tool 的 CIEDE2000 自己算"),
 dict(id="tw19",text_zh="靛藍 #333D66 跟台灣主色的 CIEDE2000 最近三家：大亞 #243952 7.0、一元 #255092 10.1、天福 #2368AD 18.2；主色在 10 以內 1 家（大亞）。大亞 #243952 是槽體漸層的深端，大亞 logo 面積最大的是黑 #060606（45%）。",
   grade="資料與程式已跑",source=W+"comparison.json（候選色距離）；"+W+"tw_peers.json（大亞 neutral）",check_how="python3 -I "+W+"work/analyze.py"),
 dict(id="tw20",text_zh="彩色面積占比（去邊後 logo 像素中彩色的比例）中位 0.997，多數台灣 logo 整個是彩色；低於三成的只有源昌（4.6%，主體是深灰 #414951）和逸居管必潔（20%，公司名是黑 #222222）。",
   grade="資料與程式已跑",source=W+"data/extra.json（彩色面積占比）",check_how="python3 -I "+W+"work/extra.py"),
 dict(id="tw21",text_zh="同業色彩整理.md 寫「沒有一家拿暖色當主色」，按占比算主色時不成立：升野主色是黃 #FCCB26，源昌唯一彩色是橘，宏隆綠橘約各半。",
   grade="資料與程式已跑",source=FOLD+"同業色彩整理.md 觀察段；"+W+"tw_peers.json",check_how="對照 tw_peers.json 的 main 與 cols"),
],
figures=[
 dict(path=W+"img/fig_tw_logo_grid.png",caption_zh="台灣同業 21 家 logo 主版本，白底等比縮放，標出來源層級與配色方式。",third_party=True),
 dict(path=W+"img/fig_tw_swatches.png",caption_zh="每家量到的彩色與黑白灰，色塊寬＝占 logo 非白像素比例，右欄配色方式、彩色數、漸層。",third_party=False),
 dict(path=W+"img/fig_scheme_compare.png",caption_zh="配色方式占比：台灣 20 家對國外 48 家，同一分組程式。",third_party=False),
 dict(path=W+"img/fig_hue_ring.png",caption_zh="主色在 OKLCH 色相環上的位置：左國外 42 家、右台灣 17 家，點是實際主色。",third_party=False),
 dict(path=W+"img/fig_dL.png",caption_zh="多色 logo 的明度差 ΔL*：台灣 7 家、國外 19 家，紅虛線是隨機兩彩色中位。",third_party=False),
 dict(path=W+"img/fig_candidates_dE.png",caption_zh="深青、靛藍跟最近三家台灣主色的 CIEDE2000（只列事實）。",third_party=False),
 dict(path=W+"img/fig_vehicle_colours.png",caption_zh="車輛照片裁切的車身色，對照 logo 色與車身工程黃 #D68702。",third_party=True),
 dict(path=W+"img/",caption_zh="31 個 logo 版本的單張圖（等高 160px、白底；純白版用深灰底），檔名＝tw_peers.json 的 vid。",third_party=True),
 dict(path=W+"tw_peers.json",caption_zh="台灣每家一筆：彩色 hex、占比、OKLCH、黑白灰、漸層、字型、圖形、來源層級、配色方式。",third_party=False),
 dict(path=W+"comparison.json",caption_zh="台灣對國外比較的全部數字（分組、彩色數、ΔL*、漸層、主色色相、候選色距離）。",third_party=False),
],
files=[W+p for p in ["progress.md","tw_peers.json","comparison.json","result.json","data/measure_raw.json","data/measure_unfiltered.json",
  "data/vehicle_colours.json","data/md_check.json","data/inventory.json","data/extra.json","work/measure.py","work/measure2.py","work/spotcheck.py",
  "work/schemes.py","work/ct.py","work/tw_decide.py","work/analyze.py","work/extra.py","work/compare_md.py","work/inventory.py",
  "work/vehicle_colour.py","work/vehicle_sheet.py","work/make_img.py","work/figs.py","work/logos.json","work/write_result.py","img/","sheets/"]],
gaps=[
 "台灣樣本小：可算色 20 家、多色只有 7 家；p 值都只當參考，約 8 個檢定沒有校正多重比較。",
 "國外漸層 4/48 只是下限：上輪沒有逐家記漸層，國外 logo 原圖不在雲端，這輪沒重看。",
 "主 PDF 25 家有 14 家沒有 logo（銘源只有網站文字），台灣樣本偏向有官網的小公司。",
 "積德是 2001 年智財局圖樣，九升、派浦崴洱、龍祥是第三方頁面，邦盛、康立是 banner 字卡，都不一定等於現行版本。",
 "華通清淤品牌與華通衛生行主體的對應，補充 PDF 註明待確認。",
 "沒有任何台灣同業的公開 CIS 手冊，沒有官方 Pantone、CMYK 值；所有色碼都是螢幕圖檔量的，JPEG 有色偏（積德掃描尤其大）。",
 "宏隆橘帶兩端淡出量測不到（像素少被當雜色），漸層判定靠目視。",
 "字型、圖形題材是目視分類，沒有字型檔可對。",
 "車身色受光線、相機影響，只是近似；只有 9 家有車輛圖，大亞、逸居的藍車頭可能是原廠車色，看不出是否刻意配合 logo。",
 "台灣主色採占比最大的彩色，國外採 peer_schemes 第一色，兩邊定義略有不同。"],
)
json.dump(res,open(W+'result.json','w'),ensure_ascii=False,indent=1)
print(len(res['claims']),len(json.dumps(res,ensure_ascii=False)))
