## MODIFIED Requirements

### Requirement: Auto-summarization of entries with block content but no Content property

The sync script SHALL detect Notion database entries where the Content property field is empty but the page body contains block content (including text and image blocks), generate a summary using the Claude API, and write the summary back to the Notion entry's Content field.

#### Scenario: Entry with block content and no Content property

- **WHEN** the sync script encounters an entry with an empty Content property but page blocks containing text or image content
- **THEN** it SHALL read the page block content using `get_page_blocks()` (which now includes image recognition results), call the Claude API to generate a concise summary, and update the Notion entry's Content field with the summary

#### Scenario: Entry already has Content

- **WHEN** the sync script encounters an entry with Content property already filled in
- **THEN** it SHALL skip auto-summarization for that entry and MUST NOT overwrite the existing content

#### Scenario: Entry blocks are empty

- **WHEN** the page blocks contain no text or image content
- **THEN** the script SHALL log the skip and leave the Content field empty, MUST NOT abort the sync
