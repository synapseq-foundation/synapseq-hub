## MODIFIED Requirements

### Requirement: Favorite persistence and ordering
The system SHALL allow users to favorite audio entries without limit, persist favorites in `synapseq-hub:favorites` localStorage key, and display favorited entries in the dedicated "Favorites" category tab instead of moving them to the top of the current list.

#### Scenario: Entry is favorited
- **WHEN** the user clicks the heart button for an audio entry that is not currently favorited
- **THEN** the entry ID is added to the `synapseq-hub:favorites` array in localStorage
- **AND** the favorites array is persisted to localStorage

#### Scenario: Entry is unfavorited
- **WHEN** the user clicks the heart button for an audio entry that is already favorited
- **THEN** the entry ID is removed from the `synapseq-hub:favorites` array in localStorage
- **AND** localStorage is updated to reflect the removal

#### Scenario: Favorites are displayed in Favorites category
- **WHEN** the user selects the "Favorites" category tab
- **THEN** the system filters the manifest entries by matching each entry's `id` against the string array in `synapseq-hub:favorites`, and renders the matching entries

#### Scenario: No list-top movement on favorite
- **WHEN** the user favorites an audio entry while viewing any category other than "Favorites"
- **THEN** the entry remains in its current position in the list and is not moved to the top

#### Scenario: No favorite limit
- **WHEN** the user favorites audio entries
- **THEN** there is no limit on the number of favorites that can be stored

## REMOVED Requirements

### Requirement: Favorite limit is reached
**Reason**: The 5-item favorite limit is removed now that favorites have a dedicated category with unlimited storage.
**Migration**: Remove the limit check; all favorite toggles now add to the `synapseq-hub:favorites` array without cap.

### Requirement: Favorites are ordered at the top
**Reason**: Favorited items no longer move to the top of the current list; they are shown in the dedicated Favorites category.
**Migration**: Remove the ordering logic that sorts favorited entries to the top of the audio list.
