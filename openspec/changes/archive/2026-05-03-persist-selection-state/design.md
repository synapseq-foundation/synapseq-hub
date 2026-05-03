## Context

The SynapseQ Hub audio player currently resets user selections on page refresh. The main page (`+page.svelte`) uses Svelte 5 runes for state management with `selectedCategory` and `selectedAudioId` as `$state` variables. The app already has a pattern for localStorage persistence with the theme feature using `writeStorage` and `restoreTheme` functions.

## Goals / Non-Goals

**Goals:**
- Persist `selectedCategory` to localStorage as `synapseq-hub:category`
- Persist `selectedAudioId` to localStorage as `synapseq-hub:current`
- Restore both values on page load before rendering the UI
- Maintain consistency between the audio list selection and the player component

**Non-Goals:**
- No server-side persistence (browser localStorage only)
- No sync across tabs or devices
- No changes to the favorites persistence system (already exists)

## Decisions

### 1. Storage Keys
**Decision**: Use `synapseq-hub:category` and `synapseq-hub:current` as localStorage keys.

**Rationale**: Follows the existing naming convention used by `themeStorageKey`. Provides clear namespacing to avoid collisions.

**Alternatives considered**:
- Single object stored under one key (rejected: harder to debug, less aligned with existing pattern)

### 2. Restore Timing
**Decision**: Read from localStorage during `onMount` before loading the manifest, then apply stored values after manifest loads.

**Rationale**: The manifest must load first to validate that the stored category/audio ID still exists. If the stored audio no longer exists, fall back to defaults.

**Alternatives considered**:
- Restore after manifest load (chosen): Allows validation against actual data
- Restore before manifest load: Would require storing category/audio metadata to be useful

### 3. Persistence Trigger
**Decision**: Write to localStorage whenever `selectCategory` or `selectEntry` functions are called.

**Rationale**: Immediate persistence ensures state is saved even if user navigates away quickly. Follows existing `writeStorage` pattern used for theme.

**Alternatives considered**:
- Debounced writes (rejected: unnecessary complexity for this use case)
- Periodic sync (rejected: overkill for simple selection state)

## Risks / Trade-offs

- **[Stale Data]** → User may have stored category/audio that no longer exists in manifest. **Mitigation**: Validate against loaded manifest, fall back to defaults (`All` category, first audio) if invalid.
- **[localStorage Unavailable]** → Private browsing or storage full. **Mitigation**: Already handled by try/catch in existing `writeStorage` function.
- **[Favorites Category]** → `Favorites` is a virtual category not in the manifest. **Mitigation**: Allow `Favorites` as valid category even though it won't be in manifest categories list.
