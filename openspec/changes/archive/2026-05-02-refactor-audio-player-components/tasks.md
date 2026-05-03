## 1. Shared Player Modules

- [x] 1.1 Create shared audio player type definitions for `Theme`, `AudioEntry`, `Manifest`, and `FavoriteRecord` under `src/lib/player/`.
- [x] 1.2 Move shared constants such as `defaultArtwork`, storage keys, and `maxFavorites` into an importable player module.
- [x] 1.3 Update `src/routes/+page.svelte` to import shared types/constants instead of defining them inline.

## 2. Component Extraction

- [x] 2.1 Create `src/lib/components/player/AudioDetails.svelte` with artwork fallback, title, author rendering, and Tailwind utility classes.
- [x] 2.2 Create `src/lib/components/player/PlayerHeader.svelte` with logo, title, theme toggle props, and Tailwind utility classes.
- [x] 2.3 Create `src/lib/components/player/CategoryBadges.svelte` with typed category props, selected category, selection callback, and Tailwind utility classes.
- [x] 2.4 Create `src/lib/components/player/AudioList.svelte` with rows, selected state, favorite state, selection callback, favorite callback, and Tailwind utility classes.
- [x] 2.5 Create `src/lib/components/player/AudioPlayerBar.svelte` with selected audio details, Play button, play message, play callback, and Tailwind utility classes.
- [x] 2.6 Create `src/lib/components/player/StatePanel.svelte` with Tailwind utility classes if it keeps route markup simpler for loading, error, and empty states.

## 3. Route Composition

- [x] 3.1 Replace inline header markup in `+page.svelte` with `PlayerHeader`.
- [x] 3.2 Replace inline category markup in `+page.svelte` with `CategoryBadges`.
- [x] 3.3 Replace inline audio list markup and reusable snippet in `+page.svelte` with `AudioList` and `AudioDetails` usage.
- [x] 3.4 Replace inline fixed player markup in `+page.svelte` with `AudioPlayerBar`.
- [x] 3.5 Keep manifest loading, derived lists, selected audio, favorites, theme, and local storage logic in `+page.svelte`.

## 4. Tailwind Styles And Behavior Preservation

- [x] 4.1 Convert component-specific styling to Tailwind utilities while preserving the current visual output.
- [x] 4.2 Use token-backed Tailwind arbitrary values such as `bg-[var(--panel-strong)]`, `text-[var(--muted)]`, `border-[var(--line)]`, and `shadow-[var(--shadow)]` where needed.
- [x] 4.3 Keep global body background, shell layout, CSS tokens, and any unavoidable global CSS in the route or layout styles.
- [x] 4.4 Remove pure component CSS that is replaced by Tailwind utilities.
- [x] 4.5 Verify row selection and favorite button interactions remain separate clickable controls.
- [x] 4.6 Verify artwork fallback remains shared between list details and player details.

## 5. Verification

- [x] 5.1 Run `npx @sveltejs/mcp svelte-autofixer` for each new or changed `.svelte` component and apply required fixes.
- [x] 5.2 Run `npm run check` and fix Svelte or TypeScript issues.
- [x] 5.3 Run `npm run build` and verify the static app builds successfully.
- [x] 5.4 Manually verify manifest loading, category filtering, artwork fallback, theme switching, favorite ordering and limit, row selection, and the Play control after component extraction.
