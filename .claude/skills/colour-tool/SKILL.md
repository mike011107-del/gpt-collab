---
name: colour-tool
description: 色彩計算與看圖工具。要算色碼的 WCAG 對比、APCA、CIELAB／OKLCH、CIEDE2000 色差、色弱模擬、USWDS 明度級、各色相最鮮豔的明度，從圖片取代表色，或把本機 HTML／SVG 算成 PNG 來實際看圖時使用。只處理不透明 sRGB 螢幕色。
---

# 色彩計算與看圖

## 什麼時候用

- 研讀時，要把原文的規則拿實際色碼驗算（例如「明度差 50 達 4.5:1」）。
- 要核對別人寫的對比、色差、色弱數字。
- 拿到圖檔或設計稿，要取色或要實際看到畫面。

不用的時候：只是轉述來源說法、不需要數字。工具存在不代表要用。

## 指令

```bash
T=.claude/skills/colour-tool/scripts      # 在專案庫根目錄執行
python3 -I $T/colourtool.py selftest                     # 先跑；退出碼 0 才算工具可用
python3 -I $T/colourtool.py info '#FACA30' '#14A5B3'     # 亮度、L*C*h、OKLCH、USWDS 級、對白／對黑
python3 -I $T/colourtool.py pair '#FACA30' '#14A5B3'     # 前景 背景：WCAG、APCA、ΔE2000、L*差、色弱三型
python3 -I $T/colourtool.py peak --step 10               # sRGB 色域內每個色相最鮮豔時的 L*
python3 -I $T/colourtool.py image 圖.png --k 8           # 圖片代表色與面積（需 Pillow）
NODE_PATH=$(npm root -g) node $T/render.cjs 稿.html 出.png 1200 1   # HTML／SVG → PNG，再用 Read 看圖
```

加 `--json` 輸出機器可讀結果。

## 用了什麼公式

| 項目 | 依據 |
|---|---|
| WCAG 對比 | WCAG 2.x：sRGB 解碼門檻 0.04045，係數 0.2126／0.7152／0.0722 |
| CIELAB | IEC 61966-2-1 矩陣，D65，白點取矩陣列和 |
| CIEDE2000 | Sharma, Wu, Dalal 2005；selftest 用該文 5 組測試資料，誤差 < 1e-4 |
| OKLCH | Ottosson 2020 |
| 色弱 | Machado 2009，severity 1.0，作用在線性 RGB |
| APCA | apca-w3 0.1.9 常數 |
| USWDS 級 | uswds-site `pages/design-tokens/color/overview.md` 的亮度表 |

裝了 coloraide 時，selftest 會用它交叉驗算：WCAG 差約 2e-4（coloraide 用完整矩陣），Lab 差 < 0.01，ΔE2000 差 < 0.005。

## 限制

- 只算不透明的 sRGB 螢幕色。不代表印刷、油漆、車膜或實物；透明色要先跟底色合成再算。
- 對比達標只說明色對，不保證字形、字級、縮放後讀得清楚。
- `image` 的代表色是量化近似值，受壓縮、光線、陰影影響，不能當品牌標準色。
- `render.cjs` 只開本機檔。頁面要載入外部字型或圖片時，在擋網路的環境會失敗，看輸出的「載入失敗」清單。
- `USWDS級` 標 `在該級範圍內: false` 時，表示亮度落在兩級之間，回傳的是最接近的一級。

## 失敗時

- selftest 退出碼 1：先看錯誤訊息；不要改容差去讓它通過，除非能說明差異來自定義（例如 WCAG 係數）。
- render 逾時或退出碼 3：回報失敗的網址；看不到圖就寫「未目視」，不要用推測代替。
