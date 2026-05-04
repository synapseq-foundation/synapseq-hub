## ADDED Requirements

### Requirement: Persist selected category to localStorage
The system SHALL store the user's selected category in localStorage under the key `synapseq-hub:category` whenever the selection changes.

#### Scenario: Category selection is persisted
- **WHEN** user selects a category (including `All`, `Favorites`, or any manifest category)
- **THEN** the system SHALL write the category name to localStorage with key `synapseq-hub:category`

#### Scenario: Category persistence handles storage errors
- **WHEN** localStorage write fails (private browsing, quota exceeded)
- **THEN** the system SHALL catch the error silently and continue operating with in-memory state

### Requirement: Persist selected audio to localStorage
The system SHALL store the user's selected audio ID in localStorage under the key `synapseq-hub:current` whenever the selection changes.

#### Scenario: Audio selection is persisted
- **WHEN** user selects an audio entry from the list
- **THEN** the system SHALL write the audio ID to localStorage with key `synapseq-hub:current`

#### Scenario: Audio persistence handles storage errors
- **WHEN** localStorage write fails (private browsing, quota exceeded)
- **THEN** the system SHALL catch the error silently and continue operating with in-memory state

### Requirement: Restore category on page load
The system SHALL restore the previously selected category from localStorage when the page loads.

#### Scenario: Valid stored category is restored
- **WHEN** page loads and localStorage contains a valid `synapseq-hub:category` value that exists in the current manifest categories (or is `All` or `Favorites`)
- **THEN** the system SHALL set `selectedCategory` to the stored value

#### Scenario: Stored category is invalid
- **WHEN** page loads and localStorage contains a `synapseq-hub:category` value that does not exist in the current manifest categories (and is not `All` or `Favorites`)
- **THEN** the system SHALL set `selectedCategory` to `All`

#### Scenario: No stored category exists
- **WHEN** page loads and localStorage does not contain `synapseq-hub:category`
- **THEN** the system SHALL set `selectedCategory` to `All`

### Requirement: Restore audio selection on page load
The system SHALL restore the previously selected audio from localStorage when the page loads.

#### Scenario: Valid stored audio is restored
- **WHEN** page loads and localStorage contains a valid `synapseq-hub:current` value that exists in the loaded manifest entries
- **THEN** the system SHALL set `selectedAudioId` to the stored value, making it selected in the list and loaded in the player component

#### Scenario: Stored audio is invalid
- **WHEN** page loads and localStorage contains a `synapseq-hub:current` value that does not exist in the loaded manifest entries
- **THEN** the system SHALL set `selectedAudioId` to the first entry in the manifest (or `null` if manifest is empty)

#### Scenario: No stored audio exists
- **WHEN** page loads and localStorage does not contain `synapseq-hub:current`
- **THEN** the system SHALL set `selectedAudioId` to the first entry in the manifest (or `null` if manifest is empty)
