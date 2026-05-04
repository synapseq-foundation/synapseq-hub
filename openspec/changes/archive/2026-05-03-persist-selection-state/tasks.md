## 1. Add Storage Keys

- [x] 1.1 Add `categoryStorageKey` and `currentAudioStorageKey` constants to `$lib/player/constants.ts` with values `synapseq-hub:category` and `synapseq-hub:current`

## 2. Persist Category Selection

- [x] 2.1 Modify `selectCategory` function in `+page.svelte` to call `writeStorage(categoryStorageKey, category)` when category changes
- [x] 2.2 Ensure `Favorites` category is also persisted when selected

## 3. Persist Audio Selection

- [x] 3.1 Modify `selectEntry` function in `+page.svelte` to call `writeStorage(currentAudioStorageKey, entry.id)` when audio changes

## 4. Restore State on Page Load

- [x] 4.1 Add `restoreSelectionState` function in `+page.svelte` that reads from localStorage and validates against manifest
- [x] 4.2 In `restoreSelectionState`, read `synapseq-hub:category` and validate it exists in categories list (or is `All`/`Favorites`), else default to `All`
- [x] 4.3 In `restoreSelectionState`, read `synapseq-hub:current` and validate it exists in entries list, else default to first entry
- [x] 4.4 Call `restoreSelectionState` in `onMount` after `loadManifest` completes successfully

## 5. Verify Integration (Manual Testing)

- [ ] 5.1 Test that selecting a category and refreshing the page restores the correct category
- [ ] 5.2 Test that selecting an audio and refreshing the page restores the correct audio in both list and player
- [ ] 5.3 Test that invalid stored values (deleted category/audio) fall back to defaults
- [ ] 5.4 Test that localStorage errors are handled silently (no console errors)
