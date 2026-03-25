# knowledge-capture Specification

## Purpose

TBD - created by archiving change 'personal-knowledge-base'. Update Purpose after archive.

## Requirements

### Requirement: Notion database structure

The system SHALL use a Notion database with the following fields: Title (Title type), Category (Select type), Source (URL type), Content (Text type), Tags (Multi-select type), and Date Added (Date type, auto-filled).

#### Scenario: Creating a new knowledge entry

- **WHEN** a user learns something new and opens Notion
- **THEN** the user SHALL be able to create a new database entry by filling in at minimum the Title and Content fields; all other fields are optional

#### Scenario: Category classification

- **WHEN** a user creates a new entry
- **THEN** the user SHALL be able to select a category from predefined options (e.g., Technology, Business, Life, Language)

---
### Requirement: Manual text input

The system SHALL support direct text entry into the Content field of the Notion database.

#### Scenario: Direct typing

- **WHEN** a user wants to record knowledge by typing
- **THEN** the user SHALL be able to open Notion on desktop or mobile and type directly into a new database entry

---
### Requirement: Web page capture

The system SHALL support one-click web page saving via the Notion Web Clipper browser extension.

#### Scenario: Saving a web article

- **WHEN** a user is reading a web page and wants to save it
- **THEN** the user SHALL be able to click the Notion Web Clipper extension to save the page title, URL, and content into the knowledge database

---
### Requirement: Image and photo OCR input

The system SHALL support knowledge capture from photos and screenshots by first converting image text to plain text using an OCR tool (e.g., Microsoft Lens) before pasting into Notion.

#### Scenario: Capturing knowledge from a photo

- **WHEN** a user takes a photo or screenshot of text they want to remember
- **THEN** the user SHALL use Microsoft Lens (or equivalent OCR tool) to convert the image to text, then paste the resulting text into a new Notion entry
