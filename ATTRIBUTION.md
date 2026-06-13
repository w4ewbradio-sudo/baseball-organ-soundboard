# Sample Attributions

The page is now a casual private-use GitHub Pages soundboard protected by a client-side passphrase gate. Static-page passphrase protection is not equivalent to server-side authentication, but it keeps the board out of casual public browsing.

## Freesound (samples/freesound/)

- **Real Baseball Organ**: "baseball organ" by treblebooster, CC0. https://freesound.org/people/treblebooster/sounds/151373/
- **Real Cavalry Short**: "Baseball cavalry sting short sustain.wav" by vckhaze, CC0. https://freesound.org/people/vckhaze/sounds/380695/
- **Real Cavalry Long**: "Baseball calvary sting long sustain.wav" by vckhaze, CC0. https://freesound.org/people/vckhaze/sounds/380696/
- **Real Play Ball**: "Play Ball!.wav" by CGEffex, CC BY. https://freesound.org/people/CGEffex/sounds/101137/

## Additional real recordings (samples/real/)

- **Leslie Cabinet Slow-Fast-Slow** by Wikipedia user wikipedia-ce, Public Domain. https://commons.wikimedia.org/wiki/File:LeslieCabinetSlowFastSlow.ogg
- **Leslie Cabinet Sequence** by Wikipedia user wikipedia-ce, Public Domain. https://commons.wikimedia.org/wiki/File:LezlieCabinetSequence.ogg
- **Drawbar Organ C Chord** by Shadowcelibi, Public Domain. https://commons.wikimedia.org/wiki/File:Drawbar_C_Chord.ogg
- **Hammond Organ - Model A Medley** by Nathaniel C. Wilcox (Organgrinder010), CC BY 3.0. https://commons.wikimedia.org/wiki/File:Hammond_Organ_-_Model_A_Medley.ogg

## Eric's stadium organ pack (samples/user-stadium-organ/)

Eric provided `Stadium Organ Music.zip` from Google Drive plus five standalone WAV attachments. The private soundboard includes the full stadium organ pack and the five attached WAVs, normalized/transcoded where needed.

The passphrase is intentionally handled in `index.html` for a static GitHub Pages deployment. If the project needs real access control later, move it behind server-side authentication or a private hosting layer.

## Rendered tunes (samples/tunes/)

Public-domain/traditional melodies written as MIDI (sources in `midi/`) and rendered with FluidSynth through the **FluidR3_GM** soundfont by Frank Wen (MIT license). The Habanera Vamp is an original phrase. Re-render with `npm run render` (requires fluidsynth and tools/FluidR3_GM.sf2, see docs/superpowers/plans/2026-06-13-organ-revamp.md Task 2).
