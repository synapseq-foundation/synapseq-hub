## 1. Audio Playback State and Logic in +page.svelte

- [x] 1.1 Add `isPlaying` state variable using `$state` (boolean, defaults to `false`)
- [x] 1.2 Add `playerLocked` state variable using `$state` (boolean, defaults to `false`)
- [x] 1.3 Add `playbackProgress` state variable using `$state` (number 0-100, defaults to `0`)
- [x] 1.4 Add `audioElement` variable (not reactive, holds the `Audio` instance, initially `null`)
- [x] 1.5 Create `startPlayback()` function that: creates `new Audio('https://audio.synapseq.org/hub/{id}.mp3')`, sets up `timeupdate` event to update `playbackProgress`, sets up `ended` event to call `stopPlayback()`, calls `audio.play()`, sets `isPlaying = true` and `playerLocked = true`
- [x] 1.6 Create `stopPlayback()` function that: calls `audio.pause()` and `audio.currentTime = 0`, removes event listeners, sets `audioElement = null`, sets `isPlaying = false`, `playerLocked = false`, `playbackProgress = 0`
- [x] 1.7 Create `togglePlayback()` function that calls `startPlayback()` if not playing, or `stopPlayback()` if playing
- [x] 1.8 Set up Media Session API metadata and action handlers inside `startPlayback()` when `navigator.mediaSession` is available
- [x] 1.9 Pass `isPlaying`, `playbackProgress`, `playerLocked`, and `togglePlayback` as props to `AudioPlayerBar`

## 2. Update AudioPlayerBar.svelte

- [x] 2.1 Add `isPlaying`, `progress`, `locked`, and `onToggle` props to the Props type
- [x] 2.2 Replace `handlePlay()` function with a call to `onToggle()` prop
- [x] 2.3 Import `Square` from `@lucide/svelte` for the Stop icon
- [x] 2.4 Update the button to conditionally render `Play` icon when `!isPlaying` and `Square` icon when `isPlaying`
- [x] 2.5 Update button text to show "Play" when `!isPlaying` and "Stop" when `isPlaying`
- [x] 2.6 Add progress bar overlay div inside the footer: an absolutely positioned div with `categoryBgClass`, width set to `{progress}%`, and `transition: width 0.3s linear`
- [x] 2.7 Conditionally apply `bg-transparent` to the footer when `isPlaying` is true (to allow the progress overlay to be visible), otherwise apply `categoryBgClass`
- [x] 2.8 Add `relative overflow-hidden` classes to the footer for proper progress bar positioning
- [x] 2.9 Ensure the button and AudioDetails content have `relative z-10` or similar to appear above the progress overlay

## 3. Update AudioList.svelte for Player Lock

- [x] 3.1 Add `locked` prop to the Props type (boolean, defaults to `false`)
- [x] 3.2 Modify the `onclick` handler on the entry button to check `if (locked) return;` before calling `onSelectEntry(entry)`
- [x] 3.3 Pass `playerLocked` as `locked` prop from `+page.svelte` to `AudioList`

## 4. Wire Up Components in +page.svelte

- [x] 4.1 Update `AudioPlayerBar` usage to pass `isPlaying`, `playbackProgress`, `onToggle={togglePlayback}`, and remove the old `onPlay={playSelected}` prop
- [x] 4.2 Update `AudioList` usage to pass `locked={playerLocked}`
- [x] 4.3 Remove or repurpose the `playSelected()` function since playback is now handled directly
- [x] 4.4 Remove the `AudioPlaybackModal` usage if no longer needed, or keep if still used for audio details

## 5. Media Session API Integration

- [x] 5.1 Inside `startPlayback()`, check if `'mediaSession' in navigator`
- [x] 5.2 Set `navigator.mediaSession.metadata` with `title`, `artist`, `album: 'SynapSeq Hub'`, and `artwork` array pointing to `/artwork/{id}.webp`
- [x] 5.3 Register `navigator.mediaSession.setActionHandler('play', () => startPlayback())`
- [x] 5.4 Register `navigator.mediaSession.setActionHandler('pause', () => stopPlayback())`
- [x] 5.5 Register `navigator.mediaSession.setActionHandler('stop', () => stopPlayback())`
- [x] 5.6 Clear Media Session metadata in `stopPlayback()` by setting `navigator.mediaSession.metadata = null` (with availability check)
