## Context

The app currently has a category system with "All" as the default. Favorites are tracked with a 5-item limit and favorited items move to the top of the current audio list. Favorites data is not persisted in a dedicated localStorage key. The new design introduces a dedicated "Favorites" category tab and unlimited favorites stored in `synapseq-hub:favorites` in localStorage.

## Goals / Non-Goals

**Goals:**
- Add a "Favorites" category tab next to "All" in the category list.
- Persist favorite audio IDs in `synapseq-hub:favorites` localStorage key as an array of strings.
- Remove the 5-item limit on favorites.
- Change favorite toggle behavior: favoriting adds the item to the favorites list (no list-top movement).
- In the Favorites category, unfavoriting removes the item from the view immediately.

**Non-Goals:**
- Syncing favorites across devices or accounts.
- Server-side persistence of favorites.
- Changing the audio player or audio data fetching logic beyond favorites.

## Decisions

1. **localStorage key `synapseq-hub:favorites`**
   - Rationale: Simple, client-side persistence with no backend needed.
   - Alternatives considered: IndexedDB (overkill for a simple array of IDs), in-memory state (lost on refresh).

2. **Favorites stored as array of audio IDs (strings)**
   - Rationale: Minimal data footprint; audio details are already available from the existing audio data source.
   - Alternatives considered: Storing full audio objects (duplication, stale data risk).

3. **"Favorites" category tab position**
   - Rationale: Placed immediately after "All" for visibility and logical grouping.
   - Alternatives considered: At the end of category list (less discoverable).

4. **Remove list-top movement on favorite**
   - Rationale: The new Favorites category is the dedicated place for favorited items; moving items in the current list is confusing.
   - Alternatives considered: Keep both behaviors (redundant and cluttered).

## Risks / Trade-offs

- [localStorage size limit] → Mitigation: Audio IDs are small strings; unlikely to hit the ~5MB limit with typical usage.
- [User clears localStorage] → Mitigation: Data loss is acceptable for a client-side only feature; no migration needed.
- [Favorites category empty state] → Mitigation: Show a friendly empty state message when no favorites exist.
