## Why

使用者不想手動整理知識條目的分類與摘要。本階段在同步腳本中加入兩個 Claude API 功能：自動分類（回填 Category）與自動摘要（讀取 Notion 頁面 block 內容並生成摘要回填 Content），讓輸入流程完全零摩擦——只需點一下 Web Clipper，其餘全自動。

## What Changes

- 同步腳本新增自動分類模組：偵測 Category 為空的條目，呼叫 Claude API 推測分類，透過 Notion API 寫回
- 同步腳本新增自動摘要模組：偵測 Content 屬性為空但頁面有 block 內容的條目，呼叫 Claude API 對 block 全文生成摘要，透過 Notion API 寫回 Content 欄位

## Capabilities

### New Capabilities

- `knowledge-categorization`: 同步時自動偵測未填 Category 的條目，呼叫 Claude API 推測分類並寫回 Notion
- `knowledge-summarization`: 同步時自動偵測 Content 屬性為空但頁面 blocks 有內容的條目，呼叫 Claude API 生成摘要並寫回 Notion Content 欄位

### Modified Capabilities

（無）

## Impact

- 修改程式元件：`sync.py` 新增自動分類與自動摘要模組
- 新增相依：Anthropic API（免費額度內）、`anthropic` Python 套件
- 相依 Phase 2 已完成的同步腳本框架（含 `get_page_blocks()` 函式）
