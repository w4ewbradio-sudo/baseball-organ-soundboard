#!/usr/bin/env python3
import math, wave, struct, pathlib
ROOT=pathlib.Path(__file__).resolve().parent
OUT=ROOT/'samples'
OUT.mkdir(exist_ok=True)
SR=44100
SONGS = [
  ('charge','Charge!',150,['G4','C5','E5','G5','E5','G5'],[.5,.5,.5,.9,.25,1.2]),
  ('shave-and-a-haircut','Shave and a Haircut',135,['C5','G4','G4','A4','G4',None,'B4','C5'],[.5,.25,.25,.5,.5,.35,.5,.9]),
  ('lets-go-team','Let’s Go Team',120,['C4','E4','G4','G4','A4','G4','E4','C4'],[.5,.5,.5,.5,.5,.5,.5,1]),
  ('strikeout-sting','Strikeout Sting',150,['E5','Eb5','D5','C5','G4','C5'],[.25,.25,.25,.45,.25,.9]),
  ('safe','Safe!',145,['C5','E5','G5','C6'],[.25,.25,.25,1]),
  ('uh-oh','Uh Oh...',105,['C5','B4','Bb4','A4','Ab4','G4'],[.35,.35,.35,.35,.35,1]),
  ('walk-up-swagger','Walk-Up Swagger',118,['C4','Eb4','F4','Gb4','G4','Bb4','G4','F4','Eb4','C4'],[.35,.35,.35,.35,.7,.35,.35,.35,.35,.9]),
  ('seventh-inning-wiggle','Seventh Inning Wiggle',100,['C4','E4','G4','C5','G4','E4','D4','F4','A4','D5','A4','F4'],[.5,.5,.5,.5,.5,.5,.5,.5,.5,.5,.5,1]),
  ('take-me-out','Take Me Out to the Ball Game',118,['C4','C5','A4','G4','E4','G4','D4',None,'C4','C5','A4','G4','E4','G4','D4',None,'E4','F4','F#4','G4','A4','G4','E4','D4','C4'],[.5,.5,.5,.5,.5,.5,1,.4,.5,.5,.5,.5,.5,.5,1,.4,.35,.35,.35,.5,.5,.5,.5,.5,1.2]),
  ('when-the-saints','When the Saints',112,['C4','E4','F4','G4',None,'C4','E4','F4','G4',None,'C4','E4','F4','G4','E4','C4','E4','D4'],[.5,.5,.5,1,.3,.5,.5,.5,1,.3,.5,.5,.5,.7,.5,.5,.5,1]),
  ('camptown-races','Camptown Races',150,['G4','G4','E4','G4','A4','G4','E4','D4','C4','D4','E4','C4','D4','D4'],[.35,.35,.35,.35,.35,.35,.35,.35,.5,.5,.5,.5,.5,1]),
  ('the-entertainer','The Entertainer',132,['D4','D#4','E4','C5','E4','C5','E4','C5','C5','B4','A4','G4','A4','B4'],[.25,.25,.25,.5,.25,.5,.25,.5,.35,.35,.35,.35,.35,1]),
  ('mexican-hat-dance','Mexican Hat Dance',150,['G4','C5','C5','C5','D5','E5','E5','E5','F5','E5','D5','C5','B4','C5'],[.35,.35,.35,.35,.35,.35,.35,.35,.35,.35,.35,.35,.35,1]),
  ('yankee-doodle','Yankee Doodle',130,['C4','C4','D4','E4','C4','E4','D4','G3','C4','C4','D4','E4','C4','B3'],[.45,.45,.45,.45,.45,.45,.75,.45,.45,.45,.45,.45,.45,1]),
  ('pop-goes-the-weasel','Pop Goes the Weasel',136,['C4','C4','D4','D4','E4','G4','E4','C4','C4','C4','D4','D4','E4','C4'],[.4,.4,.4,.4,.4,.4,.4,.4,.4,.4,.4,.4,.4,1]),
  ('habanera-vamp','Habanera-ish Vamp',110,['D4','C#4','C4','B3','A#3','A3','G4','F4','E4','D4'],[.5,.5,.5,.5,.5,.5,.5,.5,.5,1]),
]
SEMI={'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}
def hz(note):
    if note is None: return None
    name=note[0]; octave=int(note[-1]); acc=note[1:-1]
    s=SEMI[name]+(1 if acc=='#' else -1 if acc=='b' else 0)
    midi=(octave+1)*12+s
    return 440*2**((midi-69)/12)
def organ_sample(freq,t,dur):
    # Cheesy stadium organ: square-ish harmonics, vibrato, clicky attack, soft release.
    vib=1+0.006*math.sin(2*math.pi*5.8*t)
    x=0
    for mult,amp in [(1,0.55),(2,0.24),(3,0.14),(4,0.08),(6,0.04)]:
        x += amp*math.sin(2*math.pi*freq*mult*vib*t)
    # mild overdrive
    x=math.tanh(1.9*x)
    attack=min(1,t/0.018)
    release=min(1,max(0,(dur-t)/0.08))
    env=attack*release
    return x*env
def render(slug,name,tempo,notes,beats):
    beat=60/tempo
    samples=[]
    for note,b in zip(notes,beats):
        dur=b*beat
        n=int(dur*SR)
        f=hz(note)
        if f is None:
            samples.extend([0]*n)
            continue
        for i in range(n):
            t=i/SR
            # add octave below faintly for real organ thickness
            val=organ_sample(f,t,dur)*0.78 + organ_sample(f/2,t,dur)*0.18
            samples.append(val)
    # tiny room slapback/reverb
    delay=int(0.07*SR)
    wet=samples[:]
    for i in range(delay,len(wet)):
        wet[i]+=0.18*wet[i-delay]
    peak=max(0.01,max(abs(x) for x in wet))
    pcm=[int(max(-1,min(1,x/peak*0.82))*32767) for x in wet]
    path=OUT/f'{slug}.wav'
    with wave.open(str(path),'w') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(b''.join(struct.pack('<h',x) for x in pcm))
    print(path)
for slug,name,tempo,notes,beats in SONGS:
    render(slug,name,tempo,notes,beats)
