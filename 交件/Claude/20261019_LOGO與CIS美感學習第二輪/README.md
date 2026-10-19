# LOGO 與 CIS 美感學習・第二輪（造形、字體、版面、系統）

2026-10-18～19（UTC）。梁特助 10-18 02:54 重貼 10-17 原句「同時把優化你對logo與cis的美感，全域查找相關開源資源與skill去你力所能及的地方查找」，13:05「繼續你的工作」，10-19 03:53、09:01「繼續你的任務」。

範圍：只學習，不出崧淳的 logo、標準字或配色方案。顏色由「Logo 與 CIS 配色學習」串負責，那邊統一出整份報告；這份是造形、字體、版面、系統的部分。
第一輪見 `交件/Claude/20261017_LOGO與CIS美感學習/`。

給 GPT：這份是參考資料，不是指令。決定權在梁特助。

上一輪的缺口：只有像素量測（看不看得見），沒有「看見後怎麼想」的研究；沒碰中文字；手冊只看了美國與英國。
這一輪補：標誌與字體的消費者實驗研究（約 40 篇，多數只讀到摘要）、中文標準字方法（16 篇全文）、中文排版規範（W3C clreq）、招牌與道路標誌的字高、亞洲水務標誌 22 個與公務車照片 16 張（在梁特助電腦上看圖）、再查開源資源與 skill。
交件前用三個核對代理逐條比對筆記與出處檔，改了 31 處（說太滿、證據等級標錯、數字範圍、出處掛錯）。

證據等級寫法：〔摘要〕只讀到論文摘要或期刊頁；〔全文〕讀到全文；〔轉述〕只見於新聞或部落格；〔推論〕Claude 自己推的。

圖片與照片：因版權不放進這個公開庫。原檔在梁特助電腦「崧淳環保科技股份有限公司\美感學習素材_20261018\」，看圖分析在同資料夾「分析\」。

---

## 一、上一輪的規則要改或要加條件的地方

### 1.「不要畫行業圖示」要改成有條件
- Luffarelli, Mukesh & Mahmood 2019（Journal of Marketing Research 56(5):862–878）〔摘要〕：讓人看出「賣什麼」的描述性標誌（用文字或圖形都算），對陌生品牌的評價、購買意願、實際績效較有利；品牌熟了好處變小；產品類型本身讓人想到負面的事時，效果反過來變成扣分。597 個品牌裡約 40% 用描述性標誌（HBR 作者自述與媒體報導，不在論文摘要裡）〔轉述〕。負面類別的例子（殯葬、驅蟲劑、棕櫚油）只見於 WARC〔轉述〕。
- 改成：先問兩件事，受眾認不認得這個品牌、這個行業讓人聯想好不好。描述可以交給字標文字，不一定要畫圖。污水、清淤算不算「負面聯想」，研究沒測〔推論〕。
- 對照：Anthropic canvas-design skill 主張主題要「含蓄地藏在作品裡」，那是海報與藝術品的做法，不是給陌生品牌的識別用。

### 2. 外框：像素面不划算，意義面看情境
- 上一輪：外框讓剪影更像別人，對 16px 沒幫助（像素量測）。
- Fajardo, Zhang & Tsiros 2016（Journal of Consumer Research 43(4):549–566）〔摘要〕：同一個外框，購買風險高時被讀成「保護」、提高購買意願；風險低時被讀成「拘束」、降低購買意願。
- 後續〔摘要〕：拿掉外框讓品牌顯得較寬、較創新、較好延伸（Chen & Bei 2019、2020；Park 等 2024）；預防導向、較保守的人偏好有框（Chen & Bei 2020；Kwon 等 2022）。
- 改成：外框只能用意義面的理由加，而且先確定受眾覺得這筆採購風險高、需要「保護」，或受眾偏預防導向、較保守；小尺寸與撞形的代價照舊存在。

### 3.「一個構成方法」可能有實驗面的間接支持，但限於講實用的品牌〔推論：研究測的是「有結構」，不是構成方法的數量〕
- Affonso & Janiszewski 2023（Journal of Marketing 87(5):736–754）〔摘要＋AMA 新聞稿〕：對稱、平衡、幾何、規律、彼此靠近、元素相似會讓人覺得「有結構」；主打實用功能的品牌，有結構的視覺表現較好，連財務估值都看得出來；主打享樂的品牌相反。
- 不對稱讓人覺得刺激、有活力（Luffarelli, Stamatogiannakis & Yang 2019，JMR 56(1)；Bajaj & Bond 2018）；對稱讓人覺得穩定、品質好（Wu & Yildirim 2025 PLOS ONE，認知負荷低時才成立）〔摘要〕；對稱提高安全感、產品被認為不安全時最強，只見於《Psychology & Marketing》2026 一篇（作者未確認）〔摘要，只見搜尋片段〕。

### 4. 簡單不等於好認：「自然、和諧、繁簡適中」
- Henderson & Cote 1998（195 個標誌）與 van der Lans 等 2009（Marketing Science，十國含中國、新加坡）〔摘要〕：看標誌的三個維度（繁複、自然、和諧）各國一樣；越「自然」越能被正確認出；太和諧、太繁複反而容易讓人誤以為看過（錯誤辨認）。
- 有機、取材自然的形狀普遍比純幾何抽象討喜，跨國差異小（Machado 等 2015；Torres 等 2019）〔摘要〕。
- 黃金比例只在自然形上受偏好，人造幾何形反而偏好 1:1（Pittard 等 2007，澳洲、新加坡、南非）〔摘要〕。
- 簡單標誌顯得能幹但冷淡，複雜標誌多看幾次才佔上風、顯得創新溫暖（Chen 等 2025；van Grinsven & Das 2016；Mahmood 等 2019）〔摘要〕；不同研究對「複雜度隨曝光變好或變壞」結論不一致。

### 5. 負空間與縫隙：兩種量測要一起過
- 圖地反轉標誌（如 FedEx 箭頭）提升好感，前提是藏著的圖形被看出、意思讀得懂（Li 等 2026 JMR）〔摘要〕。
- 上一輪：細於寬度 1/14 的縫隙 16px 會消失。合起來：縫隙在小尺寸消失時，負空間的好處也跟著沒了〔推論，研究沒測小尺寸〕。
- 故意缺一塊的字標顯得創新但較不可信（Hagtvedt 2011 JM，只見 ScienceDaily 新聞稿）〔轉述〕。

### 6. 改版、立體、動感
- 原本尖角的標誌改得越圓，最忠誠的顧客越反感（Walsh 等 2010，Adidas、New Balance 田野實驗 632 人）〔摘要〕；大改會拖慢辨識，要靠重複曝光補（van Grinsven & Das 2015）。
- 有陰影、透視的立體標誌對「看得見的產品、乾淨背景」加分；對抽象服務、雜亂背景幾乎沒用（外川、恩藏 2026 JMR）〔摘要〕。這和上一輪公用事業改版拿掉立體效果的方向一致〔推論〕。
- 靜態標誌做出動感會被看得更久，效果要看動感跟品牌性格搭不搭（Cian 等 2014 JMR）〔摘要〕；傳統、保守的公司用動感「可能適得其反」是密西根大學新聞稿的舉例〔轉述〕。

### 7.「AI 樣子」清單本身會過期
- 上一輪用 Anthropic frontend-design 的清單判斷：米色底 #F4F1EA 配襯線大字是 AI 樣子。
- 這輪讀到 wholiver/swiftui-design-skill（MIT，2026）的「反 AI Slop 六條」：它把「暖白底 #F5F3EF／#FAFAF8 配襯線標題」當成解方。兩份反 AI 清單互相矛盾。
- 改成：不靠清單判斷。任何清單上的「正確樣子」被大量照用後就成為新的 AI 樣子；要問的是這個選擇的理由是不是只屬於這個品牌。
- 中文字距另見第三、六節：中文疏排有正當用途，不能把拉丁字母的「拉開字距小標」規則直接搬到中文。

