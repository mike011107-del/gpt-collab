# LOGO 設計邏輯優化

查大品牌中文字 LOGO、國外大廠 LOGO 與權威資源後，Claude 改寫的做法  
2026-11-03，給梁特助

> PDF 版（14 頁 A5，含外部標誌對照圖）在專案資料夾 `崧淳CI/LOGO設計邏輯優化_20261103/`。外部標誌屬各公司商標，不放公開庫；本檔是文字版。重建方式見 `程式/重建方式.txt`。

## 結論

1. 大品牌的中文字標，幾乎都是字體設計師做的，或有字體設計師參與。京東的品牌字體由方正字庫從原 Logo「京東」二字演化，再調橫豎比例；小米 MiSans、華為 HarmonyOS Sans 由漢儀參與設計；台電新標準字由聶永真工作室整理比例，保留原字帖的中宮與端點；資生堂的新進設計師要用社內教本手寫練字一年。沒有一家是打一套字、或用程式拼直線。
2. G1 到 G3 的字爛，主因是做法錯，跟筆畫粗細比沒有直接關係。大品牌字標的橫直比從 0.4 到 1.0 都有（淘寶對比很強，小紅書幾乎等粗），共同點是收筆、轉角、交接全按同一套規則畫過，大小與字距逐字調過。G1 到 G3 是等粗直線加方頭、尖角、沒有收筆，這些修正一項都沒做。
3. 圖形部分普通，是因為只做了第一個想法。Chermayeff & Geismar & Haviv 一律先做黑白剪影，所有方案攤開來比，選一個，其餘丟掉；FedEx 做了 200 多個設計，才收斂到 6 個給客戶看。G1 到 G3 每組只畫一張，而且先決定了顏色怎麼放。
4. 大品牌的中文字 LOGO 有三種做法：整組字訂製成字標（美團、小紅書、淘寶、台電）、把一個字畫成符號（支付寶「支」、豆瓣「豆」、中國銀行「中」）、字標旁配一個不是字的圖形（國航鳳凰）。崧淳是新公司，沒有人認得它的圖形，所以字標是主角，每個地方都會出現，字標的做工比圖形更要緊〔推論〕。
5. 新的做法分七步，已寫進專案 skill（logo-design-logic），以後每次做 LOGO 都照這個流程，見第四節。
6. 要你決定一件事：字標的骨架從哪裡來（第六節）。10-11 你說要原創字型；這次查到，大品牌多數是從既有字形改畫，或請字型公司重做。

證據等級：〔轉述〕新聞、訪談、書評；〔搜尋摘要〕這次只讀到搜尋結果，沒有打開全文；〔實測〕Claude 自己量的；〔推論〕Claude 推的。同一件事少於 3 個不同來源的，標「佐證不足」。這一輪大多只讀到搜尋摘要，沒有讀到書和文章全文。

## 一、大品牌中文字 LOGO 怎麼做

（圖 1 在 PDF：美團、小紅書、淘寶、UNIQLO 片假名、支付寶「支」、豆瓣「豆」、知乎「知」、國航。外部標誌不放公開庫。）

### 做法一　整組字訂製成字標

- 京東：品牌字體「京東朗正體」由方正字庫主導，主創是汪文、仇寅。字形從京東原 Logo 的「京東」二字演化，再調整橫豎比例〔搜尋摘要〕。

- 小米 MiSans、華為 HarmonyOS Sans：由漢儀字庫參與設計。iF 設計獎的署名是小米 MIUI 設計團隊加漢儀字庫〔搜尋摘要，ifdesign.com、鈦媒體、IT之家〕。

- 阿里巴巴普惠體：西文部分由 Monotype 字體總監小林章主導，中文部分由漢儀主創陶一泓主導〔搜尋摘要〕。

- 台電：新標準字由聶永真的永真急制設計工作室做，2024-01-15 決標，約 96.8 萬元。他說原本的六個字是從于右任字帖集字、排列、描圖而成，新版保留原字帖「中宮」與「端點」的特點。台電說明這次是整理字體比例與視覺系統，新舊並存、逐步替換〔轉述，NOWnews、ETtoday、聯合報、新頭殼，2026-05〕。字源說法有爭議：華梵大學黃智陽教授說 1953 年確有邀于右任題字。

- 資生堂：細長的「資生堂書體」源自小村雪岱，他 1918 到 1923 年在資生堂意匠部。現在分到創意本部的設計師，全員用社內教本手寫練一年，從自己的名字練起〔轉述，日刊工業新聞 newswitch、資生堂花椿、資生堂企業網站〕。

