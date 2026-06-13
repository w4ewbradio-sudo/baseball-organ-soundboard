# Baseball Organ Soundboard Revamp — Design Spec
**Date:** 2026-06-13
**Repo:** w4ewbradio-sudo/baseball-organ-soundboard
**Status:** Approved

---

## Goal

Turn the soundboard into a pure-organ board built from real organ audio. Remove all crowd sounds, all synthetic/generated WAVs, and all non-organ effects. Keep the classic public-domain tunes as concepts but replace their audio with realistic sampled-organ renditions (Approach A: hybrid — real recordings where licensable, soundfont-rendered otherwise).

## What gets deleted

**Scripts:** `generate_samples.py`, `generate_extra_samples.py`, `add_freesound_samples.py`, `add_wikimedia_real_samples.py`, `wikimedia-real-manifest.json`

**Crowd/effects recordings:** `samples/wikimedia-real/` (all 3: metal bat, race crowd air horns, stadium crowd), `samples/freesound/real-charge-crowd.mp3` (organ but with heavy crowd noise — review on listen; drop if crowd-dominant)

**All generated WAVs:** everything in `samples/generated-extra/` (11 files) and all root-level `samples/*.wav` (18 files)

## What stays

The 4–5 real Freesound organ clips in `samples/freesound/`:
- real-baseball-organ.mp3 (CC0, treblebooster)
- real-cavalry-short.mp3 / real-cavalry-long.mp3 (CC0, vckhaze)
- real-play-ball.mp3 (CC BY, CGEffex)
- real-charge-crowd.mp3 — only if organ-dominant on listen

## New real recordings

Search Freesound, Wikimedia Commons, and Archive.org for genuine ballpark/Hammond organ clips under CC0 or CC-BY: stings, riffs, charge calls, rally cues. Verify the license on each before download. Add whatever is genuinely good (expected 3–8 clips); do not pad the count with mediocre clips. Every addition gets an ATTRIBUTION.md entry with author, license, and source URL.

CC-BY-NC and CC-BY-SA are excluded (same policy as the existing ATTRIBUTION.md).

## Classic tunes via sampled organ

Tunes to produce (public-domain melodies):
1. Take Me Out to the Ball Game
2. Charge! (da-da-da-da-da-DUH)
3. When the Saints Go Marching In
4. Camptown Races
5. The Entertainer
6. Mexican Hat Dance
7. Yankee Doodle
8. Pop Goes the Weasel
9. Shave and a Haircut
10. Habanera-style vamp (original, Bizet-adjacent)

**Pipeline:** Each tune is written as a MIDI file (melody + chords/voicing, organ-idiomatic: sustained chords, glissando flourishes where fitting) using Python (`mido` or `midiutil`). Rendered to WAV via FluidSynth (installed with winget) using the FluidR3_GM soundfont — drawbar organ preset (GM program 17) or percussive organ (GM 18), whichever sounds more "ballpark." Output normalized and converted to MP3 or kept as WAV (match what the page already serves; WAV is fine for a static site this size).

MIDI source files live in the repo under `midi/` so tunes can be edited and re-rendered later. A single `render_tunes.py` script (replacing the deleted generators) renders all MIDI files to `samples/tunes/`.

## index.html changes

- Two sections instead of four: **"Real organ recordings"** and **"Classic tunes (sampled organ)"**
- `songs` array rewritten to match the new file set; descriptions and license tags updated
- Footer text updated (real recordings + soundfont-rendered tunes, attribution in repo)
- Visual design unchanged

## ATTRIBUTION.md changes

- Remove entries for deleted samples
- Add entries for new recordings
- Add a section documenting the FluidR3_GM soundfont (MIT license) and the MIDI render pipeline

## Out of scope

No new features: no looping, no keyboard shortcuts, no recording, no layout redesign.

## Testing

- Open `index.html` locally; every pad plays, no 404s in console
- No references to deleted files remain in the repo (grep)
- ATTRIBUTION.md matches the actual file set