---

## 二、字體與中文字標

- 中文品牌名主要靠「字的樣子」被記住與評價，英文品牌名主要靠「聲音」（Pan & Schmitt 1996；Schmitt, Pan & Tavassoli 1994；Tavassoli & Han 2002）〔摘要〕。所以中文字標不是圖形的附屬品，對中文受眾是被記住的主要途徑之一。
- 字體跟產品「搭」時，品牌在二選一中被選中約兩倍；搭不搭一部分看字體與產品在「力量感、活潑感」上是否一致，一部分看字體本身的含意（Doyle & Bottomley 2004、2006，英國，拉丁字母）〔摘要〕。
- 字體印象四類：好看、有趣、可靠、醒目；由繁複、和諧、自然、花飾、粗重、窄縮六個字形特徵決定（Henderson, Giese & Cote 2004 JM）〔摘要〕。特徵與印象的細部對應只見於轉述。
- 品牌單獨出現（招牌、標誌）時，字形可能是品牌個性的主要線索；自然、和諧、花飾最重要，換成新品牌名時「自然」仍是關鍵（Grohmann 等 2013）〔摘要〕。
- 手寫感字體讓人覺得「背後有人」、更有感情；但對功能型產品效果反過來（Schroll 等 2018 JCR）〔摘要〕；出事時，手寫字標品牌被責怪得更重（Bai 等 2023 JPBM，五個實驗）〔摘要〕。
- 繁體字實驗：復古字體提高品牌的酷感與懷舊、進而提高地位感，做成書法風格反而削弱（JPBM 2025，浙江工業大學作者）〔摘要，單篇〕。
- 台灣的字體聯想：
  - 台灣受測者認為楷體最能代表台灣、細明體代表中國；日本受測者卻把楷體歸給中國（黃耀明 2023 岩手大學博士論文）〔摘要〕。
  - W3C clreq：台灣多數公文全文用楷體；黑體常用於標題與招牌〔全文〕。
  - 臺科大鄭司維受訪：書法字讓人想到牛肉麵店，標楷體帶公文的嚴肅莊重（Rti）〔轉述〕。
  - justfont 2016：台灣街頭招牌常見的楷書多出自劉元祥書寫、民國 71 年文史哲出版的《商用字彙》，招牌店投影放大使用〔轉述〕。
  - 中國大陸流行的「江湖體」被書法界批評，2025 年官方整治「不規範字體」（Sixth Tone）〔轉述〕。
- 中英雙語：
  - 台灣實驗：英文品牌名讓品牌顯得國際化；中文名在親切、信任、喜歡上得分較高（Chang 2008 Journal of Advertising Research）〔摘要〕。
  - 旅美中國學生 210 人線上實驗：中文名字級較突出時品牌態度較好，中英等大比英文較突出好；華麗的中文字比華麗的英文字評價高，英文花俏配中文樸素不如兩邊都樸素（Bi 2014 愛荷華州立大學碩士論文）〔摘要，單篇〕。
  - 道路標誌的中英字高比：日本國交省規定羅馬字為日文字高 1/2〔全文〕；台灣道路標誌規則第 15 條是否有「英文大寫 1/2、小寫 3/8」兩邊說法不一（見第五節），佐證不足。這是行車辨讀的規格，不是企業標準字的規定，只當起點參考。
  - 譚智恒（Keith Tam）2012 中英雙語排版 76 項屬性框架，可拿來逐項檢查字重、字高、間距、對齊〔摘要〕。

---

## 三、中文排版（W3C clreq，全文讀相關章節）

- 中文預設密排，字身框之間不加空。疏排只用在字少的書眉、圖表說明、短行詩、兒童讀物，用來跟版面取得平衡；緊排用在雜誌、廣告標題。
- 橫排時漢字與西文、數字之間最多 1/4 字寬，行首行尾不加，中文逗號、句號前後與括號內側不加。
- 直排：單一字母或縮寫用全形不轉向；一般西文字詞或四位以上數字順時針轉 90 度；兩到三位數字可橫放在直行裡。
- 台灣、香港的點號放在字身框正中（中國大陸放在左下或右上）；直排用「」，橫排用彎引號。
- 台灣政府、教科書以橫排為主，直排仍是繁體地區的文化特徵。
- 標題比內文大 10–20%，常用黑體或粗明體。
- clreq 沒有把拉開字距列為強調手法（強調一節目前是空的）。

---

## 四、亞洲水務與經典企業標誌（在梁特助電腦上看圖，22 檔）

- 水務機關的標誌多半只用一種東西：東京都下水道局、水道局只用字；大阪、橫濱用市章；香港渠務署用 D、S 兩個字母嵌套。圖加字的只有新加坡 PUB、日本下水道協會、韓國 K-water、台水。
- 圖形大多只用一個構成手法：重複（味全五圓、中華電信條紋、PUB 與 K-water 的三道弧）、旋轉（Mazda 1975、大同）、字母嵌套（渠務署）、單一形狀（大阪市章）。例外是台電（細環＋台電二字＋閃電）、中油（紅焰＋火炬＋嵌字＋三道環）這種多元素徽章。和第一輪 Logo Archive 38 個裡 33 個只用一個方法的結果一致。
- 外框只有 5/22：台水、台電、中油、大同、Mazda 1975；完整閉合的只有台電與 Mazda 1975。日本、新加坡、韓國、香港的水務標誌都沒有框。圓框徽章集中在台灣公營或老牌企業〔推論，樣本小〕。
- 最細的線：純圖形標誌約為寬度的 1/7 到 1/53；英文小字常到 1/100 到 1/300；圖形裡最細的是台電環線約 1/290、中油火炬內線約 1/140，都在多元素徽章裡。用第一輪「細於 1/14 縮小會消失」來看，多元素徽章和英文小字都最容易在小尺寸壞掉〔推論，這輪沒做縮小測試〕。
- 圖字組合：11/22 是圖左字右，字高多數在圖高的 0.46 到 0.9 之間；K-water 是圖上字下。中文在上、英文在下時，英文常拉到跟中文同寬（台電、中華電信）。
- 中文字體：黑體或特製黑體 6 例；書法只有中油；明體、楷體、圓體都沒出現〔字體是看風格判斷，沒比對字型檔〕。
- 限制：日本下水道協會、台水、Mazda 1975 原圖太小只能估；年份多半沒確認。

---

## 五、車身上的字與遠看要多大

### 車輛照片（在梁特助電腦上看圖，16 張，維基共享資源）
- 16 張都是淺色車（黃、白、淺藍、銀）。淺色車身直接上字一律深色字（黑、深藍、深棕）；白字只出現在另外加上去的深色色帶裡。
- 名稱全部橫排。台灣的車在右側多由右往左寫（台電、中油、中華電信），左側由左往右只看到中油一例；中華電信 V16 同一側兩種方向混用。
- 字分兩層：前門小字放身分（標誌＋名稱，台灣車再加區處名、車號），字高約車高的 1/40 到 1/60；車廂、罐體、後段放大字名稱，約車高 1/7 到 1/28；兩層多半差 2.5 到 7 倍〔像素估，透視誤差可能 ±30%，只看量級〕。
- 一台車上的識別元素多在 3 到 6 個。
- 例外：香港渠務署只在車門放一塊標誌＋中英名，靠整車黃漆辨識；中華電信同公司有黑字與藍帶反白兩種做法；中油把「中」「油」兩字拉滿罐身兩端；台電把搶修電話用紅字放車門。

