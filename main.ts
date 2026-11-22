// news-image-20261122: "The World Today — Sunday 22 November 2026".
// A 1024x1024 newsprint front page summing up the day's world news:
// Iran strikes US bases in Bahrain, COP31 nears a deal at dawn,
// Russia's 400-drone barrage, the Peru quake, the Sparta II ablaze,
// chip stocks plunging 10%, and 34 more stories from 7 regions.
// The page was composed by compose.py (see that file for the layout)
// and is shipped here as base64 text in entry.png.b64, so this
// program is deterministic and needs no network: it just decodes
// the image to /output/entry.png.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
// /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = dirname(fileURLToPath(import.meta.url));
const b64 = readFileSync(join(root, 'entry.png.b64'), 'utf8').trim();
const bytes = Buffer.from(b64, 'base64');

// The gate allows at most 1 MiB and 1024x1024: fail loudly here instead
// of shipping an image the scorer would refuse.
if (bytes.length > 1048576) {
  throw new Error(`entry image is ${bytes.length} bytes, over the 1 MiB gate`);
}
if (bytes[0] !== 0x89 || bytes[1] !== 0x50 || bytes[2] !== 0x4e || bytes[3] !== 0x47) {
  throw new Error('entry image is not a PNG');
}

// PNG IHDR: width at bytes 16-19, height at 20-23, big-endian.
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width > 1024 || height > 1024) {
  throw new Error(`entry image is ${width}x${height}, over the 1024x1024 gate`);
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, 'entry.png'), bytes);
console.log(`wrote entry.png: ${bytes.length} bytes`);
