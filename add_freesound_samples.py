#!/usr/bin/env python3
import pathlib, requests
ROOT=pathlib.Path(__file__).resolve().parent
OUT=ROOT/'samples'/'freesound'
OUT.mkdir(parents=True, exist_ok=True)
SAMPLES=[
  ('real-baseball-organ.mp3','https://cdn.freesound.org/previews/151/151373_2657167-hq.mp3','Baseball Organ','baseball organ','treblebooster','CC0','https://freesound.org/people/treblebooster/sounds/151373/'),
  ('real-cavalry-short.mp3','https://cdn.freesound.org/previews/380/380695_167075-hq.mp3','Cavalry Sting Short','Baseball cavalry sting short sustain.wav','vckhaze','CC0','https://freesound.org/people/vckhaze/sounds/380695/'),
  ('real-cavalry-long.mp3','https://cdn.freesound.org/previews/380/380696_167075-hq.mp3','Cavalry Sting Long','Baseball calvary sting long sustain.wav','vckhaze','CC0','https://freesound.org/people/vckhaze/sounds/380696/'),
  ('real-play-ball.mp3','https://cdn.freesound.org/previews/101/101137_1386366-hq.mp3','Play Ball','Play Ball!.wav','CGEffex','CC BY','https://freesound.org/people/CGEffex/sounds/101137/'),
  ('real-charge-crowd.mp3','https://cdn.freesound.org/previews/191/191928_923993-hq.mp3','Charge with Crowd','WALLA_Ballpark Organ Cheering Charge','AshFox','CC BY','https://freesound.org/people/AshFox/sounds/191928/'),
  ('real-lets-go.mp3','https://cdn.freesound.org/previews/191/191923_923993-hq.mp3','Let’s Go Crowd Organ','WALLA Ballpark Let\'s Go Organ','AshFox','CC BY','https://freesound.org/people/AshFox/sounds/191923/'),
  ('real-take-me-out.mp3','https://cdn.freesound.org/previews/191/191927_923993-hq.mp3','Take Me Out, Stadium Recording','WALLA Ballpark Organ Take Me Out to the Ballgame','AshFox','CC BY','https://freesound.org/people/AshFox/sounds/191927/'),
  ('real-bat-crowd.mp3','https://cdn.freesound.org/previews/214/214989_4023430-hq.mp3','Bat Crack + Crowd','BaseballHitAndCrowdCheer.mp3','AmishRob','CC BY','https://freesound.org/people/AmishRob/sounds/214989/'),
]
for fn,url,*_ in SAMPLES:
    path=OUT/fn
    if not path.exists():
        r=requests.get(url,timeout=30)
        r.raise_for_status()
        path.write_bytes(r.content)
        print('downloaded',path)
lines=['# Sample Attributions','', 'This project uses a mix of locally generated organ WAV files and the following Freesound samples. CC-BY samples require attribution; CC0 samples do not require attribution but are credited anyway.','']
for fn,url,label,title,author,lic,page in SAMPLES:
    lines.append(f'- **{label}**: "{title}" by {author}, {lic}. Source: {page}')
(ROOT/'ATTRIBUTION.md').write_text('\n'.join(lines)+'\n')
print('wrote attribution')
