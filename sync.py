#!/usr/bin/env python3
"""
Knowledge Base Sync Script
Notion API → (Auto-summarize + Auto-categorize) → Markdown → Google Drive → NotebookLM
"""

import os
import sys
import base64
import io
import logging
import re
import ssl
import urllib.request
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

from notion_client import Client as NotionClient
from notion_client.errors import APIResponseError
from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload
from google.oauth2 import service_account
import anthropic
from PIL import Image

# ── 載入環境變數 ────────────────────────────────────────────────
load_dotenv()

NOTION_TOKEN            = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID      = os.getenv("NOTION_DATABASE_ID")
GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH")
GOOGLE_DRIVE_FILE_ID    = os.getenv("GOOGLE_DRIVE_FILE_ID")
ANTHROPIC_API_KEY       = os.getenv("ANTHROPIC_API_KEY")
AI_MODEL                = os.getenv("AI_MODEL", "claude-haiku-4-5-20251001")

LOG_FILE = Path(__file__).parent / "sync.log"
SCOPES   = ["https://www.googleapis.com/auth/drive"]

CATEGORIES = ["技術", "商業", "生活", "語言", "其他"]

TAGS = [
    "Generative AI",
    "AWS AI",
    "Azure AI",
    "Prompt engineering",
    "AI Governance",
    "Digital Transformation",
    "Technical Writing",
    "Cloud Strategy",
]

# ── 日誌設定 ─────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger(__name__)


# ── 驗證環境變數 ─────────────────────────────────────────────────
def validate_env():
    missing = [k for k, v in {
        "NOTION_TOKEN": NOTION_TOKEN,
        "NOTION_DATABASE_ID": NOTION_DATABASE_ID,
        "GOOGLE_CREDENTIALS_PATH": GOOGLE_CREDENTIALS_PATH,
        "GOOGLE_DRIVE_FILE_ID": GOOGLE_DRIVE_FILE_ID,
    }.items() if not v]

    if missing:
        log.error(f"缺少必要的環境變數：{', '.join(missing)}")
        sys.exit(1)

    if not Path(GOOGLE_CREDENTIALS_PATH).exists():
        log.error(f"找不到 Google 憑證檔：{GOOGLE_CREDENTIALS_PATH}")
        sys.exit(1)

    if not ANTHROPIC_API_KEY:
        log.warning("ANTHROPIC_API_KEY 未設定，將跳過自動摘要與自動分類")


# ── Notion Rich Text → Markdown ──────────────────────────────────
def rich_text_to_str(rich_text_list: list) -> str:
    return "".join(t.get("plain_text", "") for t in rich_text_list)


def _recognize_image(ai: anthropic.Anthropic, url: str) -> str:
    """下載圖片、壓縮後以 Claude Vision API 辨識，回傳文字描述。失敗時回傳空字串。"""
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
            raw = resp.read()
    except Exception as e:
        log.warning(f"圖片辨識：下載失敗（{url[:80]}）：{e}")
        return ""

    try:
        img = Image.open(io.BytesIO(raw)).convert("RGB")
        img.thumbnail((1024, 1024), Image.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=70)
        b64 = base64.standard_b64encode(buf.getvalue()).decode()
    except Exception as e:
        log.warning(f"圖片辨識：壓縮失敗：{e}")
        return ""

    try:
        resp = ai.messages.create(
            model=AI_MODEL,
            max_tokens=256,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {"type": "base64", "media_type": "image/jpeg", "data": b64},
                    },
                    {"type": "text", "text": "請描述這張圖片中的文字內容或主要資訊，用繁體中文回答，若無文字則簡短說明圖片主題。"},
                ],
            }],
        )
        return resp.content[0].text.strip()
    except Exception as e:
        log.warning(f"圖片辨識：Claude Vision API 失敗：{e}")
        return ""


