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
  return 'fluidsynth'; // assume on PATH
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
  const midiPath = path.join(__dirname, 'midi', `${tune.file}.mid`);
  const wavPath = path.join(__dirname, 'samples', 'tunes', `${tune.file}.wav`);
  fs.writeFileSync(midiPath, Buffer.from(new MidiWriter.Writer([melody, chords]).buildFile()));
  execFileSync(fluidsynth, ['-ni', '-g', '0.8', '-F', wavPath, '-r', '44100', SOUNDFONT, midiPath]);
  const kb = Math.round(fs.statSync(wavPath).size / 1024);
  console.log(`${tune.file}: midi + ${kb} KB wav`);
}
console.log(`Rendered ${tunes.length} tunes.`);
