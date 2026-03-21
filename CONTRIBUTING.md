# Contributing to SynapSeq Hub

Thank you for your interest in contributing to the **SynapSeq Hub**, the official repository of sequences for [SynapSeq](https://github.com/ruanklein/synapseq).

This document describes how to contribute new `.spsq` sequences, `.spsc` preset or option files, and background audio files while ensuring quality, compatibility, and integrity.

---

## Repository Structure

Contributions are now organized by category directly at the root of the repository.

Each category has its own directory, and the sequence file lives inside that category directory together with its local dependencies, if any.

### Directory layout

```
<category>/<sequence>.spsq
<category>/<dependency-file>
```

Where:

- **`<category>`** → Sequence category (`focus`, `relaxation`, `meditation`, `sleep`, `creative`, etc.)
- **`<sequence>`** → File name of your sequence
- **`<dependency-file>`** → Any local file referenced by the sequence and distributed with it, such as a background `.wav`

### Examples

```
focus/deep-work.spsq
focus/deep-work.wav
relaxation/ocean-drift.spsq
relaxation/ocean-drift.wav
meditation/quiet-descent.spsq
```

Pull Requests that place contribution files outside their category directory may be rejected.

---

## Quality and Integrity

SynapSeq Hub is consumed by the SynapSeq CLI, which downloads and exposes community sequences to end users.

SynapSeq Hub maintains a high standard of clarity and honesty about what brainwave entrainment can and cannot do.

Brainwave audio **cannot** reproduce the effects of drugs, medications, or chemical substances. Claims such as "LSD simulation", "ecstasy effect", "instant healing" or similar are unrealistic and misrepresent what binaural, monaural, or isochronic stimulation can achieve.

### Not allowed:

- Claims that sequences mimic drugs or psychoactive substances
- Promises of medical, pharmacological, or therapeutic outcomes
- Titles or descriptions suggesting impossible or exaggerated effects

### Allowed:

- Relaxation, focus, meditation, sleep, creativity, and atmospheric themes
- Fictional or artistic names without medical connotations
- Creative sessions built around real brainwave frequency ranges

---

## Submission Rules

### 1. Allowed file types

- `.spsq` → Sequence file (UTF‑8)
- `.spsc` → Preset or options configuration file (UTF‑8)
- `.wav` → Optional ambiance audio (PCM WAV, 8/16/24‑bit, stereo)

### 2. Size limits

- `.spsq` files: **max 32 KB**
- `.wav` ambiance files: **max 20 MB**

### 3. Dependency rules

- All dependencies must live inside the same category directory as the main `.spsq` sequence whenever possible
- The `path` and every dependency `download_url` in `manifest.json` must point to the actual repository location of the file
- Dependency names in `manifest.json` should match the file names being distributed
- Dependencies with `type: "extends"` must always point to a `.spsc` file
- Dependencies with `type: "ambiance"` must always point to a `.wav` file compatible with SynapSeq CLI limits: PCM WAV, 8/16/24-bit, up to 20 MB
- External URLs are not allowed
- All referenced local files must exist in the repository

### 4. Licensing

- All contributions must be licensed under **CC BY-SA 4.0**
- `.spsq` header must explicitly state the license
- Background `.wav` files must include proper attribution in the `.spsq` header

**Note:** Non-Commercial licenses (CC-BY-NC, CC-BY-NC-SA, etc.) are not allowed for background audio, as they are incompatible with the commercial-permissive nature of the Hub and its CC BY-SA 4.0 licensing.

**You may NOT relicense third‑party audio as CC BY-SA 4.0.**

Examples of valid background audio attribution in `.spsq` files:

```
## Background: "Ocean Waves" by user example (CC BY 3.0)
## Source: https://freesound.org/people/example/sounds/12345/
```

```
## Background: Original field recording by John Doe
## License: CC BY-SA 4.0
## Source: https://archive.org/details/john-doe-ocean-recording
```

```
## Background: "Soft Wind" by Alice (CC0 - Public Domain)
## Source: https://freesound.org/people/alice/sounds/67890/
```

---

## Sequence Header Example

Each `.spsq` file must include a header using `##` comment lines:

```
## Title: Deep Focus
## License: CC BY-SA 4.0
##
## Background: "Ocean Waves" by freesound.org/user/example (CC BY 3.0)
## Source: https://freesound.org/people/example/sounds/12345/
```

The author name is no longer declared in the `.spsq` header. It must be provided in `manifest.json` for the corresponding entry.

---

## Manifest Update Requirements

Every contribution must include a manual update to `manifest.json`.

The manifest is the source of truth used by SynapSeq Hub clients to list downloadable entries. If you add a new sequence and do not add it to `manifest.json`, the contribution will be incomplete.

### Required entry fields

Each sequence must have a corresponding object inside the `entries` array with the following structure:

```json
{
  "id": "ocean-drift",
  "name": "Ocean Drift",
  "author": "Jane Doe",
  "category": "Relaxation",
  "path": "relaxation/ocean-drift.spsq",
  "download_url": "https://hub.synapseq.org/relaxation/ocean-drift.spsq",
  "updated_at": "2026-03-21T00:00:00Z",
  "dependencies": [
    {
      "type": "ambiance",
      "name": "ocean-drift.wav",
      "download_url": "https://hub.synapseq.org/relaxation/ocean-drift.wav"
    },
    {
      "type": "extends",
      "name": "base-relax-presets.spsc",
      "download_url": "https://hub.synapseq.org/relaxation/base-relax-presets.spsc"
    }
  ]
}
```

### Field meanings

- **`id`** → Stable unique identifier for the entry
- **`name`** → Human-readable sequence name
- **`author`** → Author name shown by the Hub client
- **`category`** → Display category used by the Hub client
- **`path`** → Relative path to the main `.spsq` file inside this repository
- **`download_url`** → Public download URL for the main `.spsq` file
- **`updated_at`** → ISO 8601 timestamp in UTC
- **`dependencies`** → Optional list of downloadable dependencies

### Supported dependency types

- **`extends`** → Additional `.spsc` file used as an extension, preset source, or options source
- **`ambiance`** → Background audio file in `.wav` format

When your sequence has no dependencies, use an empty array:

```json
"dependencies": []
```

---

## Steps to Contribute

1. Fork the repository
2. Clone your fork
3. Add your `.spsq` file to the correct category directory at the repository root
4. Add any local dependencies for that sequence in the same category directory
5. Update `manifest.json` manually by adding a new object to the `entries` array
6. Make sure `path`, `download_url`, `updated_at`, and `dependencies` are correct
7. Validate the JSON formatting before opening your Pull Request
8. Commit and push
9. Open a Pull Request

---

## Support, Issues, and Discussions

For questions or suggestions:

- **Issues:**  
  https://github.com/synapseq-foundation/synapseq/issues

- **Discussions:**  
  https://github.com/synapseq-foundation/synapseq/discussions

Thank you for contributing and helping maintain a clean, reliable, and well‑structured library of sequences.
