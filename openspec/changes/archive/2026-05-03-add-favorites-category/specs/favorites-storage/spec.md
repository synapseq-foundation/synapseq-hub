## ADDED Requirements

### Requirement: Favorites localStorage persistence
The system SHALL persist favorite audio IDs in the `synapseq-hub:favorites` localStorage key as a JSON array of strings (no timestamps or additional metadata, replacing any previous `FavoriteRecord` structure).

#### Scenario: Favorites are saved
- **WHEN** the user favorites an audio entry
- **THEN** the audio ID (a string) is appended to the array stored in `synapseq-hub:favorites` and the JSON array is persisted to localStorage

#### Scenario: Favorites are removed
- **WHEN** the user unfavorites an audio entry
- **THEN** the audio ID is removed from the array stored in `synapseq-hub:favorites` and localStorage is updated

#### Scenario: Favorites are restored on load
- **WHEN** the app loads
- **THEN** the system reads the `synapseq-hub:favorites` key from localStorage and parses it as a string array; if the key does not exist, it initializes as an empty array

#### Scenario: No FavoriteRecord structure
- **WHEN** favorites are stored or read from localStorage
- **THEN** the data is a plain JSON array of strings (e.g., `["id-1", "id-2"]`) with no `FavoriteRecord` objects or timestamps

### Requirement: Unlimited favorites
The system SHALL allow users to favorite an unlimited number of audio entries.

#### Scenario: No favorite limit
- **WHEN** the user favorites more than five audio entries
- **THEN** all favorited entries are persisted and displayed in the Favorites category without any limit enforcement