### 做法二　把一個字畫成符號

- 中國銀行：靳埭強 1980 年受託。方孔古錢是外形，中間方孔加上下兩條直線，整體成「中」字；1986 年總行定為行標〔轉述，澎湃新聞；佐證不足〕。

- 支付寶的「支」、豆瓣的「豆」、知乎的「知」都是單字畫成方塊或圖形（圖 1）。字一旦變成形狀，就不會跟旁邊的名字一起被當成一行字讀。G1、G2 的「山」沒有畫成形狀，所以被讀成「山崧淳」（上一份報告 A3）。

### 做法三　字標旁配一個不是字的圖形

- 小米 2021 年新標誌由原研哉設計，官方說前後三年；外框從方形改成介於圓和方之間的「超橢圓」，字母標重畫〔轉述，商業周刊、自由時報、數位時代、IT之家〕。設計費 200 萬人民幣的說法小米沒有證實。

- 原研哉做的長崎縣美術館符號，是從美術館建築石材百葉的節奏抽出來的圖形〔轉述，長崎縣美術館網站；佐證不足〕。圖形取材自這個機構自己的真實物件，不是通用的意象。

### 中文字標的做工細節（中文來源）

- 骨架決定筆畫位置、長短、弧度，也決定比例與重心。主筆是視覺上較重要的筆畫，要粗；副筆次要，可以減細；外圍、較長的筆畫通常是主筆。先試做幾個代表字，再擴充〔轉述，justfont 字體口袋書〕。

- 中文沒有基線。一般標準字會把頂部和底部對齊，但字體設計師會依節奏微調，例如「灣」的鉤刻意往下沉，做視覺上的過衝〔轉述，許瀚文在 The News Lens 修改台灣啤酒標準字的文章；佐證不足〕。

- 字身與字面：每個字填滿同一個框，看起來不會一樣大，「國」這種方正的字會顯大，要依字形縮放〔依一般知識，未查證〕。

- justfont 做綠藤生機標準字時，提案前先照英文字體的筆畫粗細，實驗出能搭配的線條粗細，才開始畫〔轉述，justfont 部落格；佐證不足〕。崧淳也有英文名，中英文要一起定粗細。

- 筆畫做減法（簡化、斷開）是中文字標常見手法〔搜尋摘要，Canva 中文站；佐證不足〕。

## 二、國外大廠字標怎麼做

（圖 2 在 PDF：西門子、日立、東芝、Epson、FedEx、Samsung、Panasonic、3M、ABB、Caterpillar、Sony、Kyocera 字標。）

- FedEx（1994）：Landor 的 Lindon Leader 從 Univers 67 Bold Condensed 與 Futura Bold 起手，兩套字都排不出乾淨的箭頭，於是改畫字母，一對一對調字距，直到 E 和 x 之間的空白變成箭頭。他說箭頭一開始根本沒想到。做過的設計有「200 多個，收到 6 個」與「400 多個」兩種說法〔轉述，The Sneeze 訪談、CNN、Retail Brew〕。

- Google（2015）：字標以自家 Product Sans 為底再改，最明顯的是斜切的 e，讓字標跟產品名分得開〔轉述，Google Design、Typeroom、Wikipedia〕。

- 賓士：Kurt Weidemann 1987 年起任 Daimler-Benz 企業識別顧問，1985 到 1990 年間設計三套專用字體 Corporate A·S·E；AGI 收錄他 1988 年用黃金分割做的賓士標誌〔轉述，AGI、MyFonts、Luc Devroye 字體資料庫〕。

- Mastercard：2016 年 Pentagram 改版，字標移到兩個圓的下方、改小寫；2019 年做了 20 多個月的全球調查，超過 80% 的人不看名字也認得兩個圓，才把名字拿掉〔轉述，Dezeen、Design Week、Marketing Dive、Mastercard 新聞稿〕。

- 字型公司 TypeTogether：「安裝一套字型、打出品牌名稱，不會變成 logo」，因為字型的字距是為了跟任何字母相鄰而設計的，字標要重新調〔轉述，type-together.com；佐證不足〕。

