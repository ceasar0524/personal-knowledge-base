## Context

Phase 3 已實作文字 block 的摘要與分類。但 Notion 頁面中的圖片 block（image type）目前在 `blocks_to_markdown()` 中落入 `[Unsupported block: image]` 佔位符，內容完全遺失。本階段在現有管線中插入圖片辨識步驟，讓圖片中的文字資訊也能參與摘要與分類。

## Goals / Non-Goals

**Goals:**

- 偵測 Notion 頁面的 image block，下載並壓縮圖片
- 使用 Claude Vision API 辨識圖片內容（文字、圖表說明等）
- 將辨識結果與文字 block 合併，用於摘要與分類
- 壓縮僅在記憶體進行，不落地儲存圖片檔案
- Tags 為空時自動回填標籤（Multi-select 欄位）
- Date Added 為空時自動從文章內容擷取發布日期（Date 欄位）

**Non-Goals:**

- 不儲存圖片到本機或 Google Drive
- 不處理圖片中的非文字內容（純視覺圖表無文字者略過）
- 不修改 Google Drive 匯出格式（Markdown 中仍保留圖片佔位符）
- 不新增 Notion Multi-select 未定義的標籤選項

## Decisions

### 圖片辨識：使用 Claude Vision API

**決定**：下載 Notion image block 的 URL，使用 `Pillow` 壓縮後以 base64 編碼傳給 Claude Vision API，取得圖片文字描述。

**理由**：
- 與現有 Claude API 呼叫一致，不需引入新服務（如 Google Vision）
- Claude Vision 可理解圖表、截圖等多種圖片類型
- base64 傳輸無需額外儲存步驟

**失敗處理**：下載失敗或辨識失敗時，記 log 並略過該圖片，不中止 sync。

**替代方案考慮**：Google Vision API（額外費用與設定）；pytesseract OCR（僅限純文字圖片，精度低）。

### 圖片壓縮：Pillow 記憶體壓縮

**決定**：使用 `Pillow` 將圖片縮放至最大 1024px（長邊），JPEG 品質 70，在記憶體中完成，不寫入磁碟。

**理由**：
- 1024px 已足夠 Claude Vision 辨識文字
- 壓縮可大幅降低 base64 大小，減少 API token 消耗
- 記憶體操作避免臨時檔案管理問題

### 辨識結果融入現有流程

**決定**：`get_page_blocks()` 回傳時在文字結尾附加圖片辨識結果（以 `[圖片內容：...]` 標記），`auto_summarize_entry()` 和 `auto_categorize_entry()` 自動獲得完整內容，無需修改邏輯。

**理由**：影響範圍最小，現有摘要與分類邏輯完全不變。

### Tags 自動回填：使用 Claude API，預定義清單為優先，允許新增

**決定**：偵測 `Multi-select`（Tags）欄位為空的條目，將標題與內容傳給 Claude API，要求優先從預定義清單中選 1–3 個標籤；若內容明顯屬於清單以外的主題，Claude 可建議新標籤（英文，簡短）。所有回傳的標籤均寫回 Notion Multi-select 欄位（Notion API 會自動建立新選項）。

**預定義標籤清單（prompt 中提供作為參考）**：
- Generative AI
- AWS AI
- Azure AI
- Prompt engineering
- AI Governance
- Digital Transformation
- Technical Writing
- Cloud Strategy

**Notion 欄位名稱**：`Multi-select`（multi_select 類型）

**理由**：
- 預定義清單確保常見主題一致性，降低標籤碎片化
- 允許新增使系統能隨知識庫內容演進，不被初始清單限制
- Notion Multi-select 本就支援動態新增選項，無需額外處理

**失敗處理**：Claude API 失敗時記 log 並略過，不中止 sync。已有 Tags 的條目完全不處理。

### 日期擷取：使用 Claude API 從文章內容推斷

**決定**：偵測 `Date`（Date Added）欄位為空的條目，將文章內容傳給 Claude API，要求回傳 ISO 8601 格式（YYYY-MM-DD）的發布日期，寫回 Notion Date 欄位。

**Notion 欄位名稱**：`Date`（date 類型）

**理由**：
- 文章本文（blocks 內容）通常包含發布日期資訊
- Claude 可從上下文推斷日期，比正規表達式解析更靈活

**失敗處理**：
- Claude API 無法找到日期時，留空並記 log，不中止 sync
- Claude API 失敗時記 log 並略過，不中止 sync
- 已有日期的條目完全不處理

## Risks / Trade-offs

- **Notion 圖片 URL 過期**：Notion 的 image block URL 有時效性，需在 sync 執行當下立即下載。→ 緩解：sync 執行時直接下載，不快取 URL
- **API token 增加**：圖片 base64 會增加每次呼叫的 token 數。→ 緩解：壓縮至 1024px + JPEG 70 控制大小
- **辨識不準確**：純視覺圖表（無文字）可能產生雜訊描述。→ 緩解：辨識結果標記為 `[圖片內容：...]`，使用者可辨識來源