### 遠看要多大的字
- 美國招牌（USSC 2006 的面積公式與表 1；LI 定義、壅塞係數、行車折減出自另一份文件，工作檔 E01 第 14–19 頁）〔全文〕：Legibility Index（LI）＝每 1 英吋大寫字高能讀的英尺數，平均 30，約等於視距是字高的 360 倍（1 公分字高約 3.6 公尺）；壅塞環境乘 0.67 到 0.83；實際開車時 LI 平均至少降 35%。全大寫要多約 15% 字高。
- 同一張表：外照招牌黑字白底比白字黑底好認（Helvetica 29 對 26、Clarendon 28 對 24）；內照（不透光底、只有字發光）的白字黑底比外照各組都好認（Helvetica 34、Clarendon 36），但表中沒有內照的黑字白底可以直接比。全大寫一律比大小寫混排差。
- 日本道路標誌（標識令）：字高照設計速度定 10、20、30 公分，必要時可放大 1.5 到 3 倍，高速公路以外最多 2 倍；羅馬字為日文字高 1/2〔全文〕。；羅馬字為日文字高 1/2〔全文〕。
- 日本高速公路標誌 2016 改版（村重至康，IATSS Review）〔全文〕：英文從日文的 50% 提高到 55%；字距從字寬的 30% 改為 20%（一般字型約 10%）；版面留白率守在 50% 以上；字體改ヒラギノ＋Vialog。判讀距離日文增加 10–18%、英文 15–21%；60 歲以上只增加 19 公尺。
  - 換算〔推論〕：新版日文 55 公分、全體 243 公尺，每 1 公分約 4.4 公尺；英文約 30 公分、全體 130 公尺，每 1 公分約 4.3 公尺（工作檔沒寫舊版字高，舊版的換算要假設日文 50 公分）。60 歲以上看日文約 3.8 公尺，外國人看英文約 5.3 公尺。以全體受測者來看，中日文和英文每公分字高看得差不多遠。
  - 出口編號「12」改版後反而變難認：Vialog 的「1」有底線，跟「2」的底橫連成一條，數字改用 Frutiger。字體要放在實際字串上測，單字好看不代表組合好認〔推論〕。
- 台灣：路面標字用正楷或變體字，橫豎筆畫寬度可採 2：1（道路標誌規則第 150 條，電腦上讀到的摘錄）。第 15 條中英字高比兩邊說法不一：電腦上的摘錄版沒有比例；搜尋摘要稱現行版有「英文大寫 1/2、小寫 3/8 為原則」。佐證不足，這是行車規格，不再深查。

### 第一輪的車體規則要改
- 第一輪：車色不改時靠「位置、字高、明暗反轉」成套（NASA 1975）。
- 改成：位置；兩層字高（門上小字身分、車身大字名稱，寫成車高的比例）；淺色車身用深色字，反白只放在加上去的色帶裡。
- 第一輪漏掉的：整車漆指定色本身就是識別（渠務署、台電、中華電信的黃）；色帶或條紋是這批照片裡最常見、最顯眼的手法（東京都水道局、中油、中華電信）。這兩件屬顏色，轉給配色串。

---

## 六、中文標準字怎麼做（16 篇全文：justfont 部落格、許瀚文訪談、森澤字體辭典、武藏野美大）

- 標準字只做固定的一組字，不是整套字型，所以要逐字調，不能直接打字。
- 大小：同面積的菱形看起來比正方形小，「今」要做大、「國」要略縮；先做「上」「下」「國」三個基準字（justfont）。字頂字底不要機械對齊：許瀚文改台灣啤酒標準字時，「灣」的鉤下沉做過衝，「台」「啤」的口部提高，每個字以 units 微調（左右邊界、豎畫寬、內白都有調，文中沒交代 unit 尺度）。
- 重心：偏高顯得緊張、有品格；偏低顯得安定、親切；同一組字要一致（森澤）。
- 中宮：收緊時輪廓凸顯、好認、有氣勢；放鬆時方正、填滿字面。
- 粗細靠眼睛不靠數字：筆畫少的略粗、多的略細，被擠壓的部件補粗（許瀚文）。深底淺字在螢幕上看起來較粗，要另做收細版（綠藤生機改版）。
- 小尺寸：縮小粗細對比、調整內白，大小字都更清楚（許瀚文）。陳敦化主張縮到 0.4 公分還要看得清楚。也有人為小尺寸減筆畫（「灣」作「湾」、「機」省鉤點），但這改了字形，對繁體受眾要另外判斷〔推論〕。
- 中英搭配：和諧法（明體配襯線、黑體配無襯線、圓體配圓體）或襯托法（中文個性強時英文縮小低調）。不要直接用中文字型內建的英文：標楷體的英文是等寬的，新細明體的英文被壓窄（justfont）。
- 字距：中文內文不拉開；標題沒有規範，不黏就好（justfont）。西文 Bringhurst 的字距數字不能直接搬到中文。日本高速公路標誌字距 20% 是遠看的特例。
- 沒找到：常聽到的「字面率」，16 篇都沒有給百分比。

### 楷體還是黑體（把第二、四、五節放在一起）
- 台灣受眾的聯想：楷體＝台灣、公文、莊重（黃耀明 2023〔摘要，只見搜尋片段〕、clreq〔全文〕、臺科大鄭司維〔轉述〕）；街頭招牌、路面標字常見楷書（justfont〔轉述〕、第 150 條）。黑體常用於標題與招牌（clreq）。
- 實物：亞洲水務與經典企業標誌 22 檔裡，看得出中文字體的有黑體或特製黑體 6 例、書法 1 例（中油）；沒有一個用楷體〔看風格判斷，沒比對字型檔〕。
- 崧淳車身現在用黑色粗楷全名（照片）。楷體縮小後跟黑體比哪個好認，電腦上的測試這輪沒跑完，沒有結論。

---

## 七、開源資源與 skill 再查
- 新讀：anthropics/skills canvas-design（海報藝術用，主題含蓄）、brand-guidelines、theme-factory（套 Anthropic 自己的樣式，對識別學習幫助小）；wholiver/swiftui-design-skill（MIT，反 AI 清單與 Anthropic 清單互相矛盾，見一-7）；uxKero/anydesign（把圖片或網址拆成設計系統文件，偏網頁介面，未深入）。
- Claude 外掛目錄另有 brand-studio、brand-md、Codesign（未安裝，未細讀）。
- awesome 清單（ComposioHQ、travisvn）沒有專做 logo、中文字標或 CIS 手冊的 skill。
- 中文排版開源規範：W3C clreq（見第三節）。
- 結論：這輪沒找到比上一輪 rampstack logo-design 更專門的 skill；學習價值主要來自研究文獻與實物。

---

## 八、交稿前自我檢查再加幾條（接第一輪十六條）
1. 受眾認不認得這個品牌？行業讓人聯想好不好？兩者決定要不要讓標誌說出「做什麼」，而且可以交給字標文字說（Luffarelli 2019）。
2. 外框有意義面的理由嗎？受眾覺得這筆採購風險高、需要「保護」嗎？（Fajardo 2016；受眾偏預防導向、較保守時另見 Chen & Bei 2020、Kwon 等 2022）
3. 中文字標逐字調過了嗎：大小、重心、中宮、粗細？縮到 0.4 公分還認得嗎？英文是另外選的，不是中文字型內建的嗎？
4. 中文拉開字距有理由嗎（字少要跟版面平衡、或要遠看）？
5. 車身兩層字高寫成車高的比例了嗎？遠看的字高算過嗎？理想狀況 1 公分約 3.6 到 4.4 公尺（USSC 平均；日本高速公路實驗換算〔推論〕）；實際開車至少打 65 折，約 2.3 公尺，壅塞路段約 2.4 到 3.0 公尺，按保守值算。淺底是深字嗎？
6. 字體在實際字串上測過嗎（「12」的教訓）？
7. 這個選擇的理由只屬於這個品牌嗎？還是照某份清單的「正確樣子」？

