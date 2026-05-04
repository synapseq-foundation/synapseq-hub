## Why

The audio player currently has a disabled Play button with no actual audio playback functionality. Users need working real-time audio playback with proper progress visualization, Media Session API integration for system media controls, and a lock mechanism to prevent accidental audio selection changes during playback.

## What Changes

- Add HTML5 `<audio>` element for MP3 playback using the URL pattern `https://audio.synapseq.org/hub/{id}.mp3`
- Integrate Media Session API (`navigator.mediaSession`) to provide system-level media controls and metadata
- Implement Play/Stop toggle button using Lucide icons (Play icon when idle, Stop icon when playing)
- Add player lock mechanism that prevents audio selection from the list while playback is active
- Create a progress bar where the category background color fill is consumed as audio advances, rather than a traditional progress bar
- Modify category color behavior: when playback starts, the background fill transitions from full category color to being consumed progressively until playback ends

## Capabilities

### New Capabilities
<!-- None - all changes are to the existing audio-player capability -->

### Modified Capabilities
- `audio-player`: Adding actual audio playback with HTML5 audio, Media Session API integration, Play/Stop toggle, player lock mechanism during playback, and category-color-based progress visualization

## Impact

- **AudioPlayerBar.svelte**: Major changes to add audio element, playback logic, progress tracking, and lock state
- **+page.svelte**: Add playback state management, Media Session API setup, and player lock coordination
- **AudioList.svelte**: Add lock state awareness to prevent selection during playback
- **Dependencies**: Lucide icons (already installed), HTML5 audio API, Media Session API
- **Audio source**: MP3 files served from `https://audio.synapseq.org/hub/{id}.mp3`
