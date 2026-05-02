# Contributing to SynapSeq Hub

Thank you for your interest in contributing to the **SynapSeq Hub**, the official repository of sequences for [SynapSeq](https://github.com/synapseq-foundation/synapseq).

This document describes how to contribute new `.spsq` sequences, `.spsc` preset or option files, and ambiance audio files while ensuring quality, compatibility, and integrity.

---

## Repository Structure

Contributions are now organized by category directly at the `static` root directory.

Each category has its own directory for `.spsq` files. Shared dependency types now
live in dedicated directories.

### Directory layout
```
<category>/<sequence>.spsq
audio/<ambiance-file>.wav
config/<preset-file>.spsc
```

Where:

- **`<category>`** → Sequence category (`focus`, `relaxation`, `meditation`, `sleep`, `creative`, etc.)
- **`<sequence>`** → File name of your sequence
- **`<ambiance-file>`** → Ambiance audio file name stored in the root `audio/` directory
- **`<preset-file>`** → Preset or options file name stored in the root `config/` directory

### Examples

```
focus/deep-work.spsq
audio/deep-work-rain.wav
relaxation/ocean-drift.spsq
config/relaxation-presets.spsc
meditation/quiet-descent.spsq
```

Use dependency file names that clearly describe the content. For example,
`relaxation-presets.spsc` is preferred over vague names such as `presets.spsc`.

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

- `.wav` ambiance files must be stored in the root `audio/` directory
- `.spsc` preset or options files must be stored in the root `config/` directory
- Use descriptive file names that match the dependency purpose
- Inside `.spsq` files, `@ambiance` and `@extends` must always use Hub URLs, not local paths
- `@ambiance` must always use a URL under `https://hub.synapseq.org/audio/`
- `@extends` must always use a URL under `https://hub.synapseq.org/config/`
- These Hub URLs must be written even if the dependency file has not been published yet
- The `path` and every dependency `download_url` in `manifest.json` must point to the actual repository location of the file
- Dependency names in `manifest.json` should match the file names being distributed
- Dependencies with `type: "extends"` must always point to a `.spsc` file
- Dependencies with `type: "ambiance"` must always point to a `.wav` file compatible with SynapSeq CLI limits: PCM WAV, 8/16/24-bit, up to 20 MB
- External URLs are not allowed for sequence dependencies; use `hub.synapseq.org` only
- All referenced local files must exist in the repository

Examples inside `.spsq` files:

```
@ambiance ocean https://hub.synapseq.org/audio/ocean.wav

@extends https://hub.synapseq.org/config/options.spsc
```

### 4. Licensing

- All contributions must be licensed under **CC BY-SA 4.0**
- Ambiance `.wav` files must include proper attribution in the `.spsq` header

**Note:** Non-Commercial licenses (CC-BY-NC, CC-BY-NC-SA, etc.) are not allowed for ambiance audio, as they are incompatible with the commercial-permissive nature of the Hub and its CC BY-SA 4.0 licensing.

**You may NOT relicense third‑party audio as CC BY-SA 4.0.**

Examples of valid ambiance audio attribution in `.spsq` files:

```
## Ambiance "ocean": "Ocean Waves" by user example (CC BY 3.0)
## Source: https://freesound.org/people/example/sounds/12345/
```

```
## Ambiance "field": Original field recording by John Doe (CC BY-SA 4.0)
## Source: https://archive.org/details/john-doe-ocean-recording
```

```
## Ambiance "soft-wind": "Soft Wind" by Alice (CC0 - Public Domain)
## Source: https://freesound.org/people/alice/sounds/67890/
```

---

## Sequence Header Example

Each `.spsq` file must include a header using `##` comment lines:

```
## Deep Focus (20 minutes)
##
## Deep Focus is a steady, mid-intensity sequence designed to support
## alertness and sustained concentration.
## It uses clear rhythmic stimulation to promote focus without excess
## intensity, making it suitable for work, study, and other
## cognitively demanding tasks.
```

Recommended structure:

- First line: sequence title, optionally followed by duration in parentheses
- Blank separator line using `##`
- One or more short description lines using simple, direct language
- Another blank separator line using `##`
- Optional ambiance attribution lines when external audio is included

Comment lines in the header should be wrapped at 80 characters when possible.

If the sequence includes ambiance audio, extend the header like this:

```
## Deep Focus (20 minutes)
##
## Deep Focus is a steady, mid-intensity sequence designed to support
## alertness and sustained concentration.
##
## Ambiance "ocean": "Ocean Waves" by freesound.org/user/example (CC BY 3.0)
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
      "id": "ocean-waves-soft",
      "download_url": "https://hub.synapseq.org/audio/ocean-waves-soft.wav"
    },
    {
      "type": "extends",
      "id": "relaxation-presets",
      "download_url": "https://hub.synapseq.org/config/relaxation-presets.spsc"
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
- **`ambiance`** → Ambiance audio file in `.wav` format

When your sequence has no dependencies, use an empty array:

```json
"dependencies": []
```

---

## Steps to Contribute

1. Fork the repository
2. Clone your fork
3. Add your `.spsq` file to the correct category directory at the repository root
4. Add `.wav` dependencies to `audio/` and `.spsc` dependencies to `config/`
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
