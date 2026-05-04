## ADDED Requirements

### Requirement: Componentized player sections
The audio player implementation SHALL separate reusable and major UI sections into Svelte components while preserving the existing user-facing behavior.

#### Scenario: Main route composes player components
- **WHEN** the main route renders the Hub Player
- **THEN** the route composes separate components for the header, category badges, audio list, and fixed player
- **AND** route-level state remains responsible for manifest loading, selected category, selected audio, favorites, theme, and player messages

#### Scenario: Audio details are reused
- **WHEN** audio details are displayed in both the list and fixed player
- **THEN** both places use the same reusable audio details component for artwork, title, and author display

#### Scenario: Behavior is preserved after refactor
- **WHEN** the player is used after componentization
- **THEN** manifest loading, category filtering, artwork fallback, favorite persistence and ordering, favorite limit, theme switching, player selection, and Play control behavior remain equivalent to the existing implementation

#### Scenario: Components use Svelte 5 conventions
- **WHEN** extracted Svelte components are implemented
- **THEN** they use typed `$props`, `onclick` event attributes, keyed each blocks where lists are rendered, and avoid legacy Svelte patterns

#### Scenario: Components use Tailwind utilities
- **WHEN** extracted Svelte components are styled
- **THEN** they use Tailwind utility classes instead of pure component CSS for layout, spacing, borders, typography, responsive behavior, and interaction states
- **AND** they preserve SynapSeq theme tokens by referencing existing CSS variables where token-backed colors, shadows, or borders are required
