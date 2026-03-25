## Why

使用者常常學到新知識後很快就忘記，缺乏一個可以長期累積、隨時查詢的個人知識庫。本方案建立一套以 Notion 為輸入介面、Google NotebookLM 為 AI 問答引擎的知識管理系統，讓使用者能用自然語言問出自己曾學過的任何知識。

## What Changes

- 建立 Notion 知識庫資料庫結構（標題、分類、來源、內容、標籤、新增日期）
- 定義多種知識輸入方式：手動輸入、Notion Web Clipper 網頁擷取、手機拍照搭配 OCR
- 建立全自動同步腳本：Notion API 讀取 → 生成 Markdown → Google Drive API 寫入指定檔案 → NotebookLM 自動從 Drive 更新來源
- 在 NotebookLM 建立 Notebook 作為 AI 問答層，支援關鍵字搜尋與自然語言問答
- 同步腳本執行時自動偵測未分類條目，呼叫 Claude API 推測分類並回填至 Notion，使用者無需手動選擇 Category

## Capabilities

### New Capabilities

- `knowledge-capture`: 在 Notion 中建立和維護結構化知識條目，支援手動輸入、網頁擷取、圖片 OCR 等多種輸入方式
- `knowledge-sync`: 全自動同步管線——腳本從 Notion API 讀取資料，寫入 Google Drive 指定檔案，NotebookLM 自動從 Drive 取得最新內容
- `knowledge-query`: 透過 NotebookLM 對個人知識庫進行關鍵字搜尋與自然語言 AI 問答
- `knowledge-categorization`: 同步時自動偵測未填 Category 的條目，呼叫 Claude API 推測分類並寫回 Notion

### Modified Capabilities

（無）

## Impact

- 工具：Notion（免費方案）、Google NotebookLM（免費）、Notion Web Clipper 擴充功能、Microsoft Lens（OCR）
- 新增程式元件：同步腳本（Python），串接 Notion API + Google Drive API + Claude API（自動分類）
- 受影響系統：Notion 工作區、Google Drive、NotebookLM、本機（或排程服務）執行同步腳本
