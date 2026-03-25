## Context

Phase 2 已建立完整的同步管線。本階段在 `sync.py` 中加入兩個 Claude API 模組：自動分類（回填 Category）與自動摘要（讀取 Notion 頁面 block 內容生成摘要回填 Content）。Web Clipper 擷取網頁時全文已存為頁面 blocks，`get_page_blocks()` 可直接讀取，無需另行抓取網頁。使用者只需點 Web Clipper，其餘全自動完成。

## Goals / Non-Goals

**Goals:**

- 使用者新增知識條目後無需手動選擇分類
- 使用者只需用 Web Clipper 存網頁，摘要自動從頁面 block 內容生成並填入 Content
- 自動化失敗時不影響同步主流程

**Non-Goals:**

- 不自動建立新的分類選項，只從預定義清單中選擇
- 不覆蓋使用者已手動設定的分類或內容
- 不另行抓取網頁（全文已存於 Notion 頁面 blocks）

## Decisions

### 自動分類：Claude API 回填 Category

**決定**：sync script 在讀取 Notion 條目時，對 Category 為空的條目呼叫 Claude API 推測分類，並透過 Notion API 寫回。

**理由**：
- 使用者不想手動選分類，降低輸入摩擦力是核心目標
- Claude API 可根據標題與內容準確推測分類，且呼叫成本低（每筆條目約一次短 prompt）
- 只對空白條目觸發，不覆蓋使用者已手動設定的分類

**失敗處理**：API key 缺失或單筆失敗時只記 log、跳過，不中止整個 sync，確保主管線穩定。

**替代方案考慮**：本機分類模型（成本低但精度差）；要求使用者手動分類（摩擦力高，不符需求）。

### 模型彈性設計：可設定 AI 模型

**決定**：使用 `AI_MODEL` 環境變數指定呼叫的模型，預設值為 `claude-haiku-4-5-20251001`（成本低、速度快，適合批次處理）。自動摘要與自動分類共用同一個模型設定。

**理由**：
- 日後可透過修改 `.env` 切換模型（如 claude-sonnet-4-6、GPT-4o 等），不需改動程式碼
- 預設使用 Haiku 降低 API 費用，個人知識庫不需最強模型
- 摘要與分類使用同一變數，設定簡單

**替代方案考慮**：摘要和分類各用不同環境變數（過度設計，目前無差異化需求）。

### 自動摘要：讀取 Notion Block 內容 + Claude API 生成摘要

**決定**：sync script 偵測 Content 屬性為空但頁面有 block 內容的條目，直接使用已有的 `get_page_blocks()` 函式讀取全文，再呼叫 Claude API 生成 3–5 bullet 的繁體中文摘要，透過 Notion API 寫回 Content 欄位。

**理由**：
- Web Clipper 擷取網頁時，全文已存為 Notion 頁面的 block 內容（開啟頁面右側 peek 可見標題與全文）
- `get_page_blocks()` 在 Phase 2 已實作完成，可直接重用，不需額外相依
- 無需處理網頁存取失敗、付費牆等問題，降低複雜度
- Claude API 生成繁體中文摘要，符合使用者語言習慣
- 只對 Content 屬性為空的條目觸發，不覆蓋使用者自己寫的內容

**失敗處理**：block 內容為空或 Claude API 失敗時，只記 log 並跳過，不中止 sync。

**替代方案考慮**：從 Source URL 抓取網頁（已確認不需要，全文已存於 blocks）；要求使用者手動填摘要（摩擦力高，不符需求）。

## Risks / Trade-offs

- **分類準確度**：Claude 可能對模糊的條目推測錯誤。→ 緩解：使用者可隨時在 Notion 手動修正，腳本不會再覆蓋已有分類的條目
- **Block 內容為空**：若使用者只存了標題未有頁面內容，無法生成摘要。→ 緩解：留空 Content，使用者自行補充
- **API 費用**：每次 sync 對新條目各呼叫一次 Claude API。→ 緩解：個人使用量極低，免費額度足夠
