# AutoIP 文生圖 API 範例

寫了什麼：供崧淳 CI 視覺素材製作使用的 Python 範例，依序取得 OpenAPI、建立文生圖任務、輪詢至完成、下載第一張輸出圖。只新增 GPT 交件檔案。

根據什麼：梁特助本次指定的 API 流程、官方 `@autoip/mcp` 0.7.0 的實作及套件內 API 文件、本機 HTTP 模擬測試。

已查到：官方套件使用 `https://autoip.app/api/v1`、Bearer header、`multipart/form-data` 的 `prompt` 欄位、回應頂層的 `task_uuid` 與 `status`，以及 `/tasks/{task_uuid}/outputs/0`。

限制：本次帶 Authorization 的 `GET /openapi.yaml` 被雲端代理擋下，錯誤為 `Tunnel connection failed: 403 Forbidden`。未取得即時完整 OpenAPI、未確認實際金鑰權限或 API 回應、未送出真實生圖任務。因此不能把本機測試說成 AutoIP 實際串接成功。規格結構的基本文字檢查也不是 OpenAPI schema 驗證。

## 使用

需要 Python 3.10 以上，不需安裝第三方套件。先切換到本文件所在資料夾，或將以下程式路徑改成下載後的實際位置。

先只取得並另存完整規格，不建立計費任務：

```bash
python autoip_api_example.py --fetch-spec-only --spec-output autoip-openapi.yaml
```

程式優先讀取環境變數 `AUTOIP_API_KEY`。沒有設定時，會以隱藏輸入提示要求金鑰，不把金鑰印出或寫入程式。可直接在終端機的隱藏提示輸入，不必把金鑰放進命令歷史。

建立文生圖任務並下載：

```bash
python autoip_api_example.py --prompt "冷色系環保工程車概念，工程黃點綴，無文字" --output autoip-output.png
```

這一指令會在規格請求成功後送出文生圖 POST；依官方文件，提交任務會扣點。本次只交付與測試範例，沒有執行此真實生成指令。此 prompt 是呼叫方式示例，不代表崧淳配色或設計已定案。

程式會輸出 `task_uuid=...`。若等待逾時或下載失敗，保留該 ID，改用以下指令接續；不會再送建立任務的 POST：

```bash
python autoip_api_example.py --task-uuid 已取得的任務UUID --output autoip-output.png
```

可加 `--timeout 900 --interval 5`，指定最多輪詢等待時間及查詢間隔，單位都是秒。每次執行都先重新 GET `/openapi.yaml`；無法取得規格時會停止，不建立任務。

## 請求順序

1. `GET https://autoip.app/api/v1/openapi.yaml`，讀取完整規格；有指定 `--spec-output` 才另存原始內容。
2. `POST https://autoip.app/api/v1/images/text-to-image`，以 multipart 的 `prompt` 欄位建立任務。
3. `GET https://autoip.app/api/v1/tasks/{task_uuid}`，輪詢 `status`。
4. 狀態為 `completed` 後，`GET https://autoip.app/api/v1/tasks/{task_uuid}/outputs/0`，將回應的圖片 bytes 寫入 `--output`。

所有請求，包括規格與下載，都附 `Authorization: Bearer <AUTOIP_API_KEY>`。程式沿用系統代理與 TLS 驗證，不跟隨 HTTP 重新導向，避免將金鑰轉送到其他位址。不自動重試建立任務的 POST；若送出後失去回應，先到 AutoIP 任務列表確認是否已建立，避免重複扣點。

`failed`、`cancelled`、`timeout` 都會結束等待並回報失敗。規格及圖片檔都不覆寫既有檔案；部分圖片下載失敗時會清除不完整檔案。下載僅接受圖片或二進位 Content-Type，這不是圖片內容或設計品質驗證。

## 實際驗證與來源

| 佐證 | 核對範圍與實際結果 | 限制 |
| --- | --- | --- |
| 本次需求 | 端點、驗證標頭、multipart prompt、輪詢及第一張輸出的下載流程已納入 | 使用者指定需求不是服務實測結果 |
| [官方套件 @autoip/mcp 0.7.0](https://www.npmjs.com/package/@autoip/mcp/v/0.7.0) 的 `dist/index.js` 與 `skill/SKILL.md` | 核對 API base、建立回應的 task_uuid、輪詢 status、失敗狀態及帶同一 Bearer 的下載方式 | 兩份文件來自同一套件，合併視為一份來源；不當成兩份獨立證據，也不替代即時 OpenAPI |
| `test_autoip_api_example.py` 的本機 HTTP 實測 | 10 項通過：完整流程、每次請求的 Authorization、中文 multipart、規格錯誤阻止 POST、401 不重送且遮蔽金鑰、失敗任務不下載、以 UUID 接續、輪詢逾時、不跟隨重新導向、非圖片回應拒存、不完整下載清理、既有檔案保護；部分檢查合併在同一案例 | 模擬回應取自需求及套件介面，與上述來源存在依賴；只證明範例對這些情況的行為 |
| 本次即時規格請求 | 帶 Bearer 的 GET `/openapi.yaml` 遭代理 403 阻擋 | 只證明此執行環境當時無法連線，不能據此判定金鑰無效或 AutoIP 服務故障 |

重跑本機測試：

```bash
python -m unittest -v test_autoip_api_example
```

測試只使用本機模擬服務與明確標示的測試金鑰，不讀取真實金鑰、不連 AutoIP、不扣點。測試中的 OpenAPI 內容是模擬資料，沒有交付為 AutoIP 官方規格。
