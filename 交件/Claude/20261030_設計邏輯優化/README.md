# 設計邏輯優化（2026-10-30）

梁特助 10-30 11:56 原話：「開始全域查找上下文與專案內所有對話，全域優化設計邏輯，並到https://www.pinterest.com/與https://prompts.chat/中尋找適合的資源，優化自身」。

## 結論

配色做了 20 多輪都沒過。問題不在色彩知識不夠，在流程上有三個漏洞。以後照下面的六步走，每一步都有檢查點。

## 三個漏洞（從對話紀錄查到的）

1. **要求散在各處，交件時漏掉。**
   - 10-21 13:51 他問「你忘記我的要求了?」。
   - 10-24 08:02 他又說「我要的工程黃呢?要得紅色系呢?」。兩次都是交件前沒有逐條對要求。
   - Claude 和 GPT 各記一套，工程黃記成兩個顏色（見需求表第六節）。
   - 改法：用 `需求表.md` 當唯一出處，篩選條件直接寫進程式。
2. **問抽象的問題，得到「都不是」。**
   - 第九批四題全部「都不是」（Q35–Q38）。Q39 他說原因是「題目問錯方向」。
   - 他點選真實配色時，答案就清楚得多：8 組全是深藍，「都不像」從 13/28 降到 7/20。
   - 改法：方向問題先問大的，細節改成拿真實配色讓他兩兩比。
3. **從算式生色，不是從真實作品來。**
   - 10-24 07:42 他說「裡面太多湊數的了」。
   - 改法：候選取自網路真實配色。缺的角色才補，補的要標出來；黃和紅兩格都要補的整組不收。

## 六步流程

| 步驟 | 做什麼 | 檢查點 |
|---|---|---|
| 1 需求 | 新要求先寫進 `需求表.md`，跟舊要求衝突就列進衝突表 | 衝突沒解決之前，不用那一條出色 |
| 2 硬條件 | 把需求表寫成篩選程式：四格角色、色相、明度、同行色差 | 程式輸出每組都過；組數照實報 |
| 3 候選 | 從真實配色取候選，缺格才補，補的標「補」 | 每組附來源網址 |
| 4 他點選 | 本機挑色頁，4 選 1 再兩兩比，每點一次存檔 | 「都不像」比例要往下降，沒降就回步驟 1 問方向 |
| 5 規格 | 留下的組整理成三層：色值、角色、用在哪（名片、報價單、報告） | 對比用 colour-tool 算；紙本先看 |
| 6 理念 | 先寫推理（他哪些回答導出這組），再寫理念；理念講工作內容和崧、淳字義 | 每句對得到需求表的一條；附「我替你做的判斷」 |

logo 照 10-11 的順序，等顏色定了才開始。

## prompts.chat 學到的（2026-10-30 讀 `f/awesome-chatgpt-prompts` 的 prompts.csv，共 2,772 則）

prompts.chat 的網站雲端連不上。這份資料取自它在 GitHub 的原始資料檔，跟網站同一份來源。篩出 9 則跟品牌、logo、設計系統、配色有關的，已讀原文，以下 4 點會改變做法：

1. **先列推理，再給結論。**（Conversational Logo Design Process）
   - 這則先用是非題問到夠清楚，再寫 `reasoning_steps`，也就是每個回答推出什麼，最後才寫 logo 概念。
   - 我們的理念常常空洞，就是少了這一段。對應第 6 步。
2. **不一致要標出來，不要自己挑一個。**（Website Design System Builder）
   - 原文：「Flag any inconsistencies across pages … instead of picking one and ignoring the rest」。
   - 對應需求表第六節的衝突表。工程黃兩邊不一致，就是這種情況。
3. **規格分三層，並附決策紀錄。**（Token Architecture）
   - 三層是原始色值、語意角色、元件用法。每個取捨都記理由，原文說「transparency matters more than confidence」。
   - 對應第 5 步，以及梁特助要的「我替你做的判斷」。
4. **生圖交辦的限制寫法。**（logo designer）
   - 平面、不用 3D 和陰影、小尺寸要看得清、白底、不要應用圖。
   - 已併進 `cis-visual-direction` 的交辦單。不過 logo 本身仍然不交給生圖模型。

其餘幾則（Creative Branding Strategist、Design Brief、Create STYLE_GUIDE.md、Color Consistency Analysis、KERNPUNT）不是內容太泛，就是跟我們已有的做法重複，不採用。

## prompts.chat 第二輪（10-30 12:26 梁特助「prompts.chat全域查找適合你的資源」）

這次把 2,772 則全部按工作分九類重篩：文案、審稿、查證、中文、簡報、字體、需求訪談、去 AI 味、工業生圖。每類讀最相關的原文，採用下面 6 點，已寫進新 skill `.claude/skills/cis-delivery-check/`：

| 採用什麼 | 出處 | 用在哪 |
|---|---|---|
| 交件前先替他寫兩個否決理由，成立就先改 | devil adv、Critical Thinking (DeepThink) | 每次交件 |
| 先找出 AI 味的句子，再改寫，並列出改了什麼 | Humanize AI Text | 理念、slogan |
| 他做過的事比他說的話重；題目有引導性，答案要打折；原話照抄 | Customer Interview Insight Extractor | 問答紀錄、需求表 |
| 查證只能往保守調；有兩種讀法就判「不確定」 | Fact-Checking Evaluation Assistant | 回評 GPT 交件、同行資料 |
| 小記號、細線要 3:1（WCAG 1.4.11） | Accessibility Color Contrast Auditor | 黃、紅怎麼用 |
| slogan 先問禁用字，再寫推理，每個位置給主句、備選、副標 | Banner Slogan and Subtext Generator | slogan 下一輪 |

照第 5 點算出一條新的用法規則：
- 工程黃放在白紙上只有 2.0（#F7A600）和 1.7（#F2C230），當細線或小字不夠清楚。黃要放在深色底上，或者做成大面積色塊。
- 朱紅 #E54728 在白底上有 4.0，夠清楚；放在深藍 #2D4263 上只有 2.5。所以紅色小記號放白底。

沒採用的：
- 中文類都是翻譯或小說。
- 簡報類只是通用原則，像金字塔原理，我們已經用「先結論」。
- 工業生圖類沒有下水道或工程的題材。
- Idea Clarifier、Spec Interview 跟我們已有的問答做法重複。

## Pinterest

- 沒有抓。Pinterest 的 robots.txt 對所有爬蟲寫「Disallow: /」，服務條款也禁止未經許可用自動方式取資料，不登入也一樣。雲端和梁特助電腦都不自動抓。
- 10-16 那輪也沒看到任何圖。當時的檢討是「蒐集不等於學習」。
- 可行的做法：梁特助自己在 Pinterest 存他喜歡的圖，放進一個資料夾。Claude 在他電腦上打開來看、取色，寫看圖筆記。

## 同時改的

- `需求表.md`：新建。
- `.claude/skills/cis-visual-direction/SKILL.md`：交辦單的工程黃改成 CIS 黃 #F7A600，車身黃 #D68702 分開寫；加上生圖限制寫法。
- `.claude/skills/songchun-colour-study/SKILL.md`：加上交件前要對需求表；寫明 Pinterest 不能自動抓，prompts.chat 從 GitHub 原始檔讀。
