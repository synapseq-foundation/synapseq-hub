## 1. Setup and Utilities

- [x] 1.1 Create `src/lib/utils/spsq-parser.ts` with function to fetch and parse spsq files
- [x] 1.2 Implement parsing logic: fetch text from "/" + path, extract lines starting with "##", remove prefix, trim, preserve empty lines

## 2. Collapsible Text Component

- [x] 2.1 Create `src/lib/components/CollapsibleText.svelte` component
- [x] 2.2 Implement logic to detect if text exceeds 3 lines (using JavaScript height detection)
- [x] 2.3 Add "Expand"/"Collapse" toggle button with proper state management

## 3. Audio Playback Modal Component

- [x] 3.1 Create `src/lib/components/AudioPlaybackModal.svelte` component with Svelte 5 runes
- [x] 3.2 Implement modal structure: close button (top-left), artwork (center), author info, description, warnings, footer buttons
- [x] 3.3 Style modal using Tailwind CSS: overlay, centered modal, proper spacing
- [x] 3.4 Add close icon button with functionality to dismiss modal
- [x] 3.5 Display audio artwork using appropriate image element
- [x] 3.6 Display author as "created by {author}" with small font (Tailwind `text-sm`)
- [x] 3.7 Integrate `CollapsibleText` component for description display
- [x] 3.8 Add listening warnings section with the three English warnings
- [x] 3.9 Add footer with "Cancel" and "PLAY!" buttons
- [x] 3.10 Implement Cancel button to close modal (same as close icon)
- [x] 3.11 Implement PLAY! button to close modal (no playback logic yet)

## 4. Integration

- [x] 4.1 Update audio list/item component to open modal on "Play" button click
- [x] 4.2 Pass audio data (path, artwork, author) to modal component
- [x] 4.3 Fetch and parse description from spsq file when modal opens
- [x] 4.4 Test modal opens correctly with all information displayed
- [x] 4.5 Test collapsible text works for long descriptions
- [x] 4.6 Test close/cancel/play buttons all dismiss modal properly
