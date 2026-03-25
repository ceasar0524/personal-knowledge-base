## 1. 建立 Notion 知識庫（輸入層）

- [ ] 1.1 依照「Notion 資料庫欄位設計」決策，在 Notion 中建立知識庫 Database，新增 Title、Category（Select）、Source（URL）、Content（Text）、Tags（Multi-select）、Date Added（Date，設為自動填入）共六個欄位
- [ ] 1.2 設定 Category 欄位的預設選項：技術、商業、生活、語言等分類
- [ ] 1.3 驗證「Notion database structure」規格：建立一筆測試知識條目，確認所有欄位皆可正常輸入
- [ ] 1.4 安裝 Notion Web Clipper 瀏覽器擴充功能，並與 Notion 帳號連結，以支援「Web page capture」功能
- [ ] 1.5 在手機安裝 Notion App，測試「Manual text input」：用手機新增一筆知識條目，確認手機輸入流程順暢
- [ ] 1.6 在手機安裝 Microsoft Lens（或等效 OCR 工具），測試「Image and photo OCR input」：拍一張含文字的照片，將 OCR 結果貼入 Notion

## 2. 建立 NotebookLM 問答層（依「選擇 NotebookLM 而非 Notion AI」決策）

- [ ] 2.1 前往 notebooklm.google.com，用 Google 帳號登入，建立一個新的 Notebook，命名為「個人知識庫」

## 3. 建立全自動同步管線（依「同步策略：全自動管線（Notion API → Google Drive → NotebookLM）」決策）

- [ ] 3.1 在 Notion 建立 Integration，取得 `NOTION_TOKEN`，將 Integration 連結至知識庫 Database，記下 `NOTION_DATABASE_ID`，滿足「Notion API authentication」規格
- [ ] 3.2 在 Google Cloud Console 建立專案、啟用 Drive API、建立 Service Account 並下載憑證 JSON，設定 `GOOGLE_CREDENTIALS_PATH`，滿足「Google Drive API authentication」規格
- [ ] 3.3 在 Google Drive 建立一個空白文件（`knowledge-base.md`），記下 `GOOGLE_DRIVE_FILE_ID`；將 Service Account email 加入該檔案的編輯權限
- [ ] 3.4 初始化 Python 專案，安裝 `notion-client`、`google-api-python-client`，建立 `sync.py` 框架
- [ ] 3.5 實作「Automated sync script」：讀取 Notion 所有條目（含「Notion API pagination」分頁處理），轉換為 Markdown
- [ ] 3.6 實作「Markdown export format」：確保每筆條目包含 Title、Category、Source URL、Content、Tags，選填欄位缺少時優雅略過
- [ ] 3.7 實作「Notion rich text to Markdown conversion」：處理 heading、bullet、numbered list、code block 等常見 block 類型；不支援的 block 輸出 `[Unsupported block: <type>]` 佔位符
- [ ] 3.8 實作「Google Drive file update」：將 Markdown 內容透過 Drive API 覆寫 `GOOGLE_DRIVE_FILE_ID` 對應的檔案
- [ ] 3.9 實作「Sync failure logging」：每次執行（成功或失敗）都寫入帶時間戳的 log 檔；失敗時記錄錯誤訊息且以非零 exit code 結束
- [ ] 3.10 測試錯誤情境：驗證「Missing or invalid credentials」— `NOTION_TOKEN`、`NOTION_DATABASE_ID`、`GOOGLE_CREDENTIALS_PATH` 任一缺少時顯示清楚錯誤並中止
- [ ] 3.11 手動執行 `sync.py`，驗證「On-demand sync」：確認 Google Drive 上的檔案內容已更新，log 檔有成功紀錄
- [ ] 3.12 在 NotebookLM 中將步驟 3.3 的 Google Drive 檔案加入為來源，滿足「NotebookLM source linkage」的初始設定情境（一次性手動步驟）
- [ ] 3.13 執行一次同步後在 NotebookLM 中確認「Automatic content refresh」：查詢結果應反映最新 Notion 內容
- [ ] 3.14 設定 cron job（`crontab -e`）定期自動執行 `sync.py`，驗證「Scheduled or on-demand execution」規格的排程執行情境

## 4. 建立自動分類功能（依「自動分類：Claude API 回填 Category」決策）

- [ ] 4.1 取得 Anthropic API Key，設定 `ANTHROPIC_API_KEY` 環境變數，滿足「Claude API authentication」規格
- [ ] 4.2 安裝 `anthropic` Python 套件，在 `sync.py` 中加入自動分類模組
- [ ] 4.3 實作「Auto-categorization of uncategorized entries」：sync 時偵測 Category 為空的條目，呼叫 Claude API 推測分類並寫回 Notion
- [ ] 4.4 實作「Predefined category list」：prompt 中包含完整分類選項，確保回傳值符合 Notion Select 欄位的預設選項
- [ ] 4.5 實作「Categorization failure resilience」：單筆 Claude API 失敗時記 log 並繼續，不中止整個 sync
- [ ] 4.6 測試「Entry already has a Category」：手動設定分類的條目不被覆蓋
- [ ] 4.7 測試「Missing or invalid API key」：`ANTHROPIC_API_KEY` 缺少時僅記 warning，sync 主流程照常完成

## 5. 驗證查詢功能

- [ ] 5.1 確認匯出的 Markdown 字數在 500,000 字以內，滿足「NotebookLM capacity awareness」規格；若接近上限，規劃分割策略
- [ ] 5.2 在 NotebookLM 中測試「Keyword search in NotebookLM」：輸入知識條目中的關鍵字，確認能找到對應段落
- [ ] 5.3 在 NotebookLM 中測試「Natural language Q&A」：用自然語言問「我學過哪些關於 X 的東西？」，確認 AI 能給出整合性回答
- [ ] 5.4 確認「Source attribution in answers」：檢查 AI 回答中是否有標示來源文件與段落
- [ ] 5.5 測試「No relevant content found」：詢問知識庫中不存在的主題，確認 NotebookLM 不會憑空捏造答案
- [ ] 5.6 在手機瀏覽器開啟 NotebookLM，測試「Mobile access」：確認可在手機上正常執行關鍵字搜尋與自然語言問答
