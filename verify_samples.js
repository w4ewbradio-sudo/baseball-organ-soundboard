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
    else if (/\.(wav|mp3|ogg)$/i.test(e.name)) onDisk.push(path.relative(__dirname, p).replace(/\\/g, '/'));
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