| 字標 | 量的字 | 直筆 | 橫筆 | 橫÷直 |
|---|---|---|---|---|
| 日立 HITACHI | 「H」 | 65 | 40 | 0.62 |
| 西門子 SIEMENS | 「E」 | 66 | 42～49 | 0.64～0.74 |
| 東芝 TOSHIBA | 「O」 | 67 | 55 | 0.82 |
| Epson | 「E」 | 76 | 64～65 | 0.84～0.86 |
| 美團 | 「美團」 | 68～72 | 52～56 | 0.72～0.82 |
| 淘寶 | 「淘寶」 | 104～124 | 48～52 | 約 0.4～0.5 |
| 小紅書 | 「小紅書」 | 104～108 | 104 | 約 1.0 |
| 思源黑體 Bold | 「崧淳」 | 68～76 | 58～64 | 0.80～0.87 |
| 崧淳 G1 到 G3 | 「崧淳」 | 24 | 24 | 1.00 |

圖 3：Claude 11-03 把 simple-icons 的字標放大到 1600px 後掃描像素量的（單位是像素，只比比值）。看起來等粗的西文字標，橫筆也比直筆細 15% 到 38%。中文字標從 0.4 到 1.0 都有；小紅書幾乎等粗也成立，因為收筆、轉角、斜度全組一致。G1 到 G3 的問題不在 1.00，在於等粗之外什麼修正都沒做。

## 三、國外大廠圖形標怎麼做

（圖 4 在 PDF：三菱、Chase、德意志銀行、VW、Lufthansa、德國郵政、Shell、中國鐵路、Toyota、Bosch、Mastercard、Scania。）

- Sagi Haviv（Chermayeff & Geismar & Haviv 合夥人）三條：一、合適，不是表達很多，好標誌說不了多少；二、獨特好記，看一兩次就能跟別人描述，或憑記憶畫出來；三、簡單，任何像素尺寸都能用。他說「做出簡單又獨特的東西最難」〔轉述，The Futur 影片、logodesignlove 訪談、Skillshare 課程〕。

- Tom Geismar：一律從黑白開始，因為顏色會分散注意；把標誌當剪影看；給客戶看也是黑白。合夥人討論所有選項，共同挑最好的，其餘丟掉〔轉述，Creative Bloq、logogeek 訪談、Print 雜誌〕。

- Paul Rand 1991 年〈Logos, Flags, and Escutcheons〉列七個條件：獨特、看得見、好用、好記、通用、耐用、不過時。標誌要跟產品或公司連在一起才有意義；賓士星標跟汽車無關，它是好標誌，因為它代表好產品〔搜尋摘要，paulrand.design 原文頁、brandknewmag、The Next Web〕。

- 賓士星標：1909 年申請三芒星和四芒星商標，只用了三芒星，三芒代表陸、海、空的動力。加圓環與立體版的年份，各來源說法不一〔轉述，motor1、logodesignlove、fabrikbrands〕。

對崧淳的意思〔推論〕：你在 Q45 選了賓士當「高一檔」的例子。賓士的高一檔，來自比例準、做工細、一百多年沒換，而不是星標的意義。崧淳的圖形求合適、好記、縮小能用；高級感要靠字標做工和之後每次用都一致。

## 四、新的 LOGO 設計流程（七步）

### 1　一句話任務

寫一句：誰會看到（管委會、民間業主、公部門承辦）、在哪裡看到（車門、報價單、名片、報告封面）、第一眼要認出什麼。Q43 你說第一個要想到公司做的事：這件事交給「字標＋業務行」（例如「污水下水道清淤・CCTV 管內檢視」）去說，圖形只取一個形，不畫成插圖。

### 2　選標誌類型

崧淳是新公司，圖形一律跟全名一起出現；字標是主角。三種做法（第一節）都可以比，但「把字畫成符號」只能選崧或淳其中一個字，而且要畫成形狀，不能是一個看得懂的字放在名字旁邊。

### 3　黑白剪影探索

先列 8 到 12 種構成方法（重複旋轉、負空間、一筆線、截面、切割、字畫成形），配上真實取材（人孔、管截面、CCTV 鏡頭與畫面、崧字的山頭），每種畫 3 到 5 個小圖，總共 30 個以上。不上色、不放字。誰畫：AutoIP 或 GPT 出圖（不放中文字），Claude 寫交辦。

### 4　篩選

Claude 先刪：跟國外 48 家、台灣 21 家同行並排比；縮到 16px 看；看 5 秒蓋起來，能不能說出來、畫出來；Rand 七條；上一份報告的 14 條對照表。留 6 到 9 個給你挑 1 到 2 個。