---

## 九、這輪的限制
- 約 40 篇研究多數只讀到摘要；Jiang 2016 等少數拿到全文，但細節這輪還沒讀完。多用虛構品牌、學生或線上受試者；人類重複驗證很少。結論要連同條件一起用。
- B2B 或服務業的標誌實驗幾乎找不到。
- 台灣 10 個公部門機關都沒有公開 CIS 手冊 PDF；只抓到新北市立圖書館 2011 年 8 頁手冊。
- 在梁特助電腦上還沒做完兩項：日文字體研究 4 篇與 Jiang 2016 全文的細節、楷體黑體縮小測試。這兩項這輪沒有結論。
- 第四、五節的圖與照片因版權不放進公開的 gpt-collab，只放梁特助電腦「美感學習素材_20261018」。

工作檔在專案共用資料夾 崧淳CI/研究/23_LOGO與CIS美感學習_20261017/第二輪_20261018/工作檔/，不在這個庫（rc_01 標誌結構、rc_02 車輛、rc_03 標準字方法、rc_04 視認距離、notes_layout_skills 排版與 skill、shape.json 與 type.json 研究文獻整理）。


---

## 附錄：出處

### 研究文獻（依主題；seen＝Claude 實際看到的層級）

**S1** 讓人一眼看出賣什麼的「描述性」標誌，對陌生品牌的評價和購買意願比較有利
- Let the Logo Do the Talking（SAGE 期刊頁）：https://journals.sagepub.com/doi/abs/10.1177/0022243719845000（primary，search-snippet）
- Let the logo do the talking（Sussex 作者接受稿頁）：https://sussex.figshare.com/articles/journal_contribution/Let_the_logo_do_the_talking_the_influence_of_logo_descriptiveness_on_brand_equity/23483705（primary，abstract）
- A Study of 597 Logos Shows Which Kind Is Most Effective（HBR，作者自述）：https://hbr.org/2019/09/a-study-of-597-logos-shows-which-kind-is-most-effective（secondary，search-snippet）
- The science behind effective logos（WARC，負面類別例子）：https://www.warc.com/newsandopinion/news/the-science-behind-effective-logos/42646（secondary，search-snippet）
- Seeing Is Not Perceiving（arXiv 2026，AI 模擬重做）：https://arxiv.org/pdf/2609.25677（secondary，search-snippet）
- The role of brand logos in firm performance（IDEAS 摘要）：https://ideas.repec.org/a/eee/jbrese/v66y2013i2p180-187.html（primary，abstract）

**S2** 圓形標誌讓人覺得產品較舒適、公司較體貼，尖角標誌讓人覺得較耐用、較硬、較高級
- Does Your Company Have the Right Logo?（PolyU 典藏，含接受稿）：https://ira.lib.polyu.edu.hk/handle/10397/64985（primary，abstract）
- Jiang et al. 2016 JCR（作者網站 PDF）：https://static.amitavac.com/2016/02/Jiang-Gorn-Galli-and-Chattopadhyay_2016_JCR.pdf（primary，search-snippet）
- How Your Logo Shapes Consumer Judgments（INSEAD Knowledge）：https://knowledge.insead.edu/marketing/how-your-logo-shapes-consumer-judgments（secondary，search-snippet）
- Should you change your company logo?（ESADE，航空例）：https://dobetter.esade.edu/en/company-logo（secondary，search-snippet）
- The impact of self-construal on aesthetic preference for angular versus rounded shapes（CEIBS 典藏）：https://repository.ceibs.edu/en/publications/the-impact-of-self-construal-on-aesthetic-preference-for-angular-（primary，abstract）
- The shape of premiumness（IDEAS 摘要）：https://ideas.repec.org/a/eee/joreco/v75y2023ics0969698923002631.html（primary，abstract）
- Seeing Is Not Perceiving（arXiv 2026，AI 模擬重做）：https://arxiv.org/pdf/2609.25677（secondary，search-snippet）

**S3** 經典的 195 個標誌研究發現：要讓人認得，標誌最好很「自然」（像日常看得到的東西）、很「和諧」、繁簡適中
- Guidelines for Selecting or Modifying Logos（SAGE 期刊頁）：https://journals.sagepub.com/doi/abs/10.1177/002224299806200202（primary，search-snippet）
- Building strong brands in Asia（IJRM 2003，Dialnet 索引）：https://dialnet.unirioja.es/ejemplar/83603（primary，search-snippet）
- Logo Selection and Modification Guidelines: an empirical international validation in Chile：https://repositorio.uchile.cl/handle/2250/140229（primary，search-snippet）

**S4** 外框的意義看情境：消費者覺得這次購買有風險時，外框被讀成「保護」，購買意願上升
- The Contingent Nature of the Symbolic Associations of Visual Design Elements（IDEAS/RePEc 摘要）：https://ideas.repec.org/a/oup/jconrs/v43y2016i4p549-566..html（primary，abstract）
- Fajardo et al. 2016（OUP 期刊頁）：https://academic.oup.com/jcr/article-abstract/43/4/549/2630525（primary，search-snippet）
- Brand Logo Frames（ACR 2014 會議摘要，Miami 典藏）：https://scholarship.miami.edu/esploro/outputs/journalArticle/Brand-Logo-Frames-How-and-When/991031623948302976（primary，search-snippet）
- Free the brand: How a logo frame influences the potentiality of brand extensions（Springer）：https://link.springer.com/article/10.1057/s41262-018-0142-0（primary，abstract）
- The effects of logo frame design on brand extensions（Emerald）：https://www.emerald.com/insight/content/doi/10.1108/JPBM-12-2017-1698/full/html（primary，abstract）
- Politics, Promotions, and Pandemics（JACR 2022，IDEAS 摘要）：https://ideas.repec.org/a/ucp/jacres/doi10.1086-719577.html（primary，abstract）
- Open to innovation: How a logo frame shapes consumer perception of the brand（SBP 2024）：https://sbp-journal.com/index.php/sbp/article/view/13966（primary，abstract）

**S5** 標誌繁簡沒有單一最佳解：簡單標誌第一眼好認、顯得能幹但較冷淡
- Effects of Brand Logo Complexity, Repetition, and Spacing（IDEAS 摘要）：https://ideas.repec.org/a/oup/jconrs/v28y2001i1p18-32.html（primary，abstract）
- Logo design in marketing communications（van Grinsven & Das，作者上傳全文）：https://www.researchgate.net/profile/Enny-Das/publication/271939205_Logo_design_in_marketing_communications_Brand_logo_complexity_moderates_exposure_effects_on_brand_recognition_and_brand_attitude/links/5b158527a6fdcc31bbf472b9/Logo-design-in-marketing-communications-Brand-logo-complexity-moderates-exposure-effects-on-brand-recognition-and-brand-attitude.pdf（primary，search-snippet）
- Breaking Through Complexity（City 大學典藏接受稿）：https://openaccess.city.ac.uk/id/eprint/4267/（primary，search-snippet）
- What's in a logo? Complex visual cues in equity crowdfunding（Westminster 典藏）：https://westminsterresearch.westminster.ac.uk/item/q9176/what-s-in-a-logo-the-impact-of-complex-visual-cues-in-equity-crowdfunding（primary，abstract）
- Simple or complex logos? Logo complexity and brand luxuriousness（HKBU）：https://scholars.hkbu.edu.hk/en/publications/simple-or-complex-logos-the-impact-of-logo-complexity-on-brand-lu/（primary，abstract）
- The visual language of brand logos: logo simplicity, warmth and competence（IDEAS）：https://ideas.repec.org/a/eee/jbrese/v200y2025ics0148296325004035.html（primary，abstract）
- Logo visual thickness（Brock 大學典藏）：https://brocku.scholaris.ca/items/5e39f2c2-492f-4607-8c4b-4729d07d1150（primary，search-snippet）

