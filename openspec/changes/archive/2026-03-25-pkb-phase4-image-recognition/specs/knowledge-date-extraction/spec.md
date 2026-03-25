## ADDED Requirements

### Requirement: Auto date extraction for entries without a date

The sync script SHALL detect Notion database entries where the Date Added field is empty and automatically extract the article publication date from the content by calling the Claude API, then write the result back to the Notion entry.

#### Scenario: Entry with no Date Added and extractable date in content

- **WHEN** the sync script encounters an entry with an empty Date Added field and the page content contains a publication date
- **THEN** it SHALL send the entry's content to the Claude API, receive the extracted date in ISO 8601 format (YYYY-MM-DD), and update the Notion entry's Date Added field via the Notion API

#### Scenario: Entry already has Date Added

- **WHEN** the sync script encounters an entry with Date Added already filled in
- **THEN** it SHALL skip date extraction for that entry and MUST NOT overwrite the existing date

#### Scenario: No date found in content

- **WHEN** the Claude API cannot identify a publication date in the content
- **THEN** the script SHALL log the skip and leave the Date Added field empty, MUST NOT abort the sync

### Requirement: Date extraction failure resilience

If the Claude API call fails for a specific entry during date extraction, the script SHALL log the failure and continue processing remaining entries without aborting the sync.

#### Scenario: Date extraction fails for one entry

- **WHEN** the Claude API returns an error for a specific entry during date extraction
- **THEN** the script SHALL log the error with the entry title, leave the Date Added field empty, and proceed to the next entry
