## Why

The current favorites feature limits users to 5 favorited items and moves favorited audio to the top of the current list, which is unintuitive. Users need a dedicated, unlimited favorites space to easily access all their favorited audio, with data persisted in localStorage.

## What Changes

- Add a new "Favorites" category tab positioned next to the "All" category tab.
- Remove the existing 5-item limit on favorited audio.
- Update favorite toggle behavior: favoriting an item no longer moves it to the top of the list, instead it is added to the "Favorites" category dataset.
- Fetch favorites data from the `synapseq-hub:favorites` key in localStorage.
- In the "Favorites" category, unfavoriting an item immediately removes it from the category view.
- **BREAKING**: Remove previous favorite list-top movement behavior and 5-item limit.

## Capabilities

### New Capabilities
- `favorites-category`: Manages the new "Favorites" category tab, renders favorited audio items from localStorage, and handles item removal on unfavorite.
- `favorites-storage`: Handles reading from and writing to the `synapseq-hub:favorites` localStorage key for favorite audio items.

### Modified Capabilities
- `audio-player`: Updates favorite toggle logic to align with new category-based behavior, removing top-list movement and 5-item limit.

## Impact

- Category list UI component (add "Favorites" tab)
- Audio list component (update favorite toggle handler, render favorites category)
- LocalStorage interactions (new `synapseq-hub:favorites` key management)
- Removal of legacy favorite limit and list-top movement logic
