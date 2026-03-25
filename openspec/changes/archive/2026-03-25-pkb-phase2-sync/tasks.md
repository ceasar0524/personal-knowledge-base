## 1. 設定 API 憑證

- [x] 1.1 在 Notion 建立 Integration，取得 `NOTION_TOKEN`，將 Integration 連結至知識庫 Database，記下 `NOTION_DATABASE_ID`，滿足「Notion API authentication」規格
- [x] 1.2 在 Google Cloud Console 建立專案、啟用 Drive API、建立 Service Account 並下載憑證 JSON，設定 `GOOGLE_CREDENTIALS_PATH`，滿足「Google Drive API authentication」規格
- [x] 1.3 在 Google Drive 建立一個空白文件（`knowledge-base.md`），記下 `GOOGLE_DRIVE_FILE_ID`；將 Service Account email 加入該檔案的編輯權限

## 2. 建立同步腳本

- [x] 2.1 初始化 Python 專案，安裝 `notion-client`、`google-api-python-client`，建立 `sync.py` 框架
- [x] 2.2 實作「Automated sync script」：讀取 Notion 所有條目（含「Notion API pagination」分頁處理）
- [x] 2.3 實作「Markdown export format」：確保每筆條目包含 Title、Category、Source URL、Content、Tags，選填欄位缺少時優雅略過
- [x] 2.4 實作「Notion rich text to Markdown conversion」：處理 heading、bullet、numbered list、code block 等常見 block 類型；不支援的 block 輸出 `[Unsupported block: <type>]` 佔位符
- [x] 2.5 實作「Google Drive file update」：將 Markdown 內容透過 Drive API 覆寫 `GOOGLE_DRIVE_FILE_ID` 對應的檔案
- [x] 2.6 實作「Sync failure logging」：每次執行（成功或失敗）都寫入帶時間戳的 log 檔；失敗時記錄錯誤訊息且以非零 exit code 結束

## 3. 測試與驗證

- [x] 3.1 測試錯誤情境：驗證「Missing or invalid credentials」— `NOTION_TOKEN`、`NOTION_DATABASE_ID`、`GOOGLE_CREDENTIALS_PATH` 任一缺少時顯示清楚錯誤並中止
- [x] 3.2 手動執行 `sync.py`，驗證「On-demand sync」：確認 Google Drive 上的檔案內容已更新，log 檔有成功紀錄
- [x] 3.3 在 NotebookLM 中將 Google Drive 檔案加入為來源，滿足「NotebookLM source linkage」的初始設定情境（一次性手動步驟）
- [x] 3.4 執行一次同步後在 NotebookLM 中確認「Automatic content refresh」：查詢結果應反映最新 Notion 內容
- [x] 3.5 設定 cron job（`crontab -e`）定期自動執行 `sync.py`，驗證「Scheduled or on-demand execution」規格的排程執行情境
- [x] 3.6 確認匯出的 Markdown 字數在 500,000 字以內，滿足「NotebookLM capacity awareness」規格；若接近上限，規劃分割策略