### 5　字標

- 骨架照第六節你選的方式來。

- 先定風格：粗細對比強或接近等粗，要刻意選，選了就全組一致。

- 收筆、轉角、交接、點的形狀定成一套規則，每一筆都照這套規則畫。

- 逐字調大小與重心（崧筆畫多、淳左右結構，填滿同一框不會一樣大），中宮放或收要一致。

- 一對一對調字距，中文名、簡稱、英文名一起定粗細。

- 反白版修細，小尺寸版加寬字距。放大到 A4 看接筆，縮到 6mm 高看還讀不讀得出來。

### 6　組合

圖形與字標的大小比、間距（用字高當單位）、橫式與直式、單色版、最小尺寸，各做一版。

### 7　提案

先交黑白，你挑定方向才上色（11-03 已定四色）。交件附對照表，每條寫過或沒過，有沒過的就不交。實物模擬（車門、名片）等你要再做。

## 五、以前的做法跟現在的差別

| 項目 | 這次的做法 | 改成 |
|---|---|---|
| 出發點 | 「崧」字裡有山，就畫山 | 先寫一句「誰、在哪裡、第一眼認出什麼」；做的事交給字標和業務行，圖形求合適 |
| 探索量 | 3 個方向就交件 | 數十個黑白小圖，收斂成 6 到 9 個給你挑 |
| 顏色 | 先定四色怎麼放 | 先黑白剪影，挑定方向才上色 |
| 字標 | 程式拼等寬直線，方頭、尖角、沒有收筆 | 骨架照第六節選的方式；粗細風格刻意選定；收筆、轉角、交接一套規則；逐字調大小重心、逐對調字距 |
| 圖形 | 用字（山）當圖形 | 一個構成方法；看一兩次就畫得出來；任何尺寸都能用 |
| 檢查 | 縮小、反白、車身三項量測 | 加上同業並排、憑記憶畫、Rand 七條、PR #49 的 14 條對照表 |
| 誰畫 | Claude 自己畫完交 | 圖形草圖交 AutoIP／GPT（不放中文字）；字標照第五節你選的方式；Claude 寫交辦、篩選、驗收 |

## 六、下一步，與要你決定的事

### 要你決定：字標的骨架從哪裡來

- A　開源字型當骨架再改畫（建議）。用思源黑體或思源宋體，授權是 SIL OFL，授權方 SIL 的 FAQ 寫明可以拿來做 logo，用字型做出來的圖由做的人擁有〔搜尋摘要，openfontlicense.org、OFL-FAQ，同一來源〕。FedEx 就是從現成的 Univers、Futura 改起；京東的品牌字體則是從自己舊 Logo 的字演化。要改到夠多，才不像別家也能打出來的字；要註冊商標前，請律師看。這跟 10-11「原創字型」不同，所以要你點頭。

- B　維持完全原創，Claude 從零重畫，改用曲線並加上視覺修正。這輪 G1 到 G3 就是走這條路，品質風險最高。

- C　請字體設計師做標準字，Claude 寫需求與驗收標準。大品牌都這樣做；費用與人選待確認。

### 接下來會出的東西

- 字標：你選 A，Claude 先出 3 個骨架方向的黑白字標比較頁（黑體骨、宋體骨、延續車身的楷書骨），每個附第五步檢查結果。這一批不花點數。

- 圖形：照第三步，建議先用 AutoIP 試 1 張「一張圖 9 個小圖」的黑白探索圖（20 點），能用再擴到 4 張（約 80 點），比一張圖一個方向省。這個做法還沒試過；生圖前會先問你。

## 七、以後要查的權威資源

這次只讀到書目與摘要，沒有讀到書的內文。

- Identify（Chermayeff & Geismar，2011）：收了數十個大品牌標誌的草圖與被否方案〔搜尋摘要〕。

- Logo Modernism（Jens Müller，Taschen 2015，432 頁）：1940 到 1980 年約 6000 個標誌，依造形分類〔搜尋摘要〕。

- Marks of Excellence（Per Mollerup，Phaidon 1997）：標誌的歷史與分類，名字標、縮寫標、各種圖形標〔搜尋摘要〕。

- Logotype（Michael Evamy，Laurence King 2012，336 頁）：字標專集〔搜尋摘要〕。

- Paul Rand〈Logos, Flags, and Escutcheons〉（1991）：原文在 paulrand.design。

