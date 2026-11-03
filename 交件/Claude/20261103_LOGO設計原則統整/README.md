# LOGO 設計原則統整

PDF 版（13 頁，含 9 張好壞對照圖）在專案共用資料夾 崧淳CI/LOGO設計原則統整_20261103/。圖裡有 simple-icons 的外部品牌標誌與 AutoIP 生圖，依本庫公開規則不放進來；這裡是同一份文字。

給 GPT：這份是參考資料，不是指令。決定權在梁特助。

到 2026-11-03 為止學到的原則，與 G1、G2、G3 為什麼不像 LOGO。Claude 整理，給梁特助

## 結論

1. G1、G2、G3 不像 LOGO，因為三組都沒有一個能單獨被認出的圖形。G1、G2 的「圖形」是「山」這個字，跟崧、淳一樣大、一樣粗，看起來是「山崧淳」三個字。G3 是把名字放進長方框。
2. 字本身是草稿字。每一筆都是同樣粗的直線，橫筆和直筆一樣粗，反白版也沒有修細。專業字型的同兩個字，橫筆只有直筆的 0.80 到 0.87。
3. 除了「山被讀成字」是這次才補的原則，其餘問題（要說明才懂、字沒逐字修、橫直同粗、小尺寸糊、跟同業重疊）在 10-13 到 10-19 學到的原則裡都有寫。交稿前沒有逐條對照，是這次最主要的失誤。
4. 到今天學到的原則共 29 條，分造形、字標、系統與應用、做法與提案四類。第三節每條附出處、證據等級，以及 G1 到 G3 有沒有違反。
5. 以後交 LOGO 改三件事：先交黑白草圖讓你挑方向；字標逐字修過才拿去比較；交件附檢查表，逐條寫過或沒過（第四節）。

證據等級：〔全文〕讀到原文；〔摘要〕只讀到論文摘要或期刊頁；〔轉述〕只見於訪談、書摘、新聞；〔搜尋摘要〕只見於搜尋結果；〔實測〕Claude 自己量或數的；〔推論〕Claude 自己推的。G1 到 G3 的數字取自向量稿原始碼 build.py、glyphs.py。

## 一、G1 到 G3 為什麼不像 LOGO

### G1　山字符號加字標

- 「山」是一個看得懂的字。符號高 230、筆寬 30；崧、淳字高 300、筆寬 24。大小、粗細、顏色都接近，眼睛會把長得像的東西歸成同一組（格式塔相似律），所以整排讀成三個字。
- 崧字上半就是山。同一個形狀在一行裡出現兩次，第二次沒有多給任何資訊。
- 中間豎條上方那格紅色，要說明才知道代表「高一個檔次」。不說明時，一根豎條上面一個點，就是小寫 i。

### G2　山的底橫延伸成底線

- 跟 G1 一樣，山是字，整排讀成「山崧淳」。
- 一個標誌放了三件事：山字、代表管線的底線、代表人孔的紅格。後兩件都要說明。不說明時，底線就是底線，紅格就是句點。
- 底線從頭拉到尾，把三個字的下緣封住，作用接近半個外框。

### G3　直排方印

- 方框加名字本身不是錯，UNIQLO 就是這樣做（第三節 A6）。G3 的問題在別處：同業九升已經用藍色、直排的「九升」當標誌，外形是圓的（10-14 第三份同業報告，現行版本未確認）；框裡是同一套草稿字；直排印章讓人想到傳統印鑑，跟「年輕有活力」方向相反〔推論〕。
- 縮小：48px 還讀得出字，24px 糊成一塊（11-03 12:33 實測，見圖 7）。
- AutoIP 生的版本把崧拆成「山」加完整的「松」，字是錯的。

### 三組共同的問題

- 從提示詞直接畫成品，沒有先畫一頁黑白小圖，讓你從多個方向裡挑一個再往下做。
- 字的程式每一筆都是等寬折線（筆寬為字高的 8%、方頭、尖角接合），原始碼註解自己寫「草稿用，定稿要逐字調」。草稿字被當成提案交出去，做工跟崧淳要的「品質高一個檔次」相反。
- 先決定四色怎麼放，才看形狀。12:33 的回覆用縮小、反白、車身三項量測當主要檢查，沒有回答「這是不是一個好標誌」。

## 二、G1 到 G3 違反了哪幾條