**S6** 不對稱標誌讓人覺得較刺激、有活力，對主打刺激感的品牌加分
- Beyond Beauty: Design Symmetry and Brand Personality（作者學校 PDF）：https://www.scheller.gatech.edu/directory/research/marketing/bond/pdf/bajaj_bond_jcp_2018.pdf（primary，search-snippet）
- The Visual Asymmetry Effect（SAGE 期刊頁）：https://journals.sagepub.com/doi/10.1177/0022243718820548（primary，search-snippet）
- Can a Symmetrical Logo Be Bad for Your Brand?（IE Insights）：https://www.ie.edu/insights/articles/can-a-symmetrical-logo-be-bad-for-your-brand/（secondary，search-snippet）
- Beauty of symmetry: logo symmetry and perceived product quality（PMC 全文頁）：https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11774398/（primary，abstract）
- The Silent Guardian: Symmetry and safety cues（Wiley）：https://onlinelibrary.wiley.com/doi/abs/10.1002/mar.70168（primary，search-snippet）
- Stability or instability: brand concepts and logo design preferences（IDEAS）：https://ideas.repec.org/a/pal/jobman/v28y2021i5d10.1057_s41262-021-00238-6.html（primary，abstract）

**S7** 靜態標誌若讓人覺得「在動」，會讓人看得更久、更有好感，但前提是動感要符合品牌性格
- This Logo Moves Me（作者網站全文 PDF）：https://aradhnakrishna.com/wp-content/uploads/2020/05/this_logo_moves_me_jmr.pdf（primary，search-snippet）
- This Logo Moves Me（SSRN 摘要）：https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2420816（primary，abstract）
- Branding: When does a logo move you?（密西根大學新聞）：https://news.umich.edu/?p=22030（secondary，search-snippet）
- A Sign of Things to Come（作者網站）：https://aradhnakrishna.com/wp-content/uploads/2020/05/iconography.pdf（primary，search-snippet）
- Upward-tilted logos cue perceptions of unhealthiness（IDEAS）：https://ideas.repec.org/a/eee/jouret/v102y2026i1p63-77.html（primary，abstract）
- Disruptive but costly: how upside-down logos backfire（LSE 典藏）：https://researchonline.lse.ac.uk/id/eprint/129521（primary，abstract）

**S8** 取材自然、有機形狀的標誌普遍比抽象幾何標誌更討喜，而且跨國差異不大
- Brand logo design: examining consumer response to naturalness（Emerald）：https://www.emerald.com/insight/content/doi/10.1108/JPBM-05-2014-0609/full/html（primary，abstract）
- Same design, same response? Investigating natural designs in international logos（UCP）：https://ciencia.ucp.pt/en/publications/same-design-same-response-investigating-natural-designs-in-intern/（primary，abstract）
- Aesthetic theory and logo design: proportion across cultures（Monash）：https://research.monash.edu/en/publications/aesthetic-theory-and-logo-design-examining-consumer-response-to-p/（primary，abstract）
- The Impact of Aesthetic Preference in Product Design – Golden Ratio and Korean's Preference Proportion：https://aodr.org/xml/12027/12027.pdf（primary，search-snippet）
- The visual naturalness effect（Wiley）：https://onlinelibrary.wiley.com/doi/10.1111/ijcs.12912（primary，search-snippet）

**S9** 改版時改得越多，最忠誠的顧客越反感（例如把尖角標誌改圓），忠誠度低的人反而喜歡
- Do Logo Redesigns Help or Hurt Your Brand?（SSRN）：https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1998809（primary，abstract）
- Starbucks effect: committed customers don't like logo redesigns（Penn State 新聞）：https://www.psu.edu/news/research/story/starbucks-effect-committed-customers-dont-logo-redesigns（secondary，search-snippet）
- How re-designing angular logos to be rounded shapes brand attitude（Penn State）：https://pure.psu.edu/en/publications/how-re-designing-angular-logos-to-be-rounded-shapes-brand-attitud/（primary，abstract）
- The effects of visual rejuvenation through brand logos（HAL）：https://hal-hec.archives-ouvertes.fr/hal-00772061（primary，abstract）
- Processing different degrees of logo change（Emerald）：https://emeraldinsight.com/insight/content/doi/10.1108/EJM-02-2014-0127/full/html（primary，search-snippet）

**S10** 負空間／圖地反轉的標誌（例如 FedEx 的箭頭）能提高品牌好感，但前提是藏著的圖形要被認出、而且看得懂意思
- The Impact of Figure–Ground Reversal in Brand Logos on Brand Attitude（SAGE）：https://journals.sagepub.com/doi/10.1177/00222437261417659（primary，search-snippet）
- EXPRESS: The Impact of Figure-Ground Reversal (FGR) in Brand Logos（ResearchGate）：https://www.researchgate.net/publication/399732910_EXPRESS_The_Impact_of_Figure-Ground_Reversal_FGR_in_Brand_Logos_on_Brand_Attitude（primary，search-snippet）
- Illusory trust: Kanizsa shapes incidentally increase trust（科隆大學典藏）：https://kups.ub.uni-koeln.de/33402（primary，abstract）
- The incomplete art of brand imagery（ScienceDaily，Hagtvedt 2011 新聞稿）：https://sciencedaily.com/releases/2011/05/110516131542.htm（secondary，search-snippet）

**S11** 有陰影、透視等深度線索的立體標誌，比平面版本更能提高購買可能性，因為看起來較真實、較可信
- The Three-Dimensional Effect in Logo Design（SAGE DOI）：https://doi.org/10.1177/00222437261460880（primary，search-snippet）
- 早稻田大學研究者資料庫（恩藏直人）：https://w-rdb.waseda.jp/html/100000265_en.html?k=%E7%A3%AF%E7%94%B0+%E5%8F%8B%E9%87%8C%E5%AD%90（primary，search-snippet）
- 早稻田大學 GRC 研究介紹：https://www.waseda.jp/inst/research/?p=85895（secondary，search-snippet）
- How 3D logos influence brand trust and consumer behavior（Science of Money）：http://www.scienceofmoney.org/how-3d-logos-influence-brand-trust-and-consumer-behavior-1297/（secondary，search-snippet）

**S12** 標誌與行銷視覺「有結構」（對稱、平衡、幾何、規律、彼此靠近、元素相似）對主打實用功能的品牌較有利，「無結構」對主打享樂的
- Marketing by Design: The Influence of Perceptual Structure on Brand Performance（SAGE）：https://journals.sagepub.com/doi/abs/10.1177/00222429221142281（primary，search-snippet）
- Marketing by Design（SSRN）：https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6609978（primary，abstract）
- Think before designing your logo（AMA 新聞稿）：https://www.ama.org/2023/01/03/think-before-designing-your-logo-how-marketers-can-capitalize-on-the-power-of-perception-to-influence-beliefs-about-brand-performance/（secondary，search-snippet）
- How marketers can capitalize on the power of perception（Phys.org）：https://phys.org/news/2023-01-capitalize-power-perception-beliefs-brand.html（secondary，search-snippet）

