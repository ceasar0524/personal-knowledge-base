## Context

使用者目前沒有系統化的知識管理方式，學到的東西容易遺忘。本設計採用「方案二」：以 Notion 作為輸入與整理層，Google NotebookLM 作為 AI 問答層，兩者透過全自動腳本同步（Notion API → Google Drive → NotebookLM）。

使用者技術背景：原本偏好現成工具，但確認可以寫程式後，同步層改為全自動管線：Notion API → Python 腳本 → Google Drive API → NotebookLM。現有工具：Notion（已在使用）。

## Goals / Non-Goals

**Goals:**

- 建立結構化的 Notion 知識庫資料庫，支援多種輸入方式
- 建立全自動同步腳本，完成後無需手動操作即可保持 NotebookLM 資料最新
- 讓使用者能以自然語言問出自己曾學過的知識，並看到來源出處
- 支援在手機上查詢知識庫

**Non-Goals:**

- 不需即時（real-time）同步，週期性同步即可
- 不處理影片逐字稿等複雜媒體格式
- 不追蹤知識複習進度（非 Anki/Spaced Repetition 系統）

## Decisions

### 選擇 NotebookLM 而非 Notion AI

**決定**：使用 Google NotebookLM 作為 AI 問答引擎，而非 Notion 內建的 Notion AI。

**理由**：
- Notion AI 需額外付費（每月約 $10 USD），NotebookLM 免費
- NotebookLM 回答時會標示出處段落，可信度更高
- NotebookLM 支援最多 50 份來源文件、每份 50 萬字，容量充足

**替代方案考慮**：Notion AI 整合更緊密，但成本是主要考量；Obsidian + 插件需要技術設定，不符合使用者需求。

### 同步策略：全自動管線（Notion API → Google Drive → NotebookLM）

**決定**：腳本透過 Notion API 讀取資料庫，轉換為 Markdown，再透過 Google Drive API 寫入指定檔案；NotebookLM 以該 Drive 檔案作為來源，自動取得最新內容。

**管線流程**：
```
cron job → sync.py → Notion API（讀） → Markdown → Google Drive API（寫） → NotebookLM（自動更新）
```

**理由**：
- Notion API 可完整讀取所有資料庫條目（支援 pagination）
- NotebookLM 支援 Google Drive 檔案作為來源，Drive 檔案更新後 NotebookLM 自動同步
- Google Drive API 免費，個人用量遠低於免費額度
- 整個流程設定一次後完全無需人工介入

**技術選型**：Python，使用 `notion-client` + `google-api-python-client`。
理由：生態系豐富、後續擴充（向量資料庫、RAG）較容易。

**替代方案考慮**：手動匯出 SOP 簡單但依賴人工紀律；Zapier 自動化需付費且彈性不足；直接上傳 NotebookLM 因無公開 API 無法自動化。

### 自動分類：Claude API 回填 Category

**決定**：sync script 在讀取 Notion 條目時，對 Category 為空的條目呼叫 Claude API 推測分類，並透過 Notion API 寫回。

**理由**：
- 使用者不想手動選分類，降低輸入摩擦力是核心目標
- Claude API 可根據標題與內容準確推測分類，且呼叫成本低（每筆條目約一次短 prompt）
- 只對空白條目觸發，不覆蓋使用者已手動設定的分類

**失敗處理**：API key 缺失或單筆失敗時只記 log、跳過，不中止整個 sync，確保主管線穩定。

**替代方案考慮**：本機分類模型（成本低但精度差）；要求使用者手動分類（摩擦力高，不符需求）。

### Notion 資料庫欄位設計

**決定**：使用六個欄位：標題（Title）、分類（Select）、來源（URL）、內容（Text）、標籤（Multi-select）、新增日期（Date）。

**理由**：最小化輸入門檻，降低記錄新知識的摩擦力。欄位過多會讓人不想記。

## Risks / Trade-offs

- **同步延遲**：排程執行有週期間隔，NotebookLM 的資料不是即時的。→ 緩解：依需求調整 cron 頻率（例如每小時）
- **NotebookLM 服務可用性**：依賴 Google 的外部服務，若服務中斷或政策改變，問答功能受影響。→ 緩解：Notion 本身仍可作為備份與原始查詢介面
- **圖片/截圖內容無法直接被 AI 索引**：上傳的 PDF 若含圖片，NotebookLM 無法讀取圖片中的文字。→ 緩解：使用 OCR 工具（Microsoft Lens）先將圖片轉為文字再貼入 Notion