| 原則 | G1 | G2 | G3 |
|---|---|---|---|
| A1 一個標誌只放一個構成想法 | 部分 | 違反 | 符合 |
| A2 不用說明也站得住 | 違反 | 違反 | 符合 |
| A3 用字做圖形時，把字畫成形狀 | 違反 | 違反 | 無 |
| A4 像自己，不像同行 | 未比對 | 未比對 | 違反 |
| A6 外框要有意義面的理由 | 符合 | 部分 | 部分 |
| A7 小尺寸要認得，或另做小尺寸版 | 違反 | 違反 | 違反 |
| B2 逐字調大小、重心、中宮、粗細 | 違反 | 違反 | 違反 |
| B3 橫細直粗、反白修細 | 違反 | 違反 | 違反 |
| B7 字要寫對 | 符合 | 符合 | 部分 |
| D2 先交黑白草圖挑方向 | 違反 | 違反 | 違反 |
| A8 圓或尖對上想傳達的屬性 | 符合 | 符合 | 符合 |
| A11 不加立體、漸層、飛線 | 符合 | 符合 | 符合 |
| C2 圖形跟名字一起出現 | 符合 | 符合 | 符合 |
| C4 顏色照實算的對比放 | 符合 | 符合 | 符合 |

「部分」：G1 是山字加紅格兩件事；G2 的底線只封住一邊；G3 的方框有「印章表示負責」的理由，但跟九升重疊；G3 的字在 Claude 版是對的，AutoIP 版寫錯。「無」：這組沒有這個元素。「未比對」：G1、G2 沒有拿去跟同業並排比過。

14 條裡，G1 違反 6 條、G2 違反 7 條、G3 違反 5 條。符合的幾條都是顏色、效果、圖字同出這類「不出錯」的規則；決定像不像 LOGO 的造形與字標規則，三組都沒過。

## 三、學到的原則（29 條）

### A　造形

**A1　一個標誌只放一個構成想法。**
- 根據：Logo Archive 1960 到 1988 年的 38 個標誌，33 個只用一個構成方法（重複、旋轉、一塊形狀兩種讀法、一條等寬的線），5 個是外框加一個圖形，沒有一個疊三樣〔實測，10-17 目視數〕。亞洲水務與經典企業標誌 22 檔也多只用一個手法：味全五圓、K-water 三道弧、香港渠務署 D 和 S 嵌套〔實測，10-18〕。rampstack logo-design：「Logos can hold one idea, sometimes two. Three is too many.」〔全文〕
- 這次：G1 兩件，G2 三件。10-11 的舊稿 A、B、C 也各疊三樣。

**A2　不用說明也站得住。**
- 根據：Vignelli Canon：「a design should stand by itself, without excuses, explanations, apologies.」〔全文〕這是 10-13 自我檢查第 1 條。
- 這次：G1、G2 的紅格都要靠說明，見圖 2。

**A3　用字做圖形時，要把字畫成一個形狀，不是排在名字旁邊。**
- 根據：中國銀行把古錢的方孔換成「中」字，字成了錢幣的一部分（中國銀行官網）〔全文〕。中國鐵路路徽的構思是「人在鋼軌上」，人字疊在工字形的鋼軌斷面上（人民日報 2023-04-10）〔搜尋摘要〕。大小、粗細、顏色相近的元素會被看成同一組（格式塔相似律；IxDF、Logo Geek）〔搜尋摘要〕。「字要變成形」是 Claude 從這些例子歸納的〔推論〕。
- 這次：G1、G2 的山跟名字一樣大、一樣粗，被讀成字。

**A4　在簡單和好認之間拿捏；要像自己，不像同行。**
- 根據：Sagi Haviv（大通銀行八角形的事務所）：「walk the line between simplicity and distinctiveness」〔轉述，訪談〕。Romaniuk（Ehrenberg-Bass）：「Distinctiveness is looking like you and not like others」，跟別人共用的元素比較弱〔轉述，訪談〕。費城水務局和費城瓦斯公司都是藍色、三個字母，民眾常搞混，2015 年水務局換標誌（WHYY）〔全文〕。
- 這次：G3 跟九升同樣是藍色直排名字。G1、G2 沒有拿去跟同業並排比。