**S13** 直接拿企業採購者（B2B）或服務業做標誌造形實驗的研究幾乎查不到
- The visual language of brand logos（IDEAS，消費者樣本）：https://ideas.repec.org/a/eee/jbrese/v200y2025ics0148296325004035.html（primary，abstract）
- Kennesaw 州立大學期刊：服務廣告的抽象與具象圖像：https://digitalcommons.kennesaw.edu/amj/vol12/iss1/1（primary，search-snippet）
- Marketing Trends 2011（Machado，服務與有形標誌論述）：https://rdpc.uevora.pt/bitstream/10174/4075/1/Marketing%20Trends%202011%20-%20Joana%20Cesar%20Machado.pdf（primary，search-snippet）
- 工業工程公司標誌內容分析（IEOM 2025 會議）：https://ieomsociety.org/proceedings/saudiarabia2025/208.pdf（primary，search-snippet）
- Shape matters: How logo shapes influence consumer reactions（PolyU，航空例）：https://www.polyu.edu.hk/cpa/excel/en/201607/research/r2/index.html（secondary，search-snippet）

**S14** 系統性文獻回顧顯示：標誌研究裡以「形狀」為主題的最多，近年重心從「認不認得」轉向「造形帶來什麼意義」
- A comprehensive review on logo literature（JMM DOI）：https://doi.org/10.1080/0267257x.2019.1604563（primary，search-snippet）
- Forty Years of Brand Logo Literature（IDEAS）：https://ideas.repec.org/a/eee/jbrese/v200y2025ics0148296325004783.html（primary，abstract）
- ブランド・ロゴにおける視覚的要素に注目した研究の整理（日本大學）：https://www.bus.nihon-u.ac.jp/wp-content/themes/nichidai/assets/img/unique/laboratory/kiyo/94_HisashiKawamata.pdf（primary，abstract）
- Logo Impact on Consumer's Perception… A 5 Years Systematic Review（hrmars）：https://hrmars.com/papers_submitted/20084/logo-impact-on-consumers-perception-attitude-brand-image-and-purchase-intention-a-5-years-systematic-review.pdf（secondary，search-snippet）

**S15** 這批造形實驗多用虛構品牌、學生或線上受試者，本輪幾乎都只讀到摘要
- Seeing Is Not Perceiving（arXiv 2026）：https://arxiv.org/pdf/2609.25677（secondary，search-snippet）
- The AI Eye: LLMs vs Human Perception in Visual Marketing（墨爾本大學）：https://fbe.unimelb.edu.au/research/lab/behavai/news-and-events/past-events/the-ai-eye-llms-vs-human-perception-in-visual-marketing（secondary，search-snippet）
- Researchers Want to Help You Design More Successful Logos, But Do They Have Good Advice?（AIGA Eye on Design）：https://eyeondesign.aiga.org/researchers-want-to-help-you-design-more-successful-logos-but-do-they-have-good-advice/（secondary，search-snippet）
- Effects of logo element congruence on brand traits and evaluations（Twente 碩士論文）：https://essay.utwente.nl/essays/77995（primary，search-snippet）

**T01** 字體給人的印象可歸成「好看、有趣、可靠、醒目」四種，背後由六個字形特徵決定：繁複、和諧、自然、花飾、粗重、窄縮
- Impression Management using Typeface Design（SAGE 期刊頁）：https://journals.sagepub.com/doi/abs/10.1509/jmkg.68.4.60.42736（primary，search-snippet）
- Impression Management using Typeface Design（Semantic Scholar 摘要）：https://www.semanticscholar.org/paper/Impression-Management-using-Typeface-Design-Henderson-Giese/fd9f9e6361205fd0b390aff29a7f881b1757085c（summary，abstract）
- Using Type Font Characteristics to Communicate Brand Personality of New Brands（ResearchGate，轉述 2004 對應關係）：https://www.researchgate.net/publication/256016577_Using_Type_Font_Characteristics_to_Communicate_Brand_Personality_of_New_Brands（secondary，search-snippet）

**T02** 對新品牌來說，字體看起來越「自然」（有機、不機械），消費者越容易讀出品牌個性
- Using type font characteristics to communicate brand personality of new brands（Springer 期刊頁）：https://link.springer.com/article/10.1057/bm.2012.23（primary，abstract）
- SSRN 摘要頁：https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2027518（primary，abstract）

**T03** 字體跟產品「搭」的時候，品牌被選中的次數約是不搭時的兩倍
- Font appropriateness and brand choice（Cardiff ORCA 典藏）：https://orca.cardiff.ac.uk/id/eprint/2577/（primary，abstract）
- Dressed for the occasion: Font-product congruity in the perception of logotype（Cardiff ORCA 典藏）：https://orca.cardiff.ac.uk/id/eprint/2571/（primary，abstract）
- IDEAS/RePEc 書目：https://ideas.repec.org/a/eee/jbrese/v57y2004i8p873-880.html（summary，abstract）

**T04** 字體本身就帶意思，跟廣告圖片和文案說的一致時，消費者比較記得住廣告訴求
- All Dressed Up With Something to Say（全文 PDF，makinggood.ac.nz 轉載）：https://www.makinggood.ac.nz/media/1254/childers-and-jass-2002-all-dressed-up-with-something-to-say-effects-of-t.pdf（primary，abstract）
- 文字的「偷心術」：營銷中的字體效應（心理科學進展 2021）：https://journal.psych.ac.cn/xlkxjz/CN/Y2021/V29/I2/365（secondary，abstract）

**T05** 在中國大陸與新加坡做的標誌評價顯示，「有層次（摘要用 elaborate）、自然、和諧」的圖形標誌帶來好感、品質感、意思
- Building strong brands in Asia（ScienceDirect 期刊頁）：https://sciencedirect.com/science/article/abs/pii/S0167811603000466（primary，search-snippet）
- Building strong brands in Asia（USP 課程網站 PDF 副本）：https://edisciplinas.usp.br/mod/resource/view.php?id=2253173（primary，abstract）
- Guidelines for Selecting or Modifying Logos（Henderson & Cote 1998 摘要 PDF）：https://newion.uwinnipeg.ca/~ssingh5/Lm/logo-guide.pdf（primary，abstract）

**T06** 十國資料顯示人看標誌的三個基本維度（繁複、自然、和諧）各國一樣
- Cross-National Logo Evaluation Analysis（作者版 PDF，HKUST）：http://www.bm.ust.hk/mark/files/staff/Ralf/Ralf-MS-2009.pdf（primary，search-snippet）
- Cross-National Logo Evaluation Analysis（SSRN）：https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1265991（primary，abstract）
- INFORMS 期刊頁：https://pubsonline.informs.org/doi/suppl/10.1287/mksc.1080.0462（primary，search-snippet）

**T07** 同樣是黑體、宋（明）體、楷體，中國大陸和台灣受測者對「古典還是現代」的感受方向相反
- Emotions of Simplified and Traditional Chinese Typeface（J-STAGE）：https://www.jstage.jst.go.jp/article/isase/ISASE2020/0/ISASE2020_1_35/_article（primary，abstract）
- ISASE 2020 論文 PDF（研討會網站）：https://www.isase-ke.org/isase_wp/wp-content/uploads/isase2020-29_compressed.pdf（primary，search-snippet）
- Emotional Responses to Chinese Characters（ResearchGate 摘要）：https://www.researchgate.net/publication/346213117_Emotional_Responses_to_Chinese_Characters_Exploration_for_Simplified_Traditional_Chinese_and_Japanese_Typefaces（primary，abstract）

