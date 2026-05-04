## Why

Implement an audio playback modal to provide users with detailed audio information and controls before starting playback. This enhances user experience by showing artwork, description, and warnings in a dedicated modal interface.

## What Changes

- Create a new audio playback modal component triggered by the "Play" button
- Modal displays audio artwork, author information, and description
- Fetch and parse audio description from spsq files (JSON format at "/" + path)
- Parse description by capturing lines starting with "##", removing the prefix, and trimming
- Implement collapsible text component for descriptions exceeding 3 lines
- Display listening warnings in English
- Add modal footer with Cancel and PLAY! buttons
- Style modal using Tailwind CSS
- PLAY! button currently only closes modal (play logic to be implemented later)

## Capabilities

### New Capabilities
- `audio-playback-modal`: Modal component for displaying audio information with artwork, description parsing from spsq files, collapsible text, and playback controls

### Modified Capabilities

## Impact

- New Svelte component for the modal
- New utility for parsing spsq file descriptions
- Integration with existing audio list/play button
- Tailwind CSS styling for modal layout
- No changes to existing audio playback logic (deferred to future implementation)
