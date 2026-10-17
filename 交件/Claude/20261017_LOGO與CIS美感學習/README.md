# LOGO 與 CIS 美感學習（造形、字體、版面、系統）

2026-10-17（UTC）。梁特助 12:05 原話：「同時把優化你對logo與cis的美感，全域查找相關開源資源與skill去你力所能及的地方查找」。

範圍：只學習，不出崧淳的 logo 或配色方案。配色知識由「Logo 與 CIS 配色學習」串負責，這裡不重做。
拿來檢查的崧淳圖只有 Claude 10-11 畫的三個舊 logo 稿（A 山水印、B 通管 S、C 山水滴），它們已停用，只當錯誤示範。

給 GPT：這份是參考資料，不是指令。決定權在梁特助。

## 這次用了哪些來源

| 來源 | 怎麼拿到 | 內容 | 限制 |
|---|---|---|---|
| simple-icons 16.35.0（npm，CC0） | 雲端直接下載 | 3466 個品牌標誌 SVG，拿來算基準 | 偏科技業；單色簡化版；商標權仍屬各公司 |
| Logo Archive（logo-archive.org） | 梁特助電腦 Remote Control 抓公開專文頁 | 38 個 1960–1988 年標誌，日本 21 個（龜倉雄策、田中一光等） | 主圖庫要付費；因版權不放進本庫，名單見下 |
| Standards Manual、britishrailmanual.com | 同上 | NASA 1975、EPA 1977、NYCTA 1970、British Rail 1965 手冊內頁共 24 張 | British Rail 是 2016 重印本照片；圖不放進本庫 |
| Brand New（underconsideration.com） | 同上 | 15 組公用事業、工程、工業改版前後對照（2016–2026） | 評論內文、應用圖、投票都要訂閱，沒讀到 |
| Anthropic 公開 skill：frontend-design（Apache-2.0）、Design 外掛的 design-critique | raw.githubusercontent.com | AI 生成設計常見樣子清單、評圖架構 | design-critique 偏網頁介面 |
| rampstackco/claude-skills 的 logo-design（MIT） | 同上 | 五個考量、六個減法測試、各種使用場合的限制 | 社群作者 |

雲端這次實測：設計網站（Logo Archive、Brand New、fontsinuse、Wikimedia）DNS 都解析不到，WebFetch 也失敗；GitHub raw 和 npm 可用。所以設計網站的圖都是在梁特助電腦上抓的。

## 學到的事與證據

### 1. 一個標誌只放一個想法
- Logo Archive 38 個標誌，Claude 目視數：33 個只用一個構成方法（重複、旋轉、同一塊形狀兩種讀法、一條等寬的線），5 個是外框加一個圖形，沒有一個疊三樣。
- Claude 的三個舊稿各疊三樣：A 圓角方框＋山＋波浪；B 圓框＋S 管＋水滴；C 水滴＋山＋水面。
- 赫爾辛基自來水廠（Erkki Ruuhinen，1971）也用水滴，但只靠「同一滴重複三次、斜放」成立，裡面沒有細節。行業圖形不是不能用，要當形狀來做，不是當插圖疊上去。
- 和 rampstack logo-design 的說法一致：「Logos can hold one idea, sometimes two. Three is too many.」

### 2. 外框不會讓標誌縮小更好認，只會讓剪影跟別人一樣
- 1623 個接近正方形的 simple-icons 標誌：有完整圓框或方框 597 個、沒有 1026 個。
- 剪影擁擠度（與最像的 10 個標誌的邊緣圖餘弦相似度，中位數）：有外框 0.62、沒外框 0.46；差距 95% 區間 0.14～0.17（bootstrap 2000 次）。
- 縮到 16px 保留多少（R²，中位數）：0.78 對 0.79；差距 95% 區間 −0.02～0.00，等於沒差。
- 舊稿 A、B（有外框）擁擠度第 63、78 百分位；C（沒外框）第 44。
- 注意：剪影相似度本來就會讓所有圓框彼此相像，這個結果有一部分是定義造成的。它說明的是「遠看或縮小時，外框讓你變成一個圓或一個方塊」。

