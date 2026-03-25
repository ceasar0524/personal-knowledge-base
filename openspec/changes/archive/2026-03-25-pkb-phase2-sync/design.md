## Context

Phase 1 已建立 Notion 資料庫與 NotebookLM Notebook。本階段聚焦於自動化同步：以 Python 腳本串接 Notion API 和 Google Drive API，讓 NotebookLM 透過 Drive 連結自動取得最新內容。

## Goals / Non-Goals

**Goals:**

- 建立全自動同步腳本，完成後無需手動操作即可保持 NotebookLM 資料最新
- 支援 cron job 排程執行

**Non-Goals:**

- 不包含 AI 自動分類（留待 Phase 3）
- 不需即時（real-time）同步，週期性同步即可
- 不處理影片逐字稿等複雜媒體格式

## Decisions

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

## Risks / Trade-offs

- **同步延遲**：排程執行有週期間隔，NotebookLM 的資料不是即時的。→ 緩解：依需求調整 cron 頻率（例如每小時）
- **NotebookLM 服務可用性**：依賴 Google 的外部服務，若服務中斷或政策改變，問答功能受影響。→ 緩解：Notion 本身仍可作為備份與原始查詢介面
