## ADDED Requirements

### Requirement: Auto-summarization of entries with block content but no Content property

The sync script SHALL detect Notion database entries where the Content property field is empty but the page body contains block content, generate a summary using the Claude API, and write the summary back to the Notion entry's Content field.

#### Scenario: Entry with block content and no Content property

- **WHEN** the sync script encounters an entry with an empty Content property but page blocks containing text
- **THEN** it SHALL read the page block content using `get_page_blocks()`, call the Claude API to generate a concise summary, and update the Notion entry's Content field with the summary

#### Scenario: Entry already has Content

- **WHEN** the sync script encounters an entry with Content property already filled in
- **THEN** it SHALL skip auto-summarization for that entry and MUST NOT overwrite the existing content

#### Scenario: Entry blocks are empty

- **WHEN** the page blocks contain no text content
- **THEN** the script SHALL log the skip and leave the Content field empty, MUST NOT abort the sync

### Requirement: Summary generation via Claude API

The sync script SHALL generate a concise summary (3–5 bullet points) of the page block content using the Claude API.

#### Scenario: Successful summarization

- **WHEN** the page block content is successfully read
- **THEN** the Claude API SHALL return a summary in Traditional Chinese, and the script SHALL write it to the Notion Content field

### Requirement: Summarization failure resilience

If the summarization fails for a specific entry (e.g., Claude API error, empty block content), the script SHALL log the failure and continue processing remaining entries without aborting the sync.

#### Scenario: Summarization fails for one entry

- **WHEN** the Claude API fails for a specific entry
- **THEN** the script SHALL log the error with the entry title, leave the Content field empty, and proceed to the next entry
