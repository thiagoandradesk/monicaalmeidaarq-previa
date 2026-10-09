#!/usr/bin/env node
/**
 * Monta um contact sheet (mosaico com rótulos) de todas as imagens de uma pasta,
 * para curadoria visual. Saída em qa/.
 *
 * Uso: node scripts/contact-sheet.mjs [pasta=assets-originais] [saida=qa/contact-sheet.jpg] [colunas=4] [largura=360]
 */
import sharp from 'sharp';
import { readdir } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const raiz = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const [pastaArg = 'assets-originais', saidaArg = 'qa/contact-sheet.jpg', colsArg = '4', wArg = '360'] = process.argv.slice(2);
const pasta = path.resolve(raiz, pastaArg);
const saida = path.resolve(raiz, saidaArg);
const cols = +colsArg;
const W = +wArg;
const H = W; // célula quadrada (imagens em contain)
const ROTULO = 28;
const GAP = 12;

const arquivos = (await readdir(pasta))
  .filter((f) => /\.(jpe?g|png|webp|avif)$/i.test(f))
  .sort();

const celulas = [];
for (const f of arquivos) {
  const img = sharp(path.join(pasta, f));
  const meta = await img.metadata();
  const buf = await img
    .resize(W, H, { fit: 'contain', background: '#dddad2' })
    .jpeg({ quality: 82 })
    .toBuffer();
  const texto = `${f.replace(/\.[^.]+$/, '')}  ${meta.width}×${meta.height}`;
  const svg = Buffer.from(
    `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${ROTULO}">
      <rect width="100%" height="100%" fill="#222"/>
      <text x="6" y="19" font-family="Arial, Helvetica, sans-serif" font-size="13" fill="#fff">${texto}</text>
    </svg>`
  );
  const celula = await sharp({
    create: { width: W, height: H + ROTULO, channels: 3, background: '#222' },
  })
    .composite([
      { input: buf, top: 0, left: 0 },
      { input: svg, top: H, left: 0 },
    ])
    .jpeg({ quality: 82 })
    .toBuffer();
  celulas.push(celula);
}

const linhas = Math.ceil(celulas.length / cols);
const totalW = cols * W + (cols + 1) * GAP;
const totalH = linhas * (H + ROTULO) + (linhas + 1) * GAP;
const composites = celulas.map((input, i) => ({
  input,
  left: GAP + (i % cols) * (W + GAP),
  top: GAP + Math.floor(i / cols) * (H + ROTULO + GAP),
}));
await sharp({ create: { width: totalW, height: totalH, channels: 3, background: '#111' } })
  .composite(composites)
  .jpeg({ quality: 80 })
  .toFile(saida);
console.log(`${celulas.length} imagens → ${path.relative(raiz, saida)} (${totalW}×${totalH})`);
