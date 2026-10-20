# 台灣同業 CIS 配色：查核後修正

依據 verify/verdict.json。每項都自己重算或放大看圖確認後才改。查核判「確認」的項目都沒動。

## 1. 量色占比（tw03、tw20，tw_peers.json）
- 原本：所有圖都用去邊規則。華通 01 寫綠 80.4%、紅褐 9.7%、黑 9.9%；逸居寫藍 20%、黑 80%；彩色占比低於三成的有源昌、逸居。
- 改成：只有幾個純色、沒有反鋸齒的 4 張圖改成逐像素直接計數，其他圖照舊去邊。
  - 華通 01：綠 58.8%、紅褐 28.3%、黑 12.8%。
  - 華通衛生行：青 91.8%、深灰 8.2%。
  - 逸居：藍 44.0%、黑 56.0%。
  - 浩源藍版：100%，沒變。
  - 彩色占比低於三成的只剩源昌（4.5%）。大亞約三成（30–32%）。
- 順手修正：一元原本寫藍 100% 加灰 3%，合計超過 100%。改成同一個分母：藍 97%、灰 3%。
- 沒變的：主色、配色方式、ΔL*、主色色相、各項 Fisher 檢定、候選色 ΔE。這些只用到色碼，色碼沒變。
- 依據：
  - work/diag_pure.py：數每張圖不透明像素有幾個相異 RGB。
  - work/purecount.py 輸出 data/measure_final.json。
  - work/tw_decide.py、analyze.py、extra.py 重跑。
  - 放大圖 view3/huatong_x3.png、view3/yiju_x4.png。
  - 舊版存在 work/*_v1.py、data/*_v1.json。

## 2. 多色組合（tw08、摘要、tw21）
- tw08 原本：兩色 logo 有 4 家第二色在 10% 以下（含華通 9.7%）。
- tw08 改成：只有 3 家在 10% 以下，分別是大亞紅 3.6%、日技紅約 3%（2.6–4.2%）、升野藍 6.1%。華通紅褐 28.3%、積德紅 21–27%、宏隆橘 48–50%，都不是點綴。
- 摘要原本：「多色組合大多是藍或綠配紅、橘一小塊」。
- 摘要改成：5 家藍或綠配紅、橘的 logo 裡，紅橘不到 10% 的只有大亞、日技。
- tw21 原本：拿升野、源昌、宏隆反駁 md 的「沒有一家拿暖色當主色」。
- tw21 改成以下幾點：
  - 升野不在 md 的 14 家裡，不能拿來反駁 md。
  - 宏隆按規則主色是綠（52%），但橘帶約占一半，不是點綴。
  - 源昌的橘按規則算主色，但只占 4.5%，按面積仍像點綴。
  - 補一點：md 的點綴名單沒列華通紅褐，它占 28%。
- 依據：
  - work/share_sens.py 輸出 data/share_sensitivity.json（第二色的去邊值對照不去邊值）。
  - data/extra.json 裡的「兩色logo第二色占比」。
  - md 第 64 行。

## 3. 字型（tw13）
- 原本：黑體 12、楷明 1（九升）；逸居寫細黑體；升野寫粗黑體。
- 改成：黑體 11、毛筆 4、無字 4、明體或楷體 2。
  - 逸居公司名是明體：橫筆細、直筆粗，橫筆末端有三角襯線。副標是黑體。
  - 升野中文名筆畫粗、末端有毛筆頓筆，補充 PDF 也寫「帶書寫感」。這裡仍算黑體，但註明有爭議；改算毛筆的話是黑體 10、毛筆 5。
- 依據：
  - 放大圖 view3/yiju_x4.png、view3/shengye_name.png（work/view_fix.py）。
  - tw_peers.json 的 font_cls、font_disputed 欄。
  - 補充 PDF 文字（pdf/supp.txt 第 359 行）。

## 4. 來源頁碼與上輪 17 筆（tw01、new_vs_round1）
- tw01 原本：登記總表在主 PDF p6–7。
- tw01 改成：
  - 登記總表在主 PDF p5（01–13）和 p6（14–25）。
  - 有圖 11 家、未取得 14 家的分法出自補充 PDF 首頁，主 PDF p28 是同一頁。
  - 資料夾的 14 家裡，銘源沒有 logo 圖，有圖的是 13 家。
- 上輪 17 筆原本寫：全部抄自同業色彩整理.md。
- 改成：14 筆來自 md。華通衛生行 #005959、積德 #1F532F、浩源 #0086BE 這 3 筆 md 裡沒有，來自補充 PDF。
- 依據：
  - pdf/main.txt 按換頁符分頁後對照。
  - 在 md 和 pdf/supp.txt 裡逐一搜 /tmp/claude-0/work/naming_results.json 的 17 筆色碼。
  - work/inventory.py 的說明已改正。

## 5. 圖
- fig_tw_swatches.png 原本：
  - 彩色欄 100% 畫 440px，黑白灰欄 100% 畫 200px，兩欄不能互比。
  - 每塊最少畫 64px，小比例被放大。
  - 用的是錯的占比。
- fig_tw_swatches.png 改成：
  - 每家畫一條 100% 長條，彩色和黑白灰同一個比例尺（760px＝100%），不設最小寬。
  - 太窄的色塊在下一行拉引線標色碼和百分比。
  - 用修正後的占比。
- fig_candidates_dE.png 原本：沒有說明大亞色的來歷。
- fig_candidates_dE.png 改成：註明大亞 #243952 是槽體漸層的深端，大亞 logo 面積最大的是黑 #060606（41–45%）。
- 依據：
  - work/figs.py（舊版 work/figs_v1.py）。
  - 目視確認 view3/sw_a.png、view3/sw_b.png、view3/cand.png。

## 輸出
- result_fixed.json 由 work/write_result_fixed.py 產生，數字直接讀 data/extra.json 和 share_sensitivity.json。
- 改過的 claims：tw01、tw03、tw08、tw13、tw20、tw21。
- 也更新了摘要、new_vs_round1、圖說、files、gaps。
- 其他 claims 沒動。
