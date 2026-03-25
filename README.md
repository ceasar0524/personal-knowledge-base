# 個人知識庫系統

自動將 Notion 知識庫同步至 Google NotebookLM，並透過 Claude AI 自動補全摘要、分類、標籤與發布日期。

## 開發方式

本專案透過 [Claude Code](https://claude.ai/code)（AI 編程助理）與 [Spectra](https://github.com/spectra-ai/spectra)（Spec-Driven Development 工具）協作完成。由人主導需求與決策，AI 協助實作與規格管理。

## 系統架構

```
Notion（輸入層）
    │
    │  Notion API
    ▼
sync.py（同步腳本，每 6 小時自動執行）
    │
    ├── Claude AI 自動補全
    │       ├── 摘要（文字 + 圖片辨識）
    │       ├── 分類
    │       ├── 標籤
    │       └── 發布日期
    │
    │  Google Drive API
    ▼
Google Drive（Markdown 檔案）
    │
    ▼
Google NotebookLM（AI 問答）
```

## 使用工具

| 工具 | 用途 |
|------|------|
| [Notion](https://notion.so) | 知識條目輸入與管理 |
| [Notion API](https://developers.notion.com) | 讀取與回寫資料庫條目 |
| [Anthropic Claude API](https://www.anthropic.com) | 自動摘要、分類、標籤、日期擷取、圖片辨識 |
| [Google Drive API](https://developers.google.com/drive) | 上傳 Markdown 至 Google Drive |
| [Google NotebookLM](https://notebooklm.google.com) | 以 AI 問答方式查詢知識庫 |
| [Pillow](https://pillow.readthedocs.io) | 圖片壓縮（記憶體處理，不落地儲存） |
| cron | 每 6 小時自動執行同步 |

## 自動補全功能

每次同步時，針對尚未處理的條目自動執行：

- **摘要** — 從頁面內文（含圖片辨識結果）生成 3–5 條重點
- **分類** — 從預定義分類中選出最適合的一個
- **標籤** — 從參考清單推薦 1–3 個標籤，可自動新增新標籤
- **發布日期** — 從文章內容擷取發布日期，找不到時標記 `No Date`
- **圖片辨識** — 僅辨識手動上傳的圖片，Web Clipper 抓回的外部圖片略過

## 環境設定

1. 複製 `.env.example` 為 `.env`
2. 填入各項變數

```
NOTION_TOKEN=your_notion_integration_token
NOTION_DATABASE_ID=your_notion_database_id
GOOGLE_CREDENTIALS_PATH=/path/to/credentials.json
GOOGLE_DRIVE_FILE_ID=your_google_drive_file_id
ANTHROPIC_API_KEY=your_anthropic_api_key
AI_MODEL=claude-haiku-4-5-20251001
```

3. 放入 Google Service Account 的 `credentials.json`
4. 安裝相依套件：

```bash
pip install notion-client google-api-python-client google-auth anthropic pillow python-dotenv
```

## 自動同步設定（launchd）

macOS 建議使用 launchd 取代 cron，睡眠喚醒後會補跑錯過的任務。

建立 `~/Library/LaunchAgents/com.knowledgebase.sync.plist`：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.knowledgebase.sync</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/path/to/sync.py</string>
    </array>
    <key>StartInterval</key>
    <integer>21600</integer>
    <key>StandardOutPath</key>
    <string>/path/to/sync.log</string>
    <key>StandardErrorPath</key>
    <string>/path/to/sync.log</string>
    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
```

載入：

```bash
launchctl load ~/Library/LaunchAgents/com.knowledgebase.sync.plist
```
