## Why

Phase 1 完成後同步仍需手動匯出，容易忘記導致 NotebookLM 資料過時。本階段建立全自動同步管線，讓 Notion 新增的知識無需人工介入即可自動出現在 NotebookLM 中。

## What Changes

- 建立 Python 同步腳本（`sync.py`），串接 Notion API + Google Drive API
- 腳本自動讀取 Notion 資料庫、轉換為 Markdown、寫入 Google Drive 指定檔案
- NotebookLM 以 Google Drive 檔案作為來源，Drive 更新後自動同步
- 設定 cron job 定期自動執行，整個流程無需人工介入

## Capabilities

### New Capabilities

- `knowledge-sync`: 全自動同步管線——腳本從 Notion API 讀取資料，寫入 Google Drive 指定檔案，NotebookLM 自動從 Drive 取得最新內容

### Modified Capabilities

（無）

## Impact

- 新增程式元件：`sync.py`（Python），串接 Notion API + Google Drive API
- 受影響系統：Notion 工作區、Google Drive、NotebookLM、本機（或排程服務）執行同步腳本
- 相依 Phase 1 已完成的 Notion 資料庫與 NotebookLM Notebook
