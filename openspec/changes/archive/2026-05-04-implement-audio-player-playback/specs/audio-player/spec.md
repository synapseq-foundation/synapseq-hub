## MODIFIED Requirements

### Requirement: Play control
The system SHALL include a Play/Stop toggle button in the fixed player that starts and stops audio playback of the selected audio entry using HTML5 Audio API. The button SHALL show the `Play` icon from `@lucide/svelte` when not playing and the `Square` icon when playing.

#### Scenario: Play button starts audio playback
- **WHEN** the user clicks the Play button while no audio is playing
- **THEN** the system creates an `Audio` object with source URL `https://audio.synapseq.org/hub/{id}.mp3` where `{id}` is the selected entry's `id`
- **AND** starts playback of the audio
- **AND** the button icon changes to `Square` (Stop)

#### Scenario: Stop button stops audio playback
- **WHEN** the user clicks the Stop button while audio is playing
- **THEN** the system stops the audio playback
- **AND** the button icon changes to `Play`
- **AND** the player lock is released

#### Scenario: No selected audio
- **WHEN** no audio entry is selected
- **THEN** the Play button is not displayed and the player shows "Select an audio to start."

### Requirement: Audio playback with Media Session API
The system SHALL integrate with the Media Session API (`navigator.mediaSession`) when available to provide system-level media controls and display metadata during playback.

#### Scenario: Media Session metadata is set on playback
- **WHEN** audio playback starts
- **THEN** the system sets `navigator.mediaSession.metadata` with the audio entry's `name` as title, `author` as artist, and `/artwork/{id}.webp` as artwork
- **AND** registers `play`, `pause`, and `stop` action handlers

#### Scenario: Media Session play action
- **WHEN** the system triggers a Media Session `play` action (e.g., media key press)
- **THEN** the system starts audio playback if not already playing

#### Scenario: Media Session stop action
- **WHEN** the system triggers a Media Session `stop` or `pause` action (e.g., media key press)
- **THEN** the system stops audio playback

#### Scenario: Media Session not supported
- **WHEN** the browser does not support Media Session API
- **THEN** the system plays audio without Media Session integration and does not error

### Requirement: Player lock during playback
The system SHALL lock the audio list selection while audio is playing, preventing the user from selecting a different audio entry until playback is stopped.

#### Scenario: List selection is blocked during playback
- **WHEN** audio is playing
- **THEN** clicking on an audio row in the list does not change the selected audio entry

#### Scenario: List selection is restored after stop
- **WHEN** the user clicks the Stop button
- **THEN** the audio list selection is unlocked
- **AND** clicking on audio rows resumes changing the selected entry

#### Scenario: Stop button unlocks player
- **WHEN** audio playback stops (via Stop button or audio ending)
- **THEN** the player lock is released and normal selection behavior is restored

### Requirement: Progress visualization with category color
The system SHALL visualize audio playback progress by using the category background color as a progress indicator that fills from left to right as audio advances, replacing the static category background fill.

#### Scenario: Category color fills as progress advances
- **WHEN** audio playback starts
- **THEN** the player background transitions from the full category color fill to a progress-based fill
- **AND** the category color fills from left to right proportional to `currentTime / duration`

#### Scenario: Progress reaches completion
- **WHEN** audio playback reaches 100% (audio ends naturally)
- **THEN** the category color has completely filled the player bar
- **AND** playback stops
- **AND** the player lock is released

#### Scenario: Progress resets on stop
- **WHEN** the user clicks Stop before audio ends
- **THEN** the progress visualization resets
- **AND** the player returns to the static category color fill state

#### Scenario: Progress updates in real-time
- **WHEN** audio is playing
- **THEN** the progress visualization updates continuously (at least every 500ms) to reflect the current playback position
