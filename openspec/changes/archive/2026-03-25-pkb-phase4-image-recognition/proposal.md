## Why

Notion 頁面中常含有圖片（截圖、掃描文件、圖表），但目前的同步腳本只處理文字 block，圖片內容完全被忽略；此外，Tags（標籤）和 Date Added（文章發布日期）欄位目前也未自動回填，需要使用者手動輸入，增加摩擦力。本階段同時解決這三個問題，讓知識庫 AI 補全真正完整。

## What Changes

- `sync.py` 的 `get_page_blocks()` 新增圖片 block 偵測：下載圖片 → 壓縮 → 傳給 Claude Vision API 辨識文字內容
- 辨識結果融入現有摘要與分類流程，與文字內容合併處理
- 新增自動標籤模組：Claude API 根據標題與內容推測 Tags，寫回 Notion Multi-select 欄位
- 新增自動日期擷取模組：Claude API 從文章內容中擷取發布日期，寫回 Notion Date 欄位
- 下載的圖片在辨識後即刪除（不落地儲存），壓縮僅在記憶體中進行

## Capabilities

### New Capabilities

- `knowledge-image-recognition`: 偵測 Notion 頁面中的圖片 block，下載並壓縮後透過 Claude Vision API 辨識圖片內容，將辨識結果加入摘要與分類的文字輸入
- `knowledge-tagging`: sync 時自動偵測 Tags 為空的條目，呼叫 Claude API 推測標籤並寫回 Notion Multi-select 欄位
- `knowledge-date-extraction`: sync 時自動偵測 Date Added 為空的條目，呼叫 Claude API 從文章內容擷取發布日期並寫回 Notion Date 欄位

### Modified Capabilities

- `knowledge-summarization`: 摘要輸入來源新增圖片辨識文字（原有邏輯不變）
- `knowledge-categorization`: 分類輸入來源新增圖片辨識文字（原有邏輯不變）

## Impact

- 修改程式元件：`sync.py`（`get_page_blocks()`、`auto_summarize_entry()`、`auto_categorize_entry()`，新增 `auto_tag_entry()`、`auto_extract_date_entry()`）
- 新增相依：`Pillow`（圖片壓縮）
- 依賴 Phase 3 已完成的自動摘要與自動分類框架
