## Context

The application has audio categories (All, Focus, Meditation, Relaxation) that currently don't visually differentiate themselves. The List and Player components use static background colors. We need a theming system that dynamically changes colors based on the selected category with smooth transitions.

## Goals / Non-Goals

**Goals:**
- Create a centralized category-color mapping configuration
- Apply category-specific background colors to List and Player components
- Implement smooth CSS transitions when switching between categories
- Maintain "All" category with current default color scheme

**Non-Goals:**
- Not implementing dark/light mode toggling
- Not changing audio functionality or playback behavior
- Not modifying category data structures or API

## Decisions

**1. Category Theme Configuration File**
- Create `src/lib/category-themes.ts` as a standalone module exporting a color mapping object
- Use TypeScript for type safety with category keys
- Rationale: Centralized configuration is easier to maintain and update; separates concerns from components

**2. Color Scheme Definition**
- Map categories to Tailwind CSS color utilities following project standards
- Focus: Teal/blue tone using `bg-teal-500` (or custom teal value if default doesn't match)
- Relaxation: Warm tone using `bg-amber-500` or `bg-orange-400`
- Meditation: Neutral tone using `bg-neutral-500` or `bg-gray-400`
- All: Retain project's current default background class (e.g., `bg-gray-50`)
- Define custom colors via Tailwind CSS-first configuration (`@theme` in v4) if default palette needs adjustment
- Rationale: Aligns with project's Tailwind styling pattern, leverages Tailwind's design tokens for consistency

**3. Theme Application Strategy**
- Export category-specific Tailwind class strings from `src/lib/category-themes.ts` (e.g., `{ focus: 'bg-teal-500', relaxation: 'bg-amber-500' }`)
- Use Svelte's reactive class binding to apply correct background classes to List and Player components
- Rationale: Tailwind utility classes are project standard; dynamic class binding is idiomatic in Svelte

**4. Smooth Transition Implementation**
- Use Tailwind transition utilities: `transition-colors duration-300 ease-in-out` on themed elements
- Rationale: Follows Tailwind patterns, avoids custom CSS, provides consistent animation behavior

**5. Component Updates**
- List component: Apply theme to card backgrounds and container
- Player component: Apply theme to player card background
- Both components subscribe to category state or receive theme via prop/context

## Risks / Trade-offs

- [Color accessibility] → Ensure color contrast ratios meet WCAG AA standards for text over colored backgrounds; may need to adjust text colors per theme
- [Performance] → CSS variable updates are lightweight, but frequent category switching could cause visual flicker; mitigate with proper transition timing
- [Future categories] → Color mapping file will need updates; consider making it data-driven for easier extensibility
