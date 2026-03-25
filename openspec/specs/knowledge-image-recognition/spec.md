# knowledge-image-recognition Specification

## Purpose

Enables the sync script to detect image blocks in Notion pages, download and compress them in memory, and recognize their content via Claude Vision API. Recognition results are appended to the page block content for use in summarization and categorization.

## Requirements

### Requirement: Image block detection in Notion pages

The sync script SHALL detect image-type blocks within Notion page block lists and process only manually uploaded images (Notion-hosted). Externally referenced images (from web clipping) SHALL be skipped to avoid unnecessary API costs.

#### Scenario: Page contains a manually uploaded image (file type)

- **WHEN** `get_page_blocks()` encounters an image block with a Notion-hosted URL (`file` type)
- **THEN** it SHALL extract the image URL and pass it to the image recognition pipeline

#### Scenario: Page contains an externally referenced image (external type)

- **WHEN** `get_page_blocks()` encounters an image block with an external URL (`external` type)
- **THEN** it SHALL skip recognition and render the block as `[圖片]` without calling the Claude Vision API

#### Scenario: Page contains no image blocks

- **WHEN** no image-type blocks are found in the page
- **THEN** the function SHALL return only the text content without any image-related processing

### Requirement: Image download and compression

The sync script SHALL download the image from the Notion-provided URL and compress it in memory before recognition.

#### Scenario: Successful image download and compression

- **WHEN** an image URL is valid and accessible
- **THEN** the script SHALL download the image, resize it to a maximum of 1024px on the longest side, compress it to JPEG quality 70 in memory, and proceed to recognition

#### Scenario: Image download fails

- **WHEN** the image URL is unreachable or returns an error
- **THEN** the script SHALL log a warning with the page title and image URL, skip that image, and continue processing remaining blocks

### Requirement: Image recognition via Claude Vision API

The sync script SHALL send the compressed image to the Claude Vision API and retrieve a text description of the image content.

#### Scenario: Successful image recognition

- **WHEN** the compressed image is sent to Claude Vision API
- **THEN** the API SHALL return a text description, and the script SHALL append it to the block content in the format `[圖片內容：<description>]`

#### Scenario: Image recognition fails

- **WHEN** the Claude Vision API call fails (e.g., timeout, API error)
- **THEN** the script SHALL log a warning and skip that image without aborting the sync

### Requirement: Image recognition failure resilience

If image recognition fails for any individual image, the script SHALL log the failure and continue processing remaining blocks and entries without aborting the sync.

#### Scenario: Recognition fails for one image in a page

- **WHEN** recognition fails for one image block
- **THEN** the script SHALL log the error, omit that image's content from the result, and proceed with remaining blocks
