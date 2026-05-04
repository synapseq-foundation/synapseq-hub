## ADDED Requirements

### Requirement: Favorites category tab
The system SHALL display a "Favorites" category tab immediately after the "All" tab in the category badges section.

#### Scenario: Favorites tab is visible
- **WHEN** the category badges section is rendered
- **THEN** a "Favorites" tab is displayed as the second tab after "All"

#### Scenario: Favorites tab is selected
- **WHEN** the user selects the "Favorites" tab
- **THEN** the system filters the manifest audio entries by matching their `id` against the string array stored in `synapseq-hub:favorites`, and displays only matching entries (same filtering approach as other categories)

### Requirement: Favorites category empty state
The system SHALL display a friendly empty state message when the Favorites category is selected and no favorites exist.

#### Scenario: No favorites exist
- **WHEN** the user selects the "Favorites" tab and `synapseq-hub:favorites` is empty or does not exist
- **THEN** the system displays an empty state message indicating no favorites yet

### Requirement: Unfavorite removes item from Favorites category
The system SHALL immediately remove an audio entry from the Favorites category view when the user unfavorites it while in that category.

#### Scenario: Unfavorite in Favorites category
- **WHEN** the user is viewing the "Favorites" category and clicks the heart button to unfavorite an entry
- **THEN** that entry is removed from the current list view immediately