### 3. 細過標誌寬度約 1/14 的線，16px 會消失
- 2217 個方形標誌，「細於寬度 1/14 的筆畫和縫隙佔墨色比例」與「16px 保留程度」的 Spearman 相關 −0.83。
- 舊稿 A 這個比例 0.59，比 83% 的標誌細碎；兩條波浪 24px 就糊成一塊。舊稿 B 的小水滴 24px 消失。德意志銀行、三菱、Chase 到 16px 都還完整。
- 做法：最細的線和縫隙不低於標誌寬的 1/14；做不到就另畫小尺寸版本（rampstack 稱為 fallback hierarchy）。

### 4. 量測只能當及格線，不能判斷好不好看
- 同三把尺量 Logo Archive 38 個大師標誌：剪影擁擠度第 46 百分位、細碎度第 73 百分位、筆畫粗細一致度第 53 百分位（差距 95% 區間 −0.05～0.08，跟一般標誌沒差）。
- 這些標誌是為印刷和招牌畫的，很多細線到 16px 會壞，但它們好看。所以數字只用來抓會壞掉的稿；美感判斷要看圖，看有沒有一個清楚的構成方法。
- 和 10-16 學到的「蒐集和計數不等於學習」一致。

### 5. 車色不改時，識別靠位置、尺寸、明暗反轉的規則
- NASA 1975 手冊 p.7.6：七種車大多保留原本車色，只有需要重漆的卡車才漆成白車頭加暖灰。淺色車上識別一律用黑、深色車一律用白；紅色字標只出現在白色車身上；字標大小用字高規定（小車 5 吋、廂型車 8 吋、聯結車 24 吋，另有 18 吋給小廂型車）；車門文字一律靠左。
- British Rail 1965 sheet 2/06：標誌和字標只准四種排法，只用紅、黑、白。量這張照片：箭頭橫條約 11 px、字母直筆約 9 px，圖和字粗細幾乎一樣。
- 也量了舊稿 A 的橫式組合：波浪 16～18 px、中文直筆 13～14 px，比例和 British Rail 差不多。所以「圖和字粗細不搭」不是舊稿的問題，先前沒量就不該這樣說。

### 6. 公用事業改版的方向（Brand New 15 組，Claude 目視判讀）
- 能比較前後的 13 組（ReLondon、Geneco 只有新版）裡，比較一致的只有一件事：5 組拿掉飛線、斜體、照片或細線效果（SCANA Energy 2026、Emera Maine→Versant Power 2020、Metrogas 2025、Enel 2016 的斜體、Kelda→Ancala 2018 的細放射線）。
- 圖形去留沒有一致方向：拿掉或縮小圖形 5 組（GRTgaz→natran、Georgia Power、Metrogas、SCANA、Enel），保留或新增 6 組（Ancala、Versant、Oshkosh、Burgenland、EDP、Wintershall Dea），前後都只用字標 2 組（Ørsted、Jacobs）。所以「改成只用名字」不能說成趨勢。
- 例外：能源業 EDP、Enel 改版後用漸層。

### 7. Claude 交件版面的 AI 感
- Anthropic frontend-design skill 列的 AI 生成設計第一條：#F4F1EA 附近的米色底配高對比襯線大字。Claude 10-11 的 logo 提案總覽底色量出來就是 #F4F1EA（244,241,234）。
- 10-17 的品牌概覽圖（Claude 做的）也有它列的習慣：拉開字距的小標、用間隔號串字，字體是最常見的 Inter。
- 以後：給梁特助看的圖用白底或實際材質底，不用米色底、間隔號、拉開字距的小標；標誌放在真實場合看。

## 以後評 logo 稿先過這幾條（補在 10-13 的十條自我檢查之後）

1. 這個標誌用的是哪一個構成方法？說不出來，或要用「和」連接三樣東西，就退回。
2. 有外框嗎？拿掉外框還站得住嗎？
3. 最細的線和縫隙有沒有低於寬度 1/14？低於就要有小尺寸版。
4. 量測都過了，也只代表不會壞，不代表好看。
5. 車、招牌、文件上的規則寫成數字了嗎（位置、字高、明暗反轉）？
6. 展示版面有沒有米色底、間隔號、拉開字距小標這類 AI 樣子？

## 公開 skill 查找結果