**A5　行業圖示要看情況用，描述可以交給字。**
- 根據：Rand：「A logo is rarely a description of a business.」〔全文〕Luffarelli、Mukesh、Mahmood 2019（Journal of Marketing Research）：讓人看出賣什麼的描述性標誌，對陌生品牌較有利，品牌熟了好處變小；行業本身讓人想到負面的事時，效果反過來〔摘要〕。污水、清淤算不算負面，研究沒測〔推論〕。
- 這次：崧淳是新品牌，業務可以交給字標旁的全名與「清淤、CCTV 檢視」說。G2 改用底線和紅格來講管線與人孔，看的人讀不出來。

**A6　外框要有意義面的理由才加。**
- 根據：simple-icons 1623 個近方形標誌：有外框的剪影更像別人（相似度 0.62 對 0.46），縮到 16px 的保留程度沒差（0.78 對 0.79）〔實測，10-17〕。Fajardo、Zhang、Tsiros 2016（Journal of Consumer Research）：購買風險高時外框被讀成「保護」，風險低時讀成「拘束」〔摘要〕。亞洲水務 22 檔只有 5 個有框〔實測〕。
- 這次：G3 是框。UNIQLO 證明方框加字可以成立；G3 輸在框裡的東西跟同業重疊、字沒有修。

**A7　最細的線和縫不低於標誌寬的 1/14；做不到就另畫小尺寸版。**
- 根據：simple-icons 2217 個方形標誌，「細於寬度 1/14 的筆畫占比」與「縮到 16px 保留程度」的等級相關是 −0.83〔實測，10-17〕。Geismar：好標誌要清楚、簡單、縮小了還能用〔轉述，99% Invisible〕。
- 這次：三組字標在 24px 以下都糊，也沒有小尺寸版。

**A8　圓或尖，要對上想讓人感覺的屬性。**
- 根據：Jiang 等 2016（Journal of Consumer Research，五個實驗）：圓讓產品顯得舒適，尖角顯得耐用；旁邊文字講相反屬性時，效果消失〔摘要〕。
- 這次：三組都是方、直的線，跟「耐用、高標準」一致，沒有違反。

**A9　「有結構」適合實用型品牌，不對稱帶來活力，兩者要取捨。**
- 根據：Affonso、Janiszewski 2023（Journal of Marketing）：對稱、幾何、規律讓人覺得有結構，主打實用功能的品牌表現較好〔摘要〕。不對稱讓人覺得刺激、有活力（Luffarelli 等 2019；Bajaj、Bond 2018）〔摘要〕。
- 這次：崧淳要高標準，也要年輕有活力，兩邊會拉扯。G1 到 G3 都是完全規律的方塊，活力那一邊沒有處理〔推論〕。

**A10　簡單不等於好認。**
- 根據：Henderson、Cote 1998（195 個標誌）與 van der Lans 等 2009（十國，含中國、新加坡）：越「自然」越容易被正確認出；太和諧、太繁複都容易讓人誤以為看過〔摘要〕。
- 這次：直條加方塊是很常見的組合，容易被誤以為看過〔推論，未測〕。

**A11　不加立體、漸層、飛線、斜體效果。**
- 根據：Brand New 公用事業改版 13 組，5 組拿掉飛線、斜體、照片或細線效果，是唯一一致的方向〔實測，目視〕。外川、恩藏 2026（Journal of Marketing Research）：立體效果只對看得見的實體產品加分，抽象服務幾乎沒用〔摘要〕。
- 這次：三組都是平面，沒有違反。

**A12　負空間要被看出來、讀得懂，才有用。**
- 根據：Li 等 2026（Journal of Marketing Research）：圖地反轉標誌（如 FedEx 的箭頭）提升好感，前提是藏著的圖被看出、意思讀得懂〔摘要〕。縫隙在小尺寸消失時，好處也跟著沒了〔推論〕。
- 這次：三組沒有用到負空間。

### B　字標

**B1　中文字標是被記住的主要途徑，要當主角做。**
- 根據：中文品牌名主要靠「字的樣子」被記住，英文品牌名主要靠「聲音」（Pan、Schmitt 1996；Schmitt、Pan、Tavassoli 1994）〔摘要〕。
- 這次：字標是三組裡做得最粗的部分。

**B2　逐字調大小、重心、中宮、粗細。**
- 根據：許瀚文改台灣啤酒標準字：「灣」的鉤下沉、「台」「啤」的口提高，每個字以單位微調；筆畫少的字略粗、多的略細，「依視覺判斷」〔轉述，書摘〕。justfont：先做「上」「下」「國」三個基準字定大小〔全文〕。森澤字體辭典：重心偏高顯得緊張、有品格，偏低顯得安定、親切，同一組字要一致〔全文〕。
- 這次：沒做。

