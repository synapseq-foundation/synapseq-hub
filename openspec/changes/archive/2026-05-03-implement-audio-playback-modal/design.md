## Context

The application currently has audio items with a "Play" button but lacks a preview/confirmation modal. Users need to see audio details (artwork, author, description) and receive listening guidance before playback starts. The audio descriptions are stored in spsq files that need to be fetched and parsed.

## Goals / Non-Goals

**Goals:**
- Create a modal component that displays audio information when user clicks "Play"
- Parse audio descriptions from spsq files (JSON at "/" + path)
- Implement collapsible text for long descriptions (3+ lines)
- Provide clear listening warnings in English
- Use Tailwind CSS for styling
- PLAY! button closes modal (play logic deferred)

**Non-Goals:**
- Implementing actual audio playback logic
- Modifying existing audio list components beyond adding modal trigger
- Supporting mobile-specific layouts (using responsive Tailwind classes only)
- Adding animations/transitions to modal (can be added later)

## Decisions

### Modal Implementation
**Decision**: Create a new Svelte component `AudioPlaybackModal.svelte` using Tailwind CSS for styling.
**Rationale**: Tailwind provides rapid styling with utility classes. Svelte 5 runes ($state, $props) will be used for reactivity.
**Alternatives considered**: Using a CSS module or styled-components - rejected due to project using Tailwind.

### Description Parsing
**Decision**: Fetch spsq file as JSON from "/" + path, then parse content to extract lines starting with "##".
**Rationale**: spsq files contain markdown-like content where "##" prefixes indicate description lines. Removing "##" and trimming preserves formatting.
**Parsing logic**:
1. Fetch JSON from "/" + audio path
2. Extract content string from JSON response
3. Split by newlines
4. Filter lines starting with "##"
5. Remove "##" prefix and trim each line
6. Preserve empty lines (lines with just "##" become empty strings, representing newlines)

### Collapsible Text Component
**Decision**: Create a reusable `CollapsibleText.svelte` component.
**Rationale**: Separates concerns and allows reuse. Shows "Expand" button when content exceeds 3 lines.
**Implementation**: Use CSS line-clamp or JavaScript to detect text height vs 3 lines threshold.

### Modal State Management
**Decision**: Use a simple boolean state in parent component or a global modal store.
**Rationale**: Keeps it simple for now. Can be enhanced later if needed.

## Risks / Trade-offs

- **Risk**: spsq file format may vary → Mitigation: Handle edge cases in parsing (empty lines, missing "##" lines)
- **Risk**: Description parsing relies on "##" prefix convention → Mitigation: Document the convention; consider making it configurable
- **Trade-off**: PLAY! button only closes modal (no playback yet) → Acceptable for this iteration; playback logic is separate concern
