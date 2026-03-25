## ADDED Requirements

### Requirement: Auto-categorization of uncategorized entries

The sync script SHALL detect Notion database entries where the Category field is empty and automatically assign a category by calling the Claude API, then write the result back to the Notion entry.

#### Scenario: Entry with no Category set

- **WHEN** the sync script encounters an entry with an empty Category field
- **THEN** it SHALL send the entry's Title and Content to the Claude API, receive a suggested category, and update the Notion entry's Category field via the Notion API

#### Scenario: Entry already has a Category

- **WHEN** the sync script encounters an entry with a Category already set
- **THEN** it SHALL skip auto-categorization for that entry and MUST NOT overwrite the existing value

### Requirement: Predefined category list

The Claude API prompt SHALL include the predefined list of valid categories (e.g., Technology, Business, Life, Language) so that the returned category matches one of the existing Notion Select options.

#### Scenario: Category matches predefined list

- **WHEN** Claude returns a category that matches one of the predefined options
- **THEN** the script SHALL write that value to the Notion Category field

#### Scenario: Category does not match predefined list

- **WHEN** Claude returns a category that does not match any predefined option
- **THEN** the script SHALL fall back to the closest matching predefined category and MUST NOT create a new Select option in Notion

### Requirement: Configurable AI model

The sync script SHALL read the AI model name from the `AI_MODEL` environment variable, defaulting to `claude-haiku-4-5-20251001` if not set. Both auto-categorization and auto-summarization SHALL use the same model setting.

#### Scenario: AI_MODEL not set

- **WHEN** `AI_MODEL` environment variable is not set
- **THEN** the script SHALL use `claude-haiku-4-5-20251001` as the default model

#### Scenario: AI_MODEL set to a different model

- **WHEN** `AI_MODEL` is set to a valid model identifier (e.g., `claude-sonnet-4-6`)
- **THEN** the script SHALL use that model for all Claude API calls

### Requirement: Claude API authentication

The sync script SHALL authenticate with the Claude API using an API key stored in an environment variable (`ANTHROPIC_API_KEY`).

#### Scenario: Valid API key provided

- **WHEN** `ANTHROPIC_API_KEY` is set and valid
- **THEN** the script SHALL successfully call the Claude API for categorization

#### Scenario: Missing or invalid API key

- **WHEN** `ANTHROPIC_API_KEY` is missing or invalid
- **THEN** the script SHALL log a warning and skip auto-categorization for that sync run, MUST NOT abort the entire sync

### Requirement: Categorization failure resilience

If the Claude API call fails for a specific entry (e.g., timeout, rate limit), the script SHALL log the failure and continue processing remaining entries without aborting the sync.

#### Scenario: Claude API call fails for one entry

- **WHEN** the Claude API returns an error for a specific entry
- **THEN** the script SHALL log the error with the entry title, leave the Category field empty, and proceed to the next entry