def blocks_to_markdown(blocks: list, ai: anthropic.Anthropic | None = None) -> str:
    lines = []
    for block in blocks:
        btype = block.get("type", "")
        data  = block.get(btype, {})

        if btype == "paragraph":
            text = rich_text_to_str(data.get("rich_text", []))
            lines.append(text)

        elif btype == "heading_1":
            text = rich_text_to_str(data.get("rich_text", []))
            lines.append(f"# {text}")

        elif btype == "heading_2":
            text = rich_text_to_str(data.get("rich_text", []))
            lines.append(f"## {text}")

        elif btype == "heading_3":
            text = rich_text_to_str(data.get("rich_text", []))
            lines.append(f"### {text}")

        elif btype == "bulleted_list_item":
            text = rich_text_to_str(data.get("rich_text", []))
            lines.append(f"- {text}")

        elif btype == "numbered_list_item":
            text = rich_text_to_str(data.get("rich_text", []))
            lines.append(f"1. {text}")

        elif btype == "code":
            text = rich_text_to_str(data.get("rich_text", []))
            lang = data.get("language", "")
            lines.append(f"```{lang}\n{text}\n```")

        elif btype == "quote":
            text = rich_text_to_str(data.get("rich_text", []))
            lines.append(f"> {text}")

        elif btype == "image":
            img_url = data.get("file", {}).get("url", "")  # 只處理手動上傳的圖片
            if ai and img_url:
                desc = _recognize_image(ai, img_url)
                if desc:
                    lines.append(f"[圖片內容：{desc}]")
                else:
                    lines.append("[圖片內容：無法辨識]")
            else:
                lines.append("[圖片]")

        else:
            lines.append(f"[Unsupported block: {btype}]")

        lines.append("")  # 空行分隔

    return "\n".join(lines).strip()


# ── 取得 Notion 頁面的 block 內容 ────────────────────────────────
def get_page_blocks(notion: NotionClient, page_id: str, ai: anthropic.Anthropic | None = None) -> str:
    blocks = []
    cursor = None
    while True:
        kwargs = {"block_id": page_id}
        if cursor:
            kwargs["start_cursor"] = cursor
        resp = notion.blocks.children.list(**kwargs)
        blocks.extend(resp.get("results", []))
        if not resp.get("has_more"):
            break
        cursor = resp.get("next_cursor")
    return blocks_to_markdown(blocks, ai=ai)


# ── 從 Notion 讀取所有資料庫條目（含 pagination）────────────────
def fetch_all_entries(notion: NotionClient) -> list[dict]:
    entries = []
    cursor  = None
    while True:
        kwargs = {"database_id": NOTION_DATABASE_ID}
        if cursor:
            kwargs["start_cursor"] = cursor
        resp = notion.databases.query(**kwargs)
        entries.extend(resp.get("results", []))
        if not resp.get("has_more"):
            break
        cursor = resp.get("next_cursor")
    return entries


# ── 自動摘要：讀取 block 內容 → Claude API → 寫回 Content ────────
def auto_summarize_entry(notion: NotionClient, ai: anthropic.Anthropic, entry: dict):
    props = entry.get("properties", {})
    content_prop = props.get("Text", props.get("Content", {}))
    existing_content = rich_text_to_str(content_prop.get("rich_text", []))

    if existing_content:
        return  # 已有 Content，不覆蓋

    title = rich_text_to_str(
        props.get("Name", props.get("Title", {})).get("title", [])
    )

    try:
        block_text = get_page_blocks(notion, entry["id"], ai=ai)
    except Exception as e:
        log.warning(f"摘要：無法讀取 blocks（{title}）：{e}")
        return

    if not block_text:
        log.info(f"摘要：頁面 blocks 為空，跳過（{title}）")
        return

    try:
        resp = ai.messages.create(
            model=AI_MODEL,
            max_tokens=512,
            messages=[{
                "role": "user",
                "content": (
                    f"請將以下文章內容整理成 3–5 條繁體中文重點摘要，每條以「• 」開頭：\n\n{block_text[:3000]}"
                ),
            }],
        )
        summary = resp.content[0].text.strip()
    except Exception as e:
        log.warning(f"摘要：Claude API 失敗（{title}）：{e}")
        return

    try:
        notion.pages.update(
            page_id=entry["id"],
            properties={
                "Text": {
                    "rich_text": [{"text": {"content": summary}}]
                }
            },
        )
        log.info(f"摘要：已寫回 Content（{title}）")
    except Exception as e:
        log.warning(f"摘要：寫回 Notion 失敗（{title}）：{e}")


