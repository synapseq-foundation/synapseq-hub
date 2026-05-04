## Why

Currently, when users refresh the SynapseQ Hub page, they lose their selection state - the selected category and audio are reset to defaults. This creates a poor user experience as users must re-navigate to their previously selected content after every page reload.

## What Changes

- Add localStorage persistence for `synapseq-hub:category` to store the last selected category
- Add localStorage persistence for `synapseq-hub:current` to store the last selected audio
- On page load, restore the previously selected category and mark it as active
- On page load, restore the previously selected audio and set it as selected in the list and loaded in the player component
- Implement initialization logic to read from localStorage before rendering the UI

## Capabilities

### New Capabilities
- `selection-persistence`: Manages localStorage persistence of user selection state (category and audio) with restore functionality on page load

### Modified Capabilities

## Impact

- **Components**: Category selector, audio list, audio player component
- **State Management**: Initialization logic to read from localStorage on app start
- **Storage**: Uses browser localStorage API (no new dependencies)
- **User Experience**: Selections now persist across page refreshes