**B3　用眼睛修：橫筆比直筆細，反白版修細，圓要超出。**
- 根據：de Rozario（MyFonts）：一樣粗的橫筆看起來比直筆粗，要修細；一樣大的圓看起來比方形小，要讓圓超出去〔全文〕。Paget（Logo Geek）：白標誌放深底看起來比較粗，反白版要修細；格線只當參考，用眼睛修〔全文〕。思源黑體 Bold 的「崧淳」：直筆 68 到 76、橫筆 58 到 64（字級 600px），橫筆約為直筆的 0.80 到 0.87〔實測，11-03〕。
- 這次：G1 到 G3 橫直一律同粗，比值 1.00；反白版用同一筆寬。

**B4　縮小用的字要另外做。**
- 根據：許瀚文：小尺寸要縮小粗細對比、調整字裡的留白〔轉述〕。陳敦化主張縮到 0.4 公分還要看得清楚（justfont 2024）〔全文〕。
- 這次：沒有小尺寸版。

**B5　英文另外選，不用中文字型內建的英文。**
- 根據：justfont：標楷體的英文是等寬的，新細明體的英文被壓窄。中英搭配用和諧法（黑體配無襯線）或襯托法（中文個性強時英文縮小、低調）〔全文〕。
- 這次：英文還沒做。

**B6　楷體還是黑體，還沒有結論。**
- 根據：台灣受測者認為楷體最能代表台灣（黃耀明 2023）〔摘要〕；台灣多數公文用楷體，黑體常用於標題與招牌（W3C clreq）〔全文〕；亞洲水務與企業標誌 22 檔沒有一個用楷體〔實測〕。崧淳車身現在是黑色粗楷全名。
- 這次：三組都用黑體骨架。楷黑縮小比較 10-19 沒跑完，第二版提示詞的楷、黑並排也還沒生圖。

**B7　字形原創，而且字要寫對。**
- 根據：梁特助 10-11：「我要的是原創字型」。教育部楷書、宋體是 CC BY-ND，不能改作；Make Me a Hanzi 的筆畫取自文鼎字型，屬衍生，都不能拿來描（10-11 字形引擎紀錄）。AI 生圖常把崧寫成松（專案紀錄）。
- 這次：Claude 自畫的筆畫是原創；AutoIP 的 G3 把崧拆成山加松，字錯。

### C　系統與應用

**C1　畫標誌不等於做識別。**
- 根據：Bierut（Pentagram）：「designing a logo is not designing an identity」〔轉述〕。Vignelli：「A real Corporate Identity is based on an overall system approach, not just a logo.」〔全文〕
- 這次：還在標誌階段，名片、制服、整台車的規則是下一步，不算這次的錯。

**C2　新品牌的圖形要跟名字一起出現。**
- 根據：圖形加名字比只有其中一樣被評得好看（Bresciani、Del Ponte 2017）〔摘要〕；圖形比名字好記的優勢，只出現在已經認得名字的人身上（Roberts 等 2023）〔搜尋摘要〕。
- 這次：三組都有名字，沒有違反。

**C3　車身規則寫成數字：位置、兩層字高、淺底深字。**
- 根據：NASA 1975 手冊 p.7.6：淺色車用黑、深色車用白，字高按車型規定（小車 5 吋、廂型車 8 吋、聯結車 24 吋）〔全文，手冊頁照片〕。16 張公務車照片：門上小字放身分，約車高 1/40 到 1/60；車身大字約 1/7 到 1/28〔實測，像素估〕。美國招牌協會 USSC：1 公分字高理想約可在 3.6 公尺外讀，開車時至少打 65 折〔全文〕。
- 這次：車身用黑色（對車身黃 7.33）方向對；字高與位置還沒定。

**C4　顏色先決定它的工作，再放到實際底色、面積、距離上看。**
- 根據：Albers：同一個顏色放在不同背景上，看起來像不同的顏色〔轉述，書介〕。Caterpillar 的黃是為了讓道路工地被看見才選的〔全文〕。四色實算（WCAG 對比）：朱紅在白底 4.72、在深藍底 2.09；工程黃在白底 2.18、在深藍底 4.54；白在深藍底 9.87；工程黃在車身黃上只有 1.32〔實測，11-03〕。
- 這次：紅放白底、黃放深藍底、車身用黑，照實算放色，沒有違反。

