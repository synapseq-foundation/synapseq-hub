## MODIFIED Requirements

### Requirement: SynapSeq player layout
The system SHALL present the main route as a player layout composed of header, categories, list, and fixed bottom player sections.

#### Scenario: Header is displayed
- **WHEN** the main route renders
- **THEN** the header displays `/artwork/default.webp` as the logo, the text `Hub Player`, and a light/dark theme toggle button aligned horizontally

#### Scenario: Fixed player is displayed
- **WHEN** an audio entry is selected
- **THEN** the player remains fixed at the bottom of the viewport and displays the selected audio details with a Play button aligned on the right

#### Scenario: Main content occupies full page width and background
- **WHEN** the main route renders the Hub Player
- **THEN** the header, categories, and audio list sit directly inside the `<main>` element without a card-like inner wrapper
- **AND** the main content area uses Tailwind utilities directly on `<main>` for full-width layout, background, and padding so it blends with the page background
- **AND** the main content container has no horizontal margins or width constraints such as `mx-auto` or `w-[min(100%,920px)]`
- **AND** the main content container has no borders, rounded corners, shadows, or backdrop blur that would create a card-on-background effect

#### Scenario: Player bar remains unchanged
- **WHEN** the layout is remodeled
- **THEN** the fixed `<AudioPlayerBar>` remains positioned at the bottom with its existing styling and behavior
