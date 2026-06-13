# Organ Revamp Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace all synthetic and crowd audio with real organ recordings and sampled-organ tune renditions, per `docs/superpowers/specs/2026-06-13-organ-revamp-design.md`.

**Architecture:** Static single-page soundboard (`index.html`). New audio comes from two pipelines: (1) curated real CC0/CC-BY organ recordings downloaded from Freesound/Wikimedia, and (2) classic tunes written as MIDI in Node (`midi-writer-js`) and rendered to WAV through FluidSynth + the FluidR3_GM soundfont (real Hammond samples). MIDI sources and a render script live in the repo; the soundfont and FluidSynth binaries are local-only (gitignored).

**Tech Stack:** Node 24, midi-writer-js, FluidSynth CLI (winget or GitHub release zip), FluidR3_GM.sf2 soundfont, plain HTML/JS.

**Working directory for all tasks:** `C:\Users\Eric\Documents\GitHub\baseball-organ-soundboard`

**Environment notes:** Windows 11. No Python installed — do not use Python. Node v24 and winget are available. Shell commands below are Git Bash syntax unless marked PowerShell.

---

### Task 1: Delete synthetic audio, crowd sounds, and generator scripts

**Files:**
- Delete: `generate_samples.py`, `generate_extra_samples.py`, `add_freesound_samples.py`, `add_wikimedia_real_samples.py`, `wikimedia-real-manifest.json`
- Delete: entire `samples/generated-extra/` directory (11 WAVs)
- Delete: entire `samples/wikimedia-real/` directory (3 MP3s)
- Delete: all 18 root-level `samples/*.wav` files
- Delete: `samples/freesound/real-charge-crowd.mp3` (description is "WALLA_Ballpark Organ Cheering Charge" — crowd-dominant by its own title; user chose to remove all crowd sounds)

**Keep (do NOT delete):** `samples/freesound/real-baseball-organ.mp3`, `real-cavalry-short.mp3`, `real-cavalry-long.mp3`, `real-play-ball.mp3`

- [ ] **Step 1: Delete the files**

```bash
cd /c/Users/Eric/Documents/GitHub/baseball-organ-soundboard
git rm generate_samples.py generate_extra_samples.py add_freesound_samples.py add_wikimedia_real_samples.py wikimedia-real-manifest.json
git rm -r samples/generated-extra samples/wikimedia-real
git rm samples/*.wav
git rm samples/freesound/real-charge-crowd.mp3
```

