# knowledge-tagging Specification

## Purpose

Enables the sync script to automatically assign relevant tags to Notion entries where the Tags field is empty, using the Claude API with a predefined reference list while allowing new tags to be created for content outside the predefined options.

## Requirements

### Requirement: Auto-tagging of untagged entries

The sync script SHALL detect Notion database entries where the Tags field (Multi-select) is empty and automatically assign relevant tags by calling the Claude API, then write the results back to the Notion entry.

#### Scenario: Entry with no Tags set

- **WHEN** the sync script encounters an entry with an empty Tags field
- **THEN** it SHALL read the entry's page block content first (falling back to the Text summary field if blocks are unavailable), send the Title and content to the Claude API, receive 1–3 suggested tags, and update the Notion entry's Tags field via the Notion API

#### Scenario: Entry already has Tags

- **WHEN** the sync script encounters an entry with Tags already set
- **THEN** it SHALL skip auto-tagging for that entry and MUST NOT overwrite the existing tags

### Requirement: Predefined tag list for auto-tagging with extensibility

The Claude API prompt for tagging SHALL include a predefined list of reference tags. Claude SHALL prioritize tags from this list for consistency, but MAY suggest additional tags in English when the content clearly falls outside the predefined options. All returned tags SHALL be written to the Notion Tags field; the Notion API will automatically create new Multi-select options if needed.

#### Scenario: Tags match predefined list

- **WHEN** Claude returns tags that match the predefined options
- **THEN** the script SHALL write those values to the Notion Tags field

#### Scenario: Tag does not match predefined list

- **WHEN** Claude returns a tag that does not match any predefined option
- **THEN** the script SHALL still write that tag to the Notion Tags field, allowing Notion to create a new Multi-select option

### Requirement: Auto-tagging failure resilience

If the Claude API call fails for a specific entry during tagging, the script SHALL log the failure and continue processing remaining entries without aborting the sync.

#### Scenario: Tagging fails for one entry

- **WHEN** the Claude API returns an error for a specific entry during tagging
- **THEN** the script SHALL log the error with the entry title, leave the Tags field empty, and proceed to the next entry
