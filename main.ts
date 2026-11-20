import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const png = readFileSync(new URL('./edition.png', import.meta.url));
const signature = Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]);
if (png.length < 33 || png.length > 1_048_576 || !png.subarray(0, 8).equals(signature)) {
  throw new Error('Expected a complete PNG within the one MiB entry limit');
}
const width = png.readUInt32BE(16);
const height = png.readUInt32BE(20);
if (width < 1 || width > 1024 || height < 1 || height > 1024) {
  throw new Error('Image dimensions exceed the entry limits');
}
const destination = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(destination, { recursive: true });
writeFileSync(join(destination, 'entry.png'), png);
