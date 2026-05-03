## Requirements

### Requirement: Manifest-driven audio catalog
The system SHALL load the audio catalog from `/manifest.json` and render entries from the manifest `entries` array on the main route.

#### Scenario: Catalog loads from root manifest
- **WHEN** the main route is opened
- **THEN** the system fetches `/manifest.json` without adding a base URL
- **AND** renders available audio entries using each entry's `id`, `name`, `author`, `path`, `category`, `download_url`, and `updated_at` fields where needed

#### Scenario: Manifest cannot be loaded
- **WHEN** fetching or parsing `/manifest.json` fails
- **THEN** the system shows a non-crashing empty or error state on the main route

### Requirement: SynapSeq player layout
The system SHALL present the main route as a player layout composed of header, categories, list, and fixed bottom player sections.

#### Scenario: Header is displayed
- **WHEN** the main route renders
- **THEN** the header displays `/artwork/default.webp` as the logo, the text `Hub Player`, and a light/dark theme toggle button aligned horizontally

#### Scenario: Fixed player is displayed
- **WHEN** an audio entry is selected
- **THEN** the player remains fixed at the bottom of the viewport and displays the selected audio details with a Play button aligned on the right

### Requirement: Artwork resolution with fallback
The system SHALL use `/artwork/{id}.webp` for audio artwork and fall back to `/artwork/default.webp` when the entry-specific artwork cannot be loaded.

#### Scenario: Entry artwork exists
- **WHEN** an audio entry with ID `calm-state` is rendered
- **THEN** its artwork image source is `/artwork/calm-state.webp`

#### Scenario: Entry artwork is missing
- **WHEN** an entry-specific artwork request fails
- **THEN** the system displays `/artwork/default.webp` for that artwork image

### Requirement: Category badges filter audio entries
The system SHALL derive category badges from the manifest entry `category` values and display them in a horizontally scrollable category section.

#### Scenario: Categories are generated from manifest data
- **WHEN** the manifest contains entries from `Relaxation`, `Meditation`, and `Focus`
- **THEN** the categories section displays those categories as selectable badges

#### Scenario: Category is selected
- **WHEN** the user selects a category badge
- **THEN** the list displays audio entries matching that category

### Requirement: Audio list selection
The system SHALL render audio rows with details and a favorite button, and one tap on a row SHALL select that audio entry for the fixed player.

#### Scenario: Audio row details are displayed
- **WHEN** an audio entry is rendered in the list
- **THEN** the row displays its artwork, title from `name`, author from `author`, and a heart favorite button aligned horizontally

#### Scenario: Audio row is tapped
- **WHEN** the user taps an audio row once
- **THEN** that audio entry becomes the selected item displayed in the bottom player

### Requirement: Favorite persistence and ordering
The system SHALL allow users to favorite up to five audio entries, persist favorites in local storage, and order favorited entries above non-favorites by favorite timestamp.

#### Scenario: Entry is favorited
- **WHEN** the user clicks the heart button for an audio entry that is not currently favorited
- **THEN** the entry is added to favorites with the current favorite timestamp
- **AND** favorites are persisted to local storage

#### Scenario: Entry is unfavorited
- **WHEN** the user clicks the heart button for an audio entry that is already favorited
- **THEN** the entry is removed from favorites
- **AND** local storage is updated to reflect the removal

#### Scenario: Favorites are ordered at the top
- **WHEN** the list is rendered with favorited and non-favorited entries
- **THEN** favorited entries appear before non-favorited entries
- **AND** favorited entries are ordered by most recent favorite timestamp first

#### Scenario: Favorite limit is reached
- **WHEN** the user already has five favorites and clicks the heart button for a non-favorited entry
- **THEN** the system does not add a sixth favorite
- **AND** the existing local storage favorite set remains valid

### Requirement: Theme switching
The system SHALL support light and dark themes using the provided SynapSeq CSS color tokens and persist the selected theme locally.

#### Scenario: Theme is toggled
- **WHEN** the user clicks the theme toggle button
- **THEN** the system switches between light and dark themes by applying the corresponding document theme state

#### Scenario: Theme preference is restored
- **WHEN** the user returns to the app after selecting a theme
- **THEN** the previously selected theme is restored from local storage

### Requirement: Play control
The system SHALL include a Play button in the fixed player for the selected audio entry.

#### Scenario: Play button is shown for selected audio
- **WHEN** an audio entry is selected
- **THEN** the bottom player displays a Play button using an icon from `@lucide/svelte`

#### Scenario: No selected audio yet
- **WHEN** the manifest has loaded and the user has not manually selected an audio entry
- **THEN** the system has a deterministic selected entry or an explicit empty player state that does not crash
