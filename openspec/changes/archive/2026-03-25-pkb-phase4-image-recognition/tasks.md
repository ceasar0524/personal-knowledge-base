## 1. 安裝相依套件

- [x] 1.1 安裝 `Pillow` Python 套件，用於圖片壓縮

## 2. 實作圖片辨識模組（依「圖片辨識：使用 Claude Vision API」與「圖片壓縮：Pillow 記憶體壓縮」決策）

- [x] 2.1 實作「Image block detection in Notion pages」：在 `get_page_blocks()` 中偵測 image block，提取圖片 URL
- [x] 2.2 實作「Image download and compression」：下載圖片、使用 Pillow 縮放至最大 1024px、JPEG 品質 70，在記憶體中完成
- [x] 2.3 實作「Image recognition via Claude Vision API」：將壓縮後圖片以 base64 傳給 Claude Vision API，取得文字描述，附加至 block 內容（格式：`[圖片內容：...]`）
- [x] 2.4 實作「Image recognition failure resilience」：下載失敗或 Claude Vision API 失敗時記 log 並繼續，不中止 sync

## 3. 整合至摘要與分類流程（依「辨識結果融入現有流程」決策）

- [x] 3.1 確認「Auto-summarization of entries with block content but no Content property」：`auto_summarize_entry()` 自動獲得含圖片辨識結果的完整 block 內容，無需額外修改
- [x] 3.2 確認「Auto-categorization of uncategorized entries」：`auto_categorize_entry()` 自動獲得含圖片辨識結果的內容，無需額外修改

## 4. 實作自動標籤模組（依「Tags 自動回填」需求）

- [x] 4.1 實作「Auto-tagging of untagged entries」：sync 時偵測 Tags 為空的條目，呼叫 Claude API 推測 1–3 個標籤，寫回 Notion Multi-select 欄位
- [x] 4.2 實作「Predefined tag list for auto-tagging」：prompt 中包含預定義標籤清單，確保回傳值符合 Notion Multi-select 現有選項
- [x] 4.3 實作「Auto-tagging failure resilience」：Claude API 失敗時記 log 並繼續，不中止 sync

## 5. 實作自動日期擷取模組（依「Date Added 自動回填文章發布日期」需求）

- [x] 5.1 實作「Auto date extraction for entries without a date」：sync 時偵測 Date Added 為空的條目，呼叫 Claude API 從內容擷取文章發布日期（ISO 8601），寫回 Notion Date 欄位
- [x] 5.2 實作「Date extraction failure resilience」：無法擷取日期或 Claude API 失敗時記 log 並繼續，不中止 sync

## 6. 測試與驗證

- [x] 6.1 在 Notion 頁面加入一張含文字的截圖，執行 `sync.py`，確認 `[圖片內容：...]` 出現在 block 回傳結果中
- [x] 6.2 測試圖片下載失敗情境：填入無效圖片 URL，確認腳本記 log 並跳過，不中止 sync
- [x] 6.3 確認壓縮後圖片不落地儲存（本機目錄無新增圖片檔案）
- [x] 6.4 執行完整 `sync.py`，確認含圖片頁面的摘要和分類結果已包含圖片中的文字資訊
- [x] 6.5 新增 2–3 筆無標籤條目，執行 `sync.py`，確認 Claude 自動填入適當標籤
- [x] 6.6 測試「Entry already has Tags」：已有標籤的條目執行 sync 後不被覆蓋
- [x] 6.7 用 Web Clipper 存入含發布日期的文章，執行 `sync.py`，確認 Date Added 欄位自動填入正確日期
- [x] 6.8 測試「Entry already has Date Added」：已有日期的條目執行 sync 後不被覆蓋
