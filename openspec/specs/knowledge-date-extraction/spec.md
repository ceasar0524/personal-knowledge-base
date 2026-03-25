# knowledge-date-extraction Specification

## Purpose

Enables the sync script to automatically extract article publication dates from page block content for Notion entries where the Date Added field is empty, using the Claude API to identify dates in ISO 8601 format.

## Requirements

### Requirement: Auto date extraction for entries without a date

The sync script SHALL detect Notion database entries where the Date Added field is empty and automatically extract the article publication date using the following two-step strategy, then write the result back to the Notion entry.

**Step 1 — URL regex (zero API cost):** The script SHALL first attempt to extract a date from the entry's URL using common URL date patterns (e.g., `/YYYY/MM/DD/`, `/YYYYMMDD/`, `?date=YYYY-MM-DD`). If a date is found, it SHALL be written immediately without calling the Claude API.

**Step 2 — Claude API:** If no date is found in the URL, the script SHALL send the entry's title, source URL (if available), and page block content (falling back to the Text summary field) to the Claude API, and update the Date Added field with the returned ISO 8601 date.

#### Scenario: Entry with no Date Added and date extractable from URL

- **WHEN** the sync script encounters an entry with an empty Date Added field and the URL contains a recognisable date pattern
- **THEN** it SHALL extract the date via regex and update the Notion entry's Date Added field without calling the Claude API

#### Scenario: Entry with no Date Added and extractable date in content

- **WHEN** the URL contains no date but the page content or URL hint contains a publication date
- **THEN** it SHALL send the entry's title, URL, and content to the Claude API, receive the extracted date in ISO 8601 format (YYYY-MM-DD), and update the Notion entry's Date Added field via the Notion API

#### Scenario: Entry already has Date Added

- **WHEN** the sync script encounters an entry with Date Added already filled in
- **THEN** it SHALL skip date extraction for that entry and MUST NOT overwrite the existing date

#### Scenario: No date found in content

- **WHEN** the Claude API cannot identify a publication date in the content
- **THEN** the script SHALL log the skip and leave the Date Added field empty, MUST NOT abort the sync. Entries without a date can be found in Notion by filtering `Date is empty`

### Requirement: Date extraction failure resilience

If the Claude API call fails for a specific entry during date extraction, the script SHALL log the failure and continue processing remaining entries without aborting the sync.

#### Scenario: Date extraction fails for one entry

- **WHEN** the Claude API returns an error for a specific entry during date extraction
- **THEN** the script SHALL log the error with the entry title, leave the Date Added field empty, and proceed to the next entry
