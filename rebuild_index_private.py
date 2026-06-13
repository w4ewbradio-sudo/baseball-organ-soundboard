#!/usr/bin/env python3
from pathlib import Path
import json
ROOT = Path(__file__).resolve().parent
userpack = json.loads((ROOT/'userpack-songs.json').read_text())
real = [
 {'cat':'real','name':'Real Baseball Organ','desc':'CC0 Freesound organ clip by treblebooster.','tag':'CC0','src':'samples/freesound/real-baseball-organ.mp3'},
 {'cat':'real','name':'Real Cavalry Short','desc':'CC0 baseball cavalry sting by vckhaze.','tag':'CC0','src':'samples/freesound/real-cavalry-short.mp3'},
 {'cat':'real','name':'Real Cavalry Long','desc':'CC0 baseball cavalry sting by vckhaze.','tag':'CC0','src':'samples/freesound/real-cavalry-long.mp3'},
 {'cat':'real','name':'Real Play Ball','desc':'CC-BY old-time play ball organ by CGEffex.','tag':'CC BY','src':'samples/freesound/real-play-ball.mp3'},
 {'cat':'real','name':'Hammond Leslie Sweep','desc':'Public-domain Hammond through a Leslie cabinet, slow-fast-slow.','tag':'PD','src':'samples/real/hammond-leslie-slow-fast-slow.ogg'},
 {'cat':'real','name':'Hammond Leslie Sequence','desc':'Public-domain Hammond/Leslie speaker sequence.','tag':'PD','src':'samples/real/hammond-leslie-sequence.ogg'},
 {'cat':'real','name':'Drawbar Organ Chord','desc':'Public-domain drawbar organ C-chord sting.','tag':'PD','src':'samples/real/drawbar-organ-c-chord.ogg'},
 {'cat':'real','name':'Hammond Model A Medley','desc':'CC-BY 1935 Hammond Model A performance by Nathaniel C. Wilcox.','tag':'CC BY','src':'samples/real/hammond-model-a-medley.ogg'},
]
tunes = [
 {'cat':'tunes','name':'Charge!','desc':'The classic da-da-da-DUH rally fanfare.','tag':'organ','src':'samples/tunes/charge.wav'},
 {'cat':'tunes','name':'Take Me Out to the Ball Game','desc':'The essential ballpark chorus.','tag':'1908 classic','src':'samples/tunes/take-me-out.wav'},
 {'cat':'tunes','name':'When the Saints','desc':'Brassy, happy, impossible not to grin.','tag':'public domain','src':'samples/tunes/saints.wav'},
 {'cat':'tunes','name':'Camptown Races','desc':'Old-timey sprint around the bases.','tag':'public domain','src':'samples/tunes/camptown.wav'},
 {'cat':'tunes','name':'The Entertainer','desc':'Ragtime concession-stand chaos.','tag':'public domain','src':'samples/tunes/entertainer.wav'},
 {'cat':'tunes','name':'Mexican Hat Dance','desc':'Mascot race fuel.','tag':'traditional','src':'samples/tunes/mexican-hat.wav'},
 {'cat':'tunes','name':'Yankee Doodle','desc':'Patriotic baseball-adjacent silliness.','tag':'public domain','src':'samples/tunes/yankee-doodle.wav'},
 {'cat':'tunes','name':'Pop Goes the Weasel','desc':'For pitching changes and other nonsense.','tag':'public domain','src':'samples/tunes/pop-weasel.wav'},
 {'cat':'tunes','name':'Shave and a Haircut','desc':'For foul balls, bad calls, and comic timing.','tag':'rimshot energy','src':'samples/tunes/shave-haircut.wav'},
 {'cat':'tunes','name':'Habanera Vamp','desc':'Not quite Bizet, but ballpark spooky.','tag':'dramatic','src':'samples/tunes/habanera-vamp.wav'},
]
songs = real + userpack + tunes
html = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Private Ballpark Organ Soundboard</title>
  <style>
    :root{{--grass:#0f5f3b;--grass2:#073b27;--dirt:#b36b38;--cream:#fff4d7;--ink:#102018;--red:#c8272d;--blue:#133d7a;--gold:#ffd166;--panel:rgba(255,244,215,.94)}}
    *{{box-sizing:border-box}} body{{margin:0;min-height:100vh;font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:var(--ink);background:radial-gradient(circle at 50% 0%,rgba(255,255,255,.35),transparent 35%),repeating-linear-gradient(90deg,var(--grass) 0 80px,var(--grass2) 80px 160px)}}
    body:before{{content:"";position:fixed;inset:auto 0 0;height:34vh;background:linear-gradient(145deg,transparent 0 38%,#d79555 38% 62%,transparent 62%),linear-gradient(215deg,transparent 0 38%,#d79555 38% 62%,transparent 62%);opacity:.45;pointer-events:none}} main{{width:min(1120px,94vw);margin:auto;padding:34px 0 60px;position:relative;z-index:1}}
    .hero{{text-align:center;color:white;text-shadow:0 3px 12px #0008;margin-bottom:22px}} .badge{{display:inline-block;background:var(--red);color:white;border:3px solid white;border-radius:999px;padding:7px 14px;font-weight:900;letter-spacing:.08em;text-transform:uppercase;box-shadow:0 8px 22px #0004}} .hero h1{{font-size:clamp(2.4rem,8vw,5.4rem);line-height:.9;margin:18px 0 8px;letter-spacing:-.06em}} .hero p{{font-size:1.1rem;margin:0 auto;max-width:720px;color:#fff8}}
    .scoreboard{{background:#14251c;color:#f8f2d3;border:8px solid #273a31;border-radius:26px;padding:18px;box-shadow:0 20px 60px #0008;margin:24px 0}} .now{{display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap}} .lights{{display:flex;gap:8px}} .light{{width:18px;height:18px;border-radius:50%;background:#31443a;box-shadow:inset 0 2px 4px #0008}} .playing .light{{background:var(--gold);box-shadow:0 0 16px var(--gold)}} #nowPlaying{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;text-transform:uppercase;letter-spacing:.08em}}
    .stop,.lock button{{border:0;border-radius:16px;background:var(--red);color:white;font-size:1.05rem;font-weight:950;padding:14px 22px;cursor:pointer;box-shadow:0 8px 0 #7c1519}} .stop:active,.lock button:active{{transform:translateY(5px);box-shadow:0 3px 0 #7c1519}} .section-title{{color:white;text-shadow:0 2px 8px #0008;margin:28px 0 12px;font-size:1.4rem}} .grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:14px}}
    .pad{{border:4px solid #e7d5a6;background:var(--panel);border-radius:22px;padding:18px;min-height:142px;text-align:left;cursor:pointer;box-shadow:0 10px 0 #c99b62,0 22px 34px #0004;transition:.12s transform,.12s box-shadow;position:relative;overflow:hidden}} .pad:before{{content:"♪";position:absolute;right:14px;top:2px;font-size:4rem;color:rgba(19,61,122,.08);font-weight:900}} .pad:hover{{transform:translateY(-3px);box-shadow:0 13px 0 #c99b62,0 26px 36px #0005}} .pad:active,.pad.active{{transform:translateY(7px);box-shadow:0 3px 0 #c99b62,0 10px 24px #0004}} .pad strong{{display:block;font-size:1.08rem;line-height:1.1;margin:0 36px 8px 0}} .pad small{{color:#536457}} .tag{{display:inline-block;margin-top:10px;background:#e7f0ff;color:var(--blue);border-radius:999px;padding:4px 8px;font-weight:800;font-size:.72rem}}
    .star{{position:absolute;right:12px;bottom:10px;border:0;background:#fff8;border-radius:999px;font-size:1.25rem;line-height:1;padding:8px;cursor:pointer;color:#91712e;z-index:2}} .star.on{{background:var(--gold);color:#3b2600}} #favoriteWrap.empty{{display:none}} .footer{{margin-top:28px;background:rgba(255,255,255,.82);border-radius:20px;padding:14px 16px;color:#334}} .volume{{display:flex;align-items:center;gap:12px}} .volume input{{accent-color:var(--red);width:180px}}
    .lock{{position:fixed;inset:0;z-index:10;display:grid;place-items:center;background:linear-gradient(135deg,#071b13,#102018 60%,#2b130f);color:white;padding:24px}} .lock-card{{width:min(440px,92vw);background:rgba(255,255,255,.09);border:1px solid rgba(255,255,255,.2);border-radius:24px;padding:28px;box-shadow:0 20px 70px #0009;text-align:center}} .lock h1{{margin:0 0 10px;font-size:2rem}} .lock p{{color:#fffc;margin:0 0 18px;line-height:1.5}} .lock input{{width:100%;border:3px solid #ffffff55;border-radius:14px;padding:14px 16px;font-size:1.1rem;margin-bottom:14px;background:#fff;color:#111}} .lock .err{{min-height:1.4em;color:#ffd166;font-weight:800}} .hidden{{display:none!important}}
    @media(max-width:620px){{.now{{display:block}}.stop{{width:100%;margin-top:14px}}.grid{{grid-template-columns:1fr 1fr}}.pad{{min-height:160px;padding:14px}}.hero h1{{font-size:3.1rem}}}}
  </style>
</head>
<body>
<div class="lock" id="lockScreen">
  <div class="lock-card">
    <div class="badge">Private booth</div>
    <h1>Ballpark Organ</h1>
    <p>Enter the passphrase to open Eric’s private soundboard.</p>
    <form id="unlockForm">
      <input id="passphrase" type="password" autocomplete="current-password" placeholder="Passphrase" autofocus />
      <button type="submit">Unlock</button>
      <div class="err" id="lockError"></div>
    </form>
  </div>
</div>
<main id="app" class="hidden">
  <section class="hero"><span class="badge">Private press box</span><h1>Ballpark Organ</h1><p>A private browser soundboard for walk-ups, rallies, heckles, crowd noise, and deeply unserious baseball moments.</p></section>
  <section class="scoreboard" id="scoreboard"><div class="now"><div><div class="lights"><span class="light"></span><span class="light"></span><span class="light"></span></div><h2 id="nowPlaying">Ready in the booth</h2></div><div class="volume"><label for="volume">Volume</label><input id="volume" type="range" min="0" max="1" step=".01" value=".7"></div><button class="stop" id="stopBtn">■ STOP</button></div></section>
  <div id="favoriteWrap" class="empty"><h2 class="section-title">★ Favorites</h2><section class="grid" id="favorites"></section></div>
  <h2 class="section-title">Real organ recordings</h2><section class="grid" id="real"></section>
  <h2 class="section-title">Eric's stadium organ pack</h2><section class="grid" id="userpack"></section>
  <h2 class="section-title">Classic tunes (sampled organ)</h2><section class="grid" id="tunes"></section>
  <p class="footer">This is a casual private GitHub Pages soundboard. The passphrase gate keeps normal visitors out, but static files are not equivalent to server-side authentication. Favorites are saved in this browser only.</p>
</main>
<script>
const PASS_PHRASE = 'Mellwood1774Ave';
const songs = {json.dumps(songs, ensure_ascii=False, indent=2)};
let currentAudio=null, activePad=null;
const favoriteKey='ballpark-organ-favorites-v1';
function favorites(){{ try{{return new Set(JSON.parse(localStorage.getItem(favoriteKey)||'[]'));}}catch{{return new Set();}} }}
function saveFavorites(set){{ localStorage.setItem(favoriteKey, JSON.stringify([...set])); }}
function stop(){{ if(currentAudio){{currentAudio.pause();currentAudio.currentTime=0;currentAudio=null;}} document.getElementById('scoreboard').classList.remove('playing'); document.getElementById('nowPlaying').textContent='Ready in the booth'; if(activePad) activePad.classList.remove('active'); activePad=null; }}
function play(song,pad){{ stop(); activePad=pad; pad.classList.add('active'); document.getElementById('scoreboard').classList.add('playing'); document.getElementById('nowPlaying').textContent='Now playing: '+song.name; currentAudio=new Audio(song.src); currentAudio.volume=document.getElementById('volume').value; currentAudio.onended=stop; currentAudio.play().catch(err=>{{document.getElementById('nowPlaying').textContent='Tap again, browser blocked autoplay'; console.warn(err);}}); }}
function makePad(song){{ const faves=favorites(); const card=document.createElement('div'); card.className='pad'; card.tabIndex=0; card.setAttribute('role','button'); card.setAttribute('aria-label','Play '+song.name); card.innerHTML=`<strong>${{song.name}}</strong><small>${{song.desc}}</small><span class="tag">${{song.tag}}</span>`; const star=document.createElement('button'); star.className='star'+(faves.has(song.src)?' on':''); star.type='button'; star.title='Favorite'; star.textContent=faves.has(song.src)?'★':'☆'; star.onclick=(e)=>{{e.stopPropagation(); const set=favorites(); if(set.has(song.src)) set.delete(song.src); else set.add(song.src); saveFavorites(set); render();}}; card.appendChild(star); card.onclick=()=>play(song,card); card.onkeydown=(e)=>{{ if(e.key==='Enter'||e.key===' '){{e.preventDefault();play(song,card);}} }}; return card; }}
function fill(id,items){{ const el=document.getElementById(id); el.innerHTML=''; items.forEach(s=>el.appendChild(makePad(s))); }}
function render(){{ const set=favorites(); const favSongs=songs.filter(s=>set.has(s.src)); document.getElementById('favoriteWrap').classList.toggle('empty', favSongs.length===0); fill('favorites', favSongs); fill('real', songs.filter(s=>s.cat==='real')); fill('userpack', songs.filter(s=>s.cat==='userpack')); fill('tunes', songs.filter(s=>s.cat==='tunes')); }}
function unlock(){{ document.getElementById('lockScreen').classList.add('hidden'); document.getElementById('app').classList.remove('hidden'); sessionStorage.setItem('ballparkUnlocked','1'); render(); }}
document.getElementById('unlockForm').addEventListener('submit', e=>{{ e.preventDefault(); if(document.getElementById('passphrase').value===PASS_PHRASE) unlock(); else document.getElementById('lockError').textContent='Nope. Check the passphrase.'; }});
if(sessionStorage.getItem('ballparkUnlocked')==='1') unlock();
document.getElementById('stopBtn').onclick=stop; document.getElementById('volume').oninput=e=>{{ if(currentAudio) currentAudio.volume=e.target.value; }};
</script>
</body>
</html>
'''
(ROOT/'index.html').write_text(html)
print('wrote index with', len(songs), 'songs')
