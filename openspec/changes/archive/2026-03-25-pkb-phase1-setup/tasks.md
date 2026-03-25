## 1. 建立 Notion 知識庫（輸入層）

- [x] 1.1 依照「Notion 資料庫欄位設計」決策，在 Notion 中建立知識庫 Database，新增 Title、Category（Select）、Source（URL）、Content（Text）、Tags（Multi-select）、Date Added（Date，設為自動填入）共六個欄位
- [x] 1.2 設定 Category 欄位的預設選項：技術、商業、生活、語言等分類
- [x] 1.3 驗證「Notion database structure」規格：建立一筆測試知識條目，確認所有欄位皆可正常輸入
- [x] 1.4 確認 Notion Web Clipper 瀏覽器擴充功能已安裝並連結帳號，測試「Web page capture」：擷取一個網頁確認內容存入知識庫
- [x] 1.5 在手機安裝 Notion App，測試「Manual text input」：用手機新增一筆知識條目，確認手機輸入流程順暢
- [x] 1.6 在手機安裝 Microsoft Lens（或等效 OCR 工具），測試「Image and photo OCR input」：拍一張含文字的照片，將 OCR 結果貼入 Notion

## 2. 建立 NotebookLM 問答層（依「選擇 NotebookLM 而非 Notion AI」決策）

- [x] 2.1 前往 notebooklm.google.com，用 Google 帳號登入，建立一個新的 Notebook，命名為「個人知識庫」
- [x] 2.2 將本機現有的 Word、PDF、純文字筆記直接上傳至 NotebookLM 作為來源（一次性舊資料匯入）
- [x] 2.3 從 Notion 手動匯出知識庫（Export as Markdown），上傳至 NotebookLM 做初始測試，確認「Upload to NotebookLM」流程可行
- [x] 2.4 【待 Phase 2 完成後驗證】測試「Keyword search in NotebookLM」：輸入關鍵字確認能找到對應段落
- [x] 2.5 【待 Phase 2 完成後驗證】測試「Natural language Q&A」：用自然語言提問，確認 AI 能給出整合性回答並標示「Source attribution in answers」
- [x] 2.6 【待 Phase 2 完成後驗證】測試「No relevant content found」：詢問知識庫中不存在的主題，確認 NotebookLM 不會憑空捏造答案
- [x] 2.7 【待 Phase 2 完成後驗證】在手機瀏覽器開啟 NotebookLM，測試「Mobile access」：確認可在手機上正常查詢
- [x] 2.8 【待 Phase 2 完成後驗證】確認匯出的 Markdown 字數在 500,000 字以內，滿足「NotebookLM capacity awareness」規格
