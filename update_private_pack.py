#!/usr/bin/env python3
from pathlib import Path
import re, shutil, zipfile, json
ROOT = Path(__file__).resolve().parent
ZIP = ROOT/'incoming'/'stadium-organ-music.zip'
PACK = ROOT/'samples'/'user-stadium-organ'
PACK.mkdir(parents=True, exist_ok=True)

TITLE_MAP = {
 'workingman':'Working Man', 'letsgocrazy':'Let’s Go Crazy', 'sevennationarmy':'Seven Nation Army', 'oyecomova':'Oye Como Va', 'africa':'Africa', 'dangerzone':'Danger Zone', 'yankeedoodle':'Yankee Doodle', 'drunkensailor':'Drunken Sailor', 'downunder':'Down Under', 'knightsofcydonia':'Knights of Cydonia', 'tarantella':'Tarantella', 'kingofthehill':'King of the Hill', 'nanaheyhey':'Na Na Hey Hey', 'rhythmisgonnagetyou':'Rhythm Is Gonna Get You', 'girluwant':'Girl U Want', 'chinagrove':'China Grove', 'masterofpuppets':'Master of Puppets', 'walkthisway':'Walk This Way', 'letsgo':'Let’s Go', 'grapevine':'Grapevine', 'yellowroseoftexas':'Yellow Rose of Texas', 'backinblack':'Back in Black', 'ballroomblitz':'Ballroom Blitz', 'sweetcaroline':'Sweet Caroline', 'hustle':'The Hustle', 'tequila':'Tequila', 'batman':'Batman', 'mrbluesky':'Mr. Blue Sky', 'smokeonthewater':'Smoke on the Water', 'entersandman':'Enter Sandman', 'godzilla':'Godzilla', 'mysharona':'My Sharona', 'whatislove':'What Is Love', 'jump':'Jump', 'feelssogood':'Feels So Good', 'wildthing':'Wild Thing', 'imperialmarch':'Imperial March', 'warpigs':'War Pigs', 'alouette':'Alouette', 'spanishflea':'Spanish Flea', 'buddyholly':'Buddy Holly', 'duelingbanjos':'Dueling Banjos', 'zootsuitriot':'Zoot Suit Riot', 'twilightzone':'Twilight Zone', 'itsnotunusual':'It’s Not Unusual', 'startmeup':'Start Me Up', 'irishwasherwoman':'Irish Washerwoman', 'addamsfamily':'Addams Family', 'lagrange':'La Grange', 'vengabus':'Vengabus', 'shedrivesmecrazy':'She Drives Me Crazy', 'finalcountdown':'Final Countdown', 'livinonaprayer':'Livin’ on a Prayer', 'muppetshow':'Muppet Show', 'readyforthis':'Get Ready for This', 'tomsawyer':'Tom Sawyer', 'jamesbond':'James Bond', 'beerbarrelpolka':'Beer Barrel Polka', 'korobeiniki':'Korobeiniki', 'killinginthename':'Killing in the Name', 'thingthatshouldnotbe':'The Thing That Should Not Be', 'kernkraft400':'Kernkraft 400', 'imblue':'I’m Blue', 'moneyfornothing':'Money for Nothing', 'heyjude':'Hey Jude', 'anchorsaweigh':'Anchors Aweigh'
}
SAFE_PD = {'yankeedoodle','drunkensailor','tarantella','yellowroseoftexas','alouette','irishwasherwoman','korobeiniki','anchorsaweigh','beerbarrelpolka'}

def slugify(s):
    s = s.replace("'", '').replace('’','')
    return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')

entries = []
if ZIP.exists():
    with zipfile.ZipFile(ZIP) as z:
        for info in z.infolist():
            name = info.filename
            if not name.startswith('Stadium Organ Music/') or not name.lower().endswith('.ogg'):
                continue
            base = Path(name).stem
            key = re.sub(r'[^a-z0-9]+','',base.lower())
            title = TITLE_MAP.get(key) or re.sub(r'(?<!^)([A-Z])', r' \1', base).replace('_',' ').title()
            outname = f"pack-{slugify(title)}.ogg"
            dest = PACK/outname
            with z.open(info) as src, dest.open('wb') as dst:
                shutil.copyfileobj(src, dst)
            entries.append({
                'cat':'userpack',
                'name':title,
                'desc':'Private-use stadium organ recording from Eric’s pack.' if key not in SAFE_PD else 'User-provided stadium organ recording.',
                'tag':'private pack' if key not in SAFE_PD else 'traditional',
                'src':f'samples/user-stadium-organ/{outname}'
            })

# Keep standalone Telegram attachments, already transcoded to mp3.
attachments = [
 ('Down-Up Sting','samples/user-stadium-organ/user-down-up-sting.mp3'),
 ('Big Chord','samples/user-stadium-organ/user-big-chord.mp3'),
 ('Italian Organ','samples/user-stadium-organ/user-italian-organ.mp3'),
 ('Hat Dance','samples/user-stadium-organ/user-hat-dance.mp3'),
 ('Da-Da-Da Up','samples/user-stadium-organ/user-da-da-da-up.mp3'),
]
for title, src in attachments:
    if (ROOT/src).exists():
        entries.append({'cat':'userpack','name':title,'desc':'User-provided stadium organ WAV, normalized for the board.','tag':'attached','src':src})

entries = sorted(entries, key=lambda x: x['name'].lower())
(ROOT/'userpack-songs.json').write_text(json.dumps(entries, indent=2)+"\n")
print('userpack entries', len(entries))
