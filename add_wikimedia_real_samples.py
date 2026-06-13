#!/usr/bin/env python3
import pathlib, subprocess, urllib.request, json, os
ROOT = pathlib.Path(__file__).resolve().parent
RAW = ROOT/'samples'/'wikimedia-raw'
OUT = ROOT/'samples'/'wikimedia-real'
RAW.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)
SAMPLES = [
  {
    'slug':'real-metal-bat','title':'Fake Metal Bat','button':'Real Metal Bat','creator':'Shawn Eary','license':'CC0 1.0','license_url':'https://creativecommons.org/publicdomain/zero/1.0/deed.en/','source':'https://commons.wikimedia.org/w/index.php?curid=157421110','url':'https://upload.wikimedia.org/wikipedia/commons/4/4c/Fake_Metal_Bat.wav','start':0,'duration':0.48,
    'desc':'CC0 real metal-bat hit from Wikimedia Commons.'
  },
  {
    'slug':'real-race-crowd-air-horns','title':'F1-Race-Crowd-Applause-Air-Horns','button':'Real Crowd + Horns','creator':'WebbFilmsUK','license':'CC BY 4.0','license_url':'https://creativecommons.org/licenses/by/4.0/','source':'https://commons.wikimedia.org/w/index.php?curid=166556390','url':'https://upload.wikimedia.org/wikipedia/commons/9/94/F1-Race-Crowd-Applause-Air-Horns.wav','start':0,'duration':8,
    'desc':'CC-BY real sports crowd with applause and air horns.'
  },
  {
    'slug':'real-stadium-crowd','title':'WWS FootballAustriavs.Sweden','button':'Real Stadium Crowd','creator':'Work With Sounds / Torsten Nilsson','license':'CC BY 4.0','license_url':'https://creativecommons.org/licenses/by/4.0/','source':'https://commons.wikimedia.org/w/index.php?curid=38096966','url':'https://upload.wikimedia.org/wikipedia/commons/e/ec/WWS_FootballAustriavs.Sweden.ogg','start':22,'duration':8,
    'desc':'CC-BY real stadium crowd ambience from Wikimedia Commons.'
  },
]

def download(url, dest):
    if dest.exists() and dest.stat().st_size > 1000: return
    req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0 Marvin soundboard builder'})
    with urllib.request.urlopen(req, timeout=60) as r:
        dest.write_bytes(r.read())

manifest=[]
for s in SAMPLES:
    ext = s['url'].split('?')[0].rsplit('.',1)[-1]
    raw = RAW/(s['slug']+'.'+ext)
    out = OUT/(s['slug']+'.mp3')
    print('download', s['title'])
    download(s['url'], raw)
    cmd = ['ffmpeg','-y','-hide_banner','-loglevel','error','-ss',str(s['start']),'-i',str(raw),'-t',str(s['duration']),'-af','loudnorm=I=-16:LRA=11:TP=-1.5,afade=t=out:st='+str(max(0.1,s['duration']-.25))+':d=0.25','-codec:a','libmp3lame','-q:a','4',str(out)]
    subprocess.run(cmd, check=True)
    s2 = dict(s)
    s2['file'] = 'samples/wikimedia-real/'+out.name
    s2.pop('url')
    manifest.append(s2)
(ROOT/'wikimedia-real-manifest.json').write_text(json.dumps(manifest, indent=2)+"\n")
print('wrote', len(manifest), 'real Wikimedia samples')