**C5　量測只能當及格線，不能判斷好不好看。**
- 根據：同三把尺量 Logo Archive 38 個大師標誌：剪影擁擠度第 46 百分位、細碎度第 73、筆畫一致度第 53，都在中間〔實測，10-17〕。
- 這次：量測都做了，好不好看的判斷沒做。

### D　做法與提案

**D1　先研究、確認方向，再設計。**
- 根據：Wheeler《Designing Brand Identity》五階段：研究、釐清策略、設計、做成應用物、管理，每段做完才進下一段〔轉述，書摘〕。梁特助 10-11：「不是你直接開工做我指派的任務，你要先理解這個產業」。
- 這次：研究做了，但從研究直接跳到成品，中間少了挑方向。

**D2　先畫多個黑白草圖，挑定方向後再上色、再精修。**
- 根據：Geismar：好標誌單色也要能用〔轉述〕。Wheeler 的設計階段是先找一個大想法，再展開字、色、圖〔轉述，書摘〕。Airey《Logo Design Love》有「速寫本」「先黑白」的章節，只見於搜尋摘要，原書目錄沒核對到〔搜尋摘要〕。這條佐證不足，主要依據是這次被否的教訓。
- 這次：三組直接上四色交件，沒有黑白草圖階段。

**D3　把推理攤開，讓看的人自己得出同一個結論。**
- 根據：Rand 替 NeXT 只交一個方案，用一本小冊子一步一步說明理由（1986）〔轉述〕。
- 這次：推理寫在提示詞檔裡，但建立在「紅格代表高一個檔次」這種要說明才懂的意思上。

**D4　選標誌看管不管用，不看喜不喜歡。**
- 根據：Haviv：「choosing an effective logo is not about what one likes or dislikes: it's about what works.」〔轉述〕大通銀行八角形一開始被行內高層反對，幾個月後大家把它別在領帶上（Geismar）〔轉述〕。
- 這次：這條不能拿來替 G1 到 G3 辯護。它們被讀成字、要說明、字沒修，都屬於「不管用」。

**D5　不靠「AI 樣子」清單判斷，要問理由是不是只屬於這個品牌。**
- 根據：Anthropic frontend-design 把米色底 #F4F1EA 配襯線大字列為 AI 樣子；另一份 MIT 授權的 swiftui-design-skill 把暖白底配襯線標題當解方，兩份清單互相矛盾〔全文〕。
- 這次：交件是白底，沒有米色底；但「三根豎條加一個方塊」的理由，換成別家公司也說得通。

## 四、以後交 LOGO 前改三件事

1. 先交一頁黑白小圖，6 到 9 個方向，每個方向寫一句構成方法。你挑定方向後才上色、才精修。
2. 字標先逐字修：橫細直粗、重心、中宮，反白版另外修細。修過才拿去跟別的方案比。
3. 交件附第二節那張對照表，每條寫「過」或「沒過」。有「沒過」的不交。

## 五、還沒學到或沒做完的

- 楷體與黑體的縮小比較沒跑完。
- 約 40 篇研究多數只讀到摘要；拿企業採購者或服務業做的標誌實驗幾乎找不到。
- 量測都是像素計算，沒有真人辨識測試。
- 《Identify》《Designing Brand Identity》《Logo Design Love》原書都沒讀到，讀的是訪談、書摘、目錄。

## 六、出處

