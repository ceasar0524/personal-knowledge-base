# knowledge-query Specification

## Purpose

TBD - created by archiving change 'personal-knowledge-base'. Update Purpose after archive.

## Requirements

### Requirement: Keyword search in NotebookLM

The system SHALL support keyword-based search within NotebookLM to locate relevant passages from uploaded knowledge sources.

#### Scenario: Finding entries by keyword

- **WHEN** a user wants to find what they have learned about a specific topic
- **THEN** the user SHALL be able to type a keyword in the NotebookLM interface and see relevant passages highlighted from the source documents

---
### Requirement: Natural language Q&A

The system SHALL support natural language questions directed at the NotebookLM Notebook, with AI-generated answers that reference source material.

#### Scenario: Asking a question about past learning

- **WHEN** a user asks a natural language question such as "What do I know about X?"
- **THEN** NotebookLM SHALL provide a synthesized answer and MUST cite the specific source passages it used

#### Scenario: No relevant content found

- **WHEN** a user asks a question about a topic that does not exist in any uploaded source document
- **THEN** NotebookLM SHALL indicate that no relevant information was found and MUST NOT generate an answer unsupported by the source material

---
### Requirement: Mobile access

The system SHALL be accessible from a mobile device (iOS or Android) via the NotebookLM mobile web interface.

#### Scenario: Querying the knowledge base from a phone

- **WHEN** a user is away from their computer and wants to look up something they learned
- **THEN** the user SHALL be able to open NotebookLM in a mobile browser, select their Notebook, and perform keyword search or natural language Q&A

---
### Requirement: NotebookLM capacity awareness

The system SHALL remain within NotebookLM's limits of 50 source documents per Notebook and 500,000 words per source document. When the exported Markdown approaches these limits, the system SHALL provide a warning.

#### Scenario: Single export file within word limit

- **WHEN** the exported Markdown file is under 500,000 words
- **THEN** it SHALL be uploadable to NotebookLM as a single source document without issue

#### Scenario: Export file exceeds word limit

- **WHEN** the exported Markdown file exceeds 500,000 words
- **THEN** the sync script SHALL warn the user and MUST NOT silently upload a truncated file; the user SHALL decide how to split the content across multiple source documents

---
### Requirement: Source attribution in answers

The system SHALL display the source passage and document name for every AI-generated answer in NotebookLM.

#### Scenario: Verifying an answer's origin

- **WHEN** NotebookLM provides an answer to a user's question
- **THEN** the user SHALL be able to see which source document and passage the answer was derived from