**T08** 台灣受測者認為楷體最能代表台灣、細明體代表中國，日本受測者卻把楷體歸給中國
- HUANG Yao-Ming 2023 博士論文英文摘要 PDF（岩手大學典藏）：https://iwate-u.repo.nii.ac.jp/record/2000123/files/(abstract)HUANG-Yao-Ming-2023-T.pdf（primary，search-snippet）
- HUANG Yao-Ming 2023 博士論文要約 PDF：https://iwate-u.repo.nii.ac.jp/record/2000123/files/(summary)HUANG-Yao-Ming-2023-T.pdf（primary，search-snippet）
- Aesthetic evaluation and the perceived properties of Chinese characters（PLOS ONE 2025，PMC）：https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11785276/（primary，abstract）

**T09** 台灣的字體意象研究發現：常見字體適用範圍廣但沒有獨特個性，特色鮮明的字體傳達感受清楚但能用的場合窄
- 中英字型意象之研究（Airiti Library）：https://www.airitilibrary.com/Article/Detail/a0000537-201206-201210260030-201210260030-673-691（primary，abstract）
- 標題中文字體與商業管理類書籍訴求意象之符合程度探討（Airiti Library）：https://www.airitilibrary.com/Publication/alDetailedMesh?docid=16835891-201506-201510290005-201510290005-177-196（primary，abstract）

**T10** 日本的資料大致指向：有毛筆筆勢的明朝體讓人覺得可信，低對比的黑體（ゴシック）讓人覺得創新
- Typography Matters: New Research Reveals How Fonts Make Us Feel Depends on Where We Live（Monotype 新聞稿）：https://www.monotype.com/company/press-release/typography-matters-new-research-reveals-how-fonts-make-us-feel-depends-where（secondary，search-snippet）
- MT_NeuronsReport_JP（Monotype 日文報告 PDF）：https://cms-prod.monotype.com/sites/default/files/2023-06/MT_NeuronsReport_JP.pdf（secondary，search-snippet）
- Differences in Ratings of Impressions between Japanese Calligraphic Styles and a Japanese Font（千葉大學典藏）：https://opac.ll.chiba-u.jp/da/curator/102571/（primary，abstract）

**T11** 圓潤的字形容易讓人聯想到「甜」、也比較討喜，用在享樂型產品上會提高偏好
- The taste of typefaces in different countries and languages（BI 開放典藏 PDF）：https://biopen.bi.no/bi-xmlui/bitstream/handle/11250/2499581/The%20tase%20of%20typefaces%202018.pdf?sequence=4（primary，abstract）
- The taste of typeface（Royal Holloway 典藏）：https://pure.royalholloway.ac.uk/en/publications/the-taste-of-typeface/（primary，abstract）
- The typeface curvature effect（XJTLU Scholar）：https://scholar.xjtlu.edu.cn/en/publications/the-typeface-curvature-effect-the-role-of-typeface-curvature-in-i/（primary，abstract）

**T12** 手寫感字體會讓人覺得「背後有人」，因而對產品更有感情、評價更好
- Humanizing Products with Handwritten Typefaces（作者網站全文 PDF）：https://www.dhruvgrewal.com/wp-content/uploads/2018/05/2018-JCR-Font-2.pdf（primary，search-snippet）
- Humanizing Products with Handwritten Typefaces（Scinapse 摘要）：https://www.scinapse.io/papers/2789419113（summary，abstract）
- Use handwritten fonts to increase…（Science Says 摘要，數字未證實）：https://app.sciencesays.com/p/use-handwritten-fonts-to-increase（summary，search-snippet）
- The Power of the Pen（休士頓大學新聞稿）：https://bauer.uh.edu/news/2020/the-power-of-the-pen/（secondary，search-snippet）

**T13** 手寫字標的「人味」也有代價：出事時，消費者對手寫字標品牌的責怪比機器字體品牌更重
- Do products branded with handwritten scripts suffer more amid product-harm crises?（北京理工大學 Pure）：https://pure.bit.edu.cn/en/publications/do-products-branded-with-handwritten-scripts-suffer-more-amid-pro/（primary，abstract）
- Why every restaurant has an illegible menu（Fast Company）：https://www.fastcompany.com/90310920/why-every-restaurant-has-an-illegible-menu（secondary，search-snippet）

**T14** 用繁體漢字做的實驗發現，復古字體能提高品牌的「酷」與懷舊感、進而提升地位感，但做成書法風格反而削弱這個效果
- How vintage typography shapes brand status（Emerald 期刊頁）：https://www.emerald.com/jpbm/article-abstract/35/4/602/1318990/How-vintage-typography-shapes-brand-status?redirectedFrom=fulltext（primary，search-snippet）
- Typography Talks（Journal of Marketing，SAGE）：https://journals.sagepub.com/doi/10.1177/00222429231215357（primary，search-snippet）
- 老字號品牌創新設計（漢斯出版 PDF）：https://pdf.hanspub.org/design202492_521180974.pdf（secondary，search-snippet）
- Brand identity construction through the heritage of Chinese destination logos（De Gruyter）：https://www.degruyterbrill.com/document/doi/10.1515/sem-2023-0138/html（primary，search-snippet）

**T15** 中國大陸流行的「江湖體」書法招牌字被書法界、評論界批為誤解筆法、俗套的「刻奇中國風」，2025 年甚至出現禁用提案與官方
- China to Hunt Down 'Incorrect and Non-Standard' Fonts（Sixth Tone）：https://www.sixthtone.com/news/1010091（secondary，search-snippet）
- 江湖體相關評論（36氪）：https://36kr.com/p/3371341969723654（secondary，search-snippet）
- 江湖體相關評論（鳳凰網）：https://i.ifeng.com/c/8jIHNcD2zQ4（secondary，search-snippet）
- 那個讓人想到台灣的字體（justfont blog）：https://blog.justfont.com/2016/06/liu-kai-ti/（secondary，search-snippet）
- 台灣字體復興／字體是文字的靈魂（中央廣播電臺）：https://rti.org.tw/news?pid=220233&uid=3（secondary，search-snippet）

**T16** 中文品牌名主要靠「字的樣子」被記住與評價，英文品牌名主要靠「聲音」
- Language and Brand Attitudes: Impact of Script and Sound Matching in Chinese and English（中歐商學院典藏）：https://repository.ceibs.edu/en/publications/language-and-brand-attitudes-impact-of-script-and-sound-matching-（primary，abstract）
- Language and Consumer Memory（IDEAS/RePEc）：https://ideas.repec.org/a/oup/jconrs/v21y1994i3p419-31.html（primary，abstract）
- Auditory and Visual Brand Identifiers in Chinese and English（作者版 PDF，Columbia）：https://business.columbia.edu/sites/default/files-efs/pubfiles/855/Brand_Identifiers_Tavassoli_Han.pdf（primary，abstract）

**T17** 中英雙品牌名的效果取決於強調哪一個：台灣實驗中英文名讓品牌顯得較國際化，中文名則在親切、信任、喜歡上得分較高
- Creating local brands in multilingual international markets（Columbia 研究頁）：https://business.columbia.edu/faculty/research/creating-local-brands-multilingual-international-markets（primary，abstract）
- The Effectiveness of Using a Global Look in an Asian Market（WARC）：https://www.warc.com/Content/a54e3bd5-a51e-43c3-bd55-2b3c27c5c7ee（primary，abstract）
- 同篇（政治大學典藏）：https://ah.lib.nccu.edu.tw/handle/140.119/56993（primary，abstract）

**T18** 一項雙語品牌字標實驗發現：中文名字級較大時品牌態度較好，中英等大次之，英文較突出時最差
- Effects of typographic variables on attitude measures in reading bilingual brands（Iowa State 典藏）：https://dr.lib.iastate.edu/handle/20.500.12876/28272（primary，abstract）