- [ ] **Step 2: Verify only the 4 keeper files remain in samples/**

```bash
find samples -type f
```
Expected output — exactly these 4 lines:
```
samples/freesound/real-baseball-organ.mp3
samples/freesound/real-cavalry-long.mp3
samples/freesound/real-cavalry-short.mp3
samples/freesound/real-play-ball.mp3
```

- [ ] **Step 3: Commit**

```bash
git commit -m "chore: remove synthetic audio, crowd sounds, and generator scripts"
```

Note: `index.html` and `ATTRIBUTION.md` now reference missing files. That is expected; Tasks 5 and 6 fix them. Do not edit them in this task.

---

### Task 2: Tooling — package.json, .gitignore, FluidSynth, soundfont

**Files:**
- Create: `package.json`
- Create: `.gitignore`
- Local-only (gitignored): `tools/fluidsynth/` (binaries), `tools/FluidR3_GM.sf2`

- [ ] **Step 1: Create `package.json`**

```json
{
  "name": "baseball-organ-soundboard",
  "version": "2.0.0",
  "private": true,
  "description": "Browser-based baseball organ soundboard with real organ samples",
  "scripts": {
    "render": "node render_tunes.js",
    "verify": "node verify_samples.js"
  },
  "dependencies": {
    "midi-writer-js": "^3.1.1"
  }
}
```

- [ ] **Step 2: Create `.gitignore`**

```
node_modules/
tools/
*.log
```

- [ ] **Step 3: Install npm deps**

```bash
cd /c/Users/Eric/Documents/GitHub/baseball-organ-soundboard
npm install
```
Expected: `added N packages` with no errors.

- [ ] **Step 4: Install FluidSynth**

Try winget first (PowerShell):
```powershell
winget install --id FluidSynth.FluidSynth --accept-source-agreements --accept-package-agreements
```
If winget has no such package, fall back to the GitHub release zip:
```bash
mkdir -p tools/fluidsynth
curl -sL https://api.github.com/repos/FluidSynth/fluidsynth/releases/latest \
  | grep browser_download_url | grep -i 'win10-x64' | grep -o 'https://[^"]*' | head -1
# download the URL printed above:
curl -sL -o tools/fluidsynth.zip "<URL from previous command>"
cd tools/fluidsynth && unzip -o ../fluidsynth.zip && cd ../..
```
Then locate the binary: it will be `tools/fluidsynth/bin/fluidsynth.exe` (zip path) or on PATH (winget path). All later commands use the variable `FLUIDSYNTH` — set it to whichever exists:
```bash
FLUIDSYNTH=$(command -v fluidsynth || echo tools/fluidsynth/bin/fluidsynth.exe)
"$FLUIDSYNTH" --version
```
Expected: `FluidSynth runtime version 2.x.x`

- [ ] **Step 5: Download FluidR3_GM.sf2 (~140 MB)**

```bash
curl -sL -o tools/FluidR3_GM.zip "https://keymusician01.s3.amazonaws.com/FluidR3_GM.zip" \
  || curl -sL -o tools/FluidR3_GM.sf2 "https://archive.org/download/fluidr3-gm-gs/FluidR3_GM.sf2"
# if the zip downloaded, extract:
[ -f tools/FluidR3_GM.zip ] && (cd tools && unzip -o FluidR3_GM.zip FluidR3_GM.sf2)
ls -la tools/FluidR3_GM.sf2
```
Expected: file exists, size roughly 140–150 MB. If both URLs fail, search for another FluidR3_GM.sf2 mirror (it is a widely mirrored MIT-licensed soundfont) — verify size > 100 MB before accepting.

- [ ] **Step 6: Smoke-test the render pipeline**

```bash
node -e "
const M=require('midi-writer-js');const fs=require('fs');
const t=new M.Track();t.setTempo(120);
t.addEvent(new M.ProgramChangeEvent({instrument:16}));
t.addEvent(new M.NoteEvent({pitch:['C4','E4','G4'],duration:'1'}));
fs.writeFileSync('tools/smoke.mid',Buffer.from(new M.Writer(t).buildFile()));
console.log('midi ok');"
"$FLUIDSYNTH" -ni -g 0.8 -F tools/smoke.wav -r 44100 tools/FluidR3_GM.sf2 tools/smoke.mid
ls -la tools/smoke.wav
```
Expected: `midi ok`, then a WAV > 100 KB. (A C-major organ chord.)

- [ ] **Step 7: Commit**

```bash
git add package.json .gitignore package-lock.json
git commit -m "build: node tooling for MIDI/FluidSynth tune rendering"
```

---

### Task 3: Tune data and render script

**Files:**
- Create: `tunes.js` (melody data)
- Create: `render_tunes.js` (MIDI writer + FluidSynth driver)
- Create: `midi/*.mid` (generated, committed)
- Create: `samples/tunes/*.wav` (generated, committed)

**Musical direction:** Each tune is the *iconic hook only* — 5 to 15 seconds, the part a ballpark organist actually plays. Two tracks: melody (GM instrument 16, Drawbar Organ, velocity ~90) and chords (same instrument, velocity ~55, sustained root-position triads). The data below is a best-effort transcription; Task 7 includes a listening pass where wrong notes get fixed.

- [ ] **Step 1: Create `tunes.js`**

Format: each tune = `{ file, name, tempo, melody: [[pitchOrChord, duration, wait?], ...], chords: [[chordPitches, duration, wait?], ...] }`. Durations use midi-writer-js codes (`'1'`,`'2'`,`'d2'`,`'4'`,`'d4'`,`'8'`,`'16'`); `wait` is an optional rest before the note.

```js
// tunes.js — melody data for sampled-organ renditions of public-domain tunes.
// Pitches: scientific notation. Durations: midi-writer-js codes.
module.exports = [
  {
    file: 'charge', name: 'Charge!', tempo: 160,
    melody: [
      ['G4','8'], ['C5','8'], ['E5','8'], ['G5','d4'], ['E5','8'], ['G5','1'],
    ],
    chords: [
      [['C3','E3','G3'], '2', '2'], [['C3','E3','G3','C4'], '1'],
    ],
  },
  {
    file: 'take-me-out', name: 'Take Me Out to the Ball Game', tempo: 150,
    // 3/4 feel: "Take me out to the ball game / Take me out with the crowd"
    melody: [
      ['C5','4'], ['A4','4'], ['G4','4'], ['E4','4'], ['G4','2'], ['D4','d2'],
      ['C5','4','4'], ['A4','4'], ['G4','4'], ['E4','4'], ['G4','2'], ['D4','d2'],
    ],
    chords: [
      [['C3','E3','G3'], 'd2'], [['C3','E3','G3'], 'd2'], [['G2','B2','D3'], 'd2'],
      [['C3','E3','G3'], 'd2', '4'], [['C3','E3','G3'], 'd2'], [['G2','B2','D3'], 'd2'],
    ],
  },
  {
    file: 'saints', name: 'When the Saints Go Marching In', tempo: 120,
    melody: [
      ['C4','8'], ['E4','8'], ['F4','8'], ['G4','2'],
      ['C4','8','8'], ['E4','8'], ['F4','8'], ['G4','2'],
      ['C4','8','8'], ['E4','8'], ['F4','8'], ['G4','4'], ['E4','4'], ['C4','4'], ['E4','4'], ['D4','1'],
    ],
    chords: [
      [['C3','E3','G3'], '1'], [['C3','E3','G3'], '1'],
      [['C3','E3','G3'], '1'], [['G2','B2','D3'], '1'],
    ],
  },
  {
    file: 'camptown', name: 'Camptown Races', tempo: 140,
    melody: [
      ['G4','4'], ['G4','4'], ['E4','4'], ['G4','4'],
      ['A4','4'], ['G4','4'], ['E4','2'],
      ['E4','4'], ['D4','2'], ['E4','4'], ['D4','2'],
      ['G4','4','4'], ['G4','4'], ['E4','4'], ['G4','4'],
      ['A4','4'], ['G4','4'], ['E4','2'],
      ['D4','4'], ['E4','8'], ['D4','8'], ['C4','2'],
    ],
    chords: [
      [['C3','E3','G3'], '1'], [['C3','E3','G3'], '1'],
      [['G2','B2','D3'], '1'], [['G2','B2','D3'], '1'],
      [['C3','E3','G3'], '1'], [['C3','E3','G3'], '1'],
      [['G2','B2','D3'], '2'], [['C3','E3','G3'], '2'],
    ],
  },
  {
    file: 'entertainer', name: 'The Entertainer', tempo: 90,
    melody: [
      ['D4','8'], ['Eb4','8'], ['E4','8'],
      ['C5','4'], ['E4','8'], ['C5','4'], ['E4','8'], ['C5','2'],
      ['C5','8'], ['D5','8'], ['Eb5','8'], ['E5','8'], ['C5','8'], ['D5','8'],
      ['E5','4'], ['B4','8'], ['D5','4'], ['C5','2'],
    ],
    chords: [
      [['C3','E3','G3'], '2', '8'], [['C3','E3','G3'], '2'],
      [['C3','E3','G3'], '2'], [['F3','A3','C4'], '2'],
      [['G2','B2','D3'], '2'], [['C3','E3','G3'], '2'],
    ],
  },
  {
    file: 'mexican-hat', name: 'Mexican Hat Dance', tempo: 130,
    melody: [
      ['E5','8'], ['C5','8'], ['C5','8'], ['C5','4','8'],
      ['D5','8'], ['B4','8'], ['B4','8'], ['B4','4','8'],
      ['C5','8'], ['D5','8'], ['E5','8'], ['F5','8'], ['E5','8'], ['D5','8'], ['C5','4'],
    ],
    chords: [
      [['C3','E3','G3'], '2'], [['G2','B2','D3'], '2'],
      [['G2','B2','D3'], '2'], [['C3','E3','G3'], '2'],
      [['C3','E3','G3'], '2'], [['G2','B2','D3'], '4'], [['C3','E3','G3'], '4'],
    ],
  },
  {
    file: 'yankee-doodle', name: 'Yankee Doodle', tempo: 120,
    melody: [
      ['C4','4'], ['C4','4'], ['D4','4'], ['E4','4'],
      ['C4','4'], ['E4','4'], ['D4','4'], ['G3','4'],
      ['C4','4'], ['C4','4'], ['D4','4'], ['E4','4'],
      ['C4','2'], ['B3','2'],
      ['C4','4'], ['C4','4'], ['D4','4'], ['E4','4'],
      ['F4','4'], ['E4','4'], ['D4','4'], ['C4','4'],
      ['B3','4'], ['G3','4'], ['A3','4'], ['B3','4'],
      ['C4','2'], ['C4','2'],
    ],
    chords: [
      [['C3','E3','G3'], '1'], [['C3','E3','G3'], '1'],
      [['C3','E3','G3'], '1'], [['G2','B2','D3'], '1'],
      [['C3','E3','G3'], '1'], [['F3','A3','C4'], '1'],
      [['G2','B2','D3'], '1'], [['C3','E3','G3'], '1'],
    ],
  },
  {
    file: 'pop-weasel', name: 'Pop Goes the Weasel', tempo: 130,
    melody: [
      ['C4','4'], ['C4','8'], ['D4','4'], ['D4','8'],
      ['E4','8'], ['G4','8'], ['E4','8'], ['C4','d4'],
      ['C4','4'], ['C4','8'], ['D4','4'], ['D4','8'],
      ['E4','d4'], ['C4','d4'],
      ['C4','4'], ['C4','8'], ['D4','4'], ['D4','8'],
      ['E4','8'], ['G4','8'], ['E4','8'], ['C4','d4'],
      ['A4','d4'], ['D4','4'], ['F4','8'], ['E4','d4'], ['C4','d4'],
    ],
    chords: [
      [['C3','E3','G3'], 'd2'], [['C3','E3','G3'], 'd2'],
      [['G2','B2','D3'], 'd2'], [['C3','E3','G3'], 'd2'],
      [['C3','E3','G3'], 'd2'], [['C3','E3','G3'], 'd2'],
      [['F3','A3','C4'], 'd2'], [['G2','B2','D3'], '4'], [['C3','E3','G3'], '2'],
    ],
  },
  {
    file: 'shave-haircut', name: 'Shave and a Haircut', tempo: 120,
    melody: [
      ['C5','8'], ['G4','16'], ['G4','16'], ['A4','8'], ['G4','8'],
      ['B4','8','8'], ['C5','4'],
    ],
    chords: [
      [['C3','E3','G3'], '2'], [['G2','B2','D3'], '8', '8'], [['C3','E3','G3'], '4'],
    ],
  },
  {
    file: 'habanera-vamp', name: 'Habanera Vamp', tempo: 110,
    // Original Bizet-adjacent vamp in D minor, habanera rhythm, repeated twice.
    melody: [
      ['D4','d8'], ['F4','16'], ['A4','8'], ['F4','8'],
      ['D4','d8'], ['F4','16'], ['A4','8'], ['F4','8'],
      ['E4','d8'], ['G4','16'], ['Bb4','8'], ['G4','8'],
      ['A4','d8'], ['F4','16'], ['D4','8'], ['A3','8'],
      ['D4','d8'], ['F4','16'], ['A4','8'], ['F4','8'],
      ['D4','d8'], ['F4','16'], ['A4','8'], ['F4','8'],
      ['E4','d8'], ['G4','16'], ['Bb4','8'], ['G4','8'],
      ['D4','2'],
    ],
    chords: [
      [['D3','F3','A3'], '2'], [['D3','F3','A3'], '2'],
      [['A2','C#3','E3'], '2'], [['D3','F3','A3'], '2'],
      [['D3','F3','A3'], '2'], [['D3','F3','A3'], '2'],
      [['A2','C#3','E3'], '2'], [['D3','F3','A3'], '2'],
    ],
  },
];
```

- [ ] **Step 2: Create `render_tunes.js`**

```js
// render_tunes.js — writes each tune in tunes.js to midi/<file>.mid,
// then renders samples/tunes/<file>.wav through FluidSynth + FluidR3_GM.
// Usage: node render_tunes.js   (requires tools/FluidR3_GM.sf2 and fluidsynth)
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const MidiWriter = require('midi-writer-js');
const tunes = require('./tunes');

const SOUNDFONT = path.join(__dirname, 'tools', 'FluidR3_GM.sf2');
const ORGAN = 16; // GM Drawbar Organ (0-indexed)

function findFluidsynth() {
  const local = path.join(__dirname, 'tools', 'fluidsynth', 'bin', 'fluidsynth.exe');
  if (fs.existsSync(local)) return local;
  return 'fluidsynth'; // assume on PATH (winget install)
}

function buildTrack(events, velocity) {
  // Both tracks use channel 1 — midi-writer-js ProgramChangeEvent has no
  // reliable channel parameter, and both tracks are the same organ anyway.
  const track = new MidiWriter.Track();
  track.addEvent(new MidiWriter.ProgramChangeEvent({ instrument: ORGAN }));
  for (const [pitch, duration, wait] of events) {
    track.addEvent(new MidiWriter.NoteEvent({
      pitch: Array.isArray(pitch) ? pitch : [pitch],
      duration, wait: wait || '0', velocity, channel: 1,
    }));
  }
  return track;
}

if (!fs.existsSync(SOUNDFONT)) {
  console.error('Missing tools/FluidR3_GM.sf2 — see Task 2 of the plan.');
  process.exit(1);
}
fs.mkdirSync(path.join(__dirname, 'midi'), { recursive: true });
fs.mkdirSync(path.join(__dirname, 'samples', 'tunes'), { recursive: true });

const fluidsynth = findFluidsynth();
for (const tune of tunes) {
  const melody = buildTrack(tune.melody, 90);
  melody.setTempo(tune.tempo);
  const chords = buildTrack(tune.chords, 55);
  const midiPath = path.join('midi', `${tune.file}.mid`);
  const wavPath = path.join('samples', 'tunes', `${tune.file}.wav`);
  fs.writeFileSync(midiPath, Buffer.from(new MidiWriter.Writer([melody, chords]).buildFile()));
  execFileSync(fluidsynth, ['-ni', '-g', '0.8', '-F', wavPath, '-r', '44100', SOUNDFONT, midiPath]);
  const kb = Math.round(fs.statSync(wavPath).size / 1024);
  console.log(`${tune.file}: midi + ${kb} KB wav`);
}
console.log(`Rendered ${tunes.length} tunes.`);
```

- [ ] **Step 3: Run the render**

```bash
cd /c/Users/Eric/Documents/GitHub/baseball-organ-soundboard
node render_tunes.js
```
Expected: 10 lines like `charge: midi + 800 KB wav`, then `Rendered 10 tunes.` Every WAV must be > 100 KB (silence/failure produces tiny files — investigate any small one).

- [ ] **Step 4: Spot-check one WAV is real audio**

```bash
node -e "
const fs=require('fs');const b=fs.readFileSync('samples/tunes/charge.wav');
let peak=0;for(let i=44;i<b.length-1;i+=2){const v=Math.abs(b.readInt16LE(i));if(v>peak)peak=v;}
console.log('peak amplitude:',peak, peak>3000?'OK':'TOO QUIET — investigate');"
```
Expected: `peak amplitude: <number> OK` (peak above 3000 of 32767).

- [ ] **Step 5: Commit**

```bash
git add tunes.js render_tunes.js midi samples/tunes
git commit -m "feat: classic tunes rendered through real organ soundfont"
```

---

### Task 4: Source new real organ recordings

**Files:**
- Create: `samples/real/*.mp3` (3–8 new clips)
- Create: `samples/real/sources.json` (machine-readable provenance, used by Task 6)

**License policy (from spec):** CC0 or CC BY only. No CC-BY-NC, no CC-BY-SA. Verify the license on the sound's own page before downloading. Record author, license, and source URL for every file.

- [ ] **Step 1: Search for candidates**

Use WebSearch/WebFetch against these sources with queries like "baseball organ", "stadium organ", "ballpark organ", "hammond organ sting", "organ riff", "organ charge":
- `https://freesound.org/search/?q=<query>` — each result page states the license; the preview MP3 URL is in the `og:audio` meta tag of the sound page and downloads without auth (existing repo clips were obtained this way)
- Wikimedia Commons API: `https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch=<query>%20filetype:audio&format=json`
- `https://archive.org/advancedsearch.php?q=<query>+AND+mediatype:audio&output=json` — check item license field

- [ ] **Step 2: Curate**

Pick only clips that are genuinely organ-dominant and usable as soundboard pads (stings, riffs, short phrases — not 5-minute performances, not crowd-heavy recordings). Quality over quantity: 3 good clips beat 8 mediocre ones. Skip anything whose license cannot be confirmed on the source page.

- [ ] **Step 3: Download into `samples/real/`**

```bash
mkdir -p samples/real
curl -sL -o samples/real/<descriptive-name>.mp3 "<preview-or-file-url>"
```
Verify each file is > 20 KB and starts with MP3/ID3 magic bytes:
```bash
for f in samples/real/*.mp3; do head -c 3 "$f" | xxd | head -1; done
```
Expected: `ID3` or `fff` (MPEG sync) per file.

- [ ] **Step 4: Write `samples/real/sources.json`**

One entry per downloaded file:
```json
[
  {
    "file": "example-organ-sting.mp3",
    "title": "<original title>",
    "author": "<author>",
    "license": "CC0",
    "url": "<source page URL>"
  }
]
```

- [ ] **Step 5: Commit**

```bash
git add samples/real
git commit -m "feat: add real CC0/CC-BY organ recordings"
```

---

### Task 5: Rewrite index.html song list

**Files:**
- Modify: `index.html` (the `songs` array, the section headings/containers, and the footer paragraph — leave all CSS and player JS untouched)

- [ ] **Step 1: Replace the four section blocks in `<main>`**

Replace:
```html
  <h2 class="section-title">Real safe-to-use samples</h2>
  <section class="grid" id="real"></section>
  <h2 class="section-title">Generated organ bits</h2>
  <section class="grid" id="traditional"></section>
  <h2 class="section-title">Safe homemade effects</h2>
  <section class="grid" id="effects"></section>
  <h2 class="section-title">Classic public-domain tunes</h2>
  <section class="grid" id="classics"></section>
```
With:
```html
  <h2 class="section-title">Real organ recordings</h2>
  <section class="grid" id="real"></section>
  <h2 class="section-title">Classic tunes (sampled organ)</h2>
  <section class="grid" id="tunes"></section>
```

- [ ] **Step 2: Replace the footer paragraph**

Replace the existing `<p class="footer">...</p>` with:
```html
  <p class="footer">Real organ recordings are verified CC0/CC-BY samples from Freesound and Wikimedia Commons. Classic tunes are public-domain melodies rendered through a real Hammond organ soundfont. Full attribution in the repo.</p>
```

- [ ] **Step 3: Replace the `songs` array**

The `real` section lists the 4 kept Freesound clips plus every file in `samples/real/` (names/descriptions from `sources.json`). The `tunes` section lists all 10 rendered tunes. Template:

```js
const songs = [
  {cat:'real', name:'Real Baseball Organ', desc:'CC0 Freesound organ clip by treblebooster.', tag:'CC0', src:'samples/freesound/real-baseball-organ.mp3'},
  {cat:'real', name:'Real Cavalry Short', desc:'CC0 baseball cavalry sting by vckhaze.', tag:'CC0', src:'samples/freesound/real-cavalry-short.mp3'},
  {cat:'real', name:'Real Cavalry Long', desc:'CC0 baseball cavalry sting by vckhaze.', tag:'CC0', src:'samples/freesound/real-cavalry-long.mp3'},
  {cat:'real', name:'Real Play Ball', desc:'CC-BY old-time play ball organ by CGEffex.', tag:'CC BY', src:'samples/freesound/real-play-ball.mp3'},
  // one entry per samples/real/ file, e.g.:
  // {cat:'real', name:'<Title>', desc:'<license> <descr> by <author>.', tag:'<CC0|CC BY>', src:'samples/real/<file>.mp3'},

  {cat:'tunes', name:'Charge!', desc:'The classic da-da-da-DUH rally fanfare.', tag:'organ', src:'samples/tunes/charge.wav'},
  {cat:'tunes', name:'Take Me Out to the Ball Game', desc:'The essential ballpark chorus.', tag:'1908 classic', src:'samples/tunes/take-me-out.wav'},
  {cat:'tunes', name:'When the Saints', desc:'Brassy, happy, impossible not to grin.', tag:'public domain', src:'samples/tunes/saints.wav'},
  {cat:'tunes', name:'Camptown Races', desc:'Old-timey sprint around the bases.', tag:'public domain', src:'samples/tunes/camptown.wav'},
  {cat:'tunes', name:'The Entertainer', desc:'Ragtime concession-stand chaos.', tag:'public domain', src:'samples/tunes/entertainer.wav'},
  {cat:'tunes', name:'Mexican Hat Dance', desc:'Mascot race fuel.', tag:'traditional', src:'samples/tunes/mexican-hat.wav'},
  {cat:'tunes', name:'Yankee Doodle', desc:'Patriotic baseball-adjacent silliness.', tag:'public domain', src:'samples/tunes/yankee-doodle.wav'},
  {cat:'tunes', name:'Pop Goes the Weasel', desc:'For pitching changes and other nonsense.', tag:'public domain', src:'samples/tunes/pop-weasel.wav'},
  {cat:'tunes', name:'Shave and a Haircut', desc:'For foul balls, bad calls, and comic timing.', tag:'rimshot energy', src:'samples/tunes/shave-haircut.wav'},
  {cat:'tunes', name:'Habanera Vamp', desc:'Not quite Bizet, but ballpark spooky.', tag:'dramatic', src:'samples/tunes/habanera-vamp.wav'}
];
```

- [ ] **Step 4: Verify no references to deleted paths remain**

```bash
grep -n "generated-extra\|wikimedia-real\|charge-crowd\|samples/[a-z-]*\.wav" index.html
```
Expected: no output (root-level `samples/*.wav` are gone; only `samples/tunes/*.wav` and `samples/freesound|real/*.mp3` remain).

- [ ] **Step 5: Commit**

```bash
git add index.html
git commit -m "feat: two-section organ-only soundboard page"
```

---

### Task 6: Rewrite ATTRIBUTION.md

**Files:**
- Modify: `ATTRIBUTION.md` (full rewrite)

- [ ] **Step 1: Rewrite the file**

Structure (fill the `samples/real/` section from `samples/real/sources.json`):

```markdown
# Sample Attributions

All audio on this board is either a verified CC0/CC-BY recording (credited below)
or a public-domain melody rendered through the FluidR3_GM soundfont.

## Freesound (samples/freesound/)

- **Real Baseball Organ**: "baseball organ" by treblebooster, CC0. https://freesound.org/people/treblebooster/sounds/151373/
- **Real Cavalry Short**: "Baseball cavalry sting short sustain.wav" by vckhaze, CC0. https://freesound.org/people/vckhaze/sounds/380695/
- **Real Cavalry Long**: "Baseball calvary sting long sustain.wav" by vckhaze, CC0. https://freesound.org/people/vckhaze/sounds/380696/
- **Real Play Ball**: "Play Ball!.wav" by CGEffex, CC BY. https://freesound.org/people/CGEffex/sounds/101137/

## Additional real recordings (samples/real/)

<!-- one bullet per sources.json entry: **Title** by Author, License. URL -->

## Rendered tunes (samples/tunes/)

Public-domain/traditional melodies written as MIDI (sources in `midi/`) and rendered
with FluidSynth through the **FluidR3_GM** soundfont by Frank Wen (MIT license).
The Habanera Vamp is an original phrase. Re-render with `npm run render`
(requires fluidsynth and tools/FluidR3_GM.sf2 — see docs/superpowers/plans/2026-06-13-organ-revamp.md Task 2).
```

- [ ] **Step 2: Commit**

```bash
git add ATTRIBUTION.md
git commit -m "docs: attribution for organ-only sample set"
```

---

### Task 7: Verification script, listening QA, push

**Files:**
- Create: `verify_samples.js`

- [ ] **Step 1: Create `verify_samples.js`**

```js
// verify_samples.js — every src in index.html's songs array must exist on disk,
// and every audio file on disk must be referenced (no orphans).
const fs = require('fs');
const path = require('path');

const html = fs.readFileSync(path.join(__dirname, 'index.html'), 'utf8');
const srcs = [...html.matchAll(/src:'(samples\/[^']+)'/g)].map(m => m[1]);

let fail = false;
for (const src of srcs) {
  if (!fs.existsSync(path.join(__dirname, src))) {
    console.error(`MISSING FILE: ${src}`);
    fail = true;
  }
}

const onDisk = [];
(function walk(dir) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p);
    else if (/\.(wav|mp3)$/i.test(e.name)) onDisk.push(path.relative(__dirname, p).replace(/\\/g, '/'));
  }
})(path.join(__dirname, 'samples'));
for (const f of onDisk) {
  if (!srcs.includes(f)) {
    console.error(`ORPHAN FILE (on disk, not on the board): ${f}`);
    fail = true;
  }
}

console.log(`${srcs.length} pads checked, ${onDisk.length} audio files on disk.`);
process.exit(fail ? 1 : 0);
```

- [ ] **Step 2: Run it**

```bash
node verify_samples.js
```
Expected: `N pads checked, N audio files on disk.` and exit 0 (counts equal — sources.json is not an audio file). Fix any MISSING/ORPHAN before continuing.

- [ ] **Step 3: Serve the page locally for the user's listening pass**

```bash
npx -y serve -l 8123 . &
```
Tell the user: open `http://localhost:8123`, click every pad, and report any tune with wrong notes. Fix reported tunes by editing `tunes.js`, re-running `node render_tunes.js`, and re-committing. **This is a user checkpoint — wait for their feedback before pushing.**

- [ ] **Step 4: Commit and push**

```bash
git add verify_samples.js
git commit -m "test: sample/page consistency check"
git push origin main
```