# ── 自動分類：Claude API 推測分類 → 寫回 Category ────────────────
def auto_categorize_entry(notion: NotionClient, ai: anthropic.Anthropic, entry: dict):
    props = entry.get("properties", {})
    category_prop = props.get("Select", props.get("Category", {}))
    existing_category = category_prop.get("select")

    if existing_category:
        return  # 已有 Category，不覆蓋

    title = rich_text_to_str(
        props.get("Name", props.get("Title", {})).get("title", [])
    )
    content = rich_text_to_str(props.get("Content", {}).get("rich_text", []))
    category_list = "、".join(CATEGORIES)

    try:
        resp = ai.messages.create(
            model=AI_MODEL,
            max_tokens=16,
            messages=[{
                "role": "user",
                "content": (
                    f"請從以下分類中選出最適合的一個，只回傳分類名稱，不要其他文字。\n"
                    f"分類選項：{category_list}\n\n"
                    f"標題：{title}\n"
                    f"內容：{content[:500]}"
                ),
            }],
        )
        raw = resp.content[0].text.strip()
        # 確保回傳值在預定義清單中
        category = raw if raw in CATEGORIES else "其他"
    except Exception as e:
        log.warning(f"分類：Claude API 失敗（{title}）：{e}")
        return

    try:
        notion.pages.update(
            page_id=entry["id"],
            properties={
                "Select": {
                    "select": {"name": category}
                }
            },
        )
        log.info(f"分類：已寫回 Category「{category}」（{title}）")
    except Exception as e:
        log.warning(f"分類：寫回 Notion 失敗（{title}）：{e}")


# ── 自動標籤：Claude API 推測標籤 → 寫回 Multi-select ────────────
def auto_tag_entry(notion: NotionClient, ai: anthropic.Anthropic, entry: dict):
    props = entry.get("properties", {})
    existing_tags = props.get("Multi-select", {}).get("multi_select", [])

    if existing_tags:
        return  # 已有 Tags，不覆蓋

    title = rich_text_to_str(
        props.get("Name", props.get("Title", {})).get("title", [])
    )

    # 優先從 page blocks（原文）取得內容，fallback 到 Text 摘要
    try:
        content = get_page_blocks(notion, entry["id"])
    except Exception:
        content = ""
    if not content:
        content = rich_text_to_str(props.get("Text", props.get("Content", {})).get("rich_text", []))

    tag_list = ", ".join(TAGS)

    try:
        resp = ai.messages.create(
            model=AI_MODEL,
            max_tokens=64,
            messages=[{
                "role": "user",
                "content": (
                    f"請根據以下文章的標題與內容，從參考清單中選出 1–3 個最相關的標籤。"
                    f"優先使用參考清單中的標籤，若內容明顯屬於清單以外的主題，可額外建議英文短標籤。"
                    f"只回傳標籤名稱，用逗號分隔，不要其他文字。\n\n"
                    f"參考標籤清單：{tag_list}\n\n"
                    f"標題：{title}\n"
                    f"內容：{content[:500]}"
                ),
            }],
        )
        raw = resp.content[0].text.strip()
        tags = [
            t.strip() for t in raw.split(",")
            if t.strip() and "無" not in t and len(t.strip()) <= 30
        ][:3]
    except Exception as e:
        log.warning(f"標籤：Claude API 失敗（{title}）：{e}")
        return

    if not tags:
        return

    try:
        notion.pages.update(
            page_id=entry["id"],
            properties={
                "Multi-select": {
                    "multi_select": [{"name": t} for t in tags]
                }
            },
        )
        log.info(f"標籤：已寫回 Tags {tags}（{title}）")
    except Exception as e:
        log.warning(f"標籤：寫回 Notion 失敗（{title}）：{e}")


