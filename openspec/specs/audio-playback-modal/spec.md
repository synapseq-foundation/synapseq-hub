### Requirement: Modal opens on Play button click
The system SHALL open the audio playback modal when the user clicks the "Play" button on an audio item.

#### Scenario: User clicks Play button
- **WHEN** user clicks the "Play" button on an audio item
- **THEN** the audio playback modal SHALL open displaying that audio's information

### Requirement: Modal displays close button
The modal SHALL display a close icon in the top-left corner that dismisses the modal.

#### Scenario: User clicks close button
- **WHEN** user clicks the close icon in the top-left corner of the modal
- **THEN** the modal SHALL close and cancel the playback flow

### Requirement: Modal displays audio artwork
The modal SHALL display the audio's artwork in the center area of the modal.

#### Scenario: Artwork displayed
- **WHEN** the modal is open
- **THEN** the audio artwork SHALL be displayed in the center area

### Requirement: Modal displays author information
The modal SHALL display the audio author formatted as "created by {author}" using a small font.

#### Scenario: Author displayed with correct format
- **WHEN** the modal is open
- **THEN** the author information SHALL be displayed as "created by {author}" in a small font below the artwork

### Requirement: Modal parses and displays audio description from spsq file
The system SHALL fetch the spsq file as text from "/" + audio path, extract lines starting with "##", remove the "##" prefix, trim each line, and display the description.

#### Scenario: Description parsed and displayed
- **WHEN** the modal opens for an audio item
- **THEN** the system SHALL fetch the spsq file from "/" + audio path as text
- **AND** extract all lines starting with "##" from the content
- **AND** remove the "##" prefix from each line
- **AND** trim each line
- **AND** preserve empty lines (lines with only "##" become empty strings representing newlines)
- **AND** display the parsed description below the author information

### Requirement: Description supports collapsible text
The description SHALL be displayed in a collapsible text component that shows an "Expand" option when the content exceeds 3 lines.

#### Scenario: Long description shows expand option
- **WHEN** the parsed description exceeds 3 lines
- **THEN** the system SHALL show an "Expand" button to reveal the full text

#### Scenario: Short description displays fully
- **WHEN** the parsed description is 3 lines or fewer
- **THEN** the system SHALL display the full description without a collapse/expand option

#### Scenario: User expands description
- **WHEN** user clicks the "Expand" button on a collapsed description
- **THEN** the full description SHALL be displayed
- **AND** the button SHALL change to "Collapse"

### Requirement: Modal displays listening warnings
The modal SHALL display the following listening warnings in English:
- "Listen in a calm environment without interruptions."
- "Focus on your breathing and try not to think about random things."
- "Enjoy the experience!"

#### Scenario: Warnings displayed
- **WHEN** the modal is open
- **THEN** the three listening warnings SHALL be displayed in English below the description

### Requirement: Modal footer has Cancel and PLAY! buttons
The modal footer SHALL contain two buttons: "Cancel" and "PLAY!".

#### Scenario: Footer buttons present
- **WHEN** the modal is open
- **THEN** the footer SHALL display "Cancel" and "PLAY!" buttons

#### Scenario: Cancel button closes modal
- **WHEN** user clicks the "Cancel" button
- **THEN** the modal SHALL close (same behavior as close icon)

#### Scenario: PLAY! button closes modal
- **WHEN** user clicks the "PLAY!" button
- **THEN** the modal SHALL close
- **AND** no audio playback SHALL start (playback logic deferred to future implementation)

### Requirement: Modal styled with Tailwind CSS and SynapSeq palette
The modal SHALL be styled using Tailwind CSS utility classes and follow the SynapSeq color palette.

#### Scenario: Tailwind styling applied
- **WHEN** the modal is rendered
- **THEN** all styling SHALL use Tailwind CSS classes and SynapSeq palette tokens (--panel, --text, --accent, etc.)