- **Claude 過去的學習紀錄** 10-13 筆記：專案資料夾 資源查找/04_LOGO與CIS美感學習筆記.md。10-17 第一輪、10-19 第二輪：gpt-collab 交件/Claude/20261017_LOGO與CIS美感學習/、20261019_LOGO與CIS美感學習第二輪/（PR #32、#35）。G1 到 G3：PR #48 交件/Claude/20261103_LOGO生圖提示詞/。
- **A1** rampstack logo-design https://github.com/rampstackco/claude-skills ；Logo Archive https://www.logo-archive.org/
- **A2、C1** The Vignelli Canon https://www.rit.edu/vignellicenter/sites/rit.edu.vignellicenter/files/documents/The%20Vignelli%20Canon.pdf
- **A3** 中國銀行行徽 https://www.boc.cn/english/thisisboc/ab3/brd/202601/t20260104_25638404.html ；人民日報 2023-04-10 https://paper.people.com.cn/rmrb/html/2023-04/10/nw.D110000renmrb_20230410_3-05.htm ；IxDF 格式塔 https://ixdf.org/encyclopedia/gestalt_principles_of_form_perception.html ；Logo Geek 格式塔 https://logogeek.uk/logo-design/gestalt-theory/
- **A4** Haviv 訪談 https://www.logodesignlove.com/sagi-haviv-interview ；Romaniuk https://contagious.com/io/article/jenni-romaniuk-on-distinctive-assets ；費城水務 https://whyy.org/articles/philadelphia-water-department-resolves-identity-crisis-with-63000-logo
- **A5** Rand〈Logos, Flags, and Escutcheons〉https://paulrand.design/writing/articles/1991-logos-flags-and-escutcheons.html ；Luffarelli 等 2019 https://journals.sagepub.com/doi/abs/10.1177/0022243719845000
- **A6** Fajardo 等 2016 https://ideas.repec.org/a/oup/jconrs/v43y2016i4p549-566..html ；simple-icons 16.35.0（npm，CC0）
- **A7、D2** Geismar（99% Invisible）https://99percentinvisible.org/episode/making-mark-visual-identity-tom-geismar/ ；Logo Design Love 書目頁（目錄未核對）https://oreilly.com/library/view/logo-design-love/9780133812589
- **A8** Jiang 等 2016 https://ira.lib.polyu.edu.hk/handle/10397/64985
- **A9** Affonso、Janiszewski 2023 https://journals.sagepub.com/doi/abs/10.1177/00222429221142281 ；Luffarelli 等 2019 https://journals.sagepub.com/doi/10.1177/0022243718820548 ；Bajaj、Bond 2018 https://www.scheller.gatech.edu/directory/research/marketing/bond/pdf/bajaj_bond_jcp_2018.pdf
- **A10** Henderson、Cote 1998 https://journals.sagepub.com/doi/abs/10.1177/002224299806200202 ；van der Lans 等 2009 https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1265991
- **A11** Brand New https://www.underconsideration.com/brandnew/ ；外川、恩藏 2026 https://doi.org/10.1177/00222437261460880
- **A12** Li 等 2026 https://journals.sagepub.com/doi/10.1177/00222437261417659
- **B1** Schmitt、Pan、Tavassoli 1994 https://ideas.repec.org/a/oup/jconrs/v21y1994i3p419-31.html
- **B2、B4** 許瀚文改台啤字 https://www.thenewslens.com/article/51205 ；justfont https://blog.justfont.com/2012/12/hanzi-type-design-1/ 、https://blog.justfont.com/2024/12/designbychentunhua/ ；森澤字體辭典 https://www.morisawa.co.jp/culture/dictionary/
- **B3** de Rozario（MyFonts）https://cms.myfonts.com/content/optical-illusions-and-eye-trickery-in-geometric-font-design ；Paget（Logo Geek）https://logogeek.uk/?p=2617 ；思源黑體 Noto Sans TC（OFL）
- **B5** justfont 中英搭配 https://blog.justfont.com/2020/02/how-to-match/
- **B6** 黃耀明 2023 https://iwate-u.repo.nii.ac.jp/record/2000123 ；W3C clreq https://github.com/w3c/clreq
- **C2** Bresciani、Del Ponte 2017 https://ideas.repec.org/a/pal/jobman/v24y2017i5d10.1057_s41262-017-0046-4.html ；Roberts 等 2023 https://uwaterloo.ca/memory-attention-cognition-lab/sites/default/files/uploads/documents/jarmac-2023-roberts.pdf
- **C3** NASA Graphics Standards Manual https://standardsmanual.com/products/nasa-graphics-standards-manual ；USSC 招牌字高與 Legibility Index（2006，梁特助電腦 美感學習素材_20261018）
- **C4** Albers https://www.themarginalian.org/2013/08/16/interaction-of-color-josef-albers-50th-anniversary/ ；Caterpillar https://rent.cat.com/en_US/articles/why-equipment-yellow
- **D1** Wheeler https://www.logodesignlove.com/brand-identity-process
- **D3** Rand 與 NeXT https://www.logodesignlove.com/next-logo-paul-rand
- **D5** anthropics/skills https://github.com/anthropics/skills ；swiftui-design-skill https://github.com/wholiver/swiftui-design-skill
- **Bierut** https://itsnicethat.com/features/michael-bierut-logo-design