# ── 從 URL 以 regex 嘗試擷取日期 ─────────────────────────────────
_URL_DATE_PATTERNS = [
    re.compile(r"/(\d{4})/(\d{2})/(\d{2})"),   # /2025/01/15/
    re.compile(r"/(\d{4})/(\d{2})/"),            # /2025/01/
    re.compile(r"[/_-](\d{4})(\d{2})(\d{2})[/_-]"),  # /20250115/
    re.compile(r"[?&]date=(\d{4}-\d{2}-\d{2})"), # ?date=2025-01-15
]

def _extract_date_from_url(url: str) -> str:
    """從 URL 以 regex 嘗試擷取日期，成功回傳 YYYY-MM-DD，否則回傳空字串。"""
    for pattern in _URL_DATE_PATTERNS:
        m = pattern.search(url)
        if not m:
            continue
        groups = m.groups()
        if len(groups) == 1:          # ?date= 格式，已是 YYYY-MM-DD
            return groups[0]
        elif len(groups) == 2:        # /YYYY/MM/ 格式，補 01 日
            year, month = groups
            return f"{year}-{month}-01"
        else:                         # /YYYY/MM/DD/ 或 YYYYMMDD 格式
            year, month, day = groups
            return f"{year}-{month}-{day}"
    return ""


# ── 自動日期擷取：URL regex → Claude API → 寫回 Date ─────────────
def auto_extract_date_entry(notion: NotionClient, ai: anthropic.Anthropic, entry: dict):
    props = entry.get("properties", {})
    existing_date = props.get("Date", {}).get("date")

    if existing_date:
        return  # 已有日期，不覆蓋

    title = rich_text_to_str(
        props.get("Name", props.get("Title", {})).get("title", [])
    )
    url = props.get("URL", props.get("Source", {})).get("url") or ""

    # Step 1：先嘗試從 URL regex 擷取（免費，零 token）
    if url:
        date_from_url = _extract_date_from_url(url)
        if date_from_url:
            try:
                notion.pages.update(
                    page_id=entry["id"],
                    properties={"Date": {"date": {"start": date_from_url}}},
                )
                log.info(f"日期擷取（URL）：已寫回 Date「{date_from_url}」（{title}）")
            except Exception as e:
                log.warning(f"日期擷取（URL）：寫回 Notion 失敗（{title}）：{e}")
            return

    # Step 2：從 page blocks 或 Text 摘要讀取內容，連同 URL 一起送給 Claude
    try:
        content = get_page_blocks(notion, entry["id"])
    except Exception:
        content = ""

    if not content:
        content = rich_text_to_str(props.get("Text", props.get("Content", {})).get("rich_text", []))

    if not content and not url:
        return

    try:
        url_hint = f"來源 URL：{url}\n" if url else ""
        resp = ai.messages.create(
            model=AI_MODEL,
            max_tokens=16,
            messages=[{
                "role": "user",
                "content": (
                    f"請從以下資訊中找出文章的發布日期，只回傳 ISO 8601 格式（YYYY-MM-DD），"
                    f"若找不到發布日期則只回傳「無」，不要其他文字。\n\n"
                    f"標題：{title}\n"
                    f"{url_hint}"
                    f"內容：{content[:1000]}"
                ),
            }],
        )
        raw = resp.content[0].text.strip()
    except Exception as e:
        log.warning(f"日期擷取：Claude API 失敗（{title}）：{e}")
        return

    if raw == "無" or not re.match(r"^\d{4}-\d{2}-\d{2}$", raw):
        log.info(f"日期擷取：未找到發布日期，跳過（{title}）")
        return

    try:
        notion.pages.update(
            page_id=entry["id"],
            properties={
                "Date": {
                    "date": {"start": raw}
                }
            },
        )
        log.info(f"日期擷取：已寫回 Date「{raw}」（{title}）")
    except Exception as e:
        log.warning(f"日期擷取：寫回 Notion 失敗（{title}）：{e}")


