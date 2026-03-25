## Why

使用者常常學到新知識後很快就忘記，需要一個結構化的輸入介面來收集知識。本階段建立 Notion 知識庫資料庫與 NotebookLM 問答環境，讓使用者能透過多種方式快速記錄知識，並在 NotebookLM 中進行查詢。

## What Changes

- 建立 Notion 知識庫資料庫結構（標題、分類、來源、內容、標籤、新增日期）
- 定義多種知識輸入方式：手動輸入、Notion Web Clipper 網頁擷取、手機拍照搭配 OCR
- 建立 NotebookLM Notebook 作為 AI 問答層

## Capabilities

### New Capabilities

- `knowledge-capture`: 在 Notion 中建立和維護結構化知識條目，支援手動輸入、網頁擷取、圖片 OCR 等多種輸入方式
- `knowledge-query`: 透過 NotebookLM 對個人知識庫進行關鍵字搜尋與自然語言 AI 問答

### Modified Capabilities

（無）

## Impact

- 工具：Notion（免費方案）、Google NotebookLM（免費）、Notion Web Clipper 擴充功能、Microsoft Lens（OCR）
- 無程式碼，全為工具設定
- 受影響系統：使用者的 Notion 工作區與 NotebookLM 帳號
