## 1. Category Theme Configuration

- [x] 1.1 Create `src/lib/category-themes.ts` with category-to-Tailwind-class mapping
- [x] 1.2 Define Tailwind background classes: Focus (`bg-teal-500`), Relaxation (`bg-amber-500`), Meditation (`bg-neutral-500`), All (current default class)
- [x] 1.3 Export TypeScript types for category theme mapping
- [x] 1.4 Add custom color values via Tailwind CSS-first config (`@theme`) if default palette needs adjustment (N/A: default palette sufficient)

## 2. Theme Application Infrastructure

- [x] 2.1 Export reactive category class string from theme config for use in Svelte components
- [x] 2.2 Use Svelte reactive class binding (`class:bg-teal-500={$category === 'focus'}`) or computed class string
- [x] 2.3 Add Tailwind transition utilities (`transition-colors duration-300 ease-in-out`) to themed elements

## 3. List Component Updates

- [x] 3.1 Apply category theme class to List component container background via reactive binding
- [x] 3.2 Apply category theme class to List component card backgrounds
- [x] 3.3 Add `transition-colors duration-300 ease-in-out` for smooth transitions

## 4. Player Component Updates

- [x] 4.1 Apply category theme class to Player component card background via reactive binding
- [x] 4.2 Add `transition-colors duration-300 ease-in-out` for smooth transitions
- [x] 4.3 Verify Player component maintains readability with new background colors

## 5. Integration and Testing

- [x] 5.1 Connect category state management to theme class application in components
- [ ] 5.2 Test category switching: Focus → `bg-teal-500` applied
- [ ] 5.3 Test category switching: Relaxation → `bg-amber-500` applied
- [ ] 5.4 Test category switching: Meditation → `bg-neutral-500` applied
- [ ] 5.5 Test "All" category preserves default background class
- [ ] 5.6 Verify smooth `transition-colors` transitions between all category combinations