- 增補新裝版《作字百景 ニュー日本もじデザイン》（グラフィック社，2025）：40 組設計師約 800 件日文作字〔搜尋摘要〕。

- justfont 字體口袋書（learn.justfont.com）：骨架、主筆、標準字章節，可線上讀。

- 許瀚文〈修改台灣啤酒標準字〉（The News Lens 51205）：中文標準字修改的逐項細節，下一步要讀全文。

- 網站：Brand New（改版評論）、logodesignlove（設計師訪談）、Chermayeff & Geismar & Haviv 作品頁。

## 八、出處

**中文字 LOGO**　京東朗正體、MiSans、阿里巴巴普惠體：tmtpost.com/6134904.html、digitaling.com/articles/224048.html、ithome.com/0/595/412.htm、ifdesign.com（MiSans）、cn.chinadaily.com.cn/a/202309/05/WS64f6f311a310936092f206af.html。台電：nownews.com/news/6827800、nownews.com/news/6827898、ettoday.net/news/20260510/3163281.htm、udn.com/news/story/6656/9498336、newtalk.tw/news/view/2026-05-08/1033997。資生堂：newswitch.jp/p/22943、hanatsubaki-journal.shiseido.com/article/3365/、corp.shiseido.com/report/jp/2021/value_creation/history。中國銀行：m.thepaper.cn/newsDetail_forward_8702781、primaltrek.com/blog/2013/02/10/chinese-coins-and-bank-logos/。小米：businessweekly.com.tw/business/blog/3006015、ec.ltn.com.tw/article/breakingnews/3485208、bnext.com.tw/article/62113/xiaomis-new-logo、ithome.com/0/560/524.htm。長崎縣美術館：nagasaki-museum.jp/english/about-us/symbolmark-logo。justfont：learn.justfont.com/pocketbook/chinese-typeface/anatomy/structure、learn.justfont.com/pocketbook/chinese-typeface/anatomy/main-stroke、blog.justfont.com/?p=10567。許瀚文：thenewslens.com/article/51205。筆畫減法：canva.cn/learn/chinese-font-logo-design-case/。

**國外字標**　FedEx：thesneeze.com/the-man-behind-the-fedex-logo/、edition.cnn.com/style/article/hidden-designs-famous-logos、retailbrew.com/stories/2022/10/07/logo-big-or-go-home-how-fedex-s-secret-arrow-was-created-accidentally。Google：design.google/library/evolving-google-identity/、typeroom.eu（Google turns 20）、en.wikipedia.org/wiki/Product_Sans。賓士字體：a-g-i.org/design/mercedes-benz、myfonts.com/collections/kurt-weidemann、luc.devroye.org/fonts-26203.html。Mastercard：dezeen.com/2019/01/10/mastercard-rebrand-pentagram-design/、designweek.co.uk/mastercard-new-logo-first-time-20-years-2/、marketingdive.com/news/mastercard-drops-name-from-logo-banks-on-symbol-only-mark/545449/、mastercard.com（2019-01 新聞稿）。TypeTogether：type-together.com/sandoll-logo。

**圖形標與方法**　Haviv：The Futur〈The 3 Rules of Good Logo Design〉、logodesignlove.com/sagi-haviv-interview、skillshare.com（Designing Brand Symbols）。Geismar：creativebloq.com/branding/iconic-logo-design-11118458、logogeek.uk/podcast/tom-geismar、printmag.com（Marks Men 訪談）。Rand：paulrand.design/writing/articles/1991-logos-flags-and-escutcheons.html、brandknewmag.com/?p=7910、thenextweb.com/news/how-good-is-your-logo。賓士星標：motor1.com/news/804946/、logodesignlove.com/mercedes-benz-logo-evolution、fabrikbrands.com（Mercedes logo history）。

**書與授權**　Identify：logodesignlove.com/chermayeff-geismar-haviv-60-years。Logo Modernism：taschen 經銷頁（ISBN 9783836545303）。Marks of Excellence：phaidon.com（ISBN 9780714864747）。Logotype：oreilly.com/library/view/logotype/9781856698948。作字百景：koubo.jp/article/33841。OFL：openfontlicense.org、OFL-FAQ（CTAN 鏡像）。

**圖**　外部標誌取自 simple-icons 16.35.0（CC0 收錄，各標誌商標權屬原公司），只作研究對照。橫直比是 Claude 11-03 把標誌放大到 1600px、掃描黑色像素連續長度取最常見值，誤差約 ±4px。