**T19** 中英雙語排版目前有描述框架、沒有消費者實驗：譚智恒（Keith Tam）把中英文的排版屬性拆成 76 項對照
- A descriptive framework for Chinese–English bilingual typography（作者網站）：https://keithtam.net/bilingual-framework/（primary，abstract）
- 同篇（VTC 典藏）：https://repository.vtc.edu.hk/ive-de-sp/84（primary，abstract）
- Tencent expands global presence（Monotype 案例）：https://enterprise.monotype.com/resources/case-studies/tencent-expands-global-presence（secondary，search-snippet）
- Building brand identity in China through typography（Labbrand）：https://www.labbrand.com/insights/article/building-brand-identity-in-china-through-typography.html（secondary，search-snippet）

**T20** 「英文大寫字母高度為中文字高二分之一、小寫為八分之三」確有其條文，出處是交通部《道路交通標誌標線號誌設置規則》第 15 
- 道路交通標誌標線號誌設置規則（臺北市法規系統條文）：https://laws.gov.taipei/law/LawSearch/LawArticleContent/FL012456（primary，search-snippet）
- 同規則附件（臺北市法規系統，2022-08-19 版 ODT）：https://www.laws.taipei.gov.tw/lawatt/Law/A040110050001900-20220819-15000-001.odt（primary，search-snippet）
- 道路交通標誌標線號誌設置規則（民國 78 年版，維基文庫）：https://zh.wikisource.org/wiki/%E9%81%93%E8%B7%AF%E4%BA%A4%E9%80%9A%E6%A8%99%E8%AA%8C%E6%A8%99%E7%B7%9A%E8%99%9F%E8%AA%8C%E8%A8%AD%E7%BD%AE%E8%A6%8F%E5%89%87_(%E6%B0%91%E5%9C%8B78%E5%B9%B4)（primary，search-snippet）

**T21** 對還沒人認識的品牌，圖形加名字比只有其中一樣更好：圖形加名字被評得較好看，圖形的記憶優勢也只在認識名字的人身上出現
- New brand logo design: customers' preference for brand name and icon（IDEAS/RePEc）：https://ideas.repec.org/a/pal/jobman/v24y2017i5d10.1057_s41262-017-0046-4.html（primary，abstract）
- Memory for Symbolic Images: Findings From Sports Team Logos（滑鐵盧大學實驗室 PDF）：https://uwaterloo.ca/memory-attention-cognition-lab/sites/default/files/uploads/documents/jarmac-2023-roberts.pdf（primary，search-snippet）
- Brand logos versus brand names: A comparison of the memory effects（Swansea 開放全文）：https://cronfa.swan.ac.uk/Record/cronfa59789（primary，abstract）
- What's in a name（Penn State Smeal 院刊）：https://magazine.smeal.psu.edu/whats-in-a-name/（secondary，search-snippet）
- Comparing direct and indirect branding in advertising（Adelaide 典藏）：https://digital.library.adelaide.edu.au/items/8d4cb059-1ba0-480e-a2a8-4ad9f66f977d（primary，abstract）

**T22** 標誌若用文字或圖形直接說明「做什麼的」，對不知名品牌的評價、購買意願與實際績效較有利
- Let the logo do the talking（作者稿，Sussex Figshare）：https://sussex.figshare.com/articles/journal_contribution/Let_the_logo_do_the_talking_the_influence_of_logo_descriptiveness_on_brand_equity/23483705（primary，abstract）
- 同篇（Westminster 典藏）：https://westminsterresearch.westminster.ac.uk/item/qqv8q/let-the-logo-do-the-talking-the-influence-of-logo-descriptiveness-on-brand-equity（primary，abstract）
- Logos with Descriptive Elements are More Likely to Improve Brand Performance（The Fashion Law）：https://www.thefashionlaw.com/logos-with-descriptive-elements-are-more-likely-to-improve-brand-performance-per-new-study/（secondary，search-snippet）

**T23** 標誌外框的意義會隨購買風險改變：高風險購買時框被讀成「保護」、提高購買意願，低風險時被讀成「拘束」、降低購買意願
- Brand logo frames（IDEAS/RePEc 書目）：https://ideas.repec.org/a/oup/jconrs/v43y2016i4p549-566..html（primary，abstract）
- Brand Logo Frames: How and When（Miami 典藏）：https://scholarship.miami.edu/esploro/outputs/journalArticle/Brand-Logo-Frames-How-and-When/991031623948302976（primary，abstract）

**T24** 字形細節各有意義：斜體字標讓人覺得產品見效快（粗字會削弱）、大寫讓品牌顯得較高檔、對中國消費者而言襯線字顯得活潑、無襯線
- The impact of logo typeface obliqueness on product efficacy perception（PolyU 研究入口）：https://research.polyu.edu.hk/en/publications/the-impact-of-logo-typeface-obliqueness-on-product-efficacy-perce/（primary，abstract）
- 她的優博論文發現，品牌字體竟如此「別有用心」（浙大管理學院）：http://www.som.zju.edu.cn/2023/0316/c63473a2729330/page.htm（secondary，search-snippet）
- The Effect of Serif and San Serif Typeface of Luxury Fashion Logotype on Chinese Consumers' Brand Perception（ResearchGate）：https://www.researchgate.net/publication/366393144_The_Effect_of_Serif_and_San_Serif_Typeface_of_Luxury_Fashion_Logotype_on_Chinese_Consumers'_Brand_Perception（primary，search-snippet）

### 中文標準字（全文，在梁特助電腦上讀）
- D01 https://blog.justfont.com/2018/07/jf-typeclass-intro-1/
- D02 https://blog.justfont.com/2012/12/hanzi-type-design-1/
- D03 https://blog.justfont.com/2014/05/glyph-font-vs-hanz/
- D04 https://blog.justfont.com/2020/02/how-to-match/
- D05 https://blog.justfont.com/2013/12/popular-typography/
- D06 https://blog.justfont.com/2013/05/popular-typography-2/
- D07 https://blog.justfont.com/2024/12/designbychentunhua/
- D08 https://blog.justfont.com/2021/11/greenvines-new-logotype/
- D09 https://www.thenewslens.com/article/51205
- D10–D14 森澤字體辭典 https://www.morisawa.co.jp/culture/dictionary/
- D15 武藏野美術大學 造形ファイル（ロゴタイプ設計）https://zokeifile.musabi.ac.jp/
- D16 武藏野美術大學 美術・デザイン用語 https://art-design-glossary.musabi.ac.jp/?p=336

### 字高與遠看（全文，在梁特助電腦上讀，每頁轉圖看過）
- E04 United States Sign Council，招牌面積與字高公式、Legibility Index 表 1（頁面 © 2006）
- E01 招牌視認距離補充文件（第 14–19 頁：LI 定義、壅塞係數、行車折減）
- E07 道路交通標誌標線號誌設置規則摘錄（第 15、150 條）
- E08、E14 日本國土交通省 道路標識設置基準、標識令別表第 2
- E12 村重至康 2016，IATSS Review（高速道路標識改版與判讀距離實驗）

### 中文排版與 skill（雲端直接讀）
- W3C clreq：https://github.com/w3c/clreq （https://raw.githubusercontent.com/w3c/clreq/gh-pages/index.html）
- anthropics/skills canvas-design、brand-guidelines、theme-factory：https://github.com/anthropics/skills/tree/main/skills
- wholiver/swiftui-design-skill（MIT）：https://github.com/wholiver/swiftui-design-skill
- uxKero/anydesign：https://github.com/uxKero/anydesign
- awesome 清單：https://github.com/ComposioHQ/awesome-claude-skills 、https://github.com/travisvn/awesome-claude-skills
