## ADDED Requirements

### Requirement: Automated sync script

The system SHALL include a Python script (`sync.py`) that reads all entries from the Notion knowledge database via the Notion API, converts them to Markdown, and writes the result to a designated Google Drive file.

#### Scenario: Running the sync script

- **WHEN** the sync script is executed
- **THEN** it SHALL fetch all entries from the configured Notion database, generate a single Markdown document, and overwrite the designated Google Drive file with the new content

### Requirement: Notion API authentication

The sync script SHALL authenticate with the Notion API using a Notion Integration Token stored in an environment variable (`NOTION_TOKEN`) and a database ID stored in an environment variable (`NOTION_DATABASE_ID`).

#### Scenario: Valid credentials provided

- **WHEN** both `NOTION_TOKEN` and `NOTION_DATABASE_ID` are set and valid
- **THEN** the script SHALL successfully connect to the Notion API and retrieve all database entries

#### Scenario: Missing or invalid credentials

- **WHEN** either `NOTION_TOKEN` or `NOTION_DATABASE_ID` is missing or invalid
- **THEN** the script SHALL exit with a clear error message and MUST NOT proceed with the sync

### Requirement: Notion API pagination

The sync script SHALL handle Notion API pagination to ensure all database entries are retrieved, not just the first page (Notion API returns at most 100 entries per request).

#### Scenario: Database with more than 100 entries

- **WHEN** the Notion database contains more than 100 entries
- **THEN** the script SHALL follow the `next_cursor` pagination token and fetch all pages until no more entries remain

### Requirement: Markdown export format

The sync script SHALL convert each Notion database entry into a Markdown block containing the entry's Title, Category, Source URL, Content, and Tags.

#### Scenario: Entry with all fields populated

- **WHEN** a Notion entry has all six fields filled in
- **THEN** the exported Markdown SHALL include all fields in a consistent, readable format

#### Scenario: Entry with optional fields missing

- **WHEN** a Notion entry is missing optional fields (e.g., Source URL or Tags)
- **THEN** the exported Markdown SHALL omit those fields gracefully without errors

### Requirement: Google Drive API authentication

The sync script SHALL authenticate with the Google Drive API using a service account credentials JSON file, with the path stored in an environment variable (`GOOGLE_CREDENTIALS_PATH`).

#### Scenario: Valid credentials file provided

- **WHEN** `GOOGLE_CREDENTIALS_PATH` points to a valid service account JSON file
- **THEN** the script SHALL authenticate and gain write access to the designated Google Drive file

#### Scenario: Missing or invalid credentials file

- **WHEN** `GOOGLE_CREDENTIALS_PATH` is missing or the file is invalid
- **THEN** the script SHALL exit with a clear error message and MUST NOT attempt to write to Google Drive

### Requirement: Google Drive file update

The sync script SHALL overwrite a designated Google Drive file (identified by `GOOGLE_DRIVE_FILE_ID`) with the newly generated Markdown content after each sync.

#### Scenario: Successful Drive file update

- **WHEN** the script has generated the Markdown content and Drive credentials are valid
- **THEN** it SHALL overwrite the existing Google Drive file with the new Markdown content

### Requirement: NotebookLM source linkage

The NotebookLM Notebook SHALL have the designated Google Drive file added as a source, so that NotebookLM automatically reflects the latest content after each Drive file update.

#### Scenario: Initial NotebookLM setup

- **WHEN** setting up NotebookLM for the first time
- **THEN** the user SHALL add the designated Google Drive file as a source in the NotebookLM Notebook (one-time manual step)

#### Scenario: Automatic content refresh

- **WHEN** the sync script updates the Google Drive file
- **THEN** NotebookLM SHALL reflect the updated content on the next query without any manual intervention

### Requirement: Notion rich text to Markdown conversion

The sync script SHALL convert Notion rich text block types to their Markdown equivalents when exporting the Content field. Unsupported block types SHALL be exported as plain text with a note indicating the original block type.

#### Scenario: Common block types conversion

- **WHEN** the Content field contains headings, bullet lists, numbered lists, or code blocks
- **THEN** the script SHALL convert them to `#`/`##`/`###`, `-`, `1.`, and ` ``` ` Markdown syntax respectively

#### Scenario: Unsupported block type

- **WHEN** the Content field contains a block type not supported by the conversion (e.g., embedded database, synced block)
- **THEN** the script SHALL export a plain text placeholder such as `[Unsupported block: <type>]` and MUST NOT silently drop the content

### Requirement: Scheduled or on-demand execution

The sync script SHALL support both on-demand execution (manual trigger) and scheduled execution via cron job.

#### Scenario: On-demand sync

- **WHEN** a user manually runs the sync script
- **THEN** it SHALL complete the full pipeline (Notion → Markdown → Drive) and report success or failure

#### Scenario: Scheduled sync via cron

- **WHEN** the sync script is configured as a recurring cron job
- **THEN** it SHALL execute automatically at the configured interval without user intervention

### Requirement: Sync failure logging

The sync script SHALL write a timestamped log entry to a local log file on every execution, recording success or the error message on failure.

#### Scenario: Successful scheduled sync

- **WHEN** the cron job completes successfully
- **THEN** the script SHALL append a success entry with timestamp and number of entries synced to the log file

#### Scenario: Failed scheduled sync

- **WHEN** the cron job encounters an error (e.g., API failure, network timeout, invalid credentials)
- **THEN** the script SHALL append an error entry with timestamp and error details to the log file, and MUST NOT silently exit with code 0
