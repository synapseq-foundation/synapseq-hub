## ADDED Requirements

### Requirement: Category color mapping configuration
The system SHALL provide a centralized TypeScript configuration file that maps each audio category to its corresponding Tailwind CSS background utility class.

#### Scenario: Valid category color mapping
- **WHEN** the category-themes.ts file is imported
- **THEN** it exports a mapping object with Tailwind background class strings for Focus, Meditation, Relaxation, and All categories

#### Scenario: Focus category color
- **WHEN** the Focus category is selected
- **THEN** the mapped Tailwind class SHALL be `bg-teal-500` (teal/blue tone)

#### Scenario: Relaxation category color
- **WHEN** the Relaxation category is selected
- **THEN** the mapped Tailwind class SHALL be `bg-amber-500` (warm tone)

#### Scenario: Meditation category color
- **WHEN** the Meditation category is selected
- **THEN** the mapped Tailwind class SHALL be `bg-neutral-500` (neutral tone)

#### Scenario: All category preserves default
- **WHEN** the All category is selected
- **THEN** the system SHALL apply the current default background class without category-specific theming

### Requirement: Dynamic background color application
The system SHALL apply the category-specific Tailwind background class to List and Player components when the selected category changes.

#### Scenario: List component theming
- **WHEN** a user selects a category (excluding All)
- **THEN** the List component cards and container SHALL have the Tailwind background class mapped to that category

#### Scenario: Player component theming
- **WHEN** a user selects a category (excluding All)
- **THEN** the Player component card SHALL have the Tailwind background class mapped to that category

### Requirement: Smooth theme transitions
The system SHALL use Tailwind transition utilities to animate background color changes when switching between categories.

#### Scenario: Smooth color transition
- **WHEN** the selected category changes from one to another
- **THEN** the components SHALL have `transition-colors duration-300 ease-in-out` applied for smooth 300ms transitions

#### Scenario: No transition on initial load
- **WHEN** the application loads for the first time with a category already selected
- **THEN** the background class SHALL be applied immediately without animation
