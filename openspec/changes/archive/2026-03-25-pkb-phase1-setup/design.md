## Context

使用者目前沒有系統化的知識管理方式。本階段聚焦於輸入與查詢的基礎建設——建立 Notion 資料庫結構並設定 NotebookLM。同步自動化留待 Phase 2 處理。

## Goals / Non-Goals

**Goals:**

- 建立結構化的 Notion 知識庫資料庫，支援多種輸入方式
- 建立 NotebookLM Notebook 作為未來查詢層的基礎

**Non-Goals:**

- 不包含自動化同步（留待 Phase 2）
- 不包含 AI 自動分類（留待 Phase 3）
- 不追蹤知識複習進度

## Decisions

### 選擇 NotebookLM 而非 Notion AI

**決定**：使用 Google NotebookLM 作為 AI 問答引擎，而非 Notion 內建的 Notion AI。

**理由**：
- Notion AI 需額外付費（每月約 $10 USD），NotebookLM 免費
- NotebookLM 回答時會標示出處段落，可信度更高
- NotebookLM 支援最多 50 份來源文件、每份 50 萬字，容量充足

**替代方案考慮**：Notion AI 整合更緊密，但成本是主要考量。

### Notion 資料庫欄位設計

**決定**：使用六個欄位：標題（Title）、分類（Select）、來源（URL）、內容（Text）、標籤（Multi-select）、新增日期（Date）。

**理由**：最小化輸入門檻，降低記錄新知識的摩擦力。欄位過多會讓人不想記。

## Risks / Trade-offs

- **圖片/截圖內容無法直接被 AI 索引**：NotebookLM 無法讀取圖片中的文字。→ 緩解：使用 OCR 工具（Microsoft Lens）先將圖片轉為文字再貼入 Notion
- **Phase 1 查詢需手動上傳**：自動同步尚未建立，本階段需手動匯出並上傳至 NotebookLM 做初始測試
