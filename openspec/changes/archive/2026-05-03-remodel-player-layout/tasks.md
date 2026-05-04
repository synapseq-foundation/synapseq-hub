## 1. Layout Remodel:

- [x] 1.1 Remove the `<section>` wrapper and its classes from `src/routes/+page.svelte`.
- [x] 1.2 Move the removed classes (`overflow-hidden`, `border border-[var(--line)]`, `bg-[var(--panel)]`, `shadow-[var(--shadow)]`, `backdrop-blur-xl`, `rounded-[26px]` `sm:rounded-[32px]`, `aria-labelledby="player-title"`) directly onto the `<main>` element in `+page.svelte`.
- [x] 1.3 Remove `mx-auto`, `min-h-screen`, and `w-[min(100%,920px)]` from `<main>` so the container occupies the full page width without lateral margins or width constraints.
- [x] 1.4 Keep `<AudioPlayerBar>` and its positioning completely unchanged.

## 2. Verification:

- [x] 2.1 Run `npx @sveltejs/mcp svelte-autofixer ./src/routes/+page.svelte --svelte-version 5` and apply required fixes.
- [x] 2.2 Run `npm run check` and fix Svelte or TypeScript issues.
- [x] 2.3 Run `npm run build` and verify the static app builds successfully.
- [ ] 2.4 Manually verify the page background feels continuous, the player bar remains fixed, and behavior stays unchanged after the layout change.