# ── 將 Notion 條目轉換為 Markdown 區塊 ──────────────────────────
def entry_to_markdown(notion: NotionClient, entry: dict) -> str:
    props = entry.get("properties", {})

    def get_title(prop):
        items = prop.get("title", [])
        return rich_text_to_str(items)

    def get_select(prop):
        sel = prop.get("select")
        return sel.get("name", "") if sel else ""

    def get_url(prop):
        return prop.get("url") or ""

    def get_rich_text(prop):
        return rich_text_to_str(prop.get("rich_text", []))

    def get_multiselect(prop):
        items = prop.get("multi_select", [])
        return ", ".join(i["name"] for i in items)

    title    = get_title(props.get("Name", props.get("Title", {})))
    category = get_select(props.get("Select", props.get("Category", {})))
    source   = get_url(props.get("URL", props.get("Source", {})))
    content  = get_rich_text(props.get("Text", props.get("Content", {})))
    tags     = get_multiselect(props.get("Multi-select", props.get("Tags", {})))

    # 如果 Content 欄位為空，嘗試讀取頁面 block 內容
    if not content:
        try:
            content = get_page_blocks(notion, entry["id"])
        except Exception:
            content = ""

    lines = [f"## {title}"]
    if category:
        lines.append(f"**分類：** {category}")
    if source:
        lines.append(f"**來源：** {source}")
    if tags:
        lines.append(f"**標籤：** {tags}")
    if content:
        lines.append(f"\n{content}")

    return "\n".join(lines)


# ── 上傳 Markdown 至 Google Drive ───────────────────────────────
def upload_to_drive(markdown: str):
    creds = service_account.Credentials.from_service_account_file(
        GOOGLE_CREDENTIALS_PATH, scopes=SCOPES
    )
    service = build("drive", "v3", credentials=creds, cache_discovery=False)

    media = MediaInMemoryUpload(
        markdown.encode("utf-8"),
        mimetype="text/plain",
        resumable=False,
    )
    service.files().update(
        fileId=GOOGLE_DRIVE_FILE_ID,
        media_body=media,
    ).execute()


# ── 主程式 ───────────────────────────────────────────────────────
def main():
    validate_env()
    log.info("=== 同步開始 ===")

    notion = NotionClient(auth=NOTION_TOKEN)

    try:
        entries = fetch_all_entries(notion)
    except APIResponseError as e:
        log.error(f"Notion API 錯誤：{e}")
        sys.exit(1)

    log.info(f"讀取到 {len(entries)} 筆條目")

    # AI 自動補全（需要 Claude API）
    if ANTHROPIC_API_KEY:
        ai = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        log.info("開始 AI 自動補全（摘要、分類、標籤、日期）...")
        for entry in entries:
            auto_summarize_entry(notion, ai, entry)
            auto_categorize_entry(notion, ai, entry)
            auto_tag_entry(notion, ai, entry)
            auto_extract_date_entry(notion, ai, entry)
        # 重新讀取條目（AI 補全已寫回 Notion）
        try:
            entries = fetch_all_entries(notion)
        except APIResponseError as e:
            log.error(f"重新讀取 Notion 失敗：{e}")
            sys.exit(1)
    else:
        log.warning("略過 AI 自動補全（ANTHROPIC_API_KEY 未設定）")

    # 轉換為 Markdown
    sections = [
        f"# 個人知識庫\n*最後同步：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
    ]
    for entry in entries:
        try:
            sections.append(entry_to_markdown(notion, entry))
        except Exception as e:
            title = entry.get("id", "unknown")
            log.warning(f"條目轉換失敗（{title}）：{e}")

    markdown = "\n\n---\n\n".join(sections)

    # 上傳至 Google Drive
    try:
        upload_to_drive(markdown)
    except Exception as e:
        log.error(f"Google Drive 上傳失敗：{e}")
        sys.exit(1)

    log.info(f"同步完成，共 {len(entries)} 筆條目已上傳至 Google Drive")
    log.info("=== 同步結束 ===")


if __name__ == "__main__":
    main()
