## MODIFIED Requirements

### Requirement: Auto-categorization of uncategorized entries

The sync script SHALL detect Notion database entries where the Category field is empty and automatically assign a category by calling the Claude API using content that may include image recognition results, then write the result back to the Notion entry.

#### Scenario: Entry with no Category set (including image content)

- **WHEN** the sync script encounters an entry with an empty Category field
- **THEN** it SHALL send the entry's Title and Content (which may include image recognition text from `get_page_blocks()`) to the Claude API, receive a suggested category, and update the Notion entry's Category field via the Notion API

#### Scenario: Entry already has a Category

- **WHEN** the sync script encounters an entry with a Category already set
- **THEN** it SHALL skip auto-categorization for that entry and MUST NOT overwrite the existing value
