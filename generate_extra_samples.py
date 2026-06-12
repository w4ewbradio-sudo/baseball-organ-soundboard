#!/usr/bin/env python3
import math,wave,struct,pathlib,random
ROOT=pathlib.Path(__file__).resolve().parent
OUT=ROOT/'samples'/'generated-extra'; OUT.mkdir(parents=True,exist_ok=True)
SR=44100
SEMI={'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}
def hz(note):
    if note is None: return None
    name=note[0]; octave=int(note[-1]); acc=note[1:-1]
    return 440*2**(((octave+1)*12+SEMI[name]+(1 if acc=='#' else -1 if acc=='b' else 0)-69)/12)
def write(path,samples):
    peak=max(.01,max(abs(x) for x in samples)); pcm=[int(max(-1,min(1,x/peak*.84))*32767) for x in samples]
    with wave.open(str(path),'w') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(b''.join(struct.pack('<h',x) for x in pcm))
def organ(freq,t,dur):
    vib=1+0.007*math.sin(2*math.pi*6.1*t); x=0
    for m,a in [(1,.55),(2,.22),(3,.15),(5,.07),(8,.035)]: x+=a*math.sin(2*math.pi*freq*m*vib*t)
    env=min(1,t/.015)*min(1,max(0,(dur-t)/.09))
    return math.tanh(2.0*x)*env
def render_song(slug,tempo,notes,beats):
    beat=60/tempo; out=[]
    for note,b in zip(notes,beats):
        dur=b*beat; n=int(dur*SR); f=hz(note)
        if not f: out += [0]*n; continue
        for i in range(n):
            t=i/SR; out.append(organ(f,t,dur)*.75+organ(f/2,t,dur)*.16)
    delay=int(.055*SR)
    for i in range(delay,len(out)): out[i]+=out[i-delay]*.13
    write(OUT/f'{slug}.wav',out)
def noise_burst(slug,dur,kind):
    random.seed(slug); n=int(dur*SR); out=[]
    for i in range(n):
        t=i/SR
        if kind=='cheer':
            env=min(1,t/.18)*min(1,max(0,(dur-t)/.9)); val=sum(math.sin(2*math.pi*(180+random.random()*1600)*t+random.random()*6) for _ in range(6))/6
            val+=random.uniform(-1,1)*.55; out.append(val*env)
        elif kind=='boo':
            env=min(1,t/.25)*min(1,max(0,(dur-t)/.8)); val=sum(math.sin(2*math.pi*(110+random.random()*180)*t+random.random()*6) for _ in range(5))/5
            out.append((val+random.uniform(-.25,.25))*env)
        elif kind=='bat':
            env=math.exp(-t*38); val=random.uniform(-1,1)*env + math.sin(2*math.pi*2500*t)*env*.35
            out.append(val)
        elif kind=='ump':
            env=min(1,t/.04)*min(1,max(0,(dur-t)/.18)); val=math.sin(2*math.pi*290*t)+.35*math.sin(2*math.pi*580*t)
            out.append(val*env)
    write(OUT/f'{slug}.wav',out)
# More public-domain/traditional stadium-style motifs
render_song('organ-william-tell',152,['E4','E4','E4','C4','E4','G4','G4','G4','E4','G4','C5','G4','E4'],[.25,.25,.25,.25,.25,.5,.25,.25,.25,.25,.5,.5,1])
render_song('organ-here-we-go',124,['C4','E4','G4','C5',None,'C5','G4','E4','C4'],[.35,.35,.35,.7,.25,.35,.35,.35,1])
render_song('organ-rally-clap',132,['G4','G4',None,'G4','G4',None,'C5','C5','C5'],[.25,.25,.15,.25,.25,.15,.25,.25,.8])
render_song('organ-suspense',92,['C4','Db4','D4','Eb4','E4','F4','Gb4','G4'],[.45,.45,.45,.45,.45,.45,.45,1])
render_song('organ-victory',140,['C5','E5','G5','C6','G5','C6'],[.25,.25,.25,.6,.25,1])
render_song('organ-error-sad',96,['G4','F#4','F4','E4','Eb4','D4','C4'],[.35,.35,.35,.35,.35,.35,1])
render_song('organ-batter-up',116,['C4','E4','G4','Bb4','C5','Bb4','G4','E4','C4'],[.35,.35,.35,.35,.7,.35,.35,.35,1])
noise_burst('crowd-cheer-safe',2.4,'cheer')
noise_burst('crowd-boo-safe',2.1,'boo')
noise_burst('bat-crack-safe',.55,'bat')
noise_burst('ump-strike-safe',.75,'ump')
print('wrote extras to',OUT)
