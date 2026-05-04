## Context

The player route (`src/routes/+page.svelte`) currently wraps `<PlayerHeader>`, `<CategoryBadges>`, `<AudioList>`, and `<StatePanel>` inside a `<section>` with Tailwind classes that create a card-like surface: borders, rounded corners, shadows, and constrained `max-w`/`mx-auto`. The `<main>` element only provides page-level padding and min-height.

The user wants the main content area to feel like a full-page workspace, with the background and shell extending continuously behind the content, while keeping the fixed `<AudioPlayerBar>` unchanged at the bottom.

Additionally, they want the container to occupy the entire horizontal space without lateral margins or width constraints, and completely without borders, rounded corners, shadows, or backdrop blur.

## Goals / Non-Goals

**Goals:**

- Remove the inner `<section>` wrapper from `+page.svelte` so the header, categories, and list sit directly inside `<main>`.
- Move layout, padding, and background responsibilities fully onto the `<main>` element so the page feels like one continuous surface.
- Eliminate all horizontal constraints: remove `mx-auto` and `w-[min(100%,920px)]` so the container occupies the full page width.
- Eliminate borders, rounded corners, shadows, and backdrop blur from the main content container so it blends with the page background.
- Keep the fixed `<AudioPlayerBar>` and its positioning completely unchanged.
- Preserve all existing behavior: manifest loading, category filtering, artwork fallback, favorites, theme switching, selection, and Play control.

**Non-Goals:**

- No changes to extracted components: `PlayerHeader`, `CategoryBadges`, `AudioList`, `AudioDetails`, `StatePanel`.
- No changes to `src/routes/layout.css`, theme tokens, local storage keys, or static assets.
- No changes to the fixed player bar or its positioning.
- No redesign of the player UI, typography, or color usage.

## Decisions

### Remove the inner `<section>` wrapper

Move the `class` currently on the `<section>` directly onto the `<main>` element in `+page.svelte`.

Specifically, migrate these classes from `<section>` to `<main>`:
- `overflow-hidden`
- `border border-[var(--line)]`
- `bg-[var(--panel)]`
- `shadow-[var(--shadow)]`
- `backdrop-blur-xl`
- `rounded-[26px] sm:rounded-[32px]`
- `aria-labelledby="player-title"`

Then remove `mx-auto`, `min-h-screen`, and `w-[min(100%,920px)]` so the main container occupies the full horizontal space.

**Alternative considered:** Keep the `<section>` and only remove its visual classes. That still leaves an unnecessary wrapper element in the DOM and does not achieve the “full-page” feeling the user wants.

### Adjust `<main>` padding and bottom spacing

Update the `<main>` utility classes to:
- Remove `mx-auto` and `w-[min(100%,920px)]` to use the full page width.
- Preserve responsive horizontal padding: `px-2.5 sm:px-4`
- Adjust top padding to something comfortable without the card chrome: `pt-3 sm:pt-[22px]`
- Adjust bottom padding to account for the fixed player: `pb-32 sm:pb-[136px]`

**Alternative considered:** Keep the current `<main>` padding unchanged and only remove the `<section>`. That would work visually, but clarifying intent by simplifying the main container leads to a cleaner layout model.

### Keep fixed player positioning unchanged

Do not modify `<AudioPlayerBar>` or its wrapper/parent. The player must remain `fixed`, aligned to the bottom, and styled exactly as it is today.

**Alternative considered:** Move player-related layout responsibilities into the `<main>` element. That would couple the player positioning with the main content and break the explicit fixed-player behavior.

## Risks / Trade-offs

- Visual regression if any `<section>`-specific responsive or state styles were relied upon indirectly → mitigate by preserving all used classes on `<main>` and validating with build/check.
- Bottom padding (`pb-32 sm:pb-[136px]`) may need微调 if the fixed player height changes later → mitigate by keeping the player component unchanged and only adjusting page-level padding.