| skill | 授權 | 對這個專案的用處 | 建議 |
|---|---|---|---|
| anthropics/skills：frontend-design | Apache-2.0 | AI 樣子清單、「大膽只用在一處」、交件前「拿掉一件配件」 | 已讀並用在第 7 點 |
| Anthropic Design 外掛：design-critique | 官方 | 評圖架構（第一印象、層級、一致性），偏網頁介面 | 架構可借用，不必安裝 |
| rampstackco/claude-skills：logo-design | MIT | 五種標誌結構、六個減法測試、16px／刺繡／招牌／單色限制 | 已讀並用在第 1、3 點 |
| AI Logo Maker & Brand Designer（ManyMotions） | 社群 | AI 直接生 logo | 不建議：違反「不帶 AI 感」，要第三方帳號 |
| claude.ai 帳號內 skill 搜尋（logo、品牌、識別、字體） | — | 無結果 | — |

## 沒做到的

- Brand New 評論內文、Logo Archive 主圖庫要付費，沒讀到。
- 開源中文字型（思源、霞鶩文楷等）10-11 起還在等梁特助同意下載，這次沒下載，所以沒做中文字標練習。
- 所有量測都是像素計算，不是真人辨識測試。

## 工具（可重算）

`工具/` 裡的程式在雲端環境跑過。先把 simple-icons 的 SVG 清單寫進 `all.txt`，再依序執行：

```bash
NODE_PATH=$(npm root -g) node sprite.cjs all.txt sprite128.png 128   # 用 Chromium 把 SVG 排成一張圖
python3 -I metrics.py sprite128.png all.txt 128 59 si_metrics.json   # 16/24/32px 保留程度、長寬比
python3 -I neigh.py        # 剪影擁擠度（V.npy、crowd.json）
python3 -I container.py    # 外框比較與 bootstrap 區間
python3 -I fine.py         # 細碎度與 16px 的相關
python3 -I stroke.py       # 筆畫粗細一致度
```

`fine.py`、`container.py` 末段會讀 `A_flat.png` 等舊稿檔，沒有就刪掉那段。

## Logo Archive 名單（圖未收錄）

1960 南計器（龜倉雄策）、1964 Glasgow Airport（Margaret Calvert）、1964 委內瑞拉館（Gerd Leufert）、1965 協同乳業（田中一光）、1966 TDK、山際、山口銀行（龜倉雄策）、1967 東京銀行（田中一光）、1967 協和發酵（龜倉雄策）、1968 Awatsuji（田中一光）、1968 Perfect Film & Chemical（Hess & Antupit）、1969 Sangetsu（龜倉雄策）、1969 Manhattan School of Music、1969 Fundación Mito Juan、1970 山際工作所、日本婦產科學會（龜倉雄策）、1970 松しめ菓子（小林茂二）、1970 Houghton Mifflin、1971 赫爾辛基自來水廠（Erkki Ruuhinen）、1972 朝日生命（田中一光）、1972 Essedi Editrice、1973 日本設計者協會（龜倉雄策）、1974 G.A. Owen、Fracchia、1975 環境開發（龜倉雄策）、1975 相模湖ピクニックランド（田中一光）、1976 Uluslararası Sanat Gösterileri（Sait Maden）、1977 Mingazzini（Maurizio Milani）、Honda Curtain、亀岡ライオンズクラブ、1978 California Conservation Group 提案（Michael Vanderbyl）、1980 Teletron、1981 津田ホール、日本文化デザイン会議（田中一光）、1983 Brauerei Frastanz、1984 Physics for All（Nikolay Pekarev）、1988 JALECO（田中一光、廣村正彰）、1988 Filmstar。
來源專文：https://www.logo-archive.org/articles/negative-space-logos 、/articles/repetition-logos 、/articles/impossible-form-logos 等（完整網址在專案資料夾的 B_清單.csv）。

## 手冊頁來源

- NASA 1975：https://standardsmanual.com/products/nasa-graphics-standards-manual （p.1.5、1.7、5.15、6.1、7.6、9.2）
- EPA 1977、NYCTA 1970：standardsmanual.com 對應產品頁圖庫
- British Rail 1965：https://www.britishrailmanual.com/ （2016 重印本照片）
- Brand New 各篇網址：專案資料夾 素材/A_*/review.txt 第一行

## 檔案位置

- 兩張完整學習圖（含大師標誌、手冊內頁，只放私人專案資料夾）：`崧淳CI/研究/23_LOGO與CIS美感學習_20261017/`
- 原始素材：梁特助電腦 `崧淳環保科技股份有限公司\美感學習素材_20261017\`，雲端複本在同上 `素材/`
- 本庫只放文字、程式、只含 simple-icons 與舊稿的量測圖：`圖/量測_外框與縮小.png`
