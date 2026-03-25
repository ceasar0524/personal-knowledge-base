## 1. 設定 Claude API

- [x] 1.1 取得 Anthropic API Key，設定 `ANTHROPIC_API_KEY` 環境變數，安裝 `anthropic` Python 套件，滿足「Claude API authentication」規格
- [x] 1.2 在 `.env` 新增 `AI_MODEL` 環境變數（預設 `claude-haiku-4-5-20251001`），sync.py 讀取此變數作為呼叫模型，滿足「Configurable AI model」規格

## 2. 實作自動摘要模組（依「自動摘要：讀取 Notion Block 內容 + Claude API 生成摘要」決策）

- [x] 2.1 實作「Auto-summarization of entries with block content but no Content property」與「Summary generation via Claude API」：sync 時偵測 Content 屬性為空但頁面 blocks 有內容的條目，呼叫 Claude API 生成繁體中文摘要（3–5 bullet），透過 Notion API 寫回 Content 欄位
- [x] 2.2 實作「Summarization failure resilience」：block 內容為空或 Claude API 失敗時記 log 並繼續，不中止 sync

## 3. 實作自動分類模組（依「自動分類：Claude API 回填 Category」決策）

- [x] 3.1 在 `sync.py` 中加入自動分類模組框架
- [x] 3.2 實作「Auto-categorization of uncategorized entries」：sync 時偵測 Category 為空的條目，呼叫 Claude API 推測分類並寫回 Notion
- [x] 3.3 實作「Predefined category list」：prompt 中包含完整分類選項，確保回傳值符合 Notion Select 欄位的預設選項
- [x] 3.4 實作「Categorization failure resilience」：單筆 Claude API 失敗時記 log 並繼續，不中止整個 sync

## 4. 測試與驗證

- [x] 4.1 測試「Entry already has Content」：已有 Content 的條目執行 sync 後不被覆蓋
- [x] 4.2 測試「Entry blocks empty」：頁面 blocks 為空的條目，確認腳本記 log 並跳過，不中止 sync
- [x] 4.3 用 Web Clipper 存入 2–3 篇文章，執行 `sync.py`，確認 Claude 自動填入繁體中文摘要
- [x] 4.4 測試「Entry already has a Category」：手動設定分類的條目執行 sync 後不被覆蓋
- [x] 4.5 測試「Missing or invalid API key」：`ANTHROPIC_API_KEY` 缺少時僅記 warning，sync 主流程照常完成
- [x] 4.6 新增 2–3 筆無分類的測試條目，執行 `sync.py`，確認 Claude 自動填入正確的 Category
